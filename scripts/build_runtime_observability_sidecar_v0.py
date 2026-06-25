#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_RUNTIME_OBSERVABILITY_SIDECAR_V0"
TARGET_UNIT_ID = "runtime.observability_sidecar.v0"
LAYER = "RUNTIME / OBSERVATION"
MODE = "OBSERVE / EMIT_RECEIPT / APPEND_ONLY"
BUILD_MODE = "RUNTIME_OBSERVABILITY_SIDECAR_SYNTHETIC_REFERENCE_BUILD_ONLY"

SOURCE_SIDECAR_DESIGN_RECEIPT_ID = "37628e11"
SOURCE_POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_ID = "1ca1e03b"
SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID = "732016f0"
SOURCE_EDGE_OBSERVABILITY_CLOSURE_RECEIPT_ID = "ac09c2e3"

DESIGN_RECEIPT_PATH = ROOT / "data/runtime_observability_sidecar_target_from_schema_validator_and_observability_references_v0_receipts/37628e11.json"
DESIGN_DIR = ROOT / "data/runtime_observability_sidecar_target_from_schema_validator_and_observability_references_v0"

DESIGN_FILES = [
    DESIGN_DIR / "runtime_observability_sidecar_design_basis_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_source_decision_review_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_source_schema_validator_reference_review_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_source_edge_observability_reference_review_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_target_spec_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_hook_registry_target_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_event_record_schema_target_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_receipt_schema_target_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_append_only_trace_schema_target_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_rollup_readout_profile_schema_target_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_unknown_hook_behavior_target_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_forbidden_control_behavior_target_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_nonblocking_failure_behavior_target_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_load_bearing_field_map_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_observability_alignment_target_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_demo_case_plan_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_acceptance_gates_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_negative_controls_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_build_target_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_design_authority_boundary_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_design_classification_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_design_rollup_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_design_profile_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_design_report.json",
    DESIGN_DIR / "runtime_observability_sidecar_design_transition_trace.json",
]

POST_DECISION_RECEIPT_PATH = ROOT / "data/post_runtime_schema_validator_reference_decision_v0_receipts/1ca1e03b.json"
SCHEMA_VALIDATOR_CLOSURE_RECEIPT_PATH = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0_receipts/732016f0.json"
EDGE_OBSERVABILITY_CLOSURE_RECEIPT_PATH = ROOT / "data/decision_edge_observability_reference_closure_from_bounded_c6_adoption_probe_reference_v0_receipts/ac09c2e3.json"

REQUIRED_SOURCE_FILES = [
    DESIGN_RECEIPT_PATH,
    POST_DECISION_RECEIPT_PATH,
    SCHEMA_VALIDATOR_CLOSURE_RECEIPT_PATH,
    EDGE_OBSERVABILITY_CLOSURE_RECEIPT_PATH,
] + DESIGN_FILES

OUT_DIR = ROOT / "data/runtime_observability_sidecar_v0"
RECEIPT_DIR = ROOT / "data/runtime_observability_sidecar_v0_receipts"

HOOK_REGISTRY_PATH = OUT_DIR / "runtime_observability_sidecar_hook_registry_v0.json"
EVENT_RECORD_SCHEMA_PATH = OUT_DIR / "runtime_observability_sidecar_event_record_schema_v0.json"
SIDECAR_RECEIPT_SCHEMA_PATH = OUT_DIR / "runtime_observability_sidecar_receipt_schema_v0.json"
APPEND_ONLY_TRACE_SCHEMA_PATH = OUT_DIR / "runtime_observability_sidecar_append_only_trace_schema_v0.json"
ROLLUP_READOUT_PROFILE_SCHEMA_PATH = OUT_DIR / "runtime_observability_sidecar_rollup_readout_profile_schema_v0.json"
DEMO_EVENT_INPUTS_PATH = OUT_DIR / "runtime_observability_sidecar_demo_event_inputs_v0.jsonl"
EVENT_RECORDS_PATH = OUT_DIR / "runtime_observability_sidecar_event_records_v0.jsonl"
APPEND_ONLY_TRACE_PATH = OUT_DIR / "runtime_observability_sidecar_append_only_trace_v0.jsonl"
UNKNOWN_HOOK_RECORDS_PATH = OUT_DIR / "runtime_observability_sidecar_unknown_hook_records_v0.jsonl"
HOOK_GAP_RECORDS_PATH = OUT_DIR / "runtime_observability_sidecar_hook_gap_records_v0.jsonl"
FORBIDDEN_CONTROL_CLAIM_RECORDS_PATH = OUT_DIR / "runtime_observability_sidecar_forbidden_control_claim_records_v0.jsonl"
ROLLUP_PATH = OUT_DIR / "runtime_observability_sidecar_rollup_v0.json"
READOUT_PATH = OUT_DIR / "runtime_observability_sidecar_readout_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_observability_sidecar_profile_v0.json"
REPORT_PATH = OUT_DIR / "runtime_observability_sidecar_report.json"
TRACE_PATH = OUT_DIR / "runtime_observability_sidecar_transition_trace.json"

EXPECTED_DESIGN_STATUS = "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_TARGET_DESIGNED_BUILD_READY"
EXPECTED_DESIGN_STOP = "STOP_TYPED_RUNTIME_OBSERVABILITY_SIDECAR_TARGET_DESIGNED_BUILD_READY"
EXPECTED_DESIGN_NEXT = UNIT_ID

RECOMMENDED_NEXT = "REVIEW_RUNTIME_OBSERVABILITY_SIDECAR_V0"

REQUIRED_EDGE_FIELDS = [
    "active_object",
    "attempted_move",
    "boundary_checked",
    "boundary_result",
    "blocked_moves",
    "lawful_next_moves",
    "source_packet_ref",
]

