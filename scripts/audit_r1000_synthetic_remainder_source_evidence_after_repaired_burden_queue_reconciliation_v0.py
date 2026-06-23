#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "AUDIT_R1000_SYNTHETIC_REMAINDER_SOURCE_EVIDENCE_AFTER_REPAIRED_BURDEN_QUEUE_RECONCILIATION_V0"
TARGET_UNIT_ID = "r1000_synthetic_remainder.source_evidence_audit_after_repaired_burden_queue.v0"

SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID = "982ff0d0"
SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID = "46694b59"
SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID = "9b9cb3eb"
SOURCE_REPAIRED_INSPECTION_RECEIPT_ID = "dab2b21d"
SOURCE_REPAIRED_IDENTITY_REVIEW_RECEIPT_ID = "39f2fbe0"
SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID = "7cfe198f"
SOURCE_IDENTITY_REVIEW_RECEIPT_ID = "82c10dfc"
SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID = "1cb51143"
SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID = "d3135cdb"
SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID = "dea88520"
SOURCE_SELECTION_RECEIPT_ID = "7c561212"
SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID = "38604be8"
SELECTED_PRESSURE_GROUP_ID = "025fdd0c"

OUT_DIR = ROOT / "data" / "r1000_synthetic_remainder_source_evidence_audit_after_repaired_burden_queue_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_synthetic_remainder_source_evidence_audit_after_repaired_burden_queue_v0_receipts"

AUDIT_SURFACE_PATH = OUT_DIR / "r1000_synthetic_remainder_source_evidence_audit_surface_after_repaired_burden_queue.json"
EVIDENCE_CANDIDATES_PATH = OUT_DIR / "r1000_synthetic_remainder_source_evidence_candidates_after_repaired_burden_queue.json"
AUDIT_DECISION_PATH = OUT_DIR / "r1000_synthetic_remainder_source_evidence_audit_decision_after_repaired_burden_queue.json"
EXPECTED_LIMIT_PACKET_PATH = OUT_DIR / "r1000_synthetic_remainder_expected_queue_resolution_limit_packet_after_repaired_burden_queue.json"
INSPECTION_BLOCK_PACKET_PATH = OUT_DIR / "r1000_synthetic_remainder_source_audit_inspection_block_packet_after_repaired_burden_queue.json"
QUEUE_CLOSURE_CANDIDATE_PACKET_PATH = OUT_DIR / "r1000_synthetic_remainder_queue_closure_candidate_packet_after_repaired_burden_queue.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_synthetic_remainder_source_evidence_audit_transition_trace_after_repaired_burden_queue.json"
REPORT_PATH = OUT_DIR / "r1000_synthetic_remainder_source_evidence_audit_report_after_repaired_burden_queue.json"

IDENTITY_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_selected_synthetic_remainder_identity_surface_review_after_repaired_burden_queue_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID}.json"
IDENTITY_SURFACE_PATH = ROOT / "data" / "r1000_selected_synthetic_remainder_identity_surface_review_after_repaired_burden_queue_v0" / "r1000_selected_synthetic_remainder_identity_surface_after_repaired_burden_queue.json"
IDENTITY_DECISION_PATH = ROOT / "data" / "r1000_selected_synthetic_remainder_identity_surface_review_after_repaired_burden_queue_v0" / "r1000_selected_synthetic_remainder_identity_review_decision_after_repaired_burden_queue.json"
IDENTITY_DEFECT_PACKET_PATH = ROOT / "data" / "r1000_selected_synthetic_remainder_identity_surface_review_after_repaired_burden_queue_v0" / "r1000_selected_synthetic_remainder_identity_defect_packet_after_repaired_burden_queue.json"
SOURCE_AUDIT_RECOMMENDATION_PACKET_PATH = ROOT / "data" / "r1000_selected_synthetic_remainder_identity_surface_review_after_repaired_burden_queue_v0" / "r1000_selected_synthetic_remainder_source_audit_recommendation_packet_after_repaired_burden_queue.json"

SELECTION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_repaired_burden_group_queue_reconciliation_v0_receipts" / f"{SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID}.json"
SELECTED_GROUP_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_repaired_burden_group_queue_reconciliation_v0" / "r1000_selected_pressure_group_after_repaired_burden_queue_reconciliation.json"
SELECTION_AUTHORITY_PACKET_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_repaired_burden_group_queue_reconciliation_v0" / "r1000_selected_pressure_group_after_repaired_burden_queue_authority_packet.json"

REPAIRED_QUEUE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_v0_receipts" / f"{SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID}.json"
REPAIRED_QUEUE_RECONCILIATION_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_v0" / "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection.json"
REPAIRED_REMAINING_GROUPS_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_v0" / "r1000_remaining_pressure_groups_after_repaired_burden_group_inspection.json"
REPAIRED_NEXT_CANDIDATE_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_v0" / "r1000_next_selectable_group_candidate_after_repaired_burden_group_inspection.json"
REPAIRED_QUEUE_REPORT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_v0" / "r1000_queue_reconciliation_after_repaired_burden_group_inspection_report.json"

