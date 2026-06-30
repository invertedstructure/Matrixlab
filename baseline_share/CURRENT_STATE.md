# Current State

Generated at UTC: `2026-06-30T21:37:15Z`

## Git context

- Current HEAD SHA: `24619b142b0b6a961532ced6f9458809e4c9ce7a`
- Current branch: `master`
- Worktree state at generation time: `dirty`
- `baseline_share/` is generated output and may appear dirty while this packet is being refreshed.
- Git status:
- `M baseline_share/COMMIT_CONTEXT.md`
- ` M baseline_share/CURRENT_STATE.md`
- ` M baseline_share/MANIFEST.json`
- ` M baseline_share/RECEIPT_POINTERS.md`
- ` M scripts/build_baseline_share_v0.py`
- `?? docs/matrixlabs/architecture/c8_observed_decision_path_v0.json`
- `?? docs/matrixlabs/architecture/c8_observed_decision_path_v0.md`
- Git status excluding generated `baseline_share/`:
- ` M scripts/build_baseline_share_v0.py`
- `?? docs/matrixlabs/architecture/c8_observed_decision_path_v0.json`
- `?? docs/matrixlabs/architecture/c8_observed_decision_path_v0.md`

## Source layer

- Current known source layer: `docs/matrixlabs/`
- `docs/matrixlabs/` present: `true`
- Current architecture extraction commit: `9f2fd5cceee3badd1e5dd55910150fe1242252b3`
- Current C8 post-patch surface-decision acceptance commit: `24619b142b0b6a961532ced6f9458809e4c9ce7a`

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
