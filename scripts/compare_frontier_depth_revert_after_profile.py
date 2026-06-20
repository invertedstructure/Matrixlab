#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

PROFILE_DIR = ROOT / "data" / "micro_burden_profiles"
REVERT_APPLICATION_DIR = ROOT / "data" / "frontier_depth_probe_revert_applications"
PLAN_DIR = ROOT / "data" / "frontier_depth_probe_fix_disposition_plans"

COMPARISON_DIR = ROOT / "data" / "frontier_depth_probe_revert_after_comparisons"
RECEIPT_DIR = ROOT / "data" / "frontier_depth_probe_revert_after_comparison_receipts"

EXPECTED_REVERT_APPLICATION_ID = "b3471a41"
EXPECTED_PLAN_ID = "ce040a69"
EXPECTED_DECISION_ID = "22d0002e"
EXPECTED_ORIGINAL_APPLICATION_ID = "f537dd1f"
EXPECTED_ORIGINAL_COMPARISON_ID = "ed563880"
EXPECTED_PRE_FRONTIER_PROFILE_ID = "45cd7660"
EXPECTED_BAD_AFTER_PROFILE_ID = "26966e56"
EXPECTED_TARGET = "BURDEN_DEPTH_SCAN"

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


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_sig(obj: dict[str, Any]) -> str:
    body = dict(obj)
    for key in ("comparison_id", "comparison_sig8", "receipt_id", "receipt_sig8"):
        body.pop(key, None)
    blob = json.dumps(body, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:8]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def target_summary(profile: dict[str, Any]) -> dict[str, Any]:
    rows = [
        row for row in (profile.get("rows") or [])
        if row.get("burden_class") == EXPECTED_TARGET
    ]
    receipts = sum(int(row.get("receipts") or 0) for row in rows)
    elapsed_ms = sum(int(row.get("elapsed_ms") or 0) for row in rows)
    return {
        "burden_class": EXPECTED_TARGET,
        "rows": len(rows),
        "receipts": receipts,
        "elapsed_ms": elapsed_ms,
        "receipts_per_sec": round(receipts / (elapsed_ms / 1000.0), 6) if elapsed_ms > 0 else None,
        "families": sorted({row.get("family_compact") for row in rows if row.get("family_compact")}),
        "probes": sorted({row.get("probe_id") for row in rows if row.get("probe_id")}),
        "slots": [row.get("slot_id") for row in rows if row.get("slot_id")],
        "row_keys": [
            {
                "probe_id": row.get("probe_id"),
                "slot_id": row.get("slot_id"),
                "family_compact": row.get("family_compact"),
                "burden_class": row.get("burden_class"),
            }
            for row in rows
        ],
    }


