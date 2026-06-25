#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_FROM_BOUNDED_C6_ADOPTION_PROBE_REFERENCE_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "c6.bounded_adoption_probe.edge_observability.reviewed_reference.v0"
LAYER = "OBSERVABILITY_HARDENING / DECISION_EDGE_REQUIREMENT_REFERENCE_CLOSURE"
MODE = "CLOSE_ONLY / FREEZE_REVIEWED_REQUIREMENT_SURFACE / NO_RUNTIME_PATCH"
BUILD_MODE = "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REFERENCE_CLOSURE_ONLY"

SOURCE_REVIEW_RECEIPT_ID = "67314dd3"
SOURCE_EXTRACTION_RECEIPT_ID = "ea5ce604"
SOURCE_POST_BOUNDED_DECISION_RECEIPT_ID = "685c7ea1"
SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_ID = "ac9451cc"

SOURCE_REVIEW_RECEIPT_PATH = ROOT / "data/decision_edge_observability_review_from_bounded_c6_adoption_probe_reference_v0_receipts/67314dd3.json"

REVIEW_DIR = ROOT / "data/decision_edge_observability_review_from_bounded_c6_adoption_probe_reference_v0"
REVIEW_FILES = [
    REVIEW_DIR / "decision_edge_observability_review_basis_v0.json",
    REVIEW_DIR / "decision_edge_observability_source_receipt_review_v0.json",
    REVIEW_DIR / "decision_edge_observability_requirement_set_review_v0.json",
    REVIEW_DIR / "decision_edge_observability_edge_requirement_review_v0.json",
    REVIEW_DIR / "decision_edge_observability_field_schema_review_v0.json",
    REVIEW_DIR / "decision_edge_observability_distinction_guard_review_v0.json",
    REVIEW_DIR / "decision_edge_observability_negative_control_review_v0.json",
    REVIEW_DIR / "decision_edge_observability_source_mapping_review_v0.json",
    REVIEW_DIR / "decision_edge_observability_reviewed_reference_close_candidate_v0.json",
    REVIEW_DIR / "decision_edge_observability_review_authority_boundary_v0.json",
    REVIEW_DIR / "decision_edge_observability_review_classification_v0.json",
    REVIEW_DIR / "decision_edge_observability_review_rollup_v0.json",
    REVIEW_DIR / "decision_edge_observability_review_profile_v0.json",
    REVIEW_DIR / "decision_edge_observability_review_report.json",
    REVIEW_DIR / "decision_edge_observability_review_transition_trace.json",
]

EXTRACTION_DIR = ROOT / "data/decision_edge_observability_extraction_from_bounded_c6_adoption_probe_reference_v0"
SOURCE_EXTRACTION_RECEIPT_PATH = ROOT / "data/decision_edge_observability_extraction_from_bounded_c6_adoption_probe_reference_v0_receipts/ea5ce604.json"
EXTRACTION_FILES = [
    EXTRACTION_DIR / "decision_edge_observability_requirement_set_v0.json",
    EXTRACTION_DIR / "decision_edge_observability_edge_requirements_v0.jsonl",
    EXTRACTION_DIR / "decision_edge_observability_required_field_schema_v0.json",
    EXTRACTION_DIR / "decision_edge_observability_source_mapping_v0.json",
    EXTRACTION_DIR / "decision_edge_observability_distinction_guards_v0.json",
    EXTRACTION_DIR / "decision_edge_observability_negative_controls_v0.json",
]

SOURCE_POST_BOUNDED_DECISION_RECEIPT_PATH = ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0_receipts/685c7ea1.json"
SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0_receipts/ac9451cc.json"
BOUNDED_PROBE_REVIEWED_REFERENCE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_reviewed_reference_v0.json"
BOUNDED_PROBE_OBSERVABILITY_REFERENCE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_observability_reference_v0.json"

ANCESTOR_FILES = [
    SOURCE_POST_BOUNDED_DECISION_RECEIPT_PATH,
    SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_PATH,
    BOUNDED_PROBE_REVIEWED_REFERENCE_PATH,
    BOUNDED_PROBE_OBSERVABILITY_REFERENCE_PATH,
]

