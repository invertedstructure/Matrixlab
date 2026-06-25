#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "EXTRACT_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_FROM_BOUNDED_C6_ADOPTION_PROBE_REFERENCE_V0"
TARGET_UNIT_ID = "c6.bounded_adoption_probe.edge_observability.extract.v0"
LAYER = "OBSERVABILITY_HARDENING / DECISION_EDGE_REQUIREMENT_EXTRACTION"
MODE = "EXTRACT_ONLY / REQUIREMENT_SURFACE / NO_RUNTIME_PATCH"
BUILD_MODE = "DECISION_EDGE_OBSERVABILITY_EXTRACTION_ONLY"

SOURCE_POST_BOUNDED_DECISION_RECEIPT_ID = "685c7ea1"
SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_ID = "ac9451cc"

SOURCE_POST_BOUNDED_DECISION_RECEIPT_PATH = ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0_receipts/685c7ea1.json"

POST_BOUNDED_FILES = [
    ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0/post_bounded_probe_reference_decision_basis_v0.json",
    ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0/post_bounded_probe_reference_decision_options_v0.json",
    ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0/post_bounded_probe_reference_selected_branch_v0.json",
    ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0/decision_edge_observability_extraction_target_v0.json",
    ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0/bounded_probe_reference_park_record_v0.json",
    ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0/post_bounded_probe_reference_deferred_branches_v0.json",
    ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0/post_bounded_probe_reference_decision_authority_boundary_v0.json",
    ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0/post_bounded_probe_reference_decision_classification_v0.json",
    ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0/post_bounded_probe_reference_decision_rollup_v0.json",
    ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0/post_bounded_probe_reference_decision_profile_v0.json",
    ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0/post_bounded_probe_reference_decision_report.json",
    ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0/post_bounded_probe_reference_decision_transition_trace.json",
]

SOURCE_BOUNDED_PROBE_REF_CLOSE_RECEIPT_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0_receipts/ac9451cc.json"
BOUNDED_PROBE_REVIEWED_REFERENCE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_reviewed_reference_v0.json"
BOUNDED_PROBE_FREEZE_MANIFEST_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_reviewed_reference_freeze_manifest_v0.json"
BOUNDED_PROBE_REFERENCE_INDEX_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_reference_index_v0.json"
BOUNDED_PROBE_PACKET_LAW_SURVIVAL_REFERENCE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_packet_law_survival_reference_v0.json"
BOUNDED_PROBE_OBSERVABILITY_REFERENCE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_observability_reference_v0.json"
BOUNDED_PROBE_UNIT_FEEDBACK_REFERENCE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_unit_feedback_reference_v0.json"
BOUNDED_PROBE_NEGATIVE_CONTROL_REFERENCE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_negative_control_reference_v0.json"

PROBE_EDGE_OBSERVATIONS_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_edge_observations_v0.jsonl"
PROBE_PACKET_TRACE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_packet_trace_v0.jsonl"
PROBE_UNIT_FEEDBACK_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_unit_feedback_v0.jsonl"
PROBE_NEGATIVE_CONTROL_RESULTS_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_negative_control_results_v0.jsonl"

REQUIRED_SOURCE_FILES = [
    SOURCE_POST_BOUNDED_DECISION_RECEIPT_PATH,
    SOURCE_BOUNDED_PROBE_REF_CLOSE_RECEIPT_PATH,
    BOUNDED_PROBE_REVIEWED_REFERENCE_PATH,
    BOUNDED_PROBE_FREEZE_MANIFEST_PATH,
    BOUNDED_PROBE_REFERENCE_INDEX_PATH,
    BOUNDED_PROBE_PACKET_LAW_SURVIVAL_REFERENCE_PATH,
    BOUNDED_PROBE_OBSERVABILITY_REFERENCE_PATH,
    BOUNDED_PROBE_UNIT_FEEDBACK_REFERENCE_PATH,
    BOUNDED_PROBE_NEGATIVE_CONTROL_REFERENCE_PATH,
    PROBE_EDGE_OBSERVATIONS_PATH,
    PROBE_PACKET_TRACE_PATH,
    PROBE_UNIT_FEEDBACK_PATH,
    PROBE_NEGATIVE_CONTROL_RESULTS_PATH,
] + POST_BOUNDED_FILES

