#!/usr/bin/env python3
"""Build POST-VS1 direction authority update v0."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


EXPECTED_BRANCH = "master"
EXPECTED_HEAD = "3dc012d9d72201d2baf4c7d31d7545a68659ce9d"
SOURCE_RECEIPT_COMMIT = EXPECTED_HEAD
SOURCE_SURFACE_COMMIT = "975d05dfda23a632c91faeaae66abbfcf4e85da6"
SOURCE_RECEIPT_CANONICAL_SHA256 = (
    "19defc100428931ed455e4d2a64697bb9d886b11b856ececb0da6743c94f0dfe"
)
SOURCE_DECISION_PACKAGE_SHA256 = (
    "e9e4143ad2efdd285fe9e598e50d965d82057f7a8d6ccc4c52478a596d6b788b"
)

SCHEMA_VERSION = "matrixlabs_post_vs1_direction_authority_update_v0"
ARTIFACT_ID = "post_vs1_direction_authority_update_v0"
OBJECT_ID = "POST_VS1_DIRECTION_AUTHORITY_UPDATE"
OBJECT_ROLE = "BOUNDED_AUTHORITY_STATE_UPDATE_ONLY"
AUTHORITY_UPDATE_STATUS = "APPROVED_SCOPE_APPLIED_PENDING_TRANSITION_CLOSURE"
AUTHORITY_UPDATE_GATE = (
    "POST_VS1_DIRECTION_AUTHORITY_UPDATE_PASS_APPROVED_SCOPE_APPLIED_EXECUTION_AUTHORITY_ABSENT"
)
TERMINAL_TRANSITION = "ADVANCE(POST_VS1_DIRECTION_TRANSITION_CLOSURE_V0_PENDING)"

SOURCE_RECEIPT_PATH = "docs/matrixlabs/post_vs1/post_vs1_direction_decision_receipt_v0.json"
SOURCE_RECEIPT_MD_PATH = "docs/matrixlabs/post_vs1/post_vs1_direction_decision_receipt_v0.md"
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
OUTPUT_JSON = "docs/matrixlabs/post_vs1/post_vs1_direction_authority_update_v0.json"
OUTPUT_MD = "docs/matrixlabs/post_vs1/post_vs1_direction_authority_update_v0.md"

SOURCE_RECEIPT_SCHEMA = "matrixlabs_post_vs1_direction_decision_receipt_v0"
SOURCE_RECEIPT_ARTIFACT_ID = "post_vs1_direction_decision_receipt_v0"
SOURCE_RECEIPT_OBJECT_ID = "POST_VS1_DIRECTION_DECISION_RECEIPT"
SOURCE_RECEIPT_OBJECT_ROLE = "HUMAN_DIRECTION_DECISION_RECEIPT_ONLY"
SOURCE_RECEIPT_STATUS = "HUMAN_ACCEPTANCE_RECORDED_PENDING_AUTHORITY_UPDATE"
SOURCE_RECEIPT_GATE = "POST_VS1_DIRECTION_DECISION_RECEIPT_PASS_ACCEPT_EXACT_SCOPE_RECORDED"
SOURCE_RECEIPT_TERMINAL = "ADVANCE(POST_VS1_DIRECTION_AUTHORITY_UPDATE_V0_PENDING)"

CANONICALIZATION_CONTRACT = "MATRIXLAB_CANONICAL_JSON_V0"
ACCEPTED_OPTION = "ACCEPT_FIRST_SWEEP_CAPABLE_KERNEL_DIRECTION_AND_PROPOSED_SCOPE"
DECISION_MODE = "ACCEPT_EXACT_PROPOSED_SCOPE"
APPLICATION_MODE = "APPLY_EXACT_APPROVED_SCOPE"
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

AUTHORITY_UPDATE_BOUND_SECTIONS = [
    "source_decision_receipt_binding",
    "source_decision_package_binding",
    "authority_update_invocation_evidence",
    "prior_authority_state",
    "applied_authority_scope",
    "granted_authority_vector",
    "withheld_authority_vector",
    "decision_receipt_consumption",
    "authority_state_after_update",
    "transition_closure_requirement",
]

PRESERVED_SOURCE_PATHS = [
    SOURCE_RECEIPT_PATH,
    SOURCE_RECEIPT_MD_PATH,
    SOURCE_SURFACE_PATH,
    SOURCE_SURFACE_MD_PATH,
    PROPOSAL_SOURCE_PATH,
    PROPOSAL_SOURCE_SIDECAR_PATH,
    VS1_CLOSURE_PATH,
    VS1_MAP_PATH,
]

FORBIDDEN_ARTIFACTS = [
    "docs/matrixlabs/post_vs1/post_vs1_direction_transition_closure_v0.json",
    "docs/matrixlabs/post_vs1/post_vs1_direction_transition_closure_v0.md",
    "docs/matrixlabs/phase_vs2",
    "docs/matrixlabs/runner",
    "docs/matrixlabs/runtime",
    "docs/matrixlabs/move_space",
    "docs/matrixlabs/micro_sweeps",
]

AUTHORITY_UPDATE_CHECKS = [
    "POST_VS1_AUTHORITY_UPDATE_SOURCE_RECEIPT_COMMITTED_BYTES_VERIFIED",
    "POST_VS1_AUTHORITY_UPDATE_SOURCE_RECEIPT_CANONICAL_HASH_VERIFIED",
    "POST_VS1_AUTHORITY_UPDATE_SOURCE_DECISION_PACKAGE_HASH_VERIFIED",
    "POST_VS1_AUTHORITY_UPDATE_ACCEPTED_OPTION_VERIFIED",
    "POST_VS1_AUTHORITY_UPDATE_EXACT_SCOPE_APPLICATION_PASS",
    "POST_VS1_AUTHORITY_UPDATE_APPLIED_SCOPE_WITHIN_APPROVED_SCOPE",
    "POST_VS1_AUTHORITY_UPDATE_DEFINITION_AUTHORITY_GRANTED",
    "POST_VS1_AUTHORITY_UPDATE_BOUNDED_CONSTRUCTION_AUTHORITY_GRANTED",
    "POST_VS1_AUTHORITY_UPDATE_FIXTURE_CONSTRUCTION_AUTHORITY_GRANTED",
    "POST_VS1_AUTHORITY_UPDATE_READINESS_GATE_CONSTRUCTION_AUTHORITY_GRANTED",
    "POST_VS1_AUTHORITY_UPDATE_CONSTRUCTION_VERIFICATION_AUTHORITY_GRANTED",
    "POST_VS1_AUTHORITY_UPDATE_EXECUTION_AUTHORITY_ABSENT",
    "POST_VS1_AUTHORITY_UPDATE_SWEEP_AUTHORITY_ABSENT",
    "POST_VS1_AUTHORITY_UPDATE_RERUN_AUTHORITY_ABSENT",
    "POST_VS1_AUTHORITY_UPDATE_RUNNER_AUTHORITY_ABSENT",
    "POST_VS1_AUTHORITY_UPDATE_REUSE_AUTHORITY_ABSENT",
    "POST_VS1_AUTHORITY_UPDATE_SECOND_TARGET_AUTHORITY_ABSENT",
    "POST_VS1_AUTHORITY_UPDATE_PORTABILITY_AUTHORITY_ABSENT",
    "POST_VS1_AUTHORITY_UPDATE_SINGLE_CONSUMPTION_PASS",
    "POST_VS1_AUTHORITY_UPDATE_TRANSITION_CLOSURE_STILL_REQUIRED",
    "POST_VS1_AUTHORITY_UPDATE_VS2_NOT_STARTED",
    "POST_VS1_AUTHORITY_UPDATE_CANONICAL_BINDING_PASS",
]

WITHHELD_AUTHORITY_STATUSES = {
    "BROAD_OR_GLOBAL_VS2_AUTHORITY": "NOT_GRANTED",
    "KERNEL_EXECUTION_AUTHORITY": "NOT_GRANTED",
    "POSITIVE_PATH_EXECUTION_AUTHORITY": "NOT_GRANTED",
    "NEGATIVE_PATH_EXECUTION_AUTHORITY": "NOT_GRANTED",
    "PERTURBATION_SWEEP_EXECUTION_AUTHORITY": "NOT_GRANTED",
    "AUTOMATIC_RERUN_AUTHORITY": "NOT_GRANTED",
    "AUTOMATIC_RADIUS_RENEWAL_AUTHORITY": "NOT_GRANTED",
    "RADIUS_EXPANSION_AUTHORITY": "NOT_GRANTED",
    "MOVE_BUDGET_EXPANSION_AUTHORITY": "NOT_GRANTED",
    "CASE_BUDGET_EXPANSION_AUTHORITY": "NOT_GRANTED",
    "TARGET_FAMILY_EXPANSION_AUTHORITY": "NOT_GRANTED",
    "SECOND_TARGET_SELECTION_AUTHORITY": "NOT_GRANTED",
    "FIRST_TARGET_SUBSTITUTION_AUTHORITY": "NOT_GRANTED",
    "PORTABILITY_TESTING_AUTHORITY": "NOT_GRANTED",
    "AUTOMATIC_SOURCE_ACQUISITION_AUTHORITY": "NOT_GRANTED",
    "AUTOMATIC_SCHEMA_INVENTION_AUTHORITY": "NOT_GRANTED",
    "AUTOMATIC_CAPABILITY_CREATION_AUTHORITY": "NOT_GRANTED",
    "AUTOMATIC_AUTHORITY_ESCALATION_AUTHORITY": "NOT_GRANTED",
    "AUTOMATIC_REPAIR_AUTHORITY": "NOT_GRANTED",
    "AUTOMATIC_LOCAL_REVISION_AUTHORITY": "NOT_GRANTED",
    "REFINEMENT_APPLICATION_AUTHORITY": "NOT_GRANTED",
    "CANDIDATE_PROMOTION_AUTHORITY": "NOT_GRANTED",
    "REUSABLE_SCHEMA_AUTHORITY": "NOT_GRANTED",
    "REUSABLE_MOVE_SPACE_AUTHORITY": "NOT_GRANTED",
    "ACTIVE_REGISTRY_CREATION_AUTHORITY": "NOT_GRANTED",
    "RUNNER_AUTHORITY": "NOT_CREATED",
    "AUTONOMOUS_CONTINUATION_AUTHORITY": "NOT_GRANTED",
    "CROSS_DOMAIN_GENERALIZATION_AUTHORITY": "NOT_GRANTED",
    "PERFORMANCE_OPTIMIZATION_AUTHORITY": "NOT_GRANTED",
    "SCALE_OPTIMIZATION_AUTHORITY": "NOT_GRANTED",
}


class AuthorityUpdateFailure(RuntimeError):
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
    raise AuthorityUpdateFailure(code, field=field, expected=expected, actual=actual)


def run_git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def detect_repo_root(start: Path) -> Path:
    try:
        return Path(run_git(start, "rev-parse", "--show-toplevel"))
    except subprocess.CalledProcessError:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_UNEXPECTED_HEAD",
            field="repo",
            expected="/home/asd/projects/matrixlab",
            actual=str(start),
        )


def require_repo_context(root: Path) -> None:
    branch = run_git(root, "branch", "--show-current")
    head = run_git(root, "rev-parse", "HEAD")
    if branch != EXPECTED_BRANCH:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_UNEXPECTED_HEAD",
            field="branch",
            expected=EXPECTED_BRANCH,
            actual=branch,
        )
    if head != EXPECTED_HEAD:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_UNEXPECTED_HEAD",
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
        "?? scripts/build_post_vs1_direction_authority_update_v0.py",
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
            "STOP_POST_VS1_AUTHORITY_UPDATE_DOWNSTREAM_ARTIFACT_CREATED",
            field="git_status",
            expected=list(allowed_prefixes),
            actual=unexpected,
        )


def ensure_no_forbidden_artifacts(root: Path) -> None:
    present = [path for path in FORBIDDEN_ARTIFACTS if (root / path).exists()]
    if present:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_DOWNSTREAM_ARTIFACT_CREATED",
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
            "STOP_POST_VS1_AUTHORITY_UPDATE_SOURCE_RECEIPT_MISSING",
            field=rel_path,
            expected="present",
            actual="missing",
        )
    return json.loads(path.read_text(encoding="utf-8"))


def committed_file_bytes(root: Path, commit: str, rel_path: str) -> bytes:
    try:
        return subprocess.check_output(["git", "show", f"{commit}:{rel_path}"], cwd=root)
    except subprocess.CalledProcessError:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_SOURCE_RECEIPT_NOT_COMMITTED",
            field=rel_path,
            expected=f"{commit}:{rel_path}",
            actual="not_committed",
        )


def verify_committed_receipt_bytes(root: Path) -> tuple[bytes, str]:
    receipt_path = root / SOURCE_RECEIPT_PATH
    if not receipt_path.exists():
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_SOURCE_RECEIPT_MISSING",
            field=SOURCE_RECEIPT_PATH,
            expected="present",
            actual="missing",
        )
    committed = committed_file_bytes(root, SOURCE_RECEIPT_COMMIT, SOURCE_RECEIPT_PATH)
    worktree = receipt_path.read_bytes()
    if worktree != committed:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_SOURCE_RECEIPT_WORKTREE_DIVERGENCE",
            field=SOURCE_RECEIPT_PATH,
            expected=sha256_bytes(committed),
            actual=sha256_bytes(worktree),
        )
    return committed, sha256_bytes(committed)


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
            "STOP_POST_VS1_AUTHORITY_UPDATE_SOURCE_RECEIPT_REWRITE",
            field="source_hashes",
            expected=before,
            actual=changed,
        )


def validate_receipt_identity(receipt: dict[str, Any]) -> None:
    expected = {
        "schema_version": SOURCE_RECEIPT_SCHEMA,
        "artifact_id": SOURCE_RECEIPT_ARTIFACT_ID,
        "object_id": SOURCE_RECEIPT_OBJECT_ID,
        "object_role": SOURCE_RECEIPT_OBJECT_ROLE,
        "receipt_status": SOURCE_RECEIPT_STATUS,
        "receipt_gate": SOURCE_RECEIPT_GATE,
    }
    for key, value in expected.items():
        if receipt.get(key) != value:
            fail(
                "STOP_POST_VS1_AUTHORITY_UPDATE_SOURCE_RECEIPT_IDENTITY_MISMATCH",
                field=key,
                expected=value,
                actual=receipt.get(key),
            )
    if receipt.get("terminal_transition", {}).get("transition") != SOURCE_RECEIPT_TERMINAL:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_RECEIPT_TERMINAL_MISMATCH",
            field="terminal_transition.transition",
            expected=SOURCE_RECEIPT_TERMINAL,
            actual=receipt.get("terminal_transition", {}).get("transition"),
        )


def validate_receipt_binding(receipt: dict[str, Any]) -> None:
    binding = receipt.get("decision_receipt_binding", {})
    if binding.get("canonicalization") != CANONICALIZATION_CONTRACT:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_RECEIPT_CANONICALIZATION_MISMATCH",
            field="decision_receipt_binding.canonicalization",
            expected=CANONICALIZATION_CONTRACT,
            actual=binding.get("canonicalization"),
        )
    if binding.get("canonicalization_contract") != CANONICALIZATION_CONTRACT:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_RECEIPT_CANONICALIZATION_MISMATCH",
            field="decision_receipt_binding.canonicalization_contract",
            expected=CANONICALIZATION_CONTRACT,
            actual=binding.get("canonicalization_contract"),
        )
    payload = binding.get("decision_receipt_payload", {})
    if list(payload.keys()) != binding.get("bound_sections"):
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_RECEIPT_BOUND_SECTION_MISMATCH",
            field="decision_receipt_binding.bound_sections",
            expected=binding.get("bound_sections"),
            actual=list(payload.keys()),
        )
    recomputed = canonical_hash(payload)
    if binding.get("decision_receipt_sha256") != SOURCE_RECEIPT_CANONICAL_SHA256:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_RECEIPT_HASH_MISMATCH",
            field="decision_receipt_binding.decision_receipt_sha256",
            expected=SOURCE_RECEIPT_CANONICAL_SHA256,
            actual=binding.get("decision_receipt_sha256"),
        )
    if recomputed != SOURCE_RECEIPT_CANONICAL_SHA256:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_RECEIPT_HASH_MISMATCH",
            field="decision_receipt_binding.decision_receipt_payload",
            expected=SOURCE_RECEIPT_CANONICAL_SHA256,
            actual=recomputed,
        )


def validate_decision_package(receipt: dict[str, Any]) -> None:
    package_sha = receipt.get("source_decision_package_binding", {}).get("decision_package_sha256")
    source_binding_sha = receipt.get("source_surface_binding", {}).get("source_decision_package_sha256")
    selection_sha = receipt.get("decision_selection", {}).get("accepted_decision_package_sha256")
    if package_sha != SOURCE_DECISION_PACKAGE_SHA256 or source_binding_sha != SOURCE_DECISION_PACKAGE_SHA256 or selection_sha != SOURCE_DECISION_PACKAGE_SHA256:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_DECISION_PACKAGE_HASH_MISMATCH",
            field="source_decision_package_sha256",
            expected=SOURCE_DECISION_PACKAGE_SHA256,
            actual={
                "source_decision_package_binding": package_sha,
                "source_surface_binding": source_binding_sha,
                "decision_selection": selection_sha,
            },
        )


def validate_selection(receipt: dict[str, Any]) -> None:
    selection = receipt.get("decision_selection", {})
    evidence = receipt.get("human_decision_evidence", {})
    if selection.get("accepted_option") != ACCEPTED_OPTION:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_ACCEPTED_OPTION_MISMATCH",
            field="decision_selection.accepted_option",
            expected=ACCEPTED_OPTION,
            actual=selection.get("accepted_option"),
        )
    if not (
        selection.get("decision_mode")
        == selection.get("decision_branch")
        == evidence.get("decision_interpretation")
        == DECISION_MODE
    ):
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_DECISION_MODE_MISMATCH",
            field="decision_mode_aliases",
            expected=DECISION_MODE,
            actual={
                "decision_mode": selection.get("decision_mode"),
                "decision_branch": selection.get("decision_branch"),
                "decision_interpretation": evidence.get("decision_interpretation"),
            },
        )
    expected = {
        "direction_id": DIRECTION_ID,
        "target_family": TARGET_FAMILY,
        "first_target": FIRST_TARGET,
        "bundle_id": BUNDLE_ID,
    }
    for key, value in expected.items():
        if selection.get(key) != value:
            fail(
                "STOP_POST_VS1_AUTHORITY_UPDATE_SELECTION_MISMATCH",
                field=f"decision_selection.{key}",
                expected=value,
                actual=selection.get(key),
            )
    if selection.get("accepted_with_revisions") is not False or selection.get("revision_count") != 0 or selection.get("revisions") != []:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_UNDECLARED_REVISION_PRESENT",
            field="decision_selection.revisions",
            expected={"accepted_with_revisions": False, "revision_count": 0, "revisions": []},
            actual=selection,
        )
    if selection.get("second_target_selected") is not False:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_SECOND_TARGET_PRESENT",
            field="decision_selection.second_target_selected",
            expected=False,
            actual=selection.get("second_target_selected"),
        )
    if selection.get("portability_scope_selected") is not False:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_PORTABILITY_SCOPE_PRESENT",
            field="decision_selection.portability_scope_selected",
            expected=False,
            actual=selection.get("portability_scope_selected"),
        )


def validate_approval(receipt: dict[str, Any]) -> None:
    if receipt.get("approval_vector") != EXPECTED_APPROVAL_VECTOR:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_APPROVAL_VECTOR_MISMATCH",
            field="approval_vector",
            expected=EXPECTED_APPROVAL_VECTOR,
            actual=receipt.get("approval_vector"),
        )
    approved = receipt.get("approved_scope", {})
    effects = receipt.get("authority_effects", {})
    if approved.get("approved_scope_eligible_for_authority_update") is not True:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_SCOPE_NOT_ELIGIBLE",
            field="approved_scope.approved_scope_eligible_for_authority_update",
            expected=True,
            actual=approved.get("approved_scope_eligible_for_authority_update"),
        )
    if approved.get("approved_scope_applied_to_authority_state") is not False:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_SCOPE_ALREADY_APPLIED",
            field="approved_scope.approved_scope_applied_to_authority_state",
            expected=False,
            actual=approved.get("approved_scope_applied_to_authority_state"),
        )
    if (
        approved.get("approved_scope_eligible_for_authority_update")
        != effects.get("approved_scope_eligible_for_authority_update")
        or approved.get("approved_scope_applied_to_authority_state")
        != effects.get("approved_scope_applied_to_authority_state")
    ):
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_SOURCE_ALIAS_DIVERGENCE",
            field="approved_scope/authority_effects",
            expected=approved,
            actual=effects,
        )


def grant_record(grant_id: str, grant_scope: list[str]) -> dict[str, Any]:
    return {
        "grant_id": grant_id,
        "grant_status": "GRANTED",
        "grant_basis_artifact_id": SOURCE_RECEIPT_ARTIFACT_ID,
        "grant_basis_commit_sha": SOURCE_RECEIPT_COMMIT,
        "grant_basis_receipt_sha256": SOURCE_RECEIPT_CANONICAL_SHA256,
        "grant_basis_decision_package_sha256": SOURCE_DECISION_PACKAGE_SHA256,
        "grant_scope": grant_scope,
        "grant_target_phase": "VS2",
        "grant_target_direction": DIRECTION_ID,
        "grant_target_family": TARGET_FAMILY,
        "grant_first_target": FIRST_TARGET,
        "grant_reusable": False,
        "grant_portable": False,
        "grant_generalizing": False,
        "grant_execution_capable": False,
        "grant_effective_for_downstream_consumption": False,
        "grant_effectivity_condition": "POST_VS1_DIRECTION_TRANSITION_CLOSURE_PASS_REQUIRED",
        "grant_consumed_by_this_update": False,
    }


def granted_authority_vector() -> dict[str, Any]:
    profile_scope = [
        "define the First Sweep-Capable Kernel profile",
        "freeze one target family",
        "freeze one first target",
        "define the target scope and regime",
        "classify the MCCL components",
        "freeze the maximum construction envelope",
        "bind the downstream VS2 construction sequence",
    ]
    bounded_construction_scope = [
        "construct only the declared target-bound contract and schema artifacts",
        "construct the finite move-space",
        "construct selector and applicator contracts",
        "construct source, budget, halt, convergence, receipt, and evidence-yield artifacts",
        "construct replay and audit evidence surfaces",
        "construct the run-package manifest and source bindings",
    ]
    fixture_scope = [
        "construct one bounded fixture set",
        "construct positive-path fixtures",
        "construct negative-path fixtures",
        "construct bounded perturbation fixtures",
    ]
    readiness_scope = [
        "construct the first-run kernel construction-readiness gate",
    ]
    verification_scope = [
        "verify required construction artifacts are present",
        "verify hashes and source bindings",
        "verify fixture identities",
        "verify move-space finiteness",
        "verify selector and applicator contracts",
        "verify budgets and halts",
        "verify forbidden effects remain false",
        "verify the execution entrypoint remains disabled or unauthorized",
        "verify eligibility for a later execution-authority decision",
    ]
    records = [
        grant_record("VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY", profile_scope),
        grant_record("VS2_BOUNDED_CONSTRUCTION_AUTHORITY", bounded_construction_scope),
        grant_record("VS2_FIXTURE_CONSTRUCTION_AUTHORITY", fixture_scope),
        grant_record("VS2_FIRST_RUN_READINESS_GATE_CONSTRUCTION_AUTHORITY", readiness_scope),
        grant_record("VS2_CONSTRUCTION_PACKAGE_VERIFICATION_AUTHORITY", verification_scope),
    ]
    return {
        "VS2_DEFINITION_AUTHORITY": "GRANTED",
        "VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY": "GRANTED",
        "VS2_BOUNDED_CONSTRUCTION_AUTHORITY": "GRANTED",
        "VS2_FIXTURE_CONSTRUCTION_AUTHORITY": "GRANTED",
        "VS2_FIRST_RUN_READINESS_GATE_CONSTRUCTION_AUTHORITY": "GRANTED",
        "VS2_CONSTRUCTION_PACKAGE_VERIFICATION_AUTHORITY": "GRANTED",
        "definition_authority_aliases_profile_and_target_freeze_authority": True,
        "permitted_first_consumer": "VS2.1",
        "grant_records": records,
        "grant_record_count": len(records),
        "grant_effective_for_downstream_consumption": False,
        "grant_effectivity_condition": "POST_VS1_DIRECTION_TRANSITION_CLOSURE_PASS_REQUIRED",
        "grant_consumed_by_this_update": False,
        "not_permitted_by_profile_and_target_freeze_authority": [
            "construct schemas",
            "construct fixtures",
            "construct readiness gates",
            "construct verification results",
        ],
        "fixture_construction_boundary": "authority to construct fixtures != authority to run fixtures",
        "readiness_gate_boundary": "first-run kernel readiness gate != S21 controlled-loop readiness re-audit != execution authority",
        "construction_verification_boundary": "construction package verified != execution authorized",
    }


def withheld_authority_vector(excluded_scope: dict[str, Any]) -> dict[str, Any]:
    required_exclusions = {
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
    }
    missing = sorted(required_exclusions - set(excluded_scope.get("excluded_authorities", [])))
    if missing or excluded_scope.get("execution_authority_included") is not False:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_EXCLUDED_SCOPE_NOT_PRESERVED",
            field="excluded_authority_scope",
            expected=sorted(required_exclusions),
            actual=excluded_scope,
        )
    return {
        **WITHHELD_AUTHORITY_STATUSES,
        "withheld_authority_matches_source_exclusions": True,
        "source_excluded_authority_scope": excluded_scope,
        "unapproved_authority_grant_count": 0,
        "execution_authority_included": False,
    }


def build_prior_state(receipt: dict[str, Any]) -> dict[str, Any]:
    state = receipt["decision_state_after_receipt"]
    approved = receipt["approved_scope"]
    return {
        "prior_authority_state_id": "POST_VS1_DIRECTION_AUTHORITY_STATE_APPROVED_NOT_APPLIED",
        "human_decision_recorded": state["human_decision_recorded"],
        "decision_receipt_created": state["decision_receipt_created"],
        "direction_selected": state["direction_selected"],
        "target_family_selected": state["target_family_selected"],
        "first_target_selected": state["first_target_selected"],
        "definition_scope_approved": state["definition_scope_approved"],
        "bounded_construction_scope_approved": state["bounded_construction_scope_approved"],
        "construction_verification_scope_approved": state["construction_verification_scope_approved"],
        "approved_scope_eligible_for_authority_update": approved["approved_scope_eligible_for_authority_update"],
        "approved_scope_applied_to_authority_state": approved["approved_scope_applied_to_authority_state"],
        "authority_state_mutated": state["authority_state_mutated"],
        "authority_update_applied": state["authority_update_applied"],
        "authority_transition_closed": state["authority_transition_closed"],
        "vs2_definition_authority_granted": False,
        "vs2_profile_and_target_freeze_authority_granted": state["vs2_profile_and_target_freeze_authority_granted"],
        "vs2_bounded_construction_authority_granted": state["vs2_bounded_construction_authority_granted"],
        "fixture_construction_authority_granted": state["fixture_construction_authority_granted"],
        "readiness_gate_construction_authority_granted": state["readiness_gate_construction_authority_granted"],
        "construction_package_verification_authority_granted": state["construction_package_verification_authority_granted"],
        "vs2_started": state["vs2_started"],
        "vs2_1_built": state["vs2_1_built"],
        "execution_authorized": state["execution_authorized"],
        "positive_path_execution_authorized": state["positive_path_execution_authorized"],
        "negative_path_execution_authorized": state["negative_path_execution_authorized"],
        "sweep_authorized": state["sweep_authorized"],
        "automatic_rerun_authorized": state["automatic_rerun_authorized"],
        "automatic_radius_renewal_authorized": False,
        "runner_authority_created": state["runner_authority_created"],
        "reusable_schema_authority_granted": False,
        "reusable_move_authority_granted": False,
        "second_target_authority_granted": False,
        "portability_authority_granted": False,
    }


def applied_scope_from_receipt(receipt: dict[str, Any]) -> dict[str, Any]:
    approved = receipt["approved_scope"]
    return {
        "applied_scope_mode": "EXACT_APPROVED_SCOPE",
        "direction_selection_scope": approved["direction_selection_scope"],
        "definition_scope": approved["definition_scope"],
        "bounded_construction_scope": approved["bounded_construction_scope"],
        "construction_verification_scope": approved["construction_verification_scope"],
        "maximum_scope": approved["maximum_scope"],
        "approved_scope_eligible_for_authority_update": True,
        "approved_scope_applied_to_authority_state": True,
        "applied_scope_equals_source_approved_scope": True,
        "applied_scope_is_subset_of_approved_scope": True,
        "applied_scope_exceeds_approved_scope": False,
        "approved_scope_items_omitted": [],
        "unapproved_scope_items_added": [],
        "applied_with_revisions": False,
        "excluded_authority_scope": receipt["excluded_authority_scope"],
    }


def authority_state_after_update() -> dict[str, Any]:
    return {
        "authority_state_id": "POST_VS1_DIRECTION_AUTHORITY_STATE_APPLIED_PENDING_TRANSITION_CLOSURE",
        "human_decision_recorded": True,
        "decision_receipt_created": True,
        "decision_receipt_consumed_for_authority_update": True,
        "direction_selected": True,
        "target_family_selected": True,
        "first_target_selected": True,
        "definition_scope_approved": True,
        "bounded_construction_scope_approved": True,
        "construction_verification_scope_approved": True,
        "approved_scope_eligible_for_authority_update": True,
        "approved_scope_applied_to_authority_state": True,
        "authority_state_mutated": True,
        "authority_update_applied": True,
        "vs2_definition_authority_granted": True,
        "vs2_profile_and_target_freeze_authority_granted": True,
        "vs2_bounded_construction_authority_granted": True,
        "fixture_construction_authority_granted": True,
        "readiness_gate_construction_authority_granted": True,
        "construction_package_verification_authority_granted": True,
        "authority_transition_closed": False,
        "authority_effective_for_vs2_consumption": False,
        "vs2_source_intake_lawful": False,
        "vs2_started": False,
        "vs2_1_built": False,
        "broad_vs2_authority_granted": False,
        "execution_authorized": False,
        "positive_path_execution_authorized": False,
        "negative_path_execution_authorized": False,
        "sweep_authorized": False,
        "automatic_rerun_authorized": False,
        "automatic_radius_renewal_authorized": False,
        "runner_authority_created": False,
        "reusable_schema_authority_granted": False,
        "reusable_move_authority_granted": False,
        "second_target_authority_granted": False,
        "portability_authority_granted": False,
        "transition_state": "AUTHORITY_UPDATE_APPLIED_PENDING_CLOSURE",
        "authority_grants_recorded": True,
        "authority_grants_effective_for_consumption": False,
    }


def validate_authority_boundaries(granted: dict[str, Any], withheld: dict[str, Any], state: dict[str, Any]) -> None:
    required_grants = {
        "VS2_DEFINITION_AUTHORITY": "STOP_POST_VS1_AUTHORITY_UPDATE_DEFINITION_GRANT_MISSING",
        "VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY": "STOP_POST_VS1_AUTHORITY_UPDATE_DEFINITION_GRANT_MISSING",
        "VS2_BOUNDED_CONSTRUCTION_AUTHORITY": "STOP_POST_VS1_AUTHORITY_UPDATE_CONSTRUCTION_GRANT_MISSING",
        "VS2_FIXTURE_CONSTRUCTION_AUTHORITY": "STOP_POST_VS1_AUTHORITY_UPDATE_FIXTURE_GRANT_MISSING",
        "VS2_FIRST_RUN_READINESS_GATE_CONSTRUCTION_AUTHORITY": "STOP_POST_VS1_AUTHORITY_UPDATE_READINESS_GATE_GRANT_MISSING",
        "VS2_CONSTRUCTION_PACKAGE_VERIFICATION_AUTHORITY": "STOP_POST_VS1_AUTHORITY_UPDATE_CONSTRUCTION_VERIFICATION_GRANT_MISSING",
    }
    for key, code in required_grants.items():
        if granted.get(key) != "GRANTED":
            fail(code, field=f"granted_authority_vector.{key}", expected="GRANTED", actual=granted.get(key))
    if withheld["BROAD_OR_GLOBAL_VS2_AUTHORITY"] != "NOT_GRANTED" or state["broad_vs2_authority_granted"] is not False:
        fail("STOP_POST_VS1_AUTHORITY_UPDATE_BROAD_VS2_AUTHORITY_PRESENT", field="broad_vs2_authority", expected=False, actual=True)
    checks = [
        ("execution_authorized", "STOP_POST_VS1_AUTHORITY_UPDATE_EXECUTION_AUTHORITY_PRESENT"),
        ("positive_path_execution_authorized", "STOP_POST_VS1_AUTHORITY_UPDATE_POSITIVE_EXECUTION_AUTHORITY_PRESENT"),
        ("negative_path_execution_authorized", "STOP_POST_VS1_AUTHORITY_UPDATE_NEGATIVE_EXECUTION_AUTHORITY_PRESENT"),
        ("sweep_authorized", "STOP_POST_VS1_AUTHORITY_UPDATE_SWEEP_AUTHORITY_PRESENT"),
        ("automatic_rerun_authorized", "STOP_POST_VS1_AUTHORITY_UPDATE_RERUN_AUTHORITY_PRESENT"),
        ("automatic_radius_renewal_authorized", "STOP_POST_VS1_AUTHORITY_UPDATE_RADIUS_RENEWAL_AUTHORITY_PRESENT"),
        ("runner_authority_created", "STOP_POST_VS1_AUTHORITY_UPDATE_RUNNER_AUTHORITY_PRESENT"),
        ("reusable_schema_authority_granted", "STOP_POST_VS1_AUTHORITY_UPDATE_REUSE_AUTHORITY_PRESENT"),
        ("reusable_move_authority_granted", "STOP_POST_VS1_AUTHORITY_UPDATE_REUSE_AUTHORITY_PRESENT"),
        ("second_target_authority_granted", "STOP_POST_VS1_AUTHORITY_UPDATE_SECOND_TARGET_AUTHORITY_PRESENT"),
        ("portability_authority_granted", "STOP_POST_VS1_AUTHORITY_UPDATE_PORTABILITY_AUTHORITY_PRESENT"),
    ]
    for field, code in checks:
        if state[field] is not False:
            fail(code, field=f"authority_state_after_update.{field}", expected=False, actual=state[field])
    if state["authority_transition_closed"] is not False:
        fail("STOP_POST_VS1_AUTHORITY_UPDATE_TRANSITION_AUTO_CLOSED", field="authority_transition_closed", expected=False, actual=True)
    if state["authority_effective_for_vs2_consumption"] is not False or state["vs2_source_intake_lawful"] is not False:
        fail("STOP_POST_VS1_AUTHORITY_UPDATE_AUTHORITY_PREMATURELY_EFFECTIVE", field="authority_effective_for_vs2_consumption", expected=False, actual=True)
    if state["vs2_started"] is not False:
        fail("STOP_POST_VS1_AUTHORITY_UPDATE_VS2_AUTO_STARTED", field="vs2_started", expected=False, actual=True)
    if state["vs2_1_built"] is not False:
        fail("STOP_POST_VS1_AUTHORITY_UPDATE_VS2_1_AUTO_BUILT", field="vs2_1_built", expected=False, actual=True)


def build_update(root: Path, receipt: dict[str, Any], receipt_content_sha: str) -> dict[str, Any]:
    validate_receipt_identity(receipt)
    validate_receipt_binding(receipt)
    validate_decision_package(receipt)
    validate_selection(receipt)
    validate_approval(receipt)

    selection = receipt["decision_selection"]
    source_receipt_binding = {
        "source_decision_receipt_artifact_id": SOURCE_RECEIPT_ARTIFACT_ID,
        "source_decision_receipt_path": SOURCE_RECEIPT_PATH,
        "source_decision_receipt_commit_sha": SOURCE_RECEIPT_COMMIT,
        "source_decision_receipt_content_sha256": receipt_content_sha,
        "source_decision_receipt_canonical_sha256": SOURCE_RECEIPT_CANONICAL_SHA256,
        "source_decision_receipt_gate": SOURCE_RECEIPT_GATE,
        "source_decision_receipt_terminal_transition": SOURCE_RECEIPT_TERMINAL,
        "source_decision_package_sha256": SOURCE_DECISION_PACKAGE_SHA256,
        "source_receipt_authority_update_applied": False,
        "source_receipt_authority_transition_closed": False,
        "source_receipt_committed_bytes_verified": True,
        "source_receipt_worktree_matches_commit": True,
        "latest_file_resolution_used": False,
        "mtime_resolution_used": False,
        "directory_scan_authority_used": False,
        "baseline_share_used_as_source_authority": False,
    }
    source_package_binding = {
        "source_decision_package_sha256": SOURCE_DECISION_PACKAGE_SHA256,
        "source_decision_package_hash_unchanged": True,
        "source_decision_package_basis_receipt_sha256": SOURCE_RECEIPT_CANONICAL_SHA256,
        "source_decision_surface_commit_sha": SOURCE_SURFACE_COMMIT,
    }
    invocation = {
        "invocation_actor_class": "HUMAN_OPERATOR",
        "invocation_actor_identity": "HUMAN_OPERATOR_CURRENT_MATRIXLAB_SESSION",
        "invocation_source_kind": "EXPLICIT_INTERACTIVE_USER_INSTRUCTION",
        "invocation_statement_exact": "proceed",
        "invocation_interpretation": "APPLY_COMMITTED_POST_VS1_EXACT_APPROVED_SCOPE",
        "invocation_date_local": "2026-07-11",
        "invocation_timezone": "Europe/Lisbon",
        "invocation_time_precision": "DATE_AND_SESSION_SEQUENCE_ONLY",
        "invocation_sequence_anchor": "AFTER_COMMIT_3DC012D9D72201D2BAF4C7D31D7545A68659CE9D",
        "invocation_statement_sha256": sha256_bytes(b"proceed"),
        "invocation_adds_authority_scope": False,
        "invocation_revises_human_decision": False,
        "invocation_selects_application_mode_only": True,
        "application_mode": APPLICATION_MODE,
    }
    prior = build_prior_state(receipt)
    applied_scope = applied_scope_from_receipt(receipt)
    approved_lists = {key: receipt["approved_scope"][key] for key in ["direction_selection_scope", "definition_scope", "bounded_construction_scope", "construction_verification_scope", "maximum_scope"]}
    applied_lists = {key: applied_scope[key] for key in approved_lists}
    if applied_lists != approved_lists:
        fail("STOP_POST_VS1_AUTHORITY_UPDATE_APPLIED_SCOPE_OMITS_APPROVED_SCOPE", field="applied_scope", expected=approved_lists, actual=applied_lists)
    if applied_scope["unapproved_scope_items_added"]:
        fail("STOP_POST_VS1_AUTHORITY_UPDATE_APPLIED_SCOPE_EXCEEDS_APPROVED_SCOPE", field="unapproved_scope_items_added", expected=[], actual=applied_scope["unapproved_scope_items_added"])
    granted = granted_authority_vector()
    withheld = withheld_authority_vector(receipt["excluded_authority_scope"])
    consumption = {
        "decision_receipt_consumed_for_authority_update": True,
        "decision_receipt_consumption_count": 1,
        "decision_receipt_reusable_for_second_authority_update": False,
        "same_receipt_may_apply_again": False,
        "authority_update_idempotent_reapplication_allowed": False,
        "source_receipt_rewritten": False,
        "receipt_consumed_as_authority_update_basis_not_rewritten": True,
    }
    state_after = authority_state_after_update()
    transition = {
        "transition_closure_required": True,
        "transition_closure_created_by_this_unit": False,
        "transition_closure_status": "PENDING",
        "next_unit": "POST_VS1_DIRECTION_TRANSITION_CLOSURE_V0_PENDING",
        "expected_later_closure_status": (
            "POST_VS1_DIRECTION_TRANSITION_PASS_VS2_DEFINITION_AND_BOUNDED_CONSTRUCTION_AUTHORITY_GRANTED_EXECUTION_AUTHORITY_ABSENT"
        ),
        "until_closure_passes": [
            "VS2 source intake is not lawful",
            "VS2.1 is not lawful",
            "no grant may be consumed",
            "no construction may begin",
        ],
        "authority_update_applied_does_not_close_authority_transition": True,
    }
    validate_authority_boundaries(granted, withheld, state_after)
    payload = {
        "source_decision_receipt_binding": source_receipt_binding,
        "source_decision_package_binding": source_package_binding,
        "authority_update_invocation_evidence": invocation,
        "prior_authority_state": prior,
        "applied_authority_scope": applied_scope,
        "granted_authority_vector": granted,
        "withheld_authority_vector": withheld,
        "decision_receipt_consumption": consumption,
        "authority_state_after_update": state_after,
        "transition_closure_requirement": transition,
    }
    if list(payload.keys()) != AUTHORITY_UPDATE_BOUND_SECTIONS:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_HASH_MISMATCH",
            field="authority_update_payload",
            expected=AUTHORITY_UPDATE_BOUND_SECTIONS,
            actual=list(payload.keys()),
        )
    update_hash = canonical_hash(payload)
    update = {
        "schema_version": SCHEMA_VERSION,
        "artifact_id": ARTIFACT_ID,
        "object_id": OBJECT_ID,
        "object_role": OBJECT_ROLE,
        "authority_update_status": AUTHORITY_UPDATE_STATUS,
        "source_decision_receipt_binding": source_receipt_binding,
        "source_decision_package_binding": source_package_binding,
        "authority_update_invocation_evidence": invocation,
        "prior_authority_state": prior,
        "applied_authority_scope": applied_scope,
        "granted_authority_vector": granted,
        "withheld_authority_vector": withheld,
        "decision_receipt_consumption": consumption,
        "authority_state_after_update": state_after,
        "transition_closure_requirement": transition,
        "authority_update_binding": {
            "canonicalization": CANONICALIZATION_CONTRACT,
            "canonicalization_contract": CANONICALIZATION_CONTRACT,
            "bound_sections": AUTHORITY_UPDATE_BOUND_SECTIONS,
            "authority_update_payload": payload,
            "authority_update_sha256": update_hash,
            "generated_at_metadata_excluded_from_hash": True,
            "volatile_filesystem_metadata_excluded_from_hash": True,
            "commit_created_fields_excluded_from_hash": True,
            "future_transition_closure_fields_excluded_from_hash": True,
            "future_vs2_artifact_identities_excluded_from_hash": True,
            "transition_closure_must_bind_authority_update_sha256": True,
            "vs2_source_intake_must_bind_transition_closure": True,
        },
        "authority_update_checks": [
            {"check_id": check, "check_result": check, "status": "PASS"}
            for check in AUTHORITY_UPDATE_CHECKS
        ],
        "authority_update_gate": AUTHORITY_UPDATE_GATE,
        "terminal_transition": {
            "transition": TERMINAL_TRANSITION,
            "consumes_decision_receipt": True,
            "applies_authority_update": True,
            "mutates_authority_state": True,
            "grants_bounded_vs2_definition_authority": True,
            "grants_bounded_vs2_construction_authority": True,
            "grants_fixture_construction_authority": True,
            "grants_readiness_gate_construction_authority": True,
            "grants_construction_verification_authority": True,
            "closes_authority_transition": False,
            "makes_authority_effective_for_vs2_consumption": False,
            "starts_vs2": False,
            "builds_vs2_1": False,
            "authorizes_execution": False,
            "authorizes_positive_path_execution": False,
            "authorizes_negative_path_execution": False,
            "authorizes_sweep": False,
            "authorizes_rerun": False,
            "authorizes_radius_renewal": False,
            "creates_runner_authority": False,
        },
        "evidence_yield": {
            "branch": "CONFIRMATION_YIELD",
            "source_receipt_verified": True,
            "authority_update_hash_bound": True,
            "authority_transition_closure_still_required": True,
        },
        "non_claims": [
            "This update does not close the authority transition.",
            "This update does not make authority effective for VS2 consumption.",
            "This update does not start VS2 or build VS2.1.",
            "This update does not construct or verify kernel artifacts.",
            "This update does not authorize execution, sweeps, reruns, or runner authority.",
        ],
        "failures": [],
    }
    validate_update(update, receipt)
    return update


def validate_update(update: dict[str, Any], receipt: dict[str, Any]) -> None:
    binding = update["authority_update_binding"]
    if list(binding["authority_update_payload"].keys()) != binding["bound_sections"]:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_HASH_MISMATCH",
            field="authority_update_binding.bound_sections",
            expected=binding["bound_sections"],
            actual=list(binding["authority_update_payload"].keys()),
        )
    recomputed = canonical_hash(binding["authority_update_payload"])
    if recomputed != binding["authority_update_sha256"]:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_HASH_MISMATCH",
            field="authority_update_binding.authority_update_sha256",
            expected=recomputed,
            actual=binding["authority_update_sha256"],
        )
    if update["decision_receipt_consumption"]["decision_receipt_consumption_count"] != 1:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_DUPLICATE_APPLICATION",
            field="decision_receipt_consumption_count",
            expected=1,
            actual=update["decision_receipt_consumption"]["decision_receipt_consumption_count"],
        )
    if update["decision_receipt_consumption"]["same_receipt_may_apply_again"] is not False:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_REAPPLICATION_ATTEMPT",
            field="same_receipt_may_apply_again",
            expected=False,
            actual=True,
        )
    if update["source_decision_receipt_binding"]["source_receipt_authority_update_applied"] is not False:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_RECEIPT_ALREADY_CONSUMED",
            field="source_receipt_authority_update_applied",
            expected=False,
            actual=True,
        )
    if update["applied_authority_scope"]["excluded_authority_scope"] != receipt["excluded_authority_scope"]:
        fail(
            "STOP_POST_VS1_AUTHORITY_UPDATE_EXCLUDED_SCOPE_NOT_PRESERVED",
            field="applied_authority_scope.excluded_authority_scope",
            expected=receipt["excluded_authority_scope"],
            actual=update["applied_authority_scope"]["excluded_authority_scope"],
        )


def build_markdown(update: dict[str, Any]) -> str:
    selection = update["authority_update_binding"]["authority_update_payload"]["source_decision_receipt_binding"]
    source_package = update["source_decision_package_binding"]
    binding = update["authority_update_binding"]
    state = update["authority_state_after_update"]
    receipt_selection = update["authority_update_binding"]["authority_update_payload"]
    return f"""# Post-VS1 Direction Authority Update v0

