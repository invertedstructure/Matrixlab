#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_MUTATION_TARGET_V0"
TARGET_UNIT_ID = "bounded_structured_t6_trigger_surface_capability.schema_archive_mutation_target_review_v0"
NEXT_UNIT_ID = "PREPARE_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_PACKET_V0"

MUTATION_TARGET_RECEIPT_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_receipt_2063a180"
MUTATION_TARGET_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_63de098e"
ARCHIVE_ENTRY_CANDIDATE_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_entry_candidate_72e26cec"
MUTATION_TARGET_REVIEW_TARGET_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_bd32234b"
ACCEPT_DECISION_RECEIPT_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_receipt_5641e392"
ACCEPT_DECISION_RECORD_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_a0d0c10d"

ADOPTION_PATH_ID = "bounded_structured_t6_trigger_surface_capability_adoption_path_6f9974e5"
CAPABILITY_BUILD_ID = "bounded_structured_t6_trigger_surface_capability_build_721f09dc"
PROPOSAL_ID = "capability_proposal_57dda6e9"
REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"
SCHEMA_NAME = "bounded_structured_t6_trigger_surface_capability_v0"
SELECTED_SCHEMA_PROMOTION_DECISION = "ACCEPT_SCHEMA_ARCHIVE_PROMOTION_FOR_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY"

MUTATION_TARGET_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0_receipts/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_receipt_2063a180.json"
REVIEW_TARGET_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_target_v0.json"
ARCHIVE_ENTRY_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_entry_candidate_v0.json"
MUTATION_PLAN_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_plan_v0.json"
MUTATION_PRECONDITIONS_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_preconditions_v0.json"
AUTHORITY_BOUNDARY_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_authority_boundary_v0.json"
NEGATIVE_CONTROL_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_negative_control_v0.json"
SOURCE_CHAIN_BINDING_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_source_chain_binding_v0.json"
SCHEMA_CANDIDATE_SNAPSHOT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_schema_candidate_snapshot_v0.json"
MUTATION_TARGET_ROLLUP_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_rollup_v0.json"

ACCEPT_DECISION_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_v0_receipts/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_receipt_5641e392.json"
SCHEMA_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_schema_candidate_v0.json"
CAPABILITY_PROFILE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_profile_v0.json"
BUILD_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_receipt_9f1f0079.json"
BUILD_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_review_receipt_b8dba552.json"
PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"

OUT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_v0"
RECEIPT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_basis_v0.json"
SOURCE_CHAIN_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_source_chain_review_v0.json"
ARCHIVE_ENTRY_CANDIDATE_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_entry_candidate_review_v0.json"
MUTATION_PLAN_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_plan_review_v0.json"
MUTATION_PRECONDITIONS_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_preconditions_review_v0.json"
AUTHORITY_BOUNDARY_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_authority_boundary_review_v0.json"
NEGATIVE_CONTROL_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_negative_control_review_v0.json"
WRITE_DECISION_PACKET_PREP_TARGET_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_prep_target_v0.json"
READOUT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_transition_trace.json"

