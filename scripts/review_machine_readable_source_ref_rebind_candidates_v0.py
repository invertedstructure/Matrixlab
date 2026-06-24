#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_ref_rebind_review.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_REF_REBIND_REVIEW"
MODE = "SOURCE_REF_REBIND_REVIEW / NO_REBIND_APPLIED / NO_VALUE_AUTHORIZATION / NO_METADATA_FILL / NO_TIE_BREAK / NO_ACCEPTANCE"
BUILD_MODE = "SOURCE_REF_REBIND_REVIEW_ONLY"

SOURCE_REFINEMENT_RECEIPT_ID = "9f03b786"
SOURCE_REFINEMENT_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_row_path_refinement_v0_receipts/9f03b786.json"
SOURCE_REFINEMENT_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_row_path_refinement_v0/typed_machine_readable_source_ref_row_path_refinement_surface_v0.json"
SOURCE_BROKEN_BINDING_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_row_path_refinement_v0/typed_machine_readable_broken_row_binding_table_v0.json"
SOURCE_SOURCE_REF_REBIND_CANDIDATE_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_row_path_refinement_v0/typed_machine_readable_source_ref_rebind_candidate_table_v0.json"
SOURCE_ROW_PATH_CANDIDATE_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_row_path_refinement_v0/typed_machine_readable_row_path_candidate_table_v0.json"
SOURCE_ROW_PATH_REFINEMENT_PROPOSALS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_row_path_refinement_v0/typed_machine_readable_row_path_refinement_proposals_v0.json"
SOURCE_UNRESOLVED_BINDING_REASON_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_row_path_refinement_v0/typed_machine_readable_unresolved_row_binding_reason_table_v0.json"
SOURCE_REFINEMENT_REVIEW_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_row_path_refinement_v0/typed_machine_readable_source_ref_row_path_refinement_review_packet_v0.json"
SOURCE_REFINEMENT_APPLICATION_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_row_path_refinement_v0/typed_machine_readable_source_ref_row_path_refinement_application_contract_v0.json"
SOURCE_REFINEMENT_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_row_path_refinement_v0/typed_machine_readable_source_ref_row_path_refinement_classification_v0.json"
SOURCE_REFINEMENT_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_row_path_refinement_v0/typed_machine_readable_source_ref_row_path_refinement_rollup_v0.json"
SOURCE_REFINEMENT_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_row_path_refinement_v0/typed_machine_readable_source_ref_row_path_refinement_profile_v0.json"

SOURCE_MACHINE_SOURCE_SLOTS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_machine_source_slots_v0.json"
SOURCE_FIELD_POLICY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_source_field_policy_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_review_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_review_v0_receipts"

REVIEW_SURFACE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_review_surface_v0.json"
CANDIDATE_SCORE_TABLE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_candidate_score_table_v0.json"
PER_BINDING_REVIEW_TABLE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_per_binding_review_v0.json"
CANDIDATE_TIE_TABLE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_candidate_tie_table_v0.json"
UNIQUE_REBIND_PROPOSALS_PATH = OUT_DIR / "typed_machine_readable_unique_source_ref_rebind_proposals_v0.json"
AMBIGUOUS_REBIND_REASONS_PATH = OUT_DIR / "typed_machine_readable_ambiguous_source_ref_rebind_reasons_v0.json"
REVIEW_DECISION_OPTIONS_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_review_decision_options_v0.json"
NEXT_SURFACE_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_narrowing_contract_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_review_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_review_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_review_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_REFINEMENT_RECEIPT_PATH,
    SOURCE_REFINEMENT_SURFACE_PATH,
    SOURCE_BROKEN_BINDING_TABLE_PATH,
    SOURCE_SOURCE_REF_REBIND_CANDIDATE_TABLE_PATH,
    SOURCE_ROW_PATH_CANDIDATE_TABLE_PATH,
    SOURCE_ROW_PATH_REFINEMENT_PROPOSALS_PATH,
    SOURCE_UNRESOLVED_BINDING_REASON_TABLE_PATH,
    SOURCE_REFINEMENT_REVIEW_PACKET_PATH,
    SOURCE_REFINEMENT_APPLICATION_CONTRACT_PATH,
    SOURCE_REFINEMENT_CLASSIFICATION_PATH,
    SOURCE_REFINEMENT_ROLLUP_PATH,
    SOURCE_REFINEMENT_PROFILE_PATH,
    SOURCE_MACHINE_SOURCE_SLOTS_PATH,
    SOURCE_FIELD_POLICY_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_FOUND_ROW_PATH_STILL_BLOCKED"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_FOUND_ROW_PATH_STILL_BLOCKED"
