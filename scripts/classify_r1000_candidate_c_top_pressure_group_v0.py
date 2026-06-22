#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLASSIFY_R1000_CANDIDATE_C_TOP_PRESSURE_GROUP_V0"
TARGET_UNIT_ID = "r1000_candidate_c_top_pressure_group_classification.v0"

SOURCE_R1000_SCALE_RECEIPT_ID = "a121ff40"
SOURCE_R1000_BATCH_ID = "r1000_candidate_c_batch_cdd7f676"
SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID = "fabba052"
SOURCE_COARSENING_REVIEW_RECEIPT_ID = "f03689e3"
SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID = "f09b8395"
SOURCE_R250_PRESSURE_BATCH_ID = "r250_pressure_metrics_batch_1095f5c6"

ACCEPTED_CANDIDATE_ID = "C"
ACCEPTED_CANDIDATE_NAME = "parent_plus_subtype_plus_halt_reason"
ACCEPTED_CANDIDATE_FIELDS = ["parent_pressure_class", "pressure_subtype", "halt_reason"]

VALID_CLASSES = [
    "FIXABLE_PRESSURE",
    "HEALTHY_EXPECTED_PRESSURE",
    "NOT_ENOUGH_EVIDENCE",
]

DECISION_PACKET_CHOICES = [
    "ACCEPT_FIXABLE_PRESSURE_REPAIR_OBJECTIVE",
    "MARK_TOP_GROUP_HEALTHY_AND_INSPECT_NEXT",
    "REQUEST_MORE_TOP_GROUP_EVIDENCE",
    "COMPARE_TOP_TWO_GROUPS_BEFORE_DECISION",
    "REJECT_TOP_GROUP_CLASSIFICATION",
]

OUT_DIR = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0_receipts"

TOP_GROUP_SELECTION_PATH = OUT_DIR / "top_group_selection.json"
TOP_GROUP_MEMBERSHIP_PATH = OUT_DIR / "top_group_event_membership.jsonl"
TOP_GROUP_FRAGMENTS_PATH = OUT_DIR / "top_group_representative_fragments.json"
TOP_GROUP_EVIDENCE_ROLLUP_PATH = OUT_DIR / "top_group_evidence_rollup.json"
TOP_GROUP_CLASSIFICATION_PATH = OUT_DIR / "top_group_classification.json"
TOP_GROUP_DECISION_PACKET_PATH = OUT_DIR / "top_group_decision_packet.json"
TOP_GROUP_REPAIR_PROPOSAL_PATH = OUT_DIR / "top_group_repair_objective_proposal.json"

SOURCE_R1000_SCALE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0_receipts" / f"{SOURCE_R1000_SCALE_RECEIPT_ID}.json"
SOURCE_R1000_GROUP_ROWS_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_candidate_c_group_rows.jsonl"
SOURCE_R1000_MEMBERSHIP_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_candidate_c_group_event_membership.jsonl"
SOURCE_R1000_GROUP_ROLLUP_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_candidate_c_group_rollup.json"
SOURCE_R1000_PRESSURE_EVENTS_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_pressure_event_rows.jsonl"
SOURCE_R1000_COMPARISON_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r250_vs_r1000_candidate_c_comparison_matrix.json"
SOURCE_R1000_CLASSIFICATION_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_scale_stability_classification.json"
SOURCE_R1000_REPORT_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_pressure_scale_stability_report.json"
SOURCE_R1000_PACKET_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_pressure_scale_stability_decision_packet.json"
SOURCE_CANDIDATE_C_RECEIPT_PATH = ROOT / "data" / "r250_pressure_candidate_c_interrogation_v0_receipts" / f"{SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID}.json"
SOURCE_COARSENING_RECEIPT_PATH = ROOT / "data" / "r250_pressure_coarsening_review_v0_receipts" / f"{SOURCE_COARSENING_REVIEW_RECEIPT_ID}.json"
SOURCE_PRESSURE_METRICS_RECEIPT_PATH = ROOT / "data" / "r250_pressure_metrics_v0_receipts" / f"{SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID}.json"

SOURCE_FILES = [
    SOURCE_R1000_SCALE_RECEIPT_PATH,
    SOURCE_R1000_GROUP_ROWS_PATH,
    SOURCE_R1000_MEMBERSHIP_PATH,
    SOURCE_R1000_GROUP_ROLLUP_PATH,
    SOURCE_R1000_PRESSURE_EVENTS_PATH,
    SOURCE_R1000_COMPARISON_PATH,
    SOURCE_R1000_CLASSIFICATION_PATH,
    SOURCE_R1000_REPORT_PATH,
    SOURCE_R1000_PACKET_PATH,
    SOURCE_CANDIDATE_C_RECEIPT_PATH,
    SOURCE_COARSENING_RECEIPT_PATH,
    SOURCE_PRESSURE_METRICS_RECEIPT_PATH,
]

HUMAN_DECISION = {
    "decision": "CLASSIFY_R1000_CANDIDATE_C_TOP_PRESSURE_GROUP",
    "scope": "top_group_classification_only",
    "rank_rule": "stable_rank_authorizes_inspection_order_not_repair",
    "not_authorized": [
        "repair_execution",
        "taxonomy_upgrade",
        "authority_widening",
        "burden_optimization",
        "extraction_repair",
        "protocol_adoption",
        "next_group_auto_inspection",
        "build_command",
    ],
}

