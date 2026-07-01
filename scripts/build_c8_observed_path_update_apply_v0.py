#!/usr/bin/env python3
"""Apply the passed M7A proposal as an append-only observed-path readout update.

M7B consumes the committed M7A proposal and M6 packet, appends exactly c8.n22
and c8.e21_22 into new v1 readout files, emits the declared v1 derived
surfaces, writes an apply readout, and stops.
"""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_observed_path_update_apply_v0.py"

V0_PATH = "docs/matrixlabs/architecture/c8_observed_decision_path_v0.json"
V0_MD = "docs/matrixlabs/architecture/c8_observed_decision_path_v0.md"
V1_PATH = "docs/matrixlabs/architecture/c8_observed_decision_path_v1.json"
V1_MD = "docs/matrixlabs/architecture/c8_observed_decision_path_v1.md"

PROPOSAL_PATH = "docs/matrixlabs/observability/c8_observed_decision_path_update_m6_proposal_v0.json"
PROPOSAL_MD = "docs/matrixlabs/observability/c8_observed_decision_path_update_m6_proposal_v0.md"
M6_PACKET = "docs/matrixlabs/c8/continuation/c8_taxonomy_applied_continuation_packet_v0.json"
M6_PACKET_MD = "docs/matrixlabs/c8/continuation/c8_taxonomy_applied_continuation_packet_v0.md"

INDEX_V0 = "docs/matrixlabs/observability/decision_path_index_v0.json"
SPINE_V0 = "docs/matrixlabs/observability/receipt_spine_v0.json"
LAW_V0 = "docs/matrixlabs/observability/compression_decompression_law_v0.json"
TAXONOMY_V0 = "docs/matrixlabs/observability/proceed_surface_taxonomy_v0.json"

INDEX_V1 = "docs/matrixlabs/observability/decision_path_index_v1.json"
INDEX_V1_MD = "docs/matrixlabs/observability/decision_path_index_v1.md"
SPINE_V1 = "docs/matrixlabs/observability/receipt_spine_v1.json"
SPINE_V1_MD = "docs/matrixlabs/observability/receipt_spine_v1.md"
APPLY_JSON = "docs/matrixlabs/observability/c8_observed_path_update_apply_v0.json"
APPLY_MD = "docs/matrixlabs/observability/c8_observed_path_update_apply_v0.md"

EXPECTED_M7A_COMMIT = "6461d1511b4091ea76a57b040684f4cc5521a3ba"
EXPECTED_M6_COMMIT = "d21e162d7c52d57d8aa321434d533b99f7e46c23"
EXPECTED_M5_COMMIT = "099a003bf849cc0d4292c4980982166be291f405"
EXPECTED_M4_COMMIT = "6aa9070f2d7a845640a23370a742ee13723a3b51"