def verify_profile_surface(profile: dict[str, Any], after_revert_id: str) -> list[str]:
    failures: list[str] = []

    if profile.get("profile_id") != after_revert_id:
        failures.append(f"after_revert_profile_id_mismatch:{profile.get('profile_id')}")
    if profile.get("gate") != "MICRO_BURDEN_PROFILE_PASS":
        failures.append("after_revert_profile_gate_not_PASS")
    if len(profile.get("rows") or []) != 25:
        failures.append(f"after_revert_rows_not_25:{len(profile.get('rows') or [])}")
    if profile.get("families_seen") != ["A", "B", "C", "D", "E"]:
        failures.append(f"after_revert_family_coverage_wrong:{profile.get('families_seen')}")
    if profile.get("profile_receipts_total") != 1457:
        failures.append(f"after_revert_profile_total_not_1457:{profile.get('profile_receipts_total')}")
    if profile.get("profile_receipts_total") != profile.get("db_receipt_delta"):
        failures.append("after_revert_receipt_total_mismatch_registry")
    if profile.get("failures") != []:
        failures.append(f"after_revert_profile_failures_not_empty:{profile.get('failures')}")
    if profile.get("non_unknown_burden_classes") != [
        "BURDEN_CYCLE_SCAN",
        "BURDEN_DB_WRITE",
        "BURDEN_DEPTH_SCAN",
        "BURDEN_RECEIPT_VOLUME",
        "BURDEN_REPEATED_SLOT_WORK",
    ]:
        failures.append(f"after_revert_burden_classes_wrong:{profile.get('non_unknown_burden_classes')}")

    if "frontier_depth_probe" in profile:
        failures.append("frontier_depth_probe_field_still_present_after_revert")
    if "cycle_period_compression" not in profile:
        failures.append("cycle_period_compression_missing_after_revert")

    cycle = profile.get("cycle_period_compression") or {}
    if cycle.get("status") != "APPLIED_POST_EXECUTION_METADATA_ONLY":
        failures.append(f"cycle_period_status_wrong:{cycle.get('status')}")
    if cycle.get("certificate_kind") != "cycle_period_observation_certificate":
        failures.append(f"cycle_period_certificate_kind_wrong:{cycle.get('certificate_kind')}")
    if cycle.get("certificate_scope") != "post_execution_observation_metadata_only":
        failures.append(f"cycle_period_certificate_scope_wrong:{cycle.get('certificate_scope')}")
    cycle_semantics = cycle.get("semantics") or {}

    if cycle.get("does_not_change_halt_law_gate_run_semantics") is not True:
        semantic_guard_ok = all(
            cycle_semantics.get(key) is False
            for key in [
                "halt_semantics_change",
                "law_semantics_change",
                "gate_semantics_change",
                "run_semantics_change",
                "execution_skipping",
                "cycle_execution_skipping",
                "early_halt_on_period_detection",
                "reusing_prior_cycle_results_as_execution",
                "synthetic_cycle_receipts",
                "radius_expansion",
            ]
        )
        if not semantic_guard_ok:
            failures.append("cycle_period_semantics_guard_missing")

    if cycle.get("does_not_delete_or_compress_receipts") is not True:
        receipt_guard_ok = (
            cycle_semantics.get("receipt_deletion") is False
            and cycle_semantics.get("receipt_compression") is False
        )
        if not receipt_guard_ok:
            failures.append("cycle_period_receipt_guard_missing")

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
            failures.append(f"profile_semantics_not_preserved:{key}:{sem.get(key)}")
    if sem.get("passive_observability_layer") is not True:
        failures.append("profile_passive_observability_layer_missing")

    target = target_summary(profile)
    if target["rows"] != 5:
        failures.append(f"target_rows_not_5:{target['rows']}")
    if target["receipts"] != 345:
        failures.append(f"target_receipts_not_345:{target['receipts']}")
    if target["slots"] != EXPECTED_DEPTH_SLOTS:
        failures.append(f"target_depth_slots_wrong:{target['slots']}")
    if target["families"] != ["A", "B", "C", "D", "E"]:
        failures.append(f"target_depth_families_wrong:{target['families']}")
    if target["probes"] != ["MICRO_03_DEPTH_PRESSURE"]:
        failures.append(f"target_depth_probe_wrong:{target['probes']}")

    return failures


