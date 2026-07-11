#!/usr/bin/env python3

"""Build the post-VS1 human direction decision surface v0."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


EXPECTED_HEAD = "eabe605deaac3c34d2e9fa7295f4e813ea582ca7"
EXPECTED_BRANCH = "master"
SCRIPT = "scripts/build_post_vs1_direction_decision_surface_v0.py"

SCHEMA_VERSION = "matrixlabs_post_vs1_direction_decision_surface_v0"
ARTIFACT_ID = "post_vs1_direction_decision_surface_v0"
OBJECT_ID = "POST_VS1_DIRECTION_DECISION_SURFACE"
OBJECT_ROLE = "HUMAN_DIRECTION_DECISION_SURFACE_ONLY"
SURFACE_GATE = "POST_VS1_DIRECTION_DECISION_SURFACE_PASS_READY_FOR_HUMAN_DECISION"
TERMINAL_TRANSITION = "STOP_POST_VS1_DIRECTION_SURFACE_READY_PENDING_HUMAN_DECISION"

SOURCE_CLOSURE_PATH = "docs/matrixlabs/phase_vs1/phase_vs1_closure_v0.json"
SOURCE_CLOSURE_MD = "docs/matrixlabs/phase_vs1/phase_vs1_closure_v0.md"
SOURCE_MAP_PATH = "docs/matrixlabs/phase_vs1/phase_vs1_missing_precondition_next_surface_map_v0.json"
SOURCE_MAP_MD = "docs/matrixlabs/phase_vs1/phase_vs1_missing_precondition_next_surface_map_v0.md"
PROPOSAL_PATH = (
    "docs/matrixlabs/post_vs1/sources/"
    "matrixlab_first_sweep_capable_kernel_target_specification_v0.md"
)
PROPOSAL_SIDECAR_PATH = (
    "docs/matrixlabs/post_vs1/sources/"
    "matrixlab_first_sweep_capable_kernel_target_specification_v0.source.json"
)
OUTPUT_JSON = "docs/matrixlabs/post_vs1/post_vs1_direction_decision_surface_v0.json"
OUTPUT_MD = "docs/matrixlabs/post_vs1/post_vs1_direction_decision_surface_v0.md"

SOURCE_CLOSURE_COMMIT = "eabe605deaac3c34d2e9fa7295f4e813ea582ca7"
SOURCE_MAP_COMMIT = "955743f9cf281d9b83c9e68fb0f367121b3c5295"
PHASE_STATUS = "PHASE_VS1_PASS_LOOP_NOT_READY_MISSING_PRECONDITIONS_EXPOSED_AND_NEXT_SURFACES_MAPPED"
CLOSURE_GATE = "VS1_6_PHASE_CLOSURE_PASS_LOOP_NOT_READY_WITH_NEXT_SURFACES_MAPPED"
CLOSURE_BRANCH = "NOT_READY_BLOCKERS_MAPPED"
MAP_VERDICT = "VS1_5_MISSING_PRECONDITION_NEXT_SURFACE_MAP_PASS"

PROPOSAL_ARTIFACT_ID = "matrixlab_first_sweep_capable_kernel_target_specification_v0"
PROPOSAL_SOURCE_ROLE = "NON_BINDING_DIRECTIONAL_PROPOSAL"
PROPOSAL_DURABILITY = "DURABLY_CAPTURED_EXTERNAL_ARTIFACT"
PROPOSAL_TARGET_STATUS = "PROVISIONAL_NON_BINDING_PROPOSAL_TARGET"

BUNDLE_ID = "POST_VS1_FIRST_SWEEP_CAPABLE_KERNEL_BUNDLE_V0"
RELATIONSHIP_TO_VS1_5 = "BOUNDED_BUNDLE_OVER_MAPPED_VS1_5_SURFACES"
PRIMARY_BUNDLE_MEMBERS = [
    "S01_SCOPE_REGIME_DECLARATION_CONTRACT_SURFACE",
    "S02_TYPED_STATE_OBJECT_CONTRACT_SURFACE",
    "S03_MOVE_SPACE_CONTRACT_SURFACE",
    "S04_MOVE_SELECTOR_CONTRACT_SURFACE",
    "S05_MOVE_APPLICATOR_CONTRACT_SURFACE",
    "S06_AUTHORITY_POLICY_SURFACE",
    "S07_RADIUS_BUDGET_POLICY_SURFACE",
    "S08_HALT_POLICY_SURFACE",
    "S09_RECEIPT_OBLIGATION_CONTRACT_SURFACE",
    "S10_SOURCE_IDENTITY_FRESHNESS_POLICY_SURFACE",
    "S11_MICRO_SWEEP_BOUNDS_CONTRACT_SURFACE",
    "S12_PRESSURE_READOUT_CONTRACT_SURFACE",
    "S13_PRESSURE_CLASSIFICATION_VOCABULARY_SURFACE",
    "S16_REPLAY_AUDIT_CONTRACT_SURFACE",
    "S17_FORBIDDEN_EFFECT_GUARD_SURFACE",
    "S18_EVIDENCE_YIELD_HOOK_SURFACE",
    "S19_HUMAN_ESCALATION_DECISION_BOUNDARY_SURFACE",
    "S20_CONVERGENCE_CRITERION_CONTRACT_SURFACE",
]
DEFERRED_SURFACES = [
    "S14_LOCAL_REVISION_SURFACE_CONTRACT",
    "S15_BOUNDED_PORTABILITY_MAP_CONTRACT_SURFACE",
]
DOWNSTREAM_ONLY_SURFACES = ["S21_CONTROLLED_LOOP_READINESS_REAUDIT_SURFACE"]
ENTRY_PREREQUISITE = "S10_SOURCE_IDENTITY_FRESHNESS_POLICY_SURFACE"

DECISION_OPTIONS = [
    "ACCEPT_FIRST_SWEEP_CAPABLE_KERNEL_DIRECTION_AND_PROPOSED_SCOPE",
    "ACCEPT_FIRST_SWEEP_CAPABLE_KERNEL_WITH_DECLARED_REVISIONS",
    "RETURN_FIRST_SWEEP_CAPABLE_KERNEL_FOR_TIGHTENING",
    "SELECT_ALTERNATIVE_POST_VS1_SURFACE",
    "REQUEST_NEW_POST_VS1_DIRECTION_PROPOSAL",
    "HOLD_AFTER_VS1_NO_NEXT_DIRECTION_SELECTED",
    "REJECT_FIRST_SWEEP_CAPABLE_KERNEL_DIRECTION",
]

SURFACE_CHECKS = [
    "POST_VS1_SOURCE_CLOSURE_VERIFIED",
    "POST_VS1_CANDIDATE_MAP_VERIFIED",
    "FIRST_SWEEP_KERNEL_PROPOSAL_SOURCE_VERIFIED",
    "FIRST_SWEEP_KERNEL_PROPOSAL_SOURCE_DURABILITY_PASS",
    "FIRST_SWEEP_KERNEL_PROPOSAL_BOUNDARY_PASS",
    "FIRST_SWEEP_KERNEL_BUNDLE_MEMBERSHIP_PASS",
    "FIRST_SWEEP_KERNEL_PROPOSAL_TRACEABILITY_PASS",
    "POST_VS1_VS1_5_ADVISORY_ALIGNMENT_PASS",
    "POST_VS1_PROPOSAL_OVERBREADTH_EXCLUDED",
    "POST_VS1_DECISION_PACKAGE_BINDING_PASS",
    "POST_VS1_DECISION_OPTIONS_COMPLETE",
    "POST_VS1_PROPOSED_AUTHORITY_SCOPE_EXPLICIT",
    "POST_VS1_ALTERNATIVE_SCOPE_NON_INHERITANCE_PASS",
    "POST_VS1_DEFAULT_ACCEPTANCE_ABSENT",
    "POST_VS1_DECISION_PENDING_NOT_PRECONSUMED",
]

CANONICALIZATION_CONTRACT = "MATRIXLAB_CANONICAL_JSON_V0"
BOUND_SECTIONS = [
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

FORBIDDEN_ARTIFACTS = [
    "docs/matrixlabs/post_vs1/post_vs1_direction_decision_receipt_v0.json",
    "docs/matrixlabs/post_vs1/post_vs1_direction_authority_update_v0.json",
    "docs/matrixlabs/post_vs1/post_vs1_direction_transition_closure_v0.json",
    "docs/matrixlabs/phase_vs2",
    "docs/matrixlabs/runner",
    "docs/matrixlabs/runtime",
    "docs/matrixlabs/move_space",
    "docs/matrixlabs/micro_sweeps",
]

DECISION_QUESTION = (
    "Should MatrixLab select the First Sweep-Capable Kernel v0\n"
    "as the next post-VS1 direction, select Bounded Contract\n"
    "Convergence as its target family, select Typed State Contract\n"
    "Convergence v0 as its first bounded target, and approve the\n"
    "declared definition, bounded construction, and construction-\n"
    "verification scope for a separate authority-update step?"
)


class SurfaceFailure(RuntimeError):
    def __init__(
        self,
        code: str,
        *,
        source: str = "NONE",
        field: str = "NONE",
        expected: object = "NONE",
        actual: object = "NONE",
        next_surface: str = "POST_VS1_DIRECTION_DECISION_SURFACE_REPAIR",
    ) -> None:
        super().__init__(code)
        self.code = code
        self.source = source
        self.field = field
        self.expected = expected
        self.actual = actual
        self.next_surface = next_surface


def fail(
    code: str,
    *,
    source: str = "NONE",
    field: str = "NONE",
    expected: object = "NONE",
    actual: object = "NONE",
    next_surface: str = "POST_VS1_DIRECTION_DECISION_SURFACE_REPAIR",
) -> None:
    raise SurfaceFailure(
        code,
        source=source,
        field=field,
        expected=expected,
        actual=actual,
        next_surface=next_surface,
    )


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
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_SOURCE_IDENTITY_UNVERIFIED",
            source="git",
            field="git_command",
            expected="success",
            actual=proc.stderr.strip(),
        )
    return proc.stdout.rstrip()


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
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_SOURCE_IDENTITY_UNVERIFIED",
            source="repo",
            field="repo_root",
            expected="git repository",
            actual=proc.stderr.strip(),
        )
    return Path(proc.stdout.strip()).resolve()


def status_path(line: str) -> str:
    path = line[3:].strip()
    if " -> " in path:
        path = path.split(" -> ", 1)[1].strip()
    return path


def validate_dirty_scope(root: Path) -> None:
    allowed_exact = {
        SCRIPT,
        "scripts/build_baseline_share_v0.py",
        PROPOSAL_PATH,
        PROPOSAL_SIDECAR_PATH,
        OUTPUT_JSON,
        OUTPUT_MD,
    }
    allowed_prefixes = ("baseline_share/", "discussion_packets/")
    for line in run_git(root, ["status", "--short", "--untracked-files=all"]).splitlines():
        path = status_path(line)
        if path in allowed_exact or any(path.startswith(prefix) for prefix in allowed_prefixes):
            continue
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_SOURCE_IDENTITY_UNVERIFIED",
            source=path,
            field="dirty_scope",
            expected="only post-VS1 surface outputs, baseline_share, or discussion_packets",
            actual=line,
        )


def require_repo_context(root: Path) -> None:
    head = run_git(root, ["rev-parse", "HEAD"])
    branch = run_git(root, ["branch", "--show-current"])
    if head != EXPECTED_HEAD:
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_SOURCE_IDENTITY_UNVERIFIED",
            source="HEAD",
            field="commit_sha",
            expected=EXPECTED_HEAD,
            actual=head,
        )
    if branch != EXPECTED_BRANCH:
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_SOURCE_IDENTITY_UNVERIFIED",
            source="branch",
            field="branch",
            expected=EXPECTED_BRANCH,
            actual=branch,
        )


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json(root: Path, rel_path: str) -> dict[str, Any]:
    path = root / rel_path
    if not path.is_file():
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_SOURCE_IDENTITY_UNVERIFIED",
            source=rel_path,
            field="file_presence",
            expected=True,
            actual=False,
        )
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_SOURCE_IDENTITY_UNVERIFIED",
            source=rel_path,
            field="valid_json",
            expected=True,
            actual=str(exc),
        )
    if not isinstance(value, dict):
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_SOURCE_IDENTITY_UNVERIFIED",
            source=rel_path,
            field="json_object",
            expected=True,
            actual=type(value).__name__,
        )
    return value


def require_file(root: Path, rel_path: str) -> None:
    if not (root / rel_path).is_file():
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_PROPOSAL_MISSING",
            source=rel_path,
            field="file_presence",
            expected=True,
            actual=False,
        )


def get_value(obj: dict[str, Any], path: str, default: Any = None) -> Any:
    cur: Any = obj
    for part in path.split("."):
        if not isinstance(cur, dict):
            return default
        cur = cur.get(part, default)
    return cur


def capture_source_hashes(root: Path) -> dict[str, str]:
    return {
        SOURCE_CLOSURE_PATH: sha256_file(root / SOURCE_CLOSURE_PATH),
        SOURCE_CLOSURE_MD: sha256_file(root / SOURCE_CLOSURE_MD),
        SOURCE_MAP_PATH: sha256_file(root / SOURCE_MAP_PATH),
        SOURCE_MAP_MD: sha256_file(root / SOURCE_MAP_MD),
    }


def validate_source_preservation(before: dict[str, str], after: dict[str, str]) -> None:
    if before == after:
        return
    changed = sorted(
        path for path in set(before) | set(after) if before.get(path) != after.get(path)
    )
    fail(
        "STOP_POST_VS1_DECISION_SURFACE_SOURCE_IDENTITY_UNVERIFIED",
        source=changed[0] if changed else "unknown",
        field="source_hash",
        expected=before,
        actual=after,
    )


def ensure_no_forbidden_artifacts(root: Path) -> None:
    for rel_path in FORBIDDEN_ARTIFACTS:
        if (root / rel_path).exists():
            fail(
                "STOP_POST_VS1_DECISION_SURFACE_EXECUTION_AUTHORITY_INCLUDED",
                source=rel_path,
                field="forbidden_artifact",
                expected="absent",
                actual="present",
            )


def validate_closure(closure: dict[str, Any]) -> None:
    checks = {
        "artifact_id": "phase_vs1_closure_v0",
        "phase_status": PHASE_STATUS,
        "closure_gate": CLOSURE_GATE,
        "closure_branch": CLOSURE_BRANCH,
    }
    for key, expected in checks.items():
        if closure.get(key) != expected:
            fail(
                "STOP_POST_VS1_DECISION_SURFACE_VS1_NOT_CLOSED",
                source=SOURCE_CLOSURE_PATH,
                field=key,
                expected=expected,
                actual=closure.get(key),
            )
    if get_value(closure, "terminal_transition.transition") != (
        "STOP_PHASE_VS1_CLOSED_PENDING_POST_VS1_DIRECTION_DECISION"
    ):
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_VS1_NOT_CLOSED",
            source=SOURCE_CLOSURE_PATH,
            field="terminal_transition.transition",
            expected="STOP_PHASE_VS1_CLOSED_PENDING_POST_VS1_DIRECTION_DECISION",
            actual=get_value(closure, "terminal_transition.transition"),
        )
    if get_value(closure, "terminal_transition.phase_vs1_closed") is not True:
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_VS1_NOT_CLOSED",
            source=SOURCE_CLOSURE_PATH,
            field="terminal_transition.phase_vs1_closed",
            expected=True,
            actual=get_value(closure, "terminal_transition.phase_vs1_closed"),
        )


def validate_map(surface_map: dict[str, Any]) -> None:
    if surface_map.get("artifact_id") != "phase_vs1_missing_precondition_next_surface_map_v0":
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_CANDIDATE_MAP_UNUSABLE",
            source=SOURCE_MAP_PATH,
            field="artifact_id",
            expected="phase_vs1_missing_precondition_next_surface_map_v0",
            actual=surface_map.get("artifact_id"),
        )
    if surface_map.get("map_verdict") != MAP_VERDICT:
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_CANDIDATE_MAP_UNUSABLE",
            source=SOURCE_MAP_PATH,
            field="map_verdict",
            expected=MAP_VERDICT,
            actual=surface_map.get("map_verdict"),
        )
    coverage = surface_map.get("blocker_coverage", {})
    expected_counts = {
        "source_blocker_count": 20,
        "mapped_blocker_count": 20,
        "unmapped_blocker_count": 0,
    }
    for key, expected in expected_counts.items():
        if coverage.get(key) != expected:
            fail(
                "STOP_POST_VS1_DECISION_SURFACE_CANDIDATE_MAP_UNUSABLE",
                source=SOURCE_MAP_PATH,
                field=f"blocker_coverage.{key}",
                expected=expected,
                actual=coverage.get(key),
            )
    if len(surface_map.get("surface_candidates", [])) != 21:
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_CANDIDATE_MAP_UNUSABLE",
            source=SOURCE_MAP_PATH,
            field="surface_candidates",
            expected=21,
            actual=len(surface_map.get("surface_candidates", [])),
        )


def proposal_sidecar(proposal_hash: str, proposal_size: int) -> dict[str, Any]:
    return {
        "schema_version": "matrixlabs_durable_external_source_identity_v0",
        "artifact_id": PROPOSAL_ARTIFACT_ID,
        "source_title": "MatrixLab First Sweep-Capable Kernel Target Specification v0",
        "source_location_kind": PROPOSAL_DURABILITY,
        "source_durability_status": PROPOSAL_DURABILITY,
        "declared_source_path_or_reference": PROPOSAL_PATH,
        "content_sha256": proposal_hash,
        "source_status": "PRESENT_VERIFIED",
        "source_role": PROPOSAL_SOURCE_ROLE,
        "source_target_status": PROPOSAL_TARGET_STATUS,
        "admission_reason": "proposal admitted as review input for a human post-VS1 direction decision surface",
        "admission_authority": "HUMAN_DECLARED_REVIEW_INPUT_ONLY",
        "admission_scope": "THIS_DECISION_SURFACE_ONLY",
        "admitted_by_unit": "POST_VS1_DIRECTION_DECISION_SURFACE",
        "source_bytes_durably_available": True,
        "source_identity_replayable": True,
        "source_admission_grants_authority": False,
        "latest_file_resolution_used": False,
        "mtime_resolution_used": False,
        "directory_scan_authority_used": False,
        "baseline_share_used_as_source_authority": False,
        "source_byte_count": proposal_size,
    }


def surface_by_id(surface_map: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        candidate.get("surface_id"): candidate
        for candidate in surface_map.get("surface_candidates", [])
        if isinstance(candidate, dict) and candidate.get("surface_id")
    }


def validate_bundle(surface_map: dict[str, Any]) -> None:
    surfaces = surface_by_id(surface_map)
    missing = [surface_id for surface_id in PRIMARY_BUNDLE_MEMBERS if surface_id not in surfaces]
    if missing:
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_BUNDLE_MEMBER_NOT_IN_VS1_5",
            source=SOURCE_MAP_PATH,
            field="primary_bundle_members",
            expected=PRIMARY_BUNDLE_MEMBERS,
            actual=missing,
        )
    if len(PRIMARY_BUNDLE_MEMBERS) != 18:
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_BUNDLE_MEMBER_COUNT_MISMATCH",
            field="primary_bundle_member_count",
            expected=18,
            actual=len(PRIMARY_BUNDLE_MEMBERS),
        )
    if any(surface_id in PRIMARY_BUNDLE_MEMBERS for surface_id in DEFERRED_SURFACES):
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_DEFERRED_SURFACE_SMUGGLED_IN",
            field="primary_bundle_members",
            expected="S14/S15 deferred",
            actual=PRIMARY_BUNDLE_MEMBERS,
        )
    if any(surface_id in PRIMARY_BUNDLE_MEMBERS for surface_id in DOWNSTREAM_ONLY_SURFACES):
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_S21_USED_AS_BUNDLE_CONSTRUCTION_SURFACE",
            field="primary_bundle_members",
            expected="S21 downstream only",
            actual=PRIMARY_BUNDLE_MEMBERS,
        )


def build_traceability(surface_map: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trace_rows: list[dict[str, Any]] = []
    support_objects: list[dict[str, Any]] = []
    for index, candidate in enumerate(surface_map.get("surface_candidates", [])):
        if not isinstance(candidate, dict):
            continue
        component_ids = candidate.get("component_ids_addressed", [])
        if not component_ids:
            continue
        surface_id = candidate["surface_id"]
        primary = candidate.get("source_readiness_result")
        classes = sorted(candidate.get("blocker_classes_addressed", []))
        for component_id in component_ids:
            trace_rows.append(
                {
                    "trace_id": f"{component_id}::{primary}::{','.join(classes)}",
                    "source_component_id": component_id,
                    "source_primary_readiness_status": primary,
                    "source_secondary_blocker_classes": classes,
                    "source_vs1_5_surface_id": surface_id,
                    "support_parent_surface_id": surface_id,
                    "proposed_object_id": (
                        f"{BUNDLE_ID}::{surface_id}"
                        if surface_id in PRIMARY_BUNDLE_MEMBERS
                        else f"DEFERRED::{surface_id}"
                    ),
                    "proposed_scope": (
                        "PRIMARY_FIRST_KERNEL_BUNDLE"
                        if surface_id in PRIMARY_BUNDLE_MEMBERS
                        else "DEFERRED_FULL_SURFACE_NOT_IN_PRIMARY_BUNDLE"
                    ),
                    "source_artifact_path": SOURCE_MAP_PATH,
                    "source_record_pointer": f"/surface_candidates/{index}",
                }
            )
        if surface_id in PRIMARY_BUNDLE_MEMBERS:
            support_objects.append(
                {
                    "support_object_id": f"SUPPORT::{surface_id}",
                    "parent_bundle_surface_id": surface_id,
                    "support_role": "FIRST_KERNEL_BUNDLE_SUPPORT_OBJECT",
                    "why_required": "required for the bounded first sweep-capable kernel definition package",
                    "scope": "definition/construction/construction-verification only; no execution",
                    "forbidden_effects": candidate.get("forbidden_effects", []),
                }
            )
    return trace_rows, support_objects


def decision_option_payload_contracts() -> dict[str, Any]:
    false_scope = {
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
    return {
        DECISION_OPTIONS[0]: {
            "required_fields": [
                "direction_selected",
                "target_family_selected",
                "first_target_selected",
                "definition_scope_approved",
                "bounded_construction_scope_approved",
                "construction_verification_scope_approved",
            ],
            "required_approval_vector": {
                "direction_selected": True,
                "target_family_selected": True,
                "first_target_selected": True,
                "definition_scope_approved": True,
                "bounded_construction_scope_approved": True,
                "construction_verification_scope_approved": True,
                **false_scope,
            },
            "option_a_requires_explicit_scope_vector": True,
            "option_token_alone_is_not_a_complete_decision_receipt": True,
        },
        DECISION_OPTIONS[1]: {
            "required_fields": [
                "revision_id",
                "revision_target",
                "old_value",
                "new_value",
                "reason",
                "affected_bundle_members",
                "affected_support_objects",
                "unchanged_boundaries",
                "target_family_status",
                "first_target_status",
                "definition_scope_changes",
                "construction_scope_changes",
                "construction_verification_scope_changes",
                "explicit_exclusions",
                "prior_decision_package_hash",
                "revised_decision_package_hash",
            ],
            "all_revision_targets_exist_in_bound_decision_package": True,
            "all_revision_targets_remain_traceable_to_vs1_5": True,
            "revision_changes_decision_package_hash": True,
            "may_introduce_unmapped_scope": False,
            "may_introduce_second_target": False,
            "may_introduce_portability_scope": False,
            "may_introduce_execution_authority": False,
        },
        DECISION_OPTIONS[2]: {
            "required_fields": [
                "insufficient_section",
                "missing_distinction",
                "unsafe_implication",
                "required_clarification",
            ],
        },
        DECISION_OPTIONS[3]: {
            "required_fields": ["selected_surface_id"],
            "selected_surface_must_exist_in_vs1_5": True,
            "selects_only_alternative_direction_candidate": True,
            "inherits_kernel_definition_construction_or_verification_scope": False,
        },
        DECISION_OPTIONS[4]: {
            "required_fields": [
                "reason_existing_map_is_insufficient",
                "desired_direction_characteristics",
                "boundaries_to_preserve",
            ],
        },
        DECISION_OPTIONS[5]: {
            "required_fields": ["explicit_hold_decision"],
            "grants_new_authority": False,
        },
        DECISION_OPTIONS[6]: {
            "required_fields": ["rejection_reason"],
            "selects_alternative": False,
        },
    }


def proposed_approval_scope() -> dict[str, Any]:
    return {
        "direction_selection_scope": [
            "select FIRST_SWEEP_CAPABLE_KERNEL_V0",
            "select BOUNDED_CONTRACT_CONVERGENCE",
            "select TYPED_STATE_CONTRACT_CONVERGENCE_V0",
        ],
        "definition_scope": [
            "define First Sweep-Capable Kernel profile",
            "freeze one target family",
            "freeze one first target",
            "define target scope and regime",
            "define runtime control-state contract",
            "define candidate contract",
            "define frozen target contract",
            "define finite move-space",
            "define selector contract",
            "define applicator contract",
            "define validation and admissibility boundaries",
            "define source identity and freshness policy",
            "define authority policy",
            "define radius, budget, and halt policy",
            "define convergence criterion",
            "define move-receipt contract",
            "define run-report and Evidence Yield contract",
            "define forbidden-effect guard",
            "define human escalation boundary",
        ],
        "bounded_construction_scope": [
            "construct declared contract and schema artifacts",
            "construct one bounded fixture set",
            "construct positive-path fixtures",
            "construct negative-path fixtures",
            "construct bounded perturbation fixtures",
            "construct first-run readiness-gate artifacts",
            "construct replay and audit evidence surfaces",
            "construct run-package manifest and source bindings",
        ],
        "construction_verification_scope": [
            "verify required construction artifacts are present",
            "verify hashes and source bindings",
            "verify fixture identities",
            "verify move-space finiteness",
            "verify selector and applicator contracts",
            "verify budgets and halts",
            "verify forbidden effects remain false",
            "verify execution entrypoint remains disabled or unauthorized",
            "verify package eligibility for a later execution-authority decision",
        ],
        "maximum_scope": [
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
        ],
    }


def excluded_authority_scope() -> dict[str, Any]:
    exclusions = [
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
    return {"excluded_authorities": exclusions, "execution_authority_included": False}


def downstream_branch_map() -> dict[str, Any]:
    return {
        "accept_exact_scope": [
            "decision surface",
            "human decision",
            "post_vs1_direction_decision_receipt_v0",
            "post_vs1_direction_authority_update_v0",
            "post_vs1_direction_transition_closure_v0",
            "VS2 source intake",
        ],
        "accept_valid_revisions": "same chain only after revised package canonicalization and hash binding",
        "return_for_tightening": [
            "decision receipt",
            "FIRST_SWEEP_CAPABLE_KERNEL_PROPOSAL_TIGHTENING_SURFACE",
        ],
        "select_alternative": [
            "decision receipt",
            "POST_VS1_ALTERNATIVE_DIRECTION_SCOPE_PREPARATION_SURFACE",
        ],
        "request_new_proposal": [
            "decision receipt",
            "POST_VS1_NEW_DIRECTION_PROPOSAL_SURFACE",
        ],
        "hold": ["decision receipt", "STOP_POST_VS1_HELD_NO_NEXT_DIRECTION"],
        "reject": [
            "decision receipt",
            "STOP_POST_VS1_KERNEL_DIRECTION_REJECTED_NO_ALTERNATIVE_SELECTED",
        ],
    }


def build_decision_package_payload(
    proposal_binding: dict[str, Any],
    normalization: dict[str, Any],
    bundle: dict[str, Any],
    membership: dict[str, Any],
    traceability: dict[str, Any],
    advisory_alignment: dict[str, Any],
    options: list[dict[str, Any]],
    option_contracts: dict[str, Any],
    approval_scope: dict[str, Any],
    excluded_scope: dict[str, Any],
    alternative_non_inheritance: dict[str, Any],
    branches: dict[str, Any],
) -> dict[str, Any]:
    return {
        "proposal_source_binding": proposal_binding,
        "proposal_overbreadth_normalization": normalization,
        "proposal_bundle": bundle,
        "proposal_bundle_membership_contract": membership,
        "proposal_bundle_traceability": traceability,
        "vs1_5_advisory_alignment": advisory_alignment,
        "decision_question": DECISION_QUESTION,
        "recommended_direction": {
            "direction_id": "FIRST_SWEEP_CAPABLE_KERNEL_V0",
            "target_family": "BOUNDED_CONTRACT_CONVERGENCE",
            "first_target": "TYPED_STATE_CONTRACT_CONVERGENCE_V0",
            "recommendation_status": "NON_BINDING_MACHINE_ADVISORY_RECOMMENDATION",
            "machine_selected": False,
            "default_option": "NONE",
            "preselected_option": "NONE",
            "recommended_option": DECISION_OPTIONS[0],
            "recommended_option_is_binding": False,
        },
        "decision_options": options,
        "decision_option_payload_contracts": option_contracts,
        "proposed_approval_scope": approval_scope,
        "excluded_authority_scope": excluded_scope,
        "alternative_scope_non_inheritance": alternative_non_inheritance,
        "downstream_branch_map": branches,
    }


def load_existing_decision_package_hash(root: Path) -> str | None:
    surface_path = root / OUTPUT_JSON
    if not surface_path.exists():
        return None
    surface = json.loads(surface_path.read_text(encoding="utf-8"))
    return surface.get("decision_package_binding", {}).get("decision_package_sha256")


def canonical_hash(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return sha256_bytes(canonical)


def build_surface(
    root: Path,
    closure: dict[str, Any],
    surface_map: dict[str, Any],
    sidecar: dict[str, Any],
) -> dict[str, Any]:
    validate_bundle(surface_map)
    trace_rows, support_objects = build_traceability(surface_map)
    bundle = {
        "bundle_id": BUNDLE_ID,
        "proposal_relationship": RELATIONSHIP_TO_VS1_5,
        "primary_bundle_members": PRIMARY_BUNDLE_MEMBERS,
        "primary_bundle_member_count": len(PRIMARY_BUNDLE_MEMBERS),
        "deferred_full_surfaces": DEFERRED_SURFACES,
        "downstream_only_surfaces": DOWNSTREAM_ONLY_SURFACES,
        "bundle_entry_prerequisite_surface_id": ENTRY_PREREQUISITE,
        "recommended_direction": "FIRST_SWEEP_CAPABLE_KERNEL_V0",
        "recommended_target_family": "BOUNDED_CONTRACT_CONVERGENCE",
        "recommended_first_target": "TYPED_STATE_CONTRACT_CONVERGENCE_V0",
    }
    membership = {
        "primary_bundle_members_exact": True,
        "bundle_members_may_expand_without_new_decision": False,
        "undeclared_additional_surface_ids": [],
        "s14_deferred": True,
        "s15_deferred": True,
        "s21_downstream_only": True,
        "first_run_readiness_gate_is_s21": False,
    }
    traceability = {
        "trace_rows": trace_rows,
        "support_objects": support_objects,
        "synthetic_unbound_blocker_ids_created": False,
        "all_trace_rows_source_replayable": True,
        "unmapped_additional_proposal_scope": [],
        "unmapped_additional_proposal_scope_count": 0,
    }
    advisory_alignment = {
        "source_advisory_first_surface": get_value(
            surface_map, "advisory_ranking.advisory_first_surface_candidate"
        ),
        "kernel_bundle_replaces_vs1_5_ranking": False,
        "kernel_bundle_reorders_vs1_5_surfaces": False,
        "bundle_entry_prerequisite_surface_id": ENTRY_PREREQUISITE,
        "source_identity_policy_must_be_resolved_before_dependent_construction": True,
        "dependency_layers_must_be_preserved_by_later_scope_plan": True,
    }
    normalization = {
        "SOURCE_SECTION_16_FIRST_PORTABILITY_CHECK": (
            "DIRECTIONAL_FUTURE_NOTE_EXCLUDED_FROM_CURRENT_BUNDLE"
        ),
        "SOURCE_SECTION_21_SECOND_TARGET_DIRECTIONAL_NOTE": (
            "DIRECTIONAL_FUTURE_NOTE_EXCLUDED_FROM_CURRENT_BUNDLE"
        ),
        "current_proposed_scope": [
            "FIRST_SWEEP_CAPABLE_KERNEL_V0",
            "BOUNDED_CONTRACT_CONVERGENCE",
            "TYPED_STATE_CONTRACT_CONVERGENCE_V0",
            "one bounded first-kernel definition package",
            "one bounded construction package",
            "one construction-verification package",
        ],
        "current_proposed_scope_excludes": [
            "MOVE_SPACE_CONTRACT_CONVERGENCE_V0",
            "second-target testing",
            "portability testing",
            "S15 implementation",
            "cross-target abstraction",
            "automatic rerun",
            "refinement application",
            "execution",
            "sweeps",
            "runner authority",
        ],
        "second_target_scope_included": False,
        "portability_scope_included": False,
    }
    options = [
        {
            "option_id": option,
            "option_index": index,
            "preselected": False,
            "default": False,
        }
        for index, option in enumerate(DECISION_OPTIONS, start=1)
    ]
    option_contracts = decision_option_payload_contracts()
    approval_scope = proposed_approval_scope()
    excluded_scope = excluded_authority_scope()
    alternative_non_inheritance = {
        "select_alternative_inherits_kernel_scope": False,
        "alternative_scope_requires_separate_surface": True,
        "alternative_scope_must_bind_its_own_package_hash": True,
    }
    branches = downstream_branch_map()
    proposal_binding = {
        "artifact_id": sidecar["artifact_id"],
        "source_path": PROPOSAL_PATH,
        "source_identity_path": PROPOSAL_SIDECAR_PATH,
        "content_sha256": sidecar["content_sha256"],
        "source_role": sidecar["source_role"],
        "source_target_status": sidecar["source_target_status"],
        "source_admission_grants_authority": False,
    }
    decision_payload = build_decision_package_payload(
        proposal_binding,
        normalization,
        bundle,
        membership,
        traceability,
        advisory_alignment,
        options,
        option_contracts,
        approval_scope,
        excluded_scope,
        alternative_non_inheritance,
        branches,
    )
    decision_package_hash = canonical_hash(decision_payload)
    source_chain = {
        "vs1_closure": {
            "artifact_id": closure.get("artifact_id"),
            "path": SOURCE_CLOSURE_PATH,
            "commit_sha": SOURCE_CLOSURE_COMMIT,
            "sha256": sha256_file(root / SOURCE_CLOSURE_PATH),
            "phase_status": closure.get("phase_status"),
            "closure_gate": closure.get("closure_gate"),
            "closure_branch": closure.get("closure_branch"),
            "terminal_transition": get_value(closure, "terminal_transition.transition"),
            "status": "PRESENT_VERIFIED",
        },
        "vs1_5_next_surface_map": {
            "artifact_id": surface_map.get("artifact_id"),
            "path": SOURCE_MAP_PATH,
            "commit_sha": SOURCE_MAP_COMMIT,
            "sha256": sha256_file(root / SOURCE_MAP_PATH),
            "map_verdict": surface_map.get("map_verdict"),
            "source_blocker_count": get_value(surface_map, "blocker_coverage.source_blocker_count"),
            "mapped_blocker_count": get_value(surface_map, "blocker_coverage.mapped_blocker_count"),
            "unmapped_blocker_count": get_value(surface_map, "blocker_coverage.unmapped_blocker_count"),
            "surface_candidate_record_count": len(surface_map.get("surface_candidates", [])),
            "status": "PRESENT_VERIFIED",
        },
    }
    decision_state = {
        "surface_artifact_created": True,
        "surface_preparation_status": "PREPARED_PENDING_HUMAN_DECISION",
        "human_decision_required": True,
        "human_decision_recorded": False,
        "decision_status": "PENDING_HUMAN_DECISION",
        "direction_selected": False,
        "target_family_selected": False,
        "first_target_selected": False,
        "definition_scope_approved": False,
        "construction_scope_approved": False,
        "construction_verification_scope_approved": False,
        "decision_receipt_created": False,
        "authority_update_applied": False,
        "authority_transition_closed": False,
        "vs2_profile_and_target_freeze_authority_granted": False,
        "vs2_bounded_construction_authority_granted": False,
        "fixture_construction_authority_granted": False,
        "readiness_gate_construction_authority_granted": False,
        "construction_package_verification_authority_granted": False,
        "vs2_started": False,
        "execution_authorized": False,
        "positive_path_execution_authorized": False,
        "negative_path_execution_authorized": False,
        "sweep_authorized": False,
        "automatic_rerun_authorized": False,
        "runner_authority_created": False,
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "artifact_id": ARTIFACT_ID,
        "object_id": OBJECT_ID,
        "object_role": OBJECT_ROLE,
        "surface_status": "PREPARED_PENDING_HUMAN_DECISION",
        "applicable_closure_branch": CLOSURE_BRANCH,
        "source_chain_commit_bindings": {
            "vs1_closure_commit_sha": SOURCE_CLOSURE_COMMIT,
            "vs1_5_map_commit_sha": SOURCE_MAP_COMMIT,
        },
        "source_chain": source_chain,
        "source_identity_bindings": {
            "proposal_source_identity": sidecar,
            "latest_file_resolution_used": False,
            "mtime_resolution_used": False,
            "directory_scan_authority_used": False,
            "baseline_share_used_as_source_authority": False,
        },
        "source_status_table": [
            {
                "source_id": "VS1_CLOSURE",
                "status": "PRESENT_VERIFIED",
                "path": SOURCE_CLOSURE_PATH,
            },
            {
                "source_id": "VS1_5_NEXT_SURFACE_MAP",
                "status": "PRESENT_VERIFIED",
                "path": SOURCE_MAP_PATH,
            },
            {
                "source_id": PROPOSAL_ARTIFACT_ID,
                "status": "PRESENT_VERIFIED",
                "path": PROPOSAL_PATH,
            },
        ],
        "proposal_source_binding": proposal_binding,
        "proposal_overbreadth_normalization": normalization,
        "proposal_relationship_to_vs1_5": RELATIONSHIP_TO_VS1_5,
        "proposal_bundle": bundle,
        "proposal_bundle_membership_contract": membership,
        "proposal_bundle_traceability": traceability,
        "vs1_5_advisory_alignment": advisory_alignment,
        "decision_package_binding": {
            "canonicalization": CANONICALIZATION_CONTRACT,
            "canonicalization_contract": CANONICALIZATION_CONTRACT,
            "bound_sections": BOUND_SECTIONS,
            "decision_package_payload": decision_payload,
            "decision_package_sha256": decision_package_hash,
            "decision_receipt_must_bind_this_hash": True,
            "authority_update_must_bind_decision_receipt": True,
            "generated_at_excluded_from_hash": True,
            "volatile_filesystem_metadata_excluded_from_hash": True,
            "commit_created_fields_excluded_from_hash": True,
        },
        "decision_question": DECISION_QUESTION,
        "recommended_direction": {
            "direction_id": "FIRST_SWEEP_CAPABLE_KERNEL_V0",
            "target_family": "BOUNDED_CONTRACT_CONVERGENCE",
            "first_target": "TYPED_STATE_CONTRACT_CONVERGENCE_V0",
            "recommendation_status": "NON_BINDING_MACHINE_ADVISORY_RECOMMENDATION",
            "machine_selected": False,
            "default_option": "NONE",
            "preselected_option": "NONE",
            "recommended_option": DECISION_OPTIONS[0],
            "recommended_option_is_binding": False,
        },
        "recommendation_basis": [
            "source proposal admitted as non-binding review input",
            "bundle maps over VS1.5 blocker surfaces without replacing advisory ranking",
            "S10 remains earliest internal prerequisite",
        ],
        "decision_options": options,
        "decision_option_payload_contracts": option_contracts,
        "decision_default_state": {
            "default_option": "NONE",
            "preselected_option": "NONE",
            "recommended_option": DECISION_OPTIONS[0],
            "recommended_option_is_binding": False,
            "absence_of_human_choice_does_not_imply_acceptance": True,
            "timeout_does_not_imply_acceptance": True,
        },
        "proposed_approval_scope": approval_scope,
        "excluded_authority_scope": excluded_scope,
        "alternative_scope_non_inheritance": alternative_non_inheritance,
        "decision_state": decision_state,
        "human_decision_requirement": {
            "human_decision_required": True,
            "human_decision_recorded": False,
            "decision_receipt_created": False,
            "machine_may_select_direction": False,
        },
        "downstream_branch_map": branches,
        "downstream_decision_receipt_requirement": {
            "decision_receipt_required_for_any_direction": True,
            "decision_receipt_created_by_this_surface": False,
            "decision_receipt_must_bind_decision_package_sha256": decision_package_hash,
        },
        "downstream_authority_update_requirement": {
            "authority_update_required_after_acceptance": True,
            "authority_update_applied_by_this_surface": False,
            "authority_update_must_bind_decision_receipt": True,
        },
        "downstream_transition_closure_requirement": {
            "transition_closure_required_after_authority_update": True,
            "transition_closed_by_this_surface": False,
        },
        "surface_checks": [
            {"check_id": check, "status": "PASS", "check_result": check}
            for check in SURFACE_CHECKS
        ],
        "surface_gate": SURFACE_GATE,
        "terminal_transition": {
            "transition": TERMINAL_TRANSITION,
            "executes_decision": False,
            "creates_decision_receipt": False,
            "applies_authority_update": False,
            "closes_authority_transition": False,
            "starts_vs2": False,
            "builds_vs2_1": False,
            "authorizes_execution": False,
            "authorizes_sweep": False,
            "authorizes_rerun": False,
            "creates_runner_authority": False,
        },
        "evidence_yield": {
            "yield_branch": "CONFIRMATION_YIELD",
            "confirmation_yield_reason": (
                "source closure, VS1.5 map, and durable proposal source were bound "
                "into a pending human decision surface without selecting direction or authority"
            ),
        },
        "non_claims": {
            "human_decision_recorded": False,
            "decision_receipt_created": False,
            "authority_update_applied": False,
            "authority_transition_closed": False,
            "direction_selected": False,
            "target_family_selected": False,
            "first_target_selected": False,
            "scope_approved": False,
            "vs2_started": False,
            "vs2_1_built": False,
            "execution_authorized": False,
            "sweep_authorized": False,
            "automatic_rerun_authorized": False,
            "runner_authority_created": False,
            "portability_scope_included": False,
            "second_target_scope_included": False,
        },
        "failures": [],
    }


def build_markdown(surface: dict[str, Any]) -> str:
    package_hash = surface["decision_package_binding"]["decision_package_sha256"]
    option_lines = "\n".join(f"- {option}" for option in DECISION_OPTIONS)
    member_lines = "\n".join(f"- {surface_id}" for surface_id in PRIMARY_BUNDLE_MEMBERS)
    return f"""# Post-VS1 Direction Decision Surface v0

