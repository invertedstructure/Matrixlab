# Current State

Generated at UTC: `2026-07-01T13:58:24Z`

## Git context

- Current HEAD SHA: `e0e22d33ee1fdfc9dad6964013162a58d6a0b169`
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
- `?? docs/matrixlabs/observability/receipt_spine_v0.json`
- `?? docs/matrixlabs/observability/receipt_spine_v0.md`
- `?? scripts/build_receipt_spine_v0.py`
- Git status excluding generated `baseline_share/`:
- ` M scripts/build_baseline_share_v0.py`
- `?? discussion_packets/`
- `?? docs/matrixlabs/observability/receipt_spine_v0.json`
- `?? docs/matrixlabs/observability/receipt_spine_v0.md`
- `?? scripts/build_receipt_spine_v0.py`

## Source layer

- Current known source layer: `docs/matrixlabs/`
- `docs/matrixlabs/` present: `true`
- Current architecture extraction commit: `e0e22d33ee1fdfc9dad6964013162a58d6a0b169`
- Current C8 post-patch surface-decision acceptance commit: `e0e22d33ee1fdfc9dad6964013162a58d6a0b169`

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