EXPECTED_NEXT = "REVIEW_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_V0"

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

def infer_layer(ref: Any) -> str:
    if not isinstance(ref, str) or not ref:
        return "SOURCE_REF_MISSING"
    if "source_packet" in ref or "metadata_source" in ref:
        return "SOURCE_PACKET_OR_METADATA_SOURCE_LAYER"
    if "source_ref_row_path_refinement" in ref or "extraction_gap_review" in ref or "extraction_repair" in ref or "value_proposition" in ref:
        return "DERIVED_DIAGNOSTIC_LAYER"
    if "_receipts" in ref or "receipt" in ref:
        return "RECEIPT_LAYER"
    if "rollup" in ref or "profile" in ref or "report" in ref:
        return "SUMMARY_LAYER"
    if "input_repair" in ref:
        return "INPUT_REPAIR_LAYER"
    if ref.endswith(".json"):
        return "JSON_ARTIFACT_LAYER"
    return "UNKNOWN_LAYER"

def flatten_json(obj: Any, prefix: str = "$", out: List[Dict[str, Any]] | None = None, limit: int = 12000) -> List[Dict[str, Any]]:
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

def validate_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    receipt = read_json(SOURCE_REFINEMENT_RECEIPT_PATH)
    summary = receipt.get("machine_readable_source_ref_row_path_refinement_summary", {})
    surface = read_json(SOURCE_REFINEMENT_SURFACE_PATH)
    broken = read_json(SOURCE_BROKEN_BINDING_TABLE_PATH)
    candidates = read_json(SOURCE_SOURCE_REF_REBIND_CANDIDATE_TABLE_PATH)
    row_candidates = read_json(SOURCE_ROW_PATH_CANDIDATE_TABLE_PATH)
    proposals = read_json(SOURCE_ROW_PATH_REFINEMENT_PROPOSALS_PATH)
    classif = read_json(SOURCE_REFINEMENT_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_REFINEMENT_ROLLUP_PATH)
    profile = read_json(SOURCE_REFINEMENT_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_REFINEMENT_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_ref_row_path_refinement_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"refinement_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("refinement_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"refinement_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("broken_binding_count") != 21:
        failures.append("broken_binding_count_not_21")
    if summary.get("source_ref_rebind_candidate_count") != 168:
        failures.append(f"source_ref_candidate_count_not_168:{summary.get('source_ref_rebind_candidate_count')}")
    if summary.get("row_path_refinement_candidate_count") != 0:
        failures.append("row_path_refinement_candidate_count_nonzero")
    if summary.get("binding_refinement_status_counts", {}).get("SOURCE_REF_REBIND_CANDIDATES_FOUND") != 21:
        failures.append("binding_refinement_status_count_wrong")
    if summary.get("refinements_applied") is not False:
        failures.append("refinements_applied_unexpectedly")
    if summary.get("values_authorized") is not False:
        failures.append("values_authorized_unexpectedly")
    if summary.get("values_applied") is not False:
        failures.append("values_applied_unexpectedly")
    if summary.get("metadata_populated") is not False:
        failures.append("metadata_populated_unexpectedly")
    if summary.get("ready_discriminator_count") != 0:
        failures.append("ready_discriminator_nonzero")

    if surface.get("surface_status") != EXPECTED_SOURCE_STATUS:
        failures.append("refinement_surface_status_wrong")
    if broken.get("record_count") != 21:
        failures.append("broken_binding_record_count_not_21")
    if candidates.get("candidate_count") != 168:
        failures.append("candidate_table_count_not_168")
    if row_candidates.get("candidate_count") != 0:
        failures.append("row_candidate_table_nonzero")
    if proposals.get("proposal_count") != 0:
        failures.append("row_path_proposals_nonzero")
    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("refinement_classification_status_wrong")
    if roll.get("metadata_populated_count") != 0:
        failures.append("refinement_rollup_metadata_populated_nonzero")
    if profile.get("metadata_populated") is not False:
        failures.append("refinement_profile_metadata_populated_true")

    return failures

def load_records() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    broken = [r for r in read_json(SOURCE_BROKEN_BINDING_TABLE_PATH).get("records", []) if isinstance(r, dict)]
    candidates = [r for r in read_json(SOURCE_SOURCE_REF_REBIND_CANDIDATE_TABLE_PATH).get("records", []) if isinstance(r, dict)]
    slots = {
        str(s.get("slot_id")): s
        for s in read_json(SOURCE_MACHINE_SOURCE_SLOTS_PATH).get("slots", [])
        if isinstance(s, dict) and s.get("slot_id")
    }
    return broken, candidates, slots

def score_candidate(candidate: Dict[str, Any], binding: Dict[str, Any], slot: Dict[str, Any]) -> Dict[str, Any]:
    ref = candidate.get("candidate_source_ref")
    ref_path = candidate.get("candidate_ref_path_in_current_source")
    layer = infer_layer(ref)
    p = source_path_from_ref(ref)

    score = 0
    reasons: List[str] = []
    penalties: List[str] = []

    if p is not None:
        score += 25
        reasons.append("candidate_source_file_exists")
    else:
        penalties.append("candidate_source_file_not_local_or_missing")

    if layer == "SOURCE_PACKET_OR_METADATA_SOURCE_LAYER":
        score += 30
        reasons.append("candidate_layer_matches_source_packet_or_metadata_source")
    elif layer == "JSON_ARTIFACT_LAYER":
        score += 10
        reasons.append("candidate_is_json_artifact")
    elif layer in {"DERIVED_DIAGNOSTIC_LAYER", "RECEIPT_LAYER", "SUMMARY_LAYER", "INPUT_REPAIR_LAYER"}:
        score -= 30
        penalties.append(f"candidate_layer_is_non_source_or_derived:{layer}")

    if isinstance(ref_path, str):
        if "source" in ref_path:
            score += 5
            reasons.append("candidate_ref_path_contains_source")
        if "packet" in ref_path:
            score += 5
            reasons.append("candidate_ref_path_contains_packet")
        if "receipt" in ref_path:
            score -= 10
            penalties.append("candidate_ref_path_contains_receipt")
        if "rollup" in ref_path or "profile" in ref_path or "report" in ref_path:
            score -= 10
            penalties.append("candidate_ref_path_contains_summary_artifact")

    field = str(binding.get("field") or slot.get("field") or "")
    row_uid = binding.get("row_uid") or slot.get("row_uid")
    slot_id = binding.get("slot_id") or slot.get("slot_id")
    source_content_signals: List[str] = []
    source_json_readable = False
    source_contains_field_key = False
    source_contains_row_uid = False
    source_contains_slot_id = False
    source_contains_rows_key = False

    if p is not None:
        try:
            obj = read_json(p)
            source_json_readable = True
            flat = flatten_json(obj)
            keys = {x["key"] for x in flat}
            values = {str(x["value"]) for x in flat if isinstance(x.get("value"), (str, int, float, bool))}
            if field and field in keys:
                score += 20
                source_contains_field_key = True
                source_content_signals.append("contains_exact_field_key")
            if row_uid is not None and str(row_uid) in values:
                score += 20
                source_contains_row_uid = True
                source_content_signals.append("contains_row_uid_value")
            if slot_id is not None and str(slot_id) in values:
                score += 10
                source_contains_slot_id = True
                source_content_signals.append("contains_slot_id_value")
            if "rows" in keys or "records" in keys or "slots" in keys:
                score += 5
                source_contains_rows_key = True
                source_content_signals.append("contains_row_like_collection_key")
        except Exception as exc:
            penalties.append("candidate_source_json_unreadable")
            source_content_signals.append(f"json_error:{exc}")

    if score < 0:
        score = 0

    return {
        "candidate_id": candidate.get("candidate_id"),
        "slot_id": candidate.get("slot_id"),
        "row_uid": candidate.get("row_uid"),
        "field": candidate.get("field"),
        "candidate_source_ref": ref,
        "candidate_ref_path_in_current_source": ref_path,
        "candidate_layer_class": layer,
        "candidate_score": score,
        "score_reasons": reasons,
        "score_penalties": penalties,
        "source_file_resolves": p is not None,
        "source_json_readable": source_json_readable,
        "source_content_signals": source_content_signals,
        "source_contains_field_key": source_contains_field_key,
        "source_contains_row_uid": source_contains_row_uid,
        "source_contains_slot_id": source_contains_slot_id,
        "source_contains_rows_key": source_contains_rows_key,
        "review_status": "CANDIDATE_REVIEWED_NOT_APPLIED",
        "authorized_to_rebind": False,
    }

def review_per_binding(broken: List[Dict[str, Any]], candidates: List[Dict[str, Any]], slots: Dict[str, Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    candidates_by_slot: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for c in candidates:
        if c.get("slot_id"):
            candidates_by_slot[str(c["slot_id"])].append(c)

    scored_all: List[Dict[str, Any]] = []
    per_binding: List[Dict[str, Any]] = []
    unique_proposals: List[Dict[str, Any]] = []
    tie_records: List[Dict[str, Any]] = []

    for b in broken:
        slot_id = str(b.get("slot_id"))
        slot = slots.get(slot_id, {})
        scored = [score_candidate(c, b, slot) for c in candidates_by_slot.get(slot_id, [])]
        scored.sort(key=lambda x: (-int(x["candidate_score"]), str(x["candidate_source_ref"])))
        scored_all.extend(scored)

        top_score = scored[0]["candidate_score"] if scored else None
        top = [s for s in scored if s["candidate_score"] == top_score] if scored else []
        candidate_count = len(scored)

        if candidate_count == 0:
            review_status = "NO_REBIND_CANDIDATES_FOR_BINDING"
            selected = None
            ambiguity = "no candidates"
        elif top_score is None or top_score <= 0:
            review_status = "REBIND_CANDIDATES_HAVE_NO_POSITIVE_SCORE"
            selected = None
            ambiguity = "no positive candidate"
        elif len(top) == 1:
            review_status = "UNIQUE_TOP_REBIND_CANDIDATE_FOR_REVIEW"
            selected = top[0]
            ambiguity = None
            unique_proposals.append({
                "proposal_id": "source_ref_rebind_proposal_" + sha8({"slot_id": slot_id, "candidate": top[0]}),
                "slot_id": slot_id,
                "row_uid": b.get("row_uid"),
                "field": b.get("field"),
                "current_row_source_ref": b.get("current_row_source_ref"),
                "current_row_json_path": b.get("current_row_json_path"),
                "proposed_row_source_ref": top[0].get("candidate_source_ref"),
                "proposal_score": top_score,
                "proposal_reasons": top[0].get("score_reasons", []),
                "proposal_penalties": top[0].get("score_penalties", []),
                "proposal_status": "PROPOSED_FOR_REVIEW_NOT_APPLIED",
                "authorized_to_apply": False,
            })
        else:
            review_status = "MULTIPLE_TOP_REBIND_CANDIDATES_TIED"
            selected = None
            ambiguity = "multiple top candidates"
            tie_records.append({
                "slot_id": slot_id,
                "row_uid": b.get("row_uid"),
                "field": b.get("field"),
                "top_score": top_score,
                "tied_candidate_count": len(top),
                "tied_candidates": [
                    {
                        "candidate_id": t.get("candidate_id"),
                        "candidate_source_ref": t.get("candidate_source_ref"),
                        "candidate_ref_path_in_current_source": t.get("candidate_ref_path_in_current_source"),
                        "candidate_layer_class": t.get("candidate_layer_class"),
                        "score_reasons": t.get("score_reasons"),
                        "score_penalties": t.get("score_penalties"),
                    }
                    for t in top
                ],
                "tie_status": "REQUIRES_NARROWER_SOURCE_REF_REBIND_DOMINANCE_OR_SOURCE_ROW_LOCATOR",
            })

        per_binding.append({
            "slot_id": slot_id,
            "row_uid": b.get("row_uid"),
            "field": b.get("field"),
            "current_row_source_ref": b.get("current_row_source_ref"),
            "current_row_json_path": b.get("current_row_json_path"),
            "candidate_count": candidate_count,
            "top_score": top_score,
            "top_candidate_count": len(top) if scored else 0,
            "review_status": review_status,
            "ambiguity": ambiguity,
            "unique_candidate_source_ref": selected.get("candidate_source_ref") if selected else None,
            "authorized_to_rebind": False,
            "safe_next_action": "review unique proposals before application" if selected else "narrow source-ref rebind candidates before application",
        })

    return scored_all, per_binding, unique_proposals, tie_records

def decide(per_binding: List[Dict[str, Any]], unique_proposals: List[Dict[str, Any]], tie_records: List[Dict[str, Any]]) -> Tuple[str, List[str], str]:
    status_counts = Counter(r["review_status"] for r in per_binding)
    reason_codes = [
        "SOURCE_REF_REBIND_CANDIDATES_REVIEWED",
        "CANDIDATE_SCORE_TABLE_EMITTED",
        "PER_BINDING_REVIEW_EMITTED",
        "NO_REBINDS_APPLIED",
        "NO_VALUES_AUTHORIZED_OR_APPLIED",
        "NO_METADATA_POPULATION",
    ]

    if len(unique_proposals) == len(per_binding) and per_binding:
        reason_codes.append("UNIQUE_REBIND_PROPOSALS_AVAILABLE_FOR_ALL_BINDINGS")
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_REVIEWED_UNIQUE_PROPOSALS_READY_FOR_REVIEW"
        next_edge = "REVIEW_OR_APPLY_MACHINE_READABLE_SOURCE_REF_REBIND_PROPOSALS_V0"
    elif unique_proposals:
        reason_codes.append("PARTIAL_UNIQUE_REBIND_PROPOSALS_AVAILABLE")
        reason_codes.append("SOME_REBIND_CANDIDATES_STILL_AMBIGUOUS")
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_REVIEWED_PARTIAL_UNIQUE_PARTIAL_AMBIGUOUS"
        next_edge = "NARROW_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_V0"
    elif tie_records:
        reason_codes.append("SOURCE_REF_REBIND_CANDIDATES_TIED")
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_REVIEWED_AMBIGUOUS_TIED_CANDIDATES"
        next_edge = "NARROW_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_V0"
    else:
        reason_codes.append("NO_LAWFUL_REBIND_PROPOSALS_AFTER_REVIEW")
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_REVIEWED_NO_LAWFUL_PROPOSALS"
        next_edge = "BUILD_MACHINE_READABLE_SOURCE_ROW_LOCATOR_SURFACE_V0"

    return status, reason_codes, next_edge

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_ref_rebind_review_authority_boundary_v0",
        "status": status,
        "may_review_rebind_candidates": True,
        "may_score_candidates": True,
        "may_emit_unique_rebind_proposals": True,
        "may_emit_tie_records": True,
        "may_apply_rebinds": False,
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

def rollup_obj(status: str, scored: List[Dict[str, Any]], per_binding: List[Dict[str, Any]], unique: List[Dict[str, Any]], ties: List[Dict[str, Any]], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_ref_rebind_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "broken_binding_count": len(per_binding),
        "source_ref_rebind_candidate_count": len(scored),
        "unique_rebind_proposal_count": len(unique),
        "ambiguous_rebind_binding_count": len(ties),
        "per_binding_review_status_counts": dict(Counter(r["review_status"] for r in per_binding)),
        "candidate_layer_counts": dict(Counter(r["candidate_layer_class"] for r in scored)),
        "candidate_positive_score_count": sum(1 for r in scored if int(r.get("candidate_score") or 0) > 0),
        "candidate_source_file_resolves_count": sum(1 for r in scored if r.get("source_file_resolves") is True),
        "candidate_source_json_readable_count": sum(1 for r in scored if r.get("source_json_readable") is True),
        "rebinds_applied_count": 0,
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
        "rebinds_applied_count",
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
        "schema_version": "typed_machine_readable_source_ref_rebind_review_profile_v0",
        "profile_id": "source_ref_rebind_review_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "review_completed": True,
        "rebinds_applied": False,
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
        "schema_version": "typed_machine_readable_source_ref_rebind_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The refinement surface found 168 source-ref rebind candidates for 21 broken bindings; this unit reviews/scored candidates without applying rebinds or values.",
        "broken_binding_count": roll["broken_binding_count"],
        "source_ref_rebind_candidate_count": roll["source_ref_rebind_candidate_count"],
        "unique_rebind_proposal_count": roll["unique_rebind_proposal_count"],
        "ambiguous_rebind_binding_count": roll["ambiguous_rebind_binding_count"],
        "per_binding_review_status_counts": roll["per_binding_review_status_counts"],
        "candidate_layer_counts": roll["candidate_layer_counts"],
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "rebinds_applied_count": 0,
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
        "schema_version": "typed_machine_readable_source_ref_rebind_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_source_ref_rebind_candidates",
                "question": "are any candidate source refs uniquely reviewable for each binding",
                "answer": "review candidate scores and ties without applying rebinds",
                "taken": "score and classify candidates",
            },
            {
                "step": "classify_rebind_review_result",
                "question": "can rebind proposals advance to review/application boundary",
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
        broken, candidates, slots = [], [], {}
        scored, per_binding, unique, ties = [], [], [], []
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_REVIEW_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_MACHINE_READABLE_SOURCE_REF_REBIND_REVIEW_BASIS_V0"
    else:
        broken, candidates, slots = load_records()
        scored, per_binding, unique, ties = review_per_binding(broken, candidates, slots)
        status, reason_codes, next_edge = decide(per_binding, unique, ties)

    roll = rollup_obj(status, scored, per_binding, unique, ties, next_edge)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, roll, next_edge)
    boundary = authority_boundary_obj(status)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    review_surface = {
        "schema_version": "typed_machine_readable_source_ref_rebind_review_surface_v0",
        "surface_status": status,
        "source_refinement_receipt_id": SOURCE_REFINEMENT_RECEIPT_ID,
        "broken_binding_count": roll["broken_binding_count"],
        "source_ref_rebind_candidate_count": roll["source_ref_rebind_candidate_count"],
        "unique_rebind_proposal_count": roll["unique_rebind_proposal_count"],
        "ambiguous_rebind_binding_count": roll["ambiguous_rebind_binding_count"],
        "review_claim": "Source-ref rebind candidates were scored and classified without applying any rebind.",
        "candidate_score_table_ref": rel(CANDIDATE_SCORE_TABLE_PATH),
        "per_binding_review_ref": rel(PER_BINDING_REVIEW_TABLE_PATH),
        "unique_rebind_proposals_ref": rel(UNIQUE_REBIND_PROPOSALS_PATH),
        "candidate_tie_table_ref": rel(CANDIDATE_TIE_TABLE_PATH),
        "recommended_next": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    decision_options = {
        "schema_version": "typed_machine_readable_source_ref_rebind_review_decision_options_v0",
        "decision_options_status": "SOURCE_REF_REBIND_REVIEW_DECISION_OPTIONS_EMITTED",
        "safe_options": [
            {
                "option": "REVIEW_OR_APPLY_UNIQUE_REBIND_PROPOSALS",
                "recommended": next_edge == "REVIEW_OR_APPLY_MACHINE_READABLE_SOURCE_REF_REBIND_PROPOSALS_V0",
                "next_unit": "REVIEW_OR_APPLY_MACHINE_READABLE_SOURCE_REF_REBIND_PROPOSALS_V0",
                "meaning": "Only lawful if every broken binding has a unique top rebind proposal.",
            },
            {
                "option": "NARROW_SOURCE_REF_REBIND_CANDIDATES",
                "recommended": next_edge == "NARROW_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_V0",
                "next_unit": "NARROW_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_V0",
                "meaning": "Use a bounded dominance/narrowing surface when candidates remain tied or partially ambiguous.",
            },
            {
                "option": "BUILD_SOURCE_ROW_LOCATOR_SURFACE",
                "recommended": next_edge == "BUILD_MACHINE_READABLE_SOURCE_ROW_LOCATOR_SURFACE_V0",
                "next_unit": "BUILD_MACHINE_READABLE_SOURCE_ROW_LOCATOR_SURFACE_V0",
                "meaning": "Use when no lawful rebind proposals survive review.",
            },
            {
                "option": "FREEZE_AS_DIAGNOSTIC_REFERENCE",
                "recommended": False,
                "next_unit": "FREEZE_MACHINE_READABLE_SOURCE_REF_REBIND_REVIEW_V0",
                "meaning": "Freeze this review as reference only.",
            },
        ],
        "forbidden_shortcuts": [
            "apply source ref rebinds in review unit",
            "treat candidate score as authorization",
            "extract or apply values",
            "metadata population",
            "discriminator readiness",
            "rule refinement",
            "tie break",
            "target selection",
            "runtime patch",
        ],
    }

    narrowing_contract = {
        "schema_version": "typed_machine_readable_source_ref_rebind_narrowing_contract_v0",
        "contract_status": "SOURCE_REF_REBIND_NARROWING_CONTRACT_EMITTED",
        "source_rebind_review_status": status,
        "required_inputs_for_next_unit": [
            "candidate score table",
            "per-binding review table",
            "candidate tie table",
            "unique proposal table",
            "broken binding table",
        ],
        "recommended_next_unit": next_edge,
        "must_not": [
            "apply rebinds before review/application boundary",
            "infer values from candidate refs",
            "populate metadata",
            "mark discriminator ready",
            "select runtime patch target",
        ],
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    classification = {
        "schema_version": "typed_machine_readable_source_ref_rebind_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "broken_binding_count": roll["broken_binding_count"],
        "source_ref_rebind_candidate_count": roll["source_ref_rebind_candidate_count"],
        "unique_rebind_proposal_count": roll["unique_rebind_proposal_count"],
        "ambiguous_rebind_binding_count": roll["ambiguous_rebind_binding_count"],
        "per_binding_review_status_counts": roll["per_binding_review_status_counts"],
        "candidate_layer_counts": roll["candidate_layer_counts"],
        "rebinds_applied": False,
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

    write_json(REVIEW_SURFACE_PATH, review_surface)
    write_json(CANDIDATE_SCORE_TABLE_PATH, {
        "schema_version": "typed_machine_readable_source_ref_rebind_candidate_score_table_v0",
        "score_table_status": "SOURCE_REF_REBIND_CANDIDATES_SCORED_NOT_APPLIED",
        "candidate_count": len(scored),
        "records": scored,
    })
    write_json(PER_BINDING_REVIEW_TABLE_PATH, {
        "schema_version": "typed_machine_readable_source_ref_rebind_per_binding_review_v0",
        "review_status": "SOURCE_REF_REBIND_PER_BINDING_REVIEW_EMITTED",
        "binding_count": len(per_binding),
        "records": per_binding,
    })
    write_json(CANDIDATE_TIE_TABLE_PATH, {
        "schema_version": "typed_machine_readable_source_ref_rebind_candidate_tie_table_v0",
        "tie_table_status": "SOURCE_REF_REBIND_TIES_EMITTED",
        "tie_binding_count": len(ties),
        "records": ties,
    })
    write_json(UNIQUE_REBIND_PROPOSALS_PATH, {
        "schema_version": "typed_machine_readable_unique_source_ref_rebind_proposals_v0",
        "proposal_status": "UNIQUE_REBIND_PROPOSALS_EMITTED_NOT_APPLIED",
        "proposal_count": len(unique),
        "records": unique,
    })
    write_json(AMBIGUOUS_REBIND_REASONS_PATH, {
        "schema_version": "typed_machine_readable_ambiguous_source_ref_rebind_reasons_v0",
        "ambiguous_status": "AMBIGUOUS_REBINDS_EMITTED",
        "ambiguous_binding_count": len(ties),
        "records": [
            {
                "slot_id": t.get("slot_id"),
                "row_uid": t.get("row_uid"),
                "field": t.get("field"),
                "top_score": t.get("top_score"),
                "tied_candidate_count": t.get("tied_candidate_count"),
                "reason": "multiple top source-ref candidates have equal score",
                "safe_next_action": "narrow source-ref rebind candidates before application",
            }
            for t in ties
        ],
    })
    write_json(REVIEW_DECISION_OPTIONS_PATH, decision_options)
    write_json(NEXT_SURFACE_CONTRACT_PATH, narrowing_contract)
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
        "REBIND_REVIEW_0_REFINEMENT_RECEIPT_CONSUMED": SOURCE_REFINEMENT_RECEIPT_PATH.exists(),
        "REBIND_REVIEW_1_CANDIDATE_TABLE_CONSUMED": SOURCE_SOURCE_REF_REBIND_CANDIDATE_TABLE_PATH.exists(),
        "REBIND_REVIEW_2_REVIEW_SURFACE_EMITTED": REVIEW_SURFACE_PATH.exists(),
        "REBIND_REVIEW_3_CANDIDATE_SCORE_TABLE_EMITTED": CANDIDATE_SCORE_TABLE_PATH.exists(),
        "REBIND_REVIEW_4_PER_BINDING_REVIEW_EMITTED": PER_BINDING_REVIEW_TABLE_PATH.exists(),
        "REBIND_REVIEW_5_TIE_TABLE_EMITTED": CANDIDATE_TIE_TABLE_PATH.exists(),
        "REBIND_REVIEW_6_UNIQUE_PROPOSALS_EMITTED": UNIQUE_REBIND_PROPOSALS_PATH.exists(),
        "REBIND_REVIEW_7_AMBIGUOUS_REASONS_EMITTED": AMBIGUOUS_REBIND_REASONS_PATH.exists(),
        "REBIND_REVIEW_8_DECISION_OPTIONS_EMITTED": REVIEW_DECISION_OPTIONS_PATH.exists(),
        "REBIND_REVIEW_9_NEXT_SURFACE_CONTRACT_EMITTED": NEXT_SURFACE_CONTRACT_PATH.exists(),
        "REBIND_REVIEW_10_NO_REBINDS_APPLIED": roll["rebinds_applied_count"] == 0,
        "REBIND_REVIEW_11_NO_REFINEMENTS_APPLIED": roll["refinements_applied_count"] == 0,
        "REBIND_REVIEW_12_NO_VALUES_AUTHORIZED": roll["values_authorized_count"] == 0,
        "REBIND_REVIEW_13_NO_VALUES_APPLIED": roll["values_applied_count"] == 0,
        "REBIND_REVIEW_14_NO_NULL_REASONS_ACCEPTED": roll["null_reason_accepted_count"] == 0,
        "REBIND_REVIEW_15_NO_SOURCE_PACKET_MATERIALIZED": roll["source_packet_materialized_for_review_count"] == 0,
        "REBIND_REVIEW_16_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "REBIND_REVIEW_17_NO_DISCRIMINATOR_READY": roll["ready_discriminator_count"] == 0,
        "REBIND_REVIEW_18_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "REBIND_REVIEW_19_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "REBIND_REVIEW_20_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "REBIND_REVIEW_21_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classification["target_candidate_declared_for_review"] is False,
        "REBIND_REVIEW_22_NO_TARGET_SELECTED_FOR_BUILD": classification["target_selected_for_build"] is False,
        "REBIND_REVIEW_23_NO_ACCEPTED_FOR_BUILD": classification["accepted_for_build"] is False,
        "REBIND_REVIEW_24_NO_RUNTIME_PATCH": classification["runtime_patch_authorized"] is False,
        "REBIND_REVIEW_25_NO_TARGET_FILE_MODIFICATION": classification["target_file_modification_authorized"] is False,
        "REBIND_REVIEW_26_NO_C5_OPENED": classification["c5_authorized"] is False,
        "REBIND_REVIEW_27_NO_GENERAL_CELL1_AUTHORITY": classification["general_cell1_authority_granted"] is False,
        "REBIND_REVIEW_28_NO_LATEST_FILE_GUESSING": classification["latest_file_guessing"] is False,
        "REBIND_REVIEW_29_NO_MTIME_SELECTION": classification["mtime_selection"] is False,
        "REBIND_REVIEW_30_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "REBIND_REVIEW_31_ACCEPTANCE_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "REBIND_REVIEW_32_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "broken_bindings": roll["broken_binding_count"],
        "candidates": roll["source_ref_rebind_candidate_count"],
        "unique": roll["unique_rebind_proposal_count"],
        "ambiguous": roll["ambiguous_rebind_binding_count"],
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_source_ref_rebind_review_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_refinement_receipt_id": SOURCE_REFINEMENT_RECEIPT_ID,
        "machine_readable_source_ref_rebind_review_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "broken_binding_count": roll["broken_binding_count"],
            "source_ref_rebind_candidate_count": roll["source_ref_rebind_candidate_count"],
            "unique_rebind_proposal_count": roll["unique_rebind_proposal_count"],
            "ambiguous_rebind_binding_count": roll["ambiguous_rebind_binding_count"],
            "per_binding_review_status_counts": roll["per_binding_review_status_counts"],
            "candidate_layer_counts": roll["candidate_layer_counts"],
            "candidate_positive_score_count": roll["candidate_positive_score_count"],
            "candidate_source_file_resolves_count": roll["candidate_source_file_resolves_count"],
            "candidate_source_json_readable_count": roll["candidate_source_json_readable_count"],
            "rebinds_applied": False,
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
            "review_surface": rel(REVIEW_SURFACE_PATH),
            "candidate_score_table": rel(CANDIDATE_SCORE_TABLE_PATH),
            "per_binding_review_table": rel(PER_BINDING_REVIEW_TABLE_PATH),
            "candidate_tie_table": rel(CANDIDATE_TIE_TABLE_PATH),
            "unique_rebind_proposals": rel(UNIQUE_REBIND_PROPOSALS_PATH),
            "ambiguous_rebind_reasons": rel(AMBIGUOUS_REBIND_REASONS_PATH),
            "review_decision_options": rel(REVIEW_DECISION_OPTIONS_PATH),
            "next_surface_contract": rel(NEXT_SURFACE_CONTRACT_PATH),
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
    print(f"source_ref_rebind_review_receipt_id={receipt_id}")
    print(f"source_ref_rebind_review_receipt_path={rel(receipt_path)}")
    print(f"source_ref_rebind_review_surface_path={rel(REVIEW_SURFACE_PATH)}")
    print(f"candidate_score_table_path={rel(CANDIDATE_SCORE_TABLE_PATH)}")
    print(f"per_binding_review_table_path={rel(PER_BINDING_REVIEW_TABLE_PATH)}")
    print(f"candidate_tie_table_path={rel(CANDIDATE_TIE_TABLE_PATH)}")
    print(f"unique_rebind_proposals_path={rel(UNIQUE_REBIND_PROPOSALS_PATH)}")
    print(f"ambiguous_rebind_reasons_path={rel(AMBIGUOUS_REBIND_REASONS_PATH)}")
    print(f"source_ref_rebind_review_decision_options_path={rel(REVIEW_DECISION_OPTIONS_PATH)}")
    print(f"source_ref_rebind_next_surface_contract_path={rel(NEXT_SURFACE_CONTRACT_PATH)}")
    print(f"source_ref_rebind_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"source_ref_rebind_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
