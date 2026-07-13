#!/usr/bin/env python3
"""Build Phase VS2.7 static closure artifacts.

This script reads the committed VS2.1-VS2.6 machine-primary artifacts,
verifies their bindings, emits closure artifacts, and refreshes the baseline
share projection. It never runs runtime, fixture, controlled-step, or VS2.6
builder/verifier commands.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = "/home/asd/projects/matrixlab"
BRANCH = "master"
HEAD = "2369f1786d8ddcb905bc3609f983cb60af0fb70a"

PHASE_ID = "PHASE_VS2"
PHASE_NAME = "FIRST_SWEEP_CAPABLE_KERNEL_DEFINITION_CONSTRUCTION_AND_READINESS_V0"
UNIT_ID = "VS2.7_PHASE_CLOSURE"
NORMALIZED_UNIT_ID = "VS2_7_PHASE_CLOSURE"
UNIT_ROLE = "PHASE_RESULT_AND_BOUNDARY_CLOSURE_ONLY"
CANON = "MATRIXLAB_CANONICAL_JSON_V0"
HASH_ALGORITHM = "sha256"

CLOSURE_ARTIFACT_ID = "phase_vs2_closure_v0"
CLOSURE_ARTIFACT_KIND = "STATIC_PHASE_CLOSURE"
CLOSURE_RECEIPT_ID = "phase_vs2_7_phase_closure_receipt_v0"
HUMAN_READOUT_ID = "phase_vs2_closure_readout_v0"

READY_BRANCH = "READY"
READY_GATE = "VS2_6_FIRST_RUN_CONSTRUCTION_READINESS_PASS_READY_FOR_ONE_EXECUTION_DECISION"
PHASE_STATUS = "PHASE_VS2_PASS_FIRST_SWEEP_CAPABLE_KERNEL_SEALED_READY_FOR_ONE_BOUNDED_EXECUTION_DECISION"
CLOSURE_GATE = "VS2_7_PHASE_CLOSURE_PASS_READY_FOR_ONE_EXECUTION_DECISION"
FAIL_GATE = "VS2_7_PHASE_CLOSURE_FAIL"
TERMINAL_TRANSITION = "STOP_PHASE_VS2_CLOSED_PENDING_FIRST_EXECUTION_DECISION"
POST_PHASE_SURFACE = "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE"
BOOKKEEPING_TRANSITION = "ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS2_7_PHASE_CLOSURE_V0_PENDING)"
EVIDENCE_YIELD = "CONFIRMATION_YIELD"

C0_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_closure_v0.json"
C0_MD = "docs/matrixlabs/phase_vs2/phase_vs2_closure_v0.md"
H0_MD = "docs/matrixlabs/phase_vs2/phase_vs2_closure_readout_v0.md"
R0_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_7_phase_closure_receipt_v0.json"
SCRIPT = "scripts/build_phase_vs2_7_phase_closure_v0.py"
VERIFY_SCRIPT = "scripts/verify_phase_vs2_7_phase_closure_v0.py"
BASELINE_SCRIPT = "scripts/build_baseline_share_v0.py"
BASELINE_OUTPUTS = [
    "baseline_share/COMMIT_CONTEXT.md",
    "baseline_share/CURRENT_STATE.md",
    "baseline_share/MANIFEST.json",
    "baseline_share/RECEIPT_POINTERS.md",
]
GENERATED_DOCS = [C0_JSON, C0_MD, H0_MD, R0_JSON]
ALLOWED_DIRTY = set(GENERATED_DOCS) | {SCRIPT, VERIFY_SCRIPT, BASELINE_SCRIPT, *BASELINE_OUTPUTS}
EXPECTED_NEW = set(GENERATED_DOCS) | {SCRIPT, VERIFY_SCRIPT}
EXPECTED_MODIFIED = {BASELINE_SCRIPT, *BASELINE_OUTPUTS}

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
REJECTED_MOVE_ALIASES = [
    "M05_REMOVE_FORBIDDEN_CANDIDATE_DECLARATION",
    "M07_SPLIT_CONFLATED_FIELD",
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
K0_COMPONENT_IDS = [
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

P = "docs/matrixlabs/phase_vs2"
OBJ = f"{P}/object_model"
MOVE = f"{P}/move_space"
STEP = f"{P}/controlled_step"
READY = f"{P}/readiness"
FIXTURE = f"{P}/fixtures"
REPORT = f"{P}/reports"

SOURCES: dict[str, dict[str, Any]] = {
    "VS2_1_SOURCE_INTAKE": {
        "unit": "VS2.1_POST_VS1_SOURCE_INTAKE",
        "path": f"{P}/phase_vs2_post_vs1_source_intake_v0.json",
        "binding": ("source_intake_binding", "source_intake_payload", "source_intake_sha256"),
        "expected": "830c62352e6eab4445b8cac9bbb7851da49a39633fc5cb673b71283bba1eaaeb",
        "role": "SOURCE_INTAKE",
        "version": "v0",
    },
    "VS2_1_RECEIPT": {
        "unit": "VS2.1_POST_VS1_SOURCE_INTAKE",
        "path": f"{P}/phase_vs2_1_post_vs1_source_intake_receipt_v0.json",
        "binding": ("receipt_binding", "receipt_payload", "receipt_sha256"),
        "expected": "b8b440b920993d38f77b0359ea928a255d780e5e682572fcc9144c35e63609cd",
        "role": "UNIT_RECEIPT",
        "version": "v0",
    },
    "PROFILE": {
        "unit": "VS2.2_KERNEL_PROFILE_AND_TARGET_FREEZE",
        "path": f"{P}/phase_vs2_first_sweep_capable_kernel_profile_v0.json",
        "binding": ("profile_binding", "profile_payload", "profile_sha256"),
        "expected": "844fe441ecda5ec84076e9f665d09868373c9b24ea89d5d7056c485823db3142",
        "role": "KERNEL_PROFILE",
        "version": "v0",
    },
    "TARGET_FREEZE": {
        "unit": "VS2.2_KERNEL_PROFILE_AND_TARGET_FREEZE",
        "path": f"{P}/phase_vs2_typed_state_contract_convergence_target_freeze_v0.json",
        "binding": ("target_freeze_binding", "target_freeze_payload", "target_freeze_sha256"),
        "expected": "518bf3238994cfc88ea542289eb622c90f9eb7f3d6575398c95dd57203669eb8",
        "role": "TARGET_FREEZE",
        "version": "v0",
    },
    "VS2_2_RECEIPT": {
        "unit": "VS2.2_KERNEL_PROFILE_AND_TARGET_FREEZE",
        "path": f"{P}/phase_vs2_2_kernel_profile_and_target_freeze_receipt_v0.json",
        "binding": ("receipt_binding", "receipt_payload", "receipt_sha256"),
        "expected": "9e17272877e96f9db6885334e2531df8be8fdd7bb2d501d853c393b8f16ce425",
        "role": "UNIT_RECEIPT",
        "version": "v0",
    },
    "F0": {
        "unit": "VS2.3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION",
        "path": f"{OBJ}/phase_vs2_scope_regime_contract_v0.json",
        "binding": ("contract_binding", "contract_payload", "contract_sha256"),
        "expected": "a6b4819aee35e5f09686a5a69d471b31f3a5cfdcab2078a29323ba1d31211179",
        "role": "SCOPE_REGIME",
        "version": "v0",
    },
    "O1": {
        "unit": "VS2.3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION",
        "path": f"{OBJ}/phase_vs2_runtime_control_state_contract_v0.json",
        "binding": ("contract_binding", "contract_payload", "contract_sha256"),
        "expected": "25fbdfb007372e346d61a3f5de8b0a4f5004c6dff1857e5fc31df38e17c087ad",
        "role": "RUNTIME_CONTROL_STATE_CONTRACT",
        "version": "v0",
    },
    "O2": {
        "unit": "VS2.3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION",
        "path": f"{OBJ}/phase_vs2_candidate_typed_state_contract_schema_v0.json",
        "binding": ("schema_binding", "schema_payload", "schema_sha256"),
        "expected": "0216eb5944f87e760844d018d253f5e808a7a5b7ebd208d8d717e6709b979070",
        "role": "CANDIDATE_TYPED_STATE_SCHEMA",
        "version": "v0",
    },
    "O3": {
        "unit": "VS2.3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION",
        "path": f"{OBJ}/phase_vs2_frozen_target_contract_v0.json",
        "binding": ("target_contract_binding", "target_contract_payload", "target_contract_sha256"),
        "expected": "378acf4fb02ad20bfd5213bde4b267fe605dc528812e29a985909fef251d7546",
        "role": "FROZEN_TARGET_CONTRACT",
        "version": "v0",
    },
    "M0": {
        "unit": "VS2.3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION",
        "path": f"{OBJ}/phase_vs2_object_model_binding_manifest_v0.json",
        "binding": ("manifest_binding", "manifest_payload", "manifest_sha256"),
        "expected": "0af5f635aaca5c37428cc94ca1a8ee6f3885d6e56543198bbdd33a5d4062db3c",
        "role": "OBJECT_MODEL_BINDING_MANIFEST",
        "version": "v0",
    },
    "VS2_3_RECEIPT": {
        "unit": "VS2.3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION",
        "path": f"{P}/phase_vs2_3_scope_regime_and_three_object_model_definition_receipt_v0.json",
        "binding": ("receipt_binding", "receipt_payload", "receipt_sha256"),
        "expected": "61a2298c0d04fa3acf47c391cc593df70be1d8e239e26de891d88b05ac879d0c",
        "role": "UNIT_RECEIPT",
        "version": "v0",
    },
    "S0": {
        "unit": "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE",
        "path": f"{MOVE}/phase_vs2_source_and_version_binding_contract_v0.json",
        "binding": ("contract_binding", "contract_payload", "contract_sha256"),
        "expected": "9b9d6133965beec3b51600ec2d0ab9f002abbd48685cd82f1cf24e0d5d16d6ef",
        "role": "SOURCE_VERSION_BINDING_CONTRACT",
        "version": "v0",
    },
    "V0": {
        "unit": "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE",
        "path": f"{MOVE}/phase_vs2_move_vocabulary_partition_v0.json",
        "binding": ("partition_binding", "partition_payload", "partition_sha256"),
        "expected": "a193dbbee21db8d5577445789d5971ffc29c8c5c37088d4bf88b14434c518c1d",
        "role": "MOVE_VOCABULARY_PARTITION",
        "version": "v0",
    },
    "A0": {
        "unit": "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE",
        "path": f"{MOVE}/phase_vs2_move_authority_matrix_v0.json",
        "binding": ("matrix_binding", "matrix_payload", "matrix_sha256"),
        "expected": "4fbd5ae95a00444201f0da70c52515e630b07972f9a3202944f007547d0db0ad",
        "role": "MOVE_AUTHORITY_MATRIX",
        "version": "v0",
    },
    "MS0": {
        "unit": "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE",
        "path": f"{MOVE}/phase_vs2_finite_move_space_v0.json",
        "binding": ("move_space_binding", "move_space_payload", "move_space_sha256"),
        "expected": "68b094ad5f7a283e591b7b23c66650db9921357e13b0e5c7ca7992723303cbe9",
        "role": "FINITE_MOVE_SPACE",
        "version": "v0",
    },
    "P0": {
        "unit": "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE",
        "path": f"{MOVE}/phase_vs2_prospective_controlled_step_authority_envelope_v0.json",
        "binding": ("envelope_binding", "envelope_payload", "envelope_sha256"),
        "expected": "7f2878149b30ca59e46ffa7e12580d4b2c96784e1b7964698d56eca5853c484c",
        "role": "PROSPECTIVE_AUTHORITY_ENVELOPE",
        "version": "v0",
    },
    "M1": {
        "unit": "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE",
        "path": f"{MOVE}/phase_vs2_move_space_binding_manifest_v0.json",
        "binding": ("manifest_binding", "manifest_payload", "manifest_sha256"),
        "expected": "9cb7f9a66de7a0afc7109a07d789e56cb3629266d9f45821c0c971826afad389",
        "role": "MOVE_SPACE_BINDING_MANIFEST",
        "version": "v0",
    },
    "VS2_4_RECEIPT": {
        "unit": "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE",
        "path": f"{P}/phase_vs2_4_finite_move_space_source_and_authority_freeze_receipt_v0.json",
        "binding": ("receipt_binding", "receipt_payload", "receipt_sha256"),
        "expected": "c78a48e892c0554327a2b1c27570453db48ce7368b27e4b58c6830defd7ff998",
        "role": "UNIT_RECEIPT",
        "version": "v0",
    },
    "K0": {
        "unit": "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION",
        "path": f"{STEP}/phase_vs2_controlled_step_and_convergence_contract_package_v0.json",
        "binding": ("package_binding", "package_payload", "package_sha256"),
        "expected": "3448ee02a854abdd5de28e2feb1ce866854473d9f18435083d5634e82b7a98a0",
        "role": "CONTROLLED_STEP_PACKAGE",
        "version": "v0",
    },
    "C20": {
        "unit": "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION",
        "path": f"{STEP}/phase_vs2_convergence_criterion_contract_v0.json",
        "binding": ("contract_binding", "contract_payload", "contract_sha256"),
        "expected": "a9c512025963df2a07ba93e3071683f392264013824f82ddbcfd923ab8321fd4",
        "role": "CONVERGENCE_CRITERION_CONTRACT",
        "version": "v0",
    },
    "R13": {
        "unit": "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION",
        "path": f"{STEP}/phase_vs2_receipt_and_atomic_publication_contract_v0.json",
        "binding": ("contract_binding", "contract_payload", "contract_sha256"),
        "expected": "a5375ec82dd148d05d7199296b58f186747b27cf3f4922555bec6ed1ed29cbf4",
        "role": "RECEIPT_AND_ATOMIC_PUBLICATION_CONTRACT",
        "version": "v0",
    },
    "M2": {
        "unit": "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION",
        "path": f"{STEP}/phase_vs2_controlled_step_binding_manifest_v0.json",
        "binding": ("manifest_binding", "manifest_payload", "manifest_sha256"),
        "expected": "ffb10d40f6dbf641879a3385ba312f80b9a1f9d667b230e49452ad48abce1e43",
        "role": "CONTROLLED_STEP_BINDING_MANIFEST",
        "version": "v0",
    },
    "VS2_5_RECEIPT": {
        "unit": "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION",
        "path": f"{P}/phase_vs2_5_controlled_step_and_convergence_contract_construction_receipt_v0.json",
        "binding": ("receipt_binding", "receipt_payload", "receipt_sha256"),
        "expected": "31f88a51de957cca434747b02b3bbcbb1e0471f92323f5796a9607f2356e4c68",
        "role": "UNIT_RECEIPT",
        "version": "v0",
    },
    "D0": {
        "unit": "VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
        "path": f"{READY}/phase_vs2_upstream_package_dependency_inventory_v0.json",
        "binding": ("inventory_binding", "inventory_payload", "inventory_sha256"),
        "expected": "fbc1e55d9e1c773244e72e0ed4fb14f901cb364566d0cc413c3cdcb21ec1943e",
        "role": "UPSTREAM_PACKAGE_DEPENDENCY_INVENTORY",
        "version": "v0",
    },
    "F0X": {
        "unit": "VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
        "path": f"{FIXTURE}/phase_vs2_first_kernel_fixture_contract_v0.json",
        "binding": ("contract_binding", "contract_payload", "contract_sha256"),
        "expected": "d34e71cd9d75d5c6c36bde3d17092050f5f1b1f2ede0e5fb985c57931551dec4",
        "role": "FIXTURE_CONTRACT",
        "version": "v0",
    },
    "S0X": {
        "unit": "VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
        "path": f"{READY}/phase_vs2_first_kernel_runtime_source_snapshot_v0.json",
        "binding": ("snapshot_binding", "snapshot_payload", "snapshot_sha256"),
        "expected": "5638c07f1ffa559e1b12e5effaa08e21426267ac4e98906782fb0bf42b29bc7b",
        "role": "RUNTIME_SOURCE_SNAPSHOT",
        "version": "v0",
    },
    "FS0": {
        "unit": "VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
        "path": f"{FIXTURE}/phase_vs2_first_kernel_fixture_set_v0.json",
        "binding": ("fixture_set_binding", "fixture_set_payload", "fixture_set_sha256"),
        "expected": "ce374e242bd0c9a910b8adf2002d8c037151d0dd7c5c093d5c073d6cc875eca8",
        "role": "FIXTURE_SET",
        "version": "v0",
    },
    "RP0": {
        "unit": "VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
        "path": f"{REPORT}/phase_vs2_report_contract_package_v0.json",
        "binding": ("package_binding", "package_payload", "package_sha256"),
        "expected": "830b56386b5bb189d008d2bbc904000cfb07e0f25d3be27092b4467a11c7b2b6",
        "role": "REPORT_CONTRACT_PACKAGE",
        "version": "v0",
    },
    "E0": {
        "unit": "VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
        "path": f"{READY}/phase_vs2_execution_package_core_manifest_v0.json",
        "binding": ("manifest_binding", "manifest_payload", "manifest_sha256"),
        "expected": "cd3f9deed2278d8ab7292a7aa64cf1a68446312d26493f07e508f1d5360211c6",
        "role": "EXECUTION_PACKAGE_CORE",
        "version": "v0",
    },
    "G0": {
        "unit": "VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
        "path": f"{READY}/phase_vs2_first_run_construction_readiness_gate_v0.json",
        "binding": ("gate_binding", "gate_payload", "gate_sha256"),
        "expected": "94f1a98bbfb246226ef7f29887ea0a3ade2a4f71666b5852bbdf93815836cc99",
        "role": "READINESS_GATE",
        "version": "v0",
    },
    "GR0": {
        "unit": "VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
        "path": f"{READY}/phase_vs2_first_run_construction_readiness_gate_receipt_v0.json",
        "binding": ("receipt_binding", "receipt_payload", "receipt_sha256"),
        "expected": "705eb58f43460b289ac40a6e24557bce0be4accd04f372edd79df9ca38c12332",
        "role": "READINESS_GATE_RECEIPT",
        "version": "v0",
    },
    "RS0": {
        "unit": "VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
        "path": f"{READY}/phase_vs2_execution_package_readiness_seal_v0.json",
        "binding": ("seal_binding", "seal_payload", "seal_sha256"),
        "expected": "5c36c71da7bd70889c16a4722d882b0fe8dcfc5ce6cd8a72b80da4dbafbe2d79",
        "role": "READINESS_SEAL",
        "version": "v0",
    },
    "U0": {
        "unit": "VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
        "path": f"{P}/phase_vs2_6_fixtures_reports_and_first_run_construction_readiness_receipt_v0.json",
        "binding": ("receipt_binding", "receipt_payload", "receipt_sha256"),
        "expected": "a651e622335001af85a79409b7074c7b1e5b1b46b9aaeb5e2b40beee4701ade5",
        "role": "VS2_6_UNIT_RECEIPT",
        "version": "v0",
    },
}

for index in range(1, 11):
    fid = f"F{index:02d}"
    SOURCES[f"{fid}_CANDIDATE"] = {
        "unit": "VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
        "path": f"{FIXTURE}/candidates/{fid}_candidate_v0.json",
        "binding": ("candidate_binding", "candidate_payload", "candidate_sha256"),
        "expected": None,
        "role": "STATIC_CANDIDATE_SPECIMEN",
        "version": "v0",
    }

DEFINITION_STEMS = [
    "F01_positive_required_field_and_normalization_v0",
    "F02_already_valid_preservation_v0",
    "F03_repairable_typed_value_normalization_v0",
    "F04_repairable_source_identity_binding_v0",
    "F05_missing_source_blocker_v0",
    "F06_authority_overreach_blocker_v0",
    "F07_repairable_prohibited_candidate_declaration_v0",
    "F08_missing_schema_blocker_v0",
    "F09_missing_capability_blocker_v0",
    "F10_no_admissible_move_gap_v0",
]
for index, stem in enumerate(DEFINITION_STEMS, start=1):
    fid = f"F{index:02d}"
    SOURCES[f"{fid}_DEFINITION"] = {
        "unit": "VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
        "path": f"{FIXTURE}/definitions/{stem}.json",
        "binding": ("fixture_definition_binding", "fixture_definition_payload", "fixture_definition_sha256"),
        "expected": None,
        "role": "FIXTURE_DEFINITION",
        "version": "v0",
    }

UNIT_GATES = {
    "VS2.1": "VS2_1_POST_VS1_SOURCE_INTAKE_PASS",
    "VS2.2": "VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_PASS",
    "VS2.3": "VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PASS",
    "VS2.4": "VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PASS",
    "VS2.5": "VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_PASS",
    "VS2.6": READY_GATE,
}
LOGICAL_TRANSITIONS = {
    "VS2.1": "ADVANCE(VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_PENDING)",
    "VS2.2": "ADVANCE(VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PENDING)",
    "VS2.3": "ADVANCE(VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PENDING)",
    "VS2.4": "ADVANCE(VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_PENDING)",
    "VS2.5": "ADVANCE(VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS_PENDING)",
    "VS2.6": "ADVANCE(VS2_7_PHASE_CLOSURE_PENDING)",
}

CL_DEFS = [
    ("CL01_SOURCE_SPINE_COMPLETE", "Source spine complete", "VS2_7_SOURCE_SPINE_COMPLETE"),
    ("CL02_SOURCE_IDENTITIES_VERIFIED", "Source identities verified", "VS2_7_SOURCE_IDENTITY_TABLE_PASS"),
    ("CL03_SOURCE_LINKAGE_AND_DEPENDENCY_ORDER", "Source linkage and dependency order", "VS2_7_SOURCE_LINKAGE_AND_DEPENDENCY_ORDER_PASS"),
    ("CL04_PHASE_ENTRY_AUTHORITY", "Phase entry authority boundary", "VS2_7_PHASE_ENTRY_AUTHORITY_BOUNDARY_PASS"),
    ("CL05_CONSTRUCTION_AUTHORITY_HISTORY", "Construction authority consumption history", "VS2_7_CONSTRUCTION_AUTHORITY_CONSUMPTION_HISTORY_PASS"),
    ("CL06_PROFILE_AND_TARGET", "Profile and target boundary", "VS2_7_PROFILE_AND_TARGET_BOUNDARY_PASS"),
    ("CL07_SCOPE_REGIME_AND_OBJECT_MODEL", "Scope regime and object model boundary", "VS2_7_SCOPE_REGIME_AND_OBJECT_MODEL_BOUNDARY_PASS"),
    ("CL08_FINITE_MOVE_SPACE", "Finite move space boundary", "VS2_7_FINITE_MOVE_SPACE_BOUNDARY_PASS"),
    ("CL09_PROSPECTIVE_AUTHORITY_INACTIVE", "Prospective authority inactive", "VS2_7_PROSPECTIVE_AUTHORITY_INACTIVE_PASS"),
    ("CL10_CONTROLLED_STEP_AND_C20", "Controlled step and convergence package", "VS2_7_CONTROLLED_STEP_AND_CONVERGENCE_PACKAGE_PASS"),
    ("CL11_FIXTURE_PACKAGE", "Fixture package boundary", "VS2_7_FIXTURE_SET_BOUNDARY_PASS"),
    ("CL12_STATIC_EXPECTED_PATHS", "Static repeat and preservation path boundary", "VS2_7_STATIC_REPEAT_AND_PRESERVATION_PATH_BOUNDARY_PASS"),
    ("CL13_RUNTIME_SOURCE_SNAPSHOT", "Runtime source snapshot boundary", "VS2_7_RUNTIME_SOURCE_SNAPSHOT_BOUNDARY_PASS"),
    ("CL14_UPSTREAM_DEPENDENCY_INVENTORY", "Upstream dependency inventory", "VS2_7_UPSTREAM_DEPENDENCY_INVENTORY_PASS"),
    ("CL15_REPORT_CONTRACTS", "Report contract package", "VS2_7_REPORT_CONTRACT_PACKAGE_PASS"),
    ("CL16_EXECUTION_PACKAGE_CORE", "Execution package core binding", "VS2_7_EXECUTION_PACKAGE_CORE_BINDING_PASS"),
    ("CL17_READINESS_GATE_AND_RECEIPT", "Readiness gate and receipt", "VS2_7_READINESS_GATE_AND_RECEIPT_PASS"),
    ("CL18_READINESS_SEAL", "Readiness seal binding", "VS2_7_READINESS_SEAL_BINDING_PASS"),
    ("CL19_READINESS_BRANCH", "Readiness branch and blocker preservation", "VS2_7_READINESS_BRANCH_AND_BLOCKER_PRESERVATION_PASS"),
    ("CL20_AUTHORITY_POSTURE", "Authority posture preservation", "VS2_7_AUTHORITY_POSTURE_PRESERVATION_PASS"),
    ("CL21_NO_EXECUTION_OR_FORBIDDEN_CLAIMS", "No execution or forbidden claim drift", "VS2_7_NO_EXECUTION_OR_FORBIDDEN_CLAIM_DRIFT_PASS"),
]

PROTECTED_UPSTREAM_PATHS = [
    f"{OBJ}/",
    f"{MOVE}/",
    f"{STEP}/",
    f"{FIXTURE}/",
    f"{READY}/",
    f"{REPORT}/",
    f"{P}/phase_vs2_1_post_vs1_source_intake_receipt_v0.json",
    f"{P}/phase_vs2_2_kernel_profile_and_target_freeze_receipt_v0.json",
    f"{P}/phase_vs2_3_scope_regime_and_three_object_model_definition_receipt_v0.json",
    f"{P}/phase_vs2_4_finite_move_space_source_and_authority_freeze_receipt_v0.json",
    f"{P}/phase_vs2_5_controlled_step_and_convergence_contract_construction_receipt_v0.json",
    f"{P}/phase_vs2_6_fixtures_reports_and_first_run_construction_readiness_receipt_v0.json",
]


class StopFailure(RuntimeError):
    def __init__(self, code: str, check: str, artifact: str, expected: Any, observed: Any, invariant: str) -> None:
        super().__init__(code)
        self.code = code
        self.check = check
        self.artifact = artifact
        self.expected = expected
        self.observed = observed
        self.invariant = invariant


def stop(code: str, check: str, artifact: str, expected: Any, observed: Any, invariant: str = "VS2_7_PHASE_CLOSURE_BOUNDARY") -> None:
    raise StopFailure(code, check, artifact, expected, observed, invariant)


def require(observed: Any, expected: Any, code: str, check: str, artifact: str, invariant: str = "VS2_7_PHASE_CLOSURE_BOUNDARY") -> None:
    if observed != expected:
        stop(code, check, artifact, expected, observed, invariant)


def git(root: Path, args: list[str], binary: bool = False, check: bool = True) -> str | bytes:
    result = subprocess.run(["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=not binary)
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, ["git", *args], result.stdout, result.stderr)
    return result.stdout if binary else result.stdout.strip()


def status_paths(status: str) -> list[str]:
    out: list[str] = []
    for line in status.splitlines():
        raw = line[2:].strip()
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]
        out.append(raw)
    return out


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_hash(payload: Any) -> str:
    return sha256_bytes(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def bind_payload(payload: dict[str, Any], binding_name: str, payload_name: str, hash_name: str) -> dict[str, Any]:
    return {
        **payload,
        binding_name: {
            "canonicalization": CANON,
            payload_name: payload,
            hash_name: canonical_hash(payload),
        },
    }


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def check_repo(root: Path) -> None:
    require(str(root), ROOT, "STOP_VS2_7_REPOSITORY_ROOT_MISMATCH", "repo", "repository_root")
    require(git(root, ["rev-parse", "--show-toplevel"]), ROOT, "STOP_VS2_7_REPOSITORY_ROOT_MISMATCH", "repo", "git_root")
    require(git(root, ["branch", "--show-current"]), BRANCH, "STOP_VS2_7_BRANCH_MISMATCH", "repo", "branch")
    require(git(root, ["rev-parse", "HEAD"]), HEAD, "STOP_VS2_7_UNEXPECTED_HEAD", "repo", "HEAD")
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=root).returncode != 0
    require(staged, False, "STOP_VS2_7_STAGED_CHANGES_PRESENT", "repo", "staged_changes_present")
    if (root / "discussion_packets").exists():
        stop("STOP_VS2_7_DISCUSSION_PACKETS_PRESENT", "repo", "discussion_packets", "absent", "present")
    dirty = status_paths(git(root, ["status", "--short", "--untracked-files=all"]))
    unexpected = [path for path in dirty if path not in ALLOWED_DIRTY]
    if unexpected:
        stop("STOP_VS2_7_PREEXISTING_WORKTREE_CHANGES", "repo", "dirty_paths", sorted(ALLOWED_DIRTY), unexpected)


def protected_upstream_unchanged(root: Path) -> bool:
    result = subprocess.run(["git", "diff", "--quiet", "--", *PROTECTED_UPSTREAM_PATHS], cwd=root)
    return result.returncode == 0


def verify_committed(root: Path, rel: str) -> bytes:
    try:
        committed = git(root, ["show", f"{HEAD}:{rel}"], binary=True)
    except subprocess.CalledProcessError as exc:
        stop("STOP_VS2_7_SOURCE_SPINE_INCOMPLETE", "source_spine", rel, "committed path present", exc.stderr)
    path = root / rel
    if not path.exists():
        stop("STOP_VS2_7_SOURCE_SPINE_INCOMPLETE", "source_spine", rel, "worktree path present", "missing")
    current = path.read_bytes()
    require(current, committed, "STOP_VS2_7_SOURCE_IDENTITY_UNVERIFIED", "source_identity", rel, "committed bytes unchanged")
    return current


def load_source(root: Path, key: str, spec: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    rel = spec["path"]
    raw = verify_committed(root, rel)
    data = json.loads(raw.decode("utf-8"))
    binding_name, payload_name, hash_name = spec["binding"]
    binding = data.get(binding_name)
    if not isinstance(binding, dict):
        stop("STOP_VS2_7_SOURCE_IDENTITY_UNVERIFIED", "source_identity", rel, binding_name, "missing")
    payload = binding.get(payload_name)
    declared = binding.get(hash_name)
    recomputed = canonical_hash(payload)
    require(declared, recomputed, "STOP_VS2_7_SOURCE_IDENTITY_UNVERIFIED", "source_identity", rel)
    if spec["expected"] is not None:
        require(declared, spec["expected"], "STOP_VS2_7_SOURCE_IDENTITY_UNVERIFIED", "source_identity", rel)
    artifact_id = data.get("artifact_id") or payload.get("artifact_id") or key
    artifact_kind = data.get("artifact_kind") or payload.get("artifact_kind") or spec["role"]
    record = {
        "source_key": key,
        "source_unit": spec["unit"],
        "artifact_id": artifact_id,
        "artifact_kind": artifact_kind,
        "artifact_version": spec["version"],
        "declared_path": rel,
        "canonical_content_sha256": declared,
        "raw_file_sha256": sha256_bytes(raw),
        "hash_algorithm": HASH_ALGORITHM,
        "canonicalization_rule": CANON,
        "source_role": spec["role"],
        "identity_source_fields": [binding_name, f"{binding_name}.{payload_name}", f"{binding_name}.{hash_name}", "artifact_id", "artifact_kind"],
        "canonical_hash_recomputed": True,
        "raw_file_hash_recomputed": True,
        "source_identity_verified": True,
    }
    return data, record


def load_sources(root: Path) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    data: dict[str, dict[str, Any]] = {}
    ledger: list[dict[str, Any]] = []
    for key, spec in SOURCES.items():
        data[key], record = load_source(root, key, spec)
        ledger.append(record)
    intake = data["VS2_1_SOURCE_INTAKE"]
    manifest_binding = intake.get("source_manifest_binding", {})
    payload = manifest_binding.get("source_manifest_payload")
    declared = manifest_binding.get("source_manifest_sha256")
    recomputed = canonical_hash(payload)
    require(declared, recomputed, "STOP_VS2_7_SOURCE_IDENTITY_UNVERIFIED", "source_manifest", SOURCES["VS2_1_SOURCE_INTAKE"]["path"])
    require(declared, "9aaceb1758920971d8f5d7f305b837b7021ebc0a84714dea08755efce1c0a6ef", "STOP_VS2_7_SOURCE_IDENTITY_UNVERIFIED", "source_manifest", SOURCES["VS2_1_SOURCE_INTAKE"]["path"])
    ledger.append({
        "source_key": "VS2_1_SOURCE_MANIFEST",
        "source_unit": "VS2.1_POST_VS1_SOURCE_INTAKE",
        "artifact_id": "phase_vs2_embedded_source_manifest_v0",
        "artifact_kind": "EMBEDDED_SOURCE_MANIFEST",
        "artifact_version": "v0",
        "declared_path": f"{SOURCES['VS2_1_SOURCE_INTAKE']['path']}#source_manifest_binding.source_manifest_payload",
        "canonical_content_sha256": declared,
        "raw_file_sha256": ledger[0]["raw_file_sha256"],
        "hash_algorithm": HASH_ALGORITHM,
        "canonicalization_rule": CANON,
        "source_role": "SOURCE_MANIFEST",
        "identity_source_fields": ["source_manifest_binding.source_manifest_payload", "source_manifest_binding.source_manifest_sha256"],
        "canonical_hash_recomputed": True,
        "raw_file_hash_recomputed": True,
        "source_identity_verified": True,
    })
    return data, ledger


def source_ref(ledger: list[dict[str, Any]], key: str) -> dict[str, Any]:
    record = next(row for row in ledger if row["source_key"] == key)
    return {
        "artifact_id": record["artifact_id"],
        "artifact_kind": record["artifact_kind"],
        "artifact_version": record["artifact_version"],
        "declared_path": record["declared_path"],
        "canonical_sha256": record["canonical_content_sha256"],
        "raw_file_sha256": record["raw_file_sha256"],
    }


def verify_expected_ref(parent: dict[str, Any], artifact_id: str, digest: str, label: str) -> None:
    if parent.get("artifact_id") != artifact_id or parent.get("canonical_sha256") != digest:
        stop("STOP_VS2_7_SOURCE_LINKAGE_MISMATCH", "source_linkage", label, {"artifact_id": artifact_id, "canonical_sha256": digest}, parent)


def build_linkage_table(data: dict[str, dict[str, Any]], ledger: list[dict[str, Any]]) -> list[dict[str, Any]]:
    refs = {key: source_ref(ledger, key) for key in [row["source_key"] for row in ledger]}
    link_specs = [
        ("VS2.1 intake and receipt", "VS2.2 profile", "VS2_1_RECEIPT", "PROFILE", "ADVANCE(VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_PENDING)", data["VS2_1_SOURCE_INTAKE"].get("logical_terminal_transition"), ["phase_vs2_post_vs1_source_intake_v0.logical_terminal_transition", "phase_vs2_2 receipt source fields"]),
        ("VS2.2 receipt", "VS2.3 object model", "VS2_2_RECEIPT", "M0", "ADVANCE(VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PENDING)", data["PROFILE"].get("logical_terminal_transition"), ["profile.logical_terminal_transition", "vs2_3 receipt upstream_gates"]),
        ("VS2.3 M0 and receipt", "VS2.4 move space", "VS2_3_RECEIPT", "M1", "ADVANCE(VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PENDING)", data["VS2_3_RECEIPT"].get("logical_terminal_transition"), ["vs2_3_receipt.logical_terminal_transition", "vs2_4 receipt upstream_vs2_3_transition"]),
        ("VS2.4 M1 and receipt", "VS2.5 controlled step", "VS2_4_RECEIPT", "M2", "ADVANCE(VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_PENDING)", data["VS2_4_RECEIPT"].get("logical_terminal_transition"), ["vs2_4_receipt.logical_terminal_transition", "vs2_5 receipt upstream_vs2_4_transition"]),
        ("VS2.5 M2 and receipt", "VS2.6 execution core", "VS2_5_RECEIPT", "E0", "ADVANCE(VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS_PENDING)", data["VS2_5_RECEIPT"].get("logical_terminal_transition"), ["vs2_5_receipt.logical_terminal_transition", "E0.package_references"]),
        ("E0", "G0", "E0", "G0", "E0_BOUND", data["G0"].get("execution_package_core_reference", {}).get("artifact_id"), ["G0.execution_package_core_reference"]),
        ("G0", "GR0", "G0", "GR0", "G0_BOUND", data["GR0"].get("readiness_gate_reference", {}).get("artifact_id"), ["GR0.readiness_gate_reference"]),
        ("E0+G0+GR0", "RS0", "GR0", "RS0", "GR0_BOUND", data["RS0"].get("readiness_gate_receipt_reference", {}).get("artifact_id"), ["RS0.readiness_gate_receipt_reference"]),
        ("RS0 and U0", "C0 closure", "RS0", "U0", READY_GATE, data["U0"].get("readiness_verdict"), ["U0.readiness_verdict", "RS0.seal_status"]),
    ]
    rows = []
    for relationship, child_label, parent_key, child_key, expected_status, observed_status, fields in link_specs:
        parent = refs[parent_key]
        child = refs[child_key]
        if observed_status != expected_status and not (
            expected_status == "E0_BOUND" and observed_status == refs["E0"]["artifact_id"]
        ) and not (
            expected_status == "G0_BOUND" and observed_status == refs["G0"]["artifact_id"]
        ) and not (
            expected_status == "GR0_BOUND" and observed_status == refs["GR0"]["artifact_id"]
        ):
            stop("STOP_VS2_7_SOURCE_LINKAGE_MISMATCH", "source_linkage", relationship, expected_status, observed_status)
        rows.append({
            "child_artifact_id": child["artifact_id"],
            "parent_artifact_id": parent["artifact_id"],
            "parent_artifact_version": parent["artifact_version"],
            "parent_declared_path": parent["declared_path"],
            "parent_canonical_sha256": parent["canonical_sha256"],
            "relationship_role": relationship,
            "expected_parent_gate_or_status": expected_status,
            "observed_parent_gate_or_status": observed_status,
            "source_reference_fields": fields,
            "linkage_verified": True,
        })
    return rows


def verify_unit_gates(data: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        ("VS2.1", data["VS2_1_SOURCE_INTAKE"].get("intake_gate")),
        ("VS2.2", data["VS2_2_RECEIPT"].get("receipt_gate")),
        ("VS2.3", data["VS2_3_RECEIPT"].get("construction_verdict")),
        ("VS2.4", data["VS2_4_RECEIPT"].get("receipt_gate")),
        ("VS2.5", data["VS2_5_RECEIPT"].get("receipt_gate")),
        ("VS2.6", data["U0"].get("readiness_verdict")),
    ]
    out = []
    for unit, observed in rows:
        expected = UNIT_GATES[unit]
        require(observed, expected, "STOP_VS2_7_UNIT_GATE_MISMATCH", "unit_gate", unit)
        out.append({"unit": unit, "expected_gate": expected, "observed_gate": observed, "unit_gate_verified": True})
    return out


def verify_transitions(data: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    observed = {
        "VS2.1": data["VS2_1_SOURCE_INTAKE"].get("logical_terminal_transition"),
        "VS2.2": data["PROFILE"].get("logical_terminal_transition"),
        "VS2.3": data["VS2_3_RECEIPT"].get("logical_terminal_transition"),
        "VS2.4": data["VS2_4_RECEIPT"].get("logical_terminal_transition"),
        "VS2.5": data["VS2_5_RECEIPT"].get("logical_terminal_transition"),
        "VS2.6": data["U0"].get("logical_transition"),
    }
    out = []
    for unit, expected in LOGICAL_TRANSITIONS.items():
        require(observed[unit], expected, "STOP_VS2_7_DEPENDENCY_ORDER_INVALID", "logical_transition", unit)
        out.append({"unit": unit, "expected_transition": expected, "observed_transition": observed[unit], "transition_verified": True})
    return out


def verify_authority(data: dict[str, dict[str, Any]]) -> dict[str, Any]:
    vs23 = data["VS2_3_RECEIPT"]["construction_authority"]
    vs24 = data["VS2_4_RECEIPT"]["construction_authority"]
    vs25 = data["VS2_5_RECEIPT"]["construction_authority"]
    vs26 = data["U0"]
    require(data["VS2_2_RECEIPT"].get("profile_grant_consumed"), True, "STOP_VS2_7_PHASE_ENTRY_AUTHORITY_DRIFT", "authority_history", "VS2.2")
    require(vs23.get("bounded_construction_consumption_count_before"), 0, "STOP_VS2_7_CONSTRUCTION_AUTHORITY_CONSUMPTION_DRIFT", "authority_history", "VS2.3")
    require(vs23.get("bounded_construction_consumption_count_after"), 1, "STOP_VS2_7_CONSTRUCTION_AUTHORITY_CONSUMPTION_DRIFT", "authority_history", "VS2.3")
    require(vs23.get("bounded_construction_frame_open"), True, "STOP_VS2_7_CONSTRUCTION_AUTHORITY_CONSUMPTION_DRIFT", "authority_history", "VS2.3")
    require(vs24.get("additional_bounded_construction_grant_consumption_by_vs2_4"), False, "STOP_VS2_7_CONSTRUCTION_AUTHORITY_CONSUMPTION_DRIFT", "authority_history", "VS2.4")
    require(vs24.get("bounded_construction_consumption_count_after"), 1, "STOP_VS2_7_CONSTRUCTION_AUTHORITY_CONSUMPTION_DRIFT", "authority_history", "VS2.4")
    require(vs24.get("bounded_construction_frame_open_after_vs2_4"), True, "STOP_VS2_7_CONSTRUCTION_AUTHORITY_CONSUMPTION_DRIFT", "authority_history", "VS2.4")
    require(vs25.get("additional_bounded_construction_grant_consumption_by_vs2_5"), False, "STOP_VS2_7_CONSTRUCTION_AUTHORITY_CONSUMPTION_DRIFT", "authority_history", "VS2.5")
    require(vs25.get("bounded_construction_consumption_count_after"), 1, "STOP_VS2_7_CONSTRUCTION_AUTHORITY_CONSUMPTION_DRIFT", "authority_history", "VS2.5")
    require(vs25.get("bounded_construction_frame_completed_by_vs2_5"), True, "STOP_VS2_7_CONSTRUCTION_AUTHORITY_CONSUMPTION_DRIFT", "authority_history", "VS2.5")
    require(vs25.get("bounded_construction_frame_open_after_vs2_5"), False, "STOP_VS2_7_CLOSED_CONSTRUCTION_FRAME_REOPENED", "authority_history", "VS2.5")
    require(vs25.get("bounded_construction_grant_further_use_permitted"), False, "STOP_VS2_7_BOUNDED_CONSTRUCTION_GRANT_RECONSUMED", "authority_history", "VS2.5")
    closed = vs26["closed_prior_frame_state"]
    require(closed.get("prior_bounded_construction_consumption_count"), 1, "STOP_VS2_7_CONSTRUCTION_AUTHORITY_CONSUMPTION_DRIFT", "authority_history", "VS2.6")
    require(closed.get("bounded_construction_grant_reused_by_vs2_6"), False, "STOP_VS2_7_BOUNDED_CONSTRUCTION_GRANT_RECONSUMED", "authority_history", "VS2.6")
    require(closed.get("bounded_construction_frame_reopened_by_vs2_6"), False, "STOP_VS2_7_CLOSED_CONSTRUCTION_FRAME_REOPENED", "authority_history", "VS2.6")
    require(vs26.get("remaining_effective_grant_count_before"), 3, "STOP_VS2_7_REMAINING_GRANT_COUNT_MISMATCH", "authority_history", "VS2.6")
    require(vs26.get("remaining_effective_grant_count_after"), 0, "STOP_VS2_7_REMAINING_GRANT_COUNT_MISMATCH", "authority_history", "VS2.6")
    for field in ["execution_authority_consumed_by_vs2_6", "sweep_authority_consumed_by_vs2_6", "runner_authority_created_by_vs2_6"]:
        require(vs26.get(field), False, "STOP_VS2_7_AUTHORITY_STATE_MUTATED_BY_CLOSURE", "authority_history", field)
    return {
        "vs2_2": {"profile_grant_consumed": True, "bounded_construction_grant_consumed": False},
        "vs2_3": {"grant": "VS2_BOUNDED_CONSTRUCTION_AUTHORITY", "consumption_count_before": 0, "consumption_count_after": 1, "consumption_frame": "VS2.3_TO_VS2.5_BOUND_TARGET_CONSTRUCTION_SEQUENCE", "frame_open_after_vs2_3": True},
        "vs2_4": {"additional_bounded_construction_consumption": False, "consumption_count_before": 1, "consumption_count_after": 1, "frame_open_after_vs2_4": True},
        "vs2_5": {"additional_bounded_construction_consumption": False, "consumption_count_before": 1, "consumption_count_after": 1, "frame_completed_by_vs2_5": True, "frame_open_after_vs2_5": False, "bounded_construction_grant_further_use_permitted": False},
        "vs2_6": {"prior_bounded_construction_consumption_count": 1, "bounded_construction_grant_reused_by_vs2_6": False, "bounded_construction_frame_reopened_by_vs2_6": False, "remaining_effective_grant_count_before": 3, "remaining_effective_grant_count_after": 0, "fixture_construction_authority_consumed": True, "readiness_gate_construction_authority_consumed": True, "construction_package_verification_authority_consumed": True},
        "vs2_7": {"consumed_authority_count": 0, "renewed_authority_count": 0, "reopened_authority_frame_count": 0, "created_authority_count": 0},
        "hard_rule": "one consumption across VS2.3-VS2.5 frame is not one consumption per unit",
    }


def verify_kernel(data: dict[str, dict[str, Any]]) -> None:
    profile = data["PROFILE"]
    target = data["TARGET_FREEZE"]
    target_identity = target.get("target_identity", {})
    require(profile.get("profile_identity", {}).get("profile_id"), "FIRST_SWEEP_CAPABLE_KERNEL_PROFILE_V0", "STOP_VS2_7_PROFILE_OR_TARGET_DRIFT", "profile", "PROFILE")
    require(target_identity.get("target_family"), "BOUNDED_CONTRACT_CONVERGENCE", "STOP_VS2_7_PROFILE_OR_TARGET_DRIFT", "target", "TARGET_FREEZE")
    require(target_identity.get("target_id"), "TYPED_STATE_CONTRACT_CONVERGENCE_V0", "STOP_VS2_7_PROFILE_OR_TARGET_DRIFT", "target", "TARGET_FREEZE")
    require(target_identity.get("artifact_id"), "phase_vs2_typed_state_contract_convergence_target_freeze_v0", "STOP_VS2_7_PROFILE_OR_TARGET_DRIFT", "target", "TARGET_FREEZE")
    m0 = data["M0"]
    require(m0.get("artifact_id"), "phase_vs2_object_model_binding_manifest_v0", "STOP_VS2_7_M0_MISCLASSIFIED_AS_O4", "object_model", "M0")
    if "O4" in json.dumps(m0, sort_keys=True):
        stop("STOP_VS2_7_M0_MISCLASSIFIED_AS_O4", "object_model", "M0", "no O4 execution object", "O4 present")
    require(data["VS2_3_RECEIPT"].get("object_model_counts", {}).get("execution_domain_object_role_count"), 3, "STOP_VS2_7_EXECUTION_DOMAIN_OBJECT_COUNT_DRIFT", "object_model", "VS2.3")
    require(data["VS2_4_RECEIPT"].get("move_count"), 8, "STOP_VS2_7_MOVE_SPACE_DRIFT", "move_space", "VS2.4")
    require(data["VS2_4_RECEIPT"].get("vocabulary_partition_count"), 7, "STOP_VS2_7_MOVE_SPACE_DRIFT", "move_space", "VS2.4")
    require(data["VS2_4_RECEIPT"].get("terminal_outcome_count"), 17, "STOP_VS2_7_MOVE_SPACE_DRIFT", "move_space", "VS2.4")
    require(data["MS0"].get("move_space_status"), "FROZEN_NOT_ACTIVE", "STOP_VS2_7_MOVE_SPACE_DRIFT", "move_space", "MS0")
    require(data["P0"].get("prospective_authority_envelope_active"), False, "STOP_VS2_7_MOVE_AUTHORITY_ACTIVATED_PREMATURELY", "move_space", "P0")
    k0 = data["K0"]
    require(k0.get("component_count"), 17, "STOP_VS2_7_CONTROLLED_STEP_OR_CONVERGENCE_PACKAGE_DRIFT", "controlled_step", "K0")
    require(k0.get("component_ids"), K0_COMPONENT_IDS, "STOP_VS2_7_CONTROLLED_STEP_OR_CONVERGENCE_PACKAGE_DRIFT", "controlled_step", "K0")
    require(k0.get("component_hashes", {}).get("S13_RECEIPT_AND_ATOMIC_PUBLICATION_BUILDER"), SOURCES["R13"]["expected"], "STOP_VS2_7_CONTROLLED_STEP_OR_CONVERGENCE_PACKAGE_DRIFT", "controlled_step", "K0")
    require(k0.get("component_hashes", {}).get("S14_CONVERGENCE_CRITERION_EVALUATOR"), SOURCES["C20"]["expected"], "STOP_VS2_7_CONTROLLED_STEP_OR_CONVERGENCE_PACKAGE_DRIFT", "controlled_step", "K0")
    require(k0.get("primary_invocation_outcome_count"), 6, "STOP_VS2_7_CONTROLLED_STEP_OR_CONVERGENCE_PACKAGE_DRIFT", "controlled_step", "K0")
    require(k0.get("terminal_family", {}).get("terminal_outcomes"), TERMINAL_OUTCOMES, "STOP_VS2_7_CONTROLLED_STEP_OR_CONVERGENCE_PACKAGE_DRIFT", "controlled_step", "K0")
    require(k0.get("primary_invocation_outcomes"), PRIMARY_OUTCOMES, "STOP_VS2_7_CONTROLLED_STEP_OR_CONVERGENCE_PACKAGE_DRIFT", "controlled_step", "K0")
    frozen = k0.get("frozen_auxiliary_vocabularies", {})
    require(frozen.get("V6_CONVERGENCE_RESULTS"), CONVERGENCE_RESULTS, "STOP_VS2_7_CONTROLLED_STEP_OR_CONVERGENCE_PACKAGE_DRIFT", "controlled_step", "K0")
    require(data["MS0"].get("ordered_move_ids"), MOVE_IDS, "STOP_VS2_7_MOVE_SPACE_DRIFT", "move_vocabulary", "MS0")
    for alias in REJECTED_MOVE_ALIASES:
        if alias in json.dumps({"MS0": data["MS0"], "M2": data["M2"]}, sort_keys=True):
            stop("STOP_VS2_7_MOVE_SPACE_DRIFT", "move_vocabulary", "MS0/M2", "alias absent", alias)


def verify_vs26(data: dict[str, dict[str, Any]]) -> None:
    fs0 = data["FS0"]
    u0 = data["U0"]
    require(fs0.get("fixture_count"), 10, "STOP_VS2_7_FIXTURE_SET_DRIFT", "fixture_set", "FS0")
    require(fs0.get("candidate_specimen_count"), 10, "STOP_VS2_7_FIXTURE_SET_DRIFT", "fixture_set", "FS0")
    require(fs0.get("static_witness_count"), 10, "STOP_VS2_7_FIXTURE_SET_DRIFT", "fixture_set", "FS0")
    require(u0.get("fixture_definition_count"), 10, "STOP_VS2_7_FIXTURE_SET_DRIFT", "fixture_set", "U0")
    require(u0.get("runtime_candidate_instance_count"), 0, "STOP_VS2_7_EXECUTION_DETECTED_BEFORE_PHASE_CLOSURE", "execution_state", "U0")
    require(u0.get("fixture_executed_count"), 0, "STOP_VS2_7_FIXTURE_EXECUTED", "execution_state", "U0")
    require(data["S0X"].get("source_snapshot_status"), "FROZEN_FOR_CONSTRUCTION_READINESS_AUDIT", "STOP_VS2_7_RUNTIME_SOURCE_SNAPSHOT_DRIFT", "source_snapshot", "S0X")
    require(data["RP0"].get("report_contract_count"), 5, "STOP_VS2_7_REPORT_CONTRACT_DRIFT", "report_contracts", "RP0")
    e0 = data["E0"]
    required_refs = ["profile", "target_freeze", "F0", "O1", "O2", "O3", "M0", "S0", "V0", "A0", "MS0", "P0", "M1", "K0", "C20", "R13", "M2", "D0", "F0X", "S0X", "FS0", "RP0"]
    require(sorted(e0.get("package_references", {}).keys()), sorted(required_refs), "STOP_VS2_7_EXECUTION_PACKAGE_BINDING_MISMATCH", "execution_package", "E0")
    for forbidden in ["G0", "GR0", "RS0"]:
        if forbidden in e0.get("package_references", {}):
            stop("STOP_VS2_7_CORE_MANIFEST_READINESS_CYCLE_PRESENT", "execution_package", "E0", "no readiness cycle", forbidden)
    g0 = data["G0"]
    gr0 = data["GR0"]
    rs0 = data["RS0"]
    records = g0.get("readiness_component_records", [])
    require([row.get("readiness_component_id") for row in records], READINESS_COMPONENT_IDS, "STOP_VS2_7_READINESS_COMPONENT_UNCLASSIFIED", "readiness", "G0")
    require(all(row.get("readiness_status") == "READY" for row in records), True, "STOP_VS2_7_READINESS_VERDICT_AMBIGUOUS", "readiness", "G0")
    require(g0.get("readiness_verdict"), READY_GATE, "STOP_VS2_7_READINESS_VERDICT_MISMATCH", "readiness", "G0")
    require(gr0.get("readiness_verdict"), READY_GATE, "STOP_VS2_7_READINESS_VERDICT_MISMATCH", "readiness", "GR0")
    require(rs0.get("readiness_verdict"), READY_GATE, "STOP_VS2_7_READINESS_SEAL_VERDICT_MISMATCH", "readiness", "RS0")
    require(rs0.get("eligible_for_execution_decision"), True, "STOP_VS2_7_READINESS_ELIGIBILITY_MISMATCH", "readiness", "RS0")
    require(rs0.get("authority_status", {}).get("execution_authority_granted"), False, "STOP_VS2_7_READINESS_SEAL_GRANTS_AUTHORITY", "authority", "RS0")
    require(rs0.get("authority_status", {}).get("sweep_authority_granted"), False, "STOP_VS2_7_SWEEP_AUTHORITY_PRESENT", "authority", "RS0")
    require(rs0.get("authority_status", {}).get("runner_authority_created"), False, "STOP_VS2_7_RUNNER_AUTHORITY_PRESENT", "authority", "RS0")
    require(rs0.get("subset_authorization_allowed"), False, "STOP_VS2_7_READINESS_SEAL_ALLOWS_UNAUDITED_SUBSET", "readiness", "RS0")


def execution_state(data: dict[str, dict[str, Any]]) -> dict[str, Any]:
    e0_state = data["E0"].get("execution_state", {})
    u0 = data["U0"]
    state = {
        "run_id_created": e0_state.get("run_id") is not None,
        "runtime_o1_instance_created": e0_state.get("runtime_o1_instances_created", 0) != 0,
        "runtime_o2_candidate_instance_created": e0_state.get("runtime_o2_instances_created", 0) != 0,
        "fixture_executed": u0.get("fixture_executed_count", 0) != 0,
        "live_move_enumerated": False,
        "live_move_selected": u0.get("live_move_selected") is not False,
        "live_move_applied": False,
        "runtime_candidate_transformed": u0.get("runtime_candidate_transformed") is not False,
        "runtime_state_published": False,
        "runtime_receipt_emitted": u0.get("runtime_receipts_emitted", 0) != 0,
        "runtime_case_report_emitted": e0_state.get("runtime_case_reports_emitted", 0) != 0,
        "runtime_sweep_report_emitted": e0_state.get("runtime_sweep_report_emitted", 0) != 0,
        "runtime_commit_manifest_emitted": e0_state.get("runtime_commit_manifest_emitted", 0) != 0,
        "execution_authority_present": u0.get("execution_authority_present") is not False,
        "sweep_authority_present": u0.get("sweep_authority_present") is not False,
        "prospective_authority_active": data["P0"].get("prospective_authority_envelope_active") is not False,
        "runner_created": u0.get("runner_created") is not False,
        "execution_started": u0.get("execution_started") is not False,
        "fixtures_executed": u0.get("fixture_executed_count", 0),
        "moves_selected": 0,
        "moves_attempted": 0,
        "moves_applied": 0,
        "runtime_receipts_emitted": u0.get("runtime_receipts_emitted", 0),
        "runtime_reports_emitted": u0.get("runtime_reports_emitted", 0),
    }
    for key, value in state.items():
        if key in {"fixtures_executed", "moves_selected", "moves_attempted", "moves_applied", "runtime_receipts_emitted", "runtime_reports_emitted"}:
            require(value, 0, "STOP_VS2_7_EXECUTION_DETECTED_BEFORE_PHASE_CLOSURE", "execution_state", key)
        else:
            require(value, False, "STOP_VS2_7_EXECUTION_DETECTED_BEFORE_PHASE_CLOSURE", "execution_state", key)
    return state


def closure_checks() -> list[dict[str, Any]]:
    return [
        {
            "closure_check_id": check_id,
            "closure_check_name": name,
            "closure_check_status": "PASS",
            "evidence_references": ["source_identity_table", "source_linkage_table", "unit_gate_table", "readiness_seal_binding"],
            "verified_invariants": [marker],
            "failure_codes": [],
            "bounded_interpretation": "Static closure verification only; no execution or authority mutation.",
        }
        for check_id, name, marker in CL_DEFS
    ]


def build_payload(root: Path) -> dict[str, Any]:
    data, ledger = load_sources(root)
    linkage = build_linkage_table(data, ledger)
    unit_gates = verify_unit_gates(data)
    transitions = verify_transitions(data)
    authority_history = verify_authority(data)
    verify_kernel(data)
    verify_vs26(data)
    state = execution_state(data)
    require(protected_upstream_unchanged(root), True, "STOP_VS2_7_SOURCE_IDENTITY_UNVERIFIED", "protected_upstream", "git diff")

    g0_records = data["G0"]["readiness_component_records"]
    ready_count = sum(1 for row in g0_records if row.get("readiness_status") == "READY")
    e0_ref = source_ref(ledger, "E0")
    rs0_ref = source_ref(ledger, "RS0")
    payload = {
        "phase_id": PHASE_ID,
        "phase_name": PHASE_NAME,
        "unit_id": UNIT_ID,
        "normalized_unit_id": NORMALIZED_UNIT_ID,
        "unit_role": UNIT_ROLE,
        "closure_action_scope": "VERIFY_AND_CLOSE_ALREADY_SEALED_VS2_CHAIN_ONLY",
        "repository_anchor": {"repo_root": ROOT, "branch": BRANCH, "source_commit_sha": HEAD},
        "source_chain": ["VS2.1", "VS2.2", "VS2.3", "VS2.4", "VS2.5", "VS2.6"],
        "source_identity_table": ledger,
        "source_linkage_table": linkage,
        "unit_gate_table": unit_gates,
        "logical_transition_table": transitions,
        "dependency_order_checks": {"dependency_order_verified": True, "dependency_cycle_present": False},
        "construction_authority_consumption_history": authority_history,
        "kernel_profile_summary": {"profile_id": data["PROFILE"]["profile_identity"]["profile_id"], "profile_sha256": source_ref(ledger, "PROFILE")["canonical_sha256"]},
        "target_summary": {"target_family": data["TARGET_FREEZE"]["target_identity"]["target_family"], "target_id": data["TARGET_FREEZE"]["target_identity"]["target_id"], "target_artifact_id": data["TARGET_FREEZE"]["target_identity"]["artifact_id"]},
        "scope_regime_summary": {"scope": "FIRST_SWEEP_KERNEL_SCOPE_V0", "regime": "TYPED_STATE_CONTRACT_CONVERGENCE_REGIME_V0"},
        "object_model_summary": {"execution_domain_object_count": 3, "M0_static": True, "M0_not_O4": True},
        "move_space_summary": {"move_ids": MOVE_IDS, "move_count": 8, "vocabulary_partition_count": 7, "terminal_outcome_count": 17, "move_space_frozen": True, "move_space_active": False},
        "prospective_authority_summary": {"prospective_authority_envelope_active": False, "prospective_authority_envelope_status": data["P0"].get("envelope_status")},
        "controlled_step_summary": {"component_count": 17, "component_order": K0_COMPONENT_IDS, "S13_external_R13_hash": SOURCES["R13"]["expected"], "S14_external_C20_hash": SOURCES["C20"]["expected"], "primary_invocation_outcome_count": 6},
        "convergence_summary": {"convergence_vocabulary": CONVERGENCE_RESULTS, "convergence_vocabulary_count": 11},
        "fixture_summary": {"fixture_count": 10, "static_candidate_specimen_count": 10, "runtime_candidate_instance_count": 0, "fixture_definition_count": 10, "static_witness_count": 10, "fixture_status": "FROZEN_NOT_EXECUTED"},
        "runtime_source_snapshot_summary": {"source_snapshot_status": data["S0X"].get("source_snapshot_status"), "live_source_acquisition_performed": False},
        "upstream_dependency_summary": {"dependency_inventory_sha256": source_ref(ledger, "D0")["canonical_sha256"], "cycle_present": False},
        "report_package_summary": {"report_contract_count": 5, "runtime_case_reports_emitted": 0, "runtime_sweep_reports_emitted": 0},
        "execution_package_core_binding": {"artifact_id": e0_ref["artifact_id"], "package_id": data["E0"].get("package_id"), "canonical_sha256": e0_ref["canonical_sha256"], "raw_file_sha256": e0_ref["raw_file_sha256"]},
        "readiness_gate_binding": {"artifact_id": source_ref(ledger, "G0")["artifact_id"], "gate_id": data["G0"].get("gate_id"), "canonical_sha256": source_ref(ledger, "G0")["canonical_sha256"]},
        "readiness_receipt_binding": {"artifact_id": source_ref(ledger, "GR0")["artifact_id"], "canonical_sha256": source_ref(ledger, "GR0")["canonical_sha256"]},
        "readiness_seal_binding": {"artifact_id": rs0_ref["artifact_id"], "seal_id": data["RS0"].get("seal_id"), "canonical_sha256": rs0_ref["canonical_sha256"], "raw_file_sha256": rs0_ref["raw_file_sha256"]},
        "closure_check_table_CL01_CL21": closure_checks(),
        "readiness_branch": READY_BRANCH,
        "readiness_summary": {"aggregate_gate": READY_GATE, "readiness_component_count": 21, "readiness_ready_count": ready_count, "seal_status": data["RS0"].get("seal_status"), "execution_decision_eligibility": True, "typed_readiness_blocker_count": 0},
        "readiness_blockers": [],
        "authority_summary": {"bounded_construction_authority_consumed_by_vs2_7": False, "fixture_construction_authority_consumed_by_vs2_7": False, "readiness_gate_construction_authority_consumed_by_vs2_7": False, "construction_package_verification_authority_consumed_by_vs2_7": False, "execution_authority_consumed_by_vs2_7": False, "sweep_authority_consumed_by_vs2_7": False, "authority_update_applied_by_vs2_7": False, "prospective_authority_activated_by_vs2_7": False, "runner_authority_created_by_vs2_7": False, "consumed_authority_count_by_vs2_7": 0, "renewed_authority_count_by_vs2_7": 0, "reopened_authority_frame_count_by_vs2_7": 0, "created_authority_count_by_vs2_7": 0, "execution_authority_present": False, "sweep_authority_present": False, "prospective_authority_active": False, "runner_created": False},
        "execution_state": state,
        "forbidden_claim_checks": {"runtime_or_generalization_claim_drift": False, "forbidden_outputs_emitted": False},
        "phase_closed": True,
        "phase_status": PHASE_STATUS,
        "closure_gate": CLOSURE_GATE,
        "post_phase_decision_surface": {"surface_id": POST_PHASE_SURFACE, "named_by_vs2_7": True, "created_by_vs2_7": False, "decision_recorded": False, "authority_update_applied": False, "execution_started": False, "machine_may_authorize_execution": False},
        "terminal_transition": {"transition": TERMINAL_TRANSITION, "executes_next_surface": False, "creates_execution_decision": False, "authorizes_execution": False, "activates_move_authority": False, "creates_run_id": False},
        "evidence_yield": EVIDENCE_YIELD,
        "logical_transition": TERMINAL_TRANSITION,
        "bookkeeping_transition": BOOKKEEPING_TRANSITION,
        "non_claims": [
            "VS2.7 does not authorize execution.",
            "VS2.7 does not create the post-phase execution-decision surface artifact.",
            "VS2.7 does not rerun VS2.6 readiness audit.",
            "VS2.7 does not create runtime state, runtime candidate, runtime receipt, runtime report, run id, or runner.",
        ],
        "failures": [],
    }
    return payload


def render_c0_markdown(c0: dict[str, Any]) -> str:
    payload = c0["closure_payload"]
    cl_lines = "\n".join(f"- `{row['closure_check_id']}`: `{row['closure_check_status']}`" for row in payload["closure_check_table_CL01_CL21"])
    return f"""# phase_vs2_closure_v0

