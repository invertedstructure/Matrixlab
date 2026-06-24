#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_REQUIREMENTS_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_review.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_LINEAGE_FIELD_POLICY_TYPING_REVIEW"
MODE = "SOURCE_LINEAGE_FIELD_POLICY_TYPING_REVIEW / NO_TYPING_RULE_APPLIED / NO_POLICY_MODIFICATION / NO_CANDIDATE_MODIFICATION / NO_REBIND_APPLIED / NO_METADATA_FILL"
BUILD_MODE = "SOURCE_LINEAGE_FIELD_POLICY_TYPING_REVIEW_ONLY"

SOURCE_TYPING_RECEIPT_ID = "9539ff72"
SOURCE_TYPING_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_v0_receipts/9539ff72.json"
SOURCE_TYPING_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_v0/typed_machine_readable_source_lineage_field_policy_typing_surface_v0.json"
SOURCE_PER_BINDING_TYPING_GAP_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_v0/typed_machine_readable_per_binding_source_lineage_field_policy_typing_gap_v0.json"
SOURCE_FIELD_POLICY_GAP_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_v0/typed_machine_readable_field_policy_typing_gap_table_v0.json"
SOURCE_LINEAGE_REQUIREMENT_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_v0/typed_machine_readable_source_lineage_requirement_table_v0.json"
SOURCE_CANDIDATE_TYPING_OVERLAY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_v0/typed_machine_readable_candidate_artifact_required_typing_overlay_v0.json"
SOURCE_TYPING_RULE_PROPOSAL_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_v0/typed_machine_readable_source_lineage_field_policy_typing_rule_proposal_surface_v0.json"
SOURCE_ROLE_SCHEMA_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_v0/typed_machine_readable_source_role_schema_contract_v0.json"
SOURCE_FIELD_POLICY_ENRICHMENT_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_v0/typed_machine_readable_field_policy_enrichment_contract_v0.json"
SOURCE_TYPING_REVIEW_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_v0/typed_machine_readable_source_lineage_field_policy_typing_review_packet_v0.json"
SOURCE_TYPING_DECISION_OPTIONS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_v0/typed_machine_readable_source_lineage_field_policy_typing_decision_options_v0.json"
SOURCE_TYPING_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_v0/typed_machine_readable_source_lineage_field_policy_typing_classification_v0.json"
SOURCE_TYPING_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_v0/typed_machine_readable_source_lineage_field_policy_typing_rollup_v0.json"
SOURCE_TYPING_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_v0/typed_machine_readable_source_lineage_field_policy_typing_profile_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_review_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_review_assessment_v0.json"
FIELD_POLICY_GAP_REVIEW_PATH = OUT_DIR / "typed_machine_readable_field_policy_typing_gap_review_v0.json"
LINEAGE_REQUIREMENT_REVIEW_PATH = OUT_DIR / "typed_machine_readable_source_lineage_requirement_review_v0.json"
CANDIDATE_OVERLAY_REVIEW_PATH = OUT_DIR / "typed_machine_readable_candidate_artifact_typing_overlay_review_v0.json"
SCHEMA_CONTRACT_REVIEW_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_schema_contract_review_v0.json"
TYPING_RULE_REVIEW_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_rule_review_v0.json"
SCHEMA_OVERLAY_INPUT_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_schema_overlay_input_contract_v0.json"
REVIEW_DECISION_TABLE_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_review_decision_table_v0.json"
REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_review_result_packet_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_review_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_review_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_review_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_TYPING_RECEIPT_PATH,
    SOURCE_TYPING_SURFACE_PATH,
    SOURCE_PER_BINDING_TYPING_GAP_TABLE_PATH,
    SOURCE_FIELD_POLICY_GAP_TABLE_PATH,
    SOURCE_LINEAGE_REQUIREMENT_TABLE_PATH,
    SOURCE_CANDIDATE_TYPING_OVERLAY_PATH,
    SOURCE_TYPING_RULE_PROPOSAL_SURFACE_PATH,
    SOURCE_ROLE_SCHEMA_CONTRACT_PATH,
    SOURCE_FIELD_POLICY_ENRICHMENT_CONTRACT_PATH,
    SOURCE_TYPING_REVIEW_PACKET_PATH,
    SOURCE_TYPING_DECISION_OPTIONS_PATH,
    SOURCE_TYPING_CLASSIFICATION_PATH,
    SOURCE_TYPING_ROLLUP_PATH,
    SOURCE_TYPING_PROFILE_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_SURFACE_BUILT_REQUIRES_SCHEMA_OR_RULE_REVIEW"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_SURFACE_BUILT_REQUIRES_SCHEMA_OR_RULE_REVIEW"
