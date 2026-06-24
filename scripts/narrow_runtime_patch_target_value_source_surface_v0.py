#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shlex
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "NARROW_RUNTIME_PATCH_TARGET_VALUE_SOURCE_SURFACE_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_surface_narrowing.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_SURFACE_NARROWING"
MODE = "NARROW_TYPED_ROWS / DOMINANCE_CHECK / NO_ACCEPTANCE"
BUILD_MODE = "VALUE_SOURCE_SURFACE_NARROWING_ONLY"

SOURCE_VALUE_SOURCE_REPAIR_RECEIPT_ID = "6ca7147e"
SOURCE_VALUE_SOURCE_REPAIR_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_values_proposer_input_repair_v0_receipts/6ca7147e.json"
SOURCE_VALUE_SOURCE_SURFACE_MAP_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_values_proposer_input_repair_v0/runtime_patch_target_value_source_surface_map_v0.json"
SOURCE_VALUE_SOURCE_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_values_proposer_input_repair_v0/runtime_patch_target_value_source_surface_classification_v0.json"
SOURCE_VALUE_SOURCE_RECOMMENDATION_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_values_proposer_input_repair_v0/runtime_patch_target_value_source_bridge_repair_recommendation_v0.json"

SOURCE_VALUES_PROPOSER_RECEIPT_ID = "85d2d8e3"
SOURCE_VALUES_PROPOSER_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_values_proposer_v0_receipts/85d2d8e3.json"
SOURCE_VALUES_PROPOSAL_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_values_proposer_v0/runtime_patch_target_evidence_values_proposal_v0.json"
SOURCE_OPERATOR_VALUES_RECEIPT_ID = "1ac0b44d"
SOURCE_OPERATOR_VALUES_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_operator_values_v0_receipts/1ac0b44d.json"
SOURCE_INPUT_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_input_request_v0/explicit_runtime_patch_target_evidence_input_contract_v0.json"
SOURCE_HINT_INVENTORY_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_request_v0/target_hint_inventory_v0.json"
SOURCE_REQUEST_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_request_v0/narrower_runtime_patch_target_evidence_request_packet_v0.json"
SOURCE_SCHEMA_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_request_v0/runtime_patch_target_evidence_packet_schema_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_surface_narrowing_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_surface_narrowing_v0_receipts"

NARROWING_TABLE_PATH = OUT_DIR / "runtime_patch_target_value_source_narrowing_table_v0.json"
DOMINANCE_CLASSIFICATION_PATH = OUT_DIR / "runtime_patch_target_value_source_dominance_classification_v0.json"
NARROWED_VALUES_PROPOSAL_PATH = OUT_DIR / "runtime_patch_target_value_source_narrowed_values_proposal_v0.json"
NARROWED_ENV_EXPORTS_PATH = OUT_DIR / "runtime_patch_target_value_source_narrowed_env_exports.sh"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "runtime_patch_target_value_source_narrowing_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_patch_target_value_source_narrowing_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_patch_target_value_source_narrowing_profile_v0.json"
REPORT_PATH = OUT_DIR / "runtime_patch_target_value_source_narrowing_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "runtime_patch_target_value_source_narrowing_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_VALUE_SOURCE_REPAIR_RECEIPT_PATH,
    SOURCE_VALUE_SOURCE_SURFACE_MAP_PATH,
    SOURCE_VALUE_SOURCE_CLASSIFICATION_PATH,
    SOURCE_VALUE_SOURCE_RECOMMENDATION_PATH,
    SOURCE_VALUES_PROPOSER_RECEIPT_PATH,
    SOURCE_VALUES_PROPOSAL_PATH,
    SOURCE_OPERATOR_VALUES_RECEIPT_PATH,
    SOURCE_INPUT_CONTRACT_PATH,
    SOURCE_HINT_INVENTORY_PATH,
    SOURCE_REQUEST_PACKET_PATH,
    SOURCE_SCHEMA_PATH,
]

REQUIRED_ENV_FIELDS = [
    "SELECTED_TARGET_REF",
    "SELECTED_TARGET_KIND",
    "WHY_THIS_TARGET_IS_LOAD_BEARING",
    "WHY_OTHER_HINTS_ARE_NOT_TARGETS_JSON",
    "SOURCE_EVIDENCE_REFS_JSON",
    "VERIFICATION_GATE_REF",
    "ROLLBACK_OR_STOP_BOUNDARY_REF",
]