REPAIRED_INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_repaired_burden_queue_selected_group_inspection_after_identity_review_v0_receipts" / f"{SOURCE_REPAIRED_INSPECTION_RECEIPT_ID}.json"
REPAIRED_IDENTITY_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_repaired_burden_queue_candidate_identity_surface_review_v0_receipts" / f"{SOURCE_REPAIRED_IDENTITY_REVIEW_RECEIPT_ID}.json"
IDENTITY_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_burden_queue_next_candidate_identity_preservation_fix_v0_receipts" / f"{SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID}.json"
PRIOR_IDENTITY_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_selected_group_after_burden_identity_surface_review_v0_receipts" / f"{SOURCE_IDENTITY_REVIEW_RECEIPT_ID}.json"
SELECTION_AFTER_BURDEN_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_burden_pressure_reconciliation_v0_receipts" / f"{SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID}.json"
BURDEN_QUEUE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0_receipts" / f"{SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID}.json"
SELECTED_GROUP_INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_selected_pressure_group_inspection_from_reconciled_queue_v0_receipts" / f"{SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID}.json"
OLD_SELECTION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_from_reconciled_queue_v0_receipts" / f"{SOURCE_SELECTION_RECEIPT_ID}.json"
QUEUE_RECONCILIATION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0_receipts" / f"{SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID}.json"

SOURCE_FILES = [
    IDENTITY_REVIEW_RECEIPT_PATH,
    IDENTITY_SURFACE_PATH,
    IDENTITY_DECISION_PATH,
    IDENTITY_DEFECT_PACKET_PATH,
    SOURCE_AUDIT_RECOMMENDATION_PACKET_PATH,
    SELECTION_RECEIPT_PATH,
    SELECTED_GROUP_PATH,
    SELECTION_AUTHORITY_PACKET_PATH,
    REPAIRED_QUEUE_RECEIPT_PATH,
    REPAIRED_QUEUE_RECONCILIATION_PATH,
    REPAIRED_REMAINING_GROUPS_PATH,
    REPAIRED_NEXT_CANDIDATE_PATH,
    REPAIRED_QUEUE_REPORT_PATH,
    REPAIRED_INSPECTION_RECEIPT_PATH,
    REPAIRED_IDENTITY_REVIEW_RECEIPT_PATH,
    IDENTITY_FIX_RECEIPT_PATH,
    PRIOR_IDENTITY_REVIEW_RECEIPT_PATH,
    SELECTION_AFTER_BURDEN_RECEIPT_PATH,
    BURDEN_QUEUE_RECEIPT_PATH,
    SELECTED_GROUP_INSPECTION_RECEIPT_PATH,
    OLD_SELECTION_RECEIPT_PATH,
    QUEUE_RECONCILIATION_RECEIPT_PATH,
]

RECOMMENDED_NEXT_HANDLING = "MARK_R1000_SYNTHETIC_REMAINDER_AS_EXPECTED_QUEUE_RESOLUTION_LIMIT_V0"

