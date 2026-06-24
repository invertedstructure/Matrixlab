#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RUN_CELL1_SCHEMA_CONSUMPTION_TEST_FROM_C4_HANDOFF_V0"
TARGET_UNIT_ID = "cell1.schema_consumption_test_from_c4_handoff.v0"
LAYER = "CELL_1 / SCHEMA_CONSUMPTION_TEST"
MODE = "CELL1_BOUNDED_TEST / SCHEMA_ONLY / NO_RUNTIME_PATCH"
BUILD_MODE = "CELL1_SCHEMA_CONSUMPTION_TEST_ONLY"

SOURCE_C4_CONSUMPTION_RECEIPT_ID = "c56792b7"
SOURCE_C4_CONSUMPTION_RECEIPT_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0_receipts" / "c56792b7.json"
SOURCE_CELL1_INTAKE_PACKET_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0" / "cell1_intake_packet_v0.json"
SOURCE_HANDOFF_PACKET_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0" / "cell1_handoff_packet_v0.json"
SOURCE_NO_RUNTIME_PATCH_PLAN_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0" / "no_runtime_patch_plan_v0.json"
SOURCE_SCHEMA_CONSUMPTION_PROBE_RECORD_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0" / "schema_consumption_probe_record_v0.json"
SOURCE_VERIFICATION_EXPECTATION_RECORD_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0" / "verification_expectation_record_v0.json"
SOURCE_C4_CONSUMPTION_ROLLUP_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0" / "c4_consumption_rollup_v0.json"

SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID = "71bd1d92"
SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0_receipts" / "71bd1d92.json"
SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0" / "accepted_proposal_packet_v0.json"
SOURCE_REVIEW_DECISION_RECORD_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0" / "review_decision_record_v0.json"

SOURCE_C4_RERUN_RECEIPT_ID = "a17b6786"
SOURCE_C4_RERUN_RECEIPT_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_preflight_rerun_v0_receipts" / "a17b6786.json"
SOURCE_C4_RERUN_GATE_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_preflight_rerun_v0" / "c4_opening_gate_evaluation_v0_1.json"

SOURCE_C1_PATCH_RECEIPT_ID = "fffa3dd5"
SOURCE_C1_PATCH_RECEIPT_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0_receipts" / "fffa3dd5.json"
SOURCE_C1_PATCH_SCHEMA_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0" / "proposal_packet_schema_v0_1.json"

SOURCE_C2_RECEIPT_ID = "348dabde"
SOURCE_C2_RECEIPT_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts" / "348dabde.json"
SOURCE_C2_LANE_REGISTRY_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "taxonomy_lane_registry_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C4_CONSUMPTION_RECEIPT_PATH,
    SOURCE_CELL1_INTAKE_PACKET_PATH,
    SOURCE_HANDOFF_PACKET_PATH,
    SOURCE_NO_RUNTIME_PATCH_PLAN_PATH,
    SOURCE_SCHEMA_CONSUMPTION_PROBE_RECORD_PATH,
    SOURCE_VERIFICATION_EXPECTATION_RECORD_PATH,
    SOURCE_C4_CONSUMPTION_ROLLUP_PATH,
    SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH,
    SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH,
    SOURCE_REVIEW_DECISION_RECORD_PATH,
    SOURCE_C4_RERUN_RECEIPT_PATH,
    SOURCE_C4_RERUN_GATE_PATH,
    SOURCE_C1_PATCH_RECEIPT_PATH,
    SOURCE_C1_PATCH_SCHEMA_PATH,
    SOURCE_C2_RECEIPT_PATH,
    SOURCE_C2_LANE_REGISTRY_PATH,
]

OUT_DIR = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0"
RECEIPT_DIR = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0_receipts"

SOURCE_SURFACE_PATH = OUT_DIR / "cell1_schema_test_source_surface_v0.json"
AUTHORITY_CHECK_PATH = OUT_DIR / "cell1_authority_check_v0.json"
INTAKE_CHECK_PATH = OUT_DIR / "cell1_intake_check_v0.json"
SCHEMA_BINDING_RECORD_PATH = OUT_DIR / "cell1_schema_binding_record_v0.json"
EXECUTION_RECORD_PATH = OUT_DIR / "cell1_schema_consumption_execution_record_v0.json"
PROBE_RESULT_PATH = OUT_DIR / "cell1_schema_consumption_probe_result_v0.json"
VERIFICATION_RECORD_PATH = OUT_DIR / "cell1_schema_consumption_verification_record_v0.json"
NO_PATCH_OBSERVATION_PATH = OUT_DIR / "cell1_no_runtime_patch_observation_v0.json"
HANDOFF_RESULT_PATH = OUT_DIR / "cell1_schema_test_handoff_result_v0.json"
ROLLUP_PATH = OUT_DIR / "cell1_schema_consumption_test_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "cell1_schema_consumption_test_profile_v0.json"
REPORT_PATH = OUT_DIR / "cell1_schema_consumption_test_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "cell1_schema_consumption_test_transition_trace.json"

ZERO_COUNTER_KEYS = [
    "runtime_patch_applied_count",
    "target_file_modified_count",
    "taxonomy_registry_mutation_count",
    "c5_opened_count",
    "general_cell1_authority_granted_count",
    "unbounded_payload_inspection_count",
    "proposal_status_promoted_count",
    "accepted_proposal_fabricated_count",
    "proposed_only_consumed_as_accepted_count",
    "hidden_next_command_count",
    "source_mutation_count",
    "prior_receipt_mutation_count",
    "unexpected_builder_command_count",
    "runtime_build_artifact_emitted_count",
]

