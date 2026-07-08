#!/usr/bin/env python3

"""Build the C8 n22 local registry-candidate admissibility audit v0.

F.3 audits the committed F.2 candidate against the committed F.1 contract.
It creates no active registry entry, reuse authority, radius, machine action,
generalized pattern, runner authority, F.4 closure, or Block F closure.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_radius_bound_prepare_trace_registry_candidate_audit_v0.py"
OUTPUT_JSON = "docs/matrixlabs/registry/audits/c8_n22_radius_bound_prepare_trace_registry_candidate_audit_v0.json"
OUTPUT_MD = "docs/matrixlabs/registry/audits/c8_n22_radius_bound_prepare_trace_registry_candidate_audit_v0.md"

F1_SCHEMA = "docs/matrixlabs/registry/compression_trace_registry_entry_schema_contract_v0.json"
F2_CANDIDATE = "docs/matrixlabs/registry/candidates/c8_n22_radius_bound_prepare_trace_registry_candidate_v0.json"
E4_CLOSURE = "docs/matrixlabs/compression/c8_n22_compression_specimen_closure_v0.json"
E2_PACKET = "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_compressed_packet_v0.json"
E3_AUDIT = "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_decompression_audit_v0.json"
D5_CLOSURE = "docs/matrixlabs/proceed/c8_n22_machine_proceed_closure_v0.json"

SCHEMA_VERSION = "matrixlabs_compression_trace_registry_candidate_admissibility_audit_v0"
AUDIT_ID = "audit.registry.c8_n22_radius_bound_prepare_trace.candidate_admissibility.v0"
AUDIT_ROLE = "REGISTRY_CANDIDATE_ADMISSIBILITY_AUDIT"
AUDIT_STATUS = "REGISTRY_CANDIDATE_ADMISSIBILITY_AUDIT_PASS_LOCAL_ONLY"
CANDIDATE_ID = "candidate.registry.c8_n22_radius_bound_prepare_trace.v0"
CANDIDATE_SCHEMA_VERSION = "matrixlabs_compression_trace_registry_candidate_v0"
CANDIDATE_ROLE = "COMPRESSION_TRACE_REGISTRY_CANDIDATE"
CANDIDATE_STATUS = "REGISTRY_STATUS_CANDIDATE"
CANDIDATE_CREATION_STATUS = "REGISTRY_CANDIDATE_PASS_CREATED_LOCAL_ONLY_PENDING_AUDIT"
PENDING_F3 = "PENDING_F3_ADMISSIBILITY_AUDIT"
BLOCK_ID = "BLOCK_F"
BLOCK_UNIT_ID = "F3_REGISTRY_CANDIDATE_ADMISSIBILITY_AUDIT"

REGISTRY_SCHEMA_ID = "compression_trace_registry_entry_schema_contract.v0"
REGISTRY_SCHEMA_VERSION = "matrixlabs_compression_trace_registry_entry_schema_contract_v0"
REGISTRY_SCHEMA_ROLE = "REGISTRY_ENTRY_CONTRACT_ONLY"
REGISTRY_KIND = "COMPRESSION_TRACE_OBSERVABILITY_REGISTRY"
REGISTRY_SCHEMA_SCOPE = "COMPRESSION_STABLE_TRACE_CANDIDATES_ONLY"
REGISTRY_SCHEMA_STATUS = "REGISTRY_SCHEMA_PASS_CONTRACT_DEFINED_ONLY"

COMPRESSION_CLOSURE_ID = "c8.n22.compression_specimen_closure.v0"
COMPRESSION_CLOSURE_STATUS = "COMPRESSION_CLOSURE_PASS_OBSERVABILITY_ONLY"
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
NEXT_OBJECT = "c8_n22_radius_bound_prepare_trace_registry_candidate_closure_v0"
NEXT_UNIT = "F4_REGISTRY_CANDIDATE_CLOSURE"
TERMINAL_TRANSITION = "ADVANCE(F4_REGISTRY_CANDIDATE_CLOSURE_PENDING)"

FAILURE_VOCABULARY = [
    "REGISTRY_CANDIDATE_AUDIT_FAIL_SCHEMA_CONTRACT_MISSING",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_SCHEMA_CONTRACT_NOT_PASS",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_CANDIDATE_MISSING",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_CANDIDATE_NOT_PENDING_F3",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_COMPRESSION_CLOSURE_MISSING",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_COMPRESSION_CLOSURE_NOT_PASS",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_COMPRESSED_PACKET_MISSING",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_DECOMPRESSION_AUDIT_MISSING",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_DECOMPRESSION_AUDIT_NOT_PASS",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_SOURCE_HASH_MISMATCH",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_SOURCE_IDENTITY_AMBIGUOUS",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_REQUIRED_FIELD_GROUPS_MISSING",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_SPECIMEN_COUNT_MISSING",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_SPECIMEN_COUNT_NOT_ONE",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_LOCAL_ONLY_STATUS_MISSING",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_GENERALIZATION_CLAIMED",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_MULTI_SPECIMEN_STABILITY_CLAIMED",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_CROSS_CONTEXT_STABILITY_CLAIMED",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_ACTIVE_REGISTRY_CREATED",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_REGISTRY_ENTRY_ACTIVATED",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_REUSE_AUTHORIZED",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_RADIUS_RENEWED",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_ADDITIONAL_MACHINE_PROCEED_AUTHORIZED",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_MACHINE_ACTION_PERFORMED",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_RUNNER_AUTHORITY_CREATED",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_SOURCE_AUTHORITY_REPLACED",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_GENERALIZED_PATTERN_CREATED",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_SOURCE_CANDIDATE_MODIFIED",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_F4_CLOSURE_CREATED",
    "REGISTRY_CANDIDATE_AUDIT_FAIL_BLOCK_F_CLOSED",
]

REQUIRED_GROUPS = [
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

GROUP_AUDIT_KEYS = [
    "entry_identity_passed",
    "source_compression_closure_passed",
    "source_compressed_packet_passed",
    "source_decompression_audit_passed",
    "trace_label_passed",
    "trace_scope_passed",
    "specimen_evidence_passed",
    "generalization_status_passed",
    "allowed_candidate_use_passed",
    "forbidden_candidate_use_passed",
    "decompression_requirements_passed",
    "authority_boundaries_passed",
    "radius_boundaries_passed",
    "runner_boundaries_passed",
    "activation_boundaries_passed",
    "promotion_boundaries_passed",
    "revocation_or_expiry_passed",
    "audit_requirements_passed",
]

ALLOWED_USE = {
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

FORBIDDEN_USE = {
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

NON_CLAIMS = [
    "F.3 does not activate a registry entry.",
    "F.3 does not promote the trace label.",
    "F.3 does not claim generalization.",
    "F.3 does not claim multi-specimen stability.",
    "F.3 does not claim cross-context stability.",
    "F.3 does not replace source authority.",
    "F.3 does not authorize reuse.",
    "F.3 does not renew radius.",
    "F.3 does not authorize another machine proceed.",
    "F.3 does not perform machine action.",
    "F.3 does not execute anything.",
    "F.3 does not create runner authority.",
    "F.3 does not modify the F.2 candidate record.",
    "F.3 does not create F.4 closure.",
    "F.3 does not close Block F.",
    "F.3 only audits the local registry candidate entry for admissibility under the F.1 contract.",
]

KEY_NON_CLAIMS = [
    "admissibility audit \u2260 active registry entry",
    "audit pass \u2260 reuse authorization",
    "audit pass \u2260 generalized pattern",
    "audit pass \u2260 runner authority",
    "audit object \u2260 source candidate mutation",
    "F.3 pass \u2260 F.4 closure",
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
        fail("REGISTRY_CANDIDATE_AUDIT_FAIL_SOURCE_IDENTITY_AMBIGUOUS", proc.stderr.strip())
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
        fail("REGISTRY_CANDIDATE_AUDIT_FAIL_SOURCE_HASH_MISMATCH", proc.stderr.strip())
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
        fail("REGISTRY_CANDIDATE_AUDIT_FAIL_SOURCE_HASH_MISMATCH", f"{relative_path}: absent from HEAD")
    digest = sha256_bytes(content)
    head_digest = sha256_bytes(proc.stdout)
    if digest != head_digest:
        code = (
            "REGISTRY_CANDIDATE_AUDIT_FAIL_SOURCE_CANDIDATE_MODIFIED"
            if relative_path == F2_CANDIDATE
            else "REGISTRY_CANDIDATE_AUDIT_FAIL_SOURCE_HASH_MISMATCH"
        )
        fail(code, f"{relative_path}: working={digest} HEAD={head_digest}")
    commit = run_git(root, ["log", "-n", "1", "--format=%H", "--", relative_path])
    return data, digest, commit


def expect(value: object, wanted: object, code: str, field: str) -> None:
    if value != wanted:
        fail(code, f"{field}: {value!r}!={wanted!r}")


def expect_false(value: object, code: str, field: str) -> None:
    expect(value, False, code, field)


def expect_true(value: object, code: str, field: str) -> None:
    expect(value, True, code, field)


def validate_sources(sources: dict[str, dict[str, Any]]) -> None:
    schema = sources[F1_SCHEMA]
    candidate = sources[F2_CANDIDATE]
    closure = sources[E4_CLOSURE]
    packet = sources[E2_PACKET]
    audit = sources[E3_AUDIT]
    machine = sources[D5_CLOSURE]

    expect(schema.get("registry_schema_id"), REGISTRY_SCHEMA_ID, FAILURE_VOCABULARY[0], "schema.registry_schema_id")
    expect(schema.get("schema_version"), REGISTRY_SCHEMA_VERSION, FAILURE_VOCABULARY[0], "schema.schema_version")
    expect(schema.get("schema_role"), REGISTRY_SCHEMA_ROLE, FAILURE_VOCABULARY[1], "schema.schema_role")
    expect(schema.get("registry_kind"), REGISTRY_KIND, FAILURE_VOCABULARY[1], "schema.registry_kind")
    expect(schema.get("schema_scope"), REGISTRY_SCHEMA_SCOPE, FAILURE_VOCABULARY[1], "schema.schema_scope")
    expect(schema.get("schema_status"), REGISTRY_SCHEMA_STATUS, FAILURE_VOCABULARY[1], "schema.schema_status")
    expect(schema.get("required_field_group_count"), 18, FAILURE_VOCABULARY[11], "schema.required_field_group_count")
    expect(schema.get("required_field_groups"), REQUIRED_GROUPS, FAILURE_VOCABULARY[11], "schema.required_field_groups")

    expect(candidate.get("schema_version"), CANDIDATE_SCHEMA_VERSION, FAILURE_VOCABULARY[2], "candidate.schema_version")
    expect(candidate.get("registry_candidate_id"), CANDIDATE_ID, FAILURE_VOCABULARY[2], "candidate.registry_candidate_id")
    expect(candidate.get("candidate_role"), CANDIDATE_ROLE, FAILURE_VOCABULARY[2], "candidate.candidate_role")
    expect(candidate.get("candidate_status"), CANDIDATE_STATUS, FAILURE_VOCABULARY[3], "candidate.candidate_status")
    expect(candidate.get("candidate_creation_status"), CANDIDATE_CREATION_STATUS, FAILURE_VOCABULARY[3], "candidate.candidate_creation_status")
    expect(candidate.get("admissibility_audit_status"), PENDING_F3, FAILURE_VOCABULARY[3], "candidate.admissibility_audit_status")
    expect(candidate.get("candidate_field_groups_present"), REQUIRED_GROUPS, FAILURE_VOCABULARY[11], "candidate.candidate_field_groups_present")
    expect(candidate.get("schema_contract_compliance", {}).get("candidate_field_group_count_present"), 18, FAILURE_VOCABULARY[11], "candidate.candidate_field_group_count_present")
    expect_true(candidate.get("schema_contract_compliance", {}).get("candidate_declares_all_required_groups"), FAILURE_VOCABULARY[11], "candidate.candidate_declares_all_required_groups")

    registration = candidate.get("candidate_registration_boundary", {})
    expect_true(registration.get("candidate_card_created"), FAILURE_VOCABULARY[2], "candidate.candidate_card_created")
    expect_true(registration.get("candidate_queue_entry_only"), FAILURE_VOCABULARY[14], "candidate.candidate_queue_entry_only")
    expect_false(registration.get("trace_registered_as_active_entry"), FAILURE_VOCABULARY[18], "candidate.trace_registered_as_active_entry")
    expect_false(registration.get("trace_registered_as_reusable_pattern"), FAILURE_VOCABULARY[20], "candidate.trace_registered_as_reusable_pattern")

    expect(candidate.get("trace_identity", {}).get("trace_label"), TRACE_LABEL, FAILURE_VOCABULARY[14], "candidate.trace_label")
    expect(candidate.get("trace_identity", {}).get("trace_scope"), TRACE_SCOPE, FAILURE_VOCABULARY[14], "candidate.trace_scope")
    specimen = candidate.get("specimen_evidence", {})
    expect(specimen.get("specimen_count"), 1, FAILURE_VOCABULARY[13], "candidate.specimen_count")
    expect(specimen.get("evidence_kind"), EVIDENCE_KIND, FAILURE_VOCABULARY[12], "candidate.evidence_kind")
    generalization = candidate.get("generalization_status", {})
    expect(generalization.get("generalization_status"), GENERALIZATION_STATUS, FAILURE_VOCABULARY[14], "candidate.generalization_status")
    expect_true(generalization.get("local_candidate_only"), FAILURE_VOCABULARY[14], "candidate.local_candidate_only")
    expect_false(generalization.get("general_shape_claimed"), FAILURE_VOCABULARY[15], "candidate.general_shape_claimed")
    expect_false(generalization.get("multi_specimen_stability_claimed"), FAILURE_VOCABULARY[16], "candidate.multi_specimen_stability_claimed")
    expect_false(generalization.get("cross_context_stability_claimed"), FAILURE_VOCABULARY[17], "candidate.cross_context_stability_claimed")
    expect(candidate.get("allowed_candidate_use"), ALLOWED_USE, FAILURE_VOCABULARY[11], "candidate.allowed_candidate_use")
    expect(candidate.get("forbidden_candidate_use"), FORBIDDEN_USE, FAILURE_VOCABULARY[11], "candidate.forbidden_candidate_use")

    authority = candidate.get("authority_boundaries", {})
    expect_false(authority.get("candidate_grants_authority"), FAILURE_VOCABULARY[25], "candidate.candidate_grants_authority")
    expect_false(authority.get("candidate_replaces_source_authority"), FAILURE_VOCABULARY[25], "candidate.candidate_replaces_source_authority")
    expect_false(authority.get("candidate_authorizes_reuse"), FAILURE_VOCABULARY[20], "candidate.candidate_authorizes_reuse")
    expect_false(authority.get("candidate_authorizes_execution"), FAILURE_VOCABULARY[23], "candidate.candidate_authorizes_execution")
    expect_true(authority.get("source_records_remain_authority"), FAILURE_VOCABULARY[25], "candidate.source_records_remain_authority")

    radius = candidate.get("radius_boundaries", {})
    expect(radius.get("source_radius_limit"), RADIUS_LIMIT, FAILURE_VOCABULARY[21], "candidate.source_radius_limit")
    expect(radius.get("source_radius_after"), 0, FAILURE_VOCABULARY[21], "candidate.source_radius_after")
    expect_true(radius.get("source_radius_exhausted"), FAILURE_VOCABULARY[21], "candidate.source_radius_exhausted")
    expect_false(radius.get("candidate_renews_radius"), FAILURE_VOCABULARY[21], "candidate.candidate_renews_radius")
    expect_false(radius.get("candidate_authorizes_additional_machine_proceed"), FAILURE_VOCABULARY[22], "candidate.candidate_authorizes_additional_machine_proceed")

    runner = candidate.get("runner_boundaries", {})
    for key in ["candidate_is_runner_input", "candidate_authorizes_runner", "candidate_defines_runner_policy", "candidate_routes_runner", "runner_authority_created"]:
        expect_false(runner.get(key), FAILURE_VOCABULARY[24], f"candidate.runner_boundaries.{key}")
    activation = candidate.get("activation_boundaries", {})
    expect_false(activation.get("active_registry_entry_created"), FAILURE_VOCABULARY[18], "candidate.active_registry_entry_created")
    expect(activation.get("activation_status"), "ACTIVATION_INACTIVE", FAILURE_VOCABULARY[19], "candidate.activation_status")
    expect_false(activation.get("candidate_can_self_activate"), FAILURE_VOCABULARY[19], "candidate.candidate_can_self_activate")
    expect(candidate.get("promotion_boundaries", {}).get("promotion_status"), "REGISTRY_PROMOTION_NOT_REQUESTED", FAILURE_VOCABULARY[18], "candidate.promotion_status")
    expect_false(candidate.get("promotion_boundaries", {}).get("promotion_granted_by_candidate"), FAILURE_VOCABULARY[18], "candidate.promotion_granted_by_candidate")
    expect(candidate.get("revocation_or_expiry", {}).get("revocation_status"), "NOT_REVOKED", FAILURE_VOCABULARY[11], "candidate.revocation_status")
    expect(candidate.get("revocation_or_expiry", {}).get("expiry_status"), "NOT_EXPIRED", FAILURE_VOCABULARY[11], "candidate.expiry_status")
    expect(candidate.get("audit_requirements", {}).get("next_required_object"), "c8_n22_radius_bound_prepare_trace_registry_candidate_audit_v0", FAILURE_VOCABULARY[3], "candidate.next_required_object")
    for key, value in candidate.get("candidate_non_effects", {}).items():
        expect_false(value, FAILURE_VOCABULARY[18], f"candidate.candidate_non_effects.{key}")
    expect(candidate.get("candidate_gate", {}).get("failures"), [], FAILURE_VOCABULARY[11], "candidate.candidate_gate.failures")

    expect(closure.get("compression_closure_id"), COMPRESSION_CLOSURE_ID, FAILURE_VOCABULARY[4], "closure.compression_closure_id")
    expect(closure.get("closure_status"), COMPRESSION_CLOSURE_STATUS, FAILURE_VOCABULARY[5], "closure.closure_status")
    expect_true(closure.get("source_of_truth_rule", {}).get("formal_source_chain_remains_authority"), FAILURE_VOCABULARY[25], "closure.formal_source_chain_remains_authority")
    expect(packet.get("compressed_packet_id"), COMPRESSED_PACKET_ID, FAILURE_VOCABULARY[6], "packet.compressed_packet_id")
    expect(packet.get("packet_role"), PACKET_ROLE, FAILURE_VOCABULARY[6], "packet.packet_role")
    expect(packet.get("target_trace_label"), TRACE_LABEL, FAILURE_VOCABULARY[6], "packet.target_trace_label")
    expect(audit.get("decompression_audit_id"), DECOMPRESSION_AUDIT_ID, FAILURE_VOCABULARY[7], "audit.decompression_audit_id")
    expect(audit.get("audit_result", {}).get("decompression_audit_status"), DECOMPRESSION_AUDIT_STATUS, FAILURE_VOCABULARY[8], "audit.decompression_audit_status")
    expect_true(audit.get("critical_field_group_audit_summary", {}).get("all_critical_field_groups_recovered"), FAILURE_VOCABULARY[8], "audit.all_critical_field_groups_recovered")
    expect(machine.get("closure_id"), D5_SPECIMEN_ID, FAILURE_VOCABULARY[12], "machine.closure_id")
    expect(machine.get("radius_result", {}).get("radius_limit"), RADIUS_LIMIT, FAILURE_VOCABULARY[21], "machine.radius_limit")
    expect(machine.get("radius_result", {}).get("radius_after"), 0, FAILURE_VOCABULARY[21], "machine.radius_after")
    expect_true(machine.get("radius_result", {}).get("radius_exhausted"), FAILURE_VOCABULARY[21], "machine.radius_exhausted")


def build_audit(hashes: dict[str, str], commits: dict[str, str]) -> dict[str, Any]:
    compliance = {
        "source_registry_schema_id": REGISTRY_SCHEMA_ID,
        "required_field_group_count_from_contract": 18,
        "candidate_field_group_count_present": 18,
        "candidate_declares_all_required_groups": True,
        **{key: True for key in GROUP_AUDIT_KEYS},
        "all_required_field_groups_passed": True,
    }
    audit_non_effects = {
        "source_candidate_modified": False,
        "active_registry_entry_created": False,
        "registry_entry_activated": False,
        "source_authority_replaced": False,
        "reuse_authorized": False,
        "radius_renewed": False,
        "additional_machine_proceed_authorized": False,
        "machine_action_performed": False,
        "runner_authority_created": False,
        "generalized_pattern_created": False,
        "promotion_granted": False,
        "f4_closure_created": False,
        "block_f_closed": False,
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "registry_candidate_audit_id": AUDIT_ID,
        "audit_role": AUDIT_ROLE,
        "audit_status": AUDIT_STATUS,
        "audited_candidate_id": CANDIDATE_ID,
        "block_id": BLOCK_ID,
        "block_unit_id": BLOCK_UNIT_ID,
        "generated_by": GENERATOR,
        "audit_pass_meaning": {
            "candidate_admissibility_audit_passed": True,
            "candidate_record_admissible_as_local_only": True,
            "active_registry_acceptance_passed": False,
            "registry_entry_activation_passed": False,
            "reuse_authorization_passed": False,
            "runner_authorization_passed": False,
            "generalization_passed": False,
            "audit_pass_does_not_mean_active": True,
            "audit_pass_does_not_mean_reusable": True,
            "audit_pass_does_not_mean_generalized": True,
            "audit_pass_does_not_mean_runner_ready": True,
        },
        "source_integrity": {
            "registry_schema_contract_present": True,
            "registry_candidate_present": True,
            "compression_closure_present": True,
            "compressed_packet_present": True,
            "decompression_audit_present": True,
            "registry_schema_contract_hash_verified": True,
            "registry_candidate_hash_verified": True,
            "compression_closure_hash_verified": True,
            "compressed_packet_hash_verified": True,
            "decompression_audit_hash_verified": True,
            "source_identity_resolved_by_explicit_paths": True,
            "mtime_or_latest_resolution_allowed": False,
            "directory_scan_authority_allowed": False,
        },
        "source_hashes": {
            "registry_schema_contract_sha256": hashes[F1_SCHEMA],
            "registry_candidate_sha256": hashes[F2_CANDIDATE],
            "compression_closure_sha256": hashes[E4_CLOSURE],
            "compressed_packet_sha256": hashes[E2_PACKET],
            "decompression_audit_sha256": hashes[E3_AUDIT],
            "supporting_machine_proceed_closure_sha256": hashes[D5_CLOSURE],
            "source_file_hash_algorithm": "sha256",
            "source_file_hashes": hashes,
            "source_file_commits": commits,
            "source_hash_verification_basis": "WORKTREE_FILE_MATCHES_HEAD_BLOB",
        },
        "source_registry_schema_contract": {
            "registry_schema_id": REGISTRY_SCHEMA_ID,
            "schema_version": REGISTRY_SCHEMA_VERSION,
            "schema_role": REGISTRY_SCHEMA_ROLE,
            "registry_kind": REGISTRY_KIND,
            "schema_scope": REGISTRY_SCHEMA_SCOPE,
            "schema_status": REGISTRY_SCHEMA_STATUS,
            "required_field_group_count": 18,
        },
        "source_registry_candidate": {
            "registry_candidate_id": CANDIDATE_ID,
            "schema_version": CANDIDATE_SCHEMA_VERSION,
            "candidate_role": CANDIDATE_ROLE,
            "candidate_status": CANDIDATE_STATUS,
            "candidate_creation_status": CANDIDATE_CREATION_STATUS,
            "admissibility_audit_status_before_f3": PENDING_F3,
            "candidate_card_created": True,
            "candidate_queue_entry_only": True,
            "trace_registered_as_active_entry": False,
            "trace_registered_as_reusable_pattern": False,
        },
        "candidate_admissibility_result": {
            "candidate_admissible": True,
            "admissible_scope": "LOCAL_CANDIDATE_ONLY",
            "admissible_as_active_registry_entry": False,
            "admissible_as_reusable_pattern": False,
            "admissible_as_generalized_pattern": False,
            "admissible_as_runner_input": False,
            "admissible_as_machine_proceed_source": False,
        },
        "schema_contract_compliance_audit": compliance,
        "source_chain_audit": {
            "compression_closure_id": COMPRESSION_CLOSURE_ID,
            "compression_closure_status": COMPRESSION_CLOSURE_STATUS,
            "compression_closure_passed": True,
            "compressed_packet_id": COMPRESSED_PACKET_ID,
            "compressed_packet_present": True,
            "decompression_audit_id": DECOMPRESSION_AUDIT_ID,
            "decompression_audit_status": DECOMPRESSION_AUDIT_STATUS,
            "decompression_audit_passed": True,
            "formal_source_chain_remains_authority": True,
            "candidate_may_stand_alone_without_source": False,
            "source_records_remain_authority": True,
        },
        "trace_identity_audit": {
            "trace_label": TRACE_LABEL,
            "trace_scope": TRACE_SCOPE,
            "trace_label_authority_effect": "NONE",
            "trace_label_reuse_effect": "NONE",
            "trace_label_runner_effect": "NONE",
            "trace_label_present": True,
            "trace_scope_local_only": True,
            "trace_label_has_no_authority_effect": True,
            "trace_label_has_no_reuse_effect": True,
            "trace_label_has_no_runner_effect": True,
        },
        "specimen_count_audit": {
            "specimen_count": 1,
            "specimen_count_declared": True,
            "specimen_count_equals_one": True,
            "evidence_kind": EVIDENCE_KIND,
            "minimum_specimens_for_generalization_met": False,
            "single_specimen_only": True,
            "single_specimen_is_stability_evidence": False,
            "single_specimen_is_generalization_evidence": False,
            "single_specimen_is_runner_admissibility_evidence": False,
            "multi_specimen_stability_requires_future_candidates_and_audit": True,
            "specimen_count_audit_passed": True,
        },
        "generalization_audit": {
            "generalization_status": GENERALIZATION_STATUS,
            "local_candidate_only": True,
            "single_specimen_only": True,
            "general_shape_claimed": False,
            "multi_specimen_stability_claimed": False,
            "cross_context_stability_claimed": False,
            "generalization_overclaim_detected": False,
            "multi_specimen_stability_overclaim_detected": False,
            "cross_context_stability_overclaim_detected": False,
            "generalization_audit_passed": True,
        },
        "candidate_stage_use_audit": {
            **ALLOWED_USE,
            "candidate_stage_allowed_use_audit_passed": True,
        },
        "forbidden_use_audit": {
            **{f"{key}_forbidden": value for key, value in FORBIDDEN_USE.items()},
            "forbidden_use_audit_passed": True,
        },
        "authority_boundary_audit": {
            "candidate_grants_authority": False,
            "candidate_replaces_source_authority": False,
            "candidate_authorizes_reuse": False,
            "candidate_authorizes_execution": False,
            "candidate_changes_authority_state": False,
            "source_records_remain_authority": True,
            "authority_smuggling_detected": False,
            "authority_boundary_audit_passed": True,
        },
        "radius_boundary_audit": {
            "source_radius_limit": RADIUS_LIMIT,
            "source_radius_after": 0,
            "source_radius_exhausted": True,
            "candidate_renews_radius": False,
            "candidate_creates_radius": False,
            "candidate_authorizes_additional_machine_proceed": False,
            "additional_use_requires_new_authority_or_radius": True,
            "radius_renewal_detected": False,
            "additional_machine_proceed_authorization_detected": False,
            "radius_boundary_audit_passed": True,
        },
        "runner_boundary_audit": {
            "candidate_is_runner_input": False,
            "candidate_authorizes_runner": False,
            "candidate_defines_runner_policy": False,
            "candidate_routes_runner": False,
            "runner_authority_created": False,
            "future_runner_analysis_may_reference_candidate_after_admissibility_or_separate_surface": True,
            "reference_does_not_create_runner_authority": True,
            "runner_authority_smuggling_detected": False,
            "runner_boundary_audit_passed": True,
        },
        "activation_boundary_audit": {
            "active_registry_entry_created": False,
            "registry_entry_activated": False,
            "activation_status": "ACTIVATION_INACTIVE",
            "activation_requires_human_decision": True,
            "activation_requires_separate_apply_object": True,
            "candidate_can_self_activate": False,
            "activation_smuggling_detected": False,
            "activation_boundary_audit_passed": True,
        },
        "promotion_boundary_audit": {
            "promotion_status": "REGISTRY_PROMOTION_NOT_REQUESTED",
            "promotion_decision_required": True,
            "promotion_receipt_required": True,
            "promotion_apply_required": True,
            "promotion_granted_by_candidate": False,
            "promotion_smuggling_detected": False,
            "promotion_boundary_audit_passed": True,
        },
        "revocation_or_expiry_audit": {
            "revocation_status": "NOT_REVOKED",
            "expiry_status": "NOT_EXPIRED",
            "supersession_status": "NOT_SUPERSEDED",
            "invalidated_by_source_mismatch": False,
            "revocation_requires_record": True,
            "revocation_or_expiry_audit_passed": True,
        },
        "f4_handoff": {
            "next_required_object": NEXT_OBJECT,
            "next_required_unit": NEXT_UNIT,
            "f4_closure_created_by_f3": False,
            "block_f_closed_by_f3": False,
            "f3_terminal_transition": TERMINAL_TRANSITION,
        },
        "audit_non_effects": audit_non_effects,
        "audit_gate": {
            "registry_candidate_admissibility_audit_gate": AUDIT_STATUS,
            "registry_schema_contract_present": True,
            "registry_schema_contract_passed": True,
            "registry_candidate_present": True,
            "registry_candidate_status": CANDIDATE_STATUS,
            "candidate_creation_status": CANDIDATE_CREATION_STATUS,
            "candidate_was_pending_f3_audit": True,
            "compression_closure_present": True,
            "compression_closure_passed": True,
            "compressed_packet_present": True,
            "decompression_audit_present": True,
            "decompression_audit_passed": True,
            "source_hashes_verified": True,
            "source_identity_resolved_by_explicit_paths": True,
            "required_field_groups_present": True,
            "required_field_group_count": 18,
            "all_required_field_groups_passed": True,
            "trace_label": TRACE_LABEL,
            "trace_scope": TRACE_SCOPE,
            "specimen_count_declared": True,
            "specimen_count_equals_one": True,
            "evidence_kind": EVIDENCE_KIND,
            "local_only_status_preserved": True,
            "no_generalization_claimed": True,
            "no_multi_specimen_stability_claimed": True,
            "no_cross_context_stability_claimed": True,
            "no_active_registry_created": True,
            "no_registry_entry_activated": True,
            "no_reuse_authorized": True,
            "no_radius_renewed": True,
            "no_additional_machine_proceed_authorized": True,
            "no_machine_action_performed": True,
            "no_runner_authority_created": True,
            "no_generalized_pattern_created": True,
            "no_source_authority_replaced": True,
            "audit_admits_candidate_as_local_only": True,
            "audit_does_not_activate_candidate": True,
            "audit_does_not_authorize_reuse": True,
            "audit_does_not_generalize_trace": True,
            "audit_does_not_create_runner_authority": True,
            "next_required_object": NEXT_OBJECT,
            "failures": [],
        },
        "failure_vocabulary": FAILURE_VOCABULARY,
        "most_important_failures": [
            "REGISTRY_CANDIDATE_AUDIT_FAIL_GENERALIZATION_CLAIMED",
            "REGISTRY_CANDIDATE_AUDIT_FAIL_ACTIVE_REGISTRY_CREATED",
            "REGISTRY_CANDIDATE_AUDIT_FAIL_REUSE_AUTHORIZED",
            "REGISTRY_CANDIDATE_AUDIT_FAIL_RUNNER_AUTHORITY_CREATED",
            "REGISTRY_CANDIDATE_AUDIT_FAIL_SOURCE_CANDIDATE_MODIFIED",
        ],
        "non_claims": NON_CLAIMS,
        "key_non_claims": KEY_NON_CLAIMS,
        "precommit_c8_n22_registry_candidate_admissibility_audit_gate": "PASS",
        "registry_candidate_admissibility_audit_gate": AUDIT_STATUS,
        "terminal_transition": TERMINAL_TRANSITION,
    }


def validate_audit(audit: dict[str, Any]) -> None:
    expect(audit.get("schema_version"), SCHEMA_VERSION, FAILURE_VOCABULARY[11], "audit.schema_version")
    expect(audit.get("registry_candidate_audit_id"), AUDIT_ID, FAILURE_VOCABULARY[11], "audit.registry_candidate_audit_id")
    expect(audit.get("audit_status"), AUDIT_STATUS, FAILURE_VOCABULARY[11], "audit.audit_status")
    compliance = audit.get("schema_contract_compliance_audit", {})
    expect(compliance.get("required_field_group_count_from_contract"), 18, FAILURE_VOCABULARY[11], "audit.required_field_group_count")
    for key in GROUP_AUDIT_KEYS:
        expect_true(compliance.get(key), FAILURE_VOCABULARY[11], f"audit.{key}")
    for key, value in audit.get("audit_non_effects", {}).items():
        expect_false(value, FAILURE_VOCABULARY[18], f"audit.audit_non_effects.{key}")
    expect(audit.get("audit_gate", {}).get("failures"), [], FAILURE_VOCABULARY[11], "audit.audit_gate.failures")
    expect(audit.get("terminal_transition"), TERMINAL_TRANSITION, FAILURE_VOCABULARY[28], "audit.terminal_transition")


def render_markdown() -> str:
    return f"""# C8 n22 radius-bound prepare trace registry candidate admissibility audit v0

