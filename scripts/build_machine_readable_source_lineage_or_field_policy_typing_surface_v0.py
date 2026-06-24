#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_MACHINE_READABLE_SOURCE_LINEAGE_OR_FIELD_POLICY_TYPING_SURFACE_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_LINEAGE_FIELD_POLICY_TYPING"
MODE = "SOURCE_LINEAGE_FIELD_POLICY_TYPING / NO_TYPING_RULE_APPLIED / NO_REBIND_APPLIED / NO_VALUE_AUTHORIZATION / NO_METADATA_FILL"
BUILD_MODE = "SOURCE_LINEAGE_FIELD_POLICY_TYPING_SURFACE_ONLY"

SOURCE_ROW_LOCATOR_RECEIPT_ID = "e6281cfb"
SOURCE_ROW_LOCATOR_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_row_locator_v0_receipts/e6281cfb.json"
SOURCE_ROW_LOCATOR_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_row_locator_v0/typed_machine_readable_source_row_locator_surface_v0.json"
SOURCE_CANDIDATE_ARTIFACT_SCAN_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_row_locator_v0/typed_machine_readable_source_row_locator_candidate_artifact_scan_v0.json"
SOURCE_ROW_IDENTITY_MATCH_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_row_locator_v0/typed_machine_readable_source_row_identity_match_table_v0.json"
SOURCE_SOURCE_OBJECT_STRUCTURE_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_row_locator_v0/typed_machine_readable_source_object_structure_table_v0.json"
SOURCE_SOURCE_LINEAGE_MARKER_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_row_locator_v0/typed_machine_readable_source_lineage_marker_table_v0.json"
SOURCE_PER_BINDING_LOCATOR_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_row_locator_v0/typed_machine_readable_per_binding_source_row_locator_v0.json"
SOURCE_UNIQUE_LOCATOR_PROPOSALS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_row_locator_v0/typed_machine_readable_unique_source_row_locator_proposals_v0.json"
SOURCE_LOCATOR_RESIDUAL_AMBIGUITY_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_row_locator_v0/typed_machine_readable_source_row_locator_residual_ambiguity_v0.json"
SOURCE_LOCATOR_DECISION_OPTIONS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_row_locator_v0/typed_machine_readable_source_row_locator_decision_options_v0.json"
SOURCE_LOCATOR_NEXT_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_row_locator_v0/typed_machine_readable_source_row_locator_to_rebind_review_contract_v0.json"
SOURCE_LOCATOR_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_row_locator_v0/typed_machine_readable_source_row_locator_classification_v0.json"
SOURCE_LOCATOR_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_row_locator_v0/typed_machine_readable_source_row_locator_rollup_v0.json"
SOURCE_LOCATOR_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_row_locator_v0/typed_machine_readable_source_row_locator_profile_v0.json"

SOURCE_DECISION_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_decision_surface_v0/typed_machine_readable_source_ref_decision_surface_v0.json"
SOURCE_EVIDENCE_REQUIREMENTS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_decision_surface_v0/typed_machine_readable_source_ref_decision_evidence_requirements_v0.json"
SOURCE_BRANCH_DECISION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_decision_surface_v0/typed_machine_readable_source_ref_next_branch_decision_table_v0.json"
SOURCE_DOMINANCE_FEATURE_MATRIX_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing_v0/typed_machine_readable_source_ref_rebind_dominance_feature_matrix_v0.json"
SOURCE_RESIDUAL_REBIND_TIE_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing_v0/typed_machine_readable_source_ref_rebind_residual_tie_table_v0.json"
SOURCE_BROKEN_BINDING_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_row_path_refinement_v0/typed_machine_readable_broken_row_binding_table_v0.json"
SOURCE_MACHINE_SOURCE_SLOTS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_machine_source_slots_v0.json"
SOURCE_FIELD_POLICY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_source_field_policy_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_typing_v0_receipts"