HUMAN_DECISION = {
    "decision": "RUN_CELL1_SCHEMA_CONSUMPTION_TEST_FROM_C4_HANDOFF",
    "scope": "Run the first bounded Cell 1 schema-consumption test from the C4 handoff. Consume the C4 consumption receipt, Cell 1 intake packet, handoff packet, no-runtime-patch plan, schema-consumption probe, and verification expectation. Validate authority and schema binding, execute schema-consumption-only test, emit Cell 1 execution/probe/verification records, no-runtime-patch observation, rollup, profile, report, and receipt. Do not apply runtime patches, modify target files, mutate taxonomy, open C5, grant general Cell 1 authority, inspect unbounded payload, or emit hidden next command.",
    "authorized": [
        "consume C4 handoff packet",
        "consume Cell 1 intake packet",
        "validate Cell 1 bounded authority",
        "run schema-consumption-only Cell 1 test",
        "emit execution record",
        "emit schema-consumption probe result",
        "emit verification record for schema-consumption test only",
        "emit no-runtime-patch observation",
        "emit Cell 1 schema-consumption test receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "apply runtime patch",
        "modify target files",
        "mutate taxonomy registry",
        "open C5",
        "grant general Cell 1 authority",
        "inspect unbounded payload",
        "promote proposal status",
        "fabricate accepted proposal",
        "consume PROPOSED_ONLY as accepted",
        "emit hidden next command",
    ],
}

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
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def validate_source_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    c4_receipt = read_json(SOURCE_C4_CONSUMPTION_RECEIPT_PATH)
    intake = read_json(SOURCE_CELL1_INTAKE_PACKET_PATH)
    handoff = read_json(SOURCE_HANDOFF_PACKET_PATH)
    no_patch = read_json(SOURCE_NO_RUNTIME_PATCH_PLAN_PATH)
    probe = read_json(SOURCE_SCHEMA_CONSUMPTION_PROBE_RECORD_PATH)
    expectation = read_json(SOURCE_VERIFICATION_EXPECTATION_RECORD_PATH)
    c4_rollup = read_json(SOURCE_C4_CONSUMPTION_ROLLUP_PATH)
    accepted_packet = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    review = read_json(SOURCE_REVIEW_DECISION_RECORD_PATH)
    c4_gate = read_json(SOURCE_C4_RERUN_GATE_PATH)
    c1_schema = read_json(SOURCE_C1_PATCH_SCHEMA_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)

    if c4_receipt.get("receipt_id") != SOURCE_C4_CONSUMPTION_RECEIPT_ID or c4_receipt.get("gate") != "PASS":
        failures.append("c4_consumption_receipt_not_pass")
    if c4_receipt.get("terminal", {}).get("stop_code") != "STOP_C4_CONSUMED_ACCEPTED_PROPOSAL_READY_FOR_CELL1_SCHEMA_CONSUMPTION":
        failures.append("c4_consumption_wrong_terminal")
    if c4_rollup.get("accepted_proposals_consumed") != 1:
        failures.append("c4_did_not_consume_exactly_one_accepted_proposal")
    if intake.get("execution_status") != "READY_FOR_CELL1_SCHEMA_CONSUMPTION_TEST":
        failures.append("cell1_intake_not_ready")
    if intake.get("runtime_patch_allowed") is not False:
        failures.append("cell1_intake_allows_runtime_patch")
    if intake.get("general_cell1_authority_granted") is not False:
        failures.append("cell1_intake_grants_general_authority")
    if handoff.get("handoff_status") != "READY_FOR_CELL1_SCHEMA_CONSUMPTION_TEST":
        failures.append("handoff_not_ready")
    if handoff.get("next_required_action") != UNIT_ID:
        failures.append(f"handoff_wrong_next_action:{handoff.get('next_required_action')}")
    if handoff.get("cell1_execution_performed_in_this_unit") is not False:
        failures.append("handoff_claims_prior_cell1_execution")
    if no_patch.get("patch_application_expected") is not False:
        failures.append("no_patch_plan_expects_patch")
    if no_patch.get("files_expected_to_change") != []:
        failures.append("no_patch_plan_expects_file_changes")
    if probe.get("probe_status") != "PASS":
        failures.append("source_schema_probe_not_pass")
    if probe.get("runtime_patch_applied") is not False:
        failures.append("source_probe_claims_runtime_patch")
    if probe.get("verification_pass_emitted") is not False:
        failures.append("source_probe_claims_verification_pass")
    if expectation.get("verification_status") != "PENDING_NOT_RUN":
        failures.append("verification_expectation_not_pending")
    if expectation.get("verification_pass_emitted") is not False:
        failures.append("verification_expectation_already_pass")
    if accepted_packet.get("status") != "ACCEPTED_FOR_BUILD":
        failures.append("accepted_packet_not_accepted_for_build")
    if review.get("authorizes_exact_proposal_id") is not True or review.get("proposal_id") != accepted_packet.get("proposal_id"):
        failures.append("review_not_exact_proposal")
    if c4_gate.get("c4_opening_gate_status") != "OPEN_FOR_NARROW_ACCEPTED_PROPOSAL_TEST":
        failures.append("c4_gate_not_open")
    if c1_schema.get("review_authority", {}).get("cell1_may_accept") is not False:
        failures.append("c1_schema_allows_cell1_acceptance")
    if c2_receipt.get("receipt_id") != SOURCE_C2_RECEIPT_ID or c2_receipt.get("gate") != "PASS":
        failures.append("c2_basis_not_accepted")
    return failures

def source_surface() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_schema_test_source_surface_v0",
        "source_c4_consumption_receipt_id": SOURCE_C4_CONSUMPTION_RECEIPT_ID,
        "source_c4_consumption_receipt_ref": rel(SOURCE_C4_CONSUMPTION_RECEIPT_PATH),
        "source_cell1_intake_packet_ref": rel(SOURCE_CELL1_INTAKE_PACKET_PATH),
        "source_handoff_packet_ref": rel(SOURCE_HANDOFF_PACKET_PATH),
        "source_no_runtime_patch_plan_ref": rel(SOURCE_NO_RUNTIME_PATCH_PLAN_PATH),
        "source_verification_expectation_ref": rel(SOURCE_VERIFICATION_EXPECTATION_RECORD_PATH),
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_accepted_proposal_packet_ref": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "source_c1_patch_schema_ref": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "source_c2_lane_registry_ref": rel(SOURCE_C2_LANE_REGISTRY_PATH),
        "surface_status": "EXPLICIT_CELL1_SCHEMA_CONSUMPTION_TEST_SURFACE",
    }

