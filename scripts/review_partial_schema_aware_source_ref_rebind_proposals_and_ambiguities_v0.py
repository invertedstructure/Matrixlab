#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_PARTIAL_SCHEMA_AWARE_SOURCE_REF_REBIND_PROPOSALS_AND_AMBIGUITIES_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_PARTIAL_SCHEMA_AWARE_REBIND_REVIEW"
MODE = "PARTIAL_SCHEMA_AWARE_REBIND_REVIEW / PROPOSAL_AMBIGUITY_GAP_SPLIT / NO_REBIND_APPLICATION / NO_VALUES / NO_METADATA"
BUILD_MODE = "PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_AND_AMBIGUITY_REVIEW_ONLY"

SOURCE_SCHEMA_AWARE_RECEIPT_ID = "e85a9b37"
SOURCE_SCHEMA_AWARE_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_candidates_with_accepted_schema_overlay_v0_receipts/e85a9b37.json"
SOURCE_SCHEMA_AWARE_SOURCE_INVENTORY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_candidates_with_accepted_schema_overlay_v0/typed_machine_readable_source_ref_rebind_accepted_schema_overlay_source_inventory_v0.json"
SOURCE_SCHEMA_AWARE_REFERENCE_INPUT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_candidates_with_accepted_schema_overlay_v0/typed_machine_readable_source_ref_rebind_accepted_schema_overlay_reference_input_v0.json"
SOURCE_SCHEMA_AWARE_CANDIDATE_INVENTORY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_candidates_with_accepted_schema_overlay_v0/typed_machine_readable_source_ref_rebind_prior_candidate_inventory_v0.json"
SOURCE_SCHEMA_AWARE_REVIEW_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_candidates_with_accepted_schema_overlay_v0/typed_machine_readable_source_ref_rebind_schema_aware_candidate_review_table_v0.json"
SOURCE_SCHEMA_AWARE_BINDING_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_candidates_with_accepted_schema_overlay_v0/typed_machine_readable_source_ref_rebind_schema_aware_binding_rollup_v0.json"
SOURCE_SCHEMA_AWARE_PROPOSAL_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_candidates_with_accepted_schema_overlay_v0/typed_machine_readable_source_ref_rebind_schema_aware_proposal_surface_v0.json"
SOURCE_SCHEMA_AWARE_AMBIGUITY_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_candidates_with_accepted_schema_overlay_v0/typed_machine_readable_source_ref_rebind_schema_aware_ambiguity_surface_v0.json"
SOURCE_SCHEMA_AWARE_REQUIREMENT_GAP_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_candidates_with_accepted_schema_overlay_v0/typed_machine_readable_source_ref_rebind_schema_aware_requirement_gap_surface_v0.json"
SOURCE_SCHEMA_AWARE_DECISION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_candidates_with_accepted_schema_overlay_v0/typed_machine_readable_source_ref_rebind_schema_aware_downstream_decision_table_v0.json"
SOURCE_SCHEMA_AWARE_REVIEW_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_candidates_with_accepted_schema_overlay_v0/typed_machine_readable_source_ref_rebind_schema_aware_review_packet_v0.json"
SOURCE_SCHEMA_AWARE_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_candidates_with_accepted_schema_overlay_v0/typed_machine_readable_source_ref_rebind_schema_aware_classification_v0.json"
SOURCE_SCHEMA_AWARE_AUTHORITY_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_candidates_with_accepted_schema_overlay_v0/typed_machine_readable_source_ref_rebind_schema_aware_authority_boundary_v0.json"
SOURCE_SCHEMA_AWARE_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_candidates_with_accepted_schema_overlay_v0/typed_machine_readable_source_ref_rebind_schema_aware_rollup_v0.json"
SOURCE_SCHEMA_AWARE_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_candidates_with_accepted_schema_overlay_v0/typed_machine_readable_source_ref_rebind_schema_aware_profile_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_review_assessment_v0.json"
PROPOSAL_REVIEW_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_review_table_v0.json"
PROPOSAL_REVIEW_SURFACE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_review_surface_v0.json"
AMBIGUITY_REVIEW_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_ambiguity_review_table_v0.json"
AMBIGUITY_REPAIR_SURFACE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_ambiguity_repair_surface_v0.json"
REQUIREMENT_GAP_REVIEW_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_requirement_gap_review_table_v0.json"
REQUIREMENT_GAP_REPAIR_SURFACE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_requirement_gap_repair_surface_v0.json"
BRANCH_SPLIT_SURFACE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_split_surface_v0.json"
PROPOSAL_HOLD_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_hold_contract_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_downstream_decision_table_v0.json"
REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_review_packet_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_SCHEMA_AWARE_RECEIPT_PATH,
    SOURCE_SCHEMA_AWARE_SOURCE_INVENTORY_PATH,
    SOURCE_SCHEMA_AWARE_REFERENCE_INPUT_PATH,
    SOURCE_SCHEMA_AWARE_CANDIDATE_INVENTORY_PATH,
    SOURCE_SCHEMA_AWARE_REVIEW_TABLE_PATH,
    SOURCE_SCHEMA_AWARE_BINDING_ROLLUP_PATH,
    SOURCE_SCHEMA_AWARE_PROPOSAL_SURFACE_PATH,
    SOURCE_SCHEMA_AWARE_AMBIGUITY_SURFACE_PATH,
    SOURCE_SCHEMA_AWARE_REQUIREMENT_GAP_SURFACE_PATH,
    SOURCE_SCHEMA_AWARE_DECISION_TABLE_PATH,
    SOURCE_SCHEMA_AWARE_REVIEW_PACKET_PATH,
    SOURCE_SCHEMA_AWARE_CLASSIFICATION_PATH,
    SOURCE_SCHEMA_AWARE_AUTHORITY_BOUNDARY_PATH,
    SOURCE_SCHEMA_AWARE_ROLLUP_PATH,
    SOURCE_SCHEMA_AWARE_PROFILE_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_WITH_ACCEPTED_SCHEMA_OVERLAY_REVIEWED_PARTIAL_PROPOSALS_REMAINING_AMBIGUITY"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_WITH_ACCEPTED_SCHEMA_OVERLAY_REVIEWED_PARTIAL_PROPOSALS_REMAINING_AMBIGUITY"
