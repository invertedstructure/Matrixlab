#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

POLICY_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_APPROVED_NEW_BOUNDED_SURFACE_REVIEW_POLICY_V0"
POLICY_STATUS = "POLICY_ONLY_NOT_IMPLEMENTED"
REVIEW_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_APPROVED_NEW_BOUNDED_SURFACE_REVIEW_V0"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"

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

APPROVED_PROBE_RESULT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_probe_results"
APPROVED_PROBE_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_probe_receipts"
APPROVED_PROBE_POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_probe_policies"
APPROVED_PROBE_POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_probe_policy_receipts"

POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_review_policies"
POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_review_policy_receipts"

REQUIRED_PAYLOAD_FIELDS = [
    "cv",
    "state_hash_before",
    "move_id",
    "state_hash_after",
    "raw_compression_ratio_sig6",
]

FORBIDDEN_PAYLOAD_FIELDS = [
    "case_id",
    "cycle_n",
    "rowid",
    "receipt_hash",
    "receipt_path",
    "audit_pointer",
    "debug_payload",
    "full_occurrence_key",
    "registry_rowid",
]

NEXT_IMPLEMENTATION_GOAL = "RUN_RAW_DELTA_SIGNATURE_CANDIDATE_APPROVED_NEW_BOUNDED_SURFACE_REVIEW_V0"
PROBE_RESULT_SCHEMA_RESOLUTION_PATCH_ID = "PATCH_APPROVED_NEW_SURFACE_REVIEW_POLICY_PROBE_RESULT_SCHEMA_RESOLUTION_V0"

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


def probe_metric(obj: dict[str, Any], key: str) -> Any:
    """Resolve probe metrics from receipt top-level or result.analysis.*.

    Probe receipts expose rows/distinguishability metrics at top level.
    Probe result artifacts preserve the same metrics under the analysis object.
    This resolver is observer-only and does not mutate source artifacts.
    """
    if key in obj:
        return obj.get(key)
    analysis = obj.get("analysis")
    if isinstance(analysis, dict) and key in analysis:
        return analysis.get(key)
    return None