PRIMARY_VALUE_SURFACES = {
    "data/cell1_runtime_patch_target_evidence_request_v0/target_hint_inventory_v0.json",
    "data/cell1_runtime_patch_target_evidence_request_v0/narrower_runtime_patch_target_evidence_request_packet_v0.json",
}

META_SURFACE_FRAGMENTS = [
    "_receipt",
    "_report",
    "_rollup",
    "_profile",
    "_classification",
    "_authority_boundary",
    "_recommendation",
    "_proposal",
    "_schema",
    "provider_materialization",
    "operator_values",
]

NON_TARGET_PATH_FRAGMENTS = [
    "output_artifacts",
    "implementation_receipt",
    "source_",
    "receipt_id",
    "recommended_next",
    "terminal",
    "stop_code",
    "reason_codes",
    "failures",
    "warnings",
    "created_at",
    "classification_status",
    "schema_version",
    "packet_object_type",
    "required_env_fields",
    "acceptance_boundary",
    "authority",
    "rollup",
    "profile",
    "report",
    "transition_trace",
    "semantic_hits",
    "path_like_values",
]

TARGET_POSITIVE_FRAGMENTS = [
    "target",
    "candidate",
    "runtime_patch_target",
    "selected_target",
    "target_ref",
    "candidate_ref",
]

VERIFICATION_FRAGMENTS = ["verification", "gate"]
ROLLBACK_FRAGMENTS = ["rollback", "stop_boundary", "rollback_or_stop", "boundary"]

PATH_LIKE_RE = re.compile(r"^[A-Za-z0-9_./:-]+$")

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

def safe_local_bounded_path(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    if "EDIT_ME" in value or "FILL_ME" in value:
        return False
    if value.startswith("exact/"):
        return False
    p = Path(value)
    if p.is_absolute():
        return False
    if ".." in p.parts:
        return False
    if value.startswith(".git/"):
        return False
    if len(value) > 500:
        return False
    if not PATH_LIKE_RE.match(value):
        return False
    return "/" in value or value.endswith((".json", ".jsonl", ".txt", ".csv", ".py", ".md"))

def walk(obj: Any, path: str = ""):
    yield path, obj
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, f"{path}.{k}" if path else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f"{path}[{i}]")

def validate_source_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    repair = read_json(SOURCE_VALUE_SOURCE_REPAIR_RECEIPT_PATH)
    surface_class = read_json(SOURCE_VALUE_SOURCE_CLASSIFICATION_PATH)
    surface_map = read_json(SOURCE_VALUE_SOURCE_SURFACE_MAP_PATH)
    proposer = read_json(SOURCE_VALUES_PROPOSER_RECEIPT_PATH)
    operator_values = read_json(SOURCE_OPERATOR_VALUES_RECEIPT_PATH)
    input_contract = read_json(SOURCE_INPUT_CONTRACT_PATH)

    if repair.get("receipt_id") != SOURCE_VALUE_SOURCE_REPAIR_RECEIPT_ID or repair.get("gate") != "PASS":
        failures.append("value_source_repair_receipt_not_pass")
    if repair.get("value_source_surface_summary", {}).get("status") != "VALUE_SOURCE_SURFACE_MULTIPLE_AMBIGUOUS":
        failures.append("value_source_surface_not_multiple_ambiguous")
    if repair.get("terminal", {}).get("stop_code") != "STOP_VALUE_SOURCE_SURFACE_MULTIPLE_AMBIGUOUS":
        failures.append("value_source_repair_wrong_terminal")
    if surface_class.get("classification_status") != "VALUE_SOURCE_SURFACE_MULTIPLE_AMBIGUOUS":
        failures.append("source_surface_classification_not_multiple_ambiguous")
    if surface_map.get("typed_value_source_row_count", 0) <= 1:
        failures.append("surface_map_not_ambiguous_enough")
    if proposer.get("values_proposer_summary", {}).get("status") != "NO_BOUNDED_TARGET_VALUE_SOURCE":
        failures.append("values_proposer_source_status_wrong")
    if operator_values.get("operator_values_summary", {}).get("status") != "OPERATOR_TARGET_EVIDENCE_VALUES_MISSING_OR_INVALID":
        failures.append("operator_values_source_status_wrong")
    if input_contract.get("required_env_fields") != REQUIRED_ENV_FIELDS:
        failures.append("input_contract_required_fields_changed")
    if input_contract.get("target_selected_for_build") is not False:
        failures.append("input_contract_selects_target_for_build")
    if input_contract.get("runtime_patch_authorized") is not False:
        failures.append("input_contract_authorizes_runtime_patch")
    return failures

