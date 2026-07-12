# phase_vs2_move_authority_matrix_v0

- Artifact kind: `STATIC_MOVE_AUTHORITY_REQUIREMENT_MATRIX`
- Version: `v0`
- Status: `FROZEN_NOT_ACTIVE`
- Canonicalization: `MATRIXLAB_CANONICAL_JSON_V0`
- Canonical SHA-256: `4fbd5ae95a00444201f0da70c52515e630b07972f9a3202944f007547d0db0ad`

## Bound References

- `scope_regime_reference`: `BOUND` `phase_vs2_scope_regime_contract_v0`
- `source_and_version_binding_contract_reference`: `BOUND` `phase_vs2_source_and_version_binding_contract_v0`

## Source Basis

- `source_basis`: `move_authority_rows` `STRICT_CROSS_ARTIFACT_INVARIANT_REQUIRED`
- `source_basis`: `prospective_authority_envelope_identity` `STRICT_CROSS_ARTIFACT_INVARIANT_REQUIRED`

## Summary

- One authority row exists for each move.
- No row grants active authority.

## Nonclaims

- This artifact does not authorize execution.
- This artifact does not create runtime, candidate, fixture, sweep, or runner instances.
- This Markdown file is a deterministic projection of the JSON artifact.