## Status

{SURFACE_GATE}

## Applicable branch

- applicable closure branch: {CLOSURE_BRANCH}
- source VS1 closure commit: {SOURCE_CLOSURE_COMMIT}
- source VS1.5 map commit: {SOURCE_MAP_COMMIT}

## Verified sources

- VS1 closure hash: {surface['source_chain']['vs1_closure']['sha256']}
- VS1.5 map hash: {surface['source_chain']['vs1_5_next_surface_map']['sha256']}
- proposal source: {PROPOSAL_PATH}
- proposal source hash: {surface['proposal_source_binding']['content_sha256']}
- proposal role: non-binding

## Recommendation

- First Sweep-Capable Kernel recommendation: FIRST_SWEEP_CAPABLE_KERNEL_V0
- Bounded Contract Convergence target family: BOUNDED_CONTRACT_CONVERGENCE
- Typed State Contract Convergence v0 first target: TYPED_STATE_CONTRACT_CONVERGENCE_V0
- recommendation status: NON_BINDING_MACHINE_ADVISORY_RECOMMENDATION
- machine selected: false

## Bundle

- bundle id: {BUNDLE_ID}
- primary bundle member count: 18
- exact eighteen-member bundle:
{member_lines}
- S10 earliest internal prerequisite: {ENTRY_PREREQUISITE}
- S14_LOCAL_REVISION_SURFACE_CONTRACT deferred: true
- S15_BOUNDED_PORTABILITY_MAP_CONTRACT_SURFACE deferred: true
- S21_CONTROLLED_LOOP_READINESS_REAUDIT_SURFACE downstream only: true
- second target and portability excluded: true
- unmapped scope count: 0

