#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

DECISION_DIR = ROOT / "data" / "frontier_depth_probe_fix_outcome_decisions"
COMPARISON_DIR = ROOT / "data" / "frontier_depth_probe_before_after_comparisons"
APPLICATION_DIR = ROOT / "data" / "frontier_depth_probe_fix_applications"
CANDIDATE_DIR = ROOT / "data" / "frontier_depth_probe_fix_candidates"
POLICY_DIR = ROOT / "data" / "frontier_depth_probe_fix_candidate_policies"

PLAN_DIR = ROOT / "data" / "frontier_depth_probe_fix_disposition_plans"
RECEIPT_DIR = ROOT / "data" / "frontier_depth_probe_fix_disposition_plan_receipts"

EXPECTED_DECISION_ID = "22d0002e"
EXPECTED_COMPARISON_ID = "ed563880"
EXPECTED_APPLICATION_ID = "f537dd1f"
EXPECTED_SOURCE_CANDIDATE_ID = "40429f27"
EXPECTED_SOURCE_POLICY_ID = "42028fa3"
EXPECTED_BEFORE_PROFILE_ID = "45cd7660"
EXPECTED_AFTER_PROFILE_ID = "26966e56"
EXPECTED_TARGET = "BURDEN_DEPTH_SCAN"

SELECTED_DISPOSITION = "REVERT_FRONTIER_DEPTH_METADATA_CERTIFICATE_PATCH"
NEXT_COMMAND_GOAL = "APPLY_FRONTIER_DEPTH_PROBE_REVERT_V0"

EXPECTED_TARGET_RESULT = "TARGET_BURDEN_ELAPSED_WORSE_EXPLICIT_FAILURE_CLASSIFICATION"
EXPECTED_FIX_OUTCOME = "REJECT_FRONTIER_DEPTH_PROBE_FIX_AS_BURDEN_FIX"
EXPECTED_SAFETY_CLASS = "STRUCTURALLY_SAFE_OBSERVABILITY_PATCH_BUT_PERFORMANCE_NEGATIVE"

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

