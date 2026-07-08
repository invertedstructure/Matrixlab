# C8 n22 candidate promotion decision surface v0

## Status

PROMOTION_DECISION_SURFACE_PASS_OPTIONS_PRESENTED_ONLY

## Candidate

candidate.c8.n22.prepare_next_unit_definition_surface.v0

## Candidate audit

CANDIDATE_AUDIT_PASS_CONTRACT_CONFORMANT_NOT_PROMOTED

## Surface role

This surface presents typed human promotion options.

It does not select or apply an option.

## Available options

- DECISION_PROMOTE_CANDIDATE_FOR_DECLARED_SCOPE
- DECISION_PROMOTE_CANDIDATE_INACTIVE_ONLY
- DECISION_REQUEST_CANDIDATE_REVISION
- DECISION_DEFER_PROMOTION
- DECISION_REJECT_CANDIDATE_PROMOTION

## Positive promotion scope

- authority state: AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION
- requested action: PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE
- requested scope: PREPARE_SURFACE_ONLY
- basis scope: C8_N22_BASIS_ONLY
- source object: c8.n22
- output kind: NEXT_BOUNDED_UNIT_DEFINITION_SURFACE
- radius: RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT

## Not performed by this surface

- no option selected
- no promotion decision recorded
- no promotion granted
- no reuse authority granted
- no active archive entry created
- no machine proceed performed
- no authority changed
- no runner authority created

## Next

A human promotion decision receipt is required to select one option.
