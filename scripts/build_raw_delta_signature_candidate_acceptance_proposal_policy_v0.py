#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

POLICY_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_ACCEPTANCE_PROPOSAL_POLICY_V0"
POLICY_STATUS = "POLICY_ONLY_NOT_IMPLEMENTED"
PROPOSAL_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_ACCEPTANCE_PROPOSAL_V0"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"

SOURCE_REVIEW_POLICY_ID = "407df570"
SOURCE_REVIEW_POLICY_RECEIPT_ID = "58813bc2"
SOURCE_REVIEW_ID = "2946b241"
SOURCE_REVIEW_RECEIPT_ID = "79333614"

SOURCE_PROBE_ID = "87b4a010"
SOURCE_PROBE_RECEIPT_ID = "812ae591"
SOURCE_SURFACE_ID = "4427ba4b"
SOURCE_SURFACE_RECEIPT_ID = "e5022cd2"

PRIOR_PROBE_ID = "6a33c978"
PRIOR_PROBE_RECEIPT_ID = "99c90fe3"
SCALE_OUT_ID = "2b44b1fd"
SCALE_OUT_RECEIPT_ID = "f67b629b"

SOURCE_REVIEW_POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_review_policies"
SOURCE_REVIEW_POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_review_policy_receipts"
SOURCE_REVIEW_RESULT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_review_results"
SOURCE_REVIEW_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_review_receipts"

POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_acceptance_proposal_policies"
POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_acceptance_proposal_policy_receipts"

NEXT_GOAL = "EMIT_RAW_DELTA_SIGNATURE_CANDIDATE_ACCEPTANCE_PROPOSAL_V0"

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


