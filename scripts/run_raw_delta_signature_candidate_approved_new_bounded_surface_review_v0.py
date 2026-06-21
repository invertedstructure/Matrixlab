#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REVIEW_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_APPROVED_NEW_BOUNDED_SURFACE_REVIEW_V0"
POLICY_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_APPROVED_NEW_BOUNDED_SURFACE_REVIEW_POLICY_V0"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"

EXPECTED_POLICY_ID = "407df570"
EXPECTED_POLICY_RECEIPT_ID = "58813bc2"

APPROVED_SURFACE_PROBE_POLICY_ID = "a4e4d744"
APPROVED_SURFACE_PROBE_POLICY_RECEIPT_ID = "9061c1fb"
APPROVED_SURFACE_PROBE_ID = "87b4a010"
APPROVED_SURFACE_PROBE_RECEIPT_ID = "812ae591"
APPROVED_SURFACE_ID = "4427ba4b"
APPROVED_SURFACE_RECEIPT_ID = "e5022cd2"
APPROVED_SURFACE_RUN_ID = "run_20260621_183812_136149"

RAW_DELTA_CANDIDATE_POLICY_ID = "3b8eb867"
RAW_DELTA_CANDIDATE_POLICY_RECEIPT_ID = "6778ef03"
RAW_DELTA_CANDIDATE_PROBE_ID = "6a33c978"
RAW_DELTA_CANDIDATE_PROBE_RECEIPT_ID = "99c90fe3"

BOUNDED_SCALE_OUT_POLICY_ID = "189aab7f"
BOUNDED_SCALE_OUT_POLICY_RECEIPT_ID = "7f51bc70"
BOUNDED_SCALE_OUT_ID = "2b44b1fd"
BOUNDED_SCALE_OUT_RECEIPT_ID = "f67b629b"

POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_review_policies"
POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_review_policy_receipts"

APPROVED_PROBE_RESULT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_probe_results"
APPROVED_PROBE_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_probe_receipts"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_review_results"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_review_receipts"

NEXT_ACCEPTANCE_PROPOSAL_POLICY_GOAL = "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_ACCEPTANCE_PROPOSAL_POLICY_V0"
NEXT_MORE_SCALE_POLICY_GOAL = "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_ADDITIONAL_SCALE_POLICY_V0"
NEXT_DIAGNOSTIC_GOAL = "DIAGNOSE_RAW_DELTA_SIGNATURE_CANDIDATE_APPROVED_NEW_BOUNDED_SURFACE_REVIEW_FAILURE_V0"
ZERO_PRESERVING_SUMMARY_RESOLUTION_PATCH_ID = "PATCH_APPROVED_NEW_SURFACE_REVIEW_RUNNER_ZERO_PRESERVING_SUMMARY_RESOLUTION_V0"

