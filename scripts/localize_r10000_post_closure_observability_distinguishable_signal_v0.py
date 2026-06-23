#!/usr/bin/env python3
from __future__ import annotations

import collections
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "LOCALIZE_R10000_POST_CLOSURE_OBSERVABILITY_DISTINGUISHABLE_SIGNAL_V0"
TARGET_UNIT_ID = "r1000.post_closure_observability_harvest.r10000_distinguishable_signal.localization.v0"

SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID = "293faf9e"
SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID = "90042e28"
SOURCE_RADIUS_10000_RETRY_RECEIPT_ID = "bb2c8ce3"
SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID = "02711ff1"
SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID = "52d0ea8d"
SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID = "db7c0af2"
RUN_ID = "run_6b1b2494"
EXPECTED_RADIUS = 10000

OUT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0_receipts"

LOCALIZATION_PLAN_PATH = OUT_DIR / "r10000_distinguishable_signal_localization_plan.json"
SOURCE_SURFACE_PATH = OUT_DIR / "r10000_distinguishable_signal_source_surface.json"
FIELD_CARDINALITY_PROFILE_PATH = OUT_DIR / "r10000_distinguishable_signal_field_cardinality_profile.json"
VOLATILITY_CLASSIFICATION_PATH = OUT_DIR / "r10000_distinguishable_signal_volatility_classification.json"
SHAPE_REDUCTION_EXPERIMENT_PATH = OUT_DIR / "r10000_distinguishable_signal_shape_reduction_experiment.json"
SIGNAL_DRIVER_PROFILE_PATH = OUT_DIR / "r10000_distinguishable_signal_driver_profile.json"
LOCALIZATION_PACKET_PATH = OUT_DIR / "r10000_distinguishable_signal_localization_packet.json"
NEXT_DECISION_PACKET_PATH = OUT_DIR / "r10000_distinguishable_signal_localization_next_decision_packet.json"
LOCALIZATION_DECISION_PATH = OUT_DIR / "r10000_distinguishable_signal_localization_decision.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r10000_distinguishable_signal_localization_transition_trace.json"
REPORT_PATH = OUT_DIR / "r10000_distinguishable_signal_localization_report.json"

SIGNAL_INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_inspection_v0_receipts" / f"{SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID}.json"
SIGNAL_CLASSIFICATION_PACKET_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_inspection_v0" / "r1000_post_closure_observability_harvest_radius_10000_signal_classification_packet.json"
SIGNAL_NEXT_DECISION_PACKET_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_inspection_v0" / "r1000_post_closure_observability_harvest_radius_10000_signal_inspection_next_decision_packet.json"
SIGNAL_OBSERVATION_STREAM_PROFILE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_inspection_v0" / "r1000_post_closure_observability_harvest_radius_10000_observation_stream_profile.json"
SIGNAL_DISTINGUISHABILITY_PROFILE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_inspection_v0" / "r1000_post_closure_observability_harvest_radius_10000_distinguishability_profile.json"
SIGNAL_ROLLUP_PROFILE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_inspection_v0" / "r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_rollup_profile.json"

RESULT_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_result_review_v0_receipts" / f"{SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID}.json"
RETRY_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_retry_with_cli_wrapper_intercept_parse_fixed_v0_receipts" / f"{SOURCE_RADIUS_10000_RETRY_RECEIPT_ID}.json"

RUN_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_runs_v0" / RUN_ID
OBS_RECEIPT_DIR = RUN_DIR / "receipts"
RUN_RECEIPT_PATH = RUN_DIR / "run_receipt.json"
ROLLUP_PATH = RUN_DIR / "rollup.json"
RECEIPT_INDEX_PATH = RUN_DIR / "receipt_index.jsonl"

CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_intercept_parse_fix_v0_receipts" / f"{SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID}.json"
CLOSURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0_receipts" / f"{SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID}.json"
CLOSED_QUEUE_HANDOFF_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0" / "r1000_pressure_queue_closed_handoff_after_synthetic_remainder_expected_limit.json"
EXPECTED_LIMIT_MARK_RECEIPT_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID}.json"
FINAL_QUEUE_STATE_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_final_pressure_queue_state_after_synthetic_remainder_expected_limit.json"

CLI_PATH = ROOT / "src" / "matrixlab" / "cli.py"
ENTRYPOINT_MODULE_PATH = ROOT / "src" / "matrixlab" / "r1000_post_closure_observability_harvest.py"

SOURCE_FILES = [
    SIGNAL_INSPECTION_RECEIPT_PATH,
    SIGNAL_CLASSIFICATION_PACKET_PATH,
    SIGNAL_NEXT_DECISION_PACKET_PATH,
    SIGNAL_OBSERVATION_STREAM_PROFILE_PATH,
    SIGNAL_DISTINGUISHABILITY_PROFILE_PATH,
    SIGNAL_ROLLUP_PROFILE_PATH,
    RESULT_REVIEW_RECEIPT_PATH,
    RETRY_RECEIPT_PATH,
    RUN_RECEIPT_PATH,
    ROLLUP_PATH,
    RECEIPT_INDEX_PATH,
    CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_PATH,
    CLOSURE_REVIEW_RECEIPT_PATH,
    CLOSED_QUEUE_HANDOFF_PATH,
    EXPECTED_LIMIT_MARK_RECEIPT_PATH,
    FINAL_QUEUE_STATE_PATH,
    CLI_PATH,
    ENTRYPOINT_MODULE_PATH,
]

