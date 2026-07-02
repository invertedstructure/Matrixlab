#!/usr/bin/env python3
"""Build the C8 n22 authority transition closure v0.

This closes Block A by preserving the committed A3 authority-state update. It
does not apply another transition, create a router, update the observed path,
define a next unit, or authorize execution.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_authority_transition_closure_v0.py"
OUTPUT_JSON = "docs/matrixlabs/boundary/c8_n22_authority_transition_closure_v0.json"
OUTPUT_MD = "docs/matrixlabs/boundary/c8_n22_authority_transition_closure_v0.md"

BOUNDARY = "docs/matrixlabs/boundary/c8_n22_authority_boundary_transition_record_v0.json"
READABOUT = "docs/matrixlabs/readabouts/c8_n22_authority_boundary_readabout_v0.json"
SURFACE = "docs/matrixlabs/decision_surfaces/c8_n22_human_decision_surface_v0.json"
RECEIPT = "docs/matrixlabs/decisions/c8_n22_human_decision_receipt_v0.json"
UPDATE = "docs/matrixlabs/boundary/c8_n22_authority_state_update_v0.json"

COMMITS = {
    BOUNDARY: "c0e560c3d22d17ffcc734477c588a6f352950c13",
    READABOUT: "fa4deb54341ef17b0cdf71411220a0a68fea2ca8",
    SURFACE: "c006f0fd1a9833009c5660900534a692402fbe6e",
    RECEIPT: "3bd78924073756c8a3640082897d6ade5780970d",
    UPDATE: "d8a5116ec1be3756b1ad0aa6656187c91c71e87f",
}

SCHEMA_VERSION = "matrixlabs_authority_transition_closure_v0"
CLOSURE_ID = "c8.n22.authority_transition_closure.v0"
CLOSURE_ROLE = "BLOCK_A_AUTHORITY_TRANSITION_CLOSURE"
SOURCE_OBJECT_ID = "c8.n22"
SELECTED_OPTION = "DECISION_ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION"
PASS_STATUS = "AUTHORITY_TRANSITION_CLOSURE_PASS"

FAIL_BOUNDARY_RECORD_MISSING = "CLOSURE_FAIL_BOUNDARY_RECORD_MISSING"
FAIL_READABOUT_MISSING = "CLOSURE_FAIL_READABOUT_MISSING"
FAIL_READABOUT_NOT_PARITY = "CLOSURE_FAIL_READABOUT_NOT_PARITY"
FAIL_DECISION_SURFACE_MISSING = "CLOSURE_FAIL_DECISION_SURFACE_MISSING"
FAIL_DECISION_SURFACE_INVALID = "CLOSURE_FAIL_DECISION_SURFACE_INVALID"
FAIL_DECISION_RECEIPT_MISSING = "CLOSURE_FAIL_DECISION_RECEIPT_MISSING"
FAIL_DECISION_RECEIPT_INVALID = "CLOSURE_FAIL_DECISION_RECEIPT_INVALID"
FAIL_AUTHORITY_UPDATE_MISSING = "CLOSURE_FAIL_AUTHORITY_UPDATE_MISSING"
FAIL_AUTHORITY_UPDATE_INVALID = "CLOSURE_FAIL_AUTHORITY_UPDATE_INVALID"
FAIL_SOURCE_CHAIN_INCOMPLETE = "CLOSURE_FAIL_SOURCE_CHAIN_INCOMPLETE"
FAIL_RESULTING_STATE_MISMATCH = "CLOSURE_FAIL_RESULTING_STATE_MISMATCH"
FAIL_NEXT_SURFACE_MISMATCH = "CLOSURE_FAIL_NEXT_SURFACE_MISMATCH"
FAIL_AUTHORITY_EFFECT_MISMATCH = "CLOSURE_FAIL_AUTHORITY_EFFECT_MISMATCH"
FAIL_NEXT_UNIT_DEFINITION_AUTHORITY_SMUGGLED = (
    "CLOSURE_FAIL_NEXT_UNIT_DEFINITION_AUTHORITY_SMUGGLED"
)
FAIL_EXECUTION_AUTHORITY_SMUGGLED = "CLOSURE_FAIL_EXECUTION_AUTHORITY_SMUGGLED"
FAIL_REUSE_AUTHORITY_SMUGGLED = "CLOSURE_FAIL_REUSE_AUTHORITY_SMUGGLED"
FAIL_PROMOTION_AUTHORITY_SMUGGLED = "CLOSURE_FAIL_PROMOTION_AUTHORITY_SMUGGLED"
FAIL_UPDATER_GENERALIZATION_SMUGGLED = "CLOSURE_FAIL_UPDATER_GENERALIZATION_SMUGGLED"
FAIL_RUNNER_AUTHORITY_SMUGGLED = "CLOSURE_FAIL_RUNNER_AUTHORITY_SMUGGLED"
FAIL_RECEIPT_REWRITE_AUTHORITY_SMUGGLED = "CLOSURE_FAIL_RECEIPT_REWRITE_AUTHORITY_SMUGGLED"
FAIL_OBSERVED_PATH_UPDATE_SMUGGLED = "CLOSURE_FAIL_OBSERVED_PATH_UPDATE_SMUGGLED"
FAIL_BLOCK_STATUS_OVERSTATED = "CLOSURE_FAIL_BLOCK_STATUS_OVERSTATED"
FAIL_RECOMMENDATION_INSERTED = "CLOSURE_FAIL_RECOMMENDATION_INSERTED"
FAIL_MARKDOWN_JSON_PARITY = "CLOSURE_FAIL_MARKDOWN_JSON_PARITY"

AUTHORITY_EFFECTS = {
    "basis_for_next_unit_definition_authority": "GRANTED",
    "next_unit_definition_surface_preparation_authority": "GRANTED",
    "next_unit_definition_authority": "NOT_GRANTED",
    "execution_authority": "NOT_GRANTED",
    "reuse_authority": "NOT_GRANTED",
    "taxonomy_promotion_authority": "NOT_GRANTED",
    "updater_generalization_authority": "NOT_GRANTED",
    "runner_authority": "NOT_GRANTED",
}

STILL_NOT_AUTHORIZED = {
    "next_unit_definition_finalization_authority": "NOT_GRANTED",
    "execution_authority": "NOT_GRANTED",
    "reuse_authority": "NOT_GRANTED",
    "taxonomy_promotion_authority": "NOT_GRANTED",
    "updater_generalization_authority": "NOT_GRANTED",
    "runner_authority": "NOT_GRANTED",
    "receipt_rewrite_authority": "NOT_GRANTED",
    "observed_path_update_authority": "NOT_GRANTED",
}

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
    "next unit is defined",
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
    path_groups = {
        BOUNDARY: [
            BOUNDARY,
            "docs/matrixlabs/boundary/c8_n22_authority_boundary_transition_record_v0.md",
            "scripts/build_c8_n22_authority_boundary_transition_record_v0.py",
        ],
        READABOUT: [
            READABOUT,
            "docs/matrixlabs/readabouts/c8_n22_authority_boundary_readabout_v0.md",
            "scripts/build_c8_n22_authority_boundary_readabout_v0.py",
        ],
        SURFACE: [
            SURFACE,
            "docs/matrixlabs/decision_surfaces/c8_n22_human_decision_surface_v0.md",
            "scripts/build_c8_n22_human_decision_surface_v0.py",
        ],
        RECEIPT: [
            RECEIPT,
            "docs/matrixlabs/decisions/c8_n22_human_decision_receipt_v0.md",
            "scripts/build_c8_n22_human_decision_receipt_v0.py",
        ],
        UPDATE: [
            UPDATE,
            "docs/matrixlabs/boundary/c8_n22_authority_state_update_v0.md",
            "scripts/build_c8_n22_authority_state_update_v0.py",
        ],
    }
    failure_codes = {
        BOUNDARY: FAIL_BOUNDARY_RECORD_MISSING,
        READABOUT: FAIL_READABOUT_MISSING,
        SURFACE: FAIL_DECISION_SURFACE_MISSING,
        RECEIPT: FAIL_DECISION_RECEIPT_MISSING,
        UPDATE: FAIL_AUTHORITY_UPDATE_MISSING,
    }
    for path, sha in COMMITS.items():
        run_git(root, ["cat-file", "-e", f"{sha}^{{commit}}"], failure_codes[path])
        got = commit_for_paths(root, path_groups[path], failure_codes[path])
        if got != sha:
            fail(failure_codes[path], f"{path} commit mismatch: {got}!={sha}")


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


def assert_eq(got: Any, want: Any, code: str, label: str) -> None:
    if got != want:
        fail(code, f"{label}:{got}!={want}")


def validate_inputs(
    boundary: dict[str, Any],
    readabout: dict[str, Any],
    surface: dict[str, Any],
    receipt: dict[str, Any],
    update: dict[str, Any],
) -> None:
    assert_eq(boundary.get("boundary_record_id"), "c8.n22.boundary_transition.v0", FAIL_BOUNDARY_RECORD_MISSING, "boundary_record_id")
    assert_eq(readabout.get("readabout_packet_id"), "c8.n22.authority_boundary.readabout.v0", FAIL_READABOUT_MISSING, "readabout_packet_id")
    assert_eq(readabout.get("projection_gate", {}).get("readabout_gate"), "READABOUT_PASS_PARITY", FAIL_READABOUT_NOT_PARITY, "readabout_gate")
    assert_eq(surface.get("decision_surface_id"), "c8.n22.human_decision_surface.v0", FAIL_DECISION_SURFACE_MISSING, "decision_surface_id")
    assert_eq(surface.get("surface_status"), "PRESENTS_TYPED_OPTIONS_ONLY", FAIL_DECISION_SURFACE_INVALID, "surface_status")
    assert_eq(surface.get("surface_gate", {}).get("decision_surface_gate"), "DECISION_SURFACE_PASS_OPTIONS_PRESENTED_ONLY", FAIL_DECISION_SURFACE_INVALID, "decision_surface_gate")
    assert_eq(receipt.get("decision_receipt_id"), "c8.n22.human_decision_receipt.v0", FAIL_DECISION_RECEIPT_MISSING, "decision_receipt_id")
    assert_eq(receipt.get("receipt_gate", {}).get("decision_receipt_gate"), "HUMAN_DECISION_RECEIPT_PASS_TYPED_DECISION_RECORDED", FAIL_DECISION_RECEIPT_INVALID, "decision_receipt_gate")
    assert_eq(update.get("authority_update_id"), "c8.n22.authority_state_update.v0", FAIL_AUTHORITY_UPDATE_MISSING, "authority_update_id")
    assert_eq(update.get("update_gate", {}).get("authority_state_update_gate"), "AUTHORITY_UPDATE_PASS_DECISION_APPLIED", FAIL_AUTHORITY_UPDATE_INVALID, "authority_state_update_gate")

    chain_checks = {
        "update.source_boundary_record_id": (update.get("source_boundary_record_id"), "c8.n22.boundary_transition.v0"),
        "update.source_decision_surface_id": (update.get("source_decision_surface_id"), "c8.n22.human_decision_surface.v0"),
        "update.source_decision_receipt_id": (update.get("source_decision_receipt_id"), "c8.n22.human_decision_receipt.v0"),
        "update.source_readabout_id": (update.get("source_readabout_id"), "c8.n22.authority_boundary.readabout.v0"),
        "update.source_readabout_role": (update.get("source_readabout_role"), "AUDIT_REFERENCE_ONLY_DOWNSTREAM_PROJECTION"),
    }
    failures = [f"{label}:{got}!={want}" for label, (got, want) in chain_checks.items() if got != want]
    if failures:
        fail(FAIL_SOURCE_CHAIN_INCOMPLETE, "; ".join(failures))

    surface_option = next(
        (option for option in surface.get("decision_options", []) if option.get("decision_option_id") == SELECTED_OPTION),
        None,
    )
    if surface_option is None:
        fail(FAIL_DECISION_SURFACE_INVALID, SELECTED_OPTION)
    receipt_effects = receipt.get("selected_option_effects_from_surface", {}).get("authority_effects_if_applied_by_a3")
    update_effects = update.get("authority_effects_after_update")
    if surface_option.get("authority_effects") != receipt_effects or receipt_effects != update_effects:
        fail(FAIL_AUTHORITY_EFFECT_MISMATCH)
    if update_effects != AUTHORITY_EFFECTS:
        fail(FAIL_AUTHORITY_EFFECT_MISMATCH)


def validate_no_forbidden_files(root: Path) -> None:
    forbidden_paths = [
        "docs/matrixlabs/observability/c8_observed_decision_path_update_a4_proposal_v0.json",
        "docs/matrixlabs/observability/c8_observed_path_update_a4_apply_v0.json",
        "scripts/build_c8_n22_router_v0.py",
        "docs/matrixlabs/routers/c8_n22_router_v0.json",
        "docs/matrixlabs/next_units/c8_n22_next_bounded_unit_v0.json",
        "docs/matrixlabs/next_units/c8_n22_next_bounded_unit_v0.md",
        "docs/matrixlabs/block_b/c8_n22_block_b_v0.json",
    ]
    existing = [path for path in forbidden_paths if (root / path).exists()]
    if existing:
        fail(FAIL_OBSERVED_PATH_UPDATE_SMUGGLED, str(existing))


def validate_closure_effects(newly: dict[str, str], still: dict[str, str]) -> None:
    if newly != {
        "basis_for_next_unit_definition_authority": "GRANTED",
        "next_unit_definition_surface_preparation_authority": "GRANTED",
        "next_unit_definition_authority": "NOT_GRANTED",
    }:
        fail(FAIL_AUTHORITY_EFFECT_MISMATCH)
    if newly.get("next_unit_definition_authority") != "NOT_GRANTED":
        fail(FAIL_NEXT_UNIT_DEFINITION_AUTHORITY_SMUGGLED)
    if still.get("execution_authority") != "NOT_GRANTED":
        fail(FAIL_EXECUTION_AUTHORITY_SMUGGLED)
    if still.get("reuse_authority") != "NOT_GRANTED":
        fail(FAIL_REUSE_AUTHORITY_SMUGGLED)
    if still.get("taxonomy_promotion_authority") != "NOT_GRANTED":
        fail(FAIL_PROMOTION_AUTHORITY_SMUGGLED)
    if still.get("updater_generalization_authority") != "NOT_GRANTED":
        fail(FAIL_UPDATER_GENERALIZATION_SMUGGLED)
    if still.get("runner_authority") != "NOT_GRANTED":
        fail(FAIL_RUNNER_AUTHORITY_SMUGGLED)
    if still.get("receipt_rewrite_authority") != "NOT_GRANTED":
        fail(FAIL_RECEIPT_REWRITE_AUTHORITY_SMUGGLED)
    if still.get("observed_path_update_authority") != "NOT_GRANTED":
        fail(FAIL_OBSERVED_PATH_UPDATE_SMUGGLED)


def build_closure(root: Path) -> dict[str, Any]:
    verify_expected_commits(root)
    validate_no_forbidden_files(root)
    boundary = load_json(root, BOUNDARY, FAIL_BOUNDARY_RECORD_MISSING)
    readabout = load_json(root, READABOUT, FAIL_READABOUT_MISSING)
    surface = load_json(root, SURFACE, FAIL_DECISION_SURFACE_MISSING)
    receipt = load_json(root, RECEIPT, FAIL_DECISION_RECEIPT_MISSING)
    update = load_json(root, UPDATE, FAIL_AUTHORITY_UPDATE_MISSING)
    validate_inputs(boundary, readabout, surface, receipt, update)

    update_gate = update["update_gate"]
    update_effects = update["authority_effects_after_update"]
    next_router = update["next_router_state"]
    newly_authorized = {
        "basis_for_next_unit_definition_authority": update_effects["basis_for_next_unit_definition_authority"],
        "next_unit_definition_surface_preparation_authority": update_effects[
            "next_unit_definition_surface_preparation_authority"
        ],
        "next_unit_definition_authority": update_effects["next_unit_definition_authority"],
    }
    still_not_authorized = dict(STILL_NOT_AUTHORIZED)
    validate_closure_effects(newly_authorized, still_not_authorized)

    block = {
        "block_id": "BLOCK_A",
        "block_name": "complete_one_human_authority_transition_cycle",
        "block_status": "BLOCK_A_PASS_AUTHORITY_ADVANCED_TO_BASIS",
        "block_terminal": True,
    }
    source_chain = {
        "boundary_record_id": "c8.n22.boundary_transition.v0",
        "readabout_id": "c8.n22.authority_boundary.readabout.v0",
        "decision_surface_id": "c8.n22.human_decision_surface.v0",
        "decision_receipt_id": "c8.n22.human_decision_receipt.v0",
        "authority_update_id": "c8.n22.authority_state_update.v0",
    }
    source_roles = {
        "boundary_record_role": "FORMAL_AUTHORITY_BOUNDARY_RECORD",
        "readabout_role": "AUDIT_REFERENCE_ONLY_DOWNSTREAM_PROJECTION",
        "decision_surface_role": "HUMAN_DECISION_SURFACE",
        "decision_receipt_role": "HUMAN_DECISION_EVENT_RECEIPT",
        "authority_update_role": "FORMAL_AUTHORITY_STATE_TRANSITION_APPLICATION",
    }
    summary = {
        "prior_authority_state": update_gate["prior_authority_state"],
        "selected_decision_option": update_gate["selected_decision_option"],
        "authority_event_applied": update_gate["authority_event_applied"],
        "authority_event_status_after": update_gate["authority_event_status_after"],
        "resulting_authority_state": update_gate["new_authority_state"],
        "decision_receipt_application_status": update_gate["decision_receipt_application_status"],
    }
    next_lawful_surface = {
        "router_action": next_router["next_allowed_router_action"],
        "surface_scope": "C8_N22_BASIS_ONLY",
        "machine_permitted_action_scope": next_router["machine_permitted_action_scope"],
        "execution_allowed": False,
    }
    closure = {
        "schema_version": SCHEMA_VERSION,
        "closure_id": CLOSURE_ID,
        "closure_role": CLOSURE_ROLE,
        "generated_by": GENERATOR,
        "source_object_id": SOURCE_OBJECT_ID,
        "block": block,
        "source_chain": source_chain,
        "source_roles": source_roles,
        "source": {
            "boundary_record_path": BOUNDARY,
            "readabout_path": READABOUT,
            "decision_surface_path": SURFACE,
            "decision_receipt_path": RECEIPT,
            "authority_update_path": UPDATE,
            "source_commits": dict(COMMITS),
            "source_hashes": {
                "boundary_record_sha256": sha256_file(root / BOUNDARY),
                "readabout_sha256": sha256_file(root / READABOUT),
                "decision_surface_sha256": sha256_file(root / SURFACE),
                "decision_receipt_sha256": sha256_file(root / RECEIPT),
                "authority_update_sha256": sha256_file(root / UPDATE),
            },
        },
        "authority_transition_summary": summary,
        "newly_authorized": newly_authorized,
        "still_not_authorized": still_not_authorized,
        "next_lawful_surface": next_lawful_surface,
        "closure_gate": {
            "closure_status": PASS_STATUS,
            "boundary_record_present": True,
            "readabout_present": True,
            "readabout_gate": "READABOUT_PASS_PARITY",
            "decision_surface_present": True,
            "decision_surface_status": "PRESENTS_TYPED_OPTIONS_ONLY",
            "decision_receipt_present": True,
            "decision_receipt_gate": "HUMAN_DECISION_RECEIPT_PASS_TYPED_DECISION_RECORDED",
            "authority_update_present": True,
            "authority_update_gate": "AUTHORITY_UPDATE_PASS_DECISION_APPLIED",
            "source_chain_complete": True,
            **summary,
            "next_lawful_surface": next_lawful_surface["router_action"],
            "machine_permitted_action_scope": next_lawful_surface["machine_permitted_action_scope"],
            "basis_for_next_unit_definition_authority": newly_authorized[
                "basis_for_next_unit_definition_authority"
            ],
            "next_unit_definition_surface_preparation_authority": newly_authorized[
                "next_unit_definition_surface_preparation_authority"
            ],
            "next_unit_definition_authority": newly_authorized[
                "next_unit_definition_authority"
            ],
            "execution_authority": still_not_authorized["execution_authority"],
            "reuse_authority": still_not_authorized["reuse_authority"],
            "taxonomy_promotion_authority": still_not_authorized[
                "taxonomy_promotion_authority"
            ],
            "updater_generalization_authority": still_not_authorized[
                "updater_generalization_authority"
            ],
            "runner_authority": still_not_authorized["runner_authority"],
            "receipt_rewrite_authority": still_not_authorized["receipt_rewrite_authority"],
            "observed_path_update_authority": still_not_authorized[
                "observed_path_update_authority"
            ],
            "resulting_state_matches_a3": True,
            "next_lawful_surface_matches_a3": True,
            "authority_effects_match_a3": True,
            "stronger_authority_detected": False,
            "observed_path_update_detected": False,
            "failures": [],
        },
        "non_claims": [
            "A4 does not execute the next bounded unit.",
            "A4 does not define the next bounded unit.",
            "A4 does not authorize the next bounded unit.",
            "A4 does not finalize the next bounded unit definition.",
            "A4 does not update the observed path.",
            "A4 does not propose an observed-path update.",
            "A4 does not apply an observed-path update.",
            "A4 does not create a router.",
            "A4 does not promote taxonomy.",
            "A4 does not authorize reuse.",
            "A4 does not generalize the updater.",
            "A4 does not create runner authority.",
            "A4 does not rewrite receipts.",
            "A4 does not validate theorem truth.",
            "A4 does not validate edge lawfulness.",
            "A4 does not make Block A reusable.",
            "A4 only closes and preserves the completed c8.n22 authority transition cycle.",
            "The next lawful surface is preparation of the next bounded unit definition surface.",
        ],
        "unsafe_to_infer": [
            "Unsafe to infer: the next bounded unit has been defined.",
            "Unsafe to infer: the next bounded unit has been authorized.",
            "Unsafe to infer: the next bounded unit may execute.",
            "Unsafe to infer: Block B exists.",
            "Unsafe to infer: a router exists.",
            "Unsafe to infer: the observed path has been updated.",
            "Unsafe to infer: an observed-path update has been proposed.",
            "Unsafe to infer: Block A is reusable.",
            "Unsafe to infer: runtime execution is authorized.",
        ],
    }
    validate_closure(closure, update)
    return closure


def validate_closure(closure: dict[str, Any], update: dict[str, Any]) -> None:
    block = closure["block"]
    if block != {
        "block_id": "BLOCK_A",
        "block_name": "complete_one_human_authority_transition_cycle",
        "block_status": "BLOCK_A_PASS_AUTHORITY_ADVANCED_TO_BASIS",
        "block_terminal": True,
    }:
        fail(FAIL_BLOCK_STATUS_OVERSTATED)
    summary = closure["authority_transition_summary"]
    if summary["resulting_authority_state"] != update["authority_state_after"]["new_authority_state"]:
        fail(FAIL_RESULTING_STATE_MISMATCH)
    if closure["next_lawful_surface"]["router_action"] != update["next_router_state"]["next_allowed_router_action"]:
        fail(FAIL_NEXT_SURFACE_MISMATCH)
    combined_effects = dict(AUTHORITY_EFFECTS)
    if combined_effects != update["authority_effects_after_update"]:
        fail(FAIL_AUTHORITY_EFFECT_MISMATCH)
    validate_closure_effects(closure["newly_authorized"], closure["still_not_authorized"])
    gate = closure["closure_gate"]
    if gate.get("closure_status") != PASS_STATUS:
        fail(FAIL_BLOCK_STATUS_OVERSTATED)
    if gate.get("source_chain_complete") is not True:
        fail(FAIL_SOURCE_CHAIN_INCOMPLETE)
    if gate.get("stronger_authority_detected") is not False:
        fail(FAIL_AUTHORITY_EFFECT_MISMATCH)
    if gate.get("observed_path_update_detected") is not False:
        fail(FAIL_OBSERVED_PATH_UPDATE_SMUGGLED)
    if gate.get("failures") != []:
        fail(FAIL_SOURCE_CHAIN_INCOMPLETE)
    hits = scan_text_for_recommendations(json.dumps(closure, sort_keys=True))
    if hits:
        fail(FAIL_RECOMMENDATION_INSERTED, str(hits))


def render_markdown(closure: dict[str, Any]) -> str:
    block = closure["block"]
    chain = closure["source_chain"]
    summary = closure["authority_transition_summary"]
    newly = closure["newly_authorized"]
    next_surface = closure["next_lawful_surface"]
    lines = [
        "# C8 n22 authority transition closure v0",
        "",
        "## Status",
        "",
        block["block_status"],
        "",
        "## Closure status",
        "",
        closure["closure_gate"]["closure_status"],
        "",
        "## Completed chain",
        "",
        f"- boundary record: {chain['boundary_record_id']}",
        f"- Readabout: {chain['readabout_id']}",
        f"- decision surface: {chain['decision_surface_id']}",
        f"- decision receipt: {chain['decision_receipt_id']}",
        f"- authority update: {chain['authority_update_id']}",
        "",
        "## Authority transition",
        "",
        f"- prior state: {summary['prior_authority_state']}",
        f"- selected option: {summary['selected_decision_option']}",
        f"- authority event applied: {summary['authority_event_applied']}",
        f"- authority event status after: {summary['authority_event_status_after']}",
        f"- new state: {summary['resulting_authority_state']}",
        f"- decision receipt application status: {summary['decision_receipt_application_status']}",
        "",
        "## Newly authorized",
        "",
        "- basis for next-unit definition authority: "
        f"{newly['basis_for_next_unit_definition_authority']}",
        "- next-unit definition surface preparation authority: "
        f"{newly['next_unit_definition_surface_preparation_authority']}",
        "",
        "## Still not authorized",
        "",
        "- next-unit definition finalization",
        "- next-unit definition authority",
        "- execution",
        "- receipt rewrite",
        "- observed path update",
        "- taxonomy promotion",
        "- reuse",
        "- updater generalization",
        "- runner authority",
        "",
        "## Next lawful surface",
        "",
        next_surface["router_action"],
        "",
        "## Application boundary",
        "",
        "This closure preserves the completed A3 authority-state update.",
        "",
        "It does not apply a new authority transition.",
        "",
        "It does not execute, define, authorize, or finalize the next bounded unit.",
        "",
        "It does not update or propose an update to the observed path.",
        "",
        "## Non-claims",
        "",
        "This closure does not execute runtime, rewrite receipts, promote taxonomy, authorize reuse, generalize the updater, create runner authority, or make Block A reusable.",
        "",
    ]
    lines.extend(f"- {claim}" for claim in closure["non_claims"])
    lines.extend(["", "## Unsafe to infer", ""])
    lines.extend(f"- {item}" for item in closure["unsafe_to_infer"])
    return "\n".join(lines) + "\n"


def validate_markdown(closure: dict[str, Any], markdown: str) -> None:
    required = [
        "# C8 n22 authority transition closure v0",
        "BLOCK_A_PASS_AUTHORITY_ADVANCED_TO_BASIS",
        "AUTHORITY_TRANSITION_CLOSURE_PASS",
        "## Completed chain",
        "boundary record: c8.n22.boundary_transition.v0",
        "Readabout: c8.n22.authority_boundary.readabout.v0",
        "decision surface: c8.n22.human_decision_surface.v0",
        "decision receipt: c8.n22.human_decision_receipt.v0",
        "authority update: c8.n22.authority_state_update.v0",
        "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
        "## Still not authorized",
        "observed path update",
        "It does not execute, define, authorize, or finalize the next bounded unit.",
        "It does not update or propose an update to the observed path.",
    ]
    missing = [phrase for phrase in required if phrase not in markdown]
    if missing:
        fail(FAIL_MARKDOWN_JSON_PARITY, str(missing))
    hits = scan_text_for_recommendations(markdown)
    if hits:
        fail(FAIL_RECOMMENDATION_INSERTED, str(hits))


def write_outputs(root: Path, closure: dict[str, Any]) -> None:
    markdown = render_markdown(closure)
    validate_markdown(closure, markdown)
    json_path = root / OUTPUT_JSON
    md_path = root / OUTPUT_MD
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(closure, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")


def print_success(closure: dict[str, Any]) -> None:
    block = closure["block"]
    chain = closure["source_chain"]
    summary = closure["authority_transition_summary"]
    newly = closure["newly_authorized"]
    still = closure["still_not_authorized"]
    next_surface = closure["next_lawful_surface"]
    gate = closure["closure_gate"]
    print("BUILD_C8_N22_AUTHORITY_TRANSITION_CLOSURE_V0_COMPLETE")
    print(f"closure_id={closure['closure_id']}")
    print(f"schema_version={closure['schema_version']}")
    print(f"closure_role={closure['closure_role']}")
    print(f"source_object_id={closure['source_object_id']}")
    print(f"block_id={block['block_id']}")
    print(f"block_status={block['block_status']}")
    print(f"block_terminal={str(block['block_terminal']).lower()}")
    print(f"closure_status={gate['closure_status']}")
    print(f"source_chain_complete={str(gate['source_chain_complete']).lower()}")
    print(f"boundary_record_id={chain['boundary_record_id']}")
    print(f"readabout_id={chain['readabout_id']}")
    print(f"decision_surface_id={chain['decision_surface_id']}")
    print(f"decision_receipt_id={chain['decision_receipt_id']}")
    print(f"authority_update_id={chain['authority_update_id']}")
    print(f"selected_decision_option={summary['selected_decision_option']}")
    print(f"prior_authority_state={summary['prior_authority_state']}")
    print(f"authority_event_applied={summary['authority_event_applied']}")
    print(f"authority_event_status_after={summary['authority_event_status_after']}")
    print(f"resulting_authority_state={summary['resulting_authority_state']}")
    print(f"decision_receipt_application_status={summary['decision_receipt_application_status']}")
    print(f"basis_for_next_unit_definition_authority={newly['basis_for_next_unit_definition_authority']}")
    print(
        "next_unit_definition_surface_preparation_authority="
        f"{newly['next_unit_definition_surface_preparation_authority']}"
    )
    print(f"next_unit_definition_authority={newly['next_unit_definition_authority']}")
    print(f"execution_authority={still['execution_authority']}")
    print(f"reuse_authority={still['reuse_authority']}")
    print(f"taxonomy_promotion_authority={still['taxonomy_promotion_authority']}")
    print(f"updater_generalization_authority={still['updater_generalization_authority']}")
    print(f"runner_authority={still['runner_authority']}")
    print(f"receipt_rewrite_authority={still['receipt_rewrite_authority']}")
    print(f"observed_path_update_authority={still['observed_path_update_authority']}")
    print(f"next_lawful_surface={next_surface['router_action']}")
    print(f"machine_permitted_action_scope={next_surface['machine_permitted_action_scope']}")
    print(f"execution_allowed={str(next_surface['execution_allowed']).lower()}")
    print(f"resulting_state_matches_a3={str(gate['resulting_state_matches_a3']).lower()}")
    print(f"next_lawful_surface_matches_a3={str(gate['next_lawful_surface_matches_a3']).lower()}")
    print(f"authority_effects_match_a3={str(gate['authority_effects_match_a3']).lower()}")
    print(f"stronger_authority_detected={str(gate['stronger_authority_detected']).lower()}")
    print(f"observed_path_update_detected={str(gate['observed_path_update_detected']).lower()}")
    print("authority_transition_closed=true")
    print("next_unit_defined=false")
    print("next_unit_authorized=false")
    print("runtime_executed=false")
    print("receipts_rewritten=false")
    print("taxonomy_promoted=false")
    print("runner_authority_created=false")
    print("observed_path_updated=false")
    print("observed_path_update_proposed=false")
    print("router_created=false")
    print("commit_created=false")
    print("push_executed=false")
    print("terminal_transition=STOP_BLOCK_A_CLOSED")


def main() -> int:
    try:
        root = detect_repo_root(Path.cwd())
        closure = build_closure(root)
        write_outputs(root, closure)
    except GenerationError as exc:
        print(f"STOP_{exc.code}")
        return 2
    print_success(closure)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
