# C8 n22 radius-bound prepare trace registry candidate admissibility audit v0

## Status

REGISTRY_CANDIDATE_ADMISSIBILITY_AUDIT_PASS_LOCAL_ONLY

## Audited candidate

candidate.registry.c8_n22_radius_bound_prepare_trace.v0

## Registry schema contract

compression_trace_registry_entry_schema_contract.v0

## Trace label

C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0

## Trace scope

C8_N22_LOCAL_SPECIMEN_ONLY

## Audit result

- candidate admissible: true
- admissible scope: LOCAL_CANDIDATE_ONLY
- active registry acceptance passed: false
- reuse authorization passed: false
- generalization passed: false
- runner authorization passed: false

## Evidence checked

- F.1 schema contract present
- F.2 candidate present
- E.4 compression closure passed
- E.2 compressed packet present
- E.3 decompression audit passed
- source hashes verified
- source identity resolved by explicit paths

## Specimen-count audit

- specimen count: 1
- evidence kind: SINGLE_LOCAL_SPECIMEN
- single specimen is stability evidence: false
- single specimen is generalization evidence: false
- single specimen is runner admissibility evidence: false

## Generalization audit

- general shape claimed: false
- multi-specimen stability claimed: false
- cross-context stability claimed: false
- local candidate only: true

## Boundary audit

- no active registry entry created
- no registry entry activated
- no reuse authorized
- no radius renewed
- no additional machine proceed authorized
- no machine action performed
- no runner authority created
- no generalized pattern created
- source records remain authority
- F.2 candidate record not modified

## Next

Registry candidate closure is required.
