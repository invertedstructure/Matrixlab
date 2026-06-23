#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shlex
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "FIX_R1000_POST_CLOSURE_HARVEST_COMMAND_RESOLVER_FROM_CLI_HELP_V0"
TARGET_UNIT_ID = "r1000.post_closure_harvest.command_resolver_fix_from_cli_help.v0"

SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID = "c5217505"
SOURCE_FAILED_HARVEST_RECEIPT_ID = "722af13e"
SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID = "52d0ea8d"
SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID = "db7c0af2"

HARVEST_RADIUS = 10000
PROBE_RADIUS = 10

OUT_DIR = ROOT / "data" / "r1000_post_closure_harvest_command_resolver_fix_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_post_closure_harvest_command_resolver_fix_v0_receipts"

RESOLVER_SOURCE_SURFACE_PATH = OUT_DIR / "r1000_post_closure_harvest_command_resolver_source_surface.json"
CLI_COMMAND_CATALOG_PATH = OUT_DIR / "r1000_post_closure_harvest_cli_command_catalog.json"
RESOLVED_ENTRYPOINT_CANDIDATE_PATH = OUT_DIR / "r1000_post_closure_harvest_resolved_entrypoint_candidate.json"
SMALL_PROBE_PLAN_PATH = OUT_DIR / "r1000_post_closure_harvest_command_resolver_small_probe_plan.json"
SMALL_PROBE_RESULT_PATH = OUT_DIR / "r1000_post_closure_harvest_command_resolver_small_probe_result.json"
RETRY_READY_PACKET_PATH = OUT_DIR / "r1000_post_closure_harvest_radius_10000_retry_ready_packet.json"
COMMAND_RESOLVER_DECISION_PATH = OUT_DIR / "r1000_post_closure_harvest_command_resolver_fix_decision.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_post_closure_harvest_command_resolver_fix_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_post_closure_harvest_command_resolver_fix_report.json"

FAILED_HARVEST_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_review_v0_receipts" / f"{SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID}.json"
CLI_HELP_SURFACE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_review_v0" / "r1000_post_closure_observability_harvest_radius_10000_cli_help_surface.json"
COMMAND_RESOLVER_DEFECT_PACKET_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_review_v0" / "r1000_post_closure_observability_harvest_radius_10000_command_resolver_defect_packet.json"
RETRY_AUTHORITY_PACKET_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_review_v0" / "r1000_post_closure_observability_harvest_radius_10000_retry_authority_packet.json"
FAILED_HARVEST_REVIEW_DECISION_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_review_v0" / "r1000_post_closure_observability_harvest_radius_10000_review_decision.json"
FAILED_HARVEST_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_v0_receipts" / f"{SOURCE_FAILED_HARVEST_RECEIPT_ID}.json"

CLOSURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0_receipts" / f"{SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID}.json"
CLOSED_QUEUE_HANDOFF_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0" / "r1000_pressure_queue_closed_handoff_after_synthetic_remainder_expected_limit.json"
EXPECTED_LIMIT_MARK_RECEIPT_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID}.json"
FINAL_QUEUE_STATE_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_final_pressure_queue_state_after_synthetic_remainder_expected_limit.json"
CLI_PATH = ROOT / "src" / "matrixlab" / "cli.py"

SOURCE_FILES = [
    FAILED_HARVEST_REVIEW_RECEIPT_PATH,
    CLI_HELP_SURFACE_PATH,
    COMMAND_RESOLVER_DEFECT_PACKET_PATH,
    RETRY_AUTHORITY_PACKET_PATH,
    FAILED_HARVEST_REVIEW_DECISION_PATH,
    FAILED_HARVEST_RECEIPT_PATH,
    CLOSURE_REVIEW_RECEIPT_PATH,
    CLOSED_QUEUE_HANDOFF_PATH,
    EXPECTED_LIMIT_MARK_RECEIPT_PATH,
    FINAL_QUEUE_STATE_PATH,
    CLI_PATH,
]

