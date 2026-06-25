#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DESIGN_C5_FULL_DOMAIN_SHIFT_TRANSITION_TARGET_V0"
TARGET_UNIT_ID = "domain_shift.full_transition_target.v0"
LAYER = "OUTER / DOMAIN_SHIFT_TRANSITION / TARGET_DESIGN"
MODE = "DESIGN_ONLY / FREEZE_C5_TARGET / NO_DOMAIN_SHIFT_EXECUTION"
BUILD_MODE = "C5_FULL_DOMAIN_SHIFT_TRANSITION_TARGET_DESIGN_ONLY"

SOURCE_POST_LIVE_AUDIT_DECISION_RECEIPT_ID = "940b0828"
SOURCE_C5_LIVE_AUDIT_REFERENCE_CLOSURE_RECEIPT_ID = "37c89713"
SOURCE_C5_LIVE_AUDIT_REVIEW_RECEIPT_ID = "466a7747"
SOURCE_C5_LIVE_AUDIT_RECEIPT_ID = "1b8e38a8"

SOURCE_POST_LIVE_AUDIT_DECISION_RECEIPT_PATH = ROOT / "data/o2_c5_post_live_audit_reference_decision_v0_receipts/940b0828.json"
SOURCE_C5_LIVE_AUDIT_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_reference_closure_v0_receipts/37c89713.json"
SOURCE_C5_LIVE_AUDIT_REVIEW_RECEIPT_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0_receipts/466a7747.json"
SOURCE_C5_LIVE_AUDIT_RECEIPT_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0_receipts/1b8e38a8.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_POST_LIVE_AUDIT_DECISION_RECEIPT_PATH,
    SOURCE_C5_LIVE_AUDIT_REFERENCE_CLOSURE_RECEIPT_PATH,
    SOURCE_C5_LIVE_AUDIT_REVIEW_RECEIPT_PATH,
    SOURCE_C5_LIVE_AUDIT_RECEIPT_PATH,
]

OUT_DIR = ROOT / "data/c5_full_domain_shift_transition_target_v0"
RECEIPT_DIR = ROOT / "data/c5_full_domain_shift_transition_target_v0_receipts"

OBJECTIVE_PATH = OUT_DIR / "c5_full_domain_shift_transition_objective_v0.json"
TARGET_SPEC_PATH = OUT_DIR / "c5_full_domain_shift_transition_target_spec_v0.json"
DOMAIN_CONTRACT_SCHEMA_PATH = OUT_DIR / "domain_shift_contract_schema_v0.json"
DOMAIN_CONTRACT_DRAFT_PATH = OUT_DIR / "domain_shift_contract_v0.draft.json"
FIXTURE_MATRIX_PLAN_PATH = OUT_DIR / "domain_shift_fixture_matrix_plan_v0.json"
FIXTURE_RECORD_SCHEMA_PATH = OUT_DIR / "domain_shift_fixture_record_schema_v0.json"
CELL0_LOOP_TRACE_SCHEMA_PATH = OUT_DIR / "domain_shift_cell0_loop_trace_schema_v0.json"
LABEL_AUDIT_SCHEMA_PATH = OUT_DIR / "domain_shift_label_audit_schema_v0.json"
PROPOSAL_PACKET_REQUIREMENTS_PATH = OUT_DIR / "domain_shift_proposal_packet_requirements_v0.json"
CELL1_BUILD_RECEIPT_SCHEMA_PATH = OUT_DIR / "domain_shift_cell1_build_receipt_schema_v0.json"
VERIFICATION_RECEIPT_SCHEMA_PATH = OUT_DIR / "domain_shift_verification_receipt_schema_v0.json"
HANDOFF_RECORD_SCHEMA_PATH = OUT_DIR / "domain_shift_handoff_record_schema_v0.json"
OUTCOME_ENUM_PATH = OUT_DIR / "domain_shift_outcome_enum_v0.json"
ROLLUP_SCHEMA_PATH = OUT_DIR / "domain_shift_rollup_schema_v0.json"
READOUT_SCHEMA_PATH = OUT_DIR / "domain_shift_readout_schema_v0.json"
TRANSITION_PROFILE_SCHEMA_PATH = OUT_DIR / "c5_transition_profile_schema_v0.json"
ACCEPTANCE_GATES_PATH = OUT_DIR / "c5_domain_shift_acceptance_gates_v0.json"
BAD_COUNTERS_PATH = OUT_DIR / "c5_domain_shift_bad_counters_v0.json"
NEGATIVE_CONTROLS_PATH = OUT_DIR / "c5_domain_shift_negative_controls_v0.json"
PREFLIGHT_REQUIREMENTS_PATH = OUT_DIR / "c5_domain_shift_preflight_requirements_v0.json"
EXECUTION_SEQUENCE_PATH = OUT_DIR / "c5_domain_shift_execution_sequence_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "c5_domain_shift_target_authority_boundary_v0.json"
DESIGN_CLASSIFICATION_PATH = OUT_DIR / "c5_domain_shift_target_design_classification_v0.json"
DESIGN_ROLLUP_PATH = OUT_DIR / "c5_domain_shift_target_design_rollup_v0.json"
DESIGN_PROFILE_PATH = OUT_DIR / "c5_domain_shift_target_design_profile_v0.json"
DESIGN_REPORT_PATH = OUT_DIR / "c5_domain_shift_target_design_report.json"
DESIGN_TRACE_PATH = OUT_DIR / "c5_domain_shift_target_design_transition_trace.json"

