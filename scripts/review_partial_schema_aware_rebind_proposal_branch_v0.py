#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_REVIEW"
MODE = "PROPOSAL_BRANCH_REVIEW / HOLD_PRESERVED / AUTHORIZATION_CONTRACT_REQUIRED / NO_REBIND_APPLICATION"
BUILD_MODE = "PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_REVIEW_ONLY"

SOURCE_BRANCH_SPLIT_REVIEW_RECEIPT_ID = "76ee513b"
SOURCE_BRANCH_SPLIT_REVIEW_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_review_v0_receipts/76ee513b.json"
SOURCE_BRANCH_SPLIT_REVIEW_ASSESSMENT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_review_v0/typed_machine_readable_partial_schema_aware_rebind_branch_split_review_assessment_v0.json"
SOURCE_PROPOSAL_BRANCH_CONTRACT_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_contract_review_v0.json"
SOURCE_PROPOSAL_HOLD_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_hold_review_v0.json"
SOURCE_BRANCH_EXECUTION_READINESS_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_review_v0/typed_machine_readable_partial_schema_aware_rebind_branch_execution_readiness_table_v0.json"
SOURCE_NEXT_BRANCH_DECISION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_review_v0/typed_machine_readable_partial_schema_aware_rebind_next_branch_decision_table_v0.json"
SOURCE_BRANCH_SPLIT_REVIEW_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_review_v0/typed_machine_readable_partial_schema_aware_rebind_branch_split_review_result_packet_v0.json"
SOURCE_BRANCH_SPLIT_REVIEW_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_review_v0/typed_machine_readable_partial_schema_aware_rebind_branch_split_review_classification_v0.json"
SOURCE_BRANCH_SPLIT_REVIEW_AUTHORITY_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_review_v0/typed_machine_readable_partial_schema_aware_rebind_branch_split_review_authority_boundary_v0.json"
SOURCE_BRANCH_SPLIT_REVIEW_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_review_v0/typed_machine_readable_partial_schema_aware_rebind_branch_split_review_rollup_v0.json"
SOURCE_BRANCH_SPLIT_REVIEW_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_review_v0/typed_machine_readable_partial_schema_aware_rebind_branch_split_review_profile_v0.json"

SOURCE_PROPOSAL_BRANCH_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_contract_v0.json"
SOURCE_PROPOSAL_BRANCH_HOLD_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_hold_packet_v0.json"

SOURCE_PARTIAL_PROPOSAL_REVIEW_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_review_table_v0.json"
SOURCE_PARTIAL_PROPOSAL_REVIEW_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_review_surface_v0.json"
SOURCE_PARTIAL_AMBIGUITY_REPAIR_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_ambiguity_repair_surface_v0.json"
SOURCE_PARTIAL_REQUIREMENT_GAP_REPAIR_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_requirement_gap_repair_surface_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_review_assessment_v0.json"
PROPOSAL_BRANCH_INPUT_INVENTORY_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_input_inventory_v0.json"
PROPOSAL_CANDIDATE_REVIEW_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_candidate_review_table_v0.json"
PROPOSAL_CANDIDATE_INTEGRITY_SURFACE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_candidate_integrity_surface_v0.json"
PROPOSAL_HOLD_PRESERVATION_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_hold_preservation_contract_v0.json"
PROPOSAL_APPLICATION_PRECONDITION_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_application_precondition_table_v0.json"
PROPOSAL_AUTHORIZATION_REQUEST_PACKET_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_authorization_request_packet_v0.json"
RESIDUAL_BRANCH_PRESERVATION_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_residual_branch_preservation_contract_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_downstream_decision_table_v0.json"
REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_review_packet_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_BRANCH_SPLIT_REVIEW_RECEIPT_PATH,
    SOURCE_BRANCH_SPLIT_REVIEW_ASSESSMENT_PATH,
    SOURCE_PROPOSAL_BRANCH_CONTRACT_REVIEW_PATH,
    SOURCE_PROPOSAL_HOLD_REVIEW_PATH,
    SOURCE_BRANCH_EXECUTION_READINESS_TABLE_PATH,
    SOURCE_NEXT_BRANCH_DECISION_TABLE_PATH,
    SOURCE_BRANCH_SPLIT_REVIEW_PACKET_PATH,
    SOURCE_BRANCH_SPLIT_REVIEW_CLASSIFICATION_PATH,
    SOURCE_BRANCH_SPLIT_REVIEW_AUTHORITY_BOUNDARY_PATH,
    SOURCE_BRANCH_SPLIT_REVIEW_ROLLUP_PATH,
    SOURCE_BRANCH_SPLIT_REVIEW_PROFILE_PATH,
    SOURCE_PROPOSAL_BRANCH_CONTRACT_PATH,
    SOURCE_PROPOSAL_BRANCH_HOLD_PACKET_PATH,
    SOURCE_PARTIAL_PROPOSAL_REVIEW_TABLE_PATH,
    SOURCE_PARTIAL_PROPOSAL_REVIEW_SURFACE_PATH,
    SOURCE_PARTIAL_AMBIGUITY_REPAIR_SURFACE_PATH,
    SOURCE_PARTIAL_REQUIREMENT_GAP_REPAIR_SURFACE_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_REVIEWED_PROPOSAL_BRANCH_REVIEW_READY"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_REVIEWED_PROPOSAL_BRANCH_REVIEW_READY"
