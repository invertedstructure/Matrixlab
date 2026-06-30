# Current State

Generated at UTC: `2026-06-30T18:50:24Z`

## Git context

- Current HEAD SHA: `9f2fd5cceee3badd1e5dd55910150fe1242252b3`
- Current branch: `master`
- Worktree state at generation time: `dirty`
- `baseline_share/` is generated output and may appear dirty while this packet is being refreshed.
- Git status:
- `?? baseline_share/`
- `?? scripts/build_baseline_share_v0.py`
- Git status excluding generated `baseline_share/`:
- `?? scripts/build_baseline_share_v0.py`

## Source layer

- Current known source layer: `docs/matrixlabs/`
- `docs/matrixlabs/` present: `true`
- Current architecture extraction commit: `9f2fd5cceee3badd1e5dd55910150fe1242252b3`
- Current C8 post-patch surface-decision acceptance commit: `a370223f05ebdf110cf56f125052eb3128cdc814`

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
