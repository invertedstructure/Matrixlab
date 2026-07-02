# Current State

Generated at UTC: `2026-07-02T15:22:01Z`

## Git context

- Current HEAD SHA: `c006f0fd1a9833009c5660900534a692402fbe6e`
- Current branch: `master`
- Worktree state at generation time: `dirty`
- `baseline_share/` is generated output and may appear dirty while this packet is being refreshed.
- Git status:
- `M scripts/build_baseline_share_v0.py`
- `?? discussion_packets/`
- `?? docs/matrixlabs/decisions/`
- `?? scripts/build_c8_n22_human_decision_receipt_v0.py`
- Git status excluding generated `baseline_share/`:
- `M scripts/build_baseline_share_v0.py`
- `?? discussion_packets/`
- `?? docs/matrixlabs/decisions/`
- `?? scripts/build_c8_n22_human_decision_receipt_v0.py`

## Source layer

- Current known source layer: `docs/matrixlabs/`
- `docs/matrixlabs/` present: `true`
- Current architecture extraction commit: `c006f0fd1a9833009c5660900534a692402fbe6e`
- Current C8 post-patch surface-decision acceptance commit: `c006f0fd1a9833009c5660900534a692402fbe6e`

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
