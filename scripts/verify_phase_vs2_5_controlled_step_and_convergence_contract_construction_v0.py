#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path("/home/asd/projects/matrixlab")
HEAD = "447492c24675a681edc9cdb42e21c8cb895bd5e8"
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
CORE_ARTIFACTS = [K0_JSON, K0_MD, C20_JSON, C20_MD, R13_JSON, R13_MD, M2_JSON, M2_MD, RECEIPT_JSON]
CORE_JSON = [K0_JSON, C20_JSON, R13_JSON, M2_JSON, RECEIPT_JSON]
CORE_MD = [K0_MD, C20_MD, R13_MD, M2_MD]
BASELINE_OUTPUTS = [
    "baseline_share/COMMIT_CONTEXT.md",
    "baseline_share/CURRENT_STATE.md",
    "baseline_share/MANIFEST.json",
    "baseline_share/RECEIPT_POINTERS.md",
]
ALLOWED_DIRTY = set(CORE_ARTIFACTS) | {
    "scripts/build_phase_vs2_5_controlled_step_and_convergence_contract_construction_v0.py",
    "scripts/verify_phase_vs2_5_controlled_step_and_convergence_contract_construction_v0.py",
    "scripts/build_baseline_share_v0.py",
    *BASELINE_OUTPUTS,
}


class StopFailure(RuntimeError):
    def __init__(self, code: str, artifact: str, field: str, expected: Any, observed: Any, invariant: str = "VS2_5_VERIFIER_INVARIANT") -> None:
        super().__init__(code)
        self.code = code
        self.artifact = artifact
        self.field = field
        self.expected = expected
        self.observed = observed
        self.invariant = invariant


def stop(code: str, artifact: str, field: str, expected: Any, observed: Any, invariant: str = "VS2_5_VERIFIER_INVARIANT") -> None:
    raise StopFailure(code, artifact, field, expected, observed, invariant)


def git(*args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=not binary)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, ["git", *args], result.stdout, result.stderr)
    return result.stdout if binary else result.stdout.strip()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    return sha256_bytes((ROOT / path).read_bytes())


def canonical_hash(payload: Any) -> str:
    return sha256_bytes(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def load(path: str) -> dict[str, Any]:
    if not (ROOT / path).exists():
        stop("STOP_VS2_5_SUCCESSOR_BINDING_MANIFEST_MISSING", path, "path", "present", "missing")
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def require(observed: Any, expected: Any, code: str, artifact: str, field: str) -> None:
    if observed != expected:
        stop(code, artifact, field, expected, observed)


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
        K0_JSON: ("package_binding", "package_payload", "package_sha256"),
        C20_JSON: ("contract_binding", "contract_payload", "contract_sha256"),
        R13_JSON: ("contract_binding", "contract_payload", "contract_sha256"),
        M2_JSON: ("manifest_binding", "manifest_payload", "manifest_sha256"),
        RECEIPT_JSON: ("receipt_binding", "receipt_payload", "receipt_sha256"),
    }[path]


def status_paths(status: str) -> list[str]:
    paths: list[str] = []
    for line in status.splitlines():
        raw = line[2:].strip()
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]
        paths.append(raw)
    return paths


def verify_dirty_scope() -> None:
    paths = status_paths(git("status", "--short", "--untracked-files=all"))
    unexpected = [path for path in paths if path not in ALLOWED_DIRTY]
    if unexpected:
        stop("STOP_VS2_5_EXECUTION_OR_FIXTURE_DRIFT", "repo", "dirty_paths", sorted(ALLOWED_DIRTY), unexpected)


