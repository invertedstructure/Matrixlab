# C8 n22 radius-bound prepare trace decompression audit v0

## Status

DECOMPRESSION_AUDIT_PASS_CRITICAL_FIELD_PARITY

## Compressed packet

c8.n22.radius_bound_prepare_trace.compressed_packet.v0

## Compression target

c8.n22.authority_action_trace.compression_target.v0

## Trace label

C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0

## Audit scope

E1_DECLARED_CRITICAL_FIELD_PARITY_ONLY

This audit verifies local critical-field decompression parity. It does not claim full trace equivalence.

## Critical field group parity

- authority state transition: GROUP_PARITY_PASS
- human authority decision: GROUP_PARITY_PASS
- requested action: GROUP_PARITY_PASS
- route classification: GROUP_PARITY_PASS
- candidate archive status: GROUP_PARITY_PASS
- candidate audit status: GROUP_PARITY_PASS
- promotion decision: GROUP_PARITY_PASS
- active archive entry: GROUP_PARITY_PASS
- machine proceed action: GROUP_PARITY_PASS
- radius accounting: GROUP_PARITY_PASS
- created output surface: GROUP_PARITY_PASS
- confirmed non effects: GROUP_PARITY_PASS
- remaining forbidden authorities: GROUP_PARITY_PASS
- post use stop state: GROUP_PARITY_PASS
- next possible separate surface: GROUP_PARITY_PASS

## Source integrity

- E.1 source refs loaded
- E.2 copied source refs match E.1
- E.2 copied source hashes match E.1
- source file hashes match E.1 manifest

## Authority safety

- source records not replaced
- authority not strengthened
- execution not authorized
- reuse not authorized by compression
- radius not renewed
- additional machine proceed not authorized
- runner authority not created

## Result

The compressed packet passed local decompression parity and is eligible for E.4 observability-only closure.

## Non-claim

This audit does not make the compressed packet source authority, authorize reuse, renew radius, authorize additional proceed, close Block E, create a registry entry, or create runner authority.

## Next required object

c8_n22_compression_specimen_closure_v0

## Exact gate phrases

- confirmed non-effects: GROUP_PARITY_PASS
- post-use stop state: GROUP_PARITY_PASS
