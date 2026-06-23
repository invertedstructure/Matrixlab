#!/usr/bin/env python3
from __future__ import annotations

import collections
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "INSPECT_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_ROLLUP_PROFILE_SIGNAL_V0"
TARGET_UNIT_ID = "r1000.post_closure_observability_harvest.radius_10000_rollup_profile_signal.inspection.v0"

SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID = "90042e28"
SOURCE_RADIUS_10000_RETRY_RECEIPT_ID = "bb2c8ce3"
SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID = "02711ff1"
SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID = "52d0ea8d"
SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID = "db7c0af2"
RUN_ID = "run_6b1b2494"
EXPECTED_RADIUS = 10000

OUT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_inspection_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_inspection_v0_receipts"

INSPECTION_PLAN_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_inspection_plan.json"
SOURCE_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_source_surface.json"
ROLLUP_PROFILE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_rollup_profile.json"
OBSERVATION_STREAM_PROFILE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_observation_stream_profile.json"
DISTINGUISHABILITY_PROFILE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_distinguishability_profile.json"
SIGNAL_CLASSIFICATION_PACKET_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_signal_classification_packet.json"
NEXT_DECISION_PACKET_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_signal_inspection_next_decision_packet.json"
INSPECTION_DECISION_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_signal_inspection_decision.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_signal_inspection_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_signal_inspection_report.json"

