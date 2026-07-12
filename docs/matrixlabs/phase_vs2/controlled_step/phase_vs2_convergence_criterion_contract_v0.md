# phase_vs2_convergence_criterion_contract_v0

- Artifact identity: `phase_vs2_convergence_criterion_contract_v0`
- Artifact kind: `STATIC_OPERATIONAL_CONVERGENCE_CRITERION_CONTRACT`
- Version: `v0`
- Status: `DEFINED_AND_FROZEN_NOT_EXECUTED`
- Canonicalization: `MATRIXLAB_CANONICAL_JSON_V0`
- Canonical SHA-256: `a9c512025963df2a07ba93e3071683f392264013824f82ddbcfd923ab8321fd4`

## Upstream Bindings

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

- `S14_CONVERGENCE_CRITERION_EVALUATOR`: `a9c512025963df2a07ba93e3071683f392264013824f82ddbcfd923ab8321fd4`

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

- `does_not_execute_convergence`
- `does_not_mutate_candidate`
- `does_not_authorize_execution`
- `does_not_renew_budget_or_radius`

## Projection Notes

- C20 preserves exact V6 convergence results.
- C20 maps radius exhaustion to STOP_RADIUS_EXHAUSTED, not STOP_BUDGET_EXHAUSTED.
- This Markdown file is a deterministic projection of the JSON artifact.
