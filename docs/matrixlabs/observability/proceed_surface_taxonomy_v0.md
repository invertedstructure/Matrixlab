# Proceed Surface Taxonomy v0

## Status

TAXONOMY_V0_DESCRIPTIVE_ONLY

## Purpose

M5 is a zero-authority descriptive label registry for observed C8 proceed surfaces.

## Source

- M1 index: `docs/matrixlabs/observability/decision_path_index_v0.json`
  - SHA256: `626e95f48eca3ff517ff419d69d126af1069c67dfe9555d427fc436ccbcd3761`
  - Commit: `e0e22d33ee1fdfc9dad6964013162a58d6a0b169`
- M2 receipt spine: `docs/matrixlabs/observability/receipt_spine_v0.json`
  - SHA256: `ab781df8ed859a3b0e90dc120d546df3cfdbce0433352b8b0345db2e05029108`
  - Commit: `e78ae91156521669e57bfca3c112d4b83e681d05`
- M3 compression law: `docs/matrixlabs/observability/compression_decompression_law_v0.json`
  - SHA256: `1d19a317fa95ab813e05f60142f3c88b5dea1e32f26c66fd136e5317d530dd8e`
  - Commit: `58f4743e38a6d49e877a7d8b81f0a82c30ad0915`
- M4 preservation context commit: `6aa9070f2d7a845640a23370a742ee13723a3b51`
- M4 semantic dependency: `false`

## Core law

A proceed-surface label is admissible only when it resolves to M1 targets, resolves through M2 evidence or explicit source-commit-only meta status, decompresses through M3-required source fields, declares its weakest useful reading, declares what it must not impersonate, and creates no authority.

## Acceptance summary

- Label authority: `ZERO_AUTHORITY_DESCRIPTIVE_ONLY`
- Node targets considered: `21`
- Edge targets considered: `0`
- Sequence targets considered: `0`
- Assignments: `21`
- Withheld assignments: `0`
- M2 spine status: `SPINE_PASS_WITH_SOURCE_COMMIT_ONLY_META_NODES`

## Surface Families

- `SURFACE_PREP` - DESCRIPTIVE_GROUPING_ONLY
- `SURFACE_ACCEPTANCE` - DESCRIPTIVE_GROUPING_ONLY
- `SURFACE_SELECTION` - DESCRIPTIVE_GROUPING_ONLY
- `SURFACE_EXECUTION` - DESCRIPTIVE_GROUPING_ONLY
- `SURFACE_DISCOVERY` - DESCRIPTIVE_GROUPING_ONLY
- `SURFACE_DIAGNOSTIC` - DESCRIPTIVE_GROUPING_ONLY
- `SURFACE_DECISION` - DESCRIPTIVE_GROUPING_ONLY
- `SURFACE_PATCH` - DESCRIPTIVE_GROUPING_ONLY
- `SURFACE_CLOSURE` - DESCRIPTIVE_GROUPING_ONLY
- `SURFACE_EXTRACTION` - DESCRIPTIVE_GROUPING_ONLY
- `SURFACE_PROJECTION` - DESCRIPTIVE_GROUPING_ONLY
- `SURFACE_META_HANDOFF` - DESCRIPTIVE_GROUPING_ONLY
- `SURFACE_MIXED` - DESCRIPTIVE_GROUPING_ONLY

## Surface Types

