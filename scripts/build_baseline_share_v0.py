#!/usr/bin/env python3
"""Generate MatrixLabs Baseline Share Packet v0.

This script emits a portable, uploadable projection under baseline_share/.
The repository remains the source of truth.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


SCHEMA_VERSION = "matrixlabs_baseline_share_manifest_v0"
GENERATOR_SCRIPT = "scripts/build_baseline_share_v0.py"
BASELINE_DIR = "baseline_share"
INCLUDED_FILES = [
    "README.md",
    "CURRENT_STATE.md",
    "ARCHITECTURE_SUMMARY.md",
    "CODE_MAP.md",
    "DECISION_GRAPH.md",
    "OPEN_QUESTIONS.md",
    "RECEIPT_POINTERS.md",
    "COMMIT_CONTEXT.md",
    "MANIFEST.json",
]
OBSERVABILITY_INDEX_DOCS = [
    "docs/matrixlabs/observability/decision_path_index_v0.json",
    "docs/matrixlabs/observability/decision_path_index_v0.md",
]
OBSERVABILITY_INDEX_GENERATOR = "scripts/build_decision_path_index_v0.py"
RECEIPT_SPINE_DOCS = [
    "docs/matrixlabs/observability/receipt_spine_v0.json",
    "docs/matrixlabs/observability/receipt_spine_v0.md",
]
RECEIPT_SPINE_GENERATOR = "scripts/build_receipt_spine_v0.py"
COMPRESSION_LAW_DOCS = [
    "docs/matrixlabs/observability/compression_decompression_law_v0.json",
    "docs/matrixlabs/observability/compression_decompression_law_v0.md",
]
COMPRESSION_LAW_GENERATOR = "scripts/build_compression_decompression_law_v0.py"
CLOSEOUT_WRAPPER_DOCS = [
    "docs/matrixlabs/observability/closeout_wrapper_v0.json",
    "docs/matrixlabs/observability/closeout_wrapper_v0.md",
    "docs/matrixlabs/observability/closeout_manifests/matrixlabs_observability_m1_m3_closeout_v0.json",
]
CLOSEOUT_WRAPPER_GENERATOR = "scripts/matrixlab_closeout_wrapper_v0.py"
PROCEED_SURFACE_TAXONOMY_DOCS = [
    "docs/matrixlabs/observability/proceed_surface_taxonomy_v0.json",
    "docs/matrixlabs/observability/proceed_surface_taxonomy_v0.md",
]
PROCEED_SURFACE_TAXONOMY_GENERATOR = "scripts/build_proceed_surface_taxonomy_v0.py"
C8_TAXONOMY_CONTINUATION_DOCS = [
    "docs/matrixlabs/c8/continuation/c8_taxonomy_applied_continuation_packet_v0.json",
    "docs/matrixlabs/c8/continuation/c8_taxonomy_applied_continuation_packet_v0.md",
]
C8_TAXONOMY_CONTINUATION_GENERATOR = "scripts/build_c8_taxonomy_applied_continuation_packet_v0.py"
C8_OBSERVED_PATH_UPDATE_PROPOSAL_DOCS = [
    "docs/matrixlabs/observability/observed_path_update_manifests/c8_m6_observed_path_update_manifest_v0.json",
    "docs/matrixlabs/observability/c8_observed_decision_path_update_m6_proposal_v0.json",
    "docs/matrixlabs/observability/c8_observed_decision_path_update_m6_proposal_v0.md",
]
C8_OBSERVED_PATH_UPDATE_PROPOSAL_GENERATOR = "scripts/build_c8_observed_path_update_proposal_m6_v0.py"
C8_OBSERVED_PATH_UPDATE_APPLY_DOCS = [
    "docs/matrixlabs/architecture/c8_observed_decision_path_v1.json",
    "docs/matrixlabs/architecture/c8_observed_decision_path_v1.md",
    "docs/matrixlabs/observability/decision_path_index_v1.json",
    "docs/matrixlabs/observability/decision_path_index_v1.md",
    "docs/matrixlabs/observability/receipt_spine_v1.json",
    "docs/matrixlabs/observability/receipt_spine_v1.md",
    "docs/matrixlabs/observability/c8_observed_path_update_apply_v0.json",
    "docs/matrixlabs/observability/c8_observed_path_update_apply_v0.md",
]
C8_OBSERVED_PATH_UPDATE_APPLY_GENERATOR = "scripts/build_c8_observed_path_update_apply_v0.py"
C8_N22_AUTHORITY_BOUNDARY_DOCS = [
    "docs/matrixlabs/boundary/c8_n22_authority_boundary_transition_record_v0.json",
    "docs/matrixlabs/boundary/c8_n22_authority_boundary_transition_record_v0.md",
]
C8_N22_AUTHORITY_BOUNDARY_GENERATOR = "scripts/build_c8_n22_authority_boundary_transition_record_v0.py"
SOURCE_DOCS = [
    "docs/matrixlabs/INDEX.md",
    "docs/matrixlabs/architecture/current_architecture_readout_v0.md",
    "docs/matrixlabs/architecture/source_map_v0.md",
    "docs/matrixlabs/architecture/decision_graph_readout_v0.md",
    "docs/matrixlabs/proposals/extraction_followup_questions_v0.md",
    "docs/matrixlabs/raw/source_inventory_v0.md",
    *OBSERVABILITY_INDEX_DOCS,
    OBSERVABILITY_INDEX_GENERATOR,
    *RECEIPT_SPINE_DOCS,
    RECEIPT_SPINE_GENERATOR,
    *COMPRESSION_LAW_DOCS,
    COMPRESSION_LAW_GENERATOR,
    *CLOSEOUT_WRAPPER_DOCS,
    CLOSEOUT_WRAPPER_GENERATOR,
    *PROCEED_SURFACE_TAXONOMY_DOCS,
    PROCEED_SURFACE_TAXONOMY_GENERATOR,
    *C8_TAXONOMY_CONTINUATION_DOCS,
    C8_TAXONOMY_CONTINUATION_GENERATOR,
    *C8_OBSERVED_PATH_UPDATE_PROPOSAL_DOCS,
    C8_OBSERVED_PATH_UPDATE_PROPOSAL_GENERATOR,
    *C8_OBSERVED_PATH_UPDATE_APPLY_DOCS,
    C8_OBSERVED_PATH_UPDATE_APPLY_GENERATOR,
    *C8_N22_AUTHORITY_BOUNDARY_DOCS,
    C8_N22_AUTHORITY_BOUNDARY_GENERATOR,
]
C8_POST_PATCH_DIRS = [
    "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_after_runtime_adoption_closure_v0",
    "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_after_runtime_adoption_closure_v0_receipts",
]
C8_POST_PATCH_RECEIPT = (
    "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_after_runtime_adoption_closure_v0_receipts/"
    "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_receipt_22e01dcc.json"
)


class GenerationError(RuntimeError):
    pass


def run_git(root: Path, args: list[str], check: bool = False) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and proc.returncode != 0:
        raise GenerationError(
            f"git {' '.join(args)} failed: {proc.stderr.strip() or proc.stdout.strip()}"
        )
    return proc.stdout.strip()


def git_status_excluding_baseline_share(root: Path, status_lines: list[str]) -> list[str]:
    """Keep raw git status available while identifying non-generated changes."""
    def status_path(line: str) -> str:
        if len(line) >= 4 and line[2] == " ":
            return line[3:]
        parts = line.split(maxsplit=1)
        return parts[1] if len(parts) == 2 else line

    return [line for line in status_lines if not status_path(line).startswith(f"{BASELINE_DIR}/")]


def detect_repo_root(start: Path) -> Path:
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise GenerationError(f"not inside a git repository: {proc.stderr.strip()}")
    return Path(proc.stdout.strip()).resolve()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def extract_section(markdown: str, heading: str) -> str:
    marker = f"## {heading}"
    lines = markdown.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == marker:
            start = index + 1
            break
    if start is None:
        return ""
    out: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        out.append(line)
    return "\n".join(out).strip()


def compact_section(section: str, max_lines: int = 28, max_chars: int = 3200) -> str:
    if not section.strip():
        return "Uncertain: this section was not found in the source-backed docs."
    lines = [line.rstrip() for line in section.strip().splitlines()]
    compacted = "\n".join(lines[:max_lines]).strip()
    if len(compacted) > max_chars:
        compacted = compacted[:max_chars].rstrip() + "\n\n[Truncated in baseline share packet; see source docs.]"
    elif len(lines) > max_lines:
        compacted += "\n\n[Truncated in baseline share packet; see source docs.]"
    return compacted


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def count_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob("*") if item.is_file())


def existing_paths(root: Path, paths: Iterable[str]) -> list[str]:
    return [path for path in paths if (root / path).exists()]


def commit_for_paths(root: Path, paths: list[str]) -> str | None:
    existing = existing_paths(root, paths)
    if not existing:
        return None
    result = run_git(root, ["log", "-n", "1", "--format=%H", "--", *existing])
    return result or None


def scan_receipt_archive_for_architecture_refs(archive: Path, limit: int = 10) -> list[str]:
    if not archive.exists():
        return []
    needles = [
        "docs/matrixlabs",
        "architecture extraction",
        "current_architecture_readout_v0",
        "source_inventory_v0",
        "MatrixLabs architecture",
    ]
    matches: list[str] = []
    for path in sorted(item for item in archive.rglob("*") if item.is_file()):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if any(needle in text for needle in needles):
            matches.append(str(path))
            if len(matches) >= limit:
                break
    return matches


def ensure_safe_baseline_dir(root: Path) -> Path:
    baseline = root / BASELINE_DIR
    if not baseline.exists():
        baseline.mkdir(parents=True)
        return baseline
    manifest = baseline / "MANIFEST.json"
    if not manifest.exists():
        raise GenerationError(
            "baseline_share/ exists but has no recognizable MANIFEST.json; refusing to overwrite"
        )
    try:
        data = json.loads(read_text(manifest))
    except json.JSONDecodeError as exc:
        raise GenerationError(
            "baseline_share/MANIFEST.json is not valid JSON; refusing to overwrite"
        ) from exc
    if (
        data.get("schema_version") != SCHEMA_VERSION
        or data.get("generator_script") != GENERATOR_SCRIPT
    ):
        raise GenerationError(
            "baseline_share/ exists but was not generated by scripts/build_baseline_share_v0.py; refusing to overwrite"
        )
    return baseline


def bullet_status(status_lines: list[str]) -> str:
    if not status_lines:
        return "- clean"
    return "\n".join(f"- `{line}`" for line in status_lines)


def render_readme() -> str:
    return """# MatrixLabs Baseline Share Packet v0

