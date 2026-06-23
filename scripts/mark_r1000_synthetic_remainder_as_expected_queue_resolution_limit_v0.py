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

UNIT_ID = "MARK_R1000_SYNTHETIC_REMAINDER_AS_EXPECTED_QUEUE_RESOLUTION_LIMIT_V0"
TARGET_UNIT_ID = "r1000_synthetic_remainder.expected_queue_resolution_limit_mark.v0"

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

OUT_DIR = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0_receipts"

MARK_DECISION_PATH = OUT_DIR / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_decision.json"
MARKED_LIMIT_PATH = OUT_DIR / "r1000_synthetic_remainder_marked_expected_queue_resolution_limit.json"
QUEUE_CLOSURE_PATH = OUT_DIR / "r1000_pressure_queue_closure_after_synthetic_remainder_expected_limit.json"
RESOLUTION_LEDGER_PATH = OUT_DIR / "r1000_synthetic_remainder_expected_limit_resolution_ledger.json"
FINAL_QUEUE_STATE_PATH = OUT_DIR / "r1000_final_pressure_queue_state_after_synthetic_remainder_expected_limit.json"
INSPECTION_BLOCK_FINAL_PACKET_PATH = OUT_DIR / "r1000_synthetic_remainder_final_inspection_block_packet_after_expected_limit.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_synthetic_remainder_expected_limit_mark_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_synthetic_remainder_expected_limit_mark_report.json"

SOURCE_AUDIT_RECEIPT_PATH = ROOT / "data" / "r1000_synthetic_remainder_source_evidence_audit_after_repaired_burden_queue_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID}.json"
AUDIT_SURFACE_PATH = ROOT / "data" / "r1000_synthetic_remainder_source_evidence_audit_after_repaired_burden_queue_v0" / "r1000_synthetic_remainder_source_evidence_audit_surface_after_repaired_burden_queue.json"
EVIDENCE_CANDIDATES_PATH = ROOT / "data" / "r1000_synthetic_remainder_source_evidence_audit_after_repaired_burden_queue_v0" / "r1000_synthetic_remainder_source_evidence_candidates_after_repaired_burden_queue.json"
AUDIT_DECISION_PATH = ROOT / "data" / "r1000_synthetic_remainder_source_evidence_audit_after_repaired_burden_queue_v0" / "r1000_synthetic_remainder_source_evidence_audit_decision_after_repaired_burden_queue.json"
EXPECTED_LIMIT_PACKET_PATH = ROOT / "data" / "r1000_synthetic_remainder_source_evidence_audit_after_repaired_burden_queue_v0" / "r1000_synthetic_remainder_expected_queue_resolution_limit_packet_after_repaired_burden_queue.json"
QUEUE_CLOSURE_CANDIDATE_PACKET_PATH = ROOT / "data" / "r1000_synthetic_remainder_source_evidence_audit_after_repaired_burden_queue_v0" / "r1000_synthetic_remainder_queue_closure_candidate_packet_after_repaired_burden_queue.json"

IDENTITY_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_selected_synthetic_remainder_identity_surface_review_after_repaired_burden_queue_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID}.json"
SELECTION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_repaired_burden_group_queue_reconciliation_v0_receipts" / f"{SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID}.json"
SELECTED_GROUP_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_repaired_burden_group_queue_reconciliation_v0" / "r1000_selected_pressure_group_after_repaired_burden_queue_reconciliation.json"

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
    SOURCE_AUDIT_RECEIPT_PATH,
    AUDIT_SURFACE_PATH,
    EVIDENCE_CANDIDATES_PATH,
    AUDIT_DECISION_PATH,
    EXPECTED_LIMIT_PACKET_PATH,
    QUEUE_CLOSURE_CANDIDATE_PACKET_PATH,
    IDENTITY_REVIEW_RECEIPT_PATH,
    SELECTION_RECEIPT_PATH,
    SELECTED_GROUP_PATH,
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

RECOMMENDED_NEXT_HANDLING = "REVIEW_R1000_PRESSURE_QUEUE_CLOSURE_AFTER_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_V0"