def validate_source_review(policy: dict[str, Any], policy_receipt: dict[str, Any], result: dict[str, Any], receipt: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if policy.get("policy_id") != SOURCE_REVIEW_POLICY_ID:
        failures.append(f"review_policy_id_wrong:{policy.get('policy_id')}")
    if policy.get("policy_receipt_id") != SOURCE_REVIEW_POLICY_RECEIPT_ID:
        failures.append(f"review_policy_receipt_id_wrong:{policy.get('policy_receipt_id')}")
    if policy_receipt.get("policy_id") != SOURCE_REVIEW_POLICY_ID:
        failures.append(f"review_policy_receipt_policy_id_wrong:{policy_receipt.get('policy_id')}")
    if policy_receipt.get("receipt_id") != SOURCE_REVIEW_POLICY_RECEIPT_ID:
        failures.append(f"review_policy_receipt_id_wrong:{policy_receipt.get('receipt_id')}")

    if result.get("review_id") != SOURCE_REVIEW_ID:
        failures.append(f"review_result_id_wrong:{result.get('review_id')}")
    if receipt.get("review_id") != SOURCE_REVIEW_ID:
        failures.append(f"review_receipt_review_id_wrong:{receipt.get('review_id')}")
    if result.get("receipt_id") != SOURCE_REVIEW_RECEIPT_ID:
        failures.append(f"review_result_receipt_id_wrong:{result.get('receipt_id')}")
    if receipt.get("receipt_id") != SOURCE_REVIEW_RECEIPT_ID:
        failures.append(f"review_receipt_id_wrong:{receipt.get('receipt_id')}")

    for name, obj in [
        ("review_policy", policy),
        ("review_policy_receipt", policy_receipt),
        ("review_result", result),
        ("review_receipt", receipt),
    ]:
        if obj.get("gate") != "PASS":
            failures.append(f"{name}_gate_not_PASS:{obj.get('gate')}")
        if obj.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
            failures.append(f"{name}_candidate_design_id_wrong:{obj.get('candidate_design_id')}")

    if policy.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"review_policy_status_wrong:{policy.get('policy_status')}")
    if policy_receipt.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"review_policy_receipt_status_wrong:{policy_receipt.get('policy_status')}")

    if result.get("review_decision") != "EMIT_ACCEPTANCE_PROPOSAL_POLICY_NEXT":
        failures.append(f"review_result_decision_wrong:{result.get('review_decision')}")
    if receipt.get("review_decision") != "EMIT_ACCEPTANCE_PROPOSAL_POLICY_NEXT":
        failures.append(f"review_receipt_decision_wrong:{receipt.get('review_decision')}")
    if result.get("terminal_class") != "ADVANCE_TO_ACCEPTANCE_PROPOSAL_POLICY":
        failures.append(f"review_result_terminal_class_wrong:{result.get('terminal_class')}")
    if receipt.get("terminal_class") != "ADVANCE_TO_ACCEPTANCE_PROPOSAL_POLICY":
        failures.append(f"review_receipt_terminal_class_wrong:{receipt.get('terminal_class')}")

    terminal = receipt.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"review_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_ACCEPTANCE_PROPOSAL_POLICY_V0":
        failures.append(f"review_terminal_next_wrong:{terminal.get('next_command_goal')}")

    if receipt.get("source_probe_id") != SOURCE_PROBE_ID:
        failures.append(f"review_source_probe_id_wrong:{receipt.get('source_probe_id')}")
    if receipt.get("source_probe_receipt_id") != SOURCE_PROBE_RECEIPT_ID:
        failures.append(f"review_source_probe_receipt_id_wrong:{receipt.get('source_probe_receipt_id')}")
    if receipt.get("source_surface_id") != SOURCE_SURFACE_ID:
        failures.append(f"review_source_surface_id_wrong:{receipt.get('source_surface_id')}")
    if receipt.get("source_surface_receipt_id") != SOURCE_SURFACE_RECEIPT_ID:
        failures.append(f"review_source_surface_receipt_id_wrong:{receipt.get('source_surface_receipt_id')}")

    ids = receipt.get("evidence_stack_ids") or {}
    if ids.get("approved_new_bounded_surface_probe") != SOURCE_PROBE_ID:
        failures.append(f"evidence_current_probe_id_wrong:{ids.get('approved_new_bounded_surface_probe')}")
    if ids.get("prior_raw_delta_candidate_bounded_probe") != PRIOR_PROBE_ID:
        failures.append(f"evidence_prior_probe_id_wrong:{ids.get('prior_raw_delta_candidate_bounded_probe')}")
    if ids.get("bounded_scale_out_replay") != SCALE_OUT_ID:
        failures.append(f"evidence_scale_out_id_wrong:{ids.get('bounded_scale_out_replay')}")

    conditions = receipt.get("evidence_decision_conditions") or {}
    required_conditions = [
        "approved_new_bounded_surface_probe_PASS",
        "authority_guards_clean",
        "bounded_scale_out_replay_PASS_or_explicitly_resolved_unavailable",
        "burden_reduction_confirmed_any_available_surface",
        "candidate_acceptance_not_authorized_here",
        "candidate_acceptance_proposal_only",
        "no_false_merges_any_available_surface",
        "prior_raw_delta_candidate_bounded_probe_PASS_or_explicitly_resolved_unavailable",
    ]
    for key in required_conditions:
        if conditions.get(key) is not True:
            failures.append(f"review_condition_not_true:{key}:{conditions.get(key)}")

    current = receipt.get("current_probe") or {}
    if current.get("clean") is not True:
        failures.append(f"current_probe_not_clean:{current.get('clean')}")
    if current.get("gate") != "PASS":
        failures.append(f"current_probe_gate_wrong:{current.get('gate')}")
    if current.get("rows_total") != 500:
        failures.append(f"current_probe_rows_wrong:{current.get('rows_total')}")
    for key in ["false_merge_count", "collision_count", "false_split_count"]:
        if current.get(key) != 0:
            failures.append(f"current_probe_{key}_not_zero:{current.get(key)}")
    if current.get("retention") != 1.0:
        failures.append(f"current_probe_retention_wrong:{current.get('retention')}")
    if not (0 < float(current.get("burden_ratio_payload_to_source_rows", 999)) < 1):
        failures.append(f"current_probe_payload_burden_not_reduced:{current.get('burden_ratio_payload_to_source_rows')}")
    if not (0 < float(current.get("burden_ratio_candidate_payload_to_source_rows", 999)) < 1):
        failures.append(f"current_probe_candidate_payload_burden_not_reduced:{current.get('burden_ratio_candidate_payload_to_source_rows')}")

    prior = receipt.get("prior_probe") or {}
    scale = receipt.get("bounded_scale_out_replay") or {}
    if prior.get("clean") is not True:
        failures.append(f"prior_probe_not_clean:{prior}")
    if scale.get("clean") is not True:
        failures.append(f"scale_out_not_clean:{scale}")
    if prior.get("evidence_id") != PRIOR_PROBE_ID:
        failures.append(f"prior_probe_evidence_id_wrong:{prior.get('evidence_id')}")
    if prior.get("receipt_id") != PRIOR_PROBE_RECEIPT_ID:
        failures.append(f"prior_probe_receipt_id_wrong:{prior.get('receipt_id')}")
    if scale.get("evidence_id") != SCALE_OUT_ID:
        failures.append(f"scale_out_evidence_id_wrong:{scale.get('evidence_id')}")
    if scale.get("receipt_id") != SCALE_OUT_RECEIPT_ID:
        failures.append(f"scale_out_receipt_id_wrong:{scale.get('receipt_id')}")

    if receipt.get("zero_preserving_summary_resolution_patch_id") != "PATCH_APPROVED_NEW_SURFACE_REVIEW_RUNNER_ZERO_PRESERVING_SUMMARY_RESOLUTION_V0":
        failures.append(f"zero_preserving_patch_missing_or_wrong:{receipt.get('zero_preserving_summary_resolution_patch_id')}")

    guards = receipt.get("authority_guards") or {}
    for key in FORBIDDEN_AUTHORITY_TRUE:
        if guards.get(key) is not False:
            failures.append(f"review_authority_guard_not_false:{key}:{guards.get(key)}")

    return failures


