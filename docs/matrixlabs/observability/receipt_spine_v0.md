# Receipt Spine v0

## Status

SPINE_PASS_WITH_SOURCE_COMMIT_ONLY_META_NODES

## Boundary

This spine validates receipt pointer/surface consistency only.

It does not validate runtime truth, edge lawfulness, compression, taxonomy, reusable authority, or future authorization.

## Source

- Source index path: `docs/matrixlabs/observability/decision_path_index_v0.json`
- Source observed path: `docs/matrixlabs/architecture/c8_observed_decision_path_v0.json`
- Source index SHA256: `626e95f48eca3ff517ff419d69d126af1069c67dfe9555d427fc436ccbcd3761`
- Observed path SHA256: `2883e4a86b2bbad9438f6694a4177e0e6db7d8e7b85b8ba1af098a4534a10cfd`
- Source index commit: `e0e22d33ee1fdfc9dad6964013162a58d6a0b169`
- Observed path commit: `11f8c9d20e30e1c4f614d7405ff2610baa382f6a`

## Coverage

- 21 indexed nodes
- 19 runtime receipt-backed nodes
- 2 source-commit-only meta-handoff nodes
- 0 missing receipts
- 0 parse failures
- 0 index/receipt field mismatches

## Node spine table

| node_id | phase | receipt_backing_kind | receipt_id | receipt_sig8 | status_match | terminal_stop_code_match | spine_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| c8.n01 | Runtime adoption closure packet | RUNTIME_RECEIPT | c8_runtime_adoption_bounded_probe_closu... | bba0fda3 | True | True | SPINE_NODE_PASS |
| c8.n02 | Runtime adoption closure acceptance | RUNTIME_RECEIPT | c8_runtime_adoption_bounded_probe_closu... | 6b22c2bc | True | True | SPINE_NODE_PASS |
| c8.n03 | Successor surface selection | RUNTIME_RECEIPT | c8_successor_surface_selection_receipt_... | 9d0dccc2 | True | True | SPINE_NODE_PASS |
| c8.n04 | Successor surface acceptance | RUNTIME_RECEIPT | c8_selected_successor_surface_acceptanc... | f9c3a26c | True | True | SPINE_NODE_PASS |
| c8.n05 | Unit-feedback hardening bounded probe prep | RUNTIME_RECEIPT | c8_unit_feedback_hardening_bounded_prob... | b8eb87c9 | True | True | SPINE_NODE_PASS |
| c8.n06 | Unit-feedback hardening bounded probe e... | RUNTIME_RECEIPT | c8_unit_feedback_hardening_bounded_prob... | ba4cb802 | True | None | SPINE_NODE_PASS |
| c8.n07 | Unit-feedback hardening bounded probe e... | RUNTIME_RECEIPT | c8_unit_feedback_hardening_bounded_prob... | c959d8ae | True | True | SPINE_NODE_PASS |
| c8.n08 | Failed-unit sample discovery | RUNTIME_RECEIPT | c8_unit_feedback_hardening_failed_unit_... | 18507876 | True | True | SPINE_NODE_PASS |
| c8.n09 | Failed-unit diagnostic assessment | RUNTIME_RECEIPT | c8_unit_feedback_hardening_failed_unit_... | 2433edbc | True | True | SPINE_NODE_PASS |
| c8.n10 | Unit-feedback hardening decision packet | RUNTIME_RECEIPT | c8_unit_feedback_hardening_decision_pac... | 2a767f83 | True | True | SPINE_NODE_PASS |
| c8.n11 | Source-status gap response | RUNTIME_RECEIPT | c8_unit_feedback_hardening_source_statu... | 5973119f | True | True | SPINE_NODE_PASS |
| c8.n12 | Bounded status-field decision acceptance | RUNTIME_RECEIPT | c8_unit_feedback_hardening_source_statu... | 88f4bb13 | True | True | SPINE_NODE_PASS |
| c8.n13 | Bounded source-status field decision pa... | RUNTIME_RECEIPT | c8_unit_feedback_hardening_bounded_sour... | d556ff6d | True | True | SPINE_NODE_PASS |
| c8.n14 | Local patch-plan acceptance | RUNTIME_RECEIPT | c8_unit_feedback_hardening_bounded_sour... | cb36477c | True | True | SPINE_NODE_PASS |
| c8.n15 | Local patch-plan packet | RUNTIME_RECEIPT | c8_unit_feedback_hardening_local_source... | 2ab3c487 | True | True | SPINE_NODE_PASS |
| c8.n16 | Bounded patch-execution acceptance | RUNTIME_RECEIPT | c8_unit_feedback_hardening_local_source... | b1270e7e | True | True | SPINE_NODE_PASS |
| c8.n17 | Bounded patch execution | RUNTIME_RECEIPT | c8_unit_feedback_hardening_local_source... | e478f1c5 | True | True | SPINE_NODE_PASS |
| c8.n18 | Closure-readiness packet | RUNTIME_RECEIPT | c8_unit_feedback_hardening_local_source... | a38b7e3e | True | True | SPINE_NODE_PASS |
| c8.n19 | Post-patch surface decision acceptance | RUNTIME_RECEIPT | c8_unit_feedback_hardening_local_source... | 62fad892 | True | True | SPINE_NODE_PASS |
| c8.n20 | Architecture extraction reference layer | SOURCE_COMMIT_ONLY_META_HANDOFF | source_commit_only_meta_handoff |  | None | None | SPINE_NODE_SOURCE_COMMIT_ONLY |
| c8.n21 | Baseline share packet generator | SOURCE_COMMIT_ONLY_META_HANDOFF | source_commit_only_meta_handoff |  | None | None | SPINE_NODE_SOURCE_COMMIT_ONLY |

