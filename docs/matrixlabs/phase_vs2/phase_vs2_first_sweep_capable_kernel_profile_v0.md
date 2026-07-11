# Phase VS2.2 First Sweep-Capable Kernel Profile v0

## Source Binding

- Source intake commit: `9d529c6813fd5db38eb4a63368a8d538aa7a88e4`
- Source intake file SHA256: `aac9ba4eec3ca577ead6cd23f8af6b9ecc6a9d542ec2395450a698f45465514b`
- Source intake canonical SHA256: `830c62352e6eab4445b8cac9bbb7851da49a39633fc5cb673b71283bba1eaaeb`
- Source manifest SHA256: `9aaceb1758920971d8f5d7f305b837b7021ebc0a84714dea08755efce1c0a6ef`
- Source intake receipt SHA256: `b8b440b920993d38f77b0359ea928a255d780e5e682572fcc9144c35e63609cd`

## Profile Freeze

- Profile ID: `FIRST_SWEEP_CAPABLE_KERNEL_PROFILE_V0`
- Profile class: `BOUNDED_VERTICAL_EVIDENCE_PRODUCING_KERNEL_PROFILE`
- Profile status: `SEMANTIC_PROFILE_FROZEN_CONSTRUCTION_PENDING`
- MCCL relationship: `BOUNDED_PROFILE_PROJECTION_OF_MCCL_V0`
- Kernel profile frozen: `true`
- Kernel constructed: `false`
- Execution authorized: `false`

## Component Classification

- Component count: `20`
- Required full: `14`
- Required minimal: `4`
- Deferred: `2`
- Forbidden component count: `0`
- S21 remains downstream-only and is not a C01-C20 profile member.

## Grants

- Consumed exactly once: `VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY`
- Remaining grants routed and unconsumed: `4`
- Construction, fixture, readiness, and verification grants are not consumed by VS2.2.

## Frozen Boundaries

- Maximum construction envelope frozen: `true`
- Maximum future execution envelope frozen: `true`
- Forbidden behavior boundary complete: `true`
- Downstream sequence frozen: `true`
- Next unit: `VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PENDING`

## Canonical Hash

- Profile SHA256: `844fe441ecda5ec84076e9f665d09868373c9b24ea89d5d7056c485823db3142`

## Terminal

- Profile gate: `VS2_2_FIRST_SWEEP_KERNEL_PROFILE_FREEZE_PASS`
- Logical transition: `ADVANCE(VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PENDING)`
- Construction-session terminal: `ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_V0_PENDING)`
