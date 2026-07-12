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
HEAD = "447492c24675a681edc9cdb42e21c8cb895bd5e8"
PHASE_ID = "PHASE_VS2"
UNIT_ID = "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION"
UNIT_ROLE = "CONTROLLED_STEP_AND_CONVERGENCE_CONSTRUCTION_ONLY"
CANON = "MATRIXLAB_CANONICAL_JSON_V0"
HASH_ALG = "SHA-256"

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
VS2_4_RECEIPT_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_4_finite_move_space_source_and_authority_freeze_receipt_v0.json"

CONTROLLED_DIR = "docs/matrixlabs/phase_vs2/controlled_step"
K0_JSON = f"{CONTROLLED_DIR}/phase_vs2_controlled_step_and_convergence_contract_package_v0.json"
K0_MD = f"{CONTROLLED_DIR}/phase_vs2_controlled_step_and_convergence_contract_package_v0.md"
C20_JSON = f"{CONTROLLED_DIR}/phase_vs2_convergence_criterion_contract_v0.json"
C20_MD = f"{CONTROLLED_DIR}/phase_vs2_convergence_criterion_contract_v0.md"
R13_JSON = f"{CONTROLLED_DIR}/phase_vs2_receipt_and_atomic_publication_contract_v0.json"
R13_MD = f"{CONTROLLED_DIR}/phase_vs2_receipt_and_atomic_publication_contract_v0.md"
M2_JSON = f"{CONTROLLED_DIR}/phase_vs2_controlled_step_binding_manifest_v0.json"
M2_MD = f"{CONTROLLED_DIR}/phase_vs2_controlled_step_binding_manifest_v0.md"
RECEIPT_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_5_controlled_step_and_convergence_contract_construction_receipt_v0.json"

SCRIPT = "scripts/build_phase_vs2_5_controlled_step_and_convergence_contract_construction_v0.py"
VERIFY_SCRIPT = "scripts/verify_phase_vs2_5_controlled_step_and_convergence_contract_construction_v0.py"
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
    S0_JSON: "618f19d8e5caf43d14f0ba42b0bcc60ca0dc5212a732dad1f5ea388f3463390c",
    S0_MD: "41aaebbc06b0fc905814a2ed81cab8eff704195e0cf5215f736812a5cc57877a",
    V0_JSON: "c1746ca746d35f51b7c786bb0f85b855a8e61d0d4bae93c3e6fc831cb985f579",
    V0_MD: "6a916d2f9ae755368118a647af10dae7d62501ef8c2291a83b1ac5113cc45f3b",
    A0_JSON: "dfeade066cf977484c85a4434f9715d2bdfe2a49efe900ee7c2a733850bba7df",
    A0_MD: "9315128296a3d37bba9385c57e647dd7062e43437a4a19780a2fbe6a05ba114a",
    MS0_JSON: "ff716fd0dad59cd271d383bc8b2bc0c93e678d2c5619ff7ec46a473c333f2876",
    MS0_MD: "c1d34879e3d746a7295dc3509e547f67ad5f1713a39e958eba9ff108e713d189",
    P0_JSON: "4e3d5be7c14598dac52f382534c6ac2823dea9944918430393503743c8d64719",
    P0_MD: "827cf6ff1e744cf529424e910b55ed82ab660fbd684ee8122d3a48d2c3d84d8e",
    M1_JSON: "1c7f4459535c0ff36d62e1a9b66d993370a4b3c31dad81fffa3a8d03ee655c4f",
    M1_MD: "90f7f2364aa6cce8c9309a5a4ce0bdaf5a5df86145373bd314d072b0b63157c0",
    VS2_4_RECEIPT_JSON: "ff8958094a8b8cf78c0ac40d535d7daa68feaa1599db7447ea0c64237c2a951b",
}
EXPECTED_CANONICAL = {
    F0_JSON: "a6b4819aee35e5f09686a5a69d471b31f3a5cfdcab2078a29323ba1d31211179",
    O1_JSON: "25fbdfb007372e346d61a3f5de8b0a4f5004c6dff1857e5fc31df38e17c087ad",
    O2_JSON: "0216eb5944f87e760844d018d253f5e808a7a5b7ebd208d8d717e6709b979070",
    O3_JSON: "378acf4fb02ad20bfd5213bde4b267fe605dc528812e29a985909fef251d7546",
    M0_JSON: "0af5f635aaca5c37428cc94ca1a8ee6f3885d6e56543198bbdd33a5d4062db3c",
    S0_JSON: "9b9d6133965beec3b51600ec2d0ab9f002abbd48685cd82f1cf24e0d5d16d6ef",
    V0_JSON: "a193dbbee21db8d5577445789d5971ffc29c8c5c37088d4bf88b14434c518c1d",
    A0_JSON: "4fbd5ae95a00444201f0da70c52515e630b07972f9a3202944f007547d0db0ad",
    MS0_JSON: "68b094ad5f7a283e591b7b23c66650db9921357e13b0e5c7ca7992723303cbe9",
    P0_JSON: "7f2878149b30ca59e46ffa7e12580d4b2c96784e1b7964698d56eca5853c484c",
    M1_JSON: "9cb7f9a66de7a0afc7109a07d789e56cb3629266d9f45821c0c971826afad389",
    VS2_4_RECEIPT_JSON: "c78a48e892c0554327a2b1c27570453db48ce7368b27e4b58c6830defd7ff998",
}

CORE_ARTIFACTS = [K0_JSON, K0_MD, C20_JSON, C20_MD, R13_JSON, R13_MD, M2_JSON, M2_MD, RECEIPT_JSON]
CORE_JSON = [K0_JSON, C20_JSON, R13_JSON, M2_JSON, RECEIPT_JSON]
CORE_MD = [K0_MD, C20_MD, R13_MD, M2_MD]
BASELINE_OUTPUTS = [
    "baseline_share/COMMIT_CONTEXT.md",
    "baseline_share/CURRENT_STATE.md",
    "baseline_share/MANIFEST.json",
    "baseline_share/RECEIPT_POINTERS.md",
]
ALLOWED_DIRTY = set(CORE_ARTIFACTS) | {SCRIPT, VERIFY_SCRIPT, BASELINE_SCRIPT, *BASELINE_OUTPUTS}
PROTECTED_UPSTREAM = set(EXPECTED_RAW)

COMPONENT_IDS = [
    "S01_INPUT_BINDING_VERIFIER",
    "S02_CONDITION_INSPECTOR",
    "S03_CONDITION_CLASSIFIER",
    "S04_CAPABILITY_BOUNDARY_EVALUATOR",
    "S05_TRANSFORMATION_MOVE_ENUMERATOR",
    "S06_STRUCTURAL_APPLICABILITY_EVALUATOR",
    "S07_RUNTIME_AUTHORITY_AND_BUDGET_GATE",
    "S08_DETERMINISTIC_MOVE_SELECTOR",
    "S09_MOVE_APPLICATOR",
    "S10_TARGET_CONFORMANCE_VALIDATOR",
    "S11_LAWFUL_ADMISSIBILITY_EVALUATOR",
    "S12_FORBIDDEN_EFFECT_GUARD",
    "S13_RECEIPT_AND_ATOMIC_PUBLICATION_BUILDER",
    "S14_CONVERGENCE_CRITERION_EVALUATOR",
    "S15_TERMINAL_AND_REPEAT_DECIDER",
    "S16_CONTROLLED_STEP_ORCHESTRATOR",
    "S17_MINIMAL_REPLAY_AND_AUDIT_VERIFIER",
]
PRIMARY_OUTCOMES = [
    "STEP_INPUT_REJECTED",
    "STEP_PREEXECUTION_TYPED_STOP",
    "STEP_TARGET_REACHED",
    "STEP_MOVE_APPLIED_CONTINUE",
    "STEP_TYPED_STOP",
    "STEP_PUBLICATION_ABORTED",
]
GUARD_STAGES = [
    "G1_INVOCATION_BINDING_BOUNDARY",
    "G2_POST_INSPECTION_PRE_ENUMERATION",
    "G3_PRE_APPLICATION",
    "G4_POST_DELTA_STAGING",
    "G5_PRE_PUBLICATION_SEMANTIC_GUARD",
    "G6_STAGED_BUNDLE_INTEGRITY",
    "G7_PRE_TERMINAL_OR_REPEAT_DISPOSITION",
]
DISPOSITIONS = [
    "TARGET_REACHED",
    "REPEAT_NEXT_STEP_ELIGIBLE",
    "TYPED_STOP",
    "INPUT_REJECTED",
    "PREEXECUTION_TYPED_STOP",
    "PUBLICATION_ABORTED",
]
AUDIT_RESULTS = [
    "STEP_AUDIT_PASS",
    "STEP_AUDIT_FAIL_INPUT_IDENTITY",
    "STEP_AUDIT_FAIL_SCOPE_REGIME",
    "STEP_AUDIT_FAIL_SOURCE_BINDING",
    "STEP_AUDIT_FAIL_CAPABILITY_BOUNDARY",
    "STEP_AUDIT_FAIL_MOVE_ENUMERATION",
    "STEP_AUDIT_FAIL_MOVE_SELECTION",
    "STEP_AUDIT_FAIL_AUTHORITY_CHECK",
    "STEP_AUDIT_FAIL_BUDGET_ACCOUNTING",
    "STEP_AUDIT_FAIL_DELTA",
    "STEP_AUDIT_FAIL_CANDIDATE_INTEGRITY",
    "STEP_AUDIT_FAIL_TARGET_VALIDATION",
    "STEP_AUDIT_FAIL_ADMISSIBILITY",
    "STEP_AUDIT_FAIL_GUARD",
    "STEP_AUDIT_FAIL_CONVERGENCE",
    "STEP_AUDIT_FAIL_RUNTIME_HASH",
    "STEP_AUDIT_FAIL_TERMINAL_DECISION",
    "STEP_AUDIT_FAIL_ATOMIC_PUBLICATION",
    "STEP_AUDIT_FAIL_RECEIPT_INCOMPLETE",
]

GATES = {
    "upstream_gate": "VS2_5_MOVE_SPACE_AND_AUTHORITY_INPUT_PASS",
    "construction_frame_gate": "VS2_5_CONSTRUCTION_FRAME_COMPLETION_PASS",
    "capability_boundary_gate": "VS2_5_CAPABILITY_BOUNDARY_PASS",
    "component_set_gate": "VS2_5_COMPONENT_SET_COMPLETE",
    "input_preexecution_gate": "VS2_5_INPUT_AND_PREEXECUTION_BOUNDARY_PASS",
    "inspection_classification_gate": "VS2_5_INSPECTION_AND_CLASSIFICATION_PASS",
    "move_enumeration_gate": "VS2_5_COMPLETE_MOVE_ENUMERATION_PASS",
    "authority_radius_budget_gate": "VS2_5_AUTHORITY_RADIUS_AND_BUDGET_PASS",
    "selector_gate": "VS2_5_SELECTOR_DETERMINISM_PASS",
    "applicator_integrity_gate": "VS2_5_APPLICATOR_AND_CANDIDATE_INTEGRITY_PASS",
    "validation_admissibility_gate": "VS2_5_VALIDATION_AND_ADMISSIBILITY_BOUNDARY_PASS",
    "c20_gate": "VS2_5_C20_CONVERGENCE_CRITERION_PASS",
    "terminal_family_gate": "VS2_5_TERMINAL_OUTCOME_FAMILY_PRESERVED",
    "forbidden_effect_gate": "VS2_5_FORBIDDEN_EFFECT_GUARD_PASS",
    "receipt_atomicity_gate": "VS2_5_RECEIPT_HASH_AND_ATOMIC_PUBLICATION_PASS",
    "terminal_repeat_gate": "VS2_5_TERMINAL_AND_REPEAT_POLICY_PASS",
    "audit_gate": "VS2_5_MINIMAL_STEP_AUDIT_PASS",
    "successor_manifest_gate": "VS2_5_SUCCESSOR_BINDING_MANIFEST_PASS",
    "no_runtime_drift_gate": "VS2_5_NO_RUNTIME_OR_FIXTURE_DRIFT_PASS",
}


