#!/usr/bin/env python3
"""Build the C8 n22 authority boundary transition record v0.

This creates one machine-primary, human-auditable boundary record. It does not
build validator/router/halt systems, Human Readout generation, runner authority,
or any next-unit automation.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_authority_boundary_transition_record_v0.py"
OUTPUT_JSON = "docs/matrixlabs/boundary/c8_n22_authority_boundary_transition_record_v0.json"
OUTPUT_MD = "docs/matrixlabs/boundary/c8_n22_authority_boundary_transition_record_v0.md"

PATH_V1 = "docs/matrixlabs/architecture/c8_observed_decision_path_v1.json"
INDEX_V1 = "docs/matrixlabs/observability/decision_path_index_v1.json"
SPINE_V1 = "docs/matrixlabs/observability/receipt_spine_v1.json"
M7B_APPLY = "docs/matrixlabs/observability/c8_observed_path_update_apply_v0.json"
M6_PACKET = "docs/matrixlabs/c8/continuation/c8_taxonomy_applied_continuation_packet_v0.json"
M5_TAXONOMY = "docs/matrixlabs/observability/proceed_surface_taxonomy_v0.json"
CLOSEOUT_WRAPPER = "docs/matrixlabs/observability/closeout_wrapper_v0.json"

EXPECTED_COMMITS = {
    "m7b_apply_commit_sha": "d4b19660db77ba53dbf68e0f3a0cfd3e8ce899f0",
    "m7a_proposal_commit_sha": "6461d1511b4091ea76a57b040684f4cc5521a3ba",
    "m6_packet_commit_sha": "d21e162d7c52d57d8aa321434d533b99f7e46c23",
    "m5_taxonomy_commit_sha": "099a003bf849cc0d4292c4980982166be291f405",
    "m4_closeout_wrapper_commit_sha": "6aa9070f2d7a845640a23370a742ee13723a3b51",
}

NON_CLAIMS = [
    "This boundary record is machine-primary and human-auditable.",
    "Human Readout is downstream projection only.",
    "This boundary record does not consume human acceptance.",
    "This boundary record does not authorize the next C8 unit.",
    "This boundary record does not define the next C8 unit.",
    "This boundary record does not execute runtime/probe/build/rerun.",
    "This boundary record does not rewrite receipts.",
    "This boundary record does not promote taxonomy.",
    "This boundary record does not authorize reuse.",
    "This boundary record does not generalize the updater.",
    "This boundary record does not create runner authority.",
    "This boundary record does not validate theorem truth.",
    "This boundary record does not validate receipt truth.",
    "This boundary record does not validate edge lawfulness.",
    "This boundary record only preserves the typed authority state for c8.n22.",
]


class GenerationError(RuntimeError):
    pass


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
        raise GenerationError(f"not inside a git repository: {proc.stderr.strip()}")
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
        raise GenerationError(
            f"git {' '.join(args)} failed: {proc.stderr.strip() or proc.stdout.strip()}"
        )
    return proc.stdout.strip()


def commit_for_paths(root: Path, paths: list[str]) -> str:
    existing = [path for path in paths if (root / path).exists()]
    if not existing:
        raise GenerationError(f"no existing source paths among: {paths}")
    return run_git(root, ["log", "-n", "1", "--format=%H", "--", *existing])


def verify_commits(root: Path) -> None:
    for key, sha in EXPECTED_COMMITS.items():
        run_git(root, ["cat-file", "-e", f"{sha}^{{commit}}"])
    path_commits = {
        "m7b_apply_commit_sha": commit_for_paths(
            root,
            [
                M7B_APPLY,
                "docs/matrixlabs/observability/c8_observed_path_update_apply_v0.md",
                "scripts/build_c8_observed_path_update_apply_v0.py",
            ],
        ),
        "m6_packet_commit_sha": commit_for_paths(
            root,
            [
                M6_PACKET,
                "docs/matrixlabs/c8/continuation/c8_taxonomy_applied_continuation_packet_v0.md",
                "scripts/build_c8_taxonomy_applied_continuation_packet_v0.py",
            ],
        ),
        "m5_taxonomy_commit_sha": commit_for_paths(
            root,
            [
                M5_TAXONOMY,
                "docs/matrixlabs/observability/proceed_surface_taxonomy_v0.md",
                "scripts/build_proceed_surface_taxonomy_v0.py",
            ],
        ),
        "m4_closeout_wrapper_commit_sha": commit_for_paths(
            root,
            [
                CLOSEOUT_WRAPPER,
                "docs/matrixlabs/observability/closeout_wrapper_v0.md",
                "scripts/matrixlab_closeout_wrapper_v0.py",
            ],
        ),
    }
    for key, got in path_commits.items():
        if got != EXPECTED_COMMITS[key]:
            raise GenerationError(f"{key}:{got}!={EXPECTED_COMMITS[key]}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(root: Path, rel: str) -> dict[str, Any]:
    try:
        return json.loads((root / rel).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GenerationError(f"missing required source: {rel}") from exc
    except json.JSONDecodeError as exc:
        raise GenerationError(f"invalid JSON in source: {rel}") from exc


def find_list(obj: dict[str, Any], candidates: list[str]) -> list[Any] | None:
    for key in candidates:
        value = obj.get(key)
        if isinstance(value, list):
            return value
    return None


def validate_sources(
    path_v1: dict[str, Any],
    index_v1: dict[str, Any],
    spine_v1: dict[str, Any],
    m7b: dict[str, Any],
    m6: dict[str, Any],
    m5: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    nodes = find_list(path_v1, ["nodes", "path_nodes", "decision_nodes"]) or []
    edges = find_list(path_v1, ["edges", "path_edges", "decision_edges"]) or []
    n22 = next((node for node in nodes if node.get("node_id") == "c8.n22"), None)
    e21_22 = next((edge for edge in edges if edge.get("edge_id") == "c8.e21_22"), None)
    if not n22:
        raise GenerationError("c8.n22 missing from observed path v1")
    if not e21_22:
        raise GenerationError("c8.e21_22 missing from observed path v1")
    terminal = index_v1.get("terminal_node_id")
    if terminal not in ["c8.n22", None]:
        raise GenerationError(f"unexpected index v1 terminal node: {terminal}")

    checks = {
        "path_n22_receipt_backing_kind": (n22.get("receipt_backing_kind"), "SOURCE_COMMIT_ONLY_PACKET_PREPARATION"),
        "path_n22_observation_status": (n22.get("observation_status"), "OBSERVED_COMMITTED_PACKET_PREPARATION"),
        "path_n22_human_boundary": (n22.get("human_boundary_status"), "REQUIRED_NOT_YET_CONSUMED"),
        "path_n22_authorized_future_unit": (n22.get("authorized_future_unit_status"), "NOT_AUTHORIZED_BY_TAXONOMY_LABEL"),
        "path_e21_22_status": (e21_22.get("edge_status"), "OBSERVED_READOUT_EDGE_ONLY"),
        "m7b_apply_status": (m7b.get("apply_status"), "APPLY_PASS_APPEND_ONLY_READOUT_UPDATE"),
        "m6_human_boundary_status": (m6.get("taxonomy_use", {}).get("human_boundary_status"), "REQUIRED_NOT_YET_CONSUMED"),
        "m6_authorized_future_unit_status": (m6.get("taxonomy_use", {}).get("authorized_future_unit_status"), "NOT_AUTHORIZED_BY_TAXONOMY_LABEL"),
        "m6_taxonomy_use_status": (m6.get("taxonomy_use", {}).get("taxonomy_use_status"), "DESCRIPTIVE_ONLY"),
        "m6_taxonomy_use_result": (m6.get("taxonomy_use_verdict", {}).get("result"), "TAXONOMY_USE_PASS_WITH_ASSIGN_MIX"),
        "m6_next_unit_chosen": (m6.get("acceptance_summary", {}).get("next_c8_unit_chosen_by_packet"), False),
        "m5_taxonomy_status": (m5.get("taxonomy_status"), "TAXONOMY_V0_DESCRIPTIVE_ONLY"),
        "m5_label_authority": (m5.get("label_authority"), "ZERO_AUTHORITY_DESCRIPTIVE_ONLY"),
        "spine_v1_schema": (spine_v1.get("schema_version"), "matrixlabs_receipt_spine_v1"),
    }
    failures = [f"{label}:{got}!={want}" for label, (got, want) in checks.items() if got != want]
    forbidden = m7b.get("forbidden_effects", {})
    for key in [
        "next_c8_unit_chosen",
        "future_unit_authorized",
        "runtime_probe_build_rerun_executed",
        "receipts_rewritten",
        "schema_promoted",
        "runner_authority_created",
        "decision_path_updater_created_as_authority",
        "uses_m4_as_semantic_dependency",
    ]:
        if forbidden.get(key) is not False:
            failures.append(f"m7b_forbidden_{key}:{forbidden.get(key)}!=False")
    if failures:
        raise GenerationError("; ".join(failures))
    return n22, e21_22


def build_record(root: Path) -> dict[str, Any]:
    path_v1 = load_json(root, PATH_V1)
    index_v1 = load_json(root, INDEX_V1)
    spine_v1 = load_json(root, SPINE_V1)
    m7b = load_json(root, M7B_APPLY)
    m6 = load_json(root, M6_PACKET)
    m5 = load_json(root, M5_TAXONOMY)
    verify_commits(root)
    n22, e21_22 = validate_sources(path_v1, index_v1, spine_v1, m7b, m6, m5)

    record = {
        "schema_version": "matrixlabs_authority_boundary_transition_record_v0",
        "boundary_record_id": "c8.n22.boundary_transition.v0",
        "record_role": "MACHINE_PRIMARY_AUTHORITY_TRANSITION_RECORD",
        "human_readout_role": "DOWNSTREAM_PROJECTION_ONLY",
        "source_paths": {
            "observed_path_v1": PATH_V1,
            "decision_path_index_v1": INDEX_V1,
            "receipt_spine_v1": SPINE_V1,
            "m7b_apply": M7B_APPLY,
            "m6_packet": M6_PACKET,
            "m5_taxonomy": M5_TAXONOMY,
        },
        "source_hashes": {
            "observed_path_v1_sha256": sha256_file(root / PATH_V1),
            "decision_path_index_v1_sha256": sha256_file(root / INDEX_V1),
            "receipt_spine_v1_sha256": sha256_file(root / SPINE_V1),
            "m7b_apply_sha256": sha256_file(root / M7B_APPLY),
            "m6_packet_sha256": sha256_file(root / M6_PACKET),
            "m5_taxonomy_sha256": sha256_file(root / M5_TAXONOMY),
        },
        "source_commits": {
            "m7b_apply_commit_sha": EXPECTED_COMMITS["m7b_apply_commit_sha"],
            "m7a_proposal_commit_sha": EXPECTED_COMMITS["m7a_proposal_commit_sha"],
            "m6_packet_commit_sha": EXPECTED_COMMITS["m6_packet_commit_sha"],
            "m5_taxonomy_commit_sha": EXPECTED_COMMITS["m5_taxonomy_commit_sha"],
        },
        "preservation_context": {
            "uses_m4_as_semantic_dependency": False,
            "m4_closeout_wrapper_commit_sha": EXPECTED_COMMITS["m4_closeout_wrapper_commit_sha"],
        },
        "source": {
            "source_object_type": "OBSERVED_PATH_NODE",
            "source_object_id": "c8.n22",
            "source_path_version": "c8_observed_decision_path_v1",
            "source_terminal_status": n22.get("observation_status"),
            "source_receipt_backing_kind": n22.get("receipt_backing_kind"),
            "source_edge_id": "c8.e21_22",
            "source_edge_status": e21_22.get("edge_status"),
            "source_commit_sha": EXPECTED_COMMITS["m7b_apply_commit_sha"],
        },
        "boundary_class": "HUMAN_AUTHORITY_BOUNDARY",
        "current_authority": {
            "current_authority_state": "AUTH_STATE_OBSERVED_NOT_AUTHORIZED",
            "current_observation_state": "OBSERVED_COMMITTED_PACKET_PREPARATION",
            "human_acceptance_state": "AUTH_EVENT_UNCONSUMED",
            "next_unit_definition_authority": "NOT_GRANTED",
            "execution_authority": "NOT_GRANTED",
            "reuse_authority": "NOT_GRANTED",
            "promotion_authority": "NOT_GRANTED",
            "runner_authority": "NOT_GRANTED",
        },
        "proposed_transition": {
            "transition_id": "ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
            "transition_kind": "HUMAN_AUTHORITY_TRANSITION",
            "target_authority_state_if_accepted": "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
            "authority_change_if_accepted": [
                "c8.n22 may be used as the accepted basis for defining the next bounded C8 unit"
            ],
            "authority_remaining_false_after_acceptance": [
                "execution_authority",
                "reuse_authority",
                "promotion_authority",
                "runner_authority",
                "generic_updater_reuse_authority",
                "auto_next_unit_selection_authority",
            ],
        },
        "required_authority_event": {
            "required_event": "HUMAN_ACCEPTANCE",
            "required_actor": "HUMAN",
            "required_event_status": "AUTH_EVENT_UNCONSUMED",
            "decision_receipt_required": True,
            "decision_receipt_schema": "matrixlabs_human_decision_receipt_v0",
        },
        "machine_action_scope": {
            "machine_permitted_action_scope": "PREPARE_DECISION_SURFACE_ONLY",
            "machine_forbidden_action_scopes": [
                "APPLY_AUTHORITY_TRANSITION",
                "DEFINE_NEXT_UNIT_WITHOUT_ACCEPTANCE",
                "EXECUTE_UNIT",
                "REWRITE_RECEIPTS",
                "PROMOTE_TAXONOMY",
                "AUTHORIZE_REUSE",
                "GENERALIZE_UPDATER",
                "ACTIVATE_RUNNER",
                "SELECT_NEXT_UNIT",
            ],
        },
        "transition_disposition": {
            "classification_result": "HUMAN_ACCEPTANCE_REQUIRED",
            "transition_status": "BLOCKED_PENDING_AUTHORITY_EVENT",
            "router_action": "PREPARE_HUMAN_DECISION_SURFACE",
            "halt_code": "NONE",
            "escalation_code": "AWAIT_HUMAN_DECISION",
        },
        "semantic_conservation": {
            "readout_may_project": True,
            "readout_may_add_meaning": False,
            "prose_may_override_typed_fields": False,
            "taxonomy_label_may_authorize_future_unit": False,
            "commit_status_may_create_authority": False,
            "receipt_existence_may_validate_truth": False,
            "observed_edge_may_imply_acceptance": False,
            "readout_update_may_choose_next_unit": False,
        },
        "derived_checks": {
            "machine_may_prepare_decision_surface": True,
            "machine_may_apply_transition": False,
            "machine_may_define_next_unit": False,
            "machine_may_execute": False,
            "human_acceptance_required": True,
            "human_acceptance_consumed": False,
            "authority_change_pending": True,
        },
        "non_claims": list(NON_CLAIMS),
        "generated_by": GENERATOR,
    }
    verify_record(record)
    return record


def find_bool_outside_allowed(obj: Any, path: str = "$", root: str | None = None) -> list[str]:
    hits: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            next_root = key if path == "$" else root
            hits.extend(find_bool_outside_allowed(value, f"{path}.{key}", next_root))
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            hits.extend(find_bool_outside_allowed(value, f"{path}[{index}]", root))
    elif isinstance(obj, bool) and root not in {"semantic_conservation", "derived_checks"}:
        hits.append(path)
    return hits


def verify_record(record: dict[str, Any]) -> None:
    typed_fields = [
        record["current_authority"]["current_authority_state"],
        record["required_authority_event"]["required_event"],
        record["required_authority_event"]["required_event_status"],
        record["machine_action_scope"]["machine_permitted_action_scope"],
        record["transition_disposition"]["transition_status"],
    ]
    if not all(isinstance(value, str) for value in typed_fields):
        raise GenerationError("primary authority fields must be strings")
    if record["machine_action_scope"]["machine_permitted_action_scope"] != "PREPARE_DECISION_SURFACE_ONLY":
        raise GenerationError("machine scope drifted")
    if record["required_authority_event"]["required_event"] != "HUMAN_ACCEPTANCE":
        raise GenerationError("required authority event drifted")
    if record["transition_disposition"]["transition_status"] != "BLOCKED_PENDING_AUTHORITY_EVENT":
        raise GenerationError("transition disposition drifted")
    required_scopes = {
        "EXECUTE_UNIT",
        "REWRITE_RECEIPTS",
        "PROMOTE_TAXONOMY",
        "AUTHORIZE_REUSE",
        "GENERALIZE_UPDATER",
        "ACTIVATE_RUNNER",
        "SELECT_NEXT_UNIT",
    }
    got_scopes = set(record["machine_action_scope"]["machine_forbidden_action_scopes"])
    missing = sorted(required_scopes - got_scopes)
    if missing:
        raise GenerationError(f"missing machine forbidden scopes: {missing}")


def render_markdown(record: dict[str, Any]) -> str:
    source = record["source"]
    current = record["current_authority"]
    transition = record["proposed_transition"]
    required = record["required_authority_event"]
    scope = record["machine_action_scope"]
    disposition = record["transition_disposition"]
    lines = [
        "# C8 n22 authority boundary transition record v0",
        "",
        "## Status",
        "",
        disposition["transition_status"],
        "",
        "## Source",
        "",
        f"- source object: {source['source_object_id']}",
        f"- source path: {source['source_path_version']}",
        f"- backing: {source['source_receipt_backing_kind']}",
        f"- edge: {source['source_edge_id']}",
        f"- edge status: {source['source_edge_status']}",
        "",
        "## Current authority state",
        "",
        current["current_authority_state"],
        "",
        "## Proposed transition",
        "",
        transition["transition_id"],
        "",
        "## Required authority event",
        "",
        required["required_event"],
        "",
        f"Status: {required['required_event_status']}",
        "",
        "## Machine action scope",
        "",
        "Permitted:",
        f"- {scope['machine_permitted_action_scope']}",
        "",
        "Forbidden:",
    ]
    lines.extend(f"- {item}" for item in scope["machine_forbidden_action_scopes"])
    lines.extend(
        [
            "",
            "## Router disposition",
            "",
            f"router_action = {disposition['router_action']}",
            f"transition_status = {disposition['transition_status']}",
            f"escalation_code = {disposition['escalation_code']}",
            "",
            "## Human-readable projection",
            "",
            "c8.n22 has been observed as a committed packet-preparation node.",
            "",
            "It has not been accepted as the basis for defining the next bounded C8 unit.",
            "",
            "The machine may prepare a human decision surface, but it may not define the next unit, execute runtime, promote taxonomy, authorize reuse, generalize the updater, or activate runner authority.",
            "",
            "A human acceptance event is required before c8.n22 can become an accepted basis for next-unit definition.",
            "",
            "## Non-claims",
            "",
        ]
    )
    lines.extend(f"- {claim}" for claim in record["non_claims"])
    return "\n".join(lines) + "\n"


def write_outputs(root: Path, record: dict[str, Any]) -> None:
    json_path = root / OUTPUT_JSON
    md_path = root / OUTPUT_MD
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(record), encoding="utf-8")


def main() -> int:
    try:
        root = detect_repo_root(Path.cwd())
        record = build_record(root)
        write_outputs(root, record)
    except GenerationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(
        "Generated c8.n22 authority boundary transition record "
        f"{record['transition_disposition']['transition_status']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
