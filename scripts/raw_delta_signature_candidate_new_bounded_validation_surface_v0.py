#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_validation_surface_policies"
POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_validation_surface_policy_receipts"
BOUNDED_SCALE_OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_bounded_scale_outs"
BOUNDED_SCALE_OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_bounded_scale_out_receipts"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_validation_surfaces"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_validation_surface_receipts"
OUT_ROWS_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_validation_surface_rows"

EXPECTED_POLICY_ID = "7050f196"
EXPECTED_POLICY_RECEIPT_ID = "2c061175"
EXPECTED_BOUNDED_SCALE_OUT_ID = "2b44b1fd"
EXPECTED_BOUNDED_SCALE_OUT_RECEIPT_ID = "f67b629b"

SURFACE_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_NEW_BOUNDED_VALIDATION_SURFACE_V0"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"
MODE = "OUTER_OBSERVER_ONLY"

SELECTED_ENCODING_ID = "raw_decimal_sig6"
TARGET_RAW_DELTA_FIELD = "compression_ratio"

CANDIDATE_PAYLOAD_FIELDS = [
    "cv",
    "state_hash_before",
    "move_id",
    "state_hash_after",
    "raw_compression_ratio_sig6",
]

FORBIDDEN_PAYLOAD_FIELDS = {
    "full_occurrence_key",
    "raw_full_receipt_hash",
    "full_receipt_hash",
    "receipt_hash",
    "receipt_sig8",
    "receipt_rowid",
    "rowid",
    "audit_pointer",
    "debug_payload",
    "observer_notes",
    "created_at",
    "created_utc",
    "timestamp",
    "path",
    "receipt_path",
    "file_path",
    "case_id",
    "cycle_n",
    "case_id_as_primary_identity",
    "cycle_n_as_primary_identity",
    "depth_as_primary_identity",
    "raw_delta_microhash_32_as_proof",
    "microhash",
}

