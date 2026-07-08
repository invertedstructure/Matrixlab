# C8 n22 candidate promotion decision receipt v0

## Status

PROMOTION_DECISION_RECEIPT_PASS_TYPED_DECISION_RECORDED

## Selected promotion option

DECISION_PROMOTE_CANDIDATE_FOR_DECLARED_SCOPE

## Decision actor

HUMAN

## Selection source

EXPLICIT_HUMAN_SELECTION

## Source promotion surface

c8.n22.candidate_promotion_decision_surface.v0

## Candidate

candidate.c8.n22.prepare_next_unit_definition_surface.v0

## Candidate audit

CANDIDATE_AUDIT_PASS_CONTRACT_CONFORMANT_NOT_PROMOTED

## Selected promotion scope

- authority state: AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION
- requested action: PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE
- requested scope: PREPARE_SURFACE_ONLY
- basis scope: C8_N22_BASIS_ONLY
- source object: c8.n22
- output kind: NEXT_BOUNDED_UNIT_DEFINITION_SURFACE
- radius: RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT

## Effect if applied by D.3

- promotion status: PROMOTION_GRANTED_FOR_DECLARED_SCOPE
- reuse authority: REUSE_AUTHORITY_GRANTED_FOR_DECLARED_SCOPE
- activation: ACTIVATION_ACTIVE

## Application boundary

This receipt records the human promotion decision.

It does not create the active archive entry.

It does not create the inactive archive entry.

It does not apply reuse authority.

It does not apply activation.

It does not perform machine proceed.

## Next required object

c8_n22_prepare_next_unit_definition_active_archive_entry_v0