EXPECTED_SOURCE_NEXT = "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_V0"

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def list_records(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    v = obj.get("records")
    return v if isinstance(v, list) else []

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    receipt = read_json(SOURCE_BRANCH_SPLIT_REVIEW_RECEIPT_PATH)
    summary = receipt.get("machine_readable_partial_schema_aware_rebind_branch_split_review_summary", {})
    proposal_contract_review = read_json(SOURCE_PROPOSAL_BRANCH_CONTRACT_REVIEW_PATH)
    proposal_hold_review = read_json(SOURCE_PROPOSAL_HOLD_REVIEW_PATH)
    readiness = read_json(SOURCE_BRANCH_EXECUTION_READINESS_TABLE_PATH)
    next_decision = read_json(SOURCE_NEXT_BRANCH_DECISION_TABLE_PATH)
    classif = read_json(SOURCE_BRANCH_SPLIT_REVIEW_CLASSIFICATION_PATH)
    authority = read_json(SOURCE_BRANCH_SPLIT_REVIEW_AUTHORITY_BOUNDARY_PATH)
    rollup = read_json(SOURCE_BRANCH_SPLIT_REVIEW_ROLLUP_PATH)
    profile = read_json(SOURCE_BRANCH_SPLIT_REVIEW_PROFILE_PATH)
    proposal_contract = read_json(SOURCE_PROPOSAL_BRANCH_CONTRACT_PATH)
    proposal_hold_packet = read_json(SOURCE_PROPOSAL_BRANCH_HOLD_PACKET_PATH)
    proposal_table = read_json(SOURCE_PARTIAL_PROPOSAL_REVIEW_TABLE_PATH)
    proposal_surface = read_json(SOURCE_PARTIAL_PROPOSAL_REVIEW_SURFACE_PATH)
    ambiguity_surface = read_json(SOURCE_PARTIAL_AMBIGUITY_REPAIR_SURFACE_PATH)
    gap_surface = read_json(SOURCE_PARTIAL_REQUIREMENT_GAP_REPAIR_SURFACE_PATH)

    if receipt.get("receipt_id") != SOURCE_BRANCH_SPLIT_REVIEW_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_branch_split_review_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("selected_next_branch") != "proposal_review_branch":
        failures.append("proposal_branch_not_selected")
    if summary.get("proposal_branch_review_ready") is not True:
        failures.append("proposal_branch_not_ready")
    if summary.get("proposal_hold_released") is not False:
        failures.append("proposal_hold_already_released")
    if summary.get("proposal_binding_count") != 4:
        failures.append(f"source_proposal_binding_count_wrong:{summary.get('proposal_binding_count')}")
    if summary.get("ambiguity_binding_count") != 22:
        failures.append(f"source_ambiguity_binding_count_wrong:{summary.get('ambiguity_binding_count')}")
    if summary.get("requirement_gap_binding_count") != 498:
        failures.append(f"source_requirement_gap_binding_count_wrong:{summary.get('requirement_gap_binding_count')}")
    if summary.get("total_routed_binding_count") != 524:
        failures.append(f"source_total_routed_binding_count_wrong:{summary.get('total_routed_binding_count')}")

    for key in [
        "schema_overlay_applied_globally",
        "reusable_schema_authorized",
        "preapproved_schema_authorized",
        "validator_registry_entry_created",
        "future_automatic_use_allowed",
        "typing_rule_applied",
        "field_policy_modified",
        "candidate_artifact_modified",
        "source_row_locator_applied",
        "rebinds_applied",
        "dominance_rule_applied",
        "values_authorized",
        "values_applied",
        "null_reasons_accepted",
        "source_packet_materialized_for_review",
        "metadata_populated",
        "target_selected_for_build",
        "runtime_patch_applied",
        "c5_opened",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if summary.get(key) is not False:
            failures.append(f"source_summary_forbidden_true:{key}")
    if summary.get("ready_discriminator_count") != 0:
        failures.append("ready_discriminator_nonzero")

    if proposal_contract_review.get("proposal_review_ready") is not True:
        failures.append("proposal_contract_review_not_ready")
    if proposal_contract_review.get("proposal_application_ready") is not False:
        failures.append("proposal_contract_review_application_ready")
    if proposal_contract_review.get("release_hold_now") is not False:
        failures.append("proposal_contract_review_releases_hold")
    if proposal_hold_review.get("proposal_hold_preserved") is not True:
        failures.append("proposal_hold_not_preserved")
    if proposal_hold_review.get("released_now") is not False:
        failures.append("proposal_hold_review_released")
    readiness_records = readiness.get("records", [])
    proposal_ready_record = [r for r in readiness_records if isinstance(r, dict) and r.get("branch_id") == "proposal_review_branch"]
    if len(proposal_ready_record) != 1:
        failures.append("proposal_readiness_record_missing_or_multiple")
    elif proposal_ready_record[0].get("ready_for_review") is not True or proposal_ready_record[0].get("ready_for_application") is not False:
        failures.append("proposal_readiness_record_wrong")
    decision_records = next_decision.get("records", [])
    proposal_selected = [r for r in decision_records if isinstance(r, dict) and r.get("decision") == "REVIEW_PROPOSAL_BRANCH"]
    if len(proposal_selected) != 1 or proposal_selected[0].get("selected") is not True:
        failures.append("proposal_next_branch_decision_not_selected")
    if classif.get("selected_next_branch") != "proposal_review_branch":
        failures.append("classification_selected_branch_wrong")
    if authority.get("may_review_proposal_branch_next") is not True:
        failures.append("authority_does_not_allow_proposal_branch_review")
    if authority.get("may_release_proposal_hold") is not False:
        failures.append("authority_allows_hold_release")
    if authority.get("may_apply_rebinds") is not False:
        failures.append("authority_allows_rebinds")
    if rollup.get("proposal_branch_review_ready_count") != 1:
        failures.append("rollup_proposal_branch_ready_not_1")
    if rollup.get("rebinds_applied_count") != 0:
        failures.append("rollup_rebinds_nonzero")
    if profile.get("selected_next_branch") != "proposal_review_branch":
        failures.append("profile_selected_branch_wrong")
    if profile.get("rebinds_applied") is not False:
        failures.append("profile_rebinds_true")
    if proposal_contract.get("proposal_binding_count") != 4:
        failures.append("proposal_contract_count_wrong")
    if proposal_contract.get("may_apply_rebinds") is not False:
        failures.append("proposal_contract_allows_rebinds")
    if proposal_hold_packet.get("proposal_ready_count") != 4:
        failures.append("proposal_hold_packet_count_wrong")
    if proposal_hold_packet.get("released_now") is not False:
        failures.append("proposal_hold_packet_released")
    proposal_records = list_records(proposal_table)
    if len(proposal_records) != 4:
        failures.append(f"proposal_table_record_count_not_4:{len(proposal_records)}")
    if proposal_surface.get("proposal_ready_count") != 4:
        failures.append("proposal_surface_count_wrong")
    if proposal_surface.get("proposal_review_failure_count") != 0:
        failures.append("proposal_surface_has_review_failures")
    if ambiguity_surface.get("ambiguous_binding_count") != 22:
        failures.append("ambiguity_surface_count_wrong")
    if gap_surface.get("requirement_gap_binding_count") != 498:
        failures.append("gap_surface_count_wrong")

    return failures, {
        "summary": summary,
        "proposal_records": proposal_records,
        "proposal_contract": proposal_contract,
        "proposal_hold_packet": proposal_hold_packet,
        "ambiguity_surface": ambiguity_surface,
        "gap_surface": gap_surface,
    }

def review_proposal_records(proposals: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[str]]:
    rows: List[Dict[str, Any]] = []
    failures: List[str] = []
    seen_bindings = set()
    for idx, p in enumerate(proposals):
        row_failures: List[str] = []
        binding_key = p.get("binding_key")
        candidate_ref = p.get("candidate_ref")
        source_receipt_id = p.get("source_receipt_id")
        source_artifact_path = p.get("source_artifact_path")
        schema_requirement_score = p.get("schema_requirement_score")
        proposal_review_status = p.get("proposal_review_status")
        proposal_status = p.get("proposal_status")

        if not binding_key:
            row_failures.append("missing_binding_key")
        if binding_key in seen_bindings:
            row_failures.append("duplicate_binding_key")
        if binding_key:
            seen_bindings.add(binding_key)
        if not candidate_ref:
            row_failures.append("missing_candidate_ref")
        if not source_receipt_id:
            row_failures.append("missing_source_receipt_id")
        if not source_artifact_path:
            row_failures.append("missing_source_artifact_path")
        if not isinstance(schema_requirement_score, int):
            row_failures.append("schema_requirement_score_not_int")
        if proposal_review_status != "PROPOSAL_READY_FOR_SEPARATE_REVIEW_NOT_APPLICATION":
            row_failures.append(f"proposal_review_status_unexpected:{proposal_review_status}")
        if proposal_status != "PROPOSED_FOR_REVIEW_ONLY_NOT_APPLIED":
            row_failures.append(f"proposal_status_unexpected:{proposal_status}")
        if p.get("rebind_applied") is not False:
            row_failures.append("proposal_row_rebind_applied_not_false")

        rows.append({
            "proposal_branch_candidate_review_id": "proposal_branch_candidate_review_" + sha8({"idx": idx, "proposal": p}),
            "binding_key": binding_key,
            "candidate_ref": candidate_ref,
            "source_receipt_id": source_receipt_id,
            "source_artifact_path": source_artifact_path,
            "schema_requirement_score": schema_requirement_score,
            "proposal_review_status": proposal_review_status,
            "proposal_status": proposal_status,
            "proposal_branch_review_status": "PROPOSAL_BRANCH_CANDIDATE_REVIEW_PASS" if not row_failures else "PROPOSAL_BRANCH_CANDIDATE_REVIEW_FAIL",
            "proposal_branch_review_failures": row_failures,
            "proposal_application_authorized": False,
            "proposal_hold_released": False,
            "rebind_applied": False,
        })
        failures.extend([f"{binding_key or idx}:{x}" for x in row_failures])
    return rows, failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    proposal_records = src.get("proposal_records", [])
    proposal_rows, proposal_failures = review_proposal_records(proposal_records)

    proposal_binding_count = len(proposal_rows)
    proposal_candidate_review_pass_count = sum(1 for r in proposal_rows if r["proposal_branch_review_status"] == "PROPOSAL_BRANCH_CANDIDATE_REVIEW_PASS")
    proposal_candidate_review_fail_count = proposal_binding_count - proposal_candidate_review_pass_count
    ambiguity_binding_count = int(src.get("summary", {}).get("ambiguity_binding_count", 22) or 22)
    requirement_gap_binding_count = int(src.get("summary", {}).get("requirement_gap_binding_count", 498) or 498)

    if failures:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_REVIEW_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_REVIEW_BASIS_V0"
        auth_contract_required = False
    elif proposal_failures:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_REVIEWED_REPAIR_REQUIRED"
        reason_codes = [
            "PARTIAL_SCHEMA_AWARE_PROPOSAL_BRANCH_REVIEW_COMPLETE",
            "PROPOSAL_BRANCH_CANDIDATE_REVIEW_FAILURES_FOUND",
            "PROPOSAL_HOLD_PRESERVED",
            "NO_REBINDS_APPLIED",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
        ] + proposal_failures
        next_edge = "REPAIR_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_CANDIDATES_V0"
        auth_contract_required = False
    else:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_REVIEWED_AUTHORIZATION_CONTRACT_REQUIRED"
        reason_codes = [
            "PARTIAL_SCHEMA_AWARE_PROPOSAL_BRANCH_REVIEW_COMPLETE",
            "FOUR_PROPOSAL_BRANCH_CANDIDATES_REVIEWED",
            "PROPOSAL_BRANCH_CANDIDATE_INTEGRITY_PASS",
            "PROPOSAL_HOLD_PRESERVED",
            "RESIDUAL_AMBIGUITY_BRANCH_PRESERVED",
            "RESIDUAL_REQUIREMENT_GAP_BRANCH_PRESERVED",
            "AUTHORIZATION_CONTRACT_REQUIRED_BEFORE_ANY_REBIND_APPLICATION",
            "NO_REBINDS_APPLIED",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
        ]
        next_edge = "BUILD_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_V0"
        auth_contract_required = True

    proposal_branch_input_inventory = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_input_inventory_v0",
        "inventory_status": "PROPOSAL_BRANCH_INPUTS_CONSUMED",
        "source_branch_split_review_receipt_id": SOURCE_BRANCH_SPLIT_REVIEW_RECEIPT_ID,
        "source_files": [rel(p) for p in REQUIRED_SOURCE_FILES],
        "proposal_binding_count": proposal_binding_count,
        "ambiguity_binding_count_preserved": ambiguity_binding_count,
        "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
    }

    proposal_candidate_integrity_surface = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_candidate_integrity_surface_v0",
        "integrity_status": "PROPOSAL_BRANCH_CANDIDATE_INTEGRITY_PASS" if not proposal_failures else "PROPOSAL_BRANCH_CANDIDATE_INTEGRITY_FAIL",
        "proposal_candidate_review_pass_count": proposal_candidate_review_pass_count,
        "proposal_candidate_review_fail_count": proposal_candidate_review_fail_count,
        "proposal_failures": proposal_failures,
        "rebinds_applied": False,
    }

    hold_preservation_contract = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_hold_preservation_contract_v0",
        "hold_preservation_status": "PROPOSAL_HOLD_PRESERVED",
        "proposal_binding_count": proposal_binding_count,
        "hold_released": False,
        "release_allowed_now": False,
        "release_requires": [
            "authorization contract review pass",
            "explicit human or validator authorization to apply",
            "residual branch preservation remains true",
            "no broader reusable-schema authority implied",
        ],
        "rebinds_applied": False,
    }

    application_precondition_table = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_application_precondition_table_v0",
        "precondition_status": "APPLICATION_PRECONDITIONS_EMITTED_NOT_SATISFIED",
        "proposal_binding_count": proposal_binding_count,
        "preconditions": [
            {
                "precondition": "proposal_branch_review_pass",
                "satisfied": not bool(proposal_failures) and not bool(failures),
            },
            {
                "precondition": "authorization_contract_built_and_reviewed",
                "satisfied": False,
            },
            {
                "precondition": "explicit_apply_authorization_recorded",
                "satisfied": False,
            },
            {
                "precondition": "proposal_hold_release_authorized",
                "satisfied": False,
            },
            {
                "precondition": "residual_ambiguity_and_requirement_gap_branches_preserved",
                "satisfied": True,
            },
        ],
        "application_ready_now": False,
    }

    authorization_request_packet = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_authorization_request_packet_v0",
        "authorization_request_status": "AUTHORIZATION_CONTRACT_REQUIRED" if auth_contract_required else "AUTHORIZATION_CONTRACT_NOT_READY",
        "proposal_binding_count": proposal_binding_count,
        "proposal_candidate_review_pass_count": proposal_candidate_review_pass_count,
        "requested_next_object": "bounded authorization contract for proposal branch application preconditions",
        "not_a_request_to_apply_now": True,
        "rebinds_applied": False,
    }

    residual_branch_preservation_contract = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_residual_branch_preservation_contract_v0",
        "preservation_status": "RESIDUAL_BRANCHES_PRESERVED",
        "ambiguity_binding_count_preserved": ambiguity_binding_count,
        "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
        "may_discard_residual_branches": False,
        "may_collapse_gap_to_absence": False,
        "may_choose_ambiguity_winner": False,
    }

    downstream_decision_table = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_downstream_decision_table_v0",
        "decision_status": "PROPOSAL_BRANCH_DOWNSTREAM_DECISION_EMITTED",
        "records": [
            {
                "decision": "BUILD_AUTHORIZATION_CONTRACT",
                "selected": auth_contract_required,
                "next_unit": "BUILD_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_V0",
                "why": "proposal branch review passed, but application is still forbidden until bounded authorization contract exists",
            },
            {
                "decision": "APPLY_PROPOSAL_REBINDS",
                "selected": False,
                "next_unit": None,
                "why": "not authorized and hold not released",
            },
            {
                "decision": "DISCARD_RESIDUAL_BRANCHES",
                "selected": False,
                "next_unit": None,
                "why": "22 ambiguity and 498 requirement-gap branches remain preserved",
            },
        ],
    }

    review_packet = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_review_packet_v0",
        "review_packet_status": status,
        "summary": {
            "proposal_binding_count": proposal_binding_count,
            "proposal_candidate_review_pass_count": proposal_candidate_review_pass_count,
            "proposal_candidate_review_fail_count": proposal_candidate_review_fail_count,
            "proposal_hold_released": False,
            "authorization_contract_required": auth_contract_required,
            "ambiguity_binding_count_preserved": ambiguity_binding_count,
            "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
            "rebinds_applied": False,
            "metadata_populated": False,
        },
        "recommended_next": next_edge,
    }

    classification = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "proposal_branch_review_complete": not bool(failures),
        "proposal_branch_review_pass": auth_contract_required,
        "proposal_binding_count": proposal_binding_count,
        "proposal_candidate_review_pass_count": proposal_candidate_review_pass_count,
        "proposal_candidate_review_fail_count": proposal_candidate_review_fail_count,
        "authorization_contract_required": auth_contract_required,
        "proposal_hold_preserved": True,
        "proposal_hold_released": False,
        "ambiguity_binding_count_preserved": ambiguity_binding_count,
        "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
        "schema_overlay_applied_for_this_contract": True,
        "schema_overlay_applied_globally": False,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
        "typing_rule_applied": False,
        "field_policy_modified": False,
        "candidate_artifact_modified": False,
        "source_row_locator_applied": False,
        "rebinds_applied": False,
        "dominance_rule_applied": False,
        "values_authorized": False,
        "values_applied": False,
        "null_reasons_accepted": False,
        "source_packet_materialized_for_review": False,
        "metadata_populated": False,
        "ready_discriminator_count": 0,
        "target_selected_for_build": False,
        "runtime_patch_authorized": False,
        "c5_authorized": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
        "recommended_next": next_edge,
        "next_command_goal": None,
    }

    authority_boundary = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authority_boundary_v0",
        "status": status,
        "may_build_authorization_contract_next": auth_contract_required,
        "may_review_proposal_branch": True,
        "may_release_proposal_hold": False,
        "may_apply_rebinds": False,
        "may_mark_accepted_for_build": False,
        "may_discard_residual_branches": False,
        "may_choose_ambiguous_candidate": False,
        "may_invent_requirement_gap_evidence": False,
        "may_treat_schema_as_reusable": False,
        "may_treat_schema_as_preapproved": False,
        "may_create_validator_registry_entry": False,
        "may_allow_future_automatic_use": False,
        "may_apply_typing_rule": False,
        "may_modify_field_policy": False,
        "may_modify_candidate_artifacts": False,
        "may_authorize_values": False,
        "may_apply_values": False,
        "may_populate_metadata": False,
        "may_select_target_for_build": False,
        "may_apply_runtime_patch": False,
        "may_open_c5": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
    }

    rollup = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "proposal_branch_review_count": 1,
        "proposal_branch_review_pass_count": 1 if auth_contract_required else 0,
        "proposal_binding_count": proposal_binding_count,
        "proposal_candidate_review_pass_count": proposal_candidate_review_pass_count,
        "proposal_candidate_review_fail_count": proposal_candidate_review_fail_count,
        "authorization_contract_required_count": 1 if auth_contract_required else 0,
        "proposal_hold_preserved_count": 1,
        "proposal_hold_released_count": 0,
        "ambiguity_binding_count_preserved": ambiguity_binding_count,
        "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
        "schema_overlay_applied_for_this_contract_count": 1,
        "schema_overlay_applied_globally_count": 0,
        "reusable_schema_authorized_count": 0,
        "preapproved_schema_authorized_count": 0,
        "validator_registry_entry_created_count": 0,
        "future_automatic_use_allowed_count": 0,
        "typing_rule_applied_count": 0,
        "field_policy_modified_count": 0,
        "candidate_artifact_modified_count": 0,
        "source_row_locator_applied_count": 0,
        "rebinds_applied_count": 0,
        "dominance_rule_applied_count": 0,
        "refinements_applied_count": 0,
        "values_authorized_count": 0,
        "values_applied_count": 0,
        "null_reason_accepted_count": 0,
        "source_packet_materialized_for_review_count": 0,
        "metadata_populated_count": 0,
        "ready_discriminator_count": 0,
        "target_selected_for_build_count": 0,
        "accepted_for_build_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "proposal_status_promoted_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "unbounded_payload_inspection_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": next_edge,
    }

    zero_keys = [
        "schema_overlay_applied_globally_count",
        "reusable_schema_authorized_count",
        "preapproved_schema_authorized_count",
        "validator_registry_entry_created_count",
        "future_automatic_use_allowed_count",
        "typing_rule_applied_count",
        "field_policy_modified_count",
        "candidate_artifact_modified_count",
        "source_row_locator_applied_count",
        "rebinds_applied_count",
        "values_authorized_count",
        "values_applied_count",
        "metadata_populated_count",
        "ready_discriminator_count",
        "target_selected_for_build_count",
        "runtime_patch_applied_count",
        "c5_opened_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_profile_v0",
        "profile_id": "partial_schema_aware_proposal_branch_profile_" + sha8(rollup),
        "status": status,
        "proposal_branch_review_complete": not bool(failures),
        "proposal_branch_review_pass": auth_contract_required,
        "proposal_binding_count": proposal_binding_count,
        "authorization_contract_required": auth_contract_required,
        "proposal_hold_preserved": True,
        "proposal_hold_released": False,
        "ambiguity_binding_count_preserved": ambiguity_binding_count,
        "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
        "schema_overlay_applied_for_this_contract": True,
        "schema_overlay_applied_globally": False,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
        "typing_rule_applied": False,
        "field_policy_modified": False,
        "candidate_artifact_modified": False,
        "source_row_locator_applied": False,
        "rebinds_applied": False,
        "values_authorized": False,
        "values_applied": False,
        "metadata_populated": False,
        "ready_discriminator_count": 0,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "c5_opened": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommended_next": next_edge,
        "next_command_goal": None,
    }

    report = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The partial schema-aware proposal branch was reviewed. The 4 proposal candidates passed integrity review, the proposal hold was preserved, and an authorization contract is required before any rebind application. The 22 ambiguity and 498 requirement-gap branches remain preserved.",
        "proposal_binding_count": proposal_binding_count,
        "proposal_candidate_review_pass_count": proposal_candidate_review_pass_count,
        "authorization_contract_required_count": rollup["authorization_contract_required_count"],
        "proposal_hold_released_count": 0,
        "ambiguity_binding_count_preserved": ambiguity_binding_count,
        "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
        "rebinds_applied_count": 0,
        "metadata_populated_count": 0,
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
    }

    trace = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_transition_trace_v0",
        "trace": [
            {
                "step": "consume_proposal_branch",
                "question": "are 4 proposal bindings ready for branch review",
                "answer": "yes" if auth_contract_required else "no",
                "taken": "review proposal candidates",
            },
            {
                "step": "preserve_hold",
                "question": "can proposal hold be released now",
                "answer": "no",
                "taken": "emit hold preservation contract",
            },
            {
                "step": "select_next_object",
                "question": "what is required before application",
                "answer": "bounded authorization contract",
                "taken": next_edge,
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    review_assessment = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_review_assessment_v0",
        "assessment_status": status,
        "source_branch_split_review_receipt_id": SOURCE_BRANCH_SPLIT_REVIEW_RECEIPT_ID,
        "proposal_binding_count": proposal_binding_count,
        "proposal_candidate_review_pass_count": proposal_candidate_review_pass_count,
        "proposal_candidate_review_fail_count": proposal_candidate_review_fail_count,
        "authorization_contract_required": auth_contract_required,
        "recommended_next": next_edge,
    }

    write_json(REVIEW_ASSESSMENT_PATH, review_assessment)
    write_json(PROPOSAL_BRANCH_INPUT_INVENTORY_PATH, proposal_branch_input_inventory)
    write_json(PROPOSAL_CANDIDATE_REVIEW_TABLE_PATH, {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_candidate_review_table_v0",
        "candidate_review_table_status": "PROPOSAL_BRANCH_CANDIDATE_REVIEW_TABLE_EMITTED",
        "proposal_binding_count": proposal_binding_count,
        "proposal_candidate_review_pass_count": proposal_candidate_review_pass_count,
        "proposal_candidate_review_fail_count": proposal_candidate_review_fail_count,
        "records": proposal_rows,
    })
    write_json(PROPOSAL_CANDIDATE_INTEGRITY_SURFACE_PATH, proposal_candidate_integrity_surface)
    write_json(PROPOSAL_HOLD_PRESERVATION_CONTRACT_PATH, hold_preservation_contract)
    write_json(PROPOSAL_APPLICATION_PRECONDITION_TABLE_PATH, application_precondition_table)
    write_json(PROPOSAL_AUTHORIZATION_REQUEST_PACKET_PATH, authorization_request_packet)
    write_json(RESIDUAL_BRANCH_PRESERVATION_CONTRACT_PATH, residual_branch_preservation_contract)
    write_json(DOWNSTREAM_DECISION_TABLE_PATH, downstream_decision_table)
    write_json(REVIEW_PACKET_PATH, review_packet)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(AUTHORITY_BOUNDARY_PATH, authority_boundary)
    write_json(ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, profile)
    write_json(REPORT_PATH, report)
    write_json(TRANSITION_TRACE_PATH, trace)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        rollup["source_mutation_count"] = 1
        report["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup)
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "PROPOSAL_BRANCH_REVIEW_0_SOURCE_RECEIPT_CONSUMED": SOURCE_BRANCH_SPLIT_REVIEW_RECEIPT_PATH.exists(),
        "PROPOSAL_BRANCH_REVIEW_1_PROPOSAL_TABLE_CONSUMED": SOURCE_PARTIAL_PROPOSAL_REVIEW_TABLE_PATH.exists(),
        "PROPOSAL_BRANCH_REVIEW_2_FOUR_PROPOSAL_BINDINGS_REVIEWED": proposal_binding_count == 4,
        "PROPOSAL_BRANCH_REVIEW_3_PROPOSAL_CANDIDATE_INTEGRITY_PASS": proposal_candidate_review_fail_count == 0,
        "PROPOSAL_BRANCH_REVIEW_4_PROPOSAL_HOLD_PRESERVED": hold_preservation_contract["hold_released"] is False,
        "PROPOSAL_BRANCH_REVIEW_5_AUTHORIZATION_CONTRACT_REQUIRED": auth_contract_required,
        "PROPOSAL_BRANCH_REVIEW_6_RESIDUAL_AMBIGUITY_BRANCH_PRESERVED": ambiguity_binding_count == 22,
        "PROPOSAL_BRANCH_REVIEW_7_RESIDUAL_REQUIREMENT_GAP_BRANCH_PRESERVED": requirement_gap_binding_count == 498,
        "PROPOSAL_BRANCH_REVIEW_8_NO_HOLD_RELEASE": rollup["proposal_hold_released_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_9_NO_GLOBAL_SCHEMA_APPLICATION": rollup["schema_overlay_applied_globally_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_10_NO_REUSABLE_SCHEMA_AUTHORIZED": rollup["reusable_schema_authorized_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_11_NO_PREAPPROVED_SCHEMA_AUTHORIZED": rollup["preapproved_schema_authorized_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_12_NO_VALIDATOR_REGISTRY_ENTRY": rollup["validator_registry_entry_created_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_13_NO_FUTURE_AUTOMATIC_USE": rollup["future_automatic_use_allowed_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_14_NO_TYPING_RULE_APPLIED": rollup["typing_rule_applied_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_15_NO_FIELD_POLICY_MODIFIED": rollup["field_policy_modified_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_16_NO_CANDIDATE_ARTIFACT_MODIFIED": rollup["candidate_artifact_modified_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_17_NO_ROW_LOCATOR_APPLIED": rollup["source_row_locator_applied_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_18_NO_REBINDS_APPLIED": rollup["rebinds_applied_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_19_NO_VALUES_AUTHORIZED": rollup["values_authorized_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_20_NO_VALUES_APPLIED": rollup["values_applied_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_21_NO_METADATA_POPULATION": rollup["metadata_populated_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_22_NO_DISCRIMINATOR_READY": rollup["ready_discriminator_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_23_NO_TARGET_SELECTED": rollup["target_selected_for_build_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_24_NO_RUNTIME_PATCH": rollup["runtime_patch_applied_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_25_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_26_NO_LATEST_FILE_GUESSING": rollup["latest_file_guessing_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_27_NO_MTIME_SELECTION": rollup["mtime_selection_count"] == 0,
        "PROPOSAL_BRANCH_REVIEW_28_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "PROPOSAL_BRANCH_REVIEW_29_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "accepted_schema_overlay_reference_this_application_contract_only",
        "PROPOSAL_BRANCH_REVIEW_30_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "proposal": proposal_binding_count,
        "proposal_pass": proposal_candidate_review_pass_count,
        "hold": "preserved",
        "auth": auth_contract_required,
        "rebinds": 0,
        "metadata": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_branch_split_review_receipt_id": SOURCE_BRANCH_SPLIT_REVIEW_RECEIPT_ID,
        "machine_readable_partial_schema_aware_rebind_proposal_branch_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "proposal_branch_review_complete": not bool(failures),
            "proposal_branch_review_pass": auth_contract_required,
            "proposal_binding_count": proposal_binding_count,
            "proposal_candidate_review_pass_count": proposal_candidate_review_pass_count,
            "proposal_candidate_review_fail_count": proposal_candidate_review_fail_count,
            "authorization_contract_required": auth_contract_required,
            "proposal_hold_preserved": True,
            "proposal_hold_released": False,
            "ambiguity_binding_count_preserved": ambiguity_binding_count,
            "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
            "schema_overlay_applied_for_this_contract": True,
            "schema_overlay_applied_globally": False,
            "reusable_schema_authorized": False,
            "preapproved_schema_authorized": False,
            "validator_registry_entry_created": False,
            "future_automatic_use_allowed": False,
            "typing_rule_applied": False,
            "field_policy_modified": False,
            "candidate_artifact_modified": False,
            "source_row_locator_applied": False,
            "rebinds_applied": False,
            "dominance_rule_applied": False,
            "values_authorized": False,
            "values_applied": False,
            "null_reasons_accepted": False,
            "source_packet_materialized_for_review": False,
            "metadata_populated": False,
            "ready_discriminator_count": 0,
            "target_selected_for_build": False,
            "runtime_patch_applied": False,
            "c5_opened": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
            "bad_counters_zero": profile["bad_counters_zero"],
            "recommended_next": next_edge,
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "review_assessment": rel(REVIEW_ASSESSMENT_PATH),
            "proposal_branch_input_inventory": rel(PROPOSAL_BRANCH_INPUT_INVENTORY_PATH),
            "proposal_candidate_review_table": rel(PROPOSAL_CANDIDATE_REVIEW_TABLE_PATH),
            "proposal_candidate_integrity_surface": rel(PROPOSAL_CANDIDATE_INTEGRITY_SURFACE_PATH),
            "proposal_hold_preservation_contract": rel(PROPOSAL_HOLD_PRESERVATION_CONTRACT_PATH),
            "proposal_application_precondition_table": rel(PROPOSAL_APPLICATION_PRECONDITION_TABLE_PATH),
            "proposal_authorization_request_packet": rel(PROPOSAL_AUTHORIZATION_REQUEST_PACKET_PATH),
            "residual_branch_preservation_contract": rel(RESIDUAL_BRANCH_PRESERVATION_CONTRACT_PATH),
            "downstream_decision_table": rel(DOWNSTREAM_DECISION_TABLE_PATH),
            "review_packet": rel(REVIEW_PACKET_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"partial_schema_aware_proposal_branch_receipt_id={receipt_id}")
    print(f"partial_schema_aware_proposal_branch_receipt_path={rel(receipt_path)}")
    print(f"partial_schema_aware_proposal_branch_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"partial_schema_aware_proposal_candidate_review_table_path={rel(PROPOSAL_CANDIDATE_REVIEW_TABLE_PATH)}")
    print(f"partial_schema_aware_proposal_candidate_integrity_surface_path={rel(PROPOSAL_CANDIDATE_INTEGRITY_SURFACE_PATH)}")
    print(f"partial_schema_aware_proposal_hold_preservation_contract_path={rel(PROPOSAL_HOLD_PRESERVATION_CONTRACT_PATH)}")
    print(f"partial_schema_aware_proposal_application_precondition_table_path={rel(PROPOSAL_APPLICATION_PRECONDITION_TABLE_PATH)}")
    print(f"partial_schema_aware_proposal_authorization_request_packet_path={rel(PROPOSAL_AUTHORIZATION_REQUEST_PACKET_PATH)}")
    print(f"partial_schema_aware_residual_branch_preservation_contract_path={rel(RESIDUAL_BRANCH_PRESERVATION_CONTRACT_PATH)}")
    print(f"partial_schema_aware_proposal_branch_rollup_path={rel(ROLLUP_PATH)}")
    print(f"partial_schema_aware_proposal_branch_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
