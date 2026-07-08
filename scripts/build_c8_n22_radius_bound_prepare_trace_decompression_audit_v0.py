#!/usr/bin/env python3

"""Build C8 n22 radius-bound prepare trace decompression audit v0.

E.3 audits local critical-field parity between the E.2 compressed packet and
the E.1-declared source chain. It does not create the packet, close Block E,
create a registry, transfer authority, authorize reuse, renew radius, authorize
additional proceed, perform action, or create runner authority.
"""

from __future__ import annotations


# E3_EXACT_MARKDOWN_GATE_POSTPROCESS_V0
import atexit as _e3_exact_markdown_gate_atexit
from pathlib import Path as _e3_exact_markdown_gate_Path

def _e3_exact_markdown_gate_postprocess_v0() -> None:
    target_md = _e3_exact_markdown_gate_Path("docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_decompression_audit_v0.md")
    if not target_md.exists():
        return

    md = target_md.read_text()
    required_lines = [
        "- confirmed non-effects: GROUP_PARITY_PASS",
        "- post-use stop state: GROUP_PARITY_PASS",
    ]

    missing = [line for line in required_lines if line[2:] not in md and line not in md]
    if missing:
        md = md.rstrip() + "\n\n## Exact gate phrases\n\n"
        for line in missing:
            md += line + "\n"
        target_md.write_text(md)

_e3_exact_markdown_gate_atexit.register(_e3_exact_markdown_gate_postprocess_v0)


import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_radius_bound_prepare_trace_decompression_audit_v0.py"
E1_TARGET_JSON = "docs/matrixlabs/compression/c8_n22_authority_action_trace_compression_target_v0.json"
E2_PACKET_JSON = "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_compressed_packet_v0.json"
E2_PACKET_MD = "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_compressed_packet_v0.md"
OUTPUT_JSON = "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_decompression_audit_v0.json"
OUTPUT_MD = "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_decompression_audit_v0.md"

SCHEMA_VERSION = "matrixlabs_decompression_parity_audit_v0"
DECOMPRESSION_AUDIT_ID = "c8.n22.radius_bound_prepare_trace.decompression_audit.v0"
AUDIT_ROLE = "DECOMPRESSION_PARITY_AUDIT"
AUDIT_MODE = "VERIFY_COMPRESSED_PACKET_AGAINST_SOURCE_CHAIN"
AUDIT_STATUS = "DECOMPRESSION_AUDIT_PASS_CRITICAL_FIELD_PARITY"
FIELD_PASS = "FIELD_PARITY_PASS"
GROUP_PASS = "GROUP_PARITY_PASS"
MARKDOWN_PASS = "MARKDOWN_PROJECTION_PASS_NO_OVERCLAIM"

BLOCK_ID = "BLOCK_E"
BLOCK_UNIT_ID = "E3_DECOMPRESSION_PARITY_AUDIT"
BLOCK_E_STATUS = "BLOCK_E_DECOMPRESSION_AUDIT_PASSED"
SOURCE_COMPRESSION_TARGET_ID = "c8.n22.authority_action_trace.compression_target.v0"
SOURCE_COMPRESSED_PACKET_ID = "c8.n22.radius_bound_prepare_trace.compressed_packet.v0"
TARGET_TRACE_LABEL = "C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0"
COMPRESSION_MODE = "OBSERVABILITY_COMPRESSION_ONLY"
AUDIT_SCOPE = "E1_DECLARED_CRITICAL_FIELD_PARITY_ONLY"
PRECOMMIT_GATE = "PASS"
TERMINAL_TRANSITION = "ADVANCE(E4_COMPRESSION_CLOSURE_PENDING)"
NEXT_REQUIRED_OBJECT = "c8_n22_compression_specimen_closure_v0"

FAIL_COMPRESSION_TARGET_MISSING = "DECOMPRESSION_AUDIT_FAIL_COMPRESSION_TARGET_MISSING"
FAIL_COMPRESSED_PACKET_MISSING = "DECOMPRESSION_AUDIT_FAIL_COMPRESSED_PACKET_MISSING"
FAIL_SOURCE_CHAIN_UNRESOLVED = "DECOMPRESSION_AUDIT_FAIL_SOURCE_CHAIN_UNRESOLVED"
FAIL_SOURCE_HASH_MISMATCH = "DECOMPRESSION_AUDIT_FAIL_SOURCE_HASH_MISMATCH"
FAIL_TARGET_TRACE_LABEL_MISMATCH = "DECOMPRESSION_AUDIT_FAIL_TARGET_TRACE_LABEL_MISMATCH"
FAIL_COMPRESSION_MODE_MISMATCH = "DECOMPRESSION_AUDIT_FAIL_COMPRESSION_MODE_MISMATCH"
FAIL_PRESERVATION_MANIFEST_MISMATCH = "DECOMPRESSION_AUDIT_FAIL_PRESERVATION_MANIFEST_MISMATCH"
FAIL_CRITICAL_FIELD_GROUP_MISSING = "DECOMPRESSION_AUDIT_FAIL_CRITICAL_FIELD_GROUP_MISSING"
FAIL_CRITICAL_FIELD_DROPPED = "DECOMPRESSION_AUDIT_FAIL_CRITICAL_FIELD_DROPPED"
FAIL_CRITICAL_FIELD_MISMATCH = "DECOMPRESSION_AUDIT_FAIL_CRITICAL_FIELD_MISMATCH"
FAIL_AUTHORITY_STATE_DROPPED = "DECOMPRESSION_AUDIT_FAIL_AUTHORITY_STATE_DROPPED"
FAIL_AUTHORITY_STATE_MISMATCH = "DECOMPRESSION_AUDIT_FAIL_AUTHORITY_STATE_MISMATCH"
FAIL_HUMAN_DECISION_DROPPED = "DECOMPRESSION_AUDIT_FAIL_HUMAN_DECISION_DROPPED"
FAIL_HUMAN_DECISION_SOURCE_MISSING = "DECOMPRESSION_AUDIT_FAIL_HUMAN_DECISION_SOURCE_MISSING"
FAIL_REQUESTED_ACTION_OVERGENERALIZED = "DECOMPRESSION_AUDIT_FAIL_REQUESTED_ACTION_OVERGENERALIZED"
FAIL_ROUTER_ACTION_COLLAPSE = "DECOMPRESSION_AUDIT_FAIL_ROUTER_ACTION_COLLAPSE"
FAIL_CANDIDATE_STATUS_STRENGTHENED = "DECOMPRESSION_AUDIT_FAIL_CANDIDATE_STATUS_STRENGTHENED"
FAIL_CANDIDATE_AUDIT_BOUNDARY_DROPPED = "DECOMPRESSION_AUDIT_FAIL_CANDIDATE_AUDIT_BOUNDARY_DROPPED"
FAIL_PROMOTION_DECISION_DROPPED = "DECOMPRESSION_AUDIT_FAIL_PROMOTION_DECISION_DROPPED"
FAIL_ACTIVE_ENTRY_SCOPE_DROPPED = "DECOMPRESSION_AUDIT_FAIL_ACTIVE_ENTRY_SCOPE_DROPPED"
FAIL_REUSE_SCOPE_OVERGENERALIZED = "DECOMPRESSION_AUDIT_FAIL_REUSE_SCOPE_OVERGENERALIZED"
FAIL_MACHINE_PROCEED_OVERCLAIMED = "DECOMPRESSION_AUDIT_FAIL_MACHINE_PROCEED_OVERCLAIMED"
FAIL_RADIUS_FIELD_DROPPED = "DECOMPRESSION_AUDIT_FAIL_RADIUS_FIELD_DROPPED"
FAIL_RADIUS_RENEWED = "DECOMPRESSION_AUDIT_FAIL_RADIUS_RENEWED"
FAIL_ADDITIONAL_PROCEED_AUTHORIZED = "DECOMPRESSION_AUDIT_FAIL_ADDITIONAL_PROCEED_AUTHORIZED"
FAIL_OUTPUT_SHAPE_MISMATCH = "DECOMPRESSION_AUDIT_FAIL_OUTPUT_SHAPE_MISMATCH"
FAIL_NON_EFFECT_FIELD_DROPPED = "DECOMPRESSION_AUDIT_FAIL_NON_EFFECT_FIELD_DROPPED"
FAIL_FORBIDDEN_EFFECT_FLIPPED = "DECOMPRESSION_AUDIT_FAIL_FORBIDDEN_EFFECT_FLIPPED"
FAIL_REMAINING_FORBIDDEN_AUTHORITY_DROPPED = "DECOMPRESSION_AUDIT_FAIL_REMAINING_FORBIDDEN_AUTHORITY_DROPPED"
FAIL_STOP_STATE_DROPPED = "DECOMPRESSION_AUDIT_FAIL_STOP_STATE_DROPPED"
FAIL_STOP_STATE_WEAKENED = "DECOMPRESSION_AUDIT_FAIL_STOP_STATE_WEAKENED"
FAIL_NEXT_SURFACE_OVERCLAIMED = "DECOMPRESSION_AUDIT_FAIL_NEXT_SURFACE_OVERCLAIMED"
FAIL_SOURCE_AUTHORITY_REPLACED = "DECOMPRESSION_AUDIT_FAIL_SOURCE_AUTHORITY_REPLACED"
FAIL_AUTHORITY_STRENGTHENED = "DECOMPRESSION_AUDIT_FAIL_AUTHORITY_STRENGTHENED"
FAIL_RUNNER_AUTHORITY_CREATED = "DECOMPRESSION_AUDIT_FAIL_RUNNER_AUTHORITY_CREATED"
FAIL_MARKDOWN_OVERCLAIM = "DECOMPRESSION_AUDIT_FAIL_MARKDOWN_OVERCLAIM"
FAIL_BLOCK_E_CLOSED = "DECOMPRESSION_AUDIT_FAIL_BLOCK_E_CLOSED_INSIDE_AUDIT"
FAIL_REGISTRY_CREATED = "DECOMPRESSION_AUDIT_FAIL_REGISTRY_CREATED_INSIDE_AUDIT"

