#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

NEXT_DECISION_DIR = ROOT / "data" / "post_frontier_depth_revert_next_burden_decisions"
PROFILE_DIR = ROOT / "data" / "micro_burden_profiles"

POLICY_DIR = ROOT / "data" / "receipt_volume_fix_candidate_policies"
RECEIPT_DIR = ROOT / "data" / "receipt_volume_fix_candidate_policy_receipts"

EXPECTED_NEXT_DECISION_ID = "25bf9c59"
EXPECTED_AFTER_REVERT_PROFILE_ID = "b6609f93"
TARGET_BURDEN_CLASS = "BURDEN_RECEIPT_VOLUME"
EXPECTED_PROBE = "MICRO_05_RECEIPT_WRITE_PRESSURE"
EXPECTED_SLOT = "MICRO_05_RECEIPT_WRITE_PRESSURE_E"
EXPECTED_FAMILY = "E"

AUTHORIZED_FIX_CANDIDATE_ID = "FIX_CANDIDATE_RECEIPT_VOLUME_WRITE_PRESSURE_PLAN_V0"
AUTHORIZED_FIX_CANDIDATE_KIND = "RECEIPT_VOLUME_FIX_CANDIDATE"

ACCEPTED_FROZEN = [
    "BURDEN_CYCLE_SCAN",
    "BURDEN_DB_WRITE",
    "BURDEN_REPEATED_SLOT_WORK",
]

REJECTED_OR_DEFERRED = [
    "BURDEN_DEPTH_SCAN",
]

EXPECTED_ALL_NON_UNKNOWN = [
    "BURDEN_CYCLE_SCAN",
    "BURDEN_DB_WRITE",
    "BURDEN_DEPTH_SCAN",
    "BURDEN_RECEIPT_VOLUME",
    "BURDEN_REPEATED_SLOT_WORK",
]

NEXT_COMMAND_GOAL = "BUILD_RECEIPT_VOLUME_FIX_CANDIDATE_V0"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_sig(obj: dict[str, Any]) -> str:
    body = dict(obj)
    for key in ("policy_id", "policy_sig8", "receipt_id", "receipt_sig8"):
        body.pop(key, None)
    blob = json.dumps(body, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:8]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def summarize_target_rows(profile: dict[str, Any]) -> dict[str, Any]:
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
        "rows_detail": rows,
    }