HUMAN_DECISION = {
    "decision": "LOCALIZE_R10000_POST_CLOSURE_OBSERVABILITY_DISTINGUISHABLE_SIGNAL",
    "scope": "analyze the existing radius-10000 observation run properly by localizing why the receipt stream is distinguishable; identify whether the signal is semantic/structural or merely receipt-volatility/index noise; emit a next decision packet without rerunning, repairing, reopening the queue, or materializing row payloads",
    "source_r10000_signal_inspection_receipt_id": SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID,
    "authorized": [
        "consume R10000 signal inspection receipt",
        "read existing observation receipts from the accepted radius-10000 run",
        "aggregate field cardinality and shape-reduction profiles",
        "classify volatile versus stable distinguishability drivers",
        "localize signal source class",
        "emit next decision packet",
        "stop before repair, rerun, scaling, or row payload work",
    ],
    "not_authorized": [
        "rerunning radius-10000",
        "running radius above 10000",
        "running unbounded/no-cap harvest",
        "running any small probe",
        "modifying src/matrixlab/cli.py",
        "modifying src/matrixlab/r1000_post_closure_observability_harvest.py",
        "reopening R1000 pressure queue",
        "inspecting closed groups",
        "materializing row payloads",
        "assigning identity values",
        "inventing values",
        "running repair in this unit",
        "applying taxonomy changes",
        "mutating prior artifacts",
        "mutating existing receipts",
        "hiding next command",
    ],
}

VOLATILE_KEY_RE = re.compile(
    r"(^|\.|\[)(created_at|updated_at|timestamp|ts_utc|ts|receipt_id|observation_receipt_id|"
    r"receipt_path|path|sha256|sha8|hash|sig8|run_id|observation_index|index|sequence|seq|"
    r"uuid|id|elapsed_seconds|runtime_seconds|duration|wall_time|filename|file_path|"
    r"source_path|artifact_path|canonical_hash)(\]|\b|_|$)"
)

PROTECTED_PAYLOAD_RE = re.compile(r"(row_payload|closed_group|materialized|raw_source_content)", re.IGNORECASE)

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

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def norm_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    return text if len(text) <= 180 else text[:177] + "..."

def iter_flat(obj: Any, prefix: str = "") -> Iterable[Tuple[str, Any]]:
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            yield from iter_flat(v, key)
    elif isinstance(obj, list):
        yield f"{prefix}.__list_len__", len(obj)
        for i, v in enumerate(obj[:10]):
            key = f"{prefix}[{i}]"
            yield from iter_flat(v, key)
    else:
        yield prefix, obj

def scrub_obj(obj: Any, mode: str) -> Any:
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            lk = str(k)
            drop = False
            if mode in {"volatile", "aggressive"} and VOLATILE_KEY_RE.search(lk):
                drop = True
            if mode == "aggressive" and (lk.endswith("_id") or lk.endswith("_path") or "hash" in lk or "sha" in lk):
                drop = True
            if drop:
                continue
            out[k] = scrub_obj(v, mode)
        return out
    if isinstance(obj, list):
        if mode == "structure_only":
            return f"__list_len__:{len(obj)}"
        return [scrub_obj(v, mode) for v in obj]
    if mode == "structure_only":
        return type(obj).__name__
    return obj

def receipt_shape_hash(obj: Dict[str, Any], mode: str) -> str:
    return sha8(scrub_obj(obj, mode))

def entropy(counter: collections.Counter) -> float:
    total = sum(counter.values())
    if total <= 0:
        return 0.0
    h = 0.0
    for c in counter.values():
        p = c / total
        h -= p * math.log2(p)
    return h

def validate_sources() -> List[str]:
    failures: List[str] = []
    signal_receipt = read_json(SIGNAL_INSPECTION_RECEIPT_PATH)
    signal_packet = read_json(SIGNAL_CLASSIFICATION_PACKET_PATH)
    stream = read_json(SIGNAL_OBSERVATION_STREAM_PROFILE_PATH)
    rollup = read_json(ROLLUP_PATH)
    run_receipt = read_json(RUN_RECEIPT_PATH)
    closure = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if signal_receipt.get("receipt_id") != SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID:
        failures.append("signal_inspection_receipt_id_wrong")
    if signal_receipt.get("gate") != "PASS":
        failures.append("signal_inspection_gate_not_pass")
    summary = signal_receipt.get("radius_10000_signal_inspection_summary", {})
    if summary.get("signal_classification") != "R10000_SIGNAL_CLASS_DISTINGUISHABLE_CLEAN_SIGNAL_REVIEW_READY":
        failures.append("signal_inspection_classification_not_distinguishable_clean")
    if summary.get("recommended_next_handling") != UNIT_ID:
        failures.append("signal_inspection_not_recommending_this_unit")
    if signal_packet.get("recommended_next_handling") != UNIT_ID:
        failures.append("signal_packet_not_recommending_this_unit")
    if stream.get("receipt_files_seen") != EXPECTED_RADIUS or stream.get("parse_failure_count") != 0:
        failures.append("prior_stream_profile_not_clean_10000")

    if run_receipt.get("gate") != "PASS":
        failures.append("run_receipt_gate_not_pass")
    if run_receipt.get("radius_completed") != EXPECTED_RADIUS or run_receipt.get("observation_receipt_count") != EXPECTED_RADIUS:
        failures.append("run_receipt_not_radius_10000")
    if rollup.get("gate") != "PASS":
        failures.append("rollup_gate_not_pass")
    if rollup.get("radius_completed") != EXPECTED_RADIUS or rollup.get("observation_receipt_count") != EXPECTED_RADIUS:
        failures.append("rollup_not_radius_10000")

    if closure.get("gate") != "PASS":
        failures.append("closure_review_not_pass")
    if handoff.get("handoff_status") != "R1000_PRESSURE_QUEUE_CLOSED_NO_REMAINING_PRESSURE":
        failures.append("closed_queue_handoff_status_wrong")
    if final_queue.get("queue_state_status") != "R1000_PRESSURE_QUEUE_CLOSED":
        failures.append("final_queue_not_closed")
    if final_queue.get("remaining_open_group_count") != 0 or final_queue.get("remaining_open_row_count") != 0:
        failures.append("final_queue_has_remaining_pressure")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
    if not OBS_RECEIPT_DIR.exists():
        failures.append(f"source_missing:{rel(OBS_RECEIPT_DIR)}")
    if len(sorted(OBS_RECEIPT_DIR.glob("*.json"))) != EXPECTED_RADIUS:
        failures.append("observation_receipt_dir_not_10000")
    return failures

