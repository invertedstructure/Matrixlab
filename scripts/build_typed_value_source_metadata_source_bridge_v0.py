#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_TYPED_VALUE_SOURCE_METADATA_SOURCE_BRIDGE_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_bridge.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_BRIDGE"
MODE = "BUILD_SOURCE_BRIDGE / NO_METADATA_FILL / NO_TIE_BREAK / NO_ACCEPTANCE"
BUILD_MODE = "TYPED_METADATA_SOURCE_BRIDGE_ONLY"

SOURCE_METADATA_POPULATION_RECEIPT_ID = "4f2a0901"
SOURCE_METADATA_POPULATION_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_population_v0_receipts/4f2a0901.json"
SOURCE_METADATA_POPULATION_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_population_v0/typed_value_source_metadata_population_packet_v0.json"
SOURCE_METADATA_POPULATED_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_population_v0/typed_value_source_metadata_populated_surface_v0.json"
SOURCE_METADATA_POPULATION_COVERAGE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_population_v0/typed_value_source_metadata_population_coverage_v0.json"
SOURCE_DISCRIMINATOR_READINESS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_population_v0/typed_value_source_discriminator_readiness_v0.json"
SOURCE_METADATA_POPULATION_GAPS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_population_v0/typed_value_source_metadata_population_gaps_v0.json"
SOURCE_METADATA_POPULATION_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_population_v0/typed_value_source_metadata_population_classification_v0.json"
SOURCE_METADATA_POPULATION_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_population_v0/typed_value_source_metadata_population_rollup_v0.json"
SOURCE_METADATA_POPULATION_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_population_v0/typed_value_source_metadata_population_profile_v0.json"

SOURCE_METADATA_SURFACE_RECEIPT_ID = "3b98c589"
SOURCE_METADATA_SURFACE_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_surface_v0_receipts/3b98c589.json"
SOURCE_METADATA_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_surface_v0/typed_value_source_metadata_surface_v0.json"
SOURCE_ROW_METADATA_TEMPLATE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_surface_v0/typed_value_source_row_metadata_template_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0_receipts"

SOURCE_BRIDGE_PATH = OUT_DIR / "typed_value_source_metadata_source_bridge_v0.json"
FIELD_POLICY_PATH = OUT_DIR / "typed_value_source_metadata_source_field_policy_v0.json"
SOURCE_PACKET_TEMPLATE_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_template_v0.json"
ROW_SOURCE_REQUIREMENTS_PATH = OUT_DIR / "typed_value_source_metadata_row_source_requirements_v0.json"
HUMAN_SCHEMA_ONLY_FIELDS_PATH = OUT_DIR / "typed_value_source_metadata_human_schema_only_fields_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_value_source_metadata_source_bridge_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_value_source_metadata_source_bridge_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_value_source_metadata_source_bridge_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_value_source_metadata_source_bridge_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_value_source_metadata_source_bridge_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_value_source_metadata_source_bridge_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_METADATA_POPULATION_RECEIPT_PATH,
    SOURCE_METADATA_POPULATION_PACKET_PATH,
    SOURCE_METADATA_POPULATED_SURFACE_PATH,
    SOURCE_METADATA_POPULATION_COVERAGE_PATH,
    SOURCE_DISCRIMINATOR_READINESS_PATH,
    SOURCE_METADATA_POPULATION_GAPS_PATH,
    SOURCE_METADATA_POPULATION_CLASSIFICATION_PATH,
    SOURCE_METADATA_POPULATION_ROLLUP_PATH,
    SOURCE_METADATA_POPULATION_PROFILE_PATH,
    SOURCE_METADATA_SURFACE_RECEIPT_PATH,
    SOURCE_METADATA_SURFACE_PATH,
    SOURCE_ROW_METADATA_TEMPLATE_PATH,
]

EXPECTED_POPULATION_STATUS = "TYPED_VALUE_SOURCE_METADATA_PARTIALLY_POPULATED_STILL_INSUFFICIENT"
EXPECTED_POPULATION_STOP = "STOP_TYPED_VALUE_SOURCE_METADATA_PARTIALLY_POPULATED_STILL_INSUFFICIENT"
EXPECTED_NEXT = "BUILD_TYPED_VALUE_SOURCE_METADATA_SOURCE_BRIDGE_V0"

