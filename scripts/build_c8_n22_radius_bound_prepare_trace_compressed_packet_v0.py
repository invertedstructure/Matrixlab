#!/usr/bin/env python3

"""Build C8 n22 radius-bound prepare trace compressed packet v0.

E.2 creates a bounded compressed observability packet from the E.1 target.
It does not prove decompression parity, close compression, create a registry,
authorize reuse, renew radius, replace source records, execute runtime, or
create runner authority.
"""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_radius_bound_prepare_trace_compressed_packet_v0.py"
E1_TARGET_JSON = "docs/matrixlabs/compression/c8_n22_authority_action_trace_compression_target_v0.json"
OUTPUT_JSON = "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_compressed_packet_v0.json"
OUTPUT_MD = "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_compressed_packet_v0.md"

SCHEMA_VERSION = "matrixlabs_compressed_trace_packet_v0"
COMPRESSED_PACKET_ID = "c8.n22.radius_bound_prepare_trace.compressed_packet.v0"
PACKET_ROLE = "COMPRESSED_OBSERVABILITY_PACKET"
PACKET_STATUS = "COMPRESSED_PACKET_CREATED_PENDING_DECOMPRESSION_AUDIT"
BLOCK_ID = "BLOCK_E"
BLOCK_UNIT_ID = "E2_COMPRESSED_SPECIMEN_PACKET"
BLOCK_E_STATUS = "BLOCK_E_COMPRESSED_PACKET_CREATED"
TARGET_TRACE_LABEL = "C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0"
COMPRESSION_MODE = "OBSERVABILITY_COMPRESSION_ONLY"
SOURCE_COMPRESSION_TARGET_ID = "c8.n22.authority_action_trace.compression_target.v0"
COMPRESSED_PACKET_GATE = "COMPRESSED_PACKET_PASS_CREATED_WITH_BOUNDARY"
PRECOMMIT_GATE = "PASS"
TERMINAL_TRANSITION = "ADVANCE(E3_DECOMPRESSION_PARITY_AUDIT_PENDING)"
NEXT_REQUIRED_OBJECT = "c8_n22_radius_bound_prepare_trace_decompression_audit_v0"

FAIL_COMPRESSION_TARGET_MISSING = "COMPRESSED_PACKET_FAIL_COMPRESSION_TARGET_MISSING"
FAIL_TARGET_LABEL_MISSING = "COMPRESSED_PACKET_FAIL_TARGET_LABEL_MISSING"
FAIL_SOURCE_IDENTITY_NOT_COPIED_FROM_E1 = "COMPRESSED_PACKET_FAIL_SOURCE_IDENTITY_NOT_COPIED_FROM_E1"
FAIL_SOURCE_HASH_MISMATCH_WITH_E1 = "COMPRESSED_PACKET_FAIL_SOURCE_HASH_MISMATCH_WITH_E1"
FAIL_SOURCE_CHAIN_REFS_MISSING = "COMPRESSED_PACKET_FAIL_SOURCE_CHAIN_REFS_MISSING"
FAIL_AUTHORITY_TRANSITION_REF_MISSING = "COMPRESSED_PACKET_FAIL_AUTHORITY_TRANSITION_REF_MISSING"
FAIL_ROUTER_SPECIMEN_REF_MISSING = "COMPRESSED_PACKET_FAIL_ROUTER_SPECIMEN_REF_MISSING"
FAIL_CANDIDATE_AUDIT_REF_MISSING = "COMPRESSED_PACKET_FAIL_CANDIDATE_AUDIT_REF_MISSING"
FAIL_MACHINE_PROCEED_CLOSURE_REF_MISSING = "COMPRESSED_PACKET_FAIL_MACHINE_PROCEED_CLOSURE_REF_MISSING"
FAIL_PRESERVATION_MANIFEST_MISSING = "COMPRESSED_PACKET_FAIL_PRESERVATION_MANIFEST_MISSING"
FAIL_CRITICAL_SUMMARY_MISSING = "COMPRESSED_PACKET_FAIL_CRITICAL_SUMMARY_MISSING"
FAIL_AUTHORITY_TRANSITION_SUMMARY_MISSING = "COMPRESSED_PACKET_FAIL_AUTHORITY_TRANSITION_SUMMARY_MISSING"
FAIL_ROUTER_SUMMARY_MISSING = "COMPRESSED_PACKET_FAIL_ROUTER_SUMMARY_MISSING"
FAIL_CANDIDATE_ARCHIVE_SUMMARY_MISSING = "COMPRESSED_PACKET_FAIL_CANDIDATE_ARCHIVE_SUMMARY_MISSING"
FAIL_PROMOTION_SUMMARY_MISSING = "COMPRESSED_PACKET_FAIL_PROMOTION_SUMMARY_MISSING"
FAIL_ACTIVE_ARCHIVE_SUMMARY_MISSING = "COMPRESSED_PACKET_FAIL_ACTIVE_ARCHIVE_SUMMARY_MISSING"
FAIL_MACHINE_PROCEED_SUMMARY_MISSING = "COMPRESSED_PACKET_FAIL_MACHINE_PROCEED_SUMMARY_MISSING"
FAIL_RADIUS_SUMMARY_MISSING = "COMPRESSED_PACKET_FAIL_RADIUS_SUMMARY_MISSING"
FAIL_STOP_STATE_MISSING = "COMPRESSED_PACKET_FAIL_STOP_STATE_MISSING"
FAIL_NON_EFFECTS_MISSING = "COMPRESSED_PACKET_FAIL_NON_EFFECTS_MISSING"
FAIL_NEXT_SURFACE_SUMMARY_MISSING = "COMPRESSED_PACKET_FAIL_NEXT_SURFACE_SUMMARY_MISSING"
FAIL_DECOMPRESSION_MAP_MISSING = "COMPRESSED_PACKET_FAIL_DECOMPRESSION_MAP_MISSING"
FAIL_DECOMPRESSION_MAP_INCOMPLETE = "COMPRESSED_PACKET_FAIL_DECOMPRESSION_MAP_INCOMPLETE"
FAIL_DECOMPRESSION_AUDIT_CLAIMED = "COMPRESSED_PACKET_FAIL_DECOMPRESSION_AUDIT_CLAIMED_INSIDE_PACKET"
FAIL_FIELD_GROUP_PRESERVATION_PROVEN = "COMPRESSED_PACKET_FAIL_FIELD_GROUP_PRESERVATION_PROVEN_INSIDE_PACKET"
FAIL_TRUSTED_BEFORE_E3_AUDIT = "COMPRESSED_PACKET_FAIL_TRUSTED_BEFORE_E3_AUDIT"
FAIL_SOURCE_AUTHORITY_REPLACED = "COMPRESSED_PACKET_FAIL_SOURCE_AUTHORITY_REPLACED"
FAIL_REUSE_AUTHORIZED = "COMPRESSED_PACKET_FAIL_REUSE_AUTHORIZED"
FAIL_RADIUS_RENEWED = "COMPRESSED_PACKET_FAIL_RADIUS_RENEWED"
FAIL_ADDITIONAL_PROCEED_AUTHORIZED = "COMPRESSED_PACKET_FAIL_ADDITIONAL_PROCEED_AUTHORIZED"
FAIL_RUNNER_AUTHORITY_CREATED = "COMPRESSED_PACKET_FAIL_RUNNER_AUTHORITY_CREATED"
FAIL_REGISTRY_CREATED = "COMPRESSED_PACKET_FAIL_REGISTRY_CREATED_INSIDE_PACKET"

