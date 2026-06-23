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

UNIT_ID = "REVIEW_REPAIRED_R1000_BURDEN_QUEUE_NEXT_CANDIDATE_IDENTITY_SURFACE_V0"
TARGET_UNIT_ID = "r1000_repaired_burden_queue_candidate.identity_surface_review.v0"

SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID = "7cfe198f"
SOURCE_IDENTITY_REVIEW_RECEIPT_ID = "82c10dfc"
SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID = "1cb51143"
SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID = "d3135cdb"
SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID = "dea88520"
SOURCE_SELECTION_RECEIPT_ID = "7c561212"
SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID = "38604be8"
REPAIRED_CANDIDATE_ID = "a0dcb75d"
REPAIRED_SELECTED_PRESSURE_GROUP_ID = "113fd48b"

OUT_DIR = ROOT / "data" / "r1000_repaired_burden_queue_candidate_identity_surface_review_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_repaired_burden_queue_candidate_identity_surface_review_v0_receipts"

REPAIRED_IDENTITY_SURFACE_PATH = OUT_DIR / "r1000_repaired_burden_queue_candidate_identity_surface.json"
REPAIRED_IDENTITY_REVIEW_DECISION_PATH = OUT_DIR / "r1000_repaired_burden_queue_candidate_identity_review_decision.json"
REPAIRED_IDENTITY_ACCEPTANCE_PACKET_PATH = OUT_DIR / "r1000_repaired_burden_queue_candidate_identity_acceptance_packet.json"
REPAIRED_INSPECTION_AUTHORITY_PACKET_PATH = OUT_DIR / "r1000_repaired_burden_queue_candidate_inspection_authority_packet.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_repaired_burden_queue_candidate_identity_review_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_repaired_burden_queue_candidate_identity_review_report.json"

IDENTITY_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_burden_queue_next_candidate_identity_preservation_fix_v0_receipts" / f"{SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID}.json"
SOURCE_AUDIT_PATH = ROOT / "data" / "r1000_burden_queue_next_candidate_identity_preservation_fix_v0" / "r1000_burden_queue_next_candidate_identity_source_audit.json"
REPAIRED_CANDIDATE_PATH = ROOT / "data" / "r1000_burden_queue_next_candidate_identity_preservation_fix_v0" / "r1000_next_selectable_group_candidate_after_burden_identity_preserved.json"
REPAIRED_SELECTED_GROUP_PATH = ROOT / "data" / "r1000_burden_queue_next_candidate_identity_preservation_fix_v0" / "r1000_selected_pressure_group_after_burden_identity_preserved.json"
IDENTITY_PRESERVATION_DECISION_PATH = ROOT / "data" / "r1000_burden_queue_next_candidate_identity_preservation_fix_v0" / "r1000_burden_queue_next_candidate_identity_preservation_decision.json"
IDENTITY_PRESERVATION_DIFF_PATH = ROOT / "data" / "r1000_burden_queue_next_candidate_identity_preservation_fix_v0" / "r1000_burden_queue_next_candidate_identity_preservation_diff.json"
INSPECTION_RELEASE_PACKET_PATH = ROOT / "data" / "r1000_burden_queue_next_candidate_identity_preservation_fix_v0" / "r1000_burden_queue_identity_preserved_inspection_release_packet.json"
IDENTITY_FIX_REPORT_PATH = ROOT / "data" / "r1000_burden_queue_next_candidate_identity_preservation_fix_v0" / "r1000_burden_queue_next_candidate_identity_preservation_report.json"

IDENTITY_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_selected_group_after_burden_identity_surface_review_v0_receipts" / f"{SOURCE_IDENTITY_REVIEW_RECEIPT_ID}.json"
SELECTION_AFTER_BURDEN_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_burden_pressure_reconciliation_v0_receipts" / f"{SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID}.json"
BURDEN_QUEUE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0_receipts" / f"{SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID}.json"
SELECTED_GROUP_INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_selected_pressure_group_inspection_from_reconciled_queue_v0_receipts" / f"{SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID}.json"
SELECTION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_from_reconciled_queue_v0_receipts" / f"{SOURCE_SELECTION_RECEIPT_ID}.json"
QUEUE_RECONCILIATION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0_receipts" / f"{SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID}.json"