def verify_next_decision(decision: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if decision.get("decision_id") != EXPECTED_NEXT_DECISION_ID:
        failures.append(f"decision_id_mismatch:{decision.get('decision_id')}")
    if decision.get("decision_id") != decision.get("decision_sig8"):
        failures.append("decision_sig_mismatch")
    if decision.get("gate") != "PASS":
        failures.append("decision_gate_not_PASS")
    if decision.get("failures") != []:
        failures.append(f"decision_failures_not_empty:{decision.get('failures')}")
    if decision.get("after_revert_profile_id") != EXPECTED_AFTER_REVERT_PROFILE_ID:
        failures.append(f"decision_after_revert_profile_mismatch:{decision.get('after_revert_profile_id')}")

    if decision.get("accepted_burden_classes_frozen") != ACCEPTED_FROZEN:
        failures.append(f"accepted_frozen_mismatch:{decision.get('accepted_burden_classes_frozen')}")

    rejected = decision.get("rejected_or_deferred_burden_classes") or []
    rejected_classes = [item.get("burden_class") for item in rejected]
    if rejected_classes != REJECTED_OR_DEFERRED:
        failures.append(f"rejected_or_deferred_mismatch:{rejected_classes}")
    if rejected and rejected[0].get("reopen_allowed") is not False:
        failures.append("rejected_depth_reopen_allowed")

    if decision.get("all_non_unknown_burden_classes") != EXPECTED_ALL_NON_UNKNOWN:
        failures.append(f"all_non_unknown_mismatch:{decision.get('all_non_unknown_burden_classes')}")
    if decision.get("eligible_unresolved_burden_classes") != [TARGET_BURDEN_CLASS]:
        failures.append(f"eligible_unresolved_mismatch:{decision.get('eligible_unresolved_burden_classes')}")
    if decision.get("selected_next_burden_class") != TARGET_BURDEN_CLASS:
        failures.append(f"selected_next_burden_mismatch:{decision.get('selected_next_burden_class')}")

    evidence = decision.get("selected_next_burden_evidence") or {}
    if evidence.get("rows") != 1:
        failures.append(f"selected_evidence_rows_not_1:{evidence.get('rows')}")
    if evidence.get("receipts") != 176:
        failures.append(f"selected_evidence_receipts_not_176:{evidence.get('receipts')}")
    if evidence.get("elapsed_ms") != 1005:
        failures.append(f"selected_evidence_elapsed_not_1005:{evidence.get('elapsed_ms')}")
    if evidence.get("families") != [EXPECTED_FAMILY]:
        failures.append(f"selected_evidence_family_mismatch:{evidence.get('families')}")
    if evidence.get("probes") != [EXPECTED_PROBE]:
        failures.append(f"selected_evidence_probe_mismatch:{evidence.get('probes')}")
    if evidence.get("slots") != [EXPECTED_SLOT]:
        failures.append(f"selected_evidence_slot_mismatch:{evidence.get('slots')}")

    reason = decision.get("selection_reason") or {}
    if reason.get("frontier_depth_revert_confirmed") is not True:
        failures.append("frontier_depth_revert_not_confirmed")
    if reason.get("frontier_depth_probe_field_absent") is not True:
        failures.append("frontier_depth_probe_field_not_absent")
    if reason.get("cycle_period_compression_field_present") is not True:
        failures.append("cycle_period_field_not_present")
    if reason.get("accepted_classes_not_reopened") != ACCEPTED_FROZEN:
        failures.append("accepted_classes_reopened_or_mismatch")
    if reason.get("rejected_depth_not_reopened") is not True:
        failures.append("rejected_depth_reopened")
    if reason.get("only_remaining_eligible_non_unknown_burden") is not True:
        failures.append("not_only_remaining_eligible_burden")

    auth = decision.get("authorization") or {}
    if auth.get("authorizes_next_burden_policy") is not True:
        failures.append("decision_does_not_authorize_next_burden_policy")
    if auth.get("authorized_next_command_goal") != "BUILD_RECEIPT_VOLUME_FIX_CANDIDATE_POLICY_V0":
        failures.append(f"decision_authorized_next_goal_mismatch:{auth.get('authorized_next_command_goal')}")
    if auth.get("authorized_target_burden_class") != TARGET_BURDEN_CLASS:
        failures.append(f"decision_authorized_target_mismatch:{auth.get('authorized_target_burden_class')}")
    for key in [
        "authorizes_patch_application",
        "authorizes_code_change_now",
        "authorizes_reopening_accepted_burden_classes",
        "authorizes_reopening_frontier_depth",
        "authorizes_more_frontier_depth_patching",
        "authorizes_reapplying_frontier_depth_patch",
        "authorizes_observability_freeze",
        "authorizes_receipt_deletion",
        "authorizes_receipt_compression",
        "authorizes_data_artifact_deletion",
        "authorizes_execution_skipping",
        "authorizes_depth_probe_skipping",
        "authorizes_frontier_case_skipping",
        "authorizes_synthetic_receipts",
        "authorizes_depth_range_change",
        "authorizes_radius_expansion",
        "authorizes_halt_semantics_change",
        "authorizes_law_semantics_change",
        "authorizes_gate_semantics_change",
        "authorizes_run_semantics_change",
    ]:
        if auth.get(key) is not False:
            failures.append(f"decision_illegal_authorization:{key}:{auth.get(key)}")

    required = decision.get("required_next_gate") or {}
    if required.get("next_command_goal") != "BUILD_RECEIPT_VOLUME_FIX_CANDIDATE_POLICY_V0":
        failures.append(f"required_next_goal_mismatch:{required.get('next_command_goal')}")
    if required.get("must_target_burden_class") != TARGET_BURDEN_CLASS:
        failures.append("required_next_target_mismatch")
    if required.get("must_use_decision_id") != EXPECTED_NEXT_DECISION_ID:
        failures.append("required_next_decision_id_mismatch")
    if required.get("must_use_after_revert_profile_id") != EXPECTED_AFTER_REVERT_PROFILE_ID:
        failures.append("required_next_after_revert_profile_mismatch")
    if required.get("must_preserve_accepted_burden_classes") != ACCEPTED_FROZEN:
        failures.append("required_next_accepted_frozen_mismatch")
    if required.get("must_not_reopen_rejected_depth_scan") is not True:
        failures.append("required_next_may_reopen_depth_scan")
    if required.get("must_not_delete_receipts") is not True:
        failures.append("required_next_may_delete_receipts")
    if required.get("must_not_delete_data_artifacts") is not True:
        failures.append("required_next_may_delete_data_artifacts")
    if required.get("must_not_change_halt_law_gate_run_semantics") is not True:
        failures.append("required_next_may_change_semantics")
    if required.get("must_not_change_depth_range") is not True:
        failures.append("required_next_may_change_depth_range")
    if required.get("must_not_expand_radius") is not True:
        failures.append("required_next_may_expand_radius")
    if required.get("policy_only_no_patch_application") is not True:
        failures.append("required_next_not_policy_only")

    terminal = decision.get("terminal") or {}
    if terminal.get("next_command_goal") != "BUILD_RECEIPT_VOLUME_FIX_CANDIDATE_POLICY_V0":
        failures.append(f"decision_terminal_goal_mismatch:{terminal.get('next_command_goal')}")

    return failures


def verify_profile(profile: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if profile.get("profile_id") != EXPECTED_AFTER_REVERT_PROFILE_ID:
        failures.append(f"profile_id_mismatch:{profile.get('profile_id')}")
    if profile.get("gate") != "MICRO_BURDEN_PROFILE_PASS":
        failures.append("profile_gate_not_PASS")
    if profile.get("failures") != []:
        failures.append(f"profile_failures_not_empty:{profile.get('failures')}")
    if len(profile.get("rows") or []) != 25:
        failures.append(f"profile_rows_not_25:{len(profile.get('rows') or [])}")
    if profile.get("families_seen") != ["A", "B", "C", "D", "E"]:
        failures.append(f"profile_families_wrong:{profile.get('families_seen')}")
    if profile.get("profile_receipts_total") != 1457:
        failures.append(f"profile_total_not_1457:{profile.get('profile_receipts_total')}")
    if profile.get("profile_receipts_total") != profile.get("db_receipt_delta"):
        failures.append("profile_total_mismatch_registry")
    if profile.get("non_unknown_burden_classes") != EXPECTED_ALL_NON_UNKNOWN:
        failures.append(f"profile_non_unknown_mismatch:{profile.get('non_unknown_burden_classes')}")
    if "frontier_depth_probe" in profile:
        failures.append("profile_frontier_depth_probe_field_present")
    if "cycle_period_compression" not in profile:
        failures.append("profile_cycle_period_field_missing")

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

    target = summarize_target_rows(profile)
    if target["rows"] != 1:
        failures.append(f"target_rows_not_1:{target['rows']}")
    if target["receipts"] != 176:
        failures.append(f"target_receipts_not_176:{target['receipts']}")
    if target["elapsed_ms"] <= 0:
        failures.append(f"target_elapsed_not_positive:{target['elapsed_ms']}")
    if target["families"] != [EXPECTED_FAMILY]:
        failures.append(f"target_family_mismatch:{target['families']}")
    if target["probes"] != [EXPECTED_PROBE]:
        failures.append(f"target_probe_mismatch:{target['probes']}")
    if target["slots"] != [EXPECTED_SLOT]:
        failures.append(f"target_slot_mismatch:{target['slots']}")

    return failures


def build_policy(decision_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    POLICY_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    decision = load_json(NEXT_DECISION_DIR / f"{decision_id}.json")
    profile = load_json(PROFILE_DIR / f"{EXPECTED_AFTER_REVERT_PROFILE_ID}.json")

    failures: list[str] = []
    failures.extend(verify_next_decision(decision))
    failures.extend(verify_profile(profile))

    target = summarize_target_rows(profile)
    warnings = list(decision.get("warnings") or [])

    policy = {
        "schema_version": "receipt_volume_fix_candidate_policy_v0",
        "policy_kind": "BUILD_RECEIPT_VOLUME_FIX_CANDIDATE_POLICY",
        "source_next_burden_decision_id": EXPECTED_NEXT_DECISION_ID,
        "source_after_revert_profile_id": EXPECTED_AFTER_REVERT_PROFILE_ID,
        "target_burden_class": TARGET_BURDEN_CLASS,
        "target_burden_evidence": target,
        "accepted_burden_classes_frozen": ACCEPTED_FROZEN,
        "rejected_or_deferred_burden_classes_frozen": REJECTED_OR_DEFERRED,
        "policy_scope": {
            "policy_only_no_patch_application": True,
            "authorizes_exactly_one_fix_candidate": True,
            "authorized_fix_candidate_id": AUTHORIZED_FIX_CANDIDATE_ID,
            "authorized_fix_candidate_kind": AUTHORIZED_FIX_CANDIDATE_KIND,
            "authorized_target_burden_class": TARGET_BURDEN_CLASS,
            "candidate_must_preserve_receipt_rows": True,
            "candidate_must_preserve_receipt_payload_durability": True,
            "candidate_must_preserve_registry_sqlite_totals": True,
            "candidate_must_preserve_raw_receipt_writes": True,
            "candidate_must_preserve_profile_total_1457": True,
        },
        "authorization": {
            "authorizes_fix_candidate_count": 1,
            "authorizes_fix_candidate_ids": [AUTHORIZED_FIX_CANDIDATE_ID],
            "authorizes_fix_candidate_kind": AUTHORIZED_FIX_CANDIDATE_KIND,
            "authorizes_patch_application": False,
            "authorizes_code_change_now": False,
            "authorizes_receipt_deletion": False,
            "authorizes_receipt_compression": False,
            "authorizes_receipt_lossy_summary": False,
            "authorizes_raw_receipt_write_suppression": False,
            "authorizes_registry_sqlite_total_mismatch": False,
            "authorizes_execution_skipping": False,
            "authorizes_probe_skipping": False,
            "authorizes_receipt_write_pressure_skipping": False,
            "authorizes_synthetic_receipts": False,
            "authorizes_reusing_prior_receipt_volume_results_as_execution": False,
            "authorizes_depth_range_change": False,
            "authorizes_radius_expansion": False,
            "authorizes_halt_semantics_change": False,
            "authorizes_law_semantics_change": False,
            "authorizes_gate_semantics_change": False,
            "authorizes_run_semantics_change": False,
            "authorizes_reopening_accepted_burden_classes": False,
            "authorizes_reopening_frontier_depth": False,
            "authorizes_more_frontier_depth_patching": False,
            "authorizes_data_artifact_deletion": False,
        },
        "candidate_requirements": {
            "candidate_status_must_be": "PROPOSAL_ONLY_NOT_APPLIED",
            "candidate_must_target_burden_class": TARGET_BURDEN_CLASS,
            "candidate_must_use_source_policy_id": None,
            "candidate_must_use_source_profile_id": EXPECTED_AFTER_REVERT_PROFILE_ID,
            "candidate_must_use_source_decision_id": EXPECTED_NEXT_DECISION_ID,
            "candidate_must_preserve_target_row_identity": {
                "rows": 1,
                "family_compact": EXPECTED_FAMILY,
                "probe_id": EXPECTED_PROBE,
                "slot_id": EXPECTED_SLOT,
                "burden_class": TARGET_BURDEN_CLASS,
            },
            "candidate_must_preserve_receipts": 176,
            "candidate_must_preserve_micro_profile_receipt_total": 1457,
            "candidate_must_preserve_families_seen": ["A", "B", "C", "D", "E"],
            "candidate_must_preserve_all_non_unknown_burden_classes": EXPECTED_ALL_NON_UNKNOWN,
            "candidate_must_not_modify_or_reopen": {
                "accepted_burden_classes": ACCEPTED_FROZEN,
                "rejected_depth_scan": True,
            },
            "candidate_must_include_negative_controls_for": [
                "receipt deletion authority",
                "receipt compression authority",
                "raw receipt suppression authority",
                "registry total mismatch authority",
                "synthetic receipt authority",
                "execution skipping authority",
                "receipt write pressure skipping authority",
                "target row identity drift",
                "profile total drift",
                "accepted class reopening",
                "frontier-depth reopening",
            ],
        },
        "allowed_candidate_design_space": [
            {
                "design_id": "RECEIPT_WRITE_VOLUME_PLAN_CACHE_METADATA_ONLY",
                "description": "Cache deterministic receipt-write pressure plan metadata, not receipt rows/results, within one profile execution.",
                "hard_constraint": "No receipt row may be deleted, suppressed, summarized, compressed, or reused as execution output.",
            },
            {
                "design_id": "RECEIPT_VOLUME_WRITE_PATH_ACCOUNTING_CERTIFICATE",
                "description": "Add explicit post-execution accounting for receipt-volume pressure so future comparisons cannot confuse receipt volume reduction with receipt loss.",
                "hard_constraint": "Accounting certificate is observational only and cannot authorize fewer receipts.",
            },
            {
                "design_id": "RECEIPT_WRITE_PRESSURE_BATCHING_PROPOSAL_ONLY",
                "description": "Consider a future candidate that batches write-path operations while preserving exact receipt count, payload durability, and registry totals.",
                "hard_constraint": "Batching cannot alter receipt schema, receipt count, registry rows, halt/law/gate/run semantics, or raw receipt availability.",
            },
        ],
        "forbidden_candidate_design_space": [
            "delete receipt rows",
            "compress receipt rows",
            "replace receipts with summaries",
            "skip receipt write pressure probe",
            "emit synthetic receipts",
            "reuse prior receipt-volume outputs as execution",
            "change registry.sqlite accounting",
            "change receipt schema",
            "change halt/law/gate/run semantics",
            "change depth range",
            "expand radius",
            "reopen BURDEN_DEPTH_SCAN",
            "reopen accepted burden classes",
        ],
        "required_retest_if_candidate_later_applied": {
            "after_profile_required": True,
            "before_profile_id": EXPECTED_AFTER_REVERT_PROFILE_ID,
            "same_micro_suite_required": True,
            "same_probe_specs_required": True,
            "same_script": "scripts/wide_burden_profile_microruns.py --execute",
            "comparison_required": True,
            "comparison_artifact_schema": "receipt_volume_before_after_comparison_v0",
            "pass_condition": [
                "after profile gate MICRO_BURDEN_PROFILE_PASS",
                "receipt totals match registry.sqlite",
                "profile receipt total preserved at 1457",
                "target row remains MICRO_05_RECEIPT_WRITE_PRESSURE_E",
                "target receipts preserved at 176",
                "target burden class remains BURDEN_RECEIPT_VOLUME",
                "raw receipt rows preserved",
                "no receipt deletion",
                "no receipt compression",
                "no receipt schema change",
                "no synthetic receipts",
                "no execution skipping",
                "no receipt write pressure probe skipping",
                "no registry total mismatch",
                "no halt/law/gate/run semantics change",
                "no depth range change",
                "no radius expansion",
                "no accepted burden class reopening",
                "no frontier-depth reopening",
                "BURDEN_RECEIPT_VOLUME elapsed_ms non-worse or explicit failure classification",
            ],
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_RECEIPT_VOLUME_POLICY_INVALID",
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "PASS" if not failures else "FAIL",
        "created_at": now_iso(),
    }

    sig = stable_sig(policy)
    policy["policy_id"] = sig
    policy["policy_sig8"] = sig
    policy["candidate_requirements"]["candidate_must_use_source_policy_id"] = sig

    receipt = {
        "schema_version": "receipt_volume_fix_candidate_policy_receipt_v0",
        "policy_id": sig,
        "policy_path": f"data/receipt_volume_fix_candidate_policies/{sig}.json",
        "policy_sig8": sig,
        "source_next_burden_decision_id": EXPECTED_NEXT_DECISION_ID,
        "source_after_revert_profile_id": EXPECTED_AFTER_REVERT_PROFILE_ID,
        "target_burden_class": TARGET_BURDEN_CLASS,
        "target_rows": target["rows"],
        "target_receipts": target["receipts"],
        "target_elapsed_ms": target["elapsed_ms"],
        "target_receipts_per_sec": target["receipts_per_sec"],
        "target_probe": EXPECTED_PROBE,
        "target_slot": EXPECTED_SLOT,
        "accepted_burden_classes_frozen": ACCEPTED_FROZEN,
        "rejected_or_deferred_burden_classes_frozen": REJECTED_OR_DEFERRED,
        "authorizes_fix_candidate_count": 1,
        "authorized_fix_candidate_id": AUTHORIZED_FIX_CANDIDATE_ID,
        "authorized_fix_candidate_kind": AUTHORIZED_FIX_CANDIDATE_KIND,
        "authorizes_patch_application": False,
        "authorizes_code_change_now": False,
        "authorizes_receipt_deletion": False,
        "authorizes_receipt_compression": False,
        "authorizes_raw_receipt_write_suppression": False,
        "authorizes_registry_sqlite_total_mismatch": False,
        "authorizes_execution_skipping": False,
        "authorizes_synthetic_receipts": False,
        "gate": policy["gate"],
        "terminal": policy["terminal"],
        "failures": failures,
        "warnings": warnings,
        "created_at": now_iso(),
    }

    rsig = stable_sig(receipt)
    receipt["receipt_id"] = rsig
    receipt["receipt_sig8"] = rsig

    (POLICY_DIR / f"{sig}.json").write_text(json.dumps(policy, indent=2, sort_keys=True))
    (RECEIPT_DIR / f"{sig}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return policy, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decision", default=EXPECTED_NEXT_DECISION_ID)
    args = parser.parse_args()

    policy, receipt = build_policy(args.decision)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_json_path=data/receipt_volume_fix_candidate_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/receipt_volume_fix_candidate_policy_receipts/{policy['policy_id']}.json")

    return 0 if policy["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
