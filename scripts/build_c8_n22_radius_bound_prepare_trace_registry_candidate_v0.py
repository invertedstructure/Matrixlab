#!/usr/bin/env python3

"""Build C8 n22 radius-bound prepare trace registry candidate v0.

F.2 files one local candidate card under the F.1 registry-entry schema contract.
It does not create or pass F.3, activate a registry entry, authorize reuse,
renew radius, perform machine action, or create runner authority.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_radius_bound_prepare_trace_registry_candidate_v0.py"
OUTPUT_JSON = "docs/matrixlabs/registry/candidates/c8_n22_radius_bound_prepare_trace_registry_candidate_v0.json"
OUTPUT_MD = "docs/matrixlabs/registry/candidates/c8_n22_radius_bound_prepare_trace_registry_candidate_v0.md"

F1_SCHEMA_CONTRACT_JSON = "docs/matrixlabs/registry/compression_trace_registry_entry_schema_contract_v0.json"
E4_COMPRESSION_CLOSURE_JSON = "docs/matrixlabs/compression/c8_n22_compression_specimen_closure_v0.json"
E2_COMPRESSED_PACKET_JSON = "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_compressed_packet_v0.json"
E3_DECOMPRESSION_AUDIT_JSON = "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_decompression_audit_v0.json"
D5_MACHINE_PROCEED_CLOSURE_JSON = "docs/matrixlabs/proceed/c8_n22_machine_proceed_closure_v0.json"

SCHEMA_VERSION = "matrixlabs_compression_trace_registry_candidate_v0"
REGISTRY_CANDIDATE_ID = "candidate.registry.c8_n22_radius_bound_prepare_trace.v0"
CANDIDATE_ROLE = "COMPRESSION_TRACE_REGISTRY_CANDIDATE"
CANDIDATE_STATUS = "REGISTRY_STATUS_CANDIDATE"
CANDIDATE_CREATION_STATUS = "REGISTRY_CANDIDATE_PASS_CREATED_LOCAL_ONLY_PENDING_AUDIT"
ADMISSIBILITY_AUDIT_STATUS = "PENDING_F3_ADMISSIBILITY_AUDIT"
BLOCK_ID = "BLOCK_F"
BLOCK_UNIT_ID = "F2_LOCAL_REGISTRY_CANDIDATE_ENTRY"

REGISTRY_SCHEMA_ID = "compression_trace_registry_entry_schema_contract.v0"
REGISTRY_SCHEMA_VERSION = "matrixlabs_compression_trace_registry_entry_schema_contract_v0"
REGISTRY_SCHEMA_ROLE = "REGISTRY_ENTRY_CONTRACT_ONLY"
REGISTRY_KIND = "COMPRESSION_TRACE_OBSERVABILITY_REGISTRY"
REGISTRY_SCHEMA_SCOPE = "COMPRESSION_STABLE_TRACE_CANDIDATES_ONLY"
REGISTRY_SCHEMA_STATUS = "REGISTRY_SCHEMA_PASS_CONTRACT_DEFINED_ONLY"

COMPRESSION_CLOSURE_ID = "c8.n22.compression_specimen_closure.v0"
COMPRESSION_CLOSURE_STATUS = "COMPRESSION_CLOSURE_PASS_OBSERVABILITY_ONLY"
BLOCK_E_STATUS = "BLOCK_E_PASS_OBSERVABILITY_COMPRESSION_WITH_DECOMPRESSION_PARITY"
ALLOWED_USE_FROM_CLOSURE = "OBSERVABILITY_SHORTCUT_ONLY"

COMPRESSED_PACKET_ID = "c8.n22.radius_bound_prepare_trace.compressed_packet.v0"
PACKET_ROLE = "COMPRESSED_OBSERVABILITY_PACKET"
DECOMPRESSION_AUDIT_ID = "c8.n22.radius_bound_prepare_trace.decompression_audit.v0"
DECOMPRESSION_AUDIT_STATUS = "DECOMPRESSION_AUDIT_PASS_CRITICAL_FIELD_PARITY"
D5_SPECIMEN_ID = "c8.n22.machine_proceed_closure.v0"

TRACE_LABEL = "C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0"
TRACE_SCOPE = "C8_N22_LOCAL_SPECIMEN_ONLY"
GENERALIZATION_STATUS = "LOCAL_SPECIMEN_ONLY_NOT_GENERALIZED"
EVIDENCE_KIND = "SINGLE_LOCAL_SPECIMEN"
RADIUS_LIMIT = "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT"
NEXT_REQUIRED_OBJECT = "c8_n22_radius_bound_prepare_trace_registry_candidate_audit_v0"
NEXT_REQUIRED_UNIT = "F3_REGISTRY_CANDIDATE_ADMISSIBILITY_AUDIT"
PRECOMMIT_GATE = "PASS"
TERMINAL_TRANSITION = "ADVANCE(F3_REGISTRY_CANDIDATE_ADMISSIBILITY_AUDIT_PENDING)"

FAIL_SCHEMA_CONTRACT_MISSING = "REGISTRY_CANDIDATE_FAIL_SCHEMA_CONTRACT_MISSING"
FAIL_SCHEMA_CONTRACT_NOT_PASS = "REGISTRY_CANDIDATE_FAIL_SCHEMA_CONTRACT_NOT_PASS"
FAIL_SCHEMA_CONTRACT_COMPLIANCE_MISSING = "REGISTRY_CANDIDATE_FAIL_SCHEMA_CONTRACT_COMPLIANCE_MISSING"
FAIL_COMPRESSION_CLOSURE_MISSING = "REGISTRY_CANDIDATE_FAIL_COMPRESSION_CLOSURE_MISSING"
FAIL_COMPRESSION_CLOSURE_NOT_PASS = "REGISTRY_CANDIDATE_FAIL_COMPRESSION_CLOSURE_NOT_PASS"
FAIL_COMPRESSED_PACKET_MISSING = "REGISTRY_CANDIDATE_FAIL_COMPRESSED_PACKET_MISSING"
FAIL_DECOMPRESSION_AUDIT_MISSING = "REGISTRY_CANDIDATE_FAIL_DECOMPRESSION_AUDIT_MISSING"
FAIL_DECOMPRESSION_AUDIT_NOT_PASS = "REGISTRY_CANDIDATE_FAIL_DECOMPRESSION_AUDIT_NOT_PASS"
FAIL_SOURCE_HASH_MISMATCH = "REGISTRY_CANDIDATE_FAIL_SOURCE_HASH_MISMATCH"
FAIL_TRACE_LABEL_MISSING = "REGISTRY_CANDIDATE_FAIL_TRACE_LABEL_MISSING"
FAIL_TRACE_SCOPE_MISSING = "REGISTRY_CANDIDATE_FAIL_TRACE_SCOPE_MISSING"
FAIL_SPECIMEN_COUNT_MISSING = "REGISTRY_CANDIDATE_FAIL_SPECIMEN_COUNT_MISSING"
FAIL_SPECIMEN_COUNT_NOT_ONE = "REGISTRY_CANDIDATE_FAIL_SPECIMEN_COUNT_NOT_ONE"
FAIL_LOCAL_ONLY_STATUS_MISSING = "REGISTRY_CANDIDATE_FAIL_LOCAL_ONLY_STATUS_MISSING"
FAIL_ADMISSIBILITY_AUDIT_STATUS_MISSING = "REGISTRY_CANDIDATE_FAIL_ADMISSIBILITY_AUDIT_STATUS_MISSING"
FAIL_GENERALIZATION_CLAIMED = "REGISTRY_CANDIDATE_FAIL_GENERALIZATION_CLAIMED"
FAIL_MULTI_SPECIMEN_STABILITY_CLAIMED = "REGISTRY_CANDIDATE_FAIL_MULTI_SPECIMEN_STABILITY_CLAIMED"
FAIL_CROSS_CONTEXT_STABILITY_CLAIMED = "REGISTRY_CANDIDATE_FAIL_CROSS_CONTEXT_STABILITY_CLAIMED"
FAIL_ACTIVE_REGISTRY_CREATED = "REGISTRY_CANDIDATE_FAIL_ACTIVE_REGISTRY_CREATED"
FAIL_REUSE_AUTHORIZED = "REGISTRY_CANDIDATE_FAIL_REUSE_AUTHORIZED"
FAIL_RADIUS_RENEWED = "REGISTRY_CANDIDATE_FAIL_RADIUS_RENEWED"
FAIL_ADDITIONAL_MACHINE_PROCEED_AUTHORIZED = "REGISTRY_CANDIDATE_FAIL_ADDITIONAL_MACHINE_PROCEED_AUTHORIZED"
FAIL_MACHINE_ACTION_PERFORMED = "REGISTRY_CANDIDATE_FAIL_MACHINE_ACTION_PERFORMED"
FAIL_RUNNER_AUTHORITY_CREATED = "REGISTRY_CANDIDATE_FAIL_RUNNER_AUTHORITY_CREATED"
FAIL_SOURCE_AUTHORITY_REPLACED = "REGISTRY_CANDIDATE_FAIL_SOURCE_AUTHORITY_REPLACED"
FAIL_F3_AUDIT_PRETENDED_PASS = "REGISTRY_CANDIDATE_FAIL_F3_AUDIT_PRETENDED_PASS"
FAIL_GENERALIZED_PATTERN_CREATED = "REGISTRY_CANDIDATE_FAIL_GENERALIZED_PATTERN_CREATED"

FAILURE_VOCABULARY = [
    FAIL_SCHEMA_CONTRACT_MISSING,
    FAIL_SCHEMA_CONTRACT_NOT_PASS,
    FAIL_SCHEMA_CONTRACT_COMPLIANCE_MISSING,
    FAIL_COMPRESSION_CLOSURE_MISSING,
    FAIL_COMPRESSION_CLOSURE_NOT_PASS,
    FAIL_COMPRESSED_PACKET_MISSING,
    FAIL_DECOMPRESSION_AUDIT_MISSING,
    FAIL_DECOMPRESSION_AUDIT_NOT_PASS,
    FAIL_SOURCE_HASH_MISMATCH,
    FAIL_TRACE_LABEL_MISSING,
    FAIL_TRACE_SCOPE_MISSING,
    FAIL_SPECIMEN_COUNT_MISSING,
    FAIL_SPECIMEN_COUNT_NOT_ONE,
    FAIL_LOCAL_ONLY_STATUS_MISSING,
    FAIL_ADMISSIBILITY_AUDIT_STATUS_MISSING,
    FAIL_GENERALIZATION_CLAIMED,
    FAIL_MULTI_SPECIMEN_STABILITY_CLAIMED,
    FAIL_CROSS_CONTEXT_STABILITY_CLAIMED,
    FAIL_ACTIVE_REGISTRY_CREATED,
    FAIL_REUSE_AUTHORIZED,
    FAIL_RADIUS_RENEWED,
    FAIL_ADDITIONAL_MACHINE_PROCEED_AUTHORIZED,
    FAIL_MACHINE_ACTION_PERFORMED,
    FAIL_RUNNER_AUTHORITY_CREATED,
    FAIL_SOURCE_AUTHORITY_REPLACED,
    FAIL_F3_AUDIT_PRETENDED_PASS,
    FAIL_GENERALIZED_PATTERN_CREATED,
]

MOST_IMPORTANT_FAILURES = [
    FAIL_GENERALIZATION_CLAIMED,
    FAIL_ACTIVE_REGISTRY_CREATED,
    FAIL_REUSE_AUTHORIZED,
    FAIL_RUNNER_AUTHORITY_CREATED,
    FAIL_F3_AUDIT_PRETENDED_PASS,
]

REQUIRED_FIELD_GROUPS = [
    "entry_identity",
    "source_compression_closure",
    "source_compressed_packet",
    "source_decompression_audit",
    "trace_label",
    "trace_scope",
    "specimen_evidence",
    "generalization_status",
    "allowed_candidate_use",
    "forbidden_candidate_use",
    "decompression_requirements",
    "authority_boundaries",
    "radius_boundaries",
    "runner_boundaries",
    "activation_boundaries",
    "promotion_boundaries",
    "revocation_or_expiry",
    "audit_requirements",
]

ALLOWED_CANDIDATE_USE = {
    "candidate_queue_display": True,
    "human_review": True,
    "trace_search": True,
    "future_comparison_seed": True,
    "dashboard_projection": True,
    "active_registry_lookup": False,
    "authority_decision_source": False,
    "reuse_authorization_source": False,
    "machine_proceed_source": False,
    "runner_source": False,
}

FORBIDDEN_CANDIDATE_USE = {
    "replace_source_authority": True,
    "authorize_reuse": True,
    "renew_radius": True,
    "authorize_machine_proceed": True,
    "authorize_execution": True,
    "route_runner": True,
    "promote_schema": True,
    "promote_taxonomy": True,
    "claim_generalization": True,
    "claim_multi_specimen_stability": True,
    "claim_cross_context_stability": True,
}

F3_MUST_VERIFY = [
    "schema_contract_present",
    "candidate_present",
    "compression_closure_present",
    "compression_closure_status_pass",
    "decompression_audit_status_pass",
    "required_field_groups_present",
    "specimen_count_declared",
    "specimen_count_equals_one",
    "local_only_status_preserved",
    "no_generalization_claimed",
    "no_multi_specimen_stability_claimed",
    "no_cross_context_stability_claimed",
    "no_active_registry_created",
    "no_reuse_authorized",
    "no_radius_renewed",
    "no_runner_authority_created",
]

NON_CLAIMS = [
    "F.2 does not activate a registry entry.",
    "F.2 does not promote the trace label.",
    "F.2 does not claim generalization.",
    "F.2 does not claim multi-specimen stability.",
    "F.2 does not claim cross-context stability.",
    "F.2 does not replace source authority.",
    "F.2 does not authorize reuse.",
    "F.2 does not renew radius.",
    "F.2 does not authorize another machine proceed.",
    "F.2 does not perform machine action.",
    "F.2 does not execute anything.",
    "F.2 does not create runner authority.",
    "F.2 does not pass F.3 admissibility audit.",
    "F.2 only creates a local registry candidate entry for one audited compressed trace.",
]

KEY_NON_CLAIMS = [
    "registry candidate \u2260 active registry entry",
    "single specimen \u2260 generalized pattern",
    "trace label \u2260 machine authority",
    "candidate queue \u2260 runner input",
    "F.2 created \u2260 F.3 admissibility audited",
    "candidate pass \u2260 reusable trace",
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
        fail(FAIL_SOURCE_HASH_MISMATCH, proc.stderr.strip())
    return proc.stdout.strip()


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def load_committed_json(root: Path, relative_path: str, missing_code: str) -> tuple[dict[str, Any], str, str]:
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
    head_digest = sha256_bytes(proc.stdout)
    if digest != head_digest:
        fail(FAIL_SOURCE_HASH_MISMATCH, f"{relative_path}: working={digest} HEAD={head_digest}")
    commit = run_git(root, ["log", "-n", "1", "--format=%H", "--", relative_path])
    return data, digest, commit


def expect(value: object, wanted: object, failure_code: str, field: str) -> None:
    if value != wanted:
        fail(failure_code, f"{field}: {value!r}!={wanted!r}")


def expect_false(value: object, failure_code: str, field: str) -> None:
    expect(value, False, failure_code, field)


def expect_true(value: object, failure_code: str, field: str) -> None:
    expect(value, True, failure_code, field)


def validate_sources(
    schema: dict[str, Any],
    closure: dict[str, Any],
    packet: dict[str, Any],
    audit: dict[str, Any],
    machine_closure: dict[str, Any],
) -> None:
    expect(schema.get("schema_version"), REGISTRY_SCHEMA_VERSION, FAIL_SCHEMA_CONTRACT_MISSING, "schema.schema_version")
    expect(schema.get("registry_schema_id"), REGISTRY_SCHEMA_ID, FAIL_SCHEMA_CONTRACT_MISSING, "schema.registry_schema_id")
    expect(schema.get("schema_role"), REGISTRY_SCHEMA_ROLE, FAIL_SCHEMA_CONTRACT_NOT_PASS, "schema.schema_role")
    expect(schema.get("registry_kind"), REGISTRY_KIND, FAIL_SCHEMA_CONTRACT_NOT_PASS, "schema.registry_kind")
    expect(schema.get("schema_scope"), REGISTRY_SCHEMA_SCOPE, FAIL_SCHEMA_CONTRACT_NOT_PASS, "schema.schema_scope")
    expect(schema.get("schema_status"), REGISTRY_SCHEMA_STATUS, FAIL_SCHEMA_CONTRACT_NOT_PASS, "schema.schema_status")
    expect(schema.get("required_field_group_count"), 18, FAIL_SCHEMA_CONTRACT_COMPLIANCE_MISSING, "schema.required_field_group_count")
    expect(schema.get("required_field_groups"), REQUIRED_FIELD_GROUPS, FAIL_SCHEMA_CONTRACT_COMPLIANCE_MISSING, "schema.required_field_groups")

    expect(closure.get("compression_closure_id"), COMPRESSION_CLOSURE_ID, FAIL_COMPRESSION_CLOSURE_MISSING, "closure.compression_closure_id")
    expect(closure.get("closure_status"), COMPRESSION_CLOSURE_STATUS, FAIL_COMPRESSION_CLOSURE_NOT_PASS, "closure.closure_status")
    expect(closure.get("block", {}).get("block_status"), BLOCK_E_STATUS, FAIL_COMPRESSION_CLOSURE_NOT_PASS, "closure.block.block_status")
    expect(closure.get("allowed_use", {}).get("allowed_use_class"), ALLOWED_USE_FROM_CLOSURE, FAIL_COMPRESSION_CLOSURE_NOT_PASS, "closure.allowed_use.allowed_use_class")
    expect_true(closure.get("source_of_truth_rule", {}).get("formal_source_chain_remains_authority"), FAIL_SOURCE_AUTHORITY_REPLACED, "closure.source_of_truth_rule.formal_source_chain_remains_authority")
    expect_false(closure.get("closure_gate", {}).get("registry_candidate_surface_created_by_closure"), FAIL_ACTIVE_REGISTRY_CREATED, "closure.closure_gate.registry_candidate_surface_created_by_closure")
    expect_false(closure.get("closure_gate", {}).get("registry_entry_created_by_closure"), FAIL_ACTIVE_REGISTRY_CREATED, "closure.closure_gate.registry_entry_created_by_closure")
    expect_false(closure.get("closure_gate", {}).get("active_registry_created_by_closure"), FAIL_ACTIVE_REGISTRY_CREATED, "closure.closure_gate.active_registry_created_by_closure")
    expect_false(closure.get("closure_gate", {}).get("runner_authority_created_by_closure"), FAIL_RUNNER_AUTHORITY_CREATED, "closure.closure_gate.runner_authority_created_by_closure")

    expect(packet.get("compressed_packet_id"), COMPRESSED_PACKET_ID, FAIL_COMPRESSED_PACKET_MISSING, "packet.compressed_packet_id")
    expect(packet.get("target_trace_label"), TRACE_LABEL, FAIL_TRACE_LABEL_MISSING, "packet.target_trace_label")
    expect(packet.get("packet_role"), PACKET_ROLE, FAIL_COMPRESSED_PACKET_MISSING, "packet.packet_role")

    expect(audit.get("decompression_audit_id"), DECOMPRESSION_AUDIT_ID, FAIL_DECOMPRESSION_AUDIT_MISSING, "audit.decompression_audit_id")
    expect(audit.get("audit_result", {}).get("decompression_audit_status"), DECOMPRESSION_AUDIT_STATUS, FAIL_DECOMPRESSION_AUDIT_NOT_PASS, "audit.audit_result.decompression_audit_status")
    expect(audit.get("critical_field_group_audit_summary", {}).get("critical_field_group_count_checked"), 15, FAIL_DECOMPRESSION_AUDIT_NOT_PASS, "audit.critical_field_group_count_checked")
    expect(audit.get("critical_field_group_audit_summary", {}).get("critical_field_group_count_passed"), 15, FAIL_DECOMPRESSION_AUDIT_NOT_PASS, "audit.critical_field_group_count_passed")
    expect_true(audit.get("critical_field_group_audit_summary", {}).get("all_critical_field_groups_recovered"), FAIL_DECOMPRESSION_AUDIT_NOT_PASS, "audit.all_critical_field_groups_recovered")
    expect_false(audit.get("audit_scope_boundary", {}).get("full_trace_equivalence_claimed"), FAIL_GENERALIZATION_CLAIMED, "audit.audit_scope_boundary.full_trace_equivalence_claimed")
    expect_false(audit.get("audit_scope_boundary", {}).get("all_possible_fields_audited"), FAIL_GENERALIZATION_CLAIMED, "audit.audit_scope_boundary.all_possible_fields_audited")

    expect(machine_closure.get("closure_id"), D5_SPECIMEN_ID, FAIL_SPECIMEN_COUNT_MISSING, "machine_closure.closure_id")
    expect(machine_closure.get("radius_result", {}).get("radius_limit"), RADIUS_LIMIT, FAIL_RADIUS_RENEWED, "machine_closure.radius_result.radius_limit")
    expect(machine_closure.get("radius_result", {}).get("radius_after"), 0, FAIL_RADIUS_RENEWED, "machine_closure.radius_result.radius_after")
    expect_true(machine_closure.get("radius_result", {}).get("radius_exhausted"), FAIL_RADIUS_RENEWED, "machine_closure.radius_result.radius_exhausted")


def source_hash_record(hashes: dict[str, str], commits: dict[str, str]) -> dict[str, Any]:
    return {
        "source_file_hash_algorithm": "sha256",
        "source_file_hashes": hashes,
        "source_file_commits": commits,
        "source_hash_verification_basis": "WORKTREE_FILE_MATCHES_HEAD_BLOB",
    }


def build_candidate(hashes: dict[str, str], commits: dict[str, str]) -> dict[str, Any]:
    candidate_gate = {
        "registry_candidate_gate": CANDIDATE_CREATION_STATUS,
        "registry_schema_contract_present": True,
        "registry_schema_id": REGISTRY_SCHEMA_ID,
        "compression_closure_present": True,
        "compression_closure_status": COMPRESSION_CLOSURE_STATUS,
        "compression_closure_passed": True,
        "compressed_packet_present": True,
        "decompression_audit_present": True,
        "decompression_audit_status": DECOMPRESSION_AUDIT_STATUS,
        "decompression_audit_passed": True,
        "trace_label": TRACE_LABEL,
        "trace_scope": TRACE_SCOPE,
        "candidate_status": CANDIDATE_STATUS,
        "admissibility_audit_status": ADMISSIBILITY_AUDIT_STATUS,
        "specimen_count": 1,
        "specimen_count_declared": True,
        "evidence_kind": EVIDENCE_KIND,
        "local_only_status_declared": True,
        "generalization_status": GENERALIZATION_STATUS,
        "general_shape_claimed": False,
        "multi_specimen_stability_claimed": False,
        "cross_context_stability_claimed": False,
        "generalization_overclaim_detected": False,
        "authority_smuggling_detected": False,
        "runner_authority_smuggling_detected": False,
        "active_registry_entry_created": False,
        "registry_entry_activated": False,
        "source_authority_replaced": False,
        "reuse_authorized": False,
        "radius_renewed": False,
        "additional_machine_proceed_authorized": False,
        "machine_action_performed": False,
        "runner_authority_created": False,
        "generalized_pattern_created": False,
        "admissibility_audit_passed": False,
        "next_required_object": NEXT_REQUIRED_OBJECT,
        "failures": [],
    }
    candidate_non_effects = {
        "active_registry_entry_created": False,
        "registry_entry_activated": False,
        "source_authority_replaced": False,
        "reuse_authorized": False,
        "radius_renewed": False,
        "additional_machine_proceed_authorized": False,
        "machine_action_performed": False,
        "runner_authority_created": False,
        "generalized_pattern_created": False,
        "f3_audit_created": False,
        "f3_audit_passed": False,
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "registry_candidate_id": REGISTRY_CANDIDATE_ID,
        "candidate_role": CANDIDATE_ROLE,
        "candidate_status": CANDIDATE_STATUS,
        "candidate_creation_status": CANDIDATE_CREATION_STATUS,
        "admissibility_audit_status": ADMISSIBILITY_AUDIT_STATUS,
        "block_id": BLOCK_ID,
        "block_unit_id": BLOCK_UNIT_ID,
        "generated_by": GENERATOR,
        "candidate_pass_meaning": {
            "creation_gate_passed": True,
            "admissibility_audit_passed": False,
            "active_registry_acceptance_passed": False,
            "pass_does_not_mean_reusable": True,
        },
        "source_integrity": {
            "registry_schema_contract_present": True,
            "compression_closure_present": True,
            "compressed_packet_present": True,
            "decompression_audit_present": True,
            "registry_schema_contract_hash_verified": True,
            "compression_closure_hash_verified": True,
            "compressed_packet_hash_verified": True,
            "decompression_audit_hash_verified": True,
            "source_identity_resolved_by_explicit_paths": True,
            "mtime_or_latest_resolution_allowed": False,
            "directory_scan_authority_allowed": False,
        },
        "source_hashes": source_hash_record(hashes, commits),
        "source_registry_schema_contract": {
            "registry_schema_id": REGISTRY_SCHEMA_ID,
            "schema_version": REGISTRY_SCHEMA_VERSION,
            "schema_role": REGISTRY_SCHEMA_ROLE,
            "registry_kind": REGISTRY_KIND,
            "schema_scope": REGISTRY_SCHEMA_SCOPE,
            "schema_status": REGISTRY_SCHEMA_STATUS,
            "required_field_group_count": 18,
        },
        "schema_contract_compliance": {
            "source_registry_schema_id": REGISTRY_SCHEMA_ID,
            "required_field_group_count_from_contract": 18,
            "candidate_field_group_count_present": 18,
            "candidate_declares_all_required_groups": True,
            "candidate_stage_allowed_use_matches_contract": True,
            "candidate_stage_forbidden_use_matches_contract": True,
            "authority_boundaries_match_contract": True,
            "radius_boundaries_match_contract": True,
            "runner_boundaries_match_contract": True,
            "activation_boundaries_match_contract": True,
            "promotion_boundaries_match_contract": True,
            "audit_requirements_match_contract": True,
        },
        "candidate_field_groups_present": REQUIRED_FIELD_GROUPS,
        "source_compression_closure": {
            "compression_closure_id": COMPRESSION_CLOSURE_ID,
            "compression_closure_status": COMPRESSION_CLOSURE_STATUS,
            "block_status": BLOCK_E_STATUS,
            "allowed_use_from_closure": ALLOWED_USE_FROM_CLOSURE,
            "formal_source_chain_remains_authority": True,
            "registry_candidate_surface_created_by_closure": False,
            "registry_entry_created_by_closure": False,
            "active_registry_created_by_closure": False,
            "runner_authority_created_by_closure": False,
        },
        "source_compressed_packet": {
            "compressed_packet_id": COMPRESSED_PACKET_ID,
            "trace_label": TRACE_LABEL,
            "packet_role": PACKET_ROLE,
            "source_records_remain_authority": True,
        },
        "source_decompression_audit": {
            "decompression_audit_id": DECOMPRESSION_AUDIT_ID,
            "decompression_audit_status": DECOMPRESSION_AUDIT_STATUS,
            "critical_field_group_count_checked": 15,
            "critical_field_group_count_passed": 15,
            "all_critical_field_groups_recovered": True,
            "full_trace_equivalence_claimed": False,
            "all_possible_fields_audited": False,
        },
        "candidate_registration_boundary": {
            "candidate_card_created": True,
            "trace_registered_as_active_entry": False,
            "trace_registered_as_reusable_pattern": False,
            "candidate_queue_entry_only": True,
        },
        "trace_identity": {
            "trace_label": TRACE_LABEL,
            "trace_label_definition": "completed local C8 n22 radius-bound prepare trace",
            "trace_scope": TRACE_SCOPE,
            "trace_label_authority_effect": "NONE",
            "trace_label_reuse_effect": "NONE",
            "trace_label_runner_effect": "NONE",
        },
        "specimen_evidence": {
            "specimen_count": 1,
            "minimum_specimens_for_generalization_met": False,
            "multi_specimen_stability_claimed": False,
            "cross_context_stability_claimed": False,
            "evidence_kind": EVIDENCE_KIND,
            "specimen_ids": [D5_SPECIMEN_ID],
            "source_trace_ids": [TRACE_LABEL],
            "decompression_parity_passed": True,
            "critical_fields_preserved_by_e3_audit": True,
        },
        "stability_boundary": {
            "single_specimen_is_stability_evidence": False,
            "single_specimen_is_generalization_evidence": False,
            "single_specimen_is_runner_admissibility_evidence": False,
            "multi_specimen_stability_requires_future_candidates_and_audit": True,
        },
        "generalization_status": {
            "generalization_status": GENERALIZATION_STATUS,
            "local_candidate_only": True,
            "single_specimen_only": True,
            "general_shape_claimed": False,
            "multi_specimen_stability_claimed": False,
            "cross_context_stability_claimed": False,
        },
        "allowed_candidate_use": ALLOWED_CANDIDATE_USE,
        "forbidden_candidate_use": FORBIDDEN_CANDIDATE_USE,
        "decompression_requirements": {
            "decompression_audit_required": True,
            "source_decompression_audit_id": DECOMPRESSION_AUDIT_ID,
            "critical_field_parity_required": True,
            "source_records_remain_authority": True,
            "candidate_may_stand_alone_without_source": False,
        },
        "authority_boundaries": {
            "candidate_grants_authority": False,
            "candidate_replaces_source_authority": False,
            "candidate_authorizes_reuse": False,
            "candidate_authorizes_execution": False,
            "candidate_changes_authority_state": False,
            "source_records_remain_authority": True,
        },
        "radius_boundaries": {
            "source_radius_limit": RADIUS_LIMIT,
            "source_radius_after": 0,
            "source_radius_exhausted": True,
            "candidate_renews_radius": False,
            "candidate_creates_radius": False,
            "candidate_authorizes_additional_machine_proceed": False,
            "additional_use_requires_new_authority_or_radius": True,
        },
        "runner_boundaries": {
            "candidate_is_runner_input": False,
            "candidate_authorizes_runner": False,
            "candidate_defines_runner_policy": False,
            "candidate_routes_runner": False,
            "runner_authority_created": False,
            "future_runner_analysis_may_reference_candidate_after_admissibility_or_separate_surface": True,
            "reference_does_not_create_runner_authority": True,
        },
        "activation_boundaries": {
            "active_registry_entry_created": False,
            "activation_status": "ACTIVATION_INACTIVE",
            "activation_requires_human_decision": True,
            "activation_requires_separate_apply_object": True,
            "candidate_can_self_activate": False,
        },
        "promotion_boundaries": {
            "promotion_status": "REGISTRY_PROMOTION_NOT_REQUESTED",
            "promotion_decision_required": True,
            "promotion_receipt_required": True,
            "promotion_apply_required": True,
            "promotion_granted_by_candidate": False,
        },
        "revocation_or_expiry": {
            "revocation_status": "NOT_REVOKED",
            "expiry_status": "NOT_EXPIRED",
            "supersession_status": "NOT_SUPERSEDED",
            "invalidated_by_source_mismatch": False,
            "revocation_requires_record": True,
        },
        "audit_requirements": {
            "requires_registry_candidate_admissibility_audit": True,
            "next_required_object": NEXT_REQUIRED_OBJECT,
            "f3_must_verify": F3_MUST_VERIFY,
        },
        "f3_handoff": {
            "next_required_object": NEXT_REQUIRED_OBJECT,
            "next_required_unit": NEXT_REQUIRED_UNIT,
            "f3_audit_created_by_f2": False,
            "f3_audit_passed_by_f2": False,
            "f2_terminal_transition": TERMINAL_TRANSITION,
        },
        "candidate_non_effects": candidate_non_effects,
        "candidate_gate": candidate_gate,
        "failure_vocabulary": FAILURE_VOCABULARY,
        "most_important_failures": MOST_IMPORTANT_FAILURES,
        "non_claims": NON_CLAIMS,
        "key_non_claims": KEY_NON_CLAIMS,
        "precommit_c8_n22_registry_candidate_gate": PRECOMMIT_GATE,
        "registry_candidate_gate": CANDIDATE_CREATION_STATUS,
        "terminal_transition": TERMINAL_TRANSITION,
    }


def validate_candidate(candidate: dict[str, Any]) -> None:
    expect(candidate.get("schema_version"), SCHEMA_VERSION, FAIL_SCHEMA_CONTRACT_COMPLIANCE_MISSING, "schema_version")
    expect(candidate.get("registry_candidate_id"), REGISTRY_CANDIDATE_ID, FAIL_SCHEMA_CONTRACT_COMPLIANCE_MISSING, "registry_candidate_id")
    expect(candidate.get("candidate_status"), CANDIDATE_STATUS, FAIL_SCHEMA_CONTRACT_COMPLIANCE_MISSING, "candidate_status")
    expect(candidate.get("admissibility_audit_status"), ADMISSIBILITY_AUDIT_STATUS, FAIL_ADMISSIBILITY_AUDIT_STATUS_MISSING, "admissibility_audit_status")
    expect(candidate.get("schema_contract_compliance", {}).get("candidate_field_group_count_present"), 18, FAIL_SCHEMA_CONTRACT_COMPLIANCE_MISSING, "candidate_field_group_count_present")
    expect(candidate.get("specimen_evidence", {}).get("specimen_count"), 1, FAIL_SPECIMEN_COUNT_NOT_ONE, "specimen_count")
    expect(candidate.get("trace_identity", {}).get("trace_scope"), TRACE_SCOPE, FAIL_TRACE_SCOPE_MISSING, "trace_scope")
    expect(candidate.get("generalization_status", {}).get("generalization_status"), GENERALIZATION_STATUS, FAIL_LOCAL_ONLY_STATUS_MISSING, "generalization_status")
    for key, value in candidate.get("candidate_non_effects", {}).items():
        expect(value, False, FAIL_ACTIVE_REGISTRY_CREATED, f"candidate_non_effects.{key}")
    expect(candidate.get("candidate_gate", {}).get("failures"), [], FAIL_SCHEMA_CONTRACT_COMPLIANCE_MISSING, "candidate_gate.failures")
    expect(candidate.get("terminal_transition"), TERMINAL_TRANSITION, FAIL_F3_AUDIT_PRETENDED_PASS, "terminal_transition")


def render_markdown() -> str:
    return f"""# C8 n22 radius-bound prepare trace registry candidate v0

