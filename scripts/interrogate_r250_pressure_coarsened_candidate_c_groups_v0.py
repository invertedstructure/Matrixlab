#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "INTERROGATE_R250_PRESSURE_COARSENED_CANDIDATE_C_GROUPS_V0"
TARGET_UNIT_ID = "r250_pressure_coarsened_candidate_c_interrogation.v0"

SOURCE_COARSENING_REVIEW_RECEIPT_ID = "f03689e3"
SOURCE_PD_INTERROGATION_RECEIPT_ID = "1f934d51"
SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID = "f09b8395"
SOURCE_FAILED_PRESSURE_METRICS_RECEIPT_ID_OPTIONAL = "8b82d6a8"
SOURCE_R250_IMPLEMENTATION_RECEIPT_ID = "05723444"
SOURCE_R250_INTERROGATION_RECEIPT_ID = "41f65b9a"
SOURCE_R250_POLICY_ID = "44ee648b"
SOURCE_RECEIPT_INTERROGATION_ADAPTER_RECEIPT_ID = "a785297c"
SOURCE_RECEIPT_INTERROGATION_POLICY_ID = "2aa2f2f3"
SOURCE_CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID = "98ab6f11"

SOURCE_PRESSURE_BATCH_ID = "r250_pressure_metrics_batch_1095f5c6"
SOURCE_PREVIOUS_R250_BATCH_ID = "r250_batch_34f560c1"

ACCEPTED_COARSENING_CANDIDATE_ID = "C"
ACCEPTED_COARSENING_CANDIDATE_NAME = "parent_plus_subtype_plus_halt_reason"
ACCEPTED_COARSENING_FIELDS = ["parent_pressure_class", "pressure_subtype", "halt_reason"]

SOURCE_COARSENING_RECEIPT_PATH = ROOT / "data" / "r250_pressure_coarsening_review_v0_receipts" / f"{SOURCE_COARSENING_REVIEW_RECEIPT_ID}.json"
SOURCE_COARSENING_CANDIDATE_SCHEMA_PATH = ROOT / "data" / "r250_pressure_coarsening_review_v0" / "coarsening_candidate_schema_v0.json"
SOURCE_COARSENED_SIGNATURE_SCHEMA_PATH = ROOT / "data" / "r250_pressure_coarsening_review_v0" / "coarsened_signature_schema_v0.json"
SOURCE_COARSENING_GUARD_SCHEMA_PATH = ROOT / "data" / "r250_pressure_coarsening_review_v0" / "coarsening_review_guard_schema_v0.json"
SOURCE_COARSENED_EVENT_ROWS_PATH = ROOT / "data" / "r250_pressure_coarsening_review_v0" / "coarsened_pressure_event_rows.jsonl"
SOURCE_COARSENING_CANDIDATE_ROLLUPS_PATH = ROOT / "data" / "r250_pressure_coarsening_review_v0" / "coarsening_candidate_rollups.json"
SOURCE_COARSENING_COMPARISON_MATRIX_PATH = ROOT / "data" / "r250_pressure_coarsening_review_v0" / "coarsening_comparison_matrix.json"
SOURCE_COARSENING_OBSERVER_BURDEN_PATH = ROOT / "data" / "r250_pressure_coarsening_review_v0" / "coarsening_observer_burden_rollup.json"
SOURCE_COARSENING_REPORT_PATH = ROOT / "data" / "r250_pressure_coarsening_review_v0" / "r250_pressure_coarsening_review_report.json"
SOURCE_COARSENING_PACKET_PATH = ROOT / "data" / "r250_pressure_coarsening_review_v0" / "r250_pressure_coarsening_review_packet.json"

SOURCE_PD_INTERROGATION_RECEIPT_PATH = ROOT / "data" / "r250_pressure_decomposed_interrogation_receipts" / f"{SOURCE_PD_INTERROGATION_RECEIPT_ID}.json"
SOURCE_PD_INTERROGATION_REPORT_PATH = ROOT / "data" / "r250_pressure_decomposed_interrogations" / "r250_pressure_decomposed_interrogation_report.json"
SOURCE_FRAGMENTATION_QUESTION_PACKET_PATH = ROOT / "data" / "r250_pressure_decomposed_interrogations" / "r250_pressure_fragmentation_question_packet.json"
SOURCE_PRESSURE_METRICS_RECEIPT_PATH = ROOT / "data" / "r250_pressure_metrics_v0_receipts" / f"{SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID}.json"
OPTIONAL_FAILED_PRESSURE_METRICS_RECEIPT_PATH = ROOT / "data" / "r250_pressure_metrics_v0_receipts" / f"{SOURCE_FAILED_PRESSURE_METRICS_RECEIPT_ID_OPTIONAL}.json"

SOURCE_PRESSURE_EVENT_ROWS_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "pressure_event_rows.jsonl"
SOURCE_PRESSURE_DECOMPOSITION_ROLLUP_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "pressure_decomposition_rollup.json"
SOURCE_PRESSURE_SIGNATURE_ROLLUP_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "pressure_signature_repetition_rollup.json"
SOURCE_OBSERVER_BURDEN_ROLLUP_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "observer_burden_rollup.json"
SOURCE_RUNTIME_EQUIVALENCE_REPORT_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "runtime_equivalence_report.json"
SOURCE_PRESSURE_BATCH_ROLLUP_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "r250_pressure_metrics_batch_rollup.json"
SOURCE_PRESSURE_INTERROGATION_READY_INDEX_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "r250_pressure_metrics_interrogation_ready_index.json"

SOURCE_R250_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "closure_radius_real_batch_receipts" / f"{SOURCE_R250_IMPLEMENTATION_RECEIPT_ID}.json"
SOURCE_R250_INTERROGATION_RECEIPT_PATH = ROOT / "data" / "closure_radius_real_batch_interrogation_receipts" / f"{SOURCE_R250_INTERROGATION_RECEIPT_ID}.json"
SOURCE_R250_POLICY_PATH = ROOT / "data" / "closure_radius_real_batch_r250_collection_v0_policies" / f"{SOURCE_R250_POLICY_ID}.json"
SOURCE_RIA_RECEIPT_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0_implementation_receipts" / f"{SOURCE_RECEIPT_INTERROGATION_ADAPTER_RECEIPT_ID}.json"
SOURCE_RIA_POLICY_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0_policies" / f"{SOURCE_RECEIPT_INTERROGATION_POLICY_ID}.json"
SOURCE_CLOSURE_RADIUS_RECEIPT_PATH = ROOT / "data" / "closure_radius_metrics_v0_implementation_receipts" / f"{SOURCE_CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID}.json"

