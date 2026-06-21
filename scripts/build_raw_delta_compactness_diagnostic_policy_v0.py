#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

V03_FAILURE_DIAG_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_3_failure_diagnostics"
V03_FAILURE_DIAG_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_3_failure_diagnostic_receipts"
V03_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_3_receipts"
V02_SCALE_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_scale_band_receipts"

OUT_DIR = ROOT / "data" / "raw_delta_compactness_diagnostic_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_compactness_diagnostic_policy_receipts"

EXPECTED_V03_FAILURE_DIAG_ID = "d0132dd4"
EXPECTED_V03_FAILURE_DIAG_RECEIPT_ID = "13b228ac"
EXPECTED_V03_PROBE_ID = "bd1beabe"
EXPECTED_V03_RECEIPT_ID = "c598371b"
EXPECTED_V02_SCALE_PROBE_ID = "227e9426"
EXPECTED_V03_POLICY_ID = "78a6fbec"

POLICY_NAME = "BUILD_RAW_DELTA_COMPACTNESS_DIAGNOSTIC_POLICY_V0"
DIAGNOSTIC_NAME = "RAW_DELTA_COMPACTNESS_DIAGNOSTIC_V0"
NEXT_COMMAND_GOAL = "IMPLEMENT_RAW_DELTA_COMPACTNESS_DIAGNOSTIC_V0"

