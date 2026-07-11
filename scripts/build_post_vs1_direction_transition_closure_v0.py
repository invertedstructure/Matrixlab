#!/usr/bin/env python3
"""Build POST-VS1 direction transition closure v0."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


EXPECTED_BRANCH = "master"
EXPECTED_HEAD = "ebeb85a867b559df9f004ce8f4495e1581e79d14"
SOURCE_RECEIPT_COMMIT = "3dc012d9d72201d2baf4c7d31d7545a68659ce9d"
SOURCE_AUTHORITY_UPDATE_CANONICAL_SHA256 = (
    "0eac680fdfa0052696bc0360aa5278b9ce06e95b78eaf91ed418cb9f578ab60d"
)
SOURCE_RECEIPT_CANONICAL_SHA256 = (
    "19defc100428931ed455e4d2a64697bb9d886b11b856ececb0da6743c94f0dfe"
)
SOURCE_DECISION_PACKAGE_SHA256 = (
    "e9e4143ad2efdd285fe9e598e50d965d82057f7a8d6ccc4c52478a596d6b788b"
)

SCHEMA_VERSION = "matrixlabs_post_vs1_direction_transition_closure_v0"
ARTIFACT_ID = "post_vs1_direction_transition_closure_v0"
OBJECT_ID = "POST_VS1_DIRECTION_TRANSITION_CLOSURE"
OBJECT_ROLE = "AUTHORITY_TRANSITION_EFFECTIVITY_CLOSURE_ONLY"
CLOSURE_STATUS = (
    "POST_VS1_DIRECTION_TRANSITION_PASS_VS2_DEFINITION_AND_BOUNDED_CONSTRUCTION_"
    "AUTHORITY_GRANTED_EXECUTION_AUTHORITY_ABSENT"
)
CLOSURE_GATE = (
    "POST_VS1_DIRECTION_TRANSITION_CLOSURE_PASS_AUTHORITY_EFFECTIVE_FOR_VS2_"
    "SOURCE_INTAKE_EXECUTION_AUTHORITY_ABSENT"
)
TERMINAL_TRANSITION = "ADVANCE(VS2_1_POST_VS1_SOURCE_INTAKE_PENDING)"

SOURCE_AUTHORITY_UPDATE_PATH = (
    "docs/matrixlabs/post_vs1/post_vs1_direction_authority_update_v0.json"
)
SOURCE_AUTHORITY_UPDATE_MD_PATH = (
    "docs/matrixlabs/post_vs1/post_vs1_direction_authority_update_v0.md"
)
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
OUTPUT_JSON = "docs/matrixlabs/post_vs1/post_vs1_direction_transition_closure_v0.json"
OUTPUT_MD = "docs/matrixlabs/post_vs1/post_vs1_direction_transition_closure_v0.md"

SOURCE_AUTHORITY_UPDATE_SCHEMA = "matrixlabs_post_vs1_direction_authority_update_v0"
SOURCE_AUTHORITY_UPDATE_ARTIFACT_ID = "post_vs1_direction_authority_update_v0"
SOURCE_AUTHORITY_UPDATE_OBJECT_ID = "POST_VS1_DIRECTION_AUTHORITY_UPDATE"
SOURCE_AUTHORITY_UPDATE_OBJECT_ROLE = "BOUNDED_AUTHORITY_STATE_UPDATE_ONLY"
SOURCE_AUTHORITY_UPDATE_STATUS = "APPROVED_SCOPE_APPLIED_PENDING_TRANSITION_CLOSURE"
SOURCE_AUTHORITY_UPDATE_GATE = (
    "POST_VS1_DIRECTION_AUTHORITY_UPDATE_PASS_APPROVED_SCOPE_APPLIED_EXECUTION_AUTHORITY_ABSENT"
)
SOURCE_AUTHORITY_UPDATE_TERMINAL = (
    "ADVANCE(POST_VS1_DIRECTION_TRANSITION_CLOSURE_V0_PENDING)"
)

CANONICALIZATION_CONTRACT = "MATRIXLAB_CANONICAL_JSON_V0"
APPLICATION_MODE = "APPLY_EXACT_APPROVED_SCOPE"
DIRECTION_ID = "FIRST_SWEEP_CAPABLE_KERNEL_V0"
TARGET_FAMILY = "BOUNDED_CONTRACT_CONVERGENCE"
FIRST_TARGET = "TYPED_STATE_CONTRACT_CONVERGENCE_V0"
GRANT_EFFECTIVITY_CONDITION = "POST_VS1_DIRECTION_TRANSITION_CLOSURE_PASS_REQUIRED"

EXPECTED_GRANT_IDS = [
    "VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY",
    "VS2_BOUNDED_CONSTRUCTION_AUTHORITY",
    "VS2_FIXTURE_CONSTRUCTION_AUTHORITY",
    "VS2_FIRST_RUN_READINESS_GATE_CONSTRUCTION_AUTHORITY",
    "VS2_CONSTRUCTION_PACKAGE_VERIFICATION_AUTHORITY",
]

TRANSITION_CLOSURE_BOUND_SECTIONS = [
    "source_authority_update_binding",
    "source_decision_chain_binding",
    "closure_invocation_evidence",
    "pre_closure_authority_state",
    "grant_effectivity_audit",
    "withheld_authority_audit",
    "authority_update_consumption",
    "post_closure_authority_state",
    "downstream_vs2_boundary",
]

PRESERVED_SOURCE_PATHS = [
    SOURCE_AUTHORITY_UPDATE_PATH,
    SOURCE_AUTHORITY_UPDATE_MD_PATH,
    SOURCE_RECEIPT_PATH,
    SOURCE_RECEIPT_MD_PATH,
    SOURCE_SURFACE_PATH,
    SOURCE_SURFACE_MD_PATH,
    PROPOSAL_SOURCE_PATH,
    PROPOSAL_SOURCE_SIDECAR_PATH,
    VS1_CLOSURE_PATH,
    VS1_MAP_PATH,
]

FORBIDDEN_OUTPUTS = [
    "docs/matrixlabs/phase_vs2",
    "docs/matrixlabs/runner",
    "docs/matrixlabs/runtime",
    "docs/matrixlabs/move_space",
    "docs/matrixlabs/micro_sweeps",
]

TRANSITION_CLOSURE_CHECKS = [
    "POST_VS1_TRANSITION_CLOSURE_SOURCE_AUTHORITY_UPDATE_COMMITTED_BYTES_VERIFIED",
    "POST_VS1_TRANSITION_CLOSURE_SOURCE_AUTHORITY_UPDATE_CANONICAL_HASH_VERIFIED",
    "POST_VS1_TRANSITION_CLOSURE_SOURCE_DECISION_CHAIN_VERIFIED",
    "POST_VS1_TRANSITION_CLOSURE_EXACT_APPLIED_SCOPE_VERIFIED",
    "POST_VS1_TRANSITION_CLOSURE_REQUIRED_AND_PENDING_VERIFIED",
    "POST_VS1_TRANSITION_CLOSURE_FIVE_GRANT_RECORDS_VERIFIED",
    "POST_VS1_TRANSITION_CLOSURE_GRANT_SCOPE_IDENTITY_VERIFIED",
    "POST_VS1_TRANSITION_CLOSURE_GRANT_EFFECTIVITY_CONDITIONS_VERIFIED",
    "POST_VS1_TRANSITION_CLOSURE_GRANTS_MADE_EFFECTIVE",
    "POST_VS1_TRANSITION_CLOSURE_NO_GRANT_CONSUMED",
    "POST_VS1_TRANSITION_CLOSURE_WITHHELD_AUTHORITY_PRESERVED",
    "POST_VS1_TRANSITION_CLOSURE_EXECUTION_AUTHORITY_ABSENT",
    "POST_VS1_TRANSITION_CLOSURE_SWEEP_AUTHORITY_ABSENT",
    "POST_VS1_TRANSITION_CLOSURE_RERUN_AUTHORITY_ABSENT",
    "POST_VS1_TRANSITION_CLOSURE_RADIUS_RENEWAL_AUTHORITY_ABSENT",
    "POST_VS1_TRANSITION_CLOSURE_RUNNER_AUTHORITY_ABSENT",
    "POST_VS1_TRANSITION_CLOSURE_REUSE_AUTHORITY_ABSENT",
    "POST_VS1_TRANSITION_CLOSURE_SECOND_TARGET_AUTHORITY_ABSENT",
    "POST_VS1_TRANSITION_CLOSURE_PORTABILITY_AUTHORITY_ABSENT",
    "POST_VS1_TRANSITION_CLOSURE_VS2_SOURCE_INTAKE_NOW_LAWFUL",
    "POST_VS1_TRANSITION_CLOSURE_VS2_NOT_STARTED",
    "POST_VS1_TRANSITION_CLOSURE_VS2_1_NOT_BUILT",
    "POST_VS1_TRANSITION_CLOSURE_NO_CONSTRUCTION_PERFORMED",
    "POST_VS1_TRANSITION_CLOSURE_CANONICAL_BINDING_PASS",
]

REQUIRED_WITHHELD_STATUSES = {
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


class TransitionClosureFailure(RuntimeError):
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
    raise TransitionClosureFailure(code, field=field, expected=expected, actual=actual)


def run_git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def detect_repo_root(start: Path) -> Path:
    try:
        return Path(run_git(start, "rev-parse", "--show-toplevel"))
    except subprocess.CalledProcessError:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_UNEXPECTED_HEAD",
            field="repo",
            expected="/home/asd/projects/matrixlab",
            actual=str(start),
        )


def require_repo_context(root: Path) -> None:
    branch = run_git(root, "branch", "--show-current")
    head = run_git(root, "rev-parse", "HEAD")
    if branch != EXPECTED_BRANCH:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_UNEXPECTED_HEAD",
            field="branch",
            expected=EXPECTED_BRANCH,
            actual=branch,
        )
    if head != EXPECTED_HEAD:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_UNEXPECTED_HEAD",
            field="HEAD",
            expected=EXPECTED_HEAD,
            actual=head,
        )


def validate_dirty_scope(root: Path) -> None:
    allowed_exact = {
        "scripts/build_post_vs1_direction_transition_closure_v0.py",
        "scripts/build_baseline_share_v0.py",
        OUTPUT_JSON,
        OUTPUT_MD,
        "baseline_share/COMMIT_CONTEXT.md",
        "baseline_share/CURRENT_STATE.md",
        "baseline_share/MANIFEST.json",
        "baseline_share/RECEIPT_POINTERS.md",
    }

    def porcelain_paths(line: str) -> list[str]:
        path_part = line[3:] if len(line) > 3 and line[2] == " " else line[2:].strip()
        return [part.strip() for part in path_part.split(" -> ") if part.strip()]

    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=root,
        text=True,
    ).splitlines()
    unexpected = [
        line
        for line in status
        if not all(
            path in allowed_exact or path.startswith("discussion_packets/")
            for path in porcelain_paths(line)
        )
    ]
    if unexpected:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_DOWNSTREAM_ARTIFACT_CREATED",
            field="git_status",
            expected=sorted(allowed_exact),
            actual=unexpected,
        )


def ensure_no_forbidden_outputs(root: Path) -> None:
    present = [path for path in FORBIDDEN_OUTPUTS if (root / path).exists()]
    if present:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_DOWNSTREAM_ARTIFACT_CREATED",
            field="forbidden_outputs",
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
            "STOP_POST_VS1_TRANSITION_CLOSURE_SOURCE_AUTHORITY_UPDATE_MISSING",
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
            "STOP_POST_VS1_TRANSITION_CLOSURE_SOURCE_AUTHORITY_UPDATE_NOT_COMMITTED",
            field=rel_path,
            expected=f"{commit}:{rel_path}",
            actual="not_committed",
        )


def verify_committed_authority_update_bytes(root: Path) -> tuple[dict[str, Any], str]:
    path = root / SOURCE_AUTHORITY_UPDATE_PATH
    if not path.exists():
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_SOURCE_AUTHORITY_UPDATE_MISSING",
            field=SOURCE_AUTHORITY_UPDATE_PATH,
            expected="present",
            actual="missing",
        )
    committed = committed_file_bytes(root, EXPECTED_HEAD, SOURCE_AUTHORITY_UPDATE_PATH)
    worktree = path.read_bytes()
    if committed != worktree:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_SOURCE_AUTHORITY_UPDATE_WORKTREE_DIVERGENCE",
            field=SOURCE_AUTHORITY_UPDATE_PATH,
            expected=sha256_bytes(committed),
            actual=sha256_bytes(worktree),
        )
    return json.loads(committed.decode("utf-8")), sha256_bytes(committed)


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
            "STOP_POST_VS1_TRANSITION_CLOSURE_SOURCE_AUTHORITY_UPDATE_REWRITE",
            field="source_hashes",
            expected=before,
            actual=changed,
        )


def validate_authority_update_identity(update: dict[str, Any]) -> None:
    expected = {
        "schema_version": SOURCE_AUTHORITY_UPDATE_SCHEMA,
        "artifact_id": SOURCE_AUTHORITY_UPDATE_ARTIFACT_ID,
        "object_id": SOURCE_AUTHORITY_UPDATE_OBJECT_ID,
        "object_role": SOURCE_AUTHORITY_UPDATE_OBJECT_ROLE,
        "authority_update_status": SOURCE_AUTHORITY_UPDATE_STATUS,
        "authority_update_gate": SOURCE_AUTHORITY_UPDATE_GATE,
    }
    for key, value in expected.items():
        if update.get(key) != value:
            fail(
                "STOP_POST_VS1_TRANSITION_CLOSURE_SOURCE_AUTHORITY_UPDATE_IDENTITY_MISMATCH",
                field=key,
                expected=value,
                actual=update.get(key),
            )
    terminal = update.get("terminal_transition", {}).get("transition")
    if terminal != SOURCE_AUTHORITY_UPDATE_TERMINAL:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_AUTHORITY_UPDATE_TERMINAL_MISMATCH",
            field="terminal_transition.transition",
            expected=SOURCE_AUTHORITY_UPDATE_TERMINAL,
            actual=terminal,
        )


def validate_authority_update_binding(update: dict[str, Any]) -> None:
    binding = update.get("authority_update_binding", {})
    if binding.get("canonicalization") != CANONICALIZATION_CONTRACT:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_CANONICALIZATION_MISMATCH",
            field="authority_update_binding.canonicalization",
            expected=CANONICALIZATION_CONTRACT,
            actual=binding.get("canonicalization"),
        )
    if binding.get("canonicalization_contract") != CANONICALIZATION_CONTRACT:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_CANONICALIZATION_MISMATCH",
            field="authority_update_binding.canonicalization_contract",
            expected=CANONICALIZATION_CONTRACT,
            actual=binding.get("canonicalization_contract"),
        )
    payload = binding.get("authority_update_payload", {})
    if list(payload.keys()) != binding.get("bound_sections"):
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_BOUND_SECTION_MISMATCH",
            field="authority_update_binding.bound_sections",
            expected=binding.get("bound_sections"),
            actual=list(payload.keys()),
        )
    recomputed = canonical_hash(payload)
    if binding.get("authority_update_sha256") != SOURCE_AUTHORITY_UPDATE_CANONICAL_SHA256:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_AUTHORITY_UPDATE_HASH_MISMATCH",
            field="authority_update_binding.authority_update_sha256",
            expected=SOURCE_AUTHORITY_UPDATE_CANONICAL_SHA256,
            actual=binding.get("authority_update_sha256"),
        )
    if recomputed != SOURCE_AUTHORITY_UPDATE_CANONICAL_SHA256:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_AUTHORITY_UPDATE_HASH_MISMATCH",
            field="authority_update_binding.authority_update_payload",
            expected=SOURCE_AUTHORITY_UPDATE_CANONICAL_SHA256,
            actual=recomputed,
        )
    if binding.get("transition_closure_must_bind_authority_update_sha256") is not True:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_BINDING_REQUIREMENT_MISSING",
            field="transition_closure_must_bind_authority_update_sha256",
            expected=True,
            actual=binding.get("transition_closure_must_bind_authority_update_sha256"),
        )
    if binding.get("vs2_source_intake_must_bind_transition_closure") is not True:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_BINDING_REQUIREMENT_MISSING",
            field="vs2_source_intake_must_bind_transition_closure",
            expected=True,
            actual=binding.get("vs2_source_intake_must_bind_transition_closure"),
        )


def validate_source_chain(update: dict[str, Any]) -> None:
    source_receipt = update.get("source_decision_receipt_binding", {})
    source_package = update.get("source_decision_package_binding", {})
    if source_receipt.get("source_decision_receipt_commit_sha") != SOURCE_RECEIPT_COMMIT:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_SOURCE_RECEIPT_BINDING_MISMATCH",
            field="source_decision_receipt_commit_sha",
            expected=SOURCE_RECEIPT_COMMIT,
            actual=source_receipt.get("source_decision_receipt_commit_sha"),
        )
    if source_receipt.get("source_decision_receipt_canonical_sha256") != SOURCE_RECEIPT_CANONICAL_SHA256:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_SOURCE_RECEIPT_BINDING_MISMATCH",
            field="source_decision_receipt_canonical_sha256",
            expected=SOURCE_RECEIPT_CANONICAL_SHA256,
            actual=source_receipt.get("source_decision_receipt_canonical_sha256"),
        )
    for field, actual in {
        "source_decision_receipt_binding.source_decision_package_sha256": source_receipt.get(
            "source_decision_package_sha256"
        ),
        "source_decision_package_binding.source_decision_package_sha256": source_package.get(
            "source_decision_package_sha256"
        ),
    }.items():
        if actual != SOURCE_DECISION_PACKAGE_SHA256:
            fail(
                "STOP_POST_VS1_TRANSITION_CLOSURE_SOURCE_PACKAGE_BINDING_MISMATCH",
                field=field,
                expected=SOURCE_DECISION_PACKAGE_SHA256,
                actual=actual,
            )


def validate_applied_scope(update: dict[str, Any]) -> None:
    applied = update.get("applied_authority_scope", {})
    expected = {
        "applied_scope_mode": "EXACT_APPROVED_SCOPE",
        "approved_scope_eligible_for_authority_update": True,
        "approved_scope_applied_to_authority_state": True,
        "applied_scope_equals_source_approved_scope": True,
        "applied_scope_exceeds_approved_scope": False,
        "approved_scope_items_omitted": [],
        "unapproved_scope_items_added": [],
    }
    for key, value in expected.items():
        if applied.get(key) != value:
            fail(
                "STOP_POST_VS1_TRANSITION_CLOSURE_APPLIED_SCOPE_MISMATCH",
                field=f"applied_authority_scope.{key}",
                expected=value,
                actual=applied.get(key),
            )


def validate_pre_closure_state(update: dict[str, Any]) -> None:
    state = update.get("authority_state_after_update", {})
    required_true = {
        "authority_state_mutated",
        "authority_update_applied",
        "approved_scope_applied_to_authority_state",
        "vs2_definition_authority_granted",
        "vs2_profile_and_target_freeze_authority_granted",
        "vs2_bounded_construction_authority_granted",
        "fixture_construction_authority_granted",
        "readiness_gate_construction_authority_granted",
        "construction_package_verification_authority_granted",
    }
    for key in required_true:
        if state.get(key) is not True:
            fail(
                "STOP_POST_VS1_TRANSITION_CLOSURE_AUTHORITY_UPDATE_NOT_APPLIED",
                field=f"authority_state_after_update.{key}",
                expected=True,
                actual=state.get(key),
            )
    if state.get("authority_state_id") != "POST_VS1_DIRECTION_AUTHORITY_STATE_APPLIED_PENDING_TRANSITION_CLOSURE":
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_AUTHORITY_UPDATE_NOT_APPLIED",
            field="authority_state_id",
            expected="POST_VS1_DIRECTION_AUTHORITY_STATE_APPLIED_PENDING_TRANSITION_CLOSURE",
            actual=state.get("authority_state_id"),
        )
    if state.get("authority_transition_closed") is not False:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_TRANSITION_ALREADY_CLOSED",
            field="authority_transition_closed",
            expected=False,
            actual=state.get("authority_transition_closed"),
        )
    if (
        state.get("authority_effective_for_vs2_consumption") is not False
        or state.get("authority_grants_effective_for_consumption") is not False
        or state.get("vs2_source_intake_lawful") is not False
    ):
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_AUTHORITY_PREMATURELY_EFFECTIVE",
            field="pre_closure_effectivity",
            expected=False,
            actual={
                "authority_effective_for_vs2_consumption": state.get(
                    "authority_effective_for_vs2_consumption"
                ),
                "authority_grants_effective_for_consumption": state.get(
                    "authority_grants_effective_for_consumption"
                ),
                "vs2_source_intake_lawful": state.get("vs2_source_intake_lawful"),
            },
        )
    if state.get("vs2_started") is not False:
        fail("STOP_POST_VS1_TRANSITION_CLOSURE_VS2_PREMATURELY_STARTED")
    if state.get("vs2_1_built") is not False:
        fail("STOP_POST_VS1_TRANSITION_CLOSURE_VS2_1_PREMATURELY_BUILT")
    if state.get("transition_state") != "AUTHORITY_UPDATE_APPLIED_PENDING_CLOSURE":
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_AUTHORITY_UPDATE_NOT_APPLIED",
            field="transition_state",
            expected="AUTHORITY_UPDATE_APPLIED_PENDING_CLOSURE",
            actual=state.get("transition_state"),
        )


def validate_transition_requirement(update: dict[str, Any]) -> None:
    transition = update.get("transition_closure_requirement", {})
    expected = {
        "transition_closure_required": True,
        "transition_closure_created_by_this_unit": False,
        "transition_closure_status": "PENDING",
        "next_unit": "POST_VS1_DIRECTION_TRANSITION_CLOSURE_V0_PENDING",
        "expected_later_closure_status": CLOSURE_STATUS,
        "authority_update_applied_does_not_close_authority_transition": True,
    }
    for key, value in expected.items():
        if transition.get(key) != value:
            code = (
                "STOP_POST_VS1_TRANSITION_CLOSURE_NOT_REQUIRED"
                if key == "transition_closure_required"
                else "STOP_POST_VS1_TRANSITION_CLOSURE_SOURCE_STATUS_NOT_PENDING"
                if key == "transition_closure_status"
                else "STOP_POST_VS1_TRANSITION_CLOSURE_EXPECTED_STATUS_MISMATCH"
            )
            fail(code, field=f"transition_closure_requirement.{key}", expected=value, actual=transition.get(key))
    required_boundaries = {
        "VS2 source intake is not lawful",
        "VS2.1 is not lawful",
        "no grant may be consumed",
        "no construction may begin",
    }
    if set(transition.get("until_closure_passes", [])) != required_boundaries:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_SOURCE_BOUNDARY_MISSING",
            field="until_closure_passes",
            expected=sorted(required_boundaries),
            actual=transition.get("until_closure_passes", []),
        )


def validate_decision_consumption(update: dict[str, Any]) -> None:
    consumption = update.get("decision_receipt_consumption", {})
    expected = {
        "decision_receipt_consumed_for_authority_update": True,
        "decision_receipt_consumption_count": 1,
        "same_receipt_may_apply_again": False,
    }
    for key, value in expected.items():
        if consumption.get(key) != value:
            fail(
                "STOP_POST_VS1_TRANSITION_CLOSURE_DECISION_RECEIPT_CONSUMPTION_MISMATCH",
                field=f"decision_receipt_consumption.{key}",
                expected=value,
                actual=consumption.get(key),
            )


def validate_grants(granted: dict[str, Any]) -> None:
    expected_statuses = {
        "VS2_DEFINITION_AUTHORITY": "GRANTED",
        "VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY": "GRANTED",
        "VS2_BOUNDED_CONSTRUCTION_AUTHORITY": "GRANTED",
        "VS2_FIXTURE_CONSTRUCTION_AUTHORITY": "GRANTED",
        "VS2_FIRST_RUN_READINESS_GATE_CONSTRUCTION_AUTHORITY": "GRANTED",
        "VS2_CONSTRUCTION_PACKAGE_VERIFICATION_AUTHORITY": "GRANTED",
    }
    for key, value in expected_statuses.items():
        if granted.get(key) != value:
            fail(
                "STOP_POST_VS1_TRANSITION_CLOSURE_GRANT_VECTOR_MISMATCH",
                field=f"granted_authority_vector.{key}",
                expected=value,
                actual=granted.get(key),
            )
    if granted.get("definition_authority_aliases_profile_and_target_freeze_authority") is not True:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_GRANT_VECTOR_MISMATCH",
            field="definition_authority_aliases_profile_and_target_freeze_authority",
            expected=True,
            actual=granted.get("definition_authority_aliases_profile_and_target_freeze_authority"),
        )
    if granted.get("permitted_first_consumer") != "VS2.1":
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_GRANT_VECTOR_MISMATCH",
            field="permitted_first_consumer",
            expected="VS2.1",
            actual=granted.get("permitted_first_consumer"),
        )
    records = granted.get("grant_records", [])
    if granted.get("grant_record_count") != 5 or len(records) != 5:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_GRANT_RECORD_COUNT_MISMATCH",
            field="grant_record_count",
            expected=5,
            actual={"declared": granted.get("grant_record_count"), "actual": len(records)},
        )
    ids = [record.get("grant_id") for record in records]
    if ids != EXPECTED_GRANT_IDS:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_GRANT_VECTOR_MISMATCH",
            field="grant_ids",
            expected=EXPECTED_GRANT_IDS,
            actual=ids,
        )
    if len(set(ids)) != len(ids):
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_DUPLICATE_GRANT_ID",
            field="grant_ids",
            expected=EXPECTED_GRANT_IDS,
            actual=ids,
        )
    for record in records:
        expected = {
            "grant_status": "GRANTED",
            "grant_basis_commit_sha": SOURCE_RECEIPT_COMMIT,
            "grant_basis_receipt_sha256": SOURCE_RECEIPT_CANONICAL_SHA256,
            "grant_basis_decision_package_sha256": SOURCE_DECISION_PACKAGE_SHA256,
            "grant_target_phase": "VS2",
            "grant_target_direction": DIRECTION_ID,
            "grant_target_family": TARGET_FAMILY,
            "grant_first_target": FIRST_TARGET,
            "grant_reusable": False,
            "grant_portable": False,
            "grant_generalizing": False,
            "grant_execution_capable": False,
            "grant_effective_for_downstream_consumption": False,
            "grant_effectivity_condition": GRANT_EFFECTIVITY_CONDITION,
            "grant_consumed_by_this_update": False,
        }
        for key, value in expected.items():
            if record.get(key) != value:
                code = (
                    "STOP_POST_VS1_TRANSITION_CLOSURE_GRANT_EFFECTIVITY_CONDITION_MISMATCH"
                    if key == "grant_effectivity_condition"
                    else "STOP_POST_VS1_TRANSITION_CLOSURE_GRANT_PREMATURELY_CONSUMED"
                    if key == "grant_consumed_by_this_update"
                    else "STOP_POST_VS1_TRANSITION_CLOSURE_EXECUTION_CAPABLE_GRANT_PRESENT"
                    if key == "grant_execution_capable"
                    else "STOP_POST_VS1_TRANSITION_CLOSURE_GRANT_SCOPE_MISMATCH"
                )
                fail(code, field=f"{record.get('grant_id')}.{key}", expected=value, actual=record.get(key))


def build_grant_effectivity_audit(granted: dict[str, Any]) -> dict[str, Any]:
    validate_grants(granted)
    records = granted["grant_records"]
    projections = []
    for record in records:
        projections.append(
            {
                "grant_id": record["grant_id"],
                "source_grant_status": record["grant_status"],
                "source_grant_scope": record["grant_scope"],
                "source_grant_effective_for_downstream_consumption": record[
                    "grant_effective_for_downstream_consumption"
                ],
                "source_grant_effectivity_condition": record["grant_effectivity_condition"],
                "transition_closure_verified": True,
                "effective_for_downstream_consumption_after_closure": True,
                "available_to_declared_downstream_consumer": True,
                "permitted_first_consumer": "VS2.1",
                "consumed_by_transition_closure": False,
                "consumption_count_at_closure": 0,
                "execution_capable": record["grant_execution_capable"],
                "reusable": record["grant_reusable"],
                "portable": record["grant_portable"],
                "generalizing": record["grant_generalizing"],
            }
        )
    return {
        "source_grant_records": records,
        "closure_grant_projections": projections,
        "grant_effectivity_boundary": (
            "grant made effective by transition closure != grant consumed by transition closure"
        ),
        "source_grant_record_count": len(records),
        "closure_grant_projection_count": len(projections),
        "unmatched_grant_count": 0,
        "duplicate_grant_id_count": 0,
        "scope_mismatch_count": 0,
        "grant_effectivity_condition_mismatch_count": 0,
        "all_source_grants_ineffective_before_closure": True,
        "all_closure_grant_projections_effective_after_closure": True,
        "no_grant_consumed": True,
    }


def build_withheld_authority_audit(withheld: dict[str, Any]) -> dict[str, Any]:
    mismatches = {
        key: {"expected": value, "actual": withheld.get(key)}
        for key, value in REQUIRED_WITHHELD_STATUSES.items()
        if withheld.get(key) != value
    }
    if mismatches:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_WITHHELD_AUTHORITY_MISMATCH",
            field="withheld_authority_vector",
            expected=REQUIRED_WITHHELD_STATUSES,
            actual=mismatches,
        )
    if withheld.get("unapproved_authority_grant_count") != 0:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_UNAPPROVED_AUTHORITY_PRESENT",
            field="unapproved_authority_grant_count",
            expected=0,
            actual=withheld.get("unapproved_authority_grant_count"),
        )
    if withheld.get("execution_authority_included") is not False:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_EXECUTION_AUTHORITY_PRESENT",
            field="execution_authority_included",
            expected=False,
            actual=withheld.get("execution_authority_included"),
        )
    return {
        "source_withheld_authority_vector": withheld,
        "withheld_authority_matches_source_exclusions": True,
        "unapproved_authority_grant_count": 0,
        "execution_authority_included": False,
        "withheld_authority_preserved_through_closure": True,
        "withheld_authority_changed_by_closure": False,
    }


def authority_update_consumption() -> dict[str, Any]:
    return {
        "authority_update_consumed_for_transition_closure": True,
        "authority_update_consumption_count": 1,
        "authority_update_reusable_for_second_transition_closure": False,
        "same_authority_update_may_close_again": False,
        "transition_closure_idempotent_reapplication_allowed": False,
        "source_authority_update_rewritten": False,
        "authority_update_consumed_as_closure_basis_not_rewritten": True,
        "vs2_grant_consumption_count": 0,
        "profile_and_target_freeze_grant_consumed": False,
        "bounded_construction_grant_consumed": False,
        "fixture_construction_grant_consumed": False,
        "readiness_gate_construction_grant_consumed": False,
        "construction_verification_grant_consumed": False,
    }


def post_closure_authority_state() -> dict[str, Any]:
    return {
        "authority_state_id": "POST_VS1_DIRECTION_AUTHORITY_STATE_CLOSED_EFFECTIVE_FOR_VS2_SOURCE_INTAKE",
        "human_decision_recorded": True,
        "decision_receipt_created": True,
        "decision_receipt_consumed_for_authority_update": True,
        "authority_update_consumed_for_transition_closure": True,
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
        "authority_transition_closed": True,
        "vs2_definition_authority_granted": True,
        "vs2_profile_and_target_freeze_authority_granted": True,
        "vs2_bounded_construction_authority_granted": True,
        "fixture_construction_authority_granted": True,
        "readiness_gate_construction_authority_granted": True,
        "construction_package_verification_authority_granted": True,
        "authority_grants_recorded": True,
        "authority_grants_effective_for_consumption": True,
        "authority_effective_for_vs2_consumption": True,
        "vs2_source_intake_lawful": True,
        "vs2_1_may_begin": True,
        "vs2_source_intake_built": False,
        "vs2_started": False,
        "vs2_1_built": False,
        "any_vs2_grant_consumed": False,
        "construction_performed": False,
        "fixture_construction_performed": False,
        "readiness_gate_constructed": False,
        "construction_package_verified": False,
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
        "transition_state": "AUTHORITY_TRANSITION_CLOSED_EFFECTIVE_FOR_BOUNDED_VS2_CONSUMPTION",
        "closure_result": CLOSURE_STATUS,
    }


def downstream_vs2_boundary() -> dict[str, Any]:
    return {
        "next_phase_id": "PHASE_VS2",
        "next_unit": "VS2_1_POST_VS1_SOURCE_INTAKE_PENDING",
        "next_unit_role": "BOUND_SOURCE_INTAKE_ONLY",
        "next_unit_must_bind_transition_closure_sha256": True,
        "next_unit_must_bind_authority_update_sha256": True,
        "next_unit_must_preserve_execution_authority_absent": True,
        "next_unit_must_not_consume_construction_authority": True,
        "next_source_intake_unit_may": [
            "verify the committed post-VS1 chain",
            "bind this transition closure",
            "bind the effective bounded authority state",
            "establish the VS2 source surface",
            "identify the first construction consumer",
        ],
        "next_source_intake_unit_may_not": [
            "construct the kernel profile",
            "freeze the target",
            "construct contracts",
            "construct fixtures",
            "construct readiness gates",
            "run fixtures",
            "authorize execution",
        ],
        "vs2_source_intake_is_authorized_to_be_built": True,
        "vs2_source_intake_created_by_this_unit": False,
        "vs2_profile_or_target_artifact_created_by_this_unit": False,
        "vs2_construction_artifact_created_by_this_unit": False,
    }


def closure_invocation_evidence() -> dict[str, Any]:
    return {
        "invocation_actor_class": "HUMAN_OPERATOR",
        "invocation_actor_identity": "HUMAN_OPERATOR_CURRENT_MATRIXLAB_SESSION",
        "invocation_source_kind": "EXPLICIT_INTERACTIVE_USER_INSTRUCTION",
        "invocation_statement_exact": "proceed",
        "invocation_interpretation": "CLOSE_COMMITTED_POST_VS1_DIRECTION_AUTHORITY_TRANSITION",
        "invocation_date_local": "2026-07-11",
        "invocation_timezone": "Europe/Lisbon",
        "invocation_time_precision": "DATE_AND_SESSION_SEQUENCE_ONLY",
        "invocation_sequence_anchor": "AFTER_COMMIT_EBEB85A867B559DF9F004CE8F4495E1581E79D14",
        "invocation_statement_sha256": sha256_bytes(b"proceed"),
        "invocation_adds_authority_scope": False,
        "invocation_revises_authority_update": False,
        "invocation_grants_execution_authority": False,
        "invocation_selects_closure_only": True,
        "closure_mode": "VERIFY_AND_CLOSE_EXACT_AUTHORITY_UPDATE",
        "invocation_independently_grants_authority": False,
    }


def build_closure(root: Path, update: dict[str, Any], source_content_sha: str) -> dict[str, Any]:
    validate_authority_update_identity(update)
    validate_authority_update_binding(update)
    validate_source_chain(update)
    validate_applied_scope(update)
    validate_decision_consumption(update)
    validate_pre_closure_state(update)
    validate_transition_requirement(update)

    source_binding = {
        "source_authority_update_artifact_id": SOURCE_AUTHORITY_UPDATE_ARTIFACT_ID,
        "source_authority_update_path": SOURCE_AUTHORITY_UPDATE_PATH,
        "source_authority_update_commit_sha": EXPECTED_HEAD,
        "source_authority_update_content_sha256": source_content_sha,
        "source_authority_update_sha256": SOURCE_AUTHORITY_UPDATE_CANONICAL_SHA256,
        "source_authority_update_canonical_sha256": SOURCE_AUTHORITY_UPDATE_CANONICAL_SHA256,
        "source_authority_update_gate": SOURCE_AUTHORITY_UPDATE_GATE,
        "source_authority_update_terminal_transition": SOURCE_AUTHORITY_UPDATE_TERMINAL,
        "source_authority_update_status": SOURCE_AUTHORITY_UPDATE_STATUS,
        "source_authority_transition_closed": False,
        "source_authority_effective_for_vs2_consumption": False,
        "source_authority_update_committed_bytes_verified": True,
        "source_authority_update_worktree_matches_commit": True,
        "latest_file_resolution_used": False,
        "mtime_resolution_used": False,
        "directory_scan_authority_used": False,
        "baseline_share_used_as_source_authority": False,
    }
    source_receipt = update["source_decision_receipt_binding"]
    source_package = update["source_decision_package_binding"]
    source_chain = {
        "source_decision_receipt_commit_sha": source_receipt["source_decision_receipt_commit_sha"],
        "source_decision_receipt_canonical_sha256": source_receipt[
            "source_decision_receipt_canonical_sha256"
        ],
        "source_decision_receipt_sha256": source_receipt[
            "source_decision_receipt_canonical_sha256"
        ],
        "source_decision_package_sha256": source_package["source_decision_package_sha256"],
        "direction": DIRECTION_ID,
        "target_family": TARGET_FAMILY,
        "first_target": FIRST_TARGET,
        "application_mode": APPLICATION_MODE,
        "applied_scope_mode": update["applied_authority_scope"]["applied_scope_mode"],
        "applied_scope_equals_source_approved_scope": True,
        "applied_scope_exceeds_approved_scope": False,
        "approved_scope_items_omitted": [],
        "unapproved_scope_items_added": [],
    }
    grant_audit = build_grant_effectivity_audit(update["granted_authority_vector"])
    withheld_audit = build_withheld_authority_audit(update["withheld_authority_vector"])
    consumption = authority_update_consumption()
    post_state = post_closure_authority_state()
    downstream = downstream_vs2_boundary()
    payload = {
        "source_authority_update_binding": source_binding,
        "source_decision_chain_binding": source_chain,
        "closure_invocation_evidence": closure_invocation_evidence(),
        "pre_closure_authority_state": update["authority_state_after_update"],
        "grant_effectivity_audit": grant_audit,
        "withheld_authority_audit": withheld_audit,
        "authority_update_consumption": consumption,
        "post_closure_authority_state": post_state,
        "downstream_vs2_boundary": downstream,
    }
    if list(payload.keys()) != TRANSITION_CLOSURE_BOUND_SECTIONS:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_HASH_MISMATCH",
            field="transition_closure_payload",
            expected=TRANSITION_CLOSURE_BOUND_SECTIONS,
            actual=list(payload.keys()),
        )
    closure_sha = canonical_hash(payload)
    closure = {
        "schema_version": SCHEMA_VERSION,
        "artifact_id": ARTIFACT_ID,
        "object_id": OBJECT_ID,
        "object_role": OBJECT_ROLE,
        "transition_closure_status": CLOSURE_STATUS,
        "source_authority_update_binding": source_binding,
        "source_decision_chain_binding": source_chain,
        "closure_invocation_evidence": payload["closure_invocation_evidence"],
        "pre_closure_authority_state": update["authority_state_after_update"],
        "grant_effectivity_audit": grant_audit,
        "withheld_authority_audit": withheld_audit,
        "authority_update_consumption": consumption,
        "post_closure_authority_state": post_state,
        "downstream_vs2_boundary": downstream,
        "transition_closure_binding": {
            "canonicalization": CANONICALIZATION_CONTRACT,
            "canonicalization_contract": CANONICALIZATION_CONTRACT,
            "bound_sections": TRANSITION_CLOSURE_BOUND_SECTIONS,
            "transition_closure_payload": payload,
            "transition_closure_sha256": closure_sha,
            "generated_at_metadata_excluded_from_hash": True,
            "volatile_filesystem_metadata_excluded_from_hash": True,
            "commit_created_fields_excluded_from_hash": True,
            "future_vs2_artifact_identities_excluded_from_hash": True,
            "future_grant_consumption_receipts_excluded_from_hash": True,
            "execution_authority_decisions_excluded_from_hash": True,
            "vs2_source_intake_must_bind_transition_closure_sha256": True,
            "later_grant_consumption_receipts_must_bind_transition_closure_sha256": True,
        },
        "transition_closure_sha256": closure_sha,
        "transition_closure_checks": [
            {"check_id": check, "check_result": check, "status": "PASS"}
            for check in TRANSITION_CLOSURE_CHECKS
        ],
        "transition_closure_gate": CLOSURE_GATE,
        "terminal_transition": {
            "transition": TERMINAL_TRANSITION,
            "consumes_authority_update_for_closure": True,
            "closes_authority_transition": True,
            "makes_bounded_grants_effective_for_downstream_consumption": True,
            "makes_vs2_source_intake_lawful": True,
            "permits_vs2_1_to_begin": True,
            "consumes_vs2_grant": False,
            "starts_vs2": False,
            "builds_vs2_1": False,
            "performs_construction": False,
            "authorizes_execution": False,
            "authorizes_positive_path_execution": False,
            "authorizes_negative_path_execution": False,
            "authorizes_sweep": False,
            "authorizes_rerun": False,
            "authorizes_radius_renewal": False,
            "creates_runner_authority": False,
            "grants_reusable_schema_authority": False,
            "grants_reusable_move_authority": False,
            "selects_second_target": False,
            "authorizes_portability": False,
        },
        "evidence_yield": {
            "branch": "CONFIRMATION_YIELD",
            "source_authority_update_verified": True,
            "transition_closure_hash_bound": True,
            "bounded_grants_effective_for_later_downstream_consumption": True,
            "execution_authority_absent": True,
        },
        "non_claims": [
            "This closure does not start VS2.",
            "This closure does not build VS2.1 or a VS2 source-intake artifact.",
            "This closure does not consume any VS2 grant.",
            "This closure does not construct schemas, contracts, fixtures, readiness gates, or verification artifacts.",
            "This closure does not authorize execution, sweeps, reruns, radius renewal, or runner authority.",
        ],
        "failures": [],
    }
    validate_closure(closure)
    return closure


def validate_closure(closure: dict[str, Any]) -> None:
    binding = closure["transition_closure_binding"]
    if list(binding["transition_closure_payload"].keys()) != binding["bound_sections"]:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_HASH_MISMATCH",
            field="transition_closure_binding.bound_sections",
            expected=binding["bound_sections"],
            actual=list(binding["transition_closure_payload"].keys()),
        )
    recomputed = canonical_hash(binding["transition_closure_payload"])
    if recomputed != binding["transition_closure_sha256"]:
        fail(
            "STOP_POST_VS1_TRANSITION_CLOSURE_HASH_MISMATCH",
            field="transition_closure_binding.transition_closure_sha256",
            expected=recomputed,
            actual=binding["transition_closure_sha256"],
        )
    state = closure["post_closure_authority_state"]
    required_false = [
        "vs2_source_intake_built",
        "vs2_started",
        "vs2_1_built",
        "any_vs2_grant_consumed",
        "construction_performed",
        "fixture_construction_performed",
        "readiness_gate_constructed",
        "construction_package_verified",
        "broad_vs2_authority_granted",
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
    ]
    for key in required_false:
        if state[key] is not False:
            code = (
                "STOP_POST_VS1_TRANSITION_CLOSURE_EXECUTION_AUTHORITY_PRESENT"
                if key in {"execution_authorized", "positive_path_execution_authorized", "negative_path_execution_authorized"}
                else "STOP_POST_VS1_TRANSITION_CLOSURE_SWEEP_AUTHORITY_PRESENT"
                if key == "sweep_authorized"
                else "STOP_POST_VS1_TRANSITION_CLOSURE_RERUN_AUTHORITY_PRESENT"
                if key == "automatic_rerun_authorized"
                else "STOP_POST_VS1_TRANSITION_CLOSURE_RADIUS_RENEWAL_AUTHORITY_PRESENT"
                if key == "automatic_radius_renewal_authorized"
                else "STOP_POST_VS1_TRANSITION_CLOSURE_RUNNER_AUTHORITY_PRESENT"
                if key == "runner_authority_created"
                else "STOP_POST_VS1_TRANSITION_CLOSURE_REUSE_AUTHORITY_PRESENT"
                if key in {"reusable_schema_authority_granted", "reusable_move_authority_granted"}
                else "STOP_POST_VS1_TRANSITION_CLOSURE_SECOND_TARGET_AUTHORITY_PRESENT"
                if key == "second_target_authority_granted"
                else "STOP_POST_VS1_TRANSITION_CLOSURE_PORTABILITY_AUTHORITY_PRESENT"
                if key == "portability_authority_granted"
                else "STOP_POST_VS1_TRANSITION_CLOSURE_BROAD_VS2_AUTHORITY_PRESENT"
                if key == "broad_vs2_authority_granted"
                else "STOP_POST_VS1_TRANSITION_CLOSURE_DOWNSTREAM_ARTIFACT_CREATED"
            )
            fail(code, field=f"post_closure_authority_state.{key}", expected=False, actual=state[key])
    terminal = closure["terminal_transition"]
    if terminal["starts_vs2"] is not False:
        fail("STOP_POST_VS1_TRANSITION_CLOSURE_VS2_AUTO_STARTED")
    if terminal["builds_vs2_1"] is not False:
        fail("STOP_POST_VS1_TRANSITION_CLOSURE_VS2_1_AUTO_BUILT")
    if terminal["performs_construction"] is not False:
        fail("STOP_POST_VS1_TRANSITION_CLOSURE_CONSTRUCTION_AUTO_PERFORMED")
    if closure["downstream_vs2_boundary"]["vs2_source_intake_created_by_this_unit"] is not False:
        fail("STOP_POST_VS1_TRANSITION_CLOSURE_SOURCE_INTAKE_AUTO_BUILT")


def build_markdown(closure: dict[str, Any]) -> str:
    source = closure["source_authority_update_binding"]
    chain = closure["source_decision_chain_binding"]
    state = closure["post_closure_authority_state"]
    consumption = closure["authority_update_consumption"]
    grant_audit = closure["grant_effectivity_audit"]
    return f"""# Post-VS1 Direction Transition Closure v0

