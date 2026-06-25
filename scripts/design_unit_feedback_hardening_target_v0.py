#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET_V0"
TARGET_UNIT_ID = "observation.unit_feedback_hardening_target_design.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / TARGET_DESIGN"
MODE = "DESIGN_ONLY / STATIC_SCHEMA_AND_PROBE_TARGET / NO_FEEDBACK_RECORDS_EMITTED"
BUILD_MODE = "O2_TARGET_DESIGN_ONLY"

O1_CLOSE_RECEIPT_ID = "e9d2dcf5"
O1_CLOSE_RECEIPT_PATH = ROOT / "data/o1_decision_edge_observability_surface_closure_v0_receipts/e9d2dcf5.json"
O1_REVIEWED_REFERENCE_PATH = ROOT / "data/o1_decision_edge_observability_surface_closure_v0/o1_decision_edge_observability_surface_reviewed_reference_v0.json"
O1_REFERENCE_FREEZE_PATH = ROOT / "data/o1_decision_edge_observability_surface_closure_v0/o1_decision_edge_observability_surface_reference_freeze_v0.json"
O1_RECEIPT_CHAIN_PATH = ROOT / "data/o1_decision_edge_observability_surface_closure_v0/o1_decision_edge_observability_surface_receipt_chain_v0.json"
O1_BOUNDARY_LOCK_PATH = ROOT / "data/o1_decision_edge_observability_surface_closure_v0/o1_decision_edge_observability_surface_boundary_lock_v0.json"
O1_O2_READY_SURFACE_PATH = ROOT / "data/o1_decision_edge_observability_surface_closure_v0/o1_post_closure_o2_design_ready_surface_v0.json"
O1_CLOSURE_CLASSIFICATION_PATH = ROOT / "data/o1_decision_edge_observability_surface_closure_v0/o1_surface_closure_classification_v0.json"
O1_CLOSURE_AUTHORITY_PATH = ROOT / "data/o1_decision_edge_observability_surface_closure_v0/o1_surface_closure_authority_boundary_v0.json"
O1_CLOSURE_ROLLUP_PATH = ROOT / "data/o1_decision_edge_observability_surface_closure_v0/o1_surface_closure_rollup_v0.json"
O1_CLOSURE_PROFILE_PATH = ROOT / "data/o1_decision_edge_observability_surface_closure_v0/o1_surface_closure_profile_v0.json"
O1_CLOSURE_REPORT_PATH = ROOT / "data/o1_decision_edge_observability_surface_closure_v0/o1_surface_closure_report.json"
O1_SURFACE_RECORDS_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/decision_edge_observation_records_v0.jsonl"
O1_SURFACE_ROLLUP_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/decision_edge_observation_rollup_v0.json"
O1_SURFACE_READOUT_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/decision_edge_observation_readout_v0.json"

REQUIRED_SOURCE_FILES = [
    O1_CLOSE_RECEIPT_PATH,
    O1_REVIEWED_REFERENCE_PATH,
    O1_REFERENCE_FREEZE_PATH,
    O1_RECEIPT_CHAIN_PATH,
    O1_BOUNDARY_LOCK_PATH,
    O1_O2_READY_SURFACE_PATH,
    O1_CLOSURE_CLASSIFICATION_PATH,
    O1_CLOSURE_AUTHORITY_PATH,
    O1_CLOSURE_ROLLUP_PATH,
    O1_CLOSURE_PROFILE_PATH,
    O1_CLOSURE_REPORT_PATH,
    O1_SURFACE_RECORDS_PATH,
    O1_SURFACE_ROLLUP_PATH,
    O1_SURFACE_READOUT_PATH,
]

OUT_DIR = ROOT / "data/o2_unit_feedback_hardening_target_design_v0"
RECEIPT_DIR = ROOT / "data/o2_unit_feedback_hardening_target_design_v0_receipts"

TARGET_DESIGN_PATH = OUT_DIR / "o2_unit_feedback_hardening_target_design_v0.json"
OBJECTIVE_CONTRACT_PATH = OUT_DIR / "o2_objective_contract_v0.json"
MODE_CONTRACT_PATH = OUT_DIR / "o2_initial_mode_contract_v0.json"
SOURCE_SCOPE_CONTRACT_PATH = OUT_DIR / "o2_source_scope_contract_v0.json"
FEEDBACK_AXES_CONTRACT_PATH = OUT_DIR / "o2_feedback_axes_contract_v0.json"
QUALITY_ENUM_CONTRACT_PATH = OUT_DIR / "o2_feedback_quality_enum_contract_v0.json"
SCHEMA_CONTRACT_PATH = OUT_DIR / "o2_required_schema_contract_v0.json"
DEMO_PROBE_CONTRACT_PATH = OUT_DIR / "o2_demo_probe_boundary_contract_v0.json"
NEGATIVE_CONTROL_CONTRACT_PATH = OUT_DIR / "o2_negative_control_contract_v0.json"
RETRY_GATE_CONTRACT_PATH = OUT_DIR / "o2_retry_gate_contract_v0.json"
NONREPAIR_BOUNDARY_PATH = OUT_DIR / "o2_nonrepair_nonauthority_boundary_v0.json"
ACCEPTANCE_GATE_CONTRACT_PATH = OUT_DIR / "o2_acceptance_gate_contract_v0.json"
TERMINAL_CONTRACT_PATH = OUT_DIR / "o2_terminal_contract_v0.json"
BUILD_UNIT_AUTHORIZATION_PATH = OUT_DIR / "o2_build_unit_authorization_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "o2_target_design_downstream_decision_table_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_target_design_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_target_design_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_target_design_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_target_design_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_target_design_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "o2_target_design_transition_trace.json"