EXPECTED_SOURCE_NEXT = "REVIEW_PARTIAL_SCHEMA_AWARE_SOURCE_REF_REBIND_PROPOSALS_AND_AMBIGUITIES_V0"

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

def list_records(obj: Dict[str, Any], keys: List[str]) -> List[Dict[str, Any]]:
    for k in keys:
        v = obj.get(k)
        if isinstance(v, list):
            return [x for x in v if isinstance(x, dict)]
    return []

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    receipt = read_json(SOURCE_SCHEMA_AWARE_RECEIPT_PATH)
    summary = receipt.get("machine_readable_source_ref_rebind_schema_aware_summary", {})
    proposal_surface = read_json(SOURCE_SCHEMA_AWARE_PROPOSAL_SURFACE_PATH)
    ambiguity_surface = read_json(SOURCE_SCHEMA_AWARE_AMBIGUITY_SURFACE_PATH)
    requirement_gap_surface = read_json(SOURCE_SCHEMA_AWARE_REQUIREMENT_GAP_SURFACE_PATH)
    review_packet = read_json(SOURCE_SCHEMA_AWARE_REVIEW_PACKET_PATH)
    classification = read_json(SOURCE_SCHEMA_AWARE_CLASSIFICATION_PATH)
    authority = read_json(SOURCE_SCHEMA_AWARE_AUTHORITY_BOUNDARY_PATH)
    rollup = read_json(SOURCE_SCHEMA_AWARE_ROLLUP_PATH)
    profile = read_json(SOURCE_SCHEMA_AWARE_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_SCHEMA_AWARE_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_schema_aware_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("accepted_schema_overlay_reference_consumed") is not True:
        failures.append("accepted_schema_overlay_reference_not_consumed")
    if summary.get("prior_rebind_receipt_count") != 5:
        failures.append("prior_rebind_receipt_count_not_5")
    if summary.get("candidate_record_count") != 1505:
        failures.append(f"candidate_record_count_changed:{summary.get('candidate_record_count')}")
    if summary.get("binding_count") != 524:
        failures.append(f"binding_count_changed:{summary.get('binding_count')}")
    if summary.get("unique_schema_aware_rebind_proposal_count") != 4:
        failures.append(f"unique_proposal_count_changed:{summary.get('unique_schema_aware_rebind_proposal_count')}")
    if summary.get("ambiguous_binding_count") != 22:
        failures.append(f"ambiguous_binding_count_changed:{summary.get('ambiguous_binding_count')}")
    if summary.get("requirement_gap_binding_count") != 498:
        failures.append(f"requirement_gap_binding_count_changed:{summary.get('requirement_gap_binding_count')}")

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
        "dominance_rule_applied",
        "values_authorized",
        "values_applied",
        "null_reasons_accepted",
        "source_packet_materialized_for_review",
        "metadata_populated",
        "target_selected_for_build",
        "runtime_patch_applied",
        "c5_opened",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if summary.get(key) is not False:
            failures.append(f"source_summary_forbidden_true:{key}")
    if summary.get("ready_discriminator_count") != 0:
        failures.append("ready_discriminator_nonzero")

    proposals = list_records(proposal_surface, ["proposals", "records"])
    ambiguities = list_records(ambiguity_surface, ["ambiguous_bindings", "records"])
    gaps = list_records(requirement_gap_surface, ["requirement_gaps", "records"])
    if len(proposals) != 4:
        failures.append(f"proposal_surface_count_not_4:{len(proposals)}")
    if len(ambiguities) != 22:
        failures.append(f"ambiguity_surface_count_not_22:{len(ambiguities)}")
    if len(gaps) != 498:
        failures.append(f"requirement_gap_surface_count_not_498:{len(gaps)}")

    packet_summary = review_packet.get("summary", {})
    if packet_summary.get("unique_proposal_count") != 4:
        failures.append("review_packet_unique_proposal_count_not_4")
    if packet_summary.get("ambiguous_binding_count") != 22:
        failures.append("review_packet_ambiguous_count_not_22")
    if packet_summary.get("requirement_gap_binding_count") != 498:
        failures.append("review_packet_gap_count_not_498")
    if classification.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("classification_status_wrong")
    if authority.get("may_apply_rebinds") is not False:
        failures.append("authority_allows_rebind_application")
    if authority.get("may_emit_rebind_proposals_for_review") is not True:
        failures.append("authority_does_not_allow_proposal_review")
    if rollup.get("unique_schema_aware_rebind_proposal_count") != 4:
        failures.append("rollup_unique_proposal_count_not_4")
    if rollup.get("rebinds_applied_count") != 0:
        failures.append("rollup_rebinds_nonzero")
    if profile.get("unique_schema_aware_rebind_proposal_count") != 4:
        failures.append("profile_unique_proposal_count_not_4")
    if profile.get("rebinds_applied") is not False:
        failures.append("profile_rebinds_applied_true")

    return failures, {
        "receipt": receipt,
        "summary": summary,
        "proposals": proposals,
        "ambiguities": ambiguities,
        "gaps": gaps,
        "proposal_surface": proposal_surface,
        "ambiguity_surface": ambiguity_surface,
        "requirement_gap_surface": requirement_gap_surface,
        "review_packet": review_packet,
        "rollup": rollup,
    }

def review_proposals(proposals: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[str]]:
    rows: List[Dict[str, Any]] = []
    failures: List[str] = []
    seen_bindings = set()
    for idx, p in enumerate(proposals):
        binding_key = p.get("binding_key")
        candidate_ref = p.get("candidate_ref")
        proposal_status = p.get("proposal_status")
        source_receipt_id = p.get("source_receipt_id")
        score = p.get("schema_requirement_score")
        row_failures: List[str] = []
        if not binding_key:
            row_failures.append("missing_binding_key")
        if binding_key in seen_bindings:
            row_failures.append("duplicate_binding_key")
        if binding_key:
            seen_bindings.add(binding_key)
        if not candidate_ref:
            row_failures.append("missing_candidate_ref")
        if proposal_status != "PROPOSED_FOR_REVIEW_ONLY_NOT_APPLIED":
            row_failures.append(f"unexpected_proposal_status:{proposal_status}")
        if source_receipt_id in (None, ""):
            row_failures.append("missing_source_receipt_id")
        if not isinstance(score, int):
            row_failures.append("schema_requirement_score_not_int")
        rows.append({
            "proposal_review_id": "partial_schema_aware_proposal_review_" + sha8({"idx": idx, "proposal": p}),
            "binding_key": binding_key,
            "candidate_ref": candidate_ref,
            "source_receipt_id": source_receipt_id,
            "source_artifact_path": p.get("source_artifact_path"),
            "schema_requirement_score": score,
            "proposal_status": proposal_status,
            "proposal_review_status": "PROPOSAL_READY_FOR_SEPARATE_REVIEW_NOT_APPLICATION" if not row_failures else "PROPOSAL_REVIEW_DEFECT",
            "proposal_review_failures": row_failures,
            "rebind_applied": False,
        })
        failures.extend([f"{binding_key or idx}:{x}" for x in row_failures])
    return rows, failures

def review_ambiguities(ambiguities: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    rows: List[Dict[str, Any]] = []
    top_counts = Counter()
    for idx, a in enumerate(ambiguities):
        top_count = a.get("top_candidate_count")
        top_counts[str(top_count)] += 1
        rows.append({
            "ambiguity_review_id": "partial_schema_aware_ambiguity_review_" + sha8({"idx": idx, "ambiguity": a}),
            "binding_key": a.get("binding_key"),
            "ambiguity_status": a.get("ambiguity_status"),
            "top_score": a.get("top_score"),
            "top_candidate_count": top_count,
            "top_candidate_refs": a.get("top_candidate_refs", []),
            "ambiguity_review_status": "RESIDUAL_TOP_CANDIDATES_TIED_REPAIR_REQUIRED",
            "recommended_repair_class": "TIE_BREAKER_EVIDENCE_REQUIRED",
            "rebind_applied": False,
        })
    return rows, dict(sorted(top_counts.items()))

def review_gaps(gaps: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    rows: List[Dict[str, Any]] = []
    missing_counts = Counter()
    for idx, g in enumerate(gaps):
        counts = g.get("missing_requirement_counts") or {}
        for k, v in counts.items():
            try:
                missing_counts[k] += int(v)
            except Exception:
                missing_counts[k] += 1
        rows.append({
            "requirement_gap_review_id": "partial_schema_aware_requirement_gap_review_" + sha8({"idx": idx, "gap": g}),
            "binding_key": g.get("binding_key"),
            "gap_status": g.get("gap_status"),
            "candidate_count": g.get("candidate_count"),
            "top_score": g.get("top_score"),
            "missing_requirement_counts": counts,
            "requirement_gap_review_status": "SCHEMA_REQUIREMENT_EVIDENCE_GAP_REPAIR_REQUIRED",
            "recommended_repair_class": "MISSING_SCHEMA_EVIDENCE_SURFACE_REQUIRED",
            "rebind_applied": False,
        })
    return rows, dict(sorted(missing_counts.items()))

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, source = validate_basis()

    proposals = source.get("proposals", [])
    ambiguities = source.get("ambiguities", [])
    gaps = source.get("gaps", [])

    proposal_rows, proposal_failures = review_proposals(proposals)
    ambiguity_rows, ambiguity_top_counts = review_ambiguities(ambiguities)
    gap_rows, missing_requirement_counts = review_gaps(gaps)

    proposal_ready_count = sum(1 for r in proposal_rows if r["proposal_review_status"] == "PROPOSAL_READY_FOR_SEPARATE_REVIEW_NOT_APPLICATION")
    ambiguity_repair_count = len(ambiguity_rows)
    gap_repair_count = len(gap_rows)

    if failures:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_SOURCE_REF_REBIND_REVIEW_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_PARTIAL_SCHEMA_AWARE_SOURCE_REF_REBIND_REVIEW_BASIS_V0"
        branch_split_ready = False
    elif proposal_failures:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_SOURCE_REF_REBIND_REVIEWED_PROPOSAL_DEFECTS_REPAIR_REQUIRED"
        reason_codes = [
            "PARTIAL_SCHEMA_AWARE_REBIND_REVIEW_COMPLETE",
            "PROPOSAL_REVIEW_DEFECTS_FOUND",
            "NO_REBINDS_APPLIED",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
        ] + proposal_failures
        next_edge = "REPAIR_SCHEMA_AWARE_SOURCE_REF_REBIND_PROPOSAL_SURFACE_V0"
        branch_split_ready = False
    else:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_SOURCE_REF_REBIND_REVIEWED_BRANCH_SPLIT_REQUIRED"
        reason_codes = [
            "PARTIAL_SCHEMA_AWARE_REBIND_REVIEW_COMPLETE",
            "FOUR_PROPOSALS_READY_FOR_SEPARATE_REVIEW_NOT_APPLICATION",
            "RESIDUAL_AMBIGUITY_BRANCH_IDENTIFIED",
            "REQUIREMENT_GAP_REPAIR_BRANCH_IDENTIFIED",
            "BRANCH_SPLIT_REQUIRED_BEFORE_ANY_REBIND_APPLICATION",
            "NO_REBINDS_APPLIED",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
        ]
        next_edge = "BUILD_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_AND_REPAIR_SURFACE_V0"
        branch_split_ready = True

    proposal_review_surface = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_review_surface_v0",
        "proposal_review_surface_status": "PROPOSALS_READY_FOR_SEPARATE_REVIEW_NOT_APPLICATION" if proposal_ready_count == 4 else "PROPOSAL_SURFACE_REPAIR_REQUIRED",
        "proposal_ready_count": proposal_ready_count,
        "proposal_review_failure_count": len(proposal_failures),
        "proposal_rows": proposal_rows,
        "rebinds_applied": False,
    }

    ambiguity_repair_surface = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_ambiguity_repair_surface_v0",
        "ambiguity_repair_surface_status": "RESIDUAL_AMBIGUITY_REPAIR_REQUIRED",
        "ambiguous_binding_count": ambiguity_repair_count,
        "top_candidate_count_distribution": ambiguity_top_counts,
        "recommended_repair_action": "build schema-aware tie-breaker evidence surface for residual tied candidates",
        "rebinds_applied": False,
    }

    requirement_gap_repair_surface = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_requirement_gap_repair_surface_v0",
        "requirement_gap_repair_surface_status": "SCHEMA_REQUIREMENT_GAP_REPAIR_REQUIRED",
        "requirement_gap_binding_count": gap_repair_count,
        "missing_requirement_counts": missing_requirement_counts,
        "recommended_repair_action": "build missing schema-evidence surface for requirement-gap bindings",
        "rebinds_applied": False,
        "metadata_populated": False,
    }

    branch_split_surface = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_surface_v0",
        "branch_split_status": "BRANCH_SPLIT_REQUIRED_BEFORE_ANY_REBIND_APPLICATION" if branch_split_ready else "BRANCH_SPLIT_NOT_READY",
        "branches": [
            {
                "branch_id": "proposal_review_branch",
                "status": "READY_FOR_SEPARATE_REVIEW_NOT_APPLICATION" if proposal_ready_count else "NO_PROPOSALS",
                "binding_count": proposal_ready_count,
                "allowed_next": "review proposal correctness and hold/application preconditions only",
                "forbidden": ["apply rebinds", "populate metadata", "extract values"],
            },
            {
                "branch_id": "ambiguity_repair_branch",
                "status": "REPAIR_REQUIRED",
                "binding_count": ambiguity_repair_count,
                "allowed_next": "build tie-breaker evidence surface",
                "forbidden": ["choose tied candidate by score alone", "apply rebinds"],
            },
            {
                "branch_id": "requirement_gap_repair_branch",
                "status": "REPAIR_REQUIRED",
                "binding_count": gap_repair_count,
                "allowed_next": "build missing schema requirement evidence surface",
                "forbidden": ["invent missing source evidence", "populate metadata"],
            },
        ],
        "total_binding_count": proposal_ready_count + ambiguity_repair_count + gap_repair_count,
    }

    proposal_hold_contract = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_hold_contract_v0",
        "hold_contract_status": "PARTIAL_PROPOSALS_HELD_PENDING_BRANCH_SPLIT_REVIEW",
        "proposal_ready_count": proposal_ready_count,
        "held_reason": "partial proposals are useful but residual ambiguity/gap branches remain; no rebind application until branch policy is explicit",
        "may_review_proposals": True,
        "may_apply_proposals": False,
        "may_discard_residual_bindings": False,
        "must_preserve_residual_ambiguity_and_gap_surfaces": True,
    }

    downstream_decision_table = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_downstream_decision_table_v0",
        "decision_status": "PARTIAL_SCHEMA_AWARE_REBIND_REVIEW_DECISION_EMITTED",
        "records": [
            {
                "decision": "BUILD_BRANCH_SPLIT_AND_REPAIR_SURFACE",
                "selected": branch_split_ready,
                "next_unit": "BUILD_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_AND_REPAIR_SURFACE_V0",
                "why": "4 proposal-ready bindings exist, but 22 ambiguity and 498 requirement-gap bindings remain",
            },
            {
                "decision": "REVIEW_PROPOSALS_ONLY",
                "selected": False,
                "next_unit": "REVIEW_SCHEMA_AWARE_SOURCE_REF_REBIND_PROPOSALS_V0",
                "why": "not selected because proposal-only review would hide residual branches",
            },
            {
                "decision": "APPLY_REBINDS",
                "selected": False,
                "next_unit": None,
                "why": "not authorized",
            },
        ],
    }

    review_packet = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_review_packet_v0",
        "review_packet_status": status,
        "summary": {
            "proposal_ready_count": proposal_ready_count,
            "proposal_review_failure_count": len(proposal_failures),
            "ambiguous_binding_count": ambiguity_repair_count,
            "requirement_gap_binding_count": gap_repair_count,
            "branch_split_ready": branch_split_ready,
            "rebinds_applied": False,
            "metadata_populated": False,
        },
        "recommended_next": next_edge,
    }

    classification = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "partial_schema_aware_rebind_review_complete": not bool(failures),
        "proposal_ready_count": proposal_ready_count,
        "proposal_review_failure_count": len(proposal_failures),
        "ambiguous_binding_count": ambiguity_repair_count,
        "requirement_gap_binding_count": gap_repair_count,
        "branch_split_required": branch_split_ready,
        "proposal_hold_contract_emitted": True,
        "ambiguity_repair_surface_emitted": True,
        "requirement_gap_repair_surface_emitted": True,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_authority_boundary_v0",
        "status": status,
        "may_review_partial_proposals": True,
        "may_build_branch_split_surface": branch_split_ready,
        "may_build_ambiguity_repair_surface": True,
        "may_build_requirement_gap_repair_surface": True,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "partial_schema_aware_rebind_review_count": 1,
        "proposal_ready_count": proposal_ready_count,
        "proposal_review_failure_count": len(proposal_failures),
        "ambiguous_binding_count": ambiguity_repair_count,
        "requirement_gap_binding_count": gap_repair_count,
        "branch_split_required_count": 1 if branch_split_ready else 0,
        "proposal_hold_contract_emitted_count": 1,
        "ambiguity_repair_surface_emitted_count": 1,
        "requirement_gap_repair_surface_emitted_count": 1,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_profile_v0",
        "profile_id": "partial_schema_aware_rebind_profile_" + sha8(rollup),
        "status": status,
        "partial_schema_aware_rebind_review_complete": not bool(failures),
        "proposal_ready_count": proposal_ready_count,
        "ambiguous_binding_count": ambiguity_repair_count,
        "requirement_gap_binding_count": gap_repair_count,
        "branch_split_required": branch_split_ready,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Partial schema-aware rebind proposals were reviewed and separated from residual ambiguity and requirement-gap repair branches. This unit preserves proposals but does not apply rebinds, values, metadata, runtime patches, C5, or schema reuse.",
        "proposal_ready_count": proposal_ready_count,
        "ambiguous_binding_count": ambiguity_repair_count,
        "requirement_gap_binding_count": gap_repair_count,
        "branch_split_required_count": rollup["branch_split_required_count"],
        "rebinds_applied_count": 0,
        "metadata_populated_count": 0,
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
    }

    trace = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_transition_trace_v0",
        "trace": [
            {
                "step": "consume_schema_aware_rebind_review",
                "question": "what did accepted overlay distinguish",
                "answer": "4 proposal-ready, 22 ambiguous, 498 requirement-gap bindings",
                "taken": "review proposal/ambiguity/gap surfaces",
            },
            {
                "step": "hold_partial_proposals",
                "question": "can the 4 proposals be applied now",
                "answer": "no",
                "taken": "emit proposal hold contract",
            },
            {
                "step": "split_residual_branches",
                "question": "what branch shape is required",
                "answer": "proposal review branch plus ambiguity repair branch plus requirement-gap repair branch",
                "taken": next_edge,
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    review_assessment = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_review_assessment_v0",
        "assessment_status": status,
        "source_schema_aware_receipt_id": SOURCE_SCHEMA_AWARE_RECEIPT_ID,
        "proposal_ready_count": proposal_ready_count,
        "proposal_review_failure_count": len(proposal_failures),
        "ambiguous_binding_count": ambiguity_repair_count,
        "requirement_gap_binding_count": gap_repair_count,
        "branch_split_required": branch_split_ready,
        "recommended_next": next_edge,
    }

    write_json(REVIEW_ASSESSMENT_PATH, review_assessment)
    write_json(PROPOSAL_REVIEW_TABLE_PATH, {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_review_table_v0",
        "proposal_review_table_status": "PROPOSAL_REVIEW_TABLE_EMITTED",
        "proposal_ready_count": proposal_ready_count,
        "proposal_review_failure_count": len(proposal_failures),
        "records": proposal_rows,
    })
    write_json(PROPOSAL_REVIEW_SURFACE_PATH, proposal_review_surface)
    write_json(AMBIGUITY_REVIEW_TABLE_PATH, {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_ambiguity_review_table_v0",
        "ambiguity_review_table_status": "AMBIGUITY_REVIEW_TABLE_EMITTED",
        "ambiguous_binding_count": ambiguity_repair_count,
        "records": ambiguity_rows,
    })
    write_json(AMBIGUITY_REPAIR_SURFACE_PATH, ambiguity_repair_surface)
    write_json(REQUIREMENT_GAP_REVIEW_TABLE_PATH, {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_requirement_gap_review_table_v0",
        "requirement_gap_review_table_status": "REQUIREMENT_GAP_REVIEW_TABLE_EMITTED",
        "requirement_gap_binding_count": gap_repair_count,
        "records": gap_rows,
    })
    write_json(REQUIREMENT_GAP_REPAIR_SURFACE_PATH, requirement_gap_repair_surface)
    write_json(BRANCH_SPLIT_SURFACE_PATH, branch_split_surface)
    write_json(PROPOSAL_HOLD_CONTRACT_PATH, proposal_hold_contract)
    write_json(DOWNSTREAM_DECISION_TABLE_PATH, downstream_decision_table)
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
        "PARTIAL_REBIND_REVIEW_0_SOURCE_RECEIPT_CONSUMED": SOURCE_SCHEMA_AWARE_RECEIPT_PATH.exists(),
        "PARTIAL_REBIND_REVIEW_1_PROPOSAL_SURFACE_CONSUMED": SOURCE_SCHEMA_AWARE_PROPOSAL_SURFACE_PATH.exists(),
        "PARTIAL_REBIND_REVIEW_2_AMBIGUITY_SURFACE_CONSUMED": SOURCE_SCHEMA_AWARE_AMBIGUITY_SURFACE_PATH.exists(),
        "PARTIAL_REBIND_REVIEW_3_REQUIREMENT_GAP_SURFACE_CONSUMED": SOURCE_SCHEMA_AWARE_REQUIREMENT_GAP_SURFACE_PATH.exists(),
        "PARTIAL_REBIND_REVIEW_4_FOUR_PROPOSALS_REVIEWED": proposal_ready_count == 4,
        "PARTIAL_REBIND_REVIEW_5_TWENTY_TWO_AMBIGUITIES_REVIEWED": ambiguity_repair_count == 22,
        "PARTIAL_REBIND_REVIEW_6_FOUR_NINETY_EIGHT_GAPS_REVIEWED": gap_repair_count == 498,
        "PARTIAL_REBIND_REVIEW_7_BRANCH_SPLIT_SURFACE_EMITTED": BRANCH_SPLIT_SURFACE_PATH.exists(),
        "PARTIAL_REBIND_REVIEW_8_PROPOSAL_HOLD_CONTRACT_EMITTED": PROPOSAL_HOLD_CONTRACT_PATH.exists(),
        "PARTIAL_REBIND_REVIEW_9_NO_GLOBAL_SCHEMA_APPLICATION": rollup["schema_overlay_applied_globally_count"] == 0,
        "PARTIAL_REBIND_REVIEW_10_NO_REUSABLE_SCHEMA_AUTHORIZED": rollup["reusable_schema_authorized_count"] == 0,
        "PARTIAL_REBIND_REVIEW_11_NO_PREAPPROVED_SCHEMA_AUTHORIZED": rollup["preapproved_schema_authorized_count"] == 0,
        "PARTIAL_REBIND_REVIEW_12_NO_VALIDATOR_REGISTRY_ENTRY": rollup["validator_registry_entry_created_count"] == 0,
        "PARTIAL_REBIND_REVIEW_13_NO_FUTURE_AUTOMATIC_USE": rollup["future_automatic_use_allowed_count"] == 0,
        "PARTIAL_REBIND_REVIEW_14_NO_TYPING_RULE_APPLIED": rollup["typing_rule_applied_count"] == 0,
        "PARTIAL_REBIND_REVIEW_15_NO_FIELD_POLICY_MODIFIED": rollup["field_policy_modified_count"] == 0,
        "PARTIAL_REBIND_REVIEW_16_NO_CANDIDATE_ARTIFACT_MODIFIED": rollup["candidate_artifact_modified_count"] == 0,
        "PARTIAL_REBIND_REVIEW_17_NO_ROW_LOCATOR_APPLIED": rollup["source_row_locator_applied_count"] == 0,
        "PARTIAL_REBIND_REVIEW_18_NO_REBINDS_APPLIED": rollup["rebinds_applied_count"] == 0,
        "PARTIAL_REBIND_REVIEW_19_NO_VALUES_AUTHORIZED": rollup["values_authorized_count"] == 0,
        "PARTIAL_REBIND_REVIEW_20_NO_VALUES_APPLIED": rollup["values_applied_count"] == 0,
        "PARTIAL_REBIND_REVIEW_21_NO_METADATA_POPULATION": rollup["metadata_populated_count"] == 0,
        "PARTIAL_REBIND_REVIEW_22_NO_DISCRIMINATOR_READY": rollup["ready_discriminator_count"] == 0,
        "PARTIAL_REBIND_REVIEW_23_NO_TARGET_SELECTED": rollup["target_selected_for_build_count"] == 0,
        "PARTIAL_REBIND_REVIEW_24_NO_RUNTIME_PATCH": rollup["runtime_patch_applied_count"] == 0,
        "PARTIAL_REBIND_REVIEW_25_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "PARTIAL_REBIND_REVIEW_26_NO_LATEST_FILE_GUESSING": rollup["latest_file_guessing_count"] == 0,
        "PARTIAL_REBIND_REVIEW_27_NO_MTIME_SELECTION": rollup["mtime_selection_count"] == 0,
        "PARTIAL_REBIND_REVIEW_28_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "PARTIAL_REBIND_REVIEW_29_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "accepted_schema_overlay_reference_this_application_contract_only",
        "PARTIAL_REBIND_REVIEW_30_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "proposal_ready": proposal_ready_count,
        "ambiguity": ambiguity_repair_count,
        "gap": gap_repair_count,
        "rebinds": 0,
        "metadata": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_schema_aware_rebind_receipt_id": SOURCE_SCHEMA_AWARE_RECEIPT_ID,
        "machine_readable_partial_schema_aware_rebind_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "partial_schema_aware_rebind_review_complete": not bool(failures),
            "proposal_ready_count": proposal_ready_count,
            "proposal_review_failure_count": len(proposal_failures),
            "ambiguous_binding_count": ambiguity_repair_count,
            "requirement_gap_binding_count": gap_repair_count,
            "branch_split_required": branch_split_ready,
            "proposal_hold_contract_emitted": True,
            "ambiguity_repair_surface_emitted": True,
            "requirement_gap_repair_surface_emitted": True,
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
            "review_assessment": rel(REVIEW_ASSESSMENT_PATH),
            "proposal_review_table": rel(PROPOSAL_REVIEW_TABLE_PATH),
            "proposal_review_surface": rel(PROPOSAL_REVIEW_SURFACE_PATH),
            "ambiguity_review_table": rel(AMBIGUITY_REVIEW_TABLE_PATH),
            "ambiguity_repair_surface": rel(AMBIGUITY_REPAIR_SURFACE_PATH),
            "requirement_gap_review_table": rel(REQUIREMENT_GAP_REVIEW_TABLE_PATH),
            "requirement_gap_repair_surface": rel(REQUIREMENT_GAP_REPAIR_SURFACE_PATH),
            "branch_split_surface": rel(BRANCH_SPLIT_SURFACE_PATH),
            "proposal_hold_contract": rel(PROPOSAL_HOLD_CONTRACT_PATH),
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
    print(f"partial_schema_aware_rebind_receipt_id={receipt_id}")
    print(f"partial_schema_aware_rebind_receipt_path={rel(receipt_path)}")
    print(f"partial_schema_aware_rebind_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"partial_schema_aware_rebind_proposal_review_table_path={rel(PROPOSAL_REVIEW_TABLE_PATH)}")
    print(f"partial_schema_aware_rebind_proposal_review_surface_path={rel(PROPOSAL_REVIEW_SURFACE_PATH)}")
    print(f"partial_schema_aware_rebind_ambiguity_repair_surface_path={rel(AMBIGUITY_REPAIR_SURFACE_PATH)}")
    print(f"partial_schema_aware_rebind_requirement_gap_repair_surface_path={rel(REQUIREMENT_GAP_REPAIR_SURFACE_PATH)}")
    print(f"partial_schema_aware_rebind_branch_split_surface_path={rel(BRANCH_SPLIT_SURFACE_PATH)}")
    print(f"partial_schema_aware_rebind_proposal_hold_contract_path={rel(PROPOSAL_HOLD_CONTRACT_PATH)}")
    print(f"partial_schema_aware_rebind_rollup_path={rel(ROLLUP_PATH)}")
    print(f"partial_schema_aware_rebind_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