| surface_type_id | label | family | smallest honest reading | must not impersonate |
| --- | --- | --- | --- | --- |
| `surface.closure_packet.v0` | `closure_packet_surface` | `SURFACE_PREP` | Observed packet/readout surface that prepares or states closure-readiness for a bounded unit. | runner move, future move authorization, schema promotion, proof of edge lawfulness, receipt truth validation, automatic permission to execute similar units, actual closure, proof success, future authorization, receipt validation |
| `surface.human_acceptance.v0` | `human_acceptance_surface` | `SURFACE_ACCEPTANCE` | Observed surface where a human acceptance or decision boundary is explicitly consumed. | runner move, future move authorization, schema promotion, proof of edge lawfulness, receipt truth validation, automatic permission to execute similar units, preapproval, reusable schema authority, automatic authorization, runner selection |
| `surface.successor_selection.v0` | `successor_selection_surface` | `SURFACE_SELECTION` | Observed surface where the next bounded successor object or unit is selected or proposed. | runner move, future move authorization, schema promotion, proof of edge lawfulness, receipt truth validation, automatic permission to execute similar units, automatic move selection, general successor rule, reusable next-unit authority |
| `surface.bounded_probe_prep.v0` | `bounded_probe_prep_surface` | `SURFACE_PREP` | Observed surface preparing a bounded probe with explicit scope. | runner move, future move authorization, schema promotion, proof of edge lawfulness, receipt truth validation, automatic permission to execute similar units, probe execution, successful result, permission to widen the probe |
| `surface.bounded_execution.v0` | `bounded_execution_surface` | `SURFACE_EXECUTION` | Observed surface where an already-bounded unit was executed and emitted a receipt/readout. | runner move, future move authorization, schema promotion, proof of edge lawfulness, receipt truth validation, automatic permission to execute similar units, runner authority, future execution permission, correctness of the executed unit |
| `surface.failed_unit_discovery.v0` | `failed_unit_discovery_surface` | `SURFACE_DISCOVERY` | Observed surface where a failed or insufficient unit/sample is identified for diagnostic use. | runner move, future move authorization, schema promotion, proof of edge lawfulness, receipt truth validation, automatic permission to execute similar units, complete failure taxonomy, proof of root cause, permission to repair broadly |
| `surface.diagnostic_assessment.v0` | `diagnostic_assessment_surface` | `SURFACE_DIAGNOSTIC` | Observed surface where a failure/readout is assessed into a diagnostic posture. | runner move, future move authorization, schema promotion, proof of edge lawfulness, receipt truth validation, automatic permission to execute similar units, final diagnosis, taxonomy promotion, automatic repair authority |
| `surface.decision_packet.v0` | `decision_packet_surface` | `SURFACE_DECISION` | Observed packet surface that packages a decision boundary, candidate next unit, or bounded action. | runner move, future move authorization, schema promotion, proof of edge lawfulness, receipt truth validation, automatic permission to execute similar units, human decision itself, acceptance, executable move authority |
| `surface.source_status_gap_response.v0` | `source_status_gap_response_surface` | `SURFACE_DIAGNOSTIC` | Observed surface responding to a mismatch or gap in source/status representation. | runner move, future move authorization, schema promotion, proof of edge lawfulness, receipt truth validation, automatic permission to execute similar units, semantic failure, theorem failure, broad source rewrite permission |
| `surface.bounded_status_field_decision.v0` | `bounded_status_field_decision_surface` | `SURFACE_DECISION` | Observed surface deciding a bounded source/status field change. | runner move, future move authorization, schema promotion, proof of edge lawfulness, receipt truth validation, automatic permission to execute similar units, general schema change, reusable field policy, broad source mutation authority |
| `surface.local_patch_plan.v0` | `local_patch_plan_surface` | `SURFACE_PATCH` | Observed surface specifying a local patch plan under bounded scope. | runner move, future move authorization, schema promotion, proof of edge lawfulness, receipt truth validation, automatic permission to execute similar units, patch execution, correctness of patch, permission to alter unrelated files |
| `surface.bounded_patch_execution.v0` | `bounded_patch_execution_surface` | `SURFACE_PATCH` | Observed surface where a bounded patch was executed and receipt/readout evidence was emitted. | runner move, future move authorization, schema promotion, proof of edge lawfulness, receipt truth validation, automatic permission to execute similar units, general patch authority, runner action, future patch permission |
| `surface.closure_readiness.v0` | `closure_readiness_surface` | `SURFACE_CLOSURE` | Observed surface stating readiness to close or move to preservation after bounded evidence. | runner move, future move authorization, schema promotion, proof of edge lawfulness, receipt truth validation, automatic permission to execute similar units, global completion, theorem closure, automatic next-stage authority |
| `surface.post_patch_decision.v0` | `post_patch_surface_decision_surface` | `SURFACE_DECISION` | Observed surface deciding what surface follows after a bounded patch. | runner move, future move authorization, schema promotion, proof of edge lawfulness, receipt truth validation, automatic permission to execute similar units, generic continuation policy, reusable successor rule, runner transition |
| `surface.architecture_extraction_reference.v0` | `architecture_extraction_reference_surface` | `SURFACE_EXTRACTION` | Observed source-commit/reference layer that extracts architecture/readout state into stable files. | runner move, future move authorization, schema promotion, proof of edge lawfulness, receipt truth validation, automatic permission to execute similar units, runtime receipt, theorem extraction, final architecture freeze |
| `surface.baseline_projection.v0` | `baseline_projection_surface` | `SURFACE_PROJECTION` | Observed surface where repo artifacts are projected into baseline_share for discussion/reference. | runner move, future move authorization, schema promotion, proof of edge lawfulness, receipt truth validation, automatic permission to execute similar units, authority creation, semantic validation, receipt rewriting |
| `surface.mixed_human_post_patch_decision.v0` | `mixed_human_post_patch_decision_surface` | `SURFACE_MIXED` | Observed mixed surface where human acceptance and post-patch surface decision roles appear together. | runner move, future move authorization, schema promotion, proof of edge lawfulness, receipt truth validation, automatic permission to execute similar units, automatic post-patch rule, preapproved continuation, reusable schema authorization |

