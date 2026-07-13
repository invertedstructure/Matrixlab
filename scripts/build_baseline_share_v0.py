#!/usr/bin/env python3
"""Generate MatrixLabs Baseline Share Packet v0.

This script emits a portable, uploadable projection under baseline_share/.
The repository remains the source of truth.
"""

from __future__ import annotations

# VS2.6 baseline logical identity exposure v0 START
import atexit as _vs2_6_identity_atexit
import json as _vs2_6_identity_json
from pathlib import Path as _VS2_6_Identity_Path

_VS2_6_CORE_ARTIFACT_ID = (
    "phase_vs2_execution_package_core_manifest_v0"
)

_VS2_6_CORE_LOGICAL_ID = (
    "FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_CORE_V0"
)

_VS2_6_SEAL_ARTIFACT_ID = (
    "phase_vs2_execution_package_readiness_seal_v0"
)

_VS2_6_SEAL_LOGICAL_ID = (
    "FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_READINESS_SEAL_V0"
)

_VS2_6_MD_START = (
    "<!-- VS2_6_LOGICAL_IDENTITY_PROJECTION_START -->"
)

_VS2_6_MD_END = (
    "<!-- VS2_6_LOGICAL_IDENTITY_PROJECTION_END -->"
)


def _vs2_6_upsert_markdown_identity_section(
    current: str,
) -> str:
    section = "\n".join(
        [
            _VS2_6_MD_START,
            "## Phase VS2.6 execution-package identities",
            "",
            "- `execution_package_core_artifact_id`: "
            f"`{_VS2_6_CORE_ARTIFACT_ID}`",
            "- `execution_package_core_id`: "
            f"`{_VS2_6_CORE_LOGICAL_ID}`",
            "- `readiness_seal_artifact_id`: "
            f"`{_VS2_6_SEAL_ARTIFACT_ID}`",
            "- `readiness_seal_id`: "
            f"`{_VS2_6_SEAL_LOGICAL_ID}`",
            _VS2_6_MD_END,
        ]
    )

    if _VS2_6_MD_START in current:
        before, remainder = current.split(
            _VS2_6_MD_START,
            1,
        )

        if _VS2_6_MD_END not in remainder:
            raise RuntimeError(
                "VS2.6 baseline logical identity "
                "projection end marker missing"
            )

        _, after = remainder.split(
            _VS2_6_MD_END,
            1,
        )

        base = before.rstrip() + after

    else:
        base = current

    return base.rstrip() + "\n\n" + section + "\n"


