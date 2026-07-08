#!/usr/bin/env python3

"""Build C8 n22 compression specimen closure v0.

E.4 verifies the committed E.1 -> E.2 -> E.3 chain and closes Block E as an
observability-only compression specimen. It does not create registry, reuse,
radius, proceed, machine-action, source-replacement, or runner authority.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_compression_specimen_closure_v0.py"
E1_JSON = "docs/matrixlabs/compression/c8_n22_authority_action_trace_compression_target_v0.json"
E2_JSON = "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_compressed_packet_v0.json"
E3_JSON = "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_decompression_audit_v0.json"
OUTPUT_JSON = "docs/matrixlabs/compression/c8_n22_compression_specimen_closure_v0.json"
OUTPUT_MD = "docs/matrixlabs/compression/c8_n22_compression_specimen_closure_v0.md"

SCHEMA_VERSION = "matrixlabs_compression_specimen_closure_v0"
COMPRESSION_CLOSURE_ID = "c8.n22.compression_specimen_closure.v0"
CLOSURE_ROLE = "BLOCK_E_COMPRESSION_SPECIMEN_CLOSURE"
CLOSURE_STATUS = "COMPRESSION_CLOSURE_PASS_OBSERVABILITY_ONLY"
BLOCK_ID = "BLOCK_E"
BLOCK_STATUS = "BLOCK_E_PASS_OBSERVABILITY_COMPRESSION_WITH_DECOMPRESSION_PARITY"
COMPRESSION_TARGET_ID = "c8.n22.authority_action_trace.compression_target.v0"
COMPRESSED_PACKET_ID = "c8.n22.radius_bound_prepare_trace.compressed_packet.v0"
DECOMPRESSION_AUDIT_ID = "c8.n22.radius_bound_prepare_trace.decompression_audit.v0"
DECOMPRESSION_AUDIT_STATUS = "DECOMPRESSION_AUDIT_PASS_CRITICAL_FIELD_PARITY"
AUDIT_SCOPE = "E1_DECLARED_CRITICAL_FIELD_PARITY_ONLY"
PACKET_STATUS = "COMPRESSED_PACKET_CREATED_PENDING_DECOMPRESSION_AUDIT"
TARGET_TRACE_LABEL = "C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0"
COMPRESSION_MODE = "OBSERVABILITY_COMPRESSION_ONLY"
ALLOWED_USE = "OBSERVABILITY_SHORTCUT_ONLY"
NEXT_SURFACE = "COMPRESSION_REGISTRY_CANDIDATE_SURFACE"
NEXT_SURFACE_STATUS = "POSSIBLE_SEPARATE_SURFACE_NOT_CREATED"
RADIUS_LIMIT = "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT"
PRECOMMIT_GATE = "PASS"
TERMINAL_TRANSITION = "STOP_BLOCK_E_COMPRESSION_CLOSURE_COMPLETE"

FAIL_COMPRESSION_TARGET_MISSING = "COMPRESSION_CLOSURE_FAIL_COMPRESSION_TARGET_MISSING"
FAIL_COMPRESSED_PACKET_MISSING = "COMPRESSION_CLOSURE_FAIL_COMPRESSED_PACKET_MISSING"
FAIL_DECOMPRESSION_AUDIT_MISSING = "COMPRESSION_CLOSURE_FAIL_DECOMPRESSION_AUDIT_MISSING"
FAIL_DECOMPRESSION_AUDIT_NOT_PASS = "COMPRESSION_CLOSURE_FAIL_DECOMPRESSION_AUDIT_NOT_PASS"
FAIL_TRACE_LABEL_MISMATCH = "COMPRESSION_CLOSURE_FAIL_TRACE_LABEL_MISMATCH"
FAIL_COMPRESSION_MODE_MISMATCH = "COMPRESSION_CLOSURE_FAIL_COMPRESSION_MODE_MISMATCH"
FAIL_SOURCE_HASH_MISMATCH = "COMPRESSION_CLOSURE_FAIL_SOURCE_HASH_MISMATCH"
FAIL_SOURCE_AUTHORITY_REPLACED = "COMPRESSION_CLOSURE_FAIL_SOURCE_AUTHORITY_REPLACED"
FAIL_ALLOWED_USE_OVERBROAD = "COMPRESSION_CLOSURE_FAIL_ALLOWED_USE_OVERBROAD"
FAIL_REUSE_AUTHORIZED = "COMPRESSION_CLOSURE_FAIL_REUSE_AUTHORIZED"
FAIL_RADIUS_RENEWED = "COMPRESSION_CLOSURE_FAIL_RADIUS_RENEWED"
FAIL_ADDITIONAL_RADIUS_CREATED = "COMPRESSION_CLOSURE_FAIL_ADDITIONAL_RADIUS_CREATED"
FAIL_ADDITIONAL_PROCEED_AUTHORIZED = "COMPRESSION_CLOSURE_FAIL_ADDITIONAL_PROCEED_AUTHORIZED"
FAIL_MACHINE_ACTION_PERFORMED = "COMPRESSION_CLOSURE_FAIL_MACHINE_ACTION_PERFORMED"
FAIL_AUTHORITY_CHANGED = "COMPRESSION_CLOSURE_FAIL_AUTHORITY_CHANGED"
FAIL_REGISTRY_CANDIDATE_SURFACE_CREATED = "COMPRESSION_CLOSURE_FAIL_REGISTRY_CANDIDATE_SURFACE_CREATED"
FAIL_REGISTRY_ENTRY_CREATED = "COMPRESSION_CLOSURE_FAIL_REGISTRY_ENTRY_CREATED"
FAIL_ACTIVE_REGISTRY_CREATED = "COMPRESSION_CLOSURE_FAIL_ACTIVE_REGISTRY_CREATED"
FAIL_RUNNER_AUTHORITY_CREATED = "COMPRESSION_CLOSURE_FAIL_RUNNER_AUTHORITY_CREATED"
FAIL_NEXT_SURFACE_CREATED_INSIDE_CLOSURE = "COMPRESSION_CLOSURE_FAIL_NEXT_SURFACE_CREATED_INSIDE_CLOSURE"
FAIL_E3_SCOPE_UPGRADED = "COMPRESSION_CLOSURE_FAIL_E3_SCOPE_UPGRADED_TO_GLOBAL_EQUIVALENCE"
FAIL_PACKET_STATUS_REWRITTEN = "COMPRESSION_CLOSURE_FAIL_PACKET_STATUS_REWRITTEN"

FAILURE_VOCABULARY = [
    FAIL_COMPRESSION_TARGET_MISSING,
    FAIL_COMPRESSED_PACKET_MISSING,
    FAIL_DECOMPRESSION_AUDIT_MISSING,
    FAIL_DECOMPRESSION_AUDIT_NOT_PASS,
    FAIL_TRACE_LABEL_MISMATCH,
    FAIL_COMPRESSION_MODE_MISMATCH,
    FAIL_SOURCE_HASH_MISMATCH,
    FAIL_SOURCE_AUTHORITY_REPLACED,
    FAIL_ALLOWED_USE_OVERBROAD,
    FAIL_REUSE_AUTHORIZED,
    FAIL_RADIUS_RENEWED,
    FAIL_ADDITIONAL_RADIUS_CREATED,
    FAIL_ADDITIONAL_PROCEED_AUTHORIZED,
    FAIL_MACHINE_ACTION_PERFORMED,
    FAIL_AUTHORITY_CHANGED,
    FAIL_REGISTRY_CANDIDATE_SURFACE_CREATED,
    FAIL_REGISTRY_ENTRY_CREATED,
    FAIL_ACTIVE_REGISTRY_CREATED,
    FAIL_RUNNER_AUTHORITY_CREATED,
    FAIL_NEXT_SURFACE_CREATED_INSIDE_CLOSURE,
    FAIL_E3_SCOPE_UPGRADED,
    FAIL_PACKET_STATUS_REWRITTEN,
]

MARKDOWN_FORBIDDEN_PHRASES = [
    "active registry created",
    "safe to automate",
    "machine can now continue",
    "compressed packet is canonical authority",
    "runner ready",
    "registry use authorized",
    "reuse authorized",
    "radius renewed",
    "machine proceed authorized",
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
        fail(FAIL_SOURCE_HASH_MISMATCH, proc.stderr.strip())
    return Path(proc.stdout.strip()).resolve()


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def load_committed_json(
    root: Path,
    relative_path: str,
    missing_code: str,
) -> tuple[dict[str, Any], str]:
    path = root / relative_path
    try:
        content = path.read_bytes()
    except FileNotFoundError:
        fail(missing_code, relative_path)
    try:
        data = json.loads(content)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(missing_code, f"{relative_path}: {exc}")

    proc = subprocess.run(
        ["git", "show", f"HEAD:{relative_path}"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(FAIL_SOURCE_HASH_MISMATCH, f"{relative_path}: not present in HEAD")
    digest = sha256_bytes(content)
    committed_digest = sha256_bytes(proc.stdout)
    if digest != committed_digest:
        fail(
            FAIL_SOURCE_HASH_MISMATCH,
            f"{relative_path}: working={digest} HEAD={committed_digest}",
        )
    return data, digest


def expect(
    value: object,
    wanted: object,
    failure_code: str,
    field: str,
) -> None:
    if value != wanted:
        fail(failure_code, f"{field}: {value!r}!={wanted!r}")


def expect_false(value: object, failure_code: str, field: str) -> None:
    expect(value, False, failure_code, field)


def validate_source_chain(
    e1: dict[str, Any],
    e2: dict[str, Any],
    e3: dict[str, Any],
) -> None:
    expect(e1.get("schema_version"), "matrixlabs_compression_target_declaration_v0", FAIL_COMPRESSION_TARGET_MISSING, "e1.schema_version")
    expect(e1.get("compression_target_id"), COMPRESSION_TARGET_ID, FAIL_COMPRESSION_TARGET_MISSING, "e1.compression_target_id")
    expect(e2.get("schema_version"), "matrixlabs_compressed_trace_packet_v0", FAIL_COMPRESSED_PACKET_MISSING, "e2.schema_version")
    expect(e2.get("compressed_packet_id"), COMPRESSED_PACKET_ID, FAIL_COMPRESSED_PACKET_MISSING, "e2.compressed_packet_id")
    expect(e2.get("source_compression_target_id"), COMPRESSION_TARGET_ID, FAIL_SOURCE_HASH_MISMATCH, "e2.source_compression_target_id")
    expect(e3.get("schema_version"), "matrixlabs_decompression_parity_audit_v0", FAIL_DECOMPRESSION_AUDIT_MISSING, "e3.schema_version")
    expect(e3.get("decompression_audit_id"), DECOMPRESSION_AUDIT_ID, FAIL_DECOMPRESSION_AUDIT_MISSING, "e3.decompression_audit_id")
    expect(e3.get("source_compression_target_id"), COMPRESSION_TARGET_ID, FAIL_SOURCE_HASH_MISMATCH, "e3.source_compression_target_id")
    expect(e3.get("source_compressed_packet_id"), COMPRESSED_PACKET_ID, FAIL_SOURCE_HASH_MISMATCH, "e3.source_compressed_packet_id")

    for label, source in [("e1", e1), ("e2", e2), ("e3", e3)]:
        expect(source.get("target_trace_label"), TARGET_TRACE_LABEL, FAIL_TRACE_LABEL_MISMATCH, f"{label}.target_trace_label")
        expect(source.get("compression_mode"), COMPRESSION_MODE, FAIL_COMPRESSION_MODE_MISMATCH, f"{label}.compression_mode")

    expect(e2.get("packet_status"), PACKET_STATUS, FAIL_PACKET_STATUS_REWRITTEN, "e2.packet_status")
    expect(
        e2.get("source_artifacts_copied_from_e1", {}).get("source_artifacts"),
        e1.get("source_artifacts"),
        FAIL_SOURCE_HASH_MISMATCH,
        "e2.source_artifacts_copied_from_e1.source_artifacts",
    )
    expect(
        e2.get("source_artifacts_copied_from_e1", {}).get("supporting_source_artifacts"),
        e1.get("supporting_source_artifacts"),
        FAIL_SOURCE_HASH_MISMATCH,
        "e2.source_artifacts_copied_from_e1.supporting_source_artifacts",
    )

    identity = e3.get("source_identity_integrity", {})
    for field in [
        "e1_source_refs_loaded",
        "e2_copied_source_refs_match_e1",
        "e2_copied_source_hashes_match_e1",
        "source_files_exist",
        "source_file_hashes_match_e1_manifest",
    ]:
        expect(identity.get(field), True, FAIL_SOURCE_HASH_MISMATCH, f"e3.source_identity_integrity.{field}")

    result = e3.get("audit_result", {})
    expect(result.get("decompression_audit_status"), DECOMPRESSION_AUDIT_STATUS, FAIL_DECOMPRESSION_AUDIT_NOT_PASS, "e3.audit_result.decompression_audit_status")
    expect(result.get("all_critical_field_groups_recovered"), True, FAIL_DECOMPRESSION_AUDIT_NOT_PASS, "e3.audit_result.all_critical_field_groups_recovered")
    expect(result.get("eligible_for_e4_observability_closure"), True, FAIL_DECOMPRESSION_AUDIT_NOT_PASS, "e3.audit_result.eligible_for_e4_observability_closure")
    expect_false(result.get("block_e_closed_by_e3"), FAIL_AUTHORITY_CHANGED, "e3.audit_result.block_e_closed_by_e3")
    expect_false(result.get("compression_closed_by_e3"), FAIL_AUTHORITY_CHANGED, "e3.audit_result.compression_closed_by_e3")

    packet_after = e3.get("packet_audit_status_after_e3", {})
    expect(packet_after.get("source_packet_status_before_audit"), PACKET_STATUS, FAIL_PACKET_STATUS_REWRITTEN, "e3.packet_audit_status_after_e3.source_packet_status_before_audit")
    expect(packet_after.get("decompression_audit_status"), DECOMPRESSION_AUDIT_STATUS, FAIL_DECOMPRESSION_AUDIT_NOT_PASS, "e3.packet_audit_status_after_e3.decompression_audit_status")
    expect_false(packet_after.get("packet_source_record_rewritten"), FAIL_PACKET_STATUS_REWRITTEN, "e3.packet_audit_status_after_e3.packet_source_record_rewritten")
    expect_false(packet_after.get("block_e_closed_by_e3"), FAIL_AUTHORITY_CHANGED, "e3.packet_audit_status_after_e3.block_e_closed_by_e3")
    expect_false(packet_after.get("compression_closed_by_e3"), FAIL_AUTHORITY_CHANGED, "e3.packet_audit_status_after_e3.compression_closed_by_e3")

    scope = e3.get("audit_scope_boundary", {})
    expect(scope.get("audit_scope"), AUDIT_SCOPE, FAIL_E3_SCOPE_UPGRADED, "e3.audit_scope_boundary.audit_scope")
    expect_false(scope.get("full_trace_equivalence_claimed"), FAIL_E3_SCOPE_UPGRADED, "e3.audit_scope_boundary.full_trace_equivalence_claimed")
    expect_false(scope.get("all_possible_fields_audited"), FAIL_E3_SCOPE_UPGRADED, "e3.audit_scope_boundary.all_possible_fields_audited")
    expect_false(scope.get("authority_transfer_performed"), FAIL_AUTHORITY_CHANGED, "e3.audit_scope_boundary.authority_transfer_performed")
    expect_false(scope.get("observability_closure_performed"), FAIL_AUTHORITY_CHANGED, "e3.audit_scope_boundary.observability_closure_performed")

    packet_boundary = e2.get("packet_boundary", {})
    for field, code in {
        "packet_may_replace_source_authority": FAIL_SOURCE_AUTHORITY_REPLACED,
        "packet_replaces_source_authority": FAIL_SOURCE_AUTHORITY_REPLACED,
        "packet_authorizes_reuse": FAIL_REUSE_AUTHORIZED,
        "packet_renews_radius": FAIL_RADIUS_RENEWED,
        "packet_authorizes_additional_machine_proceed": FAIL_ADDITIONAL_PROCEED_AUTHORIZED,
        "packet_creates_runner_authority": FAIL_RUNNER_AUTHORITY_CREATED,
        "packet_performs_machine_action": FAIL_MACHINE_ACTION_PERFORMED,
        "packet_grants_authority": FAIL_AUTHORITY_CHANGED,
    }.items():
        expect_false(packet_boundary.get(field), code, f"e2.packet_boundary.{field}")
    expect(packet_boundary.get("source_records_remain_authority"), True, FAIL_SOURCE_AUTHORITY_REPLACED, "e2.packet_boundary.source_records_remain_authority")

    e2_effects = e2.get("confirmed_non_effects", {})
    expect_false(e2_effects.get("additional_radius_created"), FAIL_ADDITIONAL_RADIUS_CREATED, "e2.confirmed_non_effects.additional_radius_created")
    expect_false(e2_effects.get("runner_authority_created"), FAIL_RUNNER_AUTHORITY_CREATED, "e2.confirmed_non_effects.runner_authority_created")

    e3_safety = e3.get("authority_safety_checks", {})
    for field, code in {
        "compressed_packet_replaces_source_authority": FAIL_SOURCE_AUTHORITY_REPLACED,
        "authority_strengthened_by_compression": FAIL_AUTHORITY_CHANGED,
        "reuse_authorized_by_compression": FAIL_REUSE_AUTHORIZED,
        "radius_renewed_by_compression": FAIL_RADIUS_RENEWED,
        "additional_machine_proceed_authorized_by_compression": FAIL_ADDITIONAL_PROCEED_AUTHORIZED,
        "runner_authority_created_by_compression": FAIL_RUNNER_AUTHORITY_CREATED,
        "registry_created_by_decompression_audit": FAIL_REGISTRY_ENTRY_CREATED,
        "block_e_closed_by_decompression_audit": FAIL_AUTHORITY_CHANGED,
    }.items():
        expect_false(e3_safety.get(field), code, f"e3.authority_safety_checks.{field}")

    e3_effects = e3.get("audit_non_effects", {})
    for field, code in {
        "decompression_audit_closes_block_e": FAIL_AUTHORITY_CHANGED,
        "decompression_audit_creates_registry_entry": FAIL_REGISTRY_ENTRY_CREATED,
        "decompression_audit_performs_machine_action": FAIL_MACHINE_ACTION_PERFORMED,
        "decompression_audit_changes_authority": FAIL_AUTHORITY_CHANGED,
        "decompression_audit_renews_radius": FAIL_RADIUS_RENEWED,
        "decompression_audit_creates_runner_authority": FAIL_RUNNER_AUTHORITY_CREATED,
    }.items():
        expect_false(e3_effects.get(field), code, f"e3.audit_non_effects.{field}")


def closure_source_integrity() -> dict[str, bool]:
    return {
        "compression_target_present": True,
        "compressed_packet_present": True,
        "decompression_audit_present": True,
        "compression_target_hash_verified": True,
        "compressed_packet_hash_verified": True,
        "decompression_audit_hash_verified": True,
        "e3_audit_passed": True,
        "e3_field_level_audit_reperformed_by_e4": False,
    }


def closure_recognition() -> dict[str, Any]:
    return {
        "source_packet_status_remains": PACKET_STATUS,
        "e3_decompression_audit_status": DECOMPRESSION_AUDIT_STATUS,
        "e3_audit_scope": AUDIT_SCOPE,
        "e4_closure_recognizes_packet_as": "OBSERVABILITY_SHORTCUT_ONLY_WITH_PARITY_AUDIT",
        "source_packet_record_rewritten_by_e4": False,
        "full_trace_equivalence_claimed": False,
        "all_possible_fields_audited": False,
    }


def compressed_trace() -> dict[str, Any]:
    return {
        "trace_label": TARGET_TRACE_LABEL,
        "compression_mode": COMPRESSION_MODE,
        "compressed_packet_status_before_closure": PACKET_STATUS,
        "decompression_audit_status": DECOMPRESSION_AUDIT_STATUS,
        "e3_audit_scope": AUDIT_SCOPE,
        "closure_allowed_use": ALLOWED_USE,
        "packet_source_record_rewritten_by_closure": False,
    }


def closure_result() -> dict[str, Any]:
    return {
        "decompression_parity_audit_passed": True,
        "critical_fields_preserved_by_audit": True,
        "compressed_packet_may_be_displayed_as_observability_shortcut": True,
        "compressed_packet_may_replace_source_authority": False,
        "compressed_packet_may_authorize_reuse": False,
        "compressed_packet_may_renew_radius": False,
        "compressed_packet_may_authorize_additional_machine_proceed": False,
        "compressed_packet_may_create_runner_authority": False,
        "block_e_closed_by_e4": True,
        "block_e_closed_as": "OBSERVABILITY_COMPRESSION_WITH_DECOMPRESSION_PARITY",
        "block_e_closure_authorizes_future_action": False,
    }


def allowed_use() -> dict[str, Any]:
    return {
        "allowed_use_class": ALLOWED_USE,
        "human_overview": True,
        "indexing": True,
        "search": True,
        "trace_comparison": True,
        "dashboard_projection": True,
        "future_analysis": True,
        "authority_decision_source": False,
        "automated_decision_source": False,
        "reuse_authorization_source": False,
        "radius_renewal_source": False,
        "machine_proceed_source": False,
        "runner_source": False,
        "registry_activation_source": False,
        "schema_promotion_source": False,
    }


def source_of_truth_rule() -> dict[str, Any]:
    return {
        "formal_source_chain_remains_authority": True,
        "compressed_packet_is_projection_or_index": True,
        "compressed_packet_can_be_invalidated_by_source_mismatch": True,
        "compressed_packet_cannot_override_source": True,
        "compressed_packet_cannot_satisfy_source_record_requirement": True,
        "source_authority_chain": [
            "c8.n22.authority_transition_closure.v0",
            "c8.n22.router_specimen_closure.v0",
            "c8.n22.candidate_archive_entry.admissibility_audit.v0",
            "c8.n22.machine_proceed_closure.v0",
        ],
    }


def radius_boundary() -> dict[str, Any]:
    return {
        "source_radius_limit": RADIUS_LIMIT,
        "source_radius_after": 0,
        "source_radius_exhausted": True,
        "radius_renewed_by_compression_closure": False,
        "additional_radius_created_by_compression_closure": False,
        "additional_machine_proceed_authorized": False,
        "same_radius_may_be_reused": False,
        "additional_use_requires_new_authority_or_radius": True,
    }


def registry_boundary() -> dict[str, bool]:
    return {
        "may_be_cited_as_evidence_in_future_registry_candidate_surface": True,
        "registry_candidate_surface_created_by_this_closure": False,
        "registry_entry_created_by_this_closure": False,
        "registry_use_authorized": False,
        "active_registry_created": False,
        "active_registry_created_by_this_closure": False,
        "requires_separate_registry_candidate_surface": True,
        "requires_separate_human_decision_before_registry_reuse": True,
    }


def confirmed_non_effects() -> dict[str, bool]:
    return {
        "authority_changed_by_closure": False,
        "source_records_replaced_by_closure": False,
        "reuse_authorized_by_closure": False,
        "radius_renewed_by_closure": False,
        "additional_radius_created_by_closure": False,
        "additional_machine_proceed_authorized_by_closure": False,
        "machine_action_performed_by_closure": False,
        "created_next_unit_executed_by_closure": False,
        "registry_candidate_surface_created_by_closure": False,
        "registry_entry_created_by_closure": False,
        "active_registry_created_by_closure": False,
        "runner_authority_created_by_closure": False,
        "active_archive_scope_expanded_by_closure": False,
    }


def next_possible_separate_surface() -> dict[str, Any]:
    return {
        "surface": NEXT_SURFACE,
        "surface_status": NEXT_SURFACE_STATUS,
        "created_by_this_closure": False,
        "authorized_by_this_closure": False,
        "selected_as_next_unit_by_this_closure": False,
        "requires_separate_human_decision_before_registry_use": True,
    }


def closure_gate() -> dict[str, Any]:
    return {
        "compression_closure_gate": CLOSURE_STATUS,
        "compression_target_present": True,
        "compressed_packet_present": True,
        "decompression_audit_present": True,
        "compression_target_hash_verified": True,
        "compressed_packet_hash_verified": True,
        "decompression_audit_hash_verified": True,
        "decompression_audit_status": DECOMPRESSION_AUDIT_STATUS,
        "decompression_audit_passed": True,
        "critical_fields_preserved": True,
        "e3_audit_scope": AUDIT_SCOPE,
        "full_trace_equivalence_claimed": False,
        "all_possible_fields_audited": False,
        "target_trace_label": TARGET_TRACE_LABEL,
        "compression_mode": COMPRESSION_MODE,
        "allowed_use": ALLOWED_USE,
        "compressed_packet_may_be_displayed_as_observability_shortcut": True,
        "source_records_remain_authority": True,
        "compressed_packet_may_replace_source_authority": False,
        "compressed_packet_may_authorize_reuse": False,
        "compressed_packet_may_renew_radius": False,
        "compressed_packet_may_authorize_additional_machine_proceed": False,
        "compressed_packet_may_create_runner_authority": False,
        "radius_limit": RADIUS_LIMIT,
        "radius_after": 0,
        "radius_exhausted": True,
        "radius_renewed_by_closure": False,
        "additional_radius_created_by_closure": False,
        "machine_action_performed_by_closure": False,
        "authority_changed_by_closure": False,
        "registry_candidate_surface_created_by_closure": False,
        "registry_entry_created_by_closure": False,
        "active_registry_created_by_closure": False,
        "runner_authority_created_by_closure": False,
        "next_possible_separate_surface": NEXT_SURFACE,
        "next_possible_separate_surface_created_by_this_closure": False,
        "next_possible_separate_surface_authorized_by_this_closure": False,
        "failures": [],
    }


def build_record(source_hashes: dict[str, str]) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "compression_closure_id": COMPRESSION_CLOSURE_ID,
        "closure_role": CLOSURE_ROLE,
        "closure_status": CLOSURE_STATUS,
        "block": {
            "block_id": BLOCK_ID,
            "block_status": BLOCK_STATUS,
            "block_closed": True,
        },
        "source_chain": {
            "compression_target_id": COMPRESSION_TARGET_ID,
            "compressed_packet_id": COMPRESSED_PACKET_ID,
            "decompression_audit_id": DECOMPRESSION_AUDIT_ID,
        },
        "source_chain_file_hash_algorithm": "sha256",
        "source_chain_file_hashes": source_hashes,
        "source_chain_hash_verification_basis": "WORKTREE_FILE_MATCHES_HEAD_BLOB",
        "target_trace_label": TARGET_TRACE_LABEL,
        "compression_mode": COMPRESSION_MODE,
        "closure_source_integrity": closure_source_integrity(),
        "closure_recognition": closure_recognition(),
        "compressed_trace": compressed_trace(),
        "closure_result": closure_result(),
        "allowed_use": allowed_use(),
        "source_of_truth_rule": source_of_truth_rule(),
        "radius_boundary": radius_boundary(),
        "registry_boundary": registry_boundary(),
        "confirmed_non_effects": confirmed_non_effects(),
        "next_possible_separate_surface": next_possible_separate_surface(),
        "closure_gate": closure_gate(),
        "failure_vocabulary": FAILURE_VOCABULARY,
        "non_claims": [
            "E.4 does not create the compressed packet.",
            "E.4 does not perform decompression audit.",
            "E.4 does not create a compression registry.",
            "E.4 does not create an active registry.",
            "E.4 does not replace source records.",
            "E.4 does not authorize reuse.",
            "E.4 does not renew radius.",
            "E.4 does not authorize another machine proceed.",
            "E.4 does not perform machine action.",
            "E.4 does not execute the created next unit.",
            "E.4 does not expand active archive scope.",
            "E.4 does not create runner authority.",
            "E.4 only closes the compression specimen as an observability-only shortcut after E.3 parity pass.",
        ],
        "key_non_claims": [
            "compression closure ≠ registry entry",
            "observability shortcut ≠ source authority",
            "decompression parity ≠ reuse authorization",
            "compressed trace label ≠ runner permission",
            "Block E closure ≠ active registry",
            "Block E closure ≠ machine proceed authority",
        ],
        "precommit_c8_n22_compression_closure_gate": PRECOMMIT_GATE,
        "compression_closure_gate": CLOSURE_STATUS,
        "terminal_transition": TERMINAL_TRANSITION,
        "generated_by": GENERATOR,
    }


def validate_record(record: dict[str, Any]) -> None:
    expect(record.get("schema_version"), SCHEMA_VERSION, FAIL_SOURCE_HASH_MISMATCH, "schema_version")
    expect(record.get("compression_closure_id"), COMPRESSION_CLOSURE_ID, FAIL_SOURCE_HASH_MISMATCH, "compression_closure_id")
    expect(record.get("closure_role"), CLOSURE_ROLE, FAIL_AUTHORITY_CHANGED, "closure_role")
    expect(record.get("closure_status"), CLOSURE_STATUS, FAIL_ALLOWED_USE_OVERBROAD, "closure_status")
    expect(record["block"].get("block_closed"), True, FAIL_AUTHORITY_CHANGED, "block.block_closed")
    expect(record["allowed_use"].get("allowed_use_class"), ALLOWED_USE, FAIL_ALLOWED_USE_OVERBROAD, "allowed_use.allowed_use_class")
    for field in [
        "authority_decision_source",
        "automated_decision_source",
        "reuse_authorization_source",
        "radius_renewal_source",
        "machine_proceed_source",
        "runner_source",
        "registry_activation_source",
        "schema_promotion_source",
    ]:
        expect_false(record["allowed_use"].get(field), FAIL_ALLOWED_USE_OVERBROAD, f"allowed_use.{field}")
    for field, value in record["confirmed_non_effects"].items():
        expect_false(value, FAIL_AUTHORITY_CHANGED, f"confirmed_non_effects.{field}")
    expect(record["closure_gate"].get("failures"), [], FAIL_SOURCE_HASH_MISMATCH, "closure_gate.failures")
    expect(record.get("terminal_transition"), TERMINAL_TRANSITION, FAIL_NEXT_SURFACE_CREATED_INSIDE_CLOSURE, "terminal_transition")


def render_markdown() -> str:
    return f"""# C8 n22 compression specimen closure v0