NON_CLAIMS = [
    "M7B does not choose the next C8 unit.",
    "M7B does not consume human acceptance.",
    "M7B does not authorize a future unit.",
    "M7B does not execute runtime/probe/build/rerun.",
    "M7B does not rewrite receipts.",
    "M7B does not promote taxonomy.",
    "M7B does not create runner authority.",
    "M7B does not validate theorem truth.",
    "M7B does not validate receipt truth.",
    "M7B does not validate edge lawfulness.",
    "M7B only applies a passed proposal as an append-only observed-path readout update.",
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


def verify_commit(root: Path, commit_sha: str, label: str) -> None:
    run_git(root, ["cat-file", "-e", f"{commit_sha}^{{commit}}"])
    if not commit_sha:
        raise GenerationError(f"{label} commit SHA is missing")


def commit_for_paths(root: Path, paths: list[str]) -> str:
    existing = [path for path in paths if (root / path).exists()]
    if not existing:
        raise GenerationError(f"no existing source paths among: {paths}")
    return run_git(root, ["log", "-n", "1", "--format=%H", "--", *existing])


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(root: Path, rel: str) -> dict[str, Any]:
    try:
        return json.loads((root / rel).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GenerationError(f"missing required file: {rel}") from exc
    except json.JSONDecodeError as exc:
        raise GenerationError(f"invalid JSON: {rel}") from exc


def write_json(root: Path, rel: str, data: dict[str, Any]) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def canon(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def find_list(obj: dict[str, Any], candidates: list[str]) -> list[Any] | None:
    for key in candidates:
        value = obj.get(key)
        if isinstance(value, list):
            return value
    return None


def node_id_from_number(number: int | None) -> str | None:
    if number is None:
        return None
    return f"c8.n{number:02d}"


def terminal_node(nodes: list[dict[str, Any]]) -> tuple[str | None, int | None]:
    candidates: list[tuple[int, dict[str, Any]]] = []
    for node in nodes:
        number = node.get("node_number", node.get("n"))
        if isinstance(number, int):
            candidates.append((number, node))
    if not candidates:
        return None, None
    number, node = max(candidates, key=lambda item: item[0])
    return node.get("node_id") or node_id_from_number(number), number


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


def verify_clean_v0(root: Path) -> None:
    for rel in [V0_PATH, V0_MD]:
        proc = subprocess.run(["git", "diff", "--quiet", "--", rel], cwd=root, check=False)
        if proc.returncode != 0:
            raise GenerationError(f"forbidden modification detected in {rel}")


def verify_declared_commits(root: Path) -> None:
    expected = {
        "M7A proposal": (EXPECTED_M7A_COMMIT, [PROPOSAL_PATH, PROPOSAL_MD, "scripts/build_c8_observed_path_update_proposal_m6_v0.py"]),
        "M6 packet": (EXPECTED_M6_COMMIT, [M6_PACKET, M6_PACKET_MD, "scripts/build_c8_taxonomy_applied_continuation_packet_v0.py"]),
        "M5 taxonomy": (EXPECTED_M5_COMMIT, [TAXONOMY_V0, "docs/matrixlabs/observability/proceed_surface_taxonomy_v0.md", "scripts/build_proceed_surface_taxonomy_v0.py"]),
        "M4 closeout wrapper": (EXPECTED_M4_COMMIT, ["docs/matrixlabs/observability/closeout_wrapper_v0.json", "docs/matrixlabs/observability/closeout_wrapper_v0.md", "scripts/matrixlab_closeout_wrapper_v0.py"]),
    }
    for label, (expected_commit, paths) in expected.items():
        verify_commit(root, expected_commit, label)
        got = commit_for_paths(root, paths)
        if got != expected_commit:
            raise GenerationError(f"{label} commit mismatch: {got}!={expected_commit}")


def validate_inputs(v0: dict[str, Any], proposal: dict[str, Any], m6: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    nodes = find_list(v0, ["nodes", "path_nodes", "decision_nodes"])
    edges = find_list(v0, ["edges", "path_edges", "decision_edges"])
    if nodes is None or edges is None:
        raise GenerationError("v0 observed path nodes/edges not found")
    if len(nodes) != 21 or len(edges) != 20:
        raise GenerationError(f"v0 counts wrong: nodes={len(nodes)} edges={len(edges)}")
    terminal_id, terminal_number = terminal_node(nodes)
    if terminal_id != "c8.n21" or terminal_number != 21:
        raise GenerationError(f"v0 terminal mismatch: {terminal_id}/{terminal_number}")

    checks = {
        "proposal_schema": (proposal.get("schema_version"), "matrixlabs_c8_observed_path_update_proposal_v0"),
        "proposal_status": (proposal.get("proposal_status"), "UPDATER_PROPOSAL_PASS"),
        "proposal_mode": (proposal.get("proposal_mode"), "PROPOSAL_ONLY"),
        "updater_role": (proposal.get("updater_role"), "bounded_observed_decision_path_readout_updater_v0"),
        "proposal_node": (proposal.get("proposed_node", {}).get("node_id"), "c8.n22"),
        "proposal_edge": (proposal.get("proposed_edge", {}).get("edge_id"), "c8.e21_22"),
        "proposal_backing": (proposal.get("proposed_node", {}).get("receipt_backing_kind"), "SOURCE_COMMIT_ONLY_PACKET_PREPARATION"),
        "proposal_edge_status": (proposal.get("proposed_edge", {}).get("edge_status"), "OBSERVED_READOUT_EDGE_ONLY"),
        "m6_schema": (m6.get("schema_version"), "matrixlabs_c8_taxonomy_applied_continuation_packet_v0"),
        "m6_packet_status": (m6.get("packet_status"), "PACKET_PREPARED"),
        "m6_taxonomy_use_status": (m6.get("taxonomy_use", {}).get("taxonomy_use_status"), "DESCRIPTIVE_ONLY"),
        "m6_taxonomy_use_result": (m6.get("taxonomy_use_verdict", {}).get("result"), "TAXONOMY_USE_PASS_WITH_ASSIGN_MIX"),
        "m6_human_boundary": (m6.get("taxonomy_use", {}).get("human_boundary_status"), "REQUIRED_NOT_YET_CONSUMED"),
        "m6_authorized_status": (m6.get("taxonomy_use", {}).get("authorized_future_unit_status"), "NOT_AUTHORIZED_BY_TAXONOMY_LABEL"),
        "m6_next_c8_unit": (m6.get("acceptance_summary", {}).get("next_c8_unit_chosen_by_packet"), False),
        "m6_updater_created": (m6.get("acceptance_summary", {}).get("decision_path_updater_created"), False),
        "m6_runtime": (m6.get("runtime_probe_build_rerun_executed"), False),
        "m6_receipts": (m6.get("receipts_rewritten"), False),
    }
    failures = [f"{key}:{got}!={want}" for key, (got, want) in checks.items() if got != want]
    if failures:
        raise GenerationError("; ".join(failures))
    return nodes, edges


def build_applied_node(proposal: dict[str, Any], m6: dict[str, Any]) -> dict[str, Any]:
    src = proposal["proposed_node"]
    return {
        "node_id": "c8.n22",
        "node_number": 22,
        "n": 22,
        "phase": "C8 taxonomy-applied continuation packet v0 prepared",
        "node_kind": "taxonomy_applied_continuation_packet",
        "kind": "taxonomy_applied_continuation_packet",
        "receipt_backing_kind": "SOURCE_COMMIT_ONLY_PACKET_PREPARATION",
        "edge_role": "prepared_packet_observed",
        "commit_sha": EXPECTED_M6_COMMIT,
        "artifact_paths": list(src["artifact_paths"]),
        "packet_status": "PACKET_PREPARED",
        "taxonomy_use_status": "DESCRIPTIVE_ONLY",
        "taxonomy_application_status": m6["taxonomy_use"]["taxonomy_application_status"],
        "taxonomy_use_result": "TAXONOMY_USE_PASS_WITH_ASSIGN_MIX",
        "primary_surface_type": "surface.decision_packet.v0",
        "secondary_surface_types": ["surface.human_acceptance.v0"],
        "human_boundary_status": "REQUIRED_NOT_YET_CONSUMED",
        "authorized_future_unit_status": "NOT_AUTHORIZED_BY_TAXONOMY_LABEL",
        "authority_status_changed": m6["taxonomy_use_verdict"]["authority_status_changed"],
        "needs_taxonomy_refinement": m6["taxonomy_use_verdict"]["needs_taxonomy_refinement"],
        "next_c8_unit_chosen_by_packet": False,
        "decision_path_updater_created": False,
        "runtime_probe_build_rerun_executed": False,
        "receipts_rewritten": False,
        "uses_m4_as_semantic_dependency": False,
        "observation_status": "OBSERVED_COMMITTED_PACKET_PREPARATION",
        "authority_created": False,
    }


def build_applied_edge() -> dict[str, Any]:
    return {
        "edge_id": "c8.e21_22",
        "from_node_id": "c8.n21",
        "to_node_id": "c8.n22",
        "from_node_number": 21,
        "to_node_number": 22,
        "edge_kind": "committed_packet_preparation_observed",
        "edge_status": "OBSERVED_READOUT_EDGE_ONLY",
        "basis": [
            "M6 taxonomy-applied continuation packet committed",
            "M7A proposal passed",
            "packet_status remained PACKET_PREPARED",
            "taxonomy_use_status remained DESCRIPTIVE_ONLY",
            "human boundary remained required and not yet consumed",
            "taxonomy label did not authorize a future unit",
            "no runtime/probe/build/rerun was executed",
            "no receipts were rewritten",
        ],
        "must_not_impersonate": [
            "human_acceptance_edge",
            "bounded_execution_edge",
            "runtime_receipt_edge",
            "next_unit_authorization_edge",
            "decision_path_updater_authority",
            "schema_promotion_edge",
        ],
    }


def build_v1_path(v0: dict[str, Any], proposal: dict[str, Any], m6: dict[str, Any]) -> dict[str, Any]:
    v1 = copy.deepcopy(v0)
    nodes = find_list(v1, ["nodes", "path_nodes", "decision_nodes"])
    edges = find_list(v1, ["edges", "path_edges", "decision_edges"])
    if nodes is None or edges is None:
        raise GenerationError("v1 path nodes/edges not found after copy")
    nodes.append(build_applied_node(proposal, m6))
    edges.append(build_applied_edge())
    v1["schema_version"] = "matrixlabs_c8_observed_decision_path_v1"
    v1["readout_status"] = "READOUT_V1_APPEND_ONLY_APPLIED"
    v1["source_version"] = "c8_observed_decision_path_v0"
    v1["applied_update"] = {
        "apply_mode": "APPLY_ONLY_AFTER_PROPOSAL_PASS",
        "proposal_commit_sha": EXPECTED_M7A_COMMIT,
        "appended_node_id": "c8.n22",
        "appended_edge_id": "c8.e21_22",
        "append_only": True,
    }
    return v1


def verify_append_only(v0: dict[str, Any], v1: dict[str, Any]) -> None:
    v0_nodes = find_list(v0, ["nodes", "path_nodes", "decision_nodes"]) or []
    v0_edges = find_list(v0, ["edges", "path_edges", "decision_edges"]) or []
    v1_nodes = find_list(v1, ["nodes", "path_nodes", "decision_nodes"]) or []
    v1_edges = find_list(v1, ["edges", "path_edges", "decision_edges"]) or []
    if len(v1_nodes) != 22 or len(v1_edges) != 21:
        raise GenerationError(f"v1 counts wrong: nodes={len(v1_nodes)} edges={len(v1_edges)}")
    for index, node in enumerate(v0_nodes):
        if canon(node) != canon(v1_nodes[index]):
            raise GenerationError(f"prior node modified at index {index}")
    for index, edge in enumerate(v0_edges):
        if canon(edge) != canon(v1_edges[index]):
            raise GenerationError(f"prior edge modified at index {index}")
    new_node = v1_nodes[-1]
    for bad_key in ["receipt_id", "declared_receipt_id", "runtime_receipt_id"]:
        if new_node.get(bad_key) not in [None, ""]:
            raise GenerationError(f"runtime receipt field invented for c8.n22: {bad_key}")


def build_decision_path_index_v1(v1: dict[str, Any]) -> dict[str, Any]:
    nodes = find_list(v1, ["nodes", "path_nodes", "decision_nodes"]) or []
    edges = find_list(v1, ["edges", "path_edges", "decision_edges"]) or []
    lookup_by_node_kind: dict[str, list[str]] = {}
    lookup_by_human_boundary_status: dict[str, list[str]] = {}
    lookup_by_authorized_future_unit_status: dict[str, list[str]] = {}
    lookup_by_receipt_backing_kind: dict[str, list[str]] = {}
    node_records = []
    for node in nodes:
        number = node.get("node_number", node.get("n"))
        node_id = node.get("node_id") or node_id_from_number(number)
        node_kind = node.get("node_kind") or node.get("kind")
        record = dict(node)
        record["node_id"] = node_id
        record["node_number"] = number
        node_records.append(record)
        if node_kind:
            lookup_by_node_kind.setdefault(node_kind, []).append(node_id)
        for key, lookup in [
            ("human_boundary_status", lookup_by_human_boundary_status),
            ("authorized_future_unit_status", lookup_by_authorized_future_unit_status),
            ("receipt_backing_kind", lookup_by_receipt_backing_kind),
        ]:
            value = node.get(key)
            if value:
                lookup.setdefault(value, []).append(node_id)
    lookup_by_edge_kind: dict[str, list[str]] = {}
    edge_records = []
    for edge in edges:
        record = dict(edge)
        edge_id = record.get("edge_id")
        if not edge_id:
            from_number = record.get("from_node")
            to_number = record.get("to_node")
            if isinstance(from_number, int) and isinstance(to_number, int):
                edge_id = f"c8.e{from_number:02d}_{to_number:02d}"
            else:
                edge_id = f"c8.e{len(edge_records) + 1:02d}"
            record["edge_id"] = edge_id
        if "from_node_id" not in record and isinstance(record.get("from_node"), int):
            record["from_node_id"] = node_id_from_number(record["from_node"])
        if "to_node_id" not in record and isinstance(record.get("to_node"), int):
            record["to_node_id"] = node_id_from_number(record["to_node"])
        edge_records.append(record)
        if record.get("edge_kind"):
            lookup_by_edge_kind.setdefault(record["edge_kind"], []).append(edge_id)
    return {
        "schema_version": "matrixlabs_decision_path_index_v1",
        "index_status": "PASS_APPEND_ONLY_READOUT_UPDATE",
        "source_path": V1_PATH,
        "source_path_schema": v1.get("schema_version"),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "terminal_node_id": "c8.n22",
        "new_node_id": "c8.n22",
        "new_edge_id": "c8.e21_22",
        "nodes": node_records,
        "edges": edge_records,
        "lookup_by_node_kind": lookup_by_node_kind,
        "lookup_by_edge_kind": lookup_by_edge_kind,
        "lookup_by_human_boundary_status": lookup_by_human_boundary_status,
        "lookup_by_authorized_future_unit_status": lookup_by_authorized_future_unit_status,
        "lookup_by_receipt_backing_kind": lookup_by_receipt_backing_kind,
        "non_claims": list(NON_CLAIMS),
        "generated_by": GENERATOR,
    }


def build_receipt_spine_v1(root: Path) -> dict[str, Any]:
    spine_v0 = load_json(root, SPINE_V0)
    nodes = copy.deepcopy(spine_v0.get("nodes", []))
    nodes.append(
        {
            "node_id": "c8.n22",
            "node_number": 22,
            "node_kind": "taxonomy_applied_continuation_packet",
            "phase": "C8 taxonomy-applied continuation packet v0 prepared",
            "receipt_backing_kind": "SOURCE_COMMIT_ONLY_PACKET_PREPARATION",
            "declared_receipt_id": None,
            "declared_receipt_path": None,
            "receipt_exists": None,
            "receipt_parse_ok": None,
            "commit_sha": EXPECTED_M6_COMMIT,
            "artifact_paths": [
                M6_PACKET,
                M6_PACKET_MD,
            ],
            "spine_status": "SPINE_NODE_SOURCE_COMMIT_ONLY_PACKET_PREPARATION",
        }
    )
    edges = copy.deepcopy(spine_v0.get("edges", []))
    edges.append(
        {
            "edge_id": "c8.e21_22",
            "from_node_id": "c8.n21",
            "to_node_id": "c8.n22",
            "from_node_spine_status": "SPINE_NODE_SOURCE_COMMIT_ONLY",
            "to_node_spine_status": "SPINE_NODE_SOURCE_COMMIT_ONLY_PACKET_PREPARATION",
            "edge_evidence_status": "EDGE_READOUT_ONLY_SOURCE_COMMIT_PACKET_PREPARATION",
            "edge_semantic_validation_performed": False,
        }
    )
    return {
        "schema_version": "matrixlabs_receipt_spine_v1",
        "spine_status": "SPINE_PASS_WITH_SOURCE_COMMIT_ONLY_NODES",
        "source_path": V1_PATH,
        "total_node_count": 22,
        "edge_count": 21,
        "runtime_receipt_node_count": 19,
        "source_commit_only_meta_node_count": 2,
        "source_commit_only_packet_preparation_node_count": 1,
        "receipt_missing_count": 0,
        "receipt_parse_fail_count": 0,
        "nodes": nodes,
        "edges": edges,
        "non_claims": list(NON_CLAIMS),
        "generated_by": GENERATOR,
    }


def build_apply_readout() -> dict[str, Any]:
    return {
        "schema_version": "matrixlabs_c8_observed_path_update_apply_v0",
        "apply_status": "APPLY_PASS_APPEND_ONLY_READOUT_UPDATE",
        "apply_mode": "APPLY_ONLY_AFTER_PROPOSAL_PASS",
        "updater_role": "bounded_observed_decision_path_readout_updater_v0",
        "source_proposal": {
            "proposal_schema_version": "matrixlabs_c8_observed_path_update_proposal_v0",
            "proposal_status": "UPDATER_PROPOSAL_PASS",
            "proposal_commit_sha": EXPECTED_M7A_COMMIT,
        },
        "path_update": {
            "previous_path": V0_PATH,
            "new_path": V1_PATH,
            "previous_terminal_node_id": "c8.n21",
            "new_terminal_node_id": "c8.n22",
            "nodes_before": 21,
            "nodes_after": 22,
            "edges_before": 20,
            "edges_after": 21,
            "append_only": True,
            "prior_nodes_modified": False,
            "prior_edges_modified": False,
        },
        "applied_node": {
            "node_id": "c8.n22",
            "receipt_backing_kind": "SOURCE_COMMIT_ONLY_PACKET_PREPARATION",
            "packet_status": "PACKET_PREPARED",
            "taxonomy_use_result": "TAXONOMY_USE_PASS_WITH_ASSIGN_MIX",
            "human_boundary_status": "REQUIRED_NOT_YET_CONSUMED",
            "authorized_future_unit_status": "NOT_AUTHORIZED_BY_TAXONOMY_LABEL",
        },
        "applied_edge": {
            "edge_id": "c8.e21_22",
            "edge_status": "OBSERVED_READOUT_EDGE_ONLY",
            "edge_kind": "committed_packet_preparation_observed",
        },
        "derived_surfaces": {
            "decision_path_index_v1": INDEX_V1,
            "receipt_spine_v1": SPINE_V1,
            "derived_generation_status": "PASS",
        },
        "forbidden_effects": {
            "next_c8_unit_chosen": False,
            "future_unit_authorized": False,
            "runtime_probe_build_rerun_executed": False,
            "receipts_rewritten": False,
            "schema_promoted": False,
            "runner_authority_created": False,
            "decision_path_updater_created_as_authority": False,
            "uses_m4_as_semantic_dependency": False,
        },
        "terminal_result": {
            "type": "STOP_DONE",
            "reason": "M7B applied the passed proposal as an append-only readout update and stopped.",
        },
        "non_claims": list(NON_CLAIMS),
        "generated_by": GENERATOR,
    }


def render_path_md(v1: dict[str, Any]) -> str:
    nodes = find_list(v1, ["nodes", "path_nodes", "decision_nodes"]) or []
    edges = find_list(v1, ["edges", "path_edges", "decision_edges"]) or []
    return "\n".join(
        [
            "# C8 Observed Decision Path v1",
            "",
            "Append-only readout update from M7B.",
            "",
            f"- node count: `{len(nodes)}`",
            f"- edge count: `{len(edges)}`",
            "- terminal node: `c8.n22`",
            "- appended node: `c8.n22`",
            "- appended edge: `c8.e21_22`",
            "- prior nodes and edges are preserved canonically.",
            "",
            "## Boundary",
            "",
            "- No next C8 unit was chosen.",
            "- No runtime/probe/build/rerun was executed.",
            "- No receipts were rewritten.",
            "- `c8.n22` is source-commit-only packet preparation.",
            "",
        ]
    )


def render_index_md(index: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Decision Path Index v1",
            "",
            f"- schema: `{index['schema_version']}`",
            f"- node count: `{index['node_count']}`",
            f"- edge count: `{index['edge_count']}`",
            f"- terminal node: `{index['terminal_node_id']}`",
            "- new node: `c8.n22`",
            "- new edge: `c8.e21_22`",
            "",
        ]
    )


def render_spine_md(spine: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Receipt Spine v1",
            "",
            f"- schema: `{spine['schema_version']}`",
            f"- status: `{spine['spine_status']}`",
            f"- runtime receipt nodes: `{spine['runtime_receipt_node_count']}`",
            f"- source-commit-only meta nodes: `{spine['source_commit_only_meta_node_count']}`",
            f"- source-commit-only packet preparation nodes: `{spine['source_commit_only_packet_preparation_node_count']}`",
            "- `c8.n22` is `SPINE_NODE_SOURCE_COMMIT_ONLY_PACKET_PREPARATION`, not a missing receipt.",
            "",
        ]
    )


def render_apply_md() -> str:
    lines = [
        "# C8 observed path update apply v0",
        "",
        "Status: APPLY_PASS_APPEND_ONLY_READOUT_UPDATE",
        "",
        "Applied:",
        "- appended node: c8.n22",
        "- appended edge: c8.e21_22",
        "- previous path: c8_observed_decision_path_v0",
        "- new path: c8_observed_decision_path_v1",
        "",
        "Boundary:",
        "- human boundary remains REQUIRED_NOT_YET_CONSUMED",
        "- authorized future unit remains NOT_AUTHORIZED_BY_TAXONOMY_LABEL",
        "- edge is OBSERVED_READOUT_EDGE_ONLY",
        "- backing kind is SOURCE_COMMIT_ONLY_PACKET_PREPARATION",
        "",
        "Forbidden effects:",
        "- no next C8 unit chosen",
        "- no runtime executed",
        "- no receipts rewritten",
        "- no schema promoted",
        "- no runner authority created",
        "",
        "Non-claim:",
        "This apply step updates the observed readout only. It does not authorize, execute, decide, or promote.",
        "",
        "## Mandatory non-claims",
        "",
    ]
    lines.extend(f"- {claim}" for claim in NON_CLAIMS)
    lines.append("")
    return "\n".join(lines)


def write_markdown(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def generate() -> dict[str, Any]:
    root = detect_repo_root(Path.cwd())
    verify_clean_v0(root)
    verify_declared_commits(root)
    v0 = load_json(root, V0_PATH)
    proposal = load_json(root, PROPOSAL_PATH)
    m6 = load_json(root, M6_PACKET)
    validate_inputs(v0, proposal, m6)
    v1 = build_v1_path(v0, proposal, m6)
    verify_append_only(v0, v1)
    index_v1 = build_decision_path_index_v1(v1)
    spine_v1 = build_receipt_spine_v1(root)
    apply_readout = build_apply_readout()
    if exact_value_paths(apply_readout, "AUTHORIZED_BY_TAXONOMY_LABEL"):
        raise GenerationError("forbidden exact taxonomy authorization value present")

    write_json(root, V1_PATH, v1)
    write_markdown(root, V1_MD, render_path_md(v1))
    write_json(root, INDEX_V1, index_v1)
    write_markdown(root, INDEX_V1_MD, render_index_md(index_v1))
    write_json(root, SPINE_V1, spine_v1)
    write_markdown(root, SPINE_V1_MD, render_spine_md(spine_v1))
    write_json(root, APPLY_JSON, apply_readout)
    write_markdown(root, APPLY_MD, render_apply_md())
    verify_clean_v0(root)
    return apply_readout


def main() -> int:
    try:
        apply_readout = generate()
    except GenerationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(
        "Generated M7B apply readout "
        f"{apply_readout['apply_status']} for c8.n22 / c8.e21_22"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
