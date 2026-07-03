#!/usr/bin/env python3
"""Build the C8 n22 read-only router specimen closure v0.

This closes the actual committed B.2 routing specimen. It copies B.2's route
result and preserves the non-effects; it does not reroute or prepare output.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_read_only_router_specimen_closure_v0.py"
OUTPUT_JSON = "docs/matrixlabs/router/c8_n22_read_only_router_specimen_closure_v0.json"
OUTPUT_MD = "docs/matrixlabs/router/c8_n22_read_only_router_specimen_closure_v0.md"

AUTHORITY_CLOSURE = "docs/matrixlabs/boundary/c8_n22_authority_transition_closure_v0.json"
REQUESTED_ACTION = "docs/matrixlabs/router/c8_n22_requested_action_prepare_next_unit_definition_surface_v0.json"
ROUTE_CLASSIFICATION = "docs/matrixlabs/router/c8_n22_authority_route_classification_v0.json"

A4_COMMIT = "7e8a1b5594f3ee725d0393ab27433b7650ec489d"
B1_COMMIT = "636324fbd28e6bdcc895144d82e47311fcdd5f72"
B2_COMMIT = "b6f19b7de99a7d074091c38661e4ceb28ba3d378"

SCHEMA_VERSION = "matrixlabs_read_only_router_specimen_closure_v0"
ROUTER_SPECIMEN_CLOSURE_ID = "c8.n22.router_specimen_closure.v0"
CLOSURE_ROLE = "BLOCK_B_READ_ONLY_ROUTER_SPECIMEN_CLOSURE"
CLOSURE_MODE = "CLOSE_ACTUAL_COMMITTED_B2_RESULT_ONLY"
BLOCK_ID = "BLOCK_B"
BLOCK_STATUS = "BLOCK_B_PASS_READ_ONLY_ROUTE_CLASSIFIED"
CLOSURE_STATUS = "ROUTER_SPECIMEN_CLOSURE_PASS_ALLOWED_PREPARE_ONLY"

AUTHORITY_TRANSITION_CLOSURE_ID = "c8.n22.authority_transition_closure.v0"
REQUESTED_ACTION_RECORD_ID = "c8.n22.request.prepare_next_bounded_unit_definition_surface.v0"
ROUTE_CLASSIFICATION_ID = "c8.n22.route.prepare_next_unit_definition_surface.v0"

CURRENT_AUTHORITY_STATE = "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION"
BASIS_SCOPE = "C8_N22_BASIS_ONLY"
REQUESTED_ACTION_VALUE = "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"
REQUESTED_ACTION_SCOPE = "PREPARE_SURFACE_ONLY"
REQUESTED_OUTPUT_KIND = "NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"
REQUESTED_TARGET_BASIS = "c8.n22"

ROUTE_DISPOSITION = "ROUTE_MACHINE_MAY_PREPARE_ONLY"
CLASSIFIED_ACTION_STATUS = "ADMISSIBLE_AS_SEPARATE_PREPARATION_OBJECT"
ALLOWED_MACHINE_ACTION_SCOPE = "PREPARE_SURFACE_ONLY"
ALLOWED_SCOPE = "C8_N22_BASIS_ONLY"
HALT_CODE = "NONE"
ESCALATION_CODE = "NONE"

OBJECT_CLASS = "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE_OBJECT"
OBJECT_STATUS = "LAWFUL_TO_PREPARE_SEPARATELY"
SPECIMEN_KIND = "READ_ONLY_AUTHORITY_ROUTING_SPECIMEN"
SPECIMEN_STATUS = "ARCHIVABLE_LOCAL_SPECIMEN"

FAIL_AUTHORITY_CLOSURE_MISSING = "ROUTER_CLOSURE_FAIL_AUTHORITY_CLOSURE_MISSING"
FAIL_REQUESTED_ACTION_MISSING = "ROUTER_CLOSURE_FAIL_REQUESTED_ACTION_MISSING"
FAIL_ROUTE_CLASSIFICATION_MISSING = "ROUTER_CLOSURE_FAIL_ROUTE_CLASSIFICATION_MISSING"
FAIL_SOURCE_CHAIN_INCOMPLETE = "ROUTER_CLOSURE_FAIL_SOURCE_CHAIN_INCOMPLETE"
FAIL_ROUTE_RESULT_MISSING = "ROUTER_CLOSURE_FAIL_ROUTE_RESULT_MISSING"
FAIL_ROUTE_RESULT_MISMATCH = "ROUTER_CLOSURE_FAIL_ROUTE_RESULT_MISMATCH"
FAIL_ACTION_EXECUTED = "ROUTER_CLOSURE_FAIL_ACTION_EXECUTED"
FAIL_REQUESTED_OUTPUT_CREATED = "ROUTER_CLOSURE_FAIL_REQUESTED_OUTPUT_CREATED"
FAIL_AUTHORITY_CHANGED = "ROUTER_CLOSURE_FAIL_AUTHORITY_CHANGED"
FAIL_RECEIPT_REWRITTEN = "ROUTER_CLOSURE_FAIL_RECEIPT_REWRITTEN"
FAIL_SCHEMA_PROMOTED = "ROUTER_CLOSURE_FAIL_SCHEMA_PROMOTED"
FAIL_REUSE_AUTHORIZED = "ROUTER_CLOSURE_FAIL_REUSE_AUTHORIZED"
FAIL_UPDATER_GENERALIZED = "ROUTER_CLOSURE_FAIL_UPDATER_GENERALIZED"
FAIL_RUNNER_AUTHORITY_CREATED = "ROUTER_CLOSURE_FAIL_RUNNER_AUTHORITY_CREATED"
FAIL_ROUTER_AUTHORITY_CREATED = "ROUTER_CLOSURE_FAIL_ROUTER_AUTHORITY_CREATED"
FAIL_REUSABLE_ROUTER_CREATED = "ROUTER_CLOSURE_FAIL_REUSABLE_ROUTER_CREATED"
FAIL_SPECIMEN_OVERCLAIMED_REUSABLE = "ROUTER_CLOSURE_FAIL_SPECIMEN_OVERCLAIMED_REUSABLE"
FAIL_NEXT_SURFACE_PREPARED = "ROUTER_CLOSURE_FAIL_NEXT_SURFACE_PREPARED_INSIDE_CLOSURE"
FAIL_VALIDATOR_ARCHIVE_ENTRY_CREATED = "ROUTER_CLOSURE_FAIL_VALIDATOR_ARCHIVE_ENTRY_CREATED"
FAIL_OBSERVED_PATH_UPDATE_SMUGGLED = "ROUTER_CLOSURE_FAIL_OBSERVED_PATH_UPDATE_SMUGGLED"
FAIL_RECOMMENDATION_INSERTED = "ROUTER_CLOSURE_FAIL_RECOMMENDATION_INSERTED"
FAIL_MARKDOWN_JSON_PARITY = "ROUTER_CLOSURE_FAIL_MARKDOWN_JSON_PARITY"

ROUTER_NON_EFFECTS = {
    "classification_only": True,
    "requested_action_executed": False,
    "requested_output_created": False,
    "authority_changed": False,
    "receipt_rewritten": False,
    "schema_promoted": False,
    "reuse_authorized": False,
    "updater_generalized": False,
    "runner_authority_created": False,
    "router_authority_created": False,
    "reusable_router_created": False,
    "validator_archive_created": False,
    "next_unit_defined": False,
    "next_unit_authorized": False,
    "next_unit_definition_surface_prepared": False,
    "observed_path_updated": False,
    "observed_path_update_proposed": False,
}

RECOMMENDATION_PHRASES = [
    "go ahead",
    "approved forever",
    "safe route",
    "now execute",
    "router is runner",
    "request approved",
    "should proceed",
    "recommended",
    "best next move",
    "correct next move",
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
    run_git(root, ["cat-file", "-e", f"{A4_COMMIT}^{{commit}}"], FAIL_AUTHORITY_CLOSURE_MISSING)
    run_git(root, ["cat-file", "-e", f"{B1_COMMIT}^{{commit}}"], FAIL_REQUESTED_ACTION_MISSING)
    run_git(root, ["cat-file", "-e", f"{B2_COMMIT}^{{commit}}"], FAIL_ROUTE_CLASSIFICATION_MISSING)
    a4_got = commit_for_paths(
        root,
        [
            AUTHORITY_CLOSURE,
            "docs/matrixlabs/boundary/c8_n22_authority_transition_closure_v0.md",
            "scripts/build_c8_n22_authority_transition_closure_v0.py",
        ],
        FAIL_AUTHORITY_CLOSURE_MISSING,
    )
    if a4_got != A4_COMMIT:
        fail(FAIL_AUTHORITY_CLOSURE_MISSING, f"A4 commit mismatch: {a4_got}!={A4_COMMIT}")
    b1_got = commit_for_paths(
        root,
        [
            REQUESTED_ACTION,
            "docs/matrixlabs/router/c8_n22_requested_action_prepare_next_unit_definition_surface_v0.md",
            "scripts/build_c8_n22_requested_action_prepare_next_unit_definition_surface_v0.py",
        ],
        FAIL_REQUESTED_ACTION_MISSING,
    )
    if b1_got != B1_COMMIT:
        fail(FAIL_REQUESTED_ACTION_MISSING, f"B1 commit mismatch: {b1_got}!={B1_COMMIT}")
    b2_got = commit_for_paths(
        root,
        [
            ROUTE_CLASSIFICATION,
            "docs/matrixlabs/router/c8_n22_authority_route_classification_v0.md",
            "scripts/build_c8_n22_authority_route_classification_v0.py",
        ],
        FAIL_ROUTE_CLASSIFICATION_MISSING,
    )
    if b2_got != B2_COMMIT:
        fail(FAIL_ROUTE_CLASSIFICATION_MISSING, f"B2 commit mismatch: {b2_got}!={B2_COMMIT}")


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


def scan_text_for_recommendations(text: str) -> list[str]:
    lowered = text.lower()
    return [phrase for phrase in RECOMMENDATION_PHRASES if phrase in lowered]


def expect(value: object, wanted: object, failure_code: str, field: str) -> None:
    if value != wanted:
        fail(failure_code, f"{field}: {value!r}!={wanted!r}")


def validate_source_chain(authority: dict[str, Any], request: dict[str, Any], route: dict[str, Any]) -> None:
    expect(authority.get("closure_id"), AUTHORITY_TRANSITION_CLOSURE_ID, FAIL_AUTHORITY_CLOSURE_MISSING, "closure_id")
    expect(authority.get("closure_gate", {}).get("closure_status"), "AUTHORITY_TRANSITION_CLOSURE_PASS", FAIL_AUTHORITY_CLOSURE_MISSING, "closure_status")
    expect(authority.get("block", {}).get("block_status"), "BLOCK_A_PASS_AUTHORITY_ADVANCED_TO_BASIS", FAIL_AUTHORITY_CLOSURE_MISSING, "block_status")

    expect(request.get("requested_action_record_id"), REQUESTED_ACTION_RECORD_ID, FAIL_REQUESTED_ACTION_MISSING, "requested_action_record_id")
    expect(request.get("record_role"), "ROUTER_INPUT_REQUESTED_ACTION", FAIL_REQUESTED_ACTION_MISSING, "record_role")
    movement = request.get("requested_movement", {})
    expect(movement.get("requested_action"), REQUESTED_ACTION_VALUE, FAIL_REQUESTED_ACTION_MISSING, "requested_action")
    expect(movement.get("requested_action_scope"), REQUESTED_ACTION_SCOPE, FAIL_REQUESTED_ACTION_MISSING, "requested_action_scope")
    expect(movement.get("requested_output_kind"), REQUESTED_OUTPUT_KIND, FAIL_REQUESTED_ACTION_MISSING, "requested_output_kind")
    expect(movement.get("requested_target_basis"), REQUESTED_TARGET_BASIS, FAIL_REQUESTED_ACTION_MISSING, "requested_target_basis")

    expect(route.get("schema_version"), "matrixlabs_authority_route_classification_v0", FAIL_ROUTE_CLASSIFICATION_MISSING, "route_schema")
    expect(route.get("route_classification_id"), ROUTE_CLASSIFICATION_ID, FAIL_ROUTE_CLASSIFICATION_MISSING, "route_classification_id")
    expect(route.get("router_role"), "READ_ONLY_AUTHORITY_ROUTER", FAIL_ROUTE_CLASSIFICATION_MISSING, "router_role")
    expect(route.get("router_mode"), "CLASSIFY_ONLY_NO_ACTION", FAIL_ROUTE_CLASSIFICATION_MISSING, "router_mode")

    source = route.get("source_authority", {})
    expect(source.get("current_authority_state"), CURRENT_AUTHORITY_STATE, FAIL_SOURCE_CHAIN_INCOMPLETE, "current_authority_state")
    expect(source.get("basis_scope"), BASIS_SCOPE, FAIL_SOURCE_CHAIN_INCOMPLETE, "basis_scope")
    route_request = route.get("requested_action", {})
    expect(route_request.get("requested_action"), REQUESTED_ACTION_VALUE, FAIL_SOURCE_CHAIN_INCOMPLETE, "route_requested_action")
    expect(route_request.get("requested_action_scope"), REQUESTED_ACTION_SCOPE, FAIL_SOURCE_CHAIN_INCOMPLETE, "route_requested_action_scope")
    expect(route_request.get("requested_output_kind"), REQUESTED_OUTPUT_KIND, FAIL_SOURCE_CHAIN_INCOMPLETE, "route_requested_output_kind")
    expect(route_request.get("requested_target_basis"), REQUESTED_TARGET_BASIS, FAIL_SOURCE_CHAIN_INCOMPLETE, "route_requested_target_basis")

    classification = route.get("classification")
    if not isinstance(classification, dict):
        fail(FAIL_ROUTE_RESULT_MISSING)
    expected_classification = {
        "route_disposition": ROUTE_DISPOSITION,
        "classified_action_status": CLASSIFIED_ACTION_STATUS,
        "allowed_machine_action_scope": ALLOWED_MACHINE_ACTION_SCOPE,
        "allowed_scope": ALLOWED_SCOPE,
        "halt_code": HALT_CODE,
        "escalation_code": ESCALATION_CODE,
    }
    for key, value in expected_classification.items():
        expect(classification.get(key), value, FAIL_ROUTE_RESULT_MISMATCH, key)

    gate = route.get("router_gate", {})
    expect(gate.get("router_gate_status"), "ROUTER_PASS_CLASSIFICATION_ONLY", FAIL_ROUTE_CLASSIFICATION_MISSING, "router_gate_status")
    expect(gate.get("route_classification_emitted"), True, FAIL_ROUTE_CLASSIFICATION_MISSING, "route_classification_emitted")
    expect(gate.get("router_classification_record_created"), True, FAIL_ROUTE_CLASSIFICATION_MISSING, "router_classification_record_created")
    if gate.get("action_executed") is not False:
        fail(FAIL_ACTION_EXECUTED)
    if gate.get("requested_output_created") is not False:
        fail(FAIL_REQUESTED_OUTPUT_CREATED)
    if gate.get("authority_changed") is not False:
        fail(FAIL_AUTHORITY_CHANGED)
    if gate.get("receipt_rewritten") is not False:
        fail(FAIL_RECEIPT_REWRITTEN)
    if gate.get("schema_promoted") is not False:
        fail(FAIL_SCHEMA_PROMOTED)
    if gate.get("reuse_authorized") is not False:
        fail(FAIL_REUSE_AUTHORIZED)
    if gate.get("updater_generalized") is not False:
        fail(FAIL_UPDATER_GENERALIZED)
    if gate.get("runner_authority_created") is not False:
        fail(FAIL_RUNNER_AUTHORITY_CREATED)
    if gate.get("router_authority_created") is not False:
        fail(FAIL_ROUTER_AUTHORITY_CREATED)
    if gate.get("reusable_router_created") is not False:
        fail(FAIL_REUSABLE_ROUTER_CREATED)
    if gate.get("validator_archive_created") is not False:
        fail(FAIL_VALIDATOR_ARCHIVE_ENTRY_CREATED)
    if gate.get("observed_path_updated") is not False or gate.get("observed_path_update_proposed") is not False:
        fail(FAIL_OBSERVED_PATH_UPDATE_SMUGGLED)


def build_record(root: Path) -> dict[str, Any]:
    verify_expected_commits(root)
    authority = load_json(root, AUTHORITY_CLOSURE, FAIL_AUTHORITY_CLOSURE_MISSING)
    request = load_json(root, REQUESTED_ACTION, FAIL_REQUESTED_ACTION_MISSING)
    route = load_json(root, ROUTE_CLASSIFICATION, FAIL_ROUTE_CLASSIFICATION_MISSING)
    validate_source_chain(authority, request, route)

    classification = route["classification"]
    route_result = {
        "route_disposition": classification["route_disposition"],
        "classified_action_status": classification["classified_action_status"],
        "allowed_machine_action_scope": classification["allowed_machine_action_scope"],
        "allowed_scope": classification["allowed_scope"],
        "halt_code": classification["halt_code"],
        "escalation_code": classification["escalation_code"],
    }
    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "router_specimen_closure_id": ROUTER_SPECIMEN_CLOSURE_ID,
        "closure_role": CLOSURE_ROLE,
        "closure_mode": CLOSURE_MODE,
        "block_id": BLOCK_ID,
        "block_status": BLOCK_STATUS,
        "block_terminal": True,
        "generated_by": GENERATOR,
        "source": {
            "authority_transition_closure_commit_sha": A4_COMMIT,
            "authority_transition_closure_path": AUTHORITY_CLOSURE,
            "authority_transition_closure_sha256": sha256_file(root / AUTHORITY_CLOSURE),
            "requested_action_record_commit_sha": B1_COMMIT,
            "requested_action_record_path": REQUESTED_ACTION,
            "requested_action_record_sha256": sha256_file(root / REQUESTED_ACTION),
            "route_classification_commit_sha": B2_COMMIT,
            "route_classification_path": ROUTE_CLASSIFICATION,
            "route_classification_sha256": sha256_file(root / ROUTE_CLASSIFICATION),
        },
        "source_chain": {
            "authority_transition_closure_id": AUTHORITY_TRANSITION_CLOSURE_ID,
            "requested_action_record_id": REQUESTED_ACTION_RECORD_ID,
            "route_classification_id": ROUTE_CLASSIFICATION_ID,
            "source_chain_complete": True,
        },
        "routed_state": {
            "current_authority_state": route["source_authority"]["current_authority_state"],
            "basis_scope": route["source_authority"]["basis_scope"],
        },
        "routed_request": {
            "requested_action": route["requested_action"]["requested_action"],
            "requested_action_scope": route["requested_action"]["requested_action_scope"],
            "requested_output_kind": route["requested_action"]["requested_output_kind"],
            "requested_target_basis": route["requested_action"]["requested_target_basis"],
        },
        "route_result_copied_from_b2": route_result,
        "router_non_effects": dict(ROUTER_NON_EFFECTS),
        "next_separately_preparable_object_class": {
            "object_class": OBJECT_CLASS,
            "object_status": OBJECT_STATUS,
            "basis_scope": BASIS_SCOPE,
            "performed_by_b3": False,
            "created_by_b3": False,
            "requires_separate_preparation_object": True,
        },
        "specimen_archive": {
            "specimen_kind": SPECIMEN_KIND,
            "specimen_status": SPECIMEN_STATUS,
            "may_support_future_router_analysis": True,
            "may_authorize_future_reuse": False,
            "may_serve_as_validator_archive_entry": False,
            "may_preapprove_future_routes": False,
            "may_create_reusable_router_authority": False,
        },
        "closure_gate": {
            "closure_status": CLOSURE_STATUS,
            "authority_transition_closure_present": True,
            "requested_action_record_present": True,
            "route_classification_present": True,
            "source_chain_complete": True,
            "current_authority_state": CURRENT_AUTHORITY_STATE,
            "requested_action": REQUESTED_ACTION_VALUE,
            "requested_action_scope": REQUESTED_ACTION_SCOPE,
            **route_result,
            "route_result_copied_exactly_from_b2": True,
            **ROUTER_NON_EFFECTS,
            "next_separately_preparable_object_class": OBJECT_CLASS,
            "performed_by_b3": False,
            "created_by_b3": False,
            "requires_separate_preparation_object": True,
            "specimen_status": SPECIMEN_STATUS,
            "may_support_future_router_analysis": True,
            "may_authorize_future_reuse": False,
            "may_serve_as_validator_archive_entry": False,
            "may_preapprove_future_routes": False,
            "may_create_reusable_router_authority": False,
            "stronger_authority_detected": False,
            "reusable_authority_detected": False,
            "validator_archive_entry_created": False,
            "observed_path_mutation_detected": False,
            "failures": [],
        },
        "non_claims": [
            "B.3 does not execute the requested action.",
            "B.3 does not create requested output.",
            "B.3 does not prepare the next bounded unit definition surface.",
            "B.3 does not define the next bounded unit.",
            "B.3 does not authorize the next bounded unit.",
            "B.3 does not change authority.",
            "B.3 does not apply a decision.",
            "B.3 does not rewrite receipts.",
            "B.3 does not promote schema.",
            "B.3 does not authorize reuse.",
            "B.3 does not generalize updater.",
            "B.3 does not create runner authority.",
            "B.3 does not create reusable router authority.",
            "B.3 does not make this routing pattern reusable.",
            "B.3 does not create a validator archive entry.",
            "B.3 does not update the observed path.",
            "B.3 only closes and preserves one read-only routing specimen.",
        ],
        "unsafe_to_infer": [
            "Unsafe to infer: B.3 performed the requested preparation.",
            "Unsafe to infer: requested output has been created.",
            "Unsafe to infer: the next bounded unit has been defined.",
            "Unsafe to infer: the next bounded unit has been authorized.",
            "Unsafe to infer: runtime execution is authorized.",
            "Unsafe to infer: authority state changed.",
            "Unsafe to infer: this routing pattern is reusable.",
            "Unsafe to infer: this specimen is a validator archive entry.",
            "Unsafe to infer: the observed path has been updated.",
        ],
    }
    validate_record(record)
    return record


def validate_record(record: dict[str, Any]) -> None:
    if "next_separate_object_class" in record:
        fail(FAIL_NEXT_SURFACE_PREPARED)
    gate = record["closure_gate"]
    non_effects = record["router_non_effects"]
    if gate.get("route_result_copied_exactly_from_b2") is not True:
        fail(FAIL_ROUTE_RESULT_MISMATCH)
    if non_effects.get("classification_only") is not True or gate.get("classification_only") is not True:
        fail(FAIL_ROUTE_RESULT_MISMATCH, "classification_only")
    false_checks = {
        "requested_action_executed": FAIL_ACTION_EXECUTED,
        "requested_output_created": FAIL_REQUESTED_OUTPUT_CREATED,
        "authority_changed": FAIL_AUTHORITY_CHANGED,
        "receipt_rewritten": FAIL_RECEIPT_REWRITTEN,
        "schema_promoted": FAIL_SCHEMA_PROMOTED,
        "reuse_authorized": FAIL_REUSE_AUTHORIZED,
        "updater_generalized": FAIL_UPDATER_GENERALIZED,
        "runner_authority_created": FAIL_RUNNER_AUTHORITY_CREATED,
        "router_authority_created": FAIL_ROUTER_AUTHORITY_CREATED,
        "reusable_router_created": FAIL_REUSABLE_ROUTER_CREATED,
        "validator_archive_created": FAIL_VALIDATOR_ARCHIVE_ENTRY_CREATED,
        "next_unit_defined": FAIL_NEXT_SURFACE_PREPARED,
        "next_unit_authorized": FAIL_NEXT_SURFACE_PREPARED,
        "next_unit_definition_surface_prepared": FAIL_NEXT_SURFACE_PREPARED,
        "observed_path_updated": FAIL_OBSERVED_PATH_UPDATE_SMUGGLED,
        "observed_path_update_proposed": FAIL_OBSERVED_PATH_UPDATE_SMUGGLED,
    }
    for key, failure_code in false_checks.items():
        if non_effects.get(key) is not False or gate.get(key) is not False:
            fail(failure_code, key)
    obj = record["next_separately_preparable_object_class"]
    if obj["performed_by_b3"] is not False or obj["created_by_b3"] is not False:
        fail(FAIL_NEXT_SURFACE_PREPARED)
    archive = record["specimen_archive"]
    if archive["may_authorize_future_reuse"] is not False:
        fail(FAIL_SPECIMEN_OVERCLAIMED_REUSABLE)
    if archive["may_serve_as_validator_archive_entry"] is not False:
        fail(FAIL_VALIDATOR_ARCHIVE_ENTRY_CREATED)
    if archive["may_preapprove_future_routes"] is not False:
        fail(FAIL_SPECIMEN_OVERCLAIMED_REUSABLE)
    if archive["may_create_reusable_router_authority"] is not False:
        fail(FAIL_REUSABLE_ROUTER_CREATED)
    if gate["failures"] != []:
        fail(FAIL_ROUTE_RESULT_MISMATCH, str(gate["failures"]))
    hits = scan_text_for_recommendations(json.dumps(record, sort_keys=True))
    if hits:
        fail(FAIL_RECOMMENDATION_INSERTED, str(hits))


def validate_no_forbidden_files(root: Path) -> None:
    forbidden = [
        "docs/matrixlabs/router/c8_n22_route_classification_b2b_v0.json",
        "docs/matrixlabs/router/c8_n22_route_classification_b2b_v0.md",
        "scripts/build_c8_n22_route_classification_b2b_v0.py",
        "docs/matrixlabs/router/matrixlabs_authority_router_table_v0.json",
        "docs/matrixlabs/router/matrixlabs_authority_router_table_v0.md",
        "docs/matrixlabs/validators/matrixlabs_authority_router_table_v0.json",
        "docs/matrixlabs/validators/c8_n22_router_specimen_validator_archive_v0.json",
        "docs/matrixlabs/next_units/c8_n22_next_bounded_unit_v0.json",
        "docs/matrixlabs/next_units/c8_n22_next_bounded_unit_v0.md",
        "docs/matrixlabs/observability/c8_observed_decision_path_update_b3_proposal_v0.json",
        "docs/matrixlabs/observability/c8_observed_path_update_b3_apply_v0.json",
    ]
    existing = [path for path in forbidden if (root / path).exists()]
    if existing:
        fail(FAIL_NEXT_SURFACE_PREPARED, ",".join(existing))


def render_markdown(record: dict[str, Any]) -> str:
    source = record["source_chain"]
    state = record["routed_state"]
    request = record["routed_request"]
    result = record["route_result_copied_from_b2"]
    archive = record["specimen_archive"]
    lines = [
        "# C8 n22 read-only router specimen closure v0",
        "",
        "## Status",
        "",
        record["closure_gate"]["closure_status"],
        "",
        "## Block",
        "",
        record["block_id"],
        "",
        "## Source chain",
        "",
        f"- authority transition closure: {source['authority_transition_closure_id']}",
        f"- requested action record: {source['requested_action_record_id']}",
        f"- route classification: {source['route_classification_id']}",
        "",
        "## Routed state",
        "",
        state["current_authority_state"],
        "",
        "## Requested action",
        "",
        request["requested_action"],
        "",
        "## Route disposition",
        "",
        result["route_disposition"],
        "",
        "## Next separately preparable object class",
        "",
        "A separate object is classified as lawful to prepare the next bounded unit definition surface using c8.n22 as basis.",
        "",
        "This closure did not perform that preparation.",
        "",
        "## Not performed by this closure",
        "",
        "- requested action was not executed",
        "- requested output was not created",
        "- authority was not changed",
        "- next unit was not defined",
        "- next unit was not authorized",
        "- next unit definition surface was not prepared",
        "- receipts were not rewritten",
        "- schema was not promoted",
        "- reuse was not authorized",
        "- updater was not generalized",
        "- runner authority was not created",
        "- reusable router was not created",
        "- validator archive entry was not created",
        "- observed path was not updated",
        "",
        "## Specimen status",
        "",
        archive["specimen_status"],
        "",
        "## Non-claim",
        "",
        "This closure does not make the route reusable, preapproved, executable, or a validator archive entry.",
        "",
        "## Non-claims",
    ]
    lines.extend([f"- {claim}" for claim in record["non_claims"]])
    return "\n".join(lines).rstrip() + "\n"


def validate_markdown(record: dict[str, Any], markdown: str) -> None:
    required = [
        "# C8 n22 read-only router specimen closure v0",
        "ROUTER_SPECIMEN_CLOSURE_PASS_ALLOWED_PREPARE_ONLY",
        "BLOCK_B",
        "c8.n22.authority_transition_closure.v0",
        "c8.n22.request.prepare_next_bounded_unit_definition_surface.v0",
        "c8.n22.route.prepare_next_unit_definition_surface.v0",
        "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
        "ROUTE_MACHINE_MAY_PREPARE_ONLY",
        "A separate object is classified as lawful to prepare the next bounded unit definition surface using c8.n22 as basis.",
        "This closure did not perform that preparation.",
        "ARCHIVABLE_LOCAL_SPECIMEN",
        "This closure does not make the route reusable, preapproved, executable, or a validator archive entry.",
    ]
    missing = [phrase for phrase in required if phrase not in markdown]
    if missing:
        fail(FAIL_MARKDOWN_JSON_PARITY, str(missing))
    for claim in record["non_claims"]:
        if claim not in markdown:
            fail(FAIL_MARKDOWN_JSON_PARITY, claim)
    hits = scan_text_for_recommendations(markdown)
    if hits:
        fail(FAIL_RECOMMENDATION_INSERTED, str(hits))


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
    source = record["source_chain"]
    state = record["routed_state"]
    request = record["routed_request"]
    result = record["route_result_copied_from_b2"]
    gate = record["closure_gate"]
    obj = record["next_separately_preparable_object_class"]
    archive = record["specimen_archive"]
    print("BUILD_C8_N22_READ_ONLY_ROUTER_SPECIMEN_CLOSURE_V0_COMPLETE")
    print(f"router_specimen_closure_id={record['router_specimen_closure_id']}")
    print(f"schema_version={record['schema_version']}")
    print(f"closure_role={record['closure_role']}")
    print(f"closure_mode={record['closure_mode']}")
    print(f"block_id={record['block_id']}")
    print(f"block_status={record['block_status']}")
    print(f"block_terminal={str(record['block_terminal']).lower()}")
    print(f"authority_transition_closure_id={source['authority_transition_closure_id']}")
    print(f"requested_action_record_id={source['requested_action_record_id']}")
    print(f"route_classification_id={source['route_classification_id']}")
    print(f"source_chain_complete={str(source['source_chain_complete']).lower()}")
    print(f"current_authority_state={state['current_authority_state']}")
    print(f"basis_scope={state['basis_scope']}")
    print(f"requested_action={request['requested_action']}")
    print(f"requested_action_scope={request['requested_action_scope']}")
    print(f"requested_output_kind={request['requested_output_kind']}")
    print(f"requested_target_basis={request['requested_target_basis']}")
    print(f"route_disposition={result['route_disposition']}")
    print(f"classified_action_status={result['classified_action_status']}")
    print(f"allowed_machine_action_scope={result['allowed_machine_action_scope']}")
    print(f"allowed_scope={result['allowed_scope']}")
    print(f"halt_code={result['halt_code']}")
    print(f"escalation_code={result['escalation_code']}")
    print(f"closure_status={gate['closure_status']}")
    print(f"route_result_copied_exactly_from_b2={str(gate['route_result_copied_exactly_from_b2']).lower()}")
    print(f"classification_only={str(gate['classification_only']).lower()}")
    print(f"requested_action_executed={str(gate['requested_action_executed']).lower()}")
    print(f"requested_output_created={str(gate['requested_output_created']).lower()}")
    print(f"authority_changed={str(gate['authority_changed']).lower()}")
    print(f"receipt_rewritten={str(gate['receipt_rewritten']).lower()}")
    print(f"schema_promoted={str(gate['schema_promoted']).lower()}")
    print(f"reuse_authorized={str(gate['reuse_authorized']).lower()}")
    print(f"updater_generalized={str(gate['updater_generalized']).lower()}")
    print(f"runner_authority_created={str(gate['runner_authority_created']).lower()}")
    print(f"router_authority_created={str(gate['router_authority_created']).lower()}")
    print(f"reusable_router_created={str(gate['reusable_router_created']).lower()}")
    print(f"validator_archive_created={str(gate['validator_archive_created']).lower()}")
    print(f"next_unit_defined={str(gate['next_unit_defined']).lower()}")
    print(f"next_unit_authorized={str(gate['next_unit_authorized']).lower()}")
    print(f"next_unit_definition_surface_prepared={str(gate['next_unit_definition_surface_prepared']).lower()}")
    print(f"observed_path_updated={str(gate['observed_path_updated']).lower()}")
    print(f"observed_path_update_proposed={str(gate['observed_path_update_proposed']).lower()}")
    print(f"next_separately_preparable_object_class={obj['object_class']}")
    print(f"performed_by_b3={str(obj['performed_by_b3']).lower()}")
    print(f"created_by_b3={str(obj['created_by_b3']).lower()}")
    print(f"requires_separate_preparation_object={str(obj['requires_separate_preparation_object']).lower()}")
    print(f"specimen_status={archive['specimen_status']}")
    print(f"may_support_future_router_analysis={str(archive['may_support_future_router_analysis']).lower()}")
    print(f"may_authorize_future_reuse={str(archive['may_authorize_future_reuse']).lower()}")
    print(f"may_serve_as_validator_archive_entry={str(archive['may_serve_as_validator_archive_entry']).lower()}")
    print(f"may_preapprove_future_routes={str(archive['may_preapprove_future_routes']).lower()}")
    print(f"may_create_reusable_router_authority={str(archive['may_create_reusable_router_authority']).lower()}")
    print("commit_created=false")
    print("push_executed=false")
    print("terminal_transition=STOP_BLOCK_B_CLOSED")


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