TYPING_SURFACE_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_surface_v0.json"
PER_BINDING_TYPING_GAP_TABLE_PATH = OUT_DIR / "typed_machine_readable_per_binding_source_lineage_field_policy_typing_gap_v0.json"
FIELD_POLICY_GAP_TABLE_PATH = OUT_DIR / "typed_machine_readable_field_policy_typing_gap_table_v0.json"
SOURCE_LINEAGE_REQUIREMENT_TABLE_PATH = OUT_DIR / "typed_machine_readable_source_lineage_requirement_table_v0.json"
CANDIDATE_ARTIFACT_TYPING_OVERLAY_PATH = OUT_DIR / "typed_machine_readable_candidate_artifact_required_typing_overlay_v0.json"
TYPING_RULE_PROPOSAL_SURFACE_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_rule_proposal_surface_v0.json"
SOURCE_ROLE_SCHEMA_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_source_role_schema_contract_v0.json"
FIELD_POLICY_ENRICHMENT_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_field_policy_enrichment_contract_v0.json"
TYPING_REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_review_packet_v0.json"
TYPING_DECISION_OPTIONS_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_decision_options_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_typing_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_ROW_LOCATOR_RECEIPT_PATH,
    SOURCE_ROW_LOCATOR_SURFACE_PATH,
    SOURCE_CANDIDATE_ARTIFACT_SCAN_PATH,
    SOURCE_ROW_IDENTITY_MATCH_TABLE_PATH,
    SOURCE_SOURCE_OBJECT_STRUCTURE_TABLE_PATH,
    SOURCE_SOURCE_LINEAGE_MARKER_TABLE_PATH,
    SOURCE_PER_BINDING_LOCATOR_TABLE_PATH,
    SOURCE_UNIQUE_LOCATOR_PROPOSALS_PATH,
    SOURCE_LOCATOR_RESIDUAL_AMBIGUITY_TABLE_PATH,
    SOURCE_LOCATOR_DECISION_OPTIONS_PATH,
    SOURCE_LOCATOR_NEXT_CONTRACT_PATH,
    SOURCE_LOCATOR_CLASSIFICATION_PATH,
    SOURCE_LOCATOR_ROLLUP_PATH,
    SOURCE_LOCATOR_PROFILE_PATH,
    SOURCE_DECISION_SURFACE_PATH,
    SOURCE_EVIDENCE_REQUIREMENTS_PATH,
    SOURCE_BRANCH_DECISION_TABLE_PATH,
    SOURCE_DOMINANCE_FEATURE_MATRIX_PATH,
    SOURCE_RESIDUAL_REBIND_TIE_TABLE_PATH,
    SOURCE_BROKEN_BINDING_TABLE_PATH,
    SOURCE_MACHINE_SOURCE_SLOTS_PATH,
    SOURCE_FIELD_POLICY_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_SOURCE_ROW_LOCATOR_BUILT_NO_UNIQUE_PROPOSALS"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_SOURCE_ROW_LOCATOR_BUILT_NO_UNIQUE_PROPOSALS"
EXPECTED_NEXT = "BUILD_MACHINE_READABLE_SOURCE_LINEAGE_OR_FIELD_POLICY_TYPING_SURFACE_V0"

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

