#!/usr/bin/env python3
from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "FIX_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_RUNTIME_OUTPUT_V0"
TARGET_UNIT_ID = "r1000.post_closure_observability_harvest_entrypoint.runtime_output_fix.v0"

SOURCE_RUNTIME_OUTPUT_REVIEW_RECEIPT_ID = "15eaca49"
SOURCE_FAILED_CLI_REGISTRATION_FIX_RECEIPT_ID = "4fd77ccb"
SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID = "960a1048"
SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID = "9d834354"
SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID = "2d61b52e"
SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID = "b35e7989"
SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID = "52d0ea8d"
SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID = "db7c0af2"

PROBE_RADIUS = 10
FUTURE_RETRY_RADIUS = 10000

OUT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0_receipts"

PATCH_PLAN_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_patch_plan.json"
PRIOR_FAILURE_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_prior_failure_surface.json"
MODULE_BEFORE_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_module_before_surface.json"
MODULE_AFTER_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_module_after_surface.json"
CLI_BEFORE_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_cli_before_surface.json"
CLI_AFTER_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_cli_after_surface.json"
PATCH_REPORT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_patch_report.json"
HELP_CHECK_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_help_check.json"
SMALL_PROBE_RESULT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_small_probe_result.json"
RETRY_READY_PACKET_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_retry_ready_packet_after_runtime_output_fix.json"
FIX_DECISION_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_decision.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_report.json"

RUNTIME_OUTPUT_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_failure_review_v0_receipts" / f"{SOURCE_RUNTIME_OUTPUT_REVIEW_RECEIPT_ID}.json"
RUNTIME_OUTPUT_FIX_AUTHORITY_PACKET_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_failure_review_v0" / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_failure_fix_authority_packet.json"
RUNTIME_OUTPUT_CLASSIFICATION_PACKET_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_failure_review_v0" / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_failure_classification_packet.json"
RUNTIME_OUTPUT_PROBE_FAILURE_SURFACE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_failure_review_v0" / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_failure_probe_output_surface.json"

FAILED_CLI_REGISTRATION_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_v0_receipts" / f"{SOURCE_FAILED_CLI_REGISTRATION_FIX_RECEIPT_ID}.json"
FAILED_CLI_REGISTRATION_SMALL_PROBE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_v0" / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_small_probe_result.json"

BUILD_FAILURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_failure_review_v0_receipts" / f"{SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID}.json"
FAILED_ENTRYPOINT_BUILD_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_v0_receipts" / f"{SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID}.json"
CLI_ENTRYPOINT_INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_cli_observability_harvest_entrypoint_inspection_v0_receipts" / f"{SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID}.json"
COMMAND_RESOLVER_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_harvest_command_resolver_fix_v0_receipts" / f"{SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID}.json"

CLOSURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0_receipts" / f"{SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID}.json"
CLOSED_QUEUE_HANDOFF_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0" / "r1000_pressure_queue_closed_handoff_after_synthetic_remainder_expected_limit.json"
EXPECTED_LIMIT_MARK_RECEIPT_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID}.json"
FINAL_QUEUE_STATE_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_final_pressure_queue_state_after_synthetic_remainder_expected_limit.json"

CLI_PATH = ROOT / "src" / "matrixlab" / "cli.py"
ENTRYPOINT_MODULE_PATH = ROOT / "src" / "matrixlab" / "r1000_post_closure_observability_harvest.py"

PROTECTED_SOURCE_FILES = [
    RUNTIME_OUTPUT_REVIEW_RECEIPT_PATH,
    RUNTIME_OUTPUT_FIX_AUTHORITY_PACKET_PATH,
    RUNTIME_OUTPUT_CLASSIFICATION_PACKET_PATH,
    RUNTIME_OUTPUT_PROBE_FAILURE_SURFACE_PATH,
    FAILED_CLI_REGISTRATION_FIX_RECEIPT_PATH,
    FAILED_CLI_REGISTRATION_SMALL_PROBE_PATH,
    BUILD_FAILURE_REVIEW_RECEIPT_PATH,
    FAILED_ENTRYPOINT_BUILD_RECEIPT_PATH,
    CLI_ENTRYPOINT_INSPECTION_RECEIPT_PATH,
    COMMAND_RESOLVER_FIX_RECEIPT_PATH,
    CLOSURE_REVIEW_RECEIPT_PATH,
    CLOSED_QUEUE_HANDOFF_PATH,
    EXPECTED_LIMIT_MARK_RECEIPT_PATH,
    FINAL_QUEUE_STATE_PATH,
]

HUMAN_DECISION = {
    "decision": "FIX_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_RUNTIME_OUTPUT",
    "scope": "repair runtime output and receipt-write path so the post-closure observability harvest command emits exactly one JSON object on stdout and a bounded radius-10 probe writes exactly 10 observation receipts; emit retry-ready packet for radius 10000 only after probe pass",
    "source_runtime_output_review_receipt_id": SOURCE_RUNTIME_OUTPUT_REVIEW_RECEIPT_ID,
    "authorized": [
        "consume runtime-output failure review receipt and fix authority packet",
        "modify src/matrixlab/r1000_post_closure_observability_harvest.py for pure JSON runtime output and receipt writing",
        "modify src/matrixlab/cli.py only if required to call the fixed runtime path",
        "run compile checks",
        "run CLI help check",
        "run bounded radius-10 probe",
        "emit radius-10000 retry-ready packet only if probe writes 10 receipts and stdout parses as JSON",
        "stop before radius-10000 retry",
    ],
    "not_authorized": [
        "running radius-10000 harvest",
        "running unbounded/no-cap harvest",
        "reopening R1000 pressure queue",
        "inspecting closed groups",
        "materializing row payloads",
        "assigning identity values",
        "inventing values",
        "running unrelated repair",
        "applying taxonomy changes",
        "mutating prior artifacts",
        "mutating existing receipts",
        "hiding next command",
    ],
}