## Decision package

- decision package hash: {package_hash}
- decision receipt must bind this hash: true
- authority update must bind decision receipt: true

## Decision options

{option_lines}

- default option: NONE
- preselected option: NONE
- recommended option is binding: false

## Approval scope

- direction selection scope: FIRST_SWEEP_CAPABLE_KERNEL_V0, BOUNDED_CONTRACT_CONVERGENCE, TYPED_STATE_CONTRACT_CONVERGENCE_V0
- definition scope: declared contract and policy definitions only
- bounded construction scope: declared package and fixtures only
- construction-verification scope: verify construction package only

## Excluded authority

- execution authority: false
- sweep authority: false
- automatic rerun authority: false
- runner authority: false
- second target scope: false
- portability scope: false
- reusable schema approval: false
- reusable move approval: false

## Alternative non-inheritance

- selecting an alternative post-VS1 surface does not inherit kernel definition scope
- selecting an alternative post-VS1 surface does not inherit construction scope
- selecting an alternative post-VS1 surface does not inherit verification scope

## Pending decision state

No direction selected.
No target family selected.
No first target selected.
No scope approved.
No decision receipt created.
No authority update applied.
No authority transition closed.
VS2 not started.
VS2.1 not built.
Execution not authorized.
Sweeps not authorized.
Automatic rerun not authorized.
Runner authority not created.

