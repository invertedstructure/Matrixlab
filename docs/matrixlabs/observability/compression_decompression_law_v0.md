# Compression/Decompression Law v0

## Status

LAW_PASS_V0_TESTS

## Purpose

M3 is the no-lie layer before taxonomy.

## Source

- M1 index: `docs/matrixlabs/observability/decision_path_index_v0.json`
- M2 spine: `docs/matrixlabs/observability/receipt_spine_v0.json`
- Observed path: `docs/matrixlabs/architecture/c8_observed_decision_path_v0.json`
- M1 index SHA256: `626e95f48eca3ff517ff419d69d126af1069c67dfe9555d427fc436ccbcd3761`
- M2 spine SHA256: `ab781df8ed859a3b0e90dc120d546df3cfdbce0433352b8b0345db2e05029108`
- Observed path SHA256: `2883e4a86b2bbad9438f6694a4177e0e6db7d8e7b85b8ba1af098a4534a10cfd`
- M1 index commit: `e0e22d33ee1fdfc9dad6964013162a58d6a0b169`
- M2 spine commit: `e78ae91156521669e57bfca3c112d4b83e681d05`
- Observed path commit: `11f8c9d20e30e1c4f614d7405ff2610baa382f6a`

## Core law

A compression is admissible only if decompression recovers the source-critical fields needed to preserve M1 addressability, M2 evidence status, path order, receipt/source backing kind, human-boundary status, human decision status, authorized-future-unit status, forbidden-action boundaries, source pointers, and non-claims.

Compression may reduce display size. Compression may not create authority, erase human-boundary status, widen authorized-future-unit status, promote observed repetition into reusable schema, turn receipt existence into edge lawfulness, turn source-commit-only meta nodes into runtime receipts, or treat absent forbidden counters as proof that forbidden actions are impossible.

## Compression layers

- `DISPLAY_COMPRESSION` - shortens readout only - must decompress back to M1 address and M2 spine evidence fields
- `STRUCTURAL_COMPRESSION` - names a descriptive observed surface type - descriptive only; not authoritative
- `ROUTE_PATTERN_COMPRESSION` - names an observed ordered sequence - observed-pattern readout only; never a future runner rule

## Required decompression fields

- `node_id`
- `node_number`
- `node_kind`
- `edge_id`
- `edge_kind`
- `original_path_order`
- `receipt_backing_kind`
- `declared_receipt_id`
- `declared_receipt_path`
- `spine_status`
- `human_boundary_required`
- `human_decision_consumed`
- `authorized_future_unit`
- `forbidden_actions_explicitly_preserved`
- `commit_sha`
- `artifact_dir`
- `must_not_impersonate`
- `non_claims`

## Forbidden compressions

- `human_acceptance + authorized_future_unit -> auto_authorized` -> `COMPRESSION_REJECTED_AUTHORITY_LEAK`
- `receipt_exists -> edge_lawful` -> `COMPRESSION_REJECTED_EDGE_LAWFULNESS_LEAK`
- `repeated_transition -> schema_promoted` -> `COMPRESSION_REJECTED_SCHEMA_PROMOTION`
- `source_commit_only_meta_handoff -> runtime_receipt` -> `COMPRESSION_REJECTED_RECEIPT_IMPERSONATION`
- `closure_readiness -> proof_done` -> `COMPRESSION_REJECTED_AUTHORITY_LEAK`
- `bounded_execution -> runner_created` -> `COMPRESSION_REJECTED_AUTHORITY_LEAK`
- `taxonomy_label -> move_permission` -> `COMPRESSION_REJECTED_AUTHORITY_LEAK`
- `no_forbidden_counter_seen -> all_forbidden_actions_impossible` -> `COMPRESSION_REJECTED_AUTHORITY_LEAK`
- `observed route pattern -> future execution rule` -> `COMPRESSION_REJECTED_AUTHORITY_LEAK`

## Tiny v0 test suite

| test_id | input | expected | observed | result |
| --- | --- | --- | --- | --- |
| pass_node_c8_n17_bounded_patch_execution_surface | node c8.n17 -> bounded_patch_execution_surface | COMPRESSION_ADMISSIBLE_DISPLAY_ONLY | COMPRESSION_ADMISSIBLE_DISPLAY_ONLY | PASS |
| pass_sequence_c8_n01_to_n04_closure_to_successor_selection_sequence | nodes c8.n01-c8.n04 -> closure_to_successor_selection_sequence | COMPRESSION_ADMISSIBLE_OBSERVED_PATTERN_ONLY | COMPRESSION_ADMISSIBLE_OBSERVED_PATTERN_ONLY | PASS |
| fail_auto_successor_selection_authority_leak | nodes c8.n01-c8.n04 -> auto_successor_selection | COMPRESSION_REJECTED_AUTHORITY_LEAK | COMPRESSION_REJECTED_AUTHORITY_LEAK | PASS |
| fail_c8_n20_runtime_receipt_impersonation | node c8.n20 -> runtime_receipt_node | COMPRESSION_REJECTED_RECEIPT_IMPERSONATION | COMPRESSION_REJECTED_RECEIPT_IMPERSONATION | PASS |
| fail_repeated_human_acceptance_edges_schema_promotion | repeated human acceptance edges -> preapproved_reusable_schema | COMPRESSION_REJECTED_SCHEMA_PROMOTION | COMPRESSION_REJECTED_SCHEMA_PROMOTION | PASS |
| fail_receipt_backed_edge_lawful | receipt-backed edge -> edge_lawful | COMPRESSION_REJECTED_EDGE_LAWFULNESS_LEAK | COMPRESSION_REJECTED_EDGE_LAWFULNESS_LEAK | PASS |

## Acceptance gate

- law_status: `LAW_PASS_V0_TESTS`
- test_case_count: `6`
- compression_record_count: `6`
- Every admissible record resolves through M1/M2 and preserves non-authority boundaries.
- Every rejected record emits its expected rejection code.
- Taxonomy, future authority, reusable authority, runner creation, runtime replay, receipt truth validation, and edge lawfulness validation are all false.

## Non-claims

- M3 does not create taxonomy.
- M3 does not authorize moves.
- M3 does not promote schemas.
- M3 does not validate edge lawfulness.
- M3 does not replay runtime.
- M3 does not validate receipt content truth.
- M3 does not mechanize path updates.
- M3 does not create reusable/preapproved authority.
- M3 does not build a runner.
- M3 only defines v0 admissibility rules for decomposable compression over M1/M2 source-backed material.

## Relationship to M5

M5 names only what M3 can decompress safely.
