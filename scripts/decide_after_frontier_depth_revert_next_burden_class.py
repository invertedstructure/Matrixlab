#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REVERT_COMPARISON_DIR = ROOT / "data" / "frontier_depth_probe_revert_after_comparisons"
REVERT_APPLICATION_DIR = ROOT / "data" / "frontier_depth_probe_revert_applications"
PLAN_DIR = ROOT / "data" / "frontier_depth_probe_fix_disposition_plans"
FRONTIER_DECISION_DIR = ROOT / "data" / "frontier_depth_probe_fix_outcome_decisions"
PROFILE_DIR = ROOT / "data" / "micro_burden_profiles"

DECISION_DIR = ROOT / "data" / "post_frontier_depth_revert_next_burden_decisions"
RECEIPT_DIR = ROOT / "data" / "post_frontier_depth_revert_next_burden_decision_receipts"

EXPECTED_REVERT_COMPARISON_ID = "a1bd75a8"
EXPECTED_REVERT_APPLICATION_ID = "b3471a41"
EXPECTED_PLAN_ID = "ce040a69"
EXPECTED_FRONTIER_DECISION_ID = "22d0002e"
EXPECTED_AFTER_REVERT_PROFILE_ID = "b6609f93"
EXPECTED_PRE_FRONTIER_PROFILE_ID = "45cd7660"
EXPECTED_BAD_AFTER_PROFILE_ID = "26966e56"

REJECTED_BURDEN_CLASS = "BURDEN_DEPTH_SCAN"
SELECTED_NEXT_BURDEN_CLASS = "BURDEN_RECEIPT_VOLUME"

ACCEPTED_FROZEN = [
    "BURDEN_CYCLE_SCAN",
    "BURDEN_DB_WRITE",
    "BURDEN_REPEATED_SLOT_WORK",
]

EXPECTED_BURDEN_CLASSES = [
    "BURDEN_CYCLE_SCAN",
    "BURDEN_DB_WRITE",
    "BURDEN_DEPTH_SCAN",
    "BURDEN_RECEIPT_VOLUME",
    "BURDEN_REPEATED_SLOT_WORK",
]

NEXT_COMMAND_GOAL = "BUILD_RECEIPT_VOLUME_FIX_CANDIDATE_POLICY_V0"


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


