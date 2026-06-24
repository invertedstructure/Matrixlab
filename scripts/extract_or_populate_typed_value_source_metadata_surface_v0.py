#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "EXTRACT_OR_POPULATE_TYPED_VALUE_SOURCE_METADATA_SURFACE_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_population.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_POPULATION"
MODE = "EXTRACT_OR_POPULATE_METADATA / NO_TIE_BREAK / NO_ACCEPTANCE"
BUILD_MODE = "TYPED_METADATA_POPULATION_ONLY"

SOURCE_METADATA_SURFACE_RECEIPT_ID = "3b98c589"
SOURCE_METADATA_SURFACE_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_surface_v0_receipts/3b98c589.json"
SOURCE_METADATA_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_surface_v0/typed_value_source_metadata_surface_v0.json"
SOURCE_ROW_METADATA_TEMPLATE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_surface_v0/typed_value_source_row_metadata_template_v0.json"
SOURCE_DISCRIMINATOR_CANDIDATE_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_surface_v0/typed_value_source_discriminator_candidate_surface_v0.json"
SOURCE_METADATA_EXTRACTION_REQUEST_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_surface_v0/typed_value_source_metadata_extraction_request_v0.json"
SOURCE_METADATA_SURFACE_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_surface_v0/typed_value_source_metadata_surface_classification_v0.json"
SOURCE_METADATA_SURFACE_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_surface_v0/typed_value_source_metadata_surface_rollup_v0.json"
SOURCE_METADATA_SURFACE_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_surface_v0/typed_value_source_metadata_surface_profile_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_population_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_population_v0_receipts"

POPULATION_PACKET_PATH = OUT_DIR / "typed_value_source_metadata_population_packet_v0.json"
POPULATED_SURFACE_PATH = OUT_DIR / "typed_value_source_metadata_populated_surface_v0.json"
POPULATION_COVERAGE_PATH = OUT_DIR / "typed_value_source_metadata_population_coverage_v0.json"
DISCRIMINATOR_READINESS_PATH = OUT_DIR / "typed_value_source_discriminator_readiness_v0.json"
POPULATION_GAPS_PATH = OUT_DIR / "typed_value_source_metadata_population_gaps_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_value_source_metadata_population_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_value_source_metadata_population_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_value_source_metadata_population_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_value_source_metadata_population_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_value_source_metadata_population_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_value_source_metadata_population_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_METADATA_SURFACE_RECEIPT_PATH,
    SOURCE_METADATA_SURFACE_PATH,
    SOURCE_ROW_METADATA_TEMPLATE_PATH,
    SOURCE_DISCRIMINATOR_CANDIDATE_SURFACE_PATH,
    SOURCE_METADATA_EXTRACTION_REQUEST_PATH,
    SOURCE_METADATA_SURFACE_CLASSIFICATION_PATH,
    SOURCE_METADATA_SURFACE_ROLLUP_PATH,
    SOURCE_METADATA_SURFACE_PROFILE_PATH,
]

EXPECTED_SOURCE_STATUS = "NARROWER_TYPED_VALUE_SOURCE_METADATA_SURFACE_BUILT_NEEDS_POPULATION"
EXPECTED_SOURCE_STOP = "STOP_NARROWER_TYPED_VALUE_SOURCE_METADATA_SURFACE_BUILT_NEEDS_POPULATION"

CORE_METADATA_FIELDS = [
    "direct_evidence_ref",
    "direct_evidence_strength",
    "load_bearing_reason",
    "target_scope",
    "target_aspect",
    "comparison_grain",
    "source_authority",
    "source_role",
    "inference_strength",
    "inference_chain_ref",
    "provenance_depth",
    "verification_gate_ref",
    "rollback_or_stop_boundary_ref",
    "schema_preference_key",
    "human_preference_boundary_ref",
]

DERIVABLE_FROM_ROW_IDENTITY = {
    "direct_evidence_ref",
    "source_role",
    "source_authority",
    "provenance_depth",
    "inference_chain_ref",
}

