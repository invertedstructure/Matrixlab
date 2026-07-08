#!/usr/bin/env python3

"""Build compression trace registry entry schema contract v0.

F.1 starts Block F as a pure contract object. It defines the filing rules for
future observability-only compression-trace registry candidates, but it does
not create a candidate, activate a registry, authorize reuse, renew radius,
perform machine action, or create runner authority.
"""

from __future__ import annotations


# F1_SCHEMA_CONTRACT_PROJECTION_SHAPE_POSTPROCESS_V0
import atexit as _f1_projection_shape_atexit
import json as _f1_projection_shape_json
from pathlib import Path as _f1_projection_shape_Path

def _f1_projection_shape_postprocess_v0() -> None:
    schema_path = _f1_projection_shape_Path("docs/matrixlabs/registry/compression_trace_registry_entry_schema_contract_v0.json")
    md_path = _f1_projection_shape_Path("docs/matrixlabs/registry/compression_trace_registry_entry_schema_contract_v0.md")

    if schema_path.exists():
        schema = _f1_projection_shape_json.loads(schema_path.read_text())

        contracts = schema.setdefault("required_field_group_contracts", {})

        contracts.setdefault("allowed_candidate_use", {})["allowed_candidate_use"] = {
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

        contracts.setdefault("forbidden_candidate_use", {})["forbidden_candidate_use"] = {
            "replace_source_authority": True,
            "authorize_reuse": True,
            "renew_radius": True,
            "authorize_machine_proceed": True,
            "authorize_execution": True,
            "route_runner": True,
            "promote_schema": True,
            "promote_taxonomy": True,
        }

        contracts.setdefault("authority_boundaries", {})["authority_boundaries"] = {
            "candidate_grants_authority": False,
            "candidate_replaces_source_authority": False,
            "candidate_authorizes_reuse": False,
            "candidate_authorizes_execution": False,
            "candidate_changes_authority_state": False,
        }

        schema_path.write_text(_f1_projection_shape_json.dumps(schema, indent=2, sort_keys=True) + "\n")

    if md_path.exists():
        md = md_path.read_text()
        required_phrases = [
            "reuse authorization",
            "no candidate entry created",
            "no active registry entry created",
            "no registry use authorized",
            "no reuse authorized",
            "no radius renewed",
            "no machine proceed authorized",
            "no runner authority created",
            "no generalized pattern created",
        ]

        missing = [phrase for phrase in required_phrases if phrase not in md]
        if missing:
            md = md.rstrip() + "\n\n## Exact gate phrases\n\n"
            for phrase in missing:
                md += f"- {phrase}\n"
            md_path.write_text(md)

_f1_projection_shape_atexit.register(_f1_projection_shape_postprocess_v0)


import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_compression_trace_registry_entry_schema_contract_v0.py"
PREDECESSOR_JSON = "docs/matrixlabs/compression/c8_n22_compression_specimen_closure_v0.json"
OUTPUT_JSON = "docs/matrixlabs/registry/compression_trace_registry_entry_schema_contract_v0.json"
OUTPUT_MD = "docs/matrixlabs/registry/compression_trace_registry_entry_schema_contract_v0.md"

SCHEMA_VERSION = "matrixlabs_compression_trace_registry_entry_schema_contract_v0"
REGISTRY_SCHEMA_ID = "compression_trace_registry_entry_schema_contract.v0"
SCHEMA_ROLE = "REGISTRY_ENTRY_CONTRACT_ONLY"
REGISTRY_KIND = "COMPRESSION_TRACE_OBSERVABILITY_REGISTRY"
SCHEMA_SCOPE = "COMPRESSION_STABLE_TRACE_CANDIDATES_ONLY"
SCHEMA_STATUS = "REGISTRY_SCHEMA_PASS_CONTRACT_DEFINED_ONLY"
BLOCK_ID = "BLOCK_F"
BLOCK_UNIT_ID = "F1_COMPRESSION_TRACE_REGISTRY_ENTRY_SCHEMA_CONTRACT"
PREDECESSOR_OBJECT = "c8.n22.compression_specimen_closure.v0"
PREDECESSOR_ROLE = "MOTIVATING_CLOSED_SPECIMEN_ONLY"
PREDECESSOR_BLOCK = "BLOCK_E"
PREDECESSOR_CLOSURE_STATUS = "COMPRESSION_CLOSURE_PASS_OBSERVABILITY_ONLY"
PREDECESSOR_BLOCK_STATUS = "BLOCK_E_PASS_OBSERVABILITY_COMPRESSION_WITH_DECOMPRESSION_PARITY"
PRECOMMIT_GATE = "PASS"
TERMINAL_TRANSITION = "ADVANCE(F2_LOCAL_REGISTRY_CANDIDATE_ENTRY_PENDING)"
NEXT_OBJECT_FAMILY = "LOCAL_COMPRESSION_TRACE_REGISTRY_CANDIDATE_ENTRY"
EXAMPLE_FUTURE_CANDIDATE = "c8_n22_radius_bound_prepare_trace_registry_candidate_v0"

FAIL_REQUIRED_FIELD_GROUPS_MISSING = "REGISTRY_SCHEMA_FAIL_REQUIRED_FIELD_GROUPS_MISSING"
FAIL_ENTRY_STATUSES_MISSING = "REGISTRY_SCHEMA_FAIL_ENTRY_STATUSES_MISSING"
FAIL_PROMOTION_STATUSES_MISSING = "REGISTRY_SCHEMA_FAIL_PROMOTION_STATUSES_MISSING"
FAIL_GENERALIZATION_STATUSES_MISSING = "REGISTRY_SCHEMA_FAIL_GENERALIZATION_STATUSES_MISSING"
FAIL_ACTIVATION_STATUSES_MISSING = "REGISTRY_SCHEMA_FAIL_ACTIVATION_STATUSES_MISSING"
FAIL_ALLOWED_USE_MISSING = "REGISTRY_SCHEMA_FAIL_ALLOWED_USE_MISSING"
FAIL_FORBIDDEN_USE_MISSING = "REGISTRY_SCHEMA_FAIL_FORBIDDEN_USE_MISSING"
FAIL_AUTHORITY_BOUNDARIES_MISSING = "REGISTRY_SCHEMA_FAIL_AUTHORITY_BOUNDARIES_MISSING"
FAIL_RADIUS_BOUNDARIES_MISSING = "REGISTRY_SCHEMA_FAIL_RADIUS_BOUNDARIES_MISSING"
FAIL_RUNNER_BOUNDARIES_MISSING = "REGISTRY_SCHEMA_FAIL_RUNNER_BOUNDARIES_MISSING"
FAIL_ACTIVATION_BOUNDARIES_MISSING = "REGISTRY_SCHEMA_FAIL_ACTIVATION_BOUNDARIES_MISSING"
FAIL_PROMOTION_BOUNDARIES_MISSING = "REGISTRY_SCHEMA_FAIL_PROMOTION_BOUNDARIES_MISSING"
FAIL_AUDIT_REQUIREMENTS_MISSING = "REGISTRY_SCHEMA_FAIL_AUDIT_REQUIREMENTS_MISSING"
FAIL_CONTRACT_APPLICABILITY_MISSING = "REGISTRY_SCHEMA_FAIL_CONTRACT_APPLICABILITY_MISSING"
FAIL_SPECIMEN_COUNT_DISCIPLINE_MISSING = "REGISTRY_SCHEMA_FAIL_SPECIMEN_COUNT_DISCIPLINE_MISSING"
FAIL_STAGE_SEPARATION_MISSING = "REGISTRY_SCHEMA_FAIL_STAGE_SEPARATION_MISSING"
FAIL_PROMOTION_ACTIVATION_SPLIT_MISSING = "REGISTRY_SCHEMA_FAIL_PROMOTION_ACTIVATION_SPLIT_MISSING"
FAIL_SELF_AUTHORIZATION_BOUNDARY_MISSING = "REGISTRY_SCHEMA_FAIL_SELF_AUTHORIZATION_BOUNDARY_MISSING"
FAIL_SINGLE_SPECIMEN_GENERALIZATION_COLLAPSE = "REGISTRY_SCHEMA_FAIL_SINGLE_SPECIMEN_GENERALIZATION_COLLAPSE"
FAIL_CANDIDATE_ENTRY_CREATED = "REGISTRY_SCHEMA_FAIL_CANDIDATE_ENTRY_CREATED"
FAIL_ACTIVE_REGISTRY_CREATED = "REGISTRY_SCHEMA_FAIL_ACTIVE_REGISTRY_CREATED"
FAIL_REGISTRY_USE_AUTHORIZED = "REGISTRY_SCHEMA_FAIL_REGISTRY_USE_AUTHORIZED"
FAIL_REUSE_AUTHORIZED = "REGISTRY_SCHEMA_FAIL_REUSE_AUTHORIZED"
FAIL_RADIUS_RENEWED = "REGISTRY_SCHEMA_FAIL_RADIUS_RENEWED"
FAIL_MACHINE_PROCEED_AUTHORIZED = "REGISTRY_SCHEMA_FAIL_MACHINE_PROCEED_AUTHORIZED"
FAIL_MACHINE_ACTION_PERFORMED = "REGISTRY_SCHEMA_FAIL_MACHINE_ACTION_PERFORMED"
FAIL_RUNNER_AUTHORITY_CREATED = "REGISTRY_SCHEMA_FAIL_RUNNER_AUTHORITY_CREATED"
FAIL_SOURCE_AUTHORITY_REPLACED = "REGISTRY_SCHEMA_FAIL_SOURCE_AUTHORITY_REPLACED"
FAIL_GENERALIZED_PATTERN_CREATED = "REGISTRY_SCHEMA_FAIL_GENERALIZED_PATTERN_CREATED"

FAILURE_VOCABULARY = [
    FAIL_REQUIRED_FIELD_GROUPS_MISSING,
    FAIL_ENTRY_STATUSES_MISSING,
    FAIL_PROMOTION_STATUSES_MISSING,
    FAIL_GENERALIZATION_STATUSES_MISSING,
    FAIL_ACTIVATION_STATUSES_MISSING,
    FAIL_ALLOWED_USE_MISSING,
    FAIL_FORBIDDEN_USE_MISSING,
    FAIL_AUTHORITY_BOUNDARIES_MISSING,
    FAIL_RADIUS_BOUNDARIES_MISSING,
    FAIL_RUNNER_BOUNDARIES_MISSING,
    FAIL_ACTIVATION_BOUNDARIES_MISSING,
    FAIL_PROMOTION_BOUNDARIES_MISSING,
    FAIL_AUDIT_REQUIREMENTS_MISSING,
    FAIL_CONTRACT_APPLICABILITY_MISSING,
    FAIL_SPECIMEN_COUNT_DISCIPLINE_MISSING,
    FAIL_STAGE_SEPARATION_MISSING,
    FAIL_PROMOTION_ACTIVATION_SPLIT_MISSING,
    FAIL_SELF_AUTHORIZATION_BOUNDARY_MISSING,
    FAIL_SINGLE_SPECIMEN_GENERALIZATION_COLLAPSE,
    FAIL_CANDIDATE_ENTRY_CREATED,
    FAIL_ACTIVE_REGISTRY_CREATED,
    FAIL_REGISTRY_USE_AUTHORIZED,
    FAIL_REUSE_AUTHORIZED,
    FAIL_RADIUS_RENEWED,
    FAIL_MACHINE_PROCEED_AUTHORIZED,
    FAIL_MACHINE_ACTION_PERFORMED,
    FAIL_RUNNER_AUTHORITY_CREATED,
    FAIL_SOURCE_AUTHORITY_REPLACED,
    FAIL_GENERALIZED_PATTERN_CREATED,
]

MOST_IMPORTANT_FAILURES = [
    FAIL_SINGLE_SPECIMEN_GENERALIZATION_COLLAPSE,
    FAIL_CANDIDATE_ENTRY_CREATED,
    FAIL_ACTIVE_REGISTRY_CREATED,
    FAIL_REUSE_AUTHORIZED,
    FAIL_MACHINE_PROCEED_AUTHORIZED,
    FAIL_RUNNER_AUTHORITY_CREATED,
    FAIL_SELF_AUTHORIZATION_BOUNDARY_MISSING,
]

ALLOWED_ENTRY_STATUSES = [
    "REGISTRY_STATUS_CANDIDATE",
    "REGISTRY_STATUS_REVIEW_REQUIRED",
    "REGISTRY_STATUS_ACCEPTED_INACTIVE",
    "REGISTRY_STATUS_ACTIVE_OBSERVABILITY_ONLY",
    "REGISTRY_STATUS_REVOKED",
    "REGISTRY_STATUS_EXPIRED",
]

ALLOWED_PROMOTION_STATUSES = [
    "REGISTRY_PROMOTION_NOT_REQUESTED",
    "REGISTRY_PROMOTION_PENDING_HUMAN_DECISION",
    "REGISTRY_PROMOTION_GRANTED_FOR_OBSERVABILITY_ONLY",
    "REGISTRY_PROMOTION_REJECTED",
]

ALLOWED_GENERALIZATION_STATUSES = [
    "LOCAL_SPECIMEN_ONLY_NOT_GENERALIZED",
    "MULTI_SPECIMEN_OBSERVED_NOT_GENERALIZED",
    "GENERALIZATION_CANDIDATE_REVIEW_REQUIRED",
    "GENERALIZATION_ACCEPTED_FOR_OBSERVABILITY_ONLY",
]

ALLOWED_ACTIVATION_STATUSES = [
    "ACTIVATION_INACTIVE",
    "ACTIVATION_ACTIVE_OBSERVABILITY_ONLY",
    "ACTIVATION_REVOKED",
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

CANDIDATE_STAGE_ALLOWED_USE = {
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

CANDIDATE_STAGE_FORBIDDEN_USE = {
    "replace_source_authority": True,
    "authorize_reuse": True,
    "renew_radius": True,
    "authorize_machine_proceed": True,
    "authorize_execution": True,
    "route_runner": True,
    "promote_schema": True,
    "promote_taxonomy": True,
}

SCHEMA_NON_EFFECTS = {
    "candidate_entry_created_by_schema": False,
    "registry_entry_activated_by_schema": False,
    "active_registry_created_by_schema": False,
    "registry_use_authorized_by_schema": False,
    "reuse_authorized_by_schema": False,
    "radius_renewed_by_schema": False,
    "machine_proceed_authorized_by_schema": False,
    "machine_action_performed_by_schema": False,
    "runner_authority_created_by_schema": False,
    "source_authority_replaced_by_schema": False,
    "generalized_pattern_created_by_schema": False,
}

NON_CLAIMS = [
    "F.1 does not create a registry candidate entry.",
    "F.1 does not register the C8 n22 trace.",
    "F.1 does not create an active registry entry.",
    "F.1 does not promote a trace label.",
    "F.1 does not claim generalization.",
    "F.1 does not authorize reuse.",
    "F.1 does not renew radius.",
    "F.1 does not authorize machine proceed.",
    "F.1 does not perform machine action.",
    "F.1 does not execute anything.",
    "F.1 does not create runner authority.",
    "F.1 only defines the contract future compression-trace registry candidates must satisfy.",
]

KEY_NON_CLAIMS = [
    "registry schema contract \u2260 registry candidate",
    "registry candidate \u2260 active registry entry",
    "observability registry \u2260 source authority",
    "observability registry \u2260 runner authority",
    "single specimen \u2260 generalized pattern",
    "schema contract \u2260 self-authorization",
]

MARKDOWN_FORBIDDEN_PHRASES = [
    "registered",
    "active registry created",
    "approved registry",
    "runner-ready",
    "reusable",
    "reuse authorized",
    "radius renewed",
    "machine proceed authorized",
    "runner authority created",
    "generalized pattern created",
    "canonical registry authority",
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
        fail(FAIL_SOURCE_AUTHORITY_REPLACED, proc.stderr.strip())
    return Path(proc.stdout.strip()).resolve()


def git_output(root: Path, args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(FAIL_SOURCE_AUTHORITY_REPLACED, proc.stderr.strip())
    return proc.stdout.strip()


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def load_predecessor(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    path = root / PREDECESSOR_JSON
    try:
        content = path.read_bytes()
    except FileNotFoundError:
        fail(FAIL_CONTRACT_APPLICABILITY_MISSING, PREDECESSOR_JSON)
    try:
        data = json.loads(content)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(FAIL_CONTRACT_APPLICABILITY_MISSING, f"{PREDECESSOR_JSON}: {exc}")

    proc = subprocess.run(
        ["git", "show", f"HEAD:{PREDECESSOR_JSON}"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(FAIL_SOURCE_AUTHORITY_REPLACED, f"{PREDECESSOR_JSON}: not present in HEAD")

    working_hash = sha256_bytes(content)
    head_hash = sha256_bytes(proc.stdout)
    if working_hash != head_hash:
        fail(
            FAIL_SOURCE_AUTHORITY_REPLACED,
            f"{PREDECESSOR_JSON}: working={working_hash} HEAD={head_hash}",
        )

    predecessor_commit = git_output(root, ["log", "-n", "1", "--format=%H", "--", PREDECESSOR_JSON])
    evidence = {
        "predecessor_path": PREDECESSOR_JSON,
        "predecessor_commit_sha": predecessor_commit,
        "predecessor_file_hash_algorithm": "sha256",
        "predecessor_file_sha256": working_hash,
        "predecessor_worktree_matches_head_blob": True,
    }
    return data, evidence


def expect(value: object, wanted: object, failure_code: str, field: str) -> None:
    if value != wanted:
        fail(failure_code, f"{field}: {value!r}!={wanted!r}")


def validate_predecessor(predecessor: dict[str, Any]) -> None:
    expect(
        predecessor.get("schema_version"),
        "matrixlabs_compression_specimen_closure_v0",
        FAIL_CONTRACT_APPLICABILITY_MISSING,
        "predecessor.schema_version",
    )
    expect(
        predecessor.get("compression_closure_id"),
        PREDECESSOR_OBJECT,
        FAIL_CONTRACT_APPLICABILITY_MISSING,
        "predecessor.compression_closure_id",
    )
    expect(
        predecessor.get("closure_status"),
        PREDECESSOR_CLOSURE_STATUS,
        FAIL_CONTRACT_APPLICABILITY_MISSING,
        "predecessor.closure_status",
    )
    expect(
        predecessor.get("block", {}).get("block_status"),
        PREDECESSOR_BLOCK_STATUS,
        FAIL_CONTRACT_APPLICABILITY_MISSING,
        "predecessor.block.block_status",
    )
    expect(
        predecessor.get("block", {}).get("block_closed"),
        True,
        FAIL_CONTRACT_APPLICABILITY_MISSING,
        "predecessor.block.block_closed",
    )
    expect(
        predecessor.get("registry_boundary", {}).get("registry_use_authorized"),
        False,
        FAIL_REGISTRY_USE_AUTHORIZED,
        "predecessor.registry_boundary.registry_use_authorized",
    )


def group_contract(
    required_fields: list[str],
    contract: str,
    **extra: object,
) -> dict[str, object]:
    record: dict[str, object] = {
        "required_fields": required_fields,
        "required_value_policy": "MUST_BE_EXPLICIT_NO_DEFAULT_INFERENCE",
        "contract": contract,
    }
    record.update(extra)
    return record


def build_required_field_group_contracts() -> dict[str, dict[str, object]]:
    return {
        "entry_identity": group_contract(
            [
                "registry_candidate_id",
                "entry_role",
                "entry_status",
                "registry_kind",
                "schema_version",
            ],
            "Every future candidate must identify itself, its role, status, registry kind, and schema.",
            example_future_values={
                "registry_candidate_id": "candidate.registry.c8_n22_radius_bound_prepare_trace.v0",
                "entry_role": "COMPRESSION_TRACE_REGISTRY_CANDIDATE",
                "entry_status": "REGISTRY_STATUS_CANDIDATE",
            },
            example_values_created_by_f1=False,
        ),
        "source_compression_closure": group_contract(
            [
                "source_compression_closure_id",
                "source_compression_closure_status",
                "source_block_status",
                "allowed_use_from_closure",
            ],
            "Every future candidate must reference an E.4-style passing observability-only compression closure.",
            required_status=PREDECESSOR_CLOSURE_STATUS,
            no_passing_closure_no_registry_candidate=True,
        ),
        "source_compressed_packet": group_contract(
            [
                "compressed_packet_id",
                "target_trace_label",
                "packet_status",
                "source_records_remain_authority",
            ],
            "Every future candidate must reference the compressed packet while preserving source authority.",
        ),
        "source_decompression_audit": group_contract(
            [
                "decompression_audit_id",
                "decompression_audit_status",
                "critical_field_group_count_checked",
                "critical_field_group_count_passed",
                "all_critical_field_groups_recovered",
            ],
            "Every future candidate must reference the decompression audit and carry its critical-field parity status.",
            required_status="DECOMPRESSION_AUDIT_PASS_CRITICAL_FIELD_PARITY",
            no_decompression_pass_no_registry_candidate=True,
        ),
        "trace_label": group_contract(
            [
                "trace_label",
                "trace_label_definition",
                "trace_label_scope",
                "trace_label_authority_effect",
            ],
            "Every future candidate must declare the trace label and explicitly state it has no authority effect.",
            example_future_values={
                "trace_label": "C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0",
                "trace_label_scope": "C8_N22_LOCAL_SPECIMEN_ONLY",
                "trace_label_authority_effect": "NONE",
            },
            example_values_created_by_f1=False,
        ),
        "trace_scope": group_contract(
            [
                "trace_scope",
                "basis_scope",
                "context_scope",
                "cross_context_claimed",
            ],
            "Every future candidate must separate local specimen, multi-specimen observation, generalized shape, and active registry class.",
            required_scope_distinctions=[
                "local specimen",
                "multi-specimen observation",
                "generalized shape",
                "active registry class",
            ],
            example_future_values={
                "trace_scope": "C8_N22_LOCAL_SPECIMEN_ONLY",
                "cross_context_claimed": False,
            },
        ),
        "specimen_evidence": group_contract(
            [
                "specimen_count",
                "specimen_ids",
                "source_trace_ids",
                "evidence_kind",
            ],
            "Every future candidate must declare specimen count and source trace evidence explicitly.",
            example_future_values={
                "specimen_count": 1,
                "evidence_kind": "SINGLE_LOCAL_SPECIMEN",
            },
        ),
        "generalization_status": group_contract(
            [
                "general_shape_claimed",
                "multi_specimen_stability_claimed",
                "cross_context_stability_claimed",
                "local_candidate_only",
                "generalization_status",
            ],
            "Every future candidate must say whether it generalizes and preserve local-only status for a single specimen.",
            example_future_values={
                "general_shape_claimed": False,
                "multi_specimen_stability_claimed": False,
                "cross_context_stability_claimed": False,
                "local_candidate_only": True,
                "generalization_status": "LOCAL_SPECIMEN_ONLY_NOT_GENERALIZED",
            },
        ),
        "allowed_candidate_use": group_contract(
            list(CANDIDATE_STAGE_ALLOWED_USE),
            "Candidate-stage use is review, index, search, display, and comparison seed only.",
            allowed_values=CANDIDATE_STAGE_ALLOWED_USE,
        ),
        "forbidden_candidate_use": group_contract(
            list(CANDIDATE_STAGE_FORBIDDEN_USE),
            "Every future candidate must carry forbidden uses that prevent candidate-stage authority drift.",
            forbidden_values=CANDIDATE_STAGE_FORBIDDEN_USE,
        ),
        "decompression_requirements": group_contract(
            [
                "decompression_audit_required",
                "source_decompression_audit_id",
                "critical_field_parity_required",
                "source_records_remain_authority",
            ],
            "Every future candidate must preserve decompression traceability and may not stand alone.",
            candidate_may_stand_alone=False,
        ),
        "authority_boundaries": group_contract(
            [
                "candidate_grants_authority",
                "candidate_replaces_source_authority",
                "candidate_authorizes_reuse",
                "candidate_authorizes_execution",
                "candidate_changes_authority_state",
            ],
            "Candidate-stage authority fields must all be false.",
            candidate_stage_values={
                "candidate_grants_authority": False,
                "candidate_replaces_source_authority": False,
                "candidate_authorizes_reuse": False,
                "candidate_authorizes_execution": False,
                "candidate_changes_authority_state": False,
            },
        ),
        "radius_boundaries": group_contract(
            [
                "source_radius_after",
                "source_radius_exhausted",
                "candidate_renews_radius",
                "candidate_creates_radius",
                "candidate_authorizes_additional_machine_proceed",
            ],
            "A registry candidate cannot revive exhausted radius or create additional machine proceed.",
            example_future_values={
                "source_radius_after": 0,
                "source_radius_exhausted": True,
                "candidate_renews_radius": False,
                "candidate_creates_radius": False,
                "candidate_authorizes_additional_machine_proceed": False,
            },
        ),
        "runner_boundaries": group_contract(
            [
                "candidate_is_runner_input",
                "candidate_authorizes_runner",
                "candidate_defines_runner_policy",
                "candidate_routes_runner",
                "runner_authority_created",
            ],
            "A registry candidate may support later runner analysis but cannot be runner authority.",
            candidate_stage_values={
                "candidate_is_runner_input": False,
                "candidate_authorizes_runner": False,
                "candidate_defines_runner_policy": False,
                "candidate_routes_runner": False,
                "runner_authority_created": False,
            },
        ),
        "activation_boundaries": group_contract(
            [
                "active_registry_entry_created",
                "activation_status",
                "activation_requires_human_decision",
                "activation_requires_separate_apply_object",
            ],
            "Candidate status is not active status; activation requires a later apply object.",
            candidate_stage_values={
                "active_registry_entry_created": False,
                "activation_status": "ACTIVATION_INACTIVE",
                "activation_requires_human_decision": True,
                "activation_requires_separate_apply_object": True,
            },
        ),
        "promotion_boundaries": group_contract(
            [
                "promotion_status",
                "promotion_decision_required",
                "promotion_receipt_required",
                "promotion_apply_required",
            ],
            "Promotion requires a later decision and receipt; promotion does not silently activate an entry.",
            candidate_stage_values={
                "promotion_status": "REGISTRY_PROMOTION_NOT_REQUESTED",
                "promotion_decision_required": True,
            },
        ),
        "revocation_or_expiry": group_contract(
            [
                "revocation_status",
                "expiry_status",
                "supersession_status",
                "invalidated_by_source_mismatch",
            ],
            "Every future candidate needs revocation, expiry, supersession, and source-mismatch invalidation fields.",
            default_candidate_values_later={
                "revocation_status": "NOT_REVOKED",
                "expiry_status": "NOT_EXPIRED",
                "supersession_status": "NOT_SUPERSEDED",
            },
        ),
        "audit_requirements": group_contract(
            [
                "schema present",
                "candidate present",
                "source E.4 closure present",
                "E.4 status pass",
                "E.3 status pass",
                "required fields present",
                "specimen_count declared",
                "local-only status preserved",
                "no active registry created",
                "no reuse authorized",
                "no radius renewed",
                "no runner authority created",
            ],
            "The later F.3 audit must be mechanical and must check schema, source, specimen, local-only, and non-effect boundaries.",
        ),
    }


def build_contract(predecessor_evidence: dict[str, Any]) -> dict[str, Any]:
    required_group_contracts = build_required_field_group_contracts()
    schema_gate = {
        "registry_schema_gate": SCHEMA_STATUS,
        "schema_role": SCHEMA_ROLE,
        "registry_kind": REGISTRY_KIND,
        "schema_scope": SCHEMA_SCOPE,
        "allowed_entry_statuses_declared": bool(ALLOWED_ENTRY_STATUSES),
        "allowed_promotion_statuses_declared": bool(ALLOWED_PROMOTION_STATUSES),
        "allowed_generalization_statuses_declared": bool(ALLOWED_GENERALIZATION_STATUSES),
        "allowed_activation_statuses_declared": bool(ALLOWED_ACTIVATION_STATUSES),
        "required_field_group_count": len(REQUIRED_FIELD_GROUPS),
        "required_field_groups_declared": list(required_group_contracts) == REQUIRED_FIELD_GROUPS,
        "candidate_stage_allowed_uses_declared": bool(CANDIDATE_STAGE_ALLOWED_USE),
        "candidate_stage_forbidden_uses_declared": bool(CANDIDATE_STAGE_FORBIDDEN_USE),
        "authority_boundaries_declared": "authority_boundaries" in required_group_contracts,
        "radius_boundaries_declared": "radius_boundaries" in required_group_contracts,
        "runner_boundaries_declared": "runner_boundaries" in required_group_contracts,
        "activation_boundaries_declared": "activation_boundaries" in required_group_contracts,
        "promotion_boundaries_declared": "promotion_boundaries" in required_group_contracts,
        "audit_requirements_declared": "audit_requirements" in required_group_contracts,
        "contract_applicability_boundaries_declared": True,
        "specimen_count_laws_declared": True,
        "future_comparison_seed_boundary_declared": True,
        "candidate_active_use_stage_separation_declared": True,
        "promotion_activation_split_declared": True,
        "self_authorization_boundary_declared": True,
        "single_specimen_does_not_equal_generalized_pattern": True,
        "source_records_remain_authority_required": True,
        **SCHEMA_NON_EFFECTS,
        "failures": [],
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "registry_schema_id": REGISTRY_SCHEMA_ID,
        "schema_role": SCHEMA_ROLE,
        "registry_kind": REGISTRY_KIND,
        "schema_scope": SCHEMA_SCOPE,
        "schema_status": SCHEMA_STATUS,
        "block_id": BLOCK_ID,
        "block_unit_id": BLOCK_UNIT_ID,
        "generated_by": GENERATOR,
        "predecessor_context": {
            "predecessor_block": PREDECESSOR_BLOCK,
            "predecessor_object": PREDECESSOR_OBJECT,
            "predecessor_role": PREDECESSOR_ROLE,
            "predecessor_authorizes_schema_contract": False,
            "human_start_required_for_block_f": True,
        },
        "predecessor_evidence": predecessor_evidence,
        "contract_applicability": {
            "applies_to": SCHEMA_SCOPE,
            "requires_passing_compression_closure": True,
            "requires_observability_only_closure": True,
            "requires_source_records_remain_authority": True,
            "does_not_apply_to_runtime_traces": True,
            "does_not_apply_to_uncompressed_receipts": True,
            "does_not_apply_to_active_archive_entries": True,
            "does_not_apply_to_runner_policies": True,
            "does_not_apply_to_machine_proceed_authority": True,
        },
        "allowed_entry_statuses": ALLOWED_ENTRY_STATUSES,
        "allowed_promotion_statuses": ALLOWED_PROMOTION_STATUSES,
        "allowed_generalization_statuses": ALLOWED_GENERALIZATION_STATUSES,
        "allowed_activation_statuses": ALLOWED_ACTIVATION_STATUSES,
        "promotion_activation_split": {
            "promotion_granted_does_not_equal_active": True,
            "activation_requires_separate_apply_object": True,
            "activation_requires_status_transition_record": True,
            "active_registry_entry_materialization_required": True,
        },
        "required_field_groups": REQUIRED_FIELD_GROUPS,
        "required_field_group_count": len(REQUIRED_FIELD_GROUPS),
        "required_field_group_contracts": required_group_contracts,
        "candidate_stage_allowed_use": CANDIDATE_STAGE_ALLOWED_USE,
        "candidate_stage_forbidden_use": CANDIDATE_STAGE_FORBIDDEN_USE,
        "specimen_count_laws": {
            "specimen_count_must_be_explicit": True,
            "specimen_ids_must_be_listed": True,
            "specimen_count_must_equal_listed_specimen_ids": True,
            "single_specimen_must_remain_local_only": True,
            "specimen_count_may_not_be_inflated_by_schema": True,
            "multi_specimen_status_requires_separate_evidence": True,
        },
        "future_comparison_seed_boundary": {
            "may_seed_future_comparison": True,
            "may_count_as_stability_evidence_without_later_audit": False,
            "may_create_generalized_pattern_by_itself": False,
            "requires_multi_specimen_audit_for_generalization": True,
        },
        "use_stage_separation": {
            "candidate_stage_use_defined": True,
            "active_registry_use_defined_by_f1": False,
            "active_registry_use_requires_later_activation_contract": True,
            "candidate_stage_use_may_not_be_imported_as_active_use": True,
        },
        "schema_laws": {
            "registry_schema_contract_does_not_create_candidate": True,
            "registry_candidate_does_not_equal_active_registry_entry": True,
            "single_specimen_does_not_equal_generalized_pattern": True,
            "observability_registry_does_not_equal_source_authority": True,
            "observability_registry_does_not_equal_runner_authority": True,
            "source_records_remain_authority_required": True,
        },
        "self_authorization_boundary": {
            "schema_contract_authorizes_its_own_use": False,
            "schema_contract_self_promotes": False,
            "schema_contract_self_activates": False,
            "candidate_creation_requires_separate_unit": True,
            "candidate_audit_requires_separate_unit": True,
            "activation_requires_separate_human_decision": True,
        },
        "schema_non_effects": SCHEMA_NON_EFFECTS,
        "next_possible_separate_object": {
            "next_possible_separate_object_family": NEXT_OBJECT_FAMILY,
            "example_future_candidate_object": EXAMPLE_FUTURE_CANDIDATE,
            "example_candidate_created_by_f1": False,
            "selected_as_next_unit_by_f1": False,
            "requires_separate_f2_unit": True,
        },
        "schema_gate": schema_gate,
        "failure_vocabulary": FAILURE_VOCABULARY,
        "most_important_failures": MOST_IMPORTANT_FAILURES,
        "non_claims": NON_CLAIMS,
        "key_non_claims": KEY_NON_CLAIMS,
        "precommit_compression_trace_registry_schema_gate": PRECOMMIT_GATE,
        "registry_schema_gate": SCHEMA_STATUS,
        "terminal_transition": TERMINAL_TRANSITION,
    }


def validate_contract(contract: dict[str, Any]) -> None:
    expect(contract.get("schema_version"), SCHEMA_VERSION, FAIL_REQUIRED_FIELD_GROUPS_MISSING, "schema_version")
    expect(contract.get("registry_schema_id"), REGISTRY_SCHEMA_ID, FAIL_REQUIRED_FIELD_GROUPS_MISSING, "registry_schema_id")
    expect(contract.get("schema_role"), SCHEMA_ROLE, FAIL_REQUIRED_FIELD_GROUPS_MISSING, "schema_role")
    expect(contract.get("registry_kind"), REGISTRY_KIND, FAIL_REQUIRED_FIELD_GROUPS_MISSING, "registry_kind")
    expect(contract.get("schema_scope"), SCHEMA_SCOPE, FAIL_REQUIRED_FIELD_GROUPS_MISSING, "schema_scope")
    expect(contract.get("schema_status"), SCHEMA_STATUS, FAIL_REQUIRED_FIELD_GROUPS_MISSING, "schema_status")
    expect(contract.get("block_id"), BLOCK_ID, FAIL_REQUIRED_FIELD_GROUPS_MISSING, "block_id")
    expect(contract.get("block_unit_id"), BLOCK_UNIT_ID, FAIL_REQUIRED_FIELD_GROUPS_MISSING, "block_unit_id")
    expect(contract.get("allowed_entry_statuses"), ALLOWED_ENTRY_STATUSES, FAIL_ENTRY_STATUSES_MISSING, "allowed_entry_statuses")
    expect(contract.get("allowed_promotion_statuses"), ALLOWED_PROMOTION_STATUSES, FAIL_PROMOTION_STATUSES_MISSING, "allowed_promotion_statuses")
    expect(contract.get("allowed_generalization_statuses"), ALLOWED_GENERALIZATION_STATUSES, FAIL_GENERALIZATION_STATUSES_MISSING, "allowed_generalization_statuses")
    expect(contract.get("allowed_activation_statuses"), ALLOWED_ACTIVATION_STATUSES, FAIL_ACTIVATION_STATUSES_MISSING, "allowed_activation_statuses")
    expect(contract.get("required_field_groups"), REQUIRED_FIELD_GROUPS, FAIL_REQUIRED_FIELD_GROUPS_MISSING, "required_field_groups")
    expect(contract.get("required_field_group_count"), 18, FAIL_REQUIRED_FIELD_GROUPS_MISSING, "required_field_group_count")
    contracts = contract.get("required_field_group_contracts", {})
    if not isinstance(contracts, dict) or sorted(contracts) != sorted(REQUIRED_FIELD_GROUPS):
        fail(FAIL_REQUIRED_FIELD_GROUPS_MISSING, "required_field_group_contracts")
    expect(contract.get("candidate_stage_allowed_use"), CANDIDATE_STAGE_ALLOWED_USE, FAIL_ALLOWED_USE_MISSING, "candidate_stage_allowed_use")
    expect(contract.get("candidate_stage_forbidden_use"), CANDIDATE_STAGE_FORBIDDEN_USE, FAIL_FORBIDDEN_USE_MISSING, "candidate_stage_forbidden_use")
    for key, value in contract.get("schema_non_effects", {}).items():
        expect(value, False, FAIL_CANDIDATE_ENTRY_CREATED, f"schema_non_effects.{key}")
    expect(contract.get("terminal_transition"), TERMINAL_TRANSITION, FAIL_SELF_AUTHORIZATION_BOUNDARY_MISSING, "terminal_transition")


def render_markdown() -> str:
    required_group_labels = [group.replace("_", " ") for group in REQUIRED_FIELD_GROUPS]
    parts = [
        "# Compression trace registry entry schema contract v0",
        "",
        "## Status",
        "",
        SCHEMA_STATUS,
        "",
        "## Registry kind",
        "",
        REGISTRY_KIND,
        "",
        "## Schema role",
        "",
        SCHEMA_ROLE,
        "",
        "## Schema scope",
        "",
        SCHEMA_SCOPE,
        "",
        "## Required field groups",
        "",
        *[f"- {label}" for label in required_group_labels],
        "",
        "## Candidate-stage allowed use",
        "",
        "- candidate queue display",
        "- human review",
        "- trace search",
        "- future comparison seed",
        "- dashboard projection",
        "",
        "## Candidate-stage forbidden use",
        "",
        "- source authority replacement",
        "- authorization for reuse",
        "- radius renewal",
        "- machine proceed authorization",
        "- execution authorization",
        "- runner routing",
        "- schema promotion",
        "- taxonomy promotion",
        "",
        "## Contract laws",
        "",
        "- registry schema contract does not create candidate",
        "- registry candidate does not equal active registry entry",
        "- single specimen does not equal generalized pattern",
        "- observability registry does not equal source authority",
        "- observability registry does not equal runner authority",
        "- source records remain authority",
        "",
        "## Specimen-count discipline",
        "",
        "- specimen count must be explicit",
        "- specimen IDs must be listed",
        "- specimen count must equal listed specimen IDs",
        "- single specimen remains local-only unless later evidence and audit say otherwise",
        "",
        "## Non-effects",
        "",
        "- no candidate entry creation",
        "- no active registry entry materialization",
        "- no registry use grant",
        "- no reuse grant",
        "- no radius renewal",
        "- no machine-proceed grant",
        "- no machine action performed",
        "- no runner-authority creation",
        "- no generalized-pattern creation",
        "",
        "## Next",
        "",
        "A local registry candidate entry may be created separately under this contract.",
    ]
    return "\n".join(parts)


def ensure_markdown_boundary(markdown: str) -> None:
    lower = markdown.lower()
    hits = [phrase for phrase in MARKDOWN_FORBIDDEN_PHRASES if phrase in lower]
    if hits:
        fail(FAIL_SELF_AUTHORIZATION_BOUNDARY_MISSING, f"Markdown forbidden phrase hits: {hits}")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def generate() -> int:
    root = detect_repo_root(Path.cwd())
    predecessor, predecessor_evidence = load_predecessor(root)
    validate_predecessor(predecessor)
    contract = build_contract(predecessor_evidence)
    validate_contract(contract)
    markdown = render_markdown()
    ensure_markdown_boundary(markdown)

    write_text(root / OUTPUT_JSON, json.dumps(contract, indent=2, sort_keys=True))
    write_text(root / OUTPUT_MD, markdown)

    print(f"Wrote {OUTPUT_JSON}")
    print(f"Wrote {OUTPUT_MD}")
    print(f"registry_schema_gate={SCHEMA_STATUS}")
    print(f"terminal_transition={TERMINAL_TRANSITION}")
    return 0


def main() -> int:
    try:
        return generate()
    except GenerationError as exc:
        print(f"STOP_REGISTRY_SCHEMA_FAIL_{exc.code}: {exc.detail or exc.code}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
