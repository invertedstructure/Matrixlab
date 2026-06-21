#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

SOURCE_POLICY_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_scale_band_policies"
SOURCE_POLICY_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_scale_band_policy_receipts"
V02_PROBE_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_receipts"

OUT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_scale_band_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_scale_band_policy_receipts"

SOURCE_SCALE_BAND_POLICY_ID = "7d453433"
SOURCE_SCALE_BAND_POLICY_RECEIPT_ID = "b5841247"
V02_PROBE_ID = "bcdb3d93"
CANDIDATE_DESIGN_ID = "STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2"

POLICY_NAME = "BUILD_BOUNDED_SCALE_BAND_SELECTION_POLICY_V0"
BOUNDED_POLICY_NAME = "STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2_BOUNDED_SCALE_BAND_POLICY"
NEXT_COMMAND_GOAL = "IMPLEMENT_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2_SCALE_BAND_PROBE"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def blob(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")


def sha8(obj: Any) -> str:
    return hashlib.sha256(blob(obj)).hexdigest()[:8]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def verify_sources(source_policy: dict[str, Any], source_receipt: dict[str, Any], v02_probe: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if source_policy.get("policy_id") != SOURCE_SCALE_BAND_POLICY_ID:
        failures.append(f"source_policy_id_wrong:{source_policy.get('policy_id')}")
    if source_receipt.get("receipt_id") != SOURCE_SCALE_BAND_POLICY_RECEIPT_ID:
        failures.append(f"source_receipt_id_wrong:{source_receipt.get('receipt_id')}")
    if source_policy.get("gate") != "PASS":
        failures.append(f"source_policy_gate_not_PASS:{source_policy.get('gate')}")
    if source_receipt.get("gate") != "PASS":
        failures.append(f"source_receipt_gate_not_PASS:{source_receipt.get('gate')}")
    if source_policy.get("terminal", {}).get("next_command_goal") != NEXT_COMMAND_GOAL:
        failures.append(f"source_next_goal_wrong:{source_policy.get('terminal', {}).get('next_command_goal')}")

    auth = source_policy.get("authority") or {}
    if auth.get("authorizes_next_scale_band_probe_implementation") is not True:
        failures.append("source_policy_does_not_authorize_probe_implementation")
    if auth.get("authorizes_scale_band_probe_execution") is not True:
        failures.append("source_policy_does_not_authorize_probe_execution")
    for key in [
        "authorizes_scale_band_run",
        "authorizes_scale_mode",
        "authorizes_candidate_acceptance",
        "authorizes_registry_write",
        "authorizes_runtime_receipt_emission_change",
        "authorizes_receipt_replacement",
        "authorizes_receipt_deletion",
        "authorizes_receipt_compression",
        "authorizes_raw_receipt_hash_truth_surface",
    ]:
        if auth.get(key) is not False:
            failures.append(f"source_policy_illegal_authority:{key}:{auth.get(key)}")

    local = source_policy.get("local_pass_summary") or {}
    if local.get("terminal_decision") != "NEEDS_MORE_SCALE_AFTER_LOCAL_PASS":
        failures.append(f"local_terminal_wrong:{local.get('terminal_decision')}")
    if local.get("false_merge_count") != 0:
        failures.append(f"local_false_merge_not_zero:{local.get('false_merge_count')}")
    if local.get("distinguishability_retention_ratio") != 1.0:
        failures.append(f"local_retention_not_one:{local.get('distinguishability_retention_ratio')}")
    if local.get("burden_ratio_projected", 1.0) >= 1.0:
        failures.append(f"local_burden_not_reduced:{local.get('burden_ratio_projected')}")
    if local.get("scale_precondition") is not True:
        failures.append(f"local_scale_precondition_not_true:{local.get('scale_precondition')}")

    if v02_probe.get("probe_id") != V02_PROBE_ID:
        failures.append(f"v02_probe_id_wrong:{v02_probe.get('probe_id')}")
    if v02_probe.get("gate") != "PASS":
        failures.append(f"v02_probe_gate_not_PASS:{v02_probe.get('gate')}")
    if v02_probe.get("terminal_decision") != "NEEDS_MORE_SCALE_AFTER_LOCAL_PASS":
        failures.append(f"v02_probe_terminal_wrong:{v02_probe.get('terminal_decision')}")

    return failures


def build_policy(default_latest_compatible_runs: int) -> tuple[dict[str, Any], dict[str, Any]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_policy = load_json(SOURCE_POLICY_DIR / f"{SOURCE_SCALE_BAND_POLICY_ID}.json")
    source_receipt = load_json(SOURCE_POLICY_RECEIPT_DIR / f"{SOURCE_SCALE_BAND_POLICY_ID}.json")
    v02_probe = load_json(V02_PROBE_DIR / f"{V02_PROBE_ID}.json")

    failures = verify_sources(source_policy, source_receipt, v02_probe)

    source_run_ids = v02_probe.get("selected_run_ids") or []
    source_run_id = source_run_ids[0] if source_run_ids else None
    if not source_run_id:
        failures.append("missing_v02_source_run_id")

    if default_latest_compatible_runs < 1:
        failures.append(f"default_latest_compatible_runs_must_be_positive:{default_latest_compatible_runs}")
    if default_latest_compatible_runs > 25:
        failures.append(f"default_latest_compatible_runs_too_large:{default_latest_compatible_runs}")

    bounded_contract = {
        "selection_mode": "BOUNDED_BY_DEFAULT",
        "default_latest_compatible_runs": default_latest_compatible_runs,
        "source_run_id": source_run_id,
        "source_run_must_always_be_included": True,
        "latest_compatible_runs_must_be_included": True,
        "selection_order": "latest compatible runs by runs.created_utc desc, falling back to registry row order desc",
        "dedupe_rule": "source run plus latest N compatible runs are de-duplicated by run_id",
        "default_full_registry_scan": False,
        "full_registry_requires_explicit_flag": "--full-registry",
        "full_registry_scan_forbidden_without_flag": True,
        "default_max_registry_runs_touched": default_latest_compatible_runs + 1,
        "bounded_probe_args_required": [
            "--latest-compatible-runs",
            "--full-registry",
        ],
        "default_cli_behavior": f"--latest-compatible-runs {default_latest_compatible_runs}; --full-registry false",
        "honesty_rule": "probe must record selected_run_ids, skipped_compatible_run_count, total_compatible_run_count_estimate_if_known, and whether --full-registry was used",
    }

    policy = dict(source_policy)
    policy.update({
        "schema_version": "stable_delta_signature_candidate_v0_2_bounded_scale_band_policy_v0",
        "policy_name": POLICY_NAME,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "scale_policy_id_name": BOUNDED_POLICY_NAME,
        "source_unbounded_scale_band_policy_id": SOURCE_SCALE_BAND_POLICY_ID,
        "source_unbounded_scale_band_policy_receipt_id": SOURCE_SCALE_BAND_POLICY_RECEIPT_ID,
        "bounded_scale_band_selection": bounded_contract,
        "created_at": now_iso(),
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
    })

    policy["objective"] = dict(policy.get("objective") or {})
    policy["objective"]["bounded_selection_correction"] = (
        "Do not scan all compatible registry runs by default. Include the v0.2 source run and latest N compatible runs only; require --full-registry for all compatible runs."
    )

    contract = dict(policy.get("scale_band_probe_contract") or {})
    contract["minimum_required_bands"] = dict(contract.get("minimum_required_bands") or {})
    contract["minimum_required_bands"]["bounded_default"] = (
        "include source v0.2 run plus latest N compatible runs; do not scan all registry runs by default"
    )
    contract["minimum_required_bands"]["full_registry"] = (
        "only scan all compatible registry runs when --full-registry is explicitly passed"
    )
    contract["bounded_scale_band_selection"] = bounded_contract
    policy["scale_band_probe_contract"] = contract

    required_behavior = dict(policy.get("required_probe_behavior") or {})
    required_behavior.update({
        "include_v02_selected_source_run": True,
        "include_latest_n_compatible_runs_by_default": True,
        "do_not_scan_all_registry_runs_by_default": True,
        "require_full_registry_flag_for_all_runs": True,
        "record_bounded_selection_receipt_fields": True,
    })
    policy["required_probe_behavior"] = required_behavior

    impl = dict(policy.get("implementation_constraints") or {})
    impl["default_latest_compatible_runs"] = default_latest_compatible_runs
    impl["full_registry_requires_explicit_flag"] = True
    impl["must_not_scan_all_registry_runs_by_default"] = True
    policy["implementation_constraints"] = impl

    authority = dict(policy.get("authority") or {})
    authority["authorizes_full_registry_scan_by_default"] = False
    authority["authorizes_full_registry_scan_with_explicit_flag"] = True
    policy["authority"] = authority

    policy["terminal"] = {
        "type": "ADVANCE" if not failures else "STOP",
        "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
        "stop_code": None if not failures else "STOP_BOUNDED_SCALE_BAND_SELECTION_POLICY_INVALID",
    }

    policy_id = sha8({
        "policy_name": policy["policy_name"],
        "scale_policy_id_name": policy["scale_policy_id_name"],
        "source_unbounded_scale_band_policy_id": policy["source_unbounded_scale_band_policy_id"],
        "candidate_design_id": policy["candidate_design_id"],
        "bounded_scale_band_selection": policy["bounded_scale_band_selection"],
        "authority": policy["authority"],
        "required_probe_behavior": policy["required_probe_behavior"],
        "implementation_constraints": policy["implementation_constraints"],
    })
    policy["policy_id"] = policy_id
    policy["policy_sig8"] = policy_id

    receipt = {
        "schema_version": "stable_delta_signature_candidate_v0_2_bounded_scale_band_policy_receipt_v0",
        "policy_id": policy_id,
        "policy_sig8": policy_id,
        "policy_path": f"data/stable_delta_signature_candidate_v0_2_scale_band_policies/{policy_id}.json",
        "policy_name": policy["policy_name"],
        "policy_status": policy["policy_status"],
        "scale_policy_id_name": policy["scale_policy_id_name"],
        "candidate_design_id": policy["candidate_design_id"],
        "source_unbounded_scale_band_policy_id": SOURCE_SCALE_BAND_POLICY_ID,
        "source_unbounded_scale_band_policy_receipt_id": SOURCE_SCALE_BAND_POLICY_RECEIPT_ID,
        "source_v02_probe_id": V02_PROBE_ID,
        "bounded_scale_band_selection": bounded_contract,
        "authorizes_next_scale_band_probe_implementation": True,
        "authorized_next_command_goal": NEXT_COMMAND_GOAL,
        "authorizes_scale_band_probe_execution": True,
        "authorizes_full_registry_scan_by_default": False,
        "authorizes_full_registry_scan_with_explicit_flag": True,
        "authorizes_scale_band_run": False,
        "authorizes_scale_mode": False,
        "authorizes_candidate_acceptance": False,
        "authorizes_registry_write": False,
        "authorizes_runtime_receipt_emission_change": False,
        "authorizes_receipt_replacement": False,
        "authorizes_receipt_deletion": False,
        "authorizes_receipt_compression": False,
        "authorizes_raw_receipt_hash_truth_surface": False,
        "terminal": policy["terminal"],
        "gate": policy["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id

    (OUT_DIR / f"{policy_id}.json").write_text(json.dumps(policy, indent=2, sort_keys=True))
    (OUT_RECEIPT_DIR / f"{policy_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return policy, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--default-latest-compatible-runs", type=int, default=10)
    args = parser.parse_args()

    policy, receipt = build_policy(args.default_latest_compatible_runs)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_id={policy['policy_id']}")
    print(f"policy_json_path=data/stable_delta_signature_candidate_v0_2_scale_band_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/stable_delta_signature_candidate_v0_2_scale_band_policy_receipts/{policy['policy_id']}.json")

    return 0 if policy["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
