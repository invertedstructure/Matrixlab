#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

COMPARISON_DIR = ROOT / "data" / "micro_burden_before_after_comparisons"
PROFILE_DIR = ROOT / "data" / "micro_burden_profiles"
APPLICATION_DIR = ROOT / "data" / "db_write_wal_batched_receipt_write_fix_applications"

DECISION_DIR = ROOT / "data" / "db_write_fix_outcome_decisions"
RECEIPT_DIR = ROOT / "data" / "db_write_fix_outcome_decision_receipts"

EXPECTED_COMPARISON_ID = "fe67c814"
EXPECTED_BEFORE_PROFILE_ID = "c89790f0"
EXPECTED_AFTER_PROFILE_ID = "00a75664"
EXPECTED_APPLICATION_ID = "ff45a8b0"
EXPECTED_SOURCE_CANDIDATE_ID = "2de6e3c2"
EXPECTED_TARGET = "BURDEN_DB_WRITE"

NEXT_BURDEN_MAP = {
    "BURDEN_RECEIPT_VOLUME": {
        "next_command_goal": "BUILD_RECEIPT_VOLUME_ROLLUP_VIEW_FIX_CANDIDATE_POLICY_V0",
        "fix_family": "RECEIPT_VOLUME_READ_SIDE_ROLLUP_VIEW",
        "authority_note": "Operator-view/read-side compression only; raw receipts remain authoritative.",
    },
    "BURDEN_DEPTH_SCAN": {
        "next_command_goal": "BUILD_FRONTIER_DEPTH_PROBE_FIX_CANDIDATE_POLICY_V0",
        "fix_family": "FRONTIER_DEPTH_PROBE_POLICY",
        "authority_note": "Future-run depth frontier policy only; no current probe skipping.",
    },
    "BURDEN_CYCLE_SCAN": {
        "next_command_goal": "BUILD_CYCLE_PERIOD_COMPRESSION_FIX_CANDIDATE_POLICY_V0",
        "fix_family": "CYCLE_PERIOD_COMPRESSION_POLICY",
        "authority_note": "Future-run cycle-period policy only; no halt/law/gate semantics change.",
    },
    "BURDEN_REPEATED_SLOT_WORK": {
        "next_command_goal": "BUILD_REPEATED_SLOT_EXECUTION_PLAN_CACHE_FIX_CANDIDATE_POLICY_V0",
        "fix_family": "REPEATED_SLOT_EXECUTION_PLAN_CACHE",
        "authority_note": "Plan/metadata reuse only; must not skip repeated slot execution or collapse identity.",
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


def verify_sources(comparison: dict[str, Any], after_profile: dict[str, Any], application: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if comparison.get("comparison_id") != EXPECTED_COMPARISON_ID:
        failures.append(f"comparison_id_mismatch:{comparison.get('comparison_id')}")
    if comparison.get("comparison_id") != comparison.get("comparison_sig8"):
        failures.append("comparison_sig_mismatch")
    if comparison.get("gate") != "PASS":
        failures.append("comparison_gate_not_PASS")
    if comparison.get("source_application_id") != EXPECTED_APPLICATION_ID:
        failures.append(f"source_application_id_mismatch:{comparison.get('source_application_id')}")
    if comparison.get("source_candidate_id") != EXPECTED_SOURCE_CANDIDATE_ID:
        failures.append(f"source_candidate_id_mismatch:{comparison.get('source_candidate_id')}")
    if comparison.get("before_profile_id") != EXPECTED_BEFORE_PROFILE_ID:
        failures.append(f"before_profile_id_mismatch:{comparison.get('before_profile_id')}")
    if comparison.get("after_profile_id") != EXPECTED_AFTER_PROFILE_ID:
        failures.append(f"after_profile_id_mismatch:{comparison.get('after_profile_id')}")
    if comparison.get("target_burden_class") != EXPECTED_TARGET:
        failures.append(f"target_burden_class_mismatch:{comparison.get('target_burden_class')}")
    if comparison.get("target_result") not in {
        "TARGET_BURDEN_CLASS_RESOLVED",
        "TARGET_BURDEN_ELAPSED_NON_WORSE",
    }:
        failures.append(f"target_result_not_accepting:{comparison.get('target_result')}")

    gate_rules = comparison.get("gate_rules") or {}
    if not gate_rules:
        failures.append("comparison_gate_rules_missing")
    else:
        for key, value in sorted(gate_rules.items()):
            if value is not True:
                failures.append(f"comparison_gate_rule_false:{key}:{value}")

    if after_profile.get("profile_id") != EXPECTED_AFTER_PROFILE_ID:
        failures.append(f"after_profile_id_mismatch_file:{after_profile.get('profile_id')}")
    if after_profile.get("gate") != "MICRO_BURDEN_PROFILE_PASS":
        failures.append("after_profile_gate_not_MICRO_BURDEN_PROFILE_PASS")
    if after_profile.get("profile_receipts_total") != after_profile.get("db_receipt_delta"):
        failures.append("after_profile_receipt_total_mismatch_registry")
    if after_profile.get("families_seen") != ["A", "B", "C", "D", "E"]:
        failures.append("after_profile_family_coverage_not_A_E")

    sem = after_profile.get("semantics") or {}
    if sem.get("runner_semantics_changed") is not False:
        failures.append("after_profile_runner_semantics_changed")
    if sem.get("gate_semantics_changed") is not False:
        failures.append("after_profile_gate_semantics_changed")
    if sem.get("law_semantics_changed") is not False:
        failures.append("after_profile_law_semantics_changed")
    if sem.get("receipt_rows_deleted") is not False:
        failures.append("after_profile_receipt_rows_deleted")
    if sem.get("execution_skipped") is not False:
        failures.append("after_profile_execution_skipped")

    if application.get("application_id") != EXPECTED_APPLICATION_ID:
        failures.append(f"application_id_mismatch:{application.get('application_id')}")
    if application.get("gate") != "PASS":
        failures.append("application_gate_not_PASS")
    if application.get("source_candidate_id") != EXPECTED_SOURCE_CANDIDATE_ID:
        failures.append(f"application_source_candidate_mismatch:{application.get('source_candidate_id')}")
    if application.get("target_burden_class") != EXPECTED_TARGET:
        failures.append(f"application_target_mismatch:{application.get('target_burden_class')}")

    app_sem = application.get("semantics") or {}
    for key in [
        "receipt_schema_change",
        "receipt_deletion",
        "receipt_compression",
        "execution_skipping",
        "gate_semantics_change",
        "law_semantics_change",
        "run_semantics_change",
        "radius_expansion",
    ]:
        if app_sem.get(key) is not False:
            failures.append(f"application_semantics_not_preserved:{key}:{app_sem.get(key)}")

    return failures


def choose_next_burden(after_summary: dict[str, dict[str, Any]]) -> tuple[str | None, str, list[dict[str, Any]]]:
    candidates = []
    for burden_class, summary in after_summary.items():
        if burden_class in {"BURDEN_UNKNOWN", EXPECTED_TARGET}:
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
        return None, "NO_REMAINING_MAPPED_BURDEN_CLASS", []

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
    return ranked[0]["burden_class"], "MAX_AFTER_ELAPSED_MS_EXCLUDING_DB_WRITE", ranked


def build_decision(comparison_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    DECISION_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    comparison = load_json(COMPARISON_DIR / f"{comparison_id}.json")
    after_profile = load_json(PROFILE_DIR / f"{EXPECTED_AFTER_PROFILE_ID}.json")
    application = load_json(APPLICATION_DIR / f"{EXPECTED_APPLICATION_ID}.json")

    failures = verify_sources(comparison, after_profile, application)
    warnings: list[str] = []

    target_before = comparison.get("target_before") or {}
    target_after = comparison.get("target_after") or {}

    before_elapsed = int(target_before.get("elapsed_ms") or 0)
    after_elapsed = int(target_after.get("elapsed_ms") or 0)
    elapsed_delta = after_elapsed - before_elapsed if before_elapsed or after_elapsed else None
    elapsed_ratio_after_vs_before = round(after_elapsed / before_elapsed, 6) if before_elapsed > 0 else None
    speedup = round(before_elapsed / after_elapsed, 6) if after_elapsed > 0 else None

    before_rps = target_before.get("receipts_per_sec")
    after_rps = target_after.get("receipts_per_sec")
    rps_delta = round(after_rps - before_rps, 6) if before_rps is not None and after_rps is not None else None

    after_summary = comparison.get("after_burden_summary") or {}
    next_burden_class, next_selection_rule, next_ranked = choose_next_burden(after_summary)

    if not next_burden_class:
        warnings.append("NO_REMAINING_MAPPED_BURDEN_CLASS_AFTER_DB_WRITE")
        next_goal = "FREEZE_MICRO_BURDEN_LOOP_OR_DEFINE_NEW_BURDEN_CLASS_V0"
    else:
        next_goal = NEXT_BURDEN_MAP[next_burden_class]["next_command_goal"]

    if comparison.get("target_result") == "TARGET_BURDEN_ELAPSED_NON_WORSE" and elapsed_delta is not None and elapsed_delta <= 0:
        db_write_outcome = "ACCEPT_DB_WRITE_WAL_WRAPPER_FIX"
    elif comparison.get("target_result") == "TARGET_BURDEN_CLASS_RESOLVED":
        db_write_outcome = "ACCEPT_DB_WRITE_WAL_WRAPPER_FIX_TARGET_RESOLVED"
    else:
        db_write_outcome = "REJECT_DB_WRITE_FIX_OR_REQUIRE_REPAIR"
        failures.append("db_write_fix_target_not_accepted")

    decision = {
        "schema_version": "db_write_fix_outcome_decision_v0",
        "decision_kind": "DB_WRITE_FIX_OUTCOME_OR_NEXT_BURDEN_CLASS_DECISION",
        "source_comparison": {
            "comparison_id": comparison.get("comparison_id"),
            "comparison_sig8": comparison.get("comparison_sig8"),
            "gate": comparison.get("gate"),
            "path": f"data/micro_burden_before_after_comparisons/{comparison_id}.json",
        },
        "source_application_id": EXPECTED_APPLICATION_ID,
        "source_candidate_id": EXPECTED_SOURCE_CANDIDATE_ID,
        "before_profile_id": EXPECTED_BEFORE_PROFILE_ID,
        "after_profile_id": EXPECTED_AFTER_PROFILE_ID,
        "target_burden_class": EXPECTED_TARGET,
        "target_result": comparison.get("target_result"),
        "db_write_fix_outcome": db_write_outcome,
        "db_write_metric_delta": {
            "before_elapsed_ms": before_elapsed,
            "after_elapsed_ms": after_elapsed,
            "elapsed_ms_delta": elapsed_delta,
            "elapsed_ratio_after_vs_before": elapsed_ratio_after_vs_before,
            "speedup_before_over_after": speedup,
            "before_receipts_per_sec": before_rps,
            "after_receipts_per_sec": after_rps,
            "receipts_per_sec_delta": rps_delta,
            "before_receipts": target_before.get("receipts"),
            "after_receipts": target_after.get("receipts"),
            "before_rows": target_before.get("rows"),
            "after_rows": target_after.get("rows"),
        },
        "accepted_changes": [
            "KEEP_SQLITE_WAL_CONNECTION_WRAPPER",
            "KEEP_SQLITE_SYNCHRONOUS_NORMAL",
            "KEEP_SQLITE_BUSY_TIMEOUT",
        ],
        "rejected_or_deferred_changes": [
            {
                "change_id": "BATCH_RECEIPT_INSERTS_WITH_EXPLICIT_TRANSACTIONS",
                "status": "NOT_AUTHORIZED_NOW",
                "reason": "WAL-only wrapper produced target non-worse/improved result. Do not add batching without fresh burden evidence.",
            }
        ],
        "authorization": {
            "db_write_fix_accepted": db_write_outcome.startswith("ACCEPT_"),
            "authorizes_more_db_write_patch": False,
            "authorizes_batching_patch": False,
            "authorizes_receipt_deletion": False,
            "authorizes_receipt_compression": False,
            "authorizes_execution_skipping": False,
            "authorizes_gate_semantics_change": False,
            "authorizes_law_semantics_change": False,
            "authorizes_run_semantics_change": False,
            "authorizes_radius_expansion": False,
            "authorizes_next_burden_policy": bool(next_burden_class),
            "next_burden_class": next_burden_class,
        },
        "remaining_after_burden_summary": after_summary,
        "next_burden_selection": {
            "selection_rule": next_selection_rule,
            "ranked_candidates": next_ranked,
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
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": next_goal if not failures else None,
            "stop_code": None if not failures else "STOP_DB_WRITE_FIX_OUTCOME_DECISION_INVALID",
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
        "schema_version": "db_write_fix_outcome_decision_receipt_v0",
        "decision_id": sig,
        "decision_path": f"data/db_write_fix_outcome_decisions/{sig}.json",
        "decision_sig8": sig,
        "source_comparison_id": comparison_id,
        "source_application_id": EXPECTED_APPLICATION_ID,
        "db_write_fix_outcome": db_write_outcome,
        "target_burden_class": EXPECTED_TARGET,
        "target_result": comparison.get("target_result"),
        "db_write_metric_delta": decision["db_write_metric_delta"],
        "next_burden_class": next_burden_class,
        "next_burden_selection_rule": next_selection_rule,
        "authorizes_more_db_write_patch": False,
        "authorizes_batching_patch": False,
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
    print(f"decision_json_path=data/db_write_fix_outcome_decisions/{decision['decision_id']}.json")
    print(f"decision_receipt_path=data/db_write_fix_outcome_decision_receipts/{decision['decision_id']}.json")

    return 0 if decision["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
