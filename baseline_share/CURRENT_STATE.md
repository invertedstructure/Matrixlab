# Current State

Generated at UTC: `2026-07-01T21:01:04Z`

## Git context

- Current HEAD SHA: `6461d1511b4091ea76a57b040684f4cc5521a3ba`
- Current branch: `master`
- Worktree state at generation time: `dirty`
- `baseline_share/` is generated output and may appear dirty while this packet is being refreshed.
- Git status:
- `M scripts/build_baseline_share_v0.py`
- `?? discussion_packets/`
- `?? docs/matrixlabs/architecture/c8_observed_decision_path_v1.json`
- `?? docs/matrixlabs/architecture/c8_observed_decision_path_v1.md`
- `?? docs/matrixlabs/observability/c8_observed_path_update_apply_v0.json`
- `?? docs/matrixlabs/observability/c8_observed_path_update_apply_v0.md`
- `?? docs/matrixlabs/observability/decision_path_index_v1.json`
- `?? docs/matrixlabs/observability/decision_path_index_v1.md`
- `?? docs/matrixlabs/observability/receipt_spine_v1.json`
- `?? docs/matrixlabs/observability/receipt_spine_v1.md`
- `?? scripts/build_c8_observed_path_update_apply_v0.py`
- Git status excluding generated `baseline_share/`:
- `M scripts/build_baseline_share_v0.py`
- `?? discussion_packets/`
- `?? docs/matrixlabs/architecture/c8_observed_decision_path_v1.json`
- `?? docs/matrixlabs/architecture/c8_observed_decision_path_v1.md`
- `?? docs/matrixlabs/observability/c8_observed_path_update_apply_v0.json`
- `?? docs/matrixlabs/observability/c8_observed_path_update_apply_v0.md`
- `?? docs/matrixlabs/observability/decision_path_index_v1.json`
- `?? docs/matrixlabs/observability/decision_path_index_v1.md`
- `?? docs/matrixlabs/observability/receipt_spine_v1.json`
- `?? docs/matrixlabs/observability/receipt_spine_v1.md`
- `?? scripts/build_c8_observed_path_update_apply_v0.py`

## Source layer

- Current known source layer: `docs/matrixlabs/`
- `docs/matrixlabs/` present: `true`
- Current architecture extraction commit: `6461d1511b4091ea76a57b040684f4cc5521a3ba`
- Current C8 post-patch surface-decision acceptance commit: `6461d1511b4091ea76a57b040684f4cc5521a3ba`

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
