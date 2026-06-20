#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

COMPARISON_DIR = ROOT / "data" / "repeated_slot_plan_cache_before_after_comparisons"
APPLICATION_DIR = ROOT / "data" / "repeated_slot_execution_plan_cache_fix_applications"
PROFILE_DIR = ROOT / "data" / "micro_burden_profiles"

DECISION_DIR = ROOT / "data" / "repeated_slot_plan_cache_fix_outcome_decisions"
RECEIPT_DIR = ROOT / "data" / "repeated_slot_plan_cache_fix_outcome_decision_receipts"

EXPECTED_COMPARISON_ID = "d2ecdf4b"
EXPECTED_APPLICATION_ID = "2233c46c"
EXPECTED_SOURCE_CANDIDATE_ID = "57f6e627"
EXPECTED_BEFORE_PROFILE_ID = "00a75664"
EXPECTED_AFTER_PROFILE_ID = "24ac7037"
EXPECTED_TARGET = "BURDEN_REPEATED_SLOT_WORK"

ACCEPTED_BURDEN_CLASSES = {
    "BURDEN_DB_WRITE",
    "BURDEN_REPEATED_SLOT_WORK",
}

NEXT_BURDEN_MAP = {
    "BURDEN_CYCLE_SCAN": {
        "next_command_goal": "BUILD_CYCLE_PERIOD_COMPRESSION_FIX_CANDIDATE_POLICY_V0",
        "fix_family": "CYCLE_PERIOD_COMPRESSION_POLICY",
        "authority_note": "Future-run cycle-period policy only; no halt/law/gate/run semantics change.",
    },
    "BURDEN_DEPTH_SCAN": {
        "next_command_goal": "BUILD_FRONTIER_DEPTH_PROBE_FIX_CANDIDATE_POLICY_V0",
        "fix_family": "FRONTIER_DEPTH_PROBE_POLICY",
        "authority_note": "Future-run depth frontier policy only; no current probe skipping.",
    },
    "BURDEN_RECEIPT_VOLUME": {
        "next_command_goal": "BUILD_RECEIPT_VOLUME_ROLLUP_VIEW_FIX_CANDIDATE_POLICY_V0",
        "fix_family": "RECEIPT_VOLUME_READ_SIDE_ROLLUP_VIEW",
        "authority_note": "Operator-view/read-side rollup only; raw receipts remain authoritative.",
    },
    "BURDEN_MATRIX_BUILD": {
        "next_command_goal": "BUILD_MATRIX_BUILD_FIX_CANDIDATE_POLICY_V0",
        "fix_family": "MATRIX_BUILD_INFRA_POLICY",
        "authority_note": "Matrix construction optimization proposal only; no law/gate semantics change.",
    },
    "BURDEN_LAW_CHECK": {
        "next_command_goal": "BUILD_LAW_CHECK_FIX_CANDIDATE_POLICY_V0",
        "fix_family": "LAW_CHECK_INFRA_POLICY",
        "authority_note": "Law-check implementation optimization only; no law meaning change.",
    },
    "BURDEN_GATE_OVERHEAD": {
        "next_command_goal": "BUILD_GATE_OVERHEAD_FIX_CANDIDATE_POLICY_V0",
        "fix_family": "GATE_OVERHEAD_INFRA_POLICY",
        "authority_note": "Gate implementation optimization only; no gate meaning change.",
    },
    "BURDEN_MATRIX_BOUNDARY": {
        "next_command_goal": "BUILD_MATRIX_BOUNDARY_FIX_CANDIDATE_POLICY_V0",
        "fix_family": "MATRIX_BOUNDARY_POLICY",
        "authority_note": "Boundary handling proposal only; no execution skipping.",
    },
}


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