MODULE_TEXT = r'''from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import typer

app = typer.Typer(help="Bounded post-closure observability harvest commands.")

ROOT = Path(__file__).resolve().parents[2]

DEFAULT_SOURCE_CLOSURE_RECEIPT = "52d0ea8d"
DEFAULT_SOURCE_MARK_RECEIPT = "db7c0af2"

CLOSURE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0_receipts" / f"{DEFAULT_SOURCE_CLOSURE_RECEIPT}.json"
CLOSED_HANDOFF_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0" / "r1000_pressure_queue_closed_handoff_after_synthetic_remainder_expected_limit.json"
FINAL_QUEUE_STATE_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_final_pressure_queue_state_after_synthetic_remainder_expected_limit.json"
HARVEST_ROOT = ROOT / "data" / "r1000_post_closure_observability_harvest_runs_v0"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")


def _sha8(obj: Any) -> str:
    return hashlib.sha256(_canonical_bytes(obj)).hexdigest()[:8]


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _safe_get(obj: Dict[str, Any], *path: str, default: Any = None) -> Any:
    cur: Any = obj
    for part in path:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(part)
    return default if cur is None else cur


def _validate_closed_queue(source_closure_receipt_id: str) -> Dict[str, Any]:
    closure_path = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0_receipts" / f"{source_closure_receipt_id}.json"
    closure = _read_json(closure_path)
    handoff = _read_json(CLOSED_HANDOFF_PATH)
    final_queue = _read_json(FINAL_QUEUE_STATE_PATH)

    failures: List[str] = []

    closure_summary = (
        closure.get("pressure_queue_closure_review_summary")
        or closure.get("summary")
        or closure.get("closure_review_summary")
        or {}
    )

    if closure.get("gate") != "PASS":
        failures.append("closure_receipt_gate_not_pass")

    queue_closed = (
        closure_summary.get("queue_closed")
        if isinstance(closure_summary, dict)
        else None
    )
    if queue_closed is not True:
        # Some closure receipts encode the closed fact via handoff/final queue artifacts.
        if handoff.get("handoff_status") != "R1000_PRESSURE_QUEUE_CLOSED_NO_REMAINING_PRESSURE":
            failures.append("closure_summary_queue_not_closed")

    remaining_groups = (
        closure_summary.get("remaining_open_group_count")
        if isinstance(closure_summary, dict)
        else None
    )
    remaining_rows = (
        closure_summary.get("remaining_open_row_count")
        if isinstance(closure_summary, dict)
        else None
    )
    if remaining_groups not in (0, None):
        failures.append("closure_remaining_open_group_count_not_zero")
    if remaining_rows not in (0, None):
        failures.append("closure_remaining_open_row_count_not_zero")

    if handoff.get("handoff_status") != "R1000_PRESSURE_QUEUE_CLOSED_NO_REMAINING_PRESSURE":
        failures.append("closed_handoff_status_wrong")
    if handoff.get("next_command_goal") is not None:
        failures.append("closed_handoff_next_command_not_null")

    if final_queue.get("queue_state_status") != "R1000_PRESSURE_QUEUE_CLOSED":
        failures.append("final_queue_state_status_wrong")
    if final_queue.get("remaining_open_group_count") != 0:
        failures.append("final_queue_remaining_group_count_not_zero")
    if final_queue.get("remaining_open_row_count") != 0:
        failures.append("final_queue_remaining_row_count_not_zero")

    return {
        "closed_queue_valid": len(failures) == 0,
        "failures": failures,
        "closure_receipt_path": _rel(closure_path),
        "closed_handoff_status": handoff.get("handoff_status"),
        "final_queue_state_status": final_queue.get("queue_state_status"),
        "remaining_open_group_count": final_queue.get("remaining_open_group_count"),
        "remaining_open_row_count": final_queue.get("remaining_open_row_count"),
    }


def _discover_receipt_paths(exclude_under: Optional[Path] = None) -> List[Path]:
    roots = [ROOT / "data", ROOT / "logs"]
    paths: List[Path] = []
    exclude_resolved = exclude_under.resolve() if exclude_under else None
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*.json"):
            try:
                if exclude_resolved and exclude_resolved in path.resolve().parents:
                    continue
            except FileNotFoundError:
                pass
            lower_name = path.name.lower()
            lower_parent = path.parent.name.lower()
            if "receipt" in lower_name or "receipt" in lower_parent:
                paths.append(path)
    return sorted(set(paths), key=lambda p: _rel(p))


def _receipt_snapshot(exclude_under: Optional[Path] = None) -> Dict[str, Any]:
    paths = _discover_receipt_paths(exclude_under=exclude_under)
    total_size = 0
    gate_counts: Dict[str, int] = {}
    stop_counts: Dict[str, int] = {}
    parse_error_count = 0

    for path in paths:
        total_size += path.stat().st_size
        try:
            obj = _read_json(path)
            gate = str(obj.get("gate"))
            gate_counts[gate] = gate_counts.get(gate, 0) + 1
            terminal = obj.get("terminal")
            stop = None
            if isinstance(terminal, dict):
                stop = terminal.get("stop_code")
            stop = str(stop or "UNKNOWN_OR_ABSENT")
            stop_counts[stop] = stop_counts.get(stop, 0) + 1
        except Exception:
            parse_error_count += 1

    return {
        "receipt_count": len(paths),
        "receipt_total_bytes": total_size,
        "receipt_parse_error_count": parse_error_count,
        "gate_counts": dict(sorted(gate_counts.items())),
        "terminal_stop_histogram": dict(sorted(stop_counts.items())),
    }


def run_bounded_harvest(
    radius: int,
    source_closure_receipt_id: str = DEFAULT_SOURCE_CLOSURE_RECEIPT,
    label: Optional[str] = None,
) -> Dict[str, Any]:
    if radius < 1:
        return {
            "gate": "FAIL",
            "failures": ["radius_must_be_at_least_1"],
            "terminal": {"type": "STOP", "stop_code": "STOP_INVALID_RADIUS", "next_command_goal": None},
        }
    if radius > 250000:
        return {
            "gate": "FAIL",
            "failures": ["radius_safety_cap_exceeded_250000"],
            "terminal": {"type": "STOP", "stop_code": "STOP_RADIUS_SAFETY_CAP_EXCEEDED", "next_command_goal": None},
        }

    created_at = _now_iso()
    run_seed = {
        "unit": "r1000_post_closure_observability_harvest_entrypoint_v0",
        "radius": radius,
        "source_closure_receipt_id": source_closure_receipt_id,
        "label": label or "",
        "created_at": created_at,
    }
    run_id = "run_" + _sha8(run_seed)
    run_dir = HARVEST_ROOT / run_id
    receipt_dir = run_dir / "receipts"
    run_dir.mkdir(parents=True, exist_ok=True)
    receipt_dir.mkdir(parents=True, exist_ok=True)

    start = time.monotonic()
    closed_queue = _validate_closed_queue(source_closure_receipt_id)
    if not closed_queue["closed_queue_valid"]:
        receipt = {
            "schema_version": "r1000_post_closure_observability_harvest_run_receipt_v0",
            "receipt_type": "R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RUN_RECEIPT",
            "receipt_id": _sha8({"run_id": run_id, "closed_queue": closed_queue}),
            "run_id": run_id,
            "radius_requested": radius,
            "radius_completed": 0,
            "source_pressure_queue_closure_review_receipt_id": source_closure_receipt_id,
            "closed_queue_valid": False,
            "failures": closed_queue["failures"],
            "gate": "FAIL",
            "terminal": {"type": "STOP", "stop_code": "STOP_CLOSED_QUEUE_PRECONDITION_FAIL", "next_command_goal": None},
            "created_at": _now_iso(),
        }
        receipt_path = run_dir / "run_receipt.json"
        _write_json(receipt_path, receipt)
        return {
            "gate": "FAIL",
            "run_id": run_id,
            "radius_requested": radius,
            "radius_completed": 0,
            "observation_receipt_count": 0,
            "run_receipt_path": _rel(receipt_path),
            "run_dir": _rel(run_dir),
            "failures": closed_queue["failures"],
            "terminal": receipt["terminal"],
        }

    before_snapshot = _receipt_snapshot(exclude_under=run_dir)
    observation_receipts: List[str] = []
    rolling_state_hash = _sha8({"before_snapshot": before_snapshot, "radius": radius, "run_id": run_id})

    for i in range(radius):
        observation = {
            "schema_version": "r1000_post_closure_observability_observation_receipt_v0",
            "receipt_type": "R1000_POST_CLOSURE_OBSERVABILITY_OBSERVATION_RECEIPT",
            "unit_id": "R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_V0",
            "observation_index": i,
            "run_id": run_id,
            "source_pressure_queue_closure_review_receipt_id": source_closure_receipt_id,
            "source_synthetic_remainder_expected_limit_mark_receipt_id": DEFAULT_SOURCE_MARK_RECEIPT,
            "queue_closed": True,
            "remaining_open_group_count": 0,
            "remaining_open_row_count": 0,
            "radius_requested": radius,
            "bounded": True,
            "unbounded_or_no_cap": False,
            "prior_state_hash": rolling_state_hash,
            "observed_receipt_count_at_start": before_snapshot["receipt_count"],
            "observed_gate_counts_at_start": before_snapshot["gate_counts"],
            "observed_terminal_stop_histogram_at_start": before_snapshot["terminal_stop_histogram"],
            "forbidden_actions": {
                "queue_reopened": False,
                "closed_group_inspected": False,
                "row_payload_materialized": False,
                "row_payload_inspected": False,
                "identity_assignment": False,
                "field_value_invention": False,
                "repair_executed": False,
                "taxonomy_delta_proposal_emitted": False,
                "source_mutated": False,
                "existing_receipts_mutated": False,
                "hidden_next_command": False,
            },
            "gate": "PASS",
            "terminal": {
                "type": "STOP",
                "stop_code": "STOP_POST_CLOSURE_OBSERVATION_RECORDED",
                "next_command_goal": None,
            },
            "created_at": _now_iso(),
        }
        observation["receipt_id"] = _sha8(observation)
        rolling_state_hash = _sha8({"prior": rolling_state_hash, "receipt_id": observation["receipt_id"], "i": i})
        path = receipt_dir / f"{i:08d}_{observation['receipt_id']}.json"
        _write_json(path, observation)
        observation_receipts.append(_rel(path))

    after_snapshot = _receipt_snapshot(exclude_under=None)
    elapsed = time.monotonic() - start

    rollup = {
        "schema_version": "r1000_post_closure_observability_harvest_rollup_v0",
        "run_id": run_id,
        "radius_requested": radius,
        "radius_completed": radius,
        "observation_receipt_count": len(observation_receipts),
        "source_pressure_queue_closure_review_receipt_id": source_closure_receipt_id,
        "closed_queue_valid": True,
        "receipt_count_before": before_snapshot["receipt_count"],
        "receipt_count_after": after_snapshot["receipt_count"],
        "runtime_seconds": round(elapsed, 6),
        "observation_write_rate_per_second": round(len(observation_receipts) / elapsed, 6) if elapsed > 0 else None,
        "gate": "PASS",
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
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_POST_CLOSURE_OBSERVABILITY_HARVEST_COMPLETE",
            "next_command_goal": None,
        },
        "created_at": _now_iso(),
    }
    rollup_path = run_dir / "rollup.json"
    _write_json(rollup_path, rollup)

    index_path = run_dir / "receipt_index.jsonl"
    index_path.write_text("".join(json.dumps({"path": p}, sort_keys=True) + "\n" for p in observation_receipts))

    run_receipt = {
        "schema_version": "r1000_post_closure_observability_harvest_run_receipt_v0",
        "receipt_type": "R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RUN_RECEIPT",
        "receipt_id": _sha8({"run_id": run_id, "radius": radius, "observation_receipt_count": len(observation_receipts)}),
        "run_id": run_id,
        "source_pressure_queue_closure_review_receipt_id": source_closure_receipt_id,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": DEFAULT_SOURCE_MARK_RECEIPT,
        "radius_requested": radius,
        "radius_completed": radius,
        "observation_receipt_count": len(observation_receipts),
        "rollup_path": _rel(rollup_path),
        "receipt_index_path": _rel(index_path),
        "run_dir": _rel(run_dir),
        "gate": "PASS",
        "failures": [],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_POST_CLOSURE_OBSERVABILITY_HARVEST_COMPLETE",
            "next_command_goal": None,
        },
        "created_at": _now_iso(),
    }
    run_receipt_path = run_dir / "run_receipt.json"
    _write_json(run_receipt_path, run_receipt)

    return {
        "gate": "PASS",
        "run_id": run_id,
        "radius_requested": radius,
        "radius_completed": radius,
        "observation_receipt_count": len(observation_receipts),
        "run_receipt_path": _rel(run_receipt_path),
        "rollup_path": _rel(rollup_path),
        "receipt_index_path": _rel(index_path),
        "run_dir": _rel(run_dir),
        "terminal": run_receipt["terminal"],
    }


@app.command("post-closure-observability-harvest")
def post_closure_observability_harvest(
    radius: int = typer.Option(..., "--radius", "-r", min=1, help="Bounded number of observation receipts to emit."),
    source_closure_receipt_id: str = typer.Option(DEFAULT_SOURCE_CLOSURE_RECEIPT, "--source-closure-receipt-id", help="Accepted closure review receipt id."),
    label: Optional[str] = typer.Option(None, "--label", help="Optional run label."),
) -> None:
    """Emit bounded post-closure observability receipts without reopening the closed queue."""
    result = run_bounded_harvest(radius=radius, source_closure_receipt_id=source_closure_receipt_id, label=label)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result.get("gate") != "PASS":
        raise typer.Exit(code=1)
'''

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

