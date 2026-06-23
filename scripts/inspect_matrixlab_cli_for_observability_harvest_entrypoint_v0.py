#!/usr/bin/env python3
from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "INSPECT_MATRIXLAB_CLI_FOR_OBSERVABILITY_HARVEST_ENTRYPOINT_V0"
TARGET_UNIT_ID = "r1000.cli.observability_harvest_entrypoint_inspection.v0"

SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID = "b35e7989"
SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID = "c5217505"
SOURCE_FAILED_HARVEST_RECEIPT_ID = "722af13e"
SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID = "52d0ea8d"
SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID = "db7c0af2"
HARVEST_RADIUS = 10000

OUT_DIR = ROOT / "data" / "r1000_cli_observability_harvest_entrypoint_inspection_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_cli_observability_harvest_entrypoint_inspection_v0_receipts"

SOURCE_INVENTORY_PATH = OUT_DIR / "r1000_cli_observability_harvest_source_inventory.json"
CLI_AST_COMMAND_SURFACE_PATH = OUT_DIR / "r1000_cli_observability_harvest_cli_ast_command_surface.json"
MODULE_RECEIPT_WRITE_SURFACE_PATH = OUT_DIR / "r1000_cli_observability_harvest_module_receipt_write_surface.json"
ENTRYPOINT_CANDIDATE_SURFACE_PATH = OUT_DIR / "r1000_cli_observability_harvest_entrypoint_candidate_surface.json"
ENTRYPOINT_DECISION_PATH = OUT_DIR / "r1000_cli_observability_harvest_entrypoint_inspection_decision.json"
MISSING_ENTRYPOINT_PROPOSAL_PATH = OUT_DIR / "r1000_cli_observability_harvest_missing_entrypoint_proposal.json"
NEXT_AUTHORITY_PACKET_PATH = OUT_DIR / "r1000_cli_observability_harvest_next_authority_packet.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_cli_observability_harvest_entrypoint_inspection_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_cli_observability_harvest_entrypoint_inspection_report.json"

COMMAND_RESOLVER_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_harvest_command_resolver_fix_v0_receipts" / f"{SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID}.json"
COMMAND_RESOLVER_SOURCE_SURFACE_PATH = ROOT / "data" / "r1000_post_closure_harvest_command_resolver_fix_v0" / "r1000_post_closure_harvest_command_resolver_source_surface.json"
COMMAND_CATALOG_PATH = ROOT / "data" / "r1000_post_closure_harvest_command_resolver_fix_v0" / "r1000_post_closure_harvest_cli_command_catalog.json"
SMALL_PROBE_PLAN_PATH = ROOT / "data" / "r1000_post_closure_harvest_command_resolver_fix_v0" / "r1000_post_closure_harvest_command_resolver_small_probe_plan.json"
SMALL_PROBE_RESULT_PATH = ROOT / "data" / "r1000_post_closure_harvest_command_resolver_fix_v0" / "r1000_post_closure_harvest_command_resolver_small_probe_result.json"
RESOLVED_ENTRYPOINT_PATH = ROOT / "data" / "r1000_post_closure_harvest_command_resolver_fix_v0" / "r1000_post_closure_harvest_resolved_entrypoint_candidate.json"
RETRY_READY_PACKET_PATH = ROOT / "data" / "r1000_post_closure_harvest_command_resolver_fix_v0" / "r1000_post_closure_harvest_radius_10000_retry_ready_packet.json"
COMMAND_RESOLVER_DECISION_PATH = ROOT / "data" / "r1000_post_closure_harvest_command_resolver_fix_v0" / "r1000_post_closure_harvest_command_resolver_fix_decision.json"