## Assignments

| target_id | assignment_status | primary_surface_type | assigned_surface_types | confidence | basis |
| --- | --- | --- | --- | --- | --- |
| `c8.n01` | `ASSIGN` | `surface.closure_packet.v0` | `surface.closure_packet.v0` | `high` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, label does not widen authority |
| `c8.n02` | `ASSIGN_MIX` | `surface.successor_selection.v0` | `surface.human_acceptance.v0`, `surface.successor_selection.v0` | `medium` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, single pure label would hide multiple surface roles |
| `c8.n03` | `ASSIGN` | `surface.successor_selection.v0` | `surface.successor_selection.v0` | `high` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, label does not widen authority |
| `c8.n04` | `ASSIGN_MIX` | `surface.bounded_probe_prep.v0` | `surface.human_acceptance.v0`, `surface.bounded_probe_prep.v0` | `medium` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, single pure label would hide multiple surface roles |
| `c8.n05` | `ASSIGN` | `surface.bounded_probe_prep.v0` | `surface.bounded_probe_prep.v0` | `high` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, label does not widen authority |
| `c8.n06` | `ASSIGN_MIX` | `surface.bounded_execution.v0` | `surface.human_acceptance.v0`, `surface.bounded_execution.v0` | `medium` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, single pure label would hide multiple surface roles |
| `c8.n07` | `ASSIGN` | `surface.bounded_execution.v0` | `surface.bounded_execution.v0` | `high` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, label does not widen authority |
| `c8.n08` | `ASSIGN` | `surface.failed_unit_discovery.v0` | `surface.failed_unit_discovery.v0` | `high` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, label does not widen authority |
| `c8.n09` | `ASSIGN` | `surface.diagnostic_assessment.v0` | `surface.diagnostic_assessment.v0` | `high` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, label does not widen authority |
| `c8.n10` | `ASSIGN` | `surface.decision_packet.v0` | `surface.decision_packet.v0` | `high` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, label does not widen authority |
| `c8.n11` | `ASSIGN` | `surface.source_status_gap_response.v0` | `surface.source_status_gap_response.v0` | `high` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, label does not widen authority |
| `c8.n12` | `ASSIGN_MIX` | `surface.bounded_status_field_decision.v0` | `surface.human_acceptance.v0`, `surface.bounded_status_field_decision.v0` | `medium` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, single pure label would hide multiple surface roles |
| `c8.n13` | `ASSIGN` | `surface.bounded_status_field_decision.v0` | `surface.bounded_status_field_decision.v0` | `high` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, label does not widen authority |
| `c8.n14` | `ASSIGN_MIX` | `surface.local_patch_plan.v0` | `surface.human_acceptance.v0`, `surface.local_patch_plan.v0` | `medium` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, single pure label would hide multiple surface roles |
| `c8.n15` | `ASSIGN` | `surface.local_patch_plan.v0` | `surface.local_patch_plan.v0` | `high` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, label does not widen authority |
| `c8.n16` | `ASSIGN_MIX` | `surface.bounded_patch_execution.v0` | `surface.human_acceptance.v0`, `surface.bounded_patch_execution.v0` | `medium` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, single pure label would hide multiple surface roles |
| `c8.n17` | `ASSIGN` | `surface.bounded_patch_execution.v0` | `surface.bounded_patch_execution.v0` | `high` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, label does not widen authority |
| `c8.n18` | `ASSIGN` | `surface.closure_readiness.v0` | `surface.closure_readiness.v0` | `high` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, label does not widen authority |
| `c8.n19` | `ASSIGN_MIX` | `surface.mixed_human_post_patch_decision.v0` | `surface.human_acceptance.v0`, `surface.post_patch_decision.v0`, `surface.mixed_human_post_patch_decision.v0` | `medium` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, single pure label would hide multiple surface roles |
| `c8.n20` | `ASSIGN` | `surface.architecture_extraction_reference.v0` | `surface.architecture_extraction_reference.v0` | `high` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, label does not widen authority |
| `c8.n21` | `ASSIGN` | `surface.baseline_projection.v0` | `surface.baseline_projection.v0` | `high` | M1 target exists, M2 target has acceptable evidence/source status, M3 decompression recovers required fields, label does not widen authority |

