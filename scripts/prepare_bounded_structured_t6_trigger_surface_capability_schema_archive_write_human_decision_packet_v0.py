#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PREPARE_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_PACKET_V0"
TARGET_UNIT_ID = "bounded_structured_t6_trigger_surface_capability.schema_archive_write_human_decision_packet_v0"

MUTATION_TARGET_REVIEW_RECEIPT_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_receipt_e8f12c97"
MUTATION_TARGET_REVIEW_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_213c76c7"
MUTATION_TARGET_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_63de098e"
ARCHIVE_ENTRY_CANDIDATE_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_entry_candidate_72e26cec"
WRITE_DECISION_PACKET_PREP_TARGET_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_prep_cb1e3ade"
ACCEPT_DECISION_RECEIPT_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_receipt_5641e392"
ACCEPT_DECISION_RECORD_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_a0d0c10d"

ADOPTION_PATH_ID = "bounded_structured_t6_trigger_surface_capability_adoption_path_6f9974e5"
CAPABILITY_BUILD_ID = "bounded_structured_t6_trigger_surface_capability_build_721f09dc"
PROPOSAL_ID = "capability_proposal_57dda6e9"
SCHEMA_NAME = "bounded_structured_t6_trigger_surface_capability_v0"
REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"

MUTATION_TARGET_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_v0_receipts/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_receipt_e8f12c97.json"
WRITE_DECISION_PACKET_PREP_TARGET_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_prep_target_v0.json"
SOURCE_CHAIN_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_source_chain_review_v0.json"
ARCHIVE_ENTRY_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_entry_candidate_review_v0.json"
MUTATION_PLAN_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_plan_review_v0.json"
MUTATION_PRECONDITIONS_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_preconditions_review_v0.json"
AUTHORITY_BOUNDARY_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_authority_boundary_review_v0.json"
NEGATIVE_CONTROL_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_negative_control_review_v0.json"

MUTATION_TARGET_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0_receipts/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_receipt_2063a180.json"
ARCHIVE_ENTRY_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_entry_candidate_v0.json"
MUTATION_PLAN_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_plan_v0.json"
SCHEMA_CANDIDATE_SNAPSHOT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_schema_candidate_snapshot_v0.json"

ACCEPT_DECISION_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_v0_receipts/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_receipt_5641e392.json"
SCHEMA_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_schema_candidate_v0.json"
CAPABILITY_PROFILE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_profile_v0.json"
BUILD_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_receipt_9f1f0079.json"
BUILD_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_review_receipt_b8dba552.json"
PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"

OUT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_v0"
RECEIPT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_basis_v0.json"
SOURCE_CHAIN_BINDING_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_source_chain_binding_v0.json"
WRITE_SCOPE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_scope_v0.json"
WRITE_PAYLOAD_BINDING_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_payload_binding_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authority_boundary_v0.json"
DECISION_OPTIONS_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_decision_options_v0.json"
DECISION_EFFECTS_MAP_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_decision_effects_map_v0.json"
AUTHORIZE_OPTION_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_option_authorize_v0.json"
DEFER_OPTION_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_option_defer_v0.json"
REJECT_OPTION_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_option_reject_v0.json"
CLOSE_OPTION_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_option_close_no_write_v0.json"
REQUEST_PACKET_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_request_packet_v0.json"
NEGATIVE_CONTROL_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_negative_control_v0.json"
READOUT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_transition_trace.json"

STOP_CODE = "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_REQUIRED"