def validate_approved_probe(policy: dict[str, Any], policy_receipt: dict[str, Any], result: dict[str, Any], receipt: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if policy.get("policy_id") != APPROVED_SURFACE_PROBE_POLICY_ID:
        failures.append(f"approved_probe_policy_id_wrong:{policy.get('policy_id')}")
    if policy.get("policy_receipt_id") != APPROVED_SURFACE_PROBE_POLICY_RECEIPT_ID:
        failures.append(f"approved_probe_policy_receipt_id_wrong:{policy.get('policy_receipt_id')}")
    if policy_receipt.get("receipt_id") != APPROVED_SURFACE_PROBE_POLICY_RECEIPT_ID:
        failures.append(f"approved_probe_policy_receipt_wrong:{policy_receipt.get('receipt_id')}")
    if policy.get("gate") != "PASS":
        failures.append(f"approved_probe_policy_gate_not_PASS:{policy.get('gate')}")
    if policy_receipt.get("gate") != "PASS":
        failures.append(f"approved_probe_policy_receipt_gate_not_PASS:{policy_receipt.get('gate')}")
    if policy.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"approved_probe_policy_status_wrong:{policy.get('policy_status')}")

    if result.get("probe_id") != APPROVED_SURFACE_PROBE_ID:
        failures.append(f"approved_probe_result_id_wrong:{result.get('probe_id')}")
    if receipt.get("probe_id") != APPROVED_SURFACE_PROBE_ID:
        failures.append(f"approved_probe_receipt_probe_id_wrong:{receipt.get('probe_id')}")
    if result.get("receipt_id") != APPROVED_SURFACE_PROBE_RECEIPT_ID:
        failures.append(f"approved_probe_result_receipt_id_wrong:{result.get('receipt_id')}")
    if receipt.get("receipt_id") != APPROVED_SURFACE_PROBE_RECEIPT_ID:
        failures.append(f"approved_probe_receipt_id_wrong:{receipt.get('receipt_id')}")

    for obj_name, obj in [("result", result), ("receipt", receipt)]:
        if obj.get("gate") != "PASS":
            failures.append(f"approved_probe_{obj_name}_gate_not_PASS:{obj.get('gate')}")
        if obj.get("terminal_class") != "PASS_APPROVED_NEW_BOUNDED_SURFACE_PROBE":
            failures.append(f"approved_probe_{obj_name}_terminal_class_wrong:{obj.get('terminal_class')}")
        if obj.get("policy_id") != APPROVED_SURFACE_PROBE_POLICY_ID:
            failures.append(f"approved_probe_{obj_name}_policy_id_wrong:{obj.get('policy_id')}")
        if obj.get("policy_receipt_id") != APPROVED_SURFACE_PROBE_POLICY_RECEIPT_ID:
            failures.append(f"approved_probe_{obj_name}_policy_receipt_id_wrong:{obj.get('policy_receipt_id')}")
        if obj.get("source_surface_id") != APPROVED_SURFACE_ID:
            failures.append(f"approved_probe_{obj_name}_source_surface_id_wrong:{obj.get('source_surface_id')}")
        if obj.get("source_surface_receipt_id") != APPROVED_SURFACE_RECEIPT_ID:
            failures.append(f"approved_probe_{obj_name}_source_surface_receipt_id_wrong:{obj.get('source_surface_receipt_id')}")
        if obj.get("source_run_id") != APPROVED_SURFACE_RUN_ID:
            failures.append(f"approved_probe_{obj_name}_source_run_id_wrong:{obj.get('source_run_id')}")
        rows_total = probe_metric(obj, "rows_total")
        distinct_full = probe_metric(obj, "distinct_full_occurrence_keys")
        distinct_sig = probe_metric(obj, "distinct_candidate_delta_signatures")
        false_merge = probe_metric(obj, "false_merge_count")
        collision = probe_metric(obj, "collision_count")
        false_split = probe_metric(obj, "false_split_count")
        retention = probe_metric(obj, "retention")

        if rows_total != 500:
            failures.append(f"approved_probe_{obj_name}_rows_total_wrong:{rows_total}")
        if distinct_full != 500:
            failures.append(f"approved_probe_{obj_name}_distinct_full_wrong:{distinct_full}")
        if distinct_sig != 500:
            failures.append(f"approved_probe_{obj_name}_distinct_sig_wrong:{distinct_sig}")
        if false_merge != 0:
            failures.append(f"approved_probe_{obj_name}_false_merge_not_zero:{false_merge}")
        if collision != 0:
            failures.append(f"approved_probe_{obj_name}_collision_not_zero:{collision}")
        if false_split != 0:
            failures.append(f"approved_probe_{obj_name}_false_split_not_zero:{false_split}")
        if retention != 1.0:
            failures.append(f"approved_probe_{obj_name}_retention_not_one:{retention}")
        terminal = obj.get("terminal") or {}
        if terminal.get("type") != "ADVANCE":
            failures.append(f"approved_probe_{obj_name}_terminal_not_ADVANCE:{terminal}")
        if terminal.get("next_command_goal") != "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_APPROVED_NEW_BOUNDED_SURFACE_REVIEW_POLICY_V0":
            failures.append(f"approved_probe_{obj_name}_terminal_next_wrong:{terminal.get('next_command_goal')}")

    pass_conditions = receipt.get("pass_conditions") or {}
    for key in [
        "rows_equal_500",
        "full_occurrence_keys_equal_rows",
        "candidate_signatures_equal_rows",
        "false_merge_count_zero",
        "collision_count_zero",
        "false_split_count_zero",
        "retention_equal_1",
        "payload_schema_valid",
        "authority_guards_clean",
        "policy_valid",
        "source_valid",
    ]:
        if pass_conditions.get(key) is not True:
            failures.append(f"approved_probe_pass_condition_not_true:{key}:{pass_conditions.get(key)}")

    guards = receipt.get("authority_guards") or {}
    for key in FORBIDDEN_AUTHORITY_TRUE:
        if guards.get(key) is not False:
            failures.append(f"approved_probe_authority_guard_not_false:{key}:{guards.get(key)}")
    if guards.get("transition_compression_probe_run") is not True:
        failures.append(f"approved_probe_transition_probe_not_true:{guards.get('transition_compression_probe_run')}")

    if not (0 < float(receipt.get("burden_ratio_payload_to_source_rows", 999)) < 1):
        failures.append(f"approved_probe_payload_burden_ratio_not_reduced:{receipt.get('burden_ratio_payload_to_source_rows')}")
    if not (0 < float(receipt.get("burden_ratio_candidate_payload_to_source_rows", 999)) < 1):
        failures.append(f"approved_probe_candidate_payload_burden_ratio_not_reduced:{receipt.get('burden_ratio_candidate_payload_to_source_rows')}")

    return failures