## Source-commit-only meta nodes

- `c8.n20` - Architecture extraction reference layer - commit `9f2fd5cceee3badd1e5dd55910150fe1242252b3` - artifact `docs/matrixlabs`
- `c8.n21` - Baseline share packet generator - commit `24619b142b0b6a961532ced6f9458809e4c9ce7a` - artifact `baseline_share`

## Edge evidence overlay

- Edge evidence status counts: `{"EDGE_EVIDENCE_POINTER_PRESENT": 18, "EDGE_TOUCHES_SOURCE_COMMIT_ONLY_META_NODE": 2}`
- Edge records preserve evidence pointers only; they do not claim lawfulness.

| edge_id | from | to | evidence_status | evidence_path |
| --- | --- | --- | --- | --- |
| c8.e01_02 | c8.n01 | c8.n02 | EDGE_EVIDENCE_POINTER_PRESENT | data/c8_runtime_adoption_bounded_probe_closure_after_reentry_v0_recei... |
| c8.e02_03 | c8.n02 | c8.n03 | EDGE_EVIDENCE_POINTER_PRESENT | data/c8_runtime_adoption_bounded_probe_closure_acceptance_after_reent... |
| c8.e03_04 | c8.n03 | c8.n04 | EDGE_EVIDENCE_POINTER_PRESENT | data/c8_successor_surface_selection_after_runtime_adoption_closure_v0... |
| c8.e04_05 | c8.n04 | c8.n05 | EDGE_EVIDENCE_POINTER_PRESENT | data/c8_selected_successor_surface_acceptance_after_runtime_adoption_... |
| c8.e05_06 | c8.n05 | c8.n06 | EDGE_EVIDENCE_POINTER_PRESENT | data/c8_unit_feedback_hardening_bounded_probe_prep_after_runtime_adop... |
| c8.e06_07 | c8.n06 | c8.n07 | EDGE_EVIDENCE_POINTER_PRESENT | data/c8_unit_feedback_hardening_bounded_probe_execution_acceptance_af... |
| c8.e07_08 | c8.n07 | c8.n08 | EDGE_EVIDENCE_POINTER_PRESENT | data/c8_unit_feedback_hardening_bounded_probe_execution_after_runtime... |
| c8.e08_09 | c8.n08 | c8.n09 | EDGE_EVIDENCE_POINTER_PRESENT | data/c8_unit_feedback_hardening_failed_unit_sample_discovery_executio... |
| c8.e09_10 | c8.n09 | c8.n10 | EDGE_EVIDENCE_POINTER_PRESENT | data/c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessm... |
| c8.e10_11 | c8.n10 | c8.n11 | EDGE_EVIDENCE_POINTER_PRESENT | data/c8_unit_feedback_hardening_decision_packet_from_failed_unit_samp... |
| c8.e11_12 | c8.n11 | c8.n12 | EDGE_EVIDENCE_POINTER_PRESENT | data/c8_unit_feedback_hardening_source_status_gap_response_packet_aft... |
| c8.e12_13 | c8.n12 | c8.n13 | EDGE_EVIDENCE_POINTER_PRESENT | data/c8_unit_feedback_hardening_source_status_gap_response_packet_acc... |
| c8.e13_14 | c8.n13 | c8.n14 | EDGE_EVIDENCE_POINTER_PRESENT | data/c8_unit_feedback_hardening_bounded_source_status_field_decision_... |
| c8.e14_15 | c8.n14 | c8.n15 | EDGE_EVIDENCE_POINTER_PRESENT | data/c8_unit_feedback_hardening_bounded_source_status_field_decision_... |
| c8.e15_16 | c8.n15 | c8.n16 | EDGE_EVIDENCE_POINTER_PRESENT | data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_... |
| c8.e16_17 | c8.n16 | c8.n17 | EDGE_EVIDENCE_POINTER_PRESENT | data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_... |
| c8.e17_18 | c8.n17 | c8.n18 | EDGE_EVIDENCE_POINTER_PRESENT | data/c8_unit_feedback_hardening_local_source_status_field_patch_execu... |
| c8.e18_19 | c8.n18 | c8.n19 | EDGE_EVIDENCE_POINTER_PRESENT | data/c8_unit_feedback_hardening_local_source_status_field_patch_execu... |
| c8.e19_20 | c8.n19 | c8.n20 | EDGE_TOUCHES_SOURCE_COMMIT_ONLY_META_NODE | data/c8_unit_feedback_hardening_local_source_status_field_patch_execu... |
| c8.e20_21 | c8.n20 | c8.n21 | EDGE_TOUCHES_SOURCE_COMMIT_ONLY_META_NODE | docs/matrixlabs |

## Mismatches / warnings

- No field mismatches.

## Non-claims

- Does not replay the runtime.
- Does not validate that the receipt's runtime claim is operationally or mathematically true.
- Does not prove the edge from this node to the next is lawful.
- Does not decide whether authorized_future_unit was correctly consumed downstream.
- Does not classify proceed surfaces into taxonomy.
- Does not compress repeated transition patterns.
- Does not promote source-commit-only meta nodes into C8 runtime receipts.
- Does not authorize future units.
- Does not create reusable/preapproved authority.
- Does not build a runner.

## Relationship to M3

M2 gives M3 evidence-anchored addresses.
M3 defines what may be compressed and what decompression must recover.
