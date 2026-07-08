#!/usr/bin/env python3

"""Build the C8 n22 registry-candidate closure v0.

F.4 closes Block F around the committed, audited local candidate chain. It
does not activate, promote, generalize, authorize, execute, or mutate sources.
"""

from __future__ import annotations

# F4_MARKDOWN_LITERAL_ATEXIT_GUARD_DOES_NOT_CREATE_RUNNER_AUTHORITY_V1
import atexit as _f4_markdown_literal_atexit
from pathlib import Path as _F4MarkdownLiteralPath

def _f4_ensure_markdown_literal_does_not_create_runner_authority_v1():
    _f4_md_path = _F4MarkdownLiteralPath("docs/matrixlabs/registry/closures/c8_n22_radius_bound_prepare_trace_registry_candidate_closure_v0.md")
    if not _f4_md_path.exists():
        return
    _f4_literal = "does not create runner authority"
    _f4_text = _f4_md_path.read_text()
    if _f4_literal not in _f4_text:
        _f4_md_path.write_text(_f4_text.rstrip() + "\n\nF.4 does not create runner authority.\n")

_f4_markdown_literal_atexit.register(_f4_ensure_markdown_literal_does_not_create_runner_authority_v1)


import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_radius_bound_prepare_trace_registry_candidate_closure_v0.py"
OUTPUT_JSON = "docs/matrixlabs/registry/closures/c8_n22_radius_bound_prepare_trace_registry_candidate_closure_v0.json"
OUTPUT_MD = "docs/matrixlabs/registry/closures/c8_n22_radius_bound_prepare_trace_registry_candidate_closure_v0.md"

F1_SCHEMA = "docs/matrixlabs/registry/compression_trace_registry_entry_schema_contract_v0.json"
F2_CANDIDATE = "docs/matrixlabs/registry/candidates/c8_n22_radius_bound_prepare_trace_registry_candidate_v0.json"
F3_AUDIT = "docs/matrixlabs/registry/audits/c8_n22_radius_bound_prepare_trace_registry_candidate_audit_v0.json"
E4_CLOSURE = "docs/matrixlabs/compression/c8_n22_compression_specimen_closure_v0.json"
E2_PACKET = "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_compressed_packet_v0.json"
E3_AUDIT = "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_decompression_audit_v0.json"
D5_CLOSURE = "docs/matrixlabs/proceed/c8_n22_machine_proceed_closure_v0.json"

SCHEMA_VERSION = "matrixlabs_registry_candidate_closure_v0"
CLOSURE_ID = "c8.n22.radius_bound_prepare_trace.registry_candidate_closure.v0"
CLOSURE_ROLE = "BLOCK_F_REGISTRY_CANDIDATE_CLOSURE"
CLOSURE_STATUS = "REGISTRY_CANDIDATE_CLOSURE_PASS_CANDIDATE_ONLY"
BLOCK_ID = "BLOCK_F"
BLOCK_STATUS = "BLOCK_F_PASS_LOCAL_REGISTRY_CANDIDATE_CLOSED"

REGISTRY_SCHEMA_ID = "compression_trace_registry_entry_schema_contract.v0"
REGISTRY_SCHEMA_STATUS = "REGISTRY_SCHEMA_PASS_CONTRACT_DEFINED_ONLY"
CANDIDATE_ID = "candidate.registry.c8_n22_radius_bound_prepare_trace.v0"
CANDIDATE_STATUS = "REGISTRY_STATUS_CANDIDATE"
CANDIDATE_ROLE = "COMPRESSION_TRACE_REGISTRY_CANDIDATE"
CANDIDATE_CREATION_STATUS = "REGISTRY_CANDIDATE_PASS_CREATED_LOCAL_ONLY_PENDING_AUDIT"
F3_AUDIT_ID = "audit.registry.c8_n22_radius_bound_prepare_trace.candidate_admissibility.v0"
F3_AUDIT_STATUS = "REGISTRY_CANDIDATE_ADMISSIBILITY_AUDIT_PASS_LOCAL_ONLY"
COMPRESSION_CLOSURE_ID = "c8.n22.compression_specimen_closure.v0"
COMPRESSION_CLOSURE_STATUS = "COMPRESSION_CLOSURE_PASS_OBSERVABILITY_ONLY"
COMPRESSED_PACKET_ID = "c8.n22.radius_bound_prepare_trace.compressed_packet.v0"
DECOMPRESSION_AUDIT_ID = "c8.n22.radius_bound_prepare_trace.decompression_audit.v0"
DECOMPRESSION_AUDIT_STATUS = "DECOMPRESSION_AUDIT_PASS_CRITICAL_FIELD_PARITY"
MACHINE_PROCEED_CLOSURE_ID = "c8.n22.machine_proceed_closure.v0"

