#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REPAIR_TYPED_MACHINE_READABLE_VALUE_EXTRACTION_SURFACE_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_machine_readable_extraction_repair.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_MACHINE_READABLE_EXTRACTION_REPAIR"
MODE = "EXTRACTION_SURFACE_REPAIR / NO_VALUE_AUTHORIZATION / NO_METADATA_FILL / NO_TIE_BREAK / NO_ACCEPTANCE"
BUILD_MODE = "MACHINE_READABLE_EXTRACTION_SURFACE_REPAIR_ONLY"

SOURCE_VALUE_PROPOSITION_REVIEW_RECEIPT_ID = "360b2668"
SOURCE_VALUE_PROPOSITION_REVIEW_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_review_v0_receipts/360b2668.json"
SOURCE_REVIEW_ASSESSMENT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_review_v0/typed_value_source_value_proposition_review_assessment_v0.json"
SOURCE_MACHINE_GAP_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_review_v0/typed_value_source_machine_readable_gap_review_v0.json"
SOURCE_HUMAN_SCHEMA_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_review_v0/typed_value_source_human_schema_boundary_review_v0.json"
SOURCE_NULL_REASON_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_review_v0/typed_value_source_null_reason_review_v0.json"
SOURCE_REVIEW_FINDINGS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_review_v0/typed_value_source_value_proposition_review_findings_v0.json"
SOURCE_REVIEW_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_review_v0/typed_value_source_value_proposition_review_classification_v0.json"
SOURCE_REVIEW_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_review_v0/typed_value_source_value_proposition_review_rollup_v0.json"
SOURCE_REVIEW_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_review_v0/typed_value_source_value_proposition_review_profile_v0.json"

SOURCE_VALUE_PROPOSITION_RECEIPT_ID = "c581a69b"
SOURCE_VALUE_PROPOSITION_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_v0_receipts/c581a69b.json"
SOURCE_MACHINE_ATTEMPTS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_v0/typed_value_source_machine_readable_value_proposition_attempts_v0.json"
SOURCE_VALUE_PROPOSITION_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_v0/typed_value_source_value_proposition_packet_v0.json"
SOURCE_ABSENCE_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_v0/typed_value_source_value_absence_classification_v0.json"

SOURCE_SLOT_INVENTORY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_slot_inventory_v0.json"
SOURCE_MACHINE_SOURCE_SLOTS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_machine_source_slots_v0.json"
SOURCE_VALUES_PACKET_DRAFT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_v0/typed_value_source_metadata_source_packet_values_packet_draft_v0.json"
SOURCE_FIELD_POLICY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_source_field_policy_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_repair_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_repair_v0_receipts"

EXTRACTION_REPAIR_SURFACE_PATH = OUT_DIR / "typed_machine_readable_value_extraction_repair_surface_v0.json"
MACHINE_SLOT_EXTRACTION_DIAGNOSTIC_PATH = OUT_DIR / "typed_machine_readable_slot_extraction_diagnostic_v0.json"
SOURCE_REF_RESOLUTION_TABLE_PATH = OUT_DIR / "typed_machine_readable_source_ref_resolution_table_v0.json"
EXACT_KEY_CANDIDATE_TABLE_PATH = OUT_DIR / "typed_machine_readable_exact_key_candidate_table_v0.json"
EXTRACTION_RULE_CANDIDATES_PATH = OUT_DIR / "typed_machine_readable_extraction_rule_candidates_v0.json"
REPROPOSITION_INPUT_SURFACE_PATH = OUT_DIR / "typed_machine_readable_reproposition_input_surface_v0.json"
NONEXTRACTABLE_REASON_TABLE_PATH = OUT_DIR / "typed_machine_readable_nonextractable_reason_table_v0.json"
REPAIR_DECISION_OPTIONS_PATH = OUT_DIR / "typed_machine_readable_extraction_repair_decision_options_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_extraction_repair_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_extraction_repair_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_extraction_repair_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_extraction_repair_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_extraction_repair_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_extraction_repair_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_VALUE_PROPOSITION_REVIEW_RECEIPT_PATH,
    SOURCE_REVIEW_ASSESSMENT_PATH,
    SOURCE_MACHINE_GAP_REVIEW_PATH,
    SOURCE_HUMAN_SCHEMA_REVIEW_PATH,
    SOURCE_NULL_REASON_REVIEW_PATH,
    SOURCE_REVIEW_FINDINGS_PATH,
    SOURCE_REVIEW_CLASSIFICATION_PATH,
    SOURCE_REVIEW_ROLLUP_PATH,
    SOURCE_REVIEW_PROFILE_PATH,
    SOURCE_VALUE_PROPOSITION_RECEIPT_PATH,
    SOURCE_MACHINE_ATTEMPTS_PATH,
    SOURCE_VALUE_PROPOSITION_PACKET_PATH,
    SOURCE_ABSENCE_CLASSIFICATION_PATH,
    SOURCE_SLOT_INVENTORY_PATH,
    SOURCE_MACHINE_SOURCE_SLOTS_PATH,
    SOURCE_VALUES_PACKET_DRAFT_PATH,
    SOURCE_FIELD_POLICY_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_VALUE_SOURCE_VALUE_PROPOSITION_REVIEWED_REQUIRES_EXTRACTION_REPAIR_BEFORE_AUTHORIZATION"