EXPECTED_O1_STATUS = "TYPED_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_CLOSED_AS_REVIEWED_REFERENCE_O2_DESIGN_READY"
EXPECTED_O1_STOP = "STOP_TYPED_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_CLOSED_AS_REVIEWED_REFERENCE_O2_DESIGN_READY"
EXPECTED_O1_NEXT = "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET_V0"

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

FEEDBACK_AXES = [
    "why_failed",
    "where_failed",
    "failed_relative_to_object",
    "failed_relative_to_source_surface",
    "failed_relative_to_boundary",
    "failed_relative_to_rule",
    "failed_relative_to_missing_capability",
    "missing_discriminator",
    "blocked_next_moves",
    "lawful_next_refinements",
    "forbidden_next_moves",
    "evidence_refs",
    "must_not_infer",
]

UNIT_PHASE_ENUM = [
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

CAPABILITY_KIND_ENUM = [
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

REFINEMENT_TYPE_ENUM = [
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

REQUIRED_OUTPUT_ARTIFACTS = [
    "data/o2_unit_feedback_hardening_v0/unit_failure_event_schema_v0.json",
    "data/o2_unit_feedback_hardening_v0/unit_feedback_record_schema_v0.json",
    "data/o2_unit_feedback_hardening_v0/unit_failure_location_schema_v0.json",
    "data/o2_unit_feedback_hardening_v0/unit_feedback_quality_enum_v0.json",
    "data/o2_unit_feedback_hardening_v0/unit_missing_capability_record_schema_v0.json",
    "data/o2_unit_feedback_hardening_v0/unit_refinement_candidate_schema_v0.json",
    "data/o2_unit_feedback_hardening_v0/unit_retry_gate_schema_v0.json",
    "data/o2_unit_feedback_hardening_v0/edge_feedback_link_schema_v0.json",
    "data/o2_unit_feedback_hardening_v0/o2_demo_failure_events_v0.jsonl",
    "data/o2_unit_feedback_hardening_v0/unit_failure_events_v0.jsonl",
    "data/o2_unit_feedback_hardening_v0/unit_feedback_records_v0.jsonl",
    "data/o2_unit_feedback_hardening_v0/unit_failure_location_records_v0.jsonl",
    "data/o2_unit_feedback_hardening_v0/unit_missing_capability_records_v0.jsonl",
    "data/o2_unit_feedback_hardening_v0/unit_refinement_candidate_records_v0.jsonl",
    "data/o2_unit_feedback_hardening_v0/unit_retry_gate_records_v0.jsonl",
    "data/o2_unit_feedback_hardening_v0/edge_feedback_links_v0.jsonl",
    "data/o2_unit_feedback_hardening_v0/unit_feedback_rollup_v0.json",
    "data/o2_unit_feedback_hardening_v0/unit_feedback_readout_v0.json",
    "data/o2_unit_feedback_hardening_v0/o2_feedback_profile_v0.json",
    "data/o2_unit_feedback_hardening_v0/o2_transition_trace.json",
    "data/o2_unit_feedback_hardening_v0/o2_report.json",
    "data/o2_unit_feedback_hardening_v0_receipts/<receipt_id>.json",
]

ACCEPTANCE_GATES = [
    "O2_FEEDBACK_0_SOURCE_SURFACE_DECLARED",
    "O2_FEEDBACK_1_UNIT_FAILURE_EVENT_SCHEMA_EMITTED",
    "O2_FEEDBACK_2_UNIT_FEEDBACK_RECORD_SCHEMA_EMITTED",
    "O2_FEEDBACK_3_FAILURE_LOCATION_SCHEMA_EMITTED",
    "O2_FEEDBACK_4_FEEDBACK_QUALITY_ENUM_EMITTED",
    "O2_FEEDBACK_5_MISSING_CAPABILITY_SCHEMA_EMITTED",
    "O2_FEEDBACK_6_REFINEMENT_CANDIDATE_SCHEMA_EMITTED",
    "O2_FEEDBACK_7_RETRY_GATE_SCHEMA_EMITTED",
    "O2_FEEDBACK_8_EDGE_FEEDBACK_LINK_SCHEMA_EMITTED",
    "O2_FEEDBACK_9_DEMO_FAILURE_EVENTS_EMITTED",
    "O2_FEEDBACK_10_EVERY_FAILED_UNIT_HAS_FEEDBACK_RECORD_OR_UNDERTYPED_STOP",
    "O2_FEEDBACK_11_NO_BARE_FAILED_STATUS",
    "O2_FEEDBACK_12_FAILURE_LOCATION_RECORDED_OR_UNDERTYPED",
    "O2_FEEDBACK_13_BOUNDARY_RECORDED_OR_UNDERTYPED",
    "O2_FEEDBACK_14_OBJECT_OR_SOURCE_SURFACE_RECORDED_OR_UNDERTYPED",
    "O2_FEEDBACK_15_MISSING_CAPABILITY_OR_MISSING_EVIDENCE_RECORDED_WHEN_APPLICABLE",
    "O2_FEEDBACK_16_BLOCKED_NEXT_MOVES_RECORDED",
    "O2_FEEDBACK_17_LAWFUL_NEXT_REFINEMENT_OR_QUESTION_RECORDED",
    "O2_FEEDBACK_18_EXPECTED_LIMITS_SEPARATED_FROM_BUGS",
    "O2_FEEDBACK_19_RETRY_BLOCKED_WITHOUT_CHANGED_REFINEMENT",
    "O2_FEEDBACK_20_REFINEMENT_CANDIDATES_PROPOSED_ONLY",
    "O2_FEEDBACK_21_NO_REPAIR_APPLIED",
    "O2_FEEDBACK_22_NO_TARGET_SELECTED_FOR_BUILD",
    "O2_FEEDBACK_23_NO_SOURCE_MUTATION",
    "O2_FEEDBACK_24_NO_C5_OPENED",
    "O2_FEEDBACK_25_ROLLUP_READOUT_PROFILE_EMITTED",
    "O2_FEEDBACK_26_BAD_COUNTERS_ZERO",
    "O2_FEEDBACK_27_NO_HIDDEN_NEXT_COMMAND",
]

NEGATIVE_CONTROLS = [
    "bare_failed_status_fail",
    "failure_without_location_fail",
    "failure_without_boundary_fail",
    "failure_without_object_fail",
    "failure_without_source_surface_fail",
    "failure_without_missing_capability_or_evidence_fail",
    "failure_without_lawful_next_refinement_fail",
    "retry_allowed_without_refinement_fail",
    "repair_applied_by_feedback_unit_fail",
    "target_selected_by_feedback_unit_fail",
    "architecture_change_by_feedback_unit_fail",
    "source_mutated_by_feedback_unit_fail",
    "prior_receipt_mutated_fail",
    "expected_limit_counted_as_bug_fail",
    "productive_pressure_counted_as_success_fail",
    "ambiguous_failure_forced_to_repair_fail",
    "refinement_candidate_counted_as_accepted_fail",
    "c5_opened_by_feedback_unit_fail",
    "hidden_next_command_fail",
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

    receipt = read_json(O1_CLOSE_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o1_surface_closure_summary", {})
    o2_ready = read_json(O1_O2_READY_SURFACE_PATH)
    authority = read_json(O1_CLOSURE_AUTHORITY_PATH)
    rollup = read_json(O1_CLOSURE_ROLLUP_PATH)
    profile = read_json(O1_CLOSURE_PROFILE_PATH)
    o1_records = read_jsonl(O1_SURFACE_RECORDS_PATH)
    o1_surface_rollup = read_json(O1_SURFACE_ROLLUP_PATH)
    o1_readout = read_json(O1_SURFACE_READOUT_PATH)

    if receipt.get("receipt_id") != O1_CLOSE_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("o1_closure_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_O1_STOP:
        failures.append("o1_closure_terminal_not_expected")
    if summary.get("status") != EXPECTED_O1_STATUS:
        failures.append(f"o1_closure_status_not_expected:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_O1_NEXT:
        failures.append(f"o1_closure_next_not_expected:{summary.get('recommended_next')}")

    for key in [
        "o1_surface_closed",
        "closed_as_reviewed_reference",
        "reviewed_reference_emitted",
        "candidate_handles_remain_provisional",
        "o2_design_ready",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"closure_required_true_missing:{key}")

    for key in [
        "o2_executed",
        "graph_schema_claimed",
        "graph_tracker_created",
        "architecture_change",
        "source_receipt_mutated",
        "authority_expansion",
        "target_selected_for_build",
        "runtime_patch_applied",
        "c5_opened",
        "command_emitted",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if summary.get(key) is not False:
            failures.append(f"closure_forbidden_true:{key}")

    expected_counts = {
        "observations_frozen": 8,
        "source_receipt_count": 5,
        "candidate_handle_count": 13,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"closure_count_wrong:{key}:{summary.get(key)}")

    if o2_ready.get("surface_status") != "O2_DESIGN_READY_AFTER_O1_CLOSURE":
        failures.append("o2_ready_surface_status_wrong")
    if o2_ready.get("authorized_next_unit") != EXPECTED_O1_NEXT:
        failures.append("o2_ready_authorized_next_wrong")
    if authority.get("may_design_o2_target_next") is not True:
        failures.append("authority_does_not_allow_o2_design_next")
    if authority.get("may_execute_o2_now") is not False:
        failures.append("authority_allows_o2_execution")
    if rollup.get("o2_design_ready_count") != 1:
        failures.append("rollup_o2_design_ready_count_wrong")
    if rollup.get("o2_executed_count") != 0:
        failures.append("rollup_o2_executed_count_nonzero")
    if profile.get("o2_design_ready") is not True:
        failures.append("profile_o2_design_not_ready")
    if profile.get("o2_executed") is not False:
        failures.append("profile_o2_executed")
    if len(o1_records) != 8:
        failures.append(f"o1_records_count_wrong:{len(o1_records)}")
    if o1_surface_rollup.get("total_observations") != 8:
        failures.append("o1_surface_rollup_observations_wrong")
    if o1_readout.get("bad_counters_zero") is not True:
        failures.append("o1_readout_bad_counters_not_zero")

    return failures, {
        "o1_summary": summary,
        "o1_records_count": len(o1_records),
        "o1_surface_rollup": o1_surface_rollup,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    if failures:
        status = "TYPED_O2_UNIT_FEEDBACK_HARDENING_TARGET_DESIGN_BASIS_FAIL"
        target_designed = False
        reason_codes = failures
        recommended_next = "REPAIR_O2_UNIT_FEEDBACK_HARDENING_TARGET_DESIGN_BASIS_V0"
    else:
        status = "TYPED_O2_UNIT_FEEDBACK_HARDENING_TARGET_DESIGNED_BUILD_READY"
        target_designed = True
        reason_codes = [
            "O2_TARGET_DESIGN_EMITTED",
            "O1_REVIEWED_REFERENCE_CONSUMED",
            "STATIC_SCHEMA_AND_PROBE_ONLY_FROZEN_AS_INITIAL_MODE",
            "LIVE_FEEDBACK_AUDIT_DEFERRED",
            "FEEDBACK_AXES_FROZEN",
            "QUALITY_ENUM_FROZEN",
            "REQUIRED_SCHEMAS_FROZEN",
            "DEMO_PROBE_BOUNDARY_FROZEN",
            "NEGATIVE_CONTROLS_FROZEN",
            "RETRY_GATE_RULE_FROZEN",
            "NONREPAIR_BOUNDARY_LOCKED",
            "BUILD_O2_UNIT_FEEDBACK_HARDENING_AUTHORIZED_NEXT",
            "NO_FEEDBACK_RECORDS_EMITTED_IN_DESIGN_UNIT",
            "NO_REPAIR_APPLIED",
            "NO_RETRY_EXECUTED",
            "NO_TARGET_SELECTED_FOR_BUILD",
            "NO_RUNTIME_PATCH_APPLIED",
            "NO_C5_OPENED",
        ]
        recommended_next = "BUILD_O2_UNIT_FEEDBACK_HARDENING_V0"

    target_design = {
        "schema_version": "o2_unit_feedback_hardening_target_design_v0",
        "design_status": "O2_TARGET_DESIGNED_BUILD_READY" if target_designed else "O2_TARGET_DESIGN_NOT_READY",
        "unit_to_build_next": "BUILD_O2_UNIT_FEEDBACK_HARDENING_V0" if target_designed else None,
        "target_unit_id_to_build": "observation.unit_feedback_hardening.v0",
        "role": "unit feedback hardening layer",
        "core_distinction": "failure status != useful feedback",
        "clean_compression": {
            "O1": "make decision edges visible",
            "O2": "make unit failures useful",
        },
        "design_only": True,
        "feedback_records_emitted_now": False,
        "initial_mode": "STATIC_SCHEMA_AND_PROBE_ONLY",
        "deferred_mode": "LIVE_FEEDBACK_AUDIT",
        "source_basis_receipt_id": O1_CLOSE_RECEIPT_ID,
        "placement": {
            "after": "O1 / C4.5 decision-edge observability surface closure",
            "current": "O2 / C4.6 unit feedback hardening",
            "before": "C5 full domain-shift transition",
        },
    }

    objective_contract = {
        "schema_version": "o2_objective_contract_v0",
        "objective_status": "FROZEN_FOR_BUILD" if target_designed else "NOT_FROZEN",
        "objective": "upgrade unit failure output from bare status to diagnostic feedback",
        "core_question": "If a unit failed, stopped, blocked, or was under-typed, what exactly did that teach us?",
        "goal": "make failure informative enough that future repair, review, proposal, or domain-shift work can proceed without guessing",
        "not_goal": [
            "repair failure",
            "retry unit",
            "select build target",
            "apply runtime patch",
            "open C5",
            "prove root cause globally",
            "count failure as progress",
        ],
        "success_means": [
            "failure feedback names where and why failure occurred",
            "relative object/source/boundary/rule/capability are visible",
            "missing capabilities are candidate-only",
            "refinement candidates are proposed-only",
            "unchanged retries are blocked",
            "expected limits are separated from bugs",
            "rollup/readout/profile summarize feedback quality",
            "bad counters are zero",
        ],
    }

    mode_contract = {
        "schema_version": "o2_initial_mode_contract_v0",
        "initial_mode": "STATIC_SCHEMA_AND_PROBE_ONLY",
        "initial_mode_allowed": [
            "emit schemas",
            "emit feedback quality enum",
            "emit demo failure events",
            "emit demo feedback records",
            "emit rollup/readout",
            "emit negative controls",
            "emit O2 receipt",
        ],
        "initial_mode_not_required": [
            "live source failures",
            "live repair action",
            "live retry",
            "live C5 input",
        ],
        "deferred_mode": "LIVE_FEEDBACK_AUDIT",
        "deferred_mode_requires_explicit_refs": [
            "unit receipt refs",
            "unit trace refs if available",
            "halt records",
            "failure event records",
            "O1 edge observation refs if available",
            "source surface refs",
            "boundary refs",
        ],
        "no_latest_file_selection": True,
        "no_mtime_selection": True,
        "no_ambient_inference": True,
    }

    source_scope_contract = {
        "schema_version": "o2_source_scope_contract_v0",
        "source_scope_status": "STATIC_SCHEMA_AND_PROBE_ONLY_FOR_INITIAL_BUILD",
        "selection_rule": "explicit_refs_only",
        "inspection_mode": "DESIGN_AND_STATIC_PROBE_ONLY",
        "payload_inspection_allowed": False,
        "source_mutation_allowed": False,
        "allowed_inputs_for_later_live_audit": [
            "unit receipts",
            "unit traces",
            "halt records",
            "failure events",
            "B2 failure progress records",
            "O1 decision-edge observation records",
            "source surface refs",
            "boundary refs",
            "capability registry or enum if available",
            "proposal packets",
            "verification records",
            "handoff records",
            "review records",
        ],
        "forbidden_inputs": [
            "repair execution",
            "target selection",
            "architecture changes",
            "source mutation",
            "retry command",
            "hidden memory as failure evidence",
            "unbounded payload inspection",
            "C5 execution artifacts",
            "global closure / autonomy / proof claims",
        ],
        "initial_source_refs": [
            {"receipt_id": O1_CLOSE_RECEIPT_ID, "path": rel(O1_CLOSE_RECEIPT_PATH)},
            {"reference": "o1_reviewed_reference", "path": rel(O1_REVIEWED_REFERENCE_PATH)},
            {"reference": "o1_observation_records", "path": rel(O1_SURFACE_RECORDS_PATH)},
        ],
    }

    feedback_axes_contract = {
        "schema_version": "o2_feedback_axes_contract_v0",
        "axes_status": "FEEDBACK_AXES_FROZEN",
        "required_feedback_axes": FEEDBACK_AXES,
        "relative_to_stack": [
            "object",
            "source surface",
            "boundary",
            "rule",
            "capability",
            "discriminator",
        ],
        "minimum_useful_feedback_requires": [
            "where_failed",
            "failed_relative_to_boundary",
            "missing_capability_or_missing_evidence",
            "lawful_next_refinement_or_question_needed",
        ],
        "if_minimum_cannot_be_filled": [
            "UNDER_TYPED_FEEDBACK",
            "AMBIGUOUS_REQUIRES_QUESTION",
        ],
    }

    quality_enum_contract = {
        "schema_version": "o2_feedback_quality_enum_contract_v0",
        "quality_enum_status": "QUALITY_ENUM_FROZEN",
        "quality_classes": QUALITY_CLASSES,
        "quality_meanings": {
            "NO_FEEDBACK": "No useful information emitted.",
            "STATUS_ONLY": "Only status or generic reason exists.",
            "LOCALIZED_FAILURE": "The unit says where it failed.",
            "BOUNDARY_AWARE_FAILURE": "The unit says which boundary blocked progress.",
            "CAPABILITY_AWARE_FAILURE": "The unit names the missing capability.",
            "REFINEMENT_READY_FAILURE": "The unit names the smallest lawful refinement.",
            "EXPECTED_LIMIT": "The stop is lawful and expected, not a bug.",
            "AMBIGUOUS_REQUIRES_QUESTION": "The failure cannot honestly be classified yet and needs a question packet or withheld action.",
            "UNDER_TYPED_FEEDBACK": "Some diagnostic fields exist, but source is too weak to classify further.",
        },
    }

    schema_contract = {
        "schema_version": "o2_required_schema_contract_v0",
        "schema_status": "REQUIRED_SCHEMAS_FROZEN",
        "required_output_artifacts": REQUIRED_OUTPUT_ARTIFACTS,
        "unit_phase_enum": UNIT_PHASE_ENUM,
        "capability_kind_enum": CAPABILITY_KIND_ENUM,
        "refinement_type_enum": REFINEMENT_TYPE_ENUM,
    }

    demo_probe_contract = {
        "schema_version": "o2_demo_probe_boundary_contract_v0",
        "demo_probe_status": "DEMO_PROBE_BOUNDARY_FROZEN",
        "demo_cases": [
            "bare FAILED status",
            "status-only validation error",
            "localized receipt trace failure",
            "boundary-aware proposal application stop",
            "capability-aware missing target evidence values",
            "refinement-ready source-scope discriminator failure",
            "expected limit proposal requires review",
            "C4 accepted proposal missing verification requirement",
            "ambiguous label remainder failure",
            "retry unchanged failure",
        ],
        "critical_boundary": "demo_failure_events may contain weak examples, but accepted unit_feedback_records must not preserve bare FAILED as useful feedback",
        "negative_examples_may_exist_only_as": [
            "demo input event",
            "negative control",
            "rejected/under-typed source requiring question",
        ],
        "accepted_feedback_records_must": [
            "upgrade weak input into typed feedback",
            "or classify it as UNDER_TYPED_FEEDBACK / AMBIGUOUS_REQUIRES_QUESTION with missing source named",
            "or keep it outside accepted feedback as a negative control failure",
        ],
    }

    negative_control_contract = {
        "schema_version": "o2_negative_control_contract_v0",
        "negative_control_status": "NEGATIVE_CONTROLS_FROZEN",
        "negative_controls": NEGATIVE_CONTROLS,
        "negative_controls_are_non_writing": True,
        "must_not_count_as_accepted_feedback_records": True,
    }

    retry_gate_contract = {
        "schema_version": "o2_retry_gate_contract_v0",
        "retry_gate_status": "RETRY_RULE_FROZEN",
        "retry_allowed_default": False,
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

    nonrepair_boundary = {
        "schema_version": "o2_nonrepair_nonauthority_boundary_v0",
        "boundary_status": "NONREPAIR_BOUNDARY_LOCKED",
        "feedback_record_is_diagnostic_not_repair": True,
        "missing_capability_record_is_candidate_not_authorized_build": True,
        "refinement_candidate_is_proposed_only": True,
        "retry_gate_is_not_retry_command": True,
        "expected_limit_is_not_bug": True,
        "failure_localization_is_not_root_cause_proof": True,
        "feedback_hardening_is_not_c5_opening": True,
        "repair_applied": False,
        "retry_executed": False,
        "target_selected_for_build": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "architecture_change": False,
        "c5_opened": False,
    }

    acceptance_gate_contract = {
        "schema_version": "o2_acceptance_gate_contract_v0",
        "acceptance_gate_status": "GATES_FROZEN_FOR_BUILD",
        "acceptance_gates": ACCEPTANCE_GATES,
        "required_zero_counters": [
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
        ],
        "allowed_nonzero_with_interpretation": [
            "weak_feedback_count may be nonzero in exploratory audit, but C5 remains blocked until resolved or accepted as under-typed with question packet",
        ],
    }

    terminal_contract = {
        "schema_version": "o2_terminal_contract_v0",
        "terminal_contract_status": "TERMINAL_RULES_FROZEN",
        "success_terminal": {
            "type": "STOP",
            "stop_code": "STOP_O2_UNIT_FEEDBACK_HARDENED",
            "next_command_goal": None,
        },
        "weak_feedback_terminal": {
            "type": "STOP",
            "stop_code": "STOP_O2_WEAK_FEEDBACK_REMAINS",
            "next_command_goal": None,
        },
        "c5_block_terminal": {
            "type": "STOP",
            "stop_code": "STOP_O2_C5_BLOCKED_BY_FEEDBACK_QUALITY",
            "next_command_goal": None,
        },
        "question_packet_terminal": {
            "type": "STOP",
            "stop_code": "STOP_O2_QUESTION_PACKET_NOT_COMMAND",
            "next_command_goal": None,
        },
        "authority_violation_terminal": {
            "type": "STOP",
            "stop_code": "STOP_AUTHORITY_VIOLATION",
            "next_command_goal": None,
        },
    }

    build_unit_authorization = {
        "schema_version": "o2_build_unit_authorization_v0",
        "authorization_status": "BUILD_UNIT_AUTHORIZED_NEXT" if target_designed else "BUILD_UNIT_NOT_AUTHORIZED",
        "authorized_next_unit": "BUILD_O2_UNIT_FEEDBACK_HARDENING_V0" if target_designed else None,
        "authorized_initial_mode": "STATIC_SCHEMA_AND_PROBE_ONLY" if target_designed else None,
        "authorized_next_unit_scope": "build static schema/probe O2 unit feedback hardening artifacts, demo events, feedback records, rollup/readout/profile, and receipt",
        "authorization_does_not_allow": [
            "live feedback audit without explicit source receipts",
            "repair execution",
            "retry execution",
            "target selection",
            "runtime patch",
            "source mutation",
            "prior receipt mutation",
            "C5 opening",
            "authority expansion",
            "hidden next command",
        ],
    }

    downstream_decision_table = {
        "schema_version": "o2_target_design_downstream_decision_table_v0",
        "decision_status": "O2_TARGET_DESIGN_DOWNSTREAM_TABLE_EMITTED",
        "records": [
            {
                "decision": "BUILD_O2_UNIT_FEEDBACK_HARDENING",
                "selected": target_designed,
                "next_unit": "BUILD_O2_UNIT_FEEDBACK_HARDENING_V0" if target_designed else None,
                "why": "O2 target, mode, axes, quality enum, schemas, demo/probe boundary, retry gate, non-repair boundary, and gates are frozen.",
            },
            {
                "decision": "RUN_LIVE_FEEDBACK_AUDIT_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Initial O2 mode is STATIC_SCHEMA_AND_PROBE_ONLY; live audit requires explicit source receipts/traces later.",
            },
            {
                "decision": "REPAIR_FAILURES_NOW",
                "selected": False,
                "next_unit": None,
                "why": "O2 makes feedback useful; it does not repair.",
            },
            {
                "decision": "OPEN_C5_NOW",
                "selected": False,
                "next_unit": None,
                "why": "O2 is C5-preflight hardening; C5 remains blocked during O2 design.",
            },
        ],
    }

    classification = {
        "schema_version": "o2_target_design_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "o2_target_designed": target_designed,
        "o2_build_authorized_next": target_designed,
        "authorized_initial_mode": "STATIC_SCHEMA_AND_PROBE_ONLY" if target_designed else None,
        "live_feedback_audit_deferred": True,
        "feedback_axes_frozen": target_designed,
        "quality_enum_frozen": target_designed,
        "required_schemas_frozen": target_designed,
        "demo_probe_boundary_frozen": target_designed,
        "negative_controls_frozen": target_designed,
        "retry_gate_rule_frozen": target_designed,
        "nonrepair_boundary_locked": target_designed,
        "feedback_records_emitted": False,
        "demo_records_emitted": False,
        "repair_applied": False,
        "retry_executed": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "architecture_change": False,
        "c5_opened": False,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    authority_boundary = {
        "schema_version": "o2_target_design_authority_boundary_v0",
        "status": status,
        "may_build_o2_static_schema_probe_next": target_designed,
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

    rollup = {
        "schema_version": "o2_target_design_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "o2_target_designed_count": 1 if target_designed else 0,
        "o2_build_authorized_next_count": 1 if target_designed else 0,
        "feedback_axis_count": len(FEEDBACK_AXES),
        "quality_class_count": len(QUALITY_CLASSES),
        "unit_phase_count": len(UNIT_PHASE_ENUM),
        "capability_kind_count": len(CAPABILITY_KIND_ENUM),
        "refinement_type_count": len(REFINEMENT_TYPE_ENUM),
        "acceptance_gate_count": len(ACCEPTANCE_GATES),
        "negative_control_count": len(NEGATIVE_CONTROLS),
        "required_output_artifact_count": len(REQUIRED_OUTPUT_ARTIFACTS),
        "feedback_records_emitted_count": 0,
        "demo_records_emitted_count": 0,
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
        "feedback_records_emitted_count",
        "demo_records_emitted_count",
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

    profile = {
        "schema_version": "o2_target_design_profile_v0",
        "profile_id": "o2_target_design_profile_" + sha8(rollup),
        "status": status,
        "o2_target_designed": target_designed,
        "o2_build_authorized_next": target_designed,
        "initial_mode": "STATIC_SCHEMA_AND_PROBE_ONLY",
        "live_feedback_audit_deferred": True,
        "target_identity": "BUILD_O2_UNIT_FEEDBACK_HARDENING_V0",
        "core_rule": "Failure feedback must say why, where, relative to what, what is blocked, and what smallest refinement would allow progress.",
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
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
        "schema_version": "o2_target_design_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The O2 unit feedback hardening target was designed from the closed O1 observability reference. The next authorized unit may build O2 in STATIC_SCHEMA_AND_PROBE_ONLY mode. This design freezes the feedback axes, quality enum, required schemas, demo/probe boundary, negative controls, retry gate rule, terminal rules, and non-repair boundary. It emits no feedback records, applies no repair, executes no retry, selects no target, patches no runtime, mutates no sources, and opens no C5.",
        "recommended_next_handling": recommended_next,
        "bad_counters_zero": profile["bad_counters_zero"],
    }

    trace = {
        "schema_version": "o2_target_design_transition_trace_v0",
        "trace": [
            {
                "step": "consume_o1_closure",
                "question": "is O1 closed as reviewed reference and O2 design ready",
                "answer": "yes" if target_designed else "no",
                "taken": "design O2 target",
            },
            {
                "step": "freeze_initial_mode",
                "question": "which O2 mode is lawful first",
                "answer": "STATIC_SCHEMA_AND_PROBE_ONLY",
                "taken": "defer LIVE_FEEDBACK_AUDIT",
            },
            {
                "step": "freeze_feedback_contracts",
                "question": "what must useful feedback contain",
                "answer": "why, where, relative-to stack, blocked moves, lawful refinement, evidence, must-not-infer",
                "taken": "emit axes, quality enum, schemas, demo boundary, retry gate, non-repair boundary",
            },
            {
                "step": "authorize_next",
                "question": "what next unit is lawful",
                "answer": recommended_next,
                "taken": "authorize O2 static schema/probe build next",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    write_json(TARGET_DESIGN_PATH, target_design)
    write_json(OBJECTIVE_CONTRACT_PATH, objective_contract)
    write_json(MODE_CONTRACT_PATH, mode_contract)
    write_json(SOURCE_SCOPE_CONTRACT_PATH, source_scope_contract)
    write_json(FEEDBACK_AXES_CONTRACT_PATH, feedback_axes_contract)
    write_json(QUALITY_ENUM_CONTRACT_PATH, quality_enum_contract)
    write_json(SCHEMA_CONTRACT_PATH, schema_contract)
    write_json(DEMO_PROBE_CONTRACT_PATH, demo_probe_contract)
    write_json(NEGATIVE_CONTROL_CONTRACT_PATH, negative_control_contract)
    write_json(RETRY_GATE_CONTRACT_PATH, retry_gate_contract)
    write_json(NONREPAIR_BOUNDARY_PATH, nonrepair_boundary)
    write_json(ACCEPTANCE_GATE_CONTRACT_PATH, acceptance_gate_contract)
    write_json(TERMINAL_CONTRACT_PATH, terminal_contract)
    write_json(BUILD_UNIT_AUTHORIZATION_PATH, build_unit_authorization)
    write_json(DOWNSTREAM_DECISION_TABLE_PATH, downstream_decision_table)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(AUTHORITY_BOUNDARY_PATH, authority_boundary)
    write_json(ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, profile)
    write_json(REPORT_PATH, report)
    write_json(TRANSITION_TRACE_PATH, trace)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        rollup["source_mutated_count"] = 1
        report["source_mutated_count"] = 1
        write_json(ROLLUP_PATH, rollup)
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "O2_DESIGN_0_O1_CLOSURE_RECEIPT_CONSUMED": O1_CLOSE_RECEIPT_PATH.exists(),
        "O2_DESIGN_1_TARGET_DESIGN_EMITTED": TARGET_DESIGN_PATH.exists(),
        "O2_DESIGN_2_OBJECTIVE_CONTRACT_EMITTED": OBJECTIVE_CONTRACT_PATH.exists(),
        "O2_DESIGN_3_STATIC_SCHEMA_AND_PROBE_ONLY_FROZEN": mode_contract["initial_mode"] == "STATIC_SCHEMA_AND_PROBE_ONLY",
        "O2_DESIGN_4_LIVE_FEEDBACK_AUDIT_DEFERRED": classification["live_feedback_audit_deferred"] is True,
        "O2_DESIGN_5_FEEDBACK_AXES_FROZEN": FEEDBACK_AXES_CONTRACT_PATH.exists() and len(FEEDBACK_AXES) == 13,
        "O2_DESIGN_6_QUALITY_ENUM_FROZEN": QUALITY_ENUM_CONTRACT_PATH.exists() and len(QUALITY_CLASSES) == 9,
        "O2_DESIGN_7_REQUIRED_SCHEMAS_FROZEN": SCHEMA_CONTRACT_PATH.exists(),
        "O2_DESIGN_8_DEMO_PROBE_BOUNDARY_FROZEN": DEMO_PROBE_CONTRACT_PATH.exists(),
        "O2_DESIGN_9_NEGATIVE_CONTROLS_FROZEN": NEGATIVE_CONTROL_CONTRACT_PATH.exists() and len(NEGATIVE_CONTROLS) == 19,
        "O2_DESIGN_10_RETRY_GATE_RULE_FROZEN": RETRY_GATE_CONTRACT_PATH.exists(),
        "O2_DESIGN_11_NONREPAIR_BOUNDARY_LOCKED": NONREPAIR_BOUNDARY_PATH.exists(),
        "O2_DESIGN_12_ACCEPTANCE_GATES_FROZEN": len(ACCEPTANCE_GATES) == 28,
        "O2_DESIGN_13_TERMINAL_RULES_FROZEN": TERMINAL_CONTRACT_PATH.exists(),
        "O2_DESIGN_14_BUILD_UNIT_AUTHORIZED_NEXT": build_unit_authorization["authorization_status"] == "BUILD_UNIT_AUTHORIZED_NEXT",
        "O2_DESIGN_15_NO_FEEDBACK_RECORDS_EMITTED": rollup["feedback_records_emitted_count"] == 0,
        "O2_DESIGN_16_NO_DEMO_RECORDS_EMITTED": rollup["demo_records_emitted_count"] == 0,
        "O2_DESIGN_17_NO_LIVE_AUDIT_EXECUTED": rollup["live_feedback_audit_executed_count"] == 0,
        "O2_DESIGN_18_NO_REPAIR_APPLIED": rollup["repair_applied_count"] == 0,
        "O2_DESIGN_19_NO_RETRY_EXECUTED": rollup["retry_executed_count"] == 0,
        "O2_DESIGN_20_NO_TARGET_SELECTED_FOR_BUILD": rollup["target_selected_for_build_count"] == 0,
        "O2_DESIGN_21_NO_RUNTIME_PATCH": rollup["runtime_patch_count"] == 0,
        "O2_DESIGN_22_NO_SOURCE_MUTATION": rollup["source_mutated_count"] == 0,
        "O2_DESIGN_23_NO_PRIOR_RECEIPT_MUTATION": rollup["prior_receipt_mutated_count"] == 0,
        "O2_DESIGN_24_NO_ARCHITECTURE_CHANGE": rollup["architecture_change_count"] == 0,
        "O2_DESIGN_25_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "O2_DESIGN_26_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "O2_DESIGN_27_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_UNIT_FEEDBACK_HARDENING_TARGET_DESIGN_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "target_designed": target_designed,
        "initial_mode": "STATIC_SCHEMA_AND_PROBE_ONLY",
        "quality_classes": len(QUALITY_CLASSES),
        "axes": len(FEEDBACK_AXES),
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_target_design_receipt_v0",
        "receipt_type": "TYPED_O2_UNIT_FEEDBACK_HARDENING_TARGET_DESIGN_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_o1_closure_receipt_id": O1_CLOSE_RECEIPT_ID,
        "machine_readable_o2_target_design_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "o2_target_designed": target_designed,
            "o2_build_authorized_next": target_designed,
            "authorized_next_unit": "BUILD_O2_UNIT_FEEDBACK_HARDENING_V0" if target_designed else None,
            "authorized_initial_mode": "STATIC_SCHEMA_AND_PROBE_ONLY" if target_designed else None,
            "live_feedback_audit_deferred": True,
            "feedback_axes_frozen": target_designed,
            "quality_enum_frozen": target_designed,
            "required_schemas_frozen": target_designed,
            "demo_probe_boundary_frozen": target_designed,
            "negative_controls_frozen": target_designed,
            "retry_gate_rule_frozen": target_designed,
            "nonrepair_boundary_locked": target_designed,
            "feedback_axis_count": len(FEEDBACK_AXES),
            "quality_class_count": len(QUALITY_CLASSES),
            "acceptance_gate_count": len(ACCEPTANCE_GATES),
            "negative_control_count": len(NEGATIVE_CONTROLS),
            "feedback_records_emitted": False,
            "demo_records_emitted": False,
            "live_feedback_audit_executed": False,
            "repair_applied": False,
            "retry_executed": False,
            "target_selected_for_build": False,
            "runtime_patch_applied": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "architecture_change": False,
            "c5_opened": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": profile["bad_counters_zero"],
            "recommended_next": recommended_next,
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "target_design": rel(TARGET_DESIGN_PATH),
            "objective_contract": rel(OBJECTIVE_CONTRACT_PATH),
            "mode_contract": rel(MODE_CONTRACT_PATH),
            "source_scope_contract": rel(SOURCE_SCOPE_CONTRACT_PATH),
            "feedback_axes_contract": rel(FEEDBACK_AXES_CONTRACT_PATH),
            "quality_enum_contract": rel(QUALITY_ENUM_CONTRACT_PATH),
            "schema_contract": rel(SCHEMA_CONTRACT_PATH),
            "demo_probe_contract": rel(DEMO_PROBE_CONTRACT_PATH),
            "negative_control_contract": rel(NEGATIVE_CONTROL_CONTRACT_PATH),
            "retry_gate_contract": rel(RETRY_GATE_CONTRACT_PATH),
            "nonrepair_boundary": rel(NONREPAIR_BOUNDARY_PATH),
            "acceptance_gate_contract": rel(ACCEPTANCE_GATE_CONTRACT_PATH),
            "terminal_contract": rel(TERMINAL_CONTRACT_PATH),
            "build_unit_authorization": rel(BUILD_UNIT_AUTHORIZATION_PATH),
            "downstream_decision_table": rel(DOWNSTREAM_DECISION_TABLE_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"o2_target_design_receipt_id={receipt_id}")
    print(f"o2_target_design_receipt_path={rel(receipt_path)}")
    print(f"o2_target_design_path={rel(TARGET_DESIGN_PATH)}")
    print(f"o2_objective_contract_path={rel(OBJECTIVE_CONTRACT_PATH)}")
    print(f"o2_mode_contract_path={rel(MODE_CONTRACT_PATH)}")
    print(f"o2_source_scope_contract_path={rel(SOURCE_SCOPE_CONTRACT_PATH)}")
    print(f"o2_feedback_axes_contract_path={rel(FEEDBACK_AXES_CONTRACT_PATH)}")
    print(f"o2_quality_enum_contract_path={rel(QUALITY_ENUM_CONTRACT_PATH)}")
    print(f"o2_demo_probe_contract_path={rel(DEMO_PROBE_CONTRACT_PATH)}")
    print(f"o2_nonrepair_boundary_path={rel(NONREPAIR_BOUNDARY_PATH)}")
    print(f"o2_build_unit_authorization_path={rel(BUILD_UNIT_AUTHORIZATION_PATH)}")
    print(f"o2_target_design_rollup_path={rel(ROLLUP_PATH)}")
    print(f"o2_target_design_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
