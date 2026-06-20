#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

V02_PROBE_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_receipts"
V02_POLICY_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_policies"
SURFACE_PROBE_DIR = ROOT / "data" / "canonical_transition_surface_probe_receipts"

OUT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_scale_band_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_scale_band_policy_receipts"

EXPECTED_V02_PROBE_ID = "bcdb3d93"
EXPECTED_V02_PROBE_RECEIPT_ID = "484c18a3"
EXPECTED_V02_POLICY_ID = "5bc46943"
EXPECTED_V02_POLICY_RECEIPT_ID = "6b57b499"
EXPECTED_SURFACE_PROBE_ID = "07be6e6b"
EXPECTED_SURFACE_RECEIPT_ID = "1c1e392f"

POLICY_NAME = "BUILD_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2_SCALE_BAND_POLICY"
NEXT_COMMAND_GOAL = "IMPLEMENT_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2_SCALE_BAND_PROBE"
CANDIDATE_DESIGN_ID = "STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2"
SCALE_POLICY_ID_NAME = "STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2_SCALE_BAND_POLICY"


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


def verify_sources(v02_probe: dict[str, Any], v02_policy: dict[str, Any], surface_probe: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if v02_probe.get("probe_id") != EXPECTED_V02_PROBE_ID:
        failures.append(f"v02_probe_id_mismatch:{v02_probe.get('probe_id')}")
    if v02_probe.get("receipt_id") != EXPECTED_V02_PROBE_RECEIPT_ID:
        failures.append(f"v02_probe_receipt_id_mismatch:{v02_probe.get('receipt_id')}")
    if v02_probe.get("gate") != "PASS":
        failures.append(f"v02_probe_gate_not_PASS:{v02_probe.get('gate')}")
    if v02_probe.get("mode") != "OUTER_OBSERVER_ONLY":
        failures.append(f"v02_probe_mode_wrong:{v02_probe.get('mode')}")
    if v02_probe.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"candidate_design_id_wrong:{v02_probe.get('candidate_design_id')}")
    if v02_probe.get("compression_version") != "stable_delta_signature_v0.2_candidate":
        failures.append(f"compression_version_wrong:{v02_probe.get('compression_version')}")
    if v02_probe.get("source_policy_id") != EXPECTED_V02_POLICY_ID:
        failures.append(f"v02_probe_source_policy_wrong:{v02_probe.get('source_policy_id')}")
    if v02_probe.get("source_canonical_surface_probe_id") != EXPECTED_SURFACE_PROBE_ID:
        failures.append(f"v02_probe_surface_source_wrong:{v02_probe.get('source_canonical_surface_probe_id')}")
    if v02_probe.get("terminal_decision") != "NEEDS_MORE_SCALE_AFTER_LOCAL_PASS":
        failures.append(f"v02_probe_terminal_not_scale_ready:{v02_probe.get('terminal_decision')}")
    if v02_probe.get("terminal", {}).get("next_command_goal") != POLICY_NAME:
        failures.append(f"v02_probe_next_goal_wrong:{v02_probe.get('terminal', {}).get('next_command_goal')}")

    auth = v02_probe.get("authority_guards") or {}
    if auth.get("observer_only") is not True:
        failures.append("v02_probe_observer_only_missing")
    for key in [
        "runtime_receipt_emission_changed",
        "registry_sqlite_changed",
        "scale_mode_authorized",
        "scale_band_run_authorized",
        "receipt_replacement_authorized",
        "receipt_deletion_authorized",
        "receipt_compression_authorized",
        "stable_delta_candidate_acceptance_authorized",
        "raw_receipt_hash_used_as_truth_surface",
        "source_surface_extension_authorized",
    ]:
        if auth.get(key) is not False:
            failures.append(f"v02_probe_illegal_authority:{key}:{auth.get(key)}")

    gates = v02_probe.get("pass_gates") or {}
    for key in [
        "authority_containment",
        "source_surface_regression",
        "truth_surface",
        "no_identity_leak",
        "no_false_merge",
        "burden_reduction",
        "debug_separation",
        "audit_recoverability",
        "scale_precondition",
    ]:
        if gates.get(key) is not True:
            failures.append(f"v02_probe_gate_expected_true:{key}:{gates.get(key)}")

    dist = v02_probe.get("distinguishability_measurements") or {}
    if dist.get("occurrences_total") != 176:
        failures.append(f"occurrences_total_expected_176:{dist.get('occurrences_total')}")
    if dist.get("distinct_full_occurrence_keys") != 176:
        failures.append(f"distinct_full_occurrence_keys_expected_176:{dist.get('distinct_full_occurrence_keys')}")
    if dist.get("distinct_candidate_signatures") != 176:
        failures.append(f"distinct_candidate_signatures_expected_176:{dist.get('distinct_candidate_signatures')}")
    if dist.get("collision_count") != 0:
        failures.append(f"collision_count_expected_0:{dist.get('collision_count')}")
    if dist.get("false_merge_count") != 0:
        failures.append(f"false_merge_count_expected_0:{dist.get('false_merge_count')}")
    if dist.get("false_split_count") != 0:
        failures.append(f"false_split_count_expected_0:{dist.get('false_split_count')}")
    if dist.get("distinguishability_retention_ratio") != 1.0:
        failures.append(f"retention_expected_1:{dist.get('distinguishability_retention_ratio')}")

    burden = v02_probe.get("burden_measurements") or {}
    if burden.get("full_receipt_count") != 176:
        failures.append(f"full_receipt_count_expected_176:{burden.get('full_receipt_count')}")
    if burden.get("candidate_signature_count") != 176:
        failures.append(f"candidate_signature_count_expected_176:{burden.get('candidate_signature_count')}")
    if burden.get("burden_ratio_projected", 1.0) >= 1.0:
        failures.append(f"burden_ratio_projected_not_reduced:{burden.get('burden_ratio_projected')}")
    if burden.get("burden_ratio_signature_payload", 1.0) >= burden.get("burden_ratio_projected", 0.0):
        failures.append("signature_payload_ratio_not_less_than_projected_ratio")

    sig_contract = v02_probe.get("signature_contract") or {}
    if sig_contract.get("signature_payload_required_fields") != ["cv", "state_hash_before", "move_id", "state_hash_after"]:
        failures.append(f"signature_payload_required_fields_wrong:{sig_contract.get('signature_payload_required_fields')}")
    if sig_contract.get("cycle_n_in_signature_payload") is not False:
        failures.append("cycle_n_in_signature_payload_not_false")
    if sig_contract.get("case_id_in_signature_payload") is not False:
        failures.append("case_id_in_signature_payload_not_false")
    for forbidden in [
        "full_occurrence_key",
        "raw_full_receipt_hash",
        "receipt_hash",
        "receipt_rowid",
        "rowid",
        "audit_pointer",
        "debug_payload",
        "timestamp",
        "receipt_path",
    ]:
        if forbidden not in (sig_contract.get("signature_payload_forbidden_fields") or []):
            failures.append(f"forbidden_field_missing_from_probe_contract:{forbidden}")

    source_surface_check = v02_probe.get("source_surface_check") or {}
    if source_surface_check.get("source_surface_regression_failures") != []:
        failures.append(f"source_surface_regression_failures_not_empty:{source_surface_check.get('source_surface_regression_failures')}")
    if source_surface_check.get("surface_probe_terminal_decision") != "PASS_CANONICAL_TRANSITION_SURFACE_OBSERVER_ONLY":
        failures.append(f"surface_probe_terminal_wrong:{source_surface_check.get('surface_probe_terminal_decision')}")
    if source_surface_check.get("surface_probe_patch_version") != "alias_patch_state_sig8_before_after_v0":
        failures.append(f"surface_patch_version_wrong:{source_surface_check.get('surface_probe_patch_version')}")

    if v02_policy.get("policy_id") != EXPECTED_V02_POLICY_ID:
        failures.append(f"v02_policy_id_wrong:{v02_policy.get('policy_id')}")
    if v02_policy.get("gate") != "PASS":
        failures.append(f"v02_policy_gate_not_PASS:{v02_policy.get('gate')}")
    if v02_policy.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"v02_policy_candidate_design_wrong:{v02_policy.get('candidate_design_id')}")

    policy_auth = v02_policy.get("authority") or {}
    if policy_auth.get("authorizes_scale_band_run") is not False:
        failures.append("v02_policy_already_authorized_scale_band_run")
    if policy_auth.get("authorizes_scale_mode") is not False:
        failures.append("v02_policy_authorizes_scale_mode")
    if policy_auth.get("authorizes_stable_delta_candidate_acceptance") is not False:
        failures.append("v02_policy_authorizes_candidate_acceptance")

    if surface_probe.get("probe_id") != EXPECTED_SURFACE_PROBE_ID:
        failures.append(f"surface_probe_id_wrong:{surface_probe.get('probe_id')}")
    if surface_probe.get("receipt_id") != EXPECTED_SURFACE_RECEIPT_ID:
        failures.append(f"surface_receipt_id_wrong:{surface_probe.get('receipt_id')}")
    if surface_probe.get("terminal_decision") != "PASS_CANONICAL_TRANSITION_SURFACE_OBSERVER_ONLY":
        failures.append(f"surface_terminal_wrong:{surface_probe.get('terminal_decision')}")
    if surface_probe.get("gate") != "PASS":
        failures.append(f"surface_gate_not_PASS:{surface_probe.get('gate')}")

    return failures