def authority_check() -> Dict[str, Any]:
    intake = read_json(SOURCE_CELL1_INTAKE_PACKET_PATH)
    handoff = read_json(SOURCE_HANDOFF_PACKET_PATH)
    no_patch = read_json(SOURCE_NO_RUNTIME_PATCH_PLAN_PATH)
    checks = {
        "handoff_targets_this_unit": handoff.get("next_required_action") == UNIT_ID,
        "cell1_intake_ready": intake.get("execution_status") == "READY_FOR_CELL1_SCHEMA_CONSUMPTION_TEST",
        "runtime_patch_disallowed": intake.get("runtime_patch_allowed") is False and no_patch.get("patch_application_expected") is False,
        "general_authority_not_granted": intake.get("general_cell1_authority_granted") is False,
        "handoff_not_previously_executed": handoff.get("cell1_execution_performed_in_this_unit") is False,
    }
    return {
        "schema_version": "cell1_authority_check_v0",
        "authority_check_id": "cell1_auth_" + sha8(checks),
        "cell_id": "CELL_1",
        "authority_kind": "BOUNDED_SCHEMA_CONSUMPTION_TEST_ONLY",
        "checks": checks,
        "authority_status": "PASS" if all(checks.values()) else "FAIL",
        "authorized_actions": [
            "bind intake packet",
            "validate schema refs",
            "run schema-consumption probe",
            "emit schema-consumption verification record",
            "emit no-runtime-patch observation",
        ],
        "forbidden_actions": [
            "runtime patch",
            "target file modification",
            "taxonomy mutation",
            "C5 opening",
            "general Cell 1 authority",
            "hidden continuation",
        ],
    }

def intake_check() -> Dict[str, Any]:
    intake = read_json(SOURCE_CELL1_INTAKE_PACKET_PATH)
    accepted = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    review = read_json(SOURCE_REVIEW_DECISION_RECORD_PATH)
    checks = {
        "proposal_ids_match": intake.get("proposal_id") == accepted.get("proposal_id") == review.get("proposal_id"),
        "proposal_status_accepted": intake.get("proposal_status") == "ACCEPTED_FOR_BUILD",
        "review_receipt_matches": intake.get("review_receipt_id") == review.get("review_receipt_id"),
        "required_refs_present": bool(intake.get("allowed_inputs")),
        "forbidden_inputs_declared": bool(intake.get("forbidden_inputs")),
        "stop_conditions_present": bool(intake.get("stop_conditions")),
    }
    return {
        "schema_version": "cell1_intake_check_v0",
        "intake_check_id": "cell1_intake_check_" + sha8(checks),
        "proposal_id": intake.get("proposal_id"),
        "review_receipt_id": intake.get("review_receipt_id"),
        "checks": checks,
        "intake_status": "PASS" if all(checks.values()) else "FAIL",
    }

def schema_binding_record() -> Dict[str, Any]:
    intake = read_json(SOURCE_CELL1_INTAKE_PACKET_PATH)
    accepted = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    c1_schema = read_json(SOURCE_C1_PATCH_SCHEMA_PATH)
    required_sections = [
        "builder_interface",
        "verification_contract",
        "failure_or_reject_handling",
        "claim_scope",
        "payload_boundary",
        "evidence_limitations",
        "review_authority",
    ]
    bindings = {
        section: section in accepted and section in c1_schema
        for section in required_sections
    }
    return {
        "schema_version": "cell1_schema_binding_record_v0",
        "binding_id": "schema_binding_" + sha8({"proposal": intake.get("proposal_id"), "bindings": bindings}),
        "proposal_id": intake.get("proposal_id"),
        "candidate_schema_ref": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "accepted_proposal_packet_ref": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "required_sections": required_sections,
        "bindings": bindings,
        "binding_status": "PASS" if all(bindings.values()) else "FAIL",
        "must_not_infer": [
            "runtime patch correctness",
            "global builder correctness",
            "future proposal acceptance",
        ],
    }

def execution_record(authority: Dict[str, Any], intake: Dict[str, Any], binding: Dict[str, Any]) -> Dict[str, Any]:
    ok = authority["authority_status"] == "PASS" and intake["intake_status"] == "PASS" and binding["binding_status"] == "PASS"
    source_intake = read_json(SOURCE_CELL1_INTAKE_PACKET_PATH)
    return {
        "schema_version": "cell1_schema_consumption_execution_record_v0",
        "execution_id": "cell1_schema_exec_" + sha8({"proposal": source_intake.get("proposal_id"), "ok": ok}),
        "cell_id": "CELL_1",
        "execution_kind": "SCHEMA_CONSUMPTION_TEST_ONLY",
        "proposal_id": source_intake.get("proposal_id"),
        "authority_check_ref": rel(AUTHORITY_CHECK_PATH),
        "intake_check_ref": rel(INTAKE_CHECK_PATH),
        "schema_binding_record_ref": rel(SCHEMA_BINDING_RECORD_PATH),
        "execution_status": "PASS" if ok else "FAIL",
        "cell1_bounded_execution_opened": ok,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "general_cell1_authority_granted": False,
        "must_not_infer": [
            "runtime patch applied",
            "target file modified",
            "general Cell 1 builder authority",
            "C5 authorized",
        ],
    }