FORBIDDEN_AUTHORITY_TRUE = [
    "runner_executed",
    "candidate_rows_created",
    "candidate_accepted",
    "scale_mode_authorized",
    "registry_inserted",
    "registry_written",
    "registry_sqlite_read",
    "full_registry_scan_used",
    "runtime_semantic_changed",
    "runtime_code_changed",
    "runtime_receipt_emission_changed",
    "latest_or_mtime_selection_used",
    "ambient_workspace_inference_used",
    "case_id_or_cycle_n_identity_patch_used",
    "rowid_or_receipt_hash_truth_surface_used",
    "full_occurrence_key_in_signature_payload",
    "audit_or_debug_payload_in_signature_payload",
    "microhash_as_proof_used",
    "synthetic_fake_validation_rows_used",
    "transition_compression_probe_run",
    "candidate_acceptance_proposal_emitted",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def blob(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")


def sha8(obj: Any) -> str:
    return hashlib.sha256(blob(obj)).hexdigest()[:8]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required json: {path}")
    return json.loads(path.read_text())


def metric(obj: dict[str, Any], key: str) -> Any:
    if key in obj:
        return obj.get(key)
    analysis = obj.get("analysis")
    if isinstance(analysis, dict) and key in analysis:
        return analysis.get(key)
    known = obj.get("known_result_summary")
    if isinstance(known, dict) and key in known:
        return known.get(key)
    return None


def first_present(mapping: dict[str, Any], *keys: str) -> Any:
    """Return the first present non-None value while preserving falsy values.

    This is required because 0 is evidence, not absence.
    Do not use `a or b` for numeric evidence fields.
    """
    for key in keys:
        if key in mapping and mapping.get(key) is not None:
            return mapping.get(key)
    return None


def validate_policy(policy: dict[str, Any], receipt: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if policy.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if policy.get("policy_receipt_id") != EXPECTED_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy.get('policy_receipt_id')}")
    if receipt.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"receipt_policy_id_wrong:{receipt.get('policy_id')}")
    if receipt.get("receipt_id") != EXPECTED_POLICY_RECEIPT_ID:
        failures.append(f"receipt_id_wrong:{receipt.get('receipt_id')}")

    if policy.get("gate") != "PASS":
        failures.append(f"policy_gate_not_PASS:{policy.get('gate')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{receipt.get('gate')}")
    if policy.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{policy.get('policy_status')}")
    if receipt.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_receipt_status_wrong:{receipt.get('policy_status')}")

    if policy.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"candidate_design_id_wrong:{policy.get('candidate_design_id')}")
    if receipt.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"receipt_candidate_design_id_wrong:{receipt.get('candidate_design_id')}")

    terminal = policy.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"policy_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != "RUN_RAW_DELTA_SIGNATURE_CANDIDATE_APPROVED_NEW_BOUNDED_SURFACE_REVIEW_V0":
        failures.append(f"policy_terminal_next_wrong:{terminal.get('next_command_goal')}")

    source_probe = policy.get("source_probe") or {}
    expected = {
        "policy_id": APPROVED_SURFACE_PROBE_POLICY_ID,
        "policy_receipt_id": APPROVED_SURFACE_PROBE_POLICY_RECEIPT_ID,
        "probe_id": APPROVED_SURFACE_PROBE_ID,
        "probe_receipt_id": APPROVED_SURFACE_PROBE_RECEIPT_ID,
        "source_surface_id": APPROVED_SURFACE_ID,
        "source_surface_receipt_id": APPROVED_SURFACE_RECEIPT_ID,
        "source_run_id": APPROVED_SURFACE_RUN_ID,
    }
    for key, value in expected.items():
        if source_probe.get(key) != value:
            failures.append(f"source_probe_{key}_wrong:{source_probe.get(key)}")

    evidence_ids = receipt.get("evidence_stack_ids") or {}
    if evidence_ids.get("approved_new_bounded_surface_probe") != APPROVED_SURFACE_PROBE_ID:
        failures.append(f"evidence_approved_probe_id_wrong:{evidence_ids.get('approved_new_bounded_surface_probe')}")
    if evidence_ids.get("prior_raw_delta_candidate_bounded_probe") != RAW_DELTA_CANDIDATE_PROBE_ID:
        failures.append(f"evidence_prior_probe_id_wrong:{evidence_ids.get('prior_raw_delta_candidate_bounded_probe')}")
    if evidence_ids.get("bounded_scale_out_replay") != BOUNDED_SCALE_OUT_ID:
        failures.append(f"evidence_scale_out_id_wrong:{evidence_ids.get('bounded_scale_out_replay')}")

    classification = receipt.get("pre_review_classification") or {}
    for key in [
        "approved_new_surface_probe_pass_clean",
        "current_surface_distinguishability_clean",
        "current_surface_burden_reduction_clean",
        "acceptance_not_authorized_here",
    ]:
        if classification.get(key) is not True:
            failures.append(f"pre_review_classification_not_true:{key}:{classification.get(key)}")

    if classification.get("probe_result_schema_resolution_patch_id") != "PATCH_APPROVED_NEW_SURFACE_REVIEW_POLICY_PROBE_RESULT_SCHEMA_RESOLUTION_V0":
        failures.append(f"schema_resolution_patch_missing_or_wrong:{classification.get('probe_result_schema_resolution_patch_id')}")

    forbidden = policy.get("forbidden_operations") or {}
    for key, value in forbidden.items():
        if value is not True:
            failures.append(f"forbidden_operation_not_true:{key}:{value}")

    guards = receipt.get("authority_guards") or {}
    for key in FORBIDDEN_AUTHORITY_TRUE:
        if guards.get(key) is not False:
            failures.append(f"policy_authority_guard_not_false:{key}:{guards.get(key)}")

    return failures