REQUIRED_SOURCE_FILES = [SOURCE_REVIEW_RECEIPT_PATH, SOURCE_EXTRACTION_RECEIPT_PATH] + REVIEW_FILES + EXTRACTION_FILES + ANCESTOR_FILES

OUT_DIR = ROOT / "data/decision_edge_observability_reference_closure_from_bounded_c6_adoption_probe_reference_v0"
RECEIPT_DIR = ROOT / "data/decision_edge_observability_reference_closure_from_bounded_c6_adoption_probe_reference_v0_receipts"

CLOSURE_BASIS_PATH = OUT_DIR / "decision_edge_observability_reference_closure_basis_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "decision_edge_observability_reviewed_reference_v0.json"
FREEZE_MANIFEST_PATH = OUT_DIR / "decision_edge_observability_reviewed_reference_freeze_manifest_v0.json"
REFERENCE_INDEX_PATH = OUT_DIR / "decision_edge_observability_reference_index_v0.json"
REQUIREMENT_REFERENCE_PATH = OUT_DIR / "decision_edge_observability_requirement_reference_v0.json"
FIELD_SCHEMA_REFERENCE_PATH = OUT_DIR / "decision_edge_observability_field_schema_reference_v0.json"
DISTINCTION_GUARD_REFERENCE_PATH = OUT_DIR / "decision_edge_observability_distinction_guard_reference_v0.json"
NEGATIVE_CONTROL_REFERENCE_PATH = OUT_DIR / "decision_edge_observability_negative_control_reference_v0.json"
POST_CLOSURE_DECISION_READY_PATH = OUT_DIR / "decision_edge_observability_reference_post_closure_decision_ready_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "decision_edge_observability_reference_closure_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "decision_edge_observability_reference_closure_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "decision_edge_observability_reference_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "decision_edge_observability_reference_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "decision_edge_observability_reference_closure_report.json"
TRACE_PATH = OUT_DIR / "decision_edge_observability_reference_closure_transition_trace.json"

EXPECTED_REVIEW_STATUS = "TYPED_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEWED_CLOSE_READY"
EXPECTED_REVIEW_STOP = "STOP_TYPED_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEWED_CLOSE_READY"
EXPECTED_REVIEW_NEXT = UNIT_ID

