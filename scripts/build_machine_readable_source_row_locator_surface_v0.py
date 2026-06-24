#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_MACHINE_READABLE_SOURCE_ROW_LOCATOR_SURFACE_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_row_locator.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_ROW_LOCATOR"
MODE = "SOURCE_ROW_LOCATOR / NO_REBIND_APPLIED / NO_RULE_APPLIED / NO_VALUE_AUTHORIZATION / NO_METADATA_FILL"
BUILD_MODE = "SOURCE_ROW_LOCATOR_SURFACE_ONLY"

SOURCE_DECISION_SURFACE_RECEIPT_ID = "7636e62c"
SOURCE_DECISION_SURFACE_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_decision_surface_v0_receipts/7636e62c.json"
SOURCE_DECISION_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_decision_surface_v0/typed_machine_readable_source_ref_decision_surface_v0.json"
SOURCE_DECISION_LESSON_GRAPH_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_decision_surface_v0/typed_machine_readable_source_ref_decision_lesson_graph_v0.json"
SOURCE_EVIDENCE_REQUIREMENTS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_decision_surface_v0/typed_machine_readable_source_ref_decision_evidence_requirements_v0.json"
SOURCE_DOMINANCE_RULE_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_decision_surface_v0/typed_machine_readable_source_ref_rebind_dominance_rule_surface_v0.json"
SOURCE_ROW_LOCATOR_SURFACE_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_decision_surface_v0/typed_machine_readable_source_row_locator_surface_v0.json"
SOURCE_PER_BINDING_DECISION_REQUIREMENTS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_decision_surface_v0/typed_machine_readable_per_binding_source_ref_decision_requirements_v0.json"
SOURCE_RESIDUAL_TIE_EXPLANATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_decision_surface_v0/typed_machine_readable_source_ref_residual_tie_explanation_v0.json"
SOURCE_BRANCH_DECISION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_decision_surface_v0/typed_machine_readable_source_ref_next_branch_decision_table_v0.json"
SOURCE_DECISION_NEXT_UNIT_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_decision_surface_v0/typed_machine_readable_source_ref_decision_next_unit_contract_v0.json"
SOURCE_DECISION_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_decision_surface_v0/typed_machine_readable_source_ref_decision_surface_classification_v0.json"
SOURCE_DECISION_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_decision_surface_v0/typed_machine_readable_source_ref_decision_surface_rollup_v0.json"
SOURCE_DECISION_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_decision_surface_v0/typed_machine_readable_source_ref_decision_surface_profile_v0.json"

SOURCE_DOMINANCE_FEATURE_MATRIX_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing_v0/typed_machine_readable_source_ref_rebind_dominance_feature_matrix_v0.json"
SOURCE_RESIDUAL_REBIND_TIE_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing_v0/typed_machine_readable_source_ref_rebind_residual_tie_table_v0.json"
SOURCE_CANDIDATE_SCORE_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_review_v0/typed_machine_readable_source_ref_rebind_candidate_score_table_v0.json"
SOURCE_BROKEN_BINDING_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_row_path_refinement_v0/typed_machine_readable_broken_row_binding_table_v0.json"
SOURCE_MACHINE_SOURCE_SLOTS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_machine_source_slots_v0.json"
SOURCE_FIELD_POLICY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_source_field_policy_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_row_locator_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_row_locator_v0_receipts"

ROW_LOCATOR_SURFACE_PATH = OUT_DIR / "typed_machine_readable_source_row_locator_surface_v0.json"
CANDIDATE_ARTIFACT_SCAN_PATH = OUT_DIR / "typed_machine_readable_source_row_locator_candidate_artifact_scan_v0.json"
ROW_IDENTITY_MATCH_TABLE_PATH = OUT_DIR / "typed_machine_readable_source_row_identity_match_table_v0.json"
SOURCE_OBJECT_STRUCTURE_TABLE_PATH = OUT_DIR / "typed_machine_readable_source_object_structure_table_v0.json"
SOURCE_LINEAGE_MARKER_TABLE_PATH = OUT_DIR / "typed_machine_readable_source_lineage_marker_table_v0.json"
PER_BINDING_LOCATOR_TABLE_PATH = OUT_DIR / "typed_machine_readable_per_binding_source_row_locator_v0.json"
UNIQUE_LOCATOR_PROPOSALS_PATH = OUT_DIR / "typed_machine_readable_unique_source_row_locator_proposals_v0.json"
LOCATOR_RESIDUAL_AMBIGUITY_TABLE_PATH = OUT_DIR / "typed_machine_readable_source_row_locator_residual_ambiguity_v0.json"
LOCATOR_DECISION_OPTIONS_PATH = OUT_DIR / "typed_machine_readable_source_row_locator_decision_options_v0.json"
NEXT_REBIND_REVIEW_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_source_row_locator_to_rebind_review_contract_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_source_row_locator_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_source_row_locator_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_source_row_locator_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_source_row_locator_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_source_row_locator_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_source_row_locator_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_DECISION_SURFACE_RECEIPT_PATH,
    SOURCE_DECISION_SURFACE_PATH,
    SOURCE_DECISION_LESSON_GRAPH_PATH,
    SOURCE_EVIDENCE_REQUIREMENTS_PATH,
    SOURCE_DOMINANCE_RULE_SURFACE_PATH,
    SOURCE_ROW_LOCATOR_SURFACE_CONTRACT_PATH,
    SOURCE_PER_BINDING_DECISION_REQUIREMENTS_PATH,
    SOURCE_RESIDUAL_TIE_EXPLANATION_PATH,
    SOURCE_BRANCH_DECISION_TABLE_PATH,
    SOURCE_DECISION_NEXT_UNIT_CONTRACT_PATH,
    SOURCE_DECISION_CLASSIFICATION_PATH,
    SOURCE_DECISION_ROLLUP_PATH,
    SOURCE_DECISION_PROFILE_PATH,
    SOURCE_DOMINANCE_FEATURE_MATRIX_PATH,
    SOURCE_RESIDUAL_REBIND_TIE_TABLE_PATH,
    SOURCE_CANDIDATE_SCORE_TABLE_PATH,
    SOURCE_BROKEN_BINDING_TABLE_PATH,
    SOURCE_MACHINE_SOURCE_SLOTS_PATH,
    SOURCE_FIELD_POLICY_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_SOURCE_REF_DECISION_SURFACE_BUILT_ROW_LOCATOR_REQUIRED"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_SOURCE_REF_DECISION_SURFACE_BUILT_ROW_LOCATOR_REQUIRED"
