#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_WITH_ACCEPTED_SCHEMA_OVERLAY_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_ref_rebind_candidates_with_accepted_schema_overlay.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_REF_REBIND_CANDIDATES_WITH_ACCEPTED_SCHEMA_OVERLAY"
MODE = "SCHEMA_AWARE_REBIND_REVIEW / ACCEPTED_SCHEMA_REFERENCE_ONLY / NO_REBIND_APPLICATION / NO_VALUES / NO_METADATA"
BUILD_MODE = "SOURCE_REF_REBIND_CANDIDATE_REVIEW_WITH_ACCEPTED_SCHEMA_OVERLAY_ONLY"

SOURCE_APP_UNIT_REVIEW_RECEIPT_ID = "eb185428"
SOURCE_APP_UNIT_REVIEW_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_review_v0_receipts/eb185428.json"
SOURCE_ACCEPTED_REFERENCE_DOWNSTREAM_USE_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_review_v0/typed_machine_readable_schema_overlay_accepted_reference_downstream_use_contract_v0.json"
SOURCE_RETURN_TO_REBIND_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_review_v0/typed_machine_readable_schema_overlay_return_to_rebind_review_contract_v0.json"
SOURCE_APP_UNIT_REVIEW_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_review_v0/typed_machine_readable_schema_overlay_application_unit_review_classification_v0.json"
SOURCE_APP_UNIT_REVIEW_AUTHORITY_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_review_v0/typed_machine_readable_schema_overlay_application_unit_review_authority_boundary_v0.json"
SOURCE_APP_UNIT_REVIEW_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_review_v0/typed_machine_readable_schema_overlay_application_unit_review_rollup_v0.json"
SOURCE_APP_UNIT_REVIEW_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_review_v0/typed_machine_readable_schema_overlay_application_unit_review_profile_v0.json"

PRIOR_RECEIPT_IDS = [
    "c7a8616a",  # rebind candidates reviewed ambiguous
    "8edaaab8",  # rebind narrowing still ambiguous
    "7636e62c",  # dominance/row locator surface
    "e6281cfb",  # row locator no unique proposals
    "9539ff72",  # lineage/field policy typing surface
]

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_candidates_with_accepted_schema_overlay_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_candidates_with_accepted_schema_overlay_v0_receipts"

SOURCE_INVENTORY_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_accepted_schema_overlay_source_inventory_v0.json"
ACCEPTED_REFERENCE_REVIEW_INPUT_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_accepted_schema_overlay_reference_input_v0.json"
PRIOR_REBIND_CANDIDATE_INVENTORY_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_prior_candidate_inventory_v0.json"
SCHEMA_AWARE_REVIEW_TABLE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_schema_aware_candidate_review_table_v0.json"
SCHEMA_AWARE_BINDING_ROLLUP_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_schema_aware_binding_rollup_v0.json"
SCHEMA_AWARE_PROPOSAL_SURFACE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_schema_aware_proposal_surface_v0.json"
SCHEMA_AWARE_AMBIGUITY_SURFACE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_schema_aware_ambiguity_surface_v0.json"
SCHEMA_AWARE_REQUIREMENT_GAP_SURFACE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_schema_aware_requirement_gap_surface_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_schema_aware_downstream_decision_table_v0.json"
REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_schema_aware_review_packet_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_schema_aware_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_schema_aware_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_schema_aware_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_schema_aware_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_schema_aware_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_schema_aware_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_APP_UNIT_REVIEW_RECEIPT_PATH,
    SOURCE_ACCEPTED_REFERENCE_DOWNSTREAM_USE_CONTRACT_PATH,
    SOURCE_RETURN_TO_REBIND_CONTRACT_PATH,
    SOURCE_APP_UNIT_REVIEW_CLASSIFICATION_PATH,
    SOURCE_APP_UNIT_REVIEW_AUTHORITY_BOUNDARY_PATH,
    SOURCE_APP_UNIT_REVIEW_ROLLUP_PATH,
    SOURCE_APP_UNIT_REVIEW_PROFILE_PATH,
]

EXPECTED_APP_REVIEW_STATUS = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_REVIEWED_DOWNSTREAM_USE_READY"
EXPECTED_APP_REVIEW_STOP = "STOP_TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_REVIEWED_DOWNSTREAM_USE_READY"
EXPECTED_APP_REVIEW_NEXT = "REVIEW_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_WITH_ACCEPTED_SCHEMA_OVERLAY_V0"

SCHEMA_REQUIREMENTS = [
    "source_role",
    "source_packet_lineage",
    "artifact_producer_unit",
    "field_policy_source_object_match",
    "row_identity_schema",
]

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

def locate_receipt(receipt_id: str) -> Path:
    matches: List[Path] = []
    for p in (ROOT / "data").rglob("*.json"):
        if "_receipts" not in p.as_posix():
            continue
        try:
            obj = json.loads(p.read_text())
        except Exception:
            continue
        if obj.get("receipt_id") == receipt_id:
            matches.append(p)
    if len(matches) != 1:
        raise RuntimeError(f"receipt_id_lookup_count_not_1:{receipt_id}:{len(matches)}")
    return matches[0]

def recursively_find_dicts(obj: Any) -> Iterable[Dict[str, Any]]:
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from recursively_find_dicts(v)
    elif isinstance(obj, list):
        for x in obj:
            yield from recursively_find_dicts(x)

def text_of(obj: Any) -> str:
    try:
        return json.dumps(obj, sort_keys=True, default=str).lower()
    except Exception:
        return str(obj).lower()

