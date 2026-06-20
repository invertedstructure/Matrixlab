#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CANONICAL_SURFACE_RECEIPT_DIR = ROOT / "data" / "canonical_transition_surface_probe_receipts"
CANONICAL_SURFACE_POLICY_DIR = ROOT / "data" / "canonical_transition_surface_probe_policies"
V01_CANDIDATE_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_1_receipts"
FALSE_MERGE_DIAG_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_1_false_merge_diagnostics"

OUT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_policy_receipts"

EXPECTED_SURFACE_PROBE_ID = "07be6e6b"
EXPECTED_SURFACE_RECEIPT_ID = "1c1e392f"
EXPECTED_SURFACE_POLICY_ID = "c7d3d021"
EXPECTED_V01_CANDIDATE_PROBE_ID = "a097b68f"
EXPECTED_V01_CANDIDATE_RECEIPT_ID = "08b4ac55"
EXPECTED_FALSE_MERGE_DIAGNOSTIC_ID = "79acf44a"

POLICY_NAME = "BUILD_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2_POLICY"
NEXT_COMMAND_GOAL = "IMPLEMENT_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2_PROBE"
CANDIDATE_DESIGN_ID = "STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2"


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
    surface: dict[str, Any],
    surface_policy: dict[str, Any],
    v01_candidate: dict[str, Any],
    false_merge_diag: dict[str, Any],
) -> list[str]:
    failures: list[str] = []

    if surface.get("probe_id") != EXPECTED_SURFACE_PROBE_ID:
        failures.append(f"surface_probe_id_mismatch:{surface.get('probe_id')}")
    if surface.get("receipt_id") != EXPECTED_SURFACE_RECEIPT_ID:
        failures.append(f"surface_receipt_id_mismatch:{surface.get('receipt_id')}")
    if surface.get("gate") != "PASS":
        failures.append(f"surface_gate_not_PASS:{surface.get('gate')}")
    if surface.get("mode") != "OUTER_OBSERVER_ONLY":
        failures.append(f"surface_mode_wrong:{surface.get('mode')}")
    if surface.get("probe_patch_version") != "alias_patch_state_sig8_before_after_v0":
        failures.append(f"surface_patch_version_wrong:{surface.get('probe_patch_version')}")
    if surface.get("source_policy_id") != EXPECTED_SURFACE_POLICY_ID:
        failures.append(f"surface_source_policy_wrong:{surface.get('source_policy_id')}")
    if surface.get("terminal_decision") != "PASS_CANONICAL_TRANSITION_SURFACE_OBSERVER_ONLY":
        failures.append(f"surface_terminal_not_PASS:{surface.get('terminal_decision')}")
    if surface.get("terminal", {}).get("next_command_goal") != POLICY_NAME:
        failures.append(f"surface_next_goal_wrong:{surface.get('terminal', {}).get('next_command_goal')}")

    auth = surface.get("authority_guards") or {}
    if auth.get("observer_only") is not True:
        failures.append("surface_observer_only_missing")
    for key in [
        "runtime_receipt_emission_changed",
        "registry_sqlite_changed",
        "scale_mode_authorized",
        "receipt_replacement_authorized",
        "receipt_deletion_authorized",
        "receipt_compression_authorized",
        "raw_receipt_hash_used_as_truth_surface",
        "scale_band_run_authorized",
        "stable_delta_candidate_acceptance_authorized",
    ]:
        if auth.get(key) is not False:
            failures.append(f"surface_illegal_authority:{key}:{auth.get(key)}")

    summary = surface.get("summary") or {}
    required_true = [
        "state_hash_before_present",
        "state_hash_after_present",
        "move_id_present",
        "transition_surface_sufficient",
        "within_case_discriminator_present",
    ]
    for key in required_true:
        if summary.get(key) is not True:
            failures.append(f"surface_summary_expected_true:{key}:{summary.get(key)}")

    required_false = [
        "case_only_surface",
    ]
    for key in required_false:
        if summary.get(key) is not False:
            failures.append(f"surface_summary_expected_false:{key}:{summary.get(key)}")

    if summary.get("source_surface_honesty_status") != "PASS_SURFACE_PRESENT":
        failures.append(f"surface_honesty_status_wrong:{summary.get('source_surface_honesty_status')}")

    transition_surface = surface.get("transition_surface") or {}
    if transition_surface.get("full_transition_tuple_present") is not True:
        failures.append("full_transition_tuple_present_expected_true")
    if transition_surface.get("full_transition_tuple_discriminative") is not True:
        failures.append("full_transition_tuple_discriminative_expected_true")
    if transition_surface.get("rowid_allowed_as_transition_identity") is not False:
        failures.append("rowid_allowed_as_transition_identity_not_false")
    if transition_surface.get("within_case_discriminator_packaging_noise") is not False:
        failures.append("within_case_discriminator_packaging_noise_not_false")

    gates = surface.get("pass_gates") or {}
    for key in [
        "authority_containment",
        "occurrence_anchoring",
        "transition_surface_completeness",
        "within_case_discriminator",
        "source_surface_honesty",
        "rowid_not_used_as_transition_identity",
        "raw_hash_not_used_as_truth_surface",
        "no_scale_bands",
        "no_compression_candidate_created",
    ]:
        if gates.get(key) is not True:
            failures.append(f"surface_gate_expected_true:{key}:{gates.get(key)}")

    field_stats = surface.get("field_stats") or {}
    before = field_stats.get("state_hash_before") or {}
    after = field_stats.get("state_hash_after") or {}
    move = field_stats.get("move_id") or {}
    cycle = field_stats.get("cycle") or {}

    if before.get("present_count") != 176:
        failures.append(f"state_hash_before_present_count_wrong:{before.get('present_count')}")
    if before.get("distinct_present_values") != 176:
        failures.append(f"state_hash_before_distinct_wrong:{before.get('distinct_present_values')}")
    if "state_sig8_before" not in (before.get("chosen_path_top10") or []):
        failures.append(f"state_hash_before_alias_not_confirmed:{before.get('chosen_path_top10')}")
    if before.get("usable_for_signature_payload") is not True:
        failures.append("state_hash_before_not_usable_for_signature_payload")

    if after.get("present_count") != 176:
        failures.append(f"state_hash_after_present_count_wrong:{after.get('present_count')}")
    if after.get("distinct_present_values", 0) < 170:
        failures.append(f"state_hash_after_distinct_too_low:{after.get('distinct_present_values')}")
    if "state_sig8_after" not in (after.get("chosen_path_top10") or []):
        failures.append(f"state_hash_after_alias_not_confirmed:{after.get('chosen_path_top10')}")
    if after.get("usable_for_signature_payload") is not True:
        failures.append("state_hash_after_not_usable_for_signature_payload")

    if move.get("present_count") != 176:
        failures.append(f"move_id_present_count_wrong:{move.get('present_count')}")
    if move.get("usable_for_signature_payload") is not True:
        failures.append("move_id_not_usable_for_signature_payload")
    if move.get("distinct_present_values") != 1:
        failures.append(f"move_id_expected_constant_current_surface:{move.get('distinct_present_values')}")

    if cycle.get("present_count") != 176:
        failures.append(f"cycle_present_count_wrong:{cycle.get('present_count')}")
    if cycle.get("distinct_present_values") != 20:
        failures.append(f"cycle_distinct_expected_20:{cycle.get('distinct_present_values')}")

    registry = surface.get("registry_surface") or {}
    if registry.get("registry_sqlite_changed") is not False:
        failures.append("surface_registry_changed")
    cols = registry.get("receipt_columns") or []
    for col in [
        "state_sig8_before",
        "state_sig8_after",
        "move_id",
        "cycle_n",
        "row_delta",
        "col_delta",
        "rank_delta",
        "support_delta",
    ]:
        if col not in cols:
            failures.append(f"expected_registry_column_missing:{col}")

    if surface_policy.get("policy_id") != EXPECTED_SURFACE_POLICY_ID:
        failures.append(f"surface_policy_id_wrong:{surface_policy.get('policy_id')}")
    if surface_policy.get("gate") != "PASS":
        failures.append(f"surface_policy_gate_not_PASS:{surface_policy.get('gate')}")

    if v01_candidate.get("candidate_probe_id") != EXPECTED_V01_CANDIDATE_PROBE_ID:
        failures.append(f"v01_candidate_probe_id_wrong:{v01_candidate.get('candidate_probe_id')}")
    if v01_candidate.get("receipt_id") != EXPECTED_V01_CANDIDATE_RECEIPT_ID:
        failures.append(f"v01_candidate_receipt_id_wrong:{v01_candidate.get('receipt_id')}")
    if v01_candidate.get("gate") != "PASS":
        failures.append(f"v01_candidate_gate_not_PASS:{v01_candidate.get('gate')}")
    if v01_candidate.get("terminal_decision") != "FAIL_FALSE_MERGE":
        failures.append(f"v01_candidate_terminal_wrong:{v01_candidate.get('terminal_decision')}")

    if false_merge_diag.get("diagnostic_id") != EXPECTED_FALSE_MERGE_DIAGNOSTIC_ID:
        failures.append(f"false_merge_diag_id_wrong:{false_merge_diag.get('diagnostic_id')}")
    if false_merge_diag.get("gate") != "PASS":
        failures.append(f"false_merge_diag_gate_not_PASS:{false_merge_diag.get('gate')}")
    if false_merge_diag.get("decision", {}).get("do_not_scale_current_candidate") is not True:
        failures.append("false_merge_diag_do_not_scale_missing")
    if false_merge_diag.get("root_cause", {}).get("primary_failure") != "LAWFUL_PAYLOAD_TOO_COARSE_FOR_WITHIN_CASE_OCCURRENCE_SEPARABILITY":
        failures.append("false_merge_diag_root_wrong")

    return failures


