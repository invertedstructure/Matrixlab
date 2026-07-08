#!/usr/bin/env python3
"""Build C8 n22 machine proceed closure v0.

D.5 closes the Block D machine-proceed specimen. It verifies the committed
D.4 receipt and output surface, records radius exhaustion, and does not
perform another machine action or create the next decision surface.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_machine_proceed_closure_v0.py"
OUTPUT_JSON = "docs/matrixlabs/proceed/c8_n22_machine_proceed_closure_v0.json"
OUTPUT_MD = "docs/matrixlabs/proceed/c8_n22_machine_proceed_closure_v0.md"

ACTIVE_ENTRY_JSON = "docs/matrixlabs/validator_archive/active/c8_n22_prepare_next_unit_definition_active_archive_entry_v0.json"
D4_PROCEED_JSON = "docs/matrixlabs/proceed/c8_n22_prepare_next_unit_definition_surface_machine_proceed_v0.json"
D4_PROCEED_MD = "docs/matrixlabs/proceed/c8_n22_prepare_next_unit_definition_surface_machine_proceed_v0.md"
D4_SURFACE_JSON = "docs/matrixlabs/unit_surfaces/c8_n22_next_bounded_unit_definition_surface_v0.json"
D4_SURFACE_MD = "docs/matrixlabs/unit_surfaces/c8_n22_next_bounded_unit_definition_surface_v0.md"
PROMOTION_RECEIPT = "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_receipt_v0.json"
PROMOTION_SURFACE = "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_surface_v0.json"
CANDIDATE_ENTRY = "docs/matrixlabs/validator_archive/candidates/c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.json"
CANDIDATE_AUDIT = "docs/matrixlabs/validator_archive/audits/c8_n22_candidate_archive_entry_admissibility_audit_v0.json"
SCHEMA_CONTRACT = "docs/matrixlabs/validator_archive/validator_archive_entry_schema_contract_v0.json"

D4_COMMIT = "c3c926f51898b64c8b431ff026973736e8073ec8"
D3_COMMIT = "d4eda408759be982c2d9dff2622a54b9dd7b7ac0"
D2_COMMIT = "41233ed53084b9ceb2348661d07342feaf65cac7"
D1_COMMIT = "a457bf08eb263cdbdad01a4eef6b7e7e2b11f230"
C3_COMMIT = "f49dfab97774414330682151e6e3fffeb7ba6f66"
C2_COMMIT = "674c601136f381c9d85605f646900998b24ddfe9"
C1_COMMIT = "96223d2a9827543c27f93a1c0a16a6670a97de71"

SCHEMA_VERSION = "matrixlabs_machine_proceed_closure_v0"
CLOSURE_ID = "c8.n22.machine_proceed_closure.v0"
CLOSURE_ROLE = "BLOCK_D_MACHINE_PROCEED_CLOSURE"
CLOSURE_STATUS = "MACHINE_PROCEED_CLOSURE_PASS_RADIUS_EXHAUSTED_STOP"
BLOCK_ID = "BLOCK_D"
BLOCK_STATUS = "BLOCK_D_PASS_ONE_RADIUS_BOUND_MACHINE_PREPARE_MOVE"
PRECOMMIT_GATE = "PASS"
TERMINAL_TRANSITION = "STOP_BLOCK_D_MACHINE_PROCEED_CLOSED"

AUDIT_ID = "c8.n22.candidate_archive_entry.admissibility_audit.v0"
AUDIT_STATUS = "CANDIDATE_AUDIT_PASS_CONTRACT_CONFORMANT_NOT_PROMOTED"
SURFACE_ID = "c8.n22.candidate_promotion_decision_surface.v0"
RECEIPT_ID = "c8.n22.candidate_promotion_decision_receipt.v0"
SELECTED_OPTION = "DECISION_PROMOTE_CANDIDATE_FOR_DECLARED_SCOPE"
ACTIVE_ENTRY_ID = "active.c8.n22.prepare_next_unit_definition_surface.v0"
ACTIVE_ENTRY_STATUS = "ARCHIVE_STATUS_PREAPPROVED_ACTIVE"
MACHINE_PROCEED_ID = "c8.n22.prepare_next_unit_definition_surface.machine_proceed.v0"
MACHINE_PROCEED_STATUS = "MACHINE_PROCEED_PASS_RADIUS_BOUND_PREPARATION_ONLY"
OUTPUT_SURFACE_ID = "c8.n22.next_bounded_unit_definition_surface.v0"
OUTPUT_SURFACE_STATUS = "NEXT_UNIT_DEFINITION_SURFACE_PREPARED_NOT_EXECUTED"
ACTION = "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"
ACTION_SCOPE = "PREPARE_SURFACE_ONLY"
BASIS_SCOPE = "C8_N22_BASIS_ONLY"
SOURCE_OBJECT_ID = "c8.n22"
OUTPUT_KIND = "NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"
OUTPUT_SCOPE = "SURFACE_ONLY"
RADIUS_LIMIT = "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT"
NEXT_POSSIBLE_SURFACE = "REVIEW_OR_DECISION_SURFACE_FOR_CREATED_NEXT_UNIT"

FAIL_CANDIDATE_AUDIT_MISSING = "MACHINE_PROCEED_CLOSURE_FAIL_CANDIDATE_AUDIT_MISSING"
FAIL_PROMOTION_SURFACE_MISSING = "MACHINE_PROCEED_CLOSURE_FAIL_PROMOTION_SURFACE_MISSING"
FAIL_PROMOTION_RECEIPT_MISSING = "MACHINE_PROCEED_CLOSURE_FAIL_PROMOTION_RECEIPT_MISSING"
FAIL_ACTIVE_ENTRY_MISSING = "MACHINE_PROCEED_CLOSURE_FAIL_ACTIVE_ENTRY_MISSING"
FAIL_ACTIVE_ENTRY_NOT_ACTIVE = "MACHINE_PROCEED_CLOSURE_FAIL_ACTIVE_ENTRY_NOT_ACTIVE"
FAIL_MACHINE_PROCEED_RECEIPT_MISSING = "MACHINE_PROCEED_CLOSURE_FAIL_MACHINE_PROCEED_RECEIPT_MISSING"
FAIL_OUTPUT_SURFACE_MISSING = "MACHINE_PROCEED_CLOSURE_FAIL_OUTPUT_SURFACE_MISSING"
FAIL_SOURCE_CHAIN_INCOMPLETE = "MACHINE_PROCEED_CLOSURE_FAIL_SOURCE_CHAIN_INCOMPLETE"
FAIL_ACTION_SCOPE_MISMATCH = "MACHINE_PROCEED_CLOSURE_FAIL_ACTION_SCOPE_MISMATCH"
FAIL_OUTPUT_SHAPE_INVALID = "MACHINE_PROCEED_CLOSURE_FAIL_OUTPUT_SHAPE_INVALID"
FAIL_RADIUS_MISSING = "MACHINE_PROCEED_CLOSURE_FAIL_RADIUS_MISSING"
FAIL_RADIUS_NOT_CONSUMED = "MACHINE_PROCEED_CLOSURE_FAIL_RADIUS_NOT_CONSUMED"
FAIL_RADIUS_NOT_EXHAUSTED = "MACHINE_PROCEED_CLOSURE_FAIL_RADIUS_NOT_EXHAUSTED"
FAIL_RADIUS_RENEWED = "MACHINE_PROCEED_CLOSURE_FAIL_RADIUS_RENEWED"
FAIL_ADDITIONAL_PROCEED_AUTHORIZED = "MACHINE_PROCEED_CLOSURE_FAIL_ADDITIONAL_PROCEED_AUTHORIZED"
FAIL_UNIT_EXECUTED = "MACHINE_PROCEED_CLOSURE_FAIL_UNIT_EXECUTED"
FAIL_RUNTIME_EXECUTED = "MACHINE_PROCEED_CLOSURE_FAIL_RUNTIME_EXECUTED"
FAIL_AUTHORITY_CHANGED = "MACHINE_PROCEED_CLOSURE_FAIL_AUTHORITY_CHANGED"
FAIL_RECEIPTS_REWRITTEN = "MACHINE_PROCEED_CLOSURE_FAIL_RECEIPTS_REWRITTEN"
FAIL_TAXONOMY_PROMOTED = "MACHINE_PROCEED_CLOSURE_FAIL_TAXONOMY_PROMOTED"
FAIL_REUSE_SCOPE_EXPANDED = "MACHINE_PROCEED_CLOSURE_FAIL_REUSE_SCOPE_EXPANDED"
FAIL_UPDATER_GENERALIZED = "MACHINE_PROCEED_CLOSURE_FAIL_UPDATER_GENERALIZED"
FAIL_RUNNER_AUTHORITY_CREATED = "MACHINE_PROCEED_CLOSURE_FAIL_RUNNER_AUTHORITY_CREATED"
FAIL_ACTIVE_ARCHIVE_SCOPE_EXPANDED = "MACHINE_PROCEED_CLOSURE_FAIL_ACTIVE_ARCHIVE_SCOPE_EXPANDED"
FAIL_ACTIVE_ENTRY_REWRITTEN = "MACHINE_PROCEED_CLOSURE_FAIL_ACTIVE_ENTRY_REWRITTEN"
FAIL_ACTIVE_ENTRY_MUTATED = "MACHINE_PROCEED_CLOSURE_FAIL_ACTIVE_ENTRY_MUTATED"
FAIL_FORBIDDEN_EFFECT_DETECTED = "MACHINE_PROCEED_CLOSURE_FAIL_FORBIDDEN_EFFECT_DETECTED"

FAILURE_VOCABULARY = [
    FAIL_CANDIDATE_AUDIT_MISSING,
    FAIL_PROMOTION_SURFACE_MISSING,
    FAIL_PROMOTION_RECEIPT_MISSING,
    FAIL_ACTIVE_ENTRY_MISSING,
    FAIL_ACTIVE_ENTRY_NOT_ACTIVE,
    FAIL_MACHINE_PROCEED_RECEIPT_MISSING,
    FAIL_OUTPUT_SURFACE_MISSING,
    FAIL_SOURCE_CHAIN_INCOMPLETE,
    FAIL_ACTION_SCOPE_MISMATCH,
    FAIL_OUTPUT_SHAPE_INVALID,
    FAIL_RADIUS_MISSING,
    FAIL_RADIUS_NOT_CONSUMED,
    FAIL_RADIUS_NOT_EXHAUSTED,
    FAIL_RADIUS_RENEWED,
    FAIL_ADDITIONAL_PROCEED_AUTHORIZED,
    FAIL_UNIT_EXECUTED,
    FAIL_RUNTIME_EXECUTED,
    FAIL_AUTHORITY_CHANGED,
    FAIL_RECEIPTS_REWRITTEN,
    FAIL_TAXONOMY_PROMOTED,
    FAIL_REUSE_SCOPE_EXPANDED,
    FAIL_UPDATER_GENERALIZED,
    FAIL_RUNNER_AUTHORITY_CREATED,
    FAIL_ACTIVE_ARCHIVE_SCOPE_EXPANDED,
    FAIL_ACTIVE_ENTRY_REWRITTEN,
    FAIL_ACTIVE_ENTRY_MUTATED,
    FAIL_FORBIDDEN_EFFECT_DETECTED,
]

FORBIDDEN_MARKDOWN_PHRASES = [
    "system can continue automatically",
    "next proceed authorized",
    "runner ready",
    "execution ready",
    "runtime ran",
    "authority updated",
    "radius renewed",
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
        fail(FAIL_SOURCE_CHAIN_INCOMPLETE, proc.stderr.strip())
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
        (D4_COMMIT, [D4_PROCEED_JSON, D4_PROCEED_MD, D4_SURFACE_JSON, D4_SURFACE_MD, "scripts/build_c8_n22_prepare_next_unit_definition_surface_machine_proceed_v0.py"], FAIL_MACHINE_PROCEED_RECEIPT_MISSING),
        (D3_COMMIT, [ACTIVE_ENTRY_JSON, "docs/matrixlabs/validator_archive/active/c8_n22_prepare_next_unit_definition_active_archive_entry_v0.md"], FAIL_ACTIVE_ENTRY_MISSING),
        (D2_COMMIT, [PROMOTION_RECEIPT, "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_receipt_v0.md"], FAIL_PROMOTION_RECEIPT_MISSING),
        (D1_COMMIT, [PROMOTION_SURFACE, "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_surface_v0.md"], FAIL_PROMOTION_SURFACE_MISSING),
        (C3_COMMIT, [CANDIDATE_AUDIT, "docs/matrixlabs/validator_archive/audits/c8_n22_candidate_archive_entry_admissibility_audit_v0.md"], FAIL_CANDIDATE_AUDIT_MISSING),
        (C2_COMMIT, [CANDIDATE_ENTRY, "docs/matrixlabs/validator_archive/candidates/c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.md"], FAIL_SOURCE_CHAIN_INCOMPLETE),
        (C1_COMMIT, [SCHEMA_CONTRACT, "docs/matrixlabs/validator_archive/validator_archive_entry_schema_contract_v0.md"], FAIL_SOURCE_CHAIN_INCOMPLETE),
    ]
    for commit, paths, failure_code in expected:
        run_git(root, ["cat-file", "-e", f"{commit}^{{commit}}"], failure_code)
        got = commit_for_paths(root, paths, failure_code)
        if got != commit:
            fail(failure_code, f"{paths[0]} commit mismatch: {got}!={commit}")


def load_json(root: Path, rel: str, missing_code: str) -> dict[str, Any]:
    try:
        return json.loads((root / rel).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        fail(missing_code, rel)
        raise exc
    except json.JSONDecodeError as exc:
        fail(missing_code, f"{rel}: {exc}")
        raise exc


def expect(value: object, wanted: object, failure_code: str, field: str) -> None:
    if value != wanted:
        fail(failure_code, f"{field}: {value!r}!={wanted!r}")


def bool_text(value: bool) -> str:
    return str(value).lower()


def json_text(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def validate_sources(root: Path, sources: dict[str, dict[str, Any]]) -> None:
    if not (root / D4_PROCEED_MD).exists():
        fail(FAIL_MACHINE_PROCEED_RECEIPT_MISSING, D4_PROCEED_MD)
    if not (root / D4_SURFACE_MD).exists():
        fail(FAIL_OUTPUT_SURFACE_MISSING, D4_SURFACE_MD)

    active = sources["active"]
    active_state = active.get("materialized_archive_entry_state", {})
    expect(active.get("active_archive_entry_id"), ACTIVE_ENTRY_ID, FAIL_ACTIVE_ENTRY_NOT_ACTIVE, "active.active_archive_entry_id")
    expect(active_state.get("archive_entry_status"), ACTIVE_ENTRY_STATUS, FAIL_ACTIVE_ENTRY_NOT_ACTIVE, "active.archive_entry_status")
    expect(active.get("materialization_status"), "ACTIVE_ARCHIVE_ENTRY_PASS_MATERIALIZED_FOR_DECLARED_SCOPE", FAIL_ACTIVE_ENTRY_NOT_ACTIVE, "active.materialization_status")
    expect(active.get("radius_state", {}).get("radius_policy"), RADIUS_LIMIT, FAIL_RADIUS_MISSING, "active.radius_policy")

    proceed = sources["proceed"]
    expect(proceed.get("machine_proceed_id"), MACHINE_PROCEED_ID, FAIL_MACHINE_PROCEED_RECEIPT_MISSING, "machine_proceed_id")
    expect(proceed.get("proceed_status"), MACHINE_PROCEED_STATUS, FAIL_MACHINE_PROCEED_RECEIPT_MISSING, "proceed_status")
    expect(proceed.get("terminal_transition"), "ADVANCE(D5_MACHINE_PROCEED_CLOSURE_PENDING)", FAIL_SOURCE_CHAIN_INCOMPLETE, "proceed.terminal_transition")
    performed = proceed.get("performed_action", {})
    expect(performed.get("performed_action"), ACTION, FAIL_ACTION_SCOPE_MISMATCH, "performed_action")
    expect(performed.get("performed_action_scope"), ACTION_SCOPE, FAIL_ACTION_SCOPE_MISMATCH, "performed_action_scope")
    expect(performed.get("performed_basis_scope"), BASIS_SCOPE, FAIL_ACTION_SCOPE_MISMATCH, "performed_basis_scope")
    expect(performed.get("performed_source_object_id"), SOURCE_OBJECT_ID, FAIL_ACTION_SCOPE_MISMATCH, "performed_source_object_id")
    expect(performed.get("performed_output_kind"), OUTPUT_KIND, FAIL_ACTION_SCOPE_MISMATCH, "performed_output_kind")
    radius = proceed.get("radius", {})
    if "radius_before" not in radius:
        fail(FAIL_RADIUS_MISSING, "radius_before")
    expect(radius.get("radius_before"), 1, FAIL_RADIUS_MISSING, "radius_before")
    expect(radius.get("radius_consumed"), 1, FAIL_RADIUS_NOT_CONSUMED, "radius_consumed")
    expect(radius.get("radius_after"), 0, FAIL_RADIUS_NOT_EXHAUSTED, "radius_after")
    expect(radius.get("radius_exhausted"), True, FAIL_RADIUS_NOT_EXHAUSTED, "radius_exhausted")
    expect(radius.get("radius_renewed_by_this_proceed"), False, FAIL_RADIUS_RENEWED, "radius_renewed_by_this_proceed")
    expect(radius.get("additional_radius_created"), False, FAIL_RADIUS_RENEWED, "additional_radius_created")
    for key, value in proceed.get("non_effects", {}).items():
        if value is not False:
            fail(FAIL_FORBIDDEN_EFFECT_DETECTED, f"d4 non_effects.{key}: {value!r}")

    surface = sources["surface"]
    expect(surface.get("unit_surface_id"), OUTPUT_SURFACE_ID, FAIL_OUTPUT_SHAPE_INVALID, "surface.unit_surface_id")
    expect(surface.get("surface_role"), OUTPUT_KIND, FAIL_OUTPUT_SHAPE_INVALID, "surface.surface_role")
    expect(surface.get("surface_status"), OUTPUT_SURFACE_STATUS, FAIL_OUTPUT_SHAPE_INVALID, "surface.surface_status")
    expect(surface.get("basis", {}).get("basis_object_id"), SOURCE_OBJECT_ID, FAIL_OUTPUT_SHAPE_INVALID, "surface.basis_object_id")
    expect(surface.get("basis", {}).get("basis_scope"), BASIS_SCOPE, FAIL_OUTPUT_SHAPE_INVALID, "surface.basis_scope")
    expect(surface.get("proposed_next_unit", {}).get("execution_status"), "NOT_EXECUTED", FAIL_UNIT_EXECUTED, "surface.execution_status")
    expect(surface.get("surface_gate", {}).get("not_executed"), True, FAIL_UNIT_EXECUTED, "surface.not_executed")

    audit = sources["candidate_audit"]
    expect(audit.get("audit_id"), AUDIT_ID, FAIL_CANDIDATE_AUDIT_MISSING, "audit_id")
    expect(audit.get("audit_result", {}).get("candidate_audit_status"), AUDIT_STATUS, FAIL_CANDIDATE_AUDIT_MISSING, "candidate_audit_status")
    expect(sources["promotion_surface"].get("promotion_decision_surface_id"), SURFACE_ID, FAIL_PROMOTION_SURFACE_MISSING, "promotion_decision_surface_id")
    receipt = sources["promotion_receipt"]
    expect(receipt.get("promotion_decision_receipt_id"), RECEIPT_ID, FAIL_PROMOTION_RECEIPT_MISSING, "promotion_decision_receipt_id")
    expect(receipt.get("decision_event", {}).get("selected_promotion_option"), SELECTED_OPTION, FAIL_PROMOTION_RECEIPT_MISSING, "selected_promotion_option")
    expect(sources["candidate_entry"].get("archive_entry_id"), "candidate.c8.n22.prepare_next_unit_definition_surface.v0", FAIL_SOURCE_CHAIN_INCOMPLETE, "candidate_entry.archive_entry_id")
    expect(sources["schema_contract"].get("archive_schema_contract_id"), "validator_archive_entry_schema_contract.v0", FAIL_SOURCE_CHAIN_INCOMPLETE, "archive_schema_contract_id")


def source_chain() -> dict[str, Any]:
    return {
        "candidate_audit_id": AUDIT_ID,
        "candidate_audit_status": AUDIT_STATUS,
        "promotion_decision_surface_id": SURFACE_ID,
        "promotion_decision_receipt_id": RECEIPT_ID,
        "selected_promotion_option": SELECTED_OPTION,
        "active_archive_entry_id": ACTIVE_ENTRY_ID,
        "active_archive_entry_status": ACTIVE_ENTRY_STATUS,
        "machine_proceed_id": MACHINE_PROCEED_ID,
        "machine_proceed_status": MACHINE_PROCEED_STATUS,
        "created_output_surface_id": OUTPUT_SURFACE_ID,
        "created_output_surface_status": OUTPUT_SURFACE_STATUS,
        "source_chain_complete": True,
    }


def source_chain_checks() -> dict[str, Any]:
    return {
        "candidate_audit_present": True,
        "candidate_audit_status": AUDIT_STATUS,
        "promotion_decision_surface_present": True,
        "promotion_decision_receipt_present": True,
        "selected_promotion_option": SELECTED_OPTION,
        "active_archive_entry_present": True,
        "active_archive_entry_status": ACTIVE_ENTRY_STATUS,
        "machine_proceed_receipt_present": True,
        "machine_proceed_status": MACHINE_PROCEED_STATUS,
        "output_surface_present": True,
        "output_surface_status": OUTPUT_SURFACE_STATUS,
        "source_chain_complete": True,
    }


def d4_artifact_checks() -> dict[str, bool]:
    return {
        "machine_proceed_json_present": True,
        "machine_proceed_md_present": True,
        "output_surface_json_present": True,
        "output_surface_md_present": True,
        "machine_proceed_id_matches": True,
        "output_surface_id_matches": True,
        "machine_proceed_terminal_transition_matches": True,
    }


def performed_move_summary() -> dict[str, str]:
    return {
        "performed_action": ACTION,
        "performed_action_scope": ACTION_SCOPE,
        "performed_basis_scope": BASIS_SCOPE,
        "performed_source_object_id": SOURCE_OBJECT_ID,
        "performed_output_kind": OUTPUT_KIND,
    }


def radius_result() -> dict[str, Any]:
    return {
        "radius_limit": RADIUS_LIMIT,
        "radius_before": 1,
        "radius_consumed": 1,
        "radius_after": 0,
        "radius_exhausted": True,
        "radius_renewed_by_closure": False,
        "additional_radius_created": False,
        "further_machine_proceed_authorized_under_this_radius": False,
    }


def radius_verification() -> dict[str, Any]:
    return {
        "radius_declared_by_active_entry": RADIUS_LIMIT,
        "radius_before": 1,
        "radius_consumed": 1,
        "radius_after": 0,
        "radius_consumed_exactly_once": True,
        "radius_overconsumed": False,
        "radius_underconsumed": False,
        "radius_exhausted": True,
        "radius_renewed_by_closure": False,
        "additional_radius_created": False,
    }


def output_result() -> dict[str, Any]:
    return {
        "output_surface_created": True,
        "output_surface_id": OUTPUT_SURFACE_ID,
        "output_object_type": OUTPUT_KIND,
        "output_scope": OUTPUT_SCOPE,
        "output_basis": SOURCE_OBJECT_ID,
        "output_surface_status": OUTPUT_SURFACE_STATUS,
        "unit_executed": False,
    }


def output_surface_verification() -> dict[str, Any]:
    return {
        "output_surface_present": True,
        "output_surface_id": OUTPUT_SURFACE_ID,
        "output_object_type": OUTPUT_KIND,
        "output_scope": OUTPUT_SCOPE,
        "output_basis": SOURCE_OBJECT_ID,
        "execution_status": "NOT_EXECUTED",
        "output_surface_status": OUTPUT_SURFACE_STATUS,
        "output_shape_valid": True,
    }


def active_entry_post_use_status() -> dict[str, Any]:
    return {
        "active_archive_entry_id": ACTIVE_ENTRY_ID,
        "entry_remains_audit_source": True,
        "entry_has_remaining_radius": False,
        "entry_may_authorize_additional_machine_proceed": False,
        "additional_use_requires_new_authority_or_radius": True,
    }


def post_closure_authority_boundary() -> dict[str, bool]:
    return {
        "same_active_entry_may_authorize_additional_machine_proceed_under_same_radius": False,
        "same_radius_may_be_reused": False,
        "additional_machine_proceed_requires_new_authority_or_radius": True,
        "created_surface_execution_requires_separate_authority": True,
    }


def d4_verified_non_effects() -> dict[str, bool]:
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
        "active_archive_entry_rewritten": False,
        "active_archive_entry_mutated": False,
    }


def d5_closure_non_effects() -> dict[str, bool]:
    return {
        "performed_another_machine_action": False,
        "radius_renewed_by_closure": False,
        "additional_proceed_authorized_by_closure": False,
        "created_next_decision_surface": False,
        "executed_created_next_unit": False,
        "runtime_executed_by_closure": False,
        "authority_changed_by_closure": False,
        "active_archive_entry_rewritten_by_closure": False,
        "active_archive_entry_mutated_by_closure": False,
        "runner_authority_created_by_closure": False,
    }


def forbidden_effect_verification() -> dict[str, bool]:
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
        "active_archive_scope_expanded": False,
        "active_archive_entry_rewritten_by_closure": False,
        "active_archive_entry_mutated_by_closure": False,
        "forbidden_effect_detected": False,
    }


def next_possible_separate_surface() -> dict[str, Any]:
    return {
        "surface": NEXT_POSSIBLE_SURFACE,
        "reason": "D.4 created a next bounded unit definition surface but did not authorize execution.",
        "created_by_this_closure": False,
        "authorized_by_this_closure": False,
        "machine_may_prepare_without_new_authority": False,
    }


def closure_gate() -> dict[str, Any]:
    gate: dict[str, Any] = {
        "machine_proceed_closure_gate": CLOSURE_STATUS,
        "candidate_audit_present": True,
        "promotion_decision_surface_present": True,
        "promotion_decision_receipt_present": True,
        "active_archive_entry_present": True,
        "machine_proceed_receipt_present": True,
        "output_surface_present": True,
        "source_chain_complete": True,
        "candidate_audit_status": AUDIT_STATUS,
        "active_archive_entry_status": ACTIVE_ENTRY_STATUS,
        "machine_proceed_status": MACHINE_PROCEED_STATUS,
        "performed_action": ACTION,
        "performed_action_scope": ACTION_SCOPE,
        "basis_scope": BASIS_SCOPE,
        "source_object_id": SOURCE_OBJECT_ID,
        "output_object_type": OUTPUT_KIND,
        "output_scope": OUTPUT_SCOPE,
        "output_surface_status": OUTPUT_SURFACE_STATUS,
        "output_surface_created": True,
        "radius_limit": RADIUS_LIMIT,
        "radius_before": 1,
        "radius_consumed": 1,
        "radius_after": 0,
        "radius_exhausted": True,
        "radius_renewed_by_closure": False,
        "entry_has_remaining_radius": False,
        "entry_may_authorize_additional_machine_proceed": False,
        "additional_use_requires_new_authority_or_radius": True,
        "same_radius_may_be_reused": False,
        "additional_machine_proceed_authorized": False,
        "forbidden_effect_detected": False,
        "failures": [],
    }
    gate.update(forbidden_effect_verification())
    return gate


def build_record() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "closure_id": CLOSURE_ID,
        "closure_role": CLOSURE_ROLE,
        "closure_status": CLOSURE_STATUS,
        "block_id": BLOCK_ID,
        "block_status": BLOCK_STATUS,
        "block_closed": True,
        "source_chain": source_chain(),
        "source_chain_checks": source_chain_checks(),
        "d4_artifact_checks": d4_artifact_checks(),
        "performed_move_summary": performed_move_summary(),
        "radius_result": radius_result(),
        "radius_verification": radius_verification(),
        "output_result": output_result(),
        "output_surface_verification": output_surface_verification(),
        "active_entry_post_use_status": active_entry_post_use_status(),
        "post_closure_authority_boundary": post_closure_authority_boundary(),
        "d4_verified_non_effects": d4_verified_non_effects(),
        "d5_closure_non_effects": d5_closure_non_effects(),
        "forbidden_effect_verification": forbidden_effect_verification(),
        "next_possible_separate_surface": next_possible_separate_surface(),
        "closure_gate": closure_gate(),
        "failure_vocabulary": FAILURE_VOCABULARY,
        "non_claims": [
            "D.5 does not perform another machine action.",
            "D.5 does not renew radius.",
            "D.5 does not authorize additional proceed.",
            "D.5 does not execute the created next unit.",
            "D.5 does not run runtime.",
            "D.5 does not change authority state.",
            "D.5 does not rewrite receipts.",
            "D.5 does not rewrite or mutate the active archive entry.",
            "D.5 does not promote taxonomy.",
            "D.5 does not expand reuse scope.",
            "D.5 does not generalize the updater.",
            "D.5 does not activate a runner.",
            "D.5 does not create the next decision surface.",
            "D.5 only closes and preserves the completed one-radius machine preparation specimen.",
        ],
        "key_non_claims": [
            "closure ≠ renewal",
            "active archive entry used once ≠ active runner",
            "created surface ≠ executed unit",
            "one exhausted radius ≠ continued machine authority",
        ],
        "precommit_c8_n22_machine_proceed_closure_gate": PRECOMMIT_GATE,
        "machine_proceed_closure_gate": CLOSURE_STATUS,
        "terminal_transition": TERMINAL_TRANSITION,
        "generated_by": GENERATOR,
    }


def validate_record(record: dict[str, Any]) -> None:
    expect(record.get("schema_version"), SCHEMA_VERSION, FAIL_OUTPUT_SHAPE_INVALID, "schema_version")
    expect(record.get("closure_id"), CLOSURE_ID, FAIL_OUTPUT_SHAPE_INVALID, "closure_id")
    expect(record.get("closure_status"), CLOSURE_STATUS, FAIL_OUTPUT_SHAPE_INVALID, "closure_status")
    expect(record.get("block_closed"), True, FAIL_OUTPUT_SHAPE_INVALID, "block_closed")
    expect(record.get("terminal_transition"), TERMINAL_TRANSITION, FAIL_OUTPUT_SHAPE_INVALID, "terminal_transition")
    expect(record.get("source_chain", {}).get("source_chain_complete"), True, FAIL_SOURCE_CHAIN_INCOMPLETE, "source_chain_complete")
    expect(record.get("radius_result", {}).get("radius_after"), 0, FAIL_RADIUS_NOT_EXHAUSTED, "radius_after")
    expect(record.get("radius_result", {}).get("radius_consumed"), 1, FAIL_RADIUS_NOT_CONSUMED, "radius_consumed")
    expect(record.get("radius_result", {}).get("radius_renewed_by_closure"), False, FAIL_RADIUS_RENEWED, "radius_renewed_by_closure")
    expect(record.get("radius_result", {}).get("additional_radius_created"), False, FAIL_RADIUS_RENEWED, "additional_radius_created")
    expect(record.get("radius_result", {}).get("further_machine_proceed_authorized_under_this_radius"), False, FAIL_ADDITIONAL_PROCEED_AUTHORIZED, "further_machine_proceed_authorized_under_this_radius")
    for section in ["d4_verified_non_effects", "d5_closure_non_effects", "forbidden_effect_verification"]:
        for key, value in record.get(section, {}).items():
            if key == "forbidden_effect_detected":
                expect(value, False, FAIL_FORBIDDEN_EFFECT_DETECTED, f"{section}.{key}")
            elif value is not False:
                fail(FAIL_FORBIDDEN_EFFECT_DETECTED, f"{section}.{key}: {value!r}")
    expect(record.get("closure_gate", {}).get("failures"), [], FAIL_FORBIDDEN_EFFECT_DETECTED, "closure_gate.failures")


def render_markdown(record: dict[str, Any]) -> str:
    radius = record["radius_result"]
    return f"""# C8 n22 machine proceed closure v0

