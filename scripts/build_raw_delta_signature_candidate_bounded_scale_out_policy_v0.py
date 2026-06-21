#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

SCALE_REVIEW_DIR = ROOT / "data" / "raw_delta_signature_candidate_scale_reviews"
SCALE_REVIEW_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_scale_review_receipts"
SCALE_REVIEW_POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_scale_review_policies"
SCALE_REVIEW_POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_scale_review_policy_receipts"
CANDIDATE_PROBE_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_probe_receipts"
CANDIDATE_POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_policy_receipts"
RAW_DELTA_DIAG_RECEIPT_DIR = ROOT / "data" / "raw_delta_compactness_diagnostic_receipts"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_bounded_scale_out_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_bounded_scale_out_policy_receipts"

EXPECTED_SCALE_REVIEW_ID = "6539838c"
EXPECTED_SCALE_REVIEW_RECEIPT_ID = "0c85a6f1"
EXPECTED_SCALE_REVIEW_POLICY_ID = "c9c7026d"
EXPECTED_SCALE_REVIEW_POLICY_RECEIPT_ID = "f917841b"
EXPECTED_CANDIDATE_PROBE_ID = "6a33c978"
EXPECTED_CANDIDATE_PROBE_RECEIPT_ID = "99c90fe3"
EXPECTED_CANDIDATE_POLICY_ID = "3b8eb867"
EXPECTED_CANDIDATE_POLICY_RECEIPT_ID = "6778ef03"
EXPECTED_RAW_DELTA_DIAGNOSTIC_ID = "74caa0f4"
EXPECTED_RAW_DELTA_DIAGNOSTIC_RECEIPT_ID = "129e9a76"

POLICY_NAME = "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_BOUNDED_SCALE_OUT_POLICY_V0"
SCALE_OUT_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_BOUNDED_SCALE_OUT_V0"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"
NEXT_COMMAND_GOAL = "IMPLEMENT_RAW_DELTA_SIGNATURE_CANDIDATE_BOUNDED_SCALE_OUT_V0"

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