SOURCE_FILES = [
    IDENTITY_FIX_RECEIPT_PATH,
    SOURCE_AUDIT_PATH,
    REPAIRED_CANDIDATE_PATH,
    REPAIRED_SELECTED_GROUP_PATH,
    IDENTITY_PRESERVATION_DECISION_PATH,
    IDENTITY_PRESERVATION_DIFF_PATH,
    INSPECTION_RELEASE_PACKET_PATH,
    IDENTITY_FIX_REPORT_PATH,
    IDENTITY_REVIEW_RECEIPT_PATH,
    SELECTION_AFTER_BURDEN_RECEIPT_PATH,
    BURDEN_QUEUE_RECEIPT_PATH,
    SELECTED_GROUP_INSPECTION_RECEIPT_PATH,
    SELECTION_RECEIPT_PATH,
    QUEUE_RECONCILIATION_RECEIPT_PATH,
]

RECOMMENDED_NEXT_HANDLING = "INSPECT_REPAIRED_R1000_BURDEN_QUEUE_SELECTED_GROUP_AFTER_IDENTITY_REVIEW_V0"

HUMAN_DECISION = {
    "decision": "REVIEW_REPAIRED_R1000_BURDEN_QUEUE_NEXT_CANDIDATE_IDENTITY_SURFACE",
    "scope": "review the repaired burden-queue candidate identity surface and decide whether it is identity-complete enough for a separate inspection unit; do not inspect rows, run R1000, reconcile queue, or mutate prior artifacts",
    "source_identity_preservation_fix_receipt_id": SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID,
    "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
    "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
    "authorized": [
        "consume identity preservation fix receipt",
        "consume repaired candidate artifact",
        "consume repaired selected group artifact",
        "materialize repaired identity review surface",
        "classify repaired identity completeness",
        "emit repaired identity acceptance packet",
        "emit separate inspection authority packet",
        "stop before inspection",
    ],
    "not_authorized": [
        "inspecting selected group rows",
        "materializing selected group row payloads",
        "running R1000",
        "queue reconciliation",
        "repairing sources",
        "mutating repaired candidate source artifact",
        "mutating existing receipts",
        "inventing identity fields",
        "assigning descriptor values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "opening another group",
        "hiding next command",
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
        "identity_fix_receipt": read_json(IDENTITY_FIX_RECEIPT_PATH),
        "source_audit": read_json(SOURCE_AUDIT_PATH),
        "repaired_candidate": read_json(REPAIRED_CANDIDATE_PATH),
        "repaired_selected_group": read_json(REPAIRED_SELECTED_GROUP_PATH),
        "identity_preservation_decision": read_json(IDENTITY_PRESERVATION_DECISION_PATH),
        "identity_preservation_diff": read_json(IDENTITY_PRESERVATION_DIFF_PATH),
        "inspection_release_packet": read_json(INSPECTION_RELEASE_PACKET_PATH),
        "identity_fix_report": read_json(IDENTITY_FIX_REPORT_PATH),
        "identity_review_receipt": read_json(IDENTITY_REVIEW_RECEIPT_PATH),
        "selection_after_burden_receipt": read_json(SELECTION_AFTER_BURDEN_RECEIPT_PATH),
        "burden_queue_receipt": read_json(BURDEN_QUEUE_RECEIPT_PATH),
        "selected_group_inspection_receipt": read_json(SELECTED_GROUP_INSPECTION_RECEIPT_PATH),
        "selection_receipt": read_json(SELECTION_RECEIPT_PATH),
        "queue_reconciliation_receipt": read_json(QUEUE_RECONCILIATION_RECEIPT_PATH),
    }

def is_unknown(v: Any) -> bool:
    return v is None or v == "" or v == "UNKNOWN"

def fully_typed(group: Dict[str, Any]) -> bool:
    return (
        not is_unknown(group.get("parent_pressure_class"))
        and not is_unknown(group.get("pressure_subtype"))
        and not is_unknown(group.get("halt_reason"))
        and int(group.get("row_count", 0) or 0) > 0
    )

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    fix_receipt = sources["identity_fix_receipt"]
    source_audit = sources["source_audit"]
    repaired_candidate = sources["repaired_candidate"]
    repaired_selected = sources["repaired_selected_group"]
    decision = sources["identity_preservation_decision"]
    release_packet = sources["inspection_release_packet"]

    if fix_receipt.get("receipt_id") != SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID:
        failures.append("identity_fix_receipt_id_wrong")
    if fix_receipt.get("gate") != "PASS":
        failures.append("identity_fix_not_pass")
    if fix_receipt.get("aggregate_metrics", {}).get("identity_preservation_fix_emitted_count") != 1:
        failures.append("identity_fix_not_emitted")
    if fix_receipt.get("aggregate_metrics", {}).get("unknown_identity_field_count_after") != 0:
        failures.append("identity_fix_unknown_fields_remain")
    if fix_receipt.get("aggregate_metrics", {}).get("field_value_invention_count") != 0:
        failures.append("identity_fix_invented_values")
    if fix_receipt.get("aggregate_metrics", {}).get("source_mutation_count") != 0:
        failures.append("identity_fix_mutated_source")
    if fix_receipt.get("aggregate_metrics", {}).get("selected_group_inspected_count") != 0:
        failures.append("identity_fix_already_inspected_group")

    if source_audit.get("audit_result") != "EXPLICIT_TYPED_IDENTITY_EVIDENCE_FOUND":
        failures.append("source_audit_no_explicit_evidence")
    if source_audit.get("usable_evidence_candidate_count", 0) < 1:
        failures.append("source_audit_usable_evidence_missing")

    if repaired_candidate.get("repaired_candidate_id") != REPAIRED_CANDIDATE_ID:
        failures.append("repaired_candidate_id_wrong")
    if repaired_candidate.get("selection_status") != "CANDIDATE_ONLY_NOT_OPENED":
        failures.append("repaired_candidate_status_wrong")
    if repaired_candidate.get("field_value_invention") is not False:
        failures.append("repaired_candidate_invented_value")
    if repaired_candidate.get("next_group_opened") is not False:
        failures.append("repaired_candidate_already_opened")
    if not fully_typed(repaired_candidate.get("candidate_summary_after", {})):
        failures.append("repaired_candidate_not_fully_typed")

    if repaired_selected.get("selected_pressure_group_id") != REPAIRED_SELECTED_PRESSURE_GROUP_ID:
        failures.append("repaired_selected_group_id_wrong")
    if repaired_selected.get("selection_status") != "SELECTED_NOT_INSPECTED":
        failures.append("repaired_selected_status_wrong")
    if repaired_selected.get("selected_group_rows_inspected") is not False:
        failures.append("repaired_selected_already_inspected")
    if repaired_selected.get("r1000_run_executed") is not False:
        failures.append("repaired_selected_r1000_already_run")
    if not fully_typed(repaired_selected.get("selected_group", {})):
        failures.append("repaired_selected_not_fully_typed")

    if decision.get("identity_preserved") is not True:
        failures.append("decision_identity_not_preserved")
    if decision.get("identity_assignment_by_invention") is not False:
        failures.append("decision_allows_invention")
    if decision.get("inspection_authorized_in_this_unit") is not False:
        failures.append("decision_authorized_inspection_in_fix_unit")
    if release_packet.get("packet_status") != "CANDIDATE_ONLY_NOT_EXECUTED":
        failures.append("release_packet_not_candidate_only")
    if release_packet.get("inspection_release_status") != "REQUIRES_SEPARATE_IDENTITY_REVIEW_BEFORE_INSPECTION":
        failures.append("release_packet_status_wrong")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def repaired_group_summary(sources: Dict[str, Any]) -> Dict[str, Any]:
    group = sources["repaired_selected_group"].get("selected_group", {})
    return {
        "parent_pressure_class": group.get("parent_pressure_class"),
        "pressure_subtype": group.get("pressure_subtype"),
        "halt_reason": group.get("halt_reason"),
        "row_count": int(group.get("row_count", 0) or 0),
    }

def identity_defects(group: Dict[str, Any]) -> List[Dict[str, Any]]:
    defects: List[Dict[str, Any]] = []
    for field in ["parent_pressure_class", "pressure_subtype", "halt_reason", "row_count"]:
        if field == "row_count":
            if int(group.get(field, 0) or 0) <= 0:
                defects.append({
                    "field": field,
                    "observed_value": group.get(field),
                    "defect_type": "MISSING_OR_ZERO_ROW_COUNT",
                    "severity": "BLOCKS_INSPECTION",
                })
        elif is_unknown(group.get(field)):
            defects.append({
                "field": field,
                "observed_value": group.get(field),
                "defect_type": "UNKNOWN_IDENTITY_FIELD",
                "severity": "BLOCKS_INSPECTION",
            })
    return defects

def build_identity_surface(sources: Dict[str, Any]) -> Dict[str, Any]:
    group = repaired_group_summary(sources)
    defects = identity_defects(group)
    return {
        "schema_version": "r1000_repaired_burden_queue_candidate_identity_surface_v0",
        "identity_surface_id": sha8({
            "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
            "group": group,
            "review": "repaired_identity_surface",
        }),
        "source_identity_preservation_fix_receipt_id": SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID,
        "source_repaired_candidate_id": REPAIRED_CANDIDATE_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "surface_status": "REPAIRED_IDENTITY_SURFACE_MATERIALIZED_FOR_REVIEW",
        "selected_group": group,
        "identity_fields_required_for_inspection": [
            "parent_pressure_class",
            "pressure_subtype",
            "halt_reason",
            "row_count",
        ],
        "identity_defects": defects,
        "identity_defect_count": len(defects),
        "unknown_identity_field_count": sum(1 for d in defects if d["defect_type"] == "UNKNOWN_IDENTITY_FIELD"),
        "identity_complete": len(defects) == 0,
        "identity_source_status": "PRESERVED_FROM_EXPLICIT_SOURCE_EVIDENCE",
        "field_value_invention": False,
        "row_payload_inspected": False,
        "r1000_run_executed": False,
    }

def build_decision(surface: Dict[str, Any]) -> Dict[str, Any]:
    identity_complete = surface["identity_complete"]
    return {
        "schema_version": "r1000_repaired_burden_queue_candidate_identity_review_decision_v0",
        "identity_review_decision_id": sha8({
            "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
            "identity_complete": identity_complete,
            "defect_count": surface["identity_defect_count"],
        }),
        "source_identity_surface_ref": rel(REPAIRED_IDENTITY_SURFACE_PATH),
        "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "decision_status": "ACCEPT_REPAIRED_IDENTITY_FOR_SEPARATE_INSPECTION" if identity_complete else "BLOCK_REPAIRED_IDENTITY_REQUIRES_ADDITIONAL_REPAIR",
        "identity_complete": identity_complete,
        "inspection_blocked": not identity_complete,
        "inspection_allowed_in_separate_unit": identity_complete,
        "inspection_authorized_in_this_unit": False,
        "repair_required": not identity_complete,
        "repair_authorized_in_this_unit": False,
        "selected_group": surface["selected_group"],
        "identity_defects": surface["identity_defects"],
        "recommended_next_handling": RECOMMENDED_NEXT_HANDLING if identity_complete else "FIX_REPAIRED_R1000_BURDEN_QUEUE_CANDIDATE_IDENTITY_SURFACE_V0",
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_REPAIRED_IDENTITY_SURFACE_REVIEW_COMPLETE_INSPECTION_ALLOWED" if identity_complete else "STOP_REPAIRED_IDENTITY_SURFACE_REVIEW_COMPLETE_REPAIR_REQUIRED",
            "next_command_goal": None,
        },
    }

