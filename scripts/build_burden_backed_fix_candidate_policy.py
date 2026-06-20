#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import hashlib
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROFILE_DIR = ROOT / "data" / "micro_burden_profiles"
POLICY_DIR = ROOT / "data" / "burden_backed_fix_candidate_policies"
RECEIPT_DIR = ROOT / "data" / "burden_backed_fix_candidate_policy_receipts"

ALLOWED_BURDEN_CLASSES = {
    "BURDEN_UNKNOWN",
    "BURDEN_DEPTH_SCAN",
    "BURDEN_CYCLE_SCAN",
    "BURDEN_REPEATED_SLOT_WORK",
    "BURDEN_RECEIPT_VOLUME",
    "BURDEN_DB_WRITE",
    "BURDEN_PROGRESS_LOGGING",
    "BURDEN_MATRIX_BUILD",
    "BURDEN_LAW_CHECK",
    "BURDEN_GATE_OVERHEAD",
    "BURDEN_MATRIX_BOUNDARY",
}

FIX_CANDIDATE_MAP = {
    "BURDEN_DB_WRITE": {
        "fix_candidate_id": "FIX_CANDIDATE_DB_WRITE_WAL_BATCHED_RECEIPT_WRITE_V0",
        "fix_candidate_kind": "DB_WRITE_WAL_BATCHED_RECEIPT_WRITE_PROPOSAL",
        "next_command_goal": "BUILD_DB_WRITE_WAL_BATCHED_RECEIPT_WRITE_FIX_CANDIDATE_V0",
        "allowed_scope": [
            "SQLite WAL mode proposal",
            "transaction batching proposal",
            "write-path timing instrumentation preservation",
            "no receipt schema compression",
            "no receipt deletion",
        ],
        "forbidden_scope": [
            "skip receipt writes",
            "delete receipt rows",
            "change receipt content",
            "change law semantics",
            "change gate semantics",
            "change run semantics",
            "representative subset execution",
        ],
        "required_before_apply": [
            "candidate patch plan",
            "before profile c89790f0 remains archived",
            "same micro suite rerun after candidate",
            "before_after_micro_profile_comparison",
            "receipt totals must still match registry.sqlite",
        ],
    },
    "BURDEN_PROGRESS_LOGGING": {
        "fix_candidate_id": "FIX_CANDIDATE_PROGRESS_LOGGING_THROTTLE_V0",
        "fix_candidate_kind": "PROGRESS_LOGGING_THROTTLE_PROPOSAL",
        "next_command_goal": "BUILD_PROGRESS_LOGGING_THROTTLE_FIX_CANDIDATE_V0",
        "allowed_scope": [
            "stderr progress throttling proposal",
            "does not change receipt generation",
            "does not change DB writes",
        ],
        "forbidden_scope": [
            "hide gate failures",
            "skip execution",
            "change run semantics",
            "delete receipts",
        ],
        "required_before_apply": [
            "candidate patch plan",
            "same micro suite rerun after candidate",
            "before_after_micro_profile_comparison",
        ],
    },
    "BURDEN_RECEIPT_VOLUME": {
        "fix_candidate_id": "FIX_CANDIDATE_RECEIPT_VOLUME_INDEXED_ROLLUP_VIEW_V0",
        "fix_candidate_kind": "RECEIPT_VOLUME_INDEXED_ROLLUP_VIEW_PROPOSAL",
        "next_command_goal": "BUILD_RECEIPT_VOLUME_ROLLUP_VIEW_FIX_CANDIDATE_V0",
        "allowed_scope": [
            "read-side rollup/index proposal",
            "operator-view compression only",
            "raw receipts remain authoritative",
        ],
        "forbidden_scope": [
            "compress raw receipts",
            "delete raw receipts",
            "skip receipt generation",
            "change gate semantics",
        ],
        "required_before_apply": [
            "candidate patch plan",
            "same micro suite rerun after candidate",
            "before_after_micro_profile_comparison",
        ],
    },
    "BURDEN_DEPTH_SCAN": {
        "fix_candidate_id": "FIX_CANDIDATE_FRONTIER_DEPTH_PROBE_POLICY_V0",
        "fix_candidate_kind": "FRONTIER_DEPTH_PROBE_PROPOSAL",
        "next_command_goal": "BUILD_FRONTIER_DEPTH_PROBE_FIX_CANDIDATE_V0",
        "allowed_scope": [
            "future-run depth frontier policy proposal",
            "must not alter current micro probe semantics",
        ],
        "forbidden_scope": [
            "skip current required probes",
            "change law semantics",
            "change gate semantics",
            "delete receipts",
        ],
        "required_before_apply": [
            "candidate patch plan",
            "same micro suite rerun after candidate",
            "before_after_micro_profile_comparison",
        ],
    },
    "BURDEN_CYCLE_SCAN": {
        "fix_candidate_id": "FIX_CANDIDATE_CYCLE_PERIOD_COMPRESSION_POLICY_V0",
        "fix_candidate_kind": "CYCLE_PERIOD_COMPRESSION_PROPOSAL",
        "next_command_goal": "BUILD_CYCLE_PERIOD_COMPRESSION_FIX_CANDIDATE_V0",
        "allowed_scope": [
            "period detection proposal",
            "future-run cycle-bound policy proposal",
        ],
        "forbidden_scope": [
            "skip current required probes",
            "change halt semantics",
            "change law semantics",
            "change gate semantics",
            "delete receipts",
        ],
        "required_before_apply": [
            "candidate patch plan",
            "same micro suite rerun after candidate",
            "before_after_micro_profile_comparison",
        ],
    },
    "BURDEN_REPEATED_SLOT_WORK": {
        "fix_candidate_id": "FIX_CANDIDATE_REPEATED_SLOT_EXECUTION_PLAN_CACHE_V0",
        "fix_candidate_kind": "REPEATED_SLOT_EXECUTION_PLAN_CACHE_PROPOSAL",
        "next_command_goal": "BUILD_REPEATED_SLOT_EXECUTION_PLAN_CACHE_FIX_CANDIDATE_V0",
        "allowed_scope": [
            "slot plan construction cache proposal",
            "identity-preserving repeated slot metadata reuse proposal",
        ],
        "forbidden_scope": [
            "skip repeated slot execution",
            "reuse run results as execution results",
            "collapse slot identity",
            "delete receipts",
            "change run semantics",
        ],
        "required_before_apply": [
            "candidate patch plan",
            "same micro suite rerun after candidate",
            "before_after_micro_profile_comparison",
        ],
    },
}

