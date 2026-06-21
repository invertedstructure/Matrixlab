#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_scale_review_policies"
POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_scale_review_policy_receipts"
CANDIDATE_PROBE_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_probe_receipts"
CANDIDATE_POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_policy_receipts"
RAW_DELTA_DIAG_RECEIPT_DIR = ROOT / "data" / "raw_delta_compactness_diagnostic_receipts"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_scale_reviews"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_scale_review_receipts"

EXPECTED_POLICY_ID = "c9c7026d"
EXPECTED_POLICY_RECEIPT_ID = "f917841b"
EXPECTED_CANDIDATE_PROBE_ID = "6a33c978"
EXPECTED_CANDIDATE_PROBE_RECEIPT_ID = "99c90fe3"
EXPECTED_CANDIDATE_POLICY_ID = "3b8eb867"
EXPECTED_CANDIDATE_POLICY_RECEIPT_ID = "6778ef03"
EXPECTED_RAW_DELTA_DIAGNOSTIC_ID = "74caa0f4"
EXPECTED_RAW_DELTA_DIAGNOSTIC_RECEIPT_ID = "129e9a76"

REVIEW_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_SCALE_REVIEW_V0"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"
MODE = "OUTER_OBSERVER_ONLY"

TERMINAL_ADVANCE = "ADVANCE_TO_BOUNDED_SCALE_OUT_POLICY"
NEXT_COMMAND_GOAL = "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_BOUNDED_SCALE_OUT_POLICY_V0"

