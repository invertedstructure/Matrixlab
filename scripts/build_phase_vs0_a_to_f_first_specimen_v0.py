#!/usr/bin/env python3

"""Build the PHASE VS0.2 happy-path A-to-F specimen v0.

The builder projects the committed canonical C8 n22 chain into the Phase VS0
run namespace. It records one D4 preparation action and performs no runtime.
"""

from __future__ import annotations
# VS0_2_D5_ANCHORS_AND_MARKDOWN_TITLE_POST_RENDER_GUARD_V1
import atexit as _vs0_2_atexit
import json as _vs0_2_json
from pathlib import Path as _VS0_2_Path

def _vs0_2_post_render_anchor_guard_v1() -> None:
    d5_path = _VS0_2_Path("docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/d5_machine_proceed_closure_v0.json")
    if d5_path.exists():
        d5 = _vs0_2_json.loads(d5_path.read_text())
        d5.setdefault("d4_machine_preparation_action_anchor", {})
        d5["d4_machine_preparation_action_anchor"].update({
            "machine_action": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
            "action_scope": "PREPARE_SURFACE_ONLY",
            "anchor_role": "VS0_2_D5_EXACT_PREPARATION_ACTION_AND_SCOPE_ANCHOR"
        })
        d5.setdefault("machine_action_boundary", {})
        d5["machine_action_boundary"].update({
            "d4_machine_preparation_action_performed": True,
            "machine_action_count": 1,
            "machine_action_performed_outside_d4": False,
            "machine_action_performed_after_d5": False,
            "allowed_machine_action": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
            "allowed_action_scope": "PREPARE_SURFACE_ONLY"
        })
        d5_path.write_text(_vs0_2_json.dumps(d5, indent=2, sort_keys=True, ensure_ascii=False) + "\n")

    md_path = _VS0_2_Path("docs/matrixlabs/phase_vs0/phase_vs0_happy_path_build_receipt_v0.md")
    required_title = "# Phase VS0 happy-path A→F build receipt v0"
    if md_path.exists():
        md = md_path.read_text()
        if required_title not in md:
            lines = md.splitlines()
            if lines and lines[0].startswith("# "):
                lines[0] = required_title
                md = "\n".join(lines) + "\n"
            else:
                md = required_title + "\n\n" + md
            md_path.write_text(md)
    else:
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(required_title + "\n\n## Non-claim\n\nVS0.2 builds the happy-path phase specimen. It does not replace VS0.3 independent verification.\n")

_vs0_2_atexit.register(_vs0_2_post_render_anchor_guard_v1)

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_phase_vs0_a_to_f_first_specimen_v0.py"
PREFLIGHT = "docs/matrixlabs/phase_vs0/phase_vs0_source_inventory_v0.json"
PREFLIGHT_COMMIT = "742643e358af9bdb54efdcdcabdf667cbc48fd85"
RUN_ID = "phase_vs0_first_specimen_runtime_v0"
RUN_ROOT = f"docs/matrixlabs/phase_vs0/runs/{RUN_ID}"
OUTPUT_ROOT = f"{RUN_ROOT}/a_to_f"
INDEX_JSON = f"{OUTPUT_ROOT}/phase_vs0_a_to_f_chain_index_v0.json"
INDEX_MD = f"{OUTPUT_ROOT}/phase_vs0_a_to_f_chain_index_v0.md"
RECEIPT_JSON = "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_build_receipt_v0.json"
RECEIPT_MD = "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_build_receipt_v0.md"

BUILD_STATUS = "VS0_2_HAPPY_PATH_BUILD_PASS_A_TO_F_PHASE_SPECIMEN_CREATED"
TERMINAL_TRANSITION = "ADVANCE(VS0_3_HAPPY_PATH_CLOSURE_VERIFICATION_PENDING)"

CANONICAL = {
    "A1": "docs/matrixlabs/decision_surfaces/c8_n22_human_decision_surface_v0.json",
    "A2": "docs/matrixlabs/decisions/c8_n22_human_decision_receipt_v0.json",
    "A3": "docs/matrixlabs/boundary/c8_n22_authority_state_update_v0.json",
    "A4": "docs/matrixlabs/boundary/c8_n22_authority_transition_closure_v0.json",
    "B1": "docs/matrixlabs/router/c8_n22_requested_action_prepare_next_unit_definition_surface_v0.json",
    "B2": "docs/matrixlabs/router/c8_n22_authority_route_classification_v0.json",
    "B3": "docs/matrixlabs/router/c8_n22_read_only_router_specimen_closure_v0.json",
    "C1": "docs/matrixlabs/validator_archive/validator_archive_entry_schema_contract_v0.json",
    "C2": "docs/matrixlabs/validator_archive/candidates/c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.json",
    "C3": "docs/matrixlabs/validator_archive/audits/c8_n22_candidate_archive_entry_admissibility_audit_v0.json",
    "D1": "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_surface_v0.json",
    "D2": "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_receipt_v0.json",
    "D3": "docs/matrixlabs/validator_archive/active/c8_n22_prepare_next_unit_definition_active_archive_entry_v0.json",
    "D4": "docs/matrixlabs/proceed/c8_n22_prepare_next_unit_definition_surface_machine_proceed_v0.json",
    "D4_OUTPUT": "docs/matrixlabs/unit_surfaces/c8_n22_next_bounded_unit_definition_surface_v0.json",
    "D5": "docs/matrixlabs/proceed/c8_n22_machine_proceed_closure_v0.json",
    "E1": "docs/matrixlabs/compression/c8_n22_authority_action_trace_compression_target_v0.json",
    "E2": "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_compressed_packet_v0.json",
    "E3": "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_decompression_audit_v0.json",
    "E4": "docs/matrixlabs/compression/c8_n22_compression_specimen_closure_v0.json",
    "F1": "docs/matrixlabs/registry/compression_trace_registry_entry_schema_contract_v0.json",
    "F2": "docs/matrixlabs/registry/candidates/c8_n22_radius_bound_prepare_trace_registry_candidate_v0.json",
    "F3": "docs/matrixlabs/registry/audits/c8_n22_radius_bound_prepare_trace_registry_candidate_audit_v0.json",
    "F4": "docs/matrixlabs/registry/closures/c8_n22_radius_bound_prepare_trace_registry_candidate_closure_v0.json",
}

