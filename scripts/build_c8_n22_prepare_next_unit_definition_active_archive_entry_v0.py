#!/usr/bin/env python3
"""Build C8 n22 prepare-next-unit active archive entry v0.

This materializes the active archive-entry state selected by the D.2 human
promotion decision receipt. It does not perform machine proceed, consume
radius, prepare the next unit definition surface, or run runtime.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_prepare_next_unit_definition_active_archive_entry_v0.py"
OUTPUT_JSON = "docs/matrixlabs/validator_archive/active/c8_n22_prepare_next_unit_definition_active_archive_entry_v0.json"
OUTPUT_MD = "docs/matrixlabs/validator_archive/active/c8_n22_prepare_next_unit_definition_active_archive_entry_v0.md"

PROMOTION_RECEIPT = "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_receipt_v0.json"
PROMOTION_SURFACE = "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_surface_v0.json"
CANDIDATE_ENTRY = "docs/matrixlabs/validator_archive/candidates/c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.json"
CANDIDATE_AUDIT = "docs/matrixlabs/validator_archive/audits/c8_n22_candidate_archive_entry_admissibility_audit_v0.json"
SCHEMA_CONTRACT = "docs/matrixlabs/validator_archive/validator_archive_entry_schema_contract_v0.json"

D2_COMMIT = "41233ed53084b9ceb2348661d07342feaf65cac7"
D1_COMMIT = "a457bf08eb263cdbdad01a4eef6b7e7e2b11f230"
C3_COMMIT = "f49dfab97774414330682151e6e3fffeb7ba6f66"
C2_COMMIT = "674c601136f381c9d85605f646900998b24ddfe9"
C1_COMMIT = "96223d2a9827543c27f93a1c0a16a6670a97de71"

SCHEMA_VERSION = "matrixlabs_active_archive_entry_materialization_v0"
MATERIALIZATION_ID = "c8.n22.prepare_next_unit_definition.active_archive_entry_materialization.v0"
ACTIVE_ENTRY_ID = "active.c8.n22.prepare_next_unit_definition_surface.v0"
MATERIALIZATION_ROLE = "ACTIVE_ARCHIVE_ENTRY_STATE_MATERIALIZATION"
MATERIALIZATION_STATUS = "ACTIVE_ARCHIVE_ENTRY_PASS_MATERIALIZED_FOR_DECLARED_SCOPE"
BLOCK_ID = "BLOCK_D"
BLOCK_UNIT_ID = "D3_ARCHIVE_ENTRY_STATE_MATERIALIZATION"
PRECOMMIT_GATE = "PASS"
TERMINAL_TRANSITION = "ADVANCE(D4_MACHINE_PROCEED_UNDER_ACTIVE_ENTRY_PENDING)"

RECEIPT_ID = "c8.n22.candidate_promotion_decision_receipt.v0"
RECEIPT_STATUS = "PROMOTION_DECISION_RECEIPT_RECORDED"
RECEIPT_GATE = "PROMOTION_DECISION_RECEIPT_PASS_TYPED_DECISION_RECORDED"
SURFACE_ID = "c8.n22.candidate_promotion_decision_surface.v0"
SURFACE_STATUS = "PROMOTION_DECISION_SURFACE_PRESENTS_TYPED_OPTIONS_ONLY"
CANDIDATE_ID = "candidate.c8.n22.prepare_next_unit_definition_surface.v0"
CANDIDATE_STATUS = "ARCHIVE_STATUS_CANDIDATE"
AUDIT_ID = "c8.n22.candidate_archive_entry.admissibility_audit.v0"
AUDIT_STATUS = "CANDIDATE_AUDIT_PASS_CONTRACT_CONFORMANT_NOT_PROMOTED"
CONTRACT_ID = "validator_archive_entry_schema_contract.v0"

SELECTED_OPTION = "DECISION_PROMOTE_CANDIDATE_FOR_DECLARED_SCOPE"
DECISION_ACTOR_CLASS = "HUMAN"
SELECTION_SOURCE = "EXPLICIT_HUMAN_SELECTION"

AUTHORITY_STATE = "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION"
REQUESTED_ACTION = "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"
REQUESTED_SCOPE = "PREPARE_SURFACE_ONLY"
BASIS_SCOPE = "C8_N22_BASIS_ONLY"
SOURCE_OBJECT_ID = "c8.n22"
OUTPUT_KIND = "NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"
RADIUS_POLICY = "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT"

ACTIVE_ARCHIVE_ENTRY_STATUS = "ARCHIVE_STATUS_PREAPPROVED_ACTIVE"
PROMOTION_STATUS = "PROMOTION_GRANTED_FOR_DECLARED_SCOPE"
REUSE_AUTHORITY_STATUS = "REUSE_AUTHORITY_GRANTED_FOR_DECLARED_SCOPE"
ACTIVATION_STATUS = "ACTIVATION_ACTIVE"
D4_NEXT_UNIT = "D4_MACHINE_PROCEED_UNDER_ACTIVE_ENTRY"

FAIL_RECEIPT_MISSING = "ARCHIVE_ENTRY_STATE_FAIL_PROMOTION_RECEIPT_MISSING"
FAIL_RECEIPT_NOT_PASS = "ARCHIVE_ENTRY_STATE_FAIL_PROMOTION_RECEIPT_NOT_PASS"
FAIL_SELECTED_OPTION_MISSING = "ARCHIVE_ENTRY_STATE_FAIL_SELECTED_OPTION_MISSING"
FAIL_SELECTED_OPTION_NOT_ON_SURFACE = "ARCHIVE_ENTRY_STATE_FAIL_SELECTED_OPTION_NOT_ON_SURFACE"
FAIL_SELECTED_OPTION_NOT_ACTIVE_BRANCH = "ARCHIVE_ENTRY_STATE_FAIL_SELECTED_OPTION_NOT_ACTIVE_BRANCH"
FAIL_SCOPE_MISMATCH = "ARCHIVE_ENTRY_STATE_FAIL_SCOPE_MISMATCH"
FAIL_RADIUS_MISSING = "ARCHIVE_ENTRY_STATE_FAIL_RADIUS_MISSING"
FAIL_RADIUS_MISMATCH = "ARCHIVE_ENTRY_STATE_FAIL_RADIUS_MISMATCH"
FAIL_RADIUS_OVERBROAD = "ARCHIVE_ENTRY_STATE_FAIL_RADIUS_OVERBROAD"
FAIL_CANDIDATE_MISSING = "ARCHIVE_ENTRY_STATE_FAIL_CANDIDATE_MISSING"
FAIL_CANDIDATE_AUDIT_MISSING = "ARCHIVE_ENTRY_STATE_FAIL_CANDIDATE_AUDIT_MISSING"
FAIL_CANDIDATE_AUDIT_NOT_PASS = "ARCHIVE_ENTRY_STATE_FAIL_CANDIDATE_AUDIT_NOT_PASS"
FAIL_FORBIDDEN_EFFECTS_MISSING = "ARCHIVE_ENTRY_STATE_FAIL_FORBIDDEN_EFFECTS_MISSING"
FAIL_MACHINE_PROCEED = "ARCHIVE_ENTRY_STATE_FAIL_MACHINE_PROCEED_INSIDE_MATERIALIZATION"
FAIL_NEXT_UNIT_SURFACE = "ARCHIVE_ENTRY_STATE_FAIL_NEXT_UNIT_SURFACE_PREPARED_INSIDE_MATERIALIZATION"
FAIL_RUNNER_AUTHORITY = "ARCHIVE_ENTRY_STATE_FAIL_RUNNER_AUTHORITY_CREATED_INSIDE_MATERIALIZATION"
FAIL_OBSERVED_PATH = "ARCHIVE_ENTRY_STATE_FAIL_OBSERVED_PATH_UPDATED_INSIDE_MATERIALIZATION"
FAIL_RADIUS_CONSUMED = "ARCHIVE_ENTRY_STATE_FAIL_RADIUS_CONSUMED_INSIDE_MATERIALIZATION"
FAIL_SCOPE_EXPANDED = "ARCHIVE_ENTRY_STATE_FAIL_SCOPE_EXPANDED_INSIDE_MATERIALIZATION"
FAIL_RECEIPT_REWRITTEN = "ARCHIVE_ENTRY_STATE_FAIL_RECEIPT_REWRITTEN_INSIDE_MATERIALIZATION"
FAIL_MARKDOWN_JSON_PARITY = "ARCHIVE_ENTRY_STATE_FAIL_MARKDOWN_JSON_PARITY"

FAILURE_VOCABULARY = [
    FAIL_RECEIPT_MISSING,
    FAIL_RECEIPT_NOT_PASS,
    FAIL_SELECTED_OPTION_MISSING,
    FAIL_SELECTED_OPTION_NOT_ON_SURFACE,
    FAIL_SELECTED_OPTION_NOT_ACTIVE_BRANCH,
    FAIL_SCOPE_MISMATCH,
    FAIL_RADIUS_MISSING,
    FAIL_RADIUS_MISMATCH,
    FAIL_RADIUS_OVERBROAD,
    FAIL_CANDIDATE_MISSING,
    FAIL_CANDIDATE_AUDIT_MISSING,
    FAIL_CANDIDATE_AUDIT_NOT_PASS,
    FAIL_FORBIDDEN_EFFECTS_MISSING,
    FAIL_MACHINE_PROCEED,
    FAIL_NEXT_UNIT_SURFACE,
    FAIL_RUNNER_AUTHORITY,
    FAIL_OBSERVED_PATH,
    FAIL_RADIUS_CONSUMED,
    FAIL_SCOPE_EXPANDED,
    FAIL_RECEIPT_REWRITTEN,
]

FORBIDDEN_SCOPE_TERMS = [
    "ANY_C8_BASIS",
    "ANY_ACCEPTED_BASIS_OBJECT",
    "EXECUTE_UNIT",
    "RUN_NEXT_UNIT",
    "RADIUS_N_BATCH",
    "RUNNER_AUTHORITY",
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
        fail(FAIL_RECEIPT_MISSING, proc.stderr.strip())
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
        (D2_COMMIT, [PROMOTION_RECEIPT, "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_receipt_v0.md", "scripts/build_c8_n22_candidate_promotion_decision_receipt_v0.py"], FAIL_RECEIPT_MISSING),
        (D1_COMMIT, [PROMOTION_SURFACE, "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_surface_v0.md", "scripts/build_c8_n22_candidate_promotion_decision_surface_v0.py"], FAIL_SELECTED_OPTION_NOT_ON_SURFACE),
        (C3_COMMIT, [CANDIDATE_AUDIT, "docs/matrixlabs/validator_archive/audits/c8_n22_candidate_archive_entry_admissibility_audit_v0.md", "scripts/build_c8_n22_candidate_archive_entry_admissibility_audit_v0.py"], FAIL_CANDIDATE_AUDIT_MISSING),
        (C2_COMMIT, [CANDIDATE_ENTRY, "docs/matrixlabs/validator_archive/candidates/c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.md", "scripts/build_c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.py"], FAIL_CANDIDATE_MISSING),
        (C1_COMMIT, [SCHEMA_CONTRACT, "docs/matrixlabs/validator_archive/validator_archive_entry_schema_contract_v0.md", "scripts/build_validator_archive_entry_schema_contract_v0.py"], FAIL_CANDIDATE_MISSING),
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


def expected_scope() -> dict[str, str]:
    return {
        "candidate_entry_id": CANDIDATE_ID,
        "allowed_current_authority_state": AUTHORITY_STATE,
        "allowed_requested_action": REQUESTED_ACTION,
        "allowed_requested_action_scope": REQUESTED_SCOPE,
        "allowed_basis_scope": BASIS_SCOPE,
        "allowed_source_object_id": SOURCE_OBJECT_ID,
        "allowed_output_kind": OUTPUT_KIND,
        "radius": RADIUS_POLICY,
    }


def validate_sources(
    receipt: dict[str, Any],
    surface: dict[str, Any],
    candidate: dict[str, Any],
    audit: dict[str, Any],
    contract: dict[str, Any],
) -> dict[str, str]:
    expect(receipt.get("promotion_decision_receipt_id"), RECEIPT_ID, FAIL_RECEIPT_MISSING, "promotion_decision_receipt_id")
    expect(receipt.get("receipt_status"), RECEIPT_STATUS, FAIL_RECEIPT_NOT_PASS, "receipt_status")
    expect(receipt.get("promotion_decision_receipt_gate"), RECEIPT_GATE, FAIL_RECEIPT_NOT_PASS, "promotion_decision_receipt_gate")
    event = receipt.get("decision_event", {})
    expect(event.get("selected_promotion_option"), SELECTED_OPTION, FAIL_SELECTED_OPTION_NOT_ACTIVE_BRANCH, "selected_promotion_option")
    expect(event.get("selected_option_present_on_surface"), True, FAIL_SELECTED_OPTION_NOT_ON_SURFACE, "selected_option_present_on_surface")
    expect(event.get("decision_actor_class"), DECISION_ACTOR_CLASS, FAIL_RECEIPT_NOT_PASS, "decision_actor_class")
    expect(event.get("selection_source"), SELECTION_SOURCE, FAIL_RECEIPT_NOT_PASS, "selection_source")
    boundary = receipt.get("application_boundary", {})
    expect(boundary.get("promotion_decision_recorded_by_this_receipt"), True, FAIL_RECEIPT_NOT_PASS, "promotion_decision_recorded_by_this_receipt")
    expect(boundary.get("requires_active_archive_entry_materialization"), True, FAIL_RECEIPT_NOT_PASS, "requires_active_archive_entry_materialization")
    expect(boundary.get("next_required_object"), "c8_n22_prepare_next_unit_definition_active_archive_entry_v0", FAIL_RECEIPT_NOT_PASS, "next_required_object")
    expect(receipt.get("terminal_transition"), "ADVANCE(D3_ARCHIVE_ENTRY_STATE_MATERIALIZATION_PENDING)", FAIL_RECEIPT_NOT_PASS, "receipt.terminal_transition")

    expect(surface.get("promotion_decision_surface_id"), SURFACE_ID, FAIL_SELECTED_OPTION_NOT_ON_SURFACE, "promotion_decision_surface_id")
    expect(surface.get("surface_status"), SURFACE_STATUS, FAIL_SELECTED_OPTION_NOT_ON_SURFACE, "surface_status")
    options = surface.get("decision_options", [])
    if not any(option.get("decision_option_id") == SELECTED_OPTION for option in options):
        fail(FAIL_SELECTED_OPTION_NOT_ON_SURFACE, SELECTED_OPTION)

    expect(candidate.get("archive_entry_id"), CANDIDATE_ID, FAIL_CANDIDATE_MISSING, "archive_entry_id")
    expect(candidate.get("archive_entry_status"), CANDIDATE_STATUS, FAIL_CANDIDATE_MISSING, "archive_entry_status")
    expect(audit.get("audit_id"), AUDIT_ID, FAIL_CANDIDATE_AUDIT_MISSING, "audit_id")
    expect(audit.get("audit_result", {}).get("candidate_audit_status"), AUDIT_STATUS, FAIL_CANDIDATE_AUDIT_NOT_PASS, "candidate_audit_status")
    expect(contract.get("archive_schema_contract_id"), CONTRACT_ID, FAIL_CANDIDATE_MISSING, "archive_schema_contract_id")

    scope = dict(receipt.get("selected_option_scope_copied_from_surface", {}))
    for key, wanted in expected_scope().items():
        code = FAIL_RADIUS_MISMATCH if key == "radius" else FAIL_SCOPE_MISMATCH
        expect(scope.get(key), wanted, code, key)
    scope_text = json.dumps(scope, sort_keys=True)
    for term in FORBIDDEN_SCOPE_TERMS:
        if term in scope_text:
            fail(FAIL_SCOPE_MISMATCH, term)
    expect(receipt.get("receipt_gate", {}).get("selected_option_scope_matches_surface"), True, FAIL_SCOPE_MISMATCH, "selected_option_scope_matches_surface")
    expect(scope.get("radius"), RADIUS_POLICY, FAIL_RADIUS_MISMATCH, "radius")
    return scope


def materialized_archive_entry_state() -> dict[str, object]:
    return {
        "archive_entry_status": ACTIVE_ARCHIVE_ENTRY_STATUS,
        "promotion_status": PROMOTION_STATUS,
        "reuse_authority_status": REUSE_AUTHORITY_STATUS,
        "activation_status": ACTIVATION_STATUS,
        "active_archive_entry_created": True,
        "active_archive_entry_id": ACTIVE_ENTRY_ID,
        "reuse_authority_scope": "DECLARED_SCOPE_ONLY",
        "activation_scope": "DECLARED_SCOPE_ONLY",
        "machine_action_scope": "PREPARE_SURFACE_ONLY",
        "runner_authority_created": False,
        "general_reuse_authority_created": False,
        "scope_expanded": False,
    }


def radius_state() -> dict[str, object]:
    return {
        "radius_policy": RADIUS_POLICY,
        "radius_initial_count": 1,
        "radius_remaining_after_d3": 1,
        "radius_consumed_by_d3": 0,
        "radius_consumed_by_this_materialization": False,
        "radius_available_for_d4": True,
        "radius_consumer_next_unit": D4_NEXT_UNIT,
    }


def materialization_effects() -> dict[str, object]:
    return {
        "active_archive_entry_created_by_this_materialization": True,
        "promotion_status_applied_by_this_materialization": True,
        "reuse_authority_status_applied_by_this_materialization": True,
        "activation_status_applied_by_this_materialization": True,
        "machine_proceed_performed_by_this_materialization": False,
        "next_unit_definition_surface_prepared_by_this_materialization": False,
        "unit_executed_by_this_materialization": False,
        "runner_authority_created_by_this_materialization": False,
        "runtime_executed_by_this_materialization": False,
        "observed_path_updated_by_this_materialization": False,
        "receipt_rewritten_by_this_materialization": False,
        "candidate_rewritten_by_this_materialization": False,
        "scope_expanded_by_this_materialization": False,
        "radius_consumed_by_this_materialization": False,
        "activation_object_created_by_this_materialization": False,
    }


def build_record(root: Path) -> dict[str, Any]:
    verify_expected_commits(root)
    receipt = load_json(root, PROMOTION_RECEIPT, FAIL_RECEIPT_MISSING)
    surface = load_json(root, PROMOTION_SURFACE, FAIL_SELECTED_OPTION_NOT_ON_SURFACE)
    candidate = load_json(root, CANDIDATE_ENTRY, FAIL_CANDIDATE_MISSING)
    audit = load_json(root, CANDIDATE_AUDIT, FAIL_CANDIDATE_AUDIT_MISSING)
    contract = load_json(root, SCHEMA_CONTRACT, FAIL_CANDIDATE_MISSING)
    scope = validate_sources(receipt, surface, candidate, audit, contract)
    state = materialized_archive_entry_state()
    radius = radius_state()
    effects = materialization_effects()
    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "materialization_id": MATERIALIZATION_ID,
        "active_archive_entry_id": ACTIVE_ENTRY_ID,
        "materialization_role": MATERIALIZATION_ROLE,
        "materialization_status": MATERIALIZATION_STATUS,
        "block_id": BLOCK_ID,
        "block_unit_id": BLOCK_UNIT_ID,
        "generated_by": GENERATOR,
        "source_chain": {
            "promotion_decision_receipt_id": receipt["promotion_decision_receipt_id"],
            "promotion_decision_receipt_status": receipt["receipt_status"],
            "promotion_decision_receipt_gate": receipt["promotion_decision_receipt_gate"],
            "promotion_decision_surface_id": surface["promotion_decision_surface_id"],
            "promotion_decision_surface_status": surface["surface_status"],
            "candidate_entry_id": candidate["archive_entry_id"],
            "candidate_entry_status": candidate["archive_entry_status"],
            "candidate_audit_id": audit["audit_id"],
            "candidate_audit_status": audit["audit_result"]["candidate_audit_status"],
            "archive_schema_contract_id": contract["archive_schema_contract_id"],
            "source_chain_complete": True,
        },
        "selected_decision_applied": {
            "decision_actor_class": receipt["decision_event"]["decision_actor_class"],
            "selection_source": receipt["decision_event"]["selection_source"],
            "selected_promotion_option": receipt["decision_event"]["selected_promotion_option"],
            "selected_option_present_on_surface": receipt["decision_event"]["selected_option_present_on_surface"],
            "selected_option_scope_matches_surface": True,
            "promotion_decision_recorded_by_d2": True,
            "selected_option_applied_by_this_materialization": True,
        },
        "materialized_scope": scope,
        "materialized_archive_entry_state": state,
        "radius_state": radius,
        "materialization_effects": effects,
        "d4_eligibility_after_d3": {
            "active_archive_entry_exists": True,
            "active_archive_entry_id": ACTIVE_ENTRY_ID,
            "radius_available": True,
            "radius_remaining": 1,
            "allowed_d4_action": REQUESTED_ACTION,
            "allowed_d4_action_scope": REQUESTED_SCOPE,
            "allowed_d4_basis_scope": BASIS_SCOPE,
            "allowed_d4_source_object_id": SOURCE_OBJECT_ID,
            "machine_proceed_performed_by_d3": False,
            "d4_must_run_as_separate_unit": True,
        },
        "materialization_gate": {
            "active_archive_entry_materialization_gate": MATERIALIZATION_STATUS,
            "promotion_decision_receipt_present": True,
            "promotion_decision_receipt_gate": RECEIPT_GATE,
            "selected_promotion_option": SELECTED_OPTION,
            "selected_option_present_on_surface": True,
            "selected_option_scope_matches_surface": True,
            "selected_option_is_active_branch": True,
            "candidate_entry_present": True,
            "candidate_audit_present": True,
            "candidate_audit_status": AUDIT_STATUS,
            "scope_matches_d2_receipt": True,
            "scope_matches_d1_surface": True,
            "radius_declared": True,
            "radius_policy": RADIUS_POLICY,
            "radius_initial_count": 1,
            "radius_remaining_after_d3": 1,
            "radius_consumed_by_d3": 0,
            "active_archive_entry_created_by_this_materialization": True,
            "promotion_status_applied_by_this_materialization": True,
            "reuse_authority_status_applied_by_this_materialization": True,
            "activation_status_applied_by_this_materialization": True,
            "machine_proceed_performed_by_this_materialization": False,
            "next_unit_definition_surface_prepared_by_this_materialization": False,
            "runner_authority_created_by_this_materialization": False,
            "observed_path_updated_by_this_materialization": False,
            "scope_expanded_by_this_materialization": False,
            "radius_consumed_by_this_materialization": False,
            "failures": [],
        },
        "precommit_c8_n22_active_archive_entry_materialization_gate": PRECOMMIT_GATE,
        "active_archive_entry_materialization_gate": MATERIALIZATION_STATUS,
        "failure_vocabulary": FAILURE_VOCABULARY,
        "non_claims": [
            "D.3 does not perform machine proceed.",
            "D.3 does not prepare the next bounded unit definition surface.",
            "D.3 does not execute a unit.",
            "D.3 does not create runner authority.",
            "D.3 does not run runtime.",
            "D.3 does not update observed path.",
            "D.3 does not rewrite the promotion decision receipt.",
            "D.3 does not rewrite the candidate archive entry.",
            "D.3 does not expand candidate scope.",
            "D.3 does not consume radius.",
            "D.3 only materializes the selected active archive-entry state from D.2.",
            "active archive entry ≠ machine proceed performed",
            "activation active ≠ runner activated",
            "radius available ≠ radius consumed",
            "reuse authority granted for declared scope ≠ global reuse authority",
        ],
        "key_non_claims": [
            "active archive entry ≠ machine proceed performed",
            "activation active ≠ runner activated",
            "radius available ≠ radius consumed",
            "reuse authority granted for declared scope ≠ global reuse authority",
        ],
        "unsafe_to_infer": [
            "Unsafe to infer: D.4 has already run.",
            "Unsafe to infer: the next bounded unit definition surface exists.",
            "Unsafe to infer: radius was consumed.",
            "Unsafe to infer: runner authority exists.",
            "Unsafe to infer: reuse authority is global.",
        ],
        "terminal_transition": TERMINAL_TRANSITION,
    }
    validate_record(record)
    return record


def validate_record(record: dict[str, Any]) -> None:
    effects = record["materialization_effects"]
    false_checks = {
        "machine_proceed_performed_by_this_materialization": FAIL_MACHINE_PROCEED,
        "next_unit_definition_surface_prepared_by_this_materialization": FAIL_NEXT_UNIT_SURFACE,
        "unit_executed_by_this_materialization": FAIL_MACHINE_PROCEED,
        "runner_authority_created_by_this_materialization": FAIL_RUNNER_AUTHORITY,
        "runtime_executed_by_this_materialization": FAIL_MACHINE_PROCEED,
        "observed_path_updated_by_this_materialization": FAIL_OBSERVED_PATH,
        "receipt_rewritten_by_this_materialization": FAIL_RECEIPT_REWRITTEN,
        "candidate_rewritten_by_this_materialization": FAIL_RECEIPT_REWRITTEN,
        "scope_expanded_by_this_materialization": FAIL_SCOPE_EXPANDED,
        "radius_consumed_by_this_materialization": FAIL_RADIUS_CONSUMED,
        "activation_object_created_by_this_materialization": FAIL_MACHINE_PROCEED,
    }
    for field, code in false_checks.items():
        expect(effects.get(field), False, code, field)
    radius = record["radius_state"]
    expect(radius.get("radius_initial_count"), 1, FAIL_RADIUS_MISSING, "radius_initial_count")
    expect(radius.get("radius_remaining_after_d3"), 1, FAIL_RADIUS_CONSUMED, "radius_remaining_after_d3")
    expect(radius.get("radius_consumed_by_d3"), 0, FAIL_RADIUS_CONSUMED, "radius_consumed_by_d3")
    gate = record["materialization_gate"]
    expect(gate.get("active_archive_entry_materialization_gate"), MATERIALIZATION_STATUS, FAIL_FORBIDDEN_EFFECTS_MISSING, "materialization_gate")
    expect(gate.get("failures"), [], FAIL_FORBIDDEN_EFFECTS_MISSING, "failures")
    for field in [
        "machine_proceed_performed_by_this_materialization",
        "next_unit_definition_surface_prepared_by_this_materialization",
        "runner_authority_created_by_this_materialization",
        "observed_path_updated_by_this_materialization",
        "scope_expanded_by_this_materialization",
        "radius_consumed_by_this_materialization",
    ]:
        expect(gate.get(field), False, false_checks.get(field, FAIL_FORBIDDEN_EFFECTS_MISSING), f"gate.{field}")


def validate_no_forbidden_files(root: Path) -> None:
    forbidden = [
        "docs/matrixlabs/validator_archive/promoted",
        "docs/matrixlabs/validator_archive/promotion/c8_n22_machine_proceed_under_active_entry_v0.json",
        "docs/matrixlabs/validator_archive/promotion/c8_n22_machine_proceed_under_active_entry_v0.md",
        "docs/matrixlabs/next_units/c8_n22_next_bounded_unit_v0.json",
        "docs/matrixlabs/next_units/c8_n22_next_bounded_unit_v0.md",
        "docs/matrixlabs/observability/c8_observed_decision_path_update_d3_proposal_v0.json",
        "docs/matrixlabs/runners/c8_n22_runner_v0.json",
        "scripts/build_c8_n22_machine_proceed_under_active_entry_v0.py",
    ]
    existing = [path for path in forbidden if (root / path).exists()]
    if existing:
        fail(FAIL_MACHINE_PROCEED, ",".join(existing))


def render_markdown(record: dict[str, Any]) -> str:
    state = record["materialized_archive_entry_state"]
    scope = record["materialized_scope"]
    radius = record["radius_state"]
    return "\n".join(
        [
            "# C8 n22 prepare-next-unit active archive entry v0",
            "",
            "## Status",
            "",
            record["active_archive_entry_materialization_gate"],
            "",
            "## Active archive entry",
            "",
            record["active_archive_entry_id"],
            "",
            "## Source promotion decision receipt",
            "",
            record["source_chain"]["promotion_decision_receipt_id"],
            "",
            "## Selected promotion option",
            "",
            record["selected_decision_applied"]["selected_promotion_option"],
            "",
            "## Materialized archive-entry state",
            "",
            f"- archive entry status: {state['archive_entry_status']}",
            f"- promotion status: {state['promotion_status']}",
            f"- reuse authority: {state['reuse_authority_status']}",
            f"- activation: {state['activation_status']}",
            "",
            "## Declared scope",
            "",
            f"- authority state: {scope['allowed_current_authority_state']}",
            f"- requested action: {scope['allowed_requested_action']}",
            f"- requested scope: {scope['allowed_requested_action_scope']}",
            f"- basis scope: {scope['allowed_basis_scope']}",
            f"- source object: {scope['allowed_source_object_id']}",
            f"- output kind: {scope['allowed_output_kind']}",
            f"- radius: {scope['radius']}",
            "",
            "## Radius state",
            "",
            f"- initial radius: {radius['radius_initial_count']}",
            f"- radius remaining after D.3: {radius['radius_remaining_after_d3']}",
            f"- radius use by D.3: {radius['radius_consumed_by_d3']}",
            "",
            "## Not performed by D.3",
            "",
            "- no machine proceed performed",
            "- no next bounded unit definition surface prepared",
            "- no unit executed",
            "- no runner authority created",
            "- no runtime executed",
            "- no observed path updated",
            "- no receipt rewritten",
            "- no candidate rewritten",
            "- no scope expanded",
            "- no radius use by D.3",
            "",
            "## Next required object",
            "",
            D4_NEXT_UNIT,
            "",
            "D4 must run as a separate unit.",
        ]
    ).rstrip() + "\n"


def validate_markdown(record: dict[str, Any], markdown: str) -> None:
    required = [
        "# C8 n22 prepare-next-unit active archive entry v0",
        MATERIALIZATION_STATUS,
        ACTIVE_ENTRY_ID,
        RECEIPT_ID,
        SELECTED_OPTION,
        "- archive entry status: ARCHIVE_STATUS_PREAPPROVED_ACTIVE",
        "- promotion status: PROMOTION_GRANTED_FOR_DECLARED_SCOPE",
        "- reuse authority: REUSE_AUTHORITY_GRANTED_FOR_DECLARED_SCOPE",
        "- activation: ACTIVATION_ACTIVE",
        f"- authority state: {AUTHORITY_STATE}",
        f"- requested action: {REQUESTED_ACTION}",
        f"- requested scope: {REQUESTED_SCOPE}",
        f"- basis scope: {BASIS_SCOPE}",
        f"- source object: {SOURCE_OBJECT_ID}",
        f"- output kind: {OUTPUT_KIND}",
        f"- radius: {RADIUS_POLICY}",
        "- initial radius: 1",
        "- radius remaining after D.3: 1",
        "- radius use by D.3: 0",
        "- no machine proceed performed",
        "- no next bounded unit definition surface prepared",
        "- no unit executed",
        "- no runner authority created",
        "- no runtime executed",
        "- no observed path updated",
        "- no receipt rewritten",
        "- no candidate rewritten",
        "- no scope expanded",
        "- no radius use by D.3",
        D4_NEXT_UNIT,
    ]
    missing = [phrase for phrase in required if phrase not in markdown]
    if missing:
        fail(FAIL_MARKDOWN_JSON_PARITY, str(missing))
    lower = markdown.lower()
    for phrase in ["machine proceeded", "next unit prepared", "ready to run", "runner active", "global reuse"]:
        if phrase in lower:
            fail(FAIL_MARKDOWN_JSON_PARITY, phrase)


def write_outputs(root: Path, record: dict[str, Any]) -> None:
    validate_no_forbidden_files(root)
    markdown = render_markdown(record)
    validate_markdown(record, markdown)
    out_json = root / OUTPUT_JSON
    out_md = root / OUTPUT_MD
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    out_md.write_text(markdown, encoding="utf-8")


def print_success(record: dict[str, Any]) -> None:
    chain = record["source_chain"]
    selected = record["selected_decision_applied"]
    state = record["materialized_archive_entry_state"]
    effects = record["materialization_effects"]
    radius = record["radius_state"]
    d4 = record["d4_eligibility_after_d3"]
    print("BUILD_C8_N22_PREPARE_NEXT_UNIT_DEFINITION_ACTIVE_ARCHIVE_ENTRY_V0_COMPLETE")
    print(f"materialization_id={record['materialization_id']}")
    print(f"active_archive_entry_id={record['active_archive_entry_id']}")
    print(f"schema_version={record['schema_version']}")
    print(f"materialization_role={record['materialization_role']}")
    print(f"materialization_status={record['materialization_status']}")
    print(f"block_id={record['block_id']}")
    print(f"block_unit_id={record['block_unit_id']}")
    print(f"promotion_decision_receipt_id={chain['promotion_decision_receipt_id']}")
    print(f"promotion_decision_receipt_gate={chain['promotion_decision_receipt_gate']}")
    print(f"promotion_decision_surface_id={chain['promotion_decision_surface_id']}")
    print(f"candidate_entry_id={chain['candidate_entry_id']}")
    print(f"candidate_audit_id={chain['candidate_audit_id']}")
    print(f"candidate_audit_status={chain['candidate_audit_status']}")
    print(f"decision_actor_class={selected['decision_actor_class']}")
    print(f"selection_source={selected['selection_source']}")
    print(f"selected_promotion_option={selected['selected_promotion_option']}")
    print(f"selected_option_present_on_surface={bool_text(selected['selected_option_present_on_surface'])}")
    print(f"selected_option_scope_matches_surface={bool_text(selected['selected_option_scope_matches_surface'])}")
    print(f"selected_option_applied_by_this_materialization={bool_text(selected['selected_option_applied_by_this_materialization'])}")
    print(f"archive_entry_status={state['archive_entry_status']}")
    print(f"promotion_status={state['promotion_status']}")
    print(f"reuse_authority_status={state['reuse_authority_status']}")
    print(f"activation_status={state['activation_status']}")
    print(f"reuse_authority_scope={state['reuse_authority_scope']}")
    print(f"activation_scope={state['activation_scope']}")
    print(f"machine_action_scope={state['machine_action_scope']}")
    for key in [
        "active_archive_entry_created_by_this_materialization",
        "promotion_status_applied_by_this_materialization",
        "reuse_authority_status_applied_by_this_materialization",
        "activation_status_applied_by_this_materialization",
    ]:
        print(f"{key}={bool_text(effects[key])}")
    print(f"materialized_scope_radius={record['materialized_scope']['radius']}")
    print(f"radius_initial_count={radius['radius_initial_count']}")
    print(f"radius_remaining_after_d3={radius['radius_remaining_after_d3']}")
    print(f"radius_consumed_by_d3={radius['radius_consumed_by_d3']}")
    print(f"radius_available_for_d4={bool_text(radius['radius_available_for_d4'])}")
    for key in [
        "machine_proceed_performed_by_this_materialization",
        "next_unit_definition_surface_prepared_by_this_materialization",
        "unit_executed_by_this_materialization",
        "runner_authority_created_by_this_materialization",
        "runtime_executed_by_this_materialization",
        "observed_path_updated_by_this_materialization",
        "receipt_rewritten_by_this_materialization",
        "candidate_rewritten_by_this_materialization",
        "scope_expanded_by_this_materialization",
        "radius_consumed_by_this_materialization",
        "activation_object_created_by_this_materialization",
    ]:
        print(f"{key}={bool_text(effects[key])}")
    print(f"d4_eligibility_active_entry_exists={bool_text(d4['active_archive_entry_exists'])}")
    print(f"d4_eligibility_radius_available={bool_text(d4['radius_available'])}")
    print(f"d4_eligibility_radius_remaining={d4['radius_remaining']}")
    print(f"d4_must_run_as_separate_unit={bool_text(d4['d4_must_run_as_separate_unit'])}")
    print(f"active_archive_entry_materialization_gate={record['active_archive_entry_materialization_gate']}")
    print(f"precommit_c8_n22_active_archive_entry_materialization_gate={record['precommit_c8_n22_active_archive_entry_materialization_gate']}")
    print("next_unit_defined=false")
    print("next_unit_authorized=false")
    print("observed_path_updated=false")
    print("observed_path_update_proposed=false")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition={record['terminal_transition']}")


def main() -> int:
    try:
        root = detect_repo_root(Path.cwd())
        record = build_record(root)
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