def verify_upstream() -> dict[str, dict[str, Any]]:
    require(git("rev-parse", "HEAD"), HEAD, "STOP_VS2_5_MOVE_SPACE_AND_AUTHORITY_PACKAGE_NOT_PASS", "repo", "HEAD")
    data: dict[str, dict[str, Any]] = {}
    for path, raw_hash in EXPECTED_RAW.items():
        committed = git("show", f"{HEAD}:{path}", binary=True)
        current = (ROOT / path).read_bytes()
        require(current, committed, "STOP_VS2_5_MOVE_SPACE_AND_AUTHORITY_PACKAGE_NOT_PASS", path, "committed_bytes")
        require(sha256_bytes(current), raw_hash, "STOP_VS2_5_MOVE_SPACE_AND_AUTHORITY_PACKAGE_NOT_PASS", path, "raw_sha256")
        if path.endswith(".json"):
            data[path] = json.loads(current.decode("utf-8"))
    for path, expected in EXPECTED_CANONICAL.items():
        artifact = data[path]
        binding, payload_key, hash_key = binding_tuple(path)
        require(artifact[binding]["canonicalization"], CANON, "STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", path, "canonicalization")
        digest = canonical_hash(artifact[binding][payload_key])
        require(digest, expected, "STOP_VS2_5_MOVE_SPACE_AND_AUTHORITY_PACKAGE_NOT_PASS", path, f"{payload_key}_hash")
        require(artifact[binding][hash_key], expected, "STOP_VS2_5_MOVE_SPACE_AND_AUTHORITY_PACKAGE_NOT_PASS", path, hash_key)
    receipt = data[VS2_4_RECEIPT_JSON]
    require(receipt.get("receipt_gate"), "VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PASS", "STOP_VS2_5_MOVE_SPACE_AND_AUTHORITY_PACKAGE_NOT_PASS", VS2_4_RECEIPT_JSON, "receipt_gate")
    require(receipt.get("logical_terminal_transition"), "ADVANCE(VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_PENDING)", "STOP_VS2_5_MOVE_SPACE_AND_AUTHORITY_PACKAGE_NOT_PASS", VS2_4_RECEIPT_JSON, "logical_terminal_transition")
    return data


def verify_binding(path: str, artifact: dict[str, Any]) -> str:
    binding, payload_key, hash_key = binding_tuple(path)
    require(artifact[binding]["canonicalization"], CANON, "STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", path, "canonicalization")
    digest = canonical_hash(artifact[binding][payload_key])
    require(artifact[binding][hash_key], digest, "STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", path, hash_key)
    return digest


def vocab_ids(v0: dict[str, Any], partition: str) -> list[str]:
    return [row["identifier"] for row in v0["partitions"][partition]]


def verify_reference_nulls(row: dict[str, Any], artifact: str) -> None:
    if row["binding_status"] in {"PENDING", "ABSENT_BY_POLICY", "NOT_APPLICABLE"}:
        for key in ["artifact_id", "artifact_kind", "artifact_version", "declared_path", "content_sha256", "hash_algorithm", "canonicalization_rule"]:
            require(row[key], None, "STOP_VS2_5_SUCCESSOR_BINDING_MANIFEST_MISSING", artifact, f"{row['reference_id']}.{key}")
    elif row["binding_status"] == "BOUND":
        require(row["hash_algorithm"], HASH_ALG, "STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", artifact, f"{row['reference_id']}.hash_algorithm")
        require(row["canonicalization_rule"], CANON, "STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", artifact, f"{row['reference_id']}.canonicalization_rule")
    else:
        stop("STOP_VS2_5_SUCCESSOR_BINDING_MANIFEST_MISSING", artifact, f"{row['reference_id']}.binding_status", ["BOUND", "PENDING", "ABSENT_BY_POLICY", "NOT_APPLICABLE"], row["binding_status"])


