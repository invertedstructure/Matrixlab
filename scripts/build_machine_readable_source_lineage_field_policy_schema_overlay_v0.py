#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY"
MODE = "SCHEMA_OVERLAY_BUILD / NO_SCHEMA_OVERLAY_APPLICATION / NO_TYPING_RULE_APPLICATION / NO_POLICY_MODIFICATION / NO_CANDIDATE_MODIFICATION / NO_REBIND / NO_METADATA_FILL"
BUILD_MODE = "SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_BUILD_ONLY"

SOURCE_REVIEW_RECEIPT_ID = "23f4c5c5"
SOURCE_REVIEW_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_review_v0_receipts/23f4c5c5.json"
SOURCE_REVIEW_ASSESSMENT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_review_v0/typed_machine_readable_source_lineage_field_policy_typing_review_assessment_v0.json"
SOURCE_FIELD_POLICY_GAP_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_review_v0/typed_machine_readable_field_policy_typing_gap_review_v0.json"
SOURCE_LINEAGE_REQUIREMENT_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_review_v0/typed_machine_readable_source_lineage_requirement_review_v0.json"
SOURCE_CANDIDATE_OVERLAY_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_review_v0/typed_machine_readable_candidate_artifact_typing_overlay_review_v0.json"
SOURCE_SCHEMA_CONTRACT_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_review_v0/typed_machine_readable_source_lineage_field_policy_schema_contract_review_v0.json"
SOURCE_TYPING_RULE_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_review_v0/typed_machine_readable_source_lineage_field_policy_typing_rule_review_v0.json"
SOURCE_SCHEMA_OVERLAY_INPUT_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_review_v0/typed_machine_readable_source_lineage_field_policy_schema_overlay_input_contract_v0.json"
SOURCE_REVIEW_DECISION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_review_v0/typed_machine_readable_source_lineage_field_policy_typing_review_decision_table_v0.json"
SOURCE_REVIEW_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_review_v0/typed_machine_readable_source_lineage_field_policy_typing_review_result_packet_v0.json"
SOURCE_REVIEW_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_review_v0/typed_machine_readable_source_lineage_field_policy_typing_review_classification_v0.json"
SOURCE_REVIEW_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_review_v0/typed_machine_readable_source_lineage_field_policy_typing_review_rollup_v0.json"
SOURCE_REVIEW_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_review_v0/typed_machine_readable_source_lineage_field_policy_typing_review_profile_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0_receipts"

SCHEMA_OVERLAY_SURFACE_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_schema_overlay_surface_v0.json"
SOURCE_ROLE_SCHEMA_OVERLAY_PATH = OUT_DIR / "typed_machine_readable_source_role_schema_overlay_v0.json"
FIELD_POLICY_SCHEMA_OVERLAY_PATH = OUT_DIR / "typed_machine_readable_field_policy_enrichment_schema_overlay_v0.json"
CANDIDATE_ARTIFACT_SCHEMA_OVERLAY_PATH = OUT_DIR / "typed_machine_readable_candidate_artifact_typing_schema_overlay_v0.json"
LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_PATH = OUT_DIR / "typed_machine_readable_source_lineage_requirement_schema_overlay_v0.json"
ROW_IDENTITY_SCHEMA_OVERLAY_PATH = OUT_DIR / "typed_machine_readable_row_identity_schema_overlay_v0.json"
OVERLAY_VALIDATION_MATRIX_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_validation_matrix_v0.json"
OVERLAY_NONAPPLICATION_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_nonapplication_contract_v0.json"
OVERLAY_REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_schema_overlay_review_packet_v0.json"
OVERLAY_DECISION_OPTIONS_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_schema_overlay_decision_options_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_schema_overlay_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_schema_overlay_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_schema_overlay_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_schema_overlay_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_schema_overlay_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_schema_overlay_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_REVIEW_RECEIPT_PATH,
    SOURCE_REVIEW_ASSESSMENT_PATH,
    SOURCE_FIELD_POLICY_GAP_REVIEW_PATH,
    SOURCE_LINEAGE_REQUIREMENT_REVIEW_PATH,
    SOURCE_CANDIDATE_OVERLAY_REVIEW_PATH,
    SOURCE_SCHEMA_CONTRACT_REVIEW_PATH,
    SOURCE_TYPING_RULE_REVIEW_PATH,
    SOURCE_SCHEMA_OVERLAY_INPUT_CONTRACT_PATH,
    SOURCE_REVIEW_DECISION_TABLE_PATH,
    SOURCE_REVIEW_PACKET_PATH,
    SOURCE_REVIEW_CLASSIFICATION_PATH,
    SOURCE_REVIEW_ROLLUP_PATH,
    SOURCE_REVIEW_PROFILE_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_REQUIREMENTS_REVIEWED_SCHEMA_OVERLAY_READY"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_REQUIREMENTS_REVIEWED_SCHEMA_OVERLAY_READY"
EXPECTED_NEXT = "BUILD_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_V0"

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

