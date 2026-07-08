#!/usr/bin/env python3
"""Build C8 n22 prepare-next-unit surface machine proceed v0.

D.4 performs the single radius-bound preparation action authorized by the
D.3 active archive entry. It creates a next bounded unit definition surface,
records exactly one radius unit consumed, and does not execute the unit.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_prepare_next_unit_definition_surface_machine_proceed_v0.py"
PROCEED_JSON = "docs/matrixlabs/proceed/c8_n22_prepare_next_unit_definition_surface_machine_proceed_v0.json"
PROCEED_MD = "docs/matrixlabs/proceed/c8_n22_prepare_next_unit_definition_surface_machine_proceed_v0.md"
SURFACE_JSON = "docs/matrixlabs/unit_surfaces/c8_n22_next_bounded_unit_definition_surface_v0.json"
SURFACE_MD = "docs/matrixlabs/unit_surfaces/c8_n22_next_bounded_unit_definition_surface_v0.md"

ACTIVE_ENTRY = "docs/matrixlabs/validator_archive/active/c8_n22_prepare_next_unit_definition_active_archive_entry_v0.json"
PROMOTION_RECEIPT = "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_receipt_v0.json"
PROMOTION_SURFACE = "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_surface_v0.json"
CANDIDATE_ENTRY = "docs/matrixlabs/validator_archive/candidates/c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.json"
CANDIDATE_AUDIT = "docs/matrixlabs/validator_archive/audits/c8_n22_candidate_archive_entry_admissibility_audit_v0.json"
SCHEMA_CONTRACT = "docs/matrixlabs/validator_archive/validator_archive_entry_schema_contract_v0.json"
REQUESTED_ACTION_RECORD = "docs/matrixlabs/router/c8_n22_requested_action_prepare_next_unit_definition_surface_v0.json"
ROUTE_CLASSIFICATION = "docs/matrixlabs/router/c8_n22_authority_route_classification_v0.json"

D3_COMMIT = "d4eda408759be982c2d9dff2622a54b9dd7b7ac0"
D2_COMMIT = "41233ed53084b9ceb2348661d07342feaf65cac7"
D1_COMMIT = "a457bf08eb263cdbdad01a4eef6b7e7e2b11f230"
C3_COMMIT = "f49dfab97774414330682151e6e3fffeb7ba6f66"
C2_COMMIT = "674c601136f381c9d85605f646900998b24ddfe9"
C1_COMMIT = "96223d2a9827543c27f93a1c0a16a6670a97de71"

SCHEMA_VERSION = "matrixlabs_machine_proceed_receipt_v0"
MACHINE_PROCEED_ID = "c8.n22.prepare_next_unit_definition_surface.machine_proceed.v0"
PROCEED_ROLE = "RADIUS_BOUND_MACHINE_PREPARATION_ACTION"
PROCEED_STATUS = "MACHINE_PROCEED_PASS_RADIUS_BOUND_PREPARATION_ONLY"
BLOCK_ID = "BLOCK_D"
BLOCK_UNIT_ID = "D4_MACHINE_PROCEED_UNDER_ACTIVE_ENTRY"
PRECOMMIT_GATE = "PASS"
TERMINAL_TRANSITION = "ADVANCE(D5_MACHINE_PROCEED_CLOSURE_PENDING)"

ACTIVE_SCHEMA = "matrixlabs_active_archive_entry_materialization_v0"
ACTIVE_MATERIALIZATION_ID = "c8.n22.prepare_next_unit_definition.active_archive_entry_materialization.v0"
ACTIVE_ENTRY_ID = "active.c8.n22.prepare_next_unit_definition_surface.v0"
ACTIVE_MATERIALIZATION_STATUS = "ACTIVE_ARCHIVE_ENTRY_PASS_MATERIALIZED_FOR_DECLARED_SCOPE"
ACTIVE_ENTRY_STATUS = "ARCHIVE_STATUS_PREAPPROVED_ACTIVE"
PROMOTION_STATUS = "PROMOTION_GRANTED_FOR_DECLARED_SCOPE"
REUSE_AUTHORITY_STATUS = "REUSE_AUTHORITY_GRANTED_FOR_DECLARED_SCOPE"
ACTIVATION_STATUS = "ACTIVATION_ACTIVE"
DECLARED_SCOPE = "DECLARED_SCOPE_ONLY"

RECEIPT_ID = "c8.n22.candidate_promotion_decision_receipt.v0"
RECEIPT_GATE = "PROMOTION_DECISION_RECEIPT_PASS_TYPED_DECISION_RECORDED"
SURFACE_ID = "c8.n22.candidate_promotion_decision_surface.v0"
CANDIDATE_ID = "candidate.c8.n22.prepare_next_unit_definition_surface.v0"
AUDIT_ID = "c8.n22.candidate_archive_entry.admissibility_audit.v0"
AUDIT_STATUS = "CANDIDATE_AUDIT_PASS_CONTRACT_CONFORMANT_NOT_PROMOTED"
CONTRACT_ID = "validator_archive_entry_schema_contract.v0"

REQUESTED_ACTION_RECORD_ID = "c8.n22.request.prepare_next_bounded_unit_definition_surface.v0"
ROUTE_CLASSIFICATION_ID = "c8.n22.route.prepare_next_unit_definition_surface.v0"
AUTHORITY_STATE = "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION"
ACTION = "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"
ACTION_SCOPE = "PREPARE_SURFACE_ONLY"
BASIS_SCOPE = "C8_N22_BASIS_ONLY"
SOURCE_OBJECT_ID = "c8.n22"
OUTPUT_KIND = "NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"
OUTPUT_OBJECT_ID = "c8.n22.next_bounded_unit_definition_surface.v0"
OUTPUT_SCOPE = "SURFACE_ONLY"
OUTPUT_EXECUTION_STATUS = "NOT_EXECUTED"
RADIUS_LIMIT = "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT"

UNIT_SURFACE_SCHEMA = "matrixlabs_next_bounded_unit_definition_surface_v0"
UNIT_SURFACE_ID = "c8.n22.next_bounded_unit_definition_surface.v0"
UNIT_SURFACE_ROLE = "NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"
UNIT_SURFACE_STATUS = "NEXT_UNIT_DEFINITION_SURFACE_PREPARED_NOT_EXECUTED"
PLACEHOLDER_UNIT_ID = "c8.n22.next_unit.placeholder.v0"
PLACEHOLDER_KIND = "NEXT_UNIT_DECISION_SURFACE_PLACEHOLDER"
PLACEHOLDER_STATUS = "PLACEHOLDER_NOT_SELECTED"
SELECTION_STATUS = "NOT_SELECTED"

FAIL_ACTIVE_ENTRY_MISSING = "MACHINE_PROCEED_FAIL_ACTIVE_ENTRY_MISSING"
FAIL_ACTIVE_ENTRY_MALFORMED = "MACHINE_PROCEED_FAIL_ACTIVE_ENTRY_MALFORMED"
FAIL_ACTIVE_ENTRY_NOT_ACTIVE = "MACHINE_PROCEED_FAIL_ACTIVE_ENTRY_NOT_ACTIVE"
FAIL_ACTIVE_ENTRY_SCOPE_MISMATCH = "MACHINE_PROCEED_FAIL_ACTIVE_ENTRY_SCOPE_MISMATCH"
FAIL_ACTIVE_ENTRY_RADIUS_NOT_AVAILABLE = "MACHINE_PROCEED_FAIL_ACTIVE_ENTRY_RADIUS_NOT_AVAILABLE"
FAIL_PROMOTION_RECEIPT_MISSING = "MACHINE_PROCEED_FAIL_PROMOTION_RECEIPT_MISSING"
FAIL_REUSE_AUTHORITY_NOT_GRANTED = "MACHINE_PROCEED_FAIL_REUSE_AUTHORITY_NOT_GRANTED"
FAIL_AUTHORITY_STATE_MISMATCH = "MACHINE_PROCEED_FAIL_AUTHORITY_STATE_MISMATCH"
FAIL_REQUESTED_ACTION_MISSING = "MACHINE_PROCEED_FAIL_REQUESTED_ACTION_MISSING"
FAIL_REQUESTED_ACTION_SCOPE_MISMATCH = "MACHINE_PROCEED_FAIL_REQUESTED_ACTION_SCOPE_MISMATCH"
FAIL_ROUTE_CLASSIFICATION_MISSING = "MACHINE_PROCEED_FAIL_ROUTE_CLASSIFICATION_MISSING"
FAIL_BASIS_SCOPE_MISMATCH = "MACHINE_PROCEED_FAIL_BASIS_SCOPE_MISMATCH"
FAIL_SOURCE_OBJECT_MISMATCH = "MACHINE_PROCEED_FAIL_SOURCE_OBJECT_MISMATCH"
FAIL_RADIUS_MISSING = "MACHINE_PROCEED_FAIL_RADIUS_MISSING"
FAIL_RADIUS_EXCEEDED = "MACHINE_PROCEED_FAIL_RADIUS_EXCEEDED"
FAIL_RADIUS_NOT_CONSUMED = "MACHINE_PROCEED_FAIL_RADIUS_NOT_CONSUMED"
FAIL_RADIUS_OVERCONSUMED = "MACHINE_PROCEED_FAIL_RADIUS_OVERCONSUMED"
FAIL_RADIUS_RENEWED = "MACHINE_PROCEED_FAIL_RADIUS_RENEWED"
FAIL_REQUIRED_VALIDATOR_MISSING = "MACHINE_PROCEED_FAIL_REQUIRED_VALIDATOR_MISSING"
FAIL_OUTPUT_ALREADY_EXISTS = "MACHINE_PROCEED_FAIL_OUTPUT_ALREADY_EXISTS"
FAIL_OUTPUT_SHAPE_INVALID = "MACHINE_PROCEED_FAIL_OUTPUT_SHAPE_INVALID"
FAIL_OUTPUT_MISSING = "MACHINE_PROCEED_FAIL_OUTPUT_MISSING"
FAIL_UNIT_EXECUTED = "MACHINE_PROCEED_FAIL_UNIT_EXECUTED"
FAIL_RUNTIME_EXECUTED = "MACHINE_PROCEED_FAIL_RUNTIME_EXECUTED"
FAIL_AUTHORITY_CHANGED = "MACHINE_PROCEED_FAIL_AUTHORITY_CHANGED"
FAIL_RECEIPT_REWRITTEN = "MACHINE_PROCEED_FAIL_RECEIPT_REWRITTEN"
FAIL_TAXONOMY_PROMOTED = "MACHINE_PROCEED_FAIL_TAXONOMY_PROMOTED"
FAIL_REUSE_SCOPE_EXPANDED = "MACHINE_PROCEED_FAIL_REUSE_SCOPE_EXPANDED"
FAIL_UPDATER_GENERALIZED = "MACHINE_PROCEED_FAIL_UPDATER_GENERALIZED"
FAIL_RUNNER_AUTHORITY_CREATED = "MACHINE_PROCEED_FAIL_RUNNER_AUTHORITY_CREATED"
FAIL_ADDITIONAL_RADIUS_CREATED = "MACHINE_PROCEED_FAIL_ADDITIONAL_RADIUS_CREATED"
FAIL_ACTIVE_ENTRY_REWRITTEN = "MACHINE_PROCEED_FAIL_ACTIVE_ENTRY_REWRITTEN"
FAIL_ACTIVE_ENTRY_MUTATED = "MACHINE_PROCEED_FAIL_ACTIVE_ENTRY_MUTATED"
FAIL_FORBIDDEN_EFFECT_DETECTED = "MACHINE_PROCEED_FAIL_FORBIDDEN_EFFECT_DETECTED"

FAILURE_VOCABULARY = [
    FAIL_ACTIVE_ENTRY_MISSING,
    FAIL_ACTIVE_ENTRY_MALFORMED,
    FAIL_ACTIVE_ENTRY_NOT_ACTIVE,
    FAIL_ACTIVE_ENTRY_SCOPE_MISMATCH,
    FAIL_ACTIVE_ENTRY_RADIUS_NOT_AVAILABLE,
    FAIL_PROMOTION_RECEIPT_MISSING,
    FAIL_REUSE_AUTHORITY_NOT_GRANTED,
    FAIL_AUTHORITY_STATE_MISMATCH,
    FAIL_REQUESTED_ACTION_MISSING,
    FAIL_REQUESTED_ACTION_SCOPE_MISMATCH,
    FAIL_ROUTE_CLASSIFICATION_MISSING,
    FAIL_BASIS_SCOPE_MISMATCH,
    FAIL_SOURCE_OBJECT_MISMATCH,
    FAIL_RADIUS_MISSING,
    FAIL_RADIUS_EXCEEDED,
    FAIL_RADIUS_NOT_CONSUMED,
    FAIL_RADIUS_OVERCONSUMED,
    FAIL_RADIUS_RENEWED,
    FAIL_REQUIRED_VALIDATOR_MISSING,
    FAIL_OUTPUT_ALREADY_EXISTS,
    FAIL_OUTPUT_SHAPE_INVALID,
    FAIL_OUTPUT_MISSING,
    FAIL_UNIT_EXECUTED,
    FAIL_RUNTIME_EXECUTED,
    FAIL_AUTHORITY_CHANGED,
    FAIL_RECEIPT_REWRITTEN,
    FAIL_TAXONOMY_PROMOTED,
    FAIL_REUSE_SCOPE_EXPANDED,
    FAIL_UPDATER_GENERALIZED,
    FAIL_RUNNER_AUTHORITY_CREATED,
    FAIL_ADDITIONAL_RADIUS_CREATED,
    FAIL_ACTIVE_ENTRY_REWRITTEN,
    FAIL_ACTIVE_ENTRY_MUTATED,
    FAIL_FORBIDDEN_EFFECT_DETECTED,
]

FORBIDDEN_ACTIONS = [
    "EXECUTE_UNIT",
    "RUN_UNIT",
    "RUN_RUNTIME",
    "APPLY_AUTHORITY_TRANSITION",
    "REWRITE_RECEIPTS",
    "PROMOTE_TAXONOMY",
    "EXPAND_REUSE_SCOPE",
    "GENERALIZE_UPDATER",
    "ACTIVATE_RUNNER",
]

FORBIDDEN_MARKDOWN_PHRASES = [
    "runner succeeded",
    "execution ready",
    "automation enabled",
    "unit completed",
    "runtime ran",
    "reuse expanded",
]


class GenerationError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(detail or code)
        self.code = code
        self.detail = detail


def fail(code: str, detail: str = "") -> None:
    raise GenerationError(code, detail)


def detect_repo_root(start: Path) -> Path:
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(FAIL_ACTIVE_ENTRY_MISSING, proc.stderr.strip())
    return Path(proc.stdout.strip()).resolve()


def run_git(root: Path, args: list[str], failure_code: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(failure_code, proc.stderr.strip() or proc.stdout.strip())
    return proc.stdout.strip()


def commit_for_paths(root: Path, paths: list[str], failure_code: str) -> str:
    existing = [path for path in paths if (root / path).exists()]
    if not existing:
        fail(failure_code, ",".join(paths))
    return run_git(root, ["log", "-n", "1", "--format=%H", "--", *existing], failure_code)


def verify_expected_commits(root: Path) -> None:
    expected = [
        (D3_COMMIT, [ACTIVE_ENTRY, "docs/matrixlabs/validator_archive/active/c8_n22_prepare_next_unit_definition_active_archive_entry_v0.md"], FAIL_ACTIVE_ENTRY_MISSING),
        (D2_COMMIT, [PROMOTION_RECEIPT, "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_receipt_v0.md"], FAIL_PROMOTION_RECEIPT_MISSING),
        (D1_COMMIT, [PROMOTION_SURFACE, "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_surface_v0.md"], FAIL_PROMOTION_RECEIPT_MISSING),
        (C3_COMMIT, [CANDIDATE_AUDIT, "docs/matrixlabs/validator_archive/audits/c8_n22_candidate_archive_entry_admissibility_audit_v0.md"], FAIL_PROMOTION_RECEIPT_MISSING),
        (C2_COMMIT, [CANDIDATE_ENTRY, "docs/matrixlabs/validator_archive/candidates/c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.md"], FAIL_PROMOTION_RECEIPT_MISSING),
        (C1_COMMIT, [SCHEMA_CONTRACT, "docs/matrixlabs/validator_archive/validator_archive_entry_schema_contract_v0.md"], FAIL_PROMOTION_RECEIPT_MISSING),
    ]
    for commit, paths, failure_code in expected:
        run_git(root, ["cat-file", "-e", f"{commit}^{{commit}}"], failure_code)
        got = commit_for_paths(root, paths, failure_code)
        if got != commit:
            fail(failure_code, f"{paths[0]} commit mismatch: {got}!={commit}")


def load_json(root: Path, rel: str, missing_code: str, malformed_code: str | None = None) -> dict[str, Any]:
    try:
        return json.loads((root / rel).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        fail(missing_code, rel)
        raise exc
    except json.JSONDecodeError as exc:
        fail(malformed_code or missing_code, f"{rel}: {exc}")
        raise exc


def expect(value: object, wanted: object, failure_code: str, field: str) -> None:
    if value != wanted:
        fail(failure_code, f"{field}: {value!r}!={wanted!r}")


def bool_text(value: bool) -> str:
    return str(value).lower()


def json_text(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def validate_active_entry(active: dict[str, Any]) -> None:
    expect(active.get("schema_version"), ACTIVE_SCHEMA, FAIL_ACTIVE_ENTRY_MALFORMED, "schema_version")
    expect(active.get("materialization_id"), ACTIVE_MATERIALIZATION_ID, FAIL_ACTIVE_ENTRY_MALFORMED, "materialization_id")
    expect(active.get("active_archive_entry_id"), ACTIVE_ENTRY_ID, FAIL_ACTIVE_ENTRY_MALFORMED, "active_archive_entry_id")
    expect(active.get("materialization_status"), ACTIVE_MATERIALIZATION_STATUS, FAIL_ACTIVE_ENTRY_NOT_ACTIVE, "materialization_status")
    expect(active.get("terminal_transition"), "ADVANCE(D4_MACHINE_PROCEED_UNDER_ACTIVE_ENTRY_PENDING)", FAIL_ACTIVE_ENTRY_NOT_ACTIVE, "terminal_transition")

    state = active.get("materialized_archive_entry_state", {})
    expect(state.get("archive_entry_status"), ACTIVE_ENTRY_STATUS, FAIL_ACTIVE_ENTRY_NOT_ACTIVE, "archive_entry_status")
    expect(state.get("promotion_status"), PROMOTION_STATUS, FAIL_ACTIVE_ENTRY_NOT_ACTIVE, "promotion_status")
    expect(state.get("reuse_authority_status"), REUSE_AUTHORITY_STATUS, FAIL_REUSE_AUTHORITY_NOT_GRANTED, "reuse_authority_status")
    expect(state.get("activation_status"), ACTIVATION_STATUS, FAIL_ACTIVE_ENTRY_NOT_ACTIVE, "activation_status")
    expect(state.get("reuse_authority_scope"), DECLARED_SCOPE, FAIL_ACTIVE_ENTRY_SCOPE_MISMATCH, "reuse_authority_scope")
    expect(state.get("activation_scope"), DECLARED_SCOPE, FAIL_ACTIVE_ENTRY_SCOPE_MISMATCH, "activation_scope")
    expect(state.get("machine_action_scope"), ACTION_SCOPE, FAIL_ACTIVE_ENTRY_SCOPE_MISMATCH, "machine_action_scope")

    scope = active.get("materialized_scope", {})
    for key, wanted in {
        "allowed_current_authority_state": AUTHORITY_STATE,
        "allowed_requested_action": ACTION,
        "allowed_requested_action_scope": ACTION_SCOPE,
        "allowed_basis_scope": BASIS_SCOPE,
        "allowed_source_object_id": SOURCE_OBJECT_ID,
        "allowed_output_kind": OUTPUT_KIND,
        "radius": RADIUS_LIMIT,
    }.items():
        failure = FAIL_AUTHORITY_STATE_MISMATCH if key == "allowed_current_authority_state" else FAIL_ACTIVE_ENTRY_SCOPE_MISMATCH
        expect(scope.get(key), wanted, failure, f"materialized_scope.{key}")

    radius = active.get("radius_state", {})
    if "radius_remaining_after_d3" not in radius:
        fail(FAIL_RADIUS_MISSING, "radius_remaining_after_d3")
    expect(radius.get("radius_remaining_after_d3"), 1, FAIL_RADIUS_EXCEEDED, "radius_remaining_after_d3")
    expect(radius.get("radius_available_for_d4"), True, FAIL_ACTIVE_ENTRY_RADIUS_NOT_AVAILABLE, "radius_available_for_d4")
    expect(radius.get("radius_consumed_by_this_materialization"), False, FAIL_ACTIVE_ENTRY_RADIUS_NOT_AVAILABLE, "radius_consumed_by_this_materialization")

    d4 = active.get("d4_eligibility_after_d3", {})
    expect(d4.get("active_archive_entry_exists"), True, FAIL_ACTIVE_ENTRY_NOT_ACTIVE, "d4.active_archive_entry_exists")
    expect(d4.get("radius_available"), True, FAIL_ACTIVE_ENTRY_RADIUS_NOT_AVAILABLE, "d4.radius_available")
    expect(d4.get("radius_remaining"), 1, FAIL_RADIUS_EXCEEDED, "d4.radius_remaining")
    expect(d4.get("allowed_d4_action"), ACTION, FAIL_ACTIVE_ENTRY_SCOPE_MISMATCH, "d4.allowed_d4_action")
    expect(d4.get("allowed_d4_action_scope"), ACTION_SCOPE, FAIL_ACTIVE_ENTRY_SCOPE_MISMATCH, "d4.allowed_d4_action_scope")
    expect(d4.get("allowed_d4_basis_scope"), BASIS_SCOPE, FAIL_BASIS_SCOPE_MISMATCH, "d4.allowed_d4_basis_scope")
    expect(d4.get("allowed_d4_source_object_id"), SOURCE_OBJECT_ID, FAIL_SOURCE_OBJECT_MISMATCH, "d4.allowed_d4_source_object_id")
    expect(d4.get("machine_proceed_performed_by_d3"), False, FAIL_FORBIDDEN_EFFECT_DETECTED, "d4.machine_proceed_performed_by_d3")

    effects = active.get("materialization_effects", {})
    for field, failure in {
        "machine_proceed_performed_by_this_materialization": FAIL_FORBIDDEN_EFFECT_DETECTED,
        "next_unit_definition_surface_prepared_by_this_materialization": FAIL_FORBIDDEN_EFFECT_DETECTED,
        "runner_authority_created_by_this_materialization": FAIL_RUNNER_AUTHORITY_CREATED,
        "observed_path_updated_by_this_materialization": FAIL_FORBIDDEN_EFFECT_DETECTED,
        "scope_expanded_by_this_materialization": FAIL_REUSE_SCOPE_EXPANDED,
        "radius_consumed_by_this_materialization": FAIL_ACTIVE_ENTRY_RADIUS_NOT_AVAILABLE,
    }.items():
        expect(effects.get(field), False, failure, f"materialization_effects.{field}")


def validate_provenance(sources: dict[str, dict[str, Any]]) -> None:
    d2 = sources["promotion_receipt"]
    expect(d2.get("promotion_decision_receipt_id"), RECEIPT_ID, FAIL_PROMOTION_RECEIPT_MISSING, "promotion_decision_receipt_id")
    expect(d2.get("promotion_decision_receipt_gate"), RECEIPT_GATE, FAIL_PROMOTION_RECEIPT_MISSING, "promotion_decision_receipt_gate")

    d1 = sources["promotion_surface"]
    expect(d1.get("promotion_decision_surface_id"), SURFACE_ID, FAIL_PROMOTION_RECEIPT_MISSING, "promotion_decision_surface_id")

    c2 = sources["candidate_entry"]
    expect(c2.get("archive_entry_id"), CANDIDATE_ID, FAIL_PROMOTION_RECEIPT_MISSING, "candidate.archive_entry_id")

    c3 = sources["candidate_audit"]
    expect(c3.get("audit_id"), AUDIT_ID, FAIL_PROMOTION_RECEIPT_MISSING, "candidate_audit.audit_id")
    expect(
        c3.get("audit_result", {}).get("candidate_audit_status"),
        AUDIT_STATUS,
        FAIL_PROMOTION_RECEIPT_MISSING,
        "candidate_audit.audit_result.candidate_audit_status",
    )

    c1 = sources["schema_contract"]
    expect(c1.get("archive_schema_contract_id"), CONTRACT_ID, FAIL_PROMOTION_RECEIPT_MISSING, "archive_schema_contract_id")

    b1 = sources["requested_action_record"]
    movement = b1.get("requested_movement", {})
    expect(b1.get("requested_action_record_id"), REQUESTED_ACTION_RECORD_ID, FAIL_REQUESTED_ACTION_MISSING, "requested_action_record_id")
    expect(movement.get("requested_action"), ACTION, FAIL_REQUESTED_ACTION_SCOPE_MISMATCH, "b1.requested_action")
    expect(movement.get("requested_action_scope"), ACTION_SCOPE, FAIL_REQUESTED_ACTION_SCOPE_MISMATCH, "b1.requested_action_scope")
    expect(movement.get("basis_scope"), BASIS_SCOPE, FAIL_BASIS_SCOPE_MISMATCH, "b1.basis_scope")
    expect(movement.get("requested_target_basis"), SOURCE_OBJECT_ID, FAIL_SOURCE_OBJECT_MISMATCH, "b1.requested_target_basis")
    expect(movement.get("requested_output_kind"), OUTPUT_KIND, FAIL_REQUESTED_ACTION_SCOPE_MISMATCH, "b1.requested_output_kind")

    b2 = sources["route_classification"]
    classification = b2.get("classification", {})
    requested = b2.get("requested_action", {})
    expect(b2.get("route_classification_id"), ROUTE_CLASSIFICATION_ID, FAIL_ROUTE_CLASSIFICATION_MISSING, "route_classification_id")
    expect(classification.get("allowed_machine_action_scope"), ACTION_SCOPE, FAIL_REQUESTED_ACTION_SCOPE_MISMATCH, "b2.allowed_machine_action_scope")
    expect(classification.get("allowed_scope"), BASIS_SCOPE, FAIL_BASIS_SCOPE_MISMATCH, "b2.allowed_scope")
    expect(requested.get("requested_action"), ACTION, FAIL_REQUESTED_ACTION_SCOPE_MISMATCH, "b2.requested_action")
    expect(requested.get("requested_target_basis"), SOURCE_OBJECT_ID, FAIL_SOURCE_OBJECT_MISMATCH, "b2.requested_target_basis")


def source_chain() -> dict[str, Any]:
    return {
        "active_archive_entry_materialization_id": ACTIVE_MATERIALIZATION_ID,
        "active_archive_entry_id": ACTIVE_ENTRY_ID,
        "active_archive_entry_materialization_status": ACTIVE_MATERIALIZATION_STATUS,
        "promotion_decision_receipt_id": RECEIPT_ID,
        "promotion_decision_receipt_gate": RECEIPT_GATE,
        "promotion_decision_surface_id": SURFACE_ID,
        "candidate_entry_id": CANDIDATE_ID,
        "candidate_audit_id": AUDIT_ID,
        "candidate_audit_status": AUDIT_STATUS,
        "archive_schema_contract_id": CONTRACT_ID,
        "requested_action_record_id": REQUESTED_ACTION_RECORD_ID,
        "route_classification_id": ROUTE_CLASSIFICATION_ID,
        "source_chain_complete": True,
    }


def active_archive_entry_section() -> dict[str, str]:
    return {
        "active_archive_entry_id": ACTIVE_ENTRY_ID,
        "entry_status": ACTIVE_ENTRY_STATUS,
        "promotion_status": PROMOTION_STATUS,
        "reuse_authority_status": REUSE_AUTHORITY_STATUS,
        "activation_status": ACTIVATION_STATUS,
        "reuse_authority_scope": DECLARED_SCOPE,
        "activation_scope": DECLARED_SCOPE,
        "machine_action_scope": ACTION_SCOPE,
    }


def requested_action_section() -> dict[str, str]:
    return {
        "requested_action_record_id": REQUESTED_ACTION_RECORD_ID,
        "requested_action": ACTION,
        "requested_action_scope": ACTION_SCOPE,
        "requested_basis_scope": BASIS_SCOPE,
        "requested_source_object_id": SOURCE_OBJECT_ID,
        "requested_output_kind": OUTPUT_KIND,
    }


def performed_action_section() -> dict[str, str]:
    return {
        "performed_action": ACTION,
        "performed_action_scope": ACTION_SCOPE,
        "performed_basis_scope": BASIS_SCOPE,
        "performed_source_object_id": SOURCE_OBJECT_ID,
        "performed_output_kind": OUTPUT_KIND,
    }


def radius_source_section() -> dict[str, Any]:
    return {
        "source_materialization_id": ACTIVE_MATERIALIZATION_ID,
        "source_active_archive_entry_id": ACTIVE_ENTRY_ID,
        "radius_remaining_after_d3": 1,
        "radius_available_before_d4": True,
    }


def radius_section() -> dict[str, Any]:
    return {
        "radius_limit": RADIUS_LIMIT,
        "radius_before": 1,
        "radius_consumed": 1,
        "radius_after": 0,
        "radius_exhausted": True,
        "radius_renewed_by_this_proceed": False,
        "additional_radius_created": False,
    }


def created_output_section() -> dict[str, str]:
    return {
        "output_object_id": OUTPUT_OBJECT_ID,
        "output_object_type": OUTPUT_KIND,
        "output_scope": OUTPUT_SCOPE,
        "output_basis": SOURCE_OBJECT_ID,
        "output_execution_status": OUTPUT_EXECUTION_STATUS,
        "output_path_json": SURFACE_JSON,
        "output_path_md": SURFACE_MD,
    }


def non_effects_section() -> dict[str, bool]:
    return {
        "unit_executed": False,
        "runtime_executed": False,
        "authority_changed": False,
        "human_decision_consumed": False,
        "receipts_rewritten": False,
        "taxonomy_promoted": False,
        "reuse_scope_expanded": False,
        "updater_generalized": False,
        "runner_authority_created": False,
        "additional_radius_created": False,
        "radius_renewed": False,
        "active_archive_entry_rewritten": False,
        "active_archive_entry_mutated": False,
    }


def validators_section() -> dict[str, str]:
    return {
        "active_archive_entry_validator": "PASS",
        "authority_state_match_validator": "PASS",
        "requested_action_scope_validator": "PASS",
        "basis_scope_validator": "PASS",
        "source_object_validator": "PASS",
        "radius_validator": "PASS",
        "forbidden_effects_validator": "PASS",
        "output_shape_validator": "PASS",
    }


def proceed_gate() -> dict[str, Any]:
    gate: dict[str, Any] = {
        "machine_proceed_gate": PROCEED_STATUS,
        "active_archive_entry_present": True,
        "active_archive_entry_status": ACTIVE_ENTRY_STATUS,
        "promotion_status": PROMOTION_STATUS,
        "reuse_authority_status": REUSE_AUTHORITY_STATUS,
        "activation_status": ACTIVATION_STATUS,
        "current_authority_state": AUTHORITY_STATE,
        "requested_action": ACTION,
        "requested_action_scope": ACTION_SCOPE,
        "performed_action": ACTION,
        "performed_action_scope": ACTION_SCOPE,
        "basis_scope": BASIS_SCOPE,
        "source_object_id": SOURCE_OBJECT_ID,
        "output_object_type": OUTPUT_KIND,
        "output_scope": OUTPUT_SCOPE,
        "radius_limit": RADIUS_LIMIT,
        "radius_before": 1,
        "radius_consumed": 1,
        "radius_after": 0,
        "radius_exhausted": True,
        "radius_renewed_by_this_proceed": False,
        "output_surface_created": True,
        "forbidden_effect_detected": False,
        "failures": [],
    }
    gate.update(validators_section())
    gate.update(non_effects_section())
    return gate


def build_proceed_record() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "machine_proceed_id": MACHINE_PROCEED_ID,
        "proceed_role": PROCEED_ROLE,
        "proceed_status": PROCEED_STATUS,
        "block_id": BLOCK_ID,
        "block_unit_id": BLOCK_UNIT_ID,
        "source_chain": source_chain(),
        "active_archive_entry": active_archive_entry_section(),
        "requested_action": requested_action_section(),
        "performed_action": performed_action_section(),
        "radius_source": radius_source_section(),
        "radius": radius_section(),
        "created_output": created_output_section(),
        "non_effects": non_effects_section(),
        "validators": validators_section(),
        "proceed_gate": proceed_gate(),
        "failure_vocabulary": FAILURE_VOCABULARY,
        "forbidden_actions": FORBIDDEN_ACTIONS,
        "non_claims": [
            "D.4 does not execute the next bounded unit.",
            "D.4 does not run runtime.",
            "D.4 does not apply an authority transition.",
            "D.4 does not consume a human decision.",
            "D.4 does not rewrite receipts.",
            "D.4 does not rewrite the active archive entry.",
            "D.4 does not mutate the active archive entry.",
            "D.4 does not promote taxonomy.",
            "D.4 does not expand reuse scope.",
            "D.4 does not generalize the updater.",
            "D.4 does not activate a runner.",
            "D.4 does not create additional radius.",
            "D.4 does not renew radius.",
            "D.4 does not make the active archive entry reusable beyond its declared scope.",
            "D.4 only performs one radius-bound preparation action under one active archive entry.",
        ],
        "key_non_claims": [
            "machine proceed ≠ runner",
            "prepare surface ≠ execute unit",
            "radius consumed ≠ radius renewed",
            "one scoped action != generalized automation",
            "one lawful action ≠ generalized automation",
        ],
        "precommit_c8_n22_machine_proceed_gate": PRECOMMIT_GATE,
        "machine_proceed_gate": PROCEED_STATUS,
        "terminal_transition": TERMINAL_TRANSITION,
        "generated_by": GENERATOR,
    }


def build_surface_record() -> dict[str, Any]:
    return {
        "schema_version": UNIT_SURFACE_SCHEMA,
        "unit_surface_id": UNIT_SURFACE_ID,
        "surface_role": UNIT_SURFACE_ROLE,
        "surface_status": UNIT_SURFACE_STATUS,
        "created_by_machine_proceed_id": MACHINE_PROCEED_ID,
        "created_under_active_archive_entry": ACTIVE_ENTRY_ID,
        "basis": {
            "basis_object_id": SOURCE_OBJECT_ID,
            "basis_scope": BASIS_SCOPE,
            "basis_authority_state": AUTHORITY_STATE,
        },
        "proposed_next_unit": {
            "unit_id": PLACEHOLDER_UNIT_ID,
            "unit_kind": PLACEHOLDER_KIND,
            "unit_status": PLACEHOLDER_STATUS,
            "execution_status": OUTPUT_EXECUTION_STATUS,
            "selection_status": SELECTION_STATUS,
            "requires_later_human_decision": True,
        },
        "required_before_execution": {
            "human_decision_surface_required": True,
            "execution_authority_required": True,
            "execution_receipt_required": True,
            "active_execution_archive_entry_required": True,
        },
        "non_authorizations": {
            "execution_authorized": False,
            "runtime_authorized": False,
            "authority_transition_authorized": False,
            "reuse_scope_expanded": False,
            "runner_authority_created": False,
        },
        "surface_gate": {
            "surface_created": True,
            "surface_only": True,
            "not_executed": True,
            "placeholder_not_selected": True,
            "requires_later_human_decision": True,
            "failures": [],
        },
        "generated_by": GENERATOR,
    }


def render_proceed_markdown(record: dict[str, Any]) -> str:
    radius = record["radius"]
    validators = record["validators"]
    non_effects = record["non_effects"]
    return f"""# C8 n22 machine proceed v0