def run_cmd(args: List[str], timeout: int = 300) -> Tuple[int, str, str, float]:
    start = time.monotonic()
    proc = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    return proc.returncode, proc.stdout, proc.stderr, time.monotonic() - start

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def validate_sources() -> List[str]:
    failures: List[str] = []
    review = read_json(RUNTIME_OUTPUT_REVIEW_RECEIPT_PATH)
    authority = read_json(RUNTIME_OUTPUT_FIX_AUTHORITY_PACKET_PATH)
    classification = read_json(RUNTIME_OUTPUT_CLASSIFICATION_PACKET_PATH)
    failed_fix = read_json(FAILED_CLI_REGISTRATION_FIX_RECEIPT_PATH)
    failed_probe = read_json(FAILED_CLI_REGISTRATION_SMALL_PROBE_PATH)
    closure = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if review.get("receipt_id") != SOURCE_RUNTIME_OUTPUT_REVIEW_RECEIPT_ID:
        failures.append("runtime_output_review_receipt_id_wrong")
    if review.get("gate") != "PASS":
        failures.append("runtime_output_review_not_pass")
    if review.get("cli_registration_fix_failure_review_summary", {}).get("recommended_next_handling") != UNIT_ID:
        failures.append("runtime_output_review_not_recommending_this_unit")

    if authority.get("authorized_next_unit") != UNIT_ID:
        failures.append("fix_authority_not_for_this_unit")
    if authority.get("fix_authorized_in_this_unit") is not False:
        failures.append("review_unit_authority_leaked_fix_authorization")
    if authority.get("radius_10000_retry_authorized_now") is not False:
        failures.append("review_unit_authorized_radius_10000")

    if classification.get("classification") != "CLI_HELP_FIXED_RUNTIME_OUTPUT_NOT_JSON_AND_RECEIPT_WRITE_NOT_PROVEN":
        failures.append("runtime_output_classification_wrong")

    if failed_fix.get("receipt_id") != SOURCE_FAILED_CLI_REGISTRATION_FIX_RECEIPT_ID:
        failures.append("failed_cli_registration_fix_receipt_id_wrong")
    if failed_fix.get("gate") != "FAIL":
        failures.append("failed_cli_registration_fix_gate_not_fail")
    if failed_probe.get("probe_passed") is not False:
        failures.append("failed_probe_unexpectedly_passed")

    if closure.get("gate") != "PASS":
        failures.append("closure_review_not_pass")
    if handoff.get("handoff_status") != "R1000_PRESSURE_QUEUE_CLOSED_NO_REMAINING_PRESSURE":
        failures.append("closed_queue_handoff_status_wrong")
    if final_queue.get("queue_state_status") != "R1000_PRESSURE_QUEUE_CLOSED":
        failures.append("final_queue_not_closed")
    if final_queue.get("remaining_open_group_count") != 0 or final_queue.get("remaining_open_row_count") != 0:
        failures.append("final_queue_has_remaining_pressure")

    for path in PROTECTED_SOURCE_FILES + [CLI_PATH, ENTRYPOINT_MODULE_PATH]:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")

    return failures

