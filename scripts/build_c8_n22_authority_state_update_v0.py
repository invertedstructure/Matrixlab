#!/usr/bin/env python3
"""Build the C8 n22 authority state update v0.

This applies the committed A2 human decision receipt exactly once. It formally
consumes HUMAN_ACCEPTANCE here, changes the c8.n22 authority state, and keeps
all next-unit finalization, execution, reuse, taxonomy, updater, and runner
authority blocked.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_authority_state_update_v0.py"
OUTPUT_JSON = "docs/matrixlabs/boundary/c8_n22_authority_state_update_v0.json"
OUTPUT_MD = "docs/matrixlabs/boundary/c8_n22_authority_state_update_v0.md"

BOUNDARY = "docs/matrixlabs/boundary/c8_n22_authority_boundary_transition_record_v0.json"
SURFACE = "docs/matrixlabs/decision_surfaces/c8_n22_human_decision_surface_v0.json"
RECEIPT = "docs/matrixlabs/decisions/c8_n22_human_decision_receipt_v0.json"
READABOUT = "docs/matrixlabs/readabouts/c8_n22_authority_boundary_readabout_v0.json"

A1_COMMIT = "c006f0fd1a9833009c5660900534a692402fbe6e"
A2_COMMIT = "3bd78924073756c8a3640082897d6ade5780970d"

SCHEMA_VERSION = "matrixlabs_authority_state_update_v0"
AUTHORITY_UPDATE_ID = "c8.n22.authority_state_update.v0"
UPDATE_ROLE = "FORMAL_AUTHORITY_STATE_TRANSITION_APPLICATION"
SOURCE_BOUNDARY_RECORD_ID = "c8.n22.boundary_transition.v0"
SOURCE_DECISION_SURFACE_ID = "c8.n22.human_decision_surface.v0"
SOURCE_DECISION_RECEIPT_ID = "c8.n22.human_decision_receipt.v0"
SOURCE_READABOUT_ID = "c8.n22.authority_boundary.readabout.v0"
SOURCE_READABOUT_ROLE = "AUDIT_REFERENCE_ONLY_DOWNSTREAM_PROJECTION"
SELECTED_OPTION = "DECISION_ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION"
PASS_GATE = "AUTHORITY_UPDATE_PASS_DECISION_APPLIED"

FAIL_BOUNDARY_RECORD_MISSING = "AUTHORITY_UPDATE_FAIL_BOUNDARY_RECORD_MISSING"
FAIL_DECISION_SURFACE_MISSING = "AUTHORITY_UPDATE_FAIL_DECISION_SURFACE_MISSING"
FAIL_DECISION_RECEIPT_MISSING = "AUTHORITY_UPDATE_FAIL_DECISION_RECEIPT_MISSING"
FAIL_READABOUT_MISSING = "AUTHORITY_UPDATE_FAIL_READABOUT_MISSING"
FAIL_DECISION_RECEIPT_INVALID = "AUTHORITY_UPDATE_FAIL_DECISION_RECEIPT_INVALID"
FAIL_OPTION_NOT_ON_SURFACE = "AUTHORITY_UPDATE_FAIL_OPTION_NOT_ON_SURFACE"
FAIL_OPTION_EFFECT_MISMATCH = "AUTHORITY_UPDATE_FAIL_OPTION_EFFECT_MISMATCH"
FAIL_TRANSITION_TABLE_MISSING = "AUTHORITY_UPDATE_FAIL_TRANSITION_TABLE_MISSING"
FAIL_PRIOR_STATE_MISMATCH = "AUTHORITY_UPDATE_FAIL_PRIOR_STATE_MISMATCH"
FAIL_AUTHORITY_EVENT_MISMATCH = "AUTHORITY_UPDATE_FAIL_AUTHORITY_EVENT_MISMATCH"
FAIL_DECISION_RECEIPT_ALREADY_APPLIED = "AUTHORITY_UPDATE_FAIL_DECISION_RECEIPT_ALREADY_APPLIED"
FAIL_NEXT_UNIT_DEFINITION_AUTHORITY_SMUGGLED = (
    "AUTHORITY_UPDATE_FAIL_NEXT_UNIT_DEFINITION_AUTHORITY_SMUGGLED"
)
FAIL_EXECUTION_AUTHORITY_SMUGGLED = "AUTHORITY_UPDATE_FAIL_EXECUTION_AUTHORITY_SMUGGLED"
FAIL_REUSE_AUTHORITY_SMUGGLED = "AUTHORITY_UPDATE_FAIL_REUSE_AUTHORITY_SMUGGLED"
FAIL_PROMOTION_AUTHORITY_SMUGGLED = "AUTHORITY_UPDATE_FAIL_PROMOTION_AUTHORITY_SMUGGLED"
FAIL_UPDATER_GENERALIZATION_SMUGGLED = (
    "AUTHORITY_UPDATE_FAIL_UPDATER_GENERALIZATION_SMUGGLED"
)
FAIL_RUNNER_AUTHORITY_SMUGGLED = "AUTHORITY_UPDATE_FAIL_RUNNER_AUTHORITY_SMUGGLED"
FAIL_NEXT_ROUTER_ACTION_UNDECLARED = "AUTHORITY_UPDATE_FAIL_NEXT_ROUTER_ACTION_UNDECLARED"
FAIL_NONSELECTED_BRANCH_INCLUDED = "AUTHORITY_UPDATE_FAIL_NONSELECTED_BRANCH_INCLUDED"
FAIL_RECOMMENDATION_INSERTED = "AUTHORITY_UPDATE_FAIL_RECOMMENDATION_INSERTED"
FAIL_MARKDOWN_JSON_PARITY = "AUTHORITY_UPDATE_FAIL_MARKDOWN_JSON_PARITY"

AUTHORITY_EFFECT_KEYS = [
    "basis_for_next_unit_definition_authority",
    "next_unit_definition_surface_preparation_authority",
    "next_unit_definition_authority",
    "execution_authority",
    "reuse_authority",
    "taxonomy_promotion_authority",
    "updater_generalization_authority",
    "runner_authority",
]

AUTHORITY_EFFECTS_AFTER_UPDATE = {
    "basis_for_next_unit_definition_authority": "GRANTED",
    "next_unit_definition_surface_preparation_authority": "GRANTED",
    "next_unit_definition_authority": "NOT_GRANTED",
    "execution_authority": "NOT_GRANTED",
    "reuse_authority": "NOT_GRANTED",
    "taxonomy_promotion_authority": "NOT_GRANTED",
    "updater_generalization_authority": "NOT_GRANTED",
    "runner_authority": "NOT_GRANTED",
}

FORBIDDEN_ROUTER_SCOPES = [
    "FINALIZE_NEXT_UNIT_DEFINITION_WITHOUT_SEPARATE_AUTHORITY",
    "EXECUTE_UNIT",
    "REWRITE_RECEIPTS",
    "PROMOTE_TAXONOMY",
    "AUTHORIZE_REUSE",
    "GENERALIZE_UPDATER",
    "ACTIVATE_RUNNER",
]

RECOMMENDATION_PHRASES = [
    "should accept",
    "should proceed",
    "recommended",
    "best next move",
    "correct next move",
    "good choice",
    "now proceed",
    "now execute",
    "you should",
    "we should execute",
    "execution is safe",
    "safe to execute",
    "authorized to execute",
    "unit is defined",
    "next unit authorized",
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
        fail(FAIL_BOUNDARY_RECORD_MISSING, proc.stderr.strip())
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
    run_git(root, ["cat-file", "-e", f"{A1_COMMIT}^{{commit}}"], FAIL_DECISION_SURFACE_MISSING)
    run_git(root, ["cat-file", "-e", f"{A2_COMMIT}^{{commit}}"], FAIL_DECISION_RECEIPT_MISSING)
    a1_got = commit_for_paths(
        root,
        [
            SURFACE,
            "docs/matrixlabs/decision_surfaces/c8_n22_human_decision_surface_v0.md",
            "scripts/build_c8_n22_human_decision_surface_v0.py",
        ],
        FAIL_DECISION_SURFACE_MISSING,
    )
    if a1_got != A1_COMMIT:
        fail(FAIL_DECISION_SURFACE_MISSING, f"A1 commit mismatch: {a1_got}!={A1_COMMIT}")
    a2_got = commit_for_paths(
        root,
        [
            RECEIPT,
            "docs/matrixlabs/decisions/c8_n22_human_decision_receipt_v0.md",
            "scripts/build_c8_n22_human_decision_receipt_v0.py",
        ],
        FAIL_DECISION_RECEIPT_MISSING,
    )
    if a2_got != A2_COMMIT:
        fail(FAIL_DECISION_RECEIPT_MISSING, f"A2 commit mismatch: {a2_got}!={A2_COMMIT}")


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
        fail(missing_code, f"{rel}: invalid JSON")
        raise exc


def scan_text_for_recommendations(text: str) -> list[str]:
    lowered = text.lower()
    return [phrase for phrase in RECOMMENDATION_PHRASES if phrase in lowered]


def selected_option_from_surface(surface: dict[str, Any]) -> dict[str, Any]:
    for option in surface.get("decision_options", []):
        if option.get("decision_option_id") == SELECTED_OPTION:
            return option
    fail(FAIL_OPTION_NOT_ON_SURFACE, SELECTED_OPTION)
    raise AssertionError("unreachable")


def validate_boundary(boundary: dict[str, Any]) -> None:
    checks = {
        "schema_version": (
            boundary.get("schema_version"),
            "matrixlabs_authority_boundary_transition_record_v0",
        ),
        "boundary_record_id": (boundary.get("boundary_record_id"), SOURCE_BOUNDARY_RECORD_ID),
        "current_authority_state": (
            boundary.get("current_authority", {}).get("current_authority_state"),
            "AUTH_STATE_OBSERVED_NOT_AUTHORIZED",
        ),
        "required_event": (
            boundary.get("required_authority_event", {}).get("required_event"),
            "HUMAN_ACCEPTANCE",
        ),
        "required_event_status": (
            boundary.get("required_authority_event", {}).get("required_event_status"),
            "AUTH_EVENT_UNCONSUMED",
        ),
    }
    failures = [f"{key}:{got}!={want}" for key, (got, want) in checks.items() if got != want]
    if failures:
        fail(FAIL_BOUNDARY_RECORD_MISSING, "; ".join(failures))


def validate_surface(surface: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "schema_version": (
            surface.get("schema_version"),
            "matrixlabs_human_decision_surface_v0",
        ),
        "decision_surface_id": (surface.get("decision_surface_id"), SOURCE_DECISION_SURFACE_ID),
        "source_boundary_record_id": (
            surface.get("source_boundary_record_id"),
            SOURCE_BOUNDARY_RECORD_ID,
        ),
        "source_readabout_id": (surface.get("source_readabout_id"), SOURCE_READABOUT_ID),
        "decision_surface_gate": (
            surface.get("surface_gate", {}).get("decision_surface_gate"),
            "DECISION_SURFACE_PASS_OPTIONS_PRESENTED_ONLY",
        ),
        "decision_consumed": (surface.get("decision_consumed"), False),
        "authority_changed": (surface.get("authority_changed"), False),
    }
    failures = [f"{key}:{got}!={want}" for key, (got, want) in checks.items() if got != want]
    if failures:
        fail(FAIL_DECISION_SURFACE_MISSING, "; ".join(failures))
    return selected_option_from_surface(surface)


def validate_receipt(receipt: dict[str, Any], selected_option: dict[str, Any]) -> dict[str, str]:
    checks = {
        "schema_version": (receipt.get("schema_version"), "matrixlabs_human_decision_receipt_v0"),
        "decision_receipt_id": (receipt.get("decision_receipt_id"), SOURCE_DECISION_RECEIPT_ID),
        "receipt_role": (receipt.get("receipt_role"), "HUMAN_DECISION_EVENT_RECEIPT"),
        "source_decision_surface_id": (
            receipt.get("source_decision_surface_id"),
            SOURCE_DECISION_SURFACE_ID,
        ),
        "source_boundary_record_id": (
            receipt.get("source_boundary_record_id"),
            SOURCE_BOUNDARY_RECORD_ID,
        ),
        "source_readabout_id": (receipt.get("source_readabout_id"), SOURCE_READABOUT_ID),
        "receipt_gate": (
            receipt.get("receipt_gate", {}).get("decision_receipt_gate"),
            "HUMAN_DECISION_RECEIPT_PASS_TYPED_DECISION_RECORDED",
        ),
        "selected_decision_option": (
            receipt.get("decision_event", {}).get("selected_decision_option"),
            SELECTED_OPTION,
        ),
        "selection_source": (
            receipt.get("decision_event", {}).get("selection_source"),
            "EXPLICIT_HUMAN_SELECTION",
        ),
        "authority_event_pending": (
            receipt.get("receipt_gate", {}).get("authority_event_recorded_pending_a3_application"),
            "HUMAN_ACCEPTANCE",
        ),
        "authority_state_applied_by_receipt": (
            receipt.get("application_boundary", {}).get("authority_state_applied_by_this_receipt"),
            False,
        ),
        "authority_event_consumed_by_receipt": (
            receipt.get("application_boundary", {}).get(
                "authority_event_formally_consumed_by_this_receipt"
            ),
            False,
        ),
    }
    failures = [f"{key}:{got}!={want}" for key, (got, want) in checks.items() if got != want]
    if failures:
        fail(FAIL_DECISION_RECEIPT_INVALID, "; ".join(failures))
    if receipt.get("application_boundary", {}).get("authority_state_applied_by_this_receipt") is not False:
        fail(FAIL_DECISION_RECEIPT_ALREADY_APPLIED)
    if receipt.get("application_boundary", {}).get("authority_event_formally_consumed_by_this_receipt") is not False:
        fail(FAIL_DECISION_RECEIPT_ALREADY_APPLIED)

    selected_effects = receipt.get("selected_option_effects_from_surface", {})
    receipt_effects = selected_effects.get("authority_effects_if_applied_by_a3", {})
    if receipt_effects != selected_option.get("authority_effects"):
        fail(FAIL_OPTION_EFFECT_MISMATCH)
    if receipt_effects != AUTHORITY_EFFECTS_AFTER_UPDATE:
        fail(FAIL_OPTION_EFFECT_MISMATCH)
    if selected_effects.get("consumes_authority_event") != "HUMAN_ACCEPTANCE":
        fail(FAIL_AUTHORITY_EVENT_MISMATCH)
    if selected_effects.get("authority_event_status_if_applied_by_a3") != "AUTH_EVENT_CONSUMED":
        fail(FAIL_AUTHORITY_EVENT_MISMATCH)
    if selected_effects.get("resulting_authority_state_if_applied_by_a3") != (
        "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION"
    ):
        fail(FAIL_PRIOR_STATE_MISMATCH)
    return receipt_effects


def validate_readabout(readabout: dict[str, Any]) -> None:
    if readabout.get("readabout_packet_id") != SOURCE_READABOUT_ID:
        fail(FAIL_READABOUT_MISSING, str(readabout.get("readabout_packet_id")))
    source = readabout.get("source", {})
    if source.get("source_object_id") != SOURCE_BOUNDARY_RECORD_ID:
        fail(FAIL_READABOUT_MISSING, str(source.get("source_object_id")))


def local_transition_table() -> dict[str, Any]:
    return {
        "transition_table_id": "c8.n22.applied_decision_transition_table.v0",
        "transition_table_scope": "LOCAL_A3_SELECTED_RECEIPT_ONLY",
        "entries": [
            {
                "selected_decision_option": SELECTED_OPTION,
                "required_prior_state": "AUTH_STATE_OBSERVED_NOT_AUTHORIZED",
                "required_authority_event_from_receipt": "HUMAN_ACCEPTANCE",
                "required_receipt_application_status_before": "NOT_APPLIED",
                "new_authority_state": "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
                "authority_event_status_after": "AUTH_EVENT_CONSUMED",
                "next_allowed_router_action": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
                "authority_effects_after_update": dict(AUTHORITY_EFFECTS_AFTER_UPDATE),
            }
        ],
    }


def validate_transition_table(table: dict[str, Any], receipt_effects: dict[str, str]) -> dict[str, Any]:
    if table.get("transition_table_scope") != "LOCAL_A3_SELECTED_RECEIPT_ONLY":
        fail(FAIL_TRANSITION_TABLE_MISSING)
    entries = table.get("entries")
    if not isinstance(entries, list) or len(entries) != 1:
        fail(FAIL_NONSELECTED_BRANCH_INCLUDED)
    entry = entries[0]
    if entry.get("selected_decision_option") != SELECTED_OPTION:
        fail(FAIL_NONSELECTED_BRANCH_INCLUDED)
    if entry.get("required_prior_state") != "AUTH_STATE_OBSERVED_NOT_AUTHORIZED":
        fail(FAIL_PRIOR_STATE_MISMATCH)
    if entry.get("required_authority_event_from_receipt") != "HUMAN_ACCEPTANCE":
        fail(FAIL_AUTHORITY_EVENT_MISMATCH)
    if entry.get("authority_effects_after_update") != receipt_effects:
        fail(FAIL_OPTION_EFFECT_MISMATCH)
    if entry.get("next_allowed_router_action") != "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE":
        fail(FAIL_NEXT_ROUTER_ACTION_UNDECLARED)
    return entry


def validate_authority_effects(effects: dict[str, str]) -> None:
    if set(effects) != set(AUTHORITY_EFFECT_KEYS):
        fail(FAIL_OPTION_EFFECT_MISMATCH, f"effect keys: {sorted(effects)}")
    if effects.get("basis_for_next_unit_definition_authority") != "GRANTED":
        fail(FAIL_OPTION_EFFECT_MISMATCH)
    if effects.get("next_unit_definition_surface_preparation_authority") != "GRANTED":
        fail(FAIL_OPTION_EFFECT_MISMATCH)
    if effects.get("next_unit_definition_authority") != "NOT_GRANTED":
        fail(FAIL_NEXT_UNIT_DEFINITION_AUTHORITY_SMUGGLED)
    if effects.get("execution_authority") != "NOT_GRANTED":
        fail(FAIL_EXECUTION_AUTHORITY_SMUGGLED)
    if effects.get("reuse_authority") != "NOT_GRANTED":
        fail(FAIL_REUSE_AUTHORITY_SMUGGLED)
    if effects.get("taxonomy_promotion_authority") != "NOT_GRANTED":
        fail(FAIL_PROMOTION_AUTHORITY_SMUGGLED)
    if effects.get("updater_generalization_authority") != "NOT_GRANTED":
        fail(FAIL_UPDATER_GENERALIZATION_SMUGGLED)
    if effects.get("runner_authority") != "NOT_GRANTED":
        fail(FAIL_RUNNER_AUTHORITY_SMUGGLED)


def check_existing_application(root: Path) -> None:
    output = root / OUTPUT_JSON
    if not output.exists():
        return
    try:
        existing = json.loads(output.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(FAIL_DECISION_RECEIPT_ALREADY_APPLIED, str(exc))
    application = existing.get("application_record", {})
    if (
        existing.get("authority_update_id") != AUTHORITY_UPDATE_ID
        or application.get("applies_decision_receipt_id") != SOURCE_DECISION_RECEIPT_ID
    ):
        fail(FAIL_DECISION_RECEIPT_ALREADY_APPLIED)


def build_update(root: Path) -> dict[str, Any]:
    verify_expected_commits(root)
    check_existing_application(root)
    boundary = load_json(root, BOUNDARY, FAIL_BOUNDARY_RECORD_MISSING)
    surface = load_json(root, SURFACE, FAIL_DECISION_SURFACE_MISSING)
    receipt = load_json(root, RECEIPT, FAIL_DECISION_RECEIPT_MISSING)
    readabout = load_json(root, READABOUT, FAIL_READABOUT_MISSING)
    validate_boundary(boundary)
    selected_option = validate_surface(surface)
    receipt_effects = validate_receipt(receipt, selected_option)
    validate_readabout(readabout)
    validate_authority_effects(receipt_effects)
    table = local_transition_table()
    transition_entry = validate_transition_table(table, receipt_effects)

    authority_state_before = {
        "current_authority_state": "AUTH_STATE_OBSERVED_NOT_AUTHORIZED",
        "required_authority_event": "HUMAN_ACCEPTANCE",
        "authority_event_status_before": "AUTH_EVENT_UNCONSUMED",
    }
    applied_decision = {
        "selected_decision_option": SELECTED_OPTION,
        "decision_actor_class": "HUMAN",
        "selection_source": "EXPLICIT_HUMAN_SELECTION",
        "decision_receipt_status": "HUMAN_DECISION_RECEIPT_PASS_TYPED_DECISION_RECORDED",
        "decision_receipt_application_status_before": "NOT_APPLIED",
    }
    authority_state_after = {
        "new_authority_state": "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        "authority_event_applied": "HUMAN_ACCEPTANCE",
        "authority_event_status_after": "AUTH_EVENT_CONSUMED",
    }
    next_router_state = {
        "next_allowed_router_action": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
        "machine_permitted_action_scope": "PREPARE_NEXT_UNIT_DEFINITION_SURFACE_ONLY",
        "machine_forbidden_action_scopes": list(FORBIDDEN_ROUTER_SCOPES),
    }
    application_record = {
        "application_id": AUTHORITY_UPDATE_ID,
        "applies_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "decision_receipt_application_status": "APPLIED_ONCE",
    }
    update = {
        "schema_version": SCHEMA_VERSION,
        "authority_update_id": AUTHORITY_UPDATE_ID,
        "update_role": UPDATE_ROLE,
        "generated_by": GENERATOR,
        "source_boundary_record_id": SOURCE_BOUNDARY_RECORD_ID,
        "source_decision_surface_id": SOURCE_DECISION_SURFACE_ID,
        "source_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "source_readabout_id": SOURCE_READABOUT_ID,
        "source_readabout_role": SOURCE_READABOUT_ROLE,
        "source": {
            "boundary_record_path": BOUNDARY,
            "decision_surface_path": SURFACE,
            "decision_surface_commit_sha": A1_COMMIT,
            "decision_receipt_path": RECEIPT,
            "decision_receipt_commit_sha": A2_COMMIT,
            "readabout_path": READABOUT,
            "readabout_authority_role": SOURCE_READABOUT_ROLE,
            "boundary_record_sha256": sha256_file(root / BOUNDARY),
            "decision_surface_sha256": sha256_file(root / SURFACE),
            "decision_receipt_sha256": sha256_file(root / RECEIPT),
            "readabout_sha256": sha256_file(root / READABOUT),
        },
        "authority_state_before": authority_state_before,
        "applied_decision": applied_decision,
        "authority_state_after": authority_state_after,
        "authority_effects_after_update": dict(AUTHORITY_EFFECTS_AFTER_UPDATE),
        "next_router_state": next_router_state,
        "local_transition_table": table,
        "application_record": application_record,
        "update_gate": {
            "authority_state_update_gate": PASS_GATE,
            "source_boundary_record_present": True,
            "source_decision_surface_present": True,
            "source_decision_receipt_present": True,
            "source_readabout_present": True,
            "prior_authority_state": authority_state_before["current_authority_state"],
            "selected_decision_option": SELECTED_OPTION,
            "selected_option_present_on_surface": True,
            "selected_option_effects_match_surface": True,
            "decision_receipt_valid": True,
            "decision_receipt_not_already_applied_elsewhere": True,
            "transition_table_scope": table["transition_table_scope"],
            "transition_table_entry_found": True,
            "transition_table_entry_count": len(table["entries"]),
            "prior_state_matches_transition_table": True,
            "authority_event_matches_receipt": True,
            "state_transition_matches_selected_option": True,
            "new_authority_state": authority_state_after["new_authority_state"],
            "authority_event_applied": authority_state_after["authority_event_applied"],
            "authority_event_status_after": authority_state_after["authority_event_status_after"],
            "decision_receipt_application_status": application_record[
                "decision_receipt_application_status"
            ],
            "next_allowed_router_action": transition_entry["next_allowed_router_action"],
            "machine_permitted_action_scope": next_router_state["machine_permitted_action_scope"],
            **dict(AUTHORITY_EFFECTS_AFTER_UPDATE),
            "authority_smuggling_detected": False,
            "failures": [],
        },
        "non_claims": [
            "A3 does not execute the next bounded unit.",
            "A3 does not define the next bounded unit as final.",
            "A3 does not authorize final next-unit definition.",
            "A3 does not promote taxonomy.",
            "A3 does not authorize reuse.",
            "A3 does not generalize the updater.",
            "A3 does not create runner authority.",
            "A3 does not rewrite receipts.",
            "A3 does not validate theorem truth.",
            "A3 does not validate edge lawfulness.",
            "A3 does not validate receipt truth beyond verifying the declared A2 receipt fields against A1 and the local transition table.",
            "A3 only applies the selected human decision receipt to the formal c8.n22 authority state.",
            "A3 authorizes preparation of the next bounded unit definition surface only.",
            "A3 does not create, finalize, authorize, or execute that next bounded unit.",
        ],
        "unsafe_to_infer": [
            "Unsafe to infer: the next bounded unit has been defined.",
            "Unsafe to infer: the next bounded unit has been finalized.",
            "Unsafe to infer: the next bounded unit may execute.",
            "Unsafe to infer: runtime execution is authorized.",
            "Unsafe to infer: receipts may be rewritten.",
            "Unsafe to infer: taxonomy has been promoted.",
            "Unsafe to infer: reuse is authorized.",
            "Unsafe to infer: updater generalization is authorized.",
            "Unsafe to infer: runner authority exists.",
        ],
    }
    validate_update(update, receipt_effects)
    return update


def validate_update(update: dict[str, Any], receipt_effects: dict[str, str]) -> None:
    table = update["local_transition_table"]
    validate_transition_table(table, receipt_effects)
    effects = update["authority_effects_after_update"]
    validate_authority_effects(effects)
    gate = update["update_gate"]
    if gate.get("authority_state_update_gate") != PASS_GATE:
        fail(FAIL_TRANSITION_TABLE_MISSING)
    if gate.get("transition_table_entry_count") != 1:
        fail(FAIL_NONSELECTED_BRANCH_INCLUDED)
    if gate.get("authority_event_status_after") != "AUTH_EVENT_CONSUMED":
        fail(FAIL_AUTHORITY_EVENT_MISMATCH)
    if gate.get("decision_receipt_application_status") != "APPLIED_ONCE":
        fail(FAIL_DECISION_RECEIPT_ALREADY_APPLIED)
    if gate.get("next_allowed_router_action") != "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE":
        fail(FAIL_NEXT_ROUTER_ACTION_UNDECLARED)
    if gate.get("authority_smuggling_detected") is not False:
        fail(FAIL_OPTION_EFFECT_MISMATCH)
    if gate.get("failures") != []:
        fail(FAIL_TRANSITION_TABLE_MISSING)
    hits = scan_text_for_recommendations(json.dumps(update, sort_keys=True))
    if hits:
        fail(FAIL_RECOMMENDATION_INSERTED, str(hits))


def render_markdown(update: dict[str, Any]) -> str:
    gate = update["update_gate"]
    before = update["authority_state_before"]
    after = update["authority_state_after"]
    effects = update["authority_effects_after_update"]
    next_router = update["next_router_state"]
    lines = [
        "# C8 n22 authority state update v0",
        "",
        "## Status",
        "",
        gate["authority_state_update_gate"],
        "",
        "## Applied decision",
        "",
        update["applied_decision"]["selected_decision_option"],
        "",
        "## Prior authority state",
        "",
        before["current_authority_state"],
        "",
        "## New authority state",
        "",
        after["new_authority_state"],
        "",
        "## Authority event applied",
        "",
        after["authority_event_applied"],
        "",
        "## Authority event status after",
        "",
        after["authority_event_status_after"],
        "",
        "## Newly authorized",
        "",
        "- basis for next-unit definition authority: "
        f"{effects['basis_for_next_unit_definition_authority']}",
        "- next-unit definition surface preparation authority: "
        f"{effects['next_unit_definition_surface_preparation_authority']}",
        "",
        "## Still not authorized",
        "",
        "- next-unit definition finalization",
        "- execution",
        "- receipt rewrite",
        "- taxonomy promotion",
        "- reuse",
        "- updater generalization",
        "- runner authority",
        "",
        "## Next allowed router action",
        "",
        next_router["next_allowed_router_action"],
        "",
        "## Application boundary",
        "",
        "This authority update applies the committed A2 human decision receipt exactly once.",
        "",
        "It authorizes preparation of the next bounded unit definition surface only.",
        "",
        "It does not define, finalize, authorize, or execute the next bounded unit.",
        "",
        "## Non-claims",
        "",
        "This authority update does not execute runtime, rewrite receipts, promote taxonomy, authorize reuse, generalize the updater, or create runner authority.",
        "",
    ]
    lines.extend(f"- {claim}" for claim in update["non_claims"])
    lines.extend(["", "## Unsafe to infer", ""])
    lines.extend(f"- {item}" for item in update["unsafe_to_infer"])
    return "\n".join(lines) + "\n"


def validate_markdown(update: dict[str, Any], markdown: str) -> None:
    required = [
        "# C8 n22 authority state update v0",
        "AUTHORITY_UPDATE_PASS_DECISION_APPLIED",
        SELECTED_OPTION,
        "AUTH_STATE_OBSERVED_NOT_AUTHORIZED",
        "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        "HUMAN_ACCEPTANCE",
        "AUTH_EVENT_CONSUMED",
        "## Newly authorized",
        "basis for next-unit definition authority: GRANTED",
        "next-unit definition surface preparation authority: GRANTED",
        "## Still not authorized",
        "next-unit definition finalization",
        "execution",
        "receipt rewrite",
        "taxonomy promotion",
        "reuse",
        "updater generalization",
        "runner authority",
        "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
        "This authority update applies the committed A2 human decision receipt exactly once.",
        "It authorizes preparation of the next bounded unit definition surface only.",
        "It does not define, finalize, authorize, or execute the next bounded unit.",
        "This authority update does not execute runtime, rewrite receipts, promote taxonomy, authorize reuse, generalize the updater, or create runner authority.",
    ]
    missing = [phrase for phrase in required if phrase not in markdown]
    if missing:
        fail(FAIL_MARKDOWN_JSON_PARITY, str(missing))
    hits = scan_text_for_recommendations(markdown)
    if hits:
        fail(FAIL_RECOMMENDATION_INSERTED, str(hits))


def write_outputs(root: Path, update: dict[str, Any]) -> None:
    markdown = render_markdown(update)
    validate_markdown(update, markdown)
    json_path = root / OUTPUT_JSON
    md_path = root / OUTPUT_MD
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(update, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")


def print_success(update: dict[str, Any]) -> None:
    gate = update["update_gate"]
    after = update["authority_state_after"]
    effects = update["authority_effects_after_update"]
    next_router = update["next_router_state"]
    print("BUILD_C8_N22_AUTHORITY_STATE_UPDATE_V0_COMPLETE")
    print(f"authority_update_id={update['authority_update_id']}")
    print(f"schema_version={update['schema_version']}")
    print(f"update_role={update['update_role']}")
    print(f"source_boundary_record_id={update['source_boundary_record_id']}")
    print(f"source_decision_surface_id={update['source_decision_surface_id']}")
    print(f"source_decision_receipt_id={update['source_decision_receipt_id']}")
    print(f"source_readabout_id={update['source_readabout_id']}")
    print(f"source_readabout_role={update['source_readabout_role']}")
    print(f"selected_decision_option={gate['selected_decision_option']}")
    print(f"decision_receipt_status={update['applied_decision']['decision_receipt_status']}")
    print(f"authority_state_update_gate={gate['authority_state_update_gate']}")
    print(f"transition_table_scope={gate['transition_table_scope']}")
    print(f"transition_table_entry_count={gate['transition_table_entry_count']}")
    print(
        "selected_option_present_on_surface="
        f"{str(gate['selected_option_present_on_surface']).lower()}"
    )
    print(
        "selected_option_effects_match_surface="
        f"{str(gate['selected_option_effects_match_surface']).lower()}"
    )
    print(f"decision_receipt_valid={str(gate['decision_receipt_valid']).lower()}")
    print(
        "decision_receipt_not_already_applied_elsewhere="
        f"{str(gate['decision_receipt_not_already_applied_elsewhere']).lower()}"
    )
    print(f"prior_authority_state={gate['prior_authority_state']}")
    print(f"authority_event_applied={after['authority_event_applied']}")
    print(f"authority_event_status_after={after['authority_event_status_after']}")
    print(f"new_authority_state={after['new_authority_state']}")
    print(f"decision_receipt_application_status={gate['decision_receipt_application_status']}")
    for key in AUTHORITY_EFFECT_KEYS:
        print(f"{key}={effects[key]}")
    print(f"next_allowed_router_action={next_router['next_allowed_router_action']}")
    print(f"machine_permitted_action_scope={next_router['machine_permitted_action_scope']}")
    print("authority_state_changed=true")
    print("human_acceptance_formally_consumed=true")
    print("decision_receipt_applied=true")
    print("next_unit_defined=false")
    print("next_unit_authorized=false")
    print("runtime_executed=false")
    print("receipts_rewritten=false")
    print("taxonomy_promoted=false")
    print("runner_authority_created=false")
    print("a4_created=false")
    print("commit_created=false")
    print("push_executed=false")
    print("terminal_transition=ADVANCE(A4_AUTHORITY_TRANSITION_CLOSURE_PENDING)")


def main() -> int:
    try:
        root = detect_repo_root(Path.cwd())
        update = build_update(root)
        write_outputs(root, update)
    except GenerationError as exc:
        print(f"STOP_{exc.code}")
        return 2
    print_success(update)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
