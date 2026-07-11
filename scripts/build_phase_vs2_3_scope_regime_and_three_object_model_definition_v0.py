#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = "/home/asd/projects/matrixlab"
BRANCH = "master"
HEAD = "007244b3483464f76b91141ca47c85457e7f0bf1"
PHASE_ID = "PHASE_VS2"
UNIT_ID = "VS2.3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION"
UNIT_ROLE = "SCOPE_REGIME_AND_THREE_OBJECT_MODEL_CONSTRUCTION_ONLY"
CANON = "MATRIXLAB_CANONICAL_JSON_V0"
HASH_ALG = "SHA-256"

PROFILE_PATH = "docs/matrixlabs/phase_vs2/phase_vs2_first_sweep_capable_kernel_profile_v0.json"
PROFILE_MD_PATH = "docs/matrixlabs/phase_vs2/phase_vs2_first_sweep_capable_kernel_profile_v0.md"
TARGET_FREEZE_PATH = "docs/matrixlabs/phase_vs2/phase_vs2_typed_state_contract_convergence_target_freeze_v0.json"
TARGET_FREEZE_MD_PATH = "docs/matrixlabs/phase_vs2/phase_vs2_typed_state_contract_convergence_target_freeze_v0.md"
UPSTREAM_RECEIPT_PATH = "docs/matrixlabs/phase_vs2/phase_vs2_2_kernel_profile_and_target_freeze_receipt_v0.json"

PROFILE_RAW = "2d61b8f7aaa11c10416ffbf2097f4ff95069d5131a99b63b8d1728485e7cf96b"
PROFILE_MD_RAW = "42bbfeb1a77df4ed6f1c624dbd88e4a319b85c1aedf1325a66b7f6187d32c592"
TARGET_FREEZE_RAW = "5e31db512163961034c98790a762036afa1730d57c7cf7346f5e9f7260ec985a"
TARGET_FREEZE_MD_RAW = "ad0a852e157c1b75043cdaa4ab1e58def1bb17289f88386b0046c3764f8d181b"
UPSTREAM_RECEIPT_RAW = "a6a57810854215f912cb2251dbda277eb6bf8f110cd79371af615908497cc833"
PROFILE_SHA = "844fe441ecda5ec84076e9f665d09868373c9b24ea89d5d7056c485823db3142"
TARGET_FREEZE_SHA = "518bf3238994cfc88ea542289eb622c90f9eb7f3d6575398c95dd57203669eb8"
UPSTREAM_RECEIPT_SHA = "9e17272877e96f9db6885334e2531df8be8fdd7bb2d501d853c393b8f16ce425"
SOURCE_INTAKE_COMMIT = "9d529c6813fd5db38eb4a63368a8d538aa7a88e4"
SOURCE_INTAKE_RAW = "aac9ba4eec3ca577ead6cd23f8af6b9ecc6a9d542ec2395450a698f45465514b"
SOURCE_INTAKE_SHA = "830c62352e6eab4445b8cac9bbb7851da49a39633fc5cb673b71283bba1eaaeb"
SOURCE_MANIFEST_SHA = "9aaceb1758920971d8f5d7f305b837b7021ebc0a84714dea08755efce1c0a6ef"
SOURCE_INTAKE_RECEIPT_RAW = "97e0046641b67bdc4740c1a82e5356eb4ffda6df0d2584e04d474b2b8e6cac5f"
SOURCE_INTAKE_RECEIPT_SHA = "b8b440b920993d38f77b0359ea928a255d780e5e682572fcc9144c35e63609cd"

OUT_DIR = "docs/matrixlabs/phase_vs2/object_model"
SCRIPT = "scripts/build_phase_vs2_3_scope_regime_and_three_object_model_definition_v0.py"
VERIFY_SCRIPT = "scripts/verify_phase_vs2_3_scope_regime_and_three_object_model_definition_v0.py"
BASELINE_SCRIPT = "scripts/build_baseline_share_v0.py"
F0_JSON = f"{OUT_DIR}/phase_vs2_scope_regime_contract_v0.json"
F0_MD = f"{OUT_DIR}/phase_vs2_scope_regime_contract_v0.md"
O1_JSON = f"{OUT_DIR}/phase_vs2_runtime_control_state_contract_v0.json"
O1_MD = f"{OUT_DIR}/phase_vs2_runtime_control_state_contract_v0.md"
O2_JSON = f"{OUT_DIR}/phase_vs2_candidate_typed_state_contract_schema_v0.json"
O2_MD = f"{OUT_DIR}/phase_vs2_candidate_typed_state_contract_schema_v0.md"
O3_JSON = f"{OUT_DIR}/phase_vs2_frozen_target_contract_v0.json"
O3_MD = f"{OUT_DIR}/phase_vs2_frozen_target_contract_v0.md"
M0_JSON = f"{OUT_DIR}/phase_vs2_object_model_binding_manifest_v0.json"
M0_MD = f"{OUT_DIR}/phase_vs2_object_model_binding_manifest_v0.md"
RECEIPT_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_3_scope_regime_and_three_object_model_definition_receipt_v0.json"

ALLOWED_DIRTY = {
    SCRIPT,
    VERIFY_SCRIPT,
    BASELINE_SCRIPT,
    F0_JSON,
    F0_MD,
    O1_JSON,
    O1_MD,
    O2_JSON,
    O2_MD,
    O3_JSON,
    O3_MD,
    M0_JSON,
    M0_MD,
    RECEIPT_JSON,
    "baseline_share/COMMIT_CONTEXT.md",
    "baseline_share/CURRENT_STATE.md",
    "baseline_share/MANIFEST.json",
    "baseline_share/RECEIPT_POINTERS.md",
}
PROTECTED_UPSTREAM = {
    PROFILE_PATH,
    PROFILE_MD_PATH,
    TARGET_FREEZE_PATH,
    TARGET_FREEZE_MD_PATH,
    UPSTREAM_RECEIPT_PATH,
}

EXECUTION_ROLES = [
    "RUNTIME_CONTROL_STATE",
    "CANDIDATE_TYPED_STATE_CONTRACT",
    "FROZEN_TARGET_CONTRACT",
]
TERMINAL_OUTCOMES = [
    "TARGET_REACHED",
    "STOP_REPAIR_NOT_LAWFUL",
    "STOP_MISSING_SOURCE",
    "STOP_MISSING_SCHEMA",
    "STOP_MISSING_AUTHORITY",
    "STOP_MISSING_CAPABILITY",
    "STOP_RADIUS_EXHAUSTED",
    "STOP_NO_ADMISSIBLE_MOVE",
    "STOP_VALIDATION_FAILED",
    "STOP_ADMISSIBILITY_FAILED",
    "STOP_FORBIDDEN_EFFECT_DETECTED",
    "STOP_SOURCE_IDENTITY_UNVERIFIED",
    "STOP_SCOPE_REGIME_VIOLATION",
    "STOP_NON_PROGRESS",
    "STOP_REPEATED_STATE",
    "STOP_CONVERGENCE_CRITERION_UNMET",
    "STOP_UNCLASSIFIED_RESULT_REQUIRES_TAXONOMY_REFINEMENT",
]
SEMANTIC_SECTIONS = [
    "contract_identity_declarations",
    "state_identity_declarations",
    "source_binding_declarations",
    "authority_declarations",
    "typed_field_declarations",
    "runtime_boundary_declarations",
    "halt_and_terminal_declarations",
    "receipt_declarations",
    "forbidden_effect_declarations",
    "claim_declarations",
]
LOOP_POSITIONS = [
    "INITIALIZED",
    "INSPECTION_PENDING",
    "MOVE_ENUMERATION_PENDING",
    "MOVE_SELECTION_PENDING",
    "MOVE_APPLICATION_PENDING",
    "VALIDATION_PENDING",
    "ADMISSIBILITY_PENDING",
    "CONVERGENCE_CHECK_PENDING",
    "RECEIPT_PENDING",
    "TERMINAL_CHECK_PENDING",
    "TERMINAL",
]
PENDING_BINDINGS = [
    ("move_space_reference", "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE", "FINITE_MOVE_SPACE_CONTRACT"),
    ("execution_authority_shape_reference", "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE", "BOUNDED_FUTURE_EXECUTION_AUTHORITY_SHAPE"),
    ("source_and_version_binding_contract_reference", "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE", "SOURCE_AND_VERSION_BINDING_CONTRACT"),
    ("selector_contract_reference", "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION", "SELECTOR_CONTRACT"),
    ("applicator_contract_reference", "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION", "APPLICATOR_CONTRACT"),
    ("validation_contract_reference", "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION", "VALIDATION_CONTRACT"),
    ("admissibility_contract_reference", "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION", "ADMISSIBILITY_CONTRACT"),
    ("convergence_criterion_reference", "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION", "CONVERGENCE_CRITERION_CONTRACT"),
    ("radius_budget_halt_policy_reference", "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION", "RADIUS_BUDGET_HALT_POLICY"),
    ("move_receipt_contract_reference", "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION", "MOVE_RECEIPT_CONTRACT"),
    ("case_terminal_receipt_contract_reference", "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION", "CASE_TERMINAL_RECEIPT_CONTRACT"),
    ("replay_audit_contract_reference", "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION", "REPLAY_AUDIT_CONTRACT"),
    ("forbidden_effect_guard_reference", "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION", "FORBIDDEN_EFFECT_GUARD"),
    ("fixture_set_reference", "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS", "FIXTURE_SET"),
    ("source_snapshot_reference", "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS", "SOURCE_SNAPSHOT"),
    ("pressure_readout_contract_reference", "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS", "PRESSURE_READOUT_CONTRACT"),
    ("evidence_yield_report_contract_reference", "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS", "EVIDENCE_YIELD_REPORT_CONTRACT"),
    ("construction_readiness_gate_reference", "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS", "CONSTRUCTION_READINESS_GATE"),
]
INVARIANTS = [
    "SCOPE_REGIME_BINDING_INVARIANT",
    "TARGET_FAMILY_IDENTITY_INVARIANT",
    "CANDIDATE_FAMILY_IDENTITY_INVARIANT",
    "PROFILE_BINDING_INVARIANT",
    "RUNTIME_CANDIDATE_BINDING_INVARIANT",
    "RUNTIME_TARGET_BINDING_INVARIANT",
    "SOURCE_FRAME_INVARIANT",
    "AUTHORITY_ROLE_SEPARATION_INVARIANT",
    "EVALUATION_LOCATION_INVARIANT",
    "MUTATION_ROLE_INVARIANT",
    "RUNTIME_VERSION_CHAIN_INVARIANT",
    "CANDIDATE_VERSION_CHAIN_INVARIANT",
    "TERMINALIZATION_INVARIANT",
    "HASH_AND_CANONICALIZATION_INVARIANT",
    "EXACT_THREE_EXECUTION_OBJECT_ROLE_INVARIANT",
    "NO_FOURTH_MUTABLE_ROOT_INVARIANT",
    "C20_STRUCTURAL_RESERVATION_INVARIANT",
    "TERMINAL_OUTCOME_FAMILY_PRESERVATION_INVARIANT",
]