def source_surface(path: Path) -> Dict[str, Any]:
    text = path.read_text()
    return {
        "path": rel(path),
        "sha256": file_sha256(path),
        "line_count": len(text.splitlines()),
        "contains_run_bounded_harvest": "def run_bounded_harvest" in text,
        "contains_post_closure_command": "post-closure-observability-harvest" in text,
        "contains_typer_echo": "typer.echo" in text,
        "contains_rich_console": "Console(" in text or "console." in text,
        "contains_print_json": "print(json.dumps" in text,
        "tail": "\n".join(text.splitlines()[-80:]),
    }

def patch_module() -> Dict[str, Any]:
    before_sha = file_sha256(ENTRYPOINT_MODULE_PATH)
    before_text = ENTRYPOINT_MODULE_PATH.read_text()
    ENTRYPOINT_MODULE_PATH.write_text(MODULE_TEXT)
    after_sha = file_sha256(ENTRYPOINT_MODULE_PATH)
    return {
        "module_path": rel(ENTRYPOINT_MODULE_PATH),
        "before_sha256": before_sha,
        "after_sha256": after_sha,
        "patch_applied": before_sha != after_sha,
        "removed_typer_echo": "typer.echo" in before_text and "typer.echo" not in MODULE_TEXT,
        "run_bounded_harvest_present": "def run_bounded_harvest" in MODULE_TEXT,
        "pure_print_json_present": "print(json.dumps(result" in MODULE_TEXT,
    }

def patch_cli_wrapper() -> Dict[str, Any]:
    before = CLI_PATH.read_text()
    before_sha = file_sha256(CLI_PATH)
    text = before

    # The direct CLI wrapper should only call run_bounded_harvest and print JSON.
    # Replace common noisy echo route if present.
    text = text.replace("typer.echo(json.dumps(result, indent=2, sort_keys=True))", "print(json.dumps(result, indent=2, sort_keys=True))")

    # Ensure import json exists if the direct wrapper uses json.dumps.
    if "json.dumps(result" in text and "import json" not in text:
        lines = text.splitlines()
        insert_at = 0
        for i, line in enumerate(lines):
            if line.startswith("import ") or line.startswith("from "):
                insert_at = i + 1
        lines.insert(insert_at, "import json")
        text = "\n".join(lines) + "\n"

    CLI_PATH.write_text(text)
    after_sha = file_sha256(CLI_PATH)
    return {
        "cli_path": rel(CLI_PATH),
        "before_sha256": before_sha,
        "after_sha256": after_sha,
        "patch_applied": before_sha != after_sha,
        "json_import_present": "import json" in text,
        "uses_print_json": "print(json.dumps(result" in text,
        "uses_typer_echo_json": "typer.echo(json.dumps(result" in text,
    }