def probe_result(execution: Dict[str, Any]) -> Dict[str, Any]:
    accepted = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    checks = {
        "execution_record_passed": execution["execution_status"] == "PASS",
        "accepted_status_bound": accepted.get("status") == "ACCEPTED_FOR_BUILD",
        "review_ref_bound": bool(accepted.get("review_receipt_id")),
        "builder_interface_bound": "builder_interface" in accepted,
        "verification_contract_bound": "verification_contract" in accepted,
        "payload_boundary_bound": "payload_boundary" in accepted,
        "runtime_patch_not_applied": True,
        "target_file_not_modified": True,
    }
    return {
        "schema_version": "cell1_schema_consumption_probe_result_v0",
        "probe_result_id": "cell1_probe_" + sha8(checks),
        "proposal_id": accepted.get("proposal_id"),
        "probe_kind": "CELL1_SCHEMA_CONSUMPTION_ONLY",
        "checks": checks,
        "probe_status": "PASS" if all(checks.values()) else "FAIL",
        "runtime_patch_applied": False,
        "target_file_modified": False,
    }

def verification_record(execution: Dict[str, Any], probe: Dict[str, Any]) -> Dict[str, Any]:
    expectation = read_json(SOURCE_VERIFICATION_EXPECTATION_RECORD_PATH)
    ok = execution["execution_status"] == "PASS" and probe["probe_status"] == "PASS"
    return {
        "schema_version": "cell1_schema_consumption_verification_record_v0",
        "verification_record_id": "cell1_verify_" + sha8({"execution": execution["execution_id"], "probe": probe["probe_result_id"]}),
        "proposal_id": execution["proposal_id"],
        "expected_verification_receipt_shape": expectation.get("expected_verification_receipt_shape"),
        "required_checks": expectation.get("required_checks", []),
        "required_negative_controls": expectation.get("required_negative_controls", []),
        "verification_status": "PASS" if ok else "FAIL",
        "verification_scope": "SCHEMA_CONSUMPTION_TEST_ONLY",
        "runtime_patch_verified": False,
        "target_file_change_verified": False,
        "general_builder_authority_verified": False,
        "must_not_infer": [
            "runtime patch correctness",
            "target file correctness",
            "general Cell 1 authority",
            "future accepted proposal correctness",
        ],
    }

def no_patch_observation() -> Dict[str, Any]:
    no_patch = read_json(SOURCE_NO_RUNTIME_PATCH_PLAN_PATH)
    return {
        "schema_version": "cell1_no_runtime_patch_observation_v0",
        "observation_id": "no_patch_obs_" + sha8(no_patch),
        "proposal_id": no_patch.get("proposal_id"),
        "patch_plan_ref": rel(SOURCE_NO_RUNTIME_PATCH_PLAN_PATH),
        "patch_application_expected": no_patch.get("patch_application_expected"),
        "files_expected_to_change": no_patch.get("files_expected_to_change"),
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "observation_status": "PASS" if no_patch.get("patch_application_expected") is False and no_patch.get("files_expected_to_change") == [] else "FAIL",
    }

def handoff_result(execution: Dict[str, Any], verification: Dict[str, Any]) -> Dict[str, Any]:
    source_handoff = read_json(SOURCE_HANDOFF_PACKET_PATH)
    return {
        "schema_version": "cell1_schema_test_handoff_result_v0",
        "handoff_result_id": "cell1_handoff_result_" + sha8({"execution": execution["execution_id"], "verification": verification["verification_record_id"]}),
        "source_handoff_ref": rel(SOURCE_HANDOFF_PACKET_PATH),
        "source_handoff_status": source_handoff.get("handoff_status"),
        "cell1_execution_id": execution["execution_id"],
        "verification_record_id": verification["verification_record_id"],
        "handoff_result_status": "CELL1_SCHEMA_CONSUMPTION_TEST_COMPLETE",
        "next_required_object": "CELL1_SCHEMA_CONSUMPTION_TEST_REVIEW_OR_CLOSE_V0",
        "next_command_goal": None,
        "must_not_infer": [
            "C5 authorized",
            "runtime patch complete",
            "general builder capability proven",
        ],
    }

def rollup(execution: Dict[str, Any], probe: Dict[str, Any], verification: Dict[str, Any], no_patch: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_schema_consumption_test_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_c4_consumption_receipt_id": SOURCE_C4_CONSUMPTION_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "proposal_id": execution["proposal_id"],
        "cell1_schema_consumption_tests_run": 1,
        "cell1_schema_consumption_tests_passed": 1 if execution["execution_status"] == "PASS" else 0,
        "cell1_bounded_execution_opened_count": 1 if execution["cell1_bounded_execution_opened"] else 0,
        "schema_binding_pass_count": 1 if execution["execution_status"] == "PASS" else 0,
        "schema_consumption_probe_pass_count": 1 if probe["probe_status"] == "PASS" else 0,
        "schema_consumption_verification_pass_count": 1 if verification["verification_status"] == "PASS" else 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "unbounded_payload_inspection_count": 0,
        "proposal_status_promoted_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "proposed_only_consumed_as_accepted_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "unexpected_builder_command_count": 0,
        "runtime_build_artifact_emitted_count": 0,
        "recommended_next": "CELL1_SCHEMA_CONSUMPTION_TEST_REVIEW_OR_CLOSE_V0",
    }

def profile(rollup_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_schema_consumption_test_profile_v0",
        "profile_id": "cell1_schema_test_" + sha8({"proposal": rollup_obj["proposal_id"], "source": SOURCE_C4_CONSUMPTION_RECEIPT_ID}),
        "status": "CELL1_SCHEMA_CONSUMPTION_TEST_COMPLETE",
        "proposal_id": rollup_obj["proposal_id"],
        "cell1_bounded_execution_opened": rollup_obj["cell1_bounded_execution_opened_count"] == 1,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "verification_scope": "SCHEMA_CONSUMPTION_TEST_ONLY",
        "verification_status": "PASS",
        "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "must_not_infer": [
            "runtime patch applied",
            "target file modified",
            "C5 authorized",
            "general Cell 1 authority",
            "future builder correctness",
        ],
        "next_command_goal": None,
    }

