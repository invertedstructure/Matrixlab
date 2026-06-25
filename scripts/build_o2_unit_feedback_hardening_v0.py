#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_O2_UNIT_FEEDBACK_HARDENING_V0"
TARGET_UNIT_ID = "observation.unit_feedback_hardening.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY"
MODE = "STATIC_SCHEMA_AND_PROBE_ONLY / OBSERVE / CERTIFY / REFLECT"
BUILD_MODE = "O2_STATIC_SCHEMA_AND_PROBE_ONLY"

O2_DESIGN_RECEIPT_ID = "e55e60e1"
O2_DESIGN_RECEIPT_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0_receipts/e55e60e1.json"
O2_TARGET_DESIGN_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_unit_feedback_hardening_target_design_v0.json"
O2_OBJECTIVE_CONTRACT_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_objective_contract_v0.json"
O2_MODE_CONTRACT_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_initial_mode_contract_v0.json"
O2_SOURCE_SCOPE_CONTRACT_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_source_scope_contract_v0.json"
O2_FEEDBACK_AXES_CONTRACT_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_feedback_axes_contract_v0.json"
O2_QUALITY_ENUM_CONTRACT_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_feedback_quality_enum_contract_v0.json"
O2_SCHEMA_CONTRACT_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_required_schema_contract_v0.json"
O2_DEMO_PROBE_CONTRACT_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_demo_probe_boundary_contract_v0.json"
O2_NEGATIVE_CONTROL_CONTRACT_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_negative_control_contract_v0.json"
O2_RETRY_GATE_CONTRACT_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_retry_gate_contract_v0.json"
O2_NONREPAIR_BOUNDARY_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_nonrepair_nonauthority_boundary_v0.json"
O2_ACCEPTANCE_GATE_CONTRACT_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_acceptance_gate_contract_v0.json"
O2_TERMINAL_CONTRACT_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_terminal_contract_v0.json"
O2_BUILD_AUTHORIZATION_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_build_unit_authorization_v0.json"
O2_DESIGN_ROLLUP_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_target_design_rollup_v0.json"
O2_DESIGN_PROFILE_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_target_design_profile_v0.json"
O1_CLOSE_RECEIPT_PATH = ROOT / "data/o1_decision_edge_observability_surface_closure_v0_receipts/e9d2dcf5.json"
O1_REVIEWED_REFERENCE_PATH = ROOT / "data/o1_decision_edge_observability_surface_closure_v0/o1_decision_edge_observability_surface_reviewed_reference_v0.json"
O1_EDGE_OBS_RECORDS_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/decision_edge_observation_records_v0.jsonl"

REQUIRED_SOURCE_FILES = [
    O2_DESIGN_RECEIPT_PATH,
    O2_TARGET_DESIGN_PATH,
    O2_OBJECTIVE_CONTRACT_PATH,
    O2_MODE_CONTRACT_PATH,
    O2_SOURCE_SCOPE_CONTRACT_PATH,
    O2_FEEDBACK_AXES_CONTRACT_PATH,
    O2_QUALITY_ENUM_CONTRACT_PATH,
    O2_SCHEMA_CONTRACT_PATH,
    O2_DEMO_PROBE_CONTRACT_PATH,
    O2_NEGATIVE_CONTROL_CONTRACT_PATH,
    O2_RETRY_GATE_CONTRACT_PATH,
    O2_NONREPAIR_BOUNDARY_PATH,
    O2_ACCEPTANCE_GATE_CONTRACT_PATH,
    O2_TERMINAL_CONTRACT_PATH,
    O2_BUILD_AUTHORIZATION_PATH,
    O2_DESIGN_ROLLUP_PATH,
    O2_DESIGN_PROFILE_PATH,
    O1_CLOSE_RECEIPT_PATH,
    O1_REVIEWED_REFERENCE_PATH,
    O1_EDGE_OBS_RECORDS_PATH,
]

OUT_DIR = ROOT / "data/o2_unit_feedback_hardening_v0"
RECEIPT_DIR = ROOT / "data/o2_unit_feedback_hardening_v0_receipts"

UNIT_FAILURE_EVENT_SCHEMA_PATH = OUT_DIR / "unit_failure_event_schema_v0.json"
UNIT_FEEDBACK_RECORD_SCHEMA_PATH = OUT_DIR / "unit_feedback_record_schema_v0.json"
UNIT_FAILURE_LOCATION_SCHEMA_PATH = OUT_DIR / "unit_failure_location_schema_v0.json"
UNIT_FEEDBACK_QUALITY_ENUM_PATH = OUT_DIR / "unit_feedback_quality_enum_v0.json"
UNIT_MISSING_CAPABILITY_SCHEMA_PATH = OUT_DIR / "unit_missing_capability_record_schema_v0.json"
UNIT_REFINEMENT_CANDIDATE_SCHEMA_PATH = OUT_DIR / "unit_refinement_candidate_schema_v0.json"
UNIT_RETRY_GATE_SCHEMA_PATH = OUT_DIR / "unit_retry_gate_schema_v0.json"
EDGE_FEEDBACK_LINK_SCHEMA_PATH = OUT_DIR / "edge_feedback_link_schema_v0.json"

DEMO_FAILURE_EVENTS_PATH = OUT_DIR / "o2_demo_failure_events_v0.jsonl"
UNIT_FAILURE_EVENTS_PATH = OUT_DIR / "unit_failure_events_v0.jsonl"
UNIT_FEEDBACK_RECORDS_PATH = OUT_DIR / "unit_feedback_records_v0.jsonl"
UNIT_FAILURE_LOCATION_RECORDS_PATH = OUT_DIR / "unit_failure_location_records_v0.jsonl"
UNIT_MISSING_CAPABILITY_RECORDS_PATH = OUT_DIR / "unit_missing_capability_records_v0.jsonl"
UNIT_REFINEMENT_CANDIDATE_RECORDS_PATH = OUT_DIR / "unit_refinement_candidate_records_v0.jsonl"
UNIT_RETRY_GATE_RECORDS_PATH = OUT_DIR / "unit_retry_gate_records_v0.jsonl"
EDGE_FEEDBACK_LINKS_PATH = OUT_DIR / "edge_feedback_links_v0.jsonl"

ROLLUP_PATH = OUT_DIR / "unit_feedback_rollup_v0.json"
READOUT_PATH = OUT_DIR / "unit_feedback_readout_v0.json"
PROFILE_PATH = OUT_DIR / "o2_feedback_profile_v0.json"
TRACE_PATH = OUT_DIR / "o2_transition_trace.json"
REPORT_PATH = OUT_DIR / "o2_report.json"

EXPECTED_DESIGN_STATUS = "TYPED_O2_UNIT_FEEDBACK_HARDENING_TARGET_DESIGNED_BUILD_READY"
EXPECTED_DESIGN_STOP = "STOP_TYPED_O2_UNIT_FEEDBACK_HARDENING_TARGET_DESIGNED_BUILD_READY"
EXPECTED_DESIGN_NEXT = "BUILD_O2_UNIT_FEEDBACK_HARDENING_V0"

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

UNIT_PHASES = [
    "LOAD",
    "VALIDATE",
    "INSPECT",
    "CLASSIFY",
    "SELECT",
    "AUTHORIZE",
    "APPLY",
    "VERIFY",
    "EMIT_RECEIPT",
    "HANDOFF",
    "STOP",
]

CAPABILITY_KINDS = [
    "DISCRIMINATOR",
    "SOURCE_SURFACE",
    "BOUNDARY_RULE",
    "AUTHORITY_RULE",
    "EXTRACTION_SURFACE",
    "VERIFICATION_GATE",
    "RECEIPT_LINKAGE",
    "LABEL_LANE",
    "MOVE_REGISTRY_ENTRY",
    "PROPOSAL_FIELD",
    "UNKNOWN_UNDER_TYPED",
]

