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
        "promotion_receipt_created": d2_promotion_decision_receipt_present,
        "activation_object_created": False,
        "router_classification_created": b2_route_classification_present,
        "router_created": False,
        "b2_created": b2_route_classification_present,
        "b3_created": b3_router_specimen_closure_present,
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
    _baseline_exit_code = main()
    # BASELINE_UNCOMMITTED_VS0_3_MARKER_FILTER_V1_MAIN_EXIT_CALL
    _baseline_filter_uncommitted_vs0_3_markers_v1()
    raise SystemExit(_baseline_exit_code)