def classify_row(row: Dict[str, Any]) -> Dict[str, Any]:
    source_ref = str(row.get("source_ref", ""))
    json_path = str(row.get("json_path", ""))
    value = str(row.get("value", ""))
    source_lower = source_ref.lower()
    path_lower = json_path.lower()
    value_lower = value.lower()

    rejection_reasons: List[str] = []
    positive_reasons: List[str] = []
    role = "unknown"

    is_primary_surface = source_ref in PRIMARY_VALUE_SURFACES
    if is_primary_surface:
        positive_reasons.append("PRIMARY_VALUE_SURFACE")
    else:
        rejection_reasons.append("NOT_PRIMARY_VALUE_SURFACE")

    if any(fragment in source_lower for fragment in META_SURFACE_FRAGMENTS):
        rejection_reasons.append("META_OR_DERIVED_SURFACE")

    if any(fragment in path_lower for fragment in NON_TARGET_PATH_FRAGMENTS):
        rejection_reasons.append("NON_TARGET_METADATA_PATH")

    if any(fragment in path_lower for fragment in VERIFICATION_FRAGMENTS):
        role = "verification_gate_candidate"
    if any(fragment in path_lower for fragment in ROLLBACK_FRAGMENTS):
        role = "rollback_or_stop_boundary_candidate"

    has_target_semantics = any(fragment in path_lower or fragment in value_lower for fragment in TARGET_POSITIVE_FRAGMENTS)
    has_ref_semantics = ("ref" in path_lower or "path" in path_lower or value.endswith((".json", ".jsonl", ".py", ".txt", ".csv", ".md")))

    if has_target_semantics:
        positive_reasons.append("TARGET_SEMANTIC_MARKER")
    else:
        rejection_reasons.append("NO_TARGET_SEMANTIC_MARKER")

    if has_ref_semantics:
        positive_reasons.append("REF_OR_PATH_MARKER")
    else:
        rejection_reasons.append("NO_REF_OR_PATH_MARKER")

    if role == "unknown" and has_target_semantics and has_ref_semantics:
        role = "selected_target_ref_candidate"

    if role in {"verification_gate_candidate", "rollback_or_stop_boundary_candidate"}:
        rejection_reasons.append("SUPPORTING_FIELD_NOT_SELECTED_TARGET_REF")

    if not safe_local_bounded_path(value):
        rejection_reasons.append("VALUE_NOT_SAFE_LOCAL_BOUNDED_PATH")

    eligible_selected_target_ref = (
        role == "selected_target_ref_candidate"
        and is_primary_surface
        and safe_local_bounded_path(value)
        and "META_OR_DERIVED_SURFACE" not in rejection_reasons
        and "NON_TARGET_METADATA_PATH" not in rejection_reasons
        and "SUPPORTING_FIELD_NOT_SELECTED_TARGET_REF" not in rejection_reasons
    )

    dominance_score = 0
    if eligible_selected_target_ref:
        dominance_score += 10
    if source_ref == "data/cell1_runtime_patch_target_evidence_request_v0/target_hint_inventory_v0.json":
        dominance_score += 5
    if "explicit" in path_lower or "dominant" in path_lower or "selected" in path_lower:
        dominance_score += 3
    if "target" in path_lower and "ref" in path_lower:
        dominance_score += 3
    if "candidate" in path_lower:
        dominance_score += 2
    if value.endswith(".json"):
        dominance_score += 1

    return {
        "source_ref": source_ref,
        "json_path": json_path,
        "value": value,
        "source_kind": "primary_value_surface" if is_primary_surface else "meta_or_support_surface",
        "role": role,
        "eligible_selected_target_ref": eligible_selected_target_ref,
        "dominance_score": dominance_score,
        "positive_reasons": positive_reasons,
        "rejection_reasons": rejection_reasons,
        "source_semantic_score": row.get("semantic_score"),
    }

