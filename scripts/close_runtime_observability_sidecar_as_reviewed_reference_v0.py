#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_RUNTIME_OBSERVABILITY_SIDECAR_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "runtime.observability_sidecar.reference_closure.v0"
LAYER = "RUNTIME / OBSERVATION / REFERENCE_CLOSURE"
MODE = "CLOSE_ONLY / FREEZE_REVIEWED_REFERENCE / NO_LIVE_HOOKS"
BUILD_MODE = "RUNTIME_OBSERVABILITY_SIDECAR_REFERENCE_CLOSURE_ONLY"

SOURCE_REVIEW_RECEIPT_ID = "3bc9850a"
SOURCE_BUILD_RECEIPT_ID = "7a63137f"
SOURCE_REPAIR_RECEIPT_ID = "480cf138"
SOURCE_FAILED_BUILD_RECEIPT_ID = "84aec9df"
SOURCE_DESIGN_RECEIPT_ID = "37628e11"
SOURCE_POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_ID = "1ca1e03b"
SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID = "732016f0"
SOURCE_EDGE_OBSERVABILITY_CLOSURE_RECEIPT_ID = "ac09c2e3"

REVIEW_RECEIPT_PATH = ROOT / "data/runtime_observability_sidecar_review_v0_receipts/3bc9850a.json"
BUILD_RECEIPT_PATH = ROOT / "data/runtime_observability_sidecar_v0_receipts/7a63137f.json"
REPAIR_RECEIPT_PATH = ROOT / "data/runtime_observability_sidecar_build_repair_v0_receipts/480cf138.json"
FAILED_BUILD_RECEIPT_PATH = ROOT / "data/runtime_observability_sidecar_v0_receipts/84aec9df.json"
DESIGN_RECEIPT_PATH = ROOT / "data/runtime_observability_sidecar_target_from_schema_validator_and_observability_references_v0_receipts/37628e11.json"
POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_PATH = ROOT / "data/post_runtime_schema_validator_reference_decision_v0_receipts/1ca1e03b.json"
SCHEMA_VALIDATOR_CLOSURE_RECEIPT_PATH = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0_receipts/732016f0.json"
EDGE_OBSERVABILITY_CLOSURE_RECEIPT_PATH = ROOT / "data/decision_edge_observability_reference_closure_from_bounded_c6_adoption_probe_reference_v0_receipts/ac09c2e3.json"

REVIEW_DIR = ROOT / "data/runtime_observability_sidecar_review_v0"
BUILD_DIR = ROOT / "data/runtime_observability_sidecar_v0"
REPAIR_DIR = ROOT / "data/runtime_observability_sidecar_build_repair_v0"
DESIGN_DIR = ROOT / "data/runtime_observability_sidecar_target_from_schema_validator_and_observability_references_v0"
SCHEMA_VALIDATOR_REF_DIR = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0"
EDGE_OBS_REF_DIR = ROOT / "data/decision_edge_observability_reference_closure_from_bounded_c6_adoption_probe_reference_v0"

REVIEW_ARTIFACTS = [
    REVIEW_DIR / "runtime_observability_sidecar_review_basis_v0.json",
    REVIEW_DIR / "runtime_observability_sidecar_source_build_receipt_review_v0.json",
    REVIEW_DIR / "runtime_observability_sidecar_source_repair_receipt_review_v0.json",
    REVIEW_DIR / "runtime_observability_sidecar_failed_build_review_v0.json",
    REVIEW_DIR / "runtime_observability_sidecar_artifact_inventory_review_v0.json",
    REVIEW_DIR / "runtime_observability_sidecar_schema_surface_review_v0.json",
    REVIEW_DIR / "runtime_observability_sidecar_event_record_review_v0.json",
    REVIEW_DIR / "runtime_observability_sidecar_append_only_trace_review_v0.json",
    REVIEW_DIR / "runtime_observability_sidecar_unknown_hook_gap_review_v0.json",
    REVIEW_DIR / "runtime_observability_sidecar_forbidden_control_claim_review_v0.json",
    REVIEW_DIR / "runtime_observability_sidecar_negative_control_review_v0.json",
    REVIEW_DIR / "runtime_observability_sidecar_load_bearing_field_review_v0.json",
    REVIEW_DIR / "runtime_observability_sidecar_boundary_review_v0.json",
    REVIEW_DIR / "runtime_observability_sidecar_reviewed_reference_close_candidate_v0.json",
    REVIEW_DIR / "runtime_observability_sidecar_review_authority_boundary_v0.json",
    REVIEW_DIR / "runtime_observability_sidecar_review_classification_v0.json",
    REVIEW_DIR / "runtime_observability_sidecar_review_rollup_v0.json",
    REVIEW_DIR / "runtime_observability_sidecar_review_profile_v0.json",
    REVIEW_DIR / "runtime_observability_sidecar_review_report.json",
    REVIEW_DIR / "runtime_observability_sidecar_review_transition_trace.json",
]

BUILD_ARTIFACTS = [
    BUILD_DIR / "runtime_observability_sidecar_hook_registry_v0.json",
    BUILD_DIR / "runtime_observability_sidecar_event_record_schema_v0.json",
    BUILD_DIR / "runtime_observability_sidecar_receipt_schema_v0.json",
    BUILD_DIR / "runtime_observability_sidecar_append_only_trace_schema_v0.json",
    BUILD_DIR / "runtime_observability_sidecar_rollup_readout_profile_schema_v0.json",
    BUILD_DIR / "runtime_observability_sidecar_demo_event_inputs_v0.jsonl",
    BUILD_DIR / "runtime_observability_sidecar_event_records_v0.jsonl",
    BUILD_DIR / "runtime_observability_sidecar_append_only_trace_v0.jsonl",
    BUILD_DIR / "runtime_observability_sidecar_unknown_hook_records_v0.jsonl",
    BUILD_DIR / "runtime_observability_sidecar_hook_gap_records_v0.jsonl",
    BUILD_DIR / "runtime_observability_sidecar_forbidden_control_claim_records_v0.jsonl",
    BUILD_DIR / "runtime_observability_sidecar_rollup_v0.json",
    BUILD_DIR / "runtime_observability_sidecar_readout_v0.json",
    BUILD_DIR / "runtime_observability_sidecar_profile_v0.json",
    BUILD_DIR / "runtime_observability_sidecar_report.json",
    BUILD_DIR / "runtime_observability_sidecar_transition_trace.json",
]

REPAIR_ARTIFACTS = [
    REPAIR_DIR / "runtime_observability_sidecar_build_patch_record_v0.json",
    REPAIR_DIR / "runtime_observability_sidecar_build_repair_basis_v0.json",
    REPAIR_DIR / "runtime_observability_sidecar_build_repair_classification_v0.json",
]

