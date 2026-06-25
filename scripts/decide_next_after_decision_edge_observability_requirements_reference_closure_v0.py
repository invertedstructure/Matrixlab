#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_AFTER_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REFERENCE_CLOSURE_V0"
TARGET_UNIT_ID = "decision_edge_observability.reference.post_closure_decision.v0"
LAYER = "OBSERVABILITY_HARDENING / POST_REFERENCE_DECISION"
MODE = "DECIDE_ONLY / SELECT_NEXT_INTERLOCK_BRANCH / NO_RUNTIME_PATCH"
BUILD_MODE = "POST_DECISION_EDGE_OBSERVABILITY_REFERENCE_DECISION_ONLY"

SOURCE_REF_CLOSE_RECEIPT_ID = "ac09c2e3"
SOURCE_REF_CLOSE_RECEIPT_PATH = ROOT / "data/decision_edge_observability_reference_closure_from_bounded_c6_adoption_probe_reference_v0_receipts/ac09c2e3.json"

EDGE_OBS_REF_DIR = ROOT / "data/decision_edge_observability_reference_closure_from_bounded_c6_adoption_probe_reference_v0"
EDGE_OBS_REF_CLOSURE_BASIS_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_reference_closure_basis_v0.json"
EDGE_OBS_REVIEWED_REFERENCE_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_reviewed_reference_v0.json"
EDGE_OBS_FREEZE_MANIFEST_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_reviewed_reference_freeze_manifest_v0.json"
EDGE_OBS_REFERENCE_INDEX_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_reference_index_v0.json"
EDGE_OBS_REQUIREMENT_REFERENCE_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_requirement_reference_v0.json"
EDGE_OBS_FIELD_SCHEMA_REFERENCE_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_field_schema_reference_v0.json"
EDGE_OBS_DISTINCTION_GUARD_REFERENCE_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_distinction_guard_reference_v0.json"
EDGE_OBS_NEGATIVE_CONTROL_REFERENCE_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_negative_control_reference_v0.json"
EDGE_OBS_POST_CLOSURE_DECISION_READY_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_reference_post_closure_decision_ready_v0.json"
EDGE_OBS_AUTHORITY_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_reference_closure_authority_boundary_v0.json"
EDGE_OBS_CLASSIFICATION_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_reference_closure_classification_v0.json"
EDGE_OBS_ROLLUP_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_reference_closure_rollup_v0.json"
EDGE_OBS_PROFILE_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_reference_closure_profile_v0.json"
EDGE_OBS_REPORT_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_reference_closure_report.json"
EDGE_OBS_TRACE_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_reference_closure_transition_trace.json"

SOURCE_EDGE_OBS_REVIEW_RECEIPT_PATH = ROOT / "data/decision_edge_observability_review_from_bounded_c6_adoption_probe_reference_v0_receipts/67314dd3.json"
SOURCE_EDGE_OBS_EXTRACTION_RECEIPT_PATH = ROOT / "data/decision_edge_observability_extraction_from_bounded_c6_adoption_probe_reference_v0_receipts/ea5ce604.json"
SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0_receipts/ac9451cc.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_REF_CLOSE_RECEIPT_PATH,
    EDGE_OBS_REF_CLOSURE_BASIS_PATH,
    EDGE_OBS_REVIEWED_REFERENCE_PATH,
    EDGE_OBS_FREEZE_MANIFEST_PATH,
    EDGE_OBS_REFERENCE_INDEX_PATH,
    EDGE_OBS_REQUIREMENT_REFERENCE_PATH,
    EDGE_OBS_FIELD_SCHEMA_REFERENCE_PATH,
    EDGE_OBS_DISTINCTION_GUARD_REFERENCE_PATH,
    EDGE_OBS_NEGATIVE_CONTROL_REFERENCE_PATH,
    EDGE_OBS_POST_CLOSURE_DECISION_READY_PATH,
    EDGE_OBS_AUTHORITY_PATH,
    EDGE_OBS_CLASSIFICATION_PATH,
    EDGE_OBS_ROLLUP_PATH,
    EDGE_OBS_PROFILE_PATH,
    EDGE_OBS_REPORT_PATH,
    EDGE_OBS_TRACE_PATH,
    SOURCE_EDGE_OBS_REVIEW_RECEIPT_PATH,
    SOURCE_EDGE_OBS_EXTRACTION_RECEIPT_PATH,
    SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_PATH,
]