## Status

{CANDIDATE_CREATION_STATUS}

## Registry schema contract

{REGISTRY_SCHEMA_ID}

## Trace label

{TRACE_LABEL}

## Candidate status

{CANDIDATE_STATUS}

## Admissibility audit status

{ADMISSIBILITY_AUDIT_STATUS}

## Trace scope

{TRACE_SCOPE}

## Evidence

- specimen count: 1
- evidence kind: {EVIDENCE_KIND}
- decompression audit: {DECOMPRESSION_AUDIT_STATUS}
- compression closure: {COMPRESSION_CLOSURE_STATUS}

## Generalization

- general shape claimed: false
- multi-specimen stability claimed: false
- cross-context stability claimed: false
- local candidate only: true

## Allowed candidate use

- candidate queue display
- human review
- trace search
- future comparison seed
- dashboard projection

## Confirmed non-effects

- no active registry entry created
- no reuse authorized
- no radius renewed
- no additional machine proceed authorized
- no machine action performed
- no runner authority created
- source records remain authority
- no generalized pattern created
- F.3 admissibility audit not passed by F.2

## Next

Registry candidate admissibility audit is required."""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def generate() -> int:
    root = detect_repo_root(Path.cwd())
    sources: dict[str, dict[str, Any]] = {}
    hashes: dict[str, str] = {}
    commits: dict[str, str] = {}
    for rel, missing_code in [
        (F1_SCHEMA_CONTRACT_JSON, FAIL_SCHEMA_CONTRACT_MISSING),
        (E4_COMPRESSION_CLOSURE_JSON, FAIL_COMPRESSION_CLOSURE_MISSING),
        (E2_COMPRESSED_PACKET_JSON, FAIL_COMPRESSED_PACKET_MISSING),
        (E3_DECOMPRESSION_AUDIT_JSON, FAIL_DECOMPRESSION_AUDIT_MISSING),
        (D5_MACHINE_PROCEED_CLOSURE_JSON, FAIL_SPECIMEN_COUNT_MISSING),
    ]:
        data, digest, commit = load_committed_json(root, rel, missing_code)
        sources[rel] = data
        hashes[rel] = digest
        commits[rel] = commit

    validate_sources(
        sources[F1_SCHEMA_CONTRACT_JSON],
        sources[E4_COMPRESSION_CLOSURE_JSON],
        sources[E2_COMPRESSED_PACKET_JSON],
        sources[E3_DECOMPRESSION_AUDIT_JSON],
        sources[D5_MACHINE_PROCEED_CLOSURE_JSON],
    )
    candidate = build_candidate(hashes, commits)
    validate_candidate(candidate)

    write_text(root / OUTPUT_JSON, json.dumps(candidate, indent=2, sort_keys=True))
    write_text(root / OUTPUT_MD, render_markdown())

    print(f"Wrote {OUTPUT_JSON}")
    print(f"Wrote {OUTPUT_MD}")
    print(f"registry_candidate_gate={CANDIDATE_CREATION_STATUS}")
    print(f"terminal_transition={TERMINAL_TRANSITION}")
    return 0


def main() -> int:
    try:
        return generate()
    except GenerationError as exc:
        print(f"STOP_REGISTRY_CANDIDATE_FAIL_{exc.code}: {exc.detail or exc.code}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
