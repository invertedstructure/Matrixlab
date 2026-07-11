#!/usr/bin/env python3
"""Build POST-VS1 direction decision receipt v0."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


EXPECTED_BRANCH = "master"
EXPECTED_HEAD = "975d05dfda23a632c91faeaae66abbfcf4e85da6"

SCHEMA_VERSION = "matrixlabs_post_vs1_direction_decision_receipt_v0"
ARTIFACT_ID = "post_vs1_direction_decision_receipt_v0"
OBJECT_ID = "POST_VS1_DIRECTION_DECISION_RECEIPT"
OBJECT_ROLE = "HUMAN_DIRECTION_DECISION_RECEIPT_ONLY"
RECEIPT_STATUS = "HUMAN_ACCEPTANCE_RECORDED_PENDING_AUTHORITY_UPDATE"
RECEIPT_GATE = "POST_VS1_DIRECTION_DECISION_RECEIPT_PASS_ACCEPT_EXACT_SCOPE_RECORDED"
TERMINAL_TRANSITION = "ADVANCE(POST_VS1_DIRECTION_AUTHORITY_UPDATE_V0_PENDING)"
PRE_REPAIR_DECISION_RECEIPT_SHA256 = (
    "de8a3130cd7f61096464b12bb3346ec82e6c81530a46b7ba38b67d79f36fe85d"
)

SOURCE_SURFACE_PATH = "docs/matrixlabs/post_vs1/post_vs1_direction_decision_surface_v0.json"
SOURCE_SURFACE_MD_PATH = "docs/matrixlabs/post_vs1/post_vs1_direction_decision_surface_v0.md"
PROPOSAL_SOURCE_PATH = (
    "docs/matrixlabs/post_vs1/sources/"
    "matrixlab_first_sweep_capable_kernel_target_specification_v0.md"
)
PROPOSAL_SOURCE_SIDECAR_PATH = (
    "docs/matrixlabs/post_vs1/sources/"
    "matrixlab_first_sweep_capable_kernel_target_specification_v0.source.json"
)
VS1_CLOSURE_PATH = "docs/matrixlabs/phase_vs1/phase_vs1_closure_v0.json"
VS1_MAP_PATH = "docs/matrixlabs/phase_vs1/phase_vs1_missing_precondition_next_surface_map_v0.json"

OUTPUT_JSON = "docs/matrixlabs/post_vs1/post_vs1_direction_decision_receipt_v0.json"
OUTPUT_MD = "docs/matrixlabs/post_vs1/post_vs1_direction_decision_receipt_v0.md"

SOURCE_SURFACE_SCHEMA = "matrixlabs_post_vs1_direction_decision_surface_v0"
SOURCE_SURFACE_ARTIFACT_ID = "post_vs1_direction_decision_surface_v0"
SOURCE_SURFACE_OBJECT_ID = "POST_VS1_DIRECTION_DECISION_SURFACE"
SOURCE_SURFACE_OBJECT_ROLE = "HUMAN_DIRECTION_DECISION_SURFACE_ONLY"
SOURCE_SURFACE_GATE = "POST_VS1_DIRECTION_DECISION_SURFACE_PASS_READY_FOR_HUMAN_DECISION"
SOURCE_SURFACE_TERMINAL = "STOP_POST_VS1_DIRECTION_SURFACE_READY_PENDING_HUMAN_DECISION"
SOURCE_SURFACE_STATUS = "PREPARED_PENDING_HUMAN_DECISION"
SOURCE_DECISION_PACKAGE_SHA256 = (
    "e9e4143ad2efdd285fe9e598e50d965d82057f7a8d6ccc4c52478a596d6b788b"
)

CANONICALIZATION_CONTRACT = "MATRIXLAB_CANONICAL_JSON_V0"
SOURCE_BOUND_SECTIONS = [
    "proposal_source_binding",
    "proposal_overbreadth_normalization",
    "proposal_bundle",
    "proposal_bundle_membership_contract",
    "proposal_bundle_traceability",
    "vs1_5_advisory_alignment",
    "decision_question",
    "recommended_direction",
    "decision_options",
    "decision_option_payload_contracts",
    "proposed_approval_scope",
    "excluded_authority_scope",
    "alternative_scope_non_inheritance",
    "downstream_branch_map",
]
RECEIPT_BOUND_SECTIONS = [
    "source_surface_binding",
    "source_decision_package_binding",
    "human_decision_evidence",
    "decision_selection",
    "approval_vector",
    "approved_scope",
    "excluded_authority_scope",
    "revision_state",
    "decision_state_after_receipt",
    "authority_effects",
    "downstream_authority_update_requirement",
    "downstream_transition_closure_requirement",
]

ACCEPTED_OPTION = "ACCEPT_FIRST_SWEEP_CAPABLE_KERNEL_DIRECTION_AND_PROPOSED_SCOPE"
DECISION_BRANCH = "ACCEPT_EXACT_PROPOSED_SCOPE"
DECISION_STATEMENT = "accepted, proceed"
DECISION_STATEMENT_NORMALIZED = ACCEPTED_OPTION
DECISION_DATE_LOCAL = "2026-07-11"
DECISION_TIMEZONE = "Europe/Lisbon"
DECISION_SEQUENCE_ANCHOR = "AFTER_COMMIT_975D05DFDA23A632C91FAEAAE66ABBFCF4E85DA6"

DIRECTION_ID = "FIRST_SWEEP_CAPABLE_KERNEL_V0"
TARGET_FAMILY = "BOUNDED_CONTRACT_CONVERGENCE"
FIRST_TARGET = "TYPED_STATE_CONTRACT_CONVERGENCE_V0"
BUNDLE_ID = "POST_VS1_FIRST_SWEEP_CAPABLE_KERNEL_BUNDLE_V0"

EXPECTED_APPROVAL_VECTOR = {
    "direction_selected": True,
    "target_family_selected": True,
    "first_target_selected": True,
    "definition_scope_approved": True,
    "bounded_construction_scope_approved": True,
    "construction_verification_scope_approved": True,
    "execution_scope_approved": False,
    "positive_path_execution_scope_approved": False,
    "negative_path_execution_scope_approved": False,
    "sweep_scope_approved": False,
    "automatic_rerun_scope_approved": False,
    "runner_scope_approved": False,
    "reusable_schema_scope_approved": False,
    "reusable_move_scope_approved": False,
    "second_target_scope_approved": False,
    "portability_scope_approved": False,
}

REQUIRED_MAXIMUM_SCOPE_PROPERTIES = [
    "target-bound",
    "phase-bound",
    "bundle-bound",
    "definition-bound",
    "construction-bound",
    "construction-verification-bound",
    "non-execution",
    "non-reusable",
    "non-generalizing",
    "single-target",
    "non-portability",
]

REQUIRED_EXCLUSIONS = [
    "kernel execution",
    "positive-path execution",
    "negative-path execution",
    "perturbation sweep execution",
    "automatic rerun",
    "automatic radius renewal",
    "radius expansion",
    "move-budget expansion",
    "case-budget expansion",
    "target-family expansion",
    "second-target selection",
    "first-target substitution",
    "portability testing",
    "automatic source acquisition",
    "automatic schema invention",
    "automatic capability creation",
    "automatic authority escalation",
    "automatic repair",
    "automatic local revision",
    "refinement application",
    "candidate promotion",
    "reusable schema approval",
    "reusable move-space approval",
    "active registry creation",
    "runner authority",
    "autonomous continuation",
    "cross-domain generalization",
    "performance optimization",
    "scale optimization",
]

RECEIPT_CHECKS = [
    "POST_VS1_DECISION_RECEIPT_SOURCE_SURFACE_VERIFIED",
    "POST_VS1_DECISION_RECEIPT_SOURCE_PACKAGE_HASH_VERIFIED",
    "POST_VS1_DECISION_RECEIPT_EXPLICIT_HUMAN_ACCEPTANCE_VERIFIED",
    "POST_VS1_DECISION_RECEIPT_OPTION_A_PRESENT",
    "POST_VS1_DECISION_RECEIPT_OPTION_A_APPROVAL_VECTOR_EXACT",
    "POST_VS1_DECISION_RECEIPT_APPROVED_SCOPE_BOUND_TO_SURFACE",
    "POST_VS1_DECISION_RECEIPT_EXCLUDED_SCOPE_PRESERVED",
    "POST_VS1_DECISION_RECEIPT_NO_REVISIONS_PASS",
    "POST_VS1_DECISION_RECEIPT_SINGLE_TARGET_BOUNDARY_PASS",
    "POST_VS1_DECISION_RECEIPT_NON_PORTABILITY_BOUNDARY_PASS",
    "POST_VS1_DECISION_RECEIPT_AUTHORITY_NOT_MUTATED",
    "POST_VS1_DECISION_RECEIPT_EXECUTION_AUTHORITY_ABSENT",
    "POST_VS1_DECISION_RECEIPT_SWEEP_AUTHORITY_ABSENT",
    "POST_VS1_DECISION_RECEIPT_RUNNER_AUTHORITY_ABSENT",
    "POST_VS1_DECISION_RECEIPT_CANONICAL_BINDING_PASS",
    "POST_VS1_DECISION_RECEIPT_DECISION_MODE_CANONICAL_PATH_PASS",
    "POST_VS1_DECISION_RECEIPT_DECISION_MODE_ALIAS_CONSISTENCY_PASS",
    "POST_VS1_DECISION_RECEIPT_APPROVED_SCOPE_ELIGIBILITY_CANONICAL_PATH_PASS",
    "POST_VS1_DECISION_RECEIPT_APPROVED_SCOPE_ELIGIBILITY_ALIAS_CONSISTENCY_PASS",
    "POST_VS1_DECISION_RECEIPT_APPROVED_SCOPE_APPLICATION_CANONICAL_PATH_PASS",
    "POST_VS1_DECISION_RECEIPT_APPROVED_SCOPE_APPLICATION_ALIAS_CONSISTENCY_PASS",
    "POST_VS1_DECISION_RECEIPT_DECLARED_SERIALIZATION_REHASH_PASS",
]

FORBIDDEN_ARTIFACTS = [
    "docs/matrixlabs/post_vs1/post_vs1_direction_authority_update_v0.json",
    "docs/matrixlabs/post_vs1/post_vs1_direction_authority_update_v0.md",
    "docs/matrixlabs/post_vs1/post_vs1_direction_transition_closure_v0.json",
    "docs/matrixlabs/post_vs1/post_vs1_direction_transition_closure_v0.md",
    "docs/matrixlabs/phase_vs2",
    "docs/matrixlabs/runner",
    "docs/matrixlabs/runtime",
    "docs/matrixlabs/move_space",
    "docs/matrixlabs/micro_sweeps",
]

PRESERVED_SOURCE_PATHS = [
    SOURCE_SURFACE_PATH,
    SOURCE_SURFACE_MD_PATH,
    PROPOSAL_SOURCE_PATH,
    PROPOSAL_SOURCE_SIDECAR_PATH,
    VS1_CLOSURE_PATH,
    VS1_MAP_PATH,
]


class ReceiptFailure(RuntimeError):
    def __init__(
        self,
        code: str,
        *,
        field: str = "NONE",
        expected: object = "NONE",
        actual: object = "NONE",
    ) -> None:
        super().__init__(code)
        self.code = code
        self.field = field
        self.expected = expected
        self.actual = actual


def fail(
    code: str,
    *,
    field: str = "NONE",
    expected: object = "NONE",
    actual: object = "NONE",
) -> None:
    raise ReceiptFailure(code, field=field, expected=expected, actual=actual)


def run_git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def detect_repo_root(start: Path) -> Path:
    try:
        return Path(run_git(start, "rev-parse", "--show-toplevel"))
    except subprocess.CalledProcessError:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_UNEXPECTED_HEAD",
            field="repo",
            expected="/home/asd/projects/matrixlab",
            actual=str(start),
        )


def require_repo_context(root: Path) -> None:
    branch = run_git(root, "branch", "--show-current")
    head = run_git(root, "rev-parse", "HEAD")
    if branch != EXPECTED_BRANCH:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_UNEXPECTED_HEAD",
            field="branch",
            expected=EXPECTED_BRANCH,
            actual=branch,
        )
    if head != EXPECTED_HEAD:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_UNEXPECTED_HEAD",
            field="HEAD",
            expected=EXPECTED_HEAD,
            actual=head,
        )


def validate_dirty_scope(root: Path) -> None:
    allowed_prefixes = (
        " M baseline_share/COMMIT_CONTEXT.md",
        " M baseline_share/CURRENT_STATE.md",
        " M baseline_share/MANIFEST.json",
        " M baseline_share/RECEIPT_POINTERS.md",
        " M scripts/build_baseline_share_v0.py",
        "?? scripts/build_post_vs1_direction_decision_receipt_v0.py",
        f"?? {OUTPUT_JSON}",
        f"?? {OUTPUT_MD}",
        "?? discussion_packets/",
    )
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=root,
        text=True,
    ).splitlines()
    unexpected = [line for line in status if not line.startswith(allowed_prefixes)]
    if unexpected:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_DOWNSTREAM_ARTIFACT_CREATED",
            field="git_status",
            expected=list(allowed_prefixes),
            actual=unexpected,
        )


def ensure_no_forbidden_artifacts(root: Path) -> None:
    present = [path for path in FORBIDDEN_ARTIFACTS if (root / path).exists()]
    if present:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_DOWNSTREAM_ARTIFACT_CREATED",
            field="forbidden_artifacts",
            expected=[],
            actual=present,
        )


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(root: Path, rel_path: str) -> str:
    return sha256_bytes((root / rel_path).read_bytes())


def canonical_hash(payload: dict[str, Any]) -> str:
    return sha256_bytes(
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    )


def load_json(root: Path, rel_path: str) -> dict[str, Any]:
    path = root / rel_path
    if not path.exists():
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_SOURCE_SURFACE_MISSING",
            field=rel_path,
            expected="present",
            actual="missing",
        )
    return json.loads(path.read_text(encoding="utf-8"))


def capture_source_hashes(root: Path) -> dict[str, str]:
    return {path: sha256_file(root, path) for path in PRESERVED_SOURCE_PATHS}


def validate_source_preservation(before: dict[str, str], after: dict[str, str]) -> None:
    changed = {
        path: {"before": before[path], "after": after.get(path)}
        for path in before
        if before[path] != after.get(path)
    }
    if changed:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_SOURCE_SURFACE_HASH_MISMATCH",
            field="source_hashes",
            expected=before,
            actual=changed,
        )


def validate_source_surface(surface: dict[str, Any]) -> None:
    expected_values = {
        "schema_version": SOURCE_SURFACE_SCHEMA,
        "artifact_id": SOURCE_SURFACE_ARTIFACT_ID,
        "object_id": SOURCE_SURFACE_OBJECT_ID,
        "object_role": SOURCE_SURFACE_OBJECT_ROLE,
        "surface_gate": SOURCE_SURFACE_GATE,
        "surface_status": SOURCE_SURFACE_STATUS,
    }
    for field, expected in expected_values.items():
        if surface.get(field) != expected:
            fail(
                "STOP_POST_VS1_DECISION_RECEIPT_SURFACE_GATE_MISMATCH",
                field=field,
                expected=expected,
                actual=surface.get(field),
            )
    if surface.get("terminal_transition", {}).get("transition") != SOURCE_SURFACE_TERMINAL:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_SURFACE_GATE_MISMATCH",
            field="terminal_transition.transition",
            expected=SOURCE_SURFACE_TERMINAL,
            actual=surface.get("terminal_transition", {}).get("transition"),
        )
    state = surface.get("decision_state", {})
    pending_fields = {
        "human_decision_recorded": False,
        "decision_receipt_created": False,
        "authority_update_applied": False,
        "authority_transition_closed": False,
        "vs2_started": False,
    }
    for field, expected in pending_fields.items():
        if state.get(field) is not expected:
            fail(
                "STOP_POST_VS1_DECISION_RECEIPT_SURFACE_NOT_PENDING_DECISION",
                field=f"decision_state.{field}",
                expected=expected,
                actual=state.get(field),
            )


def validate_source_package(surface: dict[str, Any]) -> None:
    binding = surface.get("decision_package_binding", {})
    if not binding.get("decision_package_sha256"):
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_PACKAGE_HASH_MISSING",
            field="decision_package_binding.decision_package_sha256",
            expected=SOURCE_DECISION_PACKAGE_SHA256,
            actual=None,
        )
    payload = binding.get("decision_package_payload", {})
    recomputed = canonical_hash(payload)
    if binding.get("decision_package_sha256") != SOURCE_DECISION_PACKAGE_SHA256:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_PACKAGE_HASH_MISMATCH",
            field="decision_package_binding.decision_package_sha256",
            expected=SOURCE_DECISION_PACKAGE_SHA256,
            actual=binding.get("decision_package_sha256"),
        )
    if recomputed != SOURCE_DECISION_PACKAGE_SHA256:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_PACKAGE_HASH_MISMATCH",
            field="decision_package_binding.decision_package_payload",
            expected=SOURCE_DECISION_PACKAGE_SHA256,
            actual=recomputed,
        )
    if binding.get("canonicalization") != CANONICALIZATION_CONTRACT:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_BOUND_SECTION_MANIFEST_MISMATCH",
            field="decision_package_binding.canonicalization",
            expected=CANONICALIZATION_CONTRACT,
            actual=binding.get("canonicalization"),
        )
    if binding.get("canonicalization_contract") != CANONICALIZATION_CONTRACT:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_BOUND_SECTION_MANIFEST_MISMATCH",
            field="decision_package_binding.canonicalization_contract",
            expected=CANONICALIZATION_CONTRACT,
            actual=binding.get("canonicalization_contract"),
        )
    if binding.get("bound_sections") != SOURCE_BOUND_SECTIONS:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_BOUND_SECTION_MANIFEST_MISMATCH",
            field="decision_package_binding.bound_sections",
            expected=SOURCE_BOUND_SECTIONS,
            actual=binding.get("bound_sections"),
        )
    if list(payload.keys()) != SOURCE_BOUND_SECTIONS:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_BOUND_SECTION_MANIFEST_MISMATCH",
            field="decision_package_binding.decision_package_payload",
            expected=SOURCE_BOUND_SECTIONS,
            actual=list(payload.keys()),
        )


def validate_option_a(surface: dict[str, Any]) -> dict[str, Any]:
    contracts = surface.get("decision_option_payload_contracts", {})
    option_contract = contracts.get(ACCEPTED_OPTION)
    if not option_contract:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_ACCEPTED_OPTION_MISSING",
            field=f"decision_option_payload_contracts.{ACCEPTED_OPTION}",
            expected="present",
            actual=None,
        )
    approval_vector = option_contract.get("required_approval_vector")
    if approval_vector != EXPECTED_APPROVAL_VECTOR:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_APPROVAL_VECTOR_MISMATCH",
            field="required_approval_vector",
            expected=EXPECTED_APPROVAL_VECTOR,
            actual=approval_vector,
        )
    if option_contract.get("option_a_requires_explicit_scope_vector") is not True:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_APPROVAL_VECTOR_MISMATCH",
            field="option_a_requires_explicit_scope_vector",
            expected=True,
            actual=option_contract.get("option_a_requires_explicit_scope_vector"),
        )
    if option_contract.get("option_token_alone_is_not_a_complete_decision_receipt") is not True:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_APPROVAL_VECTOR_MISMATCH",
            field="option_token_alone_is_not_a_complete_decision_receipt",
            expected=True,
            actual=option_contract.get("option_token_alone_is_not_a_complete_decision_receipt"),
        )
    return approval_vector


def approved_scope_from_surface(surface: dict[str, Any]) -> dict[str, Any]:
    proposed = surface.get("proposed_approval_scope", {})
    approved = {
        "direction_selection_scope": proposed.get("direction_selection_scope"),
        "definition_scope": proposed.get("definition_scope"),
        "bounded_construction_scope": proposed.get("bounded_construction_scope"),
        "construction_verification_scope": proposed.get("construction_verification_scope"),
        "maximum_scope": proposed.get("maximum_scope"),
        "approved_scope_eligible_for_authority_update": True,
        "approved_scope_applied_to_authority_state": False,
    }
    for key in [
        "direction_selection_scope",
        "definition_scope",
        "bounded_construction_scope",
        "construction_verification_scope",
        "maximum_scope",
    ]:
        value = approved[key]
        if value != proposed.get(key):
            fail(
                "STOP_POST_VS1_DECISION_RECEIPT_APPROVED_SCOPE_MISMATCH",
                field=f"approved_scope.{key}",
                expected=proposed.get(key),
                actual=value,
            )
    missing = [
        value
        for value in REQUIRED_MAXIMUM_SCOPE_PROPERTIES
        if value not in (approved.get("maximum_scope") or [])
    ]
    if missing:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_APPROVED_SCOPE_MISMATCH",
            field="approved_scope.maximum_scope",
            expected=REQUIRED_MAXIMUM_SCOPE_PROPERTIES,
            actual=approved.get("maximum_scope"),
        )
    return approved


def validate_excluded_scope(excluded_scope: dict[str, Any]) -> None:
    if excluded_scope.get("execution_authority_included") is not False:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_EXECUTION_AUTHORITY_PRESENT",
            field="excluded_authority_scope.execution_authority_included",
            expected=False,
            actual=excluded_scope.get("execution_authority_included"),
        )
    missing = [
        value
        for value in REQUIRED_EXCLUSIONS
        if value not in excluded_scope.get("excluded_authorities", [])
    ]
    if missing:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_EXCLUDED_SCOPE_MISMATCH",
            field="excluded_authority_scope.excluded_authorities",
            expected=REQUIRED_EXCLUSIONS,
            actual=excluded_scope.get("excluded_authorities", []),
        )


def human_decision_evidence() -> dict[str, Any]:
    statement_hash = sha256_bytes(DECISION_STATEMENT.encode("utf-8"))
    if DECISION_STATEMENT != "accepted, proceed":
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_HUMAN_STATEMENT_MISSING",
            field="decision_statement_exact",
            expected="accepted, proceed",
            actual=DECISION_STATEMENT,
        )
    if statement_hash != sha256_bytes(b"accepted, proceed"):
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_HUMAN_STATEMENT_HASH_MISMATCH",
            field="decision_statement_sha256",
            expected=sha256_bytes(b"accepted, proceed"),
            actual=statement_hash,
        )
    return {
        "decision_actor_class": "HUMAN_OPERATOR",
        "decision_actor_identity": "HUMAN_OPERATOR_CURRENT_MATRIXLAB_SESSION",
        "decision_source_kind": "EXPLICIT_INTERACTIVE_USER_INSTRUCTION",
        "decision_statement_exact": DECISION_STATEMENT,
        "decision_statement_normalized": DECISION_STATEMENT_NORMALIZED,
        "decision_interpretation": DECISION_BRANCH,
        "decision_date_local": DECISION_DATE_LOCAL,
        "decision_timezone": DECISION_TIMEZONE,
        "decision_time_precision": "DATE_AND_SESSION_SEQUENCE_ONLY",
        "decision_sequence_anchor": DECISION_SEQUENCE_ANCHOR,
        "decision_statement_sha256": statement_hash,
        "acceptance_has_declared_revisions": False,
        "acceptance_selects_recommended_option": True,
        "acceptance_uses_exact_bound_package": True,
        "acceptance_requires_new_package_hash": False,
        "acceptance_is_default_or_timeout_derived": False,
        "human_decision_explicit": True,
    }


def build_receipt(root: Path, surface: dict[str, Any]) -> dict[str, Any]:
    validate_source_surface(surface)
    validate_source_package(surface)
    approval_vector = validate_option_a(surface)
    approved_scope = approved_scope_from_surface(surface)
    excluded_scope = surface.get("excluded_authority_scope", {})
    validate_excluded_scope(excluded_scope)

    surface_sha = sha256_file(root, SOURCE_SURFACE_PATH)
    source_surface_binding = {
        "source_surface_artifact_id": SOURCE_SURFACE_ARTIFACT_ID,
        "source_surface_path": SOURCE_SURFACE_PATH,
        "source_surface_commit_sha": EXPECTED_HEAD,
        "source_surface_content_sha256": surface_sha,
        "source_surface_gate": SOURCE_SURFACE_GATE,
        "source_surface_terminal_transition": SOURCE_SURFACE_TERMINAL,
        "source_decision_package_sha256": SOURCE_DECISION_PACKAGE_SHA256,
        "source_surface_human_decision_recorded": False,
        "source_surface_decision_receipt_created": False,
        "source_surface_authority_update_applied": False,
        "source_surface_status": SOURCE_SURFACE_STATUS,
    }
    source_decision_package_binding = {
        "canonicalization": CANONICALIZATION_CONTRACT,
        "canonicalization_contract": CANONICALIZATION_CONTRACT,
        "bound_sections": SOURCE_BOUND_SECTIONS,
        "bound_section_count": len(SOURCE_BOUND_SECTIONS),
        "bound_sections_match_payload_keys": True,
        "decision_package_sha256": SOURCE_DECISION_PACKAGE_SHA256,
        "decision_package_hash_recomputes": True,
    }
    evidence = human_decision_evidence()
    if evidence["decision_interpretation"] != DECISION_BRANCH:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_DECISION_INTERPRETATION_AMBIGUOUS",
            field="decision_interpretation",
            expected=DECISION_BRANCH,
            actual=evidence["decision_interpretation"],
        )
    decision_selection = {
        "decision_branch": DECISION_BRANCH,
        "decision_mode": DECISION_BRANCH,
        "accepted_option": ACCEPTED_OPTION,
        "direction_id": DIRECTION_ID,
        "target_family": TARGET_FAMILY,
        "first_target": FIRST_TARGET,
        "bundle_id": BUNDLE_ID,
        "accepted_decision_package_sha256": SOURCE_DECISION_PACKAGE_SHA256,
        "accepted_with_revisions": False,
        "revision_count": 0,
        "revisions": [],
        "second_target_selected": False,
        "portability_scope_selected": False,
        "option_a_requires_explicit_scope_vector": True,
        "option_token_alone_is_not_a_complete_decision_receipt": True,
    }
    revision_state = {
        "accepted_with_revisions": False,
        "revision_count": 0,
        "revisions": [],
        "acceptance_has_declared_revisions": False,
        "acceptance_requires_new_package_hash": False,
    }
    decision_state_after_receipt = {
        "human_decision_required": True,
        "human_decision_recorded": True,
        "decision_receipt_created": True,
        "direction_selected": True,
        "target_family_selected": True,
        "first_target_selected": True,
        "definition_scope_approved": True,
        "bounded_construction_scope_approved": True,
        "construction_scope_approved": True,
        "construction_verification_scope_approved": True,
        "accepted_exact_package": True,
        "accepted_with_revisions": False,
        "authority_state_mutated": False,
        "authority_update_applied": False,
        "authority_transition_closed": False,
        "vs2_authority_granted": False,
        "vs2_profile_and_target_freeze_authority_granted": False,
        "vs2_bounded_construction_authority_granted": False,
        "fixture_construction_authority_granted": False,
        "readiness_gate_construction_authority_granted": False,
        "construction_package_verification_authority_granted": False,
        "vs2_started": False,
        "vs2_1_built": False,
        "execution_authorized": False,
        "positive_path_execution_authorized": False,
        "negative_path_execution_authorized": False,
        "sweep_authorized": False,
        "automatic_rerun_authorized": False,
        "runner_authority_created": False,
        "second_target_selected": False,
        "portability_scope_selected": False,
    }
    authority_effects = {
        "decision_receipt_mutates_authority": False,
        "decision_receipt_grants_authority": False,
        "decision_receipt_consumes_construction_authority": False,
        "decision_receipt_consumes_execution_authority": False,
        "approved_scope_eligible_for_authority_update": True,
        "approved_scope_applied_to_authority_state": False,
        "authority_update_required": True,
        "authority_update_created_by_this_unit": False,
        "transition_closure_required_after_authority_update": True,
        "transition_closure_created_by_this_unit": False,
    }
    downstream_authority_update_requirement = {
        "required": True,
        "next_unit": "POST_VS1_DIRECTION_AUTHORITY_UPDATE_V0_PENDING",
        "authority_update_created_by_this_unit": False,
        "authority_update_must_bind_decision_receipt_sha256": True,
    }
    downstream_transition_closure_requirement = {
        "required_after_authority_update": True,
        "transition_closure_created_by_this_unit": False,
        "transition_closure_must_bind_authority_update": True,
    }
    receipt_payload = {
        "source_surface_binding": source_surface_binding,
        "source_decision_package_binding": source_decision_package_binding,
        "human_decision_evidence": evidence,
        "decision_selection": decision_selection,
        "approval_vector": approval_vector,
        "approved_scope": approved_scope,
        "excluded_authority_scope": excluded_scope,
        "revision_state": revision_state,
        "decision_state_after_receipt": decision_state_after_receipt,
        "authority_effects": authority_effects,
        "downstream_authority_update_requirement": downstream_authority_update_requirement,
        "downstream_transition_closure_requirement": downstream_transition_closure_requirement,
    }
    if list(receipt_payload.keys()) != RECEIPT_BOUND_SECTIONS:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_RECEIPT_HASH_MISMATCH",
            field="decision_receipt_payload",
            expected=RECEIPT_BOUND_SECTIONS,
            actual=list(receipt_payload.keys()),
        )
    receipt_sha = canonical_hash(receipt_payload)
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "artifact_id": ARTIFACT_ID,
        "object_id": OBJECT_ID,
        "object_role": OBJECT_ROLE,
        "receipt_status": RECEIPT_STATUS,
        "source_surface_binding": source_surface_binding,
        "source_decision_package_binding": source_decision_package_binding,
        "human_decision_evidence": evidence,
        "decision_selection": decision_selection,
        "approval_vector": approval_vector,
        "approved_scope": approved_scope,
        "excluded_authority_scope": excluded_scope,
        "revision_state": revision_state,
        "decision_state_after_receipt": decision_state_after_receipt,
        "authority_effects": authority_effects,
        "downstream_authority_update_requirement": downstream_authority_update_requirement,
        "downstream_transition_closure_requirement": downstream_transition_closure_requirement,
        "decision_receipt_binding": {
            "canonicalization": CANONICALIZATION_CONTRACT,
            "canonicalization_contract": CANONICALIZATION_CONTRACT,
            "bound_sections": RECEIPT_BOUND_SECTIONS,
            "decision_receipt_payload": receipt_payload,
            "decision_receipt_sha256": receipt_sha,
            "volatile_filesystem_metadata_excluded_from_hash": True,
            "generated_at_metadata_excluded_from_hash": True,
            "commit_created_fields_excluded_from_hash": True,
            "future_authority_update_fields_excluded_from_hash": True,
            "authority_update_must_bind_decision_receipt_sha256": True,
            "transition_closure_must_bind_authority_update": True,
        },
        "receipt_checks": [
            {"check_id": check, "check_result": check, "status": "PASS"}
            for check in RECEIPT_CHECKS
        ],
        "receipt_gate": RECEIPT_GATE,
        "terminal_transition": {
            "transition": TERMINAL_TRANSITION,
            "records_human_decision": True,
            "creates_decision_receipt": True,
            "applies_authority_update": False,
            "grants_vs2_authority": False,
            "closes_authority_transition": False,
            "starts_vs2": False,
            "builds_vs2_1": False,
            "authorizes_execution": False,
            "authorizes_sweep": False,
            "authorizes_rerun": False,
            "creates_runner_authority": False,
        },
        "evidence_yield": {
            "branch": "CONFIRMATION_YIELD",
            "source_surface_verified": True,
            "human_decision_explicit": True,
            "receipt_hash_bound": True,
        },
        "non_claims": [
            "This receipt records a human decision only.",
            "This receipt does not mutate authority state.",
            "This receipt does not grant VS2 authority.",
            "This receipt does not authorize execution, sweeps, reruns, or runner authority.",
            "This receipt does not create an authority update or transition closure.",
        ],
        "failures": [],
    }
    validate_receipt(receipt, surface)
    return receipt


def validate_receipt(receipt: dict[str, Any], surface: dict[str, Any]) -> None:
    state = receipt["decision_state_after_receipt"]
    selection = receipt["decision_selection"]
    evidence = receipt["human_decision_evidence"]
    approved_scope = receipt["approved_scope"]
    authority_effects = receipt["authority_effects"]
    if "decision_mode" not in selection:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_DECISION_MODE_MISSING",
            field="decision_selection.decision_mode",
            expected=DECISION_BRANCH,
            actual=None,
        )
    if selection["decision_mode"] != DECISION_BRANCH:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_DECISION_MODE_MISMATCH",
            field="decision_selection.decision_mode",
            expected=DECISION_BRANCH,
            actual=selection["decision_mode"],
        )
    if not (
        selection["decision_mode"]
        == selection["decision_branch"]
        == evidence["decision_interpretation"]
    ):
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_DECISION_MODE_ALIAS_DIVERGENCE",
            field="decision_selection",
            expected=DECISION_BRANCH,
            actual={
                "decision_mode": selection.get("decision_mode"),
                "decision_branch": selection.get("decision_branch"),
                "decision_interpretation": evidence.get("decision_interpretation"),
            },
        )
    if "approved_scope_eligible_for_authority_update" not in approved_scope:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_APPROVED_SCOPE_ELIGIBILITY_MISSING",
            field="approved_scope.approved_scope_eligible_for_authority_update",
            expected=True,
            actual=None,
        )
    if approved_scope["approved_scope_eligible_for_authority_update"] is not True:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_APPROVED_SCOPE_ELIGIBILITY_MISMATCH",
            field="approved_scope.approved_scope_eligible_for_authority_update",
            expected=True,
            actual=approved_scope["approved_scope_eligible_for_authority_update"],
        )
    if approved_scope["approved_scope_eligible_for_authority_update"] != authority_effects["approved_scope_eligible_for_authority_update"]:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_APPROVED_SCOPE_ELIGIBILITY_ALIAS_DIVERGENCE",
            field="approved_scope.approved_scope_eligible_for_authority_update",
            expected=authority_effects["approved_scope_eligible_for_authority_update"],
            actual=approved_scope["approved_scope_eligible_for_authority_update"],
        )
    if "approved_scope_applied_to_authority_state" not in approved_scope:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_APPROVED_SCOPE_APPLICATION_FIELD_MISSING",
            field="approved_scope.approved_scope_applied_to_authority_state",
            expected=False,
            actual=None,
        )
    if approved_scope["approved_scope_applied_to_authority_state"] is not False:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_APPROVED_SCOPE_APPLICATION_FIELD_MISMATCH",
            field="approved_scope.approved_scope_applied_to_authority_state",
            expected=False,
            actual=approved_scope["approved_scope_applied_to_authority_state"],
        )
    if approved_scope["approved_scope_applied_to_authority_state"] != authority_effects["approved_scope_applied_to_authority_state"]:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_APPROVED_SCOPE_APPLICATION_ALIAS_DIVERGENCE",
            field="approved_scope.approved_scope_applied_to_authority_state",
            expected=authority_effects["approved_scope_applied_to_authority_state"],
            actual=approved_scope["approved_scope_applied_to_authority_state"],
        )
    if state["accepted_with_revisions"] is not False or receipt["revision_state"]["revision_count"] != 0:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_UNDECLARED_REVISION_PRESENT",
            field="revision_state",
            expected={"accepted_with_revisions": False, "revision_count": 0},
            actual=receipt["revision_state"],
        )
    if state["second_target_selected"] is not False or receipt["approval_vector"]["second_target_scope_approved"] is not False:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_SECOND_TARGET_INCLUDED",
            field="second_target",
            expected=False,
            actual=True,
        )
    if state["portability_scope_selected"] is not False or receipt["approval_vector"]["portability_scope_approved"] is not False:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_PORTABILITY_SCOPE_INCLUDED",
            field="portability",
            expected=False,
            actual=True,
        )
    authority_false_fields = [
        "authority_state_mutated",
        "authority_update_applied",
        "authority_transition_closed",
        "vs2_authority_granted",
        "vs2_profile_and_target_freeze_authority_granted",
        "vs2_bounded_construction_authority_granted",
        "fixture_construction_authority_granted",
        "readiness_gate_construction_authority_granted",
        "construction_package_verification_authority_granted",
    ]
    for field in authority_false_fields:
        if state[field] is not False:
            fail(
                "STOP_POST_VS1_DECISION_RECEIPT_AUTHORITY_MUTATION_PRESENT",
                field=f"decision_state_after_receipt.{field}",
                expected=False,
                actual=state[field],
            )
    execution_false_fields = [
        "execution_authorized",
        "positive_path_execution_authorized",
        "negative_path_execution_authorized",
    ]
    for field in execution_false_fields:
        if state[field] is not False:
            fail(
                "STOP_POST_VS1_DECISION_RECEIPT_EXECUTION_AUTHORITY_PRESENT",
                field=f"decision_state_after_receipt.{field}",
                expected=False,
                actual=state[field],
            )
    for field, code in [
        ("sweep_authorized", "STOP_POST_VS1_DECISION_RECEIPT_SWEEP_AUTHORITY_PRESENT"),
        ("automatic_rerun_authorized", "STOP_POST_VS1_DECISION_RECEIPT_SWEEP_AUTHORITY_PRESENT"),
        ("runner_authority_created", "STOP_POST_VS1_DECISION_RECEIPT_RUNNER_AUTHORITY_PRESENT"),
        ("vs2_started", "STOP_POST_VS1_DECISION_RECEIPT_VS2_STARTED"),
    ]:
        if state[field] is not False:
            fail(
                code,
                field=f"decision_state_after_receipt.{field}",
                expected=False,
                actual=state[field],
            )
    if state["vs2_1_built"] is not False:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_VS2_STARTED",
            field="decision_state_after_receipt.vs2_1_built",
            expected=False,
            actual=state["vs2_1_built"],
        )
    expected_scope = {
        key: surface["proposed_approval_scope"][key]
        for key in [
            "direction_selection_scope",
            "definition_scope",
            "bounded_construction_scope",
            "construction_verification_scope",
            "maximum_scope",
        ]
    }
    actual_scope_lists = {key: receipt["approved_scope"][key] for key in expected_scope}
    if actual_scope_lists != expected_scope:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_APPROVED_SCOPE_MISMATCH",
            field="approved_scope",
            expected=expected_scope,
            actual=actual_scope_lists,
        )
    if receipt["excluded_authority_scope"] != surface["excluded_authority_scope"]:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_EXCLUDED_SCOPE_MISMATCH",
            field="excluded_authority_scope",
            expected=surface["excluded_authority_scope"],
            actual=receipt["excluded_authority_scope"],
        )
    binding = receipt["decision_receipt_binding"]
    if list(binding["decision_receipt_payload"].keys()) != binding["bound_sections"]:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_PAYLOAD_KEY_ORDER_MISMATCH",
            field="decision_receipt_binding.bound_sections",
            expected=binding["bound_sections"],
            actual=list(binding["decision_receipt_payload"].keys()),
        )
    recomputed = canonical_hash(binding["decision_receipt_payload"])
    if recomputed != binding["decision_receipt_sha256"]:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_POST_REPAIR_HASH_MISMATCH",
            field="decision_receipt_binding.decision_receipt_sha256",
            expected=recomputed,
            actual=binding["decision_receipt_sha256"],
        )
    if binding["decision_receipt_sha256"] == PRE_REPAIR_DECISION_RECEIPT_SHA256:
        fail(
            "STOP_POST_VS1_DECISION_RECEIPT_HASH_DID_NOT_CHANGE_AFTER_PAYLOAD_REPAIR",
            field="decision_receipt_binding.decision_receipt_sha256",
            expected=f"not {PRE_REPAIR_DECISION_RECEIPT_SHA256}",
            actual=binding["decision_receipt_sha256"],
        )


def build_markdown(receipt: dict[str, Any]) -> str:
    selection = receipt["decision_selection"]
    state = receipt["decision_state_after_receipt"]
    return f"""# Post-VS1 Direction Decision Receipt v0

