# phase_vs2_frozen_target_contract_v0

## Identity

- Artifact kind: `CONCRETE_IMMUTABLE_TARGET_CONTRACT`
- Version: `v0`
- Status: `FROZEN_FOR_FIRST_SWEEP_CAPABLE_KERNEL_PROFILE`
- Canonical hash: `378acf4fb02ad20bfd5213bde4b267fe605dc528812e29a985909fef251d7546`

## Bound References

- `profile_reference`: `BOUND` `phase_vs2_first_sweep_capable_kernel_profile_v0` `844fe441ecda5ec84076e9f665d09868373c9b24ea89d5d7056c485823db3142`
- `semantic_target_freeze_reference`: `BOUND` `phase_vs2_typed_state_contract_convergence_target_freeze_v0` `518bf3238994cfc88ea542289eb622c90f9eb7f3d6575398c95dd57203669eb8`
- `scope_regime_reference`: `BOUND` `phase_vs2_scope_regime_contract_v0` `a6b4819aee35e5f09686a5a69d471b31f3a5cfdcab2078a29323ba1d31211179`
- `candidate_schema_reference`: `BOUND` `phase_vs2_candidate_typed_state_contract_schema_v0` `0216eb5944f87e760844d018d253f5e808a7a5b7ebd208d8d717e6709b979070`

## Posture

- Mutable posture: immutable static contract/manifest or no instance created.
- Runtime instance created: `false`
- Candidate instance created: `false`
- Fixture instance created: `false`

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
