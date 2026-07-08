#!/usr/bin/env python3
"""Build C8 n22 candidate promotion decision receipt v0.

This receipt records the explicit human-selected D.1 promotion option. It does
not materialize archive-entry state, apply reuse authority, apply activation,
perform machine proceed, or prepare the next unit definition surface.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_candidate_promotion_decision_receipt_v0.py"
OUTPUT_JSON = "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_receipt_v0.json"
OUTPUT_MD = "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_receipt_v0.md"

PROMOTION_SURFACE = "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_surface_v0.json"
CANDIDATE_ENTRY = "docs/matrixlabs/validator_archive/candidates/c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.json"
CANDIDATE_AUDIT = "docs/matrixlabs/validator_archive/audits/c8_n22_candidate_archive_entry_admissibility_audit_v0.json"

D1_COMMIT = "a457bf08eb263cdbdad01a4eef6b7e7e2b11f230"
C2_COMMIT = "674c601136f381c9d85605f646900998b24ddfe9"
C3_COMMIT = "f49dfab97774414330682151e6e3fffeb7ba6f66"

SCHEMA_VERSION = "matrixlabs_human_promotion_decision_receipt_v0"
RECEIPT_ID = "c8.n22.candidate_promotion_decision_receipt.v0"
RECEIPT_ROLE = "HUMAN_PROMOTION_DECISION_EVENT_RECEIPT"
RECEIPT_STATUS = "PROMOTION_DECISION_RECEIPT_RECORDED"
BLOCK_ID = "BLOCK_D"
BLOCK_UNIT_ID = "D2_HUMAN_PROMOTION_DECISION_RECEIPT"
RECEIPT_GATE = "PROMOTION_DECISION_RECEIPT_PASS_TYPED_DECISION_RECORDED"
PRECOMMIT_GATE = "PASS"
TERMINAL_TRANSITION = "ADVANCE(D3_ARCHIVE_ENTRY_STATE_MATERIALIZATION_PENDING)"

SURFACE_ID = "c8.n22.candidate_promotion_decision_surface.v0"
SURFACE_SCHEMA_VERSION = "matrixlabs_human_promotion_decision_surface_v0"
CANDIDATE_ID = "candidate.c8.n22.prepare_next_unit_definition_surface.v0"
CANDIDATE_AUDIT_ID = "c8.n22.candidate_archive_entry.admissibility_audit.v0"
CANDIDATE_AUDIT_STATUS = "CANDIDATE_AUDIT_PASS_CONTRACT_CONFORMANT_NOT_PROMOTED"

SELECTED_OPTION = "DECISION_PROMOTE_CANDIDATE_FOR_DECLARED_SCOPE"
DECISION_ACTOR_CLASS = "HUMAN"
DECISION_EVENT_STATUS = "DECISION_EVENT_RECORDED"
SELECTION_SOURCE = "EXPLICIT_HUMAN_SELECTION"

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
SELECTED_RADIUS = "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT"
NEXT_REQUIRED_OBJECT = "c8_n22_prepare_next_unit_definition_active_archive_entry_v0"

FAIL_SURFACE_MISSING = "PROMOTION_DECISION_RECEIPT_FAIL_SURFACE_MISSING"
FAIL_CANDIDATE_MISSING = "PROMOTION_DECISION_RECEIPT_FAIL_CANDIDATE_MISSING"
FAIL_CANDIDATE_AUDIT_MISSING = "PROMOTION_DECISION_RECEIPT_FAIL_CANDIDATE_AUDIT_MISSING"
FAIL_CANDIDATE_AUDIT_NOT_PASS = "PROMOTION_DECISION_RECEIPT_FAIL_CANDIDATE_AUDIT_NOT_PASS"
FAIL_SELECTED_OPTION_MISSING = "PROMOTION_DECISION_RECEIPT_FAIL_SELECTED_OPTION_MISSING"
FAIL_OPTION_NOT_ON_SURFACE = "PROMOTION_DECISION_RECEIPT_FAIL_OPTION_NOT_ON_SURFACE"
FAIL_SCOPE_MISMATCH = "PROMOTION_DECISION_RECEIPT_FAIL_SCOPE_MISMATCH"
FAIL_RADIUS_MISMATCH = "PROMOTION_DECISION_RECEIPT_FAIL_RADIUS_MISMATCH"
FAIL_HUMAN_SELECTION_MISSING = "PROMOTION_DECISION_RECEIPT_FAIL_HUMAN_SELECTION_MISSING"
FAIL_SELECTION_NOT_EXPLICIT = "PROMOTION_DECISION_RECEIPT_FAIL_SELECTION_NOT_EXPLICIT"
FAIL_ACTIVE_ENTRY_CREATED = "PROMOTION_DECISION_RECEIPT_FAIL_ACTIVE_ENTRY_CREATED_INSIDE_RECEIPT"
FAIL_INACTIVE_ENTRY_CREATED = "PROMOTION_DECISION_RECEIPT_FAIL_INACTIVE_ENTRY_CREATED_INSIDE_RECEIPT"
FAIL_REUSE_APPLIED = "PROMOTION_DECISION_RECEIPT_FAIL_REUSE_AUTHORITY_APPLIED_INSIDE_RECEIPT"
FAIL_ACTIVATION_APPLIED = "PROMOTION_DECISION_RECEIPT_FAIL_ACTIVATION_APPLIED_INSIDE_RECEIPT"
FAIL_MACHINE_PROCEED = "PROMOTION_DECISION_RECEIPT_FAIL_MACHINE_PROCEED_INSIDE_RECEIPT"
FAIL_NEXT_UNIT_SURFACE = "PROMOTION_DECISION_RECEIPT_FAIL_NEXT_UNIT_SURFACE_PREPARED_INSIDE_RECEIPT"
FAIL_AUTHORITY_CHANGED = "PROMOTION_DECISION_RECEIPT_FAIL_AUTHORITY_CHANGED_INSIDE_RECEIPT"
FAIL_RUNNER_AUTHORITY = "PROMOTION_DECISION_RECEIPT_FAIL_RUNNER_AUTHORITY_CREATED"
FAIL_MARKDOWN_JSON_PARITY = "PROMOTION_DECISION_RECEIPT_FAIL_MARKDOWN_JSON_PARITY"

FAILURE_VOCABULARY = [
    FAIL_SURFACE_MISSING,
    FAIL_CANDIDATE_MISSING,
    FAIL_CANDIDATE_AUDIT_MISSING,
    FAIL_CANDIDATE_AUDIT_NOT_PASS,
    FAIL_SELECTED_OPTION_MISSING,
    FAIL_OPTION_NOT_ON_SURFACE,
    FAIL_SCOPE_MISMATCH,
    FAIL_RADIUS_MISMATCH,
    FAIL_HUMAN_SELECTION_MISSING,
    FAIL_SELECTION_NOT_EXPLICIT,
    FAIL_ACTIVE_ENTRY_CREATED,
    FAIL_INACTIVE_ENTRY_CREATED,
    FAIL_REUSE_APPLIED,
    FAIL_ACTIVATION_APPLIED,
    FAIL_MACHINE_PROCEED,
    FAIL_NEXT_UNIT_SURFACE,
    FAIL_AUTHORITY_CHANGED,
    FAIL_RUNNER_AUTHORITY,
]

FORBIDDEN_SCOPE_TERMS = [
    "ANY_C8_BASIS",
    "ANY_ACCEPTED_BASIS_OBJECT",
    "EXECUTE_UNIT",
    "RADIUS_N_BATCH",
    "RUNNER_AUTHORITY",
]

FORBIDDEN_MARKDOWN_PHRASES = [
    "active now",
    "machine can now proceed",
    "ready to run",
    "archive entry created",
    "reuse applied",
    "activation applied",
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
        fail(FAIL_SURFACE_MISSING, proc.stderr.strip())
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
        (D1_COMMIT, [PROMOTION_SURFACE, "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_surface_v0.md", "scripts/build_c8_n22_candidate_promotion_decision_surface_v0.py"], FAIL_SURFACE_MISSING),
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


def expected_scope() -> dict[str, str]:
    return {
        "candidate_entry_id": CANDIDATE_ID,
        "allowed_current_authority_state": AUTHORITY_STATE,
        "allowed_requested_action": REQUESTED_ACTION,
        "allowed_requested_action_scope": REQUESTED_SCOPE,
        "allowed_basis_scope": BASIS_SCOPE,
        "allowed_source_object_id": SOURCE_OBJECT_ID,
        "allowed_output_kind": OUTPUT_KIND,
        "radius": SELECTED_RADIUS,
    }


def expected_effect() -> dict[str, object]:
    return {
        "promotion_status": "PROMOTION_GRANTED_FOR_DECLARED_SCOPE",
        "reuse_authority_status": "REUSE_AUTHORITY_GRANTED_FOR_DECLARED_SCOPE",
        "activation_status": "ACTIVATION_ACTIVE",
        "active_archive_entry_may_be_materialized_by_d3": True,
        "machine_proceed_eligible_only_after_d3_materializes_active_entry": True,
    }


def receipt_boundary() -> dict[str, object]:
    return {
        "promotion_decision_recorded_by_this_receipt": True,
        "active_archive_entry_created_by_this_receipt": False,
        "inactive_archive_entry_created_by_this_receipt": False,
        "reuse_authority_applied_by_this_receipt": False,
        "activation_applied_by_this_receipt": False,
        "machine_proceed_performed_by_this_receipt": False,
        "next_unit_definition_surface_prepared_by_this_receipt": False,
        "authority_changed_by_this_receipt": False,
        "runner_authority_created_by_this_receipt": False,
        "requires_archive_entry_materialization": True,
        "requires_active_archive_entry_materialization": True,
        "next_required_object": NEXT_REQUIRED_OBJECT,
    }


def find_selected_option(surface: dict[str, Any]) -> dict[str, Any]:
    if not SELECTED_OPTION:
        fail(FAIL_SELECTED_OPTION_MISSING)
    options = surface.get("decision_options", [])
    for option in options:
        if option.get("decision_option_id") == SELECTED_OPTION:
            return option
    fail(FAIL_OPTION_NOT_ON_SURFACE, SELECTED_OPTION)


def validate_sources(surface: dict[str, Any], candidate: dict[str, Any], audit: dict[str, Any]) -> dict[str, Any]:
    expect(surface.get("schema_version"), SURFACE_SCHEMA_VERSION, FAIL_SURFACE_MISSING, "surface.schema_version")
    expect(surface.get("promotion_decision_surface_id"), SURFACE_ID, FAIL_SURFACE_MISSING, "promotion_decision_surface_id")
    expect(surface.get("terminal_transition"), "ADVANCE(D2_HUMAN_PROMOTION_DECISION_RECEIPT_PENDING)", FAIL_SURFACE_MISSING, "surface.terminal_transition")
    expect(candidate.get("archive_entry_id"), CANDIDATE_ID, FAIL_CANDIDATE_MISSING, "archive_entry_id")
    expect(candidate.get("archive_entry_status"), ARCHIVE_ENTRY_STATUS, FAIL_CANDIDATE_MISSING, "archive_entry_status")
    expect(candidate.get("promotion_status"), PROMOTION_STATUS_BEFORE, FAIL_CANDIDATE_MISSING, "promotion_status")
    expect(candidate.get("reuse_authority_status"), REUSE_AUTHORITY_STATUS_BEFORE, FAIL_CANDIDATE_MISSING, "reuse_authority_status")
    expect(candidate.get("activation_status"), ACTIVATION_STATUS_BEFORE, FAIL_CANDIDATE_MISSING, "activation_status")
    expect(candidate.get("activation_status_reason"), ACTIVATION_STATUS_REASON_BEFORE, FAIL_CANDIDATE_MISSING, "activation_status_reason")
    expect(candidate.get("active_archive_entry_status"), ACTIVE_ARCHIVE_ENTRY_STATUS_BEFORE, FAIL_CANDIDATE_MISSING, "active_archive_entry_status")
    expect(audit.get("audit_id"), CANDIDATE_AUDIT_ID, FAIL_CANDIDATE_AUDIT_MISSING, "audit_id")
    result = audit.get("audit_result", {})
    expect(result.get("candidate_audit_status"), CANDIDATE_AUDIT_STATUS, FAIL_CANDIDATE_AUDIT_NOT_PASS, "candidate_audit_status")
    expect(result.get("candidate_contract_conformant"), True, FAIL_CANDIDATE_AUDIT_NOT_PASS, "candidate_contract_conformant")
    expect(result.get("candidate_promoted"), False, FAIL_CANDIDATE_AUDIT_NOT_PASS, "candidate_promoted")
    expect(result.get("candidate_reusable"), False, FAIL_CANDIDATE_AUDIT_NOT_PASS, "candidate_reusable")
    expect(result.get("candidate_active"), False, FAIL_CANDIDATE_AUDIT_NOT_PASS, "candidate_active")
    selected = find_selected_option(surface)
    scope = selected.get("promotion_scope", {})
    for key, wanted in expected_scope().items():
        code = FAIL_RADIUS_MISMATCH if key == "radius" else FAIL_SCOPE_MISMATCH
        expect(scope.get(key), wanted, code, key)
    scope_text = json.dumps(scope, sort_keys=True)
    for term in FORBIDDEN_SCOPE_TERMS:
        if term in scope_text:
            fail(FAIL_SCOPE_MISMATCH, term)
    effect = selected.get("effect_if_selected_and_applied_by_d3", {})
    for key, wanted in expected_effect().items():
        expect(effect.get(key), wanted, FAIL_SCOPE_MISMATCH, f"effect.{key}")
    return selected


def build_record(root: Path) -> dict[str, Any]:
    verify_expected_commits(root)
    surface = load_json(root, PROMOTION_SURFACE, FAIL_SURFACE_MISSING)
    candidate = load_json(root, CANDIDATE_ENTRY, FAIL_CANDIDATE_MISSING)
    audit = load_json(root, CANDIDATE_AUDIT, FAIL_CANDIDATE_AUDIT_MISSING)
    selected = validate_sources(surface, candidate, audit)
    scope = dict(selected["promotion_scope"])
    effect = dict(selected["effect_if_selected_and_applied_by_d3"])
    boundary = receipt_boundary()
    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "promotion_decision_receipt_id": RECEIPT_ID,
        "receipt_role": RECEIPT_ROLE,
        "receipt_status": RECEIPT_STATUS,
        "block_id": BLOCK_ID,
        "block_unit_id": BLOCK_UNIT_ID,
        "generated_by": GENERATOR,
        "source_promotion_decision_surface_id": surface["promotion_decision_surface_id"],
        "source_candidate_entry_id": candidate["archive_entry_id"],
        "source_candidate_audit_id": audit["audit_id"],
        "decision_event": {
            "decision_actor_class": DECISION_ACTOR_CLASS,
            "decision_event_status": DECISION_EVENT_STATUS,
            "selection_source": SELECTION_SOURCE,
            "selected_promotion_option": SELECTED_OPTION,
            "selected_option_present_on_surface": True,
        },
        "candidate_state_before": {
            "candidate_entry_status": candidate["archive_entry_status"],
            "candidate_audit_status": audit["audit_result"]["candidate_audit_status"],
            "promotion_status_before": candidate["promotion_status"],
            "reuse_authority_status_before": candidate["reuse_authority_status"],
            "activation_status_before": candidate["activation_status"],
            "activation_status_reason_before": candidate["activation_status_reason"],
            "active_archive_entry_status_before": candidate["active_archive_entry_status"],
        },
        "selected_option_scope_copied_from_surface": scope,
        "selected_option_effect_if_applied_by_d3": effect,
        "application_boundary": boundary,
        "receipt_gate": {
            "promotion_decision_receipt_gate": RECEIPT_GATE,
            "source_surface_present": True,
            "candidate_entry_present": True,
            "candidate_audit_present": True,
            "candidate_audit_status": CANDIDATE_AUDIT_STATUS,
            "selected_promotion_option": SELECTED_OPTION,
            "selected_option_present_on_surface": True,
            "selected_option_scope_matches_surface": True,
            "decision_actor_class": DECISION_ACTOR_CLASS,
            "selection_source": SELECTION_SOURCE,
            "human_selection_explicit": True,
            "promotion_decision_recorded": True,
            **boundary,
            "failures": [],
        },
        "precommit_c8_n22_candidate_promotion_decision_receipt_gate": PRECOMMIT_GATE,
        "promotion_decision_receipt_gate": RECEIPT_GATE,
        "selected_branch": {
            "selected_promotion_option": SELECTED_OPTION,
            "promotion_status_if_applied_by_d3": effect["promotion_status"],
            "reuse_authority_status_if_applied_by_d3": effect["reuse_authority_status"],
            "activation_status_if_applied_by_d3": effect["activation_status"],
            "active_archive_entry_may_be_materialized_by_d3": effect["active_archive_entry_may_be_materialized_by_d3"],
            "inactive_archive_entry_may_be_materialized_by_d3": False,
            "machine_proceed_eligible_only_after_d3_materializes_active_entry": effect["machine_proceed_eligible_only_after_d3_materializes_active_entry"],
            "next_required_object": NEXT_REQUIRED_OBJECT,
        },
        "failure_vocabulary": FAILURE_VOCABULARY,
        "non_claims": [
            "D.2 does not create an active archive entry.",
            "D.2 does not create an inactive archive entry.",
            "D.2 does not apply reuse authority.",
            "D.2 does not apply activation.",
            "D.2 does not perform machine proceed.",
            "D.2 does not prepare the next bounded unit definition surface.",
            "D.2 does not execute a unit.",
            "D.2 does not change authority state.",
            "D.2 does not expand candidate scope.",
            "D.2 does not create runner authority.",
            "D.2 only records the explicit human-selected promotion option from D.1.",
            "promotion decision receipt != active archive entry",
            "selected promotion option != materialized promotion",
            "reuse authority if applied != reuse authority applied",
            "activation if applied != activation applied",
        ],
        "key_non_claims": [
            "promotion decision receipt ≠ active archive entry",
            "selected promotion option ≠ materialized promotion",
            "reuse authority if applied ≠ reuse authority applied",
            "activation if applied ≠ activation applied",
        ],
        "unsafe_to_infer": [
            "Unsafe to infer: selected promotion was materialized.",
            "Unsafe to infer: reuse authority has been applied.",
            "Unsafe to infer: activation has been applied.",
            "Unsafe to infer: an active archive entry exists.",
            "Unsafe to infer: machine proceed has occurred.",
        ],
        "terminal_transition": TERMINAL_TRANSITION,
    }
    validate_record(record)
    return record


def validate_record(record: dict[str, Any]) -> None:
    event = record["decision_event"]
    if event.get("decision_actor_class") != DECISION_ACTOR_CLASS:
        fail(FAIL_HUMAN_SELECTION_MISSING)
    if event.get("selection_source") != SELECTION_SOURCE:
        fail(FAIL_SELECTION_NOT_EXPLICIT)
    if event.get("selected_promotion_option") != SELECTED_OPTION:
        fail(FAIL_SELECTED_OPTION_MISSING)
    boundary = record["application_boundary"]
    for key, value in boundary.items():
        if key in {"requires_archive_entry_materialization", "requires_active_archive_entry_materialization"}:
            expect(value, True, FAIL_SCOPE_MISMATCH, key)
        elif key == "next_required_object":
            expect(value, NEXT_REQUIRED_OBJECT, FAIL_SCOPE_MISMATCH, key)
        elif key == "promotion_decision_recorded_by_this_receipt":
            expect(value, True, FAIL_HUMAN_SELECTION_MISSING, key)
        else:
            code_by_field = {
                "active_archive_entry_created_by_this_receipt": FAIL_ACTIVE_ENTRY_CREATED,
                "inactive_archive_entry_created_by_this_receipt": FAIL_INACTIVE_ENTRY_CREATED,
                "reuse_authority_applied_by_this_receipt": FAIL_REUSE_APPLIED,
                "activation_applied_by_this_receipt": FAIL_ACTIVATION_APPLIED,
                "machine_proceed_performed_by_this_receipt": FAIL_MACHINE_PROCEED,
                "next_unit_definition_surface_prepared_by_this_receipt": FAIL_NEXT_UNIT_SURFACE,
                "authority_changed_by_this_receipt": FAIL_AUTHORITY_CHANGED,
                "runner_authority_created_by_this_receipt": FAIL_RUNNER_AUTHORITY,
            }
            expect(value, False, code_by_field[key], key)
    gate = record["receipt_gate"]
    expect(gate.get("promotion_decision_receipt_gate"), RECEIPT_GATE, FAIL_HUMAN_SELECTION_MISSING, "receipt_gate")
    expect(gate.get("failures"), [], FAIL_HUMAN_SELECTION_MISSING, "receipt_gate.failures")
    for key, value in boundary.items():
        expect(gate.get(key), value, FAIL_SCOPE_MISMATCH, f"receipt_gate.{key}")


def validate_no_forbidden_files(root: Path) -> None:
    forbidden = [
        "docs/matrixlabs/validator_archive/active",
        "docs/matrixlabs/validator_archive/promoted",
        "docs/matrixlabs/validator_archive/promotion/c8_n22_selected_archive_entry_state_materialization_v0.json",
        "docs/matrixlabs/validator_archive/promotion/c8_n22_selected_archive_entry_state_materialization_v0.md",
        "docs/matrixlabs/validator_archive/promotion/c8_n22_prepare_next_unit_definition_active_archive_entry_v0.json",
        "docs/matrixlabs/validator_archive/promotion/c8_n22_prepare_next_unit_definition_active_archive_entry_v0.md",
        "docs/matrixlabs/next_units/c8_n22_next_bounded_unit_v0.json",
        "docs/matrixlabs/next_units/c8_n22_next_bounded_unit_v0.md",
        "docs/matrixlabs/observability/c8_observed_decision_path_update_d2_proposal_v0.json",
        "docs/matrixlabs/runners/c8_n22_runner_v0.json",
        "scripts/build_c8_n22_selected_archive_entry_state_materialization_v0.py",
        "scripts/build_c8_n22_machine_proceed_under_active_entry_v0.py",
    ]
    existing = [path for path in forbidden if (root / path).exists()]
    if existing:
        fail(FAIL_ACTIVE_ENTRY_CREATED, ",".join(existing))


def render_markdown(record: dict[str, Any]) -> str:
    scope = record["selected_option_scope_copied_from_surface"]
    effect = record["selected_option_effect_if_applied_by_d3"]
    event = record["decision_event"]
    return "\n".join(
        [
            "# C8 n22 candidate promotion decision receipt v0",
            "",
            "## Status",
            "",
            record["promotion_decision_receipt_gate"],
            "",
            "## Selected promotion option",
            "",
            event["selected_promotion_option"],
            "",
            "## Decision actor",
            "",
            event["decision_actor_class"],
            "",
            "## Selection source",
            "",
            event["selection_source"],
            "",
            "## Source promotion surface",
            "",
            record["source_promotion_decision_surface_id"],
            "",
            "## Candidate",
            "",
            record["source_candidate_entry_id"],
            "",
            "## Candidate audit",
            "",
            record["candidate_state_before"]["candidate_audit_status"],
            "",
            "## Selected promotion scope",
            "",
            f"- authority state: {scope['allowed_current_authority_state']}",
            f"- requested action: {scope['allowed_requested_action']}",
            f"- requested scope: {scope['allowed_requested_action_scope']}",
            f"- basis scope: {scope['allowed_basis_scope']}",
            f"- source object: {scope['allowed_source_object_id']}",
            f"- output kind: {scope['allowed_output_kind']}",
            f"- radius: {scope['radius']}",
            "",
            "## Effect if applied by D.3",
            "",
            f"- promotion status: {effect['promotion_status']}",
            f"- reuse authority: {effect['reuse_authority_status']}",
            f"- activation: {effect['activation_status']}",
            "",
            "## Application boundary",
            "",
            "This receipt records the human promotion decision.",
            "",
            "It does not create the active archive entry.",
            "",
            "It does not create the inactive archive entry.",
            "",
            "It does not apply reuse authority.",
            "",
            "It does not apply activation.",
            "",
            "It does not perform machine proceed.",
            "",
            "## Next required object",
            "",
            record["application_boundary"]["next_required_object"],
        ]
    ).rstrip() + "\n"


def validate_markdown(record: dict[str, Any], markdown: str) -> None:
    required = [
        "# C8 n22 candidate promotion decision receipt v0",
        RECEIPT_GATE,
        SELECTED_OPTION,
        DECISION_ACTOR_CLASS,
        SELECTION_SOURCE,
        SURFACE_ID,
        CANDIDATE_ID,
        CANDIDATE_AUDIT_STATUS,
        f"- authority state: {AUTHORITY_STATE}",
        f"- requested action: {REQUESTED_ACTION}",
        f"- requested scope: {REQUESTED_SCOPE}",
        f"- basis scope: {BASIS_SCOPE}",
        f"- source object: {SOURCE_OBJECT_ID}",
        f"- output kind: {OUTPUT_KIND}",
        f"- radius: {SELECTED_RADIUS}",
        "- promotion status: PROMOTION_GRANTED_FOR_DECLARED_SCOPE",
        "- reuse authority: REUSE_AUTHORITY_GRANTED_FOR_DECLARED_SCOPE",
        "- activation: ACTIVATION_ACTIVE",
        "This receipt records the human promotion decision.",
        "It does not create the active archive entry.",
        "It does not create the inactive archive entry.",
        "It does not apply reuse authority.",
        "It does not apply activation.",
        "It does not perform machine proceed.",
        NEXT_REQUIRED_OBJECT,
    ]
    missing = [phrase for phrase in required if phrase not in markdown]
    if missing:
        fail(FAIL_MARKDOWN_JSON_PARITY, str(missing))
    lower = markdown.lower()
    hits = [phrase for phrase in FORBIDDEN_MARKDOWN_PHRASES if phrase in lower]
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
    event = record["decision_event"]
    before = record["candidate_state_before"]
    scope = record["selected_option_scope_copied_from_surface"]
    effect = record["selected_option_effect_if_applied_by_d3"]
    boundary = record["application_boundary"]
    print("BUILD_C8_N22_CANDIDATE_PROMOTION_DECISION_RECEIPT_V0_COMPLETE")
    print(f"promotion_decision_receipt_id={record['promotion_decision_receipt_id']}")
    print(f"schema_version={record['schema_version']}")
    print(f"receipt_role={record['receipt_role']}")
    print(f"receipt_status={record['receipt_status']}")
    print(f"block_id={record['block_id']}")
    print(f"block_unit_id={record['block_unit_id']}")
    print(f"source_promotion_decision_surface_id={record['source_promotion_decision_surface_id']}")
    print(f"source_candidate_entry_id={record['source_candidate_entry_id']}")
    print(f"source_candidate_audit_id={record['source_candidate_audit_id']}")
    print(f"decision_actor_class={event['decision_actor_class']}")
    print(f"decision_event_status={event['decision_event_status']}")
    print(f"selection_source={event['selection_source']}")
    print(f"selected_promotion_option={event['selected_promotion_option']}")
    print(f"selected_option_present_on_surface={bool_text(event['selected_option_present_on_surface'])}")
    print("selected_option_scope_matches_surface=true")
    print(f"candidate_entry_status={before['candidate_entry_status']}")
    print(f"candidate_audit_status={before['candidate_audit_status']}")
    print(f"promotion_status_before={before['promotion_status_before']}")
    print(f"reuse_authority_status_before={before['reuse_authority_status_before']}")
    print(f"activation_status_before={before['activation_status_before']}")
    print(f"activation_status_reason_before={before['activation_status_reason_before']}")
    print(f"active_archive_entry_status_before={before['active_archive_entry_status_before']}")
    print(f"selected_scope_radius={scope['radius']}")
    print(f"promotion_status_if_applied_by_d3={effect['promotion_status']}")
    print(f"reuse_authority_status_if_applied_by_d3={effect['reuse_authority_status']}")
    print(f"activation_status_if_applied_by_d3={effect['activation_status']}")
    for key in [
        "promotion_decision_recorded_by_this_receipt",
        "active_archive_entry_created_by_this_receipt",
        "inactive_archive_entry_created_by_this_receipt",
        "reuse_authority_applied_by_this_receipt",
        "activation_applied_by_this_receipt",
        "machine_proceed_performed_by_this_receipt",
        "next_unit_definition_surface_prepared_by_this_receipt",
        "authority_changed_by_this_receipt",
        "runner_authority_created_by_this_receipt",
        "requires_archive_entry_materialization",
        "requires_active_archive_entry_materialization",
    ]:
        print(f"{key}={bool_text(boundary[key])}")
    print(f"next_required_object={boundary['next_required_object']}")
    print(f"promotion_decision_receipt_gate={record['promotion_decision_receipt_gate']}")
    print(f"precommit_c8_n22_candidate_promotion_decision_receipt_gate={record['precommit_c8_n22_candidate_promotion_decision_receipt_gate']}")
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