## Human decision

Human decision:
{receipt["human_decision_evidence"]["decision_statement_exact"]}

Normalized accepted option:
{selection["accepted_option"]}

Selected direction:
{selection["direction_id"]}

Selected target family:
{selection["target_family"]}

Selected first target:
{selection["first_target"]}

Accepted package hash:
{selection["accepted_decision_package_sha256"]}

Decision mode:
{selection["decision_mode"]}

Decision mode note:
Exact package accepted without revisions.

Approved scope eligible for authority update:
{str(receipt["approved_scope"]["approved_scope_eligible_for_authority_update"]).lower()}

Approved scope applied to authority state:
{str(receipt["approved_scope"]["approved_scope_applied_to_authority_state"]).lower()}

## Approved

- direction selection
- target-family selection
- first-target selection
- definition scope
- bounded construction scope
- construction-verification scope

## Not granted

- authority state
- VS2 authority
- execution authority
- sweep authority
- rerun authority
- runner authority
- reuse authority
- promotion authority
- second-target scope
- portability scope

## Current state

Human decision recorded.
Decision receipt created.
Authority update not applied.
Authority transition not closed.
VS2 not started.
VS2.1 not built.
Execution not authorized.
Sweeps not authorized.
Runner authority not created.

## Binding

- source surface commit: {receipt["source_surface_binding"]["source_surface_commit_sha"]}
- source decision package hash: {receipt["source_surface_binding"]["source_decision_package_sha256"]}
- decision receipt hash: {receipt["decision_receipt_binding"]["decision_receipt_sha256"]}
- authority update applied: {str(state["authority_update_applied"]).lower()}
- execution authorized: {str(state["execution_authorized"]).lower()}