DECISION_OPTIONS = [
    "AUTHORIZE_SCHEMA_ARCHIVE_WRITE_FOR_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY",
    "DEFER_SCHEMA_ARCHIVE_WRITE_DECISION",
    "REJECT_SCHEMA_ARCHIVE_WRITE",
    "CLOSE_SCHEMA_ARCHIVE_WRITE_PATH_NO_WRITE",
]

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
        MUTATION_TARGET_REVIEW_RECEIPT_PATH,
        WRITE_DECISION_PACKET_PREP_TARGET_PATH,
        SOURCE_CHAIN_REVIEW_PATH,
        ARCHIVE_ENTRY_REVIEW_PATH,
        MUTATION_PLAN_REVIEW_PATH,
        MUTATION_PRECONDITIONS_REVIEW_PATH,
        AUTHORITY_BOUNDARY_REVIEW_PATH,
        NEGATIVE_CONTROL_REVIEW_PATH,
        MUTATION_TARGET_RECEIPT_PATH,
        ARCHIVE_ENTRY_CANDIDATE_PATH,
        MUTATION_PLAN_PATH,
        SCHEMA_CANDIDATE_SNAPSHOT_PATH,
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

    review_receipt = read_json(MUTATION_TARGET_REVIEW_RECEIPT_PATH)
    prep_target = read_json(WRITE_DECISION_PACKET_PREP_TARGET_PATH)
    source_chain_review = read_json(SOURCE_CHAIN_REVIEW_PATH)
    archive_entry_review = read_json(ARCHIVE_ENTRY_REVIEW_PATH)
    mutation_plan_review = read_json(MUTATION_PLAN_REVIEW_PATH)
    mutation_preconditions_review = read_json(MUTATION_PRECONDITIONS_REVIEW_PATH)
    authority_boundary_review = read_json(AUTHORITY_BOUNDARY_REVIEW_PATH)
    negative_control_review = read_json(NEGATIVE_CONTROL_REVIEW_PATH)

    mutation_receipt = read_json(MUTATION_TARGET_RECEIPT_PATH)
    archive_entry_candidate = read_json(ARCHIVE_ENTRY_CANDIDATE_PATH)
    mutation_plan = read_json(MUTATION_PLAN_PATH)
    schema_candidate_snapshot = read_json(SCHEMA_CANDIDATE_SNAPSHOT_PATH)

    accept_receipt = read_json(ACCEPT_DECISION_RECEIPT_PATH)
    schema_candidate = read_json(SCHEMA_CANDIDATE_PATH)
    capability_profile = read_json(CAPABILITY_PROFILE_PATH)
    build_receipt = read_json(BUILD_RECEIPT_PATH)
    build_review_receipt = read_json(BUILD_REVIEW_RECEIPT_PATH)
    proposal = read_json(PROPOSAL_PATH)

    review_summary = review_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_summary", {})
    mutation_summary = mutation_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_summary", {})
    accept_summary = accept_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_summary", {})
    build_summary = build_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_summary", {})
    build_review_summary = build_review_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_review_summary", {})

    if review_receipt.get("receipt_id") != MUTATION_TARGET_REVIEW_RECEIPT_ID:
        failures.append(f"review_receipt_id_wrong:{review_receipt.get('receipt_id')}")
    if review_receipt.get("gate") != "PASS":
        failures.append("review_receipt_gate_not_pass")
    if review_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append(f"review_terminal_next_wrong:{review_receipt.get('terminal', {}).get('next_unit_id')}")

    for key in [
        "schema_archive_mutation_target_review_pass",
        "source_chain_review_pass",
        "archive_entry_candidate_review_pass",
        "mutation_plan_review_pass",
        "mutation_preconditions_review_pass",
        "authority_boundary_review_pass",
        "negative_control_review_pass",
        "schema_archive_write_human_decision_packet_prep_target_ready",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"review_summary_{key}_not_true:{review_summary.get(key)}")

    if review_summary.get("mutation_target_review_id") != MUTATION_TARGET_REVIEW_ID:
        failures.append(f"mutation_target_review_id_wrong:{review_summary.get('mutation_target_review_id')}")
    if review_summary.get("mutation_target_id") != MUTATION_TARGET_ID:
        failures.append(f"mutation_target_id_wrong:{review_summary.get('mutation_target_id')}")
    if review_summary.get("archive_entry_candidate_id") != ARCHIVE_ENTRY_CANDIDATE_ID:
        failures.append(f"archive_entry_candidate_id_wrong:{review_summary.get('archive_entry_candidate_id')}")
    if review_summary.get("schema_archive_write_human_decision_packet_prep_target_id") != WRITE_DECISION_PACKET_PREP_TARGET_ID:
        failures.append("write_decision_packet_prep_target_id_wrong")

    for key in FORBIDDEN_FALSE_KEYS:
        require_false(review_summary, key, failures, "review_summary")

    if prep_target.get("target_status") != "READY":
        failures.append(f"prep_target_status_wrong:{prep_target.get('target_status')}")
    if prep_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"prep_target_next_wrong:{prep_target.get('next_unit_id')}")
    if prep_target.get("schema_archive_write_human_decision_packet_prep_target_id") != WRITE_DECISION_PACKET_PREP_TARGET_ID:
        failures.append("prep_target_id_wrong")
    if prep_target.get("human_decision_required_before_write") is not True:
        failures.append("prep_target_human_decision_required_not_true")
    if prep_target.get("schema_archive_mutation_target_review_pass") is not True:
        failures.append("prep_target_review_pass_not_true")
    for key in ["schema_archive_mutation_authorized", "schema_mutation_authorized", "schema_archive_write_authorized", "schema_archive_write_executed"]:
        require_false(prep_target, key, failures, "prep_target")

    if source_chain_review.get("review_status") != "PASS":
        failures.append("source_chain_review_not_pass")
    if archive_entry_review.get("review_status") != "PASS":
        failures.append("archive_entry_review_not_pass")
    if mutation_plan_review.get("review_status") != "PASS":
        failures.append("mutation_plan_review_not_pass")
    if mutation_preconditions_review.get("review_status") != "PASS":
        failures.append("mutation_preconditions_review_not_pass")
    if authority_boundary_review.get("review_status") != "PASS":
        failures.append("authority_boundary_review_not_pass")
    if negative_control_review.get("review_status") != "PASS":
        failures.append("negative_control_review_not_pass")

    for obj_name, obj in [
        ("authority_boundary_review", authority_boundary_review),
        ("negative_control_review", negative_control_review),
    ]:
        for key in FORBIDDEN_FALSE_KEYS:
            if key in obj:
                require_false(obj, key, failures, obj_name)

    if archive_entry_candidate.get("archive_entry_candidate_id") != ARCHIVE_ENTRY_CANDIDATE_ID:
        failures.append("archive_entry_candidate_id_mismatch")
    if archive_entry_candidate.get("entry_status") != "CANDIDATE_ONLY_NOT_WRITTEN":
        failures.append(f"archive_entry_status_wrong:{archive_entry_candidate.get('entry_status')}")
    if archive_entry_candidate.get("archive_write_status") != "NOT_WRITTEN":
        failures.append(f"archive_write_status_wrong:{archive_entry_candidate.get('archive_write_status')}")
    if archive_entry_candidate.get("schema_archive_write_executed") is not False:
        failures.append("archive_entry_write_executed_unexpected")

    if mutation_plan.get("planned_operation") != "ADD_SCHEMA_ENTRY_CANDIDATE_TO_SCHEMA_ARCHIVE":
        failures.append(f"mutation_plan_operation_wrong:{mutation_plan.get('planned_operation')}")
    if mutation_plan.get("write_executed_now") is not False:
        failures.append("mutation_plan_write_executed_now_unexpected")
    if mutation_plan.get("schema_archive_write_authorized") is not False:
        failures.append("mutation_plan_write_authorized_unexpected")

    if mutation_summary.get("schema_archive_mutation_target_prepared") is not True:
        failures.append("mutation_summary_target_prepared_not_true")
    if accept_summary.get("schema_archive_mutation_target_prep_authorized") is not True:
        failures.append("accept_summary_target_prep_not_authorized")

    if schema_candidate.get("schema_candidate_status") != "BUILT_CANDIDATE_ONLY_NOT_ARCHIVE_MUTATION":
        failures.append(f"schema_candidate_status_wrong:{schema_candidate.get('schema_candidate_status')}")
    if schema_candidate.get("schema_name") != SCHEMA_NAME:
        failures.append(f"schema_candidate_name_wrong:{schema_candidate.get('schema_name')}")
    if schema_candidate.get("archive_mutation_authorized") is not False:
        failures.append("schema_candidate_archive_mutation_authorized_unexpected")
    if schema_candidate_snapshot.get("snapshot_status") != "BOUND_FOR_REVIEW":
        failures.append(f"schema_snapshot_status_wrong:{schema_candidate_snapshot.get('snapshot_status')}")
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
        "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_PACKET_PASS_DECISION_REQUIRED"
        if gate == "PASS"
        else "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_PACKET_GATE_FAIL"
    )

    write_decision_packet_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_" + sig8({
        "mutation_target_review_id": MUTATION_TARGET_REVIEW_ID,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "schema_name": SCHEMA_NAME,
        "decision_options": DECISION_OPTIONS,
    })

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    basis = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_basis_v0",
        "unit_id": UNIT_ID,
        "write_decision_packet_id": write_decision_packet_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_mutation_target_review_receipt_id": MUTATION_TARGET_REVIEW_RECEIPT_ID,
        "source_mutation_target_review_id": MUTATION_TARGET_REVIEW_ID,
        "source_write_decision_packet_prep_target_id": WRITE_DECISION_PACKET_PREP_TARGET_ID,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "schema_name": SCHEMA_NAME,
        "prep_claim": "Prepare human decision packet for schema archive write only. Do not authorize, execute, or perform schema archive write.",
        "source_file_hashes": source_hashes,
    }

    source_chain_binding = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_source_chain_binding_v0",
        "write_decision_packet_id": write_decision_packet_id,
        "binding_status": "PASS" if gate == "PASS" else "BLOCKED",
        "proposal_id": PROPOSAL_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "accept_decision_record_id": ACCEPT_DECISION_RECORD_ID,
        "accept_decision_receipt_id": ACCEPT_DECISION_RECEIPT_ID,
        "mutation_target_review_id": MUTATION_TARGET_REVIEW_ID,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "source_chain_review_pass": True if gate == "PASS" else False,
    }

    write_scope = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_scope_v0",
        "write_decision_packet_id": write_decision_packet_id,
        "scope_status": "READY_FOR_HUMAN_DECISION" if gate == "PASS" else "BLOCKED",
        "decision_question": "Authorize the bounded schema archive write for the reviewed archive-entry candidate?",
        "in_scope": [
            "present reviewed mutation target",
            "present archive-entry candidate",
            "present write decision options",
            "stop for human write decision",
        ],
        "not_in_scope": [
            "schema archive write execution",
            "schema archive mutation execution",
            "schema mutation without later recorded decision",
            "runtime adoption",
            "runtime patch",
            "move addition",
            "fixture expansion",
            "T6 live case execution",
            "C8 authorization",
        ],
    }

    write_payload_binding = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_payload_binding_v0",
        "write_decision_packet_id": write_decision_packet_id,
        "binding_status": "READY_FOR_HUMAN_DECISION" if gate == "PASS" else "BLOCKED",
        "schema_name": SCHEMA_NAME,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "archive_entry_candidate_ref": rel(ARCHIVE_ENTRY_CANDIDATE_PATH),
        "mutation_plan_ref": rel(MUTATION_PLAN_PATH),
        "schema_candidate_snapshot_ref": rel(SCHEMA_CANDIDATE_SNAPSHOT_PATH),
        "planned_operation": mutation_plan.get("planned_operation"),
        "archive_entry_status": archive_entry_candidate.get("entry_status"),
        "archive_write_status": archive_entry_candidate.get("archive_write_status"),
        "write_payload_ready_for_decision": True if gate == "PASS" else False,
        "schema_archive_write_authorized": False,
        "schema_archive_write_executed": False,
    }

    authority_boundary = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authority_boundary_v0",
        "write_decision_packet_id": write_decision_packet_id,
        "boundary_status": "READY_FOR_HUMAN_DECISION" if gate == "PASS" else "BLOCKED",
        "human_schema_archive_write_decision_required": True if gate == "PASS" else False,
        "human_schema_archive_write_decision_taken": False,
        "selected_schema_archive_write_decision": None,
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
        "boundary_rule": "This packet asks for human write authorization. It does not itself authorize or execute the schema archive write.",
    }

    decision_options = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_decision_options_v0",
        "write_decision_packet_id": write_decision_packet_id,
        "options_status": "READY_FOR_HUMAN_DECISION" if gate == "PASS" else "BLOCKED",
        "selected_schema_archive_write_decision": None,
        "decision_options": [
            {
                "decision": "AUTHORIZE_SCHEMA_ARCHIVE_WRITE_FOR_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY",
                "meaning": "Authorize the next bounded schema archive write execution unit for this reviewed archive-entry candidate.",
                "does_not_write_schema_archive_now": True,
            },
            {
                "decision": "DEFER_SCHEMA_ARCHIVE_WRITE_DECISION",
                "meaning": "Keep the write path open without authorizing execution.",
                "does_not_write_schema_archive_now": True,
            },
            {
                "decision": "REJECT_SCHEMA_ARCHIVE_WRITE",
                "meaning": "Reject this schema archive write.",
                "does_not_write_schema_archive_now": True,
            },
            {
                "decision": "CLOSE_SCHEMA_ARCHIVE_WRITE_PATH_NO_WRITE",
                "meaning": "Close this write path without schema archive mutation.",
                "does_not_write_schema_archive_now": True,
            },
        ],
    }

    decision_effects_map = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_decision_effects_map_v0",
        "write_decision_packet_id": write_decision_packet_id,
        "effects_status": "READY_FOR_HUMAN_DECISION" if gate == "PASS" else "BLOCKED",
        "effect_rule": "Only a later recorded human decision may authorize the next bounded write unit. This packet performs no write.",
        "decision_effects": {
            "AUTHORIZE_SCHEMA_ARCHIVE_WRITE_FOR_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY": {
                "next_surface": "record write authorization and prepare bounded schema archive write execution target",
                "schema_archive_write_authorized_by_packet": False,
                "schema_archive_write_executed_by_packet": False,
                "requires_later_recorded_human_decision": True,
            },
            "DEFER_SCHEMA_ARCHIVE_WRITE_DECISION": {
                "next_surface": "defer/hold",
                "schema_archive_write_authorized": False,
                "schema_archive_write_executed": False,
            },
            "REJECT_SCHEMA_ARCHIVE_WRITE": {
                "next_surface": "reject write",
                "schema_archive_write_authorized": False,
                "schema_archive_write_executed": False,
            },
            "CLOSE_SCHEMA_ARCHIVE_WRITE_PATH_NO_WRITE": {
                "next_surface": "close no-write",
                "schema_archive_write_authorized": False,
                "schema_archive_write_executed": False,
            },
        },
    }

    authorize_option = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_option_authorize_v0",
        "write_decision_packet_id": write_decision_packet_id,
        "option": "AUTHORIZE_SCHEMA_ARCHIVE_WRITE_FOR_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY",
        "option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
        "selected": False,
        "would_authorize_later": "bounded schema archive write execution target",
        "schema_archive_write_authorized_now": False,
        "schema_archive_write_executed_now": False,
    }

    defer_option = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_option_defer_v0",
        "write_decision_packet_id": write_decision_packet_id,
        "option": "DEFER_SCHEMA_ARCHIVE_WRITE_DECISION",
        "option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
        "selected": False,
        "schema_archive_write_authorized": False,
        "schema_archive_write_executed": False,
    }

    reject_option = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_option_reject_v0",
        "write_decision_packet_id": write_decision_packet_id,
        "option": "REJECT_SCHEMA_ARCHIVE_WRITE",
        "option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
        "selected": False,
        "schema_archive_write_authorized": False,
        "schema_archive_write_executed": False,
    }

    close_option = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_option_close_no_write_v0",
        "write_decision_packet_id": write_decision_packet_id,
        "option": "CLOSE_SCHEMA_ARCHIVE_WRITE_PATH_NO_WRITE",
        "option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
        "selected": False,
        "schema_archive_write_authorized": False,
        "schema_archive_write_executed": False,
    }

    request_packet = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_request_packet_v0",
        "packet_status": "READY_FOR_HUMAN_DECISION" if gate == "PASS" else "BLOCKED",
        "write_decision_packet_id": write_decision_packet_id,
        "mutation_target_review_id": MUTATION_TARGET_REVIEW_ID,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "schema_name": SCHEMA_NAME,
        "archive_entry_candidate_ref": rel(ARCHIVE_ENTRY_CANDIDATE_PATH),
        "mutation_plan_ref": rel(MUTATION_PLAN_PATH),
        "decision_question": "Authorize the bounded schema archive write for this reviewed schema archive entry candidate?",
        "available_decisions": DECISION_OPTIONS,
        "selected_schema_archive_write_decision": None,
        "human_schema_archive_write_decision_taken": False,
        "decision_boundary": "This packet requests a write decision only. It does not authorize or execute the schema archive write.",
        "must_remain_false_until_recorded_decision": FORBIDDEN_FALSE_KEYS,
    }

    negative_control = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_negative_control_v0",
        "write_decision_packet_id": write_decision_packet_id,
        "negative_control_status": "PASS" if gate == "PASS" else "BLOCKED",
        "human_schema_archive_write_decision_taken": False,
        "selected_schema_archive_write_decision": None,
        "zero_counters_for_this_unit": {
            "schema_archive_mutation_count": 0,
            "schema_mutation_count": 0,
            "schema_archive_write_authorization_count": 0,
            "schema_archive_write_execution_count": 0,
            "runtime_adoption_count": 0,
            "runtime_patch_count": 0,
            "move_addition_count": 0,
            "fixture_expansion_count": 0,
            "t6_live_case_execution_count": 0,
            "hidden_next_command_count": 0,
            "c8_authorization_count": 0,
        },
        "negative_control_rule": "Preparing the schema archive write decision packet is not write authorization and not write execution.",
    }

    rollup = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "write_decision_packet_id": write_decision_packet_id,
        "mutation_target_review_id": MUTATION_TARGET_REVIEW_ID,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "schema_name": SCHEMA_NAME,
        "schema_archive_write_human_decision_packet_ready": True if gate == "PASS" else False,
        "human_schema_archive_write_decision_required": True if gate == "PASS" else False,
        "human_schema_archive_write_decision_taken": False,
        "selected_schema_archive_write_decision": None,
        "available_decision_count": len(DECISION_OPTIONS) if gate == "PASS" else 0,
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
        "terminal_stop_code": STOP_CODE if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_PACKET_GATE_FAIL",
    }

    readout = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_readout_v0",
        "status": status,
        "write_decision_packet_id": write_decision_packet_id,
        "interpretation": "Schema archive write human decision packet is ready. No write authorization, schema archive write, or schema mutation occurred."
        if gate == "PASS" else "Schema archive write human decision packet preparation failed typed gates.",
        "stop_code": STOP_CODE if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_PACKET_GATE_FAIL",
    }

    profile = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_profile_v0",
        "profile_status": status,
        "write_decision_packet_id": write_decision_packet_id,
        "core_rule": "Ask for human schema archive write authorization and stop. Do not authorize or execute schema archive write in this unit.",
        "human_decision_request_packet_ref": rel(REQUEST_PACKET_PATH),
        "must_not_infer": [
            "schema archive write authorized",
            "schema archive write executed",
            "schema archive mutated",
            "schema promoted",
            "schema mutation authorized",
            "runtime adopted",
            "runtime patched",
            "move registry updated",
            "fixture suite expanded",
            "T6 live case executed",
            "C8 authorized",
            "human schema archive write decision taken",
        ],
    }

    report = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "packet_result": "SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_REQUIRED" if gate == "PASS" else "SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_PACKET_GATE_FAIL",
            "write_decision_packet_id": write_decision_packet_id,
            "mutation_target_review_id": MUTATION_TARGET_REVIEW_ID,
            "mutation_target_id": MUTATION_TARGET_ID,
            "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
            "schema_name": SCHEMA_NAME,
            "available_decisions": DECISION_OPTIONS if gate == "PASS" else [],
            "human_schema_archive_write_decision_taken": False,
            "selected_schema_archive_write_decision": None,
            "schema_archive_write_authorized": False,
            "schema_archive_write_executed": False,
            "schema_archive_mutation_authorized": False,
            "schema_mutation_authorized": False,
            "runtime_adoption_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "t6_live_case_execution_authorized": False,
            "c8_authorized": False,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_transition_trace_v0",
        "unit_id": UNIT_ID,
        "write_decision_packet_id": write_decision_packet_id,
        "transitions": [
            {
                "from": "SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_PACKET_PREP_READY",
                "edge": "prepare schema archive write human decision packet",
                "to": "SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_PACKET_READY" if gate == "PASS" else "SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_PACKET_GATE_FAIL",
            },
            {
                "from": "SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_PACKET_READY" if gate == "PASS" else "SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_PACKET_GATE_FAIL",
                "edge": "stop for human write decision without write authorization or execution",
                "to": "STOP_SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_REQUIRED" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "STOP",
            "next_unit_id": None,
            "stop_code": STOP_CODE if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_PACKET_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (SOURCE_CHAIN_BINDING_PATH, source_chain_binding),
        (WRITE_SCOPE_PATH, write_scope),
        (WRITE_PAYLOAD_BINDING_PATH, write_payload_binding),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (DECISION_OPTIONS_PATH, decision_options),
        (DECISION_EFFECTS_MAP_PATH, decision_effects_map),
        (AUTHORIZE_OPTION_PATH, authorize_option),
        (DEFER_OPTION_PATH, defer_option),
        (REJECT_OPTION_PATH, reject_option),
        (CLOSE_OPTION_PATH, close_option),
        (REQUEST_PACKET_PATH, request_packet),
        (NEGATIVE_CONTROL_PATH, negative_control),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "MUTATION_TARGET_REVIEW_RECEIPT_CONSUMED",
        "WRITE_HUMAN_DECISION_PACKET_PREP_TARGET_CONSUMED",
        "WRITE_PAYLOAD_BOUND",
        "WRITE_DECISION_OPTIONS_EMITTED",
        "WRITE_DECISION_EFFECTS_MAP_EMITTED",
        "WRITE_HUMAN_DECISION_REQUEST_PACKET_READY",
        "NEGATIVE_CONTROL_PASS",
        "STOP_SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_REQUIRED",
        "NO_HUMAN_SCHEMA_ARCHIVE_WRITE_DECISION_TAKEN",
        "NO_SELECTED_SCHEMA_ARCHIVE_WRITE_DECISION",
        "NO_SCHEMA_ARCHIVE_WRITE_AUTHORIZATION",
        "NO_SCHEMA_ARCHIVE_WRITE_EXECUTION",
        "NO_SCHEMA_ARCHIVE_MUTATION",
        "NO_SCHEMA_MUTATION_EXECUTION",
        "NO_RUNTIME_ADOPTION_AUTHORITY",
        "NO_RUNTIME_PATCH",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION",
        "NO_T6_LIVE_CASE_EXECUTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_PACKET_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "write_decision_packet_id": write_decision_packet_id,
        "source_mutation_target_review_receipt_id": MUTATION_TARGET_REVIEW_RECEIPT_ID,
        "source_mutation_target_review_receipt_ref": rel(MUTATION_TARGET_REVIEW_RECEIPT_PATH),
        "mutation_target_review_id": MUTATION_TARGET_REVIEW_ID,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
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
            "SCHEMA_ARCHIVE_WRITE_PACKET_0_REVIEW_RECEIPT_CONSUMED": gate == "PASS",
            "SCHEMA_ARCHIVE_WRITE_PACKET_1_PREP_TARGET_CONSUMED": gate == "PASS",
            "SCHEMA_ARCHIVE_WRITE_PACKET_2_SOURCE_CHAIN_BOUND": SOURCE_CHAIN_BINDING_PATH.exists() and gate == "PASS",
            "SCHEMA_ARCHIVE_WRITE_PACKET_3_WRITE_PAYLOAD_BOUND": WRITE_PAYLOAD_BINDING_PATH.exists() and gate == "PASS",
            "SCHEMA_ARCHIVE_WRITE_PACKET_4_DECISION_OPTIONS_EMITTED": DECISION_OPTIONS_PATH.exists() and gate == "PASS",
            "SCHEMA_ARCHIVE_WRITE_PACKET_5_EFFECTS_MAP_EMITTED": DECISION_EFFECTS_MAP_PATH.exists() and gate == "PASS",
            "SCHEMA_ARCHIVE_WRITE_PACKET_6_REQUEST_PACKET_READY": REQUEST_PACKET_PATH.exists() and gate == "PASS",
            "SCHEMA_ARCHIVE_WRITE_PACKET_7_NEGATIVE_CONTROL_PASS": NEGATIVE_CONTROL_PATH.exists() and gate == "PASS",
            "SCHEMA_ARCHIVE_WRITE_PACKET_8_NO_HUMAN_WRITE_DECISION_TAKEN": True,
            "SCHEMA_ARCHIVE_WRITE_PACKET_9_NO_SELECTED_WRITE_DECISION": True,
            "SCHEMA_ARCHIVE_WRITE_PACKET_10_NO_SCHEMA_ARCHIVE_WRITE_AUTHORIZATION": True,
            "SCHEMA_ARCHIVE_WRITE_PACKET_11_NO_SCHEMA_ARCHIVE_WRITE_EXECUTION": True,
            "SCHEMA_ARCHIVE_WRITE_PACKET_12_NO_SCHEMA_ARCHIVE_MUTATION": True,
            "SCHEMA_ARCHIVE_WRITE_PACKET_13_NO_SCHEMA_MUTATION": True,
            "SCHEMA_ARCHIVE_WRITE_PACKET_14_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "SCHEMA_ARCHIVE_WRITE_PACKET_15_NO_RUNTIME_PATCH": True,
            "SCHEMA_ARCHIVE_WRITE_PACKET_16_NO_MOVE_ADDITION": True,
            "SCHEMA_ARCHIVE_WRITE_PACKET_17_NO_FIXTURE_EXPANSION": True,
            "SCHEMA_ARCHIVE_WRITE_PACKET_18_NO_T6_LIVE_CASE_EXECUTION": True,
            "SCHEMA_ARCHIVE_WRITE_PACKET_19_NO_C8_AUTHORIZATION": True,
            "SCHEMA_ARCHIVE_WRITE_PACKET_20_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_summary": {
            "status": status,
            "write_decision_packet_id": write_decision_packet_id,
            "source_mutation_target_review_receipt_id": MUTATION_TARGET_REVIEW_RECEIPT_ID,
            "mutation_target_review_id": MUTATION_TARGET_REVIEW_ID,
            "mutation_target_id": MUTATION_TARGET_ID,
            "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
            "schema_name": SCHEMA_NAME,
            "schema_archive_write_human_decision_packet_ready": True if gate == "PASS" else False,
            "human_schema_archive_write_decision_required": True if gate == "PASS" else False,
            "human_schema_archive_write_decision_taken": False,
            "selected_schema_archive_write_decision": None,
            "available_decisions": DECISION_OPTIONS if gate == "PASS" else [],
            "available_decision_count": len(DECISION_OPTIONS) if gate == "PASS" else 0,
            "authorize_option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
            "defer_option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
            "reject_option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
            "close_no_write_option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
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
            "next_unit_id": None,
            "terminal_stop_code": transition_trace["terminal"]["stop_code"],
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "source_chain_binding": rel(SOURCE_CHAIN_BINDING_PATH),
            "write_scope": rel(WRITE_SCOPE_PATH),
            "write_payload_binding": rel(WRITE_PAYLOAD_BINDING_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "decision_options": rel(DECISION_OPTIONS_PATH),
            "decision_effects_map": rel(DECISION_EFFECTS_MAP_PATH),
            "authorize_option": rel(AUTHORIZE_OPTION_PATH),
            "defer_option": rel(DEFER_OPTION_PATH),
            "reject_option": rel(REJECT_OPTION_PATH),
            "close_option": rel(CLOSE_OPTION_PATH),
            "request_packet": rel(REQUEST_PACKET_PATH),
            "negative_control": rel(NEGATIVE_CONTROL_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_receipt_id={receipt_id}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_receipt_path={rel(receipt_path)}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_id={write_decision_packet_id if gate == 'PASS' else 'NONE'}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_terminal_stop_code={transition_trace['terminal']['stop_code']}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
