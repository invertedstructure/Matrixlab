from __future__ import annotations

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