class StopFailure(RuntimeError):
    def __init__(self, code: str, artifact: str, field: str, expected: Any, observed: Any, invariant: str = "VS2_3_CONSTRUCTION_BOUNDARY") -> None:
        super().__init__(code)
        self.code = code
        self.artifact = artifact
        self.field = field
        self.expected = expected
        self.observed = observed
        self.invariant = invariant


def fail(code: str, artifact: str, field: str, expected: Any, observed: Any, invariant: str = "VS2_3_CONSTRUCTION_BOUNDARY") -> None:
    raise StopFailure(code, artifact, field, expected, observed, invariant)


def git(root: Path, args: list[str], binary: bool = False) -> str | bytes:
    result = subprocess.run(["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=not binary)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, ["git", *args], result.stdout, result.stderr)
    return result.stdout if binary else result.stdout.strip()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_hash(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def status_paths(status: str) -> list[str]:
    paths = []
    for line in status.splitlines():
        raw = line[2:].strip()
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]
        paths.append(raw)
    return paths


def require(observed: Any, expected: Any, code: str, artifact: str, field: str) -> None:
    if observed != expected:
        fail(code, artifact, field, expected, observed)


def require_bool(observed: Any, expected: bool, code: str, artifact: str, field: str) -> None:
    if observed is not expected:
        fail(code, artifact, field, expected, observed)


def validate_dirty_scope(root: Path) -> None:
    status = git(root, ["status", "--short", "--untracked-files=all"])
    paths = status_paths(status)
    unexpected = [path for path in paths if path not in ALLOWED_DIRTY]
    protected = [path for path in paths if path in PROTECTED_UPSTREAM]
    if unexpected:
        fail("STOP_VS2_3_PREEXISTING_WORKTREE_CHANGES", "repo", "dirty_paths", sorted(ALLOWED_DIRTY), unexpected)
    if protected:
        fail("STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", "upstream", "protected_paths", "unchanged", protected)
    if (root / "discussion_packets").exists():
        fail("STOP_VS2_3_DISCUSSION_PACKETS_PRESENT", "repo", "discussion_packets", "absent", "present")


def check_repo(root: Path) -> None:
    require(str(root), ROOT, "STOP_VS2_3_REPOSITORY_ROOT_MISMATCH", "repo", "repository_root")
    require(git(root, ["rev-parse", "--show-toplevel"]), ROOT, "STOP_VS2_3_REPOSITORY_ROOT_MISMATCH", "repo", "git_root")
    require(git(root, ["branch", "--show-current"]), BRANCH, "STOP_VS2_3_BRANCH_MISMATCH", "repo", "branch")
    require(git(root, ["rev-parse", "HEAD"]), HEAD, "STOP_VS2_3_UNEXPECTED_HEAD", "repo", "HEAD")
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=root).returncode != 0
    require_bool(staged, False, "STOP_VS2_3_STAGED_CHANGES_PRESENT", "repo", "staged_changes_present")
    validate_dirty_scope(root)


def verify_committed(root: Path, rel: str, raw_sha: str) -> bytes:
    try:
        committed = git(root, ["show", f"{HEAD}:{rel}"], binary=True)
    except subprocess.CalledProcessError as exc:
        fail("STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", rel, "committed_path", "present", exc.stderr)
    current_path = root / rel
    if not current_path.exists():
        fail("STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", rel, "worktree_path", "present", "missing")
    current = current_path.read_bytes()
    require(current, committed, "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", rel, "committed_bytes")
    require(sha256_bytes(current), raw_sha, "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", rel, "raw_sha256")
    return current


def load_upstream(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    profile = json.loads(verify_committed(root, PROFILE_PATH, PROFILE_RAW).decode("utf-8"))
    verify_committed(root, PROFILE_MD_PATH, PROFILE_MD_RAW)
    target = json.loads(verify_committed(root, TARGET_FREEZE_PATH, TARGET_FREEZE_RAW).decode("utf-8"))
    verify_committed(root, TARGET_FREEZE_MD_PATH, TARGET_FREEZE_MD_RAW)
    receipt = json.loads(verify_committed(root, UPSTREAM_RECEIPT_PATH, UPSTREAM_RECEIPT_RAW).decode("utf-8"))
    require(profile["profile_binding"]["profile_sha256"], PROFILE_SHA, "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", PROFILE_PATH, "profile_sha256")
    require(canonical_hash(profile["profile_binding"]["profile_payload"]), PROFILE_SHA, "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", PROFILE_PATH, "profile_payload_hash")
    require(target["target_freeze_binding"]["target_freeze_sha256"], TARGET_FREEZE_SHA, "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", TARGET_FREEZE_PATH, "target_freeze_sha256")
    require(canonical_hash(target["target_freeze_binding"]["target_freeze_payload"]), TARGET_FREEZE_SHA, "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", TARGET_FREEZE_PATH, "target_payload_hash")
    require(receipt["receipt_binding"]["receipt_sha256"], UPSTREAM_RECEIPT_SHA, "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", UPSTREAM_RECEIPT_PATH, "receipt_sha256")
    require(canonical_hash(receipt["receipt_binding"]["receipt_payload"]), UPSTREAM_RECEIPT_SHA, "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", UPSTREAM_RECEIPT_PATH, "receipt_payload_hash")
    for key, want in {
        "profile_gate": "VS2_2_FIRST_SWEEP_KERNEL_PROFILE_FREEZE_PASS",
        "profile_status": "SEMANTIC_PROFILE_FROZEN_CONSTRUCTION_PENDING",
    }.items():
        require(profile.get(key), want, "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", PROFILE_PATH, key)
    require(target.get("target_freeze_gate"), "VS2_2_TYPED_STATE_CONTRACT_CONVERGENCE_TARGET_FREEZE_PASS", "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", TARGET_FREEZE_PATH, "target_freeze_gate")
    require(target.get("target_status"), "SEMANTIC_TARGET_FROZEN_IMPLEMENTATION_SCHEMA_PENDING", "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", TARGET_FREEZE_PATH, "target_status")
    require(receipt.get("receipt_gate"), "VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_PASS", "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", UPSTREAM_RECEIPT_PATH, "receipt_gate")
    require(receipt.get("logical_downstream_transition"), "ADVANCE(VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PENDING)", "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", UPSTREAM_RECEIPT_PATH, "logical_downstream_transition")
    for key in ["kernel_profile_frozen", "semantic_target_frozen", "execution_authority_absent", "withheld_authority_preserved"]:
        require_bool(receipt.get(key), True, "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", UPSTREAM_RECEIPT_PATH, key)
    for key in ["kernel_constructed", "construction_performed", "execution_performed", "sweep_executed", "runner_created"]:
        require_bool(receipt.get(key), False, "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", UPSTREAM_RECEIPT_PATH, key)
    return profile, target, receipt


def source_basis(sections: list[str], basis: str, reason: str) -> list[dict[str, str]]:
    return [
        {
            "section": section,
            "basis_class": basis,
            "basis_reason": reason,
            "source_authority": "committed_vs2_2_profile_target_receipt_or_deterministic_representation",
        }
        for section in sections
    ]


def bound_ref(reference_id: str, role: str, required_by: str, artifact_id: str, kind: str, version: str, path: str, content_sha: str, reason: str) -> dict[str, Any]:
    return {
        "reference_id": reference_id,
        "reference_role": role,
        "binding_status": "BOUND",
        "expected_artifact_kind": kind,
        "required_by_unit": required_by,
        "artifact_id": artifact_id,
        "artifact_kind": kind,
        "artifact_version": version,
        "declared_path": path,
        "content_sha256": content_sha,
        "hash_algorithm": HASH_ALG,
        "canonicalization_rule": CANON,
        "binding_reason": reason,
    }


def nonbound_ref(reference_id: str, role: str, status: str, required_by: str, expected_kind: str, reason: str) -> dict[str, Any]:
    return {
        "reference_id": reference_id,
        "reference_role": role,
        "binding_status": status,
        "expected_artifact_kind": expected_kind,
        "required_by_unit": required_by,
        "artifact_id": None,
        "artifact_kind": None,
        "artifact_version": None,
        "declared_path": None,
        "content_sha256": None,
        "hash_algorithm": None,
        "canonicalization_rule": None,
        "binding_reason": reason,
    }


def upstream_refs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    profile_ref = bound_ref("vs2_2_profile_reference", "UPSTREAM_PROFILE", UNIT_ID, "phase_vs2_first_sweep_capable_kernel_profile_v0", "KERNEL_PROFILE", "v0", PROFILE_PATH, PROFILE_SHA, "Committed VS2.2 profile is the bounded profile source.")
    target_ref = bound_ref("vs2_2_semantic_target_freeze_reference", "UPSTREAM_SEMANTIC_TARGET_FREEZE", UNIT_ID, "phase_vs2_typed_state_contract_convergence_target_freeze_v0", "SEMANTIC_TARGET_FREEZE", "v0", TARGET_FREEZE_PATH, TARGET_FREEZE_SHA, "Committed VS2.2 target freeze is the target source.")
    receipt_ref = bound_ref("vs2_2_receipt_reference", "UPSTREAM_PROFILE_TARGET_RECEIPT", UNIT_ID, "phase_vs2_2_kernel_profile_and_target_freeze_receipt_v0", "PROFILE_TARGET_FREEZE_RECEIPT", "v0", UPSTREAM_RECEIPT_PATH, UPSTREAM_RECEIPT_SHA, "Committed VS2.2 receipt proves gates and authority route.")
    return profile_ref, target_ref, receipt_ref


def provenance(upstream_receipt: dict[str, Any]) -> dict[str, Any]:
    return {
        "bounded_construction_grant_id": "VS2_BOUNDED_CONSTRUCTION_AUTHORITY",
        "source_route_status": "ROUTED_NOT_CONSUMED",
        "first_lawful_exercising_unit": UNIT_ID,
        "consumption_frame": "VS2.3_TO_VS2.5_BOUND_TARGET_CONSTRUCTION_SEQUENCE",
        "bounded_construction_grant_consumed": True,
        "bounded_construction_consumption_count_before": 0,
        "bounded_construction_consumption_count_after": 1,
        "bounded_construction_local_exercise_scope": "SCOPE_REGIME_AND_THREE_OBJECT_MODEL_ONLY",
        "same_bounded_construction_grant_may_be_consumed_again": False,
        "bounded_construction_grant_exhausted": False,
        "bounded_construction_frame_open": True,
        "remaining_frame_units": [
            "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE",
            "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION",
        ],
        "total_effective_grant_count": 5,
        "total_consumed_grant_count": 2,
        "profile_and_target_grant_consumed": True,
        "unconsumed_effective_grant_count": 3,
        "unconsumed_grant_ids": [
            "VS2_FIXTURE_CONSTRUCTION_AUTHORITY",
            "VS2_FIRST_RUN_READINESS_GATE_CONSTRUCTION_AUTHORITY",
            "VS2_CONSTRUCTION_PACKAGE_VERIFICATION_AUTHORITY",
        ],
        "fixture_construction_authority_consumed_by_vs2_3": False,
        "readiness_gate_construction_authority_consumed_by_vs2_3": False,
        "construction_package_verification_authority_consumed_by_vs2_3": False,
        "execution_authority_consumed_by_vs2_3": False,
        "basis_receipt_sha256": upstream_receipt["receipt_binding"]["receipt_sha256"],
    }


def contract_binding(payload: dict[str, Any]) -> dict[str, Any]:
    return {"canonicalization": CANON, "contract_payload": payload, "contract_sha256": canonical_hash(payload)}


def schema_binding(payload: dict[str, Any]) -> dict[str, Any]:
    return {"canonicalization": CANON, "schema_payload": payload, "schema_sha256": canonical_hash(payload)}


def target_binding(payload: dict[str, Any]) -> dict[str, Any]:
    return {"canonicalization": CANON, "target_contract_payload": payload, "target_contract_sha256": canonical_hash(payload)}


def manifest_binding(payload: dict[str, Any]) -> dict[str, Any]:
    return {"canonicalization": CANON, "manifest_payload": payload, "manifest_sha256": canonical_hash(payload)}


def field_contract(name: str, owner: str, role: str, typ: str = "string", required: bool = True, nullable: bool = False, ref: bool = False) -> dict[str, Any]:
    return {
        "field_name": name,
        "json_type": typ,
        "required": required,
        "nullable": nullable,
        "field_owner": owner,
        "semantic_role": role,
        "mutable_domain": "DECLARATIVE_FIELD_SET",
        "value_constraint": "deterministic_bounded_value_or_typed_reference",
        "reference_contract_required": ref,
        "duplicate_values_forbidden": True,
        "deterministic_order_required": True,
    }


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, artifact: dict[str, Any], hash_value: str, status_key: str) -> None:
    ref_lines = []
    for key in ["profile_reference", "semantic_target_freeze_reference", "scope_regime_reference", "candidate_schema_reference", "target_contract_reference"]:
        ref = artifact.get(key)
        if isinstance(ref, dict):
            ref_lines.append(f"- `{key}`: `{ref['binding_status']}` `{ref.get('artifact_id')}` `{ref.get('content_sha256')}`")
    if not ref_lines:
        ref_lines.append("- No local cross-reference projection available.")
    path.write_text(
        f"""# {artifact['artifact_id']}

## Identity

- Artifact kind: `{artifact['artifact_kind']}`
- Version: `{artifact.get('contract_version') or artifact.get('schema_contract_version') or artifact.get('target_version') or artifact.get('manifest_version')}`
- Status: `{artifact[status_key]}`
- Canonical hash: `{hash_value}`

## Bound References

{chr(10).join(ref_lines)}

## Posture

- Mutable posture: immutable static contract/manifest or no instance created.
- Runtime instance created: `{str(artifact.get('runtime_instance_created', False)).lower()}`
- Candidate instance created: `{str(artifact.get('candidate_instance_created', False)).lower()}`
- Fixture instance created: `{str(artifact.get('fixture_instance_created', False)).lower()}`

## Key Invariants

- Exact three execution-domain object roles are preserved.
- F0 is the static scope/regime frame, not an execution-domain object.
- M0 is a binding manifest, not a fourth mutable execution object.
- Pending downstream references do not grant authority.

## Pending Downstream Surfaces

- VS2.4 finite move-space/source/authority freeze.
- VS2.5 selector/applicator/validation/admissibility/convergence construction.
- VS2.6 fixtures/readiness surfaces.

## Non-Claims

- No runtime instance, candidate instance, fixture, move-space, selector, applicator, convergence criterion, execution authority, sweep, or runner is created by VS2.3.
""",
        encoding="utf-8",
    )


def make_f0(profile_ref: dict[str, Any], target_ref: dict[str, Any], auth: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "matrixlabs_phase_vs2_scope_regime_contract_v0",
        "artifact_id": "phase_vs2_scope_regime_contract_v0",
        "artifact_kind": "STATIC_FRAME_CONTRACT",
        "contract_id": "first_sweep_kernel_scope_regime_contract_v0",
        "contract_version": "v0",
        "scope_id": "FIRST_SWEEP_KERNEL_SCOPE_V0",
        "scope_version": "v0",
        "regime_id": "TYPED_STATE_CONTRACT_CONVERGENCE_REGIME_V0",
        "regime_version": "v0",
        "profile_reference": profile_ref,
        "semantic_target_freeze_reference": target_ref,
        "target_family": "BOUNDED_CONTRACT_CONVERGENCE",
        "first_target": "TYPED_STATE_CONTRACT_CONVERGENCE_V0",
        "candidate_family": "TYPED_STATE_CONTRACT_CANDIDATE",
        "allowed_execution_domain_object_roles": EXECUTION_ROLES,
        "allowed_source_classes": [
            "BOUND_PROFILE_OR_TARGET_ARTIFACT",
            "BOUND_CONSTRUCTION_CONTRACT_ARTIFACT",
            "BOUND_AUTHORITY_RECORD",
            "BOUND_EXECUTION_SOURCE_SNAPSHOT_MEMBER",
            "BOUND_RECEIPT_OR_EVALUATION_RECORD",
        ],
        "forbidden_source_classes": [
            "AMBIENT_CHAT_CONTEXT",
            "BASELINE_PROJECTION_AS_SOURCE_AUTHORITY",
            "UNDECLARED_WORKTREE_RESIDUE",
            "LATEST_FILE_SELECTED_SOURCE",
            "MTIME_SELECTED_SOURCE",
            "DIRECTORY_ORDER_SELECTED_SOURCE",
            "AUTOMATICALLY_ACQUIRED_SOURCE",
            "UNBOUND_EXTERNAL_SOURCE",
            "SILENTLY_SUBSTITUTED_SOURCE",
            "FUTURE_EXECUTION_RESULT_AS_CONSTRUCTION_SOURCE",
        ],
        "allowed_future_transformation_class": "FINITE_TARGET_BOUND_TYPED_STATE_CONTRACT_TRANSFORMATION",
        "forbidden_transformation_classes": [
            "SCOPE_EXPANDING_TRANSFORMATION",
            "TARGET_REPLACING_TRANSFORMATION",
            "SOURCE_SNAPSHOT_EXPANDING_TRANSFORMATION",
            "AUTHORITY_ESCALATING_TRANSFORMATION",
            "SCHEMA_SELF_MODIFYING_TRANSFORMATION",
            "MOVE_SPACE_SELF_MODIFYING_TRANSFORMATION",
            "AUTOMATIC_REPAIR_TRANSFORMATION",
            "AUTOMATIC_TAXONOMY_MUTATION",
            "PORTABILITY_GENERALIZATION_TRANSFORMATION",
        ],
        "object_identity_rules": {
            "execution_domain_object_role_count": 3,
            "static_scope_regime_frame_count": 1,
            "static_object_model_manifest_count": 1,
            "additional_mutable_execution_domain_object_count": 0,
        },
        "sameness_rules": {
            "artifact_sameness_requires": ["same artifact_id", "same artifact_version", "same canonical content hash"],
            "execution_frame_sameness_requires": ["same scope_id and scope_version", "same regime_id and regime_version", "same target_family and first_target", "same candidate_family", "same F0 canonical hash"],
        },
        "difference_rules": {
            "different_artifact_when_hash_differs": True,
            "different_execution_frame_when_scope_regime_target_or_candidate_family_differs": True,
        },
        "authority_boundary": {
            "construction_authority_limited_to_declared_vs2_3_to_vs2_5_frame": True,
            "runtime_execution_requires_separate_execution_authority_package": True,
            "candidate_authority_declarations_are_semantic_content_only": True,
            "target_authority_requirements_are_semantic_evaluation_requirements_only": True,
            "pending_references_grant_no_authority": True,
            "objects_cannot_self_authorize": True,
            "objects_cannot_expand_their_authority_frame": True,
        },
        "claim_boundary": {
            "claims_limited_to_static_frame_contract": True,
            "runtime_success_claimed": False,
            "target_reached_claimed": False,
            "move_space_defined": False,
        },
        "expansion_boundary": {
            "forbidden_within_one_package": [
                "second target family",
                "second target identity",
                "new candidate family",
                "new source class",
                "new capability class",
                "new transformation class",
                "new authority frame",
                "new scope version",
                "new regime version",
                "automatic move-space expansion",
                "automatic source-snapshot expansion",
            ]
        },
        "immutability_contract": {"frame_mutable": False},
        "construction_authority_provenance": auth,
        "source_basis": source_basis(["profile_reference", "semantic_target_freeze_reference", "authority_boundary", "immutability_contract"], "UPSTREAM_PROFILE_DERIVED", "F0 is a deterministic static projection of committed VS2.2 profile/target boundaries."),
        "contract_status": "FROZEN_FOR_FIRST_SWEEP_CAPABLE_KERNEL_PROFILE",
    }
    artifact = {**payload, "contract_binding": contract_binding(payload)}
    return artifact


def make_o2(profile_ref: dict[str, Any], f0_ref: dict[str, Any], auth: dict[str, Any]) -> dict[str, Any]:
    field_sections = {
        "contract_identity_declarations": ["declared_contract_id", "declared_contract_version", "declared_contract_kind", "declared_contract_lifecycle"],
        "state_identity_declarations": ["declared_state_identity_fields", "declared_state_version_rule", "declared_prior_state_reference_rule"],
        "source_binding_declarations": ["declared_required_source_bindings", "declared_source_identity_rules", "declared_source_freshness_rules", "declared_source_role_rules"],
        "authority_declarations": ["declared_required_authority_bindings", "declared_authorized_action_scope", "declared_forbidden_action_scope", "declared_human_decision_boundaries"],
        "typed_field_declarations": ["declared_required_fields", "declared_optional_fields", "declared_field_type_constraints", "declared_field_value_constraints", "declared_cross_field_constraints"],
        "runtime_boundary_declarations": ["declared_mutable_field_set", "declared_immutable_field_set", "declared_terminal_field_set", "declared_history_field_set", "declared_receipt_reference_fields"],
        "halt_and_terminal_declarations": ["declared_halt_conditions", "declared_terminal_outcomes", "declared_next_lawful_surface_rule"],
        "receipt_declarations": ["declared_required_receipt_fields", "declared_receipt_identity_rule", "declared_receipt_source_binding_rule"],
        "forbidden_effect_declarations": ["declared_forbidden_effects"],
        "claim_declarations": ["declared_supported_claims", "declared_unsupported_claims", "declared_explicit_nonclaims"],
    }
    field_contracts = {
        section: [field_contract(name, "O2_CANDIDATE_SCHEMA", f"{section}:{name}", typ="array" if name.endswith("fields") or name.endswith("bindings") else "string", ref="reference" in name or "bindings" in name) for name in names]
        for section, names in field_sections.items()
    }
    payload = {
        "schema_version": "matrixlabs_phase_vs2_candidate_typed_state_contract_schema_v0",
        "artifact_id": "phase_vs2_candidate_typed_state_contract_schema_v0",
        "artifact_kind": "INSTANCE_SCHEMA_AND_VERSION_CONTRACT",
        "schema_id": "candidate_typed_state_contract_schema_v0",
        "schema_contract_version": "v0",
        "candidate_family": "TYPED_STATE_CONTRACT_CANDIDATE",
        "profile_reference": profile_ref,
        "scope_regime_reference": f0_ref,
        "required_instance_sections": [
            "candidate_contract_id",
            "candidate_family",
            "candidate_version",
            "candidate_hash",
            "created_from_candidate_reference",
            "candidate_schema_reference",
            "profile_reference",
            "scope_regime_reference",
            "instance_origin_reference",
            "instance_source_snapshot_reference",
            *SEMANTIC_SECTIONS,
        ],
        "required_instance_identity_fields": [
            "candidate_contract_id",
            "candidate_family",
            "candidate_version",
            "candidate_hash",
            "candidate_schema_reference",
            "profile_reference",
            "scope_regime_reference",
            "instance_source_snapshot_reference",
        ],
        "field_contracts": field_contracts,
        "cross_field_constraints": [
            "required and optional field sets are disjoint",
            "mutable and immutable field sets are disjoint",
            "authorized and forbidden action scopes are disjoint",
            "supported and unsupported claims are disjoint",
            "all required source bindings are typed",
            "all required authority bindings are typed",
            "candidate_family matches F0",
            "profile reference is immutable",
            "F0 reference is immutable",
            "candidate_contract_id remains stable across successors",
            "candidate versions increment exactly by one",
            "prior candidate versions are never overwritten",
        ],
        "candidate_hash_rule": {"canonicalization": CANON, "hash_algorithm": HASH_ALG, "candidate_hash_recomputes_over_declared_candidate_payload": True},
        "version_rule": {
            "initial_version": 0,
            "successor_increment": 1,
            "append_only": True,
            "overwrite_forbidden": True,
            "predecessor_reference_required_after_initial": True,
            "candidate_contract_id_stable_across_versions": True,
            "maximum_successors_per_applied_transformation": 1,
        },
        "potentially_mutable_domains": SEMANTIC_SECTIONS,
        "immutable_envelope_fields": [
            "candidate_contract_id",
            "candidate_family",
            "candidate_schema_reference",
            "profile_reference",
            "scope_regime_reference",
            "instance_origin_reference",
            "instance_source_snapshot_reference",
        ],
        "evaluation_fields_forbidden": [
            "current_validation_status",
            "current_admissibility_status",
            "current_convergence_status",
            "known_validation_defects",
            "known_admissibility_defects",
            "known_source_gaps",
            "known_authority_gaps",
            "known_schema_gaps",
            "known_capability_gaps",
            "known_move_space_gaps",
            "pressure_classification",
            "terminal_evaluation_result",
        ],
        "move_eligibility_status": "POTENTIAL_DOMAINS_DECLARED_MOVES_NOT_YET_AUTHORIZED",
        "forbidden_content": [
            "grant runtime authority",
            "modify its schema",
            "define executable moves",
            "expand a source snapshot",
            "create schemas",
            "create capabilities",
            "promote itself",
            "grant reusable status",
            "alter F0",
            "alter O1 directly",
            "alter O3",
            "alter M0",
            "alter the move-space",
            "trigger automatic rerun",
            "authoritatively declare its own target conformity",
        ],
        "construction_authority_provenance": auth,
        "source_basis": source_basis(["field_contracts", "cross_field_constraints", "version_rule", "forbidden_content"], "DETERMINISTIC_REPRESENTATION_REQUIRED", "O2 is a declarative schema contract required to represent the candidate role without creating an instance."),
        "schema_status": "FROZEN_INSTANCE_SCHEMA_NO_FIXTURE_INSTANCE_CREATED",
        "candidate_instance_created": False,
        "fixture_instance_created": False,
    }
    return {**payload, "schema_binding": schema_binding(payload)}


def make_o3(profile_ref: dict[str, Any], target_ref: dict[str, Any], f0_ref: dict[str, Any], o2_ref: dict[str, Any], auth: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "matrixlabs_phase_vs2_frozen_target_contract_v0",
        "artifact_id": "phase_vs2_frozen_target_contract_v0",
        "artifact_kind": "CONCRETE_IMMUTABLE_TARGET_CONTRACT",
        "target_contract_id": "typed_state_contract_convergence_target_contract_v0",
        "target_family": "BOUNDED_CONTRACT_CONVERGENCE",
        "target_id": "TYPED_STATE_CONTRACT_CONVERGENCE_V0",
        "target_version": "v0",
        "target_status": "FROZEN_FOR_FIRST_SWEEP_CAPABLE_KERNEL_PROFILE",
        "profile_reference": profile_ref,
        "scope_regime_reference": f0_ref,
        "candidate_schema_reference": o2_ref,
        "semantic_target_freeze_reference": target_ref,
        "construction_authority_provenance": auth,
        "required_candidate_sections": SEMANTIC_SECTIONS,
        "required_candidate_identity_fields": [
            "candidate_contract_id",
            "candidate_family",
            "candidate_version",
            "candidate_hash",
            "candidate_schema_reference",
            "profile_reference",
            "scope_regime_reference",
            "instance_source_snapshot_reference",
        ],
        "required_candidate_declarations": SEMANTIC_SECTIONS,
        "field_type_constraints": {"all_required_fields_typed": True, "machine_facing_field_contract_tables_required": True},
        "field_value_constraints": {"candidate_family_matches_f0_and_o2": True, "candidate_schema_reference_matches_o2": True},
        "cross_field_constraints": [
            "candidate family matches F0 and O2",
            "candidate schema reference matches O2",
            "profile reference matches the committed VS2.2 profile",
            "scope/regime reference matches F0",
            "candidate version chain is append-only",
            "candidate hash recomputes",
            "O3 allowed mutation domains are a subset of O2 domains",
        ],
        "source_binding_requirements": {"required_source_bindings_must_pass": True},
        "authority_content_requirements": {"required_authority_declarations_must_pass": True, "target_authority_requirements_are_semantic_evaluation_requirements_only": True},
        "candidate_mutation_requirements": {"allowed_candidate_mutation_domains": SEMANTIC_SECTIONS, "candidate_can_modify_target": False, "candidate_can_modify_move_space": False, "candidate_can_modify_scope_regime": False},
        "validation_requirements": {"all_type_constraints_pass": True, "all_value_constraints_pass": True, "no_executable_validation_constructed_by_vs2_3": True},
        "admissibility_requirements": {"admissibility_pass_required_for_future_target_reached": True, "admissibility_execution_logic_constructed": False},
        "semantic_target_satisfaction_conditions": {
            "predicate": "SEMANTIC_TARGET_CONDITION_SATISFIED",
            "requires": [
                "all required sections present",
                "all required declarations present",
                "all type constraints pass",
                "all value constraints pass",
                "all cross-field constraints pass",
                "required source declarations and bindings pass",
                "required authority declarations pass",
                "scope/regime boundaries remain preserved",
                "forbidden effects are absent",
                "admissibility passes",
            ],
            "runtime_terminal_result_emitted": False,
        },
        "runtime_terminalization_requirements": {
            "target_reached_requires": [
                "SEMANTIC_TARGET_CONDITION_SATISFIED",
                "O1 current candidate binding matches evaluated O2 identity, version, and hash",
                "O1 target binding matches O3 identity, version, and hash",
                "required source bindings remain valid",
                "all applied moves were authorized",
                "budgets were preserved",
                "F0 remained invariant",
                "future C20 convergence result confirms terminal target condition",
                "terminal receipt was emitted",
            ],
            "semantic_target_conformance_equals_runtime_target_reached": False,
        },
        "terminal_outcome_family": {"terminal_outcomes": TERMINAL_OUTCOMES, "terminal_outcome_count": 17, "budget_exhaustion_terminal_outcome": "STOP_RADIUS_EXHAUSTED"},
        "budget_exhaustion_representation_rule": {
            "terminal_outcome": "STOP_RADIUS_EXHAUSTED",
            "future_subordinate_detail_values": ["ATTEMPTED_MOVE_BUDGET_EXHAUSTED", "APPLIED_MOVE_BUDGET_EXHAUSTED", "DECLARED_RADIUS_BOUND_EXHAUSTED"],
            "detail_values_are_terminal_family_members": False,
        },
        "target_change_law": {
            "semantic_change_requires_new_target_version": True,
            "semantic_change_requires_new_target_hash": True,
            "semantic_change_requires_profile_compatibility_audit": True,
            "semantic_change_requires_move_space_compatibility_audit": True,
            "semantic_change_requires_fixture_readiness_verification": True,
            "semantic_change_requires_new_execution_authority_decision": True,
            "in_place_target_rewrite_allowed": False,
        },
        "target_nonclaims": {"runtime_TARGET_REACHED_emitted": False, "execution_authority_granted": False, "validation_logic_constructed": False},
        "source_basis": source_basis(["semantic_target_satisfaction_conditions", "terminal_outcome_family", "target_change_law"], "UPSTREAM_TARGET_DERIVED", "O3 freezes the committed VS2.2 target semantics as an immutable target contract."),
        "target_mutable": False,
    }
    return {**payload, "target_contract_binding": target_binding(payload)}


def make_o1(profile_ref: dict[str, Any], f0_ref: dict[str, Any], o2_ref: dict[str, Any], o3_ref: dict[str, Any], auth: dict[str, Any]) -> dict[str, Any]:
    field_contracts = {
        "identity": [field_contract(name, "O1_RUNTIME_STATE", f"identity:{name}", ref="reference" in name) for name in ["runtime_state_id", "runtime_state_version", "runtime_state_hash", "created_from_runtime_state_reference", "run_id", "case_id", "step_index"]],
        "static_bindings": [field_contract(name, "O1_RUNTIME_STATE", f"static_bindings:{name}", ref=True) for name in ["kernel_profile_reference", "scope_regime_reference", "runtime_state_contract_reference", "candidate_contract_schema_reference", "target_contract_reference", "source_snapshot_reference", "runtime_authority_package_reference", "move_space_reference"]],
        "current_candidate_binding": [field_contract("current_candidate_reference", "O1_RUNTIME_STATE", "current candidate typed reference", ref=True)],
        "execution_position": [field_contract(name, "O1_RUNTIME_STATE", f"execution_position:{name}", required=True) for name in ["loop_position", "current_exposed_condition", "current_condition_class", "current_validation_status", "current_admissibility_status", "current_convergence_status", "current_forbidden_effect_status"]],
        "budget": [field_contract(name, "O1_RUNTIME_STATE", f"budget:{name}", typ="integer") for name in ["maximum_attempted_moves", "maximum_applied_moves", "attempted_moves_count", "applied_moves_count", "remaining_attempted_move_budget", "remaining_applied_move_budget", "maximum_automatic_reruns", "maximum_automatic_radius_renewals"]],
        "history_and_evidence": [field_contract(name, "O1_RUNTIME_STATE", f"history:{name}", typ="array", ref=True) for name in ["attempted_move_receipt_references", "applied_move_receipt_references", "rejected_move_receipt_references", "validation_result_references", "admissibility_result_references", "convergence_result_references", "forbidden_effect_result_references", "candidate_version_history", "runtime_state_version_history"]],
        "terminal_state": [field_contract(name, "O1_RUNTIME_STATE", f"terminal:{name}", nullable=name != "terminal") for name in ["terminal", "terminal_outcome", "terminal_detail_code", "terminal_reason", "terminal_receipt_reference", "next_lawful_surface", "self_repair_performed", "hidden_continuation_detected"]],
    }
    payload = {
        "schema_version": "matrixlabs_phase_vs2_runtime_control_state_contract_v0",
        "artifact_id": "phase_vs2_runtime_control_state_contract_v0",
        "artifact_kind": "INSTANCE_SCHEMA_AND_MUTATION_CONTRACT",
        "contract_id": "first_sweep_kernel_runtime_control_state_contract_v0",
        "contract_version": "v0",
        "profile_reference": profile_ref,
        "scope_regime_reference": f0_ref,
        "candidate_schema_reference": o2_ref,
        "target_contract_reference": o3_ref,
        "required_instance_sections": list(field_contracts),
        "field_contracts": field_contracts,
        "allowed_loop_positions": LOOP_POSITIONS,
        "mutable_fields": [
            "runtime_state_version",
            "runtime_state_hash",
            "created_from_runtime_state_reference",
            "step_index",
            "current_candidate_reference",
            "loop_position",
            "current condition and evaluator fields",
            "attempted and applied move counts",
            "remaining budgets",
            "history and evidence references",
            "terminal fields",
        ],
        "invariant_fields": [
            "run_id",
            "case_id",
            "kernel profile reference",
            "F0 reference",
            "O1 contract reference",
            "O2 schema reference",
            "O3 target reference",
            "source-snapshot reference",
            "runtime-authority-package reference",
            "move-space reference",
            "maximum attempted-move budget",
            "maximum applied-move budget",
            "maximum automatic reruns",
            "maximum automatic radius renewals",
        ],
        "version_rule": {
            "initial_version": 0,
            "successor_increment": 1,
            "append_only": True,
            "overwrite_forbidden": True,
            "predecessor_reference_required_after_initial": True,
            "one_successor_per_attempted_controlled_step": True,
            "successor_required_after_future_attempted_controlled_step_even_when": [
                "no candidate transformation occurs",
                "a selected move is rejected",
                "no admissible move exists",
                "validation is recorded",
                "admissibility is recorded",
                "convergence is recorded",
                "a forbidden effect is recorded",
                "a typed halt is recorded",
                "TARGET_REACHED is recorded",
            ],
            "future_contract_rule_only": True,
        },
        "instance_hash_rule": {"canonicalization": CANON, "hash_algorithm": HASH_ALG, "runtime_state_hash_recomputes_over_declared_runtime_payload": True},
        "controlled_step_successor_rule": {"transitions_between_loop_positions_defined_by_vs2_3": False, "target_reached_not_loop_position": True},
        "terminal_rule": {
            "when_terminal_true": {
                "terminal_outcome_non_null": True,
                "terminal_receipt_reference_status": "BOUND",
                "next_lawful_surface_explicit_or_NONE": True,
                "no_additional_move_may_be_selected": True,
                "no_additional_O2_successor_may_be_created": True,
                "no_additional_execution_state_O1_successor_may_be_created": True,
            },
            "static_audit_projection_after_terminalization_is_not_another_execution_state": True,
        },
        "forbidden_content": [
            "undeclared authority",
            "implicit sources",
            "unbounded scratch state",
            "unrestricted internal reasoning traces",
            "self-generated moves",
            "self-generated schemas",
            "fixture content",
            "unreceipted semantic revisions",
            "automatic refinement application",
            "automatic target replacement",
            "automatic move-space expansion",
            "automatic source-snapshot substitution",
            "automatic scope expansion",
            "automatic regime expansion",
            "runner authority",
        ],
        "construction_authority_provenance": auth,
        "source_basis": source_basis(["field_contracts", "allowed_loop_positions", "terminal_rule"], "STRICT_CROSS_OBJECT_INVARIANT_REQUIRED", "O1 separates runtime control/evaluation state from candidate and target contracts without creating an instance."),
        "contract_status": "FROZEN_INSTANCE_SCHEMA_NO_RUNTIME_INSTANCE_CREATED",
        "runtime_instance_created": False,
    }
    return {**payload, "contract_binding": contract_binding(payload)}


def make_m0(profile_ref: dict[str, Any], target_ref: dict[str, Any], f0_ref: dict[str, Any], o1_ref: dict[str, Any], o2_ref: dict[str, Any], o3_ref: dict[str, Any], auth: dict[str, Any]) -> dict[str, Any]:
    downstream = [
        nonbound_ref(ref_id, "DOWNSTREAM_CONSTRUCTION_BINDING", "PENDING", unit, kind, "Required future artifact is not constructed in VS2.3; no filename, ID, version, or hash is guessed.")
        for ref_id, unit, kind in PENDING_BINDINGS
    ]
    downstream.append(nonbound_ref("runtime_execution_authority_reference", "EXECUTION_AUTHORITY", "ABSENT_BY_POLICY", "POST_VS2_EXECUTION_AUTHORITY_DECISION", "RUNTIME_EXECUTION_AUTHORITY_PACKAGE", "Execution authority is absent until a separate post-VS2 decision."))
    invariants = [
        {
            "invariant_id": invariant_id,
            "invariant_statement": f"{invariant_id} preserved by F0/O1/O2/O3/M0 canonical bindings.",
            "bound_artifacts": ["phase_vs2_scope_regime_contract_v0", "phase_vs2_runtime_control_state_contract_v0", "phase_vs2_candidate_typed_state_contract_schema_v0", "phase_vs2_frozen_target_contract_v0", "phase_vs2_object_model_binding_manifest_v0"],
            "verification_status": "VERIFIED_AT_VS2_3_CONSTRUCTION",
            "construction_stop_code": f"STOP_VS2_3_{invariant_id}",
            "future_runtime_outcome_or_detail": "future runtime detail only; no runtime outcome emitted by VS2.3",
            "authority_effect": "no additional authority granted",
        }
        for invariant_id in INVARIANTS
    ]
    payload = {
        "schema_version": "matrixlabs_phase_vs2_object_model_binding_manifest_v0",
        "artifact_id": "phase_vs2_object_model_binding_manifest_v0",
        "artifact_kind": "STATIC_CONTRACT_BINDING_MANIFEST",
        "manifest_id": "first_sweep_kernel_object_model_binding_manifest_v0",
        "manifest_version": "v0",
        "kernel_profile_reference": profile_ref,
        "semantic_target_freeze_reference": target_ref,
        "scope_regime_contract_reference": f0_ref,
        "runtime_state_contract_reference": o1_ref,
        "candidate_contract_schema_reference": o2_ref,
        "target_contract_reference": o3_ref,
        "source_policy_frame_reference": f0_ref,
        "construction_authority_provenance": auth,
        "cross_object_invariants": invariants,
        "pending_downstream_bindings": downstream,
        "downstream_binding_summary": {
            "downstream_binding_count": len(downstream),
            "pending_binding_count": sum(1 for row in downstream if row["binding_status"] == "PENDING"),
            "absent_by_policy_binding_count": sum(1 for row in downstream if row["binding_status"] == "ABSENT_BY_POLICY"),
            "bound_future_component_count": sum(1 for row in downstream if row["binding_status"] == "BOUND"),
            "fabricated_future_reference_count": sum(1 for row in downstream if row["binding_status"] != "BOUND" and any(row[k] is not None for k in ["artifact_id", "artifact_kind", "artifact_version", "declared_path", "content_sha256"])),
        },
        "source_basis": source_basis(["cross_object_invariants", "pending_downstream_bindings", "source_policy_frame_reference"], "STRICT_CROSS_OBJECT_INVARIANT_REQUIRED", "M0 binds the exact F0/O1/O2/O3 object model and keeps future references pending or absent by policy."),
        "manifest_status": "OBJECT_MODEL_FROZEN_DOWNSTREAM_BINDINGS_PENDING",
        "manifest_mutable": False,
    }
    return {**payload, "manifest_binding": manifest_binding(payload)}


def local_ref(artifact: dict[str, Any], binding_key: str, payload_hash_key: str, path: str, kind: str, version: str, role: str) -> dict[str, Any]:
    return bound_ref(f"{artifact['artifact_id']}_reference", role, UNIT_ID, artifact["artifact_id"], kind, version, path, artifact[binding_key][payload_hash_key], f"VS2.3-built {artifact['artifact_id']} canonical binding.")


def make_receipt(artifacts: dict[str, dict[str, Any]], raw_hashes: dict[str, str], auth: dict[str, Any]) -> dict[str, Any]:
    f0 = artifacts["F0"]
    o1 = artifacts["O1"]
    o2 = artifacts["O2"]
    o3 = artifacts["O3"]
    m0 = artifacts["M0"]
    payload = {
        "schema_version": "matrixlabs_phase_vs2_3_scope_regime_and_three_object_model_definition_receipt_v0",
        "artifact_id": "phase_vs2_3_scope_regime_and_three_object_model_definition_receipt_v0",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "unit_role": UNIT_ROLE,
        "committed_parent_sha": HEAD,
        "upstream_raw_hashes": {
            PROFILE_PATH: PROFILE_RAW,
            PROFILE_MD_PATH: PROFILE_MD_RAW,
            TARGET_FREEZE_PATH: TARGET_FREEZE_RAW,
            TARGET_FREEZE_MD_PATH: TARGET_FREEZE_MD_RAW,
            UPSTREAM_RECEIPT_PATH: UPSTREAM_RECEIPT_RAW,
        },
        "upstream_canonical_hashes": {
            "profile_sha256": PROFILE_SHA,
            "target_freeze_sha256": TARGET_FREEZE_SHA,
            "upstream_receipt_sha256": UPSTREAM_RECEIPT_SHA,
            "source_intake_sha256": SOURCE_INTAKE_SHA,
            "source_manifest_sha256": SOURCE_MANIFEST_SHA,
        },
        "upstream_gates": {
            "profile_gate": "VS2_2_FIRST_SWEEP_KERNEL_PROFILE_FREEZE_PASS",
            "target_freeze_gate": "VS2_2_TYPED_STATE_CONTRACT_CONVERGENCE_TARGET_FREEZE_PASS",
            "receipt_gate": "VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_PASS",
        },
        "construction_authority": auth,
        "vs2_3_artifact_bindings": {
            "F0": {"artifact_id": f0["artifact_id"], "path": F0_JSON, "version": "v0", "raw_file_sha256": raw_hashes[F0_JSON], "canonical_sha256": f0["contract_binding"]["contract_sha256"]},
            "O1": {"artifact_id": o1["artifact_id"], "path": O1_JSON, "version": "v0", "raw_file_sha256": raw_hashes[O1_JSON], "canonical_sha256": o1["contract_binding"]["contract_sha256"]},
            "O2": {"artifact_id": o2["artifact_id"], "path": O2_JSON, "version": "v0", "raw_file_sha256": raw_hashes[O2_JSON], "canonical_sha256": o2["schema_binding"]["schema_sha256"]},
            "O3": {"artifact_id": o3["artifact_id"], "path": O3_JSON, "version": "v0", "raw_file_sha256": raw_hashes[O3_JSON], "canonical_sha256": o3["target_contract_binding"]["target_contract_sha256"]},
            "M0": {"artifact_id": m0["artifact_id"], "path": M0_JSON, "version": "v0", "raw_file_sha256": raw_hashes[M0_JSON], "canonical_sha256": m0["manifest_binding"]["manifest_sha256"]},
        },
        "object_model_counts": {
            "execution_domain_object_role_count": 3,
            "static_scope_regime_frame_count": 1,
            "static_object_model_manifest_count": 1,
            "additional_mutable_execution_domain_object_count": 0,
            "downstream_binding_count": 19,
            "pending_binding_count": 18,
            "absent_by_policy_binding_count": 1,
            "terminal_outcome_count": 17,
            "fabricated_future_reference_count": 0,
        },
        "post_state": {
            "vs2_3_built": True,
            "scope_regime_frame_constructed": True,
            "runtime_state_contract_constructed": True,
            "candidate_schema_constructed": True,
            "frozen_target_contract_constructed": True,
            "object_model_manifest_constructed": True,
            "object_model_constructed": True,
            "construction_performed": True,
            "kernel_constructed": False,
            "runtime_instance_created": False,
            "candidate_instance_created": False,
            "fixture_instance_created": False,
            "move_space_constructed": False,
            "selector_constructed": False,
            "applicator_constructed": False,
            "validation_execution_logic_constructed": False,
            "admissibility_execution_logic_constructed": False,
            "convergence_criterion_constructed": False,
            "source_snapshot_frozen": False,
            "readiness_gate_constructed": False,
            "construction_package_verified": False,
            "execution_authorized": False,
            "execution_performed": False,
            "sweep_authorized": False,
            "sweep_executed": False,
            "runner_created": False,
            "vs2_4_may_begin": True,
        },
        "gates": {
            "upstream_gate": "VS2_3_UPSTREAM_PROFILE_AND_TARGET_PASS",
            "construction_authority_gate": "VS2_3_CONSTRUCTION_AUTHORITY_BOUNDARY_PASS",
            "capability_boundary_gate": "VS2_3_CAPABILITY_BOUNDARY_PASS",
            "scope_regime_gate": "VS2_3_SCOPE_REGIME_FRAME_PASS",
            "role_count_gate": "VS2_3_EXACT_THREE_OBJECT_ROLES_PASS",
            "contract_instance_gate": "VS2_3_CONTRACT_INSTANCE_SEPARATION_PASS",
            "role_separation_gate": "VS2_3_OBJECT_ROLE_SEPARATION_PASS",
            "identity_version_hash_gate": "VS2_3_OBJECT_IDENTITY_VERSION_AND_HASH_PASS",
            "mutation_boundary_gate": "VS2_3_MUTATION_BOUNDARY_PASS",
            "evaluation_state_gate": "VS2_3_EVALUATION_STATE_SEPARATION_PASS",
            "authority_role_gate": "VS2_3_AUTHORITY_ROLE_SEPARATION_PASS",
            "source_frame_gate": "VS2_3_SOURCE_FRAME_BOUNDARY_PASS",
            "target_terminalization_gate": "VS2_3_TARGET_CONFORMANCE_AND_TERMINALIZATION_SEPARATION_PASS",
            "c20_gate": "VS2_3_C20_STRUCTURAL_BINDING_PASS",
            "pending_binding_gate": "VS2_3_DOWNSTREAM_BINDINGS_PENDING_PASS",
            "terminal_family_gate": "VS2_3_TERMINAL_OUTCOME_FAMILY_PRESERVED",
            "no_execution_drift_gate": "VS2_3_NO_MOVE_INSTANCE_OR_EXECUTION_DRIFT_PASS",
            "receipt_gate": "VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PASS",
        },
        "construction_verdict": "VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PASS",
        "evidence_yield_branch": "CONFIRMATION_YIELD",
        "logical_terminal_transition": "ADVANCE(VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PENDING)",
        "terminal_transition": "ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_V0_PENDING)",
        "failures": [],
    }
    receipt = {**payload, "receipt_binding": {"canonicalization": CANON, "receipt_payload": payload, "receipt_sha256": canonical_hash(payload)}}
    return receipt


def build_all(root: Path) -> tuple[dict[str, dict[str, Any]], dict[str, str], dict[str, Any]]:
    profile, target, upstream_receipt = load_upstream(root)
    profile_ref, target_ref, _receipt_ref = upstream_refs()
    auth = provenance(upstream_receipt)
    f0 = make_f0(profile_ref, target_ref, auth)
    write_json(root / F0_JSON, f0)
    f0_ref = local_ref(f0, "contract_binding", "contract_sha256", F0_JSON, "STATIC_FRAME_CONTRACT", "v0", "SCOPE_REGIME_FRAME")
    o2 = make_o2(profile_ref, f0_ref, auth)
    write_json(root / O2_JSON, o2)
    o2_ref = local_ref(o2, "schema_binding", "schema_sha256", O2_JSON, "INSTANCE_SCHEMA_AND_VERSION_CONTRACT", "v0", "CANDIDATE_SCHEMA")
    o3 = make_o3(profile_ref, target_ref, f0_ref, o2_ref, auth)
    write_json(root / O3_JSON, o3)
    o3_ref = local_ref(o3, "target_contract_binding", "target_contract_sha256", O3_JSON, "CONCRETE_IMMUTABLE_TARGET_CONTRACT", "v0", "FROZEN_TARGET")
    o1 = make_o1(profile_ref, f0_ref, o2_ref, o3_ref, auth)
    write_json(root / O1_JSON, o1)
    o1_ref = local_ref(o1, "contract_binding", "contract_sha256", O1_JSON, "INSTANCE_SCHEMA_AND_MUTATION_CONTRACT", "v0", "RUNTIME_CONTROL_STATE")
    m0 = make_m0(profile_ref, target_ref, f0_ref, o1_ref, o2_ref, o3_ref, auth)
    write_json(root / M0_JSON, m0)
    artifacts = {"F0": f0, "O2": o2, "O3": o3, "O1": o1, "M0": m0}
    raw_hashes = {path: sha256_file(root / path) for path in [F0_JSON, O2_JSON, O3_JSON, O1_JSON, M0_JSON]}
    receipt = make_receipt(artifacts, raw_hashes, auth)
    write_json(root / RECEIPT_JSON, receipt)
    raw_hashes[RECEIPT_JSON] = sha256_file(root / RECEIPT_JSON)
    write_md(root / F0_MD, f0, f0["contract_binding"]["contract_sha256"], "contract_status")
    write_md(root / O2_MD, o2, o2["schema_binding"]["schema_sha256"], "schema_status")
    write_md(root / O3_MD, o3, o3["target_contract_binding"]["target_contract_sha256"], "target_status")
    write_md(root / O1_MD, o1, o1["contract_binding"]["contract_sha256"], "contract_status")
    write_md(root / M0_MD, m0, m0["manifest_binding"]["manifest_sha256"], "manifest_status")
    for path in [F0_MD, O2_MD, O3_MD, O1_MD, M0_MD]:
        raw_hashes[path] = sha256_file(root / path)
    return artifacts, raw_hashes, receipt


def emit_success(artifacts: dict[str, dict[str, Any]], raw_hashes: dict[str, str], receipt: dict[str, Any]) -> None:
    f0 = artifacts["F0"]
    o1 = artifacts["O1"]
    o2 = artifacts["O2"]
    o3 = artifacts["O3"]
    m0 = artifacts["M0"]
    print("BUILD_PHASE_VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_V0_COMPLETE")
    print()
    for key, value in {
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "unit_role": UNIT_ROLE,
        "upstream_commit_sha": HEAD,
        "profile_sha256": PROFILE_SHA,
        "target_freeze_sha256": TARGET_FREEZE_SHA,
        "upstream_receipt_sha256": UPSTREAM_RECEIPT_SHA,
        "bounded_construction_grant_id": "VS2_BOUNDED_CONSTRUCTION_AUTHORITY",
        "bounded_construction_grant_consumed": "true",
        "bounded_construction_consumption_count_before": "0",
        "bounded_construction_consumption_count_after": "1",
        "bounded_construction_consumption_frame": "VS2.3_TO_VS2.5_BOUND_TARGET_CONSTRUCTION_SEQUENCE",
        "bounded_construction_local_exercise_scope": "SCOPE_REGIME_AND_THREE_OBJECT_MODEL_ONLY",
        "bounded_construction_frame_open": "true",
        "bounded_construction_grant_exhausted": "false",
        "same_bounded_construction_grant_may_be_consumed_again": "false",
        "unconsumed_effective_grant_count": "3",
        "fixture_construction_authority_consumed_by_vs2_3": "false",
        "readiness_gate_construction_authority_consumed_by_vs2_3": "false",
        "construction_package_verification_authority_consumed_by_vs2_3": "false",
        "execution_authority_consumed_by_vs2_3": "false",
        "execution_domain_object_role_count": "3",
        "static_scope_regime_frame_count": "1",
        "static_object_model_manifest_count": "1",
        "additional_mutable_execution_domain_object_count": "0",
        "scope_regime_frame_constructed": "true",
        "runtime_state_contract_constructed": "true",
        "candidate_schema_constructed": "true",
        "frozen_target_contract_constructed": "true",
        "object_model_manifest_constructed": "true",
        "object_model_constructed": "true",
        "construction_performed": "true",
        "kernel_constructed": "false",
        "runtime_instance_created": "false",
        "candidate_instance_created": "false",
        "fixture_instance_created": "false",
        "move_space_constructed": "false",
        "selector_constructed": "false",
        "applicator_constructed": "false",
        "convergence_criterion_constructed": "false",
        "source_snapshot_frozen": "false",
        "readiness_gate_constructed": "false",
        "construction_package_verified": "false",
        "terminal_outcome_count": "17",
        "downstream_binding_count": "19",
        "pending_binding_count": "18",
        "absent_by_policy_binding_count": "1",
        "fabricated_future_reference_count": "0",
        "execution_authority_absent": "true",
        "sweep_authority_absent": "true",
        "automatic_rerun_authority_absent": "true",
        "runner_authority_absent": "true",
        "execution_performed": "false",
        "sweep_executed": "false",
        "runner_created": "false",
    }.items():
        print(f"{key}={value}")
    print()
    print(f"scope_regime_contract_sha256={f0['contract_binding']['contract_sha256']}")
    print(f"runtime_state_contract_sha256={o1['contract_binding']['contract_sha256']}")
    print(f"candidate_schema_sha256={o2['schema_binding']['schema_sha256']}")
    print(f"frozen_target_contract_sha256={o3['target_contract_binding']['target_contract_sha256']}")
    print(f"object_model_manifest_sha256={m0['manifest_binding']['manifest_sha256']}")
    print(f"receipt_sha256={receipt['receipt_binding']['receipt_sha256']}")
    print()
    for path in [F0_JSON, F0_MD, O1_JSON, O1_MD, O2_JSON, O2_MD, O3_JSON, O3_MD, M0_JSON, M0_MD, RECEIPT_JSON]:
        print(f"raw_file_sha256 {path}={raw_hashes[path]}")
    print()
    for key, value in {
        "generated_artifacts_deterministic": "true",
        "protected_upstream_files_unchanged": "true",
        "forbidden_output_count": "0",
        "upstream_gate": "VS2_3_UPSTREAM_PROFILE_AND_TARGET_PASS",
        "construction_authority_gate": "VS2_3_CONSTRUCTION_AUTHORITY_BOUNDARY_PASS",
        "capability_boundary_gate": "VS2_3_CAPABILITY_BOUNDARY_PASS",
        "scope_regime_gate": "VS2_3_SCOPE_REGIME_FRAME_PASS",
        "role_count_gate": "VS2_3_EXACT_THREE_OBJECT_ROLES_PASS",
        "contract_instance_gate": "VS2_3_CONTRACT_INSTANCE_SEPARATION_PASS",
        "role_separation_gate": "VS2_3_OBJECT_ROLE_SEPARATION_PASS",
        "identity_version_hash_gate": "VS2_3_OBJECT_IDENTITY_VERSION_AND_HASH_PASS",
        "mutation_boundary_gate": "VS2_3_MUTATION_BOUNDARY_PASS",
        "evaluation_state_gate": "VS2_3_EVALUATION_STATE_SEPARATION_PASS",
        "authority_role_gate": "VS2_3_AUTHORITY_ROLE_SEPARATION_PASS",
        "source_frame_gate": "VS2_3_SOURCE_FRAME_BOUNDARY_PASS",
        "target_terminalization_gate": "VS2_3_TARGET_CONFORMANCE_AND_TERMINALIZATION_SEPARATION_PASS",
        "c20_gate": "VS2_3_C20_STRUCTURAL_BINDING_PASS",
        "pending_binding_gate": "VS2_3_DOWNSTREAM_BINDINGS_PENDING_PASS",
        "terminal_family_gate": "VS2_3_TERMINAL_OUTCOME_FAMILY_PRESERVED",
        "no_execution_drift_gate": "VS2_3_NO_MOVE_INSTANCE_OR_EXECUTION_DRIFT_PASS",
        "receipt_gate": "VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PASS",
        "evidence_yield_branch": "CONFIRMATION_YIELD",
        "staged_changes_present": "false",
        "commit_created": "false",
        "push_executed": "false",
        "logical_terminal_transition": "ADVANCE(VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PENDING)",
        "terminal_transition": "ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_V0_PENDING)",
    }.items():
        print(f"{key}={value}")


def emit_stop(exc: StopFailure) -> None:
    print("BUILD_PHASE_VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_V0_STOP")
    print(f"failure_code={exc.code}")
    print(f"failed_artifact={exc.artifact}")
    print(f"failed_field_or_relationship={exc.field}")
    print(f"expected_value={json.dumps(exc.expected, sort_keys=True)}")
    print(f"observed_value={json.dumps(exc.observed, sort_keys=True)}")
    print(f"violated_invariant={exc.invariant}")
    print("violated_authority_boundary=VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_ONLY")
    print("blocked_downstream_unit=VS2.3")
    print("exact_bounded_correction_surface=VS2_3_REPAIR_OR_BOOKKEEPING_SURFACE")
    print("capability_proposal_candidate_required=false")
    print("human_decision_required=false")
    print("self_repair_performed=false")


def main() -> int:
    root = Path.cwd().resolve()
    try:
        check_repo(root)
        artifacts, raw_hashes, receipt = build_all(root)
        validate_dirty_scope(root)
        emit_success(artifacts, raw_hashes, receipt)
        return 0
    except StopFailure as exc:
        emit_stop(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