def find_supporting_ref(surface_rows: List[Dict[str, Any]], role: str) -> str | None:
    candidates = [r for r in surface_rows if r["role"] == role and safe_local_bounded_path(r["value"])]
    primary = [r for r in candidates if r["source_ref"] in PRIMARY_VALUE_SURFACES]
    rows = primary or candidates
    if len(rows) == 1:
        return rows[0]["value"]
    return None

def build_narrowing() -> Tuple[str, List[str], Dict[str, Any], Dict[str, Any]]:
    surface_map = read_json(SOURCE_VALUE_SOURCE_SURFACE_MAP_PATH)
    typed_rows = surface_map.get("typed_value_source_rows", [])
    if not isinstance(typed_rows, list):
        typed_rows = []

    classified = [classify_row(row) for row in typed_rows if isinstance(row, dict)]

    eligible = [r for r in classified if r["eligible_selected_target_ref"]]
    max_score = max([r["dominance_score"] for r in eligible], default=0)
    top = [r for r in eligible if r["dominance_score"] == max_score] if eligible else []

    verification_gate_ref = find_supporting_ref(classified, "verification_gate_candidate")
    rollback_or_stop_boundary_ref = find_supporting_ref(classified, "rollback_or_stop_boundary_candidate")

    reason_codes: List[str] = []
    status = ""

    if not eligible:
        status = "NO_ELIGIBLE_SELECTED_TARGET_VALUE_SOURCE_ROW"
        reason_codes.append("NO_ROW_SURVIVED_PRIMARY_TARGET_REF_FILTER")
    elif len(top) == 1:
        if not verification_gate_ref:
            status = "MISSING_UNIQUE_VERIFICATION_GATE_REF"
            reason_codes.append("MISSING_UNIQUE_VERIFICATION_GATE_REF")
        elif not rollback_or_stop_boundary_ref:
            status = "MISSING_UNIQUE_ROLLBACK_OR_STOP_BOUNDARY_REF"
            reason_codes.append("MISSING_UNIQUE_ROLLBACK_OR_STOP_BOUNDARY_REF")
        else:
            status = "VALUE_SOURCE_SURFACE_NARROWED_ONE_DOMINANT_ROW"
            reason_codes.append("ONE_DOMINANT_SELECTED_TARGET_VALUE_SOURCE_ROW")
    else:
        status = "VALUE_SOURCE_SURFACE_STILL_MULTIPLE_AMBIGUOUS"
        reason_codes.append("MULTIPLE_ELIGIBLE_SELECTED_TARGET_VALUE_SOURCE_ROWS_WITH_EQUAL_DOMINANCE")

    if len(eligible) > 1 and status != "VALUE_SOURCE_SURFACE_NARROWED_ONE_DOMINANT_ROW":
        reason_codes.append("NO_SINGLE_DOMINANT_VALUE_SOURCE")
    if not verification_gate_ref:
        reason_codes.append("SUPPORTING_VERIFICATION_GATE_REF_NOT_UNIQUE")
    if not rollback_or_stop_boundary_ref:
        reason_codes.append("SUPPORTING_ROLLBACK_OR_STOP_BOUNDARY_REF_NOT_UNIQUE")

    selected = top[0] if status == "VALUE_SOURCE_SURFACE_NARROWED_ONE_DOMINANT_ROW" else None

    values: Dict[str, Any] = {}
    if selected:
        rejected = []
        for row in classified:
            if row["value"] == selected["value"] and row["json_path"] == selected["json_path"] and row["source_ref"] == selected["source_ref"]:
                continue
            if row["role"] == "selected_target_ref_candidate" or row["eligible_selected_target_ref"]:
                rejected.append({
                    "source_ref": row["source_ref"],
                    "json_path": row["json_path"],
                    "value": row["value"],
                    "role": row["role"],
                    "rejection_reasons": row["rejection_reasons"] or ["lower_dominance_or_not_primary_selected_target_ref_source"],
                    "dominance_score": row["dominance_score"],
                })

        values = {
            "SELECTED_TARGET_REF": selected["value"],
            "SELECTED_TARGET_KIND": "runtime_patch_target",
            "WHY_THIS_TARGET_IS_LOAD_BEARING": (
                "Proposed by value-source surface narrowing because exactly one primary selected-target-ref row survived "
                "the bounded dominance filter. This is a proposal only; human or prevalidated-schema acceptance is still required."
            ),
            "WHY_OTHER_HINTS_ARE_NOT_TARGETS_JSON": json.dumps(rejected),
            "SOURCE_EVIDENCE_REFS_JSON": json.dumps([
                rel(SOURCE_VALUE_SOURCE_REPAIR_RECEIPT_PATH),
                rel(SOURCE_VALUE_SOURCE_SURFACE_MAP_PATH),
                rel(SOURCE_HINT_INVENTORY_PATH),
                rel(SOURCE_REQUEST_PACKET_PATH),
                rel(SOURCE_INPUT_CONTRACT_PATH),
            ]),
            "VERIFICATION_GATE_REF": verification_gate_ref,
            "ROLLBACK_OR_STOP_BOUNDARY_REF": rollback_or_stop_boundary_ref,
        }

    table = {
        "schema_version": "runtime_patch_target_value_source_narrowing_table_v0",
        "narrowing_table_id": "value_source_narrowing_" + sha8({
            "status": status,
            "eligible_count": len(eligible),
            "top_count": len(top),
        }),
        "source_surface_map_ref": rel(SOURCE_VALUE_SOURCE_SURFACE_MAP_PATH),
        "status": status,
        "reason_codes": reason_codes,
        "typed_row_count": len(classified),
        "eligible_selected_target_ref_row_count": len(eligible),
        "top_dominance_score": max_score,
        "top_dominant_row_count": len(top),
        "verification_gate_ref": verification_gate_ref,
        "rollback_or_stop_boundary_ref": rollback_or_stop_boundary_ref,
        "dominant_row": selected,
        "eligible_rows": sorted(eligible, key=lambda r: (-r["dominance_score"], r["source_ref"], r["json_path"], r["value"]))[:100],
        "classified_rows": sorted(classified, key=lambda r: (-r["dominance_score"], r["source_ref"], r["json_path"], r["value"]))[:300],
    }

    return status, reason_codes, values, table