NON_DERIVABLE_WITHOUT_TYPED_SOURCE = {
    "direct_evidence_strength",
    "load_bearing_reason",
    "target_scope",
    "target_aspect",
    "comparison_grain",
    "inference_strength",
    "verification_gate_ref",
    "rollback_or_stop_boundary_ref",
    "schema_preference_key",
    "human_preference_boundary_ref",
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

    receipt = read_json(SOURCE_METADATA_SURFACE_RECEIPT_PATH)
    surface = read_json(SOURCE_METADATA_SURFACE_PATH)
    template = read_json(SOURCE_ROW_METADATA_TEMPLATE_PATH)
    discrim = read_json(SOURCE_DISCRIMINATOR_CANDIDATE_SURFACE_PATH)
    extraction = read_json(SOURCE_METADATA_EXTRACTION_REQUEST_PATH)
    classif = read_json(SOURCE_METADATA_SURFACE_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_METADATA_SURFACE_ROLLUP_PATH)
    prof = read_json(SOURCE_METADATA_SURFACE_PROFILE_PATH)

    summary = receipt.get("typed_metadata_surface_summary", {})

    if receipt.get("receipt_id") != SOURCE_METADATA_SURFACE_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("metadata_surface_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"metadata_surface_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("metadata_surface_terminal_not_expected")
    if summary.get("metadata_surface_built") is not True:
        failures.append("metadata_surface_not_built")
    if summary.get("metadata_populated") is not False:
        failures.append("metadata_surface_already_populated")
    if summary.get("rule_refined") is not False:
        failures.append("metadata_surface_refined_rule")
    if summary.get("tie_broken") is not False:
        failures.append("metadata_surface_broke_tie")
    if summary.get("candidate_values_filled") is not False:
        failures.append("metadata_surface_filled_candidate_values")
    if summary.get("top_row_count") != 3:
        failures.append(f"metadata_surface_top_row_count_not_3:{summary.get('top_row_count')}")
    if summary.get("missing_typed_metadata_count") != 15:
        failures.append(f"metadata_surface_missing_count_not_15:{summary.get('missing_typed_metadata_count')}")
    if summary.get("candidate_discriminator_count") != 4:
        failures.append(f"metadata_surface_candidate_discriminator_count_not_4:{summary.get('candidate_discriminator_count')}")

    if surface.get("surface_status") != "NARROWER_TYPED_VALUE_SOURCE_METADATA_SURFACE_BUILT":
        failures.append(f"surface_artifact_status_wrong:{surface.get('surface_status')}")
    if surface.get("top_row_count") != 3:
        failures.append("surface_artifact_top_count_not_3")
    if surface.get("missing_typed_metadata_count") != 15:
        failures.append("surface_artifact_missing_count_not_15")

    if template.get("template_status") != "ROW_METADATA_TEMPLATES_EMITTED":
        failures.append("row_template_status_wrong")
    if template.get("row_count") != 3:
        failures.append(f"row_template_count_not_3:{template.get('row_count')}")
    if template.get("required_fields") != CORE_METADATA_FIELDS:
        failures.append("row_template_required_fields_changed")

    if discrim.get("discriminator_status") != "VISIBLE_DIFFERENCES_REQUIRE_TYPED_METADATA_BEFORE_RULE_USE":
        failures.append("discriminator_surface_status_wrong")

    if extraction.get("request_status") != "TYPED_VALUE_SOURCE_METADATA_EXTRACTION_REQUESTED":
        failures.append("extraction_request_status_wrong")

    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("source_classification_status_wrong")
    if classif.get("target_selected_for_build") is not False:
        failures.append("source_classification_selects_target_for_build")
    if classif.get("accepted_for_build") is not False:
        failures.append("source_classification_accepts_for_build")
    if classif.get("runtime_patch_authorized") is not False:
        failures.append("source_classification_authorizes_runtime_patch")

    if roll.get("metadata_populated_count") != 0:
        failures.append("source_rollup_metadata_populated_nonzero")
    if prof.get("metadata_populated") is not False:
        failures.append("source_profile_metadata_populated")

    return failures

def row_templates() -> List[Dict[str, Any]]:
    template = read_json(SOURCE_ROW_METADATA_TEMPLATE_PATH)
    rows = template.get("row_metadata_templates", [])
    return [r for r in rows if isinstance(r, dict)]

def source_discriminators() -> List[Dict[str, Any]]:
    surface = read_json(SOURCE_DISCRIMINATOR_CANDIDATE_SURFACE_PATH)
    rows = surface.get("visible_candidate_discriminators", [])
    return [r for r in rows if isinstance(r, dict)]

def path_depth(source_ref: str, json_path: str) -> int:
    return len([p for p in source_ref.split("/") if p]) + len([p for p in json_path.replace("[", ".").replace("]", "").split(".") if p])

def populate_field(row: Dict[str, Any], field: str) -> Dict[str, Any]:
    source_ref = str(row.get("source_ref", ""))
    json_path = str(row.get("json_path", ""))
    value = row.get("value")
    role = row.get("role")
    row_uid = row.get("row_uid")

    if field == "direct_evidence_ref":
        return {
            "field": field,
            "status": "POPULATED_EXPLICIT_ROW_IDENTITY",
            "value": {
                "source_ref": source_ref,
                "json_path": json_path,
                "row_uid": row_uid,
            },
            "basis": "row source_ref/json_path/row_uid from existing metadata template",
            "usable_for_tie_break": False,
            "requires_review_before_rule_use": True,
        }

    if field == "source_role":
        return {
            "field": field,
            "status": "POPULATED_EXPLICIT_ROW_IDENTITY",
            "value": role,
            "basis": "row role from existing metadata template",
            "usable_for_tie_break": False,
            "requires_review_before_rule_use": True,
        }

    if field == "source_authority":
        authority = "primary_value_surface" if "target_hint_inventory" in source_ref or "runtime_patch_target_evidence_request" in source_ref else "derived_or_support_surface"
        return {
            "field": field,
            "status": "POPULATED_DERIVED_FROM_EXPLICIT_SOURCE_REF",
            "value": authority,
            "basis": "bounded classification from explicit source_ref",
            "usable_for_tie_break": False,
            "requires_review_before_rule_use": True,
        }

    if field == "provenance_depth":
        return {
            "field": field,
            "status": "POPULATED_DERIVED_FROM_EXPLICIT_PATH_DEPTH",
            "value": path_depth(source_ref, json_path),
            "basis": "counted source_ref/json_path path segments",
            "usable_for_tie_break": False,
            "requires_review_before_rule_use": True,
        }

    if field == "inference_chain_ref":
        return {
            "field": field,
            "status": "POPULATED_EXPLICIT_TRACE_REF",
            "value": {
                "metadata_surface_receipt": rel(SOURCE_METADATA_SURFACE_RECEIPT_PATH),
                "metadata_surface": rel(SOURCE_METADATA_SURFACE_PATH),
                "row_metadata_template": rel(SOURCE_ROW_METADATA_TEMPLATE_PATH),
            },
            "basis": "current receipt-backed extraction trace",
            "usable_for_tie_break": False,
            "requires_review_before_rule_use": True,
        }

    return {
        "field": field,
        "status": "MISSING_NO_EXPLICIT_TYPED_SOURCE",
        "value": None,
        "basis": "not derivable from current row identity/template surface without semantic inference",
        "usable_for_tie_break": False,
        "requires_review_before_rule_use": True,
    }

def build_population_packet(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    populated_rows = []
    for row in rows:
        fields = [populate_field(row, field) for field in CORE_METADATA_FIELDS]
        populated_count = sum(1 for f in fields if str(f["status"]).startswith("POPULATED_"))
        missing_count = sum(1 for f in fields if str(f["status"]).startswith("MISSING_"))

        populated_rows.append({
            "row_uid": row.get("row_uid"),
            "row_index": row.get("row_index"),
            "source_ref": row.get("source_ref"),
            "json_path": row.get("json_path"),
            "value": row.get("value"),
            "role": row.get("role"),
            "fields": fields,
            "populated_field_count": populated_count,
            "missing_field_count": missing_count,
            "row_population_status": "PARTIALLY_POPULATED_TYPED_METADATA" if populated_count else "NO_TYPED_METADATA_POPULATED",
            "row_ready_for_discriminator_use": False,
        })

    total_populated = sum(r["populated_field_count"] for r in populated_rows)
    total_missing = sum(r["missing_field_count"] for r in populated_rows)

    return {
        "schema_version": "typed_value_source_metadata_population_packet_v0",
        "packet_id": "metadata_population_" + sha8(populated_rows),
        "packet_status": "TYPED_VALUE_SOURCE_METADATA_PARTIALLY_POPULATED",
        "source_metadata_surface_receipt_id": SOURCE_METADATA_SURFACE_RECEIPT_ID,
        "source_metadata_surface_ref": rel(SOURCE_METADATA_SURFACE_PATH),
        "source_extraction_request_ref": rel(SOURCE_METADATA_EXTRACTION_REQUEST_PATH),
        "row_count": len(populated_rows),
        "required_fields_per_row": CORE_METADATA_FIELDS,
        "total_required_field_count": len(populated_rows) * len(CORE_METADATA_FIELDS),
        "total_populated_field_count": total_populated,
        "total_missing_field_count": total_missing,
        "populated_rows": populated_rows,
        "allowed_population_basis": [
            "explicit row identity fields",
            "explicit source_ref/json_path",
            "current receipt-backed trace references",
            "mechanical path-depth count"
        ],
        "forbidden_population_basis": [
            "semantic vibe inference",
            "latest-file guessing",
            "mtime selection",
            "alphabetical preference",
            "unstated human preference",
            "hidden rule refinement"
        ],
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def build_populated_surface(packet: Dict[str, Any], discriminators: List[Dict[str, Any]]) -> Dict[str, Any]:
    source_surface = read_json(SOURCE_METADATA_SURFACE_PATH)
    return {
        "schema_version": "typed_value_source_metadata_populated_surface_v0",
        "populated_surface_id": "populated_surface_" + sha8(packet),
        "surface_status": "TYPED_VALUE_SOURCE_METADATA_PARTIALLY_POPULATED_STILL_INSUFFICIENT",
        "source_surface_ref": rel(SOURCE_METADATA_SURFACE_PATH),
        "population_packet_ref": rel(POPULATION_PACKET_PATH),
        "row_count": packet["row_count"],
        "total_required_field_count": packet["total_required_field_count"],
        "total_populated_field_count": packet["total_populated_field_count"],
        "total_missing_field_count": packet["total_missing_field_count"],
        "source_top_row_count": source_surface.get("top_row_count"),
        "same_rank_surface": source_surface.get("same_rank_surface"),
        "same_value": source_surface.get("same_value"),
        "unique_value_count": source_surface.get("unique_value_count"),
        "candidate_discriminators": discriminators,
        "candidate_discriminator_count": len([d for d in discriminators if d.get("candidate_discriminator")]),
        "discriminator_use_status": "NOT_READY_REQUIRES_MISSING_TYPED_METADATA",
        "real_tie_proven": False,
        "metadata_populated": True,
        "metadata_fully_populated": False,
        "rule_refined": False,
        "tie_broken": False,
        "candidate_values_filled": False,
        "recommended_next": "BUILD_TYPED_VALUE_SOURCE_METADATA_SOURCE_BRIDGE_V0",
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def coverage_obj(packet: Dict[str, Any]) -> Dict[str, Any]:
    fields = {field: {"populated": 0, "missing": 0} for field in CORE_METADATA_FIELDS}
    for row in packet["populated_rows"]:
        for item in row["fields"]:
            if str(item["status"]).startswith("POPULATED_"):
                fields[item["field"]]["populated"] += 1
            else:
                fields[item["field"]]["missing"] += 1

    fully_populated_fields = [k for k, v in fields.items() if v["missing"] == 0]
    fully_missing_fields = [k for k, v in fields.items() if v["populated"] == 0]

    return {
        "schema_version": "typed_value_source_metadata_population_coverage_v0",
        "coverage_status": "PARTIAL_METADATA_COVERAGE",
        "row_count": packet["row_count"],
        "total_required_field_count": packet["total_required_field_count"],
        "total_populated_field_count": packet["total_populated_field_count"],
        "total_missing_field_count": packet["total_missing_field_count"],
        "field_coverage": fields,
        "fully_populated_field_count": len(fully_populated_fields),
        "fully_populated_fields": fully_populated_fields,
        "fully_missing_field_count": len(fully_missing_fields),
        "fully_missing_fields": fully_missing_fields,
        "coverage_ratio": packet["total_populated_field_count"] / packet["total_required_field_count"] if packet["total_required_field_count"] else 0,
    }

def discriminator_readiness_obj(packet: Dict[str, Any], coverage: Dict[str, Any], discriminators: List[Dict[str, Any]]) -> Dict[str, Any]:
    needed_fields_by_discriminator = {
        "value": ["target_scope", "target_aspect", "comparison_grain", "load_bearing_reason"],
        "json_path": ["target_scope", "target_aspect", "comparison_grain", "source_role"],
        "source_ref": ["source_authority", "provenance_depth", "direct_evidence_strength"],
        "ignored_differing_field": ["schema_preference_key", "direct_evidence_strength", "load_bearing_reason"],
    }

    readiness = []
    field_cov = coverage.get("field_coverage", {})
    for disc in discriminators:
        field = str(disc.get("field", "ignored_differing_field"))
        key = field if field in needed_fields_by_discriminator else "ignored_differing_field"
        needed = needed_fields_by_discriminator[key]
        missing_needed = [
            f for f in needed
            if field_cov.get(f, {}).get("missing", 999) > 0
        ]
        readiness.append({
            "candidate_discriminator_field": field,
            "candidate_discriminator": bool(disc.get("candidate_discriminator")),
            "needed_typed_metadata_fields": needed,
            "missing_needed_fields": missing_needed,
            "ready_for_rule_refinement": bool(disc.get("candidate_discriminator")) and not missing_needed,
            "status": "READY" if bool(disc.get("candidate_discriminator")) and not missing_needed else "NOT_READY_METADATA_MISSING",
        })

    ready_count = sum(1 for r in readiness if r["ready_for_rule_refinement"])

    return {
        "schema_version": "typed_value_source_discriminator_readiness_v0",
        "readiness_status": "NO_DISCRIMINATOR_READY_FOR_RULE_REFINEMENT" if ready_count == 0 else "SOME_DISCRIMINATORS_READY_FOR_RULE_REFINEMENT",
        "candidate_discriminator_count": len(readiness),
        "ready_discriminator_count": ready_count,
        "discriminator_readiness": readiness,
        "recommended_next": "BUILD_TYPED_VALUE_SOURCE_METADATA_SOURCE_BRIDGE_V0" if ready_count == 0 else "EVALUATE_TYPED_VALUE_SOURCE_DISCRIMINATORS_V0",
    }

def gaps_obj(packet: Dict[str, Any], coverage: Dict[str, Any], readiness: Dict[str, Any]) -> Dict[str, Any]:
    gaps = []
    for field, cov in coverage["field_coverage"].items():
        if cov["missing"] > 0:
            gaps.append({
                "field": field,
                "missing_count": cov["missing"],
                "populated_count": cov["populated"],
                "gap_type": "typed_metadata_field_missing",
                "required_source_bridge": "explicit typed metadata source or prevalidated schema/human review packet",
            })

    return {
        "schema_version": "typed_value_source_metadata_population_gaps_v0",
        "gap_status": "TYPED_METADATA_POPULATION_GAPS_REMAIN",
        "gap_count": len(gaps),
        "gaps": gaps,
        "discriminator_readiness_ref": rel(DISCRIMINATOR_READINESS_PATH),
        "ready_discriminator_count": readiness["ready_discriminator_count"],
        "recommended_next": readiness["recommended_next"],
    }

def classify(packet: Dict[str, Any], coverage: Dict[str, Any], readiness: Dict[str, Any]) -> Tuple[str, List[str], str]:
    reason_codes: List[str] = []

    if packet["total_populated_field_count"] > 0:
        reason_codes.append("EXPLICIT_ROW_IDENTITY_METADATA_POPULATED")
    if packet["total_missing_field_count"] > 0:
        reason_codes.append("REQUIRED_TYPED_METADATA_STILL_MISSING")
    if coverage["fully_missing_field_count"] > 0:
        reason_codes.append("SOME_METADATA_FIELDS_HAVE_NO_SOURCE")
    if readiness["ready_discriminator_count"] == 0:
        reason_codes.append("NO_DISCRIMINATOR_READY_FOR_RULE_REFINEMENT")
    if packet["total_missing_field_count"] > 0:
        reason_codes.append("SOURCE_BRIDGE_REQUIRED_FOR_TYPED_METADATA_COMPLETION")

    if packet["total_missing_field_count"] == 0 and readiness["ready_discriminator_count"] > 0:
        status = "TYPED_VALUE_SOURCE_METADATA_POPULATED_READY_FOR_DISCRIMINATOR_EVALUATION"
        next_edge = "EVALUATE_TYPED_VALUE_SOURCE_DISCRIMINATORS_V0"
    elif packet["total_populated_field_count"] > 0:
        status = "TYPED_VALUE_SOURCE_METADATA_PARTIALLY_POPULATED_STILL_INSUFFICIENT"
        next_edge = "BUILD_TYPED_VALUE_SOURCE_METADATA_SOURCE_BRIDGE_V0"
    else:
        status = "TYPED_VALUE_SOURCE_METADATA_NOT_POPULATED_NO_EXPLICIT_SOURCE"
        next_edge = "REQUEST_TYPED_VALUE_SOURCE_METADATA_POPULATION_INPUTS_V0"

    return status, reason_codes, next_edge

def classification_obj(status: str, reason_codes: List[str], next_edge: str, packet: Dict[str, Any], coverage: Dict[str, Any], readiness: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_population_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "row_count": packet["row_count"],
        "total_required_field_count": packet["total_required_field_count"],
        "total_populated_field_count": packet["total_populated_field_count"],
        "total_missing_field_count": packet["total_missing_field_count"],
        "coverage_ratio": coverage["coverage_ratio"],
        "ready_discriminator_count": readiness["ready_discriminator_count"],
        "metadata_populated": packet["total_populated_field_count"] > 0,
        "metadata_fully_populated": packet["total_missing_field_count"] == 0,
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
        "schema_version": "typed_value_source_metadata_population_authority_boundary_v0",
        "status": status,
        "may_extract_explicit_metadata": True,
        "may_populate_metadata_from_explicit_basis": True,
        "may_classify_population_gaps": True,
        "may_emit_source_bridge_recommendation": True,
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

def rollup_obj(status: str, packet: Dict[str, Any], coverage: Dict[str, Any], readiness: Dict[str, Any], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_population_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "row_count": packet["row_count"],
        "total_required_field_count": packet["total_required_field_count"],
        "total_populated_field_count": packet["total_populated_field_count"],
        "total_missing_field_count": packet["total_missing_field_count"],
        "coverage_ratio": coverage["coverage_ratio"],
        "ready_discriminator_count": readiness["ready_discriminator_count"],
        "metadata_population_packet_emitted_count": 1,
        "metadata_populated_count": 1 if packet["total_populated_field_count"] > 0 else 0,
        "metadata_fully_populated_count": 1 if packet["total_missing_field_count"] == 0 else 0,
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
        "schema_version": "typed_value_source_metadata_population_profile_v0",
        "profile_id": "metadata_population_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "metadata_population_packet_emitted": True,
        "metadata_populated": roll["metadata_populated_count"] == 1,
        "metadata_fully_populated": roll["metadata_fully_populated_count"] == 1,
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

def report_obj(status: str, reason_codes: List[str], packet: Dict[str, Any], coverage: Dict[str, Any], readiness: Dict[str, Any], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_population_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Metadata surface existed but needed population; this unit only extracts explicit metadata and classifies remaining gaps.",
        "row_count": packet["row_count"],
        "total_required_field_count": packet["total_required_field_count"],
        "total_populated_field_count": packet["total_populated_field_count"],
        "total_missing_field_count": packet["total_missing_field_count"],
        "coverage_ratio": coverage["coverage_ratio"],
        "fully_missing_field_count": coverage["fully_missing_field_count"],
        "ready_discriminator_count": readiness["ready_discriminator_count"],
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
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
        "schema_version": "typed_value_source_metadata_population_transition_trace_v0",
        "trace": [
            {
                "step": "consume_metadata_surface",
                "question": "what was missing",
                "answer": "typed value-source metadata surface existed but was not populated",
                "taken": "extract explicitly derivable row metadata only",
            },
            {
                "step": "classify_population_coverage",
                "question": "is metadata now sufficient for lawful discriminator use",
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

    if failures:
        packet = {
            "schema_version": "typed_value_source_metadata_population_packet_v0",
            "packet_id": "metadata_population_source_fail_" + sha8(failures),
            "packet_status": "TYPED_VALUE_SOURCE_METADATA_POPULATION_SOURCE_BASIS_FAIL",
            "row_count": 0,
            "required_fields_per_row": CORE_METADATA_FIELDS,
            "total_required_field_count": 0,
            "total_populated_field_count": 0,
            "total_missing_field_count": 0,
            "populated_rows": [],
            "target_candidate_declared_for_review": False,
            "target_selected_for_build": False,
            "accepted_for_build": False,
            "runtime_patch_authorized": False,
            "target_file_modification_authorized": False,
            "c5_authorized": False,
            "general_cell1_authority_granted": False,
            "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        }
        coverage = {
            "schema_version": "typed_value_source_metadata_population_coverage_v0",
            "coverage_status": "SOURCE_BASIS_FAIL",
            "row_count": 0,
            "total_required_field_count": 0,
            "total_populated_field_count": 0,
            "total_missing_field_count": 0,
            "field_coverage": {},
            "fully_populated_field_count": 0,
            "fully_populated_fields": [],
            "fully_missing_field_count": 0,
            "fully_missing_fields": [],
            "coverage_ratio": 0,
        }
        readiness = {
            "schema_version": "typed_value_source_discriminator_readiness_v0",
            "readiness_status": "SOURCE_BASIS_FAIL",
            "candidate_discriminator_count": 0,
            "ready_discriminator_count": 0,
            "discriminator_readiness": [],
            "recommended_next": "REPAIR_TYPED_VALUE_SOURCE_METADATA_POPULATION_BASIS_V0",
        }
        status = "TYPED_VALUE_SOURCE_METADATA_POPULATION_SOURCE_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_TYPED_VALUE_SOURCE_METADATA_POPULATION_BASIS_V0"
    else:
        rows = row_templates()
        discriminators = source_discriminators()
        packet = build_population_packet(rows)
        populated_surface = build_populated_surface(packet, discriminators)
        coverage = coverage_obj(packet)
        readiness = discriminator_readiness_obj(packet, coverage, discriminators)
        gaps = gaps_obj(packet, coverage, readiness)
        status, reason_codes, next_edge = classify(packet, coverage, readiness)

        write_json(POPULATED_SURFACE_PATH, populated_surface)
        write_json(POPULATION_GAPS_PATH, gaps)

    # If source basis failed, still emit compatible empty populated surface/gaps.
    if failures:
        write_json(POPULATED_SURFACE_PATH, {
            "schema_version": "typed_value_source_metadata_populated_surface_v0",
            "surface_status": "SOURCE_BASIS_FAIL",
            "source_surface_ref": rel(SOURCE_METADATA_SURFACE_PATH),
            "population_packet_ref": rel(POPULATION_PACKET_PATH),
            "row_count": 0,
            "total_required_field_count": 0,
            "total_populated_field_count": 0,
            "total_missing_field_count": 0,
            "real_tie_proven": False,
            "metadata_populated": False,
            "metadata_fully_populated": False,
            "rule_refined": False,
            "tie_broken": False,
            "candidate_values_filled": False,
            "recommended_next": next_edge,
            "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        })
        write_json(POPULATION_GAPS_PATH, {
            "schema_version": "typed_value_source_metadata_population_gaps_v0",
            "gap_status": "SOURCE_BASIS_FAIL",
            "gap_count": len(failures),
            "gaps": failures,
            "ready_discriminator_count": 0,
            "recommended_next": next_edge,
        })

    classif = classification_obj(status, reason_codes, next_edge, packet, coverage, readiness)
    boundary = authority_boundary_obj(status)
    roll = rollup_obj(status, packet, coverage, readiness, next_edge)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, packet, coverage, readiness, next_edge)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    write_json(POPULATION_PACKET_PATH, packet)
    write_json(POPULATION_COVERAGE_PATH, coverage)
    write_json(DISCRIMINATOR_READINESS_PATH, readiness)
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
        "METADATA_POPULATION_0_SURFACE_RECEIPT_CONSUMED": SOURCE_METADATA_SURFACE_RECEIPT_PATH.exists(),
        "METADATA_POPULATION_1_SURFACE_CONSUMED": SOURCE_METADATA_SURFACE_PATH.exists(),
        "METADATA_POPULATION_2_TEMPLATE_CONSUMED": SOURCE_ROW_METADATA_TEMPLATE_PATH.exists(),
        "METADATA_POPULATION_3_EXTRACTION_REQUEST_CONSUMED": SOURCE_METADATA_EXTRACTION_REQUEST_PATH.exists(),
        "METADATA_POPULATION_4_POPULATION_PACKET_EMITTED": POPULATION_PACKET_PATH.exists(),
        "METADATA_POPULATION_5_POPULATED_SURFACE_EMITTED": POPULATED_SURFACE_PATH.exists(),
        "METADATA_POPULATION_6_COVERAGE_EMITTED": POPULATION_COVERAGE_PATH.exists(),
        "METADATA_POPULATION_7_DISCRIMINATOR_READINESS_EMITTED": DISCRIMINATOR_READINESS_PATH.exists(),
        "METADATA_POPULATION_8_GAPS_EMITTED": POPULATION_GAPS_PATH.exists(),
        "METADATA_POPULATION_9_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "METADATA_POPULATION_10_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "METADATA_POPULATION_11_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "METADATA_POPULATION_12_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classif["target_candidate_declared_for_review"] is False,
        "METADATA_POPULATION_13_NO_TARGET_SELECTED_FOR_BUILD": classif["target_selected_for_build"] is False,
        "METADATA_POPULATION_14_NO_ACCEPTED_FOR_BUILD": classif["accepted_for_build"] is False,
        "METADATA_POPULATION_15_NO_RUNTIME_PATCH": classif["runtime_patch_authorized"] is False,
        "METADATA_POPULATION_16_NO_TARGET_FILE_MODIFICATION": classif["target_file_modification_authorized"] is False,
        "METADATA_POPULATION_17_NO_C5_OPENED": classif["c5_authorized"] is False,
        "METADATA_POPULATION_18_NO_GENERAL_CELL1_AUTHORITY": classif["general_cell1_authority_granted"] is False,
        "METADATA_POPULATION_19_NO_LATEST_FILE_GUESSING": classif["latest_file_guessing"] is False,
        "METADATA_POPULATION_20_NO_MTIME_SELECTION": classif["mtime_selection"] is False,
        "METADATA_POPULATION_21_NO_HIDDEN_NEXT_COMMAND": classif["next_command_goal"] is None,
        "METADATA_POPULATION_22_ACCEPTANCE_BOUNDARY_RETAINED": classif["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "METADATA_POPULATION_23_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_VALUE_SOURCE_METADATA_POPULATION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "population": packet.get("packet_id"),
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_value_source_metadata_population_receipt_v0",
        "receipt_type": "TYPED_VALUE_SOURCE_METADATA_POPULATION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_metadata_surface_receipt_id": SOURCE_METADATA_SURFACE_RECEIPT_ID,
        "typed_metadata_population_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "row_count": packet["row_count"],
            "total_required_field_count": packet["total_required_field_count"],
            "total_populated_field_count": packet["total_populated_field_count"],
            "total_missing_field_count": packet["total_missing_field_count"],
            "coverage_ratio": coverage["coverage_ratio"],
            "fully_missing_field_count": coverage["fully_missing_field_count"],
            "ready_discriminator_count": readiness["ready_discriminator_count"],
            "metadata_populated": packet["total_populated_field_count"] > 0,
            "metadata_fully_populated": packet["total_missing_field_count"] == 0,
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
            "population_packet": rel(POPULATION_PACKET_PATH),
            "populated_surface": rel(POPULATED_SURFACE_PATH),
            "population_coverage": rel(POPULATION_COVERAGE_PATH),
            "discriminator_readiness": rel(DISCRIMINATOR_READINESS_PATH),
            "population_gaps": rel(POPULATION_GAPS_PATH),
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
    print(f"metadata_population_receipt_id={receipt_id}")
    print(f"metadata_population_receipt_path={rel(receipt_path)}")
    print(f"metadata_population_packet_path={rel(POPULATION_PACKET_PATH)}")
    print(f"metadata_populated_surface_path={rel(POPULATED_SURFACE_PATH)}")
    print(f"metadata_population_coverage_path={rel(POPULATION_COVERAGE_PATH)}")
    print(f"discriminator_readiness_path={rel(DISCRIMINATOR_READINESS_PATH)}")
    print(f"metadata_population_gaps_path={rel(POPULATION_GAPS_PATH)}")
    print(f"metadata_population_classification_path={rel(CLASSIFICATION_PATH)}")
    print(f"metadata_population_rollup_path={rel(ROLLUP_PATH)}")
    print(f"metadata_population_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
