#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "FIX_R1000_BURDEN_QUEUE_NEXT_CANDIDATE_IDENTITY_PRESERVATION_V0"
TARGET_UNIT_ID = "r1000_burden_queue.next_candidate_identity_preservation_fix.v0"

SOURCE_IDENTITY_REVIEW_RECEIPT_ID = "82c10dfc"
SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID = "1cb51143"
SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID = "d3135cdb"
SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID = "dea88520"
SOURCE_SELECTION_RECEIPT_ID = "7c561212"
SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID = "38604be8"
SELECTED_UNKNOWN_GROUP_ID = "f667fa03"

OUT_DIR = ROOT / "data" / "r1000_burden_queue_next_candidate_identity_preservation_fix_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_burden_queue_next_candidate_identity_preservation_fix_v0_receipts"

SOURCE_AUDIT_PATH = OUT_DIR / "r1000_burden_queue_next_candidate_identity_source_audit.json"
REPAIRED_CANDIDATE_PATH = OUT_DIR / "r1000_next_selectable_group_candidate_after_burden_identity_preserved.json"
REPAIRED_SELECTED_GROUP_PATH = OUT_DIR / "r1000_selected_pressure_group_after_burden_identity_preserved.json"
IDENTITY_PRESERVATION_DECISION_PATH = OUT_DIR / "r1000_burden_queue_next_candidate_identity_preservation_decision.json"
IDENTITY_PRESERVATION_DIFF_PATH = OUT_DIR / "r1000_burden_queue_next_candidate_identity_preservation_diff.json"
INSPECTION_RELEASE_PACKET_PATH = OUT_DIR / "r1000_burden_queue_identity_preserved_inspection_release_packet.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_burden_queue_next_candidate_identity_preservation_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_burden_queue_next_candidate_identity_preservation_report.json"

IDENTITY_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_selected_group_after_burden_identity_surface_review_v0_receipts" / f"{SOURCE_IDENTITY_REVIEW_RECEIPT_ID}.json"
IDENTITY_REVIEW_DECISION_PATH = ROOT / "data" / "r1000_selected_group_after_burden_identity_surface_review_v0" / "r1000_selected_group_after_burden_identity_review_decision.json"
IDENTITY_DEFECT_PACKET_PATH = ROOT / "data" / "r1000_selected_group_after_burden_identity_surface_review_v0" / "r1000_selected_group_after_burden_identity_defect_packet.json"
IDENTITY_REPAIR_RECOMMENDATION_PATH = ROOT / "data" / "r1000_selected_group_after_burden_identity_surface_review_v0" / "r1000_selected_group_after_burden_identity_repair_recommendation_packet.json"

SELECTION_AFTER_BURDEN_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_burden_pressure_reconciliation_v0_receipts" / f"{SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID}.json"
SELECTED_AFTER_BURDEN_GROUP_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_burden_pressure_reconciliation_v0" / "r1000_selected_pressure_group_after_burden_pressure_reconciliation.json"

BURDEN_QUEUE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0_receipts" / f"{SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID}.json"
BURDEN_NEXT_CANDIDATE_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0" / "r1000_next_selectable_group_candidate_after_selected_burden_pressure_inspection.json"
BURDEN_REMAINING_GROUPS_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0" / "r1000_remaining_pressure_groups_after_selected_burden_pressure_inspection.json"
BURDEN_QUEUE_RECONCILIATION_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection.json"
BURDEN_QUEUE_REPORT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0" / "r1000_queue_reconciliation_after_selected_burden_pressure_inspection_report.json"

SELECTED_GROUP_INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_selected_pressure_group_inspection_from_reconciled_queue_v0_receipts" / f"{SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID}.json"
SELECTION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_from_reconciled_queue_v0_receipts" / f"{SOURCE_SELECTION_RECEIPT_ID}.json"
QUEUE_RECONCILIATION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0_receipts" / f"{SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID}.json"

SOURCE_FILES = [
    IDENTITY_REVIEW_RECEIPT_PATH,
    IDENTITY_REVIEW_DECISION_PATH,
    IDENTITY_DEFECT_PACKET_PATH,
    IDENTITY_REPAIR_RECOMMENDATION_PATH,
    SELECTION_AFTER_BURDEN_RECEIPT_PATH,
    SELECTED_AFTER_BURDEN_GROUP_PATH,
    BURDEN_QUEUE_RECEIPT_PATH,
    BURDEN_NEXT_CANDIDATE_PATH,
    BURDEN_REMAINING_GROUPS_PATH,
    BURDEN_QUEUE_RECONCILIATION_PATH,
    BURDEN_QUEUE_REPORT_PATH,
    SELECTED_GROUP_INSPECTION_RECEIPT_PATH,
    SELECTION_RECEIPT_PATH,
    QUEUE_RECONCILIATION_RECEIPT_PATH,
]

IDENTITY_FIELDS = ["parent_pressure_class", "pressure_subtype", "halt_reason", "row_count"]
RECOMMENDED_NEXT_HANDLING = "REVIEW_REPAIRED_R1000_BURDEN_QUEUE_NEXT_CANDIDATE_IDENTITY_SURFACE_V0"