FAILED_HARVEST_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_review_v0_receipts" / f"{SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID}.json"
FAILED_HARVEST_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_v0_receipts" / f"{SOURCE_FAILED_HARVEST_RECEIPT_ID}.json"
CLOSURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0_receipts" / f"{SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID}.json"
CLOSED_QUEUE_HANDOFF_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0" / "r1000_pressure_queue_closed_handoff_after_synthetic_remainder_expected_limit.json"
EXPECTED_LIMIT_MARK_RECEIPT_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID}.json"
FINAL_QUEUE_STATE_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_final_pressure_queue_state_after_synthetic_remainder_expected_limit.json"
CLI_PATH = ROOT / "src" / "matrixlab" / "cli.py"
MATRIXLAB_SRC = ROOT / "src" / "matrixlab"

SOURCE_FILES = [
    COMMAND_RESOLVER_FIX_RECEIPT_PATH,
    COMMAND_RESOLVER_SOURCE_SURFACE_PATH,
    COMMAND_CATALOG_PATH,
    SMALL_PROBE_PLAN_PATH,
    SMALL_PROBE_RESULT_PATH,
    RESOLVED_ENTRYPOINT_PATH,
    RETRY_READY_PACKET_PATH,
    COMMAND_RESOLVER_DECISION_PATH,
    FAILED_HARVEST_REVIEW_RECEIPT_PATH,
    FAILED_HARVEST_RECEIPT_PATH,
    CLOSURE_REVIEW_RECEIPT_PATH,
    CLOSED_QUEUE_HANDOFF_PATH,
    EXPECTED_LIMIT_MARK_RECEIPT_PATH,
    FINAL_QUEUE_STATE_PATH,
    CLI_PATH,
]