OUT_DIR = ROOT / "data/post_decision_edge_observability_reference_decision_v0"
RECEIPT_DIR = ROOT / "data/post_decision_edge_observability_reference_decision_v0_receipts"

DECISION_BASIS_PATH = OUT_DIR / "post_edge_observability_reference_decision_basis_v0.json"
DECISION_OPTIONS_PATH = OUT_DIR / "post_edge_observability_reference_decision_options_v0.json"
SELECTED_BRANCH_PATH = OUT_DIR / "post_edge_observability_reference_selected_branch_v0.json"
SCHEMA_VALIDATOR_TARGET_PATH = OUT_DIR / "runtime_schema_validator_cell_design_target_v0.json"
SIDECAR_DEFERRED_TARGET_PATH = OUT_DIR / "runtime_observability_sidecar_deferred_target_v0.json"
PRE_C8_INTERLOCK_PLAN_PATH = OUT_DIR / "pre_c8_interlock_plan_v0.json"
REFERENCE_PARK_RECORD_PATH = OUT_DIR / "decision_edge_observability_reference_park_record_v0.json"
DEFERRED_BRANCHES_PATH = OUT_DIR / "post_edge_observability_reference_deferred_branches_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "post_edge_observability_reference_decision_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "post_edge_observability_reference_decision_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "post_edge_observability_reference_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "post_edge_observability_reference_decision_profile_v0.json"
REPORT_PATH = OUT_DIR / "post_edge_observability_reference_decision_report.json"
TRACE_PATH = OUT_DIR / "post_edge_observability_reference_decision_transition_trace.json"

EXPECTED_SOURCE_STATUS = "TYPED_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY"
EXPECTED_SOURCE_STOP = "STOP_TYPED_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY"
EXPECTED_SOURCE_NEXT = UNIT_ID

SELECTED_BRANCH = "DESIGN_RUNTIME_SCHEMA_VALIDATOR_CELL_TARGET_FROM_REVIEWED_OBSERVABILITY_REFERENCE"
SELECTED_NEXT_UNIT = "DESIGN_RUNTIME_SCHEMA_VALIDATOR_CELL_TARGET_FROM_REVIEWED_OBSERVABILITY_REFERENCE_V0"

DEFERRED_SIDECAR_UNIT = "DESIGN_RUNTIME_OBSERVABILITY_SIDECAR_TARGET_FROM_SCHEMA_VALIDATOR_AND_OBSERVABILITY_REFERENCES_V0"