SOURCE_FILES = [
    SOURCE_COARSENING_RECEIPT_PATH,
    SOURCE_COARSENING_CANDIDATE_SCHEMA_PATH,
    SOURCE_COARSENED_SIGNATURE_SCHEMA_PATH,
    SOURCE_COARSENING_GUARD_SCHEMA_PATH,
    SOURCE_COARSENED_EVENT_ROWS_PATH,
    SOURCE_COARSENING_CANDIDATE_ROLLUPS_PATH,
    SOURCE_COARSENING_COMPARISON_MATRIX_PATH,
    SOURCE_COARSENING_OBSERVER_BURDEN_PATH,
    SOURCE_COARSENING_REPORT_PATH,
    SOURCE_COARSENING_PACKET_PATH,
    SOURCE_PD_INTERROGATION_RECEIPT_PATH,
    SOURCE_PD_INTERROGATION_REPORT_PATH,
    SOURCE_FRAGMENTATION_QUESTION_PACKET_PATH,
    SOURCE_PRESSURE_METRICS_RECEIPT_PATH,
    SOURCE_PRESSURE_EVENT_ROWS_PATH,
    SOURCE_PRESSURE_DECOMPOSITION_ROLLUP_PATH,
    SOURCE_PRESSURE_SIGNATURE_ROLLUP_PATH,
    SOURCE_OBSERVER_BURDEN_ROLLUP_PATH,
    SOURCE_RUNTIME_EQUIVALENCE_REPORT_PATH,
    SOURCE_PRESSURE_BATCH_ROLLUP_PATH,
    SOURCE_PRESSURE_INTERROGATION_READY_INDEX_PATH,
    SOURCE_R250_IMPLEMENTATION_RECEIPT_PATH,
    SOURCE_R250_INTERROGATION_RECEIPT_PATH,
    SOURCE_R250_POLICY_PATH,
    SOURCE_RIA_RECEIPT_PATH,
    SOURCE_RIA_POLICY_PATH,
    SOURCE_CLOSURE_RADIUS_RECEIPT_PATH,
]

OUT_DIR = ROOT / "data" / "r250_pressure_candidate_c_interrogation_v0"
RECEIPT_DIR = ROOT / "data" / "r250_pressure_candidate_c_interrogation_v0_receipts"

GROUP_SCHEMA_PATH = OUT_DIR / "candidate_c_group_schema_v0.json"
GROUP_ROWS_PATH = OUT_DIR / "candidate_c_group_rows.jsonl"
GROUP_EVENT_MEMBERSHIP_PATH = OUT_DIR / "candidate_c_group_event_membership.jsonl"
GROUP_INTERROGATION_ROLLUP_PATH = OUT_DIR / "candidate_c_group_interrogation_rollup.json"
GROUP_REPRESENTATIVE_FRAGMENTS_PATH = OUT_DIR / "candidate_c_representative_fragments.json"
GROUP_INTERROGATION_REPORT_PATH = OUT_DIR / "r250_candidate_c_group_interrogation_report.json"
GROUP_REVIEW_PACKET_PATH = OUT_DIR / "r250_candidate_c_group_review_packet.json"
OBSERVER_BURDEN_PATH = OUT_DIR / "candidate_c_interrogation_observer_burden.json"

VALID_GROUP_CLASSES = {
    "REPEATED_GROUP_REVIEW_SIGNAL",
    "SINGLETON_RESIDUE",
    "DOMINANT_BUT_LOW_MARGIN_GROUP",
    "REVIEW_LAYER_ACCEPTED_FOR_INTERROGATION_ONLY",
}

MUST_NOT_INFER = [
    "do not infer taxonomy upgrade",
    "do not infer authority expansion",
    "do not infer burden optimization",
    "do not infer extraction repair",
    "do not emit command from candidate C",
    "do not emit proposal from candidate C",
    "do not claim Candidate C is accepted as taxonomy",
    "do not claim Candidate C proves causality",
    "do not claim parent pressure is dominant enough for action",
    "do not overwrite exact signatures",
    "do not rerun runtime",
    "do not claim roadmap",
]