FORBIDDEN_FALSE_KEYS = [
    "schema_archive_mutation_authorized",
    "schema_mutation_authorized",
    "schema_archive_write_authorized",
    "schema_archive_write_executed",
    "runtime_adoption_authorized",
    "runtime_patch_authorized",
    "move_addition_authorized",
    "fixture_expansion_authorized",
    "t6_live_case_execution_authorized",
    "hidden_next_command",
    "c8_authorized",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def require_false(obj: Dict[str, Any], key: str, failures: List[str], prefix: str) -> None:
    if obj.get(key) is not False:
        failures.append(f"{prefix}_{key}_not_false:{obj.get(key)}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        MUTATION_TARGET_RECEIPT_PATH,
        REVIEW_TARGET_PATH,
        ARCHIVE_ENTRY_CANDIDATE_PATH,
        MUTATION_PLAN_PATH,
        MUTATION_PRECONDITIONS_PATH,
        AUTHORITY_BOUNDARY_PATH,
        NEGATIVE_CONTROL_PATH,
        SOURCE_CHAIN_BINDING_PATH,
        SCHEMA_CANDIDATE_SNAPSHOT_PATH,
        MUTATION_TARGET_ROLLUP_PATH,
        ACCEPT_DECISION_RECEIPT_PATH,
        SCHEMA_CANDIDATE_PATH,
        CAPABILITY_PROFILE_PATH,
        BUILD_RECEIPT_PATH,
        BUILD_REVIEW_RECEIPT_PATH,
        PROPOSAL_PATH,
    ]

    failures: List[str] = []
    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    mutation_receipt = read_json(MUTATION_TARGET_RECEIPT_PATH)
    review_target = read_json(REVIEW_TARGET_PATH)
    archive_entry_candidate = read_json(ARCHIVE_ENTRY_CANDIDATE_PATH)
    mutation_plan = read_json(MUTATION_PLAN_PATH)
    mutation_preconditions = read_json(MUTATION_PRECONDITIONS_PATH)
    authority_boundary = read_json(AUTHORITY_BOUNDARY_PATH)
    negative_control = read_json(NEGATIVE_CONTROL_PATH)
    source_chain_binding = read_json(SOURCE_CHAIN_BINDING_PATH)
    schema_candidate_snapshot = read_json(SCHEMA_CANDIDATE_SNAPSHOT_PATH)
    mutation_rollup = read_json(MUTATION_TARGET_ROLLUP_PATH)

    accept_receipt = read_json(ACCEPT_DECISION_RECEIPT_PATH)
    schema_candidate = read_json(SCHEMA_CANDIDATE_PATH)
    capability_profile = read_json(CAPABILITY_PROFILE_PATH)
    build_receipt = read_json(BUILD_RECEIPT_PATH)
    build_review_receipt = read_json(BUILD_REVIEW_RECEIPT_PATH)
    proposal = read_json(PROPOSAL_PATH)

    mutation_summary = mutation_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_summary", {})
    accept_summary = accept_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_summary", {})
    build_summary = build_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_summary", {})
    build_review_summary = build_review_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_review_summary", {})

    if mutation_receipt.get("receipt_id") != MUTATION_TARGET_RECEIPT_ID:
        failures.append(f"mutation_receipt_id_wrong:{mutation_receipt.get('receipt_id')}")
    if mutation_receipt.get("gate") != "PASS":
        failures.append("mutation_receipt_gate_not_pass")
    if mutation_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append(f"mutation_receipt_terminal_next_wrong:{mutation_receipt.get('terminal', {}).get('next_unit_id')}")

    for key in ["schema_archive_mutation_target_prepared", "schema_archive_mutation_target_review_ready"]:
        if mutation_summary.get(key) is not True:
            failures.append(f"mutation_summary_{key}_not_true:{mutation_summary.get(key)}")

    if mutation_summary.get("mutation_target_id") != MUTATION_TARGET_ID:
        failures.append(f"mutation_target_id_wrong:{mutation_summary.get('mutation_target_id')}")
    if mutation_summary.get("archive_entry_candidate_id") != ARCHIVE_ENTRY_CANDIDATE_ID:
        failures.append(f"archive_entry_candidate_id_wrong:{mutation_summary.get('archive_entry_candidate_id')}")
    if mutation_summary.get("schema_archive_mutation_target_review_target_id") != MUTATION_TARGET_REVIEW_TARGET_ID:
        failures.append(f"review_target_id_wrong:{mutation_summary.get('schema_archive_mutation_target_review_target_id')}")

    for key in FORBIDDEN_FALSE_KEYS:
        require_false(mutation_summary, key, failures, "mutation_summary")

    if review_target.get("target_status") != "READY":
        failures.append(f"review_target_status_wrong:{review_target.get('target_status')}")
    if review_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"review_target_next_wrong:{review_target.get('next_unit_id')}")
    if review_target.get("schema_archive_mutation_target_review_target_id") != MUTATION_TARGET_REVIEW_TARGET_ID:
        failures.append("review_target_id_mismatch")
    if review_target.get("mutation_target_id") != MUTATION_TARGET_ID:
        failures.append("review_target_mutation_target_id_mismatch")
    if review_target.get("archive_entry_candidate_id") != ARCHIVE_ENTRY_CANDIDATE_ID:
        failures.append("review_target_archive_entry_candidate_id_mismatch")
    if review_target.get("requires_later_human_decision_before_schema_archive_write") is not True:
        failures.append("review_target_later_human_write_decision_not_required")

    for key in ["schema_archive_mutation_authorized", "schema_mutation_authorized", "schema_archive_write_authorized", "schema_archive_write_executed"]:
        require_false(review_target, key, failures, "review_target")

    if archive_entry_candidate.get("archive_entry_candidate_id") != ARCHIVE_ENTRY_CANDIDATE_ID:
        failures.append("archive_entry_candidate_id_mismatch")
    if archive_entry_candidate.get("entry_status") != "CANDIDATE_ONLY_NOT_WRITTEN":
        failures.append(f"archive_entry_status_wrong:{archive_entry_candidate.get('entry_status')}")
    if archive_entry_candidate.get("archive_write_status") != "NOT_WRITTEN":
        failures.append(f"archive_write_status_wrong:{archive_entry_candidate.get('archive_write_status')}")
    if archive_entry_candidate.get("schema_name") != SCHEMA_NAME:
        failures.append(f"archive_entry_schema_name_wrong:{archive_entry_candidate.get('schema_name')}")
    for key in ["schema_archive_mutation_authorized", "schema_archive_write_executed"]:
        require_false(archive_entry_candidate, key, failures, "archive_entry_candidate")

    if mutation_plan.get("mutation_target_id") != MUTATION_TARGET_ID:
        failures.append("mutation_plan_target_id_mismatch")
    if mutation_plan.get("plan_status") != "REVIEW_READY_NOT_EXECUTED":
        failures.append(f"mutation_plan_status_wrong:{mutation_plan.get('plan_status')}")
    if mutation_plan.get("planned_operation") != "ADD_SCHEMA_ENTRY_CANDIDATE_TO_SCHEMA_ARCHIVE":
        failures.append(f"planned_operation_wrong:{mutation_plan.get('planned_operation')}")
    if mutation_plan.get("pre_write_review_required") is not True:
        failures.append("mutation_plan_pre_write_review_not_required")
    if mutation_plan.get("pre_write_human_decision_required") is not True:
        failures.append("mutation_plan_pre_write_human_decision_not_required")
    if mutation_plan.get("write_executed_now") is not False:
        failures.append("mutation_plan_write_executed_now_not_false")
    for key in ["schema_archive_mutation_authorized", "schema_archive_write_authorized"]:
        require_false(mutation_plan, key, failures, "mutation_plan")

    if mutation_preconditions.get("preconditions_status") != "READY_FOR_REVIEW":
        failures.append(f"preconditions_status_wrong:{mutation_preconditions.get('preconditions_status')}")
    required_before_write = mutation_preconditions.get("required_before_write") or []
    for required in [
        "review mutation target",
        "verify source chain",
        "verify candidate-only archive entry",
        "verify no current archive mutation occurred",
        "record later human decision for schema archive write",
    ]:
        if required not in required_before_write:
            failures.append(f"precondition_missing:{required}")

    if authority_boundary.get("boundary_status") != "PASS":
        failures.append(f"authority_boundary_status_wrong:{authority_boundary.get('boundary_status')}")
    if authority_boundary.get("schema_archive_mutation_target_prepared") is not True:
        failures.append("authority_boundary_target_not_prepared")
    if authority_boundary.get("schema_archive_mutation_target_review_ready") is not True:
        failures.append("authority_boundary_review_not_ready")
    for key in FORBIDDEN_FALSE_KEYS:
        require_false(authority_boundary, key, failures, "authority_boundary")

    if negative_control.get("negative_control_status") != "PASS":
        failures.append(f"negative_control_status_wrong:{negative_control.get('negative_control_status')}")
    zero = negative_control.get("zero_counters_for_this_unit") or {}
    for key in [
        "schema_archive_mutation_count",
        "schema_mutation_count",
        "schema_archive_write_count",
        "runtime_adoption_count",
        "runtime_patch_count",
        "move_addition_count",
        "fixture_expansion_count",
        "t6_live_case_execution_count",
        "hidden_next_command_count",
        "c8_authorization_count",
    ]:
        if zero.get(key) != 0:
            failures.append(f"negative_counter_wrong:{key}:{zero.get(key)}")

    if source_chain_binding.get("binding_status") != "PASS":
        failures.append("source_chain_binding_not_pass")
    if source_chain_binding.get("mutation_target_id") != MUTATION_TARGET_ID:
        failures.append("source_chain_mutation_target_id_wrong")
    if schema_candidate_snapshot.get("snapshot_status") != "BOUND_FOR_REVIEW":
        failures.append(f"schema_snapshot_status_wrong:{schema_candidate_snapshot.get('snapshot_status')}")
    if mutation_rollup.get("schema_archive_mutation_target_review_ready") is not True:
        failures.append("mutation_rollup_review_ready_not_true")

    if accept_summary.get("schema_archive_mutation_target_prep_authorized") is not True:
        failures.append("accept_summary_target_prep_not_authorized")
    if accept_summary.get("schema_archive_mutation_authorized") is not False:
        failures.append("accept_summary_archive_mutation_authorized_unexpected")

    if schema_candidate.get("schema_candidate_status") != "BUILT_CANDIDATE_ONLY_NOT_ARCHIVE_MUTATION":
        failures.append(f"schema_candidate_status_wrong:{schema_candidate.get('schema_candidate_status')}")
    if schema_candidate.get("schema_name") != SCHEMA_NAME:
        failures.append(f"schema_candidate_name_wrong:{schema_candidate.get('schema_name')}")
    if schema_candidate.get("archive_mutation_authorized") is not False:
        failures.append("schema_candidate_archive_mutation_authorized_unexpected")
    if capability_profile.get("capability_name") != REQUIRED_CAPABILITY:
        failures.append(f"capability_profile_name_wrong:{capability_profile.get('capability_name')}")
    if capability_profile.get("surface_name") != SCHEMA_NAME:
        failures.append(f"capability_profile_surface_wrong:{capability_profile.get('surface_name')}")
    if build_summary.get("build_executed") is not True:
        failures.append("build_not_executed")
    if build_review_summary.get("artifact_review_pass") is not True:
        failures.append("build_review_not_pass")
    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_PASS_WRITE_DECISION_PACKET_PREP_READY"
        if gate == "PASS"
        else "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_GATE_FAIL"
    )

    mutation_target_review_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_" + sig8({
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "source_receipt": MUTATION_TARGET_RECEIPT_ID,
        "unit_id": UNIT_ID,
    })

    write_decision_packet_prep_target_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_prep_" + sig8({
        "mutation_target_review_id": mutation_target_review_id,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "schema_name": SCHEMA_NAME,
    })

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    source_chain_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_source_chain_review_v0",
        "mutation_target_review_id": mutation_target_review_id,
        "review_status": "PASS" if gate == "PASS" else "BLOCKED",
        "proposal_id": PROPOSAL_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "accept_decision_record_id": ACCEPT_DECISION_RECORD_ID,
        "accept_decision_receipt_id": ACCEPT_DECISION_RECEIPT_ID,
        "mutation_target_receipt_id": MUTATION_TARGET_RECEIPT_ID,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "selected_schema_promotion_decision": SELECTED_SCHEMA_PROMOTION_DECISION,
        "source_chain_consistent": True if gate == "PASS" else False,
    }

    archive_entry_candidate_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_entry_candidate_review_v0",
        "mutation_target_review_id": mutation_target_review_id,
        "review_status": "PASS" if gate == "PASS" else "BLOCKED",
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "schema_name": SCHEMA_NAME,
        "entry_status": archive_entry_candidate.get("entry_status"),
        "archive_write_status": archive_entry_candidate.get("archive_write_status"),
        "candidate_only_not_written": archive_entry_candidate.get("entry_status") == "CANDIDATE_ONLY_NOT_WRITTEN",
        "schema_archive_mutation_authorized": False,
        "schema_archive_write_executed": False,
    }

    mutation_plan_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_plan_review_v0",
        "mutation_target_review_id": mutation_target_review_id,
        "review_status": "PASS" if gate == "PASS" else "BLOCKED",
        "mutation_target_id": MUTATION_TARGET_ID,
        "planned_operation": mutation_plan.get("planned_operation"),
        "plan_status": mutation_plan.get("plan_status"),
        "pre_write_review_required": mutation_plan.get("pre_write_review_required"),
        "pre_write_human_decision_required": mutation_plan.get("pre_write_human_decision_required"),
        "write_executed_now": False,
        "schema_archive_mutation_authorized": False,
        "schema_archive_write_authorized": False,
    }

    mutation_preconditions_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_preconditions_review_v0",
        "mutation_target_review_id": mutation_target_review_id,
        "review_status": "PASS" if gate == "PASS" else "BLOCKED",
        "mutation_target_id": MUTATION_TARGET_ID,
        "preconditions_status": mutation_preconditions.get("preconditions_status"),
        "required_before_write": mutation_preconditions.get("required_before_write"),
        "not_satisfied_in_this_unit": mutation_preconditions.get("not_satisfied_in_this_unit"),
        "review_confirms_later_human_decision_required": True if gate == "PASS" else False,
    }

    authority_boundary_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_authority_boundary_review_v0",
        "mutation_target_review_id": mutation_target_review_id,
        "review_status": "PASS" if gate == "PASS" else "BLOCKED",
        "mutation_target_id": MUTATION_TARGET_ID,
        "schema_archive_mutation_target_review_pass": True if gate == "PASS" else False,
        "write_decision_packet_prep_target_ready": True if gate == "PASS" else False,
        "allowed_effect": "prepare schema archive write human decision packet target",
        "not_allowed_effects": [
            "schema archive write",
            "schema archive mutation",
            "schema mutation",
            "runtime adoption",
            "runtime patch",
            "move addition",
            "fixture expansion",
            "T6 live case execution",
            "C8 authorization",
        ],
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "schema_archive_write_authorized": False,
        "schema_archive_write_executed": False,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
    }

    negative_control_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_negative_control_review_v0",
        "mutation_target_review_id": mutation_target_review_id,
        "review_status": "PASS" if gate == "PASS" else "BLOCKED",
        "mutation_target_id": MUTATION_TARGET_ID,
        "source_negative_control_status": negative_control.get("negative_control_status"),
        "zero_counters_confirmed": True if gate == "PASS" else False,
        "schema_archive_mutation_count": 0,
        "schema_mutation_count": 0,
        "schema_archive_write_count": 0,
        "runtime_adoption_count": 0,
        "runtime_patch_count": 0,
        "move_addition_count": 0,
        "fixture_expansion_count": 0,
        "t6_live_case_execution_count": 0,
        "hidden_next_command_count": 0,
        "c8_authorization_count": 0,
    }

    basis = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_basis_v0",
        "unit_id": UNIT_ID,
        "mutation_target_review_id": mutation_target_review_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_mutation_target_receipt_id": MUTATION_TARGET_RECEIPT_ID,
        "source_mutation_target_id": MUTATION_TARGET_ID,
        "source_archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "source_review_target_id": MUTATION_TARGET_REVIEW_TARGET_ID,
        "review_claim": "Review mutation target and emit write-decision packet prep target only. Do not write to or mutate schema archive.",
        "source_file_hashes": source_hashes,
    }

    write_decision_packet_prep_target = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_prep_target_v0",
        "target_status": "READY" if gate == "PASS" else "BLOCKED",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "schema_archive_write_human_decision_packet_prep_target_id": write_decision_packet_prep_target_id if gate == "PASS" else None,
        "mutation_target_review_id": mutation_target_review_id,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "schema_name": SCHEMA_NAME,
        "source_mutation_target_receipt_id": MUTATION_TARGET_RECEIPT_ID,
        "target_scope": "Prepare a human decision packet for whether to authorize the bounded schema archive write. Do not write to schema archive in the packet prep unit.",
        "schema_archive_mutation_target_review_pass": True if gate == "PASS" else False,
        "human_decision_required_before_write": True,
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "schema_archive_write_authorized": False,
        "schema_archive_write_executed": False,
        "does_not_authorize_runtime_adoption": True,
        "does_not_authorize_move_addition": True,
        "does_not_authorize_fixture_expansion": True,
        "does_not_authorize_t6_live_case_execution": True,
        "does_not_authorize_c8": True,
    }

    rollup = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "mutation_target_review_id": mutation_target_review_id,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "schema_name": SCHEMA_NAME,
        "source_mutation_target_receipt_id": MUTATION_TARGET_RECEIPT_ID,
        "source_accept_decision_receipt_id": ACCEPT_DECISION_RECEIPT_ID,
        "source_chain_review_pass": source_chain_review["review_status"] == "PASS",
        "archive_entry_candidate_review_pass": archive_entry_candidate_review["review_status"] == "PASS",
        "mutation_plan_review_pass": mutation_plan_review["review_status"] == "PASS",
        "mutation_preconditions_review_pass": mutation_preconditions_review["review_status"] == "PASS",
        "authority_boundary_review_pass": authority_boundary_review["review_status"] == "PASS",
        "negative_control_review_pass": negative_control_review["review_status"] == "PASS",
        "schema_archive_mutation_target_review_pass": True if gate == "PASS" else False,
        "schema_archive_write_human_decision_packet_prep_target_ready": True if gate == "PASS" else False,
        "schema_archive_write_human_decision_packet_prep_target_id": write_decision_packet_prep_target_id if gate == "PASS" else None,
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "schema_archive_write_authorized": False,
        "schema_archive_write_executed": False,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    readout = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_readout_v0",
        "status": status,
        "mutation_target_review_id": mutation_target_review_id,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "schema_name": SCHEMA_NAME,
        "interpretation": "Schema archive mutation target reviewed. Write-decision packet prep target is ready; no schema archive write or mutation occurred."
        if gate == "PASS" else "Schema archive mutation target review failed typed gates.",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    profile = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_profile_v0",
        "profile_status": status,
        "mutation_target_review_id": mutation_target_review_id,
        "core_rule": "Review target only. Actual schema archive write remains blocked behind a later human decision and write unit.",
        "write_decision_packet_prep_target_ref": rel(WRITE_DECISION_PACKET_PREP_TARGET_PATH),
        "must_not_infer": [
            "schema archive mutated",
            "schema promoted",
            "schema archive write authorized",
            "schema archive write executed",
            "schema mutation authorized",
            "runtime adopted",
            "runtime patched",
            "move registry updated",
            "fixture suite expanded",
            "T6 live case executed",
            "C8 authorized",
        ],
    }

    report = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "review_result": "SCHEMA_ARCHIVE_WRITE_DECISION_PACKET_PREP_READY" if gate == "PASS" else "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_GATE_FAIL",
            "mutation_target_review_id": mutation_target_review_id,
            "mutation_target_id": MUTATION_TARGET_ID,
            "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
            "schema_name": SCHEMA_NAME,
            "schema_archive_mutation_target_review_pass": True if gate == "PASS" else False,
            "schema_archive_write_human_decision_packet_prep_target_ready": True if gate == "PASS" else False,
            "schema_archive_mutation_authorized": False,
            "schema_mutation_authorized": False,
            "schema_archive_write_authorized": False,
            "schema_archive_write_executed": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_transition_trace_v0",
        "unit_id": UNIT_ID,
        "mutation_target_review_id": mutation_target_review_id,
        "transitions": [
            {
                "from": "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_READY",
                "edge": "review mutation target source chain, candidate, mutation plan, preconditions, boundary, and negative control",
                "to": "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_PASS" if gate == "PASS" else "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_GATE_FAIL",
            },
            {
                "from": "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_PASS" if gate == "PASS" else "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_GATE_FAIL",
                "edge": "emit schema archive write human decision packet prep target without archive write",
                "to": "SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_PACKET_PREP_READY" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (SOURCE_CHAIN_REVIEW_PATH, source_chain_review),
        (ARCHIVE_ENTRY_CANDIDATE_REVIEW_PATH, archive_entry_candidate_review),
        (MUTATION_PLAN_REVIEW_PATH, mutation_plan_review),
        (MUTATION_PRECONDITIONS_REVIEW_PATH, mutation_preconditions_review),
        (AUTHORITY_BOUNDARY_REVIEW_PATH, authority_boundary_review),
        (NEGATIVE_CONTROL_REVIEW_PATH, negative_control_review),
        (WRITE_DECISION_PACKET_PREP_TARGET_PATH, write_decision_packet_prep_target),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "SCHEMA_ARCHIVE_MUTATION_TARGET_RECEIPT_CONSUMED",
        "MUTATION_TARGET_REVIEW_TARGET_CONSUMED",
        "SOURCE_CHAIN_REVIEW_PASS",
        "ARCHIVE_ENTRY_CANDIDATE_REVIEW_PASS",
        "MUTATION_PLAN_REVIEW_PASS",
        "MUTATION_PRECONDITIONS_REVIEW_PASS",
        "AUTHORITY_BOUNDARY_REVIEW_PASS",
        "NEGATIVE_CONTROL_REVIEW_PASS",
        "WRITE_HUMAN_DECISION_PACKET_PREP_TARGET_EMITTED",
        "NO_SCHEMA_ARCHIVE_MUTATION",
        "NO_SCHEMA_MUTATION_EXECUTION",
        "NO_SCHEMA_ARCHIVE_WRITE_AUTHORIZATION",
        "NO_SCHEMA_ARCHIVE_WRITE_EXECUTION",
        "NO_RUNTIME_ADOPTION_AUTHORITY",
        "NO_RUNTIME_PATCH",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION",
        "NO_T6_LIVE_CASE_EXECUTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "mutation_target_review_id": mutation_target_review_id,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "source_mutation_target_receipt_id": MUTATION_TARGET_RECEIPT_ID,
        "source_mutation_target_receipt_ref": rel(MUTATION_TARGET_RECEIPT_PATH),
        "source_accept_decision_receipt_id": ACCEPT_DECISION_RECEIPT_ID,
        "source_accept_decision_record_id": ACCEPT_DECISION_RECORD_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_0_RECEIPT_CONSUMED": gate == "PASS",
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_1_REVIEW_TARGET_CONSUMED": gate == "PASS",
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_2_SOURCE_CHAIN_REVIEW_PASS": source_chain_review["review_status"] == "PASS",
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_3_ARCHIVE_ENTRY_CANDIDATE_REVIEW_PASS": archive_entry_candidate_review["review_status"] == "PASS",
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_4_MUTATION_PLAN_REVIEW_PASS": mutation_plan_review["review_status"] == "PASS",
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_5_MUTATION_PRECONDITIONS_REVIEW_PASS": mutation_preconditions_review["review_status"] == "PASS",
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_6_AUTHORITY_BOUNDARY_REVIEW_PASS": authority_boundary_review["review_status"] == "PASS",
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_7_NEGATIVE_CONTROL_REVIEW_PASS": negative_control_review["review_status"] == "PASS",
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_8_WRITE_DECISION_PACKET_PREP_TARGET_EMITTED": WRITE_DECISION_PACKET_PREP_TARGET_PATH.exists() and gate == "PASS",
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_9_NO_SCHEMA_ARCHIVE_MUTATION": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_10_NO_SCHEMA_MUTATION": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_11_NO_SCHEMA_ARCHIVE_WRITE_AUTHORIZATION": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_12_NO_SCHEMA_ARCHIVE_WRITE_EXECUTION": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_13_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_14_NO_RUNTIME_PATCH": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_15_NO_MOVE_ADDITION": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_16_NO_FIXTURE_EXPANSION": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_17_NO_T6_LIVE_CASE_EXECUTION": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_18_NO_C8_AUTHORIZATION": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_19_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_summary": {
            "status": status,
            "mutation_target_review_id": mutation_target_review_id,
            "mutation_target_id": MUTATION_TARGET_ID,
            "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
            "source_mutation_target_receipt_id": MUTATION_TARGET_RECEIPT_ID,
            "source_accept_decision_receipt_id": ACCEPT_DECISION_RECEIPT_ID,
            "source_accept_decision_record_id": ACCEPT_DECISION_RECORD_ID,
            "schema_name": SCHEMA_NAME,
            "schema_archive_mutation_target_review_pass": True if gate == "PASS" else False,
            "source_chain_review_pass": source_chain_review["review_status"] == "PASS",
            "archive_entry_candidate_review_pass": archive_entry_candidate_review["review_status"] == "PASS",
            "mutation_plan_review_pass": mutation_plan_review["review_status"] == "PASS",
            "mutation_preconditions_review_pass": mutation_preconditions_review["review_status"] == "PASS",
            "authority_boundary_review_pass": authority_boundary_review["review_status"] == "PASS",
            "negative_control_review_pass": negative_control_review["review_status"] == "PASS",
            "schema_archive_write_human_decision_packet_prep_target_ready": True if gate == "PASS" else False,
            "schema_archive_write_human_decision_packet_prep_target_id": write_decision_packet_prep_target_id if gate == "PASS" else None,
            "schema_archive_mutation_authorized": False,
            "schema_mutation_authorized": False,
            "schema_archive_write_authorized": False,
            "schema_archive_write_executed": False,
            "runtime_adoption_authorized": False,
            "runtime_patch_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "t6_live_case_execution_authorized": False,
            "hidden_next_command": False,
            "c8_authorized": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "source_chain_review": rel(SOURCE_CHAIN_REVIEW_PATH),
            "archive_entry_candidate_review": rel(ARCHIVE_ENTRY_CANDIDATE_REVIEW_PATH),
            "mutation_plan_review": rel(MUTATION_PLAN_REVIEW_PATH),
            "mutation_preconditions_review": rel(MUTATION_PRECONDITIONS_REVIEW_PATH),
            "authority_boundary_review": rel(AUTHORITY_BOUNDARY_REVIEW_PATH),
            "negative_control_review": rel(NEGATIVE_CONTROL_REVIEW_PATH),
            "write_decision_packet_prep_target": rel(WRITE_DECISION_PACKET_PREP_TARGET_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_receipt_id={receipt_id}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_receipt_path={rel(receipt_path)}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_id={mutation_target_review_id if gate == 'PASS' else 'NONE'}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