def build_policy(surface_probe_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    surface = load_json(CANONICAL_SURFACE_RECEIPT_DIR / f"{surface_probe_id}.json")
    surface_policy = load_json(CANONICAL_SURFACE_POLICY_DIR / f"{EXPECTED_SURFACE_POLICY_ID}.json")
    v01_candidate = load_json(V01_CANDIDATE_RECEIPT_DIR / f"{EXPECTED_V01_CANDIDATE_PROBE_ID}.json")
    false_merge_diag = load_json(FALSE_MERGE_DIAG_DIR / f"{EXPECTED_FALSE_MERGE_DIAGNOSTIC_ID}.json")

    failures = verify_sources(surface, surface_policy, v01_candidate, false_merge_diag)

    policy = {
        "schema_version": "stable_delta_signature_candidate_v0_2_policy_v0",
        "policy_name": POLICY_NAME,
        "policy_kind": "STABLE_DELTA_SIGNATURE_CANDIDATE_POLICY",
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "mode": "OUTER_OBSERVER_ONLY",
        "source_canonical_surface_probe_id": EXPECTED_SURFACE_PROBE_ID,
        "source_canonical_surface_receipt_id": EXPECTED_SURFACE_RECEIPT_ID,
        "source_canonical_surface_policy_id": EXPECTED_SURFACE_POLICY_ID,
        "source_v01_candidate_probe_id": EXPECTED_V01_CANDIDATE_PROBE_ID,
        "source_v01_candidate_receipt_id": EXPECTED_V01_CANDIDATE_RECEIPT_ID,
        "source_false_merge_diagnostic_id": EXPECTED_FALSE_MERGE_DIAGNOSTIC_ID,
        "doctrine_alignment": {
            "matrixlab_metric_doctrine_version": "matrixlab_metric_doctrine_v0.2_directional",
            "status": "NON_BINDING_DIRECTIONAL_BUT_OPERATIONALLY_ALIGNED",
            "core_rule": "A metric is useful only if its delta preserves distinguishability under compression at acceptable burden, without changing authority.",
            "corollary_applied": "The lawful transition surface exists after alias correction; build a v0.2 candidate using that surface instead of extending instrumentation.",
        },
        "source_result_summary": {
            "v01_result": {
                "candidate_probe_id": EXPECTED_V01_CANDIDATE_PROBE_ID,
                "terminal_decision": v01_candidate.get("terminal_decision"),
                "false_merge_count": v01_candidate.get("distinguishability_measurements", {}).get("false_merge_count"),
                "distinct_full_occurrence_keys": v01_candidate.get("distinguishability_measurements", {}).get("distinct_full_occurrence_keys"),
                "distinct_candidate_signatures": v01_candidate.get("distinguishability_measurements", {}).get("distinct_candidate_signatures"),
                "burden_ratio_projected": v01_candidate.get("burden_measurements", {}).get("burden_ratio_projected"),
                "burden_ratio_signature_payload": v01_candidate.get("burden_measurements", {}).get("burden_ratio_signature_payload"),
            },
            "corrected_surface_result": {
                "probe_id": EXPECTED_SURFACE_PROBE_ID,
                "receipt_id": EXPECTED_SURFACE_RECEIPT_ID,
                "terminal_decision": surface.get("terminal_decision"),
                "probe_patch_version": surface.get("probe_patch_version"),
                "state_hash_before_present": surface.get("summary", {}).get("state_hash_before_present"),
                "state_hash_after_present": surface.get("summary", {}).get("state_hash_after_present"),
                "move_id_present": surface.get("summary", {}).get("move_id_present"),
                "move_id_discriminative": surface.get("summary", {}).get("move_id_discriminative"),
                "transition_surface_sufficient": surface.get("summary", {}).get("transition_surface_sufficient"),
                "within_case_discriminator_present": surface.get("summary", {}).get("within_case_discriminator_present"),
                "case_only_surface": surface.get("summary", {}).get("case_only_surface"),
                "source_surface_honesty_status": surface.get("summary", {}).get("source_surface_honesty_status"),
            },
            "field_stats_subset": {
                "state_hash_before": surface.get("field_stats", {}).get("state_hash_before"),
                "move_id": surface.get("field_stats", {}).get("move_id"),
                "state_hash_after": surface.get("field_stats", {}).get("state_hash_after"),
                "cycle": surface.get("field_stats", {}).get("cycle"),
                "case_id": surface.get("field_stats", {}).get("case_id"),
            },
        },
        "authority": {
            "authorizes_next_candidate_probe_implementation": True,
            "authorized_next_command_goal": NEXT_COMMAND_GOAL,
            "authorizes_runtime_receipt_emission_change": False,
            "authorizes_full_receipt_suppression": False,
            "authorizes_receipt_replacement": False,
            "authorizes_receipt_deletion": False,
            "authorizes_receipt_compression": False,
            "authorizes_scale_mode": False,
            "authorizes_scale_band_run": False,
            "authorizes_theorem_content": False,
            "authorizes_taxonomy_evolution": False,
            "authorizes_architecture_redesign": False,
            "authorizes_stable_delta_candidate_acceptance": False,
            "authorizes_raw_receipt_hash_truth_surface": False,
            "authorizes_source_surface_extension": False,
        },
        "objective": {
            "goal": "Build a v0.2 observer-only stable delta signature candidate using the corrected lawful transition tuple.",
            "primary_question": "Does state_sig8_before + move_id + state_sig8_after preserve full occurrence separability with real projected burden reduction?",
            "allowed_truth_surface": "full_occurrence_key_to_candidate_delta_signature",
            "required_lawful_transition_tuple": {
                "state_hash_before": {
                    "source_column": "state_sig8_before",
                    "required_present_count": 176,
                    "required_discriminative": True,
                },
                "move_id": {
                    "source_column": "move_id",
                    "required_present_count": 176,
                    "may_be_constant": True,
                    "role": "transition context, not sufficient alone",
                },
                "state_hash_after": {
                    "source_column": "state_sig8_after",
                    "required_present_count": 176,
                    "required_discriminative": True,
                },
            },
            "non_goals": [
                "Do not run scale bands.",
                "Do not accept the candidate.",
                "Do not replace receipts.",
                "Do not compress or delete receipts.",
                "Do not modify runtime receipt emission.",
                "Do not extend the source surface.",
                "Do not use rowid, paths, timestamps, or raw receipt hashes as signature identity.",
            ],
        },
        "candidate_v0_2_signature_contract": {
            "signature_payload_required_fields": [
                "cv",
                "state_hash_before",
                "move_id",
                "state_hash_after",
            ],
            "signature_payload_optional_fields": [
                "halt_reason_if_present",
                "compact_delta_buckets_if_measured_from_existing_receipt_columns",
            ],
            "existing_delta_columns_allowed_for_compact_buckets": [
                "row_delta",
                "col_delta",
                "rank_delta",
                "support_delta",
                "distinct_column_types_before",
                "distinct_column_types_after",
                "new_column_types_added",
                "compression_ratio",
            ],
            "cycle_n_policy": {
                "may_measure_in_debug_or_surface_stats": True,
                "may_use_as_primary_signature_identity": False,
                "may_include_in_v0_2_signature_payload": False,
                "reason": "cycle_n is audit-derived and discriminative but risks uniqueness-by-position; v0.2 must first test lawful transition tuple.",
            },
            "case_id_policy": {
                "may_measure_in_debug_or_surface_stats": True,
                "may_use_as_primary_signature_identity": False,
                "may_include_in_v0_2_signature_payload": False,
                "reason": "case_id separates cases but does not by itself preserve within-case occurrence separability.",
            },
            "forbidden_signature_payload_fields": [
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
            "payload_measurement_required": True,
            "audit_sidecar_separate_required": True,
            "debug_sidecar_separate_required": True,
            "projected_scale_row_separate_required": True,
        },
        "required_candidate_probe_behavior": {
            "read_existing_surfaces_only": True,
            "load_corrected_canonical_surface_probe_receipt": True,
            "load_registry_receipts_read_only": True,
            "reconstruct_full_occurrence_key_without_raw_receipt_hash_truth_surface": True,
            "construct_candidate_signature_from_lawful_transition_tuple": True,
            "measure_signature_payload_bytes": True,
            "measure_projected_scale_row_bytes": True,
            "measure_audit_sidecar_bytes_separately": True,
            "measure_debug_sidecar_bytes_separately": True,
            "compute_distinguishability_retention_ratio": True,
            "compute_false_merge_count": True,
            "compute_burden_ratio_projected": True,
            "emit_candidate_rows_jsonl": True,
            "emit_candidate_probe_receipt": True,
            "must_not_write_to_registry_sqlite": True,
            "must_not_change_receipt_generation": True,
            "must_not_run_scale_bands": True,
            "must_not_create_source_surface_extension": True,
        },
        "pass_gates": {
            "authority_containment": "observer-only and all authority escalation guards false",
            "source_surface_regression": "state_sig8_before, move_id, state_sig8_after remain present and usable",
            "truth_surface": "compare full_occurrence_key to candidate_delta_signature, never raw receipt hash",
            "no_identity_leak": "signature payload excludes rowid, receipt hashes, audit pointer, full occurrence key, timestamps, paths",
            "no_false_merge": "false_merge_count == 0",
            "burden_reduction": "projected_scale_row_bytes < full_receipt_bytes",
            "debug_separation": "debug sidecar is measured separately and not counted as signature payload",
            "audit_recoverability": "every candidate row has an audit pointer to the source receipt row",
            "scale_precondition": "do not advance to scale bands unless local no_false_merge and burden_reduction pass",
        },
        "terminal_decisions": {
            "PASS_OBSERVER_ONLY_LOCAL": "Use when v0.2 has zero false merges, real projected burden reduction, audit recoverability, and observer containment.",
            "NEEDS_MORE_SCALE_AFTER_LOCAL_PASS": "Use only if local pass conditions hold and the next lawful step is scale-band policy.",
            "FAIL_SOURCE_SURFACE_REGRESSION": "Use if the corrected canonical transition surface is no longer present or usable.",
            "FAIL_FALSE_MERGE": "Use if distinct full occurrence keys collapse into one candidate signature.",
            "FAIL_NO_BURDEN_REDUCTION": "Use if projected scale row burden is not lower than full receipt burden.",
            "FAIL_IDENTITY_LEAK": "Use if signature payload uses rowid, raw receipt hash, full occurrence key, path, timestamp, or audit pointer as identity.",
            "FAIL_OBSERVER_INTERFERENCE": "Use if the probe changes runtime receipt emission, registry, receipts, or authority.",
        },
        "implementation_constraints": {
            "must_touch_only_files": [
                "scripts/stable_delta_signature_candidate_v0_2_probe.py"
            ],
            "must_not_modify_files": [
                "src/",
                "app/",
                "matrixlab/",
                "scripts/stable_delta_signature_candidate_v0_1_probe.py",
                "scripts/canonical_transition_surface_probe_v0.py",
                "scripts/diagnose_stable_delta_signature_candidate_v0_1_false_merges.py",
                "scripts/stable_delta_signature_probe_v0.py",
                "scripts/wide_burden_profile_microruns.py",
            ],
            "must_not_change_registry_sqlite": True,
            "must_not_delete_existing_outputs": True,
            "must_not_run_scale_bands": True,
            "must_not_accept_candidate": True,
            "must_not_extend_source_surface": True,
        },
        "required_negative_controls": [
            {
                "case": "source_surface_regression_fail",
                "must_fail_if": "state_sig8_before/state_sig8_after are not found or usable",
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
                "case": "full_occurrence_key_identity_leak_fail",
                "must_fail_if": "full_occurrence_key enters signature payload",
            },
            {
                "case": "case_only_false_pass_fail",
                "must_fail_if": "candidate passes with only case_id as signature identity",
            },
            {
                "case": "cycle_only_false_pass_fail",
                "must_fail_if": "candidate passes with only cycle_n as signature identity",
            },
            {
                "case": "debug_payload_counted_as_signature_fail",
                "must_fail_if": "debug sidecar bytes are counted as signature payload bytes",
            },
            {
                "case": "scale_mode_authority_fail",
                "must_fail_if": "probe authorizes scale mode or scale bands",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2_POLICY_INVALID",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    policy_id = sha8({
        "policy_name": policy["policy_name"],
        "candidate_design_id": policy["candidate_design_id"],
        "source_canonical_surface_probe_id": policy["source_canonical_surface_probe_id"],
        "source_v01_candidate_probe_id": policy["source_v01_candidate_probe_id"],
        "authority": policy["authority"],
        "objective": policy["objective"],
        "candidate_v0_2_signature_contract": policy["candidate_v0_2_signature_contract"],
        "required_candidate_probe_behavior": policy["required_candidate_probe_behavior"],
        "implementation_constraints": policy["implementation_constraints"],
    })
    policy["policy_id"] = policy_id
    policy["policy_sig8"] = policy_id

    receipt = {
        "schema_version": "stable_delta_signature_candidate_v0_2_policy_receipt_v0",
        "policy_id": policy_id,
        "policy_sig8": policy_id,
        "policy_path": f"data/stable_delta_signature_candidate_v0_2_policies/{policy_id}.json",
        "policy_name": POLICY_NAME,
        "policy_status": policy["policy_status"],
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_canonical_surface_probe_id": EXPECTED_SURFACE_PROBE_ID,
        "source_canonical_surface_receipt_id": EXPECTED_SURFACE_RECEIPT_ID,
        "source_canonical_surface_policy_id": EXPECTED_SURFACE_POLICY_ID,
        "source_v01_candidate_probe_id": EXPECTED_V01_CANDIDATE_PROBE_ID,
        "source_v01_candidate_receipt_id": EXPECTED_V01_CANDIDATE_RECEIPT_ID,
        "source_false_merge_diagnostic_id": EXPECTED_FALSE_MERGE_DIAGNOSTIC_ID,
        "authorizes_next_candidate_probe_implementation": True,
        "authorized_next_command_goal": NEXT_COMMAND_GOAL,
        "authorizes_runtime_receipt_emission_change": False,
        "authorizes_full_receipt_suppression": False,
        "authorizes_receipt_replacement": False,
        "authorizes_receipt_deletion": False,
        "authorizes_receipt_compression": False,
        "authorizes_scale_mode": False,
        "authorizes_scale_band_run": False,
        "authorizes_theorem_content": False,
        "authorizes_taxonomy_evolution": False,
        "authorizes_architecture_redesign": False,
        "authorizes_stable_delta_candidate_acceptance": False,
        "authorizes_raw_receipt_hash_truth_surface": False,
        "authorizes_source_surface_extension": False,
        "required_lawful_transition_tuple": policy["objective"]["required_lawful_transition_tuple"],
        "signature_payload_required_fields": policy["candidate_v0_2_signature_contract"]["signature_payload_required_fields"],
        "signature_payload_forbidden_fields": policy["candidate_v0_2_signature_contract"]["forbidden_signature_payload_fields"],
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
    parser.add_argument("--surface-probe-id", default=EXPECTED_SURFACE_PROBE_ID)
    args = parser.parse_args()

    policy, receipt = build_policy(args.surface_probe_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_id={policy['policy_id']}")
    print(f"policy_json_path=data/stable_delta_signature_candidate_v0_2_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/stable_delta_signature_candidate_v0_2_policy_receipts/{policy['policy_id']}.json")

    return 0 if policy["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