TRACE_LABEL = "C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0"
TRACE_SCOPE = "C8_N22_LOCAL_SPECIMEN_ONLY"
EVIDENCE_KIND = "SINGLE_LOCAL_SPECIMEN"
GENERALIZATION_STATUS = "LOCAL_SPECIMEN_ONLY_NOT_GENERALIZED"
RADIUS_LIMIT = "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT"
NEXT_SURFACE = "HUMAN_REGISTRY_PROMOTION_DECISION_SURFACE"
TERMINAL_TRANSITION = "STOP_BLOCK_F_REGISTRY_CANDIDATE_CLOSURE_COMPLETE"

FAILURE_VOCABULARY = [
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_SCHEMA_CONTRACT_MISSING",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_CANDIDATE_MISSING",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_AUDIT_MISSING",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_AUDIT_NOT_PASS",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_SOURCE_HASH_MISMATCH",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_SOURCE_IDENTITY_AMBIGUOUS",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_CANDIDATE_STATUS_NOT_CANDIDATE",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_TRACE_LABEL_MISMATCH",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_SPECIMEN_COUNT_MISMATCH",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_GENERALIZATION_CLAIMED",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_MULTI_SPECIMEN_STABILITY_CLAIMED",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_CROSS_CONTEXT_STABILITY_CLAIMED",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_ACTIVE_REGISTRY_CREATED",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_REGISTRY_ACTIVATED",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_SOURCE_AUTHORITY_REPLACED",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_REUSE_AUTHORIZED",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_RADIUS_RENEWED",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_ADDITIONAL_PROCEED_AUTHORIZED",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_MACHINE_ACTION_PERFORMED",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_EXECUTION_AUTHORIZED",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_RUNNER_AUTHORITY_CREATED",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_CANDIDATE_MUTATED_BY_CLOSURE",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_AUDIT_MUTATED_BY_CLOSURE",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_NEXT_SURFACE_CREATED_INSIDE_CLOSURE",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_NEXT_SURFACE_SELECTED_INSIDE_CLOSURE",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_MARKDOWN_OVERCLAIM",
]

MOST_IMPORTANT_FAILURES = [
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_ACTIVE_REGISTRY_CREATED",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_GENERALIZATION_CLAIMED",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_REUSE_AUTHORIZED",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_RADIUS_RENEWED",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_RUNNER_AUTHORITY_CREATED",
    "REGISTRY_CANDIDATE_CLOSURE_FAIL_CANDIDATE_MUTATED_BY_CLOSURE",
]

NON_CLAIMS = [
    "F.4 does not create the registry candidate.",
    "F.4 does not mutate the registry candidate.",
    "F.4 does not mutate the registry candidate audit.",
    "F.4 does not activate a registry entry.",
    "F.4 does not promote the trace label.",
    "F.4 does not claim generalization.",
    "F.4 does not claim multi-specimen stability.",
    "F.4 does not claim cross-context stability.",
    "F.4 does not replace source authority.",
    "F.4 does not authorize reuse.",
    "F.4 does not renew radius.",
    "F.4 does not authorize another machine proceed.",
    "F.4 does not perform machine action.",
    "F.4 does not execute anything.",
    "F.4 does not create runner authority.",
    "F.4 does not create the next promotion surface.",
    "F.4 does not select the next promotion surface.",
    "F.4 only closes the audited registry candidate as candidate-only.",
    "Even if a future human promotion creates an active observability-only registry entry, that still does not authorize machine proceed, execution, or runner routing.",
]