REFERENCE_SOURCE_ARTIFACTS = [
    DESIGN_DIR / "runtime_observability_sidecar_target_spec_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_build_target_v0.json",
    SCHEMA_VALIDATOR_REF_DIR / "runtime_schema_validator_reviewed_reference_v0.json",
    SCHEMA_VALIDATOR_REF_DIR / "runtime_schema_validator_observability_hook_reference_v0.json",
    EDGE_OBS_REF_DIR / "decision_edge_observability_reviewed_reference_v0.json",
    EDGE_OBS_REF_DIR / "decision_edge_observability_requirement_reference_v0.json",
]

REQUIRED_SOURCE_FILES = [
    REVIEW_RECEIPT_PATH,
    BUILD_RECEIPT_PATH,
    REPAIR_RECEIPT_PATH,
    FAILED_BUILD_RECEIPT_PATH,
    DESIGN_RECEIPT_PATH,
    POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_PATH,
    SCHEMA_VALIDATOR_CLOSURE_RECEIPT_PATH,
    EDGE_OBSERVABILITY_CLOSURE_RECEIPT_PATH,
] + REVIEW_ARTIFACTS + BUILD_ARTIFACTS + REPAIR_ARTIFACTS + REFERENCE_SOURCE_ARTIFACTS

OUT_DIR = ROOT / "data/runtime_observability_sidecar_reference_closure_v0"
RECEIPT_DIR = ROOT / "data/runtime_observability_sidecar_reference_closure_v0_receipts"

CLOSURE_BASIS_PATH = OUT_DIR / "runtime_observability_sidecar_reference_closure_basis_v0.json"
REVIEW_CONSUMPTION_PATH = OUT_DIR / "runtime_observability_sidecar_review_consumption_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "runtime_observability_sidecar_reviewed_reference_v0.json"
FREEZE_MANIFEST_PATH = OUT_DIR / "runtime_observability_sidecar_reviewed_reference_freeze_manifest_v0.json"
REFERENCE_INDEX_PATH = OUT_DIR / "runtime_observability_sidecar_reference_index_v0.json"
HOOK_REGISTRY_REFERENCE_PATH = OUT_DIR / "runtime_observability_sidecar_hook_registry_reference_v0.json"
EVENT_RECORD_REFERENCE_PATH = OUT_DIR / "runtime_observability_sidecar_event_record_reference_v0.json"
APPEND_ONLY_TRACE_REFERENCE_PATH = OUT_DIR / "runtime_observability_sidecar_append_only_trace_reference_v0.json"
UNKNOWN_HOOK_GAP_REFERENCE_PATH = OUT_DIR / "runtime_observability_sidecar_unknown_hook_gap_reference_v0.json"
FORBIDDEN_CONTROL_REFERENCE_PATH = OUT_DIR / "runtime_observability_sidecar_forbidden_control_reference_v0.json"
LOAD_BEARING_FIELD_REFERENCE_PATH = OUT_DIR / "runtime_observability_sidecar_load_bearing_field_reference_v0.json"
NEGATIVE_CONTROL_REFERENCE_PATH = OUT_DIR / "runtime_observability_sidecar_negative_control_reference_v0.json"
PRE_C8_INTERLOCK_COMPLETION_PATH = OUT_DIR / "pre_c8_interlock_completion_reference_v0.json"
POST_CLOSURE_DECISION_READY_PATH = OUT_DIR / "post_runtime_observability_sidecar_reference_decision_ready_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "runtime_observability_sidecar_reference_closure_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "runtime_observability_sidecar_reference_closure_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_observability_sidecar_reference_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_observability_sidecar_reference_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "runtime_observability_sidecar_reference_closure_report.json"
TRACE_PATH = OUT_DIR / "runtime_observability_sidecar_reference_closure_transition_trace.json"

EXPECTED_REVIEW_STATUS = "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_REVIEWED_CLOSE_READY"
EXPECTED_REVIEW_STOP = "STOP_TYPED_RUNTIME_OBSERVABILITY_SIDECAR_REVIEWED_CLOSE_READY"
EXPECTED_REVIEW_NEXT = UNIT_ID

RECOMMENDED_NEXT = "DECIDE_NEXT_AFTER_RUNTIME_OBSERVABILITY_SIDECAR_REFERENCE_CLOSURE_V0"

REQUIRED_EDGE_FIELDS = [
    "active_object",
    "attempted_move",
    "boundary_checked",
    "boundary_result",
    "blocked_moves",
    "lawful_next_moves",
    "source_packet_ref",
]