RESULT_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_result_review_v0_receipts" / f"{SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID}.json"
RESULT_REVIEW_SURFACE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_result_review_v0" / "r1000_post_closure_observability_harvest_radius_10000_result_review_surface.json"
RESULT_RUN_ARTIFACT_AUDIT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_result_review_v0" / "r1000_post_closure_observability_harvest_radius_10000_result_run_artifact_audit.json"
RESULT_OBSERVATION_PROFILE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_result_review_v0" / "r1000_post_closure_observability_harvest_radius_10000_observation_receipt_profile.json"
RESULT_BOUNDARY_GUARD_REVIEW_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_result_review_v0" / "r1000_post_closure_observability_harvest_radius_10000_boundary_guard_review.json"
RESULT_CLASSIFICATION_PACKET_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_result_review_v0" / "r1000_post_closure_observability_harvest_radius_10000_result_classification_packet.json"
RESULT_NEXT_STATUS_PACKET_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_result_review_v0" / "r1000_post_closure_observability_harvest_radius_10000_result_review_next_status_packet.json"

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
    RESULT_REVIEW_RECEIPT_PATH,
    RESULT_REVIEW_SURFACE_PATH,
    RESULT_RUN_ARTIFACT_AUDIT_PATH,
    RESULT_OBSERVATION_PROFILE_PATH,
    RESULT_BOUNDARY_GUARD_REVIEW_PATH,
    RESULT_CLASSIFICATION_PACKET_PATH,
    RESULT_NEXT_STATUS_PACKET_PATH,
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
    "decision": "INSPECT_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_ROLLUP_PROFILE_SIGNAL",
    "scope": "inspect existing radius-10000 rollup/profile/observation receipts for signal content without rerunning or repairing; classify whether the 10k harvest is purely stable/empty, exposes distinguishable signal, or exposes observability insufficiency; emit next decision packet",
    "source_radius_10000_result_review_receipt_id": SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID,
    "authorized": [
        "consume accepted radius-10000 result review",
        "read existing run receipt, rollup, receipt index, and observation receipt files",
        "aggregate observation receipt fields and low-cardinality values",
        "classify signal based only on existing receipts",
        "emit next decision packet",
        "stop before any next run or repair",
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

LOW_CARDINALITY_KEYS = [
    "gate",
    "status",
    "result_status",
    "observation_status",
    "observation_type",
    "classification",
    "result_classification",
    "signal_class",
    "signal_type",
    "halt_reason",
    "stop_code",
    "surface_type",
    "pressure_group",
    "pressure_group_id",
    "group_id",
    "reason",
    "kind",
    "type",
    "unit_id",
    "target_unit_id",
    "source_unit_id",
    "queue_state_status",
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

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def iter_flat(obj: Any, prefix: str = "") -> Iterable[Tuple[str, Any]]:
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            yield from iter_flat(v, key)
    elif isinstance(obj, list):
        yield prefix, f"__list_len__:{len(obj)}"
        for i, v in enumerate(obj[:5]):
            key = f"{prefix}[{i}]"
            yield from iter_flat(v, key)
    else:
        yield prefix, obj

def norm_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if len(text) > 160:
        return text[:157] + "..."
    return text

def scrub_for_shape(obj: Any) -> Any:
    volatile = {
        "created_at",
        "timestamp",
        "ts",
        "updated_at",
        "receipt_id",
        "observation_receipt_id",
        "receipt_path",
        "path",
        "sha256",
        "hash",
        "run_id",
        "observation_index",
        "index",
    }
    if isinstance(obj, dict):
        return {k: scrub_for_shape(v) for k, v in obj.items() if k not in volatile and not k.endswith("_id") and not k.endswith("_path")}
    if isinstance(obj, list):
        return [scrub_for_shape(v) for v in obj]
    return obj

def validate_sources() -> List[str]:
    failures: List[str] = []
    review = read_json(RESULT_REVIEW_RECEIPT_PATH)
    next_status = read_json(RESULT_NEXT_STATUS_PACKET_PATH)
    run_receipt = read_json(RUN_RECEIPT_PATH)
    rollup = read_json(ROLLUP_PATH)
    closure = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if review.get("receipt_id") != SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID:
        failures.append("radius_10000_result_review_receipt_id_wrong")
    if review.get("gate") != "PASS":
        failures.append("radius_10000_result_review_gate_not_pass")
    if review.get("radius_10000_result_review_summary", {}).get("recommended_next_handling") != "SELECT_NEXT_POST_CLOSURE_OBSERVABILITY_SCALE_OR_CLOSE_DECISION_AFTER_R10000_REVIEW_V0":
        failures.append("result_review_not_at_strategy_selection")
    if next_status.get("packet_status") != "RADIUS_10000_RESULT_REVIEW_ACCEPTED_READY_FOR_HUMAN_STRATEGY_SELECTION":
        failures.append("next_status_not_human_strategy_selection_ready")

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

    receipt_files = sorted(OBS_RECEIPT_DIR.glob("*.json"))
    if len(receipt_files) != EXPECTED_RADIUS:
        failures.append(f"observation_receipt_file_count_wrong:{len(receipt_files)}")
    return failures

def build_source_surface() -> Dict[str, Any]:
    review = read_json(RESULT_REVIEW_RECEIPT_PATH)
    rollup = read_json(ROLLUP_PATH)
    run_receipt = read_json(RUN_RECEIPT_PATH)
    next_status = read_json(RESULT_NEXT_STATUS_PACKET_PATH)
    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_source_surface_v0",
        "source_radius_10000_result_review_receipt_id": SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID,
        "run_id": RUN_ID,
        "run_dir": rel(RUN_DIR),
        "result_review_summary": review.get("radius_10000_result_review_summary"),
        "next_status_packet": next_status,
        "run_receipt_core": {
            "gate": run_receipt.get("gate"),
            "radius_requested": run_receipt.get("radius_requested"),
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

def build_rollup_profile() -> Dict[str, Any]:
    rollup = read_json(ROLLUP_PATH)
    run_receipt = read_json(RUN_RECEIPT_PATH)

    rollup_scalars = {}
    for k, v in rollup.items():
        if not isinstance(v, (dict, list)):
            rollup_scalars[k] = v

    run_scalars = {}
    for k, v in run_receipt.items():
        if not isinstance(v, (dict, list)):
            run_scalars[k] = v

    flat_rollup = list(iter_flat(rollup))
    key_presence = sorted({k for k, _ in flat_rollup})
    value_counts = {}
    for k, v in flat_rollup:
        if any(k.endswith(x) or k == x for x in LOW_CARDINALITY_KEYS):
            value_counts.setdefault(k, collections.Counter())[norm_scalar(v)] += 1

    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_rollup_profile_v0",
        "run_id": RUN_ID,
        "rollup_path": rel(ROLLUP_PATH),
        "run_receipt_path": rel(RUN_RECEIPT_PATH),
        "rollup_scalars": rollup_scalars,
        "run_receipt_scalars": run_scalars,
        "rollup_flat_key_count": len(key_presence),
        "rollup_flat_keys": key_presence,
        "rollup_low_cardinality_value_counts": {k: dict(v.most_common(25)) for k, v in value_counts.items()},
        "rollup_shape_hash": sha8(scrub_for_shape(rollup)),
        "run_receipt_shape_hash": sha8(scrub_for_shape(run_receipt)),
    }

def build_observation_stream_profile() -> Dict[str, Any]:
    receipt_files = sorted(OBS_RECEIPT_DIR.glob("*.json"))
    gate_counts = collections.Counter()
    terminal_type_counts = collections.Counter()
    terminal_stop_counts = collections.Counter()
    top_key_counts = collections.Counter()
    flat_key_counts = collections.Counter()
    low_cardinality_counts: Dict[str, collections.Counter] = {}
    shape_counts = collections.Counter()
    parse_failures = []
    index_values = []
    sample_records = []
    min_index = None
    max_index = None

    for n, path in enumerate(receipt_files):
        try:
            obj = read_json(path)
        except Exception as exc:
            parse_failures.append({"path": rel(path), "error": f"{type(exc).__name__}:{exc}"})
            continue

        if n < 5 or n in {len(receipt_files) // 2, len(receipt_files) - 1}:
            sample_records.append({
                "path": rel(path),
                "sha256": file_sha256(path),
                "top_level_keys": sorted(obj.keys()),
                "gate": obj.get("gate"),
                "observation_index": obj.get("observation_index"),
                "terminal": obj.get("terminal"),
                "shape_hash": sha8(scrub_for_shape(obj)),
            })

        gate_counts[norm_scalar(obj.get("gate"))] += 1
        terminal = obj.get("terminal") if isinstance(obj.get("terminal"), dict) else {}
        terminal_type_counts[norm_scalar(terminal.get("type"))] += 1
        terminal_stop_counts[norm_scalar(terminal.get("stop_code"))] += 1

        for k in obj.keys():
            top_key_counts[k] += 1

        idx = obj.get("observation_index")
        if isinstance(idx, int):
            index_values.append(idx)
            min_index = idx if min_index is None else min(min_index, idx)
            max_index = idx if max_index is None else max(max_index, idx)

        flat = list(iter_flat(obj))
        for k, v in flat:
            flat_key_counts[k] += 1
            leaf = k.split(".")[-1]
            if leaf in LOW_CARDINALITY_KEYS or k in LOW_CARDINALITY_KEYS:
                low_cardinality_counts.setdefault(k, collections.Counter())[norm_scalar(v)] += 1

        shape_counts[sha8(scrub_for_shape(obj))] += 1

    missing_indices = []
    duplicate_index_count = 0
    if index_values:
        counter = collections.Counter(index_values)
        duplicate_index_count = sum(c - 1 for c in counter.values() if c > 1)
        expected_indices = set(range(min_index, max_index + 1))
        missing_indices = sorted(expected_indices - set(index_values))
        if len(missing_indices) > 25:
            missing_indices = missing_indices[:25] + ["..."]

    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_observation_stream_profile_v0",
        "run_id": RUN_ID,
        "receipt_files_seen": len(receipt_files),
        "parse_failure_count": len(parse_failures),
        "parse_failure_samples": parse_failures[:10],
        "gate_counts": dict(gate_counts.most_common()),
        "terminal_type_counts": dict(terminal_type_counts.most_common()),
        "terminal_stop_code_counts": dict(terminal_stop_counts.most_common(50)),
        "top_level_key_counts": dict(top_key_counts.most_common(100)),
        "flat_key_count": len(flat_key_counts),
        "flat_key_counts_top_100": dict(flat_key_counts.most_common(100)),
        "low_cardinality_value_counts": {k: dict(v.most_common(50)) for k, v in sorted(low_cardinality_counts.items())},
        "shape_count": len(shape_counts),
        "shape_counts_top_25": dict(shape_counts.most_common(25)),
        "observation_index": {
            "count": len(index_values),
            "min": min_index,
            "max": max_index,
            "duplicate_index_count": duplicate_index_count,
            "missing_index_count_or_sample": len(missing_indices) if all(isinstance(x, int) for x in missing_indices) else missing_indices,
            "contiguous_if_zero_based_or_one_based_unknown": (
                len(index_values) == EXPECTED_RADIUS
                and duplicate_index_count == 0
                and len([x for x in missing_indices if isinstance(x, int)]) == 0
            ),
        },
        "sample_records": sample_records,
    }

def build_distinguishability_profile(stream: Dict[str, Any], rollup_profile: Dict[str, Any]) -> Dict[str, Any]:
    shape_count = stream["shape_count"]
    stop_code_counts = stream.get("terminal_stop_code_counts", {})
    gate_counts = stream.get("gate_counts", {})
    low_card = stream.get("low_cardinality_value_counts", {})

    non_pass_gates = {k: v for k, v in gate_counts.items() if k != "PASS"}
    distinct_stop_codes = [k for k in stop_code_counts if k != "null"]
    low_card_multi = {
        k: v for k, v in low_card.items()
        if len(v) > 1
        and not k.endswith("receipt_id")
        and not k.endswith("_id")
        and not k.endswith("_path")
    }

    distinguishability = {
        "shape_count": shape_count,
        "distinct_non_null_terminal_stop_codes": len(distinct_stop_codes),
        "non_pass_gate_classes": non_pass_gates,
        "low_cardinality_fields_with_multiple_values_count": len(low_card_multi),
        "low_cardinality_fields_with_multiple_values_top_25": {
            k: v for k, v in list(low_card_multi.items())[:25]
        },
    }

    if non_pass_gates:
        signal_class = "BOUNDARY_OR_FAILURE_SIGNAL_PRESENT"
    elif len(distinct_stop_codes) > 1 or len(low_card_multi) > 0 or shape_count > 1:
        signal_class = "DISTINGUISHABLE_OBSERVATION_SIGNAL_PRESENT"
    elif shape_count == 1:
        signal_class = "UNIFORM_STABLE_RECEIPT_SHAPE"
    else:
        signal_class = "OBSERVABILITY_PROFILE_INSUFFICIENT"

    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_distinguishability_profile_v0",
        "run_id": RUN_ID,
        "distinguishability": distinguishability,
        "signal_class": signal_class,
        "interpretation": {
            "BOUNDARY_OR_FAILURE_SIGNAL_PRESENT": "At least one non-PASS gate class appeared in observation receipts.",
            "DISTINGUISHABLE_OBSERVATION_SIGNAL_PRESENT": "Receipts are clean but contain more than one observable class/shape/value pattern.",
            "UNIFORM_STABLE_RECEIPT_SHAPE": "Receipts are clean and structurally uniform across the inspected stream.",
            "OBSERVABILITY_PROFILE_INSUFFICIENT": "The stream did not expose enough fields to classify a useful signal.",
        }[signal_class],
    }

def build_signal_classification(dist: Dict[str, Any], stream: Dict[str, Any], guards_clean: bool) -> Dict[str, Any]:
    base_class = dist["signal_class"]
    if not guards_clean:
        classification = "R10000_SIGNAL_INSPECTION_BLOCKED_BOUNDARY_GUARD_FAILURE"
        recommended = "REVIEW_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_SIGNAL_INSPECTION_BOUNDARY_FAILURE_V0"
    elif base_class == "BOUNDARY_OR_FAILURE_SIGNAL_PRESENT":
        classification = "R10000_SIGNAL_CLASS_BOUNDARY_OR_FAILURE_SIGNAL_REVIEW_REQUIRED"
        recommended = "LOCALIZE_R10000_POST_CLOSURE_OBSERVABILITY_FAILURE_SIGNAL_V0"
    elif base_class == "DISTINGUISHABLE_OBSERVATION_SIGNAL_PRESENT":
        classification = "R10000_SIGNAL_CLASS_DISTINGUISHABLE_CLEAN_SIGNAL_REVIEW_READY"
        recommended = "LOCALIZE_R10000_POST_CLOSURE_OBSERVABILITY_DISTINGUISHABLE_SIGNAL_V0"
    elif base_class == "UNIFORM_STABLE_RECEIPT_SHAPE":
        classification = "R10000_SIGNAL_CLASS_UNIFORM_STABLE_CLEAN_OBSERVABILITY"
        recommended = "DECIDE_CLOSE_OR_SCALE_AFTER_R10000_UNIFORM_STABLE_OBSERVABILITY_V0"
    else:
        classification = "R10000_SIGNAL_CLASS_OBSERVABILITY_PROFILE_INSUFFICIENT"
        recommended = "REPAIR_R10000_OBSERVABILITY_PROFILE_FIELDS_BEFORE_SCALE_V0"

    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_signal_classification_packet_v0",
        "classification": classification,
        "source_radius_10000_result_review_receipt_id": SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID,
        "run_id": RUN_ID,
        "evidence": {
            "receipt_files_seen": stream["receipt_files_seen"],
            "parse_failure_count": stream["parse_failure_count"],
            "gate_counts": stream["gate_counts"],
            "terminal_stop_code_counts": stream["terminal_stop_code_counts"],
            "shape_count": stream["shape_count"],
            "distinguishability": dist["distinguishability"],
            "boundary_guards_clean": guards_clean,
        },
        "requires_repair": classification in {
            "R10000_SIGNAL_INSPECTION_BLOCKED_BOUNDARY_GUARD_FAILURE",
            "R10000_SIGNAL_CLASS_OBSERVABILITY_PROFILE_INSUFFICIENT",
        },
        "requires_localization": classification in {
            "R10000_SIGNAL_CLASS_BOUNDARY_OR_FAILURE_SIGNAL_REVIEW_REQUIRED",
            "R10000_SIGNAL_CLASS_DISTINGUISHABLE_CLEAN_SIGNAL_REVIEW_READY",
        },
        "requires_human_strategy_selection": True,
        "recommended_next_handling": recommended,
    }