HUMAN_DECISION = {
    "accepted_review_packet_choice": "ACCEPT_COARSENING_LAYER_FOR_NEXT_INTERROGATION",
    "accepted_candidate_id": ACCEPTED_COARSENING_CANDIDATE_ID,
    "accepted_candidate_name": ACCEPTED_COARSENING_CANDIDATE_NAME,
    "scope": "interrogation_lens_only",
    "not_authorized": [
        "taxonomy_upgrade",
        "authority_widening",
        "burden_optimization",
        "extraction_repair",
        "objective_proposal",
        "build_command",
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
    result = subprocess.run(["git", "ls-files", "--error-unmatch", rel(path)], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def load_sources() -> Dict[str, Any]:
    return {
        "coarsening_receipt": read_json(SOURCE_COARSENING_RECEIPT_PATH),
        "coarsening_candidate_schema": read_json(SOURCE_COARSENING_CANDIDATE_SCHEMA_PATH),
        "coarsened_signature_schema": read_json(SOURCE_COARSENED_SIGNATURE_SCHEMA_PATH),
        "coarsening_guard_schema": read_json(SOURCE_COARSENING_GUARD_SCHEMA_PATH),
        "coarsened_rows": read_jsonl(SOURCE_COARSENED_EVENT_ROWS_PATH),
        "coarsening_rollups": read_json(SOURCE_COARSENING_CANDIDATE_ROLLUPS_PATH),
        "coarsening_comparison": read_json(SOURCE_COARSENING_COMPARISON_MATRIX_PATH),
        "coarsening_observer": read_json(SOURCE_COARSENING_OBSERVER_BURDEN_PATH),
        "coarsening_report": read_json(SOURCE_COARSENING_REPORT_PATH),
        "coarsening_packet": read_json(SOURCE_COARSENING_PACKET_PATH),
        "pd_receipt": read_json(SOURCE_PD_INTERROGATION_RECEIPT_PATH),
        "pressure_receipt": read_json(SOURCE_PRESSURE_METRICS_RECEIPT_PATH),
        "pressure_events": read_jsonl(SOURCE_PRESSURE_EVENT_ROWS_PATH),
        "runtime_report": read_json(SOURCE_RUNTIME_EQUIVALENCE_REPORT_PATH),
        "pressure_batch_rollup": read_json(SOURCE_PRESSURE_BATCH_ROLLUP_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    receipt = sources["coarsening_receipt"]
    rollups_doc = sources["coarsening_rollups"]
    packet = sources["coarsening_packet"]
    report = sources["coarsening_report"]
    coarsened_rows = sources["coarsened_rows"]
    pd_receipt = sources["pd_receipt"]
    pressure_receipt = sources["pressure_receipt"]
    runtime = sources["runtime_report"]
    pressure_batch = sources["pressure_batch_rollup"]

    if receipt.get("receipt_id") != SOURCE_COARSENING_REVIEW_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("coarsening_review_receipt_not_pass")
    if receipt.get("terminal", {}).get("type") != "STOP":
        failures.append("coarsening_terminal_not_stop")
    if receipt.get("terminal", {}).get("stop_code") != "STOP_HUMAN_DECISION_REQUIRED":
        failures.append("coarsening_stop_code_wrong")
    if receipt.get("source_r250_pressure_decomposed_interrogation_receipt_id") != SOURCE_PD_INTERROGATION_RECEIPT_ID:
        failures.append("coarsening_source_pd_wrong")
    if receipt.get("source_r250_pressure_metrics_repair_receipt_id") != SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID:
        failures.append("coarsening_source_pressure_metrics_wrong")

    metrics = receipt.get("aggregate_metrics", {})
    expected = {
        "source_pressure_event_count": 23,
        "exact_unique_pattern_signature_count": 23,
        "exact_repeated_pattern_count": 0,
        "exact_fragmentation_ratio": 1.0,
        "coarsening_candidate_count": 6,
        "coarsened_event_row_count": 138,
        "best_candidate_id": ACCEPTED_COARSENING_CANDIDATE_ID,
        "best_candidate_status": "PROMISING_REVIEW_LAYER",
        "candidate_a_baseline_only": True,
        "candidate_c_center_candidate": True,
        "candidate_f_invalid_without_family_rules": True,
        "coarsening_produced_repeated_groups": True,
        "coarsening_produced_dominant_group": True,
        "review_packet_emitted": True,
        "review_only": True,
        "runtime_behavior_changed_count": 0,
        "repair_authorized_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "authority_widening_authorized_count": 0,
        "optimization_authorized_count": 0,
        "command_authorized_count": 0,
        "proposal_authorized_count": 0,
        "roadmap_invented_count": 0,
        "proof_claim_count": 0,
        "source_mutation_count": 0,
        "sqlite_registry_write_count": 0,
        "exact_signature_overwrite_count": 0,
        "instance_identity_in_coarsened_signature_count": 0,
    }
    for key, value in expected.items():
        if metrics.get(key) != value:
            failures.append(f"coarsening_metric_wrong:{key}:{metrics.get(key)} expected {value}")

    best = receipt.get("review_summary", {}).get("best_candidate") or {}
    if best.get("candidate_id") != ACCEPTED_COARSENING_CANDIDATE_ID:
        failures.append("best_candidate_not_C")
    if best.get("review_status") != "PROMISING_REVIEW_LAYER":
        failures.append("candidate_C_not_promising")
    if best.get("coarsening_fields") != ACCEPTED_COARSENING_FIELDS:
        failures.append("candidate_C_fields_wrong")
    if best.get("command_authorized") is not False:
        failures.append("candidate_C_command_authorized")
    if best.get("proposal_authorized") is not False:
        failures.append("candidate_C_proposal_authorized")
    if best.get("review_only") is not True:
        failures.append("candidate_C_not_review_only")

    if packet.get("packet_type") != "HUMAN_REVIEW_PACKET_NOT_COMMAND":
        failures.append("coarsening_packet_type_wrong")
    if "ACCEPT_COARSENING_LAYER_FOR_NEXT_INTERROGATION" not in packet.get("allowed_human_choices", []):
        failures.append("accept_choice_missing")
    for key in [
        "may_emit_build_command",
        "may_emit_objective_proposal",
        "may_authorize_taxonomy_upgrade",
        "may_authorize_authority_widening",
        "may_authorize_optimization",
    ]:
        if packet.get(key) is not False:
            failures.append(f"packet_guard_not_false:{key}:{packet.get(key)}")

    if report.get("command_authorized") is not False:
        failures.append("coarsening_report_command_authorized")
    if report.get("proposal_authorized") is not False:
        failures.append("coarsening_report_proposal_authorized")
    if report.get("taxonomy_upgrade_authorized") is not False:
        failures.append("coarsening_report_taxonomy_upgrade")
    if report.get("authority_widening_authorized") is not False:
        failures.append("coarsening_report_authority_widening")
    if report.get("optimization_authorized") is not False:
        failures.append("coarsening_report_optimization")

    if pd_receipt.get("receipt_id") != SOURCE_PD_INTERROGATION_RECEIPT_ID or pd_receipt.get("gate") != "PASS":
        failures.append("pd_receipt_not_pass")
    if pressure_receipt.get("receipt_id") != SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID or pressure_receipt.get("gate") != "PASS":
        failures.append("pressure_receipt_not_pass")
    if runtime.get("runtime_behavior_changed_count") != 0:
        failures.append("runtime_behavior_changed_source")
    if pressure_batch.get("interrogation_ready") is not True:
        failures.append("pressure_batch_not_ready")

    candidate_c_rows = [row for row in coarsened_rows if row.get("coarsening_candidate_id") == ACCEPTED_COARSENING_CANDIDATE_ID]
    if len(candidate_c_rows) != 23:
        failures.append(f"candidate_C_row_count_wrong:{len(candidate_c_rows)}")
    for row in candidate_c_rows:
        if row.get("coarsening_fields_used") != ACCEPTED_COARSENING_FIELDS:
            failures.append(f"candidate_C_row_fields_wrong:{row.get('pressure_event_id')}")
        if row.get("candidate_available") is not True:
            failures.append(f"candidate_C_row_unavailable:{row.get('pressure_event_id')}")
        if row.get("exact_signature_overwritten") is not False:
            failures.append(f"candidate_C_exact_signature_overwritten:{row.get('pressure_event_id')}")
        if row.get("instance_identity_used_in_signature") is not False:
            failures.append(f"candidate_C_instance_identity_used:{row.get('pressure_event_id')}")
        if row.get("build_command") is not None:
            failures.append(f"candidate_C_build_command_present:{row.get('pressure_event_id')}")
        for key in [
            "proposal_authorized",
            "repair_authorized",
            "taxonomy_upgrade_authorized",
            "authority_widening_authorized",
            "optimization_authorized",
            "runtime_rerun",
        ]:
            if row.get(key) is not False:
                failures.append(f"candidate_C_guard_not_false:{row.get('pressure_event_id')}:{key}:{row.get(key)}")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def make_group_schema() -> Dict[str, Any]:
    return {
        "schema_version": "candidate_c_group_schema_v0",
        "accepted_candidate_id": ACCEPTED_COARSENING_CANDIDATE_ID,
        "accepted_candidate_name": ACCEPTED_COARSENING_CANDIDATE_NAME,
        "accepted_fields": ACCEPTED_COARSENING_FIELDS,
        "required_group_fields": [
            "group_id",
            "coarsened_signature_hash",
            "coarsening_payload",
            "event_count",
            "original_exact_signature_count",
            "parent_pressure_class",
            "pressure_subtype",
            "halt_reason",
            "move_kind_distribution",
            "evidence_field_distribution",
            "source_event_ids",
            "classification",
            "recommended_review_focus",
        ],
        "forbidden_authorizations": [
            "command",
            "proposal",
            "taxonomy_upgrade",
            "authority_widening",
            "optimization",
            "repair",
        ],
        "review_only": True,
    }

def group_candidate_c_rows(sources: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    rows = [row for row in sources["coarsened_rows"] if row.get("coarsening_candidate_id") == ACCEPTED_COARSENING_CANDIDATE_ID]
    by_hash: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_hash[row["coarsened_signature_hash"]].append(row)

    group_rows = []
    membership_rows = []

    for coarsened_hash, group in sorted(by_hash.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        payload = group[0]["coarsening_payload"]
        event_count = len(group)
        exact_sigs = sorted({r["original_pressure_pattern_signature_hash"] for r in group})
        move_dist = dict(sorted(Counter(r.get("move_kind") for r in group).items(), key=lambda kv: str(kv[0])))
        evidence_dist = dict(sorted(Counter(r.get("evidence_field") for r in group).items(), key=lambda kv: str(kv[0])))
        event_ids = sorted(r["pressure_event_id"] for r in group)

        if event_count == 1:
            classification = "SINGLETON_RESIDUE"
            recommended_focus = "inspect representative fragment only if human wants singleton residue detail"
        elif event_count >= 7:
            classification = "DOMINANT_BUT_LOW_MARGIN_GROUP"
            recommended_focus = "review dominant repeated group while preserving low-margin warning"
        else:
            classification = "REPEATED_GROUP_REVIEW_SIGNAL"
            recommended_focus = "review repeated group as signal, not repair authorization"

        group_id = f"candidate_c_group_{sha8({'hash': coarsened_hash, 'payload': payload})}"
        group_row = {
            "schema_version": "candidate_c_group_row_v0",
            "group_id": group_id,
            "coarsened_signature_hash": coarsened_hash,
            "coarsening_candidate_id": ACCEPTED_COARSENING_CANDIDATE_ID,
            "coarsening_candidate_name": ACCEPTED_COARSENING_CANDIDATE_NAME,
            "coarsening_fields": ACCEPTED_COARSENING_FIELDS,
            "coarsening_payload": payload,
            "event_count": event_count,
            "original_exact_signature_count": len(exact_sigs),
            "original_exact_signature_hashes": exact_sigs,
            "parent_pressure_class": payload.get("parent_pressure_class"),
            "pressure_subtype": payload.get("pressure_subtype"),
            "halt_reason": payload.get("halt_reason"),
            "move_kind_distribution": move_dist,
            "evidence_field_distribution": evidence_dist,
            "source_event_ids": event_ids,
            "classification": classification,
            "recommended_review_focus": recommended_focus,
            "command_authorized": False,
            "proposal_authorized": False,
            "taxonomy_upgrade_authorized": False,
            "authority_widening_authorized": False,
            "optimization_authorized": False,
            "repair_authorized": False,
            "runtime_rerun": False,
            "review_only": True,
        }
        group_rows.append(group_row)

        for member in group:
            membership_rows.append({
                "schema_version": "candidate_c_group_event_membership_v0",
                "group_id": group_id,
                "coarsened_signature_hash": coarsened_hash,
                "pressure_event_id": member["pressure_event_id"],
                "original_pressure_pattern_signature_hash": member["original_pressure_pattern_signature_hash"],
                "work_item_id": member["work_item_id"],
                "slot_id": member["slot_id"],
                "source_receipt_ref": member["source_receipt_ref"],
                "source_trace_ref": member["source_trace_ref"],
                "move_kind": member["move_kind"],
                "evidence_field": member["evidence_field"],
                "review_only": True,
            })

    return group_rows, membership_rows

def make_representative_fragments(group_rows: List[Dict[str, Any]], membership_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    members_by_group: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in membership_rows:
        members_by_group[row["group_id"]].append(row)

    fragments = []
    for group in group_rows:
        members = sorted(members_by_group[group["group_id"]], key=lambda row: (row["slot_id"], row["work_item_id"], row["pressure_event_id"]))
        fragments.append({
            "group_id": group["group_id"],
            "coarsened_signature_hash": group["coarsened_signature_hash"],
            "classification": group["classification"],
            "event_count": group["event_count"],
            "coarsening_payload": group["coarsening_payload"],
            "representative_event": members[0] if members else None,
            "member_sample_size": min(3, len(members)),
            "member_sample": members[:3],
            "review_only": True,
        })

    return {
        "schema_version": "candidate_c_representative_fragments_v0",
        "accepted_candidate_id": ACCEPTED_COARSENING_CANDIDATE_ID,
        "fragment_count": len(fragments),
        "fragments": fragments,
        "review_only": True,
    }

def validate_group_row(row: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    required = [
        "group_id",
        "coarsened_signature_hash",
        "coarsening_candidate_id",
        "coarsening_candidate_name",
        "coarsening_fields",
        "coarsening_payload",
        "event_count",
        "original_exact_signature_count",
        "original_exact_signature_hashes",
        "parent_pressure_class",
        "pressure_subtype",
        "halt_reason",
        "move_kind_distribution",
        "evidence_field_distribution",
        "source_event_ids",
        "classification",
        "recommended_review_focus",
    ]
    for key in required:
        if key not in row:
            failures.append(f"group_field_missing:{key}")

    if row.get("coarsening_candidate_id") != ACCEPTED_COARSENING_CANDIDATE_ID:
        failures.append("group_candidate_not_C")
    if row.get("coarsening_fields") != ACCEPTED_COARSENING_FIELDS:
        failures.append("group_fields_not_C")
    if row.get("classification") not in VALID_GROUP_CLASSES:
        failures.append(f"group_class_invalid:{row.get('classification')}")
    if row.get("event_count", 0) != len(row.get("source_event_ids", [])):
        failures.append("group_event_count_mismatch")
    if row.get("original_exact_signature_count", 0) != len(row.get("original_exact_signature_hashes", [])):
        failures.append("group_exact_signature_count_mismatch")

    for key in [
        "command_authorized",
        "proposal_authorized",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "optimization_authorized",
        "repair_authorized",
        "runtime_rerun",
    ]:
        if row.get(key) is not False:
            failures.append(f"group_guard_not_false:{key}:{row.get(key)}")
    if row.get("review_only") is not True:
        failures.append("group_not_review_only")
    return failures

def validate_outputs(group_rows: List[Dict[str, Any]], membership_rows: List[Dict[str, Any]], fragments: Dict[str, Any], rollup: Dict[str, Any], report: Dict[str, Any], packet: Dict[str, Any], observer: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if len(group_rows) != 5:
        failures.append(f"group_count_wrong:{len(group_rows)}")
    if len(membership_rows) != 23:
        failures.append(f"membership_count_wrong:{len(membership_rows)}")
    if sum(group["event_count"] for group in group_rows) != 23:
        failures.append("group_event_total_wrong")
    group_size_profile = sorted((group["event_count"] for group in group_rows), reverse=True)
    if sum(group_size_profile) != 23:
        failures.append(f"group_size_profile_total_wrong:{group_size_profile}")
    if len(group_size_profile) != 5:
        failures.append(f"group_size_profile_group_count_wrong:{group_size_profile}")
    if group_size_profile[0] != 7:
        failures.append(f"group_size_profile_dominant_wrong:{group_size_profile}")
    if group_size_profile[1] != 6:
        failures.append(f"group_size_profile_second_wrong:{group_size_profile}")
    if group_size_profile[0] - group_size_profile[1] != 1:
        failures.append(f"group_size_profile_margin_wrong:{group_size_profile}")
    if sum(1 for count in group_size_profile if count > 1) != 4:
        failures.append(f"group_size_profile_repeated_count_wrong:{group_size_profile}")
    if sum(1 for count in group_size_profile if count == 1) != 1:
        failures.append(f"group_size_profile_singleton_count_wrong:{group_size_profile}")

    for group in group_rows:
        failures.extend([f"{group.get('group_id')}:{f}" for f in validate_group_row(group)])

    membership_event_ids = [row["pressure_event_id"] for row in membership_rows]
    if len(set(membership_event_ids)) != 23:
        failures.append("membership_event_ids_not_unique")
    for row in membership_rows:
        if row.get("review_only") is not True:
            failures.append(f"membership_not_review_only:{row.get('pressure_event_id')}")
        if not row.get("original_pressure_pattern_signature_hash"):
            failures.append(f"membership_missing_exact_signature:{row.get('pressure_event_id')}")

    if fragments.get("fragment_count") != len(group_rows):
        failures.append("fragment_count_wrong")
    if fragments.get("review_only") is not True:
        failures.append("fragments_not_review_only")

    expected_rollup = {
        "accepted_candidate_id": ACCEPTED_COARSENING_CANDIDATE_ID,
        "group_count": 5,
        "total_grouped_pressure_events": 23,
        "repeated_group_count": 4,
        "singleton_group_count": 1,
        "dominant_group_count": 7,
        "second_group_count": 6,
        "dominant_group_margin": 1,
        "dominant_group_share": 7 / 23,
        "coarsened_fragmentation_ratio": 5 / 23,
    }
    for key, value in expected_rollup.items():
        if rollup.get(key) != value:
            failures.append(f"rollup_wrong:{key}:{rollup.get(key)} expected {value}")
    if rollup.get("dominant_group_low_margin_warning") is not True:
        failures.append("dominant_low_margin_warning_missing")
    if rollup.get("candidate_c_interrogation_only") is not True:
        failures.append("candidate_c_interrogation_only_not_true")

    for key in [
        "command_authorized",
        "proposal_authorized",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "optimization_authorized",
        "repair_authorized",
        "runtime_behavior_changed",
    ]:
        if report.get(key) is not False:
            failures.append(f"report_guard_not_false:{key}:{report.get(key)}")

    if packet.get("packet_type") != "HUMAN_REVIEW_PACKET_NOT_COMMAND":
        failures.append("packet_type_wrong")
    for choice in [
        "ACCEPT_CANDIDATE_C_AS_INTERROGATION_LENS_ONLY",
        "INSPECT_DOMINANT_GROUP_MEMBERS",
        "INSPECT_SINGLETON_RESIDUE",
        "RUN_MORE_BATCH_EVIDENCE_WITH_CANDIDATE_C",
        "REJECT_CANDIDATE_C_KEEP_FRAGMENTATION_SIGNAL",
    ]:
        if choice not in packet.get("allowed_human_choices", []):
            failures.append(f"packet_choice_missing:{choice}")
    for key in [
        "may_emit_build_command",
        "may_emit_objective_proposal",
        "may_authorize_taxonomy_upgrade",
        "may_authorize_authority_widening",
        "may_authorize_optimization",
        "may_authorize_repair",
    ]:
        if packet.get(key) is not False:
            failures.append(f"packet_guard_not_false:{key}:{packet.get(key)}")

    for key in [
        "candidate_c_interrogation_bytes_total",
        "candidate_c_interrogation_bytes_per_group",
        "candidate_c_interrogation_wall_time_ms",
        "observer_burden_warning",
        "observer_burden_reason",
    ]:
        if key not in observer:
            failures.append(f"observer_field_missing:{key}")

    return failures

def build_outputs(sources: Dict[str, Any]) -> Dict[str, Any]:
    start = time.perf_counter()
    group_schema = make_group_schema()
    write_json(GROUP_SCHEMA_PATH, group_schema)

    group_rows, membership_rows = group_candidate_c_rows(sources)
    fragments = make_representative_fragments(group_rows, membership_rows)

    write_jsonl(GROUP_ROWS_PATH, group_rows)
    write_jsonl(GROUP_EVENT_MEMBERSHIP_PATH, membership_rows)
    write_json(GROUP_REPRESENTATIVE_FRAGMENTS_PATH, fragments)

    group_counts = sorted([group["event_count"] for group in group_rows], reverse=True)
    dominant_count = group_counts[0]
    second_count = group_counts[1] if len(group_counts) > 1 else 0
    repeated_count = sum(1 for count in group_counts if count > 1)
    singleton_count = sum(1 for count in group_counts if count == 1)

    rollup = {
        "schema_version": "candidate_c_group_interrogation_rollup_v0",
        "accepted_candidate_id": ACCEPTED_COARSENING_CANDIDATE_ID,
        "accepted_candidate_name": ACCEPTED_COARSENING_CANDIDATE_NAME,
        "accepted_coarsening_fields": ACCEPTED_COARSENING_FIELDS,
        "source_pressure_event_count": 23,
        "group_count": len(group_rows),
        "total_grouped_pressure_events": sum(group_counts),
        "group_size_profile": group_counts,
        "repeated_group_count": repeated_count,
        "singleton_group_count": singleton_count,
        "dominant_group_count": dominant_count,
        "second_group_count": second_count,
        "dominant_group_margin": dominant_count - second_count,
        "dominant_group_share": dominant_count / 23,
        "coarsened_fragmentation_ratio": len(group_rows) / 23,
        "dominant_group_low_margin_warning": dominant_count - second_count <= 1,
        "candidate_c_interrogation_only": True,
        "command_authorized": False,
        "proposal_authorized": False,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "repair_authorized": False,
        "review_only": True,
    }
    write_json(GROUP_INTERROGATION_ROLLUP_PATH, rollup)

    elapsed_ms = max(1, int((time.perf_counter() - start) * 1000))
    bytes_total = len(canonical_bytes({
        "group_schema": group_schema,
        "group_rows": group_rows,
        "membership_rows": membership_rows,
        "fragments": fragments,
        "rollup": rollup,
    }))
    observer = {
        "schema_version": "candidate_c_interrogation_observer_burden_v0",
        "candidate_c_interrogation_bytes_total": bytes_total,
        "candidate_c_interrogation_bytes_per_group": bytes_total / max(1, len(group_rows)),
        "candidate_c_interrogation_wall_time_ms": elapsed_ms,
        "candidate_c_group_count": len(group_rows),
        "candidate_c_membership_rows": len(membership_rows),
        "observer_burden_warning": bytes_total > 200000,
        "observer_burden_reason": "within provisional review threshold" if bytes_total <= 200000 else "candidate C interrogation output exceeds provisional review threshold",
        "review_only": True,
    }
    write_json(OBSERVER_BURDEN_PATH, observer)

    report = {
        "schema_version": "r250_candidate_c_group_interrogation_report_v0",
        "source_receipt_ids": {
            "source_coarsening_review_receipt_id": SOURCE_COARSENING_REVIEW_RECEIPT_ID,
            "source_pd_interrogation_receipt_id": SOURCE_PD_INTERROGATION_RECEIPT_ID,
            "source_pressure_metrics_repair_receipt_id": SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID,
            "source_failed_pressure_metrics_receipt_id_optional": SOURCE_FAILED_PRESSURE_METRICS_RECEIPT_ID_OPTIONAL,
        },
        "human_decision": HUMAN_DECISION,
        "accepted_candidate": {
            "candidate_id": ACCEPTED_COARSENING_CANDIDATE_ID,
            "candidate_name": ACCEPTED_COARSENING_CANDIDATE_NAME,
            "coarsening_fields": ACCEPTED_COARSENING_FIELDS,
            "status_from_review_layer": "PROMISING_REVIEW_LAYER",
        },
        "group_interrogation_rollup": rollup,
        "group_rows": group_rows,
        "representative_fragments_ref": rel(GROUP_REPRESENTATIVE_FRAGMENTS_PATH),
        "observer_burden_summary": observer,
        "interpretation": {
            "candidate_c_reduced_fragmentation": True,
            "dominant_group_present": True,
            "dominant_group_low_margin_warning": True,
            "candidate_c_useful_as_interrogation_lens": True,
            "candidate_c_action_authorized": False,
            "reason": "Candidate C creates 5 groups from 23 pressure events with repeated groups, but dominant margin remains 1; use as lens only.",
        },
        "recommended_next_handling": "HUMAN_REVIEW_CANDIDATE_C_GROUPS",
        "must_not_infer": MUST_NOT_INFER,
        "command_authorized": False,
        "proposal_authorized": False,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "repair_authorized": False,
        "runtime_behavior_changed": False,
        "review_only": True,
    }
    write_json(GROUP_INTERROGATION_REPORT_PATH, report)

    packet = {
        "schema_version": "r250_candidate_c_group_review_packet_v0",
        "packet_type": "HUMAN_REVIEW_PACKET_NOT_COMMAND",
        "source_candidate_c_interrogation": TARGET_UNIT_ID,
        "human_decision_bound": HUMAN_DECISION,
        "summary": {
            "group_count": rollup["group_count"],
            "group_size_profile": rollup["group_size_profile"],
            "dominant_group_share": rollup["dominant_group_share"],
            "dominant_group_margin": rollup["dominant_group_margin"],
            "dominant_group_low_margin_warning": rollup["dominant_group_low_margin_warning"],
            "singleton_group_count": rollup["singleton_group_count"],
        },
        "allowed_human_choices": [
            "ACCEPT_CANDIDATE_C_AS_INTERROGATION_LENS_ONLY",
            "INSPECT_DOMINANT_GROUP_MEMBERS",
            "INSPECT_SINGLETON_RESIDUE",
            "RUN_MORE_BATCH_EVIDENCE_WITH_CANDIDATE_C",
            "REJECT_CANDIDATE_C_KEEP_FRAGMENTATION_SIGNAL",
        ],
        "recommended_next_handling": "INSPECT_DOMINANT_GROUP_MEMBERS",
        "must_not_ask_for": [
            "taxonomy_upgrade",
            "authority_widening",
            "burden_optimization",
            "extraction_repair",
            "direct_build_command",
            "objective_proposal_from_pressure",
        ],
        "may_emit_build_command": False,
        "may_emit_objective_proposal": False,
        "may_authorize_taxonomy_upgrade": False,
        "may_authorize_authority_widening": False,
        "may_authorize_optimization": False,
        "may_authorize_repair": False,
        "review_only": True,
    }
    write_json(GROUP_REVIEW_PACKET_PATH, packet)

    return {
        "group_schema": group_schema,
        "group_rows": group_rows,
        "membership_rows": membership_rows,
        "fragments": fragments,
        "rollup": rollup,
        "observer": observer,
        "report": report,
        "packet": packet,
    }

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    if receipt.get("source_coarsening_review_receipt_id") != SOURCE_COARSENING_REVIEW_RECEIPT_ID:
        failures.append("source_coarsening_receipt_wrong")
    if receipt.get("accepted_coarsening_candidate_id") != ACCEPTED_COARSENING_CANDIDATE_ID:
        failures.append("accepted_candidate_wrong")
    if receipt.get("human_decision", {}).get("accepted_review_packet_choice") != "ACCEPT_COARSENING_LAYER_FOR_NEXT_INTERROGATION":
        failures.append("human_decision_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "R250_CANDIDATE_C_0_SOURCE_SURFACE_VERIFIED",
        "R250_CANDIDATE_C_1_HUMAN_ACCEPTANCE_RECORDED",
        "R250_CANDIDATE_C_2_CANDIDATE_C_ACCEPTED_AS_LENS_ONLY",
        "R250_CANDIDATE_C_3_GROUPS_EMITTED",
        "R250_CANDIDATE_C_4_EXACT_SIGNATURES_PRESERVED",
        "R250_CANDIDATE_C_5_GROUP_MEMBERSHIP_EMITTED",
        "R250_CANDIDATE_C_6_REPRESENTATIVE_FRAGMENTS_EMITTED",
        "R250_CANDIDATE_C_7_NO_ACTION_AUTHORIZED",
        "R250_CANDIDATE_C_8_NO_RUNTIME_RERUN",
        "R250_CANDIDATE_C_9_REVIEW_PACKET_EMITTED",
        "R250_CANDIDATE_C_10_NO_SOURCE_MUTATION",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    expected = {
        "source_pressure_event_count": 23,
        "candidate_c_group_count": 5,
        "candidate_c_membership_count": 23,
        "candidate_c_repeated_group_count": 4,
        "candidate_c_singleton_group_count": 1,
        "candidate_c_dominant_group_count": 7,
        "candidate_c_second_group_count": 6,
        "candidate_c_dominant_group_margin": 1,
        "candidate_c_dominant_group_share": 7 / 23,
        "candidate_c_coarsened_fragmentation_ratio": 5 / 23,
        "exact_signature_overwrite_count": 0,
        "command_authorized_count": 0,
        "proposal_authorized_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "authority_widening_authorized_count": 0,
        "optimization_authorized_count": 0,
        "repair_authorized_count": 0,
        "runtime_behavior_changed_count": 0,
        "runtime_rerun_count": 0,
        "source_mutation_count": 0,
        "sqlite_registry_write_count": 0,
        "review_packet_emitted": True,
        "review_only": True,
    }
    for key, value in expected.items():
        if metrics.get(key) != value:
            failures.append(f"metric_wrong:{key}:{metrics.get(key)} expected {value}")

    guards = receipt.get("candidate_c_interrogation_guards", {})
    for key in [
        "human_acceptance_recorded",
        "candidate_c_used_as_interrogation_lens_only",
        "candidate_c_groups_emitted",
        "exact_signatures_preserved",
        "group_membership_emitted",
        "representative_fragments_emitted",
        "observer_burden_measured",
        "review_packet_emitted",
        "review_only",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "runtime_rerun",
        "runtime_behavior_changed",
        "source_mutation",
        "exact_signature_overwritten",
        "command_emitted",
        "proposal_emitted",
        "repair_authorized",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "optimization_authorized",
        "roadmap_invented",
        "proof_claimed",
        "sqlite_registry_written",
        "hidden_next_command",
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

    outputs = build_outputs(sources)
    failures.extend(validate_outputs(
        outputs["group_rows"],
        outputs["membership_rows"],
        outputs["fragments"],
        outputs["rollup"],
        outputs["report"],
        outputs["packet"],
        outputs["observer"],
    ))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    rollup = outputs["rollup"]
    exact_overwrite_count = 0

    aggregate_metrics = {
        "source_pressure_event_count": 23,
        "candidate_c_group_count": rollup["group_count"],
        "candidate_c_membership_count": rollup["total_grouped_pressure_events"],
        "candidate_c_group_size_profile": rollup["group_size_profile"],
        "candidate_c_repeated_group_count": rollup["repeated_group_count"],
        "candidate_c_singleton_group_count": rollup["singleton_group_count"],
        "candidate_c_dominant_group_count": rollup["dominant_group_count"],
        "candidate_c_second_group_count": rollup["second_group_count"],
        "candidate_c_dominant_group_margin": rollup["dominant_group_margin"],
        "candidate_c_dominant_group_share": rollup["dominant_group_share"],
        "candidate_c_coarsened_fragmentation_ratio": rollup["coarsened_fragmentation_ratio"],
        "candidate_c_low_margin_warning": rollup["dominant_group_low_margin_warning"],
        "candidate_c_interrogation_only": True,
        "exact_signature_overwrite_count": exact_overwrite_count,
        "command_authorized_count": 0,
        "proposal_authorized_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "authority_widening_authorized_count": 0,
        "optimization_authorized_count": 0,
        "repair_authorized_count": 0,
        "runtime_behavior_changed_count": 0,
        "runtime_rerun_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "sqlite_registry_write_count": 0,
        "review_packet_emitted": GROUP_REVIEW_PACKET_PATH.exists(),
        "review_only": True,
    }

    acceptance_gate_results = {
        "R250_CANDIDATE_C_0_SOURCE_SURFACE_VERIFIED": len(validate_sources(sources)) == 0,
        "R250_CANDIDATE_C_1_HUMAN_ACCEPTANCE_RECORDED": HUMAN_DECISION["accepted_review_packet_choice"] == "ACCEPT_COARSENING_LAYER_FOR_NEXT_INTERROGATION",
        "R250_CANDIDATE_C_2_CANDIDATE_C_ACCEPTED_AS_LENS_ONLY": HUMAN_DECISION["scope"] == "interrogation_lens_only",
        "R250_CANDIDATE_C_3_GROUPS_EMITTED": GROUP_ROWS_PATH.exists() and rollup["group_count"] == 5,
        "R250_CANDIDATE_C_4_EXACT_SIGNATURES_PRESERVED": exact_overwrite_count == 0,
        "R250_CANDIDATE_C_5_GROUP_MEMBERSHIP_EMITTED": GROUP_EVENT_MEMBERSHIP_PATH.exists() and rollup["total_grouped_pressure_events"] == 23,
        "R250_CANDIDATE_C_6_REPRESENTATIVE_FRAGMENTS_EMITTED": GROUP_REPRESENTATIVE_FRAGMENTS_PATH.exists(),
        "R250_CANDIDATE_C_7_NO_ACTION_AUTHORIZED": all(aggregate_metrics[key] == 0 for key in ["command_authorized_count", "proposal_authorized_count", "taxonomy_upgrade_authorized_count", "authority_widening_authorized_count", "optimization_authorized_count", "repair_authorized_count"]),
        "R250_CANDIDATE_C_8_NO_RUNTIME_RERUN": aggregate_metrics["runtime_rerun_count"] == 0 and aggregate_metrics["runtime_behavior_changed_count"] == 0,
        "R250_CANDIDATE_C_9_REVIEW_PACKET_EMITTED": GROUP_REVIEW_PACKET_PATH.exists(),
        "R250_CANDIDATE_C_10_NO_SOURCE_MUTATION": source_mutation_detected is False,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_HUMAN_DECISION_REQUIRED",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}
    if exact_overwrite_count:
        terminal = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}
    if aggregate_metrics["command_authorized_count"] or aggregate_metrics["proposal_authorized_count"]:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_coarsening_receipt": SOURCE_COARSENING_REVIEW_RECEIPT_ID,
        "accepted_candidate": ACCEPTED_COARSENING_CANDIDATE_ID,
        "group_size_profile": rollup["group_size_profile"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "candidate_c_group_schema": rel(GROUP_SCHEMA_PATH),
        "candidate_c_group_rows": rel(GROUP_ROWS_PATH),
        "candidate_c_group_event_membership": rel(GROUP_EVENT_MEMBERSHIP_PATH),
        "candidate_c_group_interrogation_rollup": rel(GROUP_INTERROGATION_ROLLUP_PATH),
        "candidate_c_representative_fragments": rel(GROUP_REPRESENTATIVE_FRAGMENTS_PATH),
        "candidate_c_interrogation_observer_burden": rel(OBSERVER_BURDEN_PATH),
        "r250_candidate_c_group_interrogation_report": rel(GROUP_INTERROGATION_REPORT_PATH),
        "r250_candidate_c_group_review_packet": rel(GROUP_REVIEW_PACKET_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    guards = {
        "human_acceptance_recorded": True,
        "candidate_c_used_as_interrogation_lens_only": True,
        "candidate_c_groups_emitted": True,
        "exact_signatures_preserved": True,
        "group_membership_emitted": True,
        "representative_fragments_emitted": True,
        "observer_burden_measured": True,
        "review_packet_emitted": True,
        "review_only": True,
        "runtime_rerun": False,
        "runtime_behavior_changed": False,
        "source_mutation": source_mutation_detected,
        "exact_signature_overwritten": False,
        "command_emitted": False,
        "proposal_emitted": False,
        "repair_authorized": False,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "roadmap_invented": False,
        "proof_claimed": False,
        "sqlite_registry_written": False,
        "hidden_next_command": False,
    }

    receipt = {
        "schema_version": "r250_pressure_coarsened_candidate_c_interrogation_receipt_v0",
        "receipt_type": "R250_PRESSURE_COARSENED_CANDIDATE_C_GROUP_INTERROGATION_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": receipt_id,
        "target_unit_id": TARGET_UNIT_ID,
        "source_coarsening_review_receipt_id": SOURCE_COARSENING_REVIEW_RECEIPT_ID,
        "source_pd_interrogation_receipt_id": SOURCE_PD_INTERROGATION_RECEIPT_ID,
        "source_pressure_metrics_repair_receipt_id": SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID,
        "source_failed_pressure_metrics_receipt_id_optional": SOURCE_FAILED_PRESSURE_METRICS_RECEIPT_ID_OPTIONAL,
        "source_pressure_batch_id": SOURCE_PRESSURE_BATCH_ID,
        "source_previous_r250_batch_id": SOURCE_PREVIOUS_R250_BATCH_ID,
        "accepted_coarsening_candidate_id": ACCEPTED_COARSENING_CANDIDATE_ID,
        "accepted_coarsening_candidate_name": ACCEPTED_COARSENING_CANDIDATE_NAME,
        "accepted_coarsening_fields": ACCEPTED_COARSENING_FIELDS,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "candidate_c_group_summary": {
            "group_count": rollup["group_count"],
            "group_size_profile": rollup["group_size_profile"],
            "repeated_group_count": rollup["repeated_group_count"],
            "singleton_group_count": rollup["singleton_group_count"],
            "dominant_group_count": rollup["dominant_group_count"],
            "second_group_count": rollup["second_group_count"],
            "dominant_group_margin": rollup["dominant_group_margin"],
            "dominant_group_share": rollup["dominant_group_share"],
            "coarsened_fragmentation_ratio": rollup["coarsened_fragmentation_ratio"],
            "dominant_group_low_margin_warning": rollup["dominant_group_low_margin_warning"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "candidate_c_interrogation_guards": guards,
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
    print(f"r250_candidate_c_interrogation_receipt_id={receipt_id}")
    print(f"r250_candidate_c_interrogation_receipt_path=data/r250_pressure_candidate_c_interrogation_v0_receipts/{receipt_id}.json")
    print(f"r250_candidate_c_interrogation_report_path=data/r250_pressure_candidate_c_interrogation_v0/r250_candidate_c_group_interrogation_report.json")
    print(f"r250_candidate_c_review_packet_path=data/r250_pressure_candidate_c_interrogation_v0/r250_candidate_c_group_review_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
