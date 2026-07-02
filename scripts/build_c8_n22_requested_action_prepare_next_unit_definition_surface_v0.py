#!/usr/bin/env python3
"""Build the C8 n22 requested-action record v0.

This declares one router input request for later classification. It does not
classify, approve, authorize, prepare, or execute the requested action.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_requested_action_prepare_next_unit_definition_surface_v0.py"
OUTPUT_JSON = "docs/matrixlabs/router/c8_n22_requested_action_prepare_next_unit_definition_surface_v0.json"
OUTPUT_MD = "docs/matrixlabs/router/c8_n22_requested_action_prepare_next_unit_definition_surface_v0.md"

CLOSURE = "docs/matrixlabs/boundary/c8_n22_authority_transition_closure_v0.json"
UPDATE = "docs/matrixlabs/boundary/c8_n22_authority_state_update_v0.json"

A4_COMMIT = "7e8a1b5594f3ee725d0393ab27433b7650ec489d"
A3_COMMIT = "d8a5116ec1be3756b1ad0aa6656187c91c71e87f"

SCHEMA_VERSION = "matrixlabs_requested_action_record_v0"
REQUESTED_ACTION_RECORD_ID = "c8.n22.request.prepare_next_bounded_unit_definition_surface.v0"
RECORD_ROLE = "ROUTER_INPUT_REQUESTED_ACTION"
REQUEST_STATUS = "REQUEST_DECLARED_FOR_CLASSIFICATION_ONLY"
REQUESTED_ACTION = "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"
REQUESTED_ACTION_SCOPE = "PREPARE_SURFACE_ONLY"
REQUESTED_OUTPUT_KIND = "NEXT_BOUNDED_UNIT_DEFINITION_SURFACE"
REQUESTED_TARGET_BASIS = "c8.n22"
BASIS_SCOPE = "C8_N22_BASIS_ONLY"
PASS_GATE = "REQUESTED_ACTION_PASS_DECLARED_ONLY"

FAIL_AUTHORITY_UPDATE_MISSING = "REQUEST_FAIL_AUTHORITY_UPDATE_MISSING"
FAIL_AUTHORITY_TRANSITION_CLOSURE_MISSING = "REQUEST_FAIL_AUTHORITY_TRANSITION_CLOSURE_MISSING"
FAIL_SOURCE_AUTHORITY_MISSING = "REQUEST_FAIL_SOURCE_AUTHORITY_MISSING"
FAIL_ACTION_MISSING = "REQUEST_FAIL_ACTION_MISSING"
FAIL_ACTION_UNTYPED = "REQUEST_FAIL_ACTION_UNTYPED"
FAIL_SCOPE_MISSING = "REQUEST_FAIL_SCOPE_MISSING"
FAIL_SCOPE_TOO_BROAD = "REQUEST_FAIL_SCOPE_TOO_BROAD"
FAIL_TARGET_BASIS_MISSING = "REQUEST_FAIL_TARGET_BASIS_MISSING"
FAIL_ACTION_EXECUTED = "REQUEST_FAIL_ACTION_EXECUTED"
FAIL_AUTHORITY_CHANGED = "REQUEST_FAIL_AUTHORITY_CHANGED"
FAIL_ROUTE_CLASSIFICATION_EMITTED = "REQUEST_FAIL_ROUTE_CLASSIFICATION_EMITTED"
FAIL_REQUESTED_OUTPUT_CREATED = "REQUEST_FAIL_REQUESTED_OUTPUT_CREATED"
FAIL_NEXT_UNIT_FINALIZATION_SMUGGLED = "REQUEST_FAIL_NEXT_UNIT_FINALIZATION_SMUGGLED"
FAIL_NEXT_UNIT_AUTHORIZATION_SMUGGLED = "REQUEST_FAIL_NEXT_UNIT_AUTHORIZATION_SMUGGLED"
FAIL_EXECUTION_SMUGGLED = "REQUEST_FAIL_EXECUTION_SMUGGLED"
FAIL_REUSE_SMUGGLED = "REQUEST_FAIL_REUSE_SMUGGLED"
FAIL_PROMOTION_SMUGGLED = "REQUEST_FAIL_PROMOTION_SMUGGLED"
FAIL_UPDATER_GENERALIZATION_SMUGGLED = "REQUEST_FAIL_UPDATER_GENERALIZATION_SMUGGLED"
FAIL_RUNNER_SMUGGLED = "REQUEST_FAIL_RUNNER_SMUGGLED"
FAIL_OBSERVED_PATH_UPDATE_SMUGGLED = "REQUEST_FAIL_OBSERVED_PATH_UPDATE_SMUGGLED"
FAIL_RECOMMENDATION_INSERTED = "REQUEST_FAIL_RECOMMENDATION_INSERTED"
FAIL_MARKDOWN_JSON_PARITY = "REQUEST_FAIL_MARKDOWN_JSON_PARITY"

ALLOWED_ACTIONS = {
    "PREPARE_HUMAN_DECISION_SURFACE",
    "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
    "PREPARE_RETYPE_OR_REVISION_SURFACE",
    "PREPARE_DISCUSSION_OR_REVIEW_SURFACE",
    "CLASSIFY_ONLY",
}

ALLOWED_SCOPES = {
    "PREPARE_SURFACE_ONLY",
    "CLASSIFY_ONLY",
    "APPLY_AUTHORITY_TRANSITION",
    "EXECUTE_UNIT",
    "PROMOTE_SCHEMA",
    "AUTHORIZE_REUSE",
    "ACTIVATE_RUNNER",
}

FORBIDDEN_REQUEST_NAMES = {
    "CONTINUE",
    "PROCEED",
    "GO",
    "NEXT",
    "DO_NEXT",
    "ADVANCE_C8",
    "RUN_NEXT",
    "BUILD_NEXT",
    "DEFINE_NEXT_UNIT",
    "EXECUTE_NEXT_UNIT",
}

STILL_NOT_AUTHORIZED = [
    "NEXT_UNIT_DEFINITION_FINALIZATION",
    "NEXT_UNIT_DEFINITION_AUTHORITY",
    "EXECUTION",
    "REUSE",
    "TAXONOMY_PROMOTION",
    "UPDATER_GENERALIZATION",
    "RUNNER_AUTHORITY",
    "RECEIPT_REWRITE",
    "OBSERVED_PATH_UPDATE",
]

CLAIMED_NON_EFFECTS = {
    "does_not_execute_unit": True,
    "does_not_apply_authority_transition": True,
    "does_not_rewrite_receipts": True,
    "does_not_promote_taxonomy": True,
    "does_not_authorize_reuse": True,
    "does_not_generalize_updater": True,
    "does_not_activate_runner": True,
    "does_not_define_next_unit_as_final": True,
    "does_not_authorize_next_unit": True,
    "does_not_change_authority_state": True,
    "does_not_update_observed_path": True,
}

RECOMMENDATION_PHRASES = [
    "should proceed",
    "recommended",
    "best next move",
    "correct next move",
    "good choice",
    "now proceed",
    "request approved",
    "classification passed",
    "safe to execute",
    "execution is safe",
    "next unit is defined",
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
        fail(FAIL_SOURCE_AUTHORITY_MISSING, proc.stderr.strip())
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
    run_git(root, ["cat-file", "-e", f"{A4_COMMIT}^{{commit}}"], FAIL_AUTHORITY_TRANSITION_CLOSURE_MISSING)
    run_git(root, ["cat-file", "-e", f"{A3_COMMIT}^{{commit}}"], FAIL_AUTHORITY_UPDATE_MISSING)
    a4_got = commit_for_paths(
        root,
        [
            CLOSURE,
            "docs/matrixlabs/boundary/c8_n22_authority_transition_closure_v0.md",
            "scripts/build_c8_n22_authority_transition_closure_v0.py",
        ],
        FAIL_AUTHORITY_TRANSITION_CLOSURE_MISSING,
    )
    if a4_got != A4_COMMIT:
        fail(FAIL_AUTHORITY_TRANSITION_CLOSURE_MISSING, f"A4 commit mismatch: {a4_got}!={A4_COMMIT}")
    a3_got = commit_for_paths(
        root,
        [
            UPDATE,
            "docs/matrixlabs/boundary/c8_n22_authority_state_update_v0.md",
            "scripts/build_c8_n22_authority_state_update_v0.py",
        ],
        FAIL_AUTHORITY_UPDATE_MISSING,
    )
    if a3_got != A3_COMMIT:
        fail(FAIL_AUTHORITY_UPDATE_MISSING, f"A3 commit mismatch: {a3_got}!={A3_COMMIT}")


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


def validate_sources(closure: dict[str, Any], update: dict[str, Any]) -> None:
    if closure.get("closure_id") != "c8.n22.authority_transition_closure.v0":
        fail(FAIL_AUTHORITY_TRANSITION_CLOSURE_MISSING)
    if closure.get("closure_gate", {}).get("closure_status") != "AUTHORITY_TRANSITION_CLOSURE_PASS":
        fail(FAIL_SOURCE_AUTHORITY_MISSING, "closure_status")
    if closure.get("block", {}).get("block_status") != "BLOCK_A_PASS_AUTHORITY_ADVANCED_TO_BASIS":
        fail(FAIL_SOURCE_AUTHORITY_MISSING, "block_status")
    if update.get("authority_update_id") != "c8.n22.authority_state_update.v0":
        fail(FAIL_AUTHORITY_UPDATE_MISSING)
    if update.get("update_gate", {}).get("authority_state_update_gate") != "AUTHORITY_UPDATE_PASS_DECISION_APPLIED":
        fail(FAIL_SOURCE_AUTHORITY_MISSING, "authority_update_gate")

    closure_surface = closure.get("next_lawful_surface", {})
    update_router = update.get("next_router_state", {})
    if closure.get("authority_transition_summary", {}).get("resulting_authority_state") != (
        "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION"
    ):
        fail(FAIL_SOURCE_AUTHORITY_MISSING, "closure resulting state")
    if update.get("authority_state_after", {}).get("new_authority_state") != (
        "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION"
    ):
        fail(FAIL_SOURCE_AUTHORITY_MISSING, "update resulting state")
    if closure_surface.get("router_action") != REQUESTED_ACTION:
        fail(FAIL_SOURCE_AUTHORITY_MISSING, "closure router action")
    if update_router.get("next_allowed_router_action") != REQUESTED_ACTION:
        fail(FAIL_SOURCE_AUTHORITY_MISSING, "update router action")
    if closure_surface.get("machine_permitted_action_scope") != "PREPARE_NEXT_UNIT_DEFINITION_SURFACE_ONLY":
        fail(FAIL_SOURCE_AUTHORITY_MISSING, "closure machine scope")
    if update_router.get("machine_permitted_action_scope") != "PREPARE_NEXT_UNIT_DEFINITION_SURFACE_ONLY":
        fail(FAIL_SOURCE_AUTHORITY_MISSING, "update machine scope")


def validate_request_enums() -> None:
    if REQUESTED_ACTION in FORBIDDEN_REQUEST_NAMES:
        fail(FAIL_ACTION_UNTYPED, REQUESTED_ACTION)
    if REQUESTED_ACTION not in ALLOWED_ACTIONS:
        fail(FAIL_ACTION_UNTYPED, REQUESTED_ACTION)
    if not REQUESTED_ACTION:
        fail(FAIL_ACTION_MISSING)
    if REQUESTED_ACTION_SCOPE not in ALLOWED_SCOPES:
        fail(FAIL_SCOPE_MISSING, REQUESTED_ACTION_SCOPE)
    if REQUESTED_ACTION_SCOPE != "PREPARE_SURFACE_ONLY":
        fail(FAIL_SCOPE_TOO_BROAD, REQUESTED_ACTION_SCOPE)
    if REQUESTED_TARGET_BASIS != "c8.n22":
        fail(FAIL_TARGET_BASIS_MISSING, REQUESTED_TARGET_BASIS)


def validate_no_forbidden_files(root: Path) -> None:
    forbidden = [
        "docs/matrixlabs/router/c8_n22_route_classification_v0.json",
        "docs/matrixlabs/router/c8_n22_route_classification_v0.md",
        "scripts/build_c8_n22_route_classification_v0.py",
        "docs/matrixlabs/router/c8_n22_router_closure_v0.json",
        "scripts/build_c8_n22_router_closure_v0.py",
        "docs/matrixlabs/next_units/c8_n22_next_bounded_unit_v0.json",
        "docs/matrixlabs/next_units/c8_n22_next_bounded_unit_v0.md",
        "docs/matrixlabs/observability/c8_observed_decision_path_update_b1_proposal_v0.json",
        "docs/matrixlabs/observability/c8_observed_path_update_b1_apply_v0.json",
    ]
    existing = [path for path in forbidden if (root / path).exists()]
    if existing:
        fail(FAIL_REQUESTED_OUTPUT_CREATED, str(existing))


def build_record(root: Path) -> dict[str, Any]:
    verify_expected_commits(root)
    validate_no_forbidden_files(root)
    closure = load_json(root, CLOSURE, FAIL_AUTHORITY_TRANSITION_CLOSURE_MISSING)
    update = load_json(root, UPDATE, FAIL_AUTHORITY_UPDATE_MISSING)
    validate_sources(closure, update)
    validate_request_enums()

    source_authority = {
        "authority_transition_closure_id": "c8.n22.authority_transition_closure.v0",
        "authority_update_id": "c8.n22.authority_state_update.v0",
        "source_object_id": "c8.n22",
        "current_authority_state": "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        "basis_scope": BASIS_SCOPE,
        "next_lawful_surface_from_closure": closure["next_lawful_surface"]["router_action"],
        "next_allowed_router_action_from_authority_update": update["next_router_state"][
            "next_allowed_router_action"
        ],
        "machine_permitted_action_scope_from_closure": closure["next_lawful_surface"][
            "machine_permitted_action_scope"
        ],
        "still_not_authorized": list(STILL_NOT_AUTHORIZED),
    }
    requested_movement = {
        "requested_action": REQUESTED_ACTION,
        "requested_action_scope": REQUESTED_ACTION_SCOPE,
        "requested_output_kind": REQUESTED_OUTPUT_KIND,
        "requested_target_basis": REQUESTED_TARGET_BASIS,
        "basis_scope": BASIS_SCOPE,
        "request_matches_next_lawful_surface_from_closure": True,
        "request_matches_authority_update_next_router_action": True,
    }
    classification_target = {
        "target_router": "READ_ONLY_AUTHORITY_ROUTER",
        "classification_question": "CLASSIFY_DECLARED_REQUEST_AGAINST_CURRENT_AUTHORITY_STATE",
        "router_must_not_execute": True,
        "router_must_not_change_authority": True,
        "router_must_not_prepare_requested_output": True,
    }
    record = {
        "schema_version": SCHEMA_VERSION,
        "requested_action_record_id": REQUESTED_ACTION_RECORD_ID,
        "record_role": RECORD_ROLE,
        "generated_by": GENERATOR,
        "request_status": REQUEST_STATUS,
        "source": {
            "authority_transition_closure_path": CLOSURE,
            "authority_transition_closure_commit_sha": A4_COMMIT,
            "authority_update_path": UPDATE,
            "authority_update_commit_sha": A3_COMMIT,
            "authority_transition_closure_sha256": sha256_file(root / CLOSURE),
            "authority_update_sha256": sha256_file(root / UPDATE),
        },
        "source_authority": source_authority,
        "requested_movement": requested_movement,
        "claimed_non_effects": dict(CLAIMED_NON_EFFECTS),
        "classification_target": classification_target,
        "request_gate": {
            "requested_action_gate": PASS_GATE,
            "requested_action_record_id": REQUESTED_ACTION_RECORD_ID,
            "source_authority_state_present": True,
            "source_authority_state": source_authority["current_authority_state"],
            "requested_action": REQUESTED_ACTION,
            "requested_action_scope": REQUESTED_ACTION_SCOPE,
            "requested_output_kind": REQUESTED_OUTPUT_KIND,
            "requested_target_basis": REQUESTED_TARGET_BASIS,
            "basis_scope": BASIS_SCOPE,
            "request_status": REQUEST_STATUS,
            "requested_action_typed": True,
            "requested_action_scope_typed": True,
            "request_source_chain_present": True,
            "requested_action_executed": False,
            "authority_changed": False,
            "route_classification_emitted": False,
            "requested_output_created": False,
            **dict(CLAIMED_NON_EFFECTS),
            "failures": [],
        },
        "non_claims": [
            "B.1 does not classify the request.",
            "B.1 does not approve the request.",
            "B.1 does not authorize the request.",
            "B.1 does not perform the request.",
            "B.1 does not prepare the next unit definition surface.",
            "B.1 does not define the next bounded unit.",
            "B.1 does not finalize the next bounded unit definition.",
            "B.1 does not authorize the next bounded unit.",
            "B.1 does not change authority state.",
            "B.1 does not execute runtime.",
            "B.1 does not update the observed path.",
            "B.1 does not promote taxonomy.",
            "B.1 does not authorize reuse.",
            "B.1 does not generalize updater.",
            "B.1 does not create runner authority.",
            "B.1 only declares the requested action for B.2 routing.",
        ],
        "unsafe_to_infer": [
            "Unsafe to infer: the request has been classified.",
            "Unsafe to infer: the request has been approved.",
            "Unsafe to infer: the request has been authorized.",
            "Unsafe to infer: the requested output has been created.",
            "Unsafe to infer: the next bounded unit has been defined.",
            "Unsafe to infer: the next bounded unit has been authorized.",
            "Unsafe to infer: runtime execution is authorized.",
            "Unsafe to infer: the observed path has been updated.",
        ],
    }
    validate_record(record)
    return record


def validate_record(record: dict[str, Any]) -> None:
    gate = record["request_gate"]
    if gate.get("requested_action_gate") != PASS_GATE:
        fail(FAIL_ACTION_MISSING)
    if gate.get("requested_action_executed") is not False:
        fail(FAIL_ACTION_EXECUTED)
    if gate.get("authority_changed") is not False:
        fail(FAIL_AUTHORITY_CHANGED)
    if gate.get("route_classification_emitted") is not False:
        fail(FAIL_ROUTE_CLASSIFICATION_EMITTED)
    if gate.get("requested_output_created") is not False:
        fail(FAIL_REQUESTED_OUTPUT_CREATED)
    if gate.get("failures") != []:
        fail(FAIL_ACTION_MISSING)
    if "expected_route_family" in record.get("classification_target", {}):
        fail(FAIL_ROUTE_CLASSIFICATION_EMITTED)
    if "route_disposition" in json.dumps(record, sort_keys=True):
        fail(FAIL_ROUTE_CLASSIFICATION_EMITTED)
    if "ROUTE_" in json.dumps(record, sort_keys=True):
        fail(FAIL_ROUTE_CLASSIFICATION_EMITTED)
    for key, value in record["claimed_non_effects"].items():
        if value is not True:
            fail(FAIL_ACTION_EXECUTED, key)
    if not record["claimed_non_effects"]["does_not_define_next_unit_as_final"]:
        fail(FAIL_NEXT_UNIT_FINALIZATION_SMUGGLED)
    if not record["claimed_non_effects"]["does_not_authorize_next_unit"]:
        fail(FAIL_NEXT_UNIT_AUTHORIZATION_SMUGGLED)
    if not record["claimed_non_effects"]["does_not_execute_unit"]:
        fail(FAIL_EXECUTION_SMUGGLED)
    if not record["claimed_non_effects"]["does_not_authorize_reuse"]:
        fail(FAIL_REUSE_SMUGGLED)
    if not record["claimed_non_effects"]["does_not_promote_taxonomy"]:
        fail(FAIL_PROMOTION_SMUGGLED)
    if not record["claimed_non_effects"]["does_not_generalize_updater"]:
        fail(FAIL_UPDATER_GENERALIZATION_SMUGGLED)
    if not record["claimed_non_effects"]["does_not_activate_runner"]:
        fail(FAIL_RUNNER_SMUGGLED)
    if not record["claimed_non_effects"]["does_not_update_observed_path"]:
        fail(FAIL_OBSERVED_PATH_UPDATE_SMUGGLED)
    hits = scan_text_for_recommendations(json.dumps(record, sort_keys=True))
    if hits:
        fail(FAIL_RECOMMENDATION_INSERTED, str(hits))


def render_markdown(record: dict[str, Any]) -> str:
    request = record["requested_movement"]
    source = record["source_authority"]
    target = record["classification_target"]
    lines = [
        "# C8 n22 requested action record v0",
        "",
        "## Status",
        "",
        record["request_gate"]["requested_action_gate"],
        "",
        "## Record role",
        "",
        record["record_role"],
        "",
        "## Requested action",
        "",
        request["requested_action"],
        "",
        "## Requested scope",
        "",
        request["requested_action_scope"],
        "",
        "## Requested output kind",
        "",
        request["requested_output_kind"],
        "",
        "## Source authority state",
        "",
        source["current_authority_state"],
        "",
        "## Basis",
        "",
        "c8.n22 only",
        "",
        "## Request role",
        "",
        "This record declares a requested action for router classification.",
        "",
        "It does not classify, approve, authorize, or perform the request.",
        "",
        "## Classification target",
        "",
        target["target_router"],
        "",
        "## Non-effects",
        "",
        "- no action executed",
        "- no authority changed",
        "- no route classification emitted",
        "- no requested output created",
        "- no unit executed",
        "- no next unit finalized",
        "- no next unit authorized",
        "- no receipts rewritten",
        "- no observed path updated",
        "- no taxonomy promoted",
        "- no reuse authorized",
        "- no updater generalized",
        "- no runner authority created",
        "",
        "## Non-claims",
        "",
    ]
    lines.extend(f"- {claim}" for claim in record["non_claims"])
    lines.extend(["", "## Unsafe to infer", ""])
    lines.extend(f"- {item}" for item in record["unsafe_to_infer"])
    return "\n".join(lines) + "\n"


def validate_markdown(record: dict[str, Any], markdown: str) -> None:
    required = [
        "# C8 n22 requested action record v0",
        "REQUESTED_ACTION_PASS_DECLARED_ONLY",
        "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
        "PREPARE_SURFACE_ONLY",
        "NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
        "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        "c8.n22 only",
        "This record declares a requested action for router classification.",
        "It does not classify, approve, authorize, or perform the request.",
        "READ_ONLY_AUTHORITY_ROUTER",
        "no route classification emitted",
        "no requested output created",
        "no next unit finalized",
        "no next unit authorized",
    ]
    missing = [phrase for phrase in required if phrase not in markdown]
    if missing:
        fail(FAIL_MARKDOWN_JSON_PARITY, str(missing))
    if "ROUTE_" in markdown:
        fail(FAIL_ROUTE_CLASSIFICATION_EMITTED)
    hits = scan_text_for_recommendations(markdown)
    if hits:
        fail(FAIL_RECOMMENDATION_INSERTED, str(hits))


def write_outputs(root: Path, record: dict[str, Any]) -> None:
    markdown = render_markdown(record)
    validate_markdown(record, markdown)
    json_path = root / OUTPUT_JSON
    md_path = root / OUTPUT_MD
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")


def print_success(record: dict[str, Any]) -> None:
    source = record["source_authority"]
    request = record["requested_movement"]
    target = record["classification_target"]
    gate = record["request_gate"]
    print("BUILD_C8_N22_REQUESTED_ACTION_RECORD_V0_COMPLETE")
    print(f"requested_action_record_id={record['requested_action_record_id']}")
    print(f"schema_version={record['schema_version']}")
    print(f"record_role={record['record_role']}")
    print(f"request_status={record['request_status']}")
    print(f"authority_transition_closure_id={source['authority_transition_closure_id']}")
    print(f"authority_update_id={source['authority_update_id']}")
    print(f"source_authority_state={source['current_authority_state']}")
    print(f"basis_scope={source['basis_scope']}")
    print(f"next_lawful_surface_from_closure={source['next_lawful_surface_from_closure']}")
    print(
        "next_allowed_router_action_from_authority_update="
        f"{source['next_allowed_router_action_from_authority_update']}"
    )
    print(
        "machine_permitted_action_scope_from_closure="
        f"{source['machine_permitted_action_scope_from_closure']}"
    )
    print(f"requested_action={request['requested_action']}")
    print(f"requested_action_scope={request['requested_action_scope']}")
    print(f"requested_output_kind={request['requested_output_kind']}")
    print(f"requested_target_basis={request['requested_target_basis']}")
    print(
        "request_matches_next_lawful_surface_from_closure="
        f"{str(request['request_matches_next_lawful_surface_from_closure']).lower()}"
    )
    print(
        "request_matches_authority_update_next_router_action="
        f"{str(request['request_matches_authority_update_next_router_action']).lower()}"
    )
    print(f"target_router={target['target_router']}")
    print(f"classification_question={target['classification_question']}")
    print(f"requested_action_gate={gate['requested_action_gate']}")
    print(f"requested_action_typed={str(gate['requested_action_typed']).lower()}")
    print(f"requested_action_scope_typed={str(gate['requested_action_scope_typed']).lower()}")
    print(f"source_authority_state_present={str(gate['source_authority_state_present']).lower()}")
    print(f"request_source_chain_present={str(gate['request_source_chain_present']).lower()}")
    print(f"requested_action_executed={str(gate['requested_action_executed']).lower()}")
    print(f"authority_changed={str(gate['authority_changed']).lower()}")
    print(f"route_classification_emitted={str(gate['route_classification_emitted']).lower()}")
    print(f"requested_output_created={str(gate['requested_output_created']).lower()}")
    print("next_unit_defined=false")
    print("next_unit_authorized=false")
    print("runtime_executed=false")
    print("receipts_rewritten=false")
    print("taxonomy_promoted=false")
    print("runner_authority_created=false")
    print("observed_path_updated=false")
    print("observed_path_update_proposed=false")
    print("router_classification_created=false")
    print("b2_created=false")
    print("b3_created=false")
    print("commit_created=false")
    print("push_executed=false")
    print("terminal_transition=ADVANCE(B2_READ_ONLY_AUTHORITY_ROUTE_CLASSIFICATION_PENDING)")


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