def compile_and_help_checks() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    for target in [
        "src/matrixlab/r1000_post_closure_observability_harvest.py",
        "src/matrixlab/cli.py",
    ]:
        rc, out, err, elapsed = run_cmd(["uv", "run", "python", "-m", "py_compile", target])
        checks.append({
            "kind": "py_compile",
            "target": target,
            "returncode": rc,
            "stdout_tail": out[-2000:],
            "stderr_tail": err[-4000:],
            "elapsed_seconds": round(elapsed, 6),
        })

    help_cmd = ["uv", "run", "python", "src/matrixlab/cli.py", "post-closure-observability-harvest", "--help"]
    rc, out, err, elapsed = run_cmd(help_cmd)
    checks.append({
        "kind": "entrypoint_help",
        "target": "post-closure-observability-harvest --help",
        "command": help_cmd,
        "returncode": rc,
        "stdout_tail": out[-8000:],
        "stderr_tail": err[-4000:],
        "elapsed_seconds": round(elapsed, 6),
        "contains_radius": "--radius" in out or "--radius" in err,
        "contains_source_closure_receipt_id": "--source-closure-receipt-id" in out or "--source-closure-receipt-id" in err,
    })

    return {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_help_check_v0",
        "checks": checks,
        "compile_checks_passed": all(c["returncode"] == 0 for c in checks if c["kind"] == "py_compile"),
        "entrypoint_help_passed": any(c["kind"] == "entrypoint_help" and c["returncode"] == 0 and c.get("contains_radius") for c in checks),
    }

def run_module_probe() -> Dict[str, Any]:
    code = "\n".join([
        "import json",
        "from matrixlab.r1000_post_closure_observability_harvest import run_bounded_harvest",
        f"result = run_bounded_harvest(radius={PROBE_RADIUS}, source_closure_receipt_id='{SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID}', label='runtime-output-fix-module-probe')",
        "print(json.dumps(result, indent=2, sort_keys=True))",
    ])
    cmd = ["uv", "run", "python", "-c", code]
    rc, out, err, elapsed = run_cmd(cmd, timeout=300)
    parsed = None
    parse_error = None
    try:
        parsed = json.loads(out)
    except Exception as exc:
        parse_error = f"{type(exc).__name__}: {exc}"
    return {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_module_probe_result_v0",
        "probe_command": cmd,
        "returncode": rc,
        "elapsed_seconds": round(elapsed, 6),
        "stdout_tail": out[-12000:],
        "stderr_tail": err[-4000:],
        "stdout_json_parseable": isinstance(parsed, dict),
        "stdout_parse_error": parse_error,
        "parsed_result": parsed,
        "probe_passed": rc == 0 and isinstance(parsed, dict) and parsed.get("gate") == "PASS" and parsed.get("observation_receipt_count") == PROBE_RADIUS,
        "probe_observation_receipt_count": parsed.get("observation_receipt_count") if isinstance(parsed, dict) else None,
        "probe_run_dir": parsed.get("run_dir") if isinstance(parsed, dict) else None,
        "probe_run_receipt_path": parsed.get("run_receipt_path") if isinstance(parsed, dict) else None,
    }

def run_cli_probe() -> Dict[str, Any]:
    cmd = [
        "uv", "run", "python", "src/matrixlab/cli.py",
        "post-closure-observability-harvest",
        "--radius", str(PROBE_RADIUS),
        "--source-closure-receipt-id", SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "--label", "runtime-output-fix-cli-probe",
    ]
    rc, out, err, elapsed = run_cmd(cmd, timeout=300)
    parsed = None
    parse_error = None
    try:
        parsed = json.loads(out)
    except Exception as exc:
        parse_error = f"{type(exc).__name__}: {exc}"

    return {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_small_probe_result_v0",
        "probe_command": cmd,
        "returncode": rc,
        "elapsed_seconds": round(elapsed, 6),
        "stdout_tail": out[-12000:],
        "stderr_tail": err[-4000:],
        "stdout_json_parseable": isinstance(parsed, dict),
        "stdout_parse_error": parse_error,
        "parsed_result": parsed,
        "probe_passed": rc == 0 and isinstance(parsed, dict) and parsed.get("gate") == "PASS" and parsed.get("observation_receipt_count") == PROBE_RADIUS and (parsed.get("terminal") or {}).get("next_command_goal") is None,
        "probe_radius": PROBE_RADIUS,
        "probe_observation_receipt_count": parsed.get("observation_receipt_count") if isinstance(parsed, dict) else None,
        "probe_run_receipt_path": parsed.get("run_receipt_path") if isinstance(parsed, dict) else None,
        "probe_rollup_path": parsed.get("rollup_path") if isinstance(parsed, dict) else None,
        "probe_run_dir": parsed.get("run_dir") if isinstance(parsed, dict) else None,
    }

def build_retry_packet(probe: Dict[str, Any]) -> Dict[str, Any]:
    ready = probe.get("probe_passed") is True
    command = [
        "uv", "run", "python", "src/matrixlab/cli.py",
        "post-closure-observability-harvest",
        "--radius", str(FUTURE_RETRY_RADIUS),
        "--source-closure-receipt-id", SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "--label", "radius-10000-post-closure-observability-harvest",
    ]
    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_retry_ready_packet_after_runtime_output_fix_v0",
        "packet_status": "RADIUS_10000_RETRY_READY_SEPARATE_UNIT" if ready else "RADIUS_10000_RETRY_BLOCKED_RUNTIME_OUTPUT_FIX_PROBE_FAILED",
        "source_runtime_output_review_receipt_id": SOURCE_RUNTIME_OUTPUT_REVIEW_RECEIPT_ID,
        "entrypoint_command": "post-closure-observability-harvest",
        "runtime_output_fixed": ready,
        "small_probe_passed": ready,
        "small_probe_radius": PROBE_RADIUS,
        "small_probe_observation_receipt_count": probe.get("probe_observation_receipt_count"),
        "radius_10000_retry_command": command if ready else None,
        "radius_10000_retry_authorized_in_this_unit": False,
        "requires_separate_retry_unit": ready,
        "recommended_next_handling": "RETRY_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_WITH_RUNTIME_OUTPUT_FIXED_V0" if ready else "REVIEW_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_RUNTIME_OUTPUT_FIX_FAILURE_V0",
    }