## Status

{AUDIT_STATUS}

## Audited candidate

{CANDIDATE_ID}

## Registry schema contract

{REGISTRY_SCHEMA_ID}

## Trace label

{TRACE_LABEL}

## Trace scope

{TRACE_SCOPE}

## Audit result

- candidate admissible: true
- admissible scope: LOCAL_CANDIDATE_ONLY
- active registry acceptance passed: false
- reuse authorization passed: false
- generalization passed: false
- runner authorization passed: false

## Evidence checked

- F.1 schema contract present
- F.2 candidate present
- E.4 compression closure passed
- E.2 compressed packet present
- E.3 decompression audit passed
- source hashes verified
- source identity resolved by explicit paths

## Specimen-count audit

- specimen count: 1
- evidence kind: {EVIDENCE_KIND}
- single specimen is stability evidence: false
- single specimen is generalization evidence: false
- single specimen is runner admissibility evidence: false

## Generalization audit

- general shape claimed: false
- multi-specimen stability claimed: false
- cross-context stability claimed: false
- local candidate only: true

## Boundary audit

- no active registry entry created
- no registry entry activated
- no reuse authorized
- no radius renewed
- no additional machine proceed authorized
- no machine action performed
- no runner authority created
- no generalized pattern created
- source records remain authority
- F.2 candidate record not modified

## Next

Registry candidate closure is required."""


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
        (F2_CANDIDATE, FAILURE_VOCABULARY[2]),
        (E4_CLOSURE, FAILURE_VOCABULARY[4]),
        (E2_PACKET, FAILURE_VOCABULARY[6]),
        (E3_AUDIT, FAILURE_VOCABULARY[7]),
        (D5_CLOSURE, FAILURE_VOCABULARY[12]),
    ]:
        data, digest, commit = load_committed_json(root, relative_path, missing_code)
        sources[relative_path] = data
        hashes[relative_path] = digest
        commits[relative_path] = commit

    validate_sources(sources)
    audit = build_audit(hashes, commits)
    validate_audit(audit)
    write_text(root / OUTPUT_JSON, json.dumps(audit, indent=2, sort_keys=True))
    write_text(root / OUTPUT_MD, render_markdown())
    print(f"Wrote {OUTPUT_JSON}")
    print(f"Wrote {OUTPUT_MD}")
    print(f"registry_candidate_admissibility_audit_gate={AUDIT_STATUS}")
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