## Status

{record['closure_status']}

## Block

{record['block_status']}

## Source chain

- candidate audit: {AUDIT_ID}
- promotion decision surface: {SURFACE_ID}
- promotion decision receipt: {RECEIPT_ID}
- active archive entry: {ACTIVE_ENTRY_ID}
- machine proceed receipt: {MACHINE_PROCEED_ID}
- output surface: {OUTPUT_SURFACE_ID}

## Performed move

{ACTION}

## Scope

{ACTION_SCOPE}

## Basis

c8.n22 only

## Radius

- before: {radius['radius_before']}
- consumed: {radius['radius_consumed']}
- after: {radius['radius_after']}
- exhausted: {bool_text(radius['radius_exhausted'])}
- renewed by closure: {bool_text(radius['radius_renewed_by_closure'])}

## Output

{OUTPUT_KIND}

## Output status

{OUTPUT_SURFACE_STATUS}

## Confirmed D.4 non-effects

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

## D.5 closure non-effects

- no second machine action performed
- radius not renewed by closure
- no additional proceed authorized
- next decision surface not created
- created next unit not executed
- runtime not executed by closure
- authority not changed by closure
- active archive entry not rewritten by closure
- active archive entry not mutated by closure
- runner authority not created by closure

## Post-use status

The active archive entry remains the authority source for this completed move, but it has no remaining radius for another machine proceed.