HUMAN_DECISION = {
    "decision": "AUDIT_R1000_SYNTHETIC_REMAINDER_SOURCE_EVIDENCE_AFTER_REPAIRED_BURDEN_QUEUE_RECONCILIATION",
    "scope": "audit fixed, explicit source and reconciliation surfaces for source-backed identity evidence for the final synthetic remainder; if no direct source evidence exists, emit expected queue-resolution limit candidate and stop before closure application",
    "source_synthetic_remainder_identity_review_receipt_id": SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID,
    "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
    "authorized": [
        "consume synthetic remainder identity review receipt",
        "consume source-audit recommendation packet",
        "consume selected group artifact",
        "consume repaired queue reconciliation artifacts",
        "inspect explicit metadata fields in fixed source artifacts",
        "classify whether direct source-backed identity evidence exists",
        "emit expected queue-resolution limit candidate if evidence is absent",
        "emit queue closure candidate packet",
        "stop before applying closure",
    ],
    "not_authorized": [
        "inspecting selected group row payloads",
        "running R1000",
        "queue reconciliation",
        "opening another group",
        "assigning identity values",
        "inventing values",
        "filling fields",
        "assigning descriptor values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "emitting taxonomy delta proposal",
        "applying expected-limit closure",
        "repairing source artifacts",
        "mutating source artifacts",
        "mutating existing receipts",
        "hidden next command",
    ],
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
    return path.relative_to(ROOT).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def tracked(path: Path) -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", rel(path)],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def load_sources() -> Dict[str, Any]:
    return {
        "identity_review_receipt": read_json(IDENTITY_REVIEW_RECEIPT_PATH),
        "identity_surface": read_json(IDENTITY_SURFACE_PATH),
        "identity_decision": read_json(IDENTITY_DECISION_PATH),
        "identity_defect_packet": read_json(IDENTITY_DEFECT_PACKET_PATH),
        "source_audit_recommendation_packet": read_json(SOURCE_AUDIT_RECOMMENDATION_PACKET_PATH),
        "selection_receipt": read_json(SELECTION_RECEIPT_PATH),
        "selected_group": read_json(SELECTED_GROUP_PATH),
        "selection_authority_packet": read_json(SELECTION_AUTHORITY_PACKET_PATH),
        "repaired_queue_receipt": read_json(REPAIRED_QUEUE_RECEIPT_PATH),
        "repaired_queue_reconciliation": read_json(REPAIRED_QUEUE_RECONCILIATION_PATH),
        "repaired_remaining_groups": read_json(REPAIRED_REMAINING_GROUPS_PATH),
        "repaired_next_candidate": read_json(REPAIRED_NEXT_CANDIDATE_PATH),
        "repaired_queue_report": read_json(REPAIRED_QUEUE_REPORT_PATH),
        "repaired_inspection_receipt": read_json(REPAIRED_INSPECTION_RECEIPT_PATH),
        "repaired_identity_review_receipt": read_json(REPAIRED_IDENTITY_REVIEW_RECEIPT_PATH),
        "identity_fix_receipt": read_json(IDENTITY_FIX_RECEIPT_PATH),
        "prior_identity_review_receipt": read_json(PRIOR_IDENTITY_REVIEW_RECEIPT_PATH),
        "selection_after_burden_receipt": read_json(SELECTION_AFTER_BURDEN_RECEIPT_PATH),
        "burden_queue_receipt": read_json(BURDEN_QUEUE_RECEIPT_PATH),
        "selected_group_inspection_receipt": read_json(SELECTED_GROUP_INSPECTION_RECEIPT_PATH),
        "old_selection_receipt": read_json(OLD_SELECTION_RECEIPT_PATH),
        "queue_reconciliation_receipt": read_json(QUEUE_RECONCILIATION_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    identity_receipt = sources["identity_review_receipt"]
    identity_surface = sources["identity_surface"]
    recommendation = sources["source_audit_recommendation_packet"]
    selected = sources["selected_group"]
    repaired_queue = sources["repaired_queue_receipt"]

    if identity_receipt.get("receipt_id") != SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID:
        failures.append("identity_review_receipt_id_wrong")
    if identity_receipt.get("gate") != "PASS":
        failures.append("identity_review_not_pass")
    if identity_receipt.get("selected_pressure_group_id") != SELECTED_PRESSURE_GROUP_ID:
        failures.append("selected_pressure_group_id_wrong_in_identity_receipt")
    if identity_receipt.get("aggregate_metrics", {}).get("source_audit_recommendation_packet_emitted_count") != 1:
        failures.append("source_audit_recommendation_not_emitted")
    if identity_receipt.get("aggregate_metrics", {}).get("source_audit_executed_count") != 0:
        failures.append("source_audit_already_executed")
    if identity_receipt.get("aggregate_metrics", {}).get("inspection_blocked_count") != 1:
        failures.append("inspection_not_blocked_before_audit")

    if identity_surface.get("candidate_identity_status") != "COUNT_ONLY_SYNTHETIC_REMAINDER":
        failures.append("identity_surface_not_synthetic_remainder")
    if identity_surface.get("inspection_blocked") is not True:
        failures.append("identity_surface_did_not_block_inspection")

    if recommendation.get("packet_status") != "CANDIDATE_ONLY_NOT_EXECUTED":
        failures.append("source_audit_recommendation_already_executed")
    if recommendation.get("selected_pressure_group_id") != SELECTED_PRESSURE_GROUP_ID:
        failures.append("source_audit_recommendation_selected_id_wrong")

    if selected.get("selected_pressure_group_id") != SELECTED_PRESSURE_GROUP_ID:
        failures.append("selected_group_id_wrong")
    if selected.get("candidate_identity_status") != "COUNT_ONLY_SYNTHETIC_REMAINDER":
        failures.append("selected_group_not_synthetic_remainder")

    if repaired_queue.get("receipt_id") != SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID:
        failures.append("repaired_queue_receipt_id_wrong")
    if repaired_queue.get("gate") != "PASS":
        failures.append("repaired_queue_not_pass")
    if repaired_queue.get("aggregate_metrics", {}).get("remaining_row_count_after") != 1:
        failures.append("remaining_row_count_not_one")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def selected_summary(sources: Dict[str, Any]) -> Dict[str, Any]:
    group = sources["selected_group"].get("selected_group", {})
    return {
        "parent_pressure_class": group.get("parent_pressure_class", "UNKNOWN"),
        "pressure_subtype": group.get("pressure_subtype", "UNKNOWN"),
        "halt_reason": group.get("halt_reason", "UNKNOWN"),
        "row_count": int(group.get("row_count", 0) or 0),
    }

def classify_evidence_candidates(sources: Dict[str, Any]) -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []

    selected = sources["selected_group"]
    next_candidate = sources["repaired_next_candidate"]
    remaining = sources["repaired_remaining_groups"]
    queue_report = sources["repaired_queue_report"]
    queue_reconciliation = sources["repaired_queue_reconciliation"]

    candidate_identity_status = selected.get("candidate_identity_status")
    next_candidate_identity_status = next_candidate.get("candidate_identity_status")
    requires_review = selected.get("requires_identity_review_before_inspection")

    candidates.append({
        "source_ref": rel(SELECTED_GROUP_PATH),
        "evidence_kind": "selected_group_candidate_identity_status",
        "observed_value": candidate_identity_status,
        "supports_direct_source_backed_identity": candidate_identity_status not in {"COUNT_ONLY_SYNTHETIC_REMAINDER", "UNKNOWN", None},
        "supports_expected_limit": candidate_identity_status == "COUNT_ONLY_SYNTHETIC_REMAINDER",
    })

    candidates.append({
        "source_ref": rel(REPAIRED_NEXT_CANDIDATE_PATH),
        "evidence_kind": "next_candidate_identity_status",
        "observed_value": next_candidate_identity_status,
        "supports_direct_source_backed_identity": next_candidate_identity_status not in {"COUNT_ONLY_SYNTHETIC_REMAINDER", "UNKNOWN", None},
        "supports_expected_limit": next_candidate_identity_status == "COUNT_ONLY_SYNTHETIC_REMAINDER",
    })

    candidates.append({
        "source_ref": rel(SELECTED_GROUP_PATH),
        "evidence_kind": "requires_identity_review_before_inspection",
        "observed_value": requires_review,
        "supports_direct_source_backed_identity": False,
        "supports_expected_limit": requires_review is True,
    })

    candidates.append({
        "source_ref": rel(REPAIRED_QUEUE_REPORT_PATH),
        "evidence_kind": "remaining_count_reconciliation",
        "observed_value": {
            "remaining_group_count_after": queue_report.get("remaining_group_count_after"),
            "remaining_row_count_after": queue_report.get("remaining_row_count_after"),
            "selected_group_removed_from_prior_remaining_list_count": queue_report.get("selected_group_removed_from_prior_remaining_list_count"),
            "selected_group_removed_row_count": queue_report.get("selected_group_removed_row_count"),
        },
        "supports_direct_source_backed_identity": False,
        "supports_expected_limit": queue_report.get("remaining_row_count_after") == 1 and queue_report.get("selected_group_removed_from_prior_remaining_list_count") == 0,
    })

    remaining_groups = remaining.get("remaining_groups", []) if isinstance(remaining.get("remaining_groups"), list) else []
    for idx, group in enumerate(remaining_groups):
        identity_status = group.get("identity_status")
        candidates.append({
            "source_ref": rel(REPAIRED_REMAINING_GROUPS_PATH),
            "source_index": idx,
            "evidence_kind": "remaining_group_identity_status",
            "observed_value": {
                "identity_status": identity_status,
                "parent_pressure_class": group.get("parent_pressure_class"),
                "pressure_subtype": group.get("pressure_subtype"),
                "halt_reason": group.get("halt_reason"),
                "row_count": group.get("row_count"),
                "requires_identity_review_before_selection": group.get("requires_identity_review_before_selection"),
            },
            "supports_direct_source_backed_identity": identity_status not in {"COUNT_ONLY_SYNTHETIC_REMAINDER", "COUNT_ONLY_SYNTHETIC_REMAINDER", "COUNT_ONLY_SYNTHETIC_REMAINDER", "COUNT_ONLY_SYNTHETIC_REMAINDER", "COUNT_ONLY_SYNTHETIC_REMAINDER", None, "UNKNOWN"} and group.get("requires_identity_review_before_selection") is not True,
            "supports_expected_limit": identity_status == "COUNT_ONLY_SYNTHETIC_REMAINDER" or group.get("requires_identity_review_before_selection") is True,
        })

    candidates.append({
        "source_ref": rel(REPAIRED_QUEUE_RECONCILIATION_PATH),
        "evidence_kind": "queue_reconciliation_next_candidate_source",
        "observed_value": {
            "queue_reconciled": queue_reconciliation.get("queue_reconciled"),
            "next_group_candidate_emitted": queue_reconciliation.get("next_group_candidate_emitted"),
            "next_group_opened": queue_reconciliation.get("next_group_opened"),
            "next_group_inspected": queue_reconciliation.get("next_group_inspected"),
            "remaining_open_row_count": queue_reconciliation.get("remaining_open_row_count"),
        },
        "supports_direct_source_backed_identity": False,
        "supports_expected_limit": queue_reconciliation.get("queue_reconciled") is True and queue_reconciliation.get("remaining_open_row_count") == 1,
    })

    return candidates

def direct_source_evidence_found(candidates: List[Dict[str, Any]]) -> bool:
    return any(candidate.get("supports_direct_source_backed_identity") is True for candidate in candidates)

def expected_limit_supported(candidates: List[Dict[str, Any]]) -> bool:
    return any(candidate.get("supports_expected_limit") is True for candidate in candidates)

def build_audit_surface(sources: Dict[str, Any], candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    selected = selected_summary(sources)
    found_direct = direct_source_evidence_found(candidates)
    supports_limit = expected_limit_supported(candidates)
    return {
        "schema_version": "r1000_synthetic_remainder_source_evidence_audit_surface_after_repaired_burden_queue_v0",
        "audit_surface_id": sha8({
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "source_identity_review_receipt_id": SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID,
            "selected": selected,
        }),
        "source_synthetic_remainder_identity_review_receipt_id": SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID,
        "source_selection_after_repaired_burden_queue_receipt_id": SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID,
        "source_repaired_burden_queue_reconciliation_receipt_id": SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_group": selected,
        "audit_scope": "fixed_explicit_source_and_reconciliation_surfaces_only",
        "audit_status": "SOURCE_EVIDENCE_AUDIT_SURFACE_MATERIALIZED",
        "candidate_identity_status": sources["selected_group"].get("candidate_identity_status"),
        "identity_source_strength_before_audit": sources["identity_surface"].get("identity_source_strength"),
        "evidence_candidate_count": len(candidates),
        "direct_source_backed_identity_evidence_found": found_direct,
        "expected_queue_resolution_limit_supported": supports_limit,
        "inspection_allowed": False,
        "identity_assignment_executed": False,
        "field_value_invention": False,
        "source_mutation": False,
        "existing_receipt_mutation": False,
    }

def build_candidates_artifact(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_synthetic_remainder_source_evidence_candidates_after_repaired_burden_queue_v0",
        "source_synthetic_remainder_identity_review_receipt_id": SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "candidate_count": len(candidates),
        "direct_source_backed_identity_candidate_count": sum(1 for c in candidates if c.get("supports_direct_source_backed_identity") is True),
        "expected_limit_support_candidate_count": sum(1 for c in candidates if c.get("supports_expected_limit") is True),
        "candidates": candidates,
    }

def build_decision(surface: Dict[str, Any]) -> Dict[str, Any]:
    found_direct = surface["direct_source_backed_identity_evidence_found"]
    decision_status = "SOURCE_BACKED_IDENTITY_EVIDENCE_FOUND_REVIEW_REQUIRED" if found_direct else "NO_SOURCE_BACKED_IDENTITY_EVIDENCE_FOUND_EXPECTED_QUEUE_RESOLUTION_LIMIT_CANDIDATE"
    return {
        "schema_version": "r1000_synthetic_remainder_source_evidence_audit_decision_after_repaired_burden_queue_v0",
        "audit_decision_id": sha8({
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "found_direct": found_direct,
            "supports_limit": surface["expected_queue_resolution_limit_supported"],
        }),
        "source_audit_surface_ref": rel(AUDIT_SURFACE_PATH),
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_group": surface["selected_group"],
        "decision_status": decision_status,
        "direct_source_backed_identity_evidence_found": found_direct,
        "expected_queue_resolution_limit_candidate": found_direct is False and surface["expected_queue_resolution_limit_supported"] is True,
        "inspection_allowed": False,
        "identity_assignment_authorized": False,
        "expected_limit_closure_applied_in_this_unit": False,
        "repair_authorized_in_this_unit": False,
        "recommended_next_handling": RECOMMENDED_NEXT_HANDLING if not found_direct else "REVIEW_RECOVERED_R1000_SYNTHETIC_REMAINDER_SOURCE_EVIDENCE_V0",
    }

def build_expected_limit_packet(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_synthetic_remainder_expected_queue_resolution_limit_packet_after_repaired_burden_queue_v0",
        "packet_status": "EXPECTED_LIMIT_CANDIDATE_NOT_APPLIED",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_group": surface["selected_group"],
        "limit_type": "EXPECTED_QUEUE_RESOLUTION_LIMIT",
        "limit_reason": "final 1-row group is count-only synthetic remainder with no direct source-backed pressure identity in audited source surfaces",
        "audit_scope": surface["audit_scope"],
        "direct_source_backed_identity_evidence_found": surface["direct_source_backed_identity_evidence_found"],
        "expected_queue_resolution_limit_supported": surface["expected_queue_resolution_limit_supported"],
        "closure_applied": False,
        "inspection_allowed": False,
        "recommended_next_handling": decision["recommended_next_handling"],
    }

def build_inspection_block_packet(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_synthetic_remainder_source_audit_inspection_block_packet_after_repaired_burden_queue_v0",
        "packet_status": "INSPECTION_STILL_BLOCKED_AFTER_SOURCE_AUDIT",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_group": surface["selected_group"],
        "block_reason": "NO_SOURCE_BACKED_IDENTITY_EVIDENCE_FOUND",
        "inspection_authorized_in_this_unit": False,
        "identity_assignment_authorized": False,
        "row_payload_materialization_authorized": False,
        "r1000_run_authorized": False,
        "recommended_next_handling": decision["recommended_next_handling"],
    }

def build_queue_closure_candidate_packet(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_synthetic_remainder_queue_closure_candidate_packet_after_repaired_burden_queue_v0",
        "packet_status": "QUEUE_CLOSURE_CANDIDATE_NOT_APPLIED",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_group": surface["selected_group"],
        "closure_candidate_type": "MARK_SYNTHETIC_REMAINDER_EXPECTED_QUEUE_RESOLUTION_LIMIT",
        "closure_preconditions": [
            "synthetic remainder identity review blocked inspection",
            "fixed source audit found no direct source-backed pressure identity",
            "remaining count is 1 row / 1 group after repaired burden queue reconciliation",
            "no source artifact mutation required",
        ],
        "closure_application_authorized_in_this_unit": False,
        "queue_reconciliation_authorized_in_this_unit": False,
        "recommended_next_handling": decision["recommended_next_handling"],
    }

def build_transition_trace(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_synthetic_remainder_source_evidence_audit_transition_trace_after_repaired_burden_queue_v0",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "trace": [
            {
                "step": "consume_synthetic_remainder_identity_review",
                "question": "inspection was blocked pending source audit",
                "answer": True,
                "taken": "audit_fixed_source_surfaces",
            },
            {
                "step": "audit_fixed_source_surfaces",
                "question": "direct source-backed identity evidence found",
                "answer": surface["direct_source_backed_identity_evidence_found"],
                "taken": "emit_expected_limit_candidate" if not surface["direct_source_backed_identity_evidence_found"] else "emit_recovered_evidence_review_required",
            },
            {
                "step": "emit_expected_limit_candidate",
                "question": "apply closure in this unit",
                "answer": False,
                "taken": "emit_queue_closure_candidate_packet",
            },
            {
                "step": "emit_queue_closure_candidate_packet",
                "question": "hidden next command allowed",
                "answer": False,
                "taken": "STOP_SYNTHETIC_REMAINDER_SOURCE_AUDIT_COMPLETE_EXPECTED_LIMIT_CANDIDATE_REVIEW_REQUIRED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_SYNTHETIC_REMAINDER_SOURCE_AUDIT_COMPLETE_EXPECTED_LIMIT_CANDIDATE_REVIEW_REQUIRED",
            "next_command_goal": None,
        },
    }

def build_report(surface: Dict[str, Any], candidates_artifact: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    group = surface["selected_group"]
    return {
        "schema_version": "r1000_synthetic_remainder_source_evidence_audit_report_after_repaired_burden_queue_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_synthetic_remainder_identity_review_receipt_id": SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID,
        "source_selection_after_repaired_burden_queue_receipt_id": SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID,
        "source_repaired_burden_queue_reconciliation_receipt_id": SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_parent_pressure_class": group.get("parent_pressure_class"),
        "selected_pressure_subtype": group.get("pressure_subtype"),
        "selected_halt_reason": group.get("halt_reason"),
        "selected_row_count": group.get("row_count"),
        "identity_review_receipt_consumed_count": 1,
        "source_audit_recommendation_packet_consumed_count": 1,
        "selected_group_consumed_count": 1,
        "repaired_queue_reconciliation_consumed_count": 1,
        "source_audit_surface_materialized_count": 1,
        "source_evidence_candidate_count": candidates_artifact["candidate_count"],
        "direct_source_backed_identity_candidate_count": candidates_artifact["direct_source_backed_identity_candidate_count"],
        "expected_limit_support_candidate_count": candidates_artifact["expected_limit_support_candidate_count"],
        "direct_source_backed_identity_evidence_found_count": 1 if surface["direct_source_backed_identity_evidence_found"] else 0,
        "no_direct_source_backed_identity_evidence_found_count": 0 if surface["direct_source_backed_identity_evidence_found"] else 1,
        "expected_queue_resolution_limit_candidate_emitted_count": 1 if decision["expected_queue_resolution_limit_candidate"] else 0,
        "inspection_block_packet_emitted_count": 1,
        "queue_closure_candidate_packet_emitted_count": 1,
        "expected_limit_closure_applied_count": 0,
        "inspection_authorized_in_this_unit_count": 0,
        "identity_assignment_count": 0,
        "field_value_invention_count": 0,
        "selected_group_inspected_count": 0,
        "selected_group_rows_materialized_count": 0,
        "selected_group_rows_inspected_count": 0,
        "queue_reconciled_count": 0,
        "next_group_auto_opened_count": 0,
        "other_group_opened_count": 0,
        "r1000_run_executed_count": 0,
        "repair_executed_count": 0,
        "proposal_applied_count": 0,
        "target_field_filled_count": 0,
        "descriptor_value_assignment_count": 0,
        "null_field_value_emitted_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": decision["recommended_next_handling"],
    }

def validate_outputs(surface: Dict[str, Any], candidates_artifact: Dict[str, Any], decision: Dict[str, Any], expected_limit_packet: Dict[str, Any], inspection_block_packet: Dict[str, Any], queue_closure_packet: Dict[str, Any], trace: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if surface.get("audit_status") != "SOURCE_EVIDENCE_AUDIT_SURFACE_MATERIALIZED":
        failures.append("audit_surface_status_wrong")
    if surface.get("direct_source_backed_identity_evidence_found") is not False:
        failures.append("direct_source_evidence_unexpectedly_found")
    if surface.get("expected_queue_resolution_limit_supported") is not True:
        failures.append("expected_limit_not_supported")
    if candidates_artifact.get("direct_source_backed_identity_candidate_count") != 0:
        failures.append("direct_source_candidate_count_not_zero")
    if decision.get("decision_status") != "NO_SOURCE_BACKED_IDENTITY_EVIDENCE_FOUND_EXPECTED_QUEUE_RESOLUTION_LIMIT_CANDIDATE":
        failures.append("decision_status_wrong")
    if decision.get("expected_limit_closure_applied_in_this_unit") is not False:
        failures.append("expected_limit_closure_applied")
    if expected_limit_packet.get("packet_status") != "EXPECTED_LIMIT_CANDIDATE_NOT_APPLIED":
        failures.append("expected_limit_packet_status_wrong")
    if expected_limit_packet.get("closure_applied") is not False:
        failures.append("expected_limit_packet_applied")
    if inspection_block_packet.get("packet_status") != "INSPECTION_STILL_BLOCKED_AFTER_SOURCE_AUDIT":
        failures.append("inspection_block_packet_status_wrong")
    if queue_closure_packet.get("packet_status") != "QUEUE_CLOSURE_CANDIDATE_NOT_APPLIED":
        failures.append("queue_closure_packet_status_wrong")
    if queue_closure_packet.get("closure_application_authorized_in_this_unit") is not False:
        failures.append("queue_closure_authorized_in_unit")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_next_not_null")

    for key in [
        "expected_limit_closure_applied_count",
        "inspection_authorized_in_this_unit_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "selected_group_inspected_count",
        "selected_group_rows_materialized_count",
        "selected_group_rows_inspected_count",
        "queue_reconciled_count",
        "next_group_auto_opened_count",
        "other_group_opened_count",
        "r1000_run_executed_count",
        "repair_executed_count",
        "proposal_applied_count",
        "target_field_filled_count",
        "descriptor_value_assignment_count",
        "null_field_value_emitted_count",
        "taxonomy_label_creation_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "hidden_next_command_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")

    if report.get("source_audit_surface_materialized_count") != 1:
        failures.append("source_audit_surface_count_wrong")
    if report.get("no_direct_source_backed_identity_evidence_found_count") != 1:
        failures.append("no_direct_evidence_count_wrong")
    if report.get("expected_queue_resolution_limit_candidate_emitted_count") != 1:
        failures.append("expected_limit_candidate_count_wrong")

    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")

    for gate, ok in receipt.get("acceptance_gate_results", {}).items():
        if ok is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{ok}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("source_audit_surface_materialized_count") != 1:
        failures.append("metric_source_audit_surface_wrong")
    if metrics.get("direct_source_backed_identity_evidence_found_count") != 0:
        failures.append("metric_direct_source_evidence_found_not_zero")
    if metrics.get("no_direct_source_backed_identity_evidence_found_count") != 1:
        failures.append("metric_no_direct_source_evidence_wrong")
    if metrics.get("expected_queue_resolution_limit_candidate_emitted_count") != 1:
        failures.append("metric_expected_limit_candidate_wrong")

    for key in [
        "expected_limit_closure_applied_count",
        "inspection_authorized_in_this_unit_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "selected_group_inspected_count",
        "selected_group_rows_materialized_count",
        "selected_group_rows_inspected_count",
        "queue_reconciled_count",
        "next_group_auto_opened_count",
        "other_group_opened_count",
        "r1000_run_executed_count",
        "repair_executed_count",
        "proposal_applied_count",
        "target_field_filled_count",
        "descriptor_value_assignment_count",
        "null_field_value_emitted_count",
        "taxonomy_label_creation_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_SYNTHETIC_REMAINDER_SOURCE_AUDIT_COMPLETE_EXPECTED_LIMIT_CANDIDATE_REVIEW_REQUIRED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def main() -> int:
    source_before = snapshot_files(SOURCE_FILES)
    sources = load_sources()
    failures: List[str] = validate_sources(sources)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    candidates = classify_evidence_candidates(sources)
    surface = build_audit_surface(sources, candidates)
    candidates_artifact = build_candidates_artifact(candidates)
    decision = build_decision(surface)
    expected_limit_packet = build_expected_limit_packet(surface, decision)
    inspection_block_packet = build_inspection_block_packet(surface, decision)
    queue_closure_packet = build_queue_closure_candidate_packet(surface, decision)
    trace = build_transition_trace(surface, decision)
    report = build_report(surface, candidates_artifact, decision)

    write_json(AUDIT_SURFACE_PATH, surface)
    write_json(EVIDENCE_CANDIDATES_PATH, candidates_artifact)
    write_json(AUDIT_DECISION_PATH, decision)
    write_json(EXPECTED_LIMIT_PACKET_PATH, expected_limit_packet)
    write_json(INSPECTION_BLOCK_PACKET_PATH, inspection_block_packet)
    write_json(QUEUE_CLOSURE_CANDIDATE_PACKET_PATH, queue_closure_packet)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(surface, candidates_artifact, decision, expected_limit_packet, inspection_block_packet, queue_closure_packet, trace, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "SYNTHETIC_REMAINDER_SOURCE_AUDIT_0_IDENTITY_REVIEW_CONSUMED": sources["identity_review_receipt"]["receipt_id"] == SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID and sources["identity_review_receipt"]["gate"] == "PASS",
        "SYNTHETIC_REMAINDER_SOURCE_AUDIT_1_RECOMMENDATION_PACKET_CONSUMED": sources["source_audit_recommendation_packet"]["packet_status"] == "CANDIDATE_ONLY_NOT_EXECUTED",
        "SYNTHETIC_REMAINDER_SOURCE_AUDIT_2_FIXED_SOURCE_SURFACES_AUDITED": surface["evidence_candidate_count"] > 0,
        "SYNTHETIC_REMAINDER_SOURCE_AUDIT_3_NO_DIRECT_SOURCE_BACKED_IDENTITY_FOUND": surface["direct_source_backed_identity_evidence_found"] is False,
        "SYNTHETIC_REMAINDER_SOURCE_AUDIT_4_EXPECTED_LIMIT_CANDIDATE_EMITTED": decision["expected_queue_resolution_limit_candidate"] is True and expected_limit_packet["packet_status"] == "EXPECTED_LIMIT_CANDIDATE_NOT_APPLIED",
        "SYNTHETIC_REMAINDER_SOURCE_AUDIT_5_CLOSURE_NOT_APPLIED": report["expected_limit_closure_applied_count"] == 0 and queue_closure_packet["closure_application_authorized_in_this_unit"] is False,
        "SYNTHETIC_REMAINDER_SOURCE_AUDIT_6_NO_IDENTITY_ASSIGNMENT_OR_INVENTION": report["identity_assignment_count"] == 0 and report["field_value_invention_count"] == 0,
        "SYNTHETIC_REMAINDER_SOURCE_AUDIT_7_NO_ROW_PAYLOAD_OR_R1000": report["selected_group_rows_materialized_count"] == 0 and report["r1000_run_executed_count"] == 0,
        "SYNTHETIC_REMAINDER_SOURCE_AUDIT_8_NO_REPAIR_FIELD_VALUE_OR_TAXONOMY": report["repair_executed_count"] == 0 and report["target_field_filled_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "SYNTHETIC_REMAINDER_SOURCE_AUDIT_9_NO_QUEUE_RECONCILIATION_OR_NEXT_OPEN": report["queue_reconciled_count"] == 0 and report["next_group_auto_opened_count"] == 0 and report["other_group_opened_count"] == 0,
        "SYNTHETIC_REMAINDER_SOURCE_AUDIT_10_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "SYNTHETIC_REMAINDER_SOURCE_AUDIT_11_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_synthetic_remainder_identity_review_receipt_id": SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID,
        "source_selection_after_repaired_burden_queue_receipt_id": SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID,
        "source_repaired_burden_queue_reconciliation_receipt_id": SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_repaired_inspection_receipt_id": SOURCE_REPAIRED_INSPECTION_RECEIPT_ID,
        "source_repaired_identity_review_receipt_id": SOURCE_REPAIRED_IDENTITY_REVIEW_RECEIPT_ID,
        "source_identity_preservation_fix_receipt_id": SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID,
        "source_identity_review_receipt_id": SOURCE_IDENTITY_REVIEW_RECEIPT_ID,
        "source_selection_after_burden_receipt_id": SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_selected_group_inspection_receipt_id": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "source_mutation_count": 1 if source_mutation_detected else 0,
    }

    guards = {
        "identity_review_receipt_consumed": True,
        "source_audit_recommendation_packet_consumed": True,
        "fixed_source_surfaces_audited": True,
        "direct_source_backed_identity_evidence_found": False,
        "expected_queue_resolution_limit_candidate_emitted": True,
        "expected_limit_closure_applied": False,
        "inspection_authorized_in_this_unit": False,
        "identity_assignment": False,
        "field_value_invention": False,
        "selected_group_inspected": False,
        "selected_group_rows_materialized": False,
        "selected_group_rows_inspected": False,
        "queue_reconciled": False,
        "next_group_opened": False,
        "r1000_run_executed": False,
        "repair_executed": False,
        "proposal_applied": False,
        "target_field_filled": False,
        "descriptor_value_assigned": False,
        "null_field_value_emitted": False,
        "taxonomy_label_created": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_identity_review_receipt": SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "decision": decision["decision_status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "audit_surface": rel(AUDIT_SURFACE_PATH),
        "evidence_candidates": rel(EVIDENCE_CANDIDATES_PATH),
        "audit_decision": rel(AUDIT_DECISION_PATH),
        "expected_limit_packet": rel(EXPECTED_LIMIT_PACKET_PATH),
        "inspection_block_packet": rel(INSPECTION_BLOCK_PACKET_PATH),
        "queue_closure_candidate_packet": rel(QUEUE_CLOSURE_CANDIDATE_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_synthetic_remainder_source_evidence_audit_after_repaired_burden_queue_receipt_v0",
        "receipt_type": "R1000_SYNTHETIC_REMAINDER_SOURCE_EVIDENCE_AUDIT_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_synthetic_remainder_identity_review_receipt_id": SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID,
        "source_selection_after_repaired_burden_queue_receipt_id": SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID,
        "source_repaired_burden_queue_reconciliation_receipt_id": SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_repaired_inspection_receipt_id": SOURCE_REPAIRED_INSPECTION_RECEIPT_ID,
        "source_repaired_identity_review_receipt_id": SOURCE_REPAIRED_IDENTITY_REVIEW_RECEIPT_ID,
        "source_identity_preservation_fix_receipt_id": SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID,
        "source_identity_review_receipt_id": SOURCE_IDENTITY_REVIEW_RECEIPT_ID,
        "source_selection_after_burden_receipt_id": SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_selected_group_inspection_receipt_id": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "synthetic_remainder_source_evidence_audit_summary": {
            "audit_result": decision["decision_status"],
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "selected_group": surface["selected_group"],
            "audit_scope": surface["audit_scope"],
            "evidence_candidate_count": surface["evidence_candidate_count"],
            "direct_source_backed_identity_evidence_found": False,
            "expected_queue_resolution_limit_candidate": decision["expected_queue_resolution_limit_candidate"],
            "expected_limit_closure_applied": False,
            "inspection_allowed": False,
            "recommended_next_handling": decision["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "synthetic_remainder_source_evidence_audit_guards": guards,
        "terminal": terminal,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_failures = validate_receipt(receipt)
    failures.extend(receipt_failures)
    receipt["failures"] = failures
    receipt["gate"] = "PASS" if not failures else "FAIL"
    if failures:
        receipt["terminal"] = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"synthetic_remainder_source_audit_receipt_id={receipt_id}")
    print(f"synthetic_remainder_source_audit_receipt_path=data/r1000_synthetic_remainder_source_evidence_audit_after_repaired_burden_queue_v0_receipts/{receipt_id}.json")
    print(f"synthetic_remainder_expected_limit_packet_path=data/r1000_synthetic_remainder_source_evidence_audit_after_repaired_burden_queue_v0/r1000_synthetic_remainder_expected_queue_resolution_limit_packet_after_repaired_burden_queue.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
