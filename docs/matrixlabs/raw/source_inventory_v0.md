# MatrixLabs Source Inventory v0

Extraction date: 2026-06-30.
Active repo root: `/home/asd/projects/matrixlab` in WSL distro `MatrixLabRescue`.

## Required discovery status

- `pwd`: `/home/asd/projects/matrixlab`.
- Repo root: `/home/asd/projects/matrixlab`.
- `git status --short` before extraction showed pre-existing changes in `.gitignore`, staged C8 post-patch decision files, and `scripts/accept_c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_for_post_patch_surface_decision_after_runtime_adoption_closure_v0.py`.
- Visible/tracked-or-unignored file count from `git ls-files -co --exclude-standard`: 15303.
- Top-level `data/` directories: 1015.
- Top-level `data/*receipts*` directories: 466.
- Top-level `scripts/` files: 455.
- `docs/`: absent before this extraction, created by this pass.
- `logs/`: absent during this pass.
- `/home/asd/matrixlab_receipts/`: present and copied.

## Source directories and files discovered

| Surface | Classification | Notes |
| --- | --- | --- |
| `data/` | generated artifact / packet archive / receipt-backed evidence | Main architecture evidence surface. Contains packet families, reports, readouts, transition traces, receipts, C0/C1/C8 chains, runtime validator surfaces, Cell1 surfaces, and graph/archive surfaces. |
| `data/*_receipts/` | receipt evidence | 466 receipt directories under `data/`. These are repo-resident receipts and were not rewritten. |
| `scripts/` | script | 455 scripts. Names show build, create, accept, execute, review, close, patch, audit, and rerun units. Scripts were inspected by name/search only and not executed. |
| `src/matrixlab/` | source code | Contains `cli.py`, jurisdiction runners, proceed adapter, trace ledger, and post-closure harvest module. Runtime/project commands were not run. |
| `tests/` | test source | Present and searched as source surface; tests were not run. |
| `configs/` | source/config | Present and searched as configuration evidence. |
| `README.md`, `pyproject.toml`, `uv.lock` | source/config | Project metadata surfaces. |
| root `matrixlab_full_normal_receipt_20260618_190803.txt` and root debug/output text files | raw/generative residue | Root-level receipt/output files exist; not promoted to architecture by themselves. |
| `.matrixlab_tmp/`, `.pytest_cache/`, `.venv/`, `__pycache__` | ignored/generated/local environment | Not used as architecture evidence. |
| `docs/matrixlabs/` | interpreted readout/raw copied evidence | Created by this extraction pass. |

## Important data packet families discovered

Representative packet families visible in `data/` include:

- `a0_receipt_to_builder_transition_layer_v0` and `a0_*frontier*` families: A0 receipt-to-builder/frontier classification and source-surface handling.
- `a1_strategic_decision_packet_layer_v0`: A1 packet and decision mapping layer.
- `b1_cell0_local_lawful_actor_stabilization_v0`, `b2_cell0_informative_failure_progress_classifier_v0`, `b3_cell0_local_decision_loop_schema_lock_v0`: Cell 0/lawful actor, failure feedback, and local decision loop surfaces.
- `c1_cell0_proposal_layer_v0`, `c2_cell0_label_taxonomy_lane_cleaning_v0`, `c3_cell0_micro_domain_shift_rehearsal_v0`: C1/C2/C3 proposal and taxonomy/shift surfaces.
- `c4_cell1_receipt_native_builder_v0` and `c4_cell1_receipt_native_builder_preflight_rerun_v0`: Cell 1/builder surfaces.
- `runtime_schema_validator_cell_v0`, `runtime_schema_validator_cell_review_v0`, `runtime_schema_validator_cell_reference_closure_v0`, and `post_runtime_schema_validator_reference_decision_v0`: runtime schema validator cell surfaces.
- `decision_graph_observation_archive_v0`: graph observation/archive surface.
- `bounded_structured_t6_trigger_surface_capability_*`: capability, adoption, human decision, schema archive promotion, mutation target, write authorization, and write execution surfaces.
- `c7_*runtime_radius*`: synthetic/runtime radius contracts, fixtures, runners, negative halts, handoff/feedback, and rollups.
- `c8_*`: target shape, interlock, successor surface, runtime adoption, reuse authority, unit feedback hardening, local source-status field patch, closure readiness, and post-patch surface decision chains.
- `cell1_*`: Cell1 runtime patch target, schema consumption, handoff-return, value-source metadata, partial-schema-aware rebind, and one-time application surfaces.
- `o2_unit_feedback_hardening_*`: unit feedback hardening target/review/closure surfaces.

## Important scripts discovered

Representative scripts include:

- A0/A1: `scripts/a0_receipt_to_builder_transition_layer_v0.py`, `scripts/a1_strategic_decision_packet_layer_v0.py`, `scripts/apply_a0_to_current_receipt_chain_frontier_v0.py`, `scripts/apply_a0_a1_to_explicit_current_frontier_receipt_v0.py`.
- Cell 0: `scripts/build_b1_cell0_local_lawful_actor_stabilization_v0.py`, `scripts/build_b2_cell0_informative_failure_progress_classifier_v0.py`, `scripts/build_b3_cell0_local_decision_loop_schema_lock_v0.py`, `scripts/build_c1_cell0_proposal_layer_v0.py`.
- Cell 1/builder: `scripts/build_c4_cell1_receipt_native_builder_v0.py`, `scripts/rerun_c4_cell1_receipt_native_builder_preflight_v0.py`, `scripts/design_cell1_minimal_runtime_patch_test_precheck_v0.py`.
- Runtime/validator: `scripts/build_runtime_schema_validator_cell_v0.py`, `scripts/close_runtime_schema_validator_cell_as_reviewed_reference_v0.py`, `scripts/build_runtime_observability_sidecar_v0.py`, `scripts/build_runtime_observability_and_feedback_attachment_v0.py`.
- Decision graph/archive: `scripts/build_decision_graph_observation_archive_v0.py`.
- C8: many `create_c8_*`, `accept_c8_*`, `execute_c8_*`, and `rerun_c8_*` scripts. They were not executed.
- Source-status/unit feedback: `scripts/create_c8_unit_feedback_hardening_*`, `scripts/accept_c8_unit_feedback_hardening_*`, and `scripts/execute_c8_unit_feedback_hardening_*` scripts.

## Receipt directories discovered

- `/home/asd/matrixlab_receipts/`: external WSL receipt archive; copied into `docs/matrixlabs/receipts/`; 714 files.
- `data/*_receipts/`: 466 repo-resident receipt directories; inspected as source evidence but not copied elsewhere.
- Root `matrixlab_full_normal_receipt_20260618_190803.txt`: raw root receipt-like file; not copied.

## Inaccessible or missing expected source surfaces

- `docs/` did not exist before this extraction layer.
- `logs/` did not exist in the active repo during this pass.
- Phase7 was not found by visible filename/term search and remains uncertain.
- Terminal/chat residue outside the attached request was not directly accessible.
- C-drive MatrixLabs residue was deliberately excluded after operator clarification that it is leftover residue, not active source.
