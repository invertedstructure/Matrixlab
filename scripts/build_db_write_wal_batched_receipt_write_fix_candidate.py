#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY_DIR = ROOT / "data" / "burden_backed_fix_candidate_policies"
CANDIDATE_DIR = ROOT / "data" / "db_write_wal_batched_receipt_write_fix_candidates"
RECEIPT_DIR = ROOT / "data" / "db_write_wal_batched_receipt_write_fix_candidate_receipts"

EXPECTED_POLICY_ID = "e8880c58"
EXPECTED_SOURCE_PROFILE_ID = "c89790f0"
EXPECTED_TARGET_BURDEN_CLASS = "BURDEN_DB_WRITE"
EXPECTED_FIX_CANDIDATE_ID = "FIX_CANDIDATE_DB_WRITE_WAL_BATCHED_RECEIPT_WRITE_V0"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_sig(obj: dict[str, Any]) -> str:
    body = dict(obj)
    for key in ("candidate_id", "candidate_sig8", "receipt_id", "receipt_sig8"):
        body.pop(key, None)
    blob = json.dumps(body, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:8]


def load_policy(policy_id: str) -> tuple[Path, dict[str, Any]]:
    path = POLICY_DIR / f"{policy_id}.json"
    if not path.exists():
        raise SystemExit(f"policy not found: {path}")
    return path, json.loads(path.read_text())


def verify_policy(policy: dict[str, Any]) -> list[str]:
    failures = []
    auth = policy.get("authorization") or {}
    source = policy.get("source_profile") or {}
    candidate_ids = auth.get("authorizes_fix_candidate_ids") or []

    if policy.get("gate") != "PASS":
        failures.append("source_policy_gate_not_PASS")
    if policy.get("policy_id") != policy.get("policy_sig8"):
        failures.append("source_policy_sig_mismatch")
    if source.get("profile_id") != EXPECTED_SOURCE_PROFILE_ID:
        failures.append(f"source_profile_not_expected:{source.get('profile_id')}")
    if source.get("gate") != "MICRO_BURDEN_PROFILE_PASS":
        failures.append("source_profile_gate_not_MICRO_BURDEN_PROFILE_PASS")
    if policy.get("target_burden_class") != EXPECTED_TARGET_BURDEN_CLASS:
        failures.append(f"target_burden_class_not_DB_WRITE:{policy.get('target_burden_class')}")
    if policy.get("target_burden_class_proven") is not True:
        failures.append("target_burden_class_not_proven")
    if auth.get("authorizes_fix_candidate_count") != 1:
        failures.append(f"authorizes_fix_candidate_count_not_one:{auth.get('authorizes_fix_candidate_count')}")
    if candidate_ids != [EXPECTED_FIX_CANDIDATE_ID]:
        failures.append(f"wrong_authorized_fix_candidate_ids:{candidate_ids}")

    forbidden_true = [
        "authorizes_apply_patch",
        "authorizes_code_change",
        "authorizes_runner_semantics_change",
        "authorizes_gate_semantics_change",
        "authorizes_law_semantics_change",
        "authorizes_receipt_deletion",
        "authorizes_receipt_compression",
        "authorizes_execution_skipping",
        "authorizes_radius_expansion",
        "authorizes_R125_or_larger",
    ]
    for key in forbidden_true:
        if auth.get(key) is not False:
            failures.append(f"illegal_policy_authorization:{key}:{auth.get(key)}")

    return failures


