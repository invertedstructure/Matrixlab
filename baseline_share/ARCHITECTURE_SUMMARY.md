# Architecture Summary

Source: `docs/matrixlabs/architecture/current_architecture_readout_v0.md`.

This summary preserves source-backed distinctions and does not promote schemas, authorize execution, or turn candidates into implemented architecture.

## Cell 0 / Lawful Admissibility Boundary

Source-backed surfaces:

- `data/b1_cell0_local_lawful_actor_stabilization_v0/`
- `data/b2_cell0_informative_failure_progress_classifier_v0/`
- `data/b3_cell0_local_decision_loop_schema_lock_v0/`
- `data/bounded_capability_proposal_validation_path_prep_v0/bounded_capability_proposal_lawful_admissibility_contract_v0.json`

Cell 0 appears as a local lawful actor / inspection / typed-stop layer. It classifies pressure, records local move results, stops at authority boundaries, and preserves distinctions rather than converting uncertainty into action. The B2 failure classifier explicitly avoids treating failure as automatic progress; it asks what got sharper, what did not change, whether retry is lawful, and what next handling is allowed.

Lawful admissibility is source-backed in proposal validation/admissibility contracts and repairs. The evidence supports bounded admissibility around specific proposals and validation paths, not a global license to execute or promote schemas.

## Builder Cell / Cell 1

Source-backed surfaces:

- `data/c4_cell1_receipt_native_builder_v0/`
- `data/c4_cell1_receipt_native_builder_preflight_rerun_v0/`
- `data/cell1_*`
- `scripts/build_c4_cell1_receipt_native_builder_v0.py`

Cell 1/builder surfaces are visible as receipt-native builder, preflight, schema-consumption, handoff-return, runtime patch target, value-source metadata, partial-schema-aware rebind, and one-time application chains. The C1 proposal layer is not Cell 1 execution: `data/c1_cell0_proposal_layer_v0/proposal_packet_records_v0.jsonl` says proposed-only packets cannot approve, apply, mutate, register, build, or verify.

## Schema Validator / Lawful Admissibility Cell

Source-backed surfaces:

- `data/runtime_schema_validator_cell_v0/`
- `data/runtime_schema_validator_cell_review_v0/`
- `data/runtime_schema_validator_cell_reference_closure_v0/`
- `data/post_runtime_schema_validator_reference_decision_v0/`
- `scripts/build_runtime_schema_validator_cell_v0.py`

A runtime schema validator cell exists as a built/reviewed/reference-closure chain. Lawful admissibility surfaces exist alongside it in bounded proposal validation paths. This extraction does not collapse them into one formal reusable cell unless a future source-backed authority says so.

## Receipt / Scribe Layer

Source-backed receipt layer:

- `data/*_receipts/`
- `/home/asd/matrixlab_receipts/`, copied to `docs/matrixlabs/receipts/`
- root receipt-like output files such as `matrixlab_full_normal_receipt_20260618_190803.txt`

Receipts are load-bearing evidence, not interpretation. They record unit IDs, gates, source receipt IDs, negative controls, scope, allowed and forbidden actions, and stop packets. This extraction copied external receipts verbatim and did not rewrite them.

The word `scribe` was not confirmed as a central formal component during this pass. Treat `Receipt/Scribe layer` as receipt-backed with `scribe` needing source confirmation unless a later pass finds explicit source files.

## Human Readout Packet Layer

Source-backed surfaces include many `*_readout_v0.json`, `*_report.json`, `*_profile_v0.json`, and `*_human_decision_*` files. Human decision packets are common in bounded adoption, schema promotion, source-status decisions, and C8 acceptances.

The pattern is bounded: packets ask or record a human decision, often prepare the next packet, and explicitly do not execute side effects unless a later execution unit is separately authorized and receipted.

## Typed Stops And Halt Vocabulary

Source-backed surfaces:

- `data/b1_cell0_local_lawful_actor_stabilization_v0/cell0_typed_stop_schema_v0.json`
- `data/b1_cell0_local_lawful_actor_stabilization_v0/cell0_local_move_result_records_v0.jsonl`
- `data/c7_synthetic_radius_negative_halts_b_c_v0/`
- `scripts/build_halt_vocabulary_v0_policy_v0.py`

Typed stops/halt vocabulary appear in Cell 0 local move results, C7 negative halts, runtime radius stop packets, and C8 feedback hardening surfaces. They preserve stop codes and reasons instead of silently turning stops into commands.

## Missing-object And Missing-instrument Capability Boundaries

Source-backed surfaces:

- `data/a0_a1_candidate_missing_object_question_resolution_v0/`
- `data/candidate_missing_object_proposal_layer_for_expected_limits_v0/`
- `data/capability_stop_packet_to_bounded_proposal_v0/`
- `data/c8_missing_instrument_proposal_review_v0/`
- `data/c8_bounded_instrument_build_packet_prep_v0/`
- `data/c8_accepted_instrument_build_packet_v0/`

Missing object is treated as a candidate/proposal or question surface, not as confirmed identity. Missing instrument appears in C8 instrument proposal/build packet surfaces. Both are capability boundaries requiring explicit proposal/review/acceptance/execution chains.

