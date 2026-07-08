# C8 n22 authority-action trace compression target v0

## Status

COMPRESSION_TARGET_PASS_DECLARED_ONLY

## Target trace

C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0

## Compression mode

OBSERVABILITY_COMPRESSION_ONLY

## Source closures

- authority transition closure: c8.n22.authority_transition_closure.v0
- router specimen closure: c8.n22.router_specimen_closure.v0
- candidate archive audit: c8.n22.candidate_archive_entry.admissibility_audit.v0
- machine proceed closure: c8.n22.machine_proceed_closure.v0

## Source identity policy

- source artifact paths recorded
- source artifact hashes recorded
- latest-file resolution not allowed
- directory scan authority not allowed

## Critical field groups

- authority state transition
- human authority decision
- requested action
- route classification
- candidate archive status
- candidate audit status
- promotion decision
- active archive entry
- machine proceed action
- radius accounting
- created output surface
- confirmed non effects
- remaining forbidden authorities
- post use stop state
- next possible separate surface

## Required later audit

A later decompression audit must recover all critical field groups and all required recoverable fields, compare them against the source chain, and fail on authority strengthening, radius renewal, runner authority, or source-record replacement.

## Non-effects

- no compression performed
- no E.2 packet produced
- no decompression audit performed
- no registry produced
- no authority changed
- no reuse grant issued
- no radius renewed
- no machine action performed
- no runner authority created
- no source records replaced

## Authority substitution boundary

The compressed packet may not replace source records as authority, satisfy active-entry requirements, satisfy human-decision requirements, satisfy radius requirements, or authorize machine proceed.

## Next

A compressed packet may be created separately in E.2 and must later pass decompression parity audit.

## Exact gate phrases

- confirmed non-effects
- post-use stop state
- no compressed packet created
- no registry created
- no reuse authorized
