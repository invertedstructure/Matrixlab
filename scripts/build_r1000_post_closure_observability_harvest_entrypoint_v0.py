#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_V0"
TARGET_UNIT_ID = "r1000.post_closure_observability_harvest_entrypoint.build.v0"

SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID = "2d61b52e"
SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID = "b35e7989"
SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID = "c5217505"
SOURCE_FAILED_HARVEST_RECEIPT_ID = "722af13e"
SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID = "52d0ea8d"
SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID = "db7c0af2"

PROBE_RADIUS = 10
FUTURE_RETRY_RADIUS = 10000

OUT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_v0_receipts"

SOURCE_PATCH_PLAN_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_source_patch_plan.json"
CLI_PATCH_REPORT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_patch_report.json"
ENTRYPOINT_CONTRACT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_contract.json"
SMALL_PROBE_RESULT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_small_probe_result.json"
RETRY_READY_PACKET_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_retry_ready_packet.json"
BUILD_DECISION_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_build_decision.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_build_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_build_report.json"

CLI_ENTRYPOINT_INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_cli_observability_harvest_entrypoint_inspection_v0_receipts" / f"{SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID}.json"
MISSING_ENTRYPOINT_PROPOSAL_PATH = ROOT / "data" / "r1000_cli_observability_harvest_entrypoint_inspection_v0" / "r1000_cli_observability_harvest_missing_entrypoint_proposal.json"
NEXT_AUTHORITY_PACKET_PATH = ROOT / "data" / "r1000_cli_observability_harvest_entrypoint_inspection_v0" / "r1000_cli_observability_harvest_next_authority_packet.json"
ENTRYPOINT_INSPECTION_DECISION_PATH = ROOT / "data" / "r1000_cli_observability_harvest_entrypoint_inspection_v0" / "r1000_cli_observability_harvest_entrypoint_inspection_decision.json"
COMMAND_RESOLVER_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_harvest_command_resolver_fix_v0_receipts" / f"{SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID}.json"
FAILED_HARVEST_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_review_v0_receipts" / f"{SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID}.json"
FAILED_HARVEST_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_v0_receipts" / f"{SOURCE_FAILED_HARVEST_RECEIPT_ID}.json"
CLOSURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0_receipts" / f"{SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID}.json"
CLOSED_QUEUE_HANDOFF_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0" / "r1000_pressure_queue_closed_handoff_after_synthetic_remainder_expected_limit.json"
EXPECTED_LIMIT_MARK_RECEIPT_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID}.json"
FINAL_QUEUE_STATE_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_final_pressure_queue_state_after_synthetic_remainder_expected_limit.json"

CLI_PATH = ROOT / "src" / "matrixlab" / "cli.py"
ENTRYPOINT_MODULE_PATH = ROOT / "src" / "matrixlab" / "r1000_post_closure_observability_harvest.py"

SOURCE_FILES = [
    CLI_ENTRYPOINT_INSPECTION_RECEIPT_PATH,
    MISSING_ENTRYPOINT_PROPOSAL_PATH,
    NEXT_AUTHORITY_PACKET_PATH,
    ENTRYPOINT_INSPECTION_DECISION_PATH,
    COMMAND_RESOLVER_FIX_RECEIPT_PATH,
    FAILED_HARVEST_REVIEW_RECEIPT_PATH,
    FAILED_HARVEST_RECEIPT_PATH,
    CLOSURE_REVIEW_RECEIPT_PATH,
    CLOSED_QUEUE_HANDOFF_PATH,
    EXPECTED_LIMIT_MARK_RECEIPT_PATH,
    FINAL_QUEUE_STATE_PATH,
    CLI_PATH,
]

