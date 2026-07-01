# Decision Path Index v0

## Status

Source-preserving lookup surface. Shape-only validation. Not authority.

## Source

- Source JSON: `docs/matrixlabs/architecture/c8_observed_decision_path_v0.json`
- Source Markdown: `docs/matrixlabs/architecture/c8_observed_decision_path_v0.md`
- Source schema: `matrixlabs_c8_observed_decision_path_v0`
- Source readout status: `observed_source_backed_not_runner`
- Source JSON SHA256: `2883e4a86b2bbad9438f6694a4177e0e6db7d8e7b85b8ba1af098a4534a10cfd`
- Source commit SHA: `11f8c9d20e30e1c4f614d7405ff2610baa382f6a`

## Address contract

- Node IDs are stable within c8_observed_decision_path_v0: c8.n01 ... c8.n21.
- Edge IDs are stable within c8_observed_decision_path_v0: c8.e01_02 ... c8.e20_21.
- These IDs are not claimed as global permanent IDs across future rewritten or separately observed paths.

## Compact counts

- node_count: `21`
- edge_count: `20`
- node kind counts: `{"bounded_execution": 3, "closure_readiness": 2, "human_acceptance": 7, "meta_handoff": 2, "packet_creation": 6, "surface_selection": 1}`
- edge kind counts: `{"authorized_future_unit": 6, "human_acceptance": 7, "meta_transition": 1, "receipt_chain": 5, "review_then_commit": 1}`
- human boundary counts: `{"not_required": 5, "required": 16, "unknown_or_null": 0}`
- authorized future unit counts: `{"absent": 0, "present": 18, "unknown_or_null": 3}`

## Node index

| node_id | node_number | node_kind | phase | receipt_id | commit_sha | human_boundary_required | authorized_future_unit |
| --- | ---: | --- | --- | --- | --- | --- | --- |
| c8.n01 | 1 | closure_readiness | Runtime adoption closure packet | c8_runtime_adoption_bounded_probe_closure... | eb9916d84... | True |  |
| c8.n02 | 2 | human_acceptance | Runtime adoption closure acceptance | c8_runtime_adoption_bounded_probe_closure... | ad79831da... | True | CREATE_C8_RETURN_TO_SURFACE_SELECTION_PACKET_AFTER_... |
| c8.n03 | 3 | surface_selection | Successor surface selection | c8_successor_surface_selection_receipt_5a... | 09fd897d0... | True | SELECT_C8_SUCCESSOR_SURFACE_AFTER_RUNTIME_ADOPTION_... |
| c8.n04 | 4 | human_acceptance | Successor surface acceptance | c8_selected_successor_surface_acceptance_... | 86722db21... | True | CREATE_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PRE... |
| c8.n05 | 5 | packet_creation | Unit-feedback hardening bounded probe prep | c8_unit_feedback_hardening_bounded_probe_... | b52ed4c3e... | True | CREATE_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PRE... |
| c8.n06 | 6 | human_acceptance | Unit-feedback hardening bounded probe execution acceptance | c8_unit_feedback_hardening_bounded_probe_... | 41f876f7a... | True | EXECUTE_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_ON... |
| c8.n07 | 7 | bounded_execution | Unit-feedback hardening bounded probe execution | c8_unit_feedback_hardening_bounded_probe_... | 0daf2585b... | False | EXECUTE_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_ON... |
| c8.n08 | 8 | bounded_execution | Failed-unit sample discovery | c8_unit_feedback_hardening_failed_unit_sa... | f9dbfc92c... | False | EXECUTE_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMP... |
| c8.n09 | 9 | packet_creation | Failed-unit diagnostic assessment | c8_unit_feedback_hardening_failed_unit_sa... | 52cd947bd... | True | CREATE_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPL... |
| c8.n10 | 10 | packet_creation | Unit-feedback hardening decision packet | c8_unit_feedback_hardening_decision_packe... | 9710da851... | True | CREATE_C8_UNIT_FEEDBACK_HARDENING_DECISION_PACKET_F... |
| c8.n11 | 11 | packet_creation | Source-status gap response | c8_unit_feedback_hardening_source_status_... | f8d9b27d3... | True | CREATE_C8_UNIT_FEEDBACK_HARDENING_SOURCE_STATUS_GAP... |
| c8.n12 | 12 | human_acceptance | Bounded status-field decision acceptance | c8_unit_feedback_hardening_source_status_... | 275a80b29... | True | CREATE_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_SOURCE_ST... |
| c8.n13 | 13 | packet_creation | Bounded source-status field decision packet | c8_unit_feedback_hardening_bounded_source... | d65de6623... | True | CREATE_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_SOURCE_ST... |
| c8.n14 | 14 | human_acceptance | Local patch-plan acceptance | c8_unit_feedback_hardening_bounded_source... | fcf51cb86... | True | CREATE_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STAT... |
| c8.n15 | 15 | packet_creation | Local patch-plan packet | c8_unit_feedback_hardening_local_source_s... | 60553debf... | True | CREATE_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STAT... |
| c8.n16 | 16 | human_acceptance | Bounded patch-execution acceptance | c8_unit_feedback_hardening_local_source_s... | 654c2d79d... | True | EXECUTE_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STA... |
| c8.n17 | 17 | bounded_execution | Bounded patch execution | c8_unit_feedback_hardening_local_source_s... | e801c5f76... | False | EXECUTE_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STA... |
| c8.n18 | 18 | closure_readiness | Closure-readiness packet | c8_unit_feedback_hardening_local_source_s... | 4df5f80df... | True | CREATE_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STAT... |
| c8.n19 | 19 | human_acceptance | Post-patch surface decision acceptance | c8_unit_feedback_hardening_local_source_s... | a370223f0... | True | CREATE_C8_UNIT_FEEDBACK_HARDENING_POST_SOURCE_STATU... |
| c8.n20 | 20 | meta_handoff | Architecture extraction reference layer | source_commit_only_meta_handoff | 9f2fd5cce... | False |  |
| c8.n21 | 21 | meta_handoff | Baseline share packet generator | source_commit_only_meta_handoff | 24619b142... | False |  |