def verify_generated(up: dict[str, dict[str, Any]]) -> dict[str, Any]:
    k0 = load(K0_JSON)
    c20 = load(C20_JSON)
    r13 = load(R13_JSON)
    m2 = load(M2_JSON)
    receipt = load(RECEIPT_JSON)
    k0_hash = verify_binding(K0_JSON, k0)
    c20_hash = verify_binding(C20_JSON, c20)
    r13_hash = verify_binding(R13_JSON, r13)
    m2_hash = verify_binding(M2_JSON, m2)
    receipt_hash = verify_binding(RECEIPT_JSON, receipt)

    require(k0["artifact_id"], "phase_vs2_controlled_step_and_convergence_contract_package_v0", "STOP_VS2_5_STEP_CONTRACT_ID_MISSING", K0_JSON, "artifact_id")
    require(k0["component_ids"], COMPONENT_IDS, "STOP_VS2_5_COMPONENT_SET_INCOMPLETE", K0_JSON, "component_ids")
    require(k0["component_count"], 17, "STOP_VS2_5_COMPONENT_SET_INCOMPLETE", K0_JSON, "component_count")
    require(k0["primary_invocation_outcomes"], PRIMARY_OUTCOMES, "STOP_VS2_5_TERMINAL_REPEAT_POLICY_INCOMPLETE", K0_JSON, "primary_invocation_outcomes")
    registry = k0["component_registry"]
    require([row["component_id"] for row in registry], COMPONENT_IDS, "STOP_VS2_5_COMPONENT_SET_INCOMPLETE", K0_JSON, "component_registry.order")
    require(len({row["primary_role"] for row in registry}), 17, "STOP_VS2_5_COMPONENT_ROLE_CONFLATION", K0_JSON, "primary_role_count")
    recomputed_components = {}
    for row in registry:
        cid = row["component_id"]
        if cid == "S13_RECEIPT_AND_ATOMIC_PUBLICATION_BUILDER":
            recomputed = r13_hash
            require(row["component_payload"], None, "STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", K0_JSON, f"{cid}.component_payload")
        elif cid == "S14_CONVERGENCE_CRITERION_EVALUATOR":
            recomputed = c20_hash
            require(row["component_payload"], None, "STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", K0_JSON, f"{cid}.component_payload")
        else:
            payload = row["component_payload"]
            for field in ["component_id", "component_version", "component_status", "primary_role", "reads", "writes", "required_inputs", "possible_results", "receipt_obligations", "allowed_next_components", "forbidden_actions", "authority_requirements", "source_basis"]:
                if field not in payload:
                    stop("STOP_VS2_5_COMPONENT_SET_INCOMPLETE", K0_JSON, f"{cid}.{field}", "present", "missing")
            recomputed = canonical_hash(payload)
        recomputed_components[cid] = recomputed
        require(row["component_sha256"], recomputed, "STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", K0_JSON, f"{cid}.component_sha256")
        require(k0["component_hashes"][cid], recomputed, "STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", K0_JSON, f"component_hashes.{cid}")
    require(recomputed_components["S13_RECEIPT_AND_ATOMIC_PUBLICATION_BUILDER"], r13_hash, "STOP_VS2_5_RECEIPT_HASH_CYCLE_PRESENT", K0_JSON, "S13_hash")
    require(recomputed_components["S14_CONVERGENCE_CRITERION_EVALUATOR"], c20_hash, "STOP_VS2_5_CONVERGENCE_CRITERION_MISSING", K0_JSON, "S14_hash")

    v0 = up[V0_JSON]
    ms0 = up[MS0_JSON]
    expected_vocab = {
        "V2_OBSERVATIONS": vocab_ids(v0, "V2_OBSERVATIONS"),
        "V3_CONDITION_CLASSIFICATIONS": vocab_ids(v0, "V3_CONDITION_CLASSIFICATIONS"),
        "V4_VALIDATION_RESULTS": vocab_ids(v0, "V4_VALIDATION_RESULTS"),
        "V5_CANDIDATE_ADMISSIBILITY_RESULTS": vocab_ids(v0, "V5_CANDIDATE_ADMISSIBILITY_RESULTS"),
        "V6_CONVERGENCE_RESULTS": vocab_ids(v0, "V6_CONVERGENCE_RESULTS"),
        "V7_TERMINAL_OUTCOMES": vocab_ids(v0, "V7_TERMINAL_OUTCOMES"),
    }
    require(k0["frozen_auxiliary_vocabularies"], expected_vocab, "STOP_VS2_5_VALIDATION_VOCABULARY_DRIFT", K0_JSON, "frozen_auxiliary_vocabularies")
    require(c20["convergence_result_vocabulary"], expected_vocab["V6_CONVERGENCE_RESULTS"], "STOP_VS2_5_CONVERGENCE_VOCABULARY_DRIFT", C20_JSON, "convergence_result_vocabulary")
    require(k0["terminal_family"]["terminal_outcome_count"], 17, "STOP_VS2_5_TERMINAL_OUTCOME_FAMILY_DRIFT", K0_JSON, "terminal_outcome_count")
    require("STOP_BUDGET_EXHAUSTED" in expected_vocab["V7_TERMINAL_OUTCOMES"], False, "STOP_VS2_5_TERMINAL_OUTCOME_FAMILY_DRIFT", V0_JSON, "STOP_BUDGET_EXHAUSTED")
    require(k0["terminal_family"]["stop_budget_exhausted_present"], False, "STOP_VS2_5_TERMINAL_OUTCOME_FAMILY_DRIFT", K0_JSON, "stop_budget_exhausted_present")
    require(k0["move_space_binding"]["ordered_move_ids"], ms0["ordered_move_ids"], "STOP_VS2_5_MOVE_ENUMERATION_INCOMPLETE", K0_JSON, "ordered_move_ids")
    require(k0["move_space_binding"]["move_count"], 8, "STOP_VS2_5_MOVE_ENUMERATION_INCOMPLETE", K0_JSON, "move_count")

    expected_selector = [
        "discard moves not runtime-authorized",
        "enforce frozen dependencies",
        "retain moves directly addressing primary condition",
        "prefer smallest candidate write-set",
        "prefer lowest move cost",
        "break remaining ties by canonical move ID",
    ]
    require(k0["selector_policy"], expected_selector, "STOP_VS2_5_SELECTOR_NONDETERMINISTIC", K0_JSON, "selector_policy")
    require("CANDIDATE_SUCCESSOR_INTEGRITY_PASS" in k0["candidate_integrity_auxiliary_results"], True, "STOP_VS2_5_CANDIDATE_INTEGRITY_CONTRACT_MISSING", K0_JSON, "candidate_integrity_auxiliary_results")

    require(k0["m2_future_hash_bound"], False, "STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", K0_JSON, "m2_future_hash_bound")
    require(m2["controlled_step_package_reference"]["content_sha256"], k0_hash, "STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", M2_JSON, "controlled_step_package_reference.content_sha256")
    require(m2["m2_binds_k0_completed_hash"], True, "STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", M2_JSON, "m2_binds_k0_completed_hash")
    require(m2["k0_binds_m2_future_hash"], False, "STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", M2_JSON, "k0_binds_m2_future_hash")
    if m2_hash in json.dumps(k0["package_binding"]["package_payload"], sort_keys=True):
        stop("STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", K0_JSON, "m2_hash_in_k0_payload", "absent", "present")
    if receipt_hash in json.dumps(receipt["receipt_binding"]["receipt_payload"], sort_keys=True):
        stop("STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", RECEIPT_JSON, "receipt_self_hash_in_payload", "absent", "present")

    summary = m2["downstream_binding_summary"]
    require(summary["downstream_binding_count"], 8, "STOP_VS2_5_SUCCESSOR_BINDING_MANIFEST_MISSING", M2_JSON, "downstream_binding_count")
    require(summary["pending_binding_count"], 6, "STOP_VS2_5_SUCCESSOR_BINDING_MANIFEST_MISSING", M2_JSON, "pending_binding_count")
    require(summary["absent_by_policy_binding_count"], 2, "STOP_VS2_5_SUCCESSOR_BINDING_MANIFEST_MISSING", M2_JSON, "absent_by_policy_binding_count")
    require(summary["fabricated_future_reference_count"], 0, "STOP_VS2_5_SUCCESSOR_BINDING_MANIFEST_MISSING", M2_JSON, "fabricated_future_reference_count")
    for row in m2["downstream_bindings"]:
        verify_reference_nulls(row, M2_JSON)

    post = receipt["post_state"]
    for key, expected in {
        "bounded_construction_consumption_count_before": 1,
        "bounded_construction_consumption_count_after": 1,
        "bounded_construction_frame_completed_by_vs2_5": True,
        "bounded_construction_frame_open_after_vs2_5": False,
        "unconsumed_effective_grant_count": 3,
        "runtime_instance_created": False,
        "candidate_instance_created": False,
        "move_enumerated_against_live_candidate": False,
        "move_selected": False,
        "move_applied": False,
        "execution_performed": False,
        "sweep_executed": False,
        "runner_created": False,
        "vs2_6_may_begin": True,
    }.items():
        require(post.get(key), expected, "STOP_VS2_5_CONSTRUCTION_FRAME_SCOPE_DRIFT", RECEIPT_JSON, key)
    require(receipt["receipt_gate"], "VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_PASS", "STOP_VS2_5_HASH_GRAPH_OR_CANONICALIZATION_INVALID", RECEIPT_JSON, "receipt_gate")
    require(receipt["logical_terminal_transition"], "ADVANCE(VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS_PENDING)", "STOP_VS2_5_NEXT_UNIT_AUTO_EXECUTED", RECEIPT_JSON, "logical_terminal_transition")

    for md_path, json_path, digest in [
        (K0_MD, K0_JSON, k0_hash),
        (C20_MD, C20_JSON, c20_hash),
        (R13_MD, R13_JSON, r13_hash),
        (M2_MD, M2_JSON, m2_hash),
    ]:
        text = (ROOT / md_path).read_text(encoding="utf-8")
        artifact = load(json_path)
        require(artifact["artifact_id"] in text, True, "STOP_VS2_5_STEP_NOT_AUDITABLE", md_path, "artifact_id_projection")
        require(digest in text, True, "STOP_VS2_5_STEP_NOT_AUDITABLE", md_path, "canonical_hash_projection")

    return {
        "controlled_step_package_sha256": k0_hash,
        "convergence_criterion_contract_sha256": c20_hash,
        "receipt_and_atomic_publication_contract_sha256": r13_hash,
        "controlled_step_binding_manifest_sha256": m2_hash,
        "receipt_sha256": receipt_hash,
        "component_hashes": recomputed_components,
    }


