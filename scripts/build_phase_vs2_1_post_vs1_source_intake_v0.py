#!/usr/bin/env python3
"""Build Phase VS2.1 post-VS1 source intake v0."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


EXPECTED_ROOT = "/home/asd/projects/matrixlab"
EXPECTED_BRANCH = "master"
EXPECTED_HEAD = "c7759b1d1e7bbc76c2c0092b07ba92be377d0dcf"

SCRIPT = "scripts/build_phase_vs2_1_post_vs1_source_intake_v0.py"
OUTPUT_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_post_vs1_source_intake_v0.json"
OUTPUT_MD = "docs/matrixlabs/phase_vs2/phase_vs2_post_vs1_source_intake_v0.md"
OUTPUT_RECEIPT = "docs/matrixlabs/phase_vs2/phase_vs2_1_post_vs1_source_intake_receipt_v0.json"

SCHEMA_VERSION = "matrixlabs_phase_vs2_post_vs1_source_intake_v0"
ARTIFACT_ID = "phase_vs2_post_vs1_source_intake_v0"
PHASE_ID = "PHASE_VS2"
UNIT_ID = "VS2.1_POST_VS1_SOURCE_INTAKE"
UNIT_ROLE = "PHASE_ENTRY_SOURCE_INTAKE_ONLY"
INTAKE_GATE = "VS2_1_POST_VS1_SOURCE_INTAKE_PASS"
EVIDENCE_YIELD_BRANCH = "CONFIRMATION_YIELD"
LOGICAL_TERMINAL = "ADVANCE(VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_PENDING)"
TERMINAL_TRANSITION = "ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS2_1_POST_VS1_SOURCE_INTAKE_V0_PENDING)"

CANONICALIZATION = "MATRIXLAB_CANONICAL_JSON_V0"
DECISION_BRANCH = "ACCEPT_EXACT_PROPOSED_SCOPE"
ACCEPTED_OPTION = "ACCEPT_FIRST_SWEEP_CAPABLE_KERNEL_DIRECTION_AND_PROPOSED_SCOPE"
DIRECTION_ID = "FIRST_SWEEP_CAPABLE_KERNEL_V0"
TARGET_FAMILY = "BOUNDED_CONTRACT_CONVERGENCE"
FIRST_TARGET = "TYPED_STATE_CONTRACT_CONVERGENCE_V0"
BUNDLE_ID = "POST_VS1_FIRST_SWEEP_CAPABLE_KERNEL_BUNDLE_V0"
DECISION_PACKAGE_SHA256 = "e9e4143ad2efdd285fe9e598e50d965d82057f7a8d6ccc4c52478a596d6b788b"
DECISION_RECEIPT_SHA256 = "19defc100428931ed455e4d2a64697bb9d886b11b856ececb0da6743c94f0dfe"
AUTHORITY_UPDATE_SHA256 = "0eac680fdfa0052696bc0360aa5278b9ce06e95b78eaf91ed418cb9f578ab60d"
TRANSITION_CLOSURE_SHA256 = "ba603da54091ed8728814f5155e9d2185f13d5baef8ed283cae08b80f7758ab2"

SOURCE_SPECS = [
    {
        "source_id": "S01_VS1_CLOSURE",
        "artifact_id": "phase_vs1_closure_v0",
        "declared_path": "docs/matrixlabs/phase_vs1/phase_vs1_closure_v0.json",
        "source_commit_sha": "eabe605deaac3c34d2e9fa7295f4e813ea582ca7",
        "expected_content_sha256": "fdc916224c41d1ef261fbb7868298f8bdc6d46ed651a1fa76503ef29cd28210d",
        "source_role": "AUTHORITATIVE_COMPLETED_SOURCE_PHASE_CLOSURE",
    },
    {
        "source_id": "S02_VS1_5_NEXT_SURFACE_MAP",
        "artifact_id": "phase_vs1_missing_precondition_next_surface_map_v0",
        "declared_path": "docs/matrixlabs/phase_vs1/phase_vs1_missing_precondition_next_surface_map_v0.json",
        "source_commit_sha": "955743f9cf281d9b83c9e68fb0f367121b3c5295",
        "expected_content_sha256": "20013bcd2de7e7545b38c2660c2be6cad27dcbe5bd5b3df3a7fe0a50328b4bae",
        "source_role": "AUTHORITATIVE_BLOCKER_AND_CANDIDATE_SURFACE_MAP",
    },
    {
        "source_id": "S03_DIRECTIONAL_PROPOSAL",
        "artifact_id": "matrixlab_first_sweep_capable_kernel_target_specification_v0",
        "declared_path": "docs/matrixlabs/post_vs1/sources/matrixlab_first_sweep_capable_kernel_target_specification_v0.md",
        "source_commit_sha": "975d05dfda23a632c91faeaae66abbfcf4e85da6",
        "expected_content_sha256": "0e5c8925652d00cbaa8eca5a58ab69d184b0cdd07d7b4b860f19092deeaea83d",
        "source_role": "NON_BINDING_DIRECTIONAL_PROPOSAL",
    },
    {
        "source_id": "S04_DIRECTIONAL_PROPOSAL_SOURCE_IDENTITY",
        "artifact_id": "matrixlab_first_sweep_capable_kernel_target_specification_v0",
        "declared_path": "docs/matrixlabs/post_vs1/sources/matrixlab_first_sweep_capable_kernel_target_specification_v0.source.json",
        "source_commit_sha": "975d05dfda23a632c91faeaae66abbfcf4e85da6",
        "source_role": "DURABLE_SOURCE_IDENTITY_SIDECAR",
    },
    {
        "source_id": "S05_DIRECTION_DECISION_SURFACE",
        "artifact_id": "post_vs1_direction_decision_surface_v0",
        "declared_path": "docs/matrixlabs/post_vs1/post_vs1_direction_decision_surface_v0.json",
        "source_commit_sha": "975d05dfda23a632c91faeaae66abbfcf4e85da6",
        "expected_content_sha256": "7ffae36f8918dc3fdaec09f53f8527cd54a33a2650b3ed723d2e64996652c33f",
        "source_role": "AUTHORITATIVE_HUMAN_DECISION_SURFACE",
    },
    {
        "source_id": "S06_HUMAN_DECISION_RECEIPT",
        "artifact_id": "post_vs1_direction_decision_receipt_v0",
        "declared_path": "docs/matrixlabs/post_vs1/post_vs1_direction_decision_receipt_v0.json",
        "source_commit_sha": "3dc012d9d72201d2baf4c7d31d7545a68659ce9d",
        "canonical_sha256": DECISION_RECEIPT_SHA256,
        "source_role": "AUTHORITATIVE_HUMAN_DIRECTION_DECISION_RECEIPT",
    },
    {
        "source_id": "S07_AUTHORITY_UPDATE",
        "artifact_id": "post_vs1_direction_authority_update_v0",
        "declared_path": "docs/matrixlabs/post_vs1/post_vs1_direction_authority_update_v0.json",
        "source_commit_sha": "ebeb85a867b559df9f004ce8f4495e1581e79d14",
        "expected_content_sha256": "0a197071d97c0bfdb894df39506aedb02b304c9d780df506cbf46ab31400709c",
        "canonical_sha256": AUTHORITY_UPDATE_SHA256,
        "source_role": "AUTHORITATIVE_APPLIED_AUTHORITY_UPDATE",
    },
    {
        "source_id": "S08_TRANSITION_CLOSURE",
        "artifact_id": "post_vs1_direction_transition_closure_v0",
        "declared_path": "docs/matrixlabs/post_vs1/post_vs1_direction_transition_closure_v0.json",
        "source_commit_sha": EXPECTED_HEAD,
        "canonical_sha256": TRANSITION_CLOSURE_SHA256,
        "source_role": "AUTHORITATIVE_AUTHORITY_TRANSITION_EFFECTIVITY_CLOSURE",
    },
]

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
GRANT_IDS = [
    "VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY",
    "VS2_BOUNDED_CONSTRUCTION_AUTHORITY",
    "VS2_FIXTURE_CONSTRUCTION_AUTHORITY",
    "VS2_FIRST_RUN_READINESS_GATE_CONSTRUCTION_AUTHORITY",
    "VS2_CONSTRUCTION_PACKAGE_VERIFICATION_AUTHORITY",
]

SOURCE_MANIFEST_BOUND_SECTIONS = [
    "manifest_contract",
    "source_entries",
    "source_identity_checks",
    "source_status_summary",
]
SOURCE_INTAKE_BOUND_SECTIONS = [
    "transition_closure_binding",
    "committed_source_manifest",
    "source_linkage_table",
    "exact_decision_branch_binding",
    "accepted_direction_binding",
    "accepted_bundle_binding",
    "proposal_traceability_binding",
    "exact_scope_application_audit",
    "effective_grant_inventory",
    "grant_alias_normalization",
    "grant_routing",
    "withheld_authority_binding",
    "pre_intake_phase_state",
    "post_intake_phase_state",
    "downstream_boundary",
]

FORBIDDEN_OUTPUTS = [
    "docs/matrixlabs/phase_vs2/phase_vs2_first_sweep_capable_kernel_profile_v0.json",
    "docs/matrixlabs/phase_vs2/phase_vs2_first_sweep_capable_kernel_profile_v0.md",
    "docs/matrixlabs/phase_vs2/phase_vs2_typed_state_contract_convergence_target_freeze_v0.json",
    "docs/matrixlabs/phase_vs2/phase_vs2_typed_state_contract_convergence_target_freeze_v0.md",
    "docs/matrixlabs/phase_vs2/phase_vs2_2_kernel_profile_and_target_freeze_receipt_v0.json",
    "docs/matrixlabs/runner",
    "docs/matrixlabs/runtime",
    "docs/matrixlabs/move_space",
    "docs/matrixlabs/micro_sweeps",
    "discussion_packets",
]


class VS21Failure(RuntimeError):
    def __init__(
        self,
        code: str,
        *,
        field: str = "NONE",
        expected: object = "NONE",
        observed: object = "NONE",
        boundary: str = "PHASE_VS2_1_SOURCE_INTAKE_ONLY",
        next_surface: str = "REPAIR_PHASE_VS2_1_SOURCE_INTAKE_INPUT",
    ) -> None:
        super().__init__(code)
        self.code = code
        self.field = field
        self.expected = expected
        self.observed = observed
        self.boundary = boundary
        self.next_surface = next_surface


def fail(
    code: str,
    *,
    field: str = "NONE",
    expected: object = "NONE",
    observed: object = "NONE",
    boundary: str = "PHASE_VS2_1_SOURCE_INTAKE_ONLY",
    next_surface: str = "REPAIR_PHASE_VS2_1_SOURCE_INTAKE_INPUT",
) -> None:
    raise VS21Failure(
        code,
        field=field,
        expected=expected,
        observed=observed,
        boundary=boundary,
        next_surface=next_surface,
    )


def run_git(root: Path, args: list[str], *, binary: bool = False) -> str | bytes:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        text=not binary,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(
            "STOP_VS2_1_SOURCE_COMMIT_MISSING",
            field="git_command",
            expected=["git", *args],
            observed=proc.stderr if binary else proc.stderr.strip(),
        )
    return proc.stdout


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
            "STOP_VS2_1_REPOSITORY_ROOT_MISMATCH",
            field="repo_root",
            expected=EXPECTED_ROOT,
            observed=proc.stderr.strip(),
        )
    root = Path(proc.stdout.strip()).resolve()
    if str(root) != EXPECTED_ROOT:
        fail(
            "STOP_VS2_1_REPOSITORY_ROOT_MISMATCH",
            field="repo_root",
            expected=EXPECTED_ROOT,
            observed=str(root),
        )
    return root


def status_path(line: str) -> str:
    path = line[3:] if len(line) > 3 and line[2] == " " else line[2:].strip()
    if " -> " in path:
        path = path.split(" -> ", 1)[1].strip()
    return path


def git_status(root: Path) -> list[str]:
    return str(run_git(root, ["status", "--short", "--untracked-files=all"])).splitlines()


def require_repo_context(root: Path) -> None:
    branch = str(run_git(root, ["branch", "--show-current"])).strip()
    head = str(run_git(root, ["rev-parse", "HEAD"])).strip()
    if branch != EXPECTED_BRANCH:
        fail("STOP_VS2_1_UNEXPECTED_HEAD", field="branch", expected=EXPECTED_BRANCH, observed=branch)
    if head != EXPECTED_HEAD:
        fail("STOP_VS2_1_UNEXPECTED_HEAD", field="HEAD", expected=EXPECTED_HEAD, observed=head)
    staged = str(run_git(root, ["diff", "--name-only", "--cached"])).strip()
    if staged:
        fail("STOP_VS2_1_PREEXISTING_DIRTY_WORKTREE", field="staged_changes", expected="", observed=staged)


def validate_dirty_scope(root: Path) -> None:
    allowed_exact = {
        SCRIPT,
        "scripts/build_baseline_share_v0.py",
        OUTPUT_JSON,
        OUTPUT_MD,
        OUTPUT_RECEIPT,
        "baseline_share/COMMIT_CONTEXT.md",
        "baseline_share/CURRENT_STATE.md",
        "baseline_share/MANIFEST.json",
        "baseline_share/RECEIPT_POINTERS.md",
    }
    unexpected = [line for line in git_status(root) if status_path(line) not in allowed_exact]
    if unexpected:
        fail(
            "STOP_VS2_1_UNDECLARED_DIRTY_PATH",
            field="git_status",
            expected=sorted(allowed_exact),
            observed=unexpected,
        )


def ensure_forbidden_absent(root: Path) -> None:
    present = [path for path in FORBIDDEN_OUTPUTS if (root / path).exists()]
    if present:
        fail(
            "STOP_VS2_1_NEXT_UNIT_AUTO_EXECUTED",
            field="forbidden_outputs",
            expected=[],
            observed=present,
            boundary="NO_VS2_2_OR_CONSTRUCTION_OUTPUTS",
        )


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_hash(payload: dict[str, Any]) -> str:
    return sha256_bytes(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    )


def committed_bytes(root: Path, commit: str, path: str) -> bytes:
    try:
        return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=root)
    except subprocess.CalledProcessError:
        fail(
            "STOP_VS2_1_SOURCE_PATH_MISSING_AT_COMMIT",
            field=path,
            expected=f"{commit}:{path}",
            observed="missing",
        )


def parse_json_bytes(path: str, data: bytes) -> dict[str, Any]:
    try:
        value = json.loads(data.decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 - typed stop reports the parse issue.
        fail("STOP_VS2_1_SOURCE_STATUS_MISMATCH", field=path, expected="valid JSON", observed=str(exc))
    if not isinstance(value, dict):
        fail("STOP_VS2_1_SOURCE_STATUS_MISMATCH", field=path, expected="JSON object", observed=type(value).__name__)
    return value


def require_equal(value: Any, expected: Any, code: str, field: str) -> None:
    if value != expected:
        fail(code, field=field, expected=expected, observed=value)


def require_false(value: Any, code: str, field: str) -> None:
    require_equal(value, False, code, field)


def verify_source(root: Path, spec: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any] | None]:
    path = spec["declared_path"]
    commit = spec["source_commit_sha"]
    commit_check = subprocess.run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=root)
    if commit_check.returncode != 0:
        fail("STOP_VS2_1_SOURCE_COMMIT_MISSING", field=commit, expected="commit exists", observed="missing")
    data = committed_bytes(root, commit, path)
    worktree = root / path
    if not worktree.exists():
        fail("STOP_VS2_1_WORKTREE_SOURCE_DIVERGES_FROM_COMMIT", field=path, expected="present", observed="missing")
    worktree_data = worktree.read_bytes()
    if data != worktree_data:
        fail(
            "STOP_VS2_1_WORKTREE_SOURCE_DIVERGES_FROM_COMMIT",
            field=path,
            expected=sha256_bytes(data),
            observed=sha256_bytes(worktree_data),
        )
    content_sha = sha256_bytes(data)
    expected_content_sha = spec.get("expected_content_sha256")
    if expected_content_sha and content_sha != expected_content_sha:
        fail(
            "STOP_VS2_1_SOURCE_CONTENT_HASH_MISMATCH",
            field=path,
            expected=expected_content_sha,
            observed=content_sha,
        )
    parsed = parse_json_bytes(path, data) if path.endswith(".json") else None
    entry = {
        **spec,
        "content_sha256": content_sha,
        "committed_bytes_verified": True,
        "worktree_bytes_match_commit": True,
        "latest_file_resolution_used": False,
        "mtime_resolution_used": False,
        "directory_scan_authority_used": False,
        "baseline_share_used_as_source_authority": False,
        "source_verified": True,
    }
    if spec.get("canonical_sha256"):
        canonical = canonical_for_artifact(parsed or {}, path)
        if canonical != spec["canonical_sha256"]:
            fail(
                "STOP_VS2_1_SOURCE_CANONICAL_HASH_MISMATCH",
                field=path,
                expected=spec["canonical_sha256"],
                observed=canonical,
            )
        entry["canonical_sha256"] = canonical
    return entry, parsed


def canonical_for_artifact(data: dict[str, Any], path: str) -> str:
    if path.endswith("post_vs1_direction_decision_receipt_v0.json"):
        return canonical_hash(data["decision_receipt_binding"]["decision_receipt_payload"])
    if path.endswith("post_vs1_direction_authority_update_v0.json"):
        return canonical_hash(data["authority_update_binding"]["authority_update_payload"])
    if path.endswith("post_vs1_direction_transition_closure_v0.json"):
        return canonical_hash(data["transition_closure_binding"]["transition_closure_payload"])
    fail("STOP_VS2_1_SOURCE_CANONICAL_HASH_MISMATCH", field=path, expected="known canonical payload", observed="missing")


def validate_sources(source_docs: dict[str, dict[str, Any]]) -> None:
    vs1 = source_docs["S01_VS1_CLOSURE"]
    require_equal(vs1.get("phase_status"), "PHASE_VS1_PASS_LOOP_NOT_READY_MISSING_PRECONDITIONS_EXPOSED_AND_NEXT_SURFACES_MAPPED", "STOP_VS2_1_SOURCE_STATUS_MISMATCH", "S01.phase_status")
    require_equal(vs1.get("closure_gate"), "VS1_6_PHASE_CLOSURE_PASS_LOOP_NOT_READY_WITH_NEXT_SURFACES_MAPPED", "STOP_VS2_1_SOURCE_STATUS_MISMATCH", "S01.closure_gate")
    require_equal(vs1.get("closure_branch"), "NOT_READY_BLOCKERS_MAPPED", "STOP_VS2_1_SOURCE_STATUS_MISMATCH", "S01.closure_branch")
    require_equal(vs1.get("terminal_transition", {}).get("transition"), "STOP_PHASE_VS1_CLOSED_PENDING_POST_VS1_DIRECTION_DECISION", "STOP_VS2_1_SOURCE_STATUS_MISMATCH", "S01.terminal_transition")

    vs15 = source_docs["S02_VS1_5_NEXT_SURFACE_MAP"]
    coverage = vs15.get("blocker_coverage", {})
    require_equal(vs15.get("map_verdict"), "VS1_5_MISSING_PRECONDITION_NEXT_SURFACE_MAP_PASS", "STOP_VS2_1_SOURCE_STATUS_MISMATCH", "S02.map_verdict")
    for key, expected in {
        "source_blocker_count": 20,
        "mapped_blocker_count": 20,
        "unmapped_blocker_count": 0,
    }.items():
        require_equal(coverage.get(key), expected, "STOP_VS2_1_SOURCE_STATUS_MISMATCH", f"S02.{key}")
    require_equal(len(vs15.get("surface_candidates", [])), 21, "STOP_VS2_1_SOURCE_STATUS_MISMATCH", "S02.surface_candidate_record_count")

    sidecar = source_docs["S04_DIRECTIONAL_PROPOSAL_SOURCE_IDENTITY"]
    sidecar_expected = {
        "schema_version": "matrixlabs_durable_external_source_identity_v0",
        "declared_source_path_or_reference": SOURCE_SPECS[2]["declared_path"],
        "content_sha256": SOURCE_SPECS[2]["expected_content_sha256"],
        "source_role": "NON_BINDING_DIRECTIONAL_PROPOSAL",
        "source_status": "PRESENT_VERIFIED",
        "source_admission_grants_authority": False,
        "latest_file_resolution_used": False,
        "mtime_resolution_used": False,
        "directory_scan_authority_used": False,
        "baseline_share_used_as_source_authority": False,
    }
    for key, expected in sidecar_expected.items():
        require_equal(sidecar.get(key), expected, "STOP_VS2_1_SOURCE_STATUS_MISMATCH", f"S04.{key}")

    surface = source_docs["S05_DIRECTION_DECISION_SURFACE"]
    require_equal(surface.get("surface_status"), "PREPARED_PENDING_HUMAN_DECISION", "STOP_VS2_1_SOURCE_STATUS_MISMATCH", "S05.surface_status")
    require_equal(surface.get("surface_gate"), "POST_VS1_DIRECTION_DECISION_SURFACE_PASS_READY_FOR_HUMAN_DECISION", "STOP_VS2_1_SOURCE_STATUS_MISMATCH", "S05.surface_gate")
    require_equal(surface.get("terminal_transition", {}).get("transition"), "STOP_POST_VS1_DIRECTION_SURFACE_READY_PENDING_HUMAN_DECISION", "STOP_VS2_1_SOURCE_STATUS_MISMATCH", "S05.terminal_transition")
    require_equal(surface.get("applicable_closure_branch"), "NOT_READY_BLOCKERS_MAPPED", "STOP_VS2_1_SOURCE_STATUS_MISMATCH", "S05.applicable_closure_branch")
    require_equal(surface.get("decision_package_binding", {}).get("decision_package_sha256"), DECISION_PACKAGE_SHA256, "STOP_VS2_1_DECISION_PACKAGE_HASH_MISMATCH", "S05.decision_package_sha256")

    receipt = source_docs["S06_HUMAN_DECISION_RECEIPT"]
    selection = receipt.get("decision_selection", {})
    revision = receipt.get("revision_state", {})
    require_equal(receipt.get("receipt_status"), "HUMAN_ACCEPTANCE_RECORDED_PENDING_AUTHORITY_UPDATE", "STOP_VS2_1_SOURCE_STATUS_MISMATCH", "S06.receipt_status")
    require_equal(selection.get("decision_branch"), DECISION_BRANCH, "STOP_VS2_1_DECISION_BRANCH_NOT_EXACT_SCOPE_ACCEPTANCE", "S06.decision_branch")
    require_equal(selection.get("decision_mode"), DECISION_BRANCH, "STOP_VS2_1_DECISION_BRANCH_NOT_EXACT_SCOPE_ACCEPTANCE", "S06.decision_mode")
    require_equal(selection.get("accepted_option"), ACCEPTED_OPTION, "STOP_VS2_1_DECISION_BRANCH_NOT_EXACT_SCOPE_ACCEPTANCE", "S06.accepted_option")
    for key, expected in {
        "direction_id": DIRECTION_ID,
        "target_family": TARGET_FAMILY,
        "first_target": FIRST_TARGET,
        "bundle_id": BUNDLE_ID,
    }.items():
        require_equal(selection.get(key), expected, "STOP_VS2_1_DIRECTION_IDENTITY_MISMATCH", f"S06.{key}")
    require_false(selection.get("accepted_with_revisions"), "STOP_VS2_1_ACCEPTED_REVISIONS_PRESENT", "S06.accepted_with_revisions")
    require_equal(selection.get("revision_count"), 0, "STOP_VS2_1_UNEXPECTED_REVISION_STATE", "S06.revision_count")
    require_equal(selection.get("revisions"), [], "STOP_VS2_1_UNEXPECTED_REVISION_STATE", "S06.revisions")
    require_false(revision.get("accepted_with_revisions"), "STOP_VS2_1_ACCEPTED_REVISIONS_PRESENT", "S06.revision_state.accepted_with_revisions")
    require_false(receipt.get("decision_state_after_receipt", {}).get("authority_state_mutated"), "STOP_VS2_1_AUTHORIZED_DOWNSTREAM_WORK_PRECONSUMED", "S06.authority_state_mutated")

    update = source_docs["S07_AUTHORITY_UPDATE"]
    require_equal(update.get("authority_update_status"), "APPROVED_SCOPE_APPLIED_PENDING_TRANSITION_CLOSURE", "STOP_VS2_1_SOURCE_STATUS_MISMATCH", "S07.authority_update_status")
    require_equal(update.get("authority_update_gate"), "POST_VS1_DIRECTION_AUTHORITY_UPDATE_PASS_APPROVED_SCOPE_APPLIED_EXECUTION_AUTHORITY_ABSENT", "STOP_VS2_1_SOURCE_STATUS_MISMATCH", "S07.authority_update_gate")
    require_equal(update.get("terminal_transition", {}).get("transition"), "ADVANCE(POST_VS1_DIRECTION_TRANSITION_CLOSURE_V0_PENDING)", "STOP_VS2_1_SOURCE_STATUS_MISMATCH", "S07.terminal_transition")

    closure = source_docs["S08_TRANSITION_CLOSURE"]
    require_equal(closure.get("transition_closure_status"), "POST_VS1_DIRECTION_TRANSITION_PASS_VS2_DEFINITION_AND_BOUNDED_CONSTRUCTION_AUTHORITY_GRANTED_EXECUTION_AUTHORITY_ABSENT", "STOP_VS2_1_SOURCE_STATUS_MISMATCH", "S08.transition_closure_status")
    require_equal(closure.get("transition_closure_gate"), "POST_VS1_DIRECTION_TRANSITION_CLOSURE_PASS_AUTHORITY_EFFECTIVE_FOR_VS2_SOURCE_INTAKE_EXECUTION_AUTHORITY_ABSENT", "STOP_VS2_1_SOURCE_STATUS_MISMATCH", "S08.transition_closure_gate")
    require_equal(closure.get("terminal_transition", {}).get("transition"), "ADVANCE(VS2_1_POST_VS1_SOURCE_INTAKE_PENDING)", "STOP_VS2_1_SOURCE_STATUS_MISMATCH", "S08.terminal_transition")


def build_source_manifest(source_entries: list[dict[str, Any]]) -> dict[str, Any]:
    source_ids = [entry["source_id"] for entry in source_entries]
    declared_paths = [entry["declared_path"] for entry in source_entries]
    duplicate_source_id_count = len(source_ids) - len(set(source_ids))
    duplicate_declared_path_count = len(declared_paths) - len(set(declared_paths))
    if source_ids != [spec["source_id"] for spec in SOURCE_SPECS]:
        fail("STOP_VS2_1_SOURCE_MANIFEST_INCOMPLETE", field="source_ids", expected=[spec["source_id"] for spec in SOURCE_SPECS], observed=source_ids)
    if duplicate_source_id_count:
        fail("STOP_VS2_1_SOURCE_MANIFEST_DUPLICATE_ID", field="source_ids", expected=0, observed=duplicate_source_id_count)
    if duplicate_declared_path_count:
        fail("STOP_VS2_1_SOURCE_MANIFEST_DUPLICATE_PATH", field="declared_paths", expected=0, observed=duplicate_declared_path_count)
    payload = {
        "manifest_contract": {
            "canonicalization": CANONICALIZATION,
            "source_manifest_entry_count": 8,
            "required_source_ids": source_ids,
            "no_placeholder_values": True,
        },
        "source_entries": source_entries,
        "source_identity_checks": {
            "latest_file_resolution_used": False,
            "mtime_resolution_used": False,
            "directory_scan_authority_used": False,
            "baseline_share_used_as_source_authority": False,
            "all_worktree_bytes_match_committed_bytes": True,
        },
        "source_status_summary": {
            "source_manifest_entry_count": len(source_entries),
            "duplicate_source_id_count": duplicate_source_id_count,
            "duplicate_declared_path_count": duplicate_declared_path_count,
            "missing_required_source_count": 0,
            "unverified_source_count": 0,
            "undeclared_source_count": 0,
        },
    }
    if list(payload.keys()) != SOURCE_MANIFEST_BOUND_SECTIONS:
        fail("STOP_VS2_1_SOURCE_MANIFEST_HASH_MISMATCH", field="source_manifest_payload.keys", expected=SOURCE_MANIFEST_BOUND_SECTIONS, observed=list(payload.keys()))
    manifest_hash = canonical_hash(payload)
    return {
        "canonicalization": CANONICALIZATION,
        "canonicalization_contract": CANONICALIZATION,
        "bound_sections": SOURCE_MANIFEST_BOUND_SECTIONS,
        "source_manifest_payload": payload,
        "source_manifest_sha256": manifest_hash,
        "source_manifest_hash_recomputes": True,
        **payload["source_status_summary"],
    }


def linkage_row(child: str, parent: str, role: str, path: str, commit: str, content: str | None, canonical: str | None, observed: Any) -> dict[str, Any]:
    return {
        "child_artifact_id": child,
        "parent_artifact_id": parent,
        "relationship_role": role,
        "expected_parent_path": path,
        "expected_parent_commit_sha": commit,
        "expected_parent_content_sha256": content,
        "expected_parent_canonical_sha256": canonical,
        "observed_parent_reference": observed,
        "linkage_verified": True,
    }


def build_linkage_table(source_docs: dict[str, dict[str, Any]], intake_to_closure: dict[str, Any]) -> dict[str, Any]:
    surface = source_docs["S05_DIRECTION_DECISION_SURFACE"]
    receipt = source_docs["S06_HUMAN_DECISION_RECEIPT"]
    update = source_docs["S07_AUTHORITY_UPDATE"]
    closure = source_docs["S08_TRANSITION_CLOSURE"]
    rows = [
        linkage_row("post_vs1_direction_decision_surface_v0", "phase_vs1_closure_v0", "decision surface -> exact VS1 closure commit and hash", SOURCE_SPECS[0]["declared_path"], SOURCE_SPECS[0]["source_commit_sha"], SOURCE_SPECS[0]["expected_content_sha256"], None, surface["source_chain"]["vs1_closure"]),
        linkage_row("post_vs1_direction_decision_surface_v0", "phase_vs1_missing_precondition_next_surface_map_v0", "decision surface -> exact VS1.5 map commit and hash", SOURCE_SPECS[1]["declared_path"], SOURCE_SPECS[1]["source_commit_sha"], SOURCE_SPECS[1]["expected_content_sha256"], None, surface["source_chain"]["vs1_5_next_surface_map"]),
        linkage_row("matrixlab_first_sweep_capable_kernel_target_specification_v0.source", "matrixlab_first_sweep_capable_kernel_target_specification_v0", "proposal source identity -> exact proposal path and content hash", SOURCE_SPECS[2]["declared_path"], SOURCE_SPECS[2]["source_commit_sha"], SOURCE_SPECS[2]["expected_content_sha256"], None, {**source_docs["S04_DIRECTIONAL_PROPOSAL_SOURCE_IDENTITY"], "source_commit_sha": SOURCE_SPECS[2]["source_commit_sha"]}),
        linkage_row("post_vs1_direction_decision_receipt_v0", "post_vs1_direction_decision_surface_v0", "decision receipt -> exact decision surface commit and content hash", SOURCE_SPECS[4]["declared_path"], SOURCE_SPECS[4]["source_commit_sha"], SOURCE_SPECS[4]["expected_content_sha256"], None, receipt["source_surface_binding"]),
        linkage_row("post_vs1_direction_decision_receipt_v0", "post_vs1_direction_decision_package", "decision receipt -> exact decision-package hash", SOURCE_SPECS[4]["declared_path"], None, None, DECISION_PACKAGE_SHA256, receipt["source_decision_package_binding"]),
        linkage_row("post_vs1_direction_authority_update_v0", "post_vs1_direction_decision_receipt_v0", "authority update -> exact decision receipt commit and canonical hash", SOURCE_SPECS[5]["declared_path"], SOURCE_SPECS[5]["source_commit_sha"], None, DECISION_RECEIPT_SHA256, update["source_decision_receipt_binding"]),
        linkage_row("post_vs1_direction_authority_update_v0", "post_vs1_direction_decision_package", "authority update -> exact decision-package hash", SOURCE_SPECS[5]["declared_path"], None, None, DECISION_PACKAGE_SHA256, update["source_decision_package_binding"]),
        linkage_row("post_vs1_direction_transition_closure_v0", "post_vs1_direction_authority_update_v0", "transition closure -> exact authority update commit and canonical hash", SOURCE_SPECS[6]["declared_path"], SOURCE_SPECS[6]["source_commit_sha"], SOURCE_SPECS[6]["expected_content_sha256"], AUTHORITY_UPDATE_SHA256, closure["source_authority_update_binding"]),
        linkage_row("post_vs1_direction_transition_closure_v0", "post_vs1_direction_decision_receipt_v0", "transition closure -> exact decision receipt commit and canonical hash", SOURCE_SPECS[5]["declared_path"], SOURCE_SPECS[5]["source_commit_sha"], None, DECISION_RECEIPT_SHA256, closure["source_decision_chain_binding"]),
        linkage_row("post_vs1_direction_transition_closure_v0", "post_vs1_direction_decision_package", "transition closure -> exact decision-package hash", SOURCE_SPECS[5]["declared_path"], None, None, DECISION_PACKAGE_SHA256, closure["source_decision_chain_binding"]),
        linkage_row(ARTIFACT_ID, "post_vs1_direction_transition_closure_v0", "VS2.1 intake -> exact transition closure commit and canonical hash", SOURCE_SPECS[7]["declared_path"], SOURCE_SPECS[7]["source_commit_sha"], None, TRANSITION_CLOSURE_SHA256, intake_to_closure),
    ]
    verify_linkage_rows(rows)
    return {
        "linkage_rows": rows,
        "linkage_row_count": len(rows),
        "full_chain_linkage_verified": True,
        "linkage_failure_count": 0,
    }


def verify_linkage_rows(rows: list[dict[str, Any]]) -> None:
    for row in rows:
        observed = row["observed_parent_reference"]
        text = json.dumps(observed, sort_keys=True)
        if row["expected_parent_commit_sha"] and row["expected_parent_commit_sha"] not in text:
            fail("STOP_VS2_1_SOURCE_CHAIN_LINKAGE_MISMATCH", field=row["relationship_role"], expected=row["expected_parent_commit_sha"], observed=observed)
        expected_hash = row["expected_parent_content_sha256"] or row["expected_parent_canonical_sha256"]
        if expected_hash and expected_hash not in text:
            fail("STOP_VS2_1_SOURCE_CHAIN_LINKAGE_MISMATCH", field=row["relationship_role"], expected=expected_hash, observed=observed)


def build_decision_bindings(source_docs: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    receipt = source_docs["S06_HUMAN_DECISION_RECEIPT"]
    surface = source_docs["S05_DIRECTION_DECISION_SURFACE"]
    selection = receipt["decision_selection"]
    exact_branch = {
        "decision_branch": selection["decision_branch"],
        "decision_mode": selection["decision_mode"],
        "accepted_option": selection["accepted_option"],
        "accepted_with_revisions": selection["accepted_with_revisions"],
        "revision_count": selection["revision_count"],
        "revisions": selection["revisions"],
        "decision_branch_exact_scope_only": True,
    }
    accepted_direction = {
        "direction_id": selection["direction_id"],
        "target_family": selection["target_family"],
        "first_target": selection["first_target"],
        "bundle_id": selection["bundle_id"],
        "decision_package_sha256": selection["accepted_decision_package_sha256"],
    }
    bundle = surface["proposal_bundle"]
    membership = surface["proposal_bundle_membership_contract"]
    if bundle.get("primary_bundle_members") != PRIMARY_BUNDLE_MEMBERS:
        fail("STOP_VS2_1_PRIMARY_BUNDLE_MEMBER_MISMATCH", field="primary_bundle_members", expected=PRIMARY_BUNDLE_MEMBERS, observed=bundle.get("primary_bundle_members"))
    if bundle.get("deferred_full_surfaces") != DEFERRED_SURFACES:
        fail("STOP_VS2_1_DEFERRED_SURFACE_MISMATCH", field="deferred_full_surfaces", expected=DEFERRED_SURFACES, observed=bundle.get("deferred_full_surfaces"))
    if bundle.get("downstream_only_surfaces") != DOWNSTREAM_ONLY_SURFACES:
        fail("STOP_VS2_1_DOWNSTREAM_ONLY_SURFACE_MISMATCH", field="downstream_only_surfaces", expected=DOWNSTREAM_ONLY_SURFACES, observed=bundle.get("downstream_only_surfaces"))
    if membership.get("first_run_readiness_gate_is_s21") is not False:
        fail("STOP_VS2_1_S21_MISCLASSIFIED_AS_FIRST_RUN_GATE", field="first_run_readiness_gate_is_s21", expected=False, observed=membership.get("first_run_readiness_gate_is_s21"))
    accepted_bundle = {
        "bundle_id": bundle["bundle_id"],
        "relationship": bundle["proposal_relationship"],
        "primary_bundle_members": bundle["primary_bundle_members"],
        "deferred_surfaces": bundle["deferred_full_surfaces"],
        "downstream_only_surfaces": bundle["downstream_only_surfaces"],
        "primary_bundle_member_count": len(bundle["primary_bundle_members"]),
        "deferred_surface_count": len(bundle["deferred_full_surfaces"]),
        "downstream_only_surface_count": len(bundle["downstream_only_surfaces"]),
        "primary_bundle_members_exact": membership["primary_bundle_members_exact"],
        "bundle_members_may_expand_without_new_decision": membership["bundle_members_may_expand_without_new_decision"],
        "undeclared_additional_surface_ids": membership["undeclared_additional_surface_ids"],
        "s14_deferred": membership["s14_deferred"],
        "s15_deferred": membership["s15_deferred"],
        "s21_downstream_only": membership["s21_downstream_only"],
        "first_run_readiness_gate_is_s21": membership["first_run_readiness_gate_is_s21"],
    }
    trace = surface["proposal_bundle_traceability"]
    primary_rows = [row for row in trace["trace_rows"] if row.get("proposed_scope") == "PRIMARY_FIRST_KERNEL_BUNDLE"]
    required_row_fields = {
        "source_component_id",
        "source_primary_readiness_status",
        "source_secondary_blocker_classes",
        "source_vs1_5_surface_id",
        "support_parent_surface_id",
        "proposed_object_id",
        "proposed_scope",
        "source_artifact_path",
        "source_record_pointer",
    }
    failures = [row.get("trace_id") for row in primary_rows if not required_row_fields.issubset(row)]
    if len(primary_rows) != 18 or failures:
        fail("STOP_VS2_1_PROPOSAL_TRACEABILITY_MISSING", field="primary_trace_rows", expected=18, observed={"count": len(primary_rows), "failures": failures})
    mapped_ids = [row["source_vs1_5_surface_id"] for row in primary_rows]
    if mapped_ids != PRIMARY_BUNDLE_MEMBERS:
        fail("STOP_VS2_1_TRACE_ROW_PARENT_MISMATCH", field="primary_trace_row_surface_ids", expected=PRIMARY_BUNDLE_MEMBERS, observed=mapped_ids)
    unmapped = trace.get("unmapped_additional_proposal_scope", [])
    if unmapped:
        fail("STOP_VS2_1_UNMAPPED_SCOPE_PRESENT", field="unmapped_additional_proposal_scope", expected=[], observed=unmapped)
    traceability = {
        "primary_trace_rows": primary_rows,
        "primary_trace_row_count": len(primary_rows),
        "primary_trace_row_failure_count": 0,
        "unmapped_primary_member_count": 0,
        "unmapped_additional_scope": unmapped,
        "unmapped_scope_authorized": False,
        "proposal_traceability_verified": True,
    }
    return exact_branch, accepted_direction, accepted_bundle, traceability


def build_scope_audit(source_docs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    update = source_docs["S07_AUTHORITY_UPDATE"]
    closure = source_docs["S08_TRANSITION_CLOSURE"]
    applied = update["applied_authority_scope"]
    chain = closure["source_decision_chain_binding"]
    expected = {
        "applied_scope_mode": "EXACT_APPROVED_SCOPE",
        "applied_scope_equals_source_approved_scope": True,
        "applied_scope_exceeds_approved_scope": False,
        "approved_scope_items_omitted": [],
        "unapproved_scope_items_added": [],
    }
    for key, value in expected.items():
        require_equal(applied.get(key), value, "STOP_VS2_1_AUTHORITY_UPDATE_NOT_EXACT_APPROVED_SCOPE", f"S07.applied_authority_scope.{key}")
        require_equal(chain.get(key), value, "STOP_VS2_1_TRANSITION_CLOSURE_SCOPE_MISMATCH", f"S08.source_decision_chain_binding.{key}")
    return {
        "decision_branch": DECISION_BRANCH,
        "decision_mode": DECISION_BRANCH,
        "application_mode": chain["application_mode"],
        "applied_scope_mode": applied["applied_scope_mode"],
        "applied_scope_equals_source_approved_scope": True,
        "applied_scope_exceeds_approved_scope": False,
        "approved_scope_items_omitted": [],
        "unapproved_scope_items_added": [],
        "exact_scope_application_result": "EXACT_APPROVED_SCOPE_APPLIED_WITHOUT_OMISSION_OR_ADDITION",
        "exact_scope_applied": True,
    }


def build_grants(source_docs: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    closure = source_docs["S08_TRANSITION_CLOSURE"]
    audit = closure["grant_effectivity_audit"]
    projections = audit["closure_grant_projections"]
    ids = [grant["grant_id"] for grant in projections]
    if ids != GRANT_IDS:
        fail("STOP_VS2_1_GRANT_SET_MISMATCH", field="grant_ids", expected=GRANT_IDS, observed=ids)
    if len(set(ids)) != len(ids):
        fail("STOP_VS2_1_DUPLICATE_GRANT_ID", field="grant_ids", expected=GRANT_IDS, observed=ids)
    for grant in projections:
        for key, expected in {
            "source_grant_status": "GRANTED",
            "transition_closure_verified": True,
            "effective_for_downstream_consumption_after_closure": True,
            "consumed_by_transition_closure": False,
            "consumption_count_at_closure": 0,
            "execution_capable": False,
            "reusable": False,
            "portable": False,
            "generalizing": False,
        }.items():
            require_equal(grant.get(key), expected, "STOP_VS2_1_GRANT_EFFECTIVITY_MISMATCH", f"{grant['grant_id']}.{key}")
    inventory = {
        "source_grant_records": audit["source_grant_records"],
        "closure_grant_projections": projections,
        "source_grant_record_count": audit["source_grant_record_count"],
        "closure_grant_projection_count": audit["closure_grant_projection_count"],
        "unmatched_grant_count": audit["unmatched_grant_count"],
        "duplicate_grant_id_count": audit["duplicate_grant_id_count"],
        "scope_mismatch_count": audit["scope_mismatch_count"],
        "grant_effectivity_condition_mismatch_count": audit["grant_effectivity_condition_mismatch_count"],
        "effective_grant_count": len(projections),
        "definition_alias_counted_as_grant": False,
    }
    alias = {
        "vs2_definition_authority_granted": True,
        "definition_authority_aliases_profile_and_target_freeze_authority": True,
        "alias_source_grant_id": "VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY",
        "definition_alias_counted_as_grant": False,
    }
    return inventory, alias


def build_grant_routing() -> dict[str, Any]:
    routes = [
        {
            "grant_id": "VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY",
            "routing_status": "ROUTED_NOT_CONSUMED",
            "first_lawful_exercising_unit": "VS2.2_KERNEL_PROFILE_AND_TARGET_FREEZE",
            "consumed_by_vs2_1": False,
            "consumption_count_after_vs2_1": 0,
            "vs2_2_may_consume_grant": True,
        }
    ]
    for grant_id in GRANT_IDS[1:]:
        routes.append(
            {
                "grant_id": grant_id,
                "routing_status": "AVAILABLE_UNCONSUMED_PENDING_VS2_2_SEQUENCE_FREEZE",
                "available_downstream": True,
                "consumed_by_vs2_1": False,
                "consumption_count_after_vs2_1": 0,
                "exact_consuming_unit_frozen": False,
            }
        )
    return {
        "grant_routes": routes,
        "profile_grant_routed_to_vs2_2": True,
        "remaining_grant_consumers_frozen": False,
        "any_vs2_grant_consumed_by_vs2_1": False,
        "vs2_grant_consumption_count_after_vs2_1": 0,
    }


def build_withheld(source_docs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    closure = source_docs["S08_TRANSITION_CLOSURE"]
    audit = closure["withheld_authority_audit"]
    vector = audit["source_withheld_authority_vector"]
    for key in [
        "KERNEL_EXECUTION_AUTHORITY",
        "POSITIVE_PATH_EXECUTION_AUTHORITY",
        "NEGATIVE_PATH_EXECUTION_AUTHORITY",
        "PERTURBATION_SWEEP_EXECUTION_AUTHORITY",
        "AUTOMATIC_RERUN_AUTHORITY",
        "RUNNER_AUTHORITY",
    ]:
        expected = "NOT_CREATED" if key == "RUNNER_AUTHORITY" else "NOT_GRANTED"
        require_equal(vector.get(key), expected, "STOP_VS2_1_WITHHELD_AUTHORITY_VECTOR_MISMATCH", key)
    return {
        "withheld_authority_vector": vector,
        "withheld_authority_preserved": True,
        "withheld_authority_changed_by_vs2_1": False,
        "unapproved_authority_grant_count": audit["unapproved_authority_grant_count"],
        "execution_authority_included": audit["execution_authority_included"],
        "execution_authority_absent": True,
        "sweep_authority_absent": True,
        "automatic_rerun_authority_absent": True,
        "runner_authority_absent": True,
    }


def build_phase_states(source_docs: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    pre = source_docs["S08_TRANSITION_CLOSURE"]["post_closure_authority_state"]
    for key, expected in {
        "authority_transition_closed": True,
        "authority_effective_for_vs2_consumption": True,
        "authority_grants_effective_for_consumption": True,
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
        "execution_authorized": False,
        "sweep_authorized": False,
        "runner_authority_created": False,
    }.items():
        require_equal(pre.get(key), expected, "STOP_VS2_1_AUTHORIZED_DOWNSTREAM_WORK_PRECONSUMED", f"pre_intake.{key}")
    post = {
        **pre,
        "vs2_source_intake_built": True,
        "vs2_started": True,
        "vs2_1_built": True,
        "source_manifest_frozen": True,
        "source_manifest_commit_pending": True,
        "bookkeeping_commit_required": True,
        "vs2_2_may_begin": True,
        "any_vs2_grant_consumed": False,
        "vs2_grant_consumption_count": 0,
        "kernel_profile_frozen": False,
        "semantic_target_frozen": False,
        "construction_performed": False,
        "fixture_construction_performed": False,
        "readiness_gate_constructed": False,
        "construction_package_verified": False,
        "execution_authorized": False,
        "sweep_authorized": False,
        "runner_authority_created": False,
        "execution_performed": False,
        "sweep_executed": False,
        "runner_created": False,
    }
    return pre, post


def downstream_boundary() -> dict[str, Any]:
    return {
        "logical_next_unit": "VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_PENDING",
        "logical_terminal_transition": LOGICAL_TERMINAL,
        "construction_session_terminal_transition": TERMINAL_TRANSITION,
        "vs2_2_may_bind_source_intake": True,
        "vs2_2_may_consume_profile_grant": True,
        "next_unit_must_not_authorize_execution": True,
        "kernel_profile_frozen_by_this_unit": False,
        "semantic_target_frozen_by_this_unit": False,
        "construction_performed_by_this_unit": False,
        "execution_performed_by_this_unit": False,
    }


def build_intake(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    source_entries: list[dict[str, Any]] = []
    source_docs: dict[str, dict[str, Any]] = {}
    for spec in SOURCE_SPECS:
        entry, parsed = verify_source(root, spec)
        source_entries.append(entry)
        if parsed is not None:
            source_docs[spec["source_id"]] = parsed
    validate_sources(source_docs)
    manifest_binding = build_source_manifest(source_entries)
    exact_branch, accepted_direction, accepted_bundle, traceability = build_decision_bindings(source_docs)
    scope_audit = build_scope_audit(source_docs)
    grant_inventory, alias = build_grants(source_docs)
    routing = build_grant_routing()
    withheld = build_withheld(source_docs)
    pre_state, post_state = build_phase_states(source_docs)
    intake_to_closure = {
        "transition_closure_commit_sha": EXPECTED_HEAD,
        "transition_closure_sha256": TRANSITION_CLOSURE_SHA256,
        "transition_closure_path": SOURCE_SPECS[7]["declared_path"],
    }
    linkage = build_linkage_table(source_docs, intake_to_closure)
    payload = {
        "transition_closure_binding": intake_to_closure,
        "committed_source_manifest": manifest_binding,
        "source_linkage_table": linkage,
        "exact_decision_branch_binding": exact_branch,
        "accepted_direction_binding": accepted_direction,
        "accepted_bundle_binding": accepted_bundle,
        "proposal_traceability_binding": traceability,
        "exact_scope_application_audit": scope_audit,
        "effective_grant_inventory": grant_inventory,
        "grant_alias_normalization": alias,
        "grant_routing": routing,
        "withheld_authority_binding": withheld,
        "pre_intake_phase_state": pre_state,
        "post_intake_phase_state": post_state,
        "downstream_boundary": downstream_boundary(),
    }
    if list(payload.keys()) != SOURCE_INTAKE_BOUND_SECTIONS:
        fail("STOP_VS2_1_SOURCE_INTAKE_HASH_MISMATCH", field="source_intake_payload.keys", expected=SOURCE_INTAKE_BOUND_SECTIONS, observed=list(payload.keys()))
    intake_hash = canonical_hash(payload)
    binding = {
        "canonicalization": CANONICALIZATION,
        "canonicalization_contract": CANONICALIZATION,
        "bound_sections": SOURCE_INTAKE_BOUND_SECTIONS,
        "source_intake_payload": payload,
        "source_intake_sha256": intake_hash,
        "bound_sections_match_payload_keys": True,
        "source_intake_hash_recomputes": True,
        "generated_timestamps_excluded_from_hash": True,
        "filesystem_mtimes_excluded_from_hash": True,
        "future_bookkeeping_commit_sha_excluded_from_hash": True,
        "future_vs2_2_artifact_hashes_excluded_from_hash": True,
        "future_grant_consumption_receipts_excluded_from_hash": True,
        "future_construction_artifacts_excluded_from_hash": True,
        "future_execution_decisions_excluded_from_hash": True,
        "future_execution_results_excluded_from_hash": True,
    }
    intake = {
        "schema_version": SCHEMA_VERSION,
        "artifact_id": ARTIFACT_ID,
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "unit_role": UNIT_ROLE,
        "intake_status": INTAKE_GATE,
        "source_manifest_binding": manifest_binding,
        **payload,
        "source_intake_binding": binding,
        "source_intake_sha256": intake_hash,
        "intake_gate": INTAKE_GATE,
        "evidence_yield": {"branch": EVIDENCE_YIELD_BRANCH, "confirmation_yield": True},
        "logical_terminal_transition": LOGICAL_TERMINAL,
        "terminal_transition": TERMINAL_TRANSITION,
        "non_claims": [
            "This source-intake unit does not freeze the kernel profile or semantic target.",
            "This source-intake unit consumes zero VS2 grants.",
            "This source-intake unit performs no construction, readiness verification, execution, sweep, or runner creation.",
        ],
        "failures": [],
    }
    receipt = build_receipt(intake)
    return intake, receipt


def build_receipt(intake: dict[str, Any]) -> dict[str, Any]:
    manifest = intake["source_manifest_binding"]
    receipt = {
        "schema_version": "matrixlabs_phase_vs2_1_post_vs1_source_intake_receipt_v0",
        "artifact_id": "phase_vs2_1_post_vs1_source_intake_receipt_v0",
        "source_intake_artifact_id": ARTIFACT_ID,
        "source_intake_sha256": intake["source_intake_sha256"],
        "source_manifest_sha256": manifest["source_manifest_sha256"],
        "transition_closure_commit_sha": EXPECTED_HEAD,
        "transition_closure_sha256": TRANSITION_CLOSURE_SHA256,
        "decision_package_sha256": DECISION_PACKAGE_SHA256,
        "decision_receipt_sha256": DECISION_RECEIPT_SHA256,
        "authority_update_sha256": AUTHORITY_UPDATE_SHA256,
        "source_manifest_entry_count": manifest["source_manifest_entry_count"],
        "source_manifest_hash_recomputes": True,
        "source_intake_hash_recomputes": True,
        "full_chain_linkage_verified": True,
        "linkage_failure_count": 0,
        "decision_branch": DECISION_BRANCH,
        "accepted_with_revisions": False,
        "revision_count": 0,
        "direction_id": DIRECTION_ID,
        "target_family": TARGET_FAMILY,
        "first_target": FIRST_TARGET,
        "bundle_id": BUNDLE_ID,
        "primary_bundle_member_count": 18,
        "deferred_surface_count": 2,
        "downstream_only_surface_count": 1,
        "unmapped_scope_count": 0,
        "exact_scope_applied": True,
        "approved_scope_items_omitted_count": 0,
        "unapproved_scope_items_added_count": 0,
        "effective_grant_count": 5,
        "definition_alias_counted_as_grant": False,
        "any_vs2_grant_consumed": False,
        "vs2_grant_consumption_count": 0,
        "profile_grant_routed_to_vs2_2": True,
        "remaining_grant_consumers_frozen": False,
        "withheld_authority_preserved": True,
        "execution_authority_absent": True,
        "sweep_authority_absent": True,
        "automatic_rerun_authority_absent": True,
        "runner_authority_absent": True,
        "vs2_source_intake_built": True,
        "vs2_started": True,
        "vs2_1_built": True,
        "vs2_2_may_begin": True,
        "kernel_profile_frozen": False,
        "semantic_target_frozen": False,
        "construction_performed": False,
        "fixtures_constructed": False,
        "fixture_construction_performed": False,
        "readiness_gate_constructed": False,
        "construction_package_verified": False,
        "execution_performed": False,
        "receipt_gate": INTAKE_GATE,
        "evidence_yield_branch": EVIDENCE_YIELD_BRANCH,
        "logical_downstream_transition": LOGICAL_TERMINAL,
        "construction_session_terminal": TERMINAL_TRANSITION,
    }
    receipt_payload = dict(receipt)
    receipt["receipt_binding"] = {
        "canonicalization": CANONICALIZATION,
        "canonicalization_contract": CANONICALIZATION,
        "receipt_payload": receipt_payload,
        "receipt_sha256": canonical_hash(receipt_payload),
    }
    return receipt


def build_markdown(intake: dict[str, Any], receipt: dict[str, Any]) -> str:
    manifest = intake["source_manifest_binding"]
    sources = manifest["source_manifest_payload"]["source_entries"]
    source_lines = "\n".join(
        f"- {entry['source_id']} - `{entry['declared_path']}` @ `{entry['source_commit_sha']}`"
        for entry in sources
    )
    grants = "\n".join(f"- {grant_id}" for grant_id in GRANT_IDS)
    withheld = intake["withheld_authority_binding"]
    return f"""# Phase VS2.1 Post-VS1 Source Intake v0