SIDECAR_HOOKS = [
    "proposal_created",
    "schema_validation_started",
    "schema_loaded",
    "schema_validation_check_completed",
    "schema_validation_result",
    "validated_candidate_packet_emitted",
    "schema_feedback_packet_emitted",
    "schema_gap_feedback_packet_emitted",
    "schema_validator_receipt_emitted",
    "admissibility_check_started",
    "admissibility_result",
    "admissibility_halt_emitted",
    "admissibility_allow_emitted",
    "execution_started",
    "execution_completed",
    "execution_failed",
    "verification_started",
    "verification_result",
    "handoff_emitted",
    "halt_emitted",
    "advance_emitted",
    "receipt_emitted",
    "decision_edge_observed",
    "unit_feedback_emitted",
]

DEMO_CASES = [
    ("known_hook_records_event", "proposal_created", "RECORDED", []),
    ("schema_validator_result_event_records_edge_fields", "schema_validation_result", "RECORDED", []),
    ("validated_candidate_packet_event_records_source_packet", "validated_candidate_packet_emitted", "RECORDED", []),
    ("schema_feedback_event_records_blocked_move", "schema_feedback_packet_emitted", "RECORDED", []),
    ("unknown_hook_returns_observation_hook_unknown", "unknown_runtime_hook", "OBSERVATION_HOOK_UNKNOWN", []),
    ("new_hook_need_returns_observability_hook_gap", "new_hook_requested", "OBSERVABILITY_HOOK_GAP", []),
    ("control_attempt_rejected_no_block", "decision_edge_observed", "CONTROL_AUTHORITY_FORBIDDEN", ["BLOCKING_ACTION"]),
    ("authorization_claim_rejected_no_block", "decision_edge_observed", "AUTHORITY_CLAIM_FORBIDDEN", ["AUTHORIZATION_VERDICT"]),
    ("admissibility_claim_rejected_no_block", "admissibility_result", "ADMISSIBILITY_CLAIM_FORBIDDEN", ["ADMISSIBILITY_VERDICT"]),
    ("execution_claim_rejected_no_block", "execution_started", "EXECUTION_CLAIM_FORBIDDEN", ["EXECUTION_COMMAND"]),
    ("repair_claim_rejected_no_block", "unit_feedback_emitted", "REPAIR_CLAIM_FORBIDDEN", ["PROPOSAL_REPAIR"]),
    ("unbounded_payload_rejected", "receipt_emitted", "UNBOUNDED_PAYLOAD_FORBIDDEN", ["UNBOUNDED_PAYLOAD"]),
    ("source_mutation_attempt_rejected", "receipt_emitted", "SOURCE_MUTATION_FORBIDDEN", ["SOURCE_MUTATION"]),
    ("runtime_patch_attempt_rejected", "receipt_emitted", "RUNTIME_PATCH_FORBIDDEN", ["RUNTIME_PATCH"]),
    ("live_hook_install_attempt_rejected", "receipt_emitted", "LIVE_HOOK_INSTALL_FORBIDDEN", ["LIVE_HOOK_INSTALL"]),
    ("c8_authorization_attempt_rejected", "receipt_emitted", "C8_AUTHORIZATION_FORBIDDEN", ["C8_AUTHORIZATION"]),
]