def validate_probe_files(probe: Dict[str, Any]) -> Dict[str, Any]:
    run_dir = probe.get("probe_run_dir")
    run_receipt = probe.get("probe_run_receipt_path")
    rollup = probe.get("probe_rollup_path")
    checks = {
        "run_dir_exists": bool(run_dir) and (ROOT / run_dir).exists(),
        "run_receipt_exists": bool(run_receipt) and (ROOT / run_receipt).exists(),
        "rollup_exists": bool(rollup) and (ROOT / rollup).exists(),
        "observation_receipt_files_count": 0,
    }
    if run_dir and (ROOT / run_dir / "receipts").exists():
        checks["observation_receipt_files_count"] = len(list((ROOT / run_dir / "receipts").glob("*.json")))
    checks["files_valid"] = (
        checks["run_dir_exists"]
        and checks["run_receipt_exists"]
        and checks["rollup_exists"]
        and checks["observation_receipt_files_count"] == PROBE_RADIUS
    )
    return checks

def validate_outputs(help_check: Dict[str, Any], module_probe: Dict[str, Any], cli_probe: Dict[str, Any], retry_packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if help_check.get("compile_checks_passed") is not True:
        failures.append("compile_checks_not_passed")
    if help_check.get("entrypoint_help_passed") is not True:
        failures.append("entrypoint_help_not_passed")
    if module_probe.get("probe_passed") is not True:
        failures.append("module_probe_not_passed")
    if cli_probe.get("stdout_json_parseable") is not True:
        failures.append("cli_probe_stdout_not_json")
    if cli_probe.get("probe_passed") is not True:
        failures.append("cli_probe_not_passed")
    if cli_probe.get("probe_observation_receipt_count") != PROBE_RADIUS:
        failures.append("cli_probe_receipt_count_wrong")
    if retry_packet.get("packet_status") != "RADIUS_10000_RETRY_READY_SEPARATE_UNIT":
        failures.append("retry_packet_not_ready")
    if retry_packet.get("radius_10000_retry_authorized_in_this_unit") is not False:
        failures.append("radius_10000_authorized_in_this_unit")

    for key in [
        "radius_10000_retry_executed_count",
        "unbounded_or_no_cap_run_count",
        "queue_reopened_count",
        "closed_group_inspected_count",
        "row_payload_materialized_count",
        "row_payload_inspected_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "repair_executed_outside_runtime_output_count",
        "taxonomy_delta_proposal_emitted_count",
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
    for key in [
        "runtime_output_review_receipt_consumed_count",
        "fix_authority_packet_consumed_count",
        "module_before_surface_emitted_count",
        "module_after_surface_emitted_count",
        "cli_before_surface_emitted_count",
        "cli_after_surface_emitted_count",
        "patch_report_emitted_count",
        "help_check_emitted_count",
        "module_probe_executed_count",
        "module_probe_passed_count",
        "cli_probe_executed_count",
        "cli_probe_passed_count",
        "retry_ready_packet_emitted_count",
        "fix_decision_emitted_count",
    ]:
        if metrics.get(key) != 1:
            failures.append(f"metric_not_one:{key}:{metrics.get(key)}")

    for key in [
        "radius_10000_retry_executed_count",
        "unbounded_or_no_cap_run_count",
        "queue_reopened_count",
        "closed_group_inspected_count",
        "row_payload_materialized_count",
        "row_payload_inspected_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "repair_executed_outside_runtime_output_count",
        "taxonomy_delta_proposal_emitted_count",
        "existing_receipt_mutation_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_RUNTIME_OUTPUT_FIX_COMPLETE_SMALL_PROBE_PASSED_RETRY_READY":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    protected_before = snapshot_files(PROTECTED_SOURCE_FILES)
    failures = validate_sources()

    prior_failure_surface = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_prior_failure_surface_v0",
        "source_runtime_output_review_receipt_id": SOURCE_RUNTIME_OUTPUT_REVIEW_RECEIPT_ID,
        "runtime_output_review_summary": read_json(RUNTIME_OUTPUT_REVIEW_RECEIPT_PATH).get("cli_registration_fix_failure_review_summary"),
        "failed_cli_registration_probe": read_json(FAILED_CLI_REGISTRATION_SMALL_PROBE_PATH),
    }
    write_json(PRIOR_FAILURE_SURFACE_PATH, prior_failure_surface)

    write_json(MODULE_BEFORE_SURFACE_PATH, source_surface(ENTRYPOINT_MODULE_PATH))
    write_json(CLI_BEFORE_SURFACE_PATH, source_surface(CLI_PATH))

    patch_plan = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_patch_plan_v0",
        "source_runtime_output_review_receipt_id": SOURCE_RUNTIME_OUTPUT_REVIEW_RECEIPT_ID,
        "classification": "CLI_HELP_FIXED_RUNTIME_OUTPUT_NOT_JSON_AND_RECEIPT_WRITE_NOT_PROVEN",
        "actions": [
            "rewrite entrypoint module with deterministic run_bounded_harvest",
            "make invalid-radius/precondition failures return JSON instead of raising before print",
            "make command wrapper print exactly json.dumps(result)",
            "replace typer.echo(json.dumps(...)) in CLI wrapper with print(json.dumps(...))",
            "verify module-level probe and CLI-level probe both produce JSON",
            "require CLI radius-10 probe to write exactly 10 observation receipts",
        ],
        "radius_10000_authorized_in_this_unit": False,
    }
    write_json(PATCH_PLAN_PATH, patch_plan)

    module_patch = patch_module()
    cli_patch = patch_cli_wrapper()

    write_json(MODULE_AFTER_SURFACE_PATH, source_surface(ENTRYPOINT_MODULE_PATH))
    write_json(CLI_AFTER_SURFACE_PATH, source_surface(CLI_PATH))

    help_check = compile_and_help_checks()
    write_json(HELP_CHECK_PATH, help_check)

    module_probe = run_module_probe()
    cli_probe = run_cli_probe()
    cli_probe_file_checks = validate_probe_files(cli_probe)
    cli_probe["probe_file_checks"] = cli_probe_file_checks
    write_json(SMALL_PROBE_RESULT_PATH, {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_probe_results_v0",
        "module_probe": module_probe,
        "cli_probe": cli_probe,
        "selected_probe": cli_probe,
    })

    retry_packet = build_retry_packet(cli_probe)
    write_json(RETRY_READY_PACKET_PATH, retry_packet)

    decision = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_decision_v0",
        "decision_id": sha8({
            "unit_id": UNIT_ID,
            "module_probe_passed": module_probe.get("probe_passed"),
            "cli_probe_passed": cli_probe.get("probe_passed"),
        }),
        "decision_status": "RUNTIME_OUTPUT_FIXED_SMALL_PROBE_PASSED_RETRY_READY" if cli_probe.get("probe_passed") else "RUNTIME_OUTPUT_FIX_INCOMPLETE_SMALL_PROBE_FAILED",
        "runtime_output_fixed": cli_probe.get("probe_passed") is True,
        "help_check_passed": help_check.get("entrypoint_help_passed") is True,
        "module_probe_passed": module_probe.get("probe_passed") is True,
        "cli_probe_passed": cli_probe.get("probe_passed") is True,
        "cli_probe_stdout_json_parseable": cli_probe.get("stdout_json_parseable") is True,
        "cli_probe_observation_receipt_count": cli_probe.get("probe_observation_receipt_count"),
        "radius_10000_retry_ready": retry_packet["packet_status"] == "RADIUS_10000_RETRY_READY_SEPARATE_UNIT",
        "radius_10000_retry_executed": False,
        "recommended_next_handling": retry_packet["recommended_next_handling"],
    }
    write_json(FIX_DECISION_PATH, decision)

    report = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_runtime_output_review_receipt_id": SOURCE_RUNTIME_OUTPUT_REVIEW_RECEIPT_ID,
        "runtime_output_review_receipt_consumed_count": 1,
        "fix_authority_packet_consumed_count": 1,
        "prior_failure_surface_emitted_count": 1,
        "module_before_surface_emitted_count": 1,
        "module_after_surface_emitted_count": 1,
        "cli_before_surface_emitted_count": 1,
        "cli_after_surface_emitted_count": 1,
        "patch_report_emitted_count": 1,
        "module_patch_applied_count": 1 if module_patch["patch_applied"] else 0,
        "cli_patch_applied_count": 1 if cli_patch["patch_applied"] else 0,
        "help_check_emitted_count": 1,
        "compile_checks_passed_count": 1 if help_check.get("compile_checks_passed") else 0,
        "entrypoint_help_passed_count": 1 if help_check.get("entrypoint_help_passed") else 0,
        "module_probe_executed_count": 1,
        "module_probe_passed_count": 1 if module_probe.get("probe_passed") else 0,
        "cli_probe_executed_count": 1,
        "cli_probe_passed_count": 1 if cli_probe.get("probe_passed") else 0,
        "cli_probe_stdout_json_parseable_count": 1 if cli_probe.get("stdout_json_parseable") else 0,
        "cli_probe_observation_receipt_count": cli_probe.get("probe_observation_receipt_count") or 0,
        "cli_probe_observation_receipt_files_count": cli_probe_file_checks["observation_receipt_files_count"],
        "runtime_output_fixed_count": 1 if cli_probe.get("probe_passed") else 0,
        "retry_ready_packet_emitted_count": 1,
        "radius_10000_retry_ready_count": 1 if retry_packet["packet_status"] == "RADIUS_10000_RETRY_READY_SEPARATE_UNIT" else 0,
        "fix_decision_emitted_count": 1,
        "radius_10000_retry_executed_count": 0,
        "unbounded_or_no_cap_run_count": 0,
        "queue_reopened_count": 0,
        "closed_group_inspected_count": 0,
        "row_payload_materialized_count": 0,
        "row_payload_inspected_count": 0,
        "identity_assignment_count": 0,
        "field_value_invention_count": 0,
        "repair_executed_outside_runtime_output_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": retry_packet["recommended_next_handling"],
    }
    write_json(REPORT_PATH, report)

    patch_report = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_patch_report_v0",
        "module_patch": module_patch,
        "cli_patch": cli_patch,
        "help_check_ref": rel(HELP_CHECK_PATH),
        "small_probe_result_ref": rel(SMALL_PROBE_RESULT_PATH),
    }
    write_json(PATCH_REPORT_PATH, patch_report)

    failures.extend(validate_outputs(help_check, module_probe, cli_probe, retry_packet, report))

    protected_after = snapshot_files(PROTECTED_SOURCE_FILES)
    protected_mutation_detected = protected_before != protected_after
    if protected_mutation_detected:
        failures.append("protected_prior_artifact_hash_changed")

    trace = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_transition_trace_v0",
        "trace": [
            {
                "step": "consume_runtime_output_failure_review",
                "question": "help fixed but runtime output/receipt write failed",
                "answer": True,
                "taken": "patch_runtime_output",
            },
            {
                "step": "patch_runtime_output",
                "question": "compile and help checks pass",
                "answer": help_check.get("compile_checks_passed") is True and help_check.get("entrypoint_help_passed") is True,
                "taken": "run_module_probe",
            },
            {
                "step": "run_module_probe",
                "question": "module path emits JSON and receipts",
                "answer": module_probe.get("probe_passed") is True,
                "taken": "run_cli_probe",
            },
            {
                "step": "run_cli_probe",
                "question": "CLI stdout is JSON and writes 10 observation receipts",
                "answer": cli_probe.get("probe_passed") is True,
                "taken": "emit_retry_ready_packet" if cli_probe.get("probe_passed") else "emit_runtime_output_fix_failure_packet",
            },
            {
                "step": "emit_retry_ready_packet",
                "question": "run radius 10000 now",
                "answer": False,
                "taken": "STOP_RUNTIME_OUTPUT_FIX_COMPLETE_SMALL_PROBE_PASSED_RETRY_READY" if cli_probe.get("probe_passed") else "STOP_RUNTIME_OUTPUT_FIX_INCOMPLETE_SMALL_PROBE_FAILED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_RUNTIME_OUTPUT_FIX_COMPLETE_SMALL_PROBE_PASSED_RETRY_READY" if cli_probe.get("probe_passed") else "STOP_RUNTIME_OUTPUT_FIX_INCOMPLETE_SMALL_PROBE_FAILED",
            "next_command_goal": None,
        },
    }
    write_json(TRANSITION_TRACE_PATH, trace)

    acceptance_gate_results = {
        "RUNTIME_OUTPUT_FIX_0_REVIEW_CONSUMED": True,
        "RUNTIME_OUTPUT_FIX_1_MODULE_PATCHED": report["module_patch_applied_count"] == 1,
        "RUNTIME_OUTPUT_FIX_2_HELP_AND_COMPILE_PASS": help_check.get("compile_checks_passed") is True and help_check.get("entrypoint_help_passed") is True,
        "RUNTIME_OUTPUT_FIX_3_MODULE_PROBE_PASSES": report["module_probe_passed_count"] == 1,
        "RUNTIME_OUTPUT_FIX_4_CLI_PROBE_STDOUT_JSON": report["cli_probe_stdout_json_parseable_count"] == 1,
        "RUNTIME_OUTPUT_FIX_5_CLI_PROBE_WRITES_10_RECEIPTS": report["cli_probe_passed_count"] == 1 and report["cli_probe_observation_receipt_count"] == PROBE_RADIUS and report["cli_probe_observation_receipt_files_count"] == PROBE_RADIUS,
        "RUNTIME_OUTPUT_FIX_6_RETRY_READY_PACKET_EMITTED": report["retry_ready_packet_emitted_count"] == 1 and report["radius_10000_retry_ready_count"] == 1,
        "RUNTIME_OUTPUT_FIX_7_RADIUS_10000_NOT_EXECUTED": report["radius_10000_retry_executed_count"] == 0,
        "RUNTIME_OUTPUT_FIX_8_NO_UNBOUNDED_RUN": report["unbounded_or_no_cap_run_count"] == 0,
        "RUNTIME_OUTPUT_FIX_9_NO_QUEUE_OR_ROW_ACTION": report["queue_reopened_count"] == 0 and report["row_payload_materialized_count"] == 0,
        "RUNTIME_OUTPUT_FIX_10_NO_PRIOR_ARTIFACT_OR_RECEIPT_MUTATION": protected_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "RUNTIME_OUTPUT_FIX_11_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if protected_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_runtime_output_review_receipt_id": SOURCE_RUNTIME_OUTPUT_REVIEW_RECEIPT_ID,
        "source_failed_cli_registration_fix_receipt_id": SOURCE_FAILED_CLI_REGISTRATION_FIX_RECEIPT_ID,
        "source_build_failure_review_receipt_id": SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_entrypoint_build_receipt_id": SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID,
        "source_cli_entrypoint_inspection_receipt_id": SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID,
        "source_command_resolver_fix_receipt_id": SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "protected_prior_artifact_mutation_count": 1 if protected_mutation_detected else 0,
    }

    guards = {
        "runtime_output_review_consumed": True,
        "runtime_output_fix_authorized": True,
        "entrypoint_module_modified": module_patch["patch_applied"],
        "cli_source_modified": cli_patch["patch_applied"],
        "help_check_passed": help_check.get("entrypoint_help_passed"),
        "module_probe_passed": module_probe.get("probe_passed"),
        "cli_probe_executed": True,
        "cli_probe_passed": cli_probe.get("probe_passed"),
        "cli_probe_stdout_json_parseable": cli_probe.get("stdout_json_parseable"),
        "radius_10000_retry_ready": retry_packet["packet_status"] == "RADIUS_10000_RETRY_READY_SEPARATE_UNIT",
        "radius_10000_retry_authorized_in_this_unit": False,
        "radius_10000_retry_executed": False,
        "unbounded_or_no_cap_run": False,
        "queue_reopened": False,
        "closed_group_inspected": False,
        "row_payload_materialized": False,
        "row_payload_inspected": False,
        "identity_assignment": False,
        "field_value_invention": False,
        "repair_executed_outside_runtime_output": False,
        "taxonomy_delta_proposal_emitted": False,
        "existing_receipts_mutated": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_runtime_output_review_receipt_id": SOURCE_RUNTIME_OUTPUT_REVIEW_RECEIPT_ID,
        "cli_probe_passed": cli_probe.get("probe_passed"),
        "retry_ready": retry_packet["packet_status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "patch_plan": rel(PATCH_PLAN_PATH),
        "prior_failure_surface": rel(PRIOR_FAILURE_SURFACE_PATH),
        "module_before_surface": rel(MODULE_BEFORE_SURFACE_PATH),
        "module_after_surface": rel(MODULE_AFTER_SURFACE_PATH),
        "cli_before_surface": rel(CLI_BEFORE_SURFACE_PATH),
        "cli_after_surface": rel(CLI_AFTER_SURFACE_PATH),
        "patch_report": rel(PATCH_REPORT_PATH),
        "help_check": rel(HELP_CHECK_PATH),
        "small_probe_result": rel(SMALL_PROBE_RESULT_PATH),
        "retry_ready_packet": rel(RETRY_READY_PACKET_PATH),
        "fix_decision": rel(FIX_DECISION_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "cli_path": rel(CLI_PATH),
        "entrypoint_module_path": rel(ENTRYPOINT_MODULE_PATH),
    }

    receipt = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_receipt_v0",
        "receipt_type": "R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_RUNTIME_OUTPUT_FIX_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_runtime_output_review_receipt_id": SOURCE_RUNTIME_OUTPUT_REVIEW_RECEIPT_ID,
        "source_failed_cli_registration_fix_receipt_id": SOURCE_FAILED_CLI_REGISTRATION_FIX_RECEIPT_ID,
        "source_build_failure_review_receipt_id": SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_entrypoint_build_receipt_id": SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID,
        "source_cli_entrypoint_inspection_receipt_id": SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID,
        "source_command_resolver_fix_receipt_id": SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "runtime_output_fix_summary": {
            "decision_status": decision["decision_status"],
            "runtime_output_fixed": decision["runtime_output_fixed"],
            "entrypoint_command": "post-closure-observability-harvest",
            "help_check_passed": decision["help_check_passed"],
            "module_probe_passed": decision["module_probe_passed"],
            "cli_probe_executed": True,
            "cli_probe_passed": decision["cli_probe_passed"],
            "cli_probe_stdout_json_parseable": decision["cli_probe_stdout_json_parseable"],
            "cli_probe_observation_receipt_count": decision["cli_probe_observation_receipt_count"],
            "radius_10000_retry_ready": decision["radius_10000_retry_ready"],
            "radius_10000_retry_executed": False,
            "radius_10000_retry_command": retry_packet["radius_10000_retry_command"],
            "recommended_next_handling": decision["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "runtime_output_fix_guards": guards,
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
    print(f"runtime_output_fix_receipt_id={receipt_id}")
    print(f"runtime_output_fix_receipt_path=data/r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0_receipts/{receipt_id}.json")
    print(f"retry_ready_packet_path=data/r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0/r1000_post_closure_observability_harvest_radius_10000_retry_ready_packet_after_runtime_output_fix.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