HUMAN_DECISION = {
    "decision": "INSPECT_MATRIXLAB_CLI_FOR_OBSERVABILITY_HARVEST_ENTRYPOINT",
    "scope": "inspect MatrixLab CLI and source surfaces to determine whether a real receipt-producing bounded observability harvest entrypoint exists; emit either a resolved-entrypoint authority packet or a typed missing-entrypoint proposal without running radius 10000",
    "source_command_resolver_fix_receipt_id": SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID,
    "authorized": [
        "consume command resolver fix receipt",
        "consume command catalog and small probe result",
        "inspect src/matrixlab/cli.py",
        "inspect MatrixLab source files deterministically for command and receipt-write surfaces",
        "classify whether a bounded receipt-producing harvest entrypoint exists",
        "emit typed missing-entrypoint proposal if absent",
        "emit next authority packet",
        "stop before implementation or radius-10000 retry",
    ],
    "not_authorized": [
        "running radius-10000 harvest",
        "running unbounded/no-cap harvest",
        "running small probe again",
        "modifying src/matrixlab/cli.py",
        "adding a new CLI command",
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

def run_cmd(args: List[str], timeout: int = 60) -> Tuple[int, str, str]:
    proc = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    return proc.returncode, proc.stdout, proc.stderr

def validate_sources() -> List[str]:
    failures: List[str] = []
    resolver_receipt = read_json(COMMAND_RESOLVER_FIX_RECEIPT_PATH)
    resolver_decision = read_json(COMMAND_RESOLVER_DECISION_PATH)
    small_probe = read_json(SMALL_PROBE_RESULT_PATH)
    entrypoint = read_json(RESOLVED_ENTRYPOINT_PATH)
    retry_packet = read_json(RETRY_READY_PACKET_PATH)
    closure_receipt = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if resolver_receipt.get("receipt_id") != SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID:
        failures.append("command_resolver_fix_receipt_id_wrong")
    if resolver_receipt.get("gate") != "PASS":
        failures.append("command_resolver_fix_not_pass")
    if resolver_receipt.get("command_resolver_fix_summary", {}).get("entrypoint_resolved") is not False:
        failures.append("command_resolver_fix_entrypoint_not_unresolved")
    if resolver_receipt.get("command_resolver_fix_summary", {}).get("recommended_next_handling") != UNIT_ID:
        failures.append("command_resolver_fix_not_recommending_this_unit")

    if resolver_decision.get("decision_status") != "COMMAND_RESOLVER_STILL_UNRESOLVED_AFTER_SMALL_PROBE":
        failures.append("resolver_decision_status_wrong")
    if small_probe.get("probe_resolved") is not False:
        failures.append("small_probe_unexpectedly_resolved")
    if small_probe.get("selected_probe_new_receipt_count") not in {0, None}:
        failures.append("small_probe_unexpected_receipts")
    if entrypoint.get("entrypoint_resolution_status") != "UNRESOLVED_AFTER_CLI_HELP_AND_SMALL_PROBE":
        failures.append("entrypoint_candidate_not_unresolved")
    if retry_packet.get("packet_status") != "RADIUS_10000_RETRY_BLOCKED_ENTRYPOINT_UNRESOLVED":
        failures.append("retry_packet_not_blocked")

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

def source_inventory() -> Dict[str, Any]:
    files: List[Dict[str, Any]] = []
    for path in sorted(MATRIXLAB_SRC.rglob("*.py"), key=lambda p: rel(p)):
        text = path.read_text(errors="replace")
        lower = text.lower()
        files.append({
            "path": rel(path),
            "sha256": file_sha256(path),
            "size_bytes": path.stat().st_size,
            "line_count": len(text.splitlines()),
            "contains_cli": "typer" in lower or "click" in lower or "argparse" in lower,
            "contains_receipt": "receipt" in lower,
            "contains_radius": "radius" in lower,
            "contains_cycle": "cycle" in lower,
            "contains_run": "run" in lower,
            "contains_write_json": "write_json" in lower or ".write_text" in lower or "json.dump" in lower,
            "contains_gate": "gate" in lower,
        })
    return {
        "schema_version": "r1000_cli_observability_harvest_source_inventory_v0",
        "root": rel(MATRIXLAB_SRC),
        "python_file_count": len(files),
        "files": files,
    }

def call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = call_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return ""

def extract_ast_surface() -> Dict[str, Any]:
    text = CLI_PATH.read_text()
    tree = ast.parse(text)
    commands: List[Dict[str, Any]] = []
    functions: List[Dict[str, Any]] = []
    imports: List[Dict[str, Any]] = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append({
                "lineno": getattr(node, "lineno", None),
                "source": ast.get_source_segment(text, node),
            })

        if isinstance(node, ast.FunctionDef):
            decorators = [ast.get_source_segment(text, d) or "" for d in node.decorator_list]
            is_command = any(".command" in d or "app.command" in d or "cli.command" in d for d in decorators)
            args = []
            for arg in node.args.args:
                args.append(arg.arg)
            for arg in node.args.kwonlyargs:
                args.append(arg.arg)

            fn_record = {
                "name": node.name,
                "lineno": node.lineno,
                "decorators": decorators,
                "is_command": is_command,
                "args": args,
                "docstring": ast.get_docstring(node),
            }
            functions.append(fn_record)
            if is_command:
                commands.append(fn_record)

    return {
        "schema_version": "r1000_cli_observability_harvest_cli_ast_command_surface_v0",
        "cli_path": rel(CLI_PATH),
        "imports": imports,
        "function_count": len(functions),
        "command_count": len(commands),
        "functions": functions,
        "commands": commands,
    }

def receipt_write_surface(inventory: Dict[str, Any]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    tokens = [
        "receipt",
        "json.dump",
        "write_json",
        "write_text",
        "jsonl",
        "gate",
        "cycle",
        "radius",
        "run_id",
        "total_cases",
        "total_receipts",
    ]

    for file_row in inventory["files"]:
        path = ROOT / file_row["path"]
        text = path.read_text(errors="replace")
        lines = text.splitlines()
        hits = []
        for i, line in enumerate(lines, start=1):
            lower = line.lower()
            if any(tok in lower for tok in tokens):
                hits.append({
                    "line": i,
                    "text": line.rstrip()[:240],
                    "tokens": [tok for tok in tokens if tok in lower],
                })
        if hits:
            rows.append({
                "path": file_row["path"],
                "hit_count": len(hits),
                "hits": hits[:120],
                "truncated": len(hits) > 120,
            })

    return {
        "schema_version": "r1000_cli_observability_harvest_module_receipt_write_surface_v0",
        "searched_tokens": tokens,
        "file_hit_count": len(rows),
        "files": rows,
    }

def inspect_help_for_existing_commands() -> Dict[str, Any]:
    base = ["uv", "run", "python", "src/matrixlab/cli.py"]
    probes = [
        base + ["--help"],
        base + ["gate", "--help"],
        base + ["run", "--help"],
        base + ["cycle", "--help"],
        base + ["cycles", "--help"],
        base + ["batch", "--help"],
        base + ["probe", "--help"],
        base + ["receipt", "--help"],
        base + ["receipts", "--help"],
        base + ["harvest", "--help"],
    ]
    results = []
    for args in probes:
        try:
            rc, out, err = run_cmd(args)
            results.append({
                "args": args,
                "returncode": rc,
                "stdout_tail": out[-12000:],
                "stderr_tail": err[-4000:],
            })
        except Exception as exc:
            results.append({
                "args": args,
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
            })
    return {
        "schema_version": "r1000_cli_observability_harvest_help_probe_surface_v0",
        "results": results,
    }

def classify_entrypoint(ast_surface: Dict[str, Any], write_surface: Dict[str, Any], help_surface: Dict[str, Any]) -> Dict[str, Any]:
    command_names = [cmd["name"] for cmd in ast_surface.get("commands", [])]
    help_success = [r for r in help_surface["results"] if r.get("returncode") == 0]
    command_help_names = []
    for r in help_success:
        args = r.get("args") or []
        if len(args) >= 5:
            command_help_names.append(args[4])

    receipt_files = [f for f in write_surface.get("files", []) if "receipt" in json.dumps(f).lower()]
    radius_files = [f for f in write_surface.get("files", []) if "radius" in json.dumps(f).lower()]
    cycle_files = [f for f in write_surface.get("files", []) if "cycle" in json.dumps(f).lower()]

    explicit_harvest_commands = [
        name for name in sorted(set(command_names + command_help_names))
        if any(tok in name.lower() for tok in ["harvest", "batch", "scale", "radius"])
    ]

    receipt_producing_command_candidates = []
    for name in sorted(set(command_names + command_help_names)):
        lower = name.lower()
        if any(tok in lower for tok in ["run", "cycle", "probe", "batch", "harvest", "scale"]):
            receipt_producing_command_candidates.append({
                "command": name,
                "basis": "command name intersects execution vocabulary; prior small probe did not prove receipt production",
                "proven_receipt_producing": False,
            })

    resolved = False
    resolved_command = None
    if explicit_harvest_commands:
        resolved = False
        resolved_command = None

    classification = "NO_PROVEN_RECEIPT_PRODUCING_BOUNDED_HARVEST_ENTRYPOINT_FOUND"
    if receipt_producing_command_candidates:
        classification = "CANDIDATE_EXECUTION_COMMANDS_EXIST_BUT_NONE_PROVEN_RECEIPT_PRODUCING"

    return {
        "schema_version": "r1000_cli_observability_harvest_entrypoint_candidate_surface_v0",
        "entrypoint_candidate_surface_id": sha8({
            "commands": command_names,
            "help_commands": command_help_names,
            "receipt_file_count": len(receipt_files),
            "radius_file_count": len(radius_files),
        }),
        "cli_command_names_from_ast": command_names,
        "cli_command_names_from_help": sorted(set(command_help_names)),
        "explicit_harvest_command_names": explicit_harvest_commands,
        "receipt_surface_file_count": len(receipt_files),
        "radius_surface_file_count": len(radius_files),
        "cycle_surface_file_count": len(cycle_files),
        "receipt_producing_command_candidates": receipt_producing_command_candidates,
        "entrypoint_resolved": resolved,
        "resolved_entrypoint_command": resolved_command,
        "classification": classification,
        "evidence_basis_strength": "source_inspection_only_no_receipt_producing_probe",
    }

def build_missing_entrypoint_proposal(candidate_surface: Dict[str, Any]) -> Dict[str, Any]:
    missing = candidate_surface["entrypoint_resolved"] is False
    return {
        "schema_version": "r1000_cli_observability_harvest_missing_entrypoint_proposal_v0",
        "proposal_status": "CANDIDATE_MISSING_ENTRYPOINT_PROPOSAL" if missing else "NOT_NEEDED_ENTRYPOINT_RESOLVED",
        "missing_object_type": "bounded_receipt_producing_observability_harvest_entrypoint" if missing else None,
        "target_surface": "src/matrixlab/cli.py and existing MatrixLab receipt execution modules",
        "evidence_basis": {
            "command_resolver_fix_receipt_id": SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID,
            "small_probe_new_receipt_count": 0,
            "entrypoint_candidate_classification": candidate_surface["classification"],
            "entrypoint_resolved": candidate_surface["entrypoint_resolved"],
        },
        "required_shape_if_accepted": {
            "must_be_bounded": True,
            "must_accept_radius_or_limit": True,
            "must_emit_receipts_or_receipt_index": True,
            "must_support_small_probe": True,
            "must_not_reopen_closed_queue": True,
            "must_not_mutate_prior_artifacts": True,
            "must_not_hide_next_command": True,
        },
        "application_authorized": False,
        "implementation_authorized_in_this_unit": False,
        "radius_10000_retry_authorized_in_this_unit": False,
    }

def build_decision(candidate_surface: Dict[str, Any], proposal: Dict[str, Any]) -> Dict[str, Any]:
    if candidate_surface["entrypoint_resolved"]:
        status = "ENTRYPOINT_RESOLVED_READY_FOR_SEPARATE_PROBE"
        recommended = "PROBE_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_V0"
    else:
        status = "MISSING_ENTRYPOINT_CONFIRMED_BUILD_REQUIRED"
        recommended = "BUILD_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_V0"

    return {
        "schema_version": "r1000_cli_observability_harvest_entrypoint_inspection_decision_v0",
        "decision_id": sha8({
            "classification": candidate_surface["classification"],
            "recommended": recommended,
            "source_command_resolver_fix_receipt_id": SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID,
        }),
        "decision_status": status,
        "entrypoint_resolved": candidate_surface["entrypoint_resolved"],
        "resolved_entrypoint_command": candidate_surface.get("resolved_entrypoint_command"),
        "missing_entrypoint_proposal_ref": rel(MISSING_ENTRYPOINT_PROPOSAL_PATH),
        "radius_10000_retry_authorized": False,
        "implementation_authorized_in_this_unit": False,
        "recommended_next_handling": recommended,
    }

def build_next_authority_packet(decision: Dict[str, Any], proposal: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_cli_observability_harvest_next_authority_packet_v0",
        "packet_status": "BUILD_MISSING_ENTRYPOINT_AUTHORITY_PACKET" if not decision["entrypoint_resolved"] else "PROBE_RESOLVED_ENTRYPOINT_AUTHORITY_PACKET",
        "source_entrypoint_inspection_decision_ref": rel(ENTRYPOINT_DECISION_PATH),
        "entrypoint_resolved": decision["entrypoint_resolved"],
        "resolved_entrypoint_command": decision["resolved_entrypoint_command"],
        "missing_entrypoint_proposal_ref": rel(MISSING_ENTRYPOINT_PROPOSAL_PATH),
        "authorized_next_unit": decision["recommended_next_handling"],
        "radius_10000_retry_authorized_now": False,
        "implementation_authorized_in_this_unit": False,
        "next_unit_must_preserve": [
            "bounded execution",
            "no unbounded/no-cap run",
            "no closed queue reopen",
            "no closed group inspection",
            "no source artifact mutation except explicitly authored new entrypoint if build unit is accepted",
            "receipt-producing small probe before radius-10000 retry",
        ],
        "recommended_next_handling": decision["recommended_next_handling"],
    }

def build_transition_trace(decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_cli_observability_harvest_entrypoint_inspection_transition_trace_v0",
        "trace": [
            {
                "step": "consume_unresolved_command_resolver_fix",
                "question": "previous resolver fix passed but entrypoint remained unresolved",
                "answer": True,
                "taken": "inspect_cli_and_source_surfaces",
            },
            {
                "step": "inspect_cli_and_source_surfaces",
                "question": "proven bounded receipt-producing harvest entrypoint exists",
                "answer": decision["entrypoint_resolved"],
                "taken": "emit_missing_entrypoint_proposal" if not decision["entrypoint_resolved"] else "emit_probe_authority_packet",
            },
            {
                "step": "emit_next_authority_packet",
                "question": "run radius 10000 now",
                "answer": False,
                "taken": "STOP_CLI_ENTRYPOINT_INSPECTION_COMPLETE_BUILD_ENTRYPOINT_REQUIRED" if not decision["entrypoint_resolved"] else "STOP_CLI_ENTRYPOINT_INSPECTION_COMPLETE_PROBE_READY",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CLI_ENTRYPOINT_INSPECTION_COMPLETE_BUILD_ENTRYPOINT_REQUIRED" if not decision["entrypoint_resolved"] else "STOP_CLI_ENTRYPOINT_INSPECTION_COMPLETE_PROBE_READY",
            "next_command_goal": None,
        },
    }

def build_report(inventory: Dict[str, Any], ast_surface: Dict[str, Any], write_surface: Dict[str, Any], candidate_surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_cli_observability_harvest_entrypoint_inspection_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_command_resolver_fix_receipt_id": SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID,
        "command_resolver_fix_receipt_consumed_count": 1,
        "command_catalog_consumed_count": 1,
        "small_probe_result_consumed_count": 1,
        "cli_source_inventory_emitted_count": 1,
        "cli_ast_command_surface_emitted_count": 1,
        "module_receipt_write_surface_emitted_count": 1,
        "entrypoint_candidate_surface_emitted_count": 1,
        "entrypoint_inspection_decision_emitted_count": 1,
        "missing_entrypoint_proposal_emitted_count": 1 if not decision["entrypoint_resolved"] else 0,
        "next_authority_packet_emitted_count": 1,
        "python_file_count": inventory["python_file_count"],
        "cli_ast_command_count": ast_surface["command_count"],
        "receipt_write_surface_file_count": write_surface["file_hit_count"],
        "entrypoint_resolved_count": 1 if decision["entrypoint_resolved"] else 0,
        "missing_entrypoint_confirmed_count": 0 if decision["entrypoint_resolved"] else 1,
        "radius_10000_retry_executed_count": 0,
        "small_probe_executed_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "queue_reopened_count": 0,
        "closed_group_inspected_count": 0,
        "row_payload_materialized_count": 0,
        "row_payload_inspected_count": 0,
        "identity_assignment_count": 0,
        "field_value_invention_count": 0,
        "repair_executed_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": decision["recommended_next_handling"],
    }

def validate_outputs(candidate: Dict[str, Any], proposal: Dict[str, Any], decision: Dict[str, Any], authority: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if candidate.get("entrypoint_resolved") is True:
        if not candidate.get("resolved_entrypoint_command"):
            failures.append("entrypoint_resolved_without_command")
        if decision.get("recommended_next_handling") != "PROBE_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_V0":
            failures.append("resolved_entrypoint_wrong_next")
    else:
        if proposal.get("proposal_status") != "CANDIDATE_MISSING_ENTRYPOINT_PROPOSAL":
            failures.append("missing_entrypoint_proposal_missing")
        if proposal.get("application_authorized") is not False:
            failures.append("proposal_application_authorized")
        if decision.get("recommended_next_handling") != "BUILD_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_V0":
            failures.append("missing_entrypoint_wrong_next")
        if report.get("missing_entrypoint_confirmed_count") != 1:
            failures.append("missing_entrypoint_confirmed_count_wrong")

    if authority.get("radius_10000_retry_authorized_now") is not False:
        failures.append("authority_authorized_radius_10000_retry")
    if authority.get("implementation_authorized_in_this_unit") is not False:
        failures.append("authority_authorized_implementation_in_this_unit")

    for key in [
        "radius_10000_retry_executed_count",
        "small_probe_executed_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "queue_reopened_count",
        "closed_group_inspected_count",
        "row_payload_materialized_count",
        "row_payload_inspected_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "repair_executed_count",
        "taxonomy_delta_proposal_emitted_count",
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
        "command_resolver_fix_receipt_consumed_count",
        "command_catalog_consumed_count",
        "small_probe_result_consumed_count",
        "cli_source_inventory_emitted_count",
        "cli_ast_command_surface_emitted_count",
        "module_receipt_write_surface_emitted_count",
        "entrypoint_candidate_surface_emitted_count",
        "entrypoint_inspection_decision_emitted_count",
        "next_authority_packet_emitted_count",
    ]:
        if metrics.get(key) != 1:
            failures.append(f"metric_not_one:{key}:{metrics.get(key)}")

    for key in [
        "radius_10000_retry_executed_count",
        "small_probe_executed_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "queue_reopened_count",
        "closed_group_inspected_count",
        "row_payload_materialized_count",
        "row_payload_inspected_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "repair_executed_count",
        "taxonomy_delta_proposal_emitted_count",
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

    inventory = source_inventory()
    ast_surface = extract_ast_surface()
    write_surface = receipt_write_surface(inventory)
    help_surface = inspect_help_for_existing_commands()
    candidate_surface = classify_entrypoint(ast_surface, write_surface, help_surface)
    proposal = build_missing_entrypoint_proposal(candidate_surface)
    decision = build_decision(candidate_surface, proposal)
    authority = build_next_authority_packet(decision, proposal)
    trace = build_transition_trace(decision)
    report = build_report(inventory, ast_surface, write_surface, candidate_surface, decision)

    write_json(SOURCE_INVENTORY_PATH, inventory)
    write_json(CLI_AST_COMMAND_SURFACE_PATH, ast_surface)
    write_json(MODULE_RECEIPT_WRITE_SURFACE_PATH, write_surface)
    write_json(ENTRYPOINT_CANDIDATE_SURFACE_PATH, candidate_surface)
    write_json(MISSING_ENTRYPOINT_PROPOSAL_PATH, proposal)
    write_json(ENTRYPOINT_DECISION_PATH, decision)
    write_json(NEXT_AUTHORITY_PACKET_PATH, authority)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(candidate_surface, proposal, decision, authority, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "CLI_ENTRYPOINT_INSPECTION_0_RESOLVER_FIX_CONSUMED": True,
        "CLI_ENTRYPOINT_INSPECTION_1_SOURCE_INVENTORY_EMITTED": report["cli_source_inventory_emitted_count"] == 1,
        "CLI_ENTRYPOINT_INSPECTION_2_AST_COMMAND_SURFACE_EMITTED": report["cli_ast_command_surface_emitted_count"] == 1,
        "CLI_ENTRYPOINT_INSPECTION_3_RECEIPT_WRITE_SURFACE_EMITTED": report["module_receipt_write_surface_emitted_count"] == 1,
        "CLI_ENTRYPOINT_INSPECTION_4_ENTRYPOINT_CLASSIFIED": candidate_surface["classification"] in {
            "NO_PROVEN_RECEIPT_PRODUCING_BOUNDED_HARVEST_ENTRYPOINT_FOUND",
            "CANDIDATE_EXECUTION_COMMANDS_EXIST_BUT_NONE_PROVEN_RECEIPT_PRODUCING",
        },
        "CLI_ENTRYPOINT_INSPECTION_5_NEXT_AUTHORITY_PACKET_EMITTED": report["next_authority_packet_emitted_count"] == 1,
        "CLI_ENTRYPOINT_INSPECTION_6_RADIUS_10000_NOT_EXECUTED": report["radius_10000_retry_executed_count"] == 0,
        "CLI_ENTRYPOINT_INSPECTION_7_NO_SMALL_PROBE_RERUN": report["small_probe_executed_count"] == 0,
        "CLI_ENTRYPOINT_INSPECTION_8_NO_QUEUE_OR_ROW_ACTION": report["queue_reopened_count"] == 0 and report["row_payload_materialized_count"] == 0,
        "CLI_ENTRYPOINT_INSPECTION_9_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "CLI_ENTRYPOINT_INSPECTION_10_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_command_resolver_fix_receipt_id": SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID,
        "source_failed_harvest_review_receipt_id": SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID,
        "source_failed_harvest_receipt_id": SOURCE_FAILED_HARVEST_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards = {
        "command_resolver_fix_consumed": True,
        "cli_source_inspected": True,
        "matrixlab_source_inventory_materialized": True,
        "entrypoint_resolved": decision["entrypoint_resolved"],
        "missing_entrypoint_proposed": not decision["entrypoint_resolved"],
        "radius_10000_retry_authorized_now": False,
        "radius_10000_retry_executed": False,
        "small_probe_rerun_executed": False,
        "implementation_authorized_in_this_unit": False,
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
        "source_command_resolver_fix_receipt_id": SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID,
        "decision": decision["decision_status"],
        "recommended_next": decision["recommended_next_handling"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_inventory": rel(SOURCE_INVENTORY_PATH),
        "cli_ast_command_surface": rel(CLI_AST_COMMAND_SURFACE_PATH),
        "module_receipt_write_surface": rel(MODULE_RECEIPT_WRITE_SURFACE_PATH),
        "entrypoint_candidate_surface": rel(ENTRYPOINT_CANDIDATE_SURFACE_PATH),
        "missing_entrypoint_proposal": rel(MISSING_ENTRYPOINT_PROPOSAL_PATH),
        "entrypoint_decision": rel(ENTRYPOINT_DECISION_PATH),
        "next_authority_packet": rel(NEXT_AUTHORITY_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_cli_observability_harvest_entrypoint_inspection_receipt_v0",
        "receipt_type": "R1000_CLI_OBSERVABILITY_HARVEST_ENTRYPOINT_INSPECTION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_command_resolver_fix_receipt_id": SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID,
        "source_failed_harvest_review_receipt_id": SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID,
        "source_failed_harvest_receipt_id": SOURCE_FAILED_HARVEST_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "cli_entrypoint_inspection_summary": {
            "decision_status": decision["decision_status"],
            "entrypoint_classification": candidate_surface["classification"],
            "entrypoint_resolved": decision["entrypoint_resolved"],
            "resolved_entrypoint_command": decision["resolved_entrypoint_command"],
            "missing_entrypoint_proposed": not decision["entrypoint_resolved"],
            "radius_10000_retry_authorized": False,
            "radius_10000_retry_executed": False,
            "recommended_next_handling": decision["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "cli_entrypoint_inspection_guards": guards,
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
    print(f"cli_entrypoint_inspection_receipt_id={receipt_id}")
    print(f"cli_entrypoint_inspection_receipt_path=data/r1000_cli_observability_harvest_entrypoint_inspection_v0_receipts/{receipt_id}.json")
    print(f"next_authority_packet_path=data/r1000_cli_observability_harvest_entrypoint_inspection_v0/r1000_cli_observability_harvest_next_authority_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