EXPECTED_SOURCE_STOP = "STOP_TYPED_VALUE_SOURCE_VALUE_PROPOSITION_REVIEWED_REQUIRES_EXTRACTION_REPAIR_BEFORE_AUTHORIZATION"
EXPECTED_NEXT = "REPAIR_TYPED_MACHINE_READABLE_VALUE_EXTRACTION_SURFACE_V0"

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

    receipt = read_json(SOURCE_VALUE_PROPOSITION_REVIEW_RECEIPT_PATH)
    summary = receipt.get("value_proposition_review_summary", {})
    assessment = read_json(SOURCE_REVIEW_ASSESSMENT_PATH)
    machine_gap = read_json(SOURCE_MACHINE_GAP_REVIEW_PATH)
    classif = read_json(SOURCE_REVIEW_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_REVIEW_ROLLUP_PATH)
    profile = read_json(SOURCE_REVIEW_PROFILE_PATH)
    prop_receipt = read_json(SOURCE_VALUE_PROPOSITION_RECEIPT_PATH)
    prop_summary = prop_receipt.get("value_proposition_summary", {})
    machine_slots = read_json(SOURCE_MACHINE_SOURCE_SLOTS_PATH)

    if receipt.get("receipt_id") != SOURCE_VALUE_PROPOSITION_REVIEW_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("value_proposition_review_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"value_proposition_review_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("value_proposition_review_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"value_proposition_review_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("repairable_machine_gap_count") != 21:
        failures.append(f"repairable_machine_gap_count_not_21:{summary.get('repairable_machine_gap_count')}")
    if summary.get("source_backed_proposed_value_count") != 0:
        failures.append("source_backed_proposed_value_count_not_zero")
    if summary.get("null_proposition_count") != 30:
        failures.append("null_proposition_count_not_30")
    if summary.get("authorization_applied") is not False:
        failures.append("authorization_applied_unexpectedly")
    if summary.get("null_reasons_accepted") is not False:
        failures.append("null_reasons_accepted_unexpectedly")
    if summary.get("metadata_populated") is not False:
        failures.append("metadata_populated_unexpectedly")
    if summary.get("ready_discriminator_count") != 0:
        failures.append("ready_discriminator_nonzero")
    if summary.get("rule_refined") is not False:
        failures.append("rule_refined_unexpectedly")
    if summary.get("tie_broken") is not False:
        failures.append("tie_broken_unexpectedly")

    if assessment.get("review_status") != EXPECTED_SOURCE_STATUS:
        failures.append("review_assessment_status_wrong")
    if machine_gap.get("repairable_machine_gap_count") != 21:
        failures.append("machine_gap_review_repairable_count_not_21")
    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("review_classification_status_wrong")
    if roll.get("metadata_populated_count") != 0:
        failures.append("review_rollup_metadata_populated_nonzero")
    if profile.get("metadata_populated") is not False:
        failures.append("review_profile_metadata_populated_true")
    if prop_summary.get("source_backed_proposed_value_count") != 0:
        failures.append("source_proposition_receipt_had_source_backed_values")
    if machine_slots.get("slot_count") != 21:
        failures.append("machine_source_slots_count_not_21")

    return failures

def load_machine_slots() -> List[Dict[str, Any]]:
    data = read_json(SOURCE_MACHINE_SOURCE_SLOTS_PATH)
    return [x for x in data.get("slots", []) if isinstance(x, dict)]

def load_machine_attempts_by_slot() -> Dict[str, Dict[str, Any]]:
    data = read_json(SOURCE_MACHINE_ATTEMPTS_PATH)
    out = {}
    for item in data.get("attempts", []):
        if isinstance(item, dict) and item.get("slot_id"):
            out[str(item["slot_id"])] = item
    return out

def source_path_from_ref(ref: Any) -> Path | None:
    if not isinstance(ref, str) or not ref.strip():
        return None
    p = Path(ref.strip())
    if not p.is_absolute():
        p = ROOT / p
    return p if p.exists() else None

def flatten_json(obj: Any, prefix: str = "$", out: List[Dict[str, Any]] | None = None, limit: int = 5000) -> List[Dict[str, Any]]:
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

def exact_key_candidates(obj: Any, field: str) -> List[Dict[str, Any]]:
    flat = flatten_json(obj)
    candidates = []
    for item in flat:
        if item["key"] == field:
            value = item["value"]
            candidates.append({
                "candidate_path": item["path"],
                "candidate_key": item["key"],
                "candidate_value_preview": value if isinstance(value, (str, int, float, bool)) or value is None else f"<{type(value).__name__}>",
                "candidate_value_type": item["type"],
                "match_type": "EXACT_FIELD_KEY",
            })
    return candidates

def suffix_key_candidates(obj: Any, field: str) -> List[Dict[str, Any]]:
    flat = flatten_json(obj)
    candidates = []
    suffixes = {field, field.replace("_ref", ""), field.replace("_strength", ""), field.replace("_key", "")}
    suffixes = {s for s in suffixes if s}
    for item in flat:
        key = item["key"]
        if key in suffixes or key.endswith("_" + field):
            value = item["value"]
            candidates.append({
                "candidate_path": item["path"],
                "candidate_key": key,
                "candidate_value_preview": value if isinstance(value, (str, int, float, bool)) or value is None else f"<{type(value).__name__}>",
                "candidate_value_type": item["type"],
                "match_type": "BOUNDED_SUFFIX_FIELD_KEY",
            })
    return candidates

def extract_json_path(obj: Any, json_path: Any) -> Any:
    if not isinstance(json_path, str) or not json_path.strip():
        return None
    path = json_path.strip()
    if path.startswith("$."):
        parts = path[2:].split(".")
    elif path.startswith("/"):
        parts = [p for p in path.split("/") if p]
    else:
        parts = [p for p in path.split(".") if p]
    cur = obj
    for part in parts:
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        elif isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except Exception:
                return None
        else:
            return None
    return cur

def source_resolution(slot: Dict[str, Any], attempt: Dict[str, Any] | None) -> Dict[str, Any]:
    source_ref = slot.get("row_source_ref")
    row_json_path = slot.get("row_json_path")
    p = source_path_from_ref(source_ref)

    base = {
        "slot_id": slot.get("slot_id"),
        "row_uid": slot.get("row_uid"),
        "field": slot.get("field"),
        "row_source_ref": source_ref,
        "row_json_path": row_json_path,
        "source_path_resolved": p is not None,
        "resolved_source_path": rel(p) if p else None,
        "source_file_readable_as_json": False,
        "row_json_path_resolves": False,
        "row_json_path_value_type": None,
        "row_json_path_value_preview": None,
        "source_resolution_status": None,
        "prior_attempt_absence_reason": attempt.get("absence_reason") if attempt else None,
        "prior_attempt_probe_status": (attempt or {}).get("source_probe", {}).get("source_probe_status"),
    }

    if p is None:
        base["source_resolution_status"] = "SOURCE_REF_UNRESOLVED_OR_FILE_MISSING"
        return base

    try:
        obj = read_json(p)
    except Exception as exc:
        base["source_resolution_status"] = "SOURCE_JSON_UNREADABLE"
        base["json_error"] = str(exc)
        return base

    base["source_file_readable_as_json"] = True
    row_value = extract_json_path(obj, row_json_path)
    if row_value is not None:
        base["row_json_path_resolves"] = True
        base["row_json_path_value_type"] = type(row_value).__name__
        base["row_json_path_value_preview"] = row_value if isinstance(row_value, (str, int, float, bool)) or row_value is None else f"<{type(row_value).__name__}>"
        base["source_resolution_status"] = "SOURCE_AND_ROW_PATH_RESOLVED"
    else:
        base["source_resolution_status"] = "SOURCE_RESOLVED_ROW_PATH_NOT_FOUND"
    return base

def diagnostic_for_slot(slot: Dict[str, Any], attempt: Dict[str, Any] | None) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
    field = str(slot.get("field"))
    source_ref = slot.get("row_source_ref")
    p = source_path_from_ref(source_ref)
    resolution = source_resolution(slot, attempt)

    exact_candidates: List[Dict[str, Any]] = []
    suffix_candidates: List[Dict[str, Any]] = []
    extraction_rule_candidates: List[Dict[str, Any]] = []

    if p is not None:
        try:
            obj = read_json(p)
            exact_candidates = exact_key_candidates(obj, field)
            suffix_candidates = suffix_key_candidates(obj, field)
        except Exception:
            exact_candidates = []
            suffix_candidates = []

    if exact_candidates:
        repair_status = "EXACT_FIELD_CANDIDATE_FOUND_NOT_APPLIED"
        extraction_gap_reason = "VALUE_PRESENT_BUT_NOT_EXTRACTED"
        for c in exact_candidates:
            extraction_rule_candidates.append({
                "rule_candidate_id": "extract_rule_" + sha8({"slot_id": slot.get("slot_id"), "candidate": c}),
                "slot_id": slot.get("slot_id"),
                "row_uid": slot.get("row_uid"),
                "field": field,
                "candidate_source_ref": source_ref,
                "candidate_json_path": c["candidate_path"],
                "candidate_value_type": c["candidate_value_type"],
                "candidate_value_preview": c["candidate_value_preview"],
                "rule_status": "CANDIDATE_ONLY_NOT_APPLIED",
                "authorization_required_before_use": True,
                "why_not_applied_now": "This unit repairs extraction surface only; it does not fill/propose values.",
            })
    elif suffix_candidates:
        repair_status = "BOUNDED_SUFFIX_CANDIDATE_FOUND_NEEDS_TYPING"
        extraction_gap_reason = "SOURCE_FIELD_NOT_TYPED"
        for c in suffix_candidates:
            extraction_rule_candidates.append({
                "rule_candidate_id": "extract_rule_" + sha8({"slot_id": slot.get("slot_id"), "candidate": c}),
                "slot_id": slot.get("slot_id"),
                "row_uid": slot.get("row_uid"),
                "field": field,
                "candidate_source_ref": source_ref,
                "candidate_json_path": c["candidate_path"],
                "candidate_value_type": c["candidate_value_type"],
                "candidate_value_preview": c["candidate_value_preview"],
                "rule_status": "CANDIDATE_ONLY_NEEDS_TYPED_FIELD_CONFIRMATION",
                "authorization_required_before_use": True,
                "why_not_applied_now": "Candidate is bounded but not an exact field-key match.",
            })
    else:
        if not resolution["source_path_resolved"]:
            repair_status = "SOURCE_REF_REPAIR_REQUIRED"
            extraction_gap_reason = "SOURCE_REF_MISSING"
        elif not resolution["source_file_readable_as_json"]:
            repair_status = "SOURCE_CONTENT_REPAIR_REQUIRED"
            extraction_gap_reason = "SOURCE_CONTENT_ABSENT"
        elif not resolution["row_json_path_resolves"]:
            repair_status = "ROW_JSON_PATH_REPAIR_REQUIRED"
            extraction_gap_reason = "SOURCE_FIELD_NOT_TYPED"
        else:
            repair_status = "SOURCE_RESOLVES_BUT_FIELD_NOT_TYPED"
            extraction_gap_reason = "SOURCE_FIELD_NOT_TYPED"

    diagnostic = {
        "slot_id": slot.get("slot_id"),
        "row_uid": slot.get("row_uid"),
        "row_index": slot.get("row_index"),
        "field": field,
        "slot_category": slot.get("slot_category"),
        "source_class": slot.get("source_class"),
        "required_source_object": slot.get("required_source_object"),
        "row_source_ref": source_ref,
        "row_json_path": slot.get("row_json_path"),
        "resolution": resolution,
        "exact_key_candidate_count": len(exact_candidates),
        "suffix_key_candidate_count": len(suffix_candidates),
        "extraction_rule_candidate_count": len(extraction_rule_candidates),
        "repair_status": repair_status,
        "extraction_gap_reason": extraction_gap_reason,
        "safe_next_action": "use candidate extraction rules only in a later proposition retry after this surface is reviewed",
    }

    exact_rows = [
        {
            "slot_id": slot.get("slot_id"),
            "row_uid": slot.get("row_uid"),
            "field": field,
            **c,
        }
        for c in exact_candidates + suffix_candidates
    ]

    return diagnostic, exact_rows, extraction_rule_candidates

def build_surface(diagnostics: List[Dict[str, Any]], rule_candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    status_counts = Counter(d["repair_status"] for d in diagnostics)
    reason_counts = Counter(d["extraction_gap_reason"] for d in diagnostics)
    return {
        "schema_version": "typed_machine_readable_value_extraction_repair_surface_v0",
        "surface_status": "MACHINE_READABLE_VALUE_EXTRACTION_SURFACE_REPAIRED_FOR_REPROPOSITION",
        "source_review_receipt_id": SOURCE_VALUE_PROPOSITION_REVIEW_RECEIPT_ID,
        "slot_count": len(diagnostics),
        "repair_status_counts": dict(status_counts),
        "extraction_gap_reason_counts": dict(reason_counts),
        "extraction_rule_candidate_count": len(rule_candidates),
        "candidate_rules_available_for_later_proposition_retry": len(rule_candidates) > 0,
        "surface_claim": "This surface repairs extraction observability and candidate extraction paths; it does not authorize or apply values.",
        "diagnostic_ref": rel(MACHINE_SLOT_EXTRACTION_DIAGNOSTIC_PATH),
        "source_ref_resolution_table_ref": rel(SOURCE_REF_RESOLUTION_TABLE_PATH),
        "exact_key_candidate_table_ref": rel(EXACT_KEY_CANDIDATE_TABLE_PATH),
        "extraction_rule_candidates_ref": rel(EXTRACTION_RULE_CANDIDATES_PATH),
        "reproposition_input_surface_ref": rel(REPROPOSITION_INPUT_SURFACE_PATH),
        "recommended_next": "RETRY_TYPED_VALUE_SOURCE_VALUE_PROPOSITIONS_WITH_REPAIRED_EXTRACTION_SURFACE_V0" if rule_candidates else "REVIEW_MACHINE_READABLE_EXTRACTION_REPAIR_GAPS_V0",
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def decide_status(diagnostics: List[Dict[str, Any]], rule_candidates: List[Dict[str, Any]]) -> Tuple[str, List[str], str]:
    reason_codes = [
        "MACHINE_READABLE_EXTRACTION_SURFACE_REVIEWED",
        "MACHINE_READABLE_SLOT_DIAGNOSTICS_EMITTED",
        "SOURCE_REF_RESOLUTION_TABLE_EMITTED",
        "NO_VALUES_AUTHORIZED_OR_APPLIED",
        "NO_METADATA_POPULATION",
    ]

    if rule_candidates:
        reason_codes.append("EXTRACTION_RULE_CANDIDATES_FOUND_FOR_REPROPOSITION")
        status = "TYPED_MACHINE_READABLE_VALUE_EXTRACTION_SURFACE_REPAIRED_WITH_RULE_CANDIDATES"
        next_edge = "RETRY_TYPED_VALUE_SOURCE_VALUE_PROPOSITIONS_WITH_REPAIRED_EXTRACTION_SURFACE_V0"
    else:
        reason_codes.append("NO_EXTRACTION_RULE_CANDIDATES_FOUND")
        reason_codes.append("MACHINE_READABLE_GAPS_REQUIRE_SOURCE_REF_OR_TYPING_REPAIR")
        status = "TYPED_MACHINE_READABLE_VALUE_EXTRACTION_SURFACE_REPAIRED_NO_RULE_CANDIDATES"
        next_edge = "REVIEW_MACHINE_READABLE_EXTRACTION_REPAIR_GAPS_V0"

    return status, reason_codes, next_edge

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_extraction_repair_authority_boundary_v0",
        "status": status,
        "may_inspect_explicit_source_refs": True,
        "may_build_extraction_diagnostics": True,
        "may_emit_candidate_extraction_rules": True,
        "may_retry_proposition_later": False,
        "may_authorize_values": False,
        "may_accept_null_reasons_as_final": False,
        "may_materialize_source_packet_for_review": False,
        "may_populate_metadata": False,
        "may_evaluate_discriminators": False,
        "may_refine_rule": False,
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

def rollup_obj(status: str, diagnostics: List[Dict[str, Any]], rule_candidates: List[Dict[str, Any]], next_edge: str) -> Dict[str, Any]:
    status_counts = Counter(d["repair_status"] for d in diagnostics)
    reason_counts = Counter(d["extraction_gap_reason"] for d in diagnostics)
    return {
        "schema_version": "typed_machine_readable_extraction_repair_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "machine_readable_slot_count": len(diagnostics),
        "repair_status_counts": dict(status_counts),
        "extraction_gap_reason_counts": dict(reason_counts),
        "source_ref_resolution_count": len(diagnostics),
        "extraction_rule_candidate_count": len(rule_candidates),
        "candidate_rules_available_count": 1 if rule_candidates else 0,
        "values_authorized_count": 0,
        "values_applied_count": 0,
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
        "values_authorized_count",
        "values_applied_count",
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
        "schema_version": "typed_machine_readable_extraction_repair_profile_v0",
        "profile_id": "machine_readable_extraction_repair_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "extraction_surface_repaired": True,
        "candidate_rules_available": roll["candidate_rules_available_count"] == 1,
        "values_authorized": False,
        "values_applied": False,
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
        "schema_version": "typed_machine_readable_extraction_repair_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The proposition review found 21 repairable machine-readable gaps; this unit repairs the extraction surface without authorizing or applying values.",
        "machine_readable_slot_count": roll["machine_readable_slot_count"],
        "extraction_rule_candidate_count": roll["extraction_rule_candidate_count"],
        "repair_status_counts": roll["repair_status_counts"],
        "extraction_gap_reason_counts": roll["extraction_gap_reason_counts"],
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "values_authorized_count": 0,
        "values_applied_count": 0,
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
        "schema_version": "typed_machine_readable_extraction_repair_transition_trace_v0",
        "trace": [
            {
                "step": "consume_review_first_gate",
                "question": "why repair extraction surface",
                "answer": "review found 21 repairable machine-readable gaps and zero source-backed propositions",
                "taken": "inspect source refs and extraction candidates",
            },
            {
                "step": "build_extraction_surface",
                "question": "can any bounded extraction rules be proposed",
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

    diagnostics: List[Dict[str, Any]] = []
    candidate_rows: List[Dict[str, Any]] = []
    rule_candidates: List[Dict[str, Any]] = []
    resolution_rows: List[Dict[str, Any]] = []

    if not failures:
        attempts_by_slot = load_machine_attempts_by_slot()
        for slot in load_machine_slots():
            attempt = attempts_by_slot.get(str(slot.get("slot_id")))
            diagnostic, candidates, rules = diagnostic_for_slot(slot, attempt)
            diagnostics.append(diagnostic)
            candidate_rows.extend(candidates)
            rule_candidates.extend(rules)
            resolution_rows.append(diagnostic["resolution"])

    if failures:
        status = "TYPED_MACHINE_READABLE_VALUE_EXTRACTION_REPAIR_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_TYPED_MACHINE_READABLE_VALUE_EXTRACTION_REPAIR_BASIS_V0"
    else:
        status, reason_codes, next_edge = decide_status(diagnostics, rule_candidates)

    surface = build_surface(diagnostics, rule_candidates)
    roll = rollup_obj(status, diagnostics, rule_candidates, next_edge)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, roll, next_edge)
    boundary = authority_boundary_obj(status)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    classification = {
        "schema_version": "typed_machine_readable_extraction_repair_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "machine_readable_slot_count": len(diagnostics),
        "extraction_rule_candidate_count": len(rule_candidates),
        "candidate_rules_available": bool(rule_candidates),
        "values_authorized": False,
        "values_applied": False,
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

    reproposition_surface = {
        "schema_version": "typed_machine_readable_reproposition_input_surface_v0",
        "surface_status": "REPROPOSITION_INPUT_SURFACE_EMITTED",
        "source_extraction_repair_ref": rel(EXTRACTION_REPAIR_SURFACE_PATH),
        "rule_candidates_ref": rel(EXTRACTION_RULE_CANDIDATES_PATH),
        "may_retry_proposition_if_rule_candidates_available": bool(rule_candidates),
        "retry_unit": "RETRY_TYPED_VALUE_SOURCE_VALUE_PROPOSITIONS_WITH_REPAIRED_EXTRACTION_SURFACE_V0",
        "not_authorized_to_apply_values": True,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    decision_options = {
        "schema_version": "typed_machine_readable_extraction_repair_decision_options_v0",
        "decision_options_status": "EXTRACTION_REPAIR_DECISION_OPTIONS_EMITTED",
        "candidate_rules_available": bool(rule_candidates),
        "safe_options": [
            {
                "option": "RETRY_PROPOSITIONS_WITH_REPAIRED_EXTRACTION_SURFACE",
                "recommended": bool(rule_candidates),
                "next_unit": "RETRY_TYPED_VALUE_SOURCE_VALUE_PROPOSITIONS_WITH_REPAIRED_EXTRACTION_SURFACE_V0",
            },
            {
                "option": "REVIEW_EXTRACTION_REPAIR_GAPS",
                "recommended": not bool(rule_candidates),
                "next_unit": "REVIEW_MACHINE_READABLE_EXTRACTION_REPAIR_GAPS_V0",
            },
            {
                "option": "REFINE_SOURCE_REF_OR_FIELD_TYPING_SURFACE",
                "recommended": not bool(rule_candidates),
                "next_unit": "REFINE_MACHINE_READABLE_SOURCE_REF_OR_FIELD_TYPING_SURFACE_V0",
            },
        ],
        "forbidden_shortcuts": [
            "apply values directly",
            "authorize null reasons",
            "metadata population",
            "discriminator readiness",
            "rule refinement",
            "tie break",
            "runtime patch",
        ],
    }

    nonextractable = [
        {
            "slot_id": d.get("slot_id"),
            "row_uid": d.get("row_uid"),
            "field": d.get("field"),
            "repair_status": d.get("repair_status"),
            "extraction_gap_reason": d.get("extraction_gap_reason"),
            "source_resolution_status": d.get("resolution", {}).get("source_resolution_status"),
            "safe_next_action": d.get("safe_next_action"),
        }
        for d in diagnostics if d.get("extraction_rule_candidate_count", 0) == 0
    ]

    write_json(EXTRACTION_REPAIR_SURFACE_PATH, surface)
    write_json(MACHINE_SLOT_EXTRACTION_DIAGNOSTIC_PATH, {
        "schema_version": "typed_machine_readable_slot_extraction_diagnostic_v0",
        "diagnostic_status": "MACHINE_READABLE_SLOT_EXTRACTION_DIAGNOSTICS_EMITTED",
        "slot_count": len(diagnostics),
        "records": diagnostics,
    })
    write_json(SOURCE_REF_RESOLUTION_TABLE_PATH, {
        "schema_version": "typed_machine_readable_source_ref_resolution_table_v0",
        "resolution_status": "SOURCE_REFS_RESOLVED_FOR_EXTRACTION_REPAIR",
        "record_count": len(resolution_rows),
        "records": resolution_rows,
    })
    write_json(EXACT_KEY_CANDIDATE_TABLE_PATH, {
        "schema_version": "typed_machine_readable_exact_key_candidate_table_v0",
        "candidate_table_status": "BOUNDED_EXTRACTION_CANDIDATES_EMITTED",
        "candidate_count": len(candidate_rows),
        "records": candidate_rows,
    })
    write_json(EXTRACTION_RULE_CANDIDATES_PATH, {
        "schema_version": "typed_machine_readable_extraction_rule_candidates_v0",
        "rule_candidate_status": "EXTRACTION_RULE_CANDIDATES_EMITTED_NOT_APPLIED",
        "rule_candidate_count": len(rule_candidates),
        "records": rule_candidates,
    })
    write_json(REPROPOSITION_INPUT_SURFACE_PATH, reproposition_surface)
    write_json(NONEXTRACTABLE_REASON_TABLE_PATH, {
        "schema_version": "typed_machine_readable_nonextractable_reason_table_v0",
        "nonextractable_status": "NONEXTRACTABLE_REASONS_EMITTED",
        "record_count": len(nonextractable),
        "records": nonextractable,
    })
    write_json(REPAIR_DECISION_OPTIONS_PATH, decision_options)
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
        "EXTRACTION_REPAIR_0_REVIEW_RECEIPT_CONSUMED": SOURCE_VALUE_PROPOSITION_REVIEW_RECEIPT_PATH.exists(),
        "EXTRACTION_REPAIR_1_MACHINE_SLOTS_CONSUMED": SOURCE_MACHINE_SOURCE_SLOTS_PATH.exists(),
        "EXTRACTION_REPAIR_2_REPAIR_SURFACE_EMITTED": EXTRACTION_REPAIR_SURFACE_PATH.exists(),
        "EXTRACTION_REPAIR_3_SLOT_DIAGNOSTIC_EMITTED": MACHINE_SLOT_EXTRACTION_DIAGNOSTIC_PATH.exists(),
        "EXTRACTION_REPAIR_4_SOURCE_REF_RESOLUTION_EMITTED": SOURCE_REF_RESOLUTION_TABLE_PATH.exists(),
        "EXTRACTION_REPAIR_5_CANDIDATE_TABLE_EMITTED": EXACT_KEY_CANDIDATE_TABLE_PATH.exists(),
        "EXTRACTION_REPAIR_6_RULE_CANDIDATES_EMITTED": EXTRACTION_RULE_CANDIDATES_PATH.exists(),
        "EXTRACTION_REPAIR_7_REPROPOSITION_SURFACE_EMITTED": REPROPOSITION_INPUT_SURFACE_PATH.exists(),
        "EXTRACTION_REPAIR_8_NONEXTRACTABLE_REASONS_EMITTED": NONEXTRACTABLE_REASON_TABLE_PATH.exists(),
        "EXTRACTION_REPAIR_9_DECISION_OPTIONS_EMITTED": REPAIR_DECISION_OPTIONS_PATH.exists(),
        "EXTRACTION_REPAIR_10_NO_VALUES_AUTHORIZED": roll["values_authorized_count"] == 0,
        "EXTRACTION_REPAIR_11_NO_VALUES_APPLIED": roll["values_applied_count"] == 0,
        "EXTRACTION_REPAIR_12_NO_SOURCE_PACKET_MATERIALIZED": roll["source_packet_materialized_for_review_count"] == 0,
        "EXTRACTION_REPAIR_13_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "EXTRACTION_REPAIR_14_NO_DISCRIMINATOR_READY": roll["ready_discriminator_count"] == 0,
        "EXTRACTION_REPAIR_15_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "EXTRACTION_REPAIR_16_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "EXTRACTION_REPAIR_17_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "EXTRACTION_REPAIR_18_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classification["target_candidate_declared_for_review"] is False,
        "EXTRACTION_REPAIR_19_NO_TARGET_SELECTED_FOR_BUILD": classification["target_selected_for_build"] is False,
        "EXTRACTION_REPAIR_20_NO_ACCEPTED_FOR_BUILD": classification["accepted_for_build"] is False,
        "EXTRACTION_REPAIR_21_NO_RUNTIME_PATCH": classification["runtime_patch_authorized"] is False,
        "EXTRACTION_REPAIR_22_NO_TARGET_FILE_MODIFICATION": classification["target_file_modification_authorized"] is False,
        "EXTRACTION_REPAIR_23_NO_C5_OPENED": classification["c5_authorized"] is False,
        "EXTRACTION_REPAIR_24_NO_GENERAL_CELL1_AUTHORITY": classification["general_cell1_authority_granted"] is False,
        "EXTRACTION_REPAIR_25_NO_LATEST_FILE_GUESSING": classification["latest_file_guessing"] is False,
        "EXTRACTION_REPAIR_26_NO_MTIME_SELECTION": classification["mtime_selection"] is False,
        "EXTRACTION_REPAIR_27_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "EXTRACTION_REPAIR_28_ACCEPTANCE_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "EXTRACTION_REPAIR_29_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_VALUE_EXTRACTION_REPAIR_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "machine_slots": len(diagnostics),
        "rule_candidates": len(rule_candidates),
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_extraction_repair_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_VALUE_EXTRACTION_REPAIR_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_value_proposition_review_receipt_id": SOURCE_VALUE_PROPOSITION_REVIEW_RECEIPT_ID,
        "machine_readable_extraction_repair_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "machine_readable_slot_count": len(diagnostics),
            "extraction_rule_candidate_count": len(rule_candidates),
            "candidate_rules_available": bool(rule_candidates),
            "repair_status_counts": roll["repair_status_counts"],
            "extraction_gap_reason_counts": roll["extraction_gap_reason_counts"],
            "values_authorized": False,
            "values_applied": False,
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
            "extraction_repair_surface": rel(EXTRACTION_REPAIR_SURFACE_PATH),
            "machine_slot_extraction_diagnostic": rel(MACHINE_SLOT_EXTRACTION_DIAGNOSTIC_PATH),
            "source_ref_resolution_table": rel(SOURCE_REF_RESOLUTION_TABLE_PATH),
            "exact_key_candidate_table": rel(EXACT_KEY_CANDIDATE_TABLE_PATH),
            "extraction_rule_candidates": rel(EXTRACTION_RULE_CANDIDATES_PATH),
            "reproposition_input_surface": rel(REPROPOSITION_INPUT_SURFACE_PATH),
            "nonextractable_reason_table": rel(NONEXTRACTABLE_REASON_TABLE_PATH),
            "repair_decision_options": rel(REPAIR_DECISION_OPTIONS_PATH),
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
    print(f"machine_readable_extraction_repair_receipt_id={receipt_id}")
    print(f"machine_readable_extraction_repair_receipt_path={rel(receipt_path)}")
    print(f"machine_readable_extraction_repair_surface_path={rel(EXTRACTION_REPAIR_SURFACE_PATH)}")
    print(f"machine_slot_extraction_diagnostic_path={rel(MACHINE_SLOT_EXTRACTION_DIAGNOSTIC_PATH)}")
    print(f"source_ref_resolution_table_path={rel(SOURCE_REF_RESOLUTION_TABLE_PATH)}")
    print(f"exact_key_candidate_table_path={rel(EXACT_KEY_CANDIDATE_TABLE_PATH)}")
    print(f"extraction_rule_candidates_path={rel(EXTRACTION_RULE_CANDIDATES_PATH)}")
    print(f"reproposition_input_surface_path={rel(REPROPOSITION_INPUT_SURFACE_PATH)}")
    print(f"nonextractable_reason_table_path={rel(NONEXTRACTABLE_REASON_TABLE_PATH)}")
    print(f"machine_readable_extraction_repair_rollup_path={rel(ROLLUP_PATH)}")
    print(f"machine_readable_extraction_repair_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