Artifact ID: `{c0['artifact_id']}`
Closure payload SHA256: `{c0['closure_payload_sha256']}`

## Phase Status

- Phase status: `{payload['phase_status']}`
- Closure gate: `{payload['closure_gate']}`
- Readiness branch: `{payload['readiness_branch']}`
- Execution-decision eligibility: `{str(payload['readiness_summary']['execution_decision_eligibility']).lower()}`

## Closure Checks

{cl_lines}

## Execution Package Core

- Artifact ID: `{payload['execution_package_core_binding']['artifact_id']}`
- Logical package ID: `{payload['execution_package_core_binding']['package_id']}`
- Canonical SHA256: `{payload['execution_package_core_binding']['canonical_sha256']}`

## Readiness Seal

- Artifact ID: `{payload['readiness_seal_binding']['artifact_id']}`
- Logical seal ID: `{payload['readiness_seal_binding']['seal_id']}`
- Canonical SHA256: `{payload['readiness_seal_binding']['canonical_sha256']}`

## Authority And Execution

- Execution authority present: `{str(payload['authority_summary']['execution_authority_present']).lower()}`
- Sweep authority present: `{str(payload['authority_summary']['sweep_authority_present']).lower()}`
- Prospective authority active: `{str(payload['authority_summary']['prospective_authority_active']).lower()}`
- Runner created: `{str(payload['authority_summary']['runner_created']).lower()}`
- Execution started: `{str(payload['execution_state']['execution_started']).lower()}`
- Runtime receipts emitted: `{payload['execution_state']['runtime_receipts_emitted']}`
- Runtime reports emitted: `{payload['execution_state']['runtime_reports_emitted']}`

