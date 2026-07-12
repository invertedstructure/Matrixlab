# phase_vs2_controlled_step_and_convergence_contract_package_v0

- Artifact identity: `phase_vs2_controlled_step_and_convergence_contract_package_v0`
- Artifact kind: `STATIC_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_PACKAGE`
- Version: `v0`
- Status: `FROZEN_NOT_EXECUTED`
- Canonicalization: `MATRIXLAB_CANONICAL_JSON_V0`
- Canonical SHA-256: `3448ee02a854abdd5de28e2feb1ce866854473d9f18435083d5634e82b7a98a0`

## Upstream Bindings

- `r13_reference`: `BOUND` `phase_vs2_receipt_and_atomic_publication_contract_v0`
- `c20_reference`: `BOUND` `phase_vs2_convergence_criterion_contract_v0`
- `phase_vs2_scope_regime_contract_v0_reference`: `BOUND` `phase_vs2_scope_regime_contract_v0`
- `phase_vs2_runtime_control_state_contract_v0_reference`: `BOUND` `phase_vs2_runtime_control_state_contract_v0`
- `phase_vs2_candidate_typed_state_contract_schema_v0_reference`: `BOUND` `phase_vs2_candidate_typed_state_contract_schema_v0`
- `phase_vs2_frozen_target_contract_v0_reference`: `BOUND` `phase_vs2_frozen_target_contract_v0`
- `phase_vs2_object_model_binding_manifest_v0_reference`: `BOUND` `phase_vs2_object_model_binding_manifest_v0`
- `phase_vs2_source_and_version_binding_contract_v0_reference`: `BOUND` `phase_vs2_source_and_version_binding_contract_v0`
- `phase_vs2_move_vocabulary_partition_v0_reference`: `BOUND` `phase_vs2_move_vocabulary_partition_v0`
- `phase_vs2_move_authority_matrix_v0_reference`: `BOUND` `phase_vs2_move_authority_matrix_v0`
- `phase_vs2_finite_move_space_v0_reference`: `BOUND` `phase_vs2_finite_move_space_v0`
- `phase_vs2_prospective_controlled_step_authority_envelope_v0_reference`: `BOUND` `phase_vs2_prospective_controlled_step_authority_envelope_v0`
- `phase_vs2_move_space_binding_manifest_v0_reference`: `BOUND` `phase_vs2_move_space_binding_manifest_v0`
- `phase_vs2_4_receipt_reference`: `BOUND` `phase_vs2_4_finite_move_space_source_and_authority_freeze_receipt_v0`

## Construction-Frame Posture

- Bounded construction consumption count after VS2.5: `1`
- Construction frame open after VS2.5: `False`

## Component Summary

- `S01_INPUT_BINDING_VERIFIER`: `30377b5edda2a36c1ebc8481ffb017ea653994e0c5777353f077535ae48130e4`
- `S02_CONDITION_INSPECTOR`: `8ba6957217af6e008cd59c467b5e7e29bc6959f7c0d1ca671b08c4811a17286b`
- `S03_CONDITION_CLASSIFIER`: `2a0a2e2ab2c3e2391b93e4563b6ae4887bd2ae774baaba1cb2b8736d7606aae5`
- `S04_CAPABILITY_BOUNDARY_EVALUATOR`: `6923d3907e1cbd786a28ced4d68edc8b0ee89cddc6feb3c9344cc920032034e5`
- `S05_TRANSFORMATION_MOVE_ENUMERATOR`: `d81dc5210b3dc24d182290e5424538ca0788ad7d46d2ead9a7504fd13853d198`
- `S06_STRUCTURAL_APPLICABILITY_EVALUATOR`: `933b83662c0886fb5df8c81e026310f2e3bfbb160edd4dcdcc02a3078ecbd4ec`
- `S07_RUNTIME_AUTHORITY_AND_BUDGET_GATE`: `47dc0e244706ae50c20f25c1349e987851c80619c82ddab8f41020238903e131`
- `S08_DETERMINISTIC_MOVE_SELECTOR`: `8aca308fbd20f0713e6545ce7bc070056614d38830acb60e9c25bfcde001e5c3`
- `S09_MOVE_APPLICATOR`: `5de461a5d7f25b22e94bec3aaf75d984ba8543520266bd3508c0c59ad89489e7`
- `S10_TARGET_CONFORMANCE_VALIDATOR`: `b31215ef8354cbde00fc04f81242b76e26da2627cb3638bb7f3082d8bd83f2be`
- `S11_LAWFUL_ADMISSIBILITY_EVALUATOR`: `d17f99ece027f95e4ea75742df3efd5410bedd50b97fee41acba3039df38b262`
- `S12_FORBIDDEN_EFFECT_GUARD`: `6cc5f15cd6b4eddcf482e31c981fc910b67c6705d56955f568d08aeb022f1cee`
- `S13_RECEIPT_AND_ATOMIC_PUBLICATION_BUILDER`: `a5375ec82dd148d05d7199296b58f186747b27cf3f4922555bec6ed1ed29cbf4`
- `S14_CONVERGENCE_CRITERION_EVALUATOR`: `a9c512025963df2a07ba93e3071683f392264013824f82ddbcfd923ab8321fd4`
- `S15_TERMINAL_AND_REPEAT_DECIDER`: `b16c7b03e5d0b88e6c5ba59449a61657c4d39f171058cf722e520d88b2597e51`
- `S16_CONTROLLED_STEP_ORCHESTRATOR`: `1ea5c68116de0f06877ec4a8c4675195358dc178130ed28180c94b848d008bf4`
- `S17_MINIMAL_REPLAY_AND_AUDIT_VERIFIER`: `8e76645e6ea0ba8055ae99e9a1f22c85652b0dd203987ea7d389ed4a5b32d3b2`

## Authority Posture

- Active execution authority present: `False`
- Active sweep authority present: `False`

## Runtime Posture

- Runtime instance created: `False`
- Candidate instance created: `False`
- Move selected: `False`
- Move applied: `False`

## Pending Bindings

- No downstream pending bindings are declared by this artifact.

## Nonclaims

- `does_not_create_fixture_instance`
- `does_not_create_runtime_state_instance`
- `does_not_create_candidate_instance`
- `does_not_enumerate_live_candidate`
- `does_not_select_move`
- `does_not_apply_move`
- `does_not_execute_sweep`
- `does_not_create_runner`

## Projection Notes

- K0 embeds fifteen component contracts and externally binds R13 and C20.
- K0 does not bind M2's future hash.
- This Markdown file is a deterministic projection of the JSON artifact.