Terminology note: `missing-object capability boundary` means the boundary where an absent, unresolved, or insufficiently sourced object cannot be repaired, introduced, executed, promoted, or treated as available until its source surface, authority boundary, capability status, and lawful next handling are explicit.

## Source Surfaces And Source-status Gaps

Source surfaces are explicit in A0/A1 frontier files and C8 unit-feedback hardening. Evidence includes `question_resolution_source_surface.json`, `a0_a1_explicit_frontier_source_surface.json`, and C8 source-status gap response packets.

The C8 unit-feedback hardening chain found a local source-status field gap: failed unit samples could be useful feedback but still lacked a machine-readable local `source_status` field. The chain responded by preserving the missing marker, creating bounded decision packets, preparing a local patch plan, executing one bounded patch, reviewing closure readiness, and then preparing for a post-patch surface decision.

## One-time Acceptance Vs Reusable Schema Authorization

The repo repeatedly distinguishes bounded human acceptance from reusable/preapproved schema authority.

Examples:

- `data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_schema_promotion_path_v0/` says human selection opens only a schema-promotion decision-packet preparation path and does not mutate or promote a schema archive.
- `data/c8_successor_surface_bounded_probe_prep_acceptance_v0/` says acceptance authorizes exactly one bounded probe-prep packet and does not execute a probe.
- `data/c8_runtime_adoption_surface_bounded_probe_prep_after_reentry_v0/` and related acceptance files explicitly avoid pre-authorizing build, probe execution, C8 rerun, or reusable schema promotion.

Therefore: one-time acceptance authorizes only the stated bounded frame. Reusable/preapproved schema authorization requires explicit future validator/admissibility/human-governed promotion and receipt evidence.

## Runtime Adoption Chain

Source-backed C8 runtime adoption chain:

- `data/c8_successor_surface_selection_after_reentry_v0/`
- `data/c8_runtime_adoption_surface_bounded_probe_prep_after_reentry_v0/`
- `data/c8_runtime_adoption_surface_probe_prep_acceptance_after_reentry_v0/`
- `data/c8_runtime_adoption_bounded_probe_execution_after_reentry_v0/`
- `data/c8_runtime_adoption_bounded_probe_execution_acceptance_after_reentry_v0/`
- `data/c8_runtime_adoption_bounded_probe_closure_after_reentry_v0/`
- `data/c8_runtime_adoption_bounded_probe_closure_acceptance_after_reentry_v0/`

The chain selects a runtime-adoption surface, prepares a bounded probe, accepts prep, executes bounded probe, accepts execution, closes, and accepts closure. It is not evidence of general runtime adoption authority beyond the receipted chain.

## Unit-feedback Hardening Chain

Source-backed surfaces:

- `data/c8_successor_surface_selection_after_runtime_adoption_closure_v0/`
- `data/c8_unit_feedback_hardening_bounded_probe_prep_after_runtime_adoption_closure_v0/`
- `data/c8_unit_feedback_hardening_bounded_probe_execution_after_runtime_adoption_closure_v0/`
- `data/c8_unit_feedback_hardening_failed_unit_sample_discovery_*`
- `data/c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_*`
- `data/c8_unit_feedback_hardening_failed_unit_sample_gap_response_*`

This chain asks whether typed stops and failed units provide useful diagnostic feedback beyond status alone: why failure happened, where it happened, relative to which object/source surface/authority boundary/missing capability, and what refinement would allow lawful progress.

## Local Source-status Field Patch Chain

Source-backed surfaces:

- `data/c8_unit_feedback_hardening_source_status_gap_response_packet_after_runtime_adoption_closure_v0/`
- `data/c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_after_runtime_adoption_closure_v0/`
- `data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_after_runtime_adoption_closure_v0/`
- `data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_once_after_runtime_adoption_closure_v0/`
- `data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_after_runtime_adoption_closure_v0/`

The patch chain is local and bounded. Receipts indicate no schema discovery/probe/build/rerun where prohibited. Closure readiness means ready for post-patch surface decision; it does not itself execute a future unit.

## Post-patch Surface Decision Chain

Present and source-backed:

- `data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_after_runtime_adoption_closure_v0/`
- `data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_after_runtime_adoption_closure_v0_receipts/`
- `scripts/accept_c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_for_post_patch_surface_decision_after_runtime_adoption_closure_v0.py`

This is a post-patch surface decision acceptance/readiness chain, not a C8 rerun. Existing files were already staged before this extraction and were not mutated.

## Decision Graph Compression Candidates

The recurring pattern is visible enough to propose compression candidates, but not to implement them:

- packet creation/review/acceptance as a reusable observation pattern;
- bounded execution followed by execution review/acceptance;
- closure/readiness packet followed by post-closure or post-patch decision surface;
- receipt inventory/lineage validation across packet chains.

These are candidates only. Authority-sensitive steps, human decisions, schema promotion, archive mutation, runtime adoption, and rerun/probe/build execution must not be compressed into reusable/preapproved authority without explicit future validation and human-governed promotion.
