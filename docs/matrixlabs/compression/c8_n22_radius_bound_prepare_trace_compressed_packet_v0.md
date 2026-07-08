# C8 n22 radius-bound prepare trace compressed packet v0

## Status

COMPRESSED_PACKET_CREATED_PENDING_DECOMPRESSION_AUDIT

## Trace label

C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0

## Role

Compressed observability packet.

## Trust state

Created, but not trusted as an observability shortcut until E.3 decompression parity audit passes.

## Source closures

- authority transition closure: c8.n22.authority_transition_closure.v0
- router specimen closure: c8.n22.router_specimen_closure.v0
- candidate archive audit: c8.n22.candidate_archive_entry.admissibility_audit.v0
- machine proceed closure: c8.n22.machine_proceed_closure.v0

## Compact summary

- initial authority state: AUTH_STATE_OBSERVED_NOT_AUTHORIZED
- accepted authority state: AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION
- requested action: PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE
- route disposition: ROUTE_MACHINE_MAY_PREPARE_ONLY
- candidate audit: CANDIDATE_AUDIT_PASS_CONTRACT_CONFORMANT_NOT_PROMOTED
- promotion: PROMOTION_GRANTED_FOR_DECLARED_SCOPE
- active entry: ARCHIVE_STATUS_PREAPPROVED_ACTIVE
- machine action: PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE
- output: c8.n22.next_bounded_unit_definition_surface.v0
- output status: NEXT_UNIT_DEFINITION_SURFACE_PREPARED_NOT_EXECUTED
- radius: 1 → 0

## Preservation manifest

The packet claims to preserve all 15 E.1 critical field groups. E.2 does not prove preservation; E.3 must audit decompression parity.

## Decompression map

The packet maps all 15 E.1 critical field groups to packet sections for E.3 audit.

## Confirmed non-effects

- unit not executed
- runtime not executed
- authority not changed after machine proceed
- receipts not rewritten
- taxonomy not promoted
- reuse scope not expanded
- updater not generalized
- runner authority not created
- additional radius not created

## Boundary

This packet does not replace source records, authorize reuse, renew radius, authorize another proceed, satisfy active-entry requirements, satisfy human-decision requirements, satisfy radius requirements, or create runner authority.

## Next required object

c8_n22_radius_bound_prepare_trace_decompression_audit_v0
