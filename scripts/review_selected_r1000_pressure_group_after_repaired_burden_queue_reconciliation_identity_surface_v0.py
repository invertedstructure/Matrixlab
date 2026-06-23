#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_SELECTED_R1000_PRESSURE_GROUP_AFTER_REPAIRED_BURDEN_QUEUE_RECONCILIATION_IDENTITY_SURFACE_V0"
TARGET_UNIT_ID = "r1000_selected_synthetic_remainder.identity_surface_review_after_repaired_burden_queue.v0"

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

OUT_DIR = ROOT / "data" / "r1000_selected_synthetic_remainder_identity_surface_review_after_repaired_burden_queue_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_selected_synthetic_remainder_identity_surface_review_after_repaired_burden_queue_v0_receipts"

IDENTITY_SURFACE_PATH = OUT_DIR / "r1000_selected_synthetic_remainder_identity_surface_after_repaired_burden_queue.json"
IDENTITY_REVIEW_DECISION_PATH = OUT_DIR / "r1000_selected_synthetic_remainder_identity_review_decision_after_repaired_burden_queue.json"
IDENTITY_DEFECT_PACKET_PATH = OUT_DIR / "r1000_selected_synthetic_remainder_identity_defect_packet_after_repaired_burden_queue.json"
INSPECTION_BLOCK_PACKET_PATH = OUT_DIR / "r1000_selected_synthetic_remainder_inspection_block_packet_after_repaired_burden_queue.json"
SOURCE_AUDIT_RECOMMENDATION_PACKET_PATH = OUT_DIR / "r1000_selected_synthetic_remainder_source_audit_recommendation_packet_after_repaired_burden_queue.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_selected_synthetic_remainder_identity_review_transition_trace_after_repaired_burden_queue.json"
REPORT_PATH = OUT_DIR / "r1000_selected_synthetic_remainder_identity_review_report_after_repaired_burden_queue.json"

SELECTION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_repaired_burden_group_queue_reconciliation_v0_receipts" / f"{SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID}.json"
SELECTED_GROUP_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_repaired_burden_group_queue_reconciliation_v0" / "r1000_selected_pressure_group_after_repaired_burden_queue_reconciliation.json"
SELECTION_DECISION_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_repaired_burden_group_queue_reconciliation_v0" / "r1000_pressure_group_selection_after_repaired_burden_queue_decision.json"
AUTHORITY_PACKET_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_repaired_burden_group_queue_reconciliation_v0" / "r1000_selected_pressure_group_after_repaired_burden_queue_authority_packet.json"

REPAIRED_QUEUE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_v0_receipts" / f"{SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID}.json"
REPAIRED_QUEUE_RECONCILIATION_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_v0" / "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection.json"
REPAIRED_REMAINING_GROUPS_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_v0" / "r1000_remaining_pressure_groups_after_repaired_burden_group_inspection.json"
REPAIRED_NEXT_CANDIDATE_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_v0" / "r1000_next_selectable_group_candidate_after_repaired_burden_group_inspection.json"
REPAIRED_QUEUE_REPORT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_v0" / "r1000_queue_reconciliation_after_repaired_burden_group_inspection_report.json"

REPAIRED_INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_repaired_burden_queue_selected_group_inspection_after_identity_review_v0_receipts" / f"{SOURCE_REPAIRED_INSPECTION_RECEIPT_ID}.json"
REPAIRED_IDENTITY_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_repaired_burden_queue_candidate_identity_surface_review_v0_receipts" / f"{SOURCE_REPAIRED_IDENTITY_REVIEW_RECEIPT_ID}.json"
IDENTITY_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_burden_queue_next_candidate_identity_preservation_fix_v0_receipts" / f"{SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID}.json"
IDENTITY_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_selected_group_after_burden_identity_surface_review_v0_receipts" / f"{SOURCE_IDENTITY_REVIEW_RECEIPT_ID}.json"
SELECTION_AFTER_BURDEN_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_burden_pressure_reconciliation_v0_receipts" / f"{SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID}.json"
BURDEN_QUEUE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0_receipts" / f"{SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID}.json"
SELECTED_GROUP_INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_selected_pressure_group_inspection_from_reconciled_queue_v0_receipts" / f"{SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID}.json"
OLD_SELECTION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_from_reconciled_queue_v0_receipts" / f"{SOURCE_SELECTION_RECEIPT_ID}.json"
QUEUE_RECONCILIATION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0_receipts" / f"{SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID}.json"