## Status

{record['proceed_status']}

## Active archive entry

{ACTIVE_ENTRY_ID}

## Performed action

{ACTION}

## Performed scope

{ACTION_SCOPE}

## Basis

c8.n22 only

## Output

{OUTPUT_OBJECT_ID}

## Radius

- before: {radius['radius_before']}
- consumed: {radius['radius_consumed']}
- after: {radius['radius_after']}
- renewed by this proceed: {bool_text(radius['radius_renewed_by_this_proceed'])}

## Validators

- active archive entry validator: {validators['active_archive_entry_validator']}
- authority state match validator: {validators['authority_state_match_validator']}
- requested action scope validator: {validators['requested_action_scope_validator']}
- basis scope validator: {validators['basis_scope_validator']}
- source object validator: {validators['source_object_validator']}
- radius validator: {validators['radius_validator']}
- forbidden effects validator: {validators['forbidden_effects_validator']}
- output shape validator: {validators['output_shape_validator']}

## Confirmed non-effects

- unit not executed
- runtime not executed
- authority not changed
- receipts not rewritten
- taxonomy not promoted
- reuse scope not expanded
- updater not generalized
- runner authority not created
- additional radius not created
- active archive entry not rewritten
- active archive entry not mutated

## Non-claim

This machine proceed prepares a definition surface only. It does not execute the next unit.
"""


def render_surface_markdown(surface: dict[str, Any]) -> str:
    return f"""# C8 n22 next bounded unit definition surface v0

