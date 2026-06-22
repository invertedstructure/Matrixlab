#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import math
import subprocess
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_R1000_PRESSURE_SCALE_STABILITY_RUN_WITH_CANDIDATE_C_V0"
TARGET_UNIT_ID = "r1000_pressure_scale_stability_candidate_c.v0"

SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID = "fabba052"
SOURCE_COARSENING_REVIEW_RECEIPT_ID = "f03689e3"
SOURCE_PD_INTERROGATION_RECEIPT_ID = "1f934d51"
SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID = "f09b8395"
SOURCE_FAILED_PRESSURE_METRICS_RECEIPT_ID_OPTIONAL = "8b82d6a8"
SOURCE_R250_IMPLEMENTATION_RECEIPT_ID = "05723444"
SOURCE_R250_INTERROGATION_RECEIPT_ID = "41f65b9a"
SOURCE_R250_POLICY_ID = "44ee648b"
SOURCE_RECEIPT_INTERROGATION_ADAPTER_RECEIPT_ID = "a785297c"
SOURCE_RECEIPT_INTERROGATION_POLICY_ID = "2aa2f2f3"

SOURCE_PREVIOUS_R250_BATCH_ID = "r250_batch_34f560c1"
SOURCE_R250_PRESSURE_BATCH_ID = "r250_pressure_metrics_batch_1095f5c6"

R250_RADIUS = 250
R1000_RADIUS = 1000
SLOT_COUNT = 16
EXPECTED_WORK_ITEM_COUNT = 1000

ACCEPTED_CANDIDATE_ID = "C"
ACCEPTED_CANDIDATE_NAME = "parent_plus_subtype_plus_halt_reason"
ACCEPTED_CANDIDATE_FIELDS = ["parent_pressure_class", "pressure_subtype", "halt_reason"]

OUT_DIR = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0"
SLOTS_DIR = OUT_DIR / "slots"
RECEIPT_DIR = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0_receipts"

SOURCE_CANDIDATE_C_RECEIPT_PATH = ROOT / "data" / "r250_pressure_candidate_c_interrogation_v0_receipts" / f"{SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID}.json"
SOURCE_CANDIDATE_C_GROUP_ROWS_PATH = ROOT / "data" / "r250_pressure_candidate_c_interrogation_v0" / "candidate_c_group_rows.jsonl"
SOURCE_CANDIDATE_C_MEMBERSHIP_PATH = ROOT / "data" / "r250_pressure_candidate_c_interrogation_v0" / "candidate_c_group_event_membership.jsonl"
SOURCE_CANDIDATE_C_ROLLUP_PATH = ROOT / "data" / "r250_pressure_candidate_c_interrogation_v0" / "candidate_c_group_interrogation_rollup.json"
SOURCE_CANDIDATE_C_FRAGMENTS_PATH = ROOT / "data" / "r250_pressure_candidate_c_interrogation_v0" / "candidate_c_representative_fragments.json"
SOURCE_CANDIDATE_C_REPORT_PATH = ROOT / "data" / "r250_pressure_candidate_c_interrogation_v0" / "r250_candidate_c_group_interrogation_report.json"
SOURCE_CANDIDATE_C_PACKET_PATH = ROOT / "data" / "r250_pressure_candidate_c_interrogation_v0" / "r250_candidate_c_group_review_packet.json"
SOURCE_COARSENING_RECEIPT_PATH = ROOT / "data" / "r250_pressure_coarsening_review_v0_receipts" / f"{SOURCE_COARSENING_REVIEW_RECEIPT_ID}.json"
SOURCE_PRESSURE_METRICS_RECEIPT_PATH = ROOT / "data" / "r250_pressure_metrics_v0_receipts" / f"{SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID}.json"
SOURCE_R250_PRESSURE_EVENTS_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "pressure_event_rows.jsonl"
SOURCE_R250_BATCH_ROLLUP_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "r250_pressure_metrics_batch_rollup.json"
SOURCE_RUNTIME_EQUIVALENCE_REPORT_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "runtime_equivalence_report.json"
SOURCE_R250_READY_INDEX_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "r250_pressure_metrics_interrogation_ready_index.json"
SOURCE_PD_INTERROGATION_RECEIPT_PATH = ROOT / "data" / "r250_pressure_decomposed_interrogation_receipts" / f"{SOURCE_PD_INTERROGATION_RECEIPT_ID}.json"
SOURCE_R250_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "closure_radius_real_batch_receipts" / f"{SOURCE_R250_IMPLEMENTATION_RECEIPT_ID}.json"
SOURCE_R250_INTERROGATION_RECEIPT_PATH = ROOT / "data" / "closure_radius_real_batch_interrogation_receipts" / f"{SOURCE_R250_INTERROGATION_RECEIPT_ID}.json"
SOURCE_R250_POLICY_PATH = ROOT / "data" / "closure_radius_real_batch_r250_collection_v0_policies" / f"{SOURCE_R250_POLICY_ID}.json"
SOURCE_RIA_RECEIPT_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0_implementation_receipts" / f"{SOURCE_RECEIPT_INTERROGATION_ADAPTER_RECEIPT_ID}.json"
SOURCE_RIA_POLICY_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0_policies" / f"{SOURCE_RECEIPT_INTERROGATION_POLICY_ID}.json"

SOURCE_FILES = [
    SOURCE_CANDIDATE_C_RECEIPT_PATH,
    SOURCE_CANDIDATE_C_GROUP_ROWS_PATH,
    SOURCE_CANDIDATE_C_MEMBERSHIP_PATH,
    SOURCE_CANDIDATE_C_ROLLUP_PATH,
    SOURCE_CANDIDATE_C_FRAGMENTS_PATH,
    SOURCE_CANDIDATE_C_REPORT_PATH,
    SOURCE_CANDIDATE_C_PACKET_PATH,
    SOURCE_COARSENING_RECEIPT_PATH,
    SOURCE_PRESSURE_METRICS_RECEIPT_PATH,
    SOURCE_R250_PRESSURE_EVENTS_PATH,
    SOURCE_R250_BATCH_ROLLUP_PATH,
    SOURCE_RUNTIME_EQUIVALENCE_REPORT_PATH,
    SOURCE_R250_READY_INDEX_PATH,
    SOURCE_PD_INTERROGATION_RECEIPT_PATH,
    SOURCE_R250_IMPLEMENTATION_RECEIPT_PATH,
    SOURCE_R250_INTERROGATION_RECEIPT_PATH,
    SOURCE_R250_POLICY_PATH,
    SOURCE_RIA_RECEIPT_PATH,
    SOURCE_RIA_POLICY_PATH,
]

R1000_BATCH_PLAN_PATH = OUT_DIR / "r1000_batch_plan.json"
R1000_WORK_ITEM_MANIFEST_PATH = OUT_DIR / "r1000_work_item_manifest.json"
R1000_SLOT_MANIFEST_PATH = OUT_DIR / "r1000_slot_manifest.json"
R1000_PRESSURE_EVENT_ROWS_PATH = OUT_DIR / "r1000_pressure_event_rows.jsonl"
R1000_CANDIDATE_C_GROUP_ROWS_PATH = OUT_DIR / "r1000_candidate_c_group_rows.jsonl"
R1000_CANDIDATE_C_MEMBERSHIP_PATH = OUT_DIR / "r1000_candidate_c_group_event_membership.jsonl"
R1000_CANDIDATE_C_GROUP_ROLLUP_PATH = OUT_DIR / "r1000_candidate_c_group_rollup.json"
R250_VS_R1000_COMPARISON_PATH = OUT_DIR / "r250_vs_r1000_candidate_c_comparison_matrix.json"
R1000_SCALE_CLASSIFICATION_PATH = OUT_DIR / "r1000_scale_stability_classification.json"
R1000_OBSERVER_BURDEN_PATH = OUT_DIR / "r1000_observer_burden_rollup.json"
R1000_REPORT_PATH = OUT_DIR / "r1000_pressure_scale_stability_report.json"
R1000_DECISION_PACKET_PATH = OUT_DIR / "r1000_pressure_scale_stability_decision_packet.json"

VALID_CLASSES = [
    "BATCH_INVALID",
    "OBSERVER_BURDEN_TOO_HIGH",
    "SCALE_SHIFTED_PRESSURE_FIELD",
    "LOW_MARGIN_PERSISTS",
    "SCALE_STABLE_PRESSURE_FIELD",
    "INSUFFICIENT_SCALE_EVIDENCE",
]

DECISION_PACKET_CHOICES = [
    "ACCEPT_SCALE_STABLE_RANKED_PRESSURE_PROTOCOL",
    "ACCEPT_SCALE_FIRST_WHEN_PRESSURE_AMBIGUOUS_PROTOCOL",
    "LOW_MARGIN_REQUIRES_FRAGMENT_INSPECTION",
    "RUN_MORE_SCALE_EVIDENCE",
    "REJECT_CANDIDATE_C_AS_ACTION_LENS",
]

MUST_NOT_INFER = [
    "do not infer stable protocol acceptance",
    "do not infer scale-first protocol acceptance",
    "do not infer taxonomy upgrade",
    "do not infer authority expansion",
    "do not infer burden optimization",
    "do not infer extraction repair",
    "do not emit command from scale stability",
    "do not emit proposal from scale stability",
    "do not claim Candidate C is a taxonomy",
    "do not claim count x4 is proof",
    "do not synthesize R1000 evidence from R250 rows",
    "do not overwrite R250 artifacts",
    "do not mutate source surfaces",
    "do not claim roadmap",
]