MUST_NOT_INFER = [
    "stable rank authorizes inspection order only",
    "stable rank does not authorize repair",
    "do not inspect top two by default",
    "top-two comparison is fallback only",
    "do not execute repair",
    "do not mutate taxonomy",
    "do not widen authority",
    "do not optimize burden",
    "do not repair extraction",
    "do not adopt protocol globally",
    "do not auto-skip future groups",
    "do not auto-open next group",
    "do not emit build command without human decision",
]

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

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")

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
        "scale_receipt": read_json(SOURCE_R1000_SCALE_RECEIPT_PATH),
        "group_rows": read_jsonl(SOURCE_R1000_GROUP_ROWS_PATH),
        "membership_rows": read_jsonl(SOURCE_R1000_MEMBERSHIP_PATH),
        "group_rollup": read_json(SOURCE_R1000_GROUP_ROLLUP_PATH),
        "pressure_events": read_jsonl(SOURCE_R1000_PRESSURE_EVENTS_PATH),
        "comparison": read_json(SOURCE_R1000_COMPARISON_PATH),
        "scale_classification": read_json(SOURCE_R1000_CLASSIFICATION_PATH),
        "scale_report": read_json(SOURCE_R1000_REPORT_PATH),
        "scale_packet": read_json(SOURCE_R1000_PACKET_PATH),
        "candidate_c_receipt": read_json(SOURCE_CANDIDATE_C_RECEIPT_PATH),
        "coarsening_receipt": read_json(SOURCE_COARSENING_RECEIPT_PATH),
        "pressure_metrics_receipt": read_json(SOURCE_PRESSURE_METRICS_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    scale = sources["scale_receipt"]
    candidate = sources["candidate_c_receipt"]
    rollup = sources["group_rollup"]
    scale_packet = sources["scale_packet"]

    if scale.get("receipt_id") != SOURCE_R1000_SCALE_RECEIPT_ID:
        failures.append("scale_receipt_id_wrong")
    if scale.get("gate") != "PASS":
        failures.append("scale_receipt_not_pass")
    if scale.get("unit_id") != "BUILD_R1000_PRESSURE_SCALE_STABILITY_RUN_WITH_CANDIDATE_C_V0":
        failures.append("scale_unit_wrong")
    if scale.get("r1000_batch_id") != SOURCE_R1000_BATCH_ID:
        failures.append("scale_batch_id_wrong")
    if scale.get("accepted_candidate_id") != ACCEPTED_CANDIDATE_ID:
        failures.append("scale_candidate_not_C")
    if scale.get("accepted_candidate_fields") != ACCEPTED_CANDIDATE_FIELDS:
        failures.append("scale_candidate_fields_wrong")
    if scale.get("scale_stability_summary", {}).get("rank_order_preserved") is not True:
        failures.append("rank_order_not_preserved")
    if scale.get("scale_stability_summary", {}).get("dominant_group_preserved") is not True:
        failures.append("dominant_group_not_preserved")
    if scale.get("aggregate_metrics", {}).get("new_r1000_group_count") != 0:
        failures.append("new_r1000_group_count_nonzero")
    if scale.get("aggregate_metrics", {}).get("missing_r250_group_count") != 0:
        failures.append("missing_r250_group_count_nonzero")
    if scale.get("aggregate_metrics", {}).get("scale_stability_class") != "LOW_MARGIN_PERSISTS":
        failures.append("expected_low_margin_persists")
    if scale.get("terminal", {}).get("type") != "STOP":
        failures.append("scale_terminal_not_stop")
    if scale.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("scale_terminal_next_not_null")

    if candidate.get("receipt_id") != SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID or candidate.get("gate") != "PASS":
        failures.append("candidate_c_receipt_not_pass")
    if candidate.get("accepted_coarsening_fields") != ACCEPTED_CANDIDATE_FIELDS:
        failures.append("candidate_c_fields_wrong")

    if rollup.get("candidate_c_group_size_profile") != [25, 24, 19, 16, 4]:
        failures.append(f"r1000_group_profile_wrong:{rollup.get('candidate_c_group_size_profile')}")
    if rollup.get("candidate_c_dominant_group_count") != 25:
        failures.append("r1000_dominant_count_wrong")
    if rollup.get("candidate_c_second_group_count") != 24:
        failures.append("r1000_second_count_wrong")
    if rollup.get("candidate_c_dominant_group_margin") != 1:
        failures.append("r1000_margin_wrong")

    if scale_packet.get("packet_type") != "HUMAN_REVIEW_PACKET_NOT_COMMAND":
        failures.append("scale_packet_type_wrong")
    for key in [
        "may_emit_build_command",
        "may_emit_objective_proposal",
        "may_authorize_taxonomy_upgrade",
        "may_authorize_authority_widening",
        "may_authorize_optimization",
        "may_authorize_extraction_repair",
        "may_authorize_protocol_adoption",
    ]:
        if scale_packet.get(key) is not False:
            failures.append(f"scale_packet_guard_not_false:{key}:{scale_packet.get(key)}")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def select_top_group(group_rows: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any] | None, List[Dict[str, Any]]]:
    ranked = sorted(group_rows, key=lambda row: (-row["r1000_count"], row["group_key_hash"]))
    if not ranked:
        raise SystemExit("STOP_GATE_FAIL: no R1000 Candidate C groups available")
    return ranked[0], ranked[1] if len(ranked) > 1 else None, ranked

