# phase_vs2_prospective_controlled_step_authority_envelope_v0

- Artifact kind: `STATIC_PROSPECTIVE_AUTHORITY_ENVELOPE`
- Version: `v0`
- Status: `FROZEN_MAXIMUM_NOT_ACTIVE`
- Canonicalization: `MATRIXLAB_CANONICAL_JSON_V0`
- Canonical SHA-256: `7f2878149b30ca59e46ffa7e12580d4b2c96784e1b7964698d56eca5853c484c`

## Bound References

- `kernel_profile_reference`: `BOUND` `phase_vs2_first_sweep_capable_kernel_profile_v0`
- `scope_regime_reference`: `BOUND` `phase_vs2_scope_regime_contract_v0`
- `runtime_state_contract_reference`: `BOUND` `phase_vs2_runtime_control_state_contract_v0`
- `candidate_schema_reference`: `BOUND` `phase_vs2_candidate_typed_state_contract_schema_v0`
- `target_contract_reference`: `BOUND` `phase_vs2_frozen_target_contract_v0`
- `object_model_manifest_reference`: `BOUND` `phase_vs2_object_model_binding_manifest_v0`
- `source_and_version_binding_contract_reference`: `BOUND` `phase_vs2_source_and_version_binding_contract_v0`
- `move_authority_matrix_reference`: `BOUND` `phase_vs2_move_authority_matrix_v0`
- `finite_move_space_reference`: `BOUND` `phase_vs2_finite_move_space_v0`
- `source_policy_frame_reference`: `BOUND` `phase_vs2_source_and_version_binding_contract_v0`

## Source Basis

- `source_basis`: `authority_bindings` `UPSTREAM_AUTHORITY_STATE_DERIVED`
- `source_basis`: `maximum_prospective_scope` `UPSTREAM_AUTHORITY_STATE_DERIVED`
- `source_basis`: `future_double_authority_check` `UPSTREAM_AUTHORITY_STATE_DERIVED`

## Summary

- Prospective authority envelope is maximum-only and inactive.
- Active controlled-step and sweep authority are absent by policy.

## Nonclaims

- This artifact does not authorize execution.
- This artifact does not create runtime, candidate, fixture, sweep, or runner instances.
- This Markdown file is a deterministic projection of the JSON artifact.