SOURCE_BRIDGE_FIELDS = {
    "direct_evidence_strength",
    "target_scope",
    "target_aspect",
    "comparison_grain",
    "inference_strength",
    "verification_gate_ref",
    "rollback_or_stop_boundary_ref",
}

HUMAN_SCHEMA_ONLY_FIELDS = {
    "load_bearing_reason",
    "schema_preference_key",
    "human_preference_boundary_ref",
}

ALREADY_POPULATED_IDENTITY_FIELDS = {
    "direct_evidence_ref",
    "source_role",
    "source_authority",
    "inference_chain_ref",
    "provenance_depth",
}

FIELD_PURPOSE = {
    "direct_evidence_strength": "Rank evidence quality only after explicit evidence-strength source is provided.",
    "load_bearing_reason": "Explain why the row matters; this is not mechanically derivable from identity alone.",
    "target_scope": "Determine whether rows compete for the same target scope.",
    "target_aspect": "Determine whether rows represent different target aspects.",
    "comparison_grain": "Determine whether rows should be compared in one grain or split first.",
    "inference_strength": "Determine whether a row depends on weaker inference.",
    "verification_gate_ref": "Bind target value source to a verification gate.",
    "rollback_or_stop_boundary_ref": "Bind target value source to rollback or stop boundary.",
    "schema_preference_key": "Record a schema-level preference key if a schema is authorized to choose.",
    "human_preference_boundary_ref": "Record explicit human/schema review boundary when machine choice is not lawful.",
}

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