## Next possible separate surface

{NEXT_POSSIBLE_SURFACE}

This closure does not create or authorize that surface.

## Non-claim

This closure does not renew radius, execute the next unit, authorize another proceed, or authorize a runner.
"""


def validate_markdown(text: str) -> None:
    lowered = text.lower()
    for phrase in FORBIDDEN_MARKDOWN_PHRASES:
        if phrase in lowered:
            fail(FAIL_FORBIDDEN_EFFECT_DETECTED, phrase)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def guard_output(root: Path, rel: str, content: str) -> None:
    path = root / rel
    if path.exists() and path.read_text(encoding="utf-8") != content:
        fail(FAIL_OUTPUT_SHAPE_INVALID, f"refusing to overwrite non-deterministic {rel}")


def write_outputs(root: Path, record: dict[str, Any]) -> None:
    json_content = json_text(record)
    md_content = render_markdown(record)
    validate_markdown(md_content)
    guard_output(root, OUTPUT_JSON, json_content)
    guard_output(root, OUTPUT_MD, md_content)
    write_text(root / OUTPUT_JSON, json_content)
    write_text(root / OUTPUT_MD, md_content)


def print_success(record: dict[str, Any]) -> None:
    chain = record["source_chain"]
    move = record["performed_move_summary"]
    radius = record["radius_result"]
    post = record["active_entry_post_use_status"]
    boundary = record["post_closure_authority_boundary"]
    d4_non = record["d4_verified_non_effects"]
    forbidden = record["forbidden_effect_verification"]
    next_surface = record["next_possible_separate_surface"]

    print("BUILD_C8_N22_MACHINE_PROCEED_CLOSURE_V0_COMPLETE")
    print(f"closure_id={record['closure_id']}")
    print(f"schema_version={record['schema_version']}")
    print(f"closure_role={record['closure_role']}")
    print(f"closure_status={record['closure_status']}")
    print(f"block_id={record['block_id']}")
    print(f"block_status={record['block_status']}")
    print(f"block_closed={bool_text(record['block_closed'])}")
    print(f"candidate_audit_id={chain['candidate_audit_id']}")
    print(f"promotion_decision_surface_id={chain['promotion_decision_surface_id']}")
    print(f"promotion_decision_receipt_id={chain['promotion_decision_receipt_id']}")
    print(f"selected_promotion_option={chain['selected_promotion_option']}")
    print(f"active_archive_entry_id={chain['active_archive_entry_id']}")
    print(f"active_archive_entry_status={chain['active_archive_entry_status']}")
    print(f"machine_proceed_id={chain['machine_proceed_id']}")
    print(f"machine_proceed_status={chain['machine_proceed_status']}")
    print(f"created_output_surface_id={chain['created_output_surface_id']}")
    print(f"created_output_surface_status={chain['created_output_surface_status']}")
    print(f"performed_action={move['performed_action']}")
    print(f"performed_action_scope={move['performed_action_scope']}")
    print(f"performed_basis_scope={move['performed_basis_scope']}")
    print(f"performed_source_object_id={move['performed_source_object_id']}")
    print(f"performed_output_kind={move['performed_output_kind']}")
    print(f"radius_limit={radius['radius_limit']}")
    print(f"radius_before={radius['radius_before']}")
    print(f"radius_consumed={radius['radius_consumed']}")
    print(f"radius_after={radius['radius_after']}")
    print(f"radius_exhausted={bool_text(radius['radius_exhausted'])}")
    print(f"radius_renewed_by_closure={bool_text(radius['radius_renewed_by_closure'])}")
    print(f"additional_radius_created={bool_text(radius['additional_radius_created'])}")
    print(f"further_machine_proceed_authorized_under_this_radius={bool_text(radius['further_machine_proceed_authorized_under_this_radius'])}")
    print(f"entry_remains_audit_source={bool_text(post['entry_remains_audit_source'])}")
    print(f"entry_has_remaining_radius={bool_text(post['entry_has_remaining_radius'])}")
    print(f"entry_may_authorize_additional_machine_proceed={bool_text(post['entry_may_authorize_additional_machine_proceed'])}")
    print(f"additional_use_requires_new_authority_or_radius={bool_text(post['additional_use_requires_new_authority_or_radius'])}")
    print(f"same_active_entry_may_authorize_additional_machine_proceed_under_same_radius={bool_text(boundary['same_active_entry_may_authorize_additional_machine_proceed_under_same_radius'])}")
    print(f"same_radius_may_be_reused={bool_text(boundary['same_radius_may_be_reused'])}")
    print(f"additional_machine_proceed_requires_new_authority_or_radius={bool_text(boundary['additional_machine_proceed_requires_new_authority_or_radius'])}")
    print(f"created_surface_execution_requires_separate_authority={bool_text(boundary['created_surface_execution_requires_separate_authority'])}")
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
    ]:
        print(f"{key}={bool_text(d4_non[key])}")
    print(f"active_archive_scope_expanded={bool_text(forbidden['active_archive_scope_expanded'])}")
    print(f"active_archive_entry_rewritten_by_closure={bool_text(forbidden['active_archive_entry_rewritten_by_closure'])}")
    print(f"active_archive_entry_mutated_by_closure={bool_text(forbidden['active_archive_entry_mutated_by_closure'])}")
    print(f"next_possible_separate_surface={next_surface['surface']}")
    print(f"next_possible_separate_surface_created_by_this_closure={bool_text(next_surface['created_by_this_closure'])}")
    print(f"next_possible_separate_surface_authorized_by_this_closure={bool_text(next_surface['authorized_by_this_closure'])}")
    print(f"machine_may_prepare_next_surface_without_new_authority={bool_text(next_surface['machine_may_prepare_without_new_authority'])}")
    print(f"machine_proceed_closure_gate={record['machine_proceed_closure_gate']}")
    print(f"precommit_c8_n22_machine_proceed_closure_gate={record['precommit_c8_n22_machine_proceed_closure_gate']}")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition={record['terminal_transition']}")


def main() -> int:
    try:
        root = detect_repo_root(Path.cwd())
        verify_expected_commits(root)
        sources = {
            "active": load_json(root, ACTIVE_ENTRY_JSON, FAIL_ACTIVE_ENTRY_MISSING),
            "proceed": load_json(root, D4_PROCEED_JSON, FAIL_MACHINE_PROCEED_RECEIPT_MISSING),
            "surface": load_json(root, D4_SURFACE_JSON, FAIL_OUTPUT_SURFACE_MISSING),
            "promotion_receipt": load_json(root, PROMOTION_RECEIPT, FAIL_PROMOTION_RECEIPT_MISSING),
            "promotion_surface": load_json(root, PROMOTION_SURFACE, FAIL_PROMOTION_SURFACE_MISSING),
            "candidate_entry": load_json(root, CANDIDATE_ENTRY, FAIL_SOURCE_CHAIN_INCOMPLETE),
            "candidate_audit": load_json(root, CANDIDATE_AUDIT, FAIL_CANDIDATE_AUDIT_MISSING),
            "schema_contract": load_json(root, SCHEMA_CONTRACT, FAIL_SOURCE_CHAIN_INCOMPLETE),
        }
        validate_sources(root, sources)
        record = build_record()
        validate_record(record)
        write_outputs(root, record)
    except GenerationError as exc:
        print(f"STOP_{exc.code}")
        if exc.detail:
            print(exc.detail, file=sys.stderr)
        return 2
    print_success(record)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
