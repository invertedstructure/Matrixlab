#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DESIGN_DECISION_EDGE_OBSERVABILITY_HARDENING_TARGET_V0"
TARGET_UNIT_ID = "observation.decision_edge_observability_target_design.v0"
LAYER = "OBSERVATION_HARDENING / DECISION_EDGE_VISIBILITY / TARGET_DESIGN"
MODE = "DESIGN_ONLY / SIDECAR_TARGET / NO_OBSERVATION_EXTRACTION"
BUILD_MODE = "O1_TARGET_DESIGN_ONLY"

SOURCE_CLOSURE_RECEIPT_ID = "c14697ae"
SOURCE_CLOSURE_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_source_ref_layer_closure_v0_receipts/c14697ae.json"
SOURCE_CLOSURE_RECORD_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_source_ref_layer_closure_v0/typed_machine_readable_source_ref_rebind_layer_closure_record_v0.json"
SOURCE_REVIEWED_REFERENCE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_source_ref_layer_closure_v0/typed_machine_readable_source_ref_rebind_layer_reviewed_reference_v0.json"
SOURCE_REFERENCE_FREEZE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_source_ref_layer_closure_v0/typed_machine_readable_source_ref_rebind_layer_reference_freeze_v0.json"
SOURCE_RECEIPT_CHAIN_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_source_ref_layer_closure_v0/typed_machine_readable_source_ref_rebind_layer_closure_receipt_chain_v0.json"
SOURCE_BOUNDARY_LOCK_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_source_ref_layer_closure_v0/typed_machine_readable_source_ref_rebind_layer_closure_boundary_lock_v0.json"
SOURCE_RESIDUAL_CARRY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_source_ref_layer_closure_v0/typed_machine_readable_source_ref_rebind_layer_residual_branch_carry_forward_v0.json"
SOURCE_POST_CLOSURE_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_source_ref_layer_closure_v0/typed_machine_readable_post_source_ref_rebind_closure_decision_surface_v0.json"
SOURCE_POST_UPDATE_HINT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_source_ref_layer_closure_v0/typed_machine_readable_post_closure_observability_feedback_hardening_sequence_hint_v0.json"
SOURCE_CLOSURE_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_source_ref_layer_closure_v0/typed_machine_readable_source_ref_rebind_layer_closure_classification_v0.json"
SOURCE_CLOSURE_AUTHORITY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_source_ref_layer_closure_v0/typed_machine_readable_source_ref_rebind_layer_closure_authority_boundary_v0.json"
SOURCE_CLOSURE_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_source_ref_layer_closure_v0/typed_machine_readable_source_ref_rebind_layer_closure_rollup_v0.json"
SOURCE_CLOSURE_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_source_ref_layer_closure_v0/typed_machine_readable_source_ref_rebind_layer_closure_profile_v0.json"

OUT_DIR = ROOT / "data/o1_decision_edge_observability_target_design_v0"
RECEIPT_DIR = ROOT / "data/o1_decision_edge_observability_target_design_v0_receipts"

TARGET_DESIGN_PATH = OUT_DIR / "o1_decision_edge_observability_target_design_v0.json"
OBJECTIVE_CONTRACT_PATH = OUT_DIR / "o1_objective_contract_v0.json"
SOURCE_SCOPE_CONTRACT_PATH = OUT_DIR / "o1_source_scope_contract_v0.json"
FIELD_CONTRACT_PATH = OUT_DIR / "o1_required_field_contract_v0.json"
CANDIDATE_HANDLE_CONTRACT_PATH = OUT_DIR / "o1_candidate_handle_contract_v0.json"
OUTPUT_ARTIFACT_CONTRACT_PATH = OUT_DIR / "o1_output_artifact_contract_v0.json"
ACCEPTANCE_GATE_CONTRACT_PATH = OUT_DIR / "o1_acceptance_gate_contract_v0.json"
NEGATIVE_CONTROL_CONTRACT_PATH = OUT_DIR / "o1_negative_control_contract_v0.json"
TERMINAL_CONTRACT_PATH = OUT_DIR / "o1_terminal_contract_v0.json"
NONAUTHORITY_BOUNDARY_PATH = OUT_DIR / "o1_nonauthority_boundary_v0.json"
BUILD_UNIT_AUTHORIZATION_PATH = OUT_DIR / "o1_build_unit_authorization_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "o1_target_design_downstream_decision_table_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o1_target_design_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o1_target_design_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "o1_target_design_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o1_target_design_profile_v0.json"
REPORT_PATH = OUT_DIR / "o1_target_design_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "o1_target_design_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_CLOSURE_RECEIPT_PATH,
    SOURCE_CLOSURE_RECORD_PATH,
    SOURCE_REVIEWED_REFERENCE_PATH,
    SOURCE_REFERENCE_FREEZE_PATH,
    SOURCE_RECEIPT_CHAIN_PATH,
    SOURCE_BOUNDARY_LOCK_PATH,
    SOURCE_RESIDUAL_CARRY_PATH,
    SOURCE_POST_CLOSURE_SURFACE_PATH,
    SOURCE_POST_UPDATE_HINT_PATH,
    SOURCE_CLOSURE_CLASSIFICATION_PATH,
    SOURCE_CLOSURE_AUTHORITY_PATH,
    SOURCE_CLOSURE_ROLLUP_PATH,
    SOURCE_CLOSURE_PROFILE_PATH,
]