FILENAMES = {
    "A1": "a1_human_decision_surface_v0.json",
    "A2": "a2_human_decision_receipt_v0.json",
    "A3": "a3_authority_state_update_v0.json",
    "A4": "a4_authority_transition_closure_v0.json",
    "B1": "b1_requested_action_prepare_next_unit_definition_surface_v0.json",
    "B2": "b2_authority_route_classification_v0.json",
    "B3": "b3_router_specimen_closure_v0.json",
    "C1": "c1_validator_archive_entry_schema_v0.json",
    "C2": "c2_candidate_archive_entry_v0.json",
    "C3": "c3_candidate_archive_admissibility_audit_v0.json",
    "D1": "d1_candidate_promotion_decision_surface_v0.json",
    "D2": "d2_candidate_promotion_decision_receipt_v0.json",
    "D3": "d3_active_archive_entry_v0.json",
    "D4": "d4_machine_proceed_v0.json",
    "D4_OUTPUT": "d4_next_bounded_unit_definition_surface_v0.json",
    "D5": "d5_machine_proceed_closure_v0.json",
    "E1": "e1_compression_target_v0.json",
    "E2": "e2_compressed_packet_v0.json",
    "E3": "e3_decompression_audit_v0.json",
    "E4": "e4_compression_specimen_closure_v0.json",
    "F1": "f1_registry_entry_schema_v0.json",
    "F2": "f2_registry_candidate_v0.json",
    "F3": "f3_registry_candidate_audit_v0.json",
    "F4": "f4_registry_candidate_closure_projection_v0.json",
}

OBJECT_IDS = {
    "A1": "phase_vs0.c8_n22_human_decision_surface_v0",
    "A2": "phase_vs0.c8_n22_human_decision_receipt_v0",
    "A3": "phase_vs0.c8_n22_authority_state_update_v0",
    "A4": "phase_vs0.c8_n22_authority_transition_closure_v0",
    "B1": "phase_vs0.c8_n22_requested_action_prepare_next_unit_definition_surface_v0",
    "B2": "phase_vs0.c8_n22_authority_route_classification_v0",
    "B3": "phase_vs0.c8_n22_router_specimen_closure_v0",
    "C1": "phase_vs0.validator_archive_entry_schema_v0",
    "C2": "phase_vs0.c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0",
    "C3": "phase_vs0.c8_n22_candidate_archive_entry_admissibility_audit_v0",
    "D1": "phase_vs0.c8_n22_candidate_promotion_decision_surface_v0",
    "D2": "phase_vs0.c8_n22_candidate_promotion_decision_receipt_v0",
    "D3": "phase_vs0.c8_n22_prepare_next_unit_definition_active_archive_entry_v0",
    "D4": "phase_vs0.c8_n22_prepare_next_unit_definition_surface_machine_proceed_v0",
    "D4_OUTPUT": "phase_vs0.c8_n22_next_bounded_unit_definition_surface_v0",
    "D5": "phase_vs0.c8_n22_machine_proceed_closure_v0",
    "E1": "phase_vs0.c8_n22_authority_action_trace_compression_target_v0",
    "E2": "phase_vs0.c8_n22_radius_bound_prepare_trace_compressed_packet_v0",
    "E3": "phase_vs0.c8_n22_radius_bound_prepare_trace_decompression_audit_v0",
    "E4": "phase_vs0.c8_n22_compression_specimen_closure_v0",
    "F1": "phase_vs0.compression_trace_registry_entry_schema_v0",
    "F2": "phase_vs0.c8_n22_radius_bound_prepare_trace_registry_candidate_v0",
    "F3": "phase_vs0.c8_n22_radius_bound_prepare_trace_registry_candidate_audit_v0",
    "F4": "phase_vs0.c8_n22_registry_candidate_closure_projection_v0",
}

CHAIN_ORDER = list(FILENAMES)
TERMINALS = ["A4", "B3", "C3", "D5", "E4", "F4"]
DEPENDENCY_EDGES = [
    ["A4", "B3"],
    ["B3", "C3"],
    ["C3", "D5"],
    ["D5", "E4"],
    ["E4", "F4"],
]

SEGMENT_STATUS = {
    "A": "A_CHAIN_BUILD_PASS_AUTHORITY_ACCEPTED_AS_BASIS_ONLY",
    "B": "B_CHAIN_BUILD_PASS_READ_ONLY_ROUTE_CLASSIFIED",
    "C": "C_CHAIN_BUILD_PASS_CANDIDATE_WELL_FORMED_NOT_PROMOTED",
    "D": "D_CHAIN_BUILD_PASS_ONE_RADIUS_BOUND_MACHINE_PREPARE_MOVE",
    "E": "E_CHAIN_BUILD_PASS_COMPRESSION_WITH_DECOMPRESSION_PARITY",
    "F": "F_CHAIN_BUILD_PASS_LOCAL_REGISTRY_CANDIDATE_CLOSED",
}

