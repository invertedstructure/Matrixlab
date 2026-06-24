#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REFINE_MACHINE_READABLE_SOURCE_REF_OR_ROW_PATH_TYPING_SURFACE_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_ref_row_path_refinement.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_REF_ROW_PATH_REFINEMENT"
MODE = "SOURCE_REF_ROW_PATH_REFINEMENT / NO_VALUE_AUTHORIZATION / NO_METADATA_FILL / NO_TIE_BREAK / NO_ACCEPTANCE"
BUILD_MODE = "SOURCE_REF_ROW_PATH_REFINEMENT_SURFACE_ONLY"

SOURCE_GAP_REVIEW_RECEIPT_ID = "62fd5e27"
SOURCE_GAP_REVIEW_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_gap_review_v0_receipts/62fd5e27.json"
SOURCE_GAP_REVIEW_ASSESSMENT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_gap_review_v0/typed_machine_readable_extraction_gap_review_assessment_v0.json"
SOURCE_ROW_JSON_PATH_GAP_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_gap_review_v0/typed_machine_readable_row_json_path_gap_table_v0.json"
SOURCE_SOURCE_REF_LAYER_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_gap_review_v0/typed_machine_readable_source_ref_layer_review_v0.json"
SOURCE_FIELD_TYPING_GAP_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_gap_review_v0/typed_machine_readable_field_typing_gap_table_v0.json"
SOURCE_EXTRACTION_NARROWNESS_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_gap_review_v0/typed_machine_readable_extraction_unit_narrowness_review_v0.json"
SOURCE_GAP_CAUSE_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_gap_review_v0/typed_machine_readable_extraction_gap_cause_classification_v0.json"
SOURCE_REPAIR_PLAN_OPTIONS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_gap_review_v0/typed_machine_readable_extraction_gap_repair_plan_options_v0.json"
SOURCE_NEXT_SURFACE_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_gap_review_v0/typed_machine_readable_source_ref_field_typing_refinement_contract_v0.json"
SOURCE_GAP_REVIEW_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_gap_review_v0/typed_machine_readable_extraction_gap_review_classification_v0.json"
SOURCE_GAP_REVIEW_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_gap_review_v0/typed_machine_readable_extraction_gap_review_rollup_v0.json"
SOURCE_GAP_REVIEW_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_gap_review_v0/typed_machine_readable_extraction_gap_review_profile_v0.json"

SOURCE_MACHINE_SOURCE_SLOTS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_machine_source_slots_v0.json"
SOURCE_SLOT_INVENTORY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_slot_inventory_v0.json"
SOURCE_FIELD_POLICY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_source_field_policy_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_row_path_refinement_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_row_path_refinement_v0_receipts"

REFINEMENT_SURFACE_PATH = OUT_DIR / "typed_machine_readable_source_ref_row_path_refinement_surface_v0.json"
BROKEN_BINDING_TABLE_PATH = OUT_DIR / "typed_machine_readable_broken_row_binding_table_v0.json"
SOURCE_REF_REBIND_CANDIDATE_TABLE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_candidate_table_v0.json"
ROW_PATH_CANDIDATE_TABLE_PATH = OUT_DIR / "typed_machine_readable_row_path_candidate_table_v0.json"
ROW_PATH_REFINEMENT_PROPOSALS_PATH = OUT_DIR / "typed_machine_readable_row_path_refinement_proposals_v0.json"
UNRESOLVED_BINDING_REASON_TABLE_PATH = OUT_DIR / "typed_machine_readable_unresolved_row_binding_reason_table_v0.json"
REFINEMENT_REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_source_ref_row_path_refinement_review_packet_v0.json"
REFINEMENT_APPLICATION_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_source_ref_row_path_refinement_application_contract_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_source_ref_row_path_refinement_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_source_ref_row_path_refinement_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_source_ref_row_path_refinement_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_source_ref_row_path_refinement_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_source_ref_row_path_refinement_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_source_ref_row_path_refinement_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_GAP_REVIEW_RECEIPT_PATH,
    SOURCE_GAP_REVIEW_ASSESSMENT_PATH,
    SOURCE_ROW_JSON_PATH_GAP_TABLE_PATH,
    SOURCE_SOURCE_REF_LAYER_REVIEW_PATH,
    SOURCE_FIELD_TYPING_GAP_TABLE_PATH,
    SOURCE_EXTRACTION_NARROWNESS_REVIEW_PATH,
    SOURCE_GAP_CAUSE_CLASSIFICATION_PATH,
    SOURCE_REPAIR_PLAN_OPTIONS_PATH,
    SOURCE_NEXT_SURFACE_CONTRACT_PATH,
    SOURCE_GAP_REVIEW_CLASSIFICATION_PATH,
    SOURCE_GAP_REVIEW_ROLLUP_PATH,
    SOURCE_GAP_REVIEW_PROFILE_PATH,
    SOURCE_MACHINE_SOURCE_SLOTS_PATH,
    SOURCE_SLOT_INVENTORY_PATH,
    SOURCE_FIELD_POLICY_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_EXTRACTION_GAPS_REVIEWED_ROW_PATH_REPAIR_REQUIRED"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_EXTRACTION_GAPS_REVIEWED_ROW_PATH_REPAIR_REQUIRED"