def build_acceptance_packet(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_repaired_burden_queue_candidate_identity_acceptance_packet_v0",
        "packet_status": "REPAIRED_IDENTITY_ACCEPTED_FOR_SEPARATE_INSPECTION",
        "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "selected_group": surface["selected_group"],
        "identity_complete": surface["identity_complete"],
        "identity_defect_count": surface["identity_defect_count"],
        "field_value_invention": False,
        "source_mutation": False,
        "inspection_allowed_in_separate_unit": decision["inspection_allowed_in_separate_unit"],
        "inspection_authorized_in_this_unit": False,
    }

def build_inspection_authority_packet(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_repaired_burden_queue_candidate_inspection_authority_packet_v0",
        "packet_status": "SEPARATE_INSPECTION_AUTHORITY_PACKET",
        "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "selected_group": surface["selected_group"],
        "allowed_next_unit": decision["recommended_next_handling"],
        "allowed_next_unit_scope": [
            "consume repaired selected group artifact",
            "materialize metadata-level inspection surface",
            "classify selected group behavior",
            "emit typed inspection decision",
            "stop before queue reconciliation",
        ],
        "not_authorized_in_review_unit": [
            "row payload inspection",
            "R1000 execution",
            "queue reconciliation",
            "repair",
            "field filling",
            "value invention",
            "taxonomy action",
            "source mutation",
            "existing receipt mutation",
            "hidden next command",
        ],
    }