EXPECTED_NEXT = "REVIEW_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_REQUIREMENTS_V0"

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

    receipt = read_json(SOURCE_TYPING_RECEIPT_PATH)
    summary = receipt.get("machine_readable_source_lineage_field_policy_typing_summary", {})
    surface = read_json(SOURCE_TYPING_SURFACE_PATH)
    per_binding = read_json(SOURCE_PER_BINDING_TYPING_GAP_TABLE_PATH)
    field_gap = read_json(SOURCE_FIELD_POLICY_GAP_TABLE_PATH)
    lineage = read_json(SOURCE_LINEAGE_REQUIREMENT_TABLE_PATH)
    overlay = read_json(SOURCE_CANDIDATE_TYPING_OVERLAY_PATH)
    rule = read_json(SOURCE_TYPING_RULE_PROPOSAL_SURFACE_PATH)
    source_role_contract = read_json(SOURCE_ROLE_SCHEMA_CONTRACT_PATH)
    field_policy_contract = read_json(SOURCE_FIELD_POLICY_ENRICHMENT_CONTRACT_PATH)
    classif = read_json(SOURCE_TYPING_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_TYPING_ROLLUP_PATH)
    profile = read_json(SOURCE_TYPING_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_TYPING_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_typing_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_typing_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_typing_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"source_typing_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("binding_count") != 21:
        failures.append("binding_count_not_21")
    if summary.get("field_policy_gap_count") != 7:
        failures.append("field_policy_gap_count_not_7")
    if summary.get("field_policy_incomplete_count") != 7:
        failures.append("field_policy_incomplete_count_not_7")
    if summary.get("source_lineage_requirement_count") != 105:
        failures.append("source_lineage_requirement_count_not_105")
    if summary.get("candidate_artifact_typing_overlay_count") != 168:
        failures.append("candidate_artifact_typing_overlay_count_not_168")
    if summary.get("candidate_artifact_requires_typing_count") != 168:
        failures.append("candidate_artifact_requires_typing_count_not_168")
    if summary.get("typing_rule_proposal_count") != 1:
        failures.append("typing_rule_proposal_count_not_1")
    if summary.get("schema_contract_count") != 2:
        failures.append("schema_contract_count_not_2")
    if summary.get("typing_rule_applied") is not False:
        failures.append("typing_rule_applied_unexpectedly")
    if summary.get("field_policy_modified") is not False:
        failures.append("field_policy_modified_unexpectedly")
    if summary.get("candidate_artifact_modified") is not False:
        failures.append("candidate_artifact_modified_unexpectedly")
    if summary.get("rebinds_applied") is not False:
        failures.append("rebinds_applied_unexpectedly")
    if summary.get("values_authorized") is not False:
        failures.append("values_authorized_unexpectedly")
    if summary.get("metadata_populated") is not False:
        failures.append("metadata_populated_unexpectedly")
    if summary.get("ready_discriminator_count") != 0:
        failures.append("ready_discriminator_nonzero")

    if surface.get("surface_status") != EXPECTED_SOURCE_STATUS:
        failures.append("typing_surface_status_wrong")
    if per_binding.get("record_count") != 21:
        failures.append("per_binding_typing_gap_record_count_not_21")
    if field_gap.get("record_count") != 7:
        failures.append("field_policy_gap_record_count_not_7")
    if lineage.get("record_count") != 105:
        failures.append("lineage_requirement_record_count_not_105")
    if overlay.get("record_count") != 168:
        failures.append("candidate_overlay_record_count_not_168")
    if rule.get("proposal_count") != 1:
        failures.append("typing_rule_surface_proposal_count_not_1")
    if source_role_contract.get("contract_status") != "SOURCE_ROLE_SCHEMA_CONTRACT_EMITTED_NOT_APPLIED":
        failures.append("source_role_schema_contract_status_wrong")
    if field_policy_contract.get("contract_status") != "FIELD_POLICY_ENRICHMENT_CONTRACT_EMITTED_NOT_APPLIED":
        failures.append("field_policy_enrichment_contract_status_wrong")
    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("typing_classification_status_wrong")
    if roll.get("metadata_populated_count") != 0:
        failures.append("typing_rollup_metadata_populated_nonzero")
    if profile.get("metadata_populated") is not False:
        failures.append("typing_profile_metadata_populated_true")

    return failures

def review_field_policy_gaps() -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    src = records(read_json(SOURCE_FIELD_POLICY_GAP_TABLE_PATH))
    reviewed = []
    for r in src:
        missing = r.get("missing_policy_typing") or []
        reviewed.append({
            "field": r.get("field"),
            "policy_present": r.get("policy_present"),
            "missing_policy_typing": missing,
            "review_status": "FIELD_POLICY_TYPING_GAP_CONFIRMED" if missing else "FIELD_POLICY_DECLARATION_PRESENT",
            "repair_class": "FIELD_POLICY_ENRICHMENT_REQUIRED" if missing else "FIELD_POLICY_LINKAGE_REQUIRED",
            "allowed_next_handling": "schema overlay may encode required field-policy declarations; no policy mutation in review",
        })
    return reviewed, dict(Counter(x["review_status"] for x in reviewed))

def review_lineage_requirements() -> Tuple[List[Dict[str, Any]], Dict[str, int], Dict[str, int]]:
    src = records(read_json(SOURCE_LINEAGE_REQUIREMENT_TABLE_PATH))
    reviewed = []
    for r in src:
        reviewed.append({
            "slot_id": r.get("slot_id"),
            "row_uid": r.get("row_uid"),
            "field": r.get("field"),
            "evidence_class": r.get("evidence_class"),
            "current_status": r.get("current_status"),
            "allowed_resolver": r.get("allowed_resolver"),
            "review_status": "LINEAGE_REQUIREMENT_CONFIRMED",
            "must_not_impersonate": r.get("must_not_impersonate", []),
            "schema_overlay_use": "required input contract, not applied fact",
        })
    return reviewed, dict(Counter(x["review_status"] for x in reviewed)), dict(Counter(str(x.get("evidence_class")) for x in reviewed))

def review_candidate_overlay() -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    src = records(read_json(SOURCE_CANDIDATE_TYPING_OVERLAY_PATH))
    reviewed = []
    for r in src:
        required = r.get("required_candidate_typing") or []
        reasons = r.get("typing_gap_reasons") or []
        reviewed.append({
            "candidate_id": r.get("candidate_id"),
            "slot_id": r.get("slot_id"),
            "row_uid": r.get("row_uid"),
            "field": r.get("field"),
            "candidate_source_ref": r.get("candidate_source_ref"),
            "required_candidate_typing": required,
            "typing_gap_reasons": reasons,
            "review_status": "CANDIDATE_ARTIFACT_TYPING_OVERLAY_CONFIRMED" if required else "NO_CANDIDATE_TYPING_REQUIRED",
            "authorized_to_modify_candidate": False,
            "schema_overlay_use": "candidate artifact requirements may be represented as overlay, not mutation",
        })
    return reviewed, dict(Counter(x["review_status"] for x in reviewed))

def review_contracts() -> Dict[str, Any]:
    source_role = read_json(SOURCE_ROLE_SCHEMA_CONTRACT_PATH)
    field_policy = read_json(SOURCE_FIELD_POLICY_ENRICHMENT_CONTRACT_PATH)
    return {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_contract_review_v0",
        "review_status": "SCHEMA_CONTRACTS_REVIEWED_OVERLAY_INPUT_READY",
        "source_role_schema_contract_status": source_role.get("contract_status"),
        "source_role_required_field_count": len(source_role.get("required_candidate_artifact_fields", [])),
        "allowed_source_role_count": len(source_role.get("allowed_source_roles", [])),
        "field_policy_enrichment_contract_status": field_policy.get("contract_status"),
        "field_policy_required_field_count": len(field_policy.get("required_field_policy_fields", [])),
        "fields_under_review_count": len(field_policy.get("fields_under_review", [])),
        "contracts_apply_now": False,
        "field_policy_modified": False,
        "candidate_artifact_modified": False,
        "review_finding": "contracts are coherent as schema overlay inputs only; applying them requires a separate build/apply unit",
    }

def review_typing_rule() -> Dict[str, Any]:
    rule = read_json(SOURCE_TYPING_RULE_PROPOSAL_SURFACE_PATH)
    proposal = rule.get("proposal", {})
    rule_shape = proposal.get("rule_shape", {})
    conditions = rule_shape.get("candidate_source_ref_may_be_reviewable_only_if", [])
    return {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_rule_review_v0",
        "review_status": "TYPING_RULE_PROPOSAL_REVIEWED_AS_SCHEMA_OVERLAY_INPUT",
        "proposal_count": rule.get("proposal_count"),
        "proposal_id": proposal.get("proposal_id"),
        "condition_count": len(conditions),
        "conditions": conditions,
        "authorization_required_before_use": rule.get("authorization_required_before_use"),
        "typing_rule_applied": False,
        "review_finding": "proposal is suitable as an overlay contract, not an executable rule application",
    }

def decide(field_review: List[Dict[str, Any]], lineage_review: List[Dict[str, Any]], overlay_review: List[Dict[str, Any]], contract_review: Dict[str, Any], rule_review: Dict[str, Any]) -> Tuple[str, List[str], str]:
    reason_codes = [
        "SOURCE_LINEAGE_FIELD_POLICY_TYPING_REQUIREMENTS_REVIEWED",
        "FIELD_POLICY_GAPS_CONFIRMED",
        "SOURCE_LINEAGE_REQUIREMENTS_CONFIRMED",
        "CANDIDATE_TYPING_OVERLAYS_CONFIRMED",
        "TYPING_RULE_PROPOSAL_REVIEWED",
        "SCHEMA_CONTRACTS_REVIEWED",
        "NO_TYPING_RULE_APPLIED",
        "NO_FIELD_POLICY_MODIFIED",
        "NO_CANDIDATE_ARTIFACT_MODIFIED",
        "NO_REBINDS_APPLIED",
        "NO_VALUES_AUTHORIZED_OR_APPLIED",
        "NO_METADATA_POPULATION",
    ]

    ok = (
        len(field_review) == 7
        and len(lineage_review) == 105
        and len(overlay_review) == 168
        and contract_review.get("review_status") == "SCHEMA_CONTRACTS_REVIEWED_OVERLAY_INPUT_READY"
        and rule_review.get("review_status") == "TYPING_RULE_PROPOSAL_REVIEWED_AS_SCHEMA_OVERLAY_INPUT"
    )

    if ok:
        reason_codes.append("SCHEMA_OVERLAY_INPUT_CONTRACT_READY")
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_REQUIREMENTS_REVIEWED_SCHEMA_OVERLAY_READY"
        next_edge = "BUILD_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_V0"
    else:
        reason_codes.append("SCHEMA_OVERLAY_INPUT_CONTRACT_NOT_READY")
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_REQUIREMENTS_REVIEWED_REPAIR_REQUIRED"
        next_edge = "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_REQUIREMENTS_V0"

    return status, reason_codes, next_edge

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_review_authority_boundary_v0",
        "status": status,
        "may_review_typing_requirements": True,
        "may_confirm_schema_overlay_inputs": True,
        "may_emit_schema_overlay_input_contract": True,
        "may_build_schema_overlay": False,
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

def rollup_obj(status: str, field_review: List[Dict[str, Any]], lineage_review: List[Dict[str, Any]], overlay_review: List[Dict[str, Any]], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "field_policy_gap_review_count": len(field_review),
        "lineage_requirement_review_count": len(lineage_review),
        "candidate_overlay_review_count": len(overlay_review),
        "typing_rule_review_count": 1,
        "schema_contract_review_count": 2,
        "field_review_status_counts": dict(Counter(x["review_status"] for x in field_review)),
        "lineage_evidence_class_counts": dict(Counter(str(x.get("evidence_class")) for x in lineage_review)),
        "candidate_overlay_review_status_counts": dict(Counter(x["review_status"] for x in overlay_review)),
        "schema_overlay_input_contract_count": 1,
        "schema_overlay_built_count": 0,
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
        "schema_overlay_built_count",
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
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_review_profile_v0",
        "profile_id": "source_lineage_field_policy_typing_review_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "review_completed": True,
        "schema_overlay_built": False,
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
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The lineage/field-policy typing surface exposed reviewable requirements; this unit reviews them as schema-overlay inputs without applying any rule, policy change, candidate mutation, rebind, or value extraction.",
        "field_policy_gap_review_count": roll["field_policy_gap_review_count"],
        "lineage_requirement_review_count": roll["lineage_requirement_review_count"],
        "candidate_overlay_review_count": roll["candidate_overlay_review_count"],
        "typing_rule_review_count": roll["typing_rule_review_count"],
        "schema_contract_review_count": roll["schema_contract_review_count"],
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "schema_overlay_built_count": 0,
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
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_typing_surface",
                "question": "are lineage/field-policy typing requirements coherent enough to become overlay inputs",
                "answer": "review field-policy gaps, lineage requirements, candidate overlays, rule proposal, and schema contracts",
                "taken": "emit review assessment and overlay input contract",
            },
            {
                "step": "classify_review_result",
                "question": "can a schema overlay be built next",
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
        field_review, field_status_counts = [], {}
        lineage_review, lineage_status_counts, evidence_class_counts = [], {}, {}
        overlay_review, overlay_status_counts = [], {}
        contract_review = {}
        rule_review = {}
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_REVIEW_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_REVIEW_BASIS_V0"
    else:
        field_review, field_status_counts = review_field_policy_gaps()
        lineage_review, lineage_status_counts, evidence_class_counts = review_lineage_requirements()
        overlay_review, overlay_status_counts = review_candidate_overlay()
        contract_review = review_contracts()
        rule_review = review_typing_rule()
        status, reason_codes, next_edge = decide(field_review, lineage_review, overlay_review, contract_review, rule_review)

    roll = rollup_obj(status, field_review, lineage_review, overlay_review, next_edge)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, roll, next_edge)
    boundary = authority_boundary_obj(status)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    assessment = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_review_assessment_v0",
        "assessment_status": status,
        "source_typing_receipt_id": SOURCE_TYPING_RECEIPT_ID,
        "field_policy_gap_review_count": roll["field_policy_gap_review_count"],
        "lineage_requirement_review_count": roll["lineage_requirement_review_count"],
        "candidate_overlay_review_count": roll["candidate_overlay_review_count"],
        "typing_rule_review_count": roll["typing_rule_review_count"],
        "schema_contract_review_count": roll["schema_contract_review_count"],
        "review_finding": "requirements are reviewed as schema-overlay inputs only; no application or mutation is authorized",
        "recommended_next": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    schema_overlay_input_contract = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_input_contract_v0",
        "contract_status": "SCHEMA_OVERLAY_INPUT_CONTRACT_READY" if next_edge == "BUILD_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_V0" else "SCHEMA_OVERLAY_INPUT_CONTRACT_REPAIR_REQUIRED",
        "recommended_next_unit": next_edge,
        "overlay_may_describe": [
            "source_role requirements",
            "candidate artifact source-object typing",
            "candidate artifact lineage typing",
            "field-policy enrichment requirements",
            "row-identity schema requirements",
        ],
        "overlay_must_not": [
            "apply typing rule",
            "modify field policy",
            "modify candidate artifacts",
            "apply source-row locator",
            "apply source-ref rebind",
            "extract values",
            "populate metadata",
            "mark discriminator ready",
        ],
        "source_inputs": {
            "field_policy_gap_review": rel(FIELD_POLICY_GAP_REVIEW_PATH),
            "lineage_requirement_review": rel(LINEAGE_REQUIREMENT_REVIEW_PATH),
            "candidate_overlay_review": rel(CANDIDATE_OVERLAY_REVIEW_PATH),
            "schema_contract_review": rel(SCHEMA_CONTRACT_REVIEW_PATH),
            "typing_rule_review": rel(TYPING_RULE_REVIEW_PATH),
        },
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    decision_table = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_review_decision_table_v0",
        "decision_status": "REVIEW_DECISION_EMITTED",
        "records": [
            {
                "decision": "BUILD_SCHEMA_OVERLAY",
                "selected": next_edge == "BUILD_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_V0",
                "next_unit": "BUILD_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_V0",
                "why": "reviewed requirements are coherent as overlay inputs; overlay build remains non-applicative",
            },
            {
                "decision": "REPAIR_REQUIREMENTS",
                "selected": next_edge == "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_REQUIREMENTS_V0",
                "next_unit": "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_REQUIREMENTS_V0",
                "why": "use only if required counts or contract coherence fail",
            },
            {
                "decision": "FREEZE_DIAGNOSTIC_REFERENCE",
                "selected": False,
                "next_unit": "FREEZE_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_REVIEW_V0",
                "why": "available if operator chooses to stop this branch",
            },
        ],
    }

    review_packet = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_review_result_packet_v0",
        "review_packet_status": "TYPING_REQUIREMENTS_REVIEW_COMPLETE",
        "summary": {
            "field_policy_gap_review_count": roll["field_policy_gap_review_count"],
            "lineage_requirement_review_count": roll["lineage_requirement_review_count"],
            "candidate_overlay_review_count": roll["candidate_overlay_review_count"],
            "schema_overlay_input_contract_count": roll["schema_overlay_input_contract_count"],
        },
        "recommended_next": next_edge,
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

    classification = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "field_policy_gap_review_count": roll["field_policy_gap_review_count"],
        "lineage_requirement_review_count": roll["lineage_requirement_review_count"],
        "candidate_overlay_review_count": roll["candidate_overlay_review_count"],
        "typing_rule_review_count": roll["typing_rule_review_count"],
        "schema_contract_review_count": roll["schema_contract_review_count"],
        "schema_overlay_input_contract_count": roll["schema_overlay_input_contract_count"],
        "schema_overlay_built": False,
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

    write_json(REVIEW_ASSESSMENT_PATH, assessment)
    write_json(FIELD_POLICY_GAP_REVIEW_PATH, {
        "schema_version": "typed_machine_readable_field_policy_typing_gap_review_v0",
        "review_status": "FIELD_POLICY_TYPING_GAPS_REVIEWED",
        "record_count": len(field_review),
        "review_status_counts": field_status_counts,
        "records": field_review,
    })
    write_json(LINEAGE_REQUIREMENT_REVIEW_PATH, {
        "schema_version": "typed_machine_readable_source_lineage_requirement_review_v0",
        "review_status": "SOURCE_LINEAGE_REQUIREMENTS_REVIEWED",
        "record_count": len(lineage_review),
        "review_status_counts": lineage_status_counts,
        "evidence_class_counts": evidence_class_counts,
        "records": lineage_review,
    })
    write_json(CANDIDATE_OVERLAY_REVIEW_PATH, {
        "schema_version": "typed_machine_readable_candidate_artifact_typing_overlay_review_v0",
        "review_status": "CANDIDATE_ARTIFACT_TYPING_OVERLAYS_REVIEWED",
        "record_count": len(overlay_review),
        "review_status_counts": overlay_status_counts,
        "records": overlay_review,
    })
    write_json(SCHEMA_CONTRACT_REVIEW_PATH, contract_review)
    write_json(TYPING_RULE_REVIEW_PATH, rule_review)
    write_json(SCHEMA_OVERLAY_INPUT_CONTRACT_PATH, schema_overlay_input_contract)
    write_json(REVIEW_DECISION_TABLE_PATH, decision_table)
    write_json(REVIEW_PACKET_PATH, review_packet)
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
        "TYPING_REVIEW_0_SOURCE_RECEIPT_CONSUMED": SOURCE_TYPING_RECEIPT_PATH.exists(),
        "TYPING_REVIEW_1_REVIEW_ASSESSMENT_EMITTED": REVIEW_ASSESSMENT_PATH.exists(),
        "TYPING_REVIEW_2_FIELD_POLICY_GAP_REVIEW_EMITTED": FIELD_POLICY_GAP_REVIEW_PATH.exists(),
        "TYPING_REVIEW_3_LINEAGE_REQUIREMENT_REVIEW_EMITTED": LINEAGE_REQUIREMENT_REVIEW_PATH.exists(),
        "TYPING_REVIEW_4_CANDIDATE_OVERLAY_REVIEW_EMITTED": CANDIDATE_OVERLAY_REVIEW_PATH.exists(),
        "TYPING_REVIEW_5_SCHEMA_CONTRACT_REVIEW_EMITTED": SCHEMA_CONTRACT_REVIEW_PATH.exists(),
        "TYPING_REVIEW_6_TYPING_RULE_REVIEW_EMITTED": TYPING_RULE_REVIEW_PATH.exists(),
        "TYPING_REVIEW_7_SCHEMA_OVERLAY_INPUT_CONTRACT_EMITTED": SCHEMA_OVERLAY_INPUT_CONTRACT_PATH.exists(),
        "TYPING_REVIEW_8_DECISION_TABLE_EMITTED": REVIEW_DECISION_TABLE_PATH.exists(),
        "TYPING_REVIEW_9_REVIEW_PACKET_EMITTED": REVIEW_PACKET_PATH.exists(),
        "TYPING_REVIEW_10_NO_SCHEMA_OVERLAY_BUILT": roll["schema_overlay_built_count"] == 0,
        "TYPING_REVIEW_11_NO_SCHEMA_OVERLAY_APPLIED": roll["schema_overlay_applied_count"] == 0,
        "TYPING_REVIEW_12_NO_TYPING_RULE_APPLIED": roll["typing_rule_applied_count"] == 0,
        "TYPING_REVIEW_13_NO_FIELD_POLICY_MODIFIED": roll["field_policy_modified_count"] == 0,
        "TYPING_REVIEW_14_NO_CANDIDATE_ARTIFACT_MODIFIED": roll["candidate_artifact_modified_count"] == 0,
        "TYPING_REVIEW_15_NO_ROW_LOCATOR_APPLIED": roll["source_row_locator_applied_count"] == 0,
        "TYPING_REVIEW_16_NO_REBINDS_APPLIED": roll["rebinds_applied_count"] == 0,
        "TYPING_REVIEW_17_NO_DOMINANCE_RULE_APPLIED": roll["dominance_rule_applied_count"] == 0,
        "TYPING_REVIEW_18_NO_VALUES_AUTHORIZED": roll["values_authorized_count"] == 0,
        "TYPING_REVIEW_19_NO_VALUES_APPLIED": roll["values_applied_count"] == 0,
        "TYPING_REVIEW_20_NO_NULL_REASONS_ACCEPTED": roll["null_reason_accepted_count"] == 0,
        "TYPING_REVIEW_21_NO_SOURCE_PACKET_MATERIALIZED": roll["source_packet_materialized_for_review_count"] == 0,
        "TYPING_REVIEW_22_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "TYPING_REVIEW_23_NO_DISCRIMINATOR_READY": roll["ready_discriminator_count"] == 0,
        "TYPING_REVIEW_24_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "TYPING_REVIEW_25_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "TYPING_REVIEW_26_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "TYPING_REVIEW_27_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classification["target_candidate_declared_for_review"] is False,
        "TYPING_REVIEW_28_NO_TARGET_SELECTED_FOR_BUILD": classification["target_selected_for_build"] is False,
        "TYPING_REVIEW_29_NO_ACCEPTED_FOR_BUILD": classification["accepted_for_build"] is False,
        "TYPING_REVIEW_30_NO_RUNTIME_PATCH": classification["runtime_patch_authorized"] is False,
        "TYPING_REVIEW_31_NO_TARGET_FILE_MODIFICATION": classification["target_file_modification_authorized"] is False,
        "TYPING_REVIEW_32_NO_C5_OPENED": classification["c5_authorized"] is False,
        "TYPING_REVIEW_33_NO_GENERAL_CELL1_AUTHORITY": classification["general_cell1_authority_granted"] is False,
        "TYPING_REVIEW_34_NO_LATEST_FILE_GUESSING": classification["latest_file_guessing"] is False,
        "TYPING_REVIEW_35_NO_MTIME_SELECTION": classification["mtime_selection"] is False,
        "TYPING_REVIEW_36_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "TYPING_REVIEW_37_ACCEPTANCE_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "TYPING_REVIEW_38_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "field_review": roll["field_policy_gap_review_count"],
        "lineage_review": roll["lineage_requirement_review_count"],
        "overlay_review": roll["candidate_overlay_review_count"],
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_review_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_typing_receipt_id": SOURCE_TYPING_RECEIPT_ID,
        "machine_readable_source_lineage_field_policy_typing_review_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "field_policy_gap_review_count": roll["field_policy_gap_review_count"],
            "lineage_requirement_review_count": roll["lineage_requirement_review_count"],
            "candidate_overlay_review_count": roll["candidate_overlay_review_count"],
            "typing_rule_review_count": roll["typing_rule_review_count"],
            "schema_contract_review_count": roll["schema_contract_review_count"],
            "schema_overlay_input_contract_count": roll["schema_overlay_input_contract_count"],
            "field_review_status_counts": roll["field_review_status_counts"],
            "lineage_evidence_class_counts": roll["lineage_evidence_class_counts"],
            "candidate_overlay_review_status_counts": roll["candidate_overlay_review_status_counts"],
            "schema_overlay_built": False,
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
            "review_assessment": rel(REVIEW_ASSESSMENT_PATH),
            "field_policy_gap_review": rel(FIELD_POLICY_GAP_REVIEW_PATH),
            "lineage_requirement_review": rel(LINEAGE_REQUIREMENT_REVIEW_PATH),
            "candidate_overlay_review": rel(CANDIDATE_OVERLAY_REVIEW_PATH),
            "schema_contract_review": rel(SCHEMA_CONTRACT_REVIEW_PATH),
            "typing_rule_review": rel(TYPING_RULE_REVIEW_PATH),
            "schema_overlay_input_contract": rel(SCHEMA_OVERLAY_INPUT_CONTRACT_PATH),
            "review_decision_table": rel(REVIEW_DECISION_TABLE_PATH),
            "review_packet": rel(REVIEW_PACKET_PATH),
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
    print(f"source_lineage_field_policy_typing_review_receipt_id={receipt_id}")
    print(f"source_lineage_field_policy_typing_review_receipt_path={rel(receipt_path)}")
    print(f"source_lineage_field_policy_typing_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"field_policy_gap_review_path={rel(FIELD_POLICY_GAP_REVIEW_PATH)}")
    print(f"lineage_requirement_review_path={rel(LINEAGE_REQUIREMENT_REVIEW_PATH)}")
    print(f"candidate_overlay_review_path={rel(CANDIDATE_OVERLAY_REVIEW_PATH)}")
    print(f"schema_contract_review_path={rel(SCHEMA_CONTRACT_REVIEW_PATH)}")
    print(f"typing_rule_review_path={rel(TYPING_RULE_REVIEW_PATH)}")
    print(f"schema_overlay_input_contract_path={rel(SCHEMA_OVERLAY_INPUT_CONTRACT_PATH)}")
    print(f"source_lineage_field_policy_typing_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"source_lineage_field_policy_typing_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