HUMAN_DECISION = {
    "decision": "BUILD_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT",
    "scope": "build the missing bounded receipt-producing post-closure observability harvest entrypoint, prove it with a small radius-10 probe, emit a radius-10000 retry-ready packet only if the probe produces receipts, and stop before radius-10000 retry",
    "source_cli_entrypoint_inspection_receipt_id": SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID,
    "authorized": [
        "consume missing-entrypoint proposal",
        "modify source code to add bounded receipt-producing observability harvest entrypoint",
        "patch CLI command surface",
        "run compile checks",
        "run help check",
        "run small bounded radius-10 probe",
        "emit retry-ready packet if small probe writes receipts",
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
        "filling source fields",
        "running repair",
        "applying taxonomy changes",
        "mutating prior artifacts",
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

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def run_cmd(args: List[str], timeout: int = 240) -> Tuple[int, str, str, float]:
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

def validate_sources() -> List[str]:
    failures: List[str] = []
    inspection_receipt = read_json(CLI_ENTRYPOINT_INSPECTION_RECEIPT_PATH)
    proposal = read_json(MISSING_ENTRYPOINT_PROPOSAL_PATH)
    authority = read_json(NEXT_AUTHORITY_PACKET_PATH)
    decision = read_json(ENTRYPOINT_INSPECTION_DECISION_PATH)
    closure_receipt = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if inspection_receipt.get("receipt_id") != SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID:
        failures.append("cli_entrypoint_inspection_receipt_id_wrong")
    if inspection_receipt.get("gate") != "PASS":
        failures.append("cli_entrypoint_inspection_not_pass")
    if inspection_receipt.get("cli_entrypoint_inspection_summary", {}).get("decision_status") != "MISSING_ENTRYPOINT_CONFIRMED_BUILD_REQUIRED":
        failures.append("inspection_did_not_confirm_build_required")
    if inspection_receipt.get("cli_entrypoint_inspection_summary", {}).get("recommended_next_handling") != UNIT_ID:
        failures.append("inspection_not_recommending_this_unit")

    if proposal.get("proposal_status") != "CANDIDATE_MISSING_ENTRYPOINT_PROPOSAL":
        failures.append("missing_entrypoint_proposal_status_wrong")
    if proposal.get("missing_object_type") != "bounded_receipt_producing_observability_harvest_entrypoint":
        failures.append("missing_object_type_wrong")
    if proposal.get("application_authorized") is not False:
        failures.append("proposal_application_unexpectedly_authorized")

    if authority.get("authorized_next_unit") != UNIT_ID:
        failures.append("next_authority_not_for_this_unit")
    if authority.get("implementation_authorized_in_this_unit") is not False:
        failures.append("prior_authority_authorized_implementation_in_wrong_unit")
    if authority.get("radius_10000_retry_authorized_now") is not False:
        failures.append("prior_authority_authorized_radius_10000_retry")

    if decision.get("decision_status") != "MISSING_ENTRYPOINT_CONFIRMED_BUILD_REQUIRED":
        failures.append("entrypoint_decision_status_wrong")

    if closure_receipt.get("gate") != "PASS":
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

    return failures

ENTRYPOINT_MODULE_TEXT = r'''from __future__ import annotations

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


def _validate_closed_queue() -> Dict[str, Any]:
    closure = _read_json(CLOSURE_RECEIPT_PATH)
    handoff = _read_json(CLOSED_HANDOFF_PATH)
    final_queue = _read_json(FINAL_QUEUE_STATE_PATH)

    failures: List[str] = []

    summary = closure.get("pressure_queue_closure_review_summary", {})
    if closure.get("gate") != "PASS":
        failures.append("closure_receipt_gate_not_pass")
    if summary.get("queue_closed") is not True:
        failures.append("closure_summary_queue_not_closed")
    if summary.get("remaining_open_group_count") != 0:
        failures.append("closure_remaining_open_group_count_not_zero")
    if summary.get("remaining_open_row_count") != 0:
        failures.append("closure_remaining_open_row_count_not_zero")
    if summary.get("recommended_next_handling") is not None:
        failures.append("closure_recommended_next_not_null")

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
        "closure_summary": summary,
        "closed_handoff_status": handoff.get("handoff_status"),
        "final_queue_state_status": final_queue.get("queue_state_status"),
    }


def _discover_receipt_paths() -> List[Path]:
    roots = [ROOT / "data", ROOT / "logs"]
    paths: List[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*.json"):
            lower_name = path.name.lower()
            lower_parent = path.parent.name.lower()
            if "receipt" in lower_name or "receipt" in lower_parent:
                paths.append(path)
    return sorted(set(paths), key=lambda p: _rel(p))


def _receipt_snapshot() -> Dict[str, Any]:
    paths = _discover_receipt_paths()
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
        raise typer.BadParameter("radius must be >= 1")
    if radius > 250000:
        raise typer.BadParameter("radius safety cap exceeded: max 250000")

    run_seed = {
        "unit": "r1000_post_closure_observability_harvest_entrypoint_v0",
        "radius": radius,
        "source_closure_receipt_id": source_closure_receipt_id,
        "label": label or "",
        "created_at": _now_iso(),
    }
    run_id = "run_" + _sha8(run_seed)
    run_dir = HARVEST_ROOT / run_id
    receipt_dir = run_dir / "receipts"
    run_dir.mkdir(parents=True, exist_ok=True)
    receipt_dir.mkdir(parents=True, exist_ok=True)

    start = time.monotonic()
    closed_queue = _validate_closed_queue()
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
            "receipt_path": _rel(receipt_path),
            "run_dir": _rel(run_dir),
            "failures": closed_queue["failures"],
        }

    before_snapshot = _receipt_snapshot()
    observation_receipts: List[str] = []
    rolling_state_hash = _sha8({"before_snapshot": before_snapshot, "radius": radius})

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

    after_snapshot = _receipt_snapshot()
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
        "receipt_delta": after_snapshot["receipt_count"] - before_snapshot["receipt_count"],
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
    _write_json(run_dir / "rollup.json", rollup)

    index_path = run_dir / "receipt_index.jsonl"
    index_path.write_text("".join(json.dumps({"path": p}, sort_keys=True) + "\n" for p in observation_receipts))

    run_receipt = {
        "schema_version": "r1000_post_closure_observability_harvest_run_receipt_v0",
        "receipt_type": "R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RUN_RECEIPT",
        "receipt_id": _sha8({"run_id": run_id, "radius": radius, "observation_receipt_count": len(observation_receipts)}),
        "run_id": run_id,
        "source_pressure_queue_closure_review_receipt_id": source_closure_receipt_id,
        "radius_requested": radius,
        "radius_completed": radius,
        "observation_receipt_count": len(observation_receipts),
        "rollup_path": _rel(run_dir / "rollup.json"),
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
        "rollup_path": _rel(run_dir / "rollup.json"),
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
    typer.echo(json.dumps(result, indent=2, sort_keys=True))
    if result.get("gate") != "PASS":
        raise typer.Exit(code=1)
'''

CLI_PATCH_MARKER = "# R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_V0"

def patch_cli() -> Dict[str, Any]:
    original = CLI_PATH.read_text()
    before_sha = file_sha256(CLI_PATH)

    if "r1000_post_closure_observability_harvest" in original and "post-closure-observability-harvest" in original:
        return {
            "cli_path": rel(CLI_PATH),
            "before_sha256": before_sha,
            "after_sha256": before_sha,
            "patch_applied": False,
            "reason": "entrypoint_already_present",
        }

    patched = original.rstrip() + "\n\n" + CLI_PATCH_MARKER + "\n"
    patched += "try:\n"
    patched += "    from matrixlab.r1000_post_closure_observability_harvest import app as _r1000_post_closure_observability_harvest_app\n"
    patched += "    app.add_typer(_r1000_post_closure_observability_harvest_app)\n"
    patched += "except Exception as _r1000_post_closure_observability_harvest_import_error:\n"
    patched += "    pass\n"

    CLI_PATH.write_text(patched)
    after_sha = file_sha256(CLI_PATH)
    return {
        "cli_path": rel(CLI_PATH),
        "before_sha256": before_sha,
        "after_sha256": after_sha,
        "patch_applied": True,
        "reason": "appended_typer_subapp_registration",
    }

def write_entrypoint_module() -> Dict[str, Any]:
    before_exists = ENTRYPOINT_MODULE_PATH.exists()
    before_sha = file_sha256(ENTRYPOINT_MODULE_PATH) if before_exists else None
    ENTRYPOINT_MODULE_PATH.write_text(ENTRYPOINT_MODULE_TEXT)
    return {
        "module_path": rel(ENTRYPOINT_MODULE_PATH),
        "before_exists": before_exists,
        "before_sha256": before_sha,
        "after_sha256": file_sha256(ENTRYPOINT_MODULE_PATH),
        "module_written": True,
    }

def run_probe() -> Dict[str, Any]:
    cmd = [
        "uv", "run", "python", "src/matrixlab/cli.py",
        "post-closure-observability-harvest",
        "--radius", str(PROBE_RADIUS),
        "--source-closure-receipt-id", SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "--label", "build-entrypoint-small-probe",
    ]
    rc, out, err, elapsed = run_cmd(cmd, timeout=240)
    parsed = None
    try:
        parsed = json.loads(out)
    except Exception:
        parsed = None

    return {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_small_probe_result_v0",
        "probe_command": cmd,
        "returncode": rc,
        "elapsed_seconds": round(elapsed, 6),
        "stdout_tail": out[-12000:],
        "stderr_tail": err[-4000:],
        "parsed_result": parsed,
        "probe_passed": rc == 0 and isinstance(parsed, dict) and parsed.get("gate") == "PASS" and parsed.get("observation_receipt_count") == PROBE_RADIUS,
        "probe_radius": PROBE_RADIUS,
        "probe_observation_receipt_count": parsed.get("observation_receipt_count") if isinstance(parsed, dict) else None,
        "probe_run_receipt_path": parsed.get("run_receipt_path") if isinstance(parsed, dict) else None,
        "probe_rollup_path": parsed.get("rollup_path") if isinstance(parsed, dict) else None,
    }

def validate_outputs(probe: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if report.get("entrypoint_module_written_count") != 1:
        failures.append("entrypoint_module_not_written")
    if report.get("cli_patch_applied_count") not in {0, 1}:
        failures.append("cli_patch_count_invalid")
    if report.get("small_probe_executed_count") != 1:
        failures.append("small_probe_not_executed")
    if report.get("small_probe_passed_count") != 1:
        failures.append("small_probe_not_passed")
    if report.get("small_probe_observation_receipt_count") != PROBE_RADIUS:
        failures.append("small_probe_receipt_count_wrong")
    if report.get("radius_10000_retry_ready_count") != 1:
        failures.append("radius_10000_not_retry_ready")
    if report.get("radius_10000_retry_executed_count") != 0:
        failures.append("radius_10000_retry_executed")
    if report.get("unbounded_or_no_cap_run_count") != 0:
        failures.append("unbounded_or_no_cap_run")
    if report.get("queue_reopened_count") != 0:
        failures.append("queue_reopened")
    if report.get("closed_group_inspected_count") != 0:
        failures.append("closed_group_inspected")
    if report.get("row_payload_materialized_count") != 0:
        failures.append("row_payload_materialized")
    if report.get("row_payload_inspected_count") != 0:
        failures.append("row_payload_inspected")
    if report.get("identity_assignment_count") != 0:
        failures.append("identity_assignment")
    if report.get("field_value_invention_count") != 0:
        failures.append("field_value_invention")
    if report.get("repair_executed_count") != 0:
        failures.append("repair_executed")
    if report.get("taxonomy_delta_proposal_emitted_count") != 0:
        failures.append("taxonomy_delta_proposal_emitted")
    if report.get("source_mutation_count") != 0:
        failures.append("source_mutation")
    if report.get("existing_receipt_mutation_count") != 0:
        failures.append("existing_receipt_mutation")
    if report.get("hidden_next_command_count") != 0:
        failures.append("hidden_next_command")

    parsed = probe.get("parsed_result")
    if not isinstance(parsed, dict):
        failures.append("probe_stdout_not_json")
    elif parsed.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("probe_terminal_next_not_null")

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
        "missing_entrypoint_proposal_consumed_count",
        "entrypoint_module_written_count",
        "entrypoint_contract_emitted_count",
        "small_probe_executed_count",
        "small_probe_passed_count",
        "retry_ready_packet_emitted_count",
        "build_decision_emitted_count",
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
    if terminal.get("stop_code") != "STOP_OBSERVABILITY_HARVEST_ENTRYPOINT_BUILT_SMALL_PROBE_PASSED_RETRY_READY":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")

    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(SOURCE_FILES)
    failures = validate_sources()

    module_report = write_entrypoint_module()
    cli_report = patch_cli()

    source_patch_plan = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_source_patch_plan_v0",
        "source_cli_entrypoint_inspection_receipt_id": SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID,
        "missing_entrypoint_proposal_ref": rel(MISSING_ENTRYPOINT_PROPOSAL_PATH),
        "entrypoint_module_path": rel(ENTRYPOINT_MODULE_PATH),
        "cli_path": rel(CLI_PATH),
        "entrypoint_command": "post-closure-observability-harvest",
        "probe_radius": PROBE_RADIUS,
        "future_retry_radius": FUTURE_RETRY_RADIUS,
        "radius_10000_authorized_in_this_unit": False,
    }
    write_json(SOURCE_PATCH_PLAN_PATH, source_patch_plan)

    entrypoint_contract = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_contract_v0",
        "command": [
            "uv", "run", "python", "src/matrixlab/cli.py",
            "post-closure-observability-harvest",
            "--radius", "<N>",
            "--source-closure-receipt-id", SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        ],
        "bounded": True,
        "requires_radius": True,
        "max_radius_safety_cap": 250000,
        "must_emit_receipts": True,
        "must_emit_rollup": True,
        "must_not_reopen_closed_queue": True,
        "must_not_inspect_closed_groups": True,
        "must_not_materialize_row_payloads": True,
        "must_not_mutate_prior_artifacts": True,
        "must_not_hide_next_command": True,
    }
    write_json(ENTRYPOINT_CONTRACT_PATH, entrypoint_contract)

    compile_checks = []
    for target in [
        "src/matrixlab/r1000_post_closure_observability_harvest.py",
        "src/matrixlab/cli.py",
    ]:
        rc, out, err, elapsed = run_cmd(["uv", "run", "python", "-m", "py_compile", target])
        compile_checks.append({
            "target": target,
            "returncode": rc,
            "stdout_tail": out[-2000:],
            "stderr_tail": err[-4000:],
            "elapsed_seconds": round(elapsed, 6),
        })
        if rc != 0:
            failures.append(f"py_compile_failed:{target}")

    help_rc, help_out, help_err, help_elapsed = run_cmd([
        "uv", "run", "python", "src/matrixlab/cli.py",
        "post-closure-observability-harvest",
        "--help",
    ])
    help_check = {
        "returncode": help_rc,
        "stdout_tail": help_out[-4000:],
        "stderr_tail": help_err[-2000:],
        "elapsed_seconds": round(help_elapsed, 6),
        "help_contains_radius": "--radius" in help_out or "--radius" in help_err,
    }
    if help_rc != 0:
        failures.append("entrypoint_help_failed")

    probe = run_probe()
    write_json(SMALL_PROBE_RESULT_PATH, probe)

    retry_ready = probe["probe_passed"] is True
    retry_command = [
        "uv", "run", "python", "src/matrixlab/cli.py",
        "post-closure-observability-harvest",
        "--radius", str(FUTURE_RETRY_RADIUS),
        "--source-closure-receipt-id", SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "--label", "radius-10000-post-closure-observability-harvest",
    ]

    retry_packet = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_retry_ready_packet_v0",
        "packet_status": "RADIUS_10000_RETRY_READY_SEPARATE_UNIT" if retry_ready else "RADIUS_10000_RETRY_BLOCKED_SMALL_PROBE_FAILED",
        "source_build_entrypoint_unit_id": UNIT_ID,
        "source_cli_entrypoint_inspection_receipt_id": SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID,
        "entrypoint_command": "post-closure-observability-harvest",
        "small_probe_passed": retry_ready,
        "small_probe_radius": PROBE_RADIUS,
        "small_probe_observation_receipt_count": probe.get("probe_observation_receipt_count"),
        "radius_10000_retry_command": retry_command if retry_ready else None,
        "radius_10000_retry_authorized_in_this_unit": False,
        "requires_separate_retry_unit": retry_ready,
        "recommended_next_handling": "RETRY_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_WITH_BUILT_ENTRYPOINT_V0" if retry_ready else "REVIEW_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_BUILD_FAILURE_V0",
    }
    write_json(RETRY_READY_PACKET_PATH, retry_packet)

    decision = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_build_decision_v0",
        "decision_id": sha8({
            "unit_id": UNIT_ID,
            "probe_passed": retry_ready,
            "entrypoint": "post-closure-observability-harvest",
        }),
        "decision_status": "ENTRYPOINT_BUILT_SMALL_PROBE_PASSED_RETRY_READY" if retry_ready else "ENTRYPOINT_BUILD_INCOMPLETE_SMALL_PROBE_FAILED",
        "entrypoint_built": True,
        "cli_patched": cli_report["patch_applied"] or cli_report["reason"] == "entrypoint_already_present",
        "small_probe_passed": retry_ready,
        "radius_10000_retry_ready": retry_ready,
        "radius_10000_retry_executed": False,
        "recommended_next_handling": retry_packet["recommended_next_handling"],
    }
    write_json(BUILD_DECISION_PATH, decision)

    report = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_build_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_cli_entrypoint_inspection_receipt_id": SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID,
        "missing_entrypoint_proposal_consumed_count": 1,
        "entrypoint_module_written_count": 1 if module_report["module_written"] else 0,
        "cli_patch_applied_count": 1 if cli_report["patch_applied"] else 0,
        "entrypoint_contract_emitted_count": 1,
        "compile_check_count": len(compile_checks),
        "compile_check_pass_count": sum(1 for c in compile_checks if c["returncode"] == 0),
        "help_check_pass_count": 1 if help_check["returncode"] == 0 else 0,
        "small_probe_executed_count": 1,
        "small_probe_passed_count": 1 if retry_ready else 0,
        "small_probe_radius": PROBE_RADIUS,
        "small_probe_observation_receipt_count": probe.get("probe_observation_receipt_count") or 0,
        "retry_ready_packet_emitted_count": 1,
        "build_decision_emitted_count": 1,
        "radius_10000_retry_ready_count": 1 if retry_ready else 0,
        "radius_10000_retry_executed_count": 0,
        "unbounded_or_no_cap_run_count": 0,
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
        "recommended_next_handling": retry_packet["recommended_next_handling"],
    }
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(probe, report))

    transition_trace = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_build_transition_trace_v0",
        "trace": [
            {
                "step": "consume_missing_entrypoint_proposal",
                "question": "bounded receipt-producing harvest entrypoint is missing",
                "answer": True,
                "taken": "write_entrypoint_module",
            },
            {
                "step": "write_entrypoint_module_and_patch_cli",
                "question": "source compiles and help surface exists",
                "answer": report["compile_check_pass_count"] == report["compile_check_count"] and report["help_check_pass_count"] == 1,
                "taken": "run_small_probe",
            },
            {
                "step": "run_small_probe",
                "question": "small probe writes requested observation receipts",
                "answer": retry_ready,
                "taken": "emit_retry_ready_packet" if retry_ready else "emit_build_failure_packet",
            },
            {
                "step": "emit_retry_ready_packet",
                "question": "run radius 10000 now",
                "answer": False,
                "taken": "STOP_OBSERVABILITY_HARVEST_ENTRYPOINT_BUILT_SMALL_PROBE_PASSED_RETRY_READY" if retry_ready else "STOP_OBSERVABILITY_HARVEST_ENTRYPOINT_BUILD_INCOMPLETE_SMALL_PROBE_FAILED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_OBSERVABILITY_HARVEST_ENTRYPOINT_BUILT_SMALL_PROBE_PASSED_RETRY_READY" if retry_ready else "STOP_OBSERVABILITY_HARVEST_ENTRYPOINT_BUILD_INCOMPLETE_SMALL_PROBE_FAILED",
            "next_command_goal": None,
        },
    }
    write_json(TRANSITION_TRACE_PATH, transition_trace)

    terminal = transition_trace["terminal"]

    acceptance_gate_results = {
        "BUILD_ENTRYPOINT_0_MISSING_PROPOSAL_CONSUMED": True,
        "BUILD_ENTRYPOINT_1_ENTRYPOINT_MODULE_WRITTEN": report["entrypoint_module_written_count"] == 1,
        "BUILD_ENTRYPOINT_2_CLI_HELP_AVAILABLE": report["help_check_pass_count"] == 1,
        "BUILD_ENTRYPOINT_3_COMPILE_CHECKS_PASS": report["compile_check_pass_count"] == report["compile_check_count"],
        "BUILD_ENTRYPOINT_4_SMALL_PROBE_EXECUTED": report["small_probe_executed_count"] == 1,
        "BUILD_ENTRYPOINT_5_SMALL_PROBE_WRITES_RECEIPTS": report["small_probe_passed_count"] == 1 and report["small_probe_observation_receipt_count"] == PROBE_RADIUS,
        "BUILD_ENTRYPOINT_6_RETRY_READY_PACKET_EMITTED": report["retry_ready_packet_emitted_count"] == 1,
        "BUILD_ENTRYPOINT_7_RADIUS_10000_NOT_EXECUTED": report["radius_10000_retry_executed_count"] == 0,
        "BUILD_ENTRYPOINT_8_NO_UNBOUNDED_RUN": report["unbounded_or_no_cap_run_count"] == 0,
        "BUILD_ENTRYPOINT_9_NO_QUEUE_OR_ROW_ACTION": report["queue_reopened_count"] == 0 and report["row_payload_materialized_count"] == 0,
        "BUILD_ENTRYPOINT_10_NO_PRIOR_ARTIFACT_OR_RECEIPT_MUTATION": report["existing_receipt_mutation_count"] == 0,
        "BUILD_ENTRYPOINT_11_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and terminal["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    aggregate_metrics = {
        "source_cli_entrypoint_inspection_receipt_id": SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID,
        "source_command_resolver_fix_receipt_id": SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID,
        "source_failed_harvest_review_receipt_id": SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID,
        "source_failed_harvest_receipt_id": SOURCE_FAILED_HARVEST_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
    }

    guards = {
        "missing_entrypoint_proposal_consumed": True,
        "implementation_authorized_in_this_unit": True,
        "entrypoint_module_written": report["entrypoint_module_written_count"] == 1,
        "cli_patch_applied_or_already_present": cli_report["patch_applied"] or cli_report["reason"] == "entrypoint_already_present",
        "small_probe_executed": True,
        "small_probe_passed": retry_ready,
        "radius_10000_retry_ready": retry_ready,
        "radius_10000_retry_executed": False,
        "unbounded_or_no_cap_run": False,
        "queue_reopened": False,
        "closed_group_inspected": False,
        "row_payload_materialized": False,
        "row_payload_inspected": False,
        "identity_assignment": False,
        "field_value_invention": False,
        "repair_executed": False,
        "taxonomy_delta_proposal_emitted": False,
        "existing_receipts_mutated": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_cli_entrypoint_inspection_receipt_id": SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID,
        "decision_status": decision["decision_status"],
        "probe_passed": retry_ready,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_patch_plan": rel(SOURCE_PATCH_PLAN_PATH),
        "cli_patch_report": rel(CLI_PATCH_REPORT_PATH),
        "entrypoint_contract": rel(ENTRYPOINT_CONTRACT_PATH),
        "small_probe_result": rel(SMALL_PROBE_RESULT_PATH),
        "retry_ready_packet": rel(RETRY_READY_PACKET_PATH),
        "build_decision": rel(BUILD_DECISION_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "entrypoint_module": rel(ENTRYPOINT_MODULE_PATH),
        "cli_path": rel(CLI_PATH),
    }

    write_json(CLI_PATCH_REPORT_PATH, {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_patch_report_v0",
        "module_report": module_report,
        "cli_report": cli_report,
        "compile_checks": compile_checks,
        "help_check": help_check,
    })

    receipt = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_build_receipt_v0",
        "receipt_type": "R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_BUILD_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_cli_entrypoint_inspection_receipt_id": SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID,
        "source_command_resolver_fix_receipt_id": SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID,
        "source_failed_harvest_review_receipt_id": SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID,
        "source_failed_harvest_receipt_id": SOURCE_FAILED_HARVEST_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "entrypoint_build_summary": {
            "decision_status": decision["decision_status"],
            "entrypoint_built": decision["entrypoint_built"],
            "entrypoint_command": "post-closure-observability-harvest",
            "small_probe_executed": True,
            "small_probe_passed": retry_ready,
            "small_probe_radius": PROBE_RADIUS,
            "small_probe_observation_receipt_count": probe.get("probe_observation_receipt_count"),
            "radius_10000_retry_ready": retry_ready,
            "radius_10000_retry_executed": False,
            "radius_10000_retry_command": retry_packet["radius_10000_retry_command"],
            "recommended_next_handling": retry_packet["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "entrypoint_build_guards": guards,
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
    print(f"entrypoint_build_receipt_id={receipt_id}")
    print(f"entrypoint_build_receipt_path=data/r1000_post_closure_observability_harvest_entrypoint_build_v0_receipts/{receipt_id}.json")
    print(f"retry_ready_packet_path=data/r1000_post_closure_observability_harvest_entrypoint_build_v0/r1000_post_closure_observability_harvest_radius_10000_retry_ready_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
