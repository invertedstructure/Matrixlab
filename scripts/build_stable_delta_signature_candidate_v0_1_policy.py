#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

DIAG_DIR = ROOT / "data" / "stable_delta_signature_diagnostics"
DIAG_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_diagnostic_receipts"
PROBE_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_probe_receipts"

POLICY_DIR = ROOT / "data" / "stable_delta_signature_candidate_policies"
RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_policy_receipts"

EXPECTED_DIAGNOSTIC_ID = "21878f3c"
EXPECTED_SOURCE_PROBE_ID = "a729e00e"
EXPECTED_SOURCE_PROBE_RECEIPT_ID = "0ce90f3f"
CANDIDATE_DESIGN_ID = "STABLE_DELTA_SIGNATURE_CANDIDATE_V0_1"
NEXT_COMMAND_GOAL = "IMPLEMENT_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_1_PROBE"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha8(obj: Any) -> str:
    blob = json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:8]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def verify_diagnostic(diag: dict[str, Any], receipt: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if diag.get("diagnostic_id") != EXPECTED_DIAGNOSTIC_ID:
        failures.append(f"diagnostic_id_mismatch:{diag.get('diagnostic_id')}")
    if receipt.get("diagnostic_id") != EXPECTED_DIAGNOSTIC_ID:
        failures.append(f"diagnostic_receipt_id_mismatch:{receipt.get('diagnostic_id')}")
    if diag.get("gate") != "PASS":
        failures.append(f"diagnostic_gate_not_PASS:{diag.get('gate')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"diagnostic_receipt_gate_not_PASS:{receipt.get('gate')}")
    if diag.get("source_probe_id") != EXPECTED_SOURCE_PROBE_ID:
        failures.append(f"source_probe_id_mismatch:{diag.get('source_probe_id')}")
    if diag.get("source_receipt_id") != EXPECTED_SOURCE_PROBE_RECEIPT_ID:
        failures.append(f"source_probe_receipt_id_mismatch:{diag.get('source_receipt_id')}")
    if diag.get("source_probe_terminal_decision") != "FAIL":
        failures.append(f"source_probe_terminal_not_FAIL:{diag.get('source_probe_terminal_decision')}")
    if diag.get("failures") != []:
        failures.append(f"diagnostic_failures_not_empty:{diag.get('failures')}")

    scope = diag.get("diagnostic_scope") or {}
    if scope.get("read_only") is not True:
        failures.append("diagnostic_not_read_only")
    for key in [
        "runtime_receipt_system_changed",
        "probe_script_changed",
        "scale_mode_authorized",
        "receipt_replacement_authorized",
        "receipt_deletion_authorized",
        "receipt_compression_authorized",
        "theorem_content_authorized",
    ]:
        if scope.get(key) is not False:
            failures.append(f"diagnostic_scope_guard_failed:{key}:{scope.get(key)}")

    root = diag.get("root_cause") or {}
    if root.get("primary_failure") != "FALSE_MERGES_AND_NO_BURDEN_REDUCTION":
        failures.append(f"root_cause_unexpected:{root.get('primary_failure')}")

    false_merge = root.get("false_merge_diagnosis") or {}
    if false_merge.get("collision_count") != 19:
        failures.append(f"collision_count_unexpected:{false_merge.get('collision_count')}")
    if false_merge.get("false_merge_count") != 19:
        failures.append(f"false_merge_count_unexpected:{false_merge.get('false_merge_count')}")
    if false_merge.get("distinct_full_occurrence_keys") != 176:
        failures.append(f"distinct_full_keys_unexpected:{false_merge.get('distinct_full_occurrence_keys')}")
    if false_merge.get("distinct_compressed_signatures") != 21:
        failures.append(f"distinct_compressed_unexpected:{false_merge.get('distinct_compressed_signatures')}")
    if false_merge.get("distinguishability_retention_ratio", 1.0) >= 0.5:
        failures.append(f"retention_expected_low:{false_merge.get('distinguishability_retention_ratio')}")

    burden = root.get("burden_diagnosis") or {}
    if burden.get("full_receipt_bytes") != 298408:
        failures.append(f"full_receipt_bytes_unexpected:{burden.get('full_receipt_bytes')}")
    if burden.get("compressed_signature_bytes") != 409753:
        failures.append(f"compressed_signature_bytes_unexpected:{burden.get('compressed_signature_bytes')}")
    if burden.get("burden_ratio_bytes", 0.0) <= 1.0:
        failures.append(f"burden_ratio_expected_over_1:{burden.get('burden_ratio_bytes')}")

    contain = root.get("containment_diagnosis") or {}
    if contain.get("observer_only_valid") is not True:
        failures.append("observer_only_not_valid")
    if contain.get("audit_recoverability_valid") is not True:
        failures.append("audit_recoverability_not_valid")
    if contain.get("truth_surface_valid") is not True:
        failures.append("truth_surface_not_valid")

    byte = diag.get("byte_bloat_diagnostics") or {}
    if byte.get("current_compressed_row_bytes_recomputed") != 409753:
        failures.append(f"current_compressed_bytes_unexpected:{byte.get('current_compressed_row_bytes_recomputed')}")
    if byte.get("current_vs_full_ratio", 0.0) <= 1.0:
        failures.append(f"current_vs_full_ratio_expected_over_1:{byte.get('current_vs_full_ratio')}")
    if byte.get("minimal_required_vs_full_ratio", 1.0) >= 1.0:
        failures.append(f"minimal_required_ratio_expected_under_1:{byte.get('minimal_required_vs_full_ratio')}")
    if byte.get("projected_scale_vs_full_ratio", 1.0) >= 1.0:
        failures.append(f"projected_scale_ratio_expected_under_1:{byte.get('projected_scale_vs_full_ratio')}")
    if byte.get("estimated_debug_sidecar_bytes", 0) <= 0:
        failures.append("estimated_debug_sidecar_bytes_expected_positive")

    missing = {item.get("field"): item for item in diag.get("missing_core_fields") or []}
    for field in [
        "state_hash_before",
        "state_hash_after",
        "delta_payload.transition.state_hash_before",
        "delta_payload.transition.state_hash_after",
        "delta_payload.case_surface.probe_id",
        "delta_payload.case_surface.slot_id",
        "delta_payload.case_surface.burden_class",
    ]:
        item = missing.get(field)
        if not item:
            failures.append(f"missing_core_field_row_absent:{field}")
        elif item.get("missing_rate") != 1.0:
            failures.append(f"missing_core_field_expected_missing:{field}:{item.get('missing_rate')}")

    candidate = diag.get("candidate_v0_1_design_target") or {}
    if candidate.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"candidate_design_id_mismatch:{candidate.get('candidate_design_id')}")
    if candidate.get("design_status") != "PROPOSED_BY_FAILURE_DIAGNOSTIC_NOT_IMPLEMENTED":
        failures.append(f"candidate_design_status_wrong:{candidate.get('design_status')}")
    if candidate.get("next_command_goal") != "BUILD_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_1_POLICY":
        failures.append(f"diagnostic_candidate_next_goal_wrong:{candidate.get('next_command_goal')}")

    decision = diag.get("decision") or {}
    for key in [
        "do_not_scale_current_signature",
        "do_not_accept_probe_candidate",
        "do_not_authorize_scale_mode",
        "do_not_authorize_receipt_replacement",
        "diagnose_before_new_probe",
    ]:
        if decision.get(key) is not True:
            failures.append(f"diagnostic_decision_guard_missing:{key}:{decision.get(key)}")
    if decision.get("recommended_next_command_goal") != "BUILD_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_1_POLICY":
        failures.append(f"diagnostic_next_goal_wrong:{decision.get('recommended_next_command_goal')}")

    terminal = diag.get("terminal") or {}
    if terminal.get("next_command_goal") != "BUILD_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_1_POLICY":
        failures.append(f"diagnostic_terminal_next_goal_wrong:{terminal.get('next_command_goal')}")

    return failures


def verify_probe_receipt(probe: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if probe.get("probe_id") != EXPECTED_SOURCE_PROBE_ID:
        failures.append(f"probe_id_mismatch:{probe.get('probe_id')}")
    if probe.get("receipt_id") != EXPECTED_SOURCE_PROBE_RECEIPT_ID:
        failures.append(f"probe_receipt_id_mismatch:{probe.get('receipt_id')}")
    if probe.get("gate") != "STABLE_DELTA_SIGNATURE_PROBE_EXECUTION_PASS":
        failures.append(f"probe_execution_gate_not_PASS:{probe.get('gate')}")
    if probe.get("terminal_decision") != "FAIL":
        failures.append(f"probe_terminal_decision_not_FAIL:{probe.get('terminal_decision')}")
    if probe.get("truth_surface", {}).get("primary_comparison") != "full_occurrence_key_to_compressed_delta_signature":
        failures.append("probe_truth_surface_wrong")
    if probe.get("truth_surface", {}).get("raw_full_receipt_hash_used_as_truth_surface") is not False:
        failures.append("probe_raw_hash_truth_surface_used")
    if probe.get("truth_surface", {}).get("full_receipt_hash_compared_to_delta_signature") is not False:
        failures.append("probe_full_receipt_hash_compared")

    guards = probe.get("authority_guards") or {}
    if guards.get("observer_only") is not True:
        failures.append("probe_observer_only_guard_missing")
    for key in [
        "runtime_receipt_emission_changed",
        "full_receipts_suppressed",
        "scale_mode_authorized",
        "compressed_signature_promoted_to_theorem_content",
        "receipt_replacement_authorized",
        "receipt_deletion_authorized",
        "receipt_compression_authorized",
    ]:
        if guards.get(key) is not False:
            failures.append(f"probe_authority_guard_failed:{key}:{guards.get(key)}")

    pass_gates = probe.get("pass_gates") or {}
    if pass_gates.get("audit_recoverability") is not True:
        failures.append("probe_audit_recoverability_not_true")
    if pass_gates.get("observer_only_containment") is not True:
        failures.append("probe_observer_containment_not_true")
    if pass_gates.get("raw_receipt_hash_not_used_as_truth_surface") is not True:
        failures.append("probe_raw_hash_guard_not_true")
    if pass_gates.get("no_silent_collapse") is not False:
        failures.append("probe_no_silent_collapse_expected_false")
    if pass_gates.get("burden_reduction_real") is not False:
        failures.append("probe_burden_reduction_expected_false")

    return failures


def build_policy(diagnostic_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    POLICY_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    diag = load_json(DIAG_DIR / f"{diagnostic_id}.json")
    diag_receipt = load_json(DIAG_RECEIPT_DIR / f"{diagnostic_id}.json")
    probe = load_json(PROBE_RECEIPT_DIR / f"{EXPECTED_SOURCE_PROBE_ID}.json")

    failures: list[str] = []
    failures.extend(verify_diagnostic(diag, diag_receipt))
    failures.extend(verify_probe_receipt(probe))

    source_summary = diag.get("source_probe_summary") or {}
    byte = diag.get("byte_bloat_diagnostics") or {}
    missing = diag.get("missing_core_fields") or []

    policy = {
        "schema_version": "stable_delta_signature_candidate_v0_1_policy_v0",
        "policy_kind": "STABLE_DELTA_SIGNATURE_CANDIDATE_POLICY",
        "policy_name": "BUILD_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_1_POLICY",
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_diagnostic_id": EXPECTED_DIAGNOSTIC_ID,
        "source_probe_id": EXPECTED_SOURCE_PROBE_ID,
        "source_probe_receipt_id": EXPECTED_SOURCE_PROBE_RECEIPT_ID,
        "source_probe_terminal_decision": "FAIL",
        "mode": "OUTER_OBSERVER_ONLY",
        "authority": {
            "authorizes_next_candidate_probe_implementation": True,
            "authorized_next_command_goal": NEXT_COMMAND_GOAL,
            "authorizes_policy_only_now": True,
            "authorizes_runtime_receipt_emission_change": False,
            "authorizes_full_receipt_suppression": False,
            "authorizes_scale_mode": False,
            "authorizes_receipt_replacement": False,
            "authorizes_receipt_deletion": False,
            "authorizes_receipt_compression": False,
            "authorizes_raw_receipt_hash_truth_surface": False,
            "authorizes_theorem_content": False,
            "authorizes_scale_band_run_now": False,
            "authorizes_acceptance_now": False,
            "authorizes_current_v0_signature_scaling": False,
        },
        "objective": {
            "goal": "Build a second read-only candidate probe that separates tiny signature payload from audit/debug sidecar and retests local separability before any scale-band work.",
            "non_goals": [
                "Do not replace receipts.",
                "Do not suppress receipts.",
                "Do not alter runtime receipt generation.",
                "Do not authorize scale mode.",
                "Do not promote compressed signatures into theorem content.",
                "Do not scale the failed v0 signature.",
            ],
        },
        "source_failure_summary": {
            "primary_failure": "FALSE_MERGES_AND_NO_BURDEN_REDUCTION",
            "full_receipt_count": source_summary.get("full_receipt_count"),
            "compressed_signature_count": source_summary.get("compressed_signature_count"),
            "distinct_full_occurrence_keys": source_summary.get("distinct_full_occurrence_keys"),
            "distinct_compressed_signatures": source_summary.get("distinct_compressed_signatures"),
            "distinguishability_retention_ratio": source_summary.get("distinguishability_retention_ratio"),
            "collision_count": source_summary.get("collision_count"),
            "false_merge_count": source_summary.get("false_merge_count"),
            "full_receipt_bytes": source_summary.get("full_receipt_bytes"),
            "compressed_signature_bytes": source_summary.get("compressed_signature_bytes"),
            "burden_ratio_bytes": source_summary.get("burden_ratio_bytes"),
            "scale_value": source_summary.get("scale_value"),
        },
        "source_bloat_summary": {
            "full_receipt_bytes": byte.get("full_receipt_bytes"),
            "current_compressed_row_bytes": byte.get("current_compressed_row_bytes_recomputed"),
            "current_vs_full_ratio": byte.get("current_vs_full_ratio"),
            "estimated_debug_sidecar_bytes": byte.get("estimated_debug_sidecar_bytes"),
            "minimal_required_row_bytes": byte.get("minimal_required_row_bytes"),
            "minimal_required_vs_full_ratio": byte.get("minimal_required_vs_full_ratio"),
            "projected_scale_row_bytes": byte.get("projected_scale_row_bytes"),
            "projected_scale_vs_full_ratio": byte.get("projected_scale_vs_full_ratio"),
        },
        "source_quality_findings": {
            "missing_core_fields": missing,
            "interpretation": [
                "Current registry receipt surface lacks state_hash_before/state_hash_after for the latest receipt-write-pressure run.",
                "Current move_id is present but has only one distinct value, so it cannot separate 176 local occurrences alone.",
                "probe_id, slot_id, and burden_class are missing from compressed row extraction for this run.",
                "A valid v0.1 candidate must either extract richer canonical transition fields from audit payloads or honestly fail as SOURCE_SURFACE_INSUFFICIENT.",
            ],
        },
        "required_v0_1_design": {
            "signature_payload_must_be_tiny": True,
            "signature_payload_measured_separately_from_debug_sidecar": True,
            "audit_recoverability_mandatory": True,
            "canonical_occurrence_key_baseline_required": True,
            "raw_receipt_hash_truth_surface_forbidden": True,
            "local_collision_diagnosis_required_before_scale_bands": True,
            "scale_bands_forbidden_until_no_silent_collapse": True,
            "terminal_must_allow_source_insufficient": True,
            "allowed_terminal_decisions": [
                "PASS_OBSERVER_ONLY_LOCAL",
                "FAIL_FALSE_MERGE",
                "FAIL_NO_BURDEN_REDUCTION",
                "FAIL_SOURCE_SURFACE_INSUFFICIENT",
                "NEEDS_MORE_SCALE_AFTER_LOCAL_PASS",
            ],
        },
        "required_v0_1_payload_contract": {
            "signature_payload_allowed_fields": [
                "compression_version",
                "state_hash_before if canonical and present",
                "move_id if canonical and discriminative",
                "state_hash_after if canonical and present",
                "halt_reason/status if canonical and present",
                "case-local canonical discriminator only if audit-derived and not raw rowid packaging noise",
                "compact shape/event buckets only if they improve separability under projected burden budget",
            ],
            "signature_payload_forbidden_fields": [
                "full_occurrence_key",
                "raw_full_receipt_hash",
                "receipt_hash",
                "receipt rowid as primary identity",
                "audit_pointer",
                "observer_notes",
                "full debug delta_payload",
                "timestamps",
                "paths",
                "run packaging fields",
                "any field copied solely to force uniqueness without occurrence meaning",
            ],
            "row_surface_split_required": {
                "signature_payload": "tiny measured candidate signal",
                "audit_pointer": "recoverability sidecar, not counted as signature signal",
                "debug_payload": "observer diagnostic sidecar, not projected scale payload",
                "minimal_required_row": "required linkage row for probe accounting",
                "projected_scale_row": "what would be stored/reviewed if scale mode existed; still not authorized",
            },
        },
        "required_v0_1_gates": {
            "gate_1_no_raw_hash_truth_surface": {
                "pass_condition": "raw_full_receipt_hash_used_as_truth_surface is false",
                "fail_condition": "any comparison uses raw full receipt hash as primary truth surface",
            },
            "gate_2_observer_only_containment": {
                "pass_condition": "runtime receipt emission unchanged and full receipts unsuppressed",
                "fail_condition": "probe changes runtime receipts, suppresses full receipts, or authorizes scale mode",
            },
            "gate_3_audit_recoverability": {
                "pass_condition": "each compressed row links back to source run/case/occurrence/audit pointer",
                "fail_condition": "any compressed row cannot escalate back to audit source",
            },
            "gate_4_no_silent_collapse_local": {
                "pass_condition": "false_merge_count == 0 on local probe unless accepted merge classification exists",
                "fail_condition": "false_merge_count > 0 without accepted merge classification",
            },
            "gate_5_real_projected_burden_reduction": {
                "pass_condition": "projected_scale_row_bytes < full_receipt_bytes and signature_payload_bytes is separately reported",
                "fail_condition": "compressed row/debug payload is larger than full receipts or burden is moved into unmeasured sidecar",
            },
            "gate_6_source_surface_honesty": {
                "pass_condition": "missing canonical transition fields are explicitly reported",
                "fail_condition": "probe fills missing transition identity with raw rowid or packaging noise and calls it a pass",
            },
        },
        "implementation_constraints": {
            "must_touch_only_files": [
                "scripts/stable_delta_signature_candidate_v0_1_probe.py"
            ],
            "must_not_modify_files": [
                "src/",
                "app/",
                "matrixlab/",
                "scripts/stable_delta_signature_probe_v0.py",
                "scripts/wide_burden_profile_microruns.py",
            ],
            "must_read_existing_receipts_only": True,
            "must_emit_new_candidate_probe_receipt": True,
            "must_emit_candidate_rows_jsonl": True,
            "must_not_delete_existing_probe_outputs": True,
            "must_not_change_registry_sqlite": True,
        },
        "required_negative_controls": [
            {
                "case": "raw_hash_truth_surface_fail",
                "must_fail_if": "candidate uses raw receipt hash as primary truth surface",
            },
            {
                "case": "scale_mode_authority_fail",
                "must_fail_if": "candidate authorizes scale mode or receipt replacement",
            },
            {
                "case": "runtime_receipt_emission_change_fail",
                "must_fail_if": "candidate changes runtime receipt emission",
            },
            {
                "case": "debug_payload_counted_as_signature_fail",
                "must_fail_if": "debug/audit sidecar bytes are counted as signature payload bytes",
            },
            {
                "case": "rowid_identity_leak_fail",
                "must_fail_if": "candidate uses receipt rowid as primary signature discriminator",
            },
            {
                "case": "false_merge_local_fail",
                "must_fail_if": "false_merge_count > 0 without accepted merge classification",
            },
            {
                "case": "source_surface_missing_fail",
                "must_fail_if": "critical canonical transition fields are missing but candidate reports local pass",
            },
        ],
        "expected_next_receipt": {
            "schema_version": "stable_delta_signature_candidate_v0_1_probe_receipt_v0",
            "mode": "OUTER_OBSERVER_ONLY",
            "source_policy_id": "<this policy id>",
            "source_diagnostic_id": EXPECTED_DIAGNOSTIC_ID,
            "signature_payload_bytes": 0,
            "debug_sidecar_bytes": 0,
            "audit_sidecar_bytes": 0,
            "projected_scale_row_bytes": 0,
            "full_receipt_bytes": 0,
            "distinct_full_occurrence_keys": 0,
            "distinct_candidate_signatures": 0,
            "false_merge_count": 0,
            "burden_ratio_projected": 0.0,
            "terminal_decision": "PASS_OBSERVER_ONLY_LOCAL | FAIL_FALSE_MERGE | FAIL_NO_BURDEN_REDUCTION | FAIL_SOURCE_SURFACE_INSUFFICIENT | NEEDS_MORE_SCALE_AFTER_LOCAL_PASS",
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_1_POLICY_INVALID",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    policy_id = sha8({
        "policy_name": policy["policy_name"],
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_diagnostic_id": EXPECTED_DIAGNOSTIC_ID,
        "required_v0_1_design": policy["required_v0_1_design"],
        "required_v0_1_payload_contract": policy["required_v0_1_payload_contract"],
        "required_v0_1_gates": policy["required_v0_1_gates"],
        "implementation_constraints": policy["implementation_constraints"],
        "terminal": policy["terminal"],
    })
    policy["policy_id"] = policy_id
    policy["policy_sig8"] = policy_id

    receipt = {
        "schema_version": "stable_delta_signature_candidate_v0_1_policy_receipt_v0",
        "policy_id": policy_id,
        "policy_sig8": policy_id,
        "policy_path": f"data/stable_delta_signature_candidate_policies/{policy_id}.json",
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_diagnostic_id": EXPECTED_DIAGNOSTIC_ID,
        "source_probe_id": EXPECTED_SOURCE_PROBE_ID,
        "source_probe_receipt_id": EXPECTED_SOURCE_PROBE_RECEIPT_ID,
        "policy_status": policy["policy_status"],
        "mode": policy["mode"],
        "authorizes_next_candidate_probe_implementation": policy["authority"]["authorizes_next_candidate_probe_implementation"],
        "authorized_next_command_goal": policy["authority"]["authorized_next_command_goal"],
        "authorizes_runtime_receipt_emission_change": False,
        "authorizes_full_receipt_suppression": False,
        "authorizes_scale_mode": False,
        "authorizes_receipt_replacement": False,
        "authorizes_receipt_deletion": False,
        "authorizes_receipt_compression": False,
        "authorizes_raw_receipt_hash_truth_surface": False,
        "authorizes_scale_band_run_now": False,
        "source_primary_failure": policy["source_failure_summary"]["primary_failure"],
        "source_false_merge_count": policy["source_failure_summary"]["false_merge_count"],
        "source_burden_ratio_bytes": policy["source_failure_summary"]["burden_ratio_bytes"],
        "source_projected_scale_vs_full_ratio": policy["source_bloat_summary"]["projected_scale_vs_full_ratio"],
        "signature_payload_must_be_tiny": True,
        "signature_payload_measured_separately_from_debug_sidecar": True,
        "scale_bands_forbidden_until_no_silent_collapse": True,
        "terminal": policy["terminal"],
        "gate": policy["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id

    (POLICY_DIR / f"{policy_id}.json").write_text(json.dumps(policy, indent=2, sort_keys=True))
    (RECEIPT_DIR / f"{policy_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return policy, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--diagnostic-id", default=EXPECTED_DIAGNOSTIC_ID)
    args = parser.parse_args()

    policy, receipt = build_policy(args.diagnostic_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_id={policy['policy_id']}")
    print(f"policy_json_path=data/stable_delta_signature_candidate_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/stable_delta_signature_candidate_policy_receipts/{policy['policy_id']}.json")

    return 0 if policy["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