REVERT_MARKERS = {
    "helper_class": "class FrontierDepthCertificate",
    "slot_ids": "EXPECTED_FRONTIER_DEPTH_SLOT_IDS",
    "observation_helper": "def _build_frontier_depth_probe_observation(",
    "profile_field": '"frontier_depth_probe": _build_frontier_depth_probe_observation(rows),',
    "certificate_scope": "post_execution_depth_observation_metadata_only",
    "status": "APPLIED_POST_EXECUTION_DEPTH_METADATA_ONLY",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_sig(obj: dict[str, Any]) -> str:
    body = dict(obj)
    for key in ("plan_id", "plan_sig8", "receipt_id", "receipt_sig8"):
        body.pop(key, None)
    blob = json.dumps(body, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:8]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def verify_decision(decision: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if decision.get("decision_id") != EXPECTED_DECISION_ID:
        failures.append(f"decision_id_mismatch:{decision.get('decision_id')}")
    if decision.get("decision_id") != decision.get("decision_sig8"):
        failures.append("decision_sig_mismatch")
    if decision.get("gate") != "PASS":
        failures.append("decision_gate_not_PASS")
    if decision.get("failures") != []:
        failures.append(f"decision_failures_not_empty:{decision.get('failures')}")

    source_comparison = decision.get("source_comparison") or {}
    if source_comparison.get("comparison_id") != EXPECTED_COMPARISON_ID:
        failures.append(f"decision_comparison_mismatch:{source_comparison.get('comparison_id')}")
    if decision.get("source_application_id") != EXPECTED_APPLICATION_ID:
        failures.append(f"decision_application_mismatch:{decision.get('source_application_id')}")
    if decision.get("source_candidate_id") != EXPECTED_SOURCE_CANDIDATE_ID:
        failures.append(f"decision_candidate_mismatch:{decision.get('source_candidate_id')}")
    if decision.get("source_policy_id") != EXPECTED_SOURCE_POLICY_ID:
        failures.append(f"decision_policy_mismatch:{decision.get('source_policy_id')}")
    if decision.get("before_profile_id") != EXPECTED_BEFORE_PROFILE_ID:
        failures.append(f"decision_before_profile_mismatch:{decision.get('before_profile_id')}")
    if decision.get("after_profile_id") != EXPECTED_AFTER_PROFILE_ID:
        failures.append(f"decision_after_profile_mismatch:{decision.get('after_profile_id')}")
    if decision.get("target_burden_class") != EXPECTED_TARGET:
        failures.append(f"decision_target_mismatch:{decision.get('target_burden_class')}")
    if decision.get("target_result") != EXPECTED_TARGET_RESULT:
        failures.append(f"decision_target_result_mismatch:{decision.get('target_result')}")
    if decision.get("frontier_depth_fix_outcome") != EXPECTED_FIX_OUTCOME:
        failures.append(f"decision_fix_outcome_mismatch:{decision.get('frontier_depth_fix_outcome')}")
    if decision.get("safety_classification") != EXPECTED_SAFETY_CLASS:
        failures.append(f"decision_safety_class_mismatch:{decision.get('safety_classification')}")
    if decision.get("accepted_as_burden_fix") is not False:
        failures.append("decision_accepted_as_burden_fix")
    if decision.get("accepted_as_observability_only") is not False:
        failures.append("decision_accepted_as_observability_only")

    reason = decision.get("reason") or {}
    if reason.get("performance_evidence_positive") is not False:
        failures.append("decision_performance_evidence_not_negative")
    if int(reason.get("elapsed_ms_delta") or 0) <= 0:
        failures.append(f"decision_elapsed_delta_not_positive:{reason.get('elapsed_ms_delta')}")
    if float(reason.get("speedup_before_over_after") or 1.0) >= 1.0:
        failures.append(f"decision_speedup_not_below_one:{reason.get('speedup_before_over_after')}")
    if reason.get("structural_evidence_clean") is not True:
        failures.append("decision_structural_evidence_not_clean")
    if reason.get("semantic_evidence_clean") is not True:
        failures.append("decision_semantic_evidence_not_clean")

    disposition = decision.get("disposition_required_before_next_burden") or {}
    if disposition.get("must_not_advance_to_next_burden_yet") is not True:
        failures.append("decision_allows_advancing_to_next_burden")
    if disposition.get("must_choose_revert_or_observability_freeze") is not True:
        failures.append("decision_missing_disposition_requirement")
    if disposition.get("default_recommended_disposition") != SELECTED_DISPOSITION:
        failures.append(f"decision_default_disposition_not_revert:{disposition.get('default_recommended_disposition')}")
    if disposition.get("alternate_disposition_allowed_only_if_explicitly_marked") != "FREEZE_AS_OBSERVABILITY_ONLY_NOT_BURDEN_FIX":
        failures.append("decision_alternate_disposition_marker_missing")

    auth = decision.get("authorization") or {}
    if auth.get("authorizes_revert_or_observability_freeze_plan") is not True:
        failures.append("decision_does_not_authorize_disposition_plan")
    if auth.get("authorizes_next_burden_policy") is not False:
        failures.append("decision_illegally_authorizes_next_burden_policy")
    for key in [
        "authorizes_patch_application",
        "authorizes_code_change",
        "authorizes_more_frontier_depth_patching",
        "authorizes_accepting_frontier_depth_as_burden_fix",
        "authorizes_execution_skipping",
        "authorizes_depth_probe_skipping",
        "authorizes_frontier_case_skipping",
        "authorizes_synthetic_depth_receipts",
        "authorizes_reusing_prior_depth_results_as_execution",
        "authorizes_depth_range_change",
        "authorizes_depth_min_change",
        "authorizes_depth_max_change",
        "authorizes_radius_expansion",
        "authorizes_receipt_deletion",
        "authorizes_receipt_compression",
        "authorizes_halt_semantics_change",
        "authorizes_law_semantics_change",
        "authorizes_gate_semantics_change",
        "authorizes_run_semantics_change",
        "authorizes_reopening_accepted_burden_classes",
    ]:
        if auth.get(key) is not False:
            failures.append(f"decision_illegal_authorization:{key}:{auth.get(key)}")

    required_next = decision.get("required_next_gate") or {}
    if required_next.get("allowed_next_goal") != "BUILD_FRONTIER_DEPTH_PROBE_REVERT_OR_OBSERVABILITY_FREEZE_PLAN_V0":
        failures.append(f"required_next_allowed_goal_mismatch:{required_next.get('allowed_next_goal')}")
    if required_next.get("must_use_comparison_id") != EXPECTED_COMPARISON_ID:
        failures.append("required_next_comparison_mismatch")
    if required_next.get("must_use_application_id") != EXPECTED_APPLICATION_ID:
        failures.append("required_next_application_mismatch")
    if required_next.get("must_not_delete_receipts") is not True:
        failures.append("required_next_may_delete_receipts")
    if required_next.get("must_not_change_halt_law_gate_run_semantics") is not True:
        failures.append("required_next_may_change_semantics")
    if required_next.get("must_not_expand_radius") is not True:
        failures.append("required_next_may_expand_radius")
    if required_next.get("must_not_change_depth_range") is not True:
        failures.append("required_next_may_change_depth_range")
    if required_next.get("must_not_reopen_accepted_burden_classes_without_explicit_new_failure") != ACCEPTED_FROZEN:
        failures.append("required_next_accepted_frozen_mismatch")

    terminal = decision.get("terminal") or {}
    if terminal.get("next_command_goal") != "BUILD_FRONTIER_DEPTH_PROBE_REVERT_OR_OBSERVABILITY_FREEZE_PLAN_V0":
        failures.append(f"decision_terminal_next_goal_mismatch:{terminal.get('next_command_goal')}")

    return failures


def verify_comparison(comparison: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if comparison.get("comparison_id") != EXPECTED_COMPARISON_ID:
        failures.append(f"comparison_id_mismatch:{comparison.get('comparison_id')}")
    if comparison.get("gate") != "PASS":
        failures.append("comparison_gate_not_PASS")
    if comparison.get("target_result") != EXPECTED_TARGET_RESULT:
        failures.append(f"comparison_target_result_mismatch:{comparison.get('target_result')}")
    if comparison.get("failures") != []:
        failures.append(f"comparison_failures_not_empty:{comparison.get('failures')}")
    if comparison.get("source_application_id") != EXPECTED_APPLICATION_ID:
        failures.append("comparison_application_mismatch")
    if comparison.get("source_candidate_id") != EXPECTED_SOURCE_CANDIDATE_ID:
        failures.append("comparison_candidate_mismatch")
    if comparison.get("source_policy_id") != EXPECTED_SOURCE_POLICY_ID:
        failures.append("comparison_policy_mismatch")
    if comparison.get("before_profile_id") != EXPECTED_BEFORE_PROFILE_ID:
        failures.append("comparison_before_profile_mismatch")
    if comparison.get("after_profile_id") != EXPECTED_AFTER_PROFILE_ID:
        failures.append("comparison_after_profile_mismatch")
    if comparison.get("target_burden_class") != EXPECTED_TARGET:
        failures.append("comparison_target_mismatch")

    before = comparison.get("target_before") or {}
    after = comparison.get("target_after") or {}
    delta = comparison.get("target_delta") or {}
    rules = comparison.get("gate_rules") or {}

    if before.get("rows") != 5 or after.get("rows") != 5:
        failures.append(f"comparison_target_rows_wrong:{before.get('rows')}->{after.get('rows')}")
    if before.get("receipts") != 345 or after.get("receipts") != 345:
        failures.append(f"comparison_target_receipts_wrong:{before.get('receipts')}->{after.get('receipts')}")
    if before.get("slots") != EXPECTED_DEPTH_SLOTS:
        failures.append(f"comparison_before_slots_wrong:{before.get('slots')}")
    if after.get("slots") != EXPECTED_DEPTH_SLOTS:
        failures.append(f"comparison_after_slots_wrong:{after.get('slots')}")

    if int(delta.get("elapsed_ms_delta") or 0) <= 0:
        failures.append(f"comparison_elapsed_delta_not_positive:{delta.get('elapsed_ms_delta')}")
    if float(delta.get("speedup_before_over_after") or 1.0) >= 1.0:
        failures.append(f"comparison_speedup_not_below_one:{delta.get('speedup_before_over_after')}")

    if rules.get("target_depth_elapsed_non_worse") is not False:
        failures.append("comparison_should_mark_elapsed_non_worse_false")
    if rules.get("target_depth_elapsed_non_worse_or_explicitly_classified") is not True:
        failures.append("comparison_explicit_classification_missing")

    for key in [
        "application_gate_pass",
        "after_profile_gate_pass",
        "after_receipt_totals_match_registry",
        "depth_range_preserved",
        "depth_slot_identity_preserved",
        "family_coverage_A_E_preserved",
        "frontier_depth_certificate_count_5",
        "frontier_depth_metadata_only_no_execution_substitution",
        "frontier_depth_metadata_present",
        "no_execution_skipping",
        "no_gate_semantics_changed",
        "no_law_semantics_changed",
        "no_receipt_deletion",
        "no_runner_semantics_changed",
        "profile_receipt_total_preserved",
        "radius_not_expanded",
        "same_row_count",
        "same_target_row_keys",
        "target_receipts_preserved",
    ]:
        if rules.get(key) is not True:
            failures.append(f"comparison_gate_rule_false:{key}:{rules.get(key)}")

    obs = comparison.get("frontier_depth_observation") or {}
    if obs.get("status") != "APPLIED_POST_EXECUTION_DEPTH_METADATA_ONLY":
        failures.append("comparison_observation_status_wrong")
    if obs.get("certificate_count") != 5:
        failures.append("comparison_observation_certificate_count_wrong")
    if obs.get("slot_identity_matches_expected") is not True:
        failures.append("comparison_observation_slot_identity_wrong")
    if obs.get("does_not_change_depth_range") is not True:
        failures.append("comparison_observation_depth_range_changed")
    if obs.get("does_not_expand_radius") is not True:
        failures.append("comparison_observation_radius_expanded")
    if obs.get("does_not_skip_depth_probe_execution") is not True:
        failures.append("comparison_observation_depth_probe_skipped")
    if obs.get("does_not_skip_frontier_cases") is not True:
        failures.append("comparison_observation_frontier_cases_skipped")
    if obs.get("does_not_emit_synthetic_depth_receipts") is not True:
        failures.append("comparison_observation_synthetic_depth_receipts")
    if obs.get("does_not_reuse_prior_depth_results_as_execution") is not True:
        failures.append("comparison_observation_reuses_depth_results")

    return failures


def verify_application(application: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if application.get("application_id") != EXPECTED_APPLICATION_ID:
        failures.append(f"application_id_mismatch:{application.get('application_id')}")
    if application.get("gate") != "PASS":
        failures.append("application_gate_not_PASS")
    if application.get("source_candidate_id") != EXPECTED_SOURCE_CANDIDATE_ID:
        failures.append("application_candidate_mismatch")
    if application.get("source_policy_id") != EXPECTED_SOURCE_POLICY_ID:
        failures.append("application_policy_mismatch")
    if application.get("before_profile_id") != EXPECTED_BEFORE_PROFILE_ID:
        failures.append("application_before_profile_mismatch")
    if application.get("target_burden_class") != EXPECTED_TARGET:
        failures.append("application_target_mismatch")

    sem = application.get("semantics") or {}
    if sem.get("patch_application") is not True:
        failures.append("application_patch_marker_missing")
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
        if sem.get(key) is not False:
            failures.append(f"application_semantics_not_preserved:{key}:{sem.get(key)}")

    return failures


def inspect_patch_markers() -> dict[str, Any]:
    path = ROOT / "scripts" / "wide_burden_profile_microruns.py"
    text = path.read_text()
    return {
        "patch_file": "scripts/wide_burden_profile_microruns.py",
        "markers_present": {name: marker in text for name, marker in REVERT_MARKERS.items()},
        "all_revert_markers_present": all(marker in text for marker in REVERT_MARKERS.values()),
    }


def build_plan(decision_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    PLAN_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    decision = load_json(DECISION_DIR / f"{decision_id}.json")
    comparison = load_json(COMPARISON_DIR / f"{EXPECTED_COMPARISON_ID}.json")
    application = load_json(APPLICATION_DIR / f"{EXPECTED_APPLICATION_ID}.json")
    candidate = load_json(CANDIDATE_DIR / f"{EXPECTED_SOURCE_CANDIDATE_ID}.json")
    policy = load_json(POLICY_DIR / f"{EXPECTED_SOURCE_POLICY_ID}.json")

    failures: list[str] = []
    failures.extend(verify_decision(decision))
    failures.extend(verify_comparison(comparison))
    failures.extend(verify_application(application))

    if candidate.get("candidate_id") != EXPECTED_SOURCE_CANDIDATE_ID or candidate.get("gate") != "PASS":
        failures.append("candidate_source_invalid")
    if policy.get("policy_id") != EXPECTED_SOURCE_POLICY_ID or policy.get("gate") != "PASS":
        failures.append("policy_source_invalid")

    marker_inspection = inspect_patch_markers()
    if marker_inspection["all_revert_markers_present"] is not True:
        failures.append("frontier_depth_patch_markers_not_all_present_for_revert_plan")

    warnings = list(decision.get("warnings") or [])
    delta = comparison.get("target_delta") or {}

    plan = {
        "schema_version": "frontier_depth_probe_fix_disposition_plan_v0",
        "plan_kind": "FRONTIER_DEPTH_PROBE_REVERT_OR_OBSERVABILITY_FREEZE_PLAN",
        "source_decision_id": EXPECTED_DECISION_ID,
        "source_comparison_id": EXPECTED_COMPARISON_ID,
        "source_application_id": EXPECTED_APPLICATION_ID,
        "source_candidate_id": EXPECTED_SOURCE_CANDIDATE_ID,
        "source_policy_id": EXPECTED_SOURCE_POLICY_ID,
        "before_profile_id": EXPECTED_BEFORE_PROFILE_ID,
        "after_profile_id": EXPECTED_AFTER_PROFILE_ID,
        "target_burden_class": EXPECTED_TARGET,
        "target_result": EXPECTED_TARGET_RESULT,
        "safety_classification": EXPECTED_SAFETY_CLASS,
        "selected_disposition": SELECTED_DISPOSITION,
        "selected_disposition_reason": {
            "performance_negative": True,
            "structurally_safe": True,
            "semantically_safe": True,
            "not_accepted_as_burden_fix": True,
            "not_accepted_as_observability_only": True,
            "before_elapsed_ms": delta.get("before_elapsed_ms"),
            "after_elapsed_ms": delta.get("after_elapsed_ms"),
            "elapsed_ms_delta": delta.get("elapsed_ms_delta"),
            "speedup_before_over_after": delta.get("speedup_before_over_after"),
            "default_recommended_by_decision": SELECTED_DISPOSITION,
        },
        "explicitly_not_selected": {
            "FREEZE_AS_OBSERVABILITY_ONLY_NOT_BURDEN_FIX": {
                "selected": False,
                "reason": "Decision did not accept observability-only carry; default is revert before next burden.",
            },
            "ADVANCE_TO_NEXT_BURDEN": {
                "selected": False,
                "reason": "Decision explicitly forbids next-burden advance until disposition is resolved.",
            },
            "MORE_FRONTIER_DEPTH_PATCHING": {
                "selected": False,
                "reason": "Decision explicitly forbids more frontier-depth patching after performance-negative result.",
            },
            "ACCEPT_AS_BURDEN_FIX": {
                "selected": False,
                "reason": "Target burden elapsed worsened.",
            },
        },
        "revert_plan": {
            "revert_kind": "REMOVE_FRONTIER_DEPTH_METADATA_CERTIFICATE_PATCH_ONLY",
            "target_files": ["scripts/wide_burden_profile_microruns.py"],
            "must_remove_markers": REVERT_MARKERS,
            "must_remove_profile_field": '"frontier_depth_probe": _build_frontier_depth_probe_observation(rows),',
            "must_leave_intact": [
                "cycle_period_compression observation",
                "micro burden profile execution loop",
                "raw receipt writes",
                "registry.sqlite rows",
                "DB write fix",
                "repeated-slot metadata plan cache",
                "cycle-period metadata certificate",
                "accepted/frozen burden class decisions",
                "comparison and decision artifacts under data/",
            ],
            "must_not_delete_receipts": True,
            "must_not_delete_data_artifacts": True,
            "must_not_change_depth_range": True,
            "must_not_expand_radius": True,
            "must_not_change_halt_law_gate_run_semantics": True,
            "must_not_reopen_accepted_burden_classes": ACCEPTED_FROZEN,
            "post_revert_required_checks": [
                "py_compile scripts/wide_burden_profile_microruns.py",
                "verify frontier-depth markers removed",
                "verify cycle-period markers still present",
                "smoke gate latest or smoke run",
                "write revert application receipt",
            ],
        },
        "authorization": {
            "authorizes_apply_revert_command": True,
            "authorized_next_command_goal": NEXT_COMMAND_GOAL,
            "authorizes_observability_freeze": False,
            "authorizes_next_burden_policy": False,
            "authorizes_more_frontier_depth_patching": False,
            "authorizes_accepting_as_burden_fix": False,
            "authorizes_patch_application_other_than_revert": False,
            "authorizes_code_change_scope": ["scripts/wide_burden_profile_microruns.py"],
            "authorizes_receipt_deletion": False,
            "authorizes_data_artifact_deletion": False,
            "authorizes_execution_skipping": False,
            "authorizes_depth_probe_skipping": False,
            "authorizes_frontier_case_skipping": False,
            "authorizes_synthetic_depth_receipts": False,
            "authorizes_depth_range_change": False,
            "authorizes_depth_min_change": False,
            "authorizes_depth_max_change": False,
            "authorizes_radius_expansion": False,
            "authorizes_halt_semantics_change": False,
            "authorizes_law_semantics_change": False,
            "authorizes_gate_semantics_change": False,
            "authorizes_run_semantics_change": False,
            "authorizes_reopening_accepted_burden_classes": False,
        },
        "marker_inspection": marker_inspection,
        "required_next_gate": {
            "next_command_goal": NEXT_COMMAND_GOAL,
            "must_use_plan_id": None,
            "must_use_decision_id": EXPECTED_DECISION_ID,
            "must_use_application_id": EXPECTED_APPLICATION_ID,
            "must_remove_frontier_depth_patch_markers": True,
            "must_preserve_cycle_period_patch_markers": True,
            "must_not_delete_receipts": True,
            "must_not_delete_data_artifacts": True,
            "must_not_change_depth_range": True,
            "must_not_expand_radius": True,
            "must_not_change_halt_law_gate_run_semantics": True,
            "must_not_reopen_accepted_burden_classes": ACCEPTED_FROZEN,
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_FRONTIER_DEPTH_DISPOSITION_PLAN_INVALID",
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "PASS" if not failures else "FAIL",
        "created_at": now_iso(),
    }

    sig = stable_sig(plan)
    plan["plan_id"] = sig
    plan["plan_sig8"] = sig
    plan["required_next_gate"]["must_use_plan_id"] = sig

    receipt = {
        "schema_version": "frontier_depth_probe_fix_disposition_plan_receipt_v0",
        "plan_id": sig,
        "plan_path": f"data/frontier_depth_probe_fix_disposition_plans/{sig}.json",
        "plan_sig8": sig,
        "source_decision_id": EXPECTED_DECISION_ID,
        "source_comparison_id": EXPECTED_COMPARISON_ID,
        "source_application_id": EXPECTED_APPLICATION_ID,
        "source_candidate_id": EXPECTED_SOURCE_CANDIDATE_ID,
        "source_policy_id": EXPECTED_SOURCE_POLICY_ID,
        "target_burden_class": EXPECTED_TARGET,
        "selected_disposition": SELECTED_DISPOSITION,
        "authorizes_apply_revert_command": True,
        "authorizes_observability_freeze": False,
        "authorizes_next_burden_policy": False,
        "authorizes_more_frontier_depth_patching": False,
        "marker_inspection": marker_inspection,
        "gate": plan["gate"],
        "terminal": plan["terminal"],
        "failures": failures,
        "warnings": warnings,
        "created_at": now_iso(),
    }

    receipt_sig = stable_sig(receipt)
    receipt["receipt_id"] = receipt_sig
    receipt["receipt_sig8"] = receipt_sig

    (PLAN_DIR / f"{sig}.json").write_text(json.dumps(plan, indent=2, sort_keys=True))
    (RECEIPT_DIR / f"{sig}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return plan, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decision", default=EXPECTED_DECISION_ID)
    args = parser.parse_args()

    plan, receipt = build_plan(args.decision)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"plan_json_path=data/frontier_depth_probe_fix_disposition_plans/{plan['plan_id']}.json")
    print(f"plan_receipt_path=data/frontier_depth_probe_fix_disposition_plan_receipts/{plan['plan_id']}.json")

    return 0 if plan["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
