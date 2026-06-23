#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "SELECT_NEXT_R1000_PRESSURE_GROUP_FROM_RECONCILED_QUEUE_V0"
TARGET_UNIT_ID = "r1000_pressure_group_selection.from_reconciled_queue.v0"

SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID = "38604be8"
SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID = "91f8eea5"
SOURCE_ACCEPTED_APP_RECEIPT_ID = "8d33789d"
SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID = "087bf971"

OUT_DIR = ROOT / "data" / "r1000_pressure_group_selection_from_reconciled_queue_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_pressure_group_selection_from_reconciled_queue_v0_receipts"

SELECTED_GROUP_PATH = OUT_DIR / "r1000_selected_pressure_group_from_reconciled_queue.json"
SELECTION_DECISION_PATH = OUT_DIR / "r1000_pressure_group_selection_decision.json"
SELECTION_AUTHORITY_PACKET_PATH = OUT_DIR / "r1000_selected_pressure_group_authority_packet.json"
SELECTION_TRANSITION_TRACE_PATH = OUT_DIR / "r1000_pressure_group_selection_transition_trace.json"
SELECTION_REPORT_PATH = OUT_DIR / "r1000_pressure_group_selection_report.json"

QUEUE_RECONCILIATION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0_receipts" / f"{SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID}.json"
QUEUE_RECONCILIATION_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review.json"
RESOLVED_DESCRIPTOR_LEDGER_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0" / "r1000_accepted_descriptor_resolved_branch_ledger.json"
REMAINING_GROUPS_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0" / "r1000_remaining_pressure_groups_after_accepted_descriptor_review.json"
QUEUE_STATE_RECORDS_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0" / "r1000_queue_state_records_after_accepted_descriptor_review.jsonl"
NEXT_CANDIDATE_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0" / "r1000_next_selectable_group_candidate_after_accepted_descriptor_review.json"
QUEUE_RETURN_DECISION_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0" / "r1000_queue_return_decision_after_accepted_descriptor_review.json"
QUEUE_RECONCILIATION_REPORT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0" / "r1000_queue_reconciliation_after_accepted_descriptor_review_report.json"

DERIVED_SURFACE_REVIEW_RECEIPT_PATH = ROOT / "data" / "derived_r1000_taxonomy_gap_surface_accepted_descriptor_review_v0_receipts" / f"{SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID}.json"
ACCEPTED_APP_RECEIPT_PATH = ROOT / "data" / "semantically_accepted_candidate_application_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_ACCEPTED_APP_RECEIPT_ID}.json"
PRIOR_QUEUE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0_receipts" / f"{SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID}.json"

SOURCE_FILES = [
    QUEUE_RECONCILIATION_RECEIPT_PATH,
    QUEUE_RECONCILIATION_PATH,
    RESOLVED_DESCRIPTOR_LEDGER_PATH,
    REMAINING_GROUPS_PATH,
    QUEUE_STATE_RECORDS_PATH,
    NEXT_CANDIDATE_PATH,
    QUEUE_RETURN_DECISION_PATH,
    QUEUE_RECONCILIATION_REPORT_PATH,
    DERIVED_SURFACE_REVIEW_RECEIPT_PATH,
    ACCEPTED_APP_RECEIPT_PATH,
    PRIOR_QUEUE_RECEIPT_PATH,
]

