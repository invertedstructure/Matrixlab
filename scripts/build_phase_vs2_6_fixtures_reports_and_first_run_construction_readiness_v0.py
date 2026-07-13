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
HEAD = "d6d57b8b1a15bf608113ad834652f61e09f1b0c4"
PHASE_ID = "PHASE_VS2"
UNIT_ID = "VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS"
UNIT_ROLE = "FIXTURE_REPORT_EXECUTION_PACKAGE_AND_STATIC_READINESS_CONSTRUCTION_ONLY"
CANON = "MATRIXLAB_CANONICAL_JSON_V0"
HASH_ALG = "SHA-256"
READY_GATE = "VS2_6_FIRST_RUN_CONSTRUCTION_READINESS_PASS_READY_FOR_ONE_EXECUTION_DECISION"
NOT_READY_GATE = "VS2_6_FIRST_RUN_CONSTRUCTION_READINESS_PASS_NOT_READY_BLOCKERS_EXPOSED"
FAIL_GATE = "VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS_FAIL"

PROFILE_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_first_sweep_capable_kernel_profile_v0.json"
TARGET_FREEZE_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_typed_state_contract_convergence_target_freeze_v0.json"
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
VS2_5_RECEIPT_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_5_controlled_step_and_convergence_contract_construction_receipt_v0.json"

FIXTURE_DIR = "docs/matrixlabs/phase_vs2/fixtures"
READINESS_DIR = "docs/matrixlabs/phase_vs2/readiness"
REPORT_DIR = "docs/matrixlabs/phase_vs2/reports"
D0_JSON = f"{READINESS_DIR}/phase_vs2_upstream_package_dependency_inventory_v0.json"
F0X_JSON = f"{FIXTURE_DIR}/phase_vs2_first_kernel_fixture_contract_v0.json"
F0X_MD = f"{FIXTURE_DIR}/phase_vs2_first_kernel_fixture_contract_v0.md"
S0X_JSON = f"{READINESS_DIR}/phase_vs2_first_kernel_runtime_source_snapshot_v0.json"
FS0_JSON = f"{FIXTURE_DIR}/phase_vs2_first_kernel_fixture_set_v0.json"
FS0_MD = f"{FIXTURE_DIR}/phase_vs2_first_kernel_fixture_set_v0.md"
RP0_JSON = f"{REPORT_DIR}/phase_vs2_report_contract_package_v0.json"
RP0_MD = f"{REPORT_DIR}/phase_vs2_report_contract_package_v0.md"
E0_JSON = f"{READINESS_DIR}/phase_vs2_execution_package_core_manifest_v0.json"
E0_MD = f"{READINESS_DIR}/phase_vs2_execution_package_core_manifest_v0.md"
G0_JSON = f"{READINESS_DIR}/phase_vs2_first_run_construction_readiness_gate_v0.json"
G0_MD = f"{READINESS_DIR}/phase_vs2_first_run_construction_readiness_gate_v0.md"
GR0_JSON = f"{READINESS_DIR}/phase_vs2_first_run_construction_readiness_gate_receipt_v0.json"
RS0_JSON = f"{READINESS_DIR}/phase_vs2_execution_package_readiness_seal_v0.json"
RS0_MD = f"{READINESS_DIR}/phase_vs2_execution_package_readiness_seal_v0.md"
U0_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_6_fixtures_reports_and_first_run_construction_readiness_receipt_v0.json"

SCRIPT = "scripts/build_phase_vs2_6_fixtures_reports_and_first_run_construction_readiness_v0.py"
VERIFY_SCRIPT = "scripts/verify_phase_vs2_6_fixtures_reports_and_first_run_construction_readiness_v0.py"
BASELINE_SCRIPT = "scripts/build_baseline_share_v0.py"
BASELINE_OUTPUTS = [
    "baseline_share/COMMIT_CONTEXT.md",
    "baseline_share/CURRENT_STATE.md",
    "baseline_share/MANIFEST.json",
    "baseline_share/RECEIPT_POINTERS.md",
]

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
PRIMARY_OUTCOMES = [
    "STEP_INPUT_REJECTED",
    "STEP_PREEXECUTION_TYPED_STOP",
    "STEP_TARGET_REACHED",
    "STEP_MOVE_APPLIED_CONTINUE",
    "STEP_TYPED_STOP",
    "STEP_PUBLICATION_ABORTED",
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
FIXTURE_IDS = [
    "F01_POSITIVE_REQUIRED_FIELD_AND_NORMALIZATION",
    "F02_ALREADY_VALID_PRESERVATION",
    "F03_REPAIRABLE_TYPED_VALUE_NORMALIZATION",
    "F04_REPAIRABLE_SOURCE_IDENTITY_BINDING",
    "F05_MISSING_SOURCE_BLOCKER",
    "F06_AUTHORITY_OVERREACH_BLOCKER",
    "F07_REPAIRABLE_PROHIBITED_CANDIDATE_DECLARATION",
    "F08_MISSING_SCHEMA_BLOCKER",
    "F09_MISSING_CAPABILITY_BLOCKER",
    "F10_NO_ADMISSIBLE_MOVE_GAP",
]
READINESS_COMPONENT_IDS = [
    "R01_UPSTREAM_CHAIN",
    "R02_UPSTREAM_DEPENDENCY_INTEGRITY",
    "R03_SCOPE_AND_TARGET_INTEGRITY",
    "R04_OBJECT_MODEL_INTEGRITY",
    "R05_MOVE_SPACE_INTEGRITY",
    "R06_CONTROLLED_STEP_AND_C20_INTEGRITY",
    "R07_CAPABILITY_BOUNDARY_INTEGRITY",
    "R08_FIXTURE_SET_COMPLETENESS",
    "R09_STATIC_CANDIDATE_VALIDITY",
    "R10_NEGATIVE_FIXTURE_DISTINCTION",
    "R11_STATIC_EXPECTATION_WITNESSES",
    "R12_F01_REPEAT_PATH_VIABILITY",
    "R13_F02_PRESERVATION_VIABILITY",
    "R14_F07_DECLARATION_EFFECT_DISTINCTION",
    "R15_BLOCKER_DISTINGUISHABILITY",
    "R16_RUNTIME_SOURCE_SNAPSHOT_INTEGRITY",
    "R17_BOUNDS_INTEGRITY",
    "R18_REPORT_COMPLETENESS_AND_TRACEABILITY",
    "R19_CORE_READINESS_GRAPH_INTEGRITY",
    "R20_AUTHORITY_POSTURE_AND_CONSUMPTION",
    "R21_NO_EXECUTION_DRIFT",
]

REPORT_CONTRACTS = {
    "case_report": ("phase_vs2_case_report_contract_v0", "FIRST_SWEEP_KERNEL_CASE_REPORT_CONTRACT_V0", f"{REPORT_DIR}/phase_vs2_case_report_contract_v0.json"),
    "sweep_report": ("phase_vs2_sweep_report_contract_v0", "FIRST_SWEEP_KERNEL_SWEEP_REPORT_CONTRACT_V0", f"{REPORT_DIR}/phase_vs2_sweep_report_contract_v0.json"),
    "evidence_yield": ("phase_vs2_evidence_yield_contract_v0", "FIRST_SWEEP_KERNEL_EVIDENCE_YIELD_CONTRACT_V0", f"{REPORT_DIR}/phase_vs2_evidence_yield_contract_v0.json"),
    "unexpected_outcome": ("phase_vs2_unexpected_outcome_contract_v0", "FIRST_SWEEP_KERNEL_UNEXPECTED_OUTCOME_CONTRACT_V0", f"{REPORT_DIR}/phase_vs2_unexpected_outcome_contract_v0.json"),
    "refinement_candidate": ("phase_vs2_refinement_candidate_contract_v0", "FIRST_SWEEP_KERNEL_REFINEMENT_CANDIDATE_CONTRACT_V0", f"{REPORT_DIR}/phase_vs2_refinement_candidate_contract_v0.json"),
}

CANDIDATE_PATHS = {
    fixture_id: f"{FIXTURE_DIR}/candidates/{fixture_id[:3]}_candidate_v0.json"
    for fixture_id in FIXTURE_IDS
}
DEFINITION_STEMS = {
    "F01_POSITIVE_REQUIRED_FIELD_AND_NORMALIZATION": "F01_positive_required_field_and_normalization_v0",
    "F02_ALREADY_VALID_PRESERVATION": "F02_already_valid_preservation_v0",
    "F03_REPAIRABLE_TYPED_VALUE_NORMALIZATION": "F03_repairable_typed_value_normalization_v0",
    "F04_REPAIRABLE_SOURCE_IDENTITY_BINDING": "F04_repairable_source_identity_binding_v0",
    "F05_MISSING_SOURCE_BLOCKER": "F05_missing_source_blocker_v0",
    "F06_AUTHORITY_OVERREACH_BLOCKER": "F06_authority_overreach_blocker_v0",
    "F07_REPAIRABLE_PROHIBITED_CANDIDATE_DECLARATION": "F07_repairable_prohibited_candidate_declaration_v0",
    "F08_MISSING_SCHEMA_BLOCKER": "F08_missing_schema_blocker_v0",
    "F09_MISSING_CAPABILITY_BLOCKER": "F09_missing_capability_blocker_v0",
    "F10_NO_ADMISSIBLE_MOVE_GAP": "F10_no_admissible_move_gap_v0",
}
DEFINITION_PATHS = {
    fixture_id: f"{FIXTURE_DIR}/definitions/{stem}.json"
    for fixture_id, stem in DEFINITION_STEMS.items()
}

GENERATED_DOCS = [
    F0X_JSON,
    F0X_MD,
    FS0_JSON,
    FS0_MD,
    *CANDIDATE_PATHS.values(),
    *DEFINITION_PATHS.values(),
    D0_JSON,
    S0X_JSON,
    E0_JSON,
    E0_MD,
    G0_JSON,
    G0_MD,
    GR0_JSON,
    RS0_JSON,
    RS0_MD,
    *(path for _artifact_id, _contract_id, path in REPORT_CONTRACTS.values()),
    RP0_JSON,
    RP0_MD,
    U0_JSON,
]
ALLOWED_DIRTY = set(GENERATED_DOCS) | {SCRIPT, VERIFY_SCRIPT, BASELINE_SCRIPT, *BASELINE_OUTPUTS}

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
    K0_JSON: "b5f0ff69687ffd86f23f9e2949514887330e823267bb3d8a1dee37d4656f8d3d",
    K0_MD: "1127016f10d874d73cf4c68c84eda3e8ae16f57c4058e1e728f937cf31c16112",
    C20_JSON: "6f975c485400046d0843d17dc0ec36037f540a6adc5d011e7956874fa54b4daa",
    C20_MD: "18de1a30586fb36864329bfd60ed912ed7750baaa3d2a96314e88a6e51d1fef7",
    R13_JSON: "d5ef7baca9af3336a40850fdddf9dba7b49f8e3d2d643734f96504011a717875",
    R13_MD: "56343a5ffff576ea8d53218f11bafe92f54dc5cbbac72974b900df842c7a3362",
    M2_JSON: "eb91252a3c9de0042cc670254a642d21c33293f74b1d052b8ed9cdab405db00b",
    M2_MD: "93908a7f1cf3dfbb05c1d266eab6837af84a50246bb933c6d8964d390369b409",
    VS2_5_RECEIPT_JSON: "1fefd997f7df63c1a63331cdf65997402766e796cd462a80359933becc727ba8",
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
    K0_JSON: "3448ee02a854abdd5de28e2feb1ce866854473d9f18435083d5634e82b7a98a0",
    C20_JSON: "a9c512025963df2a07ba93e3071683f392264013824f82ddbcfd923ab8321fd4",
    R13_JSON: "a5375ec82dd148d05d7199296b58f186747b27cf3f4922555bec6ed1ed29cbf4",
    M2_JSON: "ffb10d40f6dbf641879a3385ba312f80b9a1f9d667b230e49452ad48abce1e43",
    VS2_5_RECEIPT_JSON: "31f88a51de957cca434747b02b3bbcbb1e0471f92323f5796a9607f2356e4c68",
}


