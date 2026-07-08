#!/usr/bin/env python3
"""Build C8 n22 candidate promotion decision surface v0.

This surface presents typed human promotion options for the C.2 candidate after
the C.3 admissibility audit. It does not select, record, apply, promote,
activate, authorize reuse, or perform machine proceed.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_candidate_promotion_decision_surface_v0.py"
OUTPUT_JSON = "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_surface_v0.json"
OUTPUT_MD = "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_surface_v0.md"

SCHEMA_CONTRACT = "docs/matrixlabs/validator_archive/validator_archive_entry_schema_contract_v0.json"
CANDIDATE_ENTRY = "docs/matrixlabs/validator_archive/candidates/c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.json"
CANDIDATE_AUDIT = "docs/matrixlabs/validator_archive/audits/c8_n22_candidate_archive_entry_admissibility_audit_v0.json"

C1_COMMIT = "96223d2a9827543c27f93a1c0a16a6670a97de71"
C2_COMMIT = "674c601136f381c9d85605f646900998b24ddfe9"
C3_COMMIT = "f49dfab97774414330682151e6e3fffeb7ba6f66"

SCHEMA_VERSION = "matrixlabs_human_promotion_decision_surface_v0"
SURFACE_ID = "c8.n22.candidate_promotion_decision_surface.v0"
SURFACE_ROLE = "HUMAN_PROMOTION_DECISION_SURFACE"
SURFACE_STATUS = "PROMOTION_DECISION_SURFACE_PRESENTS_TYPED_OPTIONS_ONLY"
BLOCK_ID = "BLOCK_D"
BLOCK_UNIT_ID = "D1_CANDIDATE_PROMOTION_DECISION_SURFACE"
SURFACE_GATE = "PROMOTION_DECISION_SURFACE_PASS_OPTIONS_PRESENTED_ONLY"
PRECOMMIT_GATE = "PASS"
TERMINAL_TRANSITION = "ADVANCE(D2_HUMAN_PROMOTION_DECISION_RECEIPT_PENDING)"

CONTRACT_ID = "validator_archive_entry_schema_contract.v0"
CONTRACT_SCHEMA_VERSION = "matrixlabs_validator_archive_entry_schema_contract_v0"
CONTRACT_ROLE = "ARCHIVE_ENTRY_CONTRACT_ONLY"

CANDIDATE_ID = "candidate.c8.n22.prepare_next_unit_definition_surface.v0"
CANDIDATE_SCHEMA_VERSION = "matrixlabs_validator_archive_candidate_entry_v0"
CANDIDATE_AUDIT_ID = "c8.n22.candidate_archive_entry.admissibility_audit.v0"
CANDIDATE_AUDIT_SCHEMA_VERSION = "matrixlabs_validator_archive_candidate_audit_v0"
CANDIDATE_AUDIT_STATUS = "CANDIDATE_AUDIT_PASS_CONTRACT_CONFORMANT_NOT_PROMOTED"
ARCHIVE_ENTRY_STATUS = "ARCHIVE_STATUS_CANDIDATE"
PROMOTION_STATUS_BEFORE = "PROMOTION_NOT_REQUESTED"
REUSE_AUTHORITY_STATUS_BEFORE = "REUSE_AUTHORITY_NOT_GRANTED"
ACTIVATION_STATUS_BEFORE = "ACTIVATION_NOT_APPLICABLE"
ACTIVATION_STATUS_REASON_BEFORE = "CANDIDATE_ENTRY_NOT_ACTIVATABLE"
ACTIVE_ARCHIVE_ENTRY_STATUS_BEFORE = "NO_ACTIVE_ARCHIVE_ENTRY_CREATED"

AUTHORITY_STATE = "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION"
REQUESTED_ACTION = "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"
REQUESTED_SCOPE = "PREPARE_SURFACE_ONLY"
BASIS_SCOPE = "C8_N22_BASIS_ONLY"
SOURCE_OBJECT_ID = "c8.n22"
OUTPUT_KIND = "NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"
POSITIVE_RADIUS = "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT"

OPTION_PROMOTE_ACTIVE = "DECISION_PROMOTE_CANDIDATE_FOR_DECLARED_SCOPE"
OPTION_PROMOTE_INACTIVE = "DECISION_PROMOTE_CANDIDATE_INACTIVE_ONLY"
OPTION_REVISION = "DECISION_REQUEST_CANDIDATE_REVISION"
OPTION_DEFER = "DECISION_DEFER_PROMOTION"
OPTION_REJECT = "DECISION_REJECT_CANDIDATE_PROMOTION"
OPTION_IDS = [
    OPTION_PROMOTE_ACTIVE,
    OPTION_PROMOTE_INACTIVE,
    OPTION_REVISION,
    OPTION_DEFER,
    OPTION_REJECT,
]

FAIL_ARCHIVE_SCHEMA_CONTRACT_MISSING = "PROMOTION_SURFACE_FAIL_ARCHIVE_SCHEMA_CONTRACT_MISSING"
FAIL_CANDIDATE_MISSING = "PROMOTION_SURFACE_FAIL_CANDIDATE_MISSING"
FAIL_CANDIDATE_AUDIT_MISSING = "PROMOTION_SURFACE_FAIL_CANDIDATE_AUDIT_MISSING"
FAIL_CANDIDATE_AUDIT_NOT_PASS = "PROMOTION_SURFACE_FAIL_CANDIDATE_AUDIT_NOT_PASS"
FAIL_CANDIDATE_NOT_CANDIDATE = "PROMOTION_SURFACE_FAIL_CANDIDATE_NOT_CANDIDATE"
FAIL_CANDIDATE_ALREADY_PROMOTED = "PROMOTION_SURFACE_FAIL_CANDIDATE_ALREADY_PROMOTED"
FAIL_REUSE_ALREADY_AUTHORIZED = "PROMOTION_SURFACE_FAIL_REUSE_ALREADY_AUTHORIZED"
FAIL_DECISION_OPTIONS_MISSING = "PROMOTION_SURFACE_FAIL_DECISION_OPTIONS_MISSING"
FAIL_POSITIVE_OPTION_MISSING = "PROMOTION_SURFACE_FAIL_POSITIVE_OPTION_MISSING"
FAIL_SCOPE_OVERBROAD = "PROMOTION_SURFACE_FAIL_SCOPE_OVERBROAD"
FAIL_RADIUS_OVERBROAD = "PROMOTION_SURFACE_FAIL_RADIUS_OVERBROAD"
FAIL_OPTION_EFFECT_UNTYPED = "PROMOTION_SURFACE_FAIL_OPTION_EFFECT_UNTYPED"
FAIL_PROMOTION_GRANTED_INSIDE_SURFACE = "PROMOTION_SURFACE_FAIL_PROMOTION_GRANTED_INSIDE_SURFACE"
FAIL_REUSE_GRANTED_INSIDE_SURFACE = "PROMOTION_SURFACE_FAIL_REUSE_GRANTED_INSIDE_SURFACE"
FAIL_ACTIVE_ENTRY_CREATED_INSIDE_SURFACE = "PROMOTION_SURFACE_FAIL_ACTIVE_ENTRY_CREATED_INSIDE_SURFACE"
FAIL_MACHINE_PROCEED_INSIDE_SURFACE = "PROMOTION_SURFACE_FAIL_MACHINE_PROCEED_INSIDE_SURFACE"
FAIL_AUTHORITY_CHANGED_INSIDE_SURFACE = "PROMOTION_SURFACE_FAIL_AUTHORITY_CHANGED_INSIDE_SURFACE"
FAIL_RUNNER_AUTHORITY_CREATED = "PROMOTION_SURFACE_FAIL_RUNNER_AUTHORITY_CREATED"
FAIL_MARKDOWN_JSON_PARITY = "PROMOTION_SURFACE_FAIL_MARKDOWN_JSON_PARITY"

FAILURE_VOCABULARY = [
    FAIL_ARCHIVE_SCHEMA_CONTRACT_MISSING,
    FAIL_CANDIDATE_MISSING,
    FAIL_CANDIDATE_AUDIT_MISSING,
    FAIL_CANDIDATE_AUDIT_NOT_PASS,
    FAIL_CANDIDATE_NOT_CANDIDATE,
    FAIL_CANDIDATE_ALREADY_PROMOTED,
    FAIL_REUSE_ALREADY_AUTHORIZED,
    FAIL_DECISION_OPTIONS_MISSING,
    FAIL_POSITIVE_OPTION_MISSING,
    FAIL_SCOPE_OVERBROAD,
    FAIL_RADIUS_OVERBROAD,
    FAIL_OPTION_EFFECT_UNTYPED,
    FAIL_PROMOTION_GRANTED_INSIDE_SURFACE,
    FAIL_REUSE_GRANTED_INSIDE_SURFACE,
    FAIL_ACTIVE_ENTRY_CREATED_INSIDE_SURFACE,
    FAIL_MACHINE_PROCEED_INSIDE_SURFACE,
    FAIL_AUTHORITY_CHANGED_INSIDE_SURFACE,
    FAIL_RUNNER_AUTHORITY_CREATED,
]

FORBIDDEN_MARKDOWN_PHRASES = [
    "ready to run",
    "safe to use",
    "machine may proceed",
    "activated",
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
        fail(FAIL_ARCHIVE_SCHEMA_CONTRACT_MISSING, proc.stderr.strip())
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
        (C1_COMMIT, [SCHEMA_CONTRACT, "docs/matrixlabs/validator_archive/validator_archive_entry_schema_contract_v0.md", "scripts/build_validator_archive_entry_schema_contract_v0.py"], FAIL_ARCHIVE_SCHEMA_CONTRACT_MISSING),
        (C2_COMMIT, [CANDIDATE_ENTRY, "docs/matrixlabs/validator_archive/candidates/c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.md", "scripts/build_c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.py"], FAIL_CANDIDATE_MISSING),
        (C3_COMMIT, [CANDIDATE_AUDIT, "docs/matrixlabs/validator_archive/audits/c8_n22_candidate_archive_entry_admissibility_audit_v0.md", "scripts/build_c8_n22_candidate_archive_entry_admissibility_audit_v0.py"], FAIL_CANDIDATE_AUDIT_MISSING),
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


def validate_contract(contract: dict[str, Any]) -> None:
    expect(contract.get("archive_schema_contract_id"), CONTRACT_ID, FAIL_ARCHIVE_SCHEMA_CONTRACT_MISSING, "archive_schema_contract_id")
    expect(contract.get("schema_version"), CONTRACT_SCHEMA_VERSION, FAIL_ARCHIVE_SCHEMA_CONTRACT_MISSING, "contract.schema_version")
    expect(contract.get("contract_role"), CONTRACT_ROLE, FAIL_ARCHIVE_SCHEMA_CONTRACT_MISSING, "contract_role")


def validate_candidate(candidate: dict[str, Any]) -> None:
    expect(candidate.get("schema_version"), CANDIDATE_SCHEMA_VERSION, FAIL_CANDIDATE_MISSING, "candidate.schema_version")
    expect(candidate.get("archive_entry_id"), CANDIDATE_ID, FAIL_CANDIDATE_MISSING, "archive_entry_id")
    expect(candidate.get("archive_entry_status"), ARCHIVE_ENTRY_STATUS, FAIL_CANDIDATE_NOT_CANDIDATE, "archive_entry_status")
    expect(candidate.get("promotion_status"), PROMOTION_STATUS_BEFORE, FAIL_CANDIDATE_ALREADY_PROMOTED, "promotion_status")
    expect(candidate.get("reuse_authority_status"), REUSE_AUTHORITY_STATUS_BEFORE, FAIL_REUSE_ALREADY_AUTHORIZED, "reuse_authority_status")
    expect(candidate.get("activation_status"), ACTIVATION_STATUS_BEFORE, FAIL_CANDIDATE_NOT_CANDIDATE, "activation_status")
    expect(candidate.get("activation_status_reason"), ACTIVATION_STATUS_REASON_BEFORE, FAIL_CANDIDATE_NOT_CANDIDATE, "activation_status_reason")
    expect(candidate.get("active_archive_entry_status"), ACTIVE_ARCHIVE_ENTRY_STATUS_BEFORE, FAIL_ACTIVE_ENTRY_CREATED_INSIDE_SURFACE, "active_archive_entry_status")
    move = candidate.get("candidate_move_shape", {})
    expect(move.get("allowed_current_authority_state"), AUTHORITY_STATE, FAIL_SCOPE_OVERBROAD, "allowed_current_authority_state")
    expect(move.get("allowed_requested_action"), REQUESTED_ACTION, FAIL_SCOPE_OVERBROAD, "allowed_requested_action")
    expect(move.get("allowed_requested_action_scope"), REQUESTED_SCOPE, FAIL_SCOPE_OVERBROAD, "allowed_requested_action_scope")
    expect(move.get("allowed_basis_scope"), BASIS_SCOPE, FAIL_SCOPE_OVERBROAD, "allowed_basis_scope")
    expect(move.get("allowed_source_object_id"), SOURCE_OBJECT_ID, FAIL_SCOPE_OVERBROAD, "allowed_source_object_id")
    expect(move.get("allowed_output_kind"), OUTPUT_KIND, FAIL_SCOPE_OVERBROAD, "allowed_output_kind")
    machine = candidate.get("candidate_machine_scope", {})
    expect(machine.get("radius_limit_now"), "RADIUS_0_CANDIDATE_ONLY", FAIL_RADIUS_OVERBROAD, "radius_limit_now")
    expect(machine.get("proposed_radius_limit_if_promoted"), POSITIVE_RADIUS, FAIL_RADIUS_OVERBROAD, "proposed_radius_limit_if_promoted")


def validate_audit(audit: dict[str, Any]) -> None:
    expect(audit.get("schema_version"), CANDIDATE_AUDIT_SCHEMA_VERSION, FAIL_CANDIDATE_AUDIT_MISSING, "audit.schema_version")
    expect(audit.get("audit_id"), CANDIDATE_AUDIT_ID, FAIL_CANDIDATE_AUDIT_MISSING, "audit_id")
    result = audit.get("audit_result", {})
    expect(result.get("candidate_audit_status"), CANDIDATE_AUDIT_STATUS, FAIL_CANDIDATE_AUDIT_NOT_PASS, "candidate_audit_status")
    expect(result.get("candidate_contract_conformant"), True, FAIL_CANDIDATE_AUDIT_NOT_PASS, "candidate_contract_conformant")
    expect(result.get("candidate_promoted"), False, FAIL_CANDIDATE_ALREADY_PROMOTED, "candidate_promoted")
    expect(result.get("candidate_reusable"), False, FAIL_REUSE_ALREADY_AUTHORIZED, "candidate_reusable")
    expect(result.get("candidate_active"), False, FAIL_ACTIVE_ENTRY_CREATED_INSIDE_SURFACE, "candidate_active")
    summary = audit.get("audit_gate_summary", {})
    expect(summary.get("candidate_audit_gate"), CANDIDATE_AUDIT_STATUS, FAIL_CANDIDATE_AUDIT_NOT_PASS, "candidate_audit_gate")
    expect(summary.get("failures"), [], FAIL_CANDIDATE_AUDIT_NOT_PASS, "audit.failures")
    expect(audit.get("terminal_transition"), "STOP_BLOCK_C_CANDIDATE_AUDIT_CLOSED", FAIL_CANDIDATE_AUDIT_NOT_PASS, "audit.terminal_transition")


def surface_non_effects() -> dict[str, bool]:
    return {
        "decision_option_selected_by_this_surface": False,
        "promotion_decision_recorded_by_this_surface": False,
        "promotion_granted_by_this_surface": False,
        "reuse_authority_granted_by_this_surface": False,
        "activation_created_by_this_surface": False,
        "active_archive_entry_created_by_this_surface": False,
        "inactive_archive_entry_created_by_this_surface": False,
        "machine_proceed_performed_by_this_surface": False,
        "next_unit_definition_surface_prepared_by_this_surface": False,
        "authority_changed_by_this_surface": False,
        "runner_authority_created_by_this_surface": False,
    }


def positive_promotion_scope() -> dict[str, str]:
    return {
        "candidate_entry_id": CANDIDATE_ID,
        "allowed_current_authority_state": AUTHORITY_STATE,
        "allowed_requested_action": REQUESTED_ACTION,
        "allowed_requested_action_scope": REQUESTED_SCOPE,
        "allowed_basis_scope": BASIS_SCOPE,
        "allowed_source_object_id": SOURCE_OBJECT_ID,
        "allowed_output_kind": OUTPUT_KIND,
        "radius": POSITIVE_RADIUS,
    }


def decision_options() -> list[dict[str, Any]]:
    return [
        {
            "decision_option_id": OPTION_PROMOTE_ACTIVE,
            "option_kind": "PROMOTION_AUTHORITY_EVENT_REQUIRING_OPTION",
            "required_decision_event_if_selected": "HUMAN_PROMOTION_ACCEPTANCE",
            "promotion_scope": positive_promotion_scope(),
            "effect_if_selected_and_applied_by_d3": {
                "promotion_status": "PROMOTION_GRANTED_FOR_DECLARED_SCOPE",
                "reuse_authority_status": "REUSE_AUTHORITY_GRANTED_FOR_DECLARED_SCOPE",
                "activation_status": "ACTIVATION_ACTIVE",
                "active_archive_entry_may_be_materialized_by_d3": True,
                "machine_proceed_eligible_only_after_d3_materializes_active_entry": True,
            },
            "still_not_authorized": {
                "execute_unit": True,
                "change_authority_state": True,
                "rewrite_receipts": True,
                "promote_taxonomy": True,
                "expand_reuse_scope": True,
                "generalize_updater": True,
                "activate_runner": True,
            },
        },
        {
            "decision_option_id": OPTION_PROMOTE_INACTIVE,
            "option_kind": "PROMOTION_INACTIVE_ONLY_REQUIRING_OPTION",
            "required_decision_event_if_selected": "HUMAN_PROMOTION_ACCEPTANCE",
            "promotion_status_if_applied_by_d3": "PROMOTION_GRANTED_FOR_DECLARED_SCOPE",
            "reuse_authority_status_if_applied_by_d3": "REUSE_AUTHORITY_GRANTED_FOR_DECLARED_SCOPE",
            "activation_status_if_applied_by_d3": "ACTIVATION_INACTIVE",
            "archive_entry_status_if_applied_by_d3": "ARCHIVE_STATUS_PREAPPROVED_INACTIVE",
            "active_archive_entry_may_be_materialized_by_d3": False,
            "inactive_archive_entry_may_be_materialized_by_d3": True,
            "machine_proceed_allowed_if_applied_by_d3": False,
        },
        {
            "decision_option_id": OPTION_REVISION,
            "option_kind": "REVISION_REQUEST_REQUIRING_OPTION",
            "promotion_status_if_applied_by_d3": "PROMOTION_REJECTED",
            "promotion_status_reason_if_applied_by_d3": "REVISION_REQUESTED",
            "reuse_authority_status_if_applied_by_d3": "REUSE_AUTHORITY_NOT_GRANTED",
            "activation_status_if_applied_by_d3": "ACTIVATION_NOT_APPLICABLE",
            "activation_status_reason_if_applied_by_d3": "CANDIDATE_ENTRY_NOT_ACTIVATABLE",
            "next_surface_if_applied": "CANDIDATE_REVISION_SURFACE",
            "machine_proceed_allowed_if_applied_by_d3": False,
        },
        {
            "decision_option_id": OPTION_DEFER,
            "option_kind": "DEFER_PROMOTION_REQUIRING_OPTION",
            "promotion_status_if_applied_by_d3": "PROMOTION_PENDING_HUMAN_DECISION",
            "reuse_authority_status_if_applied_by_d3": "REUSE_AUTHORITY_NOT_GRANTED",
            "activation_status_if_applied_by_d3": "ACTIVATION_NOT_APPLICABLE",
            "activation_status_reason_if_applied_by_d3": "CANDIDATE_ENTRY_NOT_ACTIVATABLE",
            "machine_proceed_allowed_if_applied_by_d3": False,
        },
        {
            "decision_option_id": OPTION_REJECT,
            "option_kind": "REJECT_PROMOTION_REQUIRING_OPTION",
            "promotion_status_if_applied_by_d3": "PROMOTION_REJECTED",
            "reuse_authority_status_if_applied_by_d3": "REUSE_AUTHORITY_NOT_GRANTED",
            "activation_status_if_applied_by_d3": "ACTIVATION_NOT_APPLICABLE",
            "activation_status_reason_if_applied_by_d3": "CANDIDATE_ENTRY_NOT_ACTIVATABLE",
            "active_archive_entry_may_be_materialized_by_d3": False,
            "machine_proceed_allowed_if_applied_by_d3": False,
        },
    ]


def build_record(root: Path) -> dict[str, Any]:
    verify_expected_commits(root)
    contract = load_json(root, SCHEMA_CONTRACT, FAIL_ARCHIVE_SCHEMA_CONTRACT_MISSING)
    candidate = load_json(root, CANDIDATE_ENTRY, FAIL_CANDIDATE_MISSING)
    audit = load_json(root, CANDIDATE_AUDIT, FAIL_CANDIDATE_AUDIT_MISSING)
    validate_contract(contract)
    validate_candidate(candidate)
    validate_audit(audit)
    options = decision_options()
    non_effects = surface_non_effects()
    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "promotion_decision_surface_id": SURFACE_ID,
        "surface_role": SURFACE_ROLE,
        "surface_status": SURFACE_STATUS,
        "block_id": BLOCK_ID,
        "block_unit_id": BLOCK_UNIT_ID,
        "generated_by": GENERATOR,
        "source_contract": {
            "archive_schema_contract_id": contract["archive_schema_contract_id"],
            "schema_version": contract["schema_version"],
            "schema_role": contract["contract_role"],
        },
        "source_candidate": {
            "candidate_entry_id": candidate["archive_entry_id"],
            "candidate_status": candidate["archive_entry_status"],
            "candidate_audit_id": audit["audit_id"],
            "candidate_audit_status": audit["audit_result"]["candidate_audit_status"],
            "candidate_contract_conformant": audit["audit_result"]["candidate_contract_conformant"],
            "candidate_promoted": audit["audit_result"]["candidate_promoted"],
            "candidate_reusable": audit["audit_result"]["candidate_reusable"],
            "candidate_active": audit["audit_result"]["candidate_active"],
        },
        "pre_surface_authority_state": {
            "promotion_status_before": candidate["promotion_status"],
            "reuse_authority_status_before": candidate["reuse_authority_status"],
            "activation_status_before": candidate["activation_status"],
            "activation_status_reason_before": candidate["activation_status_reason"],
            "active_archive_entry_status_before": candidate["active_archive_entry_status"],
            "auto_disposition_allowed_before": False,
            "runner_authority_created_before": False,
            "machine_proceed_authorized_before": False,
        },
        "decision_options": options,
        "surface_non_effects": non_effects,
        "surface_gate": {
            "promotion_decision_surface_gate": SURFACE_GATE,
            "archive_schema_contract_present": True,
            "candidate_entry_present": True,
            "candidate_audit_present": True,
            "candidate_audit_status": CANDIDATE_AUDIT_STATUS,
            "candidate_entry_status": ARCHIVE_ENTRY_STATUS,
            "candidate_promotion_status": PROMOTION_STATUS_BEFORE,
            "candidate_reuse_authority_status": REUSE_AUTHORITY_STATUS_BEFORE,
            "candidate_activation_status": ACTIVATION_STATUS_BEFORE,
            "candidate_activation_status_reason": ACTIVATION_STATUS_REASON_BEFORE,
            "candidate_contract_conformant_not_promoted": True,
            "decision_options_present": True,
            "decision_option_count": 5,
            "positive_option_present": True,
            "positive_option_id": OPTION_PROMOTE_ACTIVE,
            "positive_option_scope_matches_candidate": True,
            "positive_option_radius": POSITIVE_RADIUS,
            "surface_status": SURFACE_STATUS,
            **non_effects,
            "failures": [],
        },
        "precommit_c8_n22_candidate_promotion_decision_surface_gate": PRECOMMIT_GATE,
        "promotion_decision_surface_gate": SURFACE_GATE,
        "failure_vocabulary": FAILURE_VOCABULARY,
        "non_claims": [
            "D.1 does not select a promotion option.",
            "D.1 does not record human promotion acceptance.",
            "D.1 does not promote the candidate.",
            "D.1 does not authorize reuse.",
            "D.1 does not activate an archive entry.",
            "D.1 does not create an active archive entry.",
            "D.1 does not perform machine proceed.",
            "D.1 does not prepare the next bounded unit definition surface.",
            "D.1 does not execute a unit.",
            "D.1 does not change authority state.",
            "D.1 does not expand candidate scope.",
            "D.1 does not create runner authority.",
            "D.1 only presents typed human promotion options.",
            "promotion surface != promotion receipt",
            "promotion option presented != promotion granted",
            "candidate clean != candidate promoted",
        ],
        "key_non_claims": [
            "promotion surface ≠ promotion receipt",
            "promotion option presented ≠ promotion granted",
            "candidate clean ≠ candidate promoted",
        ],
        "unsafe_to_infer": [
            "Unsafe to infer: a promotion option was selected.",
            "Unsafe to infer: promotion was granted.",
            "Unsafe to infer: reuse authority was granted.",
            "Unsafe to infer: an archive entry was activated or materialized.",
            "Unsafe to infer: machine proceed was performed.",
        ],
        "terminal_transition": TERMINAL_TRANSITION,
    }
    validate_record(record)
    return record


def validate_record(record: dict[str, Any]) -> None:
    options = record["decision_options"]
    option_ids = [option.get("decision_option_id") for option in options]
    if option_ids != OPTION_IDS:
        fail(FAIL_DECISION_OPTIONS_MISSING, str(option_ids))
    positive = options[0]
    if positive.get("decision_option_id") != OPTION_PROMOTE_ACTIVE:
        fail(FAIL_POSITIVE_OPTION_MISSING)
    scope = positive.get("promotion_scope", {})
    for key, value in positive_promotion_scope().items():
        expect(scope.get(key), value, FAIL_SCOPE_OVERBROAD if key != "radius" else FAIL_RADIUS_OVERBROAD, key)
    for forbidden in ["ANY_C8_BASIS", "ANY_ACCEPTED_BASIS_OBJECT", "EXECUTE_UNIT", "RUN_NEXT_UNIT", "RADIUS_N_BATCH"]:
        if forbidden in json.dumps(options, sort_keys=True):
            fail(FAIL_SCOPE_OVERBROAD, forbidden)
    for option in options:
        if not option.get("option_kind"):
            fail(FAIL_OPTION_EFFECT_UNTYPED, str(option))
    non_effects = record["surface_non_effects"]
    for field, value in non_effects.items():
        if value is not False:
            if field == "promotion_granted_by_this_surface":
                fail(FAIL_PROMOTION_GRANTED_INSIDE_SURFACE, field)
            if field == "reuse_authority_granted_by_this_surface":
                fail(FAIL_REUSE_GRANTED_INSIDE_SURFACE, field)
            if field in {"active_archive_entry_created_by_this_surface", "activation_created_by_this_surface"}:
                fail(FAIL_ACTIVE_ENTRY_CREATED_INSIDE_SURFACE, field)
            if field == "machine_proceed_performed_by_this_surface":
                fail(FAIL_MACHINE_PROCEED_INSIDE_SURFACE, field)
            if field == "authority_changed_by_this_surface":
                fail(FAIL_AUTHORITY_CHANGED_INSIDE_SURFACE, field)
            if field == "runner_authority_created_by_this_surface":
                fail(FAIL_RUNNER_AUTHORITY_CREATED, field)
            fail(FAIL_OPTION_EFFECT_UNTYPED, field)
    gate = record["surface_gate"]
    if gate.get("promotion_decision_surface_gate") != SURFACE_GATE or gate.get("failures") != []:
        fail(FAIL_DECISION_OPTIONS_MISSING, "surface_gate")
    for field, value in non_effects.items():
        expect(gate.get(field), value, FAIL_OPTION_EFFECT_UNTYPED, f"surface_gate.{field}")


def validate_no_forbidden_files(root: Path) -> None:
    forbidden = [
        "docs/matrixlabs/validator_archive/active",
        "docs/matrixlabs/validator_archive/promoted",
        "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_receipt_v0.json",
        "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_receipt_v0.md",
        "docs/matrixlabs/validator_archive/promotion/c8_n22_selected_archive_entry_state_materialization_v0.json",
        "docs/matrixlabs/validator_archive/promotion/c8_n22_selected_archive_entry_state_materialization_v0.md",
        "docs/matrixlabs/validator_archive/activation_object_v0.json",
        "docs/matrixlabs/next_units/c8_n22_next_bounded_unit_v0.json",
        "docs/matrixlabs/next_units/c8_n22_next_bounded_unit_v0.md",
        "docs/matrixlabs/observability/c8_observed_decision_path_update_d1_proposal_v0.json",
        "docs/matrixlabs/runners/c8_n22_runner_v0.json",
        "scripts/build_c8_n22_candidate_promotion_decision_receipt_v0.py",
        "scripts/build_c8_n22_selected_archive_entry_state_materialization_v0.py",
        "scripts/build_c8_n22_machine_proceed_under_active_entry_v0.py",
    ]
    existing = [path for path in forbidden if (root / path).exists()]
    if existing:
        fail(FAIL_ACTIVE_ENTRY_CREATED_INSIDE_SURFACE, ",".join(existing))


def render_markdown(record: dict[str, Any]) -> str:
    options = record["decision_options"]
    scope = options[0]["promotion_scope"]
    lines = [
        "# C8 n22 candidate promotion decision surface v0",
        "",
        "## Status",
        "",
        record["promotion_decision_surface_gate"],
        "",
        "## Candidate",
        "",
        record["source_candidate"]["candidate_entry_id"],
        "",
        "## Candidate audit",
        "",
        record["source_candidate"]["candidate_audit_status"],
        "",
        "## Surface role",
        "",
        "This surface presents typed human promotion options.",
        "",
        "It does not select or apply an option.",
        "",
        "## Available options",
        "",
    ]
    lines.extend(f"- {option['decision_option_id']}" for option in options)
    lines.extend(
        [
            "",
            "## Positive promotion scope",
            "",
            f"- authority state: {scope['allowed_current_authority_state']}",
            f"- requested action: {scope['allowed_requested_action']}",
            f"- requested scope: {scope['allowed_requested_action_scope']}",
            f"- basis scope: {scope['allowed_basis_scope']}",
            f"- source object: {scope['allowed_source_object_id']}",
            f"- output kind: {scope['allowed_output_kind']}",
            f"- radius: {scope['radius']}",
            "",
            "## Not performed by this surface",
            "",
            "- no option selected",
            "- no promotion decision recorded",
            "- no promotion granted",
            "- no reuse authority granted",
            "- no active archive entry created",
            "- no machine proceed performed",
            "- no authority changed",
            "- no runner authority created",
            "",
            "## Next",
            "",
            "A human promotion decision receipt is required to select one option.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def validate_markdown(record: dict[str, Any], markdown: str) -> None:
    required = [
        "# C8 n22 candidate promotion decision surface v0",
        "## Status",
        SURFACE_GATE,
        "## Candidate",
        CANDIDATE_ID,
        "## Candidate audit",
        CANDIDATE_AUDIT_STATUS,
        "This surface presents typed human promotion options.",
        "It does not select or apply an option.",
        "## Available options",
        f"- {OPTION_PROMOTE_ACTIVE}",
        f"- {OPTION_PROMOTE_INACTIVE}",
        f"- {OPTION_REVISION}",
        f"- {OPTION_DEFER}",
        f"- {OPTION_REJECT}",
        "## Positive promotion scope",
        f"- authority state: {AUTHORITY_STATE}",
        f"- requested action: {REQUESTED_ACTION}",
        f"- requested scope: {REQUESTED_SCOPE}",
        f"- basis scope: {BASIS_SCOPE}",
        f"- source object: {SOURCE_OBJECT_ID}",
        f"- output kind: {OUTPUT_KIND}",
        f"- radius: {POSITIVE_RADIUS}",
        "## Not performed by this surface",
        "- no option selected",
        "- no promotion decision recorded",
        "- no promotion granted",
        "- no reuse authority granted",
        "- no active archive entry created",
        "- no machine proceed performed",
        "- no authority changed",
        "- no runner authority created",
        "## Next",
        "A human promotion decision receipt is required to select one option.",
    ]
    missing = [phrase for phrase in required if phrase not in markdown]
    if missing:
        fail(FAIL_MARKDOWN_JSON_PARITY, str(missing))
    lower = markdown.lower()
    hits = [phrase for phrase in FORBIDDEN_MARKDOWN_PHRASES if phrase in lower]
    if re.search(r"approved", lower):
        hits.append("approved")
    if hits:
        fail(FAIL_MARKDOWN_JSON_PARITY, f"markdown:{hits}")


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
    source = record["source_candidate"]
    pre = record["pre_surface_authority_state"]
    gate = record["surface_gate"]
    non_effects = record["surface_non_effects"]
    print("BUILD_C8_N22_CANDIDATE_PROMOTION_DECISION_SURFACE_V0_COMPLETE")
    print(f"promotion_decision_surface_id={record['promotion_decision_surface_id']}")
    print(f"schema_version={record['schema_version']}")
    print(f"surface_role={record['surface_role']}")
    print(f"surface_status={record['surface_status']}")
    print(f"block_id={record['block_id']}")
    print(f"block_unit_id={record['block_unit_id']}")
    print(f"source_candidate_id={source['candidate_entry_id']}")
    print(f"candidate_audit_id={source['candidate_audit_id']}")
    print(f"candidate_audit_status={source['candidate_audit_status']}")
    print(f"candidate_contract_conformant={bool_text(source['candidate_contract_conformant'])}")
    print(f"candidate_promoted={bool_text(source['candidate_promoted'])}")
    print(f"candidate_reusable={bool_text(source['candidate_reusable'])}")
    print(f"candidate_active={bool_text(source['candidate_active'])}")
    print(f"promotion_status_before={pre['promotion_status_before']}")
    print(f"reuse_authority_status_before={pre['reuse_authority_status_before']}")
    print(f"activation_status_before={pre['activation_status_before']}")
    print(f"activation_status_reason_before={pre['activation_status_reason_before']}")
    print(f"active_archive_entry_status_before={pre['active_archive_entry_status_before']}")
    print(f"decision_options_present={bool_text(gate['decision_options_present'])}")
    print(f"decision_option_count={gate['decision_option_count']}")
    print(f"positive_option_id={gate['positive_option_id']}")
    print(f"positive_option_radius={gate['positive_option_radius']}")
    print(f"positive_option_scope_matches_candidate={bool_text(gate['positive_option_scope_matches_candidate'])}")
    for key in [
        "decision_option_selected_by_this_surface",
        "promotion_decision_recorded_by_this_surface",
        "promotion_granted_by_this_surface",
        "reuse_authority_granted_by_this_surface",
        "activation_created_by_this_surface",
        "active_archive_entry_created_by_this_surface",
        "inactive_archive_entry_created_by_this_surface",
        "machine_proceed_performed_by_this_surface",
        "next_unit_definition_surface_prepared_by_this_surface",
        "authority_changed_by_this_surface",
        "runner_authority_created_by_this_surface",
    ]:
        print(f"{key}={bool_text(non_effects[key])}")
    print(f"promotion_decision_surface_gate={record['promotion_decision_surface_gate']}")
    print(f"precommit_c8_n22_candidate_promotion_decision_surface_gate={record['precommit_c8_n22_candidate_promotion_decision_surface_gate']}")
    print("promotion_receipt_created=false")
    print("activation_object_created=false")
    print("active_archive_entry_created=false")
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
