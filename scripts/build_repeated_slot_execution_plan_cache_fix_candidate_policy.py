#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

DECISION_DIR = ROOT / "data" / "db_write_fix_outcome_decisions"
PROFILE_DIR = ROOT / "data" / "micro_burden_profiles"

POLICY_DIR = ROOT / "data" / "repeated_slot_execution_plan_cache_fix_candidate_policies"
RECEIPT_DIR = ROOT / "data" / "repeated_slot_execution_plan_cache_fix_candidate_policy_receipts"

EXPECTED_DECISION_ID = "811e147b"
EXPECTED_AFTER_PROFILE_ID = "00a75664"
EXPECTED_TARGET_BURDEN_CLASS = "BURDEN_REPEATED_SLOT_WORK"
EXPECTED_NEXT_GOAL = "BUILD_REPEATED_SLOT_EXECUTION_PLAN_CACHE_FIX_CANDIDATE_POLICY_V0"

FIX_CANDIDATE_ID = "FIX_CANDIDATE_REPEATED_SLOT_EXECUTION_PLAN_CACHE_V0"
FIX_CANDIDATE_KIND = "REPEATED_SLOT_EXECUTION_PLAN_CACHE_PROPOSAL"
NEXT_COMMAND_GOAL = "BUILD_REPEATED_SLOT_EXECUTION_PLAN_CACHE_FIX_CANDIDATE_V0"

EXPECTED_REPEATED_SLOTS = [
    "slot_01_E1",
    "slot_02_E2",
    "slot_03_E3",
    "slot_04_D1",
    "slot_05_D2",
    "slot_06_B1",
    "slot_07_B2",
    "slot_08_C1",
    "slot_09_A1",
]


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


