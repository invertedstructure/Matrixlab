#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

DIAGNOSTIC_DIR = ROOT / "data" / "bounded_scale_false_merge_diagnostics"
DIAGNOSTIC_RECEIPT_DIR = ROOT / "data" / "bounded_scale_false_merge_diagnostic_receipts"
SOURCE_SCALE_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_scale_band_receipts"

OUT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_3_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_3_policy_receipts"

EXPECTED_DIAGNOSTIC_ID = "62c8d96c"
EXPECTED_DIAGNOSTIC_RECEIPT_ID = "b88d3818"
EXPECTED_SOURCE_SCALE_PROBE_ID = "227e9426"
EXPECTED_SOURCE_SCALE_RECEIPT_ID = "0ae57255"
EXPECTED_SOURCE_POLICY_ID = "b79955ce"
EXPECTED_SOURCE_V02_PROBE_ID = "bcdb3d93"

POLICY_NAME = "BUILD_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_3_POLICY"
CANDIDATE_DESIGN_ID = "STABLE_DELTA_SIGNATURE_CANDIDATE_V0_3"
NEXT_COMMAND_GOAL = "IMPLEMENT_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_3_PROBE"

BASE_TRANSITION_FIELDS = ["cv", "state_hash_before", "move_id", "state_hash_after"]
DELTA_BUCKET_FIELDS = [
    "row_delta",
    "col_delta",
    "rank_delta",
    "support_delta",
    "distinct_column_types_before",
    "distinct_column_types_after",
    "new_column_types_added",
    "compression_ratio",
]

FORBIDDEN_SIGNATURE_FIELDS = [
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
    "case_id_as_primary_identity",
    "cycle_n_as_primary_identity",
    "case_id",
    "cycle_n",
    "depth_as_primary_identity",
]


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


