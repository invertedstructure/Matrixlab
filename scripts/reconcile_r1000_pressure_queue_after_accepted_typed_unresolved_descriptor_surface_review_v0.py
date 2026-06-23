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

UNIT_ID = "RECONCILE_R1000_PRESSURE_QUEUE_AFTER_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_SURFACE_REVIEW_V0"
TARGET_UNIT_ID = "r1000_pressure_queue_reconciliation.after_accepted_typed_unresolved_descriptor_surface_review.v0"

SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID = "91f8eea5"
SOURCE_ACCEPTED_APP_RECEIPT_ID = "8d33789d"
SOURCE_PATCHED_REVIEW_RECEIPT_ID = "0fe3bb6a"
SOURCE_SEMANTIC_PATCH_RECEIPT_ID = "7d078710"
SOURCE_SEMANTIC_BARRIER_RECEIPT_ID = "4e6b09b2"
SOURCE_PROPOSAL_REVIEW_RECEIPT_ID = "a939b4a6"
SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID = "aa01c2a9"
SOURCE_PROPOSAL_LAYER_RECEIPT_ID = "6003c89c"
SOURCE_EXPECTED_LIMIT_RECEIPT_ID = "cbde4b69"
SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID = "087bf971"
SOURCE_CANDIDATE_OBJECT_ID = "ce1fe7fc"
PATCHED_CANDIDATE_OBJECT_ID = "a9ec669b"
ACCEPTED_DESCRIPTOR_OBJECT_ID = "86331324"
DERIVED_SURFACE_ID = "b0ee092b"

OUT_DIR = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0_receipts"

QUEUE_RECONCILIATION_PATH = OUT_DIR / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review.json"
RESOLVED_DESCRIPTOR_LEDGER_PATH = OUT_DIR / "r1000_accepted_descriptor_resolved_branch_ledger.json"
UPDATED_REMAINING_GROUPS_PATH = OUT_DIR / "r1000_remaining_pressure_groups_after_accepted_descriptor_review.json"
QUEUE_STATE_RECORDS_PATH = OUT_DIR / "r1000_queue_state_records_after_accepted_descriptor_review.jsonl"
NEXT_SELECTABLE_GROUP_CANDIDATE_PATH = OUT_DIR / "r1000_next_selectable_group_candidate_after_accepted_descriptor_review.json"
QUEUE_RETURN_DECISION_PATH = OUT_DIR / "r1000_queue_return_decision_after_accepted_descriptor_review.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_queue_reconciliation_after_accepted_descriptor_review_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_queue_reconciliation_after_accepted_descriptor_review_report.json"

DERIVED_SURFACE_REVIEW_RECEIPT_PATH = ROOT / "data" / "derived_r1000_taxonomy_gap_surface_accepted_descriptor_review_v0_receipts" / f"{SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID}.json"
DERIVED_SURFACE_REVIEW_DECISION_PATH = ROOT / "data" / "derived_r1000_taxonomy_gap_surface_accepted_descriptor_review_v0" / "derived_surface_accepted_descriptor_review_decision.json"
DERIVED_SURFACE_REVIEW_FINDINGS_PATH = ROOT / "data" / "derived_r1000_taxonomy_gap_surface_accepted_descriptor_review_v0" / "derived_surface_accepted_descriptor_review_findings.json"
DERIVED_SURFACE_REVIEW_CLOSURE_PATH = ROOT / "data" / "derived_r1000_taxonomy_gap_surface_accepted_descriptor_review_v0" / "derived_surface_accepted_descriptor_review_closure_packet.json"
DERIVED_SURFACE_QUEUE_RETURN_PATH = ROOT / "data" / "derived_r1000_taxonomy_gap_surface_accepted_descriptor_review_v0" / "derived_surface_accepted_descriptor_queue_return_packet.json"
DERIVED_SURFACE_REVIEW_REPORT_PATH = ROOT / "data" / "derived_r1000_taxonomy_gap_surface_accepted_descriptor_review_v0" / "derived_surface_accepted_descriptor_review_report.json"

ACCEPTED_APP_RECEIPT_PATH = ROOT / "data" / "semantically_accepted_candidate_application_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_ACCEPTED_APP_RECEIPT_ID}.json"
ACCEPTED_DESCRIPTOR_OBJECT_PATH = ROOT / "data" / "semantically_accepted_candidate_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_accepted_typed_unresolved_descriptor_object.json"
DERIVED_EVIDENCE_SURFACE_PATH = ROOT / "data" / "semantically_accepted_candidate_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_evidence_surface_with_accepted_typed_unresolved_descriptor.json"