This directory is an uploadable code-native source packet for the next MatrixLabs strategy, milestone, or review chat.

It is generated from repository source and source-backed docs. It does not replace the repo, does not become the source of truth, does not promote schemas, and does not authorize execution. The repository remains the source of truth.

This packet intentionally does not include the full receipt stack. Receipts remain evidence in their original locations and are referenced by pointer. Upload `baseline_share/` first; expand individual receipts only when a claim becomes load-bearing.

The generator for this packet is `scripts/build_baseline_share_v0.py`. It uses only the Python standard library and does not run MatrixLabs runtime, probe, build, or rerun commands."""


def render_current_state(
    root: Path,
    generated_at: str,
    head: str,
    branch: str,
    status_lines: list[str],
    status_lines_excluding_baseline_share: list[str],
    architecture_commit: str | None,
    c8_post_patch_commit: str | None,
) -> str:
    dirty_state = "dirty" if status_lines else "clean"
    docs_exists = (root / "docs/matrixlabs").exists()
    post_patch_exists = all((root / path).exists() for path in C8_POST_PATCH_DIRS)
    return f"""# Current State

Generated at UTC: `{generated_at}`

## Git context

- Current HEAD SHA: `{head}`
- Current branch: `{branch or 'UNKNOWN'}`
- Worktree state at generation time: `{dirty_state}`
- `baseline_share/` is generated output and may appear dirty while this packet is being refreshed.
- Git status:
{bullet_status(status_lines)}
- Git status excluding generated `baseline_share/`:
{bullet_status(status_lines_excluding_baseline_share)}