REQUIRED_FIELDS = [
    "active_object",
    "attempted_move",
    "boundary_checked",
    "boundary_result",
    "blocked_moves",
    "lawful_next_moves",
    "source_packet_ref",
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

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{rel(path)}")
    if failures:
        return failures, {}

    receipt = read_json(SOURCE_REF_CLOSE_RECEIPT_PATH)
    summary = receipt.get("machine_readable_decision_edge_observability_reference_closure_summary", {})

    reviewed_reference = read_json(EDGE_OBS_REVIEWED_REFERENCE_PATH)
    freeze_manifest = read_json(EDGE_OBS_FREEZE_MANIFEST_PATH)
    reference_index = read_json(EDGE_OBS_REFERENCE_INDEX_PATH)
    requirement_reference = read_json(EDGE_OBS_REQUIREMENT_REFERENCE_PATH)
    field_schema_reference = read_json(EDGE_OBS_FIELD_SCHEMA_REFERENCE_PATH)
    distinction_guard_reference = read_json(EDGE_OBS_DISTINCTION_GUARD_REFERENCE_PATH)
    negative_control_reference = read_json(EDGE_OBS_NEGATIVE_CONTROL_REFERENCE_PATH)
    post_closure_decision_ready = read_json(EDGE_OBS_POST_CLOSURE_DECISION_READY_PATH)
    authority = read_json(EDGE_OBS_AUTHORITY_PATH)
    classification = read_json(EDGE_OBS_CLASSIFICATION_PATH)
    rollup = read_json(EDGE_OBS_ROLLUP_PATH)
    profile = read_json(EDGE_OBS_PROFILE_PATH)
    report = read_json(EDGE_OBS_REPORT_PATH)
    trace = read_json(EDGE_OBS_TRACE_PATH)

    edge_review_receipt = read_json(SOURCE_EDGE_OBS_REVIEW_RECEIPT_PATH)
    edge_extraction_receipt = read_json(SOURCE_EDGE_OBS_EXTRACTION_RECEIPT_PATH)
    bounded_probe_ref_close_receipt = read_json(SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_PATH)

    if receipt.get("receipt_id") != SOURCE_REF_CLOSE_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_reference_closure_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_hidden_next")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "decision_edge_observability_requirements_closed_as_reviewed_reference",
        "reviewed_reference_frozen",
        "post_observability_reference_decision_ready",
        "unit_feedback_hardening_deferred",
        "c7_deferred",
        "runtime_adoption_deferred",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
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
        "observability_reference_mutated",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if summary.get(key) is not False:
            failures.append(f"source_forbidden_true:{key}")

    for key, expected in {
        "edge_requirement_count": 7,
        "required_field_count": 7,
        "negative_control_count": 13,
    }.items():
        if summary.get(key) != expected:
            failures.append(f"source_count_wrong:{key}:{summary.get(key)}")

    if reviewed_reference.get("reference_status") != "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEWED_REFERENCE_FROZEN":
        failures.append("reviewed_reference_not_frozen")
    if freeze_manifest.get("freeze_status") != "FROZEN":
        failures.append("freeze_manifest_not_frozen")
    if reference_index.get("index_status") != "REFERENCE_INDEX_EMITTED":
        failures.append("reference_index_wrong")
    if requirement_reference.get("requirement_reference_status") != "REVIEWED_REFERENCE":
        failures.append("requirement_reference_wrong")
    if requirement_reference.get("required_fields") != REQUIRED_FIELDS:
        failures.append("requirement_reference_fields_wrong")
    if field_schema_reference.get("field_schema_reference_status") != "REVIEWED_REFERENCE":
        failures.append("field_schema_reference_wrong")
    if field_schema_reference.get("required_field_count") != 7:
        failures.append("field_schema_required_count_wrong")
    if distinction_guard_reference.get("distinction_guard_reference_status") != "REVIEWED_REFERENCE":
        failures.append("distinction_guard_reference_wrong")
    if negative_control_reference.get("negative_control_reference_status") != "REVIEWED_REFERENCE":
        failures.append("negative_control_reference_wrong")
    if negative_control_reference.get("negative_control_count") != 13:
        failures.append("negative_control_count_wrong")
    if post_closure_decision_ready.get("decision_ready") is not True:
        failures.append("post_closure_decision_not_ready")
    if post_closure_decision_ready.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append("post_closure_next_wrong")

    if authority.get("may_decide_next_after_observability_reference_closure") is not True:
        failures.append("authority_no_decide")
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
        "may_mutate_observability_reference",
    ]:
        if authority.get(forbidden) is not False:
            failures.append(f"authority_forbidden_true:{forbidden}")

    if classification.get("next_command_goal") is not None:
        failures.append("classification_hidden_next")
    if rollup.get("post_reference_decision_ready_count") != 1:
        failures.append("rollup_decision_ready_wrong")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if report.get("recommended_next_handling") != EXPECTED_SOURCE_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_hidden_next")

    for ancestor, name in [
        (edge_review_receipt, "edge_review"),
        (edge_extraction_receipt, "edge_extraction"),
        (bounded_probe_ref_close_receipt, "bounded_probe_reference_closure"),
    ]:
        if ancestor.get("gate") != "PASS":
            failures.append(f"ancestor_not_pass:{name}")

    return failures, {
        "summary": summary,
        "reviewed_reference": reviewed_reference,
        "requirement_reference": requirement_reference,
        "field_schema_reference": field_schema_reference,
        "distinction_guard_reference": distinction_guard_reference,
        "negative_control_reference": negative_control_reference,
        "post_closure_decision_ready": post_closure_decision_ready,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    decision_pass = not failures
    status = "TYPED_POST_EDGE_OBSERVABILITY_REFERENCE_DECISION_SELECTED_SCHEMA_VALIDATOR_DESIGN_READY" if decision_pass else "TYPED_POST_EDGE_OBSERVABILITY_REFERENCE_DECISION_GATE_FAIL"
    recommended_next = SELECTED_NEXT_UNIT if decision_pass else "REPAIR_POST_EDGE_OBSERVABILITY_REFERENCE_DECISION_V0"

    summary = basis.get("summary", {})
    reviewed_reference = basis.get("reviewed_reference", {})
    requirement_reference = basis.get("requirement_reference", {})
    field_schema_reference = basis.get("field_schema_reference", {})
    distinction_guard_reference = basis.get("distinction_guard_reference", {})
    negative_control_reference = basis.get("negative_control_reference", {})

    reason_codes = [
        "POST_EDGE_OBSERVABILITY_REFERENCE_DECISION_COMPLETE",
        "DECISION_EDGE_OBSERVABILITY_REFERENCE_CLOSURE_RECEIPT_CONSUMED",
        "DECISION_EDGE_OBSERVABILITY_REVIEWED_REFERENCE_CONFIRMED",
        "LOAD_BEARING_EDGE_REQUIREMENTS_CONFIRMED",
        "SCHEMA_VALIDATOR_CELL_DESIGN_SELECTED",
        "OBSERVABILITY_SIDECAR_DESIGN_DEFERRED_UNTIL_SCHEMA_VALIDATOR_REFERENCE_EXISTS",
        "C8_DEFERRED_UNTIL_SCHEMA_VALIDATOR_AND_SIDECAR_REFERENCES_EXIST",
        "UNIT_FEEDBACK_HARDENING_DEFERRED",
        "NO_RUNTIME_EFFECT",
        "NO_RUNTIME_PATCH",
        "NO_C7_AUTHORIZATION",
        "NO_C8_AUTHORIZATION",
        "NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if decision_pass else failures

    decision_basis = {
        "schema_version": "post_edge_observability_reference_decision_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if decision_pass else "BASIS_REPAIR_REQUIRED",
        "source_edge_observability_reference_closure_receipt_id": SOURCE_REF_CLOSE_RECEIPT_ID,
        "source_reference_status": reviewed_reference.get("reference_status"),
        "edge_requirement_count": requirement_reference.get("edge_requirement_count"),
        "required_fields": requirement_reference.get("required_fields"),
        "negative_control_count": negative_control_reference.get("negative_control_count"),
    }

    decision_options = {
        "schema_version": "post_edge_observability_reference_decision_options_v0",
        "decision_status": "NEXT_BRANCH_SELECTED" if decision_pass else "NO_BRANCH_SELECTED",
        "options": [
            {
                "branch": SELECTED_BRANCH,
                "selected": decision_pass,
                "next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
                "why": "Schema Validator Cell is the first basic interlock mechanic after reviewed decision-edge observability: formation/readability before admissibility.",
            },
            {
                "branch": "DESIGN_RUNTIME_OBSERVABILITY_SIDECAR_TARGET",
                "selected": False,
                "next_unit": None,
                "why": "This is the second and final basic interlock mechanic before C8, but it should consume the future Schema Validator reference.",
            },
            {
                "branch": "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET",
                "selected": False,
                "next_unit": None,
                "why": "Deferred. The current agreed pre-C8 interlock is Schema Validator Cell plus Observability Sidecar.",
            },
            {
                "branch": "OPEN_C8",
                "selected": False,
                "next_unit": None,
                "why": "Deferred until Schema Validator Cell and Observability Sidecar are designed, built, reviewed, and closed as references.",
            },
            {
                "branch": "PATCH_RUNTIME",
                "selected": False,
                "next_unit": None,
                "why": "Forbidden here. This decision selects design target only.",
            },
        ],
    }

    selected_branch = {
        "schema_version": "post_edge_observability_reference_selected_branch_v0",
        "selected_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "selected_scope": "design Schema Validator Cell as first proposal-formation sieve using reviewed decision-edge observability reference",
        "source_reference_closure_receipt_id": SOURCE_REF_CLOSE_RECEIPT_ID,
        "selected_does_not": [
            "build schema validator",
            "build observability sidecar",
            "harden unit feedback",
            "patch runtime",
            "authorize C7",
            "authorize C8",
            "claim transfer",
            "claim autonomy",
            "grant general Cell 1 authority",
            "claim runtime-wide enforcement",
        ],
    }

    schema_validator_target = {
        "schema_version": "runtime_schema_validator_cell_design_target_v0",
        "target_status": "SCHEMA_VALIDATOR_CELL_DESIGN_TARGET_SELECTED" if decision_pass else "NOT_SELECTED",
        "target_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "source_decision_edge_observability_reference_closure_receipt_id": SOURCE_REF_CLOSE_RECEIPT_ID,
        "role": "first proposal-formation sieve",
        "core_question": "Can this proposal be read as a well-formed candidate under a known schema?",
        "runtime_position": [
            "Builder / Proposal Cell",
            "Schema Validator Cell",
            "Lawful Admissibility Cell",
            "Builder Execution",
            "Advance / Halt",
        ],
        "must_consume": [
            rel(EDGE_OBS_REVIEWED_REFERENCE_PATH),
            rel(EDGE_OBS_REQUIREMENT_REFERENCE_PATH),
            rel(EDGE_OBS_FIELD_SCHEMA_REFERENCE_PATH),
            rel(EDGE_OBS_DISTINCTION_GUARD_REFERENCE_PATH),
            rel(EDGE_OBS_NEGATIVE_CONTROL_REFERENCE_PATH),
        ],
        "design_must_define": [
            "schema archive schema",
            "schema validation result enum",
            "schema validation result schema",
            "validated candidate packet schema",
            "schema feedback packet schema",
            "schema gap feedback packet schema",
            "schema validator receipt schema",
            "check table",
            "demo cases",
            "rollup/readout/profile/report/trace",
            "acceptance gates",
            "negative controls",
        ],
        "design_must_preserve_edge_observability_fields": [
            "active_object",
            "attempted_move",
            "boundary_checked",
            "boundary_result",
            "blocked_moves",
            "lawful_next_moves",
            "source_packet_ref",
        ],
        "formation_checks_only": [
            "schema known",
            "schema version compatible",
            "required fields present",
            "forbidden fields absent",
            "field types correct",
            "declared move type known",
            "declared boundary structure complete",
            "declared boundary structure internally consistent",
            "references structurally resolvable",
            "receipt contract declared",
            "distinguishability sufficient",
            "layer collapse absent",
            "hidden execution fields absent",
        ],
        "must_not_do": [
            "check authority",
            "check admissibility",
            "approve execution",
            "deny on authority grounds",
            "decide strategy",
            "decide truth",
            "decide usefulness",
            "repair proposals",
            "create schemas",
            "mutate schema archive",
            "validate unknown schema ad hoc",
            "emit builder command",
            "execute anything",
            "patch runtime",
            "authorize C7",
            "authorize C8",
        ],
        "terminology_adjustment": {
            "use": "VALIDATE / CLASSIFY / FORMATION_ONLY",
            "avoid": "VALIDATE / CERTIFY / FORMATION_ONLY",
            "why": "certify can imply authority, truth, or approval; classify preserves formation-only boundary",
        },
        "failure_precedence_required": [
            "SCHEMA_ARCHIVE_UNAVAILABLE",
            "UNKNOWN_SCHEMA",
            "SCHEMA_VERSION_MISMATCH",
            "INVALID_SHAPE",
            "MISSING_FIELD",
            "FORBIDDEN_FIELD",
            "TYPE_MISMATCH",
            "UNKNOWN_MOVE_TYPE",
            "BOUNDARY_MISSING",
            "BOUNDARY_CONFLICT",
            "UNRESOLVED_REFERENCE",
            "RECEIPT_CONTRACT_INSUFFICIENT",
            "DISTINGUISHABILITY_INSUFFICIENT",
            "LAYER_COLLAPSE_IN_PAYLOAD",
            "HIDDEN_EXECUTION_FIELD",
            "SCHEMA_ARCHIVE_GAP",
        ],
        "success_meaning": "Schema Validator design target selected. No validator built yet.",
    }

    sidecar_deferred_target = {
        "schema_version": "runtime_observability_sidecar_deferred_target_v0",
        "deferred_target_status": "DEFERRED_UNTIL_SCHEMA_VALIDATOR_REFERENCE_EXISTS",
        "future_unit": DEFERRED_SIDECAR_UNIT,
        "role": "runtime evidence recorder beside the control path",
        "core_rule": "Control path acts. Sidecar records.",
        "dependency": "consume reviewed decision-edge observability reference and future Schema Validator Cell reference",
        "why_deferred": "The Sidecar should record the Schema Validator event surface, so it should be designed after Schema Validator reference closure.",
        "must_not_do_now": [
            "design sidecar now",
            "build sidecar now",
            "patch runtime",
            "claim live runtime instrumentation",
            "authorize C8",
        ],
    }

    pre_c8_interlock_plan = {
        "schema_version": "pre_c8_interlock_plan_v0",
        "plan_status": "BASIC_INTERLOCK_PLAN_SELECTED",
        "remaining_pre_c8_mechanics": [
            {
                "order": 1,
                "object": "Schema Validator Cell",
                "role": "proposal formation/readability sieve",
                "selected_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
            },
            {
                "order": 2,
                "object": "Observability Sidecar",
                "role": "runtime event evidence recorder",
                "future_unit": DEFERRED_SIDECAR_UNIT,
            },
        ],
        "nothing_else_before_c8": True,
        "c8_deferred_until": [
            "Schema Validator Cell reference closure",
            "Observability Sidecar reference closure",
        ],
    }

    reference_park_record = {
        "schema_version": "decision_edge_observability_reference_park_record_v0",
        "park_status": "PARKED_AS_REVIEWED_REFERENCE_AVAILABLE_FOR_CONSUMPTION",
        "reference_receipt": SOURCE_REF_CLOSE_RECEIPT_ID,
        "reference_path": rel(EDGE_OBS_REVIEWED_REFERENCE_PATH),
        "meaning": "The decision-edge observability reference remains frozen and available. The current decision only selects Schema Validator Cell target design.",
    }

    deferred_branches = {
        "schema_version": "post_edge_observability_reference_deferred_branches_v0",
        "deferred": [
            DEFERRED_SIDECAR_UNIT,
            "OPEN_C8",
            "OPEN_C7",
            "PATCH_RUNTIME",
            "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET",
            "RUN_NEW_DOMAIN_SHIFT",
            "CLAIM_RUNTIME_WIDE_ENFORCEMENT",
            "CLAIM_FULL_TRANSFER",
            "CLAIM_GLOBAL_AUTONOMY",
            "GRANT_GENERAL_CELL1_AUTHORITY",
        ],
        "why": "The agreed pre-C8 interlock has exactly two mechanics: Schema Validator first, Observability Sidecar second. The current edge selects the first design target only.",
    }

    authority_boundary = {
        "schema_version": "post_edge_observability_reference_decision_authority_boundary_v0",
        "status": status,
        "may_design_schema_validator_cell_next": decision_pass,
        "may_design_observability_sidecar_now": False,
        "may_build_schema_validator_cell_now": False,
        "may_build_observability_sidecar_now": False,
        "may_harden_unit_feedback_now": False,
        "may_patch_runtime_now": False,
        "may_open_c7_now": False,
        "may_open_c8_now": False,
        "may_execute_new_domain_shift": False,
        "may_claim_full_transfer": False,
        "may_claim_global_autonomy": False,
        "may_claim_general_cell1_authority": False,
        "may_claim_runtime_wide_enforcement": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_mutate_c6_reviewed_reference": False,
        "may_mutate_bounded_probe_reference": False,
        "may_mutate_observability_reference": False,
    }

    classification = {
        "schema_version": "post_edge_observability_reference_decision_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "post_edge_observability_reference_decision_complete": decision_pass,
        "schema_validator_design_selected": decision_pass,
        "schema_validator_design_ready": decision_pass,
        "selected_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": recommended_next,
        "observability_sidecar_deferred": True,
        "unit_feedback_hardening_deferred": True,
        "c7_deferred": True,
        "c8_deferred": True,
        "runtime_adoption_deferred": True,
        "edge_requirement_count": requirement_reference.get("edge_requirement_count"),
        "required_field_count": field_schema_reference.get("required_field_count"),
        "negative_control_count": negative_control_reference.get("negative_control_count"),
        "runtime_effect": False,
        "runtime_patched": False,
        "c7_authorized": False,
        "c8_authorized": False,
        "new_domain_shift_executed": False,
        "general_cell1_authority_claimed": False,
        "global_autonomy_claimed": False,
        "full_transfer_claimed": False,
        "runtime_wide_enforcement_claimed": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "c6_reviewed_reference_mutated": False,
        "bounded_probe_reference_mutated": False,
        "observability_reference_mutated": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": True,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "post_edge_observability_reference_decision_rollup_v0",
        "decision_count": 1 if decision_pass else 0,
        "schema_validator_design_selected_count": 1 if decision_pass else 0,
        "schema_validator_build_count": 0,
        "observability_sidecar_design_count": 0,
        "observability_sidecar_build_count": 0,
        "unit_feedback_hardening_count": 0,
        "c7_authorized_count": 0,
        "c8_authorized_count": 0,
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
        "observability_reference_mutated_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    profile = {
        "schema_version": "post_edge_observability_reference_decision_profile_v0",
        "profile_id": "post_edge_obs_ref_decision_" + sig8(rollup),
        "status": status,
        "decision": "select Schema Validator Cell target design",
        "compression": "Before C8, add exactly two basic interlock mechanics: Schema Validator Cell then Observability Sidecar. This decision selects the first.",
        "schema_validator_role": "formation/readability sieve",
        "observability_sidecar_role": "evidence recorder after Schema Validator reference exists",
        "nothing_else_before_c8": True,
        "must_not_infer": [
            "Schema Validator was built",
            "Observability Sidecar was designed",
            "runtime was patched",
            "C8 was authorized",
            "unit feedback was hardened",
            "general Cell 1 authority was granted",
        ],
        "bad_counters_zero": True,
        "next_command_goal": None,
    }

    report = {
        "schema_version": "post_edge_observability_reference_decision_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The post-observability-reference decision consumed the frozen decision-edge observability reference and selected Schema Validator Cell target design as the next lawful object. Observability Sidecar is explicitly deferred until a Schema Validator reference exists. C8, runtime patching, unit-feedback hardening, and broader authority claims remain deferred.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "post_edge_observability_reference_decision_transition_trace_v0",
        "trace": [
            {
                "step": "consume_decision_edge_observability_reference_closure",
                "question": "is the reviewed decision-edge observability reference frozen and decision-ready",
                "answer": "yes" if decision_pass else "no",
                "taken": "evaluate pre-C8 interlock branches",
            },
            {
                "step": "select_schema_validator_design",
                "question": "what is the next basic interlock mechanic",
                "answer": SELECTED_NEXT_UNIT if decision_pass else recommended_next,
                "taken": "select Schema Validator Cell target design",
            },
            {
                "step": "defer_sidecar_and_c8",
                "question": "does this also design sidecar, open C8, or patch runtime",
                "answer": "no",
                "taken": "park sidecar until Schema Validator reference exists; defer C8",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (DECISION_BASIS_PATH, decision_basis),
        (DECISION_OPTIONS_PATH, decision_options),
        (SELECTED_BRANCH_PATH, selected_branch),
        (SCHEMA_VALIDATOR_TARGET_PATH, schema_validator_target),
        (SIDECAR_DEFERRED_TARGET_PATH, sidecar_deferred_target),
        (PRE_C8_INTERLOCK_PLAN_PATH, pre_c8_interlock_plan),
        (REFERENCE_PARK_RECORD_PATH, reference_park_record),
        (DEFERRED_BRANCHES_PATH, deferred_branches),
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
        "POST_EDGE_OBS_DECISION_0_REFERENCE_CLOSURE_RECEIPT_CONSUMED": SOURCE_REF_CLOSE_RECEIPT_PATH.exists(),
        "POST_EDGE_OBS_DECISION_1_REVIEWED_REFERENCE_CONFIRMED": reviewed_reference.get("reference_status") == "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEWED_REFERENCE_FROZEN",
        "POST_EDGE_OBS_DECISION_2_LOAD_BEARING_EDGE_FIELDS_CONFIRMED": requirement_reference.get("required_fields") == REQUIRED_FIELDS,
        "POST_EDGE_OBS_DECISION_3_SCHEMA_VALIDATOR_DESIGN_SELECTED": selected_branch["selected_next_unit"] == SELECTED_NEXT_UNIT,
        "POST_EDGE_OBS_DECISION_4_SCHEMA_VALIDATOR_TARGET_EMITTED": SCHEMA_VALIDATOR_TARGET_PATH.exists(),
        "POST_EDGE_OBS_DECISION_5_SIDECAR_DEFERRED_TARGET_EMITTED": SIDECAR_DEFERRED_TARGET_PATH.exists(),
        "POST_EDGE_OBS_DECISION_6_PRE_C8_INTERLOCK_PLAN_EMITTED": PRE_C8_INTERLOCK_PLAN_PATH.exists(),
        "POST_EDGE_OBS_DECISION_7_REFERENCE_PARK_RECORD_EMITTED": REFERENCE_PARK_RECORD_PATH.exists(),
        "POST_EDGE_OBS_DECISION_8_DEFERRED_BRANCHES_EMITTED": DEFERRED_BRANCHES_PATH.exists(),
        "POST_EDGE_OBS_DECISION_9_NOTHING_ELSE_BEFORE_C8_RECORDED": pre_c8_interlock_plan["nothing_else_before_c8"] is True,
        "POST_EDGE_OBS_DECISION_10_NO_SCHEMA_VALIDATOR_BUILD": rollup["schema_validator_build_count"] == 0,
        "POST_EDGE_OBS_DECISION_11_NO_SIDECAR_BUILD_OR_DESIGN": rollup["observability_sidecar_design_count"] == 0 and rollup["observability_sidecar_build_count"] == 0,
        "POST_EDGE_OBS_DECISION_12_UNIT_FEEDBACK_HARDENING_DEFERRED": classification["unit_feedback_hardening_deferred"] is True,
        "POST_EDGE_OBS_DECISION_13_NO_RUNTIME_EFFECT_OR_PATCH": classification["runtime_effect"] is False and classification["runtime_patched"] is False,
        "POST_EDGE_OBS_DECISION_14_NO_C7_OR_C8": classification["c7_authorized"] is False and classification["c8_authorized"] is False,
        "POST_EDGE_OBS_DECISION_15_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "POST_EDGE_OBS_DECISION_16_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["observability_reference_mutated"] is False,
        "POST_EDGE_OBS_DECISION_17_BAD_COUNTERS_ZERO": classification["bad_counters_zero"] is True,
        "POST_EDGE_OBS_DECISION_18_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "POST_EDGE_OBS_DECISION_19_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "POST_EDGE_OBS_DECISION_20_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_POST_EDGE_OBSERVABILITY_REFERENCE_DECISION_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_POST_EDGE_OBSERVABILITY_REFERENCE_DECISION_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_POST_EDGE_OBSERVABILITY_REFERENCE_DECISION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_reference": SOURCE_REF_CLOSE_RECEIPT_ID,
        "selected_next": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "post_edge_observability_reference_decision_receipt_v0",
        "receipt_type": "TYPED_POST_EDGE_OBSERVABILITY_REFERENCE_DECISION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_decision_edge_observability_reference_closure_receipt_id": SOURCE_REF_CLOSE_RECEIPT_ID,
        "machine_readable_post_edge_observability_reference_decision_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "post_edge_observability_reference_decision_complete": gate == "PASS",
            "schema_validator_design_selected": gate == "PASS",
            "schema_validator_design_ready": gate == "PASS",
            "selected_branch": SELECTED_BRANCH if gate == "PASS" else None,
            "selected_next_unit": final_next,
            "observability_sidecar_deferred": True,
            "unit_feedback_hardening_deferred": True,
            "c7_deferred": True,
            "c8_deferred": True,
            "runtime_adoption_deferred": True,
            "edge_requirement_count": requirement_reference.get("edge_requirement_count"),
            "required_field_count": field_schema_reference.get("required_field_count"),
            "negative_control_count": negative_control_reference.get("negative_control_count"),
            "nothing_else_before_c8": True,
            "runtime_effect": False,
            "runtime_patched": False,
            "c7_authorized": False,
            "c8_authorized": False,
            "new_domain_shift_executed": False,
            "general_cell1_authority_claimed": False,
            "global_autonomy_claimed": False,
            "full_transfer_claimed": False,
            "runtime_wide_enforcement_claimed": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "c6_reviewed_reference_mutated": False,
            "bounded_probe_reference_mutated": False,
            "observability_reference_mutated": False,
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
            "decision_basis": rel(DECISION_BASIS_PATH),
            "decision_options": rel(DECISION_OPTIONS_PATH),
            "selected_branch": rel(SELECTED_BRANCH_PATH),
            "schema_validator_target": rel(SCHEMA_VALIDATOR_TARGET_PATH),
            "sidecar_deferred_target": rel(SIDECAR_DEFERRED_TARGET_PATH),
            "pre_c8_interlock_plan": rel(PRE_C8_INTERLOCK_PLAN_PATH),
            "reference_park_record": rel(REFERENCE_PARK_RECORD_PATH),
            "deferred_branches": rel(DEFERRED_BRANCHES_PATH),
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
    print(f"post_edge_observability_reference_decision_receipt_id={receipt_id}")
    print(f"post_edge_observability_reference_decision_receipt_path={rel(receipt_path)}")
    print(f"runtime_schema_validator_design_target_path={rel(SCHEMA_VALIDATOR_TARGET_PATH)}")
    print(f"runtime_observability_sidecar_deferred_target_path={rel(SIDECAR_DEFERRED_TARGET_PATH)}")
    print(f"pre_c8_interlock_plan_path={rel(PRE_C8_INTERLOCK_PLAN_PATH)}")
    print(f"post_edge_observability_reference_decision_rollup_path={rel(ROLLUP_PATH)}")
    print(f"post_edge_observability_reference_decision_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
