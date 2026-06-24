#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_AND_REPAIR_SURFACE_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_review.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_REVIEW"
MODE = "BRANCH_SPLIT_REVIEW / ROUTING_OBJECT_VERIFICATION / NEXT_BRANCH_SELECTION / NO_REBIND_APPLICATION"
BUILD_MODE = "PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_REVIEW_ONLY"

SOURCE_BRANCH_SPLIT_RECEIPT_ID = "2f90e521"
SOURCE_BRANCH_SPLIT_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0_receipts/2f90e521.json"
SOURCE_BRANCH_SPLIT_ROUTING_OBJECT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0/typed_machine_readable_partial_schema_aware_rebind_branch_split_routing_object_v0.json"
SOURCE_PROPOSAL_BRANCH_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_contract_v0.json"
SOURCE_PROPOSAL_BRANCH_HOLD_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_hold_packet_v0.json"
SOURCE_AMBIGUITY_BRANCH_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0/typed_machine_readable_partial_schema_aware_rebind_ambiguity_branch_contract_v0.json"
SOURCE_AMBIGUITY_TIE_BREAKER_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0/typed_machine_readable_partial_schema_aware_rebind_ambiguity_tie_breaker_evidence_surface_v0.json"
SOURCE_REQUIREMENT_GAP_BRANCH_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0/typed_machine_readable_partial_schema_aware_rebind_requirement_gap_branch_contract_v0.json"
SOURCE_REQUIREMENT_GAP_EVIDENCE_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0/typed_machine_readable_partial_schema_aware_rebind_requirement_gap_evidence_surface_v0.json"
SOURCE_BRANCH_PRECONDITION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0/typed_machine_readable_partial_schema_aware_rebind_branch_precondition_table_v0.json"
SOURCE_BRANCH_FORBIDDEN_ACTION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0/typed_machine_readable_partial_schema_aware_rebind_branch_forbidden_action_table_v0.json"
SOURCE_BRANCH_PRIORITY_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0/typed_machine_readable_partial_schema_aware_rebind_branch_priority_table_v0.json"
SOURCE_BRANCH_DECISION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0/typed_machine_readable_partial_schema_aware_rebind_branch_decision_table_v0.json"
SOURCE_REVIEW_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0/typed_machine_readable_partial_schema_aware_rebind_branch_split_review_packet_v0.json"
SOURCE_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0/typed_machine_readable_partial_schema_aware_rebind_branch_split_classification_v0.json"
SOURCE_AUTHORITY_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0/typed_machine_readable_partial_schema_aware_rebind_branch_split_authority_boundary_v0.json"
SOURCE_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0/typed_machine_readable_partial_schema_aware_rebind_branch_split_rollup_v0.json"
SOURCE_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0/typed_machine_readable_partial_schema_aware_rebind_branch_split_profile_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_review_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_assessment_v0.json"
ROUTING_OBJECT_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_routing_object_review_v0.json"
PROPOSAL_BRANCH_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_contract_review_v0.json"
PROPOSAL_HOLD_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_hold_review_v0.json"
AMBIGUITY_BRANCH_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_ambiguity_branch_contract_review_v0.json"
AMBIGUITY_EVIDENCE_SURFACE_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_ambiguity_evidence_surface_review_v0.json"
REQUIREMENT_GAP_BRANCH_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_requirement_gap_branch_contract_review_v0.json"
REQUIREMENT_GAP_EVIDENCE_SURFACE_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_requirement_gap_evidence_surface_review_v0.json"
BRANCH_PRECONDITION_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_precondition_review_v0.json"
BRANCH_FORBIDDEN_ACTION_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_forbidden_action_review_v0.json"
BRANCH_EXECUTION_READINESS_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_execution_readiness_table_v0.json"
NEXT_BRANCH_DECISION_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_next_branch_decision_table_v0.json"
REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_result_packet_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_BRANCH_SPLIT_RECEIPT_PATH,
    SOURCE_BRANCH_SPLIT_ROUTING_OBJECT_PATH,
    SOURCE_PROPOSAL_BRANCH_CONTRACT_PATH,
    SOURCE_PROPOSAL_BRANCH_HOLD_PACKET_PATH,
    SOURCE_AMBIGUITY_BRANCH_CONTRACT_PATH,
    SOURCE_AMBIGUITY_TIE_BREAKER_SURFACE_PATH,
    SOURCE_REQUIREMENT_GAP_BRANCH_CONTRACT_PATH,
    SOURCE_REQUIREMENT_GAP_EVIDENCE_SURFACE_PATH,
    SOURCE_BRANCH_PRECONDITION_TABLE_PATH,
    SOURCE_BRANCH_FORBIDDEN_ACTION_TABLE_PATH,
    SOURCE_BRANCH_PRIORITY_TABLE_PATH,
    SOURCE_BRANCH_DECISION_TABLE_PATH,
    SOURCE_REVIEW_PACKET_PATH,
    SOURCE_CLASSIFICATION_PATH,
    SOURCE_AUTHORITY_BOUNDARY_PATH,
    SOURCE_ROLLUP_PATH,
    SOURCE_PROFILE_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_AND_REPAIR_SURFACE_BUILT_REVIEW_REQUIRED"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_AND_REPAIR_SURFACE_BUILT_REVIEW_REQUIRED"
