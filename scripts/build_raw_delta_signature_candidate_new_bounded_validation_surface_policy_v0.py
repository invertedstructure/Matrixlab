#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

BOUNDED_SCALE_OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_bounded_scale_outs"
BOUNDED_SCALE_OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_bounded_scale_out_receipts"
BOUNDED_SCALE_OUT_POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_bounded_scale_out_policies"
BOUNDED_SCALE_OUT_POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_bounded_scale_out_policy_receipts"
SCALE_REVIEW_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_scale_review_receipts"
CANDIDATE_PROBE_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_probe_receipts"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_validation_surface_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_validation_surface_policy_receipts"

EXPECTED_BOUNDED_SCALE_OUT_ID = "2b44b1fd"
EXPECTED_BOUNDED_SCALE_OUT_RECEIPT_ID = "f67b629b"
EXPECTED_BOUNDED_SCALE_OUT_POLICY_ID = "189aab7f"
EXPECTED_BOUNDED_SCALE_OUT_POLICY_RECEIPT_ID = "7f51bc70"
EXPECTED_SCALE_REVIEW_ID = "6539838c"
EXPECTED_SCALE_REVIEW_RECEIPT_ID = "0c85a6f1"
EXPECTED_CANDIDATE_PROBE_ID = "6a33c978"
EXPECTED_CANDIDATE_PROBE_RECEIPT_ID = "99c90fe3"

POLICY_NAME = "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_NEW_BOUNDED_VALIDATION_SURFACE_POLICY_V0"
SURFACE_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_NEW_BOUNDED_VALIDATION_SURFACE_V0"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"
NEXT_COMMAND_GOAL = "IMPLEMENT_RAW_DELTA_SIGNATURE_CANDIDATE_NEW_BOUNDED_VALIDATION_SURFACE_V0"

SELECTED_ENCODING_ID = "raw_decimal_sig6"
TARGET_RAW_DELTA_FIELD = "compression_ratio"

CANDIDATE_PAYLOAD_FIELDS = [
    "cv",
    "state_hash_before",
    "move_id",
    "state_hash_after",
    "raw_compression_ratio_sig6",
]

FORBIDDEN_PAYLOAD_FIELDS = [
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
]

