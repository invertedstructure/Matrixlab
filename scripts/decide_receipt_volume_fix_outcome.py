#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

COMPARISON_DIR = ROOT / "data" / "receipt_volume_before_after_comparisons"
APPLICATION_DIR = ROOT / "data" / "receipt_volume_fix_applications"
CANDIDATE_DIR = ROOT / "data" / "receipt_volume_fix_candidates"
POLICY_DIR = ROOT / "data" / "receipt_volume_fix_candidate_policies"
PROFILE_DIR = ROOT / "data" / "micro_burden_profiles"

DECISION_DIR = ROOT / "data" / "receipt_volume_fix_outcome_decisions"
RECEIPT_DIR = ROOT / "data" / "receipt_volume_fix_outcome_decision_receipts"

EXPECTED_COMPARISON_ID = "5ebbb28a"
EXPECTED_APPLICATION_ID = "2de50de2"
EXPECTED_CANDIDATE_ID = "17e6ee4e"
EXPECTED_POLICY_ID = "2e6aa9d6"
EXPECTED_BEFORE_PROFILE_ID = "b6609f93"
EXPECTED_AFTER_PROFILE_ID = "129e07a7"
TARGET_BURDEN_CLASS = "BURDEN_RECEIPT_VOLUME"

EXPECTED_TARGET_RESULT = "TARGET_BURDEN_ELAPSED_WORSE_EXPLICIT_FAILURE_CLASSIFICATION"

ACCEPTED_FROZEN = [
    "BURDEN_CYCLE_SCAN",
    "BURDEN_DB_WRITE",
    "BURDEN_REPEATED_SLOT_WORK",
]

