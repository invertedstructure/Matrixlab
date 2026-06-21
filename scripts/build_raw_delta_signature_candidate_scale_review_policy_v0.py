#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CANDIDATE_PROBE_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_probe_receipts"
CANDIDATE_POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_policies"
CANDIDATE_POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_policy_receipts"
RAW_DELTA_DIAG_DIR = ROOT / "data" / "raw_delta_compactness_diagnostics"
RAW_DELTA_DIAG_RECEIPT_DIR = ROOT / "data" / "raw_delta_compactness_diagnostic_receipts"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_scale_review_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_scale_review_policy_receipts"

EXPECTED_CANDIDATE_PROBE_ID = "6a33c978"
EXPECTED_CANDIDATE_PROBE_RECEIPT_ID = "99c90fe3"
EXPECTED_CANDIDATE_POLICY_ID = "3b8eb867"
EXPECTED_CANDIDATE_POLICY_RECEIPT_ID = "6778ef03"
EXPECTED_RAW_DELTA_DIAGNOSTIC_ID = "74caa0f4"
EXPECTED_RAW_DELTA_DIAGNOSTIC_RECEIPT_ID = "129e9a76"
EXPECTED_V02_SCALE_PROBE_ID = "227e9426"
EXPECTED_V03_PROBE_ID = "bd1beabe"
EXPECTED_V03_FAILURE_DIAGNOSTIC_ID = "d0132dd4"

POLICY_NAME = "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_SCALE_REVIEW_POLICY_V0"
REVIEW_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_SCALE_REVIEW_V0"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"
NEXT_COMMAND_GOAL = "IMPLEMENT_RAW_DELTA_SIGNATURE_CANDIDATE_SCALE_REVIEW_V0"

SELECTED_ENCODING_ID = "raw_decimal_sig6"
TARGET_RAW_DELTA_FIELD = "compression_ratio"