## Status

{CLOSURE_STATUS}

## Block

{BLOCK_STATUS}

## Trace label

{TARGET_TRACE_LABEL}

## Source chain

- compression target: {COMPRESSION_TARGET_ID}
- compressed packet: {COMPRESSED_PACKET_ID}
- decompression audit: {DECOMPRESSION_AUDIT_ID}

## Decompression result

{DECOMPRESSION_AUDIT_STATUS}

## Audit scope preserved

{AUDIT_SCOPE}

This closure does not claim full trace equivalence or all-possible-field audit.

## Allowed use

{ALLOWED_USE}

## Source of truth

The formal source chain remains authority.

## Confirmed boundaries

- compressed packet does not replace source authority
- compressed packet does not authorize reuse
- compressed packet does not renew radius
- compressed packet does not authorize another machine proceed
- compressed packet does not create runner authority
- closure does not create a registry candidate surface
- closure does not create a registry entry
- closure does not create an active registry

## Radius state preserved

- radius limit: {RADIUS_LIMIT}
- radius after source proceed: 0
- radius exhausted: true
- additional radius created by closure: false

## Next possible separate surface

{NEXT_SURFACE}

Status: {NEXT_SURFACE_STATUS}

## Non-claim

This closure does not create that registry surface, authorize registry use, replace source authority, renew radius, authorize reuse, authorize another proceed, perform machine action, execute the created next unit, or create runner authority.
"""


def validate_markdown(text: str) -> None:
    lowered = text.lower()
    hits = [phrase for phrase in MARKDOWN_FORBIDDEN_PHRASES if phrase in lowered]
    if hits:
        fail(FAIL_ALLOWED_USE_OVERBROAD, ",".join(hits))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_outputs(root: Path, record: dict[str, Any]) -> None:
    markdown = render_markdown()
    validate_markdown(markdown)
    write_text(root / OUTPUT_JSON, json.dumps(record, indent=2, sort_keys=True) + "\n")
    write_text(root / OUTPUT_MD, markdown)


def bool_text(value: bool) -> str:
    return str(value).lower()


def print_success(record: dict[str, Any]) -> None:
    integrity = record["closure_source_integrity"]
    recognition = record["closure_recognition"]
    result = record["closure_result"]
    source_rule = record["source_of_truth_rule"]
    radius = record["radius_boundary"]
    registry = record["registry_boundary"]
    effects = record["confirmed_non_effects"]
    next_surface = record["next_possible_separate_surface"]
    print("BUILD_C8_N22_COMPRESSION_SPECIMEN_CLOSURE_V0_COMPLETE")
    print(f"compression_closure_id={record['compression_closure_id']}")
    print(f"schema_version={record['schema_version']}")
    print(f"closure_role={record['closure_role']}")
    print(f"closure_status={record['closure_status']}")
    print(f"block_id={record['block']['block_id']}")
    print(f"block_status={record['block']['block_status']}")
    print(f"block_closed={bool_text(record['block']['block_closed'])}")
    for key in ["compression_target_id", "compressed_packet_id", "decompression_audit_id"]:
        print(f"{key}={record['source_chain'][key]}")
    print(f"target_trace_label={record['target_trace_label']}")
    print(f"compression_mode={record['compression_mode']}")
    for key in [
        "compression_target_hash_verified",
        "compressed_packet_hash_verified",
        "decompression_audit_hash_verified",
        "e3_audit_passed",
    ]:
        print(f"{key}={bool_text(integrity[key])}")
    print(f"e3_audit_scope={recognition['e3_audit_scope']}")
    print(f"e3_field_level_audit_reperformed_by_e4={bool_text(integrity['e3_field_level_audit_reperformed_by_e4'])}")
    print(f"source_packet_status_remains={recognition['source_packet_status_remains']}")
    print(f"e3_decompression_audit_status={recognition['e3_decompression_audit_status']}")
    print(f"e4_closure_recognizes_packet_as={recognition['e4_closure_recognizes_packet_as']}")
    print(f"source_packet_record_rewritten_by_e4={bool_text(recognition['source_packet_record_rewritten_by_e4'])}")
    print(f"full_trace_equivalence_claimed={bool_text(recognition['full_trace_equivalence_claimed'])}")
    print(f"all_possible_fields_audited={bool_text(recognition['all_possible_fields_audited'])}")
    for key in [
        "decompression_parity_audit_passed",
        "critical_fields_preserved_by_audit",
        "compressed_packet_may_be_displayed_as_observability_shortcut",
    ]:
        print(f"{key}={bool_text(result[key])}")
    print(f"allowed_use={record['allowed_use']['allowed_use_class']}")
    for key in [
        "formal_source_chain_remains_authority",
        "compressed_packet_is_projection_or_index",
        "compressed_packet_cannot_override_source",
    ]:
        print(f"{key}={bool_text(source_rule[key])}")
    for key in [
        "compressed_packet_may_replace_source_authority",
        "compressed_packet_may_authorize_reuse",
        "compressed_packet_may_renew_radius",
        "compressed_packet_may_authorize_additional_machine_proceed",
        "compressed_packet_may_create_runner_authority",
    ]:
        print(f"{key}={bool_text(result[key])}")
    print(f"source_radius_limit={radius['source_radius_limit']}")
    print(f"source_radius_after={radius['source_radius_after']}")
    print(f"source_radius_exhausted={bool_text(radius['source_radius_exhausted'])}")
    for key in [
        "radius_renewed_by_compression_closure",
        "additional_radius_created_by_compression_closure",
        "additional_machine_proceed_authorized",
        "same_radius_may_be_reused",
    ]:
        print(f"{key}={bool_text(radius[key])}")
    for key in [
        "may_be_cited_as_evidence_in_future_registry_candidate_surface",
        "registry_candidate_surface_created_by_this_closure",
        "registry_entry_created_by_this_closure",
        "registry_use_authorized",
        "active_registry_created",
        "active_registry_created_by_this_closure",
    ]:
        print(f"{key}={bool_text(registry[key])}")
    for key, value in effects.items():
        print(f"{key}={bool_text(value)}")
    print(f"next_possible_separate_surface={next_surface['surface']}")
    print(f"next_possible_separate_surface_status={next_surface['surface_status']}")
    print(f"next_possible_separate_surface_created_by_this_closure={bool_text(next_surface['created_by_this_closure'])}")
    print(f"next_possible_separate_surface_authorized_by_this_closure={bool_text(next_surface['authorized_by_this_closure'])}")
    print(f"selected_as_next_unit_by_this_closure={bool_text(next_surface['selected_as_next_unit_by_this_closure'])}")
    print(f"compression_closure_gate={record['compression_closure_gate']}")
    print(f"precommit_c8_n22_compression_closure_gate={record['precommit_c8_n22_compression_closure_gate']}")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition={record['terminal_transition']}")


def main() -> int:
    try:
        root = detect_repo_root(Path.cwd())
        e1, e1_hash = load_committed_json(root, E1_JSON, FAIL_COMPRESSION_TARGET_MISSING)
        e2, e2_hash = load_committed_json(root, E2_JSON, FAIL_COMPRESSED_PACKET_MISSING)
        e3, e3_hash = load_committed_json(root, E3_JSON, FAIL_DECOMPRESSION_AUDIT_MISSING)
        validate_source_chain(e1, e2, e3)
        record = build_record(
            {
                E1_JSON: e1_hash,
                E2_JSON: e2_hash,
                E3_JSON: e3_hash,
            }
        )
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