REJECTED_OR_DEFERRED = [
    "BURDEN_DEPTH_SCAN",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_sig(obj: dict[str, Any]) -> str:
    body = dict(obj)
    for key in ("decision_id", "decision_sig8", "receipt_id", "receipt_sig8"):
        body.pop(key, None)
    return hashlib.sha256(json.dumps(body, sort_keys=True, default=str).encode()).hexdigest()[:8]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def verify_comparison(comparison: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if comparison.get("comparison_id") != EXPECTED_COMPARISON_ID:
        failures.append(f"comparison_id_mismatch:{comparison.get('comparison_id')}")
    if comparison.get("comparison_sig8") != EXPECTED_COMPARISON_ID:
        failures.append(f"comparison_sig_mismatch:{comparison.get('comparison_sig8')}")
    if comparison.get("gate") != "PASS":
        failures.append("comparison_gate_not_PASS")
    if comparison.get("failures") != []:
        failures.append(f"comparison_failures_not_empty:{comparison.get('failures')}")
    if comparison.get("source_application_id") != EXPECTED_APPLICATION_ID:
        failures.append(f"comparison_application_mismatch:{comparison.get('source_application_id')}")
    if comparison.get("source_candidate_id") != EXPECTED_CANDIDATE_ID:
        failures.append(f"comparison_candidate_mismatch:{comparison.get('source_candidate_id')}")
    if comparison.get("source_policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"comparison_policy_mismatch:{comparison.get('source_policy_id')}")
    if comparison.get("before_profile_id") != EXPECTED_BEFORE_PROFILE_ID:
        failures.append(f"comparison_before_profile_mismatch:{comparison.get('before_profile_id')}")
    if comparison.get("after_profile_id") != EXPECTED_AFTER_PROFILE_ID:
        failures.append(f"comparison_after_profile_mismatch:{comparison.get('after_profile_id')}")
    if comparison.get("target_burden_class") != TARGET_BURDEN_CLASS:
        failures.append(f"comparison_target_mismatch:{comparison.get('target_burden_class')}")
    if comparison.get("target_result") != EXPECTED_TARGET_RESULT:
        failures.append(f"comparison_target_result_unexpected:{comparison.get('target_result')}")

    delta = comparison.get("target_delta") or {}
    if delta.get("before_elapsed_ms") != 1005:
        failures.append(f"before_elapsed_unexpected:{delta.get('before_elapsed_ms')}")
    if delta.get("after_elapsed_ms") != 1012:
        failures.append(f"after_elapsed_unexpected:{delta.get('after_elapsed_ms')}")
    if delta.get("elapsed_ms_delta") != 7:
        failures.append(f"elapsed_delta_unexpected:{delta.get('elapsed_ms_delta')}")
    if delta.get("speedup_before_over_after") >= 1:
        failures.append(f"speedup_should_be_negative:{delta.get('speedup_before_over_after')}")

    before_target = comparison.get("before_target") or {}
    after_target = comparison.get("after_target") or {}
    if before_target.get("receipts") != 176:
        failures.append(f"before_target_receipts_wrong:{before_target.get('receipts')}")
    if after_target.get("receipts") != 176:
        failures.append(f"after_target_receipts_wrong:{after_target.get('receipts')}")
    if before_target.get("row_keys") != after_target.get("row_keys"):
        failures.append("target_row_keys_not_preserved")
    if before_target.get("slots") != ["MICRO_05_RECEIPT_WRITE_PRESSURE_E"]:
        failures.append(f"before_target_slot_wrong:{before_target.get('slots')}")
    if after_target.get("slots") != ["MICRO_05_RECEIPT_WRITE_PRESSURE_E"]:
        failures.append(f"after_target_slot_wrong:{after_target.get('slots')}")

    surface = comparison.get("profile_surface") or {}
    if surface.get("before_profile_receipts_total") != 1457:
        failures.append(f"before_profile_total_wrong:{surface.get('before_profile_receipts_total')}")
    if surface.get("after_profile_receipts_total") != 1457:
        failures.append(f"after_profile_total_wrong:{surface.get('after_profile_receipts_total')}")
    if surface.get("after_db_receipt_delta") != 1457:
        failures.append(f"after_db_delta_wrong:{surface.get('after_db_receipt_delta')}")
    if surface.get("frontier_depth_probe_absent_after") is not True:
        failures.append("frontier_depth_probe_not_absent_after")
    if surface.get("cycle_period_compression_present_after") is not True:
        failures.append("cycle_period_missing_after")
    if surface.get("receipt_volume_write_pressure_present_after") is not True:
        failures.append("receipt_volume_certificate_missing_after")

    cert = comparison.get("receipt_volume_certificate") or {}
    if cert.get("certificate_kind") != "receipt_volume_write_pressure_accounting_certificate":
        failures.append(f"receipt_volume_cert_kind_wrong:{cert.get('certificate_kind')}")
    if cert.get("target_receipts_preserved") is not True:
        failures.append("receipt_volume_cert_receipts_not_preserved")
    if cert.get("target_row_identity_preserved") is not True:
        failures.append("receipt_volume_cert_identity_not_preserved")
    if cert.get("expected_profile_receipts_total") != 1457:
        failures.append(f"receipt_volume_cert_total_wrong:{cert.get('expected_profile_receipts_total')}")

    rules = comparison.get("gate_rules") or {}
    for key, value in sorted(rules.items()):
        if value is not True:
            failures.append(f"comparison_gate_rule_false:{key}:{value}")

    auth = comparison.get("authorization") or {}
    if auth.get("authorizes_outcome_decision_next") is not True:
        failures.append("comparison_does_not_authorize_outcome_decision")
    if auth.get("authorized_next_command_goal") != "DECIDE_RECEIPT_VOLUME_FIX_OUTCOME_OR_NEXT_STEP_V0":
        failures.append(f"comparison_next_goal_wrong:{auth.get('authorized_next_command_goal')}")
    for key in [
        "authorizes_acceptance_now",
        "authorizes_revert_now",
        "authorizes_next_burden_policy_now",
        "authorizes_more_receipt_volume_patching",
        "authorizes_receipt_deletion",
        "authorizes_receipt_compression",
        "authorizes_raw_receipt_write_suppression",
        "authorizes_synthetic_receipts",
        "authorizes_execution_skipping",
        "authorizes_registry_sqlite_total_mismatch",
        "authorizes_depth_range_change",
        "authorizes_radius_expansion",
        "authorizes_halt_law_gate_run_semantics_change",
        "authorizes_frontier_depth_reopening",
        "authorizes_accepted_class_reopening",
    ]:
        if auth.get(key) is not False:
            failures.append(f"comparison_illegal_authorization:{key}:{auth.get(key)}")

    return failures


def verify_application(app: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if app.get("application_id") != EXPECTED_APPLICATION_ID:
        failures.append(f"application_id_mismatch:{app.get('application_id')}")
    if app.get("gate") != "PASS":
        failures.append("application_gate_not_PASS")
    if app.get("source_candidate_id") != EXPECTED_CANDIDATE_ID:
        failures.append(f"application_candidate_mismatch:{app.get('source_candidate_id')}")
    if app.get("source_policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"application_policy_mismatch:{app.get('source_policy_id')}")
    if app.get("source_before_profile_id") != EXPECTED_BEFORE_PROFILE_ID:
        failures.append(f"application_before_profile_mismatch:{app.get('source_before_profile_id')}")
    if app.get("target_burden_class") != TARGET_BURDEN_CLASS:
        failures.append(f"application_target_mismatch:{app.get('target_burden_class')}")
    if app.get("failures") != []:
        failures.append(f"application_failures_not_empty:{app.get('failures')}")

    sem = app.get("semantics") or {}
    for key in [
        "execution_skipping",
        "probe_skipping",
        "receipt_write_pressure_skipping",
        "receipt_deletion",
        "receipt_compression",
        "raw_receipt_write_suppression",
        "synthetic_receipts",
        "registry_sqlite_total_mismatch",
        "receipt_schema_change",
        "depth_range_change",
        "radius_expansion",
        "halt_semantics_change",
        "law_semantics_change",
        "gate_semantics_change",
        "run_semantics_change",
        "frontier_depth_reopened",
        "accepted_burden_classes_reopened",
        "data_artifact_deletion",
    ]:
        if sem.get(key) is not False:
            failures.append(f"application_semantic_guard_failed:{key}:{sem.get(key)}")

    if sem.get("patch_application") is not True:
        failures.append("application_patch_marker_missing")
    if sem.get("metadata_only_observation") is not True:
        failures.append("application_metadata_only_marker_missing")

    return failures


def verify_profiles(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    for label, profile, expected_id in [
        ("before", before, EXPECTED_BEFORE_PROFILE_ID),
        ("after", after, EXPECTED_AFTER_PROFILE_ID),
    ]:
        if profile.get("profile_id") != expected_id:
            failures.append(f"{label}_profile_id_mismatch:{profile.get('profile_id')}")
        if profile.get("gate") != "MICRO_BURDEN_PROFILE_PASS":
            failures.append(f"{label}_profile_gate_not_PASS")
        if profile.get("profile_receipts_total") != 1457:
            failures.append(f"{label}_profile_total_not_1457:{profile.get('profile_receipts_total')}")
        if profile.get("db_receipt_delta") != 1457:
            failures.append(f"{label}_db_delta_not_1457:{profile.get('db_receipt_delta')}")
        if profile.get("profile_receipts_total") != profile.get("db_receipt_delta"):
            failures.append(f"{label}_profile_total_registry_mismatch")
        if "frontier_depth_probe" in profile:
            failures.append(f"{label}_frontier_depth_probe_present")
        if "cycle_period_compression" not in profile:
            failures.append(f"{label}_cycle_period_missing")
        if profile.get("failures") != []:
            failures.append(f"{label}_profile_failures_not_empty:{profile.get('failures')}")

    if "receipt_volume_write_pressure" not in after:
        failures.append("after_receipt_volume_certificate_missing")
    if "receipt_volume_write_pressure" in before:
        failures.append("before_receipt_volume_certificate_unexpected")

    return failures


def build_decision(comparison_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    DECISION_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    comparison = load_json(COMPARISON_DIR / f"{comparison_id}.json")
    application = load_json(APPLICATION_DIR / f"{EXPECTED_APPLICATION_ID}.json")
    candidate = load_json(CANDIDATE_DIR / f"{EXPECTED_CANDIDATE_ID}.json")
    policy = load_json(POLICY_DIR / f"{EXPECTED_POLICY_ID}.json")
    before = load_json(PROFILE_DIR / f"{EXPECTED_BEFORE_PROFILE_ID}.json")
    after = load_json(PROFILE_DIR / f"{EXPECTED_AFTER_PROFILE_ID}.json")

    failures: list[str] = []
    failures.extend(verify_comparison(comparison))
    failures.extend(verify_application(application))
    failures.extend(verify_profiles(before, after))

    if candidate.get("gate") != "PASS":
        failures.append("candidate_gate_not_PASS")
    if candidate.get("candidate_id") != EXPECTED_CANDIDATE_ID:
        failures.append(f"candidate_id_mismatch:{candidate.get('candidate_id')}")
    if policy.get("gate") != "PASS":
        failures.append("policy_gate_not_PASS")
    if policy.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"policy_id_mismatch:{policy.get('policy_id')}")

    delta = comparison.get("target_delta") or {}
    warnings = list(comparison.get("warnings") or [])

    decision = {
        "schema_version": "receipt_volume_fix_outcome_decision_v0",
        "decision_kind": "DECIDE_RECEIPT_VOLUME_FIX_OUTCOME_OR_NEXT_STEP",
        "source_comparison_id": EXPECTED_COMPARISON_ID,
        "source_application_id": EXPECTED_APPLICATION_ID,
        "source_candidate_id": EXPECTED_CANDIDATE_ID,
        "source_policy_id": EXPECTED_POLICY_ID,
        "before_profile_id": EXPECTED_BEFORE_PROFILE_ID,
        "after_profile_id": EXPECTED_AFTER_PROFILE_ID,
        "target_burden_class": TARGET_BURDEN_CLASS,
        "target_result": comparison.get("target_result"),
        "target_delta": delta,
        "outcome": "REJECT_RECEIPT_VOLUME_FIX_AS_BURDEN_FIX",
        "accepted_as_burden_fix": False,
        "accepted_as_receipt_volume_fix": False,
        "structurally_safe_observability_patch": True,
        "accepted_as_observability_only": False,
        "cycle_status": "HALT_AFTER_DECISION_FOR_DIRECTION_REVIEW",
        "outcome_reason": {
            "target_receipts_preserved": True,
            "profile_receipt_total_preserved": True,
            "registry_sqlite_total_preserved": True,
            "target_row_identity_preserved": True,
            "receipt_volume_certificate_present": True,
            "frontier_depth_remained_closed": True,
            "accepted_classes_remained_frozen": True,
            "performance_result": "NEGATIVE",
            "before_elapsed_ms": delta.get("before_elapsed_ms"),
            "after_elapsed_ms": delta.get("after_elapsed_ms"),
            "elapsed_ms_delta": delta.get("elapsed_ms_delta"),
            "speedup_before_over_after": delta.get("speedup_before_over_after"),
            "reason": "The patch preserved all structural and receipt guards, but worsened target elapsed time and therefore cannot be accepted as a burden fix.",
        },
        "closed_burden_cycle_state": {
            "accepted_burden_classes_frozen": ACCEPTED_FROZEN,
            "rejected_or_deferred_burden_classes": REJECTED_OR_DEFERRED,
            "receipt_volume_disposition": "REJECTED_AS_BURDEN_FIX_AFTER_SAFE_APPLICATION_AND_RETEST",
            "receipt_volume_reopen_allowed": False,
            "frontier_depth_reopen_allowed": False,
            "accepted_class_reopen_allowed": False,
        },
        "authorization": {
            "authorizes_next_command": False,
            "authorized_next_command_goal": None,
            "authorizes_acceptance_as_burden_fix": False,
            "authorizes_acceptance_as_receipt_volume_fix": False,
            "authorizes_observability_freeze": False,
            "authorizes_revert_now": False,
            "authorizes_next_burden_policy_now": False,
            "authorizes_more_receipt_volume_patching": False,
            "authorizes_more_frontier_depth_patching": False,
            "authorizes_reopening_receipt_volume": False,
            "authorizes_reopening_frontier_depth": False,
            "authorizes_reopening_accepted_burden_classes": False,
            "authorizes_receipt_deletion": False,
            "authorizes_receipt_compression": False,
            "authorizes_raw_receipt_write_suppression": False,
            "authorizes_synthetic_receipts": False,
            "authorizes_execution_skipping": False,
            "authorizes_registry_sqlite_total_mismatch": False,
            "authorizes_depth_range_change": False,
            "authorizes_radius_expansion": False,
            "authorizes_halt_law_gate_run_semantics_change": False,
        },
        "direction_review_packet": {
            "why_halted": "All current burden classes have been accepted, rejected, or exhausted; receipt volume did not yield a burden win under safe guards.",
            "open_direction_questions": [
                "Do we stop optimizing receipt burden and move toward stable delta signatures?",
                "Do we design a new burden model that distinguishes receipt count from write-path overhead?",
                "Do we revert observability-only patches that do not improve burden before choosing a new direction?",
                "Do we move from micro burden classes to distinguishability-per-burden experiments?"
            ],
            "last_clean_state": {
                "before_receipt_volume_patch_profile_id": EXPECTED_BEFORE_PROFILE_ID,
                "after_receipt_volume_patch_profile_id": EXPECTED_AFTER_PROFILE_ID,
                "receipt_volume_comparison_id": EXPECTED_COMPARISON_ID,
            },
        },
        "terminal": {
            "type": "HALT",
            "next_command_goal": None,
            "halt_code": "HALT_DIRECTION_REVIEW_AFTER_RECEIPT_VOLUME_DECISION",
            "stop_code": None,
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
        "schema_version": "receipt_volume_fix_outcome_decision_receipt_v0",
        "decision_id": sig,
        "decision_path": f"data/receipt_volume_fix_outcome_decisions/{sig}.json",
        "decision_sig8": sig,
        "source_comparison_id": EXPECTED_COMPARISON_ID,
        "source_application_id": EXPECTED_APPLICATION_ID,
        "source_candidate_id": EXPECTED_CANDIDATE_ID,
        "source_policy_id": EXPECTED_POLICY_ID,
        "before_profile_id": EXPECTED_BEFORE_PROFILE_ID,
        "after_profile_id": EXPECTED_AFTER_PROFILE_ID,
        "target_burden_class": TARGET_BURDEN_CLASS,
        "target_result": comparison.get("target_result"),
        "target_delta": delta,
        "outcome": decision["outcome"],
        "accepted_as_burden_fix": False,
        "accepted_as_receipt_volume_fix": False,
        "structurally_safe_observability_patch": True,
        "accepted_as_observability_only": False,
        "cycle_status": decision["cycle_status"],
        "authorizes_next_command": False,
        "terminal": decision["terminal"],
        "failures": failures,
        "warnings": warnings,
        "gate": decision["gate"],
        "created_at": now_iso(),
    }

    rsig = stable_sig(receipt)
    receipt["receipt_id"] = rsig
    receipt["receipt_sig8"] = rsig

    (DECISION_DIR / f"{sig}.json").write_text(json.dumps(decision, indent=2, sort_keys=True))
    (RECEIPT_DIR / f"{sig}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return decision, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--comparison", default=EXPECTED_COMPARISON_ID)
    args = parser.parse_args()

    decision, receipt = build_decision(args.comparison)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"decision_json_path=data/receipt_volume_fix_outcome_decisions/{decision['decision_id']}.json")
    print(f"decision_receipt_path=data/receipt_volume_fix_outcome_decision_receipts/{decision['decision_id']}.json")

    return 0 if decision["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
