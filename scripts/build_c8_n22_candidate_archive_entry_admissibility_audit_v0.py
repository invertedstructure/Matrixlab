#!/usr/bin/env python3
"""Build C8 n22 candidate archive entry admissibility audit v0.

This audits the C.2 candidate as contract-conformant and still powerless. It
does not promote, activate, authorize reuse, create a runner, or prepare the
next unit definition surface.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_candidate_archive_entry_admissibility_audit_v0.py"
OUTPUT_JSON = "docs/matrixlabs/validator_archive/audits/c8_n22_candidate_archive_entry_admissibility_audit_v0.json"
OUTPUT_MD = "docs/matrixlabs/validator_archive/audits/c8_n22_candidate_archive_entry_admissibility_audit_v0.md"

SCHEMA_CONTRACT = "docs/matrixlabs/validator_archive/validator_archive_entry_schema_contract_v0.json"
CANDIDATE_ENTRY = "docs/matrixlabs/validator_archive/candidates/c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.json"
ROUTER_SPECIMEN = "docs/matrixlabs/router/c8_n22_read_only_router_specimen_closure_v0.json"
ROUTE_CLASSIFICATION = "docs/matrixlabs/router/c8_n22_authority_route_classification_v0.json"
REQUESTED_ACTION = "docs/matrixlabs/router/c8_n22_requested_action_prepare_next_unit_definition_surface_v0.json"
AUTHORITY_CLOSURE = "docs/matrixlabs/boundary/c8_n22_authority_transition_closure_v0.json"
AUTHORITY_UPDATE = "docs/matrixlabs/boundary/c8_n22_authority_state_update_v0.json"

C1_COMMIT = "96223d2a9827543c27f93a1c0a16a6670a97de71"
C2_COMMIT = "674c601136f381c9d85605f646900998b24ddfe9"
B3_COMMIT = "e1f540582ecaa540e0e180b0715e653f54751ba5"
B2_COMMIT = "b6f19b7de99a7d074091c38661e4ceb28ba3d378"
B1_COMMIT = "636324fbd28e6bdcc895144d82e47311fcdd5f72"
A4_COMMIT = "7e8a1b5594f3ee725d0393ab27433b7650ec489d"
A3_COMMIT = "d8a5116ec1be3756b1ad0aa6656187c91c71e87f"

SCHEMA_VERSION = "matrixlabs_validator_archive_candidate_audit_v0"
AUDIT_ID = "c8.n22.candidate_archive_entry.admissibility_audit.v0"
AUDIT_ROLE = "CANDIDATE_ARCHIVE_ADMISSIBILITY_AUDIT"
AUDIT_MODE = "VERIFY_CANDIDATE_ONLY_NO_PROMOTION"
AUDIT_SCOPE = "CANDIDATE_REVIEW_READINESS_ONLY_NOT_REUSE_AUTHORITY"
BLOCK_ID = "BLOCK_C"
BLOCK_CLOSURE_STATUS = "BLOCK_C_PASS_CANDIDATE_CONTRACT_CONFORMANT_NOT_PROMOTED"
AUDIT_PASS = "CANDIDATE_AUDIT_PASS_CONTRACT_CONFORMANT_NOT_PROMOTED"
TERMINAL_TRANSITION = "STOP_BLOCK_C_CANDIDATE_AUDIT_CLOSED"

CONTRACT_ID = "validator_archive_entry_schema_contract.v0"
CONTRACT_SCHEMA_VERSION = "matrixlabs_validator_archive_entry_schema_contract_v0"
CONTRACT_ROLE = "ARCHIVE_ENTRY_CONTRACT_ONLY"

CANDIDATE_SCHEMA_VERSION = "matrixlabs_validator_archive_candidate_entry_v0"
CANDIDATE_ID = "candidate.c8.n22.prepare_next_unit_definition_surface.v0"
ENTRY_ROLE = "CANDIDATE_ARCHIVE_ENTRY"
ENTRY_KIND = "LOCAL_ROUTER_SPECIMEN_DERIVED_CANDIDATE"
ARCHIVE_ENTRY_STATUS = "ARCHIVE_STATUS_CANDIDATE"
PROMOTION_STATUS = "PROMOTION_NOT_REQUESTED"
REUSE_AUTHORITY_STATUS = "REUSE_AUTHORITY_NOT_GRANTED"
ACTIVATION_STATUS = "ACTIVATION_NOT_APPLICABLE"
ACTIVATION_STATUS_REASON = "CANDIDATE_ENTRY_NOT_ACTIVATABLE"
ACTIVE_ENTRY_STATUS = "NO_ACTIVE_ARCHIVE_ENTRY_CREATED"
RADIUS_LIMIT_NOW = "RADIUS_0_CANDIDATE_ONLY"

ROUTER_SPECIMEN_CLOSURE_ID = "c8.n22.router_specimen_closure.v0"
ROUTE_CLASSIFICATION_ID = "c8.n22.route.prepare_next_unit_definition_surface.v0"
REQUESTED_ACTION_RECORD_ID = "c8.n22.request.prepare_next_bounded_unit_definition_surface.v0"
AUTHORITY_STATE_UPDATE_ID = "c8.n22.authority_state_update.v0"
AUTHORITY_TRANSITION_CLOSURE_ID = "c8.n22.authority_transition_closure.v0"
ROUTE_DISPOSITION = "ROUTE_MACHINE_MAY_PREPARE_ONLY"
REQUESTED_ACTION_VALUE = "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"
REQUESTED_ACTION_SCOPE = "PREPARE_SURFACE_ONLY"
SOURCE_AUTHORITY_STATE = "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION"

FAIL_CONTRACT_MISSING = "CANDIDATE_AUDIT_FAIL_CONTRACT_MISSING"
FAIL_CANDIDATE_MISSING = "CANDIDATE_AUDIT_FAIL_CANDIDATE_MISSING"
FAIL_CONTRACT_REFERENCE_MISSING = "CANDIDATE_AUDIT_FAIL_CONTRACT_REFERENCE_MISSING"
FAIL_SCHEMA_VERSION_MISMATCH = "CANDIDATE_AUDIT_FAIL_SCHEMA_VERSION_MISMATCH"
FAIL_REQUIRED_FIELD_GROUP_MISSING = "CANDIDATE_AUDIT_FAIL_REQUIRED_FIELD_GROUP_MISSING"
FAIL_SOURCE_CHAIN_MISSING = "CANDIDATE_AUDIT_FAIL_SOURCE_CHAIN_MISSING"
FAIL_ENTRY_STATUS_INVALID = "CANDIDATE_AUDIT_FAIL_ENTRY_STATUS_INVALID"
FAIL_PROMOTION_STATUS_INVALID = "CANDIDATE_AUDIT_FAIL_PROMOTION_STATUS_INVALID"
FAIL_REUSE_STATUS_INVALID = "CANDIDATE_AUDIT_FAIL_REUSE_STATUS_INVALID"
FAIL_ACTIVATION_STATUS_INVALID = "CANDIDATE_AUDIT_FAIL_ACTIVATION_STATUS_INVALID"
FAIL_RADIUS_INVALID = "CANDIDATE_AUDIT_FAIL_RADIUS_INVALID"
FAIL_PROMOTION_SMUGGLED = "CANDIDATE_AUDIT_FAIL_PROMOTION_SMUGGLED"
FAIL_REUSE_AUTHORITY_SMUGGLED = "CANDIDATE_AUDIT_FAIL_REUSE_AUTHORITY_SMUGGLED"
FAIL_PREAPPROVED_ENTRY_SMUGGLED = "CANDIDATE_AUDIT_FAIL_PREAPPROVED_ENTRY_SMUGGLED"
FAIL_ACTIVE_ENTRY_SMUGGLED = "CANDIDATE_AUDIT_FAIL_ACTIVE_ENTRY_SMUGGLED"
FAIL_AUTO_DISPOSITION_SMUGGLED = "CANDIDATE_AUDIT_FAIL_AUTO_DISPOSITION_SMUGGLED"
FAIL_ACTION_EXECUTED = "CANDIDATE_AUDIT_FAIL_ACTION_EXECUTED"
FAIL_CANDIDATE_MOVE_PERFORMED = "CANDIDATE_AUDIT_FAIL_CANDIDATE_MOVE_PERFORMED"
FAIL_AUTHORITY_CHANGED = "CANDIDATE_AUDIT_FAIL_AUTHORITY_CHANGED"
FAIL_PREPARATION_SURFACE_CREATED = "CANDIDATE_AUDIT_FAIL_PREPARATION_SURFACE_CREATED"
FAIL_NEXT_UNIT_SURFACE_PREPARED = "CANDIDATE_AUDIT_FAIL_NEXT_UNIT_SURFACE_PREPARED"
FAIL_RUNNER_AUTHORITY_SMUGGLED = "CANDIDATE_AUDIT_FAIL_RUNNER_AUTHORITY_SMUGGLED"
FAIL_MARKDOWN_JSON_PARITY = "CANDIDATE_AUDIT_FAIL_MARKDOWN_JSON_PARITY"

REQUIRED_GROUPS = [
    "identity",
    "archive_status",
    "source_basis",
    "authority_scope",
    "requested_action_scope",
    "input_object_shape",
    "output_object_shape",
    "machine_action_scope",
    "radius_discipline",
    "validator_requirements",
    "receipt_obligations",
    "halt_conditions",
    "escalation_conditions",
    "freshness_rules",
    "forbidden_authority_changes",
    "promotion_and_reuse_status",
    "revocation_and_expiry",
    "readabout_projection_hooks",
]

AUDIT_STATUS_VOCABULARY = [
    AUDIT_PASS,
    FAIL_CONTRACT_MISSING,
    FAIL_CANDIDATE_MISSING,
    FAIL_CONTRACT_REFERENCE_MISSING,
    FAIL_SCHEMA_VERSION_MISMATCH,
    FAIL_REQUIRED_FIELD_GROUP_MISSING,
    FAIL_SOURCE_CHAIN_MISSING,
    FAIL_ENTRY_STATUS_INVALID,
    FAIL_PROMOTION_STATUS_INVALID,
    FAIL_REUSE_STATUS_INVALID,
    FAIL_ACTIVATION_STATUS_INVALID,
    FAIL_RADIUS_INVALID,
    FAIL_PROMOTION_SMUGGLED,
    FAIL_REUSE_AUTHORITY_SMUGGLED,
    FAIL_PREAPPROVED_ENTRY_SMUGGLED,
    FAIL_ACTIVE_ENTRY_SMUGGLED,
    FAIL_AUTO_DISPOSITION_SMUGGLED,
    FAIL_ACTION_EXECUTED,
    FAIL_CANDIDATE_MOVE_PERFORMED,
    FAIL_AUTHORITY_CHANGED,
    FAIL_PREPARATION_SURFACE_CREATED,
    FAIL_NEXT_UNIT_SURFACE_PREPARED,
    FAIL_RUNNER_AUTHORITY_SMUGGLED,
]

FAILURE_VOCABULARY = [
    "CANDIDATE_AUDIT_FAIL_IDENTITY_GROUP_MISSING",
    "CANDIDATE_AUDIT_FAIL_STATUS_GROUP_MISSING",
    "CANDIDATE_AUDIT_FAIL_SOURCE_BASIS_GROUP_MISSING",
    "CANDIDATE_AUDIT_FAIL_AUTHORITY_SCOPE_GROUP_MISSING",
    "CANDIDATE_AUDIT_FAIL_REQUESTED_ACTION_SCOPE_GROUP_MISSING",
    "CANDIDATE_AUDIT_FAIL_INPUT_SHAPE_GROUP_MISSING",
    "CANDIDATE_AUDIT_FAIL_OUTPUT_SHAPE_GROUP_MISSING",
    "CANDIDATE_AUDIT_FAIL_MACHINE_SCOPE_GROUP_MISSING",
    "CANDIDATE_AUDIT_FAIL_RADIUS_GROUP_MISSING",
    "CANDIDATE_AUDIT_FAIL_VALIDATOR_REQUIREMENTS_GROUP_MISSING",
    "CANDIDATE_AUDIT_FAIL_RECEIPT_OBLIGATIONS_GROUP_MISSING",
    "CANDIDATE_AUDIT_FAIL_HALT_CONDITIONS_GROUP_MISSING",
    "CANDIDATE_AUDIT_FAIL_ESCALATION_CONDITIONS_GROUP_MISSING",
    "CANDIDATE_AUDIT_FAIL_FRESHNESS_GROUP_MISSING",
    "CANDIDATE_AUDIT_FAIL_FORBIDDEN_EFFECTS_GROUP_MISSING",
    "CANDIDATE_AUDIT_FAIL_PROMOTION_REUSE_GROUP_MISSING",
    "CANDIDATE_AUDIT_FAIL_REVOCATION_EXPIRY_GROUP_MISSING",
    "CANDIDATE_AUDIT_FAIL_READABOUT_HOOKS_GROUP_MISSING",
    "CANDIDATE_AUDIT_FAIL_ENTRY_STATUS_NOT_CANDIDATE",
    FAIL_PROMOTION_SMUGGLED,
    FAIL_REUSE_AUTHORITY_SMUGGLED,
    FAIL_PREAPPROVED_ENTRY_SMUGGLED,
    FAIL_ACTIVE_ENTRY_SMUGGLED,
    FAIL_AUTO_DISPOSITION_SMUGGLED,
    FAIL_ACTION_EXECUTED,
    FAIL_CANDIDATE_MOVE_PERFORMED,
    FAIL_AUTHORITY_CHANGED,
    FAIL_PREPARATION_SURFACE_CREATED,
    FAIL_NEXT_UNIT_SURFACE_PREPARED,
    "CANDIDATE_AUDIT_FAIL_RUNNER_AUTHORITY_CREATED",
]

RECOMMENDATION_PHRASES = [
    "valid for reuse",
    "safe to use",
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
        fail(FAIL_SOURCE_CHAIN_MISSING, proc.stderr.strip())
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
        (C1_COMMIT, [SCHEMA_CONTRACT, "docs/matrixlabs/validator_archive/validator_archive_entry_schema_contract_v0.md", "scripts/build_validator_archive_entry_schema_contract_v0.py"], FAIL_CONTRACT_MISSING),
        (C2_COMMIT, [CANDIDATE_ENTRY, "docs/matrixlabs/validator_archive/candidates/c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.md", "scripts/build_c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.py"], FAIL_CANDIDATE_MISSING),
        (B3_COMMIT, [ROUTER_SPECIMEN, "docs/matrixlabs/router/c8_n22_read_only_router_specimen_closure_v0.md", "scripts/build_c8_n22_read_only_router_specimen_closure_v0.py"], FAIL_SOURCE_CHAIN_MISSING),
        (B2_COMMIT, [ROUTE_CLASSIFICATION, "docs/matrixlabs/router/c8_n22_authority_route_classification_v0.md", "scripts/build_c8_n22_authority_route_classification_v0.py"], FAIL_SOURCE_CHAIN_MISSING),
        (B1_COMMIT, [REQUESTED_ACTION, "docs/matrixlabs/router/c8_n22_requested_action_prepare_next_unit_definition_surface_v0.md", "scripts/build_c8_n22_requested_action_prepare_next_unit_definition_surface_v0.py"], FAIL_SOURCE_CHAIN_MISSING),
        (A4_COMMIT, [AUTHORITY_CLOSURE, "docs/matrixlabs/boundary/c8_n22_authority_transition_closure_v0.md", "scripts/build_c8_n22_authority_transition_closure_v0.py"], FAIL_SOURCE_CHAIN_MISSING),
        (A3_COMMIT, [AUTHORITY_UPDATE, "docs/matrixlabs/boundary/c8_n22_authority_state_update_v0.md", "scripts/build_c8_n22_authority_state_update_v0.py"], FAIL_SOURCE_CHAIN_MISSING),
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


def validate_contract(contract: dict[str, Any]) -> None:
    expect(contract.get("archive_schema_contract_id"), CONTRACT_ID, FAIL_CONTRACT_MISSING, "archive_schema_contract_id")
    expect(contract.get("schema_version"), CONTRACT_SCHEMA_VERSION, FAIL_SCHEMA_VERSION_MISMATCH, "contract.schema_version")
    expect(contract.get("contract_role"), CONTRACT_ROLE, FAIL_CONTRACT_MISSING, "contract_role")
    gate = contract.get("contract_gate", {})
    expect(gate.get("required_field_group_count"), 18, FAIL_REQUIRED_FIELD_GROUP_MISSING, "required_field_group_count")
    expect(gate.get("required_field_groups_present"), True, FAIL_REQUIRED_FIELD_GROUP_MISSING, "required_field_groups_present")
    groups = contract.get("required_field_groups", [])
    if groups != REQUIRED_GROUPS:
        fail(FAIL_REQUIRED_FIELD_GROUP_MISSING, "required_field_groups")
    if len(contract.get("field_group_contracts", [])) != 18:
        fail(FAIL_REQUIRED_FIELD_GROUP_MISSING, "field_group_contracts")


def validate_candidate(candidate: dict[str, Any]) -> None:
    expect(candidate.get("schema_version"), CANDIDATE_SCHEMA_VERSION, FAIL_SCHEMA_VERSION_MISMATCH, "candidate.schema_version")
    expect(candidate.get("archive_entry_id"), CANDIDATE_ID, FAIL_CANDIDATE_MISSING, "archive_entry_id")
    expect(candidate.get("entry_role"), ENTRY_ROLE, FAIL_CANDIDATE_MISSING, "entry_role")
    expect(candidate.get("entry_kind"), ENTRY_KIND, FAIL_CANDIDATE_MISSING, "entry_kind")
    expect(candidate.get("source_schema_contract_id"), CONTRACT_ID, FAIL_CONTRACT_REFERENCE_MISSING, "source_schema_contract_id")
    expect(candidate.get("archive_entry_status"), ARCHIVE_ENTRY_STATUS, FAIL_ENTRY_STATUS_INVALID, "archive_entry_status")
    expect(candidate.get("promotion_status"), PROMOTION_STATUS, FAIL_PROMOTION_STATUS_INVALID, "promotion_status")
    expect(candidate.get("reuse_authority_status"), REUSE_AUTHORITY_STATUS, FAIL_REUSE_STATUS_INVALID, "reuse_authority_status")
    expect(candidate.get("activation_status"), ACTIVATION_STATUS, FAIL_ACTIVATION_STATUS_INVALID, "activation_status")
    expect(candidate.get("activation_status_reason"), ACTIVATION_STATUS_REASON, FAIL_ACTIVATION_STATUS_INVALID, "activation_status_reason")
    expect(candidate.get("active_archive_entry_status"), ACTIVE_ENTRY_STATUS, FAIL_ACTIVE_ENTRY_SMUGGLED, "active_archive_entry_status")
    machine = candidate.get("candidate_machine_scope", {})
    expect(machine.get("radius_limit_now"), RADIUS_LIMIT_NOW, FAIL_RADIUS_INVALID, "radius_limit_now")
    summary = candidate.get("candidate_entry_gate_summary", {})
    expect(summary.get("candidate_archive_entry_created"), True, FAIL_CANDIDATE_MISSING, "candidate_archive_entry_created")
    expect(summary.get("candidate_entry_gate"), "CANDIDATE_ARCHIVE_ENTRY_PASS_REPRESENTABLE_NOT_PROMOTED", FAIL_CANDIDATE_MISSING, "candidate_entry_gate")
    false_fields = {
        "promotion_granted": FAIL_PROMOTION_SMUGGLED,
        "reuse_authority_granted": FAIL_REUSE_AUTHORITY_SMUGGLED,
        "auto_disposition_allowed": FAIL_AUTO_DISPOSITION_SMUGGLED,
        "action_executed": FAIL_ACTION_EXECUTED,
        "candidate_move_performed": FAIL_CANDIDATE_MOVE_PERFORMED,
        "authority_changed": FAIL_AUTHORITY_CHANGED,
        "runner_authority_created": FAIL_RUNNER_AUTHORITY_SMUGGLED,
        "preapproved_archive_entry_created": FAIL_PREAPPROVED_ENTRY_SMUGGLED,
        "active_archive_entry_created": FAIL_ACTIVE_ENTRY_SMUGGLED,
    }
    for field, code in false_fields.items():
        expect(summary.get(field), False, code, field)
    conformance = candidate.get("contract_conformance_map", {})
    expect(conformance.get("required_field_group_count"), 18, FAIL_REQUIRED_FIELD_GROUP_MISSING, "candidate.required_field_group_count")
    expect(conformance.get("all_required_groups_declared"), True, FAIL_REQUIRED_FIELD_GROUP_MISSING, "candidate.all_required_groups_declared")
    for group in REQUIRED_GROUPS:
        expect(conformance.get(group), "DECLARED", FAIL_REQUIRED_FIELD_GROUP_MISSING, group)


def validate_source_chain(
    candidate: dict[str, Any],
    specimen: dict[str, Any],
    route: dict[str, Any],
    request: dict[str, Any],
    authority_closure: dict[str, Any],
    authority_update: dict[str, Any],
) -> None:
    source = candidate.get("source_specimen", {})
    expect(source.get("router_specimen_closure_id"), ROUTER_SPECIMEN_CLOSURE_ID, FAIL_SOURCE_CHAIN_MISSING, "candidate.router_specimen_closure_id")
    expect(source.get("route_classification_id"), ROUTE_CLASSIFICATION_ID, FAIL_SOURCE_CHAIN_MISSING, "candidate.route_classification_id")
    expect(source.get("requested_action_record_id"), REQUESTED_ACTION_RECORD_ID, FAIL_SOURCE_CHAIN_MISSING, "candidate.requested_action_record_id")
    expect(source.get("authority_state_update_id"), AUTHORITY_STATE_UPDATE_ID, FAIL_SOURCE_CHAIN_MISSING, "candidate.authority_state_update_id")
    expect(source.get("authority_transition_closure_id"), AUTHORITY_TRANSITION_CLOSURE_ID, FAIL_SOURCE_CHAIN_MISSING, "candidate.authority_transition_closure_id")
    expect(specimen.get("router_specimen_closure_id"), ROUTER_SPECIMEN_CLOSURE_ID, FAIL_SOURCE_CHAIN_MISSING, "specimen.router_specimen_closure_id")
    expect(route.get("route_classification_id"), ROUTE_CLASSIFICATION_ID, FAIL_SOURCE_CHAIN_MISSING, "route_classification_id")
    expect(request.get("requested_action_record_id"), REQUESTED_ACTION_RECORD_ID, FAIL_SOURCE_CHAIN_MISSING, "requested_action_record_id")
    expect(authority_closure.get("closure_id"), AUTHORITY_TRANSITION_CLOSURE_ID, FAIL_SOURCE_CHAIN_MISSING, "closure_id")
    expect(authority_update.get("authority_update_id"), AUTHORITY_STATE_UPDATE_ID, FAIL_SOURCE_CHAIN_MISSING, "authority_update_id")
    expect(route.get("classification", {}).get("route_disposition"), ROUTE_DISPOSITION, FAIL_SOURCE_CHAIN_MISSING, "route_disposition")
    movement = request.get("requested_movement", {})
    expect(movement.get("requested_action"), REQUESTED_ACTION_VALUE, FAIL_SOURCE_CHAIN_MISSING, "requested_action")
    expect(movement.get("requested_action_scope"), REQUESTED_ACTION_SCOPE, FAIL_SOURCE_CHAIN_MISSING, "requested_action_scope")
    expect(authority_update.get("authority_state_after", {}).get("new_authority_state"), SOURCE_AUTHORITY_STATE, FAIL_SOURCE_CHAIN_MISSING, "source_authority_state")
    source_authority = candidate.get("source_specimen_authority", {})
    expect(source_authority.get("specimen_authorizes_reuse"), False, FAIL_REUSE_AUTHORITY_SMUGGLED, "specimen_authorizes_reuse")
    expect(source_authority.get("specimen_authorizes_promotion"), False, FAIL_PROMOTION_SMUGGLED, "specimen_authorizes_promotion")
    expect(source_authority.get("specimen_authorizes_activation"), False, FAIL_ACTIVE_ENTRY_SMUGGLED, "specimen_authorizes_activation")
    expect(source_authority.get("specimen_authorizes_runner"), False, FAIL_RUNNER_AUTHORITY_SMUGGLED, "specimen_authorizes_runner")


def bool_text(value: bool) -> str:
    return str(value).lower()


def contract_field_checks() -> dict[str, Any]:
    checks: dict[str, Any] = {
        "required_field_group_count": 18,
        "required_field_groups_present": True,
        "all_required_groups_valid_for_candidate": True,
    }
    checks.update({f"{group}_group_present": True for group in REQUIRED_GROUPS})
    return checks


def field_group_audit() -> list[dict[str, object]]:
    return [
        {
            "field_group": group,
            "present": True,
            "valid_for_candidate": True,
            "failure_code": "NONE",
        }
        for group in REQUIRED_GROUPS
    ]


def build_source_chain_checks() -> dict[str, object]:
    return {
        "router_specimen_closure_present": True,
        "route_classification_present": True,
        "requested_action_record_present": True,
        "authority_state_source_present": True,
        "authority_transition_closure_present": True,
        "router_specimen_closure_id": ROUTER_SPECIMEN_CLOSURE_ID,
        "route_classification_id": ROUTE_CLASSIFICATION_ID,
        "requested_action_record_id": REQUESTED_ACTION_RECORD_ID,
        "authority_state_update_id": AUTHORITY_STATE_UPDATE_ID,
        "authority_transition_closure_id": AUTHORITY_TRANSITION_CLOSURE_ID,
        "route_disposition": ROUTE_DISPOSITION,
        "requested_action": REQUESTED_ACTION_VALUE,
        "requested_action_scope": REQUESTED_ACTION_SCOPE,
        "source_authority_state": SOURCE_AUTHORITY_STATE,
        "source_chain_complete": True,
        "source_chain_authorizes_reuse": False,
        "source_chain_authorizes_promotion": False,
        "source_chain_authorizes_activation": False,
        "source_chain_authorizes_runner": False,
    }


def false_non_effects() -> dict[str, bool]:
    return {
        "promotion_granted": False,
        "reuse_authority_granted": False,
        "auto_disposition_allowed": False,
        "action_executed": False,
        "candidate_move_performed": False,
        "authority_changed": False,
        "preparation_surface_created": False,
        "next_unit_definition_surface_prepared": False,
        "runner_authority_created": False,
        "preapproved_archive_entry_created": False,
        "active_archive_entry_created": False,
        "human_promotion_decision_surface_created": False,
    }


def build_record(root: Path) -> dict[str, Any]:
    verify_expected_commits(root)
    contract = load_json(root, SCHEMA_CONTRACT, FAIL_CONTRACT_MISSING)
    candidate = load_json(root, CANDIDATE_ENTRY, FAIL_CANDIDATE_MISSING)
    specimen = load_json(root, ROUTER_SPECIMEN, FAIL_SOURCE_CHAIN_MISSING)
    route = load_json(root, ROUTE_CLASSIFICATION, FAIL_SOURCE_CHAIN_MISSING)
    request = load_json(root, REQUESTED_ACTION, FAIL_SOURCE_CHAIN_MISSING)
    authority_closure = load_json(root, AUTHORITY_CLOSURE, FAIL_SOURCE_CHAIN_MISSING)
    authority_update = load_json(root, AUTHORITY_UPDATE, FAIL_SOURCE_CHAIN_MISSING)
    validate_contract(contract)
    validate_candidate(candidate)
    validate_source_chain(candidate, specimen, route, request, authority_closure, authority_update)

    source_chain = build_source_chain_checks()
    non_effects = false_non_effects()
    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "audit_id": AUDIT_ID,
        "audit_role": AUDIT_ROLE,
        "audit_mode": AUDIT_MODE,
        "audit_admissibility_scope": AUDIT_SCOPE,
        "block_id": BLOCK_ID,
        "block_closure_status": BLOCK_CLOSURE_STATUS,
        "generated_by": GENERATOR,
        "source_contract": {
            "archive_schema_contract_id": contract["archive_schema_contract_id"],
            "schema_version": contract["schema_version"],
            "schema_role": contract["contract_role"],
        },
        "source_candidate": {
            "archive_entry_id": candidate["archive_entry_id"],
            "entry_role": candidate["entry_role"],
            "entry_kind": candidate["entry_kind"],
            "archive_entry_status": candidate["archive_entry_status"],
            "candidate_archive_entry_created": True,
        },
        "source_chain_checks": source_chain,
        "audit_result": {
            "candidate_audit_status": AUDIT_PASS,
            "candidate_contract_conformant": True,
            "candidate_well_formed_as_candidate": True,
            "candidate_promoted": False,
            "candidate_reusable": False,
            "candidate_active": False,
            **non_effects,
            "audit_created_candidate": False,
        },
        "contract_field_checks": contract_field_checks(),
        "field_group_audit": field_group_audit(),
        "authority_boundary_checks": {
            "archive_entry_status": ARCHIVE_ENTRY_STATUS,
            "promotion_status": PROMOTION_STATUS,
            "reuse_authority_status": REUSE_AUTHORITY_STATUS,
            "activation_status": ACTIVATION_STATUS,
            "activation_status_reason": ACTIVATION_STATUS_REASON,
            "active_archive_entry_status": ACTIVE_ENTRY_STATUS,
            "radius_limit_now": RADIUS_LIMIT_NOW,
            **non_effects,
            "audit_created_candidate": False,
        },
        "non_promotion_checks": {
            "promotion_granted": False,
            "promotion_receipt_present": False,
            "promotion_status_valid_for_candidate": True,
        },
        "non_reuse_checks": {
            "reuse_authority_granted": False,
            "reuse_scope_active": False,
            "reuse_status_valid_for_candidate": True,
        },
        "non_activation_checks": {
            "activation_status": ACTIVATION_STATUS,
            "activation_status_reason": ACTIVATION_STATUS_REASON,
            "preapproved_archive_entry_created": False,
            "active_archive_entry_created": False,
            "active_archive_entry_status": ACTIVE_ENTRY_STATUS,
        },
        "non_execution_checks": {
            "action_executed": False,
            "candidate_move_performed": False,
            "preparation_surface_created": False,
            "next_unit_definition_surface_prepared": False,
            "runtime_executed": False,
        },
        "non_runner_checks": {
            "runner_authority_created": False,
            "runner_entry_created": False,
        },
        "next_possible_separate_surface": {
            "surface": "HUMAN_PROMOTION_DECISION_SURFACE",
            "surface_status": "MAY_BE_PREPARED_SEPARATELY_IF_HUMAN_PROMOTION_REVIEW_IS_REQUESTED",
            "required_before_reuse": True,
            "created_by_this_audit": False,
            "authorized_by_this_audit": False,
        },
        "candidate_contract_conformance_gate": {
            "gate_status": "PASS",
            "source_contract_present": True,
            "source_candidate_present": True,
            "candidate_references_contract": True,
            "required_field_group_count": 18,
            "required_field_groups_present": True,
            "candidate_matches_contract_as_candidate": True,
            "failures": [],
        },
        "candidate_source_provenance_gate": {
            "gate_status": "PASS",
            "router_specimen_closure_present": True,
            "route_classification_present": True,
            "requested_action_record_present": True,
            "authority_state_source_present": True,
            "authority_transition_closure_present": True,
            "source_chain_complete": True,
            "source_chain_authorizes_reuse": False,
            "source_chain_authorizes_promotion": False,
            "source_chain_authorizes_activation": False,
            "source_chain_authorizes_runner": False,
            "failures": [],
        },
        "candidate_non_promotion_boundary_gate": {
            "gate_status": "PASS",
            "archive_entry_status": ARCHIVE_ENTRY_STATUS,
            "promotion_status": PROMOTION_STATUS,
            "reuse_authority_status": REUSE_AUTHORITY_STATUS,
            "activation_status": ACTIVATION_STATUS,
            "activation_status_reason": ACTIVATION_STATUS_REASON,
            "active_archive_entry_status": ACTIVE_ENTRY_STATUS,
            "radius_limit_now": RADIUS_LIMIT_NOW,
            "candidate_promoted": False,
            "candidate_reusable": False,
            "candidate_active": False,
            **non_effects,
            "failures": [],
        },
        "audit_gate_summary": {
            "precommit_candidate_archive_entry_audit_gate": "PASS",
            "candidate_audit_gate": AUDIT_PASS,
            "candidate_contract_conformance_gate": "PASS",
            "candidate_source_provenance_gate": "PASS",
            "candidate_non_promotion_boundary_gate": "PASS",
            "archive_schema_contract_present": True,
            "candidate_entry_present": True,
            "candidate_references_contract": True,
            "source_router_specimen_present": True,
            "required_field_group_count": 18,
            "required_field_groups_present": True,
            "archive_entry_status": ARCHIVE_ENTRY_STATUS,
            "promotion_status": PROMOTION_STATUS,
            "reuse_authority_status": REUSE_AUTHORITY_STATUS,
            "activation_status": ACTIVATION_STATUS,
            "activation_status_reason": ACTIVATION_STATUS_REASON,
            "active_archive_entry_status": ACTIVE_ENTRY_STATUS,
            "radius_limit_now": RADIUS_LIMIT_NOW,
            "candidate_contract_conformant": True,
            "candidate_promoted": False,
            "candidate_reusable": False,
            "candidate_active": False,
            **non_effects,
            "next_possible_separate_surface": "HUMAN_PROMOTION_DECISION_SURFACE",
            "next_possible_surface_created_by_this_audit": False,
            "next_possible_surface_authorized_by_this_audit": False,
            "failures": [],
        },
        "audit_status_vocabulary": AUDIT_STATUS_VOCABULARY,
        "failure_vocabulary": FAILURE_VOCABULARY,
        "non_claims": [
            "C.3 does not promote the candidate.",
            "C.3 does not authorize reuse.",
            "C.3 does not activate an archive entry.",
            "C.3 does not allow auto-disposition.",
            "C.3 does not execute the candidate move.",
            "C.3 does not perform the next bounded unit definition surface preparation.",
            "C.3 does not prepare a next unit definition surface.",
            "C.3 does not change authority state.",
            "C.3 does not consume human acceptance.",
            "C.3 does not rewrite receipts.",
            "C.3 does not generalize the router.",
            "C.3 does not create runner authority.",
            "C.3 does not create the human promotion decision surface.",
            "C.3 does not create a preapproved archive entry.",
            "C.3 does not create an active archive entry.",
            "C.3 only audits the candidate entry as contract-conformant and non-promoted.",
            "CANDIDATE_AUDIT_PASS_CONTRACT_CONFORMANT_NOT_PROMOTED does not imply REUSE_AUTHORITY_GRANTED_FOR_DECLARED_SCOPE.",
        ],
        "unsafe_to_infer": [
            "Unsafe to infer: the candidate is promoted.",
            "Unsafe to infer: reuse authority is granted.",
            "Unsafe to infer: the candidate is active.",
            "Unsafe to infer: an active archive entry can be created now.",
            "Unsafe to infer: the next bounded unit definition surface can be prepared now.",
            "Unsafe to infer: executable proceed authority exists under this schema.",
            "CANDIDATE_AUDIT_PASS_CONTRACT_CONFORMANT_NOT_PROMOTED implies REUSE_AUTHORITY_GRANTED_FOR_DECLARED_SCOPE",
            "candidate contract-conformant implies machine may proceed",
            "candidate audit closure implies active archive entry",
        ],
        "audit_created_candidate": False,
        "terminal_transition": TERMINAL_TRANSITION,
    }
    validate_record(record)
    return record


def validate_record(record: dict[str, Any]) -> None:
    if len(record["field_group_audit"]) != 18:
        fail(FAIL_REQUIRED_FIELD_GROUP_MISSING, "field_group_audit")
    for item in record["field_group_audit"]:
        if item.get("present") is not True or item.get("valid_for_candidate") is not True or item.get("failure_code") != "NONE":
            fail(FAIL_REQUIRED_FIELD_GROUP_MISSING, str(item))
    for gate_name in [
        "candidate_contract_conformance_gate",
        "candidate_source_provenance_gate",
        "candidate_non_promotion_boundary_gate",
    ]:
        gate = record[gate_name]
        if gate.get("gate_status") != "PASS" or gate.get("failures") != []:
            fail(FAIL_CONTRACT_MISSING, gate_name)
    summary = record["audit_gate_summary"]
    if summary.get("precommit_candidate_archive_entry_audit_gate") != "PASS":
        fail(FAIL_CONTRACT_MISSING, "precommit gate")
    if summary.get("candidate_audit_gate") != AUDIT_PASS:
        fail(FAIL_CONTRACT_MISSING, "candidate_audit_gate")
    for field, code in {
        "promotion_granted": FAIL_PROMOTION_SMUGGLED,
        "reuse_authority_granted": FAIL_REUSE_AUTHORITY_SMUGGLED,
        "auto_disposition_allowed": FAIL_AUTO_DISPOSITION_SMUGGLED,
        "action_executed": FAIL_ACTION_EXECUTED,
        "candidate_move_performed": FAIL_CANDIDATE_MOVE_PERFORMED,
        "authority_changed": FAIL_AUTHORITY_CHANGED,
        "preparation_surface_created": FAIL_PREPARATION_SURFACE_CREATED,
        "next_unit_definition_surface_prepared": FAIL_NEXT_UNIT_SURFACE_PREPARED,
        "runner_authority_created": FAIL_RUNNER_AUTHORITY_SMUGGLED,
        "preapproved_archive_entry_created": FAIL_PREAPPROVED_ENTRY_SMUGGLED,
        "active_archive_entry_created": FAIL_ACTIVE_ENTRY_SMUGGLED,
        "human_promotion_decision_surface_created": FAIL_PROMOTION_SMUGGLED,
    }.items():
        for scope in ["audit_result", "authority_boundary_checks", "audit_gate_summary"]:
            if record[scope].get(field) is not False:
                fail(code, f"{scope}.{field}")
    scan_for_forbidden_language(json.dumps(record, sort_keys=True), "json")


def scan_for_forbidden_language(text: str, label: str) -> None:
    lower = text.lower()
    hits = [phrase for phrase in RECOMMENDATION_PHRASES if phrase in lower]
    if re.search(r"(?<!pre)approved", lower):
        hits.append("approved")
    if hits:
        fail(FAIL_MARKDOWN_JSON_PARITY, f"{label}:{hits}")


def validate_no_forbidden_files(root: Path) -> None:
    forbidden = [
        "docs/matrixlabs/validator_archive/active",
        "docs/matrixlabs/validator_archive/promoted",
        "docs/matrixlabs/validator_archive/promotion_receipt_v0.json",
        "docs/matrixlabs/validator_archive/activation_object_v0.json",
        "docs/matrixlabs/validator_archive/human_promotion_decision_surface_v0.json",
        "docs/matrixlabs/decision_surfaces/c8_n22_human_promotion_decision_surface_v0.json",
        "docs/matrixlabs/next_units/c8_n22_next_bounded_unit_v0.json",
        "docs/matrixlabs/next_units/c8_n22_next_bounded_unit_v0.md",
        "docs/matrixlabs/observability/c8_observed_decision_path_update_c3_proposal_v0.json",
        "docs/matrixlabs/observability/c8_observed_path_update_c3_apply_v0.json",
        "docs/matrixlabs/runners/c8_n22_runner_v0.json",
        "scripts/build_c8_n22_runner_v0.py",
    ]
    existing = [path for path in forbidden if (root / path).exists()]
    if existing:
        fail(FAIL_ACTIVE_ENTRY_SMUGGLED, ",".join(existing))


def render_markdown(record: dict[str, Any]) -> str:
    result = record["audit_result"]
    boundary = record["authority_boundary_checks"]
    surface = record["next_possible_separate_surface"]
    lines = [
        "# C8 n22 candidate archive entry admissibility audit v0",
        "",
        "## Status",
        "",
        result["candidate_audit_status"],
        "",
        "## Audited candidate",
        "",
        record["source_candidate"]["archive_entry_id"],
        "",
        "## Contract",
        "",
        record["source_contract"]["archive_schema_contract_id"],
        "",
        "## Audit result",
        "",
        "The candidate archive entry is contract-conformant as a candidate.",
        "",
        "## Promotion",
        "",
        boundary["promotion_status"],
        "",
        "## Reuse authority",
        "",
        boundary["reuse_authority_status"],
        "",
        "## Activation",
        "",
        boundary["activation_status"],
        "",
        "## Activation reason",
        "",
        boundary["activation_status_reason"],
        "",
        "## Active archive entry",
        "",
        boundary["active_archive_entry_status"],
        "",
        "## Radius",
        "",
        boundary["radius_limit_now"],
        "",
        "## Confirmed non-effects",
        "",
        "- no promotion granted",
        "- no reuse authority granted",
        "- no preapproved archive entry created",
        "- no active archive entry created",
        "- no auto-disposition allowed",
        "- no action executed",
        "- no candidate move performed",
        "- no preparation surface created",
        "- no next unit definition surface prepared",
        "- no authority changed",
        "- no runner authority created",
        "",
        "## Next possible separate surface",
        "",
        "A separate human promotion decision surface may be prepared if future reuse review is requested.",
        "",
        "This audit did not create or authorize that surface.",
        "",
        "## Non-claim",
        "",
        "This audit does not promote the candidate, activate it, authorize reuse, or make it executable.",
        "",
        "## Contract-conformant candidate boundary",
        "",
        f"- next possible separate surface: {surface['surface']}",
        f"- surface created by this audit: {bool_text(surface['created_by_this_audit'])}",
        f"- surface authorized by this audit: {bool_text(surface['authorized_by_this_audit'])}",
        "",
        "## Non-claims",
    ]
    lines.extend(f"- {claim}" for claim in record["non_claims"])
    return "\n".join(lines).rstrip() + "\n"


def validate_markdown(record: dict[str, Any], markdown: str) -> None:
    required = [
        "# C8 n22 candidate archive entry admissibility audit v0",
        "## Status",
        AUDIT_PASS,
        "## Audited candidate",
        CANDIDATE_ID,
        "## Contract",
        CONTRACT_ID,
        "The candidate archive entry is contract-conformant as a candidate.",
        "## Promotion",
        PROMOTION_STATUS,
        "## Reuse authority",
        REUSE_AUTHORITY_STATUS,
        "## Activation",
        ACTIVATION_STATUS,
        "## Activation reason",
        ACTIVATION_STATUS_REASON,
        "## Active archive entry",
        ACTIVE_ENTRY_STATUS,
        "## Radius",
        RADIUS_LIMIT_NOW,
        "- no promotion granted",
        "- no reuse authority granted",
        "- no preapproved archive entry created",
        "- no active archive entry created",
        "- no auto-disposition allowed",
        "- no action executed",
        "- no candidate move performed",
        "- no preparation surface created",
        "- no next unit definition surface prepared",
        "- no authority changed",
        "- no runner authority created",
        "A separate human promotion decision surface may be prepared if future reuse review is requested.",
        "This audit did not create or authorize that surface.",
        "This audit does not promote the candidate, activate it, authorize reuse, or make it executable.",
    ]
    missing = [phrase for phrase in required if phrase not in markdown]
    if missing:
        fail(FAIL_MARKDOWN_JSON_PARITY, str(missing))
    for claim in record["non_claims"]:
        if claim not in markdown:
            fail(FAIL_MARKDOWN_JSON_PARITY, claim)
    scan_for_forbidden_language(markdown, "markdown")


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
    result = record["audit_result"]
    source_chain = record["source_chain_checks"]
    boundary = record["authority_boundary_checks"]
    field_checks = record["contract_field_checks"]
    surface = record["next_possible_separate_surface"]
    print("BUILD_C8_N22_CANDIDATE_ARCHIVE_ENTRY_ADMISSIBILITY_AUDIT_V0_COMPLETE")
    print(f"audit_id={record['audit_id']}")
    print(f"schema_version={record['schema_version']}")
    print(f"audit_role={record['audit_role']}")
    print(f"audit_mode={record['audit_mode']}")
    print(f"audit_admissibility_scope={record['audit_admissibility_scope']}")
    print(f"block_id={record['block_id']}")
    print(f"block_closure_status={record['block_closure_status']}")
    print(f"source_contract_id={record['source_contract']['archive_schema_contract_id']}")
    print(f"source_candidate_id={record['source_candidate']['archive_entry_id']}")
    print(f"candidate_audit_status={result['candidate_audit_status']}")
    print(f"candidate_contract_conformant={bool_text(result['candidate_contract_conformant'])}")
    print(f"candidate_well_formed_as_candidate={bool_text(result['candidate_well_formed_as_candidate'])}")
    print(f"candidate_promoted={bool_text(result['candidate_promoted'])}")
    print(f"candidate_reusable={bool_text(result['candidate_reusable'])}")
    print(f"candidate_active={bool_text(result['candidate_active'])}")
    print(f"candidate_archive_entry_created={bool_text(record['source_candidate']['candidate_archive_entry_created'])}")
    print(f"audit_created_candidate={bool_text(result['audit_created_candidate'])}")
    print(f"required_field_group_count={field_checks['required_field_group_count']}")
    print(f"required_field_groups_present={bool_text(field_checks['required_field_groups_present'])}")
    print(f"all_required_groups_valid_for_candidate={bool_text(field_checks['all_required_groups_valid_for_candidate'])}")
    print(f"source_chain_complete={bool_text(source_chain['source_chain_complete'])}")
    print(f"source_chain_authorizes_reuse={bool_text(source_chain['source_chain_authorizes_reuse'])}")
    print(f"source_chain_authorizes_promotion={bool_text(source_chain['source_chain_authorizes_promotion'])}")
    print(f"source_chain_authorizes_activation={bool_text(source_chain['source_chain_authorizes_activation'])}")
    print(f"source_chain_authorizes_runner={bool_text(source_chain['source_chain_authorizes_runner'])}")
    print(f"archive_entry_status={boundary['archive_entry_status']}")
    print(f"promotion_status={boundary['promotion_status']}")
    print(f"reuse_authority_status={boundary['reuse_authority_status']}")
    print(f"activation_status={boundary['activation_status']}")
    print(f"activation_status_reason={boundary['activation_status_reason']}")
    print(f"active_archive_entry_status={boundary['active_archive_entry_status']}")
    print(f"radius_limit_now={boundary['radius_limit_now']}")
    print(f"promotion_granted={bool_text(result['promotion_granted'])}")
    print(f"reuse_authority_granted={bool_text(result['reuse_authority_granted'])}")
    print(f"auto_disposition_allowed={bool_text(result['auto_disposition_allowed'])}")
    print(f"action_executed={bool_text(result['action_executed'])}")
    print(f"candidate_move_performed={bool_text(result['candidate_move_performed'])}")
    print(f"authority_changed={bool_text(result['authority_changed'])}")
    print(f"preparation_surface_created={bool_text(result['preparation_surface_created'])}")
    print(f"next_unit_definition_surface_prepared={bool_text(result['next_unit_definition_surface_prepared'])}")
    print(f"runner_authority_created={bool_text(result['runner_authority_created'])}")
    print(f"preapproved_archive_entry_created={bool_text(result['preapproved_archive_entry_created'])}")
    print(f"active_archive_entry_created={bool_text(result['active_archive_entry_created'])}")
    print(f"human_promotion_decision_surface_created={bool_text(result['human_promotion_decision_surface_created'])}")
    print(f"next_possible_separate_surface={surface['surface']}")
    print(f"next_possible_surface_created_by_this_audit={bool_text(surface['created_by_this_audit'])}")
    print(f"next_possible_surface_authorized_by_this_audit={bool_text(surface['authorized_by_this_audit'])}")
    print(f"candidate_contract_conformance_gate={record['candidate_contract_conformance_gate']['gate_status']}")
    print(f"candidate_source_provenance_gate={record['candidate_source_provenance_gate']['gate_status']}")
    print(f"candidate_non_promotion_boundary_gate={record['candidate_non_promotion_boundary_gate']['gate_status']}")
    print(f"candidate_audit_gate={record['audit_gate_summary']['candidate_audit_gate']}")
    print("promotion_receipt_created=false")
    print("activation_object_created=false")
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
