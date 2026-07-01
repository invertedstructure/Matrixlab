#!/usr/bin/env python3
"""Build MatrixLabs decision_path_index_v0.

This generator creates a source-preserving lookup surface over the committed
C8 observed decision path. It performs shape validation only.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "matrixlabs_decision_path_index_v0"
INDEX_STATUS_PASS = "PASS_SHAPE"
INDEX_STATUS_FAIL = "FAIL_SHAPE"
PATH_ID = "c8"
PATH_NAME = "C8 observed decision path"
SOURCE_JSON = Path("docs/matrixlabs/architecture/c8_observed_decision_path_v0.json")
SOURCE_MD = Path("docs/matrixlabs/architecture/c8_observed_decision_path_v0.md")
OUTPUT_JSON = Path("docs/matrixlabs/observability/decision_path_index_v0.json")
OUTPUT_MD = Path("docs/matrixlabs/observability/decision_path_index_v0.md")
GENERATED_BY = "scripts/build_decision_path_index_v0.py"
SOURCE_SCHEMA_VERSION = "matrixlabs_c8_observed_decision_path_v0"
SOURCE_READOUT_STATUS = "observed_source_backed_not_runner"

NODE_FIELDS = [
    "phase",
    "node_kind",
    "status",
    "outcome_class",
    "terminal_stop_code",
    "receipt_id",
    "receipt_path",
    "artifact_dir",
    "commit_sha",
    "human_boundary_required",
    "human_decision_consumed",
    "authorized_future_unit",
]
EDGE_FIELDS = [
    "edge_kind",
    "source_evidence_path",
    "why_lawful",
    "not_authorized",
]
NON_CLAIMS = [
    "decision_path_index_v0 does not validate receipt contents.",
    "decision_path_index_v0 does not hash or verify receipt files.",
    "decision_path_index_v0 does not prove edge lawfulness.",
    "decision_path_index_v0 does not authorize future moves.",
    "decision_path_index_v0 does not promote repeated node kinds or edge kinds into reusable schema.",
    "decision_path_index_v0 does not classify proceed-surface taxonomy.",
    "decision_path_index_v0 does not decide compression or decompression law.",
    "decision_path_index_v0 only makes the observed C8 path addressable.",
]
LATER_MILESTONES = [
    "M1 gives stable addresses.",
    "M2 uses those addresses to build the receipt spine.",
    "M3 defines what may be compressed and decompressed from those addresses.",
    "M5 uses M1 and M3 to name proceed-surface roles without authority leak.",
    "M7 may later update the index mechanically from committed source artifacts, but only after indexing and compression laws are tested.",
]
ADDRESS_STATEMENTS = [
    "Node IDs are stable within c8_observed_decision_path_v0: c8.n01 ... c8.n21.",
    "Edge IDs are stable within c8_observed_decision_path_v0: c8.e01_02 ... c8.e20_21.",
    "These IDs are not claimed as global permanent IDs across future rewritten or separately observed paths.",
]


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


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_source(root: Path) -> dict[str, Any]:
    path = root / SOURCE_JSON
    if not path.exists():
        raise GenerationError(f"source JSON missing: {SOURCE_JSON}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise GenerationError(f"source JSON is not valid JSON: {SOURCE_JSON}") from exc


def verified_source_commit(root: Path) -> str | None:
    commit = run_git(root, ["log", "-n", "1", "--format=%H", "--", str(SOURCE_JSON), str(SOURCE_MD)])
    if not commit:
        return None
    proc = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        return None
    return commit


def node_number(source_node: dict[str, Any], fallback: int) -> int | None:
    # Source v0 was corrected to expose node_number; keep n as a conservative
    # fallback only so this index remains source-preserving for the same readout.
    value = source_node.get("node_number", source_node.get("n", fallback))
    return value if isinstance(value, int) else None


def node_kind(source_node: dict[str, Any]) -> str | None:
    # Source v0 was corrected to expose node_kind; keep kind as a conservative
    # fallback only so this index preserves the original observed readout shape.
    value = source_node.get("node_kind", source_node.get("kind"))
    return value if isinstance(value, str) else None


def node_id(number: int) -> str:
    return f"{PATH_ID}.n{number:02d}"


def edge_id(from_number: int, to_number: int) -> str:
    return f"{PATH_ID}.e{from_number:02d}_{to_number:02d}"


def copied_list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, list) else []


def build_nodes(source_nodes: list[dict[str, Any]], warnings: list[str]) -> list[dict[str, Any]]:
    indexed: list[dict[str, Any]] = []
    for index, source_node in enumerate(source_nodes, start=1):
        number = node_number(source_node, index)
        kind = node_kind(source_node)
        if number is None:
            warnings.append(f"node_{index}_missing_integer_node_number")
            number = index
        if kind is None:
            warnings.append(f"node_{number}_missing_node_kind")

        node = {
            "node_id": node_id(number),
            "node_number": number,
            "source_node_number": number,
            "phase": source_node.get("phase"),
            "node_kind": kind,
            "status": source_node.get("status"),
            "outcome_class": source_node.get("outcome_class"),
            "terminal_stop_code": source_node.get("terminal_stop_code"),
            "receipt_id": source_node.get("receipt_id"),
            "receipt_path": source_node.get("receipt_path"),
            "artifact_dir": source_node.get("artifact_dir"),
            "commit_sha": source_node.get("commit_sha"),
            "human_boundary_required": source_node.get("human_boundary_required"),
            "human_decision_consumed": source_node.get("human_decision_consumed"),
            "authorized_future_unit": source_node.get("authorized_future_unit"),
            "forbidden_actions_explicitly_preserved": copied_list(source_node.get("forbidden_actions_explicitly_preserved")),
            "index_role": "observed_node_pointer",
        }
        for field in NODE_FIELDS:
            if field not in source_node and field not in ("node_kind",):
                warnings.append(f"node_{number}_missing_source_field:{field}")
        if "node_kind" not in source_node and "kind" not in source_node:
            warnings.append(f"node_{number}_missing_source_field:node_kind")
        indexed.append(node)
    return indexed


def build_edges(source_edges: list[dict[str, Any]], warnings: list[str]) -> list[dict[str, Any]]:
    indexed: list[dict[str, Any]] = []
    for index, source_edge in enumerate(source_edges, start=1):
        from_number = source_edge.get("from_node")
        to_number = source_edge.get("to_node")
        if not isinstance(from_number, int):
            warnings.append(f"edge_{index}_missing_integer_from_node")
            from_number = index
        if not isinstance(to_number, int):
            warnings.append(f"edge_{index}_missing_integer_to_node")
            to_number = index + 1

        edge = {
            "edge_id": edge_id(from_number, to_number),
            "from_node_id": node_id(from_number),
            "to_node_id": node_id(to_number),
            "from_node_number": from_number,
            "to_node_number": to_number,
            "edge_kind": source_edge.get("edge_kind"),
            "source_evidence_path": source_edge.get("source_evidence_path"),
            "why_lawful": source_edge.get("why_lawful"),
            "not_authorized": source_edge.get("not_authorized"),
            "index_role": "observed_edge_pointer",
        }
        for field in EDGE_FIELDS:
            if field not in source_edge:
                warnings.append(f"edge_{from_number}_{to_number}_missing_source_field:{field}")
        indexed.append(edge)
    return indexed


def append_lookup(mapping: dict[str, list[str]], key: Any, value: str) -> None:
    if key is None:
        return
    mapping[str(key)].append(value)


def build_lookups(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> dict[str, Any]:
    by_node_kind: dict[str, list[str]] = defaultdict(list)
    by_edge_kind: dict[str, list[str]] = defaultdict(list)
    by_receipt_id: dict[str, list[str]] = defaultdict(list)
    by_commit_sha: dict[str, list[str]] = defaultdict(list)
    by_phase: dict[str, list[str]] = defaultdict(list)
    by_terminal_stop_code: dict[str, list[str]] = defaultdict(list)
    by_outcome_class: dict[str, list[str]] = defaultdict(list)
    by_status: dict[str, list[str]] = defaultdict(list)
    by_human_boundary = {"required": [], "not_required": [], "unknown_or_null": []}
    by_authorized = {"present": [], "absent": [], "unknown_or_null": []}

    for index, node in enumerate(nodes):
        nid = node["node_id"]
        append_lookup(by_node_kind, node.get("node_kind"), nid)
        append_lookup(by_receipt_id, node.get("receipt_id"), nid)
        append_lookup(by_commit_sha, node.get("commit_sha"), nid)
        append_lookup(by_phase, node.get("phase"), nid)
        append_lookup(by_terminal_stop_code, node.get("terminal_stop_code"), nid)
        append_lookup(by_outcome_class, node.get("outcome_class"), nid)
        append_lookup(by_status, node.get("status"), nid)

        human_boundary = node.get("human_boundary_required")
        if human_boundary is True:
            by_human_boundary["required"].append(nid)
        elif human_boundary is False:
            by_human_boundary["not_required"].append(nid)
        else:
            by_human_boundary["unknown_or_null"].append(nid)

        authorized = node.get("authorized_future_unit")
        if authorized is None:
            by_authorized["unknown_or_null"].append(nid)
        elif authorized:
            by_authorized["present"].append(nid)
        else:
            by_authorized["absent"].append(nid)

    for edge in edges:
        append_lookup(by_edge_kind, edge.get("edge_kind"), edge["edge_id"])

    return {
        "lookup_by_node_id": {node["node_id"]: index for index, node in enumerate(nodes)},
        "lookup_by_edge_id": {edge["edge_id"]: index for index, edge in enumerate(edges)},
        "lookup_by_node_kind": dict(by_node_kind),
        "lookup_by_edge_kind": dict(by_edge_kind),
        "lookup_by_human_boundary": by_human_boundary,
        "lookup_by_authorized_future_unit_present": by_authorized,
        "lookup_by_receipt_id": dict(by_receipt_id),
        "lookup_by_commit_sha": dict(by_commit_sha),
        "lookup_by_phase": dict(by_phase),
        "lookup_by_terminal_stop_code": dict(by_terminal_stop_code),
        "lookup_by_outcome_class": dict(by_outcome_class),
        "lookup_by_status": dict(by_status),
    }


def validate_index(
    source: dict[str, Any],
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[str]]:
    failures: list[str] = []
    source_nodes = source.get("nodes", [])
    source_edges = source.get("edges", [])
    node_numbers = [node.get("node_number") for node in nodes]
    expected_numbers = list(range(1, len(nodes) + 1))
    expected_edges = [(i, i + 1) for i in range(1, len(edges) + 1)]
    got_edges = [(edge.get("from_node_number"), edge.get("to_node_number")) for edge in edges]
    node_ids = [node.get("node_id") for node in nodes]
    edge_ids = [edge.get("edge_id") for edge in edges]
    node_id_set = set(node_ids)

    checks = {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "node_ids_unique": len(node_ids) == len(set(node_ids)),
        "edge_ids_unique": len(edge_ids) == len(set(edge_ids)),
        "node_numbers_contiguous": node_numbers == expected_numbers,
        "edges_forward_linear": got_edges == expected_edges,
        "edge_endpoints_resolve": all(
            edge.get("from_node_id") in node_id_set and edge.get("to_node_id") in node_id_set
            for edge in edges
        ),
        "source_schema_version_preserved": source.get("schema_version") == SOURCE_SCHEMA_VERSION,
        "source_readout_status_preserved": source.get("readout_status") == SOURCE_READOUT_STATUS,
    }
    if len(nodes) != len(source_nodes):
        failures.append(f"indexed_node_count_wrong:{len(nodes)}!={len(source_nodes)}")
    if len(edges) != len(source_edges):
        failures.append(f"indexed_edge_count_wrong:{len(edges)}!={len(source_edges)}")
    for key, value in checks.items():
        if isinstance(value, bool) and not value:
            failures.append(f"{key}_false")

    validation = {
        "index_status": INDEX_STATUS_PASS if not failures else INDEX_STATUS_FAIL,
        "validation_depth": "index_shape_only",
        "receipt_validation_performed": False,
        "receipt_hash_validation_performed": False,
        "authority_validation_performed": False,
        "compression_validation_performed": False,
        "taxonomy_validation_performed": False,
        **checks,
    }
    if failures:
        validation["failures"] = failures
    return validation, failures


def address_contract(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "path_id": PATH_ID,
        "node_id_pattern": "c8.nNN",
        "edge_id_pattern": "c8.eNN_NN",
        "node_id_range": [nodes[0]["node_id"], nodes[-1]["node_id"]] if nodes else [],
        "edge_id_range": [edges[0]["edge_id"], edges[-1]["edge_id"]] if edges else [],
        "node_ids_stable_within_source_readout": True,
        "edge_ids_stable_within_source_readout": True,
        "global_permanent_ids_claimed": False,
        "statements": ADDRESS_STATEMENTS,
    }


def compact(value: Any, max_chars: int = 74) -> str:
    if value is None:
        return ""
    text = str(value)
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3] + "..."


def count_map(values: list[Any]) -> dict[str, int]:
    return dict(sorted(Counter(str(value) for value in values if value is not None).items()))


def render_markdown(index: dict[str, Any]) -> str:
    nodes = index["nodes"]
    edges = index["edges"]
    lookups = index["lookups"]
    validation = index["index_validation"]
    source = index["source"]
    node_kind_counts = count_map([node.get("node_kind") for node in nodes])
    edge_kind_counts = count_map([edge.get("edge_kind") for edge in edges])
    human_counts = {key: len(value) for key, value in lookups["lookup_by_human_boundary"].items()}
    authorized_counts = {
        key: len(value) for key, value in lookups["lookup_by_authorized_future_unit_present"].items()
    }

    parts = [
        "# Decision Path Index v0",
        "",
        "## Status",
        "",
        "Source-preserving lookup surface. Shape-only validation. Not authority.",
        "",
        "## Source",
        "",
        f"- Source JSON: `{source['source_path_json']}`",
        f"- Source Markdown: `{source['source_path_md']}`",
        f"- Source schema: `{source['source_schema_version']}`",
        f"- Source readout status: `{source['source_readout_status']}`",
        f"- Source JSON SHA256: `{source['source_json_sha256']}`",
        f"- Source commit SHA: `{source['source_commit_sha'] or 'null'}`",
        "",
        "## Address contract",
        "",
        *[f"- {statement}" for statement in ADDRESS_STATEMENTS],
        "",
        "## Compact counts",
        "",
        f"- node_count: `{len(nodes)}`",
        f"- edge_count: `{len(edges)}`",
        f"- node kind counts: `{json.dumps(node_kind_counts, sort_keys=True)}`",
        f"- edge kind counts: `{json.dumps(edge_kind_counts, sort_keys=True)}`",
        f"- human boundary counts: `{json.dumps(human_counts, sort_keys=True)}`",
        f"- authorized future unit counts: `{json.dumps(authorized_counts, sort_keys=True)}`",
        "",
        "## Node index",
        "",
        "| node_id | node_number | node_kind | phase | receipt_id | commit_sha | human_boundary_required | authorized_future_unit |",
        "| --- | ---: | --- | --- | --- | --- | --- | --- |",
    ]
    for node in nodes:
        parts.append(
            "| {node_id} | {node_number} | {node_kind} | {phase} | {receipt_id} | {commit_sha} | {human_boundary_required} | {authorized_future_unit} |".format(
                node_id=node["node_id"],
                node_number=node["node_number"],
                node_kind=compact(node.get("node_kind")),
                phase=compact(node.get("phase"), 60),
                receipt_id=compact(node.get("receipt_id"), 44),
                commit_sha=compact(node.get("commit_sha"), 12),
                human_boundary_required=node.get("human_boundary_required"),
                authorized_future_unit=compact(node.get("authorized_future_unit"), 54),
            )
        )

    parts.extend([
        "",
        "## Edge index",
        "",
        "| edge_id | from | to | edge_kind | source_evidence_path |",
        "| --- | --- | --- | --- | --- |",
    ])
    for edge in edges:
        parts.append(
            "| {edge_id} | {from_node_id} | {to_node_id} | {edge_kind} | {source_evidence_path} |".format(
                edge_id=edge["edge_id"],
                from_node_id=edge["from_node_id"],
                to_node_id=edge["to_node_id"],
                edge_kind=compact(edge.get("edge_kind")),
                source_evidence_path=compact(edge.get("source_evidence_path"), 84),
            )
        )

    parts.extend([
        "",
        "## Lookup tables",
        "",
        f"- lookup_by_node_id: `{len(lookups['lookup_by_node_id'])}` entries",
        f"- lookup_by_edge_id: `{len(lookups['lookup_by_edge_id'])}` entries",
        f"- lookup_by_node_kind: `{json.dumps({k: len(v) for k, v in lookups['lookup_by_node_kind'].items()}, sort_keys=True)}`",
        f"- lookup_by_edge_kind: `{json.dumps({k: len(v) for k, v in lookups['lookup_by_edge_kind'].items()}, sort_keys=True)}`",
        f"- lookup_by_human_boundary: `{json.dumps(human_counts, sort_keys=True)}`",
        f"- lookup_by_authorized_future_unit_present: `{json.dumps(authorized_counts, sort_keys=True)}`",
        f"- lookup_by_receipt_id: `{len(lookups['lookup_by_receipt_id'])}` keys",
        f"- lookup_by_commit_sha: `{len(lookups['lookup_by_commit_sha'])}` keys",
        f"- optional lookup_by_phase: `{len(lookups['lookup_by_phase'])}` keys",
        f"- optional lookup_by_terminal_stop_code: `{len(lookups['lookup_by_terminal_stop_code'])}` keys",
        f"- optional lookup_by_outcome_class: `{len(lookups['lookup_by_outcome_class'])}` keys",
        f"- optional lookup_by_status: `{len(lookups['lookup_by_status'])}` keys",
        "",
        "## Validation depth",
        "",
        f"- index_status: `{validation['index_status']}`",
        f"- validation_depth: `{validation['validation_depth']}`",
        f"- receipt_validation_performed: `{validation['receipt_validation_performed']}`",
        f"- receipt_hash_validation_performed: `{validation['receipt_hash_validation_performed']}`",
        f"- authority_validation_performed: `{validation['authority_validation_performed']}`",
        f"- compression_validation_performed: `{validation['compression_validation_performed']}`",
        f"- taxonomy_validation_performed: `{validation['taxonomy_validation_performed']}`",
        f"- node_ids_unique: `{validation['node_ids_unique']}`",
        f"- edge_ids_unique: `{validation['edge_ids_unique']}`",
        f"- node_numbers_contiguous: `{validation['node_numbers_contiguous']}`",
        f"- edges_forward_linear: `{validation['edges_forward_linear']}`",
        f"- edge_endpoints_resolve: `{validation['edge_endpoints_resolve']}`",
        "",
        "## Non-claims",
        "",
        *[f"- {claim}" for claim in NON_CLAIMS],
        "",
        "## Relationship to later milestones",
        "",
        *[f"- {item}" for item in LATER_MILESTONES],
    ])
    return "\n".join(parts)


def build_index(root: Path) -> dict[str, Any]:
    source = load_source(root)
    warnings: list[str] = []
    source_nodes = source.get("nodes")
    source_edges = source.get("edges")
    if not isinstance(source_nodes, list) or not all(isinstance(node, dict) for node in source_nodes):
        raise GenerationError("source nodes must be a list of objects")
    if not isinstance(source_edges, list) or not all(isinstance(edge, dict) for edge in source_edges):
        raise GenerationError("source edges must be a list of objects")

    nodes = build_nodes(source_nodes, warnings)
    edges = build_edges(source_edges, warnings)
    lookups = build_lookups(nodes, edges)
    validation, failures = validate_index(source, nodes, edges)
    status = validation["index_status"]
    source_commit_sha = verified_source_commit(root)
    if source_commit_sha is None:
        warnings.append("source_commit_sha_not_found_or_unverified")

    index = {
        "schema_version": SCHEMA_VERSION,
        "index_status": status,
        "index_role": "source_preserving_lookup_surface",
        "path_id": PATH_ID,
        "path_name": PATH_NAME,
        "source": {
            "source_path_json": str(SOURCE_JSON),
            "source_path_md": str(SOURCE_MD),
            "source_schema_version": source.get("schema_version"),
            "source_readout_status": source.get("readout_status"),
            "source_json_sha256": sha256_file(root / SOURCE_JSON),
            "source_commit_sha": source_commit_sha,
        },
        "address_contract": address_contract(nodes, edges),
        "field_policy": "source_fields_are_copied_or_null_preserved_without_reinterpretation",
        "missing_source_field_policy": "preserve_as_null_and_record_in_index_warnings",
        "nodes": nodes,
        "edges": edges,
        "lookups": lookups,
        "index_validation": validation,
        "index_warnings": warnings,
        "non_claims": NON_CLAIMS,
        "relationship_to_later_milestones": LATER_MILESTONES,
        "generated_by": GENERATED_BY,
    }
    if failures:
        index["index_warnings"].extend(failures)
    return index


def generate() -> int:
    root = detect_repo_root(Path.cwd())
    index = build_index(root)
    (root / OUTPUT_JSON).parent.mkdir(parents=True, exist_ok=True)
    (root / OUTPUT_JSON).write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (root / OUTPUT_MD).write_text(render_markdown(index).rstrip() + "\n", encoding="utf-8")
    print(
        "Generated decision_path_index_v0: "
        f"status={index['index_status']} "
        f"nodes={len(index['nodes'])} "
        f"edges={len(index['edges'])} "
        f"source_commit={index['source']['source_commit_sha'] or 'null'}"
    )
    return 0 if index["index_status"] == INDEX_STATUS_PASS else 2


def main() -> int:
    try:
        return generate()
    except GenerationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