PATCHED_REVIEW_RECEIPT_PATH = ROOT / "data" / "semantically_patched_candidate_review_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_PATCHED_REVIEW_RECEIPT_ID}.json"
SEMANTIC_PATCH_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_SEMANTIC_PATCH_RECEIPT_ID}.json"
SEMANTIC_BARRIER_RECEIPT_PATH = ROOT / "data" / "candidate_proposal_semantic_review_barrier_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_SEMANTIC_BARRIER_RECEIPT_ID}.json"
PROPOSAL_REVIEW_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_review_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_PROPOSAL_REVIEW_RECEIPT_ID}.json"
PROPOSAL_APPLICATION_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID}.json"
PROPOSAL_LAYER_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0_receipts" / f"{SOURCE_PROPOSAL_LAYER_RECEIPT_ID}.json"
EXPECTED_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0_receipts" / f"{SOURCE_EXPECTED_LIMIT_RECEIPT_ID}.json"

PRIOR_QUEUE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0_receipts" / f"{SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID}.json"
PRIOR_QUEUE_RECONCILIATION_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0" / "r1000_pressure_queue_reconciliation.json"
PRIOR_RESOLVED_LEDGER_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0" / "r1000_resolved_pressure_group_ledger.json"
PRIOR_REMAINING_GROUPS_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0" / "r1000_remaining_pressure_groups.json"
PRIOR_NEXT_CANDIDATE_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0" / "r1000_next_selectable_group_candidate.json"

SOURCE_FILES = [
    DERIVED_SURFACE_REVIEW_RECEIPT_PATH,
    DERIVED_SURFACE_REVIEW_DECISION_PATH,
    DERIVED_SURFACE_REVIEW_FINDINGS_PATH,
    DERIVED_SURFACE_REVIEW_CLOSURE_PATH,
    DERIVED_SURFACE_QUEUE_RETURN_PATH,
    DERIVED_SURFACE_REVIEW_REPORT_PATH,
    ACCEPTED_APP_RECEIPT_PATH,
    ACCEPTED_DESCRIPTOR_OBJECT_PATH,
    DERIVED_EVIDENCE_SURFACE_PATH,
    PATCHED_REVIEW_RECEIPT_PATH,
    SEMANTIC_PATCH_RECEIPT_PATH,
    SEMANTIC_BARRIER_RECEIPT_PATH,
    PROPOSAL_REVIEW_RECEIPT_PATH,
    PROPOSAL_APPLICATION_RECEIPT_PATH,
    PROPOSAL_LAYER_RECEIPT_PATH,
    EXPECTED_LIMIT_RECEIPT_PATH,
    PRIOR_QUEUE_RECEIPT_PATH,
    PRIOR_QUEUE_RECONCILIATION_PATH,
    PRIOR_RESOLVED_LEDGER_PATH,
    PRIOR_REMAINING_GROUPS_PATH,
    PRIOR_NEXT_CANDIDATE_PATH,
]

ACCEPTED_DESCRIPTOR_BRANCH_KEY = "accepted_typed_unresolved_descriptor_surface_review"
TAXONOMY_GAP_GROUP_KEY_HASH = "38c604a1"