FORBIDDEN_AUTHORITY = [
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


def verify_sources(
    scale_review: dict[str, Any],
    scale_review_receipt: dict[str, Any],
    scale_review_policy: dict[str, Any],
    scale_review_policy_receipt: dict[str, Any],
    candidate_probe_receipt: dict[str, Any],
    candidate_policy_receipt: dict[str, Any],
    raw_delta_diag_receipt: dict[str, Any],
) -> list[str]:
    failures: list[str] = []

    if scale_review.get("review_id") != EXPECTED_SCALE_REVIEW_ID:
        failures.append(f"scale_review_id_wrong:{scale_review.get('review_id')}")
    if scale_review_receipt.get("receipt_id") != EXPECTED_SCALE_REVIEW_RECEIPT_ID:
        failures.append(f"scale_review_receipt_id_wrong:{scale_review_receipt.get('receipt_id')}")
    if scale_review.get("gate") != "PASS":
        failures.append(f"scale_review_gate_not_PASS:{scale_review.get('gate')}")
    if scale_review_receipt.get("gate") != "PASS":
        failures.append(f"scale_review_receipt_gate_not_PASS:{scale_review_receipt.get('gate')}")
    if scale_review.get("mode") != "OUTER_OBSERVER_ONLY":
        failures.append(f"scale_review_mode_wrong:{scale_review.get('mode')}")
    if scale_review.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"scale_review_candidate_design_wrong:{scale_review.get('candidate_design_id')}")
    if scale_review.get("terminal_class") != "ADVANCE_TO_BOUNDED_SCALE_OUT_POLICY":
        failures.append(f"scale_review_terminal_class_wrong:{scale_review.get('terminal_class')}")
    if scale_review.get("terminal", {}).get("next_command_goal") != POLICY_NAME:
        failures.append(f"scale_review_next_goal_wrong:{scale_review.get('terminal', {}).get('next_command_goal')}")

    review_decision = scale_review.get("review_decision") or {}
    if review_decision.get("review_class") != "ADVANCE_TO_BOUNDED_SCALE_OUT_POLICY":
        failures.append(f"review_class_wrong:{review_decision.get('review_class')}")
    if review_decision.get("recommended_next_command_goal") != POLICY_NAME:
        failures.append(f"review_next_goal_wrong:{review_decision.get('recommended_next_command_goal')}")
    if review_decision.get("acceptance_sufficient") is not False:
        failures.append(f"acceptance_sufficient_not_false:{review_decision.get('acceptance_sufficient')}")
    if review_decision.get("candidate_should_remain_selected") is not True:
        failures.append(f"candidate_should_remain_selected_not_true:{review_decision.get('candidate_should_remain_selected')}")
    if review_decision.get("selected_encoding_should_remain") != SELECTED_ENCODING_ID:
        failures.append(f"selected_encoding_wrong:{review_decision.get('selected_encoding_should_remain')}")
    if review_decision.get("candidate_payload_should_remain") != CANDIDATE_PAYLOAD_FIELDS:
        failures.append(f"candidate_payload_wrong:{review_decision.get('candidate_payload_should_remain')}")

    blockers = set(review_decision.get("acceptance_blockers") or [])
    for blocker in [
        "candidate_acceptance_not_authorized_by_policy",
        "bounded_probe_is_single_validation_radius",
        "no_independent_scale_out_policy_executed_yet",
        "no_full_registry_authority",
        "runtime_change_not_authorized",
    ]:
        if blocker not in blockers:
            failures.append(f"acceptance_blocker_missing:{blocker}")

    radius = review_decision.get("next_validation_radius_recommendation") or {}
    if radius.get("kind") != "bounded_scale_out_policy":
        failures.append(f"radius_kind_wrong:{radius.get('kind')}")
    if radius.get("requires_human_decision_now") is not False:
        failures.append(f"requires_human_decision_now_wrong:{radius.get('requires_human_decision_now')}")
    for key in [
        "must_be_larger_than_current_bounded_surface",
        "must_include_prior_266_band_surface",
        "must_define_explicit_selection_rule_before_execution",
        "must_not_use_full_registry_scan",
        "must_not_read_registry_sqlite",
        "must_not_accept_candidate",
        "must_not_change_runtime",
        "must_not_write_registry",
    ]:
        if radius.get(key) is not True:
            failures.append(f"radius_flag_not_true:{key}:{radius.get(key)}")
    if radius.get("candidate_under_review") != CANDIDATE_DESIGN_ID:
        failures.append(f"radius_candidate_wrong:{radius.get('candidate_under_review')}")
    if radius.get("candidate_payload") != CANDIDATE_PAYLOAD_FIELDS:
        failures.append(f"radius_payload_wrong:{radius.get('candidate_payload')}")
    if radius.get("selected_encoding_id") != SELECTED_ENCODING_ID:
        failures.append(f"radius_encoding_wrong:{radius.get('selected_encoding_id')}")
    if radius.get("selected_target_raw_delta_field") != TARGET_RAW_DELTA_FIELD:
        failures.append(f"radius_target_wrong:{radius.get('selected_target_raw_delta_field')}")

    evidence = scale_review.get("source_bounded_pass_evidence") or {}
    expected_evidence = {
        "bands_total": 266,
        "bands_passed": 266,
        "bands_failed": 0,
        "all_band_false_merge_count": 0,
        "worst_false_merge_count": 0,
        "worst_collision_count": 0,
        "worst_false_split_count": 0,
        "worst_distinguishability_retention_ratio": 1.0,
        "identity_leak_count": 0,
        "source_surface_regression_count": 0,
        "total_full_receipt_bytes": 2870426,
        "total_projected_plus_signature_payload_bytes": 1475169,
    }
    for key, expected in expected_evidence.items():
        if evidence.get(key) != expected:
            failures.append(f"bounded_evidence_{key}_wrong:{evidence.get(key)}")
    if not (evidence.get("total_burden_ratio_projected", 999) < 1.0):
        failures.append(f"bounded_evidence_total_burden_not_below_1:{evidence.get('total_burden_ratio_projected')}")
    if not (evidence.get("worst_burden_ratio_projected", 999) < 1.0):
        failures.append(f"bounded_evidence_worst_burden_not_below_1:{evidence.get('worst_burden_ratio_projected')}")

    guards = scale_review.get("authority_guards") or {}
    if guards.get("observer_only") is not True:
        failures.append("scale_review_not_observer_only")
    if guards.get("bounded_scale_out_policy_recommended") is not True:
        failures.append(f"bounded_scale_out_policy_not_recommended:{guards.get('bounded_scale_out_policy_recommended')}")
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
            failures.append(f"scale_review_guard_not_false:{key}:{guards.get(key)}")

    pass_gates = scale_review.get("pass_gates") or {}
    for key in [
        "policy_preconditions",
        "source_candidate_probe_passed",
        "bounded_pass_evidence_clean",
        "acceptance_remains_forbidden",
        "bounded_scale_out_only",
        "authority_containment",
        "truth_surface_preserved",
        "no_identity_leak",
    ]:
        if pass_gates.get(key) is not True:
            failures.append(f"scale_review_pass_gate_not_true:{key}:{pass_gates.get(key)}")

    decision = scale_review.get("decision") or {}
    if decision.get("candidate_accepted") is not False:
        failures.append(f"decision_candidate_accepted_not_false:{decision.get('candidate_accepted')}")
    if decision.get("candidate_acceptance_authorized") is not False:
        failures.append(f"decision_candidate_acceptance_authorized_not_false:{decision.get('candidate_acceptance_authorized')}")
    if decision.get("scale_mode_authorized") is not False:
        failures.append(f"decision_scale_mode_authorized_not_false:{decision.get('scale_mode_authorized')}")
    for key in [
        "review_only",
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

    if scale_review_policy.get("policy_id") != EXPECTED_SCALE_REVIEW_POLICY_ID:
        failures.append(f"scale_review_policy_id_wrong:{scale_review_policy.get('policy_id')}")
    if scale_review_policy_receipt.get("receipt_id") != EXPECTED_SCALE_REVIEW_POLICY_RECEIPT_ID:
        failures.append(f"scale_review_policy_receipt_id_wrong:{scale_review_policy_receipt.get('receipt_id')}")
    if scale_review_policy.get("gate") != "PASS":
        failures.append(f"scale_review_policy_gate_not_PASS:{scale_review_policy.get('gate')}")
    if candidate_probe_receipt.get("probe_id") != EXPECTED_CANDIDATE_PROBE_ID:
        failures.append(f"candidate_probe_id_wrong:{candidate_probe_receipt.get('probe_id')}")
    if candidate_probe_receipt.get("receipt_id") != EXPECTED_CANDIDATE_PROBE_RECEIPT_ID:
        failures.append(f"candidate_probe_receipt_id_wrong:{candidate_probe_receipt.get('receipt_id')}")
    if candidate_probe_receipt.get("gate") != "PASS":
        failures.append(f"candidate_probe_gate_not_PASS:{candidate_probe_receipt.get('gate')}")
    if candidate_probe_receipt.get("terminal_decision") != "PASS_RAW_DELTA_SIGNATURE_CANDIDATE_BOUNDED_PROBE":
        failures.append(f"candidate_probe_terminal_wrong:{candidate_probe_receipt.get('terminal_decision')}")
    if candidate_policy_receipt.get("policy_id") != EXPECTED_CANDIDATE_POLICY_ID:
        failures.append(f"candidate_policy_id_wrong:{candidate_policy_receipt.get('policy_id')}")
    if candidate_policy_receipt.get("receipt_id") != EXPECTED_CANDIDATE_POLICY_RECEIPT_ID:
        failures.append(f"candidate_policy_receipt_id_wrong:{candidate_policy_receipt.get('receipt_id')}")
    if raw_delta_diag_receipt.get("diagnostic_id") != EXPECTED_RAW_DELTA_DIAGNOSTIC_ID:
        failures.append(f"raw_delta_diag_id_wrong:{raw_delta_diag_receipt.get('diagnostic_id')}")
    if raw_delta_diag_receipt.get("receipt_id") != EXPECTED_RAW_DELTA_DIAGNOSTIC_RECEIPT_ID:
        failures.append(f"raw_delta_diag_receipt_id_wrong:{raw_delta_diag_receipt.get('receipt_id')}")

    return failures


def build_policy(source_review_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    scale_review = load_json(SCALE_REVIEW_DIR / f"{source_review_id}.json")
    scale_review_receipt = load_json(SCALE_REVIEW_RECEIPT_DIR / f"{source_review_id}.json")
    scale_review_policy = load_json(SCALE_REVIEW_POLICY_DIR / f"{EXPECTED_SCALE_REVIEW_POLICY_ID}.json")
    scale_review_policy_receipt = load_json(SCALE_REVIEW_POLICY_RECEIPT_DIR / f"{EXPECTED_SCALE_REVIEW_POLICY_ID}.json")
    candidate_probe_receipt = load_json(CANDIDATE_PROBE_RECEIPT_DIR / f"{EXPECTED_CANDIDATE_PROBE_ID}.json")
    candidate_policy_receipt = load_json(CANDIDATE_POLICY_RECEIPT_DIR / f"{EXPECTED_CANDIDATE_POLICY_ID}.json")
    raw_delta_diag_receipt = load_json(RAW_DELTA_DIAG_RECEIPT_DIR / f"{EXPECTED_RAW_DELTA_DIAGNOSTIC_ID}.json")

    failures = verify_sources(
        scale_review,
        scale_review_receipt,
        scale_review_policy,
        scale_review_policy_receipt,
        candidate_probe_receipt,
        candidate_policy_receipt,
        raw_delta_diag_receipt,
    )

    source_evidence = scale_review.get("source_bounded_pass_evidence") or {}
    scale_out_contract = {
        "scale_out_name": SCALE_OUT_NAME,
        "scale_out_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_scale_review_id": EXPECTED_SCALE_REVIEW_ID,
        "source_scale_review_receipt_id": EXPECTED_SCALE_REVIEW_RECEIPT_ID,
        "source_candidate_probe_id": EXPECTED_CANDIDATE_PROBE_ID,
        "source_candidate_probe_receipt_id": EXPECTED_CANDIDATE_PROBE_RECEIPT_ID,
        "selected_encoding_id": SELECTED_ENCODING_ID,
        "selected_target_raw_delta_field": TARGET_RAW_DELTA_FIELD,
        "candidate_payload_fields": CANDIDATE_PAYLOAD_FIELDS,
        "candidate_payload_forbidden_fields": FORBIDDEN_PAYLOAD_FIELDS,
        "truth_surface": "full_occurrence_key_to_candidate_delta_signature",
        "source_bounded_pass_evidence": source_evidence,
        "scale_out_selection_rule": {
            "selection_name": "bounded_file_backed_scale_out_v0",
            "selection_goal": "Evaluate RAW_DELTA_SIGNATURE_CANDIDATE_V0 on a larger bounded validation surface while preserving the prior 266-band surface.",
            "must_include_prior_candidate_probe_rows_path": "data/raw_delta_signature_candidate_probe_rows/6a33c978.jsonl",
            "must_include_prior_bands_total": 266,
            "must_include_prior_selected_rows_total": 3298,
            "must_add_new_validation_surface": True,
            "new_surface_must_be_file_backed_existing_artifacts": True,
            "allowed_inventory_roots": [
                "data/",
            ],
            "allowed_inventory_patterns": [
                "data/**/*receipt*.json",
                "data/**/*receipts/*.json",
                "data/**/*.jsonl",
            ],
            "explicit_exclusions": [
                "data/**/*.sqlite",
                "data/**/*.db",
                "data/**/registry.sqlite",
                "data/**/registry.db",
                ".git/",
                ".venv/",
                "__pycache__/",
            ],
            "deterministic_order": [
                "artifact_kind",
                "source_run_id",
                "created_at_or_mtime",
                "path",
            ],
            "max_additional_candidate_rows": 10000,
            "max_additional_bands": 512,
            "max_additional_source_files": 64,
            "min_total_bands_required_if_inventory_available": 267,
            "must_stop_if_no_additional_bounded_inventory": "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY",
            "must_record_inventory_summary": True,
            "must_record_selected_inventory_paths": True,
            "must_record_excluded_inventory_paths_or_counts": True,
            "must_not_read_registry_sqlite": True,
            "must_not_full_registry_scan": True,
            "must_not_accept_candidate": True,
            "must_not_authorize_scale_mode": True,
            "must_not_change_runtime": True,
            "must_not_write_registry": True,
        },
        "scale_out_probe_required_measurements": {
            "prior_266_band_surface_replayed": True,
            "additional_inventory_selected": True,
            "total_bands_evaluated": True,
            "new_bands_evaluated": True,
            "candidate_false_merge_count": True,
            "candidate_false_split_count": True,
            "distinguishability_retention_ratio": True,
            "projected_burden_ratio": True,
            "source_surface_regression_count": True,
            "identity_leak_count": True,
            "audit_recoverability": True,
            "authority_containment": True,
            "comparison_to_prior_bounded_probe": True,
        },
        "scale_out_pass_gates": {
            "authority_containment": "observer-only, no acceptance, no scale mode, no registry read/write, no runtime change",
            "prior_surface_replayed": "the prior 266-band pass surface must remain clean",
            "larger_surface_or_hold": "evaluate at least one additional bounded surface if available, otherwise HOLD without acceptance",
            "truth_surface": "full_occurrence_key to candidate signature comparison only",
            "no_identity_leak": "payload excludes case_id/cycle_n/rowid/receipt hash/full occurrence key/audit/debug/microhash proof",
            "no_false_merge": "no candidate signature may merge distinct full occurrence keys",
            "no_false_split": "no full occurrence key may split across signatures",
            "burden_reduction": "projected burden must remain below full receipt burden on evaluated surface",
            "source_surface_clean": "all required candidate fields and burden basis must be reconstructable from allowed file-backed artifacts",
        },
        "scale_out_terminal_classes": {
            "PASS_BOUNDED_SCALE_OUT_CLEAN": "Candidate remains distinguishable and burden-reducing on the larger bounded surface; still not accepted.",
            "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY": "No lawful larger bounded inventory is available without a human decision or new run.",
            "FAIL_BOUNDED_SCALE_OUT_FALSE_MERGE": "Candidate false merge appears on larger bounded surface.",
            "FAIL_BOUNDED_SCALE_OUT_FALSE_SPLIT": "Candidate false split appears on larger bounded surface.",
            "FAIL_BOUNDED_SCALE_OUT_BURDEN": "Candidate burden is not below full receipts on evaluated surface.",
            "FAIL_BOUNDED_SCALE_OUT_SOURCE_SURFACE": "Required fields/burden basis cannot be reconstructed from bounded file-backed artifacts.",
            "FAIL_BOUNDED_SCALE_OUT_AUTHORITY": "Scale-out would require forbidden authority.",
        },
        "acceptance_after_scale_out": {
            "candidate_acceptance_still_forbidden": True,
            "scale_out_pass_may_only_recommend_next_review": True,
            "runtime_change_still_forbidden": True,
        },
    }

    authority = {
        "observer_only": True,
        "authorizes_next_bounded_scale_out_implementation": True,
        "authorized_next_command_goal": NEXT_COMMAND_GOAL,
        "authorizes_bounded_file_backed_inventory_inspection": True,
        "authorizes_bounded_candidate_scale_out_execution": True,
        "authorizes_candidate_acceptance": False,
        "authorizes_scale_mode": False,
        "authorizes_full_registry_scan": False,
        "authorizes_registry_sqlite_read": False,
        "authorizes_runtime_receipt_emission_change": False,
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
    }

    implementation_constraints = {
        "must_touch_only_files": [
            "scripts/raw_delta_signature_candidate_bounded_scale_out_v0.py",
        ],
        "must_not_modify_files": [
            "src/",
            "app/",
            "matrixlab/",
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
        "must_include_prior_266_band_surface": True,
        "must_define_inventory_before_evaluating": True,
        "must_not_read_registry_sqlite": True,
        "must_not_full_registry_scan": True,
        "must_not_accept_candidate": True,
        "must_not_authorize_scale_mode": True,
        "must_not_change_runtime_receipt_emission": True,
        "must_not_write_registry": True,
    }

    required_negative_controls = [
        {
            "case": "source_scale_review_not_advance_fail",
            "must_fail_if": "source scale review is not ADVANCE_TO_BOUNDED_SCALE_OUT_POLICY",
        },
        {
            "case": "bounded_pass_evidence_regressed_fail",
            "must_fail_if": "prior bounded pass evidence loses distinguishability, burden reduction, or clean source surface",
        },
        {
            "case": "acceptance_authority_fail",
            "must_fail_if": "candidate acceptance or runtime/scale mode authority is granted",
        },
        {
            "case": "registry_sqlite_or_full_registry_fail",
            "must_fail_if": "policy authorizes registry.sqlite read or full registry scan",
        },
        {
            "case": "identity_leak_fail",
            "must_fail_if": "case_id, cycle_n, rowid, receipt hash, full occurrence key, audit/debug payload, or microhash proof enters signature payload",
        },
        {
            "case": "selection_rule_not_larger_fail",
            "must_fail_if": "policy does not require a larger bounded validation surface or explicit hold when no inventory exists",
        },
        {
            "case": "prior_surface_not_included_fail",
            "must_fail_if": "prior 266-band surface is not included in scale-out validation",
        },
    ]

    policy = {
        "schema_version": "raw_delta_signature_candidate_bounded_scale_out_policy_v0",
        "policy_name": POLICY_NAME,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "scale_out_name": SCALE_OUT_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_scale_review_id": EXPECTED_SCALE_REVIEW_ID,
        "source_scale_review_receipt_id": EXPECTED_SCALE_REVIEW_RECEIPT_ID,
        "source_scale_review_policy_id": EXPECTED_SCALE_REVIEW_POLICY_ID,
        "source_candidate_probe_id": EXPECTED_CANDIDATE_PROBE_ID,
        "source_candidate_policy_id": EXPECTED_CANDIDATE_POLICY_ID,
        "source_raw_delta_diagnostic_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_ID,
        "scale_out_contract": scale_out_contract,
        "authority": authority,
        "implementation_constraints": implementation_constraints,
        "required_negative_controls": required_negative_controls,
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_RAW_DELTA_SIGNATURE_CANDIDATE_BOUNDED_SCALE_OUT_POLICY_INVALID",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    policy_id = sha8({
        "policy_name": POLICY_NAME,
        "scale_out_name": SCALE_OUT_NAME,
        "source_scale_review_id": EXPECTED_SCALE_REVIEW_ID,
        "scale_out_contract": scale_out_contract,
        "authority": authority,
        "implementation_constraints": implementation_constraints,
    })
    policy["policy_id"] = policy_id
    policy["policy_sig8"] = policy_id

    receipt = {
        "schema_version": "raw_delta_signature_candidate_bounded_scale_out_policy_receipt_v0",
        "policy_id": policy_id,
        "policy_sig8": policy_id,
        "policy_name": POLICY_NAME,
        "policy_status": policy["policy_status"],
        "scale_out_name": SCALE_OUT_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "policy_path": f"data/raw_delta_signature_candidate_bounded_scale_out_policies/{policy_id}.json",
        "source_scale_review_id": EXPECTED_SCALE_REVIEW_ID,
        "source_scale_review_receipt_id": EXPECTED_SCALE_REVIEW_RECEIPT_ID,
        "source_scale_review_policy_id": EXPECTED_SCALE_REVIEW_POLICY_ID,
        "source_candidate_probe_id": EXPECTED_CANDIDATE_PROBE_ID,
        "source_candidate_policy_id": EXPECTED_CANDIDATE_POLICY_ID,
        "source_raw_delta_diagnostic_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_ID,
        "scale_out_contract_summary": {
            "selected_encoding_id": SELECTED_ENCODING_ID,
            "selected_target_raw_delta_field": TARGET_RAW_DELTA_FIELD,
            "candidate_payload_fields": CANDIDATE_PAYLOAD_FIELDS,
            "prior_surface_required": True,
            "prior_bands_total": 266,
            "prior_selected_rows_total": 3298,
            "must_add_new_validation_surface": True,
            "must_stop_if_no_additional_bounded_inventory": "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY",
            "max_additional_candidate_rows": 10000,
            "max_additional_bands": 512,
            "max_additional_source_files": 64,
            "candidate_acceptance_forbidden": True,
            "full_registry_forbidden": True,
            "registry_sqlite_read_forbidden": True,
            "runtime_change_forbidden": True,
            "source_bounded_pass_evidence": source_evidence,
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
    parser.add_argument("--source-review-id", default=EXPECTED_SCALE_REVIEW_ID)
    args = parser.parse_args()

    policy, receipt = build_policy(args.source_review_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_id={policy['policy_id']}")
    print(f"policy_json_path=data/raw_delta_signature_candidate_bounded_scale_out_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/raw_delta_signature_candidate_bounded_scale_out_policy_receipts/{policy['policy_id']}.json")

    return 0 if policy["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