def write_env_exports(values: Dict[str, Any]) -> None:
    lines = [
        "# Narrowed value-source proposal only.",
        "# Human or prevalidated-schema acceptance boundary still applies.",
        "# Source this only to test existing intake/provider path; it does not select for build or authorize patching.",
    ]
    for field in REQUIRED_ENV_FIELDS:
        lines.append(f"export {field}={shlex.quote(str(values[field]))}")
    lines.append("")
    NARROWED_ENV_EXPORTS_PATH.write_text("\n".join(lines))

def next_for_status(status: str) -> str:
    if status == "VALUE_SOURCE_SURFACE_NARROWED_ONE_DOMINANT_ROW":
        return "REVIEW_RUNTIME_PATCH_TARGET_VALUE_SOURCE_NARROWING_PROPOSAL_V0"
    if status == "VALUE_SOURCE_SURFACE_STILL_MULTIPLE_AMBIGUOUS":
        return "ADD_EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_V0"
    if status == "NO_ELIGIBLE_SELECTED_TARGET_VALUE_SOURCE_ROW":
        return "TYPE_RUNTIME_PATCH_TARGET_HINT_INVENTORY_AS_VALUE_SOURCE_V0"
    if status == "MISSING_UNIQUE_VERIFICATION_GATE_REF":
        return "NARROW_RUNTIME_PATCH_TARGET_VERIFICATION_GATE_REF_V0"
    if status == "MISSING_UNIQUE_ROLLBACK_OR_STOP_BOUNDARY_REF":
        return "NARROW_RUNTIME_PATCH_TARGET_ROLLBACK_OR_STOP_BOUNDARY_REF_V0"
    return "REPAIR_VALUE_SOURCE_SURFACE_NARROWING_V0"

def stop_code_for_status(status: str) -> str:
    return "STOP_" + status