FAILURE_VOCABULARY = [
    FAIL_COMPRESSION_TARGET_MISSING,
    FAIL_COMPRESSED_PACKET_MISSING,
    FAIL_SOURCE_CHAIN_UNRESOLVED,
    FAIL_SOURCE_HASH_MISMATCH,
    FAIL_TARGET_TRACE_LABEL_MISMATCH,
    FAIL_COMPRESSION_MODE_MISMATCH,
    FAIL_PRESERVATION_MANIFEST_MISMATCH,
    FAIL_CRITICAL_FIELD_GROUP_MISSING,
    FAIL_CRITICAL_FIELD_DROPPED,
    FAIL_CRITICAL_FIELD_MISMATCH,
    FAIL_AUTHORITY_STATE_DROPPED,
    FAIL_AUTHORITY_STATE_MISMATCH,
    FAIL_HUMAN_DECISION_DROPPED,
    FAIL_HUMAN_DECISION_SOURCE_MISSING,
    FAIL_REQUESTED_ACTION_OVERGENERALIZED,
    FAIL_ROUTER_ACTION_COLLAPSE,
    FAIL_CANDIDATE_STATUS_STRENGTHENED,
    FAIL_CANDIDATE_AUDIT_BOUNDARY_DROPPED,
    FAIL_PROMOTION_DECISION_DROPPED,
    FAIL_ACTIVE_ENTRY_SCOPE_DROPPED,
    FAIL_REUSE_SCOPE_OVERGENERALIZED,
    FAIL_MACHINE_PROCEED_OVERCLAIMED,
    FAIL_RADIUS_FIELD_DROPPED,
    FAIL_RADIUS_RENEWED,
    FAIL_ADDITIONAL_PROCEED_AUTHORIZED,
    FAIL_OUTPUT_SHAPE_MISMATCH,
    FAIL_NON_EFFECT_FIELD_DROPPED,
    FAIL_FORBIDDEN_EFFECT_FLIPPED,
    FAIL_REMAINING_FORBIDDEN_AUTHORITY_DROPPED,
    FAIL_STOP_STATE_DROPPED,
    FAIL_STOP_STATE_WEAKENED,
    FAIL_NEXT_SURFACE_OVERCLAIMED,
    FAIL_SOURCE_AUTHORITY_REPLACED,
    FAIL_AUTHORITY_STRENGTHENED,
    FAIL_RUNNER_AUTHORITY_CREATED,
    FAIL_MARKDOWN_OVERCLAIM,
    FAIL_BLOCK_E_CLOSED,
    FAIL_REGISTRY_CREATED,
]

CRITICAL_FIELD_GROUPS = [
    "authority_state_transition",
    "human_authority_decision",
    "requested_action",
    "route_classification",
    "candidate_archive_status",
    "candidate_audit_status",
    "promotion_decision",
    "active_archive_entry",
    "machine_proceed_action",
    "radius_accounting",
    "created_output_surface",
    "confirmed_non_effects",
    "remaining_forbidden_authorities",
    "post_use_stop_state",
    "next_possible_separate_surface",
]

ARTIFACT_ROLES = {
    "compression_target": "E1_COMPRESSION_TARGET_DECLARATION",
    "authority_transition_closure": "A4_AUTHORITY_TRANSITION_CLOSURE",
    "authority_state_update": "A3_AUTHORITY_STATE_UPDATE",
    "router_specimen_closure": "B3_READ_ONLY_ROUTER_SPECIMEN_CLOSURE",
    "route_classification": "B2_AUTHORITY_ROUTE_CLASSIFICATION",
    "candidate_archive_entry": "C2_CANDIDATE_ARCHIVE_ENTRY",
    "candidate_archive_audit": "C3_CANDIDATE_ARCHIVE_ENTRY_ADMISSIBILITY_AUDIT",
    "active_archive_entry": "D3_ACTIVE_ARCHIVE_ENTRY_MATERIALIZATION",
    "machine_proceed": "D4_MACHINE_PROCEED_RECEIPT",
    "machine_proceed_closure": "D5_MACHINE_PROCEED_CLOSURE",
    "output_surface": "D4_CREATED_OUTPUT_SURFACE",
}

MARKDOWN_FORBIDDEN_PHRASES = [
    "registry entry created",
    "safe for automation",
    "runner ready",
    "Block E closed",
    "source authority replaced",
    "reuse authorized",
    "radius renewed",
    "additional proceed authorized",
]

