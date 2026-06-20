#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

POLICY_DIR = ROOT / "data" / "frontier_depth_probe_fix_candidate_policies"
CANDIDATE_DIR = ROOT / "data" / "frontier_depth_probe_fix_candidates"
RECEIPT_DIR = ROOT / "data" / "frontier_depth_probe_fix_candidate_receipts"

EXPECTED_POLICY_ID = "42028fa3"
EXPECTED_SOURCE_DECISION_ID = "118d66ca"
EXPECTED_SOURCE_AFTER_PROFILE_ID = "45cd7660"
EXPECTED_TARGET_BURDEN_CLASS = "BURDEN_DEPTH_SCAN"
EXPECTED_FIX_CANDIDATE_ID = "FIX_CANDIDATE_FRONTIER_DEPTH_PROBE_PLAN_V0"
EXPECTED_FIX_CANDIDATE_KIND = "FRONTIER_DEPTH_PROBE_PROPOSAL"

EXPECTED_ACCEPTED_FROZEN = [
    "BURDEN_CYCLE_SCAN",
    "BURDEN_DB_WRITE",
    "BURDEN_REPEATED_SLOT_WORK",
]

EXPECTED_DEPTH_SLOTS = [
    "MICRO_03_DEPTH_PRESSURE_A",
    "MICRO_03_DEPTH_PRESSURE_B",
    "MICRO_03_DEPTH_PRESSURE_C",
    "MICRO_03_DEPTH_PRESSURE_D",
    "MICRO_03_DEPTH_PRESSURE_E",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_sig(obj: dict[str, Any]) -> str:
    body = dict(obj)
    for key in ("candidate_id", "candidate_sig8", "receipt_id", "receipt_sig8"):
        body.pop(key, None)
    blob = json.dumps(body, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:8]


def load_policy(policy_id: str) -> tuple[Path, dict[str, Any]]:
    path = POLICY_DIR / f"{policy_id}.json"
    if not path.exists():
        raise SystemExit(f"missing frontier-depth policy: {path}")
    return path, json.loads(path.read_text())


def verify_policy(policy: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    source_decision = policy.get("source_decision") or {}
    source_after = policy.get("source_after_profile") or {}
    target = policy.get("target_evidence") or {}
    auth = policy.get("authorization") or {}
    authorized = policy.get("authorized_fix_candidate") or {}
    required_retest = policy.get("required_retest") or {}
    terminal = policy.get("terminal") or {}

    if policy.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"policy_id_mismatch:{policy.get('policy_id')}")
    if policy.get("policy_id") != policy.get("policy_sig8"):
        failures.append("policy_sig_mismatch")
    if policy.get("gate") != "PASS":
        failures.append("policy_gate_not_PASS")

    if source_decision.get("decision_id") != EXPECTED_SOURCE_DECISION_ID:
        failures.append(f"source_decision_mismatch:{source_decision.get('decision_id')}")
    if source_decision.get("gate") != "PASS":
        failures.append("source_decision_gate_not_PASS")

    if source_after.get("profile_id") != EXPECTED_SOURCE_AFTER_PROFILE_ID:
        failures.append(f"source_after_profile_mismatch:{source_after.get('profile_id')}")
    if source_after.get("gate") != "MICRO_BURDEN_PROFILE_PASS":
        failures.append("source_after_profile_gate_not_MICRO_BURDEN_PROFILE_PASS")
    if source_after.get("profile_receipts_total") != source_after.get("db_receipt_delta"):
        failures.append("source_after_profile_receipt_total_mismatch")
    if source_after.get("profile_receipts_total") != 1457:
        failures.append(f"source_after_profile_receipts_not_1457:{source_after.get('profile_receipts_total')}")

    if policy.get("accepted_burden_classes_frozen") != EXPECTED_ACCEPTED_FROZEN:
        failures.append(f"accepted_frozen_mismatch:{policy.get('accepted_burden_classes_frozen')}")
    if policy.get("target_burden_class") != EXPECTED_TARGET_BURDEN_CLASS:
        failures.append(f"target_burden_class_mismatch:{policy.get('target_burden_class')}")
    if policy.get("target_burden_class_proven") is not True:
        failures.append("target_burden_class_not_proven")

    if target.get("burden_class") != EXPECTED_TARGET_BURDEN_CLASS:
        failures.append(f"target_evidence_class_mismatch:{target.get('burden_class')}")
    if target.get("rows") != 5:
        failures.append(f"target_rows_not_5:{target.get('rows')}")
    if target.get("receipts") != 345:
        failures.append(f"target_receipts_not_345:{target.get('receipts')}")
    if int(target.get("elapsed_ms") or 0) <= 0:
        failures.append("target_elapsed_ms_not_positive")
    if target.get("families") != ["A", "B", "C", "D", "E"]:
        failures.append(f"target_families_mismatch:{target.get('families')}")
    if target.get("probes") != ["MICRO_03_DEPTH_PRESSURE"]:
        failures.append(f"target_probe_mismatch:{target.get('probes')}")
    if target.get("slots") != EXPECTED_DEPTH_SLOTS:
        failures.append(f"target_slots_mismatch:{target.get('slots')}")
    if target.get("slot_identity_matches_expected") is not True:
        failures.append("target_slot_identity_not_expected")

    if auth.get("authorizes_fix_candidate_count") != 1:
        failures.append(f"authorizes_fix_candidate_count_not_one:{auth.get('authorizes_fix_candidate_count')}")
    if auth.get("authorizes_fix_candidate_ids") != [EXPECTED_FIX_CANDIDATE_ID]:
        failures.append(f"authorizes_fix_candidate_ids_mismatch:{auth.get('authorizes_fix_candidate_ids')}")
    if auth.get("authorizes_fix_candidate_kind") != EXPECTED_FIX_CANDIDATE_KIND:
        failures.append(f"authorizes_fix_candidate_ids_mismatch:{auth.get('authorizes_fix_candidate_ids')}")
    if auth.get("authorizes_fix_candidate_kind") != EXPECTED_FIX_CANDIDATE_KIND:
        failures.append(f"authorizes_fix_candidate_kind_mismatch:{auth.get('authorizes_fix_candidate_kind')}")

    forbidden_false = [
        "authorizes_patch_application",
        "authorizes_code_change",
        "authorizes_runner_semantics_change",
        "authorizes_gate_semantics_change",
        "authorizes_law_semantics_change",
        "authorizes_halt_semantics_change",
        "authorizes_receipt_schema_change",
        "authorizes_receipt_deletion",
        "authorizes_receipt_compression",
        "authorizes_execution_skipping",
        "authorizes_depth_probe_skipping",
        "authorizes_frontier_case_skipping",
        "authorizes_synthetic_depth_receipts",
        "authorizes_reusing_prior_depth_results_as_execution",
        "authorizes_depth_range_change",
        "authorizes_depth_max_change",
        "authorizes_radius_expansion",
        "authorizes_reopening_accepted_burden_classes",
    ]
    for key in forbidden_false:
        if auth.get(key) is not False:
            failures.append(f"illegal_policy_authorization:{key}:{auth.get(key)}")

    if authorized.get("fix_candidate_id") != EXPECTED_FIX_CANDIDATE_ID:
        failures.append(f"authorized_candidate_id_mismatch:{authorized.get('fix_candidate_id')}")
    if authorized.get("fix_candidate_kind") != EXPECTED_FIX_CANDIDATE_KIND:
        failures.append(f"authorized_candidate_kind_mismatch:{authorized.get('fix_candidate_kind')}")
    if authorized.get("target_burden_class") != EXPECTED_TARGET_BURDEN_CLASS:
        failures.append(f"authorized_target_mismatch:{authorized.get('target_burden_class')}")
    if authorized.get("next_command_goal") != "BUILD_FRONTIER_DEPTH_PROBE_FIX_CANDIDATE_V0":
        failures.append(f"authorized_next_goal_mismatch:{authorized.get('next_command_goal')}")

    expected_metric = authorized.get("expected_metric_direction") or {}
    if expected_metric.get("must_preserve_rows") != 5:
        failures.append("expected_metric_rows_not_5")
    if expected_metric.get("must_preserve_slots") != EXPECTED_DEPTH_SLOTS:
        failures.append("expected_metric_slots_mismatch")
    if expected_metric.get("must_preserve_target_receipts") != 345:
        failures.append("expected_metric_receipts_not_345")
    if expected_metric.get("must_not_change_depth_range") is not True:
        failures.append("expected_metric_depth_range_guard_missing")
    if expected_metric.get("must_not_change_halt_law_gate_run_semantics") is not True:
        failures.append("expected_metric_semantics_guard_missing")

    if required_retest.get("before_profile_id") != EXPECTED_SOURCE_AFTER_PROFILE_ID:
        failures.append(f"required_retest_before_profile_mismatch:{required_retest.get('before_profile_id')}")
    if required_retest.get("same_micro_suite_required") is not True:
        failures.append("required_retest_same_micro_suite_missing")
    if required_retest.get("same_probe_specs_required") is not True:
        failures.append("required_retest_same_probe_specs_missing")
    if required_retest.get("same_script") != "scripts/wide_burden_profile_microruns.py --execute":
        failures.append(f"required_retest_script_mismatch:{required_retest.get('same_script')}")
    if required_retest.get("comparison_artifact_schema") != "frontier_depth_probe_before_after_comparison_v0":
        failures.append(f"required_retest_schema_mismatch:{required_retest.get('comparison_artifact_schema')}")

    if terminal.get("next_command_goal") != "BUILD_FRONTIER_DEPTH_PROBE_FIX_CANDIDATE_V0":
        failures.append(f"policy_terminal_next_goal_mismatch:{terminal.get('next_command_goal')}")

    return failures


def build_candidate(policy_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    CANDIDATE_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    policy_path, policy = load_policy(policy_id)
    failures = verify_policy(policy)
    warnings: list[str] = []

    target = policy.get("target_evidence") or {}

    candidate = {
        "schema_version": "frontier_depth_probe_fix_candidate_v0",
        "candidate_kind": "FRONTIER_DEPTH_PROBE_FIX_CANDIDATE",
        "candidate_name": EXPECTED_FIX_CANDIDATE_ID,
        "candidate_status": "PROPOSAL_ONLY_NOT_APPLIED",
        "source_policy": {
            "policy_id": policy.get("policy_id"),
            "policy_path": str(policy_path.relative_to(ROOT)),
            "policy_sig8": policy.get("policy_sig8"),
            "gate": policy.get("gate"),
        },
        "source_decision_id": EXPECTED_SOURCE_DECISION_ID,
        "source_after_profile_id": EXPECTED_SOURCE_AFTER_PROFILE_ID,
        "accepted_burden_classes_frozen": EXPECTED_ACCEPTED_FROZEN,
        "target_burden_class": EXPECTED_TARGET_BURDEN_CLASS,
        "target_burden_class_proven": policy.get("target_burden_class_proven") is True,
        "target_burden_evidence": target,
        "authorization": {
            "authorizes_patch_application": False,
            "authorizes_code_change_now": False,
            "authorizes_runner_semantics_change": False,
            "authorizes_gate_semantics_change": False,
            "authorizes_law_semantics_change": False,
            "authorizes_halt_semantics_change": False,
            "authorizes_receipt_schema_change": False,
            "authorizes_receipt_deletion": False,
            "authorizes_receipt_compression": False,
            "authorizes_execution_skipping": False,
            "authorizes_depth_probe_skipping": False,
            "authorizes_frontier_case_skipping": False,
            "authorizes_synthetic_depth_receipts": False,
            "authorizes_reusing_prior_depth_results_as_execution": False,
            "authorizes_reusing_prior_run_results_as_execution": False,
            "authorizes_depth_range_change": False,
            "authorizes_depth_min_change": False,
            "authorizes_depth_max_change": False,
            "authorizes_radius_expansion": False,
            "authorizes_reopening_accepted_burden_classes": False,
        },
        "patch_plan": {
            "plan_kind": "FRONTIER_DEPTH_PROBE_PATCH_PLAN",
            "plan_status": "PROPOSAL_ONLY_NOT_APPLIED",
            "files_allowed_to_touch_if_later_applied": [
                "scripts/wide_burden_profile_microruns.py",
                "narrow helper module for frontier/depth metadata certificates if one exists",
            ],
            "intended_changes": [
                {
                    "change_id": "BUILD_FRONTIER_DEPTH_METADATA_CERTIFICATE_OBJECT",
                    "description": "Construct a metadata certificate from completed MICRO_03_DEPTH_PRESSURE observations after normal execution.",
                    "expected_effect": "Make frontier/depth pressure evidence explicit without changing execution, depth range, halt, law, gate, or run semantics.",
                    "semantic_constraint": "Certificate is observational only; it cannot authorize skipping, frontier pruning, depth range change, or execution substitution.",
                },
                {
                    "change_id": "CACHE_DEPTH_PROBE_PLAN_METADATA_NOT_RESULTS",
                    "description": "Cache deterministic depth-pressure plan metadata keyed by probe id, slot id, family, depth range, cycles_per_case, and max_cells.",
                    "expected_effect": "Reduce repeated construction of depth-pressure probe metadata.",
                    "semantic_constraint": "Cache must not contain run ids, receipt rows, halt/law/gate results, stdout/stderr, depth results, or any prior execution output.",
                },
                {
                    "change_id": "PRESERVE_DEPTH_PRESSURE_ROW_IDENTITY_GUARD",
                    "description": "Add explicit checks that depth-pressure rows remain exactly MICRO_03_DEPTH_PRESSURE_A..E.",
                    "expected_effect": "Prevent depth-pressure row collapse or probe drift.",
                    "semantic_constraint": "All five A-E depth-pressure rows must remain distinguishable and present.",
                },
                {
                    "change_id": "PRESERVE_DEPTH_RANGE_AND_RUN_SEMANTICS",
                    "description": "Keep current micro-suite depth range and probe specs unchanged during retest.",
                    "expected_effect": "Allow valid before/after comparison against before_profile_id 45cd7660.",
                    "semantic_constraint": "No depth_max/depth_min change, no radius expansion, no execution skipping, no synthetic depth receipts.",
                },
            ],
            "metadata_certificate_policy": {
                "certificate_scope": "post_execution_depth_observation_metadata_only",
                "certificate_kind": "frontier_depth_observation_certificate",
                "certificate_key_fields": [
                    "probe_id",
                    "slot_id",
                    "family_compact",
                    "depth_min",
                    "depth_max",
                    "cycles_per_case",
                    "max_cells",
                ],
                "certificate_value_fields_allowed": [
                    "observed_depth_pressure_receipts",
                    "observed_depth_pressure_elapsed_ms",
                    "observed_family_compact",
                    "observed_probe_id",
                    "observed_slot_id",
                    "metadata_only_no_execution_substitution",
                    "depth_range_preserved",
                ],
                "must_not_certify_without_execution": True,
                "must_not_change_depth_range": True,
                "must_not_change_depth_max": True,
                "must_not_change_depth_min": True,
                "must_not_change_halt_reason": True,
            },
            "cache_policy": {
                "cache_scope": "within_one_micro_profile_execution_only",
                "cache_key_fields": [
                    "probe_id",
                    "slot_id",
                    "family_compact",
                    "depth_min",
                    "depth_max",
                    "cycles_per_case",
                    "max_cells",
                ],
                "cache_value_fields": [
                    "family_name",
                    "stress_cli_args",
                    "expected_depth_slot_identity",
                    "metadata_only_no_results",
                ],
                "must_not_cache": [
                    "run_id",
                    "receipt rows",
                    "receipt counts as substitutes for execution",
                    "law results",
                    "gate results",
                    "halt results",
                    "stdout/stderr from a prior run",
                    "any prior execution result",
                    "depth probe results as substitute execution",
                    "frontier case results as substitute execution",
                ],
            },
            "depth_slot_identity_guard": {
                "expected_depth_slot_ids": EXPECTED_DEPTH_SLOTS,
                "families_must_remain_A_E": ["A", "B", "C", "D", "E"],
                "probe_must_remain": "MICRO_03_DEPTH_PRESSURE",
                "fail_closed_if_slot_identity_changes": True,
                "fail_closed_if_any_depth_slot_missing": True,
                "fail_closed_if_any_depth_slot_merged": True,
                "fail_closed_if_depth_range_changes": True,
                "fail_closed_if_radius_expands": True,
            },
            "accepted_burden_class_guard": {
                "accepted_burden_classes_frozen": EXPECTED_ACCEPTED_FROZEN,
                "must_not_reopen_without_explicit_new_failure": True,
            },
        },
        "expected_metric_direction": {
            "primary_metric": "elapsed_ms",
            "secondary_metric": "receipts_per_sec",
            "target_rows": "rows with burden_class == BURDEN_DEPTH_SCAN",
            "before_profile_id": EXPECTED_SOURCE_AFTER_PROFILE_ID,
            "before_target_elapsed_ms": target.get("elapsed_ms"),
            "before_target_receipts": target.get("receipts"),
            "before_target_rows": target.get("rows"),
            "expected_elapsed_ms": "decrease_or_non_worse",
            "expected_receipts_per_sec": "increase_or_non_worse",
            "must_preserve_target_rows": 5,
            "must_preserve_target_receipts": 345,
            "must_preserve_depth_slot_identity_exactly": EXPECTED_DEPTH_SLOTS,
            "must_preserve_profile_receipts_total_match_registry": True,
            "must_preserve_family_coverage_A_E": True,
            "must_preserve_depth_pressure_probe_identity": True,
            "must_not_change_depth_range": True,
            "must_not_change_depth_min": True,
            "must_not_change_depth_max": True,
            "must_not_expand_radius": True,
            "must_not_change_halt_law_gate_run_semantics": True,
        },
        "required_retest": {
            "before_profile_id": EXPECTED_SOURCE_AFTER_PROFILE_ID,
            "after_profile_required": True,
            "same_micro_suite_required": True,
            "same_probe_specs_required": True,
            "same_script": "scripts/wide_burden_profile_microruns.py --execute",
            "comparison_required": True,
            "comparison_artifact_schema": "frontier_depth_probe_before_after_comparison_v0",
            "pass_condition": [
                "after profile gate MICRO_BURDEN_PROFILE_PASS",
                "receipt totals match registry.sqlite",
                "all five probes complete",
                "family coverage A-E preserved",
                "depth-scan row keys preserved",
                "depth-scan receipts preserved",
                "depth-scan slots preserved",
                "depth-pressure probe identity preserved",
                "no depth range change",
                "no radius expansion",
                "no gate semantics change",
                "no law semantics change",
                "no halt semantics change",
                "no run semantics change",
                "no execution skipping",
                "no depth probe skipping",
                "no frontier case skipping",
                "no synthetic depth receipts",
                "BURDEN_DEPTH_SCAN target rows show non-worse elapsed_ms or explicit failure classification",
            ],
        },
        "apply_gate": {
            "candidate_does_not_apply_itself": True,
            "must_be_followed_by_explicit_apply_command": True,
            "apply_command_goal_if_accepted": "APPLY_FRONTIER_DEPTH_PROBE_FIX_V0",
            "stop_if_patch_touches_forbidden_semantics": True,
            "stop_if_patch_skips_depth_execution": True,
            "stop_if_patch_skips_frontier_cases": True,
            "stop_if_patch_changes_depth_range": True,
            "stop_if_patch_expands_radius": True,
            "stop_if_patch_synthesizes_depth_receipts": True,
            "stop_if_patch_reuses_prior_depth_results": True,
            "stop_if_patch_changes_halt_law_gate_or_run_semantics": True,
        },
        "forbidden": {
            "skip_depth_pressure_execution": True,
            "skip_frontier_cases": True,
            "change_depth_min": True,
            "change_depth_max": True,
            "change_depth_range": True,
            "expand_radius": True,
            "reuse_prior_depth_results_as_current_execution": True,
            "emit_synthetic_depth_receipts_for_unexecuted_probes": True,
            "delete_receipts": True,
            "compress_raw_receipts": True,
            "receipt_schema_change": True,
            "halt_semantics_change": True,
            "law_semantics_change": True,
            "gate_semantics_change": True,
            "run_semantics_change": True,
            "reopen_accepted_burden_classes_without_explicit_new_failure": True,
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": "APPLY_FRONTIER_DEPTH_PROBE_FIX_V0" if not failures else None,
            "stop_code": None if not failures else "STOP_FRONTIER_DEPTH_FIX_CANDIDATE_INVALID",
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "PASS" if not failures else "FAIL",
        "created_at": now_iso(),
    }

    sig = stable_sig(candidate)
    candidate["candidate_id"] = sig
    candidate["candidate_sig8"] = sig

    receipt = {
        "schema_version": "frontier_depth_probe_fix_candidate_receipt_v0",
        "candidate_id": sig,
        "candidate_path": f"data/frontier_depth_probe_fix_candidates/{sig}.json",
        "candidate_sig8": sig,
        "candidate_name": EXPECTED_FIX_CANDIDATE_ID,
        "candidate_status": candidate["candidate_status"],
        "source_policy_id": policy.get("policy_id"),
        "source_decision_id": EXPECTED_SOURCE_DECISION_ID,
        "source_after_profile_id": EXPECTED_SOURCE_AFTER_PROFILE_ID,
        "target_burden_class": EXPECTED_TARGET_BURDEN_CLASS,
        "target_rows": target.get("rows"),
        "target_receipts": target.get("receipts"),
        "target_elapsed_ms": target.get("elapsed_ms"),
        "authorizes_patch_application": False,
        "authorizes_execution_skipping": False,
        "authorizes_depth_probe_skipping": False,
        "authorizes_frontier_case_skipping": False,
        "authorizes_synthetic_depth_receipts": False,
        "authorizes_reusing_prior_depth_results_as_execution": False,
        "authorizes_depth_range_change": False,
        "authorizes_depth_min_change": False,
        "authorizes_depth_max_change": False,
        "authorizes_radius_expansion": False,
        "gate": candidate["gate"],
        "required_retest": candidate["required_retest"],
        "terminal": candidate["terminal"],
        "failures": failures,
        "warnings": warnings,
        "created_at": now_iso(),
    }

    receipt_sig = stable_sig(receipt)
    receipt["receipt_id"] = receipt_sig
    receipt["receipt_sig8"] = receipt_sig

    (CANDIDATE_DIR / f"{sig}.json").write_text(json.dumps(candidate, indent=2, sort_keys=True))
    (RECEIPT_DIR / f"{sig}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return candidate, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", default=EXPECTED_POLICY_ID)
    args = parser.parse_args()

    candidate, receipt = build_candidate(args.policy)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"candidate_json_path=data/frontier_depth_probe_fix_candidates/{candidate['candidate_id']}.json")
    print(f"candidate_receipt_path=data/frontier_depth_probe_fix_candidate_receipts/{candidate['candidate_id']}.json")

    return 0 if candidate["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
