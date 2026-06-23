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

UNIT_ID = "REVIEW_R1000_PRESSURE_QUEUE_CLOSURE_AFTER_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_V0"
TARGET_UNIT_ID = "r1000_pressure_queue.closure_review_after_synthetic_remainder_expected_limit.v0"

SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID = "db7c0af2"
SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID = "9d2f4dc1"
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

OUT_DIR = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0_receipts"

CLOSURE_REVIEW_SURFACE_PATH = OUT_DIR / "r1000_pressure_queue_closure_review_surface_after_synthetic_remainder_expected_limit.json"
CLOSURE_REVIEW_DECISION_PATH = OUT_DIR / "r1000_pressure_queue_closure_review_decision_after_synthetic_remainder_expected_limit.json"
CLOSURE_ACCEPTANCE_PACKET_PATH = OUT_DIR / "r1000_pressure_queue_closure_acceptance_packet_after_synthetic_remainder_expected_limit.json"
FINAL_CLOSURE_HANDBACK_PATH = OUT_DIR / "r1000_pressure_queue_closed_handoff_after_synthetic_remainder_expected_limit.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_pressure_queue_closure_review_transition_trace_after_synthetic_remainder_expected_limit.json"
REPORT_PATH = OUT_DIR / "r1000_pressure_queue_closure_review_report_after_synthetic_remainder_expected_limit.json"

EXPECTED_LIMIT_MARK_RECEIPT_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID}.json"
MARK_DECISION_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_decision.json"
MARKED_EXPECTED_LIMIT_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_synthetic_remainder_marked_expected_queue_resolution_limit.json"
QUEUE_CLOSURE_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_pressure_queue_closure_after_synthetic_remainder_expected_limit.json"
RESOLUTION_LEDGER_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_synthetic_remainder_expected_limit_resolution_ledger.json"
FINAL_QUEUE_STATE_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_final_pressure_queue_state_after_synthetic_remainder_expected_limit.json"
INSPECTION_BLOCK_FINAL_PACKET_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_synthetic_remainder_final_inspection_block_packet_after_expected_limit.json"
EXPECTED_LIMIT_MARK_REPORT_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_synthetic_remainder_expected_limit_mark_report.json"

SOURCE_AUDIT_RECEIPT_PATH = ROOT / "data" / "r1000_synthetic_remainder_source_evidence_audit_after_repaired_burden_queue_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID}.json"
IDENTITY_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_selected_synthetic_remainder_identity_surface_review_after_repaired_burden_queue_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID}.json"
SELECTION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_repaired_burden_group_queue_reconciliation_v0_receipts" / f"{SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID}.json"
REPAIRED_QUEUE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_v0_receipts" / f"{SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID}.json"
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
    EXPECTED_LIMIT_MARK_RECEIPT_PATH,
    MARK_DECISION_PATH,
    MARKED_EXPECTED_LIMIT_PATH,
    QUEUE_CLOSURE_PATH,
    RESOLUTION_LEDGER_PATH,
    FINAL_QUEUE_STATE_PATH,
    INSPECTION_BLOCK_FINAL_PACKET_PATH,
    EXPECTED_LIMIT_MARK_REPORT_PATH,
    SOURCE_AUDIT_RECEIPT_PATH,
    IDENTITY_REVIEW_RECEIPT_PATH,
    SELECTION_RECEIPT_PATH,
    REPAIRED_QUEUE_RECEIPT_PATH,
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