OUT_DIR = ROOT / "data/decision_edge_observability_extraction_from_bounded_c6_adoption_probe_reference_v0"
RECEIPT_DIR = ROOT / "data/decision_edge_observability_extraction_from_bounded_c6_adoption_probe_reference_v0_receipts"

EXTRACTION_BASIS_PATH = OUT_DIR / "decision_edge_observability_extraction_basis_v0.json"
REQUIREMENT_SET_PATH = OUT_DIR / "decision_edge_observability_requirement_set_v0.json"
EDGE_REQUIREMENTS_PATH = OUT_DIR / "decision_edge_observability_edge_requirements_v0.jsonl"
FIELD_SCHEMA_PATH = OUT_DIR / "decision_edge_observability_required_field_schema_v0.json"
SOURCE_MAPPING_PATH = OUT_DIR / "decision_edge_observability_source_mapping_v0.json"
DISTINCTION_GUARDS_PATH = OUT_DIR / "decision_edge_observability_distinction_guards_v0.json"
NEGATIVE_CONTROLS_PATH = OUT_DIR / "decision_edge_observability_negative_controls_v0.json"
REVIEW_TARGET_PATH = OUT_DIR / "decision_edge_observability_review_target_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "decision_edge_observability_extraction_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "decision_edge_observability_extraction_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "decision_edge_observability_extraction_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "decision_edge_observability_extraction_profile_v0.json"
REPORT_PATH = OUT_DIR / "decision_edge_observability_extraction_report.json"
TRACE_PATH = OUT_DIR / "decision_edge_observability_extraction_transition_trace.json"

EXPECTED_SOURCE_STATUS = "TYPED_POST_BOUNDED_C6_ADOPTION_PROBE_REFERENCE_DECISION_SELECTED_OBSERVABILITY_EXTRACTION_READY"
EXPECTED_SOURCE_STOP = "STOP_TYPED_POST_BOUNDED_C6_ADOPTION_PROBE_REFERENCE_DECISION_SELECTED_OBSERVABILITY_EXTRACTION_READY"
EXPECTED_SOURCE_NEXT = UNIT_ID

RECOMMENDED_NEXT = "REVIEW_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_FROM_BOUNDED_C6_ADOPTION_PROBE_REFERENCE_V0"

REQUIRED_FIELDS = [
    "active_object",
    "attempted_move",
    "boundary_checked",
    "boundary_result",
    "blocked_moves",
    "lawful_next_moves",
    "source_packet_ref",
]

