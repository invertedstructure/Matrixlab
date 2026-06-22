#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_JURISDICTION_RUNNER_V0_1_BOOTSTRAP_POLICY_V0"
NEXT_GOAL = "IMPLEMENT_JURISDICTION_RUNNER_V0_1_WITH_DRY_RUN_FIXTURE_V0"

SPEC_ID = "JURISDICTION_RUNNER_V0_1_ADAPTIVE_LOCAL_CLOSURE_RUNTIME"
RUNNER_UNIT_ID = "jurisdiction_runner.v0.1"
LOCAL_REGIME_VERSION = "local_regime.v0"

OUT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_bootstrap_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_bootstrap_policy_receipts"

REQUIRED_MOVE_TYPES = [
    "MOVE_VALIDATE_STATE",
    "MOVE_APPLY_REGISTERED_TRANSITION",
    "MOVE_EMIT_METRIC_RECEIPT",
]

REQUIRED_HALT_CODES = [
    "STOP_DONE",
    "STOP_NO_APPLICABLE_MOVE",
    "STOP_AUTHORITY_VIOLATION",
    "STOP_GATE_FAIL",
    "STOP_UNTYPED_OBJECT",
    "STOP_DEPENDENCY_MISSING",
]

REQUIRED_METRICS = [
    "move_count",
    "applied_move_count",
    "blocked_move_count",
    "halt_count_by_code",
    "typed_object_count",
    "untyped_object_count",
    "missing_dependency_count",
    "receipt_count",
    "authority_violation_count",
    "gate_fail_count",
    "proposal_emitted_count",
    "proposal_withheld_count",
    "proposal_count_by_type",
    "duplicate_unresolved_proposal_count",
    "halt_with_proposal_count",
    "halt_without_proposal_count",
    "local_closure_radius_observed",
    "receipt_burden_bytes",
    "metric_burden_bytes",
    "artifact_burden_bytes",
]

ALLOWED_PROPOSAL_CLASSES = [
    "MOVE_DELTA_PROPOSAL",
    "TAXONOMY_DELTA_PROPOSAL",
    "METRIC_DELTA_PROPOSAL",
    "RECEIPT_DELTA_PROPOSAL",
    "VALIDATION_DELTA_PROPOSAL",
    "JURISDICTION_DELTA_PROPOSAL",
    "DISTINGUISHABILITY_DELTA_PROPOSAL",
    "ARTIFACT_PACKAGING_DELTA_PROPOSAL",
    "TERMINAL_CONTRACT_DELTA_PROPOSAL",
]

FORBIDDEN_PROPOSAL_CLASSES = [
    "GLOBAL_ARCHITECTURE_PROPOSAL",
    "FINAL_TAXONOMY_PROPOSAL",
    "UNBOUNDED_AUTONOMY_PROPOSAL",
    "RUNTIME_MUTATION_PROPOSAL",
    "REGISTRY_DATABASE_WRITE_PROPOSAL",
    "SELF_ACCEPTING_PROPOSAL",
    "PROOF_CLAIM_PROPOSAL",
]