def load_receipts() -> List[Tuple[Path, Dict[str, Any]]]:
    loaded: List[Tuple[Path, Dict[str, Any]]] = []
    for path in sorted(OBS_RECEIPT_DIR.glob("*.json")):
        obj = read_json(path)
        loaded.append((path, obj))
    return loaded

def build_source_surface() -> Dict[str, Any]:
    signal_receipt = read_json(SIGNAL_INSPECTION_RECEIPT_PATH)
    signal_packet = read_json(SIGNAL_CLASSIFICATION_PACKET_PATH)
    prior_dist = read_json(SIGNAL_DISTINGUISHABILITY_PROFILE_PATH)
    rollup = read_json(ROLLUP_PATH)
    run_receipt = read_json(RUN_RECEIPT_PATH)
    return {
        "schema_version": "r10000_distinguishable_signal_source_surface_v0",
        "source_r10000_signal_inspection_receipt_id": SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID,
        "run_id": RUN_ID,
        "run_dir": rel(RUN_DIR),
        "prior_signal_summary": signal_receipt.get("radius_10000_signal_inspection_summary"),
        "prior_signal_classification_packet": signal_packet,
        "prior_distinguishability_profile": prior_dist.get("distinguishability"),
        "run_receipt_core": {
            "gate": run_receipt.get("gate"),
            "radius_completed": run_receipt.get("radius_completed"),
            "observation_receipt_count": run_receipt.get("observation_receipt_count"),
            "terminal": run_receipt.get("terminal"),
        },
        "rollup_core": {
            "gate": rollup.get("gate"),
            "radius_completed": rollup.get("radius_completed"),
            "observation_receipt_count": rollup.get("observation_receipt_count"),
            "runtime_seconds": rollup.get("runtime_seconds"),
            "observation_write_rate_per_second": rollup.get("observation_write_rate_per_second"),
        },
    }

def build_field_cardinality_profile(receipts: List[Tuple[Path, Dict[str, Any]]]) -> Dict[str, Any]:
    key_occurrences = collections.Counter()
    value_counters: Dict[str, collections.Counter] = {}
    sample_values: Dict[str, List[str]] = collections.defaultdict(list)
    protected_payload_key_hits = []

    for path, obj in receipts:
        for key, value in iter_flat(obj):
            if PROTECTED_PAYLOAD_RE.search(key):
                protected_payload_key_hits.append({"path": rel(path), "key": key})
                continue
            key_occurrences[key] += 1
            s = norm_scalar(value)
            value_counters.setdefault(key, collections.Counter())[s] += 1
            if len(sample_values[key]) < 5 and s not in sample_values[key]:
                sample_values[key].append(s)

    fields = []
    for key, counter in value_counters.items():
        count = sum(counter.values())
        distinct = len(counter)
        fields.append({
            "key": key,
            "occurrence_count": key_occurrences[key],
            "distinct_value_count": distinct,
            "distinct_ratio": round(distinct / max(1, count), 6),
            "entropy_bits": round(entropy(counter), 6),
            "volatile_key_rule_match": bool(VOLATILE_KEY_RE.search(key)),
            "top_values": dict(counter.most_common(8)),
            "sample_values": sample_values[key],
        })

    fields_sorted = sorted(
        fields,
        key=lambda x: (x["distinct_value_count"], x["entropy_bits"], x["occurrence_count"]),
        reverse=True,
    )

    return {
        "schema_version": "r10000_distinguishable_signal_field_cardinality_profile_v0",
        "run_id": RUN_ID,
        "receipt_files_seen": len(receipts),
        "flat_field_count": len(fields_sorted),
        "protected_payload_key_hit_count": len(protected_payload_key_hits),
        "protected_payload_key_hit_samples": protected_payload_key_hits[:20],
        "highest_cardinality_fields_top_100": fields_sorted[:100],
        "stable_fields_count": sum(1 for f in fields_sorted if f["distinct_value_count"] == 1),
        "fully_unique_fields_count": sum(1 for f in fields_sorted if f["distinct_value_count"] == len(receipts)),
        "volatile_rule_unique_fields": [
            f for f in fields_sorted
            if f["distinct_value_count"] == len(receipts) and f["volatile_key_rule_match"]
        ][:100],
        "nonvolatile_high_cardinality_fields": [
            f for f in fields_sorted
            if f["distinct_value_count"] > 1 and not f["volatile_key_rule_match"]
        ][:100],
    }