def verify_sources(diagnostic: dict[str, Any], receipt: dict[str, Any], source_scale: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if diagnostic.get("diagnostic_id") != EXPECTED_DIAGNOSTIC_ID:
        failures.append(f"diagnostic_id_wrong:{diagnostic.get('diagnostic_id')}")
    if receipt.get("receipt_id") != EXPECTED_DIAGNOSTIC_RECEIPT_ID:
        failures.append(f"diagnostic_receipt_id_wrong:{receipt.get('receipt_id')}")
    if diagnostic.get("gate") != "PASS":
        failures.append(f"diagnostic_gate_not_PASS:{diagnostic.get('gate')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"diagnostic_receipt_gate_not_PASS:{receipt.get('gate')}")
    if diagnostic.get("diagnosis_status") != "DIAGNOSED":
        failures.append(f"diagnosis_status_wrong:{diagnostic.get('diagnosis_status')}")

    if diagnostic.get("source_probe_id") != EXPECTED_SOURCE_SCALE_PROBE_ID:
        failures.append(f"diagnostic_source_probe_wrong:{diagnostic.get('source_probe_id')}")
    if diagnostic.get("source_receipt_id") != EXPECTED_SOURCE_SCALE_RECEIPT_ID:
        failures.append(f"diagnostic_source_receipt_wrong:{diagnostic.get('source_receipt_id')}")
    if diagnostic.get("source_policy_id") != EXPECTED_SOURCE_POLICY_ID:
        failures.append(f"diagnostic_source_policy_wrong:{diagnostic.get('source_policy_id')}")
    if diagnostic.get("source_v02_probe_id") != EXPECTED_SOURCE_V02_PROBE_ID:
        failures.append(f"diagnostic_source_v02_probe_wrong:{diagnostic.get('source_v02_probe_id')}")

    summary = diagnostic.get("summary") or {}
    if summary.get("source_terminal_decision") != "FAIL_SCALE_FALSE_MERGE":
        failures.append(f"source_terminal_not_FAIL_SCALE_FALSE_MERGE:{summary.get('source_terminal_decision')}")
    if summary.get("bounded_default_used") is not True:
        failures.append(f"source_not_bounded_default:{summary.get('bounded_default_used')}")
    if summary.get("full_registry_used") is not False:
        failures.append(f"source_used_full_registry:{summary.get('full_registry_used')}")
    if summary.get("compatible_run_count") != 10:
        failures.append(f"compatible_run_count_not_10:{summary.get('compatible_run_count')}")
    if summary.get("bands_failed") != 10:
        failures.append(f"bands_failed_not_10:{summary.get('bands_failed')}")
    if summary.get("collision_group_count") != 10:
        failures.append(f"collision_group_count_not_10:{summary.get('collision_group_count')}")
    if summary.get("collision_signature_count") != 1:
        failures.append(f"collision_signature_count_not_1:{summary.get('collision_signature_count')}")
    if summary.get("worst_false_merge_count") != 1:
        failures.append(f"worst_false_merge_count_not_1:{summary.get('worst_false_merge_count')}")
    if summary.get("worst_burden_ratio_projected", 1.0) >= 1.0:
        failures.append(f"burden_ratio_not_viable:{summary.get('worst_burden_ratio_projected')}")

    classification = diagnostic.get("classification") or {}
    if classification.get("primary_class") != "REPEATED_TRANSITION_SIGNATURE_COLLAPSES_DISTINCT_OCCURRENCES":
        failures.append(f"classification_wrong:{classification.get('primary_class')}")
    if classification.get("all_collision_records_share_candidate_signature_payload") is not True:
        failures.append("collision_payloads_not_shared")
    field_freq = classification.get("differing_debug_field_frequency") or {}
    if field_freq.get("compact_delta_debug", 0) < 1:
        failures.append("compact_delta_debug_not_observed_as_differing")
    if field_freq.get("case_id_debug_only", 0) < 1:
        failures.append("case_id_debug_difference_missing")
    if field_freq.get("full_occurrence_key", 0) < 1:
        failures.append("full_occurrence_key_difference_missing")

    decision = diagnostic.get("decision") or {}
    expected_true = [
        "candidate_v0_2_rejected_for_scale_acceptance",
        "burden_side_remains_viable",
        "authority_side_clean",
        "source_surface_clean",
        "identity_leak_absent",
        "do_not_full_registry_scan",
        "do_not_accept_candidate",
        "do_not_change_runtime",
        "do_not_patch_by_adding_case_id_or_cycle_n_as_primary_identity",
    ]
    for key in expected_true:
        if decision.get(key) is not True:
            failures.append(f"decision_expected_true:{key}:{decision.get(key)}")
    if decision.get("primary_blocker") != "FALSE_MERGE_UNDER_BOUNDED_SCALE":
        failures.append(f"primary_blocker_wrong:{decision.get('primary_blocker')}")
    if decision.get("recommended_next_command_goal") != POLICY_NAME:
        failures.append(f"diagnostic_next_goal_not_this_policy:{decision.get('recommended_next_command_goal')}")

    auth = diagnostic.get("authority") or {}
    if auth.get("observer_only") is not True:
        failures.append("diagnostic_not_observer_only")
    for key in [
        "authorizes_candidate_acceptance",
        "authorizes_scale_mode",
        "authorizes_full_registry_scan",
        "authorizes_runtime_receipt_emission_change",
        "authorizes_registry_write",
        "authorizes_receipt_replacement",
        "authorizes_receipt_compression",
        "authorizes_raw_receipt_hash_truth_surface",
        "authorizes_case_id_or_cycle_n_primary_identity_patch",
    ]:
        if auth.get(key) is not False:
            failures.append(f"diagnostic_illegal_authority:{key}:{auth.get(key)}")

    if source_scale.get("probe_id") != EXPECTED_SOURCE_SCALE_PROBE_ID:
        failures.append(f"source_scale_probe_wrong:{source_scale.get('probe_id')}")
    if source_scale.get("receipt_id") != EXPECTED_SOURCE_SCALE_RECEIPT_ID:
        failures.append(f"source_scale_receipt_wrong:{source_scale.get('receipt_id')}")
    if source_scale.get("terminal_decision") != "FAIL_SCALE_FALSE_MERGE":
        failures.append(f"source_scale_terminal_wrong:{source_scale.get('terminal_decision')}")
    if source_scale.get("scale_coverage", {}).get("bounded_default_used") is not True:
        failures.append("source_scale_not_bounded_default")
    if source_scale.get("scale_coverage", {}).get("full_registry_used") is not False:
        failures.append("source_scale_used_full_registry")
    if source_scale.get("pass_gates", {}).get("no_false_merge_all_bands") is not False:
        failures.append("source_scale_false_merge_gate_not_false")

    return failures


def build_policy(source_diagnostic_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    diagnostic = load_json(DIAGNOSTIC_DIR / f"{source_diagnostic_id}.json")
    diagnostic_receipt = load_json(DIAGNOSTIC_RECEIPT_DIR / f"{source_diagnostic_id}.json")
    source_scale = load_json(SOURCE_SCALE_RECEIPT_DIR / f"{EXPECTED_SOURCE_SCALE_PROBE_ID}.json")

    failures = verify_sources(diagnostic, diagnostic_receipt, source_scale)

    candidate_design = {
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "design_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "reason_for_v0_3": "v0.2 transition tuple caused repeated transition signatures to collapse distinct bounded-scale occurrences.",
        "v0_2_rejected_for_scale_acceptance": True,
        "design_hypothesis": (
            "Promote lawful compact transition-delta buckets from debug sidecar into the candidate signature payload. "
            "The bounded false-merge diagnostic showed compact_delta_debug differed across all collision groups, while v0.2 payloads were identical."
        ),
        "base_transition_tuple_retained": BASE_TRANSITION_FIELDS,
        "new_lawful_discriminator": {
            "name": "transition_delta_buckets",
            "kind": "LAWFUL_TRANSITION_DELTA_DISCRIMINATOR",
            "source": "existing registry receipt delta columns only",
            "allowed_source_columns": DELTA_BUCKET_FIELDS,
            "construction": "canonical bucketized map of available transition-delta metrics; omitted metrics must be explicitly recorded as absent rather than fabricated",
            "must_be_measured_as_signature_payload": True,
            "must_be_measured_separately_from_debug_sidecar": True,
            "must_report_delta_bucket_coverage": True,
            "must_report_delta_bucket_discriminative_power": True,
        },
        "signature_payload_required_fields": [
            "cv",
            "state_hash_before",
            "move_id",
            "state_hash_after",
            "transition_delta_buckets",
        ],
        "signature_payload_forbidden_fields": FORBIDDEN_SIGNATURE_FIELDS,
        "explicit_non_solutions": [
            "Do not add case_id as primary identity.",
            "Do not add cycle_n as primary identity.",
            "Do not add rowid or receipt_rowid.",
            "Do not add full_occurrence_key.",
            "Do not add raw receipt hash or receipt hash.",
            "Do not add audit pointer to signature payload.",
            "Do not add debug payload to signature payload.",
            "Do not full-registry scan.",
            "Do not accept candidate from policy construction.",
        ],
        "truth_surface": "full_occurrence_key_to_candidate_delta_signature",
        "bounded_evaluation_surface": {
            "source_scale_probe_id": EXPECTED_SOURCE_SCALE_PROBE_ID,
            "source_scale_receipt_id": EXPECTED_SOURCE_SCALE_RECEIPT_ID,
            "source_policy_id": EXPECTED_SOURCE_POLICY_ID,
            "bounded_default_required": True,
            "full_registry_forbidden": True,
            "compatible_run_count": 10,
            "bands_total": 266,
            "failed_bands_to_retest": 10,
        },
        "pass_gates_for_next_probe": {
            "authority_containment": "observer-only, no registry writes, no runtime receipt changes, no scale mode, no acceptance",
            "bounded_selection": "must reuse bounded default surface unless explicit later policy changes it",
            "source_surface_regression": "state_sig8_before, move_id, state_sig8_after, and allowed delta columns must be inspected honestly",
            "delta_bucket_coverage": "every row must report present/absent coverage for allowed delta columns",
            "truth_surface": "compare full_occurrence_key to candidate_delta_signature, never raw receipt hashes",
            "no_identity_leak": "payload excludes case_id/cycle_n as primary identity, rowid, audit pointer, full occurrence key, receipt hashes, paths, timestamps",
            "no_false_merge_on_failed_bands": "v0.3 must clear the known 10 failed bounded bands or stop",
            "burden_reduction": "projected v0.3 burden must remain below full receipt burden",
            "audit_recoverability": "audit pointer remains outside signature payload and points back to source registry rows",
        },
        "terminal_decisions_for_next_probe": {
            "PASS_V0_3_BOUNDED_FALSE_MERGE_REPAIR": "Use when v0.3 clears known bounded false merges with burden reduction and authority containment.",
            "FAIL_V0_3_FALSE_MERGE_PERSISTS": "Use when the 10 known bounded false-merge bands still collide.",
            "FAIL_V0_3_BURDEN_REGRESSION": "Use when v0.3 projected burden is not below full receipt burden.",
            "FAIL_V0_3_IDENTITY_LEAK": "Use when forbidden identity/audit/receipt fields enter signature payload.",
            "FAIL_V0_3_SOURCE_SURFACE_REGRESSION": "Use when required transition or delta fields are missing without honest absent-field accounting.",
            "FAIL_V0_3_OBSERVER_INTERFERENCE": "Use when registry/runtime/receipt emission/authority is mutated.",
        },
    }

    authority = {
        "observer_only": True,
        "authorizes_next_candidate_probe_implementation": True,
        "authorized_next_command_goal": NEXT_COMMAND_GOAL,
        "authorizes_v0_3_policy_only": True,
        "authorizes_bounded_v0_3_probe_execution": True,
        "authorizes_candidate_acceptance": False,
        "authorizes_scale_mode": False,
        "authorizes_full_registry_scan": False,
        "authorizes_runtime_receipt_emission_change": False,
        "authorizes_registry_write": False,
        "authorizes_receipt_replacement": False,
        "authorizes_receipt_deletion": False,
        "authorizes_receipt_compression": False,
        "authorizes_raw_receipt_hash_truth_surface": False,
        "authorizes_case_id_or_cycle_n_primary_identity_patch": False,
        "authorizes_rowid_identity_patch": False,
        "authorizes_audit_pointer_in_signature_payload": False,
        "authorizes_debug_payload_in_signature_payload": False,
    }

    implementation_constraints = {
        "must_touch_only_files": [
            "scripts/stable_delta_signature_candidate_v0_3_probe.py",
        ],
        "must_not_modify_files": [
            "src/",
            "app/",
            "matrixlab/",
            "scripts/stable_delta_signature_candidate_v0_2_scale_band_probe.py",
            "scripts/diagnose_bounded_scale_false_merges_v0.py",
            "scripts/build_bounded_scale_band_selection_policy_v0.py",
            "scripts/stable_delta_signature_candidate_v0_2_probe.py",
            "scripts/canonical_transition_surface_probe_v0.py",
        ],
        "must_not_full_registry_scan": True,
        "must_reuse_bounded_source_probe_surface": True,
        "must_not_accept_candidate": True,
        "must_not_authorize_scale_mode": True,
        "must_not_change_registry_sqlite": True,
        "must_not_change_runtime_receipt_emission": True,
    }

    policy = {
        "schema_version": "stable_delta_signature_candidate_v0_3_policy_v0",
        "policy_name": POLICY_NAME,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_diagnostic_id": EXPECTED_DIAGNOSTIC_ID,
        "source_diagnostic_receipt_id": EXPECTED_DIAGNOSTIC_RECEIPT_ID,
        "source_bounded_scale_probe_id": EXPECTED_SOURCE_SCALE_PROBE_ID,
        "source_bounded_scale_receipt_id": EXPECTED_SOURCE_SCALE_RECEIPT_ID,
        "source_bounded_policy_id": EXPECTED_SOURCE_POLICY_ID,
        "source_v02_probe_id": EXPECTED_SOURCE_V02_PROBE_ID,
        "candidate_design": candidate_design,
        "authority": authority,
        "implementation_constraints": implementation_constraints,
        "required_negative_controls_for_next_probe": [
            {
                "case": "known_false_merge_not_cleared_fail",
                "must_fail_if": "any of the 10 known failed bounded bands still has false_merge_count > 0",
            },
            {
                "case": "case_id_primary_identity_fail",
                "must_fail_if": "case_id or case_id_as_primary_identity enters signature payload",
            },
            {
                "case": "cycle_n_primary_identity_fail",
                "must_fail_if": "cycle_n or cycle_n_as_primary_identity enters signature payload",
            },
            {
                "case": "rowid_identity_fail",
                "must_fail_if": "rowid or receipt_rowid enters signature payload",
            },
            {
                "case": "receipt_hash_truth_surface_fail",
                "must_fail_if": "raw/full receipt hash is used as truth surface",
            },
            {
                "case": "audit_pointer_payload_fail",
                "must_fail_if": "audit pointer enters signature payload",
            },
            {
                "case": "full_registry_scan_fail",
                "must_fail_if": "probe scans beyond bounded source surface or uses --full-registry",
            },
            {
                "case": "burden_regression_fail",
                "must_fail_if": "projected v0.3 burden >= full receipt burden",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_3_POLICY_INVALID",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    policy_id = sha8({
        "policy_name": policy["policy_name"],
        "candidate_design_id": policy["candidate_design_id"],
        "source_diagnostic_id": policy["source_diagnostic_id"],
        "candidate_design": policy["candidate_design"],
        "authority": policy["authority"],
        "implementation_constraints": policy["implementation_constraints"],
    })
    policy["policy_id"] = policy_id
    policy["policy_sig8"] = policy_id

    receipt = {
        "schema_version": "stable_delta_signature_candidate_v0_3_policy_receipt_v0",
        "policy_id": policy_id,
        "policy_sig8": policy_id,
        "policy_name": POLICY_NAME,
        "policy_status": policy["policy_status"],
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "policy_path": f"data/stable_delta_signature_candidate_v0_3_policies/{policy_id}.json",
        "source_diagnostic_id": EXPECTED_DIAGNOSTIC_ID,
        "source_diagnostic_receipt_id": EXPECTED_DIAGNOSTIC_RECEIPT_ID,
        "source_bounded_scale_probe_id": EXPECTED_SOURCE_SCALE_PROBE_ID,
        "source_bounded_scale_receipt_id": EXPECTED_SOURCE_SCALE_RECEIPT_ID,
        "source_bounded_policy_id": EXPECTED_SOURCE_POLICY_ID,
        "source_v02_probe_id": EXPECTED_SOURCE_V02_PROBE_ID,
        "candidate_design_summary": {
            "v0_2_rejected_for_scale_acceptance": True,
            "primary_blocker": "REPEATED_TRANSITION_SIGNATURE_COLLAPSES_DISTINCT_OCCURRENCES",
            "new_lawful_discriminator": "transition_delta_buckets",
            "allowed_delta_bucket_columns": DELTA_BUCKET_FIELDS,
            "forbidden_primary_identity_patch": [
                "case_id",
                "cycle_n",
                "rowid",
                "receipt_hash",
                "audit_pointer",
                "full_occurrence_key",
            ],
        },
        "authority": authority,
        "implementation_constraints": implementation_constraints,
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
    parser.add_argument("--source-diagnostic-id", default=EXPECTED_DIAGNOSTIC_ID)
    args = parser.parse_args()

    policy, receipt = build_policy(args.source_diagnostic_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_id={policy['policy_id']}")
    print(f"policy_json_path=data/stable_delta_signature_candidate_v0_3_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/stable_delta_signature_candidate_v0_3_policy_receipts/{policy['policy_id']}.json")

    return 0 if policy["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
