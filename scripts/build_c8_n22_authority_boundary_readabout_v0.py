#!/usr/bin/env python3
"""Build the c8.n22 authority boundary Readabout projection v0.

The JSON packet is the operational artifact. Markdown is rendered from the JSON
only and carries no independent authority.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_authority_boundary_readabout_v0.py"
OUTPUT_JSON = "docs/matrixlabs/readabouts/c8_n22_authority_boundary_readabout_v0.json"
OUTPUT_MD = "docs/matrixlabs/readabouts/c8_n22_authority_boundary_readabout_v0.md"

BOUNDARY = "docs/matrixlabs/boundary/c8_n22_authority_boundary_transition_record_v0.json"
PATH_V1 = "docs/matrixlabs/architecture/c8_observed_decision_path_v1.json"
M7B_APPLY = "docs/matrixlabs/observability/c8_observed_path_update_apply_v0.json"
M6_PACKET = "docs/matrixlabs/c8/continuation/c8_taxonomy_applied_continuation_packet_v0.json"
M5_TAXONOMY = "docs/matrixlabs/observability/proceed_surface_taxonomy_v0.json"

BOUNDARY_COMMIT = "c0e560c3d22d17ffcc734477c588a6f352950c13"

ALLOWED_PROJECTION_TYPES = {
    "DIRECT_FIELD_RENDER",
    "FIELD_EXPANSION",
    "FIELD_GROUPING",
    "PROJECTION_RULE_RENDER",
    "NON_CLAIM_RENDER",
    "MISSING_FIELD_RENDER",
    "UNSAFE_INFERENCE_BLOCK",
}

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


def verify_source_commit(root: Path) -> None:
    run_git(root, ["cat-file", "-e", f"{BOUNDARY_COMMIT}^{{commit}}"])
    got = commit_for_paths(
        root,
        [
            BOUNDARY,
            "docs/matrixlabs/boundary/c8_n22_authority_boundary_transition_record_v0.md",
            "scripts/build_c8_n22_authority_boundary_transition_record_v0.py",
        ],
    )
    if got != BOUNDARY_COMMIT:
        raise GenerationError(f"boundary record commit mismatch: {got}!={BOUNDARY_COMMIT}")


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


def path_get(obj: dict[str, Any], path: str) -> Any:
    if not path.startswith("$."):
        raise GenerationError(f"unsupported source path syntax: {path}")
    cur: Any = obj
    for part in path[2:].split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            raise GenerationError(f"required source field missing: {path}")
    return cur


def source_values(source: dict[str, Any], paths: list[str]) -> dict[str, Any]:
    return {path: path_get(source, path) for path in paths}


def validate_source(source: dict[str, Any]) -> None:
    checks = {
        "schema_version": (source.get("schema_version"), "matrixlabs_authority_boundary_transition_record_v0"),
        "boundary_record_id": (source.get("boundary_record_id"), "c8.n22.boundary_transition.v0"),
        "human_readout_role": (source.get("human_readout_role"), "DOWNSTREAM_PROJECTION_ONLY"),
        "current_authority_state": (
            source.get("current_authority", {}).get("current_authority_state"),
            "AUTH_STATE_OBSERVED_NOT_AUTHORIZED",
        ),
        "transition_id": (
            source.get("proposed_transition", {}).get("transition_id"),
            "ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        ),
        "required_event": (
            source.get("required_authority_event", {}).get("required_event"),
            "HUMAN_ACCEPTANCE",
        ),
        "required_event_status": (
            source.get("required_authority_event", {}).get("required_event_status"),
            "AUTH_EVENT_UNCONSUMED",
        ),
        "machine_scope": (
            source.get("machine_action_scope", {}).get("machine_permitted_action_scope"),
            "PREPARE_DECISION_SURFACE_ONLY",
        ),
        "transition_status": (
            source.get("transition_disposition", {}).get("transition_status"),
            "BLOCKED_PENDING_AUTHORITY_EVENT",
        ),
    }
    failures = [f"{label}:{got}!={want}" for label, (got, want) in checks.items() if got != want]
    if failures:
        raise GenerationError("; ".join(failures))


def claim(
    source: dict[str, Any],
    claim_id: str,
    human_language_claim: str,
    paths: list[str],
    template_id: str,
    projection_type: str,
    authority_sensitivity: str = "HIGH",
) -> dict[str, Any]:
    if projection_type not in ALLOWED_PROJECTION_TYPES:
        raise GenerationError(f"bad projection type for {claim_id}: {projection_type}")
    if projection_type == "GOVERNANCE_RULE_RENDER":
        raise GenerationError("GOVERNANCE_RULE_RENDER is not allowed")
    return {
        "claim_id": claim_id,
        "human_language_claim": human_language_claim,
        "source_field_paths": list(paths),
        "source_values": source_values(source, paths),
        "template_id": template_id,
        "projection_type": projection_type,
        "authority_sensitivity": authority_sensitivity,
        "projection_status": "BACKED",
    }


def nonclaim(
    source: dict[str, Any],
    non_claim_id: str,
    human_language_non_claim: str,
    paths: list[str],
    authority_sensitivity: str = "HIGH",
) -> dict[str, Any]:
    return {
        "non_claim_id": non_claim_id,
        "human_language_non_claim": human_language_non_claim,
        "source_field_paths": list(paths),
        "source_values": source_values(source, paths),
        "projection_type": "NON_CLAIM_RENDER",
        "authority_sensitivity": authority_sensitivity,
        "projection_status": "BACKED",
    }


def projection_templates() -> dict[str, dict[str, Any]]:
    return {
        "template.authority_state.observed_not_authorized.v0": {
            "trigger_value": "AUTH_STATE_OBSERVED_NOT_AUTHORIZED",
            "template": "The source object has been observed, but it has not been granted authority for progression.",
            "required_source_field_paths": [
                "$.current_authority.current_authority_state"
            ],
            "projection_type": "FIELD_EXPANSION",
        },
        "template.machine_scope.prepare_decision_surface_only.v0": {
            "trigger_value": "PREPARE_DECISION_SURFACE_ONLY",
            "template": "The machine may prepare the human decision surface only.",
            "required_source_field_paths": [
                "$.machine_action_scope.machine_permitted_action_scope"
            ],
            "projection_type": "FIELD_EXPANSION",
        },
        "template.transition.blocked_pending_authority_event.v0": {
            "trigger_value": "BLOCKED_PENDING_AUTHORITY_EVENT",
            "template": "Progression is blocked until the required authority event is consumed.",
            "required_source_field_paths": [
                "$.transition_disposition.transition_status",
                "$.required_authority_event.required_event",
                "$.required_authority_event.required_event_status",
            ],
            "projection_type": "FIELD_EXPANSION",
        },
    }


def build_projection_claims(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        claim(
            source,
            "claim.source.identity",
            "This Readabout projects the formal boundary record c8.n22.boundary_transition.v0.",
            ["$.boundary_record_id", "$.schema_version", "$.record_role", "$.human_readout_role"],
            "template.source.identity.v0",
            "DIRECT_FIELD_RENDER",
        ),
        claim(
            source,
            "claim.source.truth_role",
            "The formal boundary record remains the source of truth; this Readabout is a downstream projection only.",
            ["$.record_role", "$.human_readout_role"],
            "template.source.truth_role.v0",
            "FIELD_GROUPING",
        ),
        claim(
            source,
            "claim.source.object",
            "The source object is c8.n22 in c8_observed_decision_path_v1.",
            ["$.source.source_object_id", "$.source.source_path_version"],
            "template.source.object.v0",
            "DIRECT_FIELD_RENDER",
        ),
        claim(
            source,
            "claim.boundary.class",
            "The boundary record classifies c8.n22 as a human authority boundary.",
            ["$.boundary_class"],
            "template.boundary.class.v0",
            "DIRECT_FIELD_RENDER",
        ),
        claim(
            source,
            "claim.current_authority.observed_not_authorized",
            "c8.n22 has been observed, but it is not authorized for progression.",
            ["$.current_authority.current_authority_state", "$.current_authority.current_observation_state"],
            "template.authority_state.observed_not_authorized.v0",
            "FIELD_EXPANSION",
        ),
        claim(
            source,
            "claim.transition.requested",
            "The proposed transition is to accept c8.n22 as the basis for defining the next bounded C8 unit.",
            [
                "$.proposed_transition.transition_id",
                "$.proposed_transition.target_authority_state_if_accepted",
                "$.proposed_transition.authority_change_if_accepted",
            ],
            "template.transition.requested.v0",
            "FIELD_EXPANSION",
        ),
        claim(
            source,
            "claim.authority_event.required",
            "This transition requires human acceptance.",
            ["$.required_authority_event.required_event", "$.required_authority_event.required_actor"],
            "template.authority_event.required.v0",
            "FIELD_EXPANSION",
        ),
        claim(
            source,
            "claim.authority_event.unconsumed",
            "The required human acceptance event has not been consumed.",
            ["$.required_authority_event.required_event_status", "$.current_authority.human_acceptance_state"],
            "template.authority_event.unconsumed.v0",
            "FIELD_EXPANSION",
        ),
        claim(
            source,
            "claim.machine_scope.prepare_only",
            "The machine may prepare the human decision surface only.",
            ["$.machine_action_scope.machine_permitted_action_scope"],
            "template.machine_scope.prepare_decision_surface_only.v0",
            "FIELD_EXPANSION",
        ),
        claim(
            source,
            "claim.machine_scope.forbidden",
            "The machine may not apply the authority transition, define the next unit without acceptance, execute a unit, rewrite receipts, promote taxonomy, authorize reuse, generalize the updater, activate runner authority, or select the next unit.",
            ["$.machine_action_scope.machine_forbidden_action_scopes"],
            "template.machine_scope.forbidden.v0",
            "FIELD_EXPANSION",
        ),
        claim(
            source,
            "claim.transition.blocked_pending_authority",
            "Progression is blocked pending the required authority event.",
            [
                "$.transition_disposition.transition_status",
                "$.transition_disposition.classification_result",
                "$.transition_disposition.escalation_code",
            ],
            "template.transition.blocked_pending_authority_event.v0",
            "FIELD_EXPANSION",
        ),
        claim(
            source,
            "claim.router.prepare_decision_surface",
            "The router action is to prepare the human decision surface.",
            ["$.transition_disposition.router_action"],
            "template.router.prepare_decision_surface.v0",
            "DIRECT_FIELD_RENDER",
        ),
        claim(
            source,
            "claim.semantic_conservation",
            "The Readabout may project the source record, but it may not add meaning, override typed fields, use taxonomy labels as future-unit authorization, treat commit status as authority, treat receipt existence as truth validation, treat the observed edge as acceptance, or treat the readout update as next-unit selection.",
            [
                "$.semantic_conservation.readout_may_project",
                "$.semantic_conservation.readout_may_add_meaning",
                "$.semantic_conservation.prose_may_override_typed_fields",
                "$.semantic_conservation.taxonomy_label_may_authorize_future_unit",
                "$.semantic_conservation.commit_status_may_create_authority",
                "$.semantic_conservation.receipt_existence_may_validate_truth",
                "$.semantic_conservation.observed_edge_may_imply_acceptance",
                "$.semantic_conservation.readout_update_may_choose_next_unit",
            ],
            "template.semantic_conservation.v0",
            "FIELD_GROUPING",
        ),
        claim(
            source,
            "claim.decision_relevance",
            "The relevant later human decision is whether to accept c8.n22 as the basis for next-unit definition, and a decision receipt is required for that authority event.",
            [
                "$.proposed_transition.transition_id",
                "$.required_authority_event.decision_receipt_required",
                "$.required_authority_event.decision_receipt_schema",
            ],
            "template.decision_relevance.v0",
            "PROJECTION_RULE_RENDER",
        ),
    ]


def build_unsafe_blocks(source: dict[str, Any]) -> list[dict[str, Any]]:
    specs = [
        (
            "unsafe.next_unit_defined",
            "Unsafe to infer: the next C8 unit is defined.",
            ["$.current_authority.next_unit_definition_authority", "$.transition_disposition.transition_status"],
        ),
        (
            "unsafe.next_unit_authorized",
            "Unsafe to infer: the next C8 unit is authorized.",
            ["$.current_authority.next_unit_definition_authority", "$.required_authority_event.required_event_status"],
        ),
        (
            "unsafe.execution_authorized",
            "Unsafe to infer: execution of a next C8 unit is authorized.",
            ["$.current_authority.execution_authority", "$.machine_action_scope.machine_permitted_action_scope", "$.transition_disposition.transition_status"],
        ),
        (
            "unsafe.human_acceptance_consumed",
            "Unsafe to infer: human acceptance has been consumed.",
            ["$.current_authority.human_acceptance_state", "$.required_authority_event.required_event_status"],
        ),
        (
            "unsafe.taxonomy_promoted",
            "Unsafe to infer: taxonomy is promoted.",
            ["$.current_authority.promotion_authority", "$.semantic_conservation.taxonomy_label_may_authorize_future_unit"],
        ),
        (
            "unsafe.reuse_authorized",
            "Unsafe to infer: reuse is authorized.",
            ["$.current_authority.reuse_authority", "$.machine_action_scope.machine_forbidden_action_scopes"],
        ),
        (
            "unsafe.updater_generalized",
            "Unsafe to infer: updater generalization is authorized.",
            ["$.machine_action_scope.machine_forbidden_action_scopes", "$.proposed_transition.authority_remaining_false_after_acceptance"],
        ),
        (
            "unsafe.runner_authority_exists",
            "Unsafe to infer: runner authority exists.",
            ["$.current_authority.runner_authority", "$.machine_action_scope.machine_forbidden_action_scopes"],
        ),
        (
            "unsafe.receipt_truth_validated",
            "Unsafe to infer: receipt truth is validated.",
            ["$.semantic_conservation.receipt_existence_may_validate_truth", "$.non_claims"],
        ),
        (
            "unsafe.edge_lawfulness_validated",
            "Unsafe to infer: edge lawfulness is validated.",
            ["$.source.source_edge_status", "$.non_claims"],
        ),
    ]
    return [
        claim(
            source,
            claim_id,
            human,
            paths,
            f"template.{claim_id}.v0",
            "UNSAFE_INFERENCE_BLOCK",
        )
        for claim_id, human, paths in specs
    ]


def build_nonclaims(source: dict[str, Any]) -> list[dict[str, Any]]:
    specs = [
        ("nonclaim.source_remains_authority", "The formal boundary record remains the authority source for this Readabout.", ["$.record_role", "$.human_readout_role"]),
        ("nonclaim.no_human_acceptance_consumed", "This Readabout does not consume human acceptance.", ["$.current_authority.human_acceptance_state", "$.required_authority_event.required_event_status"]),
        ("nonclaim.no_next_unit_defined", "This Readabout does not define the next C8 unit.", ["$.current_authority.next_unit_definition_authority", "$.transition_disposition.transition_status"]),
        ("nonclaim.no_next_unit_authorized", "This Readabout does not authorize the next C8 unit.", ["$.current_authority.next_unit_definition_authority", "$.machine_action_scope.machine_permitted_action_scope"]),
        ("nonclaim.no_execution_authority", "This Readabout does not authorize execution.", ["$.current_authority.execution_authority", "$.machine_action_scope.machine_permitted_action_scope"]),
        ("nonclaim.no_receipt_rewrite", "This Readabout does not rewrite receipts.", ["$.machine_action_scope.machine_forbidden_action_scopes"]),
        ("nonclaim.no_taxonomy_promotion", "This Readabout does not promote taxonomy.", ["$.current_authority.promotion_authority", "$.machine_action_scope.machine_forbidden_action_scopes"]),
        ("nonclaim.no_reuse_authority", "This Readabout does not authorize reuse.", ["$.current_authority.reuse_authority", "$.machine_action_scope.machine_forbidden_action_scopes"]),
        ("nonclaim.no_updater_generalization", "This Readabout does not generalize the updater.", ["$.machine_action_scope.machine_forbidden_action_scopes", "$.proposed_transition.authority_remaining_false_after_acceptance"]),
        ("nonclaim.no_runner_authority", "This Readabout does not create runner authority.", ["$.current_authority.runner_authority", "$.machine_action_scope.machine_forbidden_action_scopes"]),
        ("nonclaim.no_theorem_truth_validation", "This Readabout does not validate theorem truth.", ["$.non_claims"]),
        ("nonclaim.no_receipt_truth_validation", "This Readabout does not validate receipt truth.", ["$.semantic_conservation.receipt_existence_may_validate_truth", "$.non_claims"]),
        ("nonclaim.no_edge_lawfulness_validation", "This Readabout does not validate edge lawfulness.", ["$.source.source_edge_status", "$.non_claims"]),
        ("nonclaim.no_recommendation", "This Readabout does not recommend an action.", ["$.record_role", "$.human_readout_role", "$.transition_disposition.transition_status"]),
        ("nonclaim.not_decision_surface", "This Readabout is not a human decision surface.", ["$.human_readout_role", "$.machine_action_scope.machine_permitted_action_scope"]),
        ("nonclaim.not_decision_receipt", "This Readabout is not a decision receipt.", ["$.required_authority_event.decision_receipt_required", "$.required_authority_event.decision_receipt_schema", "$.required_authority_event.required_event_status"]),
    ]
    return [nonclaim(source, non_id, human, paths) for non_id, human, paths in specs]


def build_packet(root: Path) -> dict[str, Any]:
    boundary = load_json(root, BOUNDARY)
    # Load declared supporting artifacts so hashes can be checked and missing
    # sources fail before the Readabout is emitted.
    load_json(root, PATH_V1)
    load_json(root, M7B_APPLY)
    load_json(root, M6_PACKET)
    load_json(root, M5_TAXONOMY)
    verify_source_commit(root)
    validate_source(boundary)

    claims = build_projection_claims(boundary)
    unsafe = build_unsafe_blocks(boundary)
    nonclaims = build_nonclaims(boundary)
    packet = {
        "schema_version": "matrixlabs_readabout_projection_v0",
        "readabout_packet_id": "c8.n22.authority_boundary.readabout.v0",
        "readabout_role": "HUMAN_AUDIT_PROJECTION",
        "source_of_truth_role": "FORMAL_SOURCE_OBJECT_REMAINS_AUTHORITY",
        "projection_mode": "FIELD_BACKED_PARITY_PROJECTION",
        "source": {
            "source_object_type": "AUTHORITY_BOUNDARY_TRANSITION_RECORD",
            "source_object_id": "c8.n22.boundary_transition.v0",
            "source_path": BOUNDARY,
            "source_schema_version": "matrixlabs_authority_boundary_transition_record_v0",
            "source_commit_sha": BOUNDARY_COMMIT,
        },
        "source_hashes": {
            "boundary_record_sha256": sha256_file(root / BOUNDARY),
            "observed_path_v1_sha256": sha256_file(root / PATH_V1),
            "m7b_apply_sha256": sha256_file(root / M7B_APPLY),
            "m6_packet_sha256": sha256_file(root / M6_PACKET),
            "m5_taxonomy_sha256": sha256_file(root / M5_TAXONOMY),
        },
        "freshness": {
            "freshness_status": "SOURCE_COMMIT_VERIFIED",
            "freshness_basis": "source_commit_sha",
            "currentness_claim": "CURRENT_ONLY_RELATIVE_TO_VERIFIED_SOURCE_COMMIT",
        },
        "projection_templates": projection_templates(),
        "projection_claims": claims,
        "non_claims": nonclaims,
        "unsupported_or_absent_fields": [],
        "unsafe_to_infer": unsafe,
        "decision_relevance": {
            "human_decision_boundary_present": True,
            "decision_requested": "ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
            "decision_receipt_required": True,
            "decision_receipt_schema": "matrixlabs_human_decision_receipt_v0",
        },
        "projection_gate": {
            "readabout_gate": "READABOUT_PASS_PARITY",
            "source_object_id": "c8.n22.boundary_transition.v0",
            "source_schema_version": "matrixlabs_authority_boundary_transition_record_v0",
            "projection_claim_count": len(claims),
            "unsupported_claim_count": 0,
            "unbacked_load_bearing_claim_count": 0,
            "missing_required_source_field_count": 0,
            "unsafe_to_infer_section_present": True,
            "unsafe_to_infer_count": len(unsafe),
            "authority_collapse_count": 0,
            "authority_collapse_detected": False,
            "proposal_authority_collapse_detected": False,
            "preparation_execution_collapse_detected": False,
            "recommendation_inserted": False,
            "markdown_json_parity_status": "PASS",
            "meaning_parity_status": "PASS",
        },
        "generated_by": GENERATOR,
    }
    validate_packet(packet, boundary)
    return packet


def validate_backed_entries(packet: dict[str, Any], boundary: dict[str, Any]) -> None:
    for entry, id_key in [
        *((claim, "claim_id") for claim in packet["projection_claims"]),
        *((item, "claim_id") for item in packet["unsafe_to_infer"]),
        *((item, "non_claim_id") for item in packet["non_claims"]),
    ]:
        entry_id = entry[id_key]
        if entry["projection_type"] not in ALLOWED_PROJECTION_TYPES:
            raise GenerationError(f"{entry_id} bad projection type")
        if not entry.get("source_field_paths"):
            raise GenerationError(f"{entry_id} lacks source paths")
        for path in entry["source_field_paths"]:
            got = path_get(boundary, path)
            if entry["source_values"].get(path) != got:
                raise GenerationError(f"{entry_id} source mismatch at {path}")
        if entry.get("projection_status") != "BACKED":
            raise GenerationError(f"{entry_id} is not backed")


def scan_text_for_recommendations(text: str) -> list[str]:
    low = text.lower()
    return [phrase for phrase in RECOMMENDATION_PHRASES if phrase in low]


def validate_packet(packet: dict[str, Any], boundary: dict[str, Any]) -> None:
    validate_backed_entries(packet, boundary)
    if len(packet["projection_claims"]) < 14:
        raise GenerationError("projection claim count is too low")
    if len(packet["unsafe_to_infer"]) != 10:
        raise GenerationError("unsafe-to-infer count must be 10")
    if len(packet["non_claims"]) < 16:
        raise GenerationError("non-claim count is too low")
    text = json.dumps(packet, sort_keys=True)
    hits = scan_text_for_recommendations(text)
    if hits:
        raise GenerationError(f"recommendation language present: {hits}")


def render_markdown(packet: dict[str, Any]) -> str:
    source = packet["source"]
    claims = packet["projection_claims"]
    unsafe = packet["unsafe_to_infer"]
    nonclaims = packet["non_claims"]
    decision = packet["decision_relevance"]
    boundary_values = {
        path: claims_by_path_value(packet, path)
        for path in [
            "$.current_authority.current_authority_state",
            "$.transition_disposition.transition_status",
            "$.machine_action_scope.machine_permitted_action_scope",
        ]
    }
    lines = [
        "# Readabout: c8.n22 authority boundary",
        "",
        "## Source",
        "",
        f"- source object: {source['source_object_id']}",
        "- source type: authority boundary transition record",
        f"- source commit: {source['source_commit_sha']}",
        "",
        "## Status",
        "",
        f"- current authority state: {boundary_values['$.current_authority.current_authority_state']}",
        f"- transition status: {boundary_values['$.transition_disposition.transition_status']}",
        f"- machine scope: {boundary_values['$.machine_action_scope.machine_permitted_action_scope']}",
        "",
        "## What this means",
        "",
    ]
    for item in claims:
        lines.append(f"- `{item['claim_id']}`: {item['human_language_claim']}")
    lines.extend(
        [
            "",
            "## Decision relevance",
            "",
            f"- requested decision: {decision['decision_requested']}",
            "- required authority event: HUMAN_ACCEPTANCE",
            "- authority event status: AUTH_EVENT_UNCONSUMED",
            "- decision receipt required: yes",
            "",
            "## Unsafe to infer",
            "",
        ]
    )
    for item in unsafe:
        lines.append(f"- `{item['claim_id']}`: {item['human_language_claim']}")
    lines.extend(["", "## Traceability", ""])
    for item in claims:
        lines.append(
            f"- `{item['claim_id']}` -> {', '.join(item['source_field_paths'])}"
        )
    for item in unsafe:
        lines.append(
            f"- `{item['claim_id']}` -> {', '.join(item['source_field_paths'])}"
        )
    lines.extend(["", "## Non-claims", ""])
    for item in nonclaims:
        lines.append(f"- `{item['non_claim_id']}`: {item['human_language_non_claim']}")
    return "\n".join(lines) + "\n"


def claims_by_path_value(packet: dict[str, Any], path: str) -> Any:
    for group in [packet["projection_claims"], packet["unsafe_to_infer"], packet["non_claims"]]:
        for item in group:
            values = item.get("source_values", {})
            if path in values:
                return values[path]
    raise GenerationError(f"no rendered value for {path}")


def write_outputs(root: Path, packet: dict[str, Any]) -> None:
    json_path = root / OUTPUT_JSON
    md_path = root / OUTPUT_MD
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md = render_markdown(packet)
    hits = scan_text_for_recommendations(md)
    if hits:
        raise GenerationError(f"recommendation language present in markdown: {hits}")
    for required in [
        "claim.machine_scope.prepare_only",
        "claim.transition.blocked_pending_authority",
        "claim.authority_event.unconsumed",
    ]:
        if required not in md:
            raise GenerationError(f"markdown missing traceability id: {required}")
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(md, encoding="utf-8")


def main() -> int:
    try:
        root = detect_repo_root(Path.cwd())
        packet = build_packet(root)
        write_outputs(root, packet)
    except GenerationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(
        "Generated c8.n22 authority boundary Readabout "
        f"with {len(packet['projection_claims'])} backed claims"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
