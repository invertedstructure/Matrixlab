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
HEAD = "99ed9ab2244c95d781ee709088839a79236f173b"
PHASE_ID = "PHASE_VS2"
UNIT_ID = "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE"
UNIT_ROLE = "FINITE_MOVE_SPACE_SOURCE_BINDING_AND_PROSPECTIVE_AUTHORITY_CONSTRUCTION_ONLY"
CANON = "MATRIXLAB_CANONICAL_JSON_V0"
HASH_ALG = "SHA-256"

PROFILE_PATH = "docs/matrixlabs/phase_vs2/phase_vs2_first_sweep_capable_kernel_profile_v0.json"
TARGET_FREEZE_PATH = "docs/matrixlabs/phase_vs2/phase_vs2_typed_state_contract_convergence_target_freeze_v0.json"
F0_JSON = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_scope_regime_contract_v0.json"
F0_MD = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_scope_regime_contract_v0.md"
O1_JSON = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_runtime_control_state_contract_v0.json"
O1_MD = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_runtime_control_state_contract_v0.md"
O2_JSON = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_candidate_typed_state_contract_schema_v0.json"
O2_MD = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_candidate_typed_state_contract_schema_v0.md"
O3_JSON = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_frozen_target_contract_v0.json"
O3_MD = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_frozen_target_contract_v0.md"
M0_JSON = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_object_model_binding_manifest_v0.json"
M0_MD = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_object_model_binding_manifest_v0.md"
VS2_3_RECEIPT_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_3_scope_regime_and_three_object_model_definition_receipt_v0.json"

S0_JSON = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_source_and_version_binding_contract_v0.json"
S0_MD = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_source_and_version_binding_contract_v0.md"
V0_JSON = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_move_vocabulary_partition_v0.json"
V0_MD = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_move_vocabulary_partition_v0.md"
A0_JSON = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_move_authority_matrix_v0.json"
A0_MD = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_move_authority_matrix_v0.md"
MS0_JSON = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_finite_move_space_v0.json"
MS0_MD = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_finite_move_space_v0.md"
P0_JSON = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_prospective_controlled_step_authority_envelope_v0.json"
P0_MD = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_prospective_controlled_step_authority_envelope_v0.md"
M1_JSON = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_move_space_binding_manifest_v0.json"
M1_MD = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_move_space_binding_manifest_v0.md"
RECEIPT_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_4_finite_move_space_source_and_authority_freeze_receipt_v0.json"

SCRIPT = "scripts/build_phase_vs2_4_finite_move_space_source_and_authority_freeze_v0.py"
VERIFY_SCRIPT = "scripts/verify_phase_vs2_4_finite_move_space_source_and_authority_freeze_v0.py"
BASELINE_SCRIPT = "scripts/build_baseline_share_v0.py"

EXPECTED_RAW = {
    F0_JSON: "afda05e34228cc40a2bcd476105c1f6c0f747717db3a3d7e657fcec84c53ffb1",
    F0_MD: "bd787bdbaaf87da3b804659a99d5334f4603cce0a6e6cc75787eccf629fb76ae",
    O1_JSON: "944eead2d69a2690b9ad61cb93b288abb9a4f05d98e1f76d7012113bed7c975e",
    O1_MD: "bab3c65157cfbe22f9ae82b5005e6689abe49ca66dcff986ce4dcd6e47792d29",
    O2_JSON: "d2b0beb329b4caf56ef9569a4100fd6aff6b2f7df1fa67b1dff5087234f5d32a",
    O2_MD: "edac672e791e19e98cf9d762331f9cdca203b87feeb45138c53ab432834d94ee",
    O3_JSON: "6cc4952517fbb1718e3247c5465c60ba1281e390fc12c38485163b6e0d6b91eb",
    O3_MD: "483bd540ce9861ce5f8cb014a07d45c243ce1344a8f6e8d333f695e44f712401",
    M0_JSON: "2586a52032d91fb4addb4ae12facb421423fef0979083174f97f51cc1cabdf71",
    M0_MD: "98d8bf95cc335d441b6e4c6915e34c7930e6c7f59932d3d3a073dbfa92112def",
    VS2_3_RECEIPT_JSON: "04ec78427d317b127d4c7d0f1ec50e159f8b7385ff56d8470132eec22fb51ef0",
}
EXPECTED_CANONICAL = {
    F0_JSON: "a6b4819aee35e5f09686a5a69d471b31f3a5cfdcab2078a29323ba1d31211179",
    O1_JSON: "25fbdfb007372e346d61a3f5de8b0a4f5004c6dff1857e5fc31df38e17c087ad",
    O2_JSON: "0216eb5944f87e760844d018d253f5e808a7a5b7ebd208d8d717e6709b979070",
    O3_JSON: "378acf4fb02ad20bfd5213bde4b267fe605dc528812e29a985909fef251d7546",
    M0_JSON: "0af5f635aaca5c37428cc94ca1a8ee6f3885d6e56543198bbdd33a5d4062db3c",
    VS2_3_RECEIPT_JSON: "61a2298c0d04fa3acf47c391cc593df70be1d8e239e26de891d88b05ac879d0c",
}

CORE_ARTIFACTS = [
    S0_JSON,
    S0_MD,
    V0_JSON,
    V0_MD,
    A0_JSON,
    A0_MD,
    MS0_JSON,
    MS0_MD,
    P0_JSON,
    P0_MD,
    M1_JSON,
    M1_MD,
    RECEIPT_JSON,
]
CORE_JSON = [S0_JSON, V0_JSON, A0_JSON, MS0_JSON, P0_JSON, M1_JSON, RECEIPT_JSON]
CORE_MD = [S0_MD, V0_MD, A0_MD, MS0_MD, P0_MD, M1_MD]

ALLOWED_DIRTY = set(CORE_ARTIFACTS) | {
    SCRIPT,
    VERIFY_SCRIPT,
    BASELINE_SCRIPT,
    "baseline_share/COMMIT_CONTEXT.md",
    "baseline_share/CURRENT_STATE.md",
    "baseline_share/MANIFEST.json",
    "baseline_share/RECEIPT_POINTERS.md",
}
PROTECTED_UPSTREAM = set(EXPECTED_RAW)