HUMAN_DECISION = {
    "decision": "REVIEW_R1000_PRESSURE_QUEUE_CLOSURE_AFTER_SYNTHETIC_REMAINDER_EXPECTED_LIMIT",
    "scope": "review the derived final queue closure after synthetic remainder expected-limit mark; accept closure if all pressure groups and rows are resolved and no forbidden actions occurred",
    "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
    "authorized": [
        "consume expected-limit mark receipt",
        "consume final queue state artifact",
        "consume queue closure artifact",
        "verify queue closed counts",
        "verify closure was derived only",
        "verify no inspection, R1000 run, identity assignment, source mutation, receipt mutation, next-group opening, or hidden next command",
        "emit closure review decision",
        "emit closure acceptance packet",
        "emit closed queue handoff",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "running R1000",
        "opening any next group",
        "inspecting any group",
        "materializing row payloads",
        "repairing surfaces",
        "assigning identity values",
        "inventing values",
        "filling fields",
        "assigning descriptor values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "emitting taxonomy delta proposal",
        "mutating source artifacts",
        "mutating existing receipts",
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
        "expected_limit_mark_receipt": read_json(EXPECTED_LIMIT_MARK_RECEIPT_PATH),
        "mark_decision": read_json(MARK_DECISION_PATH),
        "marked_expected_limit": read_json(MARKED_EXPECTED_LIMIT_PATH),
        "queue_closure": read_json(QUEUE_CLOSURE_PATH),
        "resolution_ledger": read_json(RESOLUTION_LEDGER_PATH),
        "final_queue_state": read_json(FINAL_QUEUE_STATE_PATH),
        "inspection_block_final_packet": read_json(INSPECTION_BLOCK_FINAL_PACKET_PATH),
        "expected_limit_mark_report": read_json(EXPECTED_LIMIT_MARK_REPORT_PATH),
        "source_audit_receipt": read_json(SOURCE_AUDIT_RECEIPT_PATH),
        "identity_review_receipt": read_json(IDENTITY_REVIEW_RECEIPT_PATH),
        "selection_receipt": read_json(SELECTION_RECEIPT_PATH),
        "repaired_queue_receipt": read_json(REPAIRED_QUEUE_RECEIPT_PATH),
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
    receipt = sources["expected_limit_mark_receipt"]
    final_state = sources["final_queue_state"]
    queue_closure = sources["queue_closure"]
    marked = sources["marked_expected_limit"]
    report = sources["expected_limit_mark_report"]

    if receipt.get("receipt_id") != SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID:
        failures.append("expected_limit_mark_receipt_id_wrong")
    if receipt.get("gate") != "PASS":
        failures.append("expected_limit_mark_not_pass")
    if receipt.get("selected_pressure_group_id") != SELECTED_PRESSURE_GROUP_ID:
        failures.append("selected_pressure_group_id_wrong_in_mark_receipt")

    if receipt.get("aggregate_metrics", {}).get("expected_limit_mark_applied_count") != 1:
        failures.append("expected_limit_mark_not_applied")
    if receipt.get("aggregate_metrics", {}).get("expected_limit_closure_applied_count") != 1:
        failures.append("expected_limit_closure_not_applied")
    if receipt.get("aggregate_metrics", {}).get("queue_closed_count") != 1:
        failures.append("queue_not_closed_in_receipt")
    if receipt.get("aggregate_metrics", {}).get("remaining_group_count_after") != 0:
        failures.append("remaining_group_count_not_zero_in_receipt")
    if receipt.get("aggregate_metrics", {}).get("remaining_row_count_after") != 0:
        failures.append("remaining_row_count_not_zero_in_receipt")
    if receipt.get("aggregate_metrics", {}).get("resolved_group_count_after") != receipt.get("aggregate_metrics", {}).get("total_group_count"):
        failures.append("resolved_group_count_not_total_in_receipt")
    if receipt.get("aggregate_metrics", {}).get("resolved_row_count_after") != receipt.get("aggregate_metrics", {}).get("total_pressure_row_count"):
        failures.append("resolved_row_count_not_total_in_receipt")

    if final_state.get("queue_state_status") != "R1000_PRESSURE_QUEUE_CLOSED":
        failures.append("final_queue_state_status_wrong")
    if final_state.get("queue_closed") is not True:
        failures.append("final_queue_not_closed")
    if final_state.get("remaining_open_group_count") != 0:
        failures.append("final_remaining_group_count_not_zero")
    if final_state.get("remaining_open_row_count") != 0:
        failures.append("final_remaining_row_count_not_zero")
    if final_state.get("next_selectable_group_candidate") is not None:
        failures.append("final_next_candidate_not_null")

    if queue_closure.get("queue_closure_status") != "R1000_PRESSURE_QUEUE_CLOSED_BY_EXPECTED_QUEUE_RESOLUTION_LIMIT":
        failures.append("queue_closure_status_wrong")
    if queue_closure.get("queue_closed") is not True:
        failures.append("queue_closure_not_closed")
    if queue_closure.get("next_group_candidate_emitted") is not False:
        failures.append("queue_closure_emitted_next_candidate")
    if queue_closure.get("next_group_opened") is not False:
        failures.append("queue_closure_opened_next_group")

    if marked.get("limit_status") != "MARKED_APPLIED_IN_DERIVED_QUEUE_STATE":
        failures.append("marked_limit_status_wrong")
    if marked.get("expected_limit_closure_applied") is not True:
        failures.append("marked_limit_not_applied")
    if marked.get("source_mutation") is not False:
        failures.append("marked_limit_source_mutation")

    for key in [
        "inspection_authorized_in_this_unit_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "selected_group_inspected_count",
        "selected_group_rows_materialized_count",
        "selected_group_rows_inspected_count",
        "queue_reconciled_count",
        "next_group_candidate_emitted_count",
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
            failures.append(f"source_report_forbidden_count_not_zero:{key}:{report.get(key)}")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_review_surface(sources: Dict[str, Any]) -> Dict[str, Any]:
    final_state = sources["final_queue_state"]
    mark_receipt = sources["expected_limit_mark_receipt"]
    return {
        "schema_version": "r1000_pressure_queue_closure_review_surface_after_synthetic_remainder_expected_limit_v0",
        "closure_review_surface_id": sha8({
            "source_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
            "final_queue_state": final_state,
        }),
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "source_final_queue_state_ref": rel(FINAL_QUEUE_STATE_PATH),
        "source_queue_closure_ref": rel(QUEUE_CLOSURE_PATH),
        "surface_status": "PRESSURE_QUEUE_CLOSURE_REVIEW_SURFACE_MATERIALIZED",
        "queue_state_status": final_state.get("queue_state_status"),
        "queue_closed": final_state.get("queue_closed"),
        "total_group_count": final_state.get("total_group_count"),
        "total_pressure_row_count": final_state.get("total_pressure_row_count"),
        "resolved_group_count": final_state.get("resolved_group_count"),
        "resolved_row_count": final_state.get("resolved_row_count"),
        "remaining_open_group_count": final_state.get("remaining_open_group_count"),
        "remaining_open_row_count": final_state.get("remaining_open_row_count"),
        "next_selectable_group_candidate": final_state.get("next_selectable_group_candidate"),
        "mark_receipt_gate": mark_receipt.get("gate"),
        "closure_basis": "synthetic remainder expected queue-resolution limit",
        "closure_review_required": True,
    }

def build_decision(surface: Dict[str, Any]) -> Dict[str, Any]:
    closed_ok = (
        surface["queue_closed"] is True
        and surface["remaining_open_group_count"] == 0
        and surface["remaining_open_row_count"] == 0
        and surface["resolved_group_count"] == surface["total_group_count"]
        and surface["resolved_row_count"] == surface["total_pressure_row_count"]
        and surface["next_selectable_group_candidate"] is None
    )
    return {
        "schema_version": "r1000_pressure_queue_closure_review_decision_after_synthetic_remainder_expected_limit_v0",
        "closure_review_decision_id": sha8({
            "source_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
            "closed_ok": closed_ok,
        }),
        "source_closure_review_surface_ref": rel(CLOSURE_REVIEW_SURFACE_PATH),
        "decision_status": "ACCEPT_R1000_PRESSURE_QUEUE_CLOSURE" if closed_ok else "BLOCK_R1000_PRESSURE_QUEUE_CLOSURE_REVIEW",
        "queue_closure_accepted": closed_ok,
        "queue_closed": surface["queue_closed"],
        "remaining_pressure_zero": surface["remaining_open_group_count"] == 0 and surface["remaining_open_row_count"] == 0,
        "resolved_counts_match_totals": surface["resolved_group_count"] == surface["total_group_count"] and surface["resolved_row_count"] == surface["total_pressure_row_count"],
        "next_candidate_absent": surface["next_selectable_group_candidate"] is None,
        "r1000_run_authorized": False,
        "inspection_authorized": False,
        "queue_reopen_authorized": False,
        "source_mutation_authorized": False,
        "recommended_next_handling": None,
    }

def build_acceptance_packet(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_pressure_queue_closure_acceptance_packet_after_synthetic_remainder_expected_limit_v0",
        "packet_status": "R1000_PRESSURE_QUEUE_CLOSURE_ACCEPTED",
        "source_closure_review_decision_ref": rel(CLOSURE_REVIEW_DECISION_PATH),
        "source_final_queue_state_ref": rel(FINAL_QUEUE_STATE_PATH),
        "queue_closure_accepted": decision["queue_closure_accepted"],
        "queue_state_status": surface["queue_state_status"],
        "queue_closed": surface["queue_closed"],
        "total_group_count": surface["total_group_count"],
        "total_pressure_row_count": surface["total_pressure_row_count"],
        "resolved_group_count": surface["resolved_group_count"],
        "resolved_row_count": surface["resolved_row_count"],
        "remaining_open_group_count": surface["remaining_open_group_count"],
        "remaining_open_row_count": surface["remaining_open_row_count"],
        "next_selectable_group_candidate": None,
        "closure_basis": surface["closure_basis"],
        "further_queue_action_required": False,
    }

def build_handoff(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_pressure_queue_closed_handoff_after_synthetic_remainder_expected_limit_v0",
        "handoff_status": "R1000_PRESSURE_QUEUE_CLOSED_NO_REMAINING_PRESSURE",
        "source_acceptance_packet_ref": rel(CLOSURE_ACCEPTANCE_PACKET_PATH),
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "queue_closure_accepted": decision["queue_closure_accepted"],
        "queue_closed": True,
        "remaining_open_group_count": 0,
        "remaining_open_row_count": 0,
        "resolved_group_count": surface["resolved_group_count"],
        "resolved_row_count": surface["resolved_row_count"],
        "total_group_count": surface["total_group_count"],
        "total_pressure_row_count": surface["total_pressure_row_count"],
        "terminal_state": "PRESSURE_QUEUE_CLOSED",
        "next_command_goal": None,
        "recommended_next_handling": None,
    }

def build_transition_trace(decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_pressure_queue_closure_review_transition_trace_after_synthetic_remainder_expected_limit_v0",
        "trace": [
            {
                "step": "consume_expected_limit_mark_receipt",
                "question": "mark receipt passed and expected-limit closure was applied",
                "answer": True,
                "taken": "consume_final_queue_state",
            },
            {
                "step": "consume_final_queue_state",
                "question": "queue is closed and remaining pressure is zero",
                "answer": True,
                "taken": "accept_queue_closure",
            },
            {
                "step": "accept_queue_closure",
                "question": "any next group candidate remains",
                "answer": False,
                "taken": "emit_closed_queue_handoff",
            },
            {
                "step": "emit_closed_queue_handoff",
                "question": "hidden next command allowed",
                "answer": False,
                "taken": "STOP_R1000_PRESSURE_QUEUE_CLOSURE_REVIEW_COMPLETE_QUEUE_CLOSED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_R1000_PRESSURE_QUEUE_CLOSURE_REVIEW_COMPLETE_QUEUE_CLOSED",
            "next_command_goal": None,
        },
    }

def build_report(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_pressure_queue_closure_review_report_after_synthetic_remainder_expected_limit_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "source_synthetic_remainder_source_audit_receipt_id": SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID,
        "expected_limit_mark_receipt_consumed_count": 1,
        "final_queue_state_consumed_count": 1,
        "queue_closure_artifact_consumed_count": 1,
        "closure_review_surface_materialized_count": 1,
        "closure_review_completed_count": 1,
        "queue_closure_accepted_count": 1 if decision["queue_closure_accepted"] else 0,
        "closed_queue_handoff_emitted_count": 1,
        "remaining_pressure_zero_confirmed_count": 1,
        "resolved_counts_match_totals_count": 1,
        "next_candidate_absent_count": 1,
        "total_group_count": surface["total_group_count"],
        "total_pressure_row_count": surface["total_pressure_row_count"],
        "resolved_group_count": surface["resolved_group_count"],
        "resolved_row_count": surface["resolved_row_count"],
        "remaining_open_group_count": surface["remaining_open_group_count"],
        "remaining_open_row_count": surface["remaining_open_row_count"],
        "inspection_authorized_in_this_unit_count": 0,
        "identity_assignment_count": 0,
        "field_value_invention_count": 0,
        "selected_group_inspected_count": 0,
        "selected_group_rows_materialized_count": 0,
        "selected_group_rows_inspected_count": 0,
        "queue_reconciled_count": 0,
        "queue_reopened_count": 0,
        "next_group_candidate_emitted_count": 0,
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
        "recommended_next_handling": None,
    }

def validate_outputs(surface: Dict[str, Any], decision: Dict[str, Any], acceptance: Dict[str, Any], handoff: Dict[str, Any], trace: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if surface.get("surface_status") != "PRESSURE_QUEUE_CLOSURE_REVIEW_SURFACE_MATERIALIZED":
        failures.append("surface_status_wrong")
    if decision.get("decision_status") != "ACCEPT_R1000_PRESSURE_QUEUE_CLOSURE":
        failures.append("decision_status_wrong")
    if decision.get("queue_closure_accepted") is not True:
        failures.append("queue_closure_not_accepted")
    if acceptance.get("packet_status") != "R1000_PRESSURE_QUEUE_CLOSURE_ACCEPTED":
        failures.append("acceptance_packet_status_wrong")
    if handoff.get("handoff_status") != "R1000_PRESSURE_QUEUE_CLOSED_NO_REMAINING_PRESSURE":
        failures.append("handoff_status_wrong")
    if handoff.get("next_command_goal") is not None:
        failures.append("handoff_next_not_null")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_next_not_null")

    if report.get("queue_closure_accepted_count") != 1:
        failures.append("queue_closure_accepted_count_wrong")
    if report.get("remaining_pressure_zero_confirmed_count") != 1:
        failures.append("remaining_pressure_zero_count_wrong")
    if report.get("resolved_counts_match_totals_count") != 1:
        failures.append("resolved_counts_match_totals_count_wrong")
    if report.get("next_candidate_absent_count") != 1:
        failures.append("next_candidate_absent_count_wrong")

    for key in [
        "inspection_authorized_in_this_unit_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "selected_group_inspected_count",
        "selected_group_rows_materialized_count",
        "selected_group_rows_inspected_count",
        "queue_reconciled_count",
        "queue_reopened_count",
        "next_group_candidate_emitted_count",
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

    if report.get("remaining_open_group_count") != 0:
        failures.append("remaining_open_group_count_not_zero")
    if report.get("remaining_open_row_count") != 0:
        failures.append("remaining_open_row_count_not_zero")
    if report.get("resolved_group_count") != report.get("total_group_count"):
        failures.append("resolved_group_count_not_total")
    if report.get("resolved_row_count") != report.get("total_pressure_row_count"):
        failures.append("resolved_row_count_not_total")
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
    for key in [
        "expected_limit_mark_receipt_consumed_count",
        "final_queue_state_consumed_count",
        "queue_closure_artifact_consumed_count",
        "closure_review_surface_materialized_count",
        "closure_review_completed_count",
        "queue_closure_accepted_count",
        "closed_queue_handoff_emitted_count",
        "remaining_pressure_zero_confirmed_count",
        "resolved_counts_match_totals_count",
        "next_candidate_absent_count",
    ]:
        if metrics.get(key) != 1:
            failures.append(f"metric_not_one:{key}:{metrics.get(key)}")

    for key in [
        "inspection_authorized_in_this_unit_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "selected_group_inspected_count",
        "selected_group_rows_materialized_count",
        "selected_group_rows_inspected_count",
        "queue_reconciled_count",
        "queue_reopened_count",
        "next_group_candidate_emitted_count",
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

    if metrics.get("recommended_next_handling") is not None:
        failures.append("recommended_next_handling_not_null")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_R1000_PRESSURE_QUEUE_CLOSURE_REVIEW_COMPLETE_QUEUE_CLOSED":
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

    surface = build_review_surface(sources)
    decision = build_decision(surface)
    acceptance = build_acceptance_packet(surface, decision)
    handoff = build_handoff(surface, decision)
    trace = build_transition_trace(decision)
    report = build_report(surface, decision)

    write_json(CLOSURE_REVIEW_SURFACE_PATH, surface)
    write_json(CLOSURE_REVIEW_DECISION_PATH, decision)
    write_json(CLOSURE_ACCEPTANCE_PACKET_PATH, acceptance)
    write_json(FINAL_CLOSURE_HANDBACK_PATH, handoff)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(surface, decision, acceptance, handoff, trace, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "QUEUE_CLOSURE_REVIEW_0_MARK_RECEIPT_CONSUMED": sources["expected_limit_mark_receipt"]["receipt_id"] == SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID and sources["expected_limit_mark_receipt"]["gate"] == "PASS",
        "QUEUE_CLOSURE_REVIEW_1_FINAL_QUEUE_STATE_CONSUMED": sources["final_queue_state"]["queue_state_status"] == "R1000_PRESSURE_QUEUE_CLOSED",
        "QUEUE_CLOSURE_REVIEW_2_QUEUE_CLOSED": surface["queue_closed"] is True and decision["queue_closure_accepted"] is True,
        "QUEUE_CLOSURE_REVIEW_3_REMAINING_PRESSURE_ZERO": surface["remaining_open_group_count"] == 0 and surface["remaining_open_row_count"] == 0,
        "QUEUE_CLOSURE_REVIEW_4_RESOLVED_COUNTS_MATCH_TOTALS": surface["resolved_group_count"] == surface["total_group_count"] and surface["resolved_row_count"] == surface["total_pressure_row_count"],
        "QUEUE_CLOSURE_REVIEW_5_NEXT_CANDIDATE_ABSENT": surface["next_selectable_group_candidate"] is None,
        "QUEUE_CLOSURE_REVIEW_6_NO_IDENTITY_ASSIGNMENT_OR_INVENTION": report["identity_assignment_count"] == 0 and report["field_value_invention_count"] == 0,
        "QUEUE_CLOSURE_REVIEW_7_NO_ROW_PAYLOAD_OR_R1000": report["selected_group_rows_materialized_count"] == 0 and report["r1000_run_executed_count"] == 0,
        "QUEUE_CLOSURE_REVIEW_8_NO_REPAIR_FIELD_VALUE_OR_TAXONOMY": report["repair_executed_count"] == 0 and report["target_field_filled_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "QUEUE_CLOSURE_REVIEW_9_NO_REOPEN_NEXT_OR_RECONCILE": report["queue_reopened_count"] == 0 and report["next_group_candidate_emitted_count"] == 0 and report["next_group_auto_opened_count"] == 0 and report["queue_reconciled_count"] == 0,
        "QUEUE_CLOSURE_REVIEW_10_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "QUEUE_CLOSURE_REVIEW_11_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "source_synthetic_remainder_source_audit_receipt_id": SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID,
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
        "expected_limit_mark_receipt_consumed": True,
        "final_queue_state_consumed": True,
        "queue_closure_artifact_consumed": True,
        "closure_review_completed": True,
        "queue_closure_accepted": True,
        "queue_closed": True,
        "remaining_pressure_zero": True,
        "resolved_counts_match_totals": True,
        "next_candidate_absent": True,
        "inspection_authorized_in_this_unit": False,
        "identity_assignment": False,
        "field_value_invention": False,
        "selected_group_inspected": False,
        "selected_group_rows_materialized": False,
        "selected_group_rows_inspected": False,
        "queue_reconciled": False,
        "queue_reopened": False,
        "next_group_candidate_emitted": False,
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
        "source_mark_receipt": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "queue_closed": True,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "closure_review_surface": rel(CLOSURE_REVIEW_SURFACE_PATH),
        "closure_review_decision": rel(CLOSURE_REVIEW_DECISION_PATH),
        "closure_acceptance_packet": rel(CLOSURE_ACCEPTANCE_PACKET_PATH),
        "closed_queue_handoff": rel(FINAL_CLOSURE_HANDBACK_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_receipt_v0",
        "receipt_type": "R1000_PRESSURE_QUEUE_CLOSURE_REVIEW_AFTER_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "source_synthetic_remainder_source_audit_receipt_id": SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID,
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
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "pressure_queue_closure_review_summary": {
            "review_result": "ACCEPT_R1000_PRESSURE_QUEUE_CLOSURE",
            "queue_closed": True,
            "total_group_count": surface["total_group_count"],
            "total_pressure_row_count": surface["total_pressure_row_count"],
            "resolved_group_count": surface["resolved_group_count"],
            "resolved_row_count": surface["resolved_row_count"],
            "remaining_open_group_count": 0,
            "remaining_open_row_count": 0,
            "next_selectable_group_candidate": None,
            "recommended_next_handling": None,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "pressure_queue_closure_review_guards": guards,
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
    print(f"pressure_queue_closure_review_receipt_id={receipt_id}")
    print(f"pressure_queue_closure_review_receipt_path=data/r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0_receipts/{receipt_id}.json")
    print(f"closed_queue_handoff_path=data/r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0/r1000_pressure_queue_closed_handoff_after_synthetic_remainder_expected_limit.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