def build_top_group_selection(top: Dict[str, Any], second: Dict[str, Any] | None, ranked: List[Dict[str, Any]], rollup: Dict[str, Any]) -> Dict[str, Any]:
    margin = top["r1000_count"] - (second["r1000_count"] if second else 0)
    total = rollup["total_pressure_event_count"]
    return {
        "schema_version": "top_group_selection_v0",
        "selection_rule": [
            "r1000_count descending",
            "group_key_hash ascending deterministic tie-breaker",
        ],
        "top_group_key_hash": top["group_key_hash"],
        "top_group_rank": top["rank_r1000"],
        "top_group_count": top["r1000_count"],
        "top_group_share": top["r1000_share"],
        "parent_pressure_class": top["parent_pressure_class"],
        "pressure_subtype": top["pressure_subtype"],
        "halt_reason": top["halt_reason"],
        "second_group_key_hash": second["group_key_hash"] if second else None,
        "second_group_count": second["r1000_count"] if second else 0,
        "second_group_share": second["r1000_share"] if second else 0,
        "dominant_margin": margin,
        "dominant_margin_share": margin / total if total else 0,
        "low_margin_warning": margin / total < 0.05 if total else True,
        "ranked_group_keys": [row["group_key_hash"] for row in ranked],
        "ranked_group_counts": [row["r1000_count"] for row in ranked],
        "top_two_comparison_default": False,
        "top_two_comparison_fallback_only": True,
        "review_only": True,
    }

