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

UNIT_ID = "SELECT_NEXT_R1000_PRESSURE_GROUP_AFTER_REPAIRED_BURDEN_GROUP_QUEUE_RECONCILIATION_V0"
TARGET_UNIT_ID = "r1000_pressure_group.selection_after_repaired_burden_group_queue_reconciliation.v0"

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

OUT_DIR = ROOT / "data" / "r1000_pressure_group_selection_after_repaired_burden_group_queue_reconciliation_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_pressure_group_selection_after_repaired_burden_group_queue_reconciliation_v0_receipts"

SELECTED_GROUP_PATH = OUT_DIR / "r1000_selected_pressure_group_after_repaired_burden_queue_reconciliation.json"
SELECTION_DECISION_PATH = OUT_DIR / "r1000_pressure_group_selection_after_repaired_burden_queue_decision.json"
AUTHORITY_PACKET_PATH = OUT_DIR / "r1000_selected_pressure_group_after_repaired_burden_queue_authority_packet.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_pressure_group_selection_after_repaired_burden_queue_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_pressure_group_selection_after_repaired_burden_queue_report.json"

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
SELECTION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_from_reconciled_queue_v0_receipts" / f"{SOURCE_SELECTION_RECEIPT_ID}.json"
QUEUE_RECONCILIATION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0_receipts" / f"{SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID}.json"

SOURCE_FILES = [
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
    SELECTION_RECEIPT_PATH,
    QUEUE_RECONCILIATION_RECEIPT_PATH,
]

RECOMMENDED_NEXT_HANDLING = "REVIEW_SELECTED_R1000_PRESSURE_GROUP_AFTER_REPAIRED_BURDEN_QUEUE_RECONCILIATION_IDENTITY_SURFACE_V0"