FORBIDDEN_AUTHORITY_FLAGS = [
    "authorizes_candidate_acceptance",
    "authorizes_scale_mode",
    "authorizes_full_registry_scan",
    "authorizes_registry_sqlite_read",
    "authorizes_runtime_receipt_emission_change",
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


def surface_aggregate(source: dict[str, Any], flat_key: str, nested_key: str) -> dict[str, Any]:
    """Read either receipt-style flat aggregate or full-artifact nested aggregate."""
    flat = source.get(flat_key)
    if isinstance(flat, dict) and flat:
        return flat
    nested = source.get(nested_key)
    if isinstance(nested, dict):
        agg = nested.get("aggregate")
        if isinstance(agg, dict) and agg:
            return agg
    return {}


def verify_sources(
    bounded_scale_out: dict[str, Any],
    bounded_scale_out_receipt: dict[str, Any],
    bounded_scale_out_policy: dict[str, Any],
    bounded_scale_out_policy_receipt: dict[str, Any],
    scale_review_receipt: dict[str, Any],
    candidate_probe_receipt: dict[str, Any],
) -> list[str]:
    failures: list[str] = []

    if bounded_scale_out.get("scale_out_id") != EXPECTED_BOUNDED_SCALE_OUT_ID:
        failures.append(f"scale_out_id_wrong:{bounded_scale_out.get('scale_out_id')}")
    if bounded_scale_out_receipt.get("receipt_id") != EXPECTED_BOUNDED_SCALE_OUT_RECEIPT_ID:
        failures.append(f"scale_out_receipt_id_wrong:{bounded_scale_out_receipt.get('receipt_id')}")
    if bounded_scale_out.get("gate") != "PASS":
        failures.append(f"scale_out_gate_not_PASS:{bounded_scale_out.get('gate')}")
    if bounded_scale_out_receipt.get("gate") != "PASS":
        failures.append(f"scale_out_receipt_gate_not_PASS:{bounded_scale_out_receipt.get('gate')}")
    if bounded_scale_out.get("mode") != "OUTER_OBSERVER_ONLY":
        failures.append(f"scale_out_mode_wrong:{bounded_scale_out.get('mode')}")
    if bounded_scale_out.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"scale_out_candidate_design_wrong:{bounded_scale_out.get('candidate_design_id')}")
    if bounded_scale_out.get("terminal_class") != "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY":
        failures.append(f"scale_out_terminal_class_wrong:{bounded_scale_out.get('terminal_class')}")
    if bounded_scale_out.get("terminal", {}).get("type") != "HOLD":
        failures.append(f"scale_out_terminal_type_wrong:{bounded_scale_out.get('terminal', {}).get('type')}")
    if bounded_scale_out.get("terminal", {}).get("stop_code") != "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY":
        failures.append(f"scale_out_stop_code_wrong:{bounded_scale_out.get('terminal', {}).get('stop_code')}")
    if bounded_scale_out.get("terminal", {}).get("next_command_goal") is not None:
        failures.append(f"scale_out_next_goal_not_none:{bounded_scale_out.get('terminal', {}).get('next_command_goal')}")

    addl = bounded_scale_out.get("additional_surface_summary") or {}
    if addl.get("additional_inventory_selected") is not False:
        failures.append(f"additional_inventory_selected_not_false:{addl.get('additional_inventory_selected')}")
    if addl.get("additional_candidate_rows_selected") != 0:
        failures.append(f"additional_rows_not_zero:{addl.get('additional_candidate_rows_selected')}")
    if addl.get("new_bands_evaluated") != 0:
        failures.append(f"new_bands_not_zero:{addl.get('new_bands_evaluated')}")

    inventory = bounded_scale_out.get("inventory_summary") or {}
    if inventory.get("registry_sqlite_read") is not False:
        failures.append(f"inventory_registry_sqlite_read_not_false:{inventory.get('registry_sqlite_read')}")
    if inventory.get("full_registry_scan_used") is not False:
        failures.append(f"inventory_full_registry_scan_not_false:{inventory.get('full_registry_scan_used')}")
    if inventory.get("prior_candidate_rows_replayed") != 3298:
        failures.append(f"prior_rows_replayed_wrong:{inventory.get('prior_candidate_rows_replayed')}")
    if inventory.get("prior_bands_replayed") != 266:
        failures.append(f"prior_bands_replayed_wrong:{inventory.get('prior_bands_replayed')}")
    if inventory.get("additional_candidate_rows_selected") != 0:
        failures.append(f"inventory_additional_rows_not_zero:{inventory.get('additional_candidate_rows_selected')}")
    if inventory.get("additional_bands_selected") != 0:
        failures.append(f"inventory_additional_bands_not_zero:{inventory.get('additional_bands_selected')}")

    prior = surface_aggregate(bounded_scale_out, "prior_surface_aggregate", "prior_surface_evaluation")
    combined = surface_aggregate(bounded_scale_out, "combined_surface_aggregate", "combined_surface_evaluation")
    for label, agg in [("prior", prior), ("combined", combined)]:
        expected_exact = {
            "bands_total": 266,
            "bands_passed": 266,
            "bands_failed": 0,
            "rows_total": 3298,
            "all_band_false_merge_count": 0,
            "all_band_false_split_count": 0,
            "all_band_burden_regression_count": 0,
            "worst_false_merge_count": 0,
            "worst_false_split_count": 0,
            "worst_collision_count": 0,
            "worst_distinguishability_retention_ratio": 1.0,
            "worst_identity_leak_count": 0,
            "worst_source_surface_regression_count": 0,
            "worst_audit_recoverability_failures": 0,
            "total_full_receipt_bytes": 2870426,
            "total_projected_plus_signature_payload_bytes": 1084898,
        }
        for key, expected in expected_exact.items():
            if agg.get(key) != expected:
                failures.append(f"{label}_aggregate_{key}_wrong:{agg.get(key)}")
        if not (agg.get("total_burden_ratio_projected", 999) < 1.0):
            failures.append(f"{label}_aggregate_burden_not_below_1:{agg.get('total_burden_ratio_projected')}")
        if not (agg.get("worst_burden_ratio_projected", 999) < 1.0):
            failures.append(f"{label}_aggregate_worst_burden_not_below_1:{agg.get('worst_burden_ratio_projected')}")

    pass_gates = bounded_scale_out.get("pass_gates") or {}
    for key in [
        "authority_containment",
        "burden_reduction_or_hold",
        "candidate_not_accepted",
        "inventory_defined_before_evaluation",
        "larger_surface_or_hold",
        "no_false_merge",
        "no_false_split",
        "no_identity_leak",
        "policy_preconditions",
        "prior_266_band_surface_replayed",
        "scale_mode_not_authorized",
        "source_surface_clean_or_hold",
        "truth_surface",
    ]:
        if pass_gates.get(key) is not True:
            failures.append(f"scale_out_pass_gate_not_true:{key}:{pass_gates.get(key)}")

    guards = bounded_scale_out.get("authority_guards") or {}
    if guards.get("observer_only") is not True:
        failures.append("scale_out_not_observer_only")
    for key in [
        "candidate_accepted",
        "candidate_acceptance_authorized",
        "scale_mode_authorized",
        "full_registry_scan_used",
        "registry_sqlite_read",
        "registry_sqlite_changed",
        "runtime_receipt_emission_changed",
        "registry_write_authorized",
        "receipt_replacement_authorized",
        "receipt_deletion_authorized",
        "receipt_compression_authorized",
        "receipt_suppression_authorized",
        "raw_receipt_hash_used_as_truth_surface",
        "case_id_or_cycle_n_primary_identity_patch_used",
        "rowid_or_receipt_hash_patch_used",
        "full_occurrence_key_in_payload",
        "audit_pointer_in_payload",
        "debug_payload_in_payload",
        "microhash_as_proof_used",
    ]:
        if guards.get(key) is not False:
            failures.append(f"scale_out_guard_not_false:{key}:{guards.get(key)}")

    decision = bounded_scale_out.get("decision") or {}
    if decision.get("terminal_class") != "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY":
        failures.append(f"decision_terminal_class_wrong:{decision.get('terminal_class')}")
    if decision.get("additional_inventory_selected") is not False:
        failures.append(f"decision_additional_inventory_not_false:{decision.get('additional_inventory_selected')}")
    for key in [
        "bounded_scale_out_only",
        "do_not_accept_candidate",
        "do_not_change_runtime",
        "do_not_full_registry_scan",
        "do_not_read_registry_sqlite",
        "do_not_use_case_id_or_cycle_n_as_primary_identity",
        "do_not_use_rowid_or_receipt_hash",
        "do_not_write_registry",
    ]:
        if decision.get(key) is not True:
            failures.append(f"decision_flag_not_true:{key}:{decision.get(key)}")
    for key in [
        "candidate_accepted",
        "candidate_acceptance_authorized",
        "scale_mode_authorized",
    ]:
        if decision.get(key) is not False:
            failures.append(f"decision_flag_not_false:{key}:{decision.get(key)}")

    if bounded_scale_out_policy.get("policy_id") != EXPECTED_BOUNDED_SCALE_OUT_POLICY_ID:
        failures.append(f"scale_out_policy_id_wrong:{bounded_scale_out_policy.get('policy_id')}")
    if bounded_scale_out_policy_receipt.get("receipt_id") != EXPECTED_BOUNDED_SCALE_OUT_POLICY_RECEIPT_ID:
        failures.append(f"scale_out_policy_receipt_id_wrong:{bounded_scale_out_policy_receipt.get('receipt_id')}")
    if bounded_scale_out_policy.get("gate") != "PASS":
        failures.append(f"scale_out_policy_gate_not_PASS:{bounded_scale_out_policy.get('gate')}")

    scale_out_contract = bounded_scale_out_policy.get("scale_out_contract") or {}
    scale_out_acceptance = scale_out_contract.get("acceptance_after_scale_out") or {}
    if scale_out_acceptance.get("candidate_acceptance_still_forbidden") is not True:
        failures.append("scale_out_policy_acceptance_not_forbidden")
    if scale_out_acceptance.get("runtime_change_still_forbidden") is not True:
        failures.append("scale_out_policy_runtime_change_not_forbidden")
    if scale_out_contract.get("truth_surface") != "full_occurrence_key_to_candidate_delta_signature":
        failures.append(f"scale_out_policy_truth_surface_wrong:{scale_out_contract.get('truth_surface')}")

    if scale_review_receipt.get("review_id") != EXPECTED_SCALE_REVIEW_ID:
        failures.append(f"scale_review_id_wrong:{scale_review_receipt.get('review_id')}")
    if scale_review_receipt.get("receipt_id") != EXPECTED_SCALE_REVIEW_RECEIPT_ID:
        failures.append(f"scale_review_receipt_id_wrong:{scale_review_receipt.get('receipt_id')}")
    if scale_review_receipt.get("gate") != "PASS":
        failures.append(f"scale_review_gate_not_PASS:{scale_review_receipt.get('gate')}")
    if scale_review_receipt.get("terminal_class") != "ADVANCE_TO_BOUNDED_SCALE_OUT_POLICY":
        failures.append(f"scale_review_terminal_wrong:{scale_review_receipt.get('terminal_class')}")

    if candidate_probe_receipt.get("probe_id") != EXPECTED_CANDIDATE_PROBE_ID:
        failures.append(f"candidate_probe_id_wrong:{candidate_probe_receipt.get('probe_id')}")
    if candidate_probe_receipt.get("receipt_id") != EXPECTED_CANDIDATE_PROBE_RECEIPT_ID:
        failures.append(f"candidate_probe_receipt_id_wrong:{candidate_probe_receipt.get('receipt_id')}")
    if candidate_probe_receipt.get("gate") != "PASS":
        failures.append(f"candidate_probe_gate_not_PASS:{candidate_probe_receipt.get('gate')}")
    if candidate_probe_receipt.get("terminal_decision") != "PASS_RAW_DELTA_SIGNATURE_CANDIDATE_BOUNDED_PROBE":
        failures.append(f"candidate_probe_terminal_wrong:{candidate_probe_receipt.get('terminal_decision')}")

    return failures


