#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_RUNTIME_OBSERVABILITY_SIDECAR_V0"
TARGET_UNIT_ID = "runtime.observability_sidecar.review.v0"
LAYER = "RUNTIME / OBSERVATION / REVIEW"
MODE = "REVIEW_ONLY / SYNTHETIC_REFERENCE_SIDECAR / NO_LIVE_HOOKS"
BUILD_MODE = "RUNTIME_OBSERVABILITY_SIDECAR_REVIEW_ONLY"

SOURCE_BUILD_RECEIPT_ID = "7a63137f"
SOURCE_REPAIR_RECEIPT_ID = "480cf138"
SOURCE_FAILED_BUILD_RECEIPT_ID = "84aec9df"
SOURCE_DESIGN_RECEIPT_ID = "37628e11"
SOURCE_POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_ID = "1ca1e03b"
SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID = "732016f0"
SOURCE_EDGE_OBSERVABILITY_CLOSURE_RECEIPT_ID = "ac09c2e3"

BUILD_RECEIPT_PATH = ROOT / "data/runtime_observability_sidecar_v0_receipts/7a63137f.json"
REPAIR_RECEIPT_PATH = ROOT / "data/runtime_observability_sidecar_build_repair_v0_receipts/480cf138.json"
FAILED_BUILD_RECEIPT_PATH = ROOT / "data/runtime_observability_sidecar_v0_receipts/84aec9df.json"
DESIGN_RECEIPT_PATH = ROOT / "data/runtime_observability_sidecar_target_from_schema_validator_and_observability_references_v0_receipts/37628e11.json"
POST_DECISION_RECEIPT_PATH = ROOT / "data/post_runtime_schema_validator_reference_decision_v0_receipts/1ca1e03b.json"
SCHEMA_VALIDATOR_CLOSURE_RECEIPT_PATH = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0_receipts/732016f0.json"
EDGE_OBSERVABILITY_CLOSURE_RECEIPT_PATH = ROOT / "data/decision_edge_observability_reference_closure_from_bounded_c6_adoption_probe_reference_v0_receipts/ac09c2e3.json"

BUILD_DIR = ROOT / "data/runtime_observability_sidecar_v0"
REPAIR_DIR = ROOT / "data/runtime_observability_sidecar_build_repair_v0"
DESIGN_DIR = ROOT / "data/runtime_observability_sidecar_target_from_schema_validator_and_observability_references_v0"

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

DESIGN_ARTIFACTS = [
    DESIGN_DIR / "runtime_observability_sidecar_target_spec_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_build_target_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_design_profile_v0.json",
]

REQUIRED_SOURCE_FILES = [
    BUILD_RECEIPT_PATH,
    REPAIR_RECEIPT_PATH,
    FAILED_BUILD_RECEIPT_PATH,
    DESIGN_RECEIPT_PATH,
    POST_DECISION_RECEIPT_PATH,
    SCHEMA_VALIDATOR_CLOSURE_RECEIPT_PATH,
    EDGE_OBSERVABILITY_CLOSURE_RECEIPT_PATH,
] + BUILD_ARTIFACTS + REPAIR_ARTIFACTS + DESIGN_ARTIFACTS

OUT_DIR = ROOT / "data/runtime_observability_sidecar_review_v0"
RECEIPT_DIR = ROOT / "data/runtime_observability_sidecar_review_v0_receipts"

REVIEW_BASIS_PATH = OUT_DIR / "runtime_observability_sidecar_review_basis_v0.json"
SOURCE_BUILD_RECEIPT_REVIEW_PATH = OUT_DIR / "runtime_observability_sidecar_source_build_receipt_review_v0.json"
SOURCE_REPAIR_RECEIPT_REVIEW_PATH = OUT_DIR / "runtime_observability_sidecar_source_repair_receipt_review_v0.json"
SOURCE_FAILED_BUILD_REVIEW_PATH = OUT_DIR / "runtime_observability_sidecar_failed_build_review_v0.json"
ARTIFACT_INVENTORY_PATH = OUT_DIR / "runtime_observability_sidecar_artifact_inventory_review_v0.json"
SCHEMA_SURFACE_REVIEW_PATH = OUT_DIR / "runtime_observability_sidecar_schema_surface_review_v0.json"
EVENT_RECORD_REVIEW_PATH = OUT_DIR / "runtime_observability_sidecar_event_record_review_v0.json"
TRACE_REVIEW_PATH = OUT_DIR / "runtime_observability_sidecar_append_only_trace_review_v0.json"
UNKNOWN_HOOK_GAP_REVIEW_PATH = OUT_DIR / "runtime_observability_sidecar_unknown_hook_gap_review_v0.json"
FORBIDDEN_CONTROL_REVIEW_PATH = OUT_DIR / "runtime_observability_sidecar_forbidden_control_claim_review_v0.json"
NEGATIVE_CONTROL_REVIEW_PATH = OUT_DIR / "runtime_observability_sidecar_negative_control_review_v0.json"
LOAD_BEARING_FIELD_REVIEW_PATH = OUT_DIR / "runtime_observability_sidecar_load_bearing_field_review_v0.json"
BOUNDARY_REVIEW_PATH = OUT_DIR / "runtime_observability_sidecar_boundary_review_v0.json"
REVIEWED_REFERENCE_CLOSE_CANDIDATE_PATH = OUT_DIR / "runtime_observability_sidecar_reviewed_reference_close_candidate_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "runtime_observability_sidecar_review_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "runtime_observability_sidecar_review_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_observability_sidecar_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_observability_sidecar_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "runtime_observability_sidecar_review_report.json"
TRACE_PATH = OUT_DIR / "runtime_observability_sidecar_review_transition_trace.json"