HUMAN_DECISION = {
    "decision": "SELECT_NEXT_R1000_PRESSURE_GROUP_AFTER_REPAIRED_BURDEN_GROUP_QUEUE_RECONCILIATION",
    "scope": "consume repaired burden queue reconciliation next-candidate artifact and select it only; do not inspect, repair, run R1000, reconcile again, or open another group",
    "source_repaired_burden_queue_reconciliation_receipt_id": SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
    "authorized": [
        "consume repaired burden queue reconciliation receipt",
        "consume repaired burden queue next-candidate artifact",
        "consume repaired burden queue remaining-groups artifact",
        "materialize selected pressure group candidate",
        "emit selection decision",
        "emit authority packet for separate identity review",
        "stop before identity review or inspection",
    ],
    "not_authorized": [
        "inspecting selected group",
        "materializing row payloads",
        "running R1000",
        "repairing surfaces",
        "queue reconciliation",
        "opening another group",
        "assigning identity values",
        "inventing values",
        "filling fields",
        "assigning descriptor values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "emitting taxonomy delta proposal",
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
        "selection_receipt": read_json(SELECTION_RECEIPT_PATH),
        "queue_reconciliation_receipt": read_json(QUEUE_RECONCILIATION_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    receipt = sources["repaired_queue_receipt"]
    reconciliation = sources["repaired_queue_reconciliation"]
    candidate = sources["repaired_next_candidate"]

    if receipt.get("receipt_id") != SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID:
        failures.append("repaired_queue_receipt_id_wrong")
    if receipt.get("gate") != "PASS":
        failures.append("repaired_queue_not_pass")
    if receipt.get("aggregate_metrics", {}).get("queue_reconciled_count") != 1:
        failures.append("queue_not_reconciled")
    if receipt.get("aggregate_metrics", {}).get("next_group_candidate_emitted_count") != 1:
        failures.append("next_candidate_not_emitted")
    if receipt.get("aggregate_metrics", {}).get("next_group_auto_opened_count") != 0:
        failures.append("next_group_already_opened")
    if receipt.get("aggregate_metrics", {}).get("next_group_inspected_count") != 0:
        failures.append("next_group_already_inspected")
    if receipt.get("aggregate_metrics", {}).get("remaining_group_count_after") != 1:
        failures.append("remaining_group_count_unexpected")
    if receipt.get("aggregate_metrics", {}).get("remaining_row_count_after") != 1:
        failures.append("remaining_row_count_unexpected")

    if reconciliation.get("queue_reconciled") is not True:
        failures.append("reconciliation_not_true")
    if reconciliation.get("next_group_opened") is not False:
        failures.append("reconciliation_opened_next_group")

    if candidate.get("selection_status") != "CANDIDATE_ONLY_NOT_OPENED":
        failures.append("candidate_not_selectable")
    if candidate.get("next_group_opened") is not False:
        failures.append("candidate_already_opened")
    if candidate.get("next_group_inspected") is not False:
        failures.append("candidate_already_inspected")
    if candidate.get("row_payload_materialized") is not False:
        failures.append("candidate_row_payload_materialized")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def candidate_summary(candidate: Dict[str, Any]) -> Dict[str, Any]:
    summary = candidate.get("candidate_summary") if isinstance(candidate.get("candidate_summary"), dict) else {}
    return {
        "parent_pressure_class": summary.get("parent_pressure_class", "UNKNOWN"),
        "pressure_subtype": summary.get("pressure_subtype", "UNKNOWN"),
        "halt_reason": summary.get("halt_reason", "UNKNOWN"),
        "row_count": int(summary.get("row_count", 0) or 0),
    }

def build_selected_group(sources: Dict[str, Any]) -> Dict[str, Any]:
    candidate = sources["repaired_next_candidate"]
    summary = candidate_summary(candidate)
    selected_id = sha8({
        "source_repaired_burden_queue_reconciliation_receipt_id": SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_candidate_id": candidate.get("candidate_id"),
        "summary": summary,
        "selection": "after_repaired_burden_queue_reconciliation",
    })
    return {
        "schema_version": "r1000_selected_pressure_group_after_repaired_burden_queue_reconciliation_v0",
        "selected_pressure_group_id": selected_id,
        "source_repaired_burden_queue_reconciliation_receipt_id": SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_candidate_id": candidate.get("candidate_id"),
        "source_candidate_ref": rel(REPAIRED_NEXT_CANDIDATE_PATH),
        "source_remaining_groups_ref": rel(REPAIRED_REMAINING_GROUPS_PATH),
        "selection_status": "SELECTED_NOT_INSPECTED",
        "selected_group": summary,
        "candidate_identity_status": candidate.get("candidate_identity_status", "UNKNOWN"),
        "requires_identity_review_before_inspection": bool(candidate.get("requires_identity_review_before_inspection", True)),
        "selected_group_rows_materialized": False,
        "selected_group_rows_inspected": False,
        "identity_review_executed": False,
        "r1000_run_executed": False,
        "queue_reconciled": False,
    }

def build_decision(selected: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_pressure_group_selection_after_repaired_burden_queue_decision_v0",
        "selection_decision_id": sha8({
            "selected_pressure_group_id": selected["selected_pressure_group_id"],
            "selected_group": selected["selected_group"],
        }),
        "decision_status": "SELECT_NEXT_GROUP_AFTER_REPAIRED_BURDEN_QUEUE_RECONCILIATION",
        "source_repaired_burden_queue_reconciliation_receipt_id": SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": selected["selected_pressure_group_id"],
        "selected_group": selected["selected_group"],
        "selection_result": "SELECTED_NOT_INSPECTED",
        "identity_review_required_before_inspection": selected["requires_identity_review_before_inspection"],
        "inspection_authorized_in_this_unit": False,
        "identity_review_authorized_in_this_unit": False,
        "queue_reconciliation_authorized_in_this_unit": False,
        "recommended_next_handling": RECOMMENDED_NEXT_HANDLING,
    }

def build_authority_packet(selected: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_pressure_group_after_repaired_burden_queue_authority_packet_v0",
        "packet_status": "SEPARATE_IDENTITY_REVIEW_REQUIRED",
        "source_selection_decision_ref": rel(SELECTION_DECISION_PATH),
        "selected_pressure_group_id": selected["selected_pressure_group_id"],
        "selected_group": selected["selected_group"],
        "candidate_identity_status": selected["candidate_identity_status"],
        "identity_review_required_before_inspection": selected["requires_identity_review_before_inspection"],
        "allowed_next_unit": decision["recommended_next_handling"],
        "allowed_next_unit_scope": [
            "consume selected pressure group artifact",
            "materialize identity surface",
            "classify identity completeness",
            "decide whether separate inspection is allowed",
            "stop before inspection",
        ],
        "not_authorized_in_selection_unit": [
            "identity review",
            "inspection",
            "row payload materialization",
            "R1000 execution",
            "repair",
            "queue reconciliation",
            "field filling",
            "value invention",
            "taxonomy action",
            "source mutation",
            "receipt mutation",
            "hidden next command",
        ],
    }

def build_trace(selected: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_pressure_group_selection_after_repaired_burden_queue_transition_trace_v0",
        "selected_pressure_group_id": selected["selected_pressure_group_id"],
        "trace": [
            {
                "step": "consume_repaired_burden_queue_reconciliation",
                "question": "queue reconciled and next candidate emitted",
                "answer": True,
                "taken": "consume_next_candidate",
            },
            {
                "step": "consume_next_candidate",
                "question": "candidate selectable and not opened",
                "answer": True,
                "taken": "materialize_selected_group",
            },
            {
                "step": "materialize_selected_group",
                "question": "inspect or identity-review selected group in this unit",
                "answer": False,
                "taken": "emit_authority_packet",
            },
            {
                "step": "emit_authority_packet",
                "question": "hidden next command allowed",
                "answer": False,
                "taken": "STOP_R1000_PRESSURE_GROUP_SELECTED_AFTER_REPAIRED_BURDEN_QUEUE_RECONCILIATION_IDENTITY_REVIEW_REQUIRED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_R1000_PRESSURE_GROUP_SELECTED_AFTER_REPAIRED_BURDEN_QUEUE_RECONCILIATION_IDENTITY_REVIEW_REQUIRED",
            "next_command_goal": None,
        },
    }

def build_report(selected: Dict[str, Any]) -> Dict[str, Any]:
    group = selected["selected_group"]
    return {
        "schema_version": "r1000_pressure_group_selection_after_repaired_burden_queue_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_repaired_burden_queue_reconciliation_receipt_id": SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": selected["selected_pressure_group_id"],
        "selected_parent_pressure_class": group.get("parent_pressure_class"),
        "selected_pressure_subtype": group.get("pressure_subtype"),
        "selected_halt_reason": group.get("halt_reason"),
        "selected_row_count": group.get("row_count"),
        "candidate_identity_status": selected["candidate_identity_status"],
        "requires_identity_review_before_inspection": selected["requires_identity_review_before_inspection"],
        "source_queue_reconciliation_consumed_count": 1,
        "source_next_candidate_consumed_count": 1,
        "pressure_group_selected_count": 1,
        "selected_group_materialized_count": 1,
        "authority_packet_emitted_count": 1,
        "selected_group_rows_materialized_count": 0,
        "selected_group_rows_inspected_count": 0,
        "selected_group_inspected_count": 0,
        "identity_review_executed_count": 0,
        "queue_reconciled_count": 0,
        "next_group_auto_opened_count": 0,
        "other_group_opened_count": 0,
        "r1000_run_executed_count": 0,
        "repair_executed_count": 0,
        "proposal_applied_count": 0,
        "target_field_filled_count": 0,
        "descriptor_value_assignment_count": 0,
        "null_field_value_emitted_count": 0,
        "field_value_invention_count": 0,
        "identity_assignment_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": RECOMMENDED_NEXT_HANDLING,
    }

def validate_outputs(selected: Dict[str, Any], decision: Dict[str, Any], authority: Dict[str, Any], trace: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if selected.get("selection_status") != "SELECTED_NOT_INSPECTED":
        failures.append("selected_status_wrong")
    if selected.get("selected_group_rows_inspected") is not False:
        failures.append("selected_rows_inspected")
    if selected.get("identity_review_executed") is not False:
        failures.append("identity_review_executed_in_selection")
    if selected.get("r1000_run_executed") is not False:
        failures.append("r1000_run_executed_in_selection")
    if decision.get("inspection_authorized_in_this_unit") is not False:
        failures.append("inspection_authorized_in_selection_unit")
    if decision.get("identity_review_authorized_in_this_unit") is not False:
        failures.append("identity_review_authorized_in_selection_unit")
    if authority.get("packet_status") != "SEPARATE_IDENTITY_REVIEW_REQUIRED":
        failures.append("authority_packet_status_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_next_not_null")

    for key in [
        "selected_group_rows_materialized_count",
        "selected_group_rows_inspected_count",
        "selected_group_inspected_count",
        "identity_review_executed_count",
        "queue_reconciled_count",
        "next_group_auto_opened_count",
        "other_group_opened_count",
        "r1000_run_executed_count",
        "repair_executed_count",
        "proposal_applied_count",
        "target_field_filled_count",
        "descriptor_value_assignment_count",
        "null_field_value_emitted_count",
        "field_value_invention_count",
        "identity_assignment_count",
        "taxonomy_label_creation_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "hidden_next_command_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")

    if report.get("pressure_group_selected_count") != 1:
        failures.append("pressure_group_selected_count_wrong")
    if report.get("selected_group_materialized_count") != 1:
        failures.append("selected_group_materialized_count_wrong")
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
    if metrics.get("pressure_group_selected_count") != 1:
        failures.append("metric_pressure_group_selected_wrong")
    if metrics.get("authority_packet_emitted_count") != 1:
        failures.append("metric_authority_packet_wrong")

    for key in [
        "selected_group_rows_materialized_count",
        "selected_group_rows_inspected_count",
        "selected_group_inspected_count",
        "identity_review_executed_count",
        "queue_reconciled_count",
        "next_group_auto_opened_count",
        "other_group_opened_count",
        "r1000_run_executed_count",
        "repair_executed_count",
        "proposal_applied_count",
        "target_field_filled_count",
        "descriptor_value_assignment_count",
        "null_field_value_emitted_count",
        "field_value_invention_count",
        "identity_assignment_count",
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
    if terminal.get("stop_code") != "STOP_R1000_PRESSURE_GROUP_SELECTED_AFTER_REPAIRED_BURDEN_QUEUE_RECONCILIATION_IDENTITY_REVIEW_REQUIRED":
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

    selected = build_selected_group(sources)
    decision = build_decision(selected)
    authority = build_authority_packet(selected, decision)
    trace = build_trace(selected)
    report = build_report(selected)

    write_json(SELECTED_GROUP_PATH, selected)
    write_json(SELECTION_DECISION_PATH, decision)
    write_json(AUTHORITY_PACKET_PATH, authority)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(selected, decision, authority, trace, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "SELECT_AFTER_REPAIRED_BURDEN_QUEUE_0_RECONCILIATION_CONSUMED": sources["repaired_queue_receipt"]["receipt_id"] == SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID and sources["repaired_queue_receipt"]["gate"] == "PASS",
        "SELECT_AFTER_REPAIRED_BURDEN_QUEUE_1_NEXT_CANDIDATE_CONSUMED": sources["repaired_next_candidate"]["selection_status"] == "CANDIDATE_ONLY_NOT_OPENED",
        "SELECT_AFTER_REPAIRED_BURDEN_QUEUE_2_GROUP_SELECTED": selected["selection_status"] == "SELECTED_NOT_INSPECTED",
        "SELECT_AFTER_REPAIRED_BURDEN_QUEUE_3_AUTHORITY_PACKET_EMITTED": authority["packet_status"] == "SEPARATE_IDENTITY_REVIEW_REQUIRED",
        "SELECT_AFTER_REPAIRED_BURDEN_QUEUE_4_NO_IDENTITY_REVIEW_OR_INSPECTION": report["identity_review_executed_count"] == 0 and report["selected_group_inspected_count"] == 0,
        "SELECT_AFTER_REPAIRED_BURDEN_QUEUE_5_NO_ROW_PAYLOAD_OR_R1000": report["selected_group_rows_materialized_count"] == 0 and report["r1000_run_executed_count"] == 0,
        "SELECT_AFTER_REPAIRED_BURDEN_QUEUE_6_NO_REPAIR_FIELD_VALUE_OR_TAXONOMY": report["repair_executed_count"] == 0 and report["target_field_filled_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "SELECT_AFTER_REPAIRED_BURDEN_QUEUE_7_NO_QUEUE_RECONCILIATION_OR_NEXT_OPEN": report["queue_reconciled_count"] == 0 and report["next_group_auto_opened_count"] == 0 and report["other_group_opened_count"] == 0,
        "SELECT_AFTER_REPAIRED_BURDEN_QUEUE_8_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "SELECT_AFTER_REPAIRED_BURDEN_QUEUE_9_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
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
        "repaired_queue_reconciliation_consumed": True,
        "next_candidate_consumed": True,
        "pressure_group_selected": True,
        "authority_packet_emitted": True,
        "identity_review_executed": False,
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
        "field_value_invention": False,
        "identity_assignment": False,
        "taxonomy_label_created": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_repaired_queue_receipt": SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": selected["selected_pressure_group_id"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "selected_pressure_group": rel(SELECTED_GROUP_PATH),
        "selection_decision": rel(SELECTION_DECISION_PATH),
        "authority_packet": rel(AUTHORITY_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_pressure_group_selection_after_repaired_burden_queue_reconciliation_receipt_v0",
        "receipt_type": "R1000_PRESSURE_GROUP_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
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
        "selected_pressure_group_id": selected["selected_pressure_group_id"],
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "selection_after_repaired_burden_queue_summary": {
            "selection_result": "SELECTED_NOT_INSPECTED",
            "selected_pressure_group_id": selected["selected_pressure_group_id"],
            "selected_group": selected["selected_group"],
            "candidate_identity_status": selected["candidate_identity_status"],
            "requires_identity_review_before_inspection": selected["requires_identity_review_before_inspection"],
            "recommended_next_handling": RECOMMENDED_NEXT_HANDLING,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "selection_after_repaired_burden_queue_guards": guards,
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
    print(f"selection_after_repaired_burden_queue_receipt_id={receipt_id}")
    print(f"selection_after_repaired_burden_queue_receipt_path=data/r1000_pressure_group_selection_after_repaired_burden_group_queue_reconciliation_v0_receipts/{receipt_id}.json")
    print(f"selected_group_after_repaired_burden_queue_path=data/r1000_pressure_group_selection_after_repaired_burden_group_queue_reconciliation_v0/r1000_selected_pressure_group_after_repaired_burden_queue_reconciliation.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
