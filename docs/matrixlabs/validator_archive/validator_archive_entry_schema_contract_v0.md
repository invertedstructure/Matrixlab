# Validator archive entry schema contract v0

## Status

ARCHIVE_SCHEMA_PASS_CONTRACT_DEFINED

## Role

ARCHIVE_ENTRY_CONTRACT_ONLY

This artifact defines the required contract for future validator archive entries.

## It does not

- create an archive entry
- create a candidate entry
- grant promotion
- authorize reuse
- activate an archive entry
- allow auto-disposition
- create runner authority
- create an active validator archive entry

## Required field groups

- identity
- archive status
- source basis
- authority scope
- requested action scope
- input object shape
- output object shape
- machine action scope
- radius discipline
- validator requirements
- receipt obligations
- halt conditions
- escalation conditions
- freshness rules
- forbidden authority changes
- promotion and reuse status
- revocation and expiry
- Readabout projection hooks

## Core laws

A local specimen is not reusable authority.

A candidate entry is not reusable authority.

A schema contract is not schema authorization.

Reuse requires explicit promotion and declared scope.

Activation requires explicit activation.

Preapproved inactive does not mean active.