Pre-repair receipt hash:
{PRE_REPAIR_DECISION_RECEIPT_SHA256}

Post-repair receipt hash:
{receipt["decision_receipt_binding"]["decision_receipt_sha256"]}

Receipt hash changed because canonical payload serialization was repaired.

## Next

POST_VS1_DIRECTION_AUTHORITY_UPDATE_V0_PENDING
"""


def emit_success(receipt: dict[str, Any]) -> None:
    binding = receipt["decision_receipt_binding"]
    evidence = receipt["human_decision_evidence"]
    selection = receipt["decision_selection"]
    vector = receipt["approval_vector"]
    state = receipt["decision_state_after_receipt"]
    print("BUILD_POST_VS1_DIRECTION_DECISION_RECEIPT_V0_COMPLETE")
    print()
    print(f"artifact_id={ARTIFACT_ID}")
    print(f"schema_version={SCHEMA_VERSION}")
    print(f"object_id={OBJECT_ID}")
    print(f"object_role={OBJECT_ROLE}")
    print()
    print(f"source_surface_commit_sha={EXPECTED_HEAD}")
    print(f"source_decision_package_sha256={SOURCE_DECISION_PACKAGE_SHA256}")
    print("source_decision_package_hash_recomputes=true")
    print()
    print(f"human_decision_statement={DECISION_STATEMENT}")
    print("human_decision_statement_hash_present=true")
    print("human_decision_explicit=true")
    print()
    print(f"accepted_option={ACCEPTED_OPTION}")
    print(f"decision_mode={selection['decision_mode']}")
    print("accepted_with_revisions=false")
    print("revision_count=0")
    print()
    print(f"selected_direction={selection['direction_id']}")
    print(f"selected_target_family={selection['target_family']}")
    print(f"selected_first_target={selection['first_target']}")
    print()
    print("direction_selected=true")
    print("target_family_selected=true")
    print("first_target_selected=true")
    print()
    print("definition_scope_approved=true")
    print("bounded_construction_scope_approved=true")
    print("construction_verification_scope_approved=true")
    print()
    for key in [
        "execution_scope_approved",
        "positive_path_execution_scope_approved",
        "negative_path_execution_scope_approved",
        "sweep_scope_approved",
        "automatic_rerun_scope_approved",
        "runner_scope_approved",
        "reusable_schema_scope_approved",
        "reusable_move_scope_approved",
        "second_target_scope_approved",
        "portability_scope_approved",
    ]:
        print(f"{key}={str(vector[key]).lower()}")
    print()
    print("decision_receipt_created=true")
    print("decision_receipt_hash_present=true")
    print(f"pre_repair_decision_receipt_sha256={PRE_REPAIR_DECISION_RECEIPT_SHA256}")
    print(f"post_repair_decision_receipt_sha256={binding['decision_receipt_sha256']}")
    print(
        "decision_receipt_hash_changed_for_declared_serialization_repair="
        f"{str(binding['decision_receipt_sha256'] != PRE_REPAIR_DECISION_RECEIPT_SHA256).lower()}"
    )
    print(
        "decision_receipt_hash_recomputes="
        f"{str(canonical_hash(binding['decision_receipt_payload']) == binding['decision_receipt_sha256']).lower()}"
    )
    print(
        "approved_scope_eligible_for_authority_update="
        f"{str(receipt['approved_scope']['approved_scope_eligible_for_authority_update']).lower()}"
    )
    print(
        "approved_scope_applied_to_authority_state="
        f"{str(receipt['approved_scope']['approved_scope_applied_to_authority_state']).lower()}"
    )
    print()
    print("authority_state_mutated=false")
    print("authority_update_applied=false")
    print("authority_transition_closed=false")
    print()
    print("vs2_authority_granted=false")
    print("vs2_started=false")
    print("vs2_1_built=false")
    print()
    print(f"execution_authorized={str(state['execution_authorized']).lower()}")
    print(f"sweep_authorized={str(state['sweep_authorized']).lower()}")
    print(f"automatic_rerun_authorized={str(state['automatic_rerun_authorized']).lower()}")
    print(f"runner_authority_created={str(state['runner_authority_created']).lower()}")
    print()
    print(f"receipt_gate={RECEIPT_GATE}")
    print("evidence_yield_branch=CONFIRMATION_YIELD")
    print()
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode != 0
    print(f"staged_changes_present={str(staged).lower()}")
    print("commit_created=false")
    print("push_executed=false")
    print()
    print(f"terminal_transition={TERMINAL_TRANSITION}")


def emit_failure(exc: ReceiptFailure) -> None:
    print("BUILD_POST_VS1_DIRECTION_DECISION_RECEIPT_V0_FAILED")
    print(f"failure_code={exc.code}")
    print(f"field={exc.field}")
    print(f"expected={json.dumps(exc.expected, sort_keys=True)}")
    print(f"actual={json.dumps(exc.actual, sort_keys=True)}")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition=STOP({exc.code})")


def generate() -> int:
    root = detect_repo_root(Path.cwd())
    require_repo_context(root)
    validate_dirty_scope(root)
    ensure_no_forbidden_artifacts(root)
    for path in PRESERVED_SOURCE_PATHS:
        if not (root / path).exists():
            fail(
                "STOP_POST_VS1_DECISION_RECEIPT_SOURCE_SURFACE_MISSING",
                field=path,
                expected="present",
                actual="missing",
            )
    before = capture_source_hashes(root)
    surface = load_json(root, SOURCE_SURFACE_PATH)
    receipt = build_receipt(root, surface)
    (root / OUTPUT_JSON).parent.mkdir(parents=True, exist_ok=True)
    (root / OUTPUT_JSON).write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )
    (root / OUTPUT_MD).write_text(build_markdown(receipt), encoding="utf-8")
    after = capture_source_hashes(root)
    validate_source_preservation(before, after)
    validate_dirty_scope(root)
    ensure_no_forbidden_artifacts(root)
    emit_success(receipt)
    return 0


def main() -> int:
    try:
        return generate()
    except ReceiptFailure as exc:
        emit_failure(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