EXPECTED_BUILD_STATUS = "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_BUILT_REVIEW_READY"
EXPECTED_BUILD_STOP = "STOP_TYPED_RUNTIME_OBSERVABILITY_SIDECAR_BUILT_REVIEW_READY"
EXPECTED_BUILD_NEXT = UNIT_ID

EXPECTED_REPAIR_STOP = "STOP_RUNTIME_OBSERVABILITY_SIDECAR_BUILD_REPAIR_PATCHED_RERUN_READY"
RECOMMENDED_NEXT = "CLOSE_RUNTIME_OBSERVABILITY_SIDECAR_AS_REVIEWED_REFERENCE_V0"

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

ZERO_COUNTERS = [
    "admissibility_verdict_count",
    "authorization_verdict_count",
    "blocking_action_count",
    "builder_command_count",
    "c8_authorization_count",
    "control_path_advanced_count",
    "control_path_blocked_count",
    "execution_command_count",
    "hidden_next_command_count",
    "latest_file_guessing_count",
    "live_hook_install_count",
    "mtime_selection_count",
    "proposal_repair_count",
    "reference_mutation_count",
    "runtime_patch_count",
    "schema_mutation_count",
    "source_mutation_count",
    "validation_verdict_count",
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

    build_receipt = read_json(BUILD_RECEIPT_PATH)
    build_summary = build_receipt.get("machine_readable_runtime_observability_sidecar_build_summary", {})
    repair_receipt = read_json(REPAIR_RECEIPT_PATH)
    failed_receipt = read_json(FAILED_BUILD_RECEIPT_PATH)
    design_receipt = read_json(DESIGN_RECEIPT_PATH)
    post_decision_receipt = read_json(POST_DECISION_RECEIPT_PATH)
    schema_validator_closure_receipt = read_json(SCHEMA_VALIDATOR_CLOSURE_RECEIPT_PATH)
    edge_observability_closure_receipt = read_json(EDGE_OBSERVABILITY_CLOSURE_RECEIPT_PATH)

    hook_registry = read_json(BUILD_DIR / "runtime_observability_sidecar_hook_registry_v0.json")
    event_record_schema = read_json(BUILD_DIR / "runtime_observability_sidecar_event_record_schema_v0.json")
    sidecar_receipt_schema = read_json(BUILD_DIR / "runtime_observability_sidecar_receipt_schema_v0.json")
    append_only_trace_schema = read_json(BUILD_DIR / "runtime_observability_sidecar_append_only_trace_schema_v0.json")
    rollup_readout_profile_schema = read_json(BUILD_DIR / "runtime_observability_sidecar_rollup_readout_profile_schema_v0.json")
    demo_inputs = read_jsonl(BUILD_DIR / "runtime_observability_sidecar_demo_event_inputs_v0.jsonl")
    event_records = read_jsonl(BUILD_DIR / "runtime_observability_sidecar_event_records_v0.jsonl")
    append_only_trace = read_jsonl(BUILD_DIR / "runtime_observability_sidecar_append_only_trace_v0.jsonl")
    unknown_hook_records = read_jsonl(BUILD_DIR / "runtime_observability_sidecar_unknown_hook_records_v0.jsonl")
    hook_gap_records = read_jsonl(BUILD_DIR / "runtime_observability_sidecar_hook_gap_records_v0.jsonl")
    forbidden_control_claim_records = read_jsonl(BUILD_DIR / "runtime_observability_sidecar_forbidden_control_claim_records_v0.jsonl")
    rollup = read_json(BUILD_DIR / "runtime_observability_sidecar_rollup_v0.json")
    readout = read_json(BUILD_DIR / "runtime_observability_sidecar_readout_v0.json")
    profile = read_json(BUILD_DIR / "runtime_observability_sidecar_profile_v0.json")
    report = read_json(BUILD_DIR / "runtime_observability_sidecar_report.json")
    build_trace = read_json(BUILD_DIR / "runtime_observability_sidecar_transition_trace.json")

    patch_record = read_json(REPAIR_DIR / "runtime_observability_sidecar_build_patch_record_v0.json")
    repair_basis = read_json(REPAIR_DIR / "runtime_observability_sidecar_build_repair_basis_v0.json")
    repair_classification = read_json(REPAIR_DIR / "runtime_observability_sidecar_build_repair_classification_v0.json")
    design_target = read_json(DESIGN_DIR / "runtime_observability_sidecar_target_spec_v0.json")
    design_build_target = read_json(DESIGN_DIR / "runtime_observability_sidecar_build_target_v0.json")

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
        "runtime_observability_sidecar_built",
        "review_ready",
        "synthetic_reference_build_only",
        "design_receipt_consumed",
        "hook_registry_built",
        "event_record_schema_built",
        "sidecar_receipt_schema_built",
        "append_only_trace_schema_built",
        "rollup_readout_profile_schema_built",
        "demo_event_inputs_emitted",
        "event_records_emitted",
        "append_only_trace_emitted",
        "unknown_hook_records_emitted",
        "hook_gap_records_emitted",
        "forbidden_control_claim_records_emitted",
        "rollup_emitted",
        "readout_emitted",
        "profile_emitted",
        "report_emitted",
        "transition_trace_emitted",
        "unit_feedback_hardening_deferred",
        "c7_deferred",
        "c8_deferred",
        "runtime_adoption_deferred",
        "bad_counters_zero",
    ]:
        if build_summary.get(key) is not True:
            failures.append(f"build_required_true_missing:{key}")

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
        if build_summary.get(key) is not False:
            failures.append(f"build_forbidden_true:{key}")

    for key, expected in {
        "hook_count": 24,
        "events_observed": 16,
        "events_recorded": 16,
        "append_only_trace_entries": 16,
        "unknown_hook_count": 1,
        "hook_gap_count": 1,
        "forbidden_control_claim_record_count": 10,
        "load_bearing_edge_field_count": 7,
    }.items():
        if build_summary.get(key) != expected:
            failures.append(f"build_count_wrong:{key}:{build_summary.get(key)}")

    if build_summary.get("event_status_counts") != EXPECTED_EVENT_STATUS_COUNTS:
        failures.append("build_event_status_counts_wrong")

    for field in REQUIRED_EDGE_FIELDS:
        if build_summary.get("load_bearing_field_presence_count", {}).get(field) != 16:
            failures.append(f"build_load_bearing_field_count_wrong:{field}")

    if repair_receipt.get("receipt_id") != SOURCE_REPAIR_RECEIPT_ID or repair_receipt.get("gate") != "PASS":
        failures.append("repair_receipt_not_pass")
    if repair_receipt.get("terminal", {}).get("stop_code") != EXPECTED_REPAIR_STOP:
        failures.append("repair_stop_wrong")
    if repair_receipt.get("repair_summary", {}).get("repair_class") != "RUNNER_VALIDATION_ALIGNMENT_REPAIR":
        failures.append("repair_class_wrong")
    if repair_receipt.get("repair_summary", {}).get("repair_applied") is not True:
        failures.append("repair_not_applied")

    if failed_receipt.get("receipt_id") != SOURCE_FAILED_BUILD_RECEIPT_ID or failed_receipt.get("gate") != "FAIL":
        failures.append("failed_build_receipt_wrong")
    expected_failed = {
        "event_schema_missing_forbidden_claims",
        "receipt_schema_zero_counters_missing",
        "acceptance_gate_result_false",
    }
    if not expected_failed.issubset(set(failed_receipt.get("failures") or [])):
        failures.append("failed_build_target_failures_missing")

    if design_receipt.get("receipt_id") != SOURCE_DESIGN_RECEIPT_ID or design_receipt.get("gate") != "PASS":
        failures.append("design_receipt_not_pass")
    if post_decision_receipt.get("receipt_id") != SOURCE_POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_ID or post_decision_receipt.get("gate") != "PASS":
        failures.append("post_decision_receipt_not_pass")
    if schema_validator_closure_receipt.get("receipt_id") != SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID or schema_validator_closure_receipt.get("gate") != "PASS":
        failures.append("schema_validator_closure_receipt_not_pass")
    if edge_observability_closure_receipt.get("receipt_id") != SOURCE_EDGE_OBSERVABILITY_CLOSURE_RECEIPT_ID or edge_observability_closure_receipt.get("gate") != "PASS":
        failures.append("edge_observability_closure_receipt_not_pass")

    if hook_registry.get("hook_count") != 24:
        failures.append("hook_registry_count_wrong")
    if any(h.get("live_hook_installed") is not False for h in hook_registry.get("hooks", [])):
        failures.append("hook_registry_live_hook_installed")
    if any(h.get("control_authority") is not False for h in hook_registry.get("hooks", [])):
        failures.append("hook_registry_control_authority_true")
    if hook_registry.get("dynamic_registration_allowed") is not False:
        failures.append("hook_registry_dynamic_registration_allowed")

    if event_record_schema.get("required_load_bearing_edge_fields") != REQUIRED_EDGE_FIELDS:
        failures.append("event_record_schema_edge_fields_wrong")
    if "forbidden_claims_detected" not in event_record_schema.get("required_fields", []):
        failures.append("event_record_schema_forbidden_claims_field_missing")
    if set(sidecar_receipt_schema.get("required_zero_counters", [])) != set(ZERO_COUNTERS):
        failures.append("sidecar_receipt_schema_zero_counters_wrong")
    if append_only_trace_schema.get("append_only") is not True:
        failures.append("append_only_trace_schema_not_append_only")

    if len(demo_inputs) != 16:
        failures.append("demo_inputs_count_wrong")
    if len(event_records) != 16:
        failures.append("event_records_count_wrong")
    if len(append_only_trace) != 16:
        failures.append("append_only_trace_count_wrong")
    if len(unknown_hook_records) != 1:
        failures.append("unknown_hook_records_count_wrong")
    if len(hook_gap_records) != 1:
        failures.append("hook_gap_records_count_wrong")
    if len(forbidden_control_claim_records) != 10:
        failures.append("forbidden_control_claim_records_count_wrong")

    event_status_counts = dict(Counter(r.get("event_status") for r in event_records))
    if event_status_counts != EXPECTED_EVENT_STATUS_COUNTS:
        failures.append("event_records_status_counts_wrong")
    if any(r.get("control_path_effect") != "NONE" for r in event_records):
        failures.append("event_record_control_path_effect_not_none")
    if any(r.get("sidecar_action") != "RECORDED_ONLY" for r in event_records):
        failures.append("event_record_sidecar_action_not_recorded_only")
    for field in REQUIRED_EDGE_FIELDS:
        if any(r.get(field) in (None, "", []) for r in event_records):
            failures.append(f"event_record_missing_load_bearing_field:{field}")

    for idx, entry in enumerate(append_only_trace):
        if entry.get("trace_index") != idx:
            failures.append(f"trace_index_wrong:{idx}")
        if idx == 0 and entry.get("previous_entry_digest") != "TRACE_START":
            failures.append("trace_first_previous_digest_wrong")
        if idx > 0 and entry.get("previous_entry_digest") != append_only_trace[idx - 1].get("entry_digest"):
            failures.append(f"trace_previous_digest_chain_wrong:{idx}")

    if rollup.get("events_observed") != 16 or rollup.get("events_recorded") != 16:
        failures.append("rollup_event_counts_wrong")
    if rollup.get("trace_entries") != 16:
        failures.append("rollup_trace_count_wrong")
    if rollup.get("unknown_hook_count") != 1:
        failures.append("rollup_unknown_hook_count_wrong")
    if rollup.get("hook_gap_count") != 1:
        failures.append("rollup_hook_gap_count_wrong")
    if rollup.get("forbidden_control_claim_record_count") != 10:
        failures.append("rollup_forbidden_claim_count_wrong")
    if rollup.get("event_status_counts") != EXPECTED_EVENT_STATUS_COUNTS:
        failures.append("rollup_event_status_counts_wrong")
    if not all(v == 0 for v in rollup.get("negative_controls", {}).values()):
        failures.append("rollup_negative_controls_not_zero")
    for key in [
        "validation_verdict_count",
        "admissibility_verdict_count",
        "authorization_verdict_count",
        "execution_command_count",
        "proposal_repair_count",
        "schema_mutation_count",
        "runtime_patch_count",
        "live_hook_install_count",
        "blocking_action_count",
        "builder_command_count",
        "c8_authorization_count",
    ]:
        if rollup.get(key) != 0:
            failures.append(f"rollup_forbidden_nonzero:{key}")

    if readout.get("bad_counters_zero") is not True:
        failures.append("readout_bad_counters_not_zero")
    if profile.get("control_path_effect") != "NONE":
        failures.append("profile_control_path_effect_not_none")
    if profile.get("live_runtime_hooks_installed") is not False:
        failures.append("profile_live_hooks_true")
    if profile.get("runtime_patched") is not False:
        failures.append("profile_runtime_patched_true")
    if profile.get("c8_authorized") is not False:
        failures.append("profile_c8_authorized_true")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if build_trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("build_trace_hidden_next")

    if patch_record.get("repair_status") != "PATCH_APPLIED":
        failures.append("patch_record_not_applied")
    if repair_basis.get("repair_target") != "Sidecar build runner validation alignment":
        failures.append("repair_basis_target_wrong")
    if repair_classification.get("classification_status") != "PATCHED_RERUN_READY":
        failures.append("repair_classification_status_wrong")

    if design_target.get("authority_law") != "The sidecar has eyes, not hands.":
        failures.append("design_target_authority_law_wrong")
    if design_target.get("core_compression") != "Control path acts. Sidecar records.":
        failures.append("design_target_core_compression_wrong")
    if design_build_target.get("build_target_status") != "BUILD_READY":
        failures.append("design_build_target_not_ready")

    return failures, {
        "build_summary": build_summary,
        "repair_receipt": repair_receipt,
        "failed_receipt": failed_receipt,
        "hook_registry": hook_registry,
        "event_record_schema": event_record_schema,
        "sidecar_receipt_schema": sidecar_receipt_schema,
        "append_only_trace_schema": append_only_trace_schema,
        "rollup_readout_profile_schema": rollup_readout_profile_schema,
        "demo_inputs": demo_inputs,
        "event_records": event_records,
        "append_only_trace": append_only_trace,
        "unknown_hook_records": unknown_hook_records,
        "hook_gap_records": hook_gap_records,
        "forbidden_control_claim_records": forbidden_control_claim_records,
        "rollup": rollup,
        "readout": readout,
        "profile": profile,
        "report": report,
        "build_trace": build_trace,
        "patch_record": patch_record,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    review_pass = not failures
    status = "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_REVIEWED_CLOSE_READY" if review_pass else "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_REVIEW_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if review_pass else "REPAIR_RUNTIME_OBSERVABILITY_SIDECAR_REVIEW_V0"

    build_summary = basis.get("build_summary", {})
    repair_receipt = basis.get("repair_receipt", {})
    failed_receipt = basis.get("failed_receipt", {})
    hook_registry = basis.get("hook_registry", {})
    event_records = basis.get("event_records", [])
    append_only_trace = basis.get("append_only_trace", [])
    unknown_hook_records = basis.get("unknown_hook_records", [])
    hook_gap_records = basis.get("hook_gap_records", [])
    forbidden_control_claim_records = basis.get("forbidden_control_claim_records", [])
    rollup = basis.get("rollup", {})
    readout = basis.get("readout", {})
    profile = basis.get("profile", {})
    patch_record = basis.get("patch_record", {})

    reason_codes = [
        "RUNTIME_OBSERVABILITY_SIDECAR_REVIEWED",
        "BUILD_RECEIPT_CONSUMED",
        "REPAIR_RECEIPT_CONSUMED",
        "FAILED_BUILD_RECEIPT_CONSUMED_AS_REPAIR_CONTEXT",
        "DESIGN_RECEIPT_CONSUMED",
        "HOOK_REGISTRY_REVIEWED",
        "EVENT_RECORD_SCHEMA_REVIEWED",
        "SIDECAR_RECEIPT_SCHEMA_REVIEWED",
        "APPEND_ONLY_TRACE_SCHEMA_REVIEWED",
        "DEMO_EVENT_INPUTS_REVIEWED",
        "EVENT_RECORDS_REVIEWED",
        "APPEND_ONLY_TRACE_REVIEWED",
        "UNKNOWN_HOOK_DEMO_REVIEWED",
        "HOOK_GAP_DEMO_REVIEWED",
        "FORBIDDEN_CONTROL_CLAIM_DEMOS_REVIEWED",
        "LOAD_BEARING_FIELDS_CONFIRMED",
        "NEGATIVE_CONTROLS_ZERO_CONFIRMED",
        "CONTROL_PATH_ACTS_SIDECAR_RECORDS_CONFIRMED",
        "SIDECAR_HAS_EYES_NOT_HANDS_CONFIRMED",
        "REVIEWED_REFERENCE_CLOSE_READY",
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
    ] if review_pass else failures

    review_basis = {
        "schema_version": "runtime_observability_sidecar_review_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if review_pass else "BASIS_REPAIR_REQUIRED",
        "source_build_receipt_id": SOURCE_BUILD_RECEIPT_ID,
        "source_repair_receipt_id": SOURCE_REPAIR_RECEIPT_ID,
        "source_failed_build_receipt_id": SOURCE_FAILED_BUILD_RECEIPT_ID,
        "source_design_receipt_id": SOURCE_DESIGN_RECEIPT_ID,
        "source_post_schema_validator_decision_receipt_id": SOURCE_POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_ID,
        "source_schema_validator_reference_closure_receipt_id": SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID,
        "source_decision_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBSERVABILITY_CLOSURE_RECEIPT_ID,
        "review_scope": "review synthetic/reference Runtime Observability Sidecar build surface for close readiness",
    }

    source_build_review = {
        "schema_version": "runtime_observability_sidecar_source_build_receipt_review_v0",
        "source_build_receipt_id": SOURCE_BUILD_RECEIPT_ID,
        "source_gate": "PASS" if review_pass else "REPAIR_REQUIRED",
        "status": build_summary.get("status"),
        "review_ready": build_summary.get("review_ready"),
        "synthetic_reference_build_only": build_summary.get("synthetic_reference_build_only"),
        "recommended_next": build_summary.get("recommended_next"),
        "terminal_hidden_next": False,
    }

    source_repair_review = {
        "schema_version": "runtime_observability_sidecar_source_repair_receipt_review_v0",
        "source_repair_receipt_id": SOURCE_REPAIR_RECEIPT_ID,
        "source_gate": repair_receipt.get("gate"),
        "repair_applied": repair_receipt.get("repair_summary", {}).get("repair_applied"),
        "repair_class": repair_receipt.get("repair_summary", {}).get("repair_class"),
        "patch_before_sha256": patch_record.get("before_sha256"),
        "patch_after_sha256": patch_record.get("after_sha256"),
        "boundary_clean": repair_receipt.get("repair_summary", {}).get("bad_counters_zero") is True,
    }

    failed_build_review = {
        "schema_version": "runtime_observability_sidecar_failed_build_review_v0",
        "source_failed_build_receipt_id": SOURCE_FAILED_BUILD_RECEIPT_ID,
        "source_gate": failed_receipt.get("gate"),
        "repair_context_only": True,
        "target_failures": [
            "event_schema_missing_forbidden_claims",
            "receipt_schema_zero_counters_missing",
            "acceptance_gate_result_false",
        ],
        "superseded_by_pass_receipt_id": SOURCE_BUILD_RECEIPT_ID,
    }

    artifact_inventory = {
        "schema_version": "runtime_observability_sidecar_artifact_inventory_review_v0",
        "inventory_status": "COMPLETE" if review_pass else "REPAIR_REQUIRED",
        "build_artifact_count": len(BUILD_ARTIFACTS),
        "build_artifacts": [
            {"path": rel(path), "sha256": file_sha256(path)}
            for path in BUILD_ARTIFACTS
        ],
        "repair_artifact_count": len(REPAIR_ARTIFACTS),
        "repair_artifacts": [
            {"path": rel(path), "sha256": file_sha256(path)}
            for path in REPAIR_ARTIFACTS
        ],
    }

    schema_surface_review = {
        "schema_version": "runtime_observability_sidecar_schema_surface_review_v0",
        "schema_surface_status": "REVIEWED_OK" if review_pass else "REPAIR_REQUIRED",
        "hook_registry_built": build_summary.get("hook_registry_built"),
        "hook_count": build_summary.get("hook_count"),
        "event_record_schema_built": build_summary.get("event_record_schema_built"),
        "sidecar_receipt_schema_built": build_summary.get("sidecar_receipt_schema_built"),
        "append_only_trace_schema_built": build_summary.get("append_only_trace_schema_built"),
        "rollup_readout_profile_schema_built": build_summary.get("rollup_readout_profile_schema_built"),
        "dynamic_registration_allowed": hook_registry.get("dynamic_registration_allowed"),
    }

    event_record_review = {
        "schema_version": "runtime_observability_sidecar_event_record_review_v0",
        "event_record_status": "REVIEWED_OK" if review_pass else "REPAIR_REQUIRED",
        "events_observed": build_summary.get("events_observed"),
        "events_recorded": build_summary.get("events_recorded"),
        "event_status_counts": build_summary.get("event_status_counts"),
        "control_path_effect": "NONE",
        "sidecar_action": "RECORDED_ONLY",
    }

    trace_review = {
        "schema_version": "runtime_observability_sidecar_append_only_trace_review_v0",
        "trace_status": "REVIEWED_OK" if review_pass else "REPAIR_REQUIRED",
        "append_only": True,
        "trace_entries": len(append_only_trace),
        "trace_chain_checked": review_pass,
    }

    unknown_hook_gap_review = {
        "schema_version": "runtime_observability_sidecar_unknown_hook_gap_review_v0",
        "unknown_hook_gap_status": "REVIEWED_OK" if review_pass else "REPAIR_REQUIRED",
        "unknown_hook_count": len(unknown_hook_records),
        "hook_gap_count": len(hook_gap_records),
        "unknown_hook_result": "OBSERVATION_HOOK_UNKNOWN",
        "hook_gap_result": "OBSERVABILITY_HOOK_GAP",
        "dynamic_registration_allowed": False,
    }

    forbidden_control_review = {
        "schema_version": "runtime_observability_sidecar_forbidden_control_claim_review_v0",
        "forbidden_control_status": "REVIEWED_OK" if review_pass else "REPAIR_REQUIRED",
        "forbidden_control_claim_record_count": len(forbidden_control_claim_records),
        "forbidden_results": [
            "CONTROL_AUTHORITY_FORBIDDEN",
            "AUTHORITY_CLAIM_FORBIDDEN",
            "ADMISSIBILITY_CLAIM_FORBIDDEN",
            "EXECUTION_CLAIM_FORBIDDEN",
            "REPAIR_CLAIM_FORBIDDEN",
            "UNBOUNDED_PAYLOAD_FORBIDDEN",
            "SOURCE_MUTATION_FORBIDDEN",
            "RUNTIME_PATCH_FORBIDDEN",
            "LIVE_HOOK_INSTALL_FORBIDDEN",
            "C8_AUTHORIZATION_FORBIDDEN",
        ],
        "control_path_effect": "NONE",
    }

    negative_control_review = {
        "schema_version": "runtime_observability_sidecar_negative_control_review_v0",
        "negative_control_status": "ZERO_CONFIRMED" if review_pass else "REPAIR_REQUIRED",
        "negative_controls": rollup.get("negative_controls", {}),
        "bad_counters_zero": readout.get("bad_counters_zero"),
    }

    load_bearing_field_review = {
        "schema_version": "runtime_observability_sidecar_load_bearing_field_review_v0",
        "field_review_status": "REVIEWED_OK" if review_pass else "REPAIR_REQUIRED",
        "required_edge_fields": REQUIRED_EDGE_FIELDS,
        "load_bearing_field_presence_count": build_summary.get("load_bearing_field_presence_count"),
        "all_fields_present_for_all_events": review_pass,
    }

    boundary_review = {
        "schema_version": "runtime_observability_sidecar_boundary_review_v0",
        "boundary_status": "BOUNDARY_HELD" if review_pass else "REPAIR_REQUIRED",
        "synthetic_reference_build_only": build_summary.get("synthetic_reference_build_only"),
        "live_runtime_hooks_installed": build_summary.get("live_runtime_hooks_installed"),
        "live_runtime_routing_installed": build_summary.get("live_runtime_routing_installed"),
        "runtime_effect": build_summary.get("runtime_effect"),
        "runtime_patched": build_summary.get("runtime_patched"),
        "validation_verdict_emitted": build_summary.get("validation_verdict_emitted"),
        "authority_checked": build_summary.get("authority_checked"),
        "admissibility_checked": build_summary.get("admissibility_checked"),
        "authorization_verdict_emitted": build_summary.get("authorization_verdict_emitted"),
        "execution_claimed": build_summary.get("execution_claimed"),
        "execution_command_emitted": build_summary.get("execution_command_emitted"),
        "schema_archive_mutated": build_summary.get("schema_archive_mutated"),
        "proposal_repaired": build_summary.get("proposal_repaired"),
        "schema_created": build_summary.get("schema_created"),
        "builder_command_emitted": build_summary.get("builder_command_emitted"),
        "control_path_blocked": build_summary.get("control_path_blocked"),
        "control_path_advanced": build_summary.get("control_path_advanced"),
        "c7_authorized": build_summary.get("c7_authorized"),
        "c8_authorized": build_summary.get("c8_authorized"),
        "hidden_next_command": build_summary.get("hidden_next_command"),
    }

    close_candidate = {
        "schema_version": "runtime_observability_sidecar_reviewed_reference_close_candidate_v0",
        "candidate_status": "RUNTIME_OBSERVABILITY_SIDECAR_REVIEWED_REFERENCE_CLOSE_READY" if review_pass else "NOT_READY",
        "source_build_receipt_id": SOURCE_BUILD_RECEIPT_ID,
        "source_repair_receipt_id": SOURCE_REPAIR_RECEIPT_ID,
        "recommended_close_unit": RECOMMENDED_NEXT if review_pass else None,
        "close_meaning": "freeze synthetic Runtime Observability Sidecar surface as reviewed reference; not live runtime instrumentation",
    }

    authority_boundary = {
        "schema_version": "runtime_observability_sidecar_review_authority_boundary_v0",
        "status": status,
        "may_close_observability_sidecar_as_reviewed_reference_next": review_pass,
        "may_build_or_patch_sidecar_now": False,
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
        "may_open_c8_now": False,
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
    }

    classification = {
        "schema_version": "runtime_observability_sidecar_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "runtime_observability_sidecar_reviewed": review_pass,
        "close_ready": review_pass,
        "source_build_receipt_consumed": True,
        "source_repair_receipt_consumed": True,
        "source_failed_build_receipt_consumed_as_context": True,
        "schema_surface_reviewed": review_pass,
        "event_records_reviewed": review_pass,
        "append_only_trace_reviewed": review_pass,
        "unknown_hook_gap_reviewed": review_pass,
        "forbidden_control_claims_reviewed": review_pass,
        "load_bearing_fields_confirmed": review_pass,
        "negative_controls_zero_confirmed": review_pass,
        "synthetic_reference_build_only": True,
        "runtime_observability_sidecar_built": review_pass,
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
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": review_pass,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    review_rollup = {
        "schema_version": "runtime_observability_sidecar_review_rollup_v0",
        "review_count": 1 if review_pass else 0,
        "source_build_pass_count": 1 if review_pass else 0,
        "source_repair_pass_count": 1 if review_pass else 0,
        "schema_surface_reviewed_count": 1 if review_pass else 0,
        "event_records_reviewed_count": 1 if review_pass else 0,
        "append_only_trace_reviewed_count": 1 if review_pass else 0,
        "events_observed": build_summary.get("events_observed"),
        "events_recorded": build_summary.get("events_recorded"),
        "append_only_trace_entries": build_summary.get("append_only_trace_entries"),
        "unknown_hook_count": build_summary.get("unknown_hook_count"),
        "hook_gap_count": build_summary.get("hook_gap_count"),
        "forbidden_control_claim_record_count": build_summary.get("forbidden_control_claim_record_count"),
        "hook_count": build_summary.get("hook_count"),
        "load_bearing_edge_field_count": build_summary.get("load_bearing_edge_field_count"),
        "event_status_counts": build_summary.get("event_status_counts"),
        "negative_controls_zero": readout.get("bad_counters_zero"),
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

    review_profile = {
        "schema_version": "runtime_observability_sidecar_review_profile_v0",
        "profile_id": "runtime_observability_sidecar_review_" + sig8(review_rollup),
        "status": status,
        "sidecar_id": "RUNTIME_OBSERVABILITY_SIDECAR",
        "review_result": "REVIEWED_CLOSE_READY" if review_pass else "REPAIR_REQUIRED",
        "core_compression": "Control path acts. Sidecar records.",
        "authority_law": "The sidecar has eyes, not hands.",
        "hook_count": build_summary.get("hook_count"),
        "events_recorded": build_summary.get("events_recorded"),
        "append_only_trace_entries": build_summary.get("append_only_trace_entries"),
        "control_path_effect": "NONE",
        "synthetic_reference_build_only": True,
        "live_runtime_hooks_installed": False,
        "runtime_patched": False,
        "c8_authorized": False,
        "bad_counters_zero": review_pass,
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
        "next_command_goal": None,
    }

    review_report = {
        "schema_version": "runtime_observability_sidecar_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The Runtime Observability Sidecar synthetic/reference build has been reviewed and is close-ready. The review consumed the passing build receipt and repair receipt, confirmed the runner validation repair lineage, confirmed hook registry, schemas, 16 demo events, 16 append-only trace entries, unknown-hook and hook-gap behavior, forbidden-control-claim records, all load-bearing decision-edge fields, zero negative controls, and the control-path boundary. The Sidecar remains a reference observation surface only: no live hooks, runtime routing, runtime patch, validation/admissibility/authorization/execution authority, proposal repair, schema mutation, control-path block/advance, builder command, or C8 authorization.",
        "recommended_next_handling": recommended_next,
    }

    review_trace = {
        "schema_version": "runtime_observability_sidecar_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_sidecar_build",
                "question": "did repaired synthetic Sidecar build pass",
                "answer": "yes" if review_pass else "no",
                "taken": "review hook registry, schemas, event records, trace, rollup, readout, profile",
            },
            {
                "step": "verify_append_only_observation",
                "question": "did Sidecar record events without acting",
                "answer": "yes" if review_pass else "no",
                "taken": "confirm control_path_effect NONE and sidecar_action RECORDED_ONLY",
            },
            {
                "step": "verify_boundary",
                "question": "did review preserve no-live-hooks/no-runtime-patch/no-C8 boundary",
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
        (SOURCE_BUILD_RECEIPT_REVIEW_PATH, source_build_review),
        (SOURCE_REPAIR_RECEIPT_REVIEW_PATH, source_repair_review),
        (SOURCE_FAILED_BUILD_REVIEW_PATH, failed_build_review),
        (ARTIFACT_INVENTORY_PATH, artifact_inventory),
        (SCHEMA_SURFACE_REVIEW_PATH, schema_surface_review),
        (EVENT_RECORD_REVIEW_PATH, event_record_review),
        (TRACE_REVIEW_PATH, trace_review),
        (UNKNOWN_HOOK_GAP_REVIEW_PATH, unknown_hook_gap_review),
        (FORBIDDEN_CONTROL_REVIEW_PATH, forbidden_control_review),
        (NEGATIVE_CONTROL_REVIEW_PATH, negative_control_review),
        (LOAD_BEARING_FIELD_REVIEW_PATH, load_bearing_field_review),
        (BOUNDARY_REVIEW_PATH, boundary_review),
        (REVIEWED_REFERENCE_CLOSE_CANDIDATE_PATH, close_candidate),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (CLASSIFICATION_PATH, classification),
        (ROLLUP_PATH, review_rollup),
        (PROFILE_PATH, review_profile),
        (REPORT_PATH, review_report),
        (TRACE_PATH, review_trace),
    ]

    for path, obj in artifacts:
        write_json(path, obj)

    acceptance_gate_results = {
        "SIDECAR_REVIEW_0_BUILD_RECEIPT_CONSUMED": BUILD_RECEIPT_PATH.exists(),
        "SIDECAR_REVIEW_1_REPAIR_RECEIPT_CONSUMED": REPAIR_RECEIPT_PATH.exists(),
        "SIDECAR_REVIEW_2_FAILED_BUILD_RECEIPT_CONSUMED_AS_CONTEXT": FAILED_BUILD_RECEIPT_PATH.exists(),
        "SIDECAR_REVIEW_3_SCHEMA_SURFACE_REVIEWED": schema_surface_review["schema_surface_status"] == "REVIEWED_OK",
        "SIDECAR_REVIEW_4_EVENT_RECORDS_REVIEWED": event_record_review["event_record_status"] == "REVIEWED_OK",
        "SIDECAR_REVIEW_5_APPEND_ONLY_TRACE_REVIEWED": trace_review["trace_status"] == "REVIEWED_OK",
        "SIDECAR_REVIEW_6_UNKNOWN_HOOK_AND_GAP_REVIEWED": unknown_hook_gap_review["unknown_hook_gap_status"] == "REVIEWED_OK",
        "SIDECAR_REVIEW_7_FORBIDDEN_CONTROL_REVIEWED": forbidden_control_review["forbidden_control_status"] == "REVIEWED_OK",
        "SIDECAR_REVIEW_8_LOAD_BEARING_FIELDS_CONFIRMED": load_bearing_field_review["all_fields_present_for_all_events"] is True,
        "SIDECAR_REVIEW_9_NEGATIVE_CONTROLS_ZERO": negative_control_review["bad_counters_zero"] is True,
        "SIDECAR_REVIEW_10_CLOSE_CANDIDATE_EMITTED": close_candidate["candidate_status"] == "RUNTIME_OBSERVABILITY_SIDECAR_REVIEWED_REFERENCE_CLOSE_READY",
        "SIDECAR_REVIEW_11_NO_BUILD_OR_REPAIR_NOW": authority_boundary["may_build_or_patch_sidecar_now"] is False,
        "SIDECAR_REVIEW_12_NO_LIVE_HOOKS_OR_ROUTING": classification["live_runtime_hooks_installed"] is False and classification["live_runtime_routing_installed"] is False,
        "SIDECAR_REVIEW_13_NO_RUNTIME_EFFECT_OR_PATCH": classification["runtime_effect"] is False and classification["runtime_patched"] is False,
        "SIDECAR_REVIEW_14_NO_VALIDATION_ADMISSIBILITY_AUTHORIZATION_OR_EXECUTION": classification["validation_verdict_emitted"] is False and classification["admissibility_checked"] is False and classification["authorization_verdict_emitted"] is False and classification["execution_claimed"] is False,
        "SIDECAR_REVIEW_15_NO_SCHEMA_MUTATION_OR_REPAIR": classification["schema_archive_mutated"] is False and classification["proposal_repaired"] is False and classification["schema_created"] is False,
        "SIDECAR_REVIEW_16_NO_CONTROL_PATH_BLOCK_OR_ADVANCE": classification["control_path_blocked"] is False and classification["control_path_advanced"] is False,
        "SIDECAR_REVIEW_17_NO_BUILDER_COMMAND": classification["builder_command_emitted"] is False,
        "SIDECAR_REVIEW_18_NO_C7_OR_C8": classification["c7_authorized"] is False and classification["c8_authorized"] is False,
        "SIDECAR_REVIEW_19_UNIT_FEEDBACK_DEFERRED": classification["unit_feedback_hardening_deferred"] is True,
        "SIDECAR_REVIEW_20_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "SIDECAR_REVIEW_21_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["schema_validator_reference_mutated"] is False and classification["observability_reference_mutated"] is False,
        "SIDECAR_REVIEW_22_BAD_COUNTERS_ZERO": classification["bad_counters_zero"] is True,
        "SIDECAR_REVIEW_23_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "SIDECAR_REVIEW_24_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "SIDECAR_REVIEW_25_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_REVIEW_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_RUNTIME_OBSERVABILITY_SIDECAR_REVIEW_V0"
    terminal = review_trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_RUNTIME_OBSERVABILITY_SIDECAR_REVIEW_GATE_FAIL",
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
        "schema_version": "runtime_observability_sidecar_review_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_runtime_observability_sidecar_build_receipt_id": SOURCE_BUILD_RECEIPT_ID,
        "source_runtime_observability_sidecar_repair_receipt_id": SOURCE_REPAIR_RECEIPT_ID,
        "source_runtime_observability_sidecar_failed_build_receipt_id": SOURCE_FAILED_BUILD_RECEIPT_ID,
        "source_runtime_observability_sidecar_design_receipt_id": SOURCE_DESIGN_RECEIPT_ID,
        "source_post_schema_validator_reference_decision_receipt_id": SOURCE_POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_ID,
        "source_runtime_schema_validator_reference_closure_receipt_id": SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID,
        "source_decision_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBSERVABILITY_CLOSURE_RECEIPT_ID,
        "machine_readable_runtime_observability_sidecar_review_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "runtime_observability_sidecar_reviewed": gate == "PASS",
            "close_ready": gate == "PASS",
            "source_build_receipt_consumed": True,
            "source_repair_receipt_consumed": True,
            "source_failed_build_receipt_consumed_as_context": True,
            "schema_surface_reviewed": gate == "PASS",
            "event_records_reviewed": gate == "PASS",
            "append_only_trace_reviewed": gate == "PASS",
            "unknown_hook_gap_reviewed": gate == "PASS",
            "forbidden_control_claims_reviewed": gate == "PASS",
            "load_bearing_fields_confirmed": gate == "PASS",
            "negative_controls_zero_confirmed": gate == "PASS",
            "synthetic_reference_build_only": True,
            "runtime_observability_sidecar_built": gate == "PASS",
            "events_observed": build_summary.get("events_observed"),
            "events_recorded": build_summary.get("events_recorded"),
            "append_only_trace_entries": build_summary.get("append_only_trace_entries"),
            "unknown_hook_count": build_summary.get("unknown_hook_count"),
            "hook_gap_count": build_summary.get("hook_gap_count"),
            "forbidden_control_claim_record_count": build_summary.get("forbidden_control_claim_record_count"),
            "hook_count": build_summary.get("hook_count"),
            "load_bearing_edge_field_count": build_summary.get("load_bearing_edge_field_count"),
            "event_status_counts": build_summary.get("event_status_counts"),
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
            "event_record_review": rel(EVENT_RECORD_REVIEW_PATH),
            "trace_review": rel(TRACE_REVIEW_PATH),
            "unknown_hook_gap_review": rel(UNKNOWN_HOOK_GAP_REVIEW_PATH),
            "forbidden_control_review": rel(FORBIDDEN_CONTROL_REVIEW_PATH),
            "negative_control_review": rel(NEGATIVE_CONTROL_REVIEW_PATH),
            "load_bearing_field_review": rel(LOAD_BEARING_FIELD_REVIEW_PATH),
            "boundary_review": rel(BOUNDARY_REVIEW_PATH),
            "reviewed_reference_close_candidate": rel(REVIEWED_REFERENCE_CLOSE_CANDIDATE_PATH),
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
    print(f"runtime_observability_sidecar_review_receipt_id={receipt_id}")
    print(f"runtime_observability_sidecar_review_receipt_path={rel(receipt_path)}")
    print(f"runtime_observability_sidecar_review_close_candidate_path={rel(REVIEWED_REFERENCE_CLOSE_CANDIDATE_PATH)}")
    print(f"runtime_observability_sidecar_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"runtime_observability_sidecar_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