def build_volatility_classification(cardinality: Dict[str, Any]) -> Dict[str, Any]:
    high = cardinality["highest_cardinality_fields_top_100"]
    volatile = []
    structural = []
    ambiguous = []
    for f in high:
        key = f["key"]
        if f["volatile_key_rule_match"]:
            volatile.append({**f, "driver_class": "VOLATILE_RECEIPT_METADATA_OR_INDEX"})
        elif f["distinct_value_count"] == EXPECTED_RADIUS and (
            key.endswith("path")
            or key.endswith("_path")
            or "receipt" in key
            or "hash" in key
            or "sha" in key
        ):
            volatile.append({**f, "driver_class": "LIKELY_VOLATILE_ARTIFACT_REFERENCE"})
        elif f["distinct_value_count"] > 1:
            structural.append({**f, "driver_class": "NONVOLATILE_STRUCTURAL_OR_SEMANTIC_FIELD"})
        else:
            ambiguous.append({**f, "driver_class": "STABLE_OR_LOW_SIGNAL_FIELD"})

    return {
        "schema_version": "r10000_distinguishable_signal_volatility_classification_v0",
        "run_id": RUN_ID,
        "volatile_driver_count_top_100": len(volatile),
        "nonvolatile_structural_driver_count_top_100": len(structural),
        "ambiguous_driver_count_top_100": len(ambiguous),
        "volatile_drivers_top_50": volatile[:50],
        "nonvolatile_structural_drivers_top_50": structural[:50],
        "ambiguous_drivers_top_25": ambiguous[:25],
    }

def build_shape_reduction_experiment(receipts: List[Tuple[Path, Dict[str, Any]]]) -> Dict[str, Any]:
    raw_counts = collections.Counter()
    volatile_scrub_counts = collections.Counter()
    aggressive_scrub_counts = collections.Counter()
    structure_only_counts = collections.Counter()

    for _, obj in receipts:
        raw_counts[receipt_shape_hash(obj, "raw")] += 1
        volatile_scrub_counts[receipt_shape_hash(obj, "volatile")] += 1
        aggressive_scrub_counts[receipt_shape_hash(obj, "aggressive")] += 1
        structure_only_counts[receipt_shape_hash(obj, "structure_only")] += 1

    raw_shape_count = len(raw_counts)
    volatile_shape_count = len(volatile_scrub_counts)
    aggressive_shape_count = len(aggressive_scrub_counts)
    structure_only_shape_count = len(structure_only_counts)

    if volatile_shape_count == 1:
        reduction_class = "DISTINGUISHABILITY_COLLAPSES_AFTER_VOLATILE_METADATA_SCRUB"
    elif aggressive_shape_count == 1:
        reduction_class = "DISTINGUISHABILITY_COLLAPSES_AFTER_AGGRESSIVE_ID_PATH_HASH_SCRUB"
    elif structure_only_shape_count == 1:
        reduction_class = "DISTINGUISHABILITY_VALUE_DRIVEN_BUT_STRUCTURE_UNIFORM"
    else:
        reduction_class = "DISTINGUISHABILITY_STRUCTURE_OR_NONVOLATILE_VALUE_DRIVEN"

    return {
        "schema_version": "r10000_distinguishable_signal_shape_reduction_experiment_v0",
        "run_id": RUN_ID,
        "receipt_files_seen": len(receipts),
        "raw_shape_count": raw_shape_count,
        "volatile_scrub_shape_count": volatile_shape_count,
        "aggressive_scrub_shape_count": aggressive_shape_count,
        "structure_only_shape_count": structure_only_shape_count,
        "raw_shape_counts_top_10": dict(raw_counts.most_common(10)),
        "volatile_scrub_shape_counts_top_10": dict(volatile_scrub_counts.most_common(10)),
        "aggressive_scrub_shape_counts_top_10": dict(aggressive_scrub_counts.most_common(10)),
        "structure_only_shape_counts_top_10": dict(structure_only_counts.most_common(10)),
        "reduction_class": reduction_class,
    }

