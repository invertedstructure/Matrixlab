#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

POLICY_DIR = ROOT / "data" / "receipt_volume_fix_candidate_policies"
NEXT_DECISION_DIR = ROOT / "data" / "post_frontier_depth_revert_next_burden_decisions"
PROFILE_DIR = ROOT / "data" / "micro_burden_profiles"

CANDIDATE_DIR = ROOT / "data" / "receipt_volume_fix_candidates"
RECEIPT_DIR = ROOT / "data" / "receipt_volume_fix_candidate_receipts"

EXPECTED_POLICY_ID = "2e6aa9d6"
EXPECTED_NEXT_DECISION_ID = "25bf9c59"
EXPECTED_AFTER_REVERT_PROFILE_ID = "b6609f93"

TARGET_BURDEN_CLASS = "BURDEN_RECEIPT_VOLUME"
EXPECTED_PROBE = "MICRO_05_RECEIPT_WRITE_PRESSURE"
EXPECTED_SLOT = "MICRO_05_RECEIPT_WRITE_PRESSURE_E"
EXPECTED_FAMILY = "E"

AUTHORIZED_FIX_CANDIDATE_ID = "FIX_CANDIDATE_RECEIPT_VOLUME_WRITE_PRESSURE_PLAN_V0"
AUTHORIZED_FIX_CANDIDATE_KIND = "RECEIPT_VOLUME_FIX_CANDIDATE"

ACCEPTED_FROZEN = [
    "BURDEN_CYCLE_SCAN",
    "BURDEN_DB_WRITE",
    "BURDEN_REPEATED_SLOT_WORK",
]

REJECTED_OR_DEFERRED = [
    "BURDEN_DEPTH_SCAN",
]

EXPECTED_ALL_NON_UNKNOWN = [
    "BURDEN_CYCLE_SCAN",
    "BURDEN_DB_WRITE",
    "BURDEN_DEPTH_SCAN",
    "BURDEN_RECEIPT_VOLUME",
    "BURDEN_REPEATED_SLOT_WORK",
]

NEXT_COMMAND_GOAL = "APPLY_RECEIPT_VOLUME_FIX_CANDIDATE_V0"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_sig(obj: dict[str, Any]) -> str:
    body = dict(obj)
    for key in ("candidate_id", "candidate_sig8", "receipt_id", "receipt_sig8"):
        body.pop(key, None)
    blob = json.dumps(body, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:8]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def summarize_target(profile: dict[str, Any]) -> dict[str, Any]:
    rows = [
        row for row in (profile.get("rows") or [])
        if row.get("burden_class") == TARGET_BURDEN_CLASS
    ]
    receipts = sum(int(row.get("receipts") or 0) for row in rows)
    elapsed_ms = sum(int(row.get("elapsed_ms") or 0) for row in rows)

    return {
        "burden_class": TARGET_BURDEN_CLASS,
        "rows": len(rows),
        "receipts": receipts,
        "elapsed_ms": elapsed_ms,
        "receipts_per_sec": round(receipts / (elapsed_ms / 1000.0), 6) if elapsed_ms > 0 else None,
        "families": sorted({row.get("family_compact") for row in rows if row.get("family_compact")}),
        "probes": sorted({row.get("probe_id") for row in rows if row.get("probe_id")}),
        "slots": [row.get("slot_id") for row in rows if row.get("slot_id")],
        "row_keys": [
            {
                "probe_id": row.get("probe_id"),
                "slot_id": row.get("slot_id"),
                "family_compact": row.get("family_compact"),
                "burden_class": row.get("burden_class"),
            }
            for row in rows
        ],
    }


