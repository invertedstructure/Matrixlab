#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

FM_DIAG_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_1_false_merge_diagnostics"
FM_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_1_false_merge_diagnostic_receipts"
CANDIDATE_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_1_receipts"
CANDIDATE_POLICY_DIR = ROOT / "data" / "stable_delta_signature_candidate_policies"
SOURCE_DIAG_DIR = ROOT / "data" / "stable_delta_signature_diagnostics"

OUT_DIR = ROOT / "data" / "canonical_transition_surface_probe_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "canonical_transition_surface_probe_policy_receipts"

EXPECTED_FM_DIAG_ID = "79acf44a"
EXPECTED_FM_RECEIPT_ID = "71557a8e"
EXPECTED_CANDIDATE_PROBE_ID = "a097b68f"
EXPECTED_CANDIDATE_RECEIPT_ID = "08b4ac55"
EXPECTED_CANDIDATE_POLICY_ID = "c3dcd5d1"
EXPECTED_SOURCE_DIAGNOSTIC_ID = "21878f3c"

POLICY_NAME = "BUILD_CANONICAL_TRANSITION_SURFACE_PROBE_POLICY_V0"
NEXT_COMMAND_GOAL = "IMPLEMENT_CANONICAL_TRANSITION_SURFACE_PROBE_V0"


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