## Status

{surface['surface_status']}

## Created by

{MACHINE_PROCEED_ID}

## Created under active archive entry

{ACTIVE_ENTRY_ID}

## Basis

- object: {SOURCE_OBJECT_ID}
- scope: {BASIS_SCOPE}
- authority state: {AUTHORITY_STATE}

## Proposed next unit placeholder

- unit id: {PLACEHOLDER_UNIT_ID}
- kind: {PLACEHOLDER_KIND}
- status: {PLACEHOLDER_STATUS}
- execution: {OUTPUT_EXECUTION_STATUS}
- selection: {SELECTION_STATUS}

## Required before execution

- human decision surface required
- execution authority required
- execution receipt required
- active execution archive entry required

## Non-authorizations

- execution not authorized
- runtime not authorized
- authority transition not authorized
- reuse scope not expanded
- runner authority not created
"""


def validate_record(record: dict[str, Any], surface: dict[str, Any]) -> None:
    expect(record.get("schema_version"), SCHEMA_VERSION, FAIL_OUTPUT_SHAPE_INVALID, "schema_version")
    expect(record.get("machine_proceed_id"), MACHINE_PROCEED_ID, FAIL_OUTPUT_SHAPE_INVALID, "machine_proceed_id")
    expect(record.get("proceed_status"), PROCEED_STATUS, FAIL_OUTPUT_SHAPE_INVALID, "proceed_status")
    expect(record.get("terminal_transition"), TERMINAL_TRANSITION, FAIL_OUTPUT_SHAPE_INVALID, "terminal_transition")
    expect(record.get("precommit_c8_n22_machine_proceed_gate"), PRECOMMIT_GATE, FAIL_OUTPUT_SHAPE_INVALID, "precommit")

    radius = record.get("radius", {})
    expect(radius.get("radius_before"), 1, FAIL_RADIUS_EXCEEDED, "radius_before")
    expect(radius.get("radius_consumed"), 1, FAIL_RADIUS_NOT_CONSUMED, "radius_consumed")
    expect(radius.get("radius_after"), 0, FAIL_RADIUS_NOT_CONSUMED, "radius_after")
    expect(radius.get("radius_exhausted"), True, FAIL_RADIUS_NOT_CONSUMED, "radius_exhausted")
    expect(radius.get("radius_renewed_by_this_proceed"), False, FAIL_RADIUS_RENEWED, "radius_renewed_by_this_proceed")
    expect(radius.get("additional_radius_created"), False, FAIL_ADDITIONAL_RADIUS_CREATED, "additional_radius_created")

    for key, value in record.get("validators", {}).items():
        expect(value, "PASS", FAIL_REQUIRED_VALIDATOR_MISSING, f"validators.{key}")
    if set(record.get("validators", {})) != set(validators_section()):
        fail(FAIL_REQUIRED_VALIDATOR_MISSING, "validator key set mismatch")

    for key, value in record.get("non_effects", {}).items():
        if value is not False:
            fail(FAIL_FORBIDDEN_EFFECT_DETECTED, f"non_effects.{key}: {value!r}")

    gate = record.get("proceed_gate", {})
    expect(gate.get("machine_proceed_gate"), PROCEED_STATUS, FAIL_OUTPUT_SHAPE_INVALID, "proceed_gate.machine_proceed_gate")
    expect(gate.get("radius_before"), 1, FAIL_RADIUS_EXCEEDED, "proceed_gate.radius_before")
    expect(gate.get("radius_consumed"), 1, FAIL_RADIUS_NOT_CONSUMED, "proceed_gate.radius_consumed")
    expect(gate.get("radius_after"), 0, FAIL_RADIUS_NOT_CONSUMED, "proceed_gate.radius_after")
    expect(gate.get("radius_renewed_by_this_proceed"), False, FAIL_RADIUS_RENEWED, "proceed_gate.radius_renewed_by_this_proceed")
    expect(gate.get("forbidden_effect_detected"), False, FAIL_FORBIDDEN_EFFECT_DETECTED, "proceed_gate.forbidden_effect_detected")
    expect(gate.get("failures"), [], FAIL_FORBIDDEN_EFFECT_DETECTED, "proceed_gate.failures")

    expect(surface.get("schema_version"), UNIT_SURFACE_SCHEMA, FAIL_OUTPUT_SHAPE_INVALID, "surface.schema_version")
    expect(surface.get("unit_surface_id"), UNIT_SURFACE_ID, FAIL_OUTPUT_SHAPE_INVALID, "surface.unit_surface_id")
    expect(surface.get("surface_status"), UNIT_SURFACE_STATUS, FAIL_OUTPUT_SHAPE_INVALID, "surface.surface_status")
    expect(surface.get("created_by_machine_proceed_id"), MACHINE_PROCEED_ID, FAIL_OUTPUT_SHAPE_INVALID, "surface.created_by_machine_proceed_id")
    expect(surface.get("created_under_active_archive_entry"), ACTIVE_ENTRY_ID, FAIL_OUTPUT_SHAPE_INVALID, "surface.created_under_active_archive_entry")
    expect(surface.get("proposed_next_unit", {}).get("execution_status"), OUTPUT_EXECUTION_STATUS, FAIL_UNIT_EXECUTED, "surface.execution_status")
    expect(surface.get("proposed_next_unit", {}).get("selection_status"), SELECTION_STATUS, FAIL_OUTPUT_SHAPE_INVALID, "surface.selection_status")
    for key, value in surface.get("non_authorizations", {}).items():
        if value is not False:
            fail(FAIL_FORBIDDEN_EFFECT_DETECTED, f"surface.non_authorizations.{key}: {value!r}")


def validate_markdown(*texts: str) -> None:
    for text in texts:
        lowered = text.lower()
        for phrase in FORBIDDEN_MARKDOWN_PHRASES:
            if phrase in lowered:
                fail(FAIL_FORBIDDEN_EFFECT_DETECTED, phrase)


def guard_output(root: Path, rel: str, content: str) -> None:
    path = root / rel
    if path.exists() and path.read_text(encoding="utf-8") != content:
        fail(FAIL_OUTPUT_ALREADY_EXISTS, rel)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_outputs(root: Path, record: dict[str, Any], surface: dict[str, Any]) -> None:
    proceed_json = json_text(record)
    surface_json = json_text(surface)
    proceed_md = render_proceed_markdown(record)
    surface_md = render_surface_markdown(surface)

    validate_markdown(proceed_md, surface_md)
    for rel, content in {
        PROCEED_JSON: proceed_json,
        PROCEED_MD: proceed_md,
        SURFACE_JSON: surface_json,
        SURFACE_MD: surface_md,
    }.items():
        guard_output(root, rel, content)

    write_text(root / PROCEED_JSON, proceed_json)
    write_text(root / PROCEED_MD, proceed_md)
    write_text(root / SURFACE_JSON, surface_json)
    write_text(root / SURFACE_MD, surface_md)


def print_success(record: dict[str, Any], surface: dict[str, Any]) -> None:
    active = record["active_archive_entry"]
    requested = record["requested_action"]
    performed = record["performed_action"]
    radius_source = record["radius_source"]
    radius = record["radius"]
    output = record["created_output"]
    non_effects = record["non_effects"]
    validators = record["validators"]
    non_auth = surface["non_authorizations"]
    proposed = surface["proposed_next_unit"]

    print("BUILD_C8_N22_PREPARE_NEXT_UNIT_DEFINITION_SURFACE_MACHINE_PROCEED_V0_COMPLETE")
    print(f"machine_proceed_id={record['machine_proceed_id']}")
    print(f"schema_version={record['schema_version']}")
    print(f"proceed_role={record['proceed_role']}")
    print(f"proceed_status={record['proceed_status']}")
    print(f"block_id={record['block_id']}")
    print(f"block_unit_id={record['block_unit_id']}")
    print(f"active_archive_entry_id={active['active_archive_entry_id']}")
    print(f"active_archive_entry_status={active['entry_status']}")
    print(f"promotion_status={active['promotion_status']}")
    print(f"reuse_authority_status={active['reuse_authority_status']}")
    print(f"activation_status={active['activation_status']}")
    print(f"reuse_authority_scope={active['reuse_authority_scope']}")
    print(f"activation_scope={active['activation_scope']}")
    print(f"machine_action_scope={active['machine_action_scope']}")
    print(f"requested_action={requested['requested_action']}")
    print(f"requested_action_scope={requested['requested_action_scope']}")
    print(f"performed_action={performed['performed_action']}")
    print(f"performed_action_scope={performed['performed_action_scope']}")
    print(f"performed_basis_scope={performed['performed_basis_scope']}")
    print(f"performed_source_object_id={performed['performed_source_object_id']}")
    print(f"performed_output_kind={performed['performed_output_kind']}")
    print(f"radius_limit={radius['radius_limit']}")
    print(f"radius_remaining_after_d3={radius_source['radius_remaining_after_d3']}")
    print(f"radius_before={radius['radius_before']}")
    print(f"radius_consumed={radius['radius_consumed']}")
    print(f"radius_after={radius['radius_after']}")
    print(f"radius_exhausted={bool_text(radius['radius_exhausted'])}")
    print(f"radius_renewed_by_this_proceed={bool_text(radius['radius_renewed_by_this_proceed'])}")
    print(f"additional_radius_created={bool_text(radius['additional_radius_created'])}")
    print("output_surface_created=true")
    print(f"output_object_id={output['output_object_id']}")
    print(f"output_object_type={output['output_object_type']}")
    print(f"output_scope={output['output_scope']}")
    print(f"output_execution_status={output['output_execution_status']}")
    print(f"unit_surface_id={surface['unit_surface_id']}")
    print(f"unit_surface_status={surface['surface_status']}")
    print(f"proposed_next_unit_id={proposed['unit_id']}")
    print(f"proposed_next_unit_status={proposed['unit_status']}")
    print(f"proposed_next_unit_execution_status={proposed['execution_status']}")
    for key in [
        "unit_executed",
        "runtime_executed",
        "authority_changed",
        "human_decision_consumed",
        "receipts_rewritten",
        "taxonomy_promoted",
        "reuse_scope_expanded",
        "updater_generalized",
        "runner_authority_created",
        "active_archive_entry_rewritten",
        "active_archive_entry_mutated",
    ]:
        print(f"{key}={bool_text(non_effects[key])}")
    print(f"execution_authorized={bool_text(non_auth['execution_authorized'])}")
    print(f"runtime_authorized={bool_text(non_auth['runtime_authorized'])}")
    print(f"authority_transition_authorized={bool_text(non_auth['authority_transition_authorized'])}")
    for key in [
        "active_archive_entry_validator",
        "authority_state_match_validator",
        "requested_action_scope_validator",
        "basis_scope_validator",
        "source_object_validator",
        "radius_validator",
        "forbidden_effects_validator",
        "output_shape_validator",
    ]:
        print(f"{key}={validators[key]}")
    print(f"machine_proceed_gate={record['machine_proceed_gate']}")
    print(f"precommit_c8_n22_machine_proceed_gate={record['precommit_c8_n22_machine_proceed_gate']}")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition={record['terminal_transition']}")


def main() -> int:
    try:
        root = detect_repo_root(Path.cwd())
        verify_expected_commits(root)
        sources = {
            "active_entry": load_json(root, ACTIVE_ENTRY, FAIL_ACTIVE_ENTRY_MISSING, FAIL_ACTIVE_ENTRY_MALFORMED),
            "promotion_receipt": load_json(root, PROMOTION_RECEIPT, FAIL_PROMOTION_RECEIPT_MISSING),
            "promotion_surface": load_json(root, PROMOTION_SURFACE, FAIL_PROMOTION_RECEIPT_MISSING),
            "candidate_entry": load_json(root, CANDIDATE_ENTRY, FAIL_PROMOTION_RECEIPT_MISSING),
            "candidate_audit": load_json(root, CANDIDATE_AUDIT, FAIL_PROMOTION_RECEIPT_MISSING),
            "schema_contract": load_json(root, SCHEMA_CONTRACT, FAIL_PROMOTION_RECEIPT_MISSING),
            "requested_action_record": load_json(root, REQUESTED_ACTION_RECORD, FAIL_REQUESTED_ACTION_MISSING),
            "route_classification": load_json(root, ROUTE_CLASSIFICATION, FAIL_ROUTE_CLASSIFICATION_MISSING),
        }
        validate_active_entry(sources["active_entry"])
        validate_provenance(sources)
        record = build_proceed_record()
        surface = build_surface_record()
        validate_record(record, surface)
        write_outputs(root, record, surface)
    except GenerationError as exc:
        print(f"STOP_{exc.code}")
        if exc.detail:
            print(exc.detail, file=sys.stderr)
        return 2

    print_success(record, surface)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