HUMAN_DECISION = {
    "decision": "MARK_R1000_SYNTHETIC_REMAINDER_AS_EXPECTED_QUEUE_RESOLUTION_LIMIT",
    "scope": "consume the source-audit expected-limit candidate and apply a derived expected queue-resolution limit mark to the final synthetic remainder, closing the pressure queue without inspecting rows, running R1000, assigning identity, or mutating prior artifacts",
    "source_synthetic_remainder_source_audit_receipt_id": SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID,
    "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
    "authorized": [
        "consume synthetic remainder source audit receipt",
        "consume expected queue-resolution limit packet",
        "consume queue closure candidate packet",
        "apply expected queue-resolution limit mark in derived artifact only",
        "emit final queue closure artifact",
        "emit resolution ledger",
        "emit final queue state",
        "stop before any further review or new run",
    ],
    "not_authorized": [
        "inspecting selected group row payloads",
        "running R1000",
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
        "source_audit_receipt": read_json(SOURCE_AUDIT_RECEIPT_PATH),
        "audit_surface": read_json(AUDIT_SURFACE_PATH),
        "evidence_candidates": read_json(EVIDENCE_CANDIDATES_PATH),
        "audit_decision": read_json(AUDIT_DECISION_PATH),
        "expected_limit_packet": read_json(EXPECTED_LIMIT_PACKET_PATH),
        "queue_closure_candidate_packet": read_json(QUEUE_CLOSURE_CANDIDATE_PACKET_PATH),
        "identity_review_receipt": read_json(IDENTITY_REVIEW_RECEIPT_PATH),
        "selection_receipt": read_json(SELECTION_RECEIPT_PATH),
        "selected_group": read_json(SELECTED_GROUP_PATH),
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
    receipt = sources["source_audit_receipt"]
    decision = sources["audit_decision"]
    limit_packet = sources["expected_limit_packet"]
    closure_packet = sources["queue_closure_candidate_packet"]
    selected = sources["selected_group"]
    queue_report = sources["repaired_queue_report"]

    if receipt.get("receipt_id") != SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID:
        failures.append("source_audit_receipt_id_wrong")
    if receipt.get("gate") != "PASS":
        failures.append("source_audit_not_pass")
    if receipt.get("selected_pressure_group_id") != SELECTED_PRESSURE_GROUP_ID:
        failures.append("selected_id_wrong_in_source_audit_receipt")
    if receipt.get("aggregate_metrics", {}).get("expected_queue_resolution_limit_candidate_emitted_count") != 1:
        failures.append("expected_limit_candidate_not_emitted")
    if receipt.get("aggregate_metrics", {}).get("expected_limit_closure_applied_count") != 0:
        failures.append("expected_limit_already_applied")
    if receipt.get("aggregate_metrics", {}).get("direct_source_backed_identity_evidence_found_count") != 0:
        failures.append("direct_source_identity_found_unexpectedly")

    if decision.get("decision_status") != "NO_SOURCE_BACKED_IDENTITY_EVIDENCE_FOUND_EXPECTED_QUEUE_RESOLUTION_LIMIT_CANDIDATE":
        failures.append("audit_decision_status_wrong")
    if decision.get("expected_queue_resolution_limit_candidate") is not True:
        failures.append("audit_decision_no_expected_limit_candidate")
    if decision.get("expected_limit_closure_applied_in_this_unit") is not False:
        failures.append("audit_decision_already_applied_closure")

    if limit_packet.get("packet_status") != "EXPECTED_LIMIT_CANDIDATE_NOT_APPLIED":
        failures.append("expected_limit_packet_not_candidate")
    if limit_packet.get("closure_applied") is not False:
        failures.append("expected_limit_packet_already_applied")

    if closure_packet.get("packet_status") != "QUEUE_CLOSURE_CANDIDATE_NOT_APPLIED":
        failures.append("queue_closure_packet_not_candidate")
    if closure_packet.get("closure_application_authorized_in_this_unit") is not False:
        failures.append("prior_unit_authorized_closure_unexpectedly")

    if selected.get("selected_pressure_group_id") != SELECTED_PRESSURE_GROUP_ID:
        failures.append("selected_group_id_wrong")
    if selected.get("candidate_identity_status") != "COUNT_ONLY_SYNTHETIC_REMAINDER":
        failures.append("selected_group_not_synthetic_remainder")

    if queue_report.get("remaining_row_count_after") != 1:
        failures.append("remaining_row_count_after_not_one")
    if queue_report.get("remaining_group_count_after") != 1:
        failures.append("remaining_group_count_after_not_one")

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

def prior_counts(sources: Dict[str, Any]) -> Dict[str, int]:
    report = sources["repaired_queue_report"]
    return {
        "total_group_count": int(report.get("total_group_count", 5)),
        "total_pressure_row_count": int(report.get("total_pressure_row_count", 88)),
        "resolved_group_count_before_mark": int(report.get("resolved_group_count_after", 4)),
        "resolved_row_count_before_mark": int(report.get("resolved_row_count_after", 87)),
        "remaining_group_count_before_mark": int(report.get("remaining_group_count_after", 1)),
        "remaining_row_count_before_mark": int(report.get("remaining_row_count_after", 1)),
    }

def build_mark_decision(sources: Dict[str, Any]) -> Dict[str, Any]:
    selected = selected_summary(sources)
    counts = prior_counts(sources)
    row_count = int(selected.get("row_count", 0) or 0)
    return {
        "schema_version": "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_decision_v0",
        "mark_decision_id": sha8({
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "source_audit_receipt_id": SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID,
            "selected": selected,
        }),
        "decision_status": "APPLY_EXPECTED_QUEUE_RESOLUTION_LIMIT_MARK",
        "source_synthetic_remainder_source_audit_receipt_id": SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_group": selected,
        "preconditions": {
            "source_audit_gate_pass": True,
            "direct_source_backed_identity_evidence_found": False,
            "expected_queue_resolution_limit_candidate": True,
            "prior_remaining_group_count": counts["remaining_group_count_before_mark"],
            "prior_remaining_row_count": counts["remaining_row_count_before_mark"],
        },
        "mark_authorized_in_this_unit": True,
        "inspection_authorized_in_this_unit": False,
        "identity_assignment_authorized": False,
        "source_mutation_authorized": False,
        "expected_limit_closure_applied": True,
        "after_counts": {
            "total_group_count": counts["total_group_count"],
            "total_pressure_row_count": counts["total_pressure_row_count"],
            "resolved_group_count": counts["resolved_group_count_before_mark"] + 1,
            "resolved_row_count": counts["resolved_row_count_before_mark"] + row_count,
            "remaining_open_group_count": 0,
            "remaining_open_row_count": 0,
        },
        "recommended_next_handling": RECOMMENDED_NEXT_HANDLING,
    }

def build_marked_limit(decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_synthetic_remainder_marked_expected_queue_resolution_limit_v0",
        "expected_limit_mark_id": sha8({
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "limit_type": "EXPECTED_QUEUE_RESOLUTION_LIMIT",
            "source_audit_receipt_id": SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID,
        }),
        "source_mark_decision_ref": rel(MARK_DECISION_PATH),
        "source_expected_limit_packet_ref": rel(EXPECTED_LIMIT_PACKET_PATH),
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_group": decision["selected_group"],
        "limit_type": "EXPECTED_QUEUE_RESOLUTION_LIMIT",
        "limit_status": "MARKED_APPLIED_IN_DERIVED_QUEUE_STATE",
        "closure_reason": "final synthetic remainder has no direct source-backed identity and is supported only as a 1-row queue-resolution residue",
        "closure_scope": "derived_queue_state_only",
        "expected_limit_closure_applied": True,
        "inspection_allowed": False,
        "identity_assignment_executed": False,
        "field_value_invention": False,
        "source_mutation": False,
        "existing_receipt_mutation": False,
    }

def build_queue_closure(decision: Dict[str, Any], marked_limit: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_pressure_queue_closure_after_synthetic_remainder_expected_limit_v0",
        "queue_closure_id": sha8({
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "expected_limit_mark_id": marked_limit["expected_limit_mark_id"],
            "after_counts": decision["after_counts"],
        }),
        "source_synthetic_remainder_source_audit_receipt_id": SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID,
        "source_repaired_burden_queue_reconciliation_receipt_id": SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "queue_closure_status": "R1000_PRESSURE_QUEUE_CLOSED_BY_EXPECTED_QUEUE_RESOLUTION_LIMIT",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "closed_group": decision["selected_group"],
        "closed_group_resolution": "EXPECTED_QUEUE_RESOLUTION_LIMIT",
        "expected_limit_mark_ref": rel(MARKED_LIMIT_PATH),
        "prior_counts": {
            "resolved_group_count": decision["preconditions"]["prior_remaining_group_count"],
            "remaining_open_group_count": decision["preconditions"]["prior_remaining_group_count"],
            "remaining_open_row_count": decision["preconditions"]["prior_remaining_row_count"],
        },
        "after_counts": decision["after_counts"],
        "queue_closed": True,
        "remaining_open_group_count": 0,
        "remaining_open_row_count": 0,
        "next_group_candidate_emitted": False,
        "next_group_opened": False,
        "selected_group_inspected": False,
        "r1000_run_executed": False,
    }

def build_resolution_ledger(decision: Dict[str, Any], marked_limit: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_synthetic_remainder_expected_limit_resolution_ledger_v0",
        "source_synthetic_remainder_source_audit_receipt_id": SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID,
        "resolution_entry": {
            "resolution_id": sha8({
                "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
                "resolution": "EXPECTED_QUEUE_RESOLUTION_LIMIT",
                "source_audit_receipt_id": SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID,
            }),
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "selected_group": decision["selected_group"],
            "resolution_status": "SYNTHETIC_REMAINDER_MARKED_EXPECTED_QUEUE_RESOLUTION_LIMIT",
            "resolution_basis": "no direct source-backed identity evidence in fixed explicit audit scope",
            "expected_limit_mark_id": marked_limit["expected_limit_mark_id"],
            "row_count": decision["selected_group"]["row_count"],
        },
        "queue_closure_status": "CLOSED",
        "after_counts": decision["after_counts"],
    }

def build_final_queue_state(decision: Dict[str, Any], queue_closure: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_final_pressure_queue_state_after_synthetic_remainder_expected_limit_v0",
        "source_queue_closure_ref": rel(QUEUE_CLOSURE_PATH),
        "source_mark_decision_ref": rel(MARK_DECISION_PATH),
        "queue_state_status": "R1000_PRESSURE_QUEUE_CLOSED",
        "total_group_count": decision["after_counts"]["total_group_count"],
        "total_pressure_row_count": decision["after_counts"]["total_pressure_row_count"],
        "resolved_group_count": decision["after_counts"]["resolved_group_count"],
        "resolved_row_count": decision["after_counts"]["resolved_row_count"],
        "remaining_open_group_count": decision["after_counts"]["remaining_open_group_count"],
        "remaining_open_row_count": decision["after_counts"]["remaining_open_row_count"],
        "queue_closed": True,
        "closure_reason": "all pressure rows accounted for after expected queue-resolution limit mark",
        "last_closed_group": decision["selected_group"],
        "last_closed_group_resolution": "EXPECTED_QUEUE_RESOLUTION_LIMIT",
        "next_selectable_group_candidate": None,
        "next_group_opened": False,
    }

def build_inspection_block_final_packet(decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_synthetic_remainder_final_inspection_block_packet_after_expected_limit_v0",
        "packet_status": "FINAL_INSPECTION_BLOCK_CONFIRMED_EXPECTED_LIMIT_CLOSED",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_group": decision["selected_group"],
        "inspection_allowed": False,
        "identity_assignment_allowed": False,
        "row_payload_materialization_allowed": False,
        "r1000_run_allowed": False,
        "reason": "synthetic remainder was closed as expected queue-resolution limit, not converted into an inspectable source-backed pressure group",
    }

def build_transition_trace(decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_synthetic_remainder_expected_limit_mark_transition_trace_v0",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "trace": [
            {
                "step": "consume_source_audit_expected_limit_candidate",
                "question": "expected queue-resolution limit candidate exists and is not applied",
                "answer": True,
                "taken": "apply_derived_expected_limit_mark",
            },
            {
                "step": "apply_derived_expected_limit_mark",
                "question": "mutate prior source artifacts or receipts",
                "answer": False,
                "taken": "emit_final_queue_state",
            },
            {
                "step": "emit_final_queue_state",
                "question": "remaining pressure rows after mark",
                "answer": decision["after_counts"]["remaining_open_row_count"],
                "taken": "close_queue",
            },
            {
                "step": "close_queue",
                "question": "hidden next command allowed",
                "answer": False,
                "taken": "STOP_SYNTHETIC_REMAINDER_MARKED_EXPECTED_QUEUE_RESOLUTION_LIMIT_QUEUE_CLOSED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_SYNTHETIC_REMAINDER_MARKED_EXPECTED_QUEUE_RESOLUTION_LIMIT_QUEUE_CLOSED",
            "next_command_goal": None,
        },
    }

def build_report(decision: Dict[str, Any], marked_limit: Dict[str, Any]) -> Dict[str, Any]:
    group = decision["selected_group"]
    before_resolved_group = decision["after_counts"]["resolved_group_count"] - 1
    before_resolved_row = decision["after_counts"]["resolved_row_count"] - group["row_count"]
    return {
        "schema_version": "r1000_synthetic_remainder_expected_limit_mark_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_synthetic_remainder_source_audit_receipt_id": SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID,
        "source_synthetic_remainder_identity_review_receipt_id": SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID,
        "source_selection_after_repaired_burden_queue_receipt_id": SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID,
        "source_repaired_burden_queue_reconciliation_receipt_id": SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_parent_pressure_class": group.get("parent_pressure_class"),
        "selected_pressure_subtype": group.get("pressure_subtype"),
        "selected_halt_reason": group.get("halt_reason"),
        "selected_row_count": group.get("row_count"),
        "source_audit_receipt_consumed_count": 1,
        "expected_limit_packet_consumed_count": 1,
        "queue_closure_candidate_packet_consumed_count": 1,
        "expected_limit_mark_decision_emitted_count": 1,
        "expected_limit_mark_applied_count": 1,
        "expected_limit_closure_applied_count": 1,
        "marked_expected_limit_artifact_emitted_count": 1,
        "queue_closure_artifact_emitted_count": 1,
        "resolution_ledger_emitted_count": 1,
        "final_queue_state_emitted_count": 1,
        "inspection_block_final_packet_emitted_count": 1,
        "queue_closed_count": 1,
        "resolved_group_count_before": before_resolved_group,
        "resolved_group_count_after": decision["after_counts"]["resolved_group_count"],
        "resolved_group_delta": 1,
        "resolved_row_count_before": before_resolved_row,
        "resolved_row_count_after": decision["after_counts"]["resolved_row_count"],
        "resolved_row_delta": group["row_count"],
        "remaining_group_count_before": 1,
        "remaining_group_count_after": 0,
        "remaining_group_delta": -1,
        "remaining_row_count_before": group["row_count"],
        "remaining_row_count_after": 0,
        "remaining_row_delta": -group["row_count"],
        "total_group_count": decision["after_counts"]["total_group_count"],
        "total_pressure_row_count": decision["after_counts"]["total_pressure_row_count"],
        "inspection_authorized_in_this_unit_count": 0,
        "identity_assignment_count": 0,
        "field_value_invention_count": 0,
        "selected_group_inspected_count": 0,
        "selected_group_rows_materialized_count": 0,
        "selected_group_rows_inspected_count": 0,
        "queue_reconciled_count": 0,
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
        "recommended_next_handling": RECOMMENDED_NEXT_HANDLING,
    }

def validate_outputs(
    decision: Dict[str, Any],
    marked_limit: Dict[str, Any],
    queue_closure: Dict[str, Any],
    ledger: Dict[str, Any],
    final_state: Dict[str, Any],
    block_packet: Dict[str, Any],
    trace: Dict[str, Any],
    report: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if decision.get("decision_status") != "APPLY_EXPECTED_QUEUE_RESOLUTION_LIMIT_MARK":
        failures.append("decision_status_wrong")
    if decision.get("expected_limit_closure_applied") is not True:
        failures.append("decision_did_not_apply_expected_limit")
    if marked_limit.get("limit_status") != "MARKED_APPLIED_IN_DERIVED_QUEUE_STATE":
        failures.append("marked_limit_status_wrong")
    if marked_limit.get("expected_limit_closure_applied") is not True:
        failures.append("marked_limit_not_applied")
    if marked_limit.get("source_mutation") is not False:
        failures.append("marked_limit_source_mutation")
    if queue_closure.get("queue_closure_status") != "R1000_PRESSURE_QUEUE_CLOSED_BY_EXPECTED_QUEUE_RESOLUTION_LIMIT":
        failures.append("queue_closure_status_wrong")
    if queue_closure.get("queue_closed") is not True:
        failures.append("queue_not_closed")
    if final_state.get("queue_state_status") != "R1000_PRESSURE_QUEUE_CLOSED":
        failures.append("final_queue_state_status_wrong")
    if final_state.get("remaining_open_group_count") != 0:
        failures.append("final_remaining_group_not_zero")
    if final_state.get("remaining_open_row_count") != 0:
        failures.append("final_remaining_row_not_zero")
    if block_packet.get("packet_status") != "FINAL_INSPECTION_BLOCK_CONFIRMED_EXPECTED_LIMIT_CLOSED":
        failures.append("block_packet_status_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_next_not_null")

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
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")

    if report.get("expected_limit_mark_applied_count") != 1:
        failures.append("expected_limit_mark_applied_count_wrong")
    if report.get("expected_limit_closure_applied_count") != 1:
        failures.append("expected_limit_closure_applied_count_wrong")
    if report.get("queue_closed_count") != 1:
        failures.append("queue_closed_count_wrong")
    if report.get("remaining_group_count_after") != 0:
        failures.append("remaining_group_count_after_wrong")
    if report.get("remaining_row_count_after") != 0:
        failures.append("remaining_row_count_after_wrong")
    if report.get("resolved_group_count_after") != report.get("total_group_count"):
        failures.append("resolved_group_count_not_total")
    if report.get("resolved_row_count_after") != report.get("total_pressure_row_count"):
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
        "expected_limit_mark_applied_count",
        "expected_limit_closure_applied_count",
        "queue_closed_count",
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

    if metrics.get("remaining_group_count_after") != 0:
        failures.append("metric_remaining_group_after_not_zero")
    if metrics.get("remaining_row_count_after") != 0:
        failures.append("metric_remaining_row_after_not_zero")
    if metrics.get("resolved_group_count_after") != metrics.get("total_group_count"):
        failures.append("metric_resolved_group_not_total")
    if metrics.get("resolved_row_count_after") != metrics.get("total_pressure_row_count"):
        failures.append("metric_resolved_row_not_total")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_SYNTHETIC_REMAINDER_MARKED_EXPECTED_QUEUE_RESOLUTION_LIMIT_QUEUE_CLOSED":
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

    decision = build_mark_decision(sources)
    marked_limit = build_marked_limit(decision)
    queue_closure = build_queue_closure(decision, marked_limit)
    ledger = build_resolution_ledger(decision, marked_limit)
    final_state = build_final_queue_state(decision, queue_closure)
    block_packet = build_inspection_block_final_packet(decision)
    trace = build_transition_trace(decision)
    report = build_report(decision, marked_limit)

    write_json(MARK_DECISION_PATH, decision)
    write_json(MARKED_LIMIT_PATH, marked_limit)
    write_json(QUEUE_CLOSURE_PATH, queue_closure)
    write_json(RESOLUTION_LEDGER_PATH, ledger)
    write_json(FINAL_QUEUE_STATE_PATH, final_state)
    write_json(INSPECTION_BLOCK_FINAL_PACKET_PATH, block_packet)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(decision, marked_limit, queue_closure, ledger, final_state, block_packet, trace, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "EXPECTED_LIMIT_MARK_0_SOURCE_AUDIT_RECEIPT_CONSUMED": sources["source_audit_receipt"]["receipt_id"] == SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID and sources["source_audit_receipt"]["gate"] == "PASS",
        "EXPECTED_LIMIT_MARK_1_EXPECTED_LIMIT_CANDIDATE_CONSUMED": sources["expected_limit_packet"]["packet_status"] == "EXPECTED_LIMIT_CANDIDATE_NOT_APPLIED",
        "EXPECTED_LIMIT_MARK_2_QUEUE_CLOSURE_CANDIDATE_CONSUMED": sources["queue_closure_candidate_packet"]["packet_status"] == "QUEUE_CLOSURE_CANDIDATE_NOT_APPLIED",
        "EXPECTED_LIMIT_MARK_3_EXPECTED_LIMIT_MARK_APPLIED": marked_limit["expected_limit_closure_applied"] is True and report["expected_limit_mark_applied_count"] == 1,
        "EXPECTED_LIMIT_MARK_4_QUEUE_CLOSED": final_state["queue_closed"] is True and report["queue_closed_count"] == 1,
        "EXPECTED_LIMIT_MARK_5_NO_REMAINING_PRESSURE": final_state["remaining_open_group_count"] == 0 and final_state["remaining_open_row_count"] == 0,
        "EXPECTED_LIMIT_MARK_6_NO_IDENTITY_ASSIGNMENT_OR_INVENTION": report["identity_assignment_count"] == 0 and report["field_value_invention_count"] == 0,
        "EXPECTED_LIMIT_MARK_7_NO_ROW_PAYLOAD_OR_R1000": report["selected_group_rows_materialized_count"] == 0 and report["r1000_run_executed_count"] == 0,
        "EXPECTED_LIMIT_MARK_8_NO_REPAIR_FIELD_VALUE_OR_TAXONOMY": report["repair_executed_count"] == 0 and report["target_field_filled_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "EXPECTED_LIMIT_MARK_9_NO_NEXT_GROUP_OR_QUEUE_RECONCILIATION": report["queue_reconciled_count"] == 0 and report["next_group_candidate_emitted_count"] == 0 and report["next_group_auto_opened_count"] == 0,
        "EXPECTED_LIMIT_MARK_10_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "EXPECTED_LIMIT_MARK_11_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
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
        "source_audit_receipt_consumed": True,
        "expected_limit_candidate_consumed": True,
        "queue_closure_candidate_consumed": True,
        "expected_limit_mark_applied": True,
        "expected_limit_closure_applied": True,
        "queue_closed": True,
        "remaining_pressure_zero": True,
        "inspection_authorized_in_this_unit": False,
        "identity_assignment": False,
        "field_value_invention": False,
        "selected_group_inspected": False,
        "selected_group_rows_materialized": False,
        "selected_group_rows_inspected": False,
        "queue_reconciled": False,
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
        "source_audit_receipt": SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "queue_closed": True,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "mark_decision": rel(MARK_DECISION_PATH),
        "marked_expected_limit": rel(MARKED_LIMIT_PATH),
        "queue_closure": rel(QUEUE_CLOSURE_PATH),
        "resolution_ledger": rel(RESOLUTION_LEDGER_PATH),
        "final_queue_state": rel(FINAL_QUEUE_STATE_PATH),
        "inspection_block_final_packet": rel(INSPECTION_BLOCK_FINAL_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_receipt_v0",
        "receipt_type": "R1000_SYNTHETIC_REMAINDER_EXPECTED_QUEUE_RESOLUTION_LIMIT_MARK_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
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
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "synthetic_remainder_expected_limit_mark_summary": {
            "mark_result": "SYNTHETIC_REMAINDER_MARKED_EXPECTED_QUEUE_RESOLUTION_LIMIT",
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "selected_group": decision["selected_group"],
            "expected_limit_closure_applied": True,
            "queue_closed": True,
            "remaining_open_group_count": 0,
            "remaining_open_row_count": 0,
            "inspection_allowed": False,
            "recommended_next_handling": RECOMMENDED_NEXT_HANDLING,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "synthetic_remainder_expected_limit_mark_guards": guards,
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
    print(f"synthetic_remainder_expected_limit_mark_receipt_id={receipt_id}")
    print(f"synthetic_remainder_expected_limit_mark_receipt_path=data/r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0_receipts/{receipt_id}.json")
    print(f"final_queue_state_after_synthetic_remainder_expected_limit_path=data/r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0/r1000_final_pressure_queue_state_after_synthetic_remainder_expected_limit.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