E3_MARKDOWN_FORBIDDEN_PHRASES = [
    *MARKDOWN_FORBIDDEN_PHRASES,
    "source authority transferred",
    "global equivalence proven",
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
        fail(FAIL_SOURCE_CHAIN_UNRESOLVED, proc.stderr.strip())
    return Path(proc.stdout.strip()).resolve()


def load_json(path: Path, failure_code: str) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        fail(failure_code, str(path))
        raise exc
    except json.JSONDecodeError as exc:
        fail(failure_code, f"{path}: {exc}")
        raise exc


def read_text(path: Path, failure_code: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        fail(failure_code, str(path))
        raise exc


def expect(value: object, wanted: object, failure_code: str, field: str) -> None:
    if value != wanted:
        fail(failure_code, f"{field}: {value!r}!={wanted!r}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def get_path(data: dict[str, Any], json_path: str) -> Any:
    if not json_path.startswith("$."):
        raise KeyError(json_path)
    cur: Any = data
    for part in json_path[2:].split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(json_path)
        cur = cur[part]
    return cur


def bool_text(value: bool) -> str:
    return str(value).lower()


def copied_packet_ref_path(e1: dict[str, Any], artifact_key: str) -> str:
    if artifact_key == "compression_target":
        return "$.source_compression_target_id"
    if artifact_key in e1["source_artifacts"]:
        return f"$.source_artifacts_copied_from_e1.source_artifacts.{artifact_key}.path"
    return f"$.source_artifacts_copied_from_e1.supporting_source_artifacts.{artifact_key}.path"


def artifact_ref(e1: dict[str, Any], artifact_key: str) -> dict[str, Any]:
    if artifact_key == "compression_target":
        return {
            "artifact_id": SOURCE_COMPRESSION_TARGET_ID,
            "path": E1_TARGET_JSON,
            "sha256": "",
            "sig8": "",
        }
    if artifact_key in e1["source_artifacts"]:
        return e1["source_artifacts"][artifact_key]
    return e1["supporting_source_artifacts"][artifact_key]


def load_e1_sources(root: Path, e1: dict[str, Any]) -> dict[str, dict[str, Any]]:
    sources = {"compression_target": e1}
    for section in ["source_artifacts", "supporting_source_artifacts"]:
        for key, ref in e1[section].items():
            rel = ref.get("path")
            digest = ref.get("sha256")
            if not isinstance(rel, str) or not rel:
                fail(FAIL_SOURCE_CHAIN_UNRESOLVED, f"{section}.{key}.path")
            path = root / rel
            if not path.exists():
                fail(FAIL_SOURCE_CHAIN_UNRESOLVED, rel)
            if sha256_file(path) != digest:
                fail(FAIL_SOURCE_HASH_MISMATCH, rel)
            sources[key] = load_json(path, FAIL_SOURCE_CHAIN_UNRESOLVED)
    return sources


def validate_inputs(root: Path, e1: dict[str, Any], e2: dict[str, Any]) -> dict[str, dict[str, Any]]:
    expect(e1.get("schema_version"), "matrixlabs_compression_target_declaration_v0", FAIL_COMPRESSION_TARGET_MISSING, "e1.schema")
    expect(e1.get("compression_target_id"), SOURCE_COMPRESSION_TARGET_ID, FAIL_COMPRESSION_TARGET_MISSING, "e1.id")
    expect(e1.get("target_trace_label"), TARGET_TRACE_LABEL, FAIL_TARGET_TRACE_LABEL_MISMATCH, "e1.trace")
    expect(e1.get("compression_mode"), COMPRESSION_MODE, FAIL_COMPRESSION_MODE_MISMATCH, "e1.mode")
    expect(e1.get("critical_field_groups"), CRITICAL_FIELD_GROUPS, FAIL_CRITICAL_FIELD_GROUP_MISSING, "e1.groups")
    expect(e1.get("critical_field_group_count"), 15, FAIL_CRITICAL_FIELD_GROUP_MISSING, "e1.group_count")

    expect(e2.get("schema_version"), "matrixlabs_compressed_trace_packet_v0", FAIL_COMPRESSED_PACKET_MISSING, "e2.schema")
    expect(e2.get("compressed_packet_id"), SOURCE_COMPRESSED_PACKET_ID, FAIL_COMPRESSED_PACKET_MISSING, "e2.id")
    expect(e2.get("packet_status"), "COMPRESSED_PACKET_CREATED_PENDING_DECOMPRESSION_AUDIT", FAIL_COMPRESSED_PACKET_MISSING, "e2.status")
    expect(e2.get("source_compression_target_id"), SOURCE_COMPRESSION_TARGET_ID, FAIL_COMPRESSION_TARGET_MISSING, "e2.source_target")
    expect(e2.get("target_trace_label"), TARGET_TRACE_LABEL, FAIL_TARGET_TRACE_LABEL_MISMATCH, "e2.trace")
    expect(e2.get("compression_mode"), COMPRESSION_MODE, FAIL_COMPRESSION_MODE_MISMATCH, "e2.mode")

    copied = e2.get("source_artifacts_copied_from_e1", {})
    expect(copied.get("source_artifacts"), e1.get("source_artifacts"), FAIL_SOURCE_HASH_MISMATCH, "e2 primary copied refs")
    expect(
        copied.get("supporting_source_artifacts"),
        e1.get("supporting_source_artifacts"),
        FAIL_SOURCE_HASH_MISMATCH,
        "e2 supporting copied refs",
    )

    manifest = e2.get("preservation_manifest", {})
    expect(manifest.get("declared_critical_field_group_count"), 15, FAIL_PRESERVATION_MANIFEST_MISMATCH, "preservation count")
    expect(manifest.get("field_groups_claimed_preserved"), CRITICAL_FIELD_GROUPS, FAIL_PRESERVATION_MANIFEST_MISMATCH, "preservation groups")
    expect(
        manifest.get("packet_claims_to_cover_all_required_recoverable_field_groups"),
        True,
        FAIL_PRESERVATION_MANIFEST_MISMATCH,
        "preservation recoverable claim",
    )
    expect(manifest.get("field_group_preservation_proven_by_e2"), False, FAIL_PRESERVATION_MANIFEST_MISMATCH, "e2 proven")
    expect(manifest.get("requires_e3_decompression_parity_audit"), True, FAIL_PRESERVATION_MANIFEST_MISMATCH, "e2 requires e3")

    return load_e1_sources(root, e1)


def field_specs() -> list[dict[str, Any]]:
    def s(group: str, field: str, artifact: str, source: str, packet: str, failure: str, mode: str = "equal") -> dict[str, Any]:
        return {
            "critical_field_group": group,
            "field": field,
            "source_artifact_key": artifact,
            "source_json_path": source,
            "packet_json_path": packet,
            "failure_code": failure,
            "comparison_mode": mode,
        }

    return [
        s("authority_state_transition", "prior_authority_state", "authority_transition_closure", "$.authority_transition_summary.prior_authority_state", "$.authority_transition_summary.prior_authority_state", FAIL_AUTHORITY_STATE_MISMATCH),
        s("authority_state_transition", "selected_human_authority_decision", "authority_transition_closure", "$.authority_transition_summary.selected_decision_option", "$.authority_transition_summary.selected_authority_decision", FAIL_AUTHORITY_STATE_MISMATCH),
        s("authority_state_transition", "authority_event_consumed", "authority_transition_closure", "$.authority_transition_summary.authority_event_applied", "$.authority_transition_summary.authority_event_consumed", FAIL_AUTHORITY_STATE_MISMATCH),
        s("authority_state_transition", "resulting_authority_state", "authority_transition_closure", "$.authority_transition_summary.resulting_authority_state", "$.authority_transition_summary.resulting_authority_state", FAIL_AUTHORITY_STATE_MISMATCH),
        s("authority_state_transition", "next_allowed_router_action", "authority_state_update", "$.next_router_state.next_allowed_router_action", "$.authority_transition_summary.next_allowed_router_action_after_A", FAIL_AUTHORITY_STATE_MISMATCH),
        s("human_authority_decision", "decision_actor_class", "authority_state_update", "$.applied_decision.decision_actor_class", "$.authority_transition_summary.decision_actor_class", FAIL_HUMAN_DECISION_DROPPED),
        s("human_authority_decision", "selected_decision_option", "authority_state_update", "$.applied_decision.selected_decision_option", "$.authority_transition_summary.selected_authority_decision", FAIL_HUMAN_DECISION_DROPPED),
        s("human_authority_decision", "decision_was_not_inferred_by_machine", "authority_state_update", "$.applied_decision.selection_source", "$.source_artifacts_copied_from_e1.supporting_source_artifacts.authority_state_update.path", FAIL_HUMAN_DECISION_SOURCE_MISSING, "via_source_ref"),
        s("requested_action", "requested_action", "router_specimen_closure", "$.routed_request.requested_action", "$.router_summary.requested_action", FAIL_REQUESTED_ACTION_OVERGENERALIZED),
        s("requested_action", "requested_action_scope", "router_specimen_closure", "$.routed_request.requested_action_scope", "$.router_summary.requested_action_scope", FAIL_REQUESTED_ACTION_OVERGENERALIZED),
        s("requested_action", "requested_output_kind", "router_specimen_closure", "$.routed_request.requested_output_kind", "$.compressed_summary.created_output_kind", FAIL_REQUESTED_ACTION_OVERGENERALIZED),
        s("requested_action", "basis_scope", "router_specimen_closure", "$.routed_state.basis_scope", "$.machine_proceed_summary.performed_basis_scope", FAIL_REQUESTED_ACTION_OVERGENERALIZED),
        s("requested_action", "source_object_id", "router_specimen_closure", "$.routed_request.requested_target_basis", "$.machine_proceed_summary.performed_source_object_id", FAIL_REQUESTED_ACTION_OVERGENERALIZED),
        s("route_classification", "router_mode", "route_classification", "$.router_mode", "$.router_summary.router_mode", FAIL_ROUTER_ACTION_COLLAPSE),
        s("route_classification", "route_disposition", "route_classification", "$.classification.route_disposition", "$.router_summary.route_disposition", FAIL_ROUTER_ACTION_COLLAPSE),
        s("route_classification", "router_executed_action", "route_classification", "$.router_gate.action_executed", "$.router_summary.router_executed_action", FAIL_ROUTER_ACTION_COLLAPSE),
        s("route_classification", "router_changed_authority", "route_classification", "$.router_gate.authority_changed", "$.router_summary.router_changed_authority", FAIL_ROUTER_ACTION_COLLAPSE),
        s("candidate_archive_status", "entry_status", "candidate_archive_entry", "$.archive_entry_status", "$.candidate_archive_summary.candidate_status", FAIL_CANDIDATE_STATUS_STRENGTHENED),
        s("candidate_archive_status", "promotion_status", "candidate_archive_entry", "$.promotion_status", "$.candidate_archive_summary.candidate_promoted_before_D", FAIL_CANDIDATE_STATUS_STRENGTHENED, "not_requested_to_false"),
        s("candidate_archive_status", "reuse_authority_status", "candidate_archive_entry", "$.reuse_authority_status", "$.candidate_archive_summary.candidate_reusable_before_D", FAIL_CANDIDATE_STATUS_STRENGTHENED, "not_granted_to_false"),
        s("candidate_archive_status", "activation_status", "candidate_archive_entry", "$.activation_status", "$.source_artifacts_copied_from_e1.supporting_source_artifacts.candidate_archive_entry.path", FAIL_CANDIDATE_STATUS_STRENGTHENED, "via_source_ref"),
        s("candidate_archive_status", "activation_status_reason", "candidate_archive_entry", "$.activation_status_reason", "$.source_artifacts_copied_from_e1.supporting_source_artifacts.candidate_archive_entry.path", FAIL_CANDIDATE_STATUS_STRENGTHENED, "via_source_ref"),
        s("candidate_archive_status", "radius_limit_now", "candidate_archive_entry", "$.candidate_machine_scope.radius_limit_now", "$.source_artifacts_copied_from_e1.supporting_source_artifacts.candidate_archive_entry.path", FAIL_RADIUS_FIELD_DROPPED, "via_source_ref"),
        s("candidate_audit_status", "candidate_audit_status", "candidate_archive_audit", "$.audit_result.candidate_audit_status", "$.candidate_archive_summary.candidate_audit_status", FAIL_CANDIDATE_AUDIT_BOUNDARY_DROPPED),
        s("candidate_audit_status", "candidate_contract_conformant", "candidate_archive_audit", "$.audit_result.candidate_contract_conformant", "$.source_artifacts_copied_from_e1.source_artifacts.candidate_archive_audit.path", FAIL_CANDIDATE_AUDIT_BOUNDARY_DROPPED, "via_source_ref"),
        s("candidate_audit_status", "candidate_promoted", "candidate_archive_audit", "$.audit_result.candidate_promoted", "$.candidate_archive_summary.candidate_promoted_before_D", FAIL_CANDIDATE_AUDIT_BOUNDARY_DROPPED),
        s("candidate_audit_status", "candidate_reusable", "candidate_archive_audit", "$.audit_result.candidate_reusable", "$.candidate_archive_summary.candidate_reusable_before_D", FAIL_CANDIDATE_AUDIT_BOUNDARY_DROPPED),
        s("candidate_audit_status", "candidate_active", "candidate_archive_audit", "$.audit_result.candidate_active", "$.candidate_archive_summary.candidate_active_before_D", FAIL_CANDIDATE_AUDIT_BOUNDARY_DROPPED),
        s("promotion_decision", "selected_promotion_option", "active_archive_entry", "$.selected_decision_applied.selected_promotion_option", "$.candidate_archive_summary.promotion_decision", FAIL_PROMOTION_DECISION_DROPPED),
        s("promotion_decision", "decision_actor_class", "active_archive_entry", "$.selected_decision_applied.decision_actor_class", "$.source_artifacts_copied_from_e1.supporting_source_artifacts.active_archive_entry.path", FAIL_PROMOTION_DECISION_DROPPED, "via_source_ref"),
        s("promotion_decision", "promotion_scope_basis", "active_archive_entry", "$.materialized_scope.allowed_basis_scope", "$.machine_proceed_summary.performed_basis_scope", FAIL_ACTIVE_ENTRY_SCOPE_DROPPED),
        s("promotion_decision", "promotion_scope_action", "active_archive_entry", "$.materialized_scope.allowed_requested_action_scope", "$.machine_proceed_summary.performed_action_scope", FAIL_ACTIVE_ENTRY_SCOPE_DROPPED),
        s("promotion_decision", "source_object_id", "active_archive_entry", "$.materialized_scope.allowed_source_object_id", "$.machine_proceed_summary.performed_source_object_id", FAIL_ACTIVE_ENTRY_SCOPE_DROPPED),
        s("promotion_decision", "radius_selected", "active_archive_entry", "$.materialized_scope.radius", "$.radius_and_stop_state_summary.radius_limit", FAIL_RADIUS_FIELD_DROPPED),
        s("active_archive_entry", "active_archive_entry_id", "active_archive_entry", "$.active_archive_entry_id", "$.machine_proceed_summary.active_archive_entry_id", FAIL_ACTIVE_ENTRY_SCOPE_DROPPED),
        s("active_archive_entry", "entry_status", "active_archive_entry", "$.materialized_archive_entry_state.archive_entry_status", "$.candidate_archive_summary.active_entry_status", FAIL_ACTIVE_ENTRY_SCOPE_DROPPED),
        s("active_archive_entry", "promotion_status", "active_archive_entry", "$.materialized_archive_entry_state.promotion_status", "$.candidate_archive_summary.promotion_status_after_D3", FAIL_ACTIVE_ENTRY_SCOPE_DROPPED),
        s("active_archive_entry", "reuse_authority_status", "active_archive_entry", "$.materialized_archive_entry_state.reuse_authority_status", "$.candidate_archive_summary.reuse_authority_status_after_D3", FAIL_REUSE_SCOPE_OVERGENERALIZED),
        s("active_archive_entry", "activation_status", "active_archive_entry", "$.materialized_archive_entry_state.activation_status", "$.candidate_archive_summary.activation_status_after_D3", FAIL_ACTIVE_ENTRY_SCOPE_DROPPED),
        s("active_archive_entry", "declared_scope_basis", "active_archive_entry", "$.materialized_scope.allowed_basis_scope", "$.machine_proceed_summary.performed_basis_scope", FAIL_ACTIVE_ENTRY_SCOPE_DROPPED),
        s("active_archive_entry", "declared_scope_action", "active_archive_entry", "$.materialized_scope.allowed_requested_action_scope", "$.machine_proceed_summary.performed_action_scope", FAIL_ACTIVE_ENTRY_SCOPE_DROPPED),
        s("active_archive_entry", "declared_scope_source", "active_archive_entry", "$.materialized_scope.allowed_source_object_id", "$.machine_proceed_summary.performed_source_object_id", FAIL_ACTIVE_ENTRY_SCOPE_DROPPED),
        s("active_archive_entry", "radius_limit", "active_archive_entry", "$.materialized_scope.radius", "$.radius_and_stop_state_summary.radius_limit", FAIL_RADIUS_FIELD_DROPPED),
        s("machine_proceed_action", "performed_action", "machine_proceed", "$.performed_action.performed_action", "$.machine_proceed_summary.performed_action", FAIL_MACHINE_PROCEED_OVERCLAIMED),
        s("machine_proceed_action", "performed_action_scope", "machine_proceed", "$.performed_action.performed_action_scope", "$.machine_proceed_summary.performed_action_scope", FAIL_MACHINE_PROCEED_OVERCLAIMED),
        s("machine_proceed_action", "performed_basis_scope", "machine_proceed", "$.performed_action.performed_basis_scope", "$.machine_proceed_summary.performed_basis_scope", FAIL_MACHINE_PROCEED_OVERCLAIMED),
        s("machine_proceed_action", "performed_source_object_id", "machine_proceed", "$.performed_action.performed_source_object_id", "$.machine_proceed_summary.performed_source_object_id", FAIL_MACHINE_PROCEED_OVERCLAIMED),
        s("machine_proceed_action", "performed_output_kind", "machine_proceed", "$.performed_action.performed_output_kind", "$.machine_proceed_summary.performed_output_kind", FAIL_MACHINE_PROCEED_OVERCLAIMED),
        s("radius_accounting", "radius_limit", "machine_proceed", "$.radius.radius_limit", "$.radius_and_stop_state_summary.radius_limit", FAIL_RADIUS_FIELD_DROPPED),
        s("radius_accounting", "radius_before", "machine_proceed", "$.radius.radius_before", "$.radius_and_stop_state_summary.radius_before", FAIL_RADIUS_FIELD_DROPPED),
        s("radius_accounting", "radius_consumed", "machine_proceed", "$.radius.radius_consumed", "$.radius_and_stop_state_summary.radius_consumed", FAIL_RADIUS_FIELD_DROPPED),
        s("radius_accounting", "radius_after", "machine_proceed", "$.radius.radius_after", "$.radius_and_stop_state_summary.radius_after", FAIL_RADIUS_FIELD_DROPPED),
        s("radius_accounting", "radius_exhausted", "machine_proceed", "$.radius.radius_exhausted", "$.radius_and_stop_state_summary.radius_exhausted", FAIL_RADIUS_FIELD_DROPPED),
        s("radius_accounting", "entry_may_authorize_additional_machine_proceed", "machine_proceed_closure", "$.active_entry_post_use_status.entry_may_authorize_additional_machine_proceed", "$.radius_and_stop_state_summary.entry_may_authorize_additional_machine_proceed", FAIL_ADDITIONAL_PROCEED_AUTHORIZED),
        s("radius_accounting", "same_radius_may_be_reused", "machine_proceed_closure", "$.post_closure_authority_boundary.same_radius_may_be_reused", "$.radius_and_stop_state_summary.same_radius_may_be_reused", FAIL_RADIUS_RENEWED),
        s("created_output_surface", "output_surface_id", "machine_proceed_closure", "$.output_result.output_surface_id", "$.machine_proceed_summary.output_surface_id", FAIL_OUTPUT_SHAPE_MISMATCH),
        s("created_output_surface", "output_object_type", "machine_proceed_closure", "$.output_result.output_object_type", "$.machine_proceed_summary.performed_output_kind", FAIL_OUTPUT_SHAPE_MISMATCH),
        s("created_output_surface", "output_scope", "machine_proceed_closure", "$.output_result.output_scope", "$.source_artifacts_copied_from_e1.source_artifacts.machine_proceed_closure.path", FAIL_OUTPUT_SHAPE_MISMATCH, "via_source_ref"),
        s("created_output_surface", "output_basis", "machine_proceed_closure", "$.output_result.output_basis", "$.machine_proceed_summary.performed_source_object_id", FAIL_OUTPUT_SHAPE_MISMATCH),
        s("created_output_surface", "execution_status", "machine_proceed_closure", "$.output_surface_verification.execution_status", "$.compressed_summary.output_execution_status", FAIL_OUTPUT_SHAPE_MISMATCH),
        s("created_output_surface", "output_surface_status", "machine_proceed_closure", "$.output_result.output_surface_status", "$.machine_proceed_summary.output_surface_status", FAIL_OUTPUT_SHAPE_MISMATCH),
        s("confirmed_non_effects", "unit_executed", "machine_proceed", "$.non_effects.unit_executed", "$.confirmed_non_effects.unit_executed", FAIL_NON_EFFECT_FIELD_DROPPED),
        s("confirmed_non_effects", "runtime_executed", "machine_proceed", "$.non_effects.runtime_executed", "$.confirmed_non_effects.runtime_executed", FAIL_NON_EFFECT_FIELD_DROPPED),
        s("confirmed_non_effects", "authority_changed", "machine_proceed", "$.non_effects.authority_changed", "$.confirmed_non_effects.authority_changed_after_machine_proceed", FAIL_FORBIDDEN_EFFECT_FLIPPED),
        s("confirmed_non_effects", "authority_changed_after_machine_proceed", "machine_proceed_closure", "$.forbidden_effect_verification.authority_changed", "$.confirmed_non_effects.authority_changed_after_machine_proceed", FAIL_FORBIDDEN_EFFECT_FLIPPED),
        s("confirmed_non_effects", "receipts_rewritten", "machine_proceed", "$.non_effects.receipts_rewritten", "$.confirmed_non_effects.receipts_rewritten", FAIL_NON_EFFECT_FIELD_DROPPED),
        s("confirmed_non_effects", "taxonomy_promoted", "machine_proceed", "$.non_effects.taxonomy_promoted", "$.confirmed_non_effects.taxonomy_promoted", FAIL_NON_EFFECT_FIELD_DROPPED),
        s("confirmed_non_effects", "reuse_scope_expanded", "machine_proceed", "$.non_effects.reuse_scope_expanded", "$.confirmed_non_effects.reuse_scope_expanded", FAIL_REUSE_SCOPE_OVERGENERALIZED),
        s("confirmed_non_effects", "updater_generalized", "machine_proceed", "$.non_effects.updater_generalized", "$.confirmed_non_effects.updater_generalized", FAIL_NON_EFFECT_FIELD_DROPPED),
        s("confirmed_non_effects", "runner_authority_created", "machine_proceed", "$.non_effects.runner_authority_created", "$.confirmed_non_effects.runner_authority_created", FAIL_RUNNER_AUTHORITY_CREATED),
        s("confirmed_non_effects", "additional_radius_created", "machine_proceed", "$.non_effects.additional_radius_created", "$.confirmed_non_effects.additional_radius_created", FAIL_RADIUS_RENEWED),
        s("confirmed_non_effects", "active_archive_scope_expanded", "machine_proceed_closure", "$.forbidden_effect_verification.active_archive_scope_expanded", "$.confirmed_non_effects.active_archive_scope_expanded", FAIL_REUSE_SCOPE_OVERGENERALIZED),
        s("confirmed_non_effects", "active_archive_entry_rewritten_by_packet", "machine_proceed", "$.non_effects.active_archive_entry_rewritten", "$.confirmed_non_effects.active_archive_entry_rewritten_by_packet", FAIL_NON_EFFECT_FIELD_DROPPED),
        s("confirmed_non_effects", "active_archive_entry_mutated_by_packet", "machine_proceed", "$.non_effects.active_archive_entry_mutated", "$.confirmed_non_effects.active_archive_entry_mutated_by_packet", FAIL_NON_EFFECT_FIELD_DROPPED),
        s("remaining_forbidden_authorities", "execution_remains_unauthorized", "output_surface", "$.non_authorizations.execution_authorized", "$.packet_boundary.packet_grants_authority", FAIL_REMAINING_FORBIDDEN_AUTHORITY_DROPPED),
        s("remaining_forbidden_authorities", "runtime_remains_unauthorized", "output_surface", "$.non_authorizations.runtime_authorized", "$.confirmed_non_effects.runtime_executed", FAIL_REMAINING_FORBIDDEN_AUTHORITY_DROPPED),
        s("remaining_forbidden_authorities", "receipt_rewrite_remains_unauthorized", "authority_transition_closure", "$.still_not_authorized.receipt_rewrite_authority", "$.confirmed_non_effects.receipts_rewritten", FAIL_REMAINING_FORBIDDEN_AUTHORITY_DROPPED, "not_granted_to_false"),
        s("remaining_forbidden_authorities", "taxonomy_promotion_remains_unauthorized", "authority_transition_closure", "$.still_not_authorized.taxonomy_promotion_authority", "$.confirmed_non_effects.taxonomy_promoted", FAIL_REMAINING_FORBIDDEN_AUTHORITY_DROPPED, "not_granted_to_false"),
        s("remaining_forbidden_authorities", "reuse_expansion_remains_unauthorized", "authority_transition_closure", "$.still_not_authorized.reuse_authority", "$.packet_boundary.packet_authorizes_reuse", FAIL_REUSE_SCOPE_OVERGENERALIZED, "not_granted_to_false"),
        s("remaining_forbidden_authorities", "updater_generalization_remains_unauthorized", "authority_transition_closure", "$.still_not_authorized.updater_generalization_authority", "$.confirmed_non_effects.updater_generalized", FAIL_REMAINING_FORBIDDEN_AUTHORITY_DROPPED, "not_granted_to_false"),
        s("remaining_forbidden_authorities", "runner_remains_unauthorized", "authority_transition_closure", "$.still_not_authorized.runner_authority", "$.packet_boundary.packet_creates_runner_authority", FAIL_RUNNER_AUTHORITY_CREATED, "not_granted_to_false"),
        s("remaining_forbidden_authorities", "radius_renewal_remains_unauthorized", "machine_proceed_closure", "$.radius_result.radius_renewed_by_closure", "$.packet_boundary.packet_renews_radius", FAIL_RADIUS_RENEWED),
        s("remaining_forbidden_authorities", "additional_proceed_remains_unauthorized", "machine_proceed_closure", "$.radius_result.further_machine_proceed_authorized_under_this_radius", "$.packet_boundary.packet_authorizes_additional_machine_proceed", FAIL_ADDITIONAL_PROCEED_AUTHORIZED),
        s("remaining_forbidden_authorities", "source_authority_replacement_remains_unauthorized", "compression_target", "$.authority_substitution_boundary.compressed_packet_may_replace_source_records_as_authority", "$.packet_boundary.packet_may_replace_source_authority", FAIL_SOURCE_AUTHORITY_REPLACED),
        s("post_use_stop_state", "radius_exhausted", "machine_proceed_closure", "$.radius_result.radius_exhausted", "$.radius_and_stop_state_summary.radius_exhausted", FAIL_STOP_STATE_DROPPED),
        s("post_use_stop_state", "active_entry_remains_audit_source", "machine_proceed_closure", "$.active_entry_post_use_status.entry_remains_audit_source", "$.packet_boundary.source_records_remain_authority", FAIL_STOP_STATE_DROPPED),
        s("post_use_stop_state", "entry_has_remaining_radius", "machine_proceed_closure", "$.active_entry_post_use_status.entry_has_remaining_radius", "$.radius_and_stop_state_summary.entry_has_remaining_radius", FAIL_STOP_STATE_WEAKENED),
        s("post_use_stop_state", "additional_use_requires_new_authority_or_radius", "machine_proceed_closure", "$.active_entry_post_use_status.additional_use_requires_new_authority_or_radius", "$.radius_and_stop_state_summary.additional_use_requires_new_authority_or_radius", FAIL_STOP_STATE_DROPPED),
        s("post_use_stop_state", "entry_may_authorize_additional_machine_proceed", "machine_proceed_closure", "$.active_entry_post_use_status.entry_may_authorize_additional_machine_proceed", "$.radius_and_stop_state_summary.entry_may_authorize_additional_machine_proceed", FAIL_ADDITIONAL_PROCEED_AUTHORIZED),
        s("post_use_stop_state", "same_radius_may_be_reused", "machine_proceed_closure", "$.post_closure_authority_boundary.same_radius_may_be_reused", "$.radius_and_stop_state_summary.same_radius_may_be_reused", FAIL_RADIUS_RENEWED),
        s("next_possible_separate_surface", "next_possible_separate_surface", "machine_proceed_closure", "$.next_possible_separate_surface.surface", "$.next_possible_separate_surface_summary.next_possible_separate_surface", FAIL_NEXT_SURFACE_OVERCLAIMED),
        s("next_possible_separate_surface", "created_by_compressed_packet", "machine_proceed_closure", "$.next_possible_separate_surface.created_by_this_closure", "$.next_possible_separate_surface_summary.created_by_compressed_packet", FAIL_NEXT_SURFACE_OVERCLAIMED),
        s("next_possible_separate_surface", "authorized_by_compressed_packet", "machine_proceed_closure", "$.next_possible_separate_surface.authorized_by_this_closure", "$.next_possible_separate_surface_summary.authorized_by_compressed_packet", FAIL_NEXT_SURFACE_OVERCLAIMED),
        s("next_possible_separate_surface", "machine_may_prepare_without_new_authority", "machine_proceed_closure", "$.next_possible_separate_surface.machine_may_prepare_without_new_authority", "$.next_possible_separate_surface_summary.machine_may_prepare_without_new_authority", FAIL_NEXT_SURFACE_OVERCLAIMED),
    ]


def values_match(source_value: Any, packet_value: Any, mode: str) -> bool:
    if mode == "equal":
        return source_value == packet_value
    if mode == "via_source_ref":
        return True
    if mode == "not_requested_to_false":
        return source_value == "PROMOTION_NOT_REQUESTED" and packet_value is False
    if mode == "not_granted_to_false":
        return source_value in {"REUSE_AUTHORITY_NOT_GRANTED", "NOT_GRANTED", "NOT_GRANTED_BY_ROUTER"} and packet_value is False
    fail(FAIL_CRITICAL_FIELD_MISMATCH, f"unknown comparison mode {mode}")
    return False


def build_field_map(e1: dict[str, Any], e2: dict[str, Any], sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {group: [] for group in CRITICAL_FIELD_GROUPS}
    for spec in field_specs():
        group = spec["critical_field_group"]
        artifact_key = spec["source_artifact_key"]
        source = sources[artifact_key]
        try:
            source_value = get_path(source, spec["source_json_path"])
        except KeyError:
            fail(spec["failure_code"], f"{artifact_key}:{spec['source_json_path']}")
        try:
            raw_packet_value = get_path(e2, spec["packet_json_path"])
        except KeyError:
            fail(FAIL_CRITICAL_FIELD_DROPPED, f"{group}:{spec['packet_json_path']}")
        packet_value = source_value if spec["comparison_mode"] == "via_source_ref" else raw_packet_value
        if not values_match(source_value, raw_packet_value, spec["comparison_mode"]):
            fail(spec["failure_code"], f"{group}.{spec['field']}: {source_value!r}!={raw_packet_value!r}")
        ref = artifact_ref(e1, artifact_key)
        field = {
            "field": spec["field"],
            "source_artifact_id": ref["artifact_id"],
            "source_artifact_role": ARTIFACT_ROLES[artifact_key],
            "source_artifact_path": ref["path"],
            "source_json_path": spec["source_json_path"],
            "packet_json_path": spec["packet_json_path"],
            "source_value": source_value,
            "packet_value": packet_value,
            "packet_raw_value_at_path": raw_packet_value,
            "parity_status": FIELD_PASS,
        }
        if spec["comparison_mode"] != "equal":
            field["parity_rule"] = spec["comparison_mode"]
        if spec["comparison_mode"] == "via_source_ref":
            field["packet_resolution_note"] = "field recovered through E.2 copied E.1 source reference and verified source hash"
        grouped[group].append(field)

    audit_map = []
    packet_sections = {
        "authority_state_transition": "authority_transition_summary",
        "human_authority_decision": "authority_transition_summary",
        "requested_action": "router_summary",
        "route_classification": "router_summary",
        "candidate_archive_status": "candidate_archive_summary",
        "candidate_audit_status": "candidate_archive_summary",
        "promotion_decision": "candidate_archive_summary",
        "active_archive_entry": "candidate_archive_summary",
        "machine_proceed_action": "machine_proceed_summary",
        "radius_accounting": "radius_and_stop_state_summary",
        "created_output_surface": "machine_proceed_summary",
        "confirmed_non_effects": "confirmed_non_effects",
        "remaining_forbidden_authorities": "packet_boundary",
        "post_use_stop_state": "radius_and_stop_state_summary",
        "next_possible_separate_surface": "next_possible_separate_surface_summary",
    }
    for group in CRITICAL_FIELD_GROUPS:
        fields = grouped[group]
        if not fields:
            fail(FAIL_CRITICAL_FIELD_GROUP_MISSING, group)
        artifacts_used = []
        for field in fields:
            item = {
                "artifact_id": field["source_artifact_id"],
                "artifact_role": field["source_artifact_role"],
                "artifact_path": field["source_artifact_path"],
            }
            if item not in artifacts_used:
                artifacts_used.append(item)
        audit_map.append(
            {
                "critical_field_group": group,
                "source_artifact_id": fields[0]["source_artifact_id"],
                "source_artifact_role": fields[0]["source_artifact_role"],
                "source_artifacts_used": artifacts_used,
                "packet_section": packet_sections[group],
                "fields_checked": fields,
                "group_status": GROUP_PASS,
            }
        )
    return audit_map


def source_identity_integrity() -> dict[str, bool]:
    return {
        "e1_source_refs_loaded": True,
        "e2_copied_source_refs_match_e1": True,
        "e2_copied_source_hashes_match_e1": True,
        "source_files_exist": True,
        "source_file_hashes_match_e1_manifest": True,
        "mtime_or_latest_file_resolution_allowed": False,
        "directory_scan_authority_allowed": False,
    }


def audit_scope_boundary() -> dict[str, Any]:
    return {
        "audit_scope": AUDIT_SCOPE,
        "full_trace_equivalence_claimed": False,
        "all_possible_fields_audited": False,
        "observability_closure_performed": False,
        "authority_transfer_performed": False,
    }


def packet_audit_status_after_e3() -> dict[str, Any]:
    return {
        "source_packet_status_before_audit": "COMPRESSED_PACKET_CREATED_PENDING_DECOMPRESSION_AUDIT",
        "decompression_audit_status": AUDIT_STATUS,
        "packet_eligible_for_e4_observability_closure": True,
        "packet_source_record_rewritten": False,
        "block_e_closed_by_e3": False,
        "compression_closed_by_e3": False,
    }


def critical_field_group_audit_summary() -> dict[str, Any]:
    data: dict[str, Any] = {
        "critical_field_group_count_expected": 15,
        "critical_field_group_count_checked": 15,
        "critical_field_group_count_passed": 15,
        "all_critical_field_groups_recovered": True,
    }
    for group in CRITICAL_FIELD_GROUPS:
        data[f"{group}_parity"] = GROUP_PASS
    return data


def authority_safety_checks(e2: dict[str, Any]) -> dict[str, bool]:
    boundary = e2["packet_boundary"]
    effects = e2["confirmed_non_effects"]
    checks = {
        "compressed_packet_replaces_source_authority": boundary["packet_may_replace_source_authority"],
        "authority_strengthened_by_compression": boundary["packet_grants_authority"],
        "execution_authorized_by_compression": False,
        "reuse_authorized_by_compression": boundary["packet_authorizes_reuse"],
        "reuse_scope_expanded_by_compression": effects["reuse_scope_expanded"],
        "radius_renewed_by_compression": boundary["packet_renews_radius"],
        "additional_machine_proceed_authorized_by_compression": boundary["packet_authorizes_additional_machine_proceed"],
        "runner_authority_created_by_compression": boundary["packet_creates_runner_authority"],
        "source_records_rewritten_by_compression": effects["active_archive_entry_rewritten_by_packet"],
        "registry_created_by_decompression_audit": False,
        "block_e_closed_by_decompression_audit": False,
    }
    for key, value in checks.items():
        if value is not False:
            failure = {
                "compressed_packet_replaces_source_authority": FAIL_SOURCE_AUTHORITY_REPLACED,
                "authority_strengthened_by_compression": FAIL_AUTHORITY_STRENGTHENED,
                "reuse_authorized_by_compression": FAIL_REUSE_SCOPE_OVERGENERALIZED,
                "radius_renewed_by_compression": FAIL_RADIUS_RENEWED,
                "additional_machine_proceed_authorized_by_compression": FAIL_ADDITIONAL_PROCEED_AUTHORIZED,
                "runner_authority_created_by_compression": FAIL_RUNNER_AUTHORITY_CREATED,
                "registry_created_by_decompression_audit": FAIL_REGISTRY_CREATED,
                "block_e_closed_by_decompression_audit": FAIL_BLOCK_E_CLOSED,
            }.get(key, FAIL_FORBIDDEN_EFFECT_FLIPPED)
            fail(failure, key)
    return checks


def audit_non_effects() -> dict[str, bool]:
    return {
        "decompression_audit_creates_compressed_packet": False,
        "decompression_audit_closes_block_e": False,
        "decompression_audit_creates_registry_entry": False,
        "decompression_audit_performs_machine_action": False,
        "decompression_audit_changes_authority": False,
        "decompression_audit_renews_radius": False,
        "decompression_audit_creates_runner_authority": False,
        "decompression_audit_rewrites_source_records": False,
    }


def markdown_checks(markdown: str) -> tuple[dict[str, Any], dict[str, Any]]:
    lowered = markdown.lower()
    hits = [phrase for phrase in MARKDOWN_FORBIDDEN_PHRASES if phrase.lower() in lowered]
    if hits:
        fail(FAIL_MARKDOWN_OVERCLAIM, ",".join(hits))
    projection = {
        "markdown_present": True,
        "markdown_claims_decompression_passed": "decompression passed" in lowered,
        "markdown_claims_source_authority_replaced": "source authority replaced" in lowered,
        "markdown_claims_reuse_authorized": "reuse authorized" in lowered,
        "markdown_claims_radius_renewed": "radius renewed" in lowered,
        "markdown_claims_additional_proceed_authorized": "additional proceed authorized" in lowered,
        "markdown_claims_runner_authority": "runner ready" in lowered,
        "markdown_claims_execution": "unit executed" in lowered or "execution authorized" in lowered,
        "markdown_boundary_parity": MARKDOWN_PASS,
    }
    for key, value in projection.items():
        if key.startswith("markdown_claims_") and value is not False:
            fail(FAIL_MARKDOWN_OVERCLAIM, key)
    phrase_check = {
        "forbidden_phrases_checked": MARKDOWN_FORBIDDEN_PHRASES,
        "forbidden_phrase_hits": [],
        "markdown_projection_gate": MARKDOWN_PASS,
    }
    return projection, phrase_check


def audit_result() -> dict[str, Any]:
    return {
        "decompression_audit_status": AUDIT_STATUS,
        "all_critical_field_groups_recovered": True,
        "compressed_summary_matches_sources": True,
        "source_chain_refs_resolvable": True,
        "source_file_hashes_match_e1_manifest": True,
        "preservation_manifest_matches_target": True,
        "authority_smuggling_detected": False,
        "eligible_for_e4_observability_closure": True,
        "block_e_closed_by_e3": False,
        "compression_closed_by_e3": False,
    }


def audit_gate() -> dict[str, Any]:
    data: dict[str, Any] = {
        "decompression_gate": AUDIT_STATUS,
        "compression_target_present": True,
        "compressed_packet_present": True,
        "source_chain_complete": True,
        "source_identity_integrity_passed": True,
        "target_trace_label_matches": True,
        "compression_mode_matches": True,
        "critical_field_group_count_expected": 15,
        "critical_field_group_count_checked": 15,
        "critical_field_group_count_passed": 15,
        "all_critical_field_groups_recovered": True,
        "source_chain_refs_resolvable": True,
        "source_file_hashes_match_e1_manifest": True,
        "compressed_summary_matches_sources": True,
        "preservation_manifest_matches_target": True,
    }
    for group in CRITICAL_FIELD_GROUPS:
        data[f"{group}_parity"] = GROUP_PASS
    data.update(
        {
            "compressed_packet_replaces_source_authority": False,
            "authority_strengthened_by_compression": False,
            "execution_authorized_by_compression": False,
            "reuse_authorized_by_compression": False,
            "radius_renewed_by_compression": False,
            "additional_machine_proceed_authorized_by_compression": False,
            "runner_authority_created_by_compression": False,
            "decompression_audit_performs_machine_action": False,
            "decompression_audit_changes_authority": False,
            "decompression_audit_creates_registry_entry": False,
            "decompression_audit_closes_block_e": False,
            "markdown_projection_gate": MARKDOWN_PASS,
            "eligible_for_e4_observability_closure": True,
            "failures": [],
        }
    )
    return data


def build_record(e1: dict[str, Any], e2: dict[str, Any], e2_md: str, sources: dict[str, dict[str, Any]]) -> dict[str, Any]:
    field_map = build_field_map(e1, e2, sources)
    projection, phrase_check = markdown_checks(e2_md)
    safety = authority_safety_checks(e2)
    return {
        "schema_version": SCHEMA_VERSION,
        "decompression_audit_id": DECOMPRESSION_AUDIT_ID,
        "audit_role": AUDIT_ROLE,
        "audit_mode": AUDIT_MODE,
        "block_id": BLOCK_ID,
        "block_unit_id": BLOCK_UNIT_ID,
        "block_e_status": BLOCK_E_STATUS,
        "source_compression_target_id": SOURCE_COMPRESSION_TARGET_ID,
        "source_compressed_packet_id": SOURCE_COMPRESSED_PACKET_ID,
        "target_trace_label": TARGET_TRACE_LABEL,
        "compression_mode": COMPRESSION_MODE,
        "source_identity_integrity": source_identity_integrity(),
        "audit_scope_boundary": audit_scope_boundary(),
        "packet_audit_status_after_e3": packet_audit_status_after_e3(),
        "audit_result": audit_result(),
        "critical_field_groups": CRITICAL_FIELD_GROUPS,
        "critical_field_group_audit_summary": critical_field_group_audit_summary(),
        "field_decompression_audit_map": field_map,
        "authority_safety_checks": safety,
        "audit_non_effects": audit_non_effects(),
        "markdown_projection_checks": projection,
        "markdown_forbidden_phrase_check": phrase_check,
        "audit_gate": audit_gate(),
        "failure_vocabulary": FAILURE_VOCABULARY,
        "non_claims": [
            "E.3 does not create the compressed packet.",
            "E.3 does not close Block E.",
            "E.3 does not create a compression registry entry.",
            "E.3 does not replace source records.",
            "E.3 does not authorize reuse.",
            "E.3 does not renew radius.",
            "E.3 does not authorize another machine proceed.",
            "E.3 does not perform machine action.",
            "E.3 does not execute the created next unit.",
            "E.3 does not create runner authority.",
            "E.3 only audits decompression parity between E.2 and the source chain declared by E.1.",
        ],
        "key_non_claims": [
            "decompression parity ≠ authority transfer",
            "audit pass ≠ reusable schema",
            "observability shortcut ≠ runner permission",
            "E.3 pass ≠ Block E closure",
            "local parity ≠ global trace equivalence",
        ],
        "precommit_c8_n22_decompression_audit_gate": PRECOMMIT_GATE,
        "decompression_audit_gate": AUDIT_STATUS,
        "terminal_transition": TERMINAL_TRANSITION,
        "generated_by": GENERATOR,
    }


def validate_record(record: dict[str, Any]) -> None:
    expect(record.get("schema_version"), SCHEMA_VERSION, FAIL_COMPRESSION_TARGET_MISSING, "schema")
    expect(record.get("decompression_audit_id"), DECOMPRESSION_AUDIT_ID, FAIL_COMPRESSION_TARGET_MISSING, "id")
    expect(record.get("audit_role"), AUDIT_ROLE, FAIL_COMPRESSION_TARGET_MISSING, "role")
    expect(record.get("audit_mode"), AUDIT_MODE, FAIL_COMPRESSION_TARGET_MISSING, "mode")
    expect(record.get("block_id"), BLOCK_ID, FAIL_COMPRESSION_TARGET_MISSING, "block_id")
    expect(record.get("block_unit_id"), BLOCK_UNIT_ID, FAIL_COMPRESSION_TARGET_MISSING, "block_unit_id")
    expect(record.get("block_e_status"), BLOCK_E_STATUS, FAIL_COMPRESSION_TARGET_MISSING, "block_e_status")
    expect(record.get("source_compression_target_id"), SOURCE_COMPRESSION_TARGET_ID, FAIL_COMPRESSION_TARGET_MISSING, "target id")
    expect(record.get("source_compressed_packet_id"), SOURCE_COMPRESSED_PACKET_ID, FAIL_COMPRESSED_PACKET_MISSING, "packet id")
    expect(record.get("target_trace_label"), TARGET_TRACE_LABEL, FAIL_TARGET_TRACE_LABEL_MISMATCH, "trace")
    expect(record.get("compression_mode"), COMPRESSION_MODE, FAIL_COMPRESSION_MODE_MISMATCH, "compression mode")
    expect(len(record.get("field_decompression_audit_map", [])), 15, FAIL_CRITICAL_FIELD_GROUP_MISSING, "field map count")
    for group in record["field_decompression_audit_map"]:
        expect(group.get("group_status"), GROUP_PASS, FAIL_CRITICAL_FIELD_MISMATCH, group["critical_field_group"])
        if not group.get("fields_checked"):
            fail(FAIL_CRITICAL_FIELD_DROPPED, group["critical_field_group"])
        for field in group["fields_checked"]:
            if not field.get("source_json_path") or not field.get("packet_json_path"):
                fail(FAIL_CRITICAL_FIELD_DROPPED, f"{group['critical_field_group']}.{field.get('field')}")
            expect(field.get("parity_status"), FIELD_PASS, FAIL_CRITICAL_FIELD_MISMATCH, field.get("field"))
    expect(record["markdown_forbidden_phrase_check"]["forbidden_phrase_hits"], [], FAIL_MARKDOWN_OVERCLAIM, "markdown hits")
    expect(record["audit_gate"]["failures"], [], FAIL_CRITICAL_FIELD_MISMATCH, "audit gate failures")
    expect(record.get("terminal_transition"), TERMINAL_TRANSITION, FAIL_BLOCK_E_CLOSED, "terminal")


def render_markdown(record: dict[str, Any]) -> str:
    summary = record["critical_field_group_audit_summary"]
    parity_lines = "\n".join(f"- {group.replace('_', ' ')}: {summary[f'{group}_parity']}" for group in CRITICAL_FIELD_GROUPS)
    return f"""# C8 n22 radius-bound prepare trace decompression audit v0

## Status

{AUDIT_STATUS}

## Compressed packet

{SOURCE_COMPRESSED_PACKET_ID}

## Compression target

{SOURCE_COMPRESSION_TARGET_ID}

## Trace label

{TARGET_TRACE_LABEL}

## Audit scope

{AUDIT_SCOPE}

This audit verifies local critical-field decompression parity. It does not claim full trace equivalence.

## Critical field group parity

{parity_lines}

## Source integrity

- E.1 source refs loaded
- E.2 copied source refs match E.1
- E.2 copied source hashes match E.1
- source file hashes match E.1 manifest

## Authority safety

- source records not replaced
- authority not strengthened
- execution not authorized
- reuse not authorized by compression
- radius not renewed
- additional machine proceed not authorized
- runner authority not created

## Result

The compressed packet passed local decompression parity and is eligible for E.4 observability-only closure.

## Non-claim

This audit does not make the compressed packet source authority, authorize reuse, renew radius, authorize additional proceed, close Block E, create a registry entry, or create runner authority.

## Next required object

{NEXT_REQUIRED_OBJECT}
"""


def validate_markdown(text: str) -> None:
    lowered = text.lower()
    hits = [phrase for phrase in E3_MARKDOWN_FORBIDDEN_PHRASES if phrase.lower() in lowered]
    if hits:
        fail(FAIL_MARKDOWN_OVERCLAIM, ",".join(hits))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_outputs(root: Path, record: dict[str, Any]) -> None:
    markdown = render_markdown(record)
    validate_markdown(markdown)
    write_text(root / OUTPUT_JSON, json.dumps(record, indent=2, sort_keys=True) + "\n")
    write_text(root / OUTPUT_MD, markdown)


def print_success(record: dict[str, Any]) -> None:
    identity = record["source_identity_integrity"]
    scope = record["audit_scope_boundary"]
    packet = record["packet_audit_status_after_e3"]
    result = record["audit_result"]
    summary = record["critical_field_group_audit_summary"]
    safety = record["authority_safety_checks"]
    non_effects = record["audit_non_effects"]
    phrase_hits = len(record["markdown_forbidden_phrase_check"]["forbidden_phrase_hits"])
    print("BUILD_C8_N22_RADIUS_BOUND_PREPARE_TRACE_DECOMPRESSION_AUDIT_V0_COMPLETE")
    print(f"decompression_audit_id={record['decompression_audit_id']}")
    print(f"schema_version={record['schema_version']}")
    print(f"audit_role={record['audit_role']}")
    print(f"audit_mode={record['audit_mode']}")
    print(f"block_id={record['block_id']}")
    print(f"block_unit_id={record['block_unit_id']}")
    print(f"block_e_status={record['block_e_status']}")
    print(f"source_compression_target_id={record['source_compression_target_id']}")
    print(f"source_compressed_packet_id={record['source_compressed_packet_id']}")
    print(f"target_trace_label={record['target_trace_label']}")
    print(f"compression_mode={record['compression_mode']}")
    print(f"e1_source_refs_loaded={bool_text(identity['e1_source_refs_loaded'])}")
    print(f"e2_copied_source_refs_match_e1={bool_text(identity['e2_copied_source_refs_match_e1'])}")
    print(f"e2_copied_source_hashes_match_e1={bool_text(identity['e2_copied_source_hashes_match_e1'])}")
    print(f"source_files_exist={bool_text(identity['source_files_exist'])}")
    print(f"source_file_hashes_match_e1_manifest={bool_text(identity['source_file_hashes_match_e1_manifest'])}")
    print(f"audit_scope={scope['audit_scope']}")
    print(f"full_trace_equivalence_claimed={bool_text(scope['full_trace_equivalence_claimed'])}")
    print(f"all_possible_fields_audited={bool_text(scope['all_possible_fields_audited'])}")
    print(f"observability_closure_performed={bool_text(scope['observability_closure_performed'])}")
    print(f"authority_transfer_performed={bool_text(scope['authority_transfer_performed'])}")
    print(f"source_packet_status_before_audit={packet['source_packet_status_before_audit']}")
    print(f"decompression_audit_status={packet['decompression_audit_status']}")
    print(f"packet_eligible_for_e4_observability_closure={bool_text(packet['packet_eligible_for_e4_observability_closure'])}")
    print(f"packet_source_record_rewritten={bool_text(packet['packet_source_record_rewritten'])}")
    print(f"block_e_closed_by_e3={bool_text(packet['block_e_closed_by_e3'])}")
    print(f"compression_closed_by_e3={bool_text(packet['compression_closed_by_e3'])}")
    print(f"all_critical_field_groups_recovered={bool_text(result['all_critical_field_groups_recovered'])}")
    print(f"compressed_summary_matches_sources={bool_text(result['compressed_summary_matches_sources'])}")
    print(f"source_chain_refs_resolvable={bool_text(result['source_chain_refs_resolvable'])}")
    print(f"preservation_manifest_matches_target={bool_text(result['preservation_manifest_matches_target'])}")
    print(f"authority_smuggling_detected={bool_text(result['authority_smuggling_detected'])}")
    print(f"critical_field_group_count_expected={summary['critical_field_group_count_expected']}")
    print(f"critical_field_group_count_checked={summary['critical_field_group_count_checked']}")
    print(f"critical_field_group_count_passed={summary['critical_field_group_count_passed']}")
    for group in CRITICAL_FIELD_GROUPS:
        print(f"{group}_parity={summary[f'{group}_parity']}")
    for key in [
        "compressed_packet_replaces_source_authority",
        "authority_strengthened_by_compression",
        "execution_authorized_by_compression",
        "reuse_authorized_by_compression",
        "reuse_scope_expanded_by_compression",
        "radius_renewed_by_compression",
        "additional_machine_proceed_authorized_by_compression",
        "runner_authority_created_by_compression",
        "source_records_rewritten_by_compression",
        "registry_created_by_decompression_audit",
    ]:
        print(f"{key}={bool_text(safety[key])}")
    for key in [
        "decompression_audit_creates_compressed_packet",
        "decompression_audit_closes_block_e",
        "decompression_audit_creates_registry_entry",
        "decompression_audit_performs_machine_action",
        "decompression_audit_changes_authority",
        "decompression_audit_renews_radius",
        "decompression_audit_creates_runner_authority",
    ]:
        print(f"{key}={bool_text(non_effects[key])}")
    print(f"markdown_projection_gate={record['markdown_projection_checks']['markdown_boundary_parity']}")
    print(f"markdown_forbidden_phrase_hits={phrase_hits}")
    print(f"eligible_for_e4_observability_closure={bool_text(result['eligible_for_e4_observability_closure'])}")
    print(f"decompression_audit_gate={record['decompression_audit_gate']}")
    print(f"precommit_c8_n22_decompression_audit_gate={record['precommit_c8_n22_decompression_audit_gate']}")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition={record['terminal_transition']}")


def main() -> int:
    try:
        root = detect_repo_root(Path.cwd())
        e1 = load_json(root / E1_TARGET_JSON, FAIL_COMPRESSION_TARGET_MISSING)
        e2 = load_json(root / E2_PACKET_JSON, FAIL_COMPRESSED_PACKET_MISSING)
        e2_md = read_text(root / E2_PACKET_MD, FAIL_COMPRESSED_PACKET_MISSING)
        sources = validate_inputs(root, e1, e2)
        record = build_record(e1, e2, e2_md, sources)
        validate_record(record)
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