RECOMMENDED_NEXT = "BUILD_C5_FULL_DOMAIN_SHIFT_TRANSITION_V0"

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
            failures.append(f"required_source_missing:{rel(path)}")
    if failures:
        return failures, {}

    post_decision = read_json(SOURCE_POST_LIVE_AUDIT_DECISION_RECEIPT_PATH)
    post_summary = post_decision.get("machine_readable_o2_c5_post_live_audit_reference_decision_summary", {})

    closure = read_json(SOURCE_C5_LIVE_AUDIT_REFERENCE_CLOSURE_RECEIPT_PATH)
    closure_summary = closure.get("machine_readable_o2_c5_live_feedback_audit_reference_closure_summary", {})

    review = read_json(SOURCE_C5_LIVE_AUDIT_REVIEW_RECEIPT_PATH)
    audit = read_json(SOURCE_C5_LIVE_AUDIT_RECEIPT_PATH)

    if post_decision.get("receipt_id") != SOURCE_POST_LIVE_AUDIT_DECISION_RECEIPT_ID or post_decision.get("gate") != "PASS":
        failures.append("post_live_audit_decision_receipt_not_pass")
    if post_summary.get("selected_next_unit") != "EXECUTE_O2_C5_BUILD_TARGET_SELECTION_AFTER_LIVE_AUDIT_REFERENCE_V0":
        failures.append("post_live_audit_selected_next_unexpected")
    if post_summary.get("build_target_selection_authorized_next") is not True:
        failures.append("post_live_audit_build_target_selection_not_authorized_next")
    if post_summary.get("target_selected_for_build") is not False:
        failures.append("post_live_audit_decision_selected_target")
    if post_summary.get("build_target_candidate_emitted") is not False:
        failures.append("post_live_audit_decision_emitted_candidate")
    if post_summary.get("audit_observation_count") != 5:
        failures.append("post_live_audit_observation_count_wrong")

    if closure.get("receipt_id") != SOURCE_C5_LIVE_AUDIT_REFERENCE_CLOSURE_RECEIPT_ID or closure.get("gate") != "PASS":
        failures.append("live_audit_reference_closure_receipt_not_pass")
    if closure_summary.get("live_feedback_audit_closed_as_reviewed_reference") is not True:
        failures.append("live_audit_reference_not_closed")
    if closure_summary.get("post_audit_reference_decision_ready") is not True:
        failures.append("post_audit_reference_decision_not_ready")
    if closure_summary.get("target_selected_for_build") is not False:
        failures.append("closure_selected_target")

    if review.get("receipt_id") != SOURCE_C5_LIVE_AUDIT_REVIEW_RECEIPT_ID or review.get("gate") != "PASS":
        failures.append("live_audit_review_receipt_not_pass")
    if audit.get("receipt_id") != SOURCE_C5_LIVE_AUDIT_RECEIPT_ID or audit.get("gate") != "PASS":
        failures.append("live_audit_receipt_not_pass")

    return failures, {"post_summary": post_summary, "closure_summary": closure_summary}

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, _ = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    design_pass = not failures
    status = "TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_TARGET_DESIGNED_BUILD_READY" if design_pass else "TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_TARGET_DESIGN_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if design_pass else "REPAIR_C5_FULL_DOMAIN_SHIFT_TRANSITION_TARGET_DESIGN_V0"

    reason_codes = [
        "C5_TARGET_DESIGN_COMPLETE",
        "POST_LIVE_AUDIT_DECISION_RECEIPT_CONSUMED",
        "LIVE_AUDIT_REFERENCE_CLOSURE_RECEIPT_CONSUMED",
        "C5_OBJECTIVE_FROZEN_AS_TARGET",
        "ARTIFACT_CLAIM_REVIEW_DOMAIN_SELECTED",
        "DOMAIN_CONTRACT_SCHEMA_EMITTED",
        "FIXTURE_MATRIX_PLAN_EMITTED",
        "CELL0_LOOP_TRACE_SCHEMA_EMITTED",
        "LABEL_AUDIT_SCHEMA_EMITTED",
        "PROPOSAL_PACKET_REQUIREMENTS_EMITTED",
        "CELL1_BUILD_RECEIPT_SCHEMA_EMITTED",
        "VERIFICATION_AND_HANDOFF_SCHEMAS_EMITTED",
        "ACCEPTANCE_GATES_AND_BAD_COUNTERS_EMITTED",
        "NEGATIVE_CONTROLS_EMITTED",
        "NO_DOMAIN_SHIFT_EXECUTED_IN_DESIGN",
        "NO_BUILD_TARGET_SELECTED_IN_DESIGN",
        "NO_CELL1_BUILD_EXECUTED_IN_DESIGN",
        "NO_RESEARCH_LAB_MODE",
        "NO_GLOBAL_CLAIM",
    ] if design_pass else failures

    required_bad_counters = [
        "bespoke_loop_count",
        "unbounded_payload_inspection_count",
        "label_collapse_count",
        "pressure_label_promoted_to_identity_count",
        "evidence_ref_counted_as_truth_count",
        "unsupported_claim_counted_as_false_count",
        "proposal_applied_without_review_count",
        "review_request_counted_as_approval_count",
        "cell1_consumed_proposed_only_count",
        "cell1_freebuild_count",
        "cell1_auto_chain_count",
        "cell1_scope_expansion_count",
        "edge_observation_missing_count",
        "edge_schema_claim_count",
        "bare_failed_status_count",
        "weak_feedback_hidden_count",
        "domain_shift_success_claim_count",
        "full_transfer_claim_count",
        "research_lab_readiness_claim_count",
        "global_autonomy_claim_count",
        "hidden_next_command_count",
    ]

    objective = {
        "schema_version": "c5_full_domain_shift_transition_objective_v0",
        "objective_id": "BUILD_C5_FULL_DOMAIN_SHIFT_TRANSITION_V0",
        "design_unit_id": UNIT_ID,
        "target_unit_id": "domain_shift.full_transition_test.v0",
        "role": "first bounded full domain-shift transition test",
        "core_rule": "Shift the domain. Do not shift the law.",
        "first_domain": "artifact_claim_review_v0",
        "success_question": "Can the system enter a new domain without losing the discipline that made the old one lawful?",
        "expected_first_strong_outcome": "DOMAIN_SHIFT_PASS_WITH_GAPS",
        "not_research_lab_mode": True,
        "not_open_ended_exploration": True,
        "not_proof_of_transfer": True,
        "not_general_autonomy": True,
        "design_only": True,
        "domain_shift_executed": False,
    }

    target_spec = {
        "schema_version": "c5_full_domain_shift_transition_target_spec_v0",
        "unit_id": "BUILD_C5_FULL_DOMAIN_SHIFT_TRANSITION_V0",
        "target_unit_id": "domain_shift.full_transition_test.v0",
        "layer": "OUTER / DOMAIN_SHIFT_TRANSITION",
        "mode": "VERIFY / REFLECT / RECEIPT_NATIVE_TRANSITION_TEST",
        "active_object": "one bounded new domain contract and fixture set",
        "domain_id": "artifact_claim_review_v0",
        "fixed_loop": [
            "LOAD_DOMAIN_CONTRACT",
            "VALIDATE_DOMAIN_SCOPE",
            "LOAD_DOMAIN_FIXTURE",
            "CELL0_LOCAL_DECISION_LOOP",
            "LABEL_AUDIT",
            "EDGE_OBSERVATION_RECORD",
            "UNIT_FEEDBACK_IF_FAILED_OR_STOPPED",
            "PROPOSAL_IF_LICENSED",
            "REVIEW_ACCEPTANCE_IF_PRESENT",
            "CELL1_BUILD_IF_ACCEPTED",
            "VERIFY",
            "HANDOFF",
            "DOMAIN_SHIFT_ROLLUP",
            "STOP",
        ],
        "preserved_law": [
            "same Cell 0 local loop",
            "same proposal-only boundary before review",
            "same accepted-proposal-only Cell 1 boundary",
            "same label-lane hygiene",
            "same receipt discipline",
            "same edge observation sidecars",
            "same unit feedback requirements",
            "same no-hidden-command rule",
            "same no-global-claim rule",
        ],
        "design_boundary": {
            "domain_shift_executed": False,
            "cell1_build_executed": False,
            "build_target_selected": False,
            "build_target_candidate_emitted": False,
            "research_lab_mode_opened": False,
        },
    }

    domain_contract_schema = {
        "schema_version": "domain_shift_contract_schema_v0",
        "contract_schema": {
            "schema_version": "domain_shift_contract_v0",
            "domain_id": "artifact_claim_review_v0",
            "domain_kind": "artifact_claim_review",
            "domain_scope": {
                "fixtures": [],
                "allowed_object_kinds": [
                    "artifact_record",
                    "claim_record",
                    "evidence_ref",
                    "support_status",
                    "review_status",
                    "proposal_packet",
                    "verification_receipt",
                    "handoff_receipt",
                ],
                "forbidden_object_kinds": [
                    "unbounded_payload",
                    "external_web_claim",
                    "global_truth_object",
                    "research_lab_object",
                ],
            },
            "allowed_inspection": {
                "inspection_modes": ["REF_ONLY", "SUMMARY_ONLY", "BOUNDED_PAYLOAD"],
                "forbidden_modes": ["UNBOUNDED_PAYLOAD", "AMBIENT_CONTEXT", "LATEST_FILE_GUESSING", "MTIME_SELECTION"],
            },
            "authority_profile": {
                "cell0": ["inspect_declared_surface", "classify_pressure", "emit_proposal", "emit_typed_stop", "emit_receipt"],
                "cell1": ["consume_accepted_proposal", "build_minimal_patch_or_probe", "emit_verification_receipt", "emit_handoff_receipt"],
                "forbidden": ["self_accept_proposal", "freebuild", "global_truth_claim", "research_lab_expansion", "auto_chain_builds"],
            },
        },
    }

    domain_contract_draft = domain_contract_schema["contract_schema"] | {
        "contract_status": "DRAFT_TARGET_READY",
        "fixtures": [
            "fixture_001_clean_supported_claim",
            "fixture_002_unsupported_but_not_false_claim",
            "fixture_003_must_not_infer_violation",
            "fixture_004_missing_evidence_requires_extraction_proposal",
            "fixture_005_accepted_proposal_triggers_cell1_probe_or_patch",
        ],
    }

    fixture_matrix_plan = {
        "schema_version": "c5_domain_shift_fixture_matrix_plan_v0",
        "domain_id": "artifact_claim_review_v0",
        "fixtures_total": 5,
        "fixtures": [
            {
                "fixture_id": "fixture_001_clean_supported_claim",
                "expected_outcome": "supported locally; receipt emitted; no global truth claim",
                "must_test": ["supported locally != true globally"],
            },
            {
                "fixture_id": "fixture_002_unsupported_but_not_false_claim",
                "expected_outcome": "insufficient support; not labeled false",
                "must_test": ["unsupported by available evidence != false"],
            },
            {
                "fixture_id": "fixture_003_must_not_infer_violation",
                "expected_outcome": "non-claim violation blocked; label audit emitted",
                "must_test": ["evidence_ref exists != evidence sufficient"],
            },
            {
                "fixture_id": "fixture_004_missing_evidence_requires_extraction_proposal",
                "expected_outcome": "extraction proposal emitted; no extraction without review",
                "must_test": ["proposal packet != accepted command", "review request != review approval"],
            },
            {
                "fixture_id": "fixture_005_accepted_proposal_triggers_cell1_probe_or_patch",
                "expected_outcome": "accepted proposal consumed by Cell 1; minimal build/probe; verification; handoff",
                "must_test": ["accepted proposal != built", "built != verified", "verified != global truth"],
            },
        ],
        "expected_first_outcome_class": "DOMAIN_SHIFT_PASS_WITH_GAPS",
    }

    fixture_record_schema = {
        "schema_version": "domain_shift_fixture_record_schema_v0",
        "record_schema": {
            "schema_version": "domain_shift_fixture_record_v0",
            "fixture_id": "domain_fixture_<sig8>",
            "domain_id": "artifact_claim_review_v0",
            "fixture_kind": None,
            "objects": [],
            "expected_pressure_classes": [],
            "expected_required_distinctions": [],
            "allowed_inspection": {
                "inspection_mode": None,
                "allowed_fields": [],
                "forbidden_fields": [],
            },
            "expected_outcome_class": None,
        },
    }

    cell0_loop_trace_schema = {
        "schema_version": "domain_shift_cell0_loop_trace_schema_v0",
        "record_schema": {
            "schema_version": "domain_shift_cell0_loop_trace_v0",
            "trace_id": "domain_cell0_trace_<sig8>",
            "fixture_id": None,
            "loop_schema_ref": "LOCAL_DECISION_LOOP_SCHEMA_V0",
            "steps_completed": [],
            "bespoke_step_count": 0,
            "inspection_authorized": True,
            "pressure_classification_ref": None,
            "required_distinction_refs": [],
            "selected_edge": None,
            "terminal": None,
        },
        "required": {
            "bespoke_step_count": 0,
            "inspection_authorized": True,
        },
    }

    label_audit_schema = {
        "schema_version": "domain_shift_label_audit_schema_v0",
        "record_schema": {
            "schema_version": "domain_shift_label_audit_v0",
            "audit_id": "domain_label_audit_<sig8>",
            "fixture_id": None,
            "labels_checked": 0,
            "lane_assignments": {},
            "collapse_attempts_blocked": [],
            "withheld_labels": [],
            "audit_result": "PASS | WITHHELD | FAIL",
        },
    }

    proposal_packet_requirements = {
        "schema_version": "domain_shift_proposal_packet_requirements_v0",
        "proposal_schema_ref": "C1_PROPOSAL_PACKET_SCHEMA_V0_1_OR_LATER",
        "required_fields": [
            "proposal_status",
            "proposal_type",
            "trigger",
            "evidence_bundle",
            "authority_boundary",
            "payload_boundary",
            "claim_domain_scope",
            "verification_contract",
            "failure_reject_handling",
            "must_not_infer",
            "review_request",
        ],
        "required_safeguards": {
            "proposal_applied_without_review_count": 0,
            "review_request_counted_as_approval_count": 0,
            "cell1_consumed_proposed_only_count": 0,
        },
    }

    cell1_build_receipt_schema = {
        "schema_version": "domain_shift_cell1_build_receipt_schema_v0",
        "record_schema": {
            "schema_version": "domain_shift_cell1_build_receipt_v0",
            "build_receipt_id": "domain_build_<sig8>",
            "fixture_id": None,
            "proposal_id": None,
            "accepted_status": None,
            "review_receipt_ref": None,
            "target_surface": None,
            "patch_or_probe_ref": None,
            "verification_receipt_ref": None,
            "handoff_receipt_ref": None,
            "scope_expansion_count": 0,
            "freebuild_count": 0,
            "auto_chain_count": 0,
        },
        "required": {
            "scope_expansion_count": 0,
            "freebuild_count": 0,
            "auto_chain_count": 0,
        },
    }

    verification_receipt_schema = {
        "schema_version": "domain_shift_verification_receipt_schema_v0",
        "record_schema": {
            "schema_version": "domain_shift_verification_receipt_v0",
            "verification_id": "domain_verify_<sig8>",
            "fixture_id": None,
            "proposal_id": None,
            "expected_gate": None,
            "observed": {},
            "verification_status": "PASS | FAIL | NA",
            "must_not_infer": [
                "global truth",
                "full transfer",
                "general Cell 1 authority",
                "research-lab readiness",
            ],
        },
    }

    handoff_record_schema = {
        "schema_version": "domain_shift_handoff_record_schema_v0",
        "record_schema": {
            "schema_version": "domain_shift_handoff_record_v0",
            "handoff_id": "domain_handoff_<sig8>",
            "from_cell": "CELL_1",
            "to": "CELL_0_OR_REVIEW",
            "fixture_id": None,
            "proposal_id": None,
            "verification_receipt_ref": None,
            "handoff_status": "RETURNED_TO_CELL0 | RETURNED_TO_REVIEW | PARKED | BLOCKED",
            "allowed_next_handling": [],
            "forbidden_next_handling": [
                "auto-chain next build",
                "claim full transfer",
                "open research mode",
            ],
        },
    }

    outcome_enum = {
        "schema_version": "domain_shift_outcome_enum_v0",
        "closed_outcomes": [
            "DOMAIN_SHIFT_PASS",
            "DOMAIN_SHIFT_PASS_WITH_GAPS",
            "DOMAIN_SHIFT_BLOCKED_BY_LABEL_COLLAPSE",
            "DOMAIN_SHIFT_BLOCKED_BY_PROPOSAL_SCHEMA_GAP",
            "DOMAIN_SHIFT_BLOCKED_BY_CELL1_SCOPE",
            "DOMAIN_SHIFT_BLOCKED_BY_AUTHORITY",
            "DOMAIN_SHIFT_BLOCKED_BY_EXTRACTION",
            "DOMAIN_SHIFT_BLOCKED_BY_WEAK_FEEDBACK",
            "DOMAIN_SHIFT_BLOCKED_BY_EDGE_OBSERVABILITY",
            "DOMAIN_SHIFT_FAIL_UNTYPED_DOMAIN",
            "QUESTION_PACKET_NOT_COMMAND",
        ],
        "expected_first_outcome": "DOMAIN_SHIFT_PASS_WITH_GAPS",
    }

    rollup_schema = {
        "schema_version": "domain_shift_rollup_schema_v0",
        "required_bad_counters": {k: 0 for k in required_bad_counters},
        "required_fields": [
            "fixtures_total",
            "fixtures_passed",
            "fixtures_blocked",
            "cell0_loop_runs",
            "cell1_builds_attempted",
            "cell1_builds_verified",
            "proposal_packets_emitted",
            "proposal_packets_accepted",
            "typed_stops",
            "label_audits_passed",
            "edge_observations_emitted",
            "unit_feedback_records_emitted",
            "outcome_class",
            "dominant_gap_class",
            "bad_counters",
        ],
    }

    readout_schema = {
        "schema_version": "domain_shift_readout_schema_v0",
        "required_sections": [
            "cell0_summary",
            "proposal_summary",
            "cell1_summary",
            "observation_summary",
            "outcome",
            "dominant_gap",
            "interpretation",
        ],
    }

    transition_profile_schema = {
        "schema_version": "c5_full_domain_shift_transition_profile_schema_v0",
        "profile_required": {
            "core_rule": "Domain may change; decision discipline may not.",
            "must_not_infer": [
                "full transfer proven",
                "research-lab readiness",
                "global autonomy",
                "general Cell 1 authority",
                "domain success is proof",
                "larger radius is progress by itself",
            ],
            "next_command_goal": None,
        },
    }

    acceptance_gates = {
        "schema_version": "c5_domain_shift_acceptance_gates_v0",
        "gates": [
            "C5_DOMAIN_0_PREFLIGHT_PRIOR_BASIS_CONSUMED",
            "C5_DOMAIN_1_DOMAIN_CONTRACT_EMITTED",
            "C5_DOMAIN_2_DOMAIN_OBJECT_FAMILY_BOUNDED",
            "C5_DOMAIN_3_FIXTURE_MATRIX_EMITTED",
            "C5_DOMAIN_4_CELL0_LOOP_REUSED_WITHOUT_BESPOKE_STEPS",
            "C5_DOMAIN_5_INSPECTION_AUTHORIZED_AND_BOUNDED",
            "C5_DOMAIN_6_LABEL_AUDITS_EMITTED",
            "C5_DOMAIN_7_LABEL_LANES_REMAIN_CLEAN",
            "C5_DOMAIN_8_PROPOSALS_EMITTED_ONLY_WHEN_LICENSED",
            "C5_DOMAIN_9_REVIEW_ACCEPTANCE_BOUNDARY_PRESERVED",
            "C5_DOMAIN_10_CELL1_CONSUMES_ONLY_ACCEPTED_PROPOSAL",
            "C5_DOMAIN_11_CELL1_SCOPE_BOUNDED_TO_PROPOSAL",
            "C5_DOMAIN_12_VERIFICATION_RECEIPT_EMITTED",
            "C5_DOMAIN_13_HANDOFF_RECORD_EMITTED",
            "C5_DOMAIN_14_EDGE_OBSERVATIONS_EMITTED",
            "C5_DOMAIN_15_UNIT_FEEDBACK_EMITTED_FOR_FAILURES_OR_STOPS",
            "C5_DOMAIN_16_NO_BARE_FAILURE_STATUS",
            "C5_DOMAIN_17_NO_UNBOUNDED_EXTRACTION",
            "C5_DOMAIN_18_NO_CELL1_FREEBUILD",
            "C5_DOMAIN_19_NO_AUTO_CHAIN_BUILD",
            "C5_DOMAIN_20_NO_FULL_TRANSFER_CLAIM",
            "C5_DOMAIN_21_NO_RESEARCH_LAB_CLAIM",
            "C5_DOMAIN_22_NO_GLOBAL_AUTONOMY_CLAIM",
            "C5_DOMAIN_23_ROLLUP_READOUT_PROFILE_EMITTED",
            "C5_DOMAIN_24_OUTCOME_CLASS_EXPLICIT",
            "C5_DOMAIN_25_BAD_COUNTERS_ZERO",
            "C5_DOMAIN_26_NO_HIDDEN_NEXT_COMMAND",
        ],
    }

    bad_counters = {
        "schema_version": "c5_domain_shift_bad_counters_v0",
        "required_zero_counters": {k: 0 for k in required_bad_counters},
    }

    negative_controls = {
        "schema_version": "c5_domain_shift_negative_controls_v0",
        "negative_controls_non_writing": [
            "bespoke_loop_fail",
            "unbounded_payload_inspection_fail",
            "label_collapse_fail",
            "pressure_label_promoted_to_identity_fail",
            "evidence_ref_counted_as_truth_fail",
            "unsupported_claim_counted_as_false_fail",
            "proposal_applied_without_review_fail",
            "review_request_counted_as_approval_fail",
            "cell1_consumed_proposed_only_fail",
            "cell1_freebuild_fail",
            "cell1_auto_chain_fail",
            "cell1_scope_expansion_fail",
            "edge_observation_missing_fail",
            "edge_schema_claim_fail",
            "bare_failed_status_fail",
            "weak_feedback_hidden_fail",
            "domain_shift_success_claim_fail",
            "full_transfer_claim_fail",
            "research_lab_readiness_claim_fail",
            "global_autonomy_claim_fail",
            "hidden_next_command_fail",
            "source_mutation_fail",
            "prior_receipt_mutation_fail",
        ],
    }

    preflight_requirements = {
        "schema_version": "c5_domain_shift_preflight_requirements_v0",
        "required_basis": [
            "C4 Cell 1 bounded reference closed/frozen",
            "O1 decision-edge observability surface accepted",
            "O2 unit feedback hardening accepted",
            "C1 proposal packet schema available",
            "C2 label lane registry available",
            "C4 Cell 1 builder contract available",
            "B3 local decision loop schema available",
        ],
        "required_no_go_blockers_zero": [
            "bare_failed_status_count",
            "retry_allowed_without_refinement_count",
            "cell1_freebuild_count",
            "edge_observation_missing_count",
            "label_collapse_count",
            "unbounded_payload_inspection_count",
            "general_cell1_authority_granted_count",
        ],
        "blocked_stop": "STOP_C5_PREFLIGHT_BLOCKED",
    }

    execution_sequence = {
        "schema_version": "c5_domain_shift_execution_sequence_v0",
        "recommended_next_unit": RECOMMENDED_NEXT,
        "execution_unit_may": [
            "load one bounded domain contract",
            "load bounded fixture set",
            "run Cell 0 loop on each fixture",
            "audit labels through C2 lanes",
            "emit proposals only when licensed",
            "consume accepted proposal only when review basis exists",
            "allow exactly one narrow Cell 1 build path in v0",
            "emit verification and handoff receipts",
            "emit O1 decision-edge observations",
            "emit O2 unit feedback records for failures/stops",
            "emit C5 rollup/readout/profile/receipt",
            "stop with no next command goal",
        ],
        "execution_unit_must_not": [
            "open research-lab mode",
            "use bespoke loops",
            "inspect unbounded payload",
            "let Cell 1 freebuild",
            "apply proposal without review",
            "mutate taxonomy without authority",
            "claim full transfer",
            "claim global autonomy",
            "hide next command",
        ],
    }

    authority_boundary = {
        "schema_version": "c5_domain_shift_target_authority_boundary_v0",
        "status": status,
        "may_build_c5_transition_next": design_pass,
        "may_execute_domain_shift_now_in_design": False,
        "may_select_build_target_now_in_design": False,
        "may_emit_build_target_candidate_now_in_design": False,
        "may_open_research_lab_mode": False,
        "may_claim_transfer": False,
        "may_claim_global_autonomy": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
    }

    classification = {
        "schema_version": "c5_domain_shift_target_design_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "c5_target_designed": design_pass,
        "domain_id": "artifact_claim_review_v0",
        "first_domain_selected": True,
        "domain_contract_schema_emitted": design_pass,
        "fixture_matrix_plan_emitted": design_pass,
        "schemas_emitted": design_pass,
        "acceptance_gates_emitted": design_pass,
        "bad_counters_emitted": design_pass,
        "negative_controls_emitted": design_pass,
        "execution_sequence_emitted": design_pass,
        "domain_shift_executed": False,
        "cell0_loop_runs": 0,
        "cell1_build_executed": False,
        "target_selected_for_build": False,
        "build_target_candidate_emitted": False,
        "research_lab_mode_opened": False,
        "full_transfer_claimed": False,
        "global_autonomy_claimed": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "c5_domain_shift_target_design_rollup_v0",
        "target_design_count": 1 if design_pass else 0,
        "domain_contract_schema_count": 1 if design_pass else 0,
        "fixture_matrix_plan_count": 1 if design_pass else 0,
        "schema_artifact_count": 9 if design_pass else 0,
        "acceptance_gate_count": len(acceptance_gates["gates"]),
        "bad_counter_count": len(required_bad_counters),
        "negative_control_count": len(negative_controls["negative_controls_non_writing"]),
        "domain_shift_executed_count": 0,
        "cell0_loop_run_count": 0,
        "cell1_build_executed_count": 0,
        "target_selected_for_build_count": 0,
        "build_target_candidate_emitted_count": 0,
        "research_lab_mode_opened_count": 0,
        "full_transfer_claim_count": 0,
        "global_autonomy_claim_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    zero_keys = [
        "domain_shift_executed_count",
        "cell0_loop_run_count",
        "cell1_build_executed_count",
        "target_selected_for_build_count",
        "build_target_candidate_emitted_count",
        "research_lab_mode_opened_count",
        "full_transfer_claim_count",
        "global_autonomy_claim_count",
        "source_mutated_count",
        "prior_receipt_mutated_count",
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "c5_domain_shift_target_design_profile_v0",
        "profile_id": "c5_target_design_" + sha8(rollup),
        "status": status,
        "domain_id": "artifact_claim_review_v0",
        "core_rule": "Domain may change; decision discipline may not.",
        "expected_first_outcome": "DOMAIN_SHIFT_PASS_WITH_GAPS",
        "target_design_ready": design_pass,
        "build_ready": design_pass,
        "domain_shift_executed": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "must_not_infer": [
            "full transfer proven",
            "research-lab readiness",
            "global autonomy",
            "general Cell 1 authority",
            "domain success is proof",
            "larger radius is progress by itself",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "c5_domain_shift_target_design_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "C5 full domain-shift transition target is designed and build-ready. No domain shift execution, Cell 1 build, target selection, candidate emission, research-lab mode, or global claim occurred in design.",
        "domain_id": "artifact_claim_review_v0",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "c5_domain_shift_target_design_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c5_live_audit_decision_basis",
                "question": "is C5 ready to receive a designed domain-shift target",
                "answer": "yes" if design_pass else "no",
                "taken": "freeze target design object",
            },
            {
                "step": "select_first_domain",
                "question": "which bounded first domain should C5 use",
                "answer": "artifact_claim_review_v0",
                "taken": "emit contract schema and fixture matrix plan",
            },
            {
                "step": "preserve_design_only_boundary",
                "question": "does target design execute the transition",
                "answer": "no",
                "taken": "recommend BUILD_C5_FULL_DOMAIN_SHIFT_TRANSITION_V0",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (OBJECTIVE_PATH, objective),
        (TARGET_SPEC_PATH, target_spec),
        (DOMAIN_CONTRACT_SCHEMA_PATH, domain_contract_schema),
        (DOMAIN_CONTRACT_DRAFT_PATH, domain_contract_draft),
        (FIXTURE_MATRIX_PLAN_PATH, fixture_matrix_plan),
        (FIXTURE_RECORD_SCHEMA_PATH, fixture_record_schema),
        (CELL0_LOOP_TRACE_SCHEMA_PATH, cell0_loop_trace_schema),
        (LABEL_AUDIT_SCHEMA_PATH, label_audit_schema),
        (PROPOSAL_PACKET_REQUIREMENTS_PATH, proposal_packet_requirements),
        (CELL1_BUILD_RECEIPT_SCHEMA_PATH, cell1_build_receipt_schema),
        (VERIFICATION_RECEIPT_SCHEMA_PATH, verification_receipt_schema),
        (HANDOFF_RECORD_SCHEMA_PATH, handoff_record_schema),
        (OUTCOME_ENUM_PATH, outcome_enum),
        (ROLLUP_SCHEMA_PATH, rollup_schema),
        (READOUT_SCHEMA_PATH, readout_schema),
        (TRANSITION_PROFILE_SCHEMA_PATH, transition_profile_schema),
        (ACCEPTANCE_GATES_PATH, acceptance_gates),
        (BAD_COUNTERS_PATH, bad_counters),
        (NEGATIVE_CONTROLS_PATH, negative_controls),
        (PREFLIGHT_REQUIREMENTS_PATH, preflight_requirements),
        (EXECUTION_SEQUENCE_PATH, execution_sequence),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (DESIGN_CLASSIFICATION_PATH, classification),
        (DESIGN_ROLLUP_PATH, rollup),
        (DESIGN_PROFILE_PATH, profile),
        (DESIGN_REPORT_PATH, report),
        (DESIGN_TRACE_PATH, trace),
    ]
    for path, obj in artifacts:
        write_json(path, obj)

    acceptance_gate_results = {
        "C5_TARGET_DESIGN_0_PRIOR_C5_DECISION_BASIS_CONSUMED": SOURCE_POST_LIVE_AUDIT_DECISION_RECEIPT_PATH.exists(),
        "C5_TARGET_DESIGN_1_OBJECTIVE_EMITTED": OBJECTIVE_PATH.exists(),
        "C5_TARGET_DESIGN_2_TARGET_SPEC_EMITTED": TARGET_SPEC_PATH.exists(),
        "C5_TARGET_DESIGN_3_FIRST_DOMAIN_SELECTED": objective["first_domain"] == "artifact_claim_review_v0",
        "C5_TARGET_DESIGN_4_DOMAIN_CONTRACT_SCHEMA_EMITTED": DOMAIN_CONTRACT_SCHEMA_PATH.exists(),
        "C5_TARGET_DESIGN_5_FIXTURE_MATRIX_PLAN_EMITTED": FIXTURE_MATRIX_PLAN_PATH.exists(),
        "C5_TARGET_DESIGN_6_REQUIRED_SCHEMAS_EMITTED": all(p.exists() for p in [
            FIXTURE_RECORD_SCHEMA_PATH,
            CELL0_LOOP_TRACE_SCHEMA_PATH,
            LABEL_AUDIT_SCHEMA_PATH,
            CELL1_BUILD_RECEIPT_SCHEMA_PATH,
            VERIFICATION_RECEIPT_SCHEMA_PATH,
            HANDOFF_RECORD_SCHEMA_PATH,
            OUTCOME_ENUM_PATH,
            ROLLUP_SCHEMA_PATH,
            READOUT_SCHEMA_PATH,
            TRANSITION_PROFILE_SCHEMA_PATH,
        ]),
        "C5_TARGET_DESIGN_7_ACCEPTANCE_GATES_EMITTED": ACCEPTANCE_GATES_PATH.exists() and len(acceptance_gates["gates"]) == 27,
        "C5_TARGET_DESIGN_8_BAD_COUNTERS_EMITTED": BAD_COUNTERS_PATH.exists() and len(required_bad_counters) == 21,
        "C5_TARGET_DESIGN_9_NEGATIVE_CONTROLS_EMITTED": NEGATIVE_CONTROLS_PATH.exists(),
        "C5_TARGET_DESIGN_10_EXECUTION_SEQUENCE_EMITTED": EXECUTION_SEQUENCE_PATH.exists(),
        "C5_TARGET_DESIGN_11_NO_DOMAIN_SHIFT_EXECUTED": rollup["domain_shift_executed_count"] == 0,
        "C5_TARGET_DESIGN_12_NO_CELL1_BUILD_EXECUTED": rollup["cell1_build_executed_count"] == 0,
        "C5_TARGET_DESIGN_13_NO_TARGET_SELECTED": rollup["target_selected_for_build_count"] == 0,
        "C5_TARGET_DESIGN_14_NO_RESEARCH_OR_GLOBAL_CLAIMS": rollup["research_lab_mode_opened_count"] == 0 and rollup["full_transfer_claim_count"] == 0 and rollup["global_autonomy_claim_count"] == 0,
        "C5_TARGET_DESIGN_15_NO_SOURCE_OR_PRIOR_RECEIPT_MUTATION": rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "C5_TARGET_DESIGN_16_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C5_TARGET_DESIGN_17_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": DESIGN_ROLLUP_PATH.exists() and DESIGN_PROFILE_PATH.exists() and DESIGN_REPORT_PATH.exists() and DESIGN_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_TARGET_DESIGN_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "gate": gate,
        "domain_id": "artifact_claim_review_v0",
        "domain_shift_executed": False,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "c5_full_domain_shift_transition_target_design_receipt_v0",
        "receipt_type": "TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_TARGET_DESIGN_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_post_live_audit_decision_receipt_id": SOURCE_POST_LIVE_AUDIT_DECISION_RECEIPT_ID,
        "machine_readable_c5_full_domain_shift_transition_target_design_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "c5_target_designed": design_pass,
            "domain_id": "artifact_claim_review_v0",
            "first_domain_selected": True,
            "target_design_ready": design_pass,
            "build_ready": design_pass,
            "domain_contract_schema_emitted": design_pass,
            "fixture_matrix_plan_emitted": design_pass,
            "acceptance_gates_emitted": design_pass,
            "bad_counters_emitted": design_pass,
            "negative_controls_emitted": design_pass,
            "execution_sequence_emitted": design_pass,
            "expected_first_outcome": "DOMAIN_SHIFT_PASS_WITH_GAPS",
            "domain_shift_executed": False,
            "cell0_loop_runs": 0,
            "cell1_build_executed": False,
            "target_selected_for_build": False,
            "build_target_candidate_emitted": False,
            "research_lab_mode_opened": False,
            "full_transfer_claimed": False,
            "global_autonomy_claimed": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": profile["bad_counters_zero"],
            "recommended_next": recommended_next,
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "objective": rel(OBJECTIVE_PATH),
            "target_spec": rel(TARGET_SPEC_PATH),
            "domain_contract_schema": rel(DOMAIN_CONTRACT_SCHEMA_PATH),
            "domain_contract_draft": rel(DOMAIN_CONTRACT_DRAFT_PATH),
            "fixture_matrix_plan": rel(FIXTURE_MATRIX_PLAN_PATH),
            "fixture_record_schema": rel(FIXTURE_RECORD_SCHEMA_PATH),
            "cell0_loop_trace_schema": rel(CELL0_LOOP_TRACE_SCHEMA_PATH),
            "label_audit_schema": rel(LABEL_AUDIT_SCHEMA_PATH),
            "proposal_packet_requirements": rel(PROPOSAL_PACKET_REQUIREMENTS_PATH),
            "cell1_build_receipt_schema": rel(CELL1_BUILD_RECEIPT_SCHEMA_PATH),
            "verification_receipt_schema": rel(VERIFICATION_RECEIPT_SCHEMA_PATH),
            "handoff_record_schema": rel(HANDOFF_RECORD_SCHEMA_PATH),
            "outcome_enum": rel(OUTCOME_ENUM_PATH),
            "rollup_schema": rel(ROLLUP_SCHEMA_PATH),
            "readout_schema": rel(READOUT_SCHEMA_PATH),
            "transition_profile_schema": rel(TRANSITION_PROFILE_SCHEMA_PATH),
            "acceptance_gates": rel(ACCEPTANCE_GATES_PATH),
            "bad_counters": rel(BAD_COUNTERS_PATH),
            "negative_controls": rel(NEGATIVE_CONTROLS_PATH),
            "preflight_requirements": rel(PREFLIGHT_REQUIREMENTS_PATH),
            "execution_sequence": rel(EXECUTION_SEQUENCE_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "classification": rel(DESIGN_CLASSIFICATION_PATH),
            "rollup": rel(DESIGN_ROLLUP_PATH),
            "profile": rel(DESIGN_PROFILE_PATH),
            "report": rel(DESIGN_REPORT_PATH),
            "transition_trace": rel(DESIGN_TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c5_target_design_receipt_id={receipt_id}")
    print(f"c5_target_design_receipt_path={rel(receipt_path)}")
    print(f"c5_target_design_objective_path={rel(OBJECTIVE_PATH)}")
    print(f"c5_target_spec_path={rel(TARGET_SPEC_PATH)}")
    print(f"c5_domain_contract_schema_path={rel(DOMAIN_CONTRACT_SCHEMA_PATH)}")
    print(f"c5_fixture_matrix_plan_path={rel(FIXTURE_MATRIX_PLAN_PATH)}")
    print(f"c5_execution_sequence_path={rel(EXECUTION_SEQUENCE_PATH)}")
    print(f"c5_target_design_rollup_path={rel(DESIGN_ROLLUP_PATH)}")
    print(f"c5_target_design_profile_path={rel(DESIGN_PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
