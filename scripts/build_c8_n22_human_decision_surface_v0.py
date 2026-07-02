#!/usr/bin/env python3
"""Build the C8 n22 human decision surface v0.

This surface presents typed human decision options only. It does not record a
selection, consume HUMAN_ACCEPTANCE, change authority state, define a next unit,
or authorize execution.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_human_decision_surface_v0.py"
OUTPUT_JSON = "docs/matrixlabs/decision_surfaces/c8_n22_human_decision_surface_v0.json"
OUTPUT_MD = "docs/matrixlabs/decision_surfaces/c8_n22_human_decision_surface_v0.md"

BOUNDARY = "docs/matrixlabs/boundary/c8_n22_authority_boundary_transition_record_v0.json"
READABOUT = "docs/matrixlabs/readabouts/c8_n22_authority_boundary_readabout_v0.json"

SCHEMA_VERSION = "matrixlabs_human_decision_surface_v0"
DECISION_SURFACE_ID = "c8.n22.human_decision_surface.v0"
SOURCE_BOUNDARY_RECORD_ID = "c8.n22.boundary_transition.v0"
SOURCE_READABOUT_ID = "c8.n22.authority_boundary.readabout.v0"
PASS_GATE = "DECISION_SURFACE_PASS_OPTIONS_PRESENTED_ONLY"

FAIL_SOURCE_BOUNDARY_MISSING = "DECISION_SURFACE_FAIL_SOURCE_BOUNDARY_MISSING"
FAIL_READABOUT_MISSING = "DECISION_SURFACE_FAIL_READABOUT_MISSING"
FAIL_READABOUT_AUTHORITY_COLLAPSE = "DECISION_SURFACE_FAIL_READABOUT_AUTHORITY_COLLAPSE"
FAIL_AUTHORITY_STATE_MISMATCH = "DECISION_SURFACE_FAIL_AUTHORITY_STATE_MISMATCH"
FAIL_REQUIRED_AUTHORITY_EVENT_MISMATCH = "DECISION_SURFACE_FAIL_REQUIRED_AUTHORITY_EVENT_MISMATCH"
FAIL_OPTION_SET_MISMATCH = "DECISION_SURFACE_FAIL_OPTION_SET_MISMATCH"
FAIL_AUTHORITY_EFFECT_MISMATCH = "DECISION_SURFACE_FAIL_AUTHORITY_EFFECT_MISMATCH"
FAIL_DECISION_PRESELECTED = "DECISION_SURFACE_FAIL_DECISION_PRESELECTED"
FAIL_DECISION_CONSUMED = "DECISION_SURFACE_FAIL_DECISION_CONSUMED"
FAIL_AUTHORITY_CHANGED = "DECISION_SURFACE_FAIL_AUTHORITY_CHANGED"
FAIL_RECOMMENDATION_INSERTED = "DECISION_SURFACE_FAIL_RECOMMENDATION_INSERTED"
FAIL_EXECUTION_AUTHORITY_SMUGGLED = "DECISION_SURFACE_FAIL_EXECUTION_AUTHORITY_SMUGGLED"
FAIL_NEXT_UNIT_DEFINITION_SMUGGLED = "DECISION_SURFACE_FAIL_NEXT_UNIT_DEFINITION_SMUGGLED"
FAIL_REUSE_AUTHORITY_SMUGGLED = "DECISION_SURFACE_FAIL_REUSE_AUTHORITY_SMUGGLED"
FAIL_TAXONOMY_PROMOTION_SMUGGLED = "DECISION_SURFACE_FAIL_TAXONOMY_PROMOTION_SMUGGLED"
FAIL_UPDATER_GENERALIZATION_SMUGGLED = "DECISION_SURFACE_FAIL_UPDATER_GENERALIZATION_SMUGGLED"
FAIL_RUNNER_AUTHORITY_SMUGGLED = "DECISION_SURFACE_FAIL_RUNNER_AUTHORITY_SMUGGLED"
FAIL_MARKDOWN_JSON_PARITY = "DECISION_SURFACE_FAIL_MARKDOWN_JSON_PARITY"

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

OPTION_IDS = [
    "DECISION_ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
    "DECISION_ACCEPT_AS_DISCUSSION_SURFACE_ONLY",
    "DECISION_REQUEST_RETYPE_OR_REVISE",
    "DECISION_DEFER",
    "DECISION_REJECT_AS_BASIS",
]

RECOMMENDATION_PHRASES = [
    "should accept",
    "should proceed",
    "recommended",
    "best next move",
    "correct next move",
    "you should",
    "we should execute",
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
        fail(FAIL_SOURCE_BOUNDARY_MISSING, proc.stderr.strip())
    return Path(proc.stdout.strip()).resolve()


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


def authority_effects(**overrides: str) -> dict[str, str]:
    effects = {key: "NOT_GRANTED" for key in AUTHORITY_EFFECT_KEYS}
    effects.update(overrides)
    return effects


def decision_options() -> list[dict[str, Any]]:
    return [
        {
            "decision_option_id": "DECISION_ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
            "option_kind": "AUTHORITY_EVENT_CONSUMING_OPTION",
            "consumes_decision_event": "HUMAN_DECISION",
            "consumes_authority_event": "HUMAN_ACCEPTANCE",
            "resulting_authority_state": "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
            "authority_effects": authority_effects(
                basis_for_next_unit_definition_authority="GRANTED",
                next_unit_definition_surface_preparation_authority="GRANTED",
            ),
            "next_allowed_surface_if_selected": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
            "must_not_impersonate": [
                "NEXT_UNIT_DEFINITION_FINALIZATION",
                "EXECUTION_AUTHORITY",
                "REUSE_AUTHORITY",
                "TAXONOMY_PROMOTION",
                "UPDATER_GENERALIZATION",
                "RUNNER_AUTHORITY",
            ],
        },
        {
            "decision_option_id": "DECISION_ACCEPT_AS_DISCUSSION_SURFACE_ONLY",
            "option_kind": "DECISION_CLASSIFYING_OPTION",
            "consumes_decision_event": "HUMAN_DECISION",
            "consumes_authority_event": "NONE",
            "resulting_authority_state": "AUTH_STATE_DISCUSSION_SURFACE_ONLY",
            "authority_effects": authority_effects(),
            "next_allowed_surface_if_selected": "CONTINUE_DISCUSSION_OR_RETYPE_SURFACE",
            "must_not_impersonate": [
                "ACCEPTED_AS_BASIS",
                "AUTHORITY_ADVANCE",
                "NEXT_UNIT_PREPARATION_AUTHORITY",
                "EXECUTION_AUTHORITY",
            ],
        },
        {
            "decision_option_id": "DECISION_REQUEST_RETYPE_OR_REVISE",
            "option_kind": "NON_AUTHORITY_ADVANCING_OPTION",
            "consumes_decision_event": "HUMAN_DECISION",
            "consumes_authority_event": "NONE",
            "resulting_authority_state": "AUTH_STATE_OBSERVED_NOT_AUTHORIZED",
            "authority_effects": authority_effects(),
            "next_allowed_surface_if_selected": "PREPARE_RETYPE_OR_REVISE_SURFACE",
            "must_not_impersonate": [
                "AUTHORITY_ADVANCE",
                "ACCEPTANCE",
                "REJECTION",
                "EXECUTION_AUTHORITY",
            ],
        },
        {
            "decision_option_id": "DECISION_DEFER",
            "option_kind": "NON_AUTHORITY_CHANGING_OPTION",
            "consumes_decision_event": "HUMAN_DECISION",
            "consumes_authority_event": "NONE",
            "resulting_authority_state": "AUTH_STATE_OBSERVED_NOT_AUTHORIZED",
            "authority_effects": authority_effects(),
            "next_allowed_surface_if_selected": "NONE_DECISION_DEFERRED",
            "must_not_impersonate": [
                "ACCEPTANCE",
                "REJECTION",
                "AUTHORITY_ADVANCE",
                "EXECUTION_AUTHORITY",
            ],
        },
        {
            "decision_option_id": "DECISION_REJECT_AS_BASIS",
            "option_kind": "NON_AUTHORITY_ADVANCING_OPTION",
            "consumes_decision_event": "HUMAN_DECISION",
            "consumes_authority_event": "NONE",
            "resulting_authority_state": "AUTH_STATE_REJECTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
            "authority_effects": authority_effects(),
            "next_allowed_surface_if_selected": "NONE_REJECTED_AS_BASIS",
            "must_not_impersonate": [
                "ACCEPTANCE",
                "AUTHORITY_ADVANCE",
                "RETYPE_REQUEST",
                "EXECUTION_AUTHORITY",
            ],
        },
    ]


def count_grants(options: list[dict[str, Any]], effect_key: str) -> int:
    return sum(
        1
        for option in options
        if option.get("authority_effects", {}).get(effect_key) == "GRANTED"
    )


def scan_text_for_recommendations(text: str) -> list[str]:
    lowered = text.lower()
    return [phrase for phrase in RECOMMENDATION_PHRASES if phrase in lowered]


def validate_sources(boundary: dict[str, Any], readabout: dict[str, Any]) -> None:
    boundary_checks = {
        "schema_version": (
            boundary.get("schema_version"),
            "matrixlabs_authority_boundary_transition_record_v0",
        ),
        "boundary_record_id": (boundary.get("boundary_record_id"), SOURCE_BOUNDARY_RECORD_ID),
        "record_role": (
            boundary.get("record_role"),
            "MACHINE_PRIMARY_AUTHORITY_TRANSITION_RECORD",
        ),
        "human_readout_role": (
            boundary.get("human_readout_role"),
            "DOWNSTREAM_PROJECTION_ONLY",
        ),
    }
    if any(got != want for got, want in boundary_checks.values()):
        fail(FAIL_SOURCE_BOUNDARY_MISSING, str(boundary_checks))

    current = boundary.get("current_authority", {})
    if current.get("current_authority_state") != "AUTH_STATE_OBSERVED_NOT_AUTHORIZED":
        fail(
            FAIL_AUTHORITY_STATE_MISMATCH,
            f"current_authority_state={current.get('current_authority_state')}",
        )
    if current.get("human_acceptance_state") != "AUTH_EVENT_UNCONSUMED":
        fail(
            FAIL_REQUIRED_AUTHORITY_EVENT_MISMATCH,
            f"human_acceptance_state={current.get('human_acceptance_state')}",
        )

    required = boundary.get("required_authority_event", {})
    if required.get("required_event") != "HUMAN_ACCEPTANCE":
        fail(
            FAIL_REQUIRED_AUTHORITY_EVENT_MISMATCH,
            f"required_event={required.get('required_event')}",
        )
    if required.get("required_event_status") != "AUTH_EVENT_UNCONSUMED":
        fail(
            FAIL_REQUIRED_AUTHORITY_EVENT_MISMATCH,
            f"required_event_status={required.get('required_event_status')}",
        )

    transition = boundary.get("proposed_transition", {})
    if transition.get("transition_id") != "ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION":
        fail(
            FAIL_REQUIRED_AUTHORITY_EVENT_MISMATCH,
            f"transition_id={transition.get('transition_id')}",
        )

    readabout_source = readabout.get("source", {})
    readabout_gate = readabout.get("projection_gate", {})
    readabout_checks = {
        "schema_version": (
            readabout.get("schema_version"),
            "matrixlabs_readabout_projection_v0",
        ),
        "readabout_packet_id": (
            readabout.get("readabout_packet_id"),
            SOURCE_READABOUT_ID,
        ),
        "readabout_role": (
            readabout.get("readabout_role"),
            "HUMAN_AUDIT_PROJECTION",
        ),
        "source_of_truth_role": (
            readabout.get("source_of_truth_role"),
            "FORMAL_SOURCE_OBJECT_REMAINS_AUTHORITY",
        ),
        "projection_mode": (
            readabout.get("projection_mode"),
            "FIELD_BACKED_PARITY_PROJECTION",
        ),
        "source_object_id": (
            readabout_source.get("source_object_id"),
            SOURCE_BOUNDARY_RECORD_ID,
        ),
        "source_path": (readabout_source.get("source_path"), BOUNDARY),
        "readabout_gate": (readabout_gate.get("readabout_gate"), "READABOUT_PASS_PARITY"),
        "authority_collapse_detected": (
            readabout_gate.get("authority_collapse_detected"),
            False,
        ),
        "proposal_authority_collapse_detected": (
            readabout_gate.get("proposal_authority_collapse_detected"),
            False,
        ),
    }
    if any(got != want for got, want in readabout_checks.values()):
        fail(FAIL_READABOUT_AUTHORITY_COLLAPSE, str(readabout_checks))


def validate_options(options: list[dict[str, Any]]) -> None:
    ids = [option.get("decision_option_id") for option in options]
    if ids != OPTION_IDS:
        fail(FAIL_OPTION_SET_MISMATCH, f"{ids}!={OPTION_IDS}")

    for option in options:
        missing = [
            key
            for key in [
                "decision_option_id",
                "option_kind",
                "consumes_decision_event",
                "consumes_authority_event",
                "resulting_authority_state",
                "authority_effects",
                "next_allowed_surface_if_selected",
                "must_not_impersonate",
            ]
            if key not in option
        ]
        if missing:
            fail(FAIL_OPTION_SET_MISMATCH, f"{option.get('decision_option_id')}: {missing}")
        if option["consumes_decision_event"] != "HUMAN_DECISION":
            fail(
                FAIL_OPTION_SET_MISMATCH,
                f"{option['decision_option_id']} consumes_decision_event",
            )
        effects = option["authority_effects"]
        if set(effects) != set(AUTHORITY_EFFECT_KEYS):
            fail(FAIL_AUTHORITY_EFFECT_MISMATCH, option["decision_option_id"])
        bad_values = {
            key: value
            for key, value in effects.items()
            if value not in {"GRANTED", "NOT_GRANTED"}
        }
        if bad_values:
            fail(FAIL_AUTHORITY_EFFECT_MISMATCH, str(bad_values))

    expected_effects = {
        "DECISION_ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION": authority_effects(
            basis_for_next_unit_definition_authority="GRANTED",
            next_unit_definition_surface_preparation_authority="GRANTED",
        ),
        "DECISION_ACCEPT_AS_DISCUSSION_SURFACE_ONLY": authority_effects(),
        "DECISION_REQUEST_RETYPE_OR_REVISE": authority_effects(),
        "DECISION_DEFER": authority_effects(),
        "DECISION_REJECT_AS_BASIS": authority_effects(),
    }
    for option in options:
        option_id = option["decision_option_id"]
        if option["authority_effects"] != expected_effects[option_id]:
            fail(FAIL_AUTHORITY_EFFECT_MISMATCH, option_id)

    if count_grants(options, "execution_authority"):
        fail(FAIL_EXECUTION_AUTHORITY_SMUGGLED)
    if count_grants(options, "next_unit_definition_authority"):
        fail(FAIL_NEXT_UNIT_DEFINITION_SMUGGLED)
    if count_grants(options, "reuse_authority"):
        fail(FAIL_REUSE_AUTHORITY_SMUGGLED)
    if count_grants(options, "taxonomy_promotion_authority"):
        fail(FAIL_TAXONOMY_PROMOTION_SMUGGLED)
    if count_grants(options, "updater_generalization_authority"):
        fail(FAIL_UPDATER_GENERALIZATION_SMUGGLED)
    if count_grants(options, "runner_authority"):
        fail(FAIL_RUNNER_AUTHORITY_SMUGGLED)


def build_surface(root: Path) -> dict[str, Any]:
    boundary = load_json(root, BOUNDARY, FAIL_SOURCE_BOUNDARY_MISSING)
    readabout = load_json(root, READABOUT, FAIL_READABOUT_MISSING)
    validate_sources(boundary, readabout)

    options = decision_options()
    validate_options(options)

    surface = {
        "schema_version": SCHEMA_VERSION,
        "decision_surface_id": DECISION_SURFACE_ID,
        "surface_role": "HUMAN_DECISION_SURFACE",
        "generated_by": GENERATOR,
        "source_boundary_record_id": SOURCE_BOUNDARY_RECORD_ID,
        "source_readabout_id": SOURCE_READABOUT_ID,
        "source": {
            "boundary_record_path": BOUNDARY,
            "readabout_path": READABOUT,
            "boundary_record_schema_version": boundary.get("schema_version"),
            "readabout_schema_version": readabout.get("schema_version"),
            "formal_boundary_record_role": boundary.get("record_role"),
            "formal_boundary_record_remains_source_of_truth": True,
            "readabout_role": readabout.get("readabout_role"),
            "readabout_projection_mode": readabout.get("projection_mode"),
            "readabout_is_projection_only": True,
            "source_hashes": {
                "boundary_record_sha256": sha256_file(root / BOUNDARY),
                "readabout_sha256": sha256_file(root / READABOUT),
            },
        },
        "required_authority_event": "HUMAN_ACCEPTANCE",
        "authority_event_status_before": "AUTH_EVENT_UNCONSUMED",
        "current_authority_state": "AUTH_STATE_OBSERVED_NOT_AUTHORIZED",
        "requested_transition": "ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        "surface_status": "PRESENTS_TYPED_OPTIONS_ONLY",
        "decision_consumed": False,
        "authority_changed": False,
        "decision_options": options,
        "surface_gate": {
            "decision_surface_gate": PASS_GATE,
            "decision_option_count": len(options),
            "decision_consumed": False,
            "authority_changed": False,
            "selected_decision_present": False,
            "recommendation_inserted": False,
            "execution_authority_granted_count": count_grants(options, "execution_authority"),
            "next_unit_definition_authority_granted_count": count_grants(
                options, "next_unit_definition_authority"
            ),
            "reuse_authority_granted_count": count_grants(options, "reuse_authority"),
            "taxonomy_promotion_authority_granted_count": count_grants(
                options, "taxonomy_promotion_authority"
            ),
            "updater_generalization_authority_granted_count": count_grants(
                options, "updater_generalization_authority"
            ),
            "runner_authority_granted_count": count_grants(options, "runner_authority"),
            "markdown_json_parity_status": "PASS",
            "meaning_parity_status": "PASS",
            "failures": [],
        },
        "non_claims": [
            "This decision surface does not record a decision.",
            "This decision surface does not consume HUMAN_ACCEPTANCE.",
            "This decision surface does not change authority state.",
            "The formal boundary record remains source of truth.",
            "The Readabout remains downstream projection only.",
            "Accept-as-basis authorizes only preparation of the next bounded unit definition surface.",
            "This decision surface does not define the next bounded unit.",
            "This decision surface does not finalize the next bounded unit.",
            "Execution remains NOT_GRANTED.",
            "Reuse remains NOT_GRANTED.",
            "Taxonomy promotion remains NOT_GRANTED.",
            "Updater generalization remains NOT_GRANTED.",
            "Runner authority remains NOT_GRANTED.",
        ],
        "unsafe_to_infer": [
            "Unsafe to infer: a decision has been selected.",
            "Unsafe to infer: HUMAN_ACCEPTANCE has been consumed.",
            "Unsafe to infer: authority state has changed.",
            "Unsafe to infer: the next bounded unit is defined.",
            "Unsafe to infer: the next bounded unit is authorized.",
            "Unsafe to infer: execution is authorized.",
            "Unsafe to infer: reuse is authorized.",
            "Unsafe to infer: taxonomy has been promoted.",
            "Unsafe to infer: updater generalization is authorized.",
            "Unsafe to infer: runner authority exists.",
        ],
    }
    validate_surface(surface)
    return surface


def validate_surface(surface: dict[str, Any]) -> None:
    if "selected_decision" in surface:
        fail(FAIL_DECISION_PRESELECTED)
    if surface.get("decision_consumed") is not False:
        fail(FAIL_DECISION_CONSUMED)
    if surface.get("authority_changed") is not False:
        fail(FAIL_AUTHORITY_CHANGED)
    if surface.get("current_authority_state") != "AUTH_STATE_OBSERVED_NOT_AUTHORIZED":
        fail(FAIL_AUTHORITY_STATE_MISMATCH)
    if surface.get("required_authority_event") != "HUMAN_ACCEPTANCE":
        fail(FAIL_REQUIRED_AUTHORITY_EVENT_MISMATCH)
    if surface.get("authority_event_status_before") != "AUTH_EVENT_UNCONSUMED":
        fail(FAIL_REQUIRED_AUTHORITY_EVENT_MISMATCH)

    gate = surface["surface_gate"]
    if gate["decision_option_count"] != 5:
        fail(FAIL_OPTION_SET_MISMATCH)
    if gate["decision_consumed"] is not False:
        fail(FAIL_DECISION_CONSUMED)
    if gate["authority_changed"] is not False:
        fail(FAIL_AUTHORITY_CHANGED)
    if gate["selected_decision_present"] is not False:
        fail(FAIL_DECISION_PRESELECTED)
    if gate["recommendation_inserted"] is not False:
        fail(FAIL_RECOMMENDATION_INSERTED)
    if gate["execution_authority_granted_count"]:
        fail(FAIL_EXECUTION_AUTHORITY_SMUGGLED)
    if gate["next_unit_definition_authority_granted_count"]:
        fail(FAIL_NEXT_UNIT_DEFINITION_SMUGGLED)
    if gate["reuse_authority_granted_count"]:
        fail(FAIL_REUSE_AUTHORITY_SMUGGLED)
    if gate["taxonomy_promotion_authority_granted_count"]:
        fail(FAIL_TAXONOMY_PROMOTION_SMUGGLED)
    if gate["updater_generalization_authority_granted_count"]:
        fail(FAIL_UPDATER_GENERALIZATION_SMUGGLED)
    if gate["runner_authority_granted_count"]:
        fail(FAIL_RUNNER_AUTHORITY_SMUGGLED)

    validate_options(surface["decision_options"])
    text = json.dumps(surface, sort_keys=True)
    hits = scan_text_for_recommendations(text)
    if hits:
        fail(FAIL_RECOMMENDATION_INSERTED, str(hits))


def render_markdown(surface: dict[str, Any]) -> str:
    lines = [
        "# C8 n22 human decision surface v0",
        "",
        "## Surface",
        "",
        "This is a human decision surface.",
        "",
        "It presents options only.",
        "",
        "It does not record a decision.",
        "",
        "It does not consume HUMAN_ACCEPTANCE.",
        "",
        "It does not change authority state.",
        "",
        "The formal boundary record remains source of truth.",
        "",
        "The Readabout remains downstream projection only.",
        "",
        "## Source authority and projection boundary",
        "",
        "- Formal source role: FORMAL_SOURCE_OBJECT_REMAINS_AUTHORITY.",
        "- READABOUT role: downstream human-audit projection only.",
        "- This decision surface presents typed options only; it does not consume HUMAN_ACCEPTANCE and does not change authority state.",
        "",
        "Accept-as-basis authorizes only preparation of the next bounded unit definition surface.",
        "",
        "Its typed effects grant basis-for-next-unit-definition authority and preparation authority only; final next-unit-definition authority remains NOT_GRANTED.",
        "",
        "Execution remains NOT_GRANTED.",
        "",
        "Reuse remains NOT_GRANTED.",
        "",
        "Taxonomy promotion remains NOT_GRANTED.",
        "",
        "Updater generalization remains NOT_GRANTED.",
        "",
        "Runner authority remains NOT_GRANTED.",
        "",
        "## Identity",
        "",
        f"- decision_surface_id = {surface['decision_surface_id']}",
        f"- schema_version = {surface['schema_version']}",
        f"- surface_role = {surface['surface_role']}",
        f"- source_boundary_record_id = {surface['source_boundary_record_id']}",
        f"- source_readabout_id = {surface['source_readabout_id']}",
        f"- required_authority_event = {surface['required_authority_event']}",
        f"- authority_event_status_before = {surface['authority_event_status_before']}",
        f"- current_authority_state = {surface['current_authority_state']}",
        f"- requested_transition = {surface['requested_transition']}",
        f"- surface_status = {surface['surface_status']}",
        f"- decision_consumed = {str(surface['decision_consumed']).lower()}",
        f"- authority_changed = {str(surface['authority_changed']).lower()}",
        "",
        "## Options",
        "",
    ]
    for option in surface["decision_options"]:
        lines.extend(
            [
                f"### {option['decision_option_id']}",
                "",
                f"- option_kind = {option['option_kind']}",
                f"- consumes_decision_event = {option['consumes_decision_event']}",
                f"- consumes_authority_event = {option['consumes_authority_event']}",
                f"- resulting_authority_state = {option['resulting_authority_state']}",
                f"- next_allowed_surface_if_selected = {option['next_allowed_surface_if_selected']}",
                "",
                "Authority effects:",
            ]
        )
        for key in AUTHORITY_EFFECT_KEYS:
            lines.append(f"- {key} = {option['authority_effects'][key]}")
        lines.extend(["", "Must not impersonate:"])
        for item in option["must_not_impersonate"]:
            lines.append(f"- {item}")
        lines.append("")

    gate = surface["surface_gate"]
    lines.extend(
        [
            "## Surface gate",
            "",
            f"decision_surface_gate = {gate['decision_surface_gate']}",
            f"decision_option_count = {gate['decision_option_count']}",
            f"decision_consumed = {str(gate['decision_consumed']).lower()}",
            f"authority_changed = {str(gate['authority_changed']).lower()}",
            f"selected_decision_present = {str(gate['selected_decision_present']).lower()}",
            f"recommendation_inserted = {str(gate['recommendation_inserted']).lower()}",
            f"execution_authority_granted_count = {gate['execution_authority_granted_count']}",
            f"next_unit_definition_authority_granted_count = {gate['next_unit_definition_authority_granted_count']}",
            f"reuse_authority_granted_count = {gate['reuse_authority_granted_count']}",
            f"taxonomy_promotion_authority_granted_count = {gate['taxonomy_promotion_authority_granted_count']}",
            f"updater_generalization_authority_granted_count = {gate['updater_generalization_authority_granted_count']}",
            f"runner_authority_granted_count = {gate['runner_authority_granted_count']}",
            f"markdown_json_parity_status = {gate['markdown_json_parity_status']}",
            f"meaning_parity_status = {gate['meaning_parity_status']}",
            "",
            "## Non-claims",
            "",
        ]
    )
    lines.extend(f"- {claim}" for claim in surface["non_claims"])
    lines.extend(["", "## Unsafe to infer", ""])
    lines.extend(f"- {item}" for item in surface["unsafe_to_infer"])
    return "\n".join(lines) + "\n"


def validate_markdown(surface: dict[str, Any], markdown: str) -> None:
    required_phrases = [
        "This is a human decision surface.",
        "It presents options only.",
        "It does not record a decision.",
        "It does not consume HUMAN_ACCEPTANCE.",
        "It does not change authority state.",
        "The formal boundary record remains source of truth.",
        "The Readabout remains downstream projection only.",
        "FORMAL_SOURCE_OBJECT_REMAINS_AUTHORITY",
        "READABOUT",
        "Accept-as-basis authorizes only preparation of the next bounded unit definition surface.",
        "Execution remains NOT_GRANTED.",
        "Reuse remains NOT_GRANTED.",
        "Taxonomy promotion remains NOT_GRANTED.",
        "Updater generalization remains NOT_GRANTED.",
        "Runner authority remains NOT_GRANTED.",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in markdown]
    if missing:
        fail(FAIL_MARKDOWN_JSON_PARITY, f"missing phrases: {missing}")

    for option in surface["decision_options"]:
        option_id = option["decision_option_id"]
        if option_id not in markdown:
            fail(FAIL_MARKDOWN_JSON_PARITY, f"missing option: {option_id}")
        for key in AUTHORITY_EFFECT_KEYS:
            rendered = f"{key} = {option['authority_effects'][key]}"
            if rendered not in markdown:
                fail(FAIL_MARKDOWN_JSON_PARITY, f"missing effect: {rendered}")

    gate = surface["surface_gate"]
    for key in ["decision_surface_gate", "markdown_json_parity_status", "meaning_parity_status"]:
        rendered = f"{key} = {gate[key]}"
        if rendered not in markdown:
            fail(FAIL_MARKDOWN_JSON_PARITY, f"missing gate: {rendered}")

    hits = scan_text_for_recommendations(markdown)
    if hits:
        fail(FAIL_RECOMMENDATION_INSERTED, str(hits))


def write_outputs(root: Path, surface: dict[str, Any]) -> None:
    markdown = render_markdown(surface)
    validate_markdown(surface, markdown)

    json_path = root / OUTPUT_JSON
    md_path = root / OUTPUT_MD
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(surface, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")


def print_success(surface: dict[str, Any]) -> None:
    options = {
        option["decision_option_id"]: option for option in surface["decision_options"]
    }
    accept_effects = options[
        "DECISION_ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION"
    ]["authority_effects"]
    gate = surface["surface_gate"]
    print("BUILD_C8_N22_HUMAN_DECISION_SURFACE_V0_COMPLETE")
    print(f"decision_surface_id={surface['decision_surface_id']}")
    print(f"schema_version={surface['schema_version']}")
    print(f"surface_role={surface['surface_role']}")
    print(f"source_boundary_record_id={surface['source_boundary_record_id']}")
    print(f"source_readabout_id={surface['source_readabout_id']}")
    print(f"decision_surface_gate={gate['decision_surface_gate']}")
    print(f"decision_option_count={gate['decision_option_count']}")
    print(f"decision_consumed={str(surface['decision_consumed']).lower()}")
    print(f"authority_changed={str(surface['authority_changed']).lower()}")
    print(f"selected_decision_present={str(gate['selected_decision_present']).lower()}")
    print(f"required_authority_event={surface['required_authority_event']}")
    print(f"authority_event_status_before={surface['authority_event_status_before']}")
    print(f"current_authority_state={surface['current_authority_state']}")
    print(
        "accept_as_basis_next_allowed_surface="
        f"{options['DECISION_ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION']['next_allowed_surface_if_selected']}"
    )
    for key in AUTHORITY_EFFECT_KEYS:
        print(f"{key}={accept_effects[key]}")
    print(f"markdown_json_parity_status={gate['markdown_json_parity_status']}")
    print(f"meaning_parity_status={gate['meaning_parity_status']}")
    print("a2_created=false")
    print("a3_created=false")
    print("a4_created=false")
    print("human_acceptance_consumed=false")
    print("next_unit_defined=false")
    print("next_unit_authorized=false")
    print("runtime_executed=false")
    print("taxonomy_promoted=false")
    print("runner_authority_created=false")
    print("ADVANCE(A2_HUMAN_DECISION_RECEIPT_SURFACE_PENDING_HUMAN_SELECTION)")


def main() -> int:
    try:
        root = detect_repo_root(Path.cwd())
        surface = build_surface(root)
        write_outputs(root, surface)
    except GenerationError as exc:
        print(f"STOP_{exc.code}")
        return 2
    print_success(surface)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
