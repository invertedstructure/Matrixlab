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
APPLICATION_DIR = ROOT / "data" / "receipt_volume_fix_applications"
CANDIDATE_DIR = ROOT / "data" / "receipt_volume_fix_candidates"
POLICY_DIR = ROOT / "data" / "receipt_volume_fix_candidate_policies"

COMPARISON_DIR = ROOT / "data" / "receipt_volume_before_after_comparisons"
RECEIPT_DIR = ROOT / "data" / "receipt_volume_before_after_comparison_receipts"

EXPECTED_APPLICATION_ID = "2de50de2"
EXPECTED_CANDIDATE_ID = "17e6ee4e"
EXPECTED_POLICY_ID = "2e6aa9d6"
EXPECTED_BEFORE_PROFILE_ID = "b6609f93"

TARGET_BURDEN_CLASS = "BURDEN_RECEIPT_VOLUME"
EXPECTED_PROBE = "MICRO_05_RECEIPT_WRITE_PRESSURE"
EXPECTED_SLOT = "MICRO_05_RECEIPT_WRITE_PRESSURE_E"
EXPECTED_FAMILY = "E"

ACCEPTED_FROZEN = [
    "BURDEN_CYCLE_SCAN",
    "BURDEN_DB_WRITE",
    "BURDEN_REPEATED_SLOT_WORK",
]