def summarize_burdens(profile: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in profile.get("rows") or []:
        cls = row.get("burden_class") or "BURDEN_UNKNOWN"
        b = out.setdefault(cls, {
            "rows": 0,
            "receipts": 0,
            "elapsed_ms": 0,
            "families": set(),
            "probes": set(),
            "slots": [],
            "row_keys": [],
        })
        b["rows"] += 1
        b["receipts"] += int(row.get("receipts") or 0)
        b["elapsed_ms"] += int(row.get("elapsed_ms") or 0)
        if row.get("family_compact"):
            b["families"].add(row.get("family_compact"))
        if row.get("probe_id"):
            b["probes"].add(row.get("probe_id"))
        if row.get("slot_id"):
            b["slots"].append(row.get("slot_id"))
        b["row_keys"].append({
            "probe_id": row.get("probe_id"),
            "slot_id": row.get("slot_id"),
            "family_compact": row.get("family_compact"),
            "burden_class": row.get("burden_class"),
        })

    normalized: dict[str, dict[str, Any]] = {}
    for cls, b in out.items():
        elapsed_ms = int(b["elapsed_ms"])
        receipts = int(b["receipts"])
        normalized[cls] = {
            "rows": int(b["rows"]),
            "receipts": receipts,
            "elapsed_ms": elapsed_ms,
            "receipts_per_sec": round(receipts / (elapsed_ms / 1000.0), 6) if elapsed_ms > 0 else None,
            "families": sorted(b["families"]),
            "probes": sorted(b["probes"]),
            "slots": b["slots"],
            "row_keys": b["row_keys"],
        }
    return normalized


def verify_revert_comparison(comparison: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if comparison.get("comparison_id") != EXPECTED_REVERT_COMPARISON_ID:
        failures.append(f"revert_comparison_id_mismatch:{comparison.get('comparison_id')}")
    if comparison.get("comparison_id") != comparison.get("comparison_sig8"):
        failures.append("revert_comparison_sig_mismatch")
    if comparison.get("gate") != "PASS":
        failures.append("revert_comparison_gate_not_PASS")
    if comparison.get("failures") != []:
        failures.append(f"revert_comparison_failures_not_empty:{comparison.get('failures')}")
    if comparison.get("source_revert_application_id") != EXPECTED_REVERT_APPLICATION_ID:
        failures.append(f"revert_comparison_application_mismatch:{comparison.get('source_revert_application_id')}")
    if comparison.get("source_plan_id") != EXPECTED_PLAN_ID:
        failures.append(f"revert_comparison_plan_mismatch:{comparison.get('source_plan_id')}")
    if comparison.get("source_decision_id") != EXPECTED_FRONTIER_DECISION_ID:
        failures.append(f"revert_comparison_decision_mismatch:{comparison.get('source_decision_id')}")
    if comparison.get("pre_frontier_profile_id") != EXPECTED_PRE_FRONTIER_PROFILE_ID:
        failures.append(f"revert_comparison_pre_profile_mismatch:{comparison.get('pre_frontier_profile_id')}")
    if comparison.get("bad_after_profile_id") != EXPECTED_BAD_AFTER_PROFILE_ID:
        failures.append(f"revert_comparison_bad_after_profile_mismatch:{comparison.get('bad_after_profile_id')}")
    if comparison.get("after_revert_profile_id") != EXPECTED_AFTER_REVERT_PROFILE_ID:
        failures.append(f"revert_comparison_after_revert_profile_mismatch:{comparison.get('after_revert_profile_id')}")
    if comparison.get("target_burden_class") != REJECTED_BURDEN_CLASS:
        failures.append(f"revert_comparison_target_mismatch:{comparison.get('target_burden_class')}")
    if comparison.get("revert_metric_classification") != "REVERT_DEPTH_ELAPSED_NON_WORSE_VS_REJECTED_PATCH":
        failures.append(f"revert_metric_classification_mismatch:{comparison.get('revert_metric_classification')}")

    surface = comparison.get("profile_surface") or {}
    if surface.get("frontier_depth_probe_field_absent") is not True:
        failures.append("frontier_depth_probe_field_not_absent_after_revert")
    if surface.get("cycle_period_compression_field_present") is not True:
        failures.append("cycle_period_field_missing_after_revert")
    if surface.get("cycle_period_status") != "APPLIED_POST_EXECUTION_METADATA_ONLY":
        failures.append(f"cycle_period_status_mismatch:{surface.get('cycle_period_status')}")
    if surface.get("cycle_period_certificate_kind") != "cycle_period_observation_certificate":
        failures.append(f"cycle_period_kind_mismatch:{surface.get('cycle_period_certificate_kind')}")
    if surface.get("after_revert_profile_receipts_total") != 1457:
        failures.append(f"after_revert_total_not_1457:{surface.get('after_revert_profile_receipts_total')}")
    if surface.get("after_revert_db_receipt_delta") != 1457:
        failures.append(f"after_revert_db_delta_not_1457:{surface.get('after_revert_db_receipt_delta')}")
    if surface.get("after_revert_rows") != 25:
        failures.append(f"after_revert_rows_not_25:{surface.get('after_revert_rows')}")
    if surface.get("after_revert_families_seen") != ["A", "B", "C", "D", "E"]:
        failures.append(f"after_revert_families_wrong:{surface.get('after_revert_families_seen')}")

    rules = comparison.get("gate_rules") or {}
    for key, value in sorted(rules.items()):
        if value is not True:
            failures.append(f"revert_comparison_gate_rule_false:{key}:{value}")

    auth = comparison.get("authorization") or {}
    if auth.get("authorizes_next_burden_decision") is not True:
        failures.append("revert_comparison_does_not_authorize_next_burden_decision")
    for key in [
        "authorizes_next_burden_policy",
        "authorizes_more_frontier_depth_patching",
        "authorizes_reapplying_frontier_depth_patch",
        "authorizes_observability_freeze",
        "authorizes_receipt_deletion",
        "authorizes_data_artifact_deletion",
        "authorizes_depth_range_change",
        "authorizes_radius_expansion",
        "authorizes_halt_law_gate_run_semantics_change",
        "authorizes_reopening_accepted_burden_classes",
    ]:
        if auth.get(key) is not False:
            failures.append(f"revert_comparison_illegal_authorization:{key}:{auth.get(key)}")

    terminal = comparison.get("terminal") or {}
    if terminal.get("next_command_goal") != "DECIDE_AFTER_FRONTIER_DEPTH_REVERT_NEXT_BURDEN_CLASS_V0":
        failures.append(f"revert_comparison_terminal_mismatch:{terminal.get('next_command_goal')}")

    return failures


def verify_revert_application(app: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if app.get("revert_application_id") != EXPECTED_REVERT_APPLICATION_ID:
        failures.append(f"revert_application_id_mismatch:{app.get('revert_application_id')}")
    if app.get("gate") != "PASS":
        failures.append("revert_application_gate_not_PASS")
    if app.get("source_plan_id") != EXPECTED_PLAN_ID:
        failures.append(f"revert_application_plan_mismatch:{app.get('source_plan_id')}")
    if app.get("source_decision_id") != EXPECTED_FRONTIER_DECISION_ID:
        failures.append(f"revert_application_decision_mismatch:{app.get('source_decision_id')}")
    if app.get("source_original_application_id") != "f537dd1f":
        failures.append(f"revert_application_original_app_mismatch:{app.get('source_original_application_id')}")
    if app.get("source_comparison_id") != "ed563880":
        failures.append(f"revert_application_original_comparison_mismatch:{app.get('source_comparison_id')}")
    if app.get("selected_disposition") != "REVERT_FRONTIER_DEPTH_METADATA_CERTIFICATE_PATCH":
        failures.append(f"revert_application_disposition_mismatch:{app.get('selected_disposition')}")
    if app.get("failures") != []:
        failures.append(f"revert_application_failures_not_empty:{app.get('failures')}")

    scope = app.get("revert_scope") or {}
    if scope.get("removed_frontier_depth_patch_only") is not True:
        failures.append("revert_application_not_patch_only")
    if not all((scope.get("removed_frontier_markers") or {}).values()):
        failures.append(f"revert_application_frontier_markers_not_removed:{scope.get('removed_frontier_markers')}")
    if not all((scope.get("preserved_cycle_period_markers") or {}).values()):
        failures.append(f"revert_application_cycle_markers_not_preserved:{scope.get('preserved_cycle_period_markers')}")
    if scope.get("deleted_data_artifacts") is not False:
        failures.append("revert_application_deleted_data_artifacts")
    if scope.get("deleted_receipts") is not False:
        failures.append("revert_application_deleted_receipts")
    if scope.get("changed_depth_range") is not False:
        failures.append("revert_application_changed_depth_range")
    if scope.get("expanded_radius") is not False:
        failures.append("revert_application_expanded_radius")
    if scope.get("changed_halt_law_gate_run_semantics") is not False:
        failures.append("revert_application_changed_semantics")
    if scope.get("reopened_accepted_burden_classes") is not False:
        failures.append("revert_application_reopened_accepted_classes")

    sem = app.get("semantics") or {}
    if sem.get("revert_application") is not True:
        failures.append("revert_application_marker_missing")
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
        "data_artifact_deletion",
        "reopening_accepted_burden_classes",
    ]:
        if sem.get(key) is not False:
            failures.append(f"revert_application_semantics_not_preserved:{key}:{sem.get(key)}")

    return failures


def verify_frontier_outcome_decision(decision: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if decision.get("decision_id") != EXPECTED_FRONTIER_DECISION_ID:
        failures.append(f"frontier_decision_id_mismatch:{decision.get('decision_id')}")
    if decision.get("gate") != "PASS":
        failures.append("frontier_decision_gate_not_PASS")
    if decision.get("target_burden_class") != REJECTED_BURDEN_CLASS:
        failures.append(f"frontier_decision_target_mismatch:{decision.get('target_burden_class')}")
    if decision.get("frontier_depth_fix_outcome") != "REJECT_FRONTIER_DEPTH_PROBE_FIX_AS_BURDEN_FIX":
        failures.append(f"frontier_decision_outcome_mismatch:{decision.get('frontier_depth_fix_outcome')}")
    if decision.get("accepted_as_burden_fix") is not False:
        failures.append("frontier_decision_accepted_as_burden_fix")
    if decision.get("accepted_as_observability_only") is not False:
        failures.append("frontier_decision_accepted_as_observability_only")

    auth = decision.get("authorization") or {}
    if auth.get("authorizes_next_burden_policy") is not False:
        failures.append("frontier_decision_illegally_authorizes_next_burden_policy")
    if auth.get("authorizes_more_frontier_depth_patching") is not False:
        failures.append("frontier_decision_illegally_authorizes_more_frontier_depth_patching")
    if auth.get("authorizes_accepting_frontier_depth_as_burden_fix") is not False:
        failures.append("frontier_decision_illegally_authorizes_acceptance")

    return failures


def verify_after_revert_profile(profile: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if profile.get("profile_id") != EXPECTED_AFTER_REVERT_PROFILE_ID:
        failures.append(f"after_revert_profile_id_mismatch:{profile.get('profile_id')}")
    if profile.get("gate") != "MICRO_BURDEN_PROFILE_PASS":
        failures.append("after_revert_profile_gate_not_PASS")
    if profile.get("failures") != []:
        failures.append(f"after_revert_profile_failures_not_empty:{profile.get('failures')}")
    if len(profile.get("rows") or []) != 25:
        failures.append(f"after_revert_profile_rows_not_25:{len(profile.get('rows') or [])}")
    if profile.get("families_seen") != ["A", "B", "C", "D", "E"]:
        failures.append(f"after_revert_profile_families_wrong:{profile.get('families_seen')}")
    if profile.get("profile_receipts_total") != 1457:
        failures.append(f"after_revert_profile_total_not_1457:{profile.get('profile_receipts_total')}")
    if profile.get("profile_receipts_total") != profile.get("db_receipt_delta"):
        failures.append("after_revert_profile_receipts_mismatch_registry")
    if profile.get("non_unknown_burden_classes") != EXPECTED_BURDEN_CLASSES:
        failures.append(f"after_revert_burden_classes_wrong:{profile.get('non_unknown_burden_classes')}")
    if "frontier_depth_probe" in profile:
        failures.append("frontier_depth_probe_field_present_after_revert")
    if "cycle_period_compression" not in profile:
        failures.append("cycle_period_compression_missing_after_revert")

    sem = profile.get("semantics") or {}
    for key in [
        "execution_skipped",
        "runner_semantics_changed",
        "gate_semantics_changed",
        "law_semantics_changed",
        "receipt_rows_deleted",
        "receipts_compressed",
    ]:
        if sem.get(key) is not False:
            failures.append(f"after_revert_profile_semantics_not_preserved:{key}:{sem.get(key)}")
    if sem.get("passive_observability_layer") is not True:
        failures.append("after_revert_passive_observability_missing")

    return failures


def select_next_burden(profile: dict[str, Any]) -> tuple[str | None, list[str], dict[str, Any], dict[str, Any]]:
    summary = summarize_burdens(profile)

    rejected = [REJECTED_BURDEN_CLASS]
    accepted = list(ACCEPTED_FROZEN)

    eligible = [
        cls for cls in profile.get("non_unknown_burden_classes") or []
        if cls not in accepted
        and cls not in rejected
        and cls != "BURDEN_UNKNOWN"
    ]

    if SELECTED_NEXT_BURDEN_CLASS not in eligible:
        return None, eligible, summary, {}

    return SELECTED_NEXT_BURDEN_CLASS, eligible, summary, summary.get(SELECTED_NEXT_BURDEN_CLASS) or {}


def build_decision(revert_comparison_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    DECISION_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    revert_comparison = load_json(REVERT_COMPARISON_DIR / f"{revert_comparison_id}.json")
    revert_application = load_json(REVERT_APPLICATION_DIR / f"{EXPECTED_REVERT_APPLICATION_ID}.json")
    plan = load_json(PLAN_DIR / f"{EXPECTED_PLAN_ID}.json")
    frontier_decision = load_json(FRONTIER_DECISION_DIR / f"{EXPECTED_FRONTIER_DECISION_ID}.json")
    after_revert_profile = load_json(PROFILE_DIR / f"{EXPECTED_AFTER_REVERT_PROFILE_ID}.json")

    failures: list[str] = []
    failures.extend(verify_revert_comparison(revert_comparison))
    failures.extend(verify_revert_application(revert_application))
    failures.extend(verify_frontier_outcome_decision(frontier_decision))
    failures.extend(verify_after_revert_profile(after_revert_profile))

    selected, eligible, burden_summary, selected_evidence = select_next_burden(after_revert_profile)
    if selected != SELECTED_NEXT_BURDEN_CLASS:
        failures.append(f"selected_next_burden_mismatch:{selected};eligible={eligible}")

    if selected_evidence.get("rows") != 1:
        failures.append(f"receipt_volume_rows_not_1:{selected_evidence.get('rows')}")
    if int(selected_evidence.get("receipts") or 0) <= 0:
        failures.append(f"receipt_volume_receipts_not_positive:{selected_evidence.get('receipts')}")
    if int(selected_evidence.get("elapsed_ms") or 0) <= 0:
        failures.append(f"receipt_volume_elapsed_not_positive:{selected_evidence.get('elapsed_ms')}")

    warnings = list(revert_comparison.get("warnings") or [])

    decision = {
        "schema_version": "post_frontier_depth_revert_next_burden_decision_v0",
        "decision_kind": "DECIDE_AFTER_FRONTIER_DEPTH_REVERT_NEXT_BURDEN_CLASS",
        "source_revert_comparison_id": EXPECTED_REVERT_COMPARISON_ID,
        "source_revert_application_id": EXPECTED_REVERT_APPLICATION_ID,
        "source_disposition_plan_id": EXPECTED_PLAN_ID,
        "source_frontier_depth_outcome_decision_id": EXPECTED_FRONTIER_DECISION_ID,
        "after_revert_profile_id": EXPECTED_AFTER_REVERT_PROFILE_ID,
        "pre_frontier_profile_id": EXPECTED_PRE_FRONTIER_PROFILE_ID,
        "bad_after_profile_id": EXPECTED_BAD_AFTER_PROFILE_ID,
        "profile_gate": after_revert_profile.get("gate"),
        "profile_receipts_total": after_revert_profile.get("profile_receipts_total"),
        "db_receipt_delta": after_revert_profile.get("db_receipt_delta"),
        "profile_rows": len(after_revert_profile.get("rows") or []),
        "families_seen": after_revert_profile.get("families_seen"),
        "accepted_burden_classes_frozen": ACCEPTED_FROZEN,
        "rejected_or_deferred_burden_classes": [
            {
                "burden_class": REJECTED_BURDEN_CLASS,
                "disposition": "REJECTED_AS_BURDEN_FIX_AND_REVERTED",
                "source_decision_id": EXPECTED_FRONTIER_DECISION_ID,
                "source_revert_comparison_id": EXPECTED_REVERT_COMPARISON_ID,
                "reopen_allowed": False,
                "reason": "frontier-depth patch was structurally safe but performance-negative, then reverted and confirmed clean",
            }
        ],
        "all_non_unknown_burden_classes": after_revert_profile.get("non_unknown_burden_classes"),
        "eligible_unresolved_burden_classes": eligible,
        "selected_next_burden_class": selected,
        "selected_next_burden_evidence": selected_evidence,
        "burden_summary": burden_summary,
        "selection_reason": {
            "frontier_depth_revert_confirmed": True,
            "frontier_depth_probe_field_absent": "frontier_depth_probe" not in after_revert_profile,
            "cycle_period_compression_field_present": "cycle_period_compression" in after_revert_profile,
            "accepted_classes_not_reopened": ACCEPTED_FROZEN,
            "rejected_depth_not_reopened": True,
            "only_remaining_eligible_non_unknown_burden": eligible == [SELECTED_NEXT_BURDEN_CLASS],
        },
        "authorization": {
            "authorizes_next_burden_policy": True,
            "authorized_next_command_goal": NEXT_COMMAND_GOAL,
            "authorized_target_burden_class": SELECTED_NEXT_BURDEN_CLASS,
            "authorizes_patch_application": False,
            "authorizes_code_change_now": False,
            "authorizes_reopening_accepted_burden_classes": False,
            "authorizes_reopening_frontier_depth": False,
            "authorizes_more_frontier_depth_patching": False,
            "authorizes_reapplying_frontier_depth_patch": False,
            "authorizes_observability_freeze": False,
            "authorizes_receipt_deletion": False,
            "authorizes_receipt_compression": False,
            "authorizes_data_artifact_deletion": False,
            "authorizes_execution_skipping": False,
            "authorizes_depth_probe_skipping": False,
            "authorizes_frontier_case_skipping": False,
            "authorizes_synthetic_receipts": False,
            "authorizes_depth_range_change": False,
            "authorizes_radius_expansion": False,
            "authorizes_halt_semantics_change": False,
            "authorizes_law_semantics_change": False,
            "authorizes_gate_semantics_change": False,
            "authorizes_run_semantics_change": False,
        },
        "required_next_gate": {
            "next_command_goal": NEXT_COMMAND_GOAL,
            "must_target_burden_class": SELECTED_NEXT_BURDEN_CLASS,
            "must_use_decision_id": None,
            "must_use_after_revert_profile_id": EXPECTED_AFTER_REVERT_PROFILE_ID,
            "must_preserve_accepted_burden_classes": ACCEPTED_FROZEN,
            "must_not_reopen_rejected_depth_scan": True,
            "must_not_delete_receipts": True,
            "must_not_delete_data_artifacts": True,
            "must_not_change_halt_law_gate_run_semantics": True,
            "must_not_change_depth_range": True,
            "must_not_expand_radius": True,
            "policy_only_no_patch_application": True,
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_POST_FRONTIER_DEPTH_REVERT_NEXT_BURDEN_DECISION_INVALID",
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "PASS" if not failures else "FAIL",
        "created_at": now_iso(),
    }

    sig = stable_sig(decision)
    decision["decision_id"] = sig
    decision["decision_sig8"] = sig
    decision["required_next_gate"]["must_use_decision_id"] = sig

    receipt = {
        "schema_version": "post_frontier_depth_revert_next_burden_decision_receipt_v0",
        "decision_id": sig,
        "decision_path": f"data/post_frontier_depth_revert_next_burden_decisions/{sig}.json",
        "decision_sig8": sig,
        "source_revert_comparison_id": EXPECTED_REVERT_COMPARISON_ID,
        "source_revert_application_id": EXPECTED_REVERT_APPLICATION_ID,
        "source_disposition_plan_id": EXPECTED_PLAN_ID,
        "source_frontier_depth_outcome_decision_id": EXPECTED_FRONTIER_DECISION_ID,
        "after_revert_profile_id": EXPECTED_AFTER_REVERT_PROFILE_ID,
        "accepted_burden_classes_frozen": ACCEPTED_FROZEN,
        "rejected_or_deferred_burden_classes": [REJECTED_BURDEN_CLASS],
        "eligible_unresolved_burden_classes": eligible,
        "selected_next_burden_class": selected,
        "selected_next_burden_evidence": selected_evidence,
        "authorizes_next_burden_policy": True,
        "authorized_next_command_goal": NEXT_COMMAND_GOAL,
        "gate": decision["gate"],
        "terminal": decision["terminal"],
        "failures": failures,
        "warnings": warnings,
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
    parser.add_argument("--revert-comparison", default=EXPECTED_REVERT_COMPARISON_ID)
    args = parser.parse_args()

    decision, receipt = build_decision(args.revert_comparison)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"decision_json_path=data/post_frontier_depth_revert_next_burden_decisions/{decision['decision_id']}.json")
    print(f"decision_receipt_path=data/post_frontier_depth_revert_next_burden_decision_receipts/{decision['decision_id']}.json")

    return 0 if decision["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