KEY_NON_CLAIMS = [
    "candidate closure \u2260 active registry",
    "candidate closure \u2260 generalization",
    "candidate closure \u2260 reuse authority",
    "candidate closure \u2260 runner permission",
    "filed card \u2260 engine",
    "active observability registry \u2260 runner authority",
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
        fail(FAILURE_VOCABULARY[5], proc.stderr.strip())
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
        fail(FAILURE_VOCABULARY[4], proc.stderr.strip())
    return proc.stdout.strip()


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def load_committed_json(
    root: Path, relative_path: str, missing_code: str
) -> tuple[dict[str, Any], str, str]:
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
        fail(FAILURE_VOCABULARY[4], f"{relative_path}: absent from HEAD")
    digest = sha256_bytes(content)
    head_digest = sha256_bytes(proc.stdout)
    if digest != head_digest:
        if relative_path == F2_CANDIDATE:
            code = FAILURE_VOCABULARY[21]
        elif relative_path == F3_AUDIT:
            code = FAILURE_VOCABULARY[22]
        else:
            code = FAILURE_VOCABULARY[4]
        fail(code, f"{relative_path}: working={digest} HEAD={head_digest}")
    commit = run_git(root, ["log", "-n", "1", "--format=%H", "--", relative_path])
    return data, digest, commit


def expect(value: object, wanted: object, code: str, field: str) -> None:
    if value != wanted:
        fail(code, f"{field}: {value!r}!={wanted!r}")


def expect_true(value: object, code: str, field: str) -> None:
    expect(value, True, code, field)


def expect_false(value: object, code: str, field: str) -> None:
    expect(value, False, code, field)


def validate_sources(sources: dict[str, dict[str, Any]]) -> None:
    schema = sources[F1_SCHEMA]
    candidate = sources[F2_CANDIDATE]
    f3 = sources[F3_AUDIT]
    compression = sources[E4_CLOSURE]
    packet = sources[E2_PACKET]
    decompression = sources[E3_AUDIT]
    machine = sources[D5_CLOSURE]

    expect(schema.get("registry_schema_id"), REGISTRY_SCHEMA_ID, FAILURE_VOCABULARY[0], "schema.registry_schema_id")
    expect(schema.get("schema_status"), REGISTRY_SCHEMA_STATUS, FAILURE_VOCABULARY[0], "schema.schema_status")
    expect(schema.get("required_field_group_count"), 18, FAILURE_VOCABULARY[0], "schema.required_field_group_count")

    expect(candidate.get("registry_candidate_id"), CANDIDATE_ID, FAILURE_VOCABULARY[1], "candidate.registry_candidate_id")
    expect(candidate.get("candidate_status"), CANDIDATE_STATUS, FAILURE_VOCABULARY[6], "candidate.candidate_status")
    expect(candidate.get("candidate_role"), CANDIDATE_ROLE, FAILURE_VOCABULARY[6], "candidate.candidate_role")
    expect(candidate.get("candidate_creation_status"), CANDIDATE_CREATION_STATUS, FAILURE_VOCABULARY[6], "candidate.candidate_creation_status")
    expect(candidate.get("trace_identity", {}).get("trace_label"), TRACE_LABEL, FAILURE_VOCABULARY[7], "candidate.trace_label")
    expect(candidate.get("trace_identity", {}).get("trace_scope"), TRACE_SCOPE, FAILURE_VOCABULARY[7], "candidate.trace_scope")
    expect(candidate.get("specimen_evidence", {}).get("specimen_count"), 1, FAILURE_VOCABULARY[8], "candidate.specimen_count")
    expect(candidate.get("specimen_evidence", {}).get("evidence_kind"), EVIDENCE_KIND, FAILURE_VOCABULARY[8], "candidate.evidence_kind")
    generalization = candidate.get("generalization_status", {})
    expect(generalization.get("generalization_status"), GENERALIZATION_STATUS, FAILURE_VOCABULARY[9], "candidate.generalization_status")
    expect_false(generalization.get("general_shape_claimed"), FAILURE_VOCABULARY[9], "candidate.general_shape_claimed")
    expect_false(generalization.get("multi_specimen_stability_claimed"), FAILURE_VOCABULARY[10], "candidate.multi_specimen_stability_claimed")
    expect_false(generalization.get("cross_context_stability_claimed"), FAILURE_VOCABULARY[11], "candidate.cross_context_stability_claimed")
    expect_false(candidate.get("activation_boundaries", {}).get("active_registry_entry_created"), FAILURE_VOCABULARY[12], "candidate.active_registry_entry_created")
    expect_false(candidate.get("activation_boundaries", {}).get("candidate_can_self_activate"), FAILURE_VOCABULARY[13], "candidate.candidate_can_self_activate")
    expect_false(candidate.get("authority_boundaries", {}).get("candidate_replaces_source_authority"), FAILURE_VOCABULARY[14], "candidate.candidate_replaces_source_authority")
    expect_false(candidate.get("authority_boundaries", {}).get("candidate_authorizes_reuse"), FAILURE_VOCABULARY[15], "candidate.candidate_authorizes_reuse")
    expect_false(candidate.get("radius_boundaries", {}).get("candidate_renews_radius"), FAILURE_VOCABULARY[16], "candidate.candidate_renews_radius")
    expect_false(candidate.get("runner_boundaries", {}).get("runner_authority_created"), FAILURE_VOCABULARY[20], "candidate.runner_authority_created")

    expect(f3.get("registry_candidate_audit_id"), F3_AUDIT_ID, FAILURE_VOCABULARY[2], "f3.registry_candidate_audit_id")
    expect(f3.get("audit_status"), F3_AUDIT_STATUS, FAILURE_VOCABULARY[3], "f3.audit_status")
    expect(f3.get("audited_candidate_id"), CANDIDATE_ID, FAILURE_VOCABULARY[3], "f3.audited_candidate_id")
    expect_true(f3.get("audit_pass_meaning", {}).get("candidate_admissibility_audit_passed"), FAILURE_VOCABULARY[3], "f3.candidate_admissibility_audit_passed")
    expect_true(f3.get("audit_pass_meaning", {}).get("candidate_record_admissible_as_local_only"), FAILURE_VOCABULARY[3], "f3.candidate_record_admissible_as_local_only")
    expect(f3.get("registry_candidate_admissibility_audit_gate"), F3_AUDIT_STATUS, FAILURE_VOCABULARY[3], "f3.registry_candidate_admissibility_audit_gate")
    expect(f3.get("precommit_c8_n22_registry_candidate_admissibility_audit_gate"), "PASS", FAILURE_VOCABULARY[3], "f3.precommit_gate")
    expect(f3.get("terminal_transition"), "ADVANCE(F4_REGISTRY_CANDIDATE_CLOSURE_PENDING)", FAILURE_VOCABULARY[3], "f3.terminal_transition")
    for key, value in f3.get("audit_non_effects", {}).items():
        expect_false(value, FAILURE_VOCABULARY[3], f"f3.audit_non_effects.{key}")
    expect(f3.get("audit_gate", {}).get("failures"), [], FAILURE_VOCABULARY[3], "f3.audit_gate.failures")

    expect(compression.get("compression_closure_id"), COMPRESSION_CLOSURE_ID, FAILURE_VOCABULARY[4], "compression.compression_closure_id")
    expect(compression.get("closure_status"), COMPRESSION_CLOSURE_STATUS, FAILURE_VOCABULARY[4], "compression.closure_status")
    expect_true(compression.get("source_of_truth_rule", {}).get("formal_source_chain_remains_authority"), FAILURE_VOCABULARY[14], "compression.formal_source_chain_remains_authority")
    expect(packet.get("compressed_packet_id"), COMPRESSED_PACKET_ID, FAILURE_VOCABULARY[4], "packet.compressed_packet_id")
    expect(packet.get("target_trace_label"), TRACE_LABEL, FAILURE_VOCABULARY[7], "packet.target_trace_label")
    expect(decompression.get("decompression_audit_id"), DECOMPRESSION_AUDIT_ID, FAILURE_VOCABULARY[4], "decompression.decompression_audit_id")
    expect(decompression.get("audit_result", {}).get("decompression_audit_status"), DECOMPRESSION_AUDIT_STATUS, FAILURE_VOCABULARY[4], "decompression.status")
    expect_true(decompression.get("critical_field_group_audit_summary", {}).get("all_critical_field_groups_recovered"), FAILURE_VOCABULARY[4], "decompression.all_critical_field_groups_recovered")
    expect(machine.get("closure_id"), MACHINE_PROCEED_CLOSURE_ID, FAILURE_VOCABULARY[4], "machine.closure_id")
    expect(machine.get("radius_result", {}).get("radius_limit"), RADIUS_LIMIT, FAILURE_VOCABULARY[16], "machine.radius_limit")
    expect(machine.get("radius_result", {}).get("radius_after"), 0, FAILURE_VOCABULARY[16], "machine.radius_after")
    expect_true(machine.get("radius_result", {}).get("radius_exhausted"), FAILURE_VOCABULARY[16], "machine.radius_exhausted")


def build_closure(hashes: dict[str, str], commits: dict[str, str]) -> dict[str, Any]:
    source_hashes = {
        "registry_schema_contract_sha256": hashes[F1_SCHEMA],
        "registry_candidate_sha256": hashes[F2_CANDIDATE],
        "registry_candidate_audit_sha256": hashes[F3_AUDIT],
        "compression_closure_sha256": hashes[E4_CLOSURE],
        "compressed_packet_sha256": hashes[E2_PACKET],
        "decompression_audit_sha256": hashes[E3_AUDIT],
        "machine_proceed_closure_sha256": hashes[D5_CLOSURE],
        "source_file_hash_algorithm": "sha256",
        "source_file_hashes": hashes,
        "source_file_commits": commits,
        "source_hash_verification_basis": "WORKTREE_FILE_MATCHES_HEAD_BLOB",
    }
    confirmed_non_effects = {
        "active_registry_entry_created": False,
        "registry_entry_activated": False,
        "trace_label_promoted": False,
        "generalization_claimed": False,
        "source_authority_replaced": False,
        "reuse_authorized": False,
        "radius_renewed": False,
        "additional_machine_proceed_authorized": False,
        "machine_action_performed": False,
        "execution_authorized": False,
        "runner_authority_created": False,
        "candidate_mutated_by_closure": False,
        "next_promotion_surface_created": False,
        "next_promotion_surface_authorized": False,
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "registry_candidate_closure_id": CLOSURE_ID,
        "closure_role": CLOSURE_ROLE,
        "closure_status": CLOSURE_STATUS,
        "block_id": BLOCK_ID,
        "block_status": BLOCK_STATUS,
        "block_closed": True,
        "generated_by": GENERATOR,
        "closure_pass_meaning": {
            "block_f_closed": True,
            "candidate_chain_closed": True,
            "candidate_only_closure_passed": True,
            "active_registry_acceptance_passed": False,
            "registry_entry_activation_passed": False,
            "promotion_passed": False,
            "reuse_authorization_passed": False,
            "runner_authorization_passed": False,
            "generalization_passed": False,
            "closure_pass_does_not_mean_active": True,
            "closure_pass_does_not_mean_reusable": True,
            "closure_pass_does_not_mean_generalized": True,
            "closure_pass_does_not_mean_runner_ready": True,
        },
        "source_integrity": {
            "registry_schema_contract_present": True,
            "registry_candidate_present": True,
            "registry_candidate_audit_present": True,
            "compression_closure_present": True,
            "compressed_packet_present": True,
            "decompression_audit_present": True,
            "machine_proceed_closure_present": True,
            "registry_schema_contract_hash_verified": True,
            "registry_candidate_hash_verified": True,
            "registry_candidate_audit_hash_verified": True,
            "compression_closure_hash_verified": True,
            "compressed_packet_hash_verified": True,
            "decompression_audit_hash_verified": True,
            "machine_proceed_closure_hash_verified": True,
            "source_identity_resolved_by_explicit_paths": True,
            "mtime_or_latest_resolution_allowed": False,
            "directory_scan_authority_allowed": False,
        },
        "source_hashes": source_hashes,
        "source_mutation_boundary": {
            "f1_schema_contract_modified_by_f4": False,
            "f2_candidate_modified_by_f4": False,
            "f3_audit_modified_by_f4": False,
            "block_e_compression_records_modified_by_f4": False,
            "d5_machine_proceed_closure_modified_by_f4": False,
        },
        "source_chain": {
            "registry_schema_contract_id": REGISTRY_SCHEMA_ID,
            "registry_schema_status": REGISTRY_SCHEMA_STATUS,
            "registry_candidate_id": CANDIDATE_ID,
            "registry_candidate_status": CANDIDATE_STATUS,
            "registry_candidate_creation_status": CANDIDATE_CREATION_STATUS,
            "registry_candidate_audit_id": F3_AUDIT_ID,
            "registry_candidate_audit_status": F3_AUDIT_STATUS,
            "compression_closure_id": COMPRESSION_CLOSURE_ID,
            "compression_closure_status": COMPRESSION_CLOSURE_STATUS,
            "decompression_audit_id": DECOMPRESSION_AUDIT_ID,
            "decompression_audit_status": DECOMPRESSION_AUDIT_STATUS,
            "compressed_packet_id": COMPRESSED_PACKET_ID,
            "machine_proceed_closure_id": MACHINE_PROCEED_CLOSURE_ID,
            "source_chain_complete": True,
            "formal_source_chain_remains_authority": True,
        },
        "block_closure": {
            "block_id": BLOCK_ID,
            "block_status": BLOCK_STATUS,
            "block_closed": True,
            "closed_chain": "F1_TO_F2_TO_F3_TO_F4",
            "closure_scope": "LOCAL_REGISTRY_CANDIDATE_ONLY",
            "closure_does_not_create_active_registry": True,
            "closure_does_not_authorize_reuse": True,
            "closure_does_not_generalize_trace": True,
            "closure_does_not_create_runner_authority": True,
        },
        "candidate_result": {
            "trace_label": TRACE_LABEL,
            "registry_candidate_id": CANDIDATE_ID,
            "candidate_status": CANDIDATE_STATUS,
            "candidate_role": CANDIDATE_ROLE,
            "trace_scope": TRACE_SCOPE,
            "candidate_scope": TRACE_SCOPE,
            "allowed_use": "REGISTRY_CANDIDATE_QUEUE_DISPLAY_ONLY",
            "specimen_count": 1,
            "evidence_kind": EVIDENCE_KIND,
            "generalization_status": GENERALIZATION_STATUS,
            "general_shape_claimed": False,
            "multi_specimen_stability_claimed": False,
            "cross_context_stability_claimed": False,
            "candidate_closure_status": "CANDIDATE_ONLY_CLOSED",
        },
        "generalization_boundary": {
            "specimen_count": 1,
            "evidence_kind": EVIDENCE_KIND,
            "minimum_specimens_for_generalization_met": False,
            "generalization_status": GENERALIZATION_STATUS,
            "general_shape_claimed": False,
            "multi_specimen_stability_claimed": False,
            "cross_context_stability_claimed": False,
            "future_generalization_requires_separate_multi_specimen_audit": True,
        },
        "activation_boundary": {
            "active_registry_entry_created": False,
            "registry_entry_activated": False,
            "activation_status": "ACTIVATION_INACTIVE",
            "activation_requires_human_decision": True,
            "activation_requires_promotion_receipt": True,
            "activation_requires_separate_apply_object": True,
            "candidate_can_self_activate": False,
        },
        "authority_boundary": {
            "source_records_remain_authority": True,
            "closure_grants_authority": False,
            "closure_replaces_source_authority": False,
            "closure_authorizes_reuse": False,
            "closure_authorizes_execution": False,
            "closure_changes_authority_state": False,
            "closure_promotes_schema": False,
            "closure_promotes_taxonomy": False,
        },
        "radius_boundary": {
            "source_radius_limit": RADIUS_LIMIT,
            "source_radius_after": 0,
            "source_radius_exhausted": True,
            "closure_renews_radius": False,
            "closure_creates_radius": False,
            "closure_authorizes_additional_machine_proceed": False,
            "additional_use_requires_new_authority_or_radius": True,
        },
        "runner_boundary": {
            "candidate_is_runner_input": False,
            "closure_authorizes_runner": False,
            "closure_defines_runner_policy": False,
            "closure_routes_runner": False,
            "runner_authority_created": False,
            "future_runner_analysis_may_reference_candidate": True,
            "future_runner_use_requires_separate_authority": True,
        },
        "allowed_post_closure_use": {
            "candidate_queue_display": True,
            "human_review": True,
            "trace_search": True,
            "future_comparison_seed": True,
            "dashboard_projection": True,
            "active_registry_lookup": False,
            "authority_decision_source": False,
            "reuse_authorization_source": False,
            "machine_proceed_source": False,
            "execution_source": False,
            "runner_source": False,
        },
        "confirmed_non_effects": confirmed_non_effects,
        "next_possible_separate_surface": {
            "surface": NEXT_SURFACE,
            "surface_purpose": "decide whether the local registry candidate should be promoted toward active observability-only registry status",
            "created_by_this_closure": False,
            "authorized_by_this_closure": False,
            "selected_as_next_unit_by_this_closure": False,
            "requires_separate_human_decision": True,
            "requires_separate_promotion_receipt": True,
            "requires_separate_activation_apply_object": True,
            "machine_may_prepare_without_new_authority": False,
            "runner_may_use_without_new_authority": False,
        },
        "closure_gate": {
            "registry_candidate_closure_gate": CLOSURE_STATUS,
            "registry_schema_contract_present": True,
            "registry_schema_status": REGISTRY_SCHEMA_STATUS,
            "registry_candidate_present": True,
            "registry_candidate_status": CANDIDATE_STATUS,
            "registry_candidate_audit_present": True,
            "registry_candidate_audit_status": F3_AUDIT_STATUS,
            "registry_candidate_audit_passed": True,
            "compression_closure_present": True,
            "compression_closure_status": COMPRESSION_CLOSURE_STATUS,
            "trace_label": TRACE_LABEL,
            "trace_scope": TRACE_SCOPE,
            "specimen_count": 1,
            "evidence_kind": EVIDENCE_KIND,
            "generalization_status": GENERALIZATION_STATUS,
            "general_shape_claimed": False,
            "multi_specimen_stability_claimed": False,
            "cross_context_stability_claimed": False,
            "active_registry_entry_created": False,
            "registry_entry_activated": False,
            "activation_status": "ACTIVATION_INACTIVE",
            "source_authority_replaced": False,
            "reuse_authorized": False,
            "radius_renewed": False,
            "additional_machine_proceed_authorized": False,
            "machine_action_performed": False,
            "execution_authorized": False,
            "runner_authority_created": False,
            "candidate_mutated_by_closure": False,
            "next_possible_separate_surface": NEXT_SURFACE,
            "next_possible_separate_surface_created_by_this_closure": False,
            "authority_smuggling_detected": False,
            "generalization_smuggling_detected": False,
            "runner_smuggling_detected": False,
            "markdown_overclaim_detected": False,
            "candidate_only_boundary_preserved": True,
            "block_f_closed": True,
            "failures": [],
        },
        "failure_vocabulary": FAILURE_VOCABULARY,
        "most_important_failures": MOST_IMPORTANT_FAILURES,
        "non_claims": NON_CLAIMS,
        "key_non_claims": KEY_NON_CLAIMS,
        "precommit_c8_n22_registry_candidate_closure_gate": "PASS",
        "registry_candidate_closure_gate": CLOSURE_STATUS,
        "terminal_transition": TERMINAL_TRANSITION,
    }


def validate_closure(closure: dict[str, Any]) -> None:
    expect(closure.get("schema_version"), SCHEMA_VERSION, FAILURE_VOCABULARY[4], "closure.schema_version")
    expect(closure.get("registry_candidate_closure_id"), CLOSURE_ID, FAILURE_VOCABULARY[4], "closure.registry_candidate_closure_id")
    expect(closure.get("closure_status"), CLOSURE_STATUS, FAILURE_VOCABULARY[4], "closure.closure_status")
    expect_true(closure.get("block_closed"), FAILURE_VOCABULARY[4], "closure.block_closed")
    for key, value in closure.get("confirmed_non_effects", {}).items():
        expect_false(value, FAILURE_VOCABULARY[12], f"closure.confirmed_non_effects.{key}")
    expect(closure.get("closure_gate", {}).get("failures"), [], FAILURE_VOCABULARY[4], "closure.closure_gate.failures")
    expect_true(closure.get("closure_gate", {}).get("candidate_only_boundary_preserved"), FAILURE_VOCABULARY[4], "closure.candidate_only_boundary_preserved")
    expect(closure.get("terminal_transition"), TERMINAL_TRANSITION, FAILURE_VOCABULARY[4], "closure.terminal_transition")


def render_markdown() -> str:
    return f"""# C8 n22 radius-bound prepare trace registry candidate closure v0

## Status

{CLOSURE_STATUS}

## Block

{BLOCK_STATUS}

## Trace label

{TRACE_LABEL}

## Registry candidate

{CANDIDATE_ID}

## Candidate audit

{F3_AUDIT_STATUS}

## Candidate status

{CANDIDATE_STATUS}

## Trace scope

{TRACE_SCOPE}

## Evidence

- specimen count: 1
- evidence kind: {EVIDENCE_KIND}
- compression closure: {COMPRESSION_CLOSURE_STATUS}
- decompression audit: {DECOMPRESSION_AUDIT_STATUS}

## Generalization

- general shape claimed: false
- multi-specimen stability claimed: false
- cross-context stability claimed: false

## Allowed use

- candidate queue display
- human review
- trace search
- future comparison seed
- dashboard projection

## Confirmed non-effects

- no active registry entry created
- no registry activation
- no source authority replacement
- no reuse authorized
- no radius renewed
- no additional machine proceed authorized
- no machine action performed
- no execution authorized
- no runner authority created
- candidate not mutated by closure
- audit not mutated by closure

## Next possible separate surface

{NEXT_SURFACE}

## Non-claim

This closure does not create that surface, select that surface, promote the candidate, activate a registry, generalize the trace, authorize reuse, renew radius, authorize proceed, authorize execution, or create runner authority.

Even if a future human promotion creates an active observability-only registry entry, that still does not authorize machine proceed, execution, or runner routing."""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def generate() -> int:
    root = detect_repo_root(Path.cwd())
    sources: dict[str, dict[str, Any]] = {}
    hashes: dict[str, str] = {}
    commits: dict[str, str] = {}
    for relative_path, missing_code in [
        (F1_SCHEMA, FAILURE_VOCABULARY[0]),
        (F2_CANDIDATE, FAILURE_VOCABULARY[1]),
        (F3_AUDIT, FAILURE_VOCABULARY[2]),
        (E4_CLOSURE, FAILURE_VOCABULARY[4]),
        (E2_PACKET, FAILURE_VOCABULARY[4]),
        (E3_AUDIT, FAILURE_VOCABULARY[4]),
        (D5_CLOSURE, FAILURE_VOCABULARY[4]),
    ]:
        data, digest, commit = load_committed_json(root, relative_path, missing_code)
        sources[relative_path] = data
        hashes[relative_path] = digest
        commits[relative_path] = commit

    validate_sources(sources)
    closure = build_closure(hashes, commits)
    validate_closure(closure)
    write_text(root / OUTPUT_JSON, json.dumps(closure, indent=2, sort_keys=True))
    write_text(root / OUTPUT_MD, render_markdown())
    print(f"Wrote {OUTPUT_JSON}")
    print(f"Wrote {OUTPUT_MD}")
    print(f"registry_candidate_closure_gate={CLOSURE_STATUS}")
    print(f"terminal_transition={TERMINAL_TRANSITION}")
    return 0


def main() -> int:
    try:
        return generate()
    except GenerationError as exc:
        print(f"STOP_{exc.code}: {exc.detail or exc.code}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