## Source

Source decision receipt:
post_vs1_direction_decision_receipt_v0

Source receipt commit:
{selection["source_decision_receipt_commit_sha"]}

Source receipt hash:
{selection["source_decision_receipt_canonical_sha256"]}

## Source binding

Source decision receipt commit:
{selection["source_decision_receipt_commit_sha"]}

Source decision receipt hash:
{selection["source_decision_receipt_canonical_sha256"]}

Source decision package hash:
{source_package["source_decision_package_sha256"]}

Authority update hash:
{binding["authority_update_sha256"]}

Accepted direction:
{DIRECTION_ID}

Accepted target family:
{TARGET_FAMILY}

Accepted first target:
{FIRST_TARGET}

Application mode:
{APPLICATION_MODE}

## Granted

- VS2 profile and target freeze authority
- VS2 bounded construction authority
- fixture construction authority
- first-run readiness-gate construction authority
- construction-package verification authority

## Explicitly not granted

- broad or global VS2 authority
- kernel execution authority
- positive-path execution authority
- negative-path execution authority
- sweep execution authority
- automatic rerun authority
- automatic radius renewal authority
- runner authority
- reuse authority
- second-target authority
- portability authority

## Current state

Human decision receipt consumed once.
Approved scope applied to authority state.
Authority update applied.
Authority transition not closed.
Authority not yet effective for VS2 consumption.
VS2 source intake not yet lawful.
VS2 not started.
VS2.1 not built.
No construction performed.
Execution not authorized.
Sweeps not authorized.
Runner authority not created.