## Source layer

- Current known source layer: `docs/matrixlabs/`
- `docs/matrixlabs/` present: `{str(docs_exists).lower()}`
- Current architecture extraction commit: `{architecture_commit or 'UNCERTAIN_NOT_DISCOVERED'}`
- Current C8 post-patch surface-decision acceptance commit: `{c8_post_patch_commit or 'UNCERTAIN_NOT_DISCOVERED'}`

## High-level state

- Architecture extraction source layer exists: `{str(docs_exists).lower()}`
- Post-patch surface decision acceptance exists: `{str(post_patch_exists).lower()}`
- `baseline_share/` is an uploadable projection, not source of truth.
- No MatrixLabs runtime/probe/build/rerun command was executed by the generator.
- Receipts were not rewritten.
- The full receipt stack was not copied into `baseline_share/`.

## Uncertainty

- Any missing commit value above means the generator could not discover it from git history for the expected paths.
- This packet summarizes source-backed docs where present; missing source docs are treated as uncertainty, not fact."""


def render_architecture_summary(architecture_doc: str) -> str:
    sections = [
        ("Cell 0 / Lawful Admissibility Boundary", "Cell 0 / lawful admissibility boundary"),
        ("Builder Cell / Cell 1", "Builder Cell / Cell 1"),
        ("Schema Validator / Lawful Admissibility Cell", "Schema Validator / Lawful Admissibility Cell"),
        ("Receipt / Scribe Layer", "Receipt / Scribe layer"),
        ("Human Readout Packet Layer", "Human Readout Packet layer"),
        ("Typed Stops And Halt Vocabulary", "Typed stops and halt vocabulary"),
        ("Missing-object And Missing-instrument Capability Boundaries", "Missing-object and missing-instrument capability boundaries"),
        ("Source Surfaces And Source-status Gaps", "Source surfaces and source-status gaps"),
        ("One-time Acceptance Vs Reusable Schema Authorization", "One-time acceptance vs reusable schema authorization"),
        ("Runtime Adoption Chain", "Runtime adoption chain"),
        ("Unit-feedback Hardening Chain", "Unit-feedback hardening chain"),
        ("Local Source-status Field Patch Chain", "Local source-status field patch chain"),
        ("Post-patch Surface Decision Chain", "Post-patch surface decision chain"),
        ("Decision Graph Compression Candidates", "Recurring decision graph compression candidates"),
    ]
    parts = [
        "# Architecture Summary",
        "",
        "Source: `docs/matrixlabs/architecture/current_architecture_readout_v0.md`.",
        "",
        "This summary preserves source-backed distinctions and does not promote schemas, authorize execution, or turn candidates into implemented architecture.",
    ]
    for title, heading in sections:
        parts.extend(["", f"## {title}", "", compact_section(extract_section(architecture_doc, heading))])
    return "\n".join(parts)


def render_code_map(root: Path) -> str:
    current_c8_paths = [
        "data/c8_unit_feedback_hardening_source_status_gap_response_packet_after_runtime_adoption_closure_v0",
        "data/c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_after_runtime_adoption_closure_v0",
        "data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_after_runtime_adoption_closure_v0",
        "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_once_after_runtime_adoption_closure_v0",
        "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_after_runtime_adoption_closure_v0",
        *C8_POST_PATCH_DIRS,
    ]
    path_lines = []
    for path in current_c8_paths:
        exists = (root / path).exists()
        path_lines.append(f"- `{path}` - {'present' if exists else 'missing/uncertain'}")
    return f"""# Code Map

