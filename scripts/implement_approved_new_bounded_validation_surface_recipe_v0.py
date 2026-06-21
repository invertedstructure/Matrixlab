#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]

POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_recipe_policies"
POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_recipe_policy_receipts"

OUT_ROWS_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_rows"
OUT_MANIFEST_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_manifests"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_receipts"
OUT_RUN_LOG_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_run_logs"

EXPECTED_POLICY_ID = "c176d8d4"
EXPECTED_POLICY_RECEIPT_ID = "3288057c"

IMPLEMENTATION_NAME = "IMPLEMENT_APPROVED_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_V0"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"
SELECTED_OPTION_ID = "OPTION_A_NARROWED"
RUNNER_COMMAND_ID = "EXISTING_MATRIXLAB_CLI_BOUNDED_RUN_V0"

NEXT_IF_ROWS = "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_APPROVED_NEW_BOUNDED_SURFACE_PROBE_POLICY_V0"

APPROVED_BOUNDS = {
    "max_new_runs": 1,
    "max_new_cases_total": 10,
    "max_cycles_per_case": 50,
    "max_candidate_rows": 10000,
    "max_new_bands": 512,
    "max_output_files": 16,
}

PAYLOAD_FIELDS = [
    "cv",
    "state_hash_before",
    "move_id",
    "state_hash_after",
    "raw_compression_ratio_sig6",
]

EXPECTED_VALID_AGAINST = {
    "surface_id": "40e5f5b4",
    "receipt_id": "065849ef",
    "policy_id": "7050f196",
    "policy_receipt_id": "2c061175",
    "candidate_design_id": CANDIDATE_DESIGN_ID,
    "selected_encoding_id": "raw_decimal_sig6",
    "selected_target_raw_delta_field": "compression_ratio",
}

FORBIDDEN_INPUT_NAMES = {
    "registry.sqlite",
    "matrixlab.sqlite",
    "matrixlab.db",
    "registry.db",
}

FORBIDDEN_PATH_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    "raw_delta_signature_candidate_approved_new_bounded_surface_rows",
    "raw_delta_signature_candidate_approved_new_bounded_surface_manifests",
    "raw_delta_signature_candidate_approved_new_bounded_surface_receipts",
    "raw_delta_signature_candidate_approved_new_bounded_surface_run_logs",
}

SAFE_SCAN_ROOTS = [
    ROOT / "logs",
    ROOT / "data",
]

