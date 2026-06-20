#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

COMPARISON_DIR = ROOT / "data" / "frontier_depth_probe_before_after_comparisons"
APPLICATION_DIR = ROOT / "data" / "frontier_depth_probe_fix_applications"
PROFILE_DIR = ROOT / "data" / "micro_burden_profiles"

DECISION_DIR = ROOT / "data" / "frontier_depth_probe_fix_outcome_decisions"
RECEIPT_DIR = ROOT / "data" / "frontier_depth_probe_fix_outcome_decision_receipts"

EXPECTED_COMPARISON_ID = "ed563880"
EXPECTED_APPLICATION_ID = "f537dd1f"
EXPECTED_SOURCE_CANDIDATE_ID = "40429f27"
EXPECTED_SOURCE_POLICY_ID = "42028fa3"
EXPECTED_BEFORE_PROFILE_ID = "45cd7660"
EXPECTED_AFTER_PROFILE_ID = "26966e56"
EXPECTED_TARGET = "BURDEN_DEPTH_SCAN"

EXPECTED_TARGET_RESULT = "TARGET_BURDEN_ELAPSED_WORSE_EXPLICIT_FAILURE_CLASSIFICATION"

EXPECTED_DEPTH_SLOTS = [
    "MICRO_03_DEPTH_PRESSURE_A",
    "MICRO_03_DEPTH_PRESSURE_B",
    "MICRO_03_DEPTH_PRESSURE_C",
    "MICRO_03_DEPTH_PRESSURE_D",
    "MICRO_03_DEPTH_PRESSURE_E",
]

ACCEPTED_FROZEN = [
    "BURDEN_CYCLE_SCAN",
    "BURDEN_DB_WRITE",
    "BURDEN_REPEATED_SLOT_WORK",
]

