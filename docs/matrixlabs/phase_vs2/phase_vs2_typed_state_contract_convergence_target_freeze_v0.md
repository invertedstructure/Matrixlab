# Phase VS2.2 Typed State Contract Convergence Target Freeze v0

## Target Identity

- Target family: `BOUNDED_CONTRACT_CONVERGENCE`
- Target ID: `TYPED_STATE_CONTRACT_CONVERGENCE_V0`
- Target status: `SEMANTIC_TARGET_FROZEN_IMPLEMENTATION_SCHEMA_PENDING`
- Target count: `1`
- Semantic target frozen: `true`
- Serialized target schema constructed: `false`
- Execution authorized: `false`

## Target Statement

Given one declared local scope/regime, one bounded typed-state contract candidate, one frozen local target contract, one frozen local admissibility policy, one finite authorized transformation move-space, one fixed move and case budget, one declared source snapshot, and one frozen convergence criterion, the kernel may, after later construction, construction verification, and separate execution authorization, attempt to reach a locally valid and lawfully admissible terminal typed-state contract.

## Target Path

- candidate typed-state contract
- expose current target condition or defect
- enumerate lawful transformations
- select one lawful transformation
- apply one bounded candidate delta
- validate resulting candidate
- evaluate admissibility
- evaluate convergence criterion
- emit move receipt
- continue under an explicit repeat condition or halt
- emit terminal receipt and run report

## Completion Boundary

- `TARGET_REACHED` requires validation, admissibility, source bindings, intact scope/regime boundaries, no forbidden effect, authorized moves, respected budgets, convergence criterion success, and terminal receipt emission.
- Already valid candidates may reach target with zero moves and no unnecessary mutation.
- Typed stops may produce Diagnostic Yield but do not complete the positive-path milestone.

## Canonical Hash

- Target-freeze SHA256: `518bf3238994cfc88ea542289eb622c90f9eb7f3d6575398c95dd57203669eb8`

## Terminal

- Target-freeze gate: `VS2_2_TYPED_STATE_CONTRACT_CONVERGENCE_TARGET_FREEZE_PASS`
- Logical transition: `ADVANCE(VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PENDING)`
- Construction-session terminal: `ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_V0_PENDING)`
