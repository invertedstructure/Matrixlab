# Post-VS0 direction decision receipt v0

## Status

POST_VS0_DIRECTION_DECISION_RECEIPT_PASS

## Source closure

- source phase: PHASE_VS0
- source closure id: phase_vs0_closure_v0
- source closure commit: 18324fd7d82da4a5f9210c1e30d94e8fe5ed783b
- source closure gate: VS0_6_PHASE_CLOSURE_PASS_FIRST_A_TO_F_SPECIMEN_WITH_TYPED_STOPS_AND_EVIDENCE_YIELD
- source phase status: PHASE_VS0_PASS_FIRST_A_TO_F_SPECIMEN_WITH_TYPED_NEGATIVE_STOPS_AND_EVIDENCE_YIELD
- Phase VS0 closed: true

## Decision

- decision: DECISION_OPEN_PHASE_VS1_SOURCE_INTAKE
- decision source: HUMAN_DIRECTION
- allowed scope: VS1_SOURCE_INTAKE_AND_CONTRACT_DEFINITION_PREPARATION_ONLY
- machine selected next phase: false

## Allowed

- VS1.1 source intake may be built
- VS1.1 source intake may run after this receipt is committed
- VS1.2 contract definition preparation may be reached only if VS1.1 passes

## Forbidden

- controlled loop execution authorized: false
- runner creation authorized: false
- move execution authorized: false
- micro-sweeps authorized: false
- registry activation authorized: false
- trace generalization authorized: false
- performance claim authorized: false
- scale claim authorized: false
- next phase selected by machine: false

## Next unit

VS1_1_POST_VS0_SOURCE_INTAKE

## Terminal transition

ADVANCE(VS1_1_POST_VS0_SOURCE_INTAKE_PENDING)

## Non-claim

This receipt opens VS1.1 source intake only. It does not authorize controlled-loop execution, runner creation, move execution, micro-sweeps, registry activation, trace generalization, optimization claims, total coverage claims, or machine-selected next phase.