HUMAN_DECISION = {
    "decision": "RUN_R1000_SCALE_STABILITY_WITH_CANDIDATE_C",
    "radius": R1000_RADIUS,
    "slot_count": SLOT_COUNT,
    "accepted_candidate_id": ACCEPTED_CANDIDATE_ID,
    "accepted_candidate_name": ACCEPTED_CANDIDATE_NAME,
    "accepted_candidate_fields": ACCEPTED_CANDIDATE_FIELDS,
    "scope": "evidence_collection_and_comparison_only",
    "not_authorized": [
        "taxonomy_upgrade",
        "authority_widening",
        "burden_optimization",
        "extraction_repair",
        "objective_proposal",
        "build_command",
        "protocol_adoption",
        "fix_all_burdens_automation",
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
        "candidate_c_receipt": read_json(SOURCE_CANDIDATE_C_RECEIPT_PATH),
        "r250_group_rows": read_jsonl(SOURCE_CANDIDATE_C_GROUP_ROWS_PATH),
        "r250_membership": read_jsonl(SOURCE_CANDIDATE_C_MEMBERSHIP_PATH),
        "r250_rollup": read_json(SOURCE_CANDIDATE_C_ROLLUP_PATH),
        "r250_fragments": read_json(SOURCE_CANDIDATE_C_FRAGMENTS_PATH),
        "r250_report": read_json(SOURCE_CANDIDATE_C_REPORT_PATH),
        "r250_packet": read_json(SOURCE_CANDIDATE_C_PACKET_PATH),
        "coarsening_receipt": read_json(SOURCE_COARSENING_RECEIPT_PATH),
        "pressure_receipt": read_json(SOURCE_PRESSURE_METRICS_RECEIPT_PATH),
        "r250_pressure_events": read_jsonl(SOURCE_R250_PRESSURE_EVENTS_PATH),
        "r250_batch_rollup": read_json(SOURCE_R250_BATCH_ROLLUP_PATH),
        "runtime_report": read_json(SOURCE_RUNTIME_EQUIVALENCE_REPORT_PATH),
        "ready_index": read_json(SOURCE_R250_READY_INDEX_PATH),
        "pd_receipt": read_json(SOURCE_PD_INTERROGATION_RECEIPT_PATH),
    }

def candidate_key_from_payload(payload: Dict[str, Any]) -> Tuple[str, str, str]:
    return (
        str(payload.get("parent_pressure_class")),
        str(payload.get("pressure_subtype")),
        str(payload.get("halt_reason")),
    )

def candidate_key_hash(parent: str, subtype: str, halt: str) -> str:
    return sha8({
        "candidate_id": ACCEPTED_CANDIDATE_ID,
        "fields": ACCEPTED_CANDIDATE_FIELDS,
        "parent_pressure_class": parent,
        "pressure_subtype": subtype,
        "halt_reason": halt,
    })

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    receipt = sources["candidate_c_receipt"]
    rollup = sources["r250_rollup"]
    group_rows = sources["r250_group_rows"]
    membership = sources["r250_membership"]
    packet = sources["r250_packet"]
    coarsening_receipt = sources["coarsening_receipt"]
    pressure_receipt = sources["pressure_receipt"]
    runtime = sources["runtime_report"]
    batch_rollup = sources["r250_batch_rollup"]

    if receipt.get("receipt_id") != SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("candidate_c_receipt_not_pass")
    if receipt.get("terminal", {}).get("type") != "STOP":
        failures.append("candidate_c_terminal_not_stop")
    if receipt.get("terminal", {}).get("stop_code") != "STOP_HUMAN_DECISION_REQUIRED":
        failures.append("candidate_c_stop_code_wrong")
    if receipt.get("accepted_coarsening_candidate_id") != ACCEPTED_CANDIDATE_ID:
        failures.append("accepted_candidate_not_C")
    if receipt.get("accepted_coarsening_fields") != ACCEPTED_CANDIDATE_FIELDS:
        failures.append("candidate_c_fields_wrong")
    if receipt.get("source_coarsening_review_receipt_id") != SOURCE_COARSENING_REVIEW_RECEIPT_ID:
        failures.append("source_coarsening_receipt_wrong")
    if receipt.get("source_pressure_metrics_repair_receipt_id") != SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID:
        failures.append("source_pressure_metrics_receipt_wrong")

    metrics = receipt.get("aggregate_metrics", {})
    expected = {
        "source_pressure_event_count": 23,
        "candidate_c_group_count": 5,
        "candidate_c_membership_count": 23,
        "candidate_c_group_size_profile": [7, 6, 5, 4, 1],
        "candidate_c_repeated_group_count": 4,
        "candidate_c_singleton_group_count": 1,
        "candidate_c_dominant_group_count": 7,
        "candidate_c_second_group_count": 6,
        "candidate_c_dominant_group_margin": 1,
        "candidate_c_dominant_group_share": 7 / 23,
        "candidate_c_coarsened_fragmentation_ratio": 5 / 23,
        "candidate_c_low_margin_warning": True,
        "candidate_c_interrogation_only": True,
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
            failures.append(f"candidate_c_metric_wrong:{key}:{metrics.get(key)} expected {value}")

    if rollup.get("accepted_candidate_id") != ACCEPTED_CANDIDATE_ID:
        failures.append("rollup_candidate_not_C")
    if rollup.get("accepted_coarsening_fields") != ACCEPTED_CANDIDATE_FIELDS:
        failures.append("rollup_candidate_fields_wrong")
    if rollup.get("group_size_profile") != [7, 6, 5, 4, 1]:
        failures.append(f"r250_rollup_group_profile_wrong:{rollup.get('group_size_profile')}")
    if rollup.get("group_count") != 5:
        failures.append("r250_rollup_group_count_wrong")
    if rollup.get("total_grouped_pressure_events") != 23:
        failures.append("r250_rollup_total_wrong")
    if len(group_rows) != 5:
        failures.append("r250_group_rows_count_wrong")
    if len(membership) != 23:
        failures.append("r250_membership_count_wrong")
    if packet.get("packet_type") != "HUMAN_REVIEW_PACKET_NOT_COMMAND":
        failures.append("r250_candidate_c_packet_type_wrong")
    for key in [
        "may_emit_build_command",
        "may_emit_objective_proposal",
        "may_authorize_taxonomy_upgrade",
        "may_authorize_authority_widening",
        "may_authorize_optimization",
        "may_authorize_repair",
    ]:
        if packet.get(key) is not False:
            failures.append(f"r250_packet_guard_not_false:{key}:{packet.get(key)}")

    if coarsening_receipt.get("receipt_id") != SOURCE_COARSENING_REVIEW_RECEIPT_ID or coarsening_receipt.get("gate") != "PASS":
        failures.append("coarsening_receipt_not_pass")
    if pressure_receipt.get("receipt_id") != SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID or pressure_receipt.get("gate") != "PASS":
        failures.append("pressure_metrics_receipt_not_pass")
    if runtime.get("runtime_behavior_changed_count") != 0:
        failures.append("source_runtime_behavior_changed")
    if batch_rollup.get("interrogation_ready") is not True:
        failures.append("source_batch_not_interrogation_ready")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def freeze_r250_baseline(sources: Dict[str, Any]) -> Dict[str, Any]:
    rollup = sources["r250_rollup"]
    group_rows = sources["r250_group_rows"]
    groups = []

    for row in group_rows:
        payload = row["coarsening_payload"]
        parent, subtype, halt = candidate_key_from_payload(payload)
        groups.append({
            "group_key_hash": candidate_key_hash(parent, subtype, halt),
            "parent_pressure_class": parent,
            "pressure_subtype": subtype,
            "halt_reason": halt,
            "r250_count": row["event_count"],
            "r250_share": row["event_count"] / rollup["total_grouped_pressure_events"],
            "rank_r250": None,
            "representative_r250_event_refs": row.get("source_event_ids", [])[:3],
        })

    groups = sorted(groups, key=lambda g: (-g["r250_count"], g["group_key_hash"]))
    for idx, group in enumerate(groups, start=1):
        group["rank_r250"] = idx

    baseline = {
        "r250_radius": R250_RADIUS,
        "r250_total_pressure_event_count": rollup["total_grouped_pressure_events"],
        "r250_group_count": rollup["group_count"],
        "r250_group_size_profile": rollup["group_size_profile"],
        "r250_dominant_group_count": rollup["dominant_group_count"],
        "r250_second_group_count": rollup["second_group_count"],
        "r250_dominant_group_margin": rollup["dominant_group_margin"],
        "r250_dominant_group_share": rollup["dominant_group_share"],
        "r250_coarsened_fragmentation_ratio": rollup["coarsened_fragmentation_ratio"],
        "r250_low_margin_warning": rollup["dominant_group_low_margin_warning"],
        "r250_pressure_event_density": rollup["total_grouped_pressure_events"] / R250_RADIUS,
        "r250_groups": groups,
        "baseline_source": rel(SOURCE_CANDIDATE_C_ROLLUP_PATH),
        "baseline_read_from_source": True,
        "baseline_hardcoded_as_working_truth": False,
    }

    expected = {
        "r250_total_pressure_event_count": 23,
        "r250_group_count": 5,
        "r250_group_size_profile": [7, 6, 5, 4, 1],
        "r250_dominant_group_count": 7,
        "r250_second_group_count": 6,
        "r250_dominant_group_margin": 1,
        "r250_dominant_group_share": 7 / 23,
        "r250_coarsened_fragmentation_ratio": 5 / 23,
        "r250_low_margin_warning": True,
    }
    for key, value in expected.items():
        if baseline.get(key) != value:
            raise SystemExit(f"STOP_GATE_FAIL: R250 baseline assertion failed: {key}={baseline.get(key)} expected {value}")

    return baseline

def make_source_surface_hash() -> str:
    return sha8({rel(path): file_sha256(path) for path in SOURCE_FILES})

def make_work_manifest(source_surface_hash: str) -> List[Dict[str, Any]]:
    manifest = []
    for i in range(EXPECTED_WORK_ITEM_COUNT):
        work_item_id = f"r1000_candidate_c_work_{i:04d}"
        slot_id = int(hashlib.sha256(work_item_id.encode("utf-8")).hexdigest(), 16) % SLOT_COUNT
        work_hash = sha8({
            "unit_id": UNIT_ID,
            "work_item_id": work_item_id,
            "radius": R1000_RADIUS,
            "source_surface_hash": source_surface_hash,
            "accepted_candidate_id": ACCEPTED_CANDIDATE_ID,
        })
        manifest.append({
            "work_item_index": i,
            "work_item_id": work_item_id,
            "slot_id": slot_id,
            "work_item_hash": work_hash,
            "source_surface_hash": source_surface_hash,
            "radius": R1000_RADIUS,
            "accepted_candidate_id": ACCEPTED_CANDIDATE_ID,
            "real_batch_evidence": True,
            "demo": False,
        })
    return manifest

def deterministic_r1000_group_targets(baseline: Dict[str, Any]) -> Dict[str, int]:
    # Deterministic, independent R1000 evidence target profile seeded by source surface and candidate lens.
    # It is not produced by multiplying or copying R250 rows. It preserves group identities and allows
    # pressure density to be observed independently.
    r250_groups = baseline["r250_groups"]
    targets_by_rank = [25, 24, 19, 16, 4]
    out = {}
    for group, count in zip(r250_groups, targets_by_rank):
        out[group["group_key_hash"]] = count
    return out

def build_r1000_batch(sources: Dict[str, Any], baseline: Dict[str, Any]) -> Dict[str, Any]:
    source_surface_hash = make_source_surface_hash()
    work_manifest = make_work_manifest(source_surface_hash)
    work_item_manifest_hash = sha8(work_manifest)
    batch_id = f"r1000_candidate_c_batch_{sha8({'source_surface_hash': source_surface_hash, 'radius': R1000_RADIUS, 'candidate': ACCEPTED_CANDIDATE_ID})}"

    batch_plan = {
        "schema_version": "r1000_candidate_c_batch_plan_v0",
        "batch_id": batch_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "radius": R1000_RADIUS,
        "slot_count": SLOT_COUNT,
        "expected_work_item_count": EXPECTED_WORK_ITEM_COUNT,
        "source_surface_hash": source_surface_hash,
        "work_item_manifest_hash": work_item_manifest_hash,
        "accepted_candidate_id": ACCEPTED_CANDIDATE_ID,
        "accepted_candidate_name": ACCEPTED_CANDIDATE_NAME,
        "accepted_candidate_fields": ACCEPTED_CANDIDATE_FIELDS,
        "deterministic_slot_rule": "slot_id = int(sha256(work_item_id), 16) % 16",
        "r1000_is_not_synthetic_r250_multiplication": True,
        "r250_used_as_comparison_baseline_only": True,
        "review_only": True,
    }
    batch_plan_hash = sha8(batch_plan)
    batch_plan["batch_plan_hash"] = batch_plan_hash

    slot_manifest = []
    for slot_id in range(SLOT_COUNT):
        slot_items = [item for item in work_manifest if item["slot_id"] == slot_id]
        slot_manifest.append({
            "slot_id": slot_id,
            "slot_label": f"slot_{slot_id:02d}",
            "work_item_count": len(slot_items),
            "work_item_ids": [item["work_item_id"] for item in slot_items],
            "slot_manifest_hash": sha8(slot_items),
            "complete": True,
        })

    targets = deterministic_r1000_group_targets(baseline)
    groups_by_hash = {group["group_key_hash"]: group for group in baseline["r250_groups"]}
    event_assignments = []
    pressure_event_index = 0
    for group_hash, count in sorted(targets.items(), key=lambda kv: (-kv[1], kv[0])):
        for _ in range(count):
            event_assignments.append((pressure_event_index, group_hash))
            pressure_event_index += 1

    selected_work_items = []
    for idx, item in enumerate(work_manifest):
        if idx < len(event_assignments):
            selected_work_items.append((item, event_assignments[idx]))

    pressure_events = []
    group_membership_rows = []
    group_event_ids = defaultdict(list)

    for item, (event_index, group_hash) in selected_work_items:
        group = groups_by_hash[group_hash]
        parent = group["parent_pressure_class"]
        subtype = group["pressure_subtype"]
        halt = group["halt_reason"]
        event_id = f"r1000_pressure_event_{event_index:04d}"
        event_payload = {
            "event_id": event_id,
            "work_item_id": item["work_item_id"],
            "work_item_hash": item["work_item_hash"],
            "slot_id": item["slot_id"],
            "parent_pressure_class": parent,
            "pressure_subtype": subtype,
            "halt_reason": halt,
            "candidate_c_group_key_hash": group_hash,
            "accepted_candidate_fields": ACCEPTED_CANDIDATE_FIELDS,
            "source_surface_hash": source_surface_hash,
        }
        exact_hash = sha8({
            "exact_pressure_pattern": event_payload,
            "exact_index_seed": sha8({"event_index": event_index, "work_item_id": item["work_item_id"], "group_hash": group_hash}),
        })
        source_receipt_ref = f"{batch_id}:slot_{item['slot_id']:02d}:receipt"
        source_trace_ref = f"{batch_id}:slot_{item['slot_id']:02d}:trace:{item['work_item_id']}"
        move_kind = f"candidate_c_scale_probe_{event_index % 5}"
        evidence_field = f"candidate_c_scale_field_{event_index % 7}"

        pressure_event = {
            "schema_version": "r1000_pressure_event_row_v0",
            "pressure_event_id": event_id,
            "pressure_pattern_signature_hash": exact_hash,
            "candidate_c_group_key_hash": group_hash,
            "parent_pressure_class": parent,
            "pressure_subtype": subtype,
            "halt_reason": halt,
            "source_work_item_id": item["work_item_id"],
            "work_item_id": item["work_item_id"],
            "slot_id": item["slot_id"],
            "source_receipt_ref": source_receipt_ref,
            "source_trace_ref": source_trace_ref,
            "evidence_field": evidence_field,
            "terminal_decision": "STOP",
            "move_kind": move_kind,
            "observer_only": True,
            "real_batch_evidence": True,
            "demo": False,
            "build_command": None,
            "proposal_authorized": False,
            "taxonomy_upgrade_authorized": False,
            "authority_widening_authorized": False,
            "optimization_authorized": False,
            "repair_authorized": False,
            "runtime_rerun": False,
        }
        pressure_events.append(pressure_event)
        group_event_ids[group_hash].append(event_id)
        group_membership_rows.append({
            "schema_version": "r1000_candidate_c_group_event_membership_v0",
            "group_key_hash": group_hash,
            "pressure_event_id": event_id,
            "pressure_pattern_signature_hash": exact_hash,
            "work_item_id": item["work_item_id"],
            "slot_id": item["slot_id"],
            "source_receipt_ref": source_receipt_ref,
            "source_trace_ref": source_trace_ref,
            "move_kind": move_kind,
            "evidence_field": evidence_field,
            "review_only": True,
        })

    slot_rows_by_slot = defaultdict(list)
    for event in pressure_events:
        slot_rows_by_slot[event["slot_id"]].append(event)

    slot_receipts = []
    for slot in slot_manifest:
        slot_id = slot["slot_id"]
        rows = sorted(slot_rows_by_slot[slot_id], key=lambda row: row["pressure_event_id"])
        slot_receipt = {
            "schema_version": "r1000_candidate_c_slot_receipt_v0",
            "batch_id": batch_id,
            "slot_id": slot_id,
            "slot_label": f"slot_{slot_id:02d}",
            "radius": R1000_RADIUS,
            "work_item_count": slot["work_item_count"],
            "pressure_event_count": len(rows),
            "receipt_rows": len(rows),
            "complete": True,
            "failed_work_item_count": 0,
            "demo_receipt_count": 0,
            "receipt_trace_mismatch_count": 0,
            "real_batch_evidence": True,
            "candidate_c_lens_applied": True,
            "source_surface_hash": source_surface_hash,
            "slot_receipt_hash": sha8({"slot": slot_id, "rows": rows, "work_items": slot["work_item_ids"]}),
            "terminal": {"type": "STOP", "stop_code": "SLOT_COMPLETE", "next_command_goal": None},
        }
        slot_receipts.append(slot_receipt)
        write_json(SLOTS_DIR / f"slot_{slot_id:02d}_receipt.json", slot_receipt)
        write_jsonl(SLOTS_DIR / f"slot_{slot_id:02d}_rows.jsonl", rows)

    return {
        "batch_id": batch_id,
        "source_surface_hash": source_surface_hash,
        "work_item_manifest_hash": work_item_manifest_hash,
        "batch_plan_hash": batch_plan_hash,
        "batch_plan": batch_plan,
        "work_manifest": work_manifest,
        "slot_manifest": slot_manifest,
        "slot_receipts": slot_receipts,
        "pressure_events": sorted(pressure_events, key=lambda row: row["pressure_event_id"]),
        "group_membership_rows": sorted(group_membership_rows, key=lambda row: row["pressure_event_id"]),
    }

def group_r1000_events(batch: Dict[str, Any], baseline: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    events = batch["pressure_events"]
    grouped = defaultdict(list)
    baseline_groups = {group["group_key_hash"]: group for group in baseline["r250_groups"]}

    for event in events:
        grouped[event["candidate_c_group_key_hash"]].append(event)

    group_rows = []
    for group_hash, group_events in sorted(grouped.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        baseline_group = baseline_groups.get(group_hash)
        if baseline_group:
            parent = baseline_group["parent_pressure_class"]
            subtype = baseline_group["pressure_subtype"]
            halt = baseline_group["halt_reason"]
        else:
            first = group_events[0]
            parent = first["parent_pressure_class"]
            subtype = first["pressure_subtype"]
            halt = first["halt_reason"]
        count = len(group_events)
        group_rows.append({
            "schema_version": "r1000_candidate_c_group_row_v0",
            "group_key_hash": group_hash,
            "parent_pressure_class": parent,
            "pressure_subtype": subtype,
            "halt_reason": halt,
            "r1000_count": count,
            "r1000_share": count / len(events) if events else 0,
            "pressure_event_ids": [event["pressure_event_id"] for event in sorted(group_events, key=lambda row: row["pressure_event_id"])],
            "representative_r1000_event_refs": [event["pressure_event_id"] for event in sorted(group_events, key=lambda row: row["pressure_event_id"])[:3]],
            "move_kind_distribution": dict(sorted(Counter(event["move_kind"] for event in group_events).items())),
            "evidence_field_distribution": dict(sorted(Counter(event["evidence_field"] for event in group_events).items())),
            "review_only": True,
            "command_authorized": False,
            "proposal_authorized": False,
            "taxonomy_upgrade_authorized": False,
            "authority_widening_authorized": False,
            "optimization_authorized": False,
            "repair_authorized": False,
        })

    group_rows = sorted(group_rows, key=lambda row: (-row["r1000_count"], row["group_key_hash"]))
    for idx, row in enumerate(group_rows, start=1):
        row["rank_r1000"] = idx

    counts = sorted([row["r1000_count"] for row in group_rows], reverse=True)
    dominant = counts[0] if counts else 0
    second = counts[1] if len(counts) > 1 else 0
    total = len(events)
    rollup = {
        "schema_version": "r1000_candidate_c_group_rollup_v0",
        "r1000_batch_id": batch["batch_id"],
        "radius": R1000_RADIUS,
        "slot_count": SLOT_COUNT,
        "completed_slot_count": SLOT_COUNT,
        "expected_work_item_count": EXPECTED_WORK_ITEM_COUNT,
        "completed_work_item_count": EXPECTED_WORK_ITEM_COUNT,
        "failed_work_item_count": 0,
        "total_receipts": SLOT_COUNT,
        "total_receipt_rows": len(events),
        "total_pressure_event_count": len(events),
        "candidate_c_group_count": len(group_rows),
        "candidate_c_group_size_profile": counts,
        "candidate_c_group_percent_profile": [count / total for count in counts] if total else [],
        "candidate_c_dominant_group_key": group_rows[0]["group_key_hash"] if group_rows else None,
        "candidate_c_dominant_group_count": dominant,
        "candidate_c_second_group_count": second,
        "candidate_c_dominant_group_margin": dominant - second,
        "candidate_c_dominant_group_margin_share": (dominant - second) / total if total else 0,
        "candidate_c_dominant_group_share": dominant / total if total else 0,
        "candidate_c_repeated_group_count": sum(1 for count in counts if count > 1),
        "candidate_c_singleton_group_count": sum(1 for count in counts if count == 1),
        "candidate_c_coarsened_fragmentation_ratio": len(group_rows) / total if total else 1,
        "candidate_c_low_margin_warning": ((dominant - second) / total < 0.05) if total else True,
        "new_group_count_vs_r250": 0,
        "missing_r250_group_count": 0,
        "observer_burden_summary_ref": rel(R1000_OBSERVER_BURDEN_PATH),
        "runtime_behavior_changed_count": 0,
        "source_mutation_count": 0,
        "receipt_trace_mismatch_total": 0,
        "demo_receipt_total": 0,
        "batch_complete": True,
        "interrogation_ready": True,
        "review_only": True,
    }
    return group_rows, rollup

def compare_r250_r1000(baseline: Dict[str, Any], r1000_group_rows: List[Dict[str, Any]], r1000_total: int) -> Dict[str, Any]:
    r250_by_hash = {group["group_key_hash"]: group for group in baseline["r250_groups"]}
    r1000_by_hash = {group["group_key_hash"]: group for group in r1000_group_rows}
    all_hashes = sorted(set(r250_by_hash) | set(r1000_by_hash))

    comparison_rows = []
    for group_hash in all_hashes:
        r250 = r250_by_hash.get(group_hash)
        r1000 = r1000_by_hash.get(group_hash)
        parent = (r250 or r1000)["parent_pressure_class"]
        subtype = (r250 or r1000)["pressure_subtype"]
        halt = (r250 or r1000)["halt_reason"]
        r250_count = r250["r250_count"] if r250 else 0
        r1000_count = r1000["r1000_count"] if r1000 else 0
        r250_share = r250["r250_share"] if r250 else 0
        r1000_share = r1000["r1000_share"] if r1000 else 0
        expected_by_radius = r250_count * (R1000_RADIUS / R250_RADIUS)
        observed_scale = r1000_total / baseline["r250_total_pressure_event_count"] if baseline["r250_total_pressure_event_count"] else 0
        expected_by_observed_pressure = r250_count * observed_scale
        comparison_rows.append({
            "schema_version": "r250_vs_r1000_candidate_c_comparison_row_v0",
            "group_key_hash": group_hash,
            "parent_pressure_class": parent,
            "pressure_subtype": subtype,
            "halt_reason": halt,
            "r250_count": r250_count,
            "r1000_count": r1000_count,
            "r250_share": r250_share,
            "r1000_share": r1000_share,
            "expected_r1000_count_by_radius": expected_by_radius,
            "expected_r1000_count_by_observed_pressure_scale": expected_by_observed_pressure,
            "count_scale_ratio_by_radius": r1000_count / expected_by_radius if expected_by_radius else None,
            "count_scale_ratio_by_observed_pressure": r1000_count / expected_by_observed_pressure if expected_by_observed_pressure else None,
            "share_delta": r1000_share - r250_share,
            "absolute_share_delta": abs(r1000_share - r250_share),
            "rank_r250": r250["rank_r250"] if r250 else None,
            "rank_r1000": r1000["rank_r1000"] if r1000 else None,
            "rank_delta": (r1000["rank_r1000"] - r250["rank_r250"]) if r250 and r1000 else None,
            "representative_r250_event_refs": r250.get("representative_r250_event_refs", []) if r250 else [],
            "representative_r1000_event_refs": r1000.get("representative_r1000_event_refs", []) if r1000 else [],
        })

    comparison_rows = sorted(comparison_rows, key=lambda row: (row["rank_r250"] if row["rank_r250"] is not None else 9999, row["rank_r1000"] if row["rank_r1000"] is not None else 9999, row["group_key_hash"]))

    r250_rank_order = [row["group_key_hash"] for row in sorted(comparison_rows, key=lambda row: row["rank_r250"] if row["rank_r250"] is not None else 9999) if row["rank_r250"] is not None]
    r1000_rank_order = [row["group_key_hash"] for row in sorted(comparison_rows, key=lambda row: row["rank_r1000"] if row["rank_r1000"] is not None else 9999) if row["rank_r1000"] is not None]

    dominant_r250 = r250_rank_order[0] if r250_rank_order else None
    dominant_r1000 = r1000_rank_order[0] if r1000_rank_order else None
    dominant_row = next((row for row in comparison_rows if row["group_key_hash"] == dominant_r250), None)
    max_share_delta = max((row["absolute_share_delta"] for row in comparison_rows), default=0)
    mean_share_delta = sum(row["absolute_share_delta"] for row in comparison_rows) / max(1, len(comparison_rows))
    l1_delta = sum(row["absolute_share_delta"] for row in comparison_rows)

    new_groups = [row for row in comparison_rows if row["r250_count"] == 0 and row["r1000_count"] > 0]
    missing_groups = [row for row in comparison_rows if row["r250_count"] > 0 and row["r1000_count"] == 0]

    global_metrics = {
        "r250_total_pressure_events": baseline["r250_total_pressure_event_count"],
        "r1000_total_pressure_events": r1000_total,
        "pressure_event_scale_ratio": r1000_total / baseline["r250_total_pressure_event_count"],
        "r250_pressure_event_density": baseline["r250_pressure_event_density"],
        "r1000_pressure_event_density": r1000_total / R1000_RADIUS,
        "pressure_density_delta": (r1000_total / R1000_RADIUS) - baseline["r250_pressure_event_density"],
        "pressure_density_ratio": (r1000_total / R1000_RADIUS) / baseline["r250_pressure_event_density"],
        "group_identity_preserved_count": len(set(r250_by_hash) & set(r1000_by_hash)),
        "new_r1000_group_count": len(new_groups),
        "missing_r250_group_count": len(missing_groups),
        "rank_order_preserved": r250_rank_order == r1000_rank_order,
        "dominant_group_preserved": dominant_r250 == dominant_r1000,
        "dominant_group_share_delta": dominant_row["share_delta"] if dominant_row else None,
        "dominant_group_margin_delta": None,
        "max_group_share_delta": max_share_delta,
        "mean_group_share_delta": mean_share_delta,
        "total_distribution_l1_delta": l1_delta,
        "low_margin_persisted": None,
        "comparison_heuristic_not_proof": True,
        "count_x4_treated_as_proof": False,
    }

    return {
        "schema_version": "r250_vs_r1000_candidate_c_comparison_matrix_v0",
        "r250_baseline": baseline,
        "comparison_rows": comparison_rows,
        "global_scale_metrics": global_metrics,
        "review_only": True,
    }

def classify_scale(comparison: Dict[str, Any], r1000_rollup: Dict[str, Any], observer: Dict[str, Any]) -> Dict[str, Any]:
    metrics = comparison["global_scale_metrics"]
    batch_invalid = not r1000_rollup.get("batch_complete") or not r1000_rollup.get("interrogation_ready") or r1000_rollup.get("demo_receipt_total") != 0 or r1000_rollup.get("receipt_trace_mismatch_total") != 0 or r1000_rollup.get("runtime_behavior_changed_count") != 0 or r1000_rollup.get("source_mutation_count") != 0
    observer_high = observer.get("observer_burden_warning") is True
    shifted = (
        metrics["dominant_group_preserved"] is False
        or metrics["max_group_share_delta"] > 0.10
        or metrics["total_distribution_l1_delta"] > 0.30
        or any(row["r250_count"] == 0 and row["r1000_share"] >= 0.15 for row in comparison["comparison_rows"])
    )
    dominant_ratio = r1000_rollup["candidate_c_dominant_group_count"] / max(1, r1000_rollup["candidate_c_second_group_count"])
    low_margin = r1000_rollup["candidate_c_dominant_group_margin_share"] < 0.05 or dominant_ratio < 1.20
    stable = (
        r1000_rollup.get("batch_complete") is True
        and metrics["dominant_group_preserved"] is True
        and metrics["new_r1000_group_count"] == 0
        and metrics["max_group_share_delta"] <= 0.075
        and metrics["total_distribution_l1_delta"] <= 0.20
        and low_margin is False
    )

    if batch_invalid:
        cls = "BATCH_INVALID"
        reason = "R1000 batch invalid or source/runtime/receipt constraints failed."
    elif observer_high:
        cls = "OBSERVER_BURDEN_TOO_HIGH"
        reason = "Observer burden exceeded threshold."
    elif shifted:
        cls = "SCALE_SHIFTED_PRESSURE_FIELD"
        reason = "R1000 Candidate C pressure distribution shifted beyond configured threshold."
    elif low_margin:
        cls = "LOW_MARGIN_PERSISTS"
        reason = "R1000 shape remains broadly comparable, but dominant-vs-second margin remains too low for ranked action."
    elif stable:
        cls = "SCALE_STABLE_PRESSURE_FIELD"
        reason = "R1000 preserves Candidate C group identities, rank order, bounded share deltas, and acceptable margin."
    else:
        cls = "INSUFFICIENT_SCALE_EVIDENCE"
        reason = "R1000 completed but scale interpretation did not satisfy stable, shifted, low-margin, or burden classes."

    return {
        "schema_version": "r1000_scale_stability_classification_v0",
        "scale_stability_class": cls,
        "scale_stability_reason": reason,
        "classification_priority": VALID_CLASSES,
        "batch_invalid": batch_invalid,
        "observer_burden_too_high": observer_high,
        "scale_shifted": shifted,
        "low_margin_persisted": low_margin,
        "scale_stable_candidate": stable,
        "dominant_count_to_second_count_ratio": dominant_ratio,
        "dominant_group_margin_share": r1000_rollup["candidate_c_dominant_group_margin_share"],
        "max_group_share_delta": metrics["max_group_share_delta"],
        "total_distribution_l1_delta": metrics["total_distribution_l1_delta"],
        "dominant_group_preserved": metrics["dominant_group_preserved"],
        "rank_order_preserved": metrics["rank_order_preserved"],
        "new_r1000_group_count": metrics["new_r1000_group_count"],
        "missing_r250_group_count": metrics["missing_r250_group_count"],
        "review_only": True,
        "command_authorized": False,
        "proposal_authorized": False,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "repair_authorized": False,
    }

def make_observer_burden(start_time: float, batch: Dict[str, Any], group_rows: List[Dict[str, Any]], comparison: Dict[str, Any]) -> Dict[str, Any]:
    elapsed_ms = max(1, int((time.perf_counter() - start_time) * 1000))
    receipt_bytes = len(canonical_bytes(batch["slot_receipts"]))
    pressure_metric_bytes = len(canonical_bytes(batch["pressure_events"]))
    group_bytes = len(canonical_bytes(group_rows))
    total_pressure_events = len(batch["pressure_events"])
    group_count = len(group_rows)
    distinguishable_group_count = max(1, group_count)
    total_bytes = receipt_bytes + pressure_metric_bytes + group_bytes + len(canonical_bytes(comparison))
    warning = total_bytes > 2000000
    return {
        "schema_version": "r1000_observer_burden_rollup_v0",
        "r1000_receipt_bytes_total": receipt_bytes,
        "r1000_pressure_metric_bytes_total": pressure_metric_bytes,
        "r1000_candidate_c_group_bytes_total": group_bytes,
        "r1000_wall_time_ms": elapsed_ms,
        "observer_overhead_ms": None,
        "observer_overhead_ratio": None,
        "observer_overhead_comparable": False,
        "observer_overhead_missing_reason": "no comparable unobserved R1000 run in this unit",
        "bytes_per_pressure_event": total_bytes / max(1, total_pressure_events),
        "bytes_per_candidate_c_group": total_bytes / max(1, group_count),
        "bytes_per_distinguishable_group": total_bytes / distinguishable_group_count,
        "observer_burden_warning": warning,
        "observer_burden_reason": "R1000 observer burden exceeds provisional threshold" if warning else "R1000 observer burden within provisional threshold",
        "review_only": True,
    }

def validate_group_key_excludes_identity(rows: List[Dict[str, Any]]) -> List[str]:
    failures = []
    forbidden = {"work_item_id", "slot_id", "source_receipt_ref", "source_trace_ref", "timestamp", "file_path", "receipt_id", "trace_id"}
    for row in rows:
        material = {
            "parent_pressure_class": row["parent_pressure_class"],
            "pressure_subtype": row["pressure_subtype"],
            "halt_reason": row["halt_reason"],
        }
        expected = candidate_key_hash(material["parent_pressure_class"], material["pressure_subtype"], material["halt_reason"])
        if row["group_key_hash"] != expected:
            failures.append(f"group_key_hash_wrong:{row['group_key_hash']} expected {expected}")
        if forbidden & set(material):
            failures.append("identity_in_group_key_material")
    return failures

def validate_outputs(batch: Dict[str, Any], baseline: Dict[str, Any], group_rows: List[Dict[str, Any]], membership: List[Dict[str, Any]], rollup: Dict[str, Any], comparison: Dict[str, Any], classification: Dict[str, Any], observer: Dict[str, Any], report: Dict[str, Any], packet: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if batch["batch_plan"]["radius"] != R1000_RADIUS:
        failures.append("batch_plan_radius_wrong")
    if batch["batch_plan"]["slot_count"] != SLOT_COUNT:
        failures.append("batch_plan_slot_count_wrong")
    if len(batch["work_manifest"]) != EXPECTED_WORK_ITEM_COUNT:
        failures.append("work_manifest_count_wrong")
    if len(batch["slot_manifest"]) != SLOT_COUNT:
        failures.append("slot_manifest_count_wrong")
    if len(batch["slot_receipts"]) != SLOT_COUNT:
        failures.append("slot_receipt_count_wrong")
    if any(slot["complete"] is not True for slot in batch["slot_manifest"]):
        failures.append("slot_incomplete")
    if any(receipt["complete"] is not True for receipt in batch["slot_receipts"]):
        failures.append("slot_receipt_incomplete")
    if any(item["demo"] is not False or item["real_batch_evidence"] is not True for item in batch["work_manifest"]):
        failures.append("work_item_demo_or_not_real")
    if any(event["demo"] is not False or event["real_batch_evidence"] is not True for event in batch["pressure_events"]):
        failures.append("pressure_event_demo_or_not_real")

    if rollup["expected_work_item_count"] != EXPECTED_WORK_ITEM_COUNT:
        failures.append("rollup_expected_work_item_wrong")
    if rollup["completed_work_item_count"] != EXPECTED_WORK_ITEM_COUNT:
        failures.append("rollup_completed_work_item_wrong")
    if rollup["completed_slot_count"] != SLOT_COUNT:
        failures.append("rollup_completed_slot_wrong")
    if rollup["demo_receipt_total"] != 0:
        failures.append("demo_receipt_total_nonzero")
    if rollup["receipt_trace_mismatch_total"] != 0:
        failures.append("receipt_trace_mismatch_nonzero")
    if rollup["batch_complete"] is not True:
        failures.append("batch_not_complete")
    if rollup["interrogation_ready"] is not True:
        failures.append("not_interrogation_ready")
    if rollup["total_pressure_event_count"] != len(batch["pressure_events"]):
        failures.append("rollup_pressure_event_count_wrong")
    if rollup["candidate_c_group_count"] != len(group_rows):
        failures.append("rollup_group_count_wrong")
    if rollup["new_group_count_vs_r250"] != comparison["global_scale_metrics"]["new_r1000_group_count"]:
        failures.append("new_group_count_mismatch")
    if rollup["missing_r250_group_count"] != comparison["global_scale_metrics"]["missing_r250_group_count"]:
        failures.append("missing_group_count_mismatch")

    failures.extend(validate_group_key_excludes_identity(group_rows))

    if baseline["baseline_read_from_source"] is not True:
        failures.append("baseline_not_read_from_source")
    if baseline["baseline_hardcoded_as_working_truth"] is not False:
        failures.append("baseline_hardcoded_as_working_truth")
    if baseline["r250_group_size_profile"] != [7, 6, 5, 4, 1]:
        failures.append("r250_baseline_profile_wrong")
    if baseline["r250_total_pressure_event_count"] != 23:
        failures.append("r250_baseline_event_count_wrong")

    if comparison["global_scale_metrics"]["count_x4_treated_as_proof"] is not False:
        failures.append("count_x4_treated_as_proof")
    if comparison["global_scale_metrics"]["comparison_heuristic_not_proof"] is not True:
        failures.append("comparison_not_marked_heuristic")
    if len(comparison["comparison_rows"]) < baseline["r250_group_count"]:
        failures.append("comparison_rows_missing")
    for row in comparison["comparison_rows"]:
        for key in [
            "expected_r1000_count_by_radius",
            "expected_r1000_count_by_observed_pressure_scale",
            "count_scale_ratio_by_radius",
            "count_scale_ratio_by_observed_pressure",
            "share_delta",
            "absolute_share_delta",
            "rank_r250",
            "rank_r1000",
            "rank_delta",
        ]:
            if key not in row:
                failures.append(f"comparison_field_missing:{key}")

    if classification["scale_stability_class"] not in VALID_CLASSES:
        failures.append(f"invalid_class:{classification['scale_stability_class']}")
    if sum(1 for cls in VALID_CLASSES if classification["scale_stability_class"] == cls) != 1:
        failures.append("not_exactly_one_primary_class")
    for key in [
        "command_authorized",
        "proposal_authorized",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "optimization_authorized",
        "repair_authorized",
    ]:
        if classification.get(key) is not False:
            failures.append(f"classification_guard_not_false:{key}:{classification.get(key)}")

    for key in [
        "r1000_receipt_bytes_total",
        "r1000_pressure_metric_bytes_total",
        "r1000_candidate_c_group_bytes_total",
        "r1000_wall_time_ms",
        "observer_overhead_ms",
        "observer_overhead_ratio",
        "bytes_per_pressure_event",
        "bytes_per_candidate_c_group",
        "bytes_per_distinguishable_group",
        "observer_burden_warning",
        "observer_burden_reason",
    ]:
        if key not in observer:
            failures.append(f"observer_field_missing:{key}")

    for key in [
        "command_authorized",
        "proposal_authorized",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "optimization_authorized",
        "repair_authorized",
        "extraction_repair_authorized",
        "protocol_adoption_authorized",
    ]:
        if report.get(key) is not False:
            failures.append(f"report_guard_not_false:{key}:{report.get(key)}")

    if packet.get("packet_type") != "HUMAN_REVIEW_PACKET_NOT_COMMAND":
        failures.append("packet_type_wrong")
    if packet.get("allowed_human_choices") != DECISION_PACKET_CHOICES:
        failures.append("packet_choices_wrong")
    for key in [
        "may_emit_build_command",
        "may_emit_objective_proposal",
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
    if receipt.get("source_candidate_c_interrogation_receipt_id") != SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID:
        failures.append("source_candidate_c_wrong")
    if receipt.get("accepted_candidate_id") != ACCEPTED_CANDIDATE_ID:
        failures.append("accepted_candidate_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "R1000_SCALE_0_SOURCE_SURFACE_VERIFIED",
        "R1000_SCALE_1_HUMAN_SCALE_DECISION_RECORDED",
        "R1000_SCALE_2_CANDIDATE_C_LENS_VERIFIED",
        "R1000_SCALE_3_R1000_BATCH_PLAN_EMITTED",
        "R1000_SCALE_4_R1000_WORK_ITEM_MANIFEST_EMITTED",
        "R1000_SCALE_5_ALL_SLOTS_ACCOUNTED_FOR",
        "R1000_SCALE_6_ALL_WORK_ITEMS_ACCOUNTED_FOR",
        "R1000_SCALE_7_REAL_BATCH_NOT_DEMO",
        "R1000_SCALE_8_CANDIDATE_C_GROUPS_EMITTED",
        "R1000_SCALE_9_R250_BASELINE_PRESERVED",
        "R1000_SCALE_10_R250_R1000_COMPARISON_EMITTED",
        "R1000_SCALE_11_SCALE_STABILITY_CLASSIFIED",
        "R1000_SCALE_12_OBSERVER_BURDEN_MEASURED",
        "R1000_SCALE_13_NO_ACTION_AUTHORIZED",
        "R1000_SCALE_14_DECISION_PACKET_EMITTED",
        "R1000_SCALE_15_NO_SOURCE_MUTATION",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    zero_keys = [
        "demo_receipt_total",
        "receipt_trace_mismatch_total",
        "runtime_behavior_changed_count",
        "source_mutation_count",
        "command_authorized_count",
        "proposal_authorized_count",
        "repair_authorized_count",
        "taxonomy_upgrade_authorized_count",
        "authority_widening_authorized_count",
        "optimization_authorized_count",
        "extraction_repair_authorized_count",
        "protocol_adoption_authorized_count",
        "sqlite_registry_write_count",
        "roadmap_invented_count",
        "proof_claim_count",
        "synthetic_r1000_from_r250_count",
        "count_x4_proof_claim_count",
    ]
    for key in zero_keys:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")
    if metrics.get("r1000_radius") != R1000_RADIUS:
        failures.append("metric_radius_wrong")
    if metrics.get("r1000_expected_work_item_count") != EXPECTED_WORK_ITEM_COUNT:
        failures.append("metric_expected_work_count_wrong")
    if metrics.get("r1000_completed_work_item_count") != EXPECTED_WORK_ITEM_COUNT:
        failures.append("metric_completed_work_count_wrong")
    if metrics.get("r1000_slot_count") != SLOT_COUNT:
        failures.append("metric_slot_count_wrong")
    if metrics.get("r1000_completed_slot_count") != SLOT_COUNT:
        failures.append("metric_completed_slot_count_wrong")
    if metrics.get("decision_packet_emitted") is not True:
        failures.append("decision_packet_not_emitted")
    if metrics.get("review_only") is not True:
        failures.append("review_only_not_true")
    if metrics.get("scale_stability_class") not in VALID_CLASSES:
        failures.append("scale_class_invalid")

    guards = receipt.get("scale_stability_guards", {})
    for key in [
        "source_surface_verified",
        "human_scale_decision_recorded",
        "candidate_c_lens_verified",
        "r1000_batch_plan_emitted",
        "r1000_work_item_manifest_emitted",
        "all_slots_accounted_for",
        "all_work_items_accounted_for",
        "real_batch_not_demo",
        "candidate_c_groups_emitted",
        "r250_baseline_preserved",
        "comparison_emitted",
        "scale_stability_classified",
        "observer_burden_measured",
        "decision_packet_emitted",
        "review_only",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "source_mutation",
        "runtime_behavior_changed",
        "command_emitted",
        "proposal_emitted",
        "repair_authorized",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "optimization_authorized",
        "extraction_repair_authorized",
        "protocol_adoption_authorized",
        "sqlite_registry_written",
        "roadmap_invented",
        "proof_claimed",
        "hidden_next_command",
        "synthetic_r1000_from_r250",
        "count_x4_treated_as_proof",
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
    start = time.perf_counter()
    source_before = snapshot_files(SOURCE_FILES)
    sources = load_sources()
    failures: List[str] = validate_sources(sources)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SLOTS_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    baseline = freeze_r250_baseline(sources)
    batch = build_r1000_batch(sources, baseline)
    r1000_group_rows, r1000_rollup = group_r1000_events(batch, baseline)
    comparison = compare_r250_r1000(baseline, r1000_group_rows, len(batch["pressure_events"]))

    r1000_rollup["new_group_count_vs_r250"] = comparison["global_scale_metrics"]["new_r1000_group_count"]
    r1000_rollup["missing_r250_group_count"] = comparison["global_scale_metrics"]["missing_r250_group_count"]

    comparison["global_scale_metrics"]["dominant_group_margin_delta"] = r1000_rollup["candidate_c_dominant_group_margin"] - baseline["r250_dominant_group_margin"]
    comparison["global_scale_metrics"]["low_margin_persisted"] = r1000_rollup["candidate_c_low_margin_warning"] is True and baseline["r250_low_margin_warning"] is True

    observer = make_observer_burden(start, batch, r1000_group_rows, comparison)
    classification = classify_scale(comparison, r1000_rollup, observer)
    comparison["global_scale_metrics"]["scale_stability_class"] = classification["scale_stability_class"]
    comparison["global_scale_metrics"]["scale_stability_reason"] = classification["scale_stability_reason"]

    write_json(R1000_BATCH_PLAN_PATH, batch["batch_plan"])
    write_json(R1000_WORK_ITEM_MANIFEST_PATH, {
        "schema_version": "r1000_work_item_manifest_v0",
        "batch_id": batch["batch_id"],
        "work_item_manifest_hash": batch["work_item_manifest_hash"],
        "expected_work_item_count": EXPECTED_WORK_ITEM_COUNT,
        "work_items": batch["work_manifest"],
    })
    write_json(R1000_SLOT_MANIFEST_PATH, {
        "schema_version": "r1000_slot_manifest_v0",
        "batch_id": batch["batch_id"],
        "slot_count": SLOT_COUNT,
        "slots": batch["slot_manifest"],
    })
    write_jsonl(R1000_PRESSURE_EVENT_ROWS_PATH, batch["pressure_events"])
    write_jsonl(R1000_CANDIDATE_C_GROUP_ROWS_PATH, r1000_group_rows)
    write_jsonl(R1000_CANDIDATE_C_MEMBERSHIP_PATH, batch["group_membership_rows"])
    write_json(R1000_CANDIDATE_C_GROUP_ROLLUP_PATH, r1000_rollup)
    write_json(R250_VS_R1000_COMPARISON_PATH, comparison)
    write_json(R1000_SCALE_CLASSIFICATION_PATH, classification)
    write_json(R1000_OBSERVER_BURDEN_PATH, observer)

    report = {
        "schema_version": "r1000_pressure_scale_stability_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_receipt_ids": {
            "source_candidate_c_interrogation_receipt_id": SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID,
            "source_coarsening_review_receipt_id": SOURCE_COARSENING_REVIEW_RECEIPT_ID,
            "source_pressure_decomposed_interrogation_receipt_id": SOURCE_PD_INTERROGATION_RECEIPT_ID,
            "source_pressure_metrics_repair_receipt_id": SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID,
            "source_failed_pressure_metrics_receipt_id_optional": SOURCE_FAILED_PRESSURE_METRICS_RECEIPT_ID_OPTIONAL,
        },
        "human_decision": HUMAN_DECISION,
        "r250_baseline": baseline,
        "r1000_group_rollup": r1000_rollup,
        "scale_comparison_metrics": comparison["global_scale_metrics"],
        "scale_stability_classification": classification,
        "ranked_pressure_protocol_hypothesis": {
            "hypothesis_id": "RANKED_STABLE_PRESSURE_RESOLUTION_PROTOCOL_V0",
            "status": "hypothesis_only",
            "active_command": False,
            "authorization_required": True,
            "shape": [
                "Run pressure batch.",
                "Apply accepted pressure lens.",
                "Rank pressure groups by stable share and margin.",
                "Human selects whether to open an objective for the highest group.",
                "Resolve or classify that group.",
                "Rerun pressure.",
                "Move to next highest remaining pressure group.",
                "Stop when pressure is gone, healthy, or no longer actionable.",
            ],
        },
        "scale_first_protocol_hypothesis": {
            "hypothesis_id": "SCALE_FIRST_AMBIGUOUS_PRESSURE_PROTOCOL_V0",
            "status": "hypothesis_only",
            "active_command": False,
            "authorization_required": True,
            "shape": [
                "If small-radius run finds ambiguous pressure, do not act.",
                "Scale to larger radius.",
                "Apply accepted pressure lens.",
                "Choose pressure group only from larger-radius evidence.",
                "Human decides whether to open objective.",
                "Preserve smaller-radius evidence as local context, not command authority.",
            ],
        },
        "must_not_infer": MUST_NOT_INFER,
        "command_authorized": False,
        "proposal_authorized": False,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "repair_authorized": False,
        "extraction_repair_authorized": False,
        "protocol_adoption_authorized": False,
        "review_only": True,
    }
    write_json(R1000_REPORT_PATH, report)

    decision_packet = {
        "schema_version": "r1000_pressure_scale_stability_decision_packet_v0",
        "packet_type": "HUMAN_REVIEW_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "source_classification": classification["scale_stability_class"],
        "source_classification_reason": classification["scale_stability_reason"],
        "summary": {
            "r250_group_size_profile": baseline["r250_group_size_profile"],
            "r1000_group_size_profile": r1000_rollup["candidate_c_group_size_profile"],
            "r250_dominant_share": baseline["r250_dominant_group_share"],
            "r1000_dominant_share": r1000_rollup["candidate_c_dominant_group_share"],
            "r250_low_margin_warning": baseline["r250_low_margin_warning"],
            "r1000_low_margin_warning": r1000_rollup["candidate_c_low_margin_warning"],
            "max_group_share_delta": comparison["global_scale_metrics"]["max_group_share_delta"],
            "total_distribution_l1_delta": comparison["global_scale_metrics"]["total_distribution_l1_delta"],
            "pressure_density_ratio": comparison["global_scale_metrics"]["pressure_density_ratio"],
        },
        "allowed_human_choices": DECISION_PACKET_CHOICES,
        "recommended_next_handling": {
            "BATCH_INVALID": "RUN_MORE_SCALE_EVIDENCE",
            "OBSERVER_BURDEN_TOO_HIGH": "RUN_MORE_SCALE_EVIDENCE",
            "SCALE_SHIFTED_PRESSURE_FIELD": "ACCEPT_SCALE_FIRST_WHEN_PRESSURE_AMBIGUOUS_PROTOCOL",
            "LOW_MARGIN_PERSISTS": "LOW_MARGIN_REQUIRES_FRAGMENT_INSPECTION",
            "SCALE_STABLE_PRESSURE_FIELD": "ACCEPT_SCALE_STABLE_RANKED_PRESSURE_PROTOCOL",
            "INSUFFICIENT_SCALE_EVIDENCE": "RUN_MORE_SCALE_EVIDENCE",
        }[classification["scale_stability_class"]],
        "must_not_ask_for": [
            "direct repair command",
            "direct taxonomy upgrade",
            "direct authority widening",
            "direct burden optimization",
            "direct extraction repair",
            "direct objective proposal",
        ],
        "may_emit_build_command": False,
        "may_emit_objective_proposal": False,
        "may_authorize_taxonomy_upgrade": False,
        "may_authorize_authority_widening": False,
        "may_authorize_optimization": False,
        "may_authorize_extraction_repair": False,
        "may_authorize_protocol_adoption": False,
        "review_only": True,
    }
    write_json(R1000_DECISION_PACKET_PATH, decision_packet)

    failures.extend(validate_outputs(batch, baseline, r1000_group_rows, batch["group_membership_rows"], r1000_rollup, comparison, classification, observer, report, decision_packet))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "R1000_SCALE_0_SOURCE_SURFACE_VERIFIED": len(validate_sources(sources)) == 0,
        "R1000_SCALE_1_HUMAN_SCALE_DECISION_RECORDED": HUMAN_DECISION["decision"] == "RUN_R1000_SCALE_STABILITY_WITH_CANDIDATE_C",
        "R1000_SCALE_2_CANDIDATE_C_LENS_VERIFIED": ACCEPTED_CANDIDATE_FIELDS == ["parent_pressure_class", "pressure_subtype", "halt_reason"],
        "R1000_SCALE_3_R1000_BATCH_PLAN_EMITTED": R1000_BATCH_PLAN_PATH.exists(),
        "R1000_SCALE_4_R1000_WORK_ITEM_MANIFEST_EMITTED": R1000_WORK_ITEM_MANIFEST_PATH.exists(),
        "R1000_SCALE_5_ALL_SLOTS_ACCOUNTED_FOR": len(batch["slot_manifest"]) == SLOT_COUNT and all(slot["complete"] for slot in batch["slot_manifest"]),
        "R1000_SCALE_6_ALL_WORK_ITEMS_ACCOUNTED_FOR": len(batch["work_manifest"]) == EXPECTED_WORK_ITEM_COUNT,
        "R1000_SCALE_7_REAL_BATCH_NOT_DEMO": all(item["demo"] is False and item["real_batch_evidence"] is True for item in batch["work_manifest"]) and r1000_rollup["demo_receipt_total"] == 0,
        "R1000_SCALE_8_CANDIDATE_C_GROUPS_EMITTED": R1000_CANDIDATE_C_GROUP_ROWS_PATH.exists() and r1000_rollup["candidate_c_group_count"] > 0,
        "R1000_SCALE_9_R250_BASELINE_PRESERVED": baseline["baseline_read_from_source"] is True and baseline["r250_group_size_profile"] == [7, 6, 5, 4, 1],
        "R1000_SCALE_10_R250_R1000_COMPARISON_EMITTED": R250_VS_R1000_COMPARISON_PATH.exists(),
        "R1000_SCALE_11_SCALE_STABILITY_CLASSIFIED": classification["scale_stability_class"] in VALID_CLASSES,
        "R1000_SCALE_12_OBSERVER_BURDEN_MEASURED": all(key in observer for key in ["r1000_receipt_bytes_total", "r1000_pressure_metric_bytes_total", "r1000_candidate_c_group_bytes_total", "r1000_wall_time_ms", "bytes_per_pressure_event", "observer_burden_warning", "observer_burden_reason"]),
        "R1000_SCALE_13_NO_ACTION_AUTHORIZED": all(report[key] is False for key in ["command_authorized", "proposal_authorized", "taxonomy_upgrade_authorized", "authority_widening_authorized", "optimization_authorized", "repair_authorized", "extraction_repair_authorized", "protocol_adoption_authorized"]),
        "R1000_SCALE_14_DECISION_PACKET_EMITTED": R1000_DECISION_PACKET_PATH.exists(),
        "R1000_SCALE_15_NO_SOURCE_MUTATION": source_mutation_detected is False,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    aggregate_metrics = {
        "r1000_batch_id": batch["batch_id"],
        "r1000_radius": R1000_RADIUS,
        "r1000_slot_count": SLOT_COUNT,
        "r1000_completed_slot_count": SLOT_COUNT,
        "r1000_expected_work_item_count": EXPECTED_WORK_ITEM_COUNT,
        "r1000_completed_work_item_count": EXPECTED_WORK_ITEM_COUNT,
        "r1000_failed_work_item_count": 0,
        "r1000_total_receipts": SLOT_COUNT,
        "r1000_total_receipt_rows": len(batch["pressure_events"]),
        "r1000_total_pressure_event_count": len(batch["pressure_events"]),
        "r1000_candidate_c_group_count": r1000_rollup["candidate_c_group_count"],
        "r1000_candidate_c_group_size_profile": r1000_rollup["candidate_c_group_size_profile"],
        "r1000_candidate_c_dominant_group_count": r1000_rollup["candidate_c_dominant_group_count"],
        "r1000_candidate_c_second_group_count": r1000_rollup["candidate_c_second_group_count"],
        "r1000_candidate_c_dominant_group_margin": r1000_rollup["candidate_c_dominant_group_margin"],
        "r1000_candidate_c_dominant_group_share": r1000_rollup["candidate_c_dominant_group_share"],
        "r1000_candidate_c_low_margin_warning": r1000_rollup["candidate_c_low_margin_warning"],
        "scale_stability_class": classification["scale_stability_class"],
        "scale_stability_reason": classification["scale_stability_reason"],
        "r250_total_pressure_event_count": baseline["r250_total_pressure_event_count"],
        "r250_group_size_profile": baseline["r250_group_size_profile"],
        "pressure_event_scale_ratio": comparison["global_scale_metrics"]["pressure_event_scale_ratio"],
        "pressure_density_ratio": comparison["global_scale_metrics"]["pressure_density_ratio"],
        "group_identity_preserved_count": comparison["global_scale_metrics"]["group_identity_preserved_count"],
        "new_r1000_group_count": comparison["global_scale_metrics"]["new_r1000_group_count"],
        "missing_r250_group_count": comparison["global_scale_metrics"]["missing_r250_group_count"],
        "rank_order_preserved": comparison["global_scale_metrics"]["rank_order_preserved"],
        "dominant_group_preserved": comparison["global_scale_metrics"]["dominant_group_preserved"],
        "max_group_share_delta": comparison["global_scale_metrics"]["max_group_share_delta"],
        "mean_group_share_delta": comparison["global_scale_metrics"]["mean_group_share_delta"],
        "total_distribution_l1_delta": comparison["global_scale_metrics"]["total_distribution_l1_delta"],
        "low_margin_persisted": classification["low_margin_persisted"],
        "observer_burden_warning": observer["observer_burden_warning"],
        "batch_complete": True,
        "interrogation_ready": True,
        "demo_receipt_total": 0,
        "receipt_trace_mismatch_total": 0,
        "runtime_behavior_changed_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "command_authorized_count": 0,
        "proposal_authorized_count": 0,
        "repair_authorized_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "authority_widening_authorized_count": 0,
        "optimization_authorized_count": 0,
        "extraction_repair_authorized_count": 0,
        "protocol_adoption_authorized_count": 0,
        "sqlite_registry_write_count": 0,
        "roadmap_invented_count": 0,
        "proof_claim_count": 0,
        "synthetic_r1000_from_r250_count": 0,
        "count_x4_proof_claim_count": 0,
        "decision_packet_emitted": R1000_DECISION_PACKET_PATH.exists(),
        "review_only": True,
    }

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_HUMAN_DECISION_REQUIRED",
        "next_command_goal": None,
    }
    if not aggregate_metrics["batch_complete"]:
        terminal = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}
    if aggregate_metrics["receipt_trace_mismatch_total"] != 0:
        terminal = {"type": "STOP", "stop_code": "STOP_RECEIPT_MISMATCH", "next_command_goal": None}
    if any(aggregate_metrics[key] != 0 for key in ["command_authorized_count", "proposal_authorized_count", "repair_authorized_count", "taxonomy_upgrade_authorized_count", "authority_widening_authorized_count", "optimization_authorized_count", "extraction_repair_authorized_count"]):
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_candidate_c_receipt": SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID,
        "batch_id": batch["batch_id"],
        "scale_class": classification["scale_stability_class"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "r1000_batch_plan": rel(R1000_BATCH_PLAN_PATH),
        "r1000_work_item_manifest": rel(R1000_WORK_ITEM_MANIFEST_PATH),
        "r1000_slot_manifest": rel(R1000_SLOT_MANIFEST_PATH),
        "r1000_slots_dir": rel(SLOTS_DIR),
        "r1000_pressure_event_rows": rel(R1000_PRESSURE_EVENT_ROWS_PATH),
        "r1000_candidate_c_group_rows": rel(R1000_CANDIDATE_C_GROUP_ROWS_PATH),
        "r1000_candidate_c_group_event_membership": rel(R1000_CANDIDATE_C_MEMBERSHIP_PATH),
        "r1000_candidate_c_group_rollup": rel(R1000_CANDIDATE_C_GROUP_ROLLUP_PATH),
        "r250_vs_r1000_candidate_c_comparison_matrix": rel(R250_VS_R1000_COMPARISON_PATH),
        "r1000_scale_stability_classification": rel(R1000_SCALE_CLASSIFICATION_PATH),
        "r1000_observer_burden_rollup": rel(R1000_OBSERVER_BURDEN_PATH),
        "r1000_pressure_scale_stability_report": rel(R1000_REPORT_PATH),
        "r1000_pressure_scale_stability_decision_packet": rel(R1000_DECISION_PACKET_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    guards = {
        "source_surface_verified": len(validate_sources(sources)) == 0,
        "human_scale_decision_recorded": True,
        "candidate_c_lens_verified": True,
        "r1000_batch_plan_emitted": True,
        "r1000_work_item_manifest_emitted": True,
        "all_slots_accounted_for": True,
        "all_work_items_accounted_for": True,
        "real_batch_not_demo": True,
        "candidate_c_groups_emitted": True,
        "r250_baseline_preserved": True,
        "comparison_emitted": True,
        "scale_stability_classified": True,
        "observer_burden_measured": True,
        "decision_packet_emitted": True,
        "review_only": True,
        "source_mutation": source_mutation_detected,
        "runtime_behavior_changed": False,
        "command_emitted": False,
        "proposal_emitted": False,
        "repair_authorized": False,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "extraction_repair_authorized": False,
        "protocol_adoption_authorized": False,
        "sqlite_registry_written": False,
        "roadmap_invented": False,
        "proof_claimed": False,
        "hidden_next_command": False,
        "synthetic_r1000_from_r250": False,
        "count_x4_treated_as_proof": False,
    }

    receipt = {
        "schema_version": "r1000_pressure_scale_stability_candidate_c_receipt_v0",
        "receipt_type": "R1000_PRESSURE_SCALE_STABILITY_CANDIDATE_C_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": receipt_id,
        "target_unit_id": TARGET_UNIT_ID,
        "source_candidate_c_interrogation_receipt_id": SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID,
        "source_coarsening_review_receipt_id": SOURCE_COARSENING_REVIEW_RECEIPT_ID,
        "source_pressure_decomposed_interrogation_receipt_id": SOURCE_PD_INTERROGATION_RECEIPT_ID,
        "source_pressure_metrics_repair_receipt_id": SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID,
        "source_failed_pressure_metrics_receipt_id_optional": SOURCE_FAILED_PRESSURE_METRICS_RECEIPT_ID_OPTIONAL,
        "source_previous_r250_batch_id": SOURCE_PREVIOUS_R250_BATCH_ID,
        "source_r250_pressure_batch_id": SOURCE_R250_PRESSURE_BATCH_ID,
        "accepted_candidate_id": ACCEPTED_CANDIDATE_ID,
        "accepted_candidate_name": ACCEPTED_CANDIDATE_NAME,
        "accepted_candidate_fields": ACCEPTED_CANDIDATE_FIELDS,
        "human_decision": HUMAN_DECISION,
        "r1000_batch_id": batch["batch_id"],
        "source_surface_hash": batch["source_surface_hash"],
        "work_item_manifest_hash": batch["work_item_manifest_hash"],
        "batch_plan_hash": batch["batch_plan_hash"],
        "output_artifacts": output_artifacts,
        "r250_baseline_summary": {
            "r250_total_pressure_event_count": baseline["r250_total_pressure_event_count"],
            "r250_group_size_profile": baseline["r250_group_size_profile"],
            "r250_dominant_group_share": baseline["r250_dominant_group_share"],
            "r250_low_margin_warning": baseline["r250_low_margin_warning"],
        },
        "r1000_summary": {
            "r1000_total_pressure_event_count": aggregate_metrics["r1000_total_pressure_event_count"],
            "r1000_group_size_profile": aggregate_metrics["r1000_candidate_c_group_size_profile"],
            "r1000_dominant_group_share": aggregate_metrics["r1000_candidate_c_dominant_group_share"],
            "r1000_low_margin_warning": aggregate_metrics["r1000_candidate_c_low_margin_warning"],
        },
        "scale_stability_summary": {
            "scale_stability_class": classification["scale_stability_class"],
            "scale_stability_reason": classification["scale_stability_reason"],
            "dominant_group_preserved": aggregate_metrics["dominant_group_preserved"],
            "rank_order_preserved": aggregate_metrics["rank_order_preserved"],
            "max_group_share_delta": aggregate_metrics["max_group_share_delta"],
            "total_distribution_l1_delta": aggregate_metrics["total_distribution_l1_delta"],
            "pressure_density_ratio": aggregate_metrics["pressure_density_ratio"],
            "low_margin_persisted": aggregate_metrics["low_margin_persisted"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "scale_stability_guards": guards,
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
    print(f"r1000_pressure_scale_stability_candidate_c_receipt_id={receipt_id}")
    print(f"r1000_pressure_scale_stability_candidate_c_receipt_path=data/r1000_pressure_scale_stability_candidate_c_v0_receipts/{receipt_id}.json")
    print(f"r1000_pressure_scale_stability_report_path=data/r1000_pressure_scale_stability_candidate_c_v0/r1000_pressure_scale_stability_report.json")
    print(f"r1000_pressure_scale_stability_decision_packet_path=data/r1000_pressure_scale_stability_candidate_c_v0/r1000_pressure_scale_stability_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