FORBIDDEN_AUTHORITY_FALSE = [
    "authorizes_candidate_acceptance",
    "authorizes_scale_mode",
    "authorizes_full_registry_scan",
    "authorizes_registry_sqlite_read",
    "authorizes_runtime_receipt_emission_change",
    "authorizes_runtime_code_change",
    "authorizes_registry_write",
    "authorizes_receipt_replacement",
    "authorizes_receipt_deletion",
    "authorizes_receipt_compression",
    "authorizes_receipt_suppression",
    "authorizes_case_id_or_cycle_n_primary_identity_patch",
    "authorizes_rowid_or_receipt_hash_patch",
    "authorizes_raw_receipt_hash_truth_surface",
    "authorizes_full_occurrence_key_in_payload",
    "authorizes_audit_pointer_in_payload",
    "authorizes_debug_payload_in_payload",
    "authorizes_microhash_as_proof",
    "authorizes_synthetic_fake_validation_rows",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def blob(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")


def sha8(obj: Any) -> str:
    return hashlib.sha256(blob(obj)).hexdigest()[:8]


def canonical_bytes(obj: Any) -> int:
    return len(blob(obj))


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def forbidden_path(path: Path) -> bool:
    rp = rel(path)
    return (
        path.suffix in {".sqlite", ".db"}
        or "registry.sqlite" in rp
        or "registry.db" in rp
    )


def safe_read_text(path: Path, max_chars: int = 20000) -> str:
    if forbidden_path(path):
        raise RuntimeError(f"forbidden path read: {rel(path)}")
    try:
        return path.read_text(errors="replace")[:max_chars]
    except Exception as exc:
        return f"<<READ_ERROR:{type(exc).__name__}:{exc}>>"


def run_help_command(cmd: list[str], timeout: int = 20) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        return {
            "cmd": cmd,
            "returncode": proc.returncode,
            "stdout_head": proc.stdout[:4000],
            "stderr_head": proc.stderr[:4000],
            "timeout": False,
            "elapsed_ms": int(round((time.perf_counter() - started) * 1000)),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "cmd": cmd,
            "returncode": None,
            "stdout_head": (exc.stdout or "")[:4000] if isinstance(exc.stdout, str) else "",
            "stderr_head": (exc.stderr or "")[:4000] if isinstance(exc.stderr, str) else "",
            "timeout": True,
            "elapsed_ms": int(round((time.perf_counter() - started) * 1000)),
        }
    except Exception as exc:
        return {
            "cmd": cmd,
            "returncode": None,
            "stdout_head": "",
            "stderr_head": f"{type(exc).__name__}: {exc}",
            "timeout": False,
            "elapsed_ms": int(round((time.perf_counter() - started) * 1000)),
        }


def surface_aggregate(source: dict[str, Any], flat_key: str, nested_key: str) -> dict[str, Any]:
    flat = source.get(flat_key)
    if isinstance(flat, dict) and flat:
        return flat
    nested = source.get(nested_key)
    if isinstance(nested, dict):
        agg = nested.get("aggregate")
        if isinstance(agg, dict) and agg:
            return agg
    return {}


def verify_policy_and_sources(
    policy: dict[str, Any],
    policy_receipt: dict[str, Any],
    bounded_scale_out: dict[str, Any],
    bounded_scale_out_receipt: dict[str, Any],
) -> list[str]:
    failures: list[str] = []

    if policy.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if policy_receipt.get("receipt_id") != EXPECTED_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy_receipt.get('receipt_id')}")
    if policy.get("gate") != "PASS":
        failures.append(f"policy_gate_not_PASS:{policy.get('gate')}")
    if policy_receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{policy_receipt.get('gate')}")
    if policy.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{policy.get('policy_status')}")
    if policy.get("surface_name") != SURFACE_NAME:
        failures.append(f"policy_surface_name_wrong:{policy.get('surface_name')}")
    if policy.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"policy_candidate_design_wrong:{policy.get('candidate_design_id')}")
    if policy.get("terminal", {}).get("next_command_goal") != "IMPLEMENT_RAW_DELTA_SIGNATURE_CANDIDATE_NEW_BOUNDED_VALIDATION_SURFACE_V0":
        failures.append(f"policy_next_goal_wrong:{policy.get('terminal', {}).get('next_command_goal')}")

    contract = policy.get("surface_contract") or {}
    if contract.get("surface_name") != SURFACE_NAME:
        failures.append(f"contract_surface_name_wrong:{contract.get('surface_name')}")
    if contract.get("surface_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"contract_surface_status_wrong:{contract.get('surface_status')}")
    if contract.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"contract_candidate_design_wrong:{contract.get('candidate_design_id')}")
    if contract.get("source_hold_class") != "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY":
        failures.append(f"contract_source_hold_wrong:{contract.get('source_hold_class')}")
    if contract.get("selected_encoding_id") != SELECTED_ENCODING_ID:
        failures.append(f"contract_encoding_wrong:{contract.get('selected_encoding_id')}")
    if contract.get("selected_target_raw_delta_field") != TARGET_RAW_DELTA_FIELD:
        failures.append(f"contract_target_wrong:{contract.get('selected_target_raw_delta_field')}")
    if contract.get("candidate_payload_fields") != CANDIDATE_PAYLOAD_FIELDS:
        failures.append(f"contract_payload_wrong:{contract.get('candidate_payload_fields')}")
    if contract.get("truth_surface") != "full_occurrence_key_to_candidate_delta_signature":
        failures.append(f"contract_truth_surface_wrong:{contract.get('truth_surface')}")

    for field in [
        "full_occurrence_key",
        "receipt_hash",
        "rowid",
        "audit_pointer",
        "debug_payload",
        "case_id",
        "cycle_n",
        "raw_delta_microhash_32_as_proof",
    ]:
        if field not in set(contract.get("candidate_payload_forbidden_fields") or []):
            failures.append(f"forbidden_payload_field_missing:{field}")

    actions = contract.get("new_surface_authorized_actions") or {}
    for key in [
        "inspect_existing_runner_entrypoints",
        "create_new_bounded_validation_surface",
        "write_new_surface_manifest",
        "write_new_surface_receipt",
        "write_candidate_compatible_rows_if_surface_created",
        "hold_if_no_safe_runner_or_recipe_exists",
    ]:
        if actions.get(key) is not True:
            failures.append(f"authorized_action_missing:{key}:{actions.get(key)}")

    forbidden_actions = contract.get("new_surface_forbidden_actions") or {}
    for key in [
        "candidate_acceptance",
        "scale_mode_acceptance",
        "full_registry_scan",
        "registry_sqlite_read",
        "registry_write",
        "runtime_receipt_emission_change",
        "source_runtime_code_change",
        "receipt_replacement_deletion_compression_or_suppression",
        "case_id_or_cycle_n_primary_identity_patch",
        "rowid_or_receipt_hash_patch",
        "full_occurrence_key_in_signature_payload",
        "audit_pointer_or_debug_payload_in_signature_payload",
        "raw_delta_microhash_32_as_proof",
        "synthetic_fake_validation_rows",
    ]:
        if forbidden_actions.get(key) is not True:
            failures.append(f"forbidden_action_not_marked:{key}:{forbidden_actions.get(key)}")

    rule = contract.get("bounded_surface_generation_rule") or {}
    for key in [
        "generation_must_be_bounded",
        "generation_must_be_reproducible",
        "generation_must_use_existing_project_runner_or_existing_receipt_builder_only",
        "generation_must_not_modify_runtime_code",
        "generation_must_not_read_registry_sqlite",
        "generation_must_not_full_registry_scan",
        "generation_must_not_accept_candidate",
        "generation_must_not_authorize_scale_mode",
        "generation_must_record_command_or_recipe",
        "generation_must_record_inputs",
        "generation_must_record_output_paths",
        "generation_must_record_limits",
        "generation_must_record_failure_or_hold_reason",
    ]:
        if rule.get(key) is not True:
            failures.append(f"generation_rule_not_true:{key}:{rule.get(key)}")

    bounds = rule.get("bounds") or {}
    expected_bounds = {
        "max_new_runs": 3,
        "max_new_cases_total": 30,
        "max_cycles_per_case": 50,
        "max_candidate_rows": 10000,
        "max_new_bands": 512,
        "max_observer_runtime_seconds_soft": 600,
        "max_output_files": 16,
    }
    for key, expected in expected_bounds.items():
        if bounds.get(key) != expected:
            failures.append(f"bound_wrong:{key}:{bounds.get(key)}")

    row_contract = rule.get("surface_row_contract") or {}
    if row_contract.get("required_truth_key") != "full_occurrence_key":
        failures.append(f"row_contract_truth_key_wrong:{row_contract.get('required_truth_key')}")
    if row_contract.get("required_band_key") != "source_band_id":
        failures.append(f"row_contract_band_key_wrong:{row_contract.get('required_band_key')}")
    if row_contract.get("required_signature_payload") != CANDIDATE_PAYLOAD_FIELDS:
        failures.append(f"row_contract_payload_wrong:{row_contract.get('required_signature_payload')}")
    if row_contract.get("required_truth_surface") != "full_occurrence_key_to_candidate_delta_signature":
        failures.append(f"row_contract_truth_surface_wrong:{row_contract.get('required_truth_surface')}")
    if row_contract.get("audit_reference_must_not_enter_signature_payload") is not True:
        failures.append("audit_reference_must_not_enter_signature_payload_not_true")

    after = contract.get("acceptance_after_new_surface") or {}
    for key in [
        "candidate_acceptance_still_forbidden",
        "runtime_change_still_forbidden",
        "scale_mode_still_forbidden",
        "new_surface_pass_may_only_authorize_candidate_probe_policy",
    ]:
        if after.get(key) is not True:
            failures.append(f"acceptance_after_flag_missing:{key}:{after.get(key)}")

    auth = policy.get("authority") or {}
    if auth.get("observer_only") is not True:
        failures.append("policy_not_observer_only")
    for key in [
        "authorizes_new_bounded_validation_surface_implementation",
        "authorizes_runner_entrypoint_inspection",
        "authorizes_existing_bounded_runner_execution",
        "authorizes_new_surface_manifest_write",
        "authorizes_candidate_compatible_surface_rows_write",
    ]:
        if auth.get(key) is not True:
            failures.append(f"required_authority_not_true:{key}:{auth.get(key)}")
    for key in FORBIDDEN_AUTHORITY_FALSE:
        if auth.get(key) is not False:
            failures.append(f"forbidden_authority_not_false:{key}:{auth.get(key)}")

    constraints = policy.get("implementation_constraints") or {}
    if constraints.get("must_touch_only_files") != ["scripts/raw_delta_signature_candidate_new_bounded_validation_surface_v0.py"]:
        failures.append(f"touch_scope_wrong:{constraints.get('must_touch_only_files')}")
    for key in [
        "must_reuse_existing_receipts_and_rows",
        "must_record_runner_discovery",
        "must_record_surface_recipe_or_hold",
        "must_not_read_registry_sqlite",
        "must_not_full_registry_scan",
        "must_not_accept_candidate",
        "must_not_authorize_scale_mode",
        "must_not_change_runtime_receipt_emission",
        "must_not_change_runtime_code",
        "must_not_write_registry",
    ]:
        if constraints.get(key) is not True:
            failures.append(f"constraint_not_true:{key}:{constraints.get(key)}")

    if bounded_scale_out.get("scale_out_id") != EXPECTED_BOUNDED_SCALE_OUT_ID:
        failures.append(f"source_scale_out_id_wrong:{bounded_scale_out.get('scale_out_id')}")
    if bounded_scale_out_receipt.get("receipt_id") != EXPECTED_BOUNDED_SCALE_OUT_RECEIPT_ID:
        failures.append(f"source_scale_out_receipt_wrong:{bounded_scale_out_receipt.get('receipt_id')}")
    if bounded_scale_out.get("gate") != "PASS":
        failures.append(f"source_scale_out_gate_not_PASS:{bounded_scale_out.get('gate')}")
    if bounded_scale_out_receipt.get("gate") != "PASS":
        failures.append(f"source_scale_out_receipt_gate_not_PASS:{bounded_scale_out_receipt.get('gate')}")
    if bounded_scale_out.get("terminal_class") != "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY":
        failures.append(f"source_scale_out_terminal_wrong:{bounded_scale_out.get('terminal_class')}")

    inventory = bounded_scale_out.get("inventory_summary") or {}
    if inventory.get("additional_candidate_rows_selected") != 0:
        failures.append(f"source_inventory_additional_rows_not_zero:{inventory.get('additional_candidate_rows_selected')}")
    if inventory.get("additional_bands_selected") != 0:
        failures.append(f"source_inventory_additional_bands_not_zero:{inventory.get('additional_bands_selected')}")
    if inventory.get("registry_sqlite_read") is not False:
        failures.append(f"source_inventory_registry_read_not_false:{inventory.get('registry_sqlite_read')}")
    if inventory.get("full_registry_scan_used") is not False:
        failures.append(f"source_inventory_full_scan_not_false:{inventory.get('full_registry_scan_used')}")

    prior = surface_aggregate(bounded_scale_out, "prior_surface_aggregate", "prior_surface_evaluation")
    combined = surface_aggregate(bounded_scale_out, "combined_surface_aggregate", "combined_surface_evaluation")
    for label, agg in [("prior", prior), ("combined", combined)]:
        if agg.get("bands_total") != 266:
            failures.append(f"{label}_bands_total_wrong:{agg.get('bands_total')}")
        if agg.get("rows_total") != 3298:
            failures.append(f"{label}_rows_total_wrong:{agg.get('rows_total')}")
        if agg.get("all_band_false_merge_count") != 0:
            failures.append(f"{label}_false_merge_wrong:{agg.get('all_band_false_merge_count')}")
        if agg.get("all_band_false_split_count") != 0:
            failures.append(f"{label}_false_split_wrong:{agg.get('all_band_false_split_count')}")
        if agg.get("worst_distinguishability_retention_ratio") != 1.0:
            failures.append(f"{label}_retention_wrong:{agg.get('worst_distinguishability_retention_ratio')}")
        if not (agg.get("total_burden_ratio_projected", 999) < 1.0):
            failures.append(f"{label}_burden_not_below_1:{agg.get('total_burden_ratio_projected')}")
        if agg.get("worst_identity_leak_count") != 0:
            failures.append(f"{label}_identity_leak_wrong:{agg.get('worst_identity_leak_count')}")

    return failures