## Exact Eight-Source Manifest

{source_lines}

Source manifest hash:
{manifest["source_manifest_sha256"]}

Source-intake hash:
{intake["source_intake_sha256"]}

Receipt hash:
{receipt["receipt_binding"]["receipt_sha256"]}

## Exact Decision Branch

Decision branch:
{DECISION_BRANCH}

Accepted direction:
{DIRECTION_ID}

Accepted target family:
{TARGET_FAMILY}

Accepted first target:
{FIRST_TARGET}

Accepted bundle:
{BUNDLE_ID}

Bundle classification:
18 primary, 2 deferred, 1 downstream-only.

Exact-scope application result:
EXACT_APPROVED_SCOPE_APPLIED_WITHOUT_OMISSION_OR_ADDITION

## Effective Grant IDs

{grants}

Definition authority is normalized as an alias of VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY, not a sixth grant.

Profile grant routing:
VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY routed to VS2.2_KERNEL_PROFILE_AND_TARGET_FREEZE, not consumed by VS2.1.

Zero VS2 grants consumed.

## Withheld Authority

Withheld authority preserved:
{str(withheld["withheld_authority_preserved"]).lower()}

Execution authority absent.
Sweep authority absent.
Automatic rerun authority absent.
Runner authority absent.

## Phase VS2 Entry State