FAILURE_VOCABULARY = [
    FAIL_COMPRESSION_TARGET_MISSING,
    FAIL_TARGET_LABEL_MISSING,
    FAIL_SOURCE_IDENTITY_NOT_COPIED_FROM_E1,
    FAIL_SOURCE_HASH_MISMATCH_WITH_E1,
    FAIL_SOURCE_CHAIN_REFS_MISSING,
    FAIL_AUTHORITY_TRANSITION_REF_MISSING,
    FAIL_ROUTER_SPECIMEN_REF_MISSING,
    FAIL_CANDIDATE_AUDIT_REF_MISSING,
    FAIL_MACHINE_PROCEED_CLOSURE_REF_MISSING,
    FAIL_PRESERVATION_MANIFEST_MISSING,
    FAIL_CRITICAL_SUMMARY_MISSING,
    FAIL_AUTHORITY_TRANSITION_SUMMARY_MISSING,
    FAIL_ROUTER_SUMMARY_MISSING,
    FAIL_CANDIDATE_ARCHIVE_SUMMARY_MISSING,
    FAIL_PROMOTION_SUMMARY_MISSING,
    FAIL_ACTIVE_ARCHIVE_SUMMARY_MISSING,
    FAIL_MACHINE_PROCEED_SUMMARY_MISSING,
    FAIL_RADIUS_SUMMARY_MISSING,
    FAIL_STOP_STATE_MISSING,
    FAIL_NON_EFFECTS_MISSING,
    FAIL_NEXT_SURFACE_SUMMARY_MISSING,
    FAIL_DECOMPRESSION_MAP_MISSING,
    FAIL_DECOMPRESSION_MAP_INCOMPLETE,
    FAIL_DECOMPRESSION_AUDIT_CLAIMED,
    FAIL_FIELD_GROUP_PRESERVATION_PROVEN,
    FAIL_TRUSTED_BEFORE_E3_AUDIT,
    FAIL_SOURCE_AUTHORITY_REPLACED,
    FAIL_REUSE_AUTHORIZED,
    FAIL_RADIUS_RENEWED,
    FAIL_ADDITIONAL_PROCEED_AUTHORIZED,
    FAIL_RUNNER_AUTHORITY_CREATED,
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

DECOMPRESSION_MAP = {
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

FORBIDDEN_MARKDOWN_PHRASES = [
    "decompression passed",
    "compression closed",
    "valid shortcut",
    "trusted shortcut",
    "source authority replaced",
    "registry candidate created",
    "reuse authorized",
    "radius renewed",
    "runner ready",
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
        fail(FAIL_COMPRESSION_TARGET_MISSING, proc.stderr.strip())
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


def expect(value: object, wanted: object, failure_code: str, field: str) -> None:
    if value != wanted:
        fail(failure_code, f"{field}: {value!r}!={wanted!r}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def bool_text(value: bool) -> str:
    return str(value).lower()


def artifact_id(section: dict[str, Any], key: str) -> str | None:
    value = section.get(key, {})
    if isinstance(value, dict):
        artifact = value.get("artifact_id")
        if isinstance(artifact, str) and artifact:
            return artifact
    return None


def validate_e1_target(e1: dict[str, Any]) -> None:
    expect(
        e1.get("schema_version"),
        "matrixlabs_compression_target_declaration_v0",
        FAIL_COMPRESSION_TARGET_MISSING,
        "e1.schema_version",
    )
    expect(e1.get("compression_target_id"), SOURCE_COMPRESSION_TARGET_ID, FAIL_COMPRESSION_TARGET_MISSING, "e1.id")
    expect(e1.get("target_status"), "COMPRESSION_TARGET_PASS_DECLARED_ONLY", FAIL_COMPRESSION_TARGET_MISSING, "e1.status")
    expect(e1.get("target_trace_label"), TARGET_TRACE_LABEL, FAIL_TARGET_LABEL_MISSING, "e1.target_trace_label")
    expect(e1.get("compression_mode"), COMPRESSION_MODE, FAIL_TARGET_LABEL_MISSING, "e1.compression_mode")
    expect(e1.get("critical_field_groups"), CRITICAL_FIELD_GROUPS, FAIL_PRESERVATION_MANIFEST_MISSING, "e1.critical_field_groups")
    expect(e1.get("critical_field_group_count"), 15, FAIL_PRESERVATION_MANIFEST_MISSING, "e1.critical_field_group_count")
    recoverable = e1.get("required_recoverable_fields_by_group", {})
    if set(recoverable) != set(CRITICAL_FIELD_GROUPS):
        fail(FAIL_PRESERVATION_MANIFEST_MISSING, "E.1 recoverable field groups do not match critical groups")

    chain = e1.get("source_chain", {})
    required_chain = {
        "authority_transition_closure_id": FAIL_AUTHORITY_TRANSITION_REF_MISSING,
        "router_specimen_closure_id": FAIL_ROUTER_SPECIMEN_REF_MISSING,
        "candidate_archive_audit_id": FAIL_CANDIDATE_AUDIT_REF_MISSING,
        "machine_proceed_closure_id": FAIL_MACHINE_PROCEED_CLOSURE_REF_MISSING,
    }
    for key, code in required_chain.items():
        if not isinstance(chain.get(key), str) or not chain[key]:
            fail(code, key)
    expect(chain.get("source_chain_complete"), True, FAIL_SOURCE_CHAIN_REFS_MISSING, "e1.source_chain_complete")

    if not isinstance(e1.get("source_artifacts"), dict) or not isinstance(e1.get("supporting_source_artifacts"), dict):
        fail(FAIL_SOURCE_IDENTITY_NOT_COPIED_FROM_E1, "E.1 source artifact sections missing")


def verify_e1_hashes(root: Path, e1: dict[str, Any]) -> None:
    for section_name in ["source_artifacts", "supporting_source_artifacts"]:
        section = e1.get(section_name, {})
        if not isinstance(section, dict):
            fail(FAIL_SOURCE_IDENTITY_NOT_COPIED_FROM_E1, section_name)
        for name, ref in section.items():
            if not isinstance(ref, dict):
                fail(FAIL_SOURCE_IDENTITY_NOT_COPIED_FROM_E1, f"{section_name}.{name}")
            rel = ref.get("path")
            expected_hash = ref.get("sha256")
            if not isinstance(rel, str) or not rel:
                fail(FAIL_SOURCE_IDENTITY_NOT_COPIED_FROM_E1, f"{section_name}.{name}.path")
            if not isinstance(expected_hash, str) or len(expected_hash) != 64:
                fail(FAIL_SOURCE_IDENTITY_NOT_COPIED_FROM_E1, f"{section_name}.{name}.sha256")
            path = root / rel
            if not path.exists():
                fail(FAIL_SOURCE_HASH_MISMATCH_WITH_E1, f"missing referenced source: {rel}")
            actual_hash = sha256_file(path)
            if actual_hash != expected_hash:
                fail(FAIL_SOURCE_HASH_MISMATCH_WITH_E1, f"{rel}: {actual_hash}!={expected_hash}")


def source_identity_from_e1() -> dict[str, Any]:
    return {
        "compression_target_id": SOURCE_COMPRESSION_TARGET_ID,
        "source_refs_copied_from_e1": True,
        "source_hashes_copied_from_e1": True,
        "source_identity_recomputed_by_e2": False,
        "source_hashes_verified_against_e1": True,
        "mtime_or_latest_file_resolution_allowed": False,
        "directory_scan_authority_allowed": False,
    }


def block_source_refs(e1: dict[str, Any]) -> dict[str, Any]:
    primary = e1["source_artifacts"]
    supporting = e1["supporting_source_artifacts"]
    chain = e1["source_chain"]
    return {
        "block_A": {
            "authority_transition_closure_id": chain["authority_transition_closure_id"],
            "authority_state_update_id": artifact_id(supporting, "authority_state_update"),
            "human_decision_receipt_id": None,
            "human_decision_receipt_id_reason": "not exposed as separate supporting source in E.1",
        },
        "block_B": {
            "requested_action_record_id": None,
            "requested_action_record_id_reason": "not exposed as separate supporting source in E.1",
            "route_classification_id": artifact_id(supporting, "route_classification"),
            "router_specimen_closure_id": chain["router_specimen_closure_id"],
        },
        "block_C": {
            "candidate_entry_id": artifact_id(supporting, "candidate_archive_entry"),
            "candidate_audit_id": chain["candidate_archive_audit_id"],
        },
        "block_D": {
            "promotion_decision_receipt_id": "c8.n22.candidate_promotion_decision_receipt.v0",
            "active_archive_entry_id": artifact_id(supporting, "active_archive_entry"),
            "machine_proceed_id": artifact_id(supporting, "machine_proceed"),
            "machine_proceed_closure_id": artifact_id(primary, "machine_proceed_closure"),
            "output_surface_id": artifact_id(supporting, "output_surface"),
        },
    }


def source_chain_refs(e1: dict[str, Any]) -> dict[str, str]:
    chain = e1["source_chain"]
    return {
        "authority_transition_closure_id": chain["authority_transition_closure_id"],
        "router_specimen_closure_id": chain["router_specimen_closure_id"],
        "candidate_archive_audit_id": chain["candidate_archive_audit_id"],
        "machine_proceed_closure_id": chain["machine_proceed_closure_id"],
    }


def compressed_summary() -> dict[str, Any]:
    return {
        "initial_authority_state": "AUTH_STATE_OBSERVED_NOT_AUTHORIZED",
        "accepted_authority_state": "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        "human_authority_decision": "DECISION_ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        "requested_action": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
        "requested_action_scope": "PREPARE_SURFACE_ONLY",
        "route_disposition": "ROUTE_MACHINE_MAY_PREPARE_ONLY",
        "candidate_entry_status_before_promotion": "ARCHIVE_STATUS_CANDIDATE",
        "candidate_audit_status": "CANDIDATE_AUDIT_PASS_CONTRACT_CONFORMANT_NOT_PROMOTED",
        "promotion_decision": "DECISION_PROMOTE_CANDIDATE_FOR_DECLARED_SCOPE",
        "active_archive_entry_status": "ARCHIVE_STATUS_PREAPPROVED_ACTIVE",
        "reuse_authority_status_after_promotion": "REUSE_AUTHORITY_GRANTED_FOR_DECLARED_SCOPE",
        "performed_action": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
        "performed_action_scope": "PREPARE_SURFACE_ONLY",
        "radius_limit": "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT",
        "radius_before": 1,
        "radius_consumed": 1,
        "radius_after": 0,
        "radius_exhausted": True,
        "created_output_surface": "c8.n22.next_bounded_unit_definition_surface.v0",
        "created_output_kind": "NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
        "output_execution_status": "NOT_EXECUTED",
        "output_surface_status": "NEXT_UNIT_DEFINITION_SURFACE_PREPARED_NOT_EXECUTED",
    }


def preservation_manifest(e1: dict[str, Any]) -> dict[str, Any]:
    recoverable = e1["required_recoverable_fields_by_group"]
    return {
        "source_compression_target_id": SOURCE_COMPRESSION_TARGET_ID,
        "declared_critical_field_group_count": e1["critical_field_group_count"],
        "required_recoverable_field_groups_from_e1": len(recoverable),
        "packet_claims_to_preserve_all_declared_groups": True,
        "packet_claims_to_cover_all_required_recoverable_field_groups": True,
        "field_groups_claimed_preserved": list(e1["critical_field_groups"]),
        "field_group_preservation_proven_by_e2": False,
        "requires_e3_decompression_parity_audit": True,
    }


def packet_trust_state() -> dict[str, Any]:
    return {
        "packet_created": True,
        "trusted_as_observability_shortcut": False,
        "trust_blocked_until": "E3_DECOMPRESSION_PARITY_AUDIT",
        "decompression_parity_passed": False,
        "compression_closed": False,
    }


def compressed_trace_label_definition() -> dict[str, str]:
    return {
        "label": TARGET_TRACE_LABEL,
        "meaning": "completed local radius-bound prepare trace",
        "scope": "C8_N22_LOCAL_SPECIMEN_ONLY",
        "authority_effect": "NONE",
        "reuse_effect": "NONE",
        "radius_effect": "NONE",
        "runner_effect": "NONE",
    }


def authority_transition_summary() -> dict[str, str]:
    return {
        "prior_authority_state": "AUTH_STATE_OBSERVED_NOT_AUTHORIZED",
        "selected_authority_decision": "DECISION_ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        "decision_actor_class": "HUMAN",
        "authority_event_consumed": "HUMAN_ACCEPTANCE",
        "resulting_authority_state": "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        "next_allowed_router_action_after_A": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
    }


def router_summary() -> dict[str, Any]:
    return {
        "requested_action": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
        "requested_action_scope": "PREPARE_SURFACE_ONLY",
        "route_disposition": "ROUTE_MACHINE_MAY_PREPARE_ONLY",
        "router_mode": "CLASSIFY_ONLY_NO_ACTION",
        "router_executed_action": False,
        "router_changed_authority": False,
    }


def candidate_archive_summary() -> dict[str, Any]:
    return {
        "candidate_entry_id": "candidate.c8.n22.prepare_next_unit_definition_surface.v0",
        "candidate_status": "ARCHIVE_STATUS_CANDIDATE",
        "candidate_audit_status": "CANDIDATE_AUDIT_PASS_CONTRACT_CONFORMANT_NOT_PROMOTED",
        "candidate_promoted_before_D": False,
        "candidate_reusable_before_D": False,
        "candidate_active_before_D": False,
        "promotion_decision": "DECISION_PROMOTE_CANDIDATE_FOR_DECLARED_SCOPE",
        "active_archive_entry_id": "active.c8.n22.prepare_next_unit_definition_surface.v0",
        "active_entry_status": "ARCHIVE_STATUS_PREAPPROVED_ACTIVE",
        "promotion_status_after_D3": "PROMOTION_GRANTED_FOR_DECLARED_SCOPE",
        "reuse_authority_status_after_D3": "REUSE_AUTHORITY_GRANTED_FOR_DECLARED_SCOPE",
        "activation_status_after_D3": "ACTIVATION_ACTIVE",
    }


def machine_proceed_summary() -> dict[str, Any]:
    return {
        "active_archive_entry_id": "active.c8.n22.prepare_next_unit_definition_surface.v0",
        "performed_action": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
        "performed_action_scope": "PREPARE_SURFACE_ONLY",
        "performed_basis_scope": "C8_N22_BASIS_ONLY",
        "performed_source_object_id": "c8.n22",
        "performed_output_kind": "NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
        "output_surface_id": "c8.n22.next_bounded_unit_definition_surface.v0",
        "output_surface_status": "NEXT_UNIT_DEFINITION_SURFACE_PREPARED_NOT_EXECUTED",
        "unit_executed": False,
    }


def radius_and_stop_state_summary() -> dict[str, Any]:
    return {
        "radius_limit": "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT",
        "radius_before": 1,
        "radius_consumed": 1,
        "radius_after": 0,
        "radius_exhausted": True,
        "entry_has_remaining_radius": False,
        "entry_may_authorize_additional_machine_proceed": False,
        "additional_use_requires_new_authority_or_radius": True,
        "same_radius_may_be_reused": False,
        "radius_renewed_by_packet": False,
        "additional_radius_created_by_packet": False,
    }


def confirmed_non_effects() -> dict[str, bool]:
    return {
        "unit_executed": False,
        "runtime_executed": False,
        "authority_changed_after_machine_proceed": False,
        "human_decision_consumed_by_compression": False,
        "receipts_rewritten": False,
        "taxonomy_promoted": False,
        "reuse_scope_expanded": False,
        "updater_generalized": False,
        "runner_authority_created": False,
        "additional_radius_created": False,
        "active_archive_scope_expanded": False,
        "active_archive_entry_rewritten_by_packet": False,
        "active_archive_entry_mutated_by_packet": False,
    }


def next_possible_separate_surface_summary() -> dict[str, Any]:
    return {
        "next_possible_separate_surface": "REVIEW_OR_DECISION_SURFACE_FOR_CREATED_NEXT_UNIT",
        "created_by_compressed_packet": False,
        "authorized_by_compressed_packet": False,
        "machine_may_prepare_without_new_authority": False,
        "reason": "D.4 created a next bounded unit definition surface but did not authorize execution or further proceed.",
    }


def packet_boundary() -> dict[str, Any]:
    return {
        "packet_role": "OBSERVABILITY_PACKET_PENDING_AUDIT",
        "source_records_remain_authority": True,
        "packet_may_be_used_for_display_after_e3_pass": True,
        "packet_may_be_used_for_authority_decision_without_decompression": False,
        "packet_may_replace_source_authority": False,
        "packet_replaces_source_authority": False,
        "packet_grants_authority": False,
        "packet_may_authorize_reuse": False,
        "packet_authorizes_reuse": False,
        "packet_may_renew_radius": False,
        "packet_renews_radius": False,
        "packet_may_authorize_additional_machine_proceed": False,
        "packet_authorizes_additional_machine_proceed": False,
        "packet_performs_machine_action": False,
        "packet_may_create_runner_authority": False,
        "packet_creates_runner_authority": False,
        "packet_may_satisfy_active_entry_requirement": False,
        "packet_may_satisfy_human_decision_requirement": False,
        "packet_may_satisfy_radius_requirement": False,
        "packet_may_be_input_to_machine_proceed_without_source_chain": False,
        "packet_may_be_promoted_to_registry_by_e2": False,
        "requires_decompression_parity_audit": True,
        "next_required_object": NEXT_REQUIRED_OBJECT,
    }


def packet_gate() -> dict[str, Any]:
    return {
        "compressed_packet_gate": COMPRESSED_PACKET_GATE,
        "compression_target_present": True,
        "target_trace_label": TARGET_TRACE_LABEL,
        "compression_mode": COMPRESSION_MODE,
        "source_identity_copied_from_e1": True,
        "source_hashes_copied_from_e1": True,
        "source_hashes_verified_against_e1": True,
        "source_chain_refs_present": True,
        "authority_transition_closure_ref_present": True,
        "router_specimen_closure_ref_present": True,
        "candidate_archive_audit_ref_present": True,
        "machine_proceed_closure_ref_present": True,
        "critical_summary_fields_present": True,
        "preservation_manifest_present": True,
        "packet_claims_to_preserve_all_declared_groups": True,
        "packet_claims_to_cover_all_required_recoverable_field_groups": True,
        "field_group_preservation_proven_by_e2": False,
        "decompression_map_present": True,
        "decompression_map_group_count": len(DECOMPRESSION_MAP),
        "decompression_map_covers_all_e1_critical_groups": True,
        "radius_summary_present": True,
        "radius_limit": "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT",
        "radius_after": 0,
        "radius_exhausted": True,
        "confirmed_non_effects_present": True,
        "unit_executed": False,
        "runtime_executed": False,
        "authority_changed_after_machine_proceed": False,
        "reuse_scope_expanded": False,
        "runner_authority_created": False,
        "additional_radius_created": False,
        "packet_status": PACKET_STATUS,
        "trusted_as_observability_shortcut": False,
        "decompression_parity_passed": False,
        "compression_closed": False,
        "decompression_audit_performed_by_e2": False,
        "packet_replaces_source_authority": False,
        "packet_authorizes_reuse": False,
        "packet_renews_radius": False,
        "packet_authorizes_additional_machine_proceed": False,
        "packet_creates_runner_authority": False,
        "next_required_object": NEXT_REQUIRED_OBJECT,
        "failures": [],
    }


def build_record(e1: dict[str, Any]) -> dict[str, Any]:
    copied_sources = {
        "source_artifacts": copy.deepcopy(e1["source_artifacts"]),
        "supporting_source_artifacts": copy.deepcopy(e1["supporting_source_artifacts"]),
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "compressed_packet_id": COMPRESSED_PACKET_ID,
        "packet_role": PACKET_ROLE,
        "packet_status": PACKET_STATUS,
        "block_id": BLOCK_ID,
        "block_unit_id": BLOCK_UNIT_ID,
        "block_e_status": BLOCK_E_STATUS,
        "target_trace_label": TARGET_TRACE_LABEL,
        "compression_mode": COMPRESSION_MODE,
        "source_compression_target_id": SOURCE_COMPRESSION_TARGET_ID,
        "source_identity_from_e1": source_identity_from_e1(),
        "packet_trust_state": packet_trust_state(),
        "compressed_trace_label_definition": compressed_trace_label_definition(),
        "source_chain_refs": source_chain_refs(e1),
        "source_artifacts_copied_from_e1": copied_sources,
        "block_source_refs": block_source_refs(e1),
        "compressed_summary": compressed_summary(),
        "preservation_manifest": preservation_manifest(e1),
        "decompression_map": DECOMPRESSION_MAP,
        "decompression_map_group_count": len(DECOMPRESSION_MAP),
        "decompression_map_covers_all_e1_critical_groups": True,
        "authority_transition_summary": authority_transition_summary(),
        "router_summary": router_summary(),
        "candidate_archive_summary": candidate_archive_summary(),
        "machine_proceed_summary": machine_proceed_summary(),
        "radius_and_stop_state_summary": radius_and_stop_state_summary(),
        "confirmed_non_effects": confirmed_non_effects(),
        "next_possible_separate_surface_summary": next_possible_separate_surface_summary(),
        "packet_boundary": packet_boundary(),
        "packet_gate": packet_gate(),
        "failure_vocabulary": FAILURE_VOCABULARY,
        "non_claims": [
            "E.2 does not prove decompression parity.",
            "E.2 does not close compression.",
            "E.2 does not create a registry entry.",
            "E.2 does not replace source records.",
            "E.2 does not authorize reuse.",
            "E.2 does not renew radius.",
            "E.2 does not authorize another machine proceed.",
            "E.2 does not perform machine action.",
            "E.2 does not execute the next unit.",
            "E.2 does not create runner authority.",
            "E.2 only creates a compressed observability packet pending decompression audit.",
        ],
        "key_non_claims": [
            "compressed packet ≠ decompression audit",
            "compressed packet ≠ source authority",
            "compressed label ≠ reusable schema",
            "preservation claim ≠ parity proof",
            "created packet ≠ trusted shortcut",
            "boundary pass ≠ parity pass",
        ],
        "precommit_c8_n22_compressed_packet_gate": PRECOMMIT_GATE,
        "compressed_packet_gate": COMPRESSED_PACKET_GATE,
        "terminal_transition": TERMINAL_TRANSITION,
        "generated_by": GENERATOR,
    }


def validate_record(record: dict[str, Any]) -> None:
    expect(record.get("schema_version"), SCHEMA_VERSION, FAIL_COMPRESSION_TARGET_MISSING, "schema_version")
    expect(record.get("compressed_packet_id"), COMPRESSED_PACKET_ID, FAIL_COMPRESSION_TARGET_MISSING, "compressed_packet_id")
    expect(record.get("packet_role"), PACKET_ROLE, FAIL_CRITICAL_SUMMARY_MISSING, "packet_role")
    expect(record.get("packet_status"), PACKET_STATUS, FAIL_CRITICAL_SUMMARY_MISSING, "packet_status")
    expect(record.get("block_id"), BLOCK_ID, FAIL_CRITICAL_SUMMARY_MISSING, "block_id")
    expect(record.get("block_unit_id"), BLOCK_UNIT_ID, FAIL_CRITICAL_SUMMARY_MISSING, "block_unit_id")
    expect(record.get("block_e_status"), BLOCK_E_STATUS, FAIL_CRITICAL_SUMMARY_MISSING, "block_e_status")
    expect(record.get("target_trace_label"), TARGET_TRACE_LABEL, FAIL_TARGET_LABEL_MISSING, "target_trace_label")
    expect(record.get("compression_mode"), COMPRESSION_MODE, FAIL_TARGET_LABEL_MISSING, "compression_mode")
    expect(
        record.get("source_compression_target_id"),
        SOURCE_COMPRESSION_TARGET_ID,
        FAIL_COMPRESSION_TARGET_MISSING,
        "source_compression_target_id",
    )

    identity = record.get("source_identity_from_e1", {})
    for key, expected in {
        "source_refs_copied_from_e1": True,
        "source_hashes_copied_from_e1": True,
        "source_identity_recomputed_by_e2": False,
        "source_hashes_verified_against_e1": True,
        "mtime_or_latest_file_resolution_allowed": False,
        "directory_scan_authority_allowed": False,
    }.items():
        expect(identity.get(key), expected, FAIL_SOURCE_IDENTITY_NOT_COPIED_FROM_E1, key)

    trust = record.get("packet_trust_state", {})
    for key, expected in {
        "packet_created": True,
        "trusted_as_observability_shortcut": False,
        "decompression_parity_passed": False,
        "compression_closed": False,
    }.items():
        code = FAIL_TRUSTED_BEFORE_E3_AUDIT if key == "trusted_as_observability_shortcut" else FAIL_DECOMPRESSION_AUDIT_CLAIMED
        expect(trust.get(key), expected, code, key)

    if not record.get("source_chain_refs"):
        fail(FAIL_SOURCE_CHAIN_REFS_MISSING, "source_chain_refs")
    if not record.get("source_artifacts_copied_from_e1"):
        fail(FAIL_SOURCE_IDENTITY_NOT_COPIED_FROM_E1, "source_artifacts_copied_from_e1")
    if not record.get("block_source_refs"):
        fail(FAIL_SOURCE_CHAIN_REFS_MISSING, "block_source_refs")

    summary = record.get("compressed_summary", {})
    expect(summary.get("radius_after"), 0, FAIL_RADIUS_SUMMARY_MISSING, "summary.radius_after")
    expect(summary.get("radius_exhausted"), True, FAIL_RADIUS_SUMMARY_MISSING, "summary.radius_exhausted")
    expect(
        summary.get("output_surface_status"),
        "NEXT_UNIT_DEFINITION_SURFACE_PREPARED_NOT_EXECUTED",
        FAIL_CRITICAL_SUMMARY_MISSING,
        "summary.output_surface_status",
    )

    manifest = record.get("preservation_manifest", {})
    if not manifest:
        fail(FAIL_PRESERVATION_MANIFEST_MISSING, "preservation_manifest")
    expect(manifest.get("packet_claims_to_preserve_all_declared_groups"), True, FAIL_PRESERVATION_MANIFEST_MISSING, "claims groups")
    expect(
        manifest.get("packet_claims_to_cover_all_required_recoverable_field_groups"),
        True,
        FAIL_PRESERVATION_MANIFEST_MISSING,
        "claims recoverable groups",
    )
    expect(manifest.get("field_group_preservation_proven_by_e2"), False, FAIL_FIELD_GROUP_PRESERVATION_PROVEN, "proven_by_e2")
    expect(manifest.get("requires_e3_decompression_parity_audit"), True, FAIL_DECOMPRESSION_AUDIT_CLAIMED, "requires_e3")

    expect(record.get("decompression_map_group_count"), 15, FAIL_DECOMPRESSION_MAP_INCOMPLETE, "decompression_map_group_count")
    expect(record.get("decompression_map_covers_all_e1_critical_groups"), True, FAIL_DECOMPRESSION_MAP_INCOMPLETE, "map covers")
    if set(record.get("decompression_map", {})) != set(CRITICAL_FIELD_GROUPS):
        fail(FAIL_DECOMPRESSION_MAP_INCOMPLETE, "decompression map group set")

    for name, section, failure in [
        ("authority_transition_summary", record.get("authority_transition_summary"), FAIL_AUTHORITY_TRANSITION_SUMMARY_MISSING),
        ("router_summary", record.get("router_summary"), FAIL_ROUTER_SUMMARY_MISSING),
        ("candidate_archive_summary", record.get("candidate_archive_summary"), FAIL_CANDIDATE_ARCHIVE_SUMMARY_MISSING),
        ("machine_proceed_summary", record.get("machine_proceed_summary"), FAIL_MACHINE_PROCEED_SUMMARY_MISSING),
        ("radius_and_stop_state_summary", record.get("radius_and_stop_state_summary"), FAIL_RADIUS_SUMMARY_MISSING),
        ("confirmed_non_effects", record.get("confirmed_non_effects"), FAIL_NON_EFFECTS_MISSING),
        (
            "next_possible_separate_surface_summary",
            record.get("next_possible_separate_surface_summary"),
            FAIL_NEXT_SURFACE_SUMMARY_MISSING,
        ),
    ]:
        if not isinstance(section, dict) or not section:
            fail(failure, name)

    radius = record["radius_and_stop_state_summary"]
    expect(radius.get("radius_after"), 0, FAIL_RADIUS_SUMMARY_MISSING, "radius_after")
    expect(radius.get("radius_exhausted"), True, FAIL_STOP_STATE_MISSING, "radius_exhausted")
    expect(radius.get("same_radius_may_be_reused"), False, FAIL_STOP_STATE_MISSING, "same_radius_may_be_reused")
    expect(radius.get("radius_renewed_by_packet"), False, FAIL_RADIUS_RENEWED, "radius_renewed_by_packet")
    expect(radius.get("additional_radius_created_by_packet"), False, FAIL_RADIUS_RENEWED, "additional_radius_created_by_packet")

    effects = record["confirmed_non_effects"]
    for key in [
        "unit_executed",
        "runtime_executed",
        "reuse_scope_expanded",
        "runner_authority_created",
        "additional_radius_created",
    ]:
        expect(effects.get(key), False, FAIL_NON_EFFECTS_MISSING, key)

    boundary = record["packet_boundary"]
    for key, failure in {
        "packet_may_replace_source_authority": FAIL_SOURCE_AUTHORITY_REPLACED,
        "packet_authorizes_reuse": FAIL_REUSE_AUTHORIZED,
        "packet_renews_radius": FAIL_RADIUS_RENEWED,
        "packet_authorizes_additional_machine_proceed": FAIL_ADDITIONAL_PROCEED_AUTHORIZED,
        "packet_may_satisfy_active_entry_requirement": FAIL_SOURCE_AUTHORITY_REPLACED,
        "packet_may_satisfy_human_decision_requirement": FAIL_SOURCE_AUTHORITY_REPLACED,
        "packet_may_satisfy_radius_requirement": FAIL_SOURCE_AUTHORITY_REPLACED,
        "packet_may_be_promoted_to_registry_by_e2": FAIL_REGISTRY_CREATED,
    }.items():
        expect(boundary.get(key), False, failure, key)
    expect(boundary.get("requires_decompression_parity_audit"), True, FAIL_DECOMPRESSION_AUDIT_CLAIMED, "boundary requires audit")

    gate = record["packet_gate"]
    expect(gate.get("compressed_packet_gate"), COMPRESSED_PACKET_GATE, FAIL_CRITICAL_SUMMARY_MISSING, "packet_gate")
    expect(gate.get("field_group_preservation_proven_by_e2"), False, FAIL_FIELD_GROUP_PRESERVATION_PROVEN, "gate proven")
    expect(gate.get("decompression_parity_passed"), False, FAIL_DECOMPRESSION_AUDIT_CLAIMED, "gate parity")
    expect(gate.get("trusted_as_observability_shortcut"), False, FAIL_TRUSTED_BEFORE_E3_AUDIT, "gate trusted")
    expect(gate.get("failures"), [], FAIL_CRITICAL_SUMMARY_MISSING, "gate.failures")
    expect(record.get("precommit_c8_n22_compressed_packet_gate"), PRECOMMIT_GATE, FAIL_CRITICAL_SUMMARY_MISSING, "precommit")
    expect(record.get("compressed_packet_gate"), COMPRESSED_PACKET_GATE, FAIL_CRITICAL_SUMMARY_MISSING, "compressed_packet_gate")
    expect(record.get("terminal_transition"), TERMINAL_TRANSITION, FAIL_CRITICAL_SUMMARY_MISSING, "terminal_transition")


def render_markdown(record: dict[str, Any]) -> str:
    source = record["source_chain_refs"]
    return f"""# C8 n22 radius-bound prepare trace compressed packet v0

## Status

{PACKET_STATUS}

## Trace label

{TARGET_TRACE_LABEL}

## Role

Compressed observability packet.

## Trust state

Created, but not trusted as an observability shortcut until E.3 decompression parity audit passes.

## Source closures

- authority transition closure: {source['authority_transition_closure_id']}
- router specimen closure: {source['router_specimen_closure_id']}
- candidate archive audit: {source['candidate_archive_audit_id']}
- machine proceed closure: {source['machine_proceed_closure_id']}

## Compact summary

- initial authority state: AUTH_STATE_OBSERVED_NOT_AUTHORIZED
- accepted authority state: AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION
- requested action: PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE
- route disposition: ROUTE_MACHINE_MAY_PREPARE_ONLY
- candidate audit: CANDIDATE_AUDIT_PASS_CONTRACT_CONFORMANT_NOT_PROMOTED
- promotion: PROMOTION_GRANTED_FOR_DECLARED_SCOPE
- active entry: ARCHIVE_STATUS_PREAPPROVED_ACTIVE
- machine action: PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE
- output: c8.n22.next_bounded_unit_definition_surface.v0
- output status: NEXT_UNIT_DEFINITION_SURFACE_PREPARED_NOT_EXECUTED
- radius: 1 → 0

## Preservation manifest

The packet claims to preserve all 15 E.1 critical field groups. E.2 does not prove preservation; E.3 must audit decompression parity.

## Decompression map

The packet maps all 15 E.1 critical field groups to packet sections for E.3 audit.

## Confirmed non-effects

- unit not executed
- runtime not executed
- authority not changed after machine proceed
- receipts not rewritten
- taxonomy not promoted
- reuse scope not expanded
- updater not generalized
- runner authority not created
- additional radius not created

## Boundary

This packet does not replace source records, authorize reuse, renew radius, authorize another proceed, satisfy active-entry requirements, satisfy human-decision requirements, satisfy radius requirements, or create runner authority.

## Next required object

{NEXT_REQUIRED_OBJECT}
"""


def validate_markdown(text: str) -> None:
    lowered = text.lower()
    for phrase in FORBIDDEN_MARKDOWN_PHRASES:
        if phrase in lowered:
            fail(FAIL_CRITICAL_SUMMARY_MISSING, f"forbidden markdown phrase: {phrase}")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_outputs(root: Path, record: dict[str, Any]) -> None:
    json_content = json.dumps(record, indent=2, sort_keys=True) + "\n"
    markdown = render_markdown(record)
    validate_markdown(markdown)
    write_text(root / OUTPUT_JSON, json_content)
    write_text(root / OUTPUT_MD, markdown)


def print_success(record: dict[str, Any]) -> None:
    identity = record["source_identity_from_e1"]
    trust = record["packet_trust_state"]
    manifest = record["preservation_manifest"]
    gate = record["packet_gate"]
    radius = record["radius_and_stop_state_summary"]
    effects = record["confirmed_non_effects"]
    boundary = record["packet_boundary"]
    summary = record["compressed_summary"]

    print("BUILD_C8_N22_RADIUS_BOUND_PREPARE_TRACE_COMPRESSED_PACKET_V0_COMPLETE")
    print(f"compressed_packet_id={record['compressed_packet_id']}")
    print(f"schema_version={record['schema_version']}")
    print(f"packet_role={record['packet_role']}")
    print(f"packet_status={record['packet_status']}")
    print(f"block_id={record['block_id']}")
    print(f"block_unit_id={record['block_unit_id']}")
    print(f"block_e_status={record['block_e_status']}")
    print(f"target_trace_label={record['target_trace_label']}")
    print(f"compression_mode={record['compression_mode']}")
    print(f"source_compression_target_id={record['source_compression_target_id']}")
    print(f"source_refs_copied_from_e1={bool_text(identity['source_refs_copied_from_e1'])}")
    print(f"source_hashes_copied_from_e1={bool_text(identity['source_hashes_copied_from_e1'])}")
    print(f"source_identity_recomputed_by_e2={bool_text(identity['source_identity_recomputed_by_e2'])}")
    print(f"source_hashes_verified_against_e1={bool_text(identity['source_hashes_verified_against_e1'])}")
    print(f"packet_created={bool_text(trust['packet_created'])}")
    print(f"trusted_as_observability_shortcut={bool_text(trust['trusted_as_observability_shortcut'])}")
    print(f"trust_blocked_until={trust['trust_blocked_until']}")
    print(f"decompression_parity_passed={bool_text(trust['decompression_parity_passed'])}")
    print(f"compression_closed={bool_text(trust['compression_closed'])}")
    print(f"source_chain_refs_present={bool_text(gate['source_chain_refs_present'])}")
    print(f"critical_summary_fields_present={bool_text(gate['critical_summary_fields_present'])}")
    print(f"preservation_manifest_present={bool_text(gate['preservation_manifest_present'])}")
    print(f"packet_claims_to_preserve_all_declared_groups={bool_text(manifest['packet_claims_to_preserve_all_declared_groups'])}")
    print(
        "packet_claims_to_cover_all_required_recoverable_field_groups="
        f"{bool_text(manifest['packet_claims_to_cover_all_required_recoverable_field_groups'])}"
    )
    print(f"field_group_preservation_proven_by_e2={bool_text(manifest['field_group_preservation_proven_by_e2'])}")
    print(f"requires_e3_decompression_parity_audit={bool_text(manifest['requires_e3_decompression_parity_audit'])}")
    print(f"decompression_map_present={bool_text(gate['decompression_map_present'])}")
    print(f"decompression_map_group_count={record['decompression_map_group_count']}")
    print(f"decompression_map_covers_all_e1_critical_groups={bool_text(record['decompression_map_covers_all_e1_critical_groups'])}")
    print(f"radius_limit={radius['radius_limit']}")
    print(f"radius_before={radius['radius_before']}")
    print(f"radius_consumed={radius['radius_consumed']}")
    print(f"radius_after={radius['radius_after']}")
    print(f"radius_exhausted={bool_text(radius['radius_exhausted'])}")
    print(f"same_radius_may_be_reused={bool_text(radius['same_radius_may_be_reused'])}")
    print(f"radius_renewed_by_packet={bool_text(radius['radius_renewed_by_packet'])}")
    print(f"additional_radius_created_by_packet={bool_text(radius['additional_radius_created_by_packet'])}")
    print(f"unit_executed={bool_text(effects['unit_executed'])}")
    print(f"runtime_executed={bool_text(effects['runtime_executed'])}")
    print(f"authority_changed_after_machine_proceed={bool_text(effects['authority_changed_after_machine_proceed'])}")
    print(f"reuse_scope_expanded={bool_text(effects['reuse_scope_expanded'])}")
    print(f"runner_authority_created={bool_text(effects['runner_authority_created'])}")
    print(f"additional_radius_created={bool_text(effects['additional_radius_created'])}")
    print(f"output_surface_status={summary['output_surface_status']}")
    print(f"packet_may_replace_source_authority={bool_text(boundary['packet_may_replace_source_authority'])}")
    print(f"packet_authorizes_reuse={bool_text(boundary['packet_authorizes_reuse'])}")
    print(f"packet_renews_radius={bool_text(boundary['packet_renews_radius'])}")
    print(f"packet_authorizes_additional_machine_proceed={bool_text(boundary['packet_authorizes_additional_machine_proceed'])}")
    print(f"packet_may_satisfy_active_entry_requirement={bool_text(boundary['packet_may_satisfy_active_entry_requirement'])}")
    print(f"packet_may_satisfy_human_decision_requirement={bool_text(boundary['packet_may_satisfy_human_decision_requirement'])}")
    print(f"packet_may_satisfy_radius_requirement={bool_text(boundary['packet_may_satisfy_radius_requirement'])}")
    print(f"packet_may_be_promoted_to_registry_by_e2={bool_text(boundary['packet_may_be_promoted_to_registry_by_e2'])}")
    print(f"decompression_audit_performed_by_e2={bool_text(gate['decompression_audit_performed_by_e2'])}")
    print(f"compressed_packet_gate={record['compressed_packet_gate']}")
    print(f"precommit_c8_n22_compressed_packet_gate={record['precommit_c8_n22_compressed_packet_gate']}")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition={record['terminal_transition']}")


def main() -> int:
    try:
        root = detect_repo_root(Path.cwd())
        e1 = load_json(root / E1_TARGET_JSON, FAIL_COMPRESSION_TARGET_MISSING)
        validate_e1_target(e1)
        verify_e1_hashes(root, e1)
        record = build_record(e1)
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