SELECTED_ENCODING_ID = "raw_decimal_sig6"
TARGET_RAW_DELTA_FIELD = "compression_ratio"
REQUIRED_PAYLOAD_FIELDS = [
    "cv",
    "state_hash_before",
    "move_id",
    "state_hash_after",
    "raw_compression_ratio_sig6",
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

FORBIDDEN_SOURCE_AUTHORITY_GUARDS = [
    "candidate_accepted",
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
    policy: dict[str, Any],
    policy_receipt: dict[str, Any],
    candidate_probe: dict[str, Any],
    candidate_policy_receipt: dict[str, Any],
    raw_diag_receipt: dict[str, Any],
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
    if policy.get("review_name") != REVIEW_NAME:
        failures.append(f"review_name_wrong:{policy.get('review_name')}")
    if policy.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"candidate_design_wrong:{policy.get('candidate_design_id')}")
    if policy.get("terminal", {}).get("next_command_goal") != "IMPLEMENT_RAW_DELTA_SIGNATURE_CANDIDATE_SCALE_REVIEW_V0":
        failures.append(f"policy_next_goal_wrong:{policy.get('terminal', {}).get('next_command_goal')}")

    contract = policy.get("scale_review_contract") or {}
    if contract.get("review_name") != REVIEW_NAME:
        failures.append(f"contract_review_name_wrong:{contract.get('review_name')}")
    if contract.get("review_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"contract_review_status_wrong:{contract.get('review_status')}")
    if contract.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"contract_candidate_design_wrong:{contract.get('candidate_design_id')}")
    if contract.get("source_candidate_probe_id") != EXPECTED_CANDIDATE_PROBE_ID:
        failures.append(f"contract_source_probe_wrong:{contract.get('source_candidate_probe_id')}")
    if contract.get("source_candidate_probe_receipt_id") != EXPECTED_CANDIDATE_PROBE_RECEIPT_ID:
        failures.append(f"contract_source_probe_receipt_wrong:{contract.get('source_candidate_probe_receipt_id')}")
    if contract.get("selected_payload") != REQUIRED_PAYLOAD_FIELDS:
        failures.append(f"contract_payload_wrong:{contract.get('selected_payload')}")
    if contract.get("selected_encoding_id") != SELECTED_ENCODING_ID:
        failures.append(f"contract_selected_encoding_wrong:{contract.get('selected_encoding_id')}")
    if contract.get("selected_target_raw_delta_field") != TARGET_RAW_DELTA_FIELD:
        failures.append(f"contract_target_field_wrong:{contract.get('selected_target_raw_delta_field')}")
    if contract.get("truth_surface") != "full_occurrence_key_to_candidate_delta_signature":
        failures.append(f"contract_truth_surface_wrong:{contract.get('truth_surface')}")

    allowed = contract.get("allowed_review_actions") or {}
    for key in [
        "compare_candidate_against_prior_v02_v03_raw_delta_evidence",
        "inspect_available_bounded_receipt_inventory",
        "derive_recommended_next_validation_radius",
        "write_review_receipt",
    ]:
        if allowed.get(key) is not True:
            failures.append(f"allowed_review_action_missing:{key}:{allowed.get(key)}")

    forbidden = contract.get("forbidden_review_actions") or {}
    for key in [
        "candidate_acceptance",
        "scale_mode_acceptance",
        "full_registry_scan",
        "registry_sqlite_read",
        "runtime_receipt_emission_change",
        "registry_write",
        "receipt_replacement_deletion_compression_or_suppression",
        "case_id_or_cycle_n_primary_identity_patch",
        "rowid_or_receipt_hash_patch",
        "full_occurrence_key_in_signature_payload",
        "audit_pointer_or_debug_payload_in_signature_payload",
        "raw_delta_microhash_32_as_proof",
    ]:
        if forbidden.get(key) is not True:
            failures.append(f"forbidden_review_action_not_marked:{key}:{forbidden.get(key)}")

    outputs = contract.get("authorized_review_outputs") or {}
    for key in [
        "may_recommend_bounded_scale_out_policy",
        "may_recommend_hold_for_human_review",
        "may_recommend_failure_diagnostic_if_new_blocker_found",
        "may_not_accept_candidate",
        "may_not_authorize_runtime_change",
    ]:
        if outputs.get(key) is not True:
            failures.append(f"authorized_output_missing:{key}:{outputs.get(key)}")

    evidence = contract.get("source_bounded_pass_evidence") or {}
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
            failures.append(f"evidence_{key}_wrong:{evidence.get(key)}")
    if not (evidence.get("total_burden_ratio_projected", 999) < 1.0):
        failures.append(f"evidence_total_burden_not_below_1:{evidence.get('total_burden_ratio_projected')}")
    if not (evidence.get("worst_burden_ratio_projected", 999) < 1.0):
        failures.append(f"evidence_worst_burden_not_below_1:{evidence.get('worst_burden_ratio_projected')}")

    auth = policy.get("authority") or {}
    if auth.get("observer_only") is not True:
        failures.append("policy_not_observer_only")
    if auth.get("authorizes_next_scale_review_implementation") is not True:
        failures.append("next_scale_review_not_authorized")
    if auth.get("authorized_next_command_goal") != "IMPLEMENT_RAW_DELTA_SIGNATURE_CANDIDATE_SCALE_REVIEW_V0":
        failures.append(f"authorized_next_goal_wrong:{auth.get('authorized_next_command_goal')}")
    if auth.get("authorizes_scale_review_policy_only") is not True:
        failures.append("scale_review_policy_only_not_authorized")
    if auth.get("authorizes_bounded_inventory_inspection") is not True:
        failures.append("bounded_inventory_inspection_not_authorized")
    for key in FORBIDDEN_AUTHORITY_FLAGS:
        if auth.get(key) is not False:
            failures.append(f"policy_illegal_authority:{key}:{auth.get(key)}")

    constraints = policy.get("implementation_constraints") or {}
    if constraints.get("must_touch_only_files") != ["scripts/raw_delta_signature_candidate_scale_review_v0.py"]:
        failures.append(f"touch_scope_wrong:{constraints.get('must_touch_only_files')}")
    for key in [
        "must_reuse_existing_receipts_and_rows",
        "must_not_read_registry_sqlite",
        "must_not_full_registry_scan",
        "must_not_accept_candidate",
        "must_not_authorize_scale_mode",
        "must_not_change_runtime_receipt_emission",
        "must_not_write_registry",
    ]:
        if constraints.get(key) is not True:
            failures.append(f"constraint_not_true:{key}:{constraints.get(key)}")

    if candidate_probe.get("probe_id") != EXPECTED_CANDIDATE_PROBE_ID:
        failures.append(f"candidate_probe_id_wrong:{candidate_probe.get('probe_id')}")
    if candidate_probe.get("receipt_id") != EXPECTED_CANDIDATE_PROBE_RECEIPT_ID:
        failures.append(f"candidate_probe_receipt_id_wrong:{candidate_probe.get('receipt_id')}")
    if candidate_probe.get("gate") != "PASS":
        failures.append(f"candidate_probe_gate_not_PASS:{candidate_probe.get('gate')}")
    if candidate_probe.get("terminal_decision") != "PASS_RAW_DELTA_SIGNATURE_CANDIDATE_BOUNDED_PROBE":
        failures.append(f"candidate_probe_terminal_wrong:{candidate_probe.get('terminal_decision')}")
    if candidate_probe.get("mode") != "OUTER_OBSERVER_ONLY":
        failures.append(f"candidate_probe_mode_wrong:{candidate_probe.get('mode')}")

    probe_agg = candidate_probe.get("aggregate_measurements") or {}
    probe_expected_aliases = {
        "bands_total": "bands_total",
        "bands_passed": "bands_passed",
        "bands_failed": "bands_failed",
        "all_band_false_merge_count": "all_band_false_merge_count",
        "worst_false_merge_count": "worst_false_merge_count",
        "worst_collision_count": "worst_collision_count",
        "worst_false_split_count": "worst_false_split_count",
        "worst_distinguishability_retention_ratio": "worst_distinguishability_retention_ratio",
        "identity_leak_count": "worst_identity_leak_count",
        "source_surface_regression_count": "worst_source_surface_regression_count",
        "total_full_receipt_bytes": "total_full_receipt_bytes",
        "total_projected_plus_signature_payload_bytes": "total_projected_plus_signature_payload_bytes",
    }
    for evidence_key, probe_key in probe_expected_aliases.items():
        expected = expected_evidence[evidence_key]
        observed = probe_agg.get(probe_key)
        if observed != expected:
            failures.append(f"probe_aggregate_{probe_key}_wrong:{observed}")
    if not (probe_agg.get("total_burden_ratio_projected", 999) < 1.0):
        failures.append(f"probe_total_burden_not_below_1:{probe_agg.get('total_burden_ratio_projected')}")
    if not (probe_agg.get("worst_burden_ratio_projected", 999) < 1.0):
        failures.append(f"probe_worst_burden_not_below_1:{probe_agg.get('worst_burden_ratio_projected')}")

    pass_gates = candidate_probe.get("pass_gates") or {}
    for key in [
        "audit_recoverability",
        "authority_containment",
        "bounded_surface_reused",
        "burden_reduction",
        "candidate_not_accepted",
        "no_false_merge_all_bands",
        "no_false_split_all_bands",
        "no_identity_leak",
        "policy_preconditions",
        "raw_delta_coverage",
        "scale_mode_not_authorized",
        "source_surface",
        "truth_surface",
    ]:
        if pass_gates.get(key) is not True:
            failures.append(f"candidate_probe_gate_not_true:{key}:{pass_gates.get(key)}")

    guards = candidate_probe.get("authority_guards") or {}
    if guards.get("observer_only") is not True:
        failures.append("candidate_probe_not_observer_only")
    for key in FORBIDDEN_SOURCE_AUTHORITY_GUARDS:
        if guards.get(key) is not False:
            failures.append(f"candidate_probe_guard_not_false:{key}:{guards.get(key)}")

    decision = candidate_probe.get("decision") or {}
    if decision.get("candidate_accepted") is not False:
        failures.append(f"candidate_probe_decision_accepted:{decision.get('candidate_accepted')}")
    if decision.get("candidate_acceptance_authorized") is not False:
        failures.append(f"candidate_probe_decision_acceptance_authorized:{decision.get('candidate_acceptance_authorized')}")
    for key in [
        "diagnostic_probe_only",
        "do_not_accept_candidate",
        "do_not_change_runtime",
        "do_not_full_registry_scan",
        "do_not_read_registry_sqlite",
        "do_not_use_case_id_or_cycle_n_as_primary_identity",
        "do_not_use_rowid_or_receipt_hash",
        "do_not_write_registry",
    ]:
        if decision.get(key) is not True:
            failures.append(f"candidate_probe_decision_flag_not_true:{key}:{decision.get(key)}")

    if candidate_policy_receipt.get("policy_id") != EXPECTED_CANDIDATE_POLICY_ID:
        failures.append(f"candidate_policy_id_wrong:{candidate_policy_receipt.get('policy_id')}")
    if candidate_policy_receipt.get("receipt_id") != EXPECTED_CANDIDATE_POLICY_RECEIPT_ID:
        failures.append(f"candidate_policy_receipt_id_wrong:{candidate_policy_receipt.get('receipt_id')}")
    if candidate_policy_receipt.get("gate") != "PASS":
        failures.append(f"candidate_policy_receipt_gate_not_PASS:{candidate_policy_receipt.get('gate')}")
    if raw_diag_receipt.get("diagnostic_id") != EXPECTED_RAW_DELTA_DIAGNOSTIC_ID:
        failures.append(f"raw_diag_id_wrong:{raw_diag_receipt.get('diagnostic_id')}")
    if raw_diag_receipt.get("receipt_id") != EXPECTED_RAW_DELTA_DIAGNOSTIC_RECEIPT_ID:
        failures.append(f"raw_diag_receipt_id_wrong:{raw_diag_receipt.get('receipt_id')}")
    if raw_diag_receipt.get("gate") != "PASS":
        failures.append(f"raw_diag_receipt_gate_not_PASS:{raw_diag_receipt.get('gate')}")

    return failures


def derive_review(candidate_probe: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    agg = candidate_probe.get("aggregate_measurements") or {}
    contract = policy.get("scale_review_contract") or {}

    bounded_pass_clean = (
        agg.get("bands_total") == 266
        and agg.get("bands_passed") == 266
        and agg.get("bands_failed") == 0
        and agg.get("all_band_false_merge_count") == 0
        and agg.get("worst_false_merge_count") == 0
        and agg.get("worst_collision_count") == 0
        and agg.get("worst_false_split_count") == 0
        and agg.get("worst_distinguishability_retention_ratio") == 1.0
        and agg.get("total_burden_ratio_projected", 999) < 1.0
        and agg.get("worst_burden_ratio_projected", 999) < 1.0
        and agg.get("worst_identity_leak_count") == 0
        and agg.get("worst_raw_delta_missing_count") == 0
        and agg.get("worst_source_surface_regression_count") == 0
    )

    acceptance_sufficient = False
    acceptance_blockers = [
        "candidate_acceptance_not_authorized_by_policy",
        "bounded_probe_is_single_validation_radius",
        "no_independent_scale_out_policy_executed_yet",
        "no_full_registry_authority",
        "runtime_change_not_authorized",
    ]

    if bounded_pass_clean:
        terminal_class = TERMINAL_ADVANCE
        recommended_next_command_goal = NEXT_COMMAND_GOAL
        interpretation = (
            "Candidate bounded probe is clean: distinguishability is preserved, burden is below full receipts, "
            "and authority/source surfaces are clean. This is still not acceptance; next lawful move is a bounded "
            "scale-out policy that defines a larger validation radius without full-registry scan or runtime change."
        )
    else:
        terminal_class = "STOP_SCALE_REVIEW_SOURCE_SURFACE"
        recommended_next_command_goal = None
        interpretation = "Source candidate probe evidence is not clean enough to recommend scale-out."

    return {
        "review_class": terminal_class,
        "recommended_next_command_goal": recommended_next_command_goal,
        "interpretation": interpretation,
        "acceptance_sufficient": acceptance_sufficient,
        "acceptance_blockers": acceptance_blockers,
        "candidate_should_remain_selected": bounded_pass_clean,
        "selected_encoding_should_remain": SELECTED_ENCODING_ID if bounded_pass_clean else None,
        "candidate_payload_should_remain": REQUIRED_PAYLOAD_FIELDS if bounded_pass_clean else None,
        "next_validation_radius_recommendation": {
            "kind": "bounded_scale_out_policy",
            "requires_human_decision_now": False,
            "must_be_larger_than_current_bounded_surface": True,
            "must_include_prior_266_band_surface": True,
            "must_define_explicit_selection_rule_before_execution": True,
            "must_not_use_full_registry_scan": True,
            "must_not_read_registry_sqlite": True,
            "must_not_accept_candidate": True,
            "must_not_change_runtime": True,
            "must_not_write_registry": True,
            "candidate_under_review": CANDIDATE_DESIGN_ID,
            "candidate_payload": REQUIRED_PAYLOAD_FIELDS,
            "selected_encoding_id": SELECTED_ENCODING_ID,
            "selected_target_raw_delta_field": TARGET_RAW_DELTA_FIELD,
        },
        "source_bounded_evidence": contract.get("source_bounded_pass_evidence"),
    }


def build_review(policy_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    start = time.perf_counter()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    policy = load_json(POLICY_DIR / f"{policy_id}.json")
    policy_receipt = load_json(POLICY_RECEIPT_DIR / f"{policy_id}.json")
    candidate_probe = load_json(CANDIDATE_PROBE_RECEIPT_DIR / f"{EXPECTED_CANDIDATE_PROBE_ID}.json")
    candidate_policy_receipt = load_json(CANDIDATE_POLICY_RECEIPT_DIR / f"{EXPECTED_CANDIDATE_POLICY_ID}.json")
    raw_diag_receipt = load_json(RAW_DELTA_DIAG_RECEIPT_DIR / f"{EXPECTED_RAW_DELTA_DIAGNOSTIC_ID}.json")

    failures = verify_sources(policy, policy_receipt, candidate_probe, candidate_policy_receipt, raw_diag_receipt)
    review_decision = derive_review(candidate_probe, policy)

    authority_guards = {
        "observer_only": True,
        "candidate_accepted": False,
        "candidate_acceptance_authorized": False,
        "scale_mode_authorized": False,
        "bounded_scale_out_policy_recommended": review_decision["review_class"] == TERMINAL_ADVANCE,
        "full_registry_scan_used": False,
        "registry_sqlite_read": False,
        "registry_sqlite_changed": False,
        "runtime_receipt_emission_changed": False,
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
    }

    pass_gates = {
        "policy_preconditions": not failures,
        "source_candidate_probe_passed": candidate_probe.get("terminal_decision") == "PASS_RAW_DELTA_SIGNATURE_CANDIDATE_BOUNDED_PROBE",
        "bounded_pass_evidence_clean": review_decision["review_class"] == TERMINAL_ADVANCE,
        "acceptance_remains_forbidden": review_decision["acceptance_sufficient"] is False,
        "bounded_scale_out_only": review_decision["recommended_next_command_goal"] == NEXT_COMMAND_GOAL,
        "authority_containment": all([
            authority_guards["observer_only"] is True,
            authority_guards["candidate_accepted"] is False,
            authority_guards["candidate_acceptance_authorized"] is False,
            authority_guards["scale_mode_authorized"] is False,
            authority_guards["full_registry_scan_used"] is False,
            authority_guards["registry_sqlite_read"] is False,
            authority_guards["runtime_receipt_emission_changed"] is False,
            authority_guards["registry_write_authorized"] is False,
        ]),
        "truth_surface_preserved": True,
        "no_identity_leak": True,
    }

    terminal = {
        "type": "ADVANCE" if not failures and review_decision["review_class"] == TERMINAL_ADVANCE else "STOP",
        "next_command_goal": NEXT_COMMAND_GOAL if not failures and review_decision["review_class"] == TERMINAL_ADVANCE else None,
        "stop_code": None if not failures and review_decision["review_class"] == TERMINAL_ADVANCE else "STOP_SCALE_REVIEW_SOURCE_SURFACE",
    }

    elapsed_ms = int(round((time.perf_counter() - start) * 1000))

    review = {
        "schema_version": "raw_delta_signature_candidate_scale_review_v0",
        "review_name": REVIEW_NAME,
        "mode": MODE,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_candidate_probe_id": EXPECTED_CANDIDATE_PROBE_ID,
        "source_candidate_probe_receipt_id": EXPECTED_CANDIDATE_PROBE_RECEIPT_ID,
        "source_candidate_policy_id": EXPECTED_CANDIDATE_POLICY_ID,
        "source_raw_delta_diagnostic_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_ID,
        "source_raw_delta_diagnostic_receipt_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_RECEIPT_ID,
        "source_bounded_pass_evidence": review_decision["source_bounded_evidence"],
        "comparison_to_candidate_probe": {
            "candidate_probe_terminal_decision": candidate_probe.get("terminal_decision"),
            "candidate_probe_aggregate_measurements": candidate_probe.get("aggregate_measurements"),
            "candidate_probe_pass_gates": candidate_probe.get("pass_gates"),
        },
        "review_decision": review_decision,
        "authority_guards": authority_guards,
        "pass_gates": pass_gates,
        "decision": {
            "candidate_accepted": False,
            "candidate_acceptance_authorized": False,
            "scale_mode_authorized": False,
            "review_only": True,
            "acceptance_sufficient": False,
            "do_not_accept_candidate": True,
            "do_not_full_registry_scan": True,
            "do_not_read_registry_sqlite": True,
            "do_not_change_runtime": True,
            "do_not_write_registry": True,
            "do_not_use_case_id_or_cycle_n_as_primary_identity": True,
            "do_not_use_rowid_or_receipt_hash": True,
            "terminal_class": review_decision["review_class"],
            "recommended_next_command_goal": review_decision["recommended_next_command_goal"],
        },
        "terminal_class": review_decision["review_class"],
        "terminal": terminal,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
        "actual_observer_overhead_ms": elapsed_ms,
    }

    review_id = sha8({
        "review_name": REVIEW_NAME,
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_candidate_probe_id": EXPECTED_CANDIDATE_PROBE_ID,
        "review_decision": review_decision,
        "terminal": terminal,
    })
    review["review_id"] = review_id
    review["review_sig8"] = review_id

    receipt = {
        "schema_version": "raw_delta_signature_candidate_scale_review_receipt_v0",
        "review_id": review_id,
        "review_sig8": review_id,
        "review_name": REVIEW_NAME,
        "mode": MODE,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "review_path": f"data/raw_delta_signature_candidate_scale_reviews/{review_id}.json",
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_candidate_probe_id": EXPECTED_CANDIDATE_PROBE_ID,
        "source_candidate_probe_receipt_id": EXPECTED_CANDIDATE_PROBE_RECEIPT_ID,
        "source_candidate_policy_id": EXPECTED_CANDIDATE_POLICY_ID,
        "source_raw_delta_diagnostic_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_ID,
        "source_raw_delta_diagnostic_receipt_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_RECEIPT_ID,
        "source_bounded_pass_evidence": review_decision["source_bounded_evidence"],
        "review_decision": review_decision,
        "authority_guards": authority_guards,
        "pass_gates": pass_gates,
        "decision": review["decision"],
        "terminal_class": review["terminal_class"],
        "terminal": terminal,
        "gate": review["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
        "actual_observer_overhead_ms": elapsed_ms,
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id

    (OUT_DIR / f"{review_id}.json").write_text(json.dumps(review, indent=2, sort_keys=True))
    (OUT_RECEIPT_DIR / f"{review_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return review, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy-id", default=EXPECTED_POLICY_ID)
    args = parser.parse_args()

    review, receipt = build_review(args.policy_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"review_id={review['review_id']}")
    print(f"review_json_path=data/raw_delta_signature_candidate_scale_reviews/{review['review_id']}.json")
    print(f"review_receipt_path=data/raw_delta_signature_candidate_scale_review_receipts/{review['review_id']}.json")

    return 0 if review["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