EXPECTED_EVENT_STATUS_COUNTS = {
    "RECORDED": 4,
    "OBSERVATION_HOOK_UNKNOWN": 1,
    "OBSERVABILITY_HOOK_GAP": 1,
    "CONTROL_AUTHORITY_FORBIDDEN": 1,
    "AUTHORITY_CLAIM_FORBIDDEN": 1,
    "ADMISSIBILITY_CLAIM_FORBIDDEN": 1,
    "EXECUTION_CLAIM_FORBIDDEN": 1,
    "REPAIR_CLAIM_FORBIDDEN": 1,
    "UNBOUNDED_PAYLOAD_FORBIDDEN": 1,
    "SOURCE_MUTATION_FORBIDDEN": 1,
    "RUNTIME_PATCH_FORBIDDEN": 1,
    "LIVE_HOOK_INSTALL_FORBIDDEN": 1,
    "C8_AUTHORIZATION_FORBIDDEN": 1,
}

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
    review_summary = review_receipt.get("machine_readable_runtime_observability_sidecar_review_summary", {})
    build_receipt = read_json(BUILD_RECEIPT_PATH)
    build_summary = build_receipt.get("machine_readable_runtime_observability_sidecar_build_summary", {})
    repair_receipt = read_json(REPAIR_RECEIPT_PATH)
    failed_build_receipt = read_json(FAILED_BUILD_RECEIPT_PATH)
    design_receipt = read_json(DESIGN_RECEIPT_PATH)
    post_schema_validator_decision_receipt = read_json(POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_PATH)
    schema_validator_closure_receipt = read_json(SCHEMA_VALIDATOR_CLOSURE_RECEIPT_PATH)
    edge_observability_closure_receipt = read_json(EDGE_OBSERVABILITY_CLOSURE_RECEIPT_PATH)

    close_candidate = read_json(REVIEW_DIR / "runtime_observability_sidecar_reviewed_reference_close_candidate_v0.json")
    review_authority = read_json(REVIEW_DIR / "runtime_observability_sidecar_review_authority_boundary_v0.json")
    review_classification = read_json(REVIEW_DIR / "runtime_observability_sidecar_review_classification_v0.json")
    review_rollup = read_json(REVIEW_DIR / "runtime_observability_sidecar_review_rollup_v0.json")
    review_profile = read_json(REVIEW_DIR / "runtime_observability_sidecar_review_profile_v0.json")
    review_report = read_json(REVIEW_DIR / "runtime_observability_sidecar_review_report.json")
    review_trace = read_json(REVIEW_DIR / "runtime_observability_sidecar_review_transition_trace.json")

    hook_registry = read_json(BUILD_DIR / "runtime_observability_sidecar_hook_registry_v0.json")
    event_record_schema = read_json(BUILD_DIR / "runtime_observability_sidecar_event_record_schema_v0.json")
    sidecar_receipt_schema = read_json(BUILD_DIR / "runtime_observability_sidecar_receipt_schema_v0.json")
    append_only_trace_schema = read_json(BUILD_DIR / "runtime_observability_sidecar_append_only_trace_schema_v0.json")
    event_records = read_jsonl(BUILD_DIR / "runtime_observability_sidecar_event_records_v0.jsonl")
    append_only_trace = read_jsonl(BUILD_DIR / "runtime_observability_sidecar_append_only_trace_v0.jsonl")
    unknown_hook_records = read_jsonl(BUILD_DIR / "runtime_observability_sidecar_unknown_hook_records_v0.jsonl")
    hook_gap_records = read_jsonl(BUILD_DIR / "runtime_observability_sidecar_hook_gap_records_v0.jsonl")
    forbidden_control_claim_records = read_jsonl(BUILD_DIR / "runtime_observability_sidecar_forbidden_control_claim_records_v0.jsonl")
    build_rollup = read_json(BUILD_DIR / "runtime_observability_sidecar_rollup_v0.json")
    build_readout = read_json(BUILD_DIR / "runtime_observability_sidecar_readout_v0.json")
    build_profile = read_json(BUILD_DIR / "runtime_observability_sidecar_profile_v0.json")

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
        "runtime_observability_sidecar_reviewed",
        "close_ready",
        "source_build_receipt_consumed",
        "source_repair_receipt_consumed",
        "source_failed_build_receipt_consumed_as_context",
        "schema_surface_reviewed",
        "event_records_reviewed",
        "append_only_trace_reviewed",
        "unknown_hook_gap_reviewed",
        "forbidden_control_claims_reviewed",
        "load_bearing_fields_confirmed",
        "negative_controls_zero_confirmed",
        "synthetic_reference_build_only",
        "runtime_observability_sidecar_built",
        "unit_feedback_hardening_deferred",
        "c7_deferred",
        "c8_deferred",
        "runtime_adoption_deferred",
        "bad_counters_zero",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"review_required_true_missing:{key}")

    for key in [
        "live_runtime_hooks_installed",
        "live_runtime_routing_installed",
        "runtime_effect",
        "runtime_patched",
        "validation_verdict_emitted",
        "authority_checked",
        "admissibility_checked",
        "authorization_verdict_emitted",
        "execution_claimed",
        "execution_command_emitted",
        "schema_archive_mutated",
        "proposal_repaired",
        "schema_created",
        "builder_command_emitted",
        "control_path_blocked",
        "control_path_advanced",
        "c7_authorized",
        "c8_authorized",
        "new_domain_shift_executed",
        "general_cell1_authority_claimed",
        "global_autonomy_claimed",
        "full_transfer_claimed",
        "runtime_wide_enforcement_claimed",
        "source_mutated",
        "prior_receipt_mutated",
        "schema_validator_reference_mutated",
        "observability_reference_mutated",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if review_summary.get(key) is not False:
            failures.append(f"review_forbidden_true:{key}")

    for key, expected in {
        "events_observed": 16,
        "events_recorded": 16,
        "append_only_trace_entries": 16,
        "unknown_hook_count": 1,
        "hook_gap_count": 1,
        "forbidden_control_claim_record_count": 10,
        "hook_count": 24,
        "load_bearing_edge_field_count": 7,
    }.items():
        if review_summary.get(key) != expected:
            failures.append(f"review_count_wrong:{key}:{review_summary.get(key)}")

    if review_summary.get("event_status_counts") != EXPECTED_EVENT_STATUS_COUNTS:
        failures.append("review_event_status_counts_wrong")

    if close_candidate.get("candidate_status") != "RUNTIME_OBSERVABILITY_SIDECAR_REVIEWED_REFERENCE_CLOSE_READY":
        failures.append("close_candidate_not_ready")
    if close_candidate.get("recommended_close_unit") != UNIT_ID:
        failures.append("close_candidate_next_wrong")
    if review_authority.get("may_close_observability_sidecar_as_reviewed_reference_next") is not True:
        failures.append("review_authority_close_not_allowed")
    if review_classification.get("next_command_goal") is not None:
        failures.append("review_classification_hidden_next")
    if review_rollup.get("review_count") != 1:
        failures.append("review_rollup_count_wrong")
    if review_profile.get("review_result") != "REVIEWED_CLOSE_READY":
        failures.append("review_profile_not_ready")
    if review_profile.get("next_command_goal") is not None:
        failures.append("review_profile_hidden_next")
    if review_report.get("recommended_next_handling") != UNIT_ID:
        failures.append("review_report_next_wrong")
    if review_trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("review_trace_hidden_next")

    if build_receipt.get("receipt_id") != SOURCE_BUILD_RECEIPT_ID or build_receipt.get("gate") != "PASS":
        failures.append("build_receipt_not_pass")
    if build_summary.get("status") != "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_BUILT_REVIEW_READY":
        failures.append("build_status_wrong")
    if repair_receipt.get("receipt_id") != SOURCE_REPAIR_RECEIPT_ID or repair_receipt.get("gate") != "PASS":
        failures.append("repair_receipt_not_pass")
    if failed_build_receipt.get("receipt_id") != SOURCE_FAILED_BUILD_RECEIPT_ID or failed_build_receipt.get("gate") != "FAIL":
        failures.append("failed_build_receipt_not_context_fail")
    if design_receipt.get("receipt_id") != SOURCE_DESIGN_RECEIPT_ID or design_receipt.get("gate") != "PASS":
        failures.append("design_receipt_not_pass")
    if post_schema_validator_decision_receipt.get("receipt_id") != SOURCE_POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_ID or post_schema_validator_decision_receipt.get("gate") != "PASS":
        failures.append("post_schema_validator_decision_not_pass")
    if schema_validator_closure_receipt.get("receipt_id") != SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID or schema_validator_closure_receipt.get("gate") != "PASS":
        failures.append("schema_validator_closure_not_pass")
    if edge_observability_closure_receipt.get("receipt_id") != SOURCE_EDGE_OBSERVABILITY_CLOSURE_RECEIPT_ID or edge_observability_closure_receipt.get("gate") != "PASS":
        failures.append("edge_observability_closure_not_pass")

    if hook_registry.get("hook_count") != 24:
        failures.append("hook_registry_count_wrong")
    if hook_registry.get("dynamic_registration_allowed") is not False:
        failures.append("hook_registry_dynamic_registration_allowed")
    if any(h.get("live_hook_installed") is not False for h in hook_registry.get("hooks", [])):
        failures.append("hook_registry_live_hook_installed")

    if event_record_schema.get("required_load_bearing_edge_fields") != REQUIRED_EDGE_FIELDS:
        failures.append("event_record_schema_edge_fields_wrong")
    if append_only_trace_schema.get("append_only") is not True:
        failures.append("append_only_trace_schema_not_append_only")
    if len(event_records) != 16:
        failures.append("event_records_count_wrong")
    if len(append_only_trace) != 16:
        failures.append("trace_count_wrong")
    if len(unknown_hook_records) != 1:
        failures.append("unknown_hook_count_wrong")
    if len(hook_gap_records) != 1:
        failures.append("hook_gap_count_wrong")
    if len(forbidden_control_claim_records) != 10:
        failures.append("forbidden_control_count_wrong")
    if build_rollup.get("events_recorded") != 16:
        failures.append("build_rollup_events_wrong")
    if build_readout.get("bad_counters_zero") is not True:
        failures.append("build_readout_bad_counters_not_zero")
    if build_profile.get("control_path_effect") != "NONE":
        failures.append("build_profile_control_path_effect_wrong")

    return failures, {
        "review_summary": review_summary,
        "build_summary": build_summary,
        "close_candidate": close_candidate,
        "hook_registry": hook_registry,
        "event_record_schema": event_record_schema,
        "sidecar_receipt_schema": sidecar_receipt_schema,
        "append_only_trace_schema": append_only_trace_schema,
        "event_records": event_records,
        "append_only_trace": append_only_trace,
        "unknown_hook_records": unknown_hook_records,
        "hook_gap_records": hook_gap_records,
        "forbidden_control_claim_records": forbidden_control_claim_records,
        "build_rollup": build_rollup,
        "build_readout": build_readout,
        "build_profile": build_profile,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    closure_pass = not failures
    status = "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY" if closure_pass else "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_REFERENCE_CLOSURE_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if closure_pass else "REPAIR_RUNTIME_OBSERVABILITY_SIDECAR_REFERENCE_CLOSURE_V0"

    review_summary = basis.get("review_summary", {})
    build_summary = basis.get("build_summary", {})
    hook_registry = basis.get("hook_registry", {})
    event_records = basis.get("event_records", [])
    append_only_trace = basis.get("append_only_trace", [])
    unknown_hook_records = basis.get("unknown_hook_records", [])
    hook_gap_records = basis.get("hook_gap_records", [])
    forbidden_control_claim_records = basis.get("forbidden_control_claim_records", [])
    build_rollup = basis.get("build_rollup", {})
    build_profile = basis.get("build_profile", {})

    reason_codes = [
        "RUNTIME_OBSERVABILITY_SIDECAR_CLOSED_AS_REVIEWED_REFERENCE",
        "REVIEW_RECEIPT_CONSUMED",
        "BUILD_RECEIPT_CONSUMED",
        "REPAIR_RECEIPT_CONSUMED",
        "FAILED_BUILD_RECEIPT_CONSUMED_AS_CONTEXT",
        "DESIGN_RECEIPT_CONSUMED",
        "SCHEMA_VALIDATOR_REFERENCE_CONSUMED",
        "DECISION_EDGE_OBSERVABILITY_REFERENCE_CONSUMED",
        "HOOK_REGISTRY_REFERENCE_FROZEN",
        "EVENT_RECORD_REFERENCE_FROZEN",
        "APPEND_ONLY_TRACE_REFERENCE_FROZEN",
        "UNKNOWN_HOOK_GAP_REFERENCE_FROZEN",
        "FORBIDDEN_CONTROL_REFERENCE_FROZEN",
        "LOAD_BEARING_FIELD_REFERENCE_FROZEN",
        "NEGATIVE_CONTROL_REFERENCE_FROZEN",
        "PRE_C8_INTERLOCK_PAIR_COMPLETE",
        "POST_SIDECAR_REFERENCE_DECISION_READY",
        "CONTROL_PATH_ACTS_SIDECAR_RECORDS",
        "SIDECAR_HAS_EYES_NOT_HANDS",
        "NO_LIVE_HOOK_INSTALL",
        "NO_RUNTIME_EFFECT",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_RUNTIME_ROUTING",
        "NO_VALIDATION_AUTHORITY",
        "NO_ADMISSIBILITY_AUTHORITY",
        "NO_AUTHORIZATION_AUTHORITY",
        "NO_EXECUTION_CLAIM",
        "NO_CONTROL_PATH_BLOCK_OR_ADVANCE",
        "NO_SCHEMA_MUTATION",
        "NO_PROPOSAL_REPAIR",
        "NO_BUILDER_COMMAND",
        "NO_C7_AUTHORIZATION",
        "NO_C8_AUTHORIZATION",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if closure_pass else failures

    source_hash_manifest = snapshot_files(REQUIRED_SOURCE_FILES)

    closure_basis = {
        "schema_version": "runtime_observability_sidecar_reference_closure_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if closure_pass else "BASIS_REPAIR_REQUIRED",
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "source_build_receipt_id": SOURCE_BUILD_RECEIPT_ID,
        "source_repair_receipt_id": SOURCE_REPAIR_RECEIPT_ID,
        "source_failed_build_receipt_id": SOURCE_FAILED_BUILD_RECEIPT_ID,
        "source_design_receipt_id": SOURCE_DESIGN_RECEIPT_ID,
        "source_schema_validator_reference_closure_receipt_id": SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID,
        "source_decision_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBSERVABILITY_CLOSURE_RECEIPT_ID,
        "closure_scope": "freeze synthetic Runtime Observability Sidecar surface as reviewed reference",
        "closure_does_not_mean": [
            "live runtime hooks installed",
            "runtime routing patched",
            "runtime patched",
            "Sidecar validates",
            "Sidecar authorizes",
            "Sidecar admits",
            "Sidecar executes",
            "Sidecar blocks or advances control path",
            "C8 authorized",
        ],
    }

    review_consumption = {
        "schema_version": "runtime_observability_sidecar_review_consumption_v0",
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "review_status": review_summary.get("status"),
        "close_ready": review_summary.get("close_ready"),
        "review_consumed_without_mutation": True,
    }

    reviewed_reference = {
        "schema_version": "runtime_observability_sidecar_reviewed_reference_v0",
        "reference_status": "RUNTIME_OBSERVABILITY_SIDECAR_REVIEWED_REFERENCE_FROZEN" if closure_pass else "NOT_FROZEN",
        "sidecar_id": "RUNTIME_OBSERVABILITY_SIDECAR",
        "mode": "OBSERVE / EMIT_RECEIPT / APPEND_ONLY",
        "core_compression": "Control path acts. Sidecar records.",
        "authority_law": "The sidecar has eyes, not hands.",
        "role": "synthetic/reference append-only observation surface for predefined runtime event hooks",
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "source_build_receipt_id": SOURCE_BUILD_RECEIPT_ID,
        "source_repair_receipt_id": SOURCE_REPAIR_RECEIPT_ID,
        "source_design_receipt_id": SOURCE_DESIGN_RECEIPT_ID,
        "source_schema_validator_reference_closure_receipt_id": SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID,
        "source_decision_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBSERVABILITY_CLOSURE_RECEIPT_ID,
        "hook_count": review_summary.get("hook_count"),
        "events_recorded": review_summary.get("events_recorded"),
        "append_only_trace_entries": review_summary.get("append_only_trace_entries"),
        "unknown_hook_count": review_summary.get("unknown_hook_count"),
        "hook_gap_count": review_summary.get("hook_gap_count"),
        "forbidden_control_claim_record_count": review_summary.get("forbidden_control_claim_record_count"),
        "load_bearing_edge_field_count": review_summary.get("load_bearing_edge_field_count"),
        "event_status_counts": review_summary.get("event_status_counts"),
        "negative_controls_zero": review_summary.get("negative_controls_zero_confirmed"),
        "control_path_effect": "NONE",
        "synthetic_reference_build_only": True,
        "live_runtime_hooks_installed": False,
        "runtime_patched": False,
        "c8_authorized": False,
        "must_not_infer": [
            "Sidecar is live runtime instrumentation",
            "Runtime hooks were installed",
            "Runtime routing was patched",
            "Runtime was patched",
            "Sidecar can validate",
            "Sidecar can authorize",
            "Sidecar can admit",
            "Sidecar can execute",
            "Sidecar can block control path",
            "Sidecar can advance control path",
            "C8 is authorized",
        ],
    }

    freeze_manifest = {
        "schema_version": "runtime_observability_sidecar_reviewed_reference_freeze_manifest_v0",
        "freeze_status": "FROZEN" if closure_pass else "NOT_FROZEN",
        "reference_id": "runtime_observability_sidecar_reviewed_reference_v0",
        "reference_path": rel(REVIEWED_REFERENCE_PATH),
        "source_hash_manifest": source_hash_manifest,
        "frozen_artifacts": {
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "hook_registry_reference": rel(HOOK_REGISTRY_REFERENCE_PATH),
            "event_record_reference": rel(EVENT_RECORD_REFERENCE_PATH),
            "append_only_trace_reference": rel(APPEND_ONLY_TRACE_REFERENCE_PATH),
            "unknown_hook_gap_reference": rel(UNKNOWN_HOOK_GAP_REFERENCE_PATH),
            "forbidden_control_reference": rel(FORBIDDEN_CONTROL_REFERENCE_PATH),
            "load_bearing_field_reference": rel(LOAD_BEARING_FIELD_REFERENCE_PATH),
            "negative_control_reference": rel(NEGATIVE_CONTROL_REFERENCE_PATH),
            "pre_c8_interlock_completion": rel(PRE_C8_INTERLOCK_COMPLETION_PATH),
        },
    }

    reference_index = {
        "schema_version": "runtime_observability_sidecar_reference_index_v0",
        "index_status": "REFERENCE_INDEX_EMITTED" if closure_pass else "NOT_EMITTED",
        "entries": [
            {"name": "reviewed_reference", "path": rel(REVIEWED_REFERENCE_PATH)},
            {"name": "hook_registry_reference", "path": rel(HOOK_REGISTRY_REFERENCE_PATH)},
            {"name": "event_record_reference", "path": rel(EVENT_RECORD_REFERENCE_PATH)},
            {"name": "append_only_trace_reference", "path": rel(APPEND_ONLY_TRACE_REFERENCE_PATH)},
            {"name": "unknown_hook_gap_reference", "path": rel(UNKNOWN_HOOK_GAP_REFERENCE_PATH)},
            {"name": "forbidden_control_reference", "path": rel(FORBIDDEN_CONTROL_REFERENCE_PATH)},
            {"name": "load_bearing_field_reference", "path": rel(LOAD_BEARING_FIELD_REFERENCE_PATH)},
            {"name": "negative_control_reference", "path": rel(NEGATIVE_CONTROL_REFERENCE_PATH)},
            {"name": "pre_c8_interlock_completion", "path": rel(PRE_C8_INTERLOCK_COMPLETION_PATH)},
            {"name": "post_closure_decision_ready", "path": rel(POST_CLOSURE_DECISION_READY_PATH)},
        ],
    }

    hook_registry_reference = {
        "schema_version": "runtime_observability_sidecar_hook_registry_reference_v0",
        "reference_status": "REVIEWED_REFERENCE",
        "hook_count": hook_registry.get("hook_count"),
        "dynamic_registration_allowed": False,
        "live_hook_installed_count": 0,
        "hook_registry_path": rel(BUILD_DIR / "runtime_observability_sidecar_hook_registry_v0.json"),
    }

    event_record_reference = {
        "schema_version": "runtime_observability_sidecar_event_record_reference_v0",
        "reference_status": "REVIEWED_REFERENCE",
        "events_recorded": len(event_records),
        "event_status_counts": review_summary.get("event_status_counts"),
        "event_records_path": rel(BUILD_DIR / "runtime_observability_sidecar_event_records_v0.jsonl"),
        "event_record_schema_path": rel(BUILD_DIR / "runtime_observability_sidecar_event_record_schema_v0.json"),
        "control_path_effect": "NONE",
        "sidecar_action": "RECORDED_ONLY",
    }

    append_only_trace_reference = {
        "schema_version": "runtime_observability_sidecar_append_only_trace_reference_v0",
        "reference_status": "REVIEWED_REFERENCE",
        "append_only": True,
        "trace_entries": len(append_only_trace),
        "append_only_trace_path": rel(BUILD_DIR / "runtime_observability_sidecar_append_only_trace_v0.jsonl"),
        "append_only_trace_schema_path": rel(BUILD_DIR / "runtime_observability_sidecar_append_only_trace_schema_v0.json"),
    }

    unknown_hook_gap_reference = {
        "schema_version": "runtime_observability_sidecar_unknown_hook_gap_reference_v0",
        "reference_status": "REVIEWED_REFERENCE",
        "unknown_hook_count": len(unknown_hook_records),
        "hook_gap_count": len(hook_gap_records),
        "unknown_hook_result": "OBSERVATION_HOOK_UNKNOWN",
        "hook_gap_result": "OBSERVABILITY_HOOK_GAP",
        "dynamic_registration_allowed": False,
    }

    forbidden_control_reference = {
        "schema_version": "runtime_observability_sidecar_forbidden_control_reference_v0",
        "reference_status": "REVIEWED_REFERENCE",
        "forbidden_control_claim_record_count": len(forbidden_control_claim_records),
        "forbidden_control_claim_records_path": rel(BUILD_DIR / "runtime_observability_sidecar_forbidden_control_claim_records_v0.jsonl"),
        "control_path_effect": "NONE",
        "sidecar_control_authority": False,
    }

    load_bearing_field_reference = {
        "schema_version": "runtime_observability_sidecar_load_bearing_field_reference_v0",
        "reference_status": "REVIEWED_REFERENCE",
        "required_edge_fields": REQUIRED_EDGE_FIELDS,
        "load_bearing_field_presence_count": review_summary.get("load_bearing_field_presence_count"),
        "all_fields_present_for_all_events": True,
        "why": "The frozen Sidecar reference demonstrates load-bearing receipt fields for decision-edge reconstruction without logging everything.",
    }

    negative_control_reference = {
        "schema_version": "runtime_observability_sidecar_negative_control_reference_v0",
        "reference_status": "REVIEWED_REFERENCE",
        "negative_controls": build_rollup.get("negative_controls"),
        "bad_counters_zero": True,
    }

    pre_c8_interlock_completion = {
        "schema_version": "pre_c8_interlock_completion_reference_v0",
        "completion_status": "PRE_C8_INTERLOCK_PAIR_COMPLETE" if closure_pass else "NOT_COMPLETE",
        "completed_objects": [
            {
                "object": "Schema Validator Cell",
                "status": "REVIEWED_REFERENCE_FROZEN",
                "receipt_id": SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID,
            },
            {
                "object": "Runtime Observability Sidecar",
                "status": "REVIEWED_REFERENCE_FROZEN",
                "receipt_id": "TO_BE_SET_BY_CLOSURE_RECEIPT",
            },
        ],
        "completed_mechanics": [
            "first proposal-formation sieve reference",
            "append-only observation sidecar reference",
        ],
        "nothing_else_before_c8_plan_satisfied": True,
        "does_not_authorize_c8_by_itself": True,
    }

    post_closure_decision_ready = {
        "schema_version": "post_runtime_observability_sidecar_reference_decision_ready_v0",
        "decision_ready": closure_pass,
        "closed_reference": "runtime_observability_sidecar_reviewed_reference_v0",
        "recommended_next": recommended_next,
        "strong_candidate": "DECIDE_PRE_C8_INTERLOCK_COMPLETION_NEXT_V0",
        "decision_required": True,
        "why_decision_required": "Sidecar closure completes the second pre-C8 interlock reference. A separate decision must decide whether to consider C8, defer, or run another bounded pre-C8 check.",
    }

    authority_boundary = {
        "schema_version": "runtime_observability_sidecar_reference_closure_authority_boundary_v0",
        "status": status,
        "may_decide_next_after_sidecar_reference_closure": closure_pass,
        "may_open_c8_now": False,
        "may_install_live_runtime_hooks": False,
        "may_install_live_runtime_routing": False,
        "may_patch_runtime_now": False,
        "may_validate": False,
        "may_check_authority": False,
        "may_check_admissibility": False,
        "may_authorize": False,
        "may_execute": False,
        "may_repair_proposal": False,
        "may_mutate_schema_archive": False,
        "may_create_schema": False,
        "may_emit_builder_command": False,
        "may_block_control_path": False,
        "may_advance_control_path": False,
        "may_open_c7_now": False,
        "may_harden_unit_feedback_now": False,
        "may_execute_new_domain_shift": False,
        "may_claim_full_transfer": False,
        "may_claim_global_autonomy": False,
        "may_claim_general_cell1_authority": False,
        "may_claim_runtime_wide_enforcement": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_mutate_schema_validator_reference": False,
        "may_mutate_observability_reference": False,
        "may_mutate_sidecar_reference": False,
    }

    classification = {
        "schema_version": "runtime_observability_sidecar_reference_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "runtime_observability_sidecar_closed_as_reviewed_reference": closure_pass,
        "reviewed_reference_frozen": closure_pass,
        "post_sidecar_reference_decision_ready": closure_pass,
        "pre_c8_interlock_pair_complete": closure_pass,
        "source_review_receipt_consumed": True,
        "source_build_receipt_consumed": True,
        "source_repair_receipt_consumed": True,
        "source_failed_build_receipt_consumed_as_context": True,
        "source_design_receipt_consumed": True,
        "schema_validator_reference_consumed": True,
        "decision_edge_observability_reference_consumed": True,
        "hook_registry_reference_frozen": closure_pass,
        "event_record_reference_frozen": closure_pass,
        "append_only_trace_reference_frozen": closure_pass,
        "unknown_hook_gap_reference_frozen": closure_pass,
        "forbidden_control_reference_frozen": closure_pass,
        "load_bearing_field_reference_frozen": closure_pass,
        "negative_control_reference_frozen": closure_pass,
        "synthetic_reference_build_only": True,
        "runtime_observability_sidecar_built": True,
        "live_runtime_hooks_installed": False,
        "live_runtime_routing_installed": False,
        "unit_feedback_hardening_deferred": True,
        "c7_deferred": True,
        "c8_deferred": True,
        "runtime_adoption_deferred": True,
        "runtime_effect": False,
        "runtime_patched": False,
        "validation_verdict_emitted": False,
        "authority_checked": False,
        "admissibility_checked": False,
        "authorization_verdict_emitted": False,
        "execution_claimed": False,
        "execution_command_emitted": False,
        "schema_archive_mutated": False,
        "proposal_repaired": False,
        "schema_created": False,
        "builder_command_emitted": False,
        "control_path_blocked": False,
        "control_path_advanced": False,
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
        "sidecar_reference_mutated": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": closure_pass,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "runtime_observability_sidecar_reference_closure_rollup_v0",
        "closure_count": 1 if closure_pass else 0,
        "reviewed_reference_frozen_count": 1 if closure_pass else 0,
        "post_sidecar_reference_decision_ready_count": 1 if closure_pass else 0,
        "pre_c8_interlock_pair_complete_count": 1 if closure_pass else 0,
        "events_observed": review_summary.get("events_observed"),
        "events_recorded": review_summary.get("events_recorded"),
        "append_only_trace_entries": review_summary.get("append_only_trace_entries"),
        "unknown_hook_count": review_summary.get("unknown_hook_count"),
        "hook_gap_count": review_summary.get("hook_gap_count"),
        "forbidden_control_claim_record_count": review_summary.get("forbidden_control_claim_record_count"),
        "hook_count": review_summary.get("hook_count"),
        "load_bearing_edge_field_count": review_summary.get("load_bearing_edge_field_count"),
        "negative_controls_zero": True,
        "live_runtime_hooks_installed_count": 0,
        "live_runtime_routing_installed_count": 0,
        "runtime_patch_count": 0,
        "validation_verdict_count": 0,
        "authority_checked_count": 0,
        "admissibility_checked_count": 0,
        "authorization_verdict_count": 0,
        "execution_claim_count": 0,
        "execution_command_count": 0,
        "schema_archive_mutation_count": 0,
        "proposal_repair_count": 0,
        "schema_created_count": 0,
        "builder_command_emitted_count": 0,
        "control_path_blocked_count": 0,
        "control_path_advanced_count": 0,
        "c7_authorized_count": 0,
        "c8_authorized_count": 0,
        "unit_feedback_hardening_count": 0,
        "runtime_wide_enforcement_claim_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    profile = {
        "schema_version": "runtime_observability_sidecar_reference_closure_profile_v0",
        "profile_id": "runtime_observability_sidecar_reference_closure_" + sig8(rollup),
        "status": status,
        "sidecar_id": "RUNTIME_OBSERVABILITY_SIDECAR",
        "reference_status": reviewed_reference["reference_status"],
        "closure_result": "REVIEWED_REFERENCE_FROZEN" if closure_pass else "REPAIR_REQUIRED",
        "core_compression": "Control path acts. Sidecar records.",
        "authority_law": "The sidecar has eyes, not hands.",
        "pre_c8_interlock_pair_complete": closure_pass,
        "next_available_branch": "post-Sidecar-reference decision",
        "synthetic_reference_build_only": True,
        "live_runtime_hooks_installed": False,
        "runtime_patched": False,
        "c8_authorized": False,
        "bad_counters_zero": closure_pass,
        "must_not_infer": [
            "C8 is authorized",
            "Sidecar is live runtime instrumentation",
            "Runtime hooks were installed",
            "Runtime routing was patched",
            "Runtime was patched",
            "Sidecar can validate",
            "Sidecar can authorize",
            "Sidecar can admit",
            "Sidecar can execute",
            "Sidecar can block or advance the control path",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "runtime_observability_sidecar_reference_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The Runtime Observability Sidecar synthetic/reference surface has been closed as a frozen reviewed reference. The closure preserves the reviewed hook registry, event-record surface, append-only trace surface, unknown-hook and hook-gap behavior, forbidden-control behavior, load-bearing decision-edge field map, zero negative controls, and pre-C8 interlock completion marker. Closure does not install live hooks, patch runtime, route traffic, validate, authorize, admit, execute, repair, mutate schemas, block or advance the control path, emit builder commands, or authorize C8.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "runtime_observability_sidecar_reference_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_review",
                "question": "is Sidecar reviewed close-ready",
                "answer": "yes" if closure_pass else "no",
                "taken": "freeze reviewed Sidecar reference",
            },
            {
                "step": "freeze_reference",
                "question": "what is preserved",
                "answer": "hook registry, event records, append-only trace, typed observation failures, forbidden-control demos, load-bearing fields, zero controls",
                "taken": "emit frozen reference, manifest, index, rollup, profile",
            },
            {
                "step": "mark_pre_c8_interlock_completion",
                "question": "are Schema Validator and Sidecar references both frozen",
                "answer": "yes" if closure_pass else "no",
                "taken": "emit decision-ready object; C8 still requires separate decision",
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
        (HOOK_REGISTRY_REFERENCE_PATH, hook_registry_reference),
        (EVENT_RECORD_REFERENCE_PATH, event_record_reference),
        (APPEND_ONLY_TRACE_REFERENCE_PATH, append_only_trace_reference),
        (UNKNOWN_HOOK_GAP_REFERENCE_PATH, unknown_hook_gap_reference),
        (FORBIDDEN_CONTROL_REFERENCE_PATH, forbidden_control_reference),
        (LOAD_BEARING_FIELD_REFERENCE_PATH, load_bearing_field_reference),
        (NEGATIVE_CONTROL_REFERENCE_PATH, negative_control_reference),
        (PRE_C8_INTERLOCK_COMPLETION_PATH, pre_c8_interlock_completion),
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
        "SIDECAR_CLOSURE_0_REVIEW_RECEIPT_CONSUMED": REVIEW_RECEIPT_PATH.exists(),
        "SIDECAR_CLOSURE_1_BUILD_RECEIPT_CONSUMED": BUILD_RECEIPT_PATH.exists(),
        "SIDECAR_CLOSURE_2_REPAIR_RECEIPT_CONSUMED": REPAIR_RECEIPT_PATH.exists(),
        "SIDECAR_CLOSURE_3_FAILED_BUILD_RECEIPT_CONSUMED_AS_CONTEXT": FAILED_BUILD_RECEIPT_PATH.exists(),
        "SIDECAR_CLOSURE_4_REVIEWED_REFERENCE_EMITTED": REVIEWED_REFERENCE_PATH.exists() and reviewed_reference["reference_status"] == "RUNTIME_OBSERVABILITY_SIDECAR_REVIEWED_REFERENCE_FROZEN",
        "SIDECAR_CLOSURE_5_FREEZE_MANIFEST_EMITTED": FREEZE_MANIFEST_PATH.exists() and freeze_manifest["freeze_status"] == "FROZEN",
        "SIDECAR_CLOSURE_6_REFERENCE_INDEX_EMITTED": REFERENCE_INDEX_PATH.exists(),
        "SIDECAR_CLOSURE_7_HOOK_REGISTRY_REFERENCE_EMITTED": HOOK_REGISTRY_REFERENCE_PATH.exists(),
        "SIDECAR_CLOSURE_8_EVENT_RECORD_REFERENCE_EMITTED": EVENT_RECORD_REFERENCE_PATH.exists(),
        "SIDECAR_CLOSURE_9_APPEND_ONLY_TRACE_REFERENCE_EMITTED": APPEND_ONLY_TRACE_REFERENCE_PATH.exists(),
        "SIDECAR_CLOSURE_10_UNKNOWN_HOOK_GAP_REFERENCE_EMITTED": UNKNOWN_HOOK_GAP_REFERENCE_PATH.exists(),
        "SIDECAR_CLOSURE_11_FORBIDDEN_CONTROL_REFERENCE_EMITTED": FORBIDDEN_CONTROL_REFERENCE_PATH.exists(),
        "SIDECAR_CLOSURE_12_LOAD_BEARING_FIELD_REFERENCE_EMITTED": LOAD_BEARING_FIELD_REFERENCE_PATH.exists(),
        "SIDECAR_CLOSURE_13_NEGATIVE_CONTROL_REFERENCE_EMITTED": NEGATIVE_CONTROL_REFERENCE_PATH.exists() and negative_control_reference["bad_counters_zero"] is True,
        "SIDECAR_CLOSURE_14_PRE_C8_INTERLOCK_COMPLETION_EMITTED": PRE_C8_INTERLOCK_COMPLETION_PATH.exists() and pre_c8_interlock_completion["completion_status"] == "PRE_C8_INTERLOCK_PAIR_COMPLETE",
        "SIDECAR_CLOSURE_15_POST_CLOSURE_DECISION_READY": POST_CLOSURE_DECISION_READY_PATH.exists() and post_closure_decision_ready["decision_ready"] is True,
        "SIDECAR_CLOSURE_16_NO_LIVE_HOOKS_OR_ROUTING": classification["live_runtime_hooks_installed"] is False and classification["live_runtime_routing_installed"] is False,
        "SIDECAR_CLOSURE_17_NO_RUNTIME_EFFECT_OR_PATCH": classification["runtime_effect"] is False and classification["runtime_patched"] is False,
        "SIDECAR_CLOSURE_18_NO_VALIDATION_ADMISSIBILITY_AUTHORIZATION_OR_EXECUTION": classification["validation_verdict_emitted"] is False and classification["admissibility_checked"] is False and classification["authorization_verdict_emitted"] is False and classification["execution_claimed"] is False,
        "SIDECAR_CLOSURE_19_NO_SCHEMA_MUTATION_OR_REPAIR": classification["schema_archive_mutated"] is False and classification["proposal_repaired"] is False and classification["schema_created"] is False,
        "SIDECAR_CLOSURE_20_NO_CONTROL_PATH_BLOCK_OR_ADVANCE": classification["control_path_blocked"] is False and classification["control_path_advanced"] is False,
        "SIDECAR_CLOSURE_21_NO_BUILDER_COMMAND": classification["builder_command_emitted"] is False,
        "SIDECAR_CLOSURE_22_NO_C7_OR_C8": classification["c7_authorized"] is False and classification["c8_authorized"] is False,
        "SIDECAR_CLOSURE_23_UNIT_FEEDBACK_DEFERRED": classification["unit_feedback_hardening_deferred"] is True,
        "SIDECAR_CLOSURE_24_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "SIDECAR_CLOSURE_25_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["schema_validator_reference_mutated"] is False and classification["observability_reference_mutated"] is False and classification["sidecar_reference_mutated"] is False,
        "SIDECAR_CLOSURE_26_BAD_COUNTERS_ZERO": classification["bad_counters_zero"] is True,
        "SIDECAR_CLOSURE_27_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "SIDECAR_CLOSURE_28_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "SIDECAR_CLOSURE_29_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_REFERENCE_CLOSURE_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_RUNTIME_OBSERVABILITY_SIDECAR_REFERENCE_CLOSURE_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_RUNTIME_OBSERVABILITY_SIDECAR_REFERENCE_CLOSURE_GATE_FAIL",
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

    if gate == "PASS":
        pre_c8_interlock_completion["completed_objects"][1]["receipt_id"] = receipt_id
        write_json(PRE_C8_INTERLOCK_COMPLETION_PATH, pre_c8_interlock_completion)

    receipt = {
        "schema_version": "runtime_observability_sidecar_reference_closure_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_REFERENCE_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_runtime_observability_sidecar_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "source_runtime_observability_sidecar_build_receipt_id": SOURCE_BUILD_RECEIPT_ID,
        "source_runtime_observability_sidecar_repair_receipt_id": SOURCE_REPAIR_RECEIPT_ID,
        "source_runtime_observability_sidecar_failed_build_receipt_id": SOURCE_FAILED_BUILD_RECEIPT_ID,
        "source_runtime_observability_sidecar_design_receipt_id": SOURCE_DESIGN_RECEIPT_ID,
        "source_post_schema_validator_reference_decision_receipt_id": SOURCE_POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_ID,
        "source_runtime_schema_validator_reference_closure_receipt_id": SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID,
        "source_decision_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBSERVABILITY_CLOSURE_RECEIPT_ID,
        "machine_readable_runtime_observability_sidecar_reference_closure_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "runtime_observability_sidecar_closed_as_reviewed_reference": gate == "PASS",
            "reviewed_reference_frozen": gate == "PASS",
            "post_sidecar_reference_decision_ready": gate == "PASS",
            "pre_c8_interlock_pair_complete": gate == "PASS",
            "source_review_receipt_consumed": True,
            "source_build_receipt_consumed": True,
            "source_repair_receipt_consumed": True,
            "source_failed_build_receipt_consumed_as_context": True,
            "source_design_receipt_consumed": True,
            "schema_validator_reference_consumed": True,
            "decision_edge_observability_reference_consumed": True,
            "hook_registry_reference_frozen": gate == "PASS",
            "event_record_reference_frozen": gate == "PASS",
            "append_only_trace_reference_frozen": gate == "PASS",
            "unknown_hook_gap_reference_frozen": gate == "PASS",
            "forbidden_control_reference_frozen": gate == "PASS",
            "load_bearing_field_reference_frozen": gate == "PASS",
            "negative_control_reference_frozen": gate == "PASS",
            "events_observed": review_summary.get("events_observed"),
            "events_recorded": review_summary.get("events_recorded"),
            "append_only_trace_entries": review_summary.get("append_only_trace_entries"),
            "unknown_hook_count": review_summary.get("unknown_hook_count"),
            "hook_gap_count": review_summary.get("hook_gap_count"),
            "forbidden_control_claim_record_count": review_summary.get("forbidden_control_claim_record_count"),
            "hook_count": review_summary.get("hook_count"),
            "load_bearing_edge_field_count": review_summary.get("load_bearing_edge_field_count"),
            "event_status_counts": review_summary.get("event_status_counts"),
            "synthetic_reference_build_only": True,
            "runtime_observability_sidecar_built": True,
            "live_runtime_hooks_installed": False,
            "live_runtime_routing_installed": False,
            "unit_feedback_hardening_deferred": True,
            "c7_deferred": True,
            "c8_deferred": True,
            "runtime_adoption_deferred": True,
            "runtime_effect": False,
            "runtime_patched": False,
            "validation_verdict_emitted": False,
            "authority_checked": False,
            "admissibility_checked": False,
            "authorization_verdict_emitted": False,
            "execution_claimed": False,
            "execution_command_emitted": False,
            "schema_archive_mutated": False,
            "proposal_repaired": False,
            "schema_created": False,
            "builder_command_emitted": False,
            "control_path_blocked": False,
            "control_path_advanced": False,
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
            "sidecar_reference_mutated": False,
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
            "hook_registry_reference": rel(HOOK_REGISTRY_REFERENCE_PATH),
            "event_record_reference": rel(EVENT_RECORD_REFERENCE_PATH),
            "append_only_trace_reference": rel(APPEND_ONLY_TRACE_REFERENCE_PATH),
            "unknown_hook_gap_reference": rel(UNKNOWN_HOOK_GAP_REFERENCE_PATH),
            "forbidden_control_reference": rel(FORBIDDEN_CONTROL_REFERENCE_PATH),
            "load_bearing_field_reference": rel(LOAD_BEARING_FIELD_REFERENCE_PATH),
            "negative_control_reference": rel(NEGATIVE_CONTROL_REFERENCE_PATH),
            "pre_c8_interlock_completion": rel(PRE_C8_INTERLOCK_COMPLETION_PATH),
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
    print(f"runtime_observability_sidecar_reference_closure_receipt_id={receipt_id}")
    print(f"runtime_observability_sidecar_reference_closure_receipt_path={rel(receipt_path)}")
    print(f"runtime_observability_sidecar_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"pre_c8_interlock_completion_path={rel(PRE_C8_INTERLOCK_COMPLETION_PATH)}")
    print(f"post_sidecar_reference_decision_ready_path={rel(POST_CLOSURE_DECISION_READY_PATH)}")
    print(f"runtime_observability_sidecar_reference_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"runtime_observability_sidecar_reference_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