This is a map, not the full source. The repository remains the source of truth.

## Main source directories

- `data/` - packet, generated artifact, and receipt-backed evidence surface.
- `scripts/` - repeatable unit scripts and generators. The baseline generator is `{GENERATOR_SCRIPT}`.
- `docs/matrixlabs/` - source-backed architecture extraction/readout layer.
- `docs/matrixlabs/observability/` - generated source-preserving lookup surfaces.
- `baseline_share/` - generated uploadable projection, not source of truth.

## Important architecture docs

- `docs/matrixlabs/INDEX.md`
- `docs/matrixlabs/architecture/current_architecture_readout_v0.md`
- `docs/matrixlabs/architecture/source_map_v0.md`
- `docs/matrixlabs/architecture/decision_graph_readout_v0.md`
- `docs/matrixlabs/proposals/extraction_followup_questions_v0.md`
- `docs/matrixlabs/raw/source_inventory_v0.md`
- `docs/matrixlabs/observability/decision_path_index_v0.json`
- `docs/matrixlabs/observability/decision_path_index_v0.md`

## Current C8 source-status / post-patch surface decision paths

{chr(10).join(path_lines)}

## Generator

- `{GENERATOR_SCRIPT}` - standard-library generator for this packet.

## Boundary note

This map is a portable orientation layer. It does not copy the full source, rewrite receipts, promote schemas, or authorize execution."""


def render_decision_graph(decision_doc: str, root: Path) -> str:
    sections = [
        ("Observed Recurring Pattern", "Observed unit pattern"),
        ("Authority Boundary Notes", "Authority boundary by step"),
        ("Compression Candidates", "Compression candidates"),
        ("Authority-sensitive Pieces Not Yet Compressible", "Authority-sensitive parts that must not be compressed yet"),
    ]
    parts = [
        "# Decision Graph",
        "",
        "Source: `docs/matrixlabs/architecture/decision_graph_readout_v0.md`.",
        "",
        "This file summarizes observed decision graph structure. Compression candidates remain proposals only.",
    ]
    for title, heading in sections:
        parts.extend(["", f"## {title}", "", compact_section(extract_section(decision_doc, heading), max_lines=42, max_chars=5000)])
    parts.extend([
        "",
        "## Decision Path Index v0",
        "",
        "M1 observability/addressability surface for `docs/matrixlabs/architecture/c8_observed_decision_path_v0.json`. It is not authority, not receipt validation, and not compression.",
        "",
        *[
            f"- `{path}` - {'present' if (root / path).exists() else 'missing/uncertain'}"
            for path in OBSERVABILITY_INDEX_DOCS
        ],
    ])
    return "\n".join(parts)


def render_open_questions(proposals_doc: str) -> str:
    sections = [
        ("Uncertain Concepts", "Uncertainties discovered"),
        ("Missing Source Surfaces", "Missing source surfaces"),
        ("Questions For Carlos", "Questions for Carlos"),
        ("Candidate Next Extraction Passes", "Candidate next extraction passes"),
        ("Cleanup Or Organization Proposals", "Cleanup or organization proposals"),
    ]
    parts = [
        "# Open Questions",
        "",
        "Source: `docs/matrixlabs/proposals/extraction_followup_questions_v0.md`.",
        "",
        "These items remain questions or proposals. They are not transformed into facts by this baseline share packet.",
    ]
    for title, heading in sections:
        parts.extend(["", f"## {title}", "", compact_section(extract_section(proposals_doc, heading))])
    return "\n".join(parts)


def render_receipt_pointers(root: Path, architecture_receipt_matches: list[str]) -> str:
    external_archive = Path("/home/asd/matrixlab_receipts")
    docs_receipts = root / "docs/matrixlabs/receipts"
    docs_count = count_files(docs_receipts)
    external_count = count_files(external_archive)
    c8_receipt_present = (root / C8_POST_PATCH_RECEIPT).exists()
    arch_matches = (
        "\n".join(f"- `{path}`" for path in architecture_receipt_matches)
        if architecture_receipt_matches
        else "- Uncertain: no terminal receipt filename for the architecture extraction was discovered by text scan."
    )
    return f"""# Receipt Pointers

