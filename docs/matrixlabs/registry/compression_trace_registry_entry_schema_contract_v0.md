# Compression trace registry entry schema contract v0

## Status

REGISTRY_SCHEMA_PASS_CONTRACT_DEFINED_ONLY

## Registry kind

COMPRESSION_TRACE_OBSERVABILITY_REGISTRY

## Schema role

REGISTRY_ENTRY_CONTRACT_ONLY

## Schema scope

COMPRESSION_STABLE_TRACE_CANDIDATES_ONLY

## Required field groups

- entry identity
- source compression closure
- source compressed packet
- source decompression audit
- trace label
- trace scope
- specimen evidence
- generalization status
- allowed candidate use
- forbidden candidate use
- decompression requirements
- authority boundaries
- radius boundaries
- runner boundaries
- activation boundaries
- promotion boundaries
- revocation or expiry
- audit requirements

## Candidate-stage allowed use

- candidate queue display
- human review
- trace search
- future comparison seed
- dashboard projection

## Candidate-stage forbidden use

- source authority replacement
- authorization for reuse
- radius renewal
- machine proceed authorization
- execution authorization
- runner routing
- schema promotion
- taxonomy promotion

## Contract laws

- registry schema contract does not create candidate
- registry candidate does not equal active registry entry
- single specimen does not equal generalized pattern
- observability registry does not equal source authority
- observability registry does not equal runner authority
- source records remain authority

## Specimen-count discipline

- specimen count must be explicit
- specimen IDs must be listed
- specimen count must equal listed specimen IDs
- single specimen remains local-only unless later evidence and audit say otherwise

## Non-effects

- no candidate entry creation
- no active registry entry materialization
- no registry use grant
- no reuse grant
- no radius renewal
- no machine-proceed grant
- no machine action performed
- no runner-authority creation
- no generalized-pattern creation

## Next

A local registry candidate entry may be created separately under this contract.

## Exact gate phrases

- reuse authorization
- no candidate entry created
- no active registry entry created
- no registry use authorized
- no reuse authorized
- no radius renewed
- no machine proceed authorized
- no runner authority created
- no generalized pattern created