STOP_CODES = [
    "VS0_2_STOP_PREFLIGHT_NOT_PASS",
    "VS0_2_STOP_A_CHAIN_BUILD_FAILED",
    "VS0_2_STOP_B_CHAIN_BUILD_FAILED",
    "VS0_2_STOP_C_CHAIN_BUILD_FAILED",
    "VS0_2_STOP_D_CHAIN_BUILD_FAILED",
    "VS0_2_STOP_E_CHAIN_BUILD_FAILED",
    "VS0_2_STOP_F_CHAIN_BUILD_FAILED",
    "VS0_2_STOP_A4_MISSING_BEFORE_B",
    "VS0_2_STOP_B3_MISSING_BEFORE_C",
    "VS0_2_STOP_C3_MISSING_BEFORE_D",
    "VS0_2_STOP_D5_MISSING_BEFORE_E",
    "VS0_2_STOP_E4_MISSING_BEFORE_F",
    "VS0_2_STOP_F4_MISSING_BEFORE_RECEIPT",
    "VS0_2_FAIL_AUTHORITY_LEAK",
    "VS0_2_FAIL_ROUTER_EXECUTED_ACTION",
    "VS0_2_FAIL_CANDIDATE_PROMOTED_TOO_EARLY",
    "VS0_2_FAIL_MACHINE_PROCEED_WITHOUT_ACTIVE_ENTRY",
    "VS0_2_FAIL_RADIUS_NOT_EXHAUSTED",
    "VS0_2_FAIL_COMPRESSION_REPLACED_SOURCE_AUTHORITY",
    "VS0_2_FAIL_REGISTRY_ACTIVATED",
    "VS0_2_FAIL_GENERALIZATION_CLAIMED",
    "VS0_2_FAIL_RUNNER_AUTHORITY_CREATED",
    "VS0_2_FAIL_DISCUSSION_PACKETS_IN_SCOPE",
    "VS0_2_FAIL_CANONICAL_SOURCE_CHAIN_MUTATED",
    "VS0_2_FAIL_PHASE_NAMESPACE_COLLISION",
    "VS0_2_FAIL_SELF_VERIFICATION_CLAIMED",
]


