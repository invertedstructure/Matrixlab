# MatrixLabs Extraction Reference Layer v0

This directory is a reviewable reference/readout layer for the current MatrixLabs repository state. It exists so architecture, receipts, packet chains, and source-status decisions can be inspected from files in git rather than from chat memory, terminal memory, or implicit local context.

Warning: this layer is not a redesign, not a schema promotion, not a reusable/preapproved authorization, and not a new runtime surface. It records a bounded extraction of existing evidence and separates copied evidence from interpreted readouts.

## What was copied

- `/home/asd/matrixlab_receipts/` was present in the MatrixLabRescue WSL distro and was copied verbatim into `docs/matrixlabs/receipts/` with filenames and contents preserved.
- No receipt content was rewritten or summarized in place. Receipts remain evidence.

## What was interpreted

- `architecture/current_architecture_readout_v0.md` gives a source-backed readout of the visible architecture.
- `architecture/source_map_v0.md` maps major claims to paths and confidence levels.
- `architecture/decision_graph_readout_v0.md` extracts the recurring decision packet / acceptance / execution / review / closure pattern as an observed pattern, not an implemented compression.
- `raw/source_inventory_v0.md` inventories inspected source surfaces and classifies them as raw evidence, generated artifact, script, interpreted readout, or uncertain.

## What was left uncertain

- Terminal/chat residue beyond the pasted request was not directly available from the active repo. C-drive MatrixLabs material was explicitly treated as leftover residue per operator correction, not as active source evidence.
- Phase7 was searched by filename/term and was not found as an explicit visible source surface in this pass.
- Architecture concepts that appear only as conversation language or inferred naming remain uncertain until source-backed.
- No schema, archive entry, runner pattern, or graph compression candidate is promoted by this extraction.

## Files

- `INDEX.md` - this overview.
- `raw/README.md` - raw evidence policy and intake rules.
- `raw/source_inventory_v0.md` - source, receipt, script, data-packet, and missing-surface inventory.
- `raw/external_residue_intake_placeholder_v0.md` - placeholder for future terminal/chat residue intake.
- `receipts/` - copied receipt archive evidence from `/home/asd/matrixlab_receipts/`.
- `architecture/source_map_v0.md` - claim-to-evidence map.
- `architecture/current_architecture_readout_v0.md` - current-state architecture readout.
- `architecture/decision_graph_readout_v0.md` - recurring decision graph pattern readout.
- `proposals/extraction_followup_questions_v0.md` - uncertainties, questions, and candidate follow-up passes.