## Edge index

| edge_id | from | to | edge_kind | source_evidence_path |
| --- | --- | --- | --- | --- |
| c8.e01_02 | c8.n01 | c8.n02 | human_acceptance | data/c8_runtime_adoption_bounded_probe_closure_after_reentry_v0_receipts/c8_runti... |
| c8.e02_03 | c8.n02 | c8.n03 | authorized_future_unit | data/c8_runtime_adoption_bounded_probe_closure_acceptance_after_reentry_v0_receip... |
| c8.e03_04 | c8.n03 | c8.n04 | human_acceptance | data/c8_successor_surface_selection_after_runtime_adoption_closure_v0_receipts/c8... |
| c8.e04_05 | c8.n04 | c8.n05 | authorized_future_unit | data/c8_selected_successor_surface_acceptance_after_runtime_adoption_closure_v0_r... |
| c8.e05_06 | c8.n05 | c8.n06 | human_acceptance | data/c8_unit_feedback_hardening_bounded_probe_prep_after_runtime_adoption_closure... |
| c8.e06_07 | c8.n06 | c8.n07 | authorized_future_unit | data/c8_unit_feedback_hardening_bounded_probe_execution_acceptance_after_runtime_... |
| c8.e07_08 | c8.n07 | c8.n08 | review_then_commit | data/c8_unit_feedback_hardening_bounded_probe_execution_after_runtime_adoption_cl... |
| c8.e08_09 | c8.n08 | c8.n09 | receipt_chain | data/c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_after_runt... |
| c8.e09_10 | c8.n09 | c8.n10 | receipt_chain | data/c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_after_ru... |
| c8.e10_11 | c8.n10 | c8.n11 | receipt_chain | data/c8_unit_feedback_hardening_decision_packet_from_failed_unit_sample_diagnosti... |
| c8.e11_12 | c8.n11 | c8.n12 | human_acceptance | data/c8_unit_feedback_hardening_source_status_gap_response_packet_after_runtime_a... |
| c8.e12_13 | c8.n12 | c8.n13 | authorized_future_unit | data/c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_... |
| c8.e13_14 | c8.n13 | c8.n14 | human_acceptance | data/c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_after... |
| c8.e14_15 | c8.n14 | c8.n15 | authorized_future_unit | data/c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_accep... |
| c8.e15_16 | c8.n15 | c8.n16 | human_acceptance | data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_after... |
| c8.e16_17 | c8.n16 | c8.n17 | authorized_future_unit | data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_accep... |
| c8.e17_18 | c8.n17 | c8.n18 | receipt_chain | data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_once_af... |
| c8.e18_19 | c8.n18 | c8.n19 | human_acceptance | data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure... |
| c8.e19_20 | c8.n19 | c8.n20 | meta_transition | data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure... |
| c8.e20_21 | c8.n20 | c8.n21 | receipt_chain | docs/matrixlabs |

## Lookup tables

- lookup_by_node_id: `21` entries
- lookup_by_edge_id: `20` entries
- lookup_by_node_kind: `{"bounded_execution": 3, "closure_readiness": 2, "human_acceptance": 7, "meta_handoff": 2, "packet_creation": 6, "surface_selection": 1}`
- lookup_by_edge_kind: `{"authorized_future_unit": 6, "human_acceptance": 7, "meta_transition": 1, "receipt_chain": 5, "review_then_commit": 1}`
- lookup_by_human_boundary: `{"not_required": 5, "required": 16, "unknown_or_null": 0}`
- lookup_by_authorized_future_unit_present: `{"absent": 0, "present": 18, "unknown_or_null": 3}`
- lookup_by_receipt_id: `20` keys
- lookup_by_commit_sha: `21` keys
- optional lookup_by_phase: `21` keys
- optional lookup_by_terminal_stop_code: `18` keys
- optional lookup_by_outcome_class: `20` keys
- optional lookup_by_status: `20` keys

## Validation depth

- index_status: `PASS_SHAPE`
- validation_depth: `index_shape_only`
- receipt_validation_performed: `False`
- receipt_hash_validation_performed: `False`
- authority_validation_performed: `False`
- compression_validation_performed: `False`
- taxonomy_validation_performed: `False`
- node_ids_unique: `True`
- edge_ids_unique: `True`
- node_numbers_contiguous: `True`
- edges_forward_linear: `True`
- edge_endpoints_resolve: `True`

## Non-claims

- decision_path_index_v0 does not validate receipt contents.
- decision_path_index_v0 does not hash or verify receipt files.
- decision_path_index_v0 does not prove edge lawfulness.
- decision_path_index_v0 does not authorize future moves.
- decision_path_index_v0 does not promote repeated node kinds or edge kinds into reusable schema.
- decision_path_index_v0 does not classify proceed-surface taxonomy.
- decision_path_index_v0 does not decide compression or decompression law.
- decision_path_index_v0 only makes the observed C8 path addressable.

## Relationship to later milestones

- M1 gives stable addresses.
- M2 uses those addresses to build the receipt spine.
- M3 defines what may be compressed and decompressed from those addresses.
- M5 uses M1 and M3 to name proceed-surface roles without authority leak.
- M7 may later update the index mechanically from committed source artifacts, but only after indexing and compression laws are tested.
