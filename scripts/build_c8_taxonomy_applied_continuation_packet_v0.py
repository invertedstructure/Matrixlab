#!/usr/bin/env python3
"""Build C8 taxonomy-applied continuation packet v0.

M6 uses proceed_surface_taxonomy_v0 as a descriptive label membrane inside one
continuation packet. It does not create runner authority, choose the next C8
unit, validate receipts/runtime/edge lawfulness, promote schemas, or create a
decision-path updater.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "matrixlabs_c8_taxonomy_applied_continuation_packet_v0"
GENERATOR = "scripts/build_c8_taxonomy_applied_continuation_packet_v0.py"

INDEX_PATH = "docs/matrixlabs/observability/decision_path_index_v0.json"
SPINE_PATH = "docs/matrixlabs/observability/receipt_spine_v0.json"
LAW_PATH = "docs/matrixlabs/observability/compression_decompression_law_v0.json"
TAXONOMY_PATH = "docs/matrixlabs/observability/proceed_surface_taxonomy_v0.json"
CLOSEOUT_WRAPPER_PATH = "docs/matrixlabs/observability/closeout_wrapper_v0.json"

INDEX_COMMIT_PATHS = [
    INDEX_PATH,
    "docs/matrixlabs/observability/decision_path_index_v0.md",
    "scripts/build_decision_path_index_v0.py",
]
SPINE_COMMIT_PATHS = [
    SPINE_PATH,
    "docs/matrixlabs/observability/receipt_spine_v0.md",
    "scripts/build_receipt_spine_v0.py",
]
LAW_COMMIT_PATHS = [
    LAW_PATH,
    "docs/matrixlabs/observability/compression_decompression_law_v0.md",
    "scripts/build_compression_decompression_law_v0.py",
]
TAXONOMY_COMMIT_PATHS = [
    TAXONOMY_PATH,
    "docs/matrixlabs/observability/proceed_surface_taxonomy_v0.md",
    "scripts/build_proceed_surface_taxonomy_v0.py",
]
CLOSEOUT_COMMIT_PATHS = [
    CLOSEOUT_WRAPPER_PATH,
    "docs/matrixlabs/observability/closeout_wrapper_v0.md",
    "docs/matrixlabs/observability/closeout_manifests/matrixlabs_observability_m1_m3_closeout_v0.json",
    "docs/matrixlabs/observability/closeouts/closeout_matrixlabs_observability_m1_m3_closeout_v0_dry_run_v0.json",
    "scripts/matrixlab_closeout_wrapper_v0.py",
]

EXPECTED_COMMITS = {
    "source_index_commit_sha": "e0e22d33ee1fdfc9dad6964013162a58d6a0b169",
    "source_receipt_spine_commit_sha": "e78ae91156521669e57bfca3c112d4b83e681d05",
    "source_compression_law_commit_sha": "58f4743e38a6d49e877a7d8b81f0a82c30ad0915",
    "source_taxonomy_commit_sha": "099a003bf849cc0d4292c4980982166be291f405",
    "source_closeout_wrapper_commit_sha": "6aa9070f2d7a845640a23370a742ee13723a3b51",
}

OUTPUT_JSON = "docs/matrixlabs/c8/continuation/c8_taxonomy_applied_continuation_packet_v0.json"
OUTPUT_MD = "docs/matrixlabs/c8/continuation/c8_taxonomy_applied_continuation_packet_v0.md"

PRIMARY_SURFACE_TYPE = "surface.decision_packet.v0"
SECONDARY_SURFACE_TYPES = ["surface.human_acceptance.v0"]
PACKET_STATUS = "PACKET_PREPARED"
HUMAN_BOUNDARY_STATUS = "REQUIRED_NOT_YET_CONSUMED"
AUTHORIZED_FUTURE_UNIT_STATUS = "NOT_AUTHORIZED_BY_TAXONOMY_LABEL"
TAXONOMY_APPLICATION_STATUS = "LIVE_PACKET_APPLICATION_NOT_M5_ASSIGNMENT"
TAXONOMY_USE_RESULT = "TAXONOMY_USE_PASS_WITH_ASSIGN_MIX"
TAXONOMY_FAILURE_MODE = "WITHHOLD_OR_ASSIGN_MIX"

REQUIRED_M5_SOURCE_FIELDS = [
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

REQUIRED_EVIDENCE_FIELDS = [
    "source_packet_path",
    "source_commit_sha",
    "receipt_id_or_pending_receipt_status",
    "human_boundary_status",
    "authorized_future_unit",
    "forbidden_actions_explicitly_preserved",
]

MUST_NOT_IMPERSONATE = [
    "human acceptance",
    "future unit authorization",
    "runner move",
    "schema promotion",
    "receipt validation",
    "edge lawfulness",
    "decision-path update rule",
]

FORBIDDEN_ACTIONS = [
    "do_not_treat_taxonomy_label_as_authorization",
    "do_not_treat_taxonomy_label_as_human_acceptance",
    "do_not_treat_taxonomy_label_as_runner_move",
    "do_not_treat_taxonomy_label_as_schema_promotion",
    "do_not_treat_taxonomy_label_as_receipt_validation",
    "do_not_treat_taxonomy_label_as_edge_lawfulness",
    "do_not_create_decision_path_updater",
]

NON_CLAIMS = [
    "This packet uses proceed_surface_taxonomy_v0 descriptively only.",
    "The taxonomy label does not authorize the continuation.",
    "The taxonomy label does not replace human decision.",
    "The taxonomy label does not prove receipt validity.",
    "The taxonomy label does not prove edge lawfulness.",
    "The taxonomy label does not create a reusable move.",
    "The taxonomy label does not promote a schema.",
    "The taxonomy label does not decide the next C8 unit.",
    "The taxonomy label does not create runner logic.",
    "The taxonomy label does not create a decision-path updater.",
    "The taxonomy label only makes the packet’s observed surface role explicit.",
    "The taxonomy label only makes the packet\u00e2\u20ac\u2122s observed surface role explicit.",
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
        raise GenerationError(f"no existing paths among: {paths}")
    return run_git(root, ["log", "-n", "1", "--format=%H", "--", *existing])


def verify_commit(root: Path, label: str, got: str) -> None:
    want = EXPECTED_COMMITS[label]
    if got != want:
        raise GenerationError(f"{label}:{got}!={want}")
    run_git(root, ["cat-file", "-e", f"{got}^{{commit}}"])


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


def scalar_values(value: Any) -> list[Any]:
    if isinstance(value, dict):
        out: list[Any] = []
        for item in value.values():
            out.extend(scalar_values(item))
        return out
    if isinstance(value, list):
        out = []
        for item in value:
            out.extend(scalar_values(item))
        return out
    return [value]


def validate_sources(
    index: dict[str, Any],
    spine: dict[str, Any],
    law: dict[str, Any],
    taxonomy: dict[str, Any],
) -> None:
    checks = {
        "source_index_schema": (index.get("schema_version"), "matrixlabs_decision_path_index_v0"),
        "source_receipt_spine_schema": (spine.get("schema_version"), "matrixlabs_receipt_spine_v0"),
        "source_compression_law_schema": (law.get("schema_version"), "matrixlabs_compression_decompression_law_v0"),
        "source_taxonomy_schema": (taxonomy.get("schema_version"), "matrixlabs_proceed_surface_taxonomy_v0"),
        "taxonomy_status": (taxonomy.get("taxonomy_status"), "TAXONOMY_V0_DESCRIPTIVE_ONLY"),
        "label_authority": (taxonomy.get("label_authority"), "ZERO_AUTHORITY_DESCRIPTIVE_ONLY"),
        "spine_status": (spine.get("spine_status"), "SPINE_PASS_WITH_SOURCE_COMMIT_ONLY_META_NODES"),
        "law_status": (law.get("law_status"), "LAW_PASS_V0_TESTS"),
    }
    failures = [
        f"{name}:{got}!={want}"
        for name, (got, want) in checks.items()
        if got != want
    ]
    if failures:
        raise GenerationError("; ".join(failures))


def validate_surface_types(taxonomy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    surface_types = {
        item.get("surface_type_id"): item
        for item in taxonomy.get("surface_types", [])
    }
    applied = [PRIMARY_SURFACE_TYPE, *SECONDARY_SURFACE_TYPES]
    failures = []
    for surface_id in applied:
        record = surface_types.get(surface_id)
        if not record:
            failures.append(f"applied_surface_type_missing:{surface_id}")
            continue
        if record.get("surface_status") != "DESCRIPTIVE_ACTIVE_V0":
            failures.append(f"{surface_id}_surface_status:{record.get('surface_status')}")
        for field in [
            "smallest_honest_reading",
            "allowed_use",
            "must_not_impersonate",
            "required_source_fields",
            "decompression_requirement",
        ]:
            if not record.get(field):
                failures.append(f"{surface_id}_missing_or_empty:{field}")
        missing_source_fields = [
            field
            for field in REQUIRED_M5_SOURCE_FIELDS
            if field not in record.get("required_source_fields", [])
        ]
        if missing_source_fields:
            failures.append(f"{surface_id}_missing_source_fields:{missing_source_fields}")
    if failures:
        raise GenerationError("; ".join(failures))
    return surface_types


def forbidden_authorized_value() -> str:
    return "AUTHORIZED_BY_" + "TAXONOMY_LABEL"


def validate_packet(packet: dict[str, Any]) -> None:
    bad_value = forbidden_authorized_value()
    failures = []
    if TAXONOMY_APPLICATION_STATUS != packet.get("taxonomy_use", {}).get("taxonomy_application_status"):
        failures.append("taxonomy_application_status_wrong")
    if packet.get("packet_status") == packet.get("taxonomy_use", {}).get("taxonomy_use_status"):
        failures.append("packet_status_not_separate_from_taxonomy_status")
    if bad_value in scalar_values(packet):
        failures.append("forbidden_authorized_by_taxonomy_label_value_present")
    for required in MUST_NOT_IMPERSONATE:
        if required not in packet.get("taxonomy_use", {}).get("must_not_impersonate", []):
            failures.append(f"must_not_impersonate_missing:{required}")
    for required in REQUIRED_EVIDENCE_FIELDS:
        if required not in packet.get("taxonomy_use", {}).get("required_evidence_fields", []):
            failures.append(f"required_evidence_field_missing:{required}")
    summary = packet.get("acceptance_summary", {})
    expected_summary = {
        "taxonomy_source_named": True,
        "primary_surface_type_exists_in_m5": True,
        "secondary_surface_types_exist_in_m5": True,
        "surface_types_m3_decompressible_through_m5": True,
        "packet_status_separate_from_taxonomy_label": True,
        "human_boundary_status_explicit": True,
        "authorized_future_unit_status_explicit": True,
        "forbidden_impersonations_preserved": True,
        "assign_mix_used_for_mixed_surface": True,
        "taxonomy_use_verdict_recorded": True,
        "taxonomy_treated_as_move_permission": False,
        "taxonomy_treated_as_schema_promotion": False,
        "taxonomy_treated_as_human_acceptance": False,
        "taxonomy_treated_as_receipt_validation": False,
        "taxonomy_treated_as_edge_lawfulness": False,
        "decision_path_updater_created": False,
        "next_c8_unit_chosen_by_packet": False,
    }
    for key, want in expected_summary.items():
        if summary.get(key) != want:
            failures.append(f"acceptance_summary_{key}:{summary.get(key)}!={want}")
    if failures:
        raise GenerationError("; ".join(failures))


def build_packet(root: Path) -> dict[str, Any]:
    index = load_json(root, INDEX_PATH)
    spine = load_json(root, SPINE_PATH)
    law = load_json(root, LAW_PATH)
    taxonomy = load_json(root, TAXONOMY_PATH)
    validate_sources(index, spine, law, taxonomy)
    validate_surface_types(taxonomy)

    commits = {
        "source_index_commit_sha": commit_for_paths(root, INDEX_COMMIT_PATHS),
        "source_receipt_spine_commit_sha": commit_for_paths(root, SPINE_COMMIT_PATHS),
        "source_compression_law_commit_sha": commit_for_paths(root, LAW_COMMIT_PATHS),
        "source_taxonomy_commit_sha": commit_for_paths(root, TAXONOMY_COMMIT_PATHS),
        "source_closeout_wrapper_commit_sha": commit_for_paths(root, CLOSEOUT_COMMIT_PATHS),
    }
    for label, commit in commits.items():
        verify_commit(root, label, commit)

    taxonomy_use = {
        "taxonomy_source": "proceed_surface_taxonomy_v0",
        "taxonomy_source_schema": "matrixlabs_proceed_surface_taxonomy_v0",
        "taxonomy_use_status": "DESCRIPTIVE_ONLY",
        "taxonomy_application_status": TAXONOMY_APPLICATION_STATUS,
        "primary_surface_type": PRIMARY_SURFACE_TYPE,
        "secondary_surface_types": list(SECONDARY_SURFACE_TYPES),
        "packet_status": PACKET_STATUS,
        "human_boundary_status": HUMAN_BOUNDARY_STATUS,
        "authorized_future_unit_status": AUTHORIZED_FUTURE_UNIT_STATUS,
        "authorized_future_unit": None,
        "surface_application_basis": {
            "m5_surface_type_exists": True,
            "m5_surface_type_status": "DESCRIPTIVE_ACTIVE_V0",
            "m1_m2_m3_backing": "M5 surface types were admitted through M1/M2/M3; this packet applies the already-admitted types descriptively.",
            "m3_decompression_status": "label use preserves source pointer, receipt/evidence status, human boundary, authorized future unit status, and forbidden impersonation fields",
        },
        "allowed_handling": [
            "describe the packet surface",
            "state required evidence for continuation",
            "state human boundary if acceptance is needed",
            "state forbidden impersonations",
            "make continuation packet easier to read",
        ],
        "must_not_impersonate": list(MUST_NOT_IMPERSONATE),
        "required_evidence_fields": list(REQUIRED_EVIDENCE_FIELDS),
        "decompression_target": [
            "source packet pointer",
            "commit pointer",
            "receipt or pending receipt status",
            "human boundary field",
            "authorized future unit field",
            "forbidden impersonation field",
            "non-claims",
        ],
        "taxonomy_failure_mode": TAXONOMY_FAILURE_MODE,
    }

    packet = {
        "schema_version": SCHEMA_VERSION,
        "packet_role": "c8_continuation_packet_with_one_m5_taxonomy_live_use_test",
        "continuation_unit_id": "c8.continuation.m6_taxonomy_live_use_test.v0",
        "continuation_packet_role": "one_live_use_test_of_proceed_surface_taxonomy_v0",
        "source_index_path": INDEX_PATH,
        "source_receipt_spine_path": SPINE_PATH,
        "source_compression_law_path": LAW_PATH,
        "source_taxonomy_path": TAXONOMY_PATH,
        "source_index_schema": index.get("schema_version"),
        "source_receipt_spine_schema": spine.get("schema_version"),
        "source_compression_law_schema": law.get("schema_version"),
        "source_taxonomy_schema": taxonomy.get("schema_version"),
        "source_index_sha256": sha256_file(root / INDEX_PATH),
        "source_receipt_spine_sha256": sha256_file(root / SPINE_PATH),
        "source_compression_law_sha256": sha256_file(root / LAW_PATH),
        "source_taxonomy_sha256": sha256_file(root / TAXONOMY_PATH),
        **{key: commits[key] for key in [
            "source_index_commit_sha",
            "source_receipt_spine_commit_sha",
            "source_compression_law_commit_sha",
            "source_taxonomy_commit_sha",
        ]},
        "preservation_context": {
            "uses_m4_as_semantic_dependency": False,
            "source_closeout_wrapper_path": CLOSEOUT_WRAPPER_PATH,
            "source_closeout_wrapper_commit_sha": commits["source_closeout_wrapper_commit_sha"],
        },
        "packet_status": PACKET_STATUS,
        "continuation_target": {
            "continuation_unit_id": "c8.continuation.m6_taxonomy_live_use_test.v0",
            "continuation_packet_role": "one_live_use_test_of_proceed_surface_taxonomy_v0",
            "packet_status": PACKET_STATUS,
            "primary_surface_type": PRIMARY_SURFACE_TYPE,
            "secondary_surface_types": list(SECONDARY_SURFACE_TYPES),
            "human_boundary_status": HUMAN_BOUNDARY_STATUS,
            "authorized_future_unit_status": AUTHORIZED_FUTURE_UNIT_STATUS,
            "expected_evidence_surface": "pending_future_receipt_or_source_commit_context",
            "authorized_future_unit": None,
            "forbidden_actions": list(FORBIDDEN_ACTIONS),
        },
        "taxonomy_use": taxonomy_use,
        "taxonomy_use_verdict": {
            "result": TAXONOMY_USE_RESULT,
            "surface_type_helped": True,
            "authority_status_changed": False,
            "human_boundary_preserved": True,
            "authorized_future_unit_preserved": True,
            "forbidden_impersonations_preserved": True,
            "decompression_back_to_source_available": True,
            "needs_taxonomy_refinement": False,
            "reason": "The packet is primarily a decision_packet_surface and secondarily carries a human_acceptance_surface posture with human_boundary_status REQUIRED_NOT_YET_CONSUMED; mixed use preserves the boundary without authorizing movement.",
        },
        "acceptance_summary": {
            "taxonomy_source_named": True,
            "primary_surface_type_exists_in_m5": True,
            "secondary_surface_types_exist_in_m5": True,
            "surface_types_m3_decompressible_through_m5": True,
            "packet_status_separate_from_taxonomy_label": True,
            "human_boundary_status_explicit": True,
            "authorized_future_unit_status_explicit": True,
            "forbidden_impersonations_preserved": True,
            "assign_mix_used_for_mixed_surface": True,
            "taxonomy_use_verdict_recorded": True,
            "taxonomy_treated_as_move_permission": False,
            "taxonomy_treated_as_schema_promotion": False,
            "taxonomy_treated_as_human_acceptance": False,
            "taxonomy_treated_as_receipt_validation": False,
            "taxonomy_treated_as_edge_lawfulness": False,
            "decision_path_updater_created": False,
            "next_c8_unit_chosen_by_packet": False,
        },
        "authority_created": False,
        "runner_moves_created": False,
        "runner_created": False,
        "schema_promoted": False,
        "future_authorization_created": False,
        "edge_lawfulness_validated": False,
        "receipt_truth_validated": False,
        "runtime_truth_validated": False,
        "runtime_replay_performed": False,
        "runtime_probe_build_rerun_executed": False,
        "decision_path_updater_created": False,
        "next_c8_unit_chosen_by_packet": False,
        "receipts_rewritten": False,
        "non_claims": list(NON_CLAIMS),
        "generated_by": GENERATOR,
    }
    validate_packet(packet)
    return packet


def render_markdown(packet: dict[str, Any]) -> str:
    taxonomy_use = packet["taxonomy_use"]
    verdict = packet["taxonomy_use_verdict"]
    summary = packet["acceptance_summary"]
    lines = [
        "# C8 Taxonomy-Applied Continuation Packet v0",
        "",
        "## Status",
        "",
        packet["packet_status"],
        "",
        "## Purpose",
        "",
        "One live-use test of proceed_surface_taxonomy_v0 inside a C8 continuation packet.",
        "",
        "## Source stack",
        "",
        f"- M1 index: `{packet['source_index_path']}` / `{packet['source_index_schema']}` / `{packet['source_index_sha256']}` / `{packet['source_index_commit_sha']}`",
        f"- M2 receipt spine: `{packet['source_receipt_spine_path']}` / `{packet['source_receipt_spine_schema']}` / `{packet['source_receipt_spine_sha256']}` / `{packet['source_receipt_spine_commit_sha']}`",
        f"- M3 compression law: `{packet['source_compression_law_path']}` / `{packet['source_compression_law_schema']}` / `{packet['source_compression_law_sha256']}` / `{packet['source_compression_law_commit_sha']}`",
        f"- M5 taxonomy: `{packet['source_taxonomy_path']}` / `{packet['source_taxonomy_schema']}` / `{packet['source_taxonomy_sha256']}` / `{packet['source_taxonomy_commit_sha']}`",
        "",
        "## Continuation target",
        "",
        f"- continuation_unit_id: `{packet['continuation_unit_id']}`",
        f"- packet role: `{packet['packet_role']}`",
        "",
        "## Taxonomy-use block",
        "",
        f"- taxonomy source: `{taxonomy_use['taxonomy_source']}`",
        f"- use status: `{taxonomy_use['taxonomy_use_status']}`",
        f"- application status: `{taxonomy_use['taxonomy_application_status']}`",
        f"- primary surface type: `{taxonomy_use['primary_surface_type']}`",
        f"- secondary surface types: {', '.join(f'`{item}`' for item in taxonomy_use['secondary_surface_types'])}",
        f"- packet status: `{taxonomy_use['packet_status']}`",
        f"- human-boundary status: `{taxonomy_use['human_boundary_status']}`",
        f"- authorized-future-unit status: `{taxonomy_use['authorized_future_unit_status']}`",
        f"- allowed handling: {', '.join(taxonomy_use['allowed_handling'])}",
        f"- required evidence fields: {', '.join(taxonomy_use['required_evidence_fields'])}",
        f"- forbidden impersonations: {', '.join(taxonomy_use['must_not_impersonate'])}",
        "",
        "## Taxonomy-use verdict",
        "",
        f"- result: `{verdict['result']}`",
        f"- surface_type_helped: `{str(verdict['surface_type_helped']).lower()}`",
        f"- authority_status_changed: `{str(verdict['authority_status_changed']).lower()}`",
        f"- human_boundary_preserved: `{str(verdict['human_boundary_preserved']).lower()}`",
        f"- authorized_future_unit_preserved: `{str(verdict['authorized_future_unit_preserved']).lower()}`",
        f"- forbidden_impersonations_preserved: `{str(verdict['forbidden_impersonations_preserved']).lower()}`",
        f"- decompression_back_to_source_available: `{str(verdict['decompression_back_to_source_available']).lower()}`",
        f"- needs_taxonomy_refinement: `{str(verdict['needs_taxonomy_refinement']).lower()}`",
        "",
        "## Acceptance summary",
        "",
    ]
    for key in sorted(summary):
        lines.append(f"- `{key}`: `{str(summary[key]).lower()}`")
    lines.extend(["", "## Non-claims", ""])
    for claim in packet["non_claims"]:
        lines.append(f"- {claim}")
    lines.extend(
        [
            "",
            "## Relationship to M5",
            "",
            "M5 produced the vocabulary; M6 applies it once.",
            "",
            "## Relationship to M7",
            "",
            "M6 passing makes M7 discussable, not authorized.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(root: Path, packet: dict[str, Any]) -> None:
    json_path = root / OUTPUT_JSON
    md_path = root / OUTPUT_MD
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(packet), encoding="utf-8")


def main() -> int:
    try:
        root = detect_repo_root(Path.cwd())
        packet = build_packet(root)
        write_outputs(root, packet)
    except GenerationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(
        "Generated c8_taxonomy_applied_continuation_packet_v0 "
        f"with result {packet['taxonomy_use_verdict']['result']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