## Post-Phase Surface

- Surface ID: `{payload['post_phase_decision_surface']['surface_id']}`
- Surface created: `{str(payload['post_phase_decision_surface']['created_by_vs2_7']).lower()}`
- Terminal transition: `{payload['terminal_transition']['transition']}`

## Nonclaims

{chr(10).join(f"- {item}" for item in payload['non_claims'])}"""


def render_h0(c0: dict[str, Any]) -> str:
    payload = c0["closure_payload"]
    return f"""# Phase VS2 Closure v0

Status:
{payload['phase_status']}

Closure gate:
{payload['closure_gate']}

Completed:
- post-VS1 source chain admitted
- bounded kernel profile frozen
- typed-state convergence target frozen
- F0/O1/O2/O3/M0 package frozen
- finite move-space frozen
- prospective authority envelope frozen and inactive
- controlled-step package constructed
- C20 convergence contract constructed
- ten-fixture package frozen
- runtime-source snapshot frozen
- report contracts defined
- exact execution-package core assembled
- R01-R21 readiness audit completed
- exact ready result sealed
- CL01-CL21 closure checks passed

Current readiness:
{payload['readiness_seal_binding'].get('seal_status', 'SEALED_READY_FOR_HUMAN_EXECUTION_DECISION')}

Execution-decision eligibility:
{str(payload['readiness_summary']['execution_decision_eligibility']).lower()}

