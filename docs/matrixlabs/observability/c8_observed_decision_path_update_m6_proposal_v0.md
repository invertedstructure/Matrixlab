# C8 Observed Decision Path Update Proposal - M6 v0

## Status

UPDATER_PROPOSAL_PASS

## Purpose

Proposal-only readout update for the observed C8 decision path.

## Source manifest

- Manifest path: `docs/matrixlabs/observability/observed_path_update_manifests/c8_m6_observed_path_update_manifest_v0.json`
- Update ID: `c8.m6_taxonomy_packet.observed_update.v0`

## Previous path

- Path file: `docs/matrixlabs/architecture/c8_observed_decision_path_v0.json`
- Expected terminal node: `c8.n21`
- Expected terminal node number: `21`

## New committed surface

- M6 commit SHA: `d21e162d7c52d57d8aa321434d533b99f7e46c23`
- Packet JSON: `docs/matrixlabs/c8/continuation/c8_taxonomy_applied_continuation_packet_v0.json`
- Packet Markdown: `docs/matrixlabs/c8/continuation/c8_taxonomy_applied_continuation_packet_v0.md`
- Generator: `scripts/build_c8_taxonomy_applied_continuation_packet_v0.py`

## Proposed node

- `node_id`: `c8.n22`
- `node_number`: `22`
- `phase`: `C8 taxonomy-applied continuation packet v0 prepared`
- `node_kind`: `taxonomy_applied_continuation_packet`
- `receipt_backing_kind`: `SOURCE_COMMIT_ONLY_PACKET_PREPARATION`
- `commit_sha`: `d21e162d7c52d57d8aa321434d533b99f7e46c23`
- `packet_status`: `PACKET_PREPARED`
- `taxonomy_use_status`: `DESCRIPTIVE_ONLY`
- `taxonomy_use_result`: `TAXONOMY_USE_PASS_WITH_ASSIGN_MIX`
- `primary_surface_type`: `surface.decision_packet.v0`
- `secondary_surface_types`: `['surface.human_acceptance.v0']`
- `human_boundary_status`: `REQUIRED_NOT_YET_CONSUMED`
- `authorized_future_unit_status`: `NOT_AUTHORIZED_BY_TAXONOMY_LABEL`
- `next_c8_unit_chosen_by_packet`: `False`
- `decision_path_updater_created`: `False`
- `runtime_probe_build_rerun_executed`: `False`
- `receipts_rewritten`: `False`
- `observation_role`: `prepared_packet_observed`
- `authority_created`: `False`

## Proposed edge

- `edge_id`: `c8.e21_22`
- `from_node_id`: `c8.n21`
- `to_node_id`: `c8.n22`
- `edge_kind`: `committed_packet_preparation_observed`
- `edge_status`: `OBSERVED_READOUT_EDGE_ONLY`
- `basis`: M6 packet committed at declared SHA, packet_status is PACKET_PREPARED, taxonomy label did not authorize future unit, human boundary remains required and not consumed
- `must_not_impersonate`: human acceptance edge, bounded execution edge, runtime receipt edge, next-unit authorization edge, decision updater authority

## Acceptance summary

- `authorized_future_unit_not_authorized_by_taxonomy`: `True`
- `decision_path_updater_created_false_in_observed_packet`: `True`
- `explicit_update_manifest_present`: `True`
- `forbidden_interpretations_absent`: `True`
- `human_boundary_required_not_consumed`: `True`
- `new_artifact_paths_declared`: `True`
- `new_artifact_paths_exist`: `True`
- `new_commit_declared`: `True`
- `new_commit_verified_in_git`: `True`
- `next_c8_unit_chosen_by_packet_false`: `True`
- `non_runtime_backing_kind_explicit`: `True`
- `packet_schema_matches`: `True`
- `packet_status_is_prepared`: `True`
- `path_files_modified`: `False`
- `previous_path_exists`: `True`
- `previous_terminal_node_matches`: `True`
- `proposed_edge_readout_only`: `True`
- `receipts_rewritten_false`: `True`
- `runtime_probe_build_rerun_executed_false`: `True`
- `taxonomy_use_result_allowed`: `True`
- `taxonomy_use_status_descriptive_only`: `True`

## Forbidden interpretations

- `next_c8_unit_chosen`
- `future_unit_authorized_by_taxonomy`
- `decision_path_updater_created_as_authority`
- `runtime_probe_build_rerun_executed`
- `receipts_rewritten`
- `schema_promoted`
- `human_acceptance_consumed`
- `runtime_receipt_backing_implied`

## Non-claims

- bounded_observed_decision_path_readout_updater_v0 does not choose the next C8 unit.
- It does not authorize future movement.
- It does not execute runtime probes.
- It does not rewrite receipts.
- It does not promote taxonomy labels.
- It does not create a move registry.
- It does not create runner authority.
- It does not validate theorem truth.
- It does not validate receipt truth.
- It does not validate edge lawfulness.
- It does not consume human acceptance.
- It does not apply the observed path update in proposal mode.
- It only proposes bounded readout updates from explicitly declared committed artifacts.

## Relationship to M7B

This proposal does not apply the path update. Apply mode is separate and future.
