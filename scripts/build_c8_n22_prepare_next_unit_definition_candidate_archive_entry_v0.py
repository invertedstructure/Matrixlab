#!/usr/bin/env python3
"""Build C8 n22 prepare-next-unit-definition candidate archive entry v0.

This represents one committed local router specimen as a candidate archive
entry. It does not promote, activate, authorize reuse, or perform the move.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.py"
OUTPUT_JSON = "docs/matrixlabs/validator_archive/candidates/c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.json"
OUTPUT_MD = "docs/matrixlabs/validator_archive/candidates/c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.md"

SCHEMA_CONTRACT = "docs/matrixlabs/validator_archive/validator_archive_entry_schema_contract_v0.json"
ROUTER_SPECIMEN = "docs/matrixlabs/router/c8_n22_read_only_router_specimen_closure_v0.json"
ROUTE_CLASSIFICATION = "docs/matrixlabs/router/c8_n22_authority_route_classification_v0.json"
REQUESTED_ACTION = "docs/matrixlabs/router/c8_n22_requested_action_prepare_next_unit_definition_surface_v0.json"
AUTHORITY_CLOSURE = "docs/matrixlabs/boundary/c8_n22_authority_transition_closure_v0.json"
AUTHORITY_UPDATE = "docs/matrixlabs/boundary/c8_n22_authority_state_update_v0.json"

C1_COMMIT = "96223d2a9827543c27f93a1c0a16a6670a97de71"
B3_COMMIT = "e1f540582ecaa540e0e180b0715e653f54751ba5"
B2_COMMIT = "b6f19b7de99a7d074091c38661e4ceb28ba3d378"
B1_COMMIT = "636324fbd28e6bdcc895144d82e47311fcdd5f72"
A4_COMMIT = "7e8a1b5594f3ee725d0393ab27433b7650ec489d"
A3_COMMIT = "d8a5116ec1be3756b1ad0aa6656187c91c71e87f"

SCHEMA_VERSION = "matrixlabs_validator_archive_candidate_entry_v0"
ARCHIVE_ENTRY_ID = "candidate.c8.n22.prepare_next_unit_definition_surface.v0"
ENTRY_ROLE = "CANDIDATE_ARCHIVE_ENTRY"
ENTRY_KIND = "LOCAL_ROUTER_SPECIMEN_DERIVED_CANDIDATE"
ARCHIVE_ENTRY_STATUS = "ARCHIVE_STATUS_CANDIDATE"
SOURCE_SCHEMA_CONTRACT_ID = "validator_archive_entry_schema_contract.v0"
PROMOTION_STATUS = "PROMOTION_NOT_REQUESTED"
REUSE_AUTHORITY_STATUS = "REUSE_AUTHORITY_NOT_GRANTED"
ACTIVATION_STATUS = "ACTIVATION_NOT_APPLICABLE"
ACTIVATION_STATUS_REASON = "CANDIDATE_ENTRY_NOT_ACTIVATABLE"
PREAPPROVED_STATUS = "NO_PREAPPROVED_ARCHIVE_ENTRY_CREATED"
ACTIVE_STATUS = "NO_ACTIVE_ARCHIVE_ENTRY_CREATED"
AUTO_DISPOSITION_STATUS = "AUTO_DISPOSITION_NOT_ALLOWED"
RUNNER_AUTHORITY_STATUS = "RUNNER_AUTHORITY_NOT_CREATED"

ROUTER_SPECIMEN_CLOSURE_ID = "c8.n22.router_specimen_closure.v0"
ROUTE_CLASSIFICATION_ID = "c8.n22.route.prepare_next_unit_definition_surface.v0"
REQUESTED_ACTION_RECORD_ID = "c8.n22.request.prepare_next_bounded_unit_definition_surface.v0"
AUTHORITY_STATE_UPDATE_ID = "c8.n22.authority_state_update.v0"
AUTHORITY_TRANSITION_CLOSURE_ID = "c8.n22.authority_transition_closure.v0"

CURRENT_AUTHORITY_STATE = "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION"
REQUESTED_ACTION_VALUE = "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"
REQUESTED_ACTION_SCOPE = "PREPARE_SURFACE_ONLY"
BASIS_SCOPE = "C8_N22_BASIS_ONLY"
SOURCE_OBJECT_ID = "c8.n22"
OUTPUT_KIND = "NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"

REPRESENTATION_GATE = "CANDIDATE_ARCHIVE_ENTRY_PASS_REPRESENTABLE"
NON_PROMOTION_GATE = "CANDIDATE_ARCHIVE_ENTRY_PASS_NOT_PROMOTED"
CANDIDATE_ENTRY_GATE = "CANDIDATE_ARCHIVE_ENTRY_PASS_REPRESENTABLE_NOT_PROMOTED"

FAIL_ARCHIVE_SCHEMA_CONTRACT_MISSING = "CANDIDATE_ENTRY_FAIL_ARCHIVE_SCHEMA_CONTRACT_MISSING"
FAIL_SOURCE_ROUTER_SPECIMEN_MISSING = "CANDIDATE_ENTRY_FAIL_SOURCE_ROUTER_SPECIMEN_MISSING"
FAIL_ROUTE_CLASSIFICATION_MISSING = "CANDIDATE_ENTRY_FAIL_ROUTE_CLASSIFICATION_MISSING"
FAIL_REQUESTED_ACTION_MISSING = "CANDIDATE_ENTRY_FAIL_REQUESTED_ACTION_MISSING"
FAIL_AUTHORITY_STATE_MISSING = "CANDIDATE_ENTRY_FAIL_AUTHORITY_STATE_MISSING"
FAIL_ENTRY_STATUS_NOT_CANDIDATE = "CANDIDATE_ENTRY_FAIL_ENTRY_STATUS_NOT_CANDIDATE"
FAIL_PROMOTION_STATUS_MISSING = "CANDIDATE_ENTRY_FAIL_PROMOTION_STATUS_MISSING"
FAIL_REUSE_STATUS_MISSING = "CANDIDATE_ENTRY_FAIL_REUSE_STATUS_MISSING"
FAIL_ACTIVATION_STATUS_MISSING = "CANDIDATE_ENTRY_FAIL_ACTIVATION_STATUS_MISSING"
FAIL_SCOPE_MISSING = "CANDIDATE_ENTRY_FAIL_SCOPE_MISSING"
FAIL_SOURCE_OBJECT_SCOPE_OVERBROAD = "CANDIDATE_ENTRY_FAIL_SOURCE_OBJECT_SCOPE_OVERBROAD"
FAIL_RADIUS_MISSING = "CANDIDATE_ENTRY_FAIL_RADIUS_MISSING"
FAIL_CONTRACT_CONFORMANCE_MAP_MISSING = "CANDIDATE_ENTRY_FAIL_CONTRACT_CONFORMANCE_MAP_MISSING"
FAIL_VALIDATORS_MISSING = "CANDIDATE_ENTRY_FAIL_VALIDATORS_MISSING"
FAIL_RECEIPTS_MISSING = "CANDIDATE_ENTRY_FAIL_RECEIPTS_MISSING"
FAIL_HALTS_MISSING = "CANDIDATE_ENTRY_FAIL_HALTS_MISSING"
FAIL_ESCALATIONS_MISSING = "CANDIDATE_ENTRY_FAIL_ESCALATIONS_MISSING"
FAIL_FORBIDDEN_EFFECTS_MISSING = "CANDIDATE_ENTRY_FAIL_FORBIDDEN_EFFECTS_MISSING"
FAIL_FRESHNESS_RULES_MISSING = "CANDIDATE_ENTRY_FAIL_FRESHNESS_RULES_MISSING"
FAIL_PROMOTION_SMUGGLED = "CANDIDATE_ENTRY_FAIL_PROMOTION_SMUGGLED"
FAIL_REUSE_AUTHORITY_SMUGGLED = "CANDIDATE_ENTRY_FAIL_REUSE_AUTHORITY_SMUGGLED"
FAIL_AUTO_DISPOSITION_SMUGGLED = "CANDIDATE_ENTRY_FAIL_AUTO_DISPOSITION_SMUGGLED"
FAIL_ACTION_EXECUTED = "CANDIDATE_ENTRY_FAIL_ACTION_EXECUTED"
FAIL_AUTHORITY_CHANGED = "CANDIDATE_ENTRY_FAIL_AUTHORITY_CHANGED"
FAIL_PREPARATION_PERFORMED = "CANDIDATE_ENTRY_FAIL_PREPARATION_PERFORMED"
FAIL_PREAPPROVED_ENTRY_CREATED = "CANDIDATE_ENTRY_FAIL_PREAPPROVED_ENTRY_CREATED"
FAIL_ACTIVE_ENTRY_CREATED = "CANDIDATE_ENTRY_FAIL_ACTIVE_ENTRY_CREATED"
FAIL_RUNNER_AUTHORITY_CREATED = "CANDIDATE_ENTRY_FAIL_RUNNER_AUTHORITY_CREATED"
FAIL_MARKDOWN_JSON_PARITY = "CANDIDATE_ENTRY_FAIL_MARKDOWN_JSON_PARITY"

FAILURE_VOCABULARY = [
    FAIL_ARCHIVE_SCHEMA_CONTRACT_MISSING,
    FAIL_SOURCE_ROUTER_SPECIMEN_MISSING,
    FAIL_ROUTE_CLASSIFICATION_MISSING,
    FAIL_REQUESTED_ACTION_MISSING,
    FAIL_AUTHORITY_STATE_MISSING,
    FAIL_ENTRY_STATUS_NOT_CANDIDATE,
    FAIL_PROMOTION_STATUS_MISSING,
    FAIL_REUSE_STATUS_MISSING,
    FAIL_ACTIVATION_STATUS_MISSING,
    FAIL_SCOPE_MISSING,
    FAIL_SOURCE_OBJECT_SCOPE_OVERBROAD,
    FAIL_RADIUS_MISSING,
    FAIL_CONTRACT_CONFORMANCE_MAP_MISSING,
    FAIL_VALIDATORS_MISSING,
    FAIL_RECEIPTS_MISSING,
    FAIL_HALTS_MISSING,
    FAIL_ESCALATIONS_MISSING,
    FAIL_FORBIDDEN_EFFECTS_MISSING,
    FAIL_FRESHNESS_RULES_MISSING,
    FAIL_PROMOTION_SMUGGLED,
    FAIL_REUSE_AUTHORITY_SMUGGLED,
    FAIL_AUTO_DISPOSITION_SMUGGLED,
    FAIL_ACTION_EXECUTED,
    FAIL_AUTHORITY_CHANGED,
    FAIL_PREPARATION_PERFORMED,
    FAIL_PREAPPROVED_ENTRY_CREATED,
    FAIL_ACTIVE_ENTRY_CREATED,
    FAIL_RUNNER_AUTHORITY_CREATED,
    FAIL_MARKDOWN_JSON_PARITY,
]

REQUIRED_GROUP_IDS = [
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

RECOMMENDATION_PHRASES = [
    "validated route",
    "safe to use",
    "machine may proceed",
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
        fail(FAIL_FRESHNESS_RULES_MISSING, proc.stderr.strip())
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
        (B3_COMMIT, [ROUTER_SPECIMEN, "docs/matrixlabs/router/c8_n22_read_only_router_specimen_closure_v0.md", "scripts/build_c8_n22_read_only_router_specimen_closure_v0.py"], FAIL_SOURCE_ROUTER_SPECIMEN_MISSING),
        (B2_COMMIT, [ROUTE_CLASSIFICATION, "docs/matrixlabs/router/c8_n22_authority_route_classification_v0.md", "scripts/build_c8_n22_authority_route_classification_v0.py"], FAIL_ROUTE_CLASSIFICATION_MISSING),
        (B1_COMMIT, [REQUESTED_ACTION, "docs/matrixlabs/router/c8_n22_requested_action_prepare_next_unit_definition_surface_v0.md", "scripts/build_c8_n22_requested_action_prepare_next_unit_definition_surface_v0.py"], FAIL_REQUESTED_ACTION_MISSING),
        (A4_COMMIT, [AUTHORITY_CLOSURE, "docs/matrixlabs/boundary/c8_n22_authority_transition_closure_v0.md", "scripts/build_c8_n22_authority_transition_closure_v0.py"], FAIL_AUTHORITY_STATE_MISSING),
        (A3_COMMIT, [AUTHORITY_UPDATE, "docs/matrixlabs/boundary/c8_n22_authority_state_update_v0.md", "scripts/build_c8_n22_authority_state_update_v0.py"], FAIL_AUTHORITY_STATE_MISSING),
    ]
    for commit, paths, failure_code in expected:
        run_git(root, ["cat-file", "-e", f"{commit}^{{commit}}"], failure_code)
        got = commit_for_paths(root, paths, failure_code)
        if got != commit:
            fail(failure_code, f"{paths[0]} commit mismatch: {got}!={commit}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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


def source_record(root: Path, rel: str, commit: str) -> dict[str, str]:
    return {
        "path": rel,
        "commit_sha": commit,
        "sha256": sha256_file(root / rel),
    }


def validate_sources(
    contract: dict[str, Any],
    specimen: dict[str, Any],
    route: dict[str, Any],
    request: dict[str, Any],
    authority_closure: dict[str, Any],
    authority_update: dict[str, Any],
) -> None:
    expect(contract.get("archive_schema_contract_id"), SOURCE_SCHEMA_CONTRACT_ID, FAIL_ARCHIVE_SCHEMA_CONTRACT_MISSING, "archive_schema_contract_id")
    expect(contract.get("schema_version"), "matrixlabs_validator_archive_entry_schema_contract_v0", FAIL_ARCHIVE_SCHEMA_CONTRACT_MISSING, "schema_version")
    expect(contract.get("contract_status"), "ARCHIVE_SCHEMA_PASS_CONTRACT_DEFINED", FAIL_ARCHIVE_SCHEMA_CONTRACT_MISSING, "contract_status")
    expect(contract.get("contract_gate", {}).get("required_field_group_count"), 18, FAIL_CONTRACT_CONFORMANCE_MAP_MISSING, "required_field_group_count")
    expect(contract.get("contract_gate", {}).get("required_field_groups_present"), True, FAIL_CONTRACT_CONFORMANCE_MAP_MISSING, "required_field_groups_present")

    expect(specimen.get("router_specimen_closure_id"), ROUTER_SPECIMEN_CLOSURE_ID, FAIL_SOURCE_ROUTER_SPECIMEN_MISSING, "router_specimen_closure_id")
    expect(specimen.get("block_status"), "BLOCK_B_PASS_READ_ONLY_ROUTE_CLASSIFIED", FAIL_SOURCE_ROUTER_SPECIMEN_MISSING, "block_status")
    expect(specimen.get("closure_gate", {}).get("closure_status"), "ROUTER_SPECIMEN_CLOSURE_PASS_ALLOWED_PREPARE_ONLY", FAIL_SOURCE_ROUTER_SPECIMEN_MISSING, "closure_status")
    archive = specimen.get("specimen_archive", {})
    expect(archive.get("specimen_kind"), "READ_ONLY_AUTHORITY_ROUTING_SPECIMEN", FAIL_SOURCE_ROUTER_SPECIMEN_MISSING, "specimen_kind")
    expect(archive.get("may_support_future_router_analysis"), True, FAIL_SOURCE_ROUTER_SPECIMEN_MISSING, "may_support_future_router_analysis")
    expect(archive.get("may_authorize_future_reuse"), False, FAIL_REUSE_AUTHORITY_SMUGGLED, "may_authorize_future_reuse")
    expect(archive.get("may_preapprove_future_routes"), False, FAIL_PROMOTION_SMUGGLED, "may_preapprove_future_routes")
    expect(archive.get("may_create_reusable_router_authority"), False, FAIL_REUSE_AUTHORITY_SMUGGLED, "may_create_reusable_router_authority")
    expect(archive.get("may_serve_as_validator_archive_entry"), False, FAIL_ACTIVE_ENTRY_CREATED, "may_serve_as_validator_archive_entry")

    expect(route.get("route_classification_id"), ROUTE_CLASSIFICATION_ID, FAIL_ROUTE_CLASSIFICATION_MISSING, "route_classification_id")
    classification = route.get("classification", {})
    expect(classification.get("route_disposition"), "ROUTE_MACHINE_MAY_PREPARE_ONLY", FAIL_ROUTE_CLASSIFICATION_MISSING, "route_disposition")
    expect(classification.get("allowed_machine_action_scope"), "PREPARE_SURFACE_ONLY", FAIL_ROUTE_CLASSIFICATION_MISSING, "allowed_machine_action_scope")
    expect(classification.get("allowed_scope"), BASIS_SCOPE, FAIL_ROUTE_CLASSIFICATION_MISSING, "allowed_scope")
    gate = route.get("router_gate", {})
    expect(gate.get("action_executed"), False, FAIL_ACTION_EXECUTED, "route.action_executed")
    expect(gate.get("requested_output_created"), False, FAIL_PREPARATION_PERFORMED, "route.requested_output_created")
    expect(gate.get("authority_changed"), False, FAIL_AUTHORITY_CHANGED, "route.authority_changed")
    expect(gate.get("reusable_router_created"), False, FAIL_REUSE_AUTHORITY_SMUGGLED, "route.reusable_router_created")
    expect(gate.get("validator_archive_created"), False, FAIL_ACTIVE_ENTRY_CREATED, "route.validator_archive_created")

    expect(request.get("requested_action_record_id"), REQUESTED_ACTION_RECORD_ID, FAIL_REQUESTED_ACTION_MISSING, "requested_action_record_id")
    movement = request.get("requested_movement", {})
    expect(movement.get("requested_action"), REQUESTED_ACTION_VALUE, FAIL_REQUESTED_ACTION_MISSING, "requested_action")
    expect(movement.get("requested_action_scope"), REQUESTED_ACTION_SCOPE, FAIL_REQUESTED_ACTION_MISSING, "requested_action_scope")
    expect(movement.get("requested_output_kind"), OUTPUT_KIND, FAIL_REQUESTED_ACTION_MISSING, "requested_output_kind")
    expect(movement.get("requested_target_basis"), SOURCE_OBJECT_ID, FAIL_REQUESTED_ACTION_MISSING, "requested_target_basis")

    expect(authority_closure.get("closure_id"), AUTHORITY_TRANSITION_CLOSURE_ID, FAIL_AUTHORITY_STATE_MISSING, "closure_id")
    expect(authority_closure.get("closure_gate", {}).get("resulting_authority_state"), CURRENT_AUTHORITY_STATE, FAIL_AUTHORITY_STATE_MISSING, "resulting_authority_state")
    expect(authority_closure.get("next_lawful_surface", {}).get("surface_scope"), BASIS_SCOPE, FAIL_SCOPE_MISSING, "surface_scope")
    expect(authority_update.get("authority_update_id"), AUTHORITY_STATE_UPDATE_ID, FAIL_AUTHORITY_STATE_MISSING, "authority_update_id")
    expect(authority_update.get("authority_state_after", {}).get("new_authority_state"), CURRENT_AUTHORITY_STATE, FAIL_AUTHORITY_STATE_MISSING, "new_authority_state")
    expect(authority_update.get("next_router_state", {}).get("next_allowed_router_action"), REQUESTED_ACTION_VALUE, FAIL_AUTHORITY_STATE_MISSING, "next_allowed_router_action")


def build_contract_conformance_map() -> dict[str, Any]:
    out: dict[str, Any] = {
        "source_schema_contract_id": SOURCE_SCHEMA_CONTRACT_ID,
        "required_field_group_count": 18,
    }
    out.update({group_id: "DECLARED" for group_id in REQUIRED_GROUP_IDS})
    out["all_required_groups_declared"] = True
    return out


def required_validators() -> list[dict[str, list[str] | str]]:
    return [
        {
            "validator": "authority_state_match_validator",
            "checks": [
                "current_authority_state",
                "basis_scope",
                "source_object_id",
                "next_allowed_router_action",
            ],
        },
        {
            "validator": "requested_action_scope_validator",
            "checks": [
                "requested_action",
                "requested_action_scope",
                "requested_output_kind",
            ],
        },
        {
            "validator": "basis_scope_validator",
            "checks": [
                "allowed_basis_scope",
                "allowed_source_object_id",
            ],
        },
        {
            "validator": "forbidden_effects_validator",
            "checks": [
                "execution_authority",
                "reuse_authority",
                "taxonomy_promotion_authority",
                "updater_generalization_authority",
                "runner_authority",
                "authority_state_change",
                "active_archive_entry_creation",
            ],
        },
        {
            "validator": "output_shape_validator",
            "checks": [
                "output_object_type",
                "output_scope",
                "required_nonclaims",
            ],
        },
        {
            "validator": "freshness_validator",
            "checks": [
                "source_commit_sha",
                "source_freshness_status",
            ],
        },
        {
            "validator": "radius_validator",
            "checks": [
                "radius_limit_now",
                "proposed_radius_limit_if_promoted",
            ],
        },
    ]


def build_record(root: Path) -> dict[str, Any]:
    verify_expected_commits(root)
    contract = load_json(root, SCHEMA_CONTRACT, FAIL_ARCHIVE_SCHEMA_CONTRACT_MISSING)
    specimen = load_json(root, ROUTER_SPECIMEN, FAIL_SOURCE_ROUTER_SPECIMEN_MISSING)
    route = load_json(root, ROUTE_CLASSIFICATION, FAIL_ROUTE_CLASSIFICATION_MISSING)
    request = load_json(root, REQUESTED_ACTION, FAIL_REQUESTED_ACTION_MISSING)
    authority_closure = load_json(root, AUTHORITY_CLOSURE, FAIL_AUTHORITY_STATE_MISSING)
    authority_update = load_json(root, AUTHORITY_UPDATE, FAIL_AUTHORITY_STATE_MISSING)
    validate_sources(contract, specimen, route, request, authority_closure, authority_update)

    source_artifacts = {
        "schema_contract": source_record(root, SCHEMA_CONTRACT, C1_COMMIT),
        "router_specimen": source_record(root, ROUTER_SPECIMEN, B3_COMMIT),
        "route_classification": source_record(root, ROUTE_CLASSIFICATION, B2_COMMIT),
        "requested_action": source_record(root, REQUESTED_ACTION, B1_COMMIT),
        "authority_transition_closure": source_record(root, AUTHORITY_CLOSURE, A4_COMMIT),
        "authority_state_update": source_record(root, AUTHORITY_UPDATE, A3_COMMIT),
    }
    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "archive_entry_id": ARCHIVE_ENTRY_ID,
        "entry_role": ENTRY_ROLE,
        "entry_kind": ENTRY_KIND,
        "archive_entry_status": ARCHIVE_ENTRY_STATUS,
        "source_schema_contract_id": SOURCE_SCHEMA_CONTRACT_ID,
        "promotion_status": PROMOTION_STATUS,
        "reuse_authority_status": REUSE_AUTHORITY_STATUS,
        "activation_status": ACTIVATION_STATUS,
        "activation_status_reason": ACTIVATION_STATUS_REASON,
        "preapproved_archive_entry_status": PREAPPROVED_STATUS,
        "active_archive_entry_status": ACTIVE_STATUS,
        "auto_disposition_status": AUTO_DISPOSITION_STATUS,
        "runner_authority_status": RUNNER_AUTHORITY_STATUS,
        "generated_by": GENERATOR,
        "source_artifacts": source_artifacts,
        "source_specimen": {
            "specimen_kind": "READ_ONLY_AUTHORITY_ROUTING_SPECIMEN",
            "router_specimen_closure_id": ROUTER_SPECIMEN_CLOSURE_ID,
            "route_classification_id": ROUTE_CLASSIFICATION_ID,
            "requested_action_record_id": REQUESTED_ACTION_RECORD_ID,
            "authority_state_update_id": AUTHORITY_STATE_UPDATE_ID,
            "authority_transition_closure_id": AUTHORITY_TRANSITION_CLOSURE_ID,
        },
        "source_specimen_authority": {
            "specimen_may_support_future_analysis": True,
            "specimen_authorizes_reuse": False,
            "specimen_authorizes_promotion": False,
            "specimen_authorizes_activation": False,
            "specimen_authorizes_runner": False,
        },
        "source_commit_freshness": {
            "schema_contract_source_commit_verified": True,
            "router_specimen_source_commit_verified": True,
            "route_classification_source_commit_verified": True,
            "requested_action_source_commit_verified": True,
            "authority_state_source_commit_verified": True,
            "source_freshness_status": "SOURCE_COMMIT_VERIFIED",
            "unknown_freshness_halt_code": "HALT_SOURCE_FRESHNESS_UNKNOWN",
            "stale_source_halt_code": "HALT_SOURCE_STALE",
            "source_artifacts": source_artifacts,
        },
        "candidate_move_shape": {
            "allowed_current_authority_state": CURRENT_AUTHORITY_STATE,
            "allowed_requested_action": REQUESTED_ACTION_VALUE,
            "allowed_requested_action_scope": REQUESTED_ACTION_SCOPE,
            "allowed_basis_scope": BASIS_SCOPE,
            "allowed_source_object_id": SOURCE_OBJECT_ID,
            "allowed_output_kind": OUTPUT_KIND,
        },
        "candidate_machine_scope": {
            "machine_action_scope_if_promoted": "PREPARE_SURFACE_ONLY",
            "machine_action_scope_now": "NONE_CANDIDATE_ONLY",
            "auto_disposition_allowed_now": False,
            "action_execution_allowed_now": False,
            "authority_change_allowed_now": False,
            "candidate_move_performed_now": False,
            "radius_limit_now": "RADIUS_0_CANDIDATE_ONLY",
            "proposed_radius_limit_if_promoted": "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT",
        },
        "required_input_shape_if_promoted": {
            "required_authority_source_kind": "AUTHORITY_STATE_UPDATE_OR_TRANSITION_CLOSURE",
            "required_current_authority_state": CURRENT_AUTHORITY_STATE,
            "required_next_allowed_router_action": REQUESTED_ACTION_VALUE,
            "required_basis_scope": BASIS_SCOPE,
            "required_source_object_id": SOURCE_OBJECT_ID,
            "required_requested_action_record": True,
            "required_route_classification_record": True,
            "required_router_specimen_closure_record": True,
        },
        "allowed_output_shape_if_promoted": {
            "allowed_output_object_type": OUTPUT_KIND,
            "allowed_output_scope": "SURFACE_ONLY",
            "allowed_output_basis": SOURCE_OBJECT_ID,
            "must_include_nonclaims": True,
            "must_preserve_no_execution": True,
            "must_preserve_no_reuse": True,
            "must_preserve_no_runner_authority": True,
            "must_preserve_no_authority_state_change": True,
        },
        "contract_conformance_map": build_contract_conformance_map(),
        "required_validators_if_promoted": required_validators(),
        "required_receipts_if_promoted": [
            "requested_action_record",
            "route_classification_record",
            "preparation_surface_receipt",
            "preparation_closeout_receipt",
        ],
        "optional_readouts_if_promoted": [
            "human_readabout_projection",
        ],
        "mandatory_halts_if_promoted": [
            "HALT_AUTHORITY_STATE_MISMATCH",
            "HALT_REQUESTED_ACTION_SCOPE_MISMATCH",
            "HALT_BASIS_SCOPE_MISMATCH",
            "HALT_SOURCE_OBJECT_MISMATCH",
            "HALT_OUTPUT_KIND_MISMATCH",
            "HALT_REQUIRED_VALIDATOR_MISSING",
            "HALT_REQUIRED_RECEIPT_MISSING",
            "HALT_FORBIDDEN_EFFECT_DETECTED",
            "HALT_RADIUS_EXCEEDED",
            "HALT_SOURCE_FRESHNESS_UNKNOWN",
        ],
        "mandatory_escalations_if_promoted": [
            "ESCALATE_BOUNDARY_UNCLEAR",
            "ESCALATE_SCHEMA_SCOPE_AMBIGUOUS",
            "ESCALATE_OUTPUT_SHAPE_UNEXPECTED",
            "ESCALATE_REQUESTED_AUTHORITY_CHANGE",
            "ESCALATE_PROMOTION_OR_REUSE_REQUESTED",
            "ESCALATE_SOURCE_OBJECT_NOT_C8_N22",
        ],
        "forbidden_effects_now": {
            "execute_unit": True,
            "perform_preparation_surface_now": True,
            "rewrite_receipts": True,
            "change_authority_state": True,
            "consume_human_decision": True,
            "promote_taxonomy": True,
            "authorize_reuse": True,
            "grant_promotion": True,
            "generalize_updater": True,
            "activate_runner": True,
            "create_preapproved_archive_entry": True,
            "create_active_archive_entry": True,
        },
        "forbidden_effects_even_if_promoted_unless_separately_declared": {
            "execute_unit": True,
            "change_authority_state": True,
            "consume_human_decision": True,
            "promote_taxonomy": True,
            "authorize_reuse_beyond_declared_scope": True,
            "generalize_updater": True,
            "activate_runner": True,
            "rewrite_receipts": True,
        },
        "promotion_boundary": {
            "candidate_archive_entry_created": True,
            "promotion_requested_by_this_entry": False,
            "promotion_granted_by_this_entry": False,
            "reuse_authority_granted_by_this_entry": False,
            "activation_granted_by_this_entry": False,
            "requires_human_promotion_decision_before_reuse": True,
            "required_future_surface": "HUMAN_PROMOTION_DECISION_SURFACE",
            "required_future_receipt": "HUMAN_PROMOTION_DECISION_RECEIPT",
            "preapproved_archive_entry_created": False,
            "active_archive_entry_created": False,
            "created_future_surface": False,
            "created_future_receipt": False,
        },
        "candidate_representation_gate": {
            "gate_status": REPRESENTATION_GATE,
            "archive_schema_contract_present": True,
            "source_router_specimen_present": True,
            "source_route_classification_present": True,
            "source_requested_action_present": True,
            "source_authority_state_present": True,
            "candidate_move_shape_declared": True,
            "required_input_shape_declared": True,
            "allowed_output_shape_declared": True,
            "contract_conformance_map_declared": True,
            "required_validators_declared": True,
            "required_receipts_declared": True,
            "mandatory_halts_declared": True,
            "mandatory_escalations_declared": True,
            "forbidden_effects_declared": True,
            "freshness_rules_declared": True,
            "failures": [],
        },
        "candidate_non_promotion_gate": {
            "gate_status": NON_PROMOTION_GATE,
            "archive_entry_status": ARCHIVE_ENTRY_STATUS,
            "promotion_status": PROMOTION_STATUS,
            "reuse_authority_status": REUSE_AUTHORITY_STATUS,
            "activation_status": ACTIVATION_STATUS,
            "active_archive_entry_status": ACTIVE_STATUS,
            "radius_limit_now": "RADIUS_0_CANDIDATE_ONLY",
            "promotion_granted": False,
            "reuse_authority_granted": False,
            "auto_disposition_allowed": False,
            "action_executed": False,
            "candidate_move_performed": False,
            "authority_changed": False,
            "runner_authority_created": False,
            "preapproved_archive_entry_created": False,
            "active_archive_entry_created": False,
            "failures": [],
        },
        "candidate_entry_gate_summary": {
            "precommit_candidate_archive_entry_gate": "PASS",
            "candidate_entry_gate": CANDIDATE_ENTRY_GATE,
            "candidate_representation_gate": REPRESENTATION_GATE,
            "candidate_non_promotion_gate": NON_PROMOTION_GATE,
            "archive_entry_status": ARCHIVE_ENTRY_STATUS,
            "promotion_status": PROMOTION_STATUS,
            "reuse_authority_status": REUSE_AUTHORITY_STATUS,
            "activation_status": ACTIVATION_STATUS,
            "candidate_archive_entry_created": True,
            "promotion_granted": False,
            "reuse_authority_granted": False,
            "auto_disposition_allowed": False,
            "action_executed": False,
            "candidate_move_performed": False,
            "authority_changed": False,
            "runner_authority_created": False,
            "preapproved_archive_entry_created": False,
            "active_archive_entry_created": False,
            "failures": [],
        },
        "failure_vocabulary": FAILURE_VOCABULARY,
        "non_claims": [
            "C.2 does not promote the candidate.",
            "C.2 does not authorize reuse.",
            "C.2 does not create a preapproved archive entry.",
            "C.2 does not create an active archive entry.",
            "C.2 does not allow auto-disposition.",
            "C.2 does not execute the candidate move.",
            "C.2 does not perform the next bounded unit definition surface preparation.",
            "C.2 does not change authority state.",
            "C.2 does not consume human acceptance.",
            "C.2 does not rewrite receipts.",
            "C.2 does not generalize the router.",
            "C.2 does not activate a runner.",
            "C.2 does not audit the candidate as promoted or reusable.",
            "C.2 only represents one local router specimen as a candidate archive entry.",
            "candidate archive entry != reusable archive entry",
        ],
        "unsafe_to_infer": [
            "Unsafe to infer: the candidate is promoted.",
            "Unsafe to infer: reuse authority is granted.",
            "Unsafe to infer: auto-disposition is allowed.",
            "Unsafe to infer: the candidate move was performed.",
            "Unsafe to infer: authority changed.",
            "Unsafe to infer: a runner was activated.",
            "Unsafe to infer: a preapproved archive entry exists.",
            "Unsafe to infer: an active archive entry exists.",
        ],
        "terminal_transition": "ADVANCE(C3_CANDIDATE_ARCHIVE_ADMISSIBILITY_AUDIT_PENDING)",
    }
    validate_record(record)
    return record


def validate_record(record: dict[str, Any]) -> None:
    if record["archive_entry_status"] != ARCHIVE_ENTRY_STATUS:
        fail(FAIL_ENTRY_STATUS_NOT_CANDIDATE)
    if record["promotion_status"] != PROMOTION_STATUS:
        fail(FAIL_PROMOTION_STATUS_MISSING)
    if record["reuse_authority_status"] != REUSE_AUTHORITY_STATUS:
        fail(FAIL_REUSE_STATUS_MISSING)
    if record["activation_status"] != ACTIVATION_STATUS:
        fail(FAIL_ACTIVATION_STATUS_MISSING)
    move = record["candidate_move_shape"]
    if move["allowed_basis_scope"] != BASIS_SCOPE:
        fail(FAIL_SCOPE_MISSING)
    if move["allowed_source_object_id"] != SOURCE_OBJECT_ID:
        fail(FAIL_SOURCE_OBJECT_SCOPE_OVERBROAD)
    if "ANY_ACCEPTED_BASIS_OBJECT" in json.dumps(record, sort_keys=True):
        fail(FAIL_SOURCE_OBJECT_SCOPE_OVERBROAD)
    machine = record["candidate_machine_scope"]
    if machine["radius_limit_now"] != "RADIUS_0_CANDIDATE_ONLY":
        fail(FAIL_RADIUS_MISSING)
    if machine["candidate_move_performed_now"] is not False:
        fail(FAIL_PREPARATION_PERFORMED)
    conformance = record["contract_conformance_map"]
    if conformance.get("required_field_group_count") != 18 or conformance.get("all_required_groups_declared") is not True:
        fail(FAIL_CONTRACT_CONFORMANCE_MAP_MISSING)
    for group_id in REQUIRED_GROUP_IDS:
        if conformance.get(group_id) != "DECLARED":
            fail(FAIL_CONTRACT_CONFORMANCE_MAP_MISSING, group_id)
    if len(record["required_validators_if_promoted"]) != 7:
        fail(FAIL_VALIDATORS_MISSING)
    if len(record["required_receipts_if_promoted"]) != 4:
        fail(FAIL_RECEIPTS_MISSING)
    if len(record["mandatory_halts_if_promoted"]) < 10:
        fail(FAIL_HALTS_MISSING)
    if len(record["mandatory_escalations_if_promoted"]) < 6:
        fail(FAIL_ESCALATIONS_MISSING)
    if not record["forbidden_effects_now"] or not record["forbidden_effects_even_if_promoted_unless_separately_declared"]:
        fail(FAIL_FORBIDDEN_EFFECTS_MISSING)
    if record["source_commit_freshness"].get("source_freshness_status") != "SOURCE_COMMIT_VERIFIED":
        fail(FAIL_FRESHNESS_RULES_MISSING)
    boundary = record["promotion_boundary"]
    if boundary["promotion_granted_by_this_entry"] is not False:
        fail(FAIL_PROMOTION_SMUGGLED)
    if boundary["reuse_authority_granted_by_this_entry"] is not False:
        fail(FAIL_REUSE_AUTHORITY_SMUGGLED)
    if boundary["preapproved_archive_entry_created"] is not False:
        fail(FAIL_PREAPPROVED_ENTRY_CREATED)
    if boundary["active_archive_entry_created"] is not False:
        fail(FAIL_ACTIVE_ENTRY_CREATED)
    for gate_name in ["candidate_non_promotion_gate", "candidate_entry_gate_summary"]:
        gate = record[gate_name]
        if gate["promotion_granted"] is not False:
            fail(FAIL_PROMOTION_SMUGGLED)
        if gate["reuse_authority_granted"] is not False:
            fail(FAIL_REUSE_AUTHORITY_SMUGGLED)
        if gate["auto_disposition_allowed"] is not False:
            fail(FAIL_AUTO_DISPOSITION_SMUGGLED)
        if gate["action_executed"] is not False:
            fail(FAIL_ACTION_EXECUTED)
        if gate["candidate_move_performed"] is not False:
            fail(FAIL_PREPARATION_PERFORMED)
        if gate["authority_changed"] is not False:
            fail(FAIL_AUTHORITY_CHANGED)
        if gate["runner_authority_created"] is not False:
            fail(FAIL_RUNNER_AUTHORITY_CREATED)
        if gate["preapproved_archive_entry_created"] is not False:
            fail(FAIL_PREAPPROVED_ENTRY_CREATED)
        if gate["active_archive_entry_created"] is not False:
            fail(FAIL_ACTIVE_ENTRY_CREATED)
        if gate["failures"] != []:
            fail(FAIL_MARKDOWN_JSON_PARITY, f"{gate_name}.failures")
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
        "docs/matrixlabs/validator_archive/c8_n22_candidate_archive_admissibility_audit_v0.json",
        "docs/matrixlabs/validator_archive/candidates/c8_n22_candidate_archive_admissibility_audit_v0.json",
        "scripts/build_c8_n22_candidate_archive_admissibility_audit_v0.py",
        "docs/matrixlabs/validator_archive/promotion_receipt_v0.json",
        "docs/matrixlabs/validator_archive/activation_object_v0.json",
        "docs/matrixlabs/next_units/c8_n22_next_bounded_unit_v0.json",
        "docs/matrixlabs/next_units/c8_n22_next_bounded_unit_v0.md",
        "docs/matrixlabs/observability/c8_observed_decision_path_update_c2_proposal_v0.json",
        "docs/matrixlabs/observability/c8_observed_path_update_c2_apply_v0.json",
    ]
    existing = [path for path in forbidden if (root / path).exists()]
    if existing:
        fail(FAIL_ACTIVE_ENTRY_CREATED, ",".join(existing))


def render_markdown(record: dict[str, Any]) -> str:
    move = record["candidate_move_shape"]
    validators = [item["validator"].replace("_", " ") for item in record["required_validators_if_promoted"]]
    lines = [
        "# C8 n22 prepare next unit definition candidate archive entry v0",
        "",
        "## Status",
        "",
        record["candidate_entry_gate_summary"]["candidate_entry_gate"],
        "",
        "## Entry status",
        "",
        record["archive_entry_status"],
        "",
        "## Promotion status",
        "",
        record["promotion_status"],
        "",
        "## Reuse authority",
        "",
        record["reuse_authority_status"],
        "",
        "## Activation status",
        "",
        record["activation_status"],
        "",
        "## Source specimen",
        "",
        record["source_specimen"]["router_specimen_closure_id"],
        "",
        "## Candidate move shape",
        "",
        f"- authority state: {move['allowed_current_authority_state']}",
        f"- requested action: {move['allowed_requested_action']}",
        f"- requested scope: {move['allowed_requested_action_scope']}",
        f"- basis scope: {move['allowed_basis_scope']}",
        f"- source object: {move['allowed_source_object_id']}",
        f"- output kind: {move['allowed_output_kind']}",
        "",
        "## Radius now",
        "",
        record["candidate_machine_scope"]["radius_limit_now"],
        "",
        "## Required if ever promoted",
        "",
    ]
    lines.extend(f"- {validator}" for validator in validators)
    lines.extend(
        [
            "- requested action record",
            "- route classification record",
            "- preparation receipt",
            "- closeout receipt",
            "",
            "## Forbidden now",
            "",
            "- execution",
            "- performance of the next bounded unit definition surface preparation",
            "- authority change",
            "- receipt rewrite",
            "- taxonomy promotion",
            "- reuse authorization",
            "- updater generalization",
            "- runner activation",
            "- preapproved archive entry creation",
            "- active archive entry creation",
            "",
            "## Non-claim",
            "",
            "This candidate does not authorize reuse, automation, promotion, activation, or execution.",
            "",
            "## Non-claims",
        ]
    )
    lines.extend(f"- {claim}" for claim in record["non_claims"])
    return "\n".join(lines).rstrip() + "\n"


def validate_markdown(record: dict[str, Any], markdown: str) -> None:
    required = [
        "# C8 n22 prepare next unit definition candidate archive entry v0",
        CANDIDATE_ENTRY_GATE,
        ARCHIVE_ENTRY_STATUS,
        PROMOTION_STATUS,
        REUSE_AUTHORITY_STATUS,
        ACTIVATION_STATUS,
        ROUTER_SPECIMEN_CLOSURE_ID,
        f"- authority state: {CURRENT_AUTHORITY_STATE}",
        f"- requested action: {REQUESTED_ACTION_VALUE}",
        f"- requested scope: {REQUESTED_ACTION_SCOPE}",
        f"- basis scope: {BASIS_SCOPE}",
        f"- source object: {SOURCE_OBJECT_ID}",
        f"- output kind: {OUTPUT_KIND}",
        "RADIUS_0_CANDIDATE_ONLY",
        "- authority state match validator",
        "- requested action scope validator",
        "- basis scope validator",
        "- forbidden effects validator",
        "- output shape validator",
        "- freshness validator",
        "- radius validator",
        "- requested action record",
        "- route classification record",
        "- preparation receipt",
        "- closeout receipt",
        "- performance of the next bounded unit definition surface preparation",
        "- preapproved archive entry creation",
        "- active archive entry creation",
        "This candidate does not authorize reuse, automation, promotion, activation, or execution.",
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
    source = record["source_specimen"]
    freshness = record["source_commit_freshness"]
    move = record["candidate_move_shape"]
    machine = record["candidate_machine_scope"]
    conformance = record["contract_conformance_map"]
    summary = record["candidate_entry_gate_summary"]
    print("BUILD_C8_N22_PREPARE_NEXT_UNIT_DEFINITION_CANDIDATE_ARCHIVE_ENTRY_V0_COMPLETE")
    print(f"archive_entry_id={record['archive_entry_id']}")
    print(f"schema_version={record['schema_version']}")
    print(f"entry_role={record['entry_role']}")
    print(f"entry_kind={record['entry_kind']}")
    print(f"archive_entry_status={record['archive_entry_status']}")
    print(f"source_schema_contract_id={record['source_schema_contract_id']}")
    print(f"promotion_status={record['promotion_status']}")
    print(f"reuse_authority_status={record['reuse_authority_status']}")
    print(f"activation_status={record['activation_status']}")
    print(f"activation_status_reason={record['activation_status_reason']}")
    print(f"preapproved_archive_entry_status={record['preapproved_archive_entry_status']}")
    print(f"active_archive_entry_status={record['active_archive_entry_status']}")
    print(f"auto_disposition_status={record['auto_disposition_status']}")
    print(f"runner_authority_status={record['runner_authority_status']}")
    print(f"router_specimen_closure_id={source['router_specimen_closure_id']}")
    print(f"route_classification_id={source['route_classification_id']}")
    print(f"requested_action_record_id={source['requested_action_record_id']}")
    print(f"authority_state_update_id={source['authority_state_update_id']}")
    print(f"authority_transition_closure_id={source['authority_transition_closure_id']}")
    print(f"source_freshness_status={freshness['source_freshness_status']}")
    print(f"allowed_current_authority_state={move['allowed_current_authority_state']}")
    print(f"allowed_requested_action={move['allowed_requested_action']}")
    print(f"allowed_requested_action_scope={move['allowed_requested_action_scope']}")
    print(f"allowed_basis_scope={move['allowed_basis_scope']}")
    print(f"allowed_source_object_id={move['allowed_source_object_id']}")
    print(f"allowed_output_kind={move['allowed_output_kind']}")
    print(f"machine_action_scope_if_promoted={machine['machine_action_scope_if_promoted']}")
    print(f"machine_action_scope_now={machine['machine_action_scope_now']}")
    print(f"radius_limit_now={machine['radius_limit_now']}")
    print(f"proposed_radius_limit_if_promoted={machine['proposed_radius_limit_if_promoted']}")
    print(f"contract_conformance_group_count={conformance['required_field_group_count']}")
    print(f"all_required_groups_declared={str(conformance['all_required_groups_declared']).lower()}")
    print(f"candidate_representation_gate={summary['candidate_representation_gate']}")
    print(f"candidate_non_promotion_gate={summary['candidate_non_promotion_gate']}")
    print(f"candidate_entry_gate={summary['candidate_entry_gate']}")
    print(f"candidate_archive_entry_created={str(summary['candidate_archive_entry_created']).lower()}")
    print(f"promotion_granted={str(summary['promotion_granted']).lower()}")
    print(f"reuse_authority_granted={str(summary['reuse_authority_granted']).lower()}")
    print(f"auto_disposition_allowed={str(summary['auto_disposition_allowed']).lower()}")
    print(f"action_executed={str(summary['action_executed']).lower()}")
    print(f"candidate_move_performed={str(summary['candidate_move_performed']).lower()}")
    print(f"authority_changed={str(summary['authority_changed']).lower()}")
    print(f"runner_authority_created={str(summary['runner_authority_created']).lower()}")
    print(f"preapproved_archive_entry_created={str(summary['preapproved_archive_entry_created']).lower()}")
    print(f"active_archive_entry_created={str(summary['active_archive_entry_created']).lower()}")
    print("c3_created=false")
    print("promotion_receipt_created=false")
    print("activation_object_created=false")
    print("next_unit_defined=false")
    print("next_unit_authorized=false")
    print("next_unit_definition_surface_prepared=false")
    print("observed_path_updated=false")
    print("observed_path_update_proposed=false")
    print("commit_created=false")
    print("push_executed=false")
    print("terminal_transition=ADVANCE(C3_CANDIDATE_ARCHIVE_ADMISSIBILITY_AUDIT_PENDING)")


def main() -> int:
    try:
        root = detect_repo_root(Path.cwd())
        record = build_record(root)
        write_outputs(root, record)
    except GenerationError as exc:
        print(f"STOP_{exc.code}")
        return 2
    print_success(record)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