## Withheld assignments

- None.

## Rejected Label Tests

| test_id | bad_label | expected_result | observed_result | pass/fail |
| --- | --- | --- | --- | --- |
| `reject_receipt_exists_edge_lawful` | A receipt pointer exists, therefore the edge is lawful. | `EDGE_LAWFULNESS_REJECTED` | `EDGE_LAWFULNESS_REJECTED` | `PASS` |
| `reject_human_acceptance_auto_authorized` | A human acceptance node authorizes future similar units. | `AUTHORITY_LEAK_REJECTED` | `AUTHORITY_LEAK_REJECTED` | `PASS` |
| `reject_bounded_execution_runner_move` | A bounded execution label is a runner move. | `RUNNER_IMPERSONATION_REJECTED` | `RUNNER_IMPERSONATION_REJECTED` | `PASS` |
| `reject_source_commit_only_meta_runtime_receipt` | A source-commit-only meta handoff is runtime receipt evidence. | `RECEIPT_IMPERSONATION_REJECTED` | `RECEIPT_IMPERSONATION_REJECTED` | `PASS` |
| `reject_repeated_surface_reusable_schema` | A repeated surface label is a reusable promoted schema. | `SCHEMA_PROMOTION_REJECTED` | `SCHEMA_PROMOTION_REJECTED` | `PASS` |
| `reject_baseline_projection_semantic_validation` | A baseline projection label validates semantic truth. | `SEMANTIC_VALIDATION_REJECTED` | `SEMANTIC_VALIDATION_REJECTED` | `PASS` |

## Relationship to M6

M6 uses this vocabulary once in one live continuation packet.

## Relationship to M7

M7 must not treat M5 labels as transition rules.

## Non-Claims

- proceed_surface_taxonomy_v0 does not create lawful moves.
- proceed_surface_taxonomy_v0 does not authorize future units.
- proceed_surface_taxonomy_v0 does not promote reusable schemas.
- proceed_surface_taxonomy_v0 does not prove edge lawfulness.
- proceed_surface_taxonomy_v0 does not validate receipts.
- proceed_surface_taxonomy_v0 does not validate runtime truth.
- proceed_surface_taxonomy_v0 does not choose next C8 continuation.
- proceed_surface_taxonomy_v0 does not create a decision-path updater.
- proceed_surface_taxonomy_v0 does not turn human acceptance into preapproval.
- proceed_surface_taxonomy_v0 does not turn source-commit-only meta handoff into runtime receipt evidence.
- proceed_surface_taxonomy_v0 only labels observed, source-backed proceed surfaces for readout and discussion.