NEXT_COMMAND_GOAL = "BUILD_FRONTIER_DEPTH_PROBE_REVERT_OR_OBSERVABILITY_FREEZE_PLAN_V0"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_sig(obj: dict[str, Any]) -> str:
    body = dict(obj)
    for key in ("decision_id", "decision_sig8", "receipt_id", "receipt_sig8"):
        body.pop(key, None)
    blob = json.dumps(body, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:8]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def verify_frontier_depth_observation(obs: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if obs.get("status") != "APPLIED_POST_EXECUTION_DEPTH_METADATA_ONLY":
        failures.append(f"frontier_depth_status_wrong:{obs.get('status')}")
    if obs.get("certificate_kind") != "frontier_depth_observation_certificate":
        failures.append(f"frontier_depth_kind_wrong:{obs.get('certificate_kind')}")
    if obs.get("certificate_scope") != "post_execution_depth_observation_metadata_only":
        failures.append(f"frontier_depth_scope_wrong:{obs.get('certificate_scope')}")
    if obs.get("certificate_count") != 5:
        failures.append(f"frontier_depth_certificate_count_wrong:{obs.get('certificate_count')}")
    if obs.get("expected_depth_slot_ids") != EXPECTED_DEPTH_SLOTS:
        failures.append(f"frontier_depth_expected_slots_wrong:{obs.get('expected_depth_slot_ids')}")
    if obs.get("observed_depth_slot_ids") != EXPECTED_DEPTH_SLOTS:
        failures.append(f"frontier_depth_observed_slots_wrong:{obs.get('observed_depth_slot_ids')}")
    if obs.get("slot_identity_matches_expected") is not True:
        failures.append("frontier_depth_slot_identity_not_preserved")
    if obs.get("does_not_certify_without_execution") is not True:
        failures.append("frontier_depth_certifies_without_execution")
    if obs.get("does_not_change_depth_range") is not True:
        failures.append("frontier_depth_changes_depth_range")
    if obs.get("does_not_change_depth_min") is not True:
        failures.append("frontier_depth_changes_depth_min")
    if obs.get("does_not_change_depth_max") is not True:
        failures.append("frontier_depth_changes_depth_max")
    if obs.get("does_not_expand_radius") is not True:
        failures.append("frontier_depth_expands_radius")
    if obs.get("does_not_skip_execution") is not True:
        failures.append("frontier_depth_skips_execution")
    if obs.get("does_not_skip_depth_probe_execution") is not True:
        failures.append("frontier_depth_skips_depth_probe_execution")
    if obs.get("does_not_skip_frontier_cases") is not True:
        failures.append("frontier_depth_skips_frontier_cases")
    if obs.get("does_not_emit_synthetic_depth_receipts") is not True:
        failures.append("frontier_depth_emits_synthetic_depth_receipts")
    if obs.get("does_not_reuse_prior_depth_results_as_execution") is not True:
        failures.append("frontier_depth_reuses_prior_depth_results_as_execution")
    if obs.get("does_not_reopen_accepted_burden_classes") is not True:
        failures.append("frontier_depth_reopens_accepted_burden_classes")
    if obs.get("accepted_burden_classes_frozen") != ACCEPTED_FROZEN:
        failures.append(f"frontier_depth_accepted_frozen_wrong:{obs.get('accepted_burden_classes_frozen')}")

    sem = obs.get("semantics") or {}
    for key in [
        "execution_skipping",
        "depth_probe_skipping",
        "frontier_case_skipping",
        "synthetic_depth_receipts",
        "reusing_prior_depth_results_as_execution",
        "depth_range_change",
        "depth_min_change",
        "depth_max_change",
        "radius_expansion",
        "halt_semantics_change",
        "law_semantics_change",
        "gate_semantics_change",
        "run_semantics_change",
        "receipt_deletion",
        "receipt_compression",
        "reopening_accepted_burden_classes",
    ]:
        if sem.get(key) is not False:
            failures.append(f"frontier_depth_semantics_not_preserved:{key}:{sem.get(key)}")

    return failures


def verify_sources(
    comparison: dict[str, Any],
    application: dict[str, Any],
    before_profile: dict[str, Any],
    after_profile: dict[str, Any],
) -> list[str]:
    failures: list[str] = []

    if comparison.get("comparison_id") != EXPECTED_COMPARISON_ID:
        failures.append(f"comparison_id_mismatch:{comparison.get('comparison_id')}")
    if comparison.get("comparison_id") != comparison.get("comparison_sig8"):
        failures.append("comparison_sig_mismatch")
    if comparison.get("gate") != "PASS":
        failures.append("comparison_gate_not_PASS")
    if comparison.get("failures") != []:
        failures.append(f"comparison_failures_not_empty:{comparison.get('failures')}")
    if comparison.get("source_application_id") != EXPECTED_APPLICATION_ID:
        failures.append(f"comparison_application_mismatch:{comparison.get('source_application_id')}")
    if comparison.get("source_candidate_id") != EXPECTED_SOURCE_CANDIDATE_ID:
        failures.append(f"comparison_candidate_mismatch:{comparison.get('source_candidate_id')}")
    if comparison.get("source_policy_id") != EXPECTED_SOURCE_POLICY_ID:
        failures.append(f"comparison_policy_mismatch:{comparison.get('source_policy_id')}")
    if comparison.get("before_profile_id") != EXPECTED_BEFORE_PROFILE_ID:
        failures.append(f"comparison_before_profile_mismatch:{comparison.get('before_profile_id')}")
    if comparison.get("after_profile_id") != EXPECTED_AFTER_PROFILE_ID:
        failures.append(f"comparison_after_profile_mismatch:{comparison.get('after_profile_id')}")
    if comparison.get("target_burden_class") != EXPECTED_TARGET:
        failures.append(f"comparison_target_mismatch:{comparison.get('target_burden_class')}")
    if comparison.get("target_result") != EXPECTED_TARGET_RESULT:
        failures.append(f"comparison_target_result_not_performance_negative:{comparison.get('target_result')}")

    delta = comparison.get("target_delta") or {}
    if int(delta.get("elapsed_ms_delta") or 0) <= 0:
        failures.append(f"expected_positive_elapsed_delta:{delta.get('elapsed_ms_delta')}")
    if float(delta.get("speedup_before_over_after") or 1.0) >= 1.0:
        failures.append(f"expected_speedup_below_one:{delta.get('speedup_before_over_after')}")
    if int(delta.get("after_elapsed_ms") or 0) <= int(delta.get("before_elapsed_ms") or 0):
        failures.append("expected_after_elapsed_greater_than_before")

    target_before = comparison.get("target_before") or {}
    target_after = comparison.get("target_after") or {}

    if target_before.get("rows") != 5:
        failures.append(f"target_before_rows_not_5:{target_before.get('rows')}")
    if target_after.get("rows") != 5:
        failures.append(f"target_after_rows_not_5:{target_after.get('rows')}")
    if target_before.get("receipts") != 345:
        failures.append(f"target_before_receipts_not_345:{target_before.get('receipts')}")
    if target_after.get("receipts") != 345:
        failures.append(f"target_after_receipts_not_345:{target_after.get('receipts')}")
    if target_before.get("slots") != EXPECTED_DEPTH_SLOTS:
        failures.append(f"target_before_slots_wrong:{target_before.get('slots')}")
    if target_after.get("slots") != EXPECTED_DEPTH_SLOTS:
        failures.append(f"target_after_slots_wrong:{target_after.get('slots')}")
    if target_before.get("families") != ["A", "B", "C", "D", "E"]:
        failures.append(f"target_before_families_wrong:{target_before.get('families')}")
    if target_after.get("families") != ["A", "B", "C", "D", "E"]:
        failures.append(f"target_after_families_wrong:{target_after.get('families')}")
    if target_before.get("probes") != ["MICRO_03_DEPTH_PRESSURE"]:
        failures.append(f"target_before_probe_wrong:{target_before.get('probes')}")
    if target_after.get("probes") != ["MICRO_03_DEPTH_PRESSURE"]:
        failures.append(f"target_after_probe_wrong:{target_after.get('probes')}")

    rules = comparison.get("gate_rules") or {}
    if not rules:
        failures.append("comparison_gate_rules_missing")
    else:
        for key, value in sorted(rules.items()):
            if key == "target_depth_elapsed_non_worse":
                if value is not False:
                    failures.append(f"expected_target_depth_elapsed_non_worse_false:{value}")
            elif value is not True:
                failures.append(f"comparison_gate_rule_false:{key}:{value}")
        if rules.get("target_depth_elapsed_non_worse_or_explicitly_classified") is not True:
            failures.append("explicit_failure_classification_gate_missing")

    failures.extend(verify_frontier_depth_observation(comparison.get("frontier_depth_observation") or {}))

    if application.get("application_id") != EXPECTED_APPLICATION_ID:
        failures.append(f"application_id_mismatch:{application.get('application_id')}")
    if application.get("gate") != "PASS":
        failures.append("application_gate_not_PASS")
    if application.get("source_candidate_id") != EXPECTED_SOURCE_CANDIDATE_ID:
        failures.append(f"application_candidate_mismatch:{application.get('source_candidate_id')}")
    if application.get("source_policy_id") != EXPECTED_SOURCE_POLICY_ID:
        failures.append(f"application_policy_mismatch:{application.get('source_policy_id')}")
    if application.get("before_profile_id") != EXPECTED_BEFORE_PROFILE_ID:
        failures.append(f"application_before_profile_mismatch:{application.get('before_profile_id')}")
    if application.get("target_burden_class") != EXPECTED_TARGET:
        failures.append(f"application_target_mismatch:{application.get('target_burden_class')}")

    app_self = application.get("application_self_test") or {}
    if app_self.get("certificate_count") != 5:
        failures.append(f"application_certificate_count_wrong:{app_self.get('certificate_count')}")
    if app_self.get("slot_identity_matches_expected") is not True:
        failures.append("application_slot_identity_self_test_failed")
    if app_self.get("depth_range_preserved") is not True:
        failures.append("application_depth_range_not_preserved")
    if app_self.get("radius_not_expanded") is not True:
        failures.append("application_radius_expanded")

    app_sem = application.get("semantics") or {}
    if app_sem.get("patch_application") is not True:
        failures.append("application_patch_application_marker_missing")
    for key in [
        "execution_skipping",
        "depth_probe_skipping",
        "frontier_case_skipping",
        "synthetic_depth_receipts",
        "reusing_prior_depth_results_as_execution",
        "reusing_prior_run_results_as_execution",
        "depth_range_change",
        "depth_min_change",
        "depth_max_change",
        "radius_expansion",
        "halt_semantics_change",
        "law_semantics_change",
        "gate_semantics_change",
        "run_semantics_change",
        "receipt_deletion",
        "receipt_compression",
        "receipt_schema_change",
        "reopening_accepted_burden_classes",
    ]:
        if app_sem.get(key) is not False:
            failures.append(f"application_semantics_not_preserved:{key}:{app_sem.get(key)}")

    if before_profile.get("profile_id") != EXPECTED_BEFORE_PROFILE_ID:
        failures.append(f"before_profile_id_mismatch:{before_profile.get('profile_id')}")
    if after_profile.get("profile_id") != EXPECTED_AFTER_PROFILE_ID:
        failures.append(f"after_profile_id_mismatch:{after_profile.get('profile_id')}")
    if before_profile.get("gate") != "MICRO_BURDEN_PROFILE_PASS":
        failures.append("before_profile_gate_not_PASS")
    if after_profile.get("gate") != "MICRO_BURDEN_PROFILE_PASS":
        failures.append("after_profile_gate_not_PASS")
    if before_profile.get("profile_receipts_total") != 1457:
        failures.append(f"before_profile_total_not_1457:{before_profile.get('profile_receipts_total')}")
    if after_profile.get("profile_receipts_total") != 1457:
        failures.append(f"after_profile_total_not_1457:{after_profile.get('profile_receipts_total')}")
    if after_profile.get("profile_receipts_total") != after_profile.get("db_receipt_delta"):
        failures.append("after_profile_receipt_total_mismatch_registry")
    if before_profile.get("profile_receipts_total") != before_profile.get("db_receipt_delta"):
        failures.append("before_profile_receipt_total_mismatch_registry")
    if after_profile.get("families_seen") != ["A", "B", "C", "D", "E"]:
        failures.append("after_profile_family_coverage_not_A_E")
    if len(after_profile.get("rows") or []) != 25:
        failures.append(f"after_profile_rows_not_25:{len(after_profile.get('rows') or [])}")

    return failures


def build_decision(comparison_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    DECISION_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    comparison = load_json(COMPARISON_DIR / f"{comparison_id}.json")
    application = load_json(APPLICATION_DIR / f"{EXPECTED_APPLICATION_ID}.json")
    before_profile = load_json(PROFILE_DIR / f"{EXPECTED_BEFORE_PROFILE_ID}.json")
    after_profile = load_json(PROFILE_DIR / f"{EXPECTED_AFTER_PROFILE_ID}.json")

    failures = verify_sources(comparison, application, before_profile, after_profile)
    warnings = list(comparison.get("warnings") or [])

    delta = comparison.get("target_delta") or {}

    decision = {
        "schema_version": "frontier_depth_probe_fix_outcome_decision_v0",
        "decision_kind": "FRONTIER_DEPTH_PROBE_FIX_OUTCOME_OR_NEXT_BURDEN_CLASS_DECISION",
        "source_comparison": {
            "comparison_id": comparison.get("comparison_id"),
            "comparison_sig8": comparison.get("comparison_sig8"),
            "gate": comparison.get("gate"),
            "path": f"data/frontier_depth_probe_before_after_comparisons/{comparison_id}.json",
        },
        "source_application_id": EXPECTED_APPLICATION_ID,
        "source_candidate_id": EXPECTED_SOURCE_CANDIDATE_ID,
        "source_policy_id": EXPECTED_SOURCE_POLICY_ID,
        "before_profile_id": EXPECTED_BEFORE_PROFILE_ID,
        "after_profile_id": EXPECTED_AFTER_PROFILE_ID,
        "target_burden_class": EXPECTED_TARGET,
        "target_result": comparison.get("target_result"),
        "target_metric_delta": delta,
        "frontier_depth_fix_outcome": "REJECT_FRONTIER_DEPTH_PROBE_FIX_AS_BURDEN_FIX",
        "safety_classification": "STRUCTURALLY_SAFE_OBSERVABILITY_PATCH_BUT_PERFORMANCE_NEGATIVE",
        "reason": {
            "primary_rejection_reason": "target BURDEN_DEPTH_SCAN elapsed_ms worsened",
            "before_elapsed_ms": delta.get("before_elapsed_ms"),
            "after_elapsed_ms": delta.get("after_elapsed_ms"),
            "elapsed_ms_delta": delta.get("elapsed_ms_delta"),
            "elapsed_ratio_after_vs_before": delta.get("elapsed_ratio_after_vs_before"),
            "speedup_before_over_after": delta.get("speedup_before_over_after"),
            "structural_evidence_clean": True,
            "semantic_evidence_clean": True,
            "performance_evidence_positive": False,
        },
        "accepted_as_burden_fix": False,
        "accepted_as_observability_only": False,
        "not_accepted_changes": [
            "ADDED_FRONTIER_DEPTH_METADATA_CERTIFICATE_OBJECT",
            "ADDED_POST_EXECUTION_FRONTIER_DEPTH_OBSERVATION_BUILDER",
            "ADDED_DEPTH_PRESSURE_SLOT_IDENTITY_SURFACE",
            "PRESERVED_DEPTH_RANGE_RADIUS_AND_RUN_SEMANTICS",
        ],
        "disposition_required_before_next_burden": {
            "must_not_advance_to_next_burden_yet": True,
            "must_choose_revert_or_observability_freeze": True,
            "default_recommended_disposition": "REVERT_FRONTIER_DEPTH_METADATA_CERTIFICATE_PATCH",
            "alternate_disposition_allowed_only_if_explicitly_marked": "FREEZE_AS_OBSERVABILITY_ONLY_NOT_BURDEN_FIX",
            "reason": "A performance-negative patch cannot be silently carried as a burden optimization.",
        },
        "authorization": {
            "authorizes_next_burden_policy": False,
            "authorizes_revert_or_observability_freeze_plan": True,
            "authorizes_patch_application": False,
            "authorizes_code_change": False,
            "authorizes_more_frontier_depth_patching": False,
            "authorizes_accepting_frontier_depth_as_burden_fix": False,
            "authorizes_execution_skipping": False,
            "authorizes_depth_probe_skipping": False,
            "authorizes_frontier_case_skipping": False,
            "authorizes_synthetic_depth_receipts": False,
            "authorizes_reusing_prior_depth_results_as_execution": False,
            "authorizes_depth_range_change": False,
            "authorizes_depth_min_change": False,
            "authorizes_depth_max_change": False,
            "authorizes_radius_expansion": False,
            "authorizes_receipt_deletion": False,
            "authorizes_receipt_compression": False,
            "authorizes_halt_semantics_change": False,
            "authorizes_law_semantics_change": False,
            "authorizes_gate_semantics_change": False,
            "authorizes_run_semantics_change": False,
            "authorizes_reopening_accepted_burden_classes": False,
        },
        "required_next_gate": {
            "next_command_must_target": "frontier_depth_probe_fix_disposition",
            "allowed_next_goal": NEXT_COMMAND_GOAL,
            "must_use_comparison_id": EXPECTED_COMPARISON_ID,
            "must_use_application_id": EXPECTED_APPLICATION_ID,
            "must_not_delete_receipts": True,
            "must_not_change_halt_law_gate_run_semantics": True,
            "must_not_expand_radius": True,
            "must_not_change_depth_range": True,
            "must_not_reopen_accepted_burden_classes_without_explicit_new_failure": ACCEPTED_FROZEN,
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_FRONTIER_DEPTH_OUTCOME_DECISION_INVALID",
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "PASS" if not failures else "FAIL",
        "created_at": now_iso(),
    }

    sig = stable_sig(decision)
    decision["decision_id"] = sig
    decision["decision_sig8"] = sig

    receipt = {
        "schema_version": "frontier_depth_probe_fix_outcome_decision_receipt_v0",
        "decision_id": sig,
        "decision_path": f"data/frontier_depth_probe_fix_outcome_decisions/{sig}.json",
        "decision_sig8": sig,
        "source_comparison_id": comparison_id,
        "source_application_id": EXPECTED_APPLICATION_ID,
        "source_candidate_id": EXPECTED_SOURCE_CANDIDATE_ID,
        "source_policy_id": EXPECTED_SOURCE_POLICY_ID,
        "before_profile_id": EXPECTED_BEFORE_PROFILE_ID,
        "after_profile_id": EXPECTED_AFTER_PROFILE_ID,
        "target_burden_class": EXPECTED_TARGET,
        "target_result": comparison.get("target_result"),
        "frontier_depth_fix_outcome": decision["frontier_depth_fix_outcome"],
        "safety_classification": decision["safety_classification"],
        "target_metric_delta": delta,
        "accepted_as_burden_fix": False,
        "accepted_as_observability_only": False,
        "authorizes_next_burden_policy": False,
        "authorizes_revert_or_observability_freeze_plan": True,
        "gate": decision["gate"],
        "terminal": decision["terminal"],
        "failures": failures,
        "warnings": warnings,
        "created_at": now_iso(),
    }

    receipt_sig = stable_sig(receipt)
    receipt["receipt_id"] = receipt_sig
    receipt["receipt_sig8"] = receipt_sig

    (DECISION_DIR / f"{sig}.json").write_text(json.dumps(decision, indent=2, sort_keys=True))
    (RECEIPT_DIR / f"{sig}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return decision, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--comparison", default=EXPECTED_COMPARISON_ID)
    args = parser.parse_args()

    decision, receipt = build_decision(args.comparison)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"decision_json_path=data/frontier_depth_probe_fix_outcome_decisions/{decision['decision_id']}.json")
    print(f"decision_receipt_path=data/frontier_depth_probe_fix_outcome_decision_receipts/{decision['decision_id']}.json")

    return 0 if decision["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