This packet does not copy the full receipt stack. Receipts remain evidence and should be expanded only when a claim becomes load-bearing.

## Full receipt locations

- External WSL receipt archive: `/home/asd/matrixlab_receipts/` - {'present' if external_archive.exists() else 'missing'}; file count: `{external_count}`.
- Repo architecture extraction receipt copy: `docs/matrixlabs/receipts/` - {'present' if docs_receipts.exists() else 'missing'}; file count: `{docs_count}`.

## Current load-bearing recent receipt pointers

- C8 post-patch surface decision acceptance receipt: `{C8_POST_PATCH_RECEIPT}` - {'present' if c8_receipt_present else 'missing/uncertain'}.

## Architecture extraction terminal receipt pointer

{arch_matches}

## Upload rule

Upload `baseline_share/` first. Expand individual receipts only when a claim becomes load-bearing. Do not upload or duplicate the full receipt archive unless a later bounded task specifically asks for that evidence."""


def render_commit_context(
    generated_at: str,
    head: str,
    branch: str,
    status_lines: list[str],
    status_lines_excluding_baseline_share: list[str],
    recent_commits: str,
) -> str:
    dirty_state = "dirty" if status_lines else "clean"
    return f"""# Commit Context

- Generated at UTC: `{generated_at}`
- Current HEAD SHA: `{head}`
- Branch: `{branch or 'UNKNOWN'}`
- Worktree state at generation time: `{dirty_state}`
- Generator script: `{GENERATOR_SCRIPT}`

## Recent 10 commits

```text
{recent_commits or 'UNCERTAIN_NOT_DISCOVERED'}
```

## Git status short

```text
{chr(10).join(status_lines) if status_lines else 'clean'}
```

## Git status short excluding generated baseline_share

```text
{chr(10).join(status_lines_excluding_baseline_share) if status_lines_excluding_baseline_share else 'clean'}
```

## Safety facts