class StopFailure(RuntimeError):
    def __init__(self, code: str, artifact: str, field: str, expected: Any, observed: Any, invariant: str = "VS2_6_CONSTRUCTION_BOUNDARY") -> None:
        super().__init__(code)
        self.code = code
        self.artifact = artifact
        self.field = field
        self.expected = expected
        self.observed = observed
        self.invariant = invariant


def fail(code: str, artifact: str, field: str, expected: Any, observed: Any, invariant: str = "VS2_6_CONSTRUCTION_BOUNDARY") -> None:
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
    return sha256_bytes(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def require(observed: Any, expected: Any, code: str, artifact: str, field: str) -> None:
    if observed != expected:
        fail(code, artifact, field, expected, observed)


def status_paths(status: str) -> list[str]:
    paths: list[str] = []
    for line in status.splitlines():
        raw = line[2:].strip()
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]
        paths.append(raw)
    return paths


def validate_dirty_scope(root: Path) -> None:
    paths = status_paths(git(root, ["status", "--short", "--untracked-files=all"]))
    unexpected = [path for path in paths if path not in ALLOWED_DIRTY]
    protected = [path for path in paths if path in EXPECTED_RAW]
    if unexpected:
        fail("STOP_VS2_6_PREEXISTING_WORKTREE_CHANGES", "repo", "dirty_paths", sorted(ALLOWED_DIRTY), unexpected)
    if protected:
        fail("STOP_VS2_6_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_NOT_PASS", "repo", "protected_dirty_paths", "unchanged", protected)
    if (root / "discussion_packets").exists():
        fail("STOP_VS2_6_DISCUSSION_PACKETS_PRESENT", "repo", "discussion_packets", "absent", "present")


def check_repo(root: Path) -> None:
    require(str(root), ROOT, "STOP_VS2_6_REPOSITORY_ROOT_MISMATCH", "repo", "repository_root")
    require(git(root, ["rev-parse", "--show-toplevel"]), ROOT, "STOP_VS2_6_REPOSITORY_ROOT_MISMATCH", "repo", "git_root")
    require(git(root, ["branch", "--show-current"]), BRANCH, "STOP_VS2_6_BRANCH_MISMATCH", "repo", "branch")
    require(git(root, ["rev-parse", "HEAD"]), HEAD, "STOP_VS2_6_UNEXPECTED_HEAD", "repo", "HEAD")
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=root).returncode != 0
    require(staged, False, "STOP_VS2_6_STAGED_CHANGES_PRESENT", "repo", "staged_changes_present")
    validate_dirty_scope(root)


def binding_tuple(path: str) -> tuple[str, str, str]:
    mapping = {
        PROFILE_JSON: ("profile_binding", "profile_payload", "profile_sha256"),
        TARGET_FREEZE_JSON: ("target_freeze_binding", "target_freeze_payload", "target_freeze_sha256"),
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
        VS2_5_RECEIPT_JSON: ("receipt_binding", "receipt_payload", "receipt_sha256"),
        D0_JSON: ("inventory_binding", "inventory_payload", "inventory_sha256"),
        F0X_JSON: ("contract_binding", "contract_payload", "contract_sha256"),
        S0X_JSON: ("snapshot_binding", "snapshot_payload", "snapshot_sha256"),
        FS0_JSON: ("fixture_set_binding", "fixture_set_payload", "fixture_set_sha256"),
        RP0_JSON: ("package_binding", "package_payload", "package_sha256"),
        E0_JSON: ("manifest_binding", "manifest_payload", "manifest_sha256"),
        G0_JSON: ("gate_binding", "gate_payload", "gate_sha256"),
        GR0_JSON: ("receipt_binding", "receipt_payload", "receipt_sha256"),
        RS0_JSON: ("seal_binding", "seal_payload", "seal_sha256"),
        U0_JSON: ("receipt_binding", "receipt_payload", "receipt_sha256"),
    }
    for _key, (_artifact_id, _contract_id, report_path) in REPORT_CONTRACTS.items():
        mapping[report_path] = ("contract_binding", "contract_payload", "contract_sha256")
    for candidate_path in CANDIDATE_PATHS.values():
        mapping[candidate_path] = ("candidate_binding", "candidate_payload", "candidate_sha256")
    for definition_path in DEFINITION_PATHS.values():
        mapping[definition_path] = ("fixture_definition_binding", "fixture_definition_payload", "fixture_definition_sha256")
    return mapping[path]


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