def dominance_classification(status: str, reason_codes: List[str], values: Dict[str, Any], table: Dict[str, Any]) -> Dict[str, Any]:
    ready = status == "VALUE_SOURCE_SURFACE_NARROWED_ONE_DOMINANT_ROW"
    return {
        "schema_version": "runtime_patch_target_value_source_dominance_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "proposal_ready": ready,
        "candidate_values_filled_count": len(values) if ready else 0,
        "required_values_count": len(REQUIRED_ENV_FIELDS),
        "typed_row_count": table["typed_row_count"],
        "eligible_selected_target_ref_row_count": table["eligible_selected_target_ref_row_count"],
        "top_dominant_row_count": table["top_dominant_row_count"],
        "target_candidate_proposed_count": 1 if ready else 0,
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
        "recommended_next": next_for_status(status),
        "next_command_goal": None,
    }

def narrowed_values_proposal(status: str, reason_codes: List[str], values: Dict[str, Any], table: Dict[str, Any]) -> Dict[str, Any]:
    ready = status == "VALUE_SOURCE_SURFACE_NARROWED_ONE_DOMINANT_ROW"
    return {
        "schema_version": "runtime_patch_target_value_source_narrowed_values_proposal_v0",
        "proposal_type": "NARROWED_RUNTIME_PATCH_TARGET_EVIDENCE_VALUES_PROPOSAL",
        "proposal_id": "narrowed_values_" + sha8({"status": status, "values": values, "reason_codes": reason_codes}),
        "proposal_status": status,
        "reason_codes": reason_codes,
        "candidate_values": values if ready else {},
        "dominance_basis": {
            "source_surface_map_ref": rel(SOURCE_VALUE_SOURCE_SURFACE_MAP_PATH),
            "narrowing_table_ref": rel(NARROWING_TABLE_PATH),
            "dominant_row": table.get("dominant_row"),
            "eligible_selected_target_ref_row_count": table["eligible_selected_target_ref_row_count"],
            "top_dominant_row_count": table["top_dominant_row_count"],
        },
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "recommended_next": next_for_status(status),
    }

def authority_boundary(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "runtime_patch_target_value_source_narrowing_authority_boundary_v0",
        "status": status,
        "may_classify_typed_rows": True,
        "may_emit_narrowed_values_proposal_if_single_dominant_row": status == "VALUE_SOURCE_SURFACE_NARROWED_ONE_DOMINANT_ROW",
        "may_emit_env_exports_if_single_dominant_row": status == "VALUE_SOURCE_SURFACE_NARROWED_ONE_DOMINANT_ROW",
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
        "must_not_infer": [
            "dominant value-source row is accepted for build",
            "narrowed proposal declares candidate for review",
            "narrowed proposal authorizes patching",
            "ambiguity can be collapsed by preference"
        ],
    }

def rollup(status: str, table: Dict[str, Any]) -> Dict[str, Any]:
    ready = status == "VALUE_SOURCE_SURFACE_NARROWED_ONE_DOMINANT_ROW"
    return {
        "schema_version": "runtime_patch_target_value_source_narrowing_rollup_v0",
        "build_mode": BUILD_MODE,
        "surface_narrowing_status": status,
        "typed_row_count": table["typed_row_count"],
        "eligible_selected_target_ref_row_count": table["eligible_selected_target_ref_row_count"],
        "top_dominant_row_count": table["top_dominant_row_count"],
        "values_proposal_ready_count": 1 if ready else 0,
        "values_proposal_not_ready_count": 0 if ready else 1,
        "target_candidate_proposed_count": 1 if ready else 0,
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
        "recommended_next": next_for_status(status),
    }

def profile(status: str, roll: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "runtime_patch_target_value_source_narrowing_profile_v0",
        "profile_id": "value_source_narrowing_" + sha8({"status": status, "roll": roll}),
        "status": status,
        "proposal_ready": status == "VALUE_SOURCE_SURFACE_NARROWED_ONE_DOMINANT_ROW",
        "target_candidate_proposed": status == "VALUE_SOURCE_SURFACE_NARROWED_ONE_DOMINANT_ROW",
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": all(roll.get(k) == 0 for k in [
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
        ]),
        "recommended_next": roll["recommended_next"],
        "next_command_goal": None,
    }

