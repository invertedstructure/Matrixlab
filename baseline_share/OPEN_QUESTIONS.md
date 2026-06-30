# Open Questions

Source: `docs/matrixlabs/proposals/extraction_followup_questions_v0.md`.

These items remain questions or proposals. They are not transformed into facts by this baseline share packet.

## Uncertain Concepts

- Phase7 was requested as a search target but was not found as an explicit visible filename/term surface in this pass.
- `scribe` was not confirmed as a formal source-backed component, although receipt discipline is strongly source-backed.
- C-drive MatrixLabs material exists but was identified by the operator as leftover residue. It remains excluded unless Carlos explicitly asks to ingest it as raw residue.
- The exact boundary between Runtime Schema Validator Cell and Lawful Admissibility Cell should stay source-bound until a focused pass maps the files together.
- Some source concepts are visible mainly through generated packet names and receipts; a deeper code-path map could distinguish implementation from generated evidence.

## Missing Source Surfaces

- No pre-existing `docs/` or `logs/` directory was found in the active repo before this extraction.
- No active repo terminal/chat residue archive was found beyond `/home/asd/matrixlab_receipts/` and the pasted request.
- No explicit Phase7 chain was found.

## Questions For Carlos

- Should `missing-object capability boundary` be standardized as the exact term for this discipline, or kept as a readout phrase until a source-backed glossary exists?
- Should C-drive residue be copied into `docs/matrixlabs/raw/` as historical residue, or remain excluded as stale material?
- Is there a Phase7 source surface under a different name that should be included in the next pass?
- Should `scribe` be treated as formal architecture only after a source-backed file is added, or should it remain informal language?
- Which current C8 source-status patch artifacts are intended to be considered accepted source state versus pending review?
- Should future extraction include a line-level map from scripts to emitted data directories?

## Candidate Next Extraction Passes

- Script-to-data lineage map for `scripts/create_*`, `scripts/accept_*`, `scripts/execute_*`, `scripts/close_*`, and `scripts/decide_*` families.
- Runtime schema validator versus lawful admissibility focused map.
- C8 chain map from successor surface selection through runtime adoption closure, unit feedback hardening, local source-status patch, closure readiness, and post-patch decision.
- Cell1/value-source metadata one-time application chain map.
- Receipt archive digest/inventory with filenames, timestamps, sizes, and optional hashes, without rewriting receipt contents.

## Cleanup Or Organization Proposals

- Add a generated-but-reviewable inventory file for all `data/*_receipts/` directories and external receipt archive files.
- Consider a future `docs/matrixlabs/raw/terminal_residue_*` convention if Carlos wants terminal/chat residue in repo.
- Consider a source-backed glossary only after each term has at least one cited source path and confidence level.
- Consider a decision-graph compression design document only after the authority-sensitive boundaries are explicitly reviewed.