EXPECTED_EDGE_NAMES = [
    "proposal_to_review",
    "review_to_accepted_packet",
    "accepted_packet_to_cell1_intake",
    "cell1_intake_to_probe_or_build",
    "probe_or_build_to_verification_return",
    "verification_return_to_handoff",
    "blocked_or_stop_to_feedback",
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

    decision_receipt = read_json(SOURCE_POST_BOUNDED_DECISION_RECEIPT_PATH)
    decision_summary = decision_receipt.get("machine_readable_post_bounded_probe_reference_decision_summary", {})
    selected_branch = read_json(ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0/post_bounded_probe_reference_selected_branch_v0.json")
    target = read_json(ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0/decision_edge_observability_extraction_target_v0.json")
    authority = read_json(ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0/post_bounded_probe_reference_decision_authority_boundary_v0.json")
    classification = read_json(ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0/post_bounded_probe_reference_decision_classification_v0.json")

    ref_close_receipt = read_json(SOURCE_BOUNDED_PROBE_REF_CLOSE_RECEIPT_PATH)
    reviewed_reference = read_json(BOUNDED_PROBE_REVIEWED_REFERENCE_PATH)
    observability_reference = read_json(BOUNDED_PROBE_OBSERVABILITY_REFERENCE_PATH)
    packet_law_survival_reference = read_json(BOUNDED_PROBE_PACKET_LAW_SURVIVAL_REFERENCE_PATH)
    unit_feedback_reference = read_json(BOUNDED_PROBE_UNIT_FEEDBACK_REFERENCE_PATH)
    negative_control_reference = read_json(BOUNDED_PROBE_NEGATIVE_CONTROL_REFERENCE_PATH)

    edge_observations = read_jsonl(PROBE_EDGE_OBSERVATIONS_PATH)
    packet_trace = read_jsonl(PROBE_PACKET_TRACE_PATH)
    unit_feedback = read_jsonl(PROBE_UNIT_FEEDBACK_PATH)
    negative_controls = read_jsonl(PROBE_NEGATIVE_CONTROL_RESULTS_PATH)

    if decision_receipt.get("receipt_id") != SOURCE_POST_BOUNDED_DECISION_RECEIPT_ID or decision_receipt.get("gate") != "PASS":
        failures.append("source_decision_receipt_not_pass")
    if decision_receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_decision_stop_wrong")
    if decision_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_decision_hidden_next")
    if decision_summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_decision_status_wrong:{decision_summary.get('status')}")
    if decision_summary.get("selected_next_unit") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_selected_next_wrong:{decision_summary.get('selected_next_unit')}")
    if decision_summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_recommended_next_wrong:{decision_summary.get('recommended_next')}")

    for key in [
        "post_bounded_probe_reference_decision_complete",
        "decision_edge_observability_extraction_ready",
        "bounded_probe_reference_parked_available",
        "unit_feedback_hardening_deferred",
        "c7_deferred",
        "runtime_adoption_deferred",
        "bad_counters_zero",
    ]:
        if decision_summary.get(key) is not True:
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
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if decision_summary.get(key) is not False:
            failures.append(f"source_forbidden_true:{key}")

    if selected_branch.get("selected_next_unit") != EXPECTED_SOURCE_NEXT:
        failures.append("selected_branch_next_wrong")
    if target.get("target_unit") != EXPECTED_SOURCE_NEXT:
        failures.append("target_unit_wrong")
    if target.get("minimum_requirement_fields") != REQUIRED_FIELDS:
        failures.append("target_required_fields_wrong")
    if target.get("edge_names_to_extract") != EXPECTED_EDGE_NAMES:
        failures.append("target_edge_names_wrong")
    for forbidden in ["patch runtime", "open C7", "execute a new domain shift", "claim transfer", "claim autonomy", "claim general Cell 1 authority", "claim runtime-wide enforcement"]:
        if forbidden not in target.get("must_not_do", []):
            failures.append(f"target_missing_forbidden:{forbidden}")

    if authority.get("may_extract_decision_edge_observability_requirements_next") is not True:
        failures.append("authority_no_extract")
    for forbidden in [
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
        if authority.get(forbidden) is not False:
            failures.append(f"authority_forbidden_true:{forbidden}")
    if classification.get("next_command_goal") is not None:
        failures.append("classification_hidden_next")

    if ref_close_receipt.get("receipt_id") != SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_ID or ref_close_receipt.get("gate") != "PASS":
        failures.append("bounded_probe_ref_close_not_pass")
    if reviewed_reference.get("reference_status") != "BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEWED_REFERENCE_FROZEN":
        failures.append("bounded_probe_reference_not_frozen")
    if observability_reference.get("observability_status") != "REVIEWED_REFERENCE":
        failures.append("observability_reference_wrong")
    if observability_reference.get("edge_observation_count") != 7:
        failures.append("observability_reference_edge_count_wrong")
    if packet_law_survival_reference.get("packet_law_distinctions_confirmed") is not True:
        failures.append("packet_law_distinctions_not_confirmed")
    if unit_feedback_reference.get("feedback_status") != "REVIEWED_REFERENCE":
        failures.append("unit_feedback_reference_wrong")
    if negative_control_reference.get("negative_controls_all_fail_closed") is not True:
        failures.append("negative_controls_not_fail_closed")

    if len(edge_observations) != 7:
        failures.append("edge_observation_count_wrong")
    if [row.get("edge_name") for row in edge_observations] != EXPECTED_EDGE_NAMES:
        failures.append("edge_observation_sequence_wrong")
    for row in edge_observations:
        for field in REQUIRED_FIELDS:
            if field not in row:
                failures.append(f"edge_observation_missing_field:{row.get('edge_name')}:{field}")
        if row.get("runtime_effect") is not False:
            failures.append(f"edge_observation_runtime_effect:{row.get('edge_name')}")

    if len(packet_trace) != 9:
        failures.append("packet_trace_count_wrong")
    if len(unit_feedback) != 4:
        failures.append("unit_feedback_count_wrong")
    if len(negative_controls) != 15:
        failures.append("negative_control_count_wrong")

    return failures, {
        "decision_summary": decision_summary,
        "selected_branch": selected_branch,
        "target": target,
        "reviewed_reference": reviewed_reference,
        "observability_reference": observability_reference,
        "packet_law_survival_reference": packet_law_survival_reference,
        "unit_feedback_reference": unit_feedback_reference,
        "negative_control_reference": negative_control_reference,
        "edge_observations": edge_observations,
        "packet_trace": packet_trace,
        "unit_feedback": unit_feedback,
        "negative_controls": negative_controls,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    extraction_pass = not failures
    status = "TYPED_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_EXTRACTED_REVIEW_READY" if extraction_pass else "TYPED_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_EXTRACTION_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if extraction_pass else "REPAIR_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_EXTRACTION_V0"

    decision_summary = basis.get("decision_summary", {})
    target = basis.get("target", {})
    reviewed_reference = basis.get("reviewed_reference", {})
    observability_reference = basis.get("observability_reference", {})
    packet_law_survival_reference = basis.get("packet_law_survival_reference", {})
    edge_observations = basis.get("edge_observations", [])
    packet_trace = basis.get("packet_trace", [])
    unit_feedback = basis.get("unit_feedback", [])
    negative_controls = basis.get("negative_controls", [])

    reason_codes = [
        "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_EXTRACTED",
        "POST_BOUNDED_PROBE_REFERENCE_DECISION_RECEIPT_CONSUMED",
        "BOUNDED_PROBE_REVIEWED_REFERENCE_CONSUMED",
        "OBSERVABILITY_REFERENCE_CONSUMED",
        "EDGE_OBSERVATION_ROWS_CONSUMED",
        "REQUIRED_EDGE_FIELDS_EXTRACTED",
        "EDGE_REQUIREMENTS_EMITTED",
        "FIELD_SCHEMA_EMITTED",
        "DISTINCTION_GUARDS_EMITTED",
        "NEGATIVE_CONTROLS_EMITTED",
        "REVIEW_TARGET_EMITTED",
        "UNIT_FEEDBACK_HARDENING_REMAINS_DEFERRED",
        "NO_RUNTIME_EFFECT",
        "NO_RUNTIME_PATCH",
        "NO_C7_AUTHORIZATION",
        "NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if extraction_pass else failures

    edge_requirements = []
    for idx, row in enumerate(edge_observations):
        edge_name = row.get("edge_name")
        edge_requirements.append({
            "schema_version": "decision_edge_observability_edge_requirement_v0",
            "requirement_id": f"edge_requirement_{idx:02d}_{sig8(edge_name)}",
            "edge_name": edge_name,
            "source_observation_id": row.get("observation_id"),
            "source_packet_ref": row.get("source_packet_ref"),
            "required_fields": REQUIRED_FIELDS,
            "field_values_from_source": {field: row.get(field) for field in REQUIRED_FIELDS},
            "load_bearing_reason": "supports decision-edge reconstruction, boundary diagnosis, lawful-next-move visibility, and future feedback hardening",
            "must_not_infer": [
                "edge observation is protocol proof",
                "observation sidecar grants authority",
                "edge visibility means runtime adoption",
            ],
            "runtime_effect": False,
        })

    requirement_set = {
        "schema_version": "decision_edge_observability_requirement_set_v0",
        "requirement_set_status": "EXTRACTED_REVIEW_READY" if extraction_pass else "NOT_READY",
        "source_post_bounded_decision_receipt_id": SOURCE_POST_BOUNDED_DECISION_RECEIPT_ID,
        "source_bounded_probe_reference_closure_receipt_id": SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_ID,
        "source_reference_status": reviewed_reference.get("reference_status"),
        "edge_observation_count": len(edge_observations),
        "edge_names": [row.get("edge_name") for row in edge_observations],
        "required_fields": REQUIRED_FIELDS,
        "core_rule": "A decision-edge observation is useful only when it records the active object, attempted move, checked boundary, boundary result, blocked moves, lawful next moves, and source packet reference.",
        "not_a_claim_of": [
            "runtime adoption",
            "C7 authorization",
            "general Cell 1 authority",
            "global autonomy",
            "full transfer",
            "runtime-wide enforcement",
        ],
    }

    field_schema = {
        "schema_version": "decision_edge_observability_required_field_schema_v0",
        "field_schema_status": "EXTRACTED",
        "fields": [
            {"field": "active_object", "purpose": "identifies what object the decision edge acted on", "required": True},
            {"field": "attempted_move", "purpose": "identifies the move being attempted across the edge", "required": True},
            {"field": "boundary_checked", "purpose": "records which boundary/guard was checked", "required": True},
            {"field": "boundary_result", "purpose": "records PASS/BLOCK/STOP/NA style edge result", "required": True},
            {"field": "blocked_moves", "purpose": "records moves made unlawful at the edge", "required": True},
            {"field": "lawful_next_moves", "purpose": "records what remains allowed after the edge", "required": True},
            {"field": "source_packet_ref", "purpose": "links the edge observation to the load-bearing packet/source", "required": True},
        ],
        "quality_rule": "Missing any required field downgrades the observation from load-bearing edge evidence to weak trace residue.",
    }

    source_mapping = {
        "schema_version": "decision_edge_observability_source_mapping_v0",
        "mapping_status": "EXTRACTED",
        "source_files": {
            "post_bounded_decision_receipt": rel(SOURCE_POST_BOUNDED_DECISION_RECEIPT_PATH),
            "bounded_probe_reference_closure_receipt": rel(SOURCE_BOUNDED_PROBE_REF_CLOSE_RECEIPT_PATH),
            "reviewed_reference": rel(BOUNDED_PROBE_REVIEWED_REFERENCE_PATH),
            "observability_reference": rel(BOUNDED_PROBE_OBSERVABILITY_REFERENCE_PATH),
            "edge_observations": rel(PROBE_EDGE_OBSERVATIONS_PATH),
            "packet_trace": rel(PROBE_PACKET_TRACE_PATH),
        },
        "edge_to_source_packet": [
            {
                "edge_name": row.get("edge_name"),
                "source_observation_id": row.get("observation_id"),
                "source_packet_ref": row.get("source_packet_ref"),
            }
            for row in edge_observations
        ],
    }

    distinction_guards = {
        "schema_version": "decision_edge_observability_distinction_guards_v0",
        "guards_status": "EXTRACTED",
        "guards": [
            "decision-edge observation is not protocol proof",
            "observation sidecar is not authority",
            "handoff is not hidden next command",
            "verification is not closure",
            "blocked feedback is not repair",
            "edge visibility is not runtime adoption",
            "observability extraction is not unit-feedback hardening",
            "observability extraction is not C7 authorization",
        ],
    }

    negative_controls = {
        "schema_version": "decision_edge_observability_negative_controls_v0",
        "negative_control_status": "EXTRACTED",
        "controls": [
            "missing_active_object_must_fail",
            "missing_attempted_move_must_fail",
            "missing_boundary_checked_must_fail",
            "missing_boundary_result_must_fail",
            "missing_blocked_moves_must_fail",
            "missing_lawful_next_moves_must_fail",
            "missing_source_packet_ref_must_fail",
            "edge_observation_as_protocol_proof_must_fail",
            "observation_sidecar_as_authority_must_fail",
            "edge_visibility_as_runtime_adoption_must_fail",
            "observability_extraction_as_unit_feedback_hardening_must_fail",
            "c7_authorization_claim_must_fail",
            "runtime_patch_claim_must_fail",
        ],
    }

    review_target = {
        "schema_version": "decision_edge_observability_review_target_v0",
        "review_target_status": "REVIEW_READY" if extraction_pass else "NOT_READY",
        "review_unit": RECOMMENDED_NEXT if extraction_pass else None,
        "must_review": [
            rel(REQUIREMENT_SET_PATH),
            rel(EDGE_REQUIREMENTS_PATH),
            rel(FIELD_SCHEMA_PATH),
            rel(SOURCE_MAPPING_PATH),
            rel(DISTINCTION_GUARDS_PATH),
            rel(NEGATIVE_CONTROLS_PATH),
        ],
        "review_questions": [
            "Are all 7 edge observations represented?",
            "Are all required load-bearing fields present?",
            "Are distinction guards explicit enough?",
            "Are negative controls sufficient to prevent observability from becoming authority/runtime adoption?",
            "Does extraction leave unit-feedback hardening deferred?",
        ],
    }

    extraction_basis = {
        "schema_version": "decision_edge_observability_extraction_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if extraction_pass else "BASIS_REPAIR_REQUIRED",
        "source_post_bounded_decision_receipt_id": SOURCE_POST_BOUNDED_DECISION_RECEIPT_ID,
        "source_bounded_probe_reference_closure_receipt_id": SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_ID,
        "selected_next_unit": decision_summary.get("selected_next_unit"),
        "source_reference_status": reviewed_reference.get("reference_status"),
        "observability_reference_status": observability_reference.get("observability_status"),
        "packet_law_distinctions_confirmed": packet_law_survival_reference.get("packet_law_distinctions_confirmed"),
    }

    authority_boundary = {
        "schema_version": "decision_edge_observability_extraction_authority_boundary_v0",
        "status": status,
        "may_review_decision_edge_observability_requirements_next": extraction_pass,
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
    }

    classification = {
        "schema_version": "decision_edge_observability_extraction_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "decision_edge_observability_requirements_extracted": extraction_pass,
        "review_ready": extraction_pass,
        "edge_requirement_count": len(edge_requirements),
        "required_field_count": len(REQUIRED_FIELDS),
        "negative_control_count": len(negative_controls["controls"]),
        "packet_trace_count": len(packet_trace),
        "edge_observation_count": len(edge_observations),
        "unit_feedback_count": len(unit_feedback),
        "source_reference_status": reviewed_reference.get("reference_status"),
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
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": True,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "decision_edge_observability_extraction_rollup_v0",
        "extraction_count": 1 if extraction_pass else 0,
        "review_ready_count": 1 if extraction_pass else 0,
        "edge_requirement_count": len(edge_requirements),
        "required_field_count": len(REQUIRED_FIELDS),
        "negative_control_count": len(negative_controls["controls"]),
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
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    profile = {
        "schema_version": "decision_edge_observability_extraction_profile_v0",
        "profile_id": "decision_edge_observability_extraction_" + sig8(rollup),
        "status": status,
        "extraction_object": "decision-edge observability requirement surface",
        "compression": "A load-bearing decision-edge observation must make the active object, move, boundary, result, blocked moves, lawful next moves, and source packet visible.",
        "edge_names": [row.get("edge_name") for row in edge_observations],
        "unit_feedback_hardening_deferred": True,
        "must_not_infer": requirement_set["not_a_claim_of"],
        "bad_counters_zero": True,
        "next_command_goal": None,
    }

    report = {
        "schema_version": "decision_edge_observability_extraction_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Decision-edge observability requirements were extracted from the bounded C6 adoption-probe reference. The extraction covers 7 edge observations, 7 required load-bearing fields, distinction guards, source mapping, and negative controls. It does not patch runtime, authorize C7, harden unit feedback yet, or claim transfer/autonomy/general Cell 1 authority.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "decision_edge_observability_extraction_transition_trace_v0",
        "trace": [
            {
                "step": "consume_post_bounded_probe_decision",
                "question": "was decision-edge observability extraction selected",
                "answer": "yes" if extraction_pass else "no",
                "taken": "consume bounded probe observability reference and edge observations",
            },
            {
                "step": "extract_edge_requirements",
                "question": "what must each load-bearing edge observation expose",
                "answer": ",".join(REQUIRED_FIELDS),
                "taken": "emit requirement set, per-edge requirements, field schema, and guards",
            },
            {
                "step": "preserve_boundary",
                "question": "does extraction patch runtime, authorize C7, or harden unit feedback",
                "answer": "no",
                "taken": "stop with review-ready extraction",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    write_json(EXTRACTION_BASIS_PATH, extraction_basis)
    write_json(REQUIREMENT_SET_PATH, requirement_set)
    write_jsonl(EDGE_REQUIREMENTS_PATH, edge_requirements)
    write_json(FIELD_SCHEMA_PATH, field_schema)
    write_json(SOURCE_MAPPING_PATH, source_mapping)
    write_json(DISTINCTION_GUARDS_PATH, distinction_guards)
    write_json(NEGATIVE_CONTROLS_PATH, negative_controls)
    write_json(REVIEW_TARGET_PATH, review_target)
    write_json(AUTHORITY_BOUNDARY_PATH, authority_boundary)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, profile)
    write_json(REPORT_PATH, report)
    write_json(TRACE_PATH, trace)

    acceptance_gate_results = {
        "EDGE_OBS_EXTRACTION_0_SOURCE_DECISION_RECEIPT_CONSUMED": SOURCE_POST_BOUNDED_DECISION_RECEIPT_PATH.exists(),
        "EDGE_OBS_EXTRACTION_1_BOUNDED_PROBE_REFERENCE_CONSUMED": reviewed_reference.get("reference_status") == "BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEWED_REFERENCE_FROZEN",
        "EDGE_OBS_EXTRACTION_2_OBSERVABILITY_REFERENCE_CONSUMED": observability_reference.get("observability_status") == "REVIEWED_REFERENCE",
        "EDGE_OBS_EXTRACTION_3_ALL_EDGE_OBSERVATIONS_CONSUMED": len(edge_observations) == 7,
        "EDGE_OBS_EXTRACTION_4_REQUIREMENT_SET_EMITTED": REQUIREMENT_SET_PATH.exists(),
        "EDGE_OBS_EXTRACTION_5_EDGE_REQUIREMENTS_EMITTED": EDGE_REQUIREMENTS_PATH.exists() and len(edge_requirements) == 7,
        "EDGE_OBS_EXTRACTION_6_REQUIRED_FIELD_SCHEMA_EMITTED": FIELD_SCHEMA_PATH.exists() and len(field_schema["fields"]) == 7,
        "EDGE_OBS_EXTRACTION_7_SOURCE_MAPPING_EMITTED": SOURCE_MAPPING_PATH.exists(),
        "EDGE_OBS_EXTRACTION_8_DISTINCTION_GUARDS_EMITTED": DISTINCTION_GUARDS_PATH.exists(),
        "EDGE_OBS_EXTRACTION_9_NEGATIVE_CONTROLS_EMITTED": NEGATIVE_CONTROLS_PATH.exists() and len(negative_controls["controls"]) == 13,
        "EDGE_OBS_EXTRACTION_10_REVIEW_TARGET_EMITTED": REVIEW_TARGET_PATH.exists(),
        "EDGE_OBS_EXTRACTION_11_UNIT_FEEDBACK_HARDENING_DEFERRED": classification["unit_feedback_hardening_deferred"] is True,
        "EDGE_OBS_EXTRACTION_12_NO_RUNTIME_EFFECT_OR_PATCH": classification["runtime_effect"] is False and classification["runtime_patched"] is False,
        "EDGE_OBS_EXTRACTION_13_NO_C7": classification["c7_authorized"] is False and classification["c7_deferred"] is True,
        "EDGE_OBS_EXTRACTION_14_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "EDGE_OBS_EXTRACTION_15_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["bounded_probe_reference_mutated"] is False,
        "EDGE_OBS_EXTRACTION_16_BAD_COUNTERS_ZERO": classification["bad_counters_zero"] is True,
        "EDGE_OBS_EXTRACTION_17_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "EDGE_OBS_EXTRACTION_18_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "EDGE_OBS_EXTRACTION_19_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_EXTRACTION_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_EXTRACTION_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_EXTRACTION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_decision": SOURCE_POST_BOUNDED_DECISION_RECEIPT_ID,
        "recommended_next": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "decision_edge_observability_extraction_receipt_v0",
        "receipt_type": "TYPED_DECISION_EDGE_OBSERVABILITY_EXTRACTION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_post_bounded_probe_reference_decision_receipt_id": SOURCE_POST_BOUNDED_DECISION_RECEIPT_ID,
        "source_bounded_probe_reference_closure_receipt_id": SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_ID,
        "machine_readable_decision_edge_observability_extraction_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "decision_edge_observability_requirements_extracted": gate == "PASS",
            "review_ready": gate == "PASS",
            "edge_requirement_count": len(edge_requirements),
            "required_field_count": len(REQUIRED_FIELDS),
            "negative_control_count": len(negative_controls["controls"]),
            "packet_trace_count": len(packet_trace),
            "edge_observation_count": len(edge_observations),
            "unit_feedback_count": len(unit_feedback),
            "source_reference_status": reviewed_reference.get("reference_status"),
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
            "extraction_basis": rel(EXTRACTION_BASIS_PATH),
            "requirement_set": rel(REQUIREMENT_SET_PATH),
            "edge_requirements": rel(EDGE_REQUIREMENTS_PATH),
            "field_schema": rel(FIELD_SCHEMA_PATH),
            "source_mapping": rel(SOURCE_MAPPING_PATH),
            "distinction_guards": rel(DISTINCTION_GUARDS_PATH),
            "negative_controls": rel(NEGATIVE_CONTROLS_PATH),
            "review_target": rel(REVIEW_TARGET_PATH),
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
    print(f"decision_edge_observability_extraction_receipt_id={receipt_id}")
    print(f"decision_edge_observability_extraction_receipt_path={rel(receipt_path)}")
    print(f"decision_edge_observability_requirement_set_path={rel(REQUIREMENT_SET_PATH)}")
    print(f"decision_edge_observability_edge_requirements_path={rel(EDGE_REQUIREMENTS_PATH)}")
    print(f"decision_edge_observability_review_target_path={rel(REVIEW_TARGET_PATH)}")
    print(f"decision_edge_observability_extraction_rollup_path={rel(ROLLUP_PATH)}")
    print(f"decision_edge_observability_extraction_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