MOVE_IDS = [
    "M01_ADD_AUTHORIZED_REQUIRED_FIELD",
    "M02_NORMALIZE_TYPED_VALUE",
    "M03_BIND_DECLARED_SOURCE_IDENTITY",
    "M04_BIND_DECLARED_SOURCE_FRESHNESS",
    "M05_REMOVE_PROHIBITED_CANDIDATE_DECLARATION",
    "M06_TIGHTEN_AMBIGUOUS_BOUNDARY",
    "M07_SPLIT_CONFLATED_DECLARATION",
    "M08_REJECT_UNSUPPORTED_CLAIM",
]
OBSERVATIONS = [
    "OBS_TARGET_ALREADY_REACHED",
    "OBS_MISSING_REQUIRED_FIELD_DECLARATION",
    "OBS_NONCANONICAL_TYPED_VALUE",
    "OBS_SOURCE_IDENTITY_DECLARATION_MISSING",
    "OBS_SOURCE_FRESHNESS_DECLARATION_MISSING",
    "OBS_SOURCE_STALE",
    "OBS_PROHIBITED_CANDIDATE_DECLARATION_PRESENT",
    "OBS_ACTUAL_FORBIDDEN_EFFECT_DETECTED",
    "OBS_AMBIGUOUS_BOUNDARY_DECLARATION",
    "OBS_CONFLATED_DECLARATION_PRESENT",
    "OBS_UNSUPPORTED_CLAIM_DECLARED_SUPPORTED",
    "OBS_SCHEMA_REQUIREMENT_MISSING",
    "OBS_AUTHORITY_REQUIREMENT_MISSING",
    "OBS_CAPABILITY_REQUIREMENT_MISSING",
    "OBS_SCOPE_REGIME_VIOLATION",
    "OBS_OBJECT_BINDING_MISMATCH",
    "OBS_NON_PROGRESS",
    "OBS_REPEATED_STATE",
    "OBS_NO_RECOGNIZED_CONDITION",
]
CONDITIONS = [
    "CONDITION_TARGET_SATISFIED",
    "CONDITION_REPAIRABLE_DEFECT",
    "CONDITION_UNREPAIRABLE_UNDER_CURRENT_MOVE_SPACE",
    "CONDITION_MISSING_SOURCE",
    "CONDITION_SOURCE_IDENTITY_UNVERIFIED",
    "CONDITION_SOURCE_STALE",
    "CONDITION_MISSING_SCHEMA",
    "CONDITION_MISSING_AUTHORITY",
    "CONDITION_MISSING_CAPABILITY",
    "CONDITION_FORBIDDEN_EFFECT",
    "CONDITION_AMBIGUOUS_BOUNDARY",
    "CONDITION_CONFLATED_FIELD",
    "CONDITION_UNSUPPORTED_CLAIM",
    "CONDITION_SCOPE_REGIME_VIOLATION",
    "CONDITION_OBJECT_BINDING_MISMATCH",
    "CONDITION_NON_PROGRESS",
    "CONDITION_REPEATED_STATE",
    "CONDITION_NO_ADMISSIBLE_MOVE",
    "CONDITION_UNCLASSIFIED",
]
VALIDATION_RESULTS = [
    "VALIDATION_NOT_RUN",
    "VALIDATION_PASS",
    "VALIDATION_FAIL_REQUIRED_SECTION",
    "VALIDATION_FAIL_REQUIRED_FIELD",
    "VALIDATION_FAIL_TYPE",
    "VALIDATION_FAIL_VALUE_CONSTRAINT",
    "VALIDATION_FAIL_CROSS_FIELD",
    "VALIDATION_FAIL_SOURCE_DECLARATION",
    "VALIDATION_FAIL_AUTHORITY_DECLARATION",
    "VALIDATION_FAIL_PROHIBITED_DECLARATION",
    "VALIDATION_FAIL_SCOPE_REGIME_BINDING",
    "VALIDATION_FAIL_OBJECT_BINDING",
    "VALIDATION_FAIL_SCHEMA_UNAVAILABLE",
    "VALIDATION_RESULT_AMBIGUOUS",
]
ADMISSIBILITY_RESULTS = [
    "ADMISSIBILITY_NOT_RUN",
    "ADMISSIBILITY_PASS",
    "ADMISSIBILITY_FAIL_UNSUPPORTED_CLAIM",
    "ADMISSIBILITY_FAIL_SOURCE",
    "ADMISSIBILITY_FAIL_AUTHORITY",
    "ADMISSIBILITY_FAIL_CAPABILITY",
    "ADMISSIBILITY_FAIL_FORBIDDEN_EFFECT",
    "ADMISSIBILITY_FAIL_SCOPE_REGIME",
    "ADMISSIBILITY_RESULT_AMBIGUOUS",
]
CONVERGENCE_RESULTS = [
    "CONVERGENCE_NOT_RUN",
    "CONVERGENCE_CONTINUE_ALLOWED",
    "CONVERGENCE_TARGET_TERMINAL_CONDITION_SATISFIED",
    "CONVERGENCE_STOP_NON_PROGRESS",
    "CONVERGENCE_STOP_REPEATED_STATE",
    "CONVERGENCE_STOP_OSCILLATION",
    "CONVERGENCE_STOP_ATTEMPTED_MOVE_BOUND_EXHAUSTED",
    "CONVERGENCE_STOP_APPLIED_MOVE_BOUND_EXHAUSTED",
    "CONVERGENCE_STOP_DECLARED_RADIUS_BOUND_EXHAUSTED",
    "CONVERGENCE_CRITERION_UNMET",
    "CONVERGENCE_RESULT_AMBIGUOUS",
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
APPLICATION_RESULTS = [
    "MOVE_APPLICABILITY_PASS",
    "MOVE_APPLICABILITY_BLOCKED_OBSERVATION_ABSENT",
    "MOVE_APPLICABILITY_BLOCKED_CONDITION_ABSENT",
    "MOVE_APPLICABILITY_BLOCKED_SCOPE_REGIME_MISMATCH",
    "MOVE_APPLICABILITY_BLOCKED_OBJECT_BINDING_MISMATCH",
    "MOVE_APPLICABILITY_BLOCKED_SOURCE_MISSING",
    "MOVE_APPLICABILITY_BLOCKED_SOURCE_UNVERIFIED",
    "MOVE_APPLICABILITY_BLOCKED_SOURCE_VERSION_MISMATCH",
    "MOVE_APPLICABILITY_BLOCKED_SCHEMA_MISSING",
    "MOVE_APPLICABILITY_BLOCKED_CAPABILITY_MISSING",
    "MOVE_APPLICABILITY_BLOCKED_CANDIDATE_PATH_IMMUTABLE",
    "MOVE_APPLICABILITY_BLOCKED_TARGET_RULE_MISSING",
    "MOVE_APPLICABILITY_BLOCKED_FORBIDDEN_EFFECT_RISK",
    "MOVE_APPLICABILITY_BLOCKED_DELTA_NOT_DETERMINISTIC",
]
RUNTIME_AUTHORIZATION_RESULTS = [
    "MOVE_RUNTIME_AUTHORIZATION_PASS",
    "MOVE_RUNTIME_AUTHORIZATION_BLOCKED_ACTIVE_AUTHORITY_MISSING",
    "MOVE_RUNTIME_AUTHORIZATION_BLOCKED_MOVE_NOT_GRANTED",
    "MOVE_RUNTIME_AUTHORIZATION_BLOCKED_BINDING_MISMATCH",
    "MOVE_RUNTIME_AUTHORIZATION_BLOCKED_SCOPE_EXHAUSTED",
    "MOVE_RUNTIME_AUTHORIZATION_BLOCKED_BUDGET_INSUFFICIENT",
    "MOVE_RUNTIME_AUTHORIZATION_BLOCKED_TERMINAL_STATE",
    "MOVE_RUNTIME_AUTHORIZATION_BLOCKED_HARD_HALT",
    "MOVE_RUNTIME_AUTHORIZATION_BLOCKED_FORBIDDEN_EFFECT_RISK",
    "MOVE_RUNTIME_AUTHORIZATION_BLOCKED_EXPIRED",
]
SEMANTIC_DOMAINS = [
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
FORBIDDEN_WRITE_TARGETS = [
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
    "runtime authority package",
    "runtime budget",
    "move-space binding",
    "target-contract binding",
    "current validation status",
    "current admissibility status",
    "current convergence status",
    "pressure classification",
    "diagnostic state",
]

GATES = {
    "upstream_gate": "VS2_4_SCOPE_AND_OBJECT_MODEL_INPUT_PASS",
    "construction_frame_gate": "VS2_4_CONSTRUCTION_FRAME_EXERCISE_PASS",
    "capability_boundary_gate": "VS2_4_CAPABILITY_BOUNDARY_PASS",
    "source_binding_gate": "VS2_4_SOURCE_AND_VERSION_BINDING_CONTRACT_PASS",
    "finite_catalog_gate": "VS2_4_MOVE_SPACE_FINITE_PASS",
    "vocabulary_partition_gate": "VS2_4_VOCABULARY_PARTITION_PASS",
    "move_contract_gate": "VS2_4_MOVE_CONTRACT_COMPLETENESS_PASS",
    "bounded_operand_gate": "VS2_4_BOUNDED_MOVE_OPERAND_PASS",
    "mutation_boundary_gate": "VS2_4_MOVE_MUTATION_BOUNDARY_PASS",
    "forbidden_effect_gate": "VS2_4_FORBIDDEN_DECLARATION_EFFECT_SEPARATION_PASS",
    "move_separation_gate": "VS2_4_PROHIBITED_DECLARATION_AND_CLAIM_REJECTION_SEPARATION_PASS",
    "applicability_authority_gate": "VS2_4_APPLICABILITY_AUTHORITY_SEPARATION_PASS",
    "authorization_admissibility_gate": "VS2_4_RUNTIME_AUTHORIZATION_AND_CANDIDATE_ADMISSIBILITY_SEPARATION_PASS",
    "no_invention_gate": "VS2_4_NO_INVENTION_CAPABILITY_PASS",
    "c20_gate": "VS2_4_C20_VOCABULARY_BINDING_PASS",
    "hash_graph_gate": "VS2_4_HASH_GRAPH_FREEZE_PASS",
    "prospective_authority_gate": "VS2_4_PROSPECTIVE_AUTHORITY_BOUNDARY_PASS",
    "pending_binding_gate": "VS2_4_PENDING_AUTHORITY_BINDINGS_PASS",
    "successor_manifest_gate": "VS2_4_SUCCESSOR_BINDING_MANIFEST_PASS",
    "active_authority_gate": "VS2_4_ACTIVE_EXECUTION_AUTHORITY_ABSENT_PASS",
    "downstream_pending_gate": "VS2_4_DOWNSTREAM_STEP_COMPONENTS_PENDING_PASS",
    "no_execution_gate": "VS2_4_NO_EXECUTION_OR_FIXTURE_DRIFT_PASS",
}


class StopFailure(RuntimeError):
    def __init__(self, code: str, artifact: str, field: str, expected: Any, observed: Any, invariant: str = "VS2_4_CONSTRUCTION_BOUNDARY") -> None:
        super().__init__(code)
        self.code = code
        self.artifact = artifact
        self.field = field
        self.expected = expected
        self.observed = observed
        self.invariant = invariant


def fail(code: str, artifact: str, field: str, expected: Any, observed: Any, invariant: str = "VS2_4_CONSTRUCTION_BOUNDARY") -> None:
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


def canonical_bytes(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_hash(payload: Any) -> str:
    return sha256_bytes(canonical_bytes(payload))


def status_paths(status: str) -> list[str]:
    paths: list[str] = []
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
        fail("STOP_VS2_4_PREEXISTING_WORKTREE_CHANGES", "repo", "dirty_paths", sorted(ALLOWED_DIRTY), unexpected)
    if protected:
        fail("STOP_VS2_4_SCOPE_AND_OBJECT_MODEL_NOT_PASS", "upstream", "protected_paths", "unchanged", protected)
    if (root / "discussion_packets").exists():
        fail("STOP_VS2_4_DISCUSSION_PACKETS_PRESENT", "repo", "discussion_packets", "absent", "present")


def check_repo(root: Path) -> None:
    require(str(root), ROOT, "STOP_VS2_4_REPOSITORY_ROOT_MISMATCH", "repo", "repository_root")
    require(git(root, ["rev-parse", "--show-toplevel"]), ROOT, "STOP_VS2_4_REPOSITORY_ROOT_MISMATCH", "repo", "git_root")
    require(git(root, ["branch", "--show-current"]), BRANCH, "STOP_VS2_4_BRANCH_MISMATCH", "repo", "branch")
    require(git(root, ["rev-parse", "HEAD"]), HEAD, "STOP_VS2_4_UNEXPECTED_HEAD", "repo", "HEAD")
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=root).returncode != 0
    require_bool(staged, False, "STOP_VS2_4_STAGED_CHANGES_PRESENT", "repo", "staged_changes_present")
    validate_dirty_scope(root)


def verify_committed(root: Path, rel: str, raw_sha: str) -> bytes:
    try:
        committed = git(root, ["show", f"{HEAD}:{rel}"], binary=True)
    except subprocess.CalledProcessError as exc:
        fail("STOP_VS2_4_SCOPE_AND_OBJECT_MODEL_NOT_PASS", rel, "committed_path", "present", exc.stderr)
    current_path = root / rel
    if not current_path.exists():
        fail("STOP_VS2_4_SCOPE_AND_OBJECT_MODEL_NOT_PASS", rel, "worktree_path", "present", "missing")
    current = current_path.read_bytes()
    require(current, committed, "STOP_VS2_4_SCOPE_AND_OBJECT_MODEL_NOT_PASS", rel, "committed_bytes")
    require(sha256_bytes(current), raw_sha, "STOP_VS2_4_SCOPE_AND_OBJECT_MODEL_NOT_PASS", rel, "raw_sha256")
    return current


def load_upstream(root: Path) -> dict[str, dict[str, Any]]:
    data = {}
    for path, raw in EXPECTED_RAW.items():
        content = verify_committed(root, path, raw)
        if path.endswith(".json"):
            data[path] = json.loads(content.decode("utf-8"))
    f0 = data[F0_JSON]
    o1 = data[O1_JSON]
    o2 = data[O2_JSON]
    o3 = data[O3_JSON]
    m0 = data[M0_JSON]
    receipt = data[VS2_3_RECEIPT_JSON]
    bindings = [
        (f0, "contract_binding", "contract_payload", "contract_sha256", F0_JSON),
        (o1, "contract_binding", "contract_payload", "contract_sha256", O1_JSON),
        (o2, "schema_binding", "schema_payload", "schema_sha256", O2_JSON),
        (o3, "target_contract_binding", "target_contract_payload", "target_contract_sha256", O3_JSON),
        (m0, "manifest_binding", "manifest_payload", "manifest_sha256", M0_JSON),
        (receipt, "receipt_binding", "receipt_payload", "receipt_sha256", VS2_3_RECEIPT_JSON),
    ]
    for artifact, binding, payload_key, hash_key, path in bindings:
        require(artifact[binding][hash_key], EXPECTED_CANONICAL[path], "STOP_VS2_4_SCOPE_AND_OBJECT_MODEL_NOT_PASS", path, hash_key)
        require(canonical_hash(artifact[binding][payload_key]), EXPECTED_CANONICAL[path], "STOP_VS2_4_SCOPE_AND_OBJECT_MODEL_NOT_PASS", path, f"{payload_key}_hash")
    require(receipt.get("logical_terminal_transition"), "ADVANCE(VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PENDING)", "STOP_VS2_4_SCOPE_AND_OBJECT_MODEL_NOT_PASS", VS2_3_RECEIPT_JSON, "logical_terminal_transition")
    require(receipt.get("gates", {}).get("receipt_gate"), "VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PASS", "STOP_VS2_4_SCOPE_AND_OBJECT_MODEL_NOT_PASS", VS2_3_RECEIPT_JSON, "receipt_gate")
    counts = receipt["object_model_counts"]
    state = receipt["post_state"]
    for key, want in {
        "execution_domain_object_role_count": 3,
        "additional_mutable_execution_domain_object_count": 0,
        "terminal_outcome_count": 17,
    }.items():
        require(counts.get(key), want, "STOP_VS2_4_SCOPE_AND_OBJECT_MODEL_NOT_PASS", VS2_3_RECEIPT_JSON, key)
    for key, want in {
        "move_space_constructed": False,
        "selector_constructed": False,
        "applicator_constructed": False,
        "validation_execution_logic_constructed": False,
        "admissibility_execution_logic_constructed": False,
        "convergence_criterion_constructed": False,
        "source_snapshot_frozen": False,
        "runtime_instance_created": False,
        "candidate_instance_created": False,
        "fixture_instance_created": False,
        "execution_authorized": False,
        "execution_performed": False,
        "sweep_authorized": False,
        "sweep_executed": False,
        "runner_created": False,
        "vs2_4_may_begin": True,
    }.items():
        require(state.get(key), want, "STOP_VS2_4_SCOPE_AND_OBJECT_MODEL_NOT_PASS", VS2_3_RECEIPT_JSON, key)
    auth = receipt["construction_authority"]
    for key, want in {
        "bounded_construction_grant_consumed": True,
        "bounded_construction_consumption_count_after": 1,
        "bounded_construction_frame_open": True,
        "bounded_construction_grant_exhausted": False,
        "same_bounded_construction_grant_may_be_consumed_again": False,
    }.items():
        require(auth.get(key), want, "STOP_VS2_4_CONSTRUCTION_FRAME_NOT_OPEN", VS2_3_RECEIPT_JSON, key)
    if auth.get("bounded_construction_consumption_count_after") != 1:
        fail("STOP_VS2_4_CONSTRUCTION_GRANT_RECONSUMPTION_ATTEMPT", VS2_3_RECEIPT_JSON, "bounded_construction_consumption_count_after", 1, auth.get("bounded_construction_consumption_count_after"))
    required_m0 = {
        "move_space_reference": "FINITE_MOVE_SPACE_CONTRACT",
        "execution_authority_shape_reference": "BOUNDED_FUTURE_EXECUTION_AUTHORITY_SHAPE",
        "source_and_version_binding_contract_reference": "SOURCE_AND_VERSION_BINDING_CONTRACT",
    }
    by_id = {row["reference_id"]: row for row in m0["pending_downstream_bindings"]}
    for ref_id, kind in required_m0.items():
        row = by_id.get(ref_id)
        if row is None:
            fail("STOP_VS2_4_M0_REWRITTEN_OR_SUCCESSOR_MANIFEST_MISSING", M0_JSON, ref_id, "present", "missing")
        require(row["binding_status"], "PENDING", "STOP_VS2_4_M0_REWRITTEN_OR_SUCCESSOR_MANIFEST_MISSING", M0_JSON, f"{ref_id}.binding_status")
        require(row["required_by_unit"], UNIT_ID, "STOP_VS2_4_M0_REWRITTEN_OR_SUCCESSOR_MANIFEST_MISSING", M0_JSON, f"{ref_id}.required_by_unit")
        require(row["expected_artifact_kind"], kind, "STOP_VS2_4_M0_REWRITTEN_OR_SUCCESSOR_MANIFEST_MISSING", M0_JSON, f"{ref_id}.expected_artifact_kind")
        for field in ["artifact_id", "artifact_kind", "artifact_version", "declared_path", "content_sha256", "hash_algorithm", "canonicalization_rule"]:
            require(row[field], None, "STOP_VS2_4_FAKE_OR_PREBOUND_AUTHORITY_REFERENCE", M0_JSON, f"{ref_id}.{field}")
    return data


def source_basis(sections: list[str], basis: str, reason: str) -> list[dict[str, str]]:
    return [
        {
            "section": section,
            "basis_class": basis,
            "basis_reason": reason,
            "source_authority": "committed_vs2_object_model_or_deterministic_representation",
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


def bind(payload: dict[str, Any], binding_name: str, payload_key: str, hash_key: str) -> dict[str, Any]:
    return {
        **payload,
        binding_name: {
            "canonicalization": CANON,
            payload_key: payload,
            hash_key: canonical_hash(payload),
        },
    }


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, artifact: dict[str, Any], digest: str, status_key: str, summary_lines: list[str]) -> None:
    refs = []
    for key, value in artifact.items():
        if key.endswith("_reference") and isinstance(value, dict):
            refs.append(f"- `{key}`: `{value['binding_status']}` `{value.get('artifact_id')}`")
    source_basis_lines = []
    for basis in artifact.get("source_basis", []):
        source_basis_lines.append(
            f"- `source_basis`: `{basis['section']}` `{basis['basis_class']}`"
        )
    lines = [
        f"# {artifact['artifact_id']}",
        "",
        f"- Artifact kind: `{artifact['artifact_kind']}`",
        f"- Version: `{artifact.get('contract_version') or artifact.get('partition_version') or artifact.get('matrix_version') or artifact.get('move_space_version') or artifact.get('envelope_version') or artifact.get('manifest_version')}`",
        f"- Status: `{artifact.get(status_key)}`",
        f"- Canonicalization: `{CANON}`",
        f"- Canonical SHA-256: `{digest}`",
        "",
        "## Bound References",
        "",
        *(refs or ["- No direct top-level bound references."]),
        "",
        "## Source Basis",
        "",
        *(source_basis_lines or ["- `source_basis`: `not_applicable` `DETERMINISTIC_REPRESENTATION_REQUIRED`"]),
        "",
        "## Summary",
        "",
        *summary_lines,
        "",
        "## Nonclaims",
        "",
        "- This artifact does not authorize execution.",
        "- This artifact does not create runtime, candidate, fixture, sweep, or runner instances.",
        "- This Markdown file is a deterministic projection of the JSON artifact.",
    ]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def capability_decision(missing_object: str, blocked_field: str) -> dict[str, Any]:
    return {
        "missing_object": missing_object,
        "source_basis_inspected": True,
        "representable": True,
        "inside_current_construction_capability": True,
        "authorized_by_open_bounded_construction_frame": True,
        "derivable_from_committed_sources": True,
        "non_expansive": True,
        "constructible_without_new_source_schema_target_authority_capability_or_move_identity": True,
        "blocked_move_or_field": blocked_field,
        "capability_stop_if_false": "STOP_VS2_4_CAPABILITY_LAYER_REQUIRED",
        "self_repair_performed": False,
    }


def make_refs(up: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    m0 = up[M0_JSON]
    return {
        "profile": m0["kernel_profile_reference"],
        "target_freeze": m0["semantic_target_freeze_reference"],
        "f0": m0["scope_regime_contract_reference"],
        "o1": m0["runtime_state_contract_reference"],
        "o2": m0["candidate_contract_schema_reference"],
        "o3": m0["target_contract_reference"],
        "m0": bound_ref("object_model_manifest_reference", "UPSTREAM_OBJECT_MODEL_MANIFEST", UNIT_ID, m0["artifact_id"], m0["artifact_kind"], m0["manifest_version"], M0_JSON, EXPECTED_CANONICAL[M0_JSON], "Committed M0 remains immutable and is succeeded by M1."),
    }


def construction_authority(up: dict[str, dict[str, Any]]) -> dict[str, Any]:
    previous = up[VS2_3_RECEIPT_JSON]["construction_authority"]
    return {
        "bounded_construction_grant_id": "VS2_BOUNDED_CONSTRUCTION_AUTHORITY",
        "bounded_construction_grant_prior_consumed": True,
        "bounded_construction_consumption_count_before": 1,
        "bounded_construction_consumption_count_after": 1,
        "additional_bounded_construction_grant_consumption_by_vs2_4": False,
        "bounded_construction_frame_exercised_by_vs2_4": True,
        "bounded_construction_frame": "VS2.3_TO_VS2.5_BOUND_TARGET_CONSTRUCTION_SEQUENCE",
        "bounded_construction_local_exercise_scope": "FINITE_MOVE_SPACE_SOURCE_BINDING_AND_PROSPECTIVE_AUTHORITY_ONLY",
        "bounded_construction_frame_open_after_vs2_4": True,
        "remaining_frame_units": ["VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION"],
        "source_vs2_3_consumption_frame": previous["consumption_frame"],
        "same_bounded_construction_grant_may_be_consumed_again": False,
        "unconsumed_effective_grant_count": 3,
        "unconsumed_effective_grant_ids": [
            "VS2_FIXTURE_CONSTRUCTION_AUTHORITY",
            "VS2_FIRST_RUN_READINESS_GATE_CONSTRUCTION_AUTHORITY",
            "VS2_CONSTRUCTION_PACKAGE_VERIFICATION_AUTHORITY",
        ],
        "fixture_construction_authority_consumed_by_vs2_4": False,
        "readiness_gate_construction_authority_consumed_by_vs2_4": False,
        "construction_package_verification_authority_consumed_by_vs2_4": False,
        "execution_authority_consumed_by_vs2_4": False,
    }


def make_s0(refs: dict[str, dict[str, Any]], auth: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "matrixlabs_phase_vs2_source_and_version_binding_contract_v0",
        "artifact_id": "phase_vs2_source_and_version_binding_contract_v0",
        "artifact_kind": "STATIC_SOURCE_IDENTITY_VERSION_AND_FRESHNESS_BINDING_CONTRACT",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "contract_id": "first_sweep_kernel_source_and_version_binding_contract_v0",
        "contract_version": "v0",
        "profile_reference": refs["profile"],
        "scope_regime_reference": refs["f0"],
        "object_model_manifest_reference": refs["m0"],
        "admitted_source_classes": [
            "COMMITTED_REPOSITORY_ARTIFACT",
            "COMMITTED_MATRIXLABS_SOURCE_DOCUMENT",
            "COMMITTED_CLOSED_AUTHORITY_RECORD",
            "FUTURE_EXACT_SOURCE_SNAPSHOT_MEMBER",
        ],
        "source_record_schema": {
            "required_fields": [
                "source_record_id",
                "source_role",
                "source_class",
                "source_artifact_id",
                "source_artifact_kind",
                "source_version",
                "declared_path_or_locator",
                "content_sha256",
                "hash_algorithm",
                "canonicalization_rule",
                "freshness_rule_id",
                "freshness_witness_reference",
                "snapshot_membership_reference",
                "binding_status",
            ],
            "binding_status_values": ["BOUND", "PENDING", "ABSENT_BY_POLICY", "NOT_APPLICABLE"],
            "future_records_must_bind_exact_snapshot_membership": True,
        },
        "source_identity_rule": "Future source records must declare stable source identity and artifact kind before use.",
        "source_version_rule": "Future source records must declare version or commit identity before use.",
        "source_hash_rule": "Future source records must bind canonical SHA-256 when JSON-canonicalizable, otherwise raw SHA-256 with an explicit rule.",
        "source_role_rule": "Future source records must declare a source role admitted by F0 and required by O3.",
        "freshness_rule": "Freshness is proven only by declared freshness rule and witness; latest-file and mtime are forbidden.",
        "freshness_witness_rule": "Freshness witnesses remain pending until the exact source snapshot is frozen.",
        "snapshot_membership_rule": "Exact source snapshot membership is pending for VS2.6 and is not frozen by S0.",
        "source_replacement_rule": "Silent source replacement and version substitution are forbidden.",
        "source_conflict_rule": "Conflicting source identity, version, hash, or role stops future controlled steps.",
        "forbidden_resolution_methods": [
            "latest-file resolution",
            "mtime authority",
            "directory-position authority",
            "filename-similarity authority",
            "ambient repository sourcing",
            "chat-memory sourcing",
            "automatic source acquisition",
            "silent source replacement",
            "silent version substitution",
            "silent freshness override",
            "unbound external source use",
        ],
        "pending_exact_source_snapshot_reference": nonbound_ref("exact_source_snapshot_reference", "FUTURE_EXACT_SOURCE_SNAPSHOT", "PENDING", "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS", "EXACT_SOURCE_SNAPSHOT", "S0 is frozen, but the exact source snapshot is deferred to VS2.6."),
        "construction_authority_provenance": auth,
        "source_basis": source_basis([
            "admitted_source_classes",
            "source_record_schema",
            "source_identity_rule",
            "source_version_rule",
            "source_hash_rule",
            "source_role_rule",
            "freshness_rule",
            "pending_exact_source_snapshot_reference",
        ], "UPSTREAM_F0_DERIVED", "S0 freezes source identity/version/freshness posture from F0/M0/O3 without creating a snapshot."),
        "contract_status": "FROZEN_EXACT_SOURCE_SNAPSHOT_PENDING",
        "exact_source_snapshot_frozen": False,
        "core_boundary": "S0_FROZEN_DOES_NOT_FREEZE_EXACT_SOURCE_SNAPSHOT",
    }
    return bind(payload, "contract_binding", "contract_payload", "contract_sha256")


def make_vocabulary_entries() -> dict[str, list[dict[str, Any]]]:
    def entries(ids: list[str], partition: str, producer: str, consumer: str, mutates: bool) -> list[dict[str, Any]]:
        return [
            {
                "identifier": identifier,
                "partition": partition,
                "definition": f"{identifier} is a {partition} vocabulary member for the first-sweep kernel.",
                "producer_role": producer,
                "consumer_role": consumer,
                "may_mutate_o2": mutates,
            }
            for identifier in ids
        ]
    return {
        "V1_TRANSFORMATION_MOVES": entries(MOVE_IDS, "V1_TRANSFORMATION_MOVES", "MOVE_SPACE_DEFINITION", "FUTURE_SELECTOR_AND_APPLICATOR", True),
        "V2_OBSERVATIONS": entries(OBSERVATIONS, "V2_OBSERVATIONS", "FUTURE_INSPECTION", "FUTURE_CLASSIFIER", False),
        "V3_CONDITION_CLASSIFICATIONS": entries(CONDITIONS, "V3_CONDITION_CLASSIFICATIONS", "FUTURE_CLASSIFIER", "FUTURE_SELECTOR", False),
        "V4_VALIDATION_RESULTS": entries(VALIDATION_RESULTS, "V4_VALIDATION_RESULTS", "FUTURE_VALIDATOR", "FUTURE_TERMINALIZER", False),
        "V5_CANDIDATE_ADMISSIBILITY_RESULTS": entries(ADMISSIBILITY_RESULTS, "V5_CANDIDATE_ADMISSIBILITY_RESULTS", "FUTURE_ADMISSIBILITY_EVALUATOR", "FUTURE_TERMINALIZER", False),
        "V6_CONVERGENCE_RESULTS": entries(CONVERGENCE_RESULTS, "V6_CONVERGENCE_RESULTS", "FUTURE_CONVERGENCE_EVALUATOR", "FUTURE_TERMINALIZER", False),
        "V7_TERMINAL_OUTCOMES": entries(TERMINAL_OUTCOMES, "V7_TERMINAL_OUTCOMES", "FUTURE_TERMINALIZER", "FUTURE_RECEIPT_LAYER", False),
    }


def make_v0(refs: dict[str, dict[str, Any]], auth: dict[str, Any]) -> dict[str, Any]:
    partitions = make_vocabulary_entries()
    identifiers = [row["identifier"] for rows in partitions.values() for row in rows]
    payload = {
        "schema_version": "matrixlabs_phase_vs2_move_vocabulary_partition_v0",
        "artifact_id": "phase_vs2_move_vocabulary_partition_v0",
        "artifact_kind": "STATIC_DISJOINT_VOCABULARY_PARTITION",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "partition_id": "first_sweep_kernel_move_vocabulary_partition_v0",
        "partition_version": "v0",
        "partition_status": "FROZEN",
        "partition_count": 7,
        "partitions": partitions,
        "global_identifier_requirements": {
            "every_identifier_unique": len(identifiers) == len(set(identifiers)),
            "every_identifier_appears_once": True,
            "only_v1_may_mutate_o2": True,
            "v2_through_v7_may_mutate_o2": False,
            "stop_budget_exhausted_present": "STOP_BUDGET_EXHAUSTED" in identifiers,
        },
        "move_catalog": {
            "ordered_move_ids": MOVE_IDS,
            "move_count": 8,
            "move_ids_unique": len(MOVE_IDS) == len(set(MOVE_IDS)),
            "dynamic_move_creation_allowed": False,
            "catalog_closed": True,
            "selector_priority_defined": False,
            "identity_order_is_selector_priority": False,
        },
        "convergence_result_mapping": {
            "CONVERGENCE_STOP_ATTEMPTED_MOVE_BOUND_EXHAUSTED": {"terminal_outcome": "STOP_RADIUS_EXHAUSTED", "subordinate_detail": "ATTEMPTED_MOVE_BUDGET_EXHAUSTED"},
            "CONVERGENCE_STOP_APPLIED_MOVE_BOUND_EXHAUSTED": {"terminal_outcome": "STOP_RADIUS_EXHAUSTED", "subordinate_detail": "APPLIED_MOVE_BUDGET_EXHAUSTED"},
            "CONVERGENCE_STOP_DECLARED_RADIUS_BOUND_EXHAUSTED": {"terminal_outcome": "STOP_RADIUS_EXHAUSTED", "subordinate_detail": "DECLARED_RADIUS_BOUND_EXHAUSTED"},
        },
        "auxiliary_move_evaluation_namespaces": {
            "not_v1_through_v7_entries": ["MOVE_APPLICABILITY_*", "MOVE_RUNTIME_AUTHORIZATION_*", "MOVE_APPLICATION_*"],
            "structural_applicability_results": APPLICATION_RESULTS,
            "runtime_authorization_results": RUNTIME_AUTHORIZATION_RESULTS,
            "may_mutate_o2": False,
            "globally_collision_free": True,
        },
        "scope_regime_reference": refs["f0"],
        "candidate_schema_reference": refs["o2"],
        "construction_authority_provenance": auth,
        "source_basis": source_basis(["partitions", "move_catalog", "terminal_outcomes", "auxiliary_move_evaluation_namespaces"], "DETERMINISTIC_REPRESENTATION_REQUIRED", "V0 freezes the finite vocabulary required by the target-bound move space."),
    }
    return bind(payload, "partition_binding", "partition_payload", "partition_sha256")


def common_operand(move_id: str, destination_paths: list[str]) -> dict[str, Any]:
    return {
        "move_id": move_id,
        "target_rule_reference": "O3_DECLARED_TARGET_RULE_REQUIRED",
        "candidate_source_path": "O2_SEMANTIC_CONTENT_PATH_REQUIRED",
        "candidate_destination_paths": destination_paths,
        "source_record_references": "S0_COMPLIANT_SOURCE_RECORDS_ONLY",
        "mapping_rule_reference": "O3_DETERMINISTIC_MAPPING_RULE_REQUIRED",
        "old_value_predicates": "REQUIRED_AND_EXACT",
        "new_value_predicates": "REQUIRED_AND_EXACT",
        "atomic_bundle_identity": "REQUIRED_FOR_EACH_FUTURE_MOVE_ATTEMPT",
        "free_form_operand_allowed": False,
        "resolution_sources": ["O2 candidate content", "O3 frozen target rules", "S0-compliant source records", "F0 boundaries"],
        "cannot_introduce": ["new candidate path", "new target rule", "new source record", "new schema", "new capability", "new authority class", "new move identity"],
    }


def delta(changed: int, added: int, removed: int, replaced: int) -> dict[str, Any]:
    return {
        "maximum_candidate_paths_changed": changed,
        "maximum_semantic_declarations_added": added,
        "maximum_semantic_declarations_removed": removed,
        "maximum_semantic_declarations_replaced": replaced,
        "required_provenance_records": True,
        "unrelated_path_mutation_forbidden": True,
        "required_old_value_predicates": True,
        "required_new_value_predicates": True,
        "atomic_bundle_identity": True,
        "delta_is_explicit_bounded_deterministic_path_scoped_provenance_preserving_candidate_only": True,
        "reconstructable_from_future_move_receipt": True,
    }


def move_specs() -> dict[str, dict[str, Any]]:
    return {
        "M01_ADD_AUTHORIZED_REQUIRED_FIELD": {
            "name": "Add Authorized Required Field",
            "required_observations": ["OBS_MISSING_REQUIRED_FIELD_DECLARATION"],
            "required_condition_classes": ["CONDITION_REPAIRABLE_DEFECT"],
            "write_templates": [
                "typed_field_declarations.declared_required_fields",
                "typed_field_declarations.declared_field_type_constraints",
                "typed_field_declarations.declared_field_value_constraints",
                "typed_field_declarations.declared_cross_field_constraints",
            ],
            "requirements": ["O3 declares every field-bundle member", "O3 declares the type and constraints", "operand resolves deterministically", "all destination paths are mutable", "no source, schema, capability, or authority invention"],
            "delta": delta(4, 4, 0, 0),
            "blocked": ["MOVE_APPLICATION_BLOCKED_MISSING_SOURCE", "MOVE_APPLICATION_BLOCKED_MISSING_SCHEMA", "MOVE_APPLICATION_BLOCKED_MISSING_AUTHORITY", "MOVE_APPLICATION_BLOCKED_MISSING_CAPABILITY", "MOVE_APPLICATION_BLOCKED_FIELD_NOT_MUTABLE", "MOVE_APPLICATION_BLOCKED_TARGET_RULE_MISSING", "MOVE_APPLICATION_BLOCKED_DECLARATION_RULE_AMBIGUOUS"],
        },
        "M02_NORMALIZE_TYPED_VALUE": {
            "name": "Normalize Typed Value",
            "required_observations": ["OBS_NONCANONICAL_TYPED_VALUE"],
            "required_condition_classes": ["CONDITION_REPAIRABLE_DEFECT"],
            "write_templates": ["typed_field_declarations.declared_field_value_constraints"],
            "requirements": ["candidate value exists", "O3 supplies exact canonicalization mapping", "semantic meaning is preserved", "one source path and one destination path resolve", "destination is mutable"],
            "delta": delta(1, 0, 0, 1),
            "blocked": ["MOVE_APPLICATION_BLOCKED_FIELD_NOT_MUTABLE", "MOVE_APPLICATION_BLOCKED_TARGET_RULE_MISSING", "MOVE_APPLICATION_BLOCKED_DELTA_NOT_DETERMINISTIC"],
            "forbidden_extra": ["semantic reinterpretation", "unsupported-content laundering"],
        },
        "M03_BIND_DECLARED_SOURCE_IDENTITY": {
            "name": "Bind Declared Source Identity",
            "required_observations": ["OBS_SOURCE_IDENTITY_DECLARATION_MISSING"],
            "required_condition_classes": ["CONDITION_REPAIRABLE_DEFECT"],
            "write_templates": ["source_binding_declarations.declared_required_source_bindings", "source_binding_declarations.declared_source_identity_rules", "source_binding_declarations.declared_source_role_rules"],
            "requirements": ["source record is already in the admitted future snapshot", "source record conforms to S0", "source identity and version verify", "F0 admits source class", "O3 permits source role", "no source acquisition or replacement occurs"],
            "delta": delta(3, 3, 0, 0),
            "blocked": ["MOVE_APPLICATION_BLOCKED_MISSING_SOURCE", "MOVE_APPLICATION_BLOCKED_SOURCE_UNVERIFIED", "MOVE_APPLICATION_BLOCKED_SOURCE_VERSION_MISMATCH"],
        },
        "M04_BIND_DECLARED_SOURCE_FRESHNESS": {
            "name": "Bind Declared Source Freshness",
            "required_observations": ["OBS_SOURCE_FRESHNESS_DECLARATION_MISSING"],
            "required_condition_classes": ["CONDITION_REPAIRABLE_DEFECT"],
            "write_templates": ["source_binding_declarations.declared_source_freshness_rules", "source_binding_declarations.declared_required_source_bindings"],
            "requirements": ["source identity already bound or produced by prior candidate effect", "freshness witness already exists in admitted snapshot", "freshness rule exact", "no source refresh, fetch, timestamp invention, or mtime authority"],
            "delta": delta(2, 2, 0, 0),
            "blocked": ["MOVE_APPLICATION_BLOCKED_MISSING_SOURCE", "MOVE_APPLICATION_BLOCKED_SOURCE_UNVERIFIED", "MOVE_APPLICATION_BLOCKED_SOURCE_VERSION_MISMATCH"],
            "dependency_metadata": {"requires_prior_candidate_effect": "M03_BIND_DECLARED_SOURCE_IDENTITY", "only_when_source_identity_not_already_bound": True},
        },
        "M05_REMOVE_PROHIBITED_CANDIDATE_DECLARATION": {
            "name": "Remove Prohibited Candidate Declaration",
            "required_observations": ["OBS_PROHIBITED_CANDIDATE_DECLARATION_PRESENT"],
            "required_condition_classes": ["CONDITION_REPAIRABLE_DEFECT"],
            "write_templates": ["authority_declarations", "runtime_boundary_declarations", "halt_and_terminal_declarations", "receipt_declarations", "source_binding_declarations", "typed_field_declarations"],
            "requirements": ["O3 identifies exact declaration", "O3 marks it repairable", "removal preserves required evidence", "removal preserves authority restrictions", "no replacement invention"],
            "delta": delta(1, 0, 1, 0),
            "blocked": ["MOVE_APPLICATION_BLOCKED_FIELD_NOT_MUTABLE", "MOVE_APPLICATION_BLOCKED_FORBIDDEN_EFFECT_RISK"],
            "excluded_domains": ["claim_declarations"],
            "actual_forbidden_effect_terminal_outcome": "STOP_FORBIDDEN_EFFECT_DETECTED",
        },
        "M06_TIGHTEN_AMBIGUOUS_BOUNDARY": {
            "name": "Tighten Ambiguous Boundary",
            "required_observations": ["OBS_AMBIGUOUS_BOUNDARY_DECLARATION"],
            "required_condition_classes": ["CONDITION_AMBIGUOUS_BOUNDARY"],
            "write_templates": ["authority_declarations", "runtime_boundary_declarations", "halt_and_terminal_declarations", "receipt_declarations", "source_binding_declarations", "claim_declarations"],
            "requirements": ["source token exactly matches finite mapping key", "O3 declares destination token", "mapping deterministic", "mapped value does not expand authority", "destination mutable"],
            "delta": delta(1, 0, 0, 1),
            "blocked": ["MOVE_APPLICATION_BLOCKED_DECLARATION_RULE_AMBIGUOUS", "MOVE_APPLICATION_BLOCKED_FIELD_NOT_MUTABLE"],
        },
        "M07_SPLIT_CONFLATED_DECLARATION": {
            "name": "Split Conflated Declaration",
            "required_observations": ["OBS_CONFLATED_DECLARATION_PRESENT"],
            "required_condition_classes": ["CONDITION_CONFLATED_FIELD"],
            "write_templates": ["typed_field_declarations.declared_cross_field_constraints", "source_binding_declarations.declared_required_source_bindings", "authority_declarations", "claim_declarations", "receipt_declarations"],
            "requirements": ["O3 declares every destination field", "candidate contains exact recognized source form", "O3 provides finite deterministic split map", "outputs require no inferred semantics", "all destinations mutable", "provenance preserved per output"],
            "delta": delta(5, 4, 1, 0),
            "blocked": ["MOVE_APPLICATION_BLOCKED_DELTA_NOT_DETERMINISTIC", "MOVE_APPLICATION_BLOCKED_TARGET_RULE_MISSING"],
            "unbounded_output_count_permitted": False,
        },
        "M08_REJECT_UNSUPPORTED_CLAIM": {
            "name": "Reject Unsupported Claim",
            "required_observations": ["OBS_UNSUPPORTED_CLAIM_DECLARED_SUPPORTED"],
            "required_condition_classes": ["CONDITION_UNSUPPORTED_CLAIM"],
            "write_templates": ["claim_declarations.declared_supported_claims", "claim_declarations.declared_unsupported_claims", "claim_declarations.declared_explicit_nonclaims"],
            "requirements": ["positive claim exists", "required evidence or authority absent", "O3 classifies it as unsupported", "O3 declares exact disposition", "claim paths mutable"],
            "delta": delta(3, 1, 1, 0),
            "blocked": ["MOVE_APPLICATION_BLOCKED_MISSING_SOURCE", "MOVE_APPLICATION_BLOCKED_MISSING_AUTHORITY", "MOVE_APPLICATION_BLOCKED_TARGET_RULE_MISSING"],
            "allowed_disposition_vocabulary": ["MOVE_TO_UNSUPPORTED_CLAIMS", "MOVE_TO_EXPLICIT_NONCLAIMS", "REMOVE_WITH_REJECTION_RECORD"],
            "forbidden_extra": ["replacement positive claims", "evidence invention", "silent weakening", "deletion of the rejection record"],
        },
    }


def make_move_contracts(refs: dict[str, dict[str, Any]], s0_ref: dict[str, Any]) -> list[dict[str, Any]]:
    specs = move_specs()
    moves = []
    for move_id in MOVE_IDS:
        spec = specs[move_id]
        payload = {
            "move_id": move_id,
            "move_version": "v0",
            "move_name": spec["name"],
            "move_class": "TRANSFORMATION_MOVE",
            "move_status": "FROZEN_NOT_ACTIVE",
            "program_target_family": "BOUNDED_CONTRACT_CONVERGENCE",
            "semantic_target_id": "TYPED_STATE_CONTRACT_CONVERGENCE_V0",
            "scope_regime_reference": refs["f0"],
            "runtime_state_contract_reference": refs["o1"],
            "candidate_schema_reference": refs["o2"],
            "target_contract_reference": refs["o3"],
            "object_model_manifest_reference": refs["m0"],
            "source_and_version_binding_contract_reference": s0_ref,
            "required_observations": spec["required_observations"],
            "required_condition_classes": spec["required_condition_classes"],
            "read_execution_object_roles": ["RUNTIME_CONTROL_STATE", "CANDIDATE_TYPED_STATE_CONTRACT", "FROZEN_TARGET_CONTRACT"],
            "read_static_surfaces": ["F0", "O1_CONTRACT", "O2_SCHEMA", "O3_TARGET", "M0", "S0", "MS0"],
            "read_support_surfaces": ["FUTURE_EXACT_SOURCE_SNAPSHOT", "FUTURE_ACTIVE_AUTHORITY_PACKAGE"],
            "candidate_write_path_templates": spec["write_templates"],
            "operand_contract": common_operand(move_id, spec["write_templates"]),
            "structural_applicability_preconditions": [
                "move exists in MS0",
                "required observations exist",
                "required conditions exist",
                "F0/O1/O2/O3/M0/S0 bindings match",
                "operand resolves only to target-declared paths and rules",
                "required source records exist in admitted snapshot",
                "destination paths are O2-mutable",
                "delta deterministic",
                "delta remains in F0",
                "no forbidden-object mutation required",
            ],
            "source_requirements": ["S0_COMPLIANT_SOURCE_RECORDS_ONLY", "NO_SOURCE_ACQUISITION", "NO_SOURCE_REFRESH"],
            "target_rule_requirements": spec["requirements"],
            "scope_regime_requirements": ["FIRST_SWEEP_KERNEL_SCOPE_V0", "TYPED_STATE_CONTRACT_CONVERGENCE_REGIME_V0"],
            "capability_requirements": [{"capability_id": "NONE_REQUIRED", "reason": "Move is representable under committed F0/O2/O3 and the open bounded construction frame."}],
            "prospective_authority_requirements": ["FUTURE_CONTROLLED_STEP_AUTHORITY_ENVELOPE_REQUIRED_NOT_ACTIVE"],
            "runtime_authorization_requirements": [
                "structural applicability passes",
                "active controlled-step authority exists",
                "move ID granted",
                "remaining budget covers cost",
                "runtime state non-terminal",
                "no hard halt active",
            ],
            "budget_cost": 1,
            "delta_contract": spec["delta"],
            "expected_candidate_postcondition": "O2 successor semantic content differs only by declared bounded delta.",
            "validation_obligations": ["future validation must run after application", "validation result vocabulary is V4"],
            "candidate_admissibility_obligations": ["future admissibility evaluation must run after validation", "candidate admissibility result vocabulary is V5"],
            "convergence_obligations": ["future convergence evaluation remains unconstructed in VS2.4", "convergence result vocabulary is V6"],
            "receipt_obligations": ["future move attempt receipt required", "future terminal receipt required when terminalized"],
            "forbidden_effects": [
                "mutate F0",
                "mutate O1 contract",
                "mutate O1 directly",
                "mutate O3",
                "mutate M0",
                "mutate S0",
                "mutate V0",
                "mutate A0",
                "mutate MS0",
                "mutate P0",
                "mutate M1",
                "grant authority",
                "acquire source",
                "write evaluator state",
            ],
            "blocked_result_codes": spec["blocked"],
            "possible_terminal_outcomes": TERMINAL_OUTCOMES,
            "dependency_metadata": spec.get("dependency_metadata", {}),
            "definition_authority_status": "CONSTRUCTED_UNDER_OPEN_BOUNDED_CONSTRUCTION_FRAME",
            "runtime_authority_status": "PROSPECTIVE_AUTHORITY_REQUIRED_NOT_ACTIVE",
            "reuse_status": "TARGET_BOUND_NON_REUSABLE",
            "candidate_write_law": {
                "only_o2_semantic_content_may_be_changed_by_future_applied_move": True,
                "forbidden_write_targets": FORBIDDEN_WRITE_TARGETS,
                "candidate_version_predecessor_and_hash_are_successor_envelope_metadata": True,
            },
            "capability_boundary_decision": capability_decision("move_contract", move_id),
            "source_basis": source_basis([
                "required_observations",
                "required_condition_classes",
                "candidate_write_path_templates",
                "operand_contract",
                "delta_contract",
                "forbidden_effects",
            ], "UPSTREAM_O3_DERIVED", f"{move_id} is a finite target-bound representation derived from O2 mutable domains and O3 target requirements."),
        }
        for key in ["excluded_domains", "actual_forbidden_effect_terminal_outcome", "allowed_disposition_vocabulary", "forbidden_extra", "unbounded_output_count_permitted"]:
            if key in spec:
                payload[key] = spec[key]
        moves.append({"move_id": move_id, "move_contract_payload": payload, "move_contract_sha256": canonical_hash(payload)})
    return moves


def prospective_p0_identity() -> dict[str, str]:
    return {
        "artifact_id": "phase_vs2_prospective_controlled_step_authority_envelope_v0",
        "artifact_kind": "STATIC_PROSPECTIVE_AUTHORITY_ENVELOPE",
        "artifact_version": "v0",
        "envelope_id": "FIRST_SWEEP_KERNEL_PROSPECTIVE_CONTROLLED_STEP_AUTHORITY_ENVELOPE_V0",
        "envelope_status": "FROZEN_MAXIMUM_NOT_ACTIVE",
        "binding_note": "MS0 and A0 bind P0 identity/version only; P0 hash is unavailable until P0 is built.",
    }


def local_ref(artifact: dict[str, Any], binding: str, payload_hash_key: str, path: str, role: str) -> dict[str, Any]:
    return bound_ref(f"{artifact['artifact_id']}_reference", role, UNIT_ID, artifact["artifact_id"], artifact["artifact_kind"], "v0", path, artifact[binding][payload_hash_key], f"VS2.4-built {artifact['artifact_id']} canonical binding.")


def make_a0(refs: dict[str, dict[str, Any]], s0_ref: dict[str, Any], moves: list[dict[str, Any]], auth: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for move in moves:
        rows.append({
            "move_id": move["move_id"],
            "move_contract_sha256": move["move_contract_sha256"],
            "definition_authority_basis": "CONSTRUCTED_UNDER_OPEN_BOUNDED_CONSTRUCTION_FRAME",
            "structural_applicability_requires_active_authority": False,
            "runtime_enumeration_authority_requirement": "FUTURE_CONTROLLED_STEP_ENUMERATION_AUTHORITY_REQUIRED",
            "runtime_selection_authority_requirement": "FUTURE_ONE_MOVE_SELECTION_AUTHORITY_REQUIRED",
            "runtime_application_authority_requirement": "FUTURE_ONE_EXECUTION_PACKAGE_MOVE_APPLICATION_AUTHORITY_REQUIRED",
            "candidate_successor_authority_requirement": "FUTURE_ONE_CANDIDATE_SUCCESSOR_AUTHORITY_REQUIRED",
            "runtime_successor_authority_requirement": "FUTURE_ONE_RUNTIME_SUCCESSOR_AUTHORITY_REQUIRED",
            "receipt_authority_requirement": "FUTURE_MOVE_ATTEMPT_RECEIPT_AUTHORITY_REQUIRED",
            "authority_status": "FROZEN_NOT_ACTIVE",
            "reuse_status": "TARGET_BOUND_NON_REUSABLE",
            "target_scope": "TYPED_STATE_CONTRACT_CONVERGENCE_V0_ONLY",
        })
    payload = {
        "schema_version": "matrixlabs_phase_vs2_move_authority_matrix_v0",
        "artifact_id": "phase_vs2_move_authority_matrix_v0",
        "artifact_kind": "STATIC_MOVE_AUTHORITY_REQUIREMENT_MATRIX",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "matrix_id": "first_sweep_kernel_move_authority_matrix_v0",
        "matrix_version": "v0",
        "matrix_status": "FROZEN_NOT_ACTIVE",
        "scope_regime_reference": refs["f0"],
        "source_and_version_binding_contract_reference": s0_ref,
        "prospective_authority_envelope_identity": prospective_p0_identity(),
        "move_authority_rows": rows,
        "row_count": len(rows),
        "no_row_grants_active_authority": True,
        "construction_authority_provenance": auth,
        "source_basis": source_basis(["move_authority_rows", "prospective_authority_envelope_identity"], "STRICT_CROSS_ARTIFACT_INVARIANT_REQUIRED", "A0 freezes future authority requirements without granting active authority."),
    }
    return bind(payload, "matrix_binding", "matrix_payload", "matrix_sha256")


def make_ms0(refs: dict[str, dict[str, Any]], s0_ref: dict[str, Any], v0_ref: dict[str, Any], a0_ref: dict[str, Any], moves: list[dict[str, Any]], auth: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "matrixlabs_phase_vs2_finite_move_space_v0",
        "artifact_id": "phase_vs2_finite_move_space_v0",
        "artifact_kind": "TARGET_BOUND_FINITE_CANDIDATE_TRANSFORMATION_MOVE_SPACE",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "move_space_id": "FIRST_SWEEP_KERNEL_FINITE_MOVE_SPACE_V0",
        "move_space_version": "v0",
        "move_space_status": "FROZEN_NOT_ACTIVE",
        "target_family": "BOUNDED_CONTRACT_CONVERGENCE",
        "target_id": "TYPED_STATE_CONTRACT_CONVERGENCE_V0",
        "candidate_family": "TYPED_STATE_CONTRACT_CANDIDATE",
        "kernel_profile_reference": refs["profile"],
        "scope_regime_reference": refs["f0"],
        "runtime_state_contract_reference": refs["o1"],
        "candidate_schema_reference": refs["o2"],
        "target_contract_reference": refs["o3"],
        "object_model_manifest_reference": refs["m0"],
        "source_and_version_binding_contract_reference": s0_ref,
        "move_count": 8,
        "ordered_move_ids": MOVE_IDS,
        "move_contracts": moves,
        "move_contract_hashes": {move["move_id"]: move["move_contract_sha256"] for move in moves},
        "vocabulary_partition_reference": v0_ref,
        "move_authority_matrix_reference": a0_ref,
        "dependency_metadata": {
            "M04_requires_M03_only_when_source_identity_not_already_bound": True,
            "M05_and_M08_purpose_separation": "M05 excludes claim_declarations; M08 handles unsupported claims.",
            "no_generic_no_op_move": True,
        },
        "structural_applicability_contract": {
            "function": "MOVE_STRUCTURALLY_APPLICABLE",
            "evaluated_by_vs2_4": False,
            "requires": [
                "move exists in MS0",
                "required observations exist",
                "required conditions exist",
                "F0/O1/O2/O3/M0/S0 bindings match",
                "operand resolves only to target-declared paths and rules",
                "required source records exist in admitted snapshot",
                "source identity/version verify under S0",
                "required capabilities are represented",
                "destination paths are O2-mutable",
                "delta deterministic",
                "delta remains in F0",
                "no forbidden-object mutation required",
            ],
        },
        "runtime_authorization_contract": {
            "function": "MOVE_RUNTIME_AUTHORIZED",
            "evaluated_by_vs2_4": False,
            "required_sequence": ["move defined", "structurally applicable", "runtime-authorized", "selected", "applied"],
            "construction_authority_never_serves_as_execution_authority": True,
        },
        "prospective_authority_envelope_identity": prospective_p0_identity(),
        "closure_law": {
            "closed_during_execution": True,
            "dynamic_move_creation_allowed": False,
            "move_space_active": False,
            "selector_priority_defined": False,
            "zero_applied_moves_does_not_equal_failed_run": True,
        },
        "reuse_status": "TARGET_BOUND_NON_REUSABLE",
        "portability_status": "NOT_AUTHORIZED",
        "generalization_claimed": False,
        "nonclaims": {
            "does_not_bind_p0_hash": True,
            "does_not_select_move": True,
            "does_not_apply_move": True,
            "does_not_authorize_execution": True,
        },
        "construction_authority_provenance": auth,
        "source_basis": source_basis(["move_contracts", "structural_applicability_contract", "runtime_authorization_contract", "closure_law"], "STRICT_CROSS_ARTIFACT_INVARIANT_REQUIRED", "MS0 freezes the target-bound finite move space and embeds the eight move contracts."),
    }
    return bind(payload, "move_space_binding", "move_space_payload", "move_space_sha256")


def make_p0(refs: dict[str, dict[str, Any]], s0_ref: dict[str, Any], a0_ref: dict[str, Any], ms0_ref: dict[str, Any], auth: dict[str, Any]) -> dict[str, Any]:
    authority_bindings = [
        nonbound_ref("exact_source_snapshot_reference", "FUTURE_EXACT_SOURCE_SNAPSHOT", "PENDING", "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS", "EXACT_SOURCE_SNAPSHOT", "Exact source snapshot is deferred."),
        nonbound_ref("exact_fixture_set_reference", "FUTURE_EXACT_FIXTURE_SET", "PENDING", "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS", "EXACT_FIXTURE_SET", "Fixture set is deferred."),
        nonbound_ref("exact_case_count_reference", "FUTURE_EXACT_CASE_COUNT", "PENDING", "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS", "EXACT_CASE_COUNT", "Case count is deferred."),
        nonbound_ref("exact_move_bounds_reference", "FUTURE_EXACT_MOVE_BOUNDS", "PENDING", "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS", "EXACT_MOVE_BOUNDS", "Move bounds are deferred."),
        nonbound_ref("exact_run_identity_reference", "FUTURE_EXACT_RUN_IDENTITY", "PENDING", "POST_VS2_EXECUTION_AUTHORITY_DECISION", "EXACT_RUN_IDENTITY", "Run identity requires a later decision."),
        nonbound_ref("active_controlled_step_authority_reference", "ACTIVE_CONTROLLED_STEP_AUTHORITY", "ABSENT_BY_POLICY", "POST_VS2_EXECUTION_AUTHORITY_DECISION", "ACTIVE_CONTROLLED_STEP_AUTHORITY", "Active execution authority is absent by policy in VS2.4."),
        nonbound_ref("active_sweep_authority_reference", "ACTIVE_SWEEP_AUTHORITY", "ABSENT_BY_POLICY", "POST_VS2_EXECUTION_AUTHORITY_DECISION", "ACTIVE_SWEEP_AUTHORITY", "Active sweep authority is absent by policy in VS2.4."),
    ]
    maximum_scope = {
        "target_family_count_maximum": 1,
        "target_version_count_maximum": 1,
        "scope_regime_version_count_maximum": 1,
        "move_space_version_count_maximum": 1,
        "fixture_set_version_count_maximum": 1,
        "source_snapshot_version_count_maximum": 1,
        "execution_package_count_maximum": 1,
        "case_count_maximum": 20,
        "attempted_moves_per_case_maximum": 5,
        "applied_moves_per_case_maximum": 5,
        "total_attempted_moves_maximum": 100,
        "total_applied_moves_maximum": 100,
        "automatic_reruns_maximum": 0,
        "automatic_radius_renewals_maximum": 0,
    }
    payload = {
        "schema_version": "matrixlabs_phase_vs2_prospective_controlled_step_authority_envelope_v0",
        "artifact_id": "phase_vs2_prospective_controlled_step_authority_envelope_v0",
        "artifact_kind": "STATIC_PROSPECTIVE_AUTHORITY_ENVELOPE",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "envelope_id": "FIRST_SWEEP_KERNEL_PROSPECTIVE_CONTROLLED_STEP_AUTHORITY_ENVELOPE_V0",
        "envelope_version": "v0",
        "envelope_status": "FROZEN_MAXIMUM_NOT_ACTIVE",
        "kernel_profile_reference": refs["profile"],
        "scope_regime_reference": refs["f0"],
        "runtime_state_contract_reference": refs["o1"],
        "candidate_schema_reference": refs["o2"],
        "target_contract_reference": refs["o3"],
        "object_model_manifest_reference": refs["m0"],
        "source_and_version_binding_contract_reference": s0_ref,
        "move_authority_matrix_reference": a0_ref,
        "finite_move_space_reference": ms0_ref,
        "allowed_move_ids": MOVE_IDS,
        "source_policy_frame_reference": s0_ref,
        "authority_bindings": authority_bindings,
        "authority_binding_summary": {
            "authority_binding_count": 7,
            "pending_authority_binding_count": 5,
            "absent_by_policy_authority_binding_count": 2,
            "fabricated_future_authority_reference_count": 0,
        },
        "maximum_prospective_scope": maximum_scope,
        "maximum_scope_monotonicity": {
            "applied_moves_per_case_lte_attempted_moves_per_case": maximum_scope["applied_moves_per_case_maximum"] <= maximum_scope["attempted_moves_per_case_maximum"],
            "total_applied_moves_lte_total_attempted_moves": maximum_scope["total_applied_moves_maximum"] <= maximum_scope["total_attempted_moves_maximum"],
            "maximum_eligibility_not_exact_package": True,
            "later_human_decision_may_grant_only_subset": True,
        },
        "future_allowed_actions_upper_bound": [
            "inspect current candidate condition",
            "emit declared observations",
            "emit declared condition classifications",
            "enumerate structurally applicable M01-M08 moves",
            "evaluate runtime authorization",
            "select one runtime-authorized move",
            "apply only the selected move",
            "create at most one O2 successor per applied move",
            "create exactly one O1 successor per attempted controlled step",
            "consume declared move cost",
            "validate resulting candidate",
            "evaluate candidate admissibility",
            "evaluate future C20 criterion",
            "emit required move and terminal receipts",
            "repeat only under exact frozen budget and convergence rules",
        ],
        "future_prohibited_actions": [
            "new move creation",
            "move-space mutation",
            "F0 mutation",
            "O1 contract mutation",
            "O3 mutation",
            "M0 mutation",
            "S0 mutation",
            "source acquisition",
            "schema invention",
            "capability creation",
            "authority escalation",
            "automatic rerun",
            "automatic budget renewal",
            "automatic radius renewal",
            "automatic refinement application",
            "runner continuation",
            "target-family expansion",
            "target substitution",
            "scope/regime expansion",
        ],
        "future_double_authority_check": {
            "before_executable_selection": True,
            "immediately_before_application": True,
            "required_live_fields": [
                "authority_receipt_id",
                "authority_package_version",
                "run_id",
                "case_id",
                "profile identity and hash",
                "F0 identity and hash",
                "O3 identity and hash",
                "MS0 identity and hash",
                "move_id",
                "source-snapshot identity and hash",
                "fixture-set identity and hash",
                "remaining authority scope",
                "remaining move budget",
                "remaining case budget",
                "expiration state",
            ],
            "construction_authority_may_serve_as_execution_authority": False,
        },
        "envelope_active": False,
        "prospective_authority_envelope_active": False,
        "reuse_status": "TARGET_BOUND_NON_REUSABLE",
        "construction_authority_provenance": auth,
        "source_basis": source_basis(["authority_bindings", "maximum_prospective_scope", "future_double_authority_check"], "UPSTREAM_AUTHORITY_STATE_DERIVED", "P0 freezes a maximum prospective authority envelope but leaves active authority absent."),
    }
    return bind(payload, "envelope_binding", "envelope_payload", "envelope_sha256")


def downstream_bindings() -> list[dict[str, Any]]:
    pending_vs2_5 = [
        ("selector_contract_reference", "SELECTOR_CONTRACT"),
        ("applicator_contract_reference", "APPLICATOR_CONTRACT"),
        ("validation_contract_reference", "VALIDATION_CONTRACT"),
        ("candidate_admissibility_contract_reference", "CANDIDATE_ADMISSIBILITY_CONTRACT"),
        ("convergence_criterion_reference", "CONVERGENCE_CRITERION_CONTRACT"),
        ("radius_budget_halt_policy_reference", "RADIUS_BUDGET_HALT_POLICY"),
        ("move_receipt_contract_reference", "MOVE_RECEIPT_CONTRACT"),
        ("case_terminal_receipt_contract_reference", "CASE_TERMINAL_RECEIPT_CONTRACT"),
        ("replay_audit_contract_reference", "REPLAY_AUDIT_CONTRACT"),
        ("forbidden_effect_guard_reference", "FORBIDDEN_EFFECT_GUARD"),
    ]
    pending_vs2_6 = [
        ("fixture_set_reference", "FIXTURE_SET"),
        ("exact_source_snapshot_reference", "EXACT_SOURCE_SNAPSHOT"),
        ("pressure_readout_contract_reference", "PRESSURE_READOUT_CONTRACT"),
        ("evidence_yield_report_contract_reference", "EVIDENCE_YIELD_REPORT_CONTRACT"),
        ("construction_readiness_gate_reference", "CONSTRUCTION_READINESS_GATE"),
    ]
    rows = [
        nonbound_ref(ref_id, "DOWNSTREAM_CONTROLLED_STEP_BINDING", "PENDING", "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION", kind, "VS2.5 binding remains pending; no identity or path is fabricated.")
        for ref_id, kind in pending_vs2_5
    ]
    rows.extend(
        nonbound_ref(ref_id, "DOWNSTREAM_FIXTURE_AND_READINESS_BINDING", "PENDING", "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS", kind, "VS2.6 binding remains pending; no identity or path is fabricated.")
        for ref_id, kind in pending_vs2_6
    )
    rows.extend([
        nonbound_ref("active_execution_authority_reference", "ACTIVE_EXECUTION_AUTHORITY", "ABSENT_BY_POLICY", "POST_VS2_EXECUTION_AUTHORITY_DECISION", "ACTIVE_EXECUTION_AUTHORITY", "Active execution authority is absent by policy."),
        nonbound_ref("active_sweep_authority_reference", "ACTIVE_SWEEP_AUTHORITY", "ABSENT_BY_POLICY", "POST_VS2_EXECUTION_AUTHORITY_DECISION", "ACTIVE_SWEEP_AUTHORITY", "Active sweep authority is absent by policy."),
    ])
    return rows


def make_m1(refs: dict[str, dict[str, Any]], s0_ref: dict[str, Any], v0_ref: dict[str, Any], a0_ref: dict[str, Any], ms0_ref: dict[str, Any], p0_ref: dict[str, Any], auth: dict[str, Any]) -> dict[str, Any]:
    rows = downstream_bindings()
    payload = {
        "schema_version": "matrixlabs_phase_vs2_move_space_binding_manifest_v0",
        "artifact_id": "phase_vs2_move_space_binding_manifest_v0",
        "artifact_kind": "STATIC_SUCCESSOR_BINDING_MANIFEST",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "manifest_id": "first_sweep_kernel_move_space_binding_manifest_v0",
        "manifest_version": "v0",
        "manifest_status": "MOVE_SPACE_FROZEN_CONTROLLED_STEP_BINDINGS_PENDING",
        "manifest_mutable": False,
        "predecessor_object_model_manifest_reference": refs["m0"],
        "source_and_version_binding_contract_reference": s0_ref,
        "vocabulary_partition_reference": v0_ref,
        "move_authority_matrix_reference": a0_ref,
        "finite_move_space_reference": ms0_ref,
        "prospective_authority_envelope_reference": p0_ref,
        "kernel_profile_reference": refs["profile"],
        "semantic_target_freeze_reference": refs["target_freeze"],
        "scope_regime_contract_reference": refs["f0"],
        "runtime_state_contract_reference": refs["o1"],
        "candidate_contract_schema_reference": refs["o2"],
        "target_contract_reference": refs["o3"],
        "m0_remains_unchanged": True,
        "pending_downstream_bindings": rows,
        "downstream_binding_summary": {
            "downstream_binding_count": len(rows),
            "pending_binding_count": sum(1 for row in rows if row["binding_status"] == "PENDING"),
            "absent_by_policy_binding_count": sum(1 for row in rows if row["binding_status"] == "ABSENT_BY_POLICY"),
            "fabricated_future_reference_count": sum(1 for row in rows if row["binding_status"] != "BOUND" and any(row[key] is not None for key in ["artifact_id", "artifact_kind", "artifact_version", "declared_path", "content_sha256"])),
        },
        "construction_authority_provenance": auth,
        "source_basis": source_basis(["predecessor_object_model_manifest_reference", "pending_downstream_bindings", "downstream_binding_summary"], "UPSTREAM_M0_DERIVED", "M1 succeeds M0 by binding VS2.4 artifacts while leaving downstream VS2.5/VS2.6 bindings pending or absent by policy."),
    }
    return bind(payload, "manifest_binding", "manifest_payload", "manifest_sha256")


def receipt_payload(artifacts: dict[str, dict[str, Any]], moves: list[dict[str, Any]], auth: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "matrixlabs_phase_vs2_4_finite_move_space_source_and_authority_freeze_receipt_v0",
        "artifact_id": "phase_vs2_4_finite_move_space_source_and_authority_freeze_receipt_v0",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "unit_role": UNIT_ROLE,
        "committed_parent_sha": HEAD,
        "protected_upstream_canonical_hashes": {
            "scope_regime_contract_sha256": EXPECTED_CANONICAL[F0_JSON],
            "runtime_state_contract_sha256": EXPECTED_CANONICAL[O1_JSON],
            "candidate_schema_sha256": EXPECTED_CANONICAL[O2_JSON],
            "frozen_target_contract_sha256": EXPECTED_CANONICAL[O3_JSON],
            "object_model_manifest_sha256": EXPECTED_CANONICAL[M0_JSON],
            "upstream_receipt_sha256": EXPECTED_CANONICAL[VS2_3_RECEIPT_JSON],
        },
        "upstream_gate": "VS2_4_SCOPE_AND_OBJECT_MODEL_INPUT_PASS",
        "upstream_vs2_3_gate": "VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PASS",
        "upstream_vs2_3_transition": "ADVANCE(VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PENDING)",
        "construction_authority": auth,
        "vs2_4_artifact_bindings": {
            "S0": {"artifact_id": artifacts["S0"]["artifact_id"], "version": "v0", "path": S0_JSON, "canonical_sha256": artifacts["S0"]["contract_binding"]["contract_sha256"]},
            "V0": {"artifact_id": artifacts["V0"]["artifact_id"], "version": "v0", "path": V0_JSON, "canonical_sha256": artifacts["V0"]["partition_binding"]["partition_sha256"]},
            "A0": {"artifact_id": artifacts["A0"]["artifact_id"], "version": "v0", "path": A0_JSON, "canonical_sha256": artifacts["A0"]["matrix_binding"]["matrix_sha256"]},
            "MS0": {"artifact_id": artifacts["MS0"]["artifact_id"], "version": "v0", "path": MS0_JSON, "canonical_sha256": artifacts["MS0"]["move_space_binding"]["move_space_sha256"]},
            "P0": {"artifact_id": artifacts["P0"]["artifact_id"], "version": "v0", "path": P0_JSON, "canonical_sha256": artifacts["P0"]["envelope_binding"]["envelope_sha256"]},
            "M1": {"artifact_id": artifacts["M1"]["artifact_id"], "version": "v0", "path": M1_JSON, "canonical_sha256": artifacts["M1"]["manifest_binding"]["manifest_sha256"]},
        },
        "move_hashes": {move["move_id"]: move["move_contract_sha256"] for move in moves},
        "move_count": 8,
        "move_contract_count": 8,
        "vocabulary_partition_count": 7,
        "terminal_outcome_count": 17,
        "stop_budget_exhausted_present": False,
        "downstream_binding_count": 17,
        "pending_binding_count": 15,
        "absent_by_policy_binding_count": 2,
        "fabricated_future_reference_count": 0,
        "post_state": {
            "source_and_version_binding_contract_constructed": True,
            "exact_source_snapshot_frozen": False,
            "move_space_frozen": True,
            "move_space_active": False,
            "move_authority_matrix_constructed": True,
            "prospective_authority_envelope_constructed": True,
            "prospective_authority_envelope_active": False,
            "successor_binding_manifest_constructed": True,
            "M0_unchanged": True,
            "selector_constructed": False,
            "selector_priority_frozen": False,
            "applicator_constructed": False,
            "validation_execution_logic_constructed": False,
            "candidate_admissibility_execution_logic_constructed": False,
            "convergence_criterion_constructed": False,
            "runtime_instance_created": False,
            "candidate_instance_created": False,
            "fixture_instance_created": False,
            "move_enumerated_against_live_candidate": False,
            "move_selected": False,
            "move_applied": False,
            "execution_authorized": False,
            "execution_performed": False,
            "sweep_authorized": False,
            "sweep_executed": False,
            "automatic_rerun_authorized": False,
            "runner_created": False,
            "vs2_5_may_begin": True,
        },
        "gates": GATES,
        "receipt_gate": "VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PASS",
        "construction_verdict": "VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PASS",
        "evidence_yield_branch": "CONFIRMATION_YIELD",
        "logical_terminal_transition": "ADVANCE(VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_PENDING)",
        "terminal_transition": "ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_V0_PENDING)",
        "failures": [],
    }


def make_receipt(artifacts: dict[str, dict[str, Any]], moves: list[dict[str, Any]], auth: dict[str, Any]) -> dict[str, Any]:
    payload = receipt_payload(artifacts, moves, auth)
    return {
        **payload,
        "protected_upstream_raw_hashes": EXPECTED_RAW,
        "receipt_binding": {
            "canonicalization": CANON,
            "receipt_payload": payload,
            "receipt_sha256": canonical_hash(payload),
        },
    }


def verify_no_placeholder(value: Any, path: str) -> None:
    text = json.dumps(value, sort_keys=True)
    if "<" in text or ">" in text:
        fail("STOP_VS2_4_HASH_GRAPH_OR_CANONICALIZATION_INVALID", path, "angle_bracket_placeholder", "absent", "present")


def build_all(root: Path) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], dict[str, str], dict[str, Any]]:
    up = load_upstream(root)
    refs = make_refs(up)
    auth = construction_authority(up)
    s0 = make_s0(refs, auth)
    write_json(root / S0_JSON, s0)
    s0_ref = local_ref(s0, "contract_binding", "contract_sha256", S0_JSON, "SOURCE_AND_VERSION_BINDING_CONTRACT")
    moves = make_move_contracts(refs, s0_ref)
    v0 = make_v0(refs, auth)
    write_json(root / V0_JSON, v0)
    v0_ref = local_ref(v0, "partition_binding", "partition_sha256", V0_JSON, "MOVE_VOCABULARY_PARTITION")
    a0 = make_a0(refs, s0_ref, moves, auth)
    write_json(root / A0_JSON, a0)
    a0_ref = local_ref(a0, "matrix_binding", "matrix_sha256", A0_JSON, "MOVE_AUTHORITY_MATRIX")
    ms0 = make_ms0(refs, s0_ref, v0_ref, a0_ref, moves, auth)
    if "content_sha256" in json.dumps(ms0["prospective_authority_envelope_identity"], sort_keys=True):
        fail("STOP_VS2_4_HASH_GRAPH_OR_CANONICALIZATION_INVALID", MS0_JSON, "P0 hash binding", "absent", "present")
    write_json(root / MS0_JSON, ms0)
    ms0_ref = local_ref(ms0, "move_space_binding", "move_space_sha256", MS0_JSON, "FINITE_MOVE_SPACE")
    p0 = make_p0(refs, s0_ref, a0_ref, ms0_ref, auth)
    write_json(root / P0_JSON, p0)
    p0_ref = local_ref(p0, "envelope_binding", "envelope_sha256", P0_JSON, "PROSPECTIVE_AUTHORITY_ENVELOPE")
    m1 = make_m1(refs, s0_ref, v0_ref, a0_ref, ms0_ref, p0_ref, auth)
    write_json(root / M1_JSON, m1)
    artifacts = {"S0": s0, "V0": v0, "A0": a0, "MS0": ms0, "P0": p0, "M1": m1}
    receipt = make_receipt(artifacts, moves, auth)
    write_json(root / RECEIPT_JSON, receipt)
    summaries = {
        S0_MD: (s0, s0["contract_binding"]["contract_sha256"], "contract_status", ["- Exact source snapshot remains pending.", "- Unauthorized source resolution methods are forbidden."]),
        V0_MD: (v0, v0["partition_binding"]["partition_sha256"], "partition_status", ["- Seven disjoint vocabulary partitions are frozen.", "- Only V1 transformation moves may mutate O2 semantic content."]),
        A0_MD: (a0, a0["matrix_binding"]["matrix_sha256"], "matrix_status", ["- One authority row exists for each move.", "- No row grants active authority."]),
        MS0_MD: (ms0, ms0["move_space_binding"]["move_space_sha256"], "move_space_status", ["- Eight embedded move contracts are individually hashable.", "- The move space is frozen and not active."]),
        P0_MD: (p0, p0["envelope_binding"]["envelope_sha256"], "envelope_status", ["- Prospective authority envelope is maximum-only and inactive.", "- Active controlled-step and sweep authority are absent by policy."]),
        M1_MD: (m1, m1["manifest_binding"]["manifest_sha256"], "manifest_status", ["- Successor manifest binds M0 and all VS2.4 artifacts.", "- VS2.5/VS2.6 downstream bindings remain pending or absent by policy."]),
    }
    for md_path, (artifact, digest, status_key, lines) in summaries.items():
        write_md(root / md_path, artifact, digest, status_key, lines)
    for path in CORE_JSON:
        verify_no_placeholder(json.loads((root / path).read_text()), path)
    raw_hashes = {path: sha256_file(root / path) for path in CORE_ARTIFACTS}
    return artifacts, moves, raw_hashes, receipt


def forbidden_outputs(root: Path) -> list[str]:
    forbidden_fragments = [
        "selector",
        "applicator",
        "fixture",
        "source_snapshot",
        "runtime_instance",
        "candidate_instance",
        "sweep",
        "runner",
    ]
    allowed = {Path(path) for path in CORE_ARTIFACTS}
    base = root / "docs/matrixlabs/phase_vs2"
    found: list[str] = []
    if not base.exists():
        return found
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        rel_s = str(rel)
        if Path(rel_s) in allowed:
            continue
        if "phase_vs2_first_sweep_capable_kernel_profile" in rel_s:
            continue
        if "phase_vs2_typed_state_contract_convergence_target_freeze" in rel_s:
            continue
        if rel_s in EXPECTED_RAW or rel_s in {PROFILE_PATH, TARGET_FREEZE_PATH, VS2_3_RECEIPT_JSON}:
            continue
        if any(fragment in path.name for fragment in forbidden_fragments) and "phase_vs2_post_vs1_source_intake" not in rel_s:
            found.append(rel_s)
    if (root / "discussion_packets").exists():
        found.append("discussion_packets/")
    return sorted(found)


def emit_success(artifacts: dict[str, dict[str, Any]], moves: list[dict[str, Any]], raw_hashes: dict[str, str], receipt: dict[str, Any]) -> None:
    print("BUILD_PHASE_VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_V0_COMPLETE")
    print()
    print(f"phase_id={PHASE_ID}")
    print(f"unit_id={UNIT_ID}")
    print(f"unit_role={UNIT_ROLE}")
    print(f"upstream_commit_sha={HEAD}")
    print(f"scope_regime_contract_sha256={EXPECTED_CANONICAL[F0_JSON]}")
    print(f"runtime_state_contract_sha256={EXPECTED_CANONICAL[O1_JSON]}")
    print(f"candidate_schema_sha256={EXPECTED_CANONICAL[O2_JSON]}")
    print(f"frozen_target_contract_sha256={EXPECTED_CANONICAL[O3_JSON]}")
    print(f"object_model_manifest_sha256={EXPECTED_CANONICAL[M0_JSON]}")
    print(f"upstream_receipt_sha256={EXPECTED_CANONICAL[VS2_3_RECEIPT_JSON]}")
    print()
    print(f"source_and_version_binding_contract_sha256={artifacts['S0']['contract_binding']['contract_sha256']}")
    print(f"move_vocabulary_partition_sha256={artifacts['V0']['partition_binding']['partition_sha256']}")
    print(f"move_authority_matrix_sha256={artifacts['A0']['matrix_binding']['matrix_sha256']}")
    print(f"finite_move_space_sha256={artifacts['MS0']['move_space_binding']['move_space_sha256']}")
    print(f"prospective_authority_envelope_sha256={artifacts['P0']['envelope_binding']['envelope_sha256']}")
    print(f"move_space_binding_manifest_sha256={artifacts['M1']['manifest_binding']['manifest_sha256']}")
    print(f"receipt_sha256={receipt['receipt_binding']['receipt_sha256']}")
    print()
    for move in moves:
        print(f"move_hash {move['move_id']}={move['move_contract_sha256']}")
    print()
    for path in CORE_ARTIFACTS:
        print(f"raw_file_sha256 {path}={raw_hashes[path]}")
    print()
    lines = {
        "bounded_construction_grant_prior_consumed": "true",
        "bounded_construction_consumption_count_before": "1",
        "bounded_construction_consumption_count_after": "1",
        "additional_bounded_construction_grant_consumption_by_vs2_4": "false",
        "bounded_construction_frame_exercised_by_vs2_4": "true",
        "bounded_construction_frame": "VS2.3_TO_VS2.5_BOUND_TARGET_CONSTRUCTION_SEQUENCE",
        "bounded_construction_local_exercise_scope": "FINITE_MOVE_SPACE_SOURCE_BINDING_AND_PROSPECTIVE_AUTHORITY_ONLY",
        "bounded_construction_frame_open_after_vs2_4": "true",
        "remaining_frame_unit": "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION",
        "unconsumed_effective_grant_count": "3",
        "source_and_version_binding_contract_constructed": "true",
        "exact_source_snapshot_frozen": "false",
        "move_count": "8",
        "move_contract_count": "8",
        "move_space_frozen": "true",
        "move_space_active": "false",
        "vocabulary_partition_count": "7",
        "terminal_outcome_count": "17",
        "stop_budget_exhausted_present": "false",
        "move_authority_matrix_constructed": "true",
        "prospective_authority_envelope_constructed": "true",
        "prospective_authority_envelope_active": "false",
        "successor_binding_manifest_constructed": "true",
        "M0_unchanged": "true",
        "downstream_binding_count": "17",
        "pending_binding_count": "15",
        "absent_by_policy_binding_count": "2",
        "fabricated_future_reference_count": "0",
        "selector_constructed": "false",
        "selector_priority_frozen": "false",
        "applicator_constructed": "false",
        "validation_execution_logic_constructed": "false",
        "candidate_admissibility_execution_logic_constructed": "false",
        "convergence_criterion_constructed": "false",
        "runtime_instance_created": "false",
        "candidate_instance_created": "false",
        "fixture_instance_created": "false",
        "move_enumerated_against_live_candidate": "false",
        "move_selected": "false",
        "move_applied": "false",
        "execution_authority_absent": "true",
        "sweep_authority_absent": "true",
        "automatic_rerun_authority_absent": "true",
        "runner_authority_absent": "true",
        "execution_performed": "false",
        "sweep_executed": "false",
        "runner_created": "false",
        "generated_artifacts_deterministic": "true",
        "baseline_generation_deterministic": "true",
        "protected_upstream_files_unchanged": "true",
        "forbidden_output_count": "0",
    }
    for key, value in lines.items():
        print(f"{key}={value}")
    for key, value in GATES.items():
        print(f"{key}={value}")
    print("receipt_gate=VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PASS")
    print("evidence_yield_branch=CONFIRMATION_YIELD")
    print("staged_changes_present=false")
    print("commit_created=false")
    print("push_executed=false")
    print("logical_terminal_transition=ADVANCE(VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_PENDING)")
    print("terminal_transition=ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_V0_PENDING)")


def emit_stop(exc: StopFailure) -> None:
    print("BUILD_PHASE_VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_V0_STOP")
    print(f"failure_code={exc.code}")
    print(f"failed_artifact={exc.artifact}")
    print(f"failed_move_or_field={exc.field}")
    print(f"expected_value={json.dumps(exc.expected, sort_keys=True)}")
    print(f"observed_value={json.dumps(exc.observed, sort_keys=True)}")
    print(f"violated_invariant={exc.invariant}")
    print("violated_authority_boundary=VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_ONLY")
    print("blocked_downstream_unit=VS2.4")
    print("exact_bounded_correction_surface=VS2_4_REPAIR_OR_BOOKKEEPING_SURFACE")
    print("capability_proposal_candidate_required=false")
    print("human_decision_required=false")
    print("self_repair_performed=false")


def main() -> int:
    root = Path.cwd().resolve()
    try:
        check_repo(root)
        artifacts, moves, raw_hashes, receipt = build_all(root)
        forbidden = forbidden_outputs(root)
        if forbidden:
            fail("STOP_VS2_4_EXECUTION_OR_FIXTURE_DRIFT", "repo", "forbidden_outputs", [], forbidden)
        validate_dirty_scope(root)
        emit_success(artifacts, moves, raw_hashes, receipt)
        return 0
    except StopFailure as exc:
        emit_stop(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