def build_policy(review_id: str, write_outputs: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    if review_id != SOURCE_REVIEW_ID:
        raise SystemExit(f"unsupported source review id: {review_id}")

    if write_outputs:
        POLICY_DIR.mkdir(parents=True, exist_ok=True)
        POLICY_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    review_policy = load_json(SOURCE_REVIEW_POLICY_DIR / f"{SOURCE_REVIEW_POLICY_ID}.json")
    review_policy_receipt = load_json(SOURCE_REVIEW_POLICY_RECEIPT_DIR / f"{SOURCE_REVIEW_POLICY_ID}.json")
    review_result = load_json(SOURCE_REVIEW_RESULT_DIR / f"{SOURCE_REVIEW_ID}.json")
    review_receipt = load_json(SOURCE_REVIEW_RECEIPT_DIR / f"{SOURCE_REVIEW_ID}.json")

    failures = validate_source_review(review_policy, review_policy_receipt, review_result, review_receipt)

    current = review_receipt.get("current_probe") or {}
    conditions = review_receipt.get("evidence_decision_conditions") or {}

    proposal_seed = {
        "policy_name": POLICY_NAME,
        "proposal_name": PROPOSAL_NAME,
        "source_review_id": SOURCE_REVIEW_ID,
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "conditions": conditions,
        "current_probe": current,
    }
    policy_id = sha8(proposal_seed)

    proposal_recommendation = {
        "recommended_option": "OPTION_A_PROVISIONAL_BOUNDED_ACCEPTANCE_PROPOSAL",
        "option_meaning": "Propose accepting RAW_DELTA_SIGNATURE_CANDIDATE_V0 as provisionally bounded accepted under the observed evidence stack.",
        "human_boundary_required": True,
        "does_not_accept_candidate": True,
        "does_not_write_registry": True,
        "does_not_change_runtime": True,
        "acceptance_scope": {
            "candidate_design_id": CANDIDATE_DESIGN_ID,
            "bounded_surfaces": {
                "approved_new_surface_probe": SOURCE_PROBE_ID,
                "prior_bounded_probe": PRIOR_PROBE_ID,
                "bounded_scale_out_replay": SCALE_OUT_ID,
            },
            "evidence_limits": [
                "bounded surface evidence only",
                "no global correctness claim",
                "no runtime semantic claim",
                "no mathematical finality claim",
                "acceptance would remain reversible by later failure evidence",
            ],
        },
    }

    policy = {
        "schema_version": "raw_delta_signature_candidate_acceptance_proposal_policy_v0",
        "policy_name": POLICY_NAME,
        "policy_id": policy_id,
        "policy_status": POLICY_STATUS,
        "proposal_name": PROPOSAL_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_review": {
            "review_policy_id": SOURCE_REVIEW_POLICY_ID,
            "review_policy_receipt_id": SOURCE_REVIEW_POLICY_RECEIPT_ID,
            "review_id": SOURCE_REVIEW_ID,
            "review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
            "review_result_path": rel(SOURCE_REVIEW_RESULT_DIR / f"{SOURCE_REVIEW_ID}.json"),
            "review_receipt_path": rel(SOURCE_REVIEW_RECEIPT_DIR / f"{SOURCE_REVIEW_ID}.json"),
        },
        "evidence_stack": {
            "current_approved_new_bounded_surface_probe": {
                "probe_id": SOURCE_PROBE_ID,
                "probe_receipt_id": SOURCE_PROBE_RECEIPT_ID,
                "surface_id": SOURCE_SURFACE_ID,
                "surface_receipt_id": SOURCE_SURFACE_RECEIPT_ID,
                "rows_total": current.get("rows_total"),
                "false_merge_count": current.get("false_merge_count"),
                "collision_count": current.get("collision_count"),
                "false_split_count": current.get("false_split_count"),
                "retention": current.get("retention"),
                "burden_ratio_payload_to_source_rows": current.get("burden_ratio_payload_to_source_rows"),
                "burden_ratio_candidate_payload_to_source_rows": current.get("burden_ratio_candidate_payload_to_source_rows"),
                "clean": current.get("clean"),
            },
            "prior_raw_delta_candidate_bounded_probe": {
                "probe_id": PRIOR_PROBE_ID,
                "probe_receipt_id": PRIOR_PROBE_RECEIPT_ID,
                "clean": (review_receipt.get("prior_probe") or {}).get("clean"),
            },
            "bounded_scale_out_replay": {
                "scale_out_id": SCALE_OUT_ID,
                "scale_out_receipt_id": SCALE_OUT_RECEIPT_ID,
                "clean": (review_receipt.get("bounded_scale_out_replay") or {}).get("clean"),
            },
        },
        "proposal_contract": {
            "purpose": "emit a human-reviewable candidate acceptance proposal without accepting the candidate",
            "human_boundary": "REQUIRED_BEFORE_ANY_ACCEPTANCE_OR_REGISTRY_WRITE",
            "proposal_recommendation": proposal_recommendation,
            "allowed_output": {
                "proposal_artifact": True,
                "proposal_receipt": True,
                "human_decision_request": True,
            },
            "proposal_options_for_human": {
                "OPTION_A_PROVISIONAL_BOUNDED_ACCEPT": {
                    "meaning": "Accept RAW_DELTA_SIGNATURE_CANDIDATE_V0 as provisionally bounded accepted under this evidence stack.",
                    "would_authorize_later_step": "separate candidate acceptance record and registry insertion policy",
                    "not_performed_by_proposal": True,
                },
                "OPTION_B_MORE_SCALE_BEFORE_ACCEPTANCE": {
                    "meaning": "Do not accept yet; request additional bounded scale/inventory before acceptance.",
                    "not_performed_by_proposal": True,
                },
                "OPTION_C_REJECT_OR_DIAGNOSE": {
                    "meaning": "Do not accept; open diagnostic or revise candidate.",
                    "not_performed_by_proposal": True,
                },
            },
            "required_evidence_conditions": conditions,
            "required_safety_clauses": {
                "proposal_only": True,
                "candidate_not_accepted": True,
                "registry_not_written": True,
                "runtime_not_changed": True,
                "bounded_scope_explicit": True,
                "human_decision_required": True,
            },
        },
        "authorized_operations_next": {
            "read_source_review_result": True,
            "read_source_review_receipt": True,
            "write_acceptance_proposal": True,
            "write_acceptance_proposal_receipt": True,
            "emit_human_decision_boundary": True,
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
        "pre_proposal_classification": {
            "source_review_pass_clean": not failures,
            "review_decision_is_acceptance_proposal_next": review_receipt.get("review_decision") == "EMIT_ACCEPTANCE_PROPOSAL_POLICY_NEXT",
            "all_evidence_decision_conditions_true": all(v is True for v in conditions.values()) if conditions else False,
            "candidate_acceptance_not_authorized_here": True,
            "proposal_only": True,
            "human_boundary_required": True,
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "stop_code": None if not failures else "STOP_ACCEPTANCE_PROPOSAL_POLICY_INVALID_SOURCE_REVIEW",
            "next_command_goal": NEXT_GOAL if not failures else None,
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
            "human_decision_boundary_emitted": False,
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt = {
        "schema_version": "raw_delta_signature_candidate_acceptance_proposal_policy_receipt_v0",
        "receipt_type": "RAW_DELTA_SIGNATURE_CANDIDATE_ACCEPTANCE_PROPOSAL_POLICY_RECEIPT",
        "policy_id": policy_id,
        "policy_name": POLICY_NAME,
        "policy_status": POLICY_STATUS,
        "proposal_name": PROPOSAL_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_review_policy_id": SOURCE_REVIEW_POLICY_ID,
        "source_review_policy_receipt_id": SOURCE_REVIEW_POLICY_RECEIPT_ID,
        "source_review_id": SOURCE_REVIEW_ID,
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "source_probe_id": SOURCE_PROBE_ID,
        "source_probe_receipt_id": SOURCE_PROBE_RECEIPT_ID,
        "source_surface_id": SOURCE_SURFACE_ID,
        "source_surface_receipt_id": SOURCE_SURFACE_RECEIPT_ID,
        "prior_probe_id": PRIOR_PROBE_ID,
        "prior_probe_receipt_id": PRIOR_PROBE_RECEIPT_ID,
        "scale_out_id": SCALE_OUT_ID,
        "scale_out_receipt_id": SCALE_OUT_RECEIPT_ID,
        "proposal_recommendation": proposal_recommendation,
        "pre_proposal_classification": policy["pre_proposal_classification"],
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
        (POLICY_DIR / f"{policy_id}.json").write_text(json.dumps(policy, indent=2, sort_keys=True))
        (POLICY_RECEIPT_DIR / f"{policy_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return policy, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-id", default=SOURCE_REVIEW_ID)
    args = parser.parse_args()

    policy, receipt = build_policy(args.review_id, write_outputs=True)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_id={policy['policy_id']}")
    print(f"policy_receipt_id={receipt['receipt_id']}")
    print(f"policy_path=data/raw_delta_signature_candidate_acceptance_proposal_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/raw_delta_signature_candidate_acceptance_proposal_policy_receipts/{policy['policy_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
