# Phase VS0 negative probe battery v0

## Status

VS0_4_NEGATIVE_PROBES_PASS_TYPED_STOPS

## Source

phase_vs0_happy_path_verification_v0 passed.

## Source verification

- source verification commit: daec73d1a631225a00b7d0ad967880dd9d3b301c
- happy path verification: PASS
- source build binding: VS0_3_SOURCE_BUILD_BINDING_PASS_ORIGINAL_BUILD_PLUS_REPAIR_COMMIT
- chain index hash verification: PASS
- indexed artifact hashes match current file content: true

## Probe execution mode

- mode: SYNTHETIC_CONTRACT_LEVEL_NEGATIVE_PROBE_BATTERY
- live runtime execution performed: false
- runner execution performed: false
- production move engine called: false
- contract guard evaluator used: true

## Probe policy

- isolated fixtures: true
- verified happy-path mutation allowed: false
- canonical source-chain mutation allowed: false
- self-repair allowed: false
- unexpected success allowed: false
- probe fixture invalidity allowed: true
- probe evaluator must be valid: true

## Preservation

- A→F hash manifest unchanged: true
- canonical source-chain hash manifest unchanged: true

## Probe results

- NEG01 D4 without active entry: typed stop observed
- NEG02 D4 with radius zero: typed stop observed
- NEG03 E2 without E1 target: typed stop observed
- NEG04 E3 with dropped radius field: typed stop observed
- NEG05 E4 with failed decompression audit: typed stop observed
- NEG06 F2 without E4 closure: typed stop observed
- NEG07 F2 with specimen-count overclaim: typed stop observed
- NEG08 F3 with generalization claimed: typed stop observed
- NEG09 F4 with active registry created: typed stop observed
- NEG10 runner authority true anywhere: typed stop observed

## Summary

- probes expected: 10
- probes run: 10
- expected typed stops: 10
- observed typed stops: 10
- unexpected passes: 0
- wrong stop codes: 0
- ambiguous stops: 0
- diagnostic-field misses: 0
- next-lawful-surface misses: 0
- self-repair attempts: 0
- verified happy-path mutations: 0
- canonical source-chain mutations: 0

## Evidence Yield

- battery branch: CONFIRMATION_YIELD
- probe branch: DIAGNOSTIC_YIELD

## Coverage claim

- selected probe battery only: true
- all possible illegal shortcuts tested: false
- future live runtime coverage claimed: false
- phase closure claimed: false

## Next required object

phase_vs0_evidence_yield_report_v0

## Terminal transition

ADVANCE(VS0_5_EVIDENCE_YIELD_REPORT_PENDING)

## Non-claim

VS0.4 verifies this selected synthetic negative shortcut battery against the verified VS0 phase specimen. It does not repair failed probes, activate a registry, generalize the trace, renew radius, authorize machine proceed, close Phase VS0, prove future live runtime coverage, test all possible illegal paths, or create runner authority.