def build_policy(policy_id: str, write_outputs: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    if policy_id != APPROVED_SURFACE_PROBE_POLICY_ID:
        raise SystemExit(f"unsupported approved surface probe policy id: {policy_id}")

    if write_outputs:
        POLICY_DIR.mkdir(parents=True, exist_ok=True)
        POLICY_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    approved_probe_policy = load_json(APPROVED_PROBE_POLICY_DIR / f"{APPROVED_SURFACE_PROBE_POLICY_ID}.json")
    approved_probe_policy_receipt = load_json(APPROVED_PROBE_POLICY_RECEIPT_DIR / f"{APPROVED_SURFACE_PROBE_POLICY_ID}.json")
    approved_probe_result = load_json(APPROVED_PROBE_RESULT_DIR / f"{APPROVED_SURFACE_PROBE_ID}.json")
    approved_probe_receipt = load_json(APPROVED_PROBE_RECEIPT_DIR / f"{APPROVED_SURFACE_PROBE_ID}.json")

    failures = validate_approved_probe(
        approved_probe_policy,
        approved_probe_policy_receipt,
        approved_probe_result,
        approved_probe_receipt,
    )

    evidence_stack = {
        "approved_new_bounded_surface_probe": {
            "policy_id": APPROVED_SURFACE_PROBE_POLICY_ID,
            "policy_receipt_id": APPROVED_SURFACE_PROBE_POLICY_RECEIPT_ID,
            "probe_id": APPROVED_SURFACE_PROBE_ID,
            "probe_receipt_id": APPROVED_SURFACE_PROBE_RECEIPT_ID,
            "source_surface_id": APPROVED_SURFACE_ID,
            "source_surface_receipt_id": APPROVED_SURFACE_RECEIPT_ID,
            "source_run_id": APPROVED_SURFACE_RUN_ID,
            "rows_total": approved_probe_receipt.get("rows_total"),
            "false_merge_count": approved_probe_receipt.get("false_merge_count"),
            "collision_count": approved_probe_receipt.get("collision_count"),
            "false_split_count": approved_probe_receipt.get("false_split_count"),
            "retention": approved_probe_receipt.get("retention"),
            "burden_ratio_payload_to_source_rows": approved_probe_receipt.get("burden_ratio_payload_to_source_rows"),
            "burden_ratio_candidate_payload_to_source_rows": approved_probe_receipt.get("burden_ratio_candidate_payload_to_source_rows"),
            "gate": approved_probe_receipt.get("gate"),
        },
        "prior_raw_delta_candidate_bounded_probe": {
            "policy_id": RAW_DELTA_CANDIDATE_POLICY_ID,
            "policy_receipt_id": RAW_DELTA_CANDIDATE_POLICY_RECEIPT_ID,
            "probe_id": RAW_DELTA_CANDIDATE_PROBE_ID,
            "probe_receipt_id": RAW_DELTA_CANDIDATE_PROBE_RECEIPT_ID,
            "known_result_summary": {
                "gate": "PASS",
                "bands_total": 266,
                "bands_passed": 266,
                "bands_failed": 0,
                "false_merge_count": 0,
                "collision_count": 0,
                "false_split_count": 0,
                "retention": 1.0,
                "total_burden_ratio_projected": 0.5139198851,
                "worst_burden_ratio_projected": 0.5205640423,
            },
            "review_requirement": "implementation_must_resolve_or_mark_unavailable_without_registry_scan",
        },
        "bounded_scale_out_replay": {
            "policy_id": BOUNDED_SCALE_OUT_POLICY_ID,
            "policy_receipt_id": BOUNDED_SCALE_OUT_POLICY_RECEIPT_ID,
            "scale_out_id": BOUNDED_SCALE_OUT_ID,
            "scale_out_receipt_id": BOUNDED_SCALE_OUT_RECEIPT_ID,
            "known_result_summary": {
                "gate": "PASS",
                "terminal": "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY",
                "replayed_prior_surface_bands": 266,
                "replayed_prior_surface_failed": 0,
                "false_merge_count": 0,
                "collision_count": 0,
                "false_split_count": 0,
                "retention": 1.0,
                "total_burden_ratio_projected": 0.3779571395,
                "worst_burden_ratio_projected": 0.3819036428,
                "additional_candidate_rows_selected": 0,
                "new_bands_evaluated": 0,
            },
            "review_requirement": "implementation_must_resolve_or_mark_unavailable_without_registry_scan",
        },
    }

    policy_seed = {
        "policy_name": POLICY_NAME,
        "review_name": REVIEW_NAME,
        "approved_probe_policy_id": APPROVED_SURFACE_PROBE_POLICY_ID,
        "approved_probe_id": APPROVED_SURFACE_PROBE_ID,
        "approved_probe_receipt_id": APPROVED_SURFACE_PROBE_RECEIPT_ID,
        "source_surface_id": APPROVED_SURFACE_ID,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "review_inputs": evidence_stack,
    }
    review_policy_id = sha8(policy_seed)

    approved_probe_pass_clean = not failures
    current_probe_summary = evidence_stack["approved_new_bounded_surface_probe"]

    policy = {
        "schema_version": "raw_delta_signature_candidate_approved_new_bounded_surface_review_policy_v0",
        "policy_name": POLICY_NAME,
        "policy_id": review_policy_id,
        "policy_status": POLICY_STATUS,
        "review_name": REVIEW_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_probe": {
            "policy_id": APPROVED_SURFACE_PROBE_POLICY_ID,
            "policy_receipt_id": APPROVED_SURFACE_PROBE_POLICY_RECEIPT_ID,
            "probe_id": APPROVED_SURFACE_PROBE_ID,
            "probe_receipt_id": APPROVED_SURFACE_PROBE_RECEIPT_ID,
            "source_surface_id": APPROVED_SURFACE_ID,
            "source_surface_receipt_id": APPROVED_SURFACE_RECEIPT_ID,
            "source_run_id": APPROVED_SURFACE_RUN_ID,
        },
        "evidence_stack": evidence_stack,
        "review_contract": {
            "purpose": "decide next lawful post-probe move without accepting candidate",
            "probe_result_schema_resolution_patch": PROBE_RESULT_SCHEMA_RESOLUTION_PATCH_ID,
            "probe_result_metric_resolution": {
                "receipt_metrics": "top_level",
                "result_metrics": "top_level_or_analysis_fallback",
                "mutation": "none",
            },
            "allowed_inputs": {
                "approved_new_bounded_surface_probe_result": rel(APPROVED_PROBE_RESULT_DIR / f"{APPROVED_SURFACE_PROBE_ID}.json"),
                "approved_new_bounded_surface_probe_receipt": rel(APPROVED_PROBE_RECEIPT_DIR / f"{APPROVED_SURFACE_PROBE_ID}.json"),
                "approved_new_bounded_surface_probe_policy": rel(APPROVED_PROBE_POLICY_DIR / f"{APPROVED_SURFACE_PROBE_POLICY_ID}.json"),
                "approved_new_bounded_surface_probe_policy_receipt": rel(APPROVED_PROBE_POLICY_RECEIPT_DIR / f"{APPROVED_SURFACE_PROBE_POLICY_ID}.json"),
            },
            "required_current_probe_conditions": {
                "gate": "PASS",
                "rows_total": 500,
                "distinct_full_occurrence_keys": 500,
                "distinct_candidate_delta_signatures": 500,
                "false_merge_count": 0,
                "collision_count": 0,
                "false_split_count": 0,
                "retention": 1.0,
                "burden_ratio_payload_to_source_rows_lt_1": True,
                "burden_ratio_candidate_payload_to_source_rows_lt_1": True,
            },
            "review_decision_space": {
                "emit_acceptance_proposal": {
                    "allowed": True,
                    "requires": [
                        "approved_new_bounded_surface_probe_PASS",
                        "prior_raw_delta_candidate_bounded_probe_PASS_or_explicitly_resolved_unavailable",
                        "bounded_scale_out_replay_PASS_or_explicitly_resolved_unavailable",
                        "no_false_merges_any_available_surface",
                        "burden_reduction_confirmed_any_available_surface",
                        "authority_guards_clean",
                    ],
                    "effect": "proposal_only_human_boundary_required",
                },
                "request_more_scale": {
                    "allowed": True,
                    "requires": [
                        "evidence_is_clean_but_inventory_or_scope judged insufficient",
                        "no_candidate_acceptance",
                    ],
                    "effect": "policy_or_proposal_for_more_scale_only",
                },
                "diagnose_failure": {
                    "allowed": True,
                    "requires": [
                        "any current or required evidence gate fails",
                    ],
                    "effect": "diagnostic_only",
                },
            },
            "required_output": {
                "review_result": True,
                "review_receipt": True,
                "terminal_must_be_one_of": [
                    "ADVANCE_TO_ACCEPTANCE_PROPOSAL_POLICY",
                    "ADVANCE_TO_MORE_SCALE_POLICY",
                    "STOP_TO_DIAGNOSTIC",
                ],
            },
        },
        "authorized_operations_next": {
            "read_approved_probe_policy": True,
            "read_approved_probe_policy_receipt": True,
            "read_approved_probe_result": True,
            "read_approved_probe_receipt": True,
            "write_review_result": True,
            "write_review_receipt": True,
            "resolve_prior_named_evidence_by_explicit_known_ids_only": True,
        },
        "forbidden_operations": {
            "candidate_acceptance": True,
            "candidate_registry_insert": True,
            "candidate_registry_write": True,
            "registry_sqlite_read": True,
            "full_registry_scan": True,
            "scale_mode": True,
            "runner_execution": True,
            "runtime_code_change": True,
            "runtime_semantic_change": True,
            "runtime_receipt_emission_change": True,
            "latest_or_mtime_selection": True,
            "ambient_workspace_inference": True,
            "synthetic_fake_rows": True,
            "case_id_or_cycle_n_identity_patch": True,
            "rowid_or_receipt_hash_truth_surface": True,
            "full_occurrence_key_in_signature_payload": True,
            "audit_or_debug_payload_in_signature_payload": True,
            "microhash_as_proof": True,
        },
        "current_probe_summary": current_probe_summary,
        "pre_review_classification": {
            "probe_result_schema_resolution_patch_id": PROBE_RESULT_SCHEMA_RESOLUTION_PATCH_ID,
            "approved_new_surface_probe_pass_clean": approved_probe_pass_clean,
            "current_surface_distinguishability_clean": (
                current_probe_summary.get("false_merge_count") == 0
                and current_probe_summary.get("collision_count") == 0
                and current_probe_summary.get("false_split_count") == 0
                and current_probe_summary.get("retention") == 1.0
            ),
            "current_surface_burden_reduction_clean": (
                float(current_probe_summary.get("burden_ratio_payload_to_source_rows", 999)) < 1
                and float(current_probe_summary.get("burden_ratio_candidate_payload_to_source_rows", 999)) < 1
            ),
            "acceptance_not_authorized_here": True,
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "stop_code": None if not failures else "STOP_APPROVED_NEW_BOUNDED_SURFACE_REVIEW_POLICY_INVALID_SOURCE",
            "next_command_goal": NEXT_IMPLEMENTATION_GOAL if not failures else None,
        },
        "authority_guards": {
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
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt = {
        "schema_version": "raw_delta_signature_candidate_approved_new_bounded_surface_review_policy_receipt_v0",
        "receipt_type": "APPROVED_NEW_BOUNDED_SURFACE_REVIEW_POLICY_RECEIPT",
        "policy_id": review_policy_id,
        "policy_name": POLICY_NAME,
        "policy_status": POLICY_STATUS,
        "review_name": REVIEW_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_probe_policy_id": APPROVED_SURFACE_PROBE_POLICY_ID,
        "source_probe_policy_receipt_id": APPROVED_SURFACE_PROBE_POLICY_RECEIPT_ID,
        "source_probe_id": APPROVED_SURFACE_PROBE_ID,
        "source_probe_receipt_id": APPROVED_SURFACE_PROBE_RECEIPT_ID,
        "source_surface_id": APPROVED_SURFACE_ID,
        "source_surface_receipt_id": APPROVED_SURFACE_RECEIPT_ID,
        "source_run_id": APPROVED_SURFACE_RUN_ID,
        "evidence_stack_ids": {
            "approved_new_bounded_surface_probe": APPROVED_SURFACE_PROBE_ID,
            "prior_raw_delta_candidate_bounded_probe": RAW_DELTA_CANDIDATE_PROBE_ID,
            "bounded_scale_out_replay": BOUNDED_SCALE_OUT_ID,
        },
        "pre_review_classification": policy["pre_review_classification"],
        "authorized_next": policy["authorized_operations_next"],
        "forbidden_operations": policy["forbidden_operations"],
        "terminal": policy["terminal"],
        "authority_guards": policy["authority_guards"],
        "gate": policy["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id
    policy["policy_receipt_id"] = receipt_id

    if write_outputs:
        (POLICY_DIR / f"{review_policy_id}.json").write_text(json.dumps(policy, indent=2, sort_keys=True))
        (POLICY_RECEIPT_DIR / f"{review_policy_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return policy, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--approved-probe-policy-id", default=APPROVED_SURFACE_PROBE_POLICY_ID)
    args = parser.parse_args()

    policy, receipt = build_policy(args.approved_probe_policy_id, write_outputs=True)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_id={policy['policy_id']}")
    print(f"policy_receipt_id={receipt['receipt_id']}")
    print(f"policy_path=data/raw_delta_signature_candidate_approved_new_bounded_surface_review_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/raw_delta_signature_candidate_approved_new_bounded_surface_review_policy_receipts/{policy['policy_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