def validate_outputs(stream: Dict[str, Any], dist: Dict[str, Any], classification: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if stream.get("receipt_files_seen") != EXPECTED_RADIUS:
        failures.append(f"receipt_files_seen_not_10000:{stream.get('receipt_files_seen')}")
    if stream.get("parse_failure_count") != 0:
        failures.append("observation_receipt_parse_failures")
    if classification.get("requires_human_strategy_selection") is not True:
        failures.append("classification_missing_human_strategy_selection")
    if not classification.get("classification"):
        failures.append("classification_missing")
    if dist.get("signal_class") not in {
        "BOUNDARY_OR_FAILURE_SIGNAL_PRESENT",
        "DISTINGUISHABLE_OBSERVATION_SIGNAL_PRESENT",
        "UNIFORM_STABLE_RECEIPT_SHAPE",
        "OBSERVABILITY_PROFILE_INSUFFICIENT",
    }:
        failures.append("unknown_signal_class")

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
        "radius_10000_result_review_receipt_consumed_count",
        "run_receipt_consumed_count",
        "rollup_consumed_count",
        "receipt_index_consumed_count",
        "source_surface_emitted_count",
        "rollup_profile_emitted_count",
        "observation_stream_profile_emitted_count",
        "distinguishability_profile_emitted_count",
        "signal_classification_packet_emitted_count",
        "next_decision_packet_emitted_count",
        "inspection_decision_emitted_count",
        "classification_emitted_count",
    ]
    for key in expected_one:
        if metrics.get(key) != 1:
            failures.append(f"metric_not_one:{key}:{metrics.get(key)}")

    if metrics.get("observation_receipt_files_seen_count") != EXPECTED_RADIUS:
        failures.append(f"metric_receipts_seen_not_10000:{metrics.get('observation_receipt_files_seen_count')}")
    if metrics.get("observation_receipt_parse_failure_count") != 0:
        failures.append(f"metric_parse_failure_not_zero:{metrics.get('observation_receipt_parse_failure_count')}")

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
    if terminal.get("stop_code") != "STOP_R10000_ROLLUP_PROFILE_SIGNAL_INSPECTION_COMPLETE":
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
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_inspection_plan_v0",
        "unit_id": UNIT_ID,
        "source_radius_10000_result_review_receipt_id": SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID,
        "run_id": RUN_ID,
        "inspection_mode": "existing_artifacts_only_no_rerun",
        "target_artifacts": {
            "run_receipt": rel(RUN_RECEIPT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "receipt_index": rel(RECEIPT_INDEX_PATH),
            "observation_receipts_dir": rel(OBS_RECEIPT_DIR),
        },
        "authorized_receipt_count": EXPECTED_RADIUS,
        "not_authorized": HUMAN_DECISION["not_authorized"],
    }

    source_surface = build_source_surface()
    rollup_profile = build_rollup_profile()
    stream = build_observation_stream_profile()
    dist = build_distinguishability_profile(stream, rollup_profile)

    boundary = read_json(RESULT_BOUNDARY_GUARD_REVIEW_PATH)
    guards_clean = bool(boundary.get("boundary_guard_review_passed"))
    classification = build_signal_classification(dist, stream, guards_clean)

    next_decision = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_signal_inspection_next_decision_packet_v0",
        "packet_status": "R10000_SIGNAL_INSPECTION_COMPLETE_READY_FOR_NEXT_DECISION",
        "source_radius_10000_result_review_receipt_id": SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID,
        "run_id": RUN_ID,
        "signal_classification": classification["classification"],
        "signal_class": dist["signal_class"],
        "safe_next_choices": [
            "close this observability branch as accepted",
            "localize the distinguishable signal if present",
            "repair observability profile fields if insufficient",
            "run a larger bounded radius only as a separate explicit objective",
            "freeze the bounded observability protocol as reusable infrastructure",
        ],
        "recommended_next_handling": classification["recommended_next_handling"],
        "auto_next_command": None,
    }

    decision = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_signal_inspection_decision_v0",
        "decision_id": sha8({
            "unit_id": UNIT_ID,
            "run_id": RUN_ID,
            "classification": classification["classification"],
            "signal_class": dist["signal_class"],
        }),
        "decision_status": "R10000_ROLLUP_PROFILE_SIGNAL_INSPECTION_COMPLETE",
        "signal_classification": classification["classification"],
        "signal_class": dist["signal_class"],
        "receipt_files_seen": stream["receipt_files_seen"],
        "parse_failure_count": stream["parse_failure_count"],
        "shape_count": stream["shape_count"],
        "gate_counts": stream["gate_counts"],
        "terminal_stop_code_counts": stream["terminal_stop_code_counts"],
        "inspection_only_no_rerun": True,
        "recommended_next_handling": classification["recommended_next_handling"],
    }

    report = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_signal_inspection_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_radius_10000_result_review_receipt_id": SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID,
        "radius_10000_result_review_receipt_consumed_count": 1,
        "run_receipt_consumed_count": 1,
        "rollup_consumed_count": 1,
        "receipt_index_consumed_count": 1,
        "source_surface_emitted_count": 1,
        "rollup_profile_emitted_count": 1,
        "observation_stream_profile_emitted_count": 1,
        "distinguishability_profile_emitted_count": 1,
        "signal_classification_packet_emitted_count": 1,
        "next_decision_packet_emitted_count": 1,
        "inspection_decision_emitted_count": 1,
        "classification_emitted_count": 1,
        "observation_receipt_files_seen_count": stream["receipt_files_seen"],
        "observation_receipt_parse_failure_count": stream["parse_failure_count"],
        "shape_count": stream["shape_count"],
        "signal_class": dist["signal_class"],
        "signal_classification": classification["classification"],
        "requires_repair": classification["requires_repair"],
        "requires_localization": classification["requires_localization"],
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
        "recommended_next_handling": classification["recommended_next_handling"],
    }

    trace = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_signal_inspection_transition_trace_v0",
        "trace": [
            {
                "step": "consume_accepted_radius_10000_result_review",
                "question": "accepted 10k review exists and requests strategy selection",
                "answer": True,
                "taken": "inspect_existing_rollup_and_receipts",
            },
            {
                "step": "inspect_existing_rollup_and_receipts",
                "question": "exactly 10000 existing receipts can be profiled without rerun",
                "answer": stream["receipt_files_seen"] == EXPECTED_RADIUS and stream["parse_failure_count"] == 0,
                "taken": "classify_signal",
            },
            {
                "step": "classify_signal",
                "question": "what signal class is visible from receipts",
                "answer": dist["signal_class"],
                "taken": "emit_next_decision_packet",
            },
            {
                "step": "emit_next_decision_packet",
                "question": "run or repair now",
                "answer": False,
                "taken": "STOP_R10000_ROLLUP_PROFILE_SIGNAL_INSPECTION_COMPLETE",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_R10000_ROLLUP_PROFILE_SIGNAL_INSPECTION_COMPLETE",
            "next_command_goal": None,
        },
    }

    write_json(INSPECTION_PLAN_PATH, plan)
    write_json(SOURCE_SURFACE_PATH, source_surface)
    write_json(ROLLUP_PROFILE_PATH, rollup_profile)
    write_json(OBSERVATION_STREAM_PROFILE_PATH, stream)
    write_json(DISTINGUISHABILITY_PROFILE_PATH, dist)
    write_json(SIGNAL_CLASSIFICATION_PACKET_PATH, classification)
    write_json(NEXT_DECISION_PACKET_PATH, next_decision)
    write_json(INSPECTION_DECISION_PATH, decision)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(stream, dist, classification, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "R10000_SIGNAL_INSPECTION_0_RESULT_REVIEW_CONSUMED": True,
        "R10000_SIGNAL_INSPECTION_1_EXISTING_ARTIFACTS_ONLY": report["radius_10000_rerun_count"] == 0 and report["new_small_probe_count"] == 0,
        "R10000_SIGNAL_INSPECTION_2_10000_RECEIPTS_PROFILED": report["observation_receipt_files_seen_count"] == EXPECTED_RADIUS,
        "R10000_SIGNAL_INSPECTION_3_NO_PARSE_FAILURES": report["observation_receipt_parse_failure_count"] == 0,
        "R10000_SIGNAL_INSPECTION_4_ROLLUP_PROFILE_EMITTED": report["rollup_profile_emitted_count"] == 1,
        "R10000_SIGNAL_INSPECTION_5_DISTINGUISHABILITY_PROFILE_EMITTED": report["distinguishability_profile_emitted_count"] == 1,
        "R10000_SIGNAL_INSPECTION_6_SIGNAL_CLASSIFIED": report["classification_emitted_count"] == 1 and bool(report["signal_classification"]),
        "R10000_SIGNAL_INSPECTION_7_NEXT_DECISION_PACKET_EMITTED": report["next_decision_packet_emitted_count"] == 1,
        "R10000_SIGNAL_INSPECTION_8_NO_UNBOUNDED_OR_RADIUS_ABOVE_10000": report["unbounded_or_no_cap_run_count"] == 0 and report["radius_above_10000_run_count"] == 0,
        "R10000_SIGNAL_INSPECTION_9_NO_QUEUE_OR_ROW_ACTION": report["queue_reopened_count"] == 0 and report["row_payload_materialized_count"] == 0,
        "R10000_SIGNAL_INSPECTION_10_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "R10000_SIGNAL_INSPECTION_11_NO_REPAIR_OR_TAXONOMY": report["repair_executed_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "R10000_SIGNAL_INSPECTION_12_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_radius_10000_result_review_receipt_id": SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID,
        "source_radius_10000_retry_receipt_id": SOURCE_RADIUS_10000_RETRY_RECEIPT_ID,
        "source_cli_wrapper_intercept_parse_fix_receipt_id": SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards_packet = {
        "inspection_only_no_rerun": True,
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
        "source_radius_10000_result_review_receipt_id": SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID,
        "signal_classification": classification["classification"],
        "run_id": RUN_ID,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "inspection_plan": rel(INSPECTION_PLAN_PATH),
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "rollup_profile": rel(ROLLUP_PROFILE_PATH),
        "observation_stream_profile": rel(OBSERVATION_STREAM_PROFILE_PATH),
        "distinguishability_profile": rel(DISTINGUISHABILITY_PROFILE_PATH),
        "signal_classification_packet": rel(SIGNAL_CLASSIFICATION_PACKET_PATH),
        "next_decision_packet": rel(NEXT_DECISION_PACKET_PATH),
        "inspection_decision": rel(INSPECTION_DECISION_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "run_dir": rel(RUN_DIR),
        "run_receipt_path": rel(RUN_RECEIPT_PATH),
        "rollup_path": rel(ROLLUP_PATH),
        "receipt_index_path": rel(RECEIPT_INDEX_PATH),
    }

    receipt = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_inspection_receipt_v0",
        "receipt_type": "R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_ROLLUP_PROFILE_SIGNAL_INSPECTION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_radius_10000_result_review_receipt_id": SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID,
        "source_radius_10000_retry_receipt_id": SOURCE_RADIUS_10000_RETRY_RECEIPT_ID,
        "source_cli_wrapper_intercept_parse_fix_receipt_id": SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "radius_10000_signal_inspection_summary": {
            "inspection_result": decision["decision_status"],
            "signal_classification": classification["classification"],
            "signal_class": dist["signal_class"],
            "run_id": RUN_ID,
            "receipt_files_seen": stream["receipt_files_seen"],
            "parse_failure_count": stream["parse_failure_count"],
            "shape_count": stream["shape_count"],
            "gate_counts": stream["gate_counts"],
            "terminal_stop_code_counts": stream["terminal_stop_code_counts"],
            "requires_repair": classification["requires_repair"],
            "requires_localization": classification["requires_localization"],
            "inspection_only_no_rerun": True,
            "recommended_next_handling": classification["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "radius_10000_signal_inspection_guards": guards_packet,
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
    print(f"r10000_signal_inspection_receipt_id={receipt_id}")
    print(f"r10000_signal_inspection_receipt_path=data/r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_inspection_v0_receipts/{receipt_id}.json")
    print(f"next_decision_packet_path=data/r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_inspection_v0/r1000_post_closure_observability_harvest_radius_10000_signal_inspection_next_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
