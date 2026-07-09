# Phase VS0 happy-path A→F build receipt v0

## Status

VS0_2_HAPPY_PATH_BUILD_PASS_A_TO_F_PHASE_SPECIMEN_CREATED

## Evidence Yield

CONFIRMATION_YIELD

## Preflight

phase_vs0_source_inventory_v0 passed.

## Build mode

PHASE_NAMESPACE_SPECIMEN_BUILD_FROM_COMMITTED_SOURCE_CHAIN

## Phase run namespace

docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0

## Built chains

- A authority transition chain: built
- B read-only router chain: built
- C candidate archive chain: built
- D promotion + machine proceed chain: built
- E compression chain: built
- F registry candidate chain: built

## Terminal objects

- A4: phase_vs0.c8_n22_authority_transition_closure_v0
- B3: phase_vs0.c8_n22_router_specimen_closure_v0
- C3: phase_vs0.c8_n22_candidate_archive_entry_admissibility_audit_v0
- D5: phase_vs0.c8_n22_machine_proceed_closure_v0
- E4: phase_vs0.c8_n22_compression_specimen_closure_v0
- F4: phase_vs0.c8_n22_registry_candidate_closure_projection_v0

## D-chain radius

- before: 1
- consumed: 1
- after: 0
- exhausted: true

## Machine-action boundary

- D4 preparation action performed: true
- machine action count: 1
- machine action outside D4: false
- machine action after D5: false

## Source mutation boundary

- canonical source chain mutated: false
- committed Block F start source replaced: false

## Global non-effects

- no active registry created
- no generalized trace claimed
- no declared scope expansion
- no radius renewed after D5
- no additional machine proceed authorized
- no next unit executed
- no runtime executed
- no source authority replaced by compression
- no runner authority created

## Next required object

phase_vs0_happy_path_verification_v0

## Terminal transition

ADVANCE(VS0_3_HAPPY_PATH_CLOSURE_VERIFICATION_PENDING)

## Non-claim

VS0.2 builds the happy-path phase specimen. It does not replace VS0.3 independent verification.
