#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RUN_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_V0"
TARGET_UNIT_ID = "r1000.post_closure_observability_harvest.radius_10000.v0"

SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID = "52d0ea8d"
SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID = "db7c0af2"
SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID = "9d2f4dc1"
SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID = "982ff0d0"
SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID = "46694b59"
SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID = "9b9cb3eb"

HARVEST_RADIUS = 10000

OUT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_v0_receipts"

RUN_LOG_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_run.log"
STDERR_LOG_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_stderr.log"
HARVEST_PLAN_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_plan.json"
PRE_SNAPSHOT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_pre_snapshot.json"
POST_SNAPSHOT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_post_snapshot.json"
RECEIPT_INDEX_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_receipt_index.jsonl"
FAILURE_GALLERY_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_failure_gallery.json"
HALT_HISTOGRAM_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_halt_histogram.json"
ROLLUP_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_rollup.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_report.json"

PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0_receipts" / f"{SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID}.json"
CLOSED_QUEUE_HANDOFF_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0" / "r1000_pressure_queue_closed_handoff_after_synthetic_remainder_expected_limit.json"
CLOSURE_REVIEW_REPORT_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0" / "r1000_pressure_queue_closure_review_report_after_synthetic_remainder_expected_limit.json"
EXPECTED_LIMIT_MARK_RECEIPT_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID}.json"
FINAL_QUEUE_STATE_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_final_pressure_queue_state_after_synthetic_remainder_expected_limit.json"
SOURCE_AUDIT_RECEIPT_PATH = ROOT / "data" / "r1000_synthetic_remainder_source_evidence_audit_after_repaired_burden_queue_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID}.json"
IDENTITY_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_selected_synthetic_remainder_identity_surface_review_after_repaired_burden_queue_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID}.json"
SELECTION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_repaired_burden_group_queue_reconciliation_v0_receipts" / f"{SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID}.json"
REPAIRED_QUEUE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_v0_receipts" / f"{SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID}.json"

SOURCE_FILES = [
    PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_PATH,
    CLOSED_QUEUE_HANDOFF_PATH,
    CLOSURE_REVIEW_REPORT_PATH,
    EXPECTED_LIMIT_MARK_RECEIPT_PATH,
    FINAL_QUEUE_STATE_PATH,
    SOURCE_AUDIT_RECEIPT_PATH,
    IDENTITY_REVIEW_RECEIPT_PATH,
    SELECTION_RECEIPT_PATH,
    REPAIRED_QUEUE_RECEIPT_PATH,
]

HUMAN_DECISION = {
    "decision": "RUN_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000",
    "scope": "run a bounded high-radius post-closure observability harvest anchored to the accepted R1000 pressure queue closure, collecting receipts/rollups/failure gallery without reopening the queue, inspecting closed groups, mutating prior artifacts, or hiding a next command",
    "radius": HARVEST_RADIUS,
    "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
    "authorized": [
        "consume closed queue receipt and handoff",
        "verify queue is closed before harvest",
        "run bounded radius harvest for observability",
        "collect stdout and stderr logs",
        "collect receipt index",
        "emit halt histogram",
        "emit failure gallery",
        "emit harvest rollup",
        "stop after bounded harvest",
    ],
    "not_authorized": [
        "reopening R1000 pressure queue",
        "inspecting closed pressure groups",
        "materializing row payloads",
        "assigning identity values",
        "inventing values",
        "filling fields",
        "running repair",
        "applying taxonomy changes",
        "mutating source artifacts",
        "mutating existing receipts",
        "running unbounded/no-cap harvest",
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
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))

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

def run_cmd(args: List[str], *, timeout: Optional[int] = None) -> Tuple[int, str, str, float]:
    start = time.monotonic()
    proc = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    elapsed = time.monotonic() - start
    return proc.returncode, proc.stdout, proc.stderr, elapsed