## Source binding

Source authority-update commit:
{source["source_authority_update_commit_sha"]}

Source authority-update hash:
{source["source_authority_update_canonical_sha256"]}

Source decision-receipt hash:
{chain["source_decision_receipt_sha256"]}

Source decision-package hash:
{chain["source_decision_package_sha256"]}

Transition-closure hash:
{closure["transition_closure_binding"]["transition_closure_sha256"]}

## Closure result

{closure["transition_closure_status"]}

## Effective bounded grants

- VS2 profile and target freeze authority
- VS2 bounded construction authority
- fixture construction authority
- first-run readiness-gate construction authority
- construction-package verification authority

## Boundary

Authority transition closed.
Bounded grants are effective for later downstream consumption.
VS2 source intake is now lawful to build.
VS2.1 may begin through a separate bound unit.

No VS2 grant was consumed by this closure.
VS2 source intake was not built.
VS2 was not started.
VS2.1 was not built.
No construction was performed.
Execution was not authorized.
Sweeps were not authorized.
Runner authority was not created.

## Counts

- Source grant records: {grant_audit["source_grant_record_count"]}
- Closure grant projections: {grant_audit["closure_grant_projection_count"]}
- Authority-update consumption count: {consumption["authority_update_consumption_count"]}
- VS2 grant consumption count: {consumption["vs2_grant_consumption_count"]}