HUMAN_DECISION = {
    "decision": "FIX_R1000_BURDEN_QUEUE_NEXT_CANDIDATE_IDENTITY_PRESERVATION",
    "scope": "repair the derived next-candidate identity surface by preserving typed identity from explicit remaining-group source evidence; emit repaired candidate and selected-group artifacts only, without mutating prior artifacts or inspecting the group",
    "source_identity_review_receipt_id": SOURCE_IDENTITY_REVIEW_RECEIPT_ID,
    "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
    "selected_unknown_group_id": SELECTED_UNKNOWN_GROUP_ID,
    "authorized": [
        "consume identity review receipt",
        "consume burden queue next-candidate artifact",
        "consume burden queue remaining-groups artifact",
        "audit source evidence for candidate identity",
        "emit repaired candidate identity artifact when evidence is explicit",
        "emit repaired selected group artifact from repaired candidate",
        "emit inspection release packet for separate review",
        "stop before inspection",
    ],
    "not_authorized": [
        "mutating existing candidate artifact",
        "mutating existing remaining-groups artifact",
        "mutating existing receipts",
        "inventing pressure class",
        "inventing pressure subtype",
        "inventing halt reason",
        "inspecting selected group rows",
        "running R1000",
        "repairing surfaces beyond derived identity preservation artifact",
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
        "identity_review_receipt": read_json(IDENTITY_REVIEW_RECEIPT_PATH),
        "identity_review_decision": read_json(IDENTITY_REVIEW_DECISION_PATH),
        "identity_defect_packet": read_json(IDENTITY_DEFECT_PACKET_PATH),
        "identity_repair_recommendation": read_json(IDENTITY_REPAIR_RECOMMENDATION_PATH),
        "selection_after_burden_receipt": read_json(SELECTION_AFTER_BURDEN_RECEIPT_PATH),
        "selected_after_burden_group": read_json(SELECTED_AFTER_BURDEN_GROUP_PATH),
        "burden_queue_receipt": read_json(BURDEN_QUEUE_RECEIPT_PATH),
        "burden_next_candidate": read_json(BURDEN_NEXT_CANDIDATE_PATH),
        "burden_remaining_groups": read_json(BURDEN_REMAINING_GROUPS_PATH),
        "burden_queue_reconciliation": read_json(BURDEN_QUEUE_RECONCILIATION_PATH),
        "burden_queue_report": read_json(BURDEN_QUEUE_REPORT_PATH),
        "selected_group_inspection_receipt": read_json(SELECTED_GROUP_INSPECTION_RECEIPT_PATH),
        "selection_receipt": read_json(SELECTION_RECEIPT_PATH),
        "queue_reconciliation_receipt": read_json(QUEUE_RECONCILIATION_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    identity = sources["identity_review_receipt"]
    decision = sources["identity_review_decision"]
    repair_rec = sources["identity_repair_recommendation"]
    selection = sources["selection_after_burden_receipt"]
    burden = sources["burden_queue_receipt"]
    candidate = sources["burden_next_candidate"]

    if identity.get("receipt_id") != SOURCE_IDENTITY_REVIEW_RECEIPT_ID:
        failures.append("identity_review_receipt_id_wrong")
    if identity.get("gate") != "PASS":
        failures.append("identity_review_not_pass")
    if identity.get("aggregate_metrics", {}).get("identity_defect_count") != 3:
        failures.append("identity_defect_count_unexpected")
    if identity.get("aggregate_metrics", {}).get("inspection_blocked_count") != 1:
        failures.append("identity_review_did_not_block_inspection")
    if identity.get("aggregate_metrics", {}).get("identity_assignment_count") != 0:
        failures.append("prior_identity_review_assigned_identity")

    if decision.get("decision_status") != "BLOCK_INSPECTION_REQUIRES_IDENTITY_PRESERVATION_FIX":
        failures.append("identity_decision_status_wrong")
    if repair_rec.get("packet_status") != "CANDIDATE_ONLY_NOT_EXECUTED":
        failures.append("repair_recommendation_not_candidate_only")
    if repair_rec.get("recommended_next_handling") != UNIT_ID:
        failures.append("repair_recommendation_not_for_this_unit")

    if selection.get("receipt_id") != SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID:
        failures.append("selection_after_burden_receipt_id_wrong")
    if selection.get("gate") != "PASS":
        failures.append("selection_after_burden_not_pass")
    if selection.get("selected_pressure_group_id") != SELECTED_UNKNOWN_GROUP_ID:
        failures.append("selected_unknown_group_id_wrong")
    if selection.get("aggregate_metrics", {}).get("selected_group_inspected_count") != 0:
        failures.append("selected_unknown_group_already_inspected")

    if burden.get("receipt_id") != SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID:
        failures.append("burden_queue_receipt_id_wrong")
    if burden.get("gate") != "PASS":
        failures.append("burden_queue_not_pass")
    if burden.get("aggregate_metrics", {}).get("next_group_candidate_emitted_count") != 1:
        failures.append("burden_queue_next_candidate_not_emitted")
    if burden.get("aggregate_metrics", {}).get("next_group_auto_opened_count") != 0:
        failures.append("burden_queue_next_group_already_opened")

    if candidate.get("selection_status") != "CANDIDATE_ONLY_NOT_OPENED":
        failures.append("source_candidate_not_candidate_only")
    if candidate.get("next_group_opened") is not False:
        failures.append("source_candidate_already_opened")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def is_unknown(v: Any) -> bool:
    return v is None or v == "" or v == "UNKNOWN"

def normalize_candidate(obj: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(obj, dict):
        return None

    containers = [obj]
    for key in [
        "candidate_summary",
        "selected_group",
        "selected_group_summary",
        "group",
        "pressure_group",
        "group_summary",
        "candidate",
        "source_group",
        "remaining_group",
    ]:
        nested = obj.get(key)
        if isinstance(nested, dict):
            containers.append(nested)

    best: Optional[Dict[str, Any]] = None
    best_score = -1

    aliases = {
        "parent_pressure_class": [
            "parent_pressure_class",
            "pressure_class",
            "class",
            "pressure_parent",
            "pressure_family",
            "family",
        ],
        "pressure_subtype": [
            "pressure_subtype",
            "subtype",
            "pressure_type",
            "type",
            "category",
        ],
        "halt_reason": [
            "halt_reason",
            "halt",
            "stop_code",
            "stop_reason",
            "terminal_halt",
        ],
        "row_count": [
            "row_count",
            "rows",
            "count",
            "n_rows",
            "pressure_row_count",
            "group_row_count",
        ],
    }

    for container in containers:
        candidate: Dict[str, Any] = {}
        for field, names in aliases.items():
            for name in names:
                if name in container:
                    candidate[field] = container[name]
                    break
        if "row_count" in candidate:
            try:
                candidate["row_count"] = int(candidate["row_count"] or 0)
            except Exception:
                candidate["row_count"] = 0
        score = sum(1 for field in ["parent_pressure_class", "pressure_subtype", "halt_reason"] if not is_unknown(candidate.get(field)))
        if "row_count" in candidate and candidate.get("row_count", 0) > 0:
            score += 1
        if score > best_score:
            best = candidate
            best_score = score

    if best is None:
        return None

    return {
        "parent_pressure_class": best.get("parent_pressure_class", "UNKNOWN"),
        "pressure_subtype": best.get("pressure_subtype", "UNKNOWN"),
        "halt_reason": best.get("halt_reason", "UNKNOWN"),
        "row_count": int(best.get("row_count", 0) or 0),
    }

def walk_objects(obj: Any, path: str = "$") -> List[Tuple[str, Dict[str, Any]]]:
    found: List[Tuple[str, Dict[str, Any]]] = []
    if isinstance(obj, dict):
        normalized = normalize_candidate(obj)
        if normalized is not None:
            found.append((path, normalized))
        for key, value in obj.items():
            found.extend(walk_objects(value, f"{path}.{key}"))
    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            found.extend(walk_objects(value, f"{path}[{idx}]"))
    return found

def identity_score(candidate: Dict[str, Any]) -> int:
    return sum(1 for field in ["parent_pressure_class", "pressure_subtype", "halt_reason"] if not is_unknown(candidate.get(field)))

def fully_typed(candidate: Dict[str, Any]) -> bool:
    return identity_score(candidate) == 3 and int(candidate.get("row_count", 0) or 0) > 0

def candidate_matches_required_row(candidate: Dict[str, Any], required_row_count: int) -> bool:
    return int(candidate.get("row_count", 0) or 0) == required_row_count

def select_best_evidence(sources: Dict[str, Any], required_row_count: int) -> Tuple[Optional[Dict[str, Any]], List[Dict[str, Any]]]:
    evidence_pool: List[Dict[str, Any]] = []

    source_order = [
        ("burden_remaining_groups", BURDEN_REMAINING_GROUPS_PATH),
        ("burden_queue_reconciliation", BURDEN_QUEUE_RECONCILIATION_PATH),
        ("burden_queue_receipt", BURDEN_QUEUE_RECEIPT_PATH),
        ("burden_queue_report", BURDEN_QUEUE_REPORT_PATH),
        ("queue_reconciliation_receipt", QUEUE_RECONCILIATION_RECEIPT_PATH),
        ("selection_receipt", SELECTION_RECEIPT_PATH),
    ]

    for source_name, source_path in source_order:
        for path, candidate in walk_objects(sources[source_name]):
            score = identity_score(candidate)
            row_match = candidate_matches_required_row(candidate, required_row_count)
            evidence_pool.append({
                "source_name": source_name,
                "source_ref": rel(source_path),
                "json_path": path,
                "candidate": candidate,
                "identity_score": score,
                "row_count_matches_target": row_match,
                "fully_typed": fully_typed(candidate),
                "usable_for_repair": fully_typed(candidate) and row_match,
            })

    usable = [entry for entry in evidence_pool if entry["usable_for_repair"]]
    usable.sort(key=lambda entry: (
        entry["source_name"] != "burden_remaining_groups",
        entry["json_path"],
    ))

    if usable:
        return usable[0], evidence_pool

    return None, evidence_pool

def build_source_audit(sources: Dict[str, Any], selected_unknown: Dict[str, Any], best: Optional[Dict[str, Any]], evidence_pool: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_burden_queue_next_candidate_identity_source_audit_v0",
        "source_identity_review_receipt_id": SOURCE_IDENTITY_REVIEW_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_candidate_ref": rel(BURDEN_NEXT_CANDIDATE_PATH),
        "source_remaining_groups_ref": rel(BURDEN_REMAINING_GROUPS_PATH),
        "selected_unknown_group_id": SELECTED_UNKNOWN_GROUP_ID,
        "selected_unknown_group": selected_unknown,
        "required_row_count": selected_unknown.get("row_count"),
        "evidence_candidate_count": len(evidence_pool),
        "usable_evidence_candidate_count": sum(1 for entry in evidence_pool if entry["usable_for_repair"]),
        "best_evidence": best,
        "evidence_pool": evidence_pool,
        "audit_result": "EXPLICIT_TYPED_IDENTITY_EVIDENCE_FOUND" if best else "NO_EXPLICIT_TYPED_IDENTITY_EVIDENCE_FOUND",
    }

def build_repaired_candidate(sources: Dict[str, Any], selected_unknown: Dict[str, Any], best: Dict[str, Any]) -> Dict[str, Any]:
    repaired_summary = copy.deepcopy(best["candidate"])
    repaired_candidate_id = sha8({
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_identity_review_receipt_id": SOURCE_IDENTITY_REVIEW_RECEIPT_ID,
        "repaired_summary": repaired_summary,
    })

    return {
        "schema_version": "r1000_next_selectable_group_candidate_after_burden_identity_preserved_v0",
        "repaired_candidate_id": repaired_candidate_id,
        "source_identity_review_receipt_id": SOURCE_IDENTITY_REVIEW_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_unknown_candidate_ref": rel(BURDEN_NEXT_CANDIDATE_PATH),
        "source_evidence": {
            "source_name": best["source_name"],
            "source_ref": best["source_ref"],
            "json_path": best["json_path"],
        },
        "repair_status": "IDENTITY_PRESERVED_FROM_EXPLICIT_SOURCE_EVIDENCE",
        "selection_status": "CANDIDATE_ONLY_NOT_OPENED",
        "candidate_summary_before": selected_unknown,
        "candidate_summary_after": repaired_summary,
        "identity_fields_preserved": [
            "parent_pressure_class",
            "pressure_subtype",
            "halt_reason",
            "row_count",
        ],
        "identity_assignment_method": "copy_from_explicit_source_evidence",
        "field_value_invention": False,
        "source_mutation": False,
        "existing_receipt_mutation": False,
        "next_group_opened": False,
        "r1000_run_executed": False,
    }

def build_repaired_selected_group(repaired_candidate: Dict[str, Any]) -> Dict[str, Any]:
    summary = repaired_candidate["candidate_summary_after"]
    selected_pressure_group_id = sha8({
        "source_repaired_candidate_id": repaired_candidate["repaired_candidate_id"],
        "summary": summary,
        "selection": "identity_preserved_after_burden_reconciliation",
    })
    return {
        "schema_version": "r1000_selected_pressure_group_after_burden_identity_preserved_v0",
        "selected_pressure_group_id": selected_pressure_group_id,
        "source_repaired_candidate_id": repaired_candidate["repaired_candidate_id"],
        "source_repaired_candidate_ref": rel(REPAIRED_CANDIDATE_PATH),
        "selection_status": "SELECTED_NOT_INSPECTED",
        "selected_from_candidate_status": "CANDIDATE_ONLY_NOT_OPENED",
        "selected_group": summary,
        "selected_group_rows_materialized": False,
        "selected_group_rows_inspected": False,
        "r1000_run_executed": False,
        "requires_separate_identity_review": True,
        "requires_separate_inspection_unit": True,
    }

def build_decision(best: Optional[Dict[str, Any]], repaired_candidate: Optional[Dict[str, Any]], repaired_selected: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    repaired = repaired_candidate is not None and repaired_selected is not None
    return {
        "schema_version": "r1000_burden_queue_next_candidate_identity_preservation_decision_v0",
        "decision_id": sha8({
            "source_identity_review_receipt_id": SOURCE_IDENTITY_REVIEW_RECEIPT_ID,
            "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
            "repaired": repaired,
        }),
        "decision_status": "IDENTITY_PRESERVATION_FIX_EMITTED" if repaired else "IDENTITY_PRESERVATION_FIX_BLOCKED_SOURCE_EVIDENCE_MISSING",
        "explicit_source_evidence_found": best is not None,
        "identity_preserved": repaired,
        "identity_assignment_by_invention": False,
        "source_mutation_authorized": False,
        "existing_receipt_mutation_authorized": False,
        "inspection_authorized_in_this_unit": False,
        "repair_applied_to_source_artifacts": False,
        "repaired_candidate_id": repaired_candidate.get("repaired_candidate_id") if repaired_candidate else None,
        "repaired_selected_pressure_group_id": repaired_selected.get("selected_pressure_group_id") if repaired_selected else None,
        "recommended_next_handling": RECOMMENDED_NEXT_HANDLING if repaired else "STOP_IDENTITY_PRESERVATION_FIX_REQUIRES_HUMAN_SCHEMA_DECISION_V0",
    }

def build_diff(selected_unknown: Dict[str, Any], repaired_candidate: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    after = repaired_candidate["candidate_summary_after"] if repaired_candidate else None
    diffs = []
    if after:
        for field in IDENTITY_FIELDS:
            diffs.append({
                "field": field,
                "before": selected_unknown.get(field),
                "after": after.get(field),
                "changed": selected_unknown.get(field) != after.get(field),
                "change_type": "PRESERVED_FROM_SOURCE_EVIDENCE" if selected_unknown.get(field) != after.get(field) else "UNCHANGED",
            })

    return {
        "schema_version": "r1000_burden_queue_next_candidate_identity_preservation_diff_v0",
        "source_identity_review_receipt_id": SOURCE_IDENTITY_REVIEW_RECEIPT_ID,
        "selected_unknown_group_id": SELECTED_UNKNOWN_GROUP_ID,
        "before": selected_unknown,
        "after": after,
        "field_diffs": diffs,
        "field_value_invention": False,
        "source_mutation": False,
        "existing_receipt_mutation": False,
    }

def build_release_packet(decision: Dict[str, Any], repaired_selected: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_burden_queue_identity_preserved_inspection_release_packet_v0",
        "packet_status": "CANDIDATE_ONLY_NOT_EXECUTED",
        "source_identity_preservation_decision_ref": rel(IDENTITY_PRESERVATION_DECISION_PATH),
        "identity_preserved": decision["identity_preserved"],
        "inspection_release_status": "REQUIRES_SEPARATE_IDENTITY_REVIEW_BEFORE_INSPECTION" if decision["identity_preserved"] else "BLOCKED",
        "repaired_selected_pressure_group_id": decision["repaired_selected_pressure_group_id"],
        "repaired_selected_pressure_group_ref": rel(REPAIRED_SELECTED_GROUP_PATH) if repaired_selected else None,
        "recommended_next_handling": decision["recommended_next_handling"],
        "inspection_authorized_in_this_unit": False,
        "next_group_opened": False,
    }

def build_transition_trace(decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_burden_queue_next_candidate_identity_preservation_transition_trace_v0",
        "trace": [
            {
                "step": "consume_identity_review",
                "question": "identity review found UNKNOWN fields and blocked inspection",
                "answer": True,
                "taken": "audit_source_identity_evidence",
            },
            {
                "step": "audit_source_identity_evidence",
                "question": "explicit typed identity evidence exists",
                "answer": decision["explicit_source_evidence_found"],
                "taken": "emit_repaired_candidate" if decision["explicit_source_evidence_found"] else "stop_source_evidence_missing",
            },
            {
                "step": "emit_repaired_candidate",
                "question": "mutate source candidate artifact",
                "answer": False,
                "taken": "write_derived_identity_preservation_artifacts",
            },
            {
                "step": "write_derived_identity_preservation_artifacts",
                "question": "inspect repaired group in this unit",
                "answer": False,
                "taken": "STOP_IDENTITY_PRESERVATION_FIX_EMITTED_REVIEW_REQUIRED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_IDENTITY_PRESERVATION_FIX_EMITTED_REVIEW_REQUIRED" if decision["identity_preserved"] else "STOP_IDENTITY_PRESERVATION_FIX_BLOCKED_SOURCE_EVIDENCE_MISSING",
            "next_command_goal": None,
        },
    }

def build_report(
    selected_unknown: Dict[str, Any],
    best: Optional[Dict[str, Any]],
    repaired_candidate: Optional[Dict[str, Any]],
    repaired_selected: Optional[Dict[str, Any]],
    decision: Dict[str, Any],
    source_audit: Dict[str, Any],
) -> Dict[str, Any]:
    after = repaired_candidate["candidate_summary_after"] if repaired_candidate else None
    return {
        "schema_version": "r1000_burden_queue_next_candidate_identity_preservation_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_identity_review_receipt_id": SOURCE_IDENTITY_REVIEW_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_unknown_group_id": SELECTED_UNKNOWN_GROUP_ID,
        "source_identity_review_consumed_count": 1,
        "source_candidate_consumed_count": 1,
        "source_remaining_groups_consumed_count": 1,
        "source_audit_emitted_count": 1,
        "explicit_source_evidence_found_count": 1 if best else 0,
        "identity_preservation_fix_emitted_count": 1 if decision["identity_preserved"] else 0,
        "repaired_candidate_emitted_count": 1 if repaired_candidate else 0,
        "repaired_selected_group_emitted_count": 1 if repaired_selected else 0,
        "identity_preservation_diff_emitted_count": 1,
        "inspection_release_packet_emitted_count": 1,
        "unknown_identity_field_count_before": sum(1 for field in ["parent_pressure_class", "pressure_subtype", "halt_reason"] if is_unknown(selected_unknown.get(field))),
        "unknown_identity_field_count_after": sum(1 for field in ["parent_pressure_class", "pressure_subtype", "halt_reason"] if after and is_unknown(after.get(field))),
        "selected_parent_pressure_class_before": selected_unknown.get("parent_pressure_class"),
        "selected_pressure_subtype_before": selected_unknown.get("pressure_subtype"),
        "selected_halt_reason_before": selected_unknown.get("halt_reason"),
        "selected_row_count_before": selected_unknown.get("row_count"),
        "selected_parent_pressure_class_after": after.get("parent_pressure_class") if after else None,
        "selected_pressure_subtype_after": after.get("pressure_subtype") if after else None,
        "selected_halt_reason_after": after.get("halt_reason") if after else None,
        "selected_row_count_after": after.get("row_count") if after else None,
        "identity_assignment_count": 0,
        "field_value_invention_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "source_artifact_mutation_count": 0,
        "selected_group_inspected_count": 0,
        "selected_group_rows_materialized_count": 0,
        "selected_group_rows_inspected_count": 0,
        "queue_reconciled_count": 0,
        "next_group_auto_opened_count": 0,
        "other_group_opened_count": 0,
        "r1000_run_executed_count": 0,
        "repair_source_artifact_count": 0,
        "proposal_applied_count": 0,
        "target_field_filled_count": 0,
        "descriptor_value_assignment_count": 0,
        "null_field_value_emitted_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": decision["recommended_next_handling"],
    }

def validate_outputs(
    source_audit: Dict[str, Any],
    repaired_candidate: Optional[Dict[str, Any]],
    repaired_selected: Optional[Dict[str, Any]],
    decision: Dict[str, Any],
    diff: Dict[str, Any],
    release_packet: Dict[str, Any],
    trace: Dict[str, Any],
    report: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if source_audit.get("audit_result") != "EXPLICIT_TYPED_IDENTITY_EVIDENCE_FOUND":
        failures.append("explicit_typed_identity_evidence_not_found")
    if source_audit.get("usable_evidence_candidate_count", 0) < 1:
        failures.append("usable_evidence_count_missing")
    if repaired_candidate is None:
        failures.append("repaired_candidate_missing")
    else:
        after = repaired_candidate.get("candidate_summary_after", {})
        if not fully_typed(after):
            failures.append("repaired_candidate_not_fully_typed")
        if repaired_candidate.get("field_value_invention") is not False:
            failures.append("repaired_candidate_invented_value")
        if repaired_candidate.get("source_mutation") is not False:
            failures.append("repaired_candidate_mutated_source")
        if repaired_candidate.get("next_group_opened") is not False:
            failures.append("repaired_candidate_opened_next_group")

    if repaired_selected is None:
        failures.append("repaired_selected_group_missing")
    else:
        if repaired_selected.get("selection_status") != "SELECTED_NOT_INSPECTED":
            failures.append("repaired_selected_status_wrong")
        if repaired_selected.get("selected_group_rows_inspected") is not False:
            failures.append("repaired_selected_rows_inspected")
        if repaired_selected.get("r1000_run_executed") is not False:
            failures.append("repaired_selected_r1000_run")

    if decision.get("identity_assignment_by_invention") is not False:
        failures.append("decision_allows_invention")
    if decision.get("source_mutation_authorized") is not False:
        failures.append("decision_authorizes_source_mutation")
    if decision.get("inspection_authorized_in_this_unit") is not False:
        failures.append("decision_authorizes_inspection")
    if release_packet.get("packet_status") != "CANDIDATE_ONLY_NOT_EXECUTED":
        failures.append("release_packet_not_candidate_only")
    if release_packet.get("inspection_authorized_in_this_unit") is not False:
        failures.append("release_packet_authorizes_inspection")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_next_not_null")

    for key in [
        "identity_assignment_count",
        "field_value_invention_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "source_artifact_mutation_count",
        "selected_group_inspected_count",
        "selected_group_rows_materialized_count",
        "selected_group_rows_inspected_count",
        "queue_reconciled_count",
        "next_group_auto_opened_count",
        "other_group_opened_count",
        "r1000_run_executed_count",
        "repair_source_artifact_count",
        "proposal_applied_count",
        "target_field_filled_count",
        "descriptor_value_assignment_count",
        "null_field_value_emitted_count",
        "taxonomy_label_creation_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "hidden_next_command_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")

    if report.get("identity_preservation_fix_emitted_count") != 1:
        failures.append("identity_preservation_fix_count_wrong")
    if report.get("unknown_identity_field_count_before") != 3:
        failures.append("unknown_before_count_wrong")
    if report.get("unknown_identity_field_count_after") != 0:
        failures.append("unknown_after_count_wrong")

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
    if metrics.get("identity_preservation_fix_emitted_count") != 1:
        failures.append("metric_identity_fix_count_wrong")
    if metrics.get("unknown_identity_field_count_after") != 0:
        failures.append("metric_unknown_after_not_zero")
    if metrics.get("explicit_source_evidence_found_count") != 1:
        failures.append("metric_explicit_evidence_missing")

    for key in [
        "identity_assignment_count",
        "field_value_invention_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "source_artifact_mutation_count",
        "selected_group_inspected_count",
        "selected_group_rows_materialized_count",
        "selected_group_rows_inspected_count",
        "queue_reconciled_count",
        "next_group_auto_opened_count",
        "other_group_opened_count",
        "r1000_run_executed_count",
        "repair_source_artifact_count",
        "proposal_applied_count",
        "target_field_filled_count",
        "descriptor_value_assignment_count",
        "null_field_value_emitted_count",
        "taxonomy_label_creation_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_IDENTITY_PRESERVATION_FIX_EMITTED_REVIEW_REQUIRED":
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

    selected_unknown = sources["identity_review_receipt"]["identity_surface_review_summary"]["selected_group"]
    required_row_count = int(selected_unknown.get("row_count", 0) or 0)

    best, evidence_pool = select_best_evidence(sources, required_row_count)
    source_audit = build_source_audit(sources, selected_unknown, best, evidence_pool)

    repaired_candidate = build_repaired_candidate(sources, selected_unknown, best) if best else None
    repaired_selected = build_repaired_selected_group(repaired_candidate) if repaired_candidate else None
    decision = build_decision(best, repaired_candidate, repaired_selected)
    diff = build_diff(selected_unknown, repaired_candidate)
    release_packet = build_release_packet(decision, repaired_selected)
    trace = build_transition_trace(decision)
    report = build_report(selected_unknown, best, repaired_candidate, repaired_selected, decision, source_audit)

    write_json(SOURCE_AUDIT_PATH, source_audit)
    if repaired_candidate:
        write_json(REPAIRED_CANDIDATE_PATH, repaired_candidate)
    if repaired_selected:
        write_json(REPAIRED_SELECTED_GROUP_PATH, repaired_selected)
    write_json(IDENTITY_PRESERVATION_DECISION_PATH, decision)
    write_json(IDENTITY_PRESERVATION_DIFF_PATH, diff)
    write_json(INSPECTION_RELEASE_PACKET_PATH, release_packet)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(
        source_audit,
        repaired_candidate,
        repaired_selected,
        decision,
        diff,
        release_packet,
        trace,
        report,
    ))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "IDENTITY_FIX_0_IDENTITY_REVIEW_CONSUMED": sources["identity_review_receipt"]["receipt_id"] == SOURCE_IDENTITY_REVIEW_RECEIPT_ID and sources["identity_review_receipt"]["gate"] == "PASS",
        "IDENTITY_FIX_1_SOURCE_CANDIDATE_CONSUMED": sources["burden_next_candidate"]["selection_status"] == "CANDIDATE_ONLY_NOT_OPENED",
        "IDENTITY_FIX_2_SOURCE_AUDIT_EMITTED": source_audit["audit_result"] == "EXPLICIT_TYPED_IDENTITY_EVIDENCE_FOUND",
        "IDENTITY_FIX_3_EXPLICIT_TYPED_EVIDENCE_FOUND": best is not None,
        "IDENTITY_FIX_4_REPAIRED_CANDIDATE_EMITTED": repaired_candidate is not None and fully_typed(repaired_candidate["candidate_summary_after"]),
        "IDENTITY_FIX_5_UNKNOWN_FIELDS_REMOVED_WITHOUT_INVENTION": report["unknown_identity_field_count_before"] == 3 and report["unknown_identity_field_count_after"] == 0 and report["field_value_invention_count"] == 0,
        "IDENTITY_FIX_6_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "IDENTITY_FIX_7_NO_GROUP_INSPECTION_OR_QUEUE_RECONCILIATION": report["selected_group_inspected_count"] == 0 and report["queue_reconciled_count"] == 0,
        "IDENTITY_FIX_8_NO_R1000_RUN_OR_REPAIR_SOURCE_ARTIFACT": report["r1000_run_executed_count"] == 0 and report["repair_source_artifact_count"] == 0,
        "IDENTITY_FIX_9_NO_FIELD_VALUE_OR_TAXONOMY_ACTION": report["target_field_filled_count"] == 0 and report["descriptor_value_assignment_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "IDENTITY_FIX_10_NO_NEXT_GROUP_OR_HIDDEN_COMMAND": report["next_group_auto_opened_count"] == 0 and report["other_group_opened_count"] == 0 and report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_IDENTITY_PRESERVATION_FIX_EMITTED_REVIEW_REQUIRED",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_AUTHORITY_VIOLATION",
            "next_command_goal": None,
        }
    if best is None:
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_IDENTITY_PRESERVATION_FIX_BLOCKED_SOURCE_EVIDENCE_MISSING",
            "next_command_goal": None,
        }

    aggregate_metrics = {
        "source_identity_review_receipt_id": SOURCE_IDENTITY_REVIEW_RECEIPT_ID,
        "source_selection_after_burden_receipt_id": SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_selected_group_inspection_receipt_id": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_unknown_group_id": SELECTED_UNKNOWN_GROUP_ID,
        "source_identity_review_consumed_count": 1,
        "source_candidate_consumed_count": 1,
        "source_remaining_groups_consumed_count": 1,
        "source_audit_emitted_count": 1,
        "evidence_candidate_count": source_audit["evidence_candidate_count"],
        "usable_evidence_candidate_count": source_audit["usable_evidence_candidate_count"],
        "explicit_source_evidence_found_count": report["explicit_source_evidence_found_count"],
        "identity_preservation_fix_emitted_count": report["identity_preservation_fix_emitted_count"],
        "repaired_candidate_emitted_count": report["repaired_candidate_emitted_count"],
        "repaired_selected_group_emitted_count": report["repaired_selected_group_emitted_count"],
        "identity_preservation_diff_emitted_count": 1,
        "inspection_release_packet_emitted_count": 1,
        "repaired_candidate_id": repaired_candidate.get("repaired_candidate_id") if repaired_candidate else None,
        "repaired_selected_pressure_group_id": repaired_selected.get("selected_pressure_group_id") if repaired_selected else None,
        "unknown_identity_field_count_before": report["unknown_identity_field_count_before"],
        "unknown_identity_field_count_after": report["unknown_identity_field_count_after"],
        "selected_parent_pressure_class_before": report["selected_parent_pressure_class_before"],
        "selected_pressure_subtype_before": report["selected_pressure_subtype_before"],
        "selected_halt_reason_before": report["selected_halt_reason_before"],
        "selected_row_count_before": report["selected_row_count_before"],
        "selected_parent_pressure_class_after": report["selected_parent_pressure_class_after"],
        "selected_pressure_subtype_after": report["selected_pressure_subtype_after"],
        "selected_halt_reason_after": report["selected_halt_reason_after"],
        "selected_row_count_after": report["selected_row_count_after"],
        "identity_assignment_count": 0,
        "field_value_invention_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "existing_receipt_mutation_count": 0,
        "source_artifact_mutation_count": 0,
        "selected_group_inspected_count": 0,
        "selected_group_rows_materialized_count": 0,
        "selected_group_rows_inspected_count": 0,
        "queue_reconciled_count": 0,
        "next_group_auto_opened_count": 0,
        "other_group_opened_count": 0,
        "r1000_run_executed_count": 0,
        "repair_source_artifact_count": 0,
        "proposal_applied_count": 0,
        "target_field_filled_count": 0,
        "descriptor_value_assignment_count": 0,
        "null_field_value_emitted_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": decision["recommended_next_handling"],
    }

    guards = {
        "identity_review_consumed": True,
        "source_candidate_consumed": True,
        "source_remaining_groups_consumed": True,
        "source_audit_emitted": True,
        "explicit_typed_evidence_found": best is not None,
        "identity_preservation_fix_emitted": repaired_candidate is not None,
        "unknown_fields_removed_without_invention": report["unknown_identity_field_count_after"] == 0 and report["field_value_invention_count"] == 0,
        "repaired_candidate_emitted": repaired_candidate is not None,
        "repaired_selected_group_emitted": repaired_selected is not None,
        "inspection_release_packet_emitted": True,
        "identity_assignment": False,
        "field_value_invention": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "source_artifact_mutated": False,
        "selected_group_inspected": False,
        "selected_group_rows_materialized": False,
        "selected_group_rows_inspected": False,
        "queue_reconciled": False,
        "next_group_opened": False,
        "r1000_run_executed": False,
        "repair_source_artifact": False,
        "proposal_applied": False,
        "target_field_filled": False,
        "descriptor_value_assigned": False,
        "null_field_value_emitted": False,
        "taxonomy_label_created": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_identity_review_receipt": SOURCE_IDENTITY_REVIEW_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "repaired_candidate_id": repaired_candidate.get("repaired_candidate_id") if repaired_candidate else None,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_audit": rel(SOURCE_AUDIT_PATH),
        "repaired_candidate": rel(REPAIRED_CANDIDATE_PATH) if repaired_candidate else None,
        "repaired_selected_group": rel(REPAIRED_SELECTED_GROUP_PATH) if repaired_selected else None,
        "identity_preservation_decision": rel(IDENTITY_PRESERVATION_DECISION_PATH),
        "identity_preservation_diff": rel(IDENTITY_PRESERVATION_DIFF_PATH),
        "inspection_release_packet": rel(INSPECTION_RELEASE_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_burden_queue_next_candidate_identity_preservation_fix_receipt_v0",
        "receipt_type": "R1000_BURDEN_QUEUE_NEXT_CANDIDATE_IDENTITY_PRESERVATION_FIX_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_identity_review_receipt_id": SOURCE_IDENTITY_REVIEW_RECEIPT_ID,
        "source_selection_after_burden_receipt_id": SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_selected_group_inspection_receipt_id": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_unknown_group_id": SELECTED_UNKNOWN_GROUP_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "identity_preservation_fix_summary": {
            "fix_result": "IDENTITY_PRESERVATION_FIX_EMITTED" if repaired_candidate else "IDENTITY_PRESERVATION_FIX_BLOCKED_SOURCE_EVIDENCE_MISSING",
            "selected_unknown_group_id": SELECTED_UNKNOWN_GROUP_ID,
            "selected_group_before": selected_unknown,
            "selected_group_after": repaired_candidate.get("candidate_summary_after") if repaired_candidate else None,
            "unknown_identity_field_count_before": report["unknown_identity_field_count_before"],
            "unknown_identity_field_count_after": report["unknown_identity_field_count_after"],
            "explicit_source_evidence_found": best is not None,
            "field_value_invention": False,
            "source_mutation": source_mutation_detected,
            "existing_receipt_mutation": False,
            "inspection_authorized_in_this_unit": False,
            "recommended_next_handling": decision["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "identity_preservation_fix_guards": guards,
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
    print(f"identity_preservation_fix_receipt_id={receipt_id}")
    print(f"identity_preservation_fix_receipt_path=data/r1000_burden_queue_next_candidate_identity_preservation_fix_v0_receipts/{receipt_id}.json")
    print(f"repaired_candidate_path=data/r1000_burden_queue_next_candidate_identity_preservation_fix_v0/r1000_next_selectable_group_candidate_after_burden_identity_preserved.json")
    print(f"repaired_selected_group_path=data/r1000_burden_queue_next_candidate_identity_preservation_fix_v0/r1000_selected_pressure_group_after_burden_identity_preserved.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