def verify_sources(decision: dict[str, Any], after_profile: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if decision.get("decision_id") != EXPECTED_DECISION_ID:
        failures.append(f"decision_id_mismatch:{decision.get('decision_id')}")
    if decision.get("decision_id") != decision.get("decision_sig8"):
        failures.append("decision_sig_mismatch")
    if decision.get("gate") != "PASS":
        failures.append("decision_gate_not_PASS")
    if decision.get("db_write_fix_outcome") != "ACCEPT_DB_WRITE_WAL_WRAPPER_FIX":
        failures.append(f"db_write_fix_not_accepted:{decision.get('db_write_fix_outcome')}")
    if decision.get("after_profile_id") != EXPECTED_AFTER_PROFILE_ID:
        failures.append(f"decision_after_profile_id_mismatch:{decision.get('after_profile_id')}")
    if decision.get("target_burden_class") != "BURDEN_DB_WRITE":
        failures.append(f"decision_prior_target_not_DB_WRITE:{decision.get('target_burden_class')}")

    auth = decision.get("authorization") or {}
    if auth.get("authorizes_next_burden_policy") is not True:
        failures.append("decision_does_not_authorize_next_burden_policy")
    if auth.get("next_burden_class") != EXPECTED_TARGET_BURDEN_CLASS:
        failures.append(f"decision_next_burden_class_mismatch:{auth.get('next_burden_class')}")
    if auth.get("authorizes_radius_expansion") is not False:
        failures.append("decision_illegally_authorizes_radius_expansion")
    if auth.get("authorizes_batching_patch") is not False:
        failures.append("decision_illegally_authorizes_batching_patch")
    if auth.get("authorizes_more_db_write_patch") is not False:
        failures.append("decision_illegally_authorizes_more_db_write_patch")

    terminal = decision.get("terminal") or {}
    if terminal.get("next_command_goal") != EXPECTED_NEXT_GOAL:
        failures.append(f"decision_next_goal_mismatch:{terminal.get('next_command_goal')}")

    required_next_gate = decision.get("required_next_gate") or {}
    if required_next_gate.get("next_policy_must_use_after_profile_id") != EXPECTED_AFTER_PROFILE_ID:
        failures.append("required_next_gate_after_profile_mismatch")
    if required_next_gate.get("next_policy_must_target_selected_burden_class") != EXPECTED_TARGET_BURDEN_CLASS:
        failures.append("required_next_gate_target_mismatch")
    if required_next_gate.get("next_policy_must_authorize_exactly_one_fix_candidate") is not True:
        failures.append("required_next_gate_exactly_one_missing")
    if required_next_gate.get("next_policy_must_not_authorize_patch_application") is not True:
        failures.append("required_next_gate_no_patch_missing")
    if required_next_gate.get("next_policy_must_not_authorize_radius_expansion") is not True:
        failures.append("required_next_gate_no_radius_missing")
    if required_next_gate.get("next_policy_must_preserve_raw_receipts") is not True:
        failures.append("required_next_gate_preserve_raw_receipts_missing")

    if after_profile.get("profile_id") != EXPECTED_AFTER_PROFILE_ID:
        failures.append(f"after_profile_id_mismatch:{after_profile.get('profile_id')}")
    if after_profile.get("gate") != "MICRO_BURDEN_PROFILE_PASS":
        failures.append("after_profile_gate_not_MICRO_BURDEN_PROFILE_PASS")
    if after_profile.get("profile_receipts_total") != after_profile.get("db_receipt_delta"):
        failures.append("after_profile_receipt_total_mismatch_registry")
    if after_profile.get("families_seen") != ["A", "B", "C", "D", "E"]:
        failures.append("after_profile_family_coverage_not_A_E")
    if EXPECTED_TARGET_BURDEN_CLASS not in (after_profile.get("non_unknown_burden_classes") or []):
        failures.append("target_burden_class_not_emitted_by_after_profile")

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

    return failures


def summarize_target(after_profile: dict[str, Any]) -> dict[str, Any]:
    rows = [
        row for row in (after_profile.get("rows") or [])
        if row.get("burden_class") == EXPECTED_TARGET_BURDEN_CLASS
    ]

    families = sorted({row.get("family_compact") for row in rows if row.get("family_compact")})
    probes = sorted({row.get("probe_id") for row in rows if row.get("probe_id")})
    slots = [row.get("slot_id") for row in rows if row.get("slot_id")]

    receipts = sum(int(row.get("receipts") or 0) for row in rows)
    elapsed_ms = sum(int(row.get("elapsed_ms") or 0) for row in rows)

    return {
        "burden_class": EXPECTED_TARGET_BURDEN_CLASS,
        "rows": len(rows),
        "receipts": receipts,
        "elapsed_ms": elapsed_ms,
        "receipts_per_sec": round(receipts / (elapsed_ms / 1000.0), 6) if elapsed_ms > 0 else None,
        "families": families,
        "probes": probes,
        "slots": slots,
        "slot_identity_expected": EXPECTED_REPEATED_SLOTS,
        "slot_identity_matches_expected": slots == EXPECTED_REPEATED_SLOTS,
        "rows_detail": rows,
    }


def build_policy(decision_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    POLICY_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    decision = load_json(DECISION_DIR / f"{decision_id}.json")
    after_profile = load_json(PROFILE_DIR / f"{EXPECTED_AFTER_PROFILE_ID}.json")

    failures = verify_sources(decision, after_profile)
    warnings: list[str] = []

    target_evidence = summarize_target(after_profile)

    if target_evidence["rows"] != 9:
        failures.append(f"repeated_slot_target_rows_not_9:{target_evidence['rows']}")
    if target_evidence["slot_identity_matches_expected"] is not True:
        failures.append(f"repeated_slot_identity_mismatch:{target_evidence['slots']}")
    if target_evidence["probes"] != ["MICRO_04_REPEATED_SLOT_PRESSURE"]:
        failures.append(f"repeated_slot_probe_mismatch:{target_evidence['probes']}")
    if target_evidence["receipts"] <= 0:
        failures.append("target_receipts_zero")
    if target_evidence["elapsed_ms"] <= 0:
        failures.append("target_elapsed_ms_zero")

    policy = {
        "schema_version": "repeated_slot_execution_plan_cache_fix_candidate_policy_v0",
        "policy_kind": "REPEATED_SLOT_EXECUTION_PLAN_CACHE_FIX_CANDIDATE_POLICY",
        "purpose": "Authorize exactly one repeated-slot plan-cache fix candidate proposal from the after-profile burden class.",
        "source_decision": {
            "decision_id": decision.get("decision_id"),
            "decision_sig8": decision.get("decision_sig8"),
            "gate": decision.get("gate"),
            "path": f"data/db_write_fix_outcome_decisions/{decision_id}.json",
        },
        "source_after_profile": {
            "profile_id": after_profile.get("profile_id"),
            "profile_sig8": after_profile.get("profile_sig8"),
            "gate": after_profile.get("gate"),
            "profile_receipts_total": after_profile.get("profile_receipts_total"),
            "db_receipt_delta": after_profile.get("db_receipt_delta"),
        },
        "target_burden_class": EXPECTED_TARGET_BURDEN_CLASS,
        "target_burden_class_proven": EXPECTED_TARGET_BURDEN_CLASS in (after_profile.get("non_unknown_burden_classes") or []),
        "target_evidence": target_evidence,
        "authorization": {
            "authorizes_fix_candidate_count": 1,
            "authorizes_fix_candidate_ids": [FIX_CANDIDATE_ID],
            "authorizes_fix_candidate_kind": FIX_CANDIDATE_KIND,
            "authorizes_patch_application": False,
            "authorizes_code_change": False,
            "authorizes_runner_semantics_change": False,
            "authorizes_gate_semantics_change": False,
            "authorizes_law_semantics_change": False,
            "authorizes_receipt_schema_change": False,
            "authorizes_receipt_deletion": False,
            "authorizes_receipt_compression": False,
            "authorizes_execution_skipping": False,
            "authorizes_reusing_prior_run_results_as_execution": False,
            "authorizes_slot_identity_collapse": False,
            "authorizes_radius_expansion": False,
        },
        "authorized_fix_candidate": {
            "fix_candidate_id": FIX_CANDIDATE_ID,
            "fix_candidate_kind": FIX_CANDIDATE_KIND,
            "target_burden_class": EXPECTED_TARGET_BURDEN_CLASS,
            "allowed_scope": [
                "Cache repeated-slot execution plan construction only.",
                "Reuse immutable per-family/per-slot metadata only if slot identity remains explicit.",
                "Preserve one run execution per repeated slot.",
                "Preserve one run_id per slot.",
                "Preserve slot_id fields and distinguishability.",
                "Preserve raw receipt writes.",
            ],
            "forbidden_scope": [
                "skip repeated slot execution",
                "reuse prior run results as execution results",
                "collapse repeated E/E/E or D/D or B/B slots",
                "merge slot receipts",
                "delete receipts",
                "compress raw receipts",
                "change law semantics",
                "change gate semantics",
                "change run semantics",
                "change halt semantics",
                "expand radius",
            ],
            "expected_metric_direction": {
                "primary_metric": "elapsed_ms",
                "secondary_metric": "receipts_per_sec",
                "target_rows": "rows with burden_class == BURDEN_REPEATED_SLOT_WORK",
                "expected_elapsed_ms": "decrease_or_non_worse",
                "expected_receipts_per_sec": "increase_or_non_worse",
                "must_preserve_rows": 9,
                "must_preserve_slots": EXPECTED_REPEATED_SLOTS,
                "must_preserve_receipt_total_match_registry": True,
                "must_preserve_family_coverage_A_E": True,
            },
            "next_command_goal": NEXT_COMMAND_GOAL,
        },
        "required_retest": {
            "before_profile_id": EXPECTED_AFTER_PROFILE_ID,
            "after_profile_required": True,
            "same_micro_suite_required": True,
            "same_probe_specs_required": True,
            "same_script": "scripts/wide_burden_profile_microruns.py --execute",
            "comparison_required": True,
            "comparison_artifact_schema": "repeated_slot_plan_cache_before_after_comparison_v0",
            "pass_condition": [
                "after profile gate MICRO_BURDEN_PROFILE_PASS",
                "receipt totals match registry.sqlite",
                "all five probes complete",
                "family coverage A-E preserved",
                "repeated slot identity preserved exactly",
                "same repeated-slot row keys preserved",
                "no gate semantics change",
                "no law semantics change",
                "no run semantics change",
                "no execution skipping",
                "BURDEN_REPEATED_SLOT_WORK target rows show non-worse elapsed_ms or explicit failure classification",
            ],
        },
        "policy_gate": {
            "source_decision_pass": decision.get("gate") == "PASS",
            "source_after_profile_pass": after_profile.get("gate") == "MICRO_BURDEN_PROFILE_PASS",
            "target_class_emitted": EXPECTED_TARGET_BURDEN_CLASS in (after_profile.get("non_unknown_burden_classes") or []),
            "slot_identity_distinguishable": target_evidence["slot_identity_matches_expected"],
            "authorizes_exactly_one_fix_candidate": True,
            "does_not_authorize_patch_application": True,
            "does_not_authorize_radius_expansion": True,
            "does_not_authorize_execution_skipping": True,
            "does_not_authorize_slot_identity_collapse": True,
            "preserves_raw_receipts": True,
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_REPEATED_SLOT_POLICY_INVALID",
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "PASS" if not failures else "FAIL",
        "created_at": now_iso(),
    }

    sig = stable_sig(policy)
    policy["policy_id"] = sig
    policy["policy_sig8"] = sig

    receipt = {
        "schema_version": "repeated_slot_execution_plan_cache_fix_candidate_policy_receipt_v0",
        "policy_id": sig,
        "policy_path": f"data/repeated_slot_execution_plan_cache_fix_candidate_policies/{sig}.json",
        "policy_sig8": sig,
        "source_decision_id": decision_id,
        "source_after_profile_id": EXPECTED_AFTER_PROFILE_ID,
        "target_burden_class": EXPECTED_TARGET_BURDEN_CLASS,
        "target_rows": target_evidence["rows"],
        "target_receipts": target_evidence["receipts"],
        "target_elapsed_ms": target_evidence["elapsed_ms"],
        "slot_identity_matches_expected": target_evidence["slot_identity_matches_expected"],
        "authorized_fix_candidate_ids": policy["authorization"]["authorizes_fix_candidate_ids"],
        "authorizes_patch_application": False,
        "authorizes_execution_skipping": False,
        "authorizes_slot_identity_collapse": False,
        "authorizes_radius_expansion": False,
        "gate": policy["gate"],
        "terminal": policy["terminal"],
        "failures": failures,
        "warnings": warnings,
        "created_at": now_iso(),
    }

    receipt_sig = stable_sig(receipt)
    receipt["receipt_id"] = receipt_sig
    receipt["receipt_sig8"] = receipt_sig

    (POLICY_DIR / f"{sig}.json").write_text(json.dumps(policy, indent=2, sort_keys=True))
    (RECEIPT_DIR / f"{sig}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return policy, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decision", default=EXPECTED_DECISION_ID)
    args = parser.parse_args()

    policy, receipt = build_policy(args.decision)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_json_path=data/repeated_slot_execution_plan_cache_fix_candidate_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/repeated_slot_execution_plan_cache_fix_candidate_policy_receipts/{policy['policy_id']}.json")

    return 0 if policy["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