def build_candidate(policy_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    CANDIDATE_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    policy_path, policy = load_policy(policy_id)
    failures = verify_policy(policy)
    warnings: list[str] = []

    target_total = (policy.get("burden_class_totals") or {}).get(EXPECTED_TARGET_BURDEN_CLASS) or {}

    candidate = {
        "schema_version": "db_write_wal_batched_receipt_write_fix_candidate_v0",
        "candidate_kind": "DB_WRITE_WAL_BATCHED_RECEIPT_WRITE_FIX_CANDIDATE",
        "candidate_name": EXPECTED_FIX_CANDIDATE_ID,
        "source_policy": {
            "policy_id": policy.get("policy_id"),
            "policy_path": str(policy_path.relative_to(ROOT)),
            "policy_sig8": policy.get("policy_sig8"),
            "gate": policy.get("gate"),
        },
        "source_profile_id": EXPECTED_SOURCE_PROFILE_ID,
        "target_burden_class": EXPECTED_TARGET_BURDEN_CLASS,
        "target_burden_class_proven": policy.get("target_burden_class_proven") is True,
        "target_burden_evidence": target_total,
        "candidate_status": "PROPOSAL_ONLY_NOT_APPLIED",
        "authorization": {
            "authorizes_patch_application": False,
            "authorizes_runner_semantics_change": False,
            "authorizes_gate_semantics_change": False,
            "authorizes_law_semantics_change": False,
            "authorizes_receipt_schema_change": False,
            "authorizes_receipt_deletion": False,
            "authorizes_receipt_compression": False,
            "authorizes_execution_skipping": False,
            "authorizes_radius_expansion": False,
        },
        "patch_plan": {
            "plan_kind": "DB_WRITE_WAL_BATCHED_RECEIPT_WRITE_PATCH_PLAN",
            "files_allowed_to_touch_if_later_applied": [
                "src/matrixlab/cli.py",
                "or narrow DB writer module if writer exists",
            ],
            "intended_changes": [
                {
                    "change_id": "ENABLE_SQLITE_WAL_FOR_RUN_REGISTRY_CONNECTIONS",
                    "description": "Set PRAGMA journal_mode=WAL for registry.sqlite connections used by run/receipt writes, when supported.",
                    "expected_effect": "Reduce SQLite writer lock and fsync pressure during receipt-heavy micro runs.",
                    "semantic_constraint": "Must not change receipt rows, receipt fields, law results, halt reasons, run ids, gate results, or evaluator behavior.",
                },
                {
                    "change_id": "BATCH_RECEIPT_INSERTS_WITH_EXPLICIT_TRANSACTIONS",
                    "description": "Group receipt inserts into bounded explicit transactions instead of committing each row individually, if current writer commits per receipt.",
                    "expected_effect": "Reduce DB commit overhead while preserving full raw receipt insertion.",
                    "semantic_constraint": "Must write the same receipts, in a deterministic distinguishable order, with no skipped or compressed rows.",
                },
                {
                    "change_id": "PRESERVE_WRITE_PATH_TIMING_OBSERVABILITY",
                    "description": "Preserve micro-profile elapsed_ms and receipt total checks so the same probe suite can compare before/after.",
                    "expected_effect": "Keep burden observability intact for retest.",
                    "semantic_constraint": "Measurement layer only; no gate/law/run semantic changes.",
                },
            ],
            "bounded_transaction_policy": {
                "max_batch_size_receipts": 256,
                "flush_on_run_end": True,
                "flush_before_gate": True,
                "rollback_on_exception": True,
                "no_receipt_loss_allowed": True,
            },
            "wal_policy": {
                "enable_wal": True,
                "synchronous": "NORMAL",
                "fallback_if_pragma_unsupported": "continue_without_wal_and_emit_warning",
                "must_not_require_external_service": True,
            },
        },
        "expected_metric_direction": {
            "primary_metric": "elapsed_ms",
            "secondary_metric": "receipts_per_sec",
            "target_rows": "rows with burden_class == BURDEN_DB_WRITE",
            "expected_elapsed_ms": "decrease",
            "expected_receipts_per_sec": "increase",
            "must_preserve_profile_receipts_total_match_registry": True,
            "must_preserve_all_probe_completion": True,
            "must_preserve_family_coverage_A_E": True,
            "must_preserve_repeated_slot_identity": True,
        },
        "required_retest": {
            "before_profile_id": EXPECTED_SOURCE_PROFILE_ID,
            "after_profile_required": True,
            "same_micro_suite_required": True,
            "same_probe_specs_required": True,
            "same_script": "scripts/wide_burden_profile_microruns.py --execute",
            "comparison_required": True,
            "comparison_artifact_schema": "micro_burden_before_after_comparison_v0",
            "pass_condition": [
                "after profile gate MICRO_BURDEN_PROFILE_PASS",
                "receipt totals match registry.sqlite",
                "all five probes complete",
                "family coverage A-E preserved",
                "repeated slot identity preserved",
                "no gate semantics change",
                "no law semantics change",
                "no run semantics change",
                "DB_WRITE target rows show non-worse elapsed_ms or explicit failure classification",
            ],
        },
        "apply_gate": {
            "candidate_does_not_apply_itself": True,
            "must_be_followed_by_explicit_apply_command": True,
            "apply_command_goal_if_accepted": "APPLY_DB_WRITE_WAL_BATCHED_RECEIPT_WRITE_FIX_V0",
            "stop_if_patch_touches_forbidden_semantics": True,
            "stop_if_patch_deletes_receipts": True,
            "stop_if_patch_skips_execution": True,
            "stop_if_patch_changes_gate_or_law_semantics": True,
        },
        "forbidden": {
            "receipt_deletion": True,
            "receipt_compression": True,
            "receipt_schema_change": True,
            "execution_skipping": True,
            "representative_subset": True,
            "gate_semantics_change": True,
            "law_semantics_change": True,
            "run_semantics_change": True,
            "radius_expansion": True,
            "theorem_layer": True,
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": "APPLY_DB_WRITE_WAL_BATCHED_RECEIPT_WRITE_FIX_V0" if not failures else None,
            "stop_code": None if not failures else "STOP_DB_WRITE_FIX_CANDIDATE_INVALID",
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "PASS" if not failures else "FAIL",
        "created_at": now_iso(),
    }

    sig = stable_sig(candidate)
    candidate["candidate_id"] = sig
    candidate["candidate_sig8"] = sig

    receipt = {
        "schema_version": "db_write_wal_batched_receipt_write_fix_candidate_receipt_v0",
        "candidate_id": sig,
        "candidate_path": f"data/db_write_wal_batched_receipt_write_fix_candidates/{sig}.json",
        "candidate_sig8": sig,
        "candidate_name": EXPECTED_FIX_CANDIDATE_ID,
        "source_policy_id": policy.get("policy_id"),
        "source_profile_id": EXPECTED_SOURCE_PROFILE_ID,
        "target_burden_class": EXPECTED_TARGET_BURDEN_CLASS,
        "candidate_status": candidate["candidate_status"],
        "gate": candidate["gate"],
        "authorizes_patch_application": candidate["authorization"]["authorizes_patch_application"],
        "authorizes_radius_expansion": candidate["authorization"]["authorizes_radius_expansion"],
        "required_retest": candidate["required_retest"],
        "terminal": candidate["terminal"],
        "failures": failures,
        "warnings": warnings,
        "created_at": now_iso(),
    }

    receipt_sig = stable_sig(receipt)
    receipt["receipt_id"] = receipt_sig
    receipt["receipt_sig8"] = receipt_sig

    candidate_path = CANDIDATE_DIR / f"{sig}.json"
    receipt_path = RECEIPT_DIR / f"{sig}.json"

    candidate_path.write_text(json.dumps(candidate, indent=2, sort_keys=True))
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return candidate, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", default=EXPECTED_POLICY_ID)
    args = parser.parse_args()

    candidate, receipt = build_candidate(args.policy)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"candidate_json_path=data/db_write_wal_batched_receipt_write_fix_candidates/{candidate['candidate_id']}.json")
    print(f"candidate_receipt_path=data/db_write_wal_batched_receipt_write_fix_candidate_receipts/{candidate['candidate_id']}.json")

    return 0 if candidate["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