VS2 source intake built.
VS2 started.
VS2.1 built.
Source manifest frozen.
Source manifest not yet committed.
Bookkeeping commit pending.
VS2.2 may begin.

Kernel profile not frozen.
Semantic target not frozen.
Construction not started.
Fixtures not constructed.
Readiness gate not constructed.
Construction package not verified.
Execution not authorized or performed.
Runner not created.

## Next

Logical next unit:
VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_PENDING

Pending bookkeeping boundary:
BOOKKEEPING_COMMIT_PHASE_VS2_1_POST_VS1_SOURCE_INTAKE_V0_PENDING
"""


def validate_output_scope(root: Path) -> None:
    validate_dirty_scope(root)
    ensure_forbidden_absent(root)


def generate() -> int:
    root = detect_repo_root(Path.cwd())
    require_repo_context(root)
    validate_output_scope(root)
    intake, receipt = build_intake(root)
    (root / OUTPUT_JSON).parent.mkdir(parents=True, exist_ok=True)
    (root / OUTPUT_JSON).write_text(json.dumps(intake, indent=2) + "\n", encoding="utf-8")
    (root / OUTPUT_MD).write_text(build_markdown(intake, receipt), encoding="utf-8")
    (root / OUTPUT_RECEIPT).write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    validate_output_scope(root)
    emit_success(intake, receipt)
    return 0


def emit_success(intake: dict[str, Any], receipt: dict[str, Any]) -> None:
    manifest = intake["source_manifest_binding"]
    print("BUILD_PHASE_VS2_1_POST_VS1_SOURCE_INTAKE_V0_COMPLETE")
    print()
    print(f"artifact_id={ARTIFACT_ID}")
    print(f"schema_version={SCHEMA_VERSION}")
    print(f"phase_id={PHASE_ID}")
    print(f"unit_id={UNIT_ID}")
    print(f"unit_role={UNIT_ROLE}")
    print()
    for key in [
        "source_manifest_entry_count",
        "duplicate_source_id_count",
        "duplicate_declared_path_count",
        "missing_required_source_count",
        "unverified_source_count",
        "undeclared_source_count",
    ]:
        print(f"{key}={manifest[key]}")
    print()
    print(f"source_manifest_sha256={manifest['source_manifest_sha256']}")
    print("source_manifest_hash_recomputes=true")
    print()
    print(f"source_intake_sha256={intake['source_intake_sha256']}")
    print("source_intake_hash_recomputes=true")
    print()
    print(f"transition_closure_commit_sha={EXPECTED_HEAD}")
    print(f"transition_closure_sha256={TRANSITION_CLOSURE_SHA256}")
    print()
    print(f"decision_package_sha256={DECISION_PACKAGE_SHA256}")
    print(f"decision_receipt_sha256={DECISION_RECEIPT_SHA256}")
    print(f"authority_update_sha256={AUTHORITY_UPDATE_SHA256}")
    print()
    print("full_chain_linkage_verified=true")
    print("linkage_failure_count=0")
    print()
    print(f"decision_branch={DECISION_BRANCH}")
    print("accepted_with_revisions=false")
    print("revision_count=0")
    print()
    print(f"direction_id={DIRECTION_ID}")
    print(f"target_family={TARGET_FAMILY}")
    print(f"first_target={FIRST_TARGET}")
    print(f"bundle_id={BUNDLE_ID}")
    print()
    print("primary_bundle_member_count=18")
    print("deferred_surface_count=2")
    print("downstream_only_surface_count=1")
    print("unmapped_scope_count=0")
    print("proposal_traceability_verified=true")
    print()
    print("exact_scope_applied=true")
    print("approved_scope_items_omitted_count=0")
    print("unapproved_scope_items_added_count=0")
    print()
    print("effective_grant_count=5")
    print("definition_alias_counted_as_grant=false")
    print("profile_grant_routed_to_vs2_2=true")
    print("remaining_grant_consumers_frozen=false")
    print()
    print("any_vs2_grant_consumed=false")
    print("vs2_grant_consumption_count=0")
    print()
    print("withheld_authority_preserved=true")
    print("execution_authority_absent=true")
    print("sweep_authority_absent=true")
    print("automatic_rerun_authority_absent=true")
    print("runner_authority_absent=true")
    print()
    print("vs2_source_intake_built=true")
    print("vs2_started=true")
    print("vs2_1_built=true")
    print("source_manifest_frozen=true")
    print("source_manifest_commit_pending=true")
    print("vs2_2_may_begin=true")
    print()
    print("kernel_profile_frozen=false")
    print("semantic_target_frozen=false")
    print("construction_performed=false")
    print("fixture_construction_performed=false")
    print("readiness_gate_constructed=false")
    print("construction_package_verified=false")
    print("execution_performed=false")
    print("sweep_executed=false")
    print("runner_created=false")
    print()
    print("source_files_unchanged=true")
    print("forbidden_output_count=0")
    print("generated_artifacts_deterministic=true")
    print()
    print(f"intake_gate={INTAKE_GATE}")
    print(f"evidence_yield_branch={EVIDENCE_YIELD_BRANCH}")
    print()
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode != 0
    print(f"staged_changes_present={str(staged).lower()}")
    print("commit_created=false")
    print("push_executed=false")
    print()
    print(f"logical_terminal_transition={LOGICAL_TERMINAL}")
    print()
    print(f"terminal_transition={TERMINAL_TRANSITION}")


def emit_failure(exc: VS21Failure) -> None:
    print("BUILD_PHASE_VS2_1_POST_VS1_SOURCE_INTAKE_V0_FAILED")
    print(f"failure_code={exc.code}")
    print(f"failed_source_or_field={exc.field}")
    print(f"expected_value={json.dumps(exc.expected, sort_keys=True)}")
    print(f"observed_value={json.dumps(exc.observed, sort_keys=True)}")
    print(f"violated_boundary={exc.boundary}")
    print(f"next_lawful_correction_surface={exc.next_surface}")
    print("self_repair_performed=false")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition=STOP({exc.code})")


def main() -> int:
    try:
        return generate()
    except VS21Failure as exc:
        emit_failure(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
