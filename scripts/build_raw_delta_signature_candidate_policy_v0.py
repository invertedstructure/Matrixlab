#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

RAW_DELTA_DIAG_DIR = ROOT / "data" / "raw_delta_compactness_diagnostics"
RAW_DELTA_DIAG_RECEIPT_DIR = ROOT / "data" / "raw_delta_compactness_diagnostic_receipts"
RAW_DELTA_POLICY_DIR = ROOT / "data" / "raw_delta_compactness_diagnostic_policies"
RAW_DELTA_POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_compactness_diagnostic_policy_receipts"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_policy_receipts"

EXPECTED_RAW_DELTA_DIAGNOSTIC_ID = "74caa0f4"
EXPECTED_RAW_DELTA_DIAGNOSTIC_RECEIPT_ID = "129e9a76"
EXPECTED_RAW_DELTA_POLICY_ID = "445bdd02"
EXPECTED_RAW_DELTA_POLICY_RECEIPT_ID = "25a019a1"
EXPECTED_V03_FAILURE_DIAGNOSTIC_ID = "d0132dd4"
EXPECTED_V03_PROBE_ID = "bd1beabe"
EXPECTED_V02_SCALE_PROBE_ID = "227e9426"

POLICY_NAME = "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_POLICY_V0"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"
NEXT_COMMAND_GOAL = "IMPLEMENT_RAW_DELTA_SIGNATURE_CANDIDATE_PROBE_V0"

SELECTED_ENCODING_ID = "raw_decimal_sig6"
TARGET_RAW_DELTA_FIELD = "compression_ratio"