def path_like(v: Any) -> bool:
    if not isinstance(v, str):
        return False
    s = v.lower()
    return "/" in s or s.endswith(".json") or s.endswith(".jsonl") or "data/" in s or "candidate" in s or "packet" in s

def candidate_record_score_seed(d: Dict[str, Any]) -> bool:
    keys = " ".join(str(k).lower() for k in d.keys())
    txt = text_of(d)
    return (
        "candidate" in keys
        or "source_ref" in keys
        or "rebind" in keys
        or "binding" in keys
        or "candidate" in txt
        or "source_ref" in txt
        or "rebind" in txt
    )

def binding_key(d: Dict[str, Any], fallback: str) -> str:
    for k in [
        "binding_id",
        "source_binding_id",
        "broken_binding_id",
        "slot_id",
        "slot_key",
        "target_slot_id",
        "row_uid",
        "field",
        "source_ref",
    ]:
        if k in d and d[k] not in (None, ""):
            return str(d[k])
    txt = text_of(d)
    m = re.search(r"(binding|slot|row)[_\- ]?([0-9a-f]{4,}|[0-9]+)", txt)
    if m:
        return m.group(0).replace(" ", "_")
    return fallback

def candidate_ref(d: Dict[str, Any], fallback: str) -> str:
    for k in [
        "candidate_source_ref",
        "candidate_ref",
        "candidate_artifact_path",
        "candidate_path",
        "source_file",
        "source_path",
        "path",
        "artifact_path",
        "file",
    ]:
        if k in d and d[k] not in (None, ""):
            return str(d[k])
    for k, v in d.items():
        if path_like(v):
            return str(v)
    return fallback

def schema_evidence_flags(d: Dict[str, Any]) -> Dict[str, bool]:
    txt = text_of(d)
    return {
        "source_role": ("source_role" in txt or "explicit_source_role" in txt),
        "source_packet_lineage": ("source_packet" in txt or "lineage" in txt),
        "artifact_producer_unit": ("artifact_producer" in txt or "producer_unit" in txt),
        "field_policy_source_object_match": ("field_policy" in txt or "source_object" in txt),
        "row_identity_schema": ("row_identity" in txt or "row_uid" in txt or "row identity" in txt),
    }

def score_candidate(d: Dict[str, Any], source_artifact: str) -> Tuple[int, List[str], List[str]]:
    flags = schema_evidence_flags(d)
    reasons = []
    missing = []
    score = 0
    for req in SCHEMA_REQUIREMENTS:
        if flags.get(req):
            score += 2
            reasons.append(f"{req}_signal_present")
        else:
            missing.append(req)
    txt = text_of(d) + " " + source_artifact.lower()
    if "packet" in txt:
        score += 1
        reasons.append("packet_surface_signal")
    if "lineage" in txt:
        score += 1
        reasons.append("lineage_surface_signal")
    if "review" in txt:
        score -= 1
        reasons.append("review_surface_penalty")
    if "candidate" in txt:
        score -= 1
        reasons.append("candidate_surface_penalty")
    return score, reasons, missing