EXPECTED_NEXT = "BUILD_MACHINE_READABLE_SOURCE_ROW_LOCATOR_SURFACE_V0"

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

def source_path_from_ref(ref: Any) -> Path | None:
    if not isinstance(ref, str) or not ref.strip():
        return None
    p = Path(ref.strip())
    if not p.is_absolute():
        p = ROOT / p
    return p if p.exists() else None

def flatten_json(obj: Any, prefix: str = "$", out: List[Dict[str, Any]] | None = None, limit: int = 20000) -> List[Dict[str, Any]]:
    if out is None:
        out = []
    if len(out) >= limit:
        return out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if len(out) >= limit:
                break
            key = str(k)
            path = f"{prefix}.{key}" if prefix != "$" else f"$.{key}"
            out.append({"path": path, "key": key, "value": v, "type": type(v).__name__})
            if isinstance(v, (dict, list)):
                flatten_json(v, path, out, limit)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if len(out) >= limit:
                break
            path = f"{prefix}.{i}"
            out.append({"path": path, "key": str(i), "value": v, "type": type(v).__name__})
            if isinstance(v, (dict, list)):
                flatten_json(v, path, out, limit)
    return out

def container_path(path: str) -> str:
    return path.rsplit(".", 1)[0] if "." in path else "$"