REQUIRED_CANDIDATE_PAYLOAD_FIELDS = [
    "cv",
    "state_hash_before",
    "move_id",
    "state_hash_after",
    "raw_compression_ratio_sig6",
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
    candidate_probe: dict[str, Any],
    candidate_policy: dict[str, Any],
    candidate_policy_receipt: dict[str, Any],
    raw_diag: dict[str, Any],
    raw_diag_receipt: dict[str, Any],
) -> list[str]:
    failures: list[str] = []

    if candidate_probe.get("probe_id") != EXPECTED_CANDIDATE_PROBE_ID:
        failures.append(f"candidate_probe_id_wrong:{candidate_probe.get('probe_id')}")
    if candidate_probe.get("receipt_id") != EXPECTED_CANDIDATE_PROBE_RECEIPT_ID:
        failures.append(f"candidate_probe_receipt_id_wrong:{candidate_probe.get('receipt_id')}")
    if candidate_probe.get("gate") != "PASS":
        failures.append(f"candidate_probe_gate_not_PASS:{candidate_probe.get('gate')}")
    if candidate_probe.get("mode") != "OUTER_OBSERVER_ONLY":
        failures.append(f"candidate_probe_mode_wrong:{candidate_probe.get('mode')}")
    if candidate_probe.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"candidate_design_wrong:{candidate_probe.get('candidate_design_id')}")
    if candidate_probe.get("terminal_decision") != "PASS_RAW_DELTA_SIGNATURE_CANDIDATE_BOUNDED_PROBE":
        failures.append(f"candidate_probe_terminal_wrong:{candidate_probe.get('terminal_decision')}")
    if candidate_probe.get("terminal", {}).get("next_command_goal") != POLICY_NAME:
        failures.append(f"candidate_probe_next_goal_wrong:{candidate_probe.get('terminal', {}).get('next_command_goal')}")

    if candidate_probe.get("source_policy_id") != EXPECTED_CANDIDATE_POLICY_ID:
        failures.append(f"candidate_probe_source_policy_wrong:{candidate_probe.get('source_policy_id')}")
    if candidate_probe.get("source_policy_receipt_id") != EXPECTED_CANDIDATE_POLICY_RECEIPT_ID:
        failures.append(f"candidate_probe_source_policy_receipt_wrong:{candidate_probe.get('source_policy_receipt_id')}")
    if candidate_probe.get("source_raw_delta_diagnostic_id") != EXPECTED_RAW_DELTA_DIAGNOSTIC_ID:
        failures.append(f"candidate_probe_source_raw_diag_wrong:{candidate_probe.get('source_raw_delta_diagnostic_id')}")
    if candidate_probe.get("source_raw_delta_diagnostic_receipt_id") != EXPECTED_RAW_DELTA_DIAGNOSTIC_RECEIPT_ID:
        failures.append(f"candidate_probe_source_raw_diag_receipt_wrong:{candidate_probe.get('source_raw_delta_diagnostic_receipt_id')}")
    if candidate_probe.get("source_v02_scale_probe_id") != EXPECTED_V02_SCALE_PROBE_ID:
        failures.append(f"candidate_probe_source_v02_scale_wrong:{candidate_probe.get('source_v02_scale_probe_id')}")
    if candidate_probe.get("source_v03_probe_id") != EXPECTED_V03_PROBE_ID:
        failures.append(f"candidate_probe_source_v03_wrong:{candidate_probe.get('source_v03_probe_id')}")

    contract = candidate_probe.get("candidate_contract") or {}
    if contract.get("selected_encoding_id") != SELECTED_ENCODING_ID:
        failures.append(f"selected_encoding_wrong:{contract.get('selected_encoding_id')}")
    if contract.get("selected_target_raw_delta_field") != TARGET_RAW_DELTA_FIELD:
        failures.append(f"selected_target_wrong:{contract.get('selected_target_raw_delta_field')}")
    if contract.get("signature_payload_required_fields") != REQUIRED_CANDIDATE_PAYLOAD_FIELDS:
        failures.append(f"payload_fields_wrong:{contract.get('signature_payload_required_fields')}")
    if contract.get("truth_surface") != "full_occurrence_key_to_candidate_delta_signature":
        failures.append(f"truth_surface_wrong:{contract.get('truth_surface')}")
    forbidden = set(contract.get("signature_payload_forbidden_fields") or [])
    for field in [
        "full_occurrence_key",
        "raw_full_receipt_hash",
        "receipt_hash",
        "rowid",
        "audit_pointer",
        "debug_payload",
        "case_id",
        "cycle_n",
        "raw_delta_microhash_32_as_proof",
    ]:
        if field not in forbidden:
            failures.append(f"forbidden_payload_field_missing:{field}")

    surface = candidate_probe.get("bounded_source_surface") or {}
    if surface.get("raw_delta_diagnostic_rows_path") != "data/raw_delta_compactness_rows/74caa0f4.jsonl":
        failures.append(f"raw_delta_rows_path_wrong:{surface.get('raw_delta_diagnostic_rows_path')}")
    if surface.get("selected_encoding_rows_total") != 3298:
        failures.append(f"selected_encoding_rows_wrong:{surface.get('selected_encoding_rows_total')}")
    if surface.get("bands_total") != 266:
        failures.append(f"bands_total_wrong:{surface.get('bands_total')}")
    if surface.get("full_registry_used") is not False:
        failures.append(f"full_registry_used_not_false:{surface.get('full_registry_used')}")
    if surface.get("registry_sqlite_read") is not False:
        failures.append(f"registry_sqlite_read_not_false:{surface.get('registry_sqlite_read')}")

    agg = candidate_probe.get("aggregate_measurements") or {}
    expected_exact = {
        "bands_total": 266,
        "bands_passed": 266,
        "bands_failed": 0,
        "all_band_burden_regression_count": 0,
        "all_band_false_merge_count": 0,
        "worst_false_merge_count": 0,
        "worst_collision_count": 0,
        "worst_false_split_count": 0,
        "worst_distinguishability_retention_ratio": 1.0,
        "worst_identity_leak_count": 0,
        "worst_raw_delta_missing_count": 0,
        "worst_source_surface_regression_count": 0,
        "worst_audit_recoverability_failures": 0,
        "total_full_receipt_bytes": 2870426,
        "total_projected_plus_signature_payload_bytes": 1475169,
    }
    for key, expected in expected_exact.items():
        if agg.get(key) != expected:
            failures.append(f"aggregate_{key}_wrong:{agg.get(key)}")
    if not (agg.get("total_burden_ratio_projected", 999) < 1.0):
        failures.append(f"total_burden_ratio_not_below_1:{agg.get('total_burden_ratio_projected')}")
    if not (agg.get("worst_burden_ratio_projected", 999) < 1.0):
        failures.append(f"worst_burden_ratio_not_below_1:{agg.get('worst_burden_ratio_projected')}")
    if not (0.50 <= agg.get("total_burden_ratio_projected", 0) <= 0.53):
        failures.append(f"total_burden_ratio_outside_expected_window:{agg.get('total_burden_ratio_projected')}")
    if not (0.50 <= agg.get("worst_burden_ratio_projected", 0) <= 0.53):
        failures.append(f"worst_burden_ratio_outside_expected_window:{agg.get('worst_burden_ratio_projected')}")

    pass_gates = candidate_probe.get("pass_gates") or {}
    for key in [
        "audit_recoverability",
        "authority_containment",
        "bounded_surface_reused",
        "burden_reduction",
        "candidate_not_accepted",
        "no_false_merge_all_bands",
        "no_false_split_all_bands",
        "no_identity_leak",
        "policy_preconditions",
        "raw_delta_coverage",
        "scale_mode_not_authorized",
        "source_surface",
        "truth_surface",
    ]:
        if pass_gates.get(key) is not True:
            failures.append(f"pass_gate_not_true:{key}:{pass_gates.get(key)}")

    auth = candidate_probe.get("authority_guards") or {}
    if auth.get("observer_only") is not True:
        failures.append("candidate_probe_not_observer_only")
    for key in [
        "candidate_accepted",
        "scale_mode_authorized",
        "full_registry_scan_used",
        "registry_sqlite_read",
        "registry_sqlite_changed",
        "runtime_receipt_emission_changed",
        "registry_write_authorized",
        "receipt_replacement_authorized",
        "receipt_deletion_authorized",
        "receipt_compression_authorized",
        "receipt_suppression_authorized",
        "raw_receipt_hash_used_as_truth_surface",
        "case_id_or_cycle_n_primary_identity_patch_used",
        "rowid_or_receipt_hash_patch_used",
        "full_occurrence_key_in_payload",
        "audit_pointer_in_payload",
        "debug_payload_in_payload",
        "microhash_as_proof_used",
    ]:
        if auth.get(key) is not False:
            failures.append(f"candidate_probe_authority_guard_not_false:{key}:{auth.get(key)}")

    decision = candidate_probe.get("decision") or {}
    if decision.get("candidate_accepted") is not False:
        failures.append(f"decision_candidate_accepted_not_false:{decision.get('candidate_accepted')}")
    if decision.get("candidate_acceptance_authorized") is not False:
        failures.append(f"decision_candidate_acceptance_authorized_not_false:{decision.get('candidate_acceptance_authorized')}")
    for key in [
        "diagnostic_probe_only",
        "do_not_accept_candidate",
        "do_not_change_runtime",
        "do_not_full_registry_scan",
        "do_not_read_registry_sqlite",
        "do_not_use_case_id_or_cycle_n_as_primary_identity",
        "do_not_use_rowid_or_receipt_hash",
        "do_not_write_registry",
    ]:
        if decision.get(key) is not True:
            failures.append(f"decision_flag_not_true:{key}:{decision.get(key)}")

    if candidate_policy.get("policy_id") != EXPECTED_CANDIDATE_POLICY_ID:
        failures.append(f"candidate_policy_id_wrong:{candidate_policy.get('policy_id')}")
    if candidate_policy_receipt.get("receipt_id") != EXPECTED_CANDIDATE_POLICY_RECEIPT_ID:
        failures.append(f"candidate_policy_receipt_id_wrong:{candidate_policy_receipt.get('receipt_id')}")
    if candidate_policy.get("gate") != "PASS":
        failures.append(f"candidate_policy_gate_not_PASS:{candidate_policy.get('gate')}")
    if candidate_policy.get("authority", {}).get("authorizes_candidate_acceptance") is not False:
        failures.append("candidate_policy_authorized_acceptance")
    if candidate_policy.get("authority", {}).get("authorizes_scale_mode") is not False:
        failures.append("candidate_policy_authorized_scale_mode")
    if candidate_policy.get("authority", {}).get("authorizes_full_registry_scan") is not False:
        failures.append("candidate_policy_authorized_full_registry")
    if candidate_policy.get("authority", {}).get("authorizes_registry_sqlite_read") is not False:
        failures.append("candidate_policy_authorized_registry_sqlite_read")

    if raw_diag.get("diagnostic_id") != EXPECTED_RAW_DELTA_DIAGNOSTIC_ID:
        failures.append(f"raw_diag_id_wrong:{raw_diag.get('diagnostic_id')}")
    if raw_diag_receipt.get("receipt_id") != EXPECTED_RAW_DELTA_DIAGNOSTIC_RECEIPT_ID:
        failures.append(f"raw_diag_receipt_id_wrong:{raw_diag_receipt.get('receipt_id')}")
    if raw_diag.get("gate") != "PASS":
        failures.append(f"raw_diag_gate_not_PASS:{raw_diag.get('gate')}")
    if raw_diag.get("classification", {}).get("terminal_class") != "RAW_DELTA_COMPACT_ENCODING_POSSIBLY_VIABLE":
        failures.append(f"raw_diag_terminal_wrong:{raw_diag.get('classification', {}).get('terminal_class')}")
    if raw_diag.get("decision", {}).get("candidate_created") is not False:
        failures.append("raw_diag_candidate_created")
    if raw_diag.get("authority_guards", {}).get("registry_sqlite_read") is not False:
        failures.append("raw_diag_registry_sqlite_read")

    return failures


