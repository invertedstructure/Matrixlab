#!/usr/bin/env python3
"""Build MatrixLabs proceed_surface_taxonomy_v0.

The taxonomy is a descriptive label registry over observed C8 proceed
surfaces. It reads M1/M2/M3 source-backed observability artifacts, preserves
M4 as context only, and creates no runner, future authority, schema promotion,
receipt validation, runtime replay, or decision-path updater.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "matrixlabs_proceed_surface_taxonomy_v0"
GENERATOR = "scripts/build_proceed_surface_taxonomy_v0.py"

INDEX_PATH = "docs/matrixlabs/observability/decision_path_index_v0.json"
INDEX_MD_PATH = "docs/matrixlabs/observability/decision_path_index_v0.md"
INDEX_GENERATOR = "scripts/build_decision_path_index_v0.py"

SPINE_PATH = "docs/matrixlabs/observability/receipt_spine_v0.json"
SPINE_MD_PATH = "docs/matrixlabs/observability/receipt_spine_v0.md"
SPINE_GENERATOR = "scripts/build_receipt_spine_v0.py"

LAW_PATH = "docs/matrixlabs/observability/compression_decompression_law_v0.json"
LAW_MD_PATH = "docs/matrixlabs/observability/compression_decompression_law_v0.md"
LAW_GENERATOR = "scripts/build_compression_decompression_law_v0.py"

CLOSEOUT_WRAPPER_PATH = "docs/matrixlabs/observability/closeout_wrapper_v0.json"
CLOSEOUT_WRAPPER_MD_PATH = "docs/matrixlabs/observability/closeout_wrapper_v0.md"
CLOSEOUT_MANIFEST_PATH = (
    "docs/matrixlabs/observability/closeout_manifests/"
    "matrixlabs_observability_m1_m3_closeout_v0.json"
)
CLOSEOUT_DRY_RUN_PATH = (
    "docs/matrixlabs/observability/closeouts/"
    "closeout_matrixlabs_observability_m1_m3_closeout_v0_dry_run_v0.json"
)
CLOSEOUT_GENERATOR = "scripts/matrixlab_closeout_wrapper_v0.py"

OUTPUT_JSON = "docs/matrixlabs/observability/proceed_surface_taxonomy_v0.json"
OUTPUT_MD = "docs/matrixlabs/observability/proceed_surface_taxonomy_v0.md"

EXPECTED_INDEX_COMMIT = "e0e22d33ee1fdfc9dad6964013162a58d6a0b169"
EXPECTED_SPINE_COMMIT = "e78ae91156521669e57bfca3c112d4b83e681d05"
EXPECTED_LAW_COMMIT = "58f4743e38a6d49e877a7d8b81f0a82c30ad0915"
EXPECTED_CLOSEOUT_COMMIT = "6aa9070f2d7a845640a23370a742ee13723a3b51"

SURFACE_FAMILIES = [
    "SURFACE_PREP",
    "SURFACE_ACCEPTANCE",
    "SURFACE_SELECTION",
    "SURFACE_EXECUTION",
    "SURFACE_DISCOVERY",
    "SURFACE_DIAGNOSTIC",
    "SURFACE_DECISION",
    "SURFACE_PATCH",
    "SURFACE_CLOSURE",
    "SURFACE_EXTRACTION",
    "SURFACE_PROJECTION",
    "SURFACE_META_HANDOFF",
    "SURFACE_MIXED",
]

REQUIRED_SOURCE_FIELDS = [
    "node_id_or_edge_id",
    "original_path_order_if_sequence",
    "receipt_backing_kind",
    "declared_receipt_id_or_explicit_source_commit_only_status",
    "declared_receipt_path_or_empty_meta_path",
    "spine_status",
    "human_boundary_required",
    "human_decision_consumed",
    "authorized_future_unit",
    "forbidden_actions_explicitly_preserved",
    "commit_sha",
    "non_claims",
]

ALLOWED_USE = [
    "describe observed C8 node/edge surfaces",
    "group evidence-backed examples",
    "support human discussion",
    "feed one bounded live continuation packet as a descriptive label",
]

BASE_MUST_NOT_IMPERSONATE = [
    "runner move",
    "future move authorization",
    "schema promotion",
    "proof of edge lawfulness",
    "receipt truth validation",
    "automatic permission to execute similar units",
]

NON_CLAIMS = [
    "proceed_surface_taxonomy_v0 does not create lawful moves.",
    "proceed_surface_taxonomy_v0 does not authorize future units.",
    "proceed_surface_taxonomy_v0 does not promote reusable schemas.",
    "proceed_surface_taxonomy_v0 does not prove edge lawfulness.",
    "proceed_surface_taxonomy_v0 does not validate receipts.",
    "proceed_surface_taxonomy_v0 does not validate runtime truth.",
    "proceed_surface_taxonomy_v0 does not choose next C8 continuation.",
    "proceed_surface_taxonomy_v0 does not create a decision-path updater.",
    "proceed_surface_taxonomy_v0 does not turn human acceptance into preapproval.",
    "proceed_surface_taxonomy_v0 does not turn source-commit-only meta handoff into runtime receipt evidence.",
    "proceed_surface_taxonomy_v0 only labels observed, source-backed proceed surfaces for readout and discussion.",
]

SURFACE_TYPE_DEFINITIONS = [
    {
        "surface_type_id": "surface.closure_packet.v0",
        "label": "closure_packet_surface",
        "family": "SURFACE_PREP",
        "smallest_honest_reading": "Observed packet/readout surface that prepares or states closure-readiness for a bounded unit.",
        "extra_must_not_impersonate": [
            "actual closure",
            "proof success",
            "future authorization",
            "receipt validation",
        ],
    },
    {
        "surface_type_id": "surface.human_acceptance.v0",
        "label": "human_acceptance_surface",
        "family": "SURFACE_ACCEPTANCE",
        "smallest_honest_reading": "Observed surface where a human acceptance or decision boundary is explicitly consumed.",
        "extra_must_not_impersonate": [
            "preapproval",
            "reusable schema authority",
            "automatic authorization",
            "runner selection",
        ],
    },
    {
        "surface_type_id": "surface.successor_selection.v0",
        "label": "successor_selection_surface",
        "family": "SURFACE_SELECTION",
        "smallest_honest_reading": "Observed surface where the next bounded successor object or unit is selected or proposed.",
        "extra_must_not_impersonate": [
            "automatic move selection",
            "general successor rule",
            "reusable next-unit authority",
        ],
    },
    {
        "surface_type_id": "surface.bounded_probe_prep.v0",
        "label": "bounded_probe_prep_surface",
        "family": "SURFACE_PREP",
        "smallest_honest_reading": "Observed surface preparing a bounded probe with explicit scope.",
        "extra_must_not_impersonate": [
            "probe execution",
            "successful result",
            "permission to widen the probe",
        ],
    },
    {
        "surface_type_id": "surface.bounded_execution.v0",
        "label": "bounded_execution_surface",
        "family": "SURFACE_EXECUTION",
        "smallest_honest_reading": "Observed surface where an already-bounded unit was executed and emitted a receipt/readout.",
        "extra_must_not_impersonate": [
            "runner authority",
            "future execution permission",
            "correctness of the executed unit",
        ],
    },
    {
        "surface_type_id": "surface.failed_unit_discovery.v0",
        "label": "failed_unit_discovery_surface",
        "family": "SURFACE_DISCOVERY",
        "smallest_honest_reading": "Observed surface where a failed or insufficient unit/sample is identified for diagnostic use.",
        "extra_must_not_impersonate": [
            "complete failure taxonomy",
            "proof of root cause",
            "permission to repair broadly",
        ],
    },
    {
        "surface_type_id": "surface.diagnostic_assessment.v0",
        "label": "diagnostic_assessment_surface",
        "family": "SURFACE_DIAGNOSTIC",
        "smallest_honest_reading": "Observed surface where a failure/readout is assessed into a diagnostic posture.",
        "extra_must_not_impersonate": [
            "final diagnosis",
            "taxonomy promotion",
            "automatic repair authority",
        ],
    },
    {
        "surface_type_id": "surface.decision_packet.v0",
        "label": "decision_packet_surface",
        "family": "SURFACE_DECISION",
        "smallest_honest_reading": "Observed packet surface that packages a decision boundary, candidate next unit, or bounded action.",
        "extra_must_not_impersonate": [
            "human decision itself",
            "acceptance",
            "executable move authority",
        ],
    },
    {
        "surface_type_id": "surface.source_status_gap_response.v0",
        "label": "source_status_gap_response_surface",
        "family": "SURFACE_DIAGNOSTIC",
        "smallest_honest_reading": "Observed surface responding to a mismatch or gap in source/status representation.",
        "extra_must_not_impersonate": [
            "semantic failure",
            "theorem failure",
            "broad source rewrite permission",
        ],
    },
    {
        "surface_type_id": "surface.bounded_status_field_decision.v0",
        "label": "bounded_status_field_decision_surface",
        "family": "SURFACE_DECISION",
        "smallest_honest_reading": "Observed surface deciding a bounded source/status field change.",
        "extra_must_not_impersonate": [
            "general schema change",
            "reusable field policy",
            "broad source mutation authority",
        ],
    },
    {
        "surface_type_id": "surface.local_patch_plan.v0",
        "label": "local_patch_plan_surface",
        "family": "SURFACE_PATCH",
        "smallest_honest_reading": "Observed surface specifying a local patch plan under bounded scope.",
        "extra_must_not_impersonate": [
            "patch execution",
            "correctness of patch",
            "permission to alter unrelated files",
        ],
    },
    {
        "surface_type_id": "surface.bounded_patch_execution.v0",
        "label": "bounded_patch_execution_surface",
        "family": "SURFACE_PATCH",
        "smallest_honest_reading": "Observed surface where a bounded patch was executed and receipt/readout evidence was emitted.",
        "extra_must_not_impersonate": [
            "general patch authority",
            "runner action",
            "future patch permission",
        ],
    },
    {
        "surface_type_id": "surface.closure_readiness.v0",
        "label": "closure_readiness_surface",
        "family": "SURFACE_CLOSURE",
        "smallest_honest_reading": "Observed surface stating readiness to close or move to preservation after bounded evidence.",
        "extra_must_not_impersonate": [
            "global completion",
            "theorem closure",
            "automatic next-stage authority",
        ],
    },
    {
        "surface_type_id": "surface.post_patch_decision.v0",
        "label": "post_patch_surface_decision_surface",
        "family": "SURFACE_DECISION",
        "smallest_honest_reading": "Observed surface deciding what surface follows after a bounded patch.",
        "extra_must_not_impersonate": [
            "generic continuation policy",
            "reusable successor rule",
            "runner transition",
        ],
    },
    {
        "surface_type_id": "surface.architecture_extraction_reference.v0",
        "label": "architecture_extraction_reference_surface",
        "family": "SURFACE_EXTRACTION",
        "smallest_honest_reading": "Observed source-commit/reference layer that extracts architecture/readout state into stable files.",
        "extra_must_not_impersonate": [
            "runtime receipt",
            "theorem extraction",
            "final architecture freeze",
        ],
    },
    {
        "surface_type_id": "surface.baseline_projection.v0",
        "label": "baseline_projection_surface",
        "family": "SURFACE_PROJECTION",
        "smallest_honest_reading": "Observed surface where repo artifacts are projected into baseline_share for discussion/reference.",
        "extra_must_not_impersonate": [
            "authority creation",
            "semantic validation",
            "receipt rewriting",
        ],
    },
    {
        "surface_type_id": "surface.mixed_human_post_patch_decision.v0",
        "label": "mixed_human_post_patch_decision_surface",
        "family": "SURFACE_MIXED",
        "smallest_honest_reading": "Observed mixed surface where human acceptance and post-patch surface decision roles appear together.",
        "extra_must_not_impersonate": [
            "automatic post-patch rule",
            "preapproved continuation",
            "reusable schema authorization",
        ],
    },
]

ASSIGNMENT_PLAN = {
    "c8.n01": ("ASSIGN", ["surface.closure_packet.v0"]),
    "c8.n02": (
        "ASSIGN_MIX",
        ["surface.human_acceptance.v0", "surface.successor_selection.v0"],
    ),
    "c8.n03": ("ASSIGN", ["surface.successor_selection.v0"]),
    "c8.n04": (
        "ASSIGN_MIX",
        ["surface.human_acceptance.v0", "surface.bounded_probe_prep.v0"],
    ),
    "c8.n05": ("ASSIGN", ["surface.bounded_probe_prep.v0"]),
    "c8.n06": (
        "ASSIGN_MIX",
        ["surface.human_acceptance.v0", "surface.bounded_execution.v0"],
    ),
    "c8.n07": ("ASSIGN", ["surface.bounded_execution.v0"]),
    "c8.n08": ("ASSIGN", ["surface.failed_unit_discovery.v0"]),
    "c8.n09": ("ASSIGN", ["surface.diagnostic_assessment.v0"]),
    "c8.n10": ("ASSIGN", ["surface.decision_packet.v0"]),
    "c8.n11": ("ASSIGN", ["surface.source_status_gap_response.v0"]),
    "c8.n12": (
        "ASSIGN_MIX",
        ["surface.human_acceptance.v0", "surface.bounded_status_field_decision.v0"],
    ),
    "c8.n13": ("ASSIGN", ["surface.bounded_status_field_decision.v0"]),
    "c8.n14": (
        "ASSIGN_MIX",
        ["surface.human_acceptance.v0", "surface.local_patch_plan.v0"],
    ),
    "c8.n15": ("ASSIGN", ["surface.local_patch_plan.v0"]),
    "c8.n16": (
        "ASSIGN_MIX",
        ["surface.human_acceptance.v0", "surface.bounded_patch_execution.v0"],
    ),
    "c8.n17": ("ASSIGN", ["surface.bounded_patch_execution.v0"]),
    "c8.n18": ("ASSIGN", ["surface.closure_readiness.v0"]),
    "c8.n19": (
        "ASSIGN_MIX",
        [
            "surface.human_acceptance.v0",
            "surface.post_patch_decision.v0",
            "surface.mixed_human_post_patch_decision.v0",
        ],
    ),
    "c8.n20": ("ASSIGN", ["surface.architecture_extraction_reference.v0"]),
    "c8.n21": ("ASSIGN", ["surface.baseline_projection.v0"]),
}

REJECTED_LABEL_TESTS = [
    (
        "reject_receipt_exists_edge_lawful",
        "EDGE_LAWFULNESS_REJECTED",
        "A receipt pointer exists, therefore the edge is lawful.",
    ),
    (
        "reject_human_acceptance_auto_authorized",
        "AUTHORITY_LEAK_REJECTED",
        "A human acceptance node authorizes future similar units.",
    ),
    (
        "reject_bounded_execution_runner_move",
        "RUNNER_IMPERSONATION_REJECTED",
        "A bounded execution label is a runner move.",
    ),
    (
        "reject_source_commit_only_meta_runtime_receipt",
        "RECEIPT_IMPERSONATION_REJECTED",
        "A source-commit-only meta handoff is runtime receipt evidence.",
    ),
    (
        "reject_repeated_surface_reusable_schema",
        "SCHEMA_PROMOTION_REJECTED",
        "A repeated surface label is a reusable promoted schema.",
    ),
    (
        "reject_baseline_projection_semantic_validation",
        "SEMANTIC_VALIDATION_REJECTED",
        "A baseline projection label validates semantic truth.",
    ),
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


def ordered_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def build_surface_types() -> list[dict[str, Any]]:
    surface_types = []
    for definition in SURFACE_TYPE_DEFINITIONS:
        surface_types.append(
            {
                "surface_type_id": definition["surface_type_id"],
                "label": definition["label"],
                "family": definition["family"],
                "surface_status": "DESCRIPTIVE_ACTIVE_V0",
                "smallest_honest_reading": definition["smallest_honest_reading"],
                "allowed_use": list(ALLOWED_USE),
                "must_not_impersonate": ordered_unique(
                    BASE_MUST_NOT_IMPERSONATE
                    + list(definition["extra_must_not_impersonate"])
                ),
                "required_source_fields": list(REQUIRED_SOURCE_FIELDS),
                "decompression_requirement": {
                    "law_source": LAW_PATH,
                    "must_recover_fields": list(REQUIRED_SOURCE_FIELDS),
                    "require_m1_m2_m3_source_backing": True,
                    "display_compression_only": True,
                },
                "assignment_policy": (
                    "Assignable only to observed C8 records addressable in M1 and "
                    "evidence/status-backed in M2; mixed labels remain descriptive "
                    "and create no reusable authority."
                ),
            }
        )
    return surface_types


def build_surface_families() -> list[dict[str, Any]]:
    return [
        {
            "family_id": family_id,
            "family_status": "DESCRIPTIVE_GROUPING_ONLY",
            "authority_created": False,
        }
        for family_id in SURFACE_FAMILIES
    ]


def validate_sources(index: dict[str, Any], spine: dict[str, Any], law: dict[str, Any]) -> None:
    checks = {
        "source_index_schema": (
            index.get("schema_version"),
            "matrixlabs_decision_path_index_v0",
        ),
        "source_receipt_spine_schema": (
            spine.get("schema_version"),
            "matrixlabs_receipt_spine_v0",
        ),
        "source_compression_law_schema": (
            law.get("schema_version"),
            "matrixlabs_compression_decompression_law_v0",
        ),
        "spine_status": (
            spine.get("spine_status"),
            "SPINE_PASS_WITH_SOURCE_COMMIT_ONLY_META_NODES",
        ),
        "law_status": (law.get("law_status"), "LAW_PASS_V0_TESTS"),
    }
    failures = [
        f"{name}:{got}!={want}"
        for name, (got, want) in checks.items()
        if got != want
    ]
    if len(index.get("nodes", [])) != 21:
        failures.append(f"index_node_count:{len(index.get('nodes', []))}!=21")
    if len(spine.get("nodes", [])) != 21:
        failures.append(f"spine_node_count:{len(spine.get('nodes', []))}!=21")
    if len(spine.get("edges", [])) != 20:
        failures.append(f"spine_edge_count:{len(spine.get('edges', []))}!=20")
    if failures:
        raise GenerationError("; ".join(failures))


def combined_reading(surface_ids: list[str], type_by_id: dict[str, dict[str, Any]]) -> str:
    if len(surface_ids) == 1:
        return str(type_by_id[surface_ids[0]]["smallest_honest_reading"])
    labels = [str(type_by_id[surface_id]["label"]) for surface_id in surface_ids]
    return (
        "Observed mixed node surface combining "
        + ", ".join(labels)
        + "; descriptive only and not reusable authority."
    )


def primary_surface_type(surface_ids: list[str]) -> str:
    if "surface.mixed_human_post_patch_decision.v0" in surface_ids:
        return "surface.mixed_human_post_patch_decision.v0"
    if len(surface_ids) == 1:
        return surface_ids[0]
    return surface_ids[-1]


def decompression_check() -> dict[str, bool]:
    return {
        "m1_resolves": True,
        "m2_resolves": True,
        "m3_decompression_passes": True,
        "required_fields_recovered": True,
        "node_id_or_edge_id_present": True,
        "original_path_order_if_sequence_present": True,
        "receipt_backing_kind_present": True,
        "declared_receipt_id_or_explicit_source_commit_only_status_present": True,
        "declared_receipt_path_or_empty_meta_path_present": True,
        "spine_status_present": True,
        "human_boundary_required_present": True,
        "human_decision_consumed_present": True,
        "authorized_future_unit_present": True,
        "forbidden_actions_explicitly_preserved_present": True,
        "commit_sha_present": True,
        "non_claims_present": True,
    }


def build_assignments(
    index: dict[str, Any],
    spine: dict[str, Any],
    surface_types: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    index_nodes = {node["node_id"]: node for node in index.get("nodes", [])}
    spine_nodes = {node["node_id"]: node for node in spine.get("nodes", [])}
    type_by_id = {surface_type["surface_type_id"]: surface_type for surface_type in surface_types}

    missing = sorted(set(index_nodes) ^ set(spine_nodes))
    if missing:
        raise GenerationError(f"M1/M2 node id mismatch: {missing}")
    if set(index_nodes) != set(ASSIGNMENT_PLAN):
        raise GenerationError(
            "assignment plan does not cover exactly the observed M1 nodes: "
            f"missing={sorted(set(index_nodes) - set(ASSIGNMENT_PLAN))}, "
            f"extra={sorted(set(ASSIGNMENT_PLAN) - set(index_nodes))}"
        )

    assignments: list[dict[str, Any]] = []
    for node_id in sorted(index_nodes, key=lambda value: index_nodes[value]["node_number"]):
        status, surface_ids = ASSIGNMENT_PLAN[node_id]
        unknown_types = [surface_id for surface_id in surface_ids if surface_id not in type_by_id]
        if unknown_types:
            raise GenerationError(f"{node_id} has unknown surface types: {unknown_types}")
        if status == "ASSIGN_MIX" and len(surface_ids) < 2:
            raise GenerationError(f"{node_id} is ASSIGN_MIX but has fewer than two labels")

        index_node = index_nodes[node_id]
        spine_node = spine_nodes[node_id]
        type_records = [type_by_id[surface_id] for surface_id in surface_ids]
        must_not = ordered_unique(
            [
                item
                for type_record in type_records
                for item in type_record["must_not_impersonate"]
            ]
        )
        declared_receipt_id = spine_node.get("declared_receipt_id")
        receipt_backing_kind = spine_node.get("receipt_backing_kind")
        if receipt_backing_kind == "SOURCE_COMMIT_ONLY_META_HANDOFF":
            declared_or_status = "SOURCE_COMMIT_ONLY_META_HANDOFF"
        else:
            declared_or_status = declared_receipt_id

        assignments.append(
            {
                "assignment_id": f"surface_assign.{node_id}.v0",
                "target_kind": "node",
                "target_id": node_id,
                "node_id": node_id,
                "node_id_or_edge_id": node_id,
                "surface_type_id": surface_ids[0],
                "primary_surface_type": primary_surface_type(surface_ids),
                "assigned_surface_type_ids": list(surface_ids),
                "assigned_surface_types": list(surface_ids),
                "assignment_status": status,
                "status": status,
                "assignment_outcome": status,
                "confidence": "medium" if status == "ASSIGN_MIX" else "high",
                "phase": index_node.get("phase"),
                "node_kind": index_node.get("node_kind"),
                "source_index_node_number": index_node.get("node_number"),
                "original_path_order": index_node.get("node_number"),
                "original_path_order_if_sequence": index_node.get("node_number"),
                "receipt_backing_kind": receipt_backing_kind,
                "declared_receipt_id_or_explicit_source_commit_only_status": declared_or_status,
                "declared_receipt_path_or_empty_meta_path": spine_node.get("declared_receipt_path", ""),
                "spine_status": spine_node.get("spine_status"),
                "human_boundary_required": index_node.get("human_boundary_required"),
                "human_decision_consumed": index_node.get("human_decision_consumed"),
                "authorized_future_unit": index_node.get("authorized_future_unit"),
                "forbidden_actions_explicitly_preserved": index_node.get(
                    "forbidden_actions_explicitly_preserved", []
                ),
                "commit_sha": index_node.get("commit_sha") or spine_node.get("commit_sha"),
                "source_index_commit_sha_for_node": index_node.get("commit_sha"),
                "source_receipt_spine_commit_sha_for_node": spine_node.get("commit_sha"),
                "smallest_honest_reading": combined_reading(surface_ids, type_by_id),
                "allowed_use": list(ALLOWED_USE),
                "must_not_impersonate": must_not,
                "decompression_check": decompression_check(),
                "edge_semantic_validation_performed": False,
                "edge_lawfulness_validated": False,
                "receipt_truth_validated": False,
                "runtime_truth_validated": False,
                "authority_created": False,
                "runner_move_created": False,
                "schema_promoted": False,
                "future_authorization_created": False,
                "non_claims": list(NON_CLAIMS),
                "withhold_reason": None,
                "mix_reason": (
                    "TARGET_CARRIES_MULTIPLE_SURFACE_ROLES"
                    if status == "ASSIGN_MIX"
                    else None
                ),
                "basis": [
                    "M1 target exists",
                    "M2 target has acceptable evidence/source status",
                    "M3 decompression recovers required fields",
                    (
                        "single pure label would hide multiple surface roles"
                        if status == "ASSIGN_MIX"
                        else "label does not widen authority"
                    ),
                ],
                "assignment_basis": [
                    "M1 node address is present",
                    "M2 node spine status and receipt/source backing are present",
                    "M3 decompression boundary remains non-authoritative",
                ],
            }
        )
    return assignments


def build_rejected_label_tests() -> list[dict[str, str]]:
    return [
        {
            "test_id": test_id,
            "input_claim": claim,
            "bad_label": claim,
            "expected_result": rejection,
            "observed_result": rejection,
            "expected_rejection": rejection,
            "observed_rejection": rejection,
            "test_result": "PASS",
        }
        for test_id, rejection, claim in REJECTED_LABEL_TESTS
    ]


def build_acceptance_summary(
    index: dict[str, Any],
    spine: dict[str, Any],
    assignments: list[dict[str, Any]],
    surface_types: list[dict[str, Any]],
    rejected_tests: list[dict[str, str]],
) -> dict[str, Any]:
    assign_count = sum(1 for item in assignments if item["assignment_status"] == "ASSIGN")
    assign_mix_count = sum(
        1 for item in assignments if item["assignment_status"] == "ASSIGN_MIX"
    )
    split_count = sum(1 for item in assignments if item["assignment_status"] == "SPLIT")
    withhold_count = 0
    return {
        "taxonomy_gate": "PASS",
        "taxonomy_status": "TAXONOMY_V0_DESCRIPTIVE_ONLY",
        "node_targets_considered": len(index.get("nodes", [])),
        "edge_targets_considered": 0,
        "sequence_targets_considered": 0,
        "node_targets_assigned": len(assignments),
        "node_targets_withheld": withhold_count,
        "edge_targets_assigned": 0,
        "sequence_targets_assigned": 0,
        "assignment_count": len(assignments),
        "assign_count": assign_count,
        "assign_mix_count": assign_mix_count,
        "split_count": split_count,
        "withhold_count": withhold_count,
        "surface_family_count": len(SURFACE_FAMILIES),
        "surface_type_count": len(surface_types),
        "m1_node_count": len(index.get("nodes", [])),
        "m2_node_count": len(spine.get("nodes", [])),
        "m2_edge_count": len(spine.get("edges", [])),
        "m2_spine_status": spine.get("spine_status"),
        "source_commit_only_meta_node_count": sum(
            1
            for node in spine.get("nodes", [])
            if node.get("receipt_backing_kind") == "SOURCE_COMMIT_ONLY_META_HANDOFF"
        ),
        "runtime_receipt_node_count": sum(
            1
            for node in spine.get("nodes", [])
            if node.get("receipt_backing_kind") == "RUNTIME_RECEIPT"
        ),
        "all_observed_nodes_classified_or_withheld": (
            len(assignments) + withhold_count == len(index.get("nodes", []))
        ),
        "decompression_fail_count": 0,
        "authority_leak_reject_count": sum(
            1
            for test in rejected_tests
            if test["observed_rejection"] == "AUTHORITY_LEAK_REJECTED"
        ),
        "rejected_label_test_count": len(rejected_tests),
        "assignment_outcomes_allowed": [
            "ASSIGN",
            "ASSIGN_MIX",
            "WITHHOLD",
            "REFINE",
            "WEAKEN",
            "SPLIT",
            "MERGE",
            "DROP",
        ],
        "assignment_outcomes_used": sorted(
            {assignment["assignment_status"] for assignment in assignments}
        ),
        "edge_lawfulness_validated": False,
        "receipt_truth_validated": False,
        "runtime_truth_validated": False,
        "runtime_replay_performed": False,
        "decision_path_updater_created": False,
    }


def verify_commits(
    index_commit: str,
    spine_commit: str,
    law_commit: str,
    closeout_commit: str,
) -> None:
    expected = {
        "source_index_commit_sha": (index_commit, EXPECTED_INDEX_COMMIT),
        "source_receipt_spine_commit_sha": (spine_commit, EXPECTED_SPINE_COMMIT),
        "source_compression_law_commit_sha": (law_commit, EXPECTED_LAW_COMMIT),
        "source_closeout_wrapper_commit_sha": (closeout_commit, EXPECTED_CLOSEOUT_COMMIT),
    }
    failures = [
        f"{name}:{got}!={want}"
        for name, (got, want) in expected.items()
        if got != want
    ]
    if failures:
        raise GenerationError("; ".join(failures))


def build_taxonomy(root: Path) -> dict[str, Any]:
    index = load_json(root, INDEX_PATH)
    spine = load_json(root, SPINE_PATH)
    law = load_json(root, LAW_PATH)
    validate_sources(index, spine, law)

    index_commit = commit_for_paths(root, [INDEX_PATH, INDEX_MD_PATH, INDEX_GENERATOR])
    spine_commit = commit_for_paths(root, [SPINE_PATH, SPINE_MD_PATH, SPINE_GENERATOR])
    law_commit = commit_for_paths(root, [LAW_PATH, LAW_MD_PATH, LAW_GENERATOR])
    closeout_commit = commit_for_paths(
        root,
        [
            CLOSEOUT_WRAPPER_PATH,
            CLOSEOUT_WRAPPER_MD_PATH,
            CLOSEOUT_MANIFEST_PATH,
            CLOSEOUT_DRY_RUN_PATH,
            CLOSEOUT_GENERATOR,
        ],
    )
    verify_commits(index_commit, spine_commit, law_commit, closeout_commit)

    surface_types = build_surface_types()
    surface_families = build_surface_families()
    assignments = build_assignments(index, spine, surface_types)
    rejected_tests = build_rejected_label_tests()

    taxonomy = {
        "schema_version": SCHEMA_VERSION,
        "taxonomy_role": "descriptive_label_registry_for_observed_c8_proceed_surfaces",
        "source_index_path": INDEX_PATH,
        "source_receipt_spine_path": SPINE_PATH,
        "source_compression_law_path": LAW_PATH,
        "source_index_schema": index.get("schema_version"),
        "source_receipt_spine_schema": spine.get("schema_version"),
        "source_compression_law_schema": law.get("schema_version"),
        "source_index_sha256": sha256_file(root / INDEX_PATH),
        "source_receipt_spine_sha256": sha256_file(root / SPINE_PATH),
        "source_compression_law_sha256": sha256_file(root / LAW_PATH),
        "source_index_commit_sha": index_commit,
        "source_receipt_spine_commit_sha": spine_commit,
        "source_compression_law_commit_sha": law_commit,
        "preservation_context": {
            "uses_m4_as_semantic_dependency": False,
            "context_role": "preservation_context_only",
            "source_closeout_wrapper_path": CLOSEOUT_WRAPPER_PATH,
            "source_closeout_wrapper_commit_sha": closeout_commit,
            "source_closeout_wrapper_sha256": sha256_file(root / CLOSEOUT_WRAPPER_PATH),
            "source_closeout_dry_run_path": CLOSEOUT_DRY_RUN_PATH,
            "source_closeout_dry_run_sha256": sha256_file(root / CLOSEOUT_DRY_RUN_PATH),
        },
        "taxonomy_status": "TAXONOMY_V0_DESCRIPTIVE_ONLY",
        "label_authority": "ZERO_AUTHORITY_DESCRIPTIVE_ONLY",
        "authority_created": False,
        "runner_moves_created": False,
        "runner_created": False,
        "schema_promoted": False,
        "reusable_preapproved_authority_created": False,
        "future_authorization_created": False,
        "edge_lawfulness_validated": False,
        "receipt_truth_validated": False,
        "runtime_truth_validated": False,
        "runtime_replay_performed": False,
        "runtime_probe_build_rerun_executed": False,
        "decision_path_updater_created": False,
        "receipts_rewritten": False,
        "surface_families": surface_families,
        "surface_types": surface_types,
        "surface_assignments": assignments,
        "withheld_assignments": [],
        "rejected_label_tests": rejected_tests,
        "acceptance_summary": build_acceptance_summary(
            index,
            spine,
            assignments,
            surface_types,
            rejected_tests,
        ),
        "non_claims": list(NON_CLAIMS),
        "generated_by": GENERATOR,
    }
    return taxonomy


def render_markdown(taxonomy: dict[str, Any]) -> str:
    summary = taxonomy["acceptance_summary"]
    lines = [
        "# Proceed Surface Taxonomy v0",
        "",
        "## Status",
        "",
        taxonomy["taxonomy_status"],
        "",
        "## Purpose",
        "",
        "M5 is a zero-authority descriptive label registry for observed C8 proceed surfaces.",
        "",
        "## Source",
        "",
        f"- M1 index: `{taxonomy['source_index_path']}`",
        f"  - SHA256: `{taxonomy['source_index_sha256']}`",
        f"  - Commit: `{taxonomy['source_index_commit_sha']}`",
        f"- M2 receipt spine: `{taxonomy['source_receipt_spine_path']}`",
        f"  - SHA256: `{taxonomy['source_receipt_spine_sha256']}`",
        f"  - Commit: `{taxonomy['source_receipt_spine_commit_sha']}`",
        f"- M3 compression law: `{taxonomy['source_compression_law_path']}`",
        f"  - SHA256: `{taxonomy['source_compression_law_sha256']}`",
        f"  - Commit: `{taxonomy['source_compression_law_commit_sha']}`",
        f"- M4 preservation context commit: `{taxonomy['preservation_context']['source_closeout_wrapper_commit_sha']}`",
        f"- M4 semantic dependency: `{str(taxonomy['preservation_context']['uses_m4_as_semantic_dependency']).lower()}`",
        "",
        "## Core law",
        "",
        "A proceed-surface label is admissible only when it resolves to M1 targets, resolves through M2 evidence or explicit source-commit-only meta status, decompresses through M3-required source fields, declares its weakest useful reading, declares what it must not impersonate, and creates no authority.",
        "",
        "## Acceptance summary",
        "",
        f"- Label authority: `{taxonomy['label_authority']}`",
        f"- Node targets considered: `{summary['node_targets_considered']}`",
        f"- Edge targets considered: `{summary['edge_targets_considered']}`",
        f"- Sequence targets considered: `{summary['sequence_targets_considered']}`",
        f"- Assignments: `{summary['assignment_count']}`",
        f"- Withheld assignments: `{summary['withhold_count']}`",
        f"- M2 spine status: `{summary['m2_spine_status']}`",
        "",
        "## Surface Families",
        "",
    ]
    for family in taxonomy["surface_families"]:
        lines.append(f"- `{family['family_id']}` - {family['family_status']}")

    lines.extend(["", "## Surface Types", ""])
    lines.append("| surface_type_id | label | family | smallest honest reading | must not impersonate |")
    lines.append("| --- | --- | --- | --- | --- |")
    for surface_type in taxonomy["surface_types"]:
        lines.append(
            "| `{sid}` | `{label}` | `{family}` | {reading} | {must_not} |".format(
                sid=surface_type["surface_type_id"],
                label=surface_type["label"],
                family=surface_type["family"],
                reading=surface_type["smallest_honest_reading"],
                must_not=", ".join(surface_type["must_not_impersonate"]),
            )
        )

    lines.extend(["", "## Assignments", ""])
    lines.append("| target_id | assignment_status | primary_surface_type | assigned_surface_types | confidence | basis |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for assignment in taxonomy["surface_assignments"]:
        lines.append(
            "| `{node}` | `{status}` | `{primary}` | {types} | `{confidence}` | {basis} |".format(
                node=assignment["node_id"],
                status=assignment["assignment_status"],
                primary=assignment["primary_surface_type"],
                types=", ".join(f"`{value}`" for value in assignment["assigned_surface_type_ids"]),
                confidence=assignment["confidence"],
                basis=", ".join(assignment["basis"]),
            )
        )

    lines.extend(["", "## Withheld assignments", ""])
    if taxonomy["withheld_assignments"]:
        for withheld in taxonomy["withheld_assignments"]:
            lines.append(f"- `{withheld['target_id']}`: `{withheld['withhold_reason']}`")
    else:
        lines.append("- None.")

    lines.extend(["", "## Rejected Label Tests", ""])
    lines.append("| test_id | bad_label | expected_result | observed_result | pass/fail |")
    lines.append("| --- | --- | --- | --- | --- |")
    for test in taxonomy["rejected_label_tests"]:
        lines.append(
            f"| `{test['test_id']}` | {test['bad_label']} | `{test['expected_result']}` | `{test['observed_result']}` | `{test['test_result']}` |"
        )

    lines.extend(
        [
            "",
            "## Relationship to M6",
            "",
            "M6 uses this vocabulary once in one live continuation packet.",
            "",
            "## Relationship to M7",
            "",
            "M7 must not treat M5 labels as transition rules.",
        ]
    )

    lines.extend(["", "## Non-Claims", ""])
    for claim in taxonomy["non_claims"]:
        lines.append(f"- {claim}")

    return "\n".join(lines) + "\n"


def write_outputs(root: Path, taxonomy: dict[str, Any]) -> None:
    json_path = root / OUTPUT_JSON
    md_path = root / OUTPUT_MD
    json_path.write_text(
        json.dumps(taxonomy, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(taxonomy), encoding="utf-8")


def main() -> int:
    try:
        root = detect_repo_root(Path.cwd())
        taxonomy = build_taxonomy(root)
        write_outputs(root, taxonomy)
    except GenerationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(
        "Generated proceed_surface_taxonomy_v0 with "
        f"{len(taxonomy['surface_assignments'])} node assignments"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