SOURCE_FILES = [
    SELECTION_RECEIPT_PATH,
    SELECTED_GROUP_PATH,
    SELECTION_DECISION_PATH,
    AUTHORITY_PACKET_PATH,
    REPAIRED_QUEUE_RECEIPT_PATH,
    REPAIRED_QUEUE_RECONCILIATION_PATH,
    REPAIRED_REMAINING_GROUPS_PATH,
    REPAIRED_NEXT_CANDIDATE_PATH,
    REPAIRED_QUEUE_REPORT_PATH,
    REPAIRED_INSPECTION_RECEIPT_PATH,
    REPAIRED_IDENTITY_REVIEW_RECEIPT_PATH,
    IDENTITY_FIX_RECEIPT_PATH,
    IDENTITY_REVIEW_RECEIPT_PATH,
    SELECTION_AFTER_BURDEN_RECEIPT_PATH,
    BURDEN_QUEUE_RECEIPT_PATH,
    SELECTED_GROUP_INSPECTION_RECEIPT_PATH,
    OLD_SELECTION_RECEIPT_PATH,
    QUEUE_RECONCILIATION_RECEIPT_PATH,
]

RECOMMENDED_NEXT_HANDLING = "AUDIT_R1000_SYNTHETIC_REMAINDER_SOURCE_EVIDENCE_AFTER_REPAIRED_BURDEN_QUEUE_RECONCILIATION_V0"