EXPECTED_CLOSURE_STATUS = "TYPED_SOURCE_REF_REBIND_LAYER_CLOSED_AS_REVIEWED_REFERENCE_POST_UPDATE_DECISION_READY"
EXPECTED_CLOSURE_STOP = "STOP_TYPED_SOURCE_REF_REBIND_LAYER_CLOSED_AS_REVIEWED_REFERENCE_POST_UPDATE_DECISION_READY"
EXPECTED_CLOSURE_NEXT = "DESIGN_DECISION_EDGE_OBSERVABILITY_HARDENING_TARGET_V0"

REQUIRED_FIELDS = [
    "source_receipt_ref",
    "source_unit_id",
    "active_object",
    "active_object_kind",
    "pressure_or_trigger",
    "attempted_move",
    "attempted_move_kind",
    "boundary_checked",
    "boundary_kind",
    "boundary_result",
    "guard_result",
    "classification",
    "candidate_edge_handles",
    "missing_object",
    "missing_capability",
    "authority_boundary_exposed",
    "capability_boundary_exposed",
    "blocked_moves",
    "lawful_next_moves",
    "forbidden_next_moves",
    "terminal_result",
    "parent_return_payload",
    "collection_status",
    "schema_claim",
    "architecture_change",
    "source_receipt_mutated",
    "authority_expansion",
    "runtime_patch_applied",
    "target_selected_for_build",
    "c5_opened",
]

CANDIDATE_HANDLES = [
    "OBSERVE_RECEIPT_EDGE",
    "CLASSIFY_DISTINGUISH_EDGE",
    "GUARD_AUTHORITY_EDGE",
    "PROPOSE_VALIDATE_EDGE",
    "CLOSE_FREEZE_ESCALATE_EDGE",
    "REPAIR_OR_FALLBACK_EDGE",
    "CAPABILITY_BOUNDARY_EDGE",
    "REFERENCE_ONLY_EDGE",
    "CAPABILITY_PROVIDER_MATERIALIZATION_EDGE",
    "BUILDER_HANDOFF_EDGE",
    "VERIFICATION_RETURN_EDGE",
    "LABEL_NON_COLLAPSE_EDGE",
    "FAILURE_PROGRESS_EDGE",
]

ACCEPTANCE_GATES = [
    "O1_EDGE_0_SOURCE_SURFACE_DECLARED",
    "O1_EDGE_1_EXPLICIT_SOURCE_RECEIPTS_CONSUMED",
    "O1_EDGE_2_OBSERVATION_RECORD_SCHEMA_EMITTED",
    "O1_EDGE_3_CANDIDATE_HANDLE_SCHEMA_EMITTED",
    "O1_EDGE_4_CANDIDATE_HANDLES_MARKED_PROVISIONAL",
    "O1_EDGE_5_OBSERVATION_RECORDS_EMITTED",
    "O1_EDGE_6_EVERY_RECORD_HAS_SOURCE_RECEIPT_REF",
    "O1_EDGE_7_EVERY_RECORD_HAS_ACTIVE_OBJECT_OR_UNDERTYPED_STATUS",
    "O1_EDGE_8_EVERY_RECORD_HAS_BOUNDARY_CHECKED_OR_UNDERTYPED_STATUS",
    "O1_EDGE_9_EVERY_RECORD_HAS_BOUNDARY_RESULT_OR_UNDERTYPED_STATUS",
    "O1_EDGE_10_BLOCKED_MOVES_RECORDED_WHEN_PRESENT",
    "O1_EDGE_11_LAWFUL_NEXT_MOVES_RECORDED_WHEN_PRESENT",
    "O1_EDGE_12_TERMINAL_RESULT_RECORDED",
    "O1_EDGE_13_PARENT_RETURN_PAYLOAD_PRESERVED_WHEN_PRESENT",
    "O1_EDGE_14_COLLECTION_STATUS_OBSERVATION_ONLY",
    "O1_EDGE_15_SCHEMA_CLAIM_NONE",
    "O1_EDGE_16_NO_ARCHITECTURE_CHANGE",
    "O1_EDGE_17_NO_SOURCE_RECEIPT_MUTATION",
    "O1_EDGE_18_NO_AUTHORITY_EXPANSION",
    "O1_EDGE_19_NO_TARGET_SELECTED_FOR_BUILD",
    "O1_EDGE_20_NO_RUNTIME_PATCH",
    "O1_EDGE_21_NO_C5_OPENED",
    "O1_EDGE_22_ROLLUP_PROFILE_READOUT_EMITTED",
    "O1_EDGE_23_BAD_COUNTERS_ZERO",
    "O1_EDGE_24_NO_HIDDEN_NEXT_COMMAND",
]