EXPECTED_NEXT = "REFINE_MACHINE_READABLE_SOURCE_REF_OR_ROW_PATH_TYPING_SURFACE_V0"

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

def validate_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    receipt = read_json(SOURCE_GAP_REVIEW_RECEIPT_PATH)
    summary = receipt.get("machine_readable_extraction_gap_review_summary", {})
    row_gap = read_json(SOURCE_ROW_JSON_PATH_GAP_TABLE_PATH)
    source_layer = read_json(SOURCE_SOURCE_REF_LAYER_REVIEW_PATH)
    field_gap = read_json(SOURCE_FIELD_TYPING_GAP_TABLE_PATH)
    narrowness = read_json(SOURCE_EXTRACTION_NARROWNESS_REVIEW_PATH)
    cause = read_json(SOURCE_GAP_CAUSE_CLASSIFICATION_PATH)
    classif = read_json(SOURCE_GAP_REVIEW_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_GAP_REVIEW_ROLLUP_PATH)
    profile = read_json(SOURCE_GAP_REVIEW_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_GAP_REVIEW_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("gap_review_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"gap_review_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("gap_review_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"gap_review_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("machine_readable_slot_count") != 21:
        failures.append("gap_review_machine_slot_count_not_21")
    if summary.get("primary_gap_cause_counts", {}).get("ROW_JSON_PATH_DOES_NOT_RESOLVE") != 21:
        failures.append("row_json_path_does_not_resolve_count_not_21")
    if summary.get("recommended_repair_action_counts", {}).get("REPAIR_ROW_JSON_PATH_OR_ROW_SOURCE_REF") != 21:
        failures.append("repair_row_json_path_or_source_ref_count_not_21")
    if summary.get("row_json_path_gap_count") != 21:
        failures.append("row_json_path_gap_count_not_21")
    if summary.get("field_typing_gap_count") != 0:
        failures.append("field_typing_gap_count_nonzero")
    if summary.get("extractor_too_narrow_count") != 0:
        failures.append("extractor_too_narrow_count_nonzero")
    if summary.get("values_authorized") is not False:
        failures.append("values_authorized_unexpectedly")
    if summary.get("values_applied") is not False:
        failures.append("values_applied_unexpectedly")
    if summary.get("metadata_populated") is not False:
        failures.append("metadata_populated_unexpectedly")
    if summary.get("ready_discriminator_count") != 0:
        failures.append("ready_discriminator_nonzero")

    if row_gap.get("record_count") != 21:
        failures.append("row_gap_table_count_not_21")
    if field_gap.get("record_count") != 0:
        failures.append("field_gap_table_nonzero")
    if narrowness.get("extractor_too_narrow_count") != 0:
        failures.append("narrowness_nonzero")
    if cause.get("classification_status") != "GAP_CAUSES_CLASSIFIED":
        failures.append("gap_cause_classification_status_wrong")
    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("gap_review_classification_status_wrong")
    if roll.get("metadata_populated_count") != 0:
        failures.append("gap_review_rollup_metadata_populated_nonzero")
    if profile.get("metadata_populated") is not False:
        failures.append("gap_review_profile_metadata_populated_true")
    if not isinstance(source_layer.get("records", []), list):
        failures.append("source_layer_records_not_list")

    return failures

def load_broken_bindings() -> List[Dict[str, Any]]:
    row_gap = read_json(SOURCE_ROW_JSON_PATH_GAP_TABLE_PATH)
    cause = read_json(SOURCE_GAP_CAUSE_CLASSIFICATION_PATH)
    cause_by_slot = {
        r.get("slot_id"): r
        for r in cause.get("records", [])
        if isinstance(r, dict) and r.get("slot_id")
    }
    out = []
    for r in row_gap.get("records", []):
        if not isinstance(r, dict):
            continue
        c = cause_by_slot.get(r.get("slot_id"), {})
        merged = dict(r)
        merged.update({
            "primary_gap_cause": c.get("primary_gap_cause"),
            "recommended_repair_action": c.get("recommended_repair_action"),
            "source_path_resolved": c.get("source_path_resolved"),
            "source_file_readable_as_json": c.get("source_file_readable_as_json"),
            "row_json_path_resolves": c.get("row_json_path_resolves"),
        })
        out.append(merged)
    return out

def load_machine_slots_by_slot() -> Dict[str, Dict[str, Any]]:
    data = read_json(SOURCE_MACHINE_SOURCE_SLOTS_PATH)
    return {
        str(s.get("slot_id")): s
        for s in data.get("slots", [])
        if isinstance(s, dict) and s.get("slot_id")
    }

def flatten_json(obj: Any, prefix: str = "$", out: List[Dict[str, Any]] | None = None, limit: int = 10000) -> List[Dict[str, Any]]:
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

def preview(v: Any) -> Any:
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    if isinstance(v, list):
        return f"<list:{len(v)}>"
    if isinstance(v, dict):
        return f"<dict:{len(v)}>"
    return f"<{type(v).__name__}>"

def container_path_for_match(path: str) -> str:
    if "." not in path:
        return path
    return path.rsplit(".", 1)[0] or "$"

def find_row_path_candidates(binding: Dict[str, Any], slot: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    source_ref = binding.get("row_source_ref")
    field = str(binding.get("field"))
    row_uid = binding.get("row_uid")
    slot_id = binding.get("slot_id")
    p = source_path_from_ref(source_ref)

    source_candidates: List[Dict[str, Any]] = []
    row_candidates: List[Dict[str, Any]] = []

    if p is None:
        return source_candidates, row_candidates

    try:
        obj = read_json(p)
    except Exception:
        return source_candidates, row_candidates

    flat = flatten_json(obj)

    match_specs = [
        ("slot_id", slot_id, 100),
        ("row_uid", row_uid, 95),
        ("field", field, 70),
        ("source_class", slot.get("source_class"), 40),
        ("required_source_object", slot.get("required_source_object"), 30),
    ]

    container_scores: Dict[str, int] = defaultdict(int)
    container_reasons: Dict[str, List[str]] = defaultdict(list)
    for item in flat:
        key = item["key"]
        value = item["value"]
        for expected_key, expected_value, score in match_specs:
            if expected_value is None:
                continue
            if key == expected_key and value == expected_value:
                cpath = container_path_for_match(item["path"])
                container_scores[cpath] += score
                container_reasons[cpath].append(f"matched {expected_key}={expected_value!r}")

    # Field-bearing containers are useful but low confidence unless they also contain row identity.
    for item in flat:
        if item["key"] == field:
            cpath = container_path_for_match(item["path"])
            container_scores[cpath] += 25
            container_reasons[cpath].append(f"contains exact field key {field!r}")

    for cpath, score in sorted(container_scores.items(), key=lambda kv: (-kv[1], kv[0]))[:8]:
        row_candidates.append({
            "candidate_id": "row_path_candidate_" + sha8({"slot_id": slot_id, "path": cpath, "score": score}),
            "slot_id": slot_id,
            "row_uid": row_uid,
            "field": field,
            "candidate_source_ref": source_ref,
            "candidate_row_json_path": cpath,
            "candidate_score": score,
            "candidate_reason_codes": container_reasons[cpath],
            "candidate_status": "CANDIDATE_ONLY_NOT_APPLIED",
            "safe_use": "may be used only by later reviewed refinement application",
        })

    # If same source has no row candidate, look for nearby artifact references in source object; do not follow them here.
    for item in flat:
        if isinstance(item["value"], str) and item["value"].endswith(".json"):
            source_candidates.append({
                "candidate_id": "source_ref_candidate_" + sha8({"slot_id": slot_id, "path": item["path"], "value": item["value"]}),
                "slot_id": slot_id,
                "row_uid": row_uid,
                "field": field,
                "candidate_source_ref": item["value"],
                "candidate_ref_path_in_current_source": item["path"],
                "candidate_status": "SOURCE_REF_CANDIDATE_ONLY_NOT_APPLIED",
                "safe_use": "candidate source ref must be reviewed before rebinding",
            })

    return source_candidates[:8], row_candidates

def classify_binding(binding: Dict[str, Any], slot: Dict[str, Any], source_candidates: List[Dict[str, Any]], row_candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    p = source_path_from_ref(binding.get("row_source_ref"))
    source_resolves = p is not None
    row_candidate_count = len(row_candidates)
    source_candidate_count = len(source_candidates)

    if row_candidate_count > 0:
        status = "ROW_PATH_REFINEMENT_CANDIDATES_FOUND"
        repair_class = "ROW_JSON_PATH_REBIND_CANDIDATE_AVAILABLE"
        next_action = "review row path candidate before application"
    elif source_resolves and source_candidate_count > 0:
        status = "SOURCE_REF_REBIND_CANDIDATES_FOUND"
        repair_class = "SOURCE_REF_REBIND_CANDIDATE_AVAILABLE"
        next_action = "review source ref candidate before row path refinement"
    elif source_resolves:
        status = "SOURCE_RESOLVES_BUT_NO_ROW_PATH_CANDIDATES"
        repair_class = "SOURCE_REF_POINTS_TO_NON_ROW_TYPED_ARTIFACT"
        next_action = "build source row locator / source-ref rebinding surface"
    else:
        status = "SOURCE_REF_UNRESOLVED"
        repair_class = "SOURCE_REF_MISSING_OR_INVALID"
        next_action = "repair source ref binding"

    return {
        "slot_id": binding.get("slot_id"),
        "row_uid": binding.get("row_uid"),
        "field": binding.get("field"),
        "current_row_source_ref": binding.get("row_source_ref"),
        "current_row_json_path": binding.get("row_json_path"),
        "source_path_resolves": source_resolves,
        "row_path_refinement_candidate_count": row_candidate_count,
        "source_ref_rebind_candidate_count": source_candidate_count,
        "binding_refinement_status": status,
        "binding_repair_class": repair_class,
        "safe_next_action": next_action,
        "authorized_to_apply": False,
    }

def decide(binding_reviews: List[Dict[str, Any]]) -> Tuple[str, List[str], str]:
    counts = Counter(r["binding_refinement_status"] for r in binding_reviews)
    repair_counts = Counter(r["binding_repair_class"] for r in binding_reviews)

    reason_codes = [
        "SOURCE_REF_ROW_PATH_REFINEMENT_SURFACE_EMITTED",
        "BROKEN_ROW_BINDINGS_REVIEWED",
        "ROW_PATH_CANDIDATES_SEARCHED",
        "SOURCE_REF_REBIND_CANDIDATES_SEARCHED",
        "NO_BINDINGS_APPLIED",
        "NO_VALUES_AUTHORIZED_OR_APPLIED",
        "NO_METADATA_POPULATION",
    ]

    if counts.get("ROW_PATH_REFINEMENT_CANDIDATES_FOUND", 0) > 0:
        reason_codes.append("ROW_PATH_REFINEMENT_CANDIDATES_FOUND")
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_ROW_PATH_REFINEMENT_CANDIDATES_FOUND"
        next_edge = "REVIEW_MACHINE_READABLE_ROW_PATH_REFINEMENT_PROPOSALS_V0"
    elif counts.get("SOURCE_REF_REBIND_CANDIDATES_FOUND", 0) > 0:
        reason_codes.append("SOURCE_REF_REBIND_CANDIDATES_FOUND")
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_FOUND_ROW_PATH_STILL_BLOCKED"
        next_edge = "REVIEW_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_V0"
    else:
        reason_codes.append("NO_ROW_PATH_OR_SOURCE_REF_CANDIDATES_FOUND")
        reason_codes.append("SOURCE_ROW_LOCATOR_SURFACE_REQUIRED")
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_ROW_PATH_REFINEMENT_NO_CANDIDATES_FOUND"
        next_edge = "BUILD_MACHINE_READABLE_SOURCE_ROW_LOCATOR_SURFACE_V0"

    return status, reason_codes, next_edge

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_ref_row_path_refinement_authority_boundary_v0",
        "status": status,
        "may_search_row_path_candidates": True,
        "may_search_source_ref_rebind_candidates": True,
        "may_emit_refinement_proposals": True,
        "may_apply_refinements": False,
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

def rollup_obj(status: str, binding_reviews: List[Dict[str, Any]], row_candidates: List[Dict[str, Any]], source_candidates: List[Dict[str, Any]], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_ref_row_path_refinement_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "broken_binding_count": len(binding_reviews),
        "row_path_refinement_candidate_count": len(row_candidates),
        "source_ref_rebind_candidate_count": len(source_candidates),
        "binding_refinement_status_counts": dict(Counter(r["binding_refinement_status"] for r in binding_reviews)),
        "binding_repair_class_counts": dict(Counter(r["binding_repair_class"] for r in binding_reviews)),
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
        "schema_version": "typed_machine_readable_source_ref_row_path_refinement_profile_v0",
        "profile_id": "source_ref_row_path_refinement_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "refinement_surface_built": True,
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
        "schema_version": "typed_machine_readable_source_ref_row_path_refinement_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "All 21 machine-readable extraction gaps were row JSON path failures; this unit builds candidate source-ref/row-path refinement surfaces without applying bindings or values.",
        "broken_binding_count": roll["broken_binding_count"],
        "row_path_refinement_candidate_count": roll["row_path_refinement_candidate_count"],
        "source_ref_rebind_candidate_count": roll["source_ref_rebind_candidate_count"],
        "binding_refinement_status_counts": roll["binding_refinement_status_counts"],
        "binding_repair_class_counts": roll["binding_repair_class_counts"],
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
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
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
    }

def transition_trace_obj(status: str, reason_codes: List[str], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_ref_row_path_refinement_transition_trace_v0",
        "trace": [
            {
                "step": "consume_row_path_gap_review",
                "question": "what exactly is broken",
                "answer": "21 row_source_ref / row_json_path bindings do not resolve",
                "taken": "search candidate row paths and source-ref rebinds",
            },
            {
                "step": "emit_refinement_surface",
                "question": "can the existing source refs yield lawful row-path candidates",
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

    broken_bindings = [] if failures else load_broken_bindings()
    machine_slots = {} if failures else load_machine_slots_by_slot()

    binding_reviews: List[Dict[str, Any]] = []
    row_candidates: List[Dict[str, Any]] = []
    source_candidates: List[Dict[str, Any]] = []

    for binding in broken_bindings:
        slot = machine_slots.get(str(binding.get("slot_id")), {})
        source_cands, row_cands = find_row_path_candidates(binding, slot)
        source_candidates.extend(source_cands)
        row_candidates.extend(row_cands)
        binding_reviews.append(classify_binding(binding, slot, source_cands, row_cands))

    if failures:
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_ROW_PATH_REFINEMENT_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_MACHINE_READABLE_SOURCE_REF_ROW_PATH_REFINEMENT_BASIS_V0"
    else:
        status, reason_codes, next_edge = decide(binding_reviews)

    roll = rollup_obj(status, binding_reviews, row_candidates, source_candidates, next_edge)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, roll, next_edge)
    boundary = authority_boundary_obj(status)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    refinement_surface = {
        "schema_version": "typed_machine_readable_source_ref_row_path_refinement_surface_v0",
        "surface_status": status,
        "source_gap_review_receipt_id": SOURCE_GAP_REVIEW_RECEIPT_ID,
        "broken_binding_count": roll["broken_binding_count"],
        "row_path_refinement_candidate_count": roll["row_path_refinement_candidate_count"],
        "source_ref_rebind_candidate_count": roll["source_ref_rebind_candidate_count"],
        "refinements_applied": False,
        "surface_claim": "Broken row_source_ref / row_json_path bindings are reviewed and candidate refinements are exposed without applying bindings or values.",
        "broken_binding_table_ref": rel(BROKEN_BINDING_TABLE_PATH),
        "row_path_candidate_table_ref": rel(ROW_PATH_CANDIDATE_TABLE_PATH),
        "source_ref_rebind_candidate_table_ref": rel(SOURCE_REF_REBIND_CANDIDATE_TABLE_PATH),
        "refinement_proposals_ref": rel(ROW_PATH_REFINEMENT_PROPOSALS_PATH),
        "recommended_next": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    review_packet = {
        "schema_version": "typed_machine_readable_source_ref_row_path_refinement_review_packet_v0",
        "review_packet_status": "SOURCE_REF_ROW_PATH_REFINEMENT_REVIEW_REQUIRED",
        "question": "Review candidate row-path/source-ref refinements. This packet does not authorize applying them.",
        "allowed_responses": [
            "ACCEPT_ROW_PATH_REFINEMENT_PROPOSALS_FOR_APPLICATION_UNIT",
            "REJECT_AND_BUILD_SOURCE_ROW_LOCATOR_SURFACE",
            "REQUEST_SOURCE_REF_REBIND_REVIEW",
            "FREEZE_AS_DIAGNOSTIC_REFERENCE",
        ],
        "refinement_surface_ref": rel(REFINEMENT_SURFACE_PATH),
        "candidate_tables": [
            rel(ROW_PATH_CANDIDATE_TABLE_PATH),
            rel(SOURCE_REF_REBIND_CANDIDATE_TABLE_PATH),
        ],
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    application_contract = {
        "schema_version": "typed_machine_readable_source_ref_row_path_refinement_application_contract_v0",
        "contract_status": "REFINEMENT_APPLICATION_NOT_AUTHORIZED",
        "after_review_possible_unit": "APPLY_REVIEWED_MACHINE_READABLE_ROW_PATH_REFINEMENTS_V0",
        "application_would_only_update_binding_surface": True,
        "application_would_not_apply_values": True,
        "application_would_not_populate_metadata": True,
        "application_would_not_mark_discriminators_ready": True,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    classification = {
        "schema_version": "typed_machine_readable_source_ref_row_path_refinement_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "broken_binding_count": roll["broken_binding_count"],
        "row_path_refinement_candidate_count": roll["row_path_refinement_candidate_count"],
        "source_ref_rebind_candidate_count": roll["source_ref_rebind_candidate_count"],
        "binding_refinement_status_counts": roll["binding_refinement_status_counts"],
        "binding_repair_class_counts": roll["binding_repair_class_counts"],
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

    unresolved = [
        {
            "slot_id": r.get("slot_id"),
            "row_uid": r.get("row_uid"),
            "field": r.get("field"),
            "current_row_source_ref": r.get("current_row_source_ref"),
            "current_row_json_path": r.get("current_row_json_path"),
            "binding_refinement_status": r.get("binding_refinement_status"),
            "binding_repair_class": r.get("binding_repair_class"),
            "safe_next_action": r.get("safe_next_action"),
        }
        for r in binding_reviews
        if r.get("binding_refinement_status") not in {
            "ROW_PATH_REFINEMENT_CANDIDATES_FOUND",
            "SOURCE_REF_REBIND_CANDIDATES_FOUND",
        }
    ]

    write_json(REFINEMENT_SURFACE_PATH, refinement_surface)
    write_json(BROKEN_BINDING_TABLE_PATH, {
        "schema_version": "typed_machine_readable_broken_row_binding_table_v0",
        "table_status": "BROKEN_ROW_BINDINGS_EMITTED",
        "record_count": len(binding_reviews),
        "records": binding_reviews,
    })
    write_json(SOURCE_REF_REBIND_CANDIDATE_TABLE_PATH, {
        "schema_version": "typed_machine_readable_source_ref_rebind_candidate_table_v0",
        "candidate_status": "SOURCE_REF_REBIND_CANDIDATES_EMITTED_NOT_APPLIED",
        "candidate_count": len(source_candidates),
        "records": source_candidates,
    })
    write_json(ROW_PATH_CANDIDATE_TABLE_PATH, {
        "schema_version": "typed_machine_readable_row_path_candidate_table_v0",
        "candidate_status": "ROW_PATH_CANDIDATES_EMITTED_NOT_APPLIED",
        "candidate_count": len(row_candidates),
        "records": row_candidates,
    })
    write_json(ROW_PATH_REFINEMENT_PROPOSALS_PATH, {
        "schema_version": "typed_machine_readable_row_path_refinement_proposals_v0",
        "proposal_status": "ROW_PATH_REFINEMENT_PROPOSALS_EMITTED_NOT_APPLIED",
        "proposal_count": len(row_candidates),
        "records": row_candidates,
    })
    write_json(UNRESOLVED_BINDING_REASON_TABLE_PATH, {
        "schema_version": "typed_machine_readable_unresolved_row_binding_reason_table_v0",
        "unresolved_status": "UNRESOLVED_BINDINGS_EMITTED",
        "record_count": len(unresolved),
        "records": unresolved,
    })
    write_json(REFINEMENT_REVIEW_PACKET_PATH, review_packet)
    write_json(REFINEMENT_APPLICATION_CONTRACT_PATH, application_contract)
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
        "REFINEMENT_0_GAP_REVIEW_RECEIPT_CONSUMED": SOURCE_GAP_REVIEW_RECEIPT_PATH.exists(),
        "REFINEMENT_1_ROW_JSON_PATH_GAP_TABLE_CONSUMED": SOURCE_ROW_JSON_PATH_GAP_TABLE_PATH.exists(),
        "REFINEMENT_2_REFINEMENT_SURFACE_EMITTED": REFINEMENT_SURFACE_PATH.exists(),
        "REFINEMENT_3_BROKEN_BINDING_TABLE_EMITTED": BROKEN_BINDING_TABLE_PATH.exists(),
        "REFINEMENT_4_SOURCE_REF_REBIND_CANDIDATES_EMITTED": SOURCE_REF_REBIND_CANDIDATE_TABLE_PATH.exists(),
        "REFINEMENT_5_ROW_PATH_CANDIDATES_EMITTED": ROW_PATH_CANDIDATE_TABLE_PATH.exists(),
        "REFINEMENT_6_REFINEMENT_PROPOSALS_EMITTED": ROW_PATH_REFINEMENT_PROPOSALS_PATH.exists(),
        "REFINEMENT_7_UNRESOLVED_BINDING_REASONS_EMITTED": UNRESOLVED_BINDING_REASON_TABLE_PATH.exists(),
        "REFINEMENT_8_REVIEW_PACKET_EMITTED": REFINEMENT_REVIEW_PACKET_PATH.exists(),
        "REFINEMENT_9_APPLICATION_CONTRACT_EMITTED": REFINEMENT_APPLICATION_CONTRACT_PATH.exists(),
        "REFINEMENT_10_NO_REFINEMENTS_APPLIED": roll["refinements_applied_count"] == 0,
        "REFINEMENT_11_NO_VALUES_AUTHORIZED": roll["values_authorized_count"] == 0,
        "REFINEMENT_12_NO_VALUES_APPLIED": roll["values_applied_count"] == 0,
        "REFINEMENT_13_NO_NULL_REASONS_ACCEPTED": roll["null_reason_accepted_count"] == 0,
        "REFINEMENT_14_NO_SOURCE_PACKET_MATERIALIZED": roll["source_packet_materialized_for_review_count"] == 0,
        "REFINEMENT_15_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "REFINEMENT_16_NO_DISCRIMINATOR_READY": roll["ready_discriminator_count"] == 0,
        "REFINEMENT_17_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "REFINEMENT_18_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "REFINEMENT_19_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "REFINEMENT_20_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classification["target_candidate_declared_for_review"] is False,
        "REFINEMENT_21_NO_TARGET_SELECTED_FOR_BUILD": classification["target_selected_for_build"] is False,
        "REFINEMENT_22_NO_ACCEPTED_FOR_BUILD": classification["accepted_for_build"] is False,
        "REFINEMENT_23_NO_RUNTIME_PATCH": classification["runtime_patch_authorized"] is False,
        "REFINEMENT_24_NO_TARGET_FILE_MODIFICATION": classification["target_file_modification_authorized"] is False,
        "REFINEMENT_25_NO_C5_OPENED": classification["c5_authorized"] is False,
        "REFINEMENT_26_NO_GENERAL_CELL1_AUTHORITY": classification["general_cell1_authority_granted"] is False,
        "REFINEMENT_27_NO_LATEST_FILE_GUESSING": classification["latest_file_guessing"] is False,
        "REFINEMENT_28_NO_MTIME_SELECTION": classification["mtime_selection"] is False,
        "REFINEMENT_29_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "REFINEMENT_30_ACCEPTANCE_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "REFINEMENT_31_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_SOURCE_REF_ROW_PATH_REFINEMENT_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "broken_bindings": roll["broken_binding_count"],
        "row_candidates": roll["row_path_refinement_candidate_count"],
        "source_candidates": roll["source_ref_rebind_candidate_count"],
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_source_ref_row_path_refinement_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_SOURCE_REF_ROW_PATH_REFINEMENT_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_gap_review_receipt_id": SOURCE_GAP_REVIEW_RECEIPT_ID,
        "machine_readable_source_ref_row_path_refinement_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "broken_binding_count": roll["broken_binding_count"],
            "row_path_refinement_candidate_count": roll["row_path_refinement_candidate_count"],
            "source_ref_rebind_candidate_count": roll["source_ref_rebind_candidate_count"],
            "binding_refinement_status_counts": roll["binding_refinement_status_counts"],
            "binding_repair_class_counts": roll["binding_repair_class_counts"],
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
            "refinement_surface": rel(REFINEMENT_SURFACE_PATH),
            "broken_binding_table": rel(BROKEN_BINDING_TABLE_PATH),
            "source_ref_rebind_candidate_table": rel(SOURCE_REF_REBIND_CANDIDATE_TABLE_PATH),
            "row_path_candidate_table": rel(ROW_PATH_CANDIDATE_TABLE_PATH),
            "row_path_refinement_proposals": rel(ROW_PATH_REFINEMENT_PROPOSALS_PATH),
            "unresolved_binding_reason_table": rel(UNRESOLVED_BINDING_REASON_TABLE_PATH),
            "refinement_review_packet": rel(REFINEMENT_REVIEW_PACKET_PATH),
            "refinement_application_contract": rel(REFINEMENT_APPLICATION_CONTRACT_PATH),
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
    print(f"source_ref_row_path_refinement_receipt_id={receipt_id}")
    print(f"source_ref_row_path_refinement_receipt_path={rel(receipt_path)}")
    print(f"source_ref_row_path_refinement_surface_path={rel(REFINEMENT_SURFACE_PATH)}")
    print(f"broken_binding_table_path={rel(BROKEN_BINDING_TABLE_PATH)}")
    print(f"source_ref_rebind_candidate_table_path={rel(SOURCE_REF_REBIND_CANDIDATE_TABLE_PATH)}")
    print(f"row_path_candidate_table_path={rel(ROW_PATH_CANDIDATE_TABLE_PATH)}")
    print(f"row_path_refinement_proposals_path={rel(ROW_PATH_REFINEMENT_PROPOSALS_PATH)}")
    print(f"unresolved_binding_reason_table_path={rel(UNRESOLVED_BINDING_REASON_TABLE_PATH)}")
    print(f"refinement_review_packet_path={rel(REFINEMENT_REVIEW_PACKET_PATH)}")
    print(f"refinement_application_contract_path={rel(REFINEMENT_APPLICATION_CONTRACT_PATH)}")
    print(f"source_ref_row_path_refinement_rollup_path={rel(ROLLUP_PATH)}")
    print(f"source_ref_row_path_refinement_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
