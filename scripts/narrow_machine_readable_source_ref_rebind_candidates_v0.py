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

UNIT_ID = "NARROW_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_REF_REBIND_NARROWING"
MODE = "SOURCE_REF_REBIND_NARROWING / NO_REBIND_APPLIED / NO_VALUE_AUTHORIZATION / NO_METADATA_FILL / NO_TIE_BREAK / NO_ACCEPTANCE"
BUILD_MODE = "SOURCE_REF_REBIND_NARROWING_SURFACE_ONLY"

SOURCE_REBIND_REVIEW_RECEIPT_ID = "c7a8616a"
SOURCE_REBIND_REVIEW_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_review_v0_receipts/c7a8616a.json"
SOURCE_REBIND_REVIEW_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_review_v0/typed_machine_readable_source_ref_rebind_review_surface_v0.json"
SOURCE_CANDIDATE_SCORE_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_review_v0/typed_machine_readable_source_ref_rebind_candidate_score_table_v0.json"
SOURCE_PER_BINDING_REVIEW_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_review_v0/typed_machine_readable_source_ref_rebind_per_binding_review_v0.json"
SOURCE_CANDIDATE_TIE_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_review_v0/typed_machine_readable_source_ref_rebind_candidate_tie_table_v0.json"
SOURCE_UNIQUE_REBIND_PROPOSALS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_review_v0/typed_machine_readable_unique_source_ref_rebind_proposals_v0.json"
SOURCE_AMBIGUOUS_REBIND_REASONS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_review_v0/typed_machine_readable_ambiguous_source_ref_rebind_reasons_v0.json"
SOURCE_REBIND_REVIEW_DECISION_OPTIONS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_review_v0/typed_machine_readable_source_ref_rebind_review_decision_options_v0.json"
SOURCE_REBIND_NARROWING_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_review_v0/typed_machine_readable_source_ref_rebind_narrowing_contract_v0.json"
SOURCE_REBIND_REVIEW_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_review_v0/typed_machine_readable_source_ref_rebind_review_classification_v0.json"
SOURCE_REBIND_REVIEW_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_review_v0/typed_machine_readable_source_ref_rebind_review_rollup_v0.json"
SOURCE_REBIND_REVIEW_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_review_v0/typed_machine_readable_source_ref_rebind_review_profile_v0.json"

SOURCE_BROKEN_BINDING_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_row_path_refinement_v0/typed_machine_readable_broken_row_binding_table_v0.json"
SOURCE_MACHINE_SOURCE_SLOTS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_machine_source_slots_v0.json"
SOURCE_FIELD_POLICY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_source_field_policy_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing_v0_receipts"

NARROWING_SURFACE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_narrowing_surface_v0.json"
DOMINANCE_FEATURE_MATRIX_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_dominance_feature_matrix_v0.json"
PER_BINDING_NARROWING_TABLE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_per_binding_narrowing_v0.json"
NARROWED_REBIND_PROPOSALS_PATH = OUT_DIR / "typed_machine_readable_narrowed_source_ref_rebind_proposals_v0.json"
RESIDUAL_TIE_TABLE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_residual_tie_table_v0.json"
DOMINANCE_RULE_CANDIDATES_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_dominance_rule_candidates_v0.json"
NARROWING_REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_narrowing_review_packet_v0.json"
NEXT_APPLICATION_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_application_contract_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_narrowing_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_narrowing_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_narrowing_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_narrowing_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_narrowing_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_narrowing_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_REBIND_REVIEW_RECEIPT_PATH,
    SOURCE_REBIND_REVIEW_SURFACE_PATH,
    SOURCE_CANDIDATE_SCORE_TABLE_PATH,
    SOURCE_PER_BINDING_REVIEW_TABLE_PATH,
    SOURCE_CANDIDATE_TIE_TABLE_PATH,
    SOURCE_UNIQUE_REBIND_PROPOSALS_PATH,
    SOURCE_AMBIGUOUS_REBIND_REASONS_PATH,
    SOURCE_REBIND_REVIEW_DECISION_OPTIONS_PATH,
    SOURCE_REBIND_NARROWING_CONTRACT_PATH,
    SOURCE_REBIND_REVIEW_CLASSIFICATION_PATH,
    SOURCE_REBIND_REVIEW_ROLLUP_PATH,
    SOURCE_REBIND_REVIEW_PROFILE_PATH,
    SOURCE_BROKEN_BINDING_TABLE_PATH,
    SOURCE_MACHINE_SOURCE_SLOTS_PATH,
    SOURCE_FIELD_POLICY_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_REVIEWED_AMBIGUOUS_TIED_CANDIDATES"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_REVIEWED_AMBIGUOUS_TIED_CANDIDATES"