def records(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    for key in ["records", "slots", "field_policies", "policies"]:
        val = obj.get(key)
        if isinstance(val, list):
            return [x for x in val if isinstance(x, dict)]
    return []

def validate_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    receipt = read_json(SOURCE_REVIEW_RECEIPT_PATH)
    summary = receipt.get("machine_readable_source_lineage_field_policy_typing_review_summary", {})
    input_contract = read_json(SOURCE_SCHEMA_OVERLAY_INPUT_CONTRACT_PATH)
    field_review = read_json(SOURCE_FIELD_POLICY_GAP_REVIEW_PATH)
    lineage_review = read_json(SOURCE_LINEAGE_REQUIREMENT_REVIEW_PATH)
    overlay_review = read_json(SOURCE_CANDIDATE_OVERLAY_REVIEW_PATH)
    contract_review = read_json(SOURCE_SCHEMA_CONTRACT_REVIEW_PATH)
    rule_review = read_json(SOURCE_TYPING_RULE_REVIEW_PATH)
    classif = read_json(SOURCE_REVIEW_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_REVIEW_ROLLUP_PATH)
    profile = read_json(SOURCE_REVIEW_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_REVIEW_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_review_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_review_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_review_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"source_review_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("field_policy_gap_review_count") != 7:
        failures.append("field_policy_gap_review_count_not_7")
    if summary.get("lineage_requirement_review_count") != 105:
        failures.append("lineage_requirement_review_count_not_105")
    if summary.get("candidate_overlay_review_count") != 168:
        failures.append("candidate_overlay_review_count_not_168")
    if summary.get("typing_rule_review_count") != 1:
        failures.append("typing_rule_review_count_not_1")
    if summary.get("schema_contract_review_count") != 2:
        failures.append("schema_contract_review_count_not_2")
    if summary.get("schema_overlay_input_contract_count") != 1:
        failures.append("schema_overlay_input_contract_count_not_1")
    if summary.get("schema_overlay_built") is not False:
        failures.append("source_review_schema_overlay_already_built")
    if summary.get("schema_overlay_applied") is not False:
        failures.append("source_review_schema_overlay_applied")
    if summary.get("typing_rule_applied") is not False:
        failures.append("source_review_typing_rule_applied")
    if summary.get("field_policy_modified") is not False:
        failures.append("source_review_field_policy_modified")
    if summary.get("candidate_artifact_modified") is not False:
        failures.append("source_review_candidate_artifact_modified")
    if summary.get("rebinds_applied") is not False:
        failures.append("source_review_rebinds_applied")
    if summary.get("metadata_populated") is not False:
        failures.append("source_review_metadata_populated")
    if summary.get("ready_discriminator_count") != 0:
        failures.append("source_review_ready_discriminator_nonzero")

    if input_contract.get("contract_status") != "SCHEMA_OVERLAY_INPUT_CONTRACT_READY":
        failures.append("schema_overlay_input_contract_not_ready")
    if field_review.get("record_count") != 7:
        failures.append("field_review_record_count_not_7")
    if lineage_review.get("record_count") != 105:
        failures.append("lineage_review_record_count_not_105")
    if overlay_review.get("record_count") != 168:
        failures.append("candidate_overlay_review_record_count_not_168")
    if contract_review.get("review_status") != "SCHEMA_CONTRACTS_REVIEWED_OVERLAY_INPUT_READY":
        failures.append("schema_contract_review_not_overlay_ready")
    if rule_review.get("review_status") != "TYPING_RULE_PROPOSAL_REVIEWED_AS_SCHEMA_OVERLAY_INPUT":
        failures.append("typing_rule_review_not_overlay_input")
    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("review_classification_status_wrong")
    if roll.get("schema_overlay_built_count") != 0:
        failures.append("source_review_rollup_overlay_built_nonzero")
    if profile.get("schema_overlay_built") is not False:
        failures.append("source_review_profile_overlay_built_true")

    return failures

def build_source_role_overlay(contract_review: Dict[str, Any], rule_review: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_role_schema_overlay_v0",
        "overlay_status": "SOURCE_ROLE_SCHEMA_OVERLAY_BUILT_NOT_APPLIED",
        "source_role_required_field_count": contract_review.get("source_role_required_field_count"),
        "allowed_source_role_count": contract_review.get("allowed_source_role_count"),
        "required_candidate_artifact_fields": [
            "source_role",
            "source_object_kind",
            "producer_unit",
            "lineage_ref",
            "source_packet_ref",
            "row_identity_schema",
            "allowed_field_names",
        ],
        "allowed_source_roles": [
            "source_material",
            "source_packet",
            "field_policy",
            "diagnostic_residue",
            "receipt",
            "projection",
            "review_surface",
        ],
        "reviewed_typing_rule_conditions": rule_review.get("conditions", []),
        "overlay_applied": False,
        "candidate_artifact_modified": False,
    }

def build_field_policy_overlay(field_reviews: List[Dict[str, Any]], contract_review: Dict[str, Any]) -> Dict[str, Any]:
    fields = sorted({str(r.get("field")) for r in field_reviews if r.get("field")})
    return {
        "schema_version": "typed_machine_readable_field_policy_enrichment_schema_overlay_v0",
        "overlay_status": "FIELD_POLICY_ENRICHMENT_SCHEMA_OVERLAY_BUILT_NOT_APPLIED",
        "field_policy_gap_review_count": len(field_reviews),
        "fields_under_review": fields,
        "required_field_policy_fields": [
            "field",
            "source_class",
            "required_source_object",
            "declared_source_role",
            "producer_unit_or_allowed_producer_units",
            "lineage_ref_or_source_packet_lineage_ref",
            "row_identity_keys",
        ],
        "field_policy_required_field_count": contract_review.get("field_policy_required_field_count"),
        "reviewed_field_policy_gaps": [
            {
                "field": r.get("field"),
                "missing_policy_typing": r.get("missing_policy_typing"),
                "repair_class": r.get("repair_class"),
            }
            for r in field_reviews
        ],
        "overlay_applied": False,
        "field_policy_modified": False,
    }

def build_candidate_artifact_overlay(candidate_reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_field = Counter(str(r.get("field")) for r in candidate_reviews)
    by_status = Counter(str(r.get("review_status")) for r in candidate_reviews)
    return {
        "schema_version": "typed_machine_readable_candidate_artifact_typing_schema_overlay_v0",
        "overlay_status": "CANDIDATE_ARTIFACT_TYPING_SCHEMA_OVERLAY_BUILT_NOT_APPLIED",
        "candidate_overlay_review_count": len(candidate_reviews),
        "candidate_overlay_review_status_counts": dict(by_status),
        "candidate_overlay_field_counts": dict(by_field),
        "required_candidate_typing_fields": [
            "candidate_source_role",
            "candidate_source_object_kind",
            "candidate_producer_unit",
            "candidate_lineage_ref",
            "candidate_row_identity_schema",
            "candidate_allowed_fields",
        ],
        "records": [
            {
                "candidate_id": r.get("candidate_id"),
                "slot_id": r.get("slot_id"),
                "row_uid": r.get("row_uid"),
                "field": r.get("field"),
                "candidate_source_ref": r.get("candidate_source_ref"),
                "required_candidate_typing": r.get("required_candidate_typing"),
                "typing_gap_reasons": r.get("typing_gap_reasons"),
                "overlay_binding_status": "OVERLAY_REQUIREMENT_REPRESENTED_NOT_APPLIED",
                "authorized_to_modify_candidate": False,
            }
            for r in candidate_reviews
        ],
        "overlay_applied": False,
        "candidate_artifact_modified": False,
    }

def build_lineage_overlay(lineage_reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
    evidence_counts = Counter(str(r.get("evidence_class")) for r in lineage_reviews)
    by_slot = defaultdict(list)
    for r in lineage_reviews:
        by_slot[str(r.get("slot_id"))].append(r.get("evidence_class"))
    return {
        "schema_version": "typed_machine_readable_source_lineage_requirement_schema_overlay_v0",
        "overlay_status": "SOURCE_LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_BUILT_NOT_APPLIED",
        "lineage_requirement_review_count": len(lineage_reviews),
        "lineage_evidence_class_counts": dict(evidence_counts),
        "per_slot_evidence_classes": [
            {
                "slot_id": slot_id,
                "required_evidence_classes": sorted({str(x) for x in values}),
                "required_evidence_class_count": len(set(values)),
            }
            for slot_id, values in sorted(by_slot.items())
        ],
        "overlay_applied": False,
    }

def build_row_identity_overlay(lineage_reviews: List[Dict[str, Any]], candidate_reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
    row_identity_reqs = [r for r in lineage_reviews if r.get("evidence_class") == "ROW_IDENTITY_SCHEMA"]
    candidate_count = len(candidate_reviews)
    return {
        "schema_version": "typed_machine_readable_row_identity_schema_overlay_v0",
        "overlay_status": "ROW_IDENTITY_SCHEMA_OVERLAY_BUILT_NOT_APPLIED",
        "row_identity_requirement_count": len(row_identity_reqs),
        "candidate_artifact_scope_count": candidate_count,
        "required_row_identity_keys": [
            "slot_id",
            "row_uid",
            "field",
        ],
        "allowed_equivalent_identity_forms": [
            "explicit row_identity_schema mapping slot_id,row_uid,field",
            "declared equivalent row_identity_keys list plus row map",
            "field-policy declared row_identity_keys with candidate artifact matching keys",
        ],
        "overlay_applied": False,
    }

def decide() -> Tuple[str, List[str], str]:
    reason_codes = [
        "SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_BUILT",
        "SOURCE_ROLE_SCHEMA_OVERLAY_EMITTED",
        "FIELD_POLICY_ENRICHMENT_SCHEMA_OVERLAY_EMITTED",
        "CANDIDATE_ARTIFACT_TYPING_SCHEMA_OVERLAY_EMITTED",
        "SOURCE_LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_EMITTED",
        "ROW_IDENTITY_SCHEMA_OVERLAY_EMITTED",
        "SCHEMA_OVERLAY_VALIDATION_MATRIX_EMITTED",
        "NO_SCHEMA_OVERLAY_APPLIED",
        "NO_TYPING_RULE_APPLIED",
        "NO_FIELD_POLICY_MODIFIED",
        "NO_CANDIDATE_ARTIFACT_MODIFIED",
        "NO_REBINDS_APPLIED",
        "NO_VALUES_AUTHORIZED_OR_APPLIED",
        "NO_METADATA_POPULATION",
    ]
    status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_BUILT_REVIEW_REQUIRED"
    next_edge = "REVIEW_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_V0"
    return status, reason_codes, next_edge

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_authority_boundary_v0",
        "status": status,
        "may_build_schema_overlay_artifacts": True,
        "may_emit_overlay_review_packet": True,
        "may_apply_schema_overlay": False,
        "may_apply_typing_rule": False,
        "may_modify_field_policy": False,
        "may_modify_candidate_artifacts": False,
        "may_apply_source_row_locator": False,
        "may_apply_rebinds": False,
        "may_apply_dominance_rule": False,
        "may_authorize_values": False,
        "may_apply_values": False,
        "may_accept_null_reasons_as_final": False,
        "may_materialize_source_packet_for_review": False,
        "may_populate_metadata": False,
        "may_evaluate_discriminators": False,
        "may_refine_dominance_rule": False,
        "may_break_tie": False,
        "may_emit_candidate_values_for_target": False,
        "may_declare_target_candidate_for_review": False,
        "may_select_target_for_build": False,
        "may_accept_for_build": False,
        "may_apply_runtime_patch": False,
        "may_modify_target_files": False,
        "may_open_c5": False,
        "may_grant_general_cell1_authority": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def rollup_obj(status: str, next_edge: str, field_reviews: List[Dict[str, Any]], lineage_reviews: List[Dict[str, Any]], candidate_reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "schema_overlay_built_count": 1,
        "source_role_schema_overlay_count": 1,
        "field_policy_schema_overlay_count": 1,
        "candidate_artifact_schema_overlay_count": 1,
        "lineage_requirement_schema_overlay_count": 1,
        "row_identity_schema_overlay_count": 1,
        "field_policy_gap_review_count": len(field_reviews),
        "lineage_requirement_review_count": len(lineage_reviews),
        "candidate_overlay_review_count": len(candidate_reviews),
        "lineage_evidence_class_counts": dict(Counter(str(r.get("evidence_class")) for r in lineage_reviews)),
        "candidate_overlay_review_status_counts": dict(Counter(str(r.get("review_status")) for r in candidate_reviews)),
        "schema_overlay_applied_count": 0,
        "typing_rule_applied_count": 0,
        "field_policy_modified_count": 0,
        "candidate_artifact_modified_count": 0,
        "source_row_locator_applied_count": 0,
        "rebinds_applied_count": 0,
        "dominance_rule_applied_count": 0,
        "refinements_applied_count": 0,
        "values_authorized_count": 0,
        "values_applied_count": 0,
        "null_reason_accepted_count": 0,
        "source_packet_materialized_for_review_count": 0,
        "metadata_populated_count": 0,
        "ready_discriminator_count": 0,
        "rule_refined_count": 0,
        "tie_broken_count": 0,
        "candidate_values_filled_count": 0,
        "target_candidate_declared_for_review_count": 0,
        "target_selected_for_build_count": 0,
        "accepted_for_build_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "proposal_status_promoted_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "unbounded_payload_inspection_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": next_edge,
    }

def profile_obj(roll: Dict[str, Any]) -> Dict[str, Any]:
    zero_keys = [
        "schema_overlay_applied_count",
        "typing_rule_applied_count",
        "field_policy_modified_count",
        "candidate_artifact_modified_count",
        "source_row_locator_applied_count",
        "rebinds_applied_count",
        "dominance_rule_applied_count",
        "refinements_applied_count",
        "values_authorized_count",
        "values_applied_count",
        "null_reason_accepted_count",
        "source_packet_materialized_for_review_count",
        "metadata_populated_count",
        "ready_discriminator_count",
        "rule_refined_count",
        "tie_broken_count",
        "candidate_values_filled_count",
        "target_candidate_declared_for_review_count",
        "target_selected_for_build_count",
        "accepted_for_build_count",
        "runtime_patch_applied_count",
        "target_file_modified_count",
        "c5_opened_count",
        "general_cell1_authority_granted_count",
        "taxonomy_registry_mutation_count",
        "proposal_status_promoted_count",
        "accepted_proposal_fabricated_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "hidden_next_command_count",
        "unbounded_payload_inspection_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]
    return {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_profile_v0",
        "profile_id": "source_lineage_field_policy_schema_overlay_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "schema_overlay_built": True,
        "schema_overlay_applied": False,
        "typing_rule_applied": False,
        "field_policy_modified": False,
        "candidate_artifact_modified": False,
        "source_row_locator_applied": False,
        "rebinds_applied": False,
        "dominance_rule_applied": False,
        "values_authorized": False,
        "values_applied": False,
        "null_reasons_accepted": False,
        "source_packet_materialized_for_review": False,
        "metadata_populated": False,
        "ready_discriminator_count": 0,
        "rule_refined": False,
        "tie_broken": False,
        "candidate_values_filled": False,
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": all(roll.get(k) == 0 for k in zero_keys),
        "recommended_next": roll["recommended_next"],
        "next_command_goal": None,
    }

def report_obj(status: str, reason_codes: List[str], roll: Dict[str, Any], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The reviewed typing requirements were ready for a schema overlay; this unit builds non-applicative overlay artifacts only.",
        "schema_overlay_built_count": roll["schema_overlay_built_count"],
        "field_policy_gap_review_count": roll["field_policy_gap_review_count"],
        "lineage_requirement_review_count": roll["lineage_requirement_review_count"],
        "candidate_overlay_review_count": roll["candidate_overlay_review_count"],
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "schema_overlay_applied_count": 0,
        "typing_rule_applied_count": 0,
        "field_policy_modified_count": 0,
        "candidate_artifact_modified_count": 0,
        "rebinds_applied_count": 0,
        "values_authorized_count": 0,
        "values_applied_count": 0,
        "source_packet_materialized_for_review_count": 0,
        "metadata_populated_count": 0,
        "ready_discriminator_count": 0,
        "tie_broken_count": 0,
        "accepted_for_build_count": 0,
        "runtime_patch_applied_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "hidden_next_command_count": 0,
    }

def transition_trace_obj(status: str, reason_codes: List[str], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_transition_trace_v0",
        "trace": [
            {
                "step": "consume_overlay_input_contract",
                "question": "can reviewed typing requirements be represented as a non-applicative schema overlay",
                "answer": "yes",
                "taken": "build overlay artifacts",
            },
            {
                "step": "classify_overlay_build",
                "question": "is overlay ready for review before application",
                "answer": status,
                "reason_codes": reason_codes,
                "taken": next_edge,
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_basis()

    if failures:
        field_reviews, lineage_reviews, candidate_reviews = [], [], []
        contract_review, rule_review = {}, {}
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_BASIS_V0"
    else:
        field_reviews = records(read_json(SOURCE_FIELD_POLICY_GAP_REVIEW_PATH))
        lineage_reviews = records(read_json(SOURCE_LINEAGE_REQUIREMENT_REVIEW_PATH))
        candidate_reviews = records(read_json(SOURCE_CANDIDATE_OVERLAY_REVIEW_PATH))
        contract_review = read_json(SOURCE_SCHEMA_CONTRACT_REVIEW_PATH)
        rule_review = read_json(SOURCE_TYPING_RULE_REVIEW_PATH)
        status, reason_codes, next_edge = decide()

    source_role_overlay = build_source_role_overlay(contract_review, rule_review)
    field_policy_overlay = build_field_policy_overlay(field_reviews, contract_review)
    candidate_overlay = build_candidate_artifact_overlay(candidate_reviews)
    lineage_overlay = build_lineage_overlay(lineage_reviews)
    row_identity_overlay = build_row_identity_overlay(lineage_reviews, candidate_reviews)

    validation_matrix = {
        "schema_version": "typed_machine_readable_schema_overlay_validation_matrix_v0",
        "matrix_status": "SCHEMA_OVERLAY_VALIDATION_MATRIX_EMITTED",
        "checks": {
            "source_role_schema_overlay_built": True,
            "field_policy_schema_overlay_built": True,
            "candidate_artifact_schema_overlay_built": True,
            "lineage_requirement_schema_overlay_built": True,
            "row_identity_schema_overlay_built": True,
            "schema_overlay_application_authorized": False,
            "typing_rule_application_authorized": False,
            "field_policy_modification_authorized": False,
            "candidate_artifact_modification_authorized": False,
            "source_ref_rebind_authorized": False,
            "value_extraction_authorized": False,
            "metadata_population_authorized": False,
        },
    }

    nonapplication_contract = {
        "schema_version": "typed_machine_readable_schema_overlay_nonapplication_contract_v0",
        "contract_status": "SCHEMA_OVERLAY_BUILT_NOT_APPLIED",
        "schema_overlay_may_be_reviewed": True,
        "schema_overlay_may_be_applied": False,
        "schema_overlay_application_requires": [
            "separate review unit",
            "explicit application unit",
            "human or prevalidated schema acceptance",
        ],
        "must_not": [
            "mutate field policy",
            "mutate candidate artifacts",
            "apply typing rule",
            "apply source ref rebind",
            "extract values",
            "populate metadata",
            "mark discriminator ready",
        ],
    }

    roll = rollup_obj(status, next_edge, field_reviews, lineage_reviews, candidate_reviews)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, roll, next_edge)
    boundary = authority_boundary_obj(status)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    overlay_surface = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_surface_v0",
        "surface_status": status,
        "source_typing_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "schema_overlay_built": True,
        "schema_overlay_applied": False,
        "source_role_schema_overlay_ref": rel(SOURCE_ROLE_SCHEMA_OVERLAY_PATH),
        "field_policy_schema_overlay_ref": rel(FIELD_POLICY_SCHEMA_OVERLAY_PATH),
        "candidate_artifact_schema_overlay_ref": rel(CANDIDATE_ARTIFACT_SCHEMA_OVERLAY_PATH),
        "lineage_requirement_schema_overlay_ref": rel(LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_PATH),
        "row_identity_schema_overlay_ref": rel(ROW_IDENTITY_SCHEMA_OVERLAY_PATH),
        "validation_matrix_ref": rel(OVERLAY_VALIDATION_MATRIX_PATH),
        "nonapplication_contract_ref": rel(OVERLAY_NONAPPLICATION_CONTRACT_PATH),
        "recommended_next": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    review_packet = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_review_packet_v0",
        "review_packet_status": "SCHEMA_OVERLAY_REVIEW_REQUIRED",
        "question": "Review the non-applicative schema overlay before any overlay application or source-ref rebind.",
        "allowed_responses": [
            "ACCEPT_SCHEMA_OVERLAY_FOR_APPLICATION_UNIT",
            "REPAIR_SCHEMA_OVERLAY",
            "FREEZE_SCHEMA_OVERLAY_AS_REFERENCE",
        ],
        "default_recommended_response": "REVIEW_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_V0",
        "not_authorized": [
            "schema overlay application",
            "typing rule application",
            "field policy modification",
            "candidate artifact modification",
            "source-ref rebind",
            "value extraction",
            "metadata population",
        ],
    }

    decision_options = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_decision_options_v0",
        "decision_options_status": "SCHEMA_OVERLAY_DECISION_OPTIONS_EMITTED",
        "safe_options": [
            {
                "option": "REVIEW_SCHEMA_OVERLAY",
                "recommended": True,
                "next_unit": "REVIEW_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_V0",
                "meaning": "Review overlay completeness before any application.",
            },
            {
                "option": "REPAIR_SCHEMA_OVERLAY",
                "recommended": False,
                "next_unit": "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_V0",
                "meaning": "Use if overlay coverage or contract shape is insufficient.",
            },
            {
                "option": "FREEZE_AS_REFERENCE",
                "recommended": False,
                "next_unit": "FREEZE_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_V0",
                "meaning": "Preserve this as a reference object without application.",
            },
        ],
    }

    classification = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "schema_overlay_built": True,
        "schema_overlay_applied": False,
        "source_role_schema_overlay_count": 1,
        "field_policy_schema_overlay_count": 1,
        "candidate_artifact_schema_overlay_count": 1,
        "lineage_requirement_schema_overlay_count": 1,
        "row_identity_schema_overlay_count": 1,
        "field_policy_gap_review_count": roll["field_policy_gap_review_count"],
        "lineage_requirement_review_count": roll["lineage_requirement_review_count"],
        "candidate_overlay_review_count": roll["candidate_overlay_review_count"],
        "typing_rule_applied": False,
        "field_policy_modified": False,
        "candidate_artifact_modified": False,
        "source_row_locator_applied": False,
        "rebinds_applied": False,
        "dominance_rule_applied": False,
        "values_authorized": False,
        "values_applied": False,
        "null_reasons_accepted": False,
        "source_packet_materialized_for_review": False,
        "metadata_populated": False,
        "ready_discriminator_count": 0,
        "real_tie_proven": False,
        "rule_refined": False,
        "tie_broken": False,
        "candidate_values_filled": False,
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "recommended_next": next_edge,
        "next_command_goal": None,
    }

    write_json(SCHEMA_OVERLAY_SURFACE_PATH, overlay_surface)
    write_json(SOURCE_ROLE_SCHEMA_OVERLAY_PATH, source_role_overlay)
    write_json(FIELD_POLICY_SCHEMA_OVERLAY_PATH, field_policy_overlay)
    write_json(CANDIDATE_ARTIFACT_SCHEMA_OVERLAY_PATH, candidate_overlay)
    write_json(LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_PATH, lineage_overlay)
    write_json(ROW_IDENTITY_SCHEMA_OVERLAY_PATH, row_identity_overlay)
    write_json(OVERLAY_VALIDATION_MATRIX_PATH, validation_matrix)
    write_json(OVERLAY_NONAPPLICATION_CONTRACT_PATH, nonapplication_contract)
    write_json(OVERLAY_REVIEW_PACKET_PATH, review_packet)
    write_json(OVERLAY_DECISION_OPTIONS_PATH, decision_options)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(AUTHORITY_BOUNDARY_PATH, boundary)
    write_json(ROLLUP_PATH, roll)
    write_json(PROFILE_PATH, prof)
    write_json(REPORT_PATH, rep)
    write_json(TRANSITION_TRACE_PATH, trace)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        roll["source_mutation_count"] = 1
        rep["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, roll)
        write_json(REPORT_PATH, rep)

    acceptance_gate_results = {
        "SCHEMA_OVERLAY_0_SOURCE_REVIEW_RECEIPT_CONSUMED": SOURCE_REVIEW_RECEIPT_PATH.exists(),
        "SCHEMA_OVERLAY_1_INPUT_CONTRACT_READY": read_json(SOURCE_SCHEMA_OVERLAY_INPUT_CONTRACT_PATH).get("contract_status") == "SCHEMA_OVERLAY_INPUT_CONTRACT_READY",
        "SCHEMA_OVERLAY_2_OVERLAY_SURFACE_EMITTED": SCHEMA_OVERLAY_SURFACE_PATH.exists(),
        "SCHEMA_OVERLAY_3_SOURCE_ROLE_OVERLAY_EMITTED": SOURCE_ROLE_SCHEMA_OVERLAY_PATH.exists(),
        "SCHEMA_OVERLAY_4_FIELD_POLICY_OVERLAY_EMITTED": FIELD_POLICY_SCHEMA_OVERLAY_PATH.exists(),
        "SCHEMA_OVERLAY_5_CANDIDATE_ARTIFACT_OVERLAY_EMITTED": CANDIDATE_ARTIFACT_SCHEMA_OVERLAY_PATH.exists(),
        "SCHEMA_OVERLAY_6_LINEAGE_REQUIREMENT_OVERLAY_EMITTED": LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_PATH.exists(),
        "SCHEMA_OVERLAY_7_ROW_IDENTITY_OVERLAY_EMITTED": ROW_IDENTITY_SCHEMA_OVERLAY_PATH.exists(),
        "SCHEMA_OVERLAY_8_VALIDATION_MATRIX_EMITTED": OVERLAY_VALIDATION_MATRIX_PATH.exists(),
        "SCHEMA_OVERLAY_9_NONAPPLICATION_CONTRACT_EMITTED": OVERLAY_NONAPPLICATION_CONTRACT_PATH.exists(),
        "SCHEMA_OVERLAY_10_REVIEW_PACKET_EMITTED": OVERLAY_REVIEW_PACKET_PATH.exists(),
        "SCHEMA_OVERLAY_11_SCHEMA_OVERLAY_BUILT": roll["schema_overlay_built_count"] == 1,
        "SCHEMA_OVERLAY_12_NO_SCHEMA_OVERLAY_APPLIED": roll["schema_overlay_applied_count"] == 0,
        "SCHEMA_OVERLAY_13_NO_TYPING_RULE_APPLIED": roll["typing_rule_applied_count"] == 0,
        "SCHEMA_OVERLAY_14_NO_FIELD_POLICY_MODIFIED": roll["field_policy_modified_count"] == 0,
        "SCHEMA_OVERLAY_15_NO_CANDIDATE_ARTIFACT_MODIFIED": roll["candidate_artifact_modified_count"] == 0,
        "SCHEMA_OVERLAY_16_NO_ROW_LOCATOR_APPLIED": roll["source_row_locator_applied_count"] == 0,
        "SCHEMA_OVERLAY_17_NO_REBINDS_APPLIED": roll["rebinds_applied_count"] == 0,
        "SCHEMA_OVERLAY_18_NO_DOMINANCE_RULE_APPLIED": roll["dominance_rule_applied_count"] == 0,
        "SCHEMA_OVERLAY_19_NO_VALUES_AUTHORIZED": roll["values_authorized_count"] == 0,
        "SCHEMA_OVERLAY_20_NO_VALUES_APPLIED": roll["values_applied_count"] == 0,
        "SCHEMA_OVERLAY_21_NO_NULL_REASONS_ACCEPTED": roll["null_reason_accepted_count"] == 0,
        "SCHEMA_OVERLAY_22_NO_SOURCE_PACKET_MATERIALIZED": roll["source_packet_materialized_for_review_count"] == 0,
        "SCHEMA_OVERLAY_23_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "SCHEMA_OVERLAY_24_NO_DISCRIMINATOR_READY": roll["ready_discriminator_count"] == 0,
        "SCHEMA_OVERLAY_25_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "SCHEMA_OVERLAY_26_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "SCHEMA_OVERLAY_27_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "SCHEMA_OVERLAY_28_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classification["target_candidate_declared_for_review"] is False,
        "SCHEMA_OVERLAY_29_NO_TARGET_SELECTED_FOR_BUILD": classification["target_selected_for_build"] is False,
        "SCHEMA_OVERLAY_30_NO_ACCEPTED_FOR_BUILD": classification["accepted_for_build"] is False,
        "SCHEMA_OVERLAY_31_NO_RUNTIME_PATCH": classification["runtime_patch_authorized"] is False,
        "SCHEMA_OVERLAY_32_NO_TARGET_FILE_MODIFICATION": classification["target_file_modification_authorized"] is False,
        "SCHEMA_OVERLAY_33_NO_C5_OPENED": classification["c5_authorized"] is False,
        "SCHEMA_OVERLAY_34_NO_GENERAL_CELL1_AUTHORITY": classification["general_cell1_authority_granted"] is False,
        "SCHEMA_OVERLAY_35_NO_LATEST_FILE_GUESSING": classification["latest_file_guessing"] is False,
        "SCHEMA_OVERLAY_36_NO_MTIME_SELECTION": classification["mtime_selection"] is False,
        "SCHEMA_OVERLAY_37_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "SCHEMA_OVERLAY_38_ACCEPTANCE_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "SCHEMA_OVERLAY_39_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "field_reviews": roll["field_policy_gap_review_count"],
        "lineage_reviews": roll["lineage_requirement_review_count"],
        "candidate_reviews": roll["candidate_overlay_review_count"],
        "overlay_built": roll["schema_overlay_built_count"],
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_typing_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "machine_readable_source_lineage_field_policy_schema_overlay_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "schema_overlay_built": True,
            "schema_overlay_applied": False,
            "source_role_schema_overlay_count": roll["source_role_schema_overlay_count"],
            "field_policy_schema_overlay_count": roll["field_policy_schema_overlay_count"],
            "candidate_artifact_schema_overlay_count": roll["candidate_artifact_schema_overlay_count"],
            "lineage_requirement_schema_overlay_count": roll["lineage_requirement_schema_overlay_count"],
            "row_identity_schema_overlay_count": roll["row_identity_schema_overlay_count"],
            "field_policy_gap_review_count": roll["field_policy_gap_review_count"],
            "lineage_requirement_review_count": roll["lineage_requirement_review_count"],
            "candidate_overlay_review_count": roll["candidate_overlay_review_count"],
            "lineage_evidence_class_counts": roll["lineage_evidence_class_counts"],
            "candidate_overlay_review_status_counts": roll["candidate_overlay_review_status_counts"],
            "typing_rule_applied": False,
            "field_policy_modified": False,
            "candidate_artifact_modified": False,
            "source_row_locator_applied": False,
            "rebinds_applied": False,
            "dominance_rule_applied": False,
            "values_authorized": False,
            "values_applied": False,
            "null_reasons_accepted": False,
            "source_packet_materialized_for_review": False,
            "metadata_populated": False,
            "ready_discriminator_count": 0,
            "real_tie_proven": False,
            "rule_refined": False,
            "tie_broken": False,
            "candidate_values_filled": False,
            "target_candidate_declared_for_review": False,
            "target_selected_for_build": False,
            "accepted_for_build": False,
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "general_cell1_authority_granted": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
            "bad_counters_zero": prof["bad_counters_zero"],
            "recommended_next": next_edge,
        },
        "aggregate_metrics": rep,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "schema_overlay_surface": rel(SCHEMA_OVERLAY_SURFACE_PATH),
            "source_role_schema_overlay": rel(SOURCE_ROLE_SCHEMA_OVERLAY_PATH),
            "field_policy_schema_overlay": rel(FIELD_POLICY_SCHEMA_OVERLAY_PATH),
            "candidate_artifact_schema_overlay": rel(CANDIDATE_ARTIFACT_SCHEMA_OVERLAY_PATH),
            "lineage_requirement_schema_overlay": rel(LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_PATH),
            "row_identity_schema_overlay": rel(ROW_IDENTITY_SCHEMA_OVERLAY_PATH),
            "overlay_validation_matrix": rel(OVERLAY_VALIDATION_MATRIX_PATH),
            "overlay_nonapplication_contract": rel(OVERLAY_NONAPPLICATION_CONTRACT_PATH),
            "overlay_review_packet": rel(OVERLAY_REVIEW_PACKET_PATH),
            "overlay_decision_options": rel(OVERLAY_DECISION_OPTIONS_PATH),
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
    print(f"source_lineage_field_policy_schema_overlay_receipt_id={receipt_id}")
    print(f"source_lineage_field_policy_schema_overlay_receipt_path={rel(receipt_path)}")
    print(f"source_lineage_field_policy_schema_overlay_surface_path={rel(SCHEMA_OVERLAY_SURFACE_PATH)}")
    print(f"source_role_schema_overlay_path={rel(SOURCE_ROLE_SCHEMA_OVERLAY_PATH)}")
    print(f"field_policy_schema_overlay_path={rel(FIELD_POLICY_SCHEMA_OVERLAY_PATH)}")
    print(f"candidate_artifact_schema_overlay_path={rel(CANDIDATE_ARTIFACT_SCHEMA_OVERLAY_PATH)}")
    print(f"lineage_requirement_schema_overlay_path={rel(LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_PATH)}")
    print(f"row_identity_schema_overlay_path={rel(ROW_IDENTITY_SCHEMA_OVERLAY_PATH)}")
    print(f"overlay_validation_matrix_path={rel(OVERLAY_VALIDATION_MATRIX_PATH)}")
    print(f"schema_overlay_rollup_path={rel(ROLLUP_PATH)}")
    print(f"schema_overlay_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