def validate_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    receipt = read_json(SOURCE_ROW_LOCATOR_RECEIPT_PATH)
    summary = receipt.get("machine_readable_source_row_locator_summary", {})
    scan = read_json(SOURCE_CANDIDATE_ARTIFACT_SCAN_PATH)
    row_identity = read_json(SOURCE_ROW_IDENTITY_MATCH_TABLE_PATH)
    source_object = read_json(SOURCE_SOURCE_OBJECT_STRUCTURE_TABLE_PATH)
    lineage = read_json(SOURCE_SOURCE_LINEAGE_MARKER_TABLE_PATH)
    per_binding = read_json(SOURCE_PER_BINDING_LOCATOR_TABLE_PATH)
    unique = read_json(SOURCE_UNIQUE_LOCATOR_PROPOSALS_PATH)
    residual = read_json(SOURCE_LOCATOR_RESIDUAL_AMBIGUITY_TABLE_PATH)
    classif = read_json(SOURCE_LOCATOR_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_LOCATOR_ROLLUP_PATH)
    profile = read_json(SOURCE_LOCATOR_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_ROW_LOCATOR_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_row_locator_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_row_locator_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_row_locator_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"source_row_locator_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("candidate_artifact_scan_count") != 168:
        failures.append("candidate_artifact_scan_count_not_168")
    if summary.get("binding_count") != 21:
        failures.append("binding_count_not_21")
    if summary.get("unique_locator_proposal_count") != 0:
        failures.append("unique_locator_proposal_count_nonzero")
    if summary.get("residual_locator_ambiguity_count") != 21:
        failures.append("residual_locator_ambiguity_count_not_21")
    if summary.get("candidate_positive_locator_score_count") != 0:
        failures.append("positive_locator_score_count_nonzero")
    if summary.get("candidate_full_row_identity_match_count") != 0:
        failures.append("full_row_identity_match_count_nonzero")
    if summary.get("candidate_partial_row_identity_match_count") != 0:
        failures.append("partial_row_identity_match_count_nonzero")
    if summary.get("candidate_source_object_structure_match_count") != 0:
        failures.append("source_object_structure_match_count_nonzero")
    if summary.get("candidate_lineage_marker_count") != 0:
        failures.append("lineage_marker_count_nonzero")
    if summary.get("source_row_locator_applied") is not False:
        failures.append("source_row_locator_applied_unexpectedly")
    if summary.get("rebinds_applied") is not False:
        failures.append("rebinds_applied_unexpectedly")
    if summary.get("values_authorized") is not False:
        failures.append("values_authorized_unexpectedly")
    if summary.get("metadata_populated") is not False:
        failures.append("metadata_populated_unexpectedly")
    if summary.get("ready_discriminator_count") != 0:
        failures.append("ready_discriminator_nonzero")

    if scan.get("candidate_scan_count") != 168:
        failures.append("candidate_scan_table_count_not_168")
    if row_identity.get("record_count") != 0:
        failures.append("row_identity_record_count_nonzero")
    if source_object.get("record_count") != 0:
        failures.append("source_object_record_count_nonzero")
    if lineage.get("record_count") != 0:
        failures.append("lineage_record_count_nonzero")
    if per_binding.get("binding_count") != 21:
        failures.append("per_binding_locator_count_not_21")
    if unique.get("proposal_count") != 0:
        failures.append("unique_locator_proposal_table_nonzero")
    if residual.get("ambiguity_count") != 21:
        failures.append("residual_locator_ambiguity_table_not_21")
    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("locator_classification_status_wrong")
    if roll.get("metadata_populated_count") != 0:
        failures.append("locator_rollup_metadata_populated_nonzero")
    if profile.get("metadata_populated") is not False:
        failures.append("locator_profile_metadata_populated_true")

    return failures

def records_from(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    for key in ["records", "slots", "field_policies", "policies"]:
        val = obj.get(key)
        if isinstance(val, list):
            return [x for x in val if isinstance(x, dict)]
    return []

def load_records() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    scans = [r for r in read_json(SOURCE_CANDIDATE_ARTIFACT_SCAN_PATH).get("records", []) if isinstance(r, dict)]
    residual = [r for r in read_json(SOURCE_LOCATOR_RESIDUAL_AMBIGUITY_TABLE_PATH).get("records", []) if isinstance(r, dict)]
    slots = {
        str(r.get("slot_id")): r
        for r in read_json(SOURCE_MACHINE_SOURCE_SLOTS_PATH).get("slots", [])
        if isinstance(r, dict) and r.get("slot_id")
    }
    broken = {
        str(r.get("slot_id")): r
        for r in read_json(SOURCE_BROKEN_BINDING_TABLE_PATH).get("records", [])
        if isinstance(r, dict) and r.get("slot_id")
    }
    policy_obj = read_json(SOURCE_FIELD_POLICY_PATH)
    policies: Dict[str, Dict[str, Any]] = {}
    for r in records_from(policy_obj):
        if r.get("field"):
            policies[str(r["field"])] = r
    return scans, residual, slots, broken, policies

def norm(v: Any) -> str:
    return "" if v is None else str(v)

def unique_fields(slots: Dict[str, Dict[str, Any]], residual: List[Dict[str, Any]]) -> List[str]:
    out = []
    for r in residual:
        f = norm(r.get("field") or slots.get(norm(r.get("slot_id")), {}).get("field"))
        if f and f not in out:
            out.append(f)
    return out

def build_field_policy_gaps(fields: List[str], policies: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for field in fields:
        p = policies.get(field, {})
        required_source_object = p.get("required_source_object") or p.get("source_object")
        source_class = p.get("source_class") or p.get("source_kind")
        explicit_source_role = p.get("source_role") or p.get("declared_source_role")
        lineage_ref = p.get("source_lineage_ref") or p.get("lineage_ref") or p.get("source_packet_lineage_ref")
        producer_unit = p.get("producer_unit") or p.get("source_unit") or p.get("created_by_unit")
        missing = []
        if not required_source_object:
            missing.append("FIELD_POLICY_REQUIRED_SOURCE_OBJECT_MISSING")
        if not source_class:
            missing.append("FIELD_POLICY_SOURCE_CLASS_MISSING")
        if not explicit_source_role:
            missing.append("FIELD_POLICY_EXPLICIT_SOURCE_ROLE_MISSING")
        if not lineage_ref:
            missing.append("FIELD_POLICY_LINEAGE_REF_MISSING")
        if not producer_unit:
            missing.append("FIELD_POLICY_PRODUCER_UNIT_MISSING")
        rows.append({
            "field": field,
            "policy_present": bool(p),
            "required_source_object": required_source_object,
            "source_class": source_class,
            "explicit_source_role": explicit_source_role,
            "lineage_ref": lineage_ref,
            "producer_unit": producer_unit,
            "missing_policy_typing": missing,
            "gap_status": "FIELD_POLICY_TYPING_INCOMPLETE" if missing else "FIELD_POLICY_HAS_DECLARATIONS_BUT_CANDIDATES_LACK_MARKERS",
            "safe_next_action": "enrich field policy or candidate artifact typing before source-ref rebinding",
        })
    return rows

def build_candidate_overlay(scans: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for s in scans:
        rows.append({
            "candidate_id": s.get("candidate_id"),
            "slot_id": s.get("slot_id"),
            "row_uid": s.get("row_uid"),
            "field": s.get("field"),
            "candidate_source_ref": s.get("candidate_source_ref"),
            "observed_locator_status": s.get("locator_status"),
            "row_identity_match_count": s.get("row_identity_match_count", 0),
            "source_object_structure_match_count": s.get("source_object_structure_match_count", 0),
            "lineage_marker_count": s.get("lineage_marker_count", 0),
            "required_candidate_typing": [
                "candidate_source_role",
                "candidate_source_object_kind",
                "candidate_producer_unit",
                "candidate_lineage_ref",
                "candidate_row_identity_schema",
                "candidate_allowed_fields",
            ],
            "typing_gap_reasons": [
                "ROW_IDENTITY_MARKERS_ABSENT",
                "SOURCE_OBJECT_STRUCTURE_MARKERS_ABSENT",
                "SOURCE_LINEAGE_MARKERS_ABSENT",
            ],
            "overlay_status": "CANDIDATE_ARTIFACT_REQUIRES_SOURCE_LINEAGE_FIELD_POLICY_TYPING",
            "authorized_to_modify_candidate": False,
        })
    return rows

def build_per_binding_gaps(residual: List[Dict[str, Any]], slots: Dict[str, Dict[str, Any]], broken: Dict[str, Dict[str, Any]], policies: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for r in residual:
        slot_id = norm(r.get("slot_id"))
        slot = slots.get(slot_id, {})
        b = broken.get(slot_id, {})
        field = norm(r.get("field") or slot.get("field") or b.get("field"))
        policy = policies.get(field, {})
        missing = [
            "ROW_IDENTITY_TYPING",
            "SOURCE_OBJECT_STRUCTURE_TYPING",
            "SOURCE_LINEAGE_TYPING",
        ]
        if not (policy.get("source_role") or policy.get("declared_source_role")):
            missing.append("FIELD_POLICY_EXPLICIT_SOURCE_ROLE")
        if not (policy.get("required_source_object") or policy.get("source_object")):
            missing.append("FIELD_POLICY_REQUIRED_SOURCE_OBJECT")
        if not (policy.get("producer_unit") or policy.get("source_unit") or policy.get("created_by_unit")):
            missing.append("FIELD_POLICY_PRODUCER_UNIT")
        if not (policy.get("source_lineage_ref") or policy.get("lineage_ref") or policy.get("source_packet_lineage_ref")):
            missing.append("FIELD_POLICY_LINEAGE_REF")

        rows.append({
            "slot_id": slot_id,
            "row_uid": r.get("row_uid") or slot.get("row_uid") or b.get("row_uid"),
            "field": field,
            "current_row_source_ref": b.get("current_row_source_ref") or b.get("row_source_ref"),
            "current_row_json_path": b.get("current_row_json_path") or b.get("row_json_path"),
            "tied_locator_candidate_count": r.get("tied_locator_candidate_count"),
            "required_source_object": slot.get("required_source_object") or policy.get("required_source_object") or policy.get("source_object"),
            "source_class": slot.get("source_class") or policy.get("source_class"),
            "missing_typing_classes": missing,
            "decision_question": "What typed lineage or field-policy evidence would allow one candidate source ref to serve as source for this slot?",
            "safe_null_behavior": "keep source ref unbound and do not extract values",
            "gap_status": "SOURCE_LINEAGE_OR_FIELD_POLICY_TYPING_REQUIRED",
        })
    return rows

def build_lineage_requirements(per_binding_gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    required_evidence = [
        ("EXPLICIT_SOURCE_ROLE", "candidate artifact must declare whether it is source material, diagnostic residue, receipt, policy, or projection"),
        ("ARTIFACT_PRODUCER_UNIT", "candidate artifact must expose the unit that produced it"),
        ("SOURCE_PACKET_LINEAGE", "candidate artifact must link to the source-packet or field-policy lineage it belongs to"),
        ("ROW_IDENTITY_SCHEMA", "candidate artifact must expose row_uid / slot_id / field or an equivalent declared row identity map"),
        ("FIELD_POLICY_SOURCE_OBJECT_MATCH", "field policy must declare which source object kind may serve this field"),
    ]
    for gap in per_binding_gaps:
        for ev, meaning in required_evidence:
            rows.append({
                "slot_id": gap.get("slot_id"),
                "row_uid": gap.get("row_uid"),
                "field": gap.get("field"),
                "evidence_class": ev,
                "meaning": meaning,
                "current_status": "missing_or_not_machine_distinguishable",
                "allowed_resolver": "machine_readable_schema_overlay_or_human_prevalidated_schema",
                "must_not_impersonate": [
                    "source-ref selection",
                    "value extraction",
                    "metadata population",
                    "tie break",
                ],
            })
    return rows

def decide(per_binding_gaps: List[Dict[str, Any]], field_policy_gaps: List[Dict[str, Any]], candidate_overlay: List[Dict[str, Any]]) -> Tuple[str, List[str], str]:
    reason_codes = [
        "SOURCE_LINEAGE_FIELD_POLICY_TYPING_SURFACE_BUILT",
        "FIELD_POLICY_TYPING_GAPS_EMITTED",
        "SOURCE_LINEAGE_REQUIREMENTS_EMITTED",
        "CANDIDATE_ARTIFACT_TYPING_OVERLAY_EMITTED",
        "NO_TYPING_RULE_APPLIED",
        "NO_REBINDS_APPLIED",
        "NO_VALUES_AUTHORIZED_OR_APPLIED",
        "NO_METADATA_POPULATION",
    ]

    field_gap_count = sum(1 for r in field_policy_gaps if r.get("missing_policy_typing"))
    candidate_gap_count = len(candidate_overlay)

    if field_gap_count or candidate_gap_count:
        reason_codes.append("LINEAGE_OR_FIELD_POLICY_TYPING_REQUIRED_BEFORE_REBIND_REVIEW")
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_SURFACE_BUILT_REQUIRES_SCHEMA_OR_RULE_REVIEW"
        next_edge = "REVIEW_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_REQUIREMENTS_V0"
    else:
        reason_codes.append("FIELD_POLICY_PRESENT_BUT_NOT_LINKED_TO_CANDIDATE_ARTIFACTS")
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_SURFACE_BUILT_REQUIRES_LINKAGE_RULE"
        next_edge = "BUILD_MACHINE_READABLE_SOURCE_LINEAGE_LINKAGE_RULE_CANDIDATES_V0"

    return status, reason_codes, next_edge

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_authority_boundary_v0",
        "status": status,
        "may_describe_typing_gaps": True,
        "may_emit_typing_requirements": True,
        "may_emit_schema_contracts": True,
        "may_emit_typing_rule_proposals": True,
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

def rollup_obj(status: str, per_binding_gaps: List[Dict[str, Any]], field_policy_gaps: List[Dict[str, Any]], lineage_requirements: List[Dict[str, Any]], candidate_overlay: List[Dict[str, Any]], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "binding_count": len(per_binding_gaps),
        "field_policy_gap_count": len(field_policy_gaps),
        "field_policy_incomplete_count": sum(1 for r in field_policy_gaps if r.get("missing_policy_typing")),
        "source_lineage_requirement_count": len(lineage_requirements),
        "candidate_artifact_typing_overlay_count": len(candidate_overlay),
        "candidate_artifact_requires_typing_count": sum(1 for r in candidate_overlay if r.get("required_candidate_typing")),
        "typing_rule_proposal_count": 1,
        "schema_contract_count": 2,
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
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_profile_v0",
        "profile_id": "source_lineage_field_policy_typing_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "typing_surface_built": True,
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
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The row-locator surface found no row identity, source-object, or lineage markers; this unit exposes the missing lineage and field-policy typing required before source-ref rebinding can be reviewed.",
        "binding_count": roll["binding_count"],
        "field_policy_gap_count": roll["field_policy_gap_count"],
        "field_policy_incomplete_count": roll["field_policy_incomplete_count"],
        "source_lineage_requirement_count": roll["source_lineage_requirement_count"],
        "candidate_artifact_typing_overlay_count": roll["candidate_artifact_typing_overlay_count"],
        "candidate_artifact_requires_typing_count": roll["candidate_artifact_requires_typing_count"],
        "typing_rule_proposal_count": roll["typing_rule_proposal_count"],
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "typing_rule_applied_count": 0,
        "field_policy_modified_count": 0,
        "candidate_artifact_modified_count": 0,
        "source_row_locator_applied_count": 0,
        "rebinds_applied_count": 0,
        "dominance_rule_applied_count": 0,
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
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_transition_trace_v0",
        "trace": [
            {
                "step": "consume_row_locator_zero_signal",
                "question": "why did candidate artifact inspection fail to distinguish source refs",
                "answer": "candidate artifacts lack row identity, source-object structure, and lineage markers",
                "taken": "expose source lineage and field-policy typing gaps",
            },
            {
                "step": "emit_typing_requirements",
                "question": "what typing would make source-ref choice lawful later",
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
        scans, residual, slots, broken, policies = [], [], {}, {}, {}
        fields, field_gaps, per_binding_gaps, lineage_requirements, candidate_overlay = [], [], [], [], []
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_BASIS_V0"
    else:
        scans, residual, slots, broken, policies = load_records()
        fields = unique_fields(slots, residual)
        field_gaps = build_field_policy_gaps(fields, policies)
        candidate_overlay = build_candidate_overlay(scans)
        per_binding_gaps = build_per_binding_gaps(residual, slots, broken, policies)
        lineage_requirements = build_lineage_requirements(per_binding_gaps)
        status, reason_codes, next_edge = decide(per_binding_gaps, field_gaps, candidate_overlay)

    roll = rollup_obj(status, per_binding_gaps, field_gaps, lineage_requirements, candidate_overlay, next_edge)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, roll, next_edge)
    boundary = authority_boundary_obj(status)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    typing_surface = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_surface_v0",
        "surface_status": status,
        "source_row_locator_receipt_id": SOURCE_ROW_LOCATOR_RECEIPT_ID,
        "binding_count": roll["binding_count"],
        "field_policy_gap_count": roll["field_policy_gap_count"],
        "source_lineage_requirement_count": roll["source_lineage_requirement_count"],
        "candidate_artifact_typing_overlay_count": roll["candidate_artifact_typing_overlay_count"],
        "surface_claim": "This surface states which lineage and field-policy typing must exist before candidate source refs can be lawfully distinguished.",
        "per_binding_typing_gap_ref": rel(PER_BINDING_TYPING_GAP_TABLE_PATH),
        "field_policy_gap_table_ref": rel(FIELD_POLICY_GAP_TABLE_PATH),
        "source_lineage_requirement_table_ref": rel(SOURCE_LINEAGE_REQUIREMENT_TABLE_PATH),
        "candidate_artifact_typing_overlay_ref": rel(CANDIDATE_ARTIFACT_TYPING_OVERLAY_PATH),
        "recommended_next": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    typing_rule_surface = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_rule_proposal_surface_v0",
        "surface_status": "TYPING_RULE_PROPOSAL_SURFACE_EMITTED_NOT_APPLIED",
        "proposal_count": 1,
        "proposal": {
            "proposal_id": "source_lineage_field_policy_typing_rule_" + sha8({"fields": fields, "requirements": lineage_requirements}),
            "proposal_status": "PROPOSED_FOR_REVIEW_NOT_APPLIED",
            "rule_shape": {
                "candidate_source_ref_may_be_reviewable_only_if": [
                    "candidate declares source_role",
                    "candidate declares source_object_kind",
                    "candidate declares producer_unit or source_unit",
                    "candidate declares lineage_ref or source_packet_ref",
                    "candidate exposes row_identity_schema for slot_id/row_uid/field or equivalent explicit mapping",
                    "field policy declares allowed source_object_kind and source_class for field",
                ]
            },
            "must_not": [
                "choose candidate source ref",
                "apply rebind",
                "extract values",
                "populate metadata",
                "mark discriminator ready",
            ],
        },
        "authorization_required_before_use": True,
    }

    source_role_schema_contract = {
        "schema_version": "typed_machine_readable_source_role_schema_contract_v0",
        "contract_status": "SOURCE_ROLE_SCHEMA_CONTRACT_EMITTED_NOT_APPLIED",
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
        "application_authorized": False,
    }

    field_policy_enrichment_contract = {
        "schema_version": "typed_machine_readable_field_policy_enrichment_contract_v0",
        "contract_status": "FIELD_POLICY_ENRICHMENT_CONTRACT_EMITTED_NOT_APPLIED",
        "required_field_policy_fields": [
            "field",
            "source_class",
            "required_source_object",
            "declared_source_role",
            "producer_unit_or_allowed_producer_units",
            "lineage_ref_or_source_packet_lineage_ref",
            "row_identity_keys",
        ],
        "fields_under_review": fields,
        "field_policy_modified": False,
        "application_authorized": False,
    }

    review_packet = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_review_packet_v0",
        "review_packet_status": "SOURCE_LINEAGE_FIELD_POLICY_TYPING_REVIEW_REQUIRED",
        "question": "Review the minimal lineage / field-policy typing requirements before any source-ref rebinding can be lawful.",
        "allowed_responses": [
            "ACCEPT_TYPING_REQUIREMENTS_AS_SCHEMA_CONTRACT",
            "BUILD_SCHEMA_OVERLAY_FOR_SOURCE_LINEAGE_FIELD_POLICY_TYPING",
            "REJECT_AND_FREEZE_AS_DIAGNOSTIC_REFERENCE",
        ],
        "default_recommended_response": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    decision_options = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_decision_options_v0",
        "decision_options_status": "SOURCE_LINEAGE_FIELD_POLICY_TYPING_DECISION_OPTIONS_EMITTED",
        "safe_options": [
            {
                "option": "REVIEW_TYPING_REQUIREMENTS",
                "recommended": True,
                "next_unit": "REVIEW_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_REQUIREMENTS_V0",
                "meaning": "Review the emitted typing gaps and contracts without applying schema or source refs.",
            },
            {
                "option": "BUILD_SCHEMA_OVERLAY",
                "recommended": False,
                "next_unit": "BUILD_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_V0",
                "meaning": "Only after review confirms the contract shape.",
            },
            {
                "option": "FREEZE_DIAGNOSTIC_REFERENCE",
                "recommended": False,
                "next_unit": "FREEZE_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_SURFACE_V0",
                "meaning": "Use if this surface should be preserved without continuing.",
            },
        ],
        "forbidden_shortcuts": [
            "apply typing rule immediately",
            "modify field policy immediately",
            "modify candidate artifacts",
            "select source ref",
            "extract values",
            "populate metadata",
        ],
    }

    classification = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "binding_count": roll["binding_count"],
        "field_policy_gap_count": roll["field_policy_gap_count"],
        "field_policy_incomplete_count": roll["field_policy_incomplete_count"],
        "source_lineage_requirement_count": roll["source_lineage_requirement_count"],
        "candidate_artifact_typing_overlay_count": roll["candidate_artifact_typing_overlay_count"],
        "candidate_artifact_requires_typing_count": roll["candidate_artifact_requires_typing_count"],
        "typing_rule_proposal_count": roll["typing_rule_proposal_count"],
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

    write_json(TYPING_SURFACE_PATH, typing_surface)
    write_json(PER_BINDING_TYPING_GAP_TABLE_PATH, {
        "schema_version": "typed_machine_readable_per_binding_source_lineage_field_policy_typing_gap_v0",
        "table_status": "PER_BINDING_SOURCE_LINEAGE_FIELD_POLICY_TYPING_GAPS_EMITTED",
        "record_count": len(per_binding_gaps),
        "records": per_binding_gaps,
    })
    write_json(FIELD_POLICY_GAP_TABLE_PATH, {
        "schema_version": "typed_machine_readable_field_policy_typing_gap_table_v0",
        "table_status": "FIELD_POLICY_TYPING_GAPS_EMITTED",
        "record_count": len(field_gaps),
        "records": field_gaps,
    })
    write_json(SOURCE_LINEAGE_REQUIREMENT_TABLE_PATH, {
        "schema_version": "typed_machine_readable_source_lineage_requirement_table_v0",
        "table_status": "SOURCE_LINEAGE_REQUIREMENTS_EMITTED",
        "record_count": len(lineage_requirements),
        "records": lineage_requirements,
    })
    write_json(CANDIDATE_ARTIFACT_TYPING_OVERLAY_PATH, {
        "schema_version": "typed_machine_readable_candidate_artifact_required_typing_overlay_v0",
        "overlay_status": "CANDIDATE_ARTIFACT_TYPING_OVERLAY_EMITTED_NOT_APPLIED",
        "record_count": len(candidate_overlay),
        "records": candidate_overlay,
    })
    write_json(TYPING_RULE_PROPOSAL_SURFACE_PATH, typing_rule_surface)
    write_json(SOURCE_ROLE_SCHEMA_CONTRACT_PATH, source_role_schema_contract)
    write_json(FIELD_POLICY_ENRICHMENT_CONTRACT_PATH, field_policy_enrichment_contract)
    write_json(TYPING_REVIEW_PACKET_PATH, review_packet)
    write_json(TYPING_DECISION_OPTIONS_PATH, decision_options)
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
        "LINEAGE_TYPING_0_ROW_LOCATOR_RECEIPT_CONSUMED": SOURCE_ROW_LOCATOR_RECEIPT_PATH.exists(),
        "LINEAGE_TYPING_1_ZERO_SIGNAL_LOCATOR_SURFACE_CONSUMED": SOURCE_ROW_LOCATOR_SURFACE_PATH.exists(),
        "LINEAGE_TYPING_2_TYPING_SURFACE_EMITTED": TYPING_SURFACE_PATH.exists(),
        "LINEAGE_TYPING_3_PER_BINDING_GAPS_EMITTED": PER_BINDING_TYPING_GAP_TABLE_PATH.exists(),
        "LINEAGE_TYPING_4_FIELD_POLICY_GAPS_EMITTED": FIELD_POLICY_GAP_TABLE_PATH.exists(),
        "LINEAGE_TYPING_5_SOURCE_LINEAGE_REQUIREMENTS_EMITTED": SOURCE_LINEAGE_REQUIREMENT_TABLE_PATH.exists(),
        "LINEAGE_TYPING_6_CANDIDATE_OVERLAY_EMITTED": CANDIDATE_ARTIFACT_TYPING_OVERLAY_PATH.exists(),
        "LINEAGE_TYPING_7_TYPING_RULE_PROPOSAL_SURFACE_EMITTED": TYPING_RULE_PROPOSAL_SURFACE_PATH.exists(),
        "LINEAGE_TYPING_8_SOURCE_ROLE_SCHEMA_CONTRACT_EMITTED": SOURCE_ROLE_SCHEMA_CONTRACT_PATH.exists(),
        "LINEAGE_TYPING_9_FIELD_POLICY_ENRICHMENT_CONTRACT_EMITTED": FIELD_POLICY_ENRICHMENT_CONTRACT_PATH.exists(),
        "LINEAGE_TYPING_10_REVIEW_PACKET_EMITTED": TYPING_REVIEW_PACKET_PATH.exists(),
        "LINEAGE_TYPING_11_DECISION_OPTIONS_EMITTED": TYPING_DECISION_OPTIONS_PATH.exists(),
        "LINEAGE_TYPING_12_NO_TYPING_RULE_APPLIED": roll["typing_rule_applied_count"] == 0,
        "LINEAGE_TYPING_13_NO_FIELD_POLICY_MODIFIED": roll["field_policy_modified_count"] == 0,
        "LINEAGE_TYPING_14_NO_CANDIDATE_ARTIFACT_MODIFIED": roll["candidate_artifact_modified_count"] == 0,
        "LINEAGE_TYPING_15_NO_ROW_LOCATOR_APPLIED": roll["source_row_locator_applied_count"] == 0,
        "LINEAGE_TYPING_16_NO_REBINDS_APPLIED": roll["rebinds_applied_count"] == 0,
        "LINEAGE_TYPING_17_NO_DOMINANCE_RULE_APPLIED": roll["dominance_rule_applied_count"] == 0,
        "LINEAGE_TYPING_18_NO_VALUES_AUTHORIZED": roll["values_authorized_count"] == 0,
        "LINEAGE_TYPING_19_NO_VALUES_APPLIED": roll["values_applied_count"] == 0,
        "LINEAGE_TYPING_20_NO_NULL_REASONS_ACCEPTED": roll["null_reason_accepted_count"] == 0,
        "LINEAGE_TYPING_21_NO_SOURCE_PACKET_MATERIALIZED": roll["source_packet_materialized_for_review_count"] == 0,
        "LINEAGE_TYPING_22_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "LINEAGE_TYPING_23_NO_DISCRIMINATOR_READY": roll["ready_discriminator_count"] == 0,
        "LINEAGE_TYPING_24_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "LINEAGE_TYPING_25_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "LINEAGE_TYPING_26_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "LINEAGE_TYPING_27_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classification["target_candidate_declared_for_review"] is False,
        "LINEAGE_TYPING_28_NO_TARGET_SELECTED_FOR_BUILD": classification["target_selected_for_build"] is False,
        "LINEAGE_TYPING_29_NO_ACCEPTED_FOR_BUILD": classification["accepted_for_build"] is False,
        "LINEAGE_TYPING_30_NO_RUNTIME_PATCH": classification["runtime_patch_authorized"] is False,
        "LINEAGE_TYPING_31_NO_TARGET_FILE_MODIFICATION": classification["target_file_modification_authorized"] is False,
        "LINEAGE_TYPING_32_NO_C5_OPENED": classification["c5_authorized"] is False,
        "LINEAGE_TYPING_33_NO_GENERAL_CELL1_AUTHORITY": classification["general_cell1_authority_granted"] is False,
        "LINEAGE_TYPING_34_NO_LATEST_FILE_GUESSING": classification["latest_file_guessing"] is False,
        "LINEAGE_TYPING_35_NO_MTIME_SELECTION": classification["mtime_selection"] is False,
        "LINEAGE_TYPING_36_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "LINEAGE_TYPING_37_ACCEPTANCE_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "LINEAGE_TYPING_38_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "binding_count": roll["binding_count"],
        "requirements": roll["source_lineage_requirement_count"],
        "candidate_overlay": roll["candidate_artifact_typing_overlay_count"],
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_typing_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_TYPING_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_row_locator_receipt_id": SOURCE_ROW_LOCATOR_RECEIPT_ID,
        "machine_readable_source_lineage_field_policy_typing_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "binding_count": roll["binding_count"],
            "field_policy_gap_count": roll["field_policy_gap_count"],
            "field_policy_incomplete_count": roll["field_policy_incomplete_count"],
            "source_lineage_requirement_count": roll["source_lineage_requirement_count"],
            "candidate_artifact_typing_overlay_count": roll["candidate_artifact_typing_overlay_count"],
            "candidate_artifact_requires_typing_count": roll["candidate_artifact_requires_typing_count"],
            "typing_rule_proposal_count": roll["typing_rule_proposal_count"],
            "schema_contract_count": roll["schema_contract_count"],
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
            "typing_surface": rel(TYPING_SURFACE_PATH),
            "per_binding_typing_gap_table": rel(PER_BINDING_TYPING_GAP_TABLE_PATH),
            "field_policy_gap_table": rel(FIELD_POLICY_GAP_TABLE_PATH),
            "source_lineage_requirement_table": rel(SOURCE_LINEAGE_REQUIREMENT_TABLE_PATH),
            "candidate_artifact_typing_overlay": rel(CANDIDATE_ARTIFACT_TYPING_OVERLAY_PATH),
            "typing_rule_proposal_surface": rel(TYPING_RULE_PROPOSAL_SURFACE_PATH),
            "source_role_schema_contract": rel(SOURCE_ROLE_SCHEMA_CONTRACT_PATH),
            "field_policy_enrichment_contract": rel(FIELD_POLICY_ENRICHMENT_CONTRACT_PATH),
            "typing_review_packet": rel(TYPING_REVIEW_PACKET_PATH),
            "typing_decision_options": rel(TYPING_DECISION_OPTIONS_PATH),
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
    print(f"source_lineage_field_policy_typing_receipt_id={receipt_id}")
    print(f"source_lineage_field_policy_typing_receipt_path={rel(receipt_path)}")
    print(f"source_lineage_field_policy_typing_surface_path={rel(TYPING_SURFACE_PATH)}")
    print(f"per_binding_typing_gap_table_path={rel(PER_BINDING_TYPING_GAP_TABLE_PATH)}")
    print(f"field_policy_gap_table_path={rel(FIELD_POLICY_GAP_TABLE_PATH)}")
    print(f"source_lineage_requirement_table_path={rel(SOURCE_LINEAGE_REQUIREMENT_TABLE_PATH)}")
    print(f"candidate_artifact_typing_overlay_path={rel(CANDIDATE_ARTIFACT_TYPING_OVERLAY_PATH)}")
    print(f"typing_rule_proposal_surface_path={rel(TYPING_RULE_PROPOSAL_SURFACE_PATH)}")
    print(f"source_role_schema_contract_path={rel(SOURCE_ROLE_SCHEMA_CONTRACT_PATH)}")
    print(f"field_policy_enrichment_contract_path={rel(FIELD_POLICY_ENRICHMENT_CONTRACT_PATH)}")
    print(f"source_lineage_field_policy_typing_rollup_path={rel(ROLLUP_PATH)}")
    print(f"source_lineage_field_policy_typing_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