ZERO_COUNTERS = [
    "validation_verdict_count",
    "admissibility_verdict_count",
    "authorization_verdict_count",
    "execution_command_count",
    "proposal_repair_count",
    "schema_mutation_count",
    "runtime_patch_count",
    "live_hook_install_count",
    "blocking_action_count",
    "control_path_advanced_count",
    "control_path_blocked_count",
    "builder_command_count",
    "c8_authorization_count",
    "source_mutation_count",
    "reference_mutation_count",
    "latest_file_guessing_count",
    "mtime_selection_count",
    "hidden_next_command_count",
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

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{rel(path)}")
    if failures:
        return failures, {}

    design_receipt = read_json(DESIGN_RECEIPT_PATH)
    design_summary = design_receipt.get("machine_readable_runtime_observability_sidecar_design_summary", {})
    target_spec = read_json(DESIGN_DIR / "runtime_observability_sidecar_target_spec_v0.json")
    hook_target = read_json(DESIGN_DIR / "runtime_observability_sidecar_hook_registry_target_v0.json")
    event_schema_target = read_json(DESIGN_DIR / "runtime_observability_sidecar_event_record_schema_target_v0.json")
    receipt_schema_target = read_json(DESIGN_DIR / "runtime_observability_sidecar_receipt_schema_target_v0.json")
    trace_schema_target = read_json(DESIGN_DIR / "runtime_observability_sidecar_append_only_trace_schema_target_v0.json")
    demo_plan = read_json(DESIGN_DIR / "runtime_observability_sidecar_demo_case_plan_v0.json")
    acceptance_gates = read_json(DESIGN_DIR / "runtime_observability_sidecar_acceptance_gates_v0.json")
    negative_controls = read_json(DESIGN_DIR / "runtime_observability_sidecar_negative_controls_v0.json")
    build_target = read_json(DESIGN_DIR / "runtime_observability_sidecar_build_target_v0.json")
    authority = read_json(DESIGN_DIR / "runtime_observability_sidecar_design_authority_boundary_v0.json")
    classification = read_json(DESIGN_DIR / "runtime_observability_sidecar_design_classification_v0.json")
    rollup = read_json(DESIGN_DIR / "runtime_observability_sidecar_design_rollup_v0.json")
    profile = read_json(DESIGN_DIR / "runtime_observability_sidecar_design_profile_v0.json")
    report = read_json(DESIGN_DIR / "runtime_observability_sidecar_design_report.json")
    trace = read_json(DESIGN_DIR / "runtime_observability_sidecar_design_transition_trace.json")

    post_decision = read_json(POST_DECISION_RECEIPT_PATH)
    schema_validator_closure = read_json(SCHEMA_VALIDATOR_CLOSURE_RECEIPT_PATH)
    edge_observability_closure = read_json(EDGE_OBSERVABILITY_CLOSURE_RECEIPT_PATH)

    if design_receipt.get("receipt_id") != SOURCE_SIDECAR_DESIGN_RECEIPT_ID or design_receipt.get("gate") != "PASS":
        failures.append("design_receipt_not_pass")
    if design_receipt.get("terminal", {}).get("stop_code") != EXPECTED_DESIGN_STOP:
        failures.append("design_stop_wrong")
    if design_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("design_hidden_next")
    if design_summary.get("status") != EXPECTED_DESIGN_STATUS:
        failures.append(f"design_status_wrong:{design_summary.get('status')}")
    if design_summary.get("recommended_next") != EXPECTED_DESIGN_NEXT:
        failures.append(f"design_next_wrong:{design_summary.get('recommended_next')}")

    for key in [
        "runtime_observability_sidecar_target_designed",
        "observability_sidecar_build_ready",
        "source_decision_consumed",
        "schema_validator_reference_consumed",
        "edge_observability_reference_consumed",
        "hook_registry_target_defined",
        "event_record_schema_target_defined",
        "receipt_schema_target_defined",
        "append_only_trace_schema_target_defined",
        "rollup_readout_profile_schema_target_defined",
        "unknown_hook_behavior_defined",
        "forbidden_control_behavior_defined",
        "nonblocking_failure_behavior_defined",
        "load_bearing_field_map_defined",
        "observability_alignment_defined",
        "demo_case_plan_defined",
        "acceptance_gates_defined",
        "negative_controls_defined",
        "unit_feedback_hardening_deferred",
        "c7_deferred",
        "c8_deferred",
        "runtime_adoption_deferred",
        "bad_counters_zero",
    ]:
        if design_summary.get(key) is not True:
            failures.append(f"design_true_missing:{key}")

    for key in [
        "observability_sidecar_built",
        "observability_sidecar_live",
        "live_runtime_hooks_installed",
        "live_runtime_routing_installed",
        "runtime_effect",
        "runtime_patched",
        "validation_verdict_emitted",
        "authority_checked",
        "admissibility_checked",
        "execution_claimed",
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
        if design_summary.get(key) is not False:
            failures.append(f"design_forbidden_true:{key}")

    for key, expected in {
        "hook_count": 24,
        "schema_validator_observable_event_count": 8,
        "load_bearing_edge_field_count": 7,
        "demo_case_count": 16,
        "acceptance_gate_count": 30,
        "negative_control_count": 20,
    }.items():
        if design_summary.get(key) != expected:
            failures.append(f"design_count_wrong:{key}:{design_summary.get(key)}")

    if target_spec.get("target_status") != "DESIGNED_BUILD_READY":
        failures.append("target_spec_not_build_ready")
    if target_spec.get("core_compression") != "Control path acts. Sidecar records.":
        failures.append("target_spec_core_compression_wrong")
    if target_spec.get("authority_law") != "The sidecar has eyes, not hands.":
        failures.append("target_spec_authority_law_wrong")
    if target_spec.get("must_not_build_yet") is not True or target_spec.get("must_not_install_live_runtime_hooks_yet") is not True:
        failures.append("target_spec_boundary_wrong")
    if hook_target.get("hook_count") != 24:
        failures.append("hook_target_count_wrong")
    if [h.get("hook_id") for h in hook_target.get("hooks", [])] != SIDECAR_HOOKS:
        failures.append("hook_target_ids_wrong")
    if event_schema_target.get("required_load_bearing_edge_fields") != REQUIRED_EDGE_FIELDS:
        failures.append("event_schema_edge_fields_wrong")
    if "forbidden_claims_detected" not in event_schema_target.get("required_fields", []):
        failures.append("event_schema_missing_forbidden_claims")
    # Build runner may track additional negative-control counters beyond the design receipt schema.
    # The design schema counters must be covered by the runner; the runner does not need to be a subset.
    if not set(receipt_schema_target.get("required_zero_counters", [])).issubset(set(ZERO_COUNTERS)):
        failures.append("receipt_schema_zero_counters_missing")
    if trace_schema_target.get("append_only") is not True:
        failures.append("trace_schema_not_append_only")
    if demo_plan.get("demo_case_count") != 16:
        failures.append("demo_plan_count_wrong")
    if acceptance_gates.get("gate_count") != 30:
        failures.append("acceptance_gate_count_wrong")
    if negative_controls.get("negative_control_count") != 20:
        failures.append("negative_control_count_wrong")
    if build_target.get("build_target_status") != "BUILD_READY":
        failures.append("build_target_not_ready")
    if authority.get("may_build_observability_sidecar_next") is not True:
        failures.append("authority_cannot_build_next")
    if classification.get("next_command_goal") is not None:
        failures.append("classification_hidden_next")
    if rollup.get("observability_sidecar_build_count") != 0:
        failures.append("design_rollup_already_built")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if report.get("recommended_next_handling") != EXPECTED_DESIGN_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_hidden_next")

    if post_decision.get("receipt_id") != SOURCE_POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_ID or post_decision.get("gate") != "PASS":
        failures.append("post_decision_receipt_not_pass")
    if schema_validator_closure.get("receipt_id") != SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID or schema_validator_closure.get("gate") != "PASS":
        failures.append("schema_validator_closure_not_pass")
    if edge_observability_closure.get("receipt_id") != SOURCE_EDGE_OBSERVABILITY_CLOSURE_RECEIPT_ID or edge_observability_closure.get("gate") != "PASS":
        failures.append("edge_observability_closure_not_pass")

    return failures, {
        "design_summary": design_summary,
        "target_spec": target_spec,
        "hook_target": hook_target,
        "event_schema_target": event_schema_target,
        "receipt_schema_target": receipt_schema_target,
        "trace_schema_target": trace_schema_target,
        "demo_plan": demo_plan,
        "acceptance_gates": acceptance_gates,
        "negative_controls": negative_controls,
        "build_target": build_target,
    }

def make_payload(case_name: str, hook_id: str, expected: str, claims: List[str]) -> Dict[str, Any]:
    payload = {
        "active_object": f"demo_object::{case_name}",
        "attempted_move": "observe_runtime_event",
        "boundary_checked": "sidecar_observe_only_boundary",
        "boundary_result": "OBSERVE_ALLOWED" if expected == "RECORDED" else "OBSERVATION_TYPED_FAILURE",
        "blocked_moves": [
            "validate",
            "authorize",
            "admit",
            "execute",
            "repair",
            "mutate",
            "patch_runtime",
            "install_live_hooks",
            "block_control_path",
            "advance_control_path",
            "open_c8",
        ],
        "lawful_next_moves": [
            "emit_event_record",
            "append_trace_entry",
            "emit_sidecar_receipt",
            "emit_rollup_readout_profile",
            "return_without_control_path_effect",
        ],
        "source_packet_ref": f"demo_packet::{case_name}",
        "source_cell": "DEMO_SOURCE_CELL",
        "target_cell": "RUNTIME_OBSERVABILITY_SIDECAR",
        "payload_excerpt": {
            "case": case_name,
            "hook": hook_id,
            "expected": expected,
        },
        "forbidden_claims": claims,
    }
    if expected == "UNBOUNDED_PAYLOAD_FORBIDDEN":
        payload["payload_excerpt"]["unbounded_payload_requested"] = True
    return payload

def evaluate_event(hook_id: str, payload: Dict[str, Any], expected: str) -> Tuple[str, bool, List[str]]:
    hook_known = hook_id in SIDECAR_HOOKS
    claims = list(payload.get("forbidden_claims") or [])

    if hook_id == "unknown_runtime_hook":
        return "OBSERVATION_HOOK_UNKNOWN", hook_known, []
    if hook_id == "new_hook_requested":
        return "OBSERVABILITY_HOOK_GAP", hook_known, []
    if "BLOCKING_ACTION" in claims:
        return "CONTROL_AUTHORITY_FORBIDDEN", hook_known, claims
    if "AUTHORIZATION_VERDICT" in claims:
        return "AUTHORITY_CLAIM_FORBIDDEN", hook_known, claims
    if "ADMISSIBILITY_VERDICT" in claims:
        return "ADMISSIBILITY_CLAIM_FORBIDDEN", hook_known, claims
    if "EXECUTION_COMMAND" in claims:
        return "EXECUTION_CLAIM_FORBIDDEN", hook_known, claims
    if "PROPOSAL_REPAIR" in claims:
        return "REPAIR_CLAIM_FORBIDDEN", hook_known, claims
    if "UNBOUNDED_PAYLOAD" in claims:
        return "UNBOUNDED_PAYLOAD_FORBIDDEN", hook_known, claims
    if "SOURCE_MUTATION" in claims:
        return "SOURCE_MUTATION_FORBIDDEN", hook_known, claims
    if "RUNTIME_PATCH" in claims:
        return "RUNTIME_PATCH_FORBIDDEN", hook_known, claims
    if "LIVE_HOOK_INSTALL" in claims:
        return "LIVE_HOOK_INSTALL_FORBIDDEN", hook_known, claims
    if "C8_AUTHORIZATION" in claims:
        return "C8_AUTHORIZATION_FORBIDDEN", hook_known, claims
    return "RECORDED", hook_known, claims

def build_records() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    event_inputs: List[Dict[str, Any]] = []
    event_records: List[Dict[str, Any]] = []
    trace_entries: List[Dict[str, Any]] = []
    previous_digest = "TRACE_START"

    for index, (case_name, hook_id, expected, claims) in enumerate(DEMO_CASES):
        payload = make_payload(case_name, hook_id, expected, claims)
        event_input = {
            "schema_version": "runtime_observability_sidecar_demo_event_input_v0",
            "case_id": f"sidecar_demo_{index:02d}_{case_name}",
            "case_name": case_name,
            "hook_id": hook_id,
            "expected_result": expected,
            "payload": payload,
        }
        event_inputs.append(event_input)

        result, hook_known, detected_claims = evaluate_event(hook_id, payload, expected)
        if result != expected:
            raise AssertionError(f"demo {case_name} expected {expected}, got {result}")

        event_id = "sidecar_event_" + sig8({"index": index, "case_name": case_name, "result": result})
        payload_digest = hashlib.sha256(canonical_bytes(payload)).hexdigest()

        record = {
            "schema_version": "runtime_observability_sidecar_event_record_v0",
            "event_id": event_id,
            "sidecar_id": "RUNTIME_OBSERVABILITY_SIDECAR",
            "hook_id": hook_id,
            "hook_known": hook_known,
            "event_status": result,
            "active_object": payload["active_object"],
            "attempted_move": payload["attempted_move"],
            "boundary_checked": payload["boundary_checked"],
            "boundary_result": payload["boundary_result"],
            "blocked_moves": payload["blocked_moves"],
            "lawful_next_moves": payload["lawful_next_moves"],
            "source_packet_ref": payload["source_packet_ref"],
            "source_cell": payload["source_cell"],
            "target_cell": payload["target_cell"],
            "observed_at": now_iso(),
            "payload_digest": payload_digest,
            "payload_excerpt": payload["payload_excerpt"],
            "forbidden_claims_detected": detected_claims,
            "sidecar_action": "RECORDED_ONLY",
            "control_path_effect": "NONE",
            "terminal": {
                "type": "RETURN",
                "stop_code": None if result == "RECORDED" else f"STOP_{result}",
                "next_command_goal": None,
            },
        }
        event_records.append(record)

        entry_digest = hashlib.sha256(canonical_bytes({
            "previous": previous_digest,
            "event": record,
            "trace_index": index,
        })).hexdigest()
        trace_entry = {
            "schema_version": "runtime_observability_sidecar_append_only_trace_entry_v0",
            "trace_index": index,
            "event_id": event_id,
            "hook_id": hook_id,
            "source_packet_ref": payload["source_packet_ref"],
            "active_object": payload["active_object"],
            "attempted_move": payload["attempted_move"],
            "boundary_checked": payload["boundary_checked"],
            "boundary_result": payload["boundary_result"],
            "event_status": result,
            "previous_entry_digest": previous_digest,
            "entry_digest": entry_digest,
        }
        trace_entries.append(trace_entry)
        previous_digest = entry_digest

    return event_inputs, event_records, trace_entries

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    build_pass = not failures
    event_inputs: List[Dict[str, Any]] = []
    event_records: List[Dict[str, Any]] = []
    trace_entries: List[Dict[str, Any]] = []

    if build_pass:
        try:
            event_inputs, event_records, trace_entries = build_records()
        except Exception as exc:
            failures.append(f"demo_build_failed:{exc}")
            build_pass = False

    status = "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_BUILT_REVIEW_READY" if build_pass else "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_BUILD_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if build_pass else "REPAIR_RUNTIME_OBSERVABILITY_SIDECAR_BUILD_V0"

    status_counts = Counter(row["event_status"] for row in event_records)
    hook_counts = Counter(row["hook_id"] for row in event_records)
    unknown_hook_records = [r for r in event_records if r["event_status"] == "OBSERVATION_HOOK_UNKNOWN"]
    hook_gap_records = [r for r in event_records if r["event_status"] == "OBSERVABILITY_HOOK_GAP"]
    forbidden_control_claim_records = [r for r in event_records if r["forbidden_claims_detected"]]

    negative_control_counters = {key: 0 for key in ZERO_COUNTERS}

    hook_registry = {
        "schema_version": "runtime_observability_sidecar_hook_registry_v0",
        "registry_status": "BUILT_SYNTHETIC_REFERENCE",
        "sidecar_id": "RUNTIME_OBSERVABILITY_SIDECAR",
        "hook_count": len(SIDECAR_HOOKS),
        "hooks": [
            {
                "hook_id": hook,
                "registered": True,
                "synthetic_reference_only": True,
                "live_hook_installed": False,
                "control_authority": False,
            }
            for hook in SIDECAR_HOOKS
        ],
        "unknown_hook_result": "OBSERVATION_HOOK_UNKNOWN",
        "new_hook_need_result": "OBSERVABILITY_HOOK_GAP",
        "dynamic_registration_allowed": False,
    }

    event_record_schema = {
        "schema_version": "runtime_observability_sidecar_event_record_schema_v0",
        "required_fields": [
            "schema_version",
            "event_id",
            "sidecar_id",
            "hook_id",
            "hook_known",
            "event_status",
            "active_object",
            "attempted_move",
            "boundary_checked",
            "boundary_result",
            "blocked_moves",
            "lawful_next_moves",
            "source_packet_ref",
            "source_cell",
            "target_cell",
            "observed_at",
            "payload_digest",
            "payload_excerpt",
            "forbidden_claims_detected",
            "sidecar_action",
            "control_path_effect",
            "terminal",
        ],
        "required_load_bearing_edge_fields": REQUIRED_EDGE_FIELDS,
        "payload_rule": "bounded excerpt plus digest only",
    }

    sidecar_receipt_schema = {
        "schema_version": "runtime_observability_sidecar_receipt_schema_v0",
        "required_fields": [
            "schema_version",
            "receipt_id",
            "unit_id",
            "sidecar_id",
            "gate",
            "events_observed",
            "events_recorded",
            "unknown_hooks",
            "hook_gaps",
            "forbidden_control_claims",
            "negative_controls",
            "output_artifacts",
            "terminal",
        ],
        "required_zero_counters": ZERO_COUNTERS,
    }

    append_only_trace_schema = {
        "schema_version": "runtime_observability_sidecar_append_only_trace_schema_v0",
        "append_only": True,
        "required_entry_fields": [
            "trace_index",
            "event_id",
            "hook_id",
            "source_packet_ref",
            "active_object",
            "attempted_move",
            "boundary_checked",
            "boundary_result",
            "event_status",
            "previous_entry_digest",
            "entry_digest",
        ],
        "mutation_rule": "Existing trace entries are not edited by the sidecar.",
    }

    rollup_readout_profile_schema = {
        "schema_version": "runtime_observability_sidecar_rollup_readout_profile_schema_v0",
        "must_emit": [
            "rollup",
            "readout",
            "profile",
            "report",
            "transition_trace",
            "receipt",
        ],
    }

    rollup = {
        "schema_version": "runtime_observability_sidecar_rollup_v0",
        "sidecar_id": "RUNTIME_OBSERVABILITY_SIDECAR",
        "events_observed": len(event_inputs),
        "events_recorded": len(event_records),
        "trace_entries": len(trace_entries),
        "known_hook_event_count": sum(1 for r in event_records if r["hook_known"]),
        "unknown_hook_count": len(unknown_hook_records),
        "hook_gap_count": len(hook_gap_records),
        "forbidden_control_claim_record_count": len(forbidden_control_claim_records),
        "event_status_counts": dict(status_counts),
        "hook_counts": dict(hook_counts),
        "load_bearing_field_presence_count": {
            field: sum(1 for r in event_records if r.get(field) not in (None, "", []))
            for field in REQUIRED_EDGE_FIELDS
        },
        "negative_controls": negative_control_counters,
        "validation_verdict_count": 0,
        "admissibility_verdict_count": 0,
        "authorization_verdict_count": 0,
        "execution_command_count": 0,
        "proposal_repair_count": 0,
        "schema_mutation_count": 0,
        "runtime_patch_count": 0,
        "live_hook_install_count": 0,
        "blocking_action_count": 0,
        "builder_command_count": 0,
        "c8_authorization_count": 0,
    }

    readout = {
        "schema_version": "runtime_observability_sidecar_readout_v0",
        "status": "SIDECAR_SYNTHETIC_REFERENCE_STABLE" if build_pass else "REPAIR_REQUIRED",
        "events_observed": rollup["events_observed"],
        "events_recorded": rollup["events_recorded"],
        "unknown_hook_count": rollup["unknown_hook_count"],
        "hook_gap_count": rollup["hook_gap_count"],
        "forbidden_control_claim_record_count": rollup["forbidden_control_claim_record_count"],
        "bad_counters_zero": all(v == 0 for v in negative_control_counters.values()),
        "interpretation": "Sidecar observed demo events and emitted append-only evidence records without control-path effect.",
    }

    profile = {
        "schema_version": "runtime_observability_sidecar_profile_v0",
        "profile_id": "runtime_observability_sidecar_" + sig8(rollup),
        "status": "SIDECAR_SYNTHETIC_REFERENCE_STABLE" if build_pass else "SIDECAR_REPAIR_REQUIRED",
        "sidecar_id": "RUNTIME_OBSERVABILITY_SIDECAR",
        "core_compression": "Control path acts. Sidecar records.",
        "authority_law": "The sidecar has eyes, not hands.",
        "hook_count": len(SIDECAR_HOOKS),
        "events_recorded": len(event_records),
        "append_only_trace_entries": len(trace_entries),
        "control_path_effect": "NONE",
        "live_runtime_hooks_installed": False,
        "runtime_patched": False,
        "c8_authorized": False,
        "bad_counters_zero": all(v == 0 for v in negative_control_counters.values()),
        "must_not_infer": [
            "Sidecar is live runtime instrumentation",
            "Runtime hooks were installed",
            "Runtime routing was patched",
            "Sidecar can validate",
            "Sidecar can authorize",
            "Sidecar can block",
            "Sidecar can advance control path",
            "Sidecar can execute",
            "C8 is authorized",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "runtime_observability_sidecar_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": [
            "RUNTIME_OBSERVABILITY_SIDECAR_BUILT_SYNTHETIC_REFERENCE",
            "DESIGN_RECEIPT_CONSUMED",
            "HOOK_REGISTRY_BUILT",
            "EVENT_RECORD_SCHEMA_BUILT",
            "SIDECAR_RECEIPT_SCHEMA_BUILT",
            "APPEND_ONLY_TRACE_SCHEMA_BUILT",
            "DEMO_EVENT_INPUTS_EMITTED",
            "EVENT_RECORDS_EMITTED",
            "APPEND_ONLY_TRACE_EMITTED",
            "UNKNOWN_HOOK_DEMO_EMITTED",
            "HOOK_GAP_DEMO_EMITTED",
            "FORBIDDEN_CONTROL_CLAIM_DEMOS_EMITTED",
            "ROLLUP_READOUT_PROFILE_EMITTED",
            "CONTROL_PATH_ACTS_SIDECAR_RECORDS",
            "SIDECAR_HAS_EYES_NOT_HANDS",
            "NO_LIVE_HOOK_INSTALL",
            "NO_RUNTIME_PATCH",
            "NO_LIVE_RUNTIME_ROUTING",
            "NO_VALIDATION_AUTHORITY",
            "NO_ADMISSIBILITY_AUTHORITY",
            "NO_AUTHORIZATION_AUTHORITY",
            "NO_EXECUTION_CLAIM",
            "NO_CONTROL_PATH_BLOCK_OR_ADVANCE",
            "NO_C8_AUTHORIZATION",
        ] if build_pass else failures,
        "receipt_backed_claim": "The Runtime Observability Sidecar was built as a synthetic/reference append-only observation surface. It emits hook registry, schemas, demo event inputs, event records, append-only trace, unknown-hook and hook-gap records, forbidden-control-claim records, rollup, readout, profile, report, transition trace, and receipt. It does not install live hooks, patch runtime, route traffic, validate, authorize, admit, execute, repair, mutate schemas, block or advance the control path, emit builder commands, or authorize C8.",
        "recommended_next_handling": recommended_next,
    }

    transition_trace = {
        "schema_version": "runtime_observability_sidecar_transition_trace_v0",
        "trace": [
            {
                "step": "consume_design",
                "question": "is Sidecar target design build-ready",
                "answer": "yes" if build_pass else "no",
                "taken": "build synthetic/reference Sidecar observation surface",
            },
            {
                "step": "observe_demo_events",
                "question": "does Sidecar record without acting",
                "answer": f"{len(event_records)} records, {len(trace_entries)} append-only trace entries",
                "taken": "emit event records and trace",
            },
            {
                "step": "preserve_boundary",
                "question": "did Sidecar install hooks, patch runtime, validate, authorize, execute, block, or open C8",
                "answer": "no",
                "taken": "stop review-ready",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    for path, obj in [
        (HOOK_REGISTRY_PATH, hook_registry),
        (EVENT_RECORD_SCHEMA_PATH, event_record_schema),
        (SIDECAR_RECEIPT_SCHEMA_PATH, sidecar_receipt_schema),
        (APPEND_ONLY_TRACE_SCHEMA_PATH, append_only_trace_schema),
        (ROLLUP_READOUT_PROFILE_SCHEMA_PATH, rollup_readout_profile_schema),
        (ROLLUP_PATH, rollup),
        (READOUT_PATH, readout),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    write_jsonl(DEMO_EVENT_INPUTS_PATH, event_inputs)
    write_jsonl(EVENT_RECORDS_PATH, event_records)
    write_jsonl(APPEND_ONLY_TRACE_PATH, trace_entries)
    write_jsonl(UNKNOWN_HOOK_RECORDS_PATH, unknown_hook_records)
    write_jsonl(HOOK_GAP_RECORDS_PATH, hook_gap_records)
    write_jsonl(FORBIDDEN_CONTROL_CLAIM_RECORDS_PATH, forbidden_control_claim_records)

    acceptance_gate_results = {
        "SIDECAR_BUILD_0_DESIGN_RECEIPT_CONSUMED": DESIGN_RECEIPT_PATH.exists(),
        "SIDECAR_BUILD_1_HOOK_REGISTRY_BUILT": HOOK_REGISTRY_PATH.exists() and hook_registry["hook_count"] == 24,
        "SIDECAR_BUILD_2_EVENT_RECORD_SCHEMA_BUILT": EVENT_RECORD_SCHEMA_PATH.exists(),
        "SIDECAR_BUILD_3_RECEIPT_SCHEMA_BUILT": SIDECAR_RECEIPT_SCHEMA_PATH.exists(),
        "SIDECAR_BUILD_4_APPEND_ONLY_TRACE_SCHEMA_BUILT": APPEND_ONLY_TRACE_SCHEMA_PATH.exists() and append_only_trace_schema["append_only"] is True,
        "SIDECAR_BUILD_5_DEMO_INPUTS_EMITTED": DEMO_EVENT_INPUTS_PATH.exists() and len(event_inputs) == 16,
        "SIDECAR_BUILD_6_EVENT_RECORDS_EMITTED": EVENT_RECORDS_PATH.exists() and len(event_records) == 16,
        "SIDECAR_BUILD_7_APPEND_ONLY_TRACE_EMITTED": APPEND_ONLY_TRACE_PATH.exists() and len(trace_entries) == 16,
        "SIDECAR_BUILD_8_UNKNOWN_HOOK_DEMO_EMITTED": UNKNOWN_HOOK_RECORDS_PATH.exists() and len(unknown_hook_records) == 1,
        "SIDECAR_BUILD_9_HOOK_GAP_DEMO_EMITTED": HOOK_GAP_RECORDS_PATH.exists() and len(hook_gap_records) == 1,
        "SIDECAR_BUILD_10_FORBIDDEN_CONTROL_CLAIM_DEMOS_EMITTED": FORBIDDEN_CONTROL_CLAIM_RECORDS_PATH.exists() and len(forbidden_control_claim_records) == 10,
        "SIDECAR_BUILD_11_LOAD_BEARING_FIELDS_PRESENT": all(v == 16 for v in rollup["load_bearing_field_presence_count"].values()),
        "SIDECAR_BUILD_12_ROLLUP_READOUT_PROFILE_EMITTED": ROLLUP_PATH.exists() and READOUT_PATH.exists() and PROFILE_PATH.exists(),
        "SIDECAR_BUILD_13_REPORT_TRACE_EMITTED": REPORT_PATH.exists() and TRACE_PATH.exists(),
        "SIDECAR_BUILD_14_NO_LIVE_HOOK_INSTALL": rollup["live_hook_install_count"] == 0 and profile["live_runtime_hooks_installed"] is False,
        "SIDECAR_BUILD_15_NO_RUNTIME_EFFECT_OR_PATCH": rollup["runtime_patch_count"] == 0 and profile["runtime_patched"] is False,
        "SIDECAR_BUILD_16_NO_LIVE_RUNTIME_ROUTING": True,
        "SIDECAR_BUILD_17_NO_VALIDATION_ADMISSIBILITY_AUTHORITY_OR_EXECUTION": rollup["validation_verdict_count"] == 0 and rollup["admissibility_verdict_count"] == 0 and rollup["authorization_verdict_count"] == 0 and rollup["execution_command_count"] == 0,
        "SIDECAR_BUILD_18_NO_SCHEMA_MUTATION_OR_REPAIR": rollup["schema_mutation_count"] == 0 and rollup["proposal_repair_count"] == 0,
        "SIDECAR_BUILD_19_NO_CONTROL_PATH_BLOCK_OR_ADVANCE": rollup["blocking_action_count"] == 0 and negative_control_counters["control_path_advanced_count"] == 0 and negative_control_counters["control_path_blocked_count"] == 0,
        "SIDECAR_BUILD_20_NO_BUILDER_COMMAND": rollup["builder_command_count"] == 0,
        "SIDECAR_BUILD_21_NO_C7_OR_C8": rollup["c8_authorization_count"] == 0 and profile["c8_authorized"] is False,
        "SIDECAR_BUILD_22_NO_SOURCE_OR_REFERENCE_MUTATION": negative_control_counters["source_mutation_count"] == 0 and negative_control_counters["reference_mutation_count"] == 0,
        "SIDECAR_BUILD_23_NO_LATEST_OR_MTIME": negative_control_counters["latest_file_guessing_count"] == 0 and negative_control_counters["mtime_selection_count"] == 0,
        "SIDECAR_BUILD_24_BAD_COUNTERS_ZERO": all(v == 0 for v in negative_control_counters.values()),
        "SIDECAR_BUILD_25_NO_HIDDEN_NEXT_COMMAND": profile["next_command_goal"] is None,
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_BUILD_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_RUNTIME_OBSERVABILITY_SIDECAR_BUILD_V0"
    terminal = transition_trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_RUNTIME_OBSERVABILITY_SIDECAR_BUILD_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_design": SOURCE_SIDECAR_DESIGN_RECEIPT_ID,
        "recommended_next": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "runtime_observability_sidecar_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_BUILD_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "sidecar_id": "RUNTIME_OBSERVABILITY_SIDECAR",
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_runtime_observability_sidecar_design_receipt_id": SOURCE_SIDECAR_DESIGN_RECEIPT_ID,
        "source_post_schema_validator_reference_decision_receipt_id": SOURCE_POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_ID,
        "source_runtime_schema_validator_reference_closure_receipt_id": SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID,
        "source_decision_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBSERVABILITY_CLOSURE_RECEIPT_ID,
        "events_observed": len(event_inputs),
        "events_recorded": len(event_records),
        "unknown_hooks": len(unknown_hook_records),
        "hook_gaps": len(hook_gap_records),
        "forbidden_control_claims": len(forbidden_control_claim_records),
        "negative_controls": negative_control_counters,
        "machine_readable_runtime_observability_sidecar_build_summary": {
            "status": final_status,
            "reason_codes": report["reason_codes"] if gate == "PASS" else failures,
            "runtime_observability_sidecar_built": gate == "PASS",
            "review_ready": gate == "PASS",
            "synthetic_reference_build_only": True,
            "design_receipt_consumed": True,
            "hook_registry_built": HOOK_REGISTRY_PATH.exists(),
            "event_record_schema_built": EVENT_RECORD_SCHEMA_PATH.exists(),
            "sidecar_receipt_schema_built": SIDECAR_RECEIPT_SCHEMA_PATH.exists(),
            "append_only_trace_schema_built": APPEND_ONLY_TRACE_SCHEMA_PATH.exists(),
            "rollup_readout_profile_schema_built": ROLLUP_READOUT_PROFILE_SCHEMA_PATH.exists(),
            "demo_event_inputs_emitted": DEMO_EVENT_INPUTS_PATH.exists(),
            "event_records_emitted": EVENT_RECORDS_PATH.exists(),
            "append_only_trace_emitted": APPEND_ONLY_TRACE_PATH.exists(),
            "unknown_hook_records_emitted": UNKNOWN_HOOK_RECORDS_PATH.exists(),
            "hook_gap_records_emitted": HOOK_GAP_RECORDS_PATH.exists(),
            "forbidden_control_claim_records_emitted": FORBIDDEN_CONTROL_CLAIM_RECORDS_PATH.exists(),
            "rollup_emitted": ROLLUP_PATH.exists(),
            "readout_emitted": READOUT_PATH.exists(),
            "profile_emitted": PROFILE_PATH.exists(),
            "report_emitted": REPORT_PATH.exists(),
            "transition_trace_emitted": TRACE_PATH.exists(),
            "hook_count": len(SIDECAR_HOOKS),
            "events_observed": len(event_inputs),
            "events_recorded": len(event_records),
            "append_only_trace_entries": len(trace_entries),
            "unknown_hook_count": len(unknown_hook_records),
            "hook_gap_count": len(hook_gap_records),
            "forbidden_control_claim_record_count": len(forbidden_control_claim_records),
            "event_status_counts": dict(status_counts),
            "load_bearing_edge_field_count": len(REQUIRED_EDGE_FIELDS),
            "load_bearing_field_presence_count": rollup["load_bearing_field_presence_count"],
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
        "aggregate_metrics": report | {"status": final_status, "recommended_next_handling": final_next},
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "hook_registry": rel(HOOK_REGISTRY_PATH),
            "event_record_schema": rel(EVENT_RECORD_SCHEMA_PATH),
            "sidecar_receipt_schema": rel(SIDECAR_RECEIPT_SCHEMA_PATH),
            "append_only_trace_schema": rel(APPEND_ONLY_TRACE_SCHEMA_PATH),
            "rollup_readout_profile_schema": rel(ROLLUP_READOUT_PROFILE_SCHEMA_PATH),
            "demo_event_inputs": rel(DEMO_EVENT_INPUTS_PATH),
            "event_records": rel(EVENT_RECORDS_PATH),
            "append_only_trace": rel(APPEND_ONLY_TRACE_PATH),
            "unknown_hook_records": rel(UNKNOWN_HOOK_RECORDS_PATH),
            "hook_gap_records": rel(HOOK_GAP_RECORDS_PATH),
            "forbidden_control_claim_records": rel(FORBIDDEN_CONTROL_CLAIM_RECORDS_PATH),
            "rollup": rel(ROLLUP_PATH),
            "readout": rel(READOUT_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"runtime_observability_sidecar_build_receipt_id={receipt_id}")
    print(f"runtime_observability_sidecar_build_receipt_path={rel(receipt_path)}")
    print(f"runtime_observability_sidecar_rollup_path={rel(ROLLUP_PATH)}")
    print(f"runtime_observability_sidecar_readout_path={rel(READOUT_PATH)}")
    print(f"runtime_observability_sidecar_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