def verify_sources(comparison: dict[str, Any], application: dict[str, Any], after_profile: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if comparison.get("comparison_id") != EXPECTED_COMPARISON_ID:
        failures.append(f"comparison_id_mismatch:{comparison.get('comparison_id')}")
    if comparison.get("comparison_id") != comparison.get("comparison_sig8"):
        failures.append("comparison_sig_mismatch")
    if comparison.get("gate") != "PASS":
        failures.append("comparison_gate_not_PASS")
    if comparison.get("source_application_id") != EXPECTED_APPLICATION_ID:
        failures.append(f"comparison_application_mismatch:{comparison.get('source_application_id')}")
    if comparison.get("source_candidate_id") != EXPECTED_SOURCE_CANDIDATE_ID:
        failures.append(f"comparison_candidate_mismatch:{comparison.get('source_candidate_id')}")
    if comparison.get("before_profile_id") != EXPECTED_BEFORE_PROFILE_ID:
        failures.append(f"comparison_before_profile_mismatch:{comparison.get('before_profile_id')}")
    if comparison.get("after_profile_id") != EXPECTED_AFTER_PROFILE_ID:
        failures.append(f"comparison_after_profile_mismatch:{comparison.get('after_profile_id')}")
    if comparison.get("target_burden_class") != EXPECTED_TARGET:
        failures.append(f"comparison_target_mismatch:{comparison.get('target_burden_class')}")
    if comparison.get("target_result") != "TARGET_BURDEN_ELAPSED_NON_WORSE":
        failures.append(f"comparison_target_result_not_accepted:{comparison.get('target_result')}")

    gate_rules = comparison.get("gate_rules") or {}
    if not gate_rules:
        failures.append("comparison_gate_rules_missing")
    else:
        for key, value in sorted(gate_rules.items()):
            if value is not True:
                failures.append(f"comparison_gate_rule_false:{key}:{value}")

    target_before = comparison.get("target_before") or {}
    target_after = comparison.get("target_after") or {}
    if target_before.get("rows") != 9:
        failures.append(f"target_before_rows_not_9:{target_before.get('rows')}")
    if target_after.get("rows") != 9:
        failures.append(f"target_after_rows_not_9:{target_after.get('rows')}")
    if target_before.get("receipts") != 270:
        failures.append(f"target_before_receipts_not_270:{target_before.get('receipts')}")
    if target_after.get("receipts") != 270:
        failures.append(f"target_after_receipts_not_270:{target_after.get('receipts')}")
    if target_before.get("slots") != target_after.get("slots"):
        failures.append("target_slots_changed")
    if (comparison.get("target_delta") or {}).get("elapsed_ms_delta", 1) > 0:
        failures.append("target_elapsed_delta_positive")

    if application.get("application_id") != EXPECTED_APPLICATION_ID:
        failures.append(f"application_id_mismatch:{application.get('application_id')}")
    if application.get("gate") != "PASS":
        failures.append("application_gate_not_PASS")
    if application.get("source_candidate_id") != EXPECTED_SOURCE_CANDIDATE_ID:
        failures.append(f"application_candidate_mismatch:{application.get('source_candidate_id')}")
    if application.get("before_profile_id") != EXPECTED_BEFORE_PROFILE_ID:
        failures.append(f"application_before_profile_mismatch:{application.get('before_profile_id')}")
    if application.get("target_burden_class") != EXPECTED_TARGET:
        failures.append(f"application_target_mismatch:{application.get('target_burden_class')}")

    app_sem = application.get("semantics") or {}
    for key in [
        "execution_skipping",
        "reusing_prior_run_results_as_execution",
        "slot_identity_collapse",
        "slot_receipt_merge",
        "receipt_deletion",
        "receipt_compression",
        "receipt_schema_change",
        "gate_semantics_change",
        "law_semantics_change",
        "halt_semantics_change",
        "run_semantics_change",
        "radius_expansion",
    ]:
        if app_sem.get(key) is not False:
            failures.append(f"application_semantics_not_preserved:{key}:{app_sem.get(key)}")

    if after_profile.get("profile_id") != EXPECTED_AFTER_PROFILE_ID:
        failures.append(f"after_profile_id_mismatch:{after_profile.get('profile_id')}")
    if after_profile.get("gate") != "MICRO_BURDEN_PROFILE_PASS":
        failures.append("after_profile_gate_not_PASS")
    if after_profile.get("profile_receipts_total") != after_profile.get("db_receipt_delta"):
        failures.append("after_profile_receipt_total_mismatch_registry")
    if after_profile.get("profile_receipts_total") != 1457:
        failures.append(f"after_profile_receipt_total_not_1457:{after_profile.get('profile_receipts_total')}")
    if after_profile.get("families_seen") != ["A", "B", "C", "D", "E"]:
        failures.append("after_family_coverage_not_A_E")
    if len(after_profile.get("rows") or []) != 25:
        failures.append(f"after_profile_rows_not_25:{len(after_profile.get('rows') or [])}")

    cache = after_profile.get("repeated_slot_execution_plan_cache") or {}
    if cache.get("status") != "APPLIED_METADATA_ONLY":
        failures.append(f"metadata_cache_status_wrong:{cache.get('status')}")
    if cache.get("cache_scope") != "within_one_micro_profile_execution_only":
        failures.append(f"metadata_cache_scope_wrong:{cache.get('cache_scope')}")
    for forbidden in [
        "run_id",
        "receipt rows",
        "receipt counts as substitutes for execution",
        "law results",
        "gate results",
        "halt results",
        "stdout/stderr from a prior run",
        "any prior execution result",
    ]:
        if forbidden not in (cache.get("does_not_cache") or []):
            failures.append(f"metadata_cache_forbidden_marker_missing:{forbidden}")

    sem = after_profile.get("semantics") or {}
    if sem.get("runner_semantics_changed") is not False:
        failures.append("after_runner_semantics_changed")
    if sem.get("gate_semantics_changed") is not False:
        failures.append("after_gate_semantics_changed")
    if sem.get("law_semantics_changed") is not False:
        failures.append("after_law_semantics_changed")
    if sem.get("receipt_rows_deleted") is not False:
        failures.append("after_receipt_rows_deleted")
    if sem.get("execution_skipped") is not False:
        failures.append("after_execution_skipped")

    return failures


def choose_next_burden(after_summary: dict[str, dict[str, Any]]) -> tuple[str | None, str, list[dict[str, Any]]]:
    candidates = []
    excluded = sorted(ACCEPTED_BURDEN_CLASSES)

    for burden_class, summary in after_summary.items():
        if burden_class in ACCEPTED_BURDEN_CLASSES:
            continue
        if burden_class == "BURDEN_UNKNOWN":
            continue
        if burden_class not in NEXT_BURDEN_MAP:
            continue

        candidates.append({
            "burden_class": burden_class,
            "elapsed_ms": int(summary.get("elapsed_ms") or 0),
            "receipts": int(summary.get("receipts") or 0),
            "rows": int(summary.get("rows") or 0),
            "receipts_per_sec": summary.get("receipts_per_sec"),
            "families": summary.get("families") or [],
            "probes": summary.get("probes") or [],
            "slots": summary.get("slots") or [],
            "next_command_goal": NEXT_BURDEN_MAP[burden_class]["next_command_goal"],
            "fix_family": NEXT_BURDEN_MAP[burden_class]["fix_family"],
            "authority_note": NEXT_BURDEN_MAP[burden_class]["authority_note"],
        })

    if not candidates:
        return None, f"NO_REMAINING_MAPPED_BURDEN_CLASS_AFTER_EXCLUDING_{'_'.join(excluded)}", []

    ranked = sorted(
        candidates,
        key=lambda r: (
            int(r["elapsed_ms"]),
            int(r["receipts"]),
            int(r["rows"]),
            str(r["burden_class"]),
        ),
        reverse=True,
    )
    return ranked[0]["burden_class"], "MAX_AFTER_ELAPSED_MS_EXCLUDING_ACCEPTED_BURDEN_CLASSES", ranked


def build_decision(comparison_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    DECISION_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    comparison = load_json(COMPARISON_DIR / f"{comparison_id}.json")
    application = load_json(APPLICATION_DIR / f"{EXPECTED_APPLICATION_ID}.json")
    after_profile = load_json(PROFILE_DIR / f"{EXPECTED_AFTER_PROFILE_ID}.json")

    failures = verify_sources(comparison, application, after_profile)
    warnings: list[str] = []

    delta = comparison.get("target_delta") or {}
    after_summary = comparison.get("after_burden_summary") or {}
    next_burden_class, selection_rule, ranked_candidates = choose_next_burden(after_summary)

    if not next_burden_class:
        warnings.append("NO_NEXT_BURDEN_CLASS_SELECTED")
        next_goal = "FREEZE_MICRO_BURDEN_LOOP_OR_DEFINE_NEW_BURDEN_CLASS_V0"
    else:
        next_goal = NEXT_BURDEN_MAP[next_burden_class]["next_command_goal"]

    if comparison.get("target_result") == "TARGET_BURDEN_ELAPSED_NON_WORSE":
        repeated_slot_outcome = "ACCEPT_REPEATED_SLOT_METADATA_PLAN_CACHE_FIX"
    else:
        repeated_slot_outcome = "REJECT_REPEATED_SLOT_METADATA_PLAN_CACHE_FIX"
        failures.append("repeated_slot_fix_target_not_accepted")

    decision = {
        "schema_version": "repeated_slot_plan_cache_fix_outcome_decision_v0",
        "decision_kind": "REPEATED_SLOT_PLAN_CACHE_FIX_OUTCOME_OR_NEXT_BURDEN_CLASS_DECISION",
        "source_comparison": {
            "comparison_id": comparison.get("comparison_id"),
            "comparison_sig8": comparison.get("comparison_sig8"),
            "gate": comparison.get("gate"),
            "path": f"data/repeated_slot_plan_cache_before_after_comparisons/{comparison_id}.json",
        },
        "source_application_id": EXPECTED_APPLICATION_ID,
        "source_candidate_id": EXPECTED_SOURCE_CANDIDATE_ID,
        "before_profile_id": EXPECTED_BEFORE_PROFILE_ID,
        "after_profile_id": EXPECTED_AFTER_PROFILE_ID,
        "target_burden_class": EXPECTED_TARGET,
        "target_result": comparison.get("target_result"),
        "repeated_slot_fix_outcome": repeated_slot_outcome,
        "target_metric_delta": delta,
        "accepted_changes": [
            "KEEP_IMMUTABLE_SLOT_EXECUTION_PLAN_OBJECT",
            "KEEP_PROCESS_LOCAL_METADATA_ONLY_PLAN_CACHE",
            "KEEP_REPEATED_SLOT_IDENTITY_GUARD",
            "KEEP_MICRO_PROFILE_RETEST_COMPARABILITY_SURFACE",
        ],
        "rejected_or_deferred_changes": [
            {
                "change_id": "CACHE_RUN_IDS_OR_EXECUTION_RESULTS",
                "status": "PERMANENTLY_FORBIDDEN",
                "reason": "Would convert metadata cache into execution/result reuse and break the receipt model.",
            },
            {
                "change_id": "COLLAPSE_REPEATED_SLOT_IDENTITY",
                "status": "PERMANENTLY_FORBIDDEN",
                "reason": "Repeated E/E/E, D/D, and B/B slots must remain distinguishable.",
            },
            {
                "change_id": "SKIP_REPEATED_SLOT_EXECUTION",
                "status": "PERMANENTLY_FORBIDDEN",
                "reason": "Policy allows metadata planning only, not execution skipping.",
            },
            {
                "change_id": "MORE_REPEATED_SLOT_PATCHING",
                "status": "NOT_AUTHORIZED_NOW",
                "reason": "Target is improved/non-worse; continue to next burden class instead of stacking patches.",
            },
        ],
        "authorization": {
            "repeated_slot_fix_accepted": repeated_slot_outcome.startswith("ACCEPT_"),
            "authorizes_more_repeated_slot_patch": False,
            "authorizes_patch_application": False,
            "authorizes_code_change": False,
            "authorizes_execution_skipping": False,
            "authorizes_reusing_prior_run_results_as_execution": False,
            "authorizes_slot_identity_collapse": False,
            "authorizes_slot_receipt_merge": False,
            "authorizes_receipt_deletion": False,
            "authorizes_receipt_compression": False,
            "authorizes_gate_semantics_change": False,
            "authorizes_law_semantics_change": False,
            "authorizes_halt_semantics_change": False,
            "authorizes_run_semantics_change": False,
            "authorizes_radius_expansion": False,
            "authorizes_next_burden_policy": bool(next_burden_class),
            "accepted_burden_classes_excluded_from_next_selection": sorted(ACCEPTED_BURDEN_CLASSES),
            "next_burden_class": next_burden_class,
        },
        "remaining_after_burden_summary": after_summary,
        "next_burden_selection": {
            "selection_rule": selection_rule,
            "excluded_burden_classes": sorted(ACCEPTED_BURDEN_CLASSES),
            "ranked_candidates": ranked_candidates,
            "selected_burden_class": next_burden_class,
            "selected_fix_family": NEXT_BURDEN_MAP[next_burden_class]["fix_family"] if next_burden_class else None,
            "selected_authority_note": NEXT_BURDEN_MAP[next_burden_class]["authority_note"] if next_burden_class else None,
        },
        "required_next_gate": {
            "next_policy_must_use_after_profile_id": EXPECTED_AFTER_PROFILE_ID,
            "next_policy_must_target_selected_burden_class": next_burden_class,
            "next_policy_must_authorize_exactly_one_fix_candidate": True,
            "next_policy_must_not_authorize_patch_application": True,
            "next_policy_must_not_authorize_radius_expansion": True,
            "next_policy_must_preserve_raw_receipts": True,
            "next_policy_must_not_reopen_accepted_classes_without_explicit_new_failure": sorted(ACCEPTED_BURDEN_CLASSES),
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": next_goal if not failures else None,
            "stop_code": None if not failures else "STOP_REPEATED_SLOT_FIX_OUTCOME_DECISION_INVALID",
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
        "schema_version": "repeated_slot_plan_cache_fix_outcome_decision_receipt_v0",
        "decision_id": sig,
        "decision_path": f"data/repeated_slot_plan_cache_fix_outcome_decisions/{sig}.json",
        "decision_sig8": sig,
        "source_comparison_id": comparison_id,
        "source_application_id": EXPECTED_APPLICATION_ID,
        "source_candidate_id": EXPECTED_SOURCE_CANDIDATE_ID,
        "before_profile_id": EXPECTED_BEFORE_PROFILE_ID,
        "after_profile_id": EXPECTED_AFTER_PROFILE_ID,
        "target_burden_class": EXPECTED_TARGET,
        "target_result": comparison.get("target_result"),
        "repeated_slot_fix_outcome": repeated_slot_outcome,
        "target_metric_delta": delta,
        "accepted_burden_classes_excluded_from_next_selection": sorted(ACCEPTED_BURDEN_CLASSES),
        "next_burden_class": next_burden_class,
        "next_burden_selection_rule": selection_rule,
        "authorizes_more_repeated_slot_patch": False,
        "authorizes_execution_skipping": False,
        "authorizes_reusing_prior_run_results_as_execution": False,
        "authorizes_slot_identity_collapse": False,
        "authorizes_radius_expansion": False,
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
    print(f"decision_json_path=data/repeated_slot_plan_cache_fix_outcome_decisions/{decision['decision_id']}.json")
    print(f"decision_receipt_path=data/repeated_slot_plan_cache_fix_outcome_decision_receipts/{decision['decision_id']}.json")

    return 0 if decision["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