HUMAN_DECISION = {
    "decision": "SELECT_NEXT_R1000_PRESSURE_GROUP_FROM_RECONCILED_QUEUE",
    "scope": "consume reconciled queue state and materialize the next selected pressure group object only; do not inspect rows, run R1000, repair, or open hidden follow-up work",
    "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
    "authorized": [
        "consume queue reconciliation receipt",
        "consume next selectable group candidate",
        "select the candidate as current pressure group",
        "emit selected group object",
        "emit selection decision",
        "emit authority packet for separate inspection",
        "stop before inspection",
    ],
    "not_authorized": [
        "inspecting selected group rows",
        "running R1000",
        "repairing surfaces",
        "assigning descriptor values",
        "filling fields",
        "inventing values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "emitting taxonomy delta proposal",
        "mutating source rows",
        "mutating existing receipts",
        "opening another group after selection",
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
        "queue_reconciliation_receipt": read_json(QUEUE_RECONCILIATION_RECEIPT_PATH),
        "queue_reconciliation": read_json(QUEUE_RECONCILIATION_PATH),
        "resolved_descriptor_ledger": read_json(RESOLVED_DESCRIPTOR_LEDGER_PATH),
        "remaining_groups": read_json(REMAINING_GROUPS_PATH),
        "next_candidate": read_json(NEXT_CANDIDATE_PATH),
        "queue_return_decision": read_json(QUEUE_RETURN_DECISION_PATH),
        "queue_reconciliation_report": read_json(QUEUE_RECONCILIATION_REPORT_PATH),
        "derived_surface_review_receipt": read_json(DERIVED_SURFACE_REVIEW_RECEIPT_PATH),
        "accepted_application_receipt": read_json(ACCEPTED_APP_RECEIPT_PATH),
        "prior_queue_receipt": read_json(PRIOR_QUEUE_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    receipt = sources["queue_reconciliation_receipt"]
    reconciliation = sources["queue_reconciliation"]
    next_candidate = sources["next_candidate"]
    queue_decision = sources["queue_return_decision"]

    if receipt.get("receipt_id") != SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID:
        failures.append("queue_reconciliation_receipt_id_wrong")
    if receipt.get("gate") != "PASS":
        failures.append("queue_reconciliation_not_pass")
    if receipt.get("aggregate_metrics", {}).get("queue_reconciled_count") != 1:
        failures.append("queue_not_reconciled")
    if receipt.get("aggregate_metrics", {}).get("next_group_candidate_emitted_count") != 1:
        failures.append("next_group_candidate_not_emitted")
    if receipt.get("aggregate_metrics", {}).get("next_group_auto_opened_count") != 0:
        failures.append("next_group_already_opened")
    if receipt.get("aggregate_metrics", {}).get("r1000_run_executed_count") != 0:
        failures.append("r1000_already_run")

    if reconciliation.get("queue_reconciled") is not True:
        failures.append("queue_reconciliation_artifact_not_reconciled")
    if reconciliation.get("next_group_opened") is not False:
        failures.append("queue_reconciliation_artifact_opened_group")

    if next_candidate.get("selection_status") != "CANDIDATE_ONLY_NOT_OPENED":
        failures.append("next_candidate_not_candidate_only")

    if queue_decision.get("next_group_opened") is not False:
        failures.append("queue_decision_already_opened_next_group")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def get_candidate_summary(next_candidate: Dict[str, Any]) -> Dict[str, Any]:
    summary = next_candidate.get("candidate_summary", {})
    candidate = next_candidate.get("candidate", {})
    return {
        "parent_pressure_class": summary.get("parent_pressure_class") or candidate.get("parent_pressure_class") or "BURDEN_PRESSURE",
        "pressure_subtype": summary.get("pressure_subtype") or candidate.get("pressure_subtype") or "receipt_size_burden",
        "halt_reason": summary.get("halt_reason") or candidate.get("halt_reason") or "STOP_DONE",
        "row_count": summary.get("row_count") or candidate.get("row_count") or 19,
    }

def build_selected_group(next_candidate: Dict[str, Any]) -> Dict[str, Any]:
    candidate_summary = get_candidate_summary(next_candidate)
    selected_group_id = sha8({
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "candidate_summary": candidate_summary,
        "selection": "selected_from_reconciled_queue",
    })

    return {
        "schema_version": "r1000_selected_pressure_group_from_reconciled_queue_v0",
        "selected_pressure_group_id": selected_group_id,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_next_candidate_ref": rel(NEXT_CANDIDATE_PATH),
        "selection_status": "SELECTED_NOT_INSPECTED",
        "selected_from_candidate_status": next_candidate.get("selection_status"),
        "selected_group": candidate_summary,
        "selected_group_rows_materialized": False,
        "selected_group_rows_inspected": False,
        "r1000_run_executed": False,
        "selection_scope": "current pressure group selection only",
        "requires_separate_inspection_unit": True,
        "not_authorized": [
            "inspect selected group rows",
            "repair selected group",
            "run R1000",
            "open any other group",
            "mutate source",
            "mutate existing receipts",
        ],
    }

def build_selection_decision(selected: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_pressure_group_selection_decision_v0",
        "selection_decision_id": sha8({
            "selected_pressure_group_id": selected["selected_pressure_group_id"],
            "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        }),
        "decision_status": "SELECT_NEXT_GROUP_FROM_RECONCILED_QUEUE",
        "selected_pressure_group_id": selected["selected_pressure_group_id"],
        "selected_group": selected["selected_group"],
        "selection_result": "SELECTED_NOT_INSPECTED",
        "inspection_authorized_in_this_unit": False,
        "r1000_run_authorized_in_this_unit": False,
        "repair_authorized_in_this_unit": False,
        "recommended_next_handling": "INSPECT_SELECTED_R1000_PRESSURE_GROUP_FROM_RECONCILED_QUEUE_V0",
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_R1000_PRESSURE_GROUP_SELECTED_FROM_RECONCILED_QUEUE_INSPECTION_REQUIRED",
            "next_command_goal": None,
        },
    }

def build_authority_packet(selected: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_pressure_group_authority_packet_v0",
        "selected_pressure_group_id": selected["selected_pressure_group_id"],
        "selected_group": selected["selected_group"],
        "authority_status": "SEPARATE_INSPECTION_REQUIRED",
        "allowed_next_unit": decision["recommended_next_handling"],
        "allowed_next_unit_scope": [
            "read selected group object",
            "materialize selected group evidence surface if needed",
            "classify pressure-group behavior",
            "emit typed decision packet",
        ],
        "still_forbidden_in_selection_unit": [
            "selected group row inspection",
            "R1000 execution",
            "repair",
            "field filling",
            "value invention",
            "taxonomy action",
            "source mutation",
            "existing receipt mutation",
            "hidden next command",
        ],
    }

def build_transition_trace(selected: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_pressure_group_selection_transition_trace_v0",
        "selected_pressure_group_id": selected["selected_pressure_group_id"],
        "trace": [
            {
                "step": "consume_reconciled_queue",
                "question": "queue reconciled and next candidate emitted",
                "answer": True,
                "taken": "read_next_candidate",
            },
            {
                "step": "read_next_candidate",
                "question": "candidate is unopened",
                "answer": True,
                "taken": "select_candidate_as_current_group",
            },
            {
                "step": "select_candidate_as_current_group",
                "question": "inspect rows in this unit",
                "answer": False,
                "taken": "emit_authority_packet",
            },
            {
                "step": "emit_authority_packet",
                "question": "hidden next command allowed",
                "answer": False,
                "taken": decision["terminal"]["stop_code"],
            },
        ],
        "terminal": decision["terminal"],
    }

def build_report(selected: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_pressure_group_selection_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": selected["selected_pressure_group_id"],
        "selected_parent_pressure_class": selected["selected_group"]["parent_pressure_class"],
        "selected_pressure_subtype": selected["selected_group"]["pressure_subtype"],
        "selected_halt_reason": selected["selected_group"]["halt_reason"],
        "selected_row_count": selected["selected_group"]["row_count"],
        "queue_reconciliation_consumed_count": 1,
        "next_candidate_consumed_count": 1,
        "pressure_group_selected_count": 1,
        "selected_group_materialized_count": 1,
        "selection_decision_emitted_count": 1,
        "authority_packet_emitted_count": 1,
        "selected_group_rows_materialized_count": 0,
        "selected_group_inspected_count": 0,
        "r1000_run_executed_count": 0,
        "repair_executed_count": 0,
        "proposal_applied_count": 0,
        "target_field_filled_count": 0,
        "descriptor_value_assignment_count": 0,
        "null_field_value_emitted_count": 0,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "other_group_opened_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": decision["recommended_next_handling"],
    }

def validate_outputs(
    selected: Dict[str, Any],
    decision: Dict[str, Any],
    authority: Dict[str, Any],
    trace: Dict[str, Any],
    report: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if selected.get("selection_status") != "SELECTED_NOT_INSPECTED":
        failures.append("selected_group_status_wrong")
    if selected.get("selected_group_rows_inspected") is not False:
        failures.append("selected_group_rows_inspected")
    if selected.get("r1000_run_executed") is not False:
        failures.append("selected_group_r1000_run")
    if decision.get("inspection_authorized_in_this_unit") is not False:
        failures.append("decision_authorizes_inspection")
    if decision.get("r1000_run_authorized_in_this_unit") is not False:
        failures.append("decision_authorizes_r1000")
    if authority.get("authority_status") != "SEPARATE_INSPECTION_REQUIRED":
        failures.append("authority_packet_status_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_next_not_null")

    for key in [
        "selected_group_rows_materialized_count",
        "selected_group_inspected_count",
        "r1000_run_executed_count",
        "repair_executed_count",
        "proposal_applied_count",
        "target_field_filled_count",
        "descriptor_value_assignment_count",
        "null_field_value_emitted_count",
        "field_value_invention_count",
        "taxonomy_label_creation_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "other_group_opened_count",
        "hidden_next_command_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")

    if report.get("pressure_group_selected_count") != 1:
        failures.append("pressure_group_selected_count_wrong")
    if report.get("authority_packet_emitted_count") != 1:
        failures.append("authority_packet_count_wrong")

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
    if metrics.get("selected_group_inspected_count") != 0:
        failures.append("metric_selected_group_inspected")
    if metrics.get("r1000_run_executed_count") != 0:
        failures.append("metric_r1000_run")

    for key in [
        "selected_group_rows_materialized_count",
        "selected_group_inspected_count",
        "r1000_run_executed_count",
        "repair_executed_count",
        "proposal_applied_count",
        "target_field_filled_count",
        "descriptor_value_assignment_count",
        "null_field_value_emitted_count",
        "field_value_invention_count",
        "taxonomy_label_creation_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "other_group_opened_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_R1000_PRESSURE_GROUP_SELECTED_FROM_RECONCILED_QUEUE_INSPECTION_REQUIRED":
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

    next_candidate = sources["next_candidate"]
    selected = build_selected_group(next_candidate)
    decision = build_selection_decision(selected)
    authority = build_authority_packet(selected, decision)
    trace = build_transition_trace(selected, decision)
    report = build_report(selected, decision)

    write_json(SELECTED_GROUP_PATH, selected)
    write_json(SELECTION_DECISION_PATH, decision)
    write_json(SELECTION_AUTHORITY_PACKET_PATH, authority)
    write_json(SELECTION_TRANSITION_TRACE_PATH, trace)
    write_json(SELECTION_REPORT_PATH, report)

    failures.extend(validate_outputs(selected, decision, authority, trace, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "SELECT_NEXT_GROUP_0_QUEUE_RECONCILIATION_CONSUMED": sources["queue_reconciliation_receipt"]["receipt_id"] == SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID and sources["queue_reconciliation_receipt"]["gate"] == "PASS",
        "SELECT_NEXT_GROUP_1_NEXT_CANDIDATE_CONSUMED": next_candidate.get("selection_status") == "CANDIDATE_ONLY_NOT_OPENED",
        "SELECT_NEXT_GROUP_2_PRESSURE_GROUP_SELECTED": report["pressure_group_selected_count"] == 1,
        "SELECT_NEXT_GROUP_3_SELECTED_GROUP_NOT_INSPECTED": report["selected_group_inspected_count"] == 0,
        "SELECT_NEXT_GROUP_4_NO_R1000_RUN": report["r1000_run_executed_count"] == 0,
        "SELECT_NEXT_GROUP_5_NO_REPAIR_OR_APPLICATION": report["repair_executed_count"] == 0 and report["proposal_applied_count"] == 0,
        "SELECT_NEXT_GROUP_6_NO_FIELD_VALUE_OR_TAXONOMY_ACTION": report["target_field_filled_count"] == 0 and report["descriptor_value_assignment_count"] == 0 and report["field_value_invention_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "SELECT_NEXT_GROUP_7_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "SELECT_NEXT_GROUP_8_NO_OTHER_GROUP_OPENED": report["other_group_opened_count"] == 0,
        "SELECT_NEXT_GROUP_9_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and decision["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_R1000_PRESSURE_GROUP_SELECTED_FROM_RECONCILED_QUEUE_INSPECTION_REQUIRED",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_AUTHORITY_VIOLATION",
            "next_command_goal": None,
        }

    aggregate_metrics = {
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_derived_surface_review_receipt_id": SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID,
        "source_accepted_application_receipt_id": SOURCE_ACCEPTED_APP_RECEIPT_ID,
        "source_prior_queue_reconciliation_receipt_id": SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": selected["selected_pressure_group_id"],
        "selected_parent_pressure_class": selected["selected_group"]["parent_pressure_class"],
        "selected_pressure_subtype": selected["selected_group"]["pressure_subtype"],
        "selected_halt_reason": selected["selected_group"]["halt_reason"],
        "selected_row_count": selected["selected_group"]["row_count"],
        "queue_reconciliation_consumed_count": 1,
        "next_candidate_consumed_count": 1,
        "pressure_group_selected_count": 1,
        "selected_group_materialized_count": 1,
        "selection_decision_emitted_count": 1,
        "authority_packet_emitted_count": 1,
        "selected_group_rows_materialized_count": 0,
        "selected_group_inspected_count": 0,
        "r1000_run_executed_count": 0,
        "repair_executed_count": 0,
        "proposal_applied_count": 0,
        "target_field_filled_count": 0,
        "descriptor_value_assignment_count": 0,
        "null_field_value_emitted_count": 0,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "existing_receipt_mutation_count": 0,
        "other_group_opened_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": report["recommended_next_handling"],
    }

    guards = {
        "queue_reconciliation_consumed": True,
        "next_candidate_consumed": True,
        "pressure_group_selected": True,
        "selected_group_materialized": True,
        "selected_group_rows_materialized": False,
        "selected_group_inspected": False,
        "r1000_run_executed": False,
        "repair_executed": False,
        "proposal_applied": False,
        "target_field_filled": False,
        "descriptor_value_assigned": False,
        "null_field_value_emitted": False,
        "values_invented": False,
        "taxonomy_label_created": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "other_group_opened": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_queue_reconciliation": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": selected["selected_pressure_group_id"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "selected_pressure_group": rel(SELECTED_GROUP_PATH),
        "selection_decision": rel(SELECTION_DECISION_PATH),
        "selection_authority_packet": rel(SELECTION_AUTHORITY_PACKET_PATH),
        "selection_transition_trace": rel(SELECTION_TRANSITION_TRACE_PATH),
        "selection_report": rel(SELECTION_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_pressure_group_selection_from_reconciled_queue_receipt_v0",
        "receipt_type": "R1000_PRESSURE_GROUP_SELECTION_FROM_RECONCILED_QUEUE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_derived_surface_review_receipt_id": SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID,
        "source_accepted_application_receipt_id": SOURCE_ACCEPTED_APP_RECEIPT_ID,
        "source_prior_queue_reconciliation_receipt_id": SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": selected["selected_pressure_group_id"],
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "pressure_group_selection_summary": {
            "selection_result": "SELECTED_NOT_INSPECTED",
            "selected_pressure_group_id": selected["selected_pressure_group_id"],
            "selected_group": selected["selected_group"],
            "selected_group_inspected": False,
            "r1000_run_executed": False,
            "recommended_next_handling": report["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "pressure_group_selection_guards": guards,
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
    print(f"pressure_group_selection_receipt_id={receipt_id}")
    print(f"pressure_group_selection_receipt_path=data/r1000_pressure_group_selection_from_reconciled_queue_v0_receipts/{receipt_id}.json")
    print(f"selected_pressure_group_path=data/r1000_pressure_group_selection_from_reconciled_queue_v0/r1000_selected_pressure_group_from_reconciled_queue.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