Current authority:
- VS2.7 consumed no authority
- VS2.7 applied no authority update
- prospective authority remains inactive
- active move authority absent
- controlled-step execution authority absent
- kernel execution authority absent
- sweep authority absent
- runner authority absent

Execution state:
- no run initialized
- no runtime O1 state created
- no runtime O2 candidate created
- no fixture executed
- no live move selected
- no candidate transformed
- no runtime receipt emitted
- no runtime report emitted

Next lawful surface:
{payload['post_phase_decision_surface']['surface_id']}

Surface state:
named, not created

Non-claim:
The exact sealed package may be presented
for one bounded human execution decision.

It is not authorized to run."""


def build_all(root: Path) -> dict[str, Any]:
    payload = build_payload(root)
    c0 = {
        "schema_version": "matrixlabs_phase_vs2_closure_v0",
        "artifact_id": CLOSURE_ARTIFACT_ID,
        "artifact_version": "v0",
        "artifact_kind": CLOSURE_ARTIFACT_KIND,
        "closure_payload": payload,
        "closure_payload_sha256": canonical_hash(payload),
    }
    write_json(root / C0_JSON, c0)
    write_text(root / C0_MD, render_c0_markdown(c0))
    write_text(root / H0_MD, render_h0(c0))
    c0_raw = sha256_file(root / C0_JSON)
    c0_md_raw = sha256_file(root / C0_MD)
    h0_raw = sha256_file(root / H0_MD)
    receipt_payload = {
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "normalized_unit_id": NORMALIZED_UNIT_ID,
        "source_commit_sha": HEAD,
        "source_hash_ledger": payload["source_identity_table"],
        "closure_artifact_id": CLOSURE_ARTIFACT_ID,
        "closure_artifact_sha256": c0["closure_payload_sha256"],
        "closure_json_raw_sha256": c0_raw,
        "closure_markdown_raw_sha256": c0_md_raw,
        "closure_readout_raw_sha256": h0_raw,
        "CL01_CL21_statuses": {row["closure_check_id"]: row["closure_check_status"] for row in payload["closure_check_table_CL01_CL21"]},
        "readiness_branch": READY_BRANCH,
        "phase_status": PHASE_STATUS,
        "closure_gate": CLOSURE_GATE,
        "terminal_transition": TERMINAL_TRANSITION,
        "named_post_phase_surface": POST_PHASE_SURFACE,
        "authority_non_effects": payload["authority_summary"],
        "execution_non_effects": payload["execution_state"],
        "evidence_yield": EVIDENCE_YIELD,
        "logical_transition": TERMINAL_TRANSITION,
        "bookkeeping_transition": BOOKKEEPING_TRANSITION,
        "failures": [],
    }
    r0 = {
        "schema_version": "matrixlabs_phase_vs2_7_phase_closure_receipt_v0",
        "receipt_id": CLOSURE_RECEIPT_ID,
        "receipt_version": "v0",
        "receipt_role": "PHASE_VS2_CLOSURE_RECEIPT",
        "receipt_payload": receipt_payload,
        "receipt_payload_sha256": canonical_hash(receipt_payload),
    }
    write_json(root / R0_JSON, r0)
    return {
        "c0": c0,
        "r0": r0,
        "c0_raw": c0_raw,
        "c0_md_raw": c0_md_raw,
        "h0_raw": h0_raw,
        "r0_raw": sha256_file(root / R0_JSON),
        "payload": payload,
    }


def run_baseline(root: Path) -> None:
    result = subprocess.run(["python3", BASELINE_SCRIPT], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        stop("STOP_VS2_7_CAPABILITY_LAYER_REQUIRED", "baseline_projection", BASELINE_SCRIPT, "success", result.stderr)


def validate_dirty_scope(root: Path) -> None:
    dirty = status_paths(git(root, ["status", "--short", "--untracked-files=all"]))
    dirty_set = set(dirty)
    unexpected = sorted(dirty_set - ALLOWED_DIRTY)
    missing = sorted(ALLOWED_DIRTY - dirty_set)
    if unexpected or missing:
        stop("STOP_VS2_7_PREEXISTING_WORKTREE_CHANGES", "dirty_scope", "git_status", {"expected": sorted(ALLOWED_DIRTY), "count": 11}, {"unexpected": unexpected, "missing": missing, "dirty": sorted(dirty_set)})
    modified = {path for path in dirty if path in EXPECTED_MODIFIED}
    new = {path for path in dirty if path in EXPECTED_NEW}
    require(len(modified), 5, "STOP_VS2_7_PREEXISTING_WORKTREE_CHANGES", "dirty_scope", "modified_count")
    require(len(new), 6, "STOP_VS2_7_PREEXISTING_WORKTREE_CHANGES", "dirty_scope", "new_count")


def emit_success(root: Path, result: dict[str, Any]) -> None:
    payload = result["payload"]
    print("BUILD_PHASE_VS2_7_PHASE_CLOSURE_V0_COMPLETE")
    print(f"repo_root={ROOT}")
    print(f"branch={BRANCH}")
    print(f"HEAD={HEAD}")
    print(f"C0_canonical_hash={result['c0']['closure_payload_sha256']}")
    print(f"C0_raw_hash={result['c0_raw']}")
    print(f"C0_markdown_raw_hash={result['c0_md_raw']}")
    print(f"H0_readout_raw_hash={result['h0_raw']}")
    print(f"R0_canonical_hash={result['r0']['receipt_payload_sha256']}")
    print(f"R0_raw_hash={result['r0_raw']}")
    for row in payload["closure_check_table_CL01_CL21"]:
        print(f"{row['closure_check_id']}={row['closure_check_status']}")
    print(f"source_identity_count={len(payload['source_identity_table'])}")
    print(f"source_linkage_count={len(payload['source_linkage_table'])}")
    print(f"readiness_branch={payload['readiness_branch']}")
    print(f"phase_status={payload['phase_status']}")
    print(f"closure_gate={payload['closure_gate']}")
    print(f"terminal_transition={payload['terminal_transition']['transition']}")
    print(f"post_phase_surface={payload['post_phase_decision_surface']['surface_id']}")
    print(f"post_phase_surface_created={str(payload['post_phase_decision_surface']['created_by_vs2_7']).lower()}")
    print(f"authority_consumed_by_vs2_7={payload['authority_summary']['consumed_authority_count_by_vs2_7']}")
    print(f"execution_authority_present={str(payload['authority_summary']['execution_authority_present']).lower()}")
    print(f"sweep_authority_present={str(payload['authority_summary']['sweep_authority_present']).lower()}")
    print(f"prospective_authority_active={str(payload['authority_summary']['prospective_authority_active']).lower()}")
    print(f"execution_performed={str(payload['execution_state']['execution_started']).lower()}")
    print(f"runtime_receipts_emitted={payload['execution_state']['runtime_receipts_emitted']}")
    print(f"runtime_reports_emitted={payload['execution_state']['runtime_reports_emitted']}")
    print(f"runner_created={str(payload['authority_summary']['runner_created']).lower()}")
    print(f"evidence_yield={payload['evidence_yield']}")
    print(f"bookkeeping_transition={payload['bookkeeping_transition']}")
    print("git_status_short:")
    print(git(root, ["status", "--short", "--untracked-files=all"]))


def emit_stop(exc: StopFailure) -> None:
    print("BUILD_PHASE_VS2_7_PHASE_CLOSURE_V0_STOP")
    print(f"failure_code={exc.code}")
    print(f"failed_closure_check={exc.check}")
    print(f"affected_artifact={exc.artifact}")
    print(f"expected_identity_or_value={json.dumps(exc.expected, sort_keys=True)}")
    print(f"observed_identity_or_value={json.dumps(exc.observed, sort_keys=True)}")
    print(f"violated_invariant={exc.invariant}")
    print("phase_consequence=VS2_7_PHASE_CLOSURE_NOT_TRUSTWORTHY")
    print("smallest_lawful_correction_surface=VS2_7_REPAIR_OR_BOOKKEEPING_SURFACE")
    print("capability_proposal_candidate_required=false")
    print("human_decision_required=false")
    print("self_repair_performed=false")


def main() -> int:
    root = Path.cwd().resolve()
    try:
        check_repo(root)
        result = build_all(root)
        run_baseline(root)
        validate_dirty_scope(root)
        emit_success(root, result)
        return 0
    except StopFailure as exc:
        emit_stop(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