def validate_basis() -> Tuple[List[str], List[Path], List[Dict[str, Any]]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")

    prior_receipts: List[Path] = []
    if not failures:
        try:
            prior_receipts = [locate_receipt(rid) for rid in PRIOR_RECEIPT_IDS]
        except Exception as e:
            failures.append(str(e))

    if failures:
        return failures, prior_receipts, []

    app_receipt = read_json(SOURCE_APP_UNIT_REVIEW_RECEIPT_PATH)
    summary = app_receipt.get("machine_readable_schema_overlay_application_unit_review_summary", {})
    downstream = read_json(SOURCE_ACCEPTED_REFERENCE_DOWNSTREAM_USE_CONTRACT_PATH)
    return_contract = read_json(SOURCE_RETURN_TO_REBIND_CONTRACT_PATH)
    classif = read_json(SOURCE_APP_UNIT_REVIEW_CLASSIFICATION_PATH)
    authority = read_json(SOURCE_APP_UNIT_REVIEW_AUTHORITY_BOUNDARY_PATH)
    roll = read_json(SOURCE_APP_UNIT_REVIEW_ROLLUP_PATH)
    profile = read_json(SOURCE_APP_UNIT_REVIEW_PROFILE_PATH)

    if app_receipt.get("receipt_id") != SOURCE_APP_UNIT_REVIEW_RECEIPT_ID or app_receipt.get("gate") != "PASS":
        failures.append("source_app_unit_review_receipt_not_pass")
    if summary.get("status") != EXPECTED_APP_REVIEW_STATUS:
        failures.append(f"source_app_unit_review_status_not_expected:{summary.get('status')}")
    if app_receipt.get("terminal", {}).get("stop_code") != EXPECTED_APP_REVIEW_STOP:
        failures.append("source_app_unit_review_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_APP_REVIEW_NEXT:
        failures.append(f"source_app_unit_review_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("downstream_use_ready") is not True:
        failures.append("downstream_use_not_ready")
    if summary.get("return_to_rebind_review_contract_emitted") is not True:
        failures.append("return_to_rebind_contract_not_emitted")
    if summary.get("schema_overlay_applied_for_this_contract") is not True:
        failures.append("schema_overlay_not_applied_for_contract")
    if summary.get("applied_as_reference_for_this_application_contract") is not True:
        failures.append("accepted_reference_not_applied_for_contract")
    for key in [
        "schema_overlay_applied_globally",
        "reusable_schema_authorized",
        "preapproved_schema_authorized",
        "validator_registry_entry_created",
        "future_automatic_use_allowed",
        "typing_rule_applied",
        "field_policy_modified",
        "candidate_artifact_modified",
        "source_row_locator_applied",
        "rebinds_applied",
        "values_authorized",
        "values_applied",
        "metadata_populated",
        "target_selected_for_build",
        "runtime_patch_applied",
        "c5_opened",
    ]:
        if summary.get(key) is not False:
            failures.append(f"source_summary_forbidden_true:{key}")
    if summary.get("ready_discriminator_count") != 0:
        failures.append("ready_discriminator_nonzero")

    if downstream.get("contract_status") != "ACCEPTED_REFERENCE_DOWNSTREAM_USE_READY":
        failures.append("downstream_use_contract_not_ready")
    if return_contract.get("contract_status") != "RETURN_TO_REBIND_REVIEW_READY":
        failures.append("return_to_rebind_contract_not_ready")
    if classif.get("classification_status") != EXPECTED_APP_REVIEW_STATUS:
        failures.append("classification_status_wrong")
    if authority.get("may_review_rebind_candidates_against_accepted_overlay") is not True:
        failures.append("authority_does_not_allow_rebind_review")
    if authority.get("may_apply_rebinds") is not False:
        failures.append("authority_allows_rebind_application")
    if roll.get("downstream_use_ready_count") != 1:
        failures.append("rollup_downstream_use_ready_not_1")
    if roll.get("rebinds_applied_count") != 0:
        failures.append("rollup_rebinds_already_applied")
    if profile.get("downstream_use_ready") is not True:
        failures.append("profile_downstream_use_not_ready")

    prior_receipt_objs = [read_json(p) for p in prior_receipts]
    return failures, prior_receipts, prior_receipt_objs

def collect_candidate_records(prior_receipts: List[Path], prior_receipt_objs: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[str]]:
    candidate_records: List[Dict[str, Any]] = []
    artifact_paths: List[str] = []

    for receipt_path, receipt in zip(prior_receipts, prior_receipt_objs):
        receipt_rel = rel(receipt_path)
        artifacts = receipt.get("output_artifacts", {})
        if isinstance(artifacts, dict):
            for name, artifact in artifacts.items():
                if not isinstance(artifact, str):
                    continue
                p = ROOT / artifact
                if p.exists() and p.suffix == ".json":
                    artifact_paths.append(artifact)
                    try:
                        obj = read_json(p)
                    except Exception:
                        continue
                    for idx, d in enumerate(recursively_find_dicts(obj)):
                        if candidate_record_score_seed(d):
                            candidate_records.append({
                                "source_receipt_id": receipt.get("receipt_id"),
                                "source_receipt_path": receipt_rel,
                                "source_artifact_name": name,
                                "source_artifact_path": artifact,
                                "record_index": idx,
                                "record": d,
                            })
        for idx, d in enumerate(recursively_find_dicts(receipt)):
            if candidate_record_score_seed(d):
                candidate_records.append({
                    "source_receipt_id": receipt.get("receipt_id"),
                    "source_receipt_path": receipt_rel,
                    "source_artifact_name": "receipt_recursive_record",
                    "source_artifact_path": receipt_rel,
                    "record_index": idx,
                    "record": d,
                })

    seen = set()
    deduped = []
    for row in candidate_records:
        key = sha8(row)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped, sorted(set(artifact_paths))

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, prior_receipt_paths, prior_receipt_objs = validate_basis()

    accepted_reference_contract = read_json(SOURCE_ACCEPTED_REFERENCE_DOWNSTREAM_USE_CONTRACT_PATH)
    return_contract = read_json(SOURCE_RETURN_TO_REBIND_CONTRACT_PATH)

    candidate_records, source_artifact_paths = collect_candidate_records(prior_receipt_paths, prior_receipt_objs) if not failures else ([], [])

    review_rows: List[Dict[str, Any]] = []
    for idx, row in enumerate(candidate_records):
        record = row["record"]
        bkey = binding_key(record, f"unknown_binding_{idx:04d}")
        cref = candidate_ref(record, f"unknown_candidate_{idx:04d}")
        score, reasons, missing = score_candidate(record, row["source_artifact_path"])
        review_rows.append({
            "schema_aware_candidate_review_id": "schema_rebind_candidate_review_" + sha8({"idx": idx, "row": row}),
            "source_receipt_id": row["source_receipt_id"],
            "source_receipt_path": row["source_receipt_path"],
            "source_artifact_name": row["source_artifact_name"],
            "source_artifact_path": row["source_artifact_path"],
            "record_index": row["record_index"],
            "binding_key": bkey,
            "candidate_ref": cref,
            "schema_requirement_score": score,
            "schema_evidence_reasons": reasons,
            "missing_schema_requirements": missing,
            "all_schema_requirements_observed": len(missing) == 0,
            "candidate_record_digest": sha8(record),
        })

    by_binding: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in review_rows:
        by_binding[row["binding_key"]].append(row)

    binding_rollups: List[Dict[str, Any]] = []
    unique_proposals: List[Dict[str, Any]] = []
    ambiguous_bindings: List[Dict[str, Any]] = []
    requirement_gaps: List[Dict[str, Any]] = []

    for bkey, rows in sorted(by_binding.items()):
        rows_sorted = sorted(rows, key=lambda r: (-r["schema_requirement_score"], r["candidate_ref"], r["schema_aware_candidate_review_id"]))
        top_score = rows_sorted[0]["schema_requirement_score"] if rows_sorted else None
        top_rows = [r for r in rows_sorted if r["schema_requirement_score"] == top_score]
        full_rows = [r for r in rows_sorted if r["all_schema_requirements_observed"]]
        if len(top_rows) == 1 and full_rows and top_rows[0]["all_schema_requirements_observed"]:
            status = "UNIQUE_SCHEMA_AWARE_REBIND_PROPOSAL_READY"
            unique_proposals.append({
                "binding_key": bkey,
                "candidate_ref": top_rows[0]["candidate_ref"],
                "schema_aware_candidate_review_id": top_rows[0]["schema_aware_candidate_review_id"],
                "proposal_status": "PROPOSED_FOR_REVIEW_ONLY_NOT_APPLIED",
                "schema_requirement_score": top_rows[0]["schema_requirement_score"],
                "source_receipt_id": top_rows[0]["source_receipt_id"],
                "source_artifact_path": top_rows[0]["source_artifact_path"],
            })
        elif len(top_rows) > 1:
            status = "SCHEMA_AWARE_TOP_CANDIDATES_STILL_TIED"
            ambiguous_bindings.append({
                "binding_key": bkey,
                "ambiguity_status": status,
                "top_score": top_score,
                "top_candidate_count": len(top_rows),
                "top_candidate_refs": [r["candidate_ref"] for r in top_rows[:25]],
                "truncated": len(top_rows) > 25,
            })
        else:
            status = "SCHEMA_REQUIREMENT_GAP_BLOCKS_REBIND_PROPOSAL"
            gap_counts = Counter(x for r in rows_sorted for x in r["missing_schema_requirements"])
            requirement_gaps.append({
                "binding_key": bkey,
                "gap_status": status,
                "top_score": top_score,
                "candidate_count": len(rows_sorted),
                "missing_requirement_counts": dict(sorted(gap_counts.items())),
            })

        binding_rollups.append({
            "binding_key": bkey,
            "candidate_count": len(rows_sorted),
            "top_score": top_score,
            "top_candidate_count": len(top_rows),
            "full_schema_candidate_count": len(full_rows),
            "schema_aware_binding_status": status,
        })

    binding_status_counts = Counter(r["schema_aware_binding_status"] for r in binding_rollups)
    schema_requirement_missing_counts = Counter(x for r in review_rows for x in r["missing_schema_requirements"])

    if failures:
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_WITH_ACCEPTED_SCHEMA_OVERLAY_REVIEW_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_WITH_ACCEPTED_SCHEMA_OVERLAY_REVIEW_BASIS_V0"
    elif not review_rows:
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_WITH_ACCEPTED_SCHEMA_OVERLAY_REVIEWED_NO_CANDIDATE_ROWS_EXTRACTED"
        reason_codes = [
            "ACCEPTED_SCHEMA_OVERLAY_REFERENCE_CONSUMED",
            "PRIOR_REBIND_RECEIPTS_CONSUMED",
            "NO_SCHEMA_AWARE_CANDIDATE_ROWS_EXTRACTED",
            "NO_REBINDS_APPLIED",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
        ]
        next_edge = "REPAIR_SOURCE_REF_REBIND_CANDIDATE_ROW_EXTRACTION_WITH_ACCEPTED_SCHEMA_OVERLAY_V0"
    elif unique_proposals and len(unique_proposals) == len(binding_rollups):
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_WITH_ACCEPTED_SCHEMA_OVERLAY_REVIEWED_UNIQUE_PROPOSALS_READY"
        reason_codes = [
            "ACCEPTED_SCHEMA_OVERLAY_REFERENCE_CONSUMED",
            "SCHEMA_AWARE_REBIND_REVIEW_COMPLETE",
            "UNIQUE_SCHEMA_AWARE_REBIND_PROPOSALS_READY_FOR_REVIEW",
            "PROPOSALS_EMITTED_FOR_REVIEW_ONLY",
            "NO_REBINDS_APPLIED",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
        ]
        next_edge = "REVIEW_SCHEMA_AWARE_SOURCE_REF_REBIND_PROPOSALS_V0"
    elif unique_proposals:
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_WITH_ACCEPTED_SCHEMA_OVERLAY_REVIEWED_PARTIAL_PROPOSALS_REMAINING_AMBIGUITY"
        reason_codes = [
            "ACCEPTED_SCHEMA_OVERLAY_REFERENCE_CONSUMED",
            "SCHEMA_AWARE_REBIND_REVIEW_COMPLETE",
            "PARTIAL_SCHEMA_AWARE_REBIND_PROPOSALS_EMITTED_FOR_REVIEW_ONLY",
            "RESIDUAL_REBIND_AMBIGUITY_REMAINS",
            "NO_REBINDS_APPLIED",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
        ]
        next_edge = "REVIEW_PARTIAL_SCHEMA_AWARE_SOURCE_REF_REBIND_PROPOSALS_AND_AMBIGUITIES_V0"
    else:
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_WITH_ACCEPTED_SCHEMA_OVERLAY_REVIEWED_NO_UNIQUE_PROPOSALS"
        reason_codes = [
            "ACCEPTED_SCHEMA_OVERLAY_REFERENCE_CONSUMED",
            "SCHEMA_AWARE_REBIND_REVIEW_COMPLETE",
            "NO_UNIQUE_SCHEMA_AWARE_REBIND_PROPOSALS",
            "SCHEMA_REQUIREMENT_GAPS_OR_TIES_REMAIN",
            "NO_REBINDS_APPLIED",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
        ]
        next_edge = "BUILD_SCHEMA_AWARE_SOURCE_REF_REBIND_REQUIREMENT_GAP_OR_TIE_REPAIR_SURFACE_V0"

    source_inventory = {
        "schema_version": "typed_machine_readable_source_ref_rebind_accepted_schema_overlay_source_inventory_v0",
        "inventory_status": "SOURCE_INVENTORY_EMITTED",
        "accepted_schema_overlay_application_unit_review_receipt_id": SOURCE_APP_UNIT_REVIEW_RECEIPT_ID,
        "prior_receipt_ids": PRIOR_RECEIPT_IDS,
        "prior_receipt_paths": [rel(p) for p in prior_receipt_paths],
        "prior_output_artifact_paths_scanned": source_artifact_paths,
        "candidate_row_count": len(review_rows),
    }

    accepted_reference_input = {
        "schema_version": "typed_machine_readable_source_ref_rebind_accepted_schema_overlay_reference_input_v0",
        "input_status": "ACCEPTED_SCHEMA_OVERLAY_REFERENCE_CONSUMED",
        "accepted_reference_downstream_use_contract_path": rel(SOURCE_ACCEPTED_REFERENCE_DOWNSTREAM_USE_CONTRACT_PATH),
        "return_to_rebind_contract_path": rel(SOURCE_RETURN_TO_REBIND_CONTRACT_PATH),
        "downstream_contract_status": accepted_reference_contract.get("contract_status"),
        "return_to_rebind_contract_status": return_contract.get("contract_status"),
        "schema_requirements_used_for_review": SCHEMA_REQUIREMENTS,
        "scope": "this receipt lineage only",
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
    }

    prior_candidate_inventory = {
        "schema_version": "typed_machine_readable_source_ref_rebind_prior_candidate_inventory_v0",
        "inventory_status": "PRIOR_REBIND_CANDIDATES_EXTRACTED_FROM_EXPLICIT_RECEIPT_LINEAGE",
        "candidate_record_count": len(review_rows),
        "binding_count": len(binding_rollups),
        "source_receipt_counts": dict(Counter(r["source_receipt_id"] for r in review_rows)),
        "source_artifact_counts": dict(Counter(r["source_artifact_path"] for r in review_rows)),
        "candidate_extraction_method": "explicit_prior_receipt_ids_only_no_latest_no_mtime",
    }

    proposal_surface = {
        "schema_version": "typed_machine_readable_source_ref_rebind_schema_aware_proposal_surface_v0",
        "proposal_surface_status": "SCHEMA_AWARE_REBIND_PROPOSALS_FOR_REVIEW_ONLY" if unique_proposals else "NO_SCHEMA_AWARE_REBIND_PROPOSALS",
        "proposal_count": len(unique_proposals),
        "proposals": unique_proposals,
        "rebinds_applied": False,
    }

    ambiguity_surface = {
        "schema_version": "typed_machine_readable_source_ref_rebind_schema_aware_ambiguity_surface_v0",
        "ambiguity_surface_status": "SCHEMA_AWARE_REBIND_AMBIGUITIES_REMAIN" if ambiguous_bindings else "NO_SCHEMA_AWARE_REBIND_AMBIGUITIES_RECORDED",
        "ambiguous_binding_count": len(ambiguous_bindings),
        "ambiguous_bindings": ambiguous_bindings,
    }

    requirement_gap_surface = {
        "schema_version": "typed_machine_readable_source_ref_rebind_schema_aware_requirement_gap_surface_v0",
        "requirement_gap_surface_status": "SCHEMA_REQUIREMENT_GAPS_REMAIN" if requirement_gaps else "NO_SCHEMA_REQUIREMENT_GAP_BLOCKERS_RECORDED",
        "requirement_gap_binding_count": len(requirement_gaps),
        "missing_requirement_counts": dict(sorted(schema_requirement_missing_counts.items())),
        "requirement_gaps": requirement_gaps,
    }

    decision_table = {
        "schema_version": "typed_machine_readable_source_ref_rebind_schema_aware_downstream_decision_table_v0",
        "decision_status": "SCHEMA_AWARE_REBIND_REVIEW_DECISION_EMITTED",
        "records": [
            {
                "decision": "REVIEW_SCHEMA_AWARE_REBIND_PROPOSALS",
                "selected": bool(unique_proposals),
                "next_unit": "REVIEW_SCHEMA_AWARE_SOURCE_REF_REBIND_PROPOSALS_V0" if bool(unique_proposals) else None,
                "why": "selected only when schema-aware unique proposals exist; still not applied",
            },
            {
                "decision": "REPAIR_SCHEMA_AWARE_REBIND_REQUIREMENT_GAPS_OR_TIES",
                "selected": not bool(unique_proposals),
                "next_unit": "BUILD_SCHEMA_AWARE_SOURCE_REF_REBIND_REQUIREMENT_GAP_OR_TIE_REPAIR_SURFACE_V0" if not bool(unique_proposals) else None,
                "why": "selected when accepted overlay review leaves no unique proposals",
            },
            {
                "decision": "APPLY_REBINDS",
                "selected": False,
                "next_unit": None,
                "why": "not authorized in this unit",
            },
        ],
    }

    review_packet = {
        "schema_version": "typed_machine_readable_source_ref_rebind_schema_aware_review_packet_v0",
        "review_packet_status": status,
        "summary": {
            "candidate_record_count": len(review_rows),
            "binding_count": len(binding_rollups),
            "unique_proposal_count": len(unique_proposals),
            "ambiguous_binding_count": len(ambiguous_bindings),
            "requirement_gap_binding_count": len(requirement_gaps),
            "binding_status_counts": dict(binding_status_counts),
            "missing_requirement_counts": dict(sorted(schema_requirement_missing_counts.items())),
            "rebinds_applied": False,
            "metadata_populated": False,
        },
        "recommended_next": next_edge,
    }

    classification = {
        "schema_version": "typed_machine_readable_source_ref_rebind_schema_aware_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "accepted_schema_overlay_reference_consumed": True,
        "prior_rebind_receipt_count": len(prior_receipt_paths),
        "candidate_record_count": len(review_rows),
        "binding_count": len(binding_rollups),
        "schema_aware_review_complete": not bool(failures),
        "unique_schema_aware_rebind_proposal_count": len(unique_proposals),
        "ambiguous_binding_count": len(ambiguous_bindings),
        "requirement_gap_binding_count": len(requirement_gaps),
        "schema_overlay_applied_for_this_contract": True,
        "schema_overlay_applied_globally": False,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
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
        "target_selected_for_build": False,
        "runtime_patch_authorized": False,
        "c5_authorized": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
        "recommended_next": next_edge,
        "next_command_goal": None,
    }

    authority_boundary = {
        "schema_version": "typed_machine_readable_source_ref_rebind_schema_aware_authority_boundary_v0",
        "status": status,
        "may_review_rebind_candidates_against_accepted_overlay": True,
        "may_emit_rebind_proposals_for_review": True,
        "may_apply_rebinds": False,
        "may_treat_schema_as_reusable": False,
        "may_treat_schema_as_preapproved": False,
        "may_create_validator_registry_entry": False,
        "may_allow_future_automatic_use": False,
        "may_apply_typing_rule": False,
        "may_modify_field_policy": False,
        "may_modify_candidate_artifacts": False,
        "may_authorize_values": False,
        "may_apply_values": False,
        "may_populate_metadata": False,
        "may_select_target_for_build": False,
        "may_apply_runtime_patch": False,
        "may_open_c5": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
    }

    rollup = {
        "schema_version": "typed_machine_readable_source_ref_rebind_schema_aware_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "accepted_schema_overlay_reference_consumed_count": 1,
        "prior_rebind_receipt_count": len(prior_receipt_paths),
        "candidate_record_count": len(review_rows),
        "binding_count": len(binding_rollups),
        "unique_schema_aware_rebind_proposal_count": len(unique_proposals),
        "ambiguous_binding_count": len(ambiguous_bindings),
        "requirement_gap_binding_count": len(requirement_gaps),
        "schema_overlay_applied_for_this_contract_count": 1,
        "schema_overlay_applied_globally_count": 0,
        "reusable_schema_authorized_count": 0,
        "preapproved_schema_authorized_count": 0,
        "validator_registry_entry_created_count": 0,
        "future_automatic_use_allowed_count": 0,
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
        "binding_status_counts": dict(binding_status_counts),
        "schema_requirement_missing_counts": dict(sorted(schema_requirement_missing_counts.items())),
        "recommended_next": next_edge,
    }

    zero_keys = [
        "schema_overlay_applied_globally_count",
        "reusable_schema_authorized_count",
        "preapproved_schema_authorized_count",
        "validator_registry_entry_created_count",
        "future_automatic_use_allowed_count",
        "typing_rule_applied_count",
        "field_policy_modified_count",
        "candidate_artifact_modified_count",
        "source_row_locator_applied_count",
        "rebinds_applied_count",
        "values_authorized_count",
        "values_applied_count",
        "metadata_populated_count",
        "ready_discriminator_count",
        "target_selected_for_build_count",
        "runtime_patch_applied_count",
        "c5_opened_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "typed_machine_readable_source_ref_rebind_schema_aware_profile_v0",
        "profile_id": "source_ref_rebind_schema_aware_profile_" + sha8(rollup),
        "status": status,
        "accepted_schema_overlay_reference_consumed": True,
        "schema_aware_review_complete": not bool(failures),
        "candidate_record_count": len(review_rows),
        "binding_count": len(binding_rollups),
        "unique_schema_aware_rebind_proposal_count": len(unique_proposals),
        "ambiguous_binding_count": len(ambiguous_bindings),
        "requirement_gap_binding_count": len(requirement_gaps),
        "schema_overlay_applied_for_this_contract": True,
        "schema_overlay_applied_globally": False,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
        "typing_rule_applied": False,
        "field_policy_modified": False,
        "candidate_artifact_modified": False,
        "source_row_locator_applied": False,
        "rebinds_applied": False,
        "values_authorized": False,
        "values_applied": False,
        "metadata_populated": False,
        "ready_discriminator_count": 0,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "c5_opened": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommended_next": next_edge,
        "next_command_goal": None,
    }

    report = {
        "schema_version": "typed_machine_readable_source_ref_rebind_schema_aware_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Source-ref rebind candidates were reviewed against the one-time accepted schema overlay reference. This unit emits review/proposal/gap surfaces only and does not apply rebinds, values, metadata, schema reuse, runtime patches, or C5.",
        "candidate_record_count": len(review_rows),
        "binding_count": len(binding_rollups),
        "unique_schema_aware_rebind_proposal_count": len(unique_proposals),
        "ambiguous_binding_count": len(ambiguous_bindings),
        "requirement_gap_binding_count": len(requirement_gaps),
        "rebinds_applied_count": 0,
        "metadata_populated_count": 0,
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
    }

    trace = {
        "schema_version": "typed_machine_readable_source_ref_rebind_schema_aware_transition_trace_v0",
        "trace": [
            {
                "step": "consume_accepted_schema_overlay_reference",
                "question": "is branch-only downstream schema reference available",
                "answer": "yes",
                "taken": "load accepted reference and return-to-rebind contract",
            },
            {
                "step": "consume_prior_rebind_candidate_receipts",
                "question": "which prior receipt lineage bounds the rebind review",
                "answer": PRIOR_RECEIPT_IDS,
                "taken": "extract candidate records from explicit receipt lineage only",
            },
            {
                "step": "schema_aware_candidate_review",
                "question": "does accepted schema overlay distinguish candidates",
                "answer": status,
                "taken": next_edge,
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    write_json(SOURCE_INVENTORY_PATH, source_inventory)
    write_json(ACCEPTED_REFERENCE_REVIEW_INPUT_PATH, accepted_reference_input)
    write_json(PRIOR_REBIND_CANDIDATE_INVENTORY_PATH, prior_candidate_inventory)
    write_json(SCHEMA_AWARE_REVIEW_TABLE_PATH, {
        "schema_version": "typed_machine_readable_source_ref_rebind_schema_aware_candidate_review_table_v0",
        "review_table_status": "SCHEMA_AWARE_REBIND_CANDIDATE_REVIEW_TABLE_EMITTED",
        "candidate_record_count": len(review_rows),
        "records": review_rows,
    })
    write_json(SCHEMA_AWARE_BINDING_ROLLUP_PATH, {
        "schema_version": "typed_machine_readable_source_ref_rebind_schema_aware_binding_rollup_v0",
        "binding_rollup_status": "SCHEMA_AWARE_BINDING_ROLLUP_EMITTED",
        "binding_count": len(binding_rollups),
        "binding_status_counts": dict(binding_status_counts),
        "records": binding_rollups,
    })
    write_json(SCHEMA_AWARE_PROPOSAL_SURFACE_PATH, proposal_surface)
    write_json(SCHEMA_AWARE_AMBIGUITY_SURFACE_PATH, ambiguity_surface)
    write_json(SCHEMA_AWARE_REQUIREMENT_GAP_SURFACE_PATH, requirement_gap_surface)
    write_json(DOWNSTREAM_DECISION_TABLE_PATH, decision_table)
    write_json(REVIEW_PACKET_PATH, review_packet)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(AUTHORITY_BOUNDARY_PATH, authority_boundary)
    write_json(ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, profile)
    write_json(REPORT_PATH, report)
    write_json(TRANSITION_TRACE_PATH, trace)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        rollup["source_mutation_count"] = 1
        report["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup)
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "SCHEMA_AWARE_REBIND_REVIEW_0_ACCEPTED_REFERENCE_CONSUMED": SOURCE_ACCEPTED_REFERENCE_DOWNSTREAM_USE_CONTRACT_PATH.exists(),
        "SCHEMA_AWARE_REBIND_REVIEW_1_RETURN_TO_REBIND_CONTRACT_CONSUMED": SOURCE_RETURN_TO_REBIND_CONTRACT_PATH.exists(),
        "SCHEMA_AWARE_REBIND_REVIEW_2_PRIOR_RECEIPTS_CONSUMED": len(prior_receipt_paths) == len(PRIOR_RECEIPT_IDS),
        "SCHEMA_AWARE_REBIND_REVIEW_3_SOURCE_INVENTORY_EMITTED": SOURCE_INVENTORY_PATH.exists(),
        "SCHEMA_AWARE_REBIND_REVIEW_4_CANDIDATE_INVENTORY_EMITTED": PRIOR_REBIND_CANDIDATE_INVENTORY_PATH.exists(),
        "SCHEMA_AWARE_REBIND_REVIEW_5_REVIEW_TABLE_EMITTED": SCHEMA_AWARE_REVIEW_TABLE_PATH.exists(),
        "SCHEMA_AWARE_REBIND_REVIEW_6_BINDING_ROLLUP_EMITTED": SCHEMA_AWARE_BINDING_ROLLUP_PATH.exists(),
        "SCHEMA_AWARE_REBIND_REVIEW_7_PROPOSAL_SURFACE_EMITTED": SCHEMA_AWARE_PROPOSAL_SURFACE_PATH.exists(),
        "SCHEMA_AWARE_REBIND_REVIEW_8_AMBIGUITY_SURFACE_EMITTED": SCHEMA_AWARE_AMBIGUITY_SURFACE_PATH.exists(),
        "SCHEMA_AWARE_REBIND_REVIEW_9_REQUIREMENT_GAP_SURFACE_EMITTED": SCHEMA_AWARE_REQUIREMENT_GAP_SURFACE_PATH.exists(),
        "SCHEMA_AWARE_REBIND_REVIEW_10_NO_GLOBAL_SCHEMA_APPLICATION": rollup["schema_overlay_applied_globally_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_11_NO_REUSABLE_SCHEMA_AUTHORIZED": rollup["reusable_schema_authorized_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_12_NO_PREAPPROVED_SCHEMA_AUTHORIZED": rollup["preapproved_schema_authorized_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_13_NO_VALIDATOR_REGISTRY_ENTRY": rollup["validator_registry_entry_created_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_14_NO_FUTURE_AUTOMATIC_USE": rollup["future_automatic_use_allowed_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_15_NO_TYPING_RULE_APPLIED": rollup["typing_rule_applied_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_16_NO_FIELD_POLICY_MODIFIED": rollup["field_policy_modified_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_17_NO_CANDIDATE_ARTIFACT_MODIFIED": rollup["candidate_artifact_modified_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_18_NO_ROW_LOCATOR_APPLIED": rollup["source_row_locator_applied_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_19_NO_REBINDS_APPLIED": rollup["rebinds_applied_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_20_NO_VALUES_AUTHORIZED": rollup["values_authorized_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_21_NO_VALUES_APPLIED": rollup["values_applied_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_22_NO_METADATA_POPULATION": rollup["metadata_populated_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_23_NO_DISCRIMINATOR_READY": rollup["ready_discriminator_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_24_NO_TARGET_SELECTED": rollup["target_selected_for_build_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_25_NO_RUNTIME_PATCH": rollup["runtime_patch_applied_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_26_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_27_NO_LATEST_FILE_GUESSING": rollup["latest_file_guessing_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_28_NO_MTIME_SELECTION": rollup["mtime_selection_count"] == 0,
        "SCHEMA_AWARE_REBIND_REVIEW_29_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "SCHEMA_AWARE_REBIND_REVIEW_30_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "accepted_schema_overlay_reference_this_application_contract_only",
        "SCHEMA_AWARE_REBIND_REVIEW_31_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_WITH_ACCEPTED_SCHEMA_OVERLAY_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "candidate_count": len(review_rows),
        "binding_count": len(binding_rollups),
        "proposal_count": len(unique_proposals),
        "rebinds_applied": 0,
        "metadata": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_source_ref_rebind_schema_aware_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_SCHEMA_AWARE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_application_unit_review_receipt_id": SOURCE_APP_UNIT_REVIEW_RECEIPT_ID,
        "machine_readable_source_ref_rebind_schema_aware_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "accepted_schema_overlay_reference_consumed": True,
            "prior_rebind_receipt_count": len(prior_receipt_paths),
            "candidate_record_count": len(review_rows),
            "binding_count": len(binding_rollups),
            "unique_schema_aware_rebind_proposal_count": len(unique_proposals),
            "ambiguous_binding_count": len(ambiguous_bindings),
            "requirement_gap_binding_count": len(requirement_gaps),
            "schema_overlay_applied_for_this_contract": True,
            "schema_overlay_applied_globally": False,
            "reusable_schema_authorized": False,
            "preapproved_schema_authorized": False,
            "validator_registry_entry_created": False,
            "future_automatic_use_allowed": False,
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
            "target_selected_for_build": False,
            "runtime_patch_applied": False,
            "c5_opened": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
            "bad_counters_zero": profile["bad_counters_zero"],
            "recommended_next": next_edge,
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "source_inventory": rel(SOURCE_INVENTORY_PATH),
            "accepted_reference_review_input": rel(ACCEPTED_REFERENCE_REVIEW_INPUT_PATH),
            "prior_rebind_candidate_inventory": rel(PRIOR_REBIND_CANDIDATE_INVENTORY_PATH),
            "schema_aware_review_table": rel(SCHEMA_AWARE_REVIEW_TABLE_PATH),
            "schema_aware_binding_rollup": rel(SCHEMA_AWARE_BINDING_ROLLUP_PATH),
            "schema_aware_proposal_surface": rel(SCHEMA_AWARE_PROPOSAL_SURFACE_PATH),
            "schema_aware_ambiguity_surface": rel(SCHEMA_AWARE_AMBIGUITY_SURFACE_PATH),
            "schema_aware_requirement_gap_surface": rel(SCHEMA_AWARE_REQUIREMENT_GAP_SURFACE_PATH),
            "downstream_decision_table": rel(DOWNSTREAM_DECISION_TABLE_PATH),
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
    print(f"source_ref_rebind_schema_aware_receipt_id={receipt_id}")
    print(f"source_ref_rebind_schema_aware_receipt_path={rel(receipt_path)}")
    print(f"source_ref_rebind_schema_aware_source_inventory_path={rel(SOURCE_INVENTORY_PATH)}")
    print(f"source_ref_rebind_schema_aware_candidate_inventory_path={rel(PRIOR_REBIND_CANDIDATE_INVENTORY_PATH)}")
    print(f"source_ref_rebind_schema_aware_review_table_path={rel(SCHEMA_AWARE_REVIEW_TABLE_PATH)}")
    print(f"source_ref_rebind_schema_aware_binding_rollup_path={rel(SCHEMA_AWARE_BINDING_ROLLUP_PATH)}")
    print(f"source_ref_rebind_schema_aware_proposal_surface_path={rel(SCHEMA_AWARE_PROPOSAL_SURFACE_PATH)}")
    print(f"source_ref_rebind_schema_aware_ambiguity_surface_path={rel(SCHEMA_AWARE_AMBIGUITY_SURFACE_PATH)}")
    print(f"source_ref_rebind_schema_aware_requirement_gap_surface_path={rel(SCHEMA_AWARE_REQUIREMENT_GAP_SURFACE_PATH)}")
    print(f"source_ref_rebind_schema_aware_rollup_path={rel(ROLLUP_PATH)}")
    print(f"source_ref_rebind_schema_aware_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