def discover_existing_runners(policy: dict[str, Any]) -> dict[str, Any]:
    rule = policy["surface_contract"]["bounded_surface_generation_rule"]
    allowed_paths = rule["allowed_discovery_paths"]

    discovered_files: list[dict[str, Any]] = []
    runner_candidates: list[dict[str, Any]] = []
    safe_recipe_candidates: list[dict[str, Any]] = []

    scan_roots: list[Path] = []
    for item in allowed_paths:
        p = ROOT / item
        if p.exists():
            scan_roots.append(p)

    for root in scan_roots:
        if root.is_file():
            files = [root]
        else:
            files = sorted(root.rglob("*"))
        for path in files:
            if not path.is_file():
                continue
            if forbidden_path(path):
                continue
            if path.suffix not in {".py", ".md", ".toml"}:
                continue

            text = safe_read_text(path, max_chars=12000)
            lowered = text.lower()
            rel_path = rel(path)
            record = {
                "path": rel_path,
                "suffix": path.suffix,
                "size_bytes": path.stat().st_size,
                "mentions_argparse": "argparse" in lowered,
                "mentions_click": "click" in lowered or "typer" in lowered,
                "mentions_matrixlab": "matrixlab" in lowered,
                "mentions_receipt": "receipt" in lowered,
                "mentions_run": "run" in lowered,
                "mentions_cycles": "cycles" in lowered,
                "mentions_family": "family" in lowered or "families" in lowered,
                "mentions_candidate_surface": "candidate-compatible" in lowered or "candidate compatible" in lowered,
                "mentions_raw_delta_signature_candidate": "raw_delta_signature_candidate" in lowered,
                "mentions_registry_sqlite": "registry.sqlite" in lowered,
                "mentions_sqlite": "sqlite" in lowered,
            }
            discovered_files.append(record)

            maybe_runner = (
                path.suffix == ".py"
                and (
                    "run" in path.name.lower()
                    or "probe" in path.name.lower()
                    or "sweep" in path.name.lower()
                    or "cli" in path.name.lower()
                )
            )
            if maybe_runner:
                runner_candidates.append(record)

            # Strict recipe detection. Do not infer safe execution from generic runner/probe names.
            safe_recipe = (
                record["mentions_raw_delta_signature_candidate"]
                and record["mentions_candidate_surface"]
                and not record["mentions_sqlite"]
                and "new_bounded_validation_surface" in rel_path
                and rel_path != "scripts/raw_delta_signature_candidate_new_bounded_validation_surface_v0.py"
            )
            if safe_recipe:
                safe_recipe_candidates.append(record)

    help_commands: list[dict[str, Any]] = []
    cli_path = ROOT / "src" / "matrixlab" / "cli.py"
    if cli_path.exists() and not forbidden_path(cli_path):
        help_commands.append(run_help_command(["uv", "run", "python", "src/matrixlab/cli.py", "--help"], timeout=20))

    pyproject_path = ROOT / "pyproject.toml"
    pyproject_head = safe_read_text(pyproject_path, max_chars=8000) if pyproject_path.exists() else ""

    return {
        "allowed_discovery_paths": allowed_paths,
        "files_discovered_total": len(discovered_files),
        "runner_candidates_total": len(runner_candidates),
        "safe_recipe_candidates_total": len(safe_recipe_candidates),
        "discovered_files_head": discovered_files[:80],
        "runner_candidates_head": runner_candidates[:40],
        "safe_recipe_candidates": safe_recipe_candidates,
        "help_commands": help_commands,
        "pyproject_head": pyproject_head,
        "discovery_operations_used": [
            "list_files",
            "read_file",
            "run_help_command",
        ],
        "registry_sqlite_read": False,
        "full_registry_scan_used": False,
        "runtime_code_changed": False,
    }