SAFE_PRIORITY = [
    "BURDEN_DB_WRITE",
    "BURDEN_PROGRESS_LOGGING",
    "BURDEN_RECEIPT_VOLUME",
    "BURDEN_DEPTH_SCAN",
    "BURDEN_CYCLE_SCAN",
    "BURDEN_REPEATED_SLOT_WORK",
    "BURDEN_MATRIX_BUILD",
    "BURDEN_LAW_CHECK",
    "BURDEN_GATE_OVERHEAD",
    "BURDEN_MATRIX_BOUNDARY",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_sig(obj: dict[str, Any]) -> str:
    body = dict(obj)
    for key in ("policy_id", "policy_sig8", "receipt_id", "receipt_sig8"):
        body.pop(key, None)
    blob = json.dumps(body, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:8]


def latest_profile_id() -> str:
    paths = sorted(PROFILE_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not paths:
        raise SystemExit("no micro burden profiles found")
    return paths[0].stem


def load_profile(profile_id: str) -> tuple[Path, dict[str, Any]]:
    path = PROFILE_DIR / f"{profile_id}.json"
    if not path.exists():
        raise SystemExit(f"profile not found: {path}")
    return path, json.loads(path.read_text())


def burden_totals(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    totals: dict[str, dict[str, Any]] = {}
    for row in rows:
        cls = row.get("burden_class") or "BURDEN_UNKNOWN"
        if cls not in totals:
            totals[cls] = {
                "burden_class": cls,
                "rows": 0,
                "receipts": 0,
                "elapsed_ms": 0,
                "families": set(),
                "probes": set(),
                "slots": set(),
            }
        item = totals[cls]
        item["rows"] += 1
        item["receipts"] += int(row.get("receipts") or 0)
        item["elapsed_ms"] += int(row.get("elapsed_ms") or 0)
        if row.get("family_compact"):
            item["families"].add(row.get("family_compact"))
        if row.get("probe_id"):
            item["probes"].add(row.get("probe_id"))
        if row.get("slot_id"):
            item["slots"].add(row.get("slot_id"))

    out: dict[str, dict[str, Any]] = {}
    for cls, item in totals.items():
        elapsed = int(item["elapsed_ms"])
        receipts = int(item["receipts"])
        out[cls] = {
            "burden_class": cls,
            "rows": item["rows"],
            "receipts": receipts,
            "elapsed_ms": elapsed,
            "receipts_per_sec": round(receipts / (elapsed / 1000.0), 6) if elapsed > 0 else None,
            "families": sorted(item["families"]),
            "probes": sorted(item["probes"]),
            "slots": sorted(item["slots"]),
        }
    return out


def choose_target(non_unknown: list[str], totals: dict[str, dict[str, Any]]) -> tuple[str | None, str]:
    emitted = set(non_unknown)
    for cls in SAFE_PRIORITY:
        if cls in emitted and cls in FIX_CANDIDATE_MAP:
            return cls, "SAFE_INFRA_PRIORITY_FIRST_MATCH"
    if non_unknown:
        ranked = sorted(non_unknown, key=lambda c: int(totals.get(c, {}).get("elapsed_ms") or 0), reverse=True)
        return ranked[0], "FALLBACK_MAX_ELAPSED"
    return None, "NO_NON_UNKNOWN_BURDEN_CLASS"


def verify_source_profile(profile: dict[str, Any]) -> list[str]:
    failures = []
    if profile.get("gate") != "MICRO_BURDEN_PROFILE_PASS":
        failures.append("source_profile_gate_not_MICRO_BURDEN_PROFILE_PASS")
    if profile.get("profile_id") != profile.get("profile_sig8"):
        failures.append("source_profile_sig_mismatch")
    if not profile.get("rows"):
        failures.append("source_profile_rows_missing")
    if profile.get("profile_receipts_total") != profile.get("db_receipt_delta"):
        failures.append("source_profile_receipt_total_mismatch")
    if profile.get("families_seen") != ["A", "B", "C", "D", "E"]:
        failures.append("source_profile_missing_family_A_E")
    if not profile.get("non_unknown_burden_classes"):
        failures.append("source_profile_no_non_unknown_burden_classes")
    aggs = profile.get("aggregates") or {}
    if not aggs.get("top_20_time_sources"):
        failures.append("source_profile_top_20_time_sources_missing")
    if not aggs.get("top_20_receipt_sources"):
        failures.append("source_profile_top_20_receipt_sources_missing")

    semantics = profile.get("semantics") or {}
    if semantics.get("runner_semantics_changed") is not False:
        failures.append("source_profile_runner_semantics_changed")
    if semantics.get("gate_semantics_changed") is not False:
        failures.append("source_profile_gate_semantics_changed")
    if semantics.get("law_semantics_changed") is not False:
        failures.append("source_profile_law_semantics_changed")
    if semantics.get("receipt_rows_deleted") is not False:
        failures.append("source_profile_receipt_rows_deleted")
    if semantics.get("execution_skipped") is not False:
        failures.append("source_profile_execution_skipped")
    return failures


def build_policy(profile_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    POLICY_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    profile_path, profile = load_profile(profile_id)
    failures = verify_source_profile(profile)
    warnings: list[str] = []

    rows = profile.get("rows") or []
    totals = burden_totals(rows)
    non_unknown = [c for c in profile.get("non_unknown_burden_classes") or [] if c != "BURDEN_UNKNOWN"]
    for cls in non_unknown:
        if cls not in ALLOWED_BURDEN_CLASSES:
            failures.append(f"source_profile_invalid_burden_class:{cls}")

    target_class, selection_rule = choose_target(non_unknown, totals)

    if not target_class:
        failures.append("no_fix_authorizable_without_non_unknown_burden_class")
        fix_candidate = None
    elif target_class not in non_unknown:
        failures.append(f"target_class_not_emitted:{target_class}")
        fix_candidate = None
    elif target_class not in FIX_CANDIDATE_MAP:
        failures.append(f"no_fix_candidate_mapping_for_target_class:{target_class}")
        fix_candidate = None
    else:
        fix_candidate = dict(FIX_CANDIDATE_MAP[target_class])

    authorized_fix_candidates = [fix_candidate] if fix_candidate else []
    if len(authorized_fix_candidates) != 1:
        failures.append(f"authorized_fix_candidate_count_not_one:{len(authorized_fix_candidates)}")

    if target_class and target_class not in non_unknown:
        failures.append("fix_target_not_proven_by_micro_profile")

    policy = {
        "schema_version": "burden_backed_fix_candidate_policy_v0",
        "policy_kind": "BURDEN_BACKED_FIX_CANDIDATE_POLICY",
        "purpose": "Authorize exactly one fix-candidate proposal from an explicit micro-profile burden class.",
        "source_profile": {
            "profile_id": profile.get("profile_id"),
            "profile_path": str(profile_path.relative_to(ROOT)),
            "profile_sig8": profile.get("profile_sig8"),
            "gate": profile.get("gate"),
            "profile_receipts_total": profile.get("profile_receipts_total"),
            "db_receipt_delta": profile.get("db_receipt_delta"),
        },
        "source_profile_burden_classes": profile.get("non_unknown_burden_classes") or [],
        "burden_class_totals": totals,
        "target_burden_class": target_class,
        "target_burden_class_proven": target_class in non_unknown if target_class else False,
        "selection_rule": selection_rule,
        "authorization": {
            "authorizes_fix_candidate_count": len(authorized_fix_candidates),
            "authorizes_fix_candidate_ids": [
                c["fix_candidate_id"] for c in authorized_fix_candidates
            ],
            "authorizes_apply_patch": False,
            "authorizes_code_change": False,
            "authorizes_runner_semantics_change": False,
            "authorizes_gate_semantics_change": False,
            "authorizes_law_semantics_change": False,
            "authorizes_receipt_deletion": False,
            "authorizes_receipt_compression": False,
            "authorizes_execution_skipping": False,
            "authorizes_radius_expansion": False,
            "authorizes_R125_or_larger": False,
        },
        "authorized_fix_candidates": authorized_fix_candidates,
        "required_retest": {
            "same_micro_suite_required": True,
            "same_probe_specs_required": True,
            "same_script": "scripts/wide_burden_profile_microruns.py --execute",
            "before_profile_id": profile.get("profile_id"),
            "after_profile_required": True,
            "before_after_comparison_required": True,
            "receipt_total_match_registry_required": True,
            "no_semantic_or_gate_change_required": True,
        },
        "fix_gate": {
            "candidate_must_target_target_burden_class": True,
            "candidate_must_not_apply_patch_yet": True,
            "candidate_must_emit_patch_plan": True,
            "candidate_must_emit_expected_metric_direction": True,
            "candidate_must_emit_retest_command": True,
            "candidate_must_fail_closed_if_semantics_change": True,
        },
        "allowed_next_actions": [
            "build exactly one fix-candidate proposal",
            "inspect candidate patch plan",
            "optionally apply only that candidate after explicit command",
            "rerun same micro suite",
            "compare before/after micro profiles",
        ],
        "forbidden_next_actions": [
            "apply optimization without candidate policy",
            "run larger radius",
            "skip execution",
            "delete receipts",
            "compress raw receipts",
            "change law semantics",
            "change gate semantics",
            "change run semantics",
            "authorize multiple fixes at once",
            "diagnose outside emitted burden classes",
        ],
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": fix_candidate["next_command_goal"] if fix_candidate and not failures else None,
            "stop_code": None if not failures else "STOP_BURDEN_BACKED_FIX_CANDIDATE_POLICY_INVALID",
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
        "schema_version": "burden_backed_fix_candidate_policy_receipt_v0",
        "policy_id": sig,
        "policy_path": f"data/burden_backed_fix_candidate_policies/{sig}.json",
        "policy_sig8": sig,
        "source_profile_id": profile.get("profile_id"),
        "source_profile_gate": profile.get("gate"),
        "gate": policy["gate"],
        "target_burden_class": target_class,
        "selection_rule": selection_rule,
        "authorized_fix_candidate_ids": policy["authorization"]["authorizes_fix_candidate_ids"],
        "authorizes_fix_candidate_count": policy["authorization"]["authorizes_fix_candidate_count"],
        "authorizes_apply_patch": policy["authorization"]["authorizes_apply_patch"],
        "authorizes_radius_expansion": policy["authorization"]["authorizes_radius_expansion"],
        "terminal": policy["terminal"],
        "failures": failures,
        "warnings": warnings,
        "created_at": now_iso(),
    }
    receipt_sig = stable_sig(receipt)
    receipt["receipt_id"] = receipt_sig
    receipt["receipt_sig8"] = receipt_sig

    policy_path = POLICY_DIR / f"{sig}.json"
    receipt_path = RECEIPT_DIR / f"{sig}.json"

    policy_path.write_text(json.dumps(policy, indent=2, sort_keys=True))
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return policy, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default=None, help="Micro burden profile id. Defaults to latest profile.")
    args = parser.parse_args()

    profile_id = args.profile or latest_profile_id()
    policy, receipt = build_policy(profile_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_json_path=data/burden_backed_fix_candidate_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/burden_backed_fix_candidate_policy_receipts/{policy['policy_id']}.json")

    return 0 if policy["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