def build_policy(source_scale_out_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    bounded_scale_out = load_json(BOUNDED_SCALE_OUT_DIR / f"{source_scale_out_id}.json")
    bounded_scale_out_receipt = load_json(BOUNDED_SCALE_OUT_RECEIPT_DIR / f"{source_scale_out_id}.json")
    bounded_scale_out_policy = load_json(BOUNDED_SCALE_OUT_POLICY_DIR / f"{EXPECTED_BOUNDED_SCALE_OUT_POLICY_ID}.json")
    bounded_scale_out_policy_receipt = load_json(BOUNDED_SCALE_OUT_POLICY_RECEIPT_DIR / f"{EXPECTED_BOUNDED_SCALE_OUT_POLICY_ID}.json")
    scale_review_receipt = load_json(SCALE_REVIEW_RECEIPT_DIR / f"{EXPECTED_SCALE_REVIEW_ID}.json")
    candidate_probe_receipt = load_json(CANDIDATE_PROBE_RECEIPT_DIR / f"{EXPECTED_CANDIDATE_PROBE_ID}.json")

    failures = verify_sources(
        bounded_scale_out,
        bounded_scale_out_receipt,
        bounded_scale_out_policy,
        bounded_scale_out_policy_receipt,
        scale_review_receipt,
        candidate_probe_receipt,
    )

    prior_agg = surface_aggregate(bounded_scale_out, "prior_surface_aggregate", "prior_surface_evaluation")
    combined_agg = surface_aggregate(bounded_scale_out, "combined_surface_aggregate", "combined_surface_evaluation")
    inventory = bounded_scale_out.get("inventory_summary") or {}

    surface_contract = {
        "surface_name": SURFACE_NAME,
        "surface_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_bounded_scale_out_id": EXPECTED_BOUNDED_SCALE_OUT_ID,
        "source_bounded_scale_out_receipt_id": EXPECTED_BOUNDED_SCALE_OUT_RECEIPT_ID,
        "source_hold_class": "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY",
        "hold_reason": "Existing file-backed inventory contained no additional candidate-compatible rows beyond prior 266-band replay.",
        "selected_encoding_id": SELECTED_ENCODING_ID,
        "selected_target_raw_delta_field": TARGET_RAW_DELTA_FIELD,
        "candidate_payload_fields": CANDIDATE_PAYLOAD_FIELDS,
        "candidate_payload_forbidden_fields": FORBIDDEN_PAYLOAD_FIELDS,
        "truth_surface": "full_occurrence_key_to_candidate_delta_signature",
        "source_evidence_summary": {
            "prior_surface": {
                "bands_total": prior_agg.get("bands_total"),
                "rows_total": prior_agg.get("rows_total"),
                "false_merges": prior_agg.get("all_band_false_merge_count"),
                "false_splits": prior_agg.get("all_band_false_split_count"),
                "retention": prior_agg.get("worst_distinguishability_retention_ratio"),
                "burden_ratio": prior_agg.get("total_burden_ratio_projected"),
            },
            "scale_out_inventory": {
                "candidate_files_total_after_exclusions": inventory.get("candidate_files_total_after_exclusions"),
                "additional_candidate_rows_selected": inventory.get("additional_candidate_rows_selected"),
                "additional_bands_selected": inventory.get("additional_bands_selected"),
                "registry_sqlite_read": inventory.get("registry_sqlite_read"),
                "full_registry_scan_used": inventory.get("full_registry_scan_used"),
            },
            "combined_surface": {
                "bands_total": combined_agg.get("bands_total"),
                "rows_total": combined_agg.get("rows_total"),
                "false_merges": combined_agg.get("all_band_false_merge_count"),
                "false_splits": combined_agg.get("all_band_false_split_count"),
                "retention": combined_agg.get("worst_distinguishability_retention_ratio"),
                "burden_ratio": combined_agg.get("total_burden_ratio_projected"),
            },
        },
        "new_surface_authorized_actions": {
            "inspect_existing_runner_entrypoints": True,
            "create_new_bounded_validation_surface": True,
            "write_new_surface_manifest": True,
            "write_new_surface_receipt": True,
            "write_candidate_compatible_rows_if_surface_created": True,
            "hold_if_no_safe_runner_or_recipe_exists": True,
        },
        "new_surface_forbidden_actions": {
            "candidate_acceptance": True,
            "scale_mode_acceptance": True,
            "full_registry_scan": True,
            "registry_sqlite_read": True,
            "registry_write": True,
            "runtime_receipt_emission_change": True,
            "source_runtime_code_change": True,
            "receipt_replacement_deletion_compression_or_suppression": True,
            "case_id_or_cycle_n_primary_identity_patch": True,
            "rowid_or_receipt_hash_patch": True,
            "full_occurrence_key_in_signature_payload": True,
            "audit_pointer_or_debug_payload_in_signature_payload": True,
            "raw_delta_microhash_32_as_proof": True,
            "synthetic_fake_validation_rows": True,
        },
        "bounded_surface_generation_rule": {
            "surface_generation_name": "new_bounded_existing_runner_surface_v0",
            "surface_goal": "Create a new bounded validation surface that can produce candidate-compatible rows for RAW_DELTA_SIGNATURE_CANDIDATE_V0.",
            "generation_must_be_bounded": True,
            "generation_must_be_reproducible": True,
            "generation_must_use_existing_project_runner_or_existing_receipt_builder_only": True,
            "generation_must_not_modify_runtime_code": True,
            "generation_must_not_read_registry_sqlite": True,
            "generation_must_not_full_registry_scan": True,
            "generation_must_not_accept_candidate": True,
            "generation_must_not_authorize_scale_mode": True,
            "generation_must_record_command_or_recipe": True,
            "generation_must_record_inputs": True,
            "generation_must_record_output_paths": True,
            "generation_must_record_limits": True,
            "generation_must_record_failure_or_hold_reason": True,
            "allowed_discovery_paths": [
                "scripts/",
                "src/",
                "pyproject.toml",
                "README.md",
            ],
            "allowed_discovery_operations": [
                "read_file",
                "list_files",
                "run_help_command",
                "compile_target_script",
            ],
            "allowed_execution_operations": [
                "run_existing_bounded_cli_or_script",
                "write_observer_only_surface_rows",
                "write_observer_only_surface_receipt",
            ],
            "explicit_forbidden_paths": [
                "data/**/*.sqlite",
                "data/**/*.db",
                "data/**/registry.sqlite",
                "data/**/registry.db",
            ],
            "minimum_new_surface_requirement": {
                "if_runner_available": {
                    "must_create_new_candidate_compatible_rows": True,
                    "must_evaluate_at_least_one_new_band": True,
                    "must_not_exceed_limits": True,
                },
                "if_runner_unavailable": {
                    "terminal_class": "HOLD_NEW_BOUNDED_SURFACE_REQUIRES_RUNNER_DECISION",
                    "candidate_acceptance_still_forbidden": True,
                },
            },
            "bounds": {
                "max_new_runs": 3,
                "max_new_cases_total": 30,
                "max_cycles_per_case": 50,
                "max_candidate_rows": 10000,
                "max_new_bands": 512,
                "max_observer_runtime_seconds_soft": 600,
                "max_output_files": 16,
            },
            "surface_row_contract": {
                "required_truth_key": "full_occurrence_key",
                "required_band_key": "source_band_id",
                "required_signature_payload": CANDIDATE_PAYLOAD_FIELDS,
                "required_truth_surface": "full_occurrence_key_to_candidate_delta_signature",
                "forbidden_signature_payload_fields": FORBIDDEN_PAYLOAD_FIELDS,
                "must_include_audit_recoverability_reference_outside_payload": True,
                "audit_reference_must_not_enter_signature_payload": True,
            },
        },
        "new_surface_terminal_classes": {
            "PASS_NEW_BOUNDED_VALIDATION_SURFACE_CREATED": "A new bounded candidate-compatible validation surface was created; candidate still not accepted.",
            "HOLD_NEW_BOUNDED_SURFACE_REQUIRES_RUNNER_DECISION": "No safe existing bounded runner/recipe was found; human/agent must decide how to create new evidence.",
            "FAIL_NEW_BOUNDED_SURFACE_AUTHORITY": "Surface creation would require forbidden authority.",
            "FAIL_NEW_BOUNDED_SURFACE_SOURCE_SURFACE": "Required candidate-compatible fields could not be produced or audited.",
            "FAIL_NEW_BOUNDED_SURFACE_IDENTITY_LEAK": "Forbidden identity/audit/debug/hash field entered candidate signature payload.",
            "FAIL_NEW_BOUNDED_SURFACE_UNBOUNDED": "Proposed surface is unbounded or exceeds policy limits.",
        },
        "post_surface_next_steps": {
            "if_pass": "RUN_RAW_DELTA_SIGNATURE_CANDIDATE_ON_NEW_BOUNDED_SURFACE_POLICY_V0",
            "if_hold": "HUMAN_OR_AGENT_DECIDE_NEW_SURFACE_RECIPE_V0",
            "if_fail": "DIAGNOSE_NEW_BOUNDED_SURFACE_FAILURE_V0",
        },
        "acceptance_after_new_surface": {
            "candidate_acceptance_still_forbidden": True,
            "runtime_change_still_forbidden": True,
            "scale_mode_still_forbidden": True,
            "new_surface_pass_may_only_authorize_candidate_probe_policy": True,
        },
    }

    authority = {
        "observer_only": True,
        "authorizes_new_bounded_validation_surface_implementation": True,
        "authorized_next_command_goal": NEXT_COMMAND_GOAL,
        "authorizes_runner_entrypoint_inspection": True,
        "authorizes_existing_bounded_runner_execution": True,
        "authorizes_new_surface_manifest_write": True,
        "authorizes_candidate_compatible_surface_rows_write": True,
        "authorizes_candidate_acceptance": False,
        "authorizes_scale_mode": False,
        "authorizes_full_registry_scan": False,
        "authorizes_registry_sqlite_read": False,
        "authorizes_runtime_receipt_emission_change": False,
        "authorizes_runtime_code_change": False,
        "authorizes_registry_write": False,
        "authorizes_receipt_replacement": False,
        "authorizes_receipt_deletion": False,
        "authorizes_receipt_compression": False,
        "authorizes_receipt_suppression": False,
        "authorizes_case_id_or_cycle_n_primary_identity_patch": False,
        "authorizes_rowid_or_receipt_hash_patch": False,
        "authorizes_raw_receipt_hash_truth_surface": False,
        "authorizes_full_occurrence_key_in_payload": False,
        "authorizes_audit_pointer_in_payload": False,
        "authorizes_debug_payload_in_payload": False,
        "authorizes_microhash_as_proof": False,
        "authorizes_synthetic_fake_validation_rows": False,
    }

    implementation_constraints = {
        "must_touch_only_files": [
            "scripts/raw_delta_signature_candidate_new_bounded_validation_surface_v0.py",
        ],
        "must_not_modify_files": [
            "src/",
            "app/",
            "matrixlab/",
            "scripts/raw_delta_signature_candidate_bounded_scale_out_v0.py",
            "scripts/build_raw_delta_signature_candidate_bounded_scale_out_policy_v0.py",
            "scripts/raw_delta_signature_candidate_scale_review_v0.py",
            "scripts/build_raw_delta_signature_candidate_scale_review_policy_v0.py",
            "scripts/raw_delta_signature_candidate_probe_v0.py",
            "scripts/build_raw_delta_signature_candidate_policy_v0.py",
            "scripts/raw_delta_compactness_diagnostic_v0.py",
            "scripts/build_raw_delta_compactness_diagnostic_policy_v0.py",
            "scripts/stable_delta_signature_candidate_v0_3_probe.py",
            "scripts/diagnose_v0_3_failure_v0.py",
            "scripts/stable_delta_signature_candidate_v0_2_scale_band_probe.py",
            "scripts/stable_delta_signature_candidate_v0_2_probe.py",
        ],
        "must_reuse_existing_receipts_and_rows": True,
        "must_start_from_hold_receipt": EXPECTED_BOUNDED_SCALE_OUT_ID,
        "must_record_runner_discovery": True,
        "must_record_surface_recipe_or_hold": True,
        "must_not_read_registry_sqlite": True,
        "must_not_full_registry_scan": True,
        "must_not_accept_candidate": True,
        "must_not_authorize_scale_mode": True,
        "must_not_change_runtime_receipt_emission": True,
        "must_not_change_runtime_code": True,
        "must_not_write_registry": True,
    }

    required_negative_controls = [
        {
            "case": "source_hold_not_clean_fail",
            "must_fail_if": "source bounded scale-out is not HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY with gate PASS",
        },
        {
            "case": "acceptance_authority_fail",
            "must_fail_if": "candidate acceptance, scale mode, runtime change, or registry write is authorized",
        },
        {
            "case": "registry_sqlite_or_full_scan_fail",
            "must_fail_if": "new surface policy authorizes registry.sqlite read or full registry scan",
        },
        {
            "case": "unbounded_surface_fail",
            "must_fail_if": "new surface policy lacks explicit bounded limits",
        },
        {
            "case": "identity_payload_leak_fail",
            "must_fail_if": "case_id, cycle_n, rowid, receipt hash, full occurrence key, audit/debug payload, or microhash proof enters signature payload",
        },
        {
            "case": "synthetic_rows_fail",
            "must_fail_if": "policy authorizes fake/synthetic validation rows instead of existing runner/file-backed evidence",
        },
        {
            "case": "runtime_code_mutation_fail",
            "must_fail_if": "policy authorizes modifying runtime/source code to make evidence",
        },
    ]

    policy = {
        "schema_version": "raw_delta_signature_candidate_new_bounded_validation_surface_policy_v0",
        "policy_name": POLICY_NAME,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "surface_name": SURFACE_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_bounded_scale_out_id": EXPECTED_BOUNDED_SCALE_OUT_ID,
        "source_bounded_scale_out_receipt_id": EXPECTED_BOUNDED_SCALE_OUT_RECEIPT_ID,
        "source_bounded_scale_out_policy_id": EXPECTED_BOUNDED_SCALE_OUT_POLICY_ID,
        "source_scale_review_id": EXPECTED_SCALE_REVIEW_ID,
        "source_candidate_probe_id": EXPECTED_CANDIDATE_PROBE_ID,
        "surface_contract": surface_contract,
        "authority": authority,
        "implementation_constraints": implementation_constraints,
        "required_negative_controls": required_negative_controls,
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_RAW_DELTA_SIGNATURE_CANDIDATE_NEW_BOUNDED_VALIDATION_SURFACE_POLICY_INVALID",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    policy_id = sha8({
        "policy_name": POLICY_NAME,
        "surface_name": SURFACE_NAME,
        "source_bounded_scale_out_id": EXPECTED_BOUNDED_SCALE_OUT_ID,
        "surface_contract": surface_contract,
        "authority": authority,
        "implementation_constraints": implementation_constraints,
    })
    policy["policy_id"] = policy_id
    policy["policy_sig8"] = policy_id

    receipt = {
        "schema_version": "raw_delta_signature_candidate_new_bounded_validation_surface_policy_receipt_v0",
        "policy_id": policy_id,
        "policy_sig8": policy_id,
        "policy_name": POLICY_NAME,
        "policy_status": policy["policy_status"],
        "surface_name": SURFACE_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "policy_path": f"data/raw_delta_signature_candidate_new_bounded_validation_surface_policies/{policy_id}.json",
        "source_bounded_scale_out_id": EXPECTED_BOUNDED_SCALE_OUT_ID,
        "source_bounded_scale_out_receipt_id": EXPECTED_BOUNDED_SCALE_OUT_RECEIPT_ID,
        "source_bounded_scale_out_policy_id": EXPECTED_BOUNDED_SCALE_OUT_POLICY_ID,
        "source_scale_review_id": EXPECTED_SCALE_REVIEW_ID,
        "source_candidate_probe_id": EXPECTED_CANDIDATE_PROBE_ID,
        "surface_contract_summary": {
            "source_hold_class": "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY",
            "selected_encoding_id": SELECTED_ENCODING_ID,
            "selected_target_raw_delta_field": TARGET_RAW_DELTA_FIELD,
            "candidate_payload_fields": CANDIDATE_PAYLOAD_FIELDS,
            "truth_surface": "full_occurrence_key_to_candidate_delta_signature",
            "new_surface_authorized": True,
            "existing_bounded_runner_execution_authorized": True,
            "runner_discovery_authorized": True,
            "max_new_runs": surface_contract["bounded_surface_generation_rule"]["bounds"]["max_new_runs"],
            "max_new_cases_total": surface_contract["bounded_surface_generation_rule"]["bounds"]["max_new_cases_total"],
            "max_cycles_per_case": surface_contract["bounded_surface_generation_rule"]["bounds"]["max_cycles_per_case"],
            "max_candidate_rows": surface_contract["bounded_surface_generation_rule"]["bounds"]["max_candidate_rows"],
            "max_new_bands": surface_contract["bounded_surface_generation_rule"]["bounds"]["max_new_bands"],
            "candidate_acceptance_forbidden": True,
            "full_registry_forbidden": True,
            "registry_sqlite_read_forbidden": True,
            "runtime_change_forbidden": True,
            "runtime_code_change_forbidden": True,
            "synthetic_fake_rows_forbidden": True,
        },
        "authority": authority,
        "implementation_constraints": implementation_constraints,
        "terminal": policy["terminal"],
        "gate": policy["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id

    (OUT_DIR / f"{policy_id}.json").write_text(json.dumps(policy, indent=2, sort_keys=True))
    (OUT_RECEIPT_DIR / f"{policy_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return policy, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-scale-out-id", default=EXPECTED_BOUNDED_SCALE_OUT_ID)
    args = parser.parse_args()

    policy, receipt = build_policy(args.source_scale_out_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_id={policy['policy_id']}")
    print(f"policy_json_path=data/raw_delta_signature_candidate_new_bounded_validation_surface_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/raw_delta_signature_candidate_new_bounded_validation_surface_policy_receipts/{policy['policy_id']}.json")

    return 0 if policy["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