HUMAN_DECISION = {
    "decision": "REVIEW_SELECTED_R1000_PRESSURE_GROUP_AFTER_REPAIRED_BURDEN_QUEUE_RECONCILIATION_IDENTITY_SURFACE",
    "scope": "review the selected final synthetic remainder identity surface; block inspection when identity is count-only synthetic and emit source-audit recommendation without inspecting, assigning identity, repairing, or mutating prior artifacts",
    "source_selection_after_repaired_burden_queue_receipt_id": SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID,
    "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
    "authorized": [
        "consume selection receipt",
        "consume selected pressure group artifact",
        "consume selection authority packet",
        "materialize identity surface",
        "classify identity source strength",
        "block inspection if identity is count-only synthetic",
        "emit identity defect packet",
        "emit source-audit recommendation packet",
        "stop before inspection",
    ],
    "not_authorized": [
        "inspecting selected group",
        "materializing row payloads",
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
        "selection_receipt": read_json(SELECTION_RECEIPT_PATH),
        "selected_group": read_json(SELECTED_GROUP_PATH),
        "selection_decision": read_json(SELECTION_DECISION_PATH),
        "authority_packet": read_json(AUTHORITY_PACKET_PATH),
        "repaired_queue_receipt": read_json(REPAIRED_QUEUE_RECEIPT_PATH),
        "repaired_queue_reconciliation": read_json(REPAIRED_QUEUE_RECONCILIATION_PATH),
        "repaired_remaining_groups": read_json(REPAIRED_REMAINING_GROUPS_PATH),
        "repaired_next_candidate": read_json(REPAIRED_NEXT_CANDIDATE_PATH),
        "repaired_queue_report": read_json(REPAIRED_QUEUE_REPORT_PATH),
        "repaired_inspection_receipt": read_json(REPAIRED_INSPECTION_RECEIPT_PATH),
        "repaired_identity_review_receipt": read_json(REPAIRED_IDENTITY_REVIEW_RECEIPT_PATH),
        "identity_fix_receipt": read_json(IDENTITY_FIX_RECEIPT_PATH),
        "identity_review_receipt": read_json(IDENTITY_REVIEW_RECEIPT_PATH),
        "selection_after_burden_receipt": read_json(SELECTION_AFTER_BURDEN_RECEIPT_PATH),
        "burden_queue_receipt": read_json(BURDEN_QUEUE_RECEIPT_PATH),
        "selected_group_inspection_receipt": read_json(SELECTED_GROUP_INSPECTION_RECEIPT_PATH),
        "old_selection_receipt": read_json(OLD_SELECTION_RECEIPT_PATH),
        "queue_reconciliation_receipt": read_json(QUEUE_RECONCILIATION_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    selection = sources["selection_receipt"]
    selected = sources["selected_group"]
    authority = sources["authority_packet"]

    if selection.get("receipt_id") != SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID:
        failures.append("selection_receipt_id_wrong")
    if selection.get("gate") != "PASS":
        failures.append("selection_not_pass")
    if selection.get("selected_pressure_group_id") != SELECTED_PRESSURE_GROUP_ID:
        failures.append("selected_pressure_group_id_wrong_in_receipt")
    if selection.get("aggregate_metrics", {}).get("pressure_group_selected_count") != 1:
        failures.append("selection_not_recorded")
    if selection.get("aggregate_metrics", {}).get("identity_review_executed_count") != 0:
        failures.append("identity_review_already_executed")
    if selection.get("aggregate_metrics", {}).get("selected_group_inspected_count") != 0:
        failures.append("selected_group_already_inspected")
    if selection.get("aggregate_metrics", {}).get("candidate_identity_status") != "COUNT_ONLY_SYNTHETIC_REMAINDER":
        failures.append("candidate_identity_status_not_synthetic_remainder")
    if selection.get("aggregate_metrics", {}).get("requires_identity_review_before_inspection") is not True:
        failures.append("identity_review_requirement_missing")

    if selected.get("selected_pressure_group_id") != SELECTED_PRESSURE_GROUP_ID:
        failures.append("selected_group_id_wrong")
    if selected.get("selection_status") != "SELECTED_NOT_INSPECTED":
        failures.append("selected_status_wrong")
    if selected.get("candidate_identity_status") != "COUNT_ONLY_SYNTHETIC_REMAINDER":
        failures.append("selected_candidate_identity_status_wrong")
    if selected.get("requires_identity_review_before_inspection") is not True:
        failures.append("selected_does_not_require_identity_review")
    if selected.get("selected_group_rows_inspected") is not False:
        failures.append("selected_rows_already_inspected")

    if authority.get("packet_status") != "SEPARATE_IDENTITY_REVIEW_REQUIRED":
        failures.append("authority_packet_status_wrong")
    if authority.get("selected_pressure_group_id") != SELECTED_PRESSURE_GROUP_ID:
        failures.append("authority_selected_id_wrong")

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

def build_identity_surface(sources: Dict[str, Any]) -> Dict[str, Any]:
    selected = selected_summary(sources)
    candidate_identity_status = sources["selected_group"].get("candidate_identity_status", "UNKNOWN")
    identity_source_strength = "COUNT_ONLY_SYNTHETIC_NOT_SOURCE_TYPED" if candidate_identity_status == "COUNT_ONLY_SYNTHETIC_REMAINDER" else "SOURCE_TYPED_OR_UNKNOWN"
    identity_complete_for_inspection = candidate_identity_status != "COUNT_ONLY_SYNTHETIC_REMAINDER"

    defects = []
    if candidate_identity_status == "COUNT_ONLY_SYNTHETIC_REMAINDER":
        defects.append({
            "field": "candidate_identity_status",
            "observed_value": candidate_identity_status,
            "defect_type": "COUNT_ONLY_SYNTHETIC_REMAINDER_NOT_INSPECTABLE_IDENTITY",
            "severity": "BLOCKS_INSPECTION",
            "reason": "selected group identity was derived from residual queue counts, not from a directly source-backed pressure group row",
        })
    if selected.get("row_count") != 1:
        defects.append({
            "field": "row_count",
            "observed_value": selected.get("row_count"),
            "defect_type": "UNEXPECTED_SYNTHETIC_REMAINDER_ROW_COUNT",
            "severity": "BLOCKS_INSPECTION",
        })

    return {
        "schema_version": "r1000_selected_synthetic_remainder_identity_surface_after_repaired_burden_queue_v0",
        "identity_surface_id": sha8({
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "selected_group": selected,
            "candidate_identity_status": candidate_identity_status,
        }),
        "source_selection_after_repaired_burden_queue_receipt_id": SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID,
        "source_selected_group_ref": rel(SELECTED_GROUP_PATH),
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "surface_status": "SELECTED_SYNTHETIC_REMAINDER_IDENTITY_SURFACE_MATERIALIZED_FOR_REVIEW",
        "selected_group": selected,
        "candidate_identity_status": candidate_identity_status,
        "identity_source_strength": identity_source_strength,
        "identity_complete_for_inspection": identity_complete_for_inspection,
        "identity_defects": defects,
        "identity_defect_count": len(defects),
        "synthetic_remainder_detected": candidate_identity_status == "COUNT_ONLY_SYNTHETIC_REMAINDER",
        "inspection_allowed": False,
        "inspection_blocked": True,
        "source_audit_required": True,
        "identity_assignment_executed": False,
        "field_value_invention": False,
        "row_payload_materialized": False,
        "row_payload_inspected": False,
        "r1000_run_executed": False,
    }

def build_decision(surface: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_synthetic_remainder_identity_review_decision_after_repaired_burden_queue_v0",
        "identity_review_decision_id": sha8({
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "identity_source_strength": surface["identity_source_strength"],
            "identity_defect_count": surface["identity_defect_count"],
        }),
        "source_identity_surface_ref": rel(IDENTITY_SURFACE_PATH),
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_group": surface["selected_group"],
        "decision_status": "BLOCK_INSPECTION_SYNTHETIC_REMAINDER_REQUIRES_SOURCE_EVIDENCE_AUDIT",
        "identity_complete_for_inspection": False,
        "inspection_blocked": True,
        "inspection_authorized_in_this_unit": False,
        "source_audit_required": True,
        "source_audit_authorized_in_this_unit": False,
        "identity_assignment_authorized": False,
        "repair_authorized_in_this_unit": False,
        "recommended_next_handling": RECOMMENDED_NEXT_HANDLING,
    }

def build_defect_packet(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_synthetic_remainder_identity_defect_packet_after_repaired_burden_queue_v0",
        "packet_status": "IDENTITY_DEFECT_RECORDED_INSPECTION_BLOCKED",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_group": surface["selected_group"],
        "candidate_identity_status": surface["candidate_identity_status"],
        "identity_source_strength": surface["identity_source_strength"],
        "identity_defects": surface["identity_defects"],
        "inspection_blocked": True,
        "defect_summary": "The selected final pressure group is a count-only synthetic remainder. Its labels are routing placeholders, not directly source-backed inspectable identity.",
        "recommended_next_handling": decision["recommended_next_handling"],
    }

def build_inspection_block_packet(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_synthetic_remainder_inspection_block_packet_after_repaired_burden_queue_v0",
        "packet_status": "INSPECTION_BLOCKED",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_group": surface["selected_group"],
        "block_reason": "COUNT_ONLY_SYNTHETIC_REMAINDER_NOT_INSPECTABLE_IDENTITY",
        "inspection_authorized_in_this_unit": False,
        "row_payload_materialization_authorized": False,
        "r1000_run_authorized": False,
        "repair_authorized": False,
        "source_audit_required": True,
        "recommended_next_handling": decision["recommended_next_handling"],
    }

def build_source_audit_recommendation_packet(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_synthetic_remainder_source_audit_recommendation_packet_after_repaired_burden_queue_v0",
        "packet_status": "CANDIDATE_ONLY_NOT_EXECUTED",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_group": surface["selected_group"],
        "audit_target": "find explicit source evidence for the final 1-row synthetic remainder or mark it as expected source-content/queue-resolution limit",
        "source_refs_for_audit": [
            rel(REPAIRED_REMAINING_GROUPS_PATH),
            rel(REPAIRED_NEXT_CANDIDATE_PATH),
            rel(REPAIRED_QUEUE_RECONCILIATION_PATH),
            rel(REPAIRED_QUEUE_REPORT_PATH),
            rel(SELECTION_RECEIPT_PATH),
        ],
        "allowed_next_unit": decision["recommended_next_handling"],
        "allowed_next_unit_scope": [
            "consume selected synthetic remainder identity review receipt",
            "audit source/reconciliation surfaces for explicit source-backed identity",
            "if recoverable, emit repaired identity candidate only",
            "if not recoverable, emit expected-limit packet",
            "stop before inspection",
        ],
        "not_authorized_in_this_unit": [
            "source audit execution",
            "identity assignment",
            "inspection",
            "row payload materialization",
            "R1000 execution",
            "queue reconciliation",
            "repair application",
            "taxonomy action",
            "source mutation",
            "receipt mutation",
            "hidden next command",
        ],
    }

def build_transition_trace(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_synthetic_remainder_identity_review_transition_trace_after_repaired_burden_queue_v0",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "trace": [
            {
                "step": "consume_selection_after_repaired_burden_queue",
                "question": "selected group exists and is not inspected",
                "answer": True,
                "taken": "materialize_identity_surface",
            },
            {
                "step": "materialize_identity_surface",
                "question": "identity is source-backed enough for inspection",
                "answer": surface["identity_complete_for_inspection"],
                "taken": "block_inspection_for_source_audit",
            },
            {
                "step": "block_inspection_for_source_audit",
                "question": "assign identity in this unit",
                "answer": False,
                "taken": "emit_source_audit_recommendation",
            },
            {
                "step": "emit_source_audit_recommendation",
                "question": "hidden next command allowed",
                "answer": False,
                "taken": "STOP_SELECTED_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_COMPLETE_SOURCE_AUDIT_REQUIRED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_SELECTED_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_COMPLETE_SOURCE_AUDIT_REQUIRED",
            "next_command_goal": None,
        },
    }

def build_report(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    group = surface["selected_group"]
    return {
        "schema_version": "r1000_selected_synthetic_remainder_identity_review_report_after_repaired_burden_queue_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_selection_after_repaired_burden_queue_receipt_id": SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID,
        "source_repaired_burden_queue_reconciliation_receipt_id": SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_parent_pressure_class": group.get("parent_pressure_class"),
        "selected_pressure_subtype": group.get("pressure_subtype"),
        "selected_halt_reason": group.get("halt_reason"),
        "selected_row_count": group.get("row_count"),
        "candidate_identity_status": surface["candidate_identity_status"],
        "identity_source_strength": surface["identity_source_strength"],
        "selection_receipt_consumed_count": 1,
        "selected_group_consumed_count": 1,
        "authority_packet_consumed_count": 1,
        "identity_surface_materialized_count": 1,
        "identity_review_completed_count": 1,
        "synthetic_remainder_detected_count": 1 if surface["synthetic_remainder_detected"] else 0,
        "identity_defect_count": surface["identity_defect_count"],
        "inspection_blocked_count": 1,
        "identity_defect_packet_emitted_count": 1,
        "inspection_block_packet_emitted_count": 1,
        "source_audit_recommendation_packet_emitted_count": 1,
        "source_audit_executed_count": 0,
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

def validate_outputs(surface: Dict[str, Any], decision: Dict[str, Any], defect_packet: Dict[str, Any], block_packet: Dict[str, Any], recommendation_packet: Dict[str, Any], trace: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if surface.get("surface_status") != "SELECTED_SYNTHETIC_REMAINDER_IDENTITY_SURFACE_MATERIALIZED_FOR_REVIEW":
        failures.append("surface_status_wrong")
    if surface.get("synthetic_remainder_detected") is not True:
        failures.append("synthetic_remainder_not_detected")
    if surface.get("identity_complete_for_inspection") is not False:
        failures.append("synthetic_remainder_marked_inspectable")
    if surface.get("inspection_blocked") is not True:
        failures.append("inspection_not_blocked")
    if decision.get("decision_status") != "BLOCK_INSPECTION_SYNTHETIC_REMAINDER_REQUIRES_SOURCE_EVIDENCE_AUDIT":
        failures.append("decision_status_wrong")
    if decision.get("inspection_authorized_in_this_unit") is not False:
        failures.append("inspection_authorized_in_review_unit")
    if decision.get("identity_assignment_authorized") is not False:
        failures.append("identity_assignment_authorized")
    if defect_packet.get("packet_status") != "IDENTITY_DEFECT_RECORDED_INSPECTION_BLOCKED":
        failures.append("defect_packet_status_wrong")
    if block_packet.get("packet_status") != "INSPECTION_BLOCKED":
        failures.append("block_packet_status_wrong")
    if recommendation_packet.get("packet_status") != "CANDIDATE_ONLY_NOT_EXECUTED":
        failures.append("recommendation_packet_not_candidate_only")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_next_not_null")

    for key in [
        "source_audit_executed_count",
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

    if report.get("identity_review_completed_count") != 1:
        failures.append("identity_review_completed_count_wrong")
    if report.get("synthetic_remainder_detected_count") != 1:
        failures.append("synthetic_remainder_count_wrong")
    if report.get("inspection_blocked_count") != 1:
        failures.append("inspection_blocked_count_wrong")
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
    if metrics.get("identity_review_completed_count") != 1:
        failures.append("metric_identity_review_completed_wrong")
    if metrics.get("synthetic_remainder_detected_count") != 1:
        failures.append("metric_synthetic_remainder_wrong")
    if metrics.get("inspection_blocked_count") != 1:
        failures.append("metric_inspection_blocked_wrong")

    for key in [
        "source_audit_executed_count",
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
    if terminal.get("stop_code") != "STOP_SELECTED_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_COMPLETE_SOURCE_AUDIT_REQUIRED":
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

    surface = build_identity_surface(sources)
    decision = build_decision(surface)
    defect_packet = build_defect_packet(surface, decision)
    block_packet = build_inspection_block_packet(surface, decision)
    recommendation_packet = build_source_audit_recommendation_packet(surface, decision)
    trace = build_transition_trace(surface, decision)
    report = build_report(surface, decision)

    write_json(IDENTITY_SURFACE_PATH, surface)
    write_json(IDENTITY_REVIEW_DECISION_PATH, decision)
    write_json(IDENTITY_DEFECT_PACKET_PATH, defect_packet)
    write_json(INSPECTION_BLOCK_PACKET_PATH, block_packet)
    write_json(SOURCE_AUDIT_RECOMMENDATION_PACKET_PATH, recommendation_packet)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(surface, decision, defect_packet, block_packet, recommendation_packet, trace, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "SYNTHETIC_REMAINDER_IDENTITY_REVIEW_0_SELECTION_RECEIPT_CONSUMED": sources["selection_receipt"]["receipt_id"] == SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID and sources["selection_receipt"]["gate"] == "PASS",
        "SYNTHETIC_REMAINDER_IDENTITY_REVIEW_1_SELECTED_GROUP_CONSUMED": sources["selected_group"]["selected_pressure_group_id"] == SELECTED_PRESSURE_GROUP_ID,
        "SYNTHETIC_REMAINDER_IDENTITY_REVIEW_2_SYNTHETIC_REMAINDER_DETECTED": surface["synthetic_remainder_detected"] is True,
        "SYNTHETIC_REMAINDER_IDENTITY_REVIEW_3_INSPECTION_BLOCKED": surface["inspection_blocked"] is True and decision["inspection_authorized_in_this_unit"] is False,
        "SYNTHETIC_REMAINDER_IDENTITY_REVIEW_4_SOURCE_AUDIT_RECOMMENDED_ONLY": recommendation_packet["packet_status"] == "CANDIDATE_ONLY_NOT_EXECUTED" and report["source_audit_executed_count"] == 0,
        "SYNTHETIC_REMAINDER_IDENTITY_REVIEW_5_NO_IDENTITY_ASSIGNMENT_OR_INVENTION": report["identity_assignment_count"] == 0 and report["field_value_invention_count"] == 0,
        "SYNTHETIC_REMAINDER_IDENTITY_REVIEW_6_NO_ROW_PAYLOAD_OR_R1000": report["selected_group_rows_materialized_count"] == 0 and report["r1000_run_executed_count"] == 0,
        "SYNTHETIC_REMAINDER_IDENTITY_REVIEW_7_NO_REPAIR_FIELD_VALUE_OR_TAXONOMY": report["repair_executed_count"] == 0 and report["target_field_filled_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "SYNTHETIC_REMAINDER_IDENTITY_REVIEW_8_NO_QUEUE_RECONCILIATION_OR_NEXT_OPEN": report["queue_reconciled_count"] == 0 and report["next_group_auto_opened_count"] == 0 and report["other_group_opened_count"] == 0,
        "SYNTHETIC_REMAINDER_IDENTITY_REVIEW_9_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "SYNTHETIC_REMAINDER_IDENTITY_REVIEW_10_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
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
        "selection_receipt_consumed": True,
        "selected_group_consumed": True,
        "identity_surface_materialized": True,
        "synthetic_remainder_detected": True,
        "inspection_blocked": True,
        "source_audit_recommended_only": True,
        "source_audit_executed": False,
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
        "source_selection_receipt": SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "decision": decision["decision_status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "identity_surface": rel(IDENTITY_SURFACE_PATH),
        "identity_review_decision": rel(IDENTITY_REVIEW_DECISION_PATH),
        "identity_defect_packet": rel(IDENTITY_DEFECT_PACKET_PATH),
        "inspection_block_packet": rel(INSPECTION_BLOCK_PACKET_PATH),
        "source_audit_recommendation_packet": rel(SOURCE_AUDIT_RECOMMENDATION_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_selected_synthetic_remainder_identity_surface_review_after_repaired_burden_queue_receipt_v0",
        "receipt_type": "R1000_SELECTED_SYNTHETIC_REMAINDER_IDENTITY_SURFACE_REVIEW_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
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
        "synthetic_remainder_identity_review_summary": {
            "review_result": "BLOCK_INSPECTION_SYNTHETIC_REMAINDER_REQUIRES_SOURCE_EVIDENCE_AUDIT",
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "selected_group": surface["selected_group"],
            "candidate_identity_status": surface["candidate_identity_status"],
            "identity_source_strength": surface["identity_source_strength"],
            "identity_complete_for_inspection": False,
            "synthetic_remainder_detected": True,
            "inspection_blocked": True,
            "source_audit_required": True,
            "recommended_next_handling": RECOMMENDED_NEXT_HANDLING,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "synthetic_remainder_identity_review_guards": guards,
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
    print(f"synthetic_remainder_identity_review_receipt_id={receipt_id}")
    print(f"synthetic_remainder_identity_review_receipt_path=data/r1000_selected_synthetic_remainder_identity_surface_review_after_repaired_burden_queue_v0_receipts/{receipt_id}.json")
    print(f"synthetic_remainder_identity_review_decision_path=data/r1000_selected_synthetic_remainder_identity_surface_review_after_repaired_burden_queue_v0/r1000_selected_synthetic_remainder_identity_review_decision_after_repaired_burden_queue.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
