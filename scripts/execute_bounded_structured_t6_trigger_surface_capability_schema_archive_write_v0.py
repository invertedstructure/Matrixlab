#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "EXECUTE_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_V0"
TARGET_UNIT_ID = "bounded_structured_t6_trigger_surface_capability.schema_archive_write_execution_v0"
NEXT_UNIT_ID = None

WRITE_AUTHORIZE_RECEIPT_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_receipt_ca58a57d"
WRITE_AUTHORIZE_DECISION_RECORD_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_5816bbd0"
WRITE_EXECUTION_TARGET_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_target_21e6df6e"
WRITE_DECISION_PACKET_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_f86a0126"
SELECTED_WRITE_DECISION = "AUTHORIZE_SCHEMA_ARCHIVE_WRITE_FOR_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY"

MUTATION_TARGET_REVIEW_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_213c76c7"
MUTATION_TARGET_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_63de098e"
ARCHIVE_ENTRY_CANDIDATE_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_entry_candidate_72e26cec"
ADOPTION_PATH_ID = "bounded_structured_t6_trigger_surface_capability_adoption_path_6f9974e5"
CAPABILITY_BUILD_ID = "bounded_structured_t6_trigger_surface_capability_build_721f09dc"
PROPOSAL_ID = "capability_proposal_57dda6e9"
SCHEMA_NAME = "bounded_structured_t6_trigger_surface_capability_v0"
REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"

WRITE_AUTHORIZE_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_v0_receipts/bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_receipt_ca58a57d.json"
WRITE_EXECUTION_TARGET_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_target_v0.json"
WRITE_AUTHORIZE_DECISION_RECORD_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_human_decision_record_v0.json"
WRITE_AUTHORIZATION_EFFECT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorization_effect_applied_v0.json"
WRITE_AUTHORIZE_BOUNDARY_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_authority_boundary_review_v0.json"
WRITE_AUTHORIZE_NEGATIVE_CONTROL_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_negative_control_v0.json"

WRITE_PACKET_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_v0_receipts/bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_receipt_422cdd89.json"
MUTATION_TARGET_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_v0_receipts/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_receipt_e8f12c97.json"
MUTATION_TARGET_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0_receipts/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_receipt_2063a180.json"

ARCHIVE_ENTRY_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_entry_candidate_v0.json"
MUTATION_PLAN_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_plan_v0.json"
SCHEMA_CANDIDATE_SNAPSHOT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_schema_candidate_snapshot_v0.json"

SCHEMA_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_schema_candidate_v0.json"
CAPABILITY_PROFILE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_profile_v0.json"
EVIDENCE_SHAPE_CONTRACT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_evidence_shape_contract_v0.json"
CLASSIFIER_POLICY_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_classifier_policy_v0.json"
API_CONTRACT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_api_contract_v0.json"
TEST_EXPECTATIONS_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_test_expectations_v0.json"

BUILD_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_receipt_9f1f0079.json"
BUILD_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_review_receipt_b8dba552.json"
PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"

SCHEMA_ARCHIVE_PATH = ROOT / "data/schema_archive/bounded_trigger_surface_capability_schema_archive_v0.json"

OUT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_v0"
RECEIPT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_basis_v0.json"
PRE_WRITE_ARCHIVE_STATE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_pre_write_state_v0.json"
WRITE_PAYLOAD_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_payload_v0.json"
ARCHIVE_ENTRY_WRITTEN_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_entry_written_v0.json"
POST_WRITE_ARCHIVE_STATE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_post_write_state_v0.json"
ARCHIVE_DELTA_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_delta_v0.json"
WRITE_VERIFICATION_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_verification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_authority_boundary_v0.json"
NEGATIVE_CONTROL_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_negative_control_v0.json"
READOUT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_transition_trace.json"