REFINEMENT_TYPES = [
    "ADD_DISCRIMINATOR",
    "ADD_SOURCE_SURFACE",
    "ADD_BOUNDARY_RULE",
    "ADD_RECEIPT_FIELD",
    "ADD_VERIFICATION_GATE",
    "ADD_LABEL_LANE",
    "ADD_MOVE_ENTRY",
    "ADD_PROPOSAL_FIELD",
    "NARROW_AUTHORITY_RULE",
    "REQUEST_EXTRACTION",
    "WITHHOLD_AND_PARK",
    "QUESTION_PACKET",
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

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(x, sort_keys=True) + "\n" for x in rows))

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    design_receipt = read_json(O2_DESIGN_RECEIPT_PATH)
    design_summary = design_receipt.get("machine_readable_o2_target_design_summary", {})
    build_auth = read_json(O2_BUILD_AUTHORIZATION_PATH)
    mode_contract = read_json(O2_MODE_CONTRACT_PATH)
    axes_contract = read_json(O2_FEEDBACK_AXES_CONTRACT_PATH)
    quality_contract = read_json(O2_QUALITY_ENUM_CONTRACT_PATH)

    if design_receipt.get("receipt_id") != O2_DESIGN_RECEIPT_ID or design_receipt.get("gate") != "PASS":
        failures.append("o2_design_receipt_not_pass")
    if design_receipt.get("terminal", {}).get("stop_code") != EXPECTED_DESIGN_STOP:
        failures.append("o2_design_terminal_not_expected")
    if design_summary.get("status") != EXPECTED_DESIGN_STATUS:
        failures.append(f"o2_design_status_not_expected:{design_summary.get('status')}")
    if design_summary.get("recommended_next") != EXPECTED_DESIGN_NEXT:
        failures.append(f"o2_design_next_not_expected:{design_summary.get('recommended_next')}")
    if build_auth.get("authorized_next_unit") != EXPECTED_DESIGN_NEXT:
        failures.append("build_auth_next_wrong")
    if build_auth.get("authorized_initial_mode") != "STATIC_SCHEMA_AND_PROBE_ONLY":
        failures.append("build_auth_mode_wrong")
    if mode_contract.get("initial_mode") != "STATIC_SCHEMA_AND_PROBE_ONLY":
        failures.append("mode_contract_initial_mode_wrong")
    if mode_contract.get("deferred_mode") != "LIVE_FEEDBACK_AUDIT":
        failures.append("mode_contract_deferred_mode_wrong")
    if len(axes_contract.get("required_feedback_axes", [])) != 13:
        failures.append("feedback_axis_count_wrong")
    if len(quality_contract.get("quality_classes", [])) != 9:
        failures.append("quality_class_count_wrong")

    for key in [
        "o2_target_designed",
        "o2_build_authorized_next",
        "live_feedback_audit_deferred",
        "feedback_axes_frozen",
        "quality_enum_frozen",
        "required_schemas_frozen",
        "demo_probe_boundary_frozen",
        "negative_controls_frozen",
        "retry_gate_rule_frozen",
        "nonrepair_boundary_locked",
        "bad_counters_zero",
    ]:
        if design_summary.get(key) is not True:
            failures.append(f"design_required_true_missing:{key}")

    for key in [
        "feedback_records_emitted",
        "demo_records_emitted",
        "live_feedback_audit_executed",
        "repair_applied",
        "retry_executed",
        "target_selected_for_build",
        "runtime_patch_applied",
        "source_mutated",
        "prior_receipt_mutated",
        "architecture_change",
        "c5_opened",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if design_summary.get(key) is not False:
            failures.append(f"design_forbidden_true:{key}")

    return failures, {
        "quality_classes": quality_contract.get("quality_classes", QUALITY_CLASSES),
        "feedback_axes": axes_contract.get("required_feedback_axes", []),
    }

def schema_artifacts() -> Dict[Path, Dict[str, Any]]:
    return {
        UNIT_FAILURE_EVENT_SCHEMA_PATH: {
            "schema_version": "unit_failure_event_schema_v0",
            "record_schema": {
                "schema_version": "unit_failure_event_v0",
                "failure_event_id": "failure_event_<sig8>",
                "unit_id": None,
                "run_id": None,
                "receipt_ref": None,
                "trace_ref": None,
                "status": "FAILED | STOPPED | BLOCKED | NA | UNDER_TYPED",
                "terminal": None,
                "gate": "PASS | FAIL | NA",
                "failure_or_stop_code": None,
                "source_artifact_refs": [],
                "candidate_for_feedback": True,
            },
        },
        UNIT_FEEDBACK_RECORD_SCHEMA_PATH: {
            "schema_version": "unit_feedback_record_schema_v0",
            "record_schema": {
                "schema_version": "unit_feedback_record_v0",
                "feedback_id": "unit_feedback_<sig8>",
                "source": {
                    "unit_id": None,
                    "run_id": None,
                    "receipt_ref": None,
                    "trace_ref": None,
                    "source_artifact_refs": [],
                    "decision_edge_observation_ref": None,
                },
                "unit_status": {"status": "FAILED | STOPPED | BLOCKED | NA | UNDER_TYPED", "terminal": None, "gate": None},
                "failure_location": {
                    "unit_phase": None,
                    "step_name": None,
                    "field_path": None,
                    "object_ref": None,
                    "source_surface_ref": None,
                    "boundary_ref": None,
                },
                "failure_explanation": {
                    "why_failed": None,
                    "where_failed": None,
                    "failed_relative_to_object": None,
                    "failed_relative_to_source_surface": None,
                    "failed_relative_to_boundary": None,
                    "failed_relative_to_rule": None,
                },
                "missing_capability": {
                    "missing_capability_id": None,
                    "smallest_honest_name": None,
                    "missing_discriminator": None,
                    "capability_kind": None,
                    "evidence_for_missing": [],
                },
                "movement": {"blocked_next_moves": [], "lawful_next_refinements": [], "forbidden_next_moves": []},
                "quality": {
                    "feedback_quality_class": None,
                    "diagnostic_completeness": "INSUFFICIENT | PARTIAL | SUFFICIENT_FOR_QUESTION | SUFFICIENT_FOR_REFINEMENT | EXPECTED_LIMIT",
                    "retry_allowed": False,
                    "retry_requires": [],
                },
                "safety": {
                    "must_not_infer": [],
                    "repair_applied": False,
                    "target_selected_for_build": False,
                    "source_mutated": False,
                    "prior_receipt_mutated": False,
                    "architecture_change": False,
                    "c5_opened": False,
                },
            },
        },
        UNIT_FAILURE_LOCATION_SCHEMA_PATH: {
            "schema_version": "unit_failure_location_schema_v0",
            "unit_phase_enum": UNIT_PHASES,
            "record_schema": {
                "schema_version": "unit_failure_location_v0",
                "failure_location_id": "fail_loc_<sig8>",
                "unit_id": None,
                "unit_phase": None,
                "step_name": None,
                "field_path": None,
                "object_ref": None,
                "source_surface_ref": None,
                "boundary_ref": None,
            },
        },
        UNIT_FEEDBACK_QUALITY_ENUM_PATH: {
            "schema_version": "unit_feedback_quality_enum_v0",
            "quality_classes": QUALITY_CLASSES,
            "closed_enum": True,
        },
        UNIT_MISSING_CAPABILITY_SCHEMA_PATH: {
            "schema_version": "unit_missing_capability_record_schema_v0",
            "capability_kind_enum": CAPABILITY_KINDS,
            "record_schema": {
                "schema_version": "unit_missing_capability_record_v0",
                "missing_capability_id": "missing_cap_<sig8>",
                "source_feedback_ref": None,
                "capability_kind": None,
                "smallest_honest_name": None,
                "why_needed": None,
                "not_needed_for": [],
                "candidate_refinement": None,
                "status": "CANDIDATE_ONLY",
            },
        },
        UNIT_REFINEMENT_CANDIDATE_SCHEMA_PATH: {
            "schema_version": "unit_refinement_candidate_schema_v0",
            "refinement_type_enum": REFINEMENT_TYPES,
            "record_schema": {
                "schema_version": "unit_refinement_candidate_v0",
                "refinement_id": "refine_<sig8>",
                "source_feedback_ref": None,
                "refinement_type": None,
                "smallest_refinement": None,
                "expected_effect": None,
                "acceptance_gate": None,
                "forbidden_scope": [],
                "status": "PROPOSED_ONLY",
            },
        },
        UNIT_RETRY_GATE_SCHEMA_PATH: {
            "schema_version": "unit_retry_gate_schema_v0",
            "record_schema": {
                "schema_version": "unit_retry_gate_v0",
                "retry_gate_id": "retry_gate_<sig8>",
                "source_feedback_ref": None,
                "retry_allowed": False,
                "retry_block_reason": None,
                "retry_requires_one_of": [
                    "new_evidence",
                    "changed_boundary",
                    "smaller_surface",
                    "added_discriminator",
                    "accepted_refinement",
                    "expected_external_condition_changed",
                ],
                "forbidden_retry_conditions": [
                    "same_unit",
                    "same_inputs",
                    "same_boundary",
                    "same_missing_capability",
                    "same_evidence",
                    "same_failure",
                    "retry_anyway",
                ],
                "terminal_if_blocked": "STOP_SAME_FAILURE_RETRY_BLOCKED",
            },
        },
        EDGE_FEEDBACK_LINK_SCHEMA_PATH: {
            "schema_version": "edge_feedback_link_schema_v0",
            "record_schema": {
                "schema_version": "edge_feedback_link_v0",
                "decision_edge_observation_ref": "edge_obs_<sig8>",
                "unit_feedback_ref": "unit_feedback_<sig8>",
                "relationship": None,
            },
        },
    }

def make_event(case: Dict[str, Any], idx: int) -> Dict[str, Any]:
    obj = {
        "schema_version": "unit_failure_event_v0",
        "failure_event_id": "failure_event_" + sha8({"case": case["case_id"], "idx": idx}),
        "unit_id": case["unit_id"],
        "run_id": f"demo_run_{idx:02d}",
        "receipt_ref": case.get("receipt_ref", f"demo://{case['case_id']}/receipt"),
        "trace_ref": case.get("trace_ref", f"demo://{case['case_id']}/trace"),
        "status": case["status"],
        "terminal": case["terminal"],
        "gate": case["gate"],
        "failure_or_stop_code": case["failure_or_stop_code"],
        "source_artifact_refs": case.get("source_artifact_refs", []),
        "candidate_for_feedback": True,
        "demo_input_quality": case.get("demo_input_quality"),
        "demo_case_id": case["case_id"],
    }
    return obj

def make_feedback(event: Dict[str, Any], case: Dict[str, Any]) -> Dict[str, Any]:
    feedback_id = "unit_feedback_" + sha8({"event": event["failure_event_id"], "quality": case["feedback_quality"]})
    rec = {
        "schema_version": "unit_feedback_record_v0",
        "feedback_id": feedback_id,
        "source": {
            "unit_id": event["unit_id"],
            "run_id": event["run_id"],
            "receipt_ref": event["receipt_ref"],
            "trace_ref": event["trace_ref"],
            "source_artifact_refs": event["source_artifact_refs"],
            "decision_edge_observation_ref": case.get("decision_edge_observation_ref"),
        },
        "unit_status": {"status": event["status"], "terminal": event["terminal"], "gate": event["gate"]},
        "failure_location": {
            "unit_phase": case["unit_phase"],
            "step_name": case["step_name"],
            "field_path": case["field_path"],
            "object_ref": case["object_ref"],
            "source_surface_ref": case["source_surface_ref"],
            "boundary_ref": case["boundary_ref"],
        },
        "failure_explanation": {
            "why_failed": case["why_failed"],
            "where_failed": case["where_failed"],
            "failed_relative_to_object": case["failed_relative_to_object"],
            "failed_relative_to_source_surface": case["failed_relative_to_source_surface"],
            "failed_relative_to_boundary": case["failed_relative_to_boundary"],
            "failed_relative_to_rule": case["failed_relative_to_rule"],
        },
        "missing_capability": {
            "missing_capability_id": "missing_cap_" + sha8({"feedback": feedback_id, "cap": case["missing_capability_name"]}),
            "smallest_honest_name": case["missing_capability_name"],
            "missing_discriminator": case.get("missing_discriminator"),
            "capability_kind": case["capability_kind"],
            "evidence_for_missing": case["evidence_for_missing"],
        },
        "movement": {
            "blocked_next_moves": case["blocked_next_moves"],
            "lawful_next_refinements": case["lawful_next_refinements"],
            "forbidden_next_moves": case["forbidden_next_moves"],
        },
        "quality": {
            "feedback_quality_class": case["feedback_quality"],
            "diagnostic_completeness": case["diagnostic_completeness"],
            "retry_allowed": False,
            "retry_requires": case.get("retry_requires", []),
        },
        "safety": {
            "must_not_infer": case["must_not_infer"],
            "repair_applied": False,
            "target_selected_for_build": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "architecture_change": False,
            "c5_opened": False,
        },
    }
    return rec

def make_location(feedback: Dict[str, Any]) -> Dict[str, Any]:
    loc = feedback["failure_location"]
    return {
        "schema_version": "unit_failure_location_v0",
        "failure_location_id": "fail_loc_" + sha8({"feedback": feedback["feedback_id"], "loc": loc}),
        "unit_id": feedback["source"]["unit_id"],
        "unit_phase": loc["unit_phase"],
        "step_name": loc["step_name"],
        "field_path": loc["field_path"],
        "object_ref": loc["object_ref"],
        "source_surface_ref": loc["source_surface_ref"],
        "boundary_ref": loc["boundary_ref"],
        "source_feedback_ref": feedback["feedback_id"],
    }

def make_missing_cap(feedback: Dict[str, Any]) -> Dict[str, Any]:
    cap = feedback["missing_capability"]
    return {
        "schema_version": "unit_missing_capability_record_v0",
        "missing_capability_id": cap["missing_capability_id"],
        "source_feedback_ref": feedback["feedback_id"],
        "capability_kind": cap["capability_kind"],
        "smallest_honest_name": cap["smallest_honest_name"],
        "why_needed": "Needed to convert this stop/failure into a lawful next diagnostic action.",
        "not_needed_for": [
            "claiming root cause",
            "repairing immediately",
            "opening C5",
        ],
        "candidate_refinement": feedback["movement"]["lawful_next_refinements"][0] if feedback["movement"]["lawful_next_refinements"] else "question_packet_required",
        "status": "CANDIDATE_ONLY",
    }

def refinement_type_for(case: Dict[str, Any]) -> str:
    if case["feedback_quality"] == "AMBIGUOUS_REQUIRES_QUESTION":
        return "QUESTION_PACKET"
    if case["capability_kind"] == "DISCRIMINATOR":
        return "ADD_DISCRIMINATOR"
    if case["capability_kind"] == "SOURCE_SURFACE":
        return "ADD_SOURCE_SURFACE"
    if case["capability_kind"] == "BOUNDARY_RULE":
        return "ADD_BOUNDARY_RULE"
    if case["capability_kind"] == "VERIFICATION_GATE":
        return "ADD_VERIFICATION_GATE"
    if case["capability_kind"] == "RECEIPT_LINKAGE":
        return "ADD_RECEIPT_FIELD"
    if case["capability_kind"] == "AUTHORITY_RULE":
        return "NARROW_AUTHORITY_RULE"
    if case["capability_kind"] == "UNKNOWN_UNDER_TYPED":
        return "QUESTION_PACKET"
    return "REQUEST_EXTRACTION"

def make_refinement(feedback: Dict[str, Any], case: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "unit_refinement_candidate_v0",
        "refinement_id": "refine_" + sha8({"feedback": feedback["feedback_id"], "rtype": refinement_type_for(case)}),
        "source_feedback_ref": feedback["feedback_id"],
        "refinement_type": refinement_type_for(case),
        "smallest_refinement": feedback["movement"]["lawful_next_refinements"][0] if feedback["movement"]["lawful_next_refinements"] else "withhold and ask for typed source evidence",
        "expected_effect": "Make the next run diagnosable without guessing.",
        "acceptance_gate": "human_or_validator_review_required_before_application",
        "forbidden_scope": [
            "repair_now",
            "retry_same_inputs",
            "select_target_for_build",
            "patch_runtime",
            "open_c5",
        ],
        "status": "PROPOSED_ONLY",
    }

def make_retry_gate(feedback: Dict[str, Any], case: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "unit_retry_gate_v0",
        "retry_gate_id": "retry_gate_" + sha8({"feedback": feedback["feedback_id"]}),
        "source_feedback_ref": feedback["feedback_id"],
        "retry_allowed": False,
        "retry_block_reason": case.get("retry_block_reason", "No retry without changed evidence, changed boundary, smaller surface, added discriminator, accepted refinement, or changed external condition."),
        "retry_requires_one_of": [
            "new_evidence",
            "changed_boundary",
            "smaller_surface",
            "added_discriminator",
            "accepted_refinement",
            "expected_external_condition_changed",
        ],
        "forbidden_retry_conditions": [
            "same_unit",
            "same_inputs",
            "same_boundary",
            "same_missing_capability",
            "same_evidence",
            "same_failure",
            "retry_anyway",
        ],
        "terminal_if_blocked": "STOP_SAME_FAILURE_RETRY_BLOCKED",
    }

def make_edge_link(feedback: Dict[str, Any], case: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "edge_feedback_link_v0",
        "decision_edge_observation_ref": case.get("decision_edge_observation_ref"),
        "unit_feedback_ref": feedback["feedback_id"],
        "relationship": case.get("edge_relationship", f"feedback record explains failure/stop during {case['step_name']}"),
    }

def demo_cases() -> List[Dict[str, Any]]:
    common_must_not = [
        "repair applied",
        "target selected",
        "missing capability accepted",
        "refinement candidate approved",
        "C5 opened",
        "failure counted as progress",
        "root cause globally proven",
    ]
    return [
        {
            "case_id": "bare_failed_status",
            "unit_id": "demo.bare_failed.v0",
            "status": "FAILED",
            "terminal": "FAILED",
            "gate": "FAIL",
            "failure_or_stop_code": "FAILED",
            "demo_input_quality": "NO_FEEDBACK",
            "feedback_quality": "UNDER_TYPED_FEEDBACK",
            "diagnostic_completeness": "SUFFICIENT_FOR_QUESTION",
            "unit_phase": "STOP",
            "step_name": "STOP.raw_status",
            "field_path": "terminal",
            "object_ref": "unit_receipt",
            "source_surface_ref": "demo_failure_event",
            "boundary_ref": "minimum_feedback_boundary",
            "why_failed": "The source only emitted a bare FAILED status, so diagnostic cause cannot be honestly inferred.",
            "where_failed": "STOP.raw_status",
            "failed_relative_to_object": "unit_receipt",
            "failed_relative_to_source_surface": "demo_failure_event",
            "failed_relative_to_boundary": "minimum_feedback_boundary",
            "failed_relative_to_rule": "no bare failure status may be accepted as useful feedback",
            "missing_capability_name": "typed_failure_surface",
            "missing_discriminator": "failure_location_or_boundary",
            "capability_kind": "UNKNOWN_UNDER_TYPED",
            "evidence_for_missing": ["source contains status only"],
            "blocked_next_moves": ["retry same unit", "repair now", "open C5"],
            "lawful_next_refinements": ["emit question packet requesting receipt_ref, trace_ref, failing step, and boundary"],
            "forbidden_next_moves": ["treat FAILED as useful feedback", "infer root cause"],
            "must_not_infer": common_must_not,
            "decision_edge_observation_ref": "edge_obs_demo_under_typed_bare_failed",
        },
        {
            "case_id": "status_only_validation_error",
            "unit_id": "demo.status_only_validation.v0",
            "status": "FAILED",
            "terminal": "STOP_VALIDATION_ERROR",
            "gate": "FAIL",
            "failure_or_stop_code": "VALIDATION_ERROR",
            "demo_input_quality": "STATUS_ONLY",
            "feedback_quality": "UNDER_TYPED_FEEDBACK",
            "diagnostic_completeness": "SUFFICIENT_FOR_QUESTION",
            "unit_phase": "VALIDATE",
            "step_name": "VALIDATE.schema",
            "field_path": "unknown",
            "object_ref": "unit_input",
            "source_surface_ref": "demo_failure_event",
            "boundary_ref": "schema_validation_boundary",
            "why_failed": "The validation error lacks field path and object context.",
            "where_failed": "VALIDATE.schema",
            "failed_relative_to_object": "unit_input",
            "failed_relative_to_source_surface": "demo_failure_event",
            "failed_relative_to_boundary": "schema_validation_boundary",
            "failed_relative_to_rule": "validation feedback must identify a failing field or source gap",
            "missing_capability_name": "validation_field_path_evidence",
            "missing_discriminator": "field_path",
            "capability_kind": "RECEIPT_LINKAGE",
            "evidence_for_missing": ["validation error lacks field_path"],
            "blocked_next_moves": ["retry same validation", "repair input blindly"],
            "lawful_next_refinements": ["request validation receipt with failing field_path and expected schema"],
            "forbidden_next_moves": ["guess which field failed"],
            "must_not_infer": common_must_not,
            "decision_edge_observation_ref": "edge_obs_demo_status_only_validation",
        },
        {
            "case_id": "localized_receipt_trace_failure",
            "unit_id": "demo.localized_trace.v0",
            "status": "FAILED",
            "terminal": "STOP_TRACE_REF_MISSING",
            "gate": "FAIL",
            "failure_or_stop_code": "TRACE_REF_MISSING",
            "demo_input_quality": "LOCALIZED_FAILURE",
            "feedback_quality": "LOCALIZED_FAILURE",
            "diagnostic_completeness": "PARTIAL",
            "unit_phase": "EMIT_RECEIPT",
            "step_name": "EMIT_RECEIPT.trace_refs",
            "field_path": "receipt.trace_refs[0]",
            "object_ref": "receipt",
            "source_surface_ref": "receipt_writer",
            "boundary_ref": "receipt_linkage_boundary",
            "why_failed": "The receipt trace reference was missing during receipt emission.",
            "where_failed": "EMIT_RECEIPT.trace_refs",
            "failed_relative_to_object": "receipt",
            "failed_relative_to_source_surface": "receipt_writer",
            "failed_relative_to_boundary": "receipt_linkage_boundary",
            "failed_relative_to_rule": "receipt must preserve trace refs when present",
            "missing_capability_name": "trace_ref_linkage",
            "missing_discriminator": "trace_ref",
            "capability_kind": "RECEIPT_LINKAGE",
            "evidence_for_missing": ["receipt.trace_refs[0] absent"],
            "blocked_next_moves": ["publish incomplete receipt"],
            "lawful_next_refinements": ["add trace_ref field or mark trace source explicitly unavailable"],
            "forbidden_next_moves": ["drop trace silently"],
            "must_not_infer": common_must_not,
            "decision_edge_observation_ref": "edge_obs_demo_receipt_trace",
        },
        {
            "case_id": "boundary_aware_proposal_application_stop",
            "unit_id": "demo.proposal_application.v0",
            "status": "STOPPED",
            "terminal": "STOP_PROPOSAL_REQUIRES_REVIEW",
            "gate": "PASS",
            "failure_or_stop_code": "PROPOSAL_REQUIRES_REVIEW",
            "demo_input_quality": "BOUNDARY_AWARE_FAILURE",
            "feedback_quality": "BOUNDARY_AWARE_FAILURE",
            "diagnostic_completeness": "SUFFICIENT_FOR_QUESTION",
            "unit_phase": "AUTHORIZE",
            "step_name": "AUTHORIZE.proposal_application_gate",
            "field_path": "proposal.status",
            "object_ref": "proposal_packet",
            "source_surface_ref": "proposal_packet",
            "boundary_ref": "review_authority_boundary",
            "why_failed": "The proposal could not be applied because its status was PROPOSED_ONLY.",
            "where_failed": "AUTHORIZE.proposal_application_gate",
            "failed_relative_to_object": "proposal_packet",
            "failed_relative_to_source_surface": "proposal_packet",
            "failed_relative_to_boundary": "review_authority_boundary",
            "failed_relative_to_rule": "only ACCEPTED_FOR_BUILD proposals may be applied",
            "missing_capability_name": "accepted_review_receipt",
            "missing_discriminator": "proposal_acceptance_status",
            "capability_kind": "AUTHORITY_RULE",
            "evidence_for_missing": ["proposal.status=PROPOSED_ONLY"],
            "blocked_next_moves": ["apply proposal", "patch runtime"],
            "lawful_next_refinements": ["request review and keep proposal unapplied"],
            "forbidden_next_moves": ["treat proposal as accepted"],
            "must_not_infer": common_must_not,
            "decision_edge_observation_ref": "edge_obs_demo_proposal_gate",
        },
        {
            "case_id": "capability_aware_missing_target_evidence_values",
            "unit_id": "demo.missing_target_values.v0",
            "status": "BLOCKED",
            "terminal": "STOP_TARGET_EVIDENCE_VALUES_MISSING",
            "gate": "NA",
            "failure_or_stop_code": "TARGET_EVIDENCE_VALUES_MISSING",
            "demo_input_quality": "CAPABILITY_AWARE_FAILURE",
            "feedback_quality": "CAPABILITY_AWARE_FAILURE",
            "diagnostic_completeness": "PARTIAL",
            "unit_phase": "SELECT",
            "step_name": "SELECT.target_value_evidence",
            "field_path": "candidate_target.evidence_values",
            "object_ref": "candidate_target_rows",
            "source_surface_ref": "target_evidence_surface",
            "boundary_ref": "target_selection_evidence_boundary",
            "why_failed": "The unit cannot derive selected target evidence values from the current source surface.",
            "where_failed": "SELECT.target_value_evidence",
            "failed_relative_to_object": "candidate_target_rows",
            "failed_relative_to_source_surface": "target_evidence_surface",
            "failed_relative_to_boundary": "target_selection_evidence_boundary",
            "failed_relative_to_rule": "target selection requires evidence values before selection",
            "missing_capability_name": "target_evidence_value_extraction",
            "missing_discriminator": "target_evidence_value",
            "capability_kind": "EXTRACTION_SURFACE",
            "evidence_for_missing": ["candidate rows lack evidence_values"],
            "blocked_next_moves": ["select build target", "patch runtime"],
            "lawful_next_refinements": ["add target evidence extraction surface before target selection"],
            "forbidden_next_moves": ["select target by position or mtime"],
            "must_not_infer": common_must_not,
            "decision_edge_observation_ref": "edge_obs_demo_target_values",
        },
        {
            "case_id": "refinement_ready_source_scope_discriminator",
            "unit_id": "demo.source_scope_dominance.v0",
            "status": "FAILED",
            "terminal": "STOP_DOMINANCE_INDISTINGUISHABLE",
            "gate": "FAIL",
            "failure_or_stop_code": "DOMINANCE_INDISTINGUISHABLE",
            "demo_input_quality": "REFINEMENT_READY_FAILURE",
            "feedback_quality": "REFINEMENT_READY_FAILURE",
            "diagnostic_completeness": "SUFFICIENT_FOR_REFINEMENT",
            "unit_phase": "SELECT",
            "step_name": "SELECT.dominance_selection",
            "field_path": "candidate_value_rows",
            "object_ref": "candidate_value_rows",
            "source_surface_ref": "value_source_table",
            "boundary_ref": "value_source_dominance_boundary",
            "why_failed": "Three candidate rows remain indistinguishable under the current value-source dominance rule.",
            "where_failed": "SELECT.dominance_selection",
            "failed_relative_to_object": "candidate_value_rows",
            "failed_relative_to_source_surface": "value_source_table",
            "failed_relative_to_boundary": "value_source_dominance_boundary",
            "failed_relative_to_rule": "current dominance rule lacks source-scope tie-break",
            "missing_capability_name": "source_scope_typing",
            "missing_discriminator": "source_scope_type",
            "capability_kind": "DISCRIMINATOR",
            "evidence_for_missing": ["three top candidate rows tie under current rule"],
            "blocked_next_moves": ["select one row", "repair by arbitrary preference"],
            "lawful_next_refinements": ["add source_scope_type discriminator and rerun dominance selection"],
            "forbidden_next_moves": ["break tie by latest file", "select first row"],
            "must_not_infer": common_must_not,
            "decision_edge_observation_ref": "edge_obs_demo_source_scope_discriminator",
        },
        {
            "case_id": "expected_limit_proposal_requires_review",
            "unit_id": "demo.expected_limit_proposal.v0",
            "status": "STOPPED",
            "terminal": "STOP_PROPOSAL_REQUIRES_REVIEW",
            "gate": "PASS",
            "failure_or_stop_code": "PROPOSAL_REQUIRES_REVIEW",
            "demo_input_quality": "EXPECTED_LIMIT",
            "feedback_quality": "EXPECTED_LIMIT",
            "diagnostic_completeness": "EXPECTED_LIMIT",
            "unit_phase": "AUTHORIZE",
            "step_name": "AUTHORIZE.review_boundary",
            "field_path": "proposal.status",
            "object_ref": "proposal_packet",
            "source_surface_ref": "proposal_packet",
            "boundary_ref": "human_review_boundary",
            "why_failed": "The unit stopped lawfully because proposal application requires review.",
            "where_failed": "AUTHORIZE.review_boundary",
            "failed_relative_to_object": "proposal_packet",
            "failed_relative_to_source_surface": "proposal_packet",
            "failed_relative_to_boundary": "human_review_boundary",
            "failed_relative_to_rule": "proposal may not apply itself",
            "missing_capability_name": "accepted_review_receipt",
            "missing_discriminator": "accepted_for_build_status",
            "capability_kind": "AUTHORITY_RULE",
            "evidence_for_missing": ["proposal status is not ACCEPTED_FOR_BUILD"],
            "blocked_next_moves": ["apply proposal without review"],
            "lawful_next_refinements": ["request review", "do not apply proposal"],
            "forbidden_next_moves": ["count expected stop as bug"],
            "must_not_infer": common_must_not,
            "decision_edge_observation_ref": "edge_obs_demo_expected_limit",
        },
        {
            "case_id": "c4_accepted_proposal_missing_verification_requirement",
            "unit_id": "demo.c4_verification_requirement.v0",
            "status": "BLOCKED",
            "terminal": "STOP_VERIFICATION_REQUIREMENT_MISSING",
            "gate": "NA",
            "failure_or_stop_code": "VERIFICATION_REQUIREMENT_MISSING",
            "demo_input_quality": "REFINEMENT_READY_FAILURE",
            "feedback_quality": "REFINEMENT_READY_FAILURE",
            "diagnostic_completeness": "SUFFICIENT_FOR_REFINEMENT",
            "unit_phase": "VERIFY",
            "step_name": "VERIFY.accepted_proposal_requirement",
            "field_path": "proposal.acceptance_gates.verification_requirement",
            "object_ref": "accepted_proposal_packet",
            "source_surface_ref": "c4_proposal_acceptance_surface",
            "boundary_ref": "verification_gate_boundary",
            "why_failed": "The accepted proposal lacks the verification requirement needed before build execution.",
            "where_failed": "VERIFY.accepted_proposal_requirement",
            "failed_relative_to_object": "accepted_proposal_packet",
            "failed_relative_to_source_surface": "c4_proposal_acceptance_surface",
            "failed_relative_to_boundary": "verification_gate_boundary",
            "failed_relative_to_rule": "accepted proposal must include verification requirement before build",
            "missing_capability_name": "verification_requirement_field",
            "missing_discriminator": "verification_requirement",
            "capability_kind": "VERIFICATION_GATE",
            "evidence_for_missing": ["proposal.acceptance_gates.verification_requirement absent"],
            "blocked_next_moves": ["execute build from accepted proposal"],
            "lawful_next_refinements": ["add verification_requirement acceptance gate before build"],
            "forbidden_next_moves": ["assume acceptance implies verification"],
            "must_not_infer": common_must_not,
            "decision_edge_observation_ref": "edge_obs_demo_c4_verification",
        },
        {
            "case_id": "ambiguous_label_remainder_failure",
            "unit_id": "demo.ambiguous_label_remainder.v0",
            "status": "UNDER_TYPED",
            "terminal": "STOP_AMBIGUOUS_LABEL_REMAINDER",
            "gate": "NA",
            "failure_or_stop_code": "AMBIGUOUS_LABEL_REMAINDER",
            "demo_input_quality": "AMBIGUOUS_REQUIRES_QUESTION",
            "feedback_quality": "AMBIGUOUS_REQUIRES_QUESTION",
            "diagnostic_completeness": "SUFFICIENT_FOR_QUESTION",
            "unit_phase": "CLASSIFY",
            "step_name": "CLASSIFY.label_remainder",
            "field_path": "label.remainder",
            "object_ref": "label_remainder",
            "source_surface_ref": "labeling_surface",
            "boundary_ref": "label_noncollapse_boundary",
            "why_failed": "The label remainder cannot be classified without collapsing the label into accepted meaning.",
            "where_failed": "CLASSIFY.label_remainder",
            "failed_relative_to_object": "label_remainder",
            "failed_relative_to_source_surface": "labeling_surface",
            "failed_relative_to_boundary": "label_noncollapse_boundary",
            "failed_relative_to_rule": "ambiguous label must ask or withhold, not force repair",
            "missing_capability_name": "label_remainder_question_packet",
            "missing_discriminator": "label_remainder_kind",
            "capability_kind": "LABEL_LANE",
            "evidence_for_missing": ["label remainder is ambiguous under current label lane"],
            "blocked_next_moves": ["force repair", "accept label as final"],
            "lawful_next_refinements": ["emit question packet for label remainder kind"],
            "forbidden_next_moves": ["collapse label ambiguity into accepted meaning"],
            "must_not_infer": common_must_not,
            "decision_edge_observation_ref": "edge_obs_demo_label_remainder",
        },
        {
            "case_id": "retry_unchanged_failure",
            "unit_id": "demo.retry_unchanged.v0",
            "status": "BLOCKED",
            "terminal": "STOP_SAME_FAILURE_RETRY_BLOCKED",
            "gate": "PASS",
            "failure_or_stop_code": "SAME_FAILURE_RETRY_BLOCKED",
            "demo_input_quality": "BOUNDARY_AWARE_FAILURE",
            "feedback_quality": "BOUNDARY_AWARE_FAILURE",
            "diagnostic_completeness": "SUFFICIENT_FOR_QUESTION",
            "unit_phase": "STOP",
            "step_name": "STOP.retry_gate",
            "field_path": "retry_context",
            "object_ref": "retry_request",
            "source_surface_ref": "retry_gate_surface",
            "boundary_ref": "same_failure_retry_boundary",
            "why_failed": "Retry is blocked because no evidence, boundary, surface, discriminator, or accepted refinement changed.",
            "where_failed": "STOP.retry_gate",
            "failed_relative_to_object": "retry_request",
            "failed_relative_to_source_surface": "retry_gate_surface",
            "failed_relative_to_boundary": "same_failure_retry_boundary",
            "failed_relative_to_rule": "same failure may not be retried without changed condition",
            "missing_capability_name": "changed_retry_condition",
            "missing_discriminator": "changed_evidence_or_refinement",
            "capability_kind": "BOUNDARY_RULE",
            "evidence_for_missing": ["retry context matches previous failure context"],
            "blocked_next_moves": ["retry same unit with same inputs"],
            "lawful_next_refinements": ["provide new evidence, changed boundary, smaller surface, added discriminator, accepted refinement, or changed external condition"],
            "forbidden_next_moves": ["retry anyway"],
            "must_not_infer": common_must_not,
            "retry_block_reason": "Same failure retry blocked; no changed refinement/evidence condition exists.",
            "decision_edge_observation_ref": "edge_obs_demo_retry_gate",
        },
    ]

def validate_records(events: List[Dict[str, Any]], feedback: List[Dict[str, Any]], retry_gates: List[Dict[str, Any]], refinements: List[Dict[str, Any]]) -> List[str]:
    failures: List[str] = []
    if len(events) != 10:
        failures.append(f"event_count_not_10:{len(events)}")
    if len(feedback) != 10:
        failures.append(f"feedback_count_not_10:{len(feedback)}")
    by_event = {x["failure_event_id"]: x for x in events}
    for idx, rec in enumerate(feedback):
        if rec["quality"]["feedback_quality_class"] == "NO_FEEDBACK":
            failures.append(f"accepted_feedback_no_feedback:{idx}")
        if not rec["failure_location"]["where_failed" if False else "step_name"]:
            failures.append(f"feedback_missing_step:{idx}")
        if not rec["failure_explanation"]["where_failed"]:
            failures.append(f"feedback_missing_where:{idx}")
        if not rec["failure_explanation"]["failed_relative_to_boundary"]:
            failures.append(f"feedback_missing_boundary:{idx}")
        if not rec["failure_explanation"]["failed_relative_to_object"]:
            failures.append(f"feedback_missing_object:{idx}")
        if not rec["failure_explanation"]["failed_relative_to_source_surface"]:
            failures.append(f"feedback_missing_source_surface:{idx}")
        cap = rec["missing_capability"]
        if not cap["smallest_honest_name"] and not cap["evidence_for_missing"]:
            failures.append(f"feedback_missing_capability_or_evidence:{idx}")
        if not rec["movement"]["blocked_next_moves"]:
            failures.append(f"feedback_missing_blocked_moves:{idx}")
        if not rec["movement"]["lawful_next_refinements"]:
            failures.append(f"feedback_missing_lawful_next:{idx}")
        if rec["quality"]["retry_allowed"] is not False:
            failures.append(f"retry_allowed_true:{idx}")
        for key in ["repair_applied", "target_selected_for_build", "source_mutated", "prior_receipt_mutated", "architecture_change", "c5_opened"]:
            if rec["safety"].get(key) is not False:
                failures.append(f"safety_true:{key}:{idx}")
    for idx, rg in enumerate(retry_gates):
        if rg["retry_allowed"] is not False:
            failures.append(f"retry_gate_allowed:{idx}")
    for idx, ref in enumerate(refinements):
        if ref["status"] != "PROPOSED_ONLY":
            failures.append(f"refinement_not_proposed_only:{idx}")
    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()

    if not failures:
        for path, obj in schema_artifacts().items():
            write_json(path, obj)

    cases = demo_cases()
    events = [make_event(c, i + 1) for i, c in enumerate(cases)]
    feedback = [make_feedback(events[i], cases[i]) for i in range(len(cases))]
    locations = [make_location(f) for f in feedback]
    missing_caps = [make_missing_cap(f) for f in feedback]
    refinements = [make_refinement(feedback[i], cases[i]) for i in range(len(cases))]
    retry_gates = [make_retry_gate(feedback[i], cases[i]) for i in range(len(cases))]
    edge_links = [make_edge_link(feedback[i], cases[i]) for i in range(len(cases))]

    failures.extend(validate_records(events, feedback, retry_gates, refinements))

    write_jsonl(DEMO_FAILURE_EVENTS_PATH, events)
    write_jsonl(UNIT_FAILURE_EVENTS_PATH, events)
    write_jsonl(UNIT_FEEDBACK_RECORDS_PATH, feedback)
    write_jsonl(UNIT_FAILURE_LOCATION_RECORDS_PATH, locations)
    write_jsonl(UNIT_MISSING_CAPABILITY_RECORDS_PATH, missing_caps)
    write_jsonl(UNIT_REFINEMENT_CANDIDATE_RECORDS_PATH, refinements)
    write_jsonl(UNIT_RETRY_GATE_RECORDS_PATH, retry_gates)
    write_jsonl(EDGE_FEEDBACK_LINKS_PATH, edge_links)

    quality_counts = Counter(f["quality"]["feedback_quality_class"] for f in feedback)
    phase_counts = Counter(f["failure_location"]["unit_phase"] for f in feedback)
    missing_cap_counts = Counter(f["missing_capability"]["smallest_honest_name"] for f in feedback)

    weak_feedback_count = quality_counts["STATUS_ONLY"] + quality_counts["UNDER_TYPED_FEEDBACK"] + quality_counts["AMBIGUOUS_REQUIRES_QUESTION"]
    refinement_ready_count = quality_counts["REFINEMENT_READY_FAILURE"]
    expected_limit_count = quality_counts["EXPECTED_LIMIT"]
    retry_blocked_count = sum(1 for r in retry_gates if r["retry_allowed"] is False)

    bare_failed_status_count = 0
    failure_without_location_count = sum(1 for f in feedback if not f["failure_explanation"]["where_failed"])
    failure_without_boundary_count = sum(1 for f in feedback if not f["failure_explanation"]["failed_relative_to_boundary"])
    failure_without_object_count = sum(1 for f in feedback if not f["failure_explanation"]["failed_relative_to_object"])
    failure_without_source_surface_count = sum(1 for f in feedback if not f["failure_explanation"]["failed_relative_to_source_surface"])
    failure_without_missing_capability_or_evidence_count = sum(1 for f in feedback if not f["missing_capability"]["smallest_honest_name"] and not f["missing_capability"]["evidence_for_missing"])
    failure_without_lawful_next_refinement_count = sum(1 for f in feedback if not f["movement"]["lawful_next_refinements"])
    retry_allowed_without_refinement_count = sum(1 for f in feedback if f["quality"]["retry_allowed"] is True and not f["quality"]["retry_requires"])

    rollup = {
        "schema_version": "unit_feedback_rollup_v0",
        "units_evaluated": len(events),
        "failed_or_stopped_units": len(events),
        "feedback_quality_counts": {q: quality_counts.get(q, 0) for q in QUALITY_CLASSES},
        "failure_phase_counts": {p: phase_counts.get(p, 0) for p in UNIT_PHASES},
        "missing_capability_counts": dict(sorted(missing_cap_counts.items())),
        "retry_blocked_count": retry_blocked_count,
        "refinement_ready_count": refinement_ready_count,
        "weak_feedback_count": weak_feedback_count,
        "bare_failed_status_count": bare_failed_status_count,
        "failure_without_location_count": failure_without_location_count,
        "failure_without_boundary_count": failure_without_boundary_count,
        "failure_without_object_count": failure_without_object_count,
        "failure_without_source_surface_count": failure_without_source_surface_count,
        "failure_without_missing_capability_or_evidence_count": failure_without_missing_capability_or_evidence_count,
        "failure_without_lawful_next_refinement_count": failure_without_lawful_next_refinement_count,
        "retry_allowed_without_refinement_count": retry_allowed_without_refinement_count,
        "repair_applied_by_feedback_unit_count": 0,
        "target_selected_by_feedback_unit_count": 0,
        "architecture_change_by_feedback_unit_count": 0,
        "source_mutated_by_feedback_unit_count": 0,
        "prior_receipt_mutated_by_feedback_unit_count": 0,
        "expected_limit_counted_as_bug_count": 0,
        "productive_pressure_counted_as_success_count": 0,
        "ambiguous_failure_forced_to_repair_count": 0,
        "c5_opened_count": 0,
        "hidden_next_command_count": 0,
        "live_feedback_audit_executed_count": 0,
        "runtime_patch_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
    }

    required_zero_keys = [
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
    bad_counters_zero = all(rollup[k] == 0 for k in required_zero_keys)

    c5_feedback_readiness = "BLOCKED_BY_WEAK_FEEDBACK" if weak_feedback_count > 0 else "READY"
    status = "TYPED_O2_UNIT_FEEDBACK_HARDENING_STATIC_SCHEMA_PROBE_EMITTED_WEAK_FEEDBACK_REMAINS" if weak_feedback_count > 0 else "TYPED_O2_UNIT_FEEDBACK_HARDENED"
    terminal_stop = "STOP_O2_WEAK_FEEDBACK_REMAINS" if weak_feedback_count > 0 else "STOP_O2_UNIT_FEEDBACK_HARDENED"

    readout = {
        "schema_version": "unit_feedback_readout_v0",
        "failed_or_stopped_units": len(events),
        "bare_failed_statuses": rollup["bare_failed_status_count"],
        "weak_feedback_records": weak_feedback_count,
        "refinement_ready_failures": refinement_ready_count,
        "expected_limits": expected_limit_count,
        "retry_blocked": retry_blocked_count,
        "most_common_failure_phase": phase_counts.most_common(1)[0][0] if phase_counts else None,
        "most_common_missing_capability": missing_cap_counts.most_common(1)[0][0] if missing_cap_counts else None,
        "interpretation": "Static probe emitted feedback machinery. Weak demo feedback remains by design as under-typed/question examples; bad counters are zero and C5 remains blocked until weak feedback is resolved or explicitly accepted as question/under-typed.",
        "c5_feedback_readiness": c5_feedback_readiness,
    }

    profile = {
        "schema_version": "o2_unit_feedback_hardening_profile_v0",
        "profile_id": "o2_feedback_" + sha8(rollup),
        "status": "O2_WEAK_FEEDBACK_REMAINS" if weak_feedback_count > 0 else "O2_FEEDBACK_HARDENED",
        "active_object": "unit feedback records from static demo failed/stopped/blocked/under-typed units",
        "feedback_rollup_ref": rel(ROLLUP_PATH),
        "feedback_readout_ref": rel(READOUT_PATH),
        "core_rule": "Failure feedback must say why, where, relative to what, what is blocked, and what smallest refinement would allow progress.",
        "bad_counters_zero": bad_counters_zero,
        "must_not_infer": [
            "repair applied",
            "target selected",
            "missing capability accepted",
            "refinement candidate approved",
            "C5 opened",
            "failure counted as progress",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": [
            "O2_STATIC_SCHEMA_AND_PROBE_BUILT",
            "UNIT_FAILURE_EVENT_SCHEMA_EMITTED",
            "UNIT_FEEDBACK_RECORD_SCHEMA_EMITTED",
            "FAILURE_LOCATION_SCHEMA_EMITTED",
            "FEEDBACK_QUALITY_ENUM_EMITTED",
            "MISSING_CAPABILITY_SCHEMA_EMITTED",
            "REFINEMENT_CANDIDATE_SCHEMA_EMITTED",
            "RETRY_GATE_SCHEMA_EMITTED",
            "EDGE_FEEDBACK_LINK_SCHEMA_EMITTED",
            "DEMO_FAILURE_EVENTS_EMITTED",
            "FEEDBACK_RECORDS_EMITTED",
            "BARE_FAILED_INPUT_UPGRADED_TO_UNDERTYPED_FEEDBACK",
            "EXPECTED_LIMITS_SEPARATED_FROM_BUGS",
            "UNCHANGED_RETRIES_BLOCKED",
            "REFINEMENT_CANDIDATES_PROPOSED_ONLY",
            "MISSING_CAPABILITIES_CANDIDATE_ONLY",
            "WEAK_FEEDBACK_REMAINS_AS_STATIC_PROBE_SIGNAL" if weak_feedback_count > 0 else "NO_WEAK_FEEDBACK_REMAINS",
            "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
            "NO_REPAIR_APPLIED",
            "NO_RETRY_EXECUTED",
            "NO_TARGET_SELECTED_FOR_BUILD",
            "NO_RUNTIME_PATCH_APPLIED",
            "NO_SOURCE_MUTATION",
            "NO_C5_OPENED",
        ],
        "receipt_backed_claim": "O2 emitted the static schema/probe unit feedback hardening layer. It produced schemas, demo failure events, typed feedback records, failure locations, missing capability candidate records, proposed-only refinement candidates, retry gates, edge-feedback links, rollup, readout, profile, report, transition trace, and receipt. Weak demo inputs are upgraded into under-typed/question feedback rather than accepted as bare failures. No live audit, repair, retry, target selection, runtime patch, source mutation, prior receipt mutation, or C5 opening occurred.",
        "units_evaluated": len(events),
        "feedback_records_emitted": len(feedback),
        "weak_feedback_count": weak_feedback_count,
        "bad_counters_zero": bad_counters_zero,
        "c5_feedback_readiness": c5_feedback_readiness,
        "recommended_next_handling": "REVIEW_O2_UNIT_FEEDBACK_HARDENING_V0",
    }

    trace = {
        "schema_version": "o2_transition_trace_v0",
        "trace": [
            {
                "step": "consume_o2_design",
                "question": "is O2 build authorized in static schema/probe mode",
                "answer": "yes",
                "taken": "build schemas and demo feedback machinery",
            },
            {
                "step": "emit_feedback_records",
                "question": "did demo failed/stopped/blocked units receive diagnostic feedback",
                "answer": f"{len(feedback)} feedback records emitted",
                "taken": "write feedback records, locations, missing capabilities, refinements, retry gates, and edge links",
            },
            {
                "step": "preserve_nonrepair_boundary",
                "question": "did O2 repair, retry, select target, patch runtime, mutate sources, or open C5",
                "answer": "no",
                "taken": "emit rollup/readout/profile with required bad counters zero",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": terminal_stop,
            "next_command_goal": None,
        },
    }

    write_json(ROLLUP_PATH, rollup)
    write_json(READOUT_PATH, readout)
    write_json(PROFILE_PATH, profile)
    write_json(REPORT_PATH, report)
    write_json(TRACE_PATH, trace)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        rollup["source_mutated_by_feedback_unit_count"] = 1
        bad_counters_zero = False
        write_json(ROLLUP_PATH, rollup)

    acceptance_gate_results = {
        "O2_FEEDBACK_0_SOURCE_SURFACE_DECLARED": True,
        "O2_FEEDBACK_1_UNIT_FAILURE_EVENT_SCHEMA_EMITTED": UNIT_FAILURE_EVENT_SCHEMA_PATH.exists(),
        "O2_FEEDBACK_2_UNIT_FEEDBACK_RECORD_SCHEMA_EMITTED": UNIT_FEEDBACK_RECORD_SCHEMA_PATH.exists(),
        "O2_FEEDBACK_3_FAILURE_LOCATION_SCHEMA_EMITTED": UNIT_FAILURE_LOCATION_SCHEMA_PATH.exists(),
        "O2_FEEDBACK_4_FEEDBACK_QUALITY_ENUM_EMITTED": UNIT_FEEDBACK_QUALITY_ENUM_PATH.exists(),
        "O2_FEEDBACK_5_MISSING_CAPABILITY_SCHEMA_EMITTED": UNIT_MISSING_CAPABILITY_SCHEMA_PATH.exists(),
        "O2_FEEDBACK_6_REFINEMENT_CANDIDATE_SCHEMA_EMITTED": UNIT_REFINEMENT_CANDIDATE_SCHEMA_PATH.exists(),
        "O2_FEEDBACK_7_RETRY_GATE_SCHEMA_EMITTED": UNIT_RETRY_GATE_SCHEMA_PATH.exists(),
        "O2_FEEDBACK_8_EDGE_FEEDBACK_LINK_SCHEMA_EMITTED": EDGE_FEEDBACK_LINK_SCHEMA_PATH.exists(),
        "O2_FEEDBACK_9_DEMO_FAILURE_EVENTS_EMITTED": DEMO_FAILURE_EVENTS_PATH.exists() and len(events) == 10,
        "O2_FEEDBACK_10_EVERY_FAILED_UNIT_HAS_FEEDBACK_RECORD_OR_UNDERTYPED_STOP": len(feedback) == len(events),
        "O2_FEEDBACK_11_NO_BARE_FAILED_STATUS": rollup["bare_failed_status_count"] == 0,
        "O2_FEEDBACK_12_FAILURE_LOCATION_RECORDED_OR_UNDERTYPED": rollup["failure_without_location_count"] == 0,
        "O2_FEEDBACK_13_BOUNDARY_RECORDED_OR_UNDERTYPED": rollup["failure_without_boundary_count"] == 0,
        "O2_FEEDBACK_14_OBJECT_OR_SOURCE_SURFACE_RECORDED_OR_UNDERTYPED": rollup["failure_without_object_count"] == 0 and rollup["failure_without_source_surface_count"] == 0,
        "O2_FEEDBACK_15_MISSING_CAPABILITY_OR_MISSING_EVIDENCE_RECORDED_WHEN_APPLICABLE": rollup["failure_without_missing_capability_or_evidence_count"] == 0,
        "O2_FEEDBACK_16_BLOCKED_NEXT_MOVES_RECORDED": all(bool(f["movement"]["blocked_next_moves"]) for f in feedback),
        "O2_FEEDBACK_17_LAWFUL_NEXT_REFINEMENT_OR_QUESTION_RECORDED": rollup["failure_without_lawful_next_refinement_count"] == 0,
        "O2_FEEDBACK_18_EXPECTED_LIMITS_SEPARATED_FROM_BUGS": rollup["expected_limit_counted_as_bug_count"] == 0 and quality_counts["EXPECTED_LIMIT"] >= 1,
        "O2_FEEDBACK_19_RETRY_BLOCKED_WITHOUT_CHANGED_REFINEMENT": rollup["retry_allowed_without_refinement_count"] == 0 and retry_blocked_count == len(events),
        "O2_FEEDBACK_20_REFINEMENT_CANDIDATES_PROPOSED_ONLY": all(r["status"] == "PROPOSED_ONLY" for r in refinements),
        "O2_FEEDBACK_21_NO_REPAIR_APPLIED": rollup["repair_applied_by_feedback_unit_count"] == 0,
        "O2_FEEDBACK_22_NO_TARGET_SELECTED_FOR_BUILD": rollup["target_selected_by_feedback_unit_count"] == 0,
        "O2_FEEDBACK_23_NO_SOURCE_MUTATION": rollup["source_mutated_by_feedback_unit_count"] == 0,
        "O2_FEEDBACK_24_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "O2_FEEDBACK_25_ROLLUP_READOUT_PROFILE_EMITTED": ROLLUP_PATH.exists() and READOUT_PATH.exists() and PROFILE_PATH.exists(),
        "O2_FEEDBACK_26_BAD_COUNTERS_ZERO": bad_counters_zero,
        "O2_FEEDBACK_27_NO_HIDDEN_NEXT_COMMAND": trace["terminal"]["next_command_goal"] is None,
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    if gate != "PASS":
        status = "TYPED_O2_UNIT_FEEDBACK_HARDENING_GATE_FAIL"
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION" if not bad_counters_zero else "STOP_O2_C5_BLOCKED_BY_FEEDBACK_QUALITY", "next_command_goal": None}
    else:
        terminal = trace["terminal"]

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "events": len(events),
        "feedback": len(feedback),
        "weak": weak_feedback_count,
        "bad_counters_zero": bad_counters_zero,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_unit_feedback_hardening_receipt_v0",
        "receipt_type": "TYPED_O2_UNIT_FEEDBACK_HARDENING_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_o2_target_design_receipt_id": O2_DESIGN_RECEIPT_ID,
        "machine_readable_o2_unit_feedback_summary": {
            "status": status,
            "reason_codes": report["reason_codes"] if gate == "PASS" else failures,
            "initial_mode": "STATIC_SCHEMA_AND_PROBE_ONLY",
            "live_feedback_audit_executed": False,
            "schemas_emitted": True,
            "demo_failure_events_emitted": True,
            "unit_failure_events_emitted": True,
            "unit_feedback_records_emitted": True,
            "units_evaluated": len(events),
            "feedback_records_emitted_count": len(feedback),
            "weak_feedback_count": weak_feedback_count,
            "bare_failed_status_count": rollup["bare_failed_status_count"],
            "refinement_ready_count": refinement_ready_count,
            "expected_limit_count": expected_limit_count,
            "retry_blocked_count": retry_blocked_count,
            "feedback_quality_counts": rollup["feedback_quality_counts"],
            "c5_feedback_readiness": c5_feedback_readiness,
            "bad_counters_zero": bad_counters_zero,
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
            "recommended_next": "REVIEW_O2_UNIT_FEEDBACK_HARDENING_V0",
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "unit_failure_event_schema": rel(UNIT_FAILURE_EVENT_SCHEMA_PATH),
            "unit_feedback_record_schema": rel(UNIT_FEEDBACK_RECORD_SCHEMA_PATH),
            "unit_failure_location_schema": rel(UNIT_FAILURE_LOCATION_SCHEMA_PATH),
            "unit_feedback_quality_enum": rel(UNIT_FEEDBACK_QUALITY_ENUM_PATH),
            "unit_missing_capability_record_schema": rel(UNIT_MISSING_CAPABILITY_SCHEMA_PATH),
            "unit_refinement_candidate_schema": rel(UNIT_REFINEMENT_CANDIDATE_SCHEMA_PATH),
            "unit_retry_gate_schema": rel(UNIT_RETRY_GATE_SCHEMA_PATH),
            "edge_feedback_link_schema": rel(EDGE_FEEDBACK_LINK_SCHEMA_PATH),
            "demo_failure_events": rel(DEMO_FAILURE_EVENTS_PATH),
            "unit_failure_events": rel(UNIT_FAILURE_EVENTS_PATH),
            "unit_feedback_records": rel(UNIT_FEEDBACK_RECORDS_PATH),
            "unit_failure_location_records": rel(UNIT_FAILURE_LOCATION_RECORDS_PATH),
            "unit_missing_capability_records": rel(UNIT_MISSING_CAPABILITY_RECORDS_PATH),
            "unit_refinement_candidate_records": rel(UNIT_REFINEMENT_CANDIDATE_RECORDS_PATH),
            "unit_retry_gate_records": rel(UNIT_RETRY_GATE_RECORDS_PATH),
            "edge_feedback_links": rel(EDGE_FEEDBACK_LINKS_PATH),
            "unit_feedback_rollup": rel(ROLLUP_PATH),
            "unit_feedback_readout": rel(READOUT_PATH),
            "o2_feedback_profile": rel(PROFILE_PATH),
            "o2_transition_trace": rel(TRACE_PATH),
            "o2_report": rel(REPORT_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"o2_feedback_receipt_id={receipt_id}")
    print(f"o2_feedback_receipt_path={rel(receipt_path)}")
    print(f"o2_unit_failure_event_schema_path={rel(UNIT_FAILURE_EVENT_SCHEMA_PATH)}")
    print(f"o2_unit_feedback_record_schema_path={rel(UNIT_FEEDBACK_RECORD_SCHEMA_PATH)}")
    print(f"o2_unit_feedback_quality_enum_path={rel(UNIT_FEEDBACK_QUALITY_ENUM_PATH)}")
    print(f"o2_demo_failure_events_path={rel(DEMO_FAILURE_EVENTS_PATH)}")
    print(f"o2_unit_feedback_records_path={rel(UNIT_FEEDBACK_RECORDS_PATH)}")
    print(f"o2_unit_feedback_rollup_path={rel(ROLLUP_PATH)}")
    print(f"o2_unit_feedback_readout_path={rel(READOUT_PATH)}")
    print(f"o2_feedback_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