EXPECTED_DRY_RUN_TRANSCRIPT = [
    "LOAD_REGIME",
    "LOAD_STATE",
    "VALIDATE_STATE",
    "SELECT_MOVE",
    "CHECK_AUTHORITY",
    "APPLY_OR_BLOCK_MOVE",
    "EMIT_RECEIPT",
    "EMIT_METRICS",
    "EMIT_TERMINAL",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def blob(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(blob(obj)).hexdigest()[:8]

def build_policy(write_outputs: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    local_regime_seed = {
        "local_regime_version": LOCAL_REGIME_VERSION,
        "runner_unit_id": RUNNER_UNIT_ID,
        "move_types": REQUIRED_MOVE_TYPES,
        "halt_codes": REQUIRED_HALT_CODES,
        "metrics": REQUIRED_METRICS,
        "proposal_classes": ALLOWED_PROPOSAL_CLASSES,
        "terminal_contract": "ADVANCE authorizes exact next command; STOP forbids automatic command emission",
        "artifact_packaging": "path-addressed receipt-referenced explicit artifact guards",
    }
    local_regime_hash = sha8(local_regime_seed)

    policy_seed = {
        "unit_id": UNIT_ID,
        "spec_id": SPEC_ID,
        "runner_unit_id": RUNNER_UNIT_ID,
        "local_regime_version": LOCAL_REGIME_VERSION,
        "local_regime_hash": local_regime_hash,
        "next_goal": NEXT_GOAL,
    }
    policy_id = sha8(policy_seed)

    authority_guards = {
        "bootstrap_policy_built": True,
        "runner_implemented": False,
        "runner_executed": False,
        "dry_run_fixture_created": False,
        "dry_run_fixture_executed": False,
        "local_regime_runtime_mutated": False,
        "proposal_promoted": False,
        "registry_written": False,
        "registry_inserted": False,
        "registry_sqlite_read": False,
        "registry_sqlite_written": False,
        "runtime_code_changed_by_policy": False,
        "runtime_semantic_changed_by_policy": False,
        "global_taxonomy_claimed": False,
        "final_schema_claimed": False,
        "proof_claimed": False,
        "hidden_continuation_authorized": False,
    }

    policy = {
        "schema_version": "jurisdiction_runner_v0_1_bootstrap_policy_v0",
        "policy_type": "JURISDICTION_RUNNER_V0_1_BOOTSTRAP_POLICY",
        "policy_id": policy_id,
        "unit_id": UNIT_ID,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "spec_id": SPEC_ID,
        "runner_unit_id": RUNNER_UNIT_ID,
        "local_regime_version": LOCAL_REGIME_VERSION,
        "local_regime_hash": local_regime_hash,
        "build_target": {
            "runner": RUNNER_UNIT_ID,
            "regime": LOCAL_REGIME_VERSION,
            "minimum_scope": "one dry-run fixture with expected transcript",
            "implementation_next_goal": NEXT_GOAL,
        },
        "required_surfaces": {
            "execution_surface": {
                "fixed_local_regime": True,
                "registered_moves_only": True,
                "typed_halts_only": True,
                "deterministic_selector": True,
                "selector_tie_break": [
                    "explicit move_priority",
                    "lexical move_id order",
                ],
                "no_runtime_regime_mutation": True,
            },
            "proposition_surface": {
                "bounded": True,
                "non_executing": True,
                "requires_review_before_promotion": True,
                "accepted_proposals_apply_only_to_later_regime_version": True,
                "duplicate_unresolved_proposal_guard": True,
            },
            "terminal_command_contract": {
                "advance_authorizes_exact_next_command": True,
                "stop_forbids_automatic_command": True,
                "stop_done_closes_lane": True,
                "recommendation_is_not_command_authority": True,
            },
            "artifact_packaging_discipline": {
                "input_artifacts_path_addressed": True,
                "output_artifacts_receipt_referenced": True,
                "required_dependencies_verified": True,
                "tracked_when_permanence_required": True,
                "unrelated_untracked_data_not_authority": True,
            },
            "registry_metadata_distinction": {
                "metadata_record_is_not_database_write": True,
                "registry_sqlite_write_forbidden": True,
                "registry_sqlite_read_forbidden": True,
                "full_registry_scan_forbidden": True,
            },
        },
        "required_move_types": REQUIRED_MOVE_TYPES,
        "required_halt_codes": REQUIRED_HALT_CODES,
        "required_metrics": REQUIRED_METRICS,
        "allowed_proposal_classes": ALLOWED_PROPOSAL_CLASSES,
        "forbidden_proposal_classes": FORBIDDEN_PROPOSAL_CLASSES,
        "required_receipt_fields": [
            "receipt_id",
            "receipt_type",
            "run_id",
            "unit_id",
            "local_regime_version",
            "local_regime_hash",
            "input_state_id",
            "input_artifact_paths",
            "state_before_hash",
            "state_after_hash",
            "selector_rule",
            "selected_move_id",
            "move_id",
            "move_status",
            "halt_code",
            "proposal_status",
            "proposal_id",
            "no_proposal_reason",
            "metrics",
            "authority_guards",
            "artifact_guards",
            "terminal",
        ],
        "required_dry_run_fixture": {
            "fixture_count": 1,
            "expected_transcript_required": True,
            "expected_transcript": EXPECTED_DRY_RUN_TRANSCRIPT,
            "must_test": [
                "state loaded",
                "state validated",
                "selector evaluated",
                "move selected",
                "move applied or blocked",
                "receipt emitted",
                "metrics emitted",
                "terminal emitted",
                "artifact guards emitted",
            ],
        },
        "authorized_operations_next": {
            "read_bootstrap_policy": True,
            "read_bootstrap_policy_receipt": True,
            "create_local_regime_v0_declaration": True,
            "implement_jurisdiction_runner_v0_1": True,
            "create_one_dry_run_fixture": True,
            "create_expected_dry_run_transcript": True,
            "emit_implementation_receipt": True,
        },
        "forbidden_operations": {
            "execute_runner_in_policy_unit": True,
            "promote_proposals_in_policy_unit": True,
            "mutate_runtime_registry": True,
            "registry_sqlite_write": True,
            "registry_sqlite_read": True,
            "full_registry_scan": True,
            "global_taxonomy_design": True,
            "final_schema_claim": True,
            "proof_claim": True,
            "hidden_continuation_after_stop": True,
            "ambient_workspace_authority": True,
            "latest_or_mtime_selection": True,
            "untracked_artifact_as_hidden_authority": True,
        },
        "safety_clauses": {
            "policy_only": True,
            "does_not_implement_runner": True,
            "does_not_execute_runner": True,
            "does_not_create_regime_version_runtime_effect": True,
            "does_not_promote_any_proposal": True,
            "does_not_write_registry": True,
            "does_not_claim_global_correctness": True,
            "does_not_claim_theorem_closure": True,
            "next_unit_required_for_implementation": True,
        },
        "authority_guards": authority_guards,
        "terminal": {
            "type": "ADVANCE",
            "next_command_goal": NEXT_GOAL,
            "stop_code": None,
        },
        "gate": "PASS",
        "failures": [],
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt = {
        "schema_version": "jurisdiction_runner_v0_1_bootstrap_policy_receipt_v0",
        "receipt_type": "JURISDICTION_RUNNER_V0_1_BOOTSTRAP_POLICY_RECEIPT",
        "unit_id": UNIT_ID,
        "policy_id": policy_id,
        "policy_status": policy["policy_status"],
        "spec_id": SPEC_ID,
        "runner_unit_id": RUNNER_UNIT_ID,
        "local_regime_version": LOCAL_REGIME_VERSION,
        "local_regime_hash": local_regime_hash,
        "build_target": policy["build_target"],
        "required_surfaces": policy["required_surfaces"],
        "required_move_types": REQUIRED_MOVE_TYPES,
        "required_halt_codes": REQUIRED_HALT_CODES,
        "required_metrics": REQUIRED_METRICS,
        "allowed_proposal_classes": ALLOWED_PROPOSAL_CLASSES,
        "forbidden_proposal_classes": FORBIDDEN_PROPOSAL_CLASSES,
        "required_dry_run_fixture": policy["required_dry_run_fixture"],
        "authorized_operations_next": policy["authorized_operations_next"],
        "forbidden_operations": policy["forbidden_operations"],
        "safety_clauses": policy["safety_clauses"],
        "authority_guards": authority_guards,
        "terminal": policy["terminal"],
        "gate": policy["gate"],
        "failures": [],
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id
    policy["policy_receipt_id"] = receipt_id

    if write_outputs:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
        (OUT_DIR / f"{policy_id}.json").write_text(json.dumps(policy, indent=2, sort_keys=True) + "\n")
        (OUT_RECEIPT_DIR / f"{policy_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")

    return policy, receipt

def main() -> int:
    policy, receipt = build_policy(write_outputs=True)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bootstrap_policy_id={policy['policy_id']}")
    print(f"bootstrap_policy_receipt_id={receipt['receipt_id']}")
    print(f"bootstrap_policy_path=data/jurisdiction_runner_v0_1_bootstrap_policies/{policy['policy_id']}.json")
    print(f"bootstrap_policy_receipt_path=data/jurisdiction_runner_v0_1_bootstrap_policy_receipts/{policy['policy_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
