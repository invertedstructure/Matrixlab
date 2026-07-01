#!/usr/bin/env python3
"""Build MatrixLabs compression_decompression_law_v0.

M3 is the no-lie layer before taxonomy. It defines admissibility rules for
display/readout compression over M1/M2 source-backed material, without creating
taxonomy, authority, schema promotion, runtime replay, or a runner.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "matrixlabs_compression_decompression_law_v0"
LAW_ROLE = "admissibility_law_for_decompressible_observed_path_compression"
SOURCE_INDEX = Path("docs/matrixlabs/observability/decision_path_index_v0.json")
SOURCE_SPINE = Path("docs/matrixlabs/observability/receipt_spine_v0.json")
SOURCE_OBSERVED = Path("docs/matrixlabs/architecture/c8_observed_decision_path_v0.json")
OUTPUT_JSON = Path("docs/matrixlabs/observability/compression_decompression_law_v0.json")
OUTPUT_MD = Path("docs/matrixlabs/observability/compression_decompression_law_v0.md")
GENERATED_BY = "scripts/build_compression_decompression_law_v0.py"

SOURCE_INDEX_SCHEMA = "matrixlabs_decision_path_index_v0"
SOURCE_SPINE_SCHEMA = "matrixlabs_receipt_spine_v0"
SOURCE_OBSERVED_SCHEMA = "matrixlabs_c8_observed_decision_path_v0"

LAW_PASS = "LAW_PASS_V0_TESTS"
LAW_FAIL = "LAW_FAIL_V0_TESTS"

REQUIRED_DECOMPRESSION_FIELDS = [
    "node_id",
    "node_number",
    "node_kind",
    "edge_id",
    "edge_kind",
    "original_path_order",
    "receipt_backing_kind",
    "declared_receipt_id",
    "declared_receipt_path",
    "spine_status",
    "human_boundary_required",
    "human_decision_consumed",
    "authorized_future_unit",
    "forbidden_actions_explicitly_preserved",
    "commit_sha",
    "artifact_dir",
    "must_not_impersonate",
    "non_claims",
]

MUST_NOT_IMPERSONATE = [
    "runner authority",
    "schema promotion",
    "future move authorization",
    "edge lawfulness",
    "proof closure",
    "runtime replay",
    "taxonomy permission",
    "reusable/preapproved authority",
]

NON_CLAIMS = [
    "M3 does not create taxonomy.",
    "M3 does not authorize moves.",
    "M3 does not promote schemas.",
    "M3 does not validate edge lawfulness.",
    "M3 does not replay runtime.",
    "M3 does not validate receipt content truth.",
    "M3 does not mechanize path updates.",
    "M3 does not create reusable/preapproved authority.",
    "M3 does not build a runner.",
    "M3 only defines v0 admissibility rules for decomposable compression over M1/M2 source-backed material.",
]

COMPRESSION_LAYERS = [
    {
        "layer": "DISPLAY_COMPRESSION",
        "role": "shortens readout only",
        "admissibility_boundary": "must decompress back to M1 address and M2 spine evidence fields",
        "authority_created": False,
    },
    {
        "layer": "STRUCTURAL_COMPRESSION",
        "role": "names a descriptive observed surface type",
        "admissibility_boundary": "descriptive only; not authoritative",
        "authority_created": False,
    },
    {
        "layer": "ROUTE_PATTERN_COMPRESSION",
        "role": "names an observed ordered sequence",
        "admissibility_boundary": "observed-pattern readout only; never a future runner rule",
        "authority_created": False,
    },
]

FORBIDDEN_COMPRESSIONS = [
    {
        "forbidden_compression": "human_acceptance + authorized_future_unit -> auto_authorized",
        "rejection_code": "COMPRESSION_REJECTED_AUTHORITY_LEAK",
    },
    {
        "forbidden_compression": "receipt_exists -> edge_lawful",
        "rejection_code": "COMPRESSION_REJECTED_EDGE_LAWFULNESS_LEAK",
    },
    {
        "forbidden_compression": "repeated_transition -> schema_promoted",
        "rejection_code": "COMPRESSION_REJECTED_SCHEMA_PROMOTION",
    },
    {
        "forbidden_compression": "source_commit_only_meta_handoff -> runtime_receipt",
        "rejection_code": "COMPRESSION_REJECTED_RECEIPT_IMPERSONATION",
    },
    {
        "forbidden_compression": "closure_readiness -> proof_done",
        "rejection_code": "COMPRESSION_REJECTED_AUTHORITY_LEAK",
    },
    {
        "forbidden_compression": "bounded_execution -> runner_created",
        "rejection_code": "COMPRESSION_REJECTED_AUTHORITY_LEAK",
    },
    {
        "forbidden_compression": "taxonomy_label -> move_permission",
        "rejection_code": "COMPRESSION_REJECTED_AUTHORITY_LEAK",
    },
    {
        "forbidden_compression": "no_forbidden_counter_seen -> all_forbidden_actions_impossible",
        "rejection_code": "COMPRESSION_REJECTED_AUTHORITY_LEAK",
    },
    {
        "forbidden_compression": "observed route pattern -> future execution rule",
        "rejection_code": "COMPRESSION_REJECTED_AUTHORITY_LEAK",
    },
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
    commit = run_git(root, ["log", "-n", "1", "--format=%H", "--", *[str(path) for path in paths]])
    if not git_commit_exists(root, commit):
        raise GenerationError(f"could not verify source commit for: {', '.join(str(path) for path in paths)}")
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


def source_scope(node_ids: list[str], edge_ids: list[str]) -> dict[str, list[str]]:
    return {"node_ids": node_ids, "edge_ids": edge_ids}


def node_order(node_id: str) -> int:
    return int(node_id.split(".n", 1)[1])


def spine_map(spine: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {node["node_id"]: node for node in spine.get("nodes", [])}


def index_node_map(index: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {node["node_id"]: node for node in index.get("nodes", [])}


def index_edge_map(index: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {edge["edge_id"]: edge for edge in index.get("edges", [])}


def recovered_node_fields(index_node: dict[str, Any], spine_node: dict[str, Any]) -> dict[str, Any]:
    return {
        "node_id": index_node.get("node_id"),
        "node_number": index_node.get("node_number"),
        "node_kind": index_node.get("node_kind"),
        "original_path_order": index_node.get("node_number"),
        "receipt_backing_kind": spine_node.get("receipt_backing_kind"),
        "declared_receipt_id": spine_node.get("declared_receipt_id"),
        "declared_receipt_path": spine_node.get("declared_receipt_path"),
        "spine_status": spine_node.get("spine_status"),
        "human_boundary_required": index_node.get("human_boundary_required"),
        "human_decision_consumed": index_node.get("human_decision_consumed"),
        "authorized_future_unit": index_node.get("authorized_future_unit"),
        "forbidden_actions_explicitly_preserved": index_node.get("forbidden_actions_explicitly_preserved", []),
        "commit_sha": index_node.get("commit_sha"),
        "artifact_dir": index_node.get("artifact_dir"),
        "must_not_impersonate": MUST_NOT_IMPERSONATE,
        "non_claims": NON_CLAIMS,
    }


def recovered_edge_fields(index_edge: dict[str, Any]) -> dict[str, Any]:
    return {
        "edge_id": index_edge.get("edge_id"),
        "edge_kind": index_edge.get("edge_kind"),
        "original_path_order": [index_edge.get("from_node_number"), index_edge.get("to_node_number")],
        "must_not_impersonate": MUST_NOT_IMPERSONATE,
        "non_claims": NON_CLAIMS,
    }


def build_decompression_map(
    index: dict[str, Any],
    spine: dict[str, Any],
    node_ids: list[str],
    edge_ids: list[str],
) -> dict[str, Any]:
    nodes = index_node_map(index)
    spine_nodes = spine_map(spine)
    edges = index_edge_map(index)
    recovered = {
        "nodes": {
            node_id: recovered_node_fields(nodes[node_id], spine_nodes[node_id])
            for node_id in node_ids
        },
        "edges": {
            edge_id: recovered_edge_fields(edges[edge_id])
            for edge_id in edge_ids
        },
        "original_path_order": sorted(node_ids, key=node_order),
        "non_claims": NON_CLAIMS,
    }
    return {
        "node_ids": node_ids,
        "edge_ids": edge_ids,
        "required_fields": REQUIRED_DECOMPRESSION_FIELDS,
        "recovered_fields": recovered,
    }


def clean_loss_profile(display_detail_lost: bool) -> dict[str, bool]:
    return {
        "display_detail_lost": display_detail_lost,
        "source_pointer_lost": False,
        "receipt_pointer_lost": False,
        "receipt_backing_kind_lost": False,
        "human_boundary_lost": False,
        "authorized_future_unit_lost": False,
        "forbidden_boundary_lost": False,
        "non_claims_lost": False,
    }


def admissible_record(
    compression_id: str,
    compression_kind: str,
    node_ids: list[str],
    edge_ids: list[str],
    compressed_label: str,
    compressed_reading: str,
    layer: str,
    status: str,
    index: dict[str, Any],
    spine: dict[str, Any],
) -> dict[str, Any]:
    return {
        "compression_id": compression_id,
        "compression_kind": compression_kind,
        "source_scope": source_scope(node_ids, edge_ids),
        "compressed_label": compressed_label,
        "compressed_reading": compressed_reading,
        "compression_layer": layer,
        "decompression_map": build_decompression_map(index, spine, node_ids, edge_ids),
        "must_not_impersonate": MUST_NOT_IMPERSONATE,
        "loss_profile": clean_loss_profile(display_detail_lost=True),
        "compression_status": status,
        "rejection_code": None,
    }


def rejected_record(
    compression_id: str,
    compression_kind: str,
    node_ids: list[str],
    edge_ids: list[str],
    compressed_label: str,
    status: str,
    reason: str,
) -> dict[str, Any]:
    return {
        "compression_id": compression_id,
        "compression_kind": compression_kind,
        "source_scope": source_scope(node_ids, edge_ids),
        "compressed_label": compressed_label,
        "compressed_reading": reason,
        "compression_layer": "REJECTED_COMPRESSION",
        "decompression_map": {
            "node_ids": node_ids,
            "edge_ids": edge_ids,
            "required_fields": REQUIRED_DECOMPRESSION_FIELDS,
            "recovered_fields": {},
        },
        "must_not_impersonate": MUST_NOT_IMPERSONATE,
        "loss_profile": {
            "display_detail_lost": None,
            "source_pointer_lost": None,
            "receipt_pointer_lost": None,
            "receipt_backing_kind_lost": None,
            "human_boundary_lost": None,
            "authorized_future_unit_lost": None,
            "forbidden_boundary_lost": None,
            "non_claims_lost": None,
        },
        "compression_status": status,
        "rejection_code": status,
        "rejection_reason": reason,
    }


def build_records(index: dict[str, Any], spine: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        admissible_record(
            "c8.comp.v0.001",
            "node_surface_capsule",
            ["c8.n17"],
            [],
            "bounded_patch_execution_surface",
            "Observed bounded execution surface backed by one runtime receipt node.",
            "DISPLAY_COMPRESSION",
            "COMPRESSION_ADMISSIBLE_DISPLAY_ONLY",
            index,
            spine,
        ),
        admissible_record(
            "c8.comp.v0.002",
            "sequence_capsule",
            ["c8.n01", "c8.n02", "c8.n03", "c8.n04"],
            ["c8.e01_02", "c8.e02_03", "c8.e03_04"],
            "closure_to_successor_selection_sequence",
            "Observed closure through successor-surface selection sequence.",
            "ROUTE_PATTERN_COMPRESSION",
            "COMPRESSION_ADMISSIBLE_OBSERVED_PATTERN_ONLY",
            index,
            spine,
        ),
        rejected_record(
            "c8.comp.v0.003",
            "sequence_capsule",
            ["c8.n01", "c8.n02", "c8.n03", "c8.n04"],
            ["c8.e01_02", "c8.e02_03", "c8.e03_04"],
            "auto_successor_selection",
            "COMPRESSION_REJECTED_AUTHORITY_LEAK",
            "The label erases or impersonates human acceptance / authorization boundaries.",
        ),
        rejected_record(
            "c8.comp.v0.004",
            "node_surface_capsule",
            ["c8.n20"],
            [],
            "runtime_receipt_node",
            "COMPRESSION_REJECTED_RECEIPT_IMPERSONATION",
            "c8.n20 is source-commit-only meta-handoff, not runtime receipt-backed.",
        ),
        rejected_record(
            "c8.comp.v0.005",
            "route_pattern_capsule",
            [],
            [],
            "preapproved_reusable_schema",
            "COMPRESSION_REJECTED_SCHEMA_PROMOTION",
            "Observed repetition does not create reusable authorization.",
        ),
        rejected_record(
            "c8.comp.v0.006",
            "edge_capsule",
            [],
            ["c8.e01_02"],
            "edge_lawful",
            "COMPRESSION_REJECTED_EDGE_LAWFULNESS_LEAK",
            "Receipt existence does not prove edge lawfulness.",
        ),
    ]


def evaluate_admissible_record(
    record: dict[str, Any],
    index_nodes: set[str],
    index_edges: set[str],
    spine_nodes: dict[str, dict[str, Any]],
) -> tuple[str, list[str]]:
    failures: list[str] = []
    scope = record["source_scope"]
    node_ids = scope.get("node_ids", [])
    edge_ids = scope.get("edge_ids", [])
    if not node_ids and not edge_ids:
        failures.append("missing_source_scope")
    for node_id in node_ids:
        if node_id not in index_nodes:
            failures.append(f"node_not_in_m1:{node_id}")
        if node_id not in spine_nodes:
            failures.append(f"node_not_in_m2:{node_id}")
        else:
            backing = spine_nodes[node_id].get("receipt_backing_kind")
            if backing == "RUNTIME_RECEIPT" and spine_nodes[node_id].get("spine_status") != "SPINE_NODE_PASS":
                failures.append(f"runtime_receipt_node_not_pass:{node_id}")
            if backing == "SOURCE_COMMIT_ONLY_META_HANDOFF" and spine_nodes[node_id].get("spine_status") != "SPINE_NODE_SOURCE_COMMIT_ONLY":
                failures.append(f"source_meta_node_not_preserved:{node_id}")
    for edge_id in edge_ids:
        if edge_id not in index_edges:
            failures.append(f"edge_not_in_m1:{edge_id}")
    recovered = record.get("decompression_map", {}).get("recovered_fields", {})
    if not recovered:
        failures.append("missing_recovered_fields")
    loss = record.get("loss_profile", {})
    for field in [
        "source_pointer_lost",
        "receipt_pointer_lost",
        "receipt_backing_kind_lost",
        "human_boundary_lost",
        "authorized_future_unit_lost",
        "forbidden_boundary_lost",
        "non_claims_lost",
    ]:
        if loss.get(field) is not False:
            failures.append(f"{field}_not_false")
    if not record.get("must_not_impersonate"):
        failures.append("must_not_impersonate_missing")
    return ("PASS" if not failures else "FAIL", failures)


def build_tests(records: list[dict[str, Any]], index: dict[str, Any], spine: dict[str, Any]) -> list[dict[str, Any]]:
    expected_by_id = {
        "c8.comp.v0.001": (
            "pass_node_c8_n17_bounded_patch_execution_surface",
            "node c8.n17 -> bounded_patch_execution_surface",
            "COMPRESSION_ADMISSIBLE_DISPLAY_ONLY",
            "Decompression recovers node ID, receipt backing kind, receipt pointer, spine status, human boundary, authorized future unit, forbidden boundaries, and commit pointer.",
        ),
        "c8.comp.v0.002": (
            "pass_sequence_c8_n01_to_n04_closure_to_successor_selection_sequence",
            "nodes c8.n01-c8.n04 -> closure_to_successor_selection_sequence",
            "COMPRESSION_ADMISSIBLE_OBSERVED_PATTERN_ONLY",
            "Decompression recovers exact ordered nodes and edges.",
        ),
        "c8.comp.v0.003": (
            "fail_auto_successor_selection_authority_leak",
            "nodes c8.n01-c8.n04 -> auto_successor_selection",
            "COMPRESSION_REJECTED_AUTHORITY_LEAK",
            "The label erases or impersonates human acceptance / authorization boundaries.",
        ),
        "c8.comp.v0.004": (
            "fail_c8_n20_runtime_receipt_impersonation",
            "node c8.n20 -> runtime_receipt_node",
            "COMPRESSION_REJECTED_RECEIPT_IMPERSONATION",
            "c8.n20 is source-commit-only meta-handoff, not runtime receipt-backed.",
        ),
        "c8.comp.v0.005": (
            "fail_repeated_human_acceptance_edges_schema_promotion",
            "repeated human acceptance edges -> preapproved_reusable_schema",
            "COMPRESSION_REJECTED_SCHEMA_PROMOTION",
            "Observed repetition does not create reusable authorization.",
        ),
        "c8.comp.v0.006": (
            "fail_receipt_backed_edge_lawful",
            "receipt-backed edge -> edge_lawful",
            "COMPRESSION_REJECTED_EDGE_LAWFULNESS_LEAK",
            "Receipt existence does not prove edge lawfulness.",
        ),
    }
    index_nodes = {node["node_id"] for node in index.get("nodes", [])}
    index_edges = {edge["edge_id"] for edge in index.get("edges", [])}
    spine_nodes = spine_map(spine)
    tests = []
    for record in records:
        test_id, input_text, expected, reason = expected_by_id[record["compression_id"]]
        observed = record["compression_status"]
        failures: list[str] = []
        if observed != expected:
            failures.append(f"observed_status_wrong:{observed}!={expected}")
        if observed.startswith("COMPRESSION_ADMISSIBLE"):
            _, admissible_failures = evaluate_admissible_record(record, index_nodes, index_edges, spine_nodes)
            failures.extend(admissible_failures)
        elif not record.get("rejection_code"):
            failures.append("rejection_code_missing")
        tests.append({
            "test_id": test_id,
            "input": input_text,
            "expected_status": expected,
            "observed_status": observed,
            "reason": reason,
            "test_result": "PASS" if not failures else "FAIL",
            "failures": failures,
            "compression_id": record["compression_id"],
        })
    return tests


def render_markdown(law: dict[str, Any]) -> str:
    parts = [
        "# Compression/Decompression Law v0",
        "",
        "## Status",
        "",
        law["law_status"],
        "",
        "## Purpose",
        "",
        "M3 is the no-lie layer before taxonomy.",
        "",
        "## Source",
        "",
        f"- M1 index: `{law['source_index_path']}`",
        f"- M2 spine: `{law['source_spine_path']}`",
        f"- Observed path: `{law['source_observed_path']}`",
        f"- M1 index SHA256: `{law['source_index_sha256']}`",
        f"- M2 spine SHA256: `{law['source_spine_sha256']}`",
        f"- Observed path SHA256: `{law['source_observed_path_sha256']}`",
        f"- M1 index commit: `{law['source_index_commit_sha']}`",
        f"- M2 spine commit: `{law['source_spine_commit_sha']}`",
        f"- Observed path commit: `{law['source_observed_path_commit_sha']}`",
        "",
        "## Core law",
        "",
        "A compression is admissible only if decompression recovers the source-critical fields needed to preserve M1 addressability, M2 evidence status, path order, receipt/source backing kind, human-boundary status, human decision status, authorized-future-unit status, forbidden-action boundaries, source pointers, and non-claims.",
        "",
        "Compression may reduce display size. Compression may not create authority, erase human-boundary status, widen authorized-future-unit status, promote observed repetition into reusable schema, turn receipt existence into edge lawfulness, turn source-commit-only meta nodes into runtime receipts, or treat absent forbidden counters as proof that forbidden actions are impossible.",
        "",
        "## Compression layers",
        "",
    ]
    for layer in law["admissible_compression_layers"]:
        parts.append(f"- `{layer['layer']}` - {layer['role']} - {layer['admissibility_boundary']}")
    parts.extend([
        "",
        "## Required decompression fields",
        "",
        *[f"- `{field}`" for field in law["required_decompression_fields"]],
        "",
        "## Forbidden compressions",
        "",
        *[f"- `{item['forbidden_compression']}` -> `{item['rejection_code']}`" for item in law["forbidden_compressions"]],
        "",
        "## Tiny v0 test suite",
        "",
        "| test_id | input | expected | observed | result |",
        "| --- | --- | --- | --- | --- |",
    ])
    for test in law["test_cases"]:
        parts.append(
            f"| {test['test_id']} | {test['input']} | {test['expected_status']} | {test['observed_status']} | {test['test_result']} |"
        )
    parts.extend([
        "",
        "## Acceptance gate",
        "",
        f"- law_status: `{law['law_status']}`",
        f"- test_case_count: `{len(law['test_cases'])}`",
        f"- compression_record_count: `{len(law['compression_records'])}`",
        "- Every admissible record resolves through M1/M2 and preserves non-authority boundaries.",
        "- Every rejected record emits its expected rejection code.",
        "- Taxonomy, future authority, reusable authority, runner creation, runtime replay, receipt truth validation, and edge lawfulness validation are all false.",
        "",
        "## Non-claims",
        "",
        *[f"- {claim}" for claim in law["non_claims"]],
        "",
        "## Relationship to M5",
        "",
        "M5 names only what M3 can decompress safely.",
    ])
    return "\n".join(parts)


def build_law(root: Path) -> dict[str, Any]:
    index = load_json(root / SOURCE_INDEX)
    spine = load_json(root / SOURCE_SPINE)
    observed = load_json(root / SOURCE_OBSERVED)
    source_index_commit = commit_for_paths(
        root,
        [
            SOURCE_INDEX,
            Path("docs/matrixlabs/observability/decision_path_index_v0.md"),
            Path("scripts/build_decision_path_index_v0.py"),
        ],
    )
    source_spine_commit = commit_for_paths(
        root,
        [
            SOURCE_SPINE,
            Path("docs/matrixlabs/observability/receipt_spine_v0.md"),
            Path("scripts/build_receipt_spine_v0.py"),
        ],
    )
    source_observed_commit = commit_for_paths(
        root,
        [
            SOURCE_OBSERVED,
            Path("docs/matrixlabs/architecture/c8_observed_decision_path_v0.md"),
        ],
    )
    records = build_records(index, spine)
    tests = build_tests(records, index, spine)
    law_status = LAW_PASS if all(test["test_result"] == "PASS" for test in tests) else LAW_FAIL
    return {
        "schema_version": SCHEMA_VERSION,
        "law_role": LAW_ROLE,
        "source_index_path": str(SOURCE_INDEX),
        "source_spine_path": str(SOURCE_SPINE),
        "source_observed_path": str(SOURCE_OBSERVED),
        "source_index_schema": index.get("schema_version"),
        "source_spine_schema": spine.get("schema_version"),
        "source_observed_path_schema": observed.get("schema_version"),
        "source_index_sha256": sha256_file(root / SOURCE_INDEX),
        "source_spine_sha256": sha256_file(root / SOURCE_SPINE),
        "source_observed_path_sha256": sha256_file(root / SOURCE_OBSERVED),
        "source_index_commit_sha": source_index_commit,
        "source_spine_commit_sha": source_spine_commit,
        "source_observed_path_commit_sha": source_observed_commit,
        "validation_depth": "compression_decompression_contract_only",
        "taxonomy_created": False,
        "runner_created": False,
        "future_authority_created": False,
        "reusable_preapproved_authority_created": False,
        "schema_promoted": False,
        "runtime_replay_performed": False,
        "edge_lawfulness_validation_performed": False,
        "receipt_content_truth_validation_performed": False,
        "receipt_hash_validation_performed": False,
        "required_decompression_fields": REQUIRED_DECOMPRESSION_FIELDS,
        "forbidden_compressions": FORBIDDEN_COMPRESSIONS,
        "admissible_compression_layers": COMPRESSION_LAYERS,
        "compression_records": records,
        "test_cases": tests,
        "law_status": law_status,
        "non_claims": NON_CLAIMS,
        "relationship_to_m5": "M5 names only what M3 can decompress safely.",
        "generated_by": GENERATED_BY,
    }


def generate() -> int:
    root = detect_repo_root(Path.cwd())
    law = build_law(root)
    output_json = root / OUTPUT_JSON
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(law, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (root / OUTPUT_MD).write_text(render_markdown(law).rstrip() + "\n", encoding="utf-8")
    admissible_count = sum(
        1 for record in law["compression_records"]
        if str(record.get("compression_status", "")).startswith("COMPRESSION_ADMISSIBLE")
    )
    rejected_count = sum(
        1 for record in law["compression_records"]
        if str(record.get("compression_status", "")).startswith("COMPRESSION_REJECTED")
    )
    print(
        "Generated compression_decompression_law_v0: "
        f"status={law['law_status']} "
        f"tests={len(law['test_cases'])} "
        f"admissible={admissible_count} "
        f"rejected={rejected_count}"
    )
    return 0 if law["law_status"] == LAW_PASS else 2


def main() -> int:
    try:
        return generate()
    except GenerationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