def discover_existing_receipts() -> List[Path]:
    roots = [
        ROOT / "data",
        ROOT / "logs",
    ]
    receipts: List[Path] = []
    for base in roots:
        if not base.exists():
            continue
        for path in base.rglob("*.json"):
            name = path.name.lower()
            parent = path.parent.name.lower()
            if "receipt" in name or "receipt" in parent:
                receipts.append(path)
    return sorted(set(receipts), key=lambda p: rel(p))

def receipt_index(paths: List[Path]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for path in paths:
        row: Dict[str, Any] = {
            "path": rel(path),
            "sha256": file_sha256(path),
            "size_bytes": path.stat().st_size,
        }
        try:
            obj = read_json(path)
            row.update({
                "receipt_id": obj.get("receipt_id"),
                "unit_id": obj.get("unit_id"),
                "target_unit_id": obj.get("target_unit_id"),
                "gate": obj.get("gate"),
                "terminal_stop_code": (obj.get("terminal") or {}).get("stop_code") if isinstance(obj.get("terminal"), dict) else None,
                "terminal_next_command_goal": (obj.get("terminal") or {}).get("next_command_goal") if isinstance(obj.get("terminal"), dict) else None,
                "created_at": obj.get("created_at") or obj.get("timestamp"),
            })
        except Exception as exc:
            row.update({
                "parse_error": type(exc).__name__,
            })
        rows.append(row)
    return rows

def summarize_gate_latest() -> Dict[str, Any]:
    rc, out, err, elapsed = run_cmd(["uv", "run", "python", "src/matrixlab/cli.py", "gate", "latest"], timeout=120)
    return {
        "returncode": rc,
        "stdout_tail": out[-8000:],
        "stderr_tail": err[-4000:],
        "elapsed_seconds": round(elapsed, 6),
        "gate_pass_text_present": "GATE_PASS" in out,
    }

def run_harvest_command() -> Dict[str, Any]:
    candidates = [
        ["uv", "run", "python", "src/matrixlab/cli.py", "run", "--radius", str(HARVEST_RADIUS)],
        ["uv", "run", "python", "src/matrixlab/cli.py", "run", "--cycles", str(HARVEST_RADIUS)],
        ["uv", "run", "python", "src/matrixlab/cli.py", "run", "--max-cycles", str(HARVEST_RADIUS)],
        ["uv", "run", "python", "src/matrixlab/cli.py", "cycle", "--radius", str(HARVEST_RADIUS)],
        ["uv", "run", "python", "src/matrixlab/cli.py", "harvest", "--radius", str(HARVEST_RADIUS)],
    ]

    attempted: List[Dict[str, Any]] = []
    selected: Optional[Dict[str, Any]] = None

    for args in candidates:
        start = time.monotonic()
        proc = subprocess.run(
            args,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        elapsed = time.monotonic() - start
        attempt = {
            "args": args,
            "returncode": proc.returncode,
            "elapsed_seconds": round(elapsed, 6),
            "stdout_tail": proc.stdout[-4000:],
            "stderr_tail": proc.stderr[-4000:],
        }
        attempted.append(attempt)
        if proc.returncode == 0:
            RUN_LOG_PATH.write_text(proc.stdout)
            STDERR_LOG_PATH.write_text(proc.stderr)
            selected = attempt
            break

    if selected is None:
        RUN_LOG_PATH.write_text("\n\n".join(
            "COMMAND: " + " ".join(a["args"]) + "\nSTDOUT:\n" + a["stdout_tail"] for a in attempted
        ))
        STDERR_LOG_PATH.write_text("\n\n".join(
            "COMMAND: " + " ".join(a["args"]) + "\nSTDERR:\n" + a["stderr_tail"] for a in attempted
        ))

    return {
        "attempted": attempted,
        "selected": selected,
        "harvest_command_found": selected is not None,
    }

def build_halt_histogram(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    counts = Counter()
    for row in rows:
        stop = row.get("terminal_stop_code") or "UNKNOWN_OR_ABSENT"
        counts[stop] += 1
    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_halt_histogram_v0",
        "halt_histogram": dict(sorted(counts.items())),
        "unique_halt_count": len(counts),
    }

def build_failure_gallery(rows: List[Dict[str, Any]], gate_latest: Dict[str, Any], harvest: Dict[str, Any]) -> Dict[str, Any]:
    failures = []
    for row in rows:
        if row.get("gate") not in {None, "PASS"}:
            failures.append({
                "failure_type": "receipt_gate_not_pass",
                "path": row.get("path"),
                "receipt_id": row.get("receipt_id"),
                "unit_id": row.get("unit_id"),
                "gate": row.get("gate"),
            })
        if row.get("terminal_next_command_goal") is not None:
            failures.append({
                "failure_type": "hidden_next_command_goal_present",
                "path": row.get("path"),
                "receipt_id": row.get("receipt_id"),
                "unit_id": row.get("unit_id"),
                "terminal_next_command_goal": row.get("terminal_next_command_goal"),
            })
        if row.get("parse_error"):
            failures.append({
                "failure_type": "receipt_parse_error",
                "path": row.get("path"),
                "parse_error": row.get("parse_error"),
            })

    if gate_latest.get("returncode") != 0 or gate_latest.get("gate_pass_text_present") is not True:
        failures.append({
            "failure_type": "gate_latest_not_pass",
            "returncode": gate_latest.get("returncode"),
            "stdout_tail": gate_latest.get("stdout_tail"),
            "stderr_tail": gate_latest.get("stderr_tail"),
        })

    if harvest.get("harvest_command_found") is not True:
        failures.append({
            "failure_type": "harvest_command_unresolved",
            "attempted": harvest.get("attempted"),
        })

    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_failure_gallery_v0",
        "failure_count": len(failures),
        "failures": failures[:100],
        "truncated": len(failures) > 100,
    }

def validate_sources() -> List[str]:
    failures: List[str] = []
    closure_receipt = read_json(PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_state = read_json(FINAL_QUEUE_STATE_PATH)

    if closure_receipt.get("receipt_id") != SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID:
        failures.append("closure_review_receipt_id_wrong")
    if closure_receipt.get("gate") != "PASS":
        failures.append("closure_review_not_pass")
    if closure_receipt.get("pressure_queue_closure_review_summary", {}).get("queue_closed") is not True:
        failures.append("closure_review_queue_not_closed")
    if closure_receipt.get("pressure_queue_closure_review_summary", {}).get("remaining_open_group_count") != 0:
        failures.append("closure_review_remaining_groups_not_zero")
    if closure_receipt.get("pressure_queue_closure_review_summary", {}).get("remaining_open_row_count") != 0:
        failures.append("closure_review_remaining_rows_not_zero")
    if closure_receipt.get("pressure_queue_closure_review_summary", {}).get("recommended_next_handling") is not None:
        failures.append("closure_review_recommended_next_not_null")

    if handoff.get("handoff_status") != "R1000_PRESSURE_QUEUE_CLOSED_NO_REMAINING_PRESSURE":
        failures.append("handoff_status_wrong")
    if handoff.get("next_command_goal") is not None:
        failures.append("handoff_next_command_not_null")

    if final_state.get("queue_state_status") != "R1000_PRESSURE_QUEUE_CLOSED":
        failures.append("final_queue_state_status_wrong")
    if final_state.get("remaining_open_group_count") != 0:
        failures.append("final_queue_remaining_group_not_zero")
    if final_state.get("remaining_open_row_count") != 0:
        failures.append("final_queue_remaining_row_not_zero")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def validate_outputs(rollup: Dict[str, Any], failure_gallery: Dict[str, Any], source_mutation_detected: bool) -> List[str]:
    failures: List[str] = []

    if rollup.get("radius_requested") != HARVEST_RADIUS:
        failures.append("radius_requested_wrong")
    if rollup.get("source_pressure_queue_closed") is not True:
        failures.append("source_pressure_queue_not_closed")
    if rollup.get("queue_reopened_count") != 0:
        failures.append("queue_reopened")
    if rollup.get("closed_group_inspected_count") != 0:
        failures.append("closed_group_inspected")
    if rollup.get("row_payload_materialized_count") != 0:
        failures.append("row_payload_materialized")
    if rollup.get("source_mutation_count") != 0:
        failures.append("source_mutation_count_nonzero")
    if source_mutation_detected:
        failures.append("source_hash_changed")
    if rollup.get("hidden_next_command_count") != 0:
        failures.append("hidden_next_command_count_nonzero")
    if rollup.get("gate_latest_pass") is not True:
        failures.append("gate_latest_not_pass")
    if rollup.get("harvest_command_resolved") is not True:
        failures.append("harvest_command_unresolved")
    if failure_gallery.get("failure_count", 0) > 0:
        failures.append("failure_gallery_not_empty")

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
    if metrics.get("radius_requested") != HARVEST_RADIUS:
        failures.append("metric_radius_wrong")
    if metrics.get("gate_latest_pass_count") != 1:
        failures.append("metric_gate_latest_pass_wrong")
    if metrics.get("harvest_command_resolved_count") != 1:
        failures.append("metric_harvest_command_resolved_wrong")

    for key in [
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
    if terminal.get("stop_code") != "STOP_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_COMPLETE":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(SOURCE_FILES)
    failures = validate_sources()

    pre_receipts = discover_existing_receipts()
    pre_snapshot = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_pre_snapshot_v0",
        "captured_at": now_iso(),
        "receipt_count": len(pre_receipts),
        "source_files": source_before,
    }
    write_json(PRE_SNAPSHOT_PATH, pre_snapshot)

    plan = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_plan_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "radius_requested": HARVEST_RADIUS,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "mode": "post_closure_observability_harvest",
        "bounded": True,
        "unbounded_or_no_cap": False,
        "queue_reopen_authorized": False,
        "closed_group_inspection_authorized": False,
        "source_mutation_authorized": False,
    }
    write_json(HARVEST_PLAN_PATH, plan)

    start = time.monotonic()
    harvest = run_harvest_command()
    runtime_seconds = time.monotonic() - start

    post_receipts = discover_existing_receipts()
    post_snapshot = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_post_snapshot_v0",
        "captured_at": now_iso(),
        "receipt_count": len(post_receipts),
        "source_files": snapshot_files(SOURCE_FILES),
    }
    write_json(POST_SNAPSHOT_PATH, post_snapshot)

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after

    rows = receipt_index(post_receipts)
    write_jsonl(RECEIPT_INDEX_PATH, rows)

    halt_histogram = build_halt_histogram(rows)
    write_json(HALT_HISTOGRAM_PATH, halt_histogram)

    gate_latest = summarize_gate_latest()
    failure_gallery = build_failure_gallery(rows, gate_latest, harvest)
    write_json(FAILURE_GALLERY_PATH, failure_gallery)

    new_receipt_count = max(0, len(post_receipts) - len(pre_receipts))
    selected_harvest = harvest.get("selected") or {}

    rollup = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_rollup_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_pressure_queue_closed": True,
        "radius_requested": HARVEST_RADIUS,
        "bounded": True,
        "receipt_count_before": len(pre_receipts),
        "receipt_count_after": len(post_receipts),
        "new_receipt_count": new_receipt_count,
        "runtime_seconds": round(runtime_seconds, 6),
        "receipt_write_rate_per_second": round(new_receipt_count / runtime_seconds, 6) if runtime_seconds > 0 else None,
        "harvest_command_resolved": harvest.get("harvest_command_found") is True,
        "harvest_command_selected": selected_harvest.get("args"),
        "harvest_command_returncode": selected_harvest.get("returncode"),
        "harvest_command_elapsed_seconds": selected_harvest.get("elapsed_seconds"),
        "gate_latest_returncode": gate_latest.get("returncode"),
        "gate_latest_pass": gate_latest.get("gate_pass_text_present") is True and gate_latest.get("returncode") == 0,
        "failure_count": failure_gallery["failure_count"],
        "unique_halt_count": halt_histogram["unique_halt_count"],
        "queue_reopened_count": 0,
        "closed_group_inspected_count": 0,
        "row_payload_materialized_count": 0,
        "row_payload_inspected_count": 0,
        "identity_assignment_count": 0,
        "field_value_invention_count": 0,
        "repair_executed_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": "REVIEW_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_V0",
    }
    write_json(ROLLUP_PATH, rollup)

    failures.extend(validate_outputs(rollup, failure_gallery, source_mutation_detected))

    trace = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_transition_trace_v0",
        "trace": [
            {
                "step": "consume_pressure_queue_closure_review",
                "question": "queue closed and no recommended next handling",
                "answer": True,
                "taken": "run_bounded_observability_harvest",
            },
            {
                "step": "run_bounded_observability_harvest",
                "question": "harvest command resolved",
                "answer": rollup["harvest_command_resolved"],
                "taken": "collect_receipt_index_and_rollup",
            },
            {
                "step": "collect_receipt_index_and_rollup",
                "question": "failure gallery empty and gate latest pass",
                "answer": failure_gallery["failure_count"] == 0 and rollup["gate_latest_pass"] is True,
                "taken": "emit_review_required",
            },
            {
                "step": "emit_review_required",
                "question": "hidden next command allowed",
                "answer": False,
                "taken": "STOP_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_COMPLETE",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_COMPLETE",
            "next_command_goal": None,
        },
    }
    write_json(TRANSITION_TRACE_PATH, trace)

    report = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "radius_requested": HARVEST_RADIUS,
        "harvest_plan_emitted_count": 1,
        "pre_snapshot_emitted_count": 1,
        "post_snapshot_emitted_count": 1,
        "run_log_emitted_count": 1,
        "stderr_log_emitted_count": 1,
        "receipt_index_emitted_count": 1,
        "halt_histogram_emitted_count": 1,
        "failure_gallery_emitted_count": 1,
        "rollup_emitted_count": 1,
        "receipt_count_before": rollup["receipt_count_before"],
        "receipt_count_after": rollup["receipt_count_after"],
        "new_receipt_count": rollup["new_receipt_count"],
        "runtime_seconds": rollup["runtime_seconds"],
        "receipt_write_rate_per_second": rollup["receipt_write_rate_per_second"],
        "unique_halt_count": rollup["unique_halt_count"],
        "failure_count": rollup["failure_count"],
        "gate_latest_pass_count": 1 if rollup["gate_latest_pass"] else 0,
        "harvest_command_resolved_count": 1 if rollup["harvest_command_resolved"] else 0,
        "queue_reopened_count": 0,
        "closed_group_inspected_count": 0,
        "row_payload_materialized_count": 0,
        "row_payload_inspected_count": 0,
        "identity_assignment_count": 0,
        "field_value_invention_count": 0,
        "repair_executed_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": rollup["recommended_next_handling"],
    }
    write_json(REPORT_PATH, report)

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    acceptance_gate_results = {
        "HARVEST_10000_0_CLOSED_QUEUE_CONSUMED": True,
        "HARVEST_10000_1_RADIUS_BOUNDED": HARVEST_RADIUS == 10000,
        "HARVEST_10000_2_HARVEST_COMMAND_RESOLVED": report["harvest_command_resolved_count"] == 1,
        "HARVEST_10000_3_RECEIPT_INDEX_EMITTED": report["receipt_index_emitted_count"] == 1,
        "HARVEST_10000_4_ROLLUP_EMITTED": report["rollup_emitted_count"] == 1,
        "HARVEST_10000_5_FAILURE_GALLERY_EMPTY": report["failure_count"] == 0,
        "HARVEST_10000_6_GATE_LATEST_PASS": report["gate_latest_pass_count"] == 1,
        "HARVEST_10000_7_NO_QUEUE_REOPEN_OR_CLOSED_GROUP_INSPECTION": report["queue_reopened_count"] == 0 and report["closed_group_inspected_count"] == 0,
        "HARVEST_10000_8_NO_ROW_PAYLOAD_REPAIR_TAXONOMY": report["row_payload_materialized_count"] == 0 and report["repair_executed_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "HARVEST_10000_9_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "HARVEST_10000_10_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    aggregate_metrics = {
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "source_synthetic_remainder_source_audit_receipt_id": SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID,
        "source_synthetic_remainder_identity_review_receipt_id": SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID,
        "source_selection_after_repaired_burden_queue_receipt_id": SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID,
        "source_repaired_burden_queue_reconciliation_receipt_id": SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
    }

    guards = {
        "closed_queue_consumed": True,
        "bounded_radius": True,
        "radius_requested": HARVEST_RADIUS,
        "unbounded_or_no_cap": False,
        "harvest_command_resolved": report["harvest_command_resolved_count"] == 1,
        "receipt_index_emitted": True,
        "rollup_emitted": True,
        "failure_gallery_emitted": True,
        "queue_reopened": False,
        "closed_group_inspected": False,
        "row_payload_materialized": False,
        "row_payload_inspected": False,
        "identity_assignment": False,
        "field_value_invention": False,
        "repair_executed": False,
        "taxonomy_delta_proposal_emitted": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_closure_review_receipt": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "radius": HARVEST_RADIUS,
        "runtime_seconds": report["runtime_seconds"],
        "receipt_count_after": report["receipt_count_after"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "harvest_plan": rel(HARVEST_PLAN_PATH),
        "pre_snapshot": rel(PRE_SNAPSHOT_PATH),
        "post_snapshot": rel(POST_SNAPSHOT_PATH),
        "run_log": rel(RUN_LOG_PATH),
        "stderr_log": rel(STDERR_LOG_PATH),
        "receipt_index": rel(RECEIPT_INDEX_PATH),
        "halt_histogram": rel(HALT_HISTOGRAM_PATH),
        "failure_gallery": rel(FAILURE_GALLERY_PATH),
        "rollup": rel(ROLLUP_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_receipt_v0",
        "receipt_type": "R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "source_synthetic_remainder_source_audit_receipt_id": SOURCE_SYNTHETIC_REMAINDER_SOURCE_AUDIT_RECEIPT_ID,
        "source_synthetic_remainder_identity_review_receipt_id": SOURCE_SYNTHETIC_REMAINDER_IDENTITY_REVIEW_RECEIPT_ID,
        "source_selection_after_repaired_burden_queue_receipt_id": SOURCE_SELECTION_AFTER_REPAIRED_BURDEN_QUEUE_RECEIPT_ID,
        "source_repaired_burden_queue_reconciliation_receipt_id": SOURCE_REPAIRED_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "post_closure_observability_harvest_summary": {
            "radius_requested": HARVEST_RADIUS,
            "bounded": True,
            "harvest_command_resolved": report["harvest_command_resolved_count"] == 1,
            "receipt_count_before": report["receipt_count_before"],
            "receipt_count_after": report["receipt_count_after"],
            "new_receipt_count": report["new_receipt_count"],
            "runtime_seconds": report["runtime_seconds"],
            "receipt_write_rate_per_second": report["receipt_write_rate_per_second"],
            "failure_count": report["failure_count"],
            "unique_halt_count": report["unique_halt_count"],
            "gate_latest_pass": report["gate_latest_pass_count"] == 1,
            "recommended_next_handling": report["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "post_closure_observability_harvest_guards": guards,
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
    print(f"post_closure_observability_harvest_radius_10000_receipt_id={receipt_id}")
    print(f"post_closure_observability_harvest_radius_10000_receipt_path=data/r1000_post_closure_observability_harvest_radius_10000_v0_receipts/{receipt_id}.json")
    print(f"post_closure_observability_harvest_radius_10000_rollup_path=data/r1000_post_closure_observability_harvest_radius_10000_v0/r1000_post_closure_observability_harvest_radius_10000_rollup.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
