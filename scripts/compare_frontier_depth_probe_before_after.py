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
APPLICATION_DIR = ROOT / "data" / "frontier_depth_probe_fix_applications"
COMPARISON_DIR = ROOT / "data" / "frontier_depth_probe_before_after_comparisons"
RECEIPT_DIR = ROOT / "data" / "frontier_depth_probe_before_after_comparison_receipts"

EXPECTED_APPLICATION_ID = "f537dd1f"
EXPECTED_SOURCE_CANDIDATE_ID = "40429f27"
EXPECTED_SOURCE_POLICY_ID = "42028fa3"
EXPECTED_BEFORE_PROFILE_ID = "45cd7660"
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
    slots = [row.get("slot_id") for row in rows if row.get("slot_id")]
    families = sorted({row.get("family_compact") for row in rows if row.get("family_compact")})
    probes = sorted({row.get("probe_id") for row in rows if row.get("probe_id")})
    receipts = sum(int(row.get("receipts") or 0) for row in rows)
    elapsed_ms = sum(int(row.get("elapsed_ms") or 0) for row in rows)
    return {
        "burden_class": EXPECTED_TARGET,
        "rows": len(rows),
        "receipts": receipts,
        "elapsed_ms": elapsed_ms,
        "receipts_per_sec": round(receipts / (elapsed_ms / 1000.0), 6) if elapsed_ms > 0 else None,
        "families": families,
        "probes": probes,
        "slots": slots,
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


def burden_summary(profile: dict[str, Any]) -> dict[str, dict[str, Any]]:
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

    normalized: dict[str, dict[str, Any]] = {}
    for cls, val in out.items():
        elapsed_ms = int(val["elapsed_ms"])
        receipts = int(val["receipts"])
        normalized[cls] = {
            "rows": int(val["rows"]),
            "receipts": receipts,
            "elapsed_ms": elapsed_ms,
            "receipts_per_sec": round(receipts / (elapsed_ms / 1000.0), 6) if elapsed_ms > 0 else None,
            "families": sorted(val["families"]),
            "probes": sorted(val["probes"]),
            "slots": val["slots"],
        }
    return normalized


def verify_frontier_depth_observation(after: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    obs = after.get("frontier_depth_probe") or {}

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

    certificates = obs.get("certificates") or []
    if len(certificates) != 5:
        failures.append(f"frontier_depth_certificate_rows_not_5:{len(certificates)}")
    else:
        cert_slots = [c.get("slot_id") for c in certificates]
        if cert_slots != EXPECTED_DEPTH_SLOTS:
            failures.append(f"frontier_depth_certificate_slots_wrong:{cert_slots}")
        if any(c.get("metadata_only_no_execution_substitution") is not True for c in certificates):
            failures.append("frontier_depth_certificate_missing_no_execution_substitution_marker")
        if any(c.get("depth_range_preserved") is not True for c in certificates):
            failures.append("frontier_depth_certificate_missing_depth_range_preserved_marker")

    return failures


def verify_sources(before: dict[str, Any], after: dict[str, Any], app: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if app.get("application_id") != EXPECTED_APPLICATION_ID:
        failures.append(f"application_id_mismatch:{app.get('application_id')}")
    if app.get("gate") != "PASS":
        failures.append("application_gate_not_PASS")
    if app.get("source_candidate_id") != EXPECTED_SOURCE_CANDIDATE_ID:
        failures.append(f"application_candidate_mismatch:{app.get('source_candidate_id')}")
    if app.get("source_policy_id") != EXPECTED_SOURCE_POLICY_ID:
        failures.append(f"application_policy_mismatch:{app.get('source_policy_id')}")
    if app.get("before_profile_id") != EXPECTED_BEFORE_PROFILE_ID:
        failures.append(f"application_before_profile_mismatch:{app.get('before_profile_id')}")
    if app.get("target_burden_class") != EXPECTED_TARGET:
        failures.append(f"application_target_mismatch:{app.get('target_burden_class')}")

    app_sem = app.get("semantics") or {}
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

    if before.get("profile_id") != EXPECTED_BEFORE_PROFILE_ID:
        failures.append(f"before_profile_id_mismatch:{before.get('profile_id')}")
    if before.get("gate") != "MICRO_BURDEN_PROFILE_PASS":
        failures.append("before_profile_gate_not_PASS")

    if after.get("profile_id") == EXPECTED_BEFORE_PROFILE_ID:
        failures.append("after_profile_reused_before_profile_id")
    if after.get("gate") != "MICRO_BURDEN_PROFILE_PASS":
        failures.append("after_profile_gate_not_PASS")
    if after.get("families_seen") != ["A", "B", "C", "D", "E"]:
        failures.append("after_family_coverage_not_A_E")
    if len(after.get("rows") or []) != len(before.get("rows") or []):
        failures.append(f"profile_row_count_changed:{len(before.get('rows') or [])}->{len(after.get('rows') or [])}")
    if after.get("profile_receipts_total") != after.get("db_receipt_delta"):
        failures.append("after_receipt_total_mismatch_registry")
    if before.get("profile_receipts_total") != before.get("db_receipt_delta"):
        failures.append("before_receipt_total_mismatch_registry")
    if after.get("profile_receipts_total") != before.get("profile_receipts_total"):
        failures.append(f"profile_receipt_total_changed:{before.get('profile_receipts_total')}->{after.get('profile_receipts_total')}")

    after_sem = after.get("semantics") or {}
    if after_sem.get("runner_semantics_changed") is not False:
        failures.append("after_runner_semantics_changed")
    if after_sem.get("gate_semantics_changed") is not False:
        failures.append("after_gate_semantics_changed")
    if after_sem.get("law_semantics_changed") is not False:
        failures.append("after_law_semantics_changed")
    if after_sem.get("receipt_rows_deleted") is not False:
        failures.append("after_receipt_rows_deleted")
    if after_sem.get("execution_skipped") is not False:
        failures.append("after_execution_skipped")

    failures.extend(verify_frontier_depth_observation(after))

    return failures


def build_comparison(before_id: str, after_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    COMPARISON_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    before = load_json(PROFILE_DIR / f"{before_id}.json")
    after = load_json(PROFILE_DIR / f"{after_id}.json")
    app = load_json(APPLICATION_DIR / f"{EXPECTED_APPLICATION_ID}.json")

    failures = verify_sources(before, after, app)
    warnings: list[str] = []

    before_target = target_summary(before)
    after_target = target_summary(after)

    if before_target["slots"] != EXPECTED_DEPTH_SLOTS:
        failures.append(f"before_target_slots_changed:{before_target['slots']}")
    if after_target["slots"] != EXPECTED_DEPTH_SLOTS:
        failures.append(f"after_target_slots_changed:{after_target['slots']}")
    if before_target["row_keys"] != after_target["row_keys"]:
        failures.append("target_row_keys_changed")
    if after_target["rows"] != 5:
        failures.append(f"after_target_rows_not_5:{after_target['rows']}")
    if after_target["receipts"] != before_target["receipts"]:
        failures.append(f"target_receipts_changed:{before_target['receipts']}->{after_target['receipts']}")

    before_elapsed = int(before_target.get("elapsed_ms") or 0)
    after_elapsed = int(after_target.get("elapsed_ms") or 0)
    elapsed_delta = after_elapsed - before_elapsed
    elapsed_ratio = round(after_elapsed / before_elapsed, 6) if before_elapsed > 0 else None
    speedup = round(before_elapsed / after_elapsed, 6) if after_elapsed > 0 else None

    if after_elapsed <= before_elapsed:
        target_result = "TARGET_BURDEN_ELAPSED_NON_WORSE"
    else:
        target_result = "TARGET_BURDEN_ELAPSED_WORSE_EXPLICIT_FAILURE_CLASSIFICATION"
        warnings.append(f"TARGET_BURDEN_ELAPSED_WORSE:{before_elapsed}->{after_elapsed}")

    comparison = {
        "schema_version": "frontier_depth_probe_before_after_comparison_v0",
        "comparison_kind": "FRONTIER_DEPTH_PROBE_BEFORE_AFTER_COMPARISON",
        "source_application_id": EXPECTED_APPLICATION_ID,
        "source_candidate_id": EXPECTED_SOURCE_CANDIDATE_ID,
        "source_policy_id": EXPECTED_SOURCE_POLICY_ID,
        "before_profile_id": before_id,
        "after_profile_id": after_id,
        "target_burden_class": EXPECTED_TARGET,
        "target_result": target_result,
        "target_before": before_target,
        "target_after": after_target,
        "target_delta": {
            "before_elapsed_ms": before_elapsed,
            "after_elapsed_ms": after_elapsed,
            "elapsed_ms_delta": elapsed_delta,
            "elapsed_ratio_after_vs_before": elapsed_ratio,
            "speedup_before_over_after": speedup,
            "before_receipts_per_sec": before_target.get("receipts_per_sec"),
            "after_receipts_per_sec": after_target.get("receipts_per_sec"),
            "receipts_per_sec_delta": (
                round(after_target["receipts_per_sec"] - before_target["receipts_per_sec"], 6)
                if after_target.get("receipts_per_sec") is not None and before_target.get("receipts_per_sec") is not None
                else None
            ),
        },
        "before_burden_summary": burden_summary(before),
        "after_burden_summary": burden_summary(after),
        "frontier_depth_observation": after.get("frontier_depth_probe") or {},
        "gate_rules": {
            "application_gate_pass": app.get("gate") == "PASS",
            "after_profile_gate_pass": after.get("gate") == "MICRO_BURDEN_PROFILE_PASS",
            "after_receipt_totals_match_registry": after.get("profile_receipts_total") == after.get("db_receipt_delta"),
            "profile_receipt_total_preserved": after.get("profile_receipts_total") == before.get("profile_receipts_total"),
            "family_coverage_A_E_preserved": after.get("families_seen") == ["A", "B", "C", "D", "E"],
            "same_row_count": len(after.get("rows") or []) == len(before.get("rows") or []),
            "same_target_row_keys": before_target["row_keys"] == after_target["row_keys"],
            "depth_slot_identity_preserved": after_target["slots"] == EXPECTED_DEPTH_SLOTS,
            "target_receipts_preserved": after_target["receipts"] == before_target["receipts"],
            "target_depth_elapsed_non_worse": after_elapsed <= before_elapsed,
            "target_depth_elapsed_non_worse_or_explicitly_classified": (
                after_elapsed <= before_elapsed
                or target_result == "TARGET_BURDEN_ELAPSED_WORSE_EXPLICIT_FAILURE_CLASSIFICATION"
            ),
            "frontier_depth_metadata_present": (after.get("frontier_depth_probe") or {}).get("status") == "APPLIED_POST_EXECUTION_DEPTH_METADATA_ONLY",
            "frontier_depth_certificate_count_5": (after.get("frontier_depth_probe") or {}).get("certificate_count") == 5,
            "frontier_depth_metadata_only_no_execution_substitution": all(
                c.get("metadata_only_no_execution_substitution") is True
                for c in ((after.get("frontier_depth_probe") or {}).get("certificates") or [])
            ),
            "depth_range_preserved": (after.get("frontier_depth_probe") or {}).get("does_not_change_depth_range") is True,
            "radius_not_expanded": (after.get("frontier_depth_probe") or {}).get("does_not_expand_radius") is True,
            "no_execution_skipping": (after.get("semantics") or {}).get("execution_skipped") is False,
            "no_gate_semantics_changed": (after.get("semantics") or {}).get("gate_semantics_changed") is False,
            "no_law_semantics_changed": (after.get("semantics") or {}).get("law_semantics_changed") is False,
            "no_runner_semantics_changed": (after.get("semantics") or {}).get("runner_semantics_changed") is False,
            "no_receipt_deletion": (after.get("semantics") or {}).get("receipt_rows_deleted") is False,
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": "DECIDE_FRONTIER_DEPTH_PROBE_FIX_OUTCOME_OR_NEXT_BURDEN_CLASS_V0" if not failures else None,
            "stop_code": None if not failures else "STOP_FRONTIER_DEPTH_PROBE_COMPARISON_FAILED",
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
        "schema_version": "frontier_depth_probe_before_after_comparison_receipt_v0",
        "comparison_id": sig,
        "comparison_path": f"data/frontier_depth_probe_before_after_comparisons/{sig}.json",
        "comparison_sig8": sig,
        "source_application_id": EXPECTED_APPLICATION_ID,
        "source_candidate_id": EXPECTED_SOURCE_CANDIDATE_ID,
        "source_policy_id": EXPECTED_SOURCE_POLICY_ID,
        "before_profile_id": before_id,
        "after_profile_id": after_id,
        "target_burden_class": EXPECTED_TARGET,
        "target_result": target_result,
        "target_delta": comparison["target_delta"],
        "depth_slot_identity_preserved": after_target["slots"] == EXPECTED_DEPTH_SLOTS,
        "target_receipts_preserved": after_target["receipts"] == before_target["receipts"],
        "frontier_depth_metadata_present": (after.get("frontier_depth_probe") or {}).get("status") == "APPLIED_POST_EXECUTION_DEPTH_METADATA_ONLY",
        "frontier_depth_certificate_count": (after.get("frontier_depth_probe") or {}).get("certificate_count"),
        "depth_range_preserved": (after.get("frontier_depth_probe") or {}).get("does_not_change_depth_range"),
        "radius_not_expanded": (after.get("frontier_depth_probe") or {}).get("does_not_expand_radius"),
        "gate": comparison["gate"],
        "terminal": comparison["terminal"],
        "failures": failures,
        "warnings": warnings,
        "created_at": now_iso(),
    }

    receipt_sig = stable_sig(receipt)
    receipt["receipt_id"] = receipt_sig
    receipt["receipt_sig8"] = receipt_sig

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
    print(f"comparison_json_path=data/frontier_depth_probe_before_after_comparisons/{comparison['comparison_id']}.json")
    print(f"comparison_receipt_path=data/frontier_depth_probe_before_after_comparison_receipts/{comparison['comparison_id']}.json")

    return 0 if comparison["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
