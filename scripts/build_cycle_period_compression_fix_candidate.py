#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

POLICY_DIR = ROOT / "data" / "cycle_period_compression_fix_candidate_policies"
CANDIDATE_DIR = ROOT / "data" / "cycle_period_compression_fix_candidates"
RECEIPT_DIR = ROOT / "data" / "cycle_period_compression_fix_candidate_receipts"

EXPECTED_POLICY_ID = "688b83a9"
EXPECTED_AFTER_PROFILE_ID = "24ac7037"
EXPECTED_SOURCE_DECISION_ID = "d1896459"
EXPECTED_TARGET_BURDEN_CLASS = "BURDEN_CYCLE_SCAN"
EXPECTED_FIX_CANDIDATE_ID = "FIX_CANDIDATE_CYCLE_PERIOD_COMPRESSION_V0"
EXPECTED_FIX_CANDIDATE_KIND = "CYCLE_PERIOD_COMPRESSION_PROPOSAL"

EXPECTED_CYCLE_SLOTS = [
    "MICRO_02_CYCLE_PRESSURE_A",
    "MICRO_02_CYCLE_PRESSURE_B",
    "MICRO_02_CYCLE_PRESSURE_C",
    "MICRO_02_CYCLE_PRESSURE_D",
    "MICRO_02_CYCLE_PRESSURE_E",
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
        raise SystemExit(f"missing cycle-period policy: {path}")
    return path, json.loads(path.read_text())


def verify_policy(policy: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    auth = policy.get("authorization") or {}
    source_decision = policy.get("source_decision") or {}
    source_after = policy.get("source_after_profile") or {}
    target = policy.get("target_evidence") or {}
    authorized = policy.get("authorized_fix_candidate") or {}

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
    if source_after.get("profile_id") != EXPECTED_AFTER_PROFILE_ID:
        failures.append(f"source_after_profile_mismatch:{source_after.get('profile_id')}")
    if source_after.get("gate") != "MICRO_BURDEN_PROFILE_PASS":
        failures.append("source_after_profile_gate_not_MICRO_BURDEN_PROFILE_PASS")
    if source_after.get("profile_receipts_total") != source_after.get("db_receipt_delta"):
        failures.append("source_after_profile_receipt_total_mismatch")
    if source_after.get("profile_receipts_total") != 1457:
        failures.append(f"source_after_profile_receipts_not_1457:{source_after.get('profile_receipts_total')}")

    if policy.get("target_burden_class") != EXPECTED_TARGET_BURDEN_CLASS:
        failures.append(f"target_burden_class_mismatch:{policy.get('target_burden_class')}")
    if policy.get("target_burden_class_proven") is not True:
        failures.append("target_burden_class_not_proven")
    if target.get("rows") != 5:
        failures.append(f"target_rows_not_5:{target.get('rows')}")
    if target.get("receipts") != 576:
        failures.append(f"target_receipts_not_expected_576:{target.get('receipts')}")
    if int(target.get("elapsed_ms") or 0) <= 0:
        failures.append("target_elapsed_ms_not_positive")
    if target.get("families") != ["A", "B", "C", "D", "E"]:
        failures.append(f"target_families_mismatch:{target.get('families')}")
    if target.get("probes") != ["MICRO_02_CYCLE_PRESSURE"]:
        failures.append(f"target_probe_mismatch:{target.get('probes')}")
    if target.get("slot_identity_matches_expected") is not True:
        failures.append("target_slot_identity_not_expected")
    if target.get("slots") != EXPECTED_CYCLE_SLOTS:
        failures.append(f"target_slots_mismatch:{target.get('slots')}")

    if auth.get("authorizes_fix_candidate_count") != 1:
        failures.append(f"authorizes_fix_candidate_count_not_one:{auth.get('authorizes_fix_candidate_count')}")
    if auth.get("authorizes_fix_candidate_ids") != [EXPECTED_FIX_CANDIDATE_ID]:
        failures.append(f"authorized_fix_candidate_ids_mismatch:{auth.get('authorizes_fix_candidate_ids')}")
    if auth.get("authorizes_fix_candidate_kind") != EXPECTED_FIX_CANDIDATE_KIND:
        failures.append(f"authorized_fix_candidate_kind_mismatch:{auth.get('authorizes_fix_candidate_kind')}")

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
        "authorizes_cycle_execution_skipping",
        "authorizes_synthetic_cycle_receipts",
        "authorizes_reusing_prior_cycle_results_as_execution",
        "authorizes_early_halt_on_period_detection",
        "authorizes_radius_expansion",
    ]
    for key in forbidden_false:
        if auth.get(key) is not False:
            failures.append(f"illegal_policy_authorization:{key}:{auth.get(key)}")

    if authorized.get("fix_candidate_id") != EXPECTED_FIX_CANDIDATE_ID:
        failures.append(f"authorized_candidate_id_mismatch:{authorized.get('fix_candidate_id')}")
    if authorized.get("fix_candidate_kind") != EXPECTED_FIX_CANDIDATE_KIND:
        failures.append(f"authorized_candidate_kind_mismatch:{authorized.get('fix_candidate_kind')}")
    if authorized.get("next_command_goal") != "BUILD_CYCLE_PERIOD_COMPRESSION_FIX_CANDIDATE_V0":
        failures.append(f"authorized_next_goal_mismatch:{authorized.get('next_command_goal')}")

    terminal = policy.get("terminal") or {}
    if terminal.get("next_command_goal") != "BUILD_CYCLE_PERIOD_COMPRESSION_FIX_CANDIDATE_V0":
        failures.append(f"policy_next_goal_mismatch:{terminal.get('next_command_goal')}")

    return failures


def build_candidate(policy_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    CANDIDATE_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    policy_path, policy = load_policy(policy_id)
    failures = verify_policy(policy)
    warnings: list[str] = []

    target = policy.get("target_evidence") or {}

    candidate = {
        "schema_version": "cycle_period_compression_fix_candidate_v0",
        "candidate_kind": "CYCLE_PERIOD_COMPRESSION_FIX_CANDIDATE",
        "candidate_name": EXPECTED_FIX_CANDIDATE_ID,
        "candidate_status": "PROPOSAL_ONLY_NOT_APPLIED",
        "source_policy": {
            "policy_id": policy.get("policy_id"),
            "policy_path": str(policy_path.relative_to(ROOT)),
            "policy_sig8": policy.get("policy_sig8"),
            "gate": policy.get("gate"),
        },
        "source_after_profile_id": EXPECTED_AFTER_PROFILE_ID,
        "source_decision_id": EXPECTED_SOURCE_DECISION_ID,
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
            "authorizes_cycle_execution_skipping": False,
            "authorizes_early_halt_on_period_detection": False,
            "authorizes_synthetic_cycle_receipts": False,
            "authorizes_reusing_prior_cycle_results_as_execution": False,
            "authorizes_reusing_prior_run_results_as_execution": False,
            "authorizes_radius_expansion": False,
        },
        "patch_plan": {
            "plan_kind": "CYCLE_PERIOD_COMPRESSION_PATCH_PLAN",
            "plan_status": "PROPOSAL_ONLY_NOT_APPLIED",
            "files_allowed_to_touch_if_later_applied": [
                "scripts/wide_burden_profile_microruns.py",
                "narrow helper module for cycle-period metadata certificates if one exists",
            ],
            "intended_changes": [
                {
                    "change_id": "BUILD_CYCLE_PERIOD_METADATA_CERTIFICATE_OBJECT",
                    "description": "Construct a metadata certificate from completed cycle-pressure run observations, recording observed period evidence after normal execution.",
                    "expected_effect": "Make cycle-period evidence explicit without changing halt or execution behavior.",
                    "semantic_constraint": "Certificate must be derived after execution; it cannot terminate execution early or stand in for execution.",
                },
                {
                    "change_id": "CACHE_CYCLE_PROBE_PLAN_METADATA_NOT_RESULTS",
                    "description": "Cache deterministic cycle-pressure plan metadata keyed by probe id, slot id, family, depth, cycles_per_case, and max_cells.",
                    "expected_effect": "Reduce metadata reconstruction overhead around the cycle-pressure probe.",
                    "semantic_constraint": "Cache must not contain run ids, receipt rows, halt/law/gate results, stdout/stderr, or prior execution outputs.",
                },
                {
                    "change_id": "PRESERVE_CYCLE_PRESSURE_ROW_IDENTITY_GUARD",
                    "description": "Add explicit checks that cycle-pressure rows remain exactly MICRO_02_CYCLE_PRESSURE_A..E.",
                    "expected_effect": "Prevent cycle-pressure row collapse or probe drift.",
                    "semantic_constraint": "All five A-E cycle-pressure rows must remain distinguishable and present.",
                },
                {
                    "change_id": "PRESERVE_CYCLES_PER_CASE_AND_HALT_SEMANTICS",
                    "description": "Keep requested cycles_per_case unchanged and preserve halt decision semantics.",
                    "expected_effect": "Allow valid before/after comparison against before_profile_id 24ac7037.",
                    "semantic_constraint": "No early halt on period detection; no synthetic receipts; no skipped cycles.",
                },
            ],
            "metadata_certificate_policy": {
                "certificate_scope": "post_execution_observation_metadata_only",
                "certificate_key_fields": [
                    "probe_id",
                    "slot_id",
                    "family_compact",
                    "depth_max",
                    "cycles_per_case",
                    "max_cells",
                ],
                "certificate_value_fields_allowed": [
                    "observed_halt_counts",
                    "observed_total_receipts",
                    "observed_total_cases",
                    "observed_periodic_halt_presence",
                    "metadata_only_no_execution_substitution",
                ],
                "must_not_certify_without_execution": True,
                "must_not_change_halt_reason": True,
                "must_not_change_cycles_per_case": True,
            },
            "cache_policy": {
                "cache_scope": "within_one_micro_profile_execution_only",
                "cache_key_fields": [
                    "probe_id",
                    "slot_id",
                    "family_compact",
                    "depth_max",
                    "cycles_per_case",
                    "max_cells",
                ],
                "cache_value_fields": [
                    "family_name",
                    "stress_cli_args",
                    "expected_cycle_slot_identity",
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
                    "cycle results as substitute execution",
                ],
            },
            "cycle_slot_identity_guard": {
                "expected_cycle_slot_ids": EXPECTED_CYCLE_SLOTS,
                "families_must_remain_A_E": ["A", "B", "C", "D", "E"],
                "probe_must_remain": "MICRO_02_CYCLE_PRESSURE",
                "fail_closed_if_slot_identity_changes": True,
                "fail_closed_if_any_cycle_slot_missing": True,
                "fail_closed_if_any_cycle_slot_merged": True,
                "fail_closed_if_cycles_per_case_changes": True,
            },
        },
        "expected_metric_direction": {
            "primary_metric": "elapsed_ms",
            "secondary_metric": "receipts_per_sec",
            "target_rows": "rows with burden_class == BURDEN_CYCLE_SCAN",
            "before_profile_id": EXPECTED_AFTER_PROFILE_ID,
            "before_target_elapsed_ms": target.get("elapsed_ms"),
            "before_target_receipts": target.get("receipts"),
            "before_target_rows": target.get("rows"),
            "expected_elapsed_ms": "decrease_or_non_worse",
            "expected_receipts_per_sec": "increase_or_non_worse",
            "must_preserve_target_rows": 5,
            "must_preserve_target_receipts": target.get("receipts"),
            "must_preserve_cycle_slot_identity_exactly": EXPECTED_CYCLE_SLOTS,
            "must_preserve_profile_receipts_total_match_registry": True,
            "must_preserve_family_coverage_A_E": True,
            "must_not_change_halt_law_gate_run_semantics": True,
        },
        "required_retest": {
            "before_profile_id": EXPECTED_AFTER_PROFILE_ID,
            "after_profile_required": True,
            "same_micro_suite_required": True,
            "same_probe_specs_required": True,
            "same_script": "scripts/wide_burden_profile_microruns.py --execute",
            "comparison_required": True,
            "comparison_artifact_schema": "cycle_period_compression_before_after_comparison_v0",
            "pass_condition": [
                "after profile gate MICRO_BURDEN_PROFILE_PASS",
                "receipt totals match registry.sqlite",
                "all five probes complete",
                "family coverage A-E preserved",
                "cycle-scan row keys preserved",
                "cycle-scan receipts preserved",
                "no gate semantics change",
                "no law semantics change",
                "no halt semantics change",
                "no run semantics change",
                "no execution skipping",
                "no cycle execution skipping",
                "no early halt on period detection",
                "no synthetic receipts",
                "BURDEN_CYCLE_SCAN target rows show non-worse elapsed_ms or explicit failure classification",
            ],
        },
        "apply_gate": {
            "candidate_does_not_apply_itself": True,
            "must_be_followed_by_explicit_apply_command": True,
            "apply_command_goal_if_accepted": "APPLY_CYCLE_PERIOD_COMPRESSION_FIX_V0",
            "stop_if_patch_touches_forbidden_semantics": True,
            "stop_if_patch_skips_cycle_execution": True,
            "stop_if_patch_early_halts_on_period_detection": True,
            "stop_if_patch_synthesizes_receipts": True,
            "stop_if_patch_reuses_prior_cycle_results": True,
            "stop_if_patch_changes_halt_law_gate_or_run_semantics": True,
        },
        "forbidden": {
            "skip_cycle_execution": True,
            "early_halt_on_period_detection": True,
            "reuse_prior_cycle_results_as_current_execution": True,
            "emit_synthetic_receipts_for_unexecuted_cycles": True,
            "delete_receipts": True,
            "compress_raw_receipts": True,
            "receipt_schema_change": True,
            "halt_semantics_change": True,
            "law_semantics_change": True,
            "gate_semantics_change": True,
            "run_semantics_change": True,
            "radius_expansion": True,
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": "APPLY_CYCLE_PERIOD_COMPRESSION_FIX_V0" if not failures else None,
            "stop_code": None if not failures else "STOP_CYCLE_PERIOD_FIX_CANDIDATE_INVALID",
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
        "schema_version": "cycle_period_compression_fix_candidate_receipt_v0",
        "candidate_id": sig,
        "candidate_path": f"data/cycle_period_compression_fix_candidates/{sig}.json",
        "candidate_sig8": sig,
        "candidate_name": EXPECTED_FIX_CANDIDATE_ID,
        "candidate_status": candidate["candidate_status"],
        "source_policy_id": policy.get("policy_id"),
        "source_after_profile_id": EXPECTED_AFTER_PROFILE_ID,
        "target_burden_class": EXPECTED_TARGET_BURDEN_CLASS,
        "target_rows": target.get("rows"),
        "target_receipts": target.get("receipts"),
        "target_elapsed_ms": target.get("elapsed_ms"),
        "authorizes_patch_application": False,
        "authorizes_execution_skipping": False,
        "authorizes_cycle_execution_skipping": False,
        "authorizes_early_halt_on_period_detection": False,
        "authorizes_synthetic_cycle_receipts": False,
        "authorizes_reusing_prior_cycle_results_as_execution": False,
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
    print(f"candidate_json_path=data/cycle_period_compression_fix_candidates/{candidate['candidate_id']}.json")
    print(f"candidate_receipt_path=data/cycle_period_compression_fix_candidate_receipts/{candidate['candidate_id']}.json")

    return 0 if candidate["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
