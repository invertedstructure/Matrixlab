#!/usr/bin/env python3
"""Build M7A observed path update proposal for the committed M6 packet.

M7A is proposal-only. It writes a manifest-driven readout proposal and never
modifies the observed path files, applies a node/edge, creates authority,
chooses the next C8 unit, runs runtime/probe/build/rerun, or rewrites receipts.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_observed_path_update_proposal_m6_v0.py"
MANIFEST_PATH = "docs/matrixlabs/observability/observed_path_update_manifests/c8_m6_observed_path_update_manifest_v0.json"
PROPOSAL_JSON = "docs/matrixlabs/observability/c8_observed_decision_path_update_m6_proposal_v0.json"
PROPOSAL_MD = "docs/matrixlabs/observability/c8_observed_decision_path_update_m6_proposal_v0.md"

PREVIOUS_PATH = "docs/matrixlabs/architecture/c8_observed_decision_path_v0.json"
PREVIOUS_PATH_MD = "docs/matrixlabs/architecture/c8_observed_decision_path_v0.md"
INDEX_PATH = "docs/matrixlabs/observability/decision_path_index_v0.json"
SPINE_PATH = "docs/matrixlabs/observability/receipt_spine_v0.json"
LAW_PATH = "docs/matrixlabs/observability/compression_decompression_law_v0.json"
TAXONOMY_PATH = "docs/matrixlabs/observability/proceed_surface_taxonomy_v0.json"
M6_PACKET_JSON = "docs/matrixlabs/c8/continuation/c8_taxonomy_applied_continuation_packet_v0.json"
M6_PACKET_MD = "docs/matrixlabs/c8/continuation/c8_taxonomy_applied_continuation_packet_v0.md"
M6_GENERATOR = "scripts/build_c8_taxonomy_applied_continuation_packet_v0.py"
CLOSEOUT_WRAPPER = "docs/matrixlabs/observability/closeout_wrapper_v0.json"

EXPECTED_COMMITS = {
    "source_index_commit_sha": "e0e22d33ee1fdfc9dad6964013162a58d6a0b169",
    "source_receipt_spine_commit_sha": "e78ae91156521669e57bfca3c112d4b83e681d05",
    "source_compression_law_commit_sha": "58f4743e38a6d49e877a7d8b81f0a82c30ad0915",
    "source_proceed_surface_taxonomy_commit_sha": "099a003bf849cc0d4292c4980982166be291f405",
    "source_m6_packet_commit_sha": "d21e162d7c52d57d8aa321434d533b99f7e46c23",
    "source_closeout_wrapper_commit_sha": "6aa9070f2d7a845640a23370a742ee13723a3b51",
}

NON_CLAIMS = [
    "bounded_observed_decision_path_readout_updater_v0 does not choose the next C8 unit.",
    "It does not authorize future movement.",
    "It does not execute runtime probes.",
    "It does not rewrite receipts.",
    "It does not promote taxonomy labels.",
    "It does not create a move registry.",
    "It does not create runner authority.",
    "It does not validate theorem truth.",
    "It does not validate receipt truth.",
    "It does not validate edge lawfulness.",
    "It does not consume human acceptance.",
    "It does not apply the observed path update in proposal mode.",
    "It only proposes bounded readout updates from explicitly declared committed artifacts.",
]


class GenerationError(RuntimeError):
    pass


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


def run_git(root: Path, args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise GenerationError(
            f"git {' '.join(args)} failed: {proc.stderr.strip() or proc.stdout.strip()}"
        )
    return proc.stdout.strip()


def commit_for_paths(root: Path, paths: list[str]) -> str:
    existing = [path for path in paths if (root / path).exists()]
    if not existing:
        raise GenerationError(f"no existing source paths among: {paths}")
    return run_git(root, ["log", "-n", "1", "--format=%H", "--", *existing])


def verify_expected_commit(root: Path, key: str, commit_sha: str) -> None:
    want = EXPECTED_COMMITS[key]
    if commit_sha != want:
        raise GenerationError(f"{key}:{commit_sha}!={want}")
    run_git(root, ["cat-file", "-e", f"{commit_sha}^{{commit}}"])


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(root: Path, rel: str) -> dict[str, Any]:
    path = root / rel
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GenerationError(f"missing required source file: {rel}") from exc
    except json.JSONDecodeError as exc:
        raise GenerationError(f"invalid JSON in required source file: {rel}") from exc


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_manifest() -> dict[str, Any]:
    return {
        "schema_version": "matrixlabs_observed_path_update_manifest_v0",
        "update_id": "c8.m6_taxonomy_packet.observed_update.v0",
        "update_mode": "PROPOSAL_ONLY",
        "previous_path": {
            "path_json": PREVIOUS_PATH,
            "expected_terminal_node_id": "c8.n21",
            "expected_terminal_node_number": 21,
            "expected_head_before_m6": EXPECTED_COMMITS["source_proceed_surface_taxonomy_commit_sha"],
        },
        "new_committed_surface": {
            "commit_sha": EXPECTED_COMMITS["source_m6_packet_commit_sha"],
            "paths": [
                M6_PACKET_JSON,
                M6_PACKET_MD,
                M6_GENERATOR,
            ],
            "schema_version": "matrixlabs_c8_taxonomy_applied_continuation_packet_v0",
        },
        "expected_observation": {
            "proposed_node_id": "c8.n22",
            "proposed_edge_id": "c8.e21_22",
            "node_kind": "taxonomy_applied_continuation_packet",
            "receipt_backing_kind": "SOURCE_COMMIT_ONLY_PACKET_PREPARATION",
            "surface_types": [
                "surface.decision_packet.v0",
                "surface.human_acceptance.v0",
            ],
            "packet_status": "PACKET_PREPARED",
            "taxonomy_use_status": "DESCRIPTIVE_ONLY",
            "taxonomy_use_result": "TAXONOMY_USE_PASS_WITH_ASSIGN_MIX",
            "human_boundary_status": "REQUIRED_NOT_YET_CONSUMED",
            "authorized_future_unit_status": "NOT_AUTHORIZED_BY_TAXONOMY_LABEL",
        },
        "forbidden_interpretations": [
            "next_c8_unit_chosen",
            "future_unit_authorized_by_taxonomy",
            "decision_path_updater_created_as_authority",
            "runtime_probe_build_rerun_executed",
            "receipts_rewritten",
            "schema_promoted",
            "human_acceptance_consumed",
            "runtime_receipt_backing_implied",
        ],
    }


def ensure_manifest(root: Path) -> dict[str, Any]:
    manifest = build_manifest()
    write_json(root / MANIFEST_PATH, manifest)
    loaded = load_json(root, MANIFEST_PATH)
    if loaded != manifest:
        raise GenerationError("update manifest did not round-trip deterministically")
    return loaded


def node_id_from_number(number: int | None) -> str | None:
    if number is None:
        return None
    return f"c8.n{number:02d}"


def terminal_node(path_data: dict[str, Any]) -> tuple[str | None, int | None]:
    if path_data.get("terminal_node_id"):
        node_id = path_data.get("terminal_node_id")
        number = path_data.get("terminal_node_number")
        return node_id, number
    nodes = path_data.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        return None, None
    candidates = []
    for node in nodes:
        if not isinstance(node, dict):
            continue
        number = node.get("node_number", node.get("n"))
        if isinstance(number, int):
            candidates.append((number, node))
    if not candidates:
        return None, None
    number, node = max(candidates, key=lambda item: item[0])
    node_id = node.get("node_id") or node_id_from_number(number)
    return node_id, number


def expected_source_commits(root: Path) -> dict[str, str]:
    commits = {
        "source_index_commit_sha": commit_for_paths(
            root,
            [
                INDEX_PATH,
                "docs/matrixlabs/observability/decision_path_index_v0.md",
                "scripts/build_decision_path_index_v0.py",
            ],
        ),
        "source_receipt_spine_commit_sha": commit_for_paths(
            root,
            [
                SPINE_PATH,
                "docs/matrixlabs/observability/receipt_spine_v0.md",
                "scripts/build_receipt_spine_v0.py",
            ],
        ),
        "source_compression_law_commit_sha": commit_for_paths(
            root,
            [
                LAW_PATH,
                "docs/matrixlabs/observability/compression_decompression_law_v0.md",
                "scripts/build_compression_decompression_law_v0.py",
            ],
        ),
        "source_proceed_surface_taxonomy_commit_sha": commit_for_paths(
            root,
            [
                TAXONOMY_PATH,
                "docs/matrixlabs/observability/proceed_surface_taxonomy_v0.md",
                "scripts/build_proceed_surface_taxonomy_v0.py",
            ],
        ),
        "source_m6_packet_commit_sha": commit_for_paths(
            root,
            [
                M6_PACKET_JSON,
                M6_PACKET_MD,
                M6_GENERATOR,
            ],
        ),
        "source_closeout_wrapper_commit_sha": commit_for_paths(
            root,
            [
                CLOSEOUT_WRAPPER,
                "docs/matrixlabs/observability/closeout_wrapper_v0.md",
                "scripts/matrixlab_closeout_wrapper_v0.py",
            ],
        ),
    }
    for key, commit in commits.items():
        verify_expected_commit(root, key, commit)
    return commits


def validate_sources(
    manifest: dict[str, Any],
    previous_path: dict[str, Any],
    index: dict[str, Any],
    spine: dict[str, Any],
    law: dict[str, Any],
    taxonomy: dict[str, Any],
    m6: dict[str, Any],
) -> None:
    failures: list[str] = []
    if manifest.get("schema_version") != "matrixlabs_observed_path_update_manifest_v0":
        failures.append("manifest_schema_mismatch")
    if manifest.get("update_mode") != "PROPOSAL_ONLY":
        failures.append("manifest_update_mode_not_proposal_only")
    terminal_id, terminal_number = terminal_node(previous_path)
    expected_previous = manifest["previous_path"]
    if terminal_id != expected_previous["expected_terminal_node_id"]:
        failures.append(f"terminal_node_id:{terminal_id}!={expected_previous['expected_terminal_node_id']}")
    if terminal_number != expected_previous["expected_terminal_node_number"]:
        failures.append(f"terminal_node_number:{terminal_number}!={expected_previous['expected_terminal_node_number']}")
    checks = {
        "index_schema": (index.get("schema_version"), "matrixlabs_decision_path_index_v0"),
        "spine_schema": (spine.get("schema_version"), "matrixlabs_receipt_spine_v0"),
        "law_schema": (law.get("schema_version"), "matrixlabs_compression_decompression_law_v0"),
        "taxonomy_schema": (taxonomy.get("schema_version"), "matrixlabs_proceed_surface_taxonomy_v0"),
        "m6_schema": (m6.get("schema_version"), "matrixlabs_c8_taxonomy_applied_continuation_packet_v0"),
        "m6_packet_status": (m6.get("packet_status"), "PACKET_PREPARED"),
        "m6_taxonomy_use_status": (m6.get("taxonomy_use", {}).get("taxonomy_use_status"), "DESCRIPTIVE_ONLY"),
        "m6_taxonomy_use_result": (m6.get("taxonomy_use_verdict", {}).get("result"), "TAXONOMY_USE_PASS_WITH_ASSIGN_MIX"),
        "m6_human_boundary_status": (m6.get("taxonomy_use", {}).get("human_boundary_status"), "REQUIRED_NOT_YET_CONSUMED"),
        "m6_authorized_future_unit_status": (m6.get("taxonomy_use", {}).get("authorized_future_unit_status"), "NOT_AUTHORIZED_BY_TAXONOMY_LABEL"),
        "m6_next_c8_unit_chosen_by_packet": (m6.get("acceptance_summary", {}).get("next_c8_unit_chosen_by_packet"), False),
        "m6_decision_path_updater_created": (m6.get("acceptance_summary", {}).get("decision_path_updater_created"), False),
        "m6_runtime_probe_build_rerun_executed": (m6.get("runtime_probe_build_rerun_executed"), False),
        "m6_receipts_rewritten": (m6.get("receipts_rewritten"), False),
    }
    for label, (got, want) in checks.items():
        if got != want:
            failures.append(f"{label}:{got}!={want}")
    if failures:
        raise GenerationError("; ".join(failures))


def proposed_node(commit_sha: str, m6: dict[str, Any]) -> dict[str, Any]:
    taxonomy_use = m6["taxonomy_use"]
    verdict = m6["taxonomy_use_verdict"]
    acceptance = m6["acceptance_summary"]
    return {
        "node_id": "c8.n22",
        "node_number": 22,
        "phase": "C8 taxonomy-applied continuation packet v0 prepared",
        "node_kind": "taxonomy_applied_continuation_packet",
        "receipt_backing_kind": "SOURCE_COMMIT_ONLY_PACKET_PREPARATION",
        "commit_sha": commit_sha,
        "artifact_paths": [
            M6_PACKET_JSON,
            M6_PACKET_MD,
        ],
        "packet_status": m6["packet_status"],
        "taxonomy_use_status": taxonomy_use["taxonomy_use_status"],
        "taxonomy_use_result": verdict["result"],
        "primary_surface_type": taxonomy_use["primary_surface_type"],
        "secondary_surface_types": list(taxonomy_use["secondary_surface_types"]),
        "human_boundary_status": taxonomy_use["human_boundary_status"],
        "authorized_future_unit_status": taxonomy_use["authorized_future_unit_status"],
        "next_c8_unit_chosen_by_packet": acceptance["next_c8_unit_chosen_by_packet"],
        "decision_path_updater_created": acceptance["decision_path_updater_created"],
        "runtime_probe_build_rerun_executed": m6["runtime_probe_build_rerun_executed"],
        "receipts_rewritten": m6["receipts_rewritten"],
        "observation_role": "prepared_packet_observed",
        "authority_created": False,
    }


def proposed_edge() -> dict[str, Any]:
    return {
        "edge_id": "c8.e21_22",
        "from_node_id": "c8.n21",
        "to_node_id": "c8.n22",
        "edge_kind": "committed_packet_preparation_observed",
        "edge_status": "OBSERVED_READOUT_EDGE_ONLY",
        "basis": [
            "M6 packet committed at declared SHA",
            "packet_status is PACKET_PREPARED",
            "taxonomy label did not authorize future unit",
            "human boundary remains required and not consumed",
        ],
        "must_not_impersonate": [
            "human acceptance edge",
            "bounded execution edge",
            "runtime receipt edge",
            "next-unit authorization edge",
            "decision updater authority",
        ],
    }


def build_proposal(root: Path) -> dict[str, Any]:
    manifest = ensure_manifest(root)
    previous_hash_before = sha256_file(root / PREVIOUS_PATH)
    previous_md_hash_before = sha256_file(root / PREVIOUS_PATH_MD)

    previous_path = load_json(root, PREVIOUS_PATH)
    index = load_json(root, INDEX_PATH)
    spine = load_json(root, SPINE_PATH)
    law = load_json(root, LAW_PATH)
    taxonomy = load_json(root, TAXONOMY_PATH)
    m6 = load_json(root, M6_PACKET_JSON)
    validate_sources(manifest, previous_path, index, spine, law, taxonomy, m6)

    commits = expected_source_commits(root)
    m6_commit = commits["source_m6_packet_commit_sha"]
    declared_surface = manifest["new_committed_surface"]
    if declared_surface["commit_sha"] != m6_commit:
        raise GenerationError("manifest M6 commit does not match verified M6 commit")
    for path in declared_surface["paths"]:
        if not (root / path).exists():
            raise GenerationError(f"declared M6 artifact path missing: {path}")

    node = proposed_node(m6_commit, m6)
    edge = proposed_edge()
    if node["receipt_backing_kind"] != "SOURCE_COMMIT_ONLY_PACKET_PREPARATION":
        raise GenerationError("proposed node backing kind is not explicit non-runtime packet preparation")
    if edge["edge_status"] != "OBSERVED_READOUT_EDGE_ONLY":
        raise GenerationError("proposed edge is not readout-only")
    forbidden_edge_kind_terms = ["acceptance", "execution", "authorization", "successor", "runtime transition"]
    if any(term in edge["edge_kind"] for term in forbidden_edge_kind_terms):
        raise GenerationError("proposed edge kind impersonates a stronger transition")

    proposal = {
        "schema_version": "matrixlabs_c8_observed_path_update_proposal_v0",
        "proposal_id": "c8.observed_path.update.m6_taxonomy_packet.proposal.v0",
        "proposal_mode": "PROPOSAL_ONLY",
        "updater_role": "bounded_observed_decision_path_readout_updater_v0",
        "proposal_status": "UPDATER_PROPOSAL_PASS",
        "source_manifest_path": MANIFEST_PATH,
        "previous_path_json": PREVIOUS_PATH,
        "source_paths": {
            "decision_path_index": INDEX_PATH,
            "receipt_spine": SPINE_PATH,
            "compression_law": LAW_PATH,
            "proceed_surface_taxonomy": TAXONOMY_PATH,
            "m6_packet_json": M6_PACKET_JSON,
            "m6_packet_md": M6_PACKET_MD,
            "m6_packet_generator": M6_GENERATOR,
        },
        "source_hashes": {
            "previous_path_sha256": previous_hash_before,
            "decision_path_index_sha256": sha256_file(root / INDEX_PATH),
            "receipt_spine_sha256": sha256_file(root / SPINE_PATH),
            "compression_law_sha256": sha256_file(root / LAW_PATH),
            "proceed_surface_taxonomy_sha256": sha256_file(root / TAXONOMY_PATH),
            "m6_packet_json_sha256": sha256_file(root / M6_PACKET_JSON),
        },
        "source_commits": {
            "source_index_commit_sha": commits["source_index_commit_sha"],
            "source_receipt_spine_commit_sha": commits["source_receipt_spine_commit_sha"],
            "source_compression_law_commit_sha": commits["source_compression_law_commit_sha"],
            "source_proceed_surface_taxonomy_commit_sha": commits["source_proceed_surface_taxonomy_commit_sha"],
            "source_m6_packet_commit_sha": m6_commit,
        },
        "preservation_context": {
            "uses_m4_as_semantic_dependency": False,
            "source_closeout_wrapper_commit_sha": commits["source_closeout_wrapper_commit_sha"],
        },
        "new_committed_surface": {
            "commit_sha": m6_commit,
            "packet_json": M6_PACKET_JSON,
            "packet_md": M6_PACKET_MD,
            "packet_generator": M6_GENERATOR,
            "schema_version": m6["schema_version"],
        },
        "proposed_node": node,
        "proposed_edge": edge,
        "acceptance_summary": {
            "explicit_update_manifest_present": True,
            "previous_path_exists": True,
            "previous_terminal_node_matches": True,
            "new_commit_declared": True,
            "new_commit_verified_in_git": True,
            "new_artifact_paths_declared": True,
            "new_artifact_paths_exist": True,
            "packet_schema_matches": True,
            "packet_status_is_prepared": True,
            "taxonomy_use_status_descriptive_only": True,
            "taxonomy_use_result_allowed": True,
            "human_boundary_required_not_consumed": True,
            "authorized_future_unit_not_authorized_by_taxonomy": True,
            "next_c8_unit_chosen_by_packet_false": True,
            "decision_path_updater_created_false_in_observed_packet": True,
            "runtime_probe_build_rerun_executed_false": True,
            "receipts_rewritten_false": True,
            "non_runtime_backing_kind_explicit": True,
            "proposed_edge_readout_only": True,
            "forbidden_interpretations_absent": True,
            "path_files_modified": False,
        },
        "non_claims": list(NON_CLAIMS),
        "generated_by": GENERATOR,
    }

    if previous_hash_before != sha256_file(root / PREVIOUS_PATH):
        raise GenerationError("previous observed path JSON changed during proposal generation")
    if previous_md_hash_before != sha256_file(root / PREVIOUS_PATH_MD):
        raise GenerationError("previous observed path Markdown changed during proposal generation")
    if exact_value_paths(proposal, "AUTHORIZED_BY_TAXONOMY_LABEL"):
        raise GenerationError("forbidden exact taxonomy authorization value present")
    return proposal


def exact_value_paths(obj: Any, forbidden: Any, path: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            hits.extend(exact_value_paths(value, forbidden, f"{path}.{key}"))
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            hits.extend(exact_value_paths(value, forbidden, f"{path}[{index}]"))
    elif obj == forbidden:
        hits.append(path)
    return hits


def render_markdown(root: Path, manifest: dict[str, Any], proposal: dict[str, Any]) -> str:
    node = proposal["proposed_node"]
    edge = proposal["proposed_edge"]
    summary = proposal["acceptance_summary"]
    lines = [
        "# C8 Observed Decision Path Update Proposal - M6 v0",
        "",
        "## Status",
        "",
        proposal["proposal_status"],
        "",
        "## Purpose",
        "",
        "Proposal-only readout update for the observed C8 decision path.",
        "",
        "## Source manifest",
        "",
        f"- Manifest path: `{MANIFEST_PATH}`",
        f"- Update ID: `{manifest['update_id']}`",
        "",
        "## Previous path",
        "",
        f"- Path file: `{proposal['previous_path_json']}`",
        f"- Expected terminal node: `{manifest['previous_path']['expected_terminal_node_id']}`",
        f"- Expected terminal node number: `{manifest['previous_path']['expected_terminal_node_number']}`",
        "",
        "## New committed surface",
        "",
        f"- M6 commit SHA: `{proposal['new_committed_surface']['commit_sha']}`",
        f"- Packet JSON: `{proposal['new_committed_surface']['packet_json']}`",
        f"- Packet Markdown: `{proposal['new_committed_surface']['packet_md']}`",
        f"- Generator: `{proposal['new_committed_surface']['packet_generator']}`",
        "",
        "## Proposed node",
        "",
    ]
    for key in [
        "node_id",
        "node_number",
        "phase",
        "node_kind",
        "receipt_backing_kind",
        "commit_sha",
        "packet_status",
        "taxonomy_use_status",
        "taxonomy_use_result",
        "primary_surface_type",
        "secondary_surface_types",
        "human_boundary_status",
        "authorized_future_unit_status",
        "next_c8_unit_chosen_by_packet",
        "decision_path_updater_created",
        "runtime_probe_build_rerun_executed",
        "receipts_rewritten",
        "observation_role",
        "authority_created",
    ]:
        lines.append(f"- `{key}`: `{node[key]}`")
    lines.extend(["", "## Proposed edge", ""])
    for key in ["edge_id", "from_node_id", "to_node_id", "edge_kind", "edge_status"]:
        lines.append(f"- `{key}`: `{edge[key]}`")
    lines.append("- `basis`: " + ", ".join(edge["basis"]))
    lines.append("- `must_not_impersonate`: " + ", ".join(edge["must_not_impersonate"]))
    lines.extend(["", "## Acceptance summary", ""])
    for key in sorted(summary):
        lines.append(f"- `{key}`: `{summary[key]}`")
    lines.extend(["", "## Forbidden interpretations", ""])
    for item in manifest["forbidden_interpretations"]:
        lines.append(f"- `{item}`")
    lines.extend(["", "## Non-claims", ""])
    for claim in proposal["non_claims"]:
        lines.append(f"- {claim}")
    lines.extend(
        [
            "",
            "## Relationship to M7B",
            "",
            "This proposal does not apply the path update. Apply mode is separate and future.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(root: Path, proposal: dict[str, Any]) -> None:
    manifest = load_json(root, MANIFEST_PATH)
    write_json(root / PROPOSAL_JSON, proposal)
    md_path = root / PROPOSAL_MD
    md_path.write_text(render_markdown(root, manifest, proposal), encoding="utf-8")


def main() -> int:
    try:
        root = detect_repo_root(Path.cwd())
        proposal = build_proposal(root)
        write_outputs(root, proposal)
    except GenerationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(
        "Generated M7A observed path update proposal "
        f"{proposal['proposed_node']['node_id']} / {proposal['proposed_edge']['edge_id']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