def validate_source_basis() -> List[str]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    receipt = read_json(SOURCE_METADATA_POPULATION_RECEIPT_PATH)
    packet = read_json(SOURCE_METADATA_POPULATION_PACKET_PATH)
    populated_surface = read_json(SOURCE_METADATA_POPULATED_SURFACE_PATH)
    coverage = read_json(SOURCE_METADATA_POPULATION_COVERAGE_PATH)
    readiness = read_json(SOURCE_DISCRIMINATOR_READINESS_PATH)
    gaps = read_json(SOURCE_METADATA_POPULATION_GAPS_PATH)
    classif = read_json(SOURCE_METADATA_POPULATION_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_METADATA_POPULATION_ROLLUP_PATH)
    prof = read_json(SOURCE_METADATA_POPULATION_PROFILE_PATH)
    surface_receipt = read_json(SOURCE_METADATA_SURFACE_RECEIPT_PATH)

    summary = receipt.get("typed_metadata_population_summary", {})

    if receipt.get("receipt_id") != SOURCE_METADATA_POPULATION_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("metadata_population_receipt_not_pass")
    if summary.get("status") != EXPECTED_POPULATION_STATUS:
        failures.append(f"metadata_population_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_POPULATION_STOP:
        failures.append("metadata_population_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"metadata_population_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("metadata_populated") is not True:
        failures.append("metadata_population_not_populated")
    if summary.get("metadata_fully_populated") is not False:
        failures.append("metadata_population_fully_populated_unexpectedly")
    if summary.get("ready_discriminator_count") != 0:
        failures.append("ready_discriminator_count_not_zero")
    if summary.get("total_required_field_count") != 45:
        failures.append(f"total_required_field_count_not_45:{summary.get('total_required_field_count')}")
    if summary.get("total_populated_field_count") != 15:
        failures.append(f"total_populated_field_count_not_15:{summary.get('total_populated_field_count')}")
    if summary.get("total_missing_field_count") != 30:
        failures.append(f"total_missing_field_count_not_30:{summary.get('total_missing_field_count')}")
    if summary.get("fully_missing_field_count") != 10:
        failures.append(f"fully_missing_field_count_not_10:{summary.get('fully_missing_field_count')}")
    if summary.get("rule_refined") is not False:
        failures.append("metadata_population_refined_rule")
    if summary.get("tie_broken") is not False:
        failures.append("metadata_population_broke_tie")
    if summary.get("candidate_values_filled") is not False:
        failures.append("metadata_population_filled_candidate_values")

    if packet.get("packet_status") != "TYPED_VALUE_SOURCE_METADATA_PARTIALLY_POPULATED":
        failures.append("population_packet_status_wrong")
    if populated_surface.get("surface_status") != "TYPED_VALUE_SOURCE_METADATA_PARTIALLY_POPULATED_STILL_INSUFFICIENT":
        failures.append("populated_surface_status_wrong")
    if coverage.get("coverage_status") != "PARTIAL_METADATA_COVERAGE":
        failures.append("coverage_status_wrong")
    if readiness.get("readiness_status") != "NO_DISCRIMINATOR_READY_FOR_RULE_REFINEMENT":
        failures.append("readiness_status_wrong")
    if gaps.get("gap_status") != "TYPED_METADATA_POPULATION_GAPS_REMAIN":
        failures.append("gaps_status_wrong")
    if classif.get("classification_status") != EXPECTED_POPULATION_STATUS:
        failures.append("population_classification_status_wrong")
    if roll.get("recommended_next") != EXPECTED_NEXT:
        failures.append("rollup_next_not_expected")
    if prof.get("recommended_next") != EXPECTED_NEXT:
        failures.append("profile_next_not_expected")

    surface_summary = surface_receipt.get("typed_metadata_surface_summary", {})
    if surface_receipt.get("receipt_id") != SOURCE_METADATA_SURFACE_RECEIPT_ID or surface_receipt.get("gate") != "PASS":
        failures.append("metadata_surface_receipt_not_pass")
    if surface_summary.get("metadata_surface_built") is not True:
        failures.append("source_metadata_surface_not_built")

    return failures

def source_rows() -> List[Dict[str, Any]]:
    packet = read_json(SOURCE_METADATA_POPULATION_PACKET_PATH)
    rows = packet.get("populated_rows", [])
    return [r for r in rows if isinstance(r, dict)]

def field_coverage() -> Dict[str, Any]:
    coverage = read_json(SOURCE_METADATA_POPULATION_COVERAGE_PATH)
    return coverage.get("field_coverage", {})

def missing_fields_from_coverage() -> List[str]:
    cov = field_coverage()
    missing = []
    for field, item in cov.items():
        if isinstance(item, dict) and item.get("missing", 0) > 0:
            missing.append(field)
    return sorted(missing)

def policy_for_field(field: str) -> Dict[str, Any]:
    if field in ALREADY_POPULATED_IDENTITY_FIELDS:
        source_class = "already_populated_from_explicit_row_identity"
        allowed_sources = [
            "existing population packet",
            "explicit row source_ref/json_path/row_uid",
            "receipt-backed trace"
        ]
        requirement = "none"
        bridge_role = "already_populated"
        human_schema_only = False
    elif field in SOURCE_BRIDGE_FIELDS:
        source_class = "requires_typed_source_bridge"
        allowed_sources = [
            "typed value-source metadata source packet",
            "prevalidated schema field",
            "explicit source artifact referenced by source packet"
        ]
        requirement = "source_packet_required"
        bridge_role = "machine_readable_after_bridge_population"
        human_schema_only = False
    elif field in HUMAN_SCHEMA_ONLY_FIELDS:
        source_class = "requires_human_or_prevalidated_schema_boundary"
        allowed_sources = [
            "human review packet",
            "prevalidated schema preference packet",
            "explicit acceptance-boundary packet"
        ]
        requirement = "human_or_prevalidated_schema_source_required"
        bridge_role = "review_or_schema_boundary"
        human_schema_only = True
    else:
        source_class = "unknown_field_requires_review"
        allowed_sources = [
            "human review packet",
            "schema update proposal"
        ]
        requirement = "taxonomy_or_schema_review_required"
        bridge_role = "unknown"
        human_schema_only = True

    return {
        "field": field,
        "source_class": source_class,
        "bridge_role": bridge_role,
        "human_schema_only": human_schema_only,
        "allowed_sources": allowed_sources,
        "required_source_object": requirement,
        "purpose": FIELD_PURPOSE.get(field, "No v0 purpose registered."),
        "forbidden_sources": [
            "latest-file guessing",
            "mtime selection",
            "alphabetical preference",
            "first-seen order",
            "unstated semantic inference",
            "hidden preference",
            "current dominance rank score"
        ],
        "may_be_used_for_rule_refinement_after_population": field in SOURCE_BRIDGE_FIELDS,
        "may_force_review_boundary": human_schema_only,
    }

def build_field_policy() -> Dict[str, Any]:
    cov = field_coverage()
    policies = []
    for field in sorted(cov.keys()):
        item = cov[field]
        policy = policy_for_field(field)
        policy["population_coverage"] = item
        policy["currently_missing"] = bool(isinstance(item, dict) and item.get("missing", 0) > 0)
        policy["currently_populated_count"] = item.get("populated", 0) if isinstance(item, dict) else 0
        policy["currently_missing_count"] = item.get("missing", 0) if isinstance(item, dict) else 0
        policies.append(policy)

    missing = [p for p in policies if p["currently_missing"]]
    source_bridge_missing = [p for p in missing if p["source_class"] == "requires_typed_source_bridge"]
    human_schema_missing = [p for p in missing if p["source_class"] == "requires_human_or_prevalidated_schema_boundary"]

    return {
        "schema_version": "typed_value_source_metadata_source_field_policy_v0",
        "field_policy_id": "metadata_field_policy_" + sha8(policies),
        "source_population_receipt_id": SOURCE_METADATA_POPULATION_RECEIPT_ID,
        "field_policy_status": "TYPED_METADATA_FIELD_SOURCE_POLICIES_EMITTED",
        "field_count": len(policies),
        "missing_field_count": len(missing),
        "source_bridge_required_field_count": len(source_bridge_missing),
        "human_or_schema_only_field_count": len(human_schema_missing),
        "field_policies": policies,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def build_row_requirements(rows: List[Dict[str, Any]], policy: Dict[str, Any]) -> Dict[str, Any]:
    policy_by_field = {p["field"]: p for p in policy["field_policies"]}
    row_requirements = []

    for row in rows:
        row_fields = []
        for item in row.get("fields", []):
            field = item.get("field")
            pol = policy_by_field.get(field, policy_for_field(str(field)))
            if str(item.get("status", "")).startswith("POPULATED_"):
                status = "ALREADY_POPULATED"
                required = False
            else:
                status = "SOURCE_REQUIRED"
                required = True
            row_fields.append({
                "field": field,
                "current_status": item.get("status"),
                "source_requirement_status": status,
                "source_required": required,
                "source_class": pol["source_class"],
                "required_source_object": pol["required_source_object"],
                "allowed_sources": pol["allowed_sources"],
                "human_schema_only": pol["human_schema_only"],
            })

        row_requirements.append({
            "row_uid": row.get("row_uid"),
            "row_index": row.get("row_index"),
            "source_ref": row.get("source_ref"),
            "json_path": row.get("json_path"),
            "value": row.get("value"),
            "required_sources_by_field": row_fields,
            "missing_source_count": sum(1 for f in row_fields if f["source_required"]),
            "row_source_bridge_status": "SOURCE_BRIDGE_REQUIRED" if any(f["source_required"] for f in row_fields) else "SOURCE_BRIDGE_NOT_REQUIRED",
        })

    return {
        "schema_version": "typed_value_source_metadata_row_source_requirements_v0",
        "row_source_requirements_id": "row_source_requirements_" + sha8(row_requirements),
        "row_count": len(row_requirements),
        "row_source_requirements": row_requirements,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def build_source_packet_template(rows: List[Dict[str, Any]], policy: Dict[str, Any]) -> Dict[str, Any]:
    policy_by_field = {p["field"]: p for p in policy["field_policies"]}
    template_rows = []

    for row in rows:
        missing_items = []
        for item in row.get("fields", []):
            field = item.get("field")
            if str(item.get("status", "")).startswith("POPULATED_"):
                continue
            pol = policy_by_field.get(field, policy_for_field(str(field)))
            missing_items.append({
                "field": field,
                "value": None,
                "source_ref": None,
                "source_class": pol["source_class"],
                "required_source_object": pol["required_source_object"],
                "human_schema_only": pol["human_schema_only"],
                "evidence_or_review_ref": None,
                "notes": None,
            })

        template_rows.append({
            "row_uid": row.get("row_uid"),
            "row_index": row.get("row_index"),
            "source_ref": row.get("source_ref"),
            "json_path": row.get("json_path"),
            "value": row.get("value"),
            "missing_metadata_to_supply": missing_items,
        })

    return {
        "schema_version": "typed_value_source_metadata_source_packet_template_v0",
        "template_id": "metadata_source_packet_template_" + sha8(template_rows),
        "object_type": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET",
        "template_status": "SOURCE_PACKET_TEMPLATE_EMITTED",
        "source_bridge_ref": rel(SOURCE_BRIDGE_PATH),
        "row_count": len(template_rows),
        "rows": template_rows,
        "packet_rules": {
            "must_preserve_row_uid": True,
            "must_supply_source_ref_for_each_non_null_value": True,
            "must_mark_human_schema_only_fields_as_review_or_schema_sources": True,
            "must_not_select_target": True,
            "must_not_break_tie": True,
            "must_not_refine_rule": True,
            "must_not_accept_for_build": True,
            "must_not_apply_patch": True,
        },
        "recommended_next": "PROVIDE_OR_REVIEW_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_V0",
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def build_human_schema_only(policy: Dict[str, Any]) -> Dict[str, Any]:
    fields = [p for p in policy["field_policies"] if p["human_schema_only"] and p["currently_missing"]]
    return {
        "schema_version": "typed_value_source_metadata_human_schema_only_fields_v0",
        "status": "HUMAN_OR_SCHEMA_ONLY_FIELDS_IDENTIFIED",
        "field_count": len(fields),
        "fields": fields,
        "review_boundary": "human_or_prevalidated_schema_acceptance_required",
        "machine_must_not_infer": [p["field"] for p in fields],
    }

def build_bridge(rows: List[Dict[str, Any]], policy: Dict[str, Any], row_reqs: Dict[str, Any], packet_template: Dict[str, Any], human_schema: Dict[str, Any]) -> Dict[str, Any]:
    source_bridge_required = policy["source_bridge_required_field_count"]
    human_schema_required = policy["human_or_schema_only_field_count"]

    return {
        "schema_version": "typed_value_source_metadata_source_bridge_v0",
        "source_bridge_id": "metadata_source_bridge_" + sha8({
            "source_population": SOURCE_METADATA_POPULATION_RECEIPT_ID,
            "policy": policy.get("field_policy_id"),
            "rows": row_reqs.get("row_source_requirements_id"),
        }),
        "source_population_receipt_id": SOURCE_METADATA_POPULATION_RECEIPT_ID,
        "source_metadata_surface_receipt_id": SOURCE_METADATA_SURFACE_RECEIPT_ID,
        "bridge_status": "TYPED_VALUE_SOURCE_METADATA_SOURCE_BRIDGE_BUILT_REQUIRES_SOURCE_PACKET",
        "purpose": "Bind missing typed metadata fields to lawful source classes without filling metadata, breaking tie, or refining dominance rule.",
        "receipt_backed_claim": "Metadata was partially populated from explicit identity, but discriminator use is not ready because source-bridged metadata is missing.",
        "row_count": len(rows),
        "missing_field_count": policy["missing_field_count"],
        "source_bridge_required_field_count": source_bridge_required,
        "human_or_schema_only_field_count": human_schema_required,
        "field_policy_ref": rel(FIELD_POLICY_PATH),
        "row_source_requirements_ref": rel(ROW_SOURCE_REQUIREMENTS_PATH),
        "source_packet_template_ref": rel(SOURCE_PACKET_TEMPLATE_PATH),
        "human_schema_only_fields_ref": rel(HUMAN_SCHEMA_ONLY_FIELDS_PATH),
        "allowed_next_input_object": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET",
        "not_authorized": [
            "populate missing metadata",
            "evaluate discriminators",
            "refine dominance rule",
            "break tie",
            "fill candidate values",
            "declare target candidate for review",
            "select target for build",
            "accept for build",
            "apply runtime patch",
            "open C5",
            "grant general Cell1 authority"
        ],
        "recommended_next": "PROVIDE_OR_REVIEW_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_V0",
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def classify_bridge(bridge: Dict[str, Any], policy: Dict[str, Any]) -> Tuple[str, List[str], str]:
    reason_codes = [
        "MISSING_METADATA_FIELDS_BOUND_TO_ALLOWED_SOURCE_CLASSES",
        "SOURCE_PACKET_TEMPLATE_EMITTED",
        "HUMAN_OR_SCHEMA_ONLY_FIELDS_IDENTIFIED",
        "DISCRIMINATOR_METADATA_NOT_READY_UNTIL_SOURCE_PACKET_REVIEWED",
    ]

    if policy["source_bridge_required_field_count"] > 0:
        reason_codes.append("MACHINE_READABLE_SOURCE_BRIDGE_FIELDS_REQUIRE_PACKET")
    if policy["human_or_schema_only_field_count"] > 0:
        reason_codes.append("HUMAN_OR_PREVALIDATED_SCHEMA_BOUNDARY_FIELDS_REQUIRE_PACKET")

    status = "TYPED_VALUE_SOURCE_METADATA_SOURCE_BRIDGE_BUILT_REQUIRES_SOURCE_PACKET"
    next_edge = "PROVIDE_OR_REVIEW_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_V0"
    return status, reason_codes, next_edge

def classification_obj(status: str, reason_codes: List[str], next_edge: str, bridge: Dict[str, Any], policy: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_bridge_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "missing_field_count": bridge["missing_field_count"],
        "source_bridge_required_field_count": bridge["source_bridge_required_field_count"],
        "human_or_schema_only_field_count": bridge["human_or_schema_only_field_count"],
        "source_packet_template_emitted": True,
        "metadata_populated": False,
        "metadata_source_packet_provided": False,
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

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_bridge_authority_boundary_v0",
        "status": status,
        "may_build_source_bridge": True,
        "may_emit_field_policy": True,
        "may_emit_source_packet_template": True,
        "may_identify_human_schema_only_fields": True,
        "may_populate_missing_metadata": False,
        "may_review_source_packet": False,
        "may_evaluate_discriminators": False,
        "may_refine_rule": False,
        "may_break_tie": False,
        "may_emit_candidate_values": False,
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

def rollup_obj(status: str, bridge: Dict[str, Any], policy: Dict[str, Any], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_bridge_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "source_bridge_emitted_count": 1,
        "field_policy_emitted_count": 1,
        "source_packet_template_emitted_count": 1,
        "human_schema_only_fields_emitted_count": 1,
        "missing_field_count": bridge["missing_field_count"],
        "source_bridge_required_field_count": bridge["source_bridge_required_field_count"],
        "human_or_schema_only_field_count": bridge["human_or_schema_only_field_count"],
        "metadata_source_packet_provided_count": 0,
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
        "metadata_source_packet_provided_count",
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
        "schema_version": "typed_value_source_metadata_source_bridge_profile_v0",
        "profile_id": "metadata_source_bridge_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "source_bridge_built": True,
        "metadata_source_packet_provided": False,
        "metadata_populated": False,
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

def report_obj(status: str, reason_codes: List[str], bridge: Dict[str, Any], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_bridge_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Metadata population remains insufficient; this unit maps missing fields to lawful source classes and emits a source packet template.",
        "missing_field_count": bridge["missing_field_count"],
        "source_bridge_required_field_count": bridge["source_bridge_required_field_count"],
        "human_or_schema_only_field_count": bridge["human_or_schema_only_field_count"],
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "metadata_source_packet_provided_count": 0,
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
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
    }

def transition_trace_obj(status: str, reason_codes: List[str], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_bridge_transition_trace_v0",
        "trace": [
            {
                "step": "consume_partial_metadata_population",
                "question": "why are discriminators still unavailable",
                "answer": "metadata partially populated but no discriminator ready",
                "taken": "build source bridge for missing typed metadata",
            },
            {
                "step": "bind_missing_fields_to_source_classes",
                "question": "where may missing metadata lawfully come from",
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
    failures = validate_source_basis()

    rows = source_rows() if not failures else []
    policy = build_field_policy() if not failures else {
        "schema_version": "typed_value_source_metadata_source_field_policy_v0",
        "field_policy_id": "metadata_field_policy_source_fail_" + sha8(failures),
        "field_policy_status": "SOURCE_BASIS_FAIL",
        "field_count": 0,
        "missing_field_count": 0,
        "source_bridge_required_field_count": 0,
        "human_or_schema_only_field_count": 0,
        "field_policies": [],
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }
    row_reqs = build_row_requirements(rows, policy) if not failures else {
        "schema_version": "typed_value_source_metadata_row_source_requirements_v0",
        "row_source_requirements_id": "row_source_requirements_source_fail_" + sha8(failures),
        "row_count": 0,
        "row_source_requirements": [],
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }
    packet_template = build_source_packet_template(rows, policy) if not failures else {
        "schema_version": "typed_value_source_metadata_source_packet_template_v0",
        "template_id": "metadata_source_packet_template_source_fail_" + sha8(failures),
        "object_type": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET",
        "template_status": "SOURCE_BASIS_FAIL",
        "row_count": 0,
        "rows": [],
        "recommended_next": "REPAIR_TYPED_VALUE_SOURCE_METADATA_SOURCE_BRIDGE_BASIS_V0",
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }
    human_schema = build_human_schema_only(policy) if not failures else {
        "schema_version": "typed_value_source_metadata_human_schema_only_fields_v0",
        "status": "SOURCE_BASIS_FAIL",
        "field_count": 0,
        "fields": [],
        "review_boundary": "human_or_prevalidated_schema_acceptance_required",
        "machine_must_not_infer": [],
    }
    bridge = build_bridge(rows, policy, row_reqs, packet_template, human_schema) if not failures else {
        "schema_version": "typed_value_source_metadata_source_bridge_v0",
        "source_bridge_id": "metadata_source_bridge_source_fail_" + sha8(failures),
        "bridge_status": "TYPED_VALUE_SOURCE_METADATA_SOURCE_BRIDGE_SOURCE_BASIS_FAIL",
        "purpose": "Source basis failed.",
        "row_count": 0,
        "missing_field_count": 0,
        "source_bridge_required_field_count": 0,
        "human_or_schema_only_field_count": 0,
        "field_policy_ref": rel(FIELD_POLICY_PATH),
        "row_source_requirements_ref": rel(ROW_SOURCE_REQUIREMENTS_PATH),
        "source_packet_template_ref": rel(SOURCE_PACKET_TEMPLATE_PATH),
        "human_schema_only_fields_ref": rel(HUMAN_SCHEMA_ONLY_FIELDS_PATH),
        "recommended_next": "REPAIR_TYPED_VALUE_SOURCE_METADATA_SOURCE_BRIDGE_BASIS_V0",
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    if failures:
        status = "TYPED_VALUE_SOURCE_METADATA_SOURCE_BRIDGE_SOURCE_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_TYPED_VALUE_SOURCE_METADATA_SOURCE_BRIDGE_BASIS_V0"
    else:
        status, reason_codes, next_edge = classify_bridge(bridge, policy)

    classif = classification_obj(status, reason_codes, next_edge, bridge, policy)
    boundary = authority_boundary_obj(status)
    roll = rollup_obj(status, bridge, policy, next_edge)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, bridge, next_edge)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    write_json(FIELD_POLICY_PATH, policy)
    write_json(ROW_SOURCE_REQUIREMENTS_PATH, row_reqs)
    write_json(SOURCE_PACKET_TEMPLATE_PATH, packet_template)
    write_json(HUMAN_SCHEMA_ONLY_FIELDS_PATH, human_schema)
    write_json(SOURCE_BRIDGE_PATH, bridge)
    write_json(CLASSIFICATION_PATH, classif)
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
        "SOURCE_BRIDGE_0_POPULATION_RECEIPT_CONSUMED": SOURCE_METADATA_POPULATION_RECEIPT_PATH.exists(),
        "SOURCE_BRIDGE_1_POPULATION_PACKET_CONSUMED": SOURCE_METADATA_POPULATION_PACKET_PATH.exists(),
        "SOURCE_BRIDGE_2_COVERAGE_CONSUMED": SOURCE_METADATA_POPULATION_COVERAGE_PATH.exists(),
        "SOURCE_BRIDGE_3_GAPS_CONSUMED": SOURCE_METADATA_POPULATION_GAPS_PATH.exists(),
        "SOURCE_BRIDGE_4_SOURCE_BRIDGE_EMITTED": SOURCE_BRIDGE_PATH.exists(),
        "SOURCE_BRIDGE_5_FIELD_POLICY_EMITTED": FIELD_POLICY_PATH.exists(),
        "SOURCE_BRIDGE_6_SOURCE_PACKET_TEMPLATE_EMITTED": SOURCE_PACKET_TEMPLATE_PATH.exists(),
        "SOURCE_BRIDGE_7_ROW_REQUIREMENTS_EMITTED": ROW_SOURCE_REQUIREMENTS_PATH.exists(),
        "SOURCE_BRIDGE_8_HUMAN_SCHEMA_ONLY_FIELDS_EMITTED": HUMAN_SCHEMA_ONLY_FIELDS_PATH.exists(),
        "SOURCE_BRIDGE_9_NO_METADATA_SOURCE_PACKET_PROVIDED": roll["metadata_source_packet_provided_count"] == 0,
        "SOURCE_BRIDGE_10_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "SOURCE_BRIDGE_11_NO_DISCRIMINATOR_READY": roll["ready_discriminator_count"] == 0,
        "SOURCE_BRIDGE_12_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "SOURCE_BRIDGE_13_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "SOURCE_BRIDGE_14_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "SOURCE_BRIDGE_15_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classif["target_candidate_declared_for_review"] is False,
        "SOURCE_BRIDGE_16_NO_TARGET_SELECTED_FOR_BUILD": classif["target_selected_for_build"] is False,
        "SOURCE_BRIDGE_17_NO_ACCEPTED_FOR_BUILD": classif["accepted_for_build"] is False,
        "SOURCE_BRIDGE_18_NO_RUNTIME_PATCH": classif["runtime_patch_authorized"] is False,
        "SOURCE_BRIDGE_19_NO_TARGET_FILE_MODIFICATION": classif["target_file_modification_authorized"] is False,
        "SOURCE_BRIDGE_20_NO_C5_OPENED": classif["c5_authorized"] is False,
        "SOURCE_BRIDGE_21_NO_GENERAL_CELL1_AUTHORITY": classif["general_cell1_authority_granted"] is False,
        "SOURCE_BRIDGE_22_NO_LATEST_FILE_GUESSING": classif["latest_file_guessing"] is False,
        "SOURCE_BRIDGE_23_NO_MTIME_SELECTION": classif["mtime_selection"] is False,
        "SOURCE_BRIDGE_24_NO_HIDDEN_NEXT_COMMAND": classif["next_command_goal"] is None,
        "SOURCE_BRIDGE_25_ACCEPTANCE_BOUNDARY_RETAINED": classif["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "SOURCE_BRIDGE_26_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_VALUE_SOURCE_METADATA_SOURCE_BRIDGE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "bridge": bridge.get("source_bridge_id"),
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_value_source_metadata_source_bridge_receipt_v0",
        "receipt_type": "TYPED_VALUE_SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_metadata_population_receipt_id": SOURCE_METADATA_POPULATION_RECEIPT_ID,
        "source_metadata_surface_receipt_id": SOURCE_METADATA_SURFACE_RECEIPT_ID,
        "typed_metadata_source_bridge_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "row_count": bridge["row_count"],
            "missing_field_count": bridge["missing_field_count"],
            "source_bridge_required_field_count": bridge["source_bridge_required_field_count"],
            "human_or_schema_only_field_count": bridge["human_or_schema_only_field_count"],
            "source_packet_template_emitted": True,
            "metadata_source_packet_provided": False,
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
            "source_bridge": rel(SOURCE_BRIDGE_PATH),
            "field_policy": rel(FIELD_POLICY_PATH),
            "source_packet_template": rel(SOURCE_PACKET_TEMPLATE_PATH),
            "row_source_requirements": rel(ROW_SOURCE_REQUIREMENTS_PATH),
            "human_schema_only_fields": rel(HUMAN_SCHEMA_ONLY_FIELDS_PATH),
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
    print(f"metadata_source_bridge_receipt_id={receipt_id}")
    print(f"metadata_source_bridge_receipt_path={rel(receipt_path)}")
    print(f"metadata_source_bridge_path={rel(SOURCE_BRIDGE_PATH)}")
    print(f"metadata_source_field_policy_path={rel(FIELD_POLICY_PATH)}")
    print(f"metadata_source_packet_template_path={rel(SOURCE_PACKET_TEMPLATE_PATH)}")
    print(f"metadata_row_source_requirements_path={rel(ROW_SOURCE_REQUIREMENTS_PATH)}")
    print(f"metadata_human_schema_only_fields_path={rel(HUMAN_SCHEMA_ONLY_FIELDS_PATH)}")
    print(f"metadata_source_bridge_classification_path={rel(CLASSIFICATION_PATH)}")
    print(f"metadata_source_bridge_rollup_path={rel(ROLLUP_PATH)}")
    print(f"metadata_source_bridge_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