def build_policy(v02_probe_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    v02_probe = load_json(V02_PROBE_DIR / f"{v02_probe_id}.json")
    v02_policy = load_json(V02_POLICY_DIR / f"{EXPECTED_V02_POLICY_ID}.json")
    surface_probe = load_json(SURFACE_PROBE_DIR / f"{EXPECTED_SURFACE_PROBE_ID}.json")

    failures = verify_sources(v02_probe, v02_policy, surface_probe)

    local_dist = v02_probe.get("distinguishability_measurements") or {}
    local_burden = v02_probe.get("burden_measurements") or {}

    policy = {
        "schema_version": "stable_delta_signature_candidate_v0_2_scale_band_policy_v0",
        "policy_name": POLICY_NAME,
        "policy_kind": "STABLE_DELTA_SIGNATURE_CANDIDATE_SCALE_BAND_POLICY",
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "scale_policy_id_name": SCALE_POLICY_ID_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "mode": "OUTER_OBSERVER_ONLY",
        "source_v02_probe_id": EXPECTED_V02_PROBE_ID,
        "source_v02_probe_receipt_id": EXPECTED_V02_PROBE_RECEIPT_ID,
        "source_v02_policy_id": EXPECTED_V02_POLICY_ID,
        "source_v02_policy_receipt_id": EXPECTED_V02_POLICY_RECEIPT_ID,
        "source_canonical_surface_probe_id": EXPECTED_SURFACE_PROBE_ID,
        "source_canonical_surface_receipt_id": EXPECTED_SURFACE_RECEIPT_ID,
        "local_pass_summary": {
            "terminal_decision": v02_probe.get("terminal_decision"),
            "occurrences_total": local_dist.get("occurrences_total"),
            "distinct_full_occurrence_keys": local_dist.get("distinct_full_occurrence_keys"),
            "distinct_candidate_signatures": local_dist.get("distinct_candidate_signatures"),
            "distinguishability_retention_ratio": local_dist.get("distinguishability_retention_ratio"),
            "collision_count": local_dist.get("collision_count"),
            "false_merge_count": local_dist.get("false_merge_count"),
            "false_split_count": local_dist.get("false_split_count"),
            "burden_ratio_projected": local_burden.get("burden_ratio_projected"),
            "burden_ratio_signature_payload": local_burden.get("burden_ratio_signature_payload"),
            "projected_scale_row_bytes": local_burden.get("projected_scale_row_bytes"),
            "full_receipt_bytes": local_burden.get("full_receipt_bytes"),
            "scale_precondition": v02_probe.get("pass_gates", {}).get("scale_precondition"),
        },
        "authority": {
            "authorizes_next_scale_band_probe_implementation": True,
            "authorized_next_command_goal": NEXT_COMMAND_GOAL,
            "authorizes_scale_band_probe_execution": True,
            "authorizes_scale_band_run": False,
            "authorizes_scale_mode": False,
            "authorizes_candidate_acceptance": False,
            "authorizes_runtime_receipt_emission_change": False,
            "authorizes_registry_write": False,
            "authorizes_full_receipt_suppression": False,
            "authorizes_receipt_replacement": False,
            "authorizes_receipt_deletion": False,
            "authorizes_receipt_compression": False,
            "authorizes_raw_receipt_hash_truth_surface": False,
            "authorizes_theorem_content": False,
            "authorizes_taxonomy_evolution": False,
            "authorizes_architecture_redesign": False,
            "authorizes_source_surface_extension": False,
        },
        "objective": {
            "goal": "Test whether the v0.2 local stable delta signature result survives scale variation before any acceptance or scale-mode authority.",
            "primary_question": "Does state_sig8_before + move_id + state_sig8_after preserve distinguishability and burden reduction across available radius/depth/cycle scale bands?",
            "scale_precondition_source": "v0.2 local probe had zero false merges, full retention, burden reduction, audit recoverability, and observer containment.",
            "non_goals": [
                "Do not authorize scale mode.",
                "Do not accept the candidate.",
                "Do not suppress or replace receipts.",
                "Do not compress or delete receipts.",
                "Do not mutate registry.sqlite.",
                "Do not modify runtime receipt emission.",
                "Do not use raw receipt hashes as truth surface.",
                "Do not use rowid, cycle_n, or case_id as primary signature identity.",
            ],
        },
        "scale_band_probe_contract": {
            "candidate_signature_payload_required_fields": [
                "cv",
                "state_hash_before",
                "move_id",
                "state_hash_after",
            ],
            "candidate_signature_payload_forbidden_fields": [
                "full_occurrence_key",
                "raw_full_receipt_hash",
                "full_receipt_hash",
                "receipt_hash",
                "receipt_sig8",
                "receipt_rowid",
                "rowid",
                "audit_pointer",
                "debug_payload",
                "observer_notes",
                "created_at",
                "created_utc",
                "timestamp",
                "path",
                "receipt_path",
                "file_path",
                "cycle_n_as_primary_identity",
                "case_id_as_primary_identity",
            ],
            "truth_surface": "full_occurrence_key_to_candidate_delta_signature",
            "scale_band_axes": [
                "available_run_ids",
                "depth",
                "cycle_n",
                "family",
                "case_id",
                "receipt_count",
                "raw/cell size fields if present",
            ],
            "minimum_required_bands": {
                "local_run_replay": "must include the source local run",
                "available_prior_or_later_runs": "include all compatible registry runs if present, otherwise classify insufficient scale coverage",
                "depth_variation": "measure per depth and depth growth if depth values vary",
                "cycle_variation": "measure per cycle_n and cycle growth if cycle_n values vary",
            },
            "required_per_band_measurements": [
                "run_id",
                "band_id",
                "axis",
                "axis_value",
                "occurrences_total",
                "distinct_full_occurrence_keys",
                "distinct_candidate_signatures",
                "collision_count",
                "false_merge_count",
                "false_split_count",
                "distinguishability_retention_ratio",
                "full_receipt_bytes",
                "signature_payload_bytes",
                "projected_scale_row_bytes",
                "burden_ratio_projected",
                "burden_ratio_signature_payload",
                "source_surface_regression_count",
                "identity_leak_count",
                "audit_recoverability_failures",
                "observer_overhead_ms",
            ],
            "required_aggregate_measurements": [
                "bands_total",
                "bands_passed",
                "bands_failed",
                "worst_false_merge_count",
                "worst_collision_count",
                "worst_distinguishability_retention_ratio",
                "worst_burden_ratio_projected",
                "scale_coverage_status",
                "compatible_run_count",
            ],
        },
        "pass_gates": {
            "authority_containment": "observer-only, no registry writes, no runtime receipt changes, no scale mode, no acceptance",
            "local_precondition_preserved": "source v0.2 local probe remains a clean local pass",
            "source_surface_regression": "state_sig8_before, move_id, state_sig8_after remain present and usable for every compatible band",
            "truth_surface": "compare full_occurrence_key to candidate_delta_signature, never raw receipt hashes",
            "no_identity_leak": "signature payload excludes rowid, receipt hashes, audit pointer, full occurrence key, timestamps, paths, case_id-as-identity, cycle_n-as-identity",
            "audit_recoverability": "every candidate row has an audit pointer to source registry receipt row",
            "no_false_merge_all_bands": "false_merge_count == 0 for every compatible band",
            "burden_reduction_all_bands": "projected_scale_row_bytes < full_receipt_bytes for every compatible band",
            "scale_coverage_honesty": "if only one compatible run exists, terminal must be INSUFFICIENT_SCALE_COVERAGE rather than acceptance",
        },
        "terminal_decisions": {
            "PASS_SCALE_BANDS_OBSERVER_ONLY": "Use when multiple compatible scale bands pass no false merge, burden reduction, audit recovery, and observer containment.",
            "PASS_LOCAL_REPLAY_ONLY_INSUFFICIENT_SCALE_COVERAGE": "Use when local replay passes but there are not enough compatible scale bands/runs to claim scale stability.",
            "FAIL_SCALE_FALSE_MERGE": "Use if any compatible scale band introduces false merges.",
            "FAIL_SCALE_BURDEN_REGRESSION": "Use if projected burden is not reduced in any required compatible band.",
            "FAIL_SOURCE_SURFACE_REGRESSION": "Use if required transition tuple fields are missing or unusable in any compatible band.",
            "FAIL_IDENTITY_LEAK": "Use if rowid, raw receipt hash, full occurrence key, path, timestamp, audit pointer, case_id-as-identity, or cycle_n-as-identity enters signature payload.",
            "FAIL_OBSERVER_INTERFERENCE": "Use if probe mutates registry, runtime receipt emission, receipts, or authority.",
        },
        "required_probe_behavior": {
            "read_existing_registry_only": True,
            "load_v02_local_probe_receipt": True,
            "replay_v02_signature_logic_across_compatible_runs": True,
            "emit_scale_band_rows_jsonl": True,
            "emit_scale_band_probe_receipt": True,
            "measure_per_band_burden_and_distinguishability": True,
            "measure_aggregate_worst_case": True,
            "classify_insufficient_scale_coverage_honestly": True,
            "must_not_write_registry_sqlite": True,
            "must_not_change_runtime_receipt_generation": True,
            "must_not_authorize_scale_mode": True,
            "must_not_accept_candidate": True,
            "must_not_replace_or_suppress_receipts": True,
            "must_not_use_raw_receipt_hash_truth_surface": True,
            "must_not_use_rowid_as_signature_identity": True,
            "must_not_use_cycle_n_or_case_id_as_primary_signature_identity": True,
        },
        "implementation_constraints": {
            "must_touch_only_files": [
                "scripts/stable_delta_signature_candidate_v0_2_scale_band_probe.py"
            ],
            "must_not_modify_files": [
                "src/",
                "app/",
                "matrixlab/",
                "scripts/stable_delta_signature_candidate_v0_2_probe.py",
                "scripts/build_stable_delta_signature_candidate_v0_2_policy.py",
                "scripts/canonical_transition_surface_probe_v0.py",
                "scripts/stable_delta_signature_candidate_v0_1_probe.py",
                "scripts/stable_delta_signature_probe_v0.py",
                "scripts/wide_burden_profile_microruns.py",
            ],
            "must_not_change_registry_sqlite": True,
            "must_not_delete_existing_outputs": True,
            "must_not_accept_candidate": True,
            "must_not_authorize_scale_mode": True,
        },
        "required_negative_controls": [
            {
                "case": "local_precondition_missing_fail",
                "must_fail_if": "source v0.2 local probe no longer has false_merge_count == 0 or burden reduction",
            },
            {
                "case": "scale_mode_authority_fail",
                "must_fail_if": "probe authorizes scale mode or candidate acceptance",
            },
            {
                "case": "registry_mutation_fail",
                "must_fail_if": "probe writes to registry.sqlite",
            },
            {
                "case": "raw_hash_truth_surface_fail",
                "must_fail_if": "raw receipt hash is used as truth surface",
            },
            {
                "case": "rowid_identity_leak_fail",
                "must_fail_if": "rowid or receipt_rowid enters signature payload",
            },
            {
                "case": "cycle_identity_leak_fail",
                "must_fail_if": "cycle_n is used as primary signature identity",
            },
            {
                "case": "case_identity_leak_fail",
                "must_fail_if": "case_id is used as primary signature identity",
            },
            {
                "case": "insufficient_scale_coverage_false_acceptance_fail",
                "must_fail_if": "only local replay exists but terminal claims scale-band pass",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2_SCALE_BAND_POLICY_INVALID",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    policy_id = sha8({
        "policy_name": policy["policy_name"],
        "scale_policy_id_name": policy["scale_policy_id_name"],
        "candidate_design_id": policy["candidate_design_id"],
        "source_v02_probe_id": policy["source_v02_probe_id"],
        "authority": policy["authority"],
        "objective": policy["objective"],
        "scale_band_probe_contract": policy["scale_band_probe_contract"],
        "required_probe_behavior": policy["required_probe_behavior"],
        "implementation_constraints": policy["implementation_constraints"],
    })
    policy["policy_id"] = policy_id
    policy["policy_sig8"] = policy_id

    receipt = {
        "schema_version": "stable_delta_signature_candidate_v0_2_scale_band_policy_receipt_v0",
        "policy_id": policy_id,
        "policy_sig8": policy_id,
        "policy_path": f"data/stable_delta_signature_candidate_v0_2_scale_band_policies/{policy_id}.json",
        "policy_name": POLICY_NAME,
        "policy_status": policy["policy_status"],
        "scale_policy_id_name": SCALE_POLICY_ID_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_v02_probe_id": EXPECTED_V02_PROBE_ID,
        "source_v02_probe_receipt_id": EXPECTED_V02_PROBE_RECEIPT_ID,
        "source_v02_policy_id": EXPECTED_V02_POLICY_ID,
        "source_v02_policy_receipt_id": EXPECTED_V02_POLICY_RECEIPT_ID,
        "source_canonical_surface_probe_id": EXPECTED_SURFACE_PROBE_ID,
        "source_canonical_surface_receipt_id": EXPECTED_SURFACE_RECEIPT_ID,
        "local_pass_summary": policy["local_pass_summary"],
        "authorizes_next_scale_band_probe_implementation": True,
        "authorized_next_command_goal": NEXT_COMMAND_GOAL,
        "authorizes_scale_band_probe_execution": True,
        "authorizes_scale_band_run": False,
        "authorizes_scale_mode": False,
        "authorizes_candidate_acceptance": False,
        "authorizes_runtime_receipt_emission_change": False,
        "authorizes_registry_write": False,
        "authorizes_receipt_replacement": False,
        "authorizes_receipt_deletion": False,
        "authorizes_receipt_compression": False,
        "authorizes_raw_receipt_hash_truth_surface": False,
        "terminal_decisions": policy["terminal_decisions"],
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
    parser.add_argument("--v02-probe-id", default=EXPECTED_V02_PROBE_ID)
    args = parser.parse_args()

    policy, receipt = build_policy(args.v02_probe_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_id={policy['policy_id']}")
    print(f"policy_json_path=data/stable_delta_signature_candidate_v0_2_scale_band_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/stable_delta_signature_candidate_v0_2_scale_band_policy_receipts/{policy['policy_id']}.json")

    return 0 if policy["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