def validate_approved_current_probe(result: dict[str, Any], receipt: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    failures: list[str] = []

    for obj_name, obj in [("result", result), ("receipt", receipt)]:
        if obj.get("gate") != "PASS":
            failures.append(f"approved_probe_{obj_name}_gate_not_PASS:{obj.get('gate')}")
        if obj.get("policy_id") != APPROVED_SURFACE_PROBE_POLICY_ID:
            failures.append(f"approved_probe_{obj_name}_policy_id_wrong:{obj.get('policy_id')}")
        if obj.get("policy_receipt_id") != APPROVED_SURFACE_PROBE_POLICY_RECEIPT_ID:
            failures.append(f"approved_probe_{obj_name}_policy_receipt_id_wrong:{obj.get('policy_receipt_id')}")
        if obj.get("source_surface_id") != APPROVED_SURFACE_ID:
            failures.append(f"approved_probe_{obj_name}_surface_id_wrong:{obj.get('source_surface_id')}")
        if obj.get("source_surface_receipt_id") != APPROVED_SURFACE_RECEIPT_ID:
            failures.append(f"approved_probe_{obj_name}_surface_receipt_id_wrong:{obj.get('source_surface_receipt_id')}")
        if obj.get("source_run_id") != APPROVED_SURFACE_RUN_ID:
            failures.append(f"approved_probe_{obj_name}_run_id_wrong:{obj.get('source_run_id')}")
        if metric(obj, "rows_total") != 500:
            failures.append(f"approved_probe_{obj_name}_rows_total_wrong:{metric(obj, 'rows_total')}")
        if metric(obj, "distinct_full_occurrence_keys") != 500:
            failures.append(f"approved_probe_{obj_name}_distinct_full_wrong:{metric(obj, 'distinct_full_occurrence_keys')}")
        if metric(obj, "distinct_candidate_delta_signatures") != 500:
            failures.append(f"approved_probe_{obj_name}_distinct_sig_wrong:{metric(obj, 'distinct_candidate_delta_signatures')}")
        if metric(obj, "false_merge_count") != 0:
            failures.append(f"approved_probe_{obj_name}_false_merge_not_zero:{metric(obj, 'false_merge_count')}")
        if metric(obj, "collision_count") != 0:
            failures.append(f"approved_probe_{obj_name}_collision_not_zero:{metric(obj, 'collision_count')}")
        if metric(obj, "false_split_count") != 0:
            failures.append(f"approved_probe_{obj_name}_false_split_not_zero:{metric(obj, 'false_split_count')}")
        if metric(obj, "retention") != 1.0:
            failures.append(f"approved_probe_{obj_name}_retention_not_one:{metric(obj, 'retention')}")

    if not (0 < float(receipt.get("burden_ratio_payload_to_source_rows", 999)) < 1):
        failures.append(f"approved_probe_payload_burden_not_reduced:{receipt.get('burden_ratio_payload_to_source_rows')}")
    if not (0 < float(receipt.get("burden_ratio_candidate_payload_to_source_rows", 999)) < 1):
        failures.append(f"approved_probe_candidate_payload_burden_not_reduced:{receipt.get('burden_ratio_candidate_payload_to_source_rows')}")

    guards = receipt.get("authority_guards") or {}
    for key in [
        "runner_executed",
        "candidate_rows_created",
        "candidate_accepted",
        "scale_mode_authorized",
        "registry_inserted",
        "registry_written",
        "registry_sqlite_read",
        "full_registry_scan_used",
        "runtime_semantic_changed",
        "runtime_code_changed",
        "runtime_receipt_emission_changed",
        "latest_or_mtime_selection_used",
        "ambient_workspace_inference_used",
        "case_id_or_cycle_n_identity_patch_used",
        "rowid_or_receipt_hash_truth_surface_used",
        "full_occurrence_key_in_signature_payload",
        "audit_or_debug_payload_in_signature_payload",
        "microhash_as_proof_used",
        "synthetic_fake_validation_rows_used",
    ]:
        if guards.get(key) is not False:
            failures.append(f"approved_probe_authority_guard_not_false:{key}:{guards.get(key)}")
    if guards.get("transition_compression_probe_run") is not True:
        failures.append(f"approved_probe_transition_compression_probe_run_not_true:{guards.get('transition_compression_probe_run')}")

    summary = {
        "evidence_id": APPROVED_SURFACE_PROBE_ID,
        "receipt_id": APPROVED_SURFACE_PROBE_RECEIPT_ID,
        "source": "artifact",
        "gate": receipt.get("gate"),
        "rows_total": receipt.get("rows_total"),
        "distinct_full_occurrence_keys": receipt.get("distinct_full_occurrence_keys"),
        "distinct_candidate_delta_signatures": receipt.get("distinct_candidate_delta_signatures"),
        "false_merge_count": receipt.get("false_merge_count"),
        "collision_count": receipt.get("collision_count"),
        "false_split_count": receipt.get("false_split_count"),
        "retention": receipt.get("retention"),
        "burden_ratio_payload_to_source_rows": receipt.get("burden_ratio_payload_to_source_rows"),
        "burden_ratio_candidate_payload_to_source_rows": receipt.get("burden_ratio_candidate_payload_to_source_rows"),
        "clean": not failures,
    }
    return failures, summary


def named_policy_summary(policy: dict[str, Any], key: str) -> dict[str, Any]:
    stack = policy.get("evidence_stack") or {}
    evidence = stack.get(key) or {}
    known = evidence.get("known_result_summary") or {}
    return {
        "evidence_id": (
            evidence.get("probe_id")
            or evidence.get("scale_out_id")
            or key
        ),
        "receipt_id": (
            evidence.get("probe_receipt_id")
            or evidence.get("scale_out_receipt_id")
        ),
        "source": "policy_known_result_summary",
        "gate": known.get("gate"),
        "terminal": known.get("terminal"),
        "bands_total": first_present(known, "bands_total", "replayed_prior_surface_bands"),
        "bands_passed": first_present(known, "bands_passed"),
        "bands_failed": first_present(known, "bands_failed", "replayed_prior_surface_failed"),
        "false_merge_count": first_present(known, "false_merge_count"),
        "collision_count": first_present(known, "collision_count"),
        "false_split_count": first_present(known, "false_split_count"),
        "retention": first_present(known, "retention"),
        "total_burden_ratio_projected": first_present(known, "total_burden_ratio_projected"),
        "worst_burden_ratio_projected": first_present(known, "worst_burden_ratio_projected"),
        "additional_candidate_rows_selected": first_present(known, "additional_candidate_rows_selected"),
        "new_bands_evaluated": first_present(known, "new_bands_evaluated"),
        "review_requirement": evidence.get("review_requirement"),
    }


def clean_prior_probe(summary: dict[str, Any]) -> bool:
    return (
        summary.get("gate") == "PASS"
        and summary.get("false_merge_count") == 0
        and summary.get("collision_count") == 0
        and summary.get("false_split_count") == 0
        and summary.get("retention") == 1.0
        and summary.get("bands_failed") == 0
        and summary.get("total_burden_ratio_projected") is not None
        and float(summary["total_burden_ratio_projected"]) < 1
        and summary.get("worst_burden_ratio_projected") is not None
        and float(summary["worst_burden_ratio_projected"]) < 1
    )


def clean_scale_out(summary: dict[str, Any]) -> bool:
    return (
        summary.get("gate") == "PASS"
        and summary.get("terminal") == "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY"
        and summary.get("false_merge_count") == 0
        and summary.get("collision_count") == 0
        and summary.get("false_split_count") == 0
        and summary.get("retention") == 1.0
        and summary.get("bands_failed") == 0
        and summary.get("total_burden_ratio_projected") is not None
        and float(summary["total_burden_ratio_projected"]) < 1
        and summary.get("worst_burden_ratio_projected") is not None
        and float(summary["worst_burden_ratio_projected"]) < 1
        and summary.get("additional_candidate_rows_selected") == 0
        and summary.get("new_bands_evaluated") == 0
    )


def build_review(policy_id: str, write_outputs: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    if policy_id != EXPECTED_POLICY_ID:
        raise SystemExit(f"unsupported review policy id: {policy_id}")

    if write_outputs:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    policy = load_json(POLICY_DIR / f"{policy_id}.json")
    policy_receipt = load_json(POLICY_RECEIPT_DIR / f"{policy_id}.json")
    approved_probe_result = load_json(APPROVED_PROBE_RESULT_DIR / f"{APPROVED_SURFACE_PROBE_ID}.json")
    approved_probe_receipt = load_json(APPROVED_PROBE_RECEIPT_DIR / f"{APPROVED_SURFACE_PROBE_ID}.json")

    failures = validate_policy(policy, policy_receipt)
    current_failures, current_summary = validate_approved_current_probe(approved_probe_result, approved_probe_receipt)
    failures.extend(current_failures)

    prior_summary = named_policy_summary(policy, "prior_raw_delta_candidate_bounded_probe")
    scale_out_summary = named_policy_summary(policy, "bounded_scale_out_replay")

    prior_clean = clean_prior_probe(prior_summary)
    scale_out_clean = clean_scale_out(scale_out_summary)

    if not prior_clean:
        failures.append(f"prior_raw_delta_candidate_bounded_probe_not_clean:{prior_summary}")
    if not scale_out_clean:
        failures.append(f"bounded_scale_out_replay_not_clean:{scale_out_summary}")

    current_clean = current_summary.get("clean") is True
    no_false_merges_any_available_surface = (
        current_summary.get("false_merge_count") == 0
        and prior_summary.get("false_merge_count") == 0
        and scale_out_summary.get("false_merge_count") == 0
        and current_summary.get("collision_count") == 0
        and prior_summary.get("collision_count") == 0
        and scale_out_summary.get("collision_count") == 0
        and current_summary.get("false_split_count") == 0
        and prior_summary.get("false_split_count") == 0
        and scale_out_summary.get("false_split_count") == 0
    )

    burden_reduction_confirmed_any_available_surface = (
        0 < float(current_summary.get("burden_ratio_payload_to_source_rows", 999)) < 1
        and 0 < float(current_summary.get("burden_ratio_candidate_payload_to_source_rows", 999)) < 1
        and float(prior_summary.get("total_burden_ratio_projected", 999)) < 1
        and float(scale_out_summary.get("total_burden_ratio_projected", 999)) < 1
    )

    evidence_decision_conditions = {
        "approved_new_bounded_surface_probe_PASS": current_clean,
        "prior_raw_delta_candidate_bounded_probe_PASS_or_explicitly_resolved_unavailable": prior_clean,
        "bounded_scale_out_replay_PASS_or_explicitly_resolved_unavailable": scale_out_clean,
        "no_false_merges_any_available_surface": no_false_merges_any_available_surface,
        "burden_reduction_confirmed_any_available_surface": burden_reduction_confirmed_any_available_surface,
        "authority_guards_clean": not any("authority_guard" in f for f in failures),
        "candidate_acceptance_not_authorized_here": True,
        "candidate_acceptance_proposal_only": True,
    }

    all_clean_for_acceptance_proposal = not failures and all(evidence_decision_conditions.values())

    if all_clean_for_acceptance_proposal:
        terminal_class = "ADVANCE_TO_ACCEPTANCE_PROPOSAL_POLICY"
        terminal = {
            "type": "ADVANCE",
            "stop_code": None,
            "next_command_goal": NEXT_ACCEPTANCE_PROPOSAL_POLICY_GOAL,
        }
        review_decision = "EMIT_ACCEPTANCE_PROPOSAL_POLICY_NEXT"
    elif not failures and current_clean:
        terminal_class = "ADVANCE_TO_MORE_SCALE_POLICY"
        terminal = {
            "type": "ADVANCE",
            "stop_code": None,
            "next_command_goal": NEXT_MORE_SCALE_POLICY_GOAL,
        }
        review_decision = "REQUEST_MORE_SCALE_POLICY_NEXT"
    else:
        terminal_class = "STOP_TO_DIAGNOSTIC"
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_APPROVED_NEW_BOUNDED_SURFACE_REVIEW_FAILED",
            "next_command_goal": NEXT_DIAGNOSTIC_GOAL,
        }
        review_decision = "DIAGNOSE_REVIEW_FAILURE_NEXT"

    gate = "PASS" if terminal["type"] == "ADVANCE" and not failures else "FAIL"

    review_seed = {
        "review_name": REVIEW_NAME,
        "policy_id": policy_id,
        "policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "current_probe": current_summary,
        "prior_probe": prior_summary,
        "scale_out": scale_out_summary,
        "conditions": evidence_decision_conditions,
        "terminal_class": terminal_class,
    }
    review_id = sha8(review_seed)

    authority_guards = {
        "runner_executed": False,
        "candidate_rows_created": False,
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
        "candidate_acceptance_proposal_emitted": False,
    }

    result = {
        "schema_version": "raw_delta_signature_candidate_approved_new_bounded_surface_review_result_v0",
        "review_name": REVIEW_NAME,
        "review_id": review_id,
        "review_status": "FIXED_EVIDENCE_STACK_REVIEW_COMPLETE",
        "policy_id": policy_id,
        "policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "evidence_stack": {
            "approved_new_bounded_surface_probe": current_summary,
            "prior_raw_delta_candidate_bounded_probe": prior_summary,
            "bounded_scale_out_replay": scale_out_summary,
        },
        "evidence_decision_conditions": evidence_decision_conditions,
        "zero_preserving_summary_resolution_patch_id": ZERO_PRESERVING_SUMMARY_RESOLUTION_PATCH_ID,
        "review_decision": review_decision,
        "terminal_class": terminal_class,
        "terminal": terminal,
        "authority_guards": authority_guards,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt = {
        "schema_version": "raw_delta_signature_candidate_approved_new_bounded_surface_review_receipt_v0",
        "receipt_type": "APPROVED_NEW_BOUNDED_SURFACE_REVIEW_RECEIPT",
        "review_name": REVIEW_NAME,
        "review_id": review_id,
        "policy_id": policy_id,
        "policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_probe_id": APPROVED_SURFACE_PROBE_ID,
        "source_probe_receipt_id": APPROVED_SURFACE_PROBE_RECEIPT_ID,
        "source_surface_id": APPROVED_SURFACE_ID,
        "source_surface_receipt_id": APPROVED_SURFACE_RECEIPT_ID,
        "evidence_stack_ids": {
            "approved_new_bounded_surface_probe": APPROVED_SURFACE_PROBE_ID,
            "prior_raw_delta_candidate_bounded_probe": RAW_DELTA_CANDIDATE_PROBE_ID,
            "bounded_scale_out_replay": BOUNDED_SCALE_OUT_ID,
        },
        "current_probe": current_summary,
        "prior_probe": {
            "evidence_id": prior_summary.get("evidence_id"),
            "receipt_id": prior_summary.get("receipt_id"),
            "source": prior_summary.get("source"),
            "clean": prior_clean,
        },
        "bounded_scale_out_replay": {
            "evidence_id": scale_out_summary.get("evidence_id"),
            "receipt_id": scale_out_summary.get("receipt_id"),
            "source": scale_out_summary.get("source"),
            "clean": scale_out_clean,
        },
        "evidence_decision_conditions": evidence_decision_conditions,
        "zero_preserving_summary_resolution_patch_id": ZERO_PRESERVING_SUMMARY_RESOLUTION_PATCH_ID,
        "review_decision": review_decision,
        "terminal_class": terminal_class,
        "terminal": terminal,
        "authority_guards": authority_guards,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id
    result["receipt_id"] = receipt_id

    if write_outputs:
        (OUT_DIR / f"{review_id}.json").write_text(json.dumps(result, indent=2, sort_keys=True))
        (OUT_RECEIPT_DIR / f"{review_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return result, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy-id", default=EXPECTED_POLICY_ID)
    args = parser.parse_args()

    result, receipt = build_review(args.policy_id, write_outputs=True)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"review_id={result['review_id']}")
    print(f"review_receipt_id={receipt['receipt_id']}")
    print(f"review_path=data/raw_delta_signature_candidate_approved_new_bounded_surface_review_results/{result['review_id']}.json")
    print(f"review_receipt_path=data/raw_delta_signature_candidate_approved_new_bounded_surface_review_receipts/{result['review_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