class StopFailure(RuntimeError):
    def __init__(self, code: str, artifact: str, field: str, expected: Any, observed: Any, invariant: str = "VS2_5_CONSTRUCTION_BOUNDARY") -> None:
        super().__init__(code)
        self.code = code
        self.artifact = artifact
        self.field = field
        self.expected = expected
        self.observed = observed
        self.invariant = invariant


def fail(code: str, artifact: str, field: str, expected: Any, observed: Any, invariant: str = "VS2_5_CONSTRUCTION_BOUNDARY") -> None:
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


def validate_dirty_scope(root: Path) -> None:
    status = git(root, ["status", "--short", "--untracked-files=all"])
    paths = status_paths(status)
    unexpected = [path for path in paths if path not in ALLOWED_DIRTY]
    protected = [path for path in paths if path in PROTECTED_UPSTREAM]
    if unexpected:
        fail("STOP_VS2_5_PREEXISTING_WORKTREE_CHANGES", "repo", "dirty_paths", sorted(ALLOWED_DIRTY), unexpected)
    if protected:
        fail("STOP_VS2_5_UPSTREAM_MANIFEST_REWRITTEN", "upstream", "protected_paths", "unchanged", protected)
    if (root / "discussion_packets").exists():
        fail("STOP_VS2_5_EXECUTION_OR_FIXTURE_DRIFT", "repo", "discussion_packets", "absent", "present")


def check_repo(root: Path) -> None:
    require(str(root), ROOT, "STOP_VS2_5_REPOSITORY_ROOT_MISMATCH", "repo", "repository_root")
    require(git(root, ["rev-parse", "--show-toplevel"]), ROOT, "STOP_VS2_5_REPOSITORY_ROOT_MISMATCH", "repo", "git_root")
    require(git(root, ["branch", "--show-current"]), BRANCH, "STOP_VS2_5_BRANCH_MISMATCH", "repo", "branch")
    require(git(root, ["rev-parse", "HEAD"]), HEAD, "STOP_VS2_5_UNEXPECTED_HEAD", "repo", "HEAD")
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=root).returncode != 0
    require(staged, False, "STOP_VS2_5_STAGED_CHANGES_PRESENT", "repo", "staged_changes_present")
    validate_dirty_scope(root)


def binding_tuple(path: str) -> tuple[str, str, str]:
    return {
        F0_JSON: ("contract_binding", "contract_payload", "contract_sha256"),
        O1_JSON: ("contract_binding", "contract_payload", "contract_sha256"),
        O2_JSON: ("schema_binding", "schema_payload", "schema_sha256"),
        O3_JSON: ("target_contract_binding", "target_contract_payload", "target_contract_sha256"),
        M0_JSON: ("manifest_binding", "manifest_payload", "manifest_sha256"),
        S0_JSON: ("contract_binding", "contract_payload", "contract_sha256"),
        V0_JSON: ("partition_binding", "partition_payload", "partition_sha256"),
        A0_JSON: ("matrix_binding", "matrix_payload", "matrix_sha256"),
        MS0_JSON: ("move_space_binding", "move_space_payload", "move_space_sha256"),
        P0_JSON: ("envelope_binding", "envelope_payload", "envelope_sha256"),
        M1_JSON: ("manifest_binding", "manifest_payload", "manifest_sha256"),
        VS2_4_RECEIPT_JSON: ("receipt_binding", "receipt_payload", "receipt_sha256"),
    }[path]


def verify_committed(root: Path, rel: str, raw_sha: str) -> bytes:
    try:
        committed = git(root, ["show", f"{HEAD}:{rel}"], binary=True)
    except subprocess.CalledProcessError as exc:
        fail("STOP_VS2_5_MOVE_SPACE_AND_AUTHORITY_PACKAGE_NOT_PASS", rel, "committed_path", "present", exc.stderr)
    current_path = root / rel
    if not current_path.exists():
        fail("STOP_VS2_5_MOVE_SPACE_AND_AUTHORITY_PACKAGE_NOT_PASS", rel, "worktree_path", "present", "missing")
    current = current_path.read_bytes()
    require(current, committed, "STOP_VS2_5_MOVE_SPACE_AND_AUTHORITY_PACKAGE_NOT_PASS", rel, "committed_bytes")
    require(sha256_bytes(current), raw_sha, "STOP_VS2_5_MOVE_SPACE_AND_AUTHORITY_PACKAGE_NOT_PASS", rel, "raw_sha256")
    return current


def load_upstream(root: Path) -> dict[str, dict[str, Any]]:
    data: dict[str, dict[str, Any]] = {}
    for path, raw in EXPECTED_RAW.items():
        content = verify_committed(root, path, raw)
        if path.endswith(".json"):
            data[path] = json.loads(content.decode("utf-8"))
    for path, expected in EXPECTED_CANONICAL.items():
        artifact = data[path]
        binding, payload_key, hash_key = binding_tuple(path)
        digest = canonical_hash(artifact[binding][payload_key])
        require(artifact[binding][hash_key], expected, "STOP_VS2_5_MOVE_SPACE_AND_AUTHORITY_PACKAGE_NOT_PASS", path, hash_key)
        require(digest, expected, "STOP_VS2_5_MOVE_SPACE_AND_AUTHORITY_PACKAGE_NOT_PASS", path, f"{payload_key}_hash")
    receipt = data[VS2_4_RECEIPT_JSON]
    require(receipt.get("receipt_gate"), "VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PASS", "STOP_VS2_5_MOVE_SPACE_AND_AUTHORITY_PACKAGE_NOT_PASS", VS2_4_RECEIPT_JSON, "receipt_gate")
    require(receipt.get("logical_terminal_transition"), "ADVANCE(VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_PENDING)", "STOP_VS2_5_MOVE_SPACE_AND_AUTHORITY_PACKAGE_NOT_PASS", VS2_4_RECEIPT_JSON, "logical_terminal_transition")
    require(receipt.get("move_count"), 8, "STOP_VS2_5_MOVE_ENUMERATION_INCOMPLETE", VS2_4_RECEIPT_JSON, "move_count")
    require(receipt.get("terminal_outcome_count"), 17, "STOP_VS2_5_TERMINAL_OUTCOME_FAMILY_DRIFT", VS2_4_RECEIPT_JSON, "terminal_outcome_count")
    auth = receipt["construction_authority"]
    require(auth.get("bounded_construction_grant_prior_consumed"), True, "STOP_VS2_5_CONSTRUCTION_FRAME_NOT_OPEN", VS2_4_RECEIPT_JSON, "bounded_construction_grant_prior_consumed")
    require(auth.get("bounded_construction_consumption_count_after"), 1, "STOP_VS2_5_CONSTRUCTION_GRANT_RECONSUMPTION_ATTEMPT", VS2_4_RECEIPT_JSON, "bounded_construction_consumption_count_after")
    require(auth.get("bounded_construction_frame_open_after_vs2_4"), True, "STOP_VS2_5_CONSTRUCTION_FRAME_NOT_OPEN", VS2_4_RECEIPT_JSON, "bounded_construction_frame_open_after_vs2_4")
    return data