def verify_sources(fm_diag: dict[str, Any], fm_receipt: dict[str, Any], candidate: dict[str, Any], candidate_policy: dict[str, Any], source_diag: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if fm_diag.get("diagnostic_id") != EXPECTED_FM_DIAG_ID:
        failures.append(f"fm_diag_id_mismatch:{fm_diag.get('diagnostic_id')}")
    if fm_receipt.get("receipt_id") != EXPECTED_FM_RECEIPT_ID:
        failures.append(f"fm_receipt_id_mismatch:{fm_receipt.get('receipt_id')}")
    if fm_diag.get("gate") != "PASS":
        failures.append(f"fm_diag_gate_not_PASS:{fm_diag.get('gate')}")
    if fm_receipt.get("gate") != "PASS":
        failures.append(f"fm_receipt_gate_not_PASS:{fm_receipt.get('gate')}")
    if fm_diag.get("source_candidate_probe_id") != EXPECTED_CANDIDATE_PROBE_ID:
        failures.append(f"source_candidate_probe_id_wrong:{fm_diag.get('source_candidate_probe_id')}")
    if fm_diag.get("source_candidate_receipt_id") != EXPECTED_CANDIDATE_RECEIPT_ID:
        failures.append(f"source_candidate_receipt_id_wrong:{fm_diag.get('source_candidate_receipt_id')}")
    if fm_diag.get("source_policy_id") != EXPECTED_CANDIDATE_POLICY_ID:
        failures.append(f"source_policy_id_wrong:{fm_diag.get('source_policy_id')}")
    if fm_diag.get("source_diagnostic_id") != EXPECTED_SOURCE_DIAGNOSTIC_ID:
        failures.append(f"source_diagnostic_id_wrong:{fm_diag.get('source_diagnostic_id')}")
    if fm_diag.get("failures") != []:
        failures.append(f"fm_diag_failures_not_empty:{fm_diag.get('failures')}")

    root = fm_diag.get("root_cause") or {}
    if root.get("primary_failure") != "LAWFUL_PAYLOAD_TOO_COARSE_FOR_WITHIN_CASE_OCCURRENCE_SEPARABILITY":
        failures.append(f"root_primary_failure_wrong:{root.get('primary_failure')}")
    if root.get("burden_status") != "BURDEN_SIDE_PROGRESS_CONFIRMED":
        failures.append(f"burden_status_wrong:{root.get('burden_status')}")
    if root.get("distinguishability_status") != "FAILED_LOCAL_NO_SILENT_COLLAPSE":
        failures.append(f"distinguishability_status_wrong:{root.get('distinguishability_status')}")

    decision = fm_diag.get("decision") or {}
    expected_true = [
        "do_not_scale_current_candidate",
        "do_not_accept_current_candidate",
        "do_not_authorize_scale_mode",
        "do_not_authorize_receipt_replacement",
        "burden_side_progress_confirmed",
        "distinguishability_blocker_confirmed",
        "transition_surface_missing",
        "case_only_discriminator",
        "audit_locator_distinguishability_detected",
    ]
    for key in expected_true:
        if decision.get(key) is not True:
            failures.append(f"fm_decision_expected_true:{key}:{decision.get(key)}")
    if decision.get("recommended_next_command_goal") != POLICY_NAME:
        failures.append(f"fm_recommended_next_goal_wrong:{decision.get('recommended_next_command_goal')}")

    terminal = fm_diag.get("terminal") or {}
    if terminal.get("next_command_goal") != POLICY_NAME:
        failures.append(f"fm_terminal_next_goal_wrong:{terminal.get('next_command_goal')}")

    field_cause = fm_diag.get("field_cause_analysis") or {}
    if field_cause.get("transition_sufficient") is not False:
        failures.append("transition_sufficient_expected_false")
    if field_cause.get("canonical_discriminator_sufficient") is not True:
        failures.append("canonical_discriminator_expected_true")
    if field_cause.get("weak_metric_discriminator_available") is not False:
        failures.append("weak_metric_discriminator_expected_false")

    missing = field_cause.get("missing_or_non_discriminative_fields") or {}
    for field in ["state_hash_before", "state_hash_after", "move_id"]:
        if field not in missing:
            failures.append(f"expected_missing_or_non_discriminative_field:{field}")

    cand_summary = fm_diag.get("source_candidate_summary") or {}
    if cand_summary.get("terminal_decision") != "FAIL_FALSE_MERGE":
        failures.append(f"candidate_terminal_wrong:{cand_summary.get('terminal_decision')}")
    if cand_summary.get("false_merge_count") != 10:
        failures.append(f"candidate_false_merge_count_wrong:{cand_summary.get('false_merge_count')}")
    if cand_summary.get("burden_ratio_projected", 1.0) >= 1.0:
        failures.append(f"candidate_projected_burden_not_reduced:{cand_summary.get('burden_ratio_projected')}")
    if cand_summary.get("burden_ratio_signature_payload", 1.0) >= cand_summary.get("burden_ratio_projected", 0.0):
        failures.append("signature_payload_ratio_not_less_than_projected_ratio")

    if candidate.get("candidate_probe_id") != EXPECTED_CANDIDATE_PROBE_ID:
        failures.append(f"candidate_probe_id_wrong:{candidate.get('candidate_probe_id')}")
    if candidate.get("receipt_id") != EXPECTED_CANDIDATE_RECEIPT_ID:
        failures.append(f"candidate_receipt_id_wrong:{candidate.get('receipt_id')}")
    if candidate.get("gate") != "PASS":
        failures.append(f"candidate_gate_not_PASS:{candidate.get('gate')}")
    if candidate.get("terminal_decision") != "FAIL_FALSE_MERGE":
        failures.append(f"candidate_terminal_not_FAIL_FALSE_MERGE:{candidate.get('terminal_decision')}")

    auth = candidate.get("authority_guards") or {}
    if auth.get("observer_only") is not True:
        failures.append("candidate_observer_only_missing")
    for key in [
        "runtime_receipt_emission_changed",
        "full_receipts_suppressed",
        "scale_mode_authorized",
        "receipt_replacement_authorized",
        "receipt_deletion_authorized",
        "receipt_compression_authorized",
        "raw_receipt_hash_truth_surface_authorized",
        "theorem_content_authorized",
        "scale_band_run_authorized",
    ]:
        if auth.get(key) is not False:
            failures.append(f"candidate_illegal_authority:{key}:{auth.get(key)}")

    if candidate_policy.get("policy_id") != EXPECTED_CANDIDATE_POLICY_ID:
        failures.append(f"candidate_policy_id_wrong:{candidate_policy.get('policy_id')}")
    if candidate_policy.get("gate") != "PASS":
        failures.append(f"candidate_policy_gate_not_PASS:{candidate_policy.get('gate')}")
    if candidate_policy.get("authority", {}).get("authorizes_scale_band_run_now") is not False:
        failures.append("candidate_policy_authorizes_scale_bands_unexpectedly")

    if source_diag.get("diagnostic_id") != EXPECTED_SOURCE_DIAGNOSTIC_ID:
        failures.append(f"source_diag_id_wrong:{source_diag.get('diagnostic_id')}")
    if source_diag.get("gate") != "PASS":
        failures.append(f"source_diag_gate_not_PASS:{source_diag.get('gate')}")

    return failures


def build_policy(fm_diag_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    fm_diag = load_json(FM_DIAG_DIR / f"{fm_diag_id}.json")
    fm_receipt = load_json(FM_RECEIPT_DIR / f"{fm_diag_id}.json")
    candidate = load_json(CANDIDATE_RECEIPT_DIR / f"{EXPECTED_CANDIDATE_PROBE_ID}.json")
    candidate_policy = load_json(CANDIDATE_POLICY_DIR / f"{EXPECTED_CANDIDATE_POLICY_ID}.json")
    source_diag = load_json(SOURCE_DIAG_DIR / f"{EXPECTED_SOURCE_DIAGNOSTIC_ID}.json")

    failures = verify_sources(fm_diag, fm_receipt, candidate, candidate_policy, source_diag)

    policy = {
        "schema_version": "canonical_transition_surface_probe_policy_v0",
        "policy_name": POLICY_NAME,
        "policy_kind": "CANONICAL_TRANSITION_SURFACE_PROBE_POLICY",
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "mode": "OUTER_OBSERVER_ONLY",
        "source_false_merge_diagnostic_id": EXPECTED_FM_DIAG_ID,
        "source_false_merge_diagnostic_receipt_id": EXPECTED_FM_RECEIPT_ID,
        "source_candidate_probe_id": EXPECTED_CANDIDATE_PROBE_ID,
        "source_candidate_receipt_id": EXPECTED_CANDIDATE_RECEIPT_ID,
        "source_candidate_policy_id": EXPECTED_CANDIDATE_POLICY_ID,
        "source_stable_delta_diagnostic_id": EXPECTED_SOURCE_DIAGNOSTIC_ID,
        "doctrine_alignment": {
            "matrixlab_metric_doctrine_version": "matrixlab_metric_doctrine_v0.2_directional",
            "status": "NON_BINDING_DIRECTIONAL_BUT_OPERATIONALLY_ALIGNED",
            "core_rule": "If the lawful transition surface is missing, do not fake uniqueness; stop and classify the source surface.",
        },
        "source_result_summary": {
            "burden_side_progress_confirmed": True,
            "distinguishability_blocker_confirmed": True,
            "false_merge_count": fm_diag.get("source_candidate_summary", {}).get("false_merge_count"),
            "collision_group_count": fm_diag.get("collision_summary", {}).get("collision_group_count"),
            "burden_ratio_projected": fm_diag.get("source_candidate_summary", {}).get("burden_ratio_projected"),
            "burden_ratio_signature_payload": fm_diag.get("source_candidate_summary", {}).get("burden_ratio_signature_payload"),
            "root_cause": fm_diag.get("root_cause"),
            "field_cause_analysis": fm_diag.get("field_cause_analysis"),
        },
        "authority": {
            "authorizes_next_probe_implementation": True,
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
        },
        "objective": {
            "goal": "Determine whether the existing audit/registry surface exposes lawful transition identity sufficient to support future stable delta signatures.",
            "questions": [
                "Are state_hash_before and state_hash_after present anywhere in the existing audit surface?",
                "Is move_id canonical and discriminative, or merely constant context?",
                "Is there a lawful within-case occurrence discriminator that is audit-derived and not packaging noise?",
                "Can a transition_id be reconstructed from audit-derived fields without using raw rowid as primary signature identity?",
                "Is the source surface sufficient for local no-silent-collapse testing?",
            ],
            "non_goals": [
                "Do not build a new compression candidate.",
                "Do not run scale bands.",
                "Do not modify runtime receipt emission.",
                "Do not add new instrumentation to the runner.",
                "Do not declare scale mode.",
                "Do not accept the failed v0.1 candidate.",
            ],
        },
        "required_probe_behavior": {
            "read_existing_surfaces_only": True,
            "inspect_registry_receipts": True,
            "inspect_receipt_payload_json_if_present": True,
            "inspect_existing_audit_pointer_targets_if_resolvable_without_mutation": True,
            "classify_each_candidate_field": True,
            "emit_surface_rows_jsonl": True,
            "emit_probe_receipt": True,
            "must_not_write_to_registry_sqlite": True,
            "must_not_change_receipt_generation": True,
            "must_not_use_raw_receipt_hash_as_truth_surface": True,
            "must_not_use_rowid_as_signature_identity": True,
        },
        "field_classification_contract": {
            "candidate_fields": [
                "run_id",
                "case_id",
                "occurrence_id",
                "transition_id",
                "state_hash_before",
                "move_id",
                "state_hash_after",
                "halt_reason",
                "terminal_status",
                "family",
                "radius",
                "depth",
                "cycle",
                "probe_id",
                "slot_id",
                "burden_class",
                "raw_event_count",
                "shape_count",
                "receipt_count",
            ],
            "required_stats_per_field": [
                "present_count",
                "missing_count",
                "missing_rate",
                "distinct_present_values",
                "is_constant",
                "is_discriminative",
                "is_audit_derived",
                "is_packaging_noise",
                "usable_for_transition_surface",
                "usable_for_signature_payload",
            ],
            "packaging_noise_examples": [
                "receipt rowid used as primary transition identity",
                "timestamps",
                "paths",
                "raw receipt hashes",
                "run packaging fields that do not describe transition occurrence",
            ],
        },
        "surface_pass_requirements": {
            "authority_containment": {
                "required": True,
                "pass_condition": "observer_only true and all authority escalation guards false",
            },
            "occurrence_anchoring": {
                "required": True,
                "pass_condition": "full_occurrence_key and audit_pointer are recoverable",
            },
            "transition_surface_completeness": {
                "required": True,
                "pass_condition": "state_hash_before, move_id, state_hash_after are present and/or a lawful audit-derived transition discriminator exists",
            },
            "within_case_discriminator": {
                "required": True,
                "pass_condition": "within-case occurrence identity is audit-derived and not raw packaging noise",
            },
            "source_surface_honesty": {
                "required": True,
                "pass_condition": "missing, constant, coarse, and packaging-noise fields are explicitly classified",
            },
        },
        "terminal_decisions": {
            "PASS_CANONICAL_TRANSITION_SURFACE_OBSERVER_ONLY": "Use when lawful transition identity is present, discriminative, audit-derived, and observer-only.",
            "FAIL_TRANSITION_SURFACE_MISSING": "Use when state before/after or lawful transition discriminator is absent.",
            "FAIL_WITHIN_CASE_OCCURRENCE_SURFACE_MISSING": "Use when case-level identity exists but within-case occurrence identity is absent or packaging-noise only.",
            "FAIL_PACKAGING_NOISE_ONLY": "Use when apparent uniqueness comes only from rowid, timestamps, paths, raw hashes, or packaging fields.",
            "FAIL_OBSERVER_INTERFERENCE": "Use when the probe changes runtime, receipts, registry, or authority.",
            "NEEDS_SOURCE_SURFACE_EXTENSION_POLICY": "Use when the existing surface is insufficient and a separate policy would be required to add lawful instrumentation later.",
        },
        "next_probe_required_receipt_fields": {
            "schema_version": "canonical_transition_surface_probe_receipt_v0",
            "source_policy_id": "<this policy id>",
            "mode": "OUTER_OBSERVER_ONLY",
            "field_stats": {},
            "transition_surface": {
                "state_hash_before_present": False,
                "move_id_present": False,
                "move_id_discriminative": False,
                "state_hash_after_present": False,
                "within_case_discriminator_present": False,
                "within_case_discriminator_packaging_noise": False,
                "transition_surface_sufficient": False,
            },
            "authority_guards": {
                "observer_only": True,
                "runtime_receipt_emission_changed": False,
                "registry_sqlite_changed": False,
                "scale_mode_authorized": False,
                "receipt_replacement_authorized": False,
                "receipt_compression_authorized": False,
                "raw_receipt_hash_used_as_truth_surface": False,
            },
            "terminal_decision": "PASS_CANONICAL_TRANSITION_SURFACE_OBSERVER_ONLY | FAIL_TRANSITION_SURFACE_MISSING | FAIL_WITHIN_CASE_OCCURRENCE_SURFACE_MISSING | FAIL_PACKAGING_NOISE_ONLY | FAIL_OBSERVER_INTERFERENCE | NEEDS_SOURCE_SURFACE_EXTENSION_POLICY",
            "next_command_goal": "...",
        },
        "implementation_constraints": {
            "must_touch_only_files": [
                "scripts/canonical_transition_surface_probe_v0.py"
            ],
            "must_not_modify_files": [
                "src/",
                "app/",
                "matrixlab/",
                "scripts/stable_delta_signature_candidate_v0_1_probe.py",
                "scripts/stable_delta_signature_probe_v0.py",
                "scripts/wide_burden_profile_microruns.py",
            ],
            "must_not_change_registry_sqlite": True,
            "must_not_delete_existing_outputs": True,
            "must_not_create_compression_candidate": True,
            "must_not_run_scale_bands": True,
        },
        "required_negative_controls": [
            {
                "case": "runtime_receipt_emission_change_fail",
                "must_fail_if": "probe changes runtime receipt emission",
            },
            {
                "case": "registry_mutation_fail",
                "must_fail_if": "probe writes to registry.sqlite",
            },
            {
                "case": "rowid_identity_as_transition_fail",
                "must_fail_if": "probe treats receipt rowid as primary transition identity",
            },
            {
                "case": "raw_hash_truth_surface_fail",
                "must_fail_if": "probe uses raw receipt hash as primary truth surface",
            },
            {
                "case": "case_only_false_pass_fail",
                "must_fail_if": "probe reports pass using only case_id as occurrence discriminator",
            },
            {
                "case": "scale_mode_authority_fail",
                "must_fail_if": "probe authorizes scale mode or scale bands",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_CANONICAL_TRANSITION_SURFACE_PROBE_POLICY_INVALID",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    policy_id = sha8({
        "policy_name": policy["policy_name"],
        "source_false_merge_diagnostic_id": policy["source_false_merge_diagnostic_id"],
        "authority": policy["authority"],
        "objective": policy["objective"],
        "field_classification_contract": policy["field_classification_contract"],
        "surface_pass_requirements": policy["surface_pass_requirements"],
        "terminal_decisions": policy["terminal_decisions"],
        "implementation_constraints": policy["implementation_constraints"],
    })
    policy["policy_id"] = policy_id
    policy["policy_sig8"] = policy_id

    receipt = {
        "schema_version": "canonical_transition_surface_probe_policy_receipt_v0",
        "policy_id": policy_id,
        "policy_sig8": policy_id,
        "policy_path": f"data/canonical_transition_surface_probe_policies/{policy_id}.json",
        "policy_name": POLICY_NAME,
        "policy_status": policy["policy_status"],
        "source_false_merge_diagnostic_id": EXPECTED_FM_DIAG_ID,
        "source_false_merge_diagnostic_receipt_id": EXPECTED_FM_RECEIPT_ID,
        "source_candidate_probe_id": EXPECTED_CANDIDATE_PROBE_ID,
        "source_candidate_receipt_id": EXPECTED_CANDIDATE_RECEIPT_ID,
        "source_candidate_policy_id": EXPECTED_CANDIDATE_POLICY_ID,
        "source_stable_delta_diagnostic_id": EXPECTED_SOURCE_DIAGNOSTIC_ID,
        "authorizes_next_probe_implementation": True,
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
        "source_primary_failure": "LAWFUL_PAYLOAD_TOO_COARSE_FOR_WITHIN_CASE_OCCURRENCE_SEPARABILITY",
        "source_burden_status": "BURDEN_SIDE_PROGRESS_CONFIRMED",
        "source_distinguishability_status": "FAILED_LOCAL_NO_SILENT_COLLAPSE",
        "required_probe_behavior": policy["required_probe_behavior"],
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
    parser.add_argument("--false-merge-diagnostic-id", default=EXPECTED_FM_DIAG_ID)
    args = parser.parse_args()

    policy, receipt = build_policy(args.false_merge_diagnostic_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_id={policy['policy_id']}")
    print(f"policy_json_path=data/canonical_transition_surface_probe_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/canonical_transition_surface_probe_policy_receipts/{policy['policy_id']}.json")

    return 0 if policy["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