def verify_forbidden_outputs() -> None:
    forbidden_paths = [
        "discussion_packets",
        "docs/matrixlabs/phase_vs2/fixtures",
        "docs/matrixlabs/phase_vs2/source_snapshots",
        "docs/matrixlabs/phase_vs2/runtime_instances",
        "docs/matrixlabs/phase_vs2/candidate_instances",
        "docs/matrixlabs/phase_vs2/sweeps",
        "docs/matrixlabs/phase_vs2/runners",
    ]
    present = [path for path in forbidden_paths if (ROOT / path).exists()]
    if present:
        stop("STOP_VS2_5_EXECUTION_OR_FIXTURE_DRIFT", "repo", "forbidden_outputs", [], present)


def emit_success(result: dict[str, Any]) -> None:
    output = {
        "gate": "VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_PASS",
        "controlled_step_package_sha256": result["controlled_step_package_sha256"],
        "convergence_criterion_contract_sha256": result["convergence_criterion_contract_sha256"],
        "receipt_and_atomic_publication_contract_sha256": result["receipt_and_atomic_publication_contract_sha256"],
        "controlled_step_binding_manifest_sha256": result["controlled_step_binding_manifest_sha256"],
        "receipt_sha256": result["receipt_sha256"],
        "component_count": len(result["component_hashes"]),
        "component_hashes": result["component_hashes"],
        "protected_upstream_files_unchanged": True,
        "runtime_or_fixture_drift": False,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


def emit_stop(exc: StopFailure) -> None:
    print("VERIFY_PHASE_VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_V0_STOP")
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
    try:
        verify_dirty_scope()
        up = verify_upstream()
        result = verify_generated(up)
        verify_forbidden_outputs()
        emit_success(result)
        return 0
    except StopFailure as exc:
        emit_stop(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