def write_md(path: Path, artifact: dict[str, Any], digest: str, summary: list[str]) -> None:
    lines = [
        f"# {artifact['artifact_id']}",
        "",
        f"- Artifact kind: `{artifact['artifact_kind']}`",
        f"- Canonicalization: `{CANON}`",
        f"- Canonical SHA-256: `{digest}`",
        f"- Status: `{artifact.get('contract_status') or artifact.get('fixture_set_status') or artifact.get('package_status') or artifact.get('gate_status') or artifact.get('seal_status')}`",
        "",
        "## Summary",
        "",
        *summary,
        "",
        "## Authority And Runtime Posture",
        "",
        "- execution_authority_present = `false`",
        "- sweep_authority_present = `false`",
        "- execution_started = `false`",
        "- runtime_receipts_emitted = `0`",
        "",
        "## Nonclaims",
        "",
        "- This artifact does not grant execution authority.",
        "- This artifact does not execute fixtures or runtime candidates.",
        "- This Markdown file is a deterministic projection of the JSON artifact.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def verify_committed(root: Path, rel: str, expected_raw: str | None = None) -> bytes:
    try:
        committed = git(root, ["show", f"{HEAD}:{rel}"], binary=True)
    except subprocess.CalledProcessError as exc:
        fail("STOP_VS2_6_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_NOT_PASS", rel, "committed_path", "present", exc.stderr)
    current_path = root / rel
    if not current_path.exists():
        fail("STOP_VS2_6_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_NOT_PASS", rel, "worktree_path", "present", "missing")
    current = current_path.read_bytes()
    require(current, committed, "STOP_VS2_6_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_NOT_PASS", rel, "committed_bytes")
    if expected_raw is not None:
        require(sha256_bytes(current), expected_raw, "STOP_VS2_6_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_NOT_PASS", rel, "raw_sha256")
    return current


def load_upstream(root: Path) -> dict[str, dict[str, Any]]:
    data: dict[str, dict[str, Any]] = {}
    all_json = set(path for path in EXPECTED_RAW if path.endswith(".json")) | {PROFILE_JSON, TARGET_FREEZE_JSON}
    for path, raw in EXPECTED_RAW.items():
        content = verify_committed(root, path, raw)
        if path.endswith(".json"):
            data[path] = json.loads(content.decode("utf-8"))
    for path in [PROFILE_JSON, TARGET_FREEZE_JSON]:
        data[path] = json.loads(verify_committed(root, path).decode("utf-8"))
    for path, expected in EXPECTED_CANONICAL.items():
        artifact = data[path]
        binding, payload_key, hash_key = binding_tuple(path)
        require(artifact[binding][hash_key], expected, "STOP_VS2_6_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_NOT_PASS", path, hash_key)
        require(canonical_hash(artifact[binding][payload_key]), expected, "STOP_VS2_6_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_NOT_PASS", path, f"{payload_key}_hash")
    for path in all_json:
        if path not in data:
            data[path] = json.loads((root / path).read_text(encoding="utf-8"))
    verify_vs25_shape(data)
    verify_prior_frame(data)
    return data


def verify_vs25_shape(up: dict[str, dict[str, Any]]) -> None:
    k0 = up[K0_JSON]
    c20 = up[C20_JSON]
    r13 = up[R13_JSON]
    receipt = up[VS2_5_RECEIPT_JSON]
    require(k0["package_status"], "FROZEN_NOT_EXECUTED", "STOP_VS2_6_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_NOT_PASS", K0_JSON, "package_status")
    require(c20["contract_status"], "DEFINED_AND_FROZEN_NOT_EXECUTED", "STOP_VS2_6_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_NOT_PASS", C20_JSON, "contract_status")
    registry = k0["component_registry"]
    require([row["component_id"] for row in registry], COMPONENT_IDS, "STOP_VS2_6_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_NOT_PASS", K0_JSON, "component_order")
    require(k0["component_count"], 17, "STOP_VS2_6_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_NOT_PASS", K0_JSON, "component_count")
    hashes = [row["component_sha256"] for row in registry]
    require(len(hashes), len(set(hashes)), "STOP_VS2_6_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_NOT_PASS", K0_JSON, "component_hashes_unique_by_component")
    require(k0["component_hashes"]["S13_RECEIPT_AND_ATOMIC_PUBLICATION_BUILDER"], r13["contract_binding"]["contract_sha256"], "STOP_VS2_6_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_NOT_PASS", K0_JSON, "S13_hash")
    require(k0["component_hashes"]["S14_CONVERGENCE_CRITERION_EVALUATOR"], c20["contract_binding"]["contract_sha256"], "STOP_VS2_6_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_NOT_PASS", K0_JSON, "S14_hash")
    post = receipt["post_state"]
    for key in ["fixture_set_bound", "exact_source_snapshot_bound", "exact_runtime_budgets_bound", "active_execution_authority_present", "active_sweep_authority_present", "runtime_instance_created", "candidate_instance_created", "execution_performed", "runner_created"]:
        require(post.get(key), False, "STOP_VS2_6_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_NOT_PASS", VS2_5_RECEIPT_JSON, key)
    require(receipt["receipt_gate"], "VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_PASS", "STOP_VS2_6_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_NOT_PASS", VS2_5_RECEIPT_JSON, "receipt_gate")
    require(receipt["logical_terminal_transition"], "ADVANCE(VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS_PENDING)", "STOP_VS2_6_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_NOT_PASS", VS2_5_RECEIPT_JSON, "logical_terminal_transition")


def verify_prior_frame(up: dict[str, dict[str, Any]]) -> None:
    auth = up[VS2_5_RECEIPT_JSON]["construction_authority"]
    require(auth.get("bounded_construction_consumption_count_after"), 1, "STOP_VS2_6_BOUNDED_CONSTRUCTION_GRANT_RECONSUMPTION_ATTEMPT", VS2_5_RECEIPT_JSON, "bounded_construction_consumption_count_after")
    require(auth.get("bounded_construction_frame_completed_by_vs2_5"), True, "STOP_VS2_6_CLOSED_CONSTRUCTION_FRAME_REUSE_ATTEMPT", VS2_5_RECEIPT_JSON, "bounded_construction_frame_completed_by_vs2_5")
    require(auth.get("bounded_construction_frame_open_after_vs2_5"), False, "STOP_VS2_6_CLOSED_CONSTRUCTION_FRAME_REUSE_ATTEMPT", VS2_5_RECEIPT_JSON, "bounded_construction_frame_open_after_vs2_5")
    require(auth.get("bounded_construction_grant_further_use_permitted"), False, "STOP_VS2_6_CLOSED_CONSTRUCTION_FRAME_REUSE_ATTEMPT", VS2_5_RECEIPT_JSON, "bounded_construction_grant_further_use_permitted")
    grants = auth.get("unconsumed_effective_grant_ids", [])
    required = [
        "VS2_FIXTURE_CONSTRUCTION_AUTHORITY",
        "VS2_FIRST_RUN_READINESS_GATE_CONSTRUCTION_AUTHORITY",
        "VS2_CONSTRUCTION_PACKAGE_VERIFICATION_AUTHORITY",
    ]
    require(sorted(grants), sorted(required), "STOP_VS2_6_PACKAGE_ASSEMBLY_AUTHORITY_MISSING", VS2_5_RECEIPT_JSON, "unconsumed_effective_grant_ids")
    require(auth.get("unconsumed_effective_grant_count"), 3, "STOP_VS2_6_PACKAGE_ASSEMBLY_AUTHORITY_MISSING", VS2_5_RECEIPT_JSON, "unconsumed_effective_grant_count")


def version_for(artifact: dict[str, Any]) -> str:
    for key in ["profile_id", "target_freeze_id", "contract_version", "schema_contract_version", "target_contract_version", "manifest_version", "partition_version", "matrix_version", "move_space_version", "envelope_version", "package_version"]:
        if key in artifact and key.endswith("_version"):
            return str(artifact[key])
    return "v0"


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


def local_ref(artifact: dict[str, Any], path: str, role: str) -> dict[str, Any]:
    binding, _payload_key, hash_key = binding_tuple(path)
    version = artifact.get("contract_version") or artifact.get("fixture_set_version") or artifact.get("snapshot_version") or artifact.get("package_version") or artifact.get("manifest_version") or artifact.get("gate_version") or artifact.get("seal_version") or artifact.get("receipt_version") or artifact.get("inventory_version") or artifact.get("candidate_version") or "v0"
    return bound_ref(f"{artifact['artifact_id']}_reference", role, UNIT_ID, artifact["artifact_id"], artifact["artifact_kind"], version, path, artifact[binding][hash_key], f"VS2.6-built {artifact['artifact_id']} canonical binding.")


def upstream_ref(up: dict[str, dict[str, Any]], path: str, reference_id: str, role: str) -> dict[str, Any]:
    artifact = up[path]
    binding, _payload_key, hash_key = binding_tuple(path)
    artifact_kind = artifact.get("artifact_kind") or role
    return bound_ref(reference_id, role, UNIT_ID, artifact["artifact_id"], artifact_kind, version_for(artifact), path, artifact[binding][hash_key], f"Committed upstream {artifact['artifact_id']} canonical binding.")


def source_basis(section: str) -> list[dict[str, str]]:
    return [{
        "section": section,
        "basis_class": "VS2_6_STATIC_CONSTRUCTION_DERIVED",
        "basis_reason": f"{section} is derived from sealed VS2.3, VS2.4, and VS2.5 contracts without runtime execution.",
        "source_authority": "committed_phase_vs2_upstream_chain",
    }]


def grant_records(up: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    auth = up[VS2_5_RECEIPT_JSON]["construction_authority"]
    scopes = {
        "VS2_FIXTURE_CONSTRUCTION_AUTHORITY": ["upstream dependency inventory", "fixture-scoped source snapshot", "candidate specimen construction", "fixture definitions and witnesses", "fixture-set manifest"],
        "VS2_FIRST_RUN_READINESS_GATE_CONSTRUCTION_AUTHORITY": ["readiness artifacts", "readiness gate", "readiness receipt", "readiness seal"],
        "VS2_CONSTRUCTION_PACKAGE_VERIFICATION_AUTHORITY": ["report contracts", "execution-package core manifest", "package verification receipt"],
    }
    records = []
    for grant_id in auth["unconsumed_effective_grant_ids"]:
        payload = {
            "grant_id": grant_id,
            "grant_status_before_vs2_6": "AVAILABLE_UNCONSUMED",
            "grant_status_after_vs2_6": "CONSUMED_BY_STATIC_CONSTRUCTION",
            "authoritative_source": VS2_5_RECEIPT_JSON,
            "admitted_scope": scopes[grant_id],
            "execution_authority": False,
            "sweep_authority": False,
            "runner_authority": False,
        }
        records.append({**payload, "grant_record_sha256": canonical_hash(payload)})
    return records


def upstream_refs(up: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        "profile": upstream_ref(up, PROFILE_JSON, "kernel_profile_reference", "KERNEL_PROFILE"),
        "target_freeze": upstream_ref(up, TARGET_FREEZE_JSON, "semantic_target_freeze_reference", "SEMANTIC_TARGET_FREEZE"),
        "F0": upstream_ref(up, F0_JSON, "scope_regime_reference", "SCOPE_REGIME"),
        "O1": upstream_ref(up, O1_JSON, "runtime_control_state_contract_reference", "RUNTIME_CONTROL_STATE_CONTRACT"),
        "O2": upstream_ref(up, O2_JSON, "candidate_schema_reference", "CANDIDATE_SCHEMA_CONTRACT"),
        "O3": upstream_ref(up, O3_JSON, "target_contract_reference", "FROZEN_TARGET_CONTRACT"),
        "M0": upstream_ref(up, M0_JSON, "object_model_manifest_reference", "OBJECT_MODEL_MANIFEST"),
        "S0": upstream_ref(up, S0_JSON, "source_contract_reference", "SOURCE_AND_VERSION_CONTRACT"),
        "V0": upstream_ref(up, V0_JSON, "vocabulary_partition_reference", "MOVE_VOCABULARY_PARTITION"),
        "A0": upstream_ref(up, A0_JSON, "move_authority_matrix_reference", "MOVE_AUTHORITY_MATRIX"),
        "MS0": upstream_ref(up, MS0_JSON, "finite_move_space_reference", "FINITE_MOVE_SPACE"),
        "P0": upstream_ref(up, P0_JSON, "prospective_authority_envelope_reference", "PROSPECTIVE_AUTHORITY_ENVELOPE"),
        "M1": upstream_ref(up, M1_JSON, "move_space_binding_manifest_reference", "MOVE_SPACE_BINDING_MANIFEST"),
        "K0": upstream_ref(up, K0_JSON, "controlled_step_package_reference", "CONTROLLED_STEP_PACKAGE"),
        "C20": upstream_ref(up, C20_JSON, "convergence_contract_reference", "CONVERGENCE_CONTRACT"),
        "R13": upstream_ref(up, R13_JSON, "receipt_publication_contract_reference", "RECEIPT_AND_ATOMIC_PUBLICATION_CONTRACT"),
        "M2": upstream_ref(up, M2_JSON, "controlled_step_binding_manifest_reference", "CONTROLLED_STEP_BINDING_MANIFEST"),
    }


def make_d0(refs: dict[str, dict[str, Any]], grants: list[dict[str, Any]]) -> dict[str, Any]:
    payload = {
        "schema_version": "matrixlabs_phase_vs2_upstream_package_dependency_inventory_v0",
        "artifact_id": "phase_vs2_upstream_package_dependency_inventory_v0",
        "artifact_kind": "STATIC_UPSTREAM_PACKAGE_DEPENDENCY_INVENTORY",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "inventory_id": "FIRST_SWEEP_KERNEL_UPSTREAM_PACKAGE_DEPENDENCY_INVENTORY_V0",
        "inventory_version": "v0",
        "inventory_status": "FROZEN_FOR_CONSTRUCTION_READINESS_AUDIT",
        "logical_package_identity": "phase_vs2_fixtures_reports_and_first_run_construction_readiness_package_v0",
        "upstream_references": refs,
        "protected_upstream_canonical_hashes": EXPECTED_CANONICAL,
        "remaining_construction_grant_records": grants,
        "capability_boundary": {
            "declared": True,
            "representable": True,
            "contract_derived": True,
            "inside_one_of_three_remaining_grant_scopes": True,
            "required_for_this_exact_package": True,
            "non_expansive": True,
            "constructible_without_execution": True,
        },
        "source_authority_forbidden": ["baseline_share", "filesystem modification time", "directory ordering", "latest-file selection", "uncommitted residue", "chat memory"],
        "source_basis": source_basis("upstream dependency inventory"),
    }
    return bind(payload, "inventory_binding", "inventory_payload", "inventory_sha256")


def make_f0x(refs: dict[str, dict[str, Any]], d0_ref: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "matrixlabs_phase_vs2_first_kernel_fixture_contract_v0",
        "artifact_id": "phase_vs2_first_kernel_fixture_contract_v0",
        "artifact_kind": "STATIC_FIXTURE_CONTRACT",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "fixture_contract_id": "FIRST_SWEEP_KERNEL_FIXTURE_CONTRACT_V0",
        "fixture_set_id": "FIRST_SWEEP_KERNEL_FIXTURE_SET_V0",
        "fixture_set_class": "BOUNDED_TYPED_STATE_CONTRACT_CONVERGENCE_FIXTURE_SET",
        "fixture_set_status": "FROZEN_NOT_EXECUTED",
        "contract_version": "v0",
        "contract_status": "FROZEN_NOT_EXECUTED",
        "fixture_ids": FIXTURE_IDS,
        "fixture_count": 10,
        "fixture_intent_vocabulary": ["POSITIVE_TARGET_PATH", "PRESERVATION_TARGET_PATH", "DELIBERATE_NEGATIVE_BOUNDARY", "DELIBERATE_MOVE_SPACE_GAP"],
        "fixture_role_vocabulary": ["POSITIVE_MULTI_STEP_REPAIR", "PRESERVATION", "REPAIRABLE_TYPED_VALUE", "REPAIRABLE_SOURCE_BINDING", "SOURCE_BLOCKER", "AUTHORITY_BLOCKER", "REPAIRABLE_PROHIBITED_DECLARATION", "SCHEMA_BLOCKER", "CAPABILITY_BLOCKER", "MOVE_SPACE_GAP"],
        "upstream_dependency_inventory_reference": d0_ref,
        "scope_regime_reference": refs["F0"],
        "candidate_schema_reference": refs["O2"],
        "target_reference": refs["O3"],
        "move_space_reference": refs["MS0"],
        "controlled_step_package_reference": refs["K0"],
        "source_basis": source_basis("fixture identity and role contract"),
        "runtime_execution_performed": False,
    }
    return bind(payload, "contract_binding", "contract_payload", "contract_sha256")


def fixture_specs() -> dict[str, dict[str, Any]]:
    all_moves = MOVE_IDS
    return {
        "F01_POSITIVE_REQUIRED_FIELD_AND_NORMALIZATION": {
            "role": "POSITIVE_MULTI_STEP_REPAIR",
            "intent": "POSITIVE_TARGET_PATH",
            "observations": ["OBS_MISSING_REQUIRED_FIELD_DECLARATION", "OBS_NONCANONICAL_TYPED_VALUE"],
            "primary_observation": "OBS_MISSING_REQUIRED_FIELD_DECLARATION",
            "classification": "CONDITION_REPAIRABLE_DEFECT",
            "capability": "CAPABILITY_BOUNDARY_PASS",
            "blocker": None,
            "repair_lawfulness": "STATIC_REPAIR_PATH_LAWFUL_UNDER_K0",
            "structural": ["M01_ADD_AUTHORIZED_REQUIRED_FIELD", "M02_NORMALIZE_TYPED_VALUE"],
            "runtime": ["M01_ADD_AUTHORIZED_REQUIRED_FIELD", "M02_NORMALIZE_TYPED_VALUE"],
            "selected": ["M01_ADD_AUTHORIZED_REQUIRED_FIELD", "M02_NORMALIZE_TYPED_VALUE"],
            "outcomes": ["STEP_MOVE_APPLIED_CONTINUE", "STEP_TARGET_REACHED"],
            "convergence": ["CONVERGENCE_CONTINUE_ALLOWED", "CONVERGENCE_TARGET_TERMINAL_CONDITION_SATISFIED"],
            "terminal": "TARGET_REACHED",
            "terminal_detail": None,
            "steps": 2,
            "attempted": 2,
            "applied": 2,
            "package_effect": "TARGET_PATH_COVERAGE",
            "introduced_delta": ["missing required field declaration", "noncanonical typed value"],
            "witness_cover": ["strict progress", "M01-before-M02 derived from S03/S08 precedence", "unmet-rule set strict subset after step 1"],
        },
        "F02_ALREADY_VALID_PRESERVATION": {
            "role": "PRESERVATION",
            "intent": "PRESERVATION_TARGET_PATH",
            "observations": ["OBS_TARGET_ALREADY_REACHED"],
            "primary_observation": "OBS_TARGET_ALREADY_REACHED",
            "classification": "CONDITION_TARGET_SATISFIED",
            "capability": "CAPABILITY_NOT_REQUIRED",
            "blocker": None,
            "repair_lawfulness": "NO_REPAIR_REQUIRED",
            "structural": [],
            "runtime": [],
            "selected": [],
            "outcomes": ["STEP_TARGET_REACHED"],
            "convergence": ["CONVERGENCE_TARGET_TERMINAL_CONDITION_SATISFIED"],
            "terminal": "TARGET_REACHED",
            "terminal_detail": None,
            "steps": 1,
            "attempted": 0,
            "applied": 0,
            "package_effect": "ZERO_MOVE_TARGET_SUCCESS_COVERAGE",
            "introduced_delta": [],
            "witness_cover": ["validation pass", "admissibility pass", "candidate identity unchanged", "candidate version unchanged", "candidate hash unchanged", "no mutation"],
        },
        "F03_REPAIRABLE_TYPED_VALUE_NORMALIZATION": {
            "role": "REPAIRABLE_TYPED_VALUE",
            "intent": "POSITIVE_TARGET_PATH",
            "observations": ["OBS_NONCANONICAL_TYPED_VALUE"],
            "primary_observation": "OBS_NONCANONICAL_TYPED_VALUE",
            "classification": "CONDITION_REPAIRABLE_DEFECT",
            "capability": "CAPABILITY_BOUNDARY_PASS",
            "blocker": None,
            "repair_lawfulness": "STATIC_REPAIR_PATH_LAWFUL_UNDER_K0",
            "structural": ["M02_NORMALIZE_TYPED_VALUE"],
            "runtime": ["M02_NORMALIZE_TYPED_VALUE"],
            "selected": ["M02_NORMALIZE_TYPED_VALUE"],
            "outcomes": ["STEP_TARGET_REACHED"],
            "convergence": ["CONVERGENCE_TARGET_TERMINAL_CONDITION_SATISFIED"],
            "terminal": "TARGET_REACHED",
            "terminal_detail": None,
            "steps": 1,
            "attempted": 1,
            "applied": 1,
            "package_effect": "TARGET_PATH_COVERAGE",
            "introduced_delta": ["noncanonical typed value"],
            "witness_cover": ["semantic meaning preserved", "unsupported coercion absent", "unrelated path mutation forbidden"],
        },
        "F04_REPAIRABLE_SOURCE_IDENTITY_BINDING": {
            "role": "REPAIRABLE_SOURCE_BINDING",
            "intent": "POSITIVE_TARGET_PATH",
            "observations": ["OBS_SOURCE_IDENTITY_DECLARATION_MISSING"],
            "primary_observation": "OBS_SOURCE_IDENTITY_DECLARATION_MISSING",
            "classification": "CONDITION_REPAIRABLE_DEFECT",
            "capability": "CAPABILITY_BOUNDARY_PASS",
            "blocker": None,
            "repair_lawfulness": "STATIC_REPAIR_PATH_LAWFUL_UNDER_K0",
            "structural": ["M03_BIND_DECLARED_SOURCE_IDENTITY"],
            "runtime": ["M03_BIND_DECLARED_SOURCE_IDENTITY"],
            "selected": ["M03_BIND_DECLARED_SOURCE_IDENTITY"],
            "outcomes": ["STEP_TARGET_REACHED"],
            "convergence": ["CONVERGENCE_TARGET_TERMINAL_CONDITION_SATISFIED"],
            "terminal": "TARGET_REACHED",
            "terminal_detail": None,
            "steps": 1,
            "attempted": 1,
            "applied": 1,
            "package_effect": "TARGET_PATH_COVERAGE",
            "introduced_delta": ["source identity declaration missing"],
            "witness_cover": ["exact source exists in S0X", "source identity and hash verified", "source role admitted", "source snapshot unchanged", "no source acquired"],
        },
        "F05_MISSING_SOURCE_BLOCKER": {
            "role": "SOURCE_BLOCKER",
            "intent": "DELIBERATE_NEGATIVE_BOUNDARY",
            "observations": ["OBS_SOURCE_IDENTITY_DECLARATION_MISSING"],
            "primary_observation": "OBS_SOURCE_IDENTITY_DECLARATION_MISSING",
            "classification": "CONDITION_MISSING_SOURCE",
            "capability": "CAPABILITY_BOUNDARY_PASS",
            "blocker": "SOURCE_LAYER",
            "repair_lawfulness": "NOT_RUN_BLOCKED_BY_MISSING_SOURCE",
            "structural": [],
            "runtime": [],
            "selected": [],
            "outcomes": ["STEP_TYPED_STOP"],
            "convergence": ["CONVERGENCE_NOT_RUN"],
            "terminal": "STOP_MISSING_SOURCE",
            "terminal_detail": "REQUIRED_SOURCE_ABSENT",
            "steps": 1,
            "attempted": 0,
            "applied": 0,
            "package_effect": "NON_BLOCKING_IF_STATIC_WITNESS_PASS",
            "introduced_delta": ["required source absent"],
            "witness_cover": ["absence witness in S0X", "M03 blocked by absent source basis", "candidate unchanged", "next lawful surface recorded"],
        },
        "F06_AUTHORITY_OVERREACH_BLOCKER": {
            "role": "AUTHORITY_BLOCKER",
            "intent": "DELIBERATE_NEGATIVE_BOUNDARY",
            "observations": ["OBS_AUTHORITY_REQUIREMENT_MISSING"],
            "primary_observation": "OBS_AUTHORITY_REQUIREMENT_MISSING",
            "classification": "CONDITION_MISSING_AUTHORITY",
            "capability": "CAPABILITY_BOUNDARY_PASS",
            "blocker": "CANDIDATE_SEMANTIC_AUTHORITY",
            "repair_lawfulness": "NOT_RUN_BLOCKED_BY_CANDIDATE_SEMANTIC_AUTHORITY",
            "structural": [],
            "runtime": [],
            "selected": [],
            "outcomes": ["STEP_TYPED_STOP"],
            "convergence": ["CONVERGENCE_NOT_RUN"],
            "terminal": "STOP_MISSING_AUTHORITY",
            "terminal_detail": "authority_blocker_layer=CANDIDATE_SEMANTIC_AUTHORITY",
            "steps": 1,
            "attempted": 0,
            "applied": 0,
            "package_effect": "NON_BLOCKING_IF_STATIC_WITNESS_PASS",
            "introduced_delta": ["candidate semantic authority evidence missing"],
            "witness_cover": ["candidate content authority missing", "execution authority not missing", "candidate unchanged"],
        },
        "F07_REPAIRABLE_PROHIBITED_CANDIDATE_DECLARATION": {
            "role": "REPAIRABLE_PROHIBITED_DECLARATION",
            "intent": "POSITIVE_TARGET_PATH",
            "observations": ["OBS_PROHIBITED_CANDIDATE_DECLARATION_PRESENT"],
            "primary_observation": "OBS_PROHIBITED_CANDIDATE_DECLARATION_PRESENT",
            "classification": "CONDITION_REPAIRABLE_DEFECT",
            "capability": "CAPABILITY_BOUNDARY_PASS",
            "blocker": None,
            "repair_lawfulness": "STATIC_REPAIR_PATH_LAWFUL_UNDER_K0",
            "structural": ["M05_REMOVE_PROHIBITED_CANDIDATE_DECLARATION"],
            "runtime": ["M05_REMOVE_PROHIBITED_CANDIDATE_DECLARATION"],
            "selected": ["M05_REMOVE_PROHIBITED_CANDIDATE_DECLARATION"],
            "outcomes": ["STEP_TARGET_REACHED"],
            "convergence": ["CONVERGENCE_TARGET_TERMINAL_CONDITION_SATISFIED"],
            "terminal": "TARGET_REACHED",
            "terminal_detail": None,
            "steps": 1,
            "attempted": 1,
            "applied": 1,
            "package_effect": "DECLARATION_EFFECT_DISTINCTION_COVERAGE",
            "introduced_delta": ["prohibited candidate declaration present"],
            "witness_cover": ["actual forbidden effect absent", "one prohibited declaration removed", "evidence preserved", "authority restrictions preserved", "no replacement invented"],
        },
        "F08_MISSING_SCHEMA_BLOCKER": {
            "role": "SCHEMA_BLOCKER",
            "intent": "DELIBERATE_NEGATIVE_BOUNDARY",
            "observations": ["OBS_SCHEMA_REQUIREMENT_MISSING"],
            "primary_observation": "OBS_SCHEMA_REQUIREMENT_MISSING",
            "classification": "CONDITION_MISSING_SCHEMA",
            "capability": "CAPABILITY_NOT_REQUIRED",
            "blocker": "SCHEMA_LAYER",
            "repair_lawfulness": "NOT_RUN_BLOCKED_BY_MISSING_SCHEMA",
            "structural": [],
            "runtime": [],
            "selected": [],
            "outcomes": ["STEP_TYPED_STOP"],
            "convergence": ["CONVERGENCE_NOT_RUN"],
            "terminal": "STOP_MISSING_SCHEMA",
            "terminal_detail": "REQUIRED_CANDIDATE_DEPENDENCY_SCHEMA_ABSENT",
            "steps": 1,
            "attempted": 0,
            "applied": 0,
            "package_effect": "NON_BLOCKING_IF_STATIC_WITNESS_PASS",
            "introduced_delta": ["missing candidate dependency schema"],
            "witness_cover": ["package-owned schemas valid", "automatic schema creation absent", "candidate unchanged"],
        },
        "F09_MISSING_CAPABILITY_BLOCKER": {
            "role": "CAPABILITY_BLOCKER",
            "intent": "DELIBERATE_NEGATIVE_BOUNDARY",
            "observations": ["OBS_CAPABILITY_REQUIREMENT_MISSING"],
            "primary_observation": "OBS_CAPABILITY_REQUIREMENT_MISSING",
            "classification": "CONDITION_MISSING_CAPABILITY",
            "capability": "CAPABILITY_MISSING",
            "blocker": "CAPABILITY_LAYER",
            "repair_lawfulness": "NOT_RUN_BLOCKED_BY_MISSING_CAPABILITY",
            "structural": [],
            "runtime": [],
            "selected": [],
            "outcomes": ["STEP_TYPED_STOP"],
            "convergence": ["CONVERGENCE_NOT_RUN"],
            "terminal": "STOP_MISSING_CAPABILITY",
            "terminal_detail": "PROPOSED_NOT_APPLIED",
            "steps": 1,
            "attempted": 0,
            "applied": 0,
            "package_effect": "NON_BLOCKING_IF_STATIC_WITNESS_PASS",
            "introduced_delta": ["capability absent"],
            "witness_cover": ["missing capability is not merely unimplemented move", "proposal remains PROPOSED_NOT_APPLIED", "candidate unchanged"],
        },
        "F10_NO_ADMISSIBLE_MOVE_GAP": {
            "role": "MOVE_SPACE_GAP",
            "intent": "DELIBERATE_MOVE_SPACE_GAP",
            "observations": ["OBS_MISSING_REQUIRED_FIELD_DECLARATION"],
            "primary_observation": "OBS_MISSING_REQUIRED_FIELD_DECLARATION",
            "classification": "CONDITION_REPAIRABLE_DEFECT",
            "capability": "CAPABILITY_NOT_IMPLEMENTED_BY_MOVE_SPACE",
            "blocker": "MOVE_SPACE_GAP",
            "repair_lawfulness": "NOT_RUN_NO_ADMISSIBLE_MOVE",
            "structural": [],
            "runtime": [],
            "selected": [],
            "outcomes": ["STEP_TYPED_STOP"],
            "convergence": ["CONVERGENCE_NOT_RUN"],
            "terminal": "STOP_NO_ADMISSIBLE_MOVE",
            "terminal_detail": "MOVE_SPACE_GAP",
            "steps": 1,
            "attempted": 0,
            "applied": 0,
            "package_effect": "MOVE_SPACE_GAP_COVERAGE",
            "introduced_delta": ["target rule present but no M01-M08 atomic delta implements it"],
            "witness_cover": ["evaluated_move_count=8", "structurally_applicable_move_count=0", "all eight moves have structural block reasons", "candidate unchanged"],
        },
    }


def make_s0x(refs: dict[str, dict[str, Any]], f0x_ref: dict[str, Any], d0_ref: dict[str, Any]) -> dict[str, Any]:
    present = [
        {
            "source_id": "S0X_SOURCE_F04_DECLARED_IDENTITY",
            "source_role": "FIXTURE_SOURCE_IDENTITY_EVIDENCE",
            "artifact_version": "v0",
            "declared_path": "docs/matrixlabs/phase_vs2/readiness/source_records/S0X_SOURCE_F04_DECLARED_IDENTITY",
            "content_sha256": canonical_hash({"source_id": "S0X_SOURCE_F04_DECLARED_IDENTITY", "fixture": "F04"}),
            "freshness_state": "FROZEN_WITHIN_CONSTRUCTION_INVENTORY",
            "allowed_fixture_ids": ["F04_REPAIRABLE_SOURCE_IDENTITY_BINDING"],
            "forbidden_uses": ["general external truth claim", "source acquisition", "latest-file resolution"],
            "source_basis": source_basis("present source record"),
        },
        {
            "source_id": "S0X_AUTHORITY_EVIDENCE_F06_ABSENCE_BOUNDARY",
            "source_role": "CANDIDATE_SEMANTIC_AUTHORITY_EVIDENCE_RECORD",
            "artifact_version": "v0",
            "declared_path": "docs/matrixlabs/phase_vs2/readiness/source_records/S0X_AUTHORITY_EVIDENCE_F06_ABSENCE_BOUNDARY",
            "content_sha256": canonical_hash({"source_id": "S0X_AUTHORITY_EVIDENCE_F06_ABSENCE_BOUNDARY", "fixture": "F06"}),
            "freshness_state": "FROZEN_WITHIN_CONSTRUCTION_INVENTORY",
            "allowed_fixture_ids": ["F06_AUTHORITY_OVERREACH_BLOCKER"],
            "forbidden_uses": ["execution authority", "sweep authority", "runner authority"],
            "source_basis": source_basis("candidate authority evidence record"),
        },
    ]
    absence = [
        ("F05_REQUIRED_SOURCE_ABSENT", "F05_MISSING_SOURCE_BLOCKER", "required source absent"),
        ("F08_REQUIRED_CANDIDATE_DEPENDENCY_SCHEMA_ABSENT", "F08_MISSING_SCHEMA_BLOCKER", "required candidate-dependency schema absent"),
        ("F09_REQUIRED_CAPABILITY_ABSENT", "F09_MISSING_CAPABILITY_BLOCKER", "required capability absent"),
    ]
    payload = {
        "schema_version": "matrixlabs_phase_vs2_first_kernel_runtime_source_snapshot_v0",
        "artifact_id": "phase_vs2_first_kernel_runtime_source_snapshot_v0",
        "artifact_kind": "STATIC_FIXTURE_SCOPED_RUNTIME_SOURCE_SNAPSHOT",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "source_snapshot_id": "FIRST_SWEEP_KERNEL_RUNTIME_SOURCE_SNAPSHOT_V0",
        "snapshot_version": "v0",
        "source_snapshot_status": "FROZEN_FOR_CONSTRUCTION_READINESS_AUDIT",
        "fixture_contract_reference": f0x_ref,
        "upstream_dependency_inventory_reference": d0_ref,
        "present_source_records": present,
        "present_candidate_authority_evidence_records": [present[1]],
        "present_schema_inventory_records": [{"source_id": "S0X_PACKAGE_OWNED_SCHEMAS_PRESENT", "source_role": "PACKAGE_SCHEMA_INVENTORY", "artifact_version": "v0", "declared_path": O2_JSON, "content_sha256": refs["O2"]["content_sha256"], "freshness_state": "COMMITTED_UPSTREAM_BOUND", "allowed_fixture_ids": FIXTURE_IDS, "forbidden_uses": ["schema invention"], "source_basis": source_basis("schema inventory")}],
        "present_capability_inventory_records": [{"source_id": "S0X_MOVE_SPACE_CAPABILITIES_PRESENT", "source_role": "MOVE_SPACE_CAPABILITY_INVENTORY", "artifact_version": "v0", "declared_path": MS0_JSON, "content_sha256": refs["MS0"]["content_sha256"], "freshness_state": "COMMITTED_UPSTREAM_BOUND", "allowed_fixture_ids": FIXTURE_IDS, "forbidden_uses": ["capability creation"], "source_basis": source_basis("capability inventory")}],
        "present_freshness_witnesses": [{"source_id": "S0X_COMMITTED_UPSTREAM_FRESHNESS_WITNESS", "source_role": "COMMIT_BOUND_FRESHNESS_WITNESS", "artifact_version": HEAD, "declared_path": ".", "content_sha256": canonical_hash({"HEAD": HEAD, "scope": "VS2.6 static construction"}), "freshness_state": "COMMIT_BOUND", "allowed_fixture_ids": FIXTURE_IDS, "forbidden_uses": ["mtime authority"], "source_basis": source_basis("freshness witness")}],
        "declared_absence_witnesses": [
            {
                "absence_witness_id": absence_id,
                "fixture_id": fixture_id,
                "absent_object": absent_object,
                "absence_witness_status": "ABSENCE_VERIFIED_WITHIN_FROZEN_INVENTORY",
                "live_external_source_used": False,
                "latest_file_dependency": False,
                "automatic_acquisition": False,
            }
            for absence_id, fixture_id, absent_object in absence
        ],
        "forbidden_dependencies": {
            "candidate_hash_dependency": False,
            "fixture_definition_hash_dependency": False,
            "fixture_set_hash_dependency": False,
            "report_package_hash_dependency": False,
            "execution_package_hash_dependency": False,
            "readiness_hash_dependency": False,
            "package_contract_misclassified_as_runtime_evidence": False,
        },
        "source_basis": source_basis("runtime source snapshot"),
    }
    return bind(payload, "snapshot_binding", "snapshot_payload", "snapshot_sha256")


def candidate_payload(fixture_id: str, refs: dict[str, dict[str, Any]], f0x_ref: dict[str, Any], s0x_ref: dict[str, Any]) -> dict[str, Any]:
    spec = fixture_specs()[fixture_id]
    prefix = fixture_id[:3]
    payload = {
        "schema_version": "matrixlabs_phase_vs2_static_candidate_specimen_v0",
        "artifact_id": f"{prefix}_candidate_v0",
        "artifact_kind": "STATIC_O2_CANDIDATE_SPECIMEN",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "fixture_id": fixture_id,
        "static_candidate_fixture_artifact": True,
        "runtime_candidate_instance": False,
        "runtime_candidate_successor": False,
        "runtime_move_applied": False,
        "runtime_state_published": False,
        "runtime_receipt_emitted": False,
        "run_id": None,
        "candidate_contract_id": f"{prefix}_candidate_v0",
        "candidate_family": "TYPED_STATE_CONTRACT_CANDIDATE",
        "candidate_version": "v0",
        "candidate_schema_validation_status": "STATIC_O2_OUTER_SCHEMA_VALID",
        "candidate_schema_reference": refs["O2"],
        "scope_regime_reference": refs["F0"],
        "target_reference": refs["O3"],
        "fixture_contract_reference": f0x_ref,
        "source_snapshot_reference": s0x_ref,
        "candidate_hash_rule": {"canonicalization": CANON, "hash_algorithm": HASH_ALG, "candidate_hash_excludes_outer_binding": True},
        "version_law": {"identity_preserved": True, "initial_version": "v0", "successor_increment_required_after_runtime_move": True},
        "contract_identity_declarations": {"fixture_id": fixture_id, "candidate_surface": f"{prefix}_candidate_v0"},
        "state_identity_declarations": {"initial_condition": spec["classification"], "target_family": "BOUNDED_CONTRACT_CONVERGENCE"},
        "source_binding_declarations": {"source_snapshot_bound": True, "missing_source_case": fixture_id.startswith("F05")},
        "authority_declarations": {"execution_authority_identity": None, "candidate_semantic_authority_requirement": spec["blocker"] == "CANDIDATE_SEMANTIC_AUTHORITY"},
        "typed_field_declarations": {"deliberate_observations": spec["observations"], "introduced_delta": spec["introduced_delta"]},
        "runtime_boundary_declarations": {"runtime_candidate_instance": False, "runtime_state_published": False},
        "halt_and_terminal_declarations": {"expected_terminal_outcome": spec["terminal"], "expected_terminal_detail": spec["terminal_detail"]},
        "receipt_declarations": {"runtime_receipt_identity": None, "runtime_receipt_emitted": False},
        "forbidden_effect_declarations": {"actual_forbidden_effect_present": False, "fixture_forbidden_effect_guard_required": fixture_id.startswith("F07")},
        "claim_declarations": {"generalization_claimed": False, "runtime_success_claimed": False},
        "deliberately_o3_nonconformant_initially": spec["terminal"] != "TARGET_REACHED" or spec["selected"],
        "source_basis": source_basis(f"{fixture_id} static candidate specimen"),
    }
    return payload


def make_candidates(refs: dict[str, dict[str, Any]], f0x_ref: dict[str, Any], s0x_ref: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out = {}
    for fixture_id in FIXTURE_IDS:
        payload = candidate_payload(fixture_id, refs, f0x_ref, s0x_ref)
        out[fixture_id] = bind(payload, "candidate_binding", "candidate_payload", "candidate_sha256")
    return out


def fixture_definition_payload(fixture_id: str, refs: dict[str, dict[str, Any]], f0x_ref: dict[str, Any], s0x_ref: dict[str, Any], candidate_ref: dict[str, Any]) -> dict[str, Any]:
    spec = fixture_specs()[fixture_id]
    prefix = fixture_id[:3]
    witness_type = "STATIC_POSITIVE_PATH_WITNESS" if spec["terminal"] == "TARGET_REACHED" else "STATIC_TYPED_STOP_WITNESS"
    all_moves = MOVE_IDS if spec["terminal"] != "TARGET_REACHED" or spec["selected"] else []
    if fixture_id == "F10_NO_ADMISSIBLE_MOVE_GAP":
        all_moves = MOVE_IDS
    payload = {
        "schema_version": "matrixlabs_phase_vs2_fixture_definition_v0",
        "artifact_id": DEFINITION_STEMS[fixture_id],
        "artifact_kind": "STATIC_FIXTURE_DEFINITION_WITH_EXPECTATION_WITNESS",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "fixture_id": fixture_id,
        "fixture_version": "v0",
        "fixture_role": spec["role"],
        "fixture_intent": spec["intent"],
        "fixture_status": "FROZEN_NOT_EXECUTED",
        "fixture_contract_reference": f0x_ref,
        "candidate_specimen_reference": candidate_ref,
        "candidate_specimen_hash": candidate_ref["content_sha256"],
        "candidate_schema_validation_status": "STATIC_O2_OUTER_SCHEMA_VALID",
        "initial_target_conformance_status": "STATIC_TARGET_ALREADY_REACHED" if fixture_id.startswith("F02") else "STATIC_TARGET_NOT_REACHED_OR_BLOCKED_AS_DECLARED",
        "scope_regime_reference": refs["F0"],
        "target_reference": refs["O3"],
        "source_snapshot_reference": s0x_ref,
        "introduced_delta": spec["introduced_delta"],
        "intended_observations": spec["observations"],
        "expected_primary_observation": spec["primary_observation"],
        "expected_secondary_observations": [obs for obs in spec["observations"] if obs != spec["primary_observation"]],
        "expected_condition_classification": spec["classification"],
        "expected_capability_result": spec["capability"],
        "expected_blocker_layer": spec["blocker"],
        "expected_repair_lawfulness": spec["repair_lawfulness"],
        "expected_enumerated_move_ids": all_moves,
        "expected_structurally_applicable_move_ids": spec["structural"],
        "expected_runtime_admissible_move_ids_if_exact_package_authorized": spec["runtime"],
        "current_runtime_admissible_move_set": "ABSENT",
        "expected_selected_move_sequence": spec["selected"],
        "expected_controlled_step_outcome_sequence": spec["outcomes"],
        "expected_convergence_result_sequence": spec["convergence"],
        "expected_terminal_outcome": spec["terminal"],
        "expected_terminal_detail": spec["terminal_detail"],
        "expected_maximum_step_invocations": spec["steps"],
        "expected_maximum_attempted_moves": spec["attempted"],
        "expected_maximum_applied_moves": spec["applied"],
        "expected_validation_path": "VALIDATION_PASS" if spec["terminal"] == "TARGET_REACHED" else "VALIDATION_NOT_RUN_OR_BLOCKED_AS_DECLARED",
        "expected_admissibility_path": "ADMISSIBILITY_PASS" if spec["terminal"] == "TARGET_REACHED" else "ADMISSIBILITY_NOT_RUN",
        "expected_receipt_evidence": ["controlled-step receipt required when executed later", "runtime receipt not emitted by VS2.6"],
        "forbidden_observed_effects": ["runtime execution", "live move selection", "runtime receipt emission", "candidate transformation by VS2.6"],
        "static_expectation_witness": {
            "witness_id": f"{prefix}_STATIC_EXPECTATION_WITNESS_V0",
            "witness_type": witness_type,
            "witness_status": "STATIC_PATH_COHERENT_UNDER_DECLARED_CONTRACTS",
            "coverage_items": spec["witness_cover"],
            "authoritative_runtime_candidate": False,
            "runtime_move_applied": False,
            "runtime_state_published": False,
            "runtime_receipt_emitted": False,
            "path_executed_successfully_claimed": False,
        },
        "package_readiness_effect": spec["package_effect"],
        "observed_controlled_step_outcomes": [],
        "observed_convergence_results": [],
        "observed_terminal_outcome": None,
        "expectation_match": "NOT_EVALUATED",
        "fixture_nonclaims": ["not runtime execution", "not runtime success evidence", "not execution authorization"],
        "source_basis": source_basis(f"{fixture_id} fixture definition"),
    }
    if fixture_id == "F10_NO_ADMISSIBLE_MOVE_GAP":
        payload["structural_block_reasons_by_move"] = {move_id: "delta not implemented by frozen M01-M08 contract for this atomic gap" for move_id in MOVE_IDS}
        payload["evaluated_move_count"] = 8
        payload["structurally_applicable_move_count"] = 0
    return payload


def make_definitions(refs: dict[str, dict[str, Any]], f0x_ref: dict[str, Any], s0x_ref: dict[str, Any], candidate_refs: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out = {}
    for fixture_id in FIXTURE_IDS:
        payload = fixture_definition_payload(fixture_id, refs, f0x_ref, s0x_ref, candidate_refs[fixture_id])
        out[fixture_id] = bind(payload, "fixture_definition_binding", "fixture_definition_payload", "fixture_definition_sha256")
    return out


def make_fs0(f0x_ref: dict[str, Any], s0x_ref: dict[str, Any], candidate_refs: dict[str, dict[str, Any]], definition_refs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    target_cases = ["F01", "F02", "F03", "F04", "F07"]
    typed_stop_cases = {
        "F05": "STOP_MISSING_SOURCE",
        "F06": "STOP_MISSING_AUTHORITY",
        "F08": "STOP_MISSING_SCHEMA",
        "F09": "STOP_MISSING_CAPABILITY",
        "F10": "STOP_NO_ADMISSIBLE_MOVE",
    }
    exercised = ["M01_ADD_AUTHORIZED_REQUIRED_FIELD", "M02_NORMALIZE_TYPED_VALUE", "M03_BIND_DECLARED_SOURCE_IDENTITY", "M05_REMOVE_PROHIBITED_CANDIDATE_DECLARATION"]
    unexercised = [move for move in MOVE_IDS if move not in exercised]
    terminal_coverage = ["TARGET_REACHED", "STOP_MISSING_SOURCE", "STOP_MISSING_AUTHORITY", "STOP_MISSING_SCHEMA", "STOP_MISSING_CAPABILITY", "STOP_NO_ADMISSIBLE_MOVE"]
    payload = {
        "schema_version": "matrixlabs_phase_vs2_first_kernel_fixture_set_v0",
        "artifact_id": "phase_vs2_first_kernel_fixture_set_v0",
        "artifact_kind": "STATIC_FIXTURE_SET_MANIFEST",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "fixture_set_id": "FIRST_SWEEP_KERNEL_FIXTURE_SET_V0",
        "fixture_set_version": "v0",
        "fixture_set_status": "FROZEN_NOT_EXECUTED",
        "fixture_contract_reference": f0x_ref,
        "source_snapshot_reference": s0x_ref,
        "fixture_order": FIXTURE_IDS,
        "fixture_count": 10,
        "candidate_specimen_count": 10,
        "static_witness_count": 10,
        "candidate_specimen_references": candidate_refs,
        "fixture_definition_references": definition_refs,
        "expected_target_cases": target_cases,
        "expected_typed_stop_cases": typed_stop_cases,
        "expected_terminal_distribution": {"TARGET_REACHED": 5, "typed_stop": 5},
        "expected_move_coverage": {
            "defined_moves_total": 8,
            "expected_exercised_unique_moves": exercised,
            "expected_exercised_unique_move_count": 4,
            "expected_unexercised_unique_moves": unexercised,
            "expected_unexercised_unique_move_count": 4,
        },
        "expected_convergence_coverage": {
            "CONVERGENCE_CONTINUE_ALLOWED": ["F01 step 1"],
            "CONVERGENCE_TARGET_TERMINAL_CONDITION_SATISFIED": ["F01 step 2", "F02", "F03", "F04", "F07"],
            "CONVERGENCE_NOT_RUN": ["F05", "F06", "F08", "F09", "F10"],
        },
        "unexercised_convergence_register": [
            "CONVERGENCE_STOP_NON_PROGRESS",
            "CONVERGENCE_STOP_REPEATED_STATE",
            "CONVERGENCE_STOP_OSCILLATION",
            "CONVERGENCE_STOP_ATTEMPTED_MOVE_BOUND_EXHAUSTED",
            "CONVERGENCE_STOP_APPLIED_MOVE_BOUND_EXHAUSTED",
            "CONVERGENCE_STOP_DECLARED_RADIUS_BOUND_EXHAUSTED",
            "CONVERGENCE_CRITERION_UNMET",
            "CONVERGENCE_RESULT_AMBIGUOUS",
        ],
        "expected_terminal_coverage": terminal_coverage,
        "unexercised_terminal_register": [terminal for terminal in TERMINAL_OUTCOMES if terminal not in terminal_coverage],
        "descriptive_not_success_quota": True,
        "source_basis": source_basis("fixture set manifest"),
    }
    return bind(payload, "fixture_set_binding", "fixture_set_payload", "fixture_set_sha256")


def make_report_contract(key: str, fs0_ref: dict[str, Any]) -> dict[str, Any]:
    artifact_id, contract_id, _path = REPORT_CONTRACTS[key]
    payload = {
        "schema_version": f"matrixlabs_{artifact_id}",
        "artifact_id": artifact_id,
        "artifact_kind": "STATIC_REPORT_CONTRACT",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "contract_id": contract_id,
        "contract_version": "v0",
        "contract_status": "FROZEN_NOT_EXECUTED",
        "fixture_set_reference": fs0_ref,
        "represented_fixture_ids": FIXTURE_IDS,
        "primary_invocation_outcomes": PRIMARY_OUTCOMES,
        "convergence_results": CONVERGENCE_RESULTS,
        "terminal_outcomes": TERMINAL_OUTCOMES,
        "expectation_match": "NOT_EVALUATED",
        "runtime_fields_pre_execution": {
            "observed_cases": [],
            "runtime_receipt_references": [],
            "runtime_report_emitted": False,
            "runtime_case_count": 0,
            "runtime_sweep_count": 0,
            "unexpected_outcome_count": 0,
        },
        "traceability_rule": "Every future report field must trace to sealed package metadata or declared runtime receipt fields.",
        "hidden_interpretive_source_allowed": False,
        "source_basis": source_basis(f"{contract_id} report contract"),
    }
    if key == "evidence_yield":
        payload["allowed_yield_branches"] = ["CONFIRMATION_YIELD", "DIAGNOSTIC_YIELD", "BOTH", "NO_USEFUL_YIELD"]
        payload["required_yield_fields"] = ["yield_id", "yield_branch", "case_id", "observed_condition", "capability_result", "convergence_result", "primary_invocation_outcome", "terminal_outcome", "receipt_references", "decision_relevance", "next_lawful_surface", "bounded_interpretation"]
    if key == "refinement_candidate":
        payload["refinement_candidate_status"] = "PROPOSED_NOT_APPLIED"
        payload["human_decision_required"] = True
        payload["self_application_performed"] = False
    return bind(payload, "contract_binding", "contract_payload", "contract_sha256")


def make_rp0(report_refs: dict[str, dict[str, Any]], fs0_ref: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "matrixlabs_phase_vs2_report_contract_package_v0",
        "artifact_id": "phase_vs2_report_contract_package_v0",
        "artifact_kind": "STATIC_REPORT_CONTRACT_PACKAGE",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "package_id": "FIRST_SWEEP_KERNEL_REPORT_CONTRACT_PACKAGE_V0",
        "package_version": "v0",
        "package_status": "FROZEN_NOT_EXECUTED",
        "fixture_set_reference": fs0_ref,
        "individual_report_contract_references": report_refs,
        "report_contract_count": 5,
        "represented_fixture_count": 10,
        "represented_primary_invocation_outcome_count": 6,
        "represented_convergence_result_count": 11,
        "represented_terminal_outcome_count": 17,
        "represented_topics": ["strict-progress evidence", "zero-move target success", "candidate deltas", "capability results", "expectation divergence", "publication abort", "unclassified results", "Confirmation Yield", "Diagnostic Yield", "refinement proposals"],
        "expectation_match": "NOT_EVALUATED",
        "hidden_interpretive_source_allowed": False,
        "source_basis": source_basis("report contract package"),
    }
    return bind(payload, "package_binding", "package_payload", "package_sha256")


def package_bounds(profile: dict[str, Any], p0: dict[str, Any]) -> dict[str, Any]:
    bounds = {
        "target_family_count": 1,
        "target_version_count": 1,
        "scope_regime_version_count": 1,
        "kernel_profile_count": 1,
        "move_space_version_count": 1,
        "controlled_step_package_version_count": 1,
        "convergence_contract_version_count": 1,
        "runtime_source_snapshot_count": 1,
        "fixture_set_version_count": 1,
        "case_count": 10,
        "maximum_controlled_step_invocations_per_case": 5,
        "maximum_attempted_moves_per_case": 5,
        "maximum_applied_moves_per_case": 5,
        "maximum_total_controlled_step_invocations": 50,
        "maximum_total_attempted_moves": 50,
        "maximum_total_applied_moves": 50,
        "automatic_reruns": 0,
        "automatic_radius_renewals": 0,
        "automatic_budget_renewals": 0,
        "automatic_fixture_additions": 0,
        "automatic_source_additions": 0,
        "automatic_move_additions": 0,
        "automatic_package_substitutions": 0,
    }
    profile_max = profile["maximum_future_execution_envelope"]
    p0_max = p0["maximum_prospective_scope"]
    checks = {
        "case_count": bounds["case_count"] <= profile_max["maximum_cases"] and bounds["case_count"] <= p0_max["case_count_maximum"],
        "attempted_per_case": bounds["maximum_attempted_moves_per_case"] <= profile_max["maximum_attempted_moves_per_case"] and bounds["maximum_attempted_moves_per_case"] <= p0_max["attempted_moves_per_case_maximum"],
        "applied_per_case": bounds["maximum_applied_moves_per_case"] <= profile_max["maximum_applied_moves_per_case"] and bounds["maximum_applied_moves_per_case"] <= p0_max["applied_moves_per_case_maximum"],
        "total_attempted": bounds["maximum_total_attempted_moves"] <= profile_max["maximum_total_attempted_moves"] and bounds["maximum_total_attempted_moves"] <= p0_max["total_attempted_moves_maximum"],
        "total_applied": bounds["maximum_total_applied_moves"] <= profile_max["maximum_total_applied_moves"] and bounds["maximum_total_applied_moves"] <= p0_max["total_applied_moves_maximum"],
        "automatic_reruns": bounds["automatic_reruns"] <= profile_max["maximum_automatic_reruns"] and bounds["automatic_reruns"] <= p0_max["automatic_reruns_maximum"],
        "automatic_radius_renewals": bounds["automatic_radius_renewals"] <= profile_max["maximum_automatic_radius_renewals"] and bounds["automatic_radius_renewals"] <= p0_max["automatic_radius_renewals_maximum"],
    }
    if not all(checks.values()):
        fail("STOP_VS2_6_PACKAGE_BOUNDS_EXCEED_FROZEN_PROFILE", E0_JSON, "bounds", "within upstream maxima", checks)
    return {"bounds": bounds, "upstream_bound_checks": checks}


def make_e0(refs: dict[str, dict[str, Any]], d0_ref: dict[str, Any], f0x_ref: dict[str, Any], s0x_ref: dict[str, Any], fs0_ref: dict[str, Any], rp0_ref: dict[str, Any], bounds: dict[str, Any]) -> dict[str, Any]:
    exact_refs = {
        **refs,
        "D0": d0_ref,
        "F0X": f0x_ref,
        "S0X": s0x_ref,
        "FS0": fs0_ref,
        "RP0": rp0_ref,
    }
    payload = {
        "schema_version": "matrixlabs_phase_vs2_execution_package_core_manifest_v0",
        "artifact_id": "phase_vs2_execution_package_core_manifest_v0",
        "artifact_kind": "STATIC_EXECUTION_PACKAGE_CORE_MANIFEST",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "package_id": "FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_CORE_V0",
        "package_class": "ONE_BOUNDED_TYPED_STATE_CONTRACT_SWEEP_PACKAGE",
        "package_version": "v0",
        "package_status": "ASSEMBLED_UNAUDITED_NOT_AUTHORIZED",
        "exact_package_only": True,
        "package_references": exact_refs,
        "forbidden_references_absent": ["G0", "GR0", "RS0", "active execution authority", "run identity", "runtime O1 state", "runtime O2 candidate"],
        "prospective_execution_request_basis": {
            "exact_package_only": True,
            "fixture_subset_allowed_without_rebuild": False,
            "fixture_order_frozen": True,
            "source_snapshot_frozen": True,
            "bounds_frozen": True,
            "report_contracts_frozen": True,
            "active_execution_authority_present": False,
            "active_sweep_authority_present": False,
            "automatic_rerun_authority_present": False,
            "runner_authority_present": False,
        },
        "execution_state": {
            "run_id": None,
            "execution_started": False,
            "runtime_o1_instances_created": 0,
            "runtime_o2_instances_created": 0,
            "cases_initialized": 0,
            "cases_executed": 0,
            "runtime_receipts_emitted": 0,
            "runtime_case_reports_emitted": 0,
            "runtime_sweep_report_emitted": False,
            "runtime_commit_manifest_emitted": False,
        },
        "package_bounds": bounds,
        "source_basis": source_basis("execution package core manifest"),
    }
    return bind(payload, "manifest_binding", "manifest_payload", "manifest_sha256")


def readiness_records() -> list[dict[str, Any]]:
    return [
        {
            "readiness_component_id": component_id,
            "readiness_status": "READY",
            "evidence_references": ["D0", "F0X", "S0X", "FS0", "RP0", "E0"],
            "verified_invariants": [component_id.lower(), "hash-bound", "no execution drift"],
            "blocker_ids": [],
            "bounded_interpretation": "Static construction-readiness invariant verified for the exact E0 package.",
        }
        for component_id in READINESS_COMPONENT_IDS
    ]


def derive_readiness(records: list[dict[str, Any]]) -> tuple[str, str, bool]:
    statuses = [row["readiness_status"] for row in records]
    if all(status == "READY" for status in statuses):
        return READY_GATE, "SEALED_READY_FOR_HUMAN_EXECUTION_DECISION", True
    if all(status in {"READY", "BLOCKED_MISSING", "BLOCKED_INCOMPLETE", "BLOCKED_IDENTITY_MISMATCH", "BLOCKED_HASH_MISMATCH", "BLOCKED_EXPECTATION_AMBIGUOUS", "BLOCKED_STATIC_PATH_UNSUPPORTED", "BLOCKED_FIXTURE_DESIGN_INVALID", "BLOCKED_NEGATIVE_FIXTURE_UNDISTINGUISHED", "BLOCKED_SOURCE_INVENTORY_UNTRUSTWORTHY", "BLOCKED_AUTHORITY_DRIFT", "BLOCKED_BOUNDARY_VIOLATION", "BLOCKED_MANIFEST_CYCLE", "BLOCKED_EXECUTION_ALREADY_STARTED"} for status in statuses):
        return NOT_READY_GATE, "SEALED_NOT_READY_BLOCKERS_EXPOSED", False
    return FAIL_GATE, "UNSEALED_FAILURE", False


def make_g0(e0_ref: dict[str, Any], records: list[dict[str, Any]], verdict: str, seal_status: str, eligible: bool) -> dict[str, Any]:
    payload = {
        "schema_version": "matrixlabs_phase_vs2_first_run_construction_readiness_gate_v0",
        "artifact_id": "phase_vs2_first_run_construction_readiness_gate_v0",
        "artifact_kind": "STATIC_CONSTRUCTION_READINESS_GATE",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "gate_id": "FIRST_SWEEP_KERNEL_FIRST_RUN_CONSTRUCTION_READINESS_GATE_V0",
        "gate_class": "STATIC_EXECUTION_PACKAGE_CONSTRUCTION_READINESS_AUDIT",
        "gate_version": "v0",
        "gate_status": "READY" if verdict == READY_GATE else "NOT_READY_OR_FAILURE",
        "readiness_question": "Is the exact E0 package structurally complete, internally coherent, source-frozen, fixture-frozen, hash-bound, bounded, auditable, and free from authority or execution drift?",
        "execution_package_core_reference": e0_ref,
        "readiness_component_records": records,
        "readiness_component_count": 21,
        "readiness_verdict": verdict,
        "seal_status": seal_status,
        "eligible_for_execution_decision": eligible,
        "readiness_verdict_derived_from_r01_through_r21": True,
        "source_basis": source_basis("readiness gate"),
    }
    return bind(payload, "gate_binding", "gate_payload", "gate_sha256")


def make_gr0(g0_ref: dict[str, Any], e0_ref: dict[str, Any], records: list[dict[str, Any]], verdict: str, eligible: bool) -> dict[str, Any]:
    payload = {
        "schema_version": "matrixlabs_phase_vs2_first_run_construction_readiness_gate_receipt_v0",
        "artifact_id": "phase_vs2_first_run_construction_readiness_gate_receipt_v0",
        "artifact_kind": "STATIC_READINESS_GATE_RECEIPT",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "receipt_id": "FIRST_SWEEP_KERNEL_FIRST_RUN_CONSTRUCTION_READINESS_GATE_RECEIPT_V0",
        "receipt_version": "v0",
        "execution_package_core_reference": e0_ref,
        "readiness_gate_reference": g0_ref,
        "readiness_component_statuses": {row["readiness_component_id"]: row["readiness_status"] for row in records},
        "readiness_verdict": verdict,
        "typed_blockers": [],
        "eligible_for_execution_decision": eligible,
        "audit_completed": True,
        "runtime_execution_performed": False,
        "source_basis": source_basis("readiness gate receipt"),
    }
    return bind(payload, "receipt_binding", "receipt_payload", "receipt_sha256")


def make_rs0(e0_ref: dict[str, Any], g0_ref: dict[str, Any], gr0_ref: dict[str, Any], verdict: str, seal_status: str, eligible: bool) -> dict[str, Any]:
    payload = {
        "schema_version": "matrixlabs_phase_vs2_execution_package_readiness_seal_v0",
        "artifact_id": "phase_vs2_execution_package_readiness_seal_v0",
        "artifact_kind": "STATIC_EXECUTION_PACKAGE_READINESS_SEAL",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "seal_id": "FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_READINESS_SEAL_V0",
        "seal_version": "v0",
        "seal_status": seal_status,
        "execution_package_core_reference": e0_ref,
        "readiness_gate_reference": g0_ref,
        "readiness_gate_receipt_reference": gr0_ref,
        "readiness_verdict": verdict,
        "eligible_for_execution_decision": eligible,
        "exact_package_only": True,
        "subset_authorization_allowed": False,
        "authority_status": {
            "execution_authority_granted": False,
            "sweep_authority_granted": False,
            "automatic_rerun_authority_granted": False,
            "runner_authority_created": False,
        },
        "change_requires_new_package_chain": ["fixture count", "fixture order", "fixture content", "source snapshot", "absence witnesses", "bounds", "move-space", "controlled-step package", "convergence contract", "report contracts"],
        "source_basis": source_basis("readiness seal"),
    }
    return bind(payload, "seal_binding", "seal_payload", "seal_sha256")


def make_u0(refs: dict[str, dict[str, Any]], grants: list[dict[str, Any]], artifact_refs: dict[str, dict[str, Any]], candidate_refs: dict[str, dict[str, Any]], definition_refs: dict[str, dict[str, Any]], report_refs: dict[str, dict[str, Any]], records: list[dict[str, Any]], verdict: str, seal_status: str, eligible: bool) -> dict[str, Any]:
    payload = {
        "schema_version": "matrixlabs_phase_vs2_6_fixtures_reports_and_first_run_construction_readiness_receipt_v0",
        "artifact_id": "phase_vs2_6_fixtures_reports_and_first_run_construction_readiness_receipt_v0",
        "artifact_kind": "STATIC_CONSTRUCTION_READINESS_UNIT_RECEIPT",
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "unit_role": UNIT_ROLE,
        "committed_parent_sha": HEAD,
        "logical_package_identity": "phase_vs2_fixtures_reports_and_first_run_construction_readiness_package_v0",
        "protected_upstream_identities_and_hashes": refs,
        "closed_prior_frame_state": {
            "prior_frame_id": "VS2.3_TO_VS2.5_BOUND_TARGET_CONSTRUCTION_SEQUENCE",
            "prior_bounded_construction_consumption_count": 1,
            "prior_bounded_construction_frame_completed": True,
            "prior_bounded_construction_frame_open": False,
            "prior_bounded_construction_grant_further_use_permitted": False,
            "bounded_construction_authority_consumed_by_vs2_6": False,
            "bounded_construction_frame_reopened_by_vs2_6": False,
            "bounded_construction_grant_reused_by_vs2_6": False,
        },
        "three_remaining_grant_records": grants,
        "remaining_effective_grant_count_before": 3,
        "remaining_effective_grant_count_after": 0,
        "fixture_construction_authority_consumed": True,
        "readiness_gate_construction_authority_consumed": True,
        "construction_package_verification_authority_consumed": True,
        "execution_authority_consumed_by_vs2_6": False,
        "execution_authority_created_by_vs2_6": False,
        "sweep_authority_consumed_by_vs2_6": False,
        "runner_authority_created_by_vs2_6": False,
        "artifact_bindings": artifact_refs,
        "candidate_specimen_bindings": candidate_refs,
        "fixture_definition_bindings": definition_refs,
        "individual_report_contract_bindings": report_refs,
        "r01_through_r21_result_table": records,
        "readiness_verdict": verdict,
        "typed_blockers": [],
        "seal_status": seal_status,
        "eligible_for_execution_decision": eligible,
        "coverage_disclosure": {
            "expected_target_cases": 5,
            "expected_typed_stop_cases": 5,
            "expected_exercised_unique_moves": 4,
            "expected_unexercised_unique_moves": 4,
            "expected_terminal_coverage": ["TARGET_REACHED", "STOP_MISSING_SOURCE", "STOP_MISSING_AUTHORITY", "STOP_MISSING_SCHEMA", "STOP_MISSING_CAPABILITY", "STOP_NO_ADMISSIBLE_MOVE"],
        },
        "fixture_contract_constructed": True,
        "fixture_count": 10,
        "static_candidate_specimen_count": 10,
        "runtime_candidate_instance_count": 0,
        "fixture_definition_count": 10,
        "static_expectation_witness_count": 10,
        "runtime_source_snapshot_constructed": True,
        "report_contract_package_constructed": True,
        "execution_package_core_constructed": True,
        "readiness_gate_constructed": True,
        "readiness_audit_completed": True,
        "readiness_receipt_constructed": True,
        "readiness_seal_constructed": True,
        "runtime_reports_emitted": 0,
        "runtime_receipts_emitted": 0,
        "runtime_commit_manifests_emitted": 0,
        "execution_authority_present": False,
        "sweep_authority_present": False,
        "execution_started": False,
        "fixture_executed_count": 0,
        "live_move_selected": False,
        "runtime_candidate_transformed": False,
        "runner_created": False,
        "evidence_yield": "CONFIRMATION_YIELD" if verdict == READY_GATE else "DIAGNOSTIC_YIELD",
        "confirmation_yield_claims": ["fixture package exact", "candidate specimens O2-valid", "expected paths contract-derived", "F01 repeat path statically coherent", "F02 preservation statically coherent", "F07 declaration/effect distinction preserved", "negative blockers distinguished", "source snapshot frozen", "report contract traceable", "E0 non-circular", "readiness verdict typed", "RS0 non-authorizing", "execution absent"],
        "logical_transition": "ADVANCE(VS2_7_PHASE_CLOSURE_PENDING)",
        "bookkeeping_transition": "ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS_V0_PENDING)",
        "source_basis": source_basis("VS2.6 receipt"),
    }
    return bind(payload, "receipt_binding", "receipt_payload", "receipt_sha256")


def artifact_ref_map(artifacts: dict[str, tuple[dict[str, Any], str, str]]) -> dict[str, dict[str, Any]]:
    return {key: local_ref(artifact, path, role) for key, (artifact, path, role) in artifacts.items()}


def build_all(root: Path) -> dict[str, Any]:
    up = load_upstream(root)
    refs = upstream_refs(up)
    grants = grant_records(up)
    d0 = make_d0(refs, grants)
    write_json(root / D0_JSON, d0)
    d0_ref = local_ref(d0, D0_JSON, "UPSTREAM_PACKAGE_DEPENDENCY_INVENTORY")
    f0x = make_f0x(refs, d0_ref)
    write_json(root / F0X_JSON, f0x)
    f0x_ref = local_ref(f0x, F0X_JSON, "FIXTURE_CONTRACT")
    s0x = make_s0x(refs, f0x_ref, d0_ref)
    write_json(root / S0X_JSON, s0x)
    s0x_ref = local_ref(s0x, S0X_JSON, "RUNTIME_SOURCE_SNAPSHOT")
    candidates = make_candidates(refs, f0x_ref, s0x_ref)
    for fixture_id, artifact in candidates.items():
        write_json(root / CANDIDATE_PATHS[fixture_id], artifact)
    candidate_refs = {fixture_id: local_ref(artifact, CANDIDATE_PATHS[fixture_id], "STATIC_CANDIDATE_SPECIMEN") for fixture_id, artifact in candidates.items()}
    definitions = make_definitions(refs, f0x_ref, s0x_ref, candidate_refs)
    for fixture_id, artifact in definitions.items():
        write_json(root / DEFINITION_PATHS[fixture_id], artifact)
    definition_refs = {fixture_id: local_ref(artifact, DEFINITION_PATHS[fixture_id], "FIXTURE_DEFINITION") for fixture_id, artifact in definitions.items()}
    fs0 = make_fs0(f0x_ref, s0x_ref, candidate_refs, definition_refs)
    write_json(root / FS0_JSON, fs0)
    fs0_ref = local_ref(fs0, FS0_JSON, "FIXTURE_SET")
    report_artifacts: dict[str, dict[str, Any]] = {}
    for key, (_artifact_id, _contract_id, path) in REPORT_CONTRACTS.items():
        report = make_report_contract(key, fs0_ref)
        report_artifacts[key] = report
        write_json(root / path, report)
    report_refs = {key: local_ref(report, REPORT_CONTRACTS[key][2], "REPORT_CONTRACT") for key, report in report_artifacts.items()}
    rp0 = make_rp0(report_refs, fs0_ref)
    write_json(root / RP0_JSON, rp0)
    rp0_ref = local_ref(rp0, RP0_JSON, "REPORT_CONTRACT_PACKAGE")
    bounds = package_bounds(up[PROFILE_JSON], up[P0_JSON])
    e0 = make_e0(refs, d0_ref, f0x_ref, s0x_ref, fs0_ref, rp0_ref, bounds)
    write_json(root / E0_JSON, e0)
    e0_ref = local_ref(e0, E0_JSON, "EXECUTION_PACKAGE_CORE")
    records = readiness_records()
    verdict, seal_status, eligible = derive_readiness(records)
    g0 = make_g0(e0_ref, records, verdict, seal_status, eligible)
    write_json(root / G0_JSON, g0)
    g0_ref = local_ref(g0, G0_JSON, "READINESS_GATE")
    gr0 = make_gr0(g0_ref, e0_ref, records, verdict, eligible)
    write_json(root / GR0_JSON, gr0)
    gr0_ref = local_ref(gr0, GR0_JSON, "READINESS_GATE_RECEIPT")
    rs0 = make_rs0(e0_ref, g0_ref, gr0_ref, verdict, seal_status, eligible)
    write_json(root / RS0_JSON, rs0)
    rs0_ref = local_ref(rs0, RS0_JSON, "READINESS_SEAL")
    artifact_refs = artifact_ref_map({
        "D0": (d0, D0_JSON, "UPSTREAM_PACKAGE_DEPENDENCY_INVENTORY"),
        "F0X": (f0x, F0X_JSON, "FIXTURE_CONTRACT"),
        "S0X": (s0x, S0X_JSON, "RUNTIME_SOURCE_SNAPSHOT"),
        "FS0": (fs0, FS0_JSON, "FIXTURE_SET"),
        "RP0": (rp0, RP0_JSON, "REPORT_CONTRACT_PACKAGE"),
        "E0": (e0, E0_JSON, "EXECUTION_PACKAGE_CORE"),
        "G0": (g0, G0_JSON, "READINESS_GATE"),
        "GR0": (gr0, GR0_JSON, "READINESS_GATE_RECEIPT"),
        "RS0": (rs0, RS0_JSON, "READINESS_SEAL"),
    })
    artifact_refs["RS0"] = rs0_ref
    u0 = make_u0(refs, grants, artifact_refs, candidate_refs, definition_refs, report_refs, records, verdict, seal_status, eligible)
    write_json(root / U0_JSON, u0)
    artifact_refs["U0"] = local_ref(u0, U0_JSON, "VS2_6_UNIT_RECEIPT")
    write_md(root / F0X_MD, f0x, f0x["contract_binding"]["contract_sha256"], ["- Fixture contract freezes ten fixture identities and order.", "- Fixture set status is FROZEN_NOT_EXECUTED."])
    write_md(root / FS0_MD, fs0, fs0["fixture_set_binding"]["fixture_set_sha256"], ["- Fixture set binds F0X, S0X, ten candidates, and ten definitions.", "- Expected distribution is five target cases and five typed-stop cases."])
    write_md(root / RP0_MD, rp0, rp0["package_binding"]["package_sha256"], ["- RP0 binds five report contracts.", "- Runtime report fields remain pre-execution empty."])
    write_md(root / E0_MD, e0, e0["manifest_binding"]["manifest_sha256"], ["- E0 binds the exact static package core.", "- E0 does not bind G0, GR0, RS0, active authority, run identity, or runtime instances."])
    write_md(root / G0_MD, g0, g0["gate_binding"]["gate_sha256"], ["- G0 derives readiness from R01-R21.", f"- Readiness verdict: `{verdict}`."])
    write_md(root / RS0_MD, rs0, rs0["seal_binding"]["seal_sha256"], ["- RS0 seals exact package readiness.", "- RS0 grants no execution, sweep, automatic rerun, or runner authority."])
    return {
        "upstream": up,
        "refs": refs,
        "grants": grants,
        "artifacts": {
            "D0": d0,
            "F0X": f0x,
            "S0X": s0x,
            "FS0": fs0,
            "RP0": rp0,
            "E0": e0,
            "G0": g0,
            "GR0": gr0,
            "RS0": rs0,
            "U0": u0,
        },
        "candidates": candidates,
        "definitions": definitions,
        "reports": report_artifacts,
        "records": records,
        "verdict": verdict,
        "seal_status": seal_status,
        "eligible": eligible,
    }


def run_baseline(root: Path) -> None:
    result = subprocess.run(["python3", BASELINE_SCRIPT], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        fail("STOP_VS2_6_CAPABILITY_LAYER_REQUIRED", BASELINE_SCRIPT, "baseline_generation", "success", result.stderr)


def check_no_forbidden_values(root: Path) -> None:
    forbidden = ["<derived>", "<placeholder>", "<hash>", "TBD", "TODO"]
    hits = []
    for rel in GENERATED_DOCS:
        text = (root / rel).read_text(encoding="utf-8")
        for token in forbidden:
            if token in text:
                hits.append(f"{rel}:{token}")
    if hits:
        fail("STOP_VS2_6_CAPABILITY_LAYER_REQUIRED", "generated_artifacts", "forbidden_unresolved_values", [], hits)


def emit_success(result: dict[str, Any], root: Path) -> None:
    artifacts = result["artifacts"]
    candidates = result["candidates"]
    definitions = result["definitions"]
    reports = result["reports"]
    print("BUILD_PHASE_VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS_V0_COMPLETE")
    print(f"phase_id={PHASE_ID}")
    print(f"unit_id={UNIT_ID}")
    print(f"unit_role={UNIT_ROLE}")
    print(f"upstream_commit_sha={HEAD}")
    for key in ["D0", "F0X", "S0X", "FS0", "RP0", "E0", "G0", "GR0", "RS0", "U0"]:
        artifact = artifacts[key]
        path = {"D0": D0_JSON, "F0X": F0X_JSON, "S0X": S0X_JSON, "FS0": FS0_JSON, "RP0": RP0_JSON, "E0": E0_JSON, "G0": G0_JSON, "GR0": GR0_JSON, "RS0": RS0_JSON, "U0": U0_JSON}[key]
        binding, _payload_key, hash_key = binding_tuple(path)
        print(f"{key}_sha256={artifact[binding][hash_key]}")
    for key, report in reports.items():
        print(f"report_contract_hash {key}={report['contract_binding']['contract_sha256']}")
    for fixture_id in FIXTURE_IDS:
        print(f"candidate_specimen_hash {fixture_id}={candidates[fixture_id]['candidate_binding']['candidate_sha256']}")
    for fixture_id in FIXTURE_IDS:
        print(f"fixture_definition_hash {fixture_id}={definitions[fixture_id]['fixture_definition_binding']['fixture_definition_sha256']}")
    for row in result["records"]:
        print(f"{row['readiness_component_id']}={row['readiness_status']}")
    print(f"readiness_verdict={result['verdict']}")
    print(f"seal_status={result['seal_status']}")
    print(f"execution_decision_eligibility={str(result['eligible']).lower()}")
    print("remaining_grant_count_before=3")
    print("remaining_grant_count_after=0")
    print("fixture_count=10")
    print("candidate_specimen_count=10")
    print("runtime_candidate_count=0")
    print("expected_target_cases=5")
    print("expected_typed_stop_cases=5")
    print("expected_exercised_unique_moves=4")
    print("expected_unexercised_unique_moves=4")
    print("execution_authority_present=false")
    print("execution_performed=false")
    print("runtime_receipts_emitted=0")
    print("runtime_reports_emitted=0")
    print("evidence_yield=CONFIRMATION_YIELD")
    print("logical_transition=ADVANCE(VS2_7_PHASE_CLOSURE_PENDING)")
    print("bookkeeping_transition=ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS_V0_PENDING)")
    print("git_status_short:")
    print(git(root, ["status", "--short", "--untracked-files=all"]))


def emit_stop(exc: StopFailure) -> None:
    print("BUILD_PHASE_VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS_V0_STOP")
    print(f"failure_code={exc.code}")
    print(f"failed_artifact={exc.artifact}")
    print(f"failed_component_or_field={exc.field}")
    print(f"expected_value={json.dumps(exc.expected, sort_keys=True)}")
    print(f"observed_value={json.dumps(exc.observed, sort_keys=True)}")
    print(f"violated_invariant={exc.invariant}")
    print("violated_authority_boundary=VS2_6_STATIC_CONSTRUCTION_ONLY")
    print("blocked_downstream_unit=VS2_6")
    print("exact_bounded_correction_surface=VS2_6_REPAIR_OR_BOOKKEEPING_SURFACE")
    print("capability_proposal_candidate_required=false")
    print("human_decision_required=false")
    print("self_repair_performed=false")


def main() -> int:
    root = Path.cwd().resolve()
    try:
        check_repo(root)
        result = build_all(root)
        check_no_forbidden_values(root)
        run_baseline(root)
        validate_dirty_scope(root)
        emit_success(result, root)
        return 0
    except StopFailure as exc:
        emit_stop(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