def build_policy(source_probe_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    candidate_probe = load_json(CANDIDATE_PROBE_RECEIPT_DIR / f"{source_probe_id}.json")
    candidate_policy = load_json(CANDIDATE_POLICY_DIR / f"{EXPECTED_CANDIDATE_POLICY_ID}.json")
    candidate_policy_receipt = load_json(CANDIDATE_POLICY_RECEIPT_DIR / f"{EXPECTED_CANDIDATE_POLICY_ID}.json")
    raw_diag = load_json(RAW_DELTA_DIAG_DIR / f"{EXPECTED_RAW_DELTA_DIAGNOSTIC_ID}.json")
    raw_diag_receipt = load_json(RAW_DELTA_DIAG_RECEIPT_DIR / f"{EXPECTED_RAW_DELTA_DIAGNOSTIC_ID}.json")

    failures = verify_sources(
        candidate_probe,
        candidate_policy,
        candidate_policy_receipt,
        raw_diag,
        raw_diag_receipt,
    )

    agg = candidate_probe.get("aggregate_measurements") or {}
    source_evidence = candidate_probe.get("comparison_to_source_evidence", {}) or {}

    scale_review_contract = {
        "review_name": REVIEW_NAME,
        "review_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_candidate_probe_id": EXPECTED_CANDIDATE_PROBE_ID,
        "source_candidate_probe_receipt_id": EXPECTED_CANDIDATE_PROBE_RECEIPT_ID,
        "selected_payload": REQUIRED_CANDIDATE_PAYLOAD_FIELDS,
        "selected_encoding_id": SELECTED_ENCODING_ID,
        "selected_target_raw_delta_field": TARGET_RAW_DELTA_FIELD,
        "source_bounded_pass_evidence": {
            "bands_total": agg.get("bands_total"),
            "bands_passed": agg.get("bands_passed"),
            "bands_failed": agg.get("bands_failed"),
            "all_band_false_merge_count": agg.get("all_band_false_merge_count"),
            "worst_false_merge_count": agg.get("worst_false_merge_count"),
            "worst_collision_count": agg.get("worst_collision_count"),
            "worst_false_split_count": agg.get("worst_false_split_count"),
            "worst_distinguishability_retention_ratio": agg.get("worst_distinguishability_retention_ratio"),
            "total_burden_ratio_projected": agg.get("total_burden_ratio_projected"),
            "worst_burden_ratio_projected": agg.get("worst_burden_ratio_projected"),
            "total_full_receipt_bytes": agg.get("total_full_receipt_bytes"),
            "total_projected_plus_signature_payload_bytes": agg.get("total_projected_plus_signature_payload_bytes"),
            "identity_leak_count": agg.get("worst_identity_leak_count"),
            "source_surface_regression_count": agg.get("worst_source_surface_regression_count"),
        },
        "comparison_evidence": source_evidence,
        "review_question": "What next validation radius is allowed after bounded candidate pass, without accepting candidate or enabling unbounded scale?",
        "allowed_review_actions": {
            "compare_candidate_against_prior_v02_v03_raw_delta_evidence": True,
            "inspect_available_bounded_receipt_inventory": True,
            "derive_recommended_next_validation_radius": True,
            "write_review_receipt": True,
        },
        "forbidden_review_actions": {
            "candidate_acceptance": True,
            "scale_mode_acceptance": True,
            "full_registry_scan": True,
            "registry_sqlite_read": True,
            "runtime_receipt_emission_change": True,
            "registry_write": True,
            "receipt_replacement_deletion_compression_or_suppression": True,
            "case_id_or_cycle_n_primary_identity_patch": True,
            "rowid_or_receipt_hash_patch": True,
            "full_occurrence_key_in_signature_payload": True,
            "audit_pointer_or_debug_payload_in_signature_payload": True,
            "raw_delta_microhash_32_as_proof": True,
        },
        "authorized_review_outputs": {
            "may_recommend_bounded_scale_out_policy": True,
            "may_recommend_hold_for_human_review": True,
            "may_recommend_failure_diagnostic_if_new_blocker_found": True,
            "may_not_accept_candidate": True,
            "may_not_authorize_runtime_change": True,
        },
        "review_must_assess": {
            "whether_current_bounded_surface_is_sufficient_for_policy_acceptance": True,
            "whether_more bounded radius is required": True,
            "whether scale-out can remain bounded without full registry": True,
            "whether acceptance should remain forbidden": True,
            "whether raw_decimal_sig6 should remain selected over exact/hash encodings": True,
            "whether burden basis is now source-surface clean": True,
        },
        "candidate_payload_forbidden_fields": FORBIDDEN_PAYLOAD_FIELDS,
        "truth_surface": "full_occurrence_key_to_candidate_delta_signature",
        "review_terminal_classes": {
            "ADVANCE_TO_BOUNDED_SCALE_OUT_POLICY": "Candidate bounded pass is clean, but acceptance needs at least one larger authorized bounded validation radius.",
            "HOLD_FOR_HUMAN_SCALE_DECISION": "Candidate bounded pass is clean, but the next radius or validation inventory is a human decision point.",
            "STOP_SCALE_REVIEW_SOURCE_SURFACE": "Source evidence is insufficient or inconsistent.",
            "STOP_SCALE_REVIEW_AUTHORITY": "Review would require forbidden authority.",
        },
    }

    authority = {
        "observer_only": True,
        "authorizes_next_scale_review_implementation": True,
        "authorized_next_command_goal": NEXT_COMMAND_GOAL,
        "authorizes_scale_review_policy_only": True,
        "authorizes_bounded_inventory_inspection": True,
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
        "authorizes_case_id_or_cycle_n_primary_identity_patch": False,
        "authorizes_rowid_or_receipt_hash_patch": False,
        "authorizes_raw_receipt_hash_truth_surface": False,
        "authorizes_full_occurrence_key_in_payload": False,
        "authorizes_audit_pointer_in_payload": False,
        "authorizes_debug_payload_in_payload": False,
        "authorizes_microhash_as_proof": False,
    }

    implementation_constraints = {
        "must_touch_only_files": [
            "scripts/raw_delta_signature_candidate_scale_review_v0.py",
        ],
        "must_not_modify_files": [
            "src/",
            "app/",
            "matrixlab/",
            "scripts/raw_delta_signature_candidate_probe_v0.py",
            "scripts/build_raw_delta_signature_candidate_policy_v0.py",
            "scripts/raw_delta_compactness_diagnostic_v0.py",
            "scripts/build_raw_delta_compactness_diagnostic_policy_v0.py",
            "scripts/stable_delta_signature_candidate_v0_3_probe.py",
            "scripts/diagnose_v0_3_failure_v0.py",
            "scripts/stable_delta_signature_candidate_v0_2_scale_band_probe.py",
            "scripts/stable_delta_signature_candidate_v0_2_probe.py",
        ],
        "must_reuse_existing_receipts_and_rows": True,
        "must_not_read_registry_sqlite": True,
        "must_not_full_registry_scan": True,
        "must_not_accept_candidate": True,
        "must_not_authorize_scale_mode": True,
        "must_not_change_runtime_receipt_emission": True,
        "must_not_write_registry": True,
    }

    required_negative_controls = [
        {
            "case": "candidate_probe_not_passed_fail",
            "must_fail_if": "source candidate probe terminal is not PASS_RAW_DELTA_SIGNATURE_CANDIDATE_BOUNDED_PROBE",
        },
        {
            "case": "candidate_probe_false_merge_fail",
            "must_fail_if": "source candidate probe contains any false merge/collision/split",
        },
        {
            "case": "candidate_probe_burden_regression_fail",
            "must_fail_if": "source candidate probe burden ratio is >= 1 or source surface is not clean",
        },
        {
            "case": "authority_expansion_fail",
            "must_fail_if": "policy or source evidence authorizes acceptance, full-registry scan, registry read/write, runtime changes, or scale mode",
        },
        {
            "case": "identity_leak_fail",
            "must_fail_if": "case_id, cycle_n, rowid, receipt hash, full_occurrence_key, audit pointer, debug payload, or microhash-as-proof enters signature payload",
        },
        {
            "case": "receipt_hash_truth_surface_fail",
            "must_fail_if": "receipt hash becomes truth surface instead of full_occurrence_key to candidate signature comparison",
        },
    ]

    policy = {
        "schema_version": "raw_delta_signature_candidate_scale_review_policy_v0",
        "policy_name": POLICY_NAME,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "review_name": REVIEW_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_candidate_probe_id": EXPECTED_CANDIDATE_PROBE_ID,
        "source_candidate_probe_receipt_id": EXPECTED_CANDIDATE_PROBE_RECEIPT_ID,
        "source_candidate_policy_id": EXPECTED_CANDIDATE_POLICY_ID,
        "source_raw_delta_diagnostic_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_ID,
        "source_v02_scale_probe_id": EXPECTED_V02_SCALE_PROBE_ID,
        "source_v03_probe_id": EXPECTED_V03_PROBE_ID,
        "scale_review_contract": scale_review_contract,
        "authority": authority,
        "implementation_constraints": implementation_constraints,
        "required_negative_controls": required_negative_controls,
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_RAW_DELTA_SIGNATURE_CANDIDATE_SCALE_REVIEW_POLICY_INVALID",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    policy_id = sha8({
        "policy_name": POLICY_NAME,
        "review_name": REVIEW_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_candidate_probe_id": EXPECTED_CANDIDATE_PROBE_ID,
        "scale_review_contract": scale_review_contract,
        "authority": authority,
        "implementation_constraints": implementation_constraints,
    })
    policy["policy_id"] = policy_id
    policy["policy_sig8"] = policy_id

    receipt = {
        "schema_version": "raw_delta_signature_candidate_scale_review_policy_receipt_v0",
        "policy_id": policy_id,
        "policy_sig8": policy_id,
        "policy_name": POLICY_NAME,
        "policy_status": policy["policy_status"],
        "review_name": REVIEW_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "policy_path": f"data/raw_delta_signature_candidate_scale_review_policies/{policy_id}.json",
        "source_candidate_probe_id": EXPECTED_CANDIDATE_PROBE_ID,
        "source_candidate_probe_receipt_id": EXPECTED_CANDIDATE_PROBE_RECEIPT_ID,
        "source_candidate_policy_id": EXPECTED_CANDIDATE_POLICY_ID,
        "source_raw_delta_diagnostic_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_ID,
        "source_v02_scale_probe_id": EXPECTED_V02_SCALE_PROBE_ID,
        "source_v03_probe_id": EXPECTED_V03_PROBE_ID,
        "scale_review_contract_summary": {
            "selected_encoding_id": SELECTED_ENCODING_ID,
            "selected_target_raw_delta_field": TARGET_RAW_DELTA_FIELD,
            "candidate_payload_fields": REQUIRED_CANDIDATE_PAYLOAD_FIELDS,
            "source_bounded_pass_evidence": scale_review_contract["source_bounded_pass_evidence"],
            "candidate_acceptance_forbidden": True,
            "full_registry_forbidden": True,
            "registry_sqlite_read_forbidden": True,
            "runtime_change_forbidden": True,
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
    parser.add_argument("--source-probe-id", default=EXPECTED_CANDIDATE_PROBE_ID)
    args = parser.parse_args()

    policy, receipt = build_policy(args.source_probe_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_id={policy['policy_id']}")
    print(f"policy_json_path=data/raw_delta_signature_candidate_scale_review_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/raw_delta_signature_candidate_scale_review_policy_receipts/{policy['policy_id']}.json")

    return 0 if policy["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
