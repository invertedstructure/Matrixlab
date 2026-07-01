#!/usr/bin/env python3
"""Build MatrixLabs receipt_spine_v0.

M2 creates an evidence-anchoring spine over decision_path_index_v0.
It checks receipt pointer/surface consistency only; it does not replay runtime,
prove edge lawfulness, classify taxonomy, compress meaning, or authorize moves.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "matrixlabs_receipt_spine_v0"
SPINE_ROLE = "evidence_backbone_over_decision_path_index"
SOURCE_INDEX = Path("docs/matrixlabs/observability/decision_path_index_v0.json")
SOURCE_OBSERVED = Path("docs/matrixlabs/architecture/c8_observed_decision_path_v0.json")
OUTPUT_JSON = Path("docs/matrixlabs/observability/receipt_spine_v0.json")
OUTPUT_MD = Path("docs/matrixlabs/observability/receipt_spine_v0.md")
GENERATED_BY = "scripts/build_receipt_spine_v0.py"

SOURCE_INDEX_SCHEMA = "matrixlabs_decision_path_index_v0"
SOURCE_OBSERVED_SCHEMA = "matrixlabs_c8_observed_decision_path_v0"

BACKING_RUNTIME = "RUNTIME_RECEIPT"
BACKING_SOURCE_META = "SOURCE_COMMIT_ONLY_META_HANDOFF"
BACKING_MISSING = "MISSING_RECEIPT"
BACKING_MALFORMED = "MALFORMED_RECEIPT"
BACKING_MISMATCH = "RECEIPT_FIELD_MISMATCH"
BACKING_UNTYPED = "UNTYPED_NO_RECEIPT"
BACKING_UNEXPECTED_META = "UNEXPECTED_RECEIPT_ON_META"

NODE_PASS = "SPINE_NODE_PASS"
NODE_SOURCE_META = "SPINE_NODE_SOURCE_COMMIT_ONLY"
NODE_MISSING = "SPINE_NODE_RECEIPT_MISSING"
NODE_PARSE_FAIL = "SPINE_NODE_RECEIPT_PARSE_FAIL"
NODE_MISMATCH = "SPINE_NODE_FIELD_MISMATCH"
NODE_UNTYPED = "SPINE_NODE_UNTYPED_NO_RECEIPT"
NODE_UNEXPECTED_META = "SPINE_NODE_UNEXPECTED_RECEIPT_ON_META"

SPINE_PASS = "SPINE_PASS"
SPINE_PASS_WITH_META = "SPINE_PASS_WITH_SOURCE_COMMIT_ONLY_META_NODES"
SPINE_FAIL_MISSING = "SPINE_FAIL_MISSING_RECEIPTS"
SPINE_FAIL_MISMATCH = "SPINE_FAIL_FIELD_MISMATCH"
SPINE_FAIL_PARSE = "SPINE_FAIL_PARSE"
SPINE_FAIL_UNTYPED = "SPINE_FAIL_UNTYPED_BACKING_KIND"
SPINE_FAIL_UNEXPECTED_META = "SPINE_FAIL_UNEXPECTED_RECEIPT_ON_META"

EDGE_POINTER_PRESENT = "EDGE_EVIDENCE_POINTER_PRESENT"
EDGE_POINTER_MISSING = "EDGE_EVIDENCE_POINTER_MISSING"
EDGE_TOUCHES_META = "EDGE_TOUCHES_SOURCE_COMMIT_ONLY_META_NODE"

NON_CLAIMS = [
    "Does not replay the runtime.",
    "Does not validate that the receipt's runtime claim is operationally or mathematically true.",
    "Does not prove the edge from this node to the next is lawful.",
    "Does not decide whether authorized_future_unit was correctly consumed downstream.",
    "Does not classify proceed surfaces into taxonomy.",
    "Does not compress repeated transition patterns.",
    "Does not promote source-commit-only meta nodes into C8 runtime receipts.",
    "Does not authorize future units.",
    "Does not create reusable/preapproved authority.",
    "Does not build a runner.",
]

COMPARABLE_FIELDS = [
    "status",
    "outcome_class",
    "terminal_stop_code",
    "authorized_future_unit",
    "human_decision_consumed",
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


def git_commit_exists(root: Path, sha: str | None) -> bool:
    if not sha:
        return False
    proc = subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return proc.returncode == 0


def commit_for_paths(root: Path, paths: list[Path]) -> str:
    args = ["log", "-n", "1", "--format=%H", "--", *[str(path) for path in paths]]
    commit = run_git(root, args)
    if not git_commit_exists(root, commit):
        raise GenerationError(f"could not verify source commit for: {', '.join(str(p) for p in paths)}")
    return commit


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GenerationError(f"missing JSON source: {path}") from exc
    except json.JSONDecodeError as exc:
        raise GenerationError(f"invalid JSON source: {path}") from exc


def is_present(value: Any) -> bool:
    return value is not None and value != ""


def backing_kind(node: dict[str, Any]) -> str:
    receipt_path = node.get("receipt_path") or ""
    receipt_id = node.get("receipt_id") or ""
    is_source_meta = receipt_id == "source_commit_only_meta_handoff" and node.get("node_kind") == "meta_handoff"
    if is_source_meta and receipt_path:
        return BACKING_UNEXPECTED_META
    if receipt_path:
        return BACKING_RUNTIME
    if is_source_meta:
        return BACKING_SOURCE_META
    return BACKING_UNTYPED


def first_present_path(data: dict[str, Any], candidates: list[tuple[str, ...]]) -> tuple[Any, str | None]:
    for path in candidates:
        current: Any = data
        found = True
        for part in path:
            if not isinstance(current, dict) or part not in current:
                found = False
                break
            current = current[part]
        if found and current is not None and current != "":
            return current, ".".join(path)
    return None, None


def summary_dicts(data: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    out: list[tuple[str, dict[str, Any]]] = []
    for key, value in data.items():
        if isinstance(value, dict) and (key == "summary" or key.endswith("_summary") or "summary" in key):
            out.append((key, value))
    return out


def extract_field(data: dict[str, Any], field: str) -> tuple[Any, str | None]:
    direct_candidates: dict[str, list[tuple[str, ...]]] = {
        "receipt_id": [("receipt_id",), ("receipt", "receipt_id"), ("result", "receipt_id")],
        "status": [("status",), ("receipt", "status"), ("result", "status")],
        "outcome_class": [("outcome_class",), ("receipt", "outcome_class"), ("result", "outcome_class")],
        "terminal_stop_code": [
            ("terminal_stop_code",),
            ("stop_code",),
            ("stop_condition",),
            ("terminal", "stop_code"),
            ("terminal", "terminal_stop_code"),
            ("terminal", "stop_condition"),
        ],
        "authorized_future_unit": [
            ("authorized_future_unit",),
            ("authority", "authorized_future_unit"),
            ("decision", "authorized_future_unit"),
            ("packet", "authorized_future_unit"),
            ("summary", "authorized_future_unit"),
            ("summary", "authorized_future_unit_after_review"),
        ],
        "human_decision_consumed": [
            ("human_decision_consumed",),
            ("human_decision",),
            ("decision", "human_decision"),
            ("packet", "human_decision"),
            ("summary", "human_decision_consumed"),
            ("summary", "human_decision"),
            ("summary", "recommended_human_decision"),
        ],
    }
    value, path = first_present_path(data, direct_candidates[field])
    if path is not None:
        return value, path

    summary_keys = {
        "authorized_future_unit": ["authorized_future_unit", "authorized_future_unit_after_review"],
        "human_decision_consumed": ["human_decision_consumed", "human_decision", "recommended_human_decision"],
    }.get(field, [])
    for summary_name, summary in summary_dicts(data):
        for key in summary_keys:
            value = summary.get(key)
            if value is not None and value != "":
                return value, f"{summary_name}.{key}"
    return None, None


def extract_forbidden_counter_keys(data: Any, prefix: str = "") -> list[str]:
    terms = ("forbidden", "counter", "not_authorized", "prohibited")
    found: set[str] = set()
    if isinstance(data, dict):
        for key, value in data.items():
            path = f"{prefix}.{key}" if prefix else key
            key_l = key.lower()
            path_l = path.lower()
            if isinstance(value, dict) and any(term in path_l for term in terms):
                found.update(str(child_key) for child_key in value.keys())
            elif not isinstance(value, (dict, list)) and any(term in key_l for term in terms):
                found.add(path)
            found.update(extract_forbidden_counter_keys(value, path))
    elif isinstance(data, list):
        for index, value in enumerate(data):
            found.update(extract_forbidden_counter_keys(value, f"{prefix}[{index}]"))
    return sorted(found)


def extract_receipt_fields(data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str], list[str]]:
    fields: dict[str, Any] = {}
    paths: dict[str, str] = {}
    warnings: list[str] = []
    for field in ["receipt_id", *COMPARABLE_FIELDS]:
        value, path = extract_field(data, field)
        fields[field] = value
        if path:
            paths[field] = path
    fields["forbidden_counter_keys"] = extract_forbidden_counter_keys(data)
    if "receipt_id" not in paths:
        warnings.append("receipt_id_not_extracted_from_parsed_receipt")
    return fields, paths, warnings


def consistency_for(
    node: dict[str, Any],
    extracted: dict[str, Any],
    paths: dict[str, str],
    warnings: list[str],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    mismatches: list[dict[str, Any]] = []
    consistency: dict[str, Any] = {}

    declared_receipt_id = node.get("receipt_id")
    receipt_id = extracted.get("receipt_id")
    receipt_id_matches = declared_receipt_id == receipt_id if receipt_id is not None else False
    consistency["receipt_id_matches"] = receipt_id_matches
    if not receipt_id_matches:
        mismatches.append({
            "node_id": node.get("node_id"),
            "field": "receipt_id",
            "index_value": declared_receipt_id,
            "receipt_value": receipt_id,
            "receipt_key_path": paths.get("receipt_id"),
        })

    for field in COMPARABLE_FIELDS:
        index_value = node.get(field)
        receipt_value = extracted.get(field)
        key = f"{field}_matches"
        if is_present(index_value) and is_present(receipt_value):
            if field == "outcome_class" and index_value != receipt_value:
                consistency[key] = None
                warnings.append(
                    "outcome_class_present_in_both_but_not_marked_comparable_for_v0:"
                    f"index={index_value};receipt={receipt_value};path={paths.get(field)}"
                )
                continue
            consistency[key] = index_value == receipt_value
            if not consistency[key]:
                mismatches.append({
                    "node_id": node.get("node_id"),
                    "field": field,
                    "index_value": index_value,
                    "receipt_value": receipt_value,
                    "receipt_key_path": paths.get(field),
                })
        elif is_present(index_value) and not is_present(receipt_value):
            consistency[key] = None
            warnings.append(f"{field}_present_in_index_missing_from_receipt")
        else:
            consistency[key] = None
    return consistency, mismatches


def blank_runtime_record(node: dict[str, Any], kind: str, status: str) -> dict[str, Any]:
    return {
        "node_id": node.get("node_id"),
        "node_number": node.get("node_number"),
        "phase": node.get("phase"),
        "node_kind": node.get("node_kind"),
        "receipt_backing_kind": kind,
        "declared_receipt_id": node.get("receipt_id"),
        "declared_receipt_path": node.get("receipt_path") or "",
        "receipt_exists": False if kind == BACKING_MISSING else None,
        "receipt_parse_ok": None,
        "receipt_sha256": None,
        "receipt_sig8": None,
        "receipt_file_size": None,
        "receipt_top_level_keys": [],
        "receipt_fields_extracted": {},
        "index_receipt_consistency": {},
        "field_extraction_warnings": [],
        "spine_status": status,
    }


def build_source_meta_node(node: dict[str, Any], kind: str = BACKING_SOURCE_META, status: str = NODE_SOURCE_META) -> dict[str, Any]:
    return {
        "node_id": node.get("node_id"),
        "node_number": node.get("node_number"),
        "phase": node.get("phase"),
        "node_kind": node.get("node_kind"),
        "receipt_backing_kind": kind,
        "declared_receipt_id": node.get("receipt_id"),
        "declared_receipt_path": node.get("receipt_path") or "",
        "receipt_exists": None,
        "receipt_parse_ok": None,
        "receipt_sha256": None,
        "receipt_sig8": None,
        "receipt_file_size": None,
        "receipt_top_level_keys": [],
        "commit_sha": node.get("commit_sha"),
        "artifact_dir": node.get("artifact_dir"),
        "receipt_fields_extracted": {},
        "index_receipt_consistency": {},
        "field_extraction_warnings": [],
        "spine_status": status,
    }


def build_runtime_node(root: Path, node: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    declared_path = node.get("receipt_path") or ""
    if not declared_path:
        return blank_runtime_record(node, BACKING_MISSING, NODE_MISSING), []

    path = root / declared_path
    if not path.exists():
        return blank_runtime_record(node, BACKING_MISSING, NODE_MISSING), []

    raw = path.read_bytes()
    receipt_sha = hashlib.sha256(raw).hexdigest()
    record = {
        "node_id": node.get("node_id"),
        "node_number": node.get("node_number"),
        "phase": node.get("phase"),
        "node_kind": node.get("node_kind"),
        "receipt_backing_kind": BACKING_RUNTIME,
        "declared_receipt_id": node.get("receipt_id"),
        "declared_receipt_path": declared_path,
        "receipt_exists": True,
        "receipt_parse_ok": None,
        "receipt_sha256": receipt_sha,
        "receipt_sig8": receipt_sha[:8],
        "receipt_file_size": len(raw),
        "receipt_top_level_keys": [],
        "receipt_fields_extracted": {},
        "index_receipt_consistency": {},
        "field_extraction_warnings": [],
        "spine_status": NODE_PASS,
    }

    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        record["receipt_parse_ok"] = False
        record["field_extraction_warnings"].append(f"receipt_parse_failed:{type(exc).__name__}")
        record["receipt_backing_kind"] = BACKING_MALFORMED
        record["spine_status"] = NODE_PARSE_FAIL
        return record, []

    if not isinstance(parsed, dict):
        record["receipt_parse_ok"] = False
        record["field_extraction_warnings"].append("receipt_json_top_level_not_object")
        record["receipt_backing_kind"] = BACKING_MALFORMED
        record["spine_status"] = NODE_PARSE_FAIL
        return record, []

    record["receipt_parse_ok"] = True
    record["receipt_top_level_keys"] = sorted(parsed.keys())
    extracted, paths, warnings = extract_receipt_fields(parsed)
    consistency, mismatches = consistency_for(node, extracted, paths, warnings)
    record["receipt_fields_extracted"] = extracted
    record["receipt_field_key_paths"] = paths
    record["index_receipt_consistency"] = consistency
    record["field_extraction_warnings"] = warnings
    if mismatches:
        record["receipt_backing_kind"] = BACKING_MISMATCH
        record["spine_status"] = NODE_MISMATCH
    return record, mismatches


def build_nodes(root: Path, index_nodes: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    spine_nodes: list[dict[str, Any]] = []
    mismatches: list[dict[str, Any]] = []
    warnings: list[str] = []
    for node in index_nodes:
        kind = backing_kind(node)
        if kind == BACKING_RUNTIME:
            record, node_mismatches = build_runtime_node(root, node)
            spine_nodes.append(record)
            mismatches.extend(node_mismatches)
        elif kind == BACKING_SOURCE_META:
            spine_nodes.append(build_source_meta_node(node))
        elif kind == BACKING_UNEXPECTED_META:
            spine_nodes.append(build_source_meta_node(node, BACKING_UNEXPECTED_META, NODE_UNEXPECTED_META))
        elif kind == BACKING_UNTYPED:
            spine_nodes.append(blank_runtime_record(node, BACKING_UNTYPED, NODE_UNTYPED))
        else:
            spine_nodes.append(blank_runtime_record(node, kind, NODE_MISSING))

        sha = node.get("commit_sha")
        if sha and not git_commit_exists(root, sha):
            warnings.append(f"{node.get('node_id')}_commit_sha_not_in_local_git:{sha}")
            mismatches.append({
                "node_id": node.get("node_id"),
                "field": "commit_sha",
                "index_value": sha,
                "receipt_value": None,
                "receipt_key_path": None,
            })
    return spine_nodes, mismatches, warnings


def build_edges(index_edges: list[dict[str, Any]], node_by_id: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    edges: list[dict[str, Any]] = []
    for edge in index_edges:
        from_node = node_by_id.get(edge.get("from_node_id"), {})
        to_node = node_by_id.get(edge.get("to_node_id"), {})
        evidence_path = edge.get("source_evidence_path")
        touches_meta = (
            from_node.get("receipt_backing_kind") == BACKING_SOURCE_META
            or to_node.get("receipt_backing_kind") == BACKING_SOURCE_META
        )
        if touches_meta:
            status = EDGE_TOUCHES_META
        elif evidence_path:
            status = EDGE_POINTER_PRESENT
        else:
            status = EDGE_POINTER_MISSING
        edges.append({
            "edge_id": edge.get("edge_id"),
            "from_node_id": edge.get("from_node_id"),
            "to_node_id": edge.get("to_node_id"),
            "from_node_spine_status": from_node.get("spine_status"),
            "to_node_spine_status": to_node.get("spine_status"),
            "edge_receipt_evidence_path": evidence_path,
            "edge_evidence_status": status,
            "edge_semantic_validation_performed": False,
        })
    return edges


def spine_status(counts: dict[str, int]) -> str:
    if counts["unexpected_meta"] > 0:
        return SPINE_FAIL_UNEXPECTED_META
    if counts["untyped"] > 0:
        return SPINE_FAIL_UNTYPED
    if counts["parse_fail"] > 0:
        return SPINE_FAIL_PARSE
    if counts["missing"] > 0:
        return SPINE_FAIL_MISSING
    if counts["field_mismatch"] > 0:
        return SPINE_FAIL_MISMATCH
    if counts["source_meta"] > 0:
        return SPINE_PASS_WITH_META
    return SPINE_PASS


def compact(value: Any, max_chars: int = 70) -> str:
    if value is None:
        return ""
    text = str(value)
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3] + "..."


def render_markdown(spine: dict[str, Any]) -> str:
    node_status = {node["node_id"]: node for node in spine["nodes"]}
    edge_counts = dict(Counter(edge["edge_evidence_status"] for edge in spine["edges"]))
    meta_nodes = [
        node for node in spine["nodes"]
        if node["receipt_backing_kind"] == BACKING_SOURCE_META
    ]
    parts = [
        "# Receipt Spine v0",
        "",
        "## Status",
        "",
        spine["spine_status"],
        "",
        "## Boundary",
        "",
        "This spine validates receipt pointer/surface consistency only.",
        "",
        "It does not validate runtime truth, edge lawfulness, compression, taxonomy, reusable authority, or future authorization.",
        "",
        "## Source",
        "",
        f"- Source index path: `{spine['source_index_path']}`",
        f"- Source observed path: `{spine['source_observed_path']}`",
        f"- Source index SHA256: `{spine['source_index_sha256']}`",
        f"- Observed path SHA256: `{spine['source_observed_path_sha256']}`",
        f"- Source index commit: `{spine['source_index_commit_sha']}`",
        f"- Observed path commit: `{spine['source_observed_path_commit_sha']}`",
        "",
        "## Coverage",
        "",
        f"- {spine['node_count']} indexed nodes",
        f"- {spine['runtime_receipt_node_count']} runtime receipt-backed nodes",
        f"- {spine['source_commit_only_meta_node_count']} source-commit-only meta-handoff nodes",
        f"- {spine['receipt_missing_count']} missing receipts",
        f"- {spine['receipt_parse_fail_count']} parse failures",
        f"- {spine['field_mismatch_count']} index/receipt field mismatches",
        "",
        "## Node spine table",
        "",
        "| node_id | phase | receipt_backing_kind | receipt_id | receipt_sig8 | status_match | terminal_stop_code_match | spine_status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for node in spine["nodes"]:
        consistency = node.get("index_receipt_consistency", {})
        parts.append(
            "| {node_id} | {phase} | {kind} | {receipt_id} | {sig8} | {status_match} | {terminal_match} | {spine_status} |".format(
                node_id=node["node_id"],
                phase=compact(node.get("phase"), 42),
                kind=node.get("receipt_backing_kind"),
                receipt_id=compact(node.get("declared_receipt_id"), 42),
                sig8=node.get("receipt_sig8") or "",
                status_match=consistency.get("status_matches"),
                terminal_match=consistency.get("terminal_stop_code_matches"),
                spine_status=node.get("spine_status"),
            )
        )

    parts.extend([
        "",
        "## Source-commit-only meta nodes",
        "",
    ])
    if meta_nodes:
        for node in meta_nodes:
            parts.append(
                f"- `{node['node_id']}` - {node.get('phase')} - commit `{node.get('commit_sha')}` - artifact `{node.get('artifact_dir')}`"
            )
    else:
        parts.append("- None.")

    parts.extend([
        "",
        "## Edge evidence overlay",
        "",
        f"- Edge evidence status counts: `{json.dumps(edge_counts, sort_keys=True)}`",
        "- Edge records preserve evidence pointers only; they do not claim lawfulness.",
        "",
        "| edge_id | from | to | evidence_status | evidence_path |",
        "| --- | --- | --- | --- | --- |",
    ])
    for edge in spine["edges"]:
        parts.append(
            f"| {edge['edge_id']} | {edge['from_node_id']} | {edge['to_node_id']} | {edge['edge_evidence_status']} | {compact(edge.get('edge_receipt_evidence_path'), 72)} |"
        )

    parts.extend([
        "",
        "## Mismatches / warnings",
        "",
    ])
    if spine["mismatches"]:
        for item in spine["mismatches"]:
            parts.append(f"- mismatch `{item.get('node_id')}` `{item.get('field')}`")
    else:
        parts.append("- No field mismatches.")
    if spine["warnings"]:
        for item in spine["warnings"]:
            parts.append(f"- warning: {item}")

    parts.extend([
        "",
        "## Non-claims",
        "",
        *[f"- {claim}" for claim in NON_CLAIMS],
        "",
        "## Relationship to M3",
        "",
        "M2 gives M3 evidence-anchored addresses.",
        "M3 defines what may be compressed and what decompression must recover.",
    ])
    return "\n".join(parts)


def build_spine(root: Path) -> dict[str, Any]:
    index = load_json(root / SOURCE_INDEX)
    observed = load_json(root / SOURCE_OBSERVED)
    index_nodes = index.get("nodes", [])
    index_edges = index.get("edges", [])
    if not isinstance(index_nodes, list) or not all(isinstance(node, dict) for node in index_nodes):
        raise GenerationError("source index nodes must be a list of objects")
    if not isinstance(index_edges, list) or not all(isinstance(edge, dict) for edge in index_edges):
        raise GenerationError("source index edges must be a list of objects")

    source_index_commit = commit_for_paths(
        root,
        [
            SOURCE_INDEX,
            Path("docs/matrixlabs/observability/decision_path_index_v0.md"),
            Path("scripts/build_decision_path_index_v0.py"),
        ],
    )
    source_observed_commit = commit_for_paths(
        root,
        [
            SOURCE_OBSERVED,
            Path("docs/matrixlabs/architecture/c8_observed_decision_path_v0.md"),
        ],
    )

    nodes, mismatches, warnings = build_nodes(root, index_nodes)
    node_by_id = {node["node_id"]: node for node in nodes}
    edges = build_edges(index_edges, node_by_id)

    backing_counts = Counter(node["receipt_backing_kind"] for node in nodes)
    status_counts = Counter(node["spine_status"] for node in nodes)
    count_data = {
        "unexpected_meta": backing_counts[BACKING_UNEXPECTED_META],
        "untyped": backing_counts[BACKING_UNTYPED],
        "parse_fail": status_counts[NODE_PARSE_FAIL],
        "missing": status_counts[NODE_MISSING],
        "field_mismatch": len(mismatches),
        "source_meta": backing_counts[BACKING_SOURCE_META],
    }
    top_status = spine_status(count_data)

    return {
        "schema_version": SCHEMA_VERSION,
        "spine_role": SPINE_ROLE,
        "source_index_path": str(SOURCE_INDEX),
        "source_observed_path": str(SOURCE_OBSERVED),
        "source_index_schema": index.get("schema_version"),
        "source_observed_path_schema": observed.get("schema_version"),
        "source_index_sha256": sha256_file(root / SOURCE_INDEX),
        "source_observed_path_sha256": sha256_file(root / SOURCE_OBSERVED),
        "source_index_commit_sha": source_index_commit,
        "source_observed_path_commit_sha": source_observed_commit,
        "validation_depth": "receipt_pointer_and_surface_consistency_only",
        "runtime_replay_performed": False,
        "receipt_hashes_computed": True,
        "receipt_hash_validation_performed": False,
        "receipt_content_truth_validation_performed": False,
        "edge_lawfulness_validation_performed": False,
        "taxonomy_classification_performed": False,
        "compression_performed": False,
        "future_authority_created": False,
        "reusable_preapproved_authority_created": False,
        "runner_created": False,
        "node_count": len(nodes),
        "runtime_receipt_node_count": backing_counts[BACKING_RUNTIME],
        "source_commit_only_meta_node_count": backing_counts[BACKING_SOURCE_META],
        "receipt_exists_count": sum(1 for node in nodes if node.get("receipt_exists") is True),
        "receipt_missing_count": status_counts[NODE_MISSING],
        "receipt_parse_fail_count": status_counts[NODE_PARSE_FAIL],
        "field_mismatch_count": len(mismatches),
        "spine_status": top_status,
        "nodes": nodes,
        "edges": edges,
        "mismatches": mismatches,
        "warnings": warnings,
        "non_claims": NON_CLAIMS,
        "generated_by": GENERATED_BY,
    }


def generate() -> int:
    root = detect_repo_root(Path.cwd())
    spine = build_spine(root)
    output_json = root / OUTPUT_JSON
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(spine, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (root / OUTPUT_MD).write_text(render_markdown(spine).rstrip() + "\n", encoding="utf-8")
    print(
        "Generated receipt_spine_v0: "
        f"status={spine['spine_status']} "
        f"nodes={spine['node_count']} "
        f"runtime_receipts={spine['runtime_receipt_node_count']} "
        f"source_meta={spine['source_commit_only_meta_node_count']} "
        f"missing={spine['receipt_missing_count']} "
        f"parse_fail={spine['receipt_parse_fail_count']} "
        f"mismatch={spine['field_mismatch_count']}"
    )
    return 0 if spine["spine_status"] in {SPINE_PASS, SPINE_PASS_WITH_META} else 2


def main() -> int:
    try:
        return generate()
    except GenerationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