def report(status: str, reason_codes: List[str], table: Dict[str, Any], roll: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "runtime_patch_target_value_source_narrowing_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "typed_row_count": table["typed_row_count"],
        "eligible_selected_target_ref_row_count": table["eligible_selected_target_ref_row_count"],
        "top_dominant_row_count": table["top_dominant_row_count"],
        "candidate_values_filled_count": 7 if status == "VALUE_SOURCE_SURFACE_NARROWED_ONE_DOMINANT_ROW" else 0,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "recommended_next_handling": roll["recommended_next"],
        "target_candidate_proposed_count": roll["target_candidate_proposed_count"],
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

def transition_trace(status: str, reason_codes: List[str]) -> Dict[str, Any]:
    return {
        "schema_version": "runtime_patch_target_value_source_narrowing_transition_trace_v0",
        "trace": [
            {
                "step": "consume_multiple_ambiguous_surface",
                "question": "is the source absent or overbroad",
                "answer": "overbroad source surface with multiple typed rows",
                "taken": "classify rows by provenance and role",
            },
            {
                "step": "dominance_check",
                "question": "does exactly one selected-target-ref row survive bounded dominance filters",
                "answer": status,
                "reason_codes": reason_codes,
                "taken": next_for_status(status),
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": stop_code_for_status(status),
            "next_command_goal": None,
        },
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        status = "VALUE_SOURCE_SURFACE_NARROWING_SOURCE_BASIS_FAIL"
        reason_codes = failures
        values: Dict[str, Any] = {}
        table = {
            "schema_version": "runtime_patch_target_value_source_narrowing_table_v0",
            "narrowing_table_id": "value_source_narrowing_source_fail_" + sha8(failures),
            "source_surface_map_ref": rel(SOURCE_VALUE_SOURCE_SURFACE_MAP_PATH),
            "status": status,
            "reason_codes": reason_codes,
            "typed_row_count": 0,
            "eligible_selected_target_ref_row_count": 0,
            "top_dominance_score": 0,
            "top_dominant_row_count": 0,
            "verification_gate_ref": None,
            "rollback_or_stop_boundary_ref": None,
            "dominant_row": None,
            "eligible_rows": [],
            "classified_rows": [],
        }
    else:
        status, reason_codes, values, table = build_narrowing()

    classif = dominance_classification(status, reason_codes, values, table)
    proposal = narrowed_values_proposal(status, reason_codes, values, table)
    boundary = authority_boundary(status)
    roll = rollup(status, table)
    prof = profile(status, roll)
    rep = report(status, reason_codes, table, roll)
    tr = transition_trace(status, reason_codes)

    write_json(NARROWING_TABLE_PATH, table)
    write_json(DOMINANCE_CLASSIFICATION_PATH, classif)
    write_json(NARROWED_VALUES_PROPOSAL_PATH, proposal)
    if status == "VALUE_SOURCE_SURFACE_NARROWED_ONE_DOMINANT_ROW":
        write_env_exports(values)
    elif NARROWED_ENV_EXPORTS_PATH.exists():
        NARROWED_ENV_EXPORTS_PATH.unlink()

    write_json(AUTHORITY_BOUNDARY_PATH, boundary)
    write_json(ROLLUP_PATH, roll)
    write_json(PROFILE_PATH, prof)
    write_json(REPORT_PATH, rep)
    write_json(TRANSITION_TRACE_PATH, tr)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        roll["source_mutation_count"] = 1
        rep["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, roll)
        write_json(REPORT_PATH, rep)

    acceptance_gate_results = {
        "VALUE_SOURCE_NARROWING_0_REPAIR_RECEIPT_CONSUMED": SOURCE_VALUE_SOURCE_REPAIR_RECEIPT_PATH.exists(),
        "VALUE_SOURCE_NARROWING_1_SURFACE_MAP_CONSUMED": SOURCE_VALUE_SOURCE_SURFACE_MAP_PATH.exists(),
        "VALUE_SOURCE_NARROWING_2_NARROWING_TABLE_EMITTED": NARROWING_TABLE_PATH.exists(),
        "VALUE_SOURCE_NARROWING_3_DOMINANCE_CLASSIFICATION_EMITTED": DOMINANCE_CLASSIFICATION_PATH.exists(),
        "VALUE_SOURCE_NARROWING_4_VALUES_PROPOSAL_EMITTED": NARROWED_VALUES_PROPOSAL_PATH.exists(),
        "VALUE_SOURCE_NARROWING_5_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classif["target_candidate_declared_for_review"] is False,
        "VALUE_SOURCE_NARROWING_6_NO_TARGET_SELECTED_FOR_BUILD": classif["target_selected_for_build"] is False,
        "VALUE_SOURCE_NARROWING_7_NO_ACCEPTED_FOR_BUILD": classif["accepted_for_build"] is False,
        "VALUE_SOURCE_NARROWING_8_NO_RUNTIME_PATCH": classif["runtime_patch_authorized"] is False,
        "VALUE_SOURCE_NARROWING_9_NO_TARGET_FILE_MODIFICATION": classif["target_file_modification_authorized"] is False,
        "VALUE_SOURCE_NARROWING_10_NO_C5_OPENED": classif["c5_authorized"] is False,
        "VALUE_SOURCE_NARROWING_11_NO_GENERAL_CELL1_AUTHORITY": classif["general_cell1_authority_granted"] is False,
        "VALUE_SOURCE_NARROWING_12_NO_LATEST_FILE_GUESSING": classif["latest_file_guessing"] is False,
        "VALUE_SOURCE_NARROWING_13_NO_MTIME_SELECTION": classif["mtime_selection"] is False,
        "VALUE_SOURCE_NARROWING_14_NO_HIDDEN_NEXT_COMMAND": classif["next_command_goal"] is None,
        "VALUE_SOURCE_NARROWING_15_ACCEPTANCE_BOUNDARY_RETAINED": classif["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "VALUE_SOURCE_NARROWING_16_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = tr["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_VALUE_SOURCE_SURFACE_NARROWING_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "reason_codes": reason_codes,
        "table_counts": {
            "typed": table["typed_row_count"],
            "eligible": table["eligible_selected_target_ref_row_count"],
            "top": table["top_dominant_row_count"],
        },
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "runtime_patch_target_value_source_surface_narrowing_receipt_v0",
        "receipt_type": "RUNTIME_PATCH_TARGET_VALUE_SOURCE_SURFACE_NARROWING_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_value_source_repair_receipt_id": SOURCE_VALUE_SOURCE_REPAIR_RECEIPT_ID,
        "source_values_proposer_receipt_id": SOURCE_VALUES_PROPOSER_RECEIPT_ID,
        "source_operator_values_receipt_id": SOURCE_OPERATOR_VALUES_RECEIPT_ID,
        "value_source_narrowing_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "typed_row_count": table["typed_row_count"],
            "eligible_selected_target_ref_row_count": table["eligible_selected_target_ref_row_count"],
            "top_dominant_row_count": table["top_dominant_row_count"],
            "proposal_ready": status == "VALUE_SOURCE_SURFACE_NARROWED_ONE_DOMINANT_ROW",
            "candidate_values_filled_count": len(values) if status == "VALUE_SOURCE_SURFACE_NARROWED_ONE_DOMINANT_ROW" else 0,
            "target_candidate_proposed": status == "VALUE_SOURCE_SURFACE_NARROWED_ONE_DOMINANT_ROW",
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
            "recommended_next": roll["recommended_next"],
        },
        "aggregate_metrics": rep,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "narrowing_table": rel(NARROWING_TABLE_PATH),
            "dominance_classification": rel(DOMINANCE_CLASSIFICATION_PATH),
            "narrowed_values_proposal": rel(NARROWED_VALUES_PROPOSAL_PATH),
            "narrowed_env_exports": rel(NARROWED_ENV_EXPORTS_PATH) if NARROWED_ENV_EXPORTS_PATH.exists() else None,
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
    print(f"value_source_narrowing_receipt_id={receipt_id}")
    print(f"value_source_narrowing_receipt_path={rel(receipt_path)}")
    print(f"value_source_narrowing_table_path={rel(NARROWING_TABLE_PATH)}")
    print(f"value_source_dominance_classification_path={rel(DOMINANCE_CLASSIFICATION_PATH)}")
    print(f"value_source_narrowed_values_proposal_path={rel(NARROWED_VALUES_PROPOSAL_PATH)}")
    print(f"value_source_narrowed_env_exports_path={rel(NARROWED_ENV_EXPORTS_PATH) if NARROWED_ENV_EXPORTS_PATH.exists() else ''}")
    print(f"value_source_narrowing_rollup_path={rel(ROLLUP_PATH)}")
    print(f"value_source_narrowing_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