EXPECTED_NEXT = "NARROW_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_V0"

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

    receipt = read_json(SOURCE_REBIND_REVIEW_RECEIPT_PATH)
    summary = receipt.get("machine_readable_source_ref_rebind_review_summary", {})
    score = read_json(SOURCE_CANDIDATE_SCORE_TABLE_PATH)
    per = read_json(SOURCE_PER_BINDING_REVIEW_TABLE_PATH)
    ties = read_json(SOURCE_CANDIDATE_TIE_TABLE_PATH)
    unique = read_json(SOURCE_UNIQUE_REBIND_PROPOSALS_PATH)
    classif = read_json(SOURCE_REBIND_REVIEW_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_REBIND_REVIEW_ROLLUP_PATH)
    profile = read_json(SOURCE_REBIND_REVIEW_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_REBIND_REVIEW_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("rebind_review_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"rebind_review_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("rebind_review_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"rebind_review_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("broken_binding_count") != 21:
        failures.append("broken_binding_count_not_21")
    if summary.get("source_ref_rebind_candidate_count") != 168:
        failures.append(f"source_ref_candidate_count_not_168:{summary.get('source_ref_rebind_candidate_count')}")
    if summary.get("unique_rebind_proposal_count") != 0:
        failures.append("unique_rebind_proposal_count_nonzero")
    if summary.get("ambiguous_rebind_binding_count") != 21:
        failures.append("ambiguous_rebind_binding_count_not_21")
    if summary.get("per_binding_review_status_counts", {}).get("MULTIPLE_TOP_REBIND_CANDIDATES_TIED") != 21:
        failures.append("tie_binding_count_not_21")
    if summary.get("candidate_positive_score_count") != 168:
        failures.append("candidate_positive_score_count_not_168")
    if summary.get("candidate_source_file_resolves_count") != 168:
        failures.append("candidate_source_file_resolves_count_not_168")
    if summary.get("candidate_source_json_readable_count") != 168:
        failures.append("candidate_source_json_readable_count_not_168")
    if summary.get("rebinds_applied") is not False:
        failures.append("rebinds_applied_unexpectedly")
    if summary.get("values_authorized") is not False:
        failures.append("values_authorized_unexpectedly")
    if summary.get("metadata_populated") is not False:
        failures.append("metadata_populated_unexpectedly")
    if summary.get("ready_discriminator_count") != 0:
        failures.append("ready_discriminator_nonzero")

    if score.get("candidate_count") != 168:
        failures.append("score_table_count_not_168")
    if per.get("binding_count") != 21:
        failures.append("per_binding_count_not_21")
    if ties.get("tie_binding_count") != 21:
        failures.append("tie_table_count_not_21")
    if unique.get("proposal_count") != 0:
        failures.append("unique_proposal_table_nonzero")
    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("rebind_review_classification_status_wrong")
    if roll.get("metadata_populated_count") != 0:
        failures.append("rebind_review_rollup_metadata_populated_nonzero")
    if profile.get("metadata_populated") is not False:
        failures.append("rebind_review_profile_metadata_populated_true")

    return failures

def load_records() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    scored = [r for r in read_json(SOURCE_CANDIDATE_SCORE_TABLE_PATH).get("records", []) if isinstance(r, dict)]
    per_binding = [r for r in read_json(SOURCE_PER_BINDING_REVIEW_TABLE_PATH).get("records", []) if isinstance(r, dict)]
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
    return scored, per_binding, broken, slots

def basename_tokens(path: str) -> List[str]:
    name = Path(path).name if path else ""
    stem = name[:-5] if name.endswith(".json") else Path(name).stem
    return [t for t in re.split(r"[^A-Za-z0-9]+", stem.lower()) if t]

def field_policy_by_field() -> Dict[str, Dict[str, Any]]:
    policy = read_json(SOURCE_FIELD_POLICY_PATH)
    out = {}
    for p in policy.get("field_policies", []):
        if isinstance(p, dict) and p.get("field"):
            out[str(p["field"])] = p
    return out

def source_introspection(candidate: Dict[str, Any]) -> Dict[str, Any]:
    ref = candidate.get("candidate_source_ref")
    p = source_path_from_ref(ref)
    data = {
        "json_readable": False,
        "top_keys": [],
        "schema_version": None,
        "record_count": None,
        "slot_count": None,
        "row_count": None,
        "path_count": None,
    }
    if p is None:
        return data
    try:
        obj = read_json(p)
    except Exception:
        return data
    data["json_readable"] = True
    if isinstance(obj, dict):
        data["top_keys"] = sorted([str(k) for k in obj.keys()])[:50]
        data["schema_version"] = obj.get("schema_version")
        for key in ["records", "slots", "rows", "propositions", "field_policies", "attempts"]:
            val = obj.get(key)
            if isinstance(val, list):
                data[f"{key}_count"] = len(val)
        flat = flatten_json(obj)
        data["path_count"] = len(flat)
    return data

def dominance_features(candidate: Dict[str, Any], binding: Dict[str, Any], slot: Dict[str, Any], policies: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    field = str(candidate.get("field") or binding.get("field") or slot.get("field") or "")
    slot_id = str(candidate.get("slot_id") or binding.get("slot_id") or slot.get("slot_id") or "")
    row_uid = str(candidate.get("row_uid") or binding.get("row_uid") or slot.get("row_uid") or "")
    ref = str(candidate.get("candidate_source_ref") or "")
    ref_path = str(candidate.get("candidate_ref_path_in_current_source") or "")
    tokens = set(basename_tokens(ref))
    policy = policies.get(field, {})
    introspect = source_introspection(candidate)

    features: Dict[str, Any] = {
        "candidate_id": candidate.get("candidate_id"),
        "slot_id": slot_id,
        "row_uid": row_uid,
        "field": field,
        "candidate_source_ref": ref,
        "candidate_ref_path_in_current_source": ref_path,
        "base_review_score": int(candidate.get("candidate_score") or 0),
        "candidate_layer_class": candidate.get("candidate_layer_class"),
        "source_file_resolves": candidate.get("source_file_resolves") is True,
        "source_json_readable": candidate.get("source_json_readable") is True,
        "source_contains_field_key": candidate.get("source_contains_field_key") is True,
        "source_contains_row_uid": candidate.get("source_contains_row_uid") is True,
        "source_contains_slot_id": candidate.get("source_contains_slot_id") is True,
        "source_contains_rows_key": candidate.get("source_contains_rows_key") is True,
        "source_schema_version": introspect.get("schema_version"),
        "source_top_keys": introspect.get("top_keys"),
        "source_path_count": introspect.get("path_count"),
        "records_count": introspect.get("records_count"),
        "slots_count": introspect.get("slots_count"),
        "rows_count": introspect.get("rows_count"),
        "field_policies_count": introspect.get("field_policies_count"),
        "attempts_count": introspect.get("attempts_count"),
        "filename_contains_field": field.lower() in tokens,
        "filename_contains_slot": slot_id.lower() in tokens,
        "filename_contains_row_uid": row_uid.lower() in tokens,
        "filename_contains_machine": "machine" in tokens or "machine_readable" in ref,
        "filename_contains_source": "source" in tokens or "source" in ref,
        "filename_contains_packet": "packet" in tokens or "packet" in ref,
        "filename_contains_repair": "repair" in tokens or "repair" in ref,
        "filename_contains_review": "review" in tokens or "review" in ref,
        "filename_contains_candidate": "candidate" in tokens or "candidate" in ref,
        "filename_contains_policy": "policy" in tokens or "policy" in ref,
        "ref_path_contains_current_field": field in ref_path,
        "ref_path_contains_source_ref": "source_ref" in ref_path,
        "ref_path_contains_candidate_source_ref": "candidate_source_ref" in ref_path,
        "policy_source_class": policy.get("source_class"),
        "policy_required_source_object": policy.get("required_source_object") or policy.get("source_object"),
        "policy_mentions_candidate_ref": False,
    }

    policy_text = json.dumps(policy, sort_keys=True)
    if ref and ref in policy_text:
        features["policy_mentions_candidate_ref"] = True

    score = 0
    reasons: List[str] = []
    penalties: List[str] = []

    # v0 dominance: prefer candidate refs that are direct source/packet artifacts, not review/repair/candidate artifacts.
    if features["source_file_resolves"] and features["source_json_readable"]:
        score += 20
        reasons.append("candidate_resolves_and_json_readable")
    if features["filename_contains_source"]:
        score += 12
        reasons.append("filename_contains_source")
    if features["filename_contains_packet"]:
        score += 10
        reasons.append("filename_contains_packet")
    if features["filename_contains_machine"]:
        score += 5
        reasons.append("filename_contains_machine")
    if features["source_contains_field_key"]:
        score += 20
        reasons.append("source_contains_exact_field_key")
    if features["source_contains_row_uid"]:
        score += 20
        reasons.append("source_contains_row_uid")
    if features["source_contains_slot_id"]:
        score += 10
        reasons.append("source_contains_slot_id")
    if features["source_contains_rows_key"]:
        score += 5
        reasons.append("source_contains_row_like_key")
    if features["filename_contains_field"]:
        score += 8
        reasons.append("filename_contains_field")
    if features["filename_contains_slot"]:
        score += 6
        reasons.append("filename_contains_slot")
    if features["filename_contains_row_uid"]:
        score += 6
        reasons.append("filename_contains_row_uid")
    if features["policy_mentions_candidate_ref"]:
        score += 30
        reasons.append("field_policy_mentions_candidate_ref")

    if features["filename_contains_repair"]:
        score -= 8
        penalties.append("filename_contains_repair")
    if features["filename_contains_review"]:
        score -= 12
        penalties.append("filename_contains_review")
    if features["filename_contains_candidate"]:
        score -= 8
        penalties.append("filename_contains_candidate")
    if features["filename_contains_policy"]:
        score -= 4
        penalties.append("filename_contains_policy")

    # Stable tie-breaker is deliberately NOT used as a dominance feature. If all semantic features tie, stay tied.
    features["narrowing_score"] = max(score, 0)
    features["narrowing_reasons"] = reasons
    features["narrowing_penalties"] = penalties
    features["narrowing_status"] = "NARROWING_FEATURES_COMPUTED_NOT_APPLIED"
    features["authorized_to_rebind"] = False
    return features

def narrow_per_binding(features: List[Dict[str, Any]], per_binding: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    by_slot: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for f in features:
        by_slot[str(f.get("slot_id"))].append(f)

    narrowed: List[Dict[str, Any]] = []
    residual_ties: List[Dict[str, Any]] = []
    rule_candidates: List[Dict[str, Any]] = []
    per_rows: List[Dict[str, Any]] = []

    for b in per_binding:
        slot_id = str(b.get("slot_id"))
        rows = sorted(by_slot.get(slot_id, []), key=lambda r: (-int(r.get("narrowing_score") or 0), str(r.get("candidate_source_ref"))))
        if not rows:
            status = "NO_CANDIDATES_TO_NARROW"
            top = []
            top_score = None
        else:
            top_score = rows[0]["narrowing_score"]
            top = [r for r in rows if r.get("narrowing_score") == top_score]

            if top_score and len(top) == 1:
                status = "UNIQUE_NARROWED_REBIND_PROPOSAL"
                chosen = top[0]
                narrowed.append({
                    "proposal_id": "narrowed_source_ref_rebind_" + sha8({"slot_id": slot_id, "candidate": chosen}),
                    "slot_id": slot_id,
                    "row_uid": chosen.get("row_uid"),
                    "field": chosen.get("field"),
                    "current_row_source_ref": b.get("current_row_source_ref"),
                    "current_row_json_path": b.get("current_row_json_path"),
                    "proposed_row_source_ref": chosen.get("candidate_source_ref"),
                    "narrowing_score": chosen.get("narrowing_score"),
                    "narrowing_reasons": chosen.get("narrowing_reasons"),
                    "narrowing_penalties": chosen.get("narrowing_penalties"),
                    "proposal_status": "NARROWED_REBIND_PROPOSAL_NOT_APPLIED",
                    "authorized_to_apply": False,
                })
            elif rows and len(top) > 1:
                status = "RESIDUAL_TOP_CANDIDATES_TIED"
                residual_ties.append({
                    "slot_id": slot_id,
                    "row_uid": b.get("row_uid"),
                    "field": b.get("field"),
                    "top_score": top_score,
                    "tied_candidate_count": len(top),
                    "tied_candidates": [
                        {
                            "candidate_id": t.get("candidate_id"),
                            "candidate_source_ref": t.get("candidate_source_ref"),
                            "narrowing_reasons": t.get("narrowing_reasons"),
                            "narrowing_penalties": t.get("narrowing_penalties"),
                            "source_schema_version": t.get("source_schema_version"),
                            "source_top_keys": t.get("source_top_keys"),
                        }
                        for t in top
                    ],
                    "residual_tie_reason": "no semantic dominance feature distinguishes the tied candidates",
                    "safe_next_action": "add narrower source-ref dominance rule or build source row locator",
                })
            else:
                status = "NO_POSITIVE_NARROWING_SCORE"
                residual_ties.append({
                    "slot_id": slot_id,
                    "row_uid": b.get("row_uid"),
                    "field": b.get("field"),
                    "top_score": top_score,
                    "tied_candidate_count": len(top),
                    "tied_candidates": [],
                    "residual_tie_reason": "no candidate has positive narrowing score",
                    "safe_next_action": "build source row locator",
                })

        per_rows.append({
            "slot_id": slot_id,
            "row_uid": b.get("row_uid"),
            "field": b.get("field"),
            "candidate_count": len(rows),
            "top_score": top_score,
            "top_candidate_count": len(top),
            "narrowing_status": status,
            "authorized_to_rebind": False,
            "safe_next_action": "review/apply narrowed proposal only in later application unit" if status == "UNIQUE_NARROWED_REBIND_PROPOSAL" else "do not apply; narrow further",
        })

    # Candidate dominance rule if residual ties share a single missing distinguisher.
    if residual_ties:
        rule_candidates.append({
            "rule_candidate_id": "source_ref_rebind_dominance_rule_" + sha8({"residual_ties": residual_ties}),
            "rule_status": "RULE_CANDIDATE_ONLY_NOT_APPLIED",
            "applies_to": "source_ref_rebind_candidate_ties",
            "problem": "semantic dominance features still tie for one or more bindings",
            "possible_additional_features": [
                "explicit source role",
                "artifact producer unit",
                "source packet lineage",
                "row identity match",
                "field policy declared source object",
                "human/schema accepted source preference",
            ],
            "authorization_required_before_use": True,
        })

    return per_rows, narrowed, residual_ties, rule_candidates

def decide(per_rows: List[Dict[str, Any]], narrowed: List[Dict[str, Any]], residual_ties: List[Dict[str, Any]]) -> Tuple[str, List[str], str]:
    reason_codes = [
        "SOURCE_REF_REBIND_NARROWING_SURFACE_EMITTED",
        "DOMINANCE_FEATURE_MATRIX_EMITTED",
        "PER_BINDING_NARROWING_EMITTED",
        "NO_REBINDS_APPLIED",
        "NO_VALUES_AUTHORIZED_OR_APPLIED",
        "NO_METADATA_POPULATION",
    ]

    if len(narrowed) == len(per_rows) and per_rows:
        reason_codes.append("UNIQUE_NARROWED_REBIND_PROPOSALS_FOR_ALL_BINDINGS")
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_NARROWED_UNIQUE_PROPOSALS_READY_FOR_REVIEW"
        next_edge = "REVIEW_OR_APPLY_MACHINE_READABLE_SOURCE_REF_REBIND_PROPOSALS_V0"
    elif narrowed:
        reason_codes.append("PARTIAL_NARROWED_REBIND_PROPOSALS_AVAILABLE")
        reason_codes.append("RESIDUAL_REBIND_TIES_REMAIN")
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_NARROWED_PARTIAL_WITH_RESIDUAL_TIES"
        next_edge = "REVIEW_PARTIAL_SOURCE_REF_REBIND_PROPOSALS_OR_ADD_DOMINANCE_RULE_V0"
    else:
        reason_codes.append("NO_UNIQUE_NARROWED_REBIND_PROPOSALS")
        reason_codes.append("RESIDUAL_REBIND_TIES_REQUIRE_STRONGER_DOMINANCE_OR_SOURCE_ROW_LOCATOR")
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_NARROWING_STILL_AMBIGUOUS"
        next_edge = "BUILD_MACHINE_READABLE_SOURCE_REF_REBIND_DOMINANCE_RULE_OR_ROW_LOCATOR_SURFACE_V0"

    return status, reason_codes, next_edge

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_ref_rebind_narrowing_authority_boundary_v0",
        "status": status,
        "may_compute_dominance_features": True,
        "may_emit_narrowed_rebind_proposals": True,
        "may_emit_residual_tie_table": True,
        "may_emit_dominance_rule_candidates": True,
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

def rollup_obj(status: str, features: List[Dict[str, Any]], per_rows: List[Dict[str, Any]], narrowed: List[Dict[str, Any]], residual_ties: List[Dict[str, Any]], rule_candidates: List[Dict[str, Any]], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_ref_rebind_narrowing_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "source_ref_rebind_candidate_count": len(features),
        "binding_count": len(per_rows),
        "narrowed_rebind_proposal_count": len(narrowed),
        "residual_tie_binding_count": len(residual_ties),
        "dominance_rule_candidate_count": len(rule_candidates),
        "per_binding_narrowing_status_counts": dict(Counter(r["narrowing_status"] for r in per_rows)),
        "candidate_narrowing_positive_score_count": sum(1 for f in features if int(f.get("narrowing_score") or 0) > 0),
        "candidate_feature_reason_counts": dict(Counter(reason for f in features for reason in f.get("narrowing_reasons", []))),
        "candidate_feature_penalty_counts": dict(Counter(reason for f in features for reason in f.get("narrowing_penalties", []))),
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
        "schema_version": "typed_machine_readable_source_ref_rebind_narrowing_profile_v0",
        "profile_id": "source_ref_rebind_narrowing_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "narrowing_surface_built": True,
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
        "schema_version": "typed_machine_readable_source_ref_rebind_narrowing_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The rebind review found 168 tied candidates across 21 bindings; this unit computes narrower dominance features without applying rebinds or values.",
        "source_ref_rebind_candidate_count": roll["source_ref_rebind_candidate_count"],
        "binding_count": roll["binding_count"],
        "narrowed_rebind_proposal_count": roll["narrowed_rebind_proposal_count"],
        "residual_tie_binding_count": roll["residual_tie_binding_count"],
        "dominance_rule_candidate_count": roll["dominance_rule_candidate_count"],
        "per_binding_narrowing_status_counts": roll["per_binding_narrowing_status_counts"],
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
        "schema_version": "typed_machine_readable_source_ref_rebind_narrowing_transition_trace_v0",
        "trace": [
            {
                "step": "consume_tied_rebind_review",
                "question": "can stronger dominance features narrow tied source-ref candidates",
                "answer": "compute semantic dominance features without stable arbitrary tie-breakers",
                "taken": "build narrowing surface",
            },
            {
                "step": "classify_narrowing_result",
                "question": "are unique source-ref rebind proposals available",
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
        scored, per_binding, broken, slots = [], [], {}, {}
        features, per_rows, narrowed, residual_ties, rule_candidates = [], [], [], [], []
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_NARROWING_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_MACHINE_READABLE_SOURCE_REF_REBIND_NARROWING_BASIS_V0"
    else:
        scored, per_binding, broken, slots = load_records()
        policies = field_policy_by_field()
        features = []
        for candidate in scored:
            slot_id = str(candidate.get("slot_id"))
            features.append(dominance_features(candidate, broken.get(slot_id, {}), slots.get(slot_id, {}), policies))
        per_rows, narrowed, residual_ties, rule_candidates = narrow_per_binding(features, per_binding)
        status, reason_codes, next_edge = decide(per_rows, narrowed, residual_ties)

    roll = rollup_obj(status, features, per_rows, narrowed, residual_ties, rule_candidates, next_edge)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, roll, next_edge)
    boundary = authority_boundary_obj(status)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    narrowing_surface = {
        "schema_version": "typed_machine_readable_source_ref_rebind_narrowing_surface_v0",
        "surface_status": status,
        "source_rebind_review_receipt_id": SOURCE_REBIND_REVIEW_RECEIPT_ID,
        "source_ref_rebind_candidate_count": roll["source_ref_rebind_candidate_count"],
        "binding_count": roll["binding_count"],
        "narrowed_rebind_proposal_count": roll["narrowed_rebind_proposal_count"],
        "residual_tie_binding_count": roll["residual_tie_binding_count"],
        "dominance_rule_candidate_count": roll["dominance_rule_candidate_count"],
        "surface_claim": "Candidate source refs were narrowed using explicit semantic features only; no arbitrary stable tie-breaker was used.",
        "dominance_feature_matrix_ref": rel(DOMINANCE_FEATURE_MATRIX_PATH),
        "per_binding_narrowing_ref": rel(PER_BINDING_NARROWING_TABLE_PATH),
        "narrowed_rebind_proposals_ref": rel(NARROWED_REBIND_PROPOSALS_PATH),
        "residual_tie_table_ref": rel(RESIDUAL_TIE_TABLE_PATH),
        "recommended_next": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    review_packet = {
        "schema_version": "typed_machine_readable_source_ref_rebind_narrowing_review_packet_v0",
        "review_packet_status": "SOURCE_REF_REBIND_NARROWING_REVIEW_REQUIRED",
        "question": "Review narrowed source-ref rebind proposals or residual tie reasons. This packet does not authorize applying rebinds.",
        "allowed_responses": [
            "ACCEPT_NARROWED_REBIND_PROPOSALS_FOR_APPLICATION_UNIT",
            "ADD_SOURCE_REF_REBIND_DOMINANCE_RULE",
            "BUILD_SOURCE_ROW_LOCATOR_SURFACE",
            "REJECT_AND_FREEZE_DIAGNOSTIC_REFERENCE",
        ],
        "narrowing_surface_ref": rel(NARROWING_SURFACE_PATH),
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    application_contract = {
        "schema_version": "typed_machine_readable_source_ref_rebind_application_contract_v0",
        "contract_status": "REBIND_APPLICATION_NOT_AUTHORIZED",
        "after_review_possible_unit": "APPLY_REVIEWED_MACHINE_READABLE_SOURCE_REF_REBINDS_V0",
        "application_would_only_update_binding_surface": True,
        "application_would_not_apply_values": True,
        "application_would_not_populate_metadata": True,
        "application_would_not_mark_discriminators_ready": True,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    classification = {
        "schema_version": "typed_machine_readable_source_ref_rebind_narrowing_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "source_ref_rebind_candidate_count": roll["source_ref_rebind_candidate_count"],
        "binding_count": roll["binding_count"],
        "narrowed_rebind_proposal_count": roll["narrowed_rebind_proposal_count"],
        "residual_tie_binding_count": roll["residual_tie_binding_count"],
        "dominance_rule_candidate_count": roll["dominance_rule_candidate_count"],
        "per_binding_narrowing_status_counts": roll["per_binding_narrowing_status_counts"],
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

    write_json(NARROWING_SURFACE_PATH, narrowing_surface)
    write_json(DOMINANCE_FEATURE_MATRIX_PATH, {
        "schema_version": "typed_machine_readable_source_ref_rebind_dominance_feature_matrix_v0",
        "matrix_status": "DOMINANCE_FEATURES_COMPUTED_NOT_APPLIED",
        "candidate_count": len(features),
        "records": features,
    })
    write_json(PER_BINDING_NARROWING_TABLE_PATH, {
        "schema_version": "typed_machine_readable_source_ref_rebind_per_binding_narrowing_v0",
        "narrowing_status": "PER_BINDING_NARROWING_EMITTED",
        "binding_count": len(per_rows),
        "records": per_rows,
    })
    write_json(NARROWED_REBIND_PROPOSALS_PATH, {
        "schema_version": "typed_machine_readable_narrowed_source_ref_rebind_proposals_v0",
        "proposal_status": "NARROWED_REBIND_PROPOSALS_EMITTED_NOT_APPLIED",
        "proposal_count": len(narrowed),
        "records": narrowed,
    })
    write_json(RESIDUAL_TIE_TABLE_PATH, {
        "schema_version": "typed_machine_readable_source_ref_rebind_residual_tie_table_v0",
        "residual_tie_status": "RESIDUAL_REBIND_TIES_EMITTED",
        "residual_tie_binding_count": len(residual_ties),
        "records": residual_ties,
    })
    write_json(DOMINANCE_RULE_CANDIDATES_PATH, {
        "schema_version": "typed_machine_readable_source_ref_rebind_dominance_rule_candidates_v0",
        "rule_candidate_status": "DOMINANCE_RULE_CANDIDATES_EMITTED_NOT_APPLIED",
        "rule_candidate_count": len(rule_candidates),
        "records": rule_candidates,
    })
    write_json(NARROWING_REVIEW_PACKET_PATH, review_packet)
    write_json(NEXT_APPLICATION_CONTRACT_PATH, application_contract)
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
        "NARROWING_0_REBIND_REVIEW_RECEIPT_CONSUMED": SOURCE_REBIND_REVIEW_RECEIPT_PATH.exists(),
        "NARROWING_1_CANDIDATE_SCORE_TABLE_CONSUMED": SOURCE_CANDIDATE_SCORE_TABLE_PATH.exists(),
        "NARROWING_2_NARROWING_SURFACE_EMITTED": NARROWING_SURFACE_PATH.exists(),
        "NARROWING_3_DOMINANCE_FEATURE_MATRIX_EMITTED": DOMINANCE_FEATURE_MATRIX_PATH.exists(),
        "NARROWING_4_PER_BINDING_NARROWING_EMITTED": PER_BINDING_NARROWING_TABLE_PATH.exists(),
        "NARROWING_5_NARROWED_PROPOSALS_EMITTED": NARROWED_REBIND_PROPOSALS_PATH.exists(),
        "NARROWING_6_RESIDUAL_TIE_TABLE_EMITTED": RESIDUAL_TIE_TABLE_PATH.exists(),
        "NARROWING_7_DOMINANCE_RULE_CANDIDATES_EMITTED": DOMINANCE_RULE_CANDIDATES_PATH.exists(),
        "NARROWING_8_REVIEW_PACKET_EMITTED": NARROWING_REVIEW_PACKET_PATH.exists(),
        "NARROWING_9_APPLICATION_CONTRACT_EMITTED": NEXT_APPLICATION_CONTRACT_PATH.exists(),
        "NARROWING_10_NO_REBINDS_APPLIED": roll["rebinds_applied_count"] == 0,
        "NARROWING_11_NO_REFINEMENTS_APPLIED": roll["refinements_applied_count"] == 0,
        "NARROWING_12_NO_VALUES_AUTHORIZED": roll["values_authorized_count"] == 0,
        "NARROWING_13_NO_VALUES_APPLIED": roll["values_applied_count"] == 0,
        "NARROWING_14_NO_NULL_REASONS_ACCEPTED": roll["null_reason_accepted_count"] == 0,
        "NARROWING_15_NO_SOURCE_PACKET_MATERIALIZED": roll["source_packet_materialized_for_review_count"] == 0,
        "NARROWING_16_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "NARROWING_17_NO_DISCRIMINATOR_READY": roll["ready_discriminator_count"] == 0,
        "NARROWING_18_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "NARROWING_19_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "NARROWING_20_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "NARROWING_21_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classification["target_candidate_declared_for_review"] is False,
        "NARROWING_22_NO_TARGET_SELECTED_FOR_BUILD": classification["target_selected_for_build"] is False,
        "NARROWING_23_NO_ACCEPTED_FOR_BUILD": classification["accepted_for_build"] is False,
        "NARROWING_24_NO_RUNTIME_PATCH": classification["runtime_patch_authorized"] is False,
        "NARROWING_25_NO_TARGET_FILE_MODIFICATION": classification["target_file_modification_authorized"] is False,
        "NARROWING_26_NO_C5_OPENED": classification["c5_authorized"] is False,
        "NARROWING_27_NO_GENERAL_CELL1_AUTHORITY": classification["general_cell1_authority_granted"] is False,
        "NARROWING_28_NO_LATEST_FILE_GUESSING": classification["latest_file_guessing"] is False,
        "NARROWING_29_NO_MTIME_SELECTION": classification["mtime_selection"] is False,
        "NARROWING_30_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "NARROWING_31_ACCEPTANCE_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "NARROWING_32_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_NARROWING_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "candidates": roll["source_ref_rebind_candidate_count"],
        "bindings": roll["binding_count"],
        "narrowed": roll["narrowed_rebind_proposal_count"],
        "residual": roll["residual_tie_binding_count"],
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_source_ref_rebind_narrowing_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_NARROWING_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_rebind_review_receipt_id": SOURCE_REBIND_REVIEW_RECEIPT_ID,
        "machine_readable_source_ref_rebind_narrowing_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "source_ref_rebind_candidate_count": roll["source_ref_rebind_candidate_count"],
            "binding_count": roll["binding_count"],
            "narrowed_rebind_proposal_count": roll["narrowed_rebind_proposal_count"],
            "residual_tie_binding_count": roll["residual_tie_binding_count"],
            "dominance_rule_candidate_count": roll["dominance_rule_candidate_count"],
            "per_binding_narrowing_status_counts": roll["per_binding_narrowing_status_counts"],
            "candidate_narrowing_positive_score_count": roll["candidate_narrowing_positive_score_count"],
            "candidate_feature_reason_counts": roll["candidate_feature_reason_counts"],
            "candidate_feature_penalty_counts": roll["candidate_feature_penalty_counts"],
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
            "narrowing_surface": rel(NARROWING_SURFACE_PATH),
            "dominance_feature_matrix": rel(DOMINANCE_FEATURE_MATRIX_PATH),
            "per_binding_narrowing_table": rel(PER_BINDING_NARROWING_TABLE_PATH),
            "narrowed_rebind_proposals": rel(NARROWED_REBIND_PROPOSALS_PATH),
            "residual_tie_table": rel(RESIDUAL_TIE_TABLE_PATH),
            "dominance_rule_candidates": rel(DOMINANCE_RULE_CANDIDATES_PATH),
            "narrowing_review_packet": rel(NARROWING_REVIEW_PACKET_PATH),
            "next_application_contract": rel(NEXT_APPLICATION_CONTRACT_PATH),
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
    print(f"source_ref_rebind_narrowing_receipt_id={receipt_id}")
    print(f"source_ref_rebind_narrowing_receipt_path={rel(receipt_path)}")
    print(f"source_ref_rebind_narrowing_surface_path={rel(NARROWING_SURFACE_PATH)}")
    print(f"dominance_feature_matrix_path={rel(DOMINANCE_FEATURE_MATRIX_PATH)}")
    print(f"per_binding_narrowing_table_path={rel(PER_BINDING_NARROWING_TABLE_PATH)}")
    print(f"narrowed_rebind_proposals_path={rel(NARROWED_REBIND_PROPOSALS_PATH)}")
    print(f"residual_tie_table_path={rel(RESIDUAL_TIE_TABLE_PATH)}")
    print(f"dominance_rule_candidates_path={rel(DOMINANCE_RULE_CANDIDATES_PATH)}")
    print(f"source_ref_rebind_narrowing_rollup_path={rel(ROLLUP_PATH)}")
    print(f"source_ref_rebind_narrowing_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