def _apply_vs2_6_baseline_logical_identity_projection_v0(
) -> None:
    root = _VS2_6_Identity_Path(__file__).resolve().parents[1]

    manifest_path = root / "baseline_share/MANIFEST.json"

    manifest = _vs2_6_identity_json.loads(
        manifest_path.read_text(encoding="utf-8")
    )

    if not isinstance(manifest, dict):
        raise RuntimeError(
            "VS2.6 baseline manifest must be an object"
        )

    manifest["phase_vs2_logical_identity_projection"] = {
        "execution_package_core_artifact_id":
            _VS2_6_CORE_ARTIFACT_ID,

        "execution_package_core_id":
            _VS2_6_CORE_LOGICAL_ID,

        "readiness_seal_artifact_id":
            _VS2_6_SEAL_ARTIFACT_ID,

        "readiness_seal_id":
            _VS2_6_SEAL_LOGICAL_ID,
    }

    manifest_path.write_text(
        _vs2_6_identity_json.dumps(
            manifest,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    for relative_path in (
        "baseline_share/CURRENT_STATE.md",
        "baseline_share/COMMIT_CONTEXT.md",
    ):
        target = root / relative_path
        current = target.read_text(encoding="utf-8")

        target.write_text(
            _vs2_6_upsert_markdown_identity_section(
                current
            ),
            encoding="utf-8",
        )


if __name__ == "__main__":
    _vs2_6_identity_atexit.register(
        _apply_vs2_6_baseline_logical_identity_projection_v0
    )
# VS2.6 baseline logical identity exposure v0 END


# VS2.5 baseline human next-unit exposure v0
import atexit as _vs2_5_atexit
from pathlib import Path as _VS2_5_Path

_VS2_5_NEXT_UNIT_ID = (
    "VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS"
)

_VS2_5_NEXT_TRANSITION = (
    "ADVANCE("
    "VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS_PENDING"
    ")"
)


def _apply_vs2_5_human_next_unit_projection_v0() -> None:
    root = _VS2_5_Path(__file__).resolve().parents[1]

    section = "\n".join(
        [
            "## Phase VS2 next lawful unit",
            "",
            "- `next_lawful_unit`: "
            f"`{_VS2_5_NEXT_UNIT_ID}`",
            "- `logical_terminal_transition`: "
            f"`{_VS2_5_NEXT_TRANSITION}`",
        ]
    )

    for relative_path in (
        "baseline_share/CURRENT_STATE.md",
        "baseline_share/COMMIT_CONTEXT.md",
    ):
        target = root / relative_path

        if not target.is_file():
            raise RuntimeError(
                "VS2.5 human baseline projection target missing: "
                f"{target}"
            )

        current = target.read_text(encoding="utf-8")

        if (
            _VS2_5_NEXT_UNIT_ID in current
            and _VS2_5_NEXT_TRANSITION in current
        ):
            continue

        target.write_text(
            current.rstrip()
            + "\n\n"
            + section
            + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    _vs2_5_atexit.register(
        _apply_vs2_5_human_next_unit_projection_v0
    )


import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
# BASELINE_UNCOMMITTED_VS0_3_MARKER_FILTER_V1
#
# Baseline is allowed to mention the next required object
# "phase_vs0_happy_path_verification_v0" as a VS0.2 handoff.
# It must not project uncommitted VS0.3 implementation/diagnostic file paths
# or the prior VS0.3 diagnostic fail code while those files are not tracked.
def _baseline_filter_uncommitted_vs0_3_markers_v1() -> None:
    from pathlib import Path as _Path

    verification_path = _Path(
        "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_verification_v0.json"
    )
    if verification_path.is_file():
        try:
            verification = json.loads(verification_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            verification = {}
        if (
            verification.get("verification_result", {}).get(
                "happy_path_verification_status"
            )
            == "VS0_3_HAPPY_PATH_VERIFICATION_PASS_A_TO_F_PHASE_SPECIMEN_VERIFIED"
        ):
            return

    baseline_root = _Path("baseline_share")
    if not baseline_root.exists():
        return

    forbidden_markers = [
        "VS0_3_FAIL_CHAIN_INDEX_HASH_MISMATCH",
        "scripts/verify_phase_vs0_happy_path_v0.py",
        "phase_vs0_happy_path_verification_v0.json",
        "phase_vs0_happy_path_verification_v0.md",
        "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_verification_v0.json",
        "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_verification_v0.md",
    ]

    for file_path in baseline_root.rglob("*"):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in {".md", ".json", ".txt"}:
            continue

        original = file_path.read_text(errors="ignore")
        filtered_lines = []
        removed = False

        for line in original.splitlines():
            if any(marker in line for marker in forbidden_markers):
                removed = True
                continue
            filtered_lines.append(line)

        if removed:
            file_path.write_text("\n".join(filtered_lines).rstrip() + "\n")


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
C8_N22_AUTHORITY_BOUNDARY_READABOUT_DOCS = [
    "docs/matrixlabs/readabouts/c8_n22_authority_boundary_readabout_v0.json",
    "docs/matrixlabs/readabouts/c8_n22_authority_boundary_readabout_v0.md",
]
C8_N22_AUTHORITY_BOUNDARY_READABOUT_GENERATOR = "scripts/build_c8_n22_authority_boundary_readabout_v0.py"
C8_N22_HUMAN_DECISION_SURFACE_DOCS = [
    "docs/matrixlabs/decision_surfaces/c8_n22_human_decision_surface_v0.json",
    "docs/matrixlabs/decision_surfaces/c8_n22_human_decision_surface_v0.md",
]
C8_N22_HUMAN_DECISION_SURFACE_GENERATOR = "scripts/build_c8_n22_human_decision_surface_v0.py"
C8_N22_HUMAN_DECISION_RECEIPT_DOCS = [
    "docs/matrixlabs/decisions/c8_n22_human_decision_receipt_v0.json",
    "docs/matrixlabs/decisions/c8_n22_human_decision_receipt_v0.md",
]
C8_N22_HUMAN_DECISION_RECEIPT_GENERATOR = "scripts/build_c8_n22_human_decision_receipt_v0.py"
C8_N22_AUTHORITY_STATE_UPDATE_DOCS = [
    "docs/matrixlabs/boundary/c8_n22_authority_state_update_v0.json",
    "docs/matrixlabs/boundary/c8_n22_authority_state_update_v0.md",
]
C8_N22_AUTHORITY_STATE_UPDATE_GENERATOR = "scripts/build_c8_n22_authority_state_update_v0.py"
C8_N22_AUTHORITY_TRANSITION_CLOSURE_DOCS = [
    "docs/matrixlabs/boundary/c8_n22_authority_transition_closure_v0.json",
    "docs/matrixlabs/boundary/c8_n22_authority_transition_closure_v0.md",
]
C8_N22_AUTHORITY_TRANSITION_CLOSURE_GENERATOR = "scripts/build_c8_n22_authority_transition_closure_v0.py"
C8_N22_REQUESTED_ACTION_DOCS = [
    "docs/matrixlabs/router/c8_n22_requested_action_prepare_next_unit_definition_surface_v0.json",
    "docs/matrixlabs/router/c8_n22_requested_action_prepare_next_unit_definition_surface_v0.md",
]
C8_N22_REQUESTED_ACTION_GENERATOR = "scripts/build_c8_n22_requested_action_prepare_next_unit_definition_surface_v0.py"
C8_N22_AUTHORITY_ROUTE_CLASSIFICATION_DOCS = [
    "docs/matrixlabs/router/c8_n22_authority_route_classification_v0.json",
    "docs/matrixlabs/router/c8_n22_authority_route_classification_v0.md",
]
C8_N22_AUTHORITY_ROUTE_CLASSIFICATION_GENERATOR = "scripts/build_c8_n22_authority_route_classification_v0.py"
C8_N22_READ_ONLY_ROUTER_SPECIMEN_CLOSURE_DOCS = [
    "docs/matrixlabs/router/c8_n22_read_only_router_specimen_closure_v0.json",
    "docs/matrixlabs/router/c8_n22_read_only_router_specimen_closure_v0.md",
]
C8_N22_READ_ONLY_ROUTER_SPECIMEN_CLOSURE_GENERATOR = "scripts/build_c8_n22_read_only_router_specimen_closure_v0.py"
VALIDATOR_ARCHIVE_SCHEMA_CONTRACT_DOCS = [
    "docs/matrixlabs/validator_archive/validator_archive_entry_schema_contract_v0.json",
    "docs/matrixlabs/validator_archive/validator_archive_entry_schema_contract_v0.md",
]
VALIDATOR_ARCHIVE_SCHEMA_CONTRACT_GENERATOR = "scripts/build_validator_archive_entry_schema_contract_v0.py"
C8_N22_CANDIDATE_ARCHIVE_ENTRY_DOCS = [
    "docs/matrixlabs/validator_archive/candidates/c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.json",
    "docs/matrixlabs/validator_archive/candidates/c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.md",
]
C8_N22_CANDIDATE_ARCHIVE_ENTRY_GENERATOR = "scripts/build_c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.py"
C8_N22_CANDIDATE_ARCHIVE_ADMISSIBILITY_AUDIT_DOCS = [
    "docs/matrixlabs/validator_archive/audits/c8_n22_candidate_archive_entry_admissibility_audit_v0.json",
    "docs/matrixlabs/validator_archive/audits/c8_n22_candidate_archive_entry_admissibility_audit_v0.md",
]
C8_N22_CANDIDATE_ARCHIVE_ADMISSIBILITY_AUDIT_GENERATOR = "scripts/build_c8_n22_candidate_archive_entry_admissibility_audit_v0.py"
C8_N22_CANDIDATE_PROMOTION_DECISION_SURFACE_DOCS = [
    "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_surface_v0.json",
    "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_surface_v0.md",
]
C8_N22_CANDIDATE_PROMOTION_DECISION_SURFACE_GENERATOR = "scripts/build_c8_n22_candidate_promotion_decision_surface_v0.py"
C8_N22_CANDIDATE_PROMOTION_DECISION_RECEIPT_DOCS = [
    "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_receipt_v0.json",
    "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_receipt_v0.md",
]
C8_N22_CANDIDATE_PROMOTION_DECISION_RECEIPT_GENERATOR = "scripts/build_c8_n22_candidate_promotion_decision_receipt_v0.py"
C8_N22_ACTIVE_ARCHIVE_ENTRY_DOCS = [
    "docs/matrixlabs/validator_archive/active/c8_n22_prepare_next_unit_definition_active_archive_entry_v0.json",
    "docs/matrixlabs/validator_archive/active/c8_n22_prepare_next_unit_definition_active_archive_entry_v0.md",
]
C8_N22_ACTIVE_ARCHIVE_ENTRY_GENERATOR = "scripts/build_c8_n22_prepare_next_unit_definition_active_archive_entry_v0.py"
C8_N22_MACHINE_PROCEED_DOCS = [
    "docs/matrixlabs/proceed/c8_n22_prepare_next_unit_definition_surface_machine_proceed_v0.json",
    "docs/matrixlabs/proceed/c8_n22_prepare_next_unit_definition_surface_machine_proceed_v0.md",
]
C8_N22_UNIT_SURFACE_DOCS = [
    "docs/matrixlabs/unit_surfaces/c8_n22_next_bounded_unit_definition_surface_v0.json",
    "docs/matrixlabs/unit_surfaces/c8_n22_next_bounded_unit_definition_surface_v0.md",
]
C8_N22_MACHINE_PROCEED_GENERATOR = "scripts/build_c8_n22_prepare_next_unit_definition_surface_machine_proceed_v0.py"
C8_N22_MACHINE_PROCEED_CLOSURE_DOCS = [
    "docs/matrixlabs/proceed/c8_n22_machine_proceed_closure_v0.json",
    "docs/matrixlabs/proceed/c8_n22_machine_proceed_closure_v0.md",
]
C8_N22_MACHINE_PROCEED_CLOSURE_GENERATOR = "scripts/build_c8_n22_machine_proceed_closure_v0.py"
C8_N22_COMPRESSION_TARGET_DOCS = [
    "docs/matrixlabs/compression/c8_n22_authority_action_trace_compression_target_v0.json",
    "docs/matrixlabs/compression/c8_n22_authority_action_trace_compression_target_v0.md",
]
C8_N22_COMPRESSION_TARGET_GENERATOR = "scripts/build_c8_n22_authority_action_trace_compression_target_v0.py"
C8_N22_COMPRESSED_PACKET_DOCS = [
    "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_compressed_packet_v0.json",
    "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_compressed_packet_v0.md",
]
C8_N22_COMPRESSED_PACKET_GENERATOR = "scripts/build_c8_n22_radius_bound_prepare_trace_compressed_packet_v0.py"
C8_N22_DECOMPRESSION_AUDIT_DOCS = [
    "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_decompression_audit_v0.json",
    "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_decompression_audit_v0.md",
]
C8_N22_DECOMPRESSION_AUDIT_GENERATOR = "scripts/build_c8_n22_radius_bound_prepare_trace_decompression_audit_v0.py"
C8_N22_COMPRESSION_CLOSURE_DOCS = [
    "docs/matrixlabs/compression/c8_n22_compression_specimen_closure_v0.json",
    "docs/matrixlabs/compression/c8_n22_compression_specimen_closure_v0.md",
]
C8_N22_COMPRESSION_CLOSURE_GENERATOR = "scripts/build_c8_n22_compression_specimen_closure_v0.py"
COMPRESSION_TRACE_REGISTRY_SCHEMA_CONTRACT_DOCS = [
    "docs/matrixlabs/registry/compression_trace_registry_entry_schema_contract_v0.json",
    "docs/matrixlabs/registry/compression_trace_registry_entry_schema_contract_v0.md",
]
COMPRESSION_TRACE_REGISTRY_SCHEMA_CONTRACT_GENERATOR = "scripts/build_compression_trace_registry_entry_schema_contract_v0.py"
C8_N22_TRACE_REGISTRY_CANDIDATE_DOCS = [
    "docs/matrixlabs/registry/candidates/c8_n22_radius_bound_prepare_trace_registry_candidate_v0.json",
    "docs/matrixlabs/registry/candidates/c8_n22_radius_bound_prepare_trace_registry_candidate_v0.md",
]
C8_N22_TRACE_REGISTRY_CANDIDATE_GENERATOR = "scripts/build_c8_n22_radius_bound_prepare_trace_registry_candidate_v0.py"
C8_N22_TRACE_REGISTRY_CANDIDATE_AUDIT_DOCS = [
    "docs/matrixlabs/registry/audits/c8_n22_radius_bound_prepare_trace_registry_candidate_audit_v0.json",
    "docs/matrixlabs/registry/audits/c8_n22_radius_bound_prepare_trace_registry_candidate_audit_v0.md",
]
C8_N22_TRACE_REGISTRY_CANDIDATE_AUDIT_GENERATOR = "scripts/build_c8_n22_radius_bound_prepare_trace_registry_candidate_audit_v0.py"
C8_N22_TRACE_REGISTRY_CANDIDATE_CLOSURE_DOCS = [
    "docs/matrixlabs/registry/closures/c8_n22_radius_bound_prepare_trace_registry_candidate_closure_v0.json",
    "docs/matrixlabs/registry/closures/c8_n22_radius_bound_prepare_trace_registry_candidate_closure_v0.md",
]
C8_N22_TRACE_REGISTRY_CANDIDATE_CLOSURE_GENERATOR = "scripts/build_c8_n22_radius_bound_prepare_trace_registry_candidate_closure_v0.py"
PHASE_VS0_SOURCE_INVENTORY_DOCS = [
    "docs/matrixlabs/phase_vs0/phase_vs0_source_inventory_v0.json",
    "docs/matrixlabs/phase_vs0/phase_vs0_source_inventory_v0.md",
]
PHASE_VS0_SOURCE_INVENTORY_GENERATOR = "scripts/build_phase_vs0_source_inventory_v0.py"
PHASE_VS0_HAPPY_PATH_BUILD_DOCS = [
    "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_build_receipt_v0.json",
    "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_build_receipt_v0.md",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/phase_vs0_a_to_f_chain_index_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/phase_vs0_a_to_f_chain_index_v0.md",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/a1_human_decision_surface_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/a2_human_decision_receipt_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/a3_authority_state_update_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/a4_authority_transition_closure_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/b1_requested_action_prepare_next_unit_definition_surface_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/b2_authority_route_classification_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/b3_router_specimen_closure_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/c1_validator_archive_entry_schema_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/c2_candidate_archive_entry_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/c3_candidate_archive_admissibility_audit_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/d1_candidate_promotion_decision_surface_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/d2_candidate_promotion_decision_receipt_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/d3_active_archive_entry_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/d4_machine_proceed_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/d4_next_bounded_unit_definition_surface_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/d5_machine_proceed_closure_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/e1_compression_target_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/e2_compressed_packet_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/e3_decompression_audit_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/e4_compression_specimen_closure_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/f1_registry_entry_schema_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/f2_registry_candidate_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/f3_registry_candidate_audit_v0.json",
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f/f4_registry_candidate_closure_projection_v0.json",
]
PHASE_VS0_HAPPY_PATH_BUILD_GENERATOR = "scripts/build_phase_vs0_a_to_f_first_specimen_v0.py"
PHASE_VS0_HAPPY_PATH_VERIFICATION_DOCS = [
    "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_verification_v0.json",
    "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_verification_v0.md",
]
PHASE_VS0_HAPPY_PATH_VERIFICATION_SCRIPT = "scripts/verify_phase_vs0_happy_path_v0.py"
PHASE_VS0_NEGATIVE_PROBE_ROOT = (
    "docs/matrixlabs/phase_vs0/runs/"
    "phase_vs0_first_specimen_runtime_v0/negative_probes"
)
PHASE_VS0_NEGATIVE_PROBE_DOCS = [
    f"{PHASE_VS0_NEGATIVE_PROBE_ROOT}/phase_vs0_negative_probe_definitions_v0.json",
    f"{PHASE_VS0_NEGATIVE_PROBE_ROOT}/phase_vs0_negative_probe_battery_v0.json",
    f"{PHASE_VS0_NEGATIVE_PROBE_ROOT}/phase_vs0_negative_probe_battery_v0.md",
    f"{PHASE_VS0_NEGATIVE_PROBE_ROOT}/receipts/neg01_d4_without_active_entry_v0.json",
    f"{PHASE_VS0_NEGATIVE_PROBE_ROOT}/receipts/neg02_d4_with_radius_zero_v0.json",
    f"{PHASE_VS0_NEGATIVE_PROBE_ROOT}/receipts/neg03_e2_without_e1_target_v0.json",
    f"{PHASE_VS0_NEGATIVE_PROBE_ROOT}/receipts/neg04_e3_with_dropped_radius_field_v0.json",
    f"{PHASE_VS0_NEGATIVE_PROBE_ROOT}/receipts/neg05_e4_with_failed_decompression_audit_v0.json",
    f"{PHASE_VS0_NEGATIVE_PROBE_ROOT}/receipts/neg06_f2_without_e4_closure_v0.json",
    f"{PHASE_VS0_NEGATIVE_PROBE_ROOT}/receipts/neg07_f2_with_specimen_count_overclaim_v0.json",
    f"{PHASE_VS0_NEGATIVE_PROBE_ROOT}/receipts/neg08_f3_with_generalization_claimed_v0.json",
    f"{PHASE_VS0_NEGATIVE_PROBE_ROOT}/receipts/neg09_f4_with_active_registry_created_v0.json",
    f"{PHASE_VS0_NEGATIVE_PROBE_ROOT}/receipts/neg10_any_with_runner_authority_true_v0.json",
]
PHASE_VS0_NEGATIVE_PROBE_SCRIPT = (
    "scripts/run_phase_vs0_negative_probe_battery_v0.py"
)
PHASE_VS0_EVIDENCE_YIELD_REPORT_DOCS = [
    "docs/matrixlabs/phase_vs0/phase_vs0_evidence_yield_report_v0.json",
    "docs/matrixlabs/phase_vs0/phase_vs0_evidence_yield_report_v0.md",
]
PHASE_VS0_EVIDENCE_YIELD_REPORT_SCRIPT = (
    "scripts/build_phase_vs0_evidence_yield_report_v0.py"
)
PHASE_VS0_CLOSURE_DOCS = [
    "docs/matrixlabs/phase_vs0/phase_vs0_closure_v0.json",
    "docs/matrixlabs/phase_vs0/phase_vs0_closure_v0.md",
]
PHASE_VS0_CLOSURE_SCRIPT = "scripts/close_phase_vs0_v0.py"
POST_VS0_DIRECTION_DECISION_RECEIPT_DOCS = [
    "docs/matrixlabs/phase_vs1/post_vs0_direction_decision_receipt_v0.json",
    "docs/matrixlabs/phase_vs1/post_vs0_direction_decision_receipt_v0.md",
]
POST_VS0_DIRECTION_DECISION_RECEIPT_SCRIPT = (
    "scripts/build_post_vs0_direction_decision_receipt_v0.py"
)
PHASE_VS1_SOURCE_INTAKE_DOCS = [
    "docs/matrixlabs/phase_vs1/phase_vs1_post_vs0_source_intake_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_post_vs0_source_intake_v0.md",
]
PHASE_VS1_SOURCE_INTAKE_SCRIPT = (
    "scripts/build_phase_vs1_post_vs0_source_intake_v0.py"
)
PHASE_VS1_CONTROLLED_LOOP_CONTRACT_DOCS = [
    "docs/matrixlabs/phase_vs1/phase_vs1_controlled_convergence_loop_contract_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_controlled_convergence_loop_contract_v0.md",
]
PHASE_VS1_CONTROLLED_LOOP_CONTRACT_SCRIPT = (
    "scripts/build_phase_vs1_controlled_convergence_loop_contract_v0.py"
)
PHASE_VS1_CONTROLLED_LOOP_PRECONDITION_INVENTORY_DOCS = [
    "docs/matrixlabs/phase_vs1/phase_vs1_controlled_loop_precondition_inventory_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_controlled_loop_precondition_inventory_v0.md",
]
PHASE_VS1_CONTROLLED_LOOP_PRECONDITION_INVENTORY_SCRIPT = (
    "scripts/build_phase_vs1_controlled_loop_precondition_inventory_v0.py"
)
PHASE_VS1_CONTROLLED_LOOP_READINESS_AUDIT_DOCS = [
    "docs/matrixlabs/phase_vs1/phase_vs1_controlled_loop_readiness_audit_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_controlled_loop_readiness_audit_v0.md",
]
PHASE_VS1_CONTROLLED_LOOP_READINESS_AUDIT_SCRIPT = (
    "scripts/build_phase_vs1_controlled_loop_readiness_audit_v0.py"
)
PHASE_VS1_MISSING_PRECONDITION_NEXT_SURFACE_MAP_DOCS = [
    "docs/matrixlabs/phase_vs1/phase_vs1_missing_precondition_next_surface_map_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_missing_precondition_next_surface_map_v0.md",
]
PHASE_VS1_MISSING_PRECONDITION_NEXT_SURFACE_MAP_SCRIPT = (
    "scripts/build_phase_vs1_missing_precondition_next_surface_map_v0.py"
)
PHASE_VS1_CLOSURE_DOCS = [
    "docs/matrixlabs/phase_vs1/phase_vs1_closure_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_closure_v0.md",
]
PHASE_VS1_CLOSURE_SCRIPT = "scripts/close_phase_vs1_v0.py"
POST_VS1_DIRECTION_SURFACE_DOCS = [
    "docs/matrixlabs/post_vs1/post_vs1_direction_decision_surface_v0.json",
    "docs/matrixlabs/post_vs1/post_vs1_direction_decision_surface_v0.md",
    "docs/matrixlabs/post_vs1/sources/matrixlab_first_sweep_capable_kernel_target_specification_v0.md",
    "docs/matrixlabs/post_vs1/sources/matrixlab_first_sweep_capable_kernel_target_specification_v0.source.json",
]
POST_VS1_DIRECTION_SURFACE_SCRIPT = (
    "scripts/build_post_vs1_direction_decision_surface_v0.py"
)
POST_VS1_DIRECTION_RECEIPT_DOCS = [
    "docs/matrixlabs/post_vs1/post_vs1_direction_decision_receipt_v0.json",
    "docs/matrixlabs/post_vs1/post_vs1_direction_decision_receipt_v0.md",
]
POST_VS1_DIRECTION_RECEIPT_SCRIPT = (
    "scripts/build_post_vs1_direction_decision_receipt_v0.py"
)
POST_VS1_DIRECTION_AUTHORITY_UPDATE_DOCS = [
    "docs/matrixlabs/post_vs1/post_vs1_direction_authority_update_v0.json",
    "docs/matrixlabs/post_vs1/post_vs1_direction_authority_update_v0.md",
]
POST_VS1_DIRECTION_AUTHORITY_UPDATE_SCRIPT = (
    "scripts/build_post_vs1_direction_authority_update_v0.py"
)
POST_VS1_DIRECTION_TRANSITION_CLOSURE_DOCS = [
    "docs/matrixlabs/post_vs1/post_vs1_direction_transition_closure_v0.json",
    "docs/matrixlabs/post_vs1/post_vs1_direction_transition_closure_v0.md",
]
POST_VS1_DIRECTION_TRANSITION_CLOSURE_SCRIPT = (
    "scripts/build_post_vs1_direction_transition_closure_v0.py"
)
PHASE_VS2_1_POST_VS1_SOURCE_INTAKE_DOCS = [
    "docs/matrixlabs/phase_vs2/phase_vs2_post_vs1_source_intake_v0.json",
    "docs/matrixlabs/phase_vs2/phase_vs2_post_vs1_source_intake_v0.md",
    "docs/matrixlabs/phase_vs2/phase_vs2_1_post_vs1_source_intake_receipt_v0.json",
]
PHASE_VS2_1_POST_VS1_SOURCE_INTAKE_SCRIPT = (
    "scripts/build_phase_vs2_1_post_vs1_source_intake_v0.py"
)
PHASE_VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_DOCS = [
    "docs/matrixlabs/phase_vs2/phase_vs2_first_sweep_capable_kernel_profile_v0.json",
    "docs/matrixlabs/phase_vs2/phase_vs2_first_sweep_capable_kernel_profile_v0.md",
    "docs/matrixlabs/phase_vs2/phase_vs2_typed_state_contract_convergence_target_freeze_v0.json",
    "docs/matrixlabs/phase_vs2/phase_vs2_typed_state_contract_convergence_target_freeze_v0.md",
    "docs/matrixlabs/phase_vs2/phase_vs2_2_kernel_profile_and_target_freeze_receipt_v0.json",
]
PHASE_VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_SCRIPT = (
    "scripts/build_phase_vs2_2_kernel_profile_and_target_freeze_v0.py"
)
PHASE_VS2_3_SCOPE_REGIME_OBJECT_MODEL_DOCS = [
    "docs/matrixlabs/phase_vs2/object_model/phase_vs2_scope_regime_contract_v0.json",
    "docs/matrixlabs/phase_vs2/object_model/phase_vs2_scope_regime_contract_v0.md",
    "docs/matrixlabs/phase_vs2/object_model/phase_vs2_runtime_control_state_contract_v0.json",
    "docs/matrixlabs/phase_vs2/object_model/phase_vs2_runtime_control_state_contract_v0.md",
    "docs/matrixlabs/phase_vs2/object_model/phase_vs2_candidate_typed_state_contract_schema_v0.json",
    "docs/matrixlabs/phase_vs2/object_model/phase_vs2_candidate_typed_state_contract_schema_v0.md",
    "docs/matrixlabs/phase_vs2/object_model/phase_vs2_frozen_target_contract_v0.json",
    "docs/matrixlabs/phase_vs2/object_model/phase_vs2_frozen_target_contract_v0.md",
    "docs/matrixlabs/phase_vs2/object_model/phase_vs2_object_model_binding_manifest_v0.json",
    "docs/matrixlabs/phase_vs2/object_model/phase_vs2_object_model_binding_manifest_v0.md",
    "docs/matrixlabs/phase_vs2/phase_vs2_3_scope_regime_and_three_object_model_definition_receipt_v0.json",
]
PHASE_VS2_3_SCOPE_REGIME_OBJECT_MODEL_SCRIPT = (
    "scripts/build_phase_vs2_3_scope_regime_and_three_object_model_definition_v0.py"
)
PHASE_VS2_3_SCOPE_REGIME_OBJECT_MODEL_VERIFY_SCRIPT = (
    "scripts/verify_phase_vs2_3_scope_regime_and_three_object_model_definition_v0.py"
)
PHASE_VS2_4_MOVE_SPACE_DOCS = [
    "docs/matrixlabs/phase_vs2/move_space/phase_vs2_source_and_version_binding_contract_v0.json",
    "docs/matrixlabs/phase_vs2/move_space/phase_vs2_source_and_version_binding_contract_v0.md",
    "docs/matrixlabs/phase_vs2/move_space/phase_vs2_move_vocabulary_partition_v0.json",
    "docs/matrixlabs/phase_vs2/move_space/phase_vs2_move_vocabulary_partition_v0.md",
    "docs/matrixlabs/phase_vs2/move_space/phase_vs2_move_authority_matrix_v0.json",
    "docs/matrixlabs/phase_vs2/move_space/phase_vs2_move_authority_matrix_v0.md",
    "docs/matrixlabs/phase_vs2/move_space/phase_vs2_finite_move_space_v0.json",
    "docs/matrixlabs/phase_vs2/move_space/phase_vs2_finite_move_space_v0.md",
    "docs/matrixlabs/phase_vs2/move_space/phase_vs2_prospective_controlled_step_authority_envelope_v0.json",
    "docs/matrixlabs/phase_vs2/move_space/phase_vs2_prospective_controlled_step_authority_envelope_v0.md",
    "docs/matrixlabs/phase_vs2/move_space/phase_vs2_move_space_binding_manifest_v0.json",
    "docs/matrixlabs/phase_vs2/move_space/phase_vs2_move_space_binding_manifest_v0.md",
    "docs/matrixlabs/phase_vs2/phase_vs2_4_finite_move_space_source_and_authority_freeze_receipt_v0.json",
]
PHASE_VS2_4_MOVE_SPACE_SCRIPT = (
    "scripts/build_phase_vs2_4_finite_move_space_source_and_authority_freeze_v0.py"
)
PHASE_VS2_4_MOVE_SPACE_VERIFY_SCRIPT = (
    "scripts/verify_phase_vs2_4_finite_move_space_source_and_authority_freeze_v0.py"
)
PHASE_VS2_5_CONTROLLED_STEP_DOCS = [
    "docs/matrixlabs/phase_vs2/controlled_step/phase_vs2_controlled_step_and_convergence_contract_package_v0.json",
    "docs/matrixlabs/phase_vs2/controlled_step/phase_vs2_controlled_step_and_convergence_contract_package_v0.md",
    "docs/matrixlabs/phase_vs2/controlled_step/phase_vs2_convergence_criterion_contract_v0.json",
    "docs/matrixlabs/phase_vs2/controlled_step/phase_vs2_convergence_criterion_contract_v0.md",
    "docs/matrixlabs/phase_vs2/controlled_step/phase_vs2_receipt_and_atomic_publication_contract_v0.json",
    "docs/matrixlabs/phase_vs2/controlled_step/phase_vs2_receipt_and_atomic_publication_contract_v0.md",
    "docs/matrixlabs/phase_vs2/controlled_step/phase_vs2_controlled_step_binding_manifest_v0.json",
    "docs/matrixlabs/phase_vs2/controlled_step/phase_vs2_controlled_step_binding_manifest_v0.md",
    "docs/matrixlabs/phase_vs2/phase_vs2_5_controlled_step_and_convergence_contract_construction_receipt_v0.json",
]
PHASE_VS2_5_CONTROLLED_STEP_SCRIPT = (
    "scripts/build_phase_vs2_5_controlled_step_and_convergence_contract_construction_v0.py"
)
PHASE_VS2_5_CONTROLLED_STEP_VERIFY_SCRIPT = (
    "scripts/verify_phase_vs2_5_controlled_step_and_convergence_contract_construction_v0.py"
)
PHASE_VS2_6_FIXTURES_REPORTS_READINESS_DOCS = [
    "docs/matrixlabs/phase_vs2/fixtures/phase_vs2_first_kernel_fixture_contract_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/phase_vs2_first_kernel_fixture_contract_v0.md",
    "docs/matrixlabs/phase_vs2/fixtures/phase_vs2_first_kernel_fixture_set_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/phase_vs2_first_kernel_fixture_set_v0.md",
    "docs/matrixlabs/phase_vs2/fixtures/candidates/F01_candidate_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/candidates/F02_candidate_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/candidates/F03_candidate_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/candidates/F04_candidate_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/candidates/F05_candidate_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/candidates/F06_candidate_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/candidates/F07_candidate_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/candidates/F08_candidate_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/candidates/F09_candidate_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/candidates/F10_candidate_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/definitions/F01_positive_required_field_and_normalization_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/definitions/F02_already_valid_preservation_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/definitions/F03_repairable_typed_value_normalization_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/definitions/F04_repairable_source_identity_binding_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/definitions/F05_missing_source_blocker_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/definitions/F06_authority_overreach_blocker_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/definitions/F07_repairable_prohibited_candidate_declaration_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/definitions/F08_missing_schema_blocker_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/definitions/F09_missing_capability_blocker_v0.json",
    "docs/matrixlabs/phase_vs2/fixtures/definitions/F10_no_admissible_move_gap_v0.json",
    "docs/matrixlabs/phase_vs2/readiness/phase_vs2_upstream_package_dependency_inventory_v0.json",
    "docs/matrixlabs/phase_vs2/readiness/phase_vs2_first_kernel_runtime_source_snapshot_v0.json",
    "docs/matrixlabs/phase_vs2/readiness/phase_vs2_execution_package_core_manifest_v0.json",
    "docs/matrixlabs/phase_vs2/readiness/phase_vs2_execution_package_core_manifest_v0.md",
    "docs/matrixlabs/phase_vs2/readiness/phase_vs2_first_run_construction_readiness_gate_v0.json",
    "docs/matrixlabs/phase_vs2/readiness/phase_vs2_first_run_construction_readiness_gate_v0.md",
    "docs/matrixlabs/phase_vs2/readiness/phase_vs2_first_run_construction_readiness_gate_receipt_v0.json",
    "docs/matrixlabs/phase_vs2/readiness/phase_vs2_execution_package_readiness_seal_v0.json",
    "docs/matrixlabs/phase_vs2/readiness/phase_vs2_execution_package_readiness_seal_v0.md",
    "docs/matrixlabs/phase_vs2/reports/phase_vs2_case_report_contract_v0.json",
    "docs/matrixlabs/phase_vs2/reports/phase_vs2_sweep_report_contract_v0.json",
    "docs/matrixlabs/phase_vs2/reports/phase_vs2_evidence_yield_contract_v0.json",
    "docs/matrixlabs/phase_vs2/reports/phase_vs2_unexpected_outcome_contract_v0.json",
    "docs/matrixlabs/phase_vs2/reports/phase_vs2_refinement_candidate_contract_v0.json",
    "docs/matrixlabs/phase_vs2/reports/phase_vs2_report_contract_package_v0.json",
    "docs/matrixlabs/phase_vs2/reports/phase_vs2_report_contract_package_v0.md",
    "docs/matrixlabs/phase_vs2/phase_vs2_6_fixtures_reports_and_first_run_construction_readiness_receipt_v0.json",
]
PHASE_VS2_6_FIXTURES_REPORTS_READINESS_SCRIPT = (
    "scripts/build_phase_vs2_6_fixtures_reports_and_first_run_construction_readiness_v0.py"
)
PHASE_VS2_6_FIXTURES_REPORTS_READINESS_VERIFY_SCRIPT = (
    "scripts/verify_phase_vs2_6_fixtures_reports_and_first_run_construction_readiness_v0.py"
)
PHASE_VS2_7_PHASE_CLOSURE_DOCS = [
    "docs/matrixlabs/phase_vs2/phase_vs2_closure_v0.json",
    "docs/matrixlabs/phase_vs2/phase_vs2_closure_v0.md",
    "docs/matrixlabs/phase_vs2/phase_vs2_closure_readout_v0.md",
    "docs/matrixlabs/phase_vs2/phase_vs2_7_phase_closure_receipt_v0.json",
]
PHASE_VS2_7_PHASE_CLOSURE_SCRIPT = "scripts/build_phase_vs2_7_phase_closure_v0.py"
PHASE_VS2_7_PHASE_CLOSURE_VERIFY_SCRIPT = "scripts/verify_phase_vs2_7_phase_closure_v0.py"
POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_DOCS = [
    "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_v0.json",
    "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_v0.md",
    "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_receipt_v0.json",
]
POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_SCRIPT = (
    "scripts/build_post_vs2_first_execution_decision_surface_v0.py"
)
POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_VERIFY_SCRIPT = (
    "scripts/verify_post_vs2_first_execution_decision_surface_v0.py"
)
POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_DOCS = [
    "docs/matrixlabs/post_vs2/post_vs2_first_execution_human_decision_input_contract_v0.json",
    "docs/matrixlabs/post_vs2/post_vs2_first_execution_human_decision_input_contract_v0.md",
    "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_contract_v0.json",
    "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_contract_v0.md",
    "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_machinery_receipt_v0.json",
]
POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_SCRIPT = (
    "scripts/build_post_vs2_first_execution_decision_receipt_machinery_v0.py"
)
POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_VERIFY_SCRIPT = (
    "scripts/verify_post_vs2_first_execution_decision_receipt_machinery_v0.py"
)
POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_SCRIPT = (
    "scripts/build_post_vs2_first_execution_decision_receipt_v0.py"
)
POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_VERIFY_SCRIPT = (
    "scripts/verify_post_vs2_first_execution_decision_receipt_v0.py"
)
POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_AUTHORITATIVE_DOCS = [
    "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_v0.json",
    "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_v0.md",
]
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
    *C8_N22_AUTHORITY_BOUNDARY_READABOUT_DOCS,
    C8_N22_AUTHORITY_BOUNDARY_READABOUT_GENERATOR,
    *C8_N22_HUMAN_DECISION_SURFACE_DOCS,
    C8_N22_HUMAN_DECISION_SURFACE_GENERATOR,
    *C8_N22_HUMAN_DECISION_RECEIPT_DOCS,
    C8_N22_HUMAN_DECISION_RECEIPT_GENERATOR,
    *C8_N22_AUTHORITY_STATE_UPDATE_DOCS,
    C8_N22_AUTHORITY_STATE_UPDATE_GENERATOR,
    *C8_N22_AUTHORITY_TRANSITION_CLOSURE_DOCS,
    C8_N22_AUTHORITY_TRANSITION_CLOSURE_GENERATOR,
    *C8_N22_REQUESTED_ACTION_DOCS,
    C8_N22_REQUESTED_ACTION_GENERATOR,
    *C8_N22_AUTHORITY_ROUTE_CLASSIFICATION_DOCS,
    C8_N22_AUTHORITY_ROUTE_CLASSIFICATION_GENERATOR,
    *C8_N22_READ_ONLY_ROUTER_SPECIMEN_CLOSURE_DOCS,
    C8_N22_READ_ONLY_ROUTER_SPECIMEN_CLOSURE_GENERATOR,
    *VALIDATOR_ARCHIVE_SCHEMA_CONTRACT_DOCS,
    VALIDATOR_ARCHIVE_SCHEMA_CONTRACT_GENERATOR,
    *C8_N22_CANDIDATE_ARCHIVE_ENTRY_DOCS,
    C8_N22_CANDIDATE_ARCHIVE_ENTRY_GENERATOR,
    *C8_N22_CANDIDATE_ARCHIVE_ADMISSIBILITY_AUDIT_DOCS,
    C8_N22_CANDIDATE_ARCHIVE_ADMISSIBILITY_AUDIT_GENERATOR,
    *C8_N22_CANDIDATE_PROMOTION_DECISION_SURFACE_DOCS,
    C8_N22_CANDIDATE_PROMOTION_DECISION_SURFACE_GENERATOR,
    *C8_N22_CANDIDATE_PROMOTION_DECISION_RECEIPT_DOCS,
    C8_N22_CANDIDATE_PROMOTION_DECISION_RECEIPT_GENERATOR,
    *C8_N22_ACTIVE_ARCHIVE_ENTRY_DOCS,
    C8_N22_ACTIVE_ARCHIVE_ENTRY_GENERATOR,
    *C8_N22_MACHINE_PROCEED_DOCS,
    *C8_N22_UNIT_SURFACE_DOCS,
    C8_N22_MACHINE_PROCEED_GENERATOR,
    *C8_N22_MACHINE_PROCEED_CLOSURE_DOCS,
    C8_N22_MACHINE_PROCEED_CLOSURE_GENERATOR,
    *C8_N22_COMPRESSION_TARGET_DOCS,
    C8_N22_COMPRESSION_TARGET_GENERATOR,
    *C8_N22_COMPRESSED_PACKET_DOCS,
    C8_N22_COMPRESSED_PACKET_GENERATOR,
    *C8_N22_DECOMPRESSION_AUDIT_DOCS,
    C8_N22_DECOMPRESSION_AUDIT_GENERATOR,
    *C8_N22_COMPRESSION_CLOSURE_DOCS,
    C8_N22_COMPRESSION_CLOSURE_GENERATOR,
    *COMPRESSION_TRACE_REGISTRY_SCHEMA_CONTRACT_DOCS,
    COMPRESSION_TRACE_REGISTRY_SCHEMA_CONTRACT_GENERATOR,
    *C8_N22_TRACE_REGISTRY_CANDIDATE_DOCS,
    C8_N22_TRACE_REGISTRY_CANDIDATE_GENERATOR,
    *C8_N22_TRACE_REGISTRY_CANDIDATE_AUDIT_DOCS,
    C8_N22_TRACE_REGISTRY_CANDIDATE_AUDIT_GENERATOR,
    *C8_N22_TRACE_REGISTRY_CANDIDATE_CLOSURE_DOCS,
    C8_N22_TRACE_REGISTRY_CANDIDATE_CLOSURE_GENERATOR,
    *PHASE_VS0_SOURCE_INVENTORY_DOCS,
    PHASE_VS0_SOURCE_INVENTORY_GENERATOR,
    *PHASE_VS0_HAPPY_PATH_BUILD_DOCS,
    PHASE_VS0_HAPPY_PATH_BUILD_GENERATOR,
    *PHASE_VS0_HAPPY_PATH_VERIFICATION_DOCS,
    PHASE_VS0_HAPPY_PATH_VERIFICATION_SCRIPT,
    *PHASE_VS0_NEGATIVE_PROBE_DOCS,
    PHASE_VS0_NEGATIVE_PROBE_SCRIPT,
    *PHASE_VS0_EVIDENCE_YIELD_REPORT_DOCS,
    PHASE_VS0_EVIDENCE_YIELD_REPORT_SCRIPT,
    *PHASE_VS0_CLOSURE_DOCS,
    PHASE_VS0_CLOSURE_SCRIPT,
    *POST_VS0_DIRECTION_DECISION_RECEIPT_DOCS,
    POST_VS0_DIRECTION_DECISION_RECEIPT_SCRIPT,
    *PHASE_VS1_SOURCE_INTAKE_DOCS,
    PHASE_VS1_SOURCE_INTAKE_SCRIPT,
    *PHASE_VS1_CONTROLLED_LOOP_CONTRACT_DOCS,
    PHASE_VS1_CONTROLLED_LOOP_CONTRACT_SCRIPT,
    *PHASE_VS1_CONTROLLED_LOOP_PRECONDITION_INVENTORY_DOCS,
    PHASE_VS1_CONTROLLED_LOOP_PRECONDITION_INVENTORY_SCRIPT,
    *PHASE_VS1_CONTROLLED_LOOP_READINESS_AUDIT_DOCS,
    PHASE_VS1_CONTROLLED_LOOP_READINESS_AUDIT_SCRIPT,
    *PHASE_VS1_MISSING_PRECONDITION_NEXT_SURFACE_MAP_DOCS,
    PHASE_VS1_MISSING_PRECONDITION_NEXT_SURFACE_MAP_SCRIPT,
    *PHASE_VS1_CLOSURE_DOCS,
    PHASE_VS1_CLOSURE_SCRIPT,
    *POST_VS1_DIRECTION_SURFACE_DOCS,
    POST_VS1_DIRECTION_SURFACE_SCRIPT,
    *POST_VS1_DIRECTION_RECEIPT_DOCS,
    POST_VS1_DIRECTION_RECEIPT_SCRIPT,
    *POST_VS1_DIRECTION_AUTHORITY_UPDATE_DOCS,
    POST_VS1_DIRECTION_AUTHORITY_UPDATE_SCRIPT,
    *POST_VS1_DIRECTION_TRANSITION_CLOSURE_DOCS,
    POST_VS1_DIRECTION_TRANSITION_CLOSURE_SCRIPT,
    *PHASE_VS2_1_POST_VS1_SOURCE_INTAKE_DOCS,
    PHASE_VS2_1_POST_VS1_SOURCE_INTAKE_SCRIPT,
    *PHASE_VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_DOCS,
    PHASE_VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_SCRIPT,
    *PHASE_VS2_3_SCOPE_REGIME_OBJECT_MODEL_DOCS,
    PHASE_VS2_3_SCOPE_REGIME_OBJECT_MODEL_SCRIPT,
    PHASE_VS2_3_SCOPE_REGIME_OBJECT_MODEL_VERIFY_SCRIPT,
    *PHASE_VS2_4_MOVE_SPACE_DOCS,
    PHASE_VS2_4_MOVE_SPACE_SCRIPT,
    PHASE_VS2_4_MOVE_SPACE_VERIFY_SCRIPT,
    *PHASE_VS2_5_CONTROLLED_STEP_DOCS,
    PHASE_VS2_5_CONTROLLED_STEP_SCRIPT,
    PHASE_VS2_5_CONTROLLED_STEP_VERIFY_SCRIPT,
    *PHASE_VS2_6_FIXTURES_REPORTS_READINESS_DOCS,
    PHASE_VS2_6_FIXTURES_REPORTS_READINESS_SCRIPT,
    PHASE_VS2_6_FIXTURES_REPORTS_READINESS_VERIFY_SCRIPT,
    *PHASE_VS2_7_PHASE_CLOSURE_DOCS,
    PHASE_VS2_7_PHASE_CLOSURE_SCRIPT,
    PHASE_VS2_7_PHASE_CLOSURE_VERIFY_SCRIPT,
    *POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_DOCS,
    POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_SCRIPT,
    POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_VERIFY_SCRIPT,
    *POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_DOCS,
    POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_SCRIPT,
    POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_VERIFY_SCRIPT,
    POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_SCRIPT,
    POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_VERIFY_SCRIPT,
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


def stable_generated_at_for_head(root: Path, head: str) -> str:
    commit_timestamp = int(run_git(root, ["show", "-s", "--format=%ct", head], check=True))
    return (
        datetime.fromtimestamp(commit_timestamp, timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


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


def read_json_if_present(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def phase_vs2_6_current_unit_summary(root: Path) -> str:
    receipt = read_json_if_present(root / PHASE_VS2_6_FIXTURES_REPORTS_READINESS_DOCS[-1])
    if not receipt:
        return "- current_unit = `UNKNOWN_PHASE_VS2_6_NOT_BUILT`"
    return "\n".join(
        [
            f"- current_unit = `{receipt.get('unit_id', 'UNKNOWN')}`",
            f"- readiness_verdict = `{receipt.get('readiness_verdict', 'UNKNOWN')}`",
            f"- execution_package_core_id = `{receipt.get('artifact_bindings', {}).get('E0', {}).get('artifact_id', 'UNKNOWN')}`",
            f"- readiness_seal_id = `{receipt.get('artifact_bindings', {}).get('RS0', {}).get('artifact_id', 'UNKNOWN')}`",
            f"- fixture_count = `{receipt.get('fixture_count', 'UNKNOWN')}`",
            f"- static_candidate_specimen_count = `{receipt.get('static_candidate_specimen_count', 'UNKNOWN')}`",
            f"- runtime_candidate_instance_count = `{receipt.get('runtime_candidate_instance_count', 'UNKNOWN')}`",
            f"- runtime_reports_emitted = `{receipt.get('runtime_reports_emitted', 'UNKNOWN')}`",
            f"- execution_authority_present = `{str(receipt.get('execution_authority_present', 'UNKNOWN')).lower()}`",
            f"- remaining_effective_grant_count = `{receipt.get('remaining_effective_grant_count_after', 'UNKNOWN')}`",
            f"- next_lawful_unit = `VS2_7_PHASE_CLOSURE_PENDING`",
            f"- logical_terminal_transition = `{receipt.get('logical_transition', 'UNKNOWN')}`",
        ]
    )


def phase_vs2_current_unit_summary(root: Path) -> str:
    machinery = read_json_if_present(
        root / POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_DOCS[-1]
    )
    if machinery:
        payload = machinery.get("receipt_binding", {}).get("receipt_payload", {})
        return "\n".join(
            [
                f"- current_unit = `{payload.get('current_unit', 'POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_PREPARATION')}`",
                "- current_surface = `POST_VS2_FIRST_EXECUTION_DECISION_SURFACE`",
                f"- surface_instance_state = `{payload.get('surface_state', 'UNCONSUMED')}`",
                f"- human_decision_required = `{str(payload.get('human_decision_required', True)).lower()}`",
                f"- human_decision_input_present = `{str(payload.get('human_decision_input_present', False)).lower()}`",
                f"- human_decision_recorded = `{str(payload.get('human_decision_recorded', False)).lower()}`",
                f"- selected_option = `{payload.get('selected_option')}`",
                f"- decision_receipt_created = `{str(payload.get('decision_receipt_created', False)).lower()}`",
                f"- decision_receipt_machinery_ready = `{str(payload.get('decision_receipt_machinery_ready', True)).lower()}`",
                "- decision_option_count = `6`",
                f"- authority_update_applied = `{str(payload.get('authority_update_applied', False)).lower()}`",
                f"- execution_authority_present = `{str(payload.get('execution_authority_present', False)).lower()}`",
                f"- run_id_created = `{str(payload.get('run_id_created', False)).lower()}`",
                f"- execution_source_intake_created = `{str(payload.get('execution_source_intake_created', False)).lower()}`",
                f"- execution_started = `{str(payload.get('execution_started', False)).lower()}`",
                f"- runtime_receipts_emitted = `{payload.get('runtime_receipts_emitted', 0)}`",
                f"- runtime_reports_emitted = `{payload.get('runtime_reports_emitted', 0)}`",
                f"- runner_created = `{str(payload.get('runner_authority_present', False)).lower()}`",
                f"- terminal_transition = `{payload.get('terminal_transition', 'STOP_POST_VS2_DECISION_RECEIPT_MACHINERY_READY_SURFACE_UNCONSUMED')}`",
                "- next_lawful_action = `SUPPLY_ONE_EXPLICIT_AUTHENTICATED_POST_VS2_HUMAN_DECISION_INPUT`",
            ]
        )
    post_surface = read_json_if_present(
        root / POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_DOCS[0]
    )
    if post_surface:
        payload = post_surface.get("surface_payload", {})
        e0 = payload.get("execution_package_core_reference", {})
        rs0 = payload.get("readiness_seal_reference", {})
        decision = payload.get("decision_state", {})
        authority = payload.get("authority_state", {})
        execution = payload.get("execution_state", {})
        terminal = payload.get("terminal_transition", {})
        return "\n".join(
            [
                f"- current_unit = `{payload.get('unit_id', 'POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_PREPARATION')}`",
                f"- current_surface = `{payload.get('surface_id', 'POST_VS2_FIRST_EXECUTION_DECISION_SURFACE')}`",
                f"- surface_gate = `{payload.get('surface_gate', 'UNKNOWN')}`",
                f"- surface_instance_state = `{payload.get('surface_instance_state', 'UNKNOWN')}`",
                f"- human_decision_required = `{str(decision.get('human_decision_required', 'UNKNOWN')).lower()}`",
                f"- human_decision_recorded = `{str(decision.get('human_decision_recorded', 'UNKNOWN')).lower()}`",
                f"- decision_receipt_created = `{str(decision.get('decision_receipt_created', 'UNKNOWN')).lower()}`",
                f"- decision_option_count = `{len(payload.get('decision_options', []))}`",
                f"- execution_package_core_id = `{e0.get('logical_package_id', 'UNKNOWN')}`",
                f"- execution_package_core_sha256 = `{e0.get('canonical_sha256', 'UNKNOWN')}`",
                f"- readiness_seal_id = `{rs0.get('logical_seal_id', 'UNKNOWN')}`",
                f"- readiness_seal_sha256 = `{rs0.get('canonical_sha256', 'UNKNOWN')}`",
                f"- authority_update_applied = `{str(authority.get('authority_update_applied', 'UNKNOWN')).lower()}`",
                f"- execution_authority_present = `{str(authority.get('execution_authority_present', 'UNKNOWN')).lower()}`",
                f"- sweep_authority_present = `{str(authority.get('sweep_authority_present', 'UNKNOWN')).lower()}`",
                f"- run_allocation_authority_present = `{str(authority.get('run_allocation_authority_present', 'UNKNOWN')).lower()}`",
                f"- run_id_created = `{str(execution.get('run_id_created', 'UNKNOWN')).lower()}`",
                f"- execution_source_intake_created = `{str(execution.get('execution_source_intake_created', 'UNKNOWN')).lower()}`",
                f"- execution_started = `{str(execution.get('execution_started', 'UNKNOWN')).lower()}`",
                f"- runtime_receipts_emitted = `{execution.get('runtime_receipts_emitted', 'UNKNOWN')}`",
                f"- runtime_reports_emitted = `{execution.get('runtime_reports_emitted', 'UNKNOWN')}`",
                f"- runner_created = `{str(authority.get('runner_authority_present', 'UNKNOWN')).lower()}`",
                f"- terminal_transition = `{terminal.get('transition', 'UNKNOWN')}`",
                "- next_lawful_action = `HUMAN_DECISION_REQUIRED`",
            ]
        )
    closure = read_json_if_present(root / PHASE_VS2_7_PHASE_CLOSURE_DOCS[0])
    if not closure:
        return phase_vs2_6_current_unit_summary(root)
    payload = closure.get("closure_payload", {})
    e0 = payload.get("execution_package_core_binding", {})
    rs0 = payload.get("readiness_seal_binding", {})
    authority = payload.get("authority_summary", {})
    execution = payload.get("execution_state", {})
    surface = payload.get("post_phase_decision_surface", {})
    terminal = payload.get("terminal_transition", {})
    return "\n".join(
        [
            f"- current_unit = `{payload.get('normalized_unit_id', 'VS2_7_PHASE_CLOSURE')}`",
            f"- phase_status = `{payload.get('phase_status', 'UNKNOWN')}`",
            f"- closure_gate = `{payload.get('closure_gate', 'UNKNOWN')}`",
            f"- readiness_branch = `{payload.get('readiness_branch', 'UNKNOWN')}`",
            f"- execution_package_core_artifact_id = `{e0.get('artifact_id', 'UNKNOWN')}`",
            f"- execution_package_core_id = `{e0.get('package_id', 'UNKNOWN')}`",
            f"- execution_package_core_sha256 = `{e0.get('canonical_sha256', 'UNKNOWN')}`",
            f"- readiness_seal_artifact_id = `{rs0.get('artifact_id', 'UNKNOWN')}`",
            f"- readiness_seal_id = `{rs0.get('seal_id', 'UNKNOWN')}`",
            f"- readiness_seal_sha256 = `{rs0.get('canonical_sha256', 'UNKNOWN')}`",
            f"- next_lawful_surface = `{surface.get('surface_id', 'UNKNOWN')}`",
            f"- next_surface_state = `named, not created`",
            f"- execution_authority_present = `{str(authority.get('execution_authority_present', 'UNKNOWN')).lower()}`",
            f"- execution_started = `{str(execution.get('execution_started', 'UNKNOWN')).lower()}`",
            f"- runner_created = `{str(authority.get('runner_created', 'UNKNOWN')).lower()}`",
            f"- terminal_transition = `{terminal.get('transition', 'UNKNOWN')}`",
        ]
    )


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
    manifest_text = read_text(manifest)
    try:
        data = json.loads(manifest_text)
    except json.JSONDecodeError as exc:
        generated_markers = [
            f'"schema_version": "{SCHEMA_VERSION}"',
            f'"generator_script": "{GENERATOR_SCRIPT}"',
        ]
        if all(marker in manifest_text for marker in generated_markers):
            return baseline
        raise GenerationError(
            "baseline_share/MANIFEST.json is not valid JSON and lacks generator identity; refusing to overwrite"
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

## Phase VS2 current unit

{phase_vs2_current_unit_summary(root)}

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
    phase_vs2_dir = root / "docs/matrixlabs/phase_vs2"
    post_vs2_dir = root / "docs/matrixlabs/post_vs2"
    docs_count = count_files(docs_receipts)
    external_count = count_files(external_archive)
    phase_vs2_receipt_count = len(list(phase_vs2_dir.glob("*receipt*.json"))) if phase_vs2_dir.exists() else 0
    post_vs2_receipts = (
        sorted(str(path.relative_to(root)) for path in post_vs2_dir.glob("*receipt*.json"))
        if post_vs2_dir.exists()
        else []
    )
    post_vs2_surface_preparation_receipts = [
        path for path in post_vs2_receipts
        if path.endswith("post_vs2_first_execution_decision_surface_receipt_v0.json")
    ]
    post_vs2_machinery_preparation_receipts = [
        path for path in post_vs2_receipts
        if path.endswith("post_vs2_first_execution_decision_receipt_machinery_receipt_v0.json")
    ]
    post_vs2_authoritative_decision_receipts = [
        path for path in post_vs2_receipts
        if path.endswith("post_vs2_first_execution_decision_receipt_v0.json")
    ]
    post_vs2_receipt_lines = (
        "\n".join(f"- `{path}`" for path in post_vs2_receipts)
        if post_vs2_receipts
        else "- none"
    )
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
- Repo Phase VS2 receipt JSONs: `docs/matrixlabs/phase_vs2/*receipt*.json` - file count: `{phase_vs2_receipt_count}`.
- Repo Post-VS2 receipt JSONs: `docs/matrixlabs/post_vs2/*receipt*.json` - file count: `{len(post_vs2_receipts)}`.
- Repo Post-VS2 surface-preparation receipt JSONs: file count: `{len(post_vs2_surface_preparation_receipts)}`.
- Repo Post-VS2 receipt-machinery preparation receipt JSONs: file count: `{len(post_vs2_machinery_preparation_receipts)}`.
- Repo authoritative Post-VS2 human decision receipt JSONs: file count: `{len(post_vs2_authoritative_decision_receipts)}`.

## Current load-bearing recent receipt pointers

- C8 post-patch surface decision acceptance receipt: `{C8_POST_PATCH_RECEIPT}` - {'present' if c8_receipt_present else 'missing/uncertain'}.

## Post-VS2 receipt pointers

{post_vs2_receipt_lines}

## Architecture extraction terminal receipt pointer

{arch_matches}

## Upload rule

Upload `baseline_share/` first. Expand individual receipts only when a claim becomes load-bearing. Do not upload or duplicate the full receipt archive unless a later bounded task specifically asks for that evidence."""


def render_commit_context(
    root: Path,
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
- The generator did not copy the full receipt stack into `baseline_share/`.

## Phase VS2 current unit

{phase_vs2_current_unit_summary(root)}"""


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
    a2_receipt_present = (root / C8_N22_HUMAN_DECISION_RECEIPT_DOCS[0]).exists()
    a3_update_present = (root / C8_N22_AUTHORITY_STATE_UPDATE_DOCS[0]).exists()
    a4_closure_present = (root / C8_N22_AUTHORITY_TRANSITION_CLOSURE_DOCS[0]).exists()
    b1_requested_action_present = (root / C8_N22_REQUESTED_ACTION_DOCS[0]).exists()
    b2_route_classification_present = (root / C8_N22_AUTHORITY_ROUTE_CLASSIFICATION_DOCS[0]).exists()
    b3_router_specimen_closure_present = (root / C8_N22_READ_ONLY_ROUTER_SPECIMEN_CLOSURE_DOCS[0]).exists()
    c1_archive_schema_contract_present = (root / VALIDATOR_ARCHIVE_SCHEMA_CONTRACT_DOCS[0]).exists()
    c2_candidate_archive_entry_present = (root / C8_N22_CANDIDATE_ARCHIVE_ENTRY_DOCS[0]).exists()
    c3_candidate_archive_audit_present = (root / C8_N22_CANDIDATE_ARCHIVE_ADMISSIBILITY_AUDIT_DOCS[0]).exists()
    d1_promotion_decision_surface_present = (root / C8_N22_CANDIDATE_PROMOTION_DECISION_SURFACE_DOCS[0]).exists()
    d2_promotion_decision_receipt_present = (root / C8_N22_CANDIDATE_PROMOTION_DECISION_RECEIPT_DOCS[0]).exists()
    d3_active_archive_entry_present = (root / C8_N22_ACTIVE_ARCHIVE_ENTRY_DOCS[0]).exists()
    d4_machine_proceed_present = (root / C8_N22_MACHINE_PROCEED_DOCS[0]).exists()
    d4_unit_surface_present = (root / C8_N22_UNIT_SURFACE_DOCS[0]).exists()
    d5_machine_proceed_closure_present = (root / C8_N22_MACHINE_PROCEED_CLOSURE_DOCS[0]).exists()
    e1_compression_target_present = (root / C8_N22_COMPRESSION_TARGET_DOCS[0]).exists()
    e2_compressed_packet_present = (root / C8_N22_COMPRESSED_PACKET_DOCS[0]).exists()
    e3_decompression_audit_present = (root / C8_N22_DECOMPRESSION_AUDIT_DOCS[0]).exists()
    e4_compression_closure_present = (root / C8_N22_COMPRESSION_CLOSURE_DOCS[0]).exists()
    f1_registry_schema_contract_present = (root / COMPRESSION_TRACE_REGISTRY_SCHEMA_CONTRACT_DOCS[0]).exists()
    f2_trace_registry_candidate_present = (root / C8_N22_TRACE_REGISTRY_CANDIDATE_DOCS[0]).exists()
    f3_trace_registry_candidate_audit_present = (root / C8_N22_TRACE_REGISTRY_CANDIDATE_AUDIT_DOCS[0]).exists()
    f4_trace_registry_candidate_closure_present = (root / C8_N22_TRACE_REGISTRY_CANDIDATE_CLOSURE_DOCS[0]).exists()
    phase_vs0_source_inventory_present = (root / PHASE_VS0_SOURCE_INVENTORY_DOCS[0]).exists()
    phase_vs0_happy_path_build_present = (root / PHASE_VS0_HAPPY_PATH_BUILD_DOCS[0]).exists()
    phase_vs0_happy_path_verification_present = (root / PHASE_VS0_HAPPY_PATH_VERIFICATION_DOCS[0]).exists()
    phase_vs0_happy_path_verification = (
        json.loads((root / PHASE_VS0_HAPPY_PATH_VERIFICATION_DOCS[0]).read_text(encoding="utf-8"))
        if phase_vs0_happy_path_verification_present
        else {}
    )
    phase_vs0_happy_path_verification_status = phase_vs0_happy_path_verification.get(
        "verification_result", {}
    ).get("happy_path_verification_status")
    phase_vs0_happy_path_verification_passed = (
        phase_vs0_happy_path_verification_status
        == "VS0_3_HAPPY_PATH_VERIFICATION_PASS_A_TO_F_PHASE_SPECIMEN_VERIFIED"
    )
    phase_vs0_negative_probe_battery_path = (
        root
        / PHASE_VS0_NEGATIVE_PROBE_ROOT
        / "phase_vs0_negative_probe_battery_v0.json"
    )
    phase_vs0_negative_probe_battery_present = (
        phase_vs0_negative_probe_battery_path.exists()
    )
    phase_vs0_negative_probe_battery = (
        json.loads(
            phase_vs0_negative_probe_battery_path.read_text(encoding="utf-8")
        )
        if phase_vs0_negative_probe_battery_present
        else {}
    )
    phase_vs0_negative_probe_battery_status = (
        phase_vs0_negative_probe_battery.get("battery_result", {}).get(
            "negative_probe_battery_status"
        )
    )
    phase_vs0_negative_probe_battery_passed = (
        phase_vs0_negative_probe_battery_status
        == "VS0_4_NEGATIVE_PROBES_PASS_TYPED_STOPS"
    )
    phase_vs0_probe_summary = phase_vs0_negative_probe_battery.get(
        "probe_summary", {}
    )
    phase_vs0_preservation = phase_vs0_negative_probe_battery.get(
        "preservation_snapshot", {}
    )
    phase_vs0_coverage = phase_vs0_negative_probe_battery.get(
        "coverage_claim", {}
    )
    phase_vs0_battery_result = phase_vs0_negative_probe_battery.get(
        "battery_result", {}
    )
    phase_vs0_yield = phase_vs0_negative_probe_battery.get(
        "evidence_yield_class", {}
    )
    phase_vs0_evidence_yield_report_path = (
        root / PHASE_VS0_EVIDENCE_YIELD_REPORT_DOCS[0]
    )
    phase_vs0_evidence_yield_report_present = (
        phase_vs0_evidence_yield_report_path.exists()
    )
    phase_vs0_evidence_yield_report = (
        json.loads(
            phase_vs0_evidence_yield_report_path.read_text(encoding="utf-8")
        )
        if phase_vs0_evidence_yield_report_present
        else {}
    )
    phase_vs0_evidence_yield_report_status = (
        phase_vs0_evidence_yield_report.get("yield_result", {}).get(
            "evidence_yield_report_status"
        )
    )
    phase_vs0_evidence_yield_report_passed = (
        phase_vs0_evidence_yield_report_status
        == "VS0_5_EVIDENCE_YIELD_REPORT_PASS_USEFUL_EVIDENCE_PRESENT"
    )
    phase_vs0_yield_summary = phase_vs0_evidence_yield_report.get(
        "yield_summary", {}
    )
    phase_vs0_overclaim_guard = phase_vs0_evidence_yield_report.get(
        "overclaim_guard", {}
    )
    phase_vs0_closure_readiness = phase_vs0_evidence_yield_report.get(
        "closure_readiness_boundary", {}
    )
    phase_vs0_closure_path = root / PHASE_VS0_CLOSURE_DOCS[0]
    phase_vs0_closure_present = phase_vs0_closure_path.exists()
    phase_vs0_closure = (
        json.loads(phase_vs0_closure_path.read_text(encoding="utf-8"))
        if phase_vs0_closure_present
        else {}
    )
    phase_vs0_closure_gate = phase_vs0_closure.get("phase_vs0_closure_gate")
    phase_vs0_closure_passed = (
        phase_vs0_closure_gate
        == "VS0_6_PHASE_CLOSURE_PASS_FIRST_A_TO_F_SPECIMEN_WITH_TYPED_STOPS_AND_EVIDENCE_YIELD"
    )
    phase_vs0_closure_claim_scope = phase_vs0_closure.get(
        "closure_claim_scope", {}
    )
    phase_vs0_closure_pass_scope = phase_vs0_closure.get(
        "phase_pass_scope", {}
    )
    phase_vs0_closure_next_surface = phase_vs0_closure.get(
        "next_lawful_surface", {}
    )
    phase_vs0_closure_boundaries = phase_vs0_closure.get(
        "confirmed_boundaries", {}
    )
    phase_vs0_closure_coverage = phase_vs0_closure.get(
        "coverage_boundary", {}
    )
    phase_vs0_closure_source_commits = phase_vs0_closure.get(
        "source_commits", {}
    )
    post_vs0_direction_receipt_path = (
        root / POST_VS0_DIRECTION_DECISION_RECEIPT_DOCS[0]
    )
    post_vs0_direction_receipt_present = (
        post_vs0_direction_receipt_path.exists()
    )
    post_vs0_direction_receipt = (
        json.loads(
            post_vs0_direction_receipt_path.read_text(encoding="utf-8")
        )
        if post_vs0_direction_receipt_present
        else {}
    )
    post_vs0_direction_decision = post_vs0_direction_receipt.get(
        "decision", {}
    )
    post_vs0_direction_forbidden_scope = post_vs0_direction_receipt.get(
        "forbidden_scope", {}
    )
    post_vs0_direction_source_closure = post_vs0_direction_receipt.get(
        "source_closure", {}
    )
    post_vs0_direction_next_unit = post_vs0_direction_receipt.get(
        "next_unit", {}
    )
    phase_vs1_source_intake_path = root / PHASE_VS1_SOURCE_INTAKE_DOCS[0]
    phase_vs1_source_intake_present = phase_vs1_source_intake_path.exists()
    phase_vs1_source_intake = (
        json.loads(phase_vs1_source_intake_path.read_text(encoding="utf-8"))
        if phase_vs1_source_intake_present
        else {}
    )
    phase_vs1_source_intake_authority = phase_vs1_source_intake.get(
        "source_authority_basis", {}
    )
    phase_vs1_source_intake_vs0_6 = phase_vs1_source_intake.get(
        "source_vs0_6_closure_binding", {}
    )
    phase_vs1_source_intake_scope = phase_vs1_source_intake.get(
        "accepted_input_scope", {}
    )
    phase_vs1_source_intake_boundary = phase_vs1_source_intake.get(
        "boundary_preservation_status", {}
    )
    phase_vs1_controlled_loop_contract_path = (
        root / PHASE_VS1_CONTROLLED_LOOP_CONTRACT_DOCS[0]
    )
    phase_vs1_controlled_loop_contract_present = (
        phase_vs1_controlled_loop_contract_path.exists()
    )
    phase_vs1_controlled_loop_contract = (
        json.loads(
            phase_vs1_controlled_loop_contract_path.read_text(encoding="utf-8")
        )
        if phase_vs1_controlled_loop_contract_present
        else {}
    )
    phase_vs1_contract_source_intake = phase_vs1_controlled_loop_contract.get(
        "source_intake", {}
    )
    phase_vs1_contract_loop = phase_vs1_controlled_loop_contract.get(
        "loop_contract", {}
    )
    phase_vs1_contract_components = phase_vs1_controlled_loop_contract.get(
        "component_presence_claims", {}
    )
    phase_vs1_contract_boundary = phase_vs1_controlled_loop_contract.get(
        "contract_boundary", {}
    )
    phase_vs1_contract_terminal = phase_vs1_controlled_loop_contract.get(
        "terminal_transition", {}
    )
    phase_vs1_precondition_inventory_path = (
        root / PHASE_VS1_CONTROLLED_LOOP_PRECONDITION_INVENTORY_DOCS[0]
    )
    phase_vs1_precondition_inventory_present = (
        phase_vs1_precondition_inventory_path.exists()
    )
    phase_vs1_precondition_inventory = (
        json.loads(
            phase_vs1_precondition_inventory_path.read_text(encoding="utf-8")
        )
        if phase_vs1_precondition_inventory_present
        else {}
    )
    phase_vs1_precondition_inventory_source_contract = (
        phase_vs1_precondition_inventory.get("source_contract", {})
    )
    phase_vs1_precondition_inventory_counts = (
        phase_vs1_precondition_inventory.get("summary_counts", {})
    )
    phase_vs1_precondition_inventory_mode = (
        phase_vs1_precondition_inventory.get("inventory_mode", {})
    )
    phase_vs1_precondition_inventory_repair_boundary = (
        phase_vs1_precondition_inventory.get("repair_and_ranking_boundary", {})
    )
    phase_vs1_precondition_inventory_non_claims = (
        phase_vs1_precondition_inventory.get("non_claims", {})
    )
    phase_vs1_precondition_inventory_terminal = (
        phase_vs1_precondition_inventory.get("terminal_transition", {})
    )
    phase_vs1_readiness_audit_path = (
        root / PHASE_VS1_CONTROLLED_LOOP_READINESS_AUDIT_DOCS[0]
    )
    phase_vs1_readiness_audit_present = phase_vs1_readiness_audit_path.exists()
    phase_vs1_readiness_audit = (
        json.loads(phase_vs1_readiness_audit_path.read_text(encoding="utf-8"))
        if phase_vs1_readiness_audit_present
        else {}
    )
    phase_vs1_readiness_source_inventory = phase_vs1_readiness_audit.get(
        "source_inventory", {}
    )
    phase_vs1_readiness_target = phase_vs1_readiness_audit.get(
        "readiness_target", {}
    )
    phase_vs1_readiness_profile = phase_vs1_readiness_audit.get(
        "readiness_profile", {}
    )
    phase_vs1_readiness_aggregate = phase_vs1_readiness_audit.get(
        "aggregate_readiness_verdict", {}
    )
    phase_vs1_readiness_execution = phase_vs1_readiness_audit.get(
        "execution_authority_status", {}
    )
    phase_vs1_readiness_vs1_5 = phase_vs1_readiness_audit.get(
        "vs1_5_boundary", {}
    )
    phase_vs1_readiness_terminal = phase_vs1_readiness_audit.get(
        "terminal_transition", {}
    )
    phase_vs1_next_surface_map_path = (
        root / PHASE_VS1_MISSING_PRECONDITION_NEXT_SURFACE_MAP_DOCS[0]
    )
    phase_vs1_next_surface_map_present = phase_vs1_next_surface_map_path.exists()
    phase_vs1_next_surface_map = (
        json.loads(phase_vs1_next_surface_map_path.read_text(encoding="utf-8"))
        if phase_vs1_next_surface_map_present
        else {}
    )
    phase_vs1_next_surface_source = phase_vs1_next_surface_map.get(
        "source_readiness_audit", {}
    )
    phase_vs1_next_surface_coverage = phase_vs1_next_surface_map.get(
        "blocker_coverage", {}
    )
    phase_vs1_next_surface_policy = phase_vs1_next_surface_map.get(
        "mapping_policy", {}
    )
    phase_vs1_next_surface_ranking_policy = phase_vs1_next_surface_map.get(
        "advisory_ranking_policy", {}
    )
    phase_vs1_next_surface_ranking = phase_vs1_next_surface_map.get(
        "advisory_ranking", {}
    )
    phase_vs1_next_surface_forbidden = phase_vs1_next_surface_map.get(
        "forbidden_claim_checks", {}
    )
    phase_vs1_next_surface_vs1_6 = phase_vs1_next_surface_map.get(
        "vs1_6_boundary", {}
    )
    phase_vs1_next_surface_terminal = phase_vs1_next_surface_map.get(
        "terminal_transition", {}
    )
    phase_vs1_closure_path = root / PHASE_VS1_CLOSURE_DOCS[0]
    phase_vs1_closure_present = phase_vs1_closure_path.exists()
    phase_vs1_closure = (
        json.loads(phase_vs1_closure_path.read_text(encoding="utf-8"))
        if phase_vs1_closure_present
        else {}
    )
    phase_vs1_closure_source_chain = phase_vs1_closure.get(
        "source_chain_commit_bindings", {}
    )
    phase_vs1_closure_phase_result = phase_vs1_closure.get("phase_result", {})
    phase_vs1_closure_blocker_summary = phase_vs1_closure.get(
        "blocker_summary", {}
    )
    phase_vs1_closure_next_surface = phase_vs1_closure.get(
        "next_surface_summary", {}
    )
    phase_vs1_closure_readiness = phase_vs1_closure.get("readiness_summary", {})
    phase_vs1_closure_post_vs1 = phase_vs1_closure.get(
        "post_vs1_decision_surface", {}
    )
    phase_vs1_closure_terminal = phase_vs1_closure.get("terminal_transition", {})
    post_vs1_direction_surface_path = root / POST_VS1_DIRECTION_SURFACE_DOCS[0]
    post_vs1_direction_surface_present = post_vs1_direction_surface_path.exists()
    post_vs1_direction_surface = (
        json.loads(post_vs1_direction_surface_path.read_text(encoding="utf-8"))
        if post_vs1_direction_surface_present
        else {}
    )
    post_vs1_proposal_source_path = root / POST_VS1_DIRECTION_SURFACE_DOCS[3]
    post_vs1_proposal_source_present = post_vs1_proposal_source_path.exists()
    post_vs1_proposal_source = (
        json.loads(post_vs1_proposal_source_path.read_text(encoding="utf-8"))
        if post_vs1_proposal_source_present
        else {}
    )
    post_vs1_proposal_bundle = post_vs1_direction_surface.get("proposal_bundle", {})
    post_vs1_membership = post_vs1_direction_surface.get(
        "proposal_bundle_membership_contract", {}
    )
    post_vs1_traceability = post_vs1_direction_surface.get(
        "proposal_bundle_traceability", {}
    )
    post_vs1_decision_package = post_vs1_direction_surface.get(
        "decision_package_binding", {}
    )
    post_vs1_defaults = post_vs1_direction_surface.get("decision_default_state", {})
    post_vs1_decision_state = post_vs1_direction_surface.get("decision_state", {})
    post_vs1_recommended = post_vs1_direction_surface.get("recommended_direction", {})
    post_vs1_terminal = post_vs1_direction_surface.get("terminal_transition", {})
    post_vs1_direction_receipt_path = root / POST_VS1_DIRECTION_RECEIPT_DOCS[0]
    post_vs1_direction_receipt_present = post_vs1_direction_receipt_path.exists()
    post_vs1_direction_receipt = (
        json.loads(post_vs1_direction_receipt_path.read_text(encoding="utf-8"))
        if post_vs1_direction_receipt_present
        else {}
    )
    post_vs1_receipt_selection = post_vs1_direction_receipt.get(
        "decision_selection", {}
    )
    post_vs1_receipt_state = post_vs1_direction_receipt.get(
        "decision_state_after_receipt", {}
    )
    post_vs1_receipt_source_binding = post_vs1_direction_receipt.get(
        "source_surface_binding", {}
    )
    post_vs1_receipt_terminal = post_vs1_direction_receipt.get(
        "terminal_transition", {}
    )
    post_vs1_receipt_binding = post_vs1_direction_receipt.get(
        "decision_receipt_binding", {}
    )
    post_vs1_receipt_payload = post_vs1_receipt_binding.get(
        "decision_receipt_payload", {}
    )
    post_vs1_receipt_hash = post_vs1_receipt_binding.get(
        "decision_receipt_sha256"
    )
    post_vs1_receipt_recomputed_hash = (
        hashlib.sha256(
            json.dumps(
                post_vs1_receipt_payload,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            ).encode("utf-8")
        ).hexdigest()
        if post_vs1_direction_receipt_present
        else None
    )
    post_vs1_receipt_approved_scope = post_vs1_direction_receipt.get(
        "approved_scope", {}
    )
    post_vs1_receipt_authority_effects = post_vs1_direction_receipt.get(
        "authority_effects", {}
    )
    post_vs1_direction_authority_update_path = (
        root / POST_VS1_DIRECTION_AUTHORITY_UPDATE_DOCS[0]
    )
    post_vs1_direction_authority_update_present = (
        post_vs1_direction_authority_update_path.exists()
    )
    post_vs1_direction_authority_update = (
        json.loads(
            post_vs1_direction_authority_update_path.read_text(encoding="utf-8")
        )
        if post_vs1_direction_authority_update_present
        else {}
    )
    post_vs1_authority_update_source_receipt = (
        post_vs1_direction_authority_update.get(
            "source_decision_receipt_binding", {}
        )
    )
    post_vs1_authority_update_source_package = (
        post_vs1_direction_authority_update.get(
            "source_decision_package_binding", {}
        )
    )
    post_vs1_authority_update_consumption = (
        post_vs1_direction_authority_update.get("decision_receipt_consumption", {})
    )
    post_vs1_authority_update_state = (
        post_vs1_direction_authority_update.get("authority_state_after_update", {})
    )
    post_vs1_authority_update_binding = (
        post_vs1_direction_authority_update.get("authority_update_binding", {})
    )
    post_vs1_authority_update_terminal = (
        post_vs1_direction_authority_update.get("terminal_transition", {})
    )
    post_vs1_direction_transition_closure_path = (
        root / POST_VS1_DIRECTION_TRANSITION_CLOSURE_DOCS[0]
    )
    post_vs1_direction_transition_closure_present = (
        post_vs1_direction_transition_closure_path.exists()
    )
    post_vs1_direction_transition_closure = (
        json.loads(
            post_vs1_direction_transition_closure_path.read_text(encoding="utf-8")
        )
        if post_vs1_direction_transition_closure_present
        else {}
    )
    post_vs1_transition_closure_source_authority = (
        post_vs1_direction_transition_closure.get(
            "source_authority_update_binding", {}
        )
    )
    post_vs1_transition_closure_consumption = (
        post_vs1_direction_transition_closure.get("authority_update_consumption", {})
    )
    post_vs1_transition_closure_state = (
        post_vs1_direction_transition_closure.get("post_closure_authority_state", {})
    )
    post_vs1_transition_closure_binding = (
        post_vs1_direction_transition_closure.get("transition_closure_binding", {})
    )
    post_vs1_transition_closure_terminal = (
        post_vs1_direction_transition_closure.get("terminal_transition", {})
    )
    post_vs1_effective_authority_state = (
        post_vs1_transition_closure_state
        if post_vs1_direction_transition_closure_present
        else post_vs1_authority_update_state
    )
    post_vs1_effective_terminal = (
        post_vs1_transition_closure_terminal
        if post_vs1_direction_transition_closure_present
        else post_vs1_authority_update_terminal
    )
    phase_vs2_1_source_intake_path = (
        root / PHASE_VS2_1_POST_VS1_SOURCE_INTAKE_DOCS[0]
    )
    phase_vs2_1_source_intake_present = phase_vs2_1_source_intake_path.exists()
    phase_vs2_1_source_intake = (
        json.loads(phase_vs2_1_source_intake_path.read_text(encoding="utf-8"))
        if phase_vs2_1_source_intake_present
        else {}
    )
    phase_vs2_1_source_intake_receipt_path = (
        root / PHASE_VS2_1_POST_VS1_SOURCE_INTAKE_DOCS[2]
    )
    phase_vs2_1_source_intake_receipt_present = (
        phase_vs2_1_source_intake_receipt_path.exists()
    )
    phase_vs2_1_source_intake_receipt = (
        json.loads(
            phase_vs2_1_source_intake_receipt_path.read_text(encoding="utf-8")
        )
        if phase_vs2_1_source_intake_receipt_present
        else {}
    )
    phase_vs2_1_intake_binding = phase_vs2_1_source_intake.get(
        "source_intake_binding", {}
    )
    phase_vs2_1_source_manifest = phase_vs2_1_source_intake.get(
        "source_manifest_binding", {}
    )
    phase_vs2_1_grant_routing = phase_vs2_1_source_intake.get("grant_routing", {})
    phase_vs2_1_effective_grants = phase_vs2_1_source_intake.get(
        "effective_grant_inventory", {}
    )
    phase_vs2_1_post_state = phase_vs2_1_source_intake.get(
        "post_intake_phase_state", {}
    )
    phase_vs2_2_profile_path = (
        root / PHASE_VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_DOCS[0]
    )
    phase_vs2_2_profile_present = phase_vs2_2_profile_path.exists()
    phase_vs2_2_profile = (
        json.loads(phase_vs2_2_profile_path.read_text(encoding="utf-8"))
        if phase_vs2_2_profile_present
        else {}
    )
    phase_vs2_2_target_path = (
        root / PHASE_VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_DOCS[2]
    )
    phase_vs2_2_target_present = phase_vs2_2_target_path.exists()
    phase_vs2_2_target = (
        json.loads(phase_vs2_2_target_path.read_text(encoding="utf-8"))
        if phase_vs2_2_target_present
        else {}
    )
    phase_vs2_2_receipt_path = (
        root / PHASE_VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_DOCS[4]
    )
    phase_vs2_2_receipt_present = phase_vs2_2_receipt_path.exists()
    phase_vs2_2_receipt = (
        json.loads(phase_vs2_2_receipt_path.read_text(encoding="utf-8"))
        if phase_vs2_2_receipt_present
        else {}
    )
    phase_vs2_2_profile_binding = phase_vs2_2_profile.get("profile_binding", {})
    phase_vs2_2_target_binding = phase_vs2_2_target.get("target_freeze_binding", {})
    phase_vs2_2_profile_identity = phase_vs2_2_profile.get("profile_identity", {})
    phase_vs2_2_target_identity = phase_vs2_2_target.get("target_identity", {})
    phase_vs2_2_component_summary = phase_vs2_2_profile.get(
        "component_profile_summary", {}
    )
    phase_vs2_2_remaining_grants = phase_vs2_2_profile.get(
        "remaining_grant_routing", {}
    )
    phase_vs2_2_post_state = phase_vs2_2_profile.get("post_vs2_2_phase_state", {})
    phase_vs2_2_construction_envelope = phase_vs2_2_profile.get(
        "maximum_construction_envelope", {}
    )
    phase_vs2_2_execution_envelope = phase_vs2_2_profile.get(
        "maximum_future_execution_envelope", {}
    )
    phase_vs2_2_downstream_sequence = phase_vs2_2_profile.get(
        "downstream_construction_sequence", {}
    )
    phase_vs2_2_downstream_objects = phase_vs2_2_profile.get(
        "downstream_construction_objects", {}
    )
    phase_vs2_3_receipt_path = (
        root / PHASE_VS2_3_SCOPE_REGIME_OBJECT_MODEL_DOCS[10]
    )
    phase_vs2_3_receipt_present = phase_vs2_3_receipt_path.exists()
    phase_vs2_3_receipt = (
        json.loads(phase_vs2_3_receipt_path.read_text(encoding="utf-8"))
        if phase_vs2_3_receipt_present
        else {}
    )
    phase_vs2_3_post_state = phase_vs2_3_receipt.get("post_state", {})
    phase_vs2_3_bindings = phase_vs2_3_receipt.get("vs2_3_artifact_bindings", {})
    phase_vs2_3_counts = phase_vs2_3_receipt.get("object_model_counts", {})
    phase_vs2_3_gates = phase_vs2_3_receipt.get("gates", {})
    phase_vs2_3_authority = phase_vs2_3_receipt.get("construction_authority", {})
    phase_vs2_3_receipt_binding = phase_vs2_3_receipt.get("receipt_binding", {})
    phase_vs2_4_receipt_path = root / PHASE_VS2_4_MOVE_SPACE_DOCS[12]
    phase_vs2_4_receipt_present = phase_vs2_4_receipt_path.exists()
    phase_vs2_4_receipt = (
        json.loads(phase_vs2_4_receipt_path.read_text(encoding="utf-8"))
        if phase_vs2_4_receipt_present
        else {}
    )
    phase_vs2_4_post_state = phase_vs2_4_receipt.get("post_state", {})
    phase_vs2_4_bindings = phase_vs2_4_receipt.get("vs2_4_artifact_bindings", {})
    phase_vs2_4_move_hashes = phase_vs2_4_receipt.get("move_hashes", {})
    phase_vs2_4_gates = phase_vs2_4_receipt.get("gates", {})
    phase_vs2_4_authority = phase_vs2_4_receipt.get("construction_authority", {})
    phase_vs2_4_receipt_binding = phase_vs2_4_receipt.get("receipt_binding", {})
    phase_vs2_5_receipt_path = root / PHASE_VS2_5_CONTROLLED_STEP_DOCS[8]
    phase_vs2_5_receipt_present = phase_vs2_5_receipt_path.exists()
    phase_vs2_5_receipt = (
        json.loads(phase_vs2_5_receipt_path.read_text(encoding="utf-8"))
        if phase_vs2_5_receipt_present
        else {}
    )
    phase_vs2_5_post_state = phase_vs2_5_receipt.get("post_state", {})
    phase_vs2_5_bindings = phase_vs2_5_receipt.get("vs2_5_artifact_bindings", {})
    phase_vs2_5_component_hashes = phase_vs2_5_receipt.get("component_hashes", {})
    phase_vs2_5_gates = phase_vs2_5_receipt.get("gates", {})
    phase_vs2_5_authority = phase_vs2_5_receipt.get("construction_authority", {})
    phase_vs2_5_receipt_binding = phase_vs2_5_receipt.get("receipt_binding", {})
    phase_vs2_6_receipt_path = (
        root / PHASE_VS2_6_FIXTURES_REPORTS_READINESS_DOCS[-1]
    )
    phase_vs2_6_receipt_present = phase_vs2_6_receipt_path.exists()
    phase_vs2_6_receipt = (
        json.loads(phase_vs2_6_receipt_path.read_text(encoding="utf-8"))
        if phase_vs2_6_receipt_present
        else {}
    )
    phase_vs2_6_bindings = phase_vs2_6_receipt.get("artifact_bindings", {})
    phase_vs2_6_candidate_bindings = phase_vs2_6_receipt.get(
        "candidate_specimen_bindings", {}
    )
    phase_vs2_6_fixture_definition_bindings = phase_vs2_6_receipt.get(
        "fixture_definition_bindings", {}
    )
    phase_vs2_6_report_bindings = phase_vs2_6_receipt.get(
        "individual_report_contract_bindings", {}
    )
    phase_vs2_6_records = phase_vs2_6_receipt.get(
        "r01_through_r21_result_table", []
    )
    phase_vs2_6_record_statuses = {
        row.get("readiness_component_id"): row.get("readiness_status")
        for row in phase_vs2_6_records
    }
    phase_vs2_7_closure_path = root / PHASE_VS2_7_PHASE_CLOSURE_DOCS[0]
    phase_vs2_7_closure_present = phase_vs2_7_closure_path.exists()
    phase_vs2_7_closure = (
        json.loads(phase_vs2_7_closure_path.read_text(encoding="utf-8"))
        if phase_vs2_7_closure_present
        else {}
    )
    phase_vs2_7_payload = phase_vs2_7_closure.get("closure_payload", {})
    phase_vs2_7_e0 = phase_vs2_7_payload.get("execution_package_core_binding", {})
    phase_vs2_7_rs0 = phase_vs2_7_payload.get("readiness_seal_binding", {})
    phase_vs2_7_authority = phase_vs2_7_payload.get("authority_summary", {})
    phase_vs2_7_execution = phase_vs2_7_payload.get("execution_state", {})
    phase_vs2_7_surface = phase_vs2_7_payload.get("post_phase_decision_surface", {})
    phase_vs2_7_terminal = phase_vs2_7_payload.get("terminal_transition", {})
    phase_vs2_7_receipt_path = root / PHASE_VS2_7_PHASE_CLOSURE_DOCS[-1]
    phase_vs2_7_receipt_present = phase_vs2_7_receipt_path.exists()
    phase_vs2_7_receipt = (
        json.loads(phase_vs2_7_receipt_path.read_text(encoding="utf-8"))
        if phase_vs2_7_receipt_present
        else {}
    )
    phase_vs2_7_receipt_payload = phase_vs2_7_receipt.get("receipt_payload", {})
    post_vs2_surface_path = root / POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_DOCS[0]
    post_vs2_surface_present = post_vs2_surface_path.exists()
    post_vs2_surface = (
        json.loads(post_vs2_surface_path.read_text(encoding="utf-8"))
        if post_vs2_surface_present
        else {}
    )
    post_vs2_payload = post_vs2_surface.get("surface_payload", {})
    post_vs2_e0 = post_vs2_payload.get("execution_package_core_reference", {})
    post_vs2_rs0 = post_vs2_payload.get("readiness_seal_reference", {})
    post_vs2_decision = post_vs2_payload.get("decision_state", {})
    post_vs2_authority = post_vs2_payload.get("authority_state", {})
    post_vs2_execution = post_vs2_payload.get("execution_state", {})
    post_vs2_terminal = post_vs2_payload.get("terminal_transition", {})
    post_vs2_receipt_path = root / POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_DOCS[-1]
    post_vs2_receipt_present = post_vs2_receipt_path.exists()
    post_vs2_receipt = (
        json.loads(post_vs2_receipt_path.read_text(encoding="utf-8"))
        if post_vs2_receipt_present
        else {}
    )
    post_vs2_receipt_payload = post_vs2_receipt.get("receipt_payload", {})
    post_vs2_machinery_receipt_path = root / POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_DOCS[-1]
    post_vs2_machinery_receipt_present = post_vs2_machinery_receipt_path.exists()
    post_vs2_machinery_receipt = (
        json.loads(post_vs2_machinery_receipt_path.read_text(encoding="utf-8"))
        if post_vs2_machinery_receipt_present
        else {}
    )
    post_vs2_machinery_payload = post_vs2_machinery_receipt.get("receipt_binding", {}).get("receipt_payload", {})
    phase_vs2_6_next_unit = (
        "VS2_7_PHASE_CLOSURE_PENDING"
        if phase_vs2_6_receipt_present
        else (
            "VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS_PENDING"
            if phase_vs2_5_receipt_present
            else (
                "VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_PENDING"
                if phase_vs2_4_receipt_present
                else (
                    "VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PENDING"
                    if phase_vs2_3_receipt_present
                    else (
                        "VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PENDING"
                        if phase_vs2_2_profile_present
                        else (
                            "VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_PENDING"
                            if phase_vs2_1_source_intake_present
                            else None
                        )
                    )
                )
            )
        )
    )
    phase_vs2_current_unit = (
        phase_vs2_6_receipt.get("unit_id")
        if phase_vs2_6_receipt_present
        else (
            phase_vs2_5_receipt.get("unit_id")
            if phase_vs2_5_receipt_present
            else (
                phase_vs2_4_receipt.get("unit_id")
                if phase_vs2_4_receipt_present
                else (
                    phase_vs2_3_receipt.get("unit_id")
                    if phase_vs2_3_receipt_present
                    else (
                        phase_vs2_2_profile.get("unit_id")
                        if phase_vs2_2_profile_present
                        else (
                            phase_vs2_1_source_intake.get("unit_id")
                            if phase_vs2_1_source_intake_present
                            else None
                        )
                    )
                )
            )
        )
    )
    if phase_vs2_7_closure_present:
        phase_vs2_current_unit = phase_vs2_7_payload.get(
            "normalized_unit_id",
            "VS2_7_PHASE_CLOSURE",
        )
        phase_vs2_6_next_unit = phase_vs2_7_surface.get(
            "surface_id",
            "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE",
        )
    if post_vs2_surface_present:
        phase_vs2_current_unit = post_vs2_payload.get(
            "unit_id",
            "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_PREPARATION",
        )
        phase_vs2_6_next_unit = "HUMAN_DECISION_REQUIRED"
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
        "human_decision_consumed": False,
        "authority_state_changed": a3_update_present,
        "next_unit_defined": False,
        "next_unit_authorized": False,
        "execution_authorized": False,
        "taxonomy_promoted": False,
        "runner_authority_created": False,
        "human_decision_recorded": a2_receipt_present or a3_update_present,
        "selected_decision_option": "DECISION_ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION" if (a2_receipt_present or a3_update_present) else None,
        "human_acceptance_consumed": a3_update_present,
        "authority_event_formally_consumed": a3_update_present,
        "authority_state_applied": a3_update_present,
        "decision_receipt_applied": a3_update_present,
        "new_authority_state": "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION" if a3_update_present else None,
        "next_allowed_router_action": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE" if a3_update_present else None,
        "basis_for_next_unit_definition_authority": "GRANTED" if a3_update_present else None,
        "next_unit_definition_surface_preparation_authority": "GRANTED" if a3_update_present else None,
        "a3_created": a3_update_present,
        "a4_created": a4_closure_present,
        "block_a_closed": a4_closure_present,
        "block_a_status": "BLOCK_A_PASS_AUTHORITY_ADVANCED_TO_BASIS" if a4_closure_present else None,
        "authority_transition_closure_status": "AUTHORITY_TRANSITION_CLOSURE_PASS" if a4_closure_present else None,
        "block_status": "BLOCK_B_PASS_READ_ONLY_ROUTE_CLASSIFIED" if b3_router_specimen_closure_present else ("BLOCK_A_PASS_AUTHORITY_ADVANCED_TO_BASIS" if a4_closure_present else None),
        "closure_status": "ROUTER_SPECIMEN_CLOSURE_PASS_ALLOWED_PREPARE_ONLY" if b3_router_specimen_closure_present else ("AUTHORITY_TRANSITION_CLOSURE_PASS" if a4_closure_present else None),
        "resulting_authority_state": "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION" if a4_closure_present else None,
        "next_lawful_surface": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE" if a4_closure_present else None,
        "authority_transition_closed": a4_closure_present,
        "requested_action_record_created": b1_requested_action_present,
        "requested_action": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE" if b1_requested_action_present else None,
        "requested_action_scope": "PREPARE_SURFACE_ONLY" if b1_requested_action_present else None,
        "request_status": "REQUEST_DECLARED_FOR_CLASSIFICATION_ONLY" if b1_requested_action_present else None,
        "source_authority_state": "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION" if b1_requested_action_present else None,
        "route_classification_emitted": b2_route_classification_present,
        "router_classification_record_created": b2_route_classification_present,
        "route_disposition": "ROUTE_MACHINE_MAY_PREPARE_ONLY" if b2_route_classification_present else None,
        "classified_action_status": "ADMISSIBLE_AS_SEPARATE_PREPARATION_OBJECT" if b2_route_classification_present else None,
        "allowed_machine_action_scope": "PREPARE_SURFACE_ONLY" if b2_route_classification_present else None,
        "allowed_scope": "C8_N22_BASIS_ONLY" if b2_route_classification_present else None,
        "router_gate_status": "ROUTER_PASS_CLASSIFICATION_ONLY" if b2_route_classification_present else None,
        "requested_action_executed": d4_machine_proceed_present,
        "action_executed": d4_machine_proceed_present,
        "requested_output_created": d4_unit_surface_present,
        "authority_state_changed_by_b1": False,
        "authority_state_changed_by_b2": False,
        "runtime_executed": False,
        "receipt_rewritten": False,
        "reuse_authorized": False,
        "updater_generalized": False,
        "router_authority_created": False,
        "reusable_router_created": False,
        "validator_archive_created": False,
        "router_specimen_closure_created": b3_router_specimen_closure_present,
        "router_specimen_closure_id": "c8.n22.router_specimen_closure.v0" if b3_router_specimen_closure_present else None,
        "route_result_copied_exactly_from_b2": b3_router_specimen_closure_present,
        "next_separately_preparable_object_class": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE_OBJECT" if b3_router_specimen_closure_present else None,
        "specimen_status": "ARCHIVABLE_LOCAL_SPECIMEN" if b3_router_specimen_closure_present else None,
        "next_unit_definition_surface_prepared": d4_unit_surface_present,
        "authority_state_changed_by_b3": False,
        "observed_path_updated": False,
        "observed_path_update_proposed": False,
        "archive_schema_contract_created": c1_archive_schema_contract_present,
        "archive_schema_contract_id": "validator_archive_entry_schema_contract.v0" if c1_archive_schema_contract_present else None,
        "contract_status": "ARCHIVE_SCHEMA_PASS_CONTRACT_DEFINED" if c1_archive_schema_contract_present else None,
        "required_field_group_count": 18 if (c1_archive_schema_contract_present or f1_registry_schema_contract_present) else None,
        "required_field_groups_present": c1_archive_schema_contract_present or f1_registry_schema_contract_present,
        "archive_entry_created": False,
        "candidate_entry_created": False,
        "promotion_granted": d3_active_archive_entry_present,
        "reuse_authority_granted": d3_active_archive_entry_present,
        "active_archive_entry_created": d3_active_archive_entry_present,
        "auto_disposition_allowed": False,
        "candidate_archive_entry_created": c2_candidate_archive_entry_present,
        "candidate_archive_entry_id": "candidate.c8.n22.prepare_next_unit_definition_surface.v0" if c2_candidate_archive_entry_present else None,
        "candidate_entry_gate": "CANDIDATE_ARCHIVE_ENTRY_PASS_REPRESENTABLE_NOT_PROMOTED" if c2_candidate_archive_entry_present else None,
        "candidate_representation_gate": "CANDIDATE_ARCHIVE_ENTRY_PASS_REPRESENTABLE" if c2_candidate_archive_entry_present else None,
        "candidate_non_promotion_gate": "CANDIDATE_ARCHIVE_ENTRY_PASS_NOT_PROMOTED" if c2_candidate_archive_entry_present else None,
        "candidate_audit_created": c3_candidate_archive_audit_present,
        "candidate_audit_id": "c8.n22.candidate_archive_entry.admissibility_audit.v0" if c3_candidate_archive_audit_present else None,
        "candidate_audit_gate": "CANDIDATE_AUDIT_PASS_CONTRACT_CONFORMANT_NOT_PROMOTED" if c3_candidate_archive_audit_present else None,
        "block_closure_status": "BLOCK_C_PASS_CANDIDATE_CONTRACT_CONFORMANT_NOT_PROMOTED" if c3_candidate_archive_audit_present else None,
        "candidate_contract_conformant": c3_candidate_archive_audit_present,
        "candidate_promoted": d3_active_archive_entry_present,
        "candidate_reusable": d3_active_archive_entry_present,
        "candidate_active": d3_active_archive_entry_present,
        "next_possible_separate_surface": "HUMAN_REGISTRY_PROMOTION_DECISION_SURFACE" if f4_trace_registry_candidate_closure_present else ("COMPRESSION_REGISTRY_CANDIDATE_SURFACE" if e4_compression_closure_present else ("HUMAN_PROMOTION_DECISION_SURFACE" if c3_candidate_archive_audit_present else None)),
        "next_possible_surface_created_by_this_audit": False,
        "next_possible_surface_authorized_by_this_audit": False,
        "archive_entry_status": "ARCHIVE_STATUS_PREAPPROVED_ACTIVE" if d3_active_archive_entry_present else ("ARCHIVE_STATUS_CANDIDATE" if c2_candidate_archive_entry_present else None),
        "promotion_status": "PROMOTION_GRANTED_FOR_DECLARED_SCOPE" if d3_active_archive_entry_present else ("PROMOTION_NOT_REQUESTED" if c2_candidate_archive_entry_present else None),
        "reuse_authority_status": "REUSE_AUTHORITY_GRANTED_FOR_DECLARED_SCOPE" if d3_active_archive_entry_present else ("REUSE_AUTHORITY_NOT_GRANTED" if c2_candidate_archive_entry_present else None),
        "activation_status": "ACTIVATION_ACTIVE" if d3_active_archive_entry_present else ("ACTIVATION_NOT_APPLICABLE" if c2_candidate_archive_entry_present else None),
        "radius_limit_now": "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT" if d3_active_archive_entry_present else ("RADIUS_0_CANDIDATE_ONLY" if c2_candidate_archive_entry_present else None),
        "candidate_move_performed": False,
        "authority_changed": False,
        "preparation_surface_created": d4_unit_surface_present,
        "preapproved_archive_entry_created": False,
        "human_promotion_decision_surface_created": False,
        "promotion_decision_surface_created": d1_promotion_decision_surface_present,
        "promotion_decision_surface_id": "c8.n22.candidate_promotion_decision_surface.v0" if d1_promotion_decision_surface_present else None,
        "promotion_decision_surface_gate": "PROMOTION_DECISION_SURFACE_PASS_OPTIONS_PRESENTED_ONLY" if d1_promotion_decision_surface_present else None,
        "decision_options_present": d1_promotion_decision_surface_present,
        "decision_option_count": 5 if d1_promotion_decision_surface_present else None,
        "positive_option_id": "DECISION_PROMOTE_CANDIDATE_FOR_DECLARED_SCOPE" if d1_promotion_decision_surface_present else None,
        "positive_option_radius": "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT" if d1_promotion_decision_surface_present else None,
        "decision_option_selected_by_this_surface": False,
        "promotion_decision_recorded_by_this_surface": False,
        "promotion_granted_by_this_surface": False,
        "reuse_authority_granted_by_this_surface": False,
        "activation_created_by_this_surface": False,
        "active_archive_entry_created_by_this_surface": False,
        "inactive_archive_entry_created_by_this_surface": False,
        "machine_proceed_performed_by_this_surface": False,
        "next_unit_definition_surface_prepared_by_this_surface": False,
        "authority_changed_by_this_surface": False,
        "runner_authority_created_by_this_surface": False,
        "promotion_decision_receipt_created": d2_promotion_decision_receipt_present,
        "promotion_decision_receipt_id": "c8.n22.candidate_promotion_decision_receipt.v0" if d2_promotion_decision_receipt_present else None,
        "promotion_decision_receipt_gate": "PROMOTION_DECISION_RECEIPT_PASS_TYPED_DECISION_RECORDED" if d2_promotion_decision_receipt_present else None,
        "selected_promotion_option": "DECISION_PROMOTE_CANDIDATE_FOR_DECLARED_SCOPE" if d2_promotion_decision_receipt_present else None,
        "decision_actor_class": "HUMAN" if d2_promotion_decision_receipt_present else None,
        "selection_source": "EXPLICIT_HUMAN_SELECTION" if d2_promotion_decision_receipt_present else None,
        "human_selection_explicit": d2_promotion_decision_receipt_present,
        "selected_option_present_on_surface": d2_promotion_decision_receipt_present,
        "selected_option_scope_matches_surface": d2_promotion_decision_receipt_present,
        "next_required_object": None if f4_trace_registry_candidate_closure_present else ("c8_n22_radius_bound_prepare_trace_registry_candidate_closure_v0" if f3_trace_registry_candidate_audit_present else ("c8_n22_radius_bound_prepare_trace_registry_candidate_audit_v0" if f2_trace_registry_candidate_present else ("F2_LOCAL_REGISTRY_CANDIDATE_ENTRY" if f1_registry_schema_contract_present else ("NONE_BLOCK_E_CLOSED" if e4_compression_closure_present else ("E4_COMPRESSION_CLOSURE" if e3_decompression_audit_present else ("E3_DECOMPRESSION_PARITY_AUDIT" if e2_compressed_packet_present else ("E2_COMPRESSED_SPECIMEN_PACKET" if e1_compression_target_present else ("NONE_BLOCK_D_CLOSED" if d5_machine_proceed_closure_present else ("D5_MACHINE_PROCEED_CLOSURE" if d4_machine_proceed_present else ("D4_MACHINE_PROCEED_UNDER_ACTIVE_ENTRY" if d3_active_archive_entry_present else ("c8_n22_prepare_next_unit_definition_active_archive_entry_v0" if d2_promotion_decision_receipt_present else None))))))))))),
        "active_archive_entry_created_by_this_receipt": False,
        "inactive_archive_entry_created_by_this_receipt": False,
        "reuse_authority_applied_by_this_receipt": False,
        "activation_applied_by_this_receipt": False,
        "machine_proceed_performed_by_this_receipt": False,
        "next_unit_definition_surface_prepared_by_this_receipt": False,
        "authority_changed_by_this_receipt": False,
        "runner_authority_created_by_this_receipt": False,
        "c2_created": c2_candidate_archive_entry_present,
        "c3_created": c3_candidate_archive_audit_present,
        "d1_created": d1_promotion_decision_surface_present,
        "d2_created": d2_promotion_decision_receipt_present,
        "d3_created": d3_active_archive_entry_present,
        "d4_created": d4_machine_proceed_present,
        "d5_created": d5_machine_proceed_closure_present,
        "e1_created": e1_compression_target_present,
        "active_archive_entry_materialized": d3_active_archive_entry_present,
        "active_archive_entry_id": "active.c8.n22.prepare_next_unit_definition_surface.v0" if d3_active_archive_entry_present else None,
        "active_archive_entry_materialization_gate": "ACTIVE_ARCHIVE_ENTRY_PASS_MATERIALIZED_FOR_DECLARED_SCOPE" if d3_active_archive_entry_present else None,
        "materialization_role": "ACTIVE_ARCHIVE_ENTRY_STATE_MATERIALIZATION" if d3_active_archive_entry_present else None,
        "materialization_status": "ACTIVE_ARCHIVE_ENTRY_PASS_MATERIALIZED_FOR_DECLARED_SCOPE" if d3_active_archive_entry_present else None,
        "reuse_authority_scope": "DECLARED_SCOPE_ONLY" if d3_active_archive_entry_present else None,
        "activation_scope": "DECLARED_SCOPE_ONLY" if d3_active_archive_entry_present else None,
        "machine_action_scope": "PREPARE_SURFACE_ONLY" if d3_active_archive_entry_present else None,
        "radius_policy": "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT" if d3_active_archive_entry_present else None,
        "radius_initial_count": 1 if d3_active_archive_entry_present else None,
        "radius_remaining_after_d3": 1 if d3_active_archive_entry_present else None,
        "radius_consumed_by_d3": 0 if d3_active_archive_entry_present else None,
        "radius_available_for_d4": d3_active_archive_entry_present,
        "d4_eligibility_active_entry_exists": d3_active_archive_entry_present,
        "d4_eligibility_radius_available": d3_active_archive_entry_present,
        "d4_eligibility_radius_remaining": 1 if d3_active_archive_entry_present else None,
        "d4_must_run_as_separate_unit": d3_active_archive_entry_present,
        "active_archive_entry_created_by_this_materialization": d3_active_archive_entry_present,
        "promotion_status_applied_by_this_materialization": d3_active_archive_entry_present,
        "reuse_authority_status_applied_by_this_materialization": d3_active_archive_entry_present,
        "activation_status_applied_by_this_materialization": d3_active_archive_entry_present,
        "machine_proceed_performed_by_this_materialization": False,
        "next_unit_definition_surface_prepared_by_this_materialization": False,
        "unit_executed_by_this_materialization": False,
        "runner_authority_created_by_this_materialization": False,
        "runtime_executed_by_this_materialization": False,
        "observed_path_updated_by_this_materialization": False,
        "receipt_rewritten_by_this_materialization": False,
        "candidate_rewritten_by_this_materialization": False,
        "scope_expanded_by_this_materialization": False,
        "radius_consumed_by_this_materialization": False,
        "activation_object_created_by_this_materialization": False,
        "machine_proceed_created": d4_machine_proceed_present,
        "machine_proceed_id": "c8.n22.prepare_next_unit_definition_surface.machine_proceed.v0" if d4_machine_proceed_present else None,
        "machine_proceed_gate": "MACHINE_PROCEED_PASS_RADIUS_BOUND_PREPARATION_ONLY" if d4_machine_proceed_present else None,
        "performed_action": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE" if d4_machine_proceed_present else None,
        "performed_action_scope": "PREPARE_SURFACE_ONLY" if d4_machine_proceed_present else None,
        "basis_scope": "C8_N22_BASIS_ONLY" if d4_machine_proceed_present else None,
        "source_object_id": "c8.n22" if d4_machine_proceed_present else None,
        "output_object_id": "c8.n22.next_bounded_unit_definition_surface.v0" if d4_machine_proceed_present else None,
        "output_object_type": "NEXT_BOUNDED_UNIT_DEFINITION_SURFACE" if d4_machine_proceed_present else None,
        "output_scope": "SURFACE_ONLY" if d4_machine_proceed_present else None,
        "output_execution_status": "NOT_EXECUTED" if d4_machine_proceed_present else None,
        "radius_limit": "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT" if d4_machine_proceed_present else None,
        "radius_before": 1 if d4_machine_proceed_present else None,
        "radius_consumed": 1 if d4_machine_proceed_present else None,
        "radius_after": 0 if d4_machine_proceed_present else None,
        "radius_exhausted": d4_machine_proceed_present,
        "radius_renewed_by_this_proceed": False,
        "unit_surface_created": d4_unit_surface_present,
        "unit_surface_id": "c8.n22.next_bounded_unit_definition_surface.v0" if d4_unit_surface_present else None,
        "unit_surface_status": "NEXT_UNIT_DEFINITION_SURFACE_PREPARED_NOT_EXECUTED" if d4_unit_surface_present else None,
        "block_d_closed": d5_machine_proceed_closure_present,
        "block_d_status": "BLOCK_D_PASS_ONE_RADIUS_BOUND_MACHINE_PREPARE_MOVE" if d5_machine_proceed_closure_present else None,
        "machine_proceed_closure_created": d5_machine_proceed_closure_present,
        "machine_proceed_closure_id": "c8.n22.machine_proceed_closure.v0" if d5_machine_proceed_closure_present else None,
        "machine_proceed_closure_gate": "MACHINE_PROCEED_CLOSURE_PASS_RADIUS_EXHAUSTED_STOP" if d5_machine_proceed_closure_present else None,
        "radius_after_d5": 0 if d5_machine_proceed_closure_present else None,
        "same_radius_may_be_reused": False,
        "additional_machine_proceed_authorized": False,
        "radius_renewed_by_closure": False,
        "active_archive_scope_expanded": False,
        "active_archive_entry_rewritten_by_closure": False,
        "active_archive_entry_mutated_by_closure": False,
        "block_e_status": "BLOCK_E_PASS_OBSERVABILITY_COMPRESSION_WITH_DECOMPRESSION_PARITY" if e4_compression_closure_present else ("BLOCK_E_DECOMPRESSION_AUDIT_PASSED" if e3_decompression_audit_present else ("BLOCK_E_COMPRESSED_PACKET_CREATED" if e2_compressed_packet_present else ("BLOCK_E_COMPRESSION_TARGET_DECLARED" if e1_compression_target_present else None))),
        "compression_target_created": e1_compression_target_present,
        "compression_target_id": "c8.n22.authority_action_trace.compression_target.v0" if e1_compression_target_present else None,
        "target_trace_label": "C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0" if e1_compression_target_present else None,
        "compression_mode": "OBSERVABILITY_COMPRESSION_ONLY" if e1_compression_target_present else None,
        "critical_field_group_count": 15 if e1_compression_target_present else None,
        "e2_created": e2_compressed_packet_present,
        "compressed_packet_created": e2_compressed_packet_present,
        "compressed_packet_id": "c8.n22.radius_bound_prepare_trace.compressed_packet.v0" if e2_compressed_packet_present else None,
        "packet_status": "COMPRESSED_PACKET_CREATED_PENDING_DECOMPRESSION_AUDIT" if e2_compressed_packet_present else None,
        "packet_trusted_as_observability_shortcut": e4_compression_closure_present,
        "e3_created": e3_decompression_audit_present,
        "decompression_audit_performed": e3_decompression_audit_present,
        "decompression_audit_id": "c8.n22.radius_bound_prepare_trace.decompression_audit.v0" if e3_decompression_audit_present else None,
        "decompression_audit_status": "DECOMPRESSION_AUDIT_PASS_CRITICAL_FIELD_PARITY" if e3_decompression_audit_present else None,
        "decompression_parity_passed": e3_decompression_audit_present,
        "eligible_for_e4_observability_closure": e3_decompression_audit_present,
        "critical_field_group_count_checked": 15 if e3_decompression_audit_present else None,
        "critical_field_group_count_passed": 15 if e3_decompression_audit_present else None,
        "compressed_summary_matches_sources": e3_decompression_audit_present,
        "source_file_hashes_match_e1_manifest": e3_decompression_audit_present,
        "e4_created": e4_compression_closure_present,
        "compression_closure_created": e4_compression_closure_present,
        "compression_closure_id": "c8.n22.compression_specimen_closure.v0" if e4_compression_closure_present else None,
        "compression_closure_status": "COMPRESSION_CLOSURE_PASS_OBSERVABILITY_ONLY" if e4_compression_closure_present else None,
        "allowed_use": "OBSERVABILITY_SHORTCUT_ONLY" if e4_compression_closure_present else None,
        "formal_source_chain_remains_authority": e4_compression_closure_present,
        "compressed_packet_may_replace_source_authority": False,
        "registry_candidate_surface_created": False,
        "registry_entry_created": False,
        "active_registry_created": False,
        "machine_action_performed_by_closure": False,
        "next_possible_separate_surface_created": False,
        "authority_strengthened_by_compression": False,
        "reuse_authorized_by_compression": False,
        "radius_renewed_by_compression": False,
        "additional_machine_proceed_authorized_by_compression": False,
        "runner_authority_created_by_compression": False,
        "compression_closed": e4_compression_closure_present,
        "compression_registry_created": False,
        "machine_action_performed": False,
        "source_records_replaced": False,
        "block_e_closed": e4_compression_closure_present,
        "compression_passed": e4_compression_closure_present,
        "trace_compressed": e4_compression_closure_present,
        "packet_created": e2_compressed_packet_present,
        "decompression_audit_passed": e3_decompression_audit_present,
        "registry_created": False,
        "unit_executed": False,
        "reuse_scope_expanded": False,
        "additional_radius_created": False,
        "radius_renewed": False,
        "active_archive_entry_rewritten": False,
        "active_archive_entry_mutated": False,
        "runtime_authorized": False,
        "authority_transition_authorized": False,
        "block_f_started": f1_registry_schema_contract_present,
        "block_f_closed": f4_trace_registry_candidate_closure_present,
        "block_f_status": "BLOCK_F_PASS_LOCAL_REGISTRY_CANDIDATE_CLOSED" if f4_trace_registry_candidate_closure_present else ("BLOCK_F_REGISTRY_CANDIDATE_ADMISSIBILITY_AUDIT_PASSED_LOCAL_ONLY" if f3_trace_registry_candidate_audit_present else ("BLOCK_F_LOCAL_REGISTRY_CANDIDATE_CREATED_PENDING_AUDIT" if f2_trace_registry_candidate_present else ("BLOCK_F_REGISTRY_SCHEMA_CONTRACT_DEFINED" if f1_registry_schema_contract_present else None))),
        "registry_schema_contract_created": f1_registry_schema_contract_present,
        "registry_schema_id": "compression_trace_registry_entry_schema_contract.v0" if f1_registry_schema_contract_present else None,
        "schema_role": "REGISTRY_ENTRY_CONTRACT_ONLY" if f1_registry_schema_contract_present else None,
        "registry_kind": "COMPRESSION_TRACE_OBSERVABILITY_REGISTRY" if f1_registry_schema_contract_present else None,
        "schema_scope": "COMPRESSION_STABLE_TRACE_CANDIDATES_ONLY" if f1_registry_schema_contract_present else None,
        "schema_status": "REGISTRY_SCHEMA_PASS_CONTRACT_DEFINED_ONLY" if f1_registry_schema_contract_present else None,
        "registry_schema_gate": "REGISTRY_SCHEMA_PASS_CONTRACT_DEFINED_ONLY" if f1_registry_schema_contract_present else None,
        "registry_entry_activated": False,
        "registry_use_authorized": False,
        "machine_proceed_authorized": False,
        "source_authority_replaced": False,
        "generalized_pattern_created": False,
        "registry_candidate_created": f2_trace_registry_candidate_present,
        "registry_candidate_id": "candidate.registry.c8_n22_radius_bound_prepare_trace.v0" if f2_trace_registry_candidate_present else None,
        "registry_candidate_status": "REGISTRY_STATUS_CANDIDATE" if f2_trace_registry_candidate_present else None,
        "candidate_status": "REGISTRY_STATUS_CANDIDATE" if f2_trace_registry_candidate_present else None,
        "candidate_creation_status": "REGISTRY_CANDIDATE_PASS_CREATED_LOCAL_ONLY_PENDING_AUDIT" if f2_trace_registry_candidate_present else None,
        "admissibility_audit_status": "PENDING_F3_ADMISSIBILITY_AUDIT" if f2_trace_registry_candidate_present else None,
        "admissibility_audit_status_before_f3": "PENDING_F3_ADMISSIBILITY_AUDIT" if f3_trace_registry_candidate_audit_present else None,
        "admissibility_audit_passed": f3_trace_registry_candidate_audit_present,
        "registry_candidate_audit_created": f3_trace_registry_candidate_audit_present,
        "registry_candidate_audit_id": "audit.registry.c8_n22_radius_bound_prepare_trace.candidate_admissibility.v0" if f3_trace_registry_candidate_audit_present else None,
        "registry_candidate_audit_status": "REGISTRY_CANDIDATE_ADMISSIBILITY_AUDIT_PASS_LOCAL_ONLY" if f3_trace_registry_candidate_audit_present else None,
        "registry_candidate_admissibility_audit_gate": "REGISTRY_CANDIDATE_ADMISSIBILITY_AUDIT_PASS_LOCAL_ONLY" if f3_trace_registry_candidate_audit_present else None,
        "audited_candidate_id": "candidate.registry.c8_n22_radius_bound_prepare_trace.v0" if f3_trace_registry_candidate_audit_present else None,
        "candidate_admissible": f3_trace_registry_candidate_audit_present,
        "admissible_scope": "LOCAL_CANDIDATE_ONLY" if f3_trace_registry_candidate_audit_present else None,
        "trace_label": "C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0" if f2_trace_registry_candidate_present else None,
        "trace_scope": "C8_N22_LOCAL_SPECIMEN_ONLY" if f2_trace_registry_candidate_present else None,
        "specimen_count": 1 if f2_trace_registry_candidate_present else None,
        "evidence_kind": "SINGLE_LOCAL_SPECIMEN" if f2_trace_registry_candidate_present else None,
        "generalization_status": "LOCAL_SPECIMEN_ONLY_NOT_GENERALIZED" if f2_trace_registry_candidate_present else None,
        "general_shape_claimed": False,
        "multi_specimen_stability_claimed": False,
        "cross_context_stability_claimed": False,
        "active_registry_entry_created": False,
        "trace_label_promoted": False,
        "source_candidate_modified": False,
        "registry_candidate_closure_created": f4_trace_registry_candidate_closure_present,
        "registry_candidate_closure_id": "c8.n22.radius_bound_prepare_trace.registry_candidate_closure.v0" if f4_trace_registry_candidate_closure_present else None,
        "registry_candidate_closure_gate": "REGISTRY_CANDIDATE_CLOSURE_PASS_CANDIDATE_ONLY" if f4_trace_registry_candidate_closure_present else None,
        "candidate_mutated_by_closure": False,
        "audit_mutated_by_closure": False,
        "f4_closure_created": f4_trace_registry_candidate_closure_present,
        "reusable_trace": False,
        "runner_candidate": False,
        "machine_can_use_candidate": False,
        "next_required_unit": None if f4_trace_registry_candidate_closure_present else ("F4_REGISTRY_CANDIDATE_CLOSURE" if f3_trace_registry_candidate_audit_present else ("F3_REGISTRY_CANDIDATE_ADMISSIBILITY_AUDIT" if f2_trace_registry_candidate_present else None)),
        "next_possible_separate_surface_created_by_this_closure": False,
        "next_possible_separate_surface_authorized_by_this_closure": False,
        "next_possible_separate_surface_selected_by_this_closure": False,
        "next_possible_separate_object_family": "HUMAN_REGISTRY_PROMOTION_DECISION_SURFACE" if f4_trace_registry_candidate_closure_present else ("LOCAL_COMPRESSION_TRACE_REGISTRY_CANDIDATE_ENTRY" if f1_registry_schema_contract_present else None),
        "example_future_candidate_object": "c8_n22_radius_bound_prepare_trace_registry_candidate_v0" if f1_registry_schema_contract_present else None,
        "example_candidate_created_by_f1": False,
        "selected_as_next_unit_by_f1": False,
        "terminal_transition": "STOP_BLOCK_F_REGISTRY_CANDIDATE_CLOSURE_COMPLETE" if f4_trace_registry_candidate_closure_present else ("ADVANCE(F4_REGISTRY_CANDIDATE_CLOSURE_PENDING)" if f3_trace_registry_candidate_audit_present else ("ADVANCE(F3_REGISTRY_CANDIDATE_ADMISSIBILITY_AUDIT_PENDING)" if f2_trace_registry_candidate_present else ("ADVANCE(F2_LOCAL_REGISTRY_CANDIDATE_ENTRY_PENDING)" if f1_registry_schema_contract_present else ("STOP_BLOCK_E_COMPRESSION_CLOSURE_COMPLETE" if e4_compression_closure_present else ("ADVANCE(E4_COMPRESSION_CLOSURE_PENDING)" if e3_decompression_audit_present else ("ADVANCE(E3_DECOMPRESSION_PARITY_AUDIT_PENDING)" if e2_compressed_packet_present else ("ADVANCE(E2_COMPRESSED_SPECIMEN_PACKET_PENDING)" if e1_compression_target_present else ("STOP_BLOCK_D_MACHINE_PROCEED_CLOSED" if d5_machine_proceed_closure_present else ("ADVANCE(D5_MACHINE_PROCEED_CLOSURE_PENDING)" if d4_machine_proceed_present else ("ADVANCE(D4_MACHINE_PROCEED_UNDER_ACTIVE_ENTRY_PENDING)" if d3_active_archive_entry_present else None)))))))))),
        "phase_vs0_status": phase_vs0_closure.get("phase_status") if phase_vs0_closure_present else (phase_vs0_evidence_yield_report_status if phase_vs0_evidence_yield_report_present else (phase_vs0_negative_probe_battery_status if phase_vs0_negative_probe_battery_present else (phase_vs0_happy_path_verification_status if phase_vs0_happy_path_verification_present else ("VS0_2_HAPPY_PATH_BUILD_PASS_A_TO_F_PHASE_SPECIMEN_CREATED" if phase_vs0_happy_path_build_present else ("VS0_PREFLIGHT_PASS_SCOPE_DECLARED" if phase_vs0_source_inventory_present else None))))),
        "phase_vs0_current_unit": "VS0.6_PHASE_CLOSURE" if phase_vs0_closure_present else ("VS0.5_EVIDENCE_YIELD_REPORT" if phase_vs0_evidence_yield_report_present else ("VS0.4.NEGATIVE_SHORTCUT_PROBE_BATTERY" if phase_vs0_negative_probe_battery_present else ("VS0.3_HAPPY_PATH_CLOSURE_VERIFICATION" if phase_vs0_happy_path_verification_present else ("VS0.2_HAPPY_PATH_A_TO_F_ARTIFACT_BUILD" if phase_vs0_happy_path_build_present else ("VS0.1_SOURCE_INVENTORY_AND_PREFLIGHT" if phase_vs0_source_inventory_present else None))))),
        "phase_vs0_start_mode": "FROM_COMMITTED_BLOCK_F_CANDIDATE_CHAIN" if phase_vs0_source_inventory_present else None,
        "phase_vs0_declared_start_source": "c8.n22.radius_bound_prepare_trace.registry_candidate_closure.v0" if phase_vs0_source_inventory_present else None,
        "phase_vs0_declared_start_source_path": "docs/matrixlabs/registry/closures/c8_n22_radius_bound_prepare_trace_registry_candidate_closure_v0.json" if phase_vs0_source_inventory_present else None,
        "phase_vs0_preflight_decision": "PROCEED_TO_VS0_2_HAPPY_PATH_BUILD" if phase_vs0_source_inventory_present else None,
        "phase_vs0_evidence_yield_branch": phase_vs0_yield.get("battery_yield_branch") if phase_vs0_negative_probe_battery_present else (phase_vs0_happy_path_verification.get("evidence_yield_class", {}).get("yield_branch") if phase_vs0_happy_path_verification_present else ("CONFIRMATION_YIELD" if phase_vs0_source_inventory_present else None)),
        "phase_vs0_required_start_sources_missing": False,
        "phase_vs0_expected_outputs_namespace": "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0" if phase_vs0_source_inventory_present else None,
        "phase_vs0_expected_vs0_outputs_missing_treated_as_failure": False,
        "phase_vs0_a_to_f_specimen_built_by_vs0_1": False,
        "phase_vs0_authority_changed_by_vs0_1": False,
        "phase_vs0_machine_action_performed_by_vs0_1": False,
        "phase_vs0_radius_renewed_by_vs0_1": False,
        "phase_vs0_registry_activated_by_vs0_1": False,
        "phase_vs0_runner_authority_created_by_vs0_1": False,
        "phase_vs0_phase_closure_created_by_vs0_1": False,
        "phase_vs0_discussion_packets_committed": False,
        "phase_vs0_happy_path_build_receipt_created": phase_vs0_happy_path_build_present,
        "phase_vs0_happy_path_build_receipt_id": "phase_vs0_happy_path_build_receipt_v0" if phase_vs0_happy_path_build_present else None,
        "phase_vs0_happy_path_build_gate": "VS0_2_HAPPY_PATH_BUILD_PASS_A_TO_F_PHASE_SPECIMEN_CREATED" if phase_vs0_happy_path_build_present else None,
        "phase_vs0_a_chain_built": phase_vs0_happy_path_build_present,
        "phase_vs0_b_chain_built": phase_vs0_happy_path_build_present,
        "phase_vs0_c_chain_built": phase_vs0_happy_path_build_present,
        "phase_vs0_d_chain_built": phase_vs0_happy_path_build_present,
        "phase_vs0_e_chain_built": phase_vs0_happy_path_build_present,
        "phase_vs0_f_chain_built": phase_vs0_happy_path_build_present,
        "phase_vs0_d4_machine_preparation_action_performed": phase_vs0_happy_path_build_present,
        "phase_vs0_machine_action_count": 1 if phase_vs0_happy_path_build_present else 0,
        "phase_vs0_d5_radius_after": 0 if phase_vs0_happy_path_build_present else None,
        "phase_vs0_d5_radius_exhausted": phase_vs0_happy_path_build_present,
        "phase_vs0_independent_cross_block_verification_performed": False,
        "phase_vs0_phase_closure_performed": phase_vs0_closure_passed,
        "phase_vs0_active_registry_created": False,
        "phase_vs0_trace_generalized": False,
        "phase_vs0_radius_renewed_after_d5": False,
        "phase_vs0_additional_machine_proceed_authorized": False,
        "phase_vs0_next_unit_executed": False,
        "phase_vs0_runtime_executed": False,
        "phase_vs0_source_authority_replaced_by_compression": False,
        "phase_vs0_runner_authority_created": phase_vs0_closure_boundaries.get("runner_authority_created", False) if phase_vs0_closure_present else False,
        "phase_vs0_happy_path_verification_id": "phase_vs0_happy_path_verification_v0" if phase_vs0_happy_path_verification_present else None,
        "phase_vs0_source_build_commit_sha": "49ebcf1393893bbbc61c5fcd48359770c3e554e7" if phase_vs0_happy_path_verification_present else None,
        "phase_vs0_chain_index_hash_verification": phase_vs0_happy_path_verification.get("chain_index_hash_verification", {}).get("chain_index_status") if phase_vs0_happy_path_verification_passed else phase_vs0_happy_path_verification_status,
        "phase_vs0_phase_artifact_json_count": phase_vs0_happy_path_verification.get("chain_index_hash_verification", {}).get("phase_artifact_json_count"),
        "phase_vs0_all_indexed_artifact_hashes_match_current_file_content": phase_vs0_happy_path_verification_passed,
        "phase_vs0_a_to_f_chain_verified_under_declared_gates": phase_vs0_happy_path_verification.get("verification_result", {}).get("a_to_f_chain_verified_under_declared_gates", False),
        "phase_vs0_semantic_leak_detected": phase_vs0_happy_path_verification.get("verification_result", {}).get("semantic_leak_detected", False),
        "phase_vs0_authority_smuggling_detected": phase_vs0_happy_path_verification.get("verification_result", {}).get("authority_smuggling_detected", False),
        "phase_vs0_vs0_3_built_new_a_to_f_artifacts": False,
        "phase_vs0_vs0_3_repaired_a_to_f_artifacts": False,
        "phase_vs0_vs0_3_reran_vs0_2_builder": False,
        "phase_vs0_vs0_3_ran_negative_probes": False,
        "phase_vs0_vs0_3_closed_phase": False,
        "phase_vs0_negative_probe_battery_id": "phase_vs0_negative_probe_battery_v0" if phase_vs0_negative_probe_battery_present else None,
        "phase_vs0_probe_execution_mode": phase_vs0_negative_probe_battery.get("probe_execution_mode", {}).get("probe_execution_mode"),
        "phase_vs0_source_happy_path_verification_commit_sha": phase_vs0_negative_probe_battery.get("source_happy_path_verification", {}).get("source_happy_path_verification_commit_sha"),
        "phase_vs0_probe_count_expected": phase_vs0_probe_summary.get("probe_count_expected"),
        "phase_vs0_probe_count_run": phase_vs0_probe_summary.get("probe_count_run"),
        "phase_vs0_expected_typed_stop_count": phase_vs0_probe_summary.get("expected_typed_stop_count"),
        "phase_vs0_observed_typed_stop_count": phase_vs0_probe_summary.get("observed_typed_stop_count"),
        "phase_vs0_unexpected_pass_count": phase_vs0_probe_summary.get("unexpected_pass_count"),
        "phase_vs0_wrong_stop_code_count": phase_vs0_probe_summary.get("wrong_stop_code_count"),
        "phase_vs0_ambiguous_stop_count": phase_vs0_probe_summary.get("ambiguous_stop_count"),
        "phase_vs0_diagnostic_fields_missing_count": phase_vs0_probe_summary.get("diagnostic_fields_missing_count"),
        "phase_vs0_next_lawful_surface_missing_count": phase_vs0_probe_summary.get("next_lawful_surface_missing_count"),
        "phase_vs0_self_repair_attempt_count": phase_vs0_probe_summary.get("self_repair_attempt_count"),
        "phase_vs0_happy_path_mutation_count": phase_vs0_probe_summary.get("happy_path_mutation_count"),
        "phase_vs0_canonical_source_chain_mutation_count": phase_vs0_probe_summary.get("canonical_source_chain_mutation_count"),
        "phase_vs0_a_to_f_hash_manifest_unchanged": phase_vs0_preservation.get("a_to_f_hash_manifest_unchanged"),
        "phase_vs0_canonical_source_chain_hash_manifest_unchanged": phase_vs0_preservation.get("canonical_source_chain_hash_manifest_unchanged"),
        "phase_vs0_radius_renewed": phase_vs0_battery_result.get("radius_renewed", False),
        "phase_vs0_source_authority_replaced": phase_vs0_battery_result.get("source_authority_replaced", False),
        "phase_vs0_battery_yield_branch": phase_vs0_yield.get("battery_yield_branch"),
        "phase_vs0_probe_yield_branch": phase_vs0_yield.get("probe_yield_branch"),
        "phase_vs0_selected_probe_battery_only": phase_vs0_coverage.get("selected_probe_battery_only"),
        "phase_vs0_all_possible_illegal_shortcuts_tested": phase_vs0_coverage.get("all_possible_illegal_shortcuts_tested"),
        "phase_vs0_future_live_runtime_coverage_claimed": phase_vs0_coverage.get("future_live_runtime_coverage_claimed"),
        "phase_vs0_phase_closure_claimed": phase_vs0_coverage.get("phase_closure_claimed"),
        "phase_vs0_negative_probe_battery_passed": phase_vs0_negative_probe_battery_passed,
        "phase_vs0_evidence_yield_report_id": "phase_vs0_evidence_yield_report_v0" if phase_vs0_evidence_yield_report_present else None,
        "phase_vs0_source_vs0_4_commit_sha": phase_vs0_evidence_yield_report.get("source_commits", {}).get("source_vs0_4_commit_sha"),
        "phase_vs0_closure_id": phase_vs0_closure.get("closure_id") if phase_vs0_closure_present else None,
        "phase_vs0_closure_gate": phase_vs0_closure_gate,
        "phase_vs0_closed": phase_vs0_closure_claim_scope.get("phase_vs0_closed", False) if phase_vs0_closure_present else False,
        "phase_vs0_local_phase_pass": phase_vs0_closure_pass_scope.get("local_phase_pass", False) if phase_vs0_closure_present else False,
        "phase_vs0_source_vs0_5_commit_sha": phase_vs0_closure_source_commits.get("vs0_5_evidence_yield_report_commit_sha"),
        "phase_vs0_next_lawful_surface": phase_vs0_closure_next_surface.get("surface_name"),
        "phase_vs0_next_surface_created_by_vs0_6": phase_vs0_closure_next_surface.get("surface_artifact_created_by_closure", False) if phase_vs0_closure_present else False,
        "phase_vs0_next_phase_auto_selected": phase_vs0_closure_next_surface.get("next_phase_auto_selected", False) if phase_vs0_closure_present else False,
        "phase_vs0_total_illegal_path_coverage_claimed": phase_vs0_closure_coverage.get("all_possible_illegal_shortcuts_tested", False) if phase_vs0_closure_present else False,
        "phase_vs0_confirmation_yield_event_count": phase_vs0_yield_summary.get("confirmation_yield_events"),
        "phase_vs0_diagnostic_yield_event_count": phase_vs0_yield_summary.get("diagnostic_yield_events"),
        "phase_vs0_total_decision_relevant_events": phase_vs0_yield_summary.get("total_decision_relevant_events"),
        "phase_vs0_event_count_is_descriptive_not_value_claim": phase_vs0_yield_summary.get("event_count_is_descriptive_not_value_claim"),
        "phase_vs0_decision_relevant_evidence_present": phase_vs0_yield_summary.get("decision_relevant_evidence_present"),
        "phase_vs0_sufficient_input_for_vs0_6_phase_closure": phase_vs0_closure_readiness.get("sufficient_input_for_vs0_6_phase_closure"),
        "phase_vs0_phase_closure_performed_by_vs0_5": phase_vs0_closure_readiness.get("vs0_6_phase_closure_performed", False),
        "phase_vs0_phase_closed": phase_vs0_closure_claim_scope.get("phase_vs0_closed", False) if phase_vs0_closure_present else phase_vs0_closure_readiness.get("phase_closed", False),
        "phase_vs0_coverage_overclaim_detected": phase_vs0_overclaim_guard.get("coverage_overclaim_detected", False),
        "phase_vs0_performance_optimization_claimed": phase_vs0_closure_boundaries.get("performance_optimization_claimed", False) if phase_vs0_closure_present else phase_vs0_overclaim_guard.get("performance_optimization_claimed", False),
        "phase_vs0_scale_optimization_claimed": phase_vs0_closure_boundaries.get("scale_optimization_claimed", False) if phase_vs0_closure_present else phase_vs0_overclaim_guard.get("scale_optimization_claimed", False),
        "phase_vs0_active_registry_claimed": phase_vs0_closure_boundaries.get("active_registry_created", False) if phase_vs0_closure_present else phase_vs0_overclaim_guard.get("active_registry_claimed", False),
        "phase_vs0_registry_promotion_claimed": phase_vs0_closure_claim_scope.get("registry_closed_or_promoted", False) if phase_vs0_closure_present else phase_vs0_overclaim_guard.get("registry_promotion_claimed", False),
        "phase_vs0_trace_generalization_claimed": phase_vs0_closure_boundaries.get("trace_generalized", False) if phase_vs0_closure_present else phase_vs0_overclaim_guard.get("trace_generalization_claimed", False),
        "phase_vs0_runner_readiness_claimed": phase_vs0_closure_boundaries.get("runner_readiness_claimed", False) if phase_vs0_closure_present else phase_vs0_overclaim_guard.get("runner_readiness_claimed", False),
        "phase_vs0_evidence_yield_report_passed": phase_vs0_evidence_yield_report_passed,
        "phase_vs0_next_required_object": phase_vs0_closure_next_surface.get("surface_name") if phase_vs0_closure_passed else (phase_vs0_evidence_yield_report.get("next_required_object") if phase_vs0_evidence_yield_report_passed else (phase_vs0_negative_probe_battery.get("next_required_object") if phase_vs0_negative_probe_battery_passed else (phase_vs0_happy_path_verification.get("next_required_object") if phase_vs0_happy_path_verification_passed else ("phase_vs0_happy_path_verification_v0" if not phase_vs0_happy_path_verification_present and phase_vs0_happy_path_build_present else None)))),
        "phase_vs0_terminal_transition": phase_vs0_closure.get("terminal_transition") if phase_vs0_closure_present else (phase_vs0_evidence_yield_report.get("terminal_transition") if phase_vs0_evidence_yield_report_present else (phase_vs0_negative_probe_battery.get("terminal_transition") if phase_vs0_negative_probe_battery_present else (phase_vs0_happy_path_verification.get("terminal_transition") if phase_vs0_happy_path_verification_present else ("ADVANCE(VS0_3_HAPPY_PATH_CLOSURE_VERIFICATION_PENDING)" if phase_vs0_happy_path_build_present else ("ADVANCE(VS0_2_HAPPY_PATH_A_TO_F_ARTIFACT_BUILD_PENDING)" if phase_vs0_source_inventory_present else None))))),
        "post_vs0_direction_decision_receipt_id": post_vs0_direction_receipt.get("decision_receipt_id") if post_vs0_direction_receipt_present else None,
        "post_vs0_direction_decision_status": post_vs0_direction_receipt.get("receipt_gate") if post_vs0_direction_receipt_present else None,
        "post_vs0_direction_decision": post_vs0_direction_decision.get("decision"),
        "post_vs0_direction_allowed_scope": post_vs0_direction_decision.get("decision_scope"),
        "post_vs0_direction_source_closure_commit_sha": post_vs0_direction_source_closure.get("source_closure_commit_sha"),
        "post_vs0_direction_next_unit": post_vs0_direction_next_unit.get("next_unit_id"),
        "post_vs0_direction_controlled_loop_execution_authorized": post_vs0_direction_forbidden_scope.get("controlled_loop_execution_authorized", False) if post_vs0_direction_receipt_present else False,
        "post_vs0_direction_runner_creation_authorized": post_vs0_direction_forbidden_scope.get("runner_creation_authorized", False) if post_vs0_direction_receipt_present else False,
        "post_vs0_direction_move_execution_authorized": post_vs0_direction_forbidden_scope.get("move_execution_authorized", False) if post_vs0_direction_receipt_present else False,
        "post_vs0_direction_micro_sweeps_authorized": post_vs0_direction_forbidden_scope.get("micro_sweeps_authorized", False) if post_vs0_direction_receipt_present else False,
        "post_vs0_direction_registry_activation_authorized": post_vs0_direction_forbidden_scope.get("registry_activation_authorized", False) if post_vs0_direction_receipt_present else False,
        "post_vs0_direction_trace_generalization_authorized": post_vs0_direction_forbidden_scope.get("trace_generalization_authorized", False) if post_vs0_direction_receipt_present else False,
        "post_vs0_direction_next_phase_selected_by_machine": post_vs0_direction_forbidden_scope.get("next_phase_selected_by_machine", False) if post_vs0_direction_receipt_present else False,
        "phase_vs1_current_unit": phase_vs1_closure.get("unit_id") if phase_vs1_closure_present else (phase_vs1_next_surface_map.get("unit_id") if phase_vs1_next_surface_map_present else (phase_vs1_readiness_audit.get("unit_id") if phase_vs1_readiness_audit_present else (phase_vs1_precondition_inventory.get("unit_id") if phase_vs1_precondition_inventory_present else (phase_vs1_controlled_loop_contract.get("unit_id") if phase_vs1_controlled_loop_contract_present else (phase_vs1_source_intake.get("unit_id") if phase_vs1_source_intake_present else None))))),
        "phase_vs1_source_intake_id": phase_vs1_source_intake.get("artifact_id") if phase_vs1_source_intake_present else None,
        "phase_vs1_source_intake_verdict": phase_vs1_source_intake.get("intake_verdict") if phase_vs1_source_intake_present else None,
        "phase_vs1_source_intake_scope": phase_vs1_source_intake_scope.get("scope"),
        "phase_vs1_source_intake_source_direction_receipt_commit_sha": phase_vs1_source_intake_authority.get("decision_artifact_commit_sha"),
        "phase_vs1_source_intake_source_vs0_6_commit_sha": phase_vs1_source_intake_vs0_6.get("source_vs0_6_closure_commit_sha"),
        "phase_vs1_source_intake_may_feed_vs1_2_contract_definition": phase_vs1_source_intake_scope.get("may_feed_vs1_2_contract_definition"),
        "phase_vs1_source_intake_may_feed_loop_execution": phase_vs1_source_intake_scope.get("may_feed_loop_execution", False) if phase_vs1_source_intake_present else False,
        "phase_vs1_source_intake_controlled_loop_execution_authorized": phase_vs1_source_intake_boundary.get("controlled_loop_execution_authorized", False) if phase_vs1_source_intake_present else False,
        "phase_vs1_source_intake_runner_authority_created": phase_vs1_source_intake_boundary.get("runner_authority_created", False) if phase_vs1_source_intake_present else False,
        "phase_vs1_source_intake_registry_activation_authorized": phase_vs1_source_intake_scope.get("may_feed_registry_activation", False) if phase_vs1_source_intake_present else False,
        "phase_vs1_source_intake_trace_generalization_authorized": phase_vs1_source_intake_scope.get("may_feed_trace_generalization", False) if phase_vs1_source_intake_present else False,
        "phase_vs1_source_intake_next_transition": phase_vs1_source_intake.get("terminal_transition") if phase_vs1_source_intake_present else None,
        "phase_vs1_controlled_loop_contract_id": phase_vs1_controlled_loop_contract.get("artifact_id") if phase_vs1_controlled_loop_contract_present else None,
        "phase_vs1_controlled_loop_contract_verdict": phase_vs1_controlled_loop_contract.get("contract_verdict") if phase_vs1_controlled_loop_contract_present else None,
        "phase_vs1_controlled_loop_name": phase_vs1_contract_loop.get("loop_name"),
        "phase_vs1_controlled_loop_short_name": phase_vs1_contract_loop.get("short_name"),
        "phase_vs1_controlled_loop_contract_status": phase_vs1_contract_loop.get("contract_status"),
        "phase_vs1_source_intake_commit_sha": phase_vs1_contract_source_intake.get("commit_sha"),
        "phase_vs1_component_count_declared": len(phase_vs1_controlled_loop_contract.get("required_components", [])) if phase_vs1_controlled_loop_contract_present else 0,
        "phase_vs1_components_inventoried": phase_vs1_contract_components.get("components_inventoried", False) if phase_vs1_controlled_loop_contract_present else False,
        "phase_vs1_all_components_present": phase_vs1_contract_components.get("all_components_present", False) if phase_vs1_controlled_loop_contract_present else False,
        "phase_vs1_contract_authorized_for_execution": phase_vs1_contract_boundary.get("contract_authorized_for_execution", False) if phase_vs1_controlled_loop_contract_present else False,
        "phase_vs1_contract_readiness_certified": phase_vs1_contract_boundary.get("contract_readiness_certified", False) if phase_vs1_controlled_loop_contract_present else False,
        "phase_vs1_controlled_loop_execution_authorized": phase_vs1_contract_loop.get("execution_authorized", False) if phase_vs1_controlled_loop_contract_present else False,
        "phase_vs1_runner_created": phase_vs1_contract_loop.get("runner_created", False) if phase_vs1_controlled_loop_contract_present else False,
        "phase_vs1_micro_sweeps_authorized": phase_vs1_contract_loop.get("micro_sweeps_authorized", False) if phase_vs1_controlled_loop_contract_present else False,
        "phase_vs1_local_revision_authorized": phase_vs1_contract_loop.get("local_revision_authorized", False) if phase_vs1_controlled_loop_contract_present else False,
        "phase_vs1_portability_claimed": phase_vs1_contract_loop.get("portability_claimed", False) if phase_vs1_controlled_loop_contract_present else False,
        "phase_vs1_global_generalization_claimed": phase_vs1_contract_loop.get("global_generalization_claimed", False) if phase_vs1_controlled_loop_contract_present else False,
        "phase_vs1_performance_optimization_claimed": phase_vs1_contract_loop.get("performance_optimization_claimed", False) if phase_vs1_controlled_loop_contract_present else False,
        "phase_vs1_scale_optimization_claimed": phase_vs1_contract_loop.get("scale_optimization_claimed", False) if phase_vs1_controlled_loop_contract_present else False,
        "phase_vs1_next_transition": phase_vs1_closure_terminal.get("transition") if phase_vs1_closure_present else (phase_vs1_next_surface_terminal.get("transition") if phase_vs1_next_surface_map_present else (phase_vs1_readiness_terminal.get("transition") if phase_vs1_readiness_audit_present else (phase_vs1_precondition_inventory_terminal.get("transition") if phase_vs1_precondition_inventory_present else (phase_vs1_contract_terminal.get("transition") if phase_vs1_controlled_loop_contract_present else None)))),
        "phase_vs1_controlled_loop_precondition_inventory_id": phase_vs1_precondition_inventory.get("artifact_id") if phase_vs1_precondition_inventory_present else None,
        "phase_vs1_controlled_loop_precondition_inventory_verdict": phase_vs1_precondition_inventory.get("inventory_verdict") if phase_vs1_precondition_inventory_present else None,
        "phase_vs1_source_contract_commit_sha": phase_vs1_precondition_inventory_source_contract.get("commit_sha"),
        "phase_vs1_inventory_required_components_total": phase_vs1_precondition_inventory_counts.get("required_components_total"),
        "phase_vs1_all_required_components_inventoried": len(phase_vs1_precondition_inventory.get("component_records", [])) == phase_vs1_precondition_inventory_counts.get("required_components_total", 0) if phase_vs1_precondition_inventory_present else False,
        "phase_vs1_component_set_matches_vs1_2_contract": list(phase_vs1_precondition_inventory.get("component_status_table", {}).keys()) == phase_vs1_controlled_loop_contract.get("required_components", []) if phase_vs1_precondition_inventory_present else False,
        "phase_vs1_readiness_audit_performed": phase_vs1_precondition_inventory_mode.get("readiness_audit_performed", False) if phase_vs1_precondition_inventory_present else False,
        "phase_vs1_repairs_allowed": phase_vs1_precondition_inventory_mode.get("repairs_allowed", False) if phase_vs1_precondition_inventory_present else False,
        "phase_vs1_promotions_allowed": phase_vs1_precondition_inventory_mode.get("promotions_allowed", False) if phase_vs1_precondition_inventory_present else False,
        "phase_vs1_missing_components_ranked": phase_vs1_precondition_inventory_repair_boundary.get("missing_components_ranked", False) if phase_vs1_precondition_inventory_present else False,
        "phase_vs1_next_component_to_build_selected": phase_vs1_precondition_inventory_repair_boundary.get("next_component_to_build_selected", False) if phase_vs1_precondition_inventory_present else False,
        "phase_vs1_repair_plan_created": phase_vs1_precondition_inventory_repair_boundary.get("repair_plan_created", False) if phase_vs1_precondition_inventory_present else False,
        "phase_vs1_loop_execution_authorized": phase_vs1_precondition_inventory_mode.get("loop_execution_authorized", False) if phase_vs1_precondition_inventory_present else False,
        "phase_vs1_runner_authority_created": phase_vs1_precondition_inventory_non_claims.get("runner_authority_exists", False) if phase_vs1_precondition_inventory_present else False,
        "phase_vs1_micro_sweeps_authorized": phase_vs1_precondition_inventory_non_claims.get("micro_sweeps_authorized", False) if phase_vs1_precondition_inventory_present else False,
        "phase_vs1_local_revision_authorized": phase_vs1_precondition_inventory_non_claims.get("local_revision_authorized", False) if phase_vs1_precondition_inventory_present else False,
        "phase_vs1_vs1_4_executed": phase_vs1_precondition_inventory_terminal.get("executes_vs1_4", False) if phase_vs1_precondition_inventory_present else False,
        "phase_vs1_controlled_loop_readiness_audit_id": phase_vs1_readiness_audit.get("artifact_id") if phase_vs1_readiness_audit_present else None,
        "phase_vs1_controlled_loop_readiness_audit_gate": phase_vs1_readiness_audit.get("readiness_audit_gate") if phase_vs1_readiness_audit_present else None,
        "phase_vs1_source_inventory_commit_sha": phase_vs1_readiness_source_inventory.get("commit_sha"),
        "phase_vs1_loop_name": phase_vs1_readiness_target.get("loop_name"),
        "phase_vs1_loop_short_name": phase_vs1_readiness_target.get("short_name"),
        "phase_vs1_readiness_profile": phase_vs1_readiness_profile.get("profile_id"),
        "phase_vs1_controlled_loop_ready": phase_vs1_readiness_aggregate.get("controlled_loop_ready", False) if phase_vs1_readiness_audit_present else False,
        "phase_vs1_ready_for_human_execution_authority_decision": phase_vs1_readiness_aggregate.get("ready_for_human_execution_authority_decision", False) if phase_vs1_readiness_audit_present else False,
        "phase_vs1_human_execution_authority_decision_requested_by_vs1_4": phase_vs1_readiness_aggregate.get("human_execution_authority_decision_requested_by_vs1_4", False) if phase_vs1_readiness_audit_present else False,
        "phase_vs1_ready_component_count": phase_vs1_readiness_aggregate.get("ready_component_count"),
        "phase_vs1_missing_or_blocked_component_count": phase_vs1_readiness_aggregate.get("missing_or_blocked_component_count"),
        "phase_vs1_primary_verdict": phase_vs1_readiness_aggregate.get("primary_verdict"),
        "phase_vs1_loop_execution_authorized": phase_vs1_readiness_execution.get("loop_execution_authorized", False) if phase_vs1_readiness_audit_present else False,
        "phase_vs1_runner_created": phase_vs1_readiness_execution.get("runner_created", False) if phase_vs1_readiness_audit_present else False,
        "phase_vs1_micro_sweeps_authorized": phase_vs1_readiness_execution.get("micro_sweeps_authorized", False) if phase_vs1_readiness_audit_present else False,
        "phase_vs1_local_revision_authorized": phase_vs1_readiness_execution.get("local_revision_authorized", False) if phase_vs1_readiness_audit_present else False,
        "phase_vs1_vs1_5_built": phase_vs1_readiness_vs1_5.get("vs1_5_built", False) if phase_vs1_readiness_audit_present else False,
        "phase_vs1_vs1_5_run": phase_vs1_readiness_vs1_5.get("vs1_5_run", False) if phase_vs1_readiness_audit_present else False,
        "phase_vs1_missing_precondition_next_surface_map_created": phase_vs1_readiness_vs1_5.get("missing_precondition_next_surface_map_created", False) if phase_vs1_readiness_audit_present else False,
        "phase_vs1_next_surfaces_ranked": phase_vs1_readiness_vs1_5.get("next_surfaces_ranked", False) if phase_vs1_readiness_audit_present else False,
        "phase_vs1_repair_sequence_created": phase_vs1_readiness_vs1_5.get("repair_sequence_created", False) if phase_vs1_readiness_audit_present else False,
        "phase_vs1_component_build_authorized": phase_vs1_readiness_vs1_5.get("component_build_authorized", False) if phase_vs1_readiness_audit_present else False,
        "phase_vs1_missing_precondition_next_surface_map_id": phase_vs1_next_surface_map.get("artifact_id") if phase_vs1_next_surface_map_present else None,
        "phase_vs1_missing_precondition_next_surface_map_verdict": phase_vs1_next_surface_map.get("map_verdict") if phase_vs1_next_surface_map_present else None,
        "phase_vs1_source_readiness_audit_commit_sha": phase_vs1_next_surface_source.get("commit_sha") if phase_vs1_next_surface_map_present else None,
        "phase_vs1_mapping_branch": phase_vs1_next_surface_map.get("mapping_branch") if phase_vs1_next_surface_map_present else None,
        "phase_vs1_source_blocker_count": phase_vs1_next_surface_coverage.get("source_blocker_count") if phase_vs1_next_surface_map_present else None,
        "phase_vs1_mapped_blocker_count": phase_vs1_next_surface_coverage.get("mapped_blocker_count") if phase_vs1_next_surface_map_present else None,
        "phase_vs1_unmapped_blocker_count": phase_vs1_next_surface_coverage.get("unmapped_blocker_count") if phase_vs1_next_surface_map_present else None,
        "phase_vs1_all_typed_blockers_mapped": phase_vs1_next_surface_coverage.get("all_typed_blockers_mapped", False) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_surface_candidate_records_created": all(
            candidate.get("surface_candidate_record_created_by_vs1_5") is True
            for candidate in phase_vs1_next_surface_map.get("surface_candidates", [])
        ) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_surface_artifacts_created": phase_vs1_next_surface_forbidden.get("surface_artifact_created", False) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_surfaces_built": phase_vs1_next_surface_forbidden.get("surface_built", False) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_advisory_ranking_enabled": phase_vs1_next_surface_ranking_policy.get("ranking_enabled", False) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_advisory_ranking_is_binding": phase_vs1_next_surface_ranking_policy.get("ranking_is_binding", False) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_advisory_first_surface_candidate": phase_vs1_next_surface_ranking.get("advisory_first_surface_candidate") if phase_vs1_next_surface_map_present else None,
        "phase_vs1_machine_selected_next_phase": phase_vs1_next_surface_ranking.get("machine_selected_next_phase", False) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_surface_build_authorized": phase_vs1_next_surface_policy.get("component_build_allowed", False) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_repair_attempted": phase_vs1_next_surface_forbidden.get("repair_attempted", False) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_component_build_attempted": phase_vs1_next_surface_forbidden.get("component_build_attempted", False) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_candidate_promotion_attempted": phase_vs1_next_surface_forbidden.get("candidate_promotion_attempted", False) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_loop_execution_authorized": phase_vs1_next_surface_policy.get("loop_execution_authorized", False) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_runner_created": phase_vs1_next_surface_policy.get("runner_created", False) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_micro_sweeps_authorized": phase_vs1_next_surface_forbidden.get("micro_sweeps_authorized", False) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_local_revision_authorized": phase_vs1_next_surface_forbidden.get("local_revision_authorized", False) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_vs1_6_built": phase_vs1_next_surface_vs1_6.get("vs1_6_built", False) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_vs1_6_run": phase_vs1_next_surface_vs1_6.get("vs1_6_run", False) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_phase_closure_claimed": phase_vs1_next_surface_forbidden.get("phase_closure_claimed", False) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_post_vs1_phase_selected": phase_vs1_next_surface_forbidden.get("post_vs1_phase_selected", False) if phase_vs1_next_surface_map_present else False,
        "phase_vs1_closure_id": phase_vs1_closure.get("artifact_id") if phase_vs1_closure_present else None,
        "phase_vs1_closure_gate": phase_vs1_closure.get("closure_gate") if phase_vs1_closure_present else None,
        "phase_vs1_phase_status": phase_vs1_closure.get("phase_status") if phase_vs1_closure_present else None,
        "phase_vs1_closure_branch": phase_vs1_closure.get("closure_branch") if phase_vs1_closure_present else None,
        "phase_vs1_closed": phase_vs1_closure_terminal.get("phase_vs1_closed", False) if phase_vs1_closure_present else False,
        "phase_vs1_source_chain_complete": len(phase_vs1_closure.get("source_chain", {})) == 5 if phase_vs1_closure_present else False,
        "phase_vs1_source_chain_vs1_1_commit_sha": phase_vs1_closure_source_chain.get("vs1_1_commit_sha"),
        "phase_vs1_source_chain_vs1_2_commit_sha": phase_vs1_closure_source_chain.get("vs1_2_commit_sha"),
        "phase_vs1_source_chain_vs1_3_commit_sha": phase_vs1_closure_source_chain.get("vs1_3_commit_sha"),
        "phase_vs1_source_chain_vs1_4_commit_sha": phase_vs1_closure_source_chain.get("vs1_4_commit_sha"),
        "phase_vs1_source_chain_vs1_5_commit_sha": phase_vs1_closure_source_chain.get("vs1_5_commit_sha"),
        "phase_vs1_controlled_loop_ready": phase_vs1_closure_phase_result.get("controlled_loop_ready", False) if phase_vs1_closure_present else phase_vs1_readiness_aggregate.get("controlled_loop_ready", False),
        "phase_vs1_typed_blockers_exposed": phase_vs1_closure_phase_result.get("typed_blockers_exposed", False) if phase_vs1_closure_present else False,
        "phase_vs1_required_components_total": phase_vs1_closure_phase_result.get("required_components_total") if phase_vs1_closure_present else phase_vs1_precondition_inventory_counts.get("required_components_total"),
        "phase_vs1_ready_component_count": phase_vs1_closure_blocker_summary.get("ready_component_count") if phase_vs1_closure_present else phase_vs1_readiness_aggregate.get("ready_component_count"),
        "phase_vs1_missing_or_blocked_component_count": phase_vs1_closure_blocker_summary.get("missing_or_blocked_component_count") if phase_vs1_closure_present else phase_vs1_readiness_aggregate.get("missing_or_blocked_component_count"),
        "phase_vs1_next_surfaces_mapped": phase_vs1_closure_phase_result.get("next_surfaces_mapped", False) if phase_vs1_closure_present else False,
        "phase_vs1_source_blocker_count": phase_vs1_closure_next_surface.get("source_blocker_count") if phase_vs1_closure_present else (phase_vs1_next_surface_coverage.get("source_blocker_count") if phase_vs1_next_surface_map_present else None),
        "phase_vs1_mapped_blocker_count": phase_vs1_closure_next_surface.get("mapped_blocker_count") if phase_vs1_closure_present else (phase_vs1_next_surface_coverage.get("mapped_blocker_count") if phase_vs1_next_surface_map_present else None),
        "phase_vs1_unmapped_blocker_count": phase_vs1_closure_next_surface.get("unmapped_blocker_count") if phase_vs1_closure_present else (phase_vs1_next_surface_coverage.get("unmapped_blocker_count") if phase_vs1_next_surface_map_present else None),
        "phase_vs1_surface_candidate_record_count": phase_vs1_closure_next_surface.get("surface_candidate_count") if phase_vs1_closure_present else (len(phase_vs1_next_surface_map.get("surface_candidates", [])) if phase_vs1_next_surface_map_present else None),
        "phase_vs1_advisory_first_surface_from_vs1_5": phase_vs1_closure_next_surface.get("advisory_first_surface_from_vs1_5") if phase_vs1_closure_present else None,
        "phase_vs1_ranking_recomputed_by_vs1_6": phase_vs1_closure_next_surface.get("ranking_recomputed_by_vs1_6", False) if phase_vs1_closure_present else False,
        "phase_vs1_ranking_modified_by_vs1_6": phase_vs1_closure_next_surface.get("ranking_modified_by_vs1_6", False) if phase_vs1_closure_present else False,
        "phase_vs1_post_vs1_decision_surface": phase_vs1_closure_post_vs1.get("surface") if phase_vs1_closure_present else None,
        "phase_vs1_post_vs1_decision_surface_named": phase_vs1_closure_post_vs1.get("named_by_vs1_6", False) if phase_vs1_closure_present else False,
        "phase_vs1_post_vs1_decision_artifact_created": phase_vs1_closure_post_vs1.get("decision_artifact_created_by_vs1_6", False) if phase_vs1_closure_present else False,
        "phase_vs1_machine_may_select_next_phase": phase_vs1_closure_post_vs1.get("machine_may_select_next_phase", False) if phase_vs1_closure_present else False,
        "phase_vs1_loop_execution_authorized": phase_vs1_closure_readiness.get("loop_execution_authorized", False) if phase_vs1_closure_present else (phase_vs1_next_surface_policy.get("loop_execution_authorized", False) if phase_vs1_next_surface_map_present else False),
        "phase_vs1_runner_created": phase_vs1_closure_readiness.get("runner_created", False) if phase_vs1_closure_present else (phase_vs1_next_surface_policy.get("runner_created", False) if phase_vs1_next_surface_map_present else False),
        "phase_vs1_micro_sweeps_authorized": phase_vs1_closure_readiness.get("micro_sweeps_authorized", False) if phase_vs1_closure_present else (phase_vs1_next_surface_forbidden.get("micro_sweeps_authorized", False) if phase_vs1_next_surface_map_present else False),
        "phase_vs1_local_revision_authorized": phase_vs1_closure_readiness.get("local_revision_authorized", False) if phase_vs1_closure_present else (phase_vs1_next_surface_forbidden.get("local_revision_authorized", False) if phase_vs1_next_surface_map_present else False),
        "phase_vs1_mapped_surface_selected": phase_vs1_closure.get("forbidden_claim_checks", {}).get("mapped_surface_selected", False) if phase_vs1_closure_present else False,
        "phase_vs1_mapped_surface_built": phase_vs1_closure.get("forbidden_claim_checks", {}).get("mapped_surface_built", False) if phase_vs1_closure_present else False,
        "phase_vs1_human_authority_consumed": phase_vs1_closure_readiness.get("human_authority_consumed", False) if phase_vs1_closure_present else False,
        "phase_vs1_terminal_transition": phase_vs1_closure_terminal.get("transition") if phase_vs1_closure_present else None,
        "post_vs1_current_unit": post_vs1_direction_transition_closure.get("object_id") if post_vs1_direction_transition_closure_present else (post_vs1_direction_authority_update.get("object_id") if post_vs1_direction_authority_update_present else (post_vs1_direction_receipt.get("object_id") if post_vs1_direction_receipt_present else (post_vs1_direction_surface.get("object_id") if post_vs1_direction_surface_present else None))),
        "post_vs1_surface_artifact_id": post_vs1_direction_surface.get("artifact_id") if post_vs1_direction_surface_present else None,
        "post_vs1_surface_gate": post_vs1_direction_surface.get("surface_gate") if post_vs1_direction_surface_present else None,
        "post_vs1_applicable_closure_branch": post_vs1_direction_surface.get("applicable_closure_branch") if post_vs1_direction_surface_present else None,
        "post_vs1_direction_decision_receipt_artifact_id": post_vs1_direction_receipt.get("artifact_id") if post_vs1_direction_receipt_present else None,
        "post_vs1_direction_decision_receipt_gate": post_vs1_direction_receipt.get("receipt_gate") if post_vs1_direction_receipt_present else None,
        "post_vs1_source_surface_commit_sha": post_vs1_receipt_source_binding.get("source_surface_commit_sha") if post_vs1_direction_receipt_present else None,
        "post_vs1_accepted_decision_package_sha256": post_vs1_receipt_selection.get("accepted_decision_package_sha256") if post_vs1_direction_receipt_present else None,
        "post_vs1_accepted_option": post_vs1_receipt_selection.get("accepted_option") if post_vs1_direction_receipt_present else None,
        "post_vs1_decision_mode": post_vs1_receipt_selection.get("decision_mode") if post_vs1_direction_receipt_present else None,
        "post_vs1_approved_scope_eligible_for_authority_update": post_vs1_receipt_approved_scope.get("approved_scope_eligible_for_authority_update") if post_vs1_direction_receipt_present else False,
        "post_vs1_approved_scope_applied_to_authority_state": post_vs1_authority_update_state.get("approved_scope_applied_to_authority_state", False) if post_vs1_direction_authority_update_present else (post_vs1_receipt_approved_scope.get("approved_scope_applied_to_authority_state") if post_vs1_direction_receipt_present else False),
        "post_vs1_pre_repair_decision_receipt_sha256": "de8a3130cd7f61096464b12bb3346ec82e6c81530a46b7ba38b67d79f36fe85d" if post_vs1_direction_receipt_present else None,
        "post_vs1_decision_receipt_sha256": post_vs1_receipt_hash if post_vs1_direction_receipt_present else None,
        "post_vs1_decision_receipt_hash_recomputes": (post_vs1_receipt_hash == post_vs1_receipt_recomputed_hash) if post_vs1_direction_receipt_present else False,
        "post_vs1_decision_receipt_hash_changed_for_declared_serialization_repair": (post_vs1_receipt_hash != "de8a3130cd7f61096464b12bb3346ec82e6c81530a46b7ba38b67d79f36fe85d") if post_vs1_direction_receipt_present else False,
        "post_vs1_direction_authority_update_artifact_id": post_vs1_direction_authority_update.get("artifact_id") if post_vs1_direction_authority_update_present else None,
        "post_vs1_direction_authority_update_gate": post_vs1_direction_authority_update.get("authority_update_gate") if post_vs1_direction_authority_update_present else None,
        "post_vs1_transition_closure_artifact_id": post_vs1_direction_transition_closure.get("artifact_id") if post_vs1_direction_transition_closure_present else None,
        "post_vs1_source_authority_update_commit_sha": post_vs1_transition_closure_source_authority.get("source_authority_update_commit_sha") if post_vs1_direction_transition_closure_present else None,
        "post_vs1_source_authority_update_sha256": post_vs1_transition_closure_source_authority.get("source_authority_update_canonical_sha256") if post_vs1_direction_transition_closure_present else None,
        "post_vs1_transition_closure_sha256": post_vs1_transition_closure_binding.get("transition_closure_sha256") if post_vs1_direction_transition_closure_present else None,
        "post_vs1_transition_closure_status": post_vs1_direction_transition_closure.get("transition_closure_status") if post_vs1_direction_transition_closure_present else None,
        "post_vs1_transition_closure_gate": post_vs1_direction_transition_closure.get("transition_closure_gate") if post_vs1_direction_transition_closure_present else None,
        "post_vs1_source_decision_receipt_commit_sha": post_vs1_authority_update_source_receipt.get("source_decision_receipt_commit_sha") if post_vs1_direction_authority_update_present else None,
        "post_vs1_source_decision_receipt_sha256": post_vs1_authority_update_source_receipt.get("source_decision_receipt_canonical_sha256") if post_vs1_direction_authority_update_present else None,
        "post_vs1_source_decision_package_sha256": post_vs1_authority_update_source_package.get("source_decision_package_sha256") if post_vs1_direction_authority_update_present else None,
        "post_vs1_decision_receipt_consumed_for_authority_update": post_vs1_authority_update_consumption.get("decision_receipt_consumed_for_authority_update", False) if post_vs1_direction_authority_update_present else False,
        "post_vs1_decision_receipt_consumption_count": post_vs1_authority_update_consumption.get("decision_receipt_consumption_count", 0) if post_vs1_direction_authority_update_present else 0,
        "post_vs1_authority_update_consumed_for_transition_closure": post_vs1_transition_closure_consumption.get("authority_update_consumed_for_transition_closure", False) if post_vs1_direction_transition_closure_present else False,
        "post_vs1_authority_update_consumption_count": post_vs1_transition_closure_consumption.get("authority_update_consumption_count", 0) if post_vs1_direction_transition_closure_present else 0,
        "post_vs1_proposal_source_artifact_id": post_vs1_proposal_source.get("artifact_id") if post_vs1_proposal_source_present else None,
        "post_vs1_proposal_source_role": post_vs1_proposal_source.get("source_role") if post_vs1_proposal_source_present else None,
        "post_vs1_proposal_source_durability_status": post_vs1_proposal_source.get("source_durability_status") if post_vs1_proposal_source_present else None,
        "post_vs1_proposal_source_hash_present": bool(post_vs1_proposal_source.get("content_sha256")) if post_vs1_proposal_source_present else False,
        "post_vs1_bundle_id": post_vs1_proposal_bundle.get("bundle_id") if post_vs1_direction_surface_present else None,
        "post_vs1_bundle_primary_member_count": post_vs1_proposal_bundle.get("primary_bundle_member_count") if post_vs1_direction_surface_present else None,
        "post_vs1_bundle_entry_prerequisite": post_vs1_proposal_bundle.get("bundle_entry_prerequisite_surface_id") if post_vs1_direction_surface_present else None,
        "post_vs1_s14_deferred": post_vs1_membership.get("s14_deferred", False) if post_vs1_direction_surface_present else False,
        "post_vs1_s15_deferred": post_vs1_membership.get("s15_deferred", False) if post_vs1_direction_surface_present else False,
        "post_vs1_s21_downstream_only": post_vs1_membership.get("s21_downstream_only", False) if post_vs1_direction_surface_present else False,
        "post_vs1_second_target_excluded": not post_vs1_direction_surface.get("proposal_overbreadth_normalization", {}).get("second_target_scope_included", True) if post_vs1_direction_surface_present else False,
        "post_vs1_portability_scope_excluded": not post_vs1_direction_surface.get("proposal_overbreadth_normalization", {}).get("portability_scope_included", True) if post_vs1_direction_surface_present else False,
        "post_vs1_unmapped_scope_count": post_vs1_traceability.get("unmapped_additional_proposal_scope_count") if post_vs1_direction_surface_present else None,
        "post_vs1_decision_package_hash_present": bool(post_vs1_decision_package.get("decision_package_sha256")) if post_vs1_direction_surface_present else False,
        "post_vs1_decision_options_count": len(post_vs1_direction_surface.get("decision_options", [])) if post_vs1_direction_surface_present else None,
        "post_vs1_default_option": post_vs1_defaults.get("default_option") if post_vs1_direction_surface_present else None,
        "post_vs1_preselected_option": post_vs1_defaults.get("preselected_option") if post_vs1_direction_surface_present else None,
        "post_vs1_human_decision_required": post_vs1_receipt_state.get("human_decision_required", False) if post_vs1_direction_receipt_present else (post_vs1_decision_state.get("human_decision_required", False) if post_vs1_direction_surface_present else False),
        "post_vs1_human_decision_recorded": post_vs1_receipt_state.get("human_decision_recorded", False) if post_vs1_direction_receipt_present else (post_vs1_decision_state.get("human_decision_recorded", False) if post_vs1_direction_surface_present else False),
        "post_vs1_decision_receipt_created": post_vs1_receipt_state.get("decision_receipt_created", False) if post_vs1_direction_receipt_present else (post_vs1_decision_state.get("decision_receipt_created", False) if post_vs1_direction_surface_present else False),
        "post_vs1_direction_selected": post_vs1_receipt_state.get("direction_selected", False) if post_vs1_direction_receipt_present else (post_vs1_decision_state.get("direction_selected", False) if post_vs1_direction_surface_present else False),
        "post_vs1_target_family_selected": post_vs1_receipt_state.get("target_family_selected", False) if post_vs1_direction_receipt_present else (post_vs1_decision_state.get("target_family_selected", False) if post_vs1_direction_surface_present else False),
        "post_vs1_first_target_selected": post_vs1_receipt_state.get("first_target_selected", False) if post_vs1_direction_receipt_present else (post_vs1_decision_state.get("first_target_selected", False) if post_vs1_direction_surface_present else False),
        "post_vs1_selected_direction": post_vs1_receipt_selection.get("direction_id") if post_vs1_direction_receipt_present else None,
        "post_vs1_selected_target_family": post_vs1_receipt_selection.get("target_family") if post_vs1_direction_receipt_present else None,
        "post_vs1_selected_first_target": post_vs1_receipt_selection.get("first_target") if post_vs1_direction_receipt_present else None,
        "post_vs1_definition_scope_approved": post_vs1_receipt_state.get("definition_scope_approved", False) if post_vs1_direction_receipt_present else (post_vs1_decision_state.get("definition_scope_approved", False) if post_vs1_direction_surface_present else False),
        "post_vs1_construction_scope_approved": post_vs1_receipt_state.get("construction_scope_approved", False) if post_vs1_direction_receipt_present else (post_vs1_decision_state.get("construction_scope_approved", False) if post_vs1_direction_surface_present else False),
        "post_vs1_bounded_construction_scope_approved": post_vs1_receipt_state.get("bounded_construction_scope_approved", False) if post_vs1_direction_receipt_present else False,
        "post_vs1_construction_verification_scope_approved": post_vs1_receipt_state.get("construction_verification_scope_approved", False) if post_vs1_direction_receipt_present else (post_vs1_decision_state.get("construction_verification_scope_approved", False) if post_vs1_direction_surface_present else False),
        "post_vs1_accepted_with_revisions": post_vs1_receipt_selection.get("accepted_with_revisions", False) if post_vs1_direction_receipt_present else False,
        "post_vs1_revision_count": post_vs1_receipt_selection.get("revision_count", 0) if post_vs1_direction_receipt_present else 0,
        "post_vs1_second_target_scope_approved": post_vs1_receipt_state.get("second_target_selected", False) if post_vs1_direction_receipt_present else False,
        "post_vs1_portability_scope_approved": post_vs1_receipt_state.get("portability_scope_selected", False) if post_vs1_direction_receipt_present else False,
        "post_vs1_authority_state_mutated": post_vs1_effective_authority_state.get("authority_state_mutated", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else False,
        "post_vs1_authority_update_applied": post_vs1_effective_authority_state.get("authority_update_applied", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else (post_vs1_receipt_state.get("authority_update_applied", False) if post_vs1_direction_receipt_present else (post_vs1_decision_state.get("authority_update_applied", False) if post_vs1_direction_surface_present else False)),
        "post_vs1_authority_transition_closed": post_vs1_effective_authority_state.get("authority_transition_closed", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else (post_vs1_receipt_state.get("authority_transition_closed", False) if post_vs1_direction_receipt_present else (post_vs1_decision_state.get("authority_transition_closed", False) if post_vs1_direction_surface_present else False)),
        "post_vs1_vs2_authority_granted": post_vs1_effective_authority_state.get("vs2_definition_authority_granted", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else (post_vs1_receipt_state.get("vs2_authority_granted", False) if post_vs1_direction_receipt_present else False),
        "post_vs1_vs2_definition_authority_granted": post_vs1_effective_authority_state.get("vs2_definition_authority_granted", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else False,
        "post_vs1_vs2_profile_and_target_freeze_authority_granted": post_vs1_effective_authority_state.get("vs2_profile_and_target_freeze_authority_granted", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else False,
        "post_vs1_vs2_bounded_construction_authority_granted": post_vs1_effective_authority_state.get("vs2_bounded_construction_authority_granted", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else False,
        "post_vs1_fixture_construction_authority_granted": post_vs1_effective_authority_state.get("fixture_construction_authority_granted", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else False,
        "post_vs1_readiness_gate_construction_authority_granted": post_vs1_effective_authority_state.get("readiness_gate_construction_authority_granted", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else False,
        "post_vs1_construction_package_verification_authority_granted": post_vs1_effective_authority_state.get("construction_package_verification_authority_granted", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else False,
        "post_vs1_authority_effective_for_vs2_consumption": post_vs1_effective_authority_state.get("authority_effective_for_vs2_consumption", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else False,
        "post_vs1_authority_grants_effective_for_consumption": post_vs1_effective_authority_state.get("authority_grants_effective_for_consumption", False) if post_vs1_direction_transition_closure_present else False,
        "post_vs1_vs2_source_intake_lawful": post_vs1_effective_authority_state.get("vs2_source_intake_lawful", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else False,
        "post_vs1_vs2_source_intake_built": post_vs1_effective_authority_state.get("vs2_source_intake_built", False) if post_vs1_direction_transition_closure_present else False,
        "post_vs1_vs2_1_may_begin": post_vs1_effective_authority_state.get("vs2_1_may_begin", False) if post_vs1_direction_transition_closure_present else False,
        "post_vs1_any_vs2_grant_consumed": post_vs1_effective_authority_state.get("any_vs2_grant_consumed", False) if post_vs1_direction_transition_closure_present else False,
        "post_vs1_vs2_grant_consumption_count": post_vs1_transition_closure_consumption.get("vs2_grant_consumption_count", 0) if post_vs1_direction_transition_closure_present else 0,
        "post_vs1_broad_vs2_authority_granted": post_vs1_effective_authority_state.get("broad_vs2_authority_granted", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else False,
        "post_vs1_vs2_started": post_vs1_effective_authority_state.get("vs2_started", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else (post_vs1_receipt_state.get("vs2_started", False) if post_vs1_direction_receipt_present else (post_vs1_decision_state.get("vs2_started", False) if post_vs1_direction_surface_present else False)),
        "post_vs1_vs2_1_built": post_vs1_effective_authority_state.get("vs2_1_built", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else (post_vs1_receipt_state.get("vs2_1_built", False) if post_vs1_direction_receipt_present else (post_vs1_terminal.get("builds_vs2_1", False) if post_vs1_direction_surface_present else False)),
        "post_vs1_construction_performed": post_vs1_effective_authority_state.get("construction_performed", False) if post_vs1_direction_transition_closure_present else False,
        "post_vs1_execution_authorized": post_vs1_effective_authority_state.get("execution_authorized", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else (post_vs1_receipt_state.get("execution_authorized", False) if post_vs1_direction_receipt_present else (post_vs1_decision_state.get("execution_authorized", False) if post_vs1_direction_surface_present else False)),
        "post_vs1_positive_path_execution_authorized": post_vs1_effective_authority_state.get("positive_path_execution_authorized", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else False,
        "post_vs1_negative_path_execution_authorized": post_vs1_effective_authority_state.get("negative_path_execution_authorized", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else False,
        "post_vs1_sweep_authorized": post_vs1_effective_authority_state.get("sweep_authorized", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else (post_vs1_receipt_state.get("sweep_authorized", False) if post_vs1_direction_receipt_present else (post_vs1_decision_state.get("sweep_authorized", False) if post_vs1_direction_surface_present else False)),
        "post_vs1_automatic_rerun_authorized": post_vs1_effective_authority_state.get("automatic_rerun_authorized", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else (post_vs1_receipt_state.get("automatic_rerun_authorized", False) if post_vs1_direction_receipt_present else (post_vs1_decision_state.get("automatic_rerun_authorized", False) if post_vs1_direction_surface_present else False)),
        "post_vs1_automatic_radius_renewal_authorized": post_vs1_effective_authority_state.get("automatic_radius_renewal_authorized", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else False,
        "post_vs1_runner_authority_created": post_vs1_effective_authority_state.get("runner_authority_created", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else (post_vs1_receipt_state.get("runner_authority_created", False) if post_vs1_direction_receipt_present else (post_vs1_decision_state.get("runner_authority_created", False) if post_vs1_direction_surface_present else False)),
        "post_vs1_reusable_schema_authority_granted": post_vs1_effective_authority_state.get("reusable_schema_authority_granted", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else False,
        "post_vs1_reusable_move_authority_granted": post_vs1_effective_authority_state.get("reusable_move_authority_granted", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else False,
        "post_vs1_second_target_authority_granted": post_vs1_effective_authority_state.get("second_target_authority_granted", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else False,
        "post_vs1_portability_authority_granted": post_vs1_effective_authority_state.get("portability_authority_granted", False) if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else False,
        "post_vs1_next_unit": "VS2_1_POST_VS1_SOURCE_INTAKE_PENDING" if post_vs1_direction_transition_closure_present else ("POST_VS1_DIRECTION_TRANSITION_CLOSURE_V0_PENDING" if post_vs1_direction_authority_update_present else ("POST_VS1_DIRECTION_AUTHORITY_UPDATE_V0_PENDING" if post_vs1_direction_receipt_present else None)),
        "post_vs1_terminal_transition": post_vs1_effective_terminal.get("transition") if (post_vs1_direction_transition_closure_present or post_vs1_direction_authority_update_present) else (post_vs1_receipt_terminal.get("transition") if post_vs1_direction_receipt_present else (post_vs1_terminal.get("transition") if post_vs1_direction_surface_present else None)),
        "phase_vs2_current_unit": phase_vs2_3_receipt.get("unit_id") if phase_vs2_3_receipt_present else (phase_vs2_2_profile.get("unit_id") if phase_vs2_2_profile_present else (phase_vs2_1_source_intake.get("unit_id") if phase_vs2_1_source_intake_present else None)),
        "phase_vs2_source_intake_artifact_id": phase_vs2_1_source_intake.get("artifact_id") if phase_vs2_1_source_intake_present else None,
        "phase_vs2_source_intake_receipt_artifact_id": phase_vs2_1_source_intake_receipt.get("artifact_id") if phase_vs2_1_source_intake_receipt_present else None,
        "phase_vs2_source_intake_sha256": phase_vs2_1_intake_binding.get("source_intake_sha256") if phase_vs2_1_source_intake_present else None,
        "phase_vs2_source_manifest_sha256": phase_vs2_1_source_manifest.get("source_manifest_sha256") if phase_vs2_1_source_intake_present else None,
        "phase_vs2_source_manifest_entry_count": phase_vs2_1_source_manifest.get("source_manifest_entry_count") if phase_vs2_1_source_intake_present else None,
        "phase_vs2_source_intake_committed": phase_vs2_2_profile.get("source_intake_commit_reconciliation", {}).get("source_intake_committed", False) if phase_vs2_2_profile_present else False,
        "phase_vs2_source_manifest_committed": phase_vs2_2_profile.get("source_intake_commit_reconciliation", {}).get("source_manifest_committed", False) if phase_vs2_2_profile_present else False,
        "phase_vs2_source_manifest_frozen": phase_vs2_1_post_state.get("source_manifest_frozen", False) if phase_vs2_1_source_intake_present else False,
        "phase_vs2_source_manifest_commit_pending": phase_vs2_1_post_state.get("source_manifest_commit_pending", False) if phase_vs2_1_source_intake_present else False,
        "phase_vs2_bookkeeping_commit_required": phase_vs2_3_receipt_present or (phase_vs2_2_post_state.get("bookkeeping_commit_required", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("bookkeeping_commit_required", False) if phase_vs2_1_source_intake_present else False)),
        "phase_vs2_source_intake_built": phase_vs2_1_post_state.get("vs2_source_intake_built", False) if phase_vs2_1_source_intake_present else False,
        "phase_vs2_started": phase_vs2_2_post_state.get("vs2_started", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("vs2_started", False) if phase_vs2_1_source_intake_present else False),
        "phase_vs2_1_built": phase_vs2_1_post_state.get("vs2_1_built", False) if phase_vs2_1_source_intake_present else False,
        "phase_vs2_2_built": phase_vs2_2_post_state.get("vs2_2_built", False) if phase_vs2_2_profile_present else False,
        "phase_vs2_2_may_begin": phase_vs2_1_post_state.get("vs2_2_may_begin", False) if phase_vs2_1_source_intake_present else False,
        "phase_vs2_3_may_begin": phase_vs2_2_post_state.get("vs2_3_may_begin", False) if phase_vs2_2_profile_present else False,
        "phase_vs2_effective_grant_count": phase_vs2_1_effective_grants.get("effective_grant_count") if phase_vs2_1_source_intake_present else None,
        "phase_vs2_five_grants_effective": phase_vs2_1_effective_grants.get("effective_grant_count") == 5 if phase_vs2_1_source_intake_present else False,
        "phase_vs2_any_vs2_grant_consumed": phase_vs2_3_authority.get("total_consumed_grant_count", 0) > 0 if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("any_vs2_grant_consumed", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("any_vs2_grant_consumed", False) if phase_vs2_1_source_intake_present else False)),
        "phase_vs2_grant_consumption_count": phase_vs2_3_authority.get("total_consumed_grant_count", 0) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("vs2_grant_consumption_count", 0) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("vs2_grant_consumption_count", 0) if phase_vs2_1_source_intake_present else 0)),
        "phase_vs2_profile_and_target_freeze_grant_consumed": phase_vs2_2_post_state.get("profile_and_target_freeze_grant_consumed", False) if phase_vs2_2_profile_present else False,
        "phase_vs2_profile_and_target_freeze_grant_consumption_count": phase_vs2_2_post_state.get("profile_and_target_freeze_grant_consumption_count", 0) if phase_vs2_2_profile_present else 0,
        "phase_vs2_remaining_effective_grant_count": phase_vs2_3_authority.get("unconsumed_effective_grant_count") if phase_vs2_3_receipt_present else (phase_vs2_2_remaining_grants.get("remaining_effective_grant_count") if phase_vs2_2_profile_present else None),
        "phase_vs2_remaining_grants_consumed_by_vs2_2": phase_vs2_2_remaining_grants.get("remaining_grants_consumed_by_vs2_2") if phase_vs2_2_profile_present else None,
        "phase_vs2_profile_grant_routed_to_vs2_2": phase_vs2_1_grant_routing.get("profile_grant_routed_to_vs2_2", False) if phase_vs2_1_source_intake_present else False,
        "phase_vs2_remaining_grant_consumers_frozen": phase_vs2_2_remaining_grants.get("remaining_grant_routes_frozen", False) if phase_vs2_2_profile_present else (phase_vs2_1_grant_routing.get("remaining_grant_consumers_frozen", False) if phase_vs2_1_source_intake_present else False),
        "phase_vs2_next_unit": "VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PENDING" if phase_vs2_3_receipt_present else ("VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PENDING" if phase_vs2_2_profile_present else ("VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_PENDING" if phase_vs2_1_source_intake_present else None)),
        "phase_vs2_profile_artifact_id": phase_vs2_2_profile.get("artifact_id") if phase_vs2_2_profile_present else None,
        "phase_vs2_profile_id": phase_vs2_2_profile_identity.get("profile_id") if phase_vs2_2_profile_present else None,
        "phase_vs2_profile_sha256": phase_vs2_2_profile_binding.get("profile_sha256") if phase_vs2_2_profile_present else None,
        "phase_vs2_profile_gate": phase_vs2_2_profile.get("profile_gate") if phase_vs2_2_profile_present else None,
        "phase_vs2_target_freeze_artifact_id": phase_vs2_2_target.get("artifact_id") if phase_vs2_2_target_present else None,
        "phase_vs2_target_freeze_sha256": phase_vs2_2_target_binding.get("target_freeze_sha256") if phase_vs2_2_target_present else None,
        "phase_vs2_target_freeze_gate": phase_vs2_2_target.get("target_freeze_gate") if phase_vs2_2_target_present else None,
        "phase_vs2_target_family": phase_vs2_2_target_identity.get("target_family") if phase_vs2_2_target_present else None,
        "phase_vs2_target_id": phase_vs2_2_target_identity.get("target_id") if phase_vs2_2_target_present else None,
        "phase_vs2_profile_and_target_freeze_receipt_artifact_id": phase_vs2_2_receipt.get("artifact_id") if phase_vs2_2_receipt_present else None,
        "phase_vs2_profile_and_target_freeze_receipt_sha256": phase_vs2_2_receipt.get("receipt_binding", {}).get("receipt_sha256") if phase_vs2_2_receipt_present else None,
        "phase_vs2_profile_and_target_freeze_receipt_gate": phase_vs2_2_receipt.get("receipt_gate") if phase_vs2_2_receipt_present else None,
        "phase_vs2_component_count": phase_vs2_2_component_summary.get("component_count") if phase_vs2_2_profile_present else None,
        "phase_vs2_required_full_count": phase_vs2_2_component_summary.get("required_full_count") if phase_vs2_2_profile_present else None,
        "phase_vs2_required_minimal_count": phase_vs2_2_component_summary.get("required_minimal_count") if phase_vs2_2_profile_present else None,
        "phase_vs2_deferred_count": phase_vs2_2_component_summary.get("deferred_count") if phase_vs2_2_profile_present else None,
        "phase_vs2_kernel_profile_frozen": phase_vs2_2_post_state.get("kernel_profile_frozen", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("kernel_profile_frozen", False) if phase_vs2_1_source_intake_present else False),
        "phase_vs2_semantic_target_frozen": phase_vs2_2_post_state.get("semantic_target_frozen", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("semantic_target_frozen", False) if phase_vs2_1_source_intake_present else False),
        "phase_vs2_maximum_construction_envelope_frozen": phase_vs2_2_construction_envelope.get("maximum_construction_envelope_frozen", False) if phase_vs2_2_profile_present else False,
        "phase_vs2_maximum_future_execution_envelope_frozen": phase_vs2_2_execution_envelope.get("maximum_future_execution_envelope_frozen", False) if phase_vs2_2_profile_present else False,
        "phase_vs2_downstream_sequence_frozen": phase_vs2_2_downstream_sequence.get("downstream_sequence_frozen", False) if phase_vs2_2_profile_present else False,
        "phase_vs2_downstream_construction_object_count": phase_vs2_2_downstream_objects.get("downstream_construction_object_count") if phase_vs2_2_profile_present else None,
        "phase_vs2_construction_started": phase_vs2_3_post_state.get("construction_performed", False) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("construction_performed", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("construction_performed", False) if phase_vs2_1_source_intake_present else False)),
        "phase_vs2_construction_performed": phase_vs2_3_post_state.get("construction_performed", False) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("construction_performed", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("construction_performed", False) if phase_vs2_1_source_intake_present else False)),
        "phase_vs2_fixture_construction_performed": phase_vs2_3_post_state.get("fixture_instance_created", False) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("fixture_construction_performed", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("fixture_construction_performed", False) if phase_vs2_1_source_intake_present else False)),
        "phase_vs2_readiness_gate_constructed": phase_vs2_3_post_state.get("readiness_gate_constructed", False) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("readiness_gate_constructed", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("readiness_gate_constructed", False) if phase_vs2_1_source_intake_present else False)),
        "phase_vs2_construction_package_verified": phase_vs2_3_post_state.get("construction_package_verified", False) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("construction_package_verified", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("construction_package_verified", False) if phase_vs2_1_source_intake_present else False)),
        "phase_vs2_execution_authorized": phase_vs2_3_post_state.get("execution_authorized", False) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("execution_authorized", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("execution_authorized", False) if phase_vs2_1_source_intake_present else False)),
        "phase_vs2_execution_performed": phase_vs2_3_post_state.get("execution_performed", False) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("execution_performed", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("execution_performed", False) if phase_vs2_1_source_intake_present else False)),
        "phase_vs2_sweep_authorized": phase_vs2_3_post_state.get("sweep_authorized", False) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("sweep_authorized", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("sweep_authorized", False) if phase_vs2_1_source_intake_present else False)),
        "phase_vs2_runner_created": phase_vs2_3_post_state.get("runner_created", False) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("runner_created", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("runner_created", False) if phase_vs2_1_source_intake_present else False)),
        "phase_vs2_terminal_transition": phase_vs2_3_receipt.get("terminal_transition") if phase_vs2_3_receipt_present else (phase_vs2_2_profile.get("construction_session_terminal") if phase_vs2_2_profile_present else (phase_vs2_1_source_intake.get("terminal_transition") if phase_vs2_1_source_intake_present else None)),
        "phase_vs2_3_built": phase_vs2_3_post_state.get("vs2_3_built", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_3_receipt_artifact_id": phase_vs2_3_receipt.get("artifact_id") if phase_vs2_3_receipt_present else None,
        "phase_vs2_3_receipt_sha256": phase_vs2_3_receipt_binding.get("receipt_sha256") if phase_vs2_3_receipt_present else None,
        "phase_vs2_3_receipt_gate": phase_vs2_3_gates.get("receipt_gate") if phase_vs2_3_receipt_present else None,
        "phase_vs2_3_construction_verdict": phase_vs2_3_receipt.get("construction_verdict") if phase_vs2_3_receipt_present else None,
        "phase_vs2_scope_regime_frame_constructed": phase_vs2_3_post_state.get("scope_regime_frame_constructed", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_scope_regime_contract_constructed": phase_vs2_3_post_state.get("scope_regime_frame_constructed", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_runtime_state_contract_constructed": phase_vs2_3_post_state.get("runtime_state_contract_constructed", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_runtime_control_state_contract_constructed": phase_vs2_3_post_state.get("runtime_state_contract_constructed", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_candidate_schema_constructed": phase_vs2_3_post_state.get("candidate_schema_constructed", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_frozen_target_contract_constructed": phase_vs2_3_post_state.get("frozen_target_contract_constructed", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_object_model_manifest_constructed": phase_vs2_3_post_state.get("object_model_manifest_constructed", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_object_model_constructed": phase_vs2_3_post_state.get("object_model_constructed", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_kernel_constructed": phase_vs2_3_post_state.get("kernel_constructed", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_runtime_instance_created": phase_vs2_3_post_state.get("runtime_instance_created", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_candidate_instance_created": phase_vs2_3_post_state.get("candidate_instance_created", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_fixture_instance_created": phase_vs2_3_post_state.get("fixture_instance_created", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_move_space_constructed": phase_vs2_3_post_state.get("move_space_constructed", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_selector_constructed": phase_vs2_3_post_state.get("selector_constructed", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_applicator_constructed": phase_vs2_3_post_state.get("applicator_constructed", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_validation_execution_logic_constructed": phase_vs2_3_post_state.get("validation_execution_logic_constructed", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_admissibility_execution_logic_constructed": phase_vs2_3_post_state.get("admissibility_execution_logic_constructed", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_convergence_criterion_constructed": phase_vs2_3_post_state.get("convergence_criterion_constructed", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_source_snapshot_frozen": phase_vs2_3_post_state.get("source_snapshot_frozen", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_sweep_executed": phase_vs2_3_post_state.get("sweep_executed", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_4_may_begin": phase_vs2_3_post_state.get("vs2_4_may_begin", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_bounded_construction_grant_consumed": phase_vs2_3_authority.get("bounded_construction_grant_consumed", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_bounded_construction_grant_exhausted": phase_vs2_3_authority.get("bounded_construction_grant_exhausted", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_same_bounded_construction_grant_may_be_consumed_again": phase_vs2_3_authority.get("same_bounded_construction_grant_may_be_consumed_again", False) if phase_vs2_3_receipt_present else False,
        "phase_vs2_unconsumed_effective_grant_count": phase_vs2_3_authority.get("unconsumed_effective_grant_count") if phase_vs2_3_receipt_present else None,
        "phase_vs2_scope_regime_contract_sha256": phase_vs2_3_bindings.get("F0", {}).get("canonical_sha256") if phase_vs2_3_receipt_present else None,
        "phase_vs2_runtime_state_contract_sha256": phase_vs2_3_bindings.get("O1", {}).get("canonical_sha256") if phase_vs2_3_receipt_present else None,
        "phase_vs2_runtime_control_state_contract_sha256": phase_vs2_3_bindings.get("O1", {}).get("canonical_sha256") if phase_vs2_3_receipt_present else None,
        "phase_vs2_candidate_schema_sha256": phase_vs2_3_bindings.get("O2", {}).get("canonical_sha256") if phase_vs2_3_receipt_present else None,
        "phase_vs2_frozen_target_contract_sha256": phase_vs2_3_bindings.get("O3", {}).get("canonical_sha256") if phase_vs2_3_receipt_present else None,
        "phase_vs2_object_model_manifest_sha256": phase_vs2_3_bindings.get("M0", {}).get("canonical_sha256") if phase_vs2_3_receipt_present else None,
        "phase_vs2_execution_domain_object_role_count": phase_vs2_3_counts.get("execution_domain_object_role_count") if phase_vs2_3_receipt_present else None,
        "phase_vs2_static_scope_regime_frame_count": phase_vs2_3_counts.get("static_scope_regime_frame_count") if phase_vs2_3_receipt_present else None,
        "phase_vs2_static_object_model_manifest_count": phase_vs2_3_counts.get("static_object_model_manifest_count") if phase_vs2_3_receipt_present else None,
        "phase_vs2_additional_mutable_execution_domain_object_count": phase_vs2_3_counts.get("additional_mutable_execution_domain_object_count") if phase_vs2_3_receipt_present else None,
        "phase_vs2_downstream_binding_count_after_vs2_3": phase_vs2_3_counts.get("downstream_binding_count") if phase_vs2_3_receipt_present else None,
        "phase_vs2_pending_binding_count_after_vs2_3": phase_vs2_3_counts.get("pending_binding_count") if phase_vs2_3_receipt_present else None,
        "phase_vs2_absent_by_policy_binding_count_after_vs2_3": phase_vs2_3_counts.get("absent_by_policy_binding_count") if phase_vs2_3_receipt_present else None,
        "phase_vs2_fabricated_future_reference_count": phase_vs2_3_counts.get("fabricated_future_reference_count") if phase_vs2_3_receipt_present else None,
        "phase_vs2_current_unit": phase_vs2_4_receipt.get("unit_id") if phase_vs2_4_receipt_present else (phase_vs2_3_receipt.get("unit_id") if phase_vs2_3_receipt_present else (phase_vs2_2_profile.get("unit_id") if phase_vs2_2_profile_present else (phase_vs2_1_source_intake.get("unit_id") if phase_vs2_1_source_intake_present else None))),
        "phase_vs2_next_unit": "VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_PENDING" if phase_vs2_4_receipt_present else ("VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PENDING" if phase_vs2_3_receipt_present else ("VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PENDING" if phase_vs2_2_profile_present else ("VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_PENDING" if phase_vs2_1_source_intake_present else None))),
        "phase_vs2_grant_consumption_count": phase_vs2_4_authority.get("bounded_construction_consumption_count_after", phase_vs2_3_authority.get("total_consumed_grant_count", 0)) if phase_vs2_4_receipt_present else (phase_vs2_3_authority.get("total_consumed_grant_count", 0) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("vs2_grant_consumption_count", 0) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("vs2_grant_consumption_count", 0) if phase_vs2_1_source_intake_present else 0))),
        "phase_vs2_remaining_effective_grant_count": phase_vs2_4_authority.get("unconsumed_effective_grant_count") if phase_vs2_4_receipt_present else (phase_vs2_3_authority.get("unconsumed_effective_grant_count") if phase_vs2_3_receipt_present else (phase_vs2_2_remaining_grants.get("remaining_effective_grant_count") if phase_vs2_2_profile_present else None)),
        "phase_vs2_construction_started": phase_vs2_4_receipt_present or (phase_vs2_3_post_state.get("construction_performed", False) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("construction_performed", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("construction_performed", False) if phase_vs2_1_source_intake_present else False))),
        "phase_vs2_construction_performed": phase_vs2_4_receipt_present or (phase_vs2_3_post_state.get("construction_performed", False) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("construction_performed", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("construction_performed", False) if phase_vs2_1_source_intake_present else False))),
        "phase_vs2_execution_authorized": phase_vs2_4_post_state.get("execution_authorized", False) if phase_vs2_4_receipt_present else (phase_vs2_3_post_state.get("execution_authorized", False) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("execution_authorized", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("execution_authorized", False) if phase_vs2_1_source_intake_present else False))),
        "phase_vs2_execution_performed": phase_vs2_4_post_state.get("execution_performed", False) if phase_vs2_4_receipt_present else (phase_vs2_3_post_state.get("execution_performed", False) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("execution_performed", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("execution_performed", False) if phase_vs2_1_source_intake_present else False))),
        "phase_vs2_sweep_authorized": phase_vs2_4_post_state.get("sweep_authorized", False) if phase_vs2_4_receipt_present else (phase_vs2_3_post_state.get("sweep_authorized", False) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("sweep_authorized", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("sweep_authorized", False) if phase_vs2_1_source_intake_present else False))),
        "phase_vs2_sweep_executed": phase_vs2_4_post_state.get("sweep_executed", False) if phase_vs2_4_receipt_present else (phase_vs2_3_post_state.get("sweep_executed", False) if phase_vs2_3_receipt_present else False),
        "phase_vs2_runner_created": phase_vs2_4_post_state.get("runner_created", False) if phase_vs2_4_receipt_present else (phase_vs2_3_post_state.get("runner_created", False) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("runner_created", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("runner_created", False) if phase_vs2_1_source_intake_present else False))),
        "phase_vs2_runtime_instance_created": phase_vs2_4_post_state.get("runtime_instance_created", False) if phase_vs2_4_receipt_present else (phase_vs2_3_post_state.get("runtime_instance_created", False) if phase_vs2_3_receipt_present else False),
        "phase_vs2_candidate_instance_created": phase_vs2_4_post_state.get("candidate_instance_created", False) if phase_vs2_4_receipt_present else (phase_vs2_3_post_state.get("candidate_instance_created", False) if phase_vs2_3_receipt_present else False),
        "phase_vs2_fixture_instance_created": phase_vs2_4_post_state.get("fixture_instance_created", False) if phase_vs2_4_receipt_present else (phase_vs2_3_post_state.get("fixture_instance_created", False) if phase_vs2_3_receipt_present else False),
        "phase_vs2_fixture_construction_performed": phase_vs2_4_post_state.get("fixture_instance_created", False) if phase_vs2_4_receipt_present else (phase_vs2_3_post_state.get("fixture_instance_created", False) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("fixture_construction_performed", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("fixture_construction_performed", False) if phase_vs2_1_source_intake_present else False))),
        "phase_vs2_readiness_gate_constructed": False if phase_vs2_4_receipt_present else (phase_vs2_3_post_state.get("readiness_gate_constructed", False) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("readiness_gate_constructed", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("readiness_gate_constructed", False) if phase_vs2_1_source_intake_present else False))),
        "phase_vs2_construction_package_verified": False if phase_vs2_4_receipt_present else (phase_vs2_3_post_state.get("construction_package_verified", False) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("construction_package_verified", False) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("construction_package_verified", False) if phase_vs2_1_source_intake_present else False))),
        "phase_vs2_move_space_constructed": phase_vs2_4_receipt_present or (phase_vs2_3_post_state.get("move_space_constructed", False) if phase_vs2_3_receipt_present else False),
        "phase_vs2_move_space_frozen": phase_vs2_4_post_state.get("move_space_frozen", False) if phase_vs2_4_receipt_present else False,
        "phase_vs2_move_space_active": phase_vs2_4_post_state.get("move_space_active", False) if phase_vs2_4_receipt_present else False,
        "phase_vs2_source_and_version_binding_contract_constructed": phase_vs2_4_post_state.get("source_and_version_binding_contract_constructed", False) if phase_vs2_4_receipt_present else False,
        "phase_vs2_exact_source_snapshot_frozen": phase_vs2_4_post_state.get("exact_source_snapshot_frozen", False) if phase_vs2_4_receipt_present else False,
        "phase_vs2_move_authority_matrix_constructed": phase_vs2_4_post_state.get("move_authority_matrix_constructed", False) if phase_vs2_4_receipt_present else False,
        "phase_vs2_prospective_authority_envelope_constructed": phase_vs2_4_post_state.get("prospective_authority_envelope_constructed", False) if phase_vs2_4_receipt_present else False,
        "phase_vs2_prospective_authority_envelope_active": phase_vs2_4_post_state.get("prospective_authority_envelope_active", False) if phase_vs2_4_receipt_present else False,
        "phase_vs2_successor_binding_manifest_constructed": phase_vs2_4_post_state.get("successor_binding_manifest_constructed", False) if phase_vs2_4_receipt_present else False,
        "phase_vs2_m0_unchanged": phase_vs2_4_post_state.get("M0_unchanged", False) if phase_vs2_4_receipt_present else False,
        "phase_vs2_selector_constructed": phase_vs2_4_post_state.get("selector_constructed", False) if phase_vs2_4_receipt_present else (phase_vs2_3_post_state.get("selector_constructed", False) if phase_vs2_3_receipt_present else False),
        "phase_vs2_applicator_constructed": phase_vs2_4_post_state.get("applicator_constructed", False) if phase_vs2_4_receipt_present else (phase_vs2_3_post_state.get("applicator_constructed", False) if phase_vs2_3_receipt_present else False),
        "phase_vs2_validation_execution_logic_constructed": phase_vs2_4_post_state.get("validation_execution_logic_constructed", False) if phase_vs2_4_receipt_present else (phase_vs2_3_post_state.get("validation_execution_logic_constructed", False) if phase_vs2_3_receipt_present else False),
        "phase_vs2_admissibility_execution_logic_constructed": phase_vs2_4_post_state.get("candidate_admissibility_execution_logic_constructed", False) if phase_vs2_4_receipt_present else (phase_vs2_3_post_state.get("admissibility_execution_logic_constructed", False) if phase_vs2_3_receipt_present else False),
        "phase_vs2_convergence_criterion_constructed": phase_vs2_4_post_state.get("convergence_criterion_constructed", False) if phase_vs2_4_receipt_present else (phase_vs2_3_post_state.get("convergence_criterion_constructed", False) if phase_vs2_3_receipt_present else False),
        "phase_vs2_source_snapshot_frozen": phase_vs2_4_post_state.get("exact_source_snapshot_frozen", False) if phase_vs2_4_receipt_present else (phase_vs2_3_post_state.get("source_snapshot_frozen", False) if phase_vs2_3_receipt_present else False),
        "phase_vs2_4_built": phase_vs2_4_post_state.get("source_and_version_binding_contract_constructed", False) if phase_vs2_4_receipt_present else False,
        "phase_vs2_5_may_begin": phase_vs2_4_post_state.get("vs2_5_may_begin", False) if phase_vs2_4_receipt_present else False,
        "phase_vs2_4_receipt_artifact_id": phase_vs2_4_receipt.get("artifact_id") if phase_vs2_4_receipt_present else None,
        "phase_vs2_4_receipt_sha256": phase_vs2_4_receipt_binding.get("receipt_sha256") if phase_vs2_4_receipt_present else None,
        "phase_vs2_4_receipt_gate": phase_vs2_4_gates.get("receipt_gate", phase_vs2_4_receipt.get("receipt_gate")) if phase_vs2_4_receipt_present else None,
        "phase_vs2_4_construction_verdict": phase_vs2_4_receipt.get("construction_verdict") if phase_vs2_4_receipt_present else None,
        "phase_vs2_terminal_transition": phase_vs2_4_receipt.get("terminal_transition") if phase_vs2_4_receipt_present else (phase_vs2_3_receipt.get("terminal_transition") if phase_vs2_3_receipt_present else (phase_vs2_2_profile.get("construction_session_terminal") if phase_vs2_2_profile_present else (phase_vs2_1_source_intake.get("terminal_transition") if phase_vs2_1_source_intake_present else None))),
        "phase_vs2_logical_terminal_transition": phase_vs2_4_receipt.get("logical_terminal_transition") if phase_vs2_4_receipt_present else None,
        "phase_vs2_move_count": phase_vs2_4_receipt.get("move_count") if phase_vs2_4_receipt_present else None,
        "phase_vs2_move_contract_count": phase_vs2_4_receipt.get("move_contract_count") if phase_vs2_4_receipt_present else None,
        "phase_vs2_vocabulary_partition_count": phase_vs2_4_receipt.get("vocabulary_partition_count") if phase_vs2_4_receipt_present else None,
        "phase_vs2_terminal_outcome_count": phase_vs2_4_receipt.get("terminal_outcome_count") if phase_vs2_4_receipt_present else None,
        "phase_vs2_stop_budget_exhausted_present": phase_vs2_4_receipt.get("stop_budget_exhausted_present") if phase_vs2_4_receipt_present else None,
        "phase_vs2_downstream_binding_count_after_vs2_4": phase_vs2_4_receipt.get("downstream_binding_count") if phase_vs2_4_receipt_present else None,
        "phase_vs2_pending_binding_count_after_vs2_4": phase_vs2_4_receipt.get("pending_binding_count") if phase_vs2_4_receipt_present else None,
        "phase_vs2_absent_by_policy_binding_count_after_vs2_4": phase_vs2_4_receipt.get("absent_by_policy_binding_count") if phase_vs2_4_receipt_present else None,
        "phase_vs2_fabricated_future_reference_count_after_vs2_4": phase_vs2_4_receipt.get("fabricated_future_reference_count") if phase_vs2_4_receipt_present else None,
        "phase_vs2_source_and_version_binding_contract_artifact_id": phase_vs2_4_bindings.get("S0", {}).get("artifact_id") if phase_vs2_4_receipt_present else None,
        "phase_vs2_source_and_version_binding_contract_sha256": phase_vs2_4_bindings.get("S0", {}).get("canonical_sha256") if phase_vs2_4_receipt_present else None,
        "phase_vs2_move_vocabulary_partition_artifact_id": phase_vs2_4_bindings.get("V0", {}).get("artifact_id") if phase_vs2_4_receipt_present else None,
        "phase_vs2_move_vocabulary_partition_sha256": phase_vs2_4_bindings.get("V0", {}).get("canonical_sha256") if phase_vs2_4_receipt_present else None,
        "phase_vs2_move_authority_matrix_artifact_id": phase_vs2_4_bindings.get("A0", {}).get("artifact_id") if phase_vs2_4_receipt_present else None,
        "phase_vs2_move_authority_matrix_sha256": phase_vs2_4_bindings.get("A0", {}).get("canonical_sha256") if phase_vs2_4_receipt_present else None,
        "phase_vs2_finite_move_space_artifact_id": phase_vs2_4_bindings.get("MS0", {}).get("artifact_id") if phase_vs2_4_receipt_present else None,
        "phase_vs2_finite_move_space_sha256": phase_vs2_4_bindings.get("MS0", {}).get("canonical_sha256") if phase_vs2_4_receipt_present else None,
        "phase_vs2_prospective_authority_envelope_artifact_id": phase_vs2_4_bindings.get("P0", {}).get("artifact_id") if phase_vs2_4_receipt_present else None,
        "phase_vs2_prospective_authority_envelope_sha256": phase_vs2_4_bindings.get("P0", {}).get("canonical_sha256") if phase_vs2_4_receipt_present else None,
        "phase_vs2_move_space_binding_manifest_artifact_id": phase_vs2_4_bindings.get("M1", {}).get("artifact_id") if phase_vs2_4_receipt_present else None,
        "phase_vs2_move_space_binding_manifest_sha256": phase_vs2_4_bindings.get("M1", {}).get("canonical_sha256") if phase_vs2_4_receipt_present else None,
        "phase_vs2_move_hashes": phase_vs2_4_move_hashes if phase_vs2_4_receipt_present else {},
        "phase_vs2_execution_authority_absent": not phase_vs2_4_post_state.get("execution_authorized", False) if phase_vs2_4_receipt_present else None,
        "phase_vs2_sweep_authority_absent": not phase_vs2_4_post_state.get("sweep_authorized", False) if phase_vs2_4_receipt_present else None,
        "phase_vs2_automatic_rerun_authority_absent": not phase_vs2_4_post_state.get("automatic_rerun_authorized", False) if phase_vs2_4_receipt_present else None,
        "phase_vs2_runner_authority_absent": not phase_vs2_4_post_state.get("runner_created", False) if phase_vs2_4_receipt_present else None,
        "phase_vs2_current_unit": phase_vs2_5_receipt.get("unit_id") if phase_vs2_5_receipt_present else (phase_vs2_4_receipt.get("unit_id") if phase_vs2_4_receipt_present else (phase_vs2_3_receipt.get("unit_id") if phase_vs2_3_receipt_present else (phase_vs2_2_profile.get("unit_id") if phase_vs2_2_profile_present else (phase_vs2_1_source_intake.get("unit_id") if phase_vs2_1_source_intake_present else None)))),
        "phase_vs2_next_unit": "VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS_PENDING" if phase_vs2_5_receipt_present else ("VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_PENDING" if phase_vs2_4_receipt_present else ("VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PENDING" if phase_vs2_3_receipt_present else ("VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PENDING" if phase_vs2_2_profile_present else ("VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_PENDING" if phase_vs2_1_source_intake_present else None)))),
        "phase_vs2_5_built": phase_vs2_5_receipt_present,
        "phase_vs2_5_built_but_uncommitted": phase_vs2_5_receipt_present,
        "phase_vs2_5_receipt_artifact_id": phase_vs2_5_receipt.get("artifact_id") if phase_vs2_5_receipt_present else None,
        "phase_vs2_5_receipt_sha256": phase_vs2_5_receipt_binding.get("receipt_sha256") if phase_vs2_5_receipt_present else None,
        "phase_vs2_5_receipt_gate": phase_vs2_5_receipt.get("receipt_gate") if phase_vs2_5_receipt_present else None,
        "phase_vs2_5_construction_verdict": phase_vs2_5_receipt.get("construction_verdict") if phase_vs2_5_receipt_present else None,
        "phase_vs2_5_logical_terminal_transition": phase_vs2_5_receipt.get("logical_terminal_transition") if phase_vs2_5_receipt_present else None,
        "phase_vs2_5_terminal_transition": phase_vs2_5_receipt.get("terminal_transition") if phase_vs2_5_receipt_present else None,
        "phase_vs2_controlled_step_package_artifact_id": phase_vs2_5_bindings.get("K0", {}).get("artifact_id") if phase_vs2_5_receipt_present else None,
        "phase_vs2_controlled_step_package_sha256": phase_vs2_5_bindings.get("K0", {}).get("canonical_sha256") if phase_vs2_5_receipt_present else None,
        "phase_vs2_convergence_criterion_contract_artifact_id": phase_vs2_5_bindings.get("C20", {}).get("artifact_id") if phase_vs2_5_receipt_present else None,
        "phase_vs2_convergence_criterion_contract_sha256": phase_vs2_5_bindings.get("C20", {}).get("canonical_sha256") if phase_vs2_5_receipt_present else None,
        "phase_vs2_receipt_and_atomic_publication_contract_artifact_id": phase_vs2_5_bindings.get("R13", {}).get("artifact_id") if phase_vs2_5_receipt_present else None,
        "phase_vs2_receipt_and_atomic_publication_contract_sha256": phase_vs2_5_bindings.get("R13", {}).get("canonical_sha256") if phase_vs2_5_receipt_present else None,
        "phase_vs2_controlled_step_binding_manifest_artifact_id": phase_vs2_5_bindings.get("M2", {}).get("artifact_id") if phase_vs2_5_receipt_present else None,
        "phase_vs2_controlled_step_binding_manifest_sha256": phase_vs2_5_bindings.get("M2", {}).get("canonical_sha256") if phase_vs2_5_receipt_present else None,
        "phase_vs2_component_count": phase_vs2_5_receipt.get("component_count") if phase_vs2_5_receipt_present else None,
        "phase_vs2_primary_invocation_outcome_count": phase_vs2_5_receipt.get("primary_invocation_outcome_count") if phase_vs2_5_receipt_present else None,
        "phase_vs2_terminal_count": phase_vs2_5_receipt.get("terminal_outcome_count") if phase_vs2_5_receipt_present else None,
        "phase_vs2_terminal_outcome_count": phase_vs2_5_receipt.get("terminal_outcome_count") if phase_vs2_5_receipt_present else (phase_vs2_4_receipt.get("terminal_outcome_count") if phase_vs2_4_receipt_present else None),
        "phase_vs2_stop_budget_exhausted_present": phase_vs2_5_post_state.get("stop_budget_exhausted_present") if phase_vs2_5_receipt_present else (phase_vs2_4_receipt.get("stop_budget_exhausted_present") if phase_vs2_4_receipt_present else None),
        "phase_vs2_construction_consumption_count": phase_vs2_5_authority.get("bounded_construction_consumption_count_after") if phase_vs2_5_receipt_present else (phase_vs2_4_authority.get("bounded_construction_consumption_count_after") if phase_vs2_4_receipt_present else None),
        "phase_vs2_grant_consumption_count": phase_vs2_5_authority.get("bounded_construction_consumption_count_after", 1) if phase_vs2_5_receipt_present else (phase_vs2_4_authority.get("bounded_construction_consumption_count_after", phase_vs2_3_authority.get("total_consumed_grant_count", 0)) if phase_vs2_4_receipt_present else (phase_vs2_3_authority.get("total_consumed_grant_count", 0) if phase_vs2_3_receipt_present else (phase_vs2_2_post_state.get("vs2_grant_consumption_count", 0) if phase_vs2_2_profile_present else (phase_vs2_1_post_state.get("vs2_grant_consumption_count", 0) if phase_vs2_1_source_intake_present else 0)))),
        "phase_vs2_construction_frame_closed_after_vs2_5": phase_vs2_5_authority.get("bounded_construction_frame_open_after_vs2_5") is False if phase_vs2_5_receipt_present else None,
        "phase_vs2_bounded_construction_frame_open_after_vs2_5": phase_vs2_5_authority.get("bounded_construction_frame_open_after_vs2_5") if phase_vs2_5_receipt_present else None,
        "phase_vs2_remaining_effective_grant_count": phase_vs2_5_authority.get("unconsumed_effective_grant_count") if phase_vs2_5_receipt_present else (phase_vs2_4_authority.get("unconsumed_effective_grant_count") if phase_vs2_4_receipt_present else (phase_vs2_3_authority.get("unconsumed_effective_grant_count") if phase_vs2_3_receipt_present else (phase_vs2_2_remaining_grants.get("remaining_effective_grant_count") if phase_vs2_2_profile_present else None))),
        "phase_vs2_three_effective_grants_remain_unconsumed": phase_vs2_5_authority.get("unconsumed_effective_grant_count") == 3 if phase_vs2_5_receipt_present else None,
        "phase_vs2_move_space_frozen": phase_vs2_5_post_state.get("move_space_frozen", False) if phase_vs2_5_receipt_present else (phase_vs2_4_post_state.get("move_space_frozen", False) if phase_vs2_4_receipt_present else False),
        "phase_vs2_move_space_active": phase_vs2_5_post_state.get("move_space_active", False) if phase_vs2_5_receipt_present else (phase_vs2_4_post_state.get("move_space_active", False) if phase_vs2_4_receipt_present else False),
        "phase_vs2_selector_constructed": phase_vs2_5_post_state.get("selector_defined", False) if phase_vs2_5_receipt_present else (phase_vs2_4_post_state.get("selector_constructed", False) if phase_vs2_4_receipt_present else False),
        "phase_vs2_selector_executed": phase_vs2_5_post_state.get("selector_executed", False) if phase_vs2_5_receipt_present else None,
        "phase_vs2_applicator_constructed": phase_vs2_5_post_state.get("applicator_defined", False) if phase_vs2_5_receipt_present else (phase_vs2_4_post_state.get("applicator_constructed", False) if phase_vs2_4_receipt_present else False),
        "phase_vs2_applicator_executed": phase_vs2_5_post_state.get("applicator_executed", False) if phase_vs2_5_receipt_present else None,
        "phase_vs2_validation_execution_logic_constructed": phase_vs2_5_post_state.get("validator_defined", False) if phase_vs2_5_receipt_present else (phase_vs2_4_post_state.get("validation_execution_logic_constructed", False) if phase_vs2_4_receipt_present else False),
        "phase_vs2_admissibility_execution_logic_constructed": phase_vs2_5_post_state.get("admissibility_evaluator_defined", False) if phase_vs2_5_receipt_present else (phase_vs2_4_post_state.get("candidate_admissibility_execution_logic_constructed", False) if phase_vs2_4_receipt_present else False),
        "phase_vs2_convergence_criterion_constructed": phase_vs2_5_post_state.get("convergence_criterion_constructed", False) if phase_vs2_5_receipt_present else (phase_vs2_4_post_state.get("convergence_criterion_constructed", False) if phase_vs2_4_receipt_present else False),
        "phase_vs2_atomic_publication_protocol_defined": phase_vs2_5_post_state.get("atomic_publication_protocol_defined", False) if phase_vs2_5_receipt_present else None,
        "phase_vs2_atomic_publication_performed": phase_vs2_5_post_state.get("atomic_publication_performed", False) if phase_vs2_5_receipt_present else None,
        "phase_vs2_fixtures_pending": phase_vs2_5_post_state.get("fixture_set_bound") is False if phase_vs2_5_receipt_present else None,
        "phase_vs2_exact_source_snapshot_pending": phase_vs2_5_post_state.get("exact_source_snapshot_bound") is False if phase_vs2_5_receipt_present else None,
        "phase_vs2_exact_runtime_budgets_pending": phase_vs2_5_post_state.get("exact_runtime_budgets_bound") is False if phase_vs2_5_receipt_present else None,
        "phase_vs2_active_execution_authority_absent": phase_vs2_5_post_state.get("active_execution_authority_present") is False if phase_vs2_5_receipt_present else (not phase_vs2_4_post_state.get("execution_authorized", False) if phase_vs2_4_receipt_present else None),
        "phase_vs2_active_sweep_authority_absent": phase_vs2_5_post_state.get("active_sweep_authority_present") is False if phase_vs2_5_receipt_present else (not phase_vs2_4_post_state.get("sweep_authorized", False) if phase_vs2_4_receipt_present else None),
        "phase_vs2_runtime_instance_created": phase_vs2_5_post_state.get("runtime_instance_created", False) if phase_vs2_5_receipt_present else (phase_vs2_4_post_state.get("runtime_instance_created", False) if phase_vs2_4_receipt_present else False),
        "phase_vs2_candidate_instance_created": phase_vs2_5_post_state.get("candidate_instance_created", False) if phase_vs2_5_receipt_present else (phase_vs2_4_post_state.get("candidate_instance_created", False) if phase_vs2_4_receipt_present else False),
        "phase_vs2_move_enumerated_against_live_candidate": phase_vs2_5_post_state.get("move_enumerated_against_live_candidate", False) if phase_vs2_5_receipt_present else None,
        "phase_vs2_move_selected": phase_vs2_5_post_state.get("move_selected", False) if phase_vs2_5_receipt_present else None,
        "phase_vs2_move_applied": phase_vs2_5_post_state.get("move_applied", False) if phase_vs2_5_receipt_present else None,
        "phase_vs2_execution_performed": phase_vs2_5_post_state.get("execution_performed", False) if phase_vs2_5_receipt_present else (phase_vs2_4_post_state.get("execution_performed", False) if phase_vs2_4_receipt_present else False),
        "phase_vs2_sweep_executed": phase_vs2_5_post_state.get("sweep_executed", False) if phase_vs2_5_receipt_present else (phase_vs2_4_post_state.get("sweep_executed", False) if phase_vs2_4_receipt_present else False),
        "phase_vs2_runner_created": phase_vs2_5_post_state.get("runner_created", False) if phase_vs2_5_receipt_present else (phase_vs2_4_post_state.get("runner_created", False) if phase_vs2_4_receipt_present else False),
        "phase_vs2_5_component_hashes": phase_vs2_5_component_hashes if phase_vs2_5_receipt_present else {},
        "phase_vs2_5_gates": phase_vs2_5_gates if phase_vs2_5_receipt_present else {},
        "current_unit": phase_vs2_current_unit,
        "phase_vs2_current_unit": phase_vs2_current_unit,
        "phase_vs2_next_unit": phase_vs2_6_next_unit,
        "next_lawful_unit": phase_vs2_6_next_unit,
        "readiness_verdict": phase_vs2_6_receipt.get("readiness_verdict") if phase_vs2_6_receipt_present else None,
        "execution_package_core_id": phase_vs2_6_bindings.get("E0", {}).get("artifact_id") if phase_vs2_6_receipt_present else None,
        "execution_package_core_sha256": phase_vs2_6_bindings.get("E0", {}).get("canonical_sha256") if phase_vs2_6_receipt_present else None,
        "readiness_seal_id": phase_vs2_6_bindings.get("RS0", {}).get("artifact_id") if phase_vs2_6_receipt_present else None,
        "readiness_seal_sha256": phase_vs2_6_bindings.get("RS0", {}).get("canonical_sha256") if phase_vs2_6_receipt_present else None,
        "fixture_count": phase_vs2_6_receipt.get("fixture_count") if phase_vs2_6_receipt_present else None,
        "static_candidate_specimen_count": phase_vs2_6_receipt.get("static_candidate_specimen_count") if phase_vs2_6_receipt_present else None,
        "runtime_candidate_instance_count": phase_vs2_6_receipt.get("runtime_candidate_instance_count") if phase_vs2_6_receipt_present else None,
        "runtime_reports_emitted": phase_vs2_6_receipt.get("runtime_reports_emitted") if phase_vs2_6_receipt_present else None,
        "execution_authority_present": phase_vs2_6_receipt.get("execution_authority_present") if phase_vs2_6_receipt_present else None,
        "remaining_effective_grant_count": phase_vs2_6_receipt.get("remaining_effective_grant_count_after") if phase_vs2_6_receipt_present else None,
        "phase_vs2_remaining_effective_grant_count": phase_vs2_6_receipt.get("remaining_effective_grant_count_after") if phase_vs2_6_receipt_present else (phase_vs2_5_authority.get("unconsumed_effective_grant_count") if phase_vs2_5_receipt_present else None),
        "logical_terminal_transition": phase_vs2_6_receipt.get("logical_transition") if phase_vs2_6_receipt_present else None,
        "bookkeeping_transition": phase_vs2_6_receipt.get("bookkeeping_transition") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_built": phase_vs2_6_receipt_present,
        "phase_vs2_6_built_but_uncommitted": phase_vs2_6_receipt_present,
        "phase_vs2_6_receipt_artifact_id": phase_vs2_6_receipt.get("artifact_id") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_receipt_sha256": phase_vs2_6_receipt.get("receipt_binding", {}).get("receipt_sha256") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_readiness_verdict": phase_vs2_6_receipt.get("readiness_verdict") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_seal_status": phase_vs2_6_receipt.get("seal_status") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_eligible_for_execution_decision": phase_vs2_6_receipt.get("eligible_for_execution_decision") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_execution_package_core_artifact_id": phase_vs2_6_bindings.get("E0", {}).get("artifact_id") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_execution_package_core_sha256": phase_vs2_6_bindings.get("E0", {}).get("canonical_sha256") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_readiness_gate_artifact_id": phase_vs2_6_bindings.get("G0", {}).get("artifact_id") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_readiness_gate_sha256": phase_vs2_6_bindings.get("G0", {}).get("canonical_sha256") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_readiness_gate_receipt_artifact_id": phase_vs2_6_bindings.get("GR0", {}).get("artifact_id") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_readiness_gate_receipt_sha256": phase_vs2_6_bindings.get("GR0", {}).get("canonical_sha256") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_readiness_seal_artifact_id": phase_vs2_6_bindings.get("RS0", {}).get("artifact_id") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_readiness_seal_sha256": phase_vs2_6_bindings.get("RS0", {}).get("canonical_sha256") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_fixture_count": phase_vs2_6_receipt.get("fixture_count") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_static_candidate_specimen_count": phase_vs2_6_receipt.get("static_candidate_specimen_count") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_runtime_candidate_instance_count": phase_vs2_6_receipt.get("runtime_candidate_instance_count") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_runtime_reports_emitted": phase_vs2_6_receipt.get("runtime_reports_emitted") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_runtime_receipts_emitted": phase_vs2_6_receipt.get("runtime_receipts_emitted") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_execution_authority_present": phase_vs2_6_receipt.get("execution_authority_present") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_remaining_effective_grant_count": phase_vs2_6_receipt.get("remaining_effective_grant_count_after") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_logical_terminal_transition": phase_vs2_6_receipt.get("logical_transition") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_bookkeeping_transition": phase_vs2_6_receipt.get("bookkeeping_transition") if phase_vs2_6_receipt_present else None,
        "phase_vs2_6_artifact_bindings": phase_vs2_6_bindings if phase_vs2_6_receipt_present else {},
        "phase_vs2_6_candidate_hashes": {key: value.get("canonical_sha256") for key, value in phase_vs2_6_candidate_bindings.items()} if phase_vs2_6_receipt_present else {},
        "phase_vs2_6_fixture_definition_hashes": {key: value.get("canonical_sha256") for key, value in phase_vs2_6_fixture_definition_bindings.items()} if phase_vs2_6_receipt_present else {},
        "phase_vs2_6_report_contract_hashes": {key: value.get("canonical_sha256") for key, value in phase_vs2_6_report_bindings.items()} if phase_vs2_6_receipt_present else {},
        "phase_vs2_6_r01_through_r21_statuses": phase_vs2_6_record_statuses if phase_vs2_6_receipt_present else {},
        "phase_vs2_6_r01_through_r21_count": len(phase_vs2_6_records) if phase_vs2_6_receipt_present else 0,
        "current_unit": phase_vs2_current_unit,
        "phase_vs2_current_unit": phase_vs2_current_unit,
        "phase_status": phase_vs2_7_payload.get("phase_status") if phase_vs2_7_closure_present else None,
        "closure_gate": phase_vs2_7_payload.get("closure_gate") if phase_vs2_7_closure_present else None,
        "readiness_branch": phase_vs2_7_payload.get("readiness_branch") if phase_vs2_7_closure_present else None,
        "execution_package_core_artifact_id": phase_vs2_7_e0.get("artifact_id") if phase_vs2_7_closure_present else None,
        "execution_package_core_id": phase_vs2_7_e0.get("package_id") if phase_vs2_7_closure_present else (phase_vs2_6_bindings.get("E0", {}).get("artifact_id") if phase_vs2_6_receipt_present else None),
        "execution_package_core_sha256": phase_vs2_7_e0.get("canonical_sha256") if phase_vs2_7_closure_present else (phase_vs2_6_bindings.get("E0", {}).get("canonical_sha256") if phase_vs2_6_receipt_present else None),
        "readiness_seal_artifact_id": phase_vs2_7_rs0.get("artifact_id") if phase_vs2_7_closure_present else None,
        "readiness_seal_id": phase_vs2_7_rs0.get("seal_id") if phase_vs2_7_closure_present else (phase_vs2_6_bindings.get("RS0", {}).get("artifact_id") if phase_vs2_6_receipt_present else None),
        "readiness_seal_sha256": phase_vs2_7_rs0.get("canonical_sha256") if phase_vs2_7_closure_present else (phase_vs2_6_bindings.get("RS0", {}).get("canonical_sha256") if phase_vs2_6_receipt_present else None),
        "next_lawful_surface": phase_vs2_7_surface.get("surface_id") if phase_vs2_7_closure_present else None,
        "next_surface_created": phase_vs2_7_surface.get("created_by_vs2_7") if phase_vs2_7_closure_present else None,
        "execution_authority_present": phase_vs2_7_authority.get("execution_authority_present") if phase_vs2_7_closure_present else (phase_vs2_6_receipt.get("execution_authority_present") if phase_vs2_6_receipt_present else None),
        "execution_started": phase_vs2_7_execution.get("execution_started") if phase_vs2_7_closure_present else None,
        "runner_created": phase_vs2_7_authority.get("runner_created") if phase_vs2_7_closure_present else None,
        "terminal_transition": phase_vs2_7_terminal.get("transition") if phase_vs2_7_closure_present else None,
        "phase_vs2_7_built": phase_vs2_7_closure_present,
        "phase_vs2_7_closure_artifact_id": phase_vs2_7_closure.get("artifact_id") if phase_vs2_7_closure_present else None,
        "phase_vs2_7_closure_sha256": phase_vs2_7_closure.get("closure_payload_sha256") if phase_vs2_7_closure_present else None,
        "phase_vs2_7_receipt_artifact_id": phase_vs2_7_receipt.get("receipt_id") if phase_vs2_7_receipt_present else None,
        "phase_vs2_7_receipt_sha256": phase_vs2_7_receipt.get("receipt_payload_sha256") if phase_vs2_7_receipt_present else None,
        "phase_vs2_7_receipt_gate": phase_vs2_7_receipt_payload.get("closure_gate") if phase_vs2_7_receipt_present else None,
        "phase_vs2_next_unit": phase_vs2_6_next_unit,
        "next_lawful_unit": phase_vs2_6_next_unit,
        "current_unit": post_vs2_payload.get("unit_id") if post_vs2_surface_present else phase_vs2_current_unit,
        "current_surface": post_vs2_payload.get("surface_id") if post_vs2_surface_present else None,
        "surface_gate": post_vs2_payload.get("surface_gate") if post_vs2_surface_present else None,
        "surface_instance_state": post_vs2_payload.get("surface_instance_state") if post_vs2_surface_present else None,
        "human_decision_required": post_vs2_decision.get("human_decision_required") if post_vs2_surface_present else None,
        "human_decision_recorded": post_vs2_decision.get("human_decision_recorded") if post_vs2_surface_present else None,
        "decision_receipt_created": post_vs2_decision.get("decision_receipt_created") if post_vs2_surface_present else None,
        "decision_option_count": len(post_vs2_payload.get("decision_options", [])) if post_vs2_surface_present else None,
        "execution_package_core_id": post_vs2_e0.get("logical_package_id") if post_vs2_surface_present else (phase_vs2_7_e0.get("package_id") if phase_vs2_7_closure_present else None),
        "execution_package_core_sha256": post_vs2_e0.get("canonical_sha256") if post_vs2_surface_present else (phase_vs2_7_e0.get("canonical_sha256") if phase_vs2_7_closure_present else None),
        "readiness_seal_id": post_vs2_rs0.get("logical_seal_id") if post_vs2_surface_present else (phase_vs2_7_rs0.get("seal_id") if phase_vs2_7_closure_present else None),
        "readiness_seal_sha256": post_vs2_rs0.get("canonical_sha256") if post_vs2_surface_present else (phase_vs2_7_rs0.get("canonical_sha256") if phase_vs2_7_closure_present else None),
        "authority_update_applied": post_vs2_authority.get("authority_update_applied") if post_vs2_surface_present else None,
        "execution_authority_present": post_vs2_authority.get("execution_authority_present") if post_vs2_surface_present else (phase_vs2_7_authority.get("execution_authority_present") if phase_vs2_7_closure_present else None),
        "sweep_authority_present": post_vs2_authority.get("sweep_authority_present") if post_vs2_surface_present else None,
        "run_allocation_authority_present": post_vs2_authority.get("run_allocation_authority_present") if post_vs2_surface_present else None,
        "run_id_created": post_vs2_execution.get("run_id_created") if post_vs2_surface_present else None,
        "execution_source_intake_created": post_vs2_execution.get("execution_source_intake_created") if post_vs2_surface_present else None,
        "execution_started": post_vs2_execution.get("execution_started") if post_vs2_surface_present else (phase_vs2_7_execution.get("execution_started") if phase_vs2_7_closure_present else None),
        "runtime_receipts_emitted": post_vs2_execution.get("runtime_receipts_emitted") if post_vs2_surface_present else None,
        "runtime_reports_emitted": post_vs2_execution.get("runtime_reports_emitted") if post_vs2_surface_present else None,
        "runner_created": post_vs2_authority.get("runner_authority_present") if post_vs2_surface_present else (phase_vs2_7_authority.get("runner_created") if phase_vs2_7_closure_present else None),
        "terminal_transition": post_vs2_terminal.get("transition") if post_vs2_surface_present else (phase_vs2_7_terminal.get("transition") if phase_vs2_7_closure_present else None),
        "next_lawful_action": "HUMAN_DECISION_REQUIRED" if post_vs2_surface_present else None,
        "post_vs2_surface_built": post_vs2_surface_present,
        "post_vs2_surface_artifact_id": post_vs2_surface.get("artifact_id") if post_vs2_surface_present else None,
        "post_vs2_surface_sha256": post_vs2_surface.get("surface_payload_sha256") if post_vs2_surface_present else None,
        "post_vs2_receipt_artifact_id": post_vs2_receipt.get("receipt_id") if post_vs2_receipt_present else None,
        "post_vs2_receipt_sha256": post_vs2_receipt.get("receipt_payload_sha256") if post_vs2_receipt_present else None,
        "post_vs2_receipt_gate": post_vs2_receipt_payload.get("surface_gate") if post_vs2_receipt_present else None,
        "promotion_receipt_created": d2_promotion_decision_receipt_present,
        "activation_object_created": False,
        "router_classification_created": b2_route_classification_present,
        "router_created": False,
        "b2_created": b2_route_classification_present,
        "b3_created": b3_router_specimen_closure_present,
    }
    if post_vs2_machinery_receipt_present:
        manifest.update(
            {
                "current_unit": "POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_PREPARATION",
                "current_surface": "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE",
                "surface_instance_state": "UNCONSUMED",
                "human_decision_required": True,
                "human_decision_input_present": False,
                "human_decision_recorded": False,
                "selected_option": None,
                "decision_receipt_created": False,
                "decision_receipt_machinery_ready": True,
                "decision_option_count": 6,
                "authority_update_applied": False,
                "execution_authority_present": False,
                "sweep_authority_present": False,
                "run_allocation_authority_present": False,
                "run_id_created": False,
                "execution_source_intake_created": False,
                "execution_started": False,
                "runtime_receipts_emitted": 0,
                "runtime_reports_emitted": 0,
                "runner_created": False,
                "terminal_transition": "STOP_POST_VS2_DECISION_RECEIPT_MACHINERY_READY_SURFACE_UNCONSUMED",
                "next_lawful_action": "SUPPLY_ONE_EXPLICIT_AUTHENTICATED_POST_VS2_HUMAN_DECISION_INPUT",
                "decision_receipt_machinery_gate": post_vs2_machinery_payload.get("machinery_gate"),
                "decision_receipt_machinery_receipt_id": post_vs2_machinery_receipt.get("receipt_id"),
                "decision_receipt_machinery_receipt_sha256": post_vs2_machinery_receipt.get("receipt_binding", {}).get("receipt_sha256"),
                "human_decision_input_contract_id": "POST_VS2_FIRST_EXECUTION_HUMAN_DECISION_INPUT_CONTRACT_V0",
                "decision_receipt_contract_id": "POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_CONTRACT_V0",
                "authoritative_decision_receipt_created": False,
                "authoritative_human_decision_input_created": False,
                "authority_update_eligibility_for_real_decision_claimed": False,
                "execution_authorized": False,
            }
        )
    return manifest


def generate() -> int:
    root = detect_repo_root(Path.cwd())
    baseline = ensure_safe_baseline_dir(root)

    head = run_git(root, ["rev-parse", "HEAD"], check=True)
    generated_at = stable_generated_at_for_head(root, head)
    branch = run_git(root, ["branch", "--show-current"])
    raw_status_lines = run_git(root, ["status", "--short"]).splitlines()
    status_lines = raw_status_lines
    status_lines_excluding_baseline_share = git_status_excluding_baseline_share(
        root,
        raw_status_lines,
    )
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
            root,
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
    _baseline_exit_code = main()
    # BASELINE_UNCOMMITTED_VS0_3_MARKER_FILTER_V1_MAIN_EXIT_CALL
    _baseline_filter_uncommitted_vs0_3_markers_v1()
    raise SystemExit(_baseline_exit_code)