def build_signal_driver_profile(cardinality: Dict[str, Any], volatility: Dict[str, Any], shape_exp: Dict[str, Any]) -> Dict[str, Any]:
    nonvolatile = volatility["nonvolatile_structural_drivers_top_50"]
    volatile = volatility["volatile_drivers_top_50"]

    if shape_exp["reduction_class"] in {
        "DISTINGUISHABILITY_COLLAPSES_AFTER_VOLATILE_METADATA_SCRUB",
        "DISTINGUISHABILITY_COLLAPSES_AFTER_AGGRESSIVE_ID_PATH_HASH_SCRUB",
    } and not nonvolatile:
        driver_class = "RECEIPT_VOLATILITY_ONLY_NO_STRUCTURAL_SIGNAL_LOCALIZED"
    elif shape_exp["reduction_class"] == "DISTINGUISHABILITY_VALUE_DRIVEN_BUT_STRUCTURE_UNIFORM" and nonvolatile:
        driver_class = "NONVOLATILE_VALUE_SIGNAL_STRUCTURE_UNIFORM"
    elif shape_exp["reduction_class"] == "DISTINGUISHABILITY_STRUCTURE_OR_NONVOLATILE_VALUE_DRIVEN":
        driver_class = "STRUCTURAL_OR_NONVOLATILE_SIGNAL_REMAINS_AFTER_SCRUB"
    elif nonvolatile:
        driver_class = "MIXED_VOLATILE_AND_NONVOLATILE_SIGNAL"
    else:
        driver_class = "SIGNAL_LOCALIZATION_INCONCLUSIVE"

    return {
        "schema_version": "r10000_distinguishable_signal_driver_profile_v0",
        "run_id": RUN_ID,
        "driver_class": driver_class,
        "shape_reduction_class": shape_exp["reduction_class"],
        "raw_shape_count": shape_exp["raw_shape_count"],
        "volatile_scrub_shape_count": shape_exp["volatile_scrub_shape_count"],
        "aggressive_scrub_shape_count": shape_exp["aggressive_scrub_shape_count"],
        "structure_only_shape_count": shape_exp["structure_only_shape_count"],
        "volatile_driver_count_top_50": len(volatile),
        "nonvolatile_driver_count_top_50": len(nonvolatile),
        "top_volatile_drivers": volatile[:10],
        "top_nonvolatile_drivers": nonvolatile[:10],
        "interpretation": {
            "RECEIPT_VOLATILITY_ONLY_NO_STRUCTURAL_SIGNAL_LOCALIZED": "The apparent 10k distinguishability is explained by per-receipt metadata or index/reference volatility; the clean observation shape collapses after scrub.",
            "NONVOLATILE_VALUE_SIGNAL_STRUCTURE_UNIFORM": "Receipts share structure but carry nonvolatile value variation worth localizing further.",
            "STRUCTURAL_OR_NONVOLATILE_SIGNAL_REMAINS_AFTER_SCRUB": "Distinguishability remains after volatile scrubbing and should be localized through nonvolatile fields or receipt structure.",
            "MIXED_VOLATILE_AND_NONVOLATILE_SIGNAL": "Both volatile and nonvolatile fields contribute to distinguishability.",
            "SIGNAL_LOCALIZATION_INCONCLUSIVE": "The existing profile did not isolate a trustworthy driver class.",
        }[driver_class],
    }

def build_localization_packet(driver_profile: Dict[str, Any]) -> Dict[str, Any]:
    driver_class = driver_profile["driver_class"]
    if driver_class == "RECEIPT_VOLATILITY_ONLY_NO_STRUCTURAL_SIGNAL_LOCALIZED":
        classification = "R10000_LOCALIZATION_VOLATILE_RECEIPT_METADATA_ONLY"
        recommended = "DECIDE_CLOSE_OR_FREEZE_BOUNDED_OBSERVABILITY_PROTOCOL_AFTER_R10000_VOLATILE_ONLY_SIGNAL_V0"
        requires_repair = False
        requires_localization = False
    elif driver_class in {"NONVOLATILE_VALUE_SIGNAL_STRUCTURE_UNIFORM", "MIXED_VOLATILE_AND_NONVOLATILE_SIGNAL"}:
        classification = "R10000_LOCALIZATION_NONVOLATILE_VALUE_SIGNAL_PRESENT"
        recommended = "LOCALIZE_R10000_NONVOLATILE_OBSERVABILITY_FIELD_SIGNAL_V0"
        requires_repair = False
        requires_localization = True
    elif driver_class == "STRUCTURAL_OR_NONVOLATILE_SIGNAL_REMAINS_AFTER_SCRUB":
        classification = "R10000_LOCALIZATION_STRUCTURAL_SIGNAL_REMAINS"
        recommended = "LOCALIZE_R10000_STRUCTURAL_OBSERVATION_SHAPE_SIGNAL_V0"
        requires_repair = False
        requires_localization = True
    else:
        classification = "R10000_LOCALIZATION_INCONCLUSIVE_PROFILE_REVIEW_REQUIRED"
        recommended = "REVIEW_R10000_SIGNAL_LOCALIZATION_INCONCLUSIVE_PROFILE_V0"
        requires_repair = True
        requires_localization = False

    return {
        "schema_version": "r10000_distinguishable_signal_localization_packet_v0",
        "classification": classification,
        "source_r10000_signal_inspection_receipt_id": SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID,
        "run_id": RUN_ID,
        "driver_class": driver_class,
        "evidence": {
            "raw_shape_count": driver_profile["raw_shape_count"],
            "volatile_scrub_shape_count": driver_profile["volatile_scrub_shape_count"],
            "aggressive_scrub_shape_count": driver_profile["aggressive_scrub_shape_count"],
            "structure_only_shape_count": driver_profile["structure_only_shape_count"],
            "volatile_driver_count_top_50": driver_profile["volatile_driver_count_top_50"],
            "nonvolatile_driver_count_top_50": driver_profile["nonvolatile_driver_count_top_50"],
            "top_volatile_drivers": driver_profile["top_volatile_drivers"],
            "top_nonvolatile_drivers": driver_profile["top_nonvolatile_drivers"],
        },
        "requires_repair": requires_repair,
        "requires_further_localization": requires_localization,
        "requires_human_strategy_selection": True,
        "recommended_next_handling": recommended,
    }