EXPECTED_SOURCE_NEXT = "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_AND_REPAIR_SURFACE_V0"

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

def review_bool(name: str, value: bool, expected: bool = True) -> Dict[str, Any]:
    return {"check": name, "observed": value, "expected": expected, "pass": value is expected}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    receipt = read_json(SOURCE_BRANCH_SPLIT_RECEIPT_PATH)
    summary = receipt.get("machine_readable_partial_schema_aware_rebind_branch_split_summary", {})
    routing = read_json(SOURCE_BRANCH_SPLIT_ROUTING_OBJECT_PATH)
    proposal_contract = read_json(SOURCE_PROPOSAL_BRANCH_CONTRACT_PATH)
    proposal_hold = read_json(SOURCE_PROPOSAL_BRANCH_HOLD_PACKET_PATH)
    ambiguity_contract = read_json(SOURCE_AMBIGUITY_BRANCH_CONTRACT_PATH)
    ambiguity_surface = read_json(SOURCE_AMBIGUITY_TIE_BREAKER_SURFACE_PATH)
    gap_contract = read_json(SOURCE_REQUIREMENT_GAP_BRANCH_CONTRACT_PATH)
    gap_surface = read_json(SOURCE_REQUIREMENT_GAP_EVIDENCE_SURFACE_PATH)
    preconditions = read_json(SOURCE_BRANCH_PRECONDITION_TABLE_PATH)
    forbidden = read_json(SOURCE_BRANCH_FORBIDDEN_ACTION_TABLE_PATH)
    priority = read_json(SOURCE_BRANCH_PRIORITY_TABLE_PATH)
    decision = read_json(SOURCE_BRANCH_DECISION_TABLE_PATH)
    classif = read_json(SOURCE_CLASSIFICATION_PATH)
    authority = read_json(SOURCE_AUTHORITY_BOUNDARY_PATH)
    rollup = read_json(SOURCE_ROLLUP_PATH)
    profile = read_json(SOURCE_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_BRANCH_SPLIT_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_branch_split_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_next_not_expected:{summary.get('recommended_next')}")

    for key in [
        "branch_split_surface_built",
        "branch_split_review_required",
        "proposal_branch_contract_emitted",
        "proposal_branch_hold_packet_emitted",
        "ambiguity_branch_contract_emitted",
        "ambiguity_tie_breaker_evidence_surface_emitted",
        "requirement_gap_branch_contract_emitted",
        "requirement_gap_evidence_surface_emitted",
        "schema_overlay_applied_for_this_contract",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "proposal_binding_count": 4,
        "ambiguity_binding_count": 22,
        "requirement_gap_binding_count": 498,
        "total_routed_binding_count": 524,
        "ready_discriminator_count": 0,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"summary_count_wrong:{key}:{summary.get(key)}")

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
            failures.append(f"summary_forbidden_true:{key}")

    if routing.get("routing_status") != "BRANCH_SPLIT_ROUTING_OBJECT_BUILT_REVIEW_REQUIRED":
        failures.append("routing_status_wrong")
    if routing.get("total_routed_binding_count") != 524:
        failures.append("routing_total_count_wrong")
    if proposal_contract.get("contract_status") != "PROPOSAL_BRANCH_CONTRACT_BUILT_REVIEW_REQUIRED":
        failures.append("proposal_contract_status_wrong")
    if proposal_contract.get("proposal_binding_count") != 4:
        failures.append("proposal_contract_count_wrong")
    if proposal_contract.get("may_apply_rebinds") is not False:
        failures.append("proposal_contract_allows_rebinds")
    if proposal_hold.get("hold_status") != "PROPOSALS_HELD_PENDING_BRANCH_SPLIT_REVIEW":
        failures.append("proposal_hold_status_wrong")
    if proposal_hold.get("released_now") is not False:
        failures.append("proposal_hold_released")
    if ambiguity_contract.get("contract_status") != "AMBIGUITY_BRANCH_CONTRACT_BUILT_REVIEW_REQUIRED":
        failures.append("ambiguity_contract_status_wrong")
    if ambiguity_contract.get("ambiguous_binding_count") != 22:
        failures.append("ambiguity_contract_count_wrong")
    if ambiguity_contract.get("may_choose_candidate_now") is not False:
        failures.append("ambiguity_contract_allows_candidate_choice")
    if ambiguity_surface.get("surface_status") != "AMBIGUITY_TIE_BREAKER_EVIDENCE_SURFACE_BUILT_REVIEW_REQUIRED":
        failures.append("ambiguity_surface_status_wrong")
    if ambiguity_surface.get("selected_candidate_count") != 0:
        failures.append("ambiguity_surface_selected_candidate_nonzero")
    if gap_contract.get("contract_status") != "REQUIREMENT_GAP_BRANCH_CONTRACT_BUILT_REVIEW_REQUIRED":
        failures.append("gap_contract_status_wrong")
    if gap_contract.get("requirement_gap_binding_count") != 498:
        failures.append("gap_contract_count_wrong")
    if gap_contract.get("may_invent_missing_evidence") is not False:
        failures.append("gap_contract_allows_invented_evidence")
    if gap_surface.get("surface_status") != "REQUIREMENT_GAP_EVIDENCE_SURFACE_BUILT_REVIEW_REQUIRED":
        failures.append("gap_surface_status_wrong")
    if gap_surface.get("metadata_populated") is not False:
        failures.append("gap_surface_metadata_populated")
    if preconditions.get("precondition_status") != "BRANCH_PRECONDITIONS_EMITTED":
        failures.append("preconditions_status_wrong")
    if forbidden.get("forbidden_action_status") != "FORBIDDEN_ACTIONS_REAFFIRMED":
        failures.append("forbidden_actions_status_wrong")
    if "apply rebinds" not in forbidden.get("forbidden_actions", []):
        failures.append("forbidden_actions_missing_apply_rebinds")
    if priority.get("priority_status") != "BRANCH_PRIORITY_EMITTED_REVIEW_REQUIRED":
        failures.append("priority_status_wrong")
    if decision.get("decision_status") != "BRANCH_SPLIT_DECISION_TABLE_EMITTED":
        failures.append("decision_table_status_wrong")
    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("classification_status_wrong")
    if authority.get("may_review_branch_split_surface") is not True:
        failures.append("authority_cannot_review_branch_split")
    if authority.get("may_apply_rebinds") is not False:
        failures.append("authority_allows_rebinds")
    if rollup.get("branch_split_surface_built_count") != 1:
        failures.append("rollup_branch_split_count_wrong")
    if rollup.get("rebinds_applied_count") != 0:
        failures.append("rollup_rebinds_nonzero")
    if profile.get("branch_split_surface_built") is not True:
        failures.append("profile_branch_split_not_built")
    if profile.get("rebinds_applied") is not False:
        failures.append("profile_rebinds_true")

    return failures, {
        "summary": summary,
        "routing": routing,
        "proposal_contract": proposal_contract,
        "proposal_hold": proposal_hold,
        "ambiguity_contract": ambiguity_contract,
        "ambiguity_surface": ambiguity_surface,
        "gap_contract": gap_contract,
        "gap_surface": gap_surface,
        "preconditions": preconditions,
        "forbidden": forbidden,
        "priority": priority,
        "decision": decision,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    summary = src.get("summary", {})
    routing = src.get("routing", {})
    proposal_contract = src.get("proposal_contract", {})
    proposal_hold = src.get("proposal_hold", {})
    ambiguity_contract = src.get("ambiguity_contract", {})
    ambiguity_surface = src.get("ambiguity_surface", {})
    gap_contract = src.get("gap_contract", {})
    gap_surface = src.get("gap_surface", {})
    preconditions = src.get("preconditions", {})
    forbidden = src.get("forbidden", {})

    proposal_binding_count = int(summary.get("proposal_binding_count", 0) or 0)
    ambiguity_binding_count = int(summary.get("ambiguity_binding_count", 0) or 0)
    requirement_gap_binding_count = int(summary.get("requirement_gap_binding_count", 0) or 0)
    total_routed_binding_count = int(summary.get("total_routed_binding_count", 0) or 0)

    review_checks = [
        review_bool("routing_object_built", routing.get("routing_status") == "BRANCH_SPLIT_ROUTING_OBJECT_BUILT_REVIEW_REQUIRED"),
        review_bool("total_routed_binding_count_524", routing.get("total_routed_binding_count") == 524),
        review_bool("proposal_branch_count_4", proposal_contract.get("proposal_binding_count") == 4),
        review_bool("proposal_hold_not_released", proposal_hold.get("released_now") is False),
        review_bool("ambiguity_branch_count_22", ambiguity_contract.get("ambiguous_binding_count") == 22),
        review_bool("ambiguity_no_selected_candidates", ambiguity_surface.get("selected_candidate_count") == 0),
        review_bool("requirement_gap_branch_count_498", gap_contract.get("requirement_gap_binding_count") == 498),
        review_bool("requirement_gap_no_metadata", gap_surface.get("metadata_populated") is False),
        review_bool("forbidden_actions_include_apply_rebinds", "apply rebinds" in forbidden.get("forbidden_actions", [])),
    ]

    review_failures = [c["check"] for c in review_checks if not c["pass"]]

    if failures:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_REVIEW_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_REVIEW_BASIS_V0"
        review_pass = False
    elif review_failures:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_REVIEWED_REPAIR_REQUIRED"
        reason_codes = [
            "PARTIAL_SCHEMA_AWARE_BRANCH_SPLIT_REVIEW_COMPLETE",
            "BRANCH_SPLIT_REVIEW_FAILURES_FOUND",
            "NO_BRANCH_EXECUTION_AUTHORIZED",
            "NO_REBINDS_APPLIED",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
        ] + review_failures
        next_edge = "REPAIR_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_AND_REPAIR_SURFACE_V0"
        review_pass = False
    else:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_REVIEWED_PROPOSAL_BRANCH_REVIEW_READY"
        reason_codes = [
            "PARTIAL_SCHEMA_AWARE_BRANCH_SPLIT_REVIEW_COMPLETE",
            "ROUTING_OBJECT_REVIEW_PASS",
            "PROPOSAL_BRANCH_CONTRACT_REVIEW_PASS",
            "PROPOSAL_HOLD_REVIEW_PASS",
            "AMBIGUITY_BRANCH_CONTRACT_REVIEW_PASS",
            "AMBIGUITY_TIE_BREAKER_EVIDENCE_SURFACE_REVIEW_PASS",
            "REQUIREMENT_GAP_BRANCH_CONTRACT_REVIEW_PASS",
            "REQUIREMENT_GAP_EVIDENCE_SURFACE_REVIEW_PASS",
            "BRANCH_FORBIDDEN_ACTIONS_REVIEW_PASS",
            "PROPOSAL_BRANCH_REVIEW_READY",
            "NO_REBINDS_APPLIED",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
        ]
        next_edge = "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_V0"
        review_pass = True

    routing_object_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_routing_object_review_v0",
        "review_status": "ROUTING_OBJECT_REVIEW_PASS" if review_pass else "ROUTING_OBJECT_REVIEW_REPAIR_REQUIRED",
        "checks": review_checks,
        "proposal_binding_count": proposal_binding_count,
        "ambiguity_binding_count": ambiguity_binding_count,
        "requirement_gap_binding_count": requirement_gap_binding_count,
        "total_routed_binding_count": total_routed_binding_count,
        "review_failures": review_failures,
    }

    proposal_branch_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_contract_review_v0",
        "review_status": "PROPOSAL_BRANCH_CONTRACT_REVIEW_PASS" if review_pass else "PROPOSAL_BRANCH_CONTRACT_REVIEW_REPAIR_REQUIRED",
        "proposal_binding_count": proposal_binding_count,
        "proposal_review_ready": review_pass,
        "proposal_application_ready": False,
        "release_hold_now": False,
        "next_allowed_action": "review proposal branch only" if review_pass else "repair proposal branch contract",
    }

    proposal_hold_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_hold_review_v0",
        "review_status": "PROPOSAL_HOLD_REVIEW_PASS" if proposal_hold.get("released_now") is False else "PROPOSAL_HOLD_REVIEW_FAIL",
        "proposal_hold_preserved": proposal_hold.get("released_now") is False,
        "proposal_ready_count": proposal_binding_count,
        "release_requires": proposal_hold.get("release_requires", []),
        "released_now": False,
        "rebinds_applied": False,
    }

    ambiguity_branch_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_ambiguity_branch_contract_review_v0",
        "review_status": "AMBIGUITY_BRANCH_CONTRACT_REVIEW_PASS" if review_pass else "AMBIGUITY_BRANCH_CONTRACT_REVIEW_REPAIR_REQUIRED",
        "ambiguous_binding_count": ambiguity_binding_count,
        "tie_breaker_surface_ready_for_later_review": review_pass,
        "selected_candidate_count": 0,
        "rebinds_applied": False,
    }

    ambiguity_evidence_surface_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_ambiguity_evidence_surface_review_v0",
        "review_status": "AMBIGUITY_TIE_BREAKER_EVIDENCE_SURFACE_REVIEW_PASS" if review_pass else "AMBIGUITY_TIE_BREAKER_EVIDENCE_SURFACE_REVIEW_REPAIR_REQUIRED",
        "evidence_surface_exists": bool(ambiguity_surface),
        "evidence_requirement_count": len(ambiguity_surface.get("evidence_requirements", [])) if isinstance(ambiguity_surface, dict) else 0,
        "selected_candidate_count": ambiguity_surface.get("selected_candidate_count", 0),
        "may_choose_candidate_now": False,
    }

    requirement_gap_branch_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_requirement_gap_branch_contract_review_v0",
        "review_status": "REQUIREMENT_GAP_BRANCH_CONTRACT_REVIEW_PASS" if review_pass else "REQUIREMENT_GAP_BRANCH_CONTRACT_REVIEW_REPAIR_REQUIRED",
        "requirement_gap_binding_count": requirement_gap_binding_count,
        "missing_evidence_surface_ready_for_later_review": review_pass,
        "may_invent_missing_evidence": False,
        "metadata_populated": False,
    }

    requirement_gap_evidence_surface_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_requirement_gap_evidence_surface_review_v0",
        "review_status": "REQUIREMENT_GAP_EVIDENCE_SURFACE_REVIEW_PASS" if review_pass else "REQUIREMENT_GAP_EVIDENCE_SURFACE_REVIEW_REPAIR_REQUIRED",
        "evidence_surface_exists": bool(gap_surface),
        "required_evidence_class_count": len(gap_surface.get("required_evidence_classes", [])) if isinstance(gap_surface, dict) else 0,
        "evidence_materialized_now": gap_surface.get("evidence_materialized_now", False),
        "metadata_populated": gap_surface.get("metadata_populated", False),
    }

    branch_precondition_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_precondition_review_v0",
        "review_status": "BRANCH_PRECONDITION_REVIEW_PASS" if preconditions.get("precondition_status") == "BRANCH_PRECONDITIONS_EMITTED" else "BRANCH_PRECONDITION_REVIEW_REPAIR_REQUIRED",
        "precondition_record_count": len(preconditions.get("records", [])) if isinstance(preconditions.get("records"), list) else 0,
        "branch_split_review_passed": review_pass,
    }

    branch_forbidden_action_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_forbidden_action_review_v0",
        "review_status": "BRANCH_FORBIDDEN_ACTION_REVIEW_PASS" if "apply rebinds" in forbidden.get("forbidden_actions", []) else "BRANCH_FORBIDDEN_ACTION_REVIEW_REPAIR_REQUIRED",
        "forbidden_action_count": len(forbidden.get("forbidden_actions", [])) if isinstance(forbidden.get("forbidden_actions"), list) else 0,
        "apply_rebinds_forbidden": "apply rebinds" in forbidden.get("forbidden_actions", []),
        "populate_metadata_forbidden": "populate metadata" in forbidden.get("forbidden_actions", []),
        "open_c5_forbidden": "open C5" in forbidden.get("forbidden_actions", []),
    }

    branch_execution_readiness_table = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_execution_readiness_table_v0",
        "readiness_status": "BRANCH_EXECUTION_READINESS_EMITTED",
        "records": [
            {
                "branch_id": "proposal_review_branch",
                "ready_for_review": review_pass,
                "ready_for_application": False,
                "binding_count": proposal_binding_count,
                "next_unit": "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_V0" if review_pass else None,
            },
            {
                "branch_id": "ambiguity_tie_breaker_repair_branch",
                "ready_for_review": review_pass,
                "ready_for_application": False,
                "binding_count": ambiguity_binding_count,
                "next_unit": "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_AMBIGUITY_TIE_BREAKER_EVIDENCE_SURFACE_V0" if review_pass else None,
            },
            {
                "branch_id": "requirement_gap_repair_branch",
                "ready_for_review": review_pass,
                "ready_for_application": False,
                "binding_count": requirement_gap_binding_count,
                "next_unit": "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_REQUIREMENT_GAP_EVIDENCE_SURFACE_V0" if review_pass else None,
            },
        ],
    }

    next_branch_decision_table = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_next_branch_decision_table_v0",
        "decision_status": "NEXT_BRANCH_DECISION_EMITTED",
        "records": [
            {
                "decision": "REVIEW_PROPOSAL_BRANCH",
                "selected": review_pass,
                "next_unit": "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_V0",
                "why": "branch split passed review and proposal branch is the smallest held review branch",
            },
            {
                "decision": "REVIEW_AMBIGUITY_BRANCH",
                "selected": False,
                "next_unit": "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_AMBIGUITY_TIE_BREAKER_EVIDENCE_SURFACE_V0",
                "why": "kept for later; 22 bindings require tie-breaker evidence review",
            },
            {
                "decision": "REVIEW_REQUIREMENT_GAP_BRANCH",
                "selected": False,
                "next_unit": "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_REQUIREMENT_GAP_EVIDENCE_SURFACE_V0",
                "why": "kept for later; 498 bindings require missing-evidence repair review",
            },
            {
                "decision": "APPLY_REBINDS",
                "selected": False,
                "next_unit": None,
                "why": "not authorized",
            },
        ],
    }

    review_packet = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_result_packet_v0",
        "review_packet_status": status,
        "summary": {
            "branch_split_review_pass": review_pass,
            "proposal_binding_count": proposal_binding_count,
            "ambiguity_binding_count": ambiguity_binding_count,
            "requirement_gap_binding_count": requirement_gap_binding_count,
            "total_routed_binding_count": total_routed_binding_count,
            "selected_next_branch": "proposal_review_branch" if review_pass else None,
            "rebinds_applied": False,
            "metadata_populated": False,
        },
        "recommended_next": next_edge,
    }

    classification = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "branch_split_review_complete": not bool(failures),
        "branch_split_review_pass": review_pass,
        "proposal_branch_review_ready": review_pass,
        "ambiguity_branch_review_ready_later": review_pass,
        "requirement_gap_branch_review_ready_later": review_pass,
        "selected_next_branch": "proposal_review_branch" if review_pass else None,
        "proposal_binding_count": proposal_binding_count,
        "ambiguity_binding_count": ambiguity_binding_count,
        "requirement_gap_binding_count": requirement_gap_binding_count,
        "total_routed_binding_count": total_routed_binding_count,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_authority_boundary_v0",
        "status": status,
        "may_review_proposal_branch_next": review_pass,
        "may_review_ambiguity_branch_later": review_pass,
        "may_review_requirement_gap_branch_later": review_pass,
        "may_release_proposal_hold": False,
        "may_apply_rebinds": False,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "branch_split_review_count": 1,
        "branch_split_review_pass_count": 1 if review_pass else 0,
        "proposal_branch_review_ready_count": 1 if review_pass else 0,
        "ambiguity_branch_review_ready_later_count": 1 if review_pass else 0,
        "requirement_gap_branch_review_ready_later_count": 1 if review_pass else 0,
        "proposal_binding_count": proposal_binding_count,
        "ambiguity_binding_count": ambiguity_binding_count,
        "requirement_gap_binding_count": requirement_gap_binding_count,
        "total_routed_binding_count": total_routed_binding_count,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_profile_v0",
        "profile_id": "partial_schema_aware_branch_split_review_profile_" + sha8(rollup),
        "status": status,
        "branch_split_review_complete": not bool(failures),
        "branch_split_review_pass": review_pass,
        "proposal_branch_review_ready": review_pass,
        "selected_next_branch": "proposal_review_branch" if review_pass else None,
        "proposal_binding_count": proposal_binding_count,
        "ambiguity_binding_count": ambiguity_binding_count,
        "requirement_gap_binding_count": requirement_gap_binding_count,
        "total_routed_binding_count": total_routed_binding_count,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The partial schema-aware rebind branch split was reviewed and passed as a routing object. The next lawful step is proposal-branch review only. This unit does not release proposal hold, apply rebinds, choose ambiguity winners, invent evidence, populate metadata, authorize values, select targets, patch runtime, open C5, or promote schema authority.",
        "proposal_binding_count": proposal_binding_count,
        "ambiguity_binding_count": ambiguity_binding_count,
        "requirement_gap_binding_count": requirement_gap_binding_count,
        "total_routed_binding_count": total_routed_binding_count,
        "rebinds_applied_count": 0,
        "metadata_populated_count": 0,
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
    }

    trace = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_branch_split",
                "question": "does routing object preserve 4/22/498 split",
                "answer": "yes" if review_pass else "no",
                "taken": "review branch contracts and forbidden actions",
            },
            {
                "step": "review_forbidden_boundary",
                "question": "did any branch authorize rebind application",
                "answer": "no",
                "taken": "preserve proposal hold and no-application boundary",
            },
            {
                "step": "select_next_branch",
                "question": "which branch is smallest lawful next review",
                "answer": "proposal_review_branch" if review_pass else "repair_branch_split",
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_assessment_v0",
        "assessment_status": status,
        "source_branch_split_receipt_id": SOURCE_BRANCH_SPLIT_RECEIPT_ID,
        "review_failure_count": len(review_failures),
        "branch_split_review_pass": review_pass,
        "proposal_branch_review_ready": review_pass,
        "selected_next_branch": "proposal_review_branch" if review_pass else None,
        "recommended_next": next_edge,
    }

    write_json(REVIEW_ASSESSMENT_PATH, review_assessment)
    write_json(ROUTING_OBJECT_REVIEW_PATH, routing_object_review)
    write_json(PROPOSAL_BRANCH_REVIEW_PATH, proposal_branch_review)
    write_json(PROPOSAL_HOLD_REVIEW_PATH, proposal_hold_review)
    write_json(AMBIGUITY_BRANCH_REVIEW_PATH, ambiguity_branch_review)
    write_json(AMBIGUITY_EVIDENCE_SURFACE_REVIEW_PATH, ambiguity_evidence_surface_review)
    write_json(REQUIREMENT_GAP_BRANCH_REVIEW_PATH, requirement_gap_branch_review)
    write_json(REQUIREMENT_GAP_EVIDENCE_SURFACE_REVIEW_PATH, requirement_gap_evidence_surface_review)
    write_json(BRANCH_PRECONDITION_REVIEW_PATH, branch_precondition_review)
    write_json(BRANCH_FORBIDDEN_ACTION_REVIEW_PATH, branch_forbidden_action_review)
    write_json(BRANCH_EXECUTION_READINESS_TABLE_PATH, branch_execution_readiness_table)
    write_json(NEXT_BRANCH_DECISION_TABLE_PATH, next_branch_decision_table)
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
        "BRANCH_SPLIT_REVIEW_0_SOURCE_RECEIPT_CONSUMED": SOURCE_BRANCH_SPLIT_RECEIPT_PATH.exists(),
        "BRANCH_SPLIT_REVIEW_1_REVIEW_ASSESSMENT_EMITTED": REVIEW_ASSESSMENT_PATH.exists(),
        "BRANCH_SPLIT_REVIEW_2_ROUTING_OBJECT_REVIEW_PASS": review_pass,
        "BRANCH_SPLIT_REVIEW_3_PROPOSAL_BRANCH_REVIEW_PASS": proposal_branch_review["review_status"] == "PROPOSAL_BRANCH_CONTRACT_REVIEW_PASS",
        "BRANCH_SPLIT_REVIEW_4_PROPOSAL_HOLD_PRESERVED": proposal_hold_review["proposal_hold_preserved"] is True,
        "BRANCH_SPLIT_REVIEW_5_AMBIGUITY_BRANCH_REVIEW_PASS": ambiguity_branch_review["review_status"] == "AMBIGUITY_BRANCH_CONTRACT_REVIEW_PASS",
        "BRANCH_SPLIT_REVIEW_6_REQUIREMENT_GAP_BRANCH_REVIEW_PASS": requirement_gap_branch_review["review_status"] == "REQUIREMENT_GAP_BRANCH_CONTRACT_REVIEW_PASS",
        "BRANCH_SPLIT_REVIEW_7_EXECUTION_READINESS_TABLE_EMITTED": BRANCH_EXECUTION_READINESS_TABLE_PATH.exists(),
        "BRANCH_SPLIT_REVIEW_8_NEXT_BRANCH_DECISION_EMITTED": NEXT_BRANCH_DECISION_TABLE_PATH.exists(),
        "BRANCH_SPLIT_REVIEW_9_PROPOSAL_BRANCH_SELECTED": classification["selected_next_branch"] == "proposal_review_branch",
        "BRANCH_SPLIT_REVIEW_10_FOUR_PROPOSAL_BINDINGS_RETAINED": proposal_binding_count == 4,
        "BRANCH_SPLIT_REVIEW_11_TWENTY_TWO_AMBIGUITY_BINDINGS_RETAINED": ambiguity_binding_count == 22,
        "BRANCH_SPLIT_REVIEW_12_FOUR_NINETY_EIGHT_GAP_BINDINGS_RETAINED": requirement_gap_binding_count == 498,
        "BRANCH_SPLIT_REVIEW_13_TOTAL_ROUTED_BINDINGS_524": total_routed_binding_count == 524,
        "BRANCH_SPLIT_REVIEW_14_NO_PROPOSAL_HOLD_RELEASE": proposal_hold_review["released_now"] is False,
        "BRANCH_SPLIT_REVIEW_15_NO_GLOBAL_SCHEMA_APPLICATION": rollup["schema_overlay_applied_globally_count"] == 0,
        "BRANCH_SPLIT_REVIEW_16_NO_REUSABLE_SCHEMA_AUTHORIZED": rollup["reusable_schema_authorized_count"] == 0,
        "BRANCH_SPLIT_REVIEW_17_NO_PREAPPROVED_SCHEMA_AUTHORIZED": rollup["preapproved_schema_authorized_count"] == 0,
        "BRANCH_SPLIT_REVIEW_18_NO_VALIDATOR_REGISTRY_ENTRY": rollup["validator_registry_entry_created_count"] == 0,
        "BRANCH_SPLIT_REVIEW_19_NO_FUTURE_AUTOMATIC_USE": rollup["future_automatic_use_allowed_count"] == 0,
        "BRANCH_SPLIT_REVIEW_20_NO_TYPING_RULE_APPLIED": rollup["typing_rule_applied_count"] == 0,
        "BRANCH_SPLIT_REVIEW_21_NO_FIELD_POLICY_MODIFIED": rollup["field_policy_modified_count"] == 0,
        "BRANCH_SPLIT_REVIEW_22_NO_CANDIDATE_ARTIFACT_MODIFIED": rollup["candidate_artifact_modified_count"] == 0,
        "BRANCH_SPLIT_REVIEW_23_NO_ROW_LOCATOR_APPLIED": rollup["source_row_locator_applied_count"] == 0,
        "BRANCH_SPLIT_REVIEW_24_NO_REBINDS_APPLIED": rollup["rebinds_applied_count"] == 0,
        "BRANCH_SPLIT_REVIEW_25_NO_VALUES_AUTHORIZED": rollup["values_authorized_count"] == 0,
        "BRANCH_SPLIT_REVIEW_26_NO_VALUES_APPLIED": rollup["values_applied_count"] == 0,
        "BRANCH_SPLIT_REVIEW_27_NO_METADATA_POPULATION": rollup["metadata_populated_count"] == 0,
        "BRANCH_SPLIT_REVIEW_28_NO_DISCRIMINATOR_READY": rollup["ready_discriminator_count"] == 0,
        "BRANCH_SPLIT_REVIEW_29_NO_TARGET_SELECTED": rollup["target_selected_for_build_count"] == 0,
        "BRANCH_SPLIT_REVIEW_30_NO_RUNTIME_PATCH": rollup["runtime_patch_applied_count"] == 0,
        "BRANCH_SPLIT_REVIEW_31_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "BRANCH_SPLIT_REVIEW_32_NO_LATEST_FILE_GUESSING": rollup["latest_file_guessing_count"] == 0,
        "BRANCH_SPLIT_REVIEW_33_NO_MTIME_SELECTION": rollup["mtime_selection_count"] == 0,
        "BRANCH_SPLIT_REVIEW_34_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "BRANCH_SPLIT_REVIEW_35_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "accepted_schema_overlay_reference_this_application_contract_only",
        "BRANCH_SPLIT_REVIEW_36_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "proposal": proposal_binding_count,
        "ambiguity": ambiguity_binding_count,
        "gap": requirement_gap_binding_count,
        "selected": classification["selected_next_branch"],
        "rebinds": 0,
        "metadata": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_branch_split_receipt_id": SOURCE_BRANCH_SPLIT_RECEIPT_ID,
        "machine_readable_partial_schema_aware_rebind_branch_split_review_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "branch_split_review_complete": not bool(failures),
            "branch_split_review_pass": review_pass,
            "proposal_branch_review_ready": review_pass,
            "ambiguity_branch_review_ready_later": review_pass,
            "requirement_gap_branch_review_ready_later": review_pass,
            "selected_next_branch": "proposal_review_branch" if review_pass else None,
            "proposal_binding_count": proposal_binding_count,
            "ambiguity_binding_count": ambiguity_binding_count,
            "requirement_gap_binding_count": requirement_gap_binding_count,
            "total_routed_binding_count": total_routed_binding_count,
            "proposal_hold_released": False,
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
            "routing_object_review": rel(ROUTING_OBJECT_REVIEW_PATH),
            "proposal_branch_review": rel(PROPOSAL_BRANCH_REVIEW_PATH),
            "proposal_hold_review": rel(PROPOSAL_HOLD_REVIEW_PATH),
            "ambiguity_branch_review": rel(AMBIGUITY_BRANCH_REVIEW_PATH),
            "ambiguity_evidence_surface_review": rel(AMBIGUITY_EVIDENCE_SURFACE_REVIEW_PATH),
            "requirement_gap_branch_review": rel(REQUIREMENT_GAP_BRANCH_REVIEW_PATH),
            "requirement_gap_evidence_surface_review": rel(REQUIREMENT_GAP_EVIDENCE_SURFACE_REVIEW_PATH),
            "branch_precondition_review": rel(BRANCH_PRECONDITION_REVIEW_PATH),
            "branch_forbidden_action_review": rel(BRANCH_FORBIDDEN_ACTION_REVIEW_PATH),
            "branch_execution_readiness_table": rel(BRANCH_EXECUTION_READINESS_TABLE_PATH),
            "next_branch_decision_table": rel(NEXT_BRANCH_DECISION_TABLE_PATH),
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
    print(f"partial_schema_aware_branch_split_review_receipt_id={receipt_id}")
    print(f"partial_schema_aware_branch_split_review_receipt_path={rel(receipt_path)}")
    print(f"partial_schema_aware_branch_split_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"partial_schema_aware_routing_object_review_path={rel(ROUTING_OBJECT_REVIEW_PATH)}")
    print(f"partial_schema_aware_proposal_branch_review_path={rel(PROPOSAL_BRANCH_REVIEW_PATH)}")
    print(f"partial_schema_aware_proposal_hold_review_path={rel(PROPOSAL_HOLD_REVIEW_PATH)}")
    print(f"partial_schema_aware_ambiguity_branch_review_path={rel(AMBIGUITY_BRANCH_REVIEW_PATH)}")
    print(f"partial_schema_aware_requirement_gap_branch_review_path={rel(REQUIREMENT_GAP_BRANCH_REVIEW_PATH)}")
    print(f"partial_schema_aware_branch_execution_readiness_table_path={rel(BRANCH_EXECUTION_READINESS_TABLE_PATH)}")
    print(f"partial_schema_aware_next_branch_decision_table_path={rel(NEXT_BRANCH_DECISION_TABLE_PATH)}")
    print(f"partial_schema_aware_branch_split_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"partial_schema_aware_branch_split_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