def verify_policy(policy: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if policy.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"policy_id_mismatch:{policy.get('policy_id')}")
    if policy.get("policy_id") != policy.get("policy_sig8"):
        failures.append("policy_sig_mismatch")
    if policy.get("gate") != "PASS":
        failures.append("policy_gate_not_PASS")
    if policy.get("failures") != []:
        failures.append(f"policy_failures_not_empty:{policy.get('failures')}")
    if policy.get("source_next_burden_decision_id") != EXPECTED_NEXT_DECISION_ID:
        failures.append(f"policy_decision_mismatch:{policy.get('source_next_burden_decision_id')}")
    if policy.get("source_after_revert_profile_id") != EXPECTED_AFTER_REVERT_PROFILE_ID:
        failures.append(f"policy_profile_mismatch:{policy.get('source_after_revert_profile_id')}")
    if policy.get("target_burden_class") != TARGET_BURDEN_CLASS:
        failures.append(f"policy_target_mismatch:{policy.get('target_burden_class')}")

    target = policy.get("target_burden_evidence") or {}
    if target.get("rows") != 1:
        failures.append(f"policy_target_rows_not_1:{target.get('rows')}")
    if target.get("receipts") != 176:
        failures.append(f"policy_target_receipts_not_176:{target.get('receipts')}")
    if target.get("elapsed_ms") != 1005:
        failures.append(f"policy_target_elapsed_not_1005:{target.get('elapsed_ms')}")
    if target.get("families") != [EXPECTED_FAMILY]:
        failures.append(f"policy_target_family_mismatch:{target.get('families')}")
    if target.get("probes") != [EXPECTED_PROBE]:
        failures.append(f"policy_target_probe_mismatch:{target.get('probes')}")
    if target.get("slots") != [EXPECTED_SLOT]:
        failures.append(f"policy_target_slot_mismatch:{target.get('slots')}")

    if policy.get("accepted_burden_classes_frozen") != ACCEPTED_FROZEN:
        failures.append(f"accepted_frozen_mismatch:{policy.get('accepted_burden_classes_frozen')}")
    if policy.get("rejected_or_deferred_burden_classes_frozen") != REJECTED_OR_DEFERRED:
        failures.append(f"rejected_or_deferred_mismatch:{policy.get('rejected_or_deferred_burden_classes_frozen')}")

    scope = policy.get("policy_scope") or {}
    if scope.get("policy_only_no_patch_application") is not True:
        failures.append("policy_not_policy_only")
    if scope.get("authorizes_exactly_one_fix_candidate") is not True:
        failures.append("policy_does_not_authorize_exactly_one_candidate")
    if scope.get("authorized_fix_candidate_id") != AUTHORIZED_FIX_CANDIDATE_ID:
        failures.append(f"policy_candidate_id_mismatch:{scope.get('authorized_fix_candidate_id')}")
    if scope.get("authorized_fix_candidate_kind") != AUTHORIZED_FIX_CANDIDATE_KIND:
        failures.append(f"policy_candidate_kind_mismatch:{scope.get('authorized_fix_candidate_kind')}")
    if scope.get("authorized_target_burden_class") != TARGET_BURDEN_CLASS:
        failures.append(f"policy_scope_target_mismatch:{scope.get('authorized_target_burden_class')}")
    for key in [
        "candidate_must_preserve_receipt_rows",
        "candidate_must_preserve_receipt_payload_durability",
        "candidate_must_preserve_registry_sqlite_totals",
        "candidate_must_preserve_raw_receipt_writes",
        "candidate_must_preserve_profile_total_1457",
    ]:
        if scope.get(key) is not True:
            failures.append(f"policy_scope_missing_preservation:{key}:{scope.get(key)}")

    auth = policy.get("authorization") or {}
    if auth.get("authorizes_fix_candidate_count") != 1:
        failures.append(f"policy_candidate_count_wrong:{auth.get('authorizes_fix_candidate_count')}")
    if auth.get("authorizes_fix_candidate_ids") != [AUTHORIZED_FIX_CANDIDATE_ID]:
        failures.append(f"policy_candidate_ids_wrong:{auth.get('authorizes_fix_candidate_ids')}")
    if auth.get("authorizes_fix_candidate_kind") != AUTHORIZED_FIX_CANDIDATE_KIND:
        failures.append(f"policy_candidate_kind_wrong:{auth.get('authorizes_fix_candidate_kind')}")

    for key in [
        "authorizes_patch_application",
        "authorizes_code_change_now",
        "authorizes_receipt_deletion",
        "authorizes_receipt_compression",
        "authorizes_receipt_lossy_summary",
        "authorizes_raw_receipt_write_suppression",
        "authorizes_registry_sqlite_total_mismatch",
        "authorizes_execution_skipping",
        "authorizes_probe_skipping",
        "authorizes_receipt_write_pressure_skipping",
        "authorizes_synthetic_receipts",
        "authorizes_reusing_prior_receipt_volume_results_as_execution",
        "authorizes_depth_range_change",
        "authorizes_radius_expansion",
        "authorizes_halt_semantics_change",
        "authorizes_law_semantics_change",
        "authorizes_gate_semantics_change",
        "authorizes_run_semantics_change",
        "authorizes_reopening_accepted_burden_classes",
        "authorizes_reopening_frontier_depth",
        "authorizes_more_frontier_depth_patching",
        "authorizes_data_artifact_deletion",
    ]:
        if auth.get(key) is not False:
            failures.append(f"policy_illegal_authorization:{key}:{auth.get(key)}")

    req = policy.get("candidate_requirements") or {}
    if req.get("candidate_status_must_be") != "PROPOSAL_ONLY_NOT_APPLIED":
        failures.append(f"candidate_status_requirement_wrong:{req.get('candidate_status_must_be')}")
    if req.get("candidate_must_target_burden_class") != TARGET_BURDEN_CLASS:
        failures.append(f"candidate_target_requirement_wrong:{req.get('candidate_must_target_burden_class')}")
    if req.get("candidate_must_use_source_policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"candidate_source_policy_requirement_wrong:{req.get('candidate_must_use_source_policy_id')}")
    if req.get("candidate_must_use_source_profile_id") != EXPECTED_AFTER_REVERT_PROFILE_ID:
        failures.append(f"candidate_source_profile_requirement_wrong:{req.get('candidate_must_use_source_profile_id')}")
    if req.get("candidate_must_use_source_decision_id") != EXPECTED_NEXT_DECISION_ID:
        failures.append(f"candidate_source_decision_requirement_wrong:{req.get('candidate_must_use_source_decision_id')}")
    if req.get("candidate_must_preserve_receipts") != 176:
        failures.append(f"candidate_preserve_receipts_requirement_wrong:{req.get('candidate_must_preserve_receipts')}")
    if req.get("candidate_must_preserve_micro_profile_receipt_total") != 1457:
        failures.append(f"candidate_preserve_profile_total_requirement_wrong:{req.get('candidate_must_preserve_micro_profile_receipt_total')}")
    if req.get("candidate_must_preserve_families_seen") != ["A", "B", "C", "D", "E"]:
        failures.append("candidate_preserve_families_requirement_wrong")
    if req.get("candidate_must_preserve_all_non_unknown_burden_classes") != EXPECTED_ALL_NON_UNKNOWN:
        failures.append("candidate_preserve_burden_classes_requirement_wrong")

    ident = req.get("candidate_must_preserve_target_row_identity") or {}
    if ident != {
        "rows": 1,
        "family_compact": EXPECTED_FAMILY,
        "probe_id": EXPECTED_PROBE,
        "slot_id": EXPECTED_SLOT,
        "burden_class": TARGET_BURDEN_CLASS,
    }:
        failures.append(f"candidate_target_identity_requirement_wrong:{ident}")

    frozen = req.get("candidate_must_not_modify_or_reopen") or {}
    if frozen.get("accepted_burden_classes") != ACCEPTED_FROZEN:
        failures.append("candidate_accepted_frozen_requirement_wrong")
    if frozen.get("rejected_depth_scan") is not True:
        failures.append("candidate_rejected_depth_requirement_wrong")

    required_negatives = set(req.get("candidate_must_include_negative_controls_for") or [])
    for expected in [
        "receipt deletion authority",
        "receipt compression authority",
        "raw receipt suppression authority",
        "registry total mismatch authority",
        "synthetic receipt authority",
        "execution skipping authority",
        "receipt write pressure skipping authority",
        "target row identity drift",
        "profile total drift",
        "accepted class reopening",
        "frontier-depth reopening",
    ]:
        if expected not in required_negatives:
            failures.append(f"candidate_negative_control_missing:{expected}")

    terminal = policy.get("terminal") or {}
    if terminal.get("next_command_goal") != "BUILD_RECEIPT_VOLUME_FIX_CANDIDATE_V0":
        failures.append(f"policy_terminal_goal_mismatch:{terminal.get('next_command_goal')}")

    return failures


def verify_profile(profile: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if profile.get("profile_id") != EXPECTED_AFTER_REVERT_PROFILE_ID:
        failures.append(f"profile_id_mismatch:{profile.get('profile_id')}")
    if profile.get("gate") != "MICRO_BURDEN_PROFILE_PASS":
        failures.append("profile_gate_not_PASS")
    if profile.get("failures") != []:
        failures.append(f"profile_failures_not_empty:{profile.get('failures')}")
    if len(profile.get("rows") or []) != 25:
        failures.append(f"profile_rows_not_25:{len(profile.get('rows') or [])}")
    if profile.get("families_seen") != ["A", "B", "C", "D", "E"]:
        failures.append(f"profile_families_wrong:{profile.get('families_seen')}")
    if profile.get("profile_receipts_total") != 1457:
        failures.append(f"profile_total_not_1457:{profile.get('profile_receipts_total')}")
    if profile.get("profile_receipts_total") != profile.get("db_receipt_delta"):
        failures.append("profile_total_mismatch_registry")
    if profile.get("non_unknown_burden_classes") != EXPECTED_ALL_NON_UNKNOWN:
        failures.append(f"profile_non_unknown_mismatch:{profile.get('non_unknown_burden_classes')}")
    if "frontier_depth_probe" in profile:
        failures.append("profile_frontier_depth_probe_field_present")
    if "cycle_period_compression" not in profile:
        failures.append("profile_cycle_period_field_missing")

    sem = profile.get("semantics") or {}
    for key in [
        "execution_skipped",
        "runner_semantics_changed",
        "gate_semantics_changed",
        "law_semantics_changed",
        "receipt_rows_deleted",
        "receipts_compressed",
    ]:
        if sem.get(key) is not False:
            failures.append(f"profile_semantics_not_preserved:{key}:{sem.get(key)}")
    if sem.get("passive_observability_layer") is not True:
        failures.append("profile_passive_observability_missing")

    target = summarize_target(profile)
    if target["rows"] != 1:
        failures.append(f"target_rows_not_1:{target['rows']}")
    if target["receipts"] != 176:
        failures.append(f"target_receipts_not_176:{target['receipts']}")
    if target["elapsed_ms"] != 1005:
        failures.append(f"target_elapsed_not_1005:{target['elapsed_ms']}")
    if target["families"] != [EXPECTED_FAMILY]:
        failures.append(f"target_family_mismatch:{target['families']}")
    if target["probes"] != [EXPECTED_PROBE]:
        failures.append(f"target_probe_mismatch:{target['probes']}")
    if target["slots"] != [EXPECTED_SLOT]:
        failures.append(f"target_slot_mismatch:{target['slots']}")

    return failures


def inspect_current_source() -> dict[str, Any]:
    path = ROOT / "scripts" / "wide_burden_profile_microruns.py"
    text = path.read_text()

    return {
        "file": "scripts/wide_burden_profile_microruns.py",
        "exists": path.exists(),
        "frontier_depth_probe_field_present": '"frontier_depth_probe"' in text,
        "cycle_period_compression_field_present": '"cycle_period_compression"' in text,
        "receipt_volume_probe_marker_present": "MICRO_05_RECEIPT_WRITE_PRESSURE" in text,
        "receipt_volume_slot_literal_present": "MICRO_05_RECEIPT_WRITE_PRESSURE_E" in text,
        "receipt_volume_slot_identity_source": "profile_target_row_identity",
        "profile_total_literal_1457_present": "1457" in text,
    }


def build_candidate(policy_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    CANDIDATE_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    policy = load_json(POLICY_DIR / f"{policy_id}.json")
    decision = load_json(NEXT_DECISION_DIR / f"{EXPECTED_NEXT_DECISION_ID}.json")
    profile = load_json(PROFILE_DIR / f"{EXPECTED_AFTER_REVERT_PROFILE_ID}.json")

    failures: list[str] = []
    failures.extend(verify_policy(policy))
    failures.extend(verify_profile(profile))

    if decision.get("decision_id") != EXPECTED_NEXT_DECISION_ID or decision.get("gate") != "PASS":
        failures.append("source_next_burden_decision_invalid")
    if decision.get("selected_next_burden_class") != TARGET_BURDEN_CLASS:
        failures.append(f"source_decision_target_wrong:{decision.get('selected_next_burden_class')}")
    if decision.get("authorization", {}).get("authorizes_next_burden_policy") is not True:
        failures.append("source_decision_policy_not_authorized")
    if decision.get("authorization", {}).get("authorizes_patch_application") is not False:
        failures.append("source_decision_illegally_authorizes_patch")

    target = summarize_target(profile)
    source_inspection = inspect_current_source()
    if source_inspection["frontier_depth_probe_field_present"] is not False:
        failures.append("source_inspection_frontier_depth_probe_present")
    if source_inspection["cycle_period_compression_field_present"] is not True:
        failures.append("source_inspection_cycle_period_missing")
    if source_inspection["receipt_volume_probe_marker_present"] is not True:
        failures.append("source_inspection_receipt_volume_probe_missing")
    # The full slot id is profile-derived, not required as a source-code literal.
    # The source only needs the receipt-volume probe machinery; exact row identity
    # is guarded by the profile target row, policy, and candidate application gate.
    if source_inspection.get("receipt_volume_slot_identity_source") != "profile_target_row_identity":
        failures.append("source_inspection_receipt_volume_slot_identity_source_invalid")

    candidate = {
        "schema_version": "receipt_volume_fix_candidate_v0",
        "candidate_kind": AUTHORIZED_FIX_CANDIDATE_KIND,
        "candidate_name": AUTHORIZED_FIX_CANDIDATE_ID,
        "candidate_status": "PROPOSAL_ONLY_NOT_APPLIED",
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_next_burden_decision_id": EXPECTED_NEXT_DECISION_ID,
        "source_after_revert_profile_id": EXPECTED_AFTER_REVERT_PROFILE_ID,
        "target_burden_class": TARGET_BURDEN_CLASS,
        "target_burden_evidence": target,
        "candidate_goal": {
            "goal": "Reduce receipt-volume write-path overhead without reducing receipt volume.",
            "non_goal": "Do not reduce receipt count by deletion, compression, suppression, lossy summaries, or synthetic replacement.",
            "burden_interpretation": "The burden class is about write-path / volume pressure; correctness requires exact receipt durability, not fewer receipts.",
        },
        "proposed_design": {
            "design_id": "RECEIPT_WRITE_PRESSURE_PLAN_CACHE_AND_ACCOUNTING_CERTIFICATE_V0",
            "design_class": "metadata_and_write_path_plan_proposal",
            "proposal_only": True,
            "touches_code_now": False,
            "future_patch_scope": [
                "scripts/wide_burden_profile_microruns.py"
            ],
            "allowed_future_change_summary": [
                "Within a single micro profile execution, build the receipt-write-pressure run plan once and pass its immutable plan metadata to the write-pressure probe.",
                "Add a post-execution receipt-volume accounting certificate recording expected target row identity, exact receipt count, raw write preservation, and registry total equality.",
                "Keep actual stress execution and receipt emission unchanged; no result reuse as execution.",
                "Preserve the target row MICRO_05_RECEIPT_WRITE_PRESSURE_E and the exact 176 receipts.",
            ],
            "expected_effect_hypothesis": {
                "primary": "Reduce Python-side repeated planning/accounting overhead around receipt-volume pressure measurement.",
                "secondary": "Make any future comparison distinguish true write-path improvement from illegal receipt loss.",
                "explicit_uncertainty": "This is a candidate hypothesis only; it is not accepted until applied and compared by retest.",
            },
            "hard_preservation_contract": {
                "target_receipts_must_remain": 176,
                "profile_receipt_total_must_remain": 1457,
                "registry_sqlite_total_must_match": True,
                "raw_receipt_rows_must_remain_available": True,
                "receipt_payload_durability_must_remain": True,
                "target_row_identity_must_remain": {
                    "rows": 1,
                    "family_compact": EXPECTED_FAMILY,
                    "probe_id": EXPECTED_PROBE,
                    "slot_id": EXPECTED_SLOT,
                    "burden_class": TARGET_BURDEN_CLASS,
                },
                "families_seen_must_remain": ["A", "B", "C", "D", "E"],
                "non_unknown_burden_classes_must_remain": EXPECTED_ALL_NON_UNKNOWN,
            },
        },
        "proposed_future_patch_plan": [
            {
                "step": 1,
                "operation": "Add immutable ReceiptVolumeWritePressurePlan metadata object inside wide_burden_profile_microruns.py.",
                "allowed": True,
                "forbidden": [
                    "Do not cache execution results.",
                    "Do not cache receipt rows.",
                    "Do not suppress writes.",
                ],
            },
            {
                "step": 2,
                "operation": "Thread the plan metadata through MICRO_05_RECEIPT_WRITE_PRESSURE only.",
                "allowed": True,
                "forbidden": [
                    "Do not change probe family/depth/cycle/max-cells parameters.",
                    "Do not change halt/law/gate/run semantics.",
                    "Do not affect other burden classes.",
                ],
            },
            {
                "step": 3,
                "operation": "Add receipt-volume accounting certificate to the profile output after execution.",
                "allowed": True,
                "forbidden": [
                    "Do not replace raw receipts with certificate.",
                    "Do not count certificate as a receipt substitute.",
                    "Do not allow the certificate to authorize fewer receipt rows.",
                ],
            },
            {
                "step": 4,
                "operation": "Run the same micro suite and compare before/after against profile b6609f93.",
                "allowed": True,
                "forbidden": [
                    "Do not accept if target receipts differ from 176.",
                    "Do not accept if profile total differs from 1457.",
                    "Do not accept if registry totals mismatch.",
                ],
            },
        ],
        "application_authorization_requested": {
            "requested_next_command_goal": "APPLY_RECEIPT_VOLUME_FIX_CANDIDATE_V0",
            "requested_patch_scope": ["scripts/wide_burden_profile_microruns.py"],
            "requires_explicit_application_command": True,
            "candidate_itself_applies_no_patch": True,
        },
        "candidate_authorization": {
            "authorizes_application_next": True,
            "authorized_next_command_goal": NEXT_COMMAND_GOAL,
            "authorizes_patch_application_now": False,
            "authorizes_code_change_now": False,
            "authorizes_receipt_deletion": False,
            "authorizes_receipt_compression": False,
            "authorizes_receipt_lossy_summary": False,
            "authorizes_raw_receipt_write_suppression": False,
            "authorizes_registry_sqlite_total_mismatch": False,
            "authorizes_receipt_schema_change": False,
            "authorizes_execution_skipping": False,
            "authorizes_probe_skipping": False,
            "authorizes_receipt_write_pressure_skipping": False,
            "authorizes_synthetic_receipts": False,
            "authorizes_reusing_prior_receipt_volume_results_as_execution": False,
            "authorizes_depth_range_change": False,
            "authorizes_radius_expansion": False,
            "authorizes_halt_semantics_change": False,
            "authorizes_law_semantics_change": False,
            "authorizes_gate_semantics_change": False,
            "authorizes_run_semantics_change": False,
            "authorizes_reopening_accepted_burden_classes": False,
            "authorizes_reopening_frontier_depth": False,
            "authorizes_more_frontier_depth_patching": False,
            "authorizes_data_artifact_deletion": False,
        },
        "required_application_gate": {
            "must_use_candidate_id": None,
            "must_use_policy_id": EXPECTED_POLICY_ID,
            "must_use_before_profile_id": EXPECTED_AFTER_REVERT_PROFILE_ID,
            "must_target_burden_class": TARGET_BURDEN_CLASS,
            "must_touch_only_files": ["scripts/wide_burden_profile_microruns.py"],
            "must_preserve_target_row_identity": {
                "rows": 1,
                "family_compact": EXPECTED_FAMILY,
                "probe_id": EXPECTED_PROBE,
                "slot_id": EXPECTED_SLOT,
                "burden_class": TARGET_BURDEN_CLASS,
            },
            "must_preserve_target_receipts": 176,
            "must_preserve_micro_profile_receipt_total": 1457,
            "must_preserve_raw_receipt_writes": True,
            "must_preserve_registry_sqlite_totals": True,
            "must_preserve_receipt_payload_durability": True,
            "must_preserve_cycle_period_observation": True,
            "must_not_restore_frontier_depth_probe_field": True,
            "must_not_reopen_accepted_burden_classes": ACCEPTED_FROZEN,
            "must_not_reopen_rejected_depth_scan": True,
            "must_not_delete_receipts": True,
            "must_not_compress_receipts": True,
            "must_not_suppress_raw_receipt_writes": True,
            "must_not_emit_synthetic_receipts": True,
            "must_not_skip_execution": True,
            "must_not_skip_receipt_write_pressure_probe": True,
            "must_not_change_halt_law_gate_run_semantics": True,
            "must_not_change_depth_range": True,
            "must_not_expand_radius": True,
        },
        "required_negative_controls": [
            {
                "case": "receipt_deletion_authority_fail",
                "must_fail_if": "candidate or application authorizes receipt deletion",
            },
            {
                "case": "receipt_compression_authority_fail",
                "must_fail_if": "candidate or application authorizes receipt compression",
            },
            {
                "case": "raw_receipt_suppression_authority_fail",
                "must_fail_if": "candidate or application authorizes raw receipt write suppression",
            },
            {
                "case": "registry_total_mismatch_authority_fail",
                "must_fail_if": "candidate or application authorizes registry.sqlite total mismatch",
            },
            {
                "case": "synthetic_receipt_authority_fail",
                "must_fail_if": "candidate or application authorizes synthetic receipts",
            },
            {
                "case": "execution_skipping_authority_fail",
                "must_fail_if": "candidate or application authorizes execution skipping",
            },
            {
                "case": "receipt_write_pressure_skip_authority_fail",
                "must_fail_if": "candidate or application authorizes receipt-write-pressure probe skipping",
            },
            {
                "case": "target_row_identity_drift_fail",
                "must_fail_if": "target slot/probe/family/burden identity changes",
            },
            {
                "case": "target_receipt_count_drift_fail",
                "must_fail_if": "target receipts are not exactly 176",
            },
            {
                "case": "profile_total_drift_fail",
                "must_fail_if": "micro profile total is not exactly 1457",
            },
            {
                "case": "accepted_class_reopen_fail",
                "must_fail_if": "accepted/frozen burden classes are reopened",
            },
            {
                "case": "frontier_depth_reopen_fail",
                "must_fail_if": "BURDEN_DEPTH_SCAN or frontier-depth probe is reopened/restored",
            },
        ],
        "source_inspection": source_inspection,
        "accepted_burden_classes_frozen": ACCEPTED_FROZEN,
        "rejected_or_deferred_burden_classes_frozen": REJECTED_OR_DEFERRED,
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_RECEIPT_VOLUME_CANDIDATE_INVALID",
        },
        "failures": failures,
        "warnings": list(policy.get("warnings") or []),
        "gate": "PASS" if not failures else "FAIL",
        "created_at": now_iso(),
    }

    sig = stable_sig(candidate)
    candidate["candidate_id"] = sig
    candidate["candidate_sig8"] = sig
    candidate["required_application_gate"]["must_use_candidate_id"] = sig

    receipt = {
        "schema_version": "receipt_volume_fix_candidate_receipt_v0",
        "candidate_id": sig,
        "candidate_path": f"data/receipt_volume_fix_candidates/{sig}.json",
        "candidate_sig8": sig,
        "candidate_name": AUTHORIZED_FIX_CANDIDATE_ID,
        "candidate_kind": AUTHORIZED_FIX_CANDIDATE_KIND,
        "candidate_status": "PROPOSAL_ONLY_NOT_APPLIED",
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_next_burden_decision_id": EXPECTED_NEXT_DECISION_ID,
        "source_after_revert_profile_id": EXPECTED_AFTER_REVERT_PROFILE_ID,
        "target_burden_class": TARGET_BURDEN_CLASS,
        "target_rows": target["rows"],
        "target_receipts": target["receipts"],
        "target_elapsed_ms": target["elapsed_ms"],
        "target_receipts_per_sec": target["receipts_per_sec"],
        "target_probe": EXPECTED_PROBE,
        "target_slot": EXPECTED_SLOT,
        "proposed_design_id": candidate["proposed_design"]["design_id"],
        "authorizes_application_next": True,
        "authorized_next_command_goal": NEXT_COMMAND_GOAL,
        "authorizes_patch_application_now": False,
        "authorizes_code_change_now": False,
        "authorizes_receipt_deletion": False,
        "authorizes_receipt_compression": False,
        "authorizes_raw_receipt_write_suppression": False,
        "authorizes_registry_sqlite_total_mismatch": False,
        "authorizes_execution_skipping": False,
        "authorizes_synthetic_receipts": False,
        "accepted_burden_classes_frozen": ACCEPTED_FROZEN,
        "rejected_or_deferred_burden_classes_frozen": REJECTED_OR_DEFERRED,
        "gate": candidate["gate"],
        "terminal": candidate["terminal"],
        "failures": failures,
        "warnings": candidate["warnings"],
        "created_at": now_iso(),
    }

    rsig = stable_sig(receipt)
    receipt["receipt_id"] = rsig
    receipt["receipt_sig8"] = rsig

    (CANDIDATE_DIR / f"{sig}.json").write_text(json.dumps(candidate, indent=2, sort_keys=True))
    (RECEIPT_DIR / f"{sig}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return candidate, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", default=EXPECTED_POLICY_ID)
    args = parser.parse_args()

    candidate, receipt = build_candidate(args.policy)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"candidate_json_path=data/receipt_volume_fix_candidates/{candidate['candidate_id']}.json")
    print(f"candidate_receipt_path=data/receipt_volume_fix_candidate_receipts/{candidate['candidate_id']}.json")

    return 0 if candidate["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