def validate_outputs(cardinality: Dict[str, Any], shape_exp: Dict[str, Any], localization: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if cardinality.get("receipt_files_seen") != EXPECTED_RADIUS:
        failures.append(f"receipt_files_seen_not_10000:{cardinality.get('receipt_files_seen')}")
    if cardinality.get("protected_payload_key_hit_count") != 0:
        failures.append("protected_payload_key_hit_detected")
    if shape_exp.get("raw_shape_count") != EXPECTED_RADIUS:
        failures.append(f"raw_shape_count_not_10000:{shape_exp.get('raw_shape_count')}")
    if not localization.get("classification"):
        failures.append("localization_classification_missing")
    if localization.get("requires_human_strategy_selection") is not True:
        failures.append("requires_human_strategy_selection_not_true")

    for key in [
        "radius_10000_rerun_count",
        "new_small_probe_count",
        "unbounded_or_no_cap_run_count",
        "radius_above_10000_run_count",
        "queue_reopened_count",
        "closed_group_inspected_count",
        "row_payload_materialized_count",
        "row_payload_inspected_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "repair_executed_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "hidden_next_command_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")
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
    expected_one = [
        "r10000_signal_inspection_receipt_consumed_count",
        "source_surface_emitted_count",
        "field_cardinality_profile_emitted_count",
        "volatility_classification_emitted_count",
        "shape_reduction_experiment_emitted_count",
        "signal_driver_profile_emitted_count",
        "localization_packet_emitted_count",
        "next_decision_packet_emitted_count",
        "localization_decision_emitted_count",
        "localization_classification_emitted_count",
    ]
    for key in expected_one:
        if metrics.get(key) != 1:
            failures.append(f"metric_not_one:{key}:{metrics.get(key)}")

    if metrics.get("observation_receipt_files_analyzed_count") != EXPECTED_RADIUS:
        failures.append(f"metric_receipts_analyzed_not_10000:{metrics.get('observation_receipt_files_analyzed_count')}")
    if metrics.get("protected_payload_key_hit_count") != 0:
        failures.append(f"metric_protected_payload_key_hit_count_not_zero:{metrics.get('protected_payload_key_hit_count')}")

    for key in [
        "radius_10000_rerun_count",
        "new_small_probe_count",
        "unbounded_or_no_cap_run_count",
        "radius_above_10000_run_count",
        "queue_reopened_count",
        "closed_group_inspected_count",
        "row_payload_materialized_count",
        "row_payload_inspected_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "repair_executed_count",
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
    if terminal.get("stop_code") != "STOP_R10000_DISTINGUISHABLE_SIGNAL_LOCALIZATION_COMPLETE":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(SOURCE_FILES)
    failures = validate_sources()

    plan = {
        "schema_version": "r10000_distinguishable_signal_localization_plan_v0",
        "unit_id": UNIT_ID,
        "source_r10000_signal_inspection_receipt_id": SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID,
        "run_id": RUN_ID,
        "mode": "existing_artifacts_only_no_rerun_no_payload_materialization",
        "target_artifacts": {
            "observation_receipts_dir": rel(OBS_RECEIPT_DIR),
            "receipt_index": rel(RECEIPT_INDEX_PATH),
            "rollup": rel(ROLLUP_PATH),
            "run_receipt": rel(RUN_RECEIPT_PATH),
        },
        "localization_checks": [
            "field cardinality",
            "volatile metadata classification",
            "shape reduction under volatile scrub",
            "shape reduction under aggressive id/path/hash scrub",
            "structure-only shape collapse",
            "localization packet with next decision",
        ],
    }

    receipts = load_receipts()

    source_surface = build_source_surface()
    cardinality = build_field_cardinality_profile(receipts)
    volatility = build_volatility_classification(cardinality)
    shape_exp = build_shape_reduction_experiment(receipts)
    driver_profile = build_signal_driver_profile(cardinality, volatility, shape_exp)
    localization = build_localization_packet(driver_profile)

    next_decision = {
        "schema_version": "r10000_distinguishable_signal_localization_next_decision_packet_v0",
        "packet_status": "R10000_DISTINGUISHABLE_SIGNAL_LOCALIZATION_COMPLETE_READY_FOR_NEXT_DECISION",
        "source_r10000_signal_inspection_receipt_id": SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID,
        "run_id": RUN_ID,
        "localization_classification": localization["classification"],
        "driver_class": driver_profile["driver_class"],
        "safe_next_choices": [
            "close branch if distinguishability is volatility-only",
            "freeze bounded observability protocol if volatility-only and accepted",
            "localize nonvolatile field signal if present",
            "localize structural shape signal if it remains after scrubs",
            "repair observability profile only if localization is inconclusive",
            "run larger bounded radius only as a separate explicit objective after strategy selection",
        ],
        "recommended_next_handling": localization["recommended_next_handling"],
        "auto_next_command": None,
    }

    decision = {
        "schema_version": "r10000_distinguishable_signal_localization_decision_v0",
        "decision_id": sha8({
            "unit_id": UNIT_ID,
            "run_id": RUN_ID,
            "classification": localization["classification"],
            "driver_class": driver_profile["driver_class"],
        }),
        "decision_status": "R10000_DISTINGUISHABLE_SIGNAL_LOCALIZATION_COMPLETE",
        "localization_classification": localization["classification"],
        "driver_class": driver_profile["driver_class"],
        "raw_shape_count": shape_exp["raw_shape_count"],
        "volatile_scrub_shape_count": shape_exp["volatile_scrub_shape_count"],
        "aggressive_scrub_shape_count": shape_exp["aggressive_scrub_shape_count"],
        "structure_only_shape_count": shape_exp["structure_only_shape_count"],
        "observation_receipt_files_analyzed_count": len(receipts),
        "requires_repair": localization["requires_repair"],
        "requires_further_localization": localization["requires_further_localization"],
        "inspection_only_no_rerun": True,
        "recommended_next_handling": localization["recommended_next_handling"],
    }

    report = {
        "schema_version": "r10000_distinguishable_signal_localization_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_r10000_signal_inspection_receipt_id": SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID,
        "r10000_signal_inspection_receipt_consumed_count": 1,
        "source_surface_emitted_count": 1,
        "field_cardinality_profile_emitted_count": 1,
        "volatility_classification_emitted_count": 1,
        "shape_reduction_experiment_emitted_count": 1,
        "signal_driver_profile_emitted_count": 1,
        "localization_packet_emitted_count": 1,
        "next_decision_packet_emitted_count": 1,
        "localization_decision_emitted_count": 1,
        "localization_classification_emitted_count": 1,
        "observation_receipt_files_analyzed_count": len(receipts),
        "protected_payload_key_hit_count": cardinality["protected_payload_key_hit_count"],
        "flat_field_count": cardinality["flat_field_count"],
        "raw_shape_count": shape_exp["raw_shape_count"],
        "volatile_scrub_shape_count": shape_exp["volatile_scrub_shape_count"],
        "aggressive_scrub_shape_count": shape_exp["aggressive_scrub_shape_count"],
        "structure_only_shape_count": shape_exp["structure_only_shape_count"],
        "driver_class": driver_profile["driver_class"],
        "localization_classification": localization["classification"],
        "requires_repair": localization["requires_repair"],
        "requires_further_localization": localization["requires_further_localization"],
        "radius_10000_rerun_count": 0,
        "new_small_probe_count": 0,
        "unbounded_or_no_cap_run_count": 0,
        "radius_above_10000_run_count": 0,
        "queue_reopened_count": 0,
        "closed_group_inspected_count": 0,
        "row_payload_materialized_count": 0,
        "row_payload_inspected_count": 0,
        "identity_assignment_count": 0,
        "field_value_invention_count": 0,
        "repair_executed_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": localization["recommended_next_handling"],
    }

    trace = {
        "schema_version": "r10000_distinguishable_signal_localization_transition_trace_v0",
        "trace": [
            {
                "step": "consume_r10000_signal_inspection",
                "question": "clean distinguishable signal was detected",
                "answer": True,
                "taken": "load_existing_observation_receipts",
            },
            {
                "step": "load_existing_observation_receipts",
                "question": "analyze exactly 10000 existing receipts without rerun",
                "answer": len(receipts) == EXPECTED_RADIUS,
                "taken": "field_cardinality_and_shape_reduction",
            },
            {
                "step": "field_cardinality_and_shape_reduction",
                "question": "what driver class explains distinguishability",
                "answer": driver_profile["driver_class"],
                "taken": "emit_localization_packet",
            },
            {
                "step": "emit_localization_packet",
                "question": "run repair/localization/scale now",
                "answer": False,
                "taken": "STOP_R10000_DISTINGUISHABLE_SIGNAL_LOCALIZATION_COMPLETE",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_R10000_DISTINGUISHABLE_SIGNAL_LOCALIZATION_COMPLETE",
            "next_command_goal": None,
        },
    }

    write_json(LOCALIZATION_PLAN_PATH, plan)
    write_json(SOURCE_SURFACE_PATH, source_surface)
    write_json(FIELD_CARDINALITY_PROFILE_PATH, cardinality)
    write_json(VOLATILITY_CLASSIFICATION_PATH, volatility)
    write_json(SHAPE_REDUCTION_EXPERIMENT_PATH, shape_exp)
    write_json(SIGNAL_DRIVER_PROFILE_PATH, driver_profile)
    write_json(LOCALIZATION_PACKET_PATH, localization)
    write_json(NEXT_DECISION_PACKET_PATH, next_decision)
    write_json(LOCALIZATION_DECISION_PATH, decision)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(cardinality, shape_exp, localization, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "R10000_SIGNAL_LOCALIZATION_0_SIGNAL_INSPECTION_CONSUMED": True,
        "R10000_SIGNAL_LOCALIZATION_1_EXISTING_ARTIFACTS_ONLY": report["radius_10000_rerun_count"] == 0 and report["new_small_probe_count"] == 0,
        "R10000_SIGNAL_LOCALIZATION_2_10000_RECEIPTS_ANALYZED": report["observation_receipt_files_analyzed_count"] == EXPECTED_RADIUS,
        "R10000_SIGNAL_LOCALIZATION_3_FIELD_CARDINALITY_EMITTED": report["field_cardinality_profile_emitted_count"] == 1,
        "R10000_SIGNAL_LOCALIZATION_4_SHAPE_REDUCTION_EMITTED": report["shape_reduction_experiment_emitted_count"] == 1,
        "R10000_SIGNAL_LOCALIZATION_5_DRIVER_PROFILE_EMITTED": report["signal_driver_profile_emitted_count"] == 1,
        "R10000_SIGNAL_LOCALIZATION_6_LOCALIZATION_CLASSIFIED": report["localization_classification_emitted_count"] == 1 and bool(report["localization_classification"]),
        "R10000_SIGNAL_LOCALIZATION_7_NO_PROTECTED_PAYLOAD_KEYS": report["protected_payload_key_hit_count"] == 0,
        "R10000_SIGNAL_LOCALIZATION_8_NEXT_DECISION_PACKET_EMITTED": report["next_decision_packet_emitted_count"] == 1,
        "R10000_SIGNAL_LOCALIZATION_9_NO_UNBOUNDED_OR_RADIUS_ABOVE_10000": report["unbounded_or_no_cap_run_count"] == 0 and report["radius_above_10000_run_count"] == 0,
        "R10000_SIGNAL_LOCALIZATION_10_NO_QUEUE_OR_ROW_ACTION": report["queue_reopened_count"] == 0 and report["row_payload_materialized_count"] == 0,
        "R10000_SIGNAL_LOCALIZATION_11_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "R10000_SIGNAL_LOCALIZATION_12_NO_REPAIR_OR_TAXONOMY": report["repair_executed_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "R10000_SIGNAL_LOCALIZATION_13_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_r10000_signal_inspection_receipt_id": SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID,
        "source_radius_10000_result_review_receipt_id": SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID,
        "source_radius_10000_retry_receipt_id": SOURCE_RADIUS_10000_RETRY_RECEIPT_ID,
        "source_cli_wrapper_intercept_parse_fix_receipt_id": SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards_packet = {
        "localization_only_no_rerun": True,
        "existing_artifacts_only": True,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "radius_10000_rerun": False,
        "new_small_probe": False,
        "unbounded_or_no_cap_run": False,
        "radius_above_10000_run": False,
        "queue_reopened": False,
        "closed_group_inspected": False,
        "row_payload_materialized": False,
        "row_payload_inspected": False,
        "identity_assignment": False,
        "field_value_invention": False,
        "repair_executed": False,
        "taxonomy_delta_proposal_emitted": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_r10000_signal_inspection_receipt_id": SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID,
        "localization_classification": localization["classification"],
        "driver_class": driver_profile["driver_class"],
        "run_id": RUN_ID,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "localization_plan": rel(LOCALIZATION_PLAN_PATH),
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "field_cardinality_profile": rel(FIELD_CARDINALITY_PROFILE_PATH),
        "volatility_classification": rel(VOLATILITY_CLASSIFICATION_PATH),
        "shape_reduction_experiment": rel(SHAPE_REDUCTION_EXPERIMENT_PATH),
        "signal_driver_profile": rel(SIGNAL_DRIVER_PROFILE_PATH),
        "localization_packet": rel(LOCALIZATION_PACKET_PATH),
        "next_decision_packet": rel(NEXT_DECISION_PACKET_PATH),
        "localization_decision": rel(LOCALIZATION_DECISION_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "run_dir": rel(RUN_DIR),
        "run_receipt_path": rel(RUN_RECEIPT_PATH),
        "rollup_path": rel(ROLLUP_PATH),
        "receipt_index_path": rel(RECEIPT_INDEX_PATH),
    }

    receipt = {
        "schema_version": "r10000_distinguishable_signal_localization_receipt_v0",
        "receipt_type": "R10000_DISTINGUISHABLE_SIGNAL_LOCALIZATION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_r10000_signal_inspection_receipt_id": SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID,
        "source_radius_10000_result_review_receipt_id": SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID,
        "source_radius_10000_retry_receipt_id": SOURCE_RADIUS_10000_RETRY_RECEIPT_ID,
        "source_cli_wrapper_intercept_parse_fix_receipt_id": SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "r10000_distinguishable_signal_localization_summary": {
            "localization_result": decision["decision_status"],
            "localization_classification": localization["classification"],
            "driver_class": driver_profile["driver_class"],
            "run_id": RUN_ID,
            "observation_receipt_files_analyzed_count": len(receipts),
            "raw_shape_count": shape_exp["raw_shape_count"],
            "volatile_scrub_shape_count": shape_exp["volatile_scrub_shape_count"],
            "aggressive_scrub_shape_count": shape_exp["aggressive_scrub_shape_count"],
            "structure_only_shape_count": shape_exp["structure_only_shape_count"],
            "top_volatile_driver_count": driver_profile["volatile_driver_count_top_50"],
            "top_nonvolatile_driver_count": driver_profile["nonvolatile_driver_count_top_50"],
            "requires_repair": localization["requires_repair"],
            "requires_further_localization": localization["requires_further_localization"],
            "localization_only_no_rerun": True,
            "recommended_next_handling": localization["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "r10000_distinguishable_signal_localization_guards": guards_packet,
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
    print(f"r10000_signal_localization_receipt_id={receipt_id}")
    print(f"r10000_signal_localization_receipt_path=data/r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0_receipts/{receipt_id}.json")
    print(f"localization_packet_path=data/r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0/r10000_distinguishable_signal_localization_packet.json")
    print(f"next_decision_packet_path=data/r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0/r10000_distinguishable_signal_localization_next_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