def source_basis(sections: list[str], basis: str, reason: str) -> list[dict[str, str]]:
    return [
        {
            "section": section,
            "basis_class": basis,
            "basis_reason": reason,
            "source_authority": "committed_vs2_move_space_authority_or_deterministic_vs2_5_construction",
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


def upstream_ref(up: dict[str, dict[str, Any]], path: str, reference_id: str, role: str, required_by: str | None = None) -> dict[str, Any]:
    artifact = up[path]
    binding, _payload_key, hash_key = binding_tuple(path)
    kind = artifact.get("artifact_kind", "UNIT_RECEIPT")
    version = (
        artifact.get("contract_version")
        or artifact.get("schema_version")
        or artifact.get("target_contract_version")
        or artifact.get("manifest_version")
        or artifact.get("partition_version")
        or artifact.get("matrix_version")
        or artifact.get("move_space_version")
        or artifact.get("envelope_version")
        or "v0"
    )
    if isinstance(version, str) and version.startswith("matrixlabs_"):
        version = "v0"
    return bound_ref(
        reference_id,
        role,
        required_by or UNIT_ID,
        artifact["artifact_id"],
        kind,
        version,
        path,
        artifact[binding][hash_key],
        f"Committed upstream {artifact['artifact_id']} canonical binding.",
    )


def local_ref(artifact: dict[str, Any], binding_name: str, hash_key: str, path: str, role: str, version_key: str, required_by: str = UNIT_ID) -> dict[str, Any]:
    return bound_ref(
        f"{artifact['artifact_id']}_reference",
        role,
        required_by,
        artifact["artifact_id"],
        artifact["artifact_kind"],
        artifact[version_key],
        path,
        artifact[binding_name][hash_key],
        f"VS2.5-built {artifact['artifact_id']} canonical binding.",
    )


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def artifact_version(artifact: dict[str, Any]) -> str:
    for key in ["package_version", "contract_version", "manifest_version"]:
        if key in artifact:
            return str(artifact[key])
    return "v0"


def artifact_status(artifact: dict[str, Any]) -> str:
    for key in ["package_status", "contract_status", "manifest_status"]:
        if key in artifact:
            return str(artifact[key])
    return "UNKNOWN"


def reference_lines(artifact: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for key, value in artifact.items():
        if key.endswith("_reference") and isinstance(value, dict):
            lines.append(f"- `{key}`: `{value['binding_status']}` `{value.get('artifact_id')}`")
    for key in ["upstream_bindings", "downstream_bindings"]:
        value = artifact.get(key)
        if isinstance(value, list):
            for row in value:
                lines.append(f"- `{row['reference_id']}`: `{row['binding_status']}` `{row.get('artifact_id')}`")
        elif isinstance(value, dict):
            for name, row in value.items():
                if isinstance(row, dict) and "binding_status" in row:
                    lines.append(f"- `{name}`: `{row['binding_status']}` `{row.get('artifact_id')}`")
    return lines


def write_md(path: Path, artifact: dict[str, Any], digest: str, extra: list[str]) -> None:
    component_summary: list[str] = []
    if "component_registry" in artifact:
        for row in artifact["component_registry"]:
            component_summary.append(f"- `{row['component_id']}`: `{row['component_sha256']}`")
    elif "component_id" in artifact:
        component_summary.append(f"- `{artifact['component_id']}`: `{digest}`")
    pending = []
    for row in artifact.get("downstream_bindings", []):
        pending.append(f"- `{row['reference_id']}`: `{row['binding_status']}`")
    lines = [
        f"# {artifact['artifact_id']}",
        "",
        f"- Artifact identity: `{artifact['artifact_id']}`",
        f"- Artifact kind: `{artifact['artifact_kind']}`",
        f"- Version: `{artifact_version(artifact)}`",
        f"- Status: `{artifact_status(artifact)}`",
        f"- Canonicalization: `{CANON}`",
        f"- Canonical SHA-256: `{digest}`",
        "",
        "## Upstream Bindings",
        "",
        *(reference_lines(artifact) or ["- No direct top-level upstream binding rows."]),
        "",
        "## Construction-Frame Posture",
        "",
        f"- Bounded construction consumption count after VS2.5: `{artifact.get('construction_authority_provenance', {}).get('bounded_construction_consumption_count_after', 'not_applicable')}`",
        f"- Construction frame open after VS2.5: `{artifact.get('construction_authority_provenance', {}).get('bounded_construction_frame_open_after_vs2_5', 'not_applicable')}`",
        "",
        "## Component Summary",
        "",
        *(component_summary or ["- No embedded component registry in this standalone contract."]),
        "",
        "## Authority Posture",
        "",
        f"- Active execution authority present: `{artifact.get('runtime_posture', {}).get('active_execution_authority_present', False)}`",
        f"- Active sweep authority present: `{artifact.get('runtime_posture', {}).get('active_sweep_authority_present', False)}`",
        "",
        "## Runtime Posture",
        "",
        f"- Runtime instance created: `{artifact.get('runtime_posture', {}).get('runtime_instance_created', False)}`",
        f"- Candidate instance created: `{artifact.get('runtime_posture', {}).get('candidate_instance_created', False)}`",
        f"- Move selected: `{artifact.get('runtime_posture', {}).get('move_selected', False)}`",
        f"- Move applied: `{artifact.get('runtime_posture', {}).get('move_applied', False)}`",
        "",
        "## Pending Bindings",
        "",
        *(pending or ["- No downstream pending bindings are declared by this artifact."]),
        "",
        "## Nonclaims",
        "",
        *(f"- `{item}`" for item in artifact.get("nonclaims", ["does_not_execute_runtime", "does_not_create_runner"])),
        "",
        "## Projection Notes",
        "",
        *extra,
        "- This Markdown file is a deterministic projection of the JSON artifact.",
    ]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def vocab_ids(v0: dict[str, Any], partition: str) -> list[str]:
    return [row["identifier"] for row in v0["partitions"][partition]]


def make_refs(up: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        "F0": upstream_ref(up, F0_JSON, "phase_vs2_scope_regime_contract_v0_reference", "SCOPE_REGIME_FRAME", "VS2.3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION"),
        "O1": upstream_ref(up, O1_JSON, "phase_vs2_runtime_control_state_contract_v0_reference", "RUNTIME_CONTROL_STATE_CONTRACT", "VS2.3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION"),
        "O2": upstream_ref(up, O2_JSON, "phase_vs2_candidate_typed_state_contract_schema_v0_reference", "CANDIDATE_SCHEMA_CONTRACT", "VS2.3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION"),
        "O3": upstream_ref(up, O3_JSON, "phase_vs2_frozen_target_contract_v0_reference", "FROZEN_TARGET_CONTRACT", "VS2.3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION"),
        "M0": upstream_ref(up, M0_JSON, "phase_vs2_object_model_binding_manifest_v0_reference", "OBJECT_MODEL_BINDING_MANIFEST", "VS2.3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION"),
        "S0": upstream_ref(up, S0_JSON, "phase_vs2_source_and_version_binding_contract_v0_reference", "SOURCE_AND_VERSION_BINDING_CONTRACT", "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE"),
        "V0": upstream_ref(up, V0_JSON, "phase_vs2_move_vocabulary_partition_v0_reference", "MOVE_VOCABULARY_PARTITION", "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE"),
        "A0": upstream_ref(up, A0_JSON, "phase_vs2_move_authority_matrix_v0_reference", "MOVE_AUTHORITY_MATRIX", "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE"),
        "MS0": upstream_ref(up, MS0_JSON, "phase_vs2_finite_move_space_v0_reference", "FINITE_MOVE_SPACE", "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE"),
        "P0": upstream_ref(up, P0_JSON, "phase_vs2_prospective_controlled_step_authority_envelope_v0_reference", "PROSPECTIVE_AUTHORITY_ENVELOPE", "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE"),
        "M1": upstream_ref(up, M1_JSON, "phase_vs2_move_space_binding_manifest_v0_reference", "MOVE_SPACE_BINDING_MANIFEST", "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE"),
        "VS2_4_RECEIPT": upstream_ref(up, VS2_4_RECEIPT_JSON, "phase_vs2_4_receipt_reference", "UPSTREAM_UNIT_RECEIPT", "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE"),
    }


def construction_authority(up: dict[str, dict[str, Any]]) -> dict[str, Any]:
    previous = up[VS2_4_RECEIPT_JSON]["construction_authority"]
    return {
        "bounded_construction_grant_id": "VS2_BOUNDED_CONSTRUCTION_AUTHORITY",
        "bounded_construction_grant_prior_consumed": True,
        "bounded_construction_consumption_count_before": 1,
        "bounded_construction_consumption_count_after": 1,
        "additional_bounded_construction_grant_consumption_by_vs2_5": False,
        "bounded_construction_frame_exercised_by_vs2_5": True,
        "bounded_construction_local_exercise_scope": "CONTROLLED_STEP_AND_CONVERGENCE_CONTRACTS_ONLY",
        "bounded_construction_frame_completed_by_vs2_5": True,
        "bounded_construction_frame_open_after_vs2_5": False,
        "bounded_construction_grant_further_use_permitted": False,
        "source_vs2_4_construction_authority": previous,
        "same_bounded_construction_grant_may_be_consumed_again": False,
        "unconsumed_effective_grant_count": 3,
        "unconsumed_effective_grant_ids": [
            "VS2_FIXTURE_CONSTRUCTION_AUTHORITY",
            "VS2_FIRST_RUN_READINESS_GATE_CONSTRUCTION_AUTHORITY",
            "VS2_CONSTRUCTION_PACKAGE_VERIFICATION_AUTHORITY",
        ],
        "fixture_construction_authority_consumed_by_vs2_5": False,
        "readiness_gate_construction_authority_consumed_by_vs2_5": False,
        "construction_package_verification_authority_consumed_by_vs2_5": False,
        "execution_authority_consumed_by_vs2_5": False,
    }


def common_forbidden_actions(extra: list[str] | None = None) -> list[str]:
    base = [
        "source acquisition",
        "source refresh",
        "schema invention",
        "capability creation",
        "authority activation",
        "authority escalation",
        "automatic repair",
        "automatic taxonomy upgrade",
        "automatic rerun",
        "automatic radius renewal",
        "runtime publication",
        "runner creation",
        "registry activation",
        "promotion record creation",
    ]
    return base + (extra or [])


def component_payload(component_id: str, primary_role: str, reads: list[str], writes: list[str], required_inputs: list[str], possible_results: list[str], receipt_obligations: list[str], allowed_next: list[str], forbidden: list[str], authority_requirements: list[str], source_sections: list[str], details: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = {
        "component_id": component_id,
        "component_version": "v0",
        "component_status": "DEFINED_AND_FROZEN_NOT_EXECUTED",
        "primary_role": primary_role,
        "reads": reads,
        "writes": writes,
        "required_inputs": required_inputs,
        "possible_results": possible_results,
        "receipt_obligations": receipt_obligations,
        "allowed_next_components": allowed_next,
        "forbidden_actions": forbidden,
        "authority_requirements": authority_requirements,
        "source_basis": source_basis(source_sections, "VS2_5_PROMPT_AND_UPSTREAM_CONTRACT_DERIVED", f"{component_id} is frozen as part of the VS2.5 controlled-step contract package."),
    }
    if details:
        payload.update(details)
    return payload


def make_embedded_components(vocab: dict[str, list[str]], move_ids: list[str]) -> dict[str, dict[str, Any]]:
    input_results = [
        "INPUT_BINDINGS_PASS",
        "INPUT_BINDINGS_PASS_AUTHORITY_ABSENT",
        "INPUT_BINDINGS_PASS_SOURCE_SNAPSHOT_ABSENT",
        "INPUT_BINDING_FAIL_SCOPE_REGIME",
        "INPUT_BINDING_FAIL_RUNTIME_STATE",
        "INPUT_BINDING_FAIL_RUNTIME_CANDIDATE",
        "INPUT_BINDING_FAIL_RUNTIME_TARGET",
        "INPUT_BINDING_FAIL_TARGET_HASH",
        "INPUT_BINDING_FAIL_OBJECT_MODEL",
        "INPUT_BINDING_FAIL_MOVE_SPACE",
        "INPUT_BINDING_FAIL_MOVE_SPACE_SUCCESSOR_MANIFEST",
        "INPUT_BINDING_FAIL_STEP_PACKAGE",
        "INPUT_BINDING_FAIL_STEP_SUCCESSOR_MANIFEST",
        "INPUT_BINDING_FAIL_KERNEL_PROFILE",
        "INPUT_BINDING_FAIL_SOURCE_RECORD",
        "INPUT_BINDING_FAIL_FIXTURE_RECORD",
        "INPUT_BINDING_FAIL_AUTHORITY_RECORD",
        "INPUT_BINDING_FAIL_RUN_CASE",
        "INPUT_BINDING_FAIL_STEP_INDEX",
        "INPUT_BINDING_FAIL_IDEMPOTENCY_KEY",
        "INPUT_BINDING_FAIL_TERMINAL_ALREADY_ACTIVE",
    ]
    classifications = [
        "HARD_FORBIDDEN_EFFECT_BLOCKER",
        "SCOPE_REGIME_BLOCKER",
        "OBJECT_BINDING_BLOCKER",
        "SOURCE_BLOCKER",
        "SCHEMA_BLOCKER",
        "AUTHORITY_BLOCKER",
        "CAPABILITY_BLOCKER",
        "NON_PROGRESS_CONDITION",
        "REPEATED_STATE_CONDITION",
        "REPAIRABLE_CONDITION_CANDIDATE",
        "NON_REPAIRABLE_CURRENT_MOVE_SPACE",
        "TARGET_CANDIDATE_STATE",
        "UNCLASSIFIED_CONDITION",
    ]
    capability_results = [
        "CAPABILITY_NOT_REQUIRED",
        "CAPABILITY_BOUNDARY_PASS",
        "CAPABILITY_MISSING",
        "CAPABILITY_UNREPRESENTED",
        "CAPABILITY_OUTSIDE_PROFILE",
        "CAPABILITY_NOT_IMPLEMENTED_BY_MOVE_SPACE",
        "CAPABILITY_EVIDENCE_INSUFFICIENT",
    ]
    integrity_results = [
        "CANDIDATE_SUCCESSOR_INTEGRITY_PASS",
        "CANDIDATE_SUCCESSOR_FAIL_SCHEMA",
        "CANDIDATE_SUCCESSOR_FAIL_VERSION_CHAIN",
        "CANDIDATE_SUCCESSOR_FAIL_DELTA_CONTRACT",
        "CANDIDATE_SUCCESSOR_FAIL_WRITE_SET",
        "CANDIDATE_SUCCESSOR_FAIL_HASH",
        "CANDIDATE_SUCCESSOR_FAIL_FORBIDDEN_MUTATION",
    ]
    components: list[dict[str, Any]] = [
        component_payload(
            "S01_INPUT_BINDING_VERIFIER",
            "Verify invocation structure and immutable bindings before semantics.",
            ["F0", "O1", "O2", "O3", "M0", "M1", "MS0", "K0", "M2", "kernel profile", "source-snapshot record", "fixture-set record", "execution-authority record"],
            ["input binding result", "pre-execution typed stop disposition when authority or source snapshot is well typed but absent"],
            ["runtime state conforms to O1", "candidate conforms to O2", "target identity and hash match O3", "terminal state not already active"],
            input_results,
            ["input-rejection receipt for malformed, invalid, or mismatched records", "pre-execution-stop receipt for well-typed absent authority or source snapshot"],
            ["S02_CONDITION_INSPECTOR", "S15_TERMINAL_AND_REPEAT_DECIDER"],
            common_forbidden_actions(["repair bindings", "substitute source", "substitute authority", "inspect candidate semantics", "create O1 successor", "create O2 successor"]),
            ["active step authority checked before semantic inspection", "construction authority cannot substitute for execution authority"],
            ["input verifier", "preexecution typed stop"],
            {
                "malformed_invalid_or_mismatched_record_maps_to": "STEP_INPUT_REJECTED",
                "authority_absent_maps_to": ["STEP_PREEXECUTION_TYPED_STOP", "STOP_MISSING_AUTHORITY"],
                "source_snapshot_absent_maps_to": ["STEP_PREEXECUTION_TYPED_STOP", "STOP_MISSING_SOURCE"],
                "input_rejection_creates_successor": False,
                "preexecution_stop_creates_successor": False,
                "move_budget_consumed": False,
            },
        ),
        component_payload(
            "S02_CONDITION_INSPECTOR",
            "Inspect candidate conditions without deciding repair, target, or terminal status.",
            ["F0", "current O1 instance", "current O2 instance", "O3", "M0", "S0-compliant source records"],
            ["condition_observation_set"],
            ["inspection_id", "runtime_state_version", "candidate_version", "candidate_hash", "target_version", "target_hash", "rules_checked", "evidence_references"],
            ["INSPECTION_COMPLETE", "NOT_EVALUABLE_MISSING_SOURCE", "NOT_EVALUABLE_MISSING_SCHEMA", "NOT_EVALUABLE_MISSING_AUTHORITY", "NOT_EVALUABLE_MISSING_CAPABILITY"],
            ["inspection receipt when authorized path proceeds"],
            ["S03_CONDITION_CLASSIFIER"],
            common_forbidden_actions(["introduce STOP_INSPECTION_INCOMPLETE", "repair candidate", "treat target observation as verdict"]),
            ["inspection requires active step authority after S01 passes"],
            ["inspection fields", "V2 observations"],
            {
                "observation_vocabulary": vocab["V2_OBSERVATIONS"],
                "required_observation_ids": [
                    "OBS_TARGET_ALREADY_REACHED",
                    "OBS_PROHIBITED_CANDIDATE_DECLARATION_PRESENT",
                    "OBS_ACTUAL_FORBIDDEN_EFFECT_DETECTED",
                    "OBS_NON_PROGRESS",
                    "OBS_REPEATED_STATE",
                    "OBS_NO_RECOGNIZED_CONDITION",
                ],
                "incomplete_inspection_terminal_mapping": {
                    "missing source": "STOP_MISSING_SOURCE",
                    "missing schema": "STOP_MISSING_SCHEMA",
                    "missing authority": "STOP_MISSING_AUTHORITY",
                    "missing capability": "STOP_MISSING_CAPABILITY",
                    "otherwise": "STOP_UNCLASSIFIED_RESULT_REQUIRES_TAXONOMY_REFINEMENT",
                },
            },
        ),
        component_payload(
            "S03_CONDITION_CLASSIFIER",
            "Classify observed conditions using frozen V3 condition IDs and deterministic precedence.",
            ["condition_observation_set", "V3 condition classifications"],
            ["classified_condition_set", "primary_exposed_condition", "secondary_observed_conditions", "classification_rule_trace"],
            ["observed_condition_ids", "classification precedence", "canonical condition IDs"],
            classifications,
            ["classification trace included in controlled-step receipt when path proceeds"],
            ["S04_CAPABILITY_BOUNDARY_EVALUATOR", "S15_TERMINAL_AND_REPEAT_DECIDER"],
            common_forbidden_actions(["invent condition vocabulary", "let target candidate outrank blocker or repairable defect"]),
            ["classification requires prior authorized inspection"],
            ["classification groups", "V3 conditions"],
            {
                "condition_vocabulary": vocab["V3_CONDITION_CLASSIFICATIONS"],
                "precedence": classifications,
                "tie_break": "lowest canonical condition ID",
                "target_candidate_cannot_outrank_blocker_or_repairable_defect": True,
            },
        ),
        component_payload(
            "S04_CAPABILITY_BOUNDARY_EVALUATOR",
            "Separate identified, represented, admitted, implemented, and authorized capability states.",
            ["primary condition", "F0", "MS0", "future active package metadata when present"],
            ["capability boundary result", "bounded proposal candidate only when missing capability branch requires it"],
            ["capability identified", "capability represented", "capability admitted by F0", "capability implemented by MS0", "capability authorized by active package"],
            capability_results,
            ["capability boundary result in controlled-step receipt"],
            ["S05_TRANSFORMATION_MOVE_ENUMERATOR", "S15_TERMINAL_AND_REPEAT_DECIDER"],
            common_forbidden_actions(["approve capability", "implement capability", "register capability", "activate capability", "promote capability", "auto-apply proposal candidate"]),
            ["capability proposal is construction evidence only, not execution authority"],
            ["capability statuses", "capability mappings"],
            {
                "terminal_mappings": {
                    "CAPABILITY_MISSING": "STOP_MISSING_CAPABILITY",
                    "CAPABILITY_UNREPRESENTED": "STOP_MISSING_CAPABILITY",
                    "CAPABILITY_OUTSIDE_PROFILE": "STOP_MISSING_CAPABILITY",
                    "CAPABILITY_NOT_IMPLEMENTED_BY_MOVE_SPACE": "STOP_NO_ADMISSIBLE_MOVE",
                    "CAPABILITY_EVIDENCE_INSUFFICIENT": ["STOP_MISSING_CAPABILITY", "STOP_UNCLASSIFIED_RESULT_REQUIRES_TAXONOMY_REFINEMENT"],
                }
            },
        ),
        component_payload(
            "S05_TRANSFORMATION_MOVE_ENUMERATOR",
            "Enumerate all frozen transformation moves on transformation branches.",
            ["primary condition", "MS0 ordered move IDs", "S0 source requirements", "O2 mutable paths", "O3 target rules"],
            ["complete structural enumeration records"],
            ["transformation branch", "MS0 bound", "move vocabulary bound"],
            ["MOVE_ENUMERATION_COMPLETE", "NOT_RUN_TYPED_NON_TRANSFORMATION_BRANCH"],
            ["enumeration coverage in controlled-step receipt"],
            ["S06_STRUCTURAL_APPLICABILITY_EVALUATOR"],
            common_forbidden_actions(["stop after first candidate", "select move", "call move candidate-admissible"]),
            ["enumeration consumes no move budget and requires no active move authority"],
            ["move enumeration", "MS0 ordered moves"],
            {
                "evaluated_move_count": 8,
                "ordered_move_ids": move_ids,
                "required_record_fields": [
                    "move_id",
                    "required_observation_match",
                    "required_condition_class_match",
                    "scope_regime_match",
                    "object_binding_match",
                    "target_rule_present",
                    "source_requirements_present",
                    "capability_requirements_present",
                    "candidate_write_paths_mutable",
                    "delta_shape_supported",
                    "structurally_applicable_candidate",
                    "structural_block_reasons",
                ],
            },
        ),
        component_payload(
            "S06_STRUCTURAL_APPLICABILITY_EVALUATOR",
            "Evaluate every enumerated move structurally before runtime authority is considered.",
            ["enumerated move records", "F0", "O1", "O2", "O3", "M0", "M1", "S0", "MS0"],
            ["structurally_applicable_move_set", "structurally_blocked_move_set"],
            ["complete enumeration", "candidate write paths", "target rules", "capability representation"],
            ["STRUCTURAL_APPLICABILITY_COMPLETE", "NO_STRUCTURALLY_APPLICABLE_MOVE"],
            ["structural applicability evidence in controlled-step receipt"],
            ["S07_RUNTIME_AUTHORITY_AND_BUDGET_GATE"],
            common_forbidden_actions(["require active authority for structural applicability", "mutate candidate"]),
            ["structural applicability does not grant runtime authority"],
            ["structural applicability"],
            {"evaluates_all_enumerated_moves": True, "active_move_authority_required": False},
        ),
        component_payload(
            "S07_RUNTIME_AUTHORITY_AND_BUDGET_GATE",
            "Check active authority, radius, budget, bindings, and attempted boundary.",
            ["structurally applicable move set", "active authority package if present", "runtime budget state", "P0 maxima"],
            ["runtime-authorized move set", "budget gate result", "attempted-boundary eligibility"],
            ["step_index", "attempted_moves_count", "applied_moves_count", "remaining attempted budget", "remaining applied budget"],
            [
                "AUTHORITY_RADIUS_BUDGET_PASS",
                "STOP_MISSING_AUTHORITY",
                "STOP_RADIUS_EXHAUSTED",
                "STOP_NO_ADMISSIBLE_MOVE",
                "CONVERGENCE_STOP_ATTEMPTED_MOVE_BOUND_EXHAUSTED",
                "CONVERGENCE_STOP_APPLIED_MOVE_BOUND_EXHAUSTED",
                "CONVERGENCE_STOP_DECLARED_RADIUS_BOUND_EXHAUSTED",
            ],
            ["authority and budget check evidence in controlled-step receipt"],
            ["S08_DETERMINISTIC_MOVE_SELECTOR", "S15_TERMINAL_AND_REPEAT_DECIDER"],
            common_forbidden_actions(["use definition authority as execution authority", "use P0 as active authority", "renew budget", "renew radius", "introduce STOP_BUDGET_EXHAUSTED"]),
            ["step authority before semantics", "move authority after structural applicability", "move authority immediately before attempted-move boundary"],
            ["authority gate", "budget vocabulary"],
            {
                "budget_accounting": {
                    "inspection_consumes_move_budget": False,
                    "classification_consumes_move_budget": False,
                    "capability_evaluation_consumes_move_budget": False,
                    "enumeration_consumes_move_budget": False,
                    "structural_applicability_consumes_move_budget": False,
                    "runtime_authorization_consumes_move_budget": False,
                    "selection_consumes_move_budget": False,
                    "infrastructure_publication_abort_consumes_authoritative_budget": False,
                },
                "forbidden_terminal": "STOP_BUDGET_EXHAUSTED",
            },
        ),
        component_payload(
            "S08_DETERMINISTIC_MOVE_SELECTOR",
            "Select at most one runtime-authorized move using frozen deterministic policy.",
            ["primary condition", "runtime-authorized move set", "move dependency metadata", "candidate version", "target version", "move-space version", "budget state"],
            ["selected_move_id", "selection_rule_trace", "unselected_runtime_authorized_move_ids"],
            ["runtime-authorized move set", "dependency metadata", "primary condition"],
            ["MOVE_SELECTED", "NO_RUNTIME_AUTHORIZED_MOVE"],
            ["selection trace in controlled-step receipt"],
            ["S07_RUNTIME_AUTHORITY_AND_BUDGET_GATE", "S09_MOVE_APPLICATOR", "S15_TERMINAL_AND_REPEAT_DECIDER"],
            common_forbidden_actions(["mutate O2", "invent a move", "call authorized moves candidate-admissible"]),
            ["selector consumes no move budget and cannot substitute missing runtime authority"],
            ["selector policy"],
            {
                "policy": [
                    "discard moves not runtime-authorized",
                    "enforce frozen dependencies",
                    "retain moves directly addressing primary condition",
                    "prefer smallest candidate write-set",
                    "prefer lowest move cost",
                    "break remaining ties by canonical move ID",
                ],
                "identity_order_is_only_final_tie_break": True,
            },
        ),
        component_payload(
            "S09_MOVE_APPLICATOR",
            "Stage exactly one O2 successor from the selected move without publishing.",
            ["selected move", "admitted sources", "O2 candidate", "O3 target rules", "S0 source records"],
            ["staged candidate delta", "canonical staged candidate hash", "candidate integrity result"],
            ["selected move only", "declared O2 write paths", "exact delta shape", "predecessor identity/version/hash"],
            integrity_results,
            ["attempted-move receipt when attempted boundary is crossed"],
            ["S12_FORBIDDEN_EFFECT_GUARD", "S10_TARGET_CONFORMANCE_VALIDATOR"],
            common_forbidden_actions(["select move", "apply multiple moves", "publish", "mutate F0", "mutate O1 directly", "mutate O3", "mutate M0", "mutate M1", "mutate MS0", "write evaluator-owned O2 fields"]),
            ["application requires selected move, rechecked authority, budget, bindings, and preconditions"],
            ["applicator", "candidate integrity"],
            {
                "maximum_o2_successors_staged": 1,
                "candidate_version_increment": 1,
                "semantic_failure_after_attempted_boundary_may_consume_attempted_budget": True,
                "candidate_integrity_results_are_auxiliary": True,
            },
        ),
        component_payload(
            "S10_TARGET_CONFORMANCE_VALIDATOR",
            "Validate candidate conformance using exact V4 result vocabulary.",
            ["current or staged candidate", "O2", "O3", "F0", "S0"],
            ["validation_result"],
            ["candidate payload", "target rules", "source declarations"],
            vocab["V4_VALIDATION_RESULTS"],
            ["validation result in controlled-step receipt"],
            ["S11_LAWFUL_ADMISSIBILITY_EVALUATOR", "S15_TERMINAL_AND_REPEAT_DECIDER"],
            common_forbidden_actions(["repair O2", "invent validation result", "conflate with candidate integrity"]),
            ["validator requires authorized path and candidate under evaluation"],
            ["V4 validation vocabulary"],
            {"validation_result_vocabulary": vocab["V4_VALIDATION_RESULTS"], "repairs_candidate": False},
        ),
        component_payload(
            "S11_LAWFUL_ADMISSIBILITY_EVALUATOR",
            "Evaluate candidate admissibility only after VALIDATION_PASS using exact V5 results.",
            ["validation result", "candidate", "sources", "authority", "capability evidence", "F0"],
            ["admissibility_result"],
            ["VALIDATION_PASS"],
            vocab["V5_CANDIDATE_ADMISSIBILITY_RESULTS"],
            ["admissibility result in controlled-step receipt"],
            ["S12_FORBIDDEN_EFFECT_GUARD", "S14_CONVERGENCE_CRITERION_EVALUATOR", "S15_TERMINAL_AND_REPEAT_DECIDER"],
            common_forbidden_actions(["repair candidate", "acquire sources", "create schemas", "create capabilities", "grant authority", "promote artifacts", "run before VALIDATION_PASS"]),
            ["admissibility evaluation requires validation pass and active step authority"],
            ["V5 admissibility vocabulary"],
            {"not_run_detail_when_validation_not_passed": "VALIDATION_DID_NOT_PASS", "repairs_candidate": False},
        ),
        component_payload(
            "S12_FORBIDDEN_EFFECT_GUARD",
            "Run seven guard stages and stop actual forbidden effects without repair.",
            ["invocation bundle", "inspection outputs", "staged delta", "staged publication bundle", "terminal or repeat disposition"],
            ["guard results", "publication abort detail when staged bundle integrity fails"],
            ["guard stage inputs", "scope/regime invariants", "authority invariants"],
            ["GUARD_PASS", "STOP_FORBIDDEN_EFFECT_DETECTED", "STEP_PUBLICATION_ABORTED"],
            ["guard evidence in controlled-step receipt and publication-attempt integrity receipt"],
            ["S10_TARGET_CONFORMANCE_VALIDATOR", "S14_CONVERGENCE_CRITERION_EVALUATOR", "S15_TERMINAL_AND_REPEAT_DECIDER"],
            common_forbidden_actions(["mark actual forbidden effect repairable", "allow hidden continuation", "introduce STOP_STEP_ATOMICITY_VIOLATION"]),
            ["guard checks cannot activate authority or repair state"],
            ["forbidden-effect guard stages"],
            {
                "guard_stages": GUARD_STAGES,
                "bundle_integrity_failure_maps_to": {"primary_outcome": "STEP_PUBLICATION_ABORTED", "publication_abort_detail": "STAGED_BUNDLE_INTEGRITY_FAILURE"},
            },
        ),
        component_payload(
            "S15_TERMINAL_AND_REPEAT_DECIDER",
            "Decide target, repeat eligibility, typed stop, input rejection, pre-execution stop, or publication abort.",
            ["C20 result", "validation result", "admissibility result", "guard results", "receipt and publication status", "runtime budget state"],
            ["controlled-step disposition"],
            ["complete upstream stage results", "strict progress witness when repeat is considered"],
            DISPOSITIONS,
            ["case-terminal or controlled-step receipt obligations according to disposition"],
            ["S13_RECEIPT_AND_ATOMIC_PUBLICATION_BUILDER", "S17_MINIMAL_REPLAY_AND_AUDIT_VERIFIER"],
            common_forbidden_actions(["self-invoke", "start another step", "reopen terminal state", "assume future move"]),
            ["repeat eligibility requires separate bounded harness authority"],
            ["terminal and repeat policy"],
            {
                "repeat_requires": [
                    "one O2 successor committed",
                    "one O1 successor committed",
                    "CONVERGENCE_CONTINUE_ALLOWED",
                    "strict progress witness",
                    "candidate hash not repeated",
                    "oscillation absent",
                    "remaining radius and budgets positive",
                    "controlled-step receipt committed",
                    "execution package still valid",
                ],
                "terminal_o1_state_immutable": True,
            },
        ),
        component_payload(
            "S16_CONTROLLED_STEP_ORCHESTRATOR",
            "Orchestrate exactly one controlled-step invocation without self-invocation.",
            ["all S01-S15 results", "K0 package", "M2 manifest", "runtime envelope when present"],
            ["ordered stage record", "skipped stage typed reasons", "single-invocation disposition"],
            ["valid invocation structure", "bound K0", "bound M2"],
            PRIMARY_OUTCOMES,
            ["controlled-step receipt references all executed and skipped stages"],
            ["S17_MINIMAL_REPLAY_AND_AUDIT_VERIFIER"],
            common_forbidden_actions(["self-invoke", "automatic rerun", "hidden continuation", "run fixture", "stage runtime publication outside R13"]),
            ["orchestration requires active execution authority when passing preflight"],
            ["S16 orchestration"],
            {
                "ordered_contract": [
                    "verify invocation structure and immutable bindings",
                    "reject malformed, invalid, or mismatched input",
                    "inspect active step-authority status",
                    "inspect source-snapshot status",
                    "run G1",
                    "inspect candidate",
                    "classify observations",
                    "evaluate capability boundary",
                    "target branch or hard-stop branch or transformation branch",
                    "allocate receipt IDs",
                    "stage O1 successor where lawful",
                    "compute state hashes",
                    "construct receipts",
                    "construct commit manifest",
                    "verify staged bundle",
                    "publish provisionally",
                    "read-back audit",
                ],
                "one_invocation_only": True,
                "skipped_stage_reason_prefix": "NOT_RUN_",
            },
        ),
        component_payload(
            "S17_MINIMAL_REPLAY_AND_AUDIT_VERIFIER",
            "Verify minimal replay and audit evidence for a completed controlled-step bundle.",
            ["input identities and hashes", "F0", "O3", "M0", "M1", "MS0", "K0", "M2", "source-snapshot binding", "execution-authority binding", "stage results", "receipt set", "commit manifest"],
            ["minimal audit result"],
            ["complete controlled-step evidence bundle"],
            AUDIT_RESULTS,
            ["audit result and failure code in controlled-step receipt"],
            [],
            common_forbidden_actions(["general replay authority", "rerun authority", "repair evidence", "publish missing receipt"]),
            ["audit is read-only and creates no replay authority"],
            ["minimal audit"],
            {"general_replay_or_rerun_authority_created": False},
        ),
    ]
    return {payload["component_id"]: payload for payload in components}


def runtime_posture() -> dict[str, bool]:
    return {
        "fixture_set_bound": False,
        "exact_source_snapshot_bound": False,
        "exact_runtime_budgets_bound": False,
        "active_execution_authority_present": False,
        "active_sweep_authority_present": False,
        "runtime_instance_created": False,
        "candidate_instance_created": False,
        "move_enumerated_against_live_candidate": False,
        "move_selected": False,
        "move_applied": False,
        "execution_performed": False,
        "sweep_executed": False,
        "runner_created": False,
    }


def make_r13(refs: dict[str, dict[str, Any]], auth: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "matrixlabs_phase_vs2_receipt_and_atomic_publication_contract_v0",
        "artifact_id": "phase_vs2_receipt_and_atomic_publication_contract_v0",
        "artifact_kind": "STATIC_RECEIPT_AND_ATOMIC_PUBLICATION_CONTRACT",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "contract_id": "FIRST_SWEEP_KERNEL_RECEIPT_AND_ATOMIC_PUBLICATION_CONTRACT_V0",
        "contract_version": "v0",
        "contract_status": "DEFINED_AND_FROZEN_NOT_EXECUTED",
        "component_id": "S13_RECEIPT_AND_ATOMIC_PUBLICATION_BUILDER",
        "component_version": "v0",
        "component_status": "DEFINED_AND_FROZEN_NOT_EXECUTED",
        "primary_role": "Build deterministic receipts and publish an authoritative bundle only after read-back passes.",
        "reads": ["controlled-step disposition", "staged O1/O2 successors", "state hashes", "receipt payloads", "commit manifest"],
        "writes": ["deterministic receipt IDs", "receipt payloads", "commit manifest", "authoritative bundle marker after read-back passes"],
        "required_inputs": ["run_id", "case_id", "step_index", "invocation envelope hash", "controlled-step disposition"],
        "possible_results": ["RECEIPT_IDS_ALLOCATED", "STAGED_BUNDLE_VERIFIED", "AUTHORITATIVE_PUBLICATION_MARKED", "STEP_PUBLICATION_ABORTED"],
        "receipt_obligations": ["input-rejection receipt", "pre-execution-stop receipt", "inspection receipt", "attempted-move receipt", "controlled-step receipt", "case-terminal receipt", "publication-attempt integrity receipt", "controlled-step commit manifest"],
        "allowed_next_components": ["S17_MINIMAL_REPLAY_AND_AUDIT_VERIFIER"],
        "forbidden_actions": common_forbidden_actions(["create authoritative O1/O2 successor on publication failure", "claim automatic rollback capability", "include receipt hashes in runtime objects"]),
        "authority_requirements": ["active execution authority required for authorized branches", "input rejection and pre-execution stop publish only bounded preflight receipts"],
        "source_basis": source_basis(["receipt classes", "runtime hash graph", "publication branches"], "VS2_5_PROMPT_DERIVED", "R13 freezes receipt and atomic publication rules without executing publication."),
        "receipt_classes": [
            "input-rejection receipt",
            "pre-execution-stop receipt",
            "inspection receipt",
            "attempted-move receipt",
            "controlled-step receipt",
            "case-terminal receipt",
            "publication-attempt integrity receipt",
            "controlled-step commit manifest",
        ],
        "receipt_id_rules": {
            "valid_run_case_receipt_id": "receipt::<run_id>::<case_id>::<step_index>::<receipt_type>",
            "invalid_preflight_receipt_id": "receipt::preflight::<invocation_envelope_hash>::<receipt_type>",
            "invocation_envelope_hash_excludes": ["receipt identifiers", "volatile metadata", "generated timestamps"],
            "receipt_ids_are_not_receipt_hashes": True,
        },
        "runtime_hash_graph_order": [
            "allocate deterministic receipt IDs",
            "stage O2 successor if permitted",
            "stage O1 successor if permitted",
            "compute O2 and O1 hashes",
            "construct receipt payloads",
            "compute receipt hashes",
            "construct commit manifest",
            "compute commit-manifest hash",
            "verify complete staged bundle",
            "publish provisionally as one bundle",
            "perform read-back integrity audit",
            "mark bundle authoritative only after read-back passes",
        ],
        "runtime_objects_may_reference_receipt_ids": True,
        "runtime_objects_may_bind_receipt_payload_hashes": False,
        "self_hashing_or_commit_manifest_hash_cycle_allowed": False,
        "publication_branches": {
            "input_rejection": ["input-rejection receipt", "rejection-integrity record"],
            "pre_execution_stop": ["pre-execution-stop receipt", "pre-execution integrity record"],
            "authorized_target": ["one terminal O1 successor", "required receipts", "one commit manifest"],
            "authorized_continue": ["one O2 successor", "one O1 successor", "inspection receipt", "attempted-move receipt", "controlled-step receipt", "one commit manifest"],
            "authorized_typed_stop_after_lawful_delta": ["O2 successor only if candidate integrity and all post-delta guards pass"],
        },
        "publication_failure": {
            "primary_outcome": "STEP_PUBLICATION_ABORTED",
            "creates_authoritative_o1_successor": False,
            "creates_authoritative_o2_successor": False,
            "creates_budget_change": False,
            "creates_terminal_state_transition": False,
            "automatic_rollback_claimed": False,
        },
        "upstream_bindings": list(refs.values()),
        "construction_authority_provenance": auth,
        "runtime_posture": runtime_posture(),
        "nonclaims": ["does_not_execute_runtime", "does_not_publish_runtime_bundle", "does_not_create_runtime_receipt_instance", "does_not_create_runner"],
    }
    return bind(payload, "contract_binding", "contract_payload", "contract_sha256")


def make_c20(refs: dict[str, dict[str, Any]], auth: dict[str, Any], vocab: dict[str, list[str]]) -> dict[str, Any]:
    payload = {
        "schema_version": "matrixlabs_phase_vs2_convergence_criterion_contract_v0",
        "artifact_id": "phase_vs2_convergence_criterion_contract_v0",
        "artifact_kind": "STATIC_OPERATIONAL_CONVERGENCE_CRITERION_CONTRACT",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "contract_id": "FIRST_SWEEP_KERNEL_CONVERGENCE_CRITERION_CONTRACT_V0",
        "contract_version": "v0",
        "contract_status": "DEFINED_AND_FROZEN_NOT_EXECUTED",
        "component_id": "S14_CONVERGENCE_CRITERION_EVALUATOR",
        "component_version": "v0",
        "component_status": "DEFINED_AND_FROZEN_NOT_EXECUTED",
        "primary_role": "Evaluate target terminal, continue, non-progress, repeated-state, oscillation, radius, and ambiguous convergence states.",
        "reads": ["binding integrity", "candidate integrity", "validation result", "admissibility result", "guard results", "candidate hash", "case history", "budget state"],
        "writes": ["convergence result", "evaluation signature"],
        "required_inputs": ["highest completed stage", "unmet rule IDs", "hard blocker classes", "primary condition", "candidate hash"],
        "possible_results": vocab["V6_CONVERGENCE_RESULTS"],
        "receipt_obligations": ["C20 result recorded in controlled-step receipt"],
        "allowed_next_components": ["S15_TERMINAL_AND_REPEAT_DECIDER"],
        "forbidden_actions": common_forbidden_actions(["mutate candidate", "renew budget", "authorize execution", "invoke rerun", "reinterpret ambiguous evidence as success"]),
        "authority_requirements": ["C20 is defined by construction, but runtime evaluation requires active step authority"],
        "source_basis": source_basis(["V6 vocabulary", "progress rule", "target and continue rules", "terminal mappings"], "VS2_5_PROMPT_AND_V0_DERIVED", "C20 preserves V6 and maps to the existing V7 terminal family."),
        "convergence_result_vocabulary": vocab["V6_CONVERGENCE_RESULTS"],
        "evaluation_stages": [
            "STAGE_0_BINDING_INTEGRITY",
            "STAGE_1_TARGET_VALIDATION",
            "STAGE_2_LAWFUL_ADMISSIBILITY",
            "STAGE_3_TARGET_TERMINAL_CONDITION",
        ],
        "evaluation_record_fields": [
            "highest_completed_stage",
            "unmet_rule_ids_at_current_stage",
            "passed_rule_ids",
            "hard_blocker_classes",
            "candidate_hash",
            "primary_condition",
            "evaluation_signature",
        ],
        "canonical_signature_fields": ["highest_completed_stage", "sorted unmet rule IDs", "sorted hard blocker classes", "primary condition ID", "candidate hash"],
        "strict_local_progress_rule": {
            "requires_candidate_integrity_pass": True,
            "requires_no_previously_passed_target_rule_regresses": True,
            "requires_no_new_hard_blocker": True,
            "progress_when_stage_increases": True,
            "progress_when_same_stage_unmet_rule_set_strict_subset": True,
            "candidate_hash_change_alone_is_progress": False,
            "move_application_alone_is_progress": False,
            "movement_is_progress": False,
        },
        "repeated_state_rule": "current candidate hash already appears in committed case history",
        "oscillation_rule": {
            "evaluation_signature_repeats_after_intervening_different_signature": True,
            "two_state_candidate_hash_cycle_detected": True,
            "maps_to": ["CONVERGENCE_STOP_OSCILLATION", "STOP_REPEATED_STATE", "OSCILLATION_DETECTED"],
        },
        "target_terminal_requires": [
            "binding integrity passes",
            "active step authority exists",
            "candidate integrity passes or unchanged current candidate remains valid",
            "VALIDATION_PASS",
            "ADMISSIBILITY_PASS",
            "all guard stages pass",
            "candidate binding matches O1",
            "target binding matches O3",
            "F0 remains invariant",
            "terminal bundle can be completed",
        ],
        "continue_requires": [
            "target not reached",
            "one lawful O2 successor staged",
            "strict local progress witnessed",
            "candidate hash not repeated",
            "oscillation absent",
            "no hard stop",
            "remaining radius positive",
            "remaining attempted budget positive",
            "remaining applied budget positive",
            "all guard stages pass",
        ],
        "unchanged_candidate_can_continue": False,
        "terminal_mappings": {
            "CONVERGENCE_STOP_NON_PROGRESS": {"terminal_outcome": "STOP_NON_PROGRESS"},
            "CONVERGENCE_STOP_REPEATED_STATE": {"terminal_outcome": "STOP_REPEATED_STATE"},
            "CONVERGENCE_STOP_OSCILLATION": {"terminal_outcome": "STOP_REPEATED_STATE", "detail": "OSCILLATION_DETECTED"},
            "CONVERGENCE_STOP_ATTEMPTED_MOVE_BOUND_EXHAUSTED": {"terminal_outcome": "STOP_RADIUS_EXHAUSTED", "detail": "ATTEMPTED_MOVE_BUDGET_EXHAUSTED"},
            "CONVERGENCE_STOP_APPLIED_MOVE_BOUND_EXHAUSTED": {"terminal_outcome": "STOP_RADIUS_EXHAUSTED", "detail": "APPLIED_MOVE_BUDGET_EXHAUSTED"},
            "CONVERGENCE_STOP_DECLARED_RADIUS_BOUND_EXHAUSTED": {"terminal_outcome": "STOP_RADIUS_EXHAUSTED", "detail": "DECLARED_RADIUS_BOUND_EXHAUSTED"},
            "CONVERGENCE_CRITERION_UNMET": {"terminal_outcome": "STOP_CONVERGENCE_CRITERION_UNMET"},
            "CONVERGENCE_RESULT_AMBIGUOUS": {"terminal_outcome": "STOP_UNCLASSIFIED_RESULT_REQUIRES_TAXONOMY_REFINEMENT"},
        },
        "upstream_bindings": list(refs.values()),
        "construction_authority_provenance": auth,
        "runtime_posture": runtime_posture(),
        "nonclaims": ["does_not_execute_convergence", "does_not_mutate_candidate", "does_not_authorize_execution", "does_not_renew_budget_or_radius"],
    }
    return bind(payload, "contract_binding", "contract_payload", "contract_sha256")


def make_k0(refs: dict[str, dict[str, Any]], auth: dict[str, Any], embedded: dict[str, dict[str, Any]], r13: dict[str, Any], c20: dict[str, Any], vocab: dict[str, list[str]], move_ids: list[str]) -> dict[str, Any]:
    component_hashes: dict[str, str] = {cid: canonical_hash(payload) for cid, payload in embedded.items()}
    component_hashes["S13_RECEIPT_AND_ATOMIC_PUBLICATION_BUILDER"] = r13["contract_binding"]["contract_sha256"]
    component_hashes["S14_CONVERGENCE_CRITERION_EVALUATOR"] = c20["contract_binding"]["contract_sha256"]
    registry = []
    r13_ref = local_ref(r13, "contract_binding", "contract_sha256", R13_JSON, "RECEIPT_AND_ATOMIC_PUBLICATION_CONTRACT", "contract_version")
    c20_ref = local_ref(c20, "contract_binding", "contract_sha256", C20_JSON, "CONVERGENCE_CRITERION_CONTRACT", "contract_version")
    for cid in COMPONENT_IDS:
        if cid == "S13_RECEIPT_AND_ATOMIC_PUBLICATION_BUILDER":
            registry.append({
                "component_id": cid,
                "component_version": "v0",
                "primary_role": r13["primary_role"],
                "component_storage": "EXTERNAL_STANDALONE_CONTRACT",
                "component_payload": None,
                "external_contract_reference": r13_ref,
                "component_sha256": component_hashes[cid],
            })
        elif cid == "S14_CONVERGENCE_CRITERION_EVALUATOR":
            registry.append({
                "component_id": cid,
                "component_version": "v0",
                "primary_role": c20["primary_role"],
                "component_storage": "EXTERNAL_STANDALONE_CONTRACT",
                "component_payload": None,
                "external_contract_reference": c20_ref,
                "component_sha256": component_hashes[cid],
            })
        else:
            payload = embedded[cid]
            registry.append({
                "component_id": cid,
                "component_version": "v0",
                "primary_role": payload["primary_role"],
                "component_storage": "EMBEDDED_IN_K0",
                "component_payload": payload,
                "external_contract_reference": None,
                "component_sha256": component_hashes[cid],
            })
    terminal_outcomes = vocab["V7_TERMINAL_OUTCOMES"]
    payload = {
        "schema_version": "matrixlabs_phase_vs2_controlled_step_and_convergence_contract_package_v0",
        "artifact_id": "phase_vs2_controlled_step_and_convergence_contract_package_v0",
        "artifact_kind": "STATIC_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_PACKAGE",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "package_id": "FIRST_SWEEP_KERNEL_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_V0",
        "package_version": "v0",
        "package_status": "FROZEN_NOT_EXECUTED",
        "controlled_step_contract": {
            "step_contract_id": "FIRST_SWEEP_KERNEL_CONTROLLED_STEP_CONTRACT_V0",
            "step_contract_version": "v0",
            "step_class": "ONE_MOVE_BOUNDED_DETERMINISTIC_RECEIPTED_ATOMIC_STEP",
            "contract_status": "DEFINED_AND_FROZEN_NOT_EXECUTED",
            "maximum_candidate_transformations_per_step": 1,
            "self_invocation_allowed": False,
        },
        "component_count": 17,
        "component_ids": COMPONENT_IDS,
        "component_ids_unique": len(COMPONENT_IDS) == len(set(COMPONENT_IDS)),
        "one_primary_role_per_component": all(row["primary_role"] for row in registry),
        "component_registry": registry,
        "component_hashes": {cid: component_hashes[cid] for cid in COMPONENT_IDS},
        "embedded_component_count": 15,
        "external_component_count": 2,
        "primary_invocation_outcomes": PRIMARY_OUTCOMES,
        "primary_invocation_outcome_count": len(PRIMARY_OUTCOMES),
        "frozen_auxiliary_vocabularies": {
            "V2_OBSERVATIONS": vocab["V2_OBSERVATIONS"],
            "V3_CONDITION_CLASSIFICATIONS": vocab["V3_CONDITION_CLASSIFICATIONS"],
            "V4_VALIDATION_RESULTS": vocab["V4_VALIDATION_RESULTS"],
            "V5_CANDIDATE_ADMISSIBILITY_RESULTS": vocab["V5_CANDIDATE_ADMISSIBILITY_RESULTS"],
            "V6_CONVERGENCE_RESULTS": vocab["V6_CONVERGENCE_RESULTS"],
            "V7_TERMINAL_OUTCOMES": terminal_outcomes,
        },
        "move_space_binding": {
            "move_count": len(move_ids),
            "ordered_move_ids": move_ids,
            "complete_enumeration_required": True,
            "enumeration_bypass_status": "NOT_RUN_TYPED_NON_TRANSFORMATION_BRANCH",
        },
        "terminal_family": {
            "terminal_outcomes": terminal_outcomes,
            "terminal_outcome_count": len(terminal_outcomes),
            "forbidden_terminal_outcomes": [
                "STOP_BUDGET_EXHAUSTED",
                "STOP_OBJECT_BINDING_MISMATCH",
                "STOP_INSPECTION_INCOMPLETE",
                "STOP_STEP_ATOMICITY_VIOLATION",
            ],
            "stop_budget_exhausted_present": "STOP_BUDGET_EXHAUSTED" in terminal_outcomes,
        },
        "selector_policy": embedded["S08_DETERMINISTIC_MOVE_SELECTOR"]["policy"],
        "candidate_integrity_auxiliary_results": embedded["S09_MOVE_APPLICATOR"]["possible_results"],
        "upstream_bindings": list(refs.values()),
        "r13_reference": r13_ref,
        "c20_reference": c20_ref,
        "m2_future_hash_bound": False,
        "construction_order": [
            "construct and hash R13",
            "construct and hash C20",
            "construct and hash the fifteen embedded component contracts",
            "construct and hash K0 without M2 hash",
            "construct and hash M2 after K0 hash exists",
            "construct and hash VS2.5 receipt",
            "render deterministic Markdown projections",
        ],
        "construction_authority_provenance": auth,
        "runtime_posture": runtime_posture(),
        "nonclaims": [
            "does_not_create_fixture_instance",
            "does_not_create_runtime_state_instance",
            "does_not_create_candidate_instance",
            "does_not_enumerate_live_candidate",
            "does_not_select_move",
            "does_not_apply_move",
            "does_not_execute_sweep",
            "does_not_create_runner",
        ],
    }
    if payload["m2_future_hash_bound"]:
        fail("STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", K0_JSON, "m2_future_hash_bound", False, True)
    return bind(payload, "package_binding", "package_payload", "package_sha256")


def downstream_bindings() -> list[dict[str, Any]]:
    pending = [
        ("fixture_set_reference", "FUTURE_FIXTURE_SET", "FIXTURE_SET"),
        ("exact_source_snapshot_reference", "FUTURE_EXACT_SOURCE_SNAPSHOT", "EXACT_SOURCE_SNAPSHOT"),
        ("exact_step_and_move_budget_reference", "FUTURE_EXACT_STEP_AND_MOVE_BUDGET", "EXACT_STEP_AND_MOVE_BUDGET"),
        ("pressure_readout_contract_reference", "FUTURE_PRESSURE_READOUT_CONTRACT", "PRESSURE_READOUT_CONTRACT"),
        ("evidence_yield_report_contract_reference", "FUTURE_EVIDENCE_YIELD_REPORT_CONTRACT", "EVIDENCE_YIELD_REPORT_CONTRACT"),
        ("construction_readiness_gate_reference", "FUTURE_CONSTRUCTION_READINESS_GATE", "CONSTRUCTION_READINESS_GATE"),
    ]
    rows = [
        nonbound_ref(ref_id, role, "PENDING", "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS", kind, "VS2.6 binding remains pending; no identity or path is fabricated.")
        for ref_id, role, kind in pending
    ]
    rows.extend([
        nonbound_ref("active_execution_authority_reference", "ACTIVE_EXECUTION_AUTHORITY", "ABSENT_BY_POLICY", "POST_VS2_EXECUTION_AUTHORITY_DECISION", "ACTIVE_EXECUTION_AUTHORITY", "Active execution authority is absent by policy in VS2.5."),
        nonbound_ref("active_sweep_authority_reference", "ACTIVE_SWEEP_AUTHORITY", "ABSENT_BY_POLICY", "POST_VS2_EXECUTION_AUTHORITY_DECISION", "ACTIVE_SWEEP_AUTHORITY", "Active sweep authority is absent by policy in VS2.5."),
    ])
    return rows


def resolved_m1_bindings(component_hashes: dict[str, str], r13_ref: dict[str, Any], c20_ref: dict[str, Any], k0_ref: dict[str, Any]) -> list[dict[str, Any]]:
    mapping = [
        ("selector_contract_reference", "S08_DETERMINISTIC_MOVE_SELECTOR", k0_ref),
        ("applicator_contract_reference", "S09_MOVE_APPLICATOR", k0_ref),
        ("validation_contract_reference", "S10_TARGET_CONFORMANCE_VALIDATOR", k0_ref),
        ("candidate_admissibility_contract_reference", "S11_LAWFUL_ADMISSIBILITY_EVALUATOR", k0_ref),
        ("convergence_criterion_reference", "S14_CONVERGENCE_CRITERION_EVALUATOR", c20_ref),
        ("radius_budget_halt_policy_reference", "S07_RUNTIME_AUTHORITY_AND_BUDGET_GATE", k0_ref),
        ("move_receipt_contract_reference", "S13_RECEIPT_AND_ATOMIC_PUBLICATION_BUILDER", r13_ref),
        ("case_terminal_receipt_contract_reference", "S13_RECEIPT_AND_ATOMIC_PUBLICATION_BUILDER", r13_ref),
        ("replay_audit_contract_reference", "S17_MINIMAL_REPLAY_AND_AUDIT_VERIFIER", k0_ref),
        ("forbidden_effect_guard_reference", "S12_FORBIDDEN_EFFECT_GUARD", k0_ref),
    ]
    return [
        {
            "m1_reference_id": ref_id,
            "resolved_component_id": component_id,
            "resolved_component_sha256": component_hashes[component_id],
            "resolution_artifact_reference": artifact_ref,
            "resolution_status": "BOUND_BY_VS2_5_M2",
        }
        for ref_id, component_id, artifact_ref in mapping
    ]


def make_m2(refs: dict[str, dict[str, Any]], auth: dict[str, Any], k0: dict[str, Any], r13: dict[str, Any], c20: dict[str, Any]) -> dict[str, Any]:
    k0_ref = local_ref(k0, "package_binding", "package_sha256", K0_JSON, "CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE", "package_version")
    r13_ref = local_ref(r13, "contract_binding", "contract_sha256", R13_JSON, "RECEIPT_AND_ATOMIC_PUBLICATION_CONTRACT", "contract_version")
    c20_ref = local_ref(c20, "contract_binding", "contract_sha256", C20_JSON, "CONVERGENCE_CRITERION_CONTRACT", "contract_version")
    component_hashes = k0["component_hashes"]
    downstream = downstream_bindings()
    payload = {
        "schema_version": "matrixlabs_phase_vs2_controlled_step_binding_manifest_v0",
        "artifact_id": "phase_vs2_controlled_step_binding_manifest_v0",
        "artifact_kind": "STATIC_SUCCESSOR_BINDING_MANIFEST",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "manifest_id": "first_sweep_kernel_controlled_step_binding_manifest_v0",
        "manifest_version": "v0",
        "manifest_status": "CONTROLLED_STEP_AND_CONVERGENCE_FROZEN_RUNTIME_PACKAGE_PENDING",
        "manifest_mutable": False,
        "predecessor_move_space_manifest_reference": refs["M1"],
        "controlled_step_package_reference": k0_ref,
        "receipt_and_atomic_publication_contract_reference": r13_ref,
        "convergence_criterion_contract_reference": c20_ref,
        "component_bindings": [
            {
                "component_id": cid,
                "component_version": "v0",
                "component_sha256": component_hashes[cid],
                "hash_algorithm": HASH_ALG,
                "canonicalization_rule": CANON,
                "binding_status": "BOUND",
            }
            for cid in COMPONENT_IDS
        ],
        "resolved_m1_vs2_5_bindings": resolved_m1_bindings(component_hashes, r13_ref, c20_ref, k0_ref),
        "resolved_m1_vs2_5_binding_count": 10,
        "downstream_bindings": downstream,
        "downstream_binding_summary": {
            "downstream_binding_count": len(downstream),
            "pending_binding_count": sum(1 for row in downstream if row["binding_status"] == "PENDING"),
            "absent_by_policy_binding_count": sum(1 for row in downstream if row["binding_status"] == "ABSENT_BY_POLICY"),
            "fabricated_future_reference_count": sum(1 for row in downstream if row["binding_status"] != "BOUND" and any(row[key] is not None for key in ["artifact_id", "artifact_kind", "artifact_version", "declared_path", "content_sha256"])),
        },
        "m1_remains_byte_identical": True,
        "m2_binds_k0_completed_hash": True,
        "k0_binds_m2_future_hash": False,
        "construction_authority_provenance": auth,
        "runtime_posture": runtime_posture(),
        "source_basis": source_basis(["predecessor_move_space_manifest_reference", "component_bindings", "downstream_bindings"], "UPSTREAM_M1_DERIVED", "M2 succeeds M1 by resolving VS2.5 component bindings and leaving VS2.6/runtime authority pending or absent by policy."),
        "nonclaims": ["does_not_create_fixture_set", "does_not_bind_exact_source_snapshot", "does_not_bind_exact_runtime_budgets", "does_not_create_active_authority"],
    }
    return bind(payload, "manifest_binding", "manifest_payload", "manifest_sha256")


def receipt_payload(k0: dict[str, Any], c20: dict[str, Any], r13: dict[str, Any], m2: dict[str, Any], raw_hashes: dict[str, str], auth: dict[str, Any]) -> dict[str, Any]:
    post_state = {
        "controlled_step_package_constructed": True,
        "component_count": 17,
        "convergence_criterion_constructed": True,
        "receipt_and_atomic_publication_contract_constructed": True,
        "controlled_step_successor_manifest_constructed": True,
        "bounded_construction_consumption_count_before": 1,
        "bounded_construction_consumption_count_after": 1,
        "additional_bounded_construction_grant_consumption_by_vs2_5": False,
        "bounded_construction_frame_completed_by_vs2_5": True,
        "bounded_construction_frame_open_after_vs2_5": False,
        "unconsumed_effective_grant_count": 3,
        "move_space_frozen": True,
        "move_space_active": False,
        "terminal_outcome_count": 17,
        "stop_budget_exhausted_present": False,
        "selector_defined": True,
        "selector_executed": False,
        "applicator_defined": True,
        "applicator_executed": False,
        "validator_defined": True,
        "validator_executed": False,
        "admissibility_evaluator_defined": True,
        "admissibility_evaluator_executed": False,
        "convergence_evaluator_defined": True,
        "convergence_evaluator_executed": False,
        "atomic_publication_protocol_defined": True,
        "atomic_publication_performed": False,
        "fixture_set_bound": False,
        "exact_source_snapshot_bound": False,
        "exact_runtime_budgets_bound": False,
        "active_execution_authority_present": False,
        "active_sweep_authority_present": False,
        "runtime_instance_created": False,
        "candidate_instance_created": False,
        "move_enumerated_against_live_candidate": False,
        "move_selected": False,
        "move_applied": False,
        "execution_performed": False,
        "sweep_executed": False,
        "runner_created": False,
        "vs2_6_may_begin": True,
    }
    artifact_bindings = {
        "K0": {
            "artifact_id": k0["artifact_id"],
            "version": k0["package_version"],
            "path": K0_JSON,
            "raw_sha256": raw_hashes[K0_JSON],
            "canonical_sha256": k0["package_binding"]["package_sha256"],
        },
        "C20": {
            "artifact_id": c20["artifact_id"],
            "version": c20["contract_version"],
            "path": C20_JSON,
            "raw_sha256": raw_hashes[C20_JSON],
            "canonical_sha256": c20["contract_binding"]["contract_sha256"],
        },
        "R13": {
            "artifact_id": r13["artifact_id"],
            "version": r13["contract_version"],
            "path": R13_JSON,
            "raw_sha256": raw_hashes[R13_JSON],
            "canonical_sha256": r13["contract_binding"]["contract_sha256"],
        },
        "M2": {
            "artifact_id": m2["artifact_id"],
            "version": m2["manifest_version"],
            "path": M2_JSON,
            "raw_sha256": raw_hashes[M2_JSON],
            "canonical_sha256": m2["manifest_binding"]["manifest_sha256"],
        },
    }
    return {
        "schema_version": "matrixlabs_phase_vs2_5_controlled_step_and_convergence_contract_construction_receipt_v0",
        "artifact_id": "phase_vs2_5_controlled_step_and_convergence_contract_construction_receipt_v0",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "unit_role": UNIT_ROLE,
        "committed_parent_sha": HEAD,
        "protected_upstream_raw_hashes": EXPECTED_RAW,
        "protected_upstream_canonical_hashes": EXPECTED_CANONICAL,
        "upstream_vs2_4_gate": "VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PASS",
        "upstream_vs2_4_transition": "ADVANCE(VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_PENDING)",
        "construction_authority": auth,
        "vs2_5_artifact_bindings": artifact_bindings,
        "component_hashes": k0["component_hashes"],
        "component_count": 17,
        "primary_invocation_outcome_count": 6,
        "terminal_outcome_count": 17,
        "move_count": 8,
        "vocabulary_partition_count": 7,
        "downstream_binding_count": 8,
        "pending_binding_count": 6,
        "absent_by_policy_binding_count": 2,
        "fabricated_future_reference_count": 0,
        "gates": GATES,
        "post_state": post_state,
        "receipt_gate": "VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_PASS",
        "construction_verdict": "VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_PASS",
        "evidence_yield_branch": "CONFIRMATION_YIELD",
        "logical_terminal_transition": "ADVANCE(VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS_PENDING)",
        "terminal_transition": "ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_V0_PENDING)",
        "failures": [],
    }


def make_receipt(k0: dict[str, Any], c20: dict[str, Any], r13: dict[str, Any], m2: dict[str, Any], raw_hashes: dict[str, str], auth: dict[str, Any]) -> dict[str, Any]:
    payload = receipt_payload(k0, c20, r13, m2, raw_hashes, auth)
    return {
        **payload,
        "receipt_binding": {
            "canonicalization": CANON,
            "receipt_payload": payload,
            "receipt_sha256": canonical_hash(payload),
        },
    }


def verify_no_self_hash_cycles(k0: dict[str, Any], m2: dict[str, Any], receipt: dict[str, Any]) -> None:
    k0_text = json.dumps(k0["package_binding"]["package_payload"], sort_keys=True)
    m2_hash = m2["manifest_binding"]["manifest_sha256"]
    if m2_hash in k0_text:
        fail("STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", K0_JSON, "m2_hash_in_k0_payload", "absent", "present")
    receipt_hash = receipt["receipt_binding"]["receipt_sha256"]
    payload_text = json.dumps(receipt["receipt_binding"]["receipt_payload"], sort_keys=True)
    if receipt_hash in payload_text:
        fail("STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", RECEIPT_JSON, "receipt_self_hash_in_payload", "absent", "present")


def build_all(root: Path) -> tuple[dict[str, dict[str, Any]], dict[str, str], dict[str, Any]]:
    up = load_upstream(root)
    refs = make_refs(up)
    auth = construction_authority(up)
    v0 = up[V0_JSON]
    ms0 = up[MS0_JSON]
    vocab = {
        "V2_OBSERVATIONS": vocab_ids(v0, "V2_OBSERVATIONS"),
        "V3_CONDITION_CLASSIFICATIONS": vocab_ids(v0, "V3_CONDITION_CLASSIFICATIONS"),
        "V4_VALIDATION_RESULTS": vocab_ids(v0, "V4_VALIDATION_RESULTS"),
        "V5_CANDIDATE_ADMISSIBILITY_RESULTS": vocab_ids(v0, "V5_CANDIDATE_ADMISSIBILITY_RESULTS"),
        "V6_CONVERGENCE_RESULTS": vocab_ids(v0, "V6_CONVERGENCE_RESULTS"),
        "V7_TERMINAL_OUTCOMES": vocab_ids(v0, "V7_TERMINAL_OUTCOMES"),
    }
    move_ids = ms0["ordered_move_ids"]
    r13 = make_r13(refs, auth)
    write_json(root / R13_JSON, r13)
    c20 = make_c20(refs, auth, vocab)
    write_json(root / C20_JSON, c20)
    embedded = make_embedded_components(vocab, move_ids)
    k0 = make_k0(refs, auth, embedded, r13, c20, vocab, move_ids)
    write_json(root / K0_JSON, k0)
    m2 = make_m2(refs, auth, k0, r13, c20)
    write_json(root / M2_JSON, m2)
    raw_hashes = {path: sha256_file(root / path) for path in [K0_JSON, C20_JSON, R13_JSON, M2_JSON]}
    receipt = make_receipt(k0, c20, r13, m2, raw_hashes, auth)
    verify_no_self_hash_cycles(k0, m2, receipt)
    write_json(root / RECEIPT_JSON, receipt)
    write_md(root / K0_MD, k0, k0["package_binding"]["package_sha256"], ["- K0 embeds fifteen component contracts and externally binds R13 and C20.", "- K0 does not bind M2's future hash."])
    write_md(root / C20_MD, c20, c20["contract_binding"]["contract_sha256"], ["- C20 preserves exact V6 convergence results.", "- C20 maps radius exhaustion to STOP_RADIUS_EXHAUSTED, not STOP_BUDGET_EXHAUSTED."])
    write_md(root / R13_MD, r13, r13["contract_binding"]["contract_sha256"], ["- R13 defines receipt IDs and atomic publication ordering.", "- R13 does not create runtime receipts or publish a runtime bundle in VS2.5."])
    write_md(root / M2_MD, m2, m2["manifest_binding"]["manifest_sha256"], ["- M2 resolves the ten VS2.5 M1 bindings.", "- VS2.6 bindings remain pending and active authorities remain absent by policy."])
    raw_hashes = {path: sha256_file(root / path) for path in CORE_ARTIFACTS}
    artifacts = {"K0": k0, "C20": c20, "R13": r13, "M2": m2, "receipt": receipt}
    return artifacts, raw_hashes, up[VS2_4_RECEIPT_JSON]


def forbidden_outputs(root: Path) -> list[str]:
    forbidden = []
    forbidden_paths = [
        "discussion_packets",
        "docs/matrixlabs/phase_vs2/fixtures",
        "docs/matrixlabs/phase_vs2/source_snapshots",
        "docs/matrixlabs/phase_vs2/runtime_instances",
        "docs/matrixlabs/phase_vs2/candidate_instances",
        "docs/matrixlabs/phase_vs2/sweeps",
        "docs/matrixlabs/phase_vs2/runners",
    ]
    for rel in forbidden_paths:
        if (root / rel).exists():
            forbidden.append(rel)
    return forbidden


def emit_success(artifacts: dict[str, dict[str, Any]], raw_hashes: dict[str, str]) -> None:
    k0 = artifacts["K0"]
    c20 = artifacts["C20"]
    r13 = artifacts["R13"]
    m2 = artifacts["M2"]
    receipt = artifacts["receipt"]
    print("BUILD_PHASE_VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_V0_COMPLETE")
    print()
    print(f"phase_id={PHASE_ID}")
    print(f"unit_id={UNIT_ID}")
    print(f"unit_role={UNIT_ROLE}")
    print(f"upstream_commit_sha={HEAD}")
    print()
    for path, digest in EXPECTED_CANONICAL.items():
        print(f"upstream_canonical_sha256 {path}={digest}")
    print()
    print(f"controlled_step_package_sha256={k0['package_binding']['package_sha256']}")
    print(f"convergence_criterion_contract_sha256={c20['contract_binding']['contract_sha256']}")
    print(f"receipt_and_atomic_publication_contract_sha256={r13['contract_binding']['contract_sha256']}")
    print(f"controlled_step_binding_manifest_sha256={m2['manifest_binding']['manifest_sha256']}")
    print(f"receipt_sha256={receipt['receipt_binding']['receipt_sha256']}")
    print()
    for component_id in COMPONENT_IDS:
        print(f"component_hash {component_id}={k0['component_hashes'][component_id]}")
    print()
    for path in CORE_ARTIFACTS:
        print(f"raw_file_sha256 {path}={raw_hashes[path]}")
    print()
    lines = {
        "bounded_construction_grant_prior_consumed": "true",
        "bounded_construction_consumption_count_before": "1",
        "bounded_construction_consumption_count_after": "1",
        "additional_bounded_construction_grant_consumption_by_vs2_5": "false",
        "bounded_construction_frame_exercised_by_vs2_5": "true",
        "bounded_construction_local_exercise_scope": "CONTROLLED_STEP_AND_CONVERGENCE_CONTRACTS_ONLY",
        "bounded_construction_frame_completed_by_vs2_5": "true",
        "bounded_construction_frame_open_after_vs2_5": "false",
        "bounded_construction_grant_further_use_permitted": "false",
        "unconsumed_effective_grant_count": "3",
        "controlled_step_package_constructed": "true",
        "component_count": "17",
        "component_ids_unique": "true",
        "one_primary_role_per_component": "true",
        "primary_invocation_outcome_count": "6",
        "convergence_criterion_constructed": "true",
        "receipt_and_atomic_publication_contract_constructed": "true",
        "controlled_step_successor_manifest_constructed": "true",
        "move_space_frozen": "true",
        "move_space_active": "false",
        "move_count": "8",
        "vocabulary_partition_count": "7",
        "terminal_outcome_count": "17",
        "stop_budget_exhausted_present": "false",
        "selector_defined": "true",
        "selector_executed": "false",
        "applicator_defined": "true",
        "applicator_executed": "false",
        "validator_defined": "true",
        "validator_executed": "false",
        "admissibility_evaluator_defined": "true",
        "admissibility_evaluator_executed": "false",
        "convergence_evaluator_defined": "true",
        "convergence_evaluator_executed": "false",
        "atomic_publication_protocol_defined": "true",
        "atomic_publication_performed": "false",
        "fixture_set_bound": "false",
        "exact_source_snapshot_bound": "false",
        "exact_runtime_budgets_bound": "false",
        "active_execution_authority_present": "false",
        "active_sweep_authority_present": "false",
        "runtime_instance_created": "false",
        "candidate_instance_created": "false",
        "move_enumerated_against_live_candidate": "false",
        "move_selected": "false",
        "move_applied": "false",
        "execution_performed": "false",
        "sweep_executed": "false",
        "runner_created": "false",
        "downstream_binding_count": "8",
        "pending_binding_count": "6",
        "absent_by_policy_binding_count": "2",
        "fabricated_future_reference_count": "0",
        "generated_artifacts_deterministic": "true",
        "baseline_generation_deterministic": "true",
        "protected_upstream_files_unchanged": "true",
        "forbidden_output_count": "0",
    }
    for key, value in lines.items():
        print(f"{key}={value}")
    for key, value in GATES.items():
        print(f"{key}={value}")
    print("receipt_gate=VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_PASS")
    print("evidence_yield_branch=CONFIRMATION_YIELD")
    print("staged_changes_present=false")
    print("commit_created=false")
    print("push_executed=false")
    print("logical_terminal_transition=ADVANCE(VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS_PENDING)")
    print("terminal_transition=ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_V0_PENDING)")
    print()
    print("git status --short --untracked-files=all")
    print(git(Path(ROOT), ["status", "--short", "--untracked-files=all"]))


def emit_stop(exc: StopFailure) -> None:
    print("BUILD_PHASE_VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_V0_STOP")
    print(f"failure_code={exc.code}")
    print(f"failed_artifact={exc.artifact}")
    print(f"failed_component_or_field={exc.field}")
    print(f"expected_value={json.dumps(exc.expected, sort_keys=True)}")
    print(f"observed_value={json.dumps(exc.observed, sort_keys=True)}")
    print(f"violated_invariant={exc.invariant}")
    print("violated_authority_boundary=VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONSTRUCTION_ONLY")
    print("blocked_downstream_unit=VS2.5")
    print("exact_bounded_correction_surface=VS2_5_REPAIR_OR_BOOKKEEPING_SURFACE")
    print("capability_proposal_candidate_required=false")
    print("human_decision_required=false")
    print("self_repair_performed=false")


def main() -> int:
    root = Path.cwd().resolve()
    try:
        check_repo(root)
        artifacts, raw_hashes, _upstream_receipt = build_all(root)
        forbidden = forbidden_outputs(root)
        if forbidden:
            fail("STOP_VS2_5_EXECUTION_OR_FIXTURE_DRIFT", "repo", "forbidden_outputs", [], forbidden)
        validate_dirty_scope(root)
        emit_success(artifacts, raw_hashes)
        return 0
    except StopFailure as exc:
        emit_stop(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