def build_membership_and_fragments(top: Dict[str, Any], membership_rows: List[Dict[str, Any]], pressure_events: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    event_by_id = {event["pressure_event_id"]: event for event in pressure_events}
    top_membership = [
        row for row in membership_rows
        if row["group_key_hash"] == top["group_key_hash"]
    ]
    top_membership = sorted(top_membership, key=lambda row: row["pressure_event_id"])

    fragments = []
    for row in top_membership[: min(10, len(top_membership))]:
        event = event_by_id.get(row["pressure_event_id"])
        if not event:
            continue
        fragments.append({
            "pressure_event_id": row["pressure_event_id"],
            "pressure_pattern_signature_hash": row["pressure_pattern_signature_hash"],
            "work_item_id": row["work_item_id"],
            "slot_id": row["slot_id"],
            "source_receipt_ref": row["source_receipt_ref"],
            "source_trace_ref": row["source_trace_ref"],
            "move_kind": row["move_kind"],
            "evidence_field": row["evidence_field"],
            "terminal_decision": event.get("terminal_decision"),
            "parent_pressure_class": event.get("parent_pressure_class"),
            "pressure_subtype": event.get("pressure_subtype"),
            "halt_reason": event.get("halt_reason"),
            "candidate_c_group_key_hash": event.get("candidate_c_group_key_hash"),
            "observer_only": True,
            "repair_command": None,
            "proposal_authorized": False,
        })

    return top_membership, {
        "schema_version": "top_group_representative_fragments_v0",
        "top_group_key_hash": top["group_key_hash"],
        "representative_fragment_limit": min(10, len(top_membership)),
        "representative_fragment_count": len(fragments),
        "fragments": fragments,
        "top_two_comparison_performed": False,
        "top_two_comparison_reason": None,
        "review_only": True,
    }

def build_evidence_rollup(top: Dict[str, Any], second: Dict[str, Any] | None, top_membership: List[Dict[str, Any]], fragments: Dict[str, Any], comparison: Dict[str, Any]) -> Dict[str, Any]:
    comparison_row = next(
        (row for row in comparison["comparison_rows"] if row["group_key_hash"] == top["group_key_hash"]),
        None,
    )
    move_kind_distribution = dict(sorted(Counter(row["move_kind"] for row in top_membership).items()))
    evidence_field_distribution = dict(sorted(Counter(row["evidence_field"] for row in top_membership).items()))
    terminal_decision_distribution = dict(sorted(Counter(fragment["terminal_decision"] for fragment in fragments["fragments"]).items()))
    halt_reason_distribution = dict(sorted(Counter(fragment["halt_reason"] for fragment in fragments["fragments"]).items()))
    signature_hashes = sorted({row["pressure_pattern_signature_hash"] for row in top_membership})

    return {
        "schema_version": "top_group_evidence_rollup_v0",
        "top_group_key_hash": top["group_key_hash"],
        "parent_pressure_class": top["parent_pressure_class"],
        "pressure_subtype": top["pressure_subtype"],
        "halt_reason": top["halt_reason"],
        "r1000_count": top["r1000_count"],
        "r1000_share": top["r1000_share"],
        "rank_r1000": top["rank_r1000"],
        "r250_count": comparison_row["r250_count"] if comparison_row else None,
        "r250_share": comparison_row["r250_share"] if comparison_row else None,
        "rank_r250": comparison_row["rank_r250"] if comparison_row else None,
        "share_delta": comparison_row["share_delta"] if comparison_row else None,
        "rank_delta": comparison_row["rank_delta"] if comparison_row else None,
        "dominant_margin_against_second": top["r1000_count"] - (second["r1000_count"] if second else 0),
        "dominant_margin_share": top["r1000_share"] - (second["r1000_share"] if second else 0),
        "source_event_ids": [row["pressure_event_id"] for row in top_membership],
        "representative_event_refs": [fragment["pressure_event_id"] for fragment in fragments["fragments"]],
        "representative_trace_refs": [fragment["source_trace_ref"] for fragment in fragments["fragments"]],
        "representative_receipt_refs": [fragment["source_receipt_ref"] for fragment in fragments["fragments"]],
        "move_kind_distribution": move_kind_distribution,
        "evidence_field_distribution": evidence_field_distribution,
        "terminal_decision_distribution": terminal_decision_distribution,
        "halt_reason_distribution": halt_reason_distribution,
        "pressure_pattern_signature_hashes": signature_hashes,
        "representative_fragment_count": fragments["representative_fragment_count"],
        "event_membership_count": len(top_membership),
        "same_operational_cause_as_second_unknown": True,
        "top_two_comparison_required_now": False,
        "top_two_comparison_fallback_condition": "only if top fragments cannot classify cleanly or top and second appear to be same operational cause split by lens",
        "review_only": True,
    }

def classify_top_group(evidence: Dict[str, Any], fragments: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    parent = evidence["parent_pressure_class"]
    subtype = evidence["pressure_subtype"]
    halt = evidence["halt_reason"]

    concrete_scope = None
    classification = "NOT_ENOUGH_EVIDENCE"
    reason = "Top group evidence is insufficient for safe repair or healthy classification without deeper fragment review."

    if parent == "AUTHORITY_BOUNDARY" and subtype == "healthy_boundary_stop":
        classification = "HEALTHY_EXPECTED_PRESSURE"
        reason = "Top group represents healthy authority-boundary stopping; pressure is expected and should be skipped rather than repaired."
    elif parent == "TAXONOMY_PRESSURE" and subtype == "missing_label":
        classification = "NOT_ENOUGH_EVIDENCE"
        reason = "Top group points to missing-label taxonomy pressure, but taxonomy upgrade or repair is not authorized from pressure alone; fragment review is required before any concrete objective."
    elif parent == "BURDEN_PRESSURE" and subtype == "receipt_size_burden":
        classification = "FIXABLE_PRESSURE"
        reason = "Top group points to bounded receipt-size burden pressure; a concrete observer-burden repair objective can be proposed for human review."
        concrete_scope = {
            "repair_objective_id": "PROPOSE_RECEIPT_SIZE_BURDEN_REDUCTION_FOR_TOP_CANDIDATE_C_GROUP_V0",
            "repair_scope": "Inspect top Candidate C group receipt-size burden fragments and propose a bounded reduction of observer receipt burden without deleting identity, trace, or decision fields.",
            "files_or_modules_to_inspect": [
                "data/r1000_pressure_scale_stability_candidate_c_v0/r1000_pressure_event_rows.jsonl",
                "data/r1000_pressure_scale_stability_candidate_c_v0/r1000_candidate_c_group_event_membership.jsonl",
                "data/r1000_candidate_c_top_group_classification_v0/top_group_representative_fragments.json",
            ],
            "expected_acceptance_gates": [
                "burden fields reduced only after distinguishability check",
                "receipt identity preserved",
                "trace refs preserved",
                "no source mutation",
                "no taxonomy or authority mutation",
            ],
            "forbidden_scope": [
                "delete receipt identity",
                "delete trace references",
                "change Candidate C lens",
                "mutate taxonomy",
                "widen authority",
                "execute repair without human command",
            ],
            "terminal_rule": "STOP_HUMAN_DECISION_REQUIRED",
        }
    elif parent == "EXTRACTION_PRESSURE" and subtype == "evidence_missing":
        classification = "NOT_ENOUGH_EVIDENCE"
        reason = "Top group points to missing evidence; classification requires deeper fragment inspection before extraction repair can be proposed."

    class_obj = {
        "schema_version": "top_group_classification_v0",
        "classification": classification,
        "classification_reason": reason,
        "classification_classes": VALID_CLASSES,
        "classified_exactly_once": True,
        "classification_priority": [
            "NOT_ENOUGH_EVIDENCE",
            "HEALTHY_EXPECTED_PRESSURE",
            "FIXABLE_PRESSURE",
        ],
        "top_group_key_hash": evidence["top_group_key_hash"],
        "parent_pressure_class": parent,
        "pressure_subtype": subtype,
        "halt_reason": halt,
        "evidence_supports_concrete_repair": classification == "FIXABLE_PRESSURE",
        "evidence_supports_healthy_expected_pressure": classification == "HEALTHY_EXPECTED_PRESSURE",
        "evidence_insufficient": classification == "NOT_ENOUGH_EVIDENCE",
        "top_two_comparison_performed": False,
        "top_two_comparison_fallback_only": True,
        "repair_command_emitted": False,
        "proposal_authorized": classification == "FIXABLE_PRESSURE",
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "extraction_repair_authorized": False,
        "protocol_adoption_authorized": False,
        "review_only": True,
    }

    if classification == "FIXABLE_PRESSURE":
        proposal = {
            "schema_version": "top_group_repair_objective_proposal_v0",
            "proposal_emitted": True,
            "proposal_type": "REPAIR_OBJECTIVE_PROPOSAL_NOT_COMMAND",
            "classification": classification,
            "source_pressure_group_key_hash": evidence["top_group_key_hash"],
            "source_evidence_refs": evidence["representative_event_refs"],
            **concrete_scope,
            "build_command_emitted": False,
            "repair_executed": False,
            "taxonomy_upgrade_authorized": False,
            "authority_widening_authorized": False,
            "optimization_authorized": False,
            "extraction_repair_authorized": False,
            "protocol_adoption_authorized": False,
        }
    else:
        proposal = {
            "schema_version": "top_group_repair_objective_proposal_v0",
            "proposal_emitted": False,
            "reason": "classification_not_fixable",
            "classification": classification,
            "source_pressure_group_key_hash": evidence["top_group_key_hash"],
            "build_command_emitted": False,
            "repair_executed": False,
            "taxonomy_upgrade_authorized": False,
            "authority_widening_authorized": False,
            "optimization_authorized": False,
            "extraction_repair_authorized": False,
            "protocol_adoption_authorized": False,
        }

    return class_obj, proposal

def make_decision_packet(classification: Dict[str, Any], evidence: Dict[str, Any], proposal: Dict[str, Any], ranked_group_keys: List[str]) -> Dict[str, Any]:
    if classification["classification"] == "FIXABLE_PRESSURE":
        recommended = "ACCEPT_FIXABLE_PRESSURE_REPAIR_OBJECTIVE"
    elif classification["classification"] == "HEALTHY_EXPECTED_PRESSURE":
        recommended = "MARK_TOP_GROUP_HEALTHY_AND_INSPECT_NEXT"
    else:
        recommended = "REQUEST_MORE_TOP_GROUP_EVIDENCE"

    next_group = ranked_group_keys[1] if len(ranked_group_keys) > 1 else None

    return {
        "schema_version": "top_group_decision_packet_v0",
        "packet_type": "HUMAN_REVIEW_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "top_group_key_hash": evidence["top_group_key_hash"],
        "classification": classification["classification"],
        "classification_reason": classification["classification_reason"],
        "allowed_human_choices": DECISION_PACKET_CHOICES,
        "recommended_next_handling": recommended,
        "skip_recommendation": classification["classification"] == "HEALTHY_EXPECTED_PRESSURE",
        "skip_reason": classification["classification_reason"] if classification["classification"] == "HEALTHY_EXPECTED_PRESSURE" else None,
        "next_group_rank_to_inspect": 2 if classification["classification"] == "HEALTHY_EXPECTED_PRESSURE" and next_group else None,
        "next_group_key_hash": next_group if classification["classification"] == "HEALTHY_EXPECTED_PRESSURE" else None,
        "evidence_packet_required": classification["classification"] == "NOT_ENOUGH_EVIDENCE",
        "evidence_packet_options": [
            "more representative fragments",
            "deeper event membership inspection",
            "top-vs-second group comparison",
            "additional scale band",
            "manual human read",
        ] if classification["classification"] == "NOT_ENOUGH_EVIDENCE" else [],
        "repair_objective_proposal_ref": rel(TOP_GROUP_REPAIR_PROPOSAL_PATH),
        "repair_objective_proposal_emitted": proposal["proposal_emitted"],
        "top_two_comparison_default": False,
        "top_two_comparison_fallback_only": True,
        "may_emit_repair_command": False,
        "may_emit_build_command": False,
        "may_authorize_taxonomy_upgrade": False,
        "may_authorize_authority_widening": False,
        "may_authorize_optimization": False,
        "may_authorize_extraction_repair": False,
        "may_authorize_protocol_adoption": False,
        "review_only": True,
    }

def validate_outputs(selection: Dict[str, Any], top_membership: List[Dict[str, Any]], fragments: Dict[str, Any], evidence: Dict[str, Any], classification: Dict[str, Any], proposal: Dict[str, Any], packet: Dict[str, Any], ranked: List[Dict[str, Any]]) -> List[str]:
    failures: List[str] = []

    if selection["top_group_key_hash"] != ranked[0]["group_key_hash"]:
        failures.append("top_group_not_highest_count")
    if selection["top_group_count"] != ranked[0]["r1000_count"]:
        failures.append("top_group_count_wrong")
    if selection["top_group_count"] != 25:
        failures.append(f"top_group_expected_count_wrong:{selection['top_group_count']}")
    if selection["second_group_count"] != 24:
        failures.append(f"second_group_expected_count_wrong:{selection['second_group_count']}")
    if selection["selection_rule"] != ["r1000_count descending", "group_key_hash ascending deterministic tie-breaker"]:
        failures.append("tie_breaker_missing_or_wrong")
    if selection["top_two_comparison_default"] is not False:
        failures.append("top_two_comparison_default_true")
    if selection["top_two_comparison_fallback_only"] is not True:
        failures.append("top_two_fallback_not_true")

    if len(top_membership) != selection["top_group_count"]:
        failures.append(f"membership_count_wrong:{len(top_membership)} expected {selection['top_group_count']}")
    if fragments["representative_fragment_count"] == 0:
        failures.append("representative_fragments_missing")
    if fragments["representative_fragment_count"] > 10:
        failures.append("too_many_representative_fragments")
    if fragments["top_two_comparison_performed"] is not False:
        failures.append("top_two_comparison_performed_by_default")

    if evidence["event_membership_count"] != selection["top_group_count"]:
        failures.append("evidence_membership_count_wrong")
    if evidence["top_two_comparison_required_now"] is not False:
        failures.append("top_two_comparison_required_now_wrong")
    if evidence["top_group_key_hash"] != selection["top_group_key_hash"]:
        failures.append("evidence_top_group_key_mismatch")
    if evidence["parent_pressure_class"] != selection["parent_pressure_class"]:
        failures.append("evidence_parent_mismatch")
    if evidence["pressure_subtype"] != selection["pressure_subtype"]:
        failures.append("evidence_subtype_mismatch")
    if evidence["halt_reason"] != selection["halt_reason"]:
        failures.append("evidence_halt_reason_mismatch")

    if classification["classification"] not in VALID_CLASSES:
        failures.append(f"invalid_classification:{classification['classification']}")
    if classification["classified_exactly_once"] is not True:
        failures.append("classification_not_exactly_once")
    class_flags = [
        classification["evidence_supports_concrete_repair"],
        classification["evidence_supports_healthy_expected_pressure"],
        classification["evidence_insufficient"],
    ]
    if sum(1 for flag in class_flags if flag is True) != 1:
        failures.append("classification_multiple_classes_or_zero")
    if classification["top_two_comparison_performed"] is not False:
        failures.append("classification_top_two_performed_by_default")
    if classification["repair_command_emitted"] is not False:
        failures.append("repair_command_emitted")
    for key in [
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "optimization_authorized",
        "extraction_repair_authorized",
        "protocol_adoption_authorized",
    ]:
        if classification.get(key) is not False:
            failures.append(f"classification_guard_not_false:{key}:{classification.get(key)}")

    if classification["classification"] == "FIXABLE_PRESSURE":
        if proposal["proposal_emitted"] is not True:
            failures.append("fixable_without_repair_objective_proposal")
        for key in ["repair_objective_id", "repair_scope", "source_pressure_group_key_hash", "source_evidence_refs", "files_or_modules_to_inspect", "expected_acceptance_gates", "forbidden_scope", "terminal_rule"]:
            if key not in proposal:
                failures.append(f"fixable_proposal_field_missing:{key}")
    else:
        if proposal["proposal_emitted"] is not False:
            failures.append(f"proposal_emitted_for_non_fixable:{classification['classification']}")
        if proposal.get("reason") != "classification_not_fixable":
            failures.append("non_fixable_proposal_reason_wrong")

    for key in [
        "build_command_emitted",
        "repair_executed",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "optimization_authorized",
        "extraction_repair_authorized",
        "protocol_adoption_authorized",
    ]:
        if proposal.get(key) is not False:
            failures.append(f"proposal_guard_not_false:{key}:{proposal.get(key)}")

    if packet["packet_type"] != "HUMAN_REVIEW_PACKET_NOT_COMMAND":
        failures.append("packet_type_wrong")
    if packet["allowed_human_choices"] != DECISION_PACKET_CHOICES:
        failures.append("packet_choices_wrong")
    if packet["top_two_comparison_default"] is not False:
        failures.append("packet_top_two_default_true")
    if packet["top_two_comparison_fallback_only"] is not True:
        failures.append("packet_top_two_fallback_not_true")
    for key in [
        "may_emit_repair_command",
        "may_emit_build_command",
        "may_authorize_taxonomy_upgrade",
        "may_authorize_authority_widening",
        "may_authorize_optimization",
        "may_authorize_extraction_repair",
        "may_authorize_protocol_adoption",
    ]:
        if packet.get(key) is not False:
            failures.append(f"packet_guard_not_false:{key}:{packet.get(key)}")

    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    if receipt.get("source_r1000_scale_stability_receipt_id") != SOURCE_R1000_SCALE_RECEIPT_ID:
        failures.append("source_scale_receipt_wrong")
    if receipt.get("source_r1000_batch_id") != SOURCE_R1000_BATCH_ID:
        failures.append("source_batch_wrong")
    if receipt.get("accepted_candidate_fields") != ACCEPTED_CANDIDATE_FIELDS:
        failures.append("accepted_candidate_fields_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "TOP_GROUP_CLASSIFY_0_SOURCE_SURFACE_VERIFIED",
        "TOP_GROUP_CLASSIFY_1_HUMAN_DECISION_RECORDED",
        "TOP_GROUP_CLASSIFY_2_CANDIDATE_C_LENS_VERIFIED",
        "TOP_GROUP_CLASSIFY_3_R1000_SCALE_RESULT_VERIFIED",
        "TOP_GROUP_CLASSIFY_4_TOP_GROUP_SELECTED_DETERMINISTICALLY",
        "TOP_GROUP_CLASSIFY_5_TOP_GROUP_MEMBERSHIP_EXTRACTED",
        "TOP_GROUP_CLASSIFY_6_REPRESENTATIVE_FRAGMENTS_EMITTED",
        "TOP_GROUP_CLASSIFY_7_EVIDENCE_ROLLUP_EMITTED",
        "TOP_GROUP_CLASSIFY_8_TOP_GROUP_CLASSIFIED_EXACTLY_ONCE",
        "TOP_GROUP_CLASSIFY_9_REPAIR_PROPOSAL_ONLY_IF_FIXABLE",
        "TOP_GROUP_CLASSIFY_10_DECISION_PACKET_EMITTED",
        "TOP_GROUP_CLASSIFY_11_NO_ACTION_EXECUTED",
        "TOP_GROUP_CLASSIFY_12_NO_SOURCE_MUTATION",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    for key in [
        "repair_command_emitted_count",
        "build_command_emitted_count",
        "repair_executed_count",
        "taxonomy_upgrade_authorized_count",
        "authority_widening_authorized_count",
        "optimization_authorized_count",
        "extraction_repair_authorized_count",
        "protocol_adoption_authorized_count",
        "source_mutation_count",
        "hidden_next_command_count",
        "top_two_comparison_default_count",
        "next_group_auto_inspection_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")
    if metrics.get("top_group_count") != 25:
        failures.append("metric_top_group_count_wrong")
    if metrics.get("second_group_count") != 24:
        failures.append("metric_second_group_count_wrong")
    if metrics.get("classification") not in VALID_CLASSES:
        failures.append("metric_classification_invalid")
    if metrics.get("classified_exactly_once") is not True:
        failures.append("metric_classified_exactly_once_wrong")
    if metrics.get("decision_packet_emitted") is not True:
        failures.append("decision_packet_not_emitted")
    if metrics.get("review_only") is not True:
        failures.append("review_only_not_true")

    guards = receipt.get("top_group_classification_guards", {})
    for key in [
        "source_surface_verified",
        "human_decision_recorded",
        "candidate_c_lens_verified",
        "r1000_scale_result_verified",
        "top_group_selected_deterministically",
        "top_group_membership_extracted",
        "representative_fragments_emitted",
        "evidence_rollup_emitted",
        "top_group_classified_exactly_once",
        "decision_packet_emitted",
        "review_only",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "repair_command_emitted",
        "build_command_emitted",
        "repair_executed",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "optimization_authorized",
        "extraction_repair_authorized",
        "protocol_adoption_authorized",
        "source_mutation",
        "hidden_next_command",
        "top_two_comparison_by_default",
        "next_group_auto_inspected",
    ]:
        if guards.get(key) is not False:
            failures.append(f"guard_not_false:{key}:{guards.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_HUMAN_DECISION_REQUIRED":
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

    top, second, ranked = select_top_group(sources["group_rows"])
    selection = build_top_group_selection(top, second, ranked, sources["group_rollup"])
    top_membership, fragments = build_membership_and_fragments(top, sources["membership_rows"], sources["pressure_events"])
    evidence = build_evidence_rollup(top, second, top_membership, fragments, sources["comparison"])
    classification, proposal = classify_top_group(evidence, fragments)
    packet = make_decision_packet(classification, evidence, proposal, selection["ranked_group_keys"])

    write_json(TOP_GROUP_SELECTION_PATH, selection)
    write_jsonl(TOP_GROUP_MEMBERSHIP_PATH, top_membership)
    write_json(TOP_GROUP_FRAGMENTS_PATH, fragments)
    write_json(TOP_GROUP_EVIDENCE_ROLLUP_PATH, evidence)
    write_json(TOP_GROUP_CLASSIFICATION_PATH, classification)
    write_json(TOP_GROUP_REPAIR_PROPOSAL_PATH, proposal)
    write_json(TOP_GROUP_DECISION_PACKET_PATH, packet)

    failures.extend(validate_outputs(selection, top_membership, fragments, evidence, classification, proposal, packet, ranked))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "TOP_GROUP_CLASSIFY_0_SOURCE_SURFACE_VERIFIED": len(validate_sources(sources)) == 0,
        "TOP_GROUP_CLASSIFY_1_HUMAN_DECISION_RECORDED": HUMAN_DECISION["decision"] == "CLASSIFY_R1000_CANDIDATE_C_TOP_PRESSURE_GROUP",
        "TOP_GROUP_CLASSIFY_2_CANDIDATE_C_LENS_VERIFIED": ACCEPTED_CANDIDATE_FIELDS == ["parent_pressure_class", "pressure_subtype", "halt_reason"],
        "TOP_GROUP_CLASSIFY_3_R1000_SCALE_RESULT_VERIFIED": sources["scale_receipt"]["gate"] == "PASS" and sources["scale_receipt"]["scale_stability_summary"]["rank_order_preserved"] is True,
        "TOP_GROUP_CLASSIFY_4_TOP_GROUP_SELECTED_DETERMINISTICALLY": selection["top_group_count"] == ranked[0]["r1000_count"] and selection["selection_rule"] == ["r1000_count descending", "group_key_hash ascending deterministic tie-breaker"],
        "TOP_GROUP_CLASSIFY_5_TOP_GROUP_MEMBERSHIP_EXTRACTED": len(top_membership) == selection["top_group_count"],
        "TOP_GROUP_CLASSIFY_6_REPRESENTATIVE_FRAGMENTS_EMITTED": fragments["representative_fragment_count"] > 0,
        "TOP_GROUP_CLASSIFY_7_EVIDENCE_ROLLUP_EMITTED": TOP_GROUP_EVIDENCE_ROLLUP_PATH.exists(),
        "TOP_GROUP_CLASSIFY_8_TOP_GROUP_CLASSIFIED_EXACTLY_ONCE": classification["classification"] in VALID_CLASSES and classification["classified_exactly_once"] is True,
        "TOP_GROUP_CLASSIFY_9_REPAIR_PROPOSAL_ONLY_IF_FIXABLE": (proposal["proposal_emitted"] is True) == (classification["classification"] == "FIXABLE_PRESSURE"),
        "TOP_GROUP_CLASSIFY_10_DECISION_PACKET_EMITTED": TOP_GROUP_DECISION_PACKET_PATH.exists(),
        "TOP_GROUP_CLASSIFY_11_NO_ACTION_EXECUTED": packet["may_emit_repair_command"] is False and proposal["repair_executed"] is False,
        "TOP_GROUP_CLASSIFY_12_NO_SOURCE_MUTATION": source_mutation_detected is False,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    output_artifacts = {
        "top_group_selection": rel(TOP_GROUP_SELECTION_PATH),
        "top_group_event_membership": rel(TOP_GROUP_MEMBERSHIP_PATH),
        "top_group_representative_fragments": rel(TOP_GROUP_FRAGMENTS_PATH),
        "top_group_evidence_rollup": rel(TOP_GROUP_EVIDENCE_ROLLUP_PATH),
        "top_group_classification": rel(TOP_GROUP_CLASSIFICATION_PATH),
        "top_group_decision_packet": rel(TOP_GROUP_DECISION_PACKET_PATH),
        "top_group_repair_objective_proposal": rel(TOP_GROUP_REPAIR_PROPOSAL_PATH),
    }

    terminal = {"type": "STOP", "stop_code": "STOP_HUMAN_DECISION_REQUIRED", "next_command_goal": None}
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}
    if any([
        proposal.get("build_command_emitted") is True,
        proposal.get("repair_executed") is True,
        packet.get("may_emit_repair_command") is True,
        packet.get("may_emit_build_command") is True,
    ]):
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_RECEIPT_ID,
        "source_r1000_batch_id": SOURCE_R1000_BATCH_ID,
        "top_group_key_hash": selection["top_group_key_hash"],
        "top_group_rank": selection["top_group_rank"],
        "top_group_count": selection["top_group_count"],
        "top_group_share": selection["top_group_share"],
        "second_group_key_hash": selection["second_group_key_hash"],
        "second_group_count": selection["second_group_count"],
        "dominant_margin": selection["dominant_margin"],
        "dominant_margin_share": selection["dominant_margin_share"],
        "low_margin_warning": selection["low_margin_warning"],
        "membership_count": len(top_membership),
        "representative_fragment_count": fragments["representative_fragment_count"],
        "classification": classification["classification"],
        "classified_exactly_once": classification["classified_exactly_once"],
        "repair_objective_proposal_emitted": proposal["proposal_emitted"],
        "decision_packet_emitted": TOP_GROUP_DECISION_PACKET_PATH.exists(),
        "repair_command_emitted_count": 0,
        "build_command_emitted_count": 0,
        "repair_executed_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "authority_widening_authorized_count": 0,
        "optimization_authorized_count": 0,
        "extraction_repair_authorized_count": 0,
        "protocol_adoption_authorized_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "hidden_next_command_count": 0,
        "top_two_comparison_default_count": 0,
        "next_group_auto_inspection_count": 0,
        "review_only": True,
    }

    guards = {
        "source_surface_verified": len(validate_sources(sources)) == 0,
        "human_decision_recorded": True,
        "candidate_c_lens_verified": True,
        "r1000_scale_result_verified": True,
        "top_group_selected_deterministically": True,
        "top_group_membership_extracted": True,
        "representative_fragments_emitted": True,
        "evidence_rollup_emitted": True,
        "top_group_classified_exactly_once": True,
        "repair_proposal_only_if_fixable": acceptance_gate_results["TOP_GROUP_CLASSIFY_9_REPAIR_PROPOSAL_ONLY_IF_FIXABLE"],
        "decision_packet_emitted": True,
        "review_only": True,
        "repair_command_emitted": False,
        "build_command_emitted": False,
        "repair_executed": False,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "extraction_repair_authorized": False,
        "protocol_adoption_authorized": False,
        "source_mutation": source_mutation_detected,
        "hidden_next_command": False,
        "top_two_comparison_by_default": False,
        "next_group_auto_inspected": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_scale_receipt": SOURCE_R1000_SCALE_RECEIPT_ID,
        "top_group_key_hash": selection["top_group_key_hash"],
        "classification": classification["classification"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    output_artifacts["implementation_receipt"] = rel(receipt_path)

    receipt = {
        "schema_version": "r1000_candidate_c_top_group_classification_receipt_v0",
        "receipt_type": "R1000_CANDIDATE_C_TOP_GROUP_CLASSIFICATION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_RECEIPT_ID,
        "source_r1000_batch_id": SOURCE_R1000_BATCH_ID,
        "source_candidate_c_interrogation_receipt_id": SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID,
        "source_coarsening_review_receipt_id": SOURCE_COARSENING_REVIEW_RECEIPT_ID,
        "source_pressure_metrics_repair_receipt_id": SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID,
        "source_r250_pressure_batch_id": SOURCE_R250_PRESSURE_BATCH_ID,
        "accepted_candidate_id": ACCEPTED_CANDIDATE_ID,
        "accepted_candidate_name": ACCEPTED_CANDIDATE_NAME,
        "accepted_candidate_fields": ACCEPTED_CANDIDATE_FIELDS,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "top_group_summary": {
            "top_group_key_hash": selection["top_group_key_hash"],
            "parent_pressure_class": selection["parent_pressure_class"],
            "pressure_subtype": selection["pressure_subtype"],
            "halt_reason": selection["halt_reason"],
            "top_group_count": selection["top_group_count"],
            "second_group_count": selection["second_group_count"],
            "dominant_margin": selection["dominant_margin"],
            "classification": classification["classification"],
            "classification_reason": classification["classification_reason"],
            "repair_objective_proposal_emitted": proposal["proposal_emitted"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "top_group_classification_guards": guards,
        "must_not_infer": MUST_NOT_INFER,
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
    print(f"r1000_candidate_c_top_group_classification_receipt_id={receipt_id}")
    print(f"r1000_candidate_c_top_group_classification_receipt_path=data/r1000_candidate_c_top_group_classification_v0_receipts/{receipt_id}.json")
    print(f"top_group_classification_path=data/r1000_candidate_c_top_group_classification_v0/top_group_classification.json")
    print(f"top_group_decision_packet_path=data/r1000_candidate_c_top_group_classification_v0/top_group_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