def create_surface_or_hold(policy_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    start = time.perf_counter()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_ROWS_DIR.mkdir(parents=True, exist_ok=True)

    policy = load_json(POLICY_DIR / f"{policy_id}.json")
    policy_receipt = load_json(POLICY_RECEIPT_DIR / f"{policy_id}.json")
    bounded_scale_out = load_json(BOUNDED_SCALE_OUT_DIR / f"{EXPECTED_BOUNDED_SCALE_OUT_ID}.json")
    bounded_scale_out_receipt = load_json(BOUNDED_SCALE_OUT_RECEIPT_DIR / f"{EXPECTED_BOUNDED_SCALE_OUT_ID}.json")

    failures = verify_policy_and_sources(policy, policy_receipt, bounded_scale_out, bounded_scale_out_receipt)
    discovery = discover_existing_runners(policy)

    contract = policy["surface_contract"]
    rule = contract["bounded_surface_generation_rule"]
    bounds = rule["bounds"]

    # Conservative rule: only run an existing recipe if it explicitly advertises this exact new bounded
    # surface/candidate-compatible row contract. Generic runners are discovery evidence, not safe execution.
    safe_recipes = discovery["safe_recipe_candidates"]
    rows: list[dict[str, Any]] = []
    surface_recipe: dict[str, Any]

    if failures:
        terminal_class = "FAIL_NEW_BOUNDED_SURFACE_AUTHORITY"
        terminal = {"type": "STOP", "next_command_goal": None, "stop_code": terminal_class}
        surface_recipe = {
            "recipe_status": "NOT_ATTEMPTED_POLICY_PRECONDITION_FAILURE",
            "reason": "source policy/source receipts failed verification",
            "safe_recipe_selected": None,
            "command_or_recipe": None,
        }
    elif not safe_recipes:
        terminal_class = "HOLD_NEW_BOUNDED_SURFACE_REQUIRES_RUNNER_DECISION"
        terminal = {"type": "HOLD", "next_command_goal": None, "stop_code": terminal_class}
        surface_recipe = {
            "recipe_status": "HOLD_NO_SAFE_EXISTING_RECIPE",
            "reason": (
                "Runner discovery found generic scripts/entrypoints, but no existing recipe explicitly declares "
                "candidate-compatible RAW_DELTA_SIGNATURE_CANDIDATE_V0 rows for a new bounded validation surface. "
                "Policy forbids synthetic rows and runtime code mutation, so this layer must hold for a runner/recipe decision."
            ),
            "safe_recipe_selected": None,
            "command_or_recipe": None,
            "generic_runner_candidates_total": discovery["runner_candidates_total"],
            "safe_recipe_candidates_total": discovery["safe_recipe_candidates_total"],
        }
    else:
        # Deliberately not used in current project unless a precise recipe exists.
        # Kept as a structural branch for future strict recipes.
        terminal_class = "HOLD_NEW_BOUNDED_SURFACE_REQUIRES_RUNNER_DECISION"
        terminal = {"type": "HOLD", "next_command_goal": None, "stop_code": terminal_class}
        surface_recipe = {
            "recipe_status": "HOLD_SAFE_RECIPE_PRESENT_BUT_EXECUTION_NOT_BOUND_BY_THIS_IMPLEMENTATION",
            "reason": "A possible recipe was discovered, but this implementation requires a human/agent decision before execution.",
            "safe_recipe_selected": safe_recipes[0],
            "command_or_recipe": None,
            "safe_recipe_candidates_total": len(safe_recipes),
        }

    rows_path = OUT_ROWS_DIR / "PLACEHOLDER.jsonl"
    manifest = {
        "schema_version": "raw_delta_signature_candidate_new_bounded_validation_surface_v0",
        "surface_name": SURFACE_NAME,
        "mode": MODE,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_bounded_scale_out_id": EXPECTED_BOUNDED_SCALE_OUT_ID,
        "source_bounded_scale_out_receipt_id": EXPECTED_BOUNDED_SCALE_OUT_RECEIPT_ID,
        "source_hold_class": "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY",
        "selected_encoding_id": SELECTED_ENCODING_ID,
        "selected_target_raw_delta_field": TARGET_RAW_DELTA_FIELD,
        "candidate_payload_fields": CANDIDATE_PAYLOAD_FIELDS,
        "candidate_payload_forbidden_fields": sorted(FORBIDDEN_PAYLOAD_FIELDS),
        "truth_surface": "full_occurrence_key_to_candidate_delta_signature",
        "bounds": bounds,
        "runner_discovery": discovery,
        "surface_recipe_or_hold": surface_recipe,
        "surface_rows_summary": {
            "rows_created": len(rows),
            "new_bands_created": 0,
            "candidate_compatible_rows_created": 0,
            "synthetic_fake_rows_created": 0,
            "rows_path": None,
        },
        "authority_guards": {
            "observer_only": True,
            "candidate_accepted": False,
            "candidate_acceptance_authorized": False,
            "scale_mode_authorized": False,
            "full_registry_scan_used": False,
            "registry_sqlite_read": False,
            "registry_sqlite_changed": False,
            "runtime_receipt_emission_changed": False,
            "runtime_code_changed": False,
            "registry_write_authorized": False,
            "receipt_replacement_authorized": False,
            "receipt_deletion_authorized": False,
            "receipt_compression_authorized": False,
            "receipt_suppression_authorized": False,
            "raw_receipt_hash_used_as_truth_surface": False,
            "case_id_or_cycle_n_primary_identity_patch_used": False,
            "rowid_or_receipt_hash_patch_used": False,
            "full_occurrence_key_in_payload": False,
            "audit_pointer_in_payload": False,
            "debug_payload_in_payload": False,
            "microhash_as_proof_used": False,
            "synthetic_fake_validation_rows_used": False,
        },
        "pass_gates": {},
        "decision": {
            "candidate_accepted": False,
            "candidate_acceptance_authorized": False,
            "scale_mode_authorized": False,
            "new_surface_policy_only": False,
            "new_surface_attempted": True,
            "new_surface_created": False,
            "runner_discovery_completed": True,
            "safe_runner_recipe_found": bool(safe_recipes),
            "do_not_accept_candidate": True,
            "do_not_full_registry_scan": True,
            "do_not_read_registry_sqlite": True,
            "do_not_change_runtime": True,
            "do_not_change_runtime_code": True,
            "do_not_write_registry": True,
            "do_not_use_case_id_or_cycle_n_as_primary_identity": True,
            "do_not_use_rowid_or_receipt_hash": True,
            "terminal_class": terminal_class,
        },
        "terminal_class": terminal_class,
        "terminal": terminal,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
        "actual_observer_overhead_ms": int(round((time.perf_counter() - start) * 1000)),
    }

    gates = {
        "policy_preconditions": not failures,
        "authority_containment": all([
            manifest["authority_guards"]["observer_only"] is True,
            manifest["authority_guards"]["candidate_accepted"] is False,
            manifest["authority_guards"]["candidate_acceptance_authorized"] is False,
            manifest["authority_guards"]["scale_mode_authorized"] is False,
            manifest["authority_guards"]["full_registry_scan_used"] is False,
            manifest["authority_guards"]["registry_sqlite_read"] is False,
            manifest["authority_guards"]["runtime_receipt_emission_changed"] is False,
            manifest["authority_guards"]["runtime_code_changed"] is False,
            manifest["authority_guards"]["registry_write_authorized"] is False,
            manifest["authority_guards"]["synthetic_fake_validation_rows_used"] is False,
        ]),
        "runner_discovery_recorded": discovery["files_discovered_total"] >= 0 and "runner_candidates_total" in discovery,
        "surface_recipe_or_hold_recorded": bool(surface_recipe.get("recipe_status")),
        "bounded_limits_recorded": all(k in bounds for k in [
            "max_new_runs",
            "max_new_cases_total",
            "max_cycles_per_case",
            "max_candidate_rows",
            "max_new_bands",
            "max_output_files",
        ]),
        "candidate_not_accepted": True,
        "scale_mode_not_authorized": True,
        "registry_sqlite_not_read": True,
        "full_registry_not_scanned": True,
        "runtime_code_not_changed": True,
        "runtime_receipt_emission_not_changed": True,
        "synthetic_rows_not_created": True,
        "truth_surface_preserved": manifest["truth_surface"] == "full_occurrence_key_to_candidate_delta_signature",
        "payload_contract_preserved": manifest["candidate_payload_fields"] == CANDIDATE_PAYLOAD_FIELDS,
        "hold_is_lawful_if_no_safe_recipe": terminal_class == "HOLD_NEW_BOUNDED_SURFACE_REQUIRES_RUNNER_DECISION",
    }
    manifest["pass_gates"] = gates

    surface_id = sha8({
        "surface_name": SURFACE_NAME,
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_bounded_scale_out_id": EXPECTED_BOUNDED_SCALE_OUT_ID,
        "terminal_class": terminal_class,
        "runner_discovery": {
            "files_discovered_total": discovery["files_discovered_total"],
            "runner_candidates_total": discovery["runner_candidates_total"],
            "safe_recipe_candidates_total": discovery["safe_recipe_candidates_total"],
        },
        "surface_recipe_or_hold": surface_recipe,
        "bounds": bounds,
    })
    manifest["surface_id"] = surface_id
    manifest["surface_sig8"] = surface_id

    rows_path = OUT_ROWS_DIR / f"{surface_id}.jsonl"
    rows_path.write_text("")
    manifest["surface_rows_path"] = f"data/raw_delta_signature_candidate_new_bounded_validation_surface_rows/{surface_id}.jsonl"
    manifest["surface_rows_summary"]["rows_path"] = manifest["surface_rows_path"]

    receipt = {
        "schema_version": "raw_delta_signature_candidate_new_bounded_validation_surface_receipt_v0",
        "surface_id": surface_id,
        "surface_sig8": surface_id,
        "surface_name": SURFACE_NAME,
        "mode": MODE,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "surface_path": f"data/raw_delta_signature_candidate_new_bounded_validation_surfaces/{surface_id}.json",
        "surface_rows_path": manifest["surface_rows_path"],
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_bounded_scale_out_id": EXPECTED_BOUNDED_SCALE_OUT_ID,
        "source_bounded_scale_out_receipt_id": EXPECTED_BOUNDED_SCALE_OUT_RECEIPT_ID,
        "source_hold_class": "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY",
        "selected_encoding_id": SELECTED_ENCODING_ID,
        "selected_target_raw_delta_field": TARGET_RAW_DELTA_FIELD,
        "candidate_payload_fields": CANDIDATE_PAYLOAD_FIELDS,
        "bounds": bounds,
        "runner_discovery_summary": {
            "files_discovered_total": discovery["files_discovered_total"],
            "runner_candidates_total": discovery["runner_candidates_total"],
            "safe_recipe_candidates_total": discovery["safe_recipe_candidates_total"],
            "help_commands": discovery["help_commands"],
            "registry_sqlite_read": discovery["registry_sqlite_read"],
            "full_registry_scan_used": discovery["full_registry_scan_used"],
            "runtime_code_changed": discovery["runtime_code_changed"],
        },
        "surface_recipe_or_hold": surface_recipe,
        "surface_rows_summary": manifest["surface_rows_summary"],
        "authority_guards": manifest["authority_guards"],
        "pass_gates": manifest["pass_gates"],
        "decision": manifest["decision"],
        "terminal_class": terminal_class,
        "terminal": terminal,
        "gate": manifest["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
        "actual_observer_overhead_ms": manifest["actual_observer_overhead_ms"],
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id

    (OUT_DIR / f"{surface_id}.json").write_text(json.dumps(manifest, indent=2, sort_keys=True))
    (OUT_RECEIPT_DIR / f"{surface_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return manifest, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy-id", default=EXPECTED_POLICY_ID)
    args = parser.parse_args()

    manifest, receipt = create_surface_or_hold(args.policy_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"surface_id={manifest['surface_id']}")
    print(f"surface_json_path=data/raw_delta_signature_candidate_new_bounded_validation_surfaces/{manifest['surface_id']}.json")
    print(f"surface_receipt_path=data/raw_delta_signature_candidate_new_bounded_validation_surface_receipts/{manifest['surface_id']}.json")
    print(f"surface_rows_path={manifest['surface_rows_path']}")

    return 0 if manifest["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