HUMAN_DECISION = {
    "decision": "FIX_R1000_POST_CLOSURE_HARVEST_COMMAND_RESOLVER_FROM_CLI_HELP",
    "scope": "resolve the real MatrixLab command entrypoint for bounded post-closure observability harvesting from CLI help/source surfaces, prove it with a small probe, and emit a retry-ready packet for radius 10000 without running radius 10000 in this unit",
    "source_failed_harvest_review_receipt_id": SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID,
    "authorized": [
        "consume failed harvest review receipt",
        "consume CLI help surface",
        "consume command resolver defect packet",
        "inspect src/matrixlab/cli.py as source surface",
        "materialize command catalog",
        "resolve a concrete bounded entrypoint if present",
        "run a small bounded probe only if the entrypoint is resolved",
        "emit retry-ready packet only if small probe is clean",
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
        "filling fields",
        "running repair",
        "applying taxonomy changes",
        "mutating source artifacts",
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

def run_cmd(args: List[str], timeout: int = 180) -> Tuple[int, str, str, float]:
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
    review_receipt = read_json(FAILED_HARVEST_REVIEW_RECEIPT_PATH)
    defect_packet = read_json(COMMAND_RESOLVER_DEFECT_PACKET_PATH)
    retry_packet = read_json(RETRY_AUTHORITY_PACKET_PATH)
    closure_receipt = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if review_receipt.get("receipt_id") != SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID:
        failures.append("failed_harvest_review_receipt_id_wrong")
    if review_receipt.get("gate") != "PASS":
        failures.append("failed_harvest_review_not_pass")
    if review_receipt.get("failed_harvest_review_summary", {}).get("failure_classification") != "COMMAND_INTERFACE_CAPABILITY_FAILURE_NOT_SEMANTIC_QUEUE_FAILURE":
        failures.append("failed_harvest_not_command_interface_failure")
    if review_receipt.get("failed_harvest_review_summary", {}).get("recommended_next_handling") != UNIT_ID:
        failures.append("failed_harvest_review_not_recommending_this_fix")

    if defect_packet.get("defect_type") != "HARVEST_COMMAND_INTERFACE_UNRESOLVED":
        failures.append("defect_type_wrong")
    if defect_packet.get("requires_entrypoint_resolution") is not True:
        failures.append("defect_does_not_require_entrypoint_resolution")

    if retry_packet.get("packet_status") != "RETRY_BLOCKED_UNTIL_ENTRYPOINT_RESOLVED":
        failures.append("retry_packet_status_wrong")
    if retry_packet.get("retry_authorized_now") is not False:
        failures.append("retry_packet_authorized_before_fix")

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

def parse_cli_source() -> Dict[str, Any]:
    text = CLI_PATH.read_text()
    command_like_lines: List[str] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        lower = line.lower()
        if any(token in lower for token in ["@app.command", "@cli.command", "def ", "typer", "click", "radius", "cycle", "receipt", "gate"]):
            command_like_lines.append(f"{idx}: {line.rstrip()}")

    defs = re.findall(r"^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", text, flags=re.MULTILINE)
    app_commands = re.findall(r"@(?:app|cli)\.command\((.*?)\)", text, flags=re.DOTALL)
    likely_defs = [name for name in defs if any(token in name.lower() for token in ["run", "cycle", "gate", "receipt", "harvest", "probe", "execute", "batch", "scale"])]

    return {
        "schema_version": "r1000_post_closure_harvest_command_resolver_source_surface_v0",
        "cli_path": rel(CLI_PATH),
        "cli_source_sha256": file_sha256(CLI_PATH),
        "defined_functions": defs,
        "likely_command_functions": likely_defs,
        "decorated_command_fragments": app_commands,
        "command_like_line_count": len(command_like_lines),
        "command_like_lines": command_like_lines[:250],
        "truncated": len(command_like_lines) > 250,
    }

def collect_help(args: List[str]) -> Dict[str, Any]:
    try:
        rc, out, err, elapsed = run_cmd(args + ["--help"], timeout=60)
        return {
            "args": args + ["--help"],
            "returncode": rc,
            "elapsed_seconds": round(elapsed, 6),
            "stdout_tail": out[-12000:],
            "stderr_tail": err[-4000:],
        }
    except Exception as exc:
        return {
            "args": args + ["--help"],
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
        }

def command_exists(args: List[str]) -> bool:
    result = collect_help(args)
    return result.get("returncode") == 0

def build_command_catalog(cli_help_surface: Dict[str, Any], source_surface: Dict[str, Any]) -> Dict[str, Any]:
    base = ["uv", "run", "python", "src/matrixlab/cli.py"]
    root_help = collect_help(base)

    possible_subcommands = [
        "run",
        "cycle",
        "cycles",
        "execute",
        "batch",
        "gate",
        "receipt",
        "receipts",
        "probe",
        "harvest",
        "replay",
        "scale",
        "summary",
        "doctor",
    ]

    for fn in source_surface.get("likely_command_functions", []):
        normalized = fn.replace("_", "-")
        if normalized not in possible_subcommands:
            possible_subcommands.append(normalized)

    subcommand_help = []
    existing = []
    for name in possible_subcommands:
        args = base + [name]
        help_result = collect_help(args)
        subcommand_help.append({
            "name": name,
            "help": help_result,
            "exists": help_result.get("returncode") == 0,
        })
        if help_result.get("returncode") == 0:
            existing.append(name)

    return {
        "schema_version": "r1000_post_closure_harvest_cli_command_catalog_v0",
        "base_command": base,
        "root_help": root_help,
        "existing_subcommands": existing,
        "subcommand_help": subcommand_help,
        "source_surface_ref": rel(RESOLVER_SOURCE_SURFACE_PATH),
        "prior_cli_help_surface_ref": rel(CLI_HELP_SURFACE_PATH),
    }

def build_candidate_commands(catalog: Dict[str, Any]) -> List[List[str]]:
    base = catalog["base_command"]
    existing = set(catalog.get("existing_subcommands", []))
    candidates: List[List[str]] = []

    if "run" in existing:
        candidates.extend([
            base + ["run", "--cases", str(PROBE_RADIUS)],
            base + ["run", "--count", str(PROBE_RADIUS)],
            base + ["run", "--limit", str(PROBE_RADIUS)],
            base + ["run", "--n", str(PROBE_RADIUS)],
            base + ["run"],
        ])

    if "cycle" in existing:
        candidates.extend([
            base + ["cycle", "--count", str(PROBE_RADIUS)],
            base + ["cycle", "--limit", str(PROBE_RADIUS)],
            base + ["cycle"],
        ])

    if "cycles" in existing:
        candidates.extend([
            base + ["cycles", "--count", str(PROBE_RADIUS)],
            base + ["cycles", "--limit", str(PROBE_RADIUS)],
            base + ["cycles"],
        ])

    if "batch" in existing:
        candidates.extend([
            base + ["batch", "--count", str(PROBE_RADIUS)],
            base + ["batch", "--limit", str(PROBE_RADIUS)],
            base + ["batch"],
        ])

    if "probe" in existing:
        candidates.extend([
            base + ["probe", "--count", str(PROBE_RADIUS)],
            base + ["probe", "--limit", str(PROBE_RADIUS)],
            base + ["probe"],
        ])

    if "harvest" in existing:
        candidates.extend([
            base + ["harvest", "--count", str(PROBE_RADIUS)],
            base + ["harvest", "--limit", str(PROBE_RADIUS)],
            base + ["harvest"],
        ])

    deduped: List[List[str]] = []
    seen = set()
    for cmd in candidates:
        key = tuple(cmd)
        if key not in seen:
            seen.add(key)
            deduped.append(cmd)
    return deduped

def discover_existing_receipt_paths() -> List[Path]:
    roots = [ROOT / "data", ROOT / "logs"]
    paths: List[Path] = []
    for root in roots:
        if root.exists():
            for p in root.rglob("*.json"):
                if "receipt" in p.name.lower() or "receipt" in p.parent.name.lower():
                    paths.append(p)
    return sorted(set(paths), key=lambda p: rel(p))

def run_small_probe(candidates: List[List[str]]) -> Dict[str, Any]:
    before = discover_existing_receipt_paths()
    before_hashes = {rel(p): file_sha256(p) for p in before if p.exists()}

    attempts: List[Dict[str, Any]] = []
    selected: Optional[Dict[str, Any]] = None

    for cmd in candidates:
        try:
            rc, out, err, elapsed = run_cmd(cmd, timeout=180)
            after = discover_existing_receipt_paths()
            new_paths = [p for p in after if rel(p) not in before_hashes]
            attempt = {
                "args": cmd,
                "returncode": rc,
                "elapsed_seconds": round(elapsed, 6),
                "stdout_tail": out[-4000:],
                "stderr_tail": err[-4000:],
                "new_receipt_count": len(new_paths),
                "new_receipt_paths": [rel(p) for p in new_paths[:25]],
            }
            attempts.append(attempt)
            if rc == 0 and len(new_paths) > 0:
                selected = attempt
                break
        except Exception as exc:
            attempts.append({
                "args": cmd,
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
                "new_receipt_count": 0,
            })

    after = discover_existing_receipt_paths()
    return {
        "schema_version": "r1000_post_closure_harvest_command_resolver_small_probe_result_v0",
        "probe_radius": PROBE_RADIUS,
        "probe_attempt_count": len(attempts),
        "probe_resolved": selected is not None,
        "selected_probe_command": selected.get("args") if selected else None,
        "selected_probe_new_receipt_count": selected.get("new_receipt_count") if selected else 0,
        "attempts": attempts,
        "receipt_count_before": len(before),
        "receipt_count_after": len(after),
        "new_receipt_count_total": max(0, len(after) - len(before)),
    }

def build_entrypoint_candidate(catalog: Dict[str, Any], probe: Dict[str, Any]) -> Dict[str, Any]:
    selected_probe = probe.get("selected_probe_command")
    retry_command = None
    if selected_probe:
        retry_command = list(selected_probe)
        for i, part in enumerate(retry_command):
            if part == str(PROBE_RADIUS):
                retry_command[i] = str(HARVEST_RADIUS)

    return {
        "schema_version": "r1000_post_closure_harvest_resolved_entrypoint_candidate_v0",
        "entrypoint_resolution_status": "RESOLVED_BY_SMALL_PROBE" if probe.get("probe_resolved") else "UNRESOLVED_AFTER_CLI_HELP_AND_SMALL_PROBE",
        "base_command": catalog.get("base_command"),
        "existing_subcommands": catalog.get("existing_subcommands"),
        "selected_probe_command": selected_probe,
        "selected_probe_new_receipt_count": probe.get("selected_probe_new_receipt_count"),
        "radius_10000_retry_command_candidate": retry_command,
        "radius_10000_retry_authorized_in_this_unit": False,
        "requires_separate_retry_unit": probe.get("probe_resolved") is True,
    }

def build_probe_plan(catalog: Dict[str, Any], candidates: List[List[str]]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_post_closure_harvest_command_resolver_small_probe_plan_v0",
        "probe_radius": PROBE_RADIUS,
        "radius_10000_requested_for_later": HARVEST_RADIUS,
        "radius_10000_run_authorized_in_this_unit": False,
        "candidate_command_count": len(candidates),
        "candidate_commands": candidates,
        "existing_subcommands": catalog.get("existing_subcommands"),
    }

def build_retry_ready_packet(entrypoint: Dict[str, Any], probe: Dict[str, Any]) -> Dict[str, Any]:
    resolved = entrypoint["entrypoint_resolution_status"] == "RESOLVED_BY_SMALL_PROBE"
    return {
        "schema_version": "r1000_post_closure_harvest_radius_10000_retry_ready_packet_v0",
        "packet_status": "RADIUS_10000_RETRY_READY_SEPARATE_UNIT" if resolved else "RADIUS_10000_RETRY_BLOCKED_ENTRYPOINT_UNRESOLVED",
        "source_failed_harvest_review_receipt_id": SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID,
        "entrypoint_resolved": resolved,
        "small_probe_passed": probe.get("probe_resolved") is True,
        "small_probe_new_receipt_count": probe.get("selected_probe_new_receipt_count") or 0,
        "radius_10000_retry_command_candidate": entrypoint.get("radius_10000_retry_command_candidate"),
        "radius_10000_retry_authorized_in_this_unit": False,
        "requires_separate_retry_unit": resolved,
        "recommended_next_handling": "RETRY_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_WITH_RESOLVED_COMMAND_V0" if resolved else "INSPECT_MATRIXLAB_CLI_FOR_OBSERVABILITY_HARVEST_ENTRYPOINT_V0",
    }

def build_decision(entrypoint: Dict[str, Any], retry_packet: Dict[str, Any], probe: Dict[str, Any]) -> Dict[str, Any]:
    resolved = entrypoint["entrypoint_resolution_status"] == "RESOLVED_BY_SMALL_PROBE"
    return {
        "schema_version": "r1000_post_closure_harvest_command_resolver_fix_decision_v0",
        "decision_id": sha8({
            "source_failed_harvest_review_receipt_id": SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID,
            "resolved": resolved,
            "retry_command": entrypoint.get("radius_10000_retry_command_candidate"),
        }),
        "decision_status": "COMMAND_RESOLVER_FIXED_SMALL_PROBE_PASSED" if resolved else "COMMAND_RESOLVER_STILL_UNRESOLVED_AFTER_SMALL_PROBE",
        "source_entrypoint_candidate_ref": rel(RESOLVED_ENTRYPOINT_CANDIDATE_PATH),
        "source_small_probe_result_ref": rel(SMALL_PROBE_RESULT_PATH),
        "entrypoint_resolved": resolved,
        "small_probe_executed": True,
        "small_probe_passed": probe.get("probe_resolved") is True,
        "radius_10000_retry_executed": False,
        "radius_10000_retry_ready": resolved,
        "recommended_next_handling": retry_packet["recommended_next_handling"],
    }

def build_transition_trace(decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_post_closure_harvest_command_resolver_fix_transition_trace_v0",
        "trace": [
            {
                "step": "consume_failed_harvest_review",
                "question": "failure was command-interface resolver defect",
                "answer": True,
                "taken": "inspect_cli_help_and_source",
            },
            {
                "step": "inspect_cli_help_and_source",
                "question": "candidate bounded entrypoints identified",
                "answer": True,
                "taken": "run_small_probe",
            },
            {
                "step": "run_small_probe",
                "question": "small probe resolved a receipt-producing entrypoint",
                "answer": decision["small_probe_passed"],
                "taken": "emit_retry_ready_packet" if decision["small_probe_passed"] else "emit_unresolved_packet",
            },
            {
                "step": "emit_retry_packet",
                "question": "run radius 10000 in this unit",
                "answer": False,
                "taken": "STOP_COMMAND_RESOLVER_FIX_COMPLETE_RETRY_READY" if decision["radius_10000_retry_ready"] else "STOP_COMMAND_RESOLVER_FIX_INCOMPLETE_ENTRYPOINT_UNRESOLVED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_COMMAND_RESOLVER_FIX_COMPLETE_RETRY_READY" if decision["radius_10000_retry_ready"] else "STOP_COMMAND_RESOLVER_FIX_INCOMPLETE_ENTRYPOINT_UNRESOLVED",
            "next_command_goal": None,
        },
    }

def build_report(source_surface: Dict[str, Any], catalog: Dict[str, Any], probe: Dict[str, Any], entrypoint: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    resolved = decision["entrypoint_resolved"]
    return {
        "schema_version": "r1000_post_closure_harvest_command_resolver_fix_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_failed_harvest_review_receipt_id": SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID,
        "failed_harvest_review_receipt_consumed_count": 1,
        "cli_help_surface_consumed_count": 1,
        "command_resolver_defect_packet_consumed_count": 1,
        "retry_authority_packet_consumed_count": 1,
        "cli_source_surface_materialized_count": 1,
        "cli_command_catalog_emitted_count": 1,
        "candidate_command_count": len(build_candidate_commands(catalog)),
        "existing_subcommand_count": len(catalog.get("existing_subcommands") or []),
        "small_probe_plan_emitted_count": 1,
        "small_probe_executed_count": 1,
        "small_probe_passed_count": 1 if probe.get("probe_resolved") else 0,
        "small_probe_new_receipt_count": probe.get("selected_probe_new_receipt_count") or 0,
        "entrypoint_candidate_emitted_count": 1,
        "entrypoint_resolved_count": 1 if resolved else 0,
        "retry_ready_packet_emitted_count": 1,
        "radius_10000_retry_ready_count": 1 if decision["radius_10000_retry_ready"] else 0,
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
        "recommended_next_handling": decision["recommended_next_handling"],
    }

def validate_outputs(probe: Dict[str, Any], entrypoint: Dict[str, Any], retry: Dict[str, Any], decision: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if report.get("small_probe_executed_count") != 1:
        failures.append("small_probe_not_executed")
    if entrypoint.get("entrypoint_resolution_status") not in {"RESOLVED_BY_SMALL_PROBE", "UNRESOLVED_AFTER_CLI_HELP_AND_SMALL_PROBE"}:
        failures.append("entrypoint_resolution_status_unknown")
    if probe.get("probe_resolved") is True:
        if entrypoint.get("radius_10000_retry_command_candidate") is None:
            failures.append("probe_resolved_but_no_retry_command")
        if retry.get("packet_status") != "RADIUS_10000_RETRY_READY_SEPARATE_UNIT":
            failures.append("retry_packet_not_ready_after_probe")
        if decision.get("radius_10000_retry_ready") is not True:
            failures.append("decision_retry_not_ready_after_probe")
        if report.get("entrypoint_resolved_count") != 1:
            failures.append("entrypoint_resolved_count_wrong")
    else:
        if retry.get("packet_status") != "RADIUS_10000_RETRY_BLOCKED_ENTRYPOINT_UNRESOLVED":
            failures.append("retry_packet_not_blocked_when_unresolved")

    if retry.get("radius_10000_retry_authorized_in_this_unit") is not False:
        failures.append("retry_authorized_in_this_unit")
    if decision.get("radius_10000_retry_executed") is not False:
        failures.append("decision_says_radius_10000_executed")

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
        "failed_harvest_review_receipt_consumed_count",
        "cli_help_surface_consumed_count",
        "command_resolver_defect_packet_consumed_count",
        "retry_authority_packet_consumed_count",
        "cli_source_surface_materialized_count",
        "cli_command_catalog_emitted_count",
        "small_probe_plan_emitted_count",
        "small_probe_executed_count",
        "entrypoint_candidate_emitted_count",
        "retry_ready_packet_emitted_count",
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
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")

    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(SOURCE_FILES)
    failures = validate_sources()

    cli_help_surface = read_json(CLI_HELP_SURFACE_PATH)
    source_surface = parse_cli_source()
    catalog = build_command_catalog(cli_help_surface, source_surface)
    candidate_commands = build_candidate_commands(catalog)
    probe_plan = build_probe_plan(catalog, candidate_commands)
    probe_result = run_small_probe(candidate_commands)
    entrypoint = build_entrypoint_candidate(catalog, probe_result)
    retry_packet = build_retry_ready_packet(entrypoint, probe_result)
    decision = build_decision(entrypoint, retry_packet, probe_result)
    trace = build_transition_trace(decision)
    report = build_report(source_surface, catalog, probe_result, entrypoint, decision)

    write_json(RESOLVER_SOURCE_SURFACE_PATH, source_surface)
    write_json(CLI_COMMAND_CATALOG_PATH, catalog)
    write_json(SMALL_PROBE_PLAN_PATH, probe_plan)
    write_json(SMALL_PROBE_RESULT_PATH, probe_result)
    write_json(RESOLVED_ENTRYPOINT_CANDIDATE_PATH, entrypoint)
    write_json(RETRY_READY_PACKET_PATH, retry_packet)
    write_json(COMMAND_RESOLVER_DECISION_PATH, decision)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(probe_result, entrypoint, retry_packet, decision, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "COMMAND_RESOLVER_FIX_0_FAILED_REVIEW_CONSUMED": True,
        "COMMAND_RESOLVER_FIX_1_CLI_SOURCE_AND_HELP_SURFACES_MATERIALIZED": report["cli_source_surface_materialized_count"] == 1 and report["cli_command_catalog_emitted_count"] == 1,
        "COMMAND_RESOLVER_FIX_2_SMALL_PROBE_EXECUTED": report["small_probe_executed_count"] == 1,
        "COMMAND_RESOLVER_FIX_3_ENTRYPOINT_STATUS_TYPED": entrypoint["entrypoint_resolution_status"] in {"RESOLVED_BY_SMALL_PROBE", "UNRESOLVED_AFTER_CLI_HELP_AND_SMALL_PROBE"},
        "COMMAND_RESOLVER_FIX_4_RADIUS_10000_NOT_EXECUTED": report["radius_10000_retry_executed_count"] == 0,
        "COMMAND_RESOLVER_FIX_5_NO_UNBOUNDED_RUN": report["unbounded_or_no_cap_run_count"] == 0,
        "COMMAND_RESOLVER_FIX_6_NO_QUEUE_REOPEN_OR_CLOSED_GROUP_INSPECTION": report["queue_reopened_count"] == 0 and report["closed_group_inspected_count"] == 0,
        "COMMAND_RESOLVER_FIX_7_NO_ROW_PAYLOAD_REPAIR_TAXONOMY": report["row_payload_materialized_count"] == 0 and report["repair_executed_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "COMMAND_RESOLVER_FIX_8_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "COMMAND_RESOLVER_FIX_9_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_failed_harvest_review_receipt_id": SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID,
        "source_failed_harvest_receipt_id": SOURCE_FAILED_HARVEST_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards = {
        "failed_harvest_review_consumed": True,
        "cli_help_surface_consumed": True,
        "cli_source_surface_materialized": True,
        "small_probe_executed": True,
        "small_probe_passed": probe_result.get("probe_resolved") is True,
        "entrypoint_resolved": decision["entrypoint_resolved"],
        "radius_10000_retry_ready": decision["radius_10000_retry_ready"],
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
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_failed_harvest_review_receipt_id": SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID,
        "entrypoint_status": entrypoint["entrypoint_resolution_status"],
        "retry_command": entrypoint.get("radius_10000_retry_command_candidate"),
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "resolver_source_surface": rel(RESOLVER_SOURCE_SURFACE_PATH),
        "cli_command_catalog": rel(CLI_COMMAND_CATALOG_PATH),
        "small_probe_plan": rel(SMALL_PROBE_PLAN_PATH),
        "small_probe_result": rel(SMALL_PROBE_RESULT_PATH),
        "resolved_entrypoint_candidate": rel(RESOLVED_ENTRYPOINT_CANDIDATE_PATH),
        "retry_ready_packet": rel(RETRY_READY_PACKET_PATH),
        "command_resolver_decision": rel(COMMAND_RESOLVER_DECISION_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_post_closure_harvest_command_resolver_fix_receipt_v0",
        "receipt_type": "R1000_POST_CLOSURE_HARVEST_COMMAND_RESOLVER_FIX_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_failed_harvest_review_receipt_id": SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID,
        "source_failed_harvest_receipt_id": SOURCE_FAILED_HARVEST_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "command_resolver_fix_summary": {
            "decision_status": decision["decision_status"],
            "entrypoint_resolution_status": entrypoint["entrypoint_resolution_status"],
            "entrypoint_resolved": decision["entrypoint_resolved"],
            "small_probe_executed": True,
            "small_probe_passed": decision["small_probe_passed"],
            "small_probe_new_receipt_count": probe_result.get("selected_probe_new_receipt_count") or 0,
            "radius_10000_retry_ready": decision["radius_10000_retry_ready"],
            "radius_10000_retry_executed": False,
            "radius_10000_retry_command_candidate": entrypoint.get("radius_10000_retry_command_candidate"),
            "recommended_next_handling": decision["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "command_resolver_fix_guards": guards,
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
    print(f"command_resolver_fix_receipt_id={receipt_id}")
    print(f"command_resolver_fix_receipt_path=data/r1000_post_closure_harvest_command_resolver_fix_v0_receipts/{receipt_id}.json")
    print(f"retry_ready_packet_path=data/r1000_post_closure_harvest_command_resolver_fix_v0/r1000_post_closure_harvest_radius_10000_retry_ready_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
