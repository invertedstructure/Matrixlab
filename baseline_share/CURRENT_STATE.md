# Current State

Generated at UTC: `2026-07-01T13:06:52Z`

## Git context

- Current HEAD SHA: `11f8c9d20e30e1c4f614d7405ff2610baa382f6a`
- Current branch: `master`
- Worktree state at generation time: `dirty`
- `baseline_share/` is generated output and may appear dirty while this packet is being refreshed.
- Git status:
- `M baseline_share/CODE_MAP.md`
- ` M baseline_share/COMMIT_CONTEXT.md`
- ` M baseline_share/CURRENT_STATE.md`
- ` M baseline_share/DECISION_GRAPH.md`
- ` M baseline_share/MANIFEST.json`
- ` M baseline_share/RECEIPT_POINTERS.md`
- ` M scripts/build_baseline_share_v0.py`
- `?? discussion_packets/`
- `?? docs/matrixlabs/observability/`
- `?? scripts/build_decision_path_index_v0.py`
- Git status excluding generated `baseline_share/`:
- ` M scripts/build_baseline_share_v0.py`
- `?? discussion_packets/`
- `?? docs/matrixlabs/observability/`
- `?? scripts/build_decision_path_index_v0.py`

## Source layer

- Current known source layer: `docs/matrixlabs/`
- `docs/matrixlabs/` present: `true`
- Current architecture extraction commit: `11f8c9d20e30e1c4f614d7405ff2610baa382f6a`
- Current C8 post-patch surface-decision acceptance commit: `11f8c9d20e30e1c4f614d7405ff2610baa382f6a`

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
