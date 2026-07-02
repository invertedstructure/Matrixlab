#!/usr/bin/env python3
"""Build the C8 n22 read-only authority route classification v0.

This classifies the committed B.1 requested action against the formal A4/A3
authority state. It does not perform the requested action or prepare output.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_authority_route_classification_v0.py"
OUTPUT_JSON = "docs/matrixlabs/router/c8_n22_authority_route_classification_v0.json"
OUTPUT_MD = "docs/matrixlabs/router/c8_n22_authority_route_classification_v0.md"

REQUEST = "docs/matrixlabs/router/c8_n22_requested_action_prepare_next_unit_definition_surface_v0.json"
CLOSURE = "docs/matrixlabs/boundary/c8_n22_authority_transition_closure_v0.json"
UPDATE = "docs/matrixlabs/boundary/c8_n22_authority_state_update_v0.json"

B1_COMMIT = "636324fbd28e6bdcc895144d82e47311fcdd5f72"
A4_COMMIT = "7e8a1b5594f3ee725d0393ab27433b7650ec489d"
A3_COMMIT = "d8a5116ec1be3756b1ad0aa6656187c91c71e87f"

SCHEMA_VERSION = "matrixlabs_authority_route_classification_v0"
ROUTE_CLASSIFICATION_ID = "c8.n22.route.prepare_next_unit_definition_surface.v0"
ROUTER_ROLE = "READ_ONLY_AUTHORITY_ROUTER"
ROUTER_MODE = "CLASSIFY_ONLY_NO_ACTION"
ROUTER_GATE_STATUS = "ROUTER_PASS_CLASSIFICATION_ONLY"

REQUESTED_ACTION_RECORD_ID = "c8.n22.request.prepare_next_bounded_unit_definition_surface.v0"
REQUESTED_ACTION = "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"
REQUESTED_ACTION_SCOPE = "PREPARE_SURFACE_ONLY"
REQUESTED_OUTPUT_KIND = "NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"
REQUESTED_TARGET_BASIS = "c8.n22"
REQUEST_STATUS = "REQUEST_DECLARED_FOR_CLASSIFICATION_ONLY"

CURRENT_AUTHORITY_STATE = "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION"
BASIS_SCOPE = "C8_N22_BASIS_ONLY"
NEXT_ALLOWED_ROUTER_ACTION = "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"
MACHINE_PERMITTED_ACTION_SCOPE = "PREPARE_NEXT_UNIT_DEFINITION_SURFACE_ONLY"

ROUTING_TABLE_ID = "matrixlabs_authority_router_table_v0"
ROUTING_TABLE_SCOPE = "C8_N22_LOCAL_SPECIMEN"
ROUTING_TABLE_ROLE = "LOCAL_READ_ONLY_ROUTING_TABLE"
ROUTING_TABLE_AUTHORITY = "LOCAL_SPECIMEN_ONLY_NOT_REUSABLE_VALIDATOR_ARCHIVE"
ROUTING_TABLE_ENTRY_ID = "route.accepted_basis.prepare_next_unit_definition_surface.v0"

ROUTE_DISPOSITION = "ROUTE_MACHINE_MAY_PREPARE_ONLY"
CLASSIFIED_ACTION_STATUS = "ADMISSIBLE_AS_SEPARATE_PREPARATION_OBJECT"
ALLOWED_MACHINE_ACTION_SCOPE = "PREPARE_SURFACE_ONLY"
ALLOWED_SCOPE = "C8_N22_BASIS_ONLY"
HALT_CODE = "NONE"
ESCALATION_CODE = "NONE"

FAIL_AUTHORITY_STATE_MISSING = "ROUTER_FAIL_AUTHORITY_STATE_MISSING"
FAIL_REQUESTED_ACTION_MISSING = "ROUTER_FAIL_REQUESTED_ACTION_MISSING"
FAIL_REQUESTED_ACTION_INVALID = "ROUTER_FAIL_REQUESTED_ACTION_INVALID"
FAIL_REQUESTED_ACTION_UNTYPED = "ROUTER_FAIL_REQUESTED_ACTION_UNTYPED"
FAIL_REQUESTED_SCOPE_MISSING = "ROUTER_FAIL_REQUESTED_SCOPE_MISSING"
FAIL_ROUTING_TABLE_MISSING = "ROUTER_FAIL_ROUTING_TABLE_MISSING"
FAIL_ROUTING_TABLE_ENTRY_MISSING = "ROUTER_FAIL_ROUTING_TABLE_ENTRY_MISSING"
FAIL_CLASSIFICATION_MISMATCH = "ROUTER_FAIL_CLASSIFICATION_MISMATCH"
FAIL_ACTION_EXECUTED = "ROUTER_FAIL_ACTION_EXECUTED"
FAIL_REQUESTED_OUTPUT_CREATED = "ROUTER_FAIL_REQUESTED_OUTPUT_CREATED"
FAIL_AUTHORITY_CHANGED = "ROUTER_FAIL_AUTHORITY_CHANGED"
FAIL_RECEIPT_REWRITTEN = "ROUTER_FAIL_RECEIPT_REWRITTEN"
FAIL_SCHEMA_PROMOTED = "ROUTER_FAIL_SCHEMA_PROMOTED"
FAIL_REUSE_AUTHORIZED = "ROUTER_FAIL_REUSE_AUTHORIZED"
FAIL_UPDATER_GENERALIZED = "ROUTER_FAIL_UPDATER_GENERALIZED"
FAIL_RUNNER_AUTHORITY_CREATED = "ROUTER_FAIL_RUNNER_AUTHORITY_CREATED"
FAIL_REUSABLE_ROUTER_CREATED = "ROUTER_FAIL_REUSABLE_ROUTER_CREATED"
FAIL_UNSUPPORTED_AUTHORITY_CHANGE = "ROUTER_FAIL_UNSUPPORTED_AUTHORITY_CHANGE"
FAIL_LOCAL_TABLE_PROMOTED = "ROUTER_FAIL_LOCAL_TABLE_PROMOTED_TO_REUSABLE_AUTHORITY"
FAIL_ROUTE_DISPOSITION_AMBIGUOUS = "ROUTER_FAIL_ROUTE_DISPOSITION_AMBIGUOUS"
FAIL_RECOMMENDATION_INSERTED = "ROUTER_FAIL_RECOMMENDATION_INSERTED"
FAIL_MARKDOWN_JSON_PARITY = "ROUTER_FAIL_MARKDOWN_JSON_PARITY"

ALLOWED_ACTIONS = {
    "PREPARE_HUMAN_DECISION_SURFACE",
    "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
    "PREPARE_RETYPE_OR_REVISION_SURFACE",
    "PREPARE_DISCUSSION_OR_REVIEW_SURFACE",
    "CLASSIFY_ONLY",
}

AMBIGUOUS_DISPOSITIONS = {"OK", "READY", "GOOD", "APPROVED", "GO", "CONTINUE"}

RECOMMENDATION_PHRASES = [
    "request approved",
    "proceed now",
    "ready to execute",
    "should proceed",
    "recommended",
    "best next move",
    "correct next move",
    "good choice",
    "safe to execute",
    "execution is safe",
]

LOCAL_ROUTING_TABLE = {
    "routing_table_id": ROUTING_TABLE_ID,
    "routing_table_scope": ROUTING_TABLE_SCOPE,
    "routing_table_role": ROUTING_TABLE_ROLE,
    "routing_table_authority": ROUTING_TABLE_AUTHORITY,
    "entries": [
        {
            "entry_id": "route.observed_not_authorized.prepare_human_decision_surface.v0",
            "current_authority_state": "AUTH_STATE_OBSERVED_NOT_AUTHORIZED",
            "requested_action": "PREPARE_HUMAN_DECISION_SURFACE",
            "requested_action_scope": "PREPARE_SURFACE_ONLY",
            "route_disposition": "ROUTE_MACHINE_MAY_PREPARE_ONLY",
            "classified_action_status": "ADMISSIBLE_AS_SEPARATE_PREPARATION_OBJECT",
            "allowed_scope": "PREPARE_DECISION_SURFACE_ONLY",
            "halt_code": "NONE",
        },
        {
            "entry_id": "route.observed_not_authorized.prepare_next_unit_definition.v0",
            "current_authority_state": "AUTH_STATE_OBSERVED_NOT_AUTHORIZED",
            "requested_action": REQUESTED_ACTION,
            "requested_action_scope": REQUESTED_ACTION_SCOPE,
            "route_disposition": "ROUTE_BLOCKED_PENDING_HUMAN_AUTHORITY",
            "classified_action_status": "BLOCKED_PENDING_AUTHORITY_EVENT",
            "allowed_scope": "NONE",
            "halt_code": "BH_HUMAN_DECISION_REQUIRED_UNCONSUMED",
        },
        {
            "entry_id": ROUTING_TABLE_ENTRY_ID,
            "current_authority_state": CURRENT_AUTHORITY_STATE,
            "requested_action": REQUESTED_ACTION,
            "requested_action_scope": REQUESTED_ACTION_SCOPE,
            "route_disposition": ROUTE_DISPOSITION,
            "classified_action_status": CLASSIFIED_ACTION_STATUS,
            "allowed_scope": ALLOWED_SCOPE,
            "halt_code": HALT_CODE,
        },
        {
            "entry_id": "route.accepted_basis.execute_unit.v0",
            "current_authority_state": CURRENT_AUTHORITY_STATE,
            "requested_action": "EXECUTE_UNIT",
            "requested_action_scope": "EXECUTE_UNIT",
            "route_disposition": "ROUTE_HALT_MISSING_AUTHORITY",
            "classified_action_status": "HALTED_AUTHORITY_MISSING",
            "allowed_scope": "NONE",
            "halt_code": "BH_EXECUTION_AUTHORITY_MISSING",
        },
    ],
}

STILL_FORBIDDEN = {
    "next_unit_definition_finalization_authority": "NOT_GRANTED",
    "execution_authority": "NOT_GRANTED",
    "receipt_rewrite_authority": "NOT_GRANTED",
    "taxonomy_promotion_authority": "NOT_GRANTED",
    "reuse_authority": "NOT_GRANTED",
    "updater_generalization_authority": "NOT_GRANTED",
    "runner_authority": "NOT_GRANTED",
    "authority_state_change": "NOT_GRANTED_BY_ROUTER",
    "reusable_router_authority": "NOT_GRANTED",
}

DERIVED_NON_EFFECT_CHECKS = {
    "execute_unit": False,
    "prepare_requested_output": False,
    "define_next_unit": False,
    "authorize_next_unit": False,
    "rewrite_receipts": False,
    "promote_taxonomy": False,
    "authorize_reuse": False,
    "generalize_updater": False,
    "activate_runner": False,
    "change_authority_state": False,
    "create_reusable_router": False,
}


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
        fail(FAIL_AUTHORITY_STATE_MISSING, proc.stderr.strip())
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
    run_git(root, ["cat-file", "-e", f"{B1_COMMIT}^{{commit}}"], FAIL_REQUESTED_ACTION_MISSING)
    run_git(root, ["cat-file", "-e", f"{A4_COMMIT}^{{commit}}"], FAIL_AUTHORITY_STATE_MISSING)
    run_git(root, ["cat-file", "-e", f"{A3_COMMIT}^{{commit}}"], FAIL_AUTHORITY_STATE_MISSING)
    b1_got = commit_for_paths(
        root,
        [
            REQUEST,
            "docs/matrixlabs/router/c8_n22_requested_action_prepare_next_unit_definition_surface_v0.md",
            "scripts/build_c8_n22_requested_action_prepare_next_unit_definition_surface_v0.py",
        ],
        FAIL_REQUESTED_ACTION_MISSING,
    )
    if b1_got != B1_COMMIT:
        fail(FAIL_REQUESTED_ACTION_MISSING, f"B1 commit mismatch: {b1_got}!={B1_COMMIT}")
    a4_got = commit_for_paths(
        root,
        [
            CLOSURE,
            "docs/matrixlabs/boundary/c8_n22_authority_transition_closure_v0.md",
            "scripts/build_c8_n22_authority_transition_closure_v0.py",
        ],
        FAIL_AUTHORITY_STATE_MISSING,
    )
    if a4_got != A4_COMMIT:
        fail(FAIL_AUTHORITY_STATE_MISSING, f"A4 commit mismatch: {a4_got}!={A4_COMMIT}")
    a3_got = commit_for_paths(
        root,
        [
            UPDATE,
            "docs/matrixlabs/boundary/c8_n22_authority_state_update_v0.md",
            "scripts/build_c8_n22_authority_state_update_v0.py",
        ],
        FAIL_AUTHORITY_STATE_MISSING,
    )
    if a3_got != A3_COMMIT:
        fail(FAIL_AUTHORITY_STATE_MISSING, f"A3 commit mismatch: {a3_got}!={A3_COMMIT}")


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


def validate_sources(request: dict[str, Any], closure: dict[str, Any], update: dict[str, Any]) -> None:
    if request.get("schema_version") != "matrixlabs_requested_action_record_v0":
        fail(FAIL_REQUESTED_ACTION_MISSING, "schema_version")
    if request.get("requested_action_record_id") != REQUESTED_ACTION_RECORD_ID:
        fail(FAIL_REQUESTED_ACTION_MISSING, "requested_action_record_id")
    if request.get("record_role") != "ROUTER_INPUT_REQUESTED_ACTION":
        fail(FAIL_REQUESTED_ACTION_INVALID, "record_role")
    if request.get("request_status") != REQUEST_STATUS:
        fail(FAIL_REQUESTED_ACTION_INVALID, "request_status")
    movement = request.get("requested_movement", {})
    if movement.get("requested_action") != REQUESTED_ACTION:
        fail(FAIL_REQUESTED_ACTION_INVALID, "requested_action")
    if movement.get("requested_action") not in ALLOWED_ACTIONS:
        fail(FAIL_REQUESTED_ACTION_UNTYPED, str(movement.get("requested_action")))
    if movement.get("requested_action_scope") != REQUESTED_ACTION_SCOPE:
        fail(FAIL_REQUESTED_SCOPE_MISSING, "requested_action_scope")
    if movement.get("requested_output_kind") != REQUESTED_OUTPUT_KIND:
        fail(FAIL_REQUESTED_ACTION_INVALID, "requested_output_kind")
    if movement.get("requested_target_basis") != REQUESTED_TARGET_BASIS:
        fail(FAIL_REQUESTED_ACTION_INVALID, "requested_target_basis")
    if request.get("request_gate", {}).get("route_classification_emitted") is not False:
        fail(FAIL_CLASSIFICATION_MISMATCH, "B1 already emitted route classification")
    if request.get("request_gate", {}).get("requested_output_created") is not False:
        fail(FAIL_REQUESTED_OUTPUT_CREATED, "B1 requested output")

    if closure.get("closure_id") != "c8.n22.authority_transition_closure.v0":
        fail(FAIL_AUTHORITY_STATE_MISSING, "closure_id")
    closure_gate = closure.get("closure_gate", {})
    if closure_gate.get("closure_status") != "AUTHORITY_TRANSITION_CLOSURE_PASS":
        fail(FAIL_AUTHORITY_STATE_MISSING, "closure_status")
    if closure.get("block", {}).get("block_status") != "BLOCK_A_PASS_AUTHORITY_ADVANCED_TO_BASIS":
        fail(FAIL_AUTHORITY_STATE_MISSING, "block_status")
    if closure_gate.get("resulting_authority_state") != CURRENT_AUTHORITY_STATE:
        fail(FAIL_AUTHORITY_STATE_MISSING, "resulting_authority_state")
    if closure_gate.get("next_lawful_surface") != NEXT_ALLOWED_ROUTER_ACTION:
        fail(FAIL_AUTHORITY_STATE_MISSING, "next_lawful_surface")
    if closure_gate.get("machine_permitted_action_scope") != MACHINE_PERMITTED_ACTION_SCOPE:
        fail(FAIL_AUTHORITY_STATE_MISSING, "machine_permitted_action_scope")
    next_surface = closure.get("next_lawful_surface", {})
    if next_surface.get("surface_scope") != BASIS_SCOPE:
        fail(FAIL_AUTHORITY_STATE_MISSING, "surface_scope")

    if update.get("authority_update_id") != "c8.n22.authority_state_update.v0":
        fail(FAIL_AUTHORITY_STATE_MISSING, "authority_update_id")
    update_gate = update.get("update_gate", {})
    if update_gate.get("authority_state_update_gate") != "AUTHORITY_UPDATE_PASS_DECISION_APPLIED":
        fail(FAIL_AUTHORITY_STATE_MISSING, "authority_state_update_gate")
    if update.get("authority_state_after", {}).get("new_authority_state") != CURRENT_AUTHORITY_STATE:
        fail(FAIL_AUTHORITY_STATE_MISSING, "new_authority_state")
    next_router_state = update.get("next_router_state", {})
    if next_router_state.get("next_allowed_router_action") != NEXT_ALLOWED_ROUTER_ACTION:
        fail(FAIL_AUTHORITY_STATE_MISSING, "next_allowed_router_action")
    if next_router_state.get("machine_permitted_action_scope") != MACHINE_PERMITTED_ACTION_SCOPE:
        fail(FAIL_AUTHORITY_STATE_MISSING, "machine_permitted_action_scope")


def find_routing_table_entry(authority_state: str, action: str, scope: str) -> dict[str, Any]:
    if not LOCAL_ROUTING_TABLE.get("entries"):
        fail(FAIL_ROUTING_TABLE_MISSING)
    matches = [
        entry
        for entry in LOCAL_ROUTING_TABLE["entries"]
        if entry.get("current_authority_state") == authority_state
        and entry.get("requested_action") == action
        and entry.get("requested_action_scope") == scope
    ]
    if len(matches) != 1:
        fail(FAIL_ROUTING_TABLE_ENTRY_MISSING, f"{authority_state}:{action}:{scope}")
    return matches[0]


def build_record(root: Path) -> dict[str, Any]:
    verify_expected_commits(root)
    request = load_json(root, REQUEST, FAIL_REQUESTED_ACTION_MISSING)
    closure = load_json(root, CLOSURE, FAIL_AUTHORITY_STATE_MISSING)
    update = load_json(root, UPDATE, FAIL_AUTHORITY_STATE_MISSING)
    validate_sources(request, closure, update)

    movement = request["requested_movement"]
    entry = find_routing_table_entry(
        CURRENT_AUTHORITY_STATE,
        movement["requested_action"],
        movement["requested_action_scope"],
    )
    if entry.get("entry_id") != ROUTING_TABLE_ENTRY_ID:
        fail(FAIL_ROUTING_TABLE_ENTRY_MISSING, str(entry.get("entry_id")))
    if entry.get("route_disposition") in AMBIGUOUS_DISPOSITIONS:
        fail(FAIL_ROUTE_DISPOSITION_AMBIGUOUS, entry["route_disposition"])
    if entry.get("route_disposition") != ROUTE_DISPOSITION:
        fail(FAIL_CLASSIFICATION_MISMATCH, "route_disposition")
    if entry.get("classified_action_status") != CLASSIFIED_ACTION_STATUS:
        fail(FAIL_CLASSIFICATION_MISMATCH, "classified_action_status")
    if entry.get("allowed_scope") != ALLOWED_SCOPE:
        fail(FAIL_CLASSIFICATION_MISMATCH, "allowed_scope")
    if entry.get("halt_code") != HALT_CODE:
        fail(FAIL_CLASSIFICATION_MISMATCH, "halt_code")

    classification = {
        "route_disposition": entry["route_disposition"],
        "classified_action_status": entry["classified_action_status"],
        "allowed_machine_action_scope": ALLOWED_MACHINE_ACTION_SCOPE,
        "allowed_scope": entry["allowed_scope"],
        "halt_code": entry["halt_code"],
        "escalation_code": ESCALATION_CODE,
    }
    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "route_classification_id": ROUTE_CLASSIFICATION_ID,
        "router_role": ROUTER_ROLE,
        "router_mode": ROUTER_MODE,
        "generated_by": GENERATOR,
        "source": {
            "requested_action_record_commit_sha": B1_COMMIT,
            "requested_action_record_path": REQUEST,
            "requested_action_record_sha256": sha256_file(root / REQUEST),
            "authority_transition_closure_commit_sha": A4_COMMIT,
            "authority_transition_closure_path": CLOSURE,
            "authority_transition_closure_sha256": sha256_file(root / CLOSURE),
            "authority_update_commit_sha": A3_COMMIT,
            "authority_update_path": UPDATE,
            "authority_update_sha256": sha256_file(root / UPDATE),
        },
        "source_authority": {
            "authority_state_update_id": "c8.n22.authority_state_update.v0",
            "authority_transition_closure_id": "c8.n22.authority_transition_closure.v0",
            "source_object_id": "c8.n22",
            "current_authority_state": CURRENT_AUTHORITY_STATE,
            "basis_scope": BASIS_SCOPE,
            "next_allowed_router_action": NEXT_ALLOWED_ROUTER_ACTION,
            "machine_permitted_action_scope": MACHINE_PERMITTED_ACTION_SCOPE,
        },
        "requested_action": {
            "requested_action_record_id": REQUESTED_ACTION_RECORD_ID,
            "requested_action": movement["requested_action"],
            "requested_action_scope": movement["requested_action_scope"],
            "requested_output_kind": movement["requested_output_kind"],
            "requested_target_basis": movement["requested_target_basis"],
            "request_status": request["request_status"],
        },
        "local_routing_table": LOCAL_ROUTING_TABLE,
        "routing_table_match": {
            "routing_table_id": ROUTING_TABLE_ID,
            "routing_table_scope": ROUTING_TABLE_SCOPE,
            "routing_table_role": ROUTING_TABLE_ROLE,
            "routing_table_authority": ROUTING_TABLE_AUTHORITY,
            "routing_table_entry_id": ROUTING_TABLE_ENTRY_ID,
            "entry_found": True,
            "entry_match_status": "MATCH",
        },
        "classification": classification,
        "classified_admissible_response": {
            "machine_action_classified_as_admissible": REQUESTED_ACTION,
            "admissible_scope": ALLOWED_SCOPE,
            "admissible_only_as_separate_object": True,
            "action_may_be_performed_by_this_record": False,
            "requested_output_created_by_this_record": False,
            "requires_separate_preparation_object": True,
        },
        "still_forbidden": STILL_FORBIDDEN,
        "derived_non_effect_checks": DERIVED_NON_EFFECT_CHECKS,
        "router_gate": {
            "router_gate_status": ROUTER_GATE_STATUS,
            "source_authority_state_present": True,
            "requested_action_record_present": True,
            "requested_action_typed": True,
            "current_authority_state": CURRENT_AUTHORITY_STATE,
            "requested_action": REQUESTED_ACTION,
            "requested_action_scope": REQUESTED_ACTION_SCOPE,
            "routing_table_present": True,
            "routing_table_scope": ROUTING_TABLE_SCOPE,
            "routing_table_authority": ROUTING_TABLE_AUTHORITY,
            "routing_table_entry_found": True,
            "routing_table_entry_match_status": "MATCH",
            "route_disposition": ROUTE_DISPOSITION,
            "classified_action_status": CLASSIFIED_ACTION_STATUS,
            "allowed_machine_action_scope": ALLOWED_MACHINE_ACTION_SCOPE,
            "allowed_scope": ALLOWED_SCOPE,
            "halt_code": HALT_CODE,
            "escalation_code": ESCALATION_CODE,
            "classification_only": True,
            "route_classification_emitted": True,
            "router_classification_record_created": True,
            "action_executed": False,
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
            "runtime_executed": False,
            "observed_path_updated": False,
            "observed_path_update_proposed": False,
            "b3_created": False,
            "failures": [],
        },
        "non_claims": [
            "B.2 does not perform the requested action.",
            "B.2 does not prepare the next bounded unit definition surface.",
            "B.2 does not create the requested output.",
            "B.2 does not define the next bounded unit.",
            "B.2 does not authorize the next bounded unit.",
            "B.2 does not execute runtime.",
            "B.2 does not apply an authority transition.",
            "B.2 does not consume human acceptance.",
            "B.2 does not rewrite receipts.",
            "B.2 does not promote taxonomy.",
            "B.2 does not authorize reuse.",
            "B.2 does not generalize updater.",
            "B.2 does not create runner authority.",
            "B.2 does not create a reusable router.",
            "B.2 does not create a reusable validator archive.",
            "B.2 only classifies the requested action against the formal authority state.",
        ],
        "unsafe_to_infer": [
            "Unsafe to infer: this record performed the requested preparation.",
            "Unsafe to infer: the requested output has been created.",
            "Unsafe to infer: the next bounded unit has been defined.",
            "Unsafe to infer: the next bounded unit has been authorized.",
            "Unsafe to infer: runtime execution is authorized.",
            "Unsafe to infer: authority state changed.",
            "Unsafe to infer: the local routing table is reusable authority.",
            "Unsafe to infer: a validator archive was created.",
        ],
    }
    validate_record(record)
    return record


def validate_record(record: dict[str, Any]) -> None:
    gate = record["router_gate"]
    if "allowed_response" in record:
        fail(FAIL_CLASSIFICATION_MISMATCH, "allowed_response")
    if record["classification"]["route_disposition"] in AMBIGUOUS_DISPOSITIONS:
        fail(FAIL_ROUTE_DISPOSITION_AMBIGUOUS)
    if record["local_routing_table"]["routing_table_authority"] != ROUTING_TABLE_AUTHORITY:
        fail(FAIL_LOCAL_TABLE_PROMOTED)
    if gate["classification_only"] is not True:
        fail(FAIL_CLASSIFICATION_MISMATCH, "classification_only")
    if gate["route_classification_emitted"] is not True:
        fail(FAIL_CLASSIFICATION_MISMATCH, "route_classification_emitted")
    if gate["router_classification_record_created"] is not True:
        fail(FAIL_CLASSIFICATION_MISMATCH, "router_classification_record_created")
    if gate["action_executed"] is not False:
        fail(FAIL_ACTION_EXECUTED)
    if gate["requested_output_created"] is not False:
        fail(FAIL_REQUESTED_OUTPUT_CREATED)
    if gate["authority_changed"] is not False:
        fail(FAIL_AUTHORITY_CHANGED)
    if gate["receipt_rewritten"] is not False:
        fail(FAIL_RECEIPT_REWRITTEN)
    if gate["schema_promoted"] is not False:
        fail(FAIL_SCHEMA_PROMOTED)
    if gate["reuse_authorized"] is not False:
        fail(FAIL_REUSE_AUTHORIZED)
    if gate["updater_generalized"] is not False:
        fail(FAIL_UPDATER_GENERALIZED)
    if gate["runner_authority_created"] is not False:
        fail(FAIL_RUNNER_AUTHORITY_CREATED)
    if gate["reusable_router_created"] is not False:
        fail(FAIL_REUSABLE_ROUTER_CREATED)
    if gate["router_authority_created"] is not False:
        fail(FAIL_REUSABLE_ROUTER_CREATED)
    if gate["validator_archive_created"] is not False:
        fail(FAIL_LOCAL_TABLE_PROMOTED)
    if gate["failures"] != []:
        fail(FAIL_CLASSIFICATION_MISMATCH, str(gate["failures"]))
    for key, value in record["derived_non_effect_checks"].items():
        if value is not False:
            fail(FAIL_ACTION_EXECUTED, key)
    hits = scan_text_for_recommendations(json.dumps(record, sort_keys=True))
    if hits:
        fail(FAIL_RECOMMENDATION_INSERTED, str(hits))


def validate_no_forbidden_files(root: Path) -> None:
    forbidden = [
        "docs/matrixlabs/router/c8_n22_router_specimen_closure_v0.json",
        "docs/matrixlabs/router/c8_n22_router_specimen_closure_v0.md",
        "scripts/build_c8_n22_router_specimen_closure_v0.py",
        "docs/matrixlabs/router/c8_n22_router_closure_v0.json",
        "scripts/build_c8_n22_router_closure_v0.py",
        "docs/matrixlabs/router/matrixlabs_authority_router_table_v0.json",
        "docs/matrixlabs/router/matrixlabs_authority_router_table_v0.md",
        "docs/matrixlabs/validators/matrixlabs_authority_router_table_v0.json",
        "docs/matrixlabs/next_units/c8_n22_next_bounded_unit_v0.json",
        "docs/matrixlabs/next_units/c8_n22_next_bounded_unit_v0.md",
        "docs/matrixlabs/observability/c8_observed_decision_path_update_b2_proposal_v0.json",
        "docs/matrixlabs/observability/c8_observed_path_update_b2_apply_v0.json",
    ]
    existing = [path for path in forbidden if (root / path).exists()]
    if existing:
        fail(FAIL_ACTION_EXECUTED, ",".join(existing))


def render_markdown(record: dict[str, Any]) -> str:
    source = record["source_authority"]
    request = record["requested_action"]
    classification = record["classification"]
    gate = record["router_gate"]
    lines = [
        "# C8 n22 authority route classification v0",
        "",
        "## Status",
        "",
        gate["router_gate_status"],
        "",
        "## Router mode",
        "",
        record["router_mode"],
        "",
        "## Source authority state",
        "",
        source["current_authority_state"],
        "",
        "## Requested action",
        "",
        request["requested_action"],
        "",
        "## Requested scope",
        "",
        request["requested_action_scope"],
        "",
        "## Route disposition",
        "",
        classification["route_disposition"],
        "",
        "## Classified response",
        "",
        "A separate object is classified as admissible to prepare the next bounded unit definition surface using c8.n22 as basis.",
        "",
        "This router did not perform that preparation.",
        "",
        "## Not performed by this router",
        "",
        "- requested action not executed",
        "- requested output not created",
        "- authority not changed",
        "- receipts not rewritten",
        "- schema not promoted",
        "- reuse not authorized",
        "- updater not generalized",
        "- runner authority not created",
        "- reusable router not created",
        "",
        "## Still forbidden",
        "",
        "- next-unit definition finalization",
        "- execution",
        "- receipt rewrite",
        "- taxonomy promotion",
        "- reuse",
        "- updater generalization",
        "- runner authority",
        "- reusable router authority",
        "",
        "## Table status",
        "",
        "The routing table is local to this C8 n22 specimen and is not a reusable validator archive.",
        "",
        "## Non-claims",
    ]
    lines.extend([f"- {claim}" for claim in record["non_claims"]])
    return "\n".join(lines).rstrip() + "\n"


def validate_markdown(record: dict[str, Any], markdown: str) -> None:
    required = [
        "# C8 n22 authority route classification v0",
        "ROUTER_PASS_CLASSIFICATION_ONLY",
        "CLASSIFY_ONLY_NO_ACTION",
        "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
        "PREPARE_SURFACE_ONLY",
        "ROUTE_MACHINE_MAY_PREPARE_ONLY",
        "A separate object is classified as admissible to prepare the next bounded unit definition surface using c8.n22 as basis.",
        "This router did not perform that preparation.",
        "The routing table is local to this C8 n22 specimen and is not a reusable validator archive.",
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
    source = record["source_authority"]
    request = record["requested_action"]
    match = record["routing_table_match"]
    classification = record["classification"]
    gate = record["router_gate"]
    print("BUILD_C8_N22_AUTHORITY_ROUTE_CLASSIFICATION_V0_COMPLETE")
    print(f"route_classification_id={record['route_classification_id']}")
    print(f"schema_version={record['schema_version']}")
    print(f"router_role={record['router_role']}")
    print(f"router_mode={record['router_mode']}")
    print(f"authority_state_update_id={source['authority_state_update_id']}")
    print(f"authority_transition_closure_id={source['authority_transition_closure_id']}")
    print(f"requested_action_record_id={request['requested_action_record_id']}")
    print(f"current_authority_state={source['current_authority_state']}")
    print(f"basis_scope={source['basis_scope']}")
    print(f"next_allowed_router_action={source['next_allowed_router_action']}")
    print(f"machine_permitted_action_scope={source['machine_permitted_action_scope']}")
    print(f"requested_action={request['requested_action']}")
    print(f"requested_action_scope={request['requested_action_scope']}")
    print(f"requested_output_kind={request['requested_output_kind']}")
    print(f"requested_target_basis={request['requested_target_basis']}")
    print(f"routing_table_id={match['routing_table_id']}")
    print(f"routing_table_scope={match['routing_table_scope']}")
    print(f"routing_table_authority={match['routing_table_authority']}")
    print(f"routing_table_entry_id={match['routing_table_entry_id']}")
    print(f"routing_table_entry_found={str(match['entry_found']).lower()}")
    print(f"routing_table_entry_match_status={match['entry_match_status']}")
    print(f"route_disposition={classification['route_disposition']}")
    print(f"classified_action_status={classification['classified_action_status']}")
    print(f"allowed_machine_action_scope={classification['allowed_machine_action_scope']}")
    print(f"allowed_scope={classification['allowed_scope']}")
    print(f"halt_code={classification['halt_code']}")
    print(f"escalation_code={classification['escalation_code']}")
    print(f"router_gate_status={gate['router_gate_status']}")
    print(f"classification_only={str(gate['classification_only']).lower()}")
    print(f"route_classification_emitted={str(gate['route_classification_emitted']).lower()}")
    print(f"router_classification_record_created={str(gate['router_classification_record_created']).lower()}")
    print(f"action_executed={str(gate['action_executed']).lower()}")
    print(f"requested_output_created={str(gate['requested_output_created']).lower()}")
    print(f"next_unit_defined={str(gate['next_unit_defined']).lower()}")
    print(f"next_unit_authorized={str(gate['next_unit_authorized']).lower()}")
    print(f"authority_changed={str(gate['authority_changed']).lower()}")
    print(f"receipt_rewritten={str(gate['receipt_rewritten']).lower()}")
    print(f"schema_promoted={str(gate['schema_promoted']).lower()}")
    print(f"reuse_authorized={str(gate['reuse_authorized']).lower()}")
    print(f"updater_generalized={str(gate['updater_generalized']).lower()}")
    print(f"runner_authority_created={str(gate['runner_authority_created']).lower()}")
    print(f"router_authority_created={str(gate['router_authority_created']).lower()}")
    print(f"reusable_router_created={str(gate['reusable_router_created']).lower()}")
    print(f"validator_archive_created={str(gate['validator_archive_created']).lower()}")
    print(f"runtime_executed={str(gate['runtime_executed']).lower()}")
    print(f"observed_path_updated={str(gate['observed_path_updated']).lower()}")
    print(f"observed_path_update_proposed={str(gate['observed_path_update_proposed']).lower()}")
    print(f"b3_created={str(gate['b3_created']).lower()}")
    print("commit_created=false")
    print("push_executed=false")
    print("terminal_transition=ADVANCE(B3_ROUTER_SPECIMEN_CLOSURE_PENDING)")


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