STATE_BEFORE_ALIASES = [
    "state_hash_before",
    "state_sig8_before",
    "state_before_hash",
    "before_state_hash",
    "pre_state_hash",
]
STATE_AFTER_ALIASES = [
    "state_hash_after",
    "state_sig8_after",
    "state_after_hash",
    "after_state_hash",
    "post_state_hash",
]
MOVE_ID_ALIASES = [
    "move_id",
    "move",
    "move_kind",
    "transition_move_id",
]
CV_ALIASES = [
    "cv",
]
COMPRESSION_RATIO_ALIASES = [
    "compression_ratio",
    "raw_compression_ratio",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def blob(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")


def sha8(obj: Any) -> str:
    return hashlib.sha256(blob(obj)).hexdigest()[:8]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def verify_policy(policy: dict[str, Any], receipt: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if policy.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if receipt.get("receipt_id") != EXPECTED_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{receipt.get('receipt_id')}")
    if receipt.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"policy_receipt_policy_id_wrong:{receipt.get('policy_id')}")

    if policy.get("gate") != "PASS":
        failures.append(f"policy_gate_not_PASS:{policy.get('gate')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{receipt.get('gate')}")

    if policy.get("policy_name") != "APPROVED_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_POLICY_V0":
        failures.append(f"policy_name_wrong:{policy.get('policy_name')}")
    if policy.get("policy_status") != "POLICY_ONLY_APPROVED_RECIPE_NOT_EXECUTED":
        failures.append(f"policy_status_wrong:{policy.get('policy_status')}")
    if policy.get("selected_option_id") != SELECTED_OPTION_ID:
        failures.append(f"selected_option_wrong:{policy.get('selected_option_id')}")
    if policy.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"candidate_design_wrong:{policy.get('candidate_design_id')}")
    if policy.get("approved_bounds") != APPROVED_BOUNDS:
        failures.append(f"approved_bounds_wrong:{policy.get('approved_bounds')}")
    if policy.get("valid_against") != EXPECTED_VALID_AGAINST:
        failures.append(f"valid_against_wrong:{policy.get('valid_against')}")

    terminal = policy.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"policy_terminal_type_wrong:{terminal.get('type')}")
    if terminal.get("next_command_goal") != IMPLEMENTATION_NAME:
        failures.append(f"policy_next_goal_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"policy_stop_code_not_none:{terminal.get('stop_code')}")

    auth = policy.get("authority") or {}
    for key in [
        "observer_only_policy_build",
        "authorizes_next_implementation_policy",
        "authorizes_runner_command_precheck_in_next_implementation",
        "authorizes_existing_bounded_runner_execution_in_next_implementation_only",
        "authorizes_observer_extractor_in_next_implementation_only",
        "authorizes_candidate_row_write_in_next_implementation_only",
        "authorizes_surface_manifest_write_in_next_implementation_only",
        "authorizes_surface_receipt_write_in_next_implementation_only",
    ]:
        if auth.get(key) is not True:
            failures.append(f"required_authority_not_true:{key}:{auth.get(key)}")

    if auth.get("authorized_next_command_goal") != IMPLEMENTATION_NAME:
        failures.append(f"authorized_next_goal_wrong:{auth.get('authorized_next_command_goal')}")

    for key in [
        "authorizes_runner_execution_now",
        "authorizes_candidate_rows_creation_now",
        "authorizes_candidate_acceptance",
        "authorizes_scale_mode",
        "authorizes_registry_insertion",
        "authorizes_registry_write",
        "authorizes_registry_sqlite_read",
        "authorizes_full_registry_scan",
        "authorizes_runtime_semantic_change",
        "authorizes_runtime_code_change",
        "authorizes_runtime_receipt_emission_change",
        "authorizes_latest_or_mtime_selection",
        "authorizes_ambient_workspace_inference",
        "authorizes_case_id_or_cycle_n_identity_patch",
        "authorizes_rowid_or_receipt_hash_truth_surface",
        "authorizes_full_occurrence_key_in_payload",
        "authorizes_audit_pointer_in_payload",
        "authorizes_debug_payload_in_payload",
        "authorizes_microhash_as_proof",
        "authorizes_synthetic_fake_validation_rows",
        "authorizes_transition_compression_probe",
    ]:
        if auth.get(key) is not False:
            failures.append(f"forbidden_authority_not_false:{key}:{auth.get(key)}")

    contract = policy.get("recipe_contract") or {}
    if contract.get("recipe_id") != "OPTION_A_NARROWED_APPROVED_RECIPE_V0":
        failures.append(f"recipe_id_wrong:{contract.get('recipe_id')}")
    if contract.get("recipe_status") != "APPROVED_FOR_POLICY_IMPLEMENTATION_NOT_EXECUTED":
        failures.append(f"recipe_status_wrong:{contract.get('recipe_status')}")
    if contract.get("recipe_shape") != "existing_cli_fresh_run_plus_observer_extractor":
        failures.append(f"recipe_shape_wrong:{contract.get('recipe_shape')}")

    runner = contract.get("runner_recipe") or {}
    if runner.get("runner_command_id") != RUNNER_COMMAND_ID:
        failures.append(f"runner_command_id_wrong:{runner.get('runner_command_id')}")
    if runner.get("runner_command_status") != "DECLARED_FOR_NEXT_IMPLEMENTATION_PRECHECK_REQUIRED":
        failures.append(f"runner_command_status_wrong:{runner.get('runner_command_status')}")
    if runner.get("runner_command_precheck_required") is not True:
        failures.append(f"runner_precheck_not_true:{runner.get('runner_command_precheck_required')}")
    if runner.get("bounded_parameters") != {
        "families": ["projection_quotient"],
        "depth_min": 3,
        "depth_max": 12,
        "case_count_expected_max": 10,
        "cycles_per_case": 50,
        "max_cells": 50000,
        "max_new_runs": 1,
    }:
        failures.append(f"runner_bounds_wrong:{runner.get('bounded_parameters')}")

    extractor = contract.get("observer_extractor_contract") or {}
    if extractor.get("extractor_name") != "RAW_DELTA_SIGNATURE_CANDIDATE_NEW_BOUNDED_SURFACE_OBSERVER_EXTRACTOR_V0":
        failures.append(f"extractor_name_wrong:{extractor.get('extractor_name')}")
    if extractor.get("extractor_mode") != "OUTER_OBSERVER_ONLY":
        failures.append(f"extractor_mode_wrong:{extractor.get('extractor_mode')}")

    schema = (extractor.get("candidate_row_schema") or {})
    if schema.get("signature_payload_fields") != PAYLOAD_FIELDS:
        failures.append(f"payload_fields_wrong:{schema.get('signature_payload_fields')}")
    if schema.get("truth_surface") != "full_occurrence_key_to_candidate_delta_signature":
        failures.append(f"truth_surface_wrong:{schema.get('truth_surface')}")
    for f in [
        "case_id",
        "cycle_n",
        "rowid",
        "receipt_hash",
        "receipt_path",
        "audit_pointer",
        "debug_payload",
        "full_occurrence_key",
        "registry_rowid",
    ]:
        if f not in set(schema.get("payload_forbidden_fields") or []):
            failures.append(f"payload_forbidden_field_missing:{f}")

    gates = policy.get("required_next_implementation_gates") or {}
    for key in [
        "must_compile",
        "must_precheck_runner_command",
        "must_execute_at_most_one_new_run",
        "must_capture_explicit_run_id",
        "must_read_only_explicit_run_receipts",
        "must_write_candidate_rows_under_bound",
        "must_emit_surface_manifest",
        "must_emit_surface_receipt",
        "must_not_use_latest_or_mtime",
        "must_not_read_registry_sqlite",
        "must_not_full_registry_scan",
        "must_not_change_runtime_code",
        "must_not_change_runtime_receipt_emission",
        "must_not_accept_candidate",
        "must_not_authorize_scale_mode",
        "must_not_write_registry",
        "must_not_create_synthetic_rows",
        "must_halt_if_no_candidate_compatible_rows",
        "must_halt_if_runner_command_unavailable",
    ]:
        if gates.get(key) is not True:
            failures.append(f"required_gate_not_true:{key}:{gates.get(key)}")

    return failures


def command_precheck(command: list[str]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "precheck_attempted": True,
        "runner_command_available": False,
        "runner_command_path_exists": False,
        "runner_help_checked": False,
        "runner_help_exit_code": None,
        "runner_help_stdout_tail": "",
        "runner_help_stderr_tail": "",
        "failure": None,
    }

    cli_path = ROOT / "src" / "matrixlab" / "cli.py"
    result["runner_command_path_exists"] = cli_path.exists()
    if not cli_path.exists():
        result["failure"] = "HOLD_APPROVED_RECIPE_RUNNER_COMMAND_UNAVAILABLE"
        return result

    help_cmd = command[:4] + ["run", "--help"] if command[:4] == ["uv", "run", "python", "src/matrixlab/cli.py"] else command + ["--help"]
    try:
        proc = subprocess.run(
            help_cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )
        result["runner_help_checked"] = True
        result["runner_help_exit_code"] = proc.returncode
        result["runner_help_stdout_tail"] = proc.stdout[-2000:]
        result["runner_help_stderr_tail"] = proc.stderr[-2000:]
        help_text = proc.stdout + "\n" + proc.stderr
        required_flags = ["--families", "--depth-min", "--depth-max", "--cycles-per-case", "--max-cells"]
        missing = [flag for flag in required_flags if flag not in help_text]
        if proc.returncode == 0 and not missing:
            result["runner_command_available"] = True
        else:
            result["failure"] = "HOLD_APPROVED_RECIPE_RUNNER_COMMAND_UNAVAILABLE"
            result["missing_flags"] = missing
    except Exception as exc:
        result["failure"] = "HOLD_APPROVED_RECIPE_RUNNER_COMMAND_UNAVAILABLE"
        result["exception"] = repr(exc)

    return result


def run_bounded_runner(command: list[str], run_log_path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "runner_executed": False,
        "runner_exit_code": None,
        "runner_stdout_path": rel(run_log_path),
        "runner_stderr_path": None,
        "captured_run_id": None,
        "failure": None,
    }
    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=900,
        )
        result["runner_executed"] = True
        result["runner_exit_code"] = proc.returncode
        run_log_path.write_text(
            json.dumps(
                {
                    "command": command,
                    "returncode": proc.returncode,
                    "stdout": proc.stdout,
                    "stderr": proc.stderr,
                    "created_at": now_iso(),
                },
                indent=2,
                sort_keys=True,
            )
        )

        text = proc.stdout + "\n" + proc.stderr
        match = re.search(r"\b(run_[0-9]{8}_[0-9]{6}_[0-9]+)\b", text)
        if match:
            result["captured_run_id"] = match.group(1)

        if proc.returncode != 0:
            result["failure"] = "HOLD_APPROVED_RECIPE_RUNNER_COMMAND_FAILED"
        elif not result["captured_run_id"]:
            result["failure"] = "HOLD_APPROVED_RECIPE_RUN_ID_NOT_CAPTURED"
    except subprocess.TimeoutExpired as exc:
        result["runner_executed"] = True
        result["failure"] = "HOLD_APPROVED_RECIPE_RUNNER_TIMEOUT"
        run_log_path.write_text(
            json.dumps(
                {
                    "command": command,
                    "timeout": True,
                    "exception": repr(exc),
                    "stdout": (exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
                    "stderr": (exc.stderr or "")[-4000:] if isinstance(exc.stderr, str) else "",
                    "created_at": now_iso(),
                },
                indent=2,
                sort_keys=True,
            )
        )
    except Exception as exc:
        result["failure"] = "HOLD_APPROVED_RECIPE_RUNNER_EXCEPTION"
        result["exception"] = repr(exc)

    return result


def allowed_file(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.name in FORBIDDEN_INPUT_NAMES:
        return False
    if path.suffix.lower() not in {".json", ".jsonl", ".txt"}:
        return False
    parts = set(path.parts)
    if parts.intersection(FORBIDDEN_PATH_PARTS):
        return False
    lower = str(path).lower()
    if lower.endswith((".sqlite", ".db", ".sqlite3")):
        return False
    return True


def find_files_for_run_id(run_id: str) -> list[Path]:
    found: list[Path] = []
    for root in SAFE_SCAN_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not allowed_file(path):
                continue
            try:
                text = path.read_text(errors="ignore")
            except Exception:
                continue
            if run_id in text:
                found.append(path)
    unique = []
    seen = set()
    for p in found:
        rp = rel(p)
        if rp not in seen:
            unique.append(p)
            seen.add(rp)
    return sorted(unique, key=lambda p: rel(p))


def iter_json_objects_from_file(path: Path, run_id: str) -> Iterable[tuple[dict[str, Any], str]]:
    try:
        if path.suffix.lower() == ".jsonl":
            for idx, line in enumerate(path.read_text(errors="ignore").splitlines(), start=1):
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                yield from walk_json(obj, run_id, f"{rel(path)}:{idx}", inherited_run_id=None)
        elif path.suffix.lower() == ".json":
            try:
                obj = json.loads(path.read_text(errors="ignore"))
            except Exception:
                return
            yield from walk_json(obj, run_id, rel(path), inherited_run_id=None)
    except Exception:
        return


def walk_json(value: Any, run_id: str, source_ref: str, inherited_run_id: str | None) -> Iterable[tuple[dict[str, Any], str]]:
    if isinstance(value, dict):
        current_run_id = value.get("run_id") or inherited_run_id
        if current_run_id == run_id:
            yield value, source_ref
        for k, v in value.items():
            if isinstance(v, (dict, list)):
                yield from walk_json(v, run_id, source_ref, current_run_id)
    elif isinstance(value, list):
        for idx, item in enumerate(value):
            yield from walk_json(item, run_id, f"{source_ref}#{idx}", inherited_run_id)


def is_forbidden_traversal_key(key: str) -> bool:
    lower = key.lower()
    return any(part in lower for part in ["debug", "audit", "registry", "receipt_path"])


def deep_get_first(obj: Any, aliases: list[str]) -> Any:
    aliases_set = set(aliases)

    def walk(value: Any) -> Any:
        if isinstance(value, dict):
            for k, v in value.items():
                if k in aliases_set and not is_forbidden_traversal_key(k):
                    return v
            for k, v in value.items():
                if is_forbidden_traversal_key(k):
                    continue
                got = walk(v)
                if got is not None:
                    return got
        elif isinstance(value, list):
            for v in value:
                got = walk(v)
                if got is not None:
                    return got
        return None

    return walk(obj)


def decimal_sig6(value: Any) -> str | None:
    try:
        f = float(value)
    except Exception:
        return None
    if not (f == f) or f in (float("inf"), float("-inf")):
        return None
    return format(f, ".6g")


def as_string(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def make_row(obj: dict[str, Any], run_id: str, source_ref: str, surface_id: str) -> tuple[dict[str, Any] | None, str | None]:
    cv = as_string(deep_get_first(obj, CV_ALIASES))
    state_before = as_string(deep_get_first(obj, STATE_BEFORE_ALIASES))
    state_after = as_string(deep_get_first(obj, STATE_AFTER_ALIASES))
    move_id = as_string(deep_get_first(obj, MOVE_ID_ALIASES))
    ratio_raw = deep_get_first(obj, COMPRESSION_RATIO_ALIASES)
    ratio_sig6 = decimal_sig6(ratio_raw)

    missing = []
    if cv is None:
        missing.append("cv")
    if state_before is None:
        missing.append("state_hash_before")
    if move_id is None:
        missing.append("move_id")
    if state_after is None:
        missing.append("state_hash_after")
    if ratio_sig6 is None:
        missing.append("raw_compression_ratio_sig6")

    if missing:
        return None, ",".join(missing)

    receipt_id = as_string(obj.get("receipt_id") or obj.get("id") or obj.get("receipt_sig8"))
    family = as_string(obj.get("family") or obj.get("family_id"))
    depth = as_string(obj.get("depth") or obj.get("depth_n"))
    cycle = as_string(obj.get("cycle") or obj.get("cycle_n"))
    transition_id = as_string(obj.get("transition_id"))

    full_occurrence_key = {
        "source_run_id": run_id,
        "source_receipt_ref": source_ref,
        "source_receipt_id": receipt_id,
        "family": family,
        "depth": depth,
        "cycle": cycle,
        "transition_id": transition_id,
        "state_hash_before": state_before,
        "move_id": move_id,
        "state_hash_after": state_after,
    }

    signature_payload = {
        "cv": cv,
        "state_hash_before": state_before,
        "move_id": move_id,
        "state_hash_after": state_after,
        "raw_compression_ratio_sig6": ratio_sig6,
    }

    candidate_delta_signature = sha8(
        {
            "candidate_design_id": CANDIDATE_DESIGN_ID,
            "signature_payload": signature_payload,
        }
    )

    row = {
        "row_type": "RAW_DELTA_SIGNATURE_CANDIDATE_V0_ROW",
        "row_id": sha8({"full_occurrence_key": full_occurrence_key, "candidate_delta_signature": candidate_delta_signature}),
        "source_run_id": run_id,
        "source_receipt_ref": source_ref,
        "full_occurrence_key": full_occurrence_key,
        "candidate_delta_signature": candidate_delta_signature,
        "signature_payload": signature_payload,
        "truth_surface": "full_occurrence_key_to_candidate_delta_signature",
        "source_surface_id": surface_id,
        "created_by": IMPLEMENTATION_NAME,
    }
    return row, None


def extract_rows(run_id: str, surface_id: str, max_files: int, max_rows: int) -> dict[str, Any]:
    files = find_files_for_run_id(run_id)
    result: dict[str, Any] = {
        "receipt_files_found": [rel(p) for p in files],
        "receipt_files_found_total": len(files),
        "receipt_files_used": [],
        "receipt_files_used_total": 0,
        "candidate_compatible_rows": [],
        "rows_created": 0,
        "missing_field_counts": {},
        "objects_seen_for_run_id": 0,
        "failure": None,
    }

    if not files:
        result["failure"] = "HOLD_APPROVED_RECIPE_NO_FILE_BACKED_RECEIPTS"
        return result

    if len(files) > max_files:
        result["failure"] = "HOLD_APPROVED_RECIPE_AMBIGUOUS_SOURCE_SURFACE"
        return result

    used: list[str] = []
    rows_by_id: dict[str, dict[str, Any]] = {}
    missing_counts: dict[str, int] = {}

    for path in files:
        file_used = False
        for obj, source_ref in iter_json_objects_from_file(path, run_id):
            result["objects_seen_for_run_id"] += 1
            row, missing = make_row(obj, run_id, source_ref, surface_id)
            if row is None:
                if missing:
                    missing_counts[missing] = missing_counts.get(missing, 0) + 1
                continue
            file_used = True
            rows_by_id[row["row_id"]] = row
            if len(rows_by_id) > max_rows:
                result["failure"] = "HOLD_APPROVED_RECIPE_ROWS_EXCEED_BOUND"
                break
        if file_used:
            used.append(rel(path))
        if result["failure"]:
            break

    rows = list(rows_by_id.values())
    rows.sort(key=lambda r: r["row_id"])

    result["receipt_files_used"] = used
    result["receipt_files_used_total"] = len(used)
    result["candidate_compatible_rows"] = rows
    result["rows_created"] = len(rows)
    result["missing_field_counts"] = missing_counts

    if not result["failure"] and not rows:
        result["failure"] = "HOLD_APPROVED_RECIPE_NO_CANDIDATE_COMPATIBLE_ROWS"

    return result


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))


def build_terminal(failures: list[str], hold_code: str | None, rows_created: int) -> dict[str, Any]:
    if failures:
        return {
            "type": "STOP",
            "stop_code": "STOP_APPROVED_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_INVALID",
            "next_command_goal": None,
        }
    if hold_code:
        return {
            "type": "HOLD",
            "stop_code": hold_code,
            "next_command_goal": None,
        }
    if rows_created > 0:
        return {
            "type": "ADVANCE",
            "stop_code": None,
            "next_command_goal": NEXT_IF_ROWS,
        }
    return {
        "type": "HOLD",
        "stop_code": "HOLD_APPROVED_RECIPE_NO_CANDIDATE_COMPATIBLE_ROWS",
        "next_command_goal": None,
    }


def implement(policy_id: str, execute_runner: bool = True, write_outputs: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    policy = load_json(POLICY_DIR / f"{policy_id}.json")
    policy_receipt = load_json(POLICY_RECEIPT_DIR / f"{policy_id}.json")
    failures = verify_policy(policy, policy_receipt)

    if write_outputs:
        OUT_ROWS_DIR.mkdir(parents=True, exist_ok=True)
        OUT_MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
        OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
        OUT_RUN_LOG_DIR.mkdir(parents=True, exist_ok=True)

    surface_seed = {
        "implementation_name": IMPLEMENTATION_NAME,
        "policy_id": policy_id,
        "policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "selected_option_id": SELECTED_OPTION_ID,
        "created_at_day": datetime.now(timezone.utc).strftime("%Y%m%d"),
    }
    surface_id = sha8(surface_seed)

    runner = (policy.get("recipe_contract") or {}).get("runner_recipe") or {}
    command = runner.get("runner_command") or []
    run_log_path = OUT_RUN_LOG_DIR / f"{surface_id}_runner.json"

    precheck = command_precheck(command)
    runner_result: dict[str, Any] = {
        "runner_executed": False,
        "runner_exit_code": None,
        "captured_run_id": None,
        "failure": None,
    }
    extraction: dict[str, Any] = {
        "receipt_files_found": [],
        "receipt_files_found_total": 0,
        "receipt_files_used": [],
        "receipt_files_used_total": 0,
        "candidate_compatible_rows": [],
        "rows_created": 0,
        "missing_field_counts": {},
        "objects_seen_for_run_id": 0,
        "failure": None,
    }

    hold_code: str | None = None

    if failures:
        hold_code = None
    elif not precheck.get("runner_command_available"):
        hold_code = precheck.get("failure") or "HOLD_APPROVED_RECIPE_RUNNER_COMMAND_UNAVAILABLE"
    elif not execute_runner:
        hold_code = "HOLD_APPROVED_RECIPE_EXECUTION_DISABLED"
    else:
        runner_result = run_bounded_runner(command, run_log_path)
        if runner_result.get("failure"):
            hold_code = runner_result["failure"]
        else:
            run_id = runner_result.get("captured_run_id")
            extraction = extract_rows(
                run_id=run_id,
                surface_id=surface_id,
                max_files=APPROVED_BOUNDS["max_output_files"],
                max_rows=APPROVED_BOUNDS["max_candidate_rows"],
            )
            if extraction.get("failure"):
                hold_code = extraction["failure"]

    rows = extraction.get("candidate_compatible_rows") or []
    rows_created = len(rows)
    bands_created = len({row["candidate_delta_signature"] for row in rows})

    rows_path = OUT_ROWS_DIR / f"{surface_id}.jsonl"
    manifest_path = OUT_MANIFEST_DIR / f"{surface_id}.json"
    receipt_path = OUT_RECEIPT_DIR / f"{surface_id}.json"

    if rows_created > APPROVED_BOUNDS["max_candidate_rows"]:
        hold_code = "HOLD_APPROVED_RECIPE_ROWS_EXCEED_BOUND"
    if bands_created > APPROVED_BOUNDS["max_new_bands"]:
        hold_code = "HOLD_APPROVED_RECIPE_BANDS_EXCEED_BOUND"

    terminal = build_terminal(failures, hold_code, rows_created)

    authority_guards = {
        "runner_precheck_attempted": bool(precheck.get("precheck_attempted")),
        "runner_command_available": bool(precheck.get("runner_command_available")),
        "runner_executed": bool(runner_result.get("runner_executed")),
        "runner_executions_total": 1 if runner_result.get("runner_executed") else 0,
        "explicit_run_id_captured": runner_result.get("captured_run_id") is not None,
        "explicit_run_id": runner_result.get("captured_run_id"),
        "candidate_rows_created": rows_created > 0,
        "candidate_rows_created_total": rows_created,
        "surface_manifest_written": write_outputs,
        "surface_receipt_written": write_outputs,
        "candidate_accepted": False,
        "scale_mode_authorized": False,
        "registry_inserted": False,
        "registry_written": False,
        "registry_sqlite_read": False,
        "full_registry_scan_used": False,
        "runtime_semantic_changed": False,
        "runtime_code_changed": False,
        "runtime_receipt_emission_changed": False,
        "latest_or_mtime_selection_used": False,
        "ambient_workspace_inference_used": False,
        "case_id_or_cycle_n_identity_patch_used": False,
        "rowid_or_receipt_hash_truth_surface_used": False,
        "full_occurrence_key_in_signature_payload": False,
        "audit_or_debug_payload_in_signature_payload": False,
        "microhash_as_proof_used": False,
        "synthetic_fake_validation_rows_used": False,
        "transition_compression_probe_run": False,
    }

    manifest = {
        "schema_version": "raw_delta_signature_candidate_approved_new_bounded_surface_manifest_v0",
        "surface_id": surface_id,
        "implementation_name": IMPLEMENTATION_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "policy_id": policy_id,
        "policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_decision_id": policy.get("source_decision_id"),
        "source_decision_receipt_id": policy.get("source_decision_receipt_id"),
        "selected_option_id": SELECTED_OPTION_ID,
        "valid_against": EXPECTED_VALID_AGAINST,
        "approved_bounds": APPROVED_BOUNDS,
        "runner_command_id": RUNNER_COMMAND_ID,
        "runner_command": command,
        "runner_precheck": precheck,
        "runner_result": runner_result,
        "receipt_discovery": {
            "receipt_files_found": extraction.get("receipt_files_found"),
            "receipt_files_found_total": extraction.get("receipt_files_found_total"),
            "receipt_files_used": extraction.get("receipt_files_used"),
            "receipt_files_used_total": extraction.get("receipt_files_used_total"),
            "objects_seen_for_run_id": extraction.get("objects_seen_for_run_id"),
            "missing_field_counts": extraction.get("missing_field_counts"),
        },
        "surface_rows_path": rel(rows_path),
        "surface_receipt_path": rel(receipt_path),
        "rows_created": rows_created,
        "new_bands_created": bands_created,
        "candidate_signature_distinct_count": bands_created,
        "truth_surface": "full_occurrence_key_to_candidate_delta_signature",
        "signature_payload_fields": PAYLOAD_FIELDS,
        "hold_code": hold_code,
        "terminal": terminal,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "authority_guards": authority_guards,
        "created_at": now_iso(),
    }

    receipt = {
        "schema_version": "raw_delta_signature_candidate_approved_new_bounded_surface_receipt_v0",
        "receipt_type": "APPROVED_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_IMPLEMENTATION_RECEIPT",
        "surface_id": surface_id,
        "implementation_name": IMPLEMENTATION_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "policy_id": policy_id,
        "policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_decision_id": policy.get("source_decision_id"),
        "source_decision_receipt_id": policy.get("source_decision_receipt_id"),
        "selected_option_id": SELECTED_OPTION_ID,
        "valid_against": EXPECTED_VALID_AGAINST,
        "approved_bounds": APPROVED_BOUNDS,
        "runner_command": command,
        "runner_precheck": precheck,
        "runner_result": runner_result,
        "explicit_run_id": runner_result.get("captured_run_id"),
        "receipt_files_found_total": extraction.get("receipt_files_found_total"),
        "receipt_files_used_total": extraction.get("receipt_files_used_total"),
        "receipt_files_used": extraction.get("receipt_files_used"),
        "rows_created": rows_created,
        "new_bands_created": bands_created,
        "candidate_signature_distinct_count": bands_created,
        "surface_rows_path": rel(rows_path),
        "surface_manifest_path": rel(manifest_path),
        "truth_surface": "full_occurrence_key_to_candidate_delta_signature",
        "signature_payload_fields": PAYLOAD_FIELDS,
        "payload_forbidden_fields": [
            "case_id",
            "cycle_n",
            "rowid",
            "receipt_hash",
            "receipt_path",
            "audit_pointer",
            "debug_payload",
            "full_occurrence_key",
            "registry_rowid",
        ],
        "authority_guards": authority_guards,
        "hold_code": hold_code,
        "terminal": terminal,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id
    manifest["receipt_id"] = receipt_id

    if write_outputs:
        if rows_created > 0:
            write_jsonl(rows_path, rows)
        else:
            rows_path.write_text("")
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True))
        receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return manifest, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy-id", default=EXPECTED_POLICY_ID)
    parser.add_argument("--no-execute", action="store_true")
    args = parser.parse_args()

    manifest, receipt = implement(
        policy_id=args.policy_id,
        execute_runner=not args.no_execute,
        write_outputs=True,
    )

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"surface_id={receipt['surface_id']}")
    print(f"surface_rows_path={receipt['surface_rows_path']}")
    print(f"surface_manifest_path={receipt['surface_manifest_path']}")
    print(f"surface_receipt_path=data/raw_delta_signature_candidate_approved_new_bounded_surface_receipts/{receipt['surface_id']}.json")

    return 0 if receipt["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