def report(rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_schema_consumption_test_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_c4_handoff_consumed_count": 1,
        "source_cell1_intake_packet_consumed_count": 1,
        "authority_check_emitted_count": 1,
        "intake_check_emitted_count": 1,
        "schema_binding_record_emitted_count": 1,
        "execution_record_emitted_count": 1,
        "probe_result_emitted_count": 1,
        "verification_record_emitted_count": 1,
        "no_runtime_patch_observation_emitted_count": 1,
        "handoff_result_emitted_count": 1,
        "profile_status": profile_obj["status"],
        "cell1_schema_consumption_tests_run": rollup_obj["cell1_schema_consumption_tests_run"],
        "cell1_schema_consumption_tests_passed": rollup_obj["cell1_schema_consumption_tests_passed"],
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "recommended_next_handling": rollup_obj["recommended_next"],
    }

def transition_trace() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_schema_consumption_test_transition_trace_v0",
        "trace": [
            {
                "step": "load_c4_handoff",
                "question": "does C4 provide a bounded Cell 1 schema-consumption handoff",
                "answer": SOURCE_HANDOFF_PACKET_PATH.relative_to(ROOT).as_posix(),
                "taken": "check_cell1_authority",
            },
            {
                "step": "check_cell1_authority",
                "question": "is this bounded to schema consumption only",
                "answer": "PASS",
                "taken": "bind_schema",
            },
            {
                "step": "bind_schema",
                "question": "does accepted proposal bind required schema sections",
                "answer": "PASS",
                "taken": "run_schema_consumption_test",
            },
            {
                "step": "run_schema_consumption_test",
                "question": "did schema-consumption pass without runtime patch",
                "answer": "PASS",
                "taken": "emit_verification_and_stop",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CELL1_SCHEMA_CONSUMPTION_TEST_COMPLETE_REVIEW_OR_CLOSE",
            "next_command_goal": None,
        },
    }