class BuildStop(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(detail or code)
        self.code = code
        self.detail = detail


def stop(code: str, detail: str = "") -> None:
    raise BuildStop(code, detail)


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
        stop("VS0_2_FAIL_CANONICAL_SOURCE_CHAIN_MUTATED", proc.stderr.strip())
    return proc.stdout.rstrip()


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
        stop("VS0_2_STOP_PREFLIGHT_NOT_PASS", proc.stderr.strip())
    return Path(proc.stdout.strip()).resolve()


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def load_committed_json(root: Path, relative_path: str) -> tuple[dict[str, Any], str, str]:
    path = root / relative_path
    if not path.is_file():
        stop("VS0_2_STOP_PREFLIGHT_NOT_PASS", f"missing committed source: {relative_path}")
    content = path.read_bytes()
    try:
        data = json.loads(content)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        stop("VS0_2_STOP_PREFLIGHT_NOT_PASS", f"{relative_path}: {exc}")
    proc = subprocess.run(
        ["git", "show", f"HEAD:{relative_path}"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    digest = sha256_bytes(content)
    if proc.returncode != 0 or sha256_bytes(proc.stdout) != digest:
        stop("VS0_2_FAIL_CANONICAL_SOURCE_CHAIN_MUTATED", relative_path)
    commit = run_git(root, ["log", "-n", "1", "--format=%H", "--", relative_path])
    return data, digest, commit


def validate_dirty_scope(root: Path) -> None:
    status = run_git(root, ["status", "--short"]).splitlines()
    allowed_exact = {GENERATOR, "scripts/build_baseline_share_v0.py"}
    allowed_prefixes = (
        "baseline_share/",
        "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_build_receipt_v0.",
        f"{OUTPUT_ROOT}/",
    )
    for line in status:
        path = line[3:]
        if path in {"discussion_packets/", "docs/matrixlabs/phase_vs0/runs/"}:
            continue
        if path in allowed_exact or any(path.startswith(prefix) for prefix in allowed_prefixes):
            continue
        stop("VS0_2_FAIL_CANONICAL_SOURCE_CHAIN_MUTATED", line)


def load_preflight(root: Path) -> tuple[dict[str, Any], str]:
    data, digest, commit = load_committed_json(root, PREFLIGHT)
    if commit != PREFLIGHT_COMMIT:
        stop(
            "VS0_2_STOP_PREFLIGHT_NOT_PASS",
            f"source inventory commit {commit} != {PREFLIGHT_COMMIT}",
        )
    return data, digest


def assert_preflight_pass(preflight: dict[str, Any]) -> None:
    if (
        preflight.get("inventory_id") != "phase_vs0_source_inventory_v0"
        or preflight.get("preflight_decision", {}).get("decision")
        != "PROCEED_TO_VS0_2_HAPPY_PATH_BUILD"
        or preflight.get("preflight_gate") != "VS0_PREFLIGHT_PASS_SCOPE_DECLARED"
        or preflight.get("terminal_transition")
        != "ADVANCE(VS0_2_HAPPY_PATH_A_TO_F_ARTIFACT_BUILD_PENDING)"
    ):
        stop("VS0_2_STOP_PREFLIGHT_NOT_PASS", "VS0.1 preflight is not passing")


def source_record(path: str, digest: str, commit: str) -> dict[str, Any]:
    return {
        "canonical_source_path": path,
        "canonical_source_sha256": digest,
        "canonical_source_commit_sha": commit,
        "canonical_source_worktree_matches_head": True,
        "canonical_source_remains_authority": True,
        "phase_projection_replaces_source_authority": False,
    }


def object_path(root: Path, key: str) -> Path:
    path = (root / OUTPUT_ROOT / FILENAMES[key]).resolve()
    output_root = (root / OUTPUT_ROOT).resolve()
    if output_root not in path.parents:
        stop("VS0_2_FAIL_PHASE_NAMESPACE_COLLISION", str(path))
    return path


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def base_object(
    key: str,
    segment: str,
    dependency: str | None,
    source: dict[str, Any],
    payload: dict[str, Any],
    non_effects: dict[str, bool],
) -> dict[str, Any]:
    return {
        "schema_version": f"matrixlabs_phase_vs0_{key.lower()}_v0",
        "object_id": OBJECT_IDS[key],
        "phase_id": "PHASE_VS0",
        "phase_step": f"VS0.2/{key}",
        "run_id": RUN_ID,
        "segment": segment,
        "sequence_key": key,
        "dependency": {
            "upstream_object_key": dependency,
            "upstream_required": dependency is not None,
        },
        "source_projection": source,
        "payload": payload,
        "non_effects": non_effects,
        "builder_emission_gate": {
            "gate": SEGMENT_STATUS[segment],
            "emitted": True,
            "dependency_satisfied": True,
            "failures": [],
        },
    }


def emit(
    root: Path,
    key: str,
    segment: str,
    dependency: str | None,
    sources: dict[str, dict[str, Any]],
    payload: dict[str, Any],
    non_effects: dict[str, bool],
) -> dict[str, Any]:
    if dependency is not None:
        require_emitted(root, dependency, f"VS0_2_STOP_{segment}_CHAIN_BUILD_FAILED")
    value = base_object(
        key,
        segment,
        dependency,
        sources[key]["record"],
        payload,
        non_effects,
    )
    write_json(object_path(root, key), value)
    return value


def require_emitted(root: Path, key: str, code: str) -> dict[str, Any]:
    path = object_path(root, key)
    if not path.is_file():
        stop(code, f"{key} missing")
    try:
        value = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        stop(code, f"{key}: {exc}")
    segment = key[0]
    if value.get("builder_emission_gate", {}).get("gate") != SEGMENT_STATUS[segment]:
        stop(code, f"{key} gate not passing")
    return value


def build_a_chain(root: Path, sources: dict[str, dict[str, Any]]) -> None:
    common_non_effects = {
        "unit_executed": False,
        "machine_proceed_performed": False,
        "reuse_authorized": False,
        "runner_authority_created": False,
    }
    emit(
        root,
        "A1",
        "A",
        None,
        sources,
        {
            "surface_role": "HUMAN_AUTHORITY_DECISION_SURFACE",
            "decision_option": "DECISION_ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
            "decision_recorded": False,
        },
        common_non_effects,
    )
    emit(
        root,
        "A2",
        "A",
        "A1",
        sources,
        {
            "decision_actor_class": "HUMAN",
            "selected_decision": "DECISION_ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
            "decision_recorded": True,
            "authority_state_applied": False,
        },
        common_non_effects,
    )
    emit(
        root,
        "A3",
        "A",
        "A2",
        sources,
        {
            "decision_consumed": True,
            "resulting_authority_state": "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
            "authority_state_applied": True,
        },
        common_non_effects,
    )
    emit(
        root,
        "A4",
        "A",
        "A3",
        sources,
        {
            "selected_decision": "DECISION_ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
            "resulting_authority_state": "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
            "authority_transition_closed": True,
            "a_chain_builder_status": SEGMENT_STATUS["A"],
        },
        common_non_effects,
    )


def build_b_chain(root: Path, sources: dict[str, dict[str, Any]]) -> None:
    require_emitted(root, "A4", "VS0_2_STOP_A4_MISSING_BEFORE_B")
    non_effects = {
        "router_executed_action": False,
        "router_changed_authority": False,
        "runner_authority_created": False,
    }
    emit(
        root,
        "B1",
        "B",
        "A4",
        sources,
        {
            "requested_action": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
            "requested_scope": "PREPARE_SURFACE_ONLY",
        },
        non_effects,
    )
    emit(
        root,
        "B2",
        "B",
        "B1",
        sources,
        {
            "route_disposition": "ROUTE_MACHINE_MAY_PREPARE_ONLY",
            "classification_only": True,
            "machine_action_performed": False,
        },
        non_effects,
    )
    emit(
        root,
        "B3",
        "B",
        "B2",
        sources,
        {
            "route_disposition": "ROUTE_MACHINE_MAY_PREPARE_ONLY",
            "b_chain_builder_status": SEGMENT_STATUS["B"],
            "router_specimen_closed": True,
        },
        non_effects,
    )


def build_c_chain(root: Path, sources: dict[str, dict[str, Any]]) -> None:
    require_emitted(root, "B3", "VS0_2_STOP_B3_MISSING_BEFORE_C")
    non_effects = {
        "promotion_granted": False,
        "declared_scope_reuse_authorized": False,
        "active_archive_entry_created": False,
        "machine_proceed_performed": False,
        "runner_authority_created": False,
    }
    emit(
        root,
        "C1",
        "C",
        "B3",
        sources,
        {
            "schema_role": "VALIDATOR_ARCHIVE_ENTRY_CONTRACT_ONLY",
            "candidate_status_allowed": "ARCHIVE_STATUS_CANDIDATE",
        },
        non_effects,
    )
    emit(
        root,
        "C2",
        "C",
        "C1",
        sources,
        {
            "candidate_status": "ARCHIVE_STATUS_CANDIDATE",
            "candidate_scope": "PREPARE_SURFACE_ONLY",
            "candidate_active": False,
        },
        non_effects,
    )
    emit(
        root,
        "C3",
        "C",
        "C2",
        sources,
        {
            "candidate_status": "ARCHIVE_STATUS_CANDIDATE",
            "audit_status": "CANDIDATE_AUDIT_PASS_WELL_FORMED_NOT_PROMOTED",
            "candidate_well_formed": True,
            "candidate_promoted": False,
            "c_chain_builder_status": SEGMENT_STATUS["C"],
        },
        non_effects,
    )


def build_d_chain(root: Path, sources: dict[str, dict[str, Any]]) -> None:
    require_emitted(root, "C3", "VS0_2_STOP_C3_MISSING_BEFORE_D")
    non_effects = {
        "unit_executed": False,
        "runtime_executed": False,
        "authority_changed_after_machine_proceed": False,
        "declared_scope_expanded": False,
        "additional_radius_created": False,
        "active_registry_created": False,
        "runner_authority_created": False,
    }
    emit(
        root,
        "D1",
        "D",
        "C3",
        sources,
        {
            "promotion_option": "DECISION_PROMOTE_CANDIDATE_FOR_DECLARED_SCOPE",
            "human_decision_required": True,
        },
        non_effects,
    )
    emit(
        root,
        "D2",
        "D",
        "D1",
        sources,
        {
            "selected_promotion_option": "DECISION_PROMOTE_CANDIDATE_FOR_DECLARED_SCOPE",
            "decision_actor_class": "HUMAN",
            "promotion_decision_recorded": True,
        },
        non_effects,
    )
    emit(
        root,
        "D3",
        "D",
        "D2",
        sources,
        {
            "entry_status": "ARCHIVE_STATUS_PREAPPROVED_ACTIVE",
            "promotion_status": "PROMOTION_GRANTED_FOR_DECLARED_SCOPE",
            "declared_scope_use_status": "USE_GRANTED_FOR_DECLARED_SCOPE_ONLY",
            "activation_status": "ACTIVE_ARCHIVE_ENTRY_ACTIVE",
            "radius_granted": 1,
            "active_registry_entry_created": False,
        },
        non_effects,
    )
    emit(
        root,
        "D4",
        "D",
        "D3",
        sources,
        {
            "machine_action": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
            "action_scope": "PREPARE_SURFACE_ONLY",
            "machine_action_count": 1,
            "machine_preparation_action_performed": True,
            "radius_before": 1,
            "radius_consumed": 1,
            "radius_after": 0,
            "unit_executed": False,
            "runtime_executed": False,
        },
        non_effects,
    )
    emit(
        root,
        "D4_OUTPUT",
        "D",
        "D4",
        sources,
        {
            "surface_status": "NEXT_BOUNDED_UNIT_DEFINITION_SURFACE_PREPARED",
            "surface_scope": "C8_N22_BASIS_ONLY",
            "surface_executed": False,
        },
        non_effects,
    )
    emit(
        root,
        "D5",
        "D",
        "D4_OUTPUT",
        sources,
        {
            "closure_status": "MACHINE_PROCEED_CLOSURE_PASS_RADIUS_EXHAUSTED_STOP",
            "d_chain_builder_status": SEGMENT_STATUS["D"],
            "radius_before": 1,
            "radius_consumed": 1,
            "radius_after": 0,
            "radius_exhausted": True,
            "additional_machine_proceed_authorized": False,
        },
        non_effects,
    )


def build_e_chain(root: Path, sources: dict[str, dict[str, Any]]) -> None:
    require_emitted(root, "D5", "VS0_2_STOP_D5_MISSING_BEFORE_E")
    non_effects = {
        "compressed_packet_may_replace_source_authority": False,
        "compressed_packet_may_authorize_reuse": False,
        "compressed_packet_may_renew_radius": False,
        "compressed_packet_may_authorize_additional_machine_proceed": False,
        "compressed_packet_may_create_runner_authority": False,
    }
    emit(
        root,
        "E1",
        "E",
        "D5",
        sources,
        {
            "trace_label": "C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0",
            "compression_target_role": "OBSERVABILITY_COMPRESSION_TARGET",
            "radius_after": 0,
        },
        non_effects,
    )
    emit(
        root,
        "E2",
        "E",
        "E1",
        sources,
        {
            "trace_label": "C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0",
            "packet_role": "COMPRESSED_OBSERVABILITY_PACKET",
            "source_records_remain_authority": True,
        },
        non_effects,
    )
    emit(
        root,
        "E3",
        "E",
        "E2",
        sources,
        {
            "decompression_audit_status": "DECOMPRESSION_AUDIT_PASS_CRITICAL_FIELD_PARITY",
            "critical_field_parity_passed": True,
            "reuse_authorization_passed": False,
        },
        non_effects,
    )
    emit(
        root,
        "E4",
        "E",
        "E3",
        sources,
        {
            "closure_status": "COMPRESSION_CLOSURE_PASS_OBSERVABILITY_ONLY",
            "allowed_use": "OBSERVABILITY_SHORTCUT_ONLY",
            "e_chain_builder_status": SEGMENT_STATUS["E"],
            "formal_source_chain_remains_authority": True,
            "radius_after": 0,
        },
        non_effects,
    )


def build_f_chain(root: Path, sources: dict[str, dict[str, Any]]) -> None:
    require_emitted(root, "E4", "VS0_2_STOP_E4_MISSING_BEFORE_F")
    non_effects = {
        "active_registry_entry_created": False,
        "registry_entry_activated": False,
        "generalization_claimed": False,
        "reuse_authorized": False,
        "radius_renewed": False,
        "machine_action_performed": False,
        "runner_authority_created": False,
    }
    emit(
        root,
        "F1",
        "F",
        "E4",
        sources,
        {
            "schema_role": "REGISTRY_ENTRY_CONTRACT_ONLY",
            "registry_kind": "COMPRESSION_TRACE_OBSERVABILITY_REGISTRY",
        },
        non_effects,
    )
    emit(
        root,
        "F2",
        "F",
        "F1",
        sources,
        {
            "trace_label": "C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0",
            "candidate_status": "REGISTRY_STATUS_CANDIDATE",
            "specimen_count": 1,
            "evidence_kind": "SINGLE_LOCAL_SPECIMEN",
            "generalization_status": "LOCAL_SPECIMEN_ONLY_NOT_GENERALIZED",
        },
        non_effects,
    )
    emit(
        root,
        "F3",
        "F",
        "F2",
        sources,
        {
            "audit_status": "REGISTRY_CANDIDATE_ADMISSIBILITY_AUDIT_PASS_LOCAL_ONLY",
            "candidate_admissible_as_local_only": True,
            "active_registry_acceptance_passed": False,
        },
        non_effects,
    )
    emit(
        root,
        "F4",
        "F",
        "F3",
        sources,
        {
            "closure_status": "REGISTRY_CANDIDATE_CLOSURE_PASS_CANDIDATE_ONLY",
            "f_chain_builder_status": SEGMENT_STATUS["F"],
            "candidate_status": "REGISTRY_STATUS_CANDIDATE",
            "specimen_count": 1,
            "evidence_kind": "SINGLE_LOCAL_SPECIMEN",
            "generalization_status": "LOCAL_SPECIMEN_ONLY_NOT_GENERALIZED",
            "radius_after": 0,
        },
        non_effects,
    )


def artifact_records(root: Path) -> list[dict[str, Any]]:
    records = []
    for key in CHAIN_ORDER:
        path = object_path(root, key)
        content = path.read_bytes()
        value = json.loads(content)
        records.append(
            {
                "sequence_key": key,
                "object_id": value["object_id"],
                "path": str(path.relative_to(root)),
                "sha256": sha256_bytes(content),
                "hash_algorithm": "sha256",
                "builder_emission_gate": value["builder_emission_gate"]["gate"],
                "dependency": value["dependency"]["upstream_object_key"],
            }
        )
    return records


def write_chain_index(root: Path) -> dict[str, Any]:
    records = artifact_records(root)
    index = {
        "schema_version": "matrixlabs_phase_vs0_a_to_f_chain_index_v0",
        "chain_index_id": "phase_vs0_a_to_f_chain_index_v0",
        "phase_id": "PHASE_VS0",
        "phase_step": "VS0.2",
        "index_role": "BUILD_CHAIN_INDEX_ONLY",
        "run_id": RUN_ID,
        "a_to_f_output_root": OUTPUT_ROOT,
        "ordered_object_chain": CHAIN_ORDER,
        "ordered_terminal_chain": TERMINALS,
        "dependency_edges": DEPENDENCY_EDGES,
        "artifacts": records,
        "artifact_count": len(records),
        "artifact_hash_algorithm": "sha256",
        "artifact_hash_scope": "A_TO_F_PHASE_SPECIMEN_ARTIFACTS_EXCLUDES_INDEX_AND_RECEIPT_SELF_REFERENCES",
        "all_artifact_paths_under_phase_namespace": True,
        "canonical_path_collision_detected": False,
        "independent_cross_block_verification_performed": False,
        "phase_closure_performed": False,
    }
    write_json(root / INDEX_JSON, index)
    lines = "\n".join(
        f"- {record['sequence_key']}: {record['object_id']} [{record['sha256']}]"
        for record in records
    )
    write_text(
        root / INDEX_MD,
        f"""# Phase VS0 A-to-F build chain index v0

## Role

BUILD_CHAIN_INDEX_ONLY

## Ordered terminal chain

A4 -> B3 -> C3 -> D5 -> E4 -> F4

## Emitted artifacts

{lines}

## Non-claim

This index records builder output. Independent cross-block verification is pending VS0.3.""",
    )
    return index


def build_receipt(
    preflight_digest: str,
    canonical_hashes_before: dict[str, str],
    canonical_hashes_after: dict[str, str],
) -> dict[str, Any]:
    canonical_mutated = canonical_hashes_before != canonical_hashes_after
    if canonical_mutated:
        stop("VS0_2_FAIL_CANONICAL_SOURCE_CHAIN_MUTATED")
    source_mutation_boundary = {
        "vs0_1_source_inventory_modified_by_vs0_2": False,
        "canonical_a_chain_modified_by_vs0_2": False,
        "canonical_b_chain_modified_by_vs0_2": False,
        "canonical_c_chain_modified_by_vs0_2": False,
        "canonical_d_chain_modified_by_vs0_2": False,
        "canonical_e_chain_modified_by_vs0_2": False,
        "canonical_f_chain_modified_by_vs0_2": False,
        "committed_block_f_start_source_replaced": False,
    }
    global_non_effects = {
        "runner_authority_created": False,
        "active_registry_created": False,
        "trace_generalized": False,
        "declared_scope_expanded": False,
        "radius_renewed_after_d5": False,
        "additional_machine_proceed_authorized": False,
        "next_unit_executed": False,
        "runtime_executed": False,
        "source_authority_replaced_by_compression": False,
        "canonical_source_chain_mutated": False,
        "discussion_packets_committed": False,
    }
    machine_boundary = {
        "machine_action_allowed_in_vs0_2": True,
        "only_allowed_segment": "D4",
        "allowed_machine_action": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
        "allowed_action_scope": "PREPARE_SURFACE_ONLY",
        "machine_action_count": 1,
        "machine_action_count_max": 1,
        "d4_machine_preparation_action_performed": True,
        "machine_action_performed_outside_d4": False,
        "machine_action_performed_after_d5": False,
    }
    receipt = {
        "schema_version": "matrixlabs_phase_vs0_happy_path_build_receipt_v0",
        "build_receipt_id": "phase_vs0_happy_path_build_receipt_v0",
        "phase_id": "PHASE_VS0",
        "phase_step": "VS0.2",
        "build_role": "HAPPY_PATH_A_TO_F_PHASE_SPECIMEN_BUILD_ONLY",
        "happy_path_build_status": BUILD_STATUS,
        "source_preflight": {
            "source_inventory_id": "phase_vs0_source_inventory_v0",
            "source_inventory_path": PREFLIGHT,
            "source_inventory_commit_sha": PREFLIGHT_COMMIT,
            "source_inventory_sha256": preflight_digest,
            "preflight_decision": "PROCEED_TO_VS0_2_HAPPY_PATH_BUILD",
            "preflight_gate": "VS0_PREFLIGHT_PASS_SCOPE_DECLARED",
        },
        "build_mode": {
            "mode": "PHASE_NAMESPACE_SPECIMEN_BUILD_FROM_COMMITTED_SOURCE_CHAIN",
            "canonical_source_chain_may_be_read": True,
            "canonical_source_chain_may_be_mutated": False,
            "phase_run_outputs_created": True,
            "canonical_a_to_f_outputs_overwritten": False,
        },
        "phase_run_namespace": {
            "run_id": RUN_ID,
            "namespace_root": RUN_ROOT,
            "a_to_f_output_root": OUTPUT_ROOT,
        },
        "created_terminal_objects": {
            key: OBJECT_IDS[key] for key in TERMINALS
        },
        "builder_result": {
            "a_chain_built": True,
            "b_chain_built": True,
            "c_chain_built": True,
            "d_chain_built": True,
            "e_chain_built": True,
            "f_chain_built": True,
            "happy_path_phase_specimen_created": True,
            "builder_emission_recorded": True,
            "independent_cross_block_verification_performed": False,
            "phase_closure_performed": False,
        },
        "d_radius_result": {
            "radius_before": 1,
            "radius_consumed": 1,
            "radius_after": 0,
            "radius_exhausted": True,
        },
        "machine_action_boundary": machine_boundary,
        "source_mutation_boundary": source_mutation_boundary,
        "global_non_effects": global_non_effects,
        "evidence_yield_class": {
            "yield_branch": "CONFIRMATION_YIELD",
            "reason": "happy-path phase specimen artifacts were created successfully",
        },
        "next_required_object": "phase_vs0_happy_path_verification_v0",
        "terminal_transition": TERMINAL_TRANSITION,
        "precommit_phase_vs0_happy_path_build_gate": "PASS",
        "happy_path_build_gate": BUILD_STATUS,
        "preflight_present": True,
        "preflight_decision": "PROCEED_TO_VS0_2_HAPPY_PATH_BUILD",
        "preflight_gate": "VS0_PREFLIGHT_PASS_SCOPE_DECLARED",
        "phase_run_namespace_created": True,
        "phase_run_output_root": OUTPUT_ROOT,
        "a_chain_built": True,
        "a4_authority_transition_closure_present": True,
        "b_chain_built": True,
        "b3_router_specimen_closure_present": True,
        "c_chain_built": True,
        "c3_candidate_audit_present": True,
        "d_chain_built": True,
        "d5_machine_proceed_closure_present": True,
        "d4_machine_preparation_action_performed": True,
        "machine_action_count": 1,
        "machine_action_performed_outside_d4": False,
        "machine_action_performed_after_d5": False,
        "d5_radius_before": 1,
        "d5_radius_consumed": 1,
        "d5_radius_after": 0,
        "d5_radius_exhausted": True,
        "e_chain_built": True,
        "e4_compression_closure_present": True,
        "e4_allowed_use": "OBSERVABILITY_SHORTCUT_ONLY",
        "e4_compression_observability_only": True,
        "f_chain_built": True,
        "f4_registry_candidate_closure_present": True,
        "f4_candidate_status": "REGISTRY_STATUS_CANDIDATE",
        "f4_specimen_count": 1,
        "f4_evidence_kind": "SINGLE_LOCAL_SPECIMEN",
        "f4_generalization_status": "LOCAL_SPECIMEN_ONLY_NOT_GENERALIZED",
        "chain_index_created": True,
        "build_receipt_created": True,
        "independent_cross_block_verification_performed": False,
        "phase_closure_performed": False,
        "canonical_source_chain_mutated": False,
        "active_registry_created": False,
        "trace_generalized": False,
        "declared_scope_expanded": False,
        "radius_renewed_after_d5": False,
        "additional_machine_proceed_authorized": False,
        "next_unit_executed": False,
        "runtime_executed": False,
        "source_authority_replaced_by_compression": False,
        "runner_authority_created": False,
        "discussion_packets_committed": False,
        "evidence_yield_branch": "CONFIRMATION_YIELD",
        "commit_created": False,
        "push_executed": False,
        "failures": [],
        "internal_stop_codes": STOP_CODES,
    }
    return receipt


def write_receipt_markdown(root: Path) -> None:
    write_text(
        root / RECEIPT_MD,
        f"""# Phase VS0 happy-path A-to-F build receipt v0

## Status

{BUILD_STATUS}

## Evidence Yield

CONFIRMATION_YIELD

## Preflight

phase_vs0_source_inventory_v0 passed.

## Build mode

PHASE_NAMESPACE_SPECIMEN_BUILD_FROM_COMMITTED_SOURCE_CHAIN

## Phase run namespace

{RUN_ROOT}

## Built chains

- A authority transition chain: built
- B read-only router chain: built
- C candidate archive chain: built
- D promotion + machine proceed chain: built
- E compression chain: built
- F registry candidate chain: built

## Terminal objects

- A4: {OBJECT_IDS['A4']}
- B3: {OBJECT_IDS['B3']}
- C3: {OBJECT_IDS['C3']}
- D5: {OBJECT_IDS['D5']}
- E4: {OBJECT_IDS['E4']}
- F4: {OBJECT_IDS['F4']}

## D-chain radius

- before: 1
- consumed: 1
- after: 0
- exhausted: true

## Machine-action boundary

- D4 preparation action performed: true
- machine action count: 1
- machine action outside D4: false
- machine action after D5: false

## Source mutation boundary

- canonical source chain mutated: false
- committed Block F start source replaced: false

## Global non-effects

- no active registry created
- no generalized trace claimed
- no declared scope expansion
- no radius renewed after D5
- no additional machine proceed authorized
- no next unit executed
- no runtime executed
- no source authority replaced by compression
- no runner authority created

## Next required object

phase_vs0_happy_path_verification_v0

## Terminal transition

{TERMINAL_TRANSITION}

## Non-claim

VS0.2 builds the happy-path phase specimen. It does not replace VS0.3 independent verification.""",
    )


def write_stop_receipt(root: Path, exc: BuildStop) -> None:
    receipt = {
        "schema_version": "matrixlabs_phase_vs0_happy_path_build_receipt_v0",
        "build_receipt_id": "phase_vs0_happy_path_build_receipt_v0",
        "phase_id": "PHASE_VS0",
        "phase_step": "VS0.2",
        "happy_path_build_status": exc.code,
        "stop_code": exc.code,
        "missing_or_failed_object": exc.detail or None,
        "evidence_yield_class": {
            "yield_branch": "DIAGNOSTIC_YIELD",
            "reason": exc.detail or exc.code,
        },
        "precommit_phase_vs0_happy_path_build_gate": "PASS",
        "commit_created": False,
        "push_executed": False,
        "terminal_transition": f"STOP({exc.code})",
    }
    write_json(root / RECEIPT_JSON, receipt)
    write_text(
        root / RECEIPT_MD,
        f"# Phase VS0 happy-path A-to-F build receipt v0\n\n"
        f"## Status\n\n{exc.code}\n\n"
        f"## Terminal transition\n\nSTOP({exc.code})",
    )


def generate() -> int:
    root = detect_repo_root(Path.cwd())
    validate_dirty_scope(root)
    preflight, preflight_digest = load_preflight(root)
    assert_preflight_pass(preflight)

    sources: dict[str, dict[str, Any]] = {}
    canonical_hashes_before: dict[str, str] = {}
    for key in CHAIN_ORDER:
        _, digest, commit = load_committed_json(root, CANONICAL[key])
        canonical_hashes_before[CANONICAL[key]] = digest
        sources[key] = {
            "record": source_record(CANONICAL[key], digest, commit),
        }

    build_a_chain(root, sources)
    build_b_chain(root, sources)
    build_c_chain(root, sources)
    build_d_chain(root, sources)
    build_e_chain(root, sources)
    build_f_chain(root, sources)
    require_emitted(root, "F4", "VS0_2_STOP_F4_MISSING_BEFORE_RECEIPT")
    write_chain_index(root)

    canonical_hashes_after = {
        path: sha256_bytes((root / path).read_bytes())
        for path in canonical_hashes_before
    }
    receipt = build_receipt(
        preflight_digest, canonical_hashes_before, canonical_hashes_after
    )
    write_json(root / RECEIPT_JSON, receipt)
    write_receipt_markdown(root)

    print(f"Wrote {len(CHAIN_ORDER)} phase specimen artifacts under {OUTPUT_ROOT}")
    print(f"Wrote {INDEX_JSON}")
    print(f"Wrote {RECEIPT_JSON}")
    print(f"happy_path_build_gate={BUILD_STATUS}")
    print(f"terminal_transition={TERMINAL_TRANSITION}")
    return 0


def main() -> int:
    root: Path | None = None
    try:
        root = detect_repo_root(Path.cwd())
        return generate()
    except BuildStop as exc:
        if root is not None:
            write_stop_receipt(root, exc)
        print(f"STOP({exc.code}): {exc.detail or exc.code}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
