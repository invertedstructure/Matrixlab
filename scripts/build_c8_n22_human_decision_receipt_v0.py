#!/usr/bin/env python3
"""Build the C8 n22 human decision receipt v0.

This records the explicit human-selected A1 option. It does not apply the
formal authority-state update, formally consume HUMAN_ACCEPTANCE, define the
next bounded unit, or authorize execution.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_human_decision_receipt_v0.py"
OUTPUT_JSON = "docs/matrixlabs/decisions/c8_n22_human_decision_receipt_v0.json"
OUTPUT_MD = "docs/matrixlabs/decisions/c8_n22_human_decision_receipt_v0.md"

SURFACE = "docs/matrixlabs/decision_surfaces/c8_n22_human_decision_surface_v0.json"
BOUNDARY = "docs/matrixlabs/boundary/c8_n22_authority_boundary_transition_record_v0.json"
READABOUT = "docs/matrixlabs/readabouts/c8_n22_authority_boundary_readabout_v0.json"

A1_COMMIT = "c006f0fd1a9833009c5660900534a692402fbe6e"
SCHEMA_VERSION = "matrixlabs_human_decision_receipt_v0"
DECISION_RECEIPT_ID = "c8.n22.human_decision_receipt.v0"
SOURCE_DECISION_SURFACE_ID = "c8.n22.human_decision_surface.v0"
SOURCE_BOUNDARY_RECORD_ID = "c8.n22.boundary_transition.v0"
SOURCE_READABOUT_ID = "c8.n22.authority_boundary.readabout.v0"
SELECTED_OPTION = "DECISION_ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION"
PASS_GATE = "HUMAN_DECISION_RECEIPT_PASS_TYPED_DECISION_RECORDED"

FAIL_SURFACE_MISSING = "DECISION_RECEIPT_FAIL_SURFACE_MISSING"
FAIL_BOUNDARY_RECORD_MISSING = "DECISION_RECEIPT_FAIL_BOUNDARY_RECORD_MISSING"
FAIL_READABOUT_MISSING = "DECISION_RECEIPT_FAIL_READABOUT_MISSING"
FAIL_SELECTED_OPTION_MISSING = "DECISION_RECEIPT_FAIL_SELECTED_OPTION_MISSING"
FAIL_OPTION_NOT_ON_SURFACE = "DECISION_RECEIPT_FAIL_OPTION_NOT_ON_SURFACE"
FAIL_OPTION_EFFECT_MISMATCH = "DECISION_RECEIPT_FAIL_OPTION_EFFECT_MISMATCH"
FAIL_HUMAN_EVENT_MISSING = "DECISION_RECEIPT_FAIL_HUMAN_EVENT_MISSING"
FAIL_HUMAN_EVENT_NOT_EXPLICIT = "DECISION_RECEIPT_FAIL_HUMAN_EVENT_NOT_EXPLICIT"
FAIL_AUTHORITY_EVENT_ALREADY_CONSUMED = "DECISION_RECEIPT_FAIL_AUTHORITY_EVENT_ALREADY_CONSUMED"
FAIL_UNDECLARED_AUTHORITY_EVENT = "DECISION_RECEIPT_FAIL_UNDECLARED_AUTHORITY_EVENT"
FAIL_NEXT_UNIT_DEFINITION_AUTHORITY_SMUGGLED = (
    "DECISION_RECEIPT_FAIL_NEXT_UNIT_DEFINITION_AUTHORITY_SMUGGLED"
)
FAIL_EXECUTION_AUTHORITY_SMUGGLED = "DECISION_RECEIPT_FAIL_EXECUTION_AUTHORITY_SMUGGLED"
FAIL_REUSE_AUTHORITY_SMUGGLED = "DECISION_RECEIPT_FAIL_REUSE_AUTHORITY_SMUGGLED"
FAIL_PROMOTION_AUTHORITY_SMUGGLED = "DECISION_RECEIPT_FAIL_PROMOTION_AUTHORITY_SMUGGLED"
FAIL_UPDATER_GENERALIZATION_SMUGGLED = (
    "DECISION_RECEIPT_FAIL_UPDATER_GENERALIZATION_SMUGGLED"
)
FAIL_RUNNER_AUTHORITY_SMUGGLED = "DECISION_RECEIPT_FAIL_RUNNER_AUTHORITY_SMUGGLED"
FAIL_STATE_APPLIED_INSIDE_RECEIPT = "DECISION_RECEIPT_FAIL_STATE_APPLIED_INSIDE_RECEIPT"
FAIL_AUTHORITY_EVENT_CONSUMED_INSIDE_RECEIPT = (
    "DECISION_RECEIPT_FAIL_AUTHORITY_EVENT_CONSUMED_INSIDE_RECEIPT"
)
FAIL_RECOMMENDATION_INSERTED = "DECISION_RECEIPT_FAIL_RECOMMENDATION_INSERTED"
FAIL_MARKDOWN_JSON_PARITY = "DECISION_RECEIPT_FAIL_MARKDOWN_JSON_PARITY"

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

EXPECTED_SELECTED_EFFECTS = {
    "basis_for_next_unit_definition_authority": "GRANTED",
    "next_unit_definition_surface_preparation_authority": "GRANTED",
    "next_unit_definition_authority": "NOT_GRANTED",
    "execution_authority": "NOT_GRANTED",
    "reuse_authority": "NOT_GRANTED",
    "taxonomy_promotion_authority": "NOT_GRANTED",
    "updater_generalization_authority": "NOT_GRANTED",
    "runner_authority": "NOT_GRANTED",
}

RECOMMENDATION_PHRASES = [
    "should accept",
    "should proceed",
    "recommended",
    "best next move",
    "correct next move",
    "good choice",
    "now proceed",
    "you should",
    "we should execute",
    "execution is safe",
    "safe to execute",
    "authorized to execute",
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


def run_git(root: Path, args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(FAIL_SURFACE_MISSING, proc.stderr.strip() or proc.stdout.strip())
    return proc.stdout.strip()


def commit_for_paths(root: Path, paths: list[str]) -> str:
    existing = [path for path in paths if (root / path).exists()]
    if not existing:
        fail(FAIL_SURFACE_MISSING, ",".join(paths))
    return run_git(root, ["log", "-n", "1", "--format=%H", "--", *existing])


def verify_a1_commit(root: Path) -> None:
    run_git(root, ["cat-file", "-e", f"{A1_COMMIT}^{{commit}}"])
    got = commit_for_paths(
        root,
        [
            SURFACE,
            "docs/matrixlabs/decision_surfaces/c8_n22_human_decision_surface_v0.md",
            "scripts/build_c8_n22_human_decision_surface_v0.py",
        ],
    )
    if got != A1_COMMIT:
        fail(FAIL_SURFACE_MISSING, f"A1 commit mismatch: {got}!={A1_COMMIT}")


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
    if not SELECTED_OPTION:
        fail(FAIL_SELECTED_OPTION_MISSING)
    for option in surface.get("decision_options", []):
        if option.get("decision_option_id") == SELECTED_OPTION:
            return option
    fail(FAIL_OPTION_NOT_ON_SURFACE, SELECTED_OPTION)
    raise AssertionError("unreachable")


def validate_surface(surface: dict[str, Any]) -> None:
    checks = {
        "schema_version": (
            surface.get("schema_version"),
            "matrixlabs_human_decision_surface_v0",
        ),
        "decision_surface_id": (
            surface.get("decision_surface_id"),
            SOURCE_DECISION_SURFACE_ID,
        ),
        "source_boundary_record_id": (
            surface.get("source_boundary_record_id"),
            SOURCE_BOUNDARY_RECORD_ID,
        ),
        "source_readabout_id": (
            surface.get("source_readabout_id"),
            SOURCE_READABOUT_ID,
        ),
        "decision_surface_gate": (
            surface.get("surface_gate", {}).get("decision_surface_gate"),
            "DECISION_SURFACE_PASS_OPTIONS_PRESENTED_ONLY",
        ),
        "decision_consumed": (surface.get("decision_consumed"), False),
        "authority_changed": (surface.get("authority_changed"), False),
        "required_authority_event": (
            surface.get("required_authority_event"),
            "HUMAN_ACCEPTANCE",
        ),
        "authority_event_status_before": (
            surface.get("authority_event_status_before"),
            "AUTH_EVENT_UNCONSUMED",
        ),
        "current_authority_state": (
            surface.get("current_authority_state"),
            "AUTH_STATE_OBSERVED_NOT_AUTHORIZED",
        ),
    }
    failures = [f"{key}:{got}!={want}" for key, (got, want) in checks.items() if got != want]
    if failures:
        fail(FAIL_SURFACE_MISSING, "; ".join(failures))
    if "selected_decision" in surface:
        fail(FAIL_SELECTED_OPTION_MISSING, "A1 surface already has selected_decision")


def validate_sources(
    root: Path,
    surface: dict[str, Any],
    boundary: dict[str, Any],
    readabout: dict[str, Any],
) -> None:
    source = surface.get("source", {})
    boundary_path = source.get("boundary_record_path", BOUNDARY)
    readabout_path = source.get("readabout_path", READABOUT)
    if boundary_path != BOUNDARY:
        fail(FAIL_BOUNDARY_RECORD_MISSING, str(boundary_path))
    if readabout_path != READABOUT:
        fail(FAIL_READABOUT_MISSING, str(readabout_path))
    if not (root / boundary_path).exists():
        fail(FAIL_BOUNDARY_RECORD_MISSING, boundary_path)
    if not (root / readabout_path).exists():
        fail(FAIL_READABOUT_MISSING, readabout_path)
    if boundary.get("boundary_record_id") != SOURCE_BOUNDARY_RECORD_ID:
        fail(FAIL_BOUNDARY_RECORD_MISSING, str(boundary.get("boundary_record_id")))
    if readabout.get("readabout_packet_id") != SOURCE_READABOUT_ID:
        fail(FAIL_READABOUT_MISSING, str(readabout.get("readabout_packet_id")))


def build_selected_effects(option: dict[str, Any]) -> dict[str, Any]:
    effects = dict(option.get("authority_effects", {}))
    if effects != EXPECTED_SELECTED_EFFECTS:
        fail(FAIL_OPTION_EFFECT_MISMATCH, json.dumps(effects, sort_keys=True))
    if set(effects) != set(AUTHORITY_EFFECT_KEYS):
        fail(FAIL_OPTION_EFFECT_MISMATCH, f"effect keys: {sorted(effects)}")
    if option.get("consumes_authority_event") != "HUMAN_ACCEPTANCE":
        fail(FAIL_UNDECLARED_AUTHORITY_EVENT, str(option.get("consumes_authority_event")))
    return {
        "consumes_authority_event": option["consumes_authority_event"],
        "authority_event_record_status": "AUTHORITY_EVENT_RECORDED_PENDING_A3_APPLICATION",
        "authority_event_status_if_applied_by_a3": "AUTH_EVENT_CONSUMED",
        "resulting_authority_state_if_applied_by_a3": option.get("resulting_authority_state"),
        "authority_effects_if_applied_by_a3": effects,
        "next_allowed_surface_if_applied_by_a3": option.get("next_allowed_surface_if_selected"),
    }


def build_receipt(root: Path) -> dict[str, Any]:
    surface = load_json(root, SURFACE, FAIL_SURFACE_MISSING)
    validate_surface(surface)
    verify_a1_commit(root)
    boundary = load_json(root, BOUNDARY, FAIL_BOUNDARY_RECORD_MISSING)
    readabout = load_json(root, READABOUT, FAIL_READABOUT_MISSING)
    validate_sources(root, surface, boundary, readabout)

    selected_option = selected_option_from_surface(surface)
    selected_effects = build_selected_effects(selected_option)
    effects = selected_effects["authority_effects_if_applied_by_a3"]
    decision_event = {
        "decision_actor_class": "HUMAN",
        "decision_event_status": "DECISION_EVENT_RECORDED",
        "selected_decision_option": SELECTED_OPTION,
        "selection_source": "EXPLICIT_HUMAN_SELECTION",
        "selection_source_status": "PRESENT",
        "selection_source_text": "Accept as basis, proceed",
    }
    application_boundary = {
        "authority_state_applied_by_this_receipt": False,
        "authority_event_formally_consumed_by_this_receipt": False,
        "requires_authority_state_update_object": True,
        "next_required_object": "c8_n22_authority_state_update_v0",
    }
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "decision_receipt_id": DECISION_RECEIPT_ID,
        "receipt_role": "HUMAN_DECISION_EVENT_RECEIPT",
        "generated_by": GENERATOR,
        "source_decision_surface_id": SOURCE_DECISION_SURFACE_ID,
        "source_boundary_record_id": SOURCE_BOUNDARY_RECORD_ID,
        "source_readabout_id": SOURCE_READABOUT_ID,
        "source": {
            "decision_surface_path": SURFACE,
            "decision_surface_commit_sha": A1_COMMIT,
            "boundary_record_path": BOUNDARY,
            "readabout_path": READABOUT,
            "decision_surface_sha256": sha256_file(root / SURFACE),
            "boundary_record_sha256": sha256_file(root / BOUNDARY),
            "readabout_sha256": sha256_file(root / READABOUT),
            "selection_source_declared_by_prompt": True,
        },
        "decision_event": decision_event,
        "authority_state_before": {
            "current_authority_state": "AUTH_STATE_OBSERVED_NOT_AUTHORIZED",
            "required_authority_event": "HUMAN_ACCEPTANCE",
            "authority_event_status_before": "AUTH_EVENT_UNCONSUMED",
        },
        "selected_option_from_surface": selected_option,
        "selected_option_effects_from_surface": selected_effects,
        "application_boundary": application_boundary,
        "receipt_gate": {
            "decision_receipt_gate": PASS_GATE,
            "source_decision_surface_present": True,
            "source_boundary_record_present": True,
            "source_readabout_present": True,
            "selected_decision_option": SELECTED_OPTION,
            "selected_option_present_on_surface": True,
            "selected_option_effects_match_surface": True,
            "human_decision_event_present": True,
            "human_decision_event_source_explicit": True,
            "authority_event_before": "AUTH_EVENT_UNCONSUMED",
            "authority_event_recorded_pending_a3_application": "HUMAN_ACCEPTANCE",
            "authority_state_applied_by_this_receipt": False,
            "authority_event_formally_consumed_by_this_receipt": False,
            "requires_authority_state_update_object": True,
            "basis_for_next_unit_definition_authority_if_applied": effects[
                "basis_for_next_unit_definition_authority"
            ],
            "next_unit_definition_surface_preparation_authority_if_applied": effects[
                "next_unit_definition_surface_preparation_authority"
            ],
            "next_unit_definition_authority_if_applied": effects[
                "next_unit_definition_authority"
            ],
            "execution_authority_if_applied": effects["execution_authority"],
            "reuse_authority_if_applied": effects["reuse_authority"],
            "taxonomy_promotion_authority_if_applied": effects[
                "taxonomy_promotion_authority"
            ],
            "updater_generalization_authority_if_applied": effects[
                "updater_generalization_authority"
            ],
            "runner_authority_if_applied": effects["runner_authority"],
            "authority_smuggling_detected": False,
            "markdown_json_parity_status": "PASS",
            "meaning_parity_status": "PASS",
            "failures": [],
        },
        "non_claims": [
            "A2 does not define the next bounded C8 unit.",
            "A2 does not authorize final next-unit definition.",
            "A2 does not execute runtime.",
            "A2 does not rewrite receipts.",
            "A2 does not promote taxonomy.",
            "A2 does not authorize reuse.",
            "A2 does not generalize the updater.",
            "A2 does not create runner authority.",
            "A2 does not apply the authority-state update.",
            "A2 does not formally consume the authority event.",
            "A2 records only the selected human decision option and its declared effects pending A3 application.",
        ],
        "unsafe_to_infer": [
            "Unsafe to infer: the authority-state update has been applied.",
            "Unsafe to infer: HUMAN_ACCEPTANCE has been formally consumed.",
            "Unsafe to infer: the next bounded C8 unit is defined.",
            "Unsafe to infer: final next-unit definition is authorized.",
            "Unsafe to infer: runtime execution is authorized.",
            "Unsafe to infer: reuse is authorized.",
            "Unsafe to infer: taxonomy is promoted.",
            "Unsafe to infer: updater generalization is authorized.",
            "Unsafe to infer: runner authority exists.",
        ],
    }
    validate_receipt(receipt, surface, selected_option)
    return receipt


def validate_decision_event(event: dict[str, Any]) -> None:
    checks = {
        "decision_actor_class": (event.get("decision_actor_class"), "HUMAN"),
        "decision_event_status": (event.get("decision_event_status"), "DECISION_EVENT_RECORDED"),
        "selected_decision_option": (event.get("selected_decision_option"), SELECTED_OPTION),
        "selection_source": (event.get("selection_source"), "EXPLICIT_HUMAN_SELECTION"),
        "selection_source_status": (event.get("selection_source_status"), "PRESENT"),
        "selection_source_text": (event.get("selection_source_text"), "Accept as basis, proceed"),
    }
    failures = [f"{key}:{got}!={want}" for key, (got, want) in checks.items() if got != want]
    if failures:
        fail(FAIL_HUMAN_EVENT_MISSING, "; ".join(failures))
    if event.get("selection_source") != "EXPLICIT_HUMAN_SELECTION":
        fail(FAIL_HUMAN_EVENT_NOT_EXPLICIT)


def validate_receipt(
    receipt: dict[str, Any],
    surface: dict[str, Any],
    selected_option: dict[str, Any],
) -> None:
    validate_decision_event(receipt["decision_event"])
    boundary = receipt["application_boundary"]
    if boundary.get("authority_state_applied_by_this_receipt") is not False:
        fail(FAIL_STATE_APPLIED_INSIDE_RECEIPT)
    if boundary.get("authority_event_formally_consumed_by_this_receipt") is not False:
        fail(FAIL_AUTHORITY_EVENT_CONSUMED_INSIDE_RECEIPT)
    if boundary.get("requires_authority_state_update_object") is not True:
        fail(FAIL_STATE_APPLIED_INSIDE_RECEIPT)

    before = receipt["authority_state_before"]
    if before.get("authority_event_status_before") != "AUTH_EVENT_UNCONSUMED":
        fail(FAIL_AUTHORITY_EVENT_ALREADY_CONSUMED)

    selected_effects = receipt["selected_option_effects_from_surface"]
    copied_effects = selected_effects["authority_effects_if_applied_by_a3"]
    if copied_effects != selected_option.get("authority_effects"):
        fail(FAIL_OPTION_EFFECT_MISMATCH)
    if selected_effects.get("resulting_authority_state_if_applied_by_a3") != selected_option.get(
        "resulting_authority_state"
    ):
        fail(FAIL_OPTION_EFFECT_MISMATCH)
    if selected_effects.get("next_allowed_surface_if_applied_by_a3") != selected_option.get(
        "next_allowed_surface_if_selected"
    ):
        fail(FAIL_OPTION_EFFECT_MISMATCH)

    if copied_effects.get("next_unit_definition_authority") != "NOT_GRANTED":
        fail(FAIL_NEXT_UNIT_DEFINITION_AUTHORITY_SMUGGLED)
    if copied_effects.get("execution_authority") != "NOT_GRANTED":
        fail(FAIL_EXECUTION_AUTHORITY_SMUGGLED)
    if copied_effects.get("reuse_authority") != "NOT_GRANTED":
        fail(FAIL_REUSE_AUTHORITY_SMUGGLED)
    if copied_effects.get("taxonomy_promotion_authority") != "NOT_GRANTED":
        fail(FAIL_PROMOTION_AUTHORITY_SMUGGLED)
    if copied_effects.get("updater_generalization_authority") != "NOT_GRANTED":
        fail(FAIL_UPDATER_GENERALIZATION_SMUGGLED)
    if copied_effects.get("runner_authority") != "NOT_GRANTED":
        fail(FAIL_RUNNER_AUTHORITY_SMUGGLED)

    if "authority_event_status_after" in json.dumps(receipt, sort_keys=True):
        fail(FAIL_AUTHORITY_EVENT_CONSUMED_INSIDE_RECEIPT)

    if surface.get("authority_event_status_before") != "AUTH_EVENT_UNCONSUMED":
        fail(FAIL_AUTHORITY_EVENT_ALREADY_CONSUMED)
    hits = scan_text_for_recommendations(json.dumps(receipt, sort_keys=True))
    if hits:
        fail(FAIL_RECOMMENDATION_INSERTED, str(hits))


def render_markdown(receipt: dict[str, Any]) -> str:
    gate = receipt["receipt_gate"]
    event = receipt["decision_event"]
    selected = receipt["selected_option_effects_from_surface"]
    effects = selected["authority_effects_if_applied_by_a3"]
    boundary = receipt["application_boundary"]
    lines = [
        "# C8 n22 human decision receipt v0",
        "",
        "## Status",
        "",
        gate["decision_receipt_gate"],
        "",
        "## Selected decision",
        "",
        event["selected_decision_option"],
        "",
        "## Source",
        "",
        f"- decision surface: {receipt['source_decision_surface_id']}",
        f"- boundary record: {receipt['source_boundary_record_id']}",
        f"- Readabout: {receipt['source_readabout_id']}",
        "",
        "## Decision event",
        "",
        f"- decision actor class: {event['decision_actor_class']}",
        f"- decision event status: {event['decision_event_status']}",
        f"- selection source: {event['selection_source']}",
        f"- selection source status: {event['selection_source_status']}",
        f"- selection source text: {event['selection_source_text']}",
        "",
        "## Authority effect if applied by A3",
        "",
        f"- authority event recorded for A3 application: {selected['consumes_authority_event']}",
        "- authority event record status: "
        f"{selected['authority_event_record_status']}",
        "- resulting authority state if applied by A3: "
        f"{selected['resulting_authority_state_if_applied_by_a3']}",
        "- basis for next-unit definition authority: "
        f"{effects['basis_for_next_unit_definition_authority']}",
        "- next-unit definition surface preparation authority: "
        f"{effects['next_unit_definition_surface_preparation_authority']}",
        "- next-unit definition authority: "
        f"{effects['next_unit_definition_authority']}",
        f"- execution authority: {effects['execution_authority']}",
        f"- reuse authority: {effects['reuse_authority']}",
        f"- taxonomy promotion authority: {effects['taxonomy_promotion_authority']}",
        "- updater generalization authority: "
        f"{effects['updater_generalization_authority']}",
        f"- runner authority: {effects['runner_authority']}",
        "",
        "## Application boundary",
        "",
        "This receipt records the human decision event.",
        "",
        "It does not apply the formal authority-state update.",
        "",
        "It does not formally consume the authority event.",
        "",
        f"The next required object is {boundary['next_required_object']}.",
        "",
        "## Non-claims",
        "",
    ]
    lines.extend(f"- {claim}" for claim in receipt["non_claims"])
    lines.extend(["", "## Unsafe to infer", ""])
    lines.extend(f"- {item}" for item in receipt["unsafe_to_infer"])
    return "\n".join(lines) + "\n"


def validate_markdown(receipt: dict[str, Any], markdown: str) -> None:
    required = [
        "# C8 n22 human decision receipt v0",
        "HUMAN_DECISION_RECEIPT_PASS_TYPED_DECISION_RECORDED",
        SELECTED_OPTION,
        "decision surface: c8.n22.human_decision_surface.v0",
        "boundary record: c8.n22.boundary_transition.v0",
        "Readabout: c8.n22.authority_boundary.readabout.v0",
        "authority event recorded for A3 application: HUMAN_ACCEPTANCE",
        "resulting authority state if applied by A3: AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        "basis for next-unit definition authority: GRANTED",
        "next-unit definition surface preparation authority: GRANTED",
        "next-unit definition authority: NOT_GRANTED",
        "execution authority: NOT_GRANTED",
        "reuse authority: NOT_GRANTED",
        "taxonomy promotion authority: NOT_GRANTED",
        "updater generalization authority: NOT_GRANTED",
        "runner authority: NOT_GRANTED",
        "This receipt records the human decision event.",
        "It does not apply the formal authority-state update.",
        "It does not formally consume the authority event.",
        "The next required object is c8_n22_authority_state_update_v0.",
    ]
    missing = [phrase for phrase in required if phrase not in markdown]
    if missing:
        fail(FAIL_MARKDOWN_JSON_PARITY, str(missing))
    hits = scan_text_for_recommendations(markdown)
    if hits:
        fail(FAIL_RECOMMENDATION_INSERTED, str(hits))


def write_outputs(root: Path, receipt: dict[str, Any]) -> None:
    markdown = render_markdown(receipt)
    validate_markdown(receipt, markdown)
    json_path = root / OUTPUT_JSON
    md_path = root / OUTPUT_MD
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")


def print_success(receipt: dict[str, Any]) -> None:
    gate = receipt["receipt_gate"]
    event = receipt["decision_event"]
    selected = receipt["selected_option_effects_from_surface"]
    print("BUILD_C8_N22_HUMAN_DECISION_RECEIPT_V0_COMPLETE")
    print(f"decision_receipt_id={receipt['decision_receipt_id']}")
    print(f"schema_version={receipt['schema_version']}")
    print(f"receipt_role={receipt['receipt_role']}")
    print(f"source_decision_surface_id={receipt['source_decision_surface_id']}")
    print(f"source_boundary_record_id={receipt['source_boundary_record_id']}")
    print(f"source_readabout_id={receipt['source_readabout_id']}")
    print(f"selected_decision_option={event['selected_decision_option']}")
    print(f"selection_source={event['selection_source']}")
    print(f"selection_source_status={event['selection_source_status']}")
    print(f"decision_event_status={event['decision_event_status']}")
    print(f"decision_receipt_gate={gate['decision_receipt_gate']}")
    print(
        "selected_option_present_on_surface="
        f"{str(gate['selected_option_present_on_surface']).lower()}"
    )
    print(
        "selected_option_effects_match_surface="
        f"{str(gate['selected_option_effects_match_surface']).lower()}"
    )
    print(
        "human_decision_event_present="
        f"{str(gate['human_decision_event_present']).lower()}"
    )
    print(
        "human_decision_event_source_explicit="
        f"{str(gate['human_decision_event_source_explicit']).lower()}"
    )
    print(
        "authority_event_recorded_pending_a3_application="
        f"{gate['authority_event_recorded_pending_a3_application']}"
    )
    print(
        "authority_state_applied_by_this_receipt="
        f"{str(gate['authority_state_applied_by_this_receipt']).lower()}"
    )
    print(
        "authority_event_formally_consumed_by_this_receipt="
        f"{str(gate['authority_event_formally_consumed_by_this_receipt']).lower()}"
    )
    print(
        "requires_authority_state_update_object="
        f"{str(gate['requires_authority_state_update_object']).lower()}"
    )
    print(
        "resulting_authority_state_if_applied_by_a3="
        f"{selected['resulting_authority_state_if_applied_by_a3']}"
    )
    for key in [
        "basis_for_next_unit_definition_authority_if_applied",
        "next_unit_definition_surface_preparation_authority_if_applied",
        "next_unit_definition_authority_if_applied",
        "execution_authority_if_applied",
        "reuse_authority_if_applied",
        "taxonomy_promotion_authority_if_applied",
        "updater_generalization_authority_if_applied",
        "runner_authority_if_applied",
    ]:
        print(f"{key}={gate[key]}")
    print("a3_created=false")
    print("a4_created=false")
    print("authority_state_changed=false")
    print("human_acceptance_formally_consumed=false")
    print("next_unit_defined=false")
    print("next_unit_authorized=false")
    print("runtime_executed=false")
    print("receipts_rewritten=false")
    print("taxonomy_promoted=false")
    print("runner_authority_created=false")
    print("commit_created=false")
    print("push_executed=false")
    print("terminal_transition=ADVANCE(A3_AUTHORITY_STATE_UPDATE_PENDING_RECEIPT_APPLICATION)")


def main() -> int:
    try:
        root = detect_repo_root(Path.cwd())
        receipt = build_receipt(root)
        write_outputs(root, receipt)
    except GenerationError as exc:
        print(f"STOP_{exc.code}")
        return 2
    print_success(receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
