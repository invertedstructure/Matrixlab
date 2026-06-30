# Raw Evidence README v0

Raw evidence means copied or directly discoverable material that should not be rewritten into architecture by assumption: repository files, generated packets, scripts, tracked receipts, external receipt archives, and explicitly pasted residue. Interpreted readouts belong in `docs/matrixlabs/architecture/`, not in raw evidence files.

## Source surfaces inspected

- Active repo root: `/home/asd/projects/matrixlab` in WSL distro `MatrixLabRescue`.
- Top-level source surfaces: `data/`, `scripts/`, `src/`, `tests/`, `configs/`, `README.md`, `pyproject.toml`, and root receipt/debug text files.
- Git state was checked with `git status --short`; the repo already had modified/staged work unrelated to this extraction.
- `docs/` and `logs/` did not exist before this extraction pass.

## Raw evidence copied

- `/home/asd/matrixlab_receipts/` existed and was copied into `docs/matrixlabs/receipts/` with `cp -a`.
- The copy contains 714 receipt text files from the external WSL receipt archive.
- The copied receipt files are evidence. They were not edited, normalized, renamed, or interpreted in place.

## Residue unavailable or deliberately excluded

- Terminal/chat history beyond the attached pasted request was not directly accessible as an active repo source surface.
- `C:\Users\asd\docs\matrixlabs` and other C-drive MatrixLabs material were treated as leftover residue after operator clarification that the active code was moved to `D:`/WSL-backed storage.
- No C-drive residue was copied into this reference layer in this pass.
- Phase7 was not found as an explicit filename/term surface during the visible search and remains uncertain.

## Future residue intake rule

Future terminal/chat residue should be added as new files under `docs/matrixlabs/raw/` using unique names such as `terminal_residue_YYYYMMDD_vN.txt` or `chat_residue_YYYYMMDD_vN.md`. Do not overwrite existing raw files. Do not edit copied receipts. If a later readout interprets new residue, create or update an interpreted readout separately and cite the raw residue path.