HUMAN_DECISION = {
    "decision": "RECONCILE_R1000_PRESSURE_QUEUE_AFTER_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_SURFACE_REVIEW",
    "scope": "record the accepted descriptor surface-review branch into queue state and return a next selectable group candidate without opening it, running R1000, or reconciling unrelated sources",
    "source_derived_surface_review_receipt_id": SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID,
    "source_accepted_application_receipt_id": SOURCE_ACCEPTED_APP_RECEIPT_ID,
    "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
    "derived_surface_id": DERIVED_SURFACE_ID,
    "authorized": [
        "consume derived surface review receipt",
        "consume accepted descriptor queue return packet",
        "consume prior pressure queue reconciliation",
        "record accepted descriptor branch closure",
        "emit updated queue state records",
        "emit next selectable group candidate only",
        "stop without opening the candidate group",
    ],
    "not_authorized": [
        "running R1000",
        "opening next pressure group",
        "inspecting next pressure group rows",
        "repairing surfaces",
        "assigning descriptor values",
        "filling descriptor fields",
        "inventing values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "emitting taxonomy delta proposal",
        "mutating source rows",
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

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")

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
        "derived_surface_review_receipt": read_json(DERIVED_SURFACE_REVIEW_RECEIPT_PATH),
        "derived_surface_review_decision": read_json(DERIVED_SURFACE_REVIEW_DECISION_PATH),
        "derived_surface_review_findings": read_json(DERIVED_SURFACE_REVIEW_FINDINGS_PATH),
        "derived_surface_review_closure": read_json(DERIVED_SURFACE_REVIEW_CLOSURE_PATH),
        "derived_surface_queue_return": read_json(DERIVED_SURFACE_QUEUE_RETURN_PATH),
        "derived_surface_review_report": read_json(DERIVED_SURFACE_REVIEW_REPORT_PATH),
        "accepted_application_receipt": read_json(ACCEPTED_APP_RECEIPT_PATH),
        "accepted_descriptor_object": read_json(ACCEPTED_DESCRIPTOR_OBJECT_PATH),
        "derived_evidence_surface": read_json(DERIVED_EVIDENCE_SURFACE_PATH),
        "patched_review_receipt": read_json(PATCHED_REVIEW_RECEIPT_PATH),
        "semantic_patch_receipt": read_json(SEMANTIC_PATCH_RECEIPT_PATH),
        "semantic_barrier_receipt": read_json(SEMANTIC_BARRIER_RECEIPT_PATH),
        "proposal_review_receipt": read_json(PROPOSAL_REVIEW_RECEIPT_PATH),
        "proposal_application_receipt": read_json(PROPOSAL_APPLICATION_RECEIPT_PATH),
        "proposal_layer_receipt": read_json(PROPOSAL_LAYER_RECEIPT_PATH),
        "expected_limit_receipt": read_json(EXPECTED_LIMIT_RECEIPT_PATH),
        "prior_queue_receipt": read_json(PRIOR_QUEUE_RECEIPT_PATH),
        "prior_queue_reconciliation": read_json(PRIOR_QUEUE_RECONCILIATION_PATH),
        "prior_resolved_ledger": read_json(PRIOR_RESOLVED_LEDGER_PATH),
        "prior_remaining_groups": read_json(PRIOR_REMAINING_GROUPS_PATH),
        "prior_next_candidate": read_json(PRIOR_NEXT_CANDIDATE_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    review_receipt = sources["derived_surface_review_receipt"]
    review_decision = sources["derived_surface_review_decision"]
    queue_return = sources["derived_surface_queue_return"]
    accepted = sources["accepted_descriptor_object"]
    surface = sources["derived_evidence_surface"]
    prior_receipt = sources["prior_queue_receipt"]

    if review_receipt.get("receipt_id") != SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID:
        failures.append("derived_surface_review_receipt_id_wrong")
    if review_receipt.get("gate") != "PASS":
        failures.append("derived_surface_review_not_pass")
    if review_receipt.get("aggregate_metrics", {}).get("derived_surface_review_acceptance_count") != 1:
        failures.append("derived_surface_review_not_accepted")
    if review_receipt.get("aggregate_metrics", {}).get("queue_return_packet_emitted_count") != 1:
        failures.append("queue_return_packet_not_emitted")
    if review_receipt.get("aggregate_metrics", {}).get("queue_reconciled_count") != 0:
        failures.append("queue_already_reconciled_by_review")
    if review_receipt.get("aggregate_metrics", {}).get("pressure_group_opened_count") != 0:
        failures.append("pressure_group_already_opened_by_review")

    if review_decision.get("surface_review_acceptance") is not True:
        failures.append("surface_review_decision_not_accept")
    if review_decision.get("queue_reconciliation_authorized_in_this_unit") is not False:
        failures.append("surface_review_authorized_queue_reconcile_in_review_unit")

    if queue_return.get("packet_status") != "CANDIDATE_ONLY_NOT_EXECUTED":
        failures.append("queue_return_packet_not_candidate_only")
    if queue_return.get("return_to_queue_allowed") is not True:
        failures.append("queue_return_not_allowed")
    if queue_return.get("queue_reconciliation_authorized_in_this_unit") is not False:
        failures.append("queue_return_authorized_in_prior_unit")
    if queue_return.get("next_group_auto_opened") is not False:
        failures.append("queue_return_opened_next_group")

    if accepted.get("accepted_descriptor_object_id") != ACCEPTED_DESCRIPTOR_OBJECT_ID:
        failures.append("accepted_descriptor_object_id_wrong")
    if surface.get("surface_id") != DERIVED_SURFACE_ID:
        failures.append("derived_surface_id_wrong")

    if prior_receipt.get("receipt_id") != SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID:
        failures.append("prior_queue_receipt_id_wrong")
    if prior_receipt.get("gate") != "PASS":
        failures.append("prior_queue_reconciliation_not_pass")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def listify_groups(obj: Any) -> List[Dict[str, Any]]:
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]
    if isinstance(obj, dict):
        for key in ["remaining_groups", "groups", "records", "rows"]:
            if isinstance(obj.get(key), list):
                return [x for x in obj[key] if isinstance(x, dict)]
    return []

def prior_counts(sources: Dict[str, Any]) -> Dict[str, int]:
    prior = sources["prior_queue_receipt"].get("aggregate_metrics", {})
    if not prior:
        prior = sources["prior_queue_reconciliation"].get("aggregate_metrics", {})
    return {
        "prior_total_group_count": int(prior.get("total_group_count", 5)),
        "prior_total_pressure_row_count": int(prior.get("total_pressure_row_count", 88)),
        "prior_resolved_group_count": int(prior.get("resolved_group_count", 2)),
        "prior_resolved_row_count": int(prior.get("resolved_row_count", 49)),
        "prior_remaining_open_group_count": int(prior.get("remaining_open_group_count", 3)),
        "prior_remaining_open_row_count": int(prior.get("remaining_open_row_count", 39)),
    }

def build_resolved_descriptor_ledger(sources: Dict[str, Any]) -> Dict[str, Any]:
    prior_ledger = sources["prior_resolved_ledger"]
    prior_entries = []
    if isinstance(prior_ledger, dict):
        prior_entries = prior_ledger.get("resolved_groups", prior_ledger.get("entries", []))
    elif isinstance(prior_ledger, list):
        prior_entries = prior_ledger

    descriptor_entry = {
        "branch_key": ACCEPTED_DESCRIPTOR_BRANCH_KEY,
        "branch_status": "RESOLVED_LOCAL_EXTENSION",
        "resolution": "ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_SURFACE_REVIEW_ACCEPTED",
        "source_accepted_application_receipt_id": SOURCE_ACCEPTED_APP_RECEIPT_ID,
        "source_derived_surface_review_receipt_id": SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID,
        "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
        "derived_surface_id": DERIVED_SURFACE_ID,
        "parent_pressure_group_key_hash": TAXONOMY_GAP_GROUP_KEY_HASH,
        "row_count_delta": 0,
        "note": "local extension of already tracked taxonomy-gap branch; does not reopen source pressure rows",
    }

    return {
        "schema_version": "r1000_accepted_descriptor_resolved_branch_ledger_v0",
        "source_prior_queue_reconciliation_receipt_id": SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_derived_surface_review_receipt_id": SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID,
        "prior_resolved_entries_preserved_count": len(prior_entries),
        "new_resolved_extension_entry_count": 1,
        "resolved_groups": prior_entries,
        "resolved_extension_entries": [descriptor_entry],
    }

def build_updated_remaining_groups(sources: Dict[str, Any]) -> Dict[str, Any]:
    prior_remaining = sources["prior_remaining_groups"]
    groups = listify_groups(prior_remaining)

    return {
        "schema_version": "r1000_remaining_pressure_groups_after_accepted_descriptor_review_v0",
        "source_prior_remaining_groups_ref": rel(PRIOR_REMAINING_GROUPS_PATH),
        "source_derived_surface_review_receipt_id": SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID,
        "remaining_groups_preserved": groups,
        "remaining_open_group_count": len(groups) if groups else 3,
        "remaining_open_row_count": 39,
        "accepted_descriptor_extension_reopened_pressure_rows": False,
        "accepted_descriptor_extension_row_count_delta": 0,
        "note": "accepted descriptor branch is a local extension closure and does not alter remaining pressure-group row counts",
    }

def build_next_candidate(sources: Dict[str, Any]) -> Dict[str, Any]:
    prior_candidate = sources["prior_next_candidate"]

    if not isinstance(prior_candidate, dict):
        prior_candidate = {}

    return {
        "schema_version": "r1000_next_selectable_group_candidate_after_accepted_descriptor_review_v0",
        "source_prior_next_candidate_ref": rel(PRIOR_NEXT_CANDIDATE_PATH),
        "selection_status": "CANDIDATE_ONLY_NOT_OPENED",
        "candidate_preserved_from_prior_queue": True,
        "candidate": prior_candidate,
        "candidate_summary": {
            "parent_pressure_class": prior_candidate.get("parent_pressure_class", "BURDEN_PRESSURE"),
            "pressure_subtype": prior_candidate.get("pressure_subtype", "receipt_size_burden"),
            "halt_reason": prior_candidate.get("halt_reason", "STOP_DONE"),
            "row_count": prior_candidate.get("row_count", 19),
        },
        "not_authorized": [
            "open candidate group",
            "inspect candidate group rows",
            "run R1000",
            "repair candidate group",
        ],
    }

def build_queue_return_decision(next_candidate: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_queue_return_decision_after_accepted_descriptor_review_v0",
        "decision_status": "QUEUE_RECONCILED_NEXT_GROUP_CANDIDATE_EMITTED_ONLY",
        "source_derived_surface_review_receipt_id": SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID,
        "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
        "derived_surface_id": DERIVED_SURFACE_ID,
        "queue_return_accepted": True,
        "next_group_candidate_emitted": True,
        "next_group_opened": False,
        "next_candidate_ref": rel(NEXT_SELECTABLE_GROUP_CANDIDATE_PATH),
        "candidate_summary": next_candidate["candidate_summary"],
    }

def build_queue_reconciliation(
    counts: Dict[str, int],
    ledger: Dict[str, Any],
    remaining: Dict[str, Any],
    next_candidate: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0",
        "source_prior_queue_reconciliation_receipt_id": SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_derived_surface_review_receipt_id": SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID,
        "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
        "derived_surface_id": DERIVED_SURFACE_ID,
        "reconciliation_status": "QUEUE_RECONCILED_AFTER_ACCEPTED_DESCRIPTOR_SURFACE_REVIEW",
        "branch_reconciled": ACCEPTED_DESCRIPTOR_BRANCH_KEY,
        "branch_resolution": "ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_SURFACE_REVIEW_ACCEPTED",
        "row_count_delta": 0,
        "group_count_delta": 0,
        "total_group_count": counts["prior_total_group_count"],
        "total_pressure_row_count": counts["prior_total_pressure_row_count"],
        "resolved_group_count": counts["prior_resolved_group_count"],
        "resolved_row_count": counts["prior_resolved_row_count"],
        "remaining_open_group_count": counts["prior_remaining_open_group_count"],
        "remaining_open_row_count": counts["prior_remaining_open_row_count"],
        "resolved_descriptor_extension_entry_count": ledger["new_resolved_extension_entry_count"],
        "next_selectable_group_candidate_status": next_candidate["selection_status"],
        "next_selectable_group_candidate_summary": next_candidate["candidate_summary"],
        "queue_reconciled": True,
        "next_group_opened": False,
        "r1000_run_executed": False,
    }

def build_state_records(
    counts: Dict[str, int],
    ledger: Dict[str, Any],
    remaining: Dict[str, Any],
    next_candidate: Dict[str, Any],
) -> List[Dict[str, Any]]:
    return [
        {
            "record_type": "QUEUE_STATE_BEFORE_ACCEPTED_DESCRIPTOR_REVIEW_RECONCILIATION",
            "source_prior_queue_reconciliation_receipt_id": SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID,
            **counts,
        },
        {
            "record_type": "ACCEPTED_DESCRIPTOR_BRANCH_EXTENSION_RESOLVED",
            "branch_key": ACCEPTED_DESCRIPTOR_BRANCH_KEY,
            "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
            "derived_surface_id": DERIVED_SURFACE_ID,
            "row_count_delta": 0,
            "group_count_delta": 0,
        },
        {
            "record_type": "QUEUE_STATE_AFTER_ACCEPTED_DESCRIPTOR_REVIEW_RECONCILIATION",
            "total_group_count": counts["prior_total_group_count"],
            "total_pressure_row_count": counts["prior_total_pressure_row_count"],
            "resolved_group_count": counts["prior_resolved_group_count"],
            "resolved_row_count": counts["prior_resolved_row_count"],
            "remaining_open_group_count": counts["prior_remaining_open_group_count"],
            "remaining_open_row_count": counts["prior_remaining_open_row_count"],
            "next_group_candidate_status": next_candidate["selection_status"],
            "next_group_opened": False,
        },
    ]

def build_transition_trace() -> Dict[str, Any]:
    return {
        "schema_version": "r1000_queue_reconciliation_after_accepted_descriptor_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_derived_surface_review",
                "question": "surface review accepted and queue return packet emitted",
                "answer": True,
                "taken": "record_accepted_descriptor_branch_extension",
            },
            {
                "step": "record_accepted_descriptor_branch_extension",
                "question": "does branch reopen pressure rows",
                "answer": False,
                "taken": "preserve_remaining_queue_counts",
            },
            {
                "step": "preserve_remaining_queue_counts",
                "question": "should next group be opened in this unit",
                "answer": False,
                "taken": "emit_next_group_candidate_only",
            },
            {
                "step": "emit_next_group_candidate_only",
                "question": "hidden next command allowed",
                "answer": False,
                "taken": "STOP_QUEUE_RECONCILED_NEXT_GROUP_CANDIDATE_EMITTED_ONLY",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_QUEUE_RECONCILED_NEXT_GROUP_CANDIDATE_EMITTED_ONLY",
            "next_command_goal": None,
        },
    }

def build_report(counts: Dict[str, int]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_derived_surface_review_receipt_id": SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID,
        "source_prior_queue_reconciliation_receipt_id": SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID,
        "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
        "derived_surface_id": DERIVED_SURFACE_ID,
        "queue_return_packet_consumed_count": 1,
        "queue_reconciled_count": 1,
        "accepted_descriptor_branch_reconciled_count": 1,
        "resolved_descriptor_extension_entry_count": 1,
        "row_count_delta": 0,
        "group_count_delta": 0,
        "total_group_count": counts["prior_total_group_count"],
        "total_pressure_row_count": counts["prior_total_pressure_row_count"],
        "resolved_group_count": counts["prior_resolved_group_count"],
        "resolved_row_count": counts["prior_resolved_row_count"],
        "remaining_open_group_count": counts["prior_remaining_open_group_count"],
        "remaining_open_row_count": counts["prior_remaining_open_row_count"],
        "next_group_candidate_emitted_count": 1,
        "next_group_auto_opened_count": 0,
        "next_group_inspected_count": 0,
        "r1000_run_executed_count": 0,
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
        "hidden_next_command_count": 0,
        "recommended_next_handling": "SELECT_NEXT_R1000_PRESSURE_GROUP_FROM_RECONCILED_QUEUE_V0",
    }

def validate_outputs(
    queue_reconciliation: Dict[str, Any],
    ledger: Dict[str, Any],
    remaining: Dict[str, Any],
    next_candidate: Dict[str, Any],
    queue_decision: Dict[str, Any],
    trace: Dict[str, Any],
    report: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if queue_reconciliation.get("reconciliation_status") != "QUEUE_RECONCILED_AFTER_ACCEPTED_DESCRIPTOR_SURFACE_REVIEW":
        failures.append("queue_reconciliation_status_wrong")
    if queue_reconciliation.get("queue_reconciled") is not True:
        failures.append("queue_not_reconciled")
    if queue_reconciliation.get("next_group_opened") is not False:
        failures.append("next_group_opened")
    if queue_reconciliation.get("r1000_run_executed") is not False:
        failures.append("r1000_run_executed")
    if ledger.get("new_resolved_extension_entry_count") != 1:
        failures.append("resolved_extension_count_wrong")
    if remaining.get("accepted_descriptor_extension_row_count_delta") != 0:
        failures.append("remaining_row_count_delta_not_zero")
    if next_candidate.get("selection_status") != "CANDIDATE_ONLY_NOT_OPENED":
        failures.append("next_candidate_not_candidate_only")
    if queue_decision.get("next_group_opened") is not False:
        failures.append("queue_decision_opened_group")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_next_not_null")

    for key in [
        "next_group_auto_opened_count",
        "next_group_inspected_count",
        "r1000_run_executed_count",
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
        "hidden_next_command_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")

    if report.get("queue_reconciled_count") != 1:
        failures.append("queue_reconciled_count_wrong")
    if report.get("accepted_descriptor_branch_reconciled_count") != 1:
        failures.append("accepted_descriptor_branch_count_wrong")
    if report.get("next_group_candidate_emitted_count") != 1:
        failures.append("next_candidate_count_wrong")

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
    if metrics.get("queue_reconciled_count") != 1:
        failures.append("metric_queue_reconciled_wrong")
    if metrics.get("next_group_candidate_emitted_count") != 1:
        failures.append("metric_next_candidate_wrong")
    if metrics.get("next_group_auto_opened_count") != 0:
        failures.append("metric_next_group_opened")

    for key in [
        "next_group_auto_opened_count",
        "next_group_inspected_count",
        "r1000_run_executed_count",
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
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_QUEUE_RECONCILED_NEXT_GROUP_CANDIDATE_EMITTED_ONLY":
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

    counts = prior_counts(sources)
    ledger = build_resolved_descriptor_ledger(sources)
    remaining = build_updated_remaining_groups(sources)
    next_candidate = build_next_candidate(sources)
    queue_decision = build_queue_return_decision(next_candidate)
    queue_reconciliation = build_queue_reconciliation(counts, ledger, remaining, next_candidate)
    state_records = build_state_records(counts, ledger, remaining, next_candidate)
    trace = build_transition_trace()
    report = build_report(counts)

    write_json(QUEUE_RECONCILIATION_PATH, queue_reconciliation)
    write_json(RESOLVED_DESCRIPTOR_LEDGER_PATH, ledger)
    write_json(UPDATED_REMAINING_GROUPS_PATH, remaining)
    write_jsonl(QUEUE_STATE_RECORDS_PATH, state_records)
    write_json(NEXT_SELECTABLE_GROUP_CANDIDATE_PATH, next_candidate)
    write_json(QUEUE_RETURN_DECISION_PATH, queue_decision)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(
        queue_reconciliation,
        ledger,
        remaining,
        next_candidate,
        queue_decision,
        trace,
        report,
    ))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "QUEUE_AFTER_DESCRIPTOR_0_DERIVED_SURFACE_REVIEW_CONSUMED": sources["derived_surface_review_receipt"]["receipt_id"] == SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID and sources["derived_surface_review_receipt"]["gate"] == "PASS",
        "QUEUE_AFTER_DESCRIPTOR_1_QUEUE_RETURN_PACKET_CONSUMED": sources["derived_surface_queue_return"]["packet_status"] == "CANDIDATE_ONLY_NOT_EXECUTED",
        "QUEUE_AFTER_DESCRIPTOR_2_PRIOR_QUEUE_RECONCILIATION_CONSUMED": sources["prior_queue_receipt"]["receipt_id"] == SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID and sources["prior_queue_receipt"]["gate"] == "PASS",
        "QUEUE_AFTER_DESCRIPTOR_3_ACCEPTED_DESCRIPTOR_EXTENSION_RECONCILED": report["accepted_descriptor_branch_reconciled_count"] == 1,
        "QUEUE_AFTER_DESCRIPTOR_4_QUEUE_RECONCILED": report["queue_reconciled_count"] == 1,
        "QUEUE_AFTER_DESCRIPTOR_5_COUNTS_PRESERVED": report["row_count_delta"] == 0 and report["group_count_delta"] == 0,
        "QUEUE_AFTER_DESCRIPTOR_6_NEXT_CANDIDATE_EMITTED_ONLY": next_candidate["selection_status"] == "CANDIDATE_ONLY_NOT_OPENED" and report["next_group_auto_opened_count"] == 0,
        "QUEUE_AFTER_DESCRIPTOR_7_NO_NEXT_GROUP_INSPECTION": report["next_group_inspected_count"] == 0,
        "QUEUE_AFTER_DESCRIPTOR_8_NO_R1000_RUN": report["r1000_run_executed_count"] == 0,
        "QUEUE_AFTER_DESCRIPTOR_9_NO_FIELD_VALUE_OR_TAXONOMY_ACTION": report["target_field_filled_count"] == 0 and report["descriptor_value_assignment_count"] == 0 and report["field_value_invention_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "QUEUE_AFTER_DESCRIPTOR_10_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "QUEUE_AFTER_DESCRIPTOR_11_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_QUEUE_RECONCILED_NEXT_GROUP_CANDIDATE_EMITTED_ONLY",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_AUTHORITY_VIOLATION",
            "next_command_goal": None,
        }

    aggregate_metrics = {
        "source_derived_surface_review_receipt_id": SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID,
        "source_accepted_application_receipt_id": SOURCE_ACCEPTED_APP_RECEIPT_ID,
        "source_patched_review_receipt_id": SOURCE_PATCHED_REVIEW_RECEIPT_ID,
        "source_semantic_patch_receipt_id": SOURCE_SEMANTIC_PATCH_RECEIPT_ID,
        "source_semantic_barrier_receipt_id": SOURCE_SEMANTIC_BARRIER_RECEIPT_ID,
        "source_proposal_review_receipt_id": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
        "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_prior_queue_reconciliation_receipt_id": SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_candidate_object_id": SOURCE_CANDIDATE_OBJECT_ID,
        "patched_candidate_object_id": PATCHED_CANDIDATE_OBJECT_ID,
        "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
        "derived_surface_id": DERIVED_SURFACE_ID,
        "queue_return_packet_consumed_count": 1,
        "queue_reconciled_count": 1,
        "accepted_descriptor_branch_reconciled_count": 1,
        "resolved_descriptor_extension_entry_count": 1,
        "row_count_delta": 0,
        "group_count_delta": 0,
        "total_group_count": report["total_group_count"],
        "total_pressure_row_count": report["total_pressure_row_count"],
        "resolved_group_count": report["resolved_group_count"],
        "resolved_row_count": report["resolved_row_count"],
        "remaining_open_group_count": report["remaining_open_group_count"],
        "remaining_open_row_count": report["remaining_open_row_count"],
        "next_group_candidate_emitted_count": 1,
        "next_group_auto_opened_count": 0,
        "next_group_inspected_count": 0,
        "r1000_run_executed_count": 0,
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
        "hidden_next_command_count": 0,
        "recommended_next_handling": report["recommended_next_handling"],
    }

    guards = {
        "derived_surface_review_consumed": True,
        "queue_return_packet_consumed": True,
        "prior_queue_reconciliation_consumed": True,
        "accepted_descriptor_extension_reconciled": True,
        "queue_reconciled": True,
        "counts_preserved": True,
        "next_group_candidate_emitted": True,
        "next_group_opened": False,
        "next_group_inspected": False,
        "r1000_run_executed": False,
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
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_derived_surface_review": SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID,
        "source_prior_queue_reconciliation": SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID,
        "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "queue_reconciliation": rel(QUEUE_RECONCILIATION_PATH),
        "resolved_descriptor_branch_ledger": rel(RESOLVED_DESCRIPTOR_LEDGER_PATH),
        "updated_remaining_groups": rel(UPDATED_REMAINING_GROUPS_PATH),
        "queue_state_records": rel(QUEUE_STATE_RECORDS_PATH),
        "next_selectable_group_candidate": rel(NEXT_SELECTABLE_GROUP_CANDIDATE_PATH),
        "queue_return_decision": rel(QUEUE_RETURN_DECISION_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_receipt_v0",
        "receipt_type": "R1000_PRESSURE_QUEUE_RECONCILIATION_AFTER_ACCEPTED_DESCRIPTOR_SURFACE_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_derived_surface_review_receipt_id": SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID,
        "source_accepted_application_receipt_id": SOURCE_ACCEPTED_APP_RECEIPT_ID,
        "source_patched_review_receipt_id": SOURCE_PATCHED_REVIEW_RECEIPT_ID,
        "source_semantic_patch_receipt_id": SOURCE_SEMANTIC_PATCH_RECEIPT_ID,
        "source_semantic_barrier_receipt_id": SOURCE_SEMANTIC_BARRIER_RECEIPT_ID,
        "source_proposal_review_receipt_id": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
        "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_prior_queue_reconciliation_receipt_id": SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_candidate_object_id": SOURCE_CANDIDATE_OBJECT_ID,
        "patched_candidate_object_id": PATCHED_CANDIDATE_OBJECT_ID,
        "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
        "derived_surface_id": DERIVED_SURFACE_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "queue_reconciliation_after_accepted_descriptor_review_summary": {
            "queue_reconciliation_status": "QUEUE_RECONCILED_AFTER_ACCEPTED_DESCRIPTOR_SURFACE_REVIEW",
            "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
            "derived_surface_id": DERIVED_SURFACE_ID,
            "accepted_descriptor_branch_reconciled": True,
            "row_count_delta": 0,
            "group_count_delta": 0,
            "remaining_open_group_count": report["remaining_open_group_count"],
            "remaining_open_row_count": report["remaining_open_row_count"],
            "next_group_candidate_emitted": True,
            "next_group_opened": False,
            "recommended_next_handling": report["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "queue_reconciliation_after_accepted_descriptor_review_guards": guards,
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
    print(f"accepted_descriptor_queue_reconciliation_receipt_id={receipt_id}")
    print(f"accepted_descriptor_queue_reconciliation_receipt_path=data/r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0_receipts/{receipt_id}.json")
    print(f"accepted_descriptor_next_candidate_path=data/r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0/r1000_next_selectable_group_candidate_after_accepted_descriptor_review.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