EXPECTED_ALL_NON_UNKNOWN = [
    "BURDEN_CYCLE_SCAN",
    "BURDEN_DB_WRITE",
    "BURDEN_DEPTH_SCAN",
    "BURDEN_RECEIPT_VOLUME",
    "BURDEN_REPEATED_SLOT_WORK",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_sig(obj: dict[str, Any]) -> str:
    body = dict(obj)
    for key in ("comparison_id", "comparison_sig8", "receipt_id", "receipt_sig8"):
        body.pop(key, None)
    return hashlib.sha256(json.dumps(body, sort_keys=True, default=str).encode()).hexdigest()[:8]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def target_summary(profile: dict[str, Any]) -> dict[str, Any]:
    rows = [
        row for row in (profile.get("rows") or [])
        if row.get("burden_class") == TARGET_BURDEN_CLASS
    ]
    receipts = sum(int(row.get("receipts") or 0) for row in rows)
    elapsed_ms = sum(int(row.get("elapsed_ms") or 0) for row in rows)

    return {
        "burden_class": TARGET_BURDEN_CLASS,
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

    scope = app.get("patch_scope") or {}
    if scope.get("touched_files") != ["scripts/wide_burden_profile_microruns.py"]:
        failures.append(f"application_touched_files_wrong:{scope.get('touched_files')}")
    for key in [
        "added_receipt_volume_write_pressure_plan",
        "added_receipt_volume_accounting_certificate",
        "metadata_only_observation",
        "raw_execution_unchanged",
        "raw_receipt_writes_preserved",
        "registry_sqlite_totals_preserved",
        "receipt_payload_durability_preserved",
    ]:
        if scope.get(key) is not True:
            failures.append(f"application_scope_true_guard_failed:{key}:{scope.get(key)}")

    for key in [
        "deleted_receipts",
        "compressed_receipts",
        "suppressed_raw_receipt_writes",
        "emitted_synthetic_receipts",
        "skipped_execution",
        "skipped_receipt_write_pressure_probe",
        "changed_receipt_schema",
        "changed_depth_range",
        "expanded_radius",
        "changed_halt_law_gate_run_semantics",
        "restored_frontier_depth_probe",
        "reopened_accepted_burden_classes",
        "reopened_rejected_depth_scan",
    ]:
        if scope.get(key) is not False:
            failures.append(f"application_scope_false_guard_failed:{key}:{scope.get(key)}")

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
        "reusing_prior_receipt_volume_results_as_execution",
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
            failures.append(f"application_semantics_false_guard_failed:{key}:{sem.get(key)}")
    if sem.get("patch_application") is not True:
        failures.append("application_semantics_patch_application_missing")
    if sem.get("metadata_only_observation") is not True:
        failures.append("application_semantics_metadata_only_missing")

    terminal = app.get("terminal") or {}
    if terminal.get("next_command_goal") != "RERUN_MICRO_BURDEN_PROFILE_AFTER_RECEIPT_VOLUME_FIX_V0":
        failures.append(f"application_terminal_goal_wrong:{terminal.get('next_command_goal')}")

    return failures


def verify_profile(profile: dict[str, Any], expected_id: str, after: bool) -> list[str]:
    failures: list[str] = []

    if profile.get("profile_id") != expected_id:
        failures.append(f"profile_id_mismatch:{profile.get('profile_id')}!={expected_id}")
    if profile.get("gate") != "MICRO_BURDEN_PROFILE_PASS":
        failures.append("profile_gate_not_PASS")
    if len(profile.get("rows") or []) != 25:
        failures.append(f"profile_rows_not_25:{len(profile.get('rows') or [])}")
    if profile.get("families_seen") != ["A", "B", "C", "D", "E"]:
        failures.append(f"profile_families_wrong:{profile.get('families_seen')}")
    if profile.get("profile_receipts_total") != 1457:
        failures.append(f"profile_total_not_1457:{profile.get('profile_receipts_total')}")
    if profile.get("db_receipt_delta") != 1457:
        failures.append(f"profile_db_delta_not_1457:{profile.get('db_receipt_delta')}")
    if profile.get("profile_receipts_total") != profile.get("db_receipt_delta"):
        failures.append("profile_total_mismatch_registry")
    if profile.get("non_unknown_burden_classes") != EXPECTED_ALL_NON_UNKNOWN:
        failures.append(f"profile_non_unknown_wrong:{profile.get('non_unknown_burden_classes')}")
    if profile.get("failures") != []:
        failures.append(f"profile_failures_not_empty:{profile.get('failures')}")
    if "frontier_depth_probe" in profile:
        failures.append("frontier_depth_probe_field_present")
    if "cycle_period_compression" not in profile:
        failures.append("cycle_period_compression_missing")

    target = target_summary(profile)
    if target["rows"] != 1:
        failures.append(f"target_rows_not_1:{target['rows']}")
    if target["receipts"] != 176:
        failures.append(f"target_receipts_not_176:{target['receipts']}")
    if target["families"] != [EXPECTED_FAMILY]:
        failures.append(f"target_family_wrong:{target['families']}")
    if target["probes"] != [EXPECTED_PROBE]:
        failures.append(f"target_probe_wrong:{target['probes']}")
    if target["slots"] != [EXPECTED_SLOT]:
        failures.append(f"target_slot_wrong:{target['slots']}")

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
        failures.append("profile_passive_observability_missing")

    rv = profile.get("receipt_volume_write_pressure")
    if after:
        if not isinstance(rv, dict):
            failures.append("after_receipt_volume_certificate_missing")
        else:
            cert = rv
            if cert.get("certificate_kind") != "receipt_volume_write_pressure_accounting_certificate":
                failures.append(f"receipt_volume_cert_kind_wrong:{cert.get('certificate_kind')}")
            if cert.get("certificate_scope") != "post_execution_observation_metadata_only":
                failures.append(f"receipt_volume_cert_scope_wrong:{cert.get('certificate_scope')}")
            if cert.get("status") != "APPLIED_POST_EXECUTION_METADATA_ONLY":
                failures.append(f"receipt_volume_cert_status_wrong:{cert.get('status')}")
            if cert.get("candidate_id") != EXPECTED_CANDIDATE_ID:
                failures.append(f"receipt_volume_cert_candidate_wrong:{cert.get('candidate_id')}")
            if cert.get("target_burden_class") != TARGET_BURDEN_CLASS:
                failures.append(f"receipt_volume_cert_target_wrong:{cert.get('target_burden_class')}")
            if cert.get("target_rows") != 1:
                failures.append(f"receipt_volume_cert_rows_wrong:{cert.get('target_rows')}")
            if cert.get("target_receipts") != 176:
                failures.append(f"receipt_volume_cert_receipts_wrong:{cert.get('target_receipts')}")
            if cert.get("target_receipts") != target["receipts"]:
                failures.append("receipt_volume_cert_receipts_mismatch_rows")
            if cert.get("target_elapsed_ms") != target["elapsed_ms"]:
                failures.append("receipt_volume_cert_elapsed_mismatch_rows")
            if cert.get("target_row_keys") != target["row_keys"]:
                failures.append("receipt_volume_cert_row_keys_mismatch_rows")
            if cert.get("target_row_identity_preserved") is not True:
                failures.append("receipt_volume_cert_identity_not_preserved")
            if cert.get("target_receipts_preserved") is not True:
                failures.append("receipt_volume_cert_receipts_not_preserved")
            if cert.get("expected_profile_receipts_total") != 1457:
                failures.append(f"receipt_volume_cert_expected_total_wrong:{cert.get('expected_profile_receipts_total')}")
            plan = cert.get("plan") or {}
            if plan.get("expected_target_rows") != 1:
                failures.append("receipt_volume_plan_rows_wrong")
            if plan.get("expected_target_receipts") != 176:
                failures.append("receipt_volume_plan_receipts_wrong")
            if plan.get("expected_profile_receipts_total") != 1457:
                failures.append("receipt_volume_plan_profile_total_wrong")
            if plan.get("probe_id") != EXPECTED_PROBE:
                failures.append("receipt_volume_plan_probe_wrong")
            if plan.get("slot_id") != EXPECTED_SLOT:
                failures.append("receipt_volume_plan_slot_wrong")
            if plan.get("family_compact") != EXPECTED_FAMILY:
                failures.append("receipt_volume_plan_family_wrong")

            cert_sem = cert.get("semantics") or {}
            for key in [
                "receipt_deletion",
                "receipt_compression",
                "raw_receipt_write_suppression",
                "synthetic_receipts",
                "execution_skipping",
                "receipt_write_pressure_probe_skipping",
                "reusing_prior_receipt_volume_results_as_execution",
                "registry_sqlite_total_mismatch",
                "halt_semantics_change",
                "law_semantics_change",
                "gate_semantics_change",
                "run_semantics_change",
                "depth_range_change",
                "radius_expansion",
                "frontier_depth_reopened",
                "accepted_burden_classes_reopened",
            ]:
                if cert_sem.get(key) is not False:
                    failures.append(f"receipt_volume_cert_semantics_not_preserved:{key}:{cert_sem.get(key)}")
    else:
        if rv is not None:
            failures.append("before_profile_unexpected_receipt_volume_certificate")

    return failures


def build_comparison(before_id: str, after_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    COMPARISON_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    application = load_json(APPLICATION_DIR / f"{EXPECTED_APPLICATION_ID}.json")
    candidate = load_json(CANDIDATE_DIR / f"{EXPECTED_CANDIDATE_ID}.json")
    policy = load_json(POLICY_DIR / f"{EXPECTED_POLICY_ID}.json")
    before = load_json(PROFILE_DIR / f"{before_id}.json")
    after = load_json(PROFILE_DIR / f"{after_id}.json")

    failures: list[str] = []
    failures.extend(verify_application(application))

    if candidate.get("gate") != "PASS":
        failures.append("candidate_gate_not_PASS")
    if candidate.get("candidate_id") != EXPECTED_CANDIDATE_ID:
        failures.append(f"candidate_id_mismatch:{candidate.get('candidate_id')}")
    if candidate.get("candidate_status") != "PROPOSAL_ONLY_NOT_APPLIED":
        failures.append(f"candidate_status_mismatch:{candidate.get('candidate_status')}")
    if policy.get("gate") != "PASS":
        failures.append("policy_gate_not_PASS")
    if policy.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"policy_id_mismatch:{policy.get('policy_id')}")

    failures.extend(verify_profile(before, before_id, after=False))
    failures.extend(verify_profile(after, after_id, after=True))

    before_target = target_summary(before)
    after_target = target_summary(after)

    if before_target["row_keys"] != after_target["row_keys"]:
        failures.append("target_row_keys_changed")
    if before_target["receipts"] != after_target["receipts"]:
        failures.append(f"target_receipts_changed:{before_target['receipts']}->{after_target['receipts']}")
    if before.get("profile_receipts_total") != after.get("profile_receipts_total"):
        failures.append(f"profile_total_changed:{before.get('profile_receipts_total')}->{after.get('profile_receipts_total')}")
    if after.get("profile_receipts_total") != after.get("db_receipt_delta"):
        failures.append("after_profile_total_mismatch_registry")

    before_elapsed = int(before_target.get("elapsed_ms") or 0)
    after_elapsed = int(after_target.get("elapsed_ms") or 0)

    elapsed_delta = after_elapsed - before_elapsed
    if after_elapsed <= before_elapsed:
        target_result = "TARGET_BURDEN_ELAPSED_NON_WORSE"
    else:
        target_result = "TARGET_BURDEN_ELAPSED_WORSE_EXPLICIT_FAILURE_CLASSIFICATION"

    warnings = list(application.get("warnings") or [])
    if after_elapsed > before_elapsed:
        warnings.append(f"TARGET_BURDEN_ELAPSED_WORSE:{before_elapsed}->{after_elapsed}")

    rv = after.get("receipt_volume_write_pressure") or {}

    comparison = {
        "schema_version": "receipt_volume_before_after_comparison_v0",
        "comparison_kind": "RECEIPT_VOLUME_BEFORE_AFTER_COMPARISON",
        "source_application_id": EXPECTED_APPLICATION_ID,
        "source_candidate_id": EXPECTED_CANDIDATE_ID,
        "source_policy_id": EXPECTED_POLICY_ID,
        "before_profile_id": before_id,
        "after_profile_id": after_id,
        "target_burden_class": TARGET_BURDEN_CLASS,
        "before_target": before_target,
        "after_target": after_target,
        "target_delta": {
            "before_elapsed_ms": before_elapsed,
            "after_elapsed_ms": after_elapsed,
            "elapsed_ms_delta": elapsed_delta,
            "elapsed_ratio_after_vs_before": round(after_elapsed / before_elapsed, 6) if before_elapsed > 0 else None,
            "speedup_before_over_after": round(before_elapsed / after_elapsed, 6) if after_elapsed > 0 else None,
            "before_receipts_per_sec": before_target.get("receipts_per_sec"),
            "after_receipts_per_sec": after_target.get("receipts_per_sec"),
        },
        "target_result": target_result,
        "profile_surface": {
            "before_gate": before.get("gate"),
            "after_gate": after.get("gate"),
            "before_rows": len(before.get("rows") or []),
            "after_rows": len(after.get("rows") or []),
            "before_profile_receipts_total": before.get("profile_receipts_total"),
            "after_profile_receipts_total": after.get("profile_receipts_total"),
            "after_db_receipt_delta": after.get("db_receipt_delta"),
            "families_seen_preserved": before.get("families_seen") == after.get("families_seen") == ["A", "B", "C", "D", "E"],
            "non_unknown_burden_classes_preserved": before.get("non_unknown_burden_classes") == after.get("non_unknown_burden_classes") == EXPECTED_ALL_NON_UNKNOWN,
            "frontier_depth_probe_absent_after": "frontier_depth_probe" not in after,
            "cycle_period_compression_present_after": "cycle_period_compression" in after,
            "receipt_volume_write_pressure_present_after": "receipt_volume_write_pressure" in after,
        },
        "receipt_volume_certificate": {
            "certificate_kind": rv.get("certificate_kind"),
            "certificate_scope": rv.get("certificate_scope"),
            "status": rv.get("status"),
            "candidate_id": rv.get("candidate_id"),
            "target_row_identity_preserved": rv.get("target_row_identity_preserved"),
            "target_receipts_preserved": rv.get("target_receipts_preserved"),
            "expected_profile_receipts_total": rv.get("expected_profile_receipts_total"),
            "semantics": rv.get("semantics"),
        },
        "gate_rules": {
            "application_gate_pass": application.get("gate") == "PASS",
            "candidate_gate_pass": candidate.get("gate") == "PASS",
            "policy_gate_pass": policy.get("gate") == "PASS",
            "before_profile_gate_pass": before.get("gate") == "MICRO_BURDEN_PROFILE_PASS",
            "after_profile_gate_pass": after.get("gate") == "MICRO_BURDEN_PROFILE_PASS",
            "row_count_preserved": len(before.get("rows") or []) == len(after.get("rows") or []) == 25,
            "families_preserved": before.get("families_seen") == after.get("families_seen") == ["A", "B", "C", "D", "E"],
            "non_unknown_classes_preserved": before.get("non_unknown_burden_classes") == after.get("non_unknown_burden_classes") == EXPECTED_ALL_NON_UNKNOWN,
            "profile_receipt_total_preserved": before.get("profile_receipts_total") == after.get("profile_receipts_total") == 1457,
            "after_registry_total_matches_profile": after.get("profile_receipts_total") == after.get("db_receipt_delta") == 1457,
            "target_row_identity_preserved": before_target["row_keys"] == after_target["row_keys"],
            "target_receipts_preserved": before_target["receipts"] == after_target["receipts"] == 176,
            "receipt_volume_certificate_present": "receipt_volume_write_pressure" in after,
            "receipt_volume_certificate_identity_preserved": rv.get("target_row_identity_preserved") is True,
            "receipt_volume_certificate_receipts_preserved": rv.get("target_receipts_preserved") is True,
            "receipt_volume_certificate_expected_total": rv.get("expected_profile_receipts_total") == 1457,
            "frontier_depth_probe_absent": "frontier_depth_probe" not in after,
            "cycle_period_compression_present": "cycle_period_compression" in after,
            "no_receipt_deletion": (rv.get("semantics") or {}).get("receipt_deletion") is False,
            "no_receipt_compression": (rv.get("semantics") or {}).get("receipt_compression") is False,
            "no_raw_receipt_write_suppression": (rv.get("semantics") or {}).get("raw_receipt_write_suppression") is False,
            "no_synthetic_receipts": (rv.get("semantics") or {}).get("synthetic_receipts") is False,
            "no_execution_skipping": (rv.get("semantics") or {}).get("execution_skipping") is False,
            "no_receipt_write_pressure_probe_skipping": (rv.get("semantics") or {}).get("receipt_write_pressure_probe_skipping") is False,
            "no_registry_sqlite_total_mismatch": (rv.get("semantics") or {}).get("registry_sqlite_total_mismatch") is False,
            "no_halt_law_gate_run_semantics_change": all(
                (rv.get("semantics") or {}).get(k) is False
                for k in ["halt_semantics_change", "law_semantics_change", "gate_semantics_change", "run_semantics_change"]
            ),
            "no_depth_range_change": (rv.get("semantics") or {}).get("depth_range_change") is False,
            "no_radius_expansion": (rv.get("semantics") or {}).get("radius_expansion") is False,
            "no_frontier_depth_reopened": (rv.get("semantics") or {}).get("frontier_depth_reopened") is False,
            "no_accepted_classes_reopened": (rv.get("semantics") or {}).get("accepted_burden_classes_reopened") is False,
        },
        "authorization": {
            "authorizes_outcome_decision_next": True,
            "authorized_next_command_goal": "DECIDE_RECEIPT_VOLUME_FIX_OUTCOME_OR_NEXT_STEP_V0",
            "authorizes_acceptance_now": False,
            "authorizes_revert_now": False,
            "authorizes_next_burden_policy_now": False,
            "authorizes_more_receipt_volume_patching": False,
            "authorizes_receipt_deletion": False,
            "authorizes_receipt_compression": False,
            "authorizes_raw_receipt_write_suppression": False,
            "authorizes_synthetic_receipts": False,
            "authorizes_execution_skipping": False,
            "authorizes_registry_sqlite_total_mismatch": False,
            "authorizes_depth_range_change": False,
            "authorizes_radius_expansion": False,
            "authorizes_halt_law_gate_run_semantics_change": False,
            "authorizes_frontier_depth_reopening": False,
            "authorizes_accepted_class_reopening": False,
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": "DECIDE_RECEIPT_VOLUME_FIX_OUTCOME_OR_NEXT_STEP_V0" if not failures else None,
            "stop_code": None if not failures else "STOP_RECEIPT_VOLUME_BEFORE_AFTER_COMPARISON_INVALID",
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
        "schema_version": "receipt_volume_before_after_comparison_receipt_v0",
        "comparison_id": sig,
        "comparison_path": f"data/receipt_volume_before_after_comparisons/{sig}.json",
        "comparison_sig8": sig,
        "source_application_id": EXPECTED_APPLICATION_ID,
        "source_candidate_id": EXPECTED_CANDIDATE_ID,
        "source_policy_id": EXPECTED_POLICY_ID,
        "before_profile_id": before_id,
        "after_profile_id": after_id,
        "target_burden_class": TARGET_BURDEN_CLASS,
        "target_result": target_result,
        "target_delta": comparison["target_delta"],
        "target_receipts_preserved": before_target["receipts"] == after_target["receipts"] == 176,
        "profile_receipt_total_preserved": before.get("profile_receipts_total") == after.get("profile_receipts_total") == 1457,
        "after_registry_total_matches_profile": after.get("profile_receipts_total") == after.get("db_receipt_delta") == 1457,
        "receipt_volume_certificate_present": "receipt_volume_write_pressure" in after,
        "frontier_depth_probe_absent": "frontier_depth_probe" not in after,
        "cycle_period_compression_present": "cycle_period_compression" in after,
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
    parser.add_argument("--before", default=EXPECTED_BEFORE_PROFILE_ID)
    parser.add_argument("--after", required=True)
    args = parser.parse_args()

    comparison, receipt = build_comparison(args.before, args.after)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"comparison_json_path=data/receipt_volume_before_after_comparisons/{comparison['comparison_id']}.json")
    print(f"comparison_receipt_path=data/receipt_volume_before_after_comparison_receipts/{comparison['comparison_id']}.json")

    return 0 if comparison["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