FORBIDDEN_RUNTIME_FALSE_KEYS = [
    "schema_mutation_authorized",
    "schema_mutation_executed",
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

def obj_sha256(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def require_false(obj: Dict[str, Any], key: str, failures: List[str], prefix: str) -> None:
    if obj.get(key) is not False:
        failures.append(f"{prefix}_{key}_not_false:{obj.get(key)}")

def require_true(obj: Dict[str, Any], key: str, failures: List[str], prefix: str) -> None:
    if obj.get(key) is not True:
        failures.append(f"{prefix}_{key}_not_true:{obj.get(key)}")

def empty_archive() -> Dict[str, Any]:
    return {
        "schema_version": "bounded_trigger_surface_capability_schema_archive_v0",
        "archive_kind": "schema_archive",
        "archive_family": "bounded_trigger_surface_capability_schema",
        "archive_status": "ACTIVE",
        "created_at": now_iso(),
        "last_updated_at": None,
        "entries": {},
        "entry_order": [],
        "write_receipts": [],
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    SCHEMA_ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)

    required_files = [
        WRITE_AUTHORIZE_RECEIPT_PATH,
        WRITE_EXECUTION_TARGET_PATH,
        WRITE_AUTHORIZE_DECISION_RECORD_PATH,
        WRITE_AUTHORIZATION_EFFECT_PATH,
        WRITE_AUTHORIZE_BOUNDARY_PATH,
        WRITE_AUTHORIZE_NEGATIVE_CONTROL_PATH,
        WRITE_PACKET_RECEIPT_PATH,
        MUTATION_TARGET_REVIEW_RECEIPT_PATH,
        MUTATION_TARGET_RECEIPT_PATH,
        ARCHIVE_ENTRY_CANDIDATE_PATH,
        MUTATION_PLAN_PATH,
        SCHEMA_CANDIDATE_SNAPSHOT_PATH,
        SCHEMA_CANDIDATE_PATH,
        CAPABILITY_PROFILE_PATH,
        EVIDENCE_SHAPE_CONTRACT_PATH,
        CLASSIFIER_POLICY_PATH,
        API_CONTRACT_PATH,
        TEST_EXPECTATIONS_PATH,
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

    write_auth_receipt = read_json(WRITE_AUTHORIZE_RECEIPT_PATH)
    execution_target = read_json(WRITE_EXECUTION_TARGET_PATH)
    decision_record = read_json(WRITE_AUTHORIZE_DECISION_RECORD_PATH)
    authorization_effect = read_json(WRITE_AUTHORIZATION_EFFECT_PATH)
    authorize_boundary = read_json(WRITE_AUTHORIZE_BOUNDARY_PATH)
    authorize_negative = read_json(WRITE_AUTHORIZE_NEGATIVE_CONTROL_PATH)

    write_packet_receipt = read_json(WRITE_PACKET_RECEIPT_PATH)
    review_receipt = read_json(MUTATION_TARGET_REVIEW_RECEIPT_PATH)
    mutation_receipt = read_json(MUTATION_TARGET_RECEIPT_PATH)

    archive_entry_candidate = read_json(ARCHIVE_ENTRY_CANDIDATE_PATH)
    mutation_plan = read_json(MUTATION_PLAN_PATH)
    schema_candidate_snapshot = read_json(SCHEMA_CANDIDATE_SNAPSHOT_PATH)

    schema_candidate = read_json(SCHEMA_CANDIDATE_PATH)
    capability_profile = read_json(CAPABILITY_PROFILE_PATH)
    evidence_shape_contract = read_json(EVIDENCE_SHAPE_CONTRACT_PATH)
    classifier_policy = read_json(CLASSIFIER_POLICY_PATH)
    api_contract = read_json(API_CONTRACT_PATH)
    test_expectations = read_json(TEST_EXPECTATIONS_PATH)

    build_receipt = read_json(BUILD_RECEIPT_PATH)
    build_review_receipt = read_json(BUILD_REVIEW_RECEIPT_PATH)
    proposal = read_json(PROPOSAL_PATH)

    write_auth_summary = write_auth_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_summary", {})
    write_packet_summary = write_packet_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_summary", {})
    review_summary = review_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_summary", {})
    mutation_summary = mutation_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_summary", {})
    build_summary = build_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_summary", {})
    build_review_summary = build_review_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_review_summary", {})

    if write_auth_receipt.get("receipt_id") != WRITE_AUTHORIZE_RECEIPT_ID:
        failures.append(f"write_auth_receipt_id_wrong:{write_auth_receipt.get('receipt_id')}")
    if write_auth_receipt.get("gate") != "PASS":
        failures.append("write_auth_receipt_gate_not_pass")
    if write_auth_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append(f"write_auth_terminal_next_wrong:{write_auth_receipt.get('terminal', {}).get('next_unit_id')}")

    for key in [
        "human_schema_archive_write_decision_taken",
        "schema_archive_write_authorized",
        "schema_archive_mutation_authorized",
        "schema_archive_write_execution_target_ready",
    ]:
        require_true(write_auth_summary, key, failures, "write_auth_summary")

    if write_auth_summary.get("selected_schema_archive_write_decision") != SELECTED_WRITE_DECISION:
        failures.append(f"selected_decision_wrong:{write_auth_summary.get('selected_schema_archive_write_decision')}")
    if write_auth_summary.get("write_authorize_decision_record_id") != WRITE_AUTHORIZE_DECISION_RECORD_ID:
        failures.append("write_authorize_decision_record_id_wrong")
    if write_auth_summary.get("schema_archive_write_execution_target_id") != WRITE_EXECUTION_TARGET_ID:
        failures.append("write_execution_target_id_wrong")
    if write_auth_summary.get("schema_archive_write_executed") is not False:
        failures.append("write_auth_summary_write_already_executed")
    if write_auth_summary.get("schema_archive_mutation_executed") is not False:
        failures.append("write_auth_summary_mutation_already_executed")

    for key in FORBIDDEN_RUNTIME_FALSE_KEYS:
        require_false(write_auth_summary, key, failures, "write_auth_summary")

    if execution_target.get("target_status") != "READY":
        failures.append(f"execution_target_status_wrong:{execution_target.get('target_status')}")
    if execution_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"execution_target_next_wrong:{execution_target.get('next_unit_id')}")
    if execution_target.get("schema_archive_write_execution_target_id") != WRITE_EXECUTION_TARGET_ID:
        failures.append("execution_target_id_mismatch")
    if execution_target.get("write_authorize_decision_record_id") != WRITE_AUTHORIZE_DECISION_RECORD_ID:
        failures.append("execution_target_record_id_mismatch")
    if execution_target.get("schema_archive_write_authorized") is not True:
        failures.append("execution_target_write_not_authorized")
    if execution_target.get("schema_archive_mutation_authorized") is not True:
        failures.append("execution_target_mutation_not_authorized")
    if execution_target.get("schema_archive_write_executed") is not False:
        failures.append("execution_target_write_already_executed")
    if execution_target.get("schema_archive_mutation_executed") is not False:
        failures.append("execution_target_mutation_already_executed")
    if execution_target.get("must_fail_if_archive_entry_already_exists") is not True:
        failures.append("execution_target_duplicate_guard_missing")
    if execution_target.get("must_emit_write_receipt") is not True:
        failures.append("execution_target_receipt_guard_missing")
    if execution_target.get("planned_schema_archive_ref") != rel(SCHEMA_ARCHIVE_PATH):
        failures.append(f"execution_target_archive_ref_wrong:{execution_target.get('planned_schema_archive_ref')}")
    if execution_target.get("planned_operation") != "ADD_SCHEMA_ENTRY_CANDIDATE_TO_SCHEMA_ARCHIVE":
        failures.append(f"execution_target_operation_wrong:{execution_target.get('planned_operation')}")

    if decision_record.get("decision_record_status") != "HUMAN_SCHEMA_ARCHIVE_WRITE_DECISION_RECORDED":
        failures.append("decision_record_status_wrong")
    if decision_record.get("selected_schema_archive_write_decision") != SELECTED_WRITE_DECISION:
        failures.append("decision_record_selected_decision_wrong")
    if authorization_effect.get("schema_archive_write_authorized") is not True:
        failures.append("authorization_effect_write_not_authorized")
    if authorization_effect.get("schema_archive_mutation_authorized") is not True:
        failures.append("authorization_effect_mutation_not_authorized")
    if authorization_effect.get("schema_archive_write_execution_target_ready") is not True:
        failures.append("authorization_effect_execution_target_not_ready")
    if authorization_effect.get("schema_archive_write_executed") is not False:
        failures.append("authorization_effect_write_executed_unexpected")
    if authorization_effect.get("schema_archive_mutation_executed") is not False:
        failures.append("authorization_effect_mutation_executed_unexpected")

    if authorize_boundary.get("review_status") != "PASS":
        failures.append("authorize_boundary_not_pass")
    if authorize_negative.get("negative_control_status") != "PASS":
        failures.append("authorize_negative_not_pass")
    zero = authorize_negative.get("zero_counters_for_this_unit") or {}
    for key in [
        "schema_archive_write_execution_count",
        "schema_archive_mutation_execution_count",
        "schema_content_mutation_count",
        "runtime_adoption_count",
        "runtime_patch_count",
        "move_addition_count",
        "fixture_expansion_count",
        "t6_live_case_execution_count",
        "hidden_next_command_count",
        "c8_authorization_count",
    ]:
        if zero.get(key) != 0:
            failures.append(f"authorize_negative_counter_wrong:{key}:{zero.get(key)}")

    if write_packet_summary.get("write_decision_packet_id") != WRITE_DECISION_PACKET_ID:
        failures.append("write_packet_id_wrong")
    if review_summary.get("schema_archive_mutation_target_review_pass") is not True:
        failures.append("review_summary_not_pass")
    if mutation_summary.get("schema_archive_mutation_target_prepared") is not True:
        failures.append("mutation_summary_target_not_prepared")

    if archive_entry_candidate.get("archive_entry_candidate_id") != ARCHIVE_ENTRY_CANDIDATE_ID:
        failures.append("archive_entry_candidate_id_mismatch")
    if archive_entry_candidate.get("entry_status") != "CANDIDATE_ONLY_NOT_WRITTEN":
        failures.append(f"archive_entry_status_wrong:{archive_entry_candidate.get('entry_status')}")
    if archive_entry_candidate.get("archive_write_status") != "NOT_WRITTEN":
        failures.append(f"archive_write_status_wrong:{archive_entry_candidate.get('archive_write_status')}")
    if archive_entry_candidate.get("schema_name") != SCHEMA_NAME:
        failures.append(f"archive_entry_schema_name_wrong:{archive_entry_candidate.get('schema_name')}")

    if mutation_plan.get("planned_operation") != "ADD_SCHEMA_ENTRY_CANDIDATE_TO_SCHEMA_ARCHIVE":
        failures.append(f"mutation_plan_operation_wrong:{mutation_plan.get('planned_operation')}")
    if mutation_plan.get("planned_archive_key") != SCHEMA_NAME:
        failures.append(f"mutation_plan_archive_key_wrong:{mutation_plan.get('planned_archive_key')}")
    if mutation_plan.get("write_executed_now") is not False:
        failures.append("mutation_plan_write_already_executed")

    if schema_candidate_snapshot.get("snapshot_status") != "BOUND_FOR_REVIEW":
        failures.append(f"schema_snapshot_status_wrong:{schema_candidate_snapshot.get('snapshot_status')}")
    if schema_candidate.get("schema_name") != SCHEMA_NAME:
        failures.append(f"schema_candidate_name_wrong:{schema_candidate.get('schema_name')}")
    if schema_candidate.get("schema_candidate_status") != "BUILT_CANDIDATE_ONLY_NOT_ARCHIVE_MUTATION":
        failures.append(f"schema_candidate_status_wrong:{schema_candidate.get('schema_candidate_status')}")
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

    archive_existed_before = SCHEMA_ARCHIVE_PATH.exists()
    if archive_existed_before:
        archive_before = read_json(SCHEMA_ARCHIVE_PATH)
        archive_before_sha256 = file_sha256(SCHEMA_ARCHIVE_PATH)
    else:
        archive_before = None
        archive_before_sha256 = None

    working_archive = copy.deepcopy(archive_before) if archive_before is not None else empty_archive()

    if not isinstance(working_archive, dict):
        failures.append("archive_before_not_object")
    else:
        if working_archive.get("schema_version") != "bounded_trigger_surface_capability_schema_archive_v0":
            failures.append(f"archive_schema_version_wrong:{working_archive.get('schema_version')}")
        if working_archive.get("archive_kind") != "schema_archive":
            failures.append(f"archive_kind_wrong:{working_archive.get('archive_kind')}")
        if working_archive.get("archive_family") != "bounded_trigger_surface_capability_schema":
            failures.append(f"archive_family_wrong:{working_archive.get('archive_family')}")
        if not isinstance(working_archive.get("entries"), dict):
            failures.append("archive_entries_not_object")
        if not isinstance(working_archive.get("entry_order"), list):
            failures.append("archive_entry_order_not_list")
        if not isinstance(working_archive.get("write_receipts"), list):
            failures.append("archive_write_receipts_not_list")

    if not failures:
        if SCHEMA_NAME in working_archive["entries"]:
            failures.append(f"archive_entry_already_exists:{SCHEMA_NAME}")
        if SCHEMA_NAME in working_archive["entry_order"]:
            failures.append(f"archive_entry_order_already_contains:{SCHEMA_NAME}")

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_EXECUTION_PASS_ARCHIVE_ENTRY_WRITTEN"
        if gate == "PASS"
        else "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_EXECUTION_GATE_FAIL"
    )

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    schema_candidate_sha256 = file_sha256(SCHEMA_CANDIDATE_PATH)
    schema_candidate_snapshot_sha256 = file_sha256(SCHEMA_CANDIDATE_SNAPSHOT_PATH)
    archive_entry_candidate_sha256 = file_sha256(ARCHIVE_ENTRY_CANDIDATE_PATH)

    archive_write_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_write_" + sig8({
        "write_authorize_decision_record_id": WRITE_AUTHORIZE_DECISION_RECORD_ID,
        "write_execution_target_id": WRITE_EXECUTION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "schema_name": SCHEMA_NAME,
        "archive_before_sha256": archive_before_sha256,
    })

    entry_payload = {
        "schema_version": "bounded_trigger_surface_capability_schema_archive_entry_v0",
        "archive_write_id": archive_write_id,
        "schema_name": SCHEMA_NAME,
        "capability_name": REQUIRED_CAPABILITY,
        "entry_status": "ARCHIVED",
        "authorized_scope": "bounded_trigger_surface_capability_schema",
        "authorized_trigger_object_family": "bounded_structured_t6_trigger_surface_capability",
        "authorization_boundary": "Reusable only for the bounded trigger surface capability schema family unless later validator/human authority expands it.",
        "source_schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
        "source_schema_candidate_sha256": schema_candidate_sha256,
        "source_schema_candidate_snapshot_ref": rel(SCHEMA_CANDIDATE_SNAPSHOT_PATH),
        "source_schema_candidate_snapshot_sha256": schema_candidate_snapshot_sha256,
        "source_archive_entry_candidate_ref": rel(ARCHIVE_ENTRY_CANDIDATE_PATH),
        "source_archive_entry_candidate_sha256": archive_entry_candidate_sha256,
        "source_capability_profile_ref": rel(CAPABILITY_PROFILE_PATH),
        "source_evidence_shape_contract_ref": rel(EVIDENCE_SHAPE_CONTRACT_PATH),
        "source_classifier_policy_ref": rel(CLASSIFIER_POLICY_PATH),
        "source_api_contract_ref": rel(API_CONTRACT_PATH),
        "source_test_expectations_ref": rel(TEST_EXPECTATIONS_PATH),
        "source_write_authorize_decision_record_id": WRITE_AUTHORIZE_DECISION_RECORD_ID,
        "source_write_authorize_receipt_id": WRITE_AUTHORIZE_RECEIPT_ID,
        "source_write_decision_packet_id": WRITE_DECISION_PACKET_ID,
        "source_mutation_target_review_id": MUTATION_TARGET_REVIEW_ID,
        "source_mutation_target_id": MUTATION_TARGET_ID,
        "source_archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "source_capability_build_id": CAPABILITY_BUILD_ID,
        "source_proposal_id": PROPOSAL_ID,
        "created_at": now_iso(),
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "c8_authorized": False,
    }

    write_payload = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_payload_v0",
        "archive_write_id": archive_write_id,
        "write_execution_target_id": WRITE_EXECUTION_TARGET_ID,
        "schema_name": SCHEMA_NAME,
        "planned_schema_archive_ref": rel(SCHEMA_ARCHIVE_PATH),
        "planned_operation": "ADD_SCHEMA_ENTRY_CANDIDATE_TO_SCHEMA_ARCHIVE",
        "entry_payload": entry_payload,
    }

    if gate == "PASS":
        working_archive["entries"][SCHEMA_NAME] = entry_payload
        working_archive["entry_order"].append(SCHEMA_NAME)
        working_archive["last_updated_at"] = now_iso()
        working_archive["write_receipts"].append({
            "archive_write_id": archive_write_id,
            "schema_name": SCHEMA_NAME,
            "write_authorize_decision_record_id": WRITE_AUTHORIZE_DECISION_RECORD_ID,
            "source_write_authorize_receipt_id": WRITE_AUTHORIZE_RECEIPT_ID,
            "receipt_pending": True,
        })

        pre_state = {
            "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_pre_write_state_v0",
            "archive_existed_before": archive_existed_before,
            "archive_ref": rel(SCHEMA_ARCHIVE_PATH),
            "archive_before_sha256": archive_before_sha256,
            "entry_existed_before": False,
            "entry_count_before": 0 if archive_before is None else len(archive_before.get("entries", {})),
        }
        write_json(PRE_WRITE_ARCHIVE_STATE_PATH, pre_state)
        write_json(WRITE_PAYLOAD_PATH, write_payload)

        write_json(SCHEMA_ARCHIVE_PATH, working_archive)
        archive_after = read_json(SCHEMA_ARCHIVE_PATH)
        archive_after_sha256 = file_sha256(SCHEMA_ARCHIVE_PATH)

        entry_written = archive_after.get("entries", {}).get(SCHEMA_NAME)
        archive_write_executed = isinstance(entry_written, dict) and entry_written.get("archive_write_id") == archive_write_id
        archive_entry_written = archive_write_executed and SCHEMA_NAME in archive_after.get("entry_order", [])
        duplicate_count = archive_after.get("entry_order", []).count(SCHEMA_NAME)

        post_state = {
            "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_post_write_state_v0",
            "archive_ref": rel(SCHEMA_ARCHIVE_PATH),
            "archive_after_sha256": archive_after_sha256,
            "entry_exists_after": archive_entry_written,
            "entry_count_after": len(archive_after.get("entries", {})),
            "entry_order_count_for_schema": duplicate_count,
            "archive_write_executed": archive_write_executed,
        }

        archive_delta = {
            "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_delta_v0",
            "archive_write_id": archive_write_id,
            "archive_ref": rel(SCHEMA_ARCHIVE_PATH),
            "archive_existed_before": archive_existed_before,
            "archive_before_sha256": archive_before_sha256,
            "archive_after_sha256": archive_after_sha256,
            "entry_count_before": pre_state["entry_count_before"],
            "entry_count_after": post_state["entry_count_after"],
            "delta_entry_count": post_state["entry_count_after"] - pre_state["entry_count_before"],
            "added_schema_name": SCHEMA_NAME,
            "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        }

        write_verification = {
            "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_verification_v0",
            "archive_write_id": archive_write_id,
            "verification_status": "PASS" if archive_entry_written and duplicate_count == 1 else "FAIL",
            "archive_ref": rel(SCHEMA_ARCHIVE_PATH),
            "archive_after_sha256": archive_after_sha256,
            "entry_exists_after": archive_entry_written,
            "entry_order_count_for_schema": duplicate_count,
            "entry_archive_write_id_matches": archive_write_executed,
            "schema_archive_write_executed": archive_entry_written and duplicate_count == 1,
            "schema_archive_mutation_executed": archive_entry_written and duplicate_count == 1,
        }

        if write_verification["verification_status"] != "PASS":
            failures.append("post_write_verification_failed")
            gate = "FAIL"
            status = "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_EXECUTION_POST_WRITE_VERIFY_FAIL"

    else:
        pre_state = {
            "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_pre_write_state_v0",
            "archive_existed_before": archive_existed_before,
            "archive_ref": rel(SCHEMA_ARCHIVE_PATH),
            "archive_before_sha256": archive_before_sha256,
            "entry_existed_before": SCHEMA_NAME in ((archive_before or {}).get("entries", {}) if isinstance(archive_before, dict) else {}),
            "entry_count_before": None if archive_before is None or not isinstance(archive_before, dict) else len(archive_before.get("entries", {})),
        }
        post_state = {
            "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_post_write_state_v0",
            "archive_ref": rel(SCHEMA_ARCHIVE_PATH),
            "archive_after_sha256": archive_before_sha256,
            "entry_exists_after": pre_state["entry_existed_before"],
            "entry_count_after": pre_state["entry_count_before"],
            "archive_write_executed": False,
        }
        archive_delta = {
            "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_delta_v0",
            "archive_write_id": archive_write_id,
            "archive_ref": rel(SCHEMA_ARCHIVE_PATH),
            "archive_existed_before": archive_existed_before,
            "archive_before_sha256": archive_before_sha256,
            "archive_after_sha256": archive_before_sha256,
            "delta_entry_count": 0,
            "added_schema_name": None,
            "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        }
        write_verification = {
            "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_verification_v0",
            "archive_write_id": archive_write_id,
            "verification_status": "BLOCKED",
            "archive_ref": rel(SCHEMA_ARCHIVE_PATH),
            "schema_archive_write_executed": False,
            "schema_archive_mutation_executed": False,
            "failures": failures,
        }
        write_json(PRE_WRITE_ARCHIVE_STATE_PATH, pre_state)
        write_json(WRITE_PAYLOAD_PATH, write_payload)

    archive_entry_written_obj = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_entry_written_v0",
        "archive_write_id": archive_write_id,
        "entry_written_status": "WRITTEN" if gate == "PASS" else "BLOCKED",
        "schema_name": SCHEMA_NAME if gate == "PASS" else None,
        "schema_archive_ref": rel(SCHEMA_ARCHIVE_PATH),
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "write_authorize_decision_record_id": WRITE_AUTHORIZE_DECISION_RECORD_ID,
        "schema_archive_write_authorized": gate == "PASS",
        "schema_archive_mutation_authorized": gate == "PASS",
        "schema_archive_write_executed": gate == "PASS",
        "schema_archive_mutation_executed": gate == "PASS",
        "schema_mutation_authorized": False,
        "schema_mutation_executed": False,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
    }

    authority_boundary = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_authority_boundary_v0",
        "archive_write_id": archive_write_id,
        "boundary_status": "PASS" if gate == "PASS" else "BLOCKED",
        "allowed_effect_executed": "one bounded schema archive entry write",
        "schema_archive_write_authorized": gate == "PASS",
        "schema_archive_mutation_authorized": gate == "PASS",
        "schema_archive_write_executed": gate == "PASS",
        "schema_archive_mutation_executed": gate == "PASS",
        "schema_mutation_authorized": False,
        "schema_mutation_executed": False,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
        "not_allowed_effects": [
            "schema candidate content mutation",
            "runtime adoption",
            "runtime patch",
            "move registry addition",
            "fixture expansion",
            "T6 live case execution",
            "C8 authorization",
        ],
    }

    negative_control = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_negative_control_v0",
        "archive_write_id": archive_write_id,
        "negative_control_status": "PASS" if gate == "PASS" else "BLOCKED",
        "positive_counters_for_this_unit": {
            "schema_archive_write_execution_count": 1 if gate == "PASS" else 0,
            "schema_archive_mutation_execution_count": 1 if gate == "PASS" else 0,
        },
        "zero_counters_for_this_unit": {
            "schema_content_mutation_count": 0,
            "runtime_adoption_count": 0,
            "runtime_patch_count": 0,
            "move_addition_count": 0,
            "fixture_expansion_count": 0,
            "t6_live_case_execution_count": 0,
            "hidden_next_command_count": 0,
            "c8_authorization_count": 0,
        },
        "negative_control_rule": "This unit writes only the bounded schema archive entry and does not adopt runtime behavior or mutate schema content.",
    }

    basis = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_basis_v0",
        "unit_id": UNIT_ID,
        "archive_write_id": archive_write_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_write_authorize_receipt_id": WRITE_AUTHORIZE_RECEIPT_ID,
        "source_write_authorize_decision_record_id": WRITE_AUTHORIZE_DECISION_RECORD_ID,
        "source_write_execution_target_id": WRITE_EXECUTION_TARGET_ID,
        "source_mutation_target_id": MUTATION_TARGET_ID,
        "source_archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "schema_name": SCHEMA_NAME,
        "archive_ref": rel(SCHEMA_ARCHIVE_PATH),
        "execution_claim": "Execute exactly one bounded schema archive entry write and emit receipt.",
        "source_file_hashes": source_hashes,
    }

    rollup = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "archive_write_id": archive_write_id,
        "schema_name": SCHEMA_NAME,
        "schema_archive_ref": rel(SCHEMA_ARCHIVE_PATH),
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "write_authorize_decision_record_id": WRITE_AUTHORIZE_DECISION_RECORD_ID,
        "schema_archive_write_authorized": gate == "PASS",
        "schema_archive_mutation_authorized": gate == "PASS",
        "schema_archive_write_executed": gate == "PASS",
        "schema_archive_mutation_executed": gate == "PASS",
        "schema_archive_entry_written": gate == "PASS",
        "schema_archive_entry_promoted": gate == "PASS",
        "archive_before_sha256": archive_before_sha256,
        "archive_after_sha256": post_state.get("archive_after_sha256"),
        "schema_mutation_authorized": False,
        "schema_mutation_executed": False,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
        "next_unit_id": None,
    }

    readout = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_readout_v0",
        "status": status,
        "archive_write_id": archive_write_id,
        "schema_name": SCHEMA_NAME,
        "schema_archive_ref": rel(SCHEMA_ARCHIVE_PATH),
        "interpretation": "Bounded schema archive entry was written. Runtime adoption, move addition, fixture expansion, T6 live execution, and C8 remain unauthorized."
        if gate == "PASS" else "Schema archive write execution failed typed gates or duplicate guard.",
        "next_unit_id": None,
    }

    profile = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_profile_v0",
        "profile_status": status,
        "archive_write_id": archive_write_id,
        "core_rule": "A successful write promotes only the bounded schema entry into the schema archive. It does not authorize runtime use.",
        "schema_archive_ref": rel(SCHEMA_ARCHIVE_PATH),
        "must_not_infer": [
            "runtime adopted",
            "runtime patched",
            "move registry updated",
            "fixture suite expanded",
            "T6 live case executed",
            "C8 authorized",
            "schema candidate content mutated",
            "general reusable schema outside bounded trigger surface family",
        ],
    }

    report = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "execution_result": "SCHEMA_ARCHIVE_ENTRY_WRITTEN" if gate == "PASS" else "SCHEMA_ARCHIVE_WRITE_EXECUTION_GATE_FAIL",
            "archive_write_id": archive_write_id,
            "schema_name": SCHEMA_NAME,
            "schema_archive_ref": rel(SCHEMA_ARCHIVE_PATH),
            "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
            "schema_archive_write_authorized": gate == "PASS",
            "schema_archive_mutation_authorized": gate == "PASS",
            "schema_archive_write_executed": gate == "PASS",
            "schema_archive_mutation_executed": gate == "PASS",
            "schema_archive_entry_written": gate == "PASS",
            "schema_archive_entry_promoted": gate == "PASS",
            "schema_mutation_authorized": False,
            "schema_mutation_executed": False,
            "runtime_adoption_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "t6_live_case_execution_authorized": False,
            "c8_authorized": False,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_transition_trace_v0",
        "unit_id": UNIT_ID,
        "archive_write_id": archive_write_id,
        "transitions": [
            {
                "from": "SCHEMA_ARCHIVE_WRITE_EXECUTION_TARGET_READY",
                "edge": "consume write authorization and execution target",
                "to": "SCHEMA_ARCHIVE_WRITE_EXECUTION_AUTHORIZED" if gate == "PASS" else "SCHEMA_ARCHIVE_WRITE_EXECUTION_GATE_FAIL",
            },
            {
                "from": "SCHEMA_ARCHIVE_WRITE_EXECUTION_AUTHORIZED" if gate == "PASS" else "SCHEMA_ARCHIVE_WRITE_EXECUTION_GATE_FAIL",
                "edge": "write bounded archive entry with duplicate guard",
                "to": "SCHEMA_ARCHIVE_ENTRY_WRITTEN" if gate == "PASS" else "STOP_GATE_FAIL",
            },
            {
                "from": "SCHEMA_ARCHIVE_ENTRY_WRITTEN" if gate == "PASS" else "STOP_GATE_FAIL",
                "edge": "emit final write receipt and stop",
                "to": "STOP_SCHEMA_ARCHIVE_WRITE_COMPLETE" if gate == "PASS" else "STOP_SCHEMA_ARCHIVE_WRITE_FAILED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "next_unit_id": None,
            "stop_code": "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_COMPLETE" if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_EXECUTION_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (PRE_WRITE_ARCHIVE_STATE_PATH, pre_state),
        (WRITE_PAYLOAD_PATH, write_payload),
        (ARCHIVE_ENTRY_WRITTEN_PATH, archive_entry_written_obj),
        (POST_WRITE_ARCHIVE_STATE_PATH, post_state),
        (ARCHIVE_DELTA_PATH, archive_delta),
        (WRITE_VERIFICATION_PATH, write_verification),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (NEGATIVE_CONTROL_PATH, negative_control),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_DECISION_RECEIPT_CONSUMED",
        "SCHEMA_ARCHIVE_WRITE_EXECUTION_TARGET_CONSUMED",
        "WRITE_AUTHORIZATION_TRUE",
        "MUTATION_AUTHORIZATION_TRUE",
        "DUPLICATE_GUARD_PASS",
        "SCHEMA_ARCHIVE_ENTRY_WRITTEN",
        "SCHEMA_ARCHIVE_WRITE_VERIFIED",
        "WRITE_RECEIPT_EMITTED",
        "NO_SCHEMA_CONTENT_MUTATION",
        "NO_RUNTIME_ADOPTION_AUTHORITY",
        "NO_RUNTIME_PATCH",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION",
        "NO_T6_LIVE_CASE_EXECUTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_EXECUTION_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "archive_write_id": archive_write_id,
        "schema_name": SCHEMA_NAME,
        "schema_archive_ref": rel(SCHEMA_ARCHIVE_PATH),
        "source_write_authorize_receipt_id": WRITE_AUTHORIZE_RECEIPT_ID,
        "source_write_authorize_receipt_ref": rel(WRITE_AUTHORIZE_RECEIPT_PATH),
        "source_write_authorize_decision_record_id": WRITE_AUTHORIZE_DECISION_RECORD_ID,
        "source_write_execution_target_id": WRITE_EXECUTION_TARGET_ID,
        "mutation_target_review_id": MUTATION_TARGET_REVIEW_ID,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "SCHEMA_ARCHIVE_WRITE_EXECUTION_0_AUTHORIZE_RECEIPT_CONSUMED": write_auth_receipt.get("receipt_id") == WRITE_AUTHORIZE_RECEIPT_ID,
            "SCHEMA_ARCHIVE_WRITE_EXECUTION_1_EXECUTION_TARGET_CONSUMED": execution_target.get("schema_archive_write_execution_target_id") == WRITE_EXECUTION_TARGET_ID,
            "SCHEMA_ARCHIVE_WRITE_EXECUTION_2_WRITE_AUTHORIZATION_TRUE": write_auth_summary.get("schema_archive_write_authorized") is True,
            "SCHEMA_ARCHIVE_WRITE_EXECUTION_3_MUTATION_AUTHORIZATION_TRUE": write_auth_summary.get("schema_archive_mutation_authorized") is True,
            "SCHEMA_ARCHIVE_WRITE_EXECUTION_4_DUPLICATE_GUARD_PASS": gate == "PASS",
            "SCHEMA_ARCHIVE_WRITE_EXECUTION_5_ARCHIVE_ENTRY_WRITTEN": gate == "PASS",
            "SCHEMA_ARCHIVE_WRITE_EXECUTION_6_WRITE_VERIFICATION_PASS": write_verification.get("verification_status") == "PASS",
            "SCHEMA_ARCHIVE_WRITE_EXECUTION_7_WRITE_RECEIPT_EMITTED": True,
            "SCHEMA_ARCHIVE_WRITE_EXECUTION_8_NO_SCHEMA_CONTENT_MUTATION": True,
            "SCHEMA_ARCHIVE_WRITE_EXECUTION_9_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "SCHEMA_ARCHIVE_WRITE_EXECUTION_10_NO_RUNTIME_PATCH": True,
            "SCHEMA_ARCHIVE_WRITE_EXECUTION_11_NO_MOVE_ADDITION": True,
            "SCHEMA_ARCHIVE_WRITE_EXECUTION_12_NO_FIXTURE_EXPANSION": True,
            "SCHEMA_ARCHIVE_WRITE_EXECUTION_13_NO_T6_LIVE_CASE_EXECUTION": True,
            "SCHEMA_ARCHIVE_WRITE_EXECUTION_14_NO_C8_AUTHORIZATION": True,
            "SCHEMA_ARCHIVE_WRITE_EXECUTION_15_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_summary": {
            "status": status,
            "archive_write_id": archive_write_id,
            "schema_name": SCHEMA_NAME,
            "schema_archive_ref": rel(SCHEMA_ARCHIVE_PATH),
            "source_write_authorize_receipt_id": WRITE_AUTHORIZE_RECEIPT_ID,
            "source_write_authorize_decision_record_id": WRITE_AUTHORIZE_DECISION_RECORD_ID,
            "source_write_execution_target_id": WRITE_EXECUTION_TARGET_ID,
            "selected_schema_archive_write_decision": SELECTED_WRITE_DECISION,
            "mutation_target_review_id": MUTATION_TARGET_REVIEW_ID,
            "mutation_target_id": MUTATION_TARGET_ID,
            "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
            "schema_archive_write_authorized": gate == "PASS",
            "schema_archive_mutation_authorized": gate == "PASS",
            "schema_archive_write_executed": gate == "PASS",
            "schema_archive_mutation_executed": gate == "PASS",
            "schema_archive_entry_written": gate == "PASS",
            "schema_archive_entry_promoted": gate == "PASS",
            "archive_existed_before": archive_existed_before,
            "archive_before_sha256": archive_before_sha256,
            "archive_after_sha256": post_state.get("archive_after_sha256"),
            "schema_mutation_authorized": False,
            "schema_mutation_executed": False,
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
            "pre_write_archive_state": rel(PRE_WRITE_ARCHIVE_STATE_PATH),
            "write_payload": rel(WRITE_PAYLOAD_PATH),
            "archive_entry_written": rel(ARCHIVE_ENTRY_WRITTEN_PATH),
            "post_write_archive_state": rel(POST_WRITE_ARCHIVE_STATE_PATH),
            "archive_delta": rel(ARCHIVE_DELTA_PATH),
            "write_verification": rel(WRITE_VERIFICATION_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "negative_control": rel(NEGATIVE_CONTROL_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
            "schema_archive": rel(SCHEMA_ARCHIVE_PATH) if SCHEMA_ARCHIVE_PATH.exists() else None,
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id

    if gate == "PASS":
        archive_latest = read_json(SCHEMA_ARCHIVE_PATH)
        for wr in archive_latest.get("write_receipts", []):
            if wr.get("archive_write_id") == archive_write_id:
                wr["receipt_pending"] = False
                wr["receipt_id"] = receipt_id
                wr["receipt_ref"] = f"data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_v0_receipts/{receipt_id}.json"
        write_json(SCHEMA_ARCHIVE_PATH, archive_latest)
        archive_final_sha256 = file_sha256(SCHEMA_ARCHIVE_PATH)
        receipt["machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_summary"]["archive_after_sha256"] = archive_final_sha256
        receipt["machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_summary"]["archive_receipt_link_patch_applied"] = True

    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_receipt_id={receipt_id}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_receipt_path={rel(receipt_path)}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_write_id={archive_write_id if gate == 'PASS' else 'NONE'}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_ref={rel(SCHEMA_ARCHIVE_PATH)}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_terminal_stop_code={transition_trace['terminal']['stop_code']}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