## Binding

- authority update hash: {update["authority_update_binding"]["authority_update_sha256"]}
- authority transition closed: {str(state["authority_transition_closed"]).lower()}
- authority effective for VS2 consumption: {str(state["authority_effective_for_vs2_consumption"]).lower()}
- execution authorized: {str(state["execution_authorized"]).lower()}

## Next

POST_VS1_DIRECTION_TRANSITION_CLOSURE_V0_PENDING
"""


def emit_success(update: dict[str, Any]) -> None:
    state = update["authority_state_after_update"]
    selection = update["authority_update_binding"]["authority_update_payload"]["source_decision_receipt_binding"]
    binding = update["authority_update_binding"]
    applied = update["applied_authority_scope"]
    consumption = update["decision_receipt_consumption"]
    print("BUILD_POST_VS1_DIRECTION_AUTHORITY_UPDATE_V0_COMPLETE")
    print()
    print(f"artifact_id={ARTIFACT_ID}")
    print(f"schema_version={SCHEMA_VERSION}")
    print(f"object_id={OBJECT_ID}")
    print(f"object_role={OBJECT_ROLE}")
    print()
    print(f"source_decision_receipt_commit_sha={SOURCE_RECEIPT_COMMIT}")
    print(f"source_decision_receipt_sha256={SOURCE_RECEIPT_CANONICAL_SHA256}")
    print("source_decision_receipt_hash_recomputes=true")
    print("source_decision_receipt_committed_bytes_verified=true")
    print()
    print(f"source_decision_package_sha256={SOURCE_DECISION_PACKAGE_SHA256}")
    print("source_decision_package_hash_unchanged=true")
    print()
    print(f"accepted_option={ACCEPTED_OPTION}")
    print(f"decision_mode={DECISION_MODE}")
    print(f"application_mode={APPLICATION_MODE}")
    print()
    print(f"selected_direction={DIRECTION_ID}")
    print(f"selected_target_family={TARGET_FAMILY}")
    print(f"selected_first_target={FIRST_TARGET}")
    print()
    print(f"applied_scope_equals_source_approved_scope={str(applied['applied_scope_equals_source_approved_scope']).lower()}")
    print(f"applied_scope_exceeds_approved_scope={str(applied['applied_scope_exceeds_approved_scope']).lower()}")
    print(f"unapproved_scope_items_added_count={len(applied['unapproved_scope_items_added'])}")
    print()
    print(f"decision_receipt_consumed_for_authority_update={str(consumption['decision_receipt_consumed_for_authority_update']).lower()}")
    print(f"decision_receipt_consumption_count={consumption['decision_receipt_consumption_count']}")
    print(f"same_receipt_may_apply_again={str(consumption['same_receipt_may_apply_again']).lower()}")
    print()
    print("authority_state_mutated=true")
    print("authority_update_applied=true")
    print("approved_scope_applied_to_authority_state=true")
    print()
    for key in [
        "vs2_definition_authority_granted",
        "vs2_profile_and_target_freeze_authority_granted",
        "vs2_bounded_construction_authority_granted",
        "fixture_construction_authority_granted",
        "readiness_gate_construction_authority_granted",
        "construction_package_verification_authority_granted",
    ]:
        print(f"{key}={str(state[key]).lower()}")
    print()
    print("authority_transition_closed=false")
    print("authority_effective_for_vs2_consumption=false")
    print("vs2_source_intake_lawful=false")
    print()
    print("broad_vs2_authority_granted=false")
    print()
    for key in [
        "execution_authorized",
        "positive_path_execution_authorized",
        "negative_path_execution_authorized",
        "sweep_authorized",
        "automatic_rerun_authorized",
        "automatic_radius_renewal_authorized",
        "runner_authority_created",
        "reusable_schema_authority_granted",
        "reusable_move_authority_granted",
        "second_target_authority_granted",
        "portability_authority_granted",
        "vs2_started",
        "vs2_1_built",
    ]:
        print(f"{key}={str(state[key]).lower()}")
    print()
    print("authority_update_hash_present=true")
    print(f"authority_update_hash_recomputes={str(canonical_hash(binding['authority_update_payload']) == binding['authority_update_sha256']).lower()}")
    print()
    print(f"authority_update_gate={AUTHORITY_UPDATE_GATE}")
    print("evidence_yield_branch=CONFIRMATION_YIELD")
    print()
    print("source_files_unchanged=true")
    print("forbidden_output_count=0")
    print()
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode != 0
    print(f"staged_changes_present={str(staged).lower()}")
    print("commit_created=false")
    print("push_executed=false")
    print()
    print(f"terminal_transition={TERMINAL_TRANSITION}")


def emit_failure(exc: AuthorityUpdateFailure) -> None:
    print("BUILD_POST_VS1_DIRECTION_AUTHORITY_UPDATE_V0_FAILED")
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
    before = capture_source_hashes(root)
    committed_receipt, receipt_content_sha = verify_committed_receipt_bytes(root)
    receipt = json.loads(committed_receipt.decode("utf-8"))
    update = build_update(root, receipt, receipt_content_sha)
    (root / OUTPUT_JSON).parent.mkdir(parents=True, exist_ok=True)
    (root / OUTPUT_JSON).write_text(json.dumps(update, indent=2) + "\n", encoding="utf-8")
    (root / OUTPUT_MD).write_text(build_markdown(update), encoding="utf-8")
    after = capture_source_hashes(root)
    validate_source_preservation(before, after)
    validate_dirty_scope(root)
    ensure_no_forbidden_artifacts(root)
    emit_success(update)
    return 0


def main() -> int:
    try:
        return generate()
    except AuthorityUpdateFailure as exc:
        emit_failure(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