def validate_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    receipt = read_json(SOURCE_DECISION_SURFACE_RECEIPT_PATH)
    summary = receipt.get("machine_readable_source_ref_decision_surface_summary", {})
    decision = read_json(SOURCE_DECISION_SURFACE_PATH)
    row_locator_contract = read_json(SOURCE_ROW_LOCATOR_SURFACE_CONTRACT_PATH)
    branch = read_json(SOURCE_BRANCH_DECISION_TABLE_PATH)
    classif = read_json(SOURCE_DECISION_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_DECISION_ROLLUP_PATH)
    profile = read_json(SOURCE_DECISION_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_DECISION_SURFACE_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("decision_surface_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"decision_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("decision_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"decision_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("selected_next_machine_surface") != EXPECTED_NEXT:
        failures.append("selected_next_machine_surface_not_row_locator")
    if summary.get("residual_tie_binding_count") != 21:
        failures.append("decision_residual_tie_count_not_21")
    if summary.get("decision_evidence_requirement_count") != 105:
        failures.append("decision_evidence_requirement_count_not_105")
    if summary.get("dominance_rule_applied") is not False:
        failures.append("dominance_rule_applied_unexpectedly")
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

    if decision.get("surface_status") != EXPECTED_SOURCE_STATUS:
        failures.append("decision_surface_status_wrong")
    if row_locator_contract.get("surface_status") != "SOURCE_ROW_LOCATOR_SURFACE_BUILT_AS_NEXT_MACHINE_SAFE_BRANCH":
        failures.append("row_locator_contract_status_wrong")
    records = branch.get("records", [])
    if not any(r.get("branch") == "SOURCE_ROW_LOCATOR_SURFACE" and r.get("safe_now") is True for r in records if isinstance(r, dict)):
        failures.append("branch_table_missing_safe_row_locator_branch")
    if not any(r.get("branch") == "DOMINANCE_RULE_AUTHORIZATION" and r.get("safe_now") is False for r in records if isinstance(r, dict)):
        failures.append("branch_table_missing_unsafe_dominance_rule_branch")
    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("decision_classification_status_wrong")
    if roll.get("metadata_populated_count") != 0:
        failures.append("decision_rollup_metadata_populated_nonzero")
    if profile.get("metadata_populated") is not False:
        failures.append("decision_profile_metadata_populated_true")

    return failures

def load_records() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    features = [r for r in read_json(SOURCE_DOMINANCE_FEATURE_MATRIX_PATH).get("records", []) if isinstance(r, dict)]
    residual_ties = [r for r in read_json(SOURCE_RESIDUAL_REBIND_TIE_TABLE_PATH).get("records", []) if isinstance(r, dict)]
    broken = {
        str(r.get("slot_id")): r
        for r in read_json(SOURCE_BROKEN_BINDING_TABLE_PATH).get("records", [])
        if isinstance(r, dict) and r.get("slot_id")
    }
    slots = {
        str(r.get("slot_id")): r
        for r in read_json(SOURCE_MACHINE_SOURCE_SLOTS_PATH).get("slots", [])
        if isinstance(r, dict) and r.get("slot_id")
    }
    policies = {}
    policy_obj = read_json(SOURCE_FIELD_POLICY_PATH)
    for key in ["field_policies", "records", "policies"]:
        for r in policy_obj.get(key, []):
            if isinstance(r, dict) and r.get("field"):
                policies[str(r["field"])] = r
    return features, residual_ties, broken, slots, policies

def norm(v: Any) -> str:
    return "" if v is None else str(v)

def is_scalar(v: Any) -> bool:
    return isinstance(v, (str, int, float, bool)) or v is None

def summarize_source(ref: str) -> Dict[str, Any]:
    p = source_path_from_ref(ref)
    out = {
        "candidate_source_ref": ref,
        "source_path_resolves": p is not None,
        "source_json_readable": False,
        "schema_version": None,
        "top_keys": [],
        "path_count": 0,
        "row_like_collection_paths": [],
        "producer_unit_candidates": [],
        "lineage_marker_paths": [],
    }
    if p is None:
        return out
    try:
        obj = read_json(p)
    except Exception:
        return out
    out["source_json_readable"] = True
    if isinstance(obj, dict):
        out["schema_version"] = obj.get("schema_version")
        out["top_keys"] = sorted([str(k) for k in obj.keys()])[:50]
    flat = flatten_json(obj)
    out["path_count"] = len(flat)
    for item in flat:
        key = str(item.get("key"))
        value = item.get("value")
        path = str(item.get("path"))
        if key in {"records", "rows", "slots", "field_policies", "propositions", "attempts"} and isinstance(value, list):
            out["row_like_collection_paths"].append({"path": path, "key": key, "count": len(value)})
        if key in {"unit_id", "target_unit_id", "producer_unit", "source_unit", "created_by_unit"} and is_scalar(value):
            out["producer_unit_candidates"].append({"path": path, "key": key, "value": value})
        if key in {"source_ref", "source_refs", "source_packet_ref", "source_packet_path", "lineage", "lineage_ref", "parent_receipt_id", "source_receipt_id"}:
            out["lineage_marker_paths"].append({"path": path, "key": key, "value_preview": value if is_scalar(value) else f"<{type(value).__name__}>"})
    return out

def scan_candidate_for_binding(feature: Dict[str, Any], broken: Dict[str, Any], slot: Dict[str, Any], policy: Dict[str, Any]) -> Dict[str, Any]:
    ref = norm(feature.get("candidate_source_ref"))
    p = source_path_from_ref(ref)
    slot_id = norm(feature.get("slot_id") or broken.get("slot_id") or slot.get("slot_id"))
    row_uid = norm(feature.get("row_uid") or broken.get("row_uid") or slot.get("row_uid"))
    field = norm(feature.get("field") or broken.get("field") or slot.get("field"))
    required_source_object = norm(slot.get("required_source_object") or policy.get("required_source_object") or policy.get("source_object"))
    source_class = norm(slot.get("source_class") or policy.get("source_class"))

    matches: List[Dict[str, Any]] = []
    structure_matches: List[Dict[str, Any]] = []
    lineage_matches: List[Dict[str, Any]] = []
    score = 0
    reasons: List[str] = []
    penalties: List[str] = []

    if p is None:
        penalties.append("candidate_source_ref_unresolved")
        return {
            "candidate_id": feature.get("candidate_id"),
            "slot_id": slot_id,
            "row_uid": row_uid,
            "field": field,
            "candidate_source_ref": ref,
            "locator_score": 0,
            "locator_reasons": reasons,
            "locator_penalties": penalties,
            "row_identity_match_count": 0,
            "source_object_structure_match_count": 0,
            "lineage_marker_count": 0,
            "row_identity_matches": matches,
            "source_object_structure_matches": structure_matches,
            "lineage_matches": lineage_matches,
            "locator_status": "SOURCE_REF_UNRESOLVED",
            "authorized_to_rebind": False,
        }

    try:
        obj = read_json(p)
    except Exception:
        penalties.append("candidate_source_json_unreadable")
        return {
            "candidate_id": feature.get("candidate_id"),
            "slot_id": slot_id,
            "row_uid": row_uid,
            "field": field,
            "candidate_source_ref": ref,
            "locator_score": 0,
            "locator_reasons": reasons,
            "locator_penalties": penalties,
            "row_identity_match_count": 0,
            "source_object_structure_match_count": 0,
            "lineage_marker_count": 0,
            "row_identity_matches": matches,
            "source_object_structure_matches": structure_matches,
            "lineage_matches": lineage_matches,
            "locator_status": "SOURCE_JSON_UNREADABLE",
            "authorized_to_rebind": False,
        }

    flat = flatten_json(obj)
    # Container-level matching: row_uid/slot_id/field should co-occur in same local object when possible.
    container_hits: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"matched": set(), "paths": []})

    for item in flat:
        key = norm(item.get("key"))
        val = item.get("value")
        sval = norm(val)
        path = norm(item.get("path"))
        cpath = container_path(path)

        if slot_id and ((key == "slot_id" and sval == slot_id) or sval == slot_id):
            container_hits[cpath]["matched"].add("slot_id")
            container_hits[cpath]["paths"].append({"path": path, "match": "slot_id", "value": sval})
        if row_uid and ((key == "row_uid" and sval == row_uid) or sval == row_uid):
            container_hits[cpath]["matched"].add("row_uid")
            container_hits[cpath]["paths"].append({"path": path, "match": "row_uid", "value": sval})
        if field and ((key == "field" and sval == field) or key == field or sval == field):
            container_hits[cpath]["matched"].add("field")
            container_hits[cpath]["paths"].append({"path": path, "match": "field", "value": sval if is_scalar(val) else f"<{type(val).__name__}>"})

        if required_source_object and (key in {"required_source_object", "source_object", "object_kind", "artifact_kind"} and sval == required_source_object):
            structure_matches.append({"path": path, "match": "required_source_object", "value": sval})
        if source_class and (key in {"source_class", "class", "source_kind"} and sval == source_class):
            structure_matches.append({"path": path, "match": "source_class", "value": sval})
        if key in {"records", "rows", "slots"} and isinstance(val, list):
            structure_matches.append({"path": path, "match": "row_like_collection", "count": len(val)})
        if key in {"unit_id", "target_unit_id", "producer_unit", "source_unit", "created_by_unit", "source_packet_ref", "source_packet_path", "lineage_ref", "source_receipt_id", "parent_receipt_id"}:
            lineage_matches.append({"path": path, "match": key, "value": sval if is_scalar(val) else f"<{type(val).__name__}>"})

    for cpath, payload in container_hits.items():
        matched = sorted(payload["matched"])
        if matched:
            matches.append({
                "container_path": cpath,
                "matched_identity_fields": matched,
                "match_count": len(matched),
                "paths": payload["paths"][:20],
                "candidate_row_json_path": cpath,
            })

    full_identity_matches = [m for m in matches if set(m["matched_identity_fields"]) >= {"slot_id", "row_uid", "field"}]
    partial_identity_matches = [m for m in matches if len(m["matched_identity_fields"]) >= 2]

    if full_identity_matches:
        score += 100
        reasons.append("full_row_identity_match_slot_row_uid_field")
    elif partial_identity_matches:
        score += 40
        reasons.append("partial_row_identity_match")
    elif matches:
        score += 10
        reasons.append("weak_identity_match")

    if structure_matches:
        score += min(30, 10 * len(structure_matches))
        reasons.append("source_object_structure_markers_found")
    else:
        penalties.append("no_source_object_structure_marker")

    if lineage_matches:
        score += min(25, 5 * len(lineage_matches))
        reasons.append("lineage_or_producer_markers_found")
    else:
        penalties.append("no_lineage_or_producer_marker")

    # Keep penalty for diagnostic-looking candidate, not fatal.
    if any(tok in ref for tok in ["review", "narrowing", "decision_surface"]):
        score -= 5
        penalties.append("candidate_ref_looks_diagnostic_or_decision_surface")
    if "source_packet" in ref or "source_metadata" in ref:
        score += 10
        reasons.append("candidate_ref_name_matches_source_packet_or_metadata")

    score = max(score, 0)
    if full_identity_matches:
        status = "FULL_ROW_IDENTITY_LOCATED"
    elif partial_identity_matches:
        status = "PARTIAL_ROW_IDENTITY_LOCATED"
    elif matches:
        status = "WEAK_ROW_IDENTITY_SIGNAL"
    else:
        status = "NO_ROW_IDENTITY_SIGNAL"

    return {
        "candidate_id": feature.get("candidate_id"),
        "slot_id": slot_id,
        "row_uid": row_uid,
        "field": field,
        "candidate_source_ref": ref,
        "candidate_ref_path_in_current_source": feature.get("candidate_ref_path_in_current_source"),
        "locator_score": score,
        "locator_reasons": reasons,
        "locator_penalties": penalties,
        "row_identity_match_count": len(matches),
        "full_row_identity_match_count": len(full_identity_matches),
        "partial_row_identity_match_count": len(partial_identity_matches),
        "source_object_structure_match_count": len(structure_matches),
        "lineage_marker_count": len(lineage_matches),
        "row_identity_matches": matches[:20],
        "source_object_structure_matches": structure_matches[:20],
        "lineage_matches": lineage_matches[:20],
        "best_candidate_row_json_path": full_identity_matches[0]["candidate_row_json_path"] if full_identity_matches else (partial_identity_matches[0]["candidate_row_json_path"] if partial_identity_matches else None),
        "locator_status": status,
        "authorized_to_rebind": False,
        "authorized_to_extract_value": False,
    }

def per_binding_locator(scans: List[Dict[str, Any]], residual_ties: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    by_slot: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for s in scans:
        by_slot[str(s.get("slot_id"))].append(s)

    per_rows: List[Dict[str, Any]] = []
    unique: List[Dict[str, Any]] = []
    ambiguous: List[Dict[str, Any]] = []

    for tie in residual_ties:
        slot_id = norm(tie.get("slot_id"))
        rows = sorted(by_slot.get(slot_id, []), key=lambda r: (-int(r.get("locator_score") or 0), norm(r.get("candidate_source_ref"))))
        if not rows:
            status = "NO_CANDIDATES_TO_LOCATE"
            top_score = None
            top = []
        else:
            top_score = rows[0]["locator_score"]
            top = [r for r in rows if r.get("locator_score") == top_score]

            if top_score and len(top) == 1:
                status = "UNIQUE_SOURCE_ROW_LOCATOR_PROPOSAL"
                chosen = top[0]
                unique.append({
                    "proposal_id": "source_row_locator_proposal_" + sha8({"slot_id": slot_id, "chosen": chosen}),
                    "slot_id": slot_id,
                    "row_uid": tie.get("row_uid"),
                    "field": tie.get("field"),
                    "proposed_row_source_ref": chosen.get("candidate_source_ref"),
                    "proposed_row_json_path": chosen.get("best_candidate_row_json_path"),
                    "locator_score": chosen.get("locator_score"),
                    "locator_reasons": chosen.get("locator_reasons"),
                    "locator_penalties": chosen.get("locator_penalties"),
                    "proposal_status": "SOURCE_ROW_LOCATED_FOR_REVIEW_NOT_APPLIED",
                    "authorized_to_apply": False,
                    "authorized_to_extract_value": False,
                })
            elif top_score and len(top) > 1:
                status = "RESIDUAL_SOURCE_ROW_LOCATOR_TIE"
                ambiguous.append({
                    "slot_id": slot_id,
                    "row_uid": tie.get("row_uid"),
                    "field": tie.get("field"),
                    "top_score": top_score,
                    "tied_locator_candidate_count": len(top),
                    "tied_candidates": [
                        {
                            "candidate_id": r.get("candidate_id"),
                            "candidate_source_ref": r.get("candidate_source_ref"),
                            "best_candidate_row_json_path": r.get("best_candidate_row_json_path"),
                            "locator_reasons": r.get("locator_reasons"),
                            "locator_penalties": r.get("locator_penalties"),
                            "locator_status": r.get("locator_status"),
                        }
                        for r in top
                    ],
                    "residual_ambiguity_reason": "multiple candidate artifacts expose equal row-locator evidence",
                    "safe_next_action": "review/narrow locator ties before rebind application",
                })
            else:
                status = "NO_POSITIVE_SOURCE_ROW_LOCATOR_SIGNAL"
                ambiguous.append({
                    "slot_id": slot_id,
                    "row_uid": tie.get("row_uid"),
                    "field": tie.get("field"),
                    "top_score": top_score,
                    "tied_locator_candidate_count": len(top),
                    "tied_candidates": [],
                    "residual_ambiguity_reason": "no candidate artifact exposes positive row identity/source-object evidence",
                    "safe_next_action": "build stronger source lineage or source-object typing surface",
                })

        per_rows.append({
            "slot_id": slot_id,
            "row_uid": tie.get("row_uid"),
            "field": tie.get("field"),
            "candidate_count": len(rows),
            "top_score": top_score,
            "top_candidate_count": len(top),
            "locator_status": status,
            "authorized_to_rebind": False,
            "authorized_to_extract_value": False,
            "safe_next_action": "review locator proposal before any application" if status == "UNIQUE_SOURCE_ROW_LOCATOR_PROPOSAL" else "do not apply; narrow or enrich locator evidence",
        })

    return per_rows, unique, ambiguous

def decide(per_rows: List[Dict[str, Any]], unique: List[Dict[str, Any]], ambiguous: List[Dict[str, Any]]) -> Tuple[str, List[str], str]:
    reason_codes = [
        "SOURCE_ROW_LOCATOR_SURFACE_BUILT",
        "CANDIDATE_ARTIFACTS_SCANNED_FOR_ROW_IDENTITY",
        "SOURCE_OBJECT_STRUCTURE_SCANNED",
        "SOURCE_LINEAGE_MARKERS_SCANNED",
        "NO_REBINDS_APPLIED",
        "NO_RULE_APPLIED",
        "NO_VALUES_AUTHORIZED_OR_APPLIED",
        "NO_METADATA_POPULATION",
    ]

    if len(unique) == len(per_rows) and per_rows:
        reason_codes.append("UNIQUE_SOURCE_ROW_LOCATOR_PROPOSALS_AVAILABLE_FOR_ALL_BINDINGS")
        status = "TYPED_MACHINE_READABLE_SOURCE_ROW_LOCATOR_BUILT_UNIQUE_PROPOSALS_READY_FOR_REVIEW"
        next_edge = "REVIEW_MACHINE_READABLE_SOURCE_ROW_LOCATOR_PROPOSALS_V0"
    elif unique:
        reason_codes.append("PARTIAL_SOURCE_ROW_LOCATOR_PROPOSALS_AVAILABLE")
        reason_codes.append("RESIDUAL_SOURCE_ROW_LOCATOR_AMBIGUITY_REMAINS")
        status = "TYPED_MACHINE_READABLE_SOURCE_ROW_LOCATOR_BUILT_PARTIAL_WITH_RESIDUAL_AMBIGUITY"
        next_edge = "REVIEW_PARTIAL_SOURCE_ROW_LOCATOR_PROPOSALS_OR_NARROW_RESIDUAL_AMBIGUITY_V0"
    else:
        reason_codes.append("NO_UNIQUE_SOURCE_ROW_LOCATOR_PROPOSALS")
        reason_codes.append("SOURCE_ROW_LOCATOR_EVIDENCE_INSUFFICIENT_FOR_REBIND_REVIEW")
        status = "TYPED_MACHINE_READABLE_SOURCE_ROW_LOCATOR_BUILT_NO_UNIQUE_PROPOSALS"
        next_edge = "BUILD_MACHINE_READABLE_SOURCE_LINEAGE_OR_FIELD_POLICY_TYPING_SURFACE_V0"

    return status, reason_codes, next_edge

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_row_locator_authority_boundary_v0",
        "status": status,
        "may_scan_candidate_artifacts": True,
        "may_locate_row_identity": True,
        "may_emit_locator_proposals": True,
        "may_emit_residual_locator_ambiguity": True,
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

def rollup_obj(status: str, scans: List[Dict[str, Any]], per_rows: List[Dict[str, Any]], unique: List[Dict[str, Any]], ambiguous: List[Dict[str, Any]], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_row_locator_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "candidate_artifact_scan_count": len(scans),
        "binding_count": len(per_rows),
        "unique_locator_proposal_count": len(unique),
        "residual_locator_ambiguity_count": len(ambiguous),
        "per_binding_locator_status_counts": dict(Counter(r["locator_status"] for r in per_rows)),
        "candidate_locator_status_counts": dict(Counter(r["locator_status"] for r in scans)),
        "candidate_positive_locator_score_count": sum(1 for r in scans if int(r.get("locator_score") or 0) > 0),
        "candidate_full_row_identity_match_count": sum(1 for r in scans if int(r.get("full_row_identity_match_count") or 0) > 0),
        "candidate_partial_row_identity_match_count": sum(1 for r in scans if int(r.get("partial_row_identity_match_count") or 0) > 0),
        "candidate_source_object_structure_match_count": sum(1 for r in scans if int(r.get("source_object_structure_match_count") or 0) > 0),
        "candidate_lineage_marker_count": sum(1 for r in scans if int(r.get("lineage_marker_count") or 0) > 0),
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
        "schema_version": "typed_machine_readable_source_row_locator_profile_v0",
        "profile_id": "source_row_locator_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "source_row_locator_surface_built": True,
        "source_row_locator_applied": False,
        "rebinds_applied": False,
        "dominance_rule_applied": False,
        "refinements_applied": False,
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
        "schema_version": "typed_machine_readable_source_row_locator_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The decision surface selected the source-row locator as the next machine-safe branch; this unit scans candidate artifacts for row identity and source-object evidence without applying source refs or values.",
        "candidate_artifact_scan_count": roll["candidate_artifact_scan_count"],
        "binding_count": roll["binding_count"],
        "unique_locator_proposal_count": roll["unique_locator_proposal_count"],
        "residual_locator_ambiguity_count": roll["residual_locator_ambiguity_count"],
        "per_binding_locator_status_counts": roll["per_binding_locator_status_counts"],
        "candidate_locator_status_counts": roll["candidate_locator_status_counts"],
        "candidate_positive_locator_score_count": roll["candidate_positive_locator_score_count"],
        "candidate_full_row_identity_match_count": roll["candidate_full_row_identity_match_count"],
        "candidate_partial_row_identity_match_count": roll["candidate_partial_row_identity_match_count"],
        "candidate_source_object_structure_match_count": roll["candidate_source_object_structure_match_count"],
        "candidate_lineage_marker_count": roll["candidate_lineage_marker_count"],
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
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
        "schema_version": "typed_machine_readable_source_row_locator_transition_trace_v0",
        "trace": [
            {
                "step": "consume_decision_surface",
                "question": "what machine-safe evidence can distinguish source-ref ties",
                "answer": "row identity, source-object structure, and lineage markers",
                "taken": "scan tied candidate artifacts",
            },
            {
                "step": "classify_locator_result",
                "question": "did row-location evidence make any source-ref choice uniquely reviewable",
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
        features, residual_ties, broken, slots, policies = [], [], {}, {}, {}
        scans, per_rows, unique, ambiguous = [], [], [], []
        status = "TYPED_MACHINE_READABLE_SOURCE_ROW_LOCATOR_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_MACHINE_READABLE_SOURCE_ROW_LOCATOR_BASIS_V0"
    else:
        features, residual_ties, broken, slots, policies = load_records()
        scans = []
        for f in features:
            slot_id = str(f.get("slot_id"))
            field = str(f.get("field") or broken.get(slot_id, {}).get("field") or slots.get(slot_id, {}).get("field") or "")
            scans.append(scan_candidate_for_binding(f, broken.get(slot_id, {}), slots.get(slot_id, {}), policies.get(field, {})))
        per_rows, unique, ambiguous = per_binding_locator(scans, residual_ties)
        status, reason_codes, next_edge = decide(per_rows, unique, ambiguous)

    roll = rollup_obj(status, scans, per_rows, unique, ambiguous, next_edge)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, roll, next_edge)
    boundary = authority_boundary_obj(status)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    source_summaries = []
    seen_refs = set()
    for s in scans:
        ref = s.get("candidate_source_ref")
        if ref and ref not in seen_refs:
            seen_refs.add(ref)
            source_summaries.append(summarize_source(ref))

    row_identity_records = []
    structure_records = []
    lineage_records = []
    for s in scans:
        for m in s.get("row_identity_matches", []):
            row_identity_records.append({
                "slot_id": s.get("slot_id"),
                "row_uid": s.get("row_uid"),
                "field": s.get("field"),
                "candidate_source_ref": s.get("candidate_source_ref"),
                **m,
            })
        for m in s.get("source_object_structure_matches", []):
            structure_records.append({
                "slot_id": s.get("slot_id"),
                "field": s.get("field"),
                "candidate_source_ref": s.get("candidate_source_ref"),
                **m,
            })
        for m in s.get("lineage_matches", []):
            lineage_records.append({
                "slot_id": s.get("slot_id"),
                "field": s.get("field"),
                "candidate_source_ref": s.get("candidate_source_ref"),
                **m,
            })

    locator_surface = {
        "schema_version": "typed_machine_readable_source_row_locator_surface_v0",
        "surface_status": status,
        "source_decision_surface_receipt_id": SOURCE_DECISION_SURFACE_RECEIPT_ID,
        "candidate_artifact_scan_count": roll["candidate_artifact_scan_count"],
        "binding_count": roll["binding_count"],
        "unique_locator_proposal_count": roll["unique_locator_proposal_count"],
        "residual_locator_ambiguity_count": roll["residual_locator_ambiguity_count"],
        "surface_claim": "Candidate artifacts were scanned for row identity, source-object structure, and lineage markers without applying source refs or values.",
        "candidate_artifact_scan_ref": rel(CANDIDATE_ARTIFACT_SCAN_PATH),
        "row_identity_match_table_ref": rel(ROW_IDENTITY_MATCH_TABLE_PATH),
        "source_object_structure_table_ref": rel(SOURCE_OBJECT_STRUCTURE_TABLE_PATH),
        "source_lineage_marker_table_ref": rel(SOURCE_LINEAGE_MARKER_TABLE_PATH),
        "per_binding_locator_table_ref": rel(PER_BINDING_LOCATOR_TABLE_PATH),
        "unique_locator_proposals_ref": rel(UNIQUE_LOCATOR_PROPOSALS_PATH),
        "residual_ambiguity_table_ref": rel(LOCATOR_RESIDUAL_AMBIGUITY_TABLE_PATH),
        "recommended_next": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    decision_options = {
        "schema_version": "typed_machine_readable_source_row_locator_decision_options_v0",
        "decision_options_status": "SOURCE_ROW_LOCATOR_DECISION_OPTIONS_EMITTED",
        "safe_options": [
            {
                "option": "REVIEW_UNIQUE_SOURCE_ROW_LOCATOR_PROPOSALS",
                "recommended": next_edge == "REVIEW_MACHINE_READABLE_SOURCE_ROW_LOCATOR_PROPOSALS_V0",
                "next_unit": "REVIEW_MACHINE_READABLE_SOURCE_ROW_LOCATOR_PROPOSALS_V0",
                "meaning": "Use only if every binding has a unique row-locator proposal; still no automatic rebind.",
            },
            {
                "option": "REVIEW_PARTIAL_OR_NARROW_RESIDUAL_LOCATOR_AMBIGUITY",
                "recommended": next_edge == "REVIEW_PARTIAL_SOURCE_ROW_LOCATOR_PROPOSALS_OR_NARROW_RESIDUAL_AMBIGUITY_V0",
                "next_unit": "REVIEW_PARTIAL_SOURCE_ROW_LOCATOR_PROPOSALS_OR_NARROW_RESIDUAL_AMBIGUITY_V0",
                "meaning": "Use if some bindings have row-location evidence but others remain ambiguous.",
            },
            {
                "option": "BUILD_SOURCE_LINEAGE_OR_FIELD_POLICY_TYPING_SURFACE",
                "recommended": next_edge == "BUILD_MACHINE_READABLE_SOURCE_LINEAGE_OR_FIELD_POLICY_TYPING_SURFACE_V0",
                "next_unit": "BUILD_MACHINE_READABLE_SOURCE_LINEAGE_OR_FIELD_POLICY_TYPING_SURFACE_V0",
                "meaning": "Use if row-locator evidence cannot make any binding uniquely reviewable.",
            },
        ],
        "forbidden_shortcuts": [
            "apply source refs from locator score",
            "extract values from located rows",
            "populate metadata",
            "mark discriminators ready",
            "break tie",
            "select build target",
        ],
    }

    next_contract = {
        "schema_version": "typed_machine_readable_source_row_locator_to_rebind_review_contract_v0",
        "contract_status": "SOURCE_ROW_LOCATOR_NEXT_CONTRACT_EMITTED",
        "recommended_next_unit": next_edge,
        "required_inputs_for_next_unit": [
            rel(ROW_LOCATOR_SURFACE_PATH),
            rel(CANDIDATE_ARTIFACT_SCAN_PATH),
            rel(PER_BINDING_LOCATOR_TABLE_PATH),
            rel(UNIQUE_LOCATOR_PROPOSALS_PATH),
            rel(LOCATOR_RESIDUAL_AMBIGUITY_TABLE_PATH),
        ],
        "must_not": [
            "apply source refs before review/application boundary",
            "infer values from locator output",
            "populate metadata",
            "mark discriminator ready",
            "use latest/mtime guessing",
        ],
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    classification = {
        "schema_version": "typed_machine_readable_source_row_locator_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "candidate_artifact_scan_count": roll["candidate_artifact_scan_count"],
        "binding_count": roll["binding_count"],
        "unique_locator_proposal_count": roll["unique_locator_proposal_count"],
        "residual_locator_ambiguity_count": roll["residual_locator_ambiguity_count"],
        "per_binding_locator_status_counts": roll["per_binding_locator_status_counts"],
        "candidate_locator_status_counts": roll["candidate_locator_status_counts"],
        "source_row_locator_applied": False,
        "rebinds_applied": False,
        "dominance_rule_applied": False,
        "refinements_applied": False,
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

    write_json(ROW_LOCATOR_SURFACE_PATH, locator_surface)
    write_json(CANDIDATE_ARTIFACT_SCAN_PATH, {
        "schema_version": "typed_machine_readable_source_row_locator_candidate_artifact_scan_v0",
        "scan_status": "CANDIDATE_ARTIFACTS_SCANNED_NOT_APPLIED",
        "candidate_scan_count": len(scans),
        "unique_candidate_source_ref_count": len(source_summaries),
        "source_summaries": source_summaries,
        "records": scans,
    })
    write_json(ROW_IDENTITY_MATCH_TABLE_PATH, {
        "schema_version": "typed_machine_readable_source_row_identity_match_table_v0",
        "table_status": "ROW_IDENTITY_MATCHES_EMITTED",
        "record_count": len(row_identity_records),
        "records": row_identity_records,
    })
    write_json(SOURCE_OBJECT_STRUCTURE_TABLE_PATH, {
        "schema_version": "typed_machine_readable_source_object_structure_table_v0",
        "table_status": "SOURCE_OBJECT_STRUCTURE_MARKERS_EMITTED",
        "record_count": len(structure_records),
        "records": structure_records,
    })
    write_json(SOURCE_LINEAGE_MARKER_TABLE_PATH, {
        "schema_version": "typed_machine_readable_source_lineage_marker_table_v0",
        "table_status": "SOURCE_LINEAGE_MARKERS_EMITTED",
        "record_count": len(lineage_records),
        "records": lineage_records,
    })
    write_json(PER_BINDING_LOCATOR_TABLE_PATH, {
        "schema_version": "typed_machine_readable_per_binding_source_row_locator_v0",
        "table_status": "PER_BINDING_SOURCE_ROW_LOCATOR_EMITTED",
        "binding_count": len(per_rows),
        "records": per_rows,
    })
    write_json(UNIQUE_LOCATOR_PROPOSALS_PATH, {
        "schema_version": "typed_machine_readable_unique_source_row_locator_proposals_v0",
        "proposal_status": "SOURCE_ROW_LOCATOR_PROPOSALS_EMITTED_NOT_APPLIED",
        "proposal_count": len(unique),
        "records": unique,
    })
    write_json(LOCATOR_RESIDUAL_AMBIGUITY_TABLE_PATH, {
        "schema_version": "typed_machine_readable_source_row_locator_residual_ambiguity_v0",
        "ambiguity_status": "SOURCE_ROW_LOCATOR_RESIDUAL_AMBIGUITY_EMITTED",
        "ambiguity_count": len(ambiguous),
        "records": ambiguous,
    })
    write_json(LOCATOR_DECISION_OPTIONS_PATH, decision_options)
    write_json(NEXT_REBIND_REVIEW_CONTRACT_PATH, next_contract)
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
        "ROW_LOCATOR_0_DECISION_SURFACE_RECEIPT_CONSUMED": SOURCE_DECISION_SURFACE_RECEIPT_PATH.exists(),
        "ROW_LOCATOR_1_ROW_LOCATOR_CONTRACT_CONSUMED": SOURCE_ROW_LOCATOR_SURFACE_CONTRACT_PATH.exists(),
        "ROW_LOCATOR_2_CANDIDATE_FEATURE_MATRIX_CONSUMED": SOURCE_DOMINANCE_FEATURE_MATRIX_PATH.exists(),
        "ROW_LOCATOR_3_ROW_LOCATOR_SURFACE_EMITTED": ROW_LOCATOR_SURFACE_PATH.exists(),
        "ROW_LOCATOR_4_CANDIDATE_ARTIFACT_SCAN_EMITTED": CANDIDATE_ARTIFACT_SCAN_PATH.exists(),
        "ROW_LOCATOR_5_ROW_IDENTITY_MATCH_TABLE_EMITTED": ROW_IDENTITY_MATCH_TABLE_PATH.exists(),
        "ROW_LOCATOR_6_SOURCE_OBJECT_STRUCTURE_TABLE_EMITTED": SOURCE_OBJECT_STRUCTURE_TABLE_PATH.exists(),
        "ROW_LOCATOR_7_SOURCE_LINEAGE_MARKER_TABLE_EMITTED": SOURCE_LINEAGE_MARKER_TABLE_PATH.exists(),
        "ROW_LOCATOR_8_PER_BINDING_LOCATOR_TABLE_EMITTED": PER_BINDING_LOCATOR_TABLE_PATH.exists(),
        "ROW_LOCATOR_9_UNIQUE_LOCATOR_PROPOSALS_EMITTED": UNIQUE_LOCATOR_PROPOSALS_PATH.exists(),
        "ROW_LOCATOR_10_RESIDUAL_AMBIGUITY_TABLE_EMITTED": LOCATOR_RESIDUAL_AMBIGUITY_TABLE_PATH.exists(),
        "ROW_LOCATOR_11_DECISION_OPTIONS_EMITTED": LOCATOR_DECISION_OPTIONS_PATH.exists(),
        "ROW_LOCATOR_12_NEXT_CONTRACT_EMITTED": NEXT_REBIND_REVIEW_CONTRACT_PATH.exists(),
        "ROW_LOCATOR_13_NO_ROW_LOCATOR_APPLIED": roll["source_row_locator_applied_count"] == 0,
        "ROW_LOCATOR_14_NO_REBINDS_APPLIED": roll["rebinds_applied_count"] == 0,
        "ROW_LOCATOR_15_NO_DOMINANCE_RULE_APPLIED": roll["dominance_rule_applied_count"] == 0,
        "ROW_LOCATOR_16_NO_VALUES_AUTHORIZED": roll["values_authorized_count"] == 0,
        "ROW_LOCATOR_17_NO_VALUES_APPLIED": roll["values_applied_count"] == 0,
        "ROW_LOCATOR_18_NO_NULL_REASONS_ACCEPTED": roll["null_reason_accepted_count"] == 0,
        "ROW_LOCATOR_19_NO_SOURCE_PACKET_MATERIALIZED": roll["source_packet_materialized_for_review_count"] == 0,
        "ROW_LOCATOR_20_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "ROW_LOCATOR_21_NO_DISCRIMINATOR_READY": roll["ready_discriminator_count"] == 0,
        "ROW_LOCATOR_22_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "ROW_LOCATOR_23_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "ROW_LOCATOR_24_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "ROW_LOCATOR_25_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classification["target_candidate_declared_for_review"] is False,
        "ROW_LOCATOR_26_NO_TARGET_SELECTED_FOR_BUILD": classification["target_selected_for_build"] is False,
        "ROW_LOCATOR_27_NO_ACCEPTED_FOR_BUILD": classification["accepted_for_build"] is False,
        "ROW_LOCATOR_28_NO_RUNTIME_PATCH": classification["runtime_patch_authorized"] is False,
        "ROW_LOCATOR_29_NO_TARGET_FILE_MODIFICATION": classification["target_file_modification_authorized"] is False,
        "ROW_LOCATOR_30_NO_C5_OPENED": classification["c5_authorized"] is False,
        "ROW_LOCATOR_31_NO_GENERAL_CELL1_AUTHORITY": classification["general_cell1_authority_granted"] is False,
        "ROW_LOCATOR_32_NO_LATEST_FILE_GUESSING": classification["latest_file_guessing"] is False,
        "ROW_LOCATOR_33_NO_MTIME_SELECTION": classification["mtime_selection"] is False,
        "ROW_LOCATOR_34_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "ROW_LOCATOR_35_ACCEPTANCE_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "ROW_LOCATOR_36_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_SOURCE_ROW_LOCATOR_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "candidate_scans": roll["candidate_artifact_scan_count"],
        "bindings": roll["binding_count"],
        "unique": roll["unique_locator_proposal_count"],
        "ambiguous": roll["residual_locator_ambiguity_count"],
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_source_row_locator_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_SOURCE_ROW_LOCATOR_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_decision_surface_receipt_id": SOURCE_DECISION_SURFACE_RECEIPT_ID,
        "machine_readable_source_row_locator_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "candidate_artifact_scan_count": roll["candidate_artifact_scan_count"],
            "binding_count": roll["binding_count"],
            "unique_locator_proposal_count": roll["unique_locator_proposal_count"],
            "residual_locator_ambiguity_count": roll["residual_locator_ambiguity_count"],
            "per_binding_locator_status_counts": roll["per_binding_locator_status_counts"],
            "candidate_locator_status_counts": roll["candidate_locator_status_counts"],
            "candidate_positive_locator_score_count": roll["candidate_positive_locator_score_count"],
            "candidate_full_row_identity_match_count": roll["candidate_full_row_identity_match_count"],
            "candidate_partial_row_identity_match_count": roll["candidate_partial_row_identity_match_count"],
            "candidate_source_object_structure_match_count": roll["candidate_source_object_structure_match_count"],
            "candidate_lineage_marker_count": roll["candidate_lineage_marker_count"],
            "source_row_locator_applied": False,
            "rebinds_applied": False,
            "dominance_rule_applied": False,
            "refinements_applied": False,
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
            "row_locator_surface": rel(ROW_LOCATOR_SURFACE_PATH),
            "candidate_artifact_scan": rel(CANDIDATE_ARTIFACT_SCAN_PATH),
            "row_identity_match_table": rel(ROW_IDENTITY_MATCH_TABLE_PATH),
            "source_object_structure_table": rel(SOURCE_OBJECT_STRUCTURE_TABLE_PATH),
            "source_lineage_marker_table": rel(SOURCE_LINEAGE_MARKER_TABLE_PATH),
            "per_binding_locator_table": rel(PER_BINDING_LOCATOR_TABLE_PATH),
            "unique_locator_proposals": rel(UNIQUE_LOCATOR_PROPOSALS_PATH),
            "locator_residual_ambiguity_table": rel(LOCATOR_RESIDUAL_AMBIGUITY_TABLE_PATH),
            "locator_decision_options": rel(LOCATOR_DECISION_OPTIONS_PATH),
            "next_rebind_review_contract": rel(NEXT_REBIND_REVIEW_CONTRACT_PATH),
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
    print(f"source_row_locator_receipt_id={receipt_id}")
    print(f"source_row_locator_receipt_path={rel(receipt_path)}")
    print(f"source_row_locator_surface_path={rel(ROW_LOCATOR_SURFACE_PATH)}")
    print(f"candidate_artifact_scan_path={rel(CANDIDATE_ARTIFACT_SCAN_PATH)}")
    print(f"row_identity_match_table_path={rel(ROW_IDENTITY_MATCH_TABLE_PATH)}")
    print(f"source_object_structure_table_path={rel(SOURCE_OBJECT_STRUCTURE_TABLE_PATH)}")
    print(f"source_lineage_marker_table_path={rel(SOURCE_LINEAGE_MARKER_TABLE_PATH)}")
    print(f"per_binding_locator_table_path={rel(PER_BINDING_LOCATOR_TABLE_PATH)}")
    print(f"unique_locator_proposals_path={rel(UNIQUE_LOCATOR_PROPOSALS_PATH)}")
    print(f"locator_residual_ambiguity_table_path={rel(LOCATOR_RESIDUAL_AMBIGUITY_TABLE_PATH)}")
    print(f"source_row_locator_rollup_path={rel(ROLLUP_PATH)}")
    print(f"source_row_locator_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