CANDIDATE_REQUIRED_FIELDS = [
    "cv",
    "state_hash_before",
    "move_id",
    "state_hash_after",
    "raw_compression_ratio_sig6",
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
    "case_id",
    "cycle_n",
    "case_id_as_primary_identity",
    "cycle_n_as_primary_identity",
    "depth_as_primary_identity",
    "raw_delta_microhash_32_as_proof",
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


def verify_sources(
    raw_diag: dict[str, Any],
    raw_diag_receipt: dict[str, Any],
    raw_policy: dict[str, Any],
    raw_policy_receipt: dict[str, Any],
) -> list[str]:
    failures: list[str] = []

    if raw_diag.get("diagnostic_id") != EXPECTED_RAW_DELTA_DIAGNOSTIC_ID:
        failures.append(f"raw_delta_diagnostic_id_wrong:{raw_diag.get('diagnostic_id')}")
    if raw_diag_receipt.get("receipt_id") != EXPECTED_RAW_DELTA_DIAGNOSTIC_RECEIPT_ID:
        failures.append(f"raw_delta_diagnostic_receipt_id_wrong:{raw_diag_receipt.get('receipt_id')}")
    if raw_diag.get("gate") != "PASS":
        failures.append(f"raw_delta_diagnostic_gate_not_PASS:{raw_diag.get('gate')}")
    if raw_diag_receipt.get("gate") != "PASS":
        failures.append(f"raw_delta_diagnostic_receipt_gate_not_PASS:{raw_diag_receipt.get('gate')}")
    if raw_diag.get("diagnosis_status") != "DIAGNOSED":
        failures.append(f"raw_delta_diagnosis_status_wrong:{raw_diag.get('diagnosis_status')}")
    if raw_diag.get("mode") != "OUTER_OBSERVER_ONLY":
        failures.append(f"raw_delta_mode_wrong:{raw_diag.get('mode')}")

    if raw_diag.get("source_policy_id") != EXPECTED_RAW_DELTA_POLICY_ID:
        failures.append(f"raw_delta_source_policy_wrong:{raw_diag.get('source_policy_id')}")
    if raw_diag.get("source_v03_failure_diagnostic_id") != EXPECTED_V03_FAILURE_DIAGNOSTIC_ID:
        failures.append(f"raw_delta_source_v03_failure_diag_wrong:{raw_diag.get('source_v03_failure_diagnostic_id')}")
    if raw_diag.get("source_v03_probe_id") != EXPECTED_V03_PROBE_ID:
        failures.append(f"raw_delta_source_v03_probe_wrong:{raw_diag.get('source_v03_probe_id')}")
    if raw_diag.get("source_v02_scale_probe_id") != EXPECTED_V02_SCALE_PROBE_ID:
        failures.append(f"raw_delta_source_v02_scale_probe_wrong:{raw_diag.get('source_v02_scale_probe_id')}")

    bounded = raw_diag.get("bounded_source_surface") or {}
    if bounded.get("known_failed_bands_total") != 10:
        failures.append(f"known_failed_bands_total_not_10:{bounded.get('known_failed_bands_total')}")
    if bounded.get("all_bands_total") != 266:
        failures.append(f"all_bands_total_not_266:{bounded.get('all_bands_total')}")
    if bounded.get("full_registry_used") is not False:
        failures.append(f"full_registry_used_not_false:{bounded.get('full_registry_used')}")
    if bounded.get("registry_sqlite_read") is not False:
        failures.append(f"registry_sqlite_read_not_false:{bounded.get('registry_sqlite_read')}")

    classification = raw_diag.get("classification") or {}
    if classification.get("terminal_class") != "RAW_DELTA_COMPACT_ENCODING_POSSIBLY_VIABLE":
        failures.append(f"terminal_class_wrong:{classification.get('terminal_class')}")
    if classification.get("recommended_next_command_goal") != POLICY_NAME:
        failures.append(f"recommended_next_goal_wrong:{classification.get('recommended_next_command_goal')}")
    if SELECTED_ENCODING_ID not in set(classification.get("compact_viable_encodings") or []):
        failures.append(f"selected_encoding_not_compact_viable:{classification.get('compact_viable_encodings')}")
    if SELECTED_ENCODING_ID not in set(classification.get("encodings_clearing_known_false_merges") or []):
        failures.append(f"selected_encoding_not_clearing_false_merges:{classification.get('encodings_clearing_known_false_merges')}")
    if SELECTED_ENCODING_ID not in set(classification.get("encodings_viable_on_known_failed_bands") or []):
        failures.append(f"selected_encoding_not_viable_on_known_failed:{classification.get('encodings_viable_on_known_failed_bands')}")

    summaries = raw_diag.get("encoding_summaries") or {}
    selected = summaries.get(SELECTED_ENCODING_ID) or {}
    if selected.get("encoding_id") != SELECTED_ENCODING_ID:
        failures.append(f"selected_encoding_summary_missing:{selected.get('encoding_id')}")
    if selected.get("all_bands_clear") is not True:
        failures.append(f"selected_all_bands_not_clear:{selected.get('all_bands_clear')}")
    if selected.get("known_failed_all_clear") is not True:
        failures.append(f"selected_known_failed_not_clear:{selected.get('known_failed_all_clear')}")
    if selected.get("known_failed_false_merge_bands") != 0:
        failures.append(f"selected_known_failed_false_merge_bands_not_0:{selected.get('known_failed_false_merge_bands')}")
    if selected.get("all_band_false_merge_bands") != 0:
        failures.append(f"selected_all_band_false_merge_bands_not_0:{selected.get('all_band_false_merge_bands')}")
    if selected.get("worst_false_merge_count") != 0:
        failures.append(f"selected_worst_false_merge_not_0:{selected.get('worst_false_merge_count')}")
    if selected.get("worst_collision_count") != 0:
        failures.append(f"selected_worst_collision_not_0:{selected.get('worst_collision_count')}")
    if selected.get("worst_distinguishability_retention_ratio") != 1.0:
        failures.append(f"selected_retention_not_1:{selected.get('worst_distinguishability_retention_ratio')}")
    if not (selected.get("worst_burden_ratio_projected", 999) < 1.0):
        failures.append(f"selected_burden_not_below_full:{selected.get('worst_burden_ratio_projected')}")
    if selected.get("worst_identity_leak_count") != 0:
        failures.append(f"selected_identity_leak:{selected.get('worst_identity_leak_count')}")
    if selected.get("worst_raw_delta_missing_count") != 0:
        failures.append(f"selected_raw_delta_missing:{selected.get('worst_raw_delta_missing_count')}")
    if selected.get("worst_source_surface_regression_count") != 0:
        failures.append(f"selected_source_surface_regression:{selected.get('worst_source_surface_regression_count')}")

    # We select sig6 because it is the lowest-burden non-hash compact viable encoding.
    for enc, summary in summaries.items():
        if enc == "raw_delta_microhash_32":
            continue
        if summary.get("all_bands_clear") is True and summary.get("known_failed_all_clear") is True:
            if selected.get("total_projected_plus_signature_payload_bytes", 999999999) > summary.get("total_projected_plus_signature_payload_bytes", 0):
                failures.append(
                    f"selected_not_lowest_burden_non_hash_viable:{SELECTED_ENCODING_ID}:{selected.get('total_projected_plus_signature_payload_bytes')} > {enc}:{summary.get('total_projected_plus_signature_payload_bytes')}"
                )

    comparison = raw_diag.get("comparison_to_v02_v03") or {}
    if comparison.get("v02_terminal_decision") != "FAIL_SCALE_FALSE_MERGE":
        failures.append(f"v02_terminal_wrong:{comparison.get('v02_terminal_decision')}")
    if comparison.get("v02_worst_false_merge_count") != 1:
        failures.append(f"v02_worst_false_merge_wrong:{comparison.get('v02_worst_false_merge_count')}")
    if comparison.get("v03_terminal_decision") != "FAIL_V0_3_FALSE_MERGE_PERSISTS":
        failures.append(f"v03_terminal_wrong:{comparison.get('v03_terminal_decision')}")
    if comparison.get("v03_worst_false_merge_count") != 1:
        failures.append(f"v03_worst_false_merge_wrong:{comparison.get('v03_worst_false_merge_count')}")
    if not (comparison.get("v03_worst_burden_ratio_projected", 0) > 1.0):
        failures.append(f"v03_burden_regression_missing:{comparison.get('v03_worst_burden_ratio_projected')}")

    decision = raw_diag.get("decision") or {}
    expected_true = [
        "diagnostic_only",
        "do_not_accept_candidate",
        "do_not_full_registry_scan",
        "do_not_change_runtime",
        "do_not_use_case_id_or_cycle_n_as_primary_identity",
        "do_not_use_rowid_or_receipt_hash",
    ]
    for key in expected_true:
        if decision.get(key) is not True:
            failures.append(f"decision_expected_true:{key}:{decision.get(key)}")
    if decision.get("candidate_created") is not False:
        failures.append(f"candidate_created_not_false:{decision.get('candidate_created')}")
    if decision.get("candidate_accepted") is not False:
        failures.append(f"candidate_accepted_not_false:{decision.get('candidate_accepted')}")
    if decision.get("primary_result") != "RAW_DELTA_COMPACT_ENCODING_POSSIBLY_VIABLE":
        failures.append(f"primary_result_wrong:{decision.get('primary_result')}")
    if decision.get("recommended_next_command_goal") != POLICY_NAME:
        failures.append(f"decision_next_goal_wrong:{decision.get('recommended_next_command_goal')}")

    auth = raw_diag.get("authority_guards") or {}
    if auth.get("observer_only") is not True:
        failures.append("raw_diag_not_observer_only")
    for key in [
        "candidate_created",
        "candidate_accepted",
        "candidate_design_authorized",
        "scale_mode_authorized",
        "full_registry_scan_used",
        "registry_sqlite_read",
        "registry_sqlite_changed",
        "registry_write_authorized",
        "runtime_receipt_emission_changed",
        "raw_receipt_hash_used_as_truth_surface",
        "case_id_or_cycle_n_primary_identity_patch_used",
        "rowid_or_receipt_hash_patch_used",
    ]:
        if auth.get(key) is not False:
            failures.append(f"raw_diag_authority_guard_not_false:{key}:{auth.get(key)}")

    pass_gates = raw_diag.get("pass_gates") or {}
    for key in [
        "authority_containment",
        "policy_preconditions",
        "bounded_rows_reused",
        "raw_delta_coverage",
        "truth_surface",
        "no_identity_leak",
        "candidate_not_created",
        "candidate_not_accepted",
        "diagnostic_only",
    ]:
        if pass_gates.get(key) is not True:
            failures.append(f"pass_gate_not_true:{key}:{pass_gates.get(key)}")

    if raw_policy.get("policy_id") != EXPECTED_RAW_DELTA_POLICY_ID:
        failures.append(f"raw_policy_id_wrong:{raw_policy.get('policy_id')}")
    if raw_policy_receipt.get("receipt_id") != EXPECTED_RAW_DELTA_POLICY_RECEIPT_ID:
        failures.append(f"raw_policy_receipt_id_wrong:{raw_policy_receipt.get('receipt_id')}")
    if raw_policy.get("authority", {}).get("authorizes_candidate_design") is not False:
        failures.append("raw_policy_authorized_candidate_design_unexpectedly")
    if raw_policy.get("authority", {}).get("authorizes_candidate_acceptance") is not False:
        failures.append("raw_policy_authorized_candidate_acceptance_unexpectedly")

    return failures


def build_policy(source_diagnostic_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    raw_diag = load_json(RAW_DELTA_DIAG_DIR / f"{source_diagnostic_id}.json")
    raw_diag_receipt = load_json(RAW_DELTA_DIAG_RECEIPT_DIR / f"{source_diagnostic_id}.json")
    raw_policy = load_json(RAW_DELTA_POLICY_DIR / f"{EXPECTED_RAW_DELTA_POLICY_ID}.json")
    raw_policy_receipt = load_json(RAW_DELTA_POLICY_RECEIPT_DIR / f"{EXPECTED_RAW_DELTA_POLICY_ID}.json")

    failures = verify_sources(raw_diag, raw_diag_receipt, raw_policy, raw_policy_receipt)
    selected_summary = raw_diag.get("encoding_summaries", {}).get(SELECTED_ENCODING_ID, {})

    candidate_contract = {
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "candidate_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "selected_encoding_id": SELECTED_ENCODING_ID,
        "selected_target_raw_delta_field": TARGET_RAW_DELTA_FIELD,
        "selection_reason": "Lowest-burden non-hash compact viable encoding on the bounded diagnostic surface.",
        "source_evidence": {
            "raw_delta_diagnostic_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_ID,
            "raw_delta_diagnostic_receipt_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_RECEIPT_ID,
            "selected_encoding_summary": selected_summary,
            "comparison_to_v02_v03": raw_diag.get("comparison_to_v02_v03"),
        },
        "signature_payload_required_fields": CANDIDATE_REQUIRED_FIELDS,
        "signature_payload_field_definitions": {
            "cv": "constant candidate version marker raw_delta_signature_v0",
            "state_hash_before": "audit-derived state_sig8_before surfaced through existing v02/v03 rows",
            "move_id": "move identifier from existing bounded source rows",
            "state_hash_after": "audit-derived state_sig8_after surfaced through existing v02/v03 rows",
            "raw_compression_ratio_sig6": "canonical 6-significant-digit decimal encoding of v02 compact_delta_debug.compression_ratio.raw",
        },
        "signature_payload_forbidden_fields": FORBIDDEN_SIGNATURE_FIELDS,
        "truth_surface": "full_occurrence_key_to_candidate_delta_signature",
        "bounded_probe_surface": {
            "must_reuse_raw_delta_diagnostic_rows_path": raw_diag.get("diagnostic_rows_path"),
            "must_reuse_v02_scale_rows_path": raw_diag.get("bounded_source_surface", {}).get("v02_scale_rows_path"),
            "must_reuse_v03_rows_path": raw_diag.get("bounded_source_surface", {}).get("v03_rows_path"),
            "known_failed_bands_total": 10,
            "all_bands_total": 266,
            "full_registry_forbidden": True,
            "registry_sqlite_read_forbidden": True,
        },
        "candidate_probe_required_measurements": {
            "all_band_false_merge_count": True,
            "known_failed_false_merge_count": True,
            "distinguishability_retention_ratio": True,
            "projected_burden_ratio": True,
            "signature_payload_bytes": True,
            "raw_delta_coverage": True,
            "identity_leak_check": True,
            "comparison_to_v02_v03_and_raw_delta_diagnostic": True,
        },
        "pass_gates_for_next_probe": {
            "authority_containment": "observer-only, no candidate acceptance, no scale mode, no registry write, no runtime change",
            "bounded_surface_reused": "use only the existing bounded diagnostic/source rows",
            "raw_delta_coverage": "raw compression_ratio must be present for all evaluated rows",
            "no_identity_leak": "payload excludes case_id/cycle_n/rowid/receipt hash/full occurrence key/audit pointer/debug payload",
            "truth_surface": "compare full_occurrence_key to candidate signature, not receipt hashes",
            "no_false_merge_all_bands": "candidate must clear false merges across all 266 bounded bands",
            "burden_reduction": "projected burden must remain below full receipt burden",
        },
        "terminal_decisions_for_next_probe": {
            "PASS_RAW_DELTA_SIGNATURE_CANDIDATE_BOUNDED_PROBE": "Candidate clears bounded false merges and burden stays below full receipts; still no acceptance.",
            "FAIL_RAW_DELTA_SIGNATURE_FALSE_MERGE": "Candidate still has false merges.",
            "FAIL_RAW_DELTA_SIGNATURE_BURDEN": "Candidate burden is not below full receipts.",
            "FAIL_RAW_DELTA_SIGNATURE_IDENTITY_LEAK": "Forbidden identity/audit/receipt fields entered payload.",
            "FAIL_RAW_DELTA_SIGNATURE_SOURCE_SURFACE": "Raw compression_ratio or transition tuple cannot be reconstructed from bounded rows.",
            "FAIL_RAW_DELTA_SIGNATURE_AUTHORITY": "Observer-only containment is violated.",
        },
        "explicit_non_authorizations": [
            "No candidate acceptance.",
            "No scale mode.",
            "No runtime receipt emission change.",
            "No registry write.",
            "No full-registry scan.",
            "No registry.sqlite read.",
            "No receipt replacement, deletion, compression, or suppression.",
            "No case_id or cycle_n as primary identity.",
            "No rowid, receipt hash, or full occurrence key in payload.",
            "No raw_delta_microhash_32 as proof of identity.",
        ],
    }

    authority = {
        "observer_only": True,
        "authorizes_next_candidate_probe_implementation": True,
        "authorized_next_command_goal": NEXT_COMMAND_GOAL,
        "authorizes_bounded_candidate_probe_execution": True,
        "authorizes_candidate_design_policy_only": True,
        "authorizes_candidate_acceptance": False,
        "authorizes_scale_mode": False,
        "authorizes_full_registry_scan": False,
        "authorizes_registry_sqlite_read": False,
        "authorizes_runtime_receipt_emission_change": False,
        "authorizes_registry_write": False,
        "authorizes_receipt_replacement": False,
        "authorizes_receipt_deletion": False,
        "authorizes_receipt_compression": False,
        "authorizes_receipt_suppression": False,
        "authorizes_raw_receipt_hash_truth_surface": False,
        "authorizes_case_id_or_cycle_n_primary_identity_patch": False,
        "authorizes_rowid_or_receipt_hash_patch": False,
        "authorizes_full_occurrence_key_in_payload": False,
        "authorizes_audit_pointer_in_payload": False,
        "authorizes_debug_payload_in_payload": False,
        "authorizes_microhash_as_proof": False,
    }

    implementation_constraints = {
        "must_touch_only_files": [
            "scripts/raw_delta_signature_candidate_probe_v0.py",
        ],
        "must_not_modify_files": [
            "src/",
            "app/",
            "matrixlab/",
            "scripts/raw_delta_compactness_diagnostic_v0.py",
            "scripts/build_raw_delta_compactness_diagnostic_policy_v0.py",
            "scripts/stable_delta_signature_candidate_v0_3_probe.py",
            "scripts/diagnose_v0_3_failure_v0.py",
            "scripts/stable_delta_signature_candidate_v0_2_scale_band_probe.py",
            "scripts/stable_delta_signature_candidate_v0_2_probe.py",
        ],
        "must_reuse_existing_bounded_rows": True,
        "must_not_read_registry_sqlite": True,
        "must_not_full_registry_scan": True,
        "must_not_accept_candidate": True,
        "must_not_authorize_scale_mode": True,
        "must_not_change_runtime_receipt_emission": True,
        "must_not_write_registry": True,
    }

    required_negative_controls = [
        {
            "case": "selected_encoding_not_viable_fail",
            "must_fail_if": "raw_decimal_sig6 does not clear all bounded bands or known failed bands",
        },
        {
            "case": "selected_encoding_burden_regression_fail",
            "must_fail_if": "raw_decimal_sig6 projected burden is >= full receipt burden",
        },
        {
            "case": "identity_leak_fail",
            "must_fail_if": "case_id, cycle_n, rowid, receipt hash, full_occurrence_key, audit pointer, or debug payload enter signature payload",
        },
        {
            "case": "microhash_as_proof_fail",
            "must_fail_if": "raw_delta_microhash_32 is selected as proof instead of measured as diagnostic stress test",
        },
        {
            "case": "candidate_acceptance_fail",
            "must_fail_if": "policy or next probe accepts candidate or authorizes scale mode",
        },
        {
            "case": "full_registry_or_registry_sqlite_fail",
            "must_fail_if": "next probe reads registry.sqlite or scans outside bounded row files",
        },
        {
            "case": "receipt_hash_truth_surface_fail",
            "must_fail_if": "raw/full receipt hash is used as truth surface",
        },
    ]

    policy = {
        "schema_version": "raw_delta_signature_candidate_policy_v0",
        "policy_name": POLICY_NAME,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_raw_delta_diagnostic_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_ID,
        "source_raw_delta_diagnostic_receipt_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_RECEIPT_ID,
        "source_raw_delta_policy_id": EXPECTED_RAW_DELTA_POLICY_ID,
        "source_v03_failure_diagnostic_id": EXPECTED_V03_FAILURE_DIAGNOSTIC_ID,
        "source_v03_probe_id": EXPECTED_V03_PROBE_ID,
        "source_v02_scale_probe_id": EXPECTED_V02_SCALE_PROBE_ID,
        "candidate_contract": candidate_contract,
        "authority": authority,
        "implementation_constraints": implementation_constraints,
        "required_negative_controls": required_negative_controls,
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_RAW_DELTA_SIGNATURE_CANDIDATE_POLICY_INVALID",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    policy_id = sha8({
        "policy_name": POLICY_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_raw_delta_diagnostic_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_ID,
        "candidate_contract": candidate_contract,
        "authority": authority,
        "implementation_constraints": implementation_constraints,
    })
    policy["policy_id"] = policy_id
    policy["policy_sig8"] = policy_id

    receipt = {
        "schema_version": "raw_delta_signature_candidate_policy_receipt_v0",
        "policy_id": policy_id,
        "policy_sig8": policy_id,
        "policy_name": POLICY_NAME,
        "policy_status": policy["policy_status"],
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "policy_path": f"data/raw_delta_signature_candidate_policies/{policy_id}.json",
        "source_raw_delta_diagnostic_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_ID,
        "source_raw_delta_diagnostic_receipt_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_RECEIPT_ID,
        "source_raw_delta_policy_id": EXPECTED_RAW_DELTA_POLICY_ID,
        "source_v03_failure_diagnostic_id": EXPECTED_V03_FAILURE_DIAGNOSTIC_ID,
        "source_v03_probe_id": EXPECTED_V03_PROBE_ID,
        "source_v02_scale_probe_id": EXPECTED_V02_SCALE_PROBE_ID,
        "candidate_contract_summary": {
            "selected_encoding_id": SELECTED_ENCODING_ID,
            "selected_target_raw_delta_field": TARGET_RAW_DELTA_FIELD,
            "signature_payload_required_fields": CANDIDATE_REQUIRED_FIELDS,
            "known_failed_all_clear": selected_summary.get("known_failed_all_clear"),
            "all_bands_clear": selected_summary.get("all_bands_clear"),
            "worst_burden_ratio_projected": selected_summary.get("worst_burden_ratio_projected"),
            "worst_false_merge_count": selected_summary.get("worst_false_merge_count"),
            "worst_distinguishability_retention_ratio": selected_summary.get("worst_distinguishability_retention_ratio"),
            "full_registry_forbidden": True,
            "candidate_acceptance_forbidden": True,
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
    parser.add_argument("--source-diagnostic-id", default=EXPECTED_RAW_DELTA_DIAGNOSTIC_ID)
    args = parser.parse_args()

    policy, receipt = build_policy(args.source_diagnostic_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_id={policy['policy_id']}")
    print(f"policy_json_path=data/raw_delta_signature_candidate_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/raw_delta_signature_candidate_policy_receipts/{policy['policy_id']}.json")

    return 0 if policy["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