TARGET_RAW_DELTA_FIELD = "compression_ratio"
ALLOWED_RAW_DELTA_FIELDS = [
    "compression_ratio",
]
CONTEXT_ONLY_DELTA_FIELDS = [
    "row_delta",
    "col_delta",
    "rank_delta",
    "support_delta",
    "distinct_column_types_before",
    "distinct_column_types_after",
    "new_column_types_added",
]
FORBIDDEN_PAYLOAD_FIELDS = [
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
    "case_id",
    "cycle_n",
    "case_id_as_primary_identity",
    "cycle_n_as_primary_identity",
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


def verify_sources(v03_failure_diag: dict[str, Any], v03_failure_receipt: dict[str, Any], v03_probe: dict[str, Any], v02_scale: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if v03_failure_diag.get("diagnostic_id") != EXPECTED_V03_FAILURE_DIAG_ID:
        failures.append(f"v03_failure_diagnostic_id_wrong:{v03_failure_diag.get('diagnostic_id')}")
    if v03_failure_receipt.get("receipt_id") != EXPECTED_V03_FAILURE_DIAG_RECEIPT_ID:
        failures.append(f"v03_failure_diagnostic_receipt_id_wrong:{v03_failure_receipt.get('receipt_id')}")
    if v03_failure_diag.get("gate") != "PASS":
        failures.append(f"v03_failure_diagnostic_gate_not_PASS:{v03_failure_diag.get('gate')}")
    if v03_failure_receipt.get("gate") != "PASS":
        failures.append(f"v03_failure_diagnostic_receipt_gate_not_PASS:{v03_failure_receipt.get('gate')}")
    if v03_failure_diag.get("diagnosis_status") != "DIAGNOSED":
        failures.append(f"v03_failure_diagnosis_status_wrong:{v03_failure_diag.get('diagnosis_status')}")

    if v03_failure_diag.get("source_v03_probe_id") != EXPECTED_V03_PROBE_ID:
        failures.append(f"source_v03_probe_wrong:{v03_failure_diag.get('source_v03_probe_id')}")
    if v03_failure_diag.get("source_v03_receipt_id") != EXPECTED_V03_RECEIPT_ID:
        failures.append(f"source_v03_receipt_wrong:{v03_failure_diag.get('source_v03_receipt_id')}")
    if v03_failure_diag.get("source_v03_policy_id") != EXPECTED_V03_POLICY_ID:
        failures.append(f"source_v03_policy_wrong:{v03_failure_diag.get('source_v03_policy_id')}")
    if v03_failure_diag.get("source_v02_scale_probe_id") != EXPECTED_V02_SCALE_PROBE_ID:
        failures.append(f"source_v02_scale_probe_wrong:{v03_failure_diag.get('source_v02_scale_probe_id')}")

    classification = v03_failure_diag.get("classification") or {}
    if classification.get("primary_class") != "BUCKETIZATION_COLLAPSED_RAW_DELTA_DIFFERENCE":
        failures.append(f"classification_not_bucketization_collapse:{classification.get('primary_class')}")
    if classification.get("burden_class") != "BURDEN_REGRESSION_CONFIRMED":
        failures.append(f"burden_class_not_regression:{classification.get('burden_class')}")

    summary = v03_failure_diag.get("summary") or {}
    if summary.get("source_terminal_decision") != "FAIL_V0_3_FALSE_MERGE_PERSISTS":
        failures.append(f"source_terminal_wrong:{summary.get('source_terminal_decision')}")
    if summary.get("known_failed_bands_cleared") is not False:
        failures.append("known_failed_bands_claimed_cleared")
    if summary.get("known_failed_remaining_false_merge_bands") != 10:
        failures.append(f"known_failed_remaining_false_merge_bands_not_10:{summary.get('known_failed_remaining_false_merge_bands')}")
    if summary.get("worst_burden_ratio_projected", 0) <= 1.0:
        failures.append(f"v03_burden_regression_missing:{summary.get('worst_burden_ratio_projected')}")
    if summary.get("raw_delta_differing_column_counts", {}).get(TARGET_RAW_DELTA_FIELD) != 10:
        failures.append(f"compression_ratio_raw_difference_not_10:{summary.get('raw_delta_differing_column_counts')}")
    if summary.get("bucket_delta_differing_column_counts") not in ({}, None):
        failures.append(f"bucket_delta_difference_unexpected:{summary.get('bucket_delta_differing_column_counts')}")
    if summary.get("failed_reason_counts", {}).get("false_merge") != 10:
        failures.append(f"false_merge_count_not_10:{summary.get('failed_reason_counts')}")
    if summary.get("failed_reason_counts", {}).get("burden_regression") != 266:
        failures.append(f"burden_regression_count_not_266:{summary.get('failed_reason_counts')}")

    decision = v03_failure_diag.get("decision") or {}
    expected_true = [
        "candidate_v0_3_rejected_for_scale_acceptance",
        "candidate_v0_3_rejected_for_burden",
        "authority_side_clean",
        "source_surface_clean",
        "identity_leak_absent",
        "delta_bucket_coverage_clean",
        "do_not_accept_candidate",
        "do_not_full_registry_scan",
        "do_not_change_runtime",
        "do_not_patch_by_adding_case_id_or_cycle_n_as_primary_identity",
        "do_not_patch_by_adding_rowid_or_receipt_hash",
    ]
    for key in expected_true:
        if decision.get(key) is not True:
            failures.append(f"decision_expected_true:{key}:{decision.get(key)}")
    if decision.get("primary_blocker") != "FALSE_MERGE_PERSISTS_AND_BURDEN_REGRESSED":
        failures.append(f"primary_blocker_wrong:{decision.get('primary_blocker')}")
    if decision.get("recommended_next_command_goal") != POLICY_NAME:
        failures.append(f"recommended_next_command_goal_wrong:{decision.get('recommended_next_command_goal')}")

    auth = v03_failure_diag.get("authority") or {}
    if auth.get("observer_only") is not True:
        failures.append("v03_failure_diag_not_observer_only")
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
        "authorizes_rowid_or_receipt_hash_patch",
    ]:
        if auth.get(key) is not False:
            failures.append(f"v03_failure_diag_illegal_authority:{key}:{auth.get(key)}")

    if v03_probe.get("probe_id") != EXPECTED_V03_PROBE_ID:
        failures.append(f"v03_probe_id_wrong:{v03_probe.get('probe_id')}")
    if v03_probe.get("receipt_id") != EXPECTED_V03_RECEIPT_ID:
        failures.append(f"v03_receipt_id_wrong:{v03_probe.get('receipt_id')}")
    if v03_probe.get("terminal_decision") != "FAIL_V0_3_FALSE_MERGE_PERSISTS":
        failures.append(f"v03_terminal_wrong:{v03_probe.get('terminal_decision')}")
    if v03_probe.get("bounded_source_surface", {}).get("full_registry_used") is not False:
        failures.append("v03_probe_used_full_registry")
    if v03_probe.get("pass_gates", {}).get("no_identity_leak") is not True:
        failures.append("v03_identity_leak_gate_not_true")

    if v02_scale.get("probe_id") != EXPECTED_V02_SCALE_PROBE_ID:
        failures.append(f"v02_scale_probe_id_wrong:{v02_scale.get('probe_id')}")
    if v02_scale.get("terminal_decision") != "FAIL_SCALE_FALSE_MERGE":
        failures.append(f"v02_scale_terminal_wrong:{v02_scale.get('terminal_decision')}")
    if v02_scale.get("scale_coverage", {}).get("full_registry_used") is not False:
        failures.append("v02_scale_used_full_registry")
    if v02_scale.get("pass_gates", {}).get("no_false_merge_all_bands") is not False:
        failures.append("v02_false_merge_gate_not_false")

    return failures


def build_policy(source_diagnostic_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    v03_failure_diag = load_json(V03_FAILURE_DIAG_DIR / f"{source_diagnostic_id}.json")
    v03_failure_receipt = load_json(V03_FAILURE_DIAG_RECEIPT_DIR / f"{source_diagnostic_id}.json")
    v03_probe = load_json(V03_RECEIPT_DIR / f"{EXPECTED_V03_PROBE_ID}.json")
    v02_scale = load_json(V02_SCALE_RECEIPT_DIR / f"{EXPECTED_V02_SCALE_PROBE_ID}.json")

    failures = verify_sources(v03_failure_diag, v03_failure_receipt, v03_probe, v02_scale)

    diagnostic_contract = {
        "diagnostic_name": DIAGNOSTIC_NAME,
        "diagnostic_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "source_question": "Can a compact raw compression_ratio encoding preserve the separability that bucketization erased, without exceeding full receipt burden?",
        "bounded_source_surface": {
            "v02_scale_probe_id": EXPECTED_V02_SCALE_PROBE_ID,
            "v02_scale_rows_path": v02_scale.get("scale_band_rows_path"),
            "v03_probe_id": EXPECTED_V03_PROBE_ID,
            "v03_rows_path": v03_probe.get("v03_rows_path"),
            "v03_failure_diagnostic_id": EXPECTED_V03_FAILURE_DIAG_ID,
            "bounded_default_required": True,
            "full_registry_forbidden": True,
            "known_failed_bands_total": 10,
            "all_bands_total": 266,
        },
        "target_raw_delta_fields": ALLOWED_RAW_DELTA_FIELDS,
        "context_only_delta_fields": CONTEXT_ONLY_DELTA_FIELDS,
        "must_inspect_collision_groups": True,
        "must_focus_known_failed_bands": True,
        "must_measure_all_bands_for_burden_context": True,
        "must_not_create_candidate": True,
        "must_not_accept_candidate": True,
        "encoding_candidates_to_measure": [
            {
                "encoding_id": "raw_decimal_string_exact",
                "description": "Canonical string of raw compression_ratio as found in v02 compact_delta_debug.raw.",
                "purpose": "Upper-bound distinguishability, likely burden-heavy.",
            },
            {
                "encoding_id": "raw_decimal_sig6",
                "description": "Canonical significant-digit decimal string with 6 significant digits.",
                "purpose": "Small candidate; may preserve enough separability.",
            },
            {
                "encoding_id": "raw_decimal_sig9",
                "description": "Canonical significant-digit decimal string with 9 significant digits.",
                "purpose": "Middle candidate; tests whether bucket collapse can be repaired cheaply.",
            },
            {
                "encoding_id": "raw_decimal_sig12",
                "description": "Canonical significant-digit decimal string with 12 significant digits.",
                "purpose": "High precision candidate before exact raw string.",
            },
            {
                "encoding_id": "raw_delta_microhash_32",
                "description": "32-bit hash of canonical raw compression_ratio value only, not receipt/hash/identity.",
                "purpose": "Compact discriminator stress test; must report collision risk and must not be accepted as proof.",
            },
        ],
        "forbidden_payload_fields": FORBIDDEN_PAYLOAD_FIELDS,
        "truth_surface": "full_occurrence_key_to_candidate_delta_signature",
        "required_measurements": {
            "per_encoding_known_failed_false_merge_count": True,
            "per_encoding_all_band_false_merge_count": True,
            "per_encoding_burden_ratio_projected": True,
            "per_encoding_signature_payload_bytes": True,
            "per_encoding_raw_delta_coverage": True,
            "per_encoding_collision_gallery": True,
            "compare_against_v02_and_v03": True,
        },
        "diagnostic_terminal_classes": {
            "RAW_DELTA_COMPACT_ENCODING_POSSIBLY_VIABLE": "At least one compact raw-delta encoding clears known false merges and keeps burden below full receipt burden. Still diagnostic only.",
            "RAW_DELTA_ONLY_EXACT_VIABLE_BUT_TOO_HEAVY": "Only exact/raw-heavy encoding clears false merges, or compact versions fail; no candidate yet.",
            "RAW_DELTA_NOT_VIABLE": "Raw compression_ratio does not clear false merges even before burden constraints.",
            "PAYLOAD_CONSTRUCTION_OR_SOURCE_LINKAGE_FAILURE": "Raw values cannot be reconstructed from v02/v03 row linkage.",
        },
    }

    authority = {
        "observer_only": True,
        "authorizes_next_diagnostic_implementation": True,
        "authorized_next_command_goal": NEXT_COMMAND_GOAL,
        "authorizes_raw_delta_compactness_measurement": True,
        "authorizes_candidate_design": False,
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
        "authorizes_rowid_or_receipt_hash_patch": False,
    }

    implementation_constraints = {
        "must_touch_only_files": [
            "scripts/raw_delta_compactness_diagnostic_v0.py",
        ],
        "must_not_modify_files": [
            "src/",
            "app/",
            "matrixlab/",
            "scripts/stable_delta_signature_candidate_v0_3_probe.py",
            "scripts/diagnose_v0_3_failure_v0.py",
            "scripts/build_stable_delta_signature_candidate_v0_3_policy.py",
            "scripts/stable_delta_signature_candidate_v0_2_scale_band_probe.py",
            "scripts/stable_delta_signature_candidate_v0_2_probe.py",
        ],
        "must_reuse_existing_bounded_rows": True,
        "must_not_read_registry_sqlite": True,
        "must_not_full_registry_scan": True,
        "must_not_accept_candidate": True,
        "must_not_authorize_scale_mode": True,
        "must_not_change_runtime_receipt_emission": True,
    }

    required_negative_controls = [
        {
            "case": "source_classification_not_bucketization_fail",
            "must_fail_if": "v03 failure diagnostic is not BUCKETIZATION_COLLAPSED_RAW_DELTA_DIFFERENCE",
        },
        {
            "case": "raw_compression_ratio_difference_missing_fail",
            "must_fail_if": "raw_delta_differing_column_counts.compression_ratio is absent or zero",
        },
        {
            "case": "bucket_difference_present_unexpected_fail",
            "must_fail_if": "bucket_delta_differing_column_counts is non-empty without explicit policy revision",
        },
        {
            "case": "candidate_creation_fail",
            "must_fail_if": "diagnostic emits candidate acceptance, scale mode, or v0.4 policy",
        },
        {
            "case": "identity_leak_fail",
            "must_fail_if": "case_id, cycle_n, rowid, receipt hash, full occurrence key, audit pointer, or debug payload enter measured signature payload",
        },
        {
            "case": "full_registry_scan_fail",
            "must_fail_if": "diagnostic reads registry.sqlite or uses any run outside the bounded row files",
        },
        {
            "case": "raw_receipt_hash_truth_surface_fail",
            "must_fail_if": "raw/full receipt hash is used as truth surface",
        },
    ]

    policy = {
        "schema_version": "raw_delta_compactness_diagnostic_policy_v0",
        "policy_name": POLICY_NAME,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "source_v03_failure_diagnostic_id": EXPECTED_V03_FAILURE_DIAG_ID,
        "source_v03_failure_diagnostic_receipt_id": EXPECTED_V03_FAILURE_DIAG_RECEIPT_ID,
        "source_v03_probe_id": EXPECTED_V03_PROBE_ID,
        "source_v03_receipt_id": EXPECTED_V03_RECEIPT_ID,
        "source_v03_policy_id": EXPECTED_V03_POLICY_ID,
        "source_v02_scale_probe_id": EXPECTED_V02_SCALE_PROBE_ID,
        "diagnostic_contract": diagnostic_contract,
        "authority": authority,
        "implementation_constraints": implementation_constraints,
        "required_negative_controls": required_negative_controls,
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_RAW_DELTA_COMPACTNESS_DIAGNOSTIC_POLICY_INVALID",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    policy_id = sha8({
        "policy_name": POLICY_NAME,
        "source_v03_failure_diagnostic_id": EXPECTED_V03_FAILURE_DIAG_ID,
        "diagnostic_contract": diagnostic_contract,
        "authority": authority,
        "implementation_constraints": implementation_constraints,
    })
    policy["policy_id"] = policy_id
    policy["policy_sig8"] = policy_id

    receipt = {
        "schema_version": "raw_delta_compactness_diagnostic_policy_receipt_v0",
        "policy_id": policy_id,
        "policy_sig8": policy_id,
        "policy_name": POLICY_NAME,
        "policy_status": policy["policy_status"],
        "policy_path": f"data/raw_delta_compactness_diagnostic_policies/{policy_id}.json",
        "source_v03_failure_diagnostic_id": EXPECTED_V03_FAILURE_DIAG_ID,
        "source_v03_failure_diagnostic_receipt_id": EXPECTED_V03_FAILURE_DIAG_RECEIPT_ID,
        "source_v03_probe_id": EXPECTED_V03_PROBE_ID,
        "source_v03_receipt_id": EXPECTED_V03_RECEIPT_ID,
        "source_v02_scale_probe_id": EXPECTED_V02_SCALE_PROBE_ID,
        "diagnostic_contract_summary": {
            "target_raw_delta_fields": ALLOWED_RAW_DELTA_FIELDS,
            "context_only_delta_fields": CONTEXT_ONLY_DELTA_FIELDS,
            "encoding_candidates_to_measure": [
                e["encoding_id"] for e in diagnostic_contract["encoding_candidates_to_measure"]
            ],
            "known_failed_bands_total": 10,
            "all_bands_total": 266,
            "full_registry_forbidden": True,
            "candidate_creation_forbidden": True,
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
    parser.add_argument("--source-diagnostic-id", default=EXPECTED_V03_FAILURE_DIAG_ID)
    args = parser.parse_args()

    policy, receipt = build_policy(args.source_diagnostic_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_id={policy['policy_id']}")
    print(f"policy_json_path=data/raw_delta_compactness_diagnostic_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/raw_delta_compactness_diagnostic_policy_receipts/{policy['policy_id']}.json")

    return 0 if policy["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