- The generator did not run MatrixLabs runtime/probe/build/rerun commands.
- The generator did not rewrite receipts.
- The generator did not copy the full receipt stack into `baseline_share/`."""


def build_manifest(
    root: Path,
    baseline: Path,
    generated_at: str,
    head: str,
    branch: str,
    status_lines: list[str],
    status_lines_excluding_baseline_share: list[str],
    source_files: list[str],
    receipt_archive_count: int,
) -> dict:
    included = [f"{BASELINE_DIR}/{name}" for name in INCLUDED_FILES]
    hashes: dict[str, str] = {}
    for rel in included:
        path = root / rel
        if path.name == "MANIFEST.json":
            continue
        elif path.exists():
            hashes[rel] = sha256_file(path)
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": generated_at,
        "repo_root": str(root),
        "head_commit_sha": head,
        "branch": branch,
        "git_status_short": status_lines,
        "git_status_short_excluding_baseline_share": status_lines_excluding_baseline_share,
        "git_status_note": "baseline_share/ is generated output and may appear dirty while this packet is being refreshed",
        "generator_script": GENERATOR_SCRIPT,
        "included_files": included,
        "source_files": source_files,
        "receipt_archive_count": receipt_archive_count,
        "file_hash_algorithm": "sha256",
        "file_hashes": hashes,
        "manifest_self_hash_excluded_due_to_self_reference": True,
        "repo_is_source_of_truth": True,
        "baseline_share_is_projection": True,
        "schema_promoted": False,
        "reusable_preapproved_authorization_created": False,
        "runtime_probe_build_rerun_executed": False,
        "receipts_rewritten": False,
        "full_receipt_stack_copied_into_baseline_share": False,
    }
    return manifest


def generate() -> int:
    root = detect_repo_root(Path.cwd())
    baseline = ensure_safe_baseline_dir(root)

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    head = run_git(root, ["rev-parse", "HEAD"], check=True)
    branch = run_git(root, ["branch", "--show-current"])
    status_lines = run_git(root, ["status", "--short"]).splitlines()
    status_lines_excluding_baseline_share = git_status_excluding_baseline_share(root, status_lines)
    recent_commits = run_git(root, ["log", "-n", "10", "--oneline"])
    architecture_commit = commit_for_paths(root, ["docs/matrixlabs"])
    c8_post_patch_commit = commit_for_paths(root, [*C8_POST_PATCH_DIRS, GENERATOR_SCRIPT])

    architecture_doc = read_text(root / "docs/matrixlabs/architecture/current_architecture_readout_v0.md")
    decision_doc = read_text(root / "docs/matrixlabs/architecture/decision_graph_readout_v0.md")
    proposals_doc = read_text(root / "docs/matrixlabs/proposals/extraction_followup_questions_v0.md")
    architecture_receipt_matches = scan_receipt_archive_for_architecture_refs(Path("/home/asd/matrixlab_receipts"))

    content = {
        "README.md": render_readme(),
        "CURRENT_STATE.md": render_current_state(
            root,
            generated_at,
            head,
            branch,
            status_lines,
            status_lines_excluding_baseline_share,
            architecture_commit,
            c8_post_patch_commit,
        ),
        "ARCHITECTURE_SUMMARY.md": render_architecture_summary(architecture_doc),
        "CODE_MAP.md": render_code_map(root),
        "DECISION_GRAPH.md": render_decision_graph(decision_doc, root),
        "OPEN_QUESTIONS.md": render_open_questions(proposals_doc),
        "RECEIPT_POINTERS.md": render_receipt_pointers(root, architecture_receipt_matches),
        "COMMIT_CONTEXT.md": render_commit_context(
            generated_at,
            head,
            branch,
            status_lines,
            status_lines_excluding_baseline_share,
            recent_commits,
        ),
    }

    for filename in INCLUDED_FILES:
        if filename == "MANIFEST.json":
            continue
        write_text(baseline / filename, content[filename])

    source_files = [path for path in SOURCE_DOCS if (root / path).exists()]
    if (root / GENERATOR_SCRIPT).exists():
        source_files.append(GENERATOR_SCRIPT)
    receipt_archive_count = count_files(root / "docs/matrixlabs/receipts")
    manifest = build_manifest(
        root,
        baseline,
        generated_at,
        head,
        branch,
        status_lines,
        status_lines_excluding_baseline_share,
        source_files,
        receipt_archive_count,
    )
    write_text(baseline / "MANIFEST.json", json.dumps(manifest, indent=2, sort_keys=True))

    print(f"Generated {BASELINE_DIR}/ with {len(INCLUDED_FILES)} files")
    return 0


def main() -> int:
    try:
        return generate()
    except GenerationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