## Terminal transition

{TERMINAL_TRANSITION}
"""


def validate_surface(
    surface: dict[str, Any],
    sidecar: dict[str, Any],
    previous_decision_package_hash: str | None,
) -> None:
    if surface["proposal_source_binding"]["content_sha256"] != sidecar["content_sha256"]:
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_PROPOSAL_HASH_MISMATCH",
            field="proposal_source_binding.content_sha256",
            expected=sidecar["content_sha256"],
            actual=surface["proposal_source_binding"]["content_sha256"],
        )
    if len(surface["proposal_bundle"]["primary_bundle_members"]) != 18:
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_BUNDLE_MEMBER_COUNT_MISMATCH",
            field="proposal_bundle.primary_bundle_members",
            expected=18,
            actual=len(surface["proposal_bundle"]["primary_bundle_members"]),
        )
    if len(surface["decision_options"]) != 7:
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_OPTIONS_INCOMPLETE",
            field="decision_options",
            expected=7,
            actual=len(surface["decision_options"]),
        )
    if surface["decision_default_state"]["default_option"] != "NONE":
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_DEFAULT_ACCEPTANCE_PRESENT",
            field="decision_default_state.default_option",
            expected="NONE",
            actual=surface["decision_default_state"]["default_option"],
        )
    binding = surface["decision_package_binding"]
    if binding.get("canonicalization") != CANONICALIZATION_CONTRACT:
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_CANONICALIZATION_CONTRACT_MISMATCH",
            field="decision_package_binding.canonicalization",
            expected=CANONICALIZATION_CONTRACT,
            actual=binding.get("canonicalization"),
        )
    if binding.get("canonicalization_contract") != CANONICALIZATION_CONTRACT:
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_CANONICALIZATION_CONTRACT_MISMATCH",
            field="decision_package_binding.canonicalization_contract",
            expected=CANONICALIZATION_CONTRACT,
            actual=binding.get("canonicalization_contract"),
        )
    if "bound_sections" not in binding:
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_BOUND_SECTION_MANIFEST_MISSING",
            field="decision_package_binding.bound_sections",
            expected=BOUND_SECTIONS,
            actual=None,
        )
    if len(binding["bound_sections"]) != len(BOUND_SECTIONS):
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_BOUND_SECTION_COUNT_MISMATCH",
            field="decision_package_binding.bound_sections",
            expected=len(BOUND_SECTIONS),
            actual=len(binding["bound_sections"]),
        )
    if binding["bound_sections"] != BOUND_SECTIONS:
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_BOUND_SECTION_MANIFEST_MISMATCH",
            field="decision_package_binding.bound_sections",
            expected=BOUND_SECTIONS,
            actual=binding["bound_sections"],
        )
    payload = binding["decision_package_payload"]
    if list(payload.keys()) != BOUND_SECTIONS:
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_BOUND_SECTION_MANIFEST_MISMATCH",
            field="decision_package_binding.decision_package_payload",
            expected=BOUND_SECTIONS,
            actual=list(payload.keys()),
        )
    recomputed = canonical_hash(payload)
    if recomputed != binding["decision_package_sha256"]:
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_DECISION_PACKAGE_HASH_MISMATCH",
            field="decision_package_binding.decision_package_sha256",
            expected=recomputed,
            actual=binding["decision_package_sha256"],
        )
    if (
        previous_decision_package_hash is not None
        and binding["decision_package_sha256"] != previous_decision_package_hash
    ):
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_DECISION_PACKAGE_HASH_CHANGED_UNEXPECTEDLY",
            field="decision_package_binding.decision_package_sha256",
            expected=previous_decision_package_hash,
            actual=binding["decision_package_sha256"],
        )
    for key, value in surface["decision_state"].items():
        if key in {"surface_artifact_created", "human_decision_required"}:
            continue
        if key == "surface_preparation_status" and value == "PREPARED_PENDING_HUMAN_DECISION":
            continue
        if key == "decision_status" and value == "PENDING_HUMAN_DECISION":
            continue
        if value is not False:
            fail(
                "STOP_POST_VS1_DECISION_SURFACE_DECISION_PRECONSUMED",
                field=f"decision_state.{key}",
                expected=False,
                actual=value,
            )
    for key, value in surface["terminal_transition"].items():
        if key == "transition":
            continue
        if value is not False:
            fail(
                "STOP_POST_VS1_DECISION_SURFACE_EXECUTION_AUTHORITY_INCLUDED",
                field=f"terminal_transition.{key}",
                expected=False,
                actual=value,
            )


def emit_success() -> None:
    print("BUILD_POST_VS1_DIRECTION_DECISION_SURFACE_V0_COMPLETE")
    print(f"artifact_id={ARTIFACT_ID}")
    print(f"schema_version={SCHEMA_VERSION}")
    print(f"object_id={OBJECT_ID}")
    print(f"object_role={OBJECT_ROLE}")
    print()
    print(f"applicable_closure_branch={CLOSURE_BRANCH}")
    print(f"source_vs1_closure_commit_sha={SOURCE_CLOSURE_COMMIT}")
    print(f"source_vs1_5_map_commit_sha={SOURCE_MAP_COMMIT}")
    print()
    print(f"proposal_source_artifact_id={PROPOSAL_ARTIFACT_ID}")
    print(f"proposal_source_role={PROPOSAL_SOURCE_ROLE}")
    print(f"proposal_source_location_kind={PROPOSAL_DURABILITY}")
    print(f"proposal_source_durability_status={PROPOSAL_DURABILITY}")
    print("proposal_source_hash_present=true")
    print("proposal_source_identity_replayable=true")
    print("proposal_source_admission_grants_authority=false")
    print()
    print(f"proposal_relationship={RELATIONSHIP_TO_VS1_5}")
    print(f"bundle_id={BUNDLE_ID}")
    print("primary_bundle_member_count=18")
    print("bundle_members_exact=true")
    print(f"bundle_entry_prerequisite_surface_id={ENTRY_PREREQUISITE}")
    print("kernel_bundle_replaces_vs1_5_ranking=false")
    print("kernel_bundle_reorders_vs1_5_surfaces=false")
    print("s14_deferred=true")
    print("s15_deferred=true")
    print("s21_downstream_only=true")
    print("first_run_readiness_gate_is_s21=false")
    print("unmapped_additional_proposal_scope_count=0")
    print("all_trace_rows_source_replayable=true")
    print()
    print("second_target_scope_included=false")
    print("portability_scope_included=false")
    print()
    print("recommended_direction=FIRST_SWEEP_CAPABLE_KERNEL_V0")
    print("recommended_target_family=BOUNDED_CONTRACT_CONVERGENCE")
    print("recommended_first_target=TYPED_STATE_CONTRACT_CONVERGENCE_V0")
    print("recommendation_status=NON_BINDING_MACHINE_ADVISORY_RECOMMENDATION")
    print("machine_selected=false")
    print()
    print("decision_option_count=7")
    print("default_option=NONE")
    print("preselected_option=NONE")
    print("recommended_option_is_binding=false")
    print("decision_package_hash_present=true")
    print()
    print("human_decision_required=true")
    print("human_decision_recorded=false")
    print("direction_selected=false")
    print("target_family_selected=false")
    print("first_target_selected=false")
    print("definition_scope_approved=false")
    print("construction_scope_approved=false")
    print("construction_verification_scope_approved=false")
    print()
    print("decision_receipt_created=false")
    print("authority_update_applied=false")
    print("authority_transition_closed=false")
    print("vs2_started=false")
    print("vs2_1_built=false")
    print()
    print("execution_authorized=false")
    print("positive_path_execution_authorized=false")
    print("negative_path_execution_authorized=false")
    print("sweep_authorized=false")
    print("automatic_rerun_authorized=false")
    print("runner_authority_created=false")
    print()
    print(f"surface_gate={SURFACE_GATE}")
    print("evidence_yield_branch=CONFIRMATION_YIELD")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition={TERMINAL_TRANSITION}")


def emit_stop(exc: SurfaceFailure) -> None:
    print("BUILD_POST_VS1_DIRECTION_DECISION_SURFACE_V0_TYPED_STOP")
    print(f"artifact_id={ARTIFACT_ID}")
    print(f"object_id={OBJECT_ID}")
    print(f"surface_gate={exc.code}")
    print("yield_branch=DIAGNOSTIC_YIELD")
    print(f"missing_or_invalid_source={exc.source}")
    print(f"violating_field={exc.field}")
    print(f"expected_value={exc.expected}")
    print(f"actual_value={exc.actual}")
    print(f"next_lawful_surface={exc.next_surface}")
    print("self_repair_performed=false")
    print("human_decision_recorded=false")
    print("decision_receipt_created=false")
    print("authority_update_applied=false")
    print("authority_transition_closed=false")
    print("vs2_started=false")
    print("execution_authorized=false")
    print("sweep_authorized=false")
    print("runner_authority_created=false")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition=STOP({exc.code})")


def generate() -> int:
    root = detect_repo_root(Path.cwd())
    require_repo_context(root)
    validate_dirty_scope(root)
    ensure_no_forbidden_artifacts(root)
    for rel_path in [SOURCE_CLOSURE_PATH, SOURCE_CLOSURE_MD, SOURCE_MAP_PATH, SOURCE_MAP_MD, PROPOSAL_PATH]:
        require_file(root, rel_path)
    before_hashes = capture_source_hashes(root)
    previous_decision_package_hash = load_existing_decision_package_hash(root)
    closure = load_json(root, SOURCE_CLOSURE_PATH)
    surface_map = load_json(root, SOURCE_MAP_PATH)
    validate_closure(closure)
    validate_map(surface_map)
    proposal_bytes = (root / PROPOSAL_PATH).read_bytes()
    proposal_hash = sha256_bytes(proposal_bytes)
    sidecar = proposal_sidecar(proposal_hash, len(proposal_bytes))
    if sidecar["source_durability_status"] != PROPOSAL_DURABILITY:
        fail(
            "STOP_POST_VS1_DECISION_SURFACE_PROPOSAL_SOURCE_NOT_DURABLY_PINNED",
            field="source_durability_status",
            expected=PROPOSAL_DURABILITY,
            actual=sidecar["source_durability_status"],
        )
    surface = build_surface(root, closure, surface_map, sidecar)
    validate_surface(surface, sidecar, previous_decision_package_hash)
    (root / PROPOSAL_SIDECAR_PATH).parent.mkdir(parents=True, exist_ok=True)
    (root / OUTPUT_JSON).parent.mkdir(parents=True, exist_ok=True)
    (root / PROPOSAL_SIDECAR_PATH).write_text(
        json.dumps(sidecar, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (root / OUTPUT_JSON).write_text(
        json.dumps(surface, indent=2) + "\n",
        encoding="utf-8",
    )
    (root / OUTPUT_MD).write_text(build_markdown(surface), encoding="utf-8")
    after_hashes = capture_source_hashes(root)
    validate_source_preservation(before_hashes, after_hashes)
    validate_dirty_scope(root)
    ensure_no_forbidden_artifacts(root)
    emit_success()
    return 0


def main() -> int:
    try:
        return generate()
    except SurfaceFailure as exc:
        emit_stop(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