RECOMMENDED_NEXT = "DECIDE_NEXT_AFTER_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REFERENCE_CLOSURE_V0"

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

    review_receipt = read_json(SOURCE_REVIEW_RECEIPT_PATH)
    review_summary = review_receipt.get("machine_readable_decision_edge_observability_review_summary", {})

    extraction_receipt = read_json(SOURCE_EXTRACTION_RECEIPT_PATH)
    extraction_summary = extraction_receipt.get("machine_readable_decision_edge_observability_extraction_summary", {})

    requirement_set = read_json(EXTRACTION_DIR / "decision_edge_observability_requirement_set_v0.json")
    edge_requirements = read_jsonl(EXTRACTION_DIR / "decision_edge_observability_edge_requirements_v0.jsonl")
    field_schema = read_json(EXTRACTION_DIR / "decision_edge_observability_required_field_schema_v0.json")
    distinction_guards = read_json(EXTRACTION_DIR / "decision_edge_observability_distinction_guards_v0.json")
    negative_controls = read_json(EXTRACTION_DIR / "decision_edge_observability_negative_controls_v0.json")

    close_candidate = read_json(REVIEW_DIR / "decision_edge_observability_reviewed_reference_close_candidate_v0.json")
    review_authority = read_json(REVIEW_DIR / "decision_edge_observability_review_authority_boundary_v0.json")
    review_rollup = read_json(REVIEW_DIR / "decision_edge_observability_review_rollup_v0.json")
    review_profile = read_json(REVIEW_DIR / "decision_edge_observability_review_profile_v0.json")
    review_report = read_json(REVIEW_DIR / "decision_edge_observability_review_report.json")
    review_trace = read_json(REVIEW_DIR / "decision_edge_observability_review_transition_trace.json")

    post_decision_receipt = read_json(SOURCE_POST_BOUNDED_DECISION_RECEIPT_PATH)
    bounded_probe_ref_close = read_json(SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_PATH)
    bounded_probe_reference = read_json(BOUNDED_PROBE_REVIEWED_REFERENCE_PATH)
    bounded_probe_observability = read_json(BOUNDED_PROBE_OBSERVABILITY_REFERENCE_PATH)

    if review_receipt.get("receipt_id") != SOURCE_REVIEW_RECEIPT_ID or review_receipt.get("gate") != "PASS":
        failures.append("source_review_receipt_not_pass")
    if review_receipt.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("source_review_stop_wrong")
    if review_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_review_hidden_next")
    if review_summary.get("status") != EXPECTED_REVIEW_STATUS:
        failures.append(f"source_review_status_wrong:{review_summary.get('status')}")
    if review_summary.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append(f"source_review_next_wrong:{review_summary.get('recommended_next')}")

    for key in [
        "decision_edge_observability_requirements_review_complete",
        "decision_edge_observability_requirements_review_pass",
        "close_candidate_ready",
        "source_extraction_review_ready",
        "unit_feedback_hardening_deferred",
        "c7_deferred",
        "runtime_adoption_deferred",
        "bad_counters_zero",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"review_required_true_missing:{key}")

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
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if review_summary.get(key) is not False:
            failures.append(f"review_forbidden_true:{key}")

    for key, expected in {
        "edge_requirement_count": 7,
        "required_field_count": 7,
        "negative_control_count": 13,
        "source_edge_observation_count": 7,
        "packet_trace_count": 9,
        "unit_feedback_count": 4,
    }.items():
        if review_summary.get(key) != expected:
            failures.append(f"review_count_wrong:{key}:{review_summary.get(key)}")

    if extraction_receipt.get("receipt_id") != SOURCE_EXTRACTION_RECEIPT_ID or extraction_receipt.get("gate") != "PASS":
        failures.append("source_extraction_receipt_not_pass")
    if extraction_summary.get("decision_edge_observability_requirements_extracted") is not True:
        failures.append("source_extraction_not_extracted")

    if requirement_set.get("requirement_set_status") != "EXTRACTED_REVIEW_READY":
        failures.append("requirement_set_not_review_ready")
    if requirement_set.get("required_fields") != REQUIRED_FIELDS:
        failures.append("requirement_set_required_fields_wrong")
    if len(edge_requirements) != 7:
        failures.append("edge_requirement_count_wrong")
    if [field.get("field") for field in field_schema.get("fields", [])] != REQUIRED_FIELDS:
        failures.append("field_schema_required_fields_wrong")
    if len(distinction_guards.get("guards", [])) != 8:
        failures.append("distinction_guard_count_wrong")
    if len(negative_controls.get("controls", [])) != 13:
        failures.append("negative_control_count_wrong")

    if close_candidate.get("candidate_status") != "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEWED_REFERENCE_CLOSE_READY":
        failures.append("close_candidate_not_ready")
    if close_candidate.get("review_pass") is not True:
        failures.append("close_candidate_review_not_pass")
    if review_authority.get("may_close_decision_edge_observability_requirements_as_reviewed_reference_next") is not True:
        failures.append("review_authority_no_close")
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
    ]:
        if review_authority.get(forbidden) is not False:
            failures.append(f"review_authority_forbidden_true:{forbidden}")

    if review_rollup.get("review_pass_count") != 1 or review_rollup.get("close_candidate_ready_count") != 1:
        failures.append("review_rollup_not_close_ready")
    if review_profile.get("next_command_goal") is not None:
        failures.append("review_profile_hidden_next")
    if review_report.get("recommended_next_handling") != EXPECTED_REVIEW_NEXT:
        failures.append("review_report_next_wrong")
    if review_trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("review_trace_hidden_next")

    if post_decision_receipt.get("gate") != "PASS":
        failures.append("post_decision_receipt_not_pass")
    if bounded_probe_ref_close.get("gate") != "PASS":
        failures.append("bounded_probe_reference_closure_not_pass")
    if bounded_probe_reference.get("reference_status") != "BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEWED_REFERENCE_FROZEN":
        failures.append("bounded_probe_reference_not_frozen")
    if bounded_probe_observability.get("observability_status") != "REVIEWED_REFERENCE":
        failures.append("bounded_probe_observability_not_reference")

    return failures, {
        "review_summary": review_summary,
        "requirement_set": requirement_set,
        "edge_requirements": edge_requirements,
        "field_schema": field_schema,
        "distinction_guards": distinction_guards,
        "negative_controls": negative_controls,
        "bounded_probe_reference": bounded_probe_reference,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    close_pass = not failures
    status = "TYPED_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY" if close_pass else "TYPED_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REFERENCE_CLOSURE_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if close_pass else "REPAIR_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REFERENCE_CLOSURE_V0"

    review_summary = basis.get("review_summary", {})
    requirement_set = basis.get("requirement_set", {})
    edge_requirements = basis.get("edge_requirements", [])
    field_schema = basis.get("field_schema", {})
    distinction_guards = basis.get("distinction_guards", {})
    negative_controls = basis.get("negative_controls", {})
    bounded_probe_reference = basis.get("bounded_probe_reference", {})

    reason_codes = [
        "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_CLOSED_AS_REVIEWED_REFERENCE",
        "REVIEW_RECEIPT_CONSUMED",
        "EXTRACTION_RECEIPT_CONSUMED",
        "REQUIREMENT_SET_FROZEN",
        "EDGE_REQUIREMENTS_FROZEN",
        "FIELD_SCHEMA_FROZEN",
        "DISTINCTION_GUARDS_FROZEN",
        "NEGATIVE_CONTROLS_FROZEN",
        "LOAD_BEARING_EDGE_FIELDS_FROZEN",
        "POST_OBSERVABILITY_REFERENCE_DECISION_READY",
        "UNIT_FEEDBACK_HARDENING_REMAINS_DEFERRED",
        "NO_RUNTIME_EFFECT",
        "NO_RUNTIME_PATCH",
        "NO_C7_AUTHORIZATION",
        "NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if close_pass else failures

    closure_basis = {
        "schema_version": "decision_edge_observability_reference_closure_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if close_pass else "BASIS_REPAIR_REQUIRED",
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "source_extraction_receipt_id": SOURCE_EXTRACTION_RECEIPT_ID,
        "source_post_bounded_decision_receipt_id": SOURCE_POST_BOUNDED_DECISION_RECEIPT_ID,
        "source_bounded_probe_reference_closure_receipt_id": SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_ID,
        "review_status": review_summary.get("status"),
        "bounded_probe_reference_status": bounded_probe_reference.get("reference_status"),
    }

    reviewed_reference = {
        "schema_version": "decision_edge_observability_reviewed_reference_v0",
        "reference_status": "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEWED_REFERENCE_FROZEN" if close_pass else "NOT_FROZEN",
        "reference_id": "decision_edge_observability_reference_" + sig8(reason_codes),
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "source_extraction_receipt_id": SOURCE_EXTRACTION_RECEIPT_ID,
        "source_bounded_probe_reference_closure_receipt_id": SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_ID,
        "reference_claim": "A load-bearing decision-edge observation must expose active object, attempted move, boundary checked, boundary result, blocked moves, lawful next moves, and source packet ref.",
        "edge_requirement_count": len(edge_requirements),
        "required_fields": REQUIRED_FIELDS,
        "negative_control_count": len(negative_controls.get("controls", [])),
        "must_not_infer": [
            "unit-feedback hardening",
            "runtime patch",
            "C7 authorization",
            "full transfer",
            "global autonomy",
            "general Cell 1 authority",
            "runtime-wide enforcement",
        ],
    }

    freeze_manifest = {
        "schema_version": "decision_edge_observability_reviewed_reference_freeze_manifest_v0",
        "freeze_status": "FROZEN" if close_pass else "NOT_FROZEN",
        "frozen_receipts": [
            rel(SOURCE_REVIEW_RECEIPT_PATH),
            rel(SOURCE_EXTRACTION_RECEIPT_PATH),
            rel(SOURCE_POST_BOUNDED_DECISION_RECEIPT_PATH),
            rel(SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_PATH),
        ],
        "frozen_review_files": [rel(p) for p in REVIEW_FILES],
        "frozen_extraction_files": [rel(p) for p in EXTRACTION_FILES],
        "frozen_ancestor_files": [rel(p) for p in ANCESTOR_FILES],
        "frozen_file_sha256": snapshot_files(REQUIRED_SOURCE_FILES),
    }

    reference_index = {
        "schema_version": "decision_edge_observability_reference_index_v0",
        "index_status": "REFERENCE_INDEX_EMITTED",
        "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
        "freeze_manifest": rel(FREEZE_MANIFEST_PATH),
        "requirement_reference": rel(REQUIREMENT_REFERENCE_PATH),
        "field_schema_reference": rel(FIELD_SCHEMA_REFERENCE_PATH),
        "distinction_guard_reference": rel(DISTINCTION_GUARD_REFERENCE_PATH),
        "negative_control_reference": rel(NEGATIVE_CONTROL_REFERENCE_PATH),
        "post_closure_decision_ready": rel(POST_CLOSURE_DECISION_READY_PATH),
    }

    requirement_reference = {
        "schema_version": "decision_edge_observability_requirement_reference_v0",
        "requirement_reference_status": "REVIEWED_REFERENCE",
        "requirement_set_status": requirement_set.get("requirement_set_status"),
        "edge_requirement_count": len(edge_requirements),
        "required_fields": REQUIRED_FIELDS,
        "core_rule": requirement_set.get("core_rule"),
    }

    field_schema_reference = {
        "schema_version": "decision_edge_observability_field_schema_reference_v0",
        "field_schema_reference_status": "REVIEWED_REFERENCE",
        "required_field_count": len(REQUIRED_FIELDS),
        "fields": field_schema.get("fields", []),
        "quality_rule": field_schema.get("quality_rule"),
    }

    distinction_guard_reference = {
        "schema_version": "decision_edge_observability_distinction_guard_reference_v0",
        "distinction_guard_reference_status": "REVIEWED_REFERENCE",
        "guard_count": len(distinction_guards.get("guards", [])),
        "guards": distinction_guards.get("guards", []),
    }

    negative_control_reference = {
        "schema_version": "decision_edge_observability_negative_control_reference_v0",
        "negative_control_reference_status": "REVIEWED_REFERENCE",
        "negative_control_count": len(negative_controls.get("controls", [])),
        "controls": negative_controls.get("controls", []),
    }

    post_closure_decision_ready = {
        "schema_version": "decision_edge_observability_reference_post_closure_decision_ready_v0",
        "decision_ready": close_pass,
        "recommended_next": recommended_next,
        "closed_reference_status": reviewed_reference["reference_status"],
        "decision_options": [
            "decide whether to proceed to unit-feedback hardening from the reviewed observability reference",
            "decide whether to design a small observability adoption probe",
            "decide whether to park the observability reference",
            "decide whether to defer C7 until after unit-feedback hardening",
        ],
        "not_authorized_by_closure": [
            "unit-feedback hardening execution",
            "runtime adoption",
            "C7 execution",
            "full transfer claim",
            "global autonomy claim",
            "general Cell 1 authority",
            "runtime-wide enforcement claim",
        ],
    }

    authority_boundary = {
        "schema_version": "decision_edge_observability_reference_closure_authority_boundary_v0",
        "status": status,
        "may_close_decision_edge_observability_requirements_as_reviewed_reference": close_pass,
        "may_decide_next_after_observability_reference_closure": close_pass,
        "may_harden_unit_feedback_now": False,
        "may_patch_runtime_now": False,
        "may_open_c7_now": False,
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
        "schema_version": "decision_edge_observability_reference_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "decision_edge_observability_requirements_closed_as_reviewed_reference": close_pass,
        "reviewed_reference_frozen": close_pass,
        "post_observability_reference_decision_ready": close_pass,
        "edge_requirement_count": len(edge_requirements),
        "required_field_count": len(REQUIRED_FIELDS),
        "negative_control_count": len(negative_controls.get("controls", [])),
        "unit_feedback_hardening_deferred": True,
        "c7_deferred": True,
        "runtime_adoption_deferred": True,
        "runtime_effect": False,
        "runtime_patched": False,
        "c7_authorized": False,
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
        "schema_version": "decision_edge_observability_reference_closure_rollup_v0",
        "closure_count": 1 if close_pass else 0,
        "reviewed_reference_frozen_count": 1 if close_pass else 0,
        "post_reference_decision_ready_count": 1 if close_pass else 0,
        "edge_requirement_count": len(edge_requirements),
        "required_field_count": len(REQUIRED_FIELDS),
        "negative_control_count": len(negative_controls.get("controls", [])),
        "unit_feedback_hardening_count": 0,
        "c7_authorized_count": 0,
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
        "schema_version": "decision_edge_observability_reference_closure_profile_v0",
        "profile_id": "decision_edge_observability_reference_closure_" + sig8(rollup),
        "status": status,
        "schema_claim": "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEWED_REFERENCE_ONLY",
        "reference_object": "decision-edge observability requirement surface",
        "compression": "Load-bearing decision-edge observations must expose object, move, boundary, result, blocked moves, lawful next moves, and source packet.",
        "unit_feedback_hardening_deferred": True,
        "must_not_infer": reviewed_reference["must_not_infer"],
        "bad_counters_zero": True,
        "next_command_goal": None,
    }

    report = {
        "schema_version": "decision_edge_observability_reference_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The decision-edge observability requirements are closed as a reviewed reference. The reference freezes 7 edge requirements, 7 required load-bearing fields, distinction guards, and 13 negative controls. It does not harden unit feedback yet, patch runtime, authorize C7, or claim transfer/autonomy/general Cell 1 authority.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "decision_edge_observability_reference_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_observability_review",
                "question": "are decision-edge observability requirements reviewed and close-ready",
                "answer": "yes" if close_pass else "no",
                "taken": "freeze reviewed observability requirement reference",
            },
            {
                "step": "freeze_requirement_surface",
                "question": "what is frozen",
                "answer": "edge requirements, required fields, field schema, guards, negative controls",
                "taken": "emit reference, manifest, index, rollup/profile/report",
            },
            {
                "step": "preserve_boundary",
                "question": "does closure harden unit feedback, patch runtime, or authorize C7",
                "answer": "no",
                "taken": "stop with post-observability-reference decision ready",
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
        (REVIEWED_REFERENCE_PATH, reviewed_reference),
        (FREEZE_MANIFEST_PATH, freeze_manifest),
        (REFERENCE_INDEX_PATH, reference_index),
        (REQUIREMENT_REFERENCE_PATH, requirement_reference),
        (FIELD_SCHEMA_REFERENCE_PATH, field_schema_reference),
        (DISTINCTION_GUARD_REFERENCE_PATH, distinction_guard_reference),
        (NEGATIVE_CONTROL_REFERENCE_PATH, negative_control_reference),
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
        "EDGE_OBS_REF_CLOSE_0_REVIEW_RECEIPT_CONSUMED": SOURCE_REVIEW_RECEIPT_PATH.exists(),
        "EDGE_OBS_REF_CLOSE_1_EXTRACTION_RECEIPT_CONSUMED": SOURCE_EXTRACTION_RECEIPT_PATH.exists(),
        "EDGE_OBS_REF_CLOSE_2_REVIEWED_REFERENCE_FROZEN": REVIEWED_REFERENCE_PATH.exists() and reviewed_reference["reference_status"] == "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEWED_REFERENCE_FROZEN",
        "EDGE_OBS_REF_CLOSE_3_FREEZE_MANIFEST_EMITTED": FREEZE_MANIFEST_PATH.exists(),
        "EDGE_OBS_REF_CLOSE_4_REFERENCE_INDEX_EMITTED": REFERENCE_INDEX_PATH.exists(),
        "EDGE_OBS_REF_CLOSE_5_REQUIREMENT_REFERENCE_EMITTED": REQUIREMENT_REFERENCE_PATH.exists() and requirement_reference["edge_requirement_count"] == 7,
        "EDGE_OBS_REF_CLOSE_6_FIELD_SCHEMA_REFERENCE_EMITTED": FIELD_SCHEMA_REFERENCE_PATH.exists() and field_schema_reference["required_field_count"] == 7,
        "EDGE_OBS_REF_CLOSE_7_DISTINCTION_GUARD_REFERENCE_EMITTED": DISTINCTION_GUARD_REFERENCE_PATH.exists() and distinction_guard_reference["guard_count"] == 8,
        "EDGE_OBS_REF_CLOSE_8_NEGATIVE_CONTROL_REFERENCE_EMITTED": NEGATIVE_CONTROL_REFERENCE_PATH.exists() and negative_control_reference["negative_control_count"] == 13,
        "EDGE_OBS_REF_CLOSE_9_POST_REFERENCE_DECISION_READY": POST_CLOSURE_DECISION_READY_PATH.exists() and post_closure_decision_ready["decision_ready"] is True,
        "EDGE_OBS_REF_CLOSE_10_UNIT_FEEDBACK_HARDENING_DEFERRED": classification["unit_feedback_hardening_deferred"] is True,
        "EDGE_OBS_REF_CLOSE_11_NO_RUNTIME_EFFECT_OR_PATCH": classification["runtime_effect"] is False and classification["runtime_patched"] is False,
        "EDGE_OBS_REF_CLOSE_12_NO_C7": classification["c7_authorized"] is False and classification["c7_deferred"] is True,
        "EDGE_OBS_REF_CLOSE_13_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "EDGE_OBS_REF_CLOSE_14_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["observability_reference_mutated"] is False,
        "EDGE_OBS_REF_CLOSE_15_BAD_COUNTERS_ZERO": classification["bad_counters_zero"] is True,
        "EDGE_OBS_REF_CLOSE_16_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "EDGE_OBS_REF_CLOSE_17_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "EDGE_OBS_REF_CLOSE_18_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REFERENCE_CLOSURE_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REFERENCE_CLOSURE_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REFERENCE_CLOSURE_GATE_FAIL",
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
        "schema_version": "decision_edge_observability_reference_closure_receipt_v0",
        "receipt_type": "TYPED_DECISION_EDGE_OBSERVABILITY_REFERENCE_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_decision_edge_observability_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "source_decision_edge_observability_extraction_receipt_id": SOURCE_EXTRACTION_RECEIPT_ID,
        "source_bounded_probe_reference_closure_receipt_id": SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_ID,
        "machine_readable_decision_edge_observability_reference_closure_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "decision_edge_observability_requirements_closed_as_reviewed_reference": gate == "PASS",
            "reviewed_reference_frozen": gate == "PASS",
            "post_observability_reference_decision_ready": gate == "PASS",
            "edge_requirement_count": len(edge_requirements),
            "required_field_count": len(REQUIRED_FIELDS),
            "negative_control_count": len(negative_controls.get("controls", [])),
            "unit_feedback_hardening_deferred": True,
            "c7_deferred": True,
            "runtime_adoption_deferred": True,
            "runtime_effect": False,
            "runtime_patched": False,
            "c7_authorized": False,
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
            "closure_basis": rel(CLOSURE_BASIS_PATH),
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "freeze_manifest": rel(FREEZE_MANIFEST_PATH),
            "reference_index": rel(REFERENCE_INDEX_PATH),
            "requirement_reference": rel(REQUIREMENT_REFERENCE_PATH),
            "field_schema_reference": rel(FIELD_SCHEMA_REFERENCE_PATH),
            "distinction_guard_reference": rel(DISTINCTION_GUARD_REFERENCE_PATH),
            "negative_control_reference": rel(NEGATIVE_CONTROL_REFERENCE_PATH),
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
    print(f"decision_edge_observability_reference_closure_receipt_id={receipt_id}")
    print(f"decision_edge_observability_reference_closure_receipt_path={rel(receipt_path)}")
    print(f"decision_edge_observability_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"decision_edge_observability_freeze_manifest_path={rel(FREEZE_MANIFEST_PATH)}")
    print(f"decision_edge_observability_post_closure_decision_ready_path={rel(POST_CLOSURE_DECISION_READY_PATH)}")
    print(f"decision_edge_observability_reference_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"decision_edge_observability_reference_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