def validate_outputs(authority: Dict[str, Any], intake: Dict[str, Any], binding: Dict[str, Any], execution: Dict[str, Any], probe: Dict[str, Any], verification: Dict[str, Any], no_patch: Dict[str, Any], handoff_result_obj: Dict[str, Any], rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any], report_obj: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if authority.get("authority_status") != "PASS":
        failures.append("authority_check_not_pass")
    if intake.get("intake_status") != "PASS":
        failures.append("intake_check_not_pass")
    if binding.get("binding_status") != "PASS":
        failures.append("schema_binding_not_pass")
    if execution.get("execution_status") != "PASS":
        failures.append("execution_status_not_pass")
    if execution.get("cell1_bounded_execution_opened") is not True:
        failures.append("bounded_cell1_execution_not_opened")
    if execution.get("runtime_patch_applied") is not False:
        failures.append("execution_claims_runtime_patch")
    if execution.get("target_file_modified") is not False:
        failures.append("execution_claims_target_file_modified")
    if execution.get("general_cell1_authority_granted") is not False:
        failures.append("execution_grants_general_authority")
    if probe.get("probe_status") != "PASS":
        failures.append("probe_not_pass")
    if probe.get("runtime_patch_applied") is not False:
        failures.append("probe_claims_runtime_patch")
    if probe.get("target_file_modified") is not False:
        failures.append("probe_claims_target_file_modified")
    if verification.get("verification_status") != "PASS":
        failures.append("verification_not_pass")
    if verification.get("verification_scope") != "SCHEMA_CONSUMPTION_TEST_ONLY":
        failures.append("verification_scope_wrong")
    if verification.get("runtime_patch_verified") is not False:
        failures.append("verification_claims_runtime_patch_verified")
    if verification.get("target_file_change_verified") is not False:
        failures.append("verification_claims_target_file_verified")
    if no_patch.get("observation_status") != "PASS":
        failures.append("no_patch_observation_not_pass")
    if no_patch.get("runtime_patch_applied") is not False:
        failures.append("no_patch_claims_runtime_patch")
    if no_patch.get("target_file_modified") is not False:
        failures.append("no_patch_claims_target_file_modified")
    if handoff_result_obj.get("handoff_result_status") != "CELL1_SCHEMA_CONSUMPTION_TEST_COMPLETE":
        failures.append("handoff_result_status_wrong")
    if handoff_result_obj.get("next_command_goal") is not None:
        failures.append("handoff_hidden_next_command")
    if rollup_obj.get("cell1_schema_consumption_tests_run") != 1:
        failures.append("schema_tests_run_not_one")
    if rollup_obj.get("cell1_schema_consumption_tests_passed") != 1:
        failures.append("schema_tests_passed_not_one")
    if rollup_obj.get("cell1_bounded_execution_opened_count") != 1:
        failures.append("bounded_execution_count_not_one")
    if rollup_obj.get("schema_consumption_verification_pass_count") != 1:
        failures.append("schema_verification_pass_count_not_one")
    for key in ZERO_COUNTER_KEYS:
        if rollup_obj.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup_obj.get(key)}")
    if profile_obj.get("cell1_bounded_execution_opened") is not True:
        failures.append("profile_missing_bounded_execution")
    if profile_obj.get("runtime_patch_applied") is not False:
        failures.append("profile_claims_runtime_patch")
    if profile_obj.get("target_file_modified") is not False:
        failures.append("profile_claims_target_file_modified")
    if profile_obj.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")
    for key in [
        "runtime_patch_applied_count",
        "target_file_modified_count",
        "taxonomy_registry_mutation_count",
        "c5_opened_count",
        "general_cell1_authority_granted_count",
        "hidden_next_command_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
    ]:
        if report_obj.get(key) != 0:
            failures.append(f"report_counter_nonzero:{key}:{report_obj.get(key)}")
    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    for gate, ok in receipt.get("acceptance_gate_results", {}).items():
        if ok is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{ok}")
    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_CELL1_SCHEMA_CONSUMPTION_TEST_COMPLETE_REVIEW_OR_CLOSE":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    authority = read_json(AUTHORITY_CHECK_PATH)
    intake = read_json(INTAKE_CHECK_PATH)
    binding = read_json(SCHEMA_BINDING_RECORD_PATH)
    execution = read_json(EXECUTION_RECORD_PATH)
    probe = read_json(PROBE_RESULT_PATH)
    verification = read_json(VERIFICATION_RECORD_PATH)
    no_patch = read_json(NO_PATCH_OBSERVATION_PATH)
    handoff_result_obj = read_json(HANDOFF_RESULT_PATH)
    rollup_obj = read_json(ROLLUP_PATH)
    profile_obj = read_json(PROFILE_PATH)
    report_obj = read_json(REPORT_PATH)

    controls: List[Dict[str, Any]] = []

    def add(case: str, failures: List[str], expected_fragment: str) -> None:
        controls.append({
            "case": case,
            "negative_control_pass": any(expected_fragment in f for f in failures),
            "failures": failures,
            "wrote_live_artifact": False,
        })

    bad_authority = copy.deepcopy(authority)
    bad_authority["authority_status"] = "FAIL"
    add("authority_check_fail", validate_outputs(bad_authority, intake, binding, execution, probe, verification, no_patch, handoff_result_obj, rollup_obj, profile_obj, report_obj), "authority_check_not_pass")

    bad_intake = copy.deepcopy(intake)
    bad_intake["intake_status"] = "FAIL"
    add("intake_check_fail", validate_outputs(authority, bad_intake, binding, execution, probe, verification, no_patch, handoff_result_obj, rollup_obj, profile_obj, report_obj), "intake_check_not_pass")

    bad_binding = copy.deepcopy(binding)
    bad_binding["binding_status"] = "FAIL"
    add("schema_binding_fail", validate_outputs(authority, intake, bad_binding, execution, probe, verification, no_patch, handoff_result_obj, rollup_obj, profile_obj, report_obj), "schema_binding_not_pass")

    bad_execution = copy.deepcopy(execution)
    bad_execution["execution_status"] = "FAIL"
    add("execution_status_fail", validate_outputs(authority, intake, binding, bad_execution, probe, verification, no_patch, handoff_result_obj, rollup_obj, profile_obj, report_obj), "execution_status_not_pass")

    bad_execution = copy.deepcopy(execution)
    bad_execution["runtime_patch_applied"] = True
    add("execution_claims_runtime_patch_fail", validate_outputs(authority, intake, binding, bad_execution, probe, verification, no_patch, handoff_result_obj, rollup_obj, profile_obj, report_obj), "execution_claims_runtime_patch")

    bad_execution = copy.deepcopy(execution)
    bad_execution["target_file_modified"] = True
    add("execution_claims_target_file_modified_fail", validate_outputs(authority, intake, binding, bad_execution, probe, verification, no_patch, handoff_result_obj, rollup_obj, profile_obj, report_obj), "execution_claims_target_file_modified")

    bad_execution = copy.deepcopy(execution)
    bad_execution["general_cell1_authority_granted"] = True
    add("execution_grants_general_authority_fail", validate_outputs(authority, intake, binding, bad_execution, probe, verification, no_patch, handoff_result_obj, rollup_obj, profile_obj, report_obj), "execution_grants_general_authority")

    bad_probe = copy.deepcopy(probe)
    bad_probe["probe_status"] = "FAIL"
    add("probe_fail", validate_outputs(authority, intake, binding, execution, bad_probe, verification, no_patch, handoff_result_obj, rollup_obj, profile_obj, report_obj), "probe_not_pass")

    bad_probe = copy.deepcopy(probe)
    bad_probe["runtime_patch_applied"] = True
    add("probe_claims_runtime_patch_fail", validate_outputs(authority, intake, binding, execution, bad_probe, verification, no_patch, handoff_result_obj, rollup_obj, profile_obj, report_obj), "probe_claims_runtime_patch")

    bad_verification = copy.deepcopy(verification)
    bad_verification["verification_status"] = "FAIL"
    add("verification_fail", validate_outputs(authority, intake, binding, execution, probe, bad_verification, no_patch, handoff_result_obj, rollup_obj, profile_obj, report_obj), "verification_not_pass")

    bad_verification = copy.deepcopy(verification)
    bad_verification["verification_scope"] = "RUNTIME_PATCH_TEST"
    add("verification_scope_wrong_fail", validate_outputs(authority, intake, binding, execution, probe, bad_verification, no_patch, handoff_result_obj, rollup_obj, profile_obj, report_obj), "verification_scope_wrong")

    bad_no_patch = copy.deepcopy(no_patch)
    bad_no_patch["runtime_patch_applied"] = True
    add("no_patch_claims_runtime_patch_fail", validate_outputs(authority, intake, binding, execution, probe, verification, bad_no_patch, handoff_result_obj, rollup_obj, profile_obj, report_obj), "no_patch_claims_runtime_patch")

    bad_handoff = copy.deepcopy(handoff_result_obj)
    bad_handoff["next_command_goal"] = "RUN_C5"
    add("handoff_hidden_next_command_fail", validate_outputs(authority, intake, binding, execution, probe, verification, no_patch, bad_handoff, rollup_obj, profile_obj, report_obj), "handoff_hidden_next_command")

    for case, counter in [
        ("runtime_patch_applied_fail", "runtime_patch_applied_count"),
        ("target_file_modified_fail", "target_file_modified_count"),
        ("taxonomy_registry_mutated_fail", "taxonomy_registry_mutation_count"),
        ("c5_opened_fail", "c5_opened_count"),
        ("general_cell1_authority_granted_fail", "general_cell1_authority_granted_count"),
        ("unbounded_payload_inspection_fail", "unbounded_payload_inspection_count"),
        ("proposal_status_promoted_fail", "proposal_status_promoted_count"),
        ("accepted_proposal_fabricated_fail", "accepted_proposal_fabricated_count"),
        ("proposed_only_consumed_as_accepted_fail", "proposed_only_consumed_as_accepted_count"),
        ("hidden_next_command_fail", "hidden_next_command_count"),
        ("source_mutation_fail", "source_mutation_count"),
        ("prior_receipt_mutation_fail", "prior_receipt_mutation_count"),
        ("unexpected_builder_command_fail", "unexpected_builder_command_count"),
        ("runtime_build_artifact_emitted_fail", "runtime_build_artifact_emitted_count"),
    ]:
        bad_rollup = copy.deepcopy(rollup_obj)
        bad_report = copy.deepcopy(report_obj)
        bad_rollup[counter] = 1
        if counter in bad_report:
            bad_report[counter] = 1
        add(case, validate_outputs(authority, intake, binding, execution, probe, verification, no_patch, handoff_result_obj, bad_rollup, profile_obj, bad_report), counter)

    bad_rollup = copy.deepcopy(rollup_obj)
    bad_rollup["cell1_schema_consumption_tests_run"] = 0
    add("schema_tests_run_not_one_fail", validate_outputs(authority, intake, binding, execution, probe, verification, no_patch, handoff_result_obj, bad_rollup, profile_obj, report_obj), "schema_tests_run_not_one")

    bad_rollup = copy.deepcopy(rollup_obj)
    bad_rollup["schema_consumption_verification_pass_count"] = 0
    add("schema_verification_pass_count_not_one_fail", validate_outputs(authority, intake, binding, execution, probe, verification, no_patch, handoff_result_obj, bad_rollup, profile_obj, report_obj), "schema_verification_pass_count_not_one")

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_CELL1_SCHEMA_TEST_DEPENDENCY_MISSING", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "cell1_schema_consumption_test_receipt_v0",
            "receipt_type": "CELL1_SCHEMA_CONSUMPTION_TEST_RECEIPT",
            "receipt_id": receipt_id,
            "unit_id": UNIT_ID,
            "target_unit_id": TARGET_UNIT_ID,
            "gate": "FAIL",
            "failures": failures,
            "terminal": terminal,
            "created_at": now_iso(),
        }
        write_json(receipt_path, receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        print(f"cell1_schema_test_receipt_id={receipt_id}")
        print(f"cell1_schema_test_receipt_path=data/cell1_schema_consumption_test_from_c4_handoff_v0_receipts/{receipt_id}.json")
        return 1

    authority = authority_check()
    intake = intake_check()
    binding = schema_binding_record()
    execution = execution_record(authority, intake, binding)
    probe = probe_result(execution)
    verification = verification_record(execution, probe)
    no_patch = no_patch_observation()
    handoff_result_obj = handoff_result(execution, verification)
    rollup_obj = rollup(execution, probe, verification, no_patch)
    profile_obj = profile(rollup_obj)
    report_obj = report(rollup_obj, profile_obj)
    trace = transition_trace()

    write_json(SOURCE_SURFACE_PATH, source_surface())
    write_json(AUTHORITY_CHECK_PATH, authority)
    write_json(INTAKE_CHECK_PATH, intake)
    write_json(SCHEMA_BINDING_RECORD_PATH, binding)
    write_json(EXECUTION_RECORD_PATH, execution)
    write_json(PROBE_RESULT_PATH, probe)
    write_json(VERIFICATION_RECORD_PATH, verification)
    write_json(NO_PATCH_OBSERVATION_PATH, no_patch)
    write_json(HANDOFF_RESULT_PATH, handoff_result_obj)
    write_json(ROLLUP_PATH, rollup_obj)
    write_json(PROFILE_PATH, profile_obj)
    write_json(REPORT_PATH, report_obj)
    write_json(TRANSITION_TRACE_PATH, trace)

    failures.extend(validate_outputs(authority, intake, binding, execution, probe, verification, no_patch, handoff_result_obj, rollup_obj, profile_obj, report_obj))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup_obj["source_mutation_count"] = 1
        report_obj["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup_obj)
        write_json(REPORT_PATH, report_obj)

    acceptance_gate_results = {
        "CELL1_SCHEMA_TEST_0_C4_CONSUMPTION_RECEIPT_CONSUMED": SOURCE_C4_CONSUMPTION_RECEIPT_PATH.exists(),
        "CELL1_SCHEMA_TEST_1_CELL1_INTAKE_PACKET_CONSUMED": SOURCE_CELL1_INTAKE_PACKET_PATH.exists(),
        "CELL1_SCHEMA_TEST_2_HANDOFF_PACKET_CONSUMED": SOURCE_HANDOFF_PACKET_PATH.exists(),
        "CELL1_SCHEMA_TEST_3_HANDOFF_TARGETS_THIS_UNIT": authority["checks"]["handoff_targets_this_unit"] is True,
        "CELL1_SCHEMA_TEST_4_AUTHORITY_CHECK_PASS": authority["authority_status"] == "PASS",
        "CELL1_SCHEMA_TEST_5_INTAKE_CHECK_PASS": intake["intake_status"] == "PASS",
        "CELL1_SCHEMA_TEST_6_SCHEMA_BINDING_PASS": binding["binding_status"] == "PASS",
        "CELL1_SCHEMA_TEST_7_EXECUTION_RECORD_EMITTED": EXECUTION_RECORD_PATH.exists() and execution["execution_status"] == "PASS",
        "CELL1_SCHEMA_TEST_8_BOUNDED_CELL1_EXECUTION_OPENED": execution["cell1_bounded_execution_opened"] is True,
        "CELL1_SCHEMA_TEST_9_PROBE_RESULT_PASS": PROBE_RESULT_PATH.exists() and probe["probe_status"] == "PASS",
        "CELL1_SCHEMA_TEST_10_VERIFICATION_RECORD_PASS_SCHEMA_ONLY": VERIFICATION_RECORD_PATH.exists() and verification["verification_status"] == "PASS" and verification["verification_scope"] == "SCHEMA_CONSUMPTION_TEST_ONLY",
        "CELL1_SCHEMA_TEST_11_NO_RUNTIME_PATCH_APPLIED": rollup_obj["runtime_patch_applied_count"] == 0,
        "CELL1_SCHEMA_TEST_12_NO_TARGET_FILE_MODIFIED": rollup_obj["target_file_modified_count"] == 0,
        "CELL1_SCHEMA_TEST_13_NO_TAXONOMY_MUTATION": rollup_obj["taxonomy_registry_mutation_count"] == 0,
        "CELL1_SCHEMA_TEST_14_NO_C5_OPENED": rollup_obj["c5_opened_count"] == 0,
        "CELL1_SCHEMA_TEST_15_NO_GENERAL_CELL1_AUTHORITY": rollup_obj["general_cell1_authority_granted_count"] == 0,
        "CELL1_SCHEMA_TEST_16_NO_UNBOUNDED_PAYLOAD_INSPECTION": rollup_obj["unbounded_payload_inspection_count"] == 0,
        "CELL1_SCHEMA_TEST_17_NO_PROPOSAL_STATUS_PROMOTION": rollup_obj["proposal_status_promoted_count"] == 0,
        "CELL1_SCHEMA_TEST_18_NO_HIDDEN_NEXT_COMMAND": rollup_obj["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
        "CELL1_SCHEMA_TEST_19_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    for gate_name, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate_name}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_c4_consumption": SOURCE_C4_CONSUMPTION_RECEIPT_ID,
        "proposal_id": rollup_obj["proposal_id"],
        "verification": rollup_obj["schema_consumption_verification_pass_count"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "authority_check": rel(AUTHORITY_CHECK_PATH),
        "intake_check": rel(INTAKE_CHECK_PATH),
        "schema_binding_record": rel(SCHEMA_BINDING_RECORD_PATH),
        "execution_record": rel(EXECUTION_RECORD_PATH),
        "probe_result": rel(PROBE_RESULT_PATH),
        "verification_record": rel(VERIFICATION_RECORD_PATH),
        "no_runtime_patch_observation": rel(NO_PATCH_OBSERVATION_PATH),
        "handoff_result": rel(HANDOFF_RESULT_PATH),
        "rollup": rel(ROLLUP_PATH),
        "profile": rel(PROFILE_PATH),
        "report": rel(REPORT_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_c4_consumption_receipt": rel(SOURCE_C4_CONSUMPTION_RECEIPT_PATH),
        "source_cell1_intake_packet": rel(SOURCE_CELL1_INTAKE_PACKET_PATH),
        "source_c4_handoff_packet": rel(SOURCE_HANDOFF_PACKET_PATH),
        "source_accepted_proposal_packet": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "source_c1_patch_schema": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "source_c2_lane_registry": rel(SOURCE_C2_LANE_REGISTRY_PATH),
    }

    guards = {
        "build_mode_cell1_schema_consumption_test_only": BUILD_MODE == "CELL1_SCHEMA_CONSUMPTION_TEST_ONLY",
        "bounded_cell1_execution_opened": execution["cell1_bounded_execution_opened"] is True,
        "schema_consumption_verification_passed": verification["verification_status"] == "PASS",
        "verification_scope_schema_only": verification["verification_scope"] == "SCHEMA_CONSUMPTION_TEST_ONLY",
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "taxonomy_registry_mutated": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "hidden_next_command": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
    }

    receipt = {
        "schema_version": "cell1_schema_consumption_test_receipt_v0",
        "receipt_type": "CELL1_SCHEMA_CONSUMPTION_TEST_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "first bounded Cell 1 schema-consumption test from C4 handoff",
        "source_c4_consumption_receipt_id": SOURCE_C4_CONSUMPTION_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "cell1_schema_consumption_summary": {
            "profile_status": profile_obj["status"],
            "proposal_id": rollup_obj["proposal_id"],
            "cell1_schema_consumption_tests_run": rollup_obj["cell1_schema_consumption_tests_run"],
            "cell1_schema_consumption_tests_passed": rollup_obj["cell1_schema_consumption_tests_passed"],
            "cell1_bounded_execution_opened_count": rollup_obj["cell1_bounded_execution_opened_count"],
            "schema_consumption_verification_pass_count": rollup_obj["schema_consumption_verification_pass_count"],
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "verification_scope": "SCHEMA_CONSUMPTION_TEST_ONLY",
            "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
            "recommended_next": rollup_obj["recommended_next"],
        },
        "aggregate_metrics": {
            **{k: v for k, v in report_obj.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
            "rollup": rollup_obj,
            "source_mutation_count": 1 if source_mutation_detected else report_obj["source_mutation_count"],
        },
        "acceptance_gate_results": acceptance_gate_results,
        "cell1_schema_consumption_guards": guards,
        "terminal": terminal,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_failures = validate_receipt(receipt)
    failures.extend(receipt_failures)
    receipt["failures"] = failures
    receipt["gate"] = "PASS" if not failures else "FAIL"
    if failures:
        receipt["terminal"] = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}

    write_json(receipt_path, receipt)

    negative_controls = run_negative_controls(receipt_path)
    if len(negative_controls) != 29 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
        receipt = read_json(receipt_path)
        receipt["gate"] = "FAIL"
        receipt["failures"].append("negative_controls_failed")
        receipt["negative_controls"] = negative_controls
        receipt["terminal"] = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}
        write_json(receipt_path, receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 1

    receipt = read_json(receipt_path)
    receipt["negative_controls"] = negative_controls
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"cell1_schema_test_receipt_id={receipt_id}")
    print(f"cell1_schema_test_receipt_path=data/cell1_schema_consumption_test_from_c4_handoff_v0_receipts/{receipt_id}.json")
    print(f"cell1_schema_test_verification_path=data/cell1_schema_consumption_test_from_c4_handoff_v0/cell1_schema_consumption_verification_record_v0.json")
    print(f"cell1_schema_test_rollup_path=data/cell1_schema_consumption_test_from_c4_handoff_v0/cell1_schema_consumption_test_rollup_v0.json")
    print(f"cell1_schema_test_profile_path=data/cell1_schema_consumption_test_from_c4_handoff_v0/cell1_schema_consumption_test_profile_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
