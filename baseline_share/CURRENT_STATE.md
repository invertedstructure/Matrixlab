# Current State

Generated at UTC: `2026-07-08T00:10:38Z`

## Git context

- Current HEAD SHA: `f49dfab97774414330682151e6e3fffeb7ba6f66`
- Current branch: `master`
- Worktree state at generation time: `dirty`
- `baseline_share/` is generated output and may appear dirty while this packet is being refreshed.
- Git status:
- `M baseline_share/COMMIT_CONTEXT.md`
- ` M baseline_share/CURRENT_STATE.md`
- ` M baseline_share/MANIFEST.json`
- ` M baseline_share/RECEIPT_POINTERS.md`
- ` M scripts/build_baseline_share_v0.py`
- `?? discussion_packets/`
- `?? docs/matrixlabs/validator_archive/promotion/`
- `?? scripts/build_c8_n22_candidate_promotion_decision_surface_v0.py`
- Git status excluding generated `baseline_share/`:
- ` M scripts/build_baseline_share_v0.py`
- `?? discussion_packets/`
- `?? docs/matrixlabs/validator_archive/promotion/`
- `?? scripts/build_c8_n22_candidate_promotion_decision_surface_v0.py`

## Source layer

- Current known source layer: `docs/matrixlabs/`
- `docs/matrixlabs/` present: `true`
- Current architecture extraction commit: `f49dfab97774414330682151e6e3fffeb7ba6f66`
- Current C8 post-patch surface-decision acceptance commit: `f49dfab97774414330682151e6e3fffeb7ba6f66`

## High-level state

- Architecture extraction source layer exists: `true`
- Post-patch surface decision acceptance exists: `true`
- `baseline_share/` is an uploadable projection, not source of truth.
- No MatrixLabs runtime/probe/build/rerun command was executed by the generator.
- Receipts were not rewritten.
- The full receipt stack was not copied into `baseline_share/`.

## Uncertainty

- Any missing commit value above means the generator could not discover it from git history for the expected paths.
- This packet summarizes source-backed docs where present; missing source docs are treated as uncertainty, not fact.