## Binding

- authority transition closed: {str(state["authority_transition_closed"]).lower()}
- authority effective for VS2 consumption: {str(state["authority_effective_for_vs2_consumption"]).lower()}
- authority grants effective for consumption: {str(state["authority_grants_effective_for_consumption"]).lower()}
- VS2 source intake lawful: {str(state["vs2_source_intake_lawful"]).lower()}
- VS2 source intake built: {str(state["vs2_source_intake_built"]).lower()}
- VS2.1 may begin: {str(state["vs2_1_may_begin"]).lower()}
- VS2 started: {str(state["vs2_started"]).lower()}
- VS2.1 built: {str(state["vs2_1_built"]).lower()}
- construction performed: {str(state["construction_performed"]).lower()}
- execution authorized: {str(state["execution_authorized"]).lower()}
- sweep authorized: {str(state["sweep_authorized"]).lower()}

## Next

VS2_1_POST_VS1_SOURCE_INTAKE_PENDING
"""


def emit_success(closure: dict[str, Any]) -> None:
    source = closure["source_authority_update_binding"]
    chain = closure["source_decision_chain_binding"]
    grant_audit = closure["grant_effectivity_audit"]
    consumption = closure["authority_update_consumption"]
    state = closure["post_closure_authority_state"]
    binding = closure["transition_closure_binding"]
    print("BUILD_POST_VS1_DIRECTION_TRANSITION_CLOSURE_V0_COMPLETE")
    print()
    print(f"artifact_id={ARTIFACT_ID}")
    print(f"schema_version={SCHEMA_VERSION}")
    print(f"object_id={OBJECT_ID}")
    print(f"object_role={OBJECT_ROLE}")
    print()
    print(f"source_authority_update_commit_sha={EXPECTED_HEAD}")
    print(f"source_authority_update_sha256={SOURCE_AUTHORITY_UPDATE_CANONICAL_SHA256}")
    print("source_authority_update_hash_recomputes=true")
    print(f"source_authority_update_committed_bytes_verified={str(source['source_authority_update_committed_bytes_verified']).lower()}")
    print()
    print(f"source_decision_receipt_sha256={chain['source_decision_receipt_sha256']}")
    print(f"source_decision_package_sha256={chain['source_decision_package_sha256']}")
    print()
    print("closure_mode=VERIFY_AND_CLOSE_EXACT_AUTHORITY_UPDATE")
    print()
    print(f"source_grant_record_count={grant_audit['source_grant_record_count']}")
    print(f"closure_grant_projection_count={grant_audit['closure_grant_projection_count']}")
    print(f"unmatched_grant_count={grant_audit['unmatched_grant_count']}")
    print(f"duplicate_grant_id_count={grant_audit['duplicate_grant_id_count']}")
    print(f"scope_mismatch_count={grant_audit['scope_mismatch_count']}")
    print()
    print("authority_update_consumed_for_transition_closure=true")
    print(f"authority_update_consumption_count={consumption['authority_update_consumption_count']}")
    print("same_authority_update_may_close_again=false")
    print()
    for key in [
        "authority_transition_closed",
        "authority_effective_for_vs2_consumption",
        "authority_grants_effective_for_consumption",
        "vs2_source_intake_lawful",
        "vs2_source_intake_built",
        "vs2_1_may_begin",
        "any_vs2_grant_consumed",
    ]:
        print(f"{key}={str(state[key]).lower()}")
    print(f"vs2_grant_consumption_count={consumption['vs2_grant_consumption_count']}")
    print()
    for key in [
        "vs2_started",
        "vs2_1_built",
        "construction_performed",
        "broad_vs2_authority_granted",
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
    ]:
        print(f"{key}={str(state[key]).lower()}")
    print()
    print(f"transition_closure_sha256={binding['transition_closure_sha256']}")
    print("transition_closure_hash_present=true")
    print(f"transition_closure_hash_recomputes={str(canonical_hash(binding['transition_closure_payload']) == binding['transition_closure_sha256']).lower()}")
    print()
    print(f"transition_closure_status={CLOSURE_STATUS}")
    print()
    print(f"transition_closure_gate={CLOSURE_GATE}")
    print()
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


def emit_failure(exc: TransitionClosureFailure) -> None:
    print("BUILD_POST_VS1_DIRECTION_TRANSITION_CLOSURE_V0_FAILED")
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
    ensure_no_forbidden_outputs(root)
    before = capture_source_hashes(root)
    update, content_sha = verify_committed_authority_update_bytes(root)
    closure = build_closure(root, update, content_sha)
    (root / OUTPUT_JSON).parent.mkdir(parents=True, exist_ok=True)
    (root / OUTPUT_JSON).write_text(json.dumps(closure, indent=2) + "\n", encoding="utf-8")
    (root / OUTPUT_MD).write_text(build_markdown(closure), encoding="utf-8")
    after = capture_source_hashes(root)
    validate_source_preservation(before, after)
    validate_dirty_scope(root)
    ensure_no_forbidden_outputs(root)
    emit_success(closure)
    return 0


def main() -> int:
    try:
        return generate()
    except TransitionClosureFailure as exc:
        emit_failure(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
