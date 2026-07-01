# Code Map

This is a map, not the full source. The repository remains the source of truth.

## Main source directories

- `data/` - packet, generated artifact, and receipt-backed evidence surface.
- `scripts/` - repeatable unit scripts and generators. The baseline generator is `scripts/build_baseline_share_v0.py`.
- `docs/matrixlabs/` - source-backed architecture extraction/readout layer.
- `docs/matrixlabs/observability/` - generated source-preserving lookup surfaces.
- `baseline_share/` - generated uploadable projection, not source of truth.

## Important architecture docs

- `docs/matrixlabs/INDEX.md`
- `docs/matrixlabs/architecture/current_architecture_readout_v0.md`
- `docs/matrixlabs/architecture/source_map_v0.md`
- `docs/matrixlabs/architecture/decision_graph_readout_v0.md`
- `docs/matrixlabs/proposals/extraction_followup_questions_v0.md`
- `docs/matrixlabs/raw/source_inventory_v0.md`
- `docs/matrixlabs/observability/decision_path_index_v0.json`
- `docs/matrixlabs/observability/decision_path_index_v0.md`

## Current C8 source-status / post-patch surface decision paths

- `data/c8_unit_feedback_hardening_source_status_gap_response_packet_after_runtime_adoption_closure_v0` - present
- `data/c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_after_runtime_adoption_closure_v0` - present
- `data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_after_runtime_adoption_closure_v0` - present
- `data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_once_after_runtime_adoption_closure_v0` - present
- `data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_after_runtime_adoption_closure_v0` - present
- `data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_after_runtime_adoption_closure_v0` - present
- `data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_after_runtime_adoption_closure_v0_receipts` - present

## Generator

- `scripts/build_baseline_share_v0.py` - standard-library generator for this packet.

## Boundary note

This map is a portable orientation layer. It does not copy the full source, rewrite receipts, promote schemas, or authorize execution.