def build_transition_trace(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_repaired_burden_queue_candidate_identity_review_transition_trace_v0",
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "trace": [
            {
                "step": "consume_identity_preservation_fix",
                "question": "identity preservation fix passed and emitted repaired artifacts",
                "answer": True,
                "taken": "materialize_repaired_identity_surface",
            },
            {
                "step": "materialize_repaired_identity_surface",
                "question": "repaired identity is complete",
                "answer": surface["identity_complete"],
                "taken": "accept_for_separate_inspection" if surface["identity_complete"] else "block_for_additional_repair",
            },
            {
                "step": "accept_for_separate_inspection",
                "question": "inspect selected group in this unit",
                "answer": False,
                "taken": "emit_separate_inspection_authority_packet",
            },
            {
                "step": "emit_separate_inspection_authority_packet",
                "question": "hidden next command allowed",
                "answer": False,
                "taken": decision["terminal"]["stop_code"],
            },
        ],
        "terminal": decision["terminal"],
    }

def build_report(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    group = surface["selected_group"]
    return {
        "schema_version": "r1000_repaired_burden_queue_candidate_identity_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_identity_preservation_fix_receipt_id": SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID,
        "source_identity_review_receipt_id": SOURCE_IDENTITY_REVIEW_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "selected_parent_pressure_class": group.get("parent_pressure_class"),
        "selected_pressure_subtype": group.get("pressure_subtype"),
        "selected_halt_reason": group.get("halt_reason"),
        "selected_row_count": group.get("row_count"),
        "identity_preservation_fix_consumed_count": 1,
        "repaired_candidate_consumed_count": 1,
        "repaired_selected_group_consumed_count": 1,
        "repaired_identity_surface_materialized_count": 1,
        "repaired_identity_review_completed_count": 1,
        "identity_complete_count": 1 if surface["identity_complete"] else 0,
        "identity_defect_count": surface["identity_defect_count"],
        "unknown_identity_field_count": surface["unknown_identity_field_count"],
        "repaired_identity_accepted_count": 1 if decision["inspection_allowed_in_separate_unit"] else 0,
        "inspection_allowed_in_separate_unit_count": 1 if decision["inspection_allowed_in_separate_unit"] else 0,
        "inspection_authority_packet_emitted_count": 1,
        "identity_acceptance_packet_emitted_count": 1,
        "inspection_authorized_in_this_unit_count": 0,
        "repair_executed_count": 0,
        "identity_assignment_count": 0,
        "field_value_invention_count": 0,
        "selected_group_inspected_count": 0,
        "selected_group_rows_materialized_count": 0,
        "selected_group_rows_inspected_count": 0,
        "queue_reconciled_count": 0,
        "next_group_auto_opened_count": 0,
        "other_group_opened_count": 0,
        "r1000_run_executed_count": 0,
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

def validate_outputs(
    surface: Dict[str, Any],
    decision: Dict[str, Any],
    acceptance_packet: Dict[str, Any],
    authority_packet: Dict[str, Any],
    trace: Dict[str, Any],
    report: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if surface.get("surface_status") != "REPAIRED_IDENTITY_SURFACE_MATERIALIZED_FOR_REVIEW":
        failures.append("surface_status_wrong")
    if surface.get("identity_complete") is not True:
        failures.append("repaired_identity_not_complete")
    if surface.get("identity_defect_count") != 0:
        failures.append("identity_defects_remain")
    if surface.get("unknown_identity_field_count") != 0:
        failures.append("unknown_identity_fields_remain")
    if surface.get("field_value_invention") is not False:
        failures.append("surface_records_invention")

    if decision.get("decision_status") != "ACCEPT_REPAIRED_IDENTITY_FOR_SEPARATE_INSPECTION":
        failures.append("decision_status_wrong")
    if decision.get("inspection_allowed_in_separate_unit") is not True:
        failures.append("separate_inspection_not_allowed")
    if decision.get("inspection_authorized_in_this_unit") is not False:
        failures.append("inspection_authorized_in_review_unit")
    if decision.get("repair_authorized_in_this_unit") is not False:
        failures.append("repair_authorized_in_review_unit")

    if acceptance_packet.get("packet_status") != "REPAIRED_IDENTITY_ACCEPTED_FOR_SEPARATE_INSPECTION":
        failures.append("acceptance_packet_status_wrong")
    if acceptance_packet.get("field_value_invention") is not False:
        failures.append("acceptance_packet_records_invention")
    if acceptance_packet.get("inspection_authorized_in_this_unit") is not False:
        failures.append("acceptance_packet_authorizes_inspection_in_unit")

    if authority_packet.get("packet_status") != "SEPARATE_INSPECTION_AUTHORITY_PACKET":
        failures.append("authority_packet_status_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_next_not_null")

    for key in [
        "inspection_authorized_in_this_unit_count",
        "repair_executed_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "selected_group_inspected_count",
        "selected_group_rows_materialized_count",
        "selected_group_rows_inspected_count",
        "queue_reconciled_count",
        "next_group_auto_opened_count",
        "other_group_opened_count",
        "r1000_run_executed_count",
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

    if report.get("repaired_identity_review_completed_count") != 1:
        failures.append("identity_review_completed_count_wrong")
    if report.get("repaired_identity_accepted_count") != 1:
        failures.append("repaired_identity_accepted_count_wrong")
    if report.get("identity_complete_count") != 1:
        failures.append("identity_complete_count_wrong")
    if report.get("unknown_identity_field_count") != 0:
        failures.append("unknown_identity_count_wrong")

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
    if metrics.get("repaired_identity_review_completed_count") != 1:
        failures.append("metric_review_completed_wrong")
    if metrics.get("identity_complete_count") != 1:
        failures.append("metric_identity_complete_wrong")
    if metrics.get("unknown_identity_field_count") != 0:
        failures.append("metric_unknown_identity_not_zero")
    if metrics.get("inspection_allowed_in_separate_unit_count") != 1:
        failures.append("metric_separate_inspection_not_allowed")

    for key in [
        "inspection_authorized_in_this_unit_count",
        "repair_executed_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "selected_group_inspected_count",
        "selected_group_rows_materialized_count",
        "selected_group_rows_inspected_count",
        "queue_reconciled_count",
        "next_group_auto_opened_count",
        "other_group_opened_count",
        "r1000_run_executed_count",
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
    if terminal.get("stop_code") != "STOP_REPAIRED_IDENTITY_SURFACE_REVIEW_COMPLETE_INSPECTION_ALLOWED":
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
    acceptance_packet = build_acceptance_packet(surface, decision)
    authority_packet = build_inspection_authority_packet(surface, decision)
    trace = build_transition_trace(surface, decision)
    report = build_report(surface, decision)

    write_json(REPAIRED_IDENTITY_SURFACE_PATH, surface)
    write_json(REPAIRED_IDENTITY_REVIEW_DECISION_PATH, decision)
    write_json(REPAIRED_IDENTITY_ACCEPTANCE_PACKET_PATH, acceptance_packet)
    write_json(REPAIRED_INSPECTION_AUTHORITY_PACKET_PATH, authority_packet)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(surface, decision, acceptance_packet, authority_packet, trace, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "REPAIRED_IDENTITY_REVIEW_0_FIX_RECEIPT_CONSUMED": sources["identity_fix_receipt"]["receipt_id"] == SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID and sources["identity_fix_receipt"]["gate"] == "PASS",
        "REPAIRED_IDENTITY_REVIEW_1_REPAIRED_CANDIDATE_CONSUMED": sources["repaired_candidate"]["repaired_candidate_id"] == REPAIRED_CANDIDATE_ID,
        "REPAIRED_IDENTITY_REVIEW_2_REPAIRED_SELECTED_GROUP_CONSUMED": sources["repaired_selected_group"]["selected_pressure_group_id"] == REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "REPAIRED_IDENTITY_REVIEW_3_SURFACE_MATERIALIZED": surface["surface_status"] == "REPAIRED_IDENTITY_SURFACE_MATERIALIZED_FOR_REVIEW",
        "REPAIRED_IDENTITY_REVIEW_4_IDENTITY_COMPLETE": surface["identity_complete"] is True and surface["identity_defect_count"] == 0,
        "REPAIRED_IDENTITY_REVIEW_5_ACCEPTED_FOR_SEPARATE_INSPECTION": decision["inspection_allowed_in_separate_unit"] is True and decision["inspection_authorized_in_this_unit"] is False,
        "REPAIRED_IDENTITY_REVIEW_6_NO_IDENTITY_ASSIGNMENT_OR_INVENTION": report["identity_assignment_count"] == 0 and report["field_value_invention_count"] == 0,
        "REPAIRED_IDENTITY_REVIEW_7_NO_GROUP_INSPECTION_OR_QUEUE_RECONCILIATION": report["selected_group_inspected_count"] == 0 and report["queue_reconciled_count"] == 0,
        "REPAIRED_IDENTITY_REVIEW_8_NO_R1000_RUN_OR_REPAIR": report["r1000_run_executed_count"] == 0 and report["repair_executed_count"] == 0,
        "REPAIRED_IDENTITY_REVIEW_9_NO_FIELD_VALUE_OR_TAXONOMY_ACTION": report["target_field_filled_count"] == 0 and report["descriptor_value_assignment_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "REPAIRED_IDENTITY_REVIEW_10_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "REPAIRED_IDENTITY_REVIEW_11_NO_NEXT_GROUP_OR_HIDDEN_COMMAND": report["next_group_auto_opened_count"] == 0 and report["other_group_opened_count"] == 0 and report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_REPAIRED_IDENTITY_SURFACE_REVIEW_COMPLETE_INSPECTION_ALLOWED",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_AUTHORITY_VIOLATION",
            "next_command_goal": None,
        }

    aggregate_metrics = {
        "source_identity_preservation_fix_receipt_id": SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID,
        "source_identity_review_receipt_id": SOURCE_IDENTITY_REVIEW_RECEIPT_ID,
        "source_selection_after_burden_receipt_id": SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_selected_group_inspection_receipt_id": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "selected_parent_pressure_class": surface["selected_group"].get("parent_pressure_class"),
        "selected_pressure_subtype": surface["selected_group"].get("pressure_subtype"),
        "selected_halt_reason": surface["selected_group"].get("halt_reason"),
        "selected_row_count": surface["selected_group"].get("row_count"),
        "identity_preservation_fix_consumed_count": 1,
        "repaired_candidate_consumed_count": 1,
        "repaired_selected_group_consumed_count": 1,
        "repaired_identity_surface_materialized_count": 1,
        "repaired_identity_review_completed_count": 1,
        "identity_complete_count": 1,
        "identity_defect_count": surface["identity_defect_count"],
        "unknown_identity_field_count": surface["unknown_identity_field_count"],
        "repaired_identity_accepted_count": 1,
        "inspection_allowed_in_separate_unit_count": 1,
        "inspection_authority_packet_emitted_count": 1,
        "identity_acceptance_packet_emitted_count": 1,
        "inspection_authorized_in_this_unit_count": 0,
        "repair_executed_count": 0,
        "identity_assignment_count": 0,
        "field_value_invention_count": 0,
        "selected_group_inspected_count": 0,
        "selected_group_rows_materialized_count": 0,
        "selected_group_rows_inspected_count": 0,
        "queue_reconciled_count": 0,
        "next_group_auto_opened_count": 0,
        "other_group_opened_count": 0,
        "r1000_run_executed_count": 0,
        "proposal_applied_count": 0,
        "target_field_filled_count": 0,
        "descriptor_value_assignment_count": 0,
        "null_field_value_emitted_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": decision["recommended_next_handling"],
    }

    guards = {
        "identity_preservation_fix_consumed": True,
        "repaired_candidate_consumed": True,
        "repaired_selected_group_consumed": True,
        "repaired_identity_surface_materialized": True,
        "identity_complete": True,
        "identity_defects_remaining": False,
        "unknown_identity_fields_remaining": False,
        "repaired_identity_accepted": True,
        "inspection_allowed_in_separate_unit": True,
        "inspection_authorized_in_this_unit": False,
        "inspection_authority_packet_emitted": True,
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
        "source_identity_preservation_fix_receipt": SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID,
        "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "identity_complete": surface["identity_complete"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "repaired_identity_surface": rel(REPAIRED_IDENTITY_SURFACE_PATH),
        "repaired_identity_review_decision": rel(REPAIRED_IDENTITY_REVIEW_DECISION_PATH),
        "repaired_identity_acceptance_packet": rel(REPAIRED_IDENTITY_ACCEPTANCE_PACKET_PATH),
        "repaired_inspection_authority_packet": rel(REPAIRED_INSPECTION_AUTHORITY_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_repaired_burden_queue_candidate_identity_surface_review_receipt_v0",
        "receipt_type": "R1000_REPAIRED_BURDEN_QUEUE_CANDIDATE_IDENTITY_SURFACE_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_identity_preservation_fix_receipt_id": SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID,
        "source_identity_review_receipt_id": SOURCE_IDENTITY_REVIEW_RECEIPT_ID,
        "source_selection_after_burden_receipt_id": SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_selected_group_inspection_receipt_id": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "repaired_identity_surface_review_summary": {
            "review_result": "ACCEPT_REPAIRED_IDENTITY_FOR_SEPARATE_INSPECTION",
            "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
            "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
            "selected_group": surface["selected_group"],
            "identity_complete": surface["identity_complete"],
            "identity_defect_count": surface["identity_defect_count"],
            "unknown_identity_field_count": surface["unknown_identity_field_count"],
            "inspection_allowed_in_separate_unit": True,
            "inspection_authorized_in_this_unit": False,
            "recommended_next_handling": decision["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "repaired_identity_surface_review_guards": guards,
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
    print(f"repaired_identity_review_receipt_id={receipt_id}")
    print(f"repaired_identity_review_receipt_path=data/r1000_repaired_burden_queue_candidate_identity_surface_review_v0_receipts/{receipt_id}.json")
    print(f"repaired_identity_review_decision_path=data/r1000_repaired_burden_queue_candidate_identity_surface_review_v0/r1000_repaired_burden_queue_candidate_identity_review_decision.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