NEGATIVE_CONTROLS = [
    "source_receipt_mutated_fail",
    "candidate_handle_treated_as_final_primitive_fail",
    "schema_claim_emitted_fail",
    "architecture_change_emitted_fail",
    "edge_observation_emits_command_fail",
    "edge_observation_selects_build_target_fail",
    "edge_observation_opens_c5_fail",
    "missing_object_invented_without_source_basis_fail",
    "blocked_moves_omitted_fail",
    "lawful_next_moves_omitted_fail",
    "terminal_result_missing_fail",
    "bad_counters_hidden_fail",
    "latest_or_mtime_selection_fail",
    "authority_expansion_fail",
    "runtime_patch_fail",
]

OUTPUT_ARTIFACTS = [
    "data/o1_decision_edge_observability_surface_v0/decision_edge_observation_record_schema_v0.json",
    "data/o1_decision_edge_observability_surface_v0/decision_edge_candidate_handle_schema_v0.json",
    "data/o1_decision_edge_observability_surface_v0/decision_edge_candidate_handle_records_v0.jsonl",
    "data/o1_decision_edge_observability_surface_v0/decision_edge_observation_records_v0.jsonl",
    "data/o1_decision_edge_observability_surface_v0/decision_edge_observation_rollup_v0.json",
    "data/o1_decision_edge_observability_surface_v0/decision_edge_observation_profile_v0.json",
    "data/o1_decision_edge_observability_surface_v0/decision_edge_observation_readout_v0.json",
    "data/o1_decision_edge_observability_surface_v0/o1_source_surface_v0.json",
    "data/o1_decision_edge_observability_surface_v0/o1_transition_trace.json",
    "data/o1_decision_edge_observability_surface_v0/o1_report.json",
    "data/o1_decision_edge_observability_surface_v0_receipts/<receipt_id>.json",
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

    receipt = read_json(SOURCE_CLOSURE_RECEIPT_PATH)
    summary = receipt.get("machine_readable_source_ref_rebind_layer_closure_summary", {})
    post_surface = read_json(SOURCE_POST_CLOSURE_SURFACE_PATH)
    hint = read_json(SOURCE_POST_UPDATE_HINT_PATH)
    authority = read_json(SOURCE_CLOSURE_AUTHORITY_PATH)
    rollup = read_json(SOURCE_CLOSURE_ROLLUP_PATH)
    profile = read_json(SOURCE_CLOSURE_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_CLOSURE_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_closure_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_CLOSURE_STOP:
        failures.append("source_terminal_not_expected")
    if summary.get("status") != EXPECTED_CLOSURE_STATUS:
        failures.append(f"source_status_not_expected:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_CLOSURE_NEXT:
        failures.append(f"source_next_not_expected:{summary.get('recommended_next')}")

    for key in [
        "source_ref_rebind_layer_closed",
        "closed_as_reviewed_reference",
        "reviewed_reference_emitted",
        "post_closure_next_objective_decision_ready",
        "schema_overlay_applied_for_this_contract",
    ]:
        if summary.get(key) is not True:
            failures.append(f"closure_summary_required_true_missing:{key}")

    expected_counts = {
        "applied_rebind_count": 4,
        "proposal_binding_count": 4,
        "ambiguity_binding_count_preserved": 22,
        "requirement_gap_binding_count_preserved": 498,
        "ready_discriminator_count": 0,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"closure_summary_count_wrong:{key}:{summary.get(key)}")

    for key in [
        "post_closure_next_objective_executed",
        "schema_overlay_applied_globally",
        "reusable_schema_authorized",
        "preapproved_schema_authorized",
        "validator_registry_entry_created",
        "future_automatic_use_allowed",
        "values_authorized",
        "values_applied",
        "metadata_populated",
        "target_selected_for_build",
        "runtime_patch_applied",
        "c5_opened",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if summary.get(key) is not False:
            failures.append(f"closure_forbidden_true:{key}")

    if post_surface.get("decision_surface_status") != "POST_CLOSURE_NEXT_OBJECTIVE_READY":
        failures.append("post_closure_decision_surface_not_ready")
    if post_surface.get("recommended_default") != EXPECTED_CLOSURE_NEXT:
        failures.append("post_closure_recommended_default_wrong")
    if hint.get("hint_status") != "POST_UPDATE_HARDENING_SEQUENCE_PRESERVED_AS_HINT_NOT_EXECUTED":
        failures.append("post_update_hint_status_wrong")
    hint_targets = [x.get("target") for x in hint.get("sequence", []) if isinstance(x, dict)]
    if hint_targets[:2] != ["decision_edge_observability", "unit_feedback_hardening"]:
        failures.append(f"hint_sequence_wrong:{hint_targets}")
    if authority.get("may_design_decision_edge_observability_next") is not True:
        failures.append("authority_does_not_allow_o1_design_next")
    if rollup.get("post_closure_next_objective_executed_count") != 0:
        failures.append("rollup_post_closure_already_executed")
    if profile.get("post_closure_next_objective_executed") is not False:
        failures.append("profile_post_closure_already_executed")

    return failures, {
        "closure_summary": summary,
        "post_surface": post_surface,
        "hint": hint,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    if failures:
        status = "TYPED_O1_DECISION_EDGE_OBSERVABILITY_TARGET_DESIGN_BASIS_FAIL"
        reason_codes = failures
        target_designed = False
        next_edge = "REPAIR_O1_DECISION_EDGE_OBSERVABILITY_TARGET_DESIGN_BASIS_V0"
    else:
        status = "TYPED_O1_DECISION_EDGE_OBSERVABILITY_HARDENING_TARGET_DESIGNED_BUILD_READY"
        reason_codes = [
            "O1_TARGET_DESIGN_EMITTED",
            "SOURCE_REF_REBIND_CLOSURE_RECEIPT_CONSUMED",
            "O1_SCOPE_SET_TO_RECEIPT_SIDE_DECISION_EDGE_OBSERVABILITY",
            "SIDECAR_ONLY_OBSERVATION_SURFACE_REQUIRED",
            "EXPLICIT_REFS_ONLY_SELECTION_RULE_REQUIRED",
            "REQUIRED_EDGE_FIELDS_FROZEN",
            "PROVISIONAL_CANDIDATE_HANDLES_FROZEN",
            "ACCEPTANCE_GATES_FROZEN",
            "NEGATIVE_CONTROLS_FROZEN",
            "BUILD_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_AUTHORIZED_NEXT",
            "NO_OBSERVATIONS_EXTRACTED_IN_DESIGN_UNIT",
            "NO_GRAPH_SCHEMA_CLAIMED",
            "NO_GRAPH_TRACKER_CREATED",
            "NO_ARCHITECTURE_CHANGE",
            "NO_SOURCE_RECEIPT_MUTATION",
            "NO_AUTHORITY_EXPANSION",
            "NO_TARGET_SELECTED_FOR_BUILD",
            "NO_RUNTIME_PATCH_APPLIED",
            "NO_C5_OPENED",
        ]
        target_designed = True
        next_edge = "BUILD_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_V0"

    target_design = {
        "schema_version": "o1_decision_edge_observability_target_design_v0",
        "design_status": "O1_TARGET_DESIGNED_BUILD_READY" if target_designed else "O1_TARGET_DESIGN_NOT_READY",
        "unit_to_build_next": "BUILD_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_V0" if target_designed else None,
        "target_unit_id_to_build": "observation.decision_edge_observability_surface.v0",
        "role": "receipt-side decision-edge observability surface",
        "core_distinction": "Do not build the graph. Make the edges observable.",
        "design_only": True,
        "observations_extracted_now": False,
        "active_object": "source receipts and transition artifacts from bounded Cell 0 / Cell 1 runs",
        "source_basis_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "placement": {
            "after": "C4 / source-ref rebind layer closure",
            "current": "O1 / C4.5 decision-edge observability surface",
            "next_recommended": "O2 / C4.6 unit feedback hardening",
            "before": "C5 full domain shift",
        },
    }

    objective_contract = {
        "schema_version": "o1_objective_contract_v0",
        "objective_status": "FROZEN_FOR_BUILD" if target_designed else "NOT_FROZEN",
        "objective": "emit source-backed sidecar records that expose local decision-edge fields from receipts",
        "questions_answered": [
            "What object was active?",
            "What pressure or trigger existed?",
            "What move was attempted or considered?",
            "What boundary was checked?",
            "What result occurred?",
            "What was blocked?",
            "What became lawful?",
            "What terminal returned?",
        ],
        "success_means": [
            "decision-edge sidecars exist",
            "edge-like transitions are visible from receipts",
            "candidate handles are provisional",
            "blocked and lawful moves are captured",
            "boundary exposure is visible",
            "rollup/profile/readout summarize observations",
            "bad counters are zero",
            "no graph schema is claimed",
        ],
        "success_does_not_mean": [
            "decision graph is built",
            "edge taxonomy is final",
            "architecture changed",
            "C5 opened",
            "target selected for build",
            "authority expanded",
            "recurrence proven",
        ],
    }

    source_scope_contract = {
        "schema_version": "o1_source_scope_contract_v0",
        "source_scope_status": "EXPLICIT_REFS_ONLY",
        "selection_rule": "explicit_refs_only",
        "inspection_mode": "REF_AND_SUMMARY_ONLY",
        "payload_inspection_allowed": False,
        "source_mutation_allowed": False,
        "allowed_inputs": [
            "source receipt refs",
            "source unit IDs",
            "source artifact refs",
            "loop traces",
            "proposal packets",
            "label audits",
            "build / verification / handoff receipts",
            "schema-consumption reference packets",
            "halt records",
            "authority verdict records",
            "failure-progress records",
            "proposal review records",
        ],
        "forbidden_inputs": [
            "hidden graph assumptions",
            "final graph schema",
            "ambient workspace inference",
            "latest-file guessing",
            "mtime selection",
            "unreviewed target selection",
            "runtime patching",
            "C5 planning as authorization",
            "authority expansion",
            "global closure / autonomy / proof claims",
        ],
        "initial_source_receipts": [
            {"receipt_id": SOURCE_CLOSURE_RECEIPT_ID, "path": rel(SOURCE_CLOSURE_RECEIPT_PATH)},
            {"receipt_id": "b3bcc049", "path": "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0_receipts/b3bcc049.json"},
            {"receipt_id": "4086e0bb", "path": "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0_receipts/4086e0bb.json"},
            {"receipt_id": "f549ad67", "path": "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0_receipts/f549ad67.json"},
        ],
    }

    field_contract = {
        "schema_version": "o1_required_field_contract_v0",
        "field_contract_status": "REQUIRED_FIELDS_FROZEN",
        "required_fields": REQUIRED_FIELDS,
        "under_typed_policy": {
            "allowed": True,
            "confidence_class": "UNDER_TYPED",
            "schema_claim": "NONE",
            "collection_status": "OBSERVATION_ONLY",
            "terminal_if_source_surface_under_typed": "STOP_O1_OBSERVATION_SOURCE_UNDER_TYPED",
        },
    }

    candidate_handle_contract = {
        "schema_version": "o1_candidate_handle_contract_v0",
        "candidate_handle_status": "PROVISIONAL_HANDLES_ONLY",
        "candidate_handles": CANDIDATE_HANDLES,
        "allowed_use": [
            "tag observation",
            "count recurrence",
            "compare with future observations",
        ],
        "forbidden_use": [
            "authorize move",
            "define final graph edge",
            "open new architecture",
            "claim proof of recurrence",
        ],
    }

    output_artifact_contract = {
        "schema_version": "o1_output_artifact_contract_v0",
        "output_artifact_status": "OUTPUTS_FROZEN_FOR_BUILD",
        "required_output_artifacts": OUTPUT_ARTIFACTS,
        "forbidden_output_artifacts": [
            "source receipt mutation",
            "runtime patches",
            "target build selection",
            "accepted proposal fabrication",
            "C5 artifacts",
            "decision graph tracker",
            "final graph schema",
            "architecture mutation",
            "taxonomy registry mutation",
            "move registry mutation",
            "general Cell 1 authority artifacts",
        ],
    }

    acceptance_gate_contract = {
        "schema_version": "o1_acceptance_gate_contract_v0",
        "acceptance_gate_status": "GATES_FROZEN_FOR_BUILD",
        "acceptance_gates": ACCEPTANCE_GATES,
        "required_zero_counters": [
            "schema_claim_count",
            "architecture_change_count",
            "source_receipt_mutation_count",
            "authority_expansion_count",
            "target_selected_for_build_count",
            "runtime_patch_count",
            "c5_opened_count",
            "command_emitted_count",
        ],
    }

    negative_control_contract = {
        "schema_version": "o1_negative_control_contract_v0",
        "negative_control_status": "NEGATIVE_CONTROLS_FROZEN_FOR_BUILD",
        "negative_controls": NEGATIVE_CONTROLS,
        "negative_controls_are_non_writing": True,
    }

    terminal_contract = {
        "schema_version": "o1_terminal_contract_v0",
        "terminal_contract_status": "TERMINAL_RULES_FROZEN_FOR_BUILD",
        "success_terminal": {
            "type": "STOP",
            "stop_code": "STOP_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_EMITTED",
            "next_command_goal": None,
        },
        "under_typed_terminal": {
            "type": "STOP",
            "stop_code": "STOP_O1_OBSERVATION_SOURCE_UNDER_TYPED",
            "next_command_goal": None,
        },
        "schema_extraction_terminal": {
            "type": "STOP",
            "stop_code": "STOP_O1_GRAPH_SCHEMA_EXTRACTION_NOT_AUTHORIZED",
            "next_command_goal": None,
        },
        "authority_violation_terminal": {
            "type": "STOP",
            "stop_code": "STOP_AUTHORITY_VIOLATION",
            "next_command_goal": None,
        },
    }

    nonauthority_boundary = {
        "schema_version": "o1_nonauthority_boundary_v0",
        "boundary_status": "NONAUTHORITY_BOUNDARY_FROZEN",
        "observation_record_is_evidence_not_authority": True,
        "may_describe_transition": True,
        "may_command_transition": False,
        "may_tag_candidate_edge_handle": True,
        "may_define_final_graph_primitive": False,
        "may_show_recurrence": True,
        "may_claim_recurrence_as_proof": False,
        "may_expose_missing_object_or_capability": True,
        "may_invent_or_apply_missing_object": False,
        "schema_claim": "NONE",
        "architecture_change": False,
        "authority_expansion": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "c5_opened": False,
    }

    build_unit_authorization = {
        "schema_version": "o1_build_unit_authorization_v0",
        "authorization_status": "BUILD_UNIT_AUTHORIZED_NEXT" if target_designed else "BUILD_UNIT_NOT_AUTHORIZED",
        "authorized_next_unit": "BUILD_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_V0" if target_designed else None,
        "authorized_next_unit_scope": "build the sidecar-only receipt-backed O1 decision-edge observability surface from explicit source refs",
        "authorization_does_not_allow": [
            "graph schema extraction",
            "decision graph tracker",
            "source receipt mutation",
            "target build selection",
            "runtime patch",
            "C5 opening",
            "authority expansion",
            "schema reuse promotion",
            "hidden next command",
        ],
    }

    downstream_decision_table = {
        "schema_version": "o1_target_design_downstream_decision_table_v0",
        "decision_status": "O1_TARGET_DESIGN_DOWNSTREAM_TABLE_EMITTED",
        "records": [
            {
                "decision": "BUILD_O1_DECISION_EDGE_OBSERVABILITY_SURFACE",
                "selected": target_designed,
                "next_unit": "BUILD_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_V0" if target_designed else None,
                "why": "O1 target, source scope, fields, gates, negative controls, terminal rules, and boundaries are frozen for build",
            },
            {
                "decision": "BUILD_DECISION_GRAPH_TRACKER",
                "selected": False,
                "next_unit": None,
                "why": "O1 is observability, not graph tracker construction",
            },
            {
                "decision": "START_UNIT_FEEDBACK_HARDENING_NOW",
                "selected": False,
                "next_unit": None,
                "why": "O2 follows after O1 surface build/review",
            },
            {
                "decision": "START_METADATA_VALUE_POPULATION_NOW",
                "selected": False,
                "next_unit": None,
                "why": "metadata/value population remains after post-update hardening",
            },
        ],
    }

    classification = {
        "schema_version": "o1_target_design_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "o1_target_designed": target_designed,
        "o1_build_authorized_next": target_designed,
        "observations_extracted": False,
        "observation_records_emitted": False,
        "source_surface_frozen": target_designed,
        "required_fields_frozen": target_designed,
        "candidate_handles_frozen_as_provisional": target_designed,
        "acceptance_gates_frozen": target_designed,
        "negative_controls_frozen": target_designed,
        "terminal_rules_frozen": target_designed,
        "sidecar_only": True,
        "explicit_refs_only": True,
        "payload_inspection_allowed": False,
        "source_mutation_allowed": False,
        "graph_schema_claimed": False,
        "graph_tracker_created": False,
        "architecture_change": False,
        "source_receipt_mutated": False,
        "authority_expansion": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "c5_opened": False,
        "values_authorized": False,
        "values_applied": False,
        "metadata_populated": False,
        "unit_feedback_hardening_executed": False,
        "recommended_next": next_edge,
        "next_command_goal": None,
    }

    authority_boundary = {
        "schema_version": "o1_target_design_authority_boundary_v0",
        "status": status,
        "may_build_o1_decision_edge_surface_next": target_designed,
        "may_extract_observations_now": False,
        "may_create_graph_schema": False,
        "may_create_graph_tracker": False,
        "may_promote_candidate_handles_to_final_primitives": False,
        "may_mutate_source_receipts": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "may_select_target_for_build": False,
        "may_patch_runtime": False,
        "may_open_c5": False,
        "may_expand_authority": False,
        "may_start_o2_now": False,
        "may_start_metadata_value_population_now": False,
    }

    rollup = {
        "schema_version": "o1_target_design_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "o1_target_designed_count": 1 if target_designed else 0,
        "o1_build_authorized_next_count": 1 if target_designed else 0,
        "required_field_count": len(REQUIRED_FIELDS),
        "candidate_handle_count": len(CANDIDATE_HANDLES),
        "acceptance_gate_count": len(ACCEPTANCE_GATES),
        "negative_control_count": len(NEGATIVE_CONTROLS),
        "required_output_artifact_count": len(OUTPUT_ARTIFACTS),
        "source_receipt_ref_count": 4,
        "observations_extracted_count": 0,
        "observation_records_emitted_count": 0,
        "graph_schema_claim_count": 0,
        "graph_tracker_created_count": 0,
        "architecture_change_count": 0,
        "source_receipt_mutation_count": 0,
        "authority_expansion_count": 0,
        "target_selected_for_build_count": 0,
        "runtime_patch_count": 0,
        "c5_opened_count": 0,
        "values_authorized_count": 0,
        "values_applied_count": 0,
        "metadata_populated_count": 0,
        "unit_feedback_hardening_executed_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": next_edge,
    }

    zero_keys = [
        "observations_extracted_count",
        "observation_records_emitted_count",
        "graph_schema_claim_count",
        "graph_tracker_created_count",
        "architecture_change_count",
        "source_receipt_mutation_count",
        "authority_expansion_count",
        "target_selected_for_build_count",
        "runtime_patch_count",
        "c5_opened_count",
        "values_authorized_count",
        "values_applied_count",
        "metadata_populated_count",
        "unit_feedback_hardening_executed_count",
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "o1_target_design_profile_v0",
        "profile_id": "o1_target_design_profile_" + sha8(rollup),
        "status": status,
        "o1_target_designed": target_designed,
        "o1_build_authorized_next": target_designed,
        "target_identity": "BUILD_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_V0",
        "design_scope": "receipt-side sidecar observability only",
        "required_field_count": len(REQUIRED_FIELDS),
        "candidate_handle_count": len(CANDIDATE_HANDLES),
        "acceptance_gate_count": len(ACCEPTANCE_GATES),
        "negative_control_count": len(NEGATIVE_CONTROLS),
        "graph_schema_claimed": False,
        "graph_tracker_created": False,
        "observations_extracted": False,
        "architecture_change": False,
        "source_receipt_mutated": False,
        "authority_expansion": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "c5_opened": False,
        "recommended_next": next_edge,
        "recommended_second": "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET_V0",
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o1_target_design_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The O1 decision-edge observability hardening target was designed from the closed source-ref rebind layer. The next authorized unit may build a sidecar-only, explicit-ref, receipt-backed edge observability surface. This design does not extract observations, define a graph schema, create a graph tracker, select a build target, patch runtime, expand authority, open C5, or start O2.",
        "recommended_next_handling": next_edge,
        "recommended_second_handling": "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET_V0",
        "bad_counters_zero": profile["bad_counters_zero"],
    }

    trace = {
        "schema_version": "o1_target_design_transition_trace_v0",
        "trace": [
            {
                "step": "consume_closure_reference",
                "question": "is source-ref rebind layer closed and post-update decision ready",
                "answer": "yes" if target_designed else "no",
                "taken": "design O1 target",
            },
            {
                "step": "freeze_o1_scope",
                "question": "what is O1 allowed to build",
                "answer": "sidecar-only decision-edge observability surface from explicit receipt refs",
                "taken": "emit source scope, fields, gates, negative controls, terminal contract",
            },
            {
                "step": "preserve_non_graph_boundary",
                "question": "does this design build a graph or tracker",
                "answer": "no",
                "taken": "emit nonauthority boundary",
            },
            {
                "step": "authorize_next",
                "question": "what next unit is lawful",
                "answer": next_edge,
                "taken": "authorize O1 build next, no observations extracted now",
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
    write_json(SOURCE_SCOPE_CONTRACT_PATH, source_scope_contract)
    write_json(FIELD_CONTRACT_PATH, field_contract)
    write_json(CANDIDATE_HANDLE_CONTRACT_PATH, candidate_handle_contract)
    write_json(OUTPUT_ARTIFACT_CONTRACT_PATH, output_artifact_contract)
    write_json(ACCEPTANCE_GATE_CONTRACT_PATH, acceptance_gate_contract)
    write_json(NEGATIVE_CONTROL_CONTRACT_PATH, negative_control_contract)
    write_json(TERMINAL_CONTRACT_PATH, terminal_contract)
    write_json(NONAUTHORITY_BOUNDARY_PATH, nonauthority_boundary)
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
        rollup["source_receipt_mutation_count"] = 1
        report["source_receipt_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup)
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "O1_DESIGN_0_SOURCE_CLOSURE_RECEIPT_CONSUMED": SOURCE_CLOSURE_RECEIPT_PATH.exists(),
        "O1_DESIGN_1_TARGET_DESIGN_EMITTED": TARGET_DESIGN_PATH.exists(),
        "O1_DESIGN_2_OBJECTIVE_CONTRACT_EMITTED": OBJECTIVE_CONTRACT_PATH.exists(),
        "O1_DESIGN_3_SOURCE_SCOPE_CONTRACT_EXPLICIT_REFS_ONLY": source_scope_contract["selection_rule"] == "explicit_refs_only",
        "O1_DESIGN_4_REQUIRED_FIELDS_FROZEN": FIELD_CONTRACT_PATH.exists() and len(REQUIRED_FIELDS) >= 30,
        "O1_DESIGN_5_CANDIDATE_HANDLES_PROVISIONAL": candidate_handle_contract["candidate_handle_status"] == "PROVISIONAL_HANDLES_ONLY",
        "O1_DESIGN_6_OUTPUT_ARTIFACTS_FROZEN": OUTPUT_ARTIFACT_CONTRACT_PATH.exists(),
        "O1_DESIGN_7_ACCEPTANCE_GATES_FROZEN": len(ACCEPTANCE_GATES) == 25,
        "O1_DESIGN_8_NEGATIVE_CONTROLS_FROZEN": len(NEGATIVE_CONTROLS) >= 15,
        "O1_DESIGN_9_TERMINAL_RULES_FROZEN": TERMINAL_CONTRACT_PATH.exists(),
        "O1_DESIGN_10_NONAUTHORITY_BOUNDARY_FROZEN": NONAUTHORITY_BOUNDARY_PATH.exists(),
        "O1_DESIGN_11_BUILD_UNIT_AUTHORIZED_NEXT": build_unit_authorization["authorization_status"] == "BUILD_UNIT_AUTHORIZED_NEXT",
        "O1_DESIGN_12_NO_OBSERVATIONS_EXTRACTED": rollup["observations_extracted_count"] == 0,
        "O1_DESIGN_13_NO_OBSERVATION_RECORDS_EMITTED": rollup["observation_records_emitted_count"] == 0,
        "O1_DESIGN_14_NO_GRAPH_SCHEMA_CLAIM": rollup["graph_schema_claim_count"] == 0,
        "O1_DESIGN_15_NO_GRAPH_TRACKER": rollup["graph_tracker_created_count"] == 0,
        "O1_DESIGN_16_NO_ARCHITECTURE_CHANGE": rollup["architecture_change_count"] == 0,
        "O1_DESIGN_17_NO_SOURCE_RECEIPT_MUTATION": rollup["source_receipt_mutation_count"] == 0,
        "O1_DESIGN_18_NO_AUTHORITY_EXPANSION": rollup["authority_expansion_count"] == 0,
        "O1_DESIGN_19_NO_TARGET_SELECTED_FOR_BUILD": rollup["target_selected_for_build_count"] == 0,
        "O1_DESIGN_20_NO_RUNTIME_PATCH": rollup["runtime_patch_count"] == 0,
        "O1_DESIGN_21_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "O1_DESIGN_22_NO_O2_EXECUTED": rollup["unit_feedback_hardening_executed_count"] == 0,
        "O1_DESIGN_23_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "O1_DESIGN_24_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O1_DECISION_EDGE_OBSERVABILITY_TARGET_DESIGN_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "target_designed": target_designed,
        "required_fields": len(REQUIRED_FIELDS),
        "handles": len(CANDIDATE_HANDLES),
        "observations": 0,
        "graph": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o1_target_design_receipt_v0",
        "receipt_type": "TYPED_O1_DECISION_EDGE_OBSERVABILITY_TARGET_DESIGN_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_closure_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "machine_readable_o1_target_design_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "o1_target_designed": target_designed,
            "o1_build_authorized_next": target_designed,
            "authorized_next_unit": "BUILD_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_V0" if target_designed else None,
            "source_surface_frozen": target_designed,
            "required_fields_frozen": target_designed,
            "candidate_handles_frozen_as_provisional": target_designed,
            "acceptance_gates_frozen": target_designed,
            "negative_controls_frozen": target_designed,
            "terminal_rules_frozen": target_designed,
            "sidecar_only": True,
            "explicit_refs_only": True,
            "observations_extracted": False,
            "observation_records_emitted": False,
            "graph_schema_claimed": False,
            "graph_tracker_created": False,
            "architecture_change": False,
            "source_receipt_mutated": False,
            "authority_expansion": False,
            "target_selected_for_build": False,
            "runtime_patch_applied": False,
            "c5_opened": False,
            "values_authorized": False,
            "values_applied": False,
            "metadata_populated": False,
            "unit_feedback_hardening_executed": False,
            "required_field_count": len(REQUIRED_FIELDS),
            "candidate_handle_count": len(CANDIDATE_HANDLES),
            "acceptance_gate_count": len(ACCEPTANCE_GATES),
            "negative_control_count": len(NEGATIVE_CONTROLS),
            "bad_counters_zero": profile["bad_counters_zero"],
            "recommended_next": next_edge,
            "recommended_second": "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET_V0",
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "target_design": rel(TARGET_DESIGN_PATH),
            "objective_contract": rel(OBJECTIVE_CONTRACT_PATH),
            "source_scope_contract": rel(SOURCE_SCOPE_CONTRACT_PATH),
            "required_field_contract": rel(FIELD_CONTRACT_PATH),
            "candidate_handle_contract": rel(CANDIDATE_HANDLE_CONTRACT_PATH),
            "output_artifact_contract": rel(OUTPUT_ARTIFACT_CONTRACT_PATH),
            "acceptance_gate_contract": rel(ACCEPTANCE_GATE_CONTRACT_PATH),
            "negative_control_contract": rel(NEGATIVE_CONTROL_CONTRACT_PATH),
            "terminal_contract": rel(TERMINAL_CONTRACT_PATH),
            "nonauthority_boundary": rel(NONAUTHORITY_BOUNDARY_PATH),
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
    print(f"o1_target_design_receipt_id={receipt_id}")
    print(f"o1_target_design_receipt_path={rel(receipt_path)}")
    print(f"o1_target_design_path={rel(TARGET_DESIGN_PATH)}")
    print(f"o1_objective_contract_path={rel(OBJECTIVE_CONTRACT_PATH)}")
    print(f"o1_source_scope_contract_path={rel(SOURCE_SCOPE_CONTRACT_PATH)}")
    print(f"o1_required_field_contract_path={rel(FIELD_CONTRACT_PATH)}")
    print(f"o1_acceptance_gate_contract_path={rel(ACCEPTANCE_GATE_CONTRACT_PATH)}")
    print(f"o1_negative_control_contract_path={rel(NEGATIVE_CONTROL_CONTRACT_PATH)}")
    print(f"o1_build_unit_authorization_path={rel(BUILD_UNIT_AUTHORIZATION_PATH)}")
    print(f"o1_target_design_rollup_path={rel(ROLLUP_PATH)}")
    print(f"o1_target_design_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