def verify_sources(revert_app: dict[str, Any], plan: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if revert_app.get("revert_application_id") != EXPECTED_REVERT_APPLICATION_ID:
        failures.append(f"revert_application_id_mismatch:{revert_app.get('revert_application_id')}")
    if revert_app.get("gate") != "PASS":
        failures.append("revert_application_gate_not_PASS")
    if revert_app.get("source_plan_id") != EXPECTED_PLAN_ID:
        failures.append(f"revert_app_plan_mismatch:{revert_app.get('source_plan_id')}")
    if revert_app.get("source_decision_id") != EXPECTED_DECISION_ID:
        failures.append(f"revert_app_decision_mismatch:{revert_app.get('source_decision_id')}")
    if revert_app.get("source_original_application_id") != EXPECTED_ORIGINAL_APPLICATION_ID:
        failures.append(f"revert_app_original_application_mismatch:{revert_app.get('source_original_application_id')}")
    if revert_app.get("source_comparison_id") != EXPECTED_ORIGINAL_COMPARISON_ID:
        failures.append(f"revert_app_comparison_mismatch:{revert_app.get('source_comparison_id')}")
    if revert_app.get("selected_disposition") != "REVERT_FRONTIER_DEPTH_METADATA_CERTIFICATE_PATCH":
        failures.append(f"revert_app_disposition_wrong:{revert_app.get('selected_disposition')}")

    scope = revert_app.get("revert_scope") or {}
    if scope.get("removed_frontier_depth_patch_only") is not True:
        failures.append("revert_app_not_patch_only")
    if scope.get("deleted_data_artifacts") is not False:
        failures.append("revert_app_deleted_data_artifacts")
    if scope.get("deleted_receipts") is not False:
        failures.append("revert_app_deleted_receipts")
    if scope.get("changed_depth_range") is not False:
        failures.append("revert_app_changed_depth_range")
    if scope.get("expanded_radius") is not False:
        failures.append("revert_app_expanded_radius")
    if scope.get("changed_halt_law_gate_run_semantics") is not False:
        failures.append("revert_app_changed_semantics")
    if scope.get("reopened_accepted_burden_classes") is not False:
        failures.append("revert_app_reopened_accepted_classes")

    removed = scope.get("removed_frontier_markers") or {}
    preserved = scope.get("preserved_cycle_period_markers") or {}
    if not removed or not all(removed.values()):
        failures.append(f"revert_app_frontier_markers_not_removed:{removed}")
    if not preserved or not all(preserved.values()):
        failures.append(f"revert_app_cycle_markers_not_preserved:{preserved}")

    sem = revert_app.get("semantics") or {}
    if sem.get("revert_application") is not True:
        failures.append("revert_app_marker_missing")
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
            failures.append(f"revert_app_semantics_not_preserved:{key}:{sem.get(key)}")

    if plan.get("plan_id") != EXPECTED_PLAN_ID:
        failures.append(f"plan_id_mismatch:{plan.get('plan_id')}")
    if plan.get("gate") != "PASS":
        failures.append("plan_gate_not_PASS")
    if plan.get("selected_disposition") != "REVERT_FRONTIER_DEPTH_METADATA_CERTIFICATE_PATCH":
        failures.append(f"plan_disposition_wrong:{plan.get('selected_disposition')}")
    auth = plan.get("authorization") or {}
    if auth.get("authorizes_apply_revert_command") is not True:
        failures.append("plan_does_not_authorize_revert")
    if auth.get("authorizes_next_burden_policy") is not False:
        failures.append("plan_illegally_authorizes_next_burden")

    return failures


def build_comparison(after_revert_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    COMPARISON_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    after_revert = load_json(PROFILE_DIR / f"{after_revert_id}.json")
    pre_frontier = load_json(PROFILE_DIR / f"{EXPECTED_PRE_FRONTIER_PROFILE_ID}.json")
    bad_after = load_json(PROFILE_DIR / f"{EXPECTED_BAD_AFTER_PROFILE_ID}.json")
    revert_app = load_json(REVERT_APPLICATION_DIR / f"{EXPECTED_REVERT_APPLICATION_ID}.json")
    plan = load_json(PLAN_DIR / f"{EXPECTED_PLAN_ID}.json")

    failures: list[str] = []
    failures.extend(verify_sources(revert_app, plan))
    failures.extend(verify_profile_surface(after_revert, after_revert_id))

    pre_target = target_summary(pre_frontier)
    bad_target = target_summary(bad_after)
    revert_target = target_summary(after_revert)

    if pre_target["row_keys"] != revert_target["row_keys"]:
        failures.append("pre_frontier_to_revert_target_row_keys_changed")
    if pre_target["receipts"] != revert_target["receipts"]:
        failures.append(f"pre_frontier_to_revert_target_receipts_changed:{pre_target['receipts']}->{revert_target['receipts']}")
    if pre_target["slots"] != revert_target["slots"]:
        failures.append(f"pre_frontier_to_revert_target_slots_changed:{pre_target['slots']}->{revert_target['slots']}")

    pre_elapsed = int(pre_target.get("elapsed_ms") or 0)
    bad_elapsed = int(bad_target.get("elapsed_ms") or 0)
    revert_elapsed = int(revert_target.get("elapsed_ms") or 0)

    delta_vs_pre = revert_elapsed - pre_elapsed
    delta_vs_bad = revert_elapsed - bad_elapsed

    if revert_elapsed <= bad_elapsed:
        revert_metric_class = "REVERT_DEPTH_ELAPSED_NON_WORSE_VS_REJECTED_PATCH"
    else:
        revert_metric_class = "REVERT_DEPTH_ELAPSED_WORSE_VS_REJECTED_PATCH_EXPLICITLY_CLASSIFIED"

    warnings = list(revert_app.get("warnings") or [])
    if revert_elapsed > bad_elapsed:
        warnings.append(f"REVERT_DEPTH_ELAPSED_WORSE_VS_REJECTED_PATCH:{bad_elapsed}->{revert_elapsed}")

    comparison = {
        "schema_version": "frontier_depth_probe_revert_after_comparison_v0",
        "comparison_kind": "FRONTIER_DEPTH_PROBE_REVERT_AFTER_PROFILE_COMPARISON",
        "source_revert_application_id": EXPECTED_REVERT_APPLICATION_ID,
        "source_plan_id": EXPECTED_PLAN_ID,
        "source_decision_id": EXPECTED_DECISION_ID,
        "source_original_application_id": EXPECTED_ORIGINAL_APPLICATION_ID,
        "source_original_comparison_id": EXPECTED_ORIGINAL_COMPARISON_ID,
        "pre_frontier_profile_id": EXPECTED_PRE_FRONTIER_PROFILE_ID,
        "bad_after_profile_id": EXPECTED_BAD_AFTER_PROFILE_ID,
        "after_revert_profile_id": after_revert_id,
        "target_burden_class": EXPECTED_TARGET,
        "target_pre_frontier": pre_target,
        "target_bad_after": bad_target,
        "target_after_revert": revert_target,
        "target_delta": {
            "pre_frontier_elapsed_ms": pre_elapsed,
            "bad_after_elapsed_ms": bad_elapsed,
            "after_revert_elapsed_ms": revert_elapsed,
            "after_revert_delta_vs_pre_frontier_ms": delta_vs_pre,
            "after_revert_delta_vs_bad_after_ms": delta_vs_bad,
            "after_revert_ratio_vs_pre_frontier": round(revert_elapsed / pre_elapsed, 6) if pre_elapsed > 0 else None,
            "after_revert_ratio_vs_bad_after": round(revert_elapsed / bad_elapsed, 6) if bad_elapsed > 0 else None,
            "after_revert_receipts_per_sec": revert_target.get("receipts_per_sec"),
        },
        "revert_metric_classification": revert_metric_class,
        "profile_surface": {
            "after_revert_gate": after_revert.get("gate"),
            "after_revert_rows": len(after_revert.get("rows") or []),
            "after_revert_profile_receipts_total": after_revert.get("profile_receipts_total"),
            "after_revert_db_receipt_delta": after_revert.get("db_receipt_delta"),
            "after_revert_families_seen": after_revert.get("families_seen"),
            "frontier_depth_probe_field_absent": "frontier_depth_probe" not in after_revert,
            "cycle_period_compression_field_present": "cycle_period_compression" in after_revert,
            "cycle_period_status": (after_revert.get("cycle_period_compression") or {}).get("status"),
            "cycle_period_certificate_kind": (after_revert.get("cycle_period_compression") or {}).get("certificate_kind"),
        },
        "gate_rules": {
            "revert_application_gate_pass": revert_app.get("gate") == "PASS",
            "after_revert_profile_gate_pass": after_revert.get("gate") == "MICRO_BURDEN_PROFILE_PASS",
            "after_revert_receipt_totals_match_registry": after_revert.get("profile_receipts_total") == after_revert.get("db_receipt_delta"),
            "after_revert_profile_receipt_total_preserved": after_revert.get("profile_receipts_total") == 1457,
            "after_revert_family_coverage_A_E_preserved": after_revert.get("families_seen") == ["A", "B", "C", "D", "E"],
            "after_revert_same_row_count": len(after_revert.get("rows") or []) == 25,
            "frontier_depth_probe_field_absent": "frontier_depth_probe" not in after_revert,
            "cycle_period_compression_field_present": "cycle_period_compression" in after_revert,
            "cycle_period_observation_preserved": (after_revert.get("cycle_period_compression") or {}).get("status") == "APPLIED_POST_EXECUTION_METADATA_ONLY",
            "target_rows_preserved": revert_target["rows"] == 5,
            "target_receipts_preserved": revert_target["receipts"] == 345,
            "target_depth_slots_preserved": revert_target["slots"] == EXPECTED_DEPTH_SLOTS,
            "target_row_keys_match_pre_frontier": pre_target["row_keys"] == revert_target["row_keys"],
            "no_execution_skipping": (after_revert.get("semantics") or {}).get("execution_skipped") is False,
            "no_runner_semantics_changed": (after_revert.get("semantics") or {}).get("runner_semantics_changed") is False,
            "no_gate_semantics_changed": (after_revert.get("semantics") or {}).get("gate_semantics_changed") is False,
            "no_law_semantics_changed": (after_revert.get("semantics") or {}).get("law_semantics_changed") is False,
            "no_receipt_deletion": (after_revert.get("semantics") or {}).get("receipt_rows_deleted") is False,
            "no_receipt_compression": (after_revert.get("semantics") or {}).get("receipts_compressed") is False,
            "passive_observability_layer_preserved": (after_revert.get("semantics") or {}).get("passive_observability_layer") is True,
        },
        "authorization": {
            "authorizes_next_burden_decision": True,
            "authorizes_next_burden_policy": False,
            "authorizes_more_frontier_depth_patching": False,
            "authorizes_reapplying_frontier_depth_patch": False,
            "authorizes_observability_freeze": False,
            "authorizes_receipt_deletion": False,
            "authorizes_data_artifact_deletion": False,
            "authorizes_depth_range_change": False,
            "authorizes_radius_expansion": False,
            "authorizes_halt_law_gate_run_semantics_change": False,
            "authorizes_reopening_accepted_burden_classes": False,
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": "DECIDE_AFTER_FRONTIER_DEPTH_REVERT_NEXT_BURDEN_CLASS_V0" if not failures else None,
            "stop_code": None if not failures else "STOP_FRONTIER_DEPTH_REVERT_AFTER_COMPARISON_FAILED",
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "PASS" if not failures else "FAIL",
        "created_at": now_iso(),
    }

    sig = stable_sig(comparison)
    comparison["comparison_id"] = sig
    comparison["comparison_sig8"] = sig

    receipt = {
        "schema_version": "frontier_depth_probe_revert_after_comparison_receipt_v0",
        "comparison_id": sig,
        "comparison_path": f"data/frontier_depth_probe_revert_after_comparisons/{sig}.json",
        "comparison_sig8": sig,
        "source_revert_application_id": EXPECTED_REVERT_APPLICATION_ID,
        "source_plan_id": EXPECTED_PLAN_ID,
        "source_decision_id": EXPECTED_DECISION_ID,
        "pre_frontier_profile_id": EXPECTED_PRE_FRONTIER_PROFILE_ID,
        "bad_after_profile_id": EXPECTED_BAD_AFTER_PROFILE_ID,
        "after_revert_profile_id": after_revert_id,
        "target_burden_class": EXPECTED_TARGET,
        "revert_metric_classification": revert_metric_class,
        "target_delta": comparison["target_delta"],
        "frontier_depth_probe_field_absent": "frontier_depth_probe" not in after_revert,
        "cycle_period_compression_field_present": "cycle_period_compression" in after_revert,
        "target_receipts_preserved": revert_target["receipts"] == 345,
        "target_rows_preserved": revert_target["rows"] == 5,
        "target_depth_slots_preserved": revert_target["slots"] == EXPECTED_DEPTH_SLOTS,
        "gate": comparison["gate"],
        "terminal": comparison["terminal"],
        "failures": failures,
        "warnings": warnings,
        "created_at": now_iso(),
    }

    rsig = stable_sig(receipt)
    receipt["receipt_id"] = rsig
    receipt["receipt_sig8"] = rsig

    (COMPARISON_DIR / f"{sig}.json").write_text(json.dumps(comparison, indent=2, sort_keys=True))
    (RECEIPT_DIR / f"{sig}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return comparison, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--after-revert", required=True)
    args = parser.parse_args()

    comparison, receipt = build_comparison(args.after_revert)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"comparison_json_path=data/frontier_depth_probe_revert_after_comparisons/{comparison['comparison_id']}.json")
    print(f"comparison_receipt_path=data/frontier_depth_probe_revert_after_comparison_receipts/{comparison['comparison_id']}.json")

    return 0 if comparison["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
