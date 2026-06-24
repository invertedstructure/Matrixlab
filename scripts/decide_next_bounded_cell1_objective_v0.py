#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_BOUNDED_CELL1_OBJECTIVE_V0"
TARGET_UNIT_ID = "cell1.next_bounded_objective_decision.v0"
LAYER = "CELL_1 / STRATEGIC_DECISION_SURFACE"
MODE = "DECIDE / CLASSIFY / NO_EXECUTION"
BUILD_MODE = "NEXT_OBJECTIVE_DECISION_ONLY"

SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_ID = "e1bc0ed0"
SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0_receipts" / "e1bc0ed0.json"
SOURCE_CELL1_REFERENCE_PACKET_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0" / "cell1_schema_test_frozen_reference_packet_v0.json"
SOURCE_CELL1_NEXT_DECISION_SURFACE_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0" / "cell1_schema_test_next_decision_surface_v0.json"
SOURCE_CELL1_BOUNDARY_AUDIT_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0" / "cell1_schema_test_boundary_audit_v0.json"
SOURCE_CELL1_REVIEW_ROLLUP_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0" / "cell1_schema_test_review_or_close_rollup_v0.json"
SOURCE_CELL1_REVIEW_PROFILE_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0" / "cell1_schema_test_review_or_close_profile_v0.json"
SOURCE_CELL1_CLOSURE_DECISION_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0" / "cell1_schema_test_closure_decision_v0.json"

SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID = "e6b0fd97"
SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0_receipts" / "e6b0fd97.json"
SOURCE_CELL1_SCHEMA_TEST_ROLLUP_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0" / "cell1_schema_consumption_test_rollup_v0.json"
SOURCE_CELL1_SCHEMA_TEST_VERIFICATION_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0" / "cell1_schema_consumption_verification_record_v0.json"

SOURCE_C4_CONSUMPTION_RECEIPT_ID = "c56792b7"
SOURCE_C4_CONSUMPTION_RECEIPT_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0_receipts" / "c56792b7.json"
SOURCE_CELL1_INTAKE_PACKET_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0" / "cell1_intake_packet_v0.json"
SOURCE_C4_HANDOFF_PACKET_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0" / "cell1_handoff_packet_v0.json"
SOURCE_C4_CONSUMPTION_ROLLUP_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0" / "c4_consumption_rollup_v0.json"

SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID = "71bd1d92"
SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0_receipts" / "71bd1d92.json"
SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0" / "accepted_proposal_packet_v0.json"
SOURCE_REVIEW_DECISION_RECORD_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0" / "review_decision_record_v0.json"

SOURCE_C1_PATCH_RECEIPT_ID = "fffa3dd5"
SOURCE_C1_PATCH_RECEIPT_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0_receipts" / "fffa3dd5.json"
SOURCE_C1_PATCH_SCHEMA_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0" / "proposal_packet_schema_v0_1.json"

SOURCE_C2_RECEIPT_ID = "348dabde"
SOURCE_C2_RECEIPT_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts" / "348dabde.json"
SOURCE_C2_LANE_REGISTRY_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "taxonomy_lane_registry_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_PATH,
    SOURCE_CELL1_REFERENCE_PACKET_PATH,
    SOURCE_CELL1_NEXT_DECISION_SURFACE_PATH,
    SOURCE_CELL1_BOUNDARY_AUDIT_PATH,
    SOURCE_CELL1_REVIEW_ROLLUP_PATH,
    SOURCE_CELL1_REVIEW_PROFILE_PATH,
    SOURCE_CELL1_CLOSURE_DECISION_PATH,
    SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH,
    SOURCE_CELL1_SCHEMA_TEST_ROLLUP_PATH,
    SOURCE_CELL1_SCHEMA_TEST_VERIFICATION_PATH,
    SOURCE_C4_CONSUMPTION_RECEIPT_PATH,
    SOURCE_CELL1_INTAKE_PACKET_PATH,
    SOURCE_C4_HANDOFF_PACKET_PATH,
    SOURCE_C4_CONSUMPTION_ROLLUP_PATH,
    SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH,
    SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH,
    SOURCE_REVIEW_DECISION_RECORD_PATH,
    SOURCE_C1_PATCH_RECEIPT_PATH,
    SOURCE_C1_PATCH_SCHEMA_PATH,
    SOURCE_C2_RECEIPT_PATH,
    SOURCE_C2_LANE_REGISTRY_PATH,
]

OUT_DIR = ROOT / "data" / "cell1_next_bounded_objective_decision_v0"
RECEIPT_DIR = ROOT / "data" / "cell1_next_bounded_objective_decision_v0_receipts"

SOURCE_SURFACE_PATH = OUT_DIR / "source_surface_v0.json"
REFERENCE_READOUT_PATH = OUT_DIR / "reference_object_readout_v0.json"
CANDIDATE_RECORDS_PATH = OUT_DIR / "objective_candidate_records_v0.jsonl"
DECISION_RECORD_PATH = OUT_DIR / "objective_decision_record_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "objective_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "objective_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "objective_profile_v0.json"
REPORT_PATH = OUT_DIR / "objective_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "objective_transition_trace.json"

SELECTED_DECISION_CLASS = "CELL1_OBJECTIVE_HANDOFF_RETURN_LOOP_TEST"
RECOMMENDED_NEXT = "DESIGN_CELL1_HANDOFF_RETURN_LOOP_TEST_V0"

CLOSED_DECISION_CLASSES = [
    "CELL1_OBJECTIVE_SECOND_SCHEMA_CONSUMPTION_TEST",
    "CELL1_OBJECTIVE_MINIMAL_RUNTIME_PATCH_TEST",
    "CELL1_OBJECTIVE_HANDOFF_RETURN_LOOP_TEST",
    "CELL1_OBJECTIVE_ACCEPTED_PROPOSAL_VARIANT_TEST",
    "CELL1_OBJECTIVE_C5_PREFLIGHT_READINESS_CHECK",
    "CELL1_OBJECTIVE_CLOSE_CELL1_TRACK_FOR_NOW",
    "CELL1_OBJECTIVE_REPAIR_REFERENCE_PACKET",
    "CELL1_OBJECTIVE_REQUEST_NARROWER_EVIDENCE",
    "QUESTION_PACKET_NOT_COMMAND",
]

ZERO_COUNTER_KEYS = [
    "c5_opened_count",
    "general_cell1_authority_granted_count",
    "new_cell1_execution_count",
    "runtime_patch_applied_count",
    "target_file_modified_count",
    "proposal_status_promoted_count",
    "accepted_proposal_fabricated_count",
    "hidden_next_command_count",
    "source_mutation_count",
    "prior_receipt_mutation_count",
    "runtime_build_artifact_emitted_count",
    "taxonomy_registry_mutation_count",
    "next_unit_executed_count",
]

HUMAN_DECISION = {
    "decision": "DECIDE_NEXT_BOUNDED_CELL1_OBJECTIVE",
    "scope": "Select the next bounded Cell 1 objective from a closed decision set using the frozen Cell 1 schema-consumption reference object. Emit source surface, reference readout, candidate records, objective decision record, authority boundary, rollup, profile, report, transition trace, and receipt. Do not execute the selected objective, do not open C5, do not grant general Cell 1 authority, do not patch runtime, do not modify targets, do not fabricate or promote proposals, and do not emit hidden next command.",
    "authorized": [
        "consume frozen Cell 1 reference object",
        "consume Cell 1 review/closure receipt",
        "enumerate closed next-objective candidates",
        "select one bounded next objective",
        "emit authority boundary",
        "emit decision receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "execute selected next objective",
        "open C5",
        "grant general Cell 1 authority",
        "apply runtime patch",
        "modify target files",
        "promote proposal status",
        "fabricate accepted proposal",
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

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def validate_source_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    review_receipt = read_json(SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_PATH)
    reference = read_json(SOURCE_CELL1_REFERENCE_PACKET_PATH)
    next_surface = read_json(SOURCE_CELL1_NEXT_DECISION_SURFACE_PATH)
    audit = read_json(SOURCE_CELL1_BOUNDARY_AUDIT_PATH)
    review_rollup = read_json(SOURCE_CELL1_REVIEW_ROLLUP_PATH)
    review_profile = read_json(SOURCE_CELL1_REVIEW_PROFILE_PATH)
    closure = read_json(SOURCE_CELL1_CLOSURE_DECISION_PATH)
    schema_test_receipt = read_json(SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH)
    schema_rollup = read_json(SOURCE_CELL1_SCHEMA_TEST_ROLLUP_PATH)
    verification = read_json(SOURCE_CELL1_SCHEMA_TEST_VERIFICATION_PATH)
    c4_receipt = read_json(SOURCE_C4_CONSUMPTION_RECEIPT_PATH)
    c4_rollup = read_json(SOURCE_C4_CONSUMPTION_ROLLUP_PATH)
    accepted_receipt = read_json(SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH)
    accepted_packet = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    review_decision = read_json(SOURCE_REVIEW_DECISION_RECORD_PATH)
    c1_receipt = read_json(SOURCE_C1_PATCH_RECEIPT_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)

    if review_receipt.get("receipt_id") != SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_ID or review_receipt.get("gate") != "PASS":
        failures.append("cell1_review_receipt_not_pass")
    if review_receipt.get("terminal", {}).get("stop_code") != "STOP_CELL1_SCHEMA_CONSUMPTION_TEST_CLOSED_REFERENCE_ONLY":
        failures.append("cell1_review_receipt_wrong_terminal")
    if reference.get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("reference_not_frozen")
    if closure.get("decision") != "CLOSE_AND_FREEZE_REFERENCE":
        failures.append("closure_decision_not_closed")
    if review_profile.get("status") != "CELL1_SCHEMA_CONSUMPTION_TEST_CLOSED_REFERENCE_ONLY":
        failures.append("review_profile_not_closed")
    if audit.get("boundary_status") != "PASS" or audit.get("zero_counters_clean") is not True:
        failures.append("boundary_audit_not_clean")
    if review_rollup.get("closure_status") != "CLOSED_REFERENCE_ONLY":
        failures.append("review_rollup_not_closed")
    if review_rollup.get("c5_opened_count") != 0:
        failures.append("review_rollup_c5_opened")
    if next_surface.get("next_command_goal") is not None:
        failures.append("next_decision_surface_has_hidden_command")
    if "C5 domain shift" not in next_surface.get("explicitly_not_licensed", []):
        failures.append("next_decision_surface_missing_c5_block")
    if schema_test_receipt.get("receipt_id") != SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID or schema_test_receipt.get("gate") != "PASS":
        failures.append("schema_test_receipt_not_pass")
    if schema_rollup.get("cell1_schema_consumption_tests_run") != 1:
        failures.append("schema_test_run_count_not_one")
    if schema_rollup.get("cell1_bounded_execution_opened_count") != 1:
        failures.append("schema_test_bounded_execution_count_not_one")
    if verification.get("verification_status") != "PASS" or verification.get("verification_scope") != "SCHEMA_CONSUMPTION_TEST_ONLY":
        failures.append("schema_test_verification_not_schema_only_pass")
    if c4_receipt.get("receipt_id") != SOURCE_C4_CONSUMPTION_RECEIPT_ID or c4_receipt.get("gate") != "PASS":
        failures.append("c4_consumption_receipt_not_pass")
    if c4_rollup.get("accepted_proposals_consumed") != 1:
        failures.append("c4_consumption_did_not_consume_accepted_proposal")
    if accepted_receipt.get("receipt_id") != SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID or accepted_receipt.get("gate") != "PASS":
        failures.append("accepted_proposal_receipt_not_pass")
    if accepted_packet.get("status") != "ACCEPTED_FOR_BUILD":
        failures.append("accepted_packet_not_accepted_for_build")
    if review_decision.get("review_decision") != "ACCEPTED_FOR_BUILD":
        failures.append("review_decision_not_accepted_for_build")
    if c1_receipt.get("receipt_id") != SOURCE_C1_PATCH_RECEIPT_ID or c1_receipt.get("gate") != "PASS":
        failures.append("c1_patch_basis_not_pass")
    if c2_receipt.get("receipt_id") != SOURCE_C2_RECEIPT_ID or c2_receipt.get("gate") != "PASS":
        failures.append("c2_basis_not_pass")
    return failures

def source_surface() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_next_bounded_objective_source_surface_v0",
        "source_cell1_review_receipt_id": SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_ID,
        "source_cell1_review_receipt_ref": rel(SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_PATH),
        "source_frozen_reference_packet_ref": rel(SOURCE_CELL1_REFERENCE_PACKET_PATH),
        "source_next_decision_surface_ref": rel(SOURCE_CELL1_NEXT_DECISION_SURFACE_PATH),
        "source_boundary_audit_ref": rel(SOURCE_CELL1_BOUNDARY_AUDIT_PATH),
        "source_review_rollup_ref": rel(SOURCE_CELL1_REVIEW_ROLLUP_PATH),
        "source_cell1_schema_test_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "source_c4_consumption_receipt_id": SOURCE_C4_CONSUMPTION_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "surface_status": "EXPLICIT_FROZEN_REFERENCE_DECISION_SURFACE",
    }

def reference_readout() -> Dict[str, Any]:
    reference = read_json(SOURCE_CELL1_REFERENCE_PACKET_PATH)
    schema_rollup = read_json(SOURCE_CELL1_SCHEMA_TEST_ROLLUP_PATH)
    verification = read_json(SOURCE_CELL1_SCHEMA_TEST_VERIFICATION_PATH)
    return {
        "schema_version": "cell1_next_bounded_objective_reference_readout_v0",
        "reference_id": reference.get("reference_id"),
        "reference_status": reference.get("reference_status"),
        "source_reference_packet_ref": rel(SOURCE_CELL1_REFERENCE_PACKET_PATH),
        "reference_proves": [
            "C4 to Cell 1 handoff can be consumed at schema level.",
            "One accepted proposal packet can bind to the Cell 1 schema-consumption surface.",
            "A bounded Cell 1 schema-consumption execution can complete and verify schema-only.",
        ],
        "reference_does_not_prove": [
            "Cell 1 can return typed result objects through the loop.",
            "Cell 1 can apply runtime patches safely.",
            "Cell 1 has general builder authority.",
            "C5 is authorized.",
            "A single proposal family proves transfer across proposal variants.",
        ],
        "observed_positive_counters": {
            "cell1_schema_consumption_tests_run": schema_rollup.get("cell1_schema_consumption_tests_run"),
            "cell1_schema_consumption_tests_passed": schema_rollup.get("cell1_schema_consumption_tests_passed"),
            "cell1_bounded_execution_opened_count": schema_rollup.get("cell1_bounded_execution_opened_count"),
            "schema_consumption_verification_pass_count": schema_rollup.get("schema_consumption_verification_pass_count"),
        },
        "verification_scope": verification.get("verification_scope"),
    }

def objective_candidates(readout: Dict[str, Any]) -> List[Dict[str, Any]]:
    base_reasons = {
        "CELL1_OBJECTIVE_SECOND_SCHEMA_CONSUMPTION_TEST": "Safe repetition across another accepted packet, but less informative than testing the missing return edge immediately.",
        "CELL1_OBJECTIVE_MINIMAL_RUNTIME_PATCH_TEST": "Potential later objective, but current reference is schema-only and does not yet prove return-loop handling or runtime patch safety.",
        "CELL1_OBJECTIVE_HANDOFF_RETURN_LOOP_TEST": "Best next smallest edge: the reference proves C4 to Cell1 intake; it does not prove Cell1 can return a typed result through review/Cell0 without ambiguity.",
        "CELL1_OBJECTIVE_ACCEPTED_PROPOSAL_VARIANT_TEST": "Strong alternate: useful for proposal-family breadth, but return semantics are the first missing inter-cell edge.",
        "CELL1_OBJECTIVE_C5_PREFLIGHT_READINESS_CHECK": "Premature as execution or C5 opening; C5 can remain blocked until return-loop and/or runtime-patch evidence exists.",
        "CELL1_OBJECTIVE_CLOSE_CELL1_TRACK_FOR_NOW": "Valid success option, but current closed reference exposes a clear next bounded Cell1 edge.",
        "CELL1_OBJECTIVE_REPAIR_REFERENCE_PACKET": "Not selected because the frozen reference packet and boundary audit passed.",
        "CELL1_OBJECTIVE_REQUEST_NARROWER_EVIDENCE": "Not selected because the receipt surface is sufficient to choose the next bounded class.",
        "QUESTION_PACKET_NOT_COMMAND": "Not selected because the decision surface is typed enough and the closed enum is available.",
    }
    scores = {
        "CELL1_OBJECTIVE_SECOND_SCHEMA_CONSUMPTION_TEST": 60,
        "CELL1_OBJECTIVE_MINIMAL_RUNTIME_PATCH_TEST": 35,
        "CELL1_OBJECTIVE_HANDOFF_RETURN_LOOP_TEST": 95,
        "CELL1_OBJECTIVE_ACCEPTED_PROPOSAL_VARIANT_TEST": 85,
        "CELL1_OBJECTIVE_C5_PREFLIGHT_READINESS_CHECK": 30,
        "CELL1_OBJECTIVE_CLOSE_CELL1_TRACK_FOR_NOW": 50,
        "CELL1_OBJECTIVE_REPAIR_REFERENCE_PACKET": 10,
        "CELL1_OBJECTIVE_REQUEST_NARROWER_EVIDENCE": 15,
        "QUESTION_PACKET_NOT_COMMAND": 5,
    }
    candidates: List[Dict[str, Any]] = []
    for cls in CLOSED_DECISION_CLASSES:
        candidates.append({
            "schema_version": "cell1_next_bounded_objective_candidate_record_v0",
            "candidate_id": "candidate_" + sha8({"class": cls, "source": SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_ID}),
            "decision_class": cls,
            "score": scores[cls],
            "selected": cls == SELECTED_DECISION_CLASS,
            "selection_reason": base_reasons[cls],
            "authority_boundary": {
                "may_execute_now": False,
                "may_open_c5": False,
                "may_grant_general_cell1_authority": False,
                "may_apply_runtime_patch": False,
            },
        })
    return candidates

def authority_boundary() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_next_bounded_objective_authority_boundary_v0",
        "authority_boundary_id": "cell1_next_obj_authority_" + sha8({"selected": SELECTED_DECISION_CLASS}),
        "selected_decision_class": SELECTED_DECISION_CLASS,
        "may_emit_next_objective_candidate": True,
        "may_emit_executable_command": False,
        "may_execute_next_unit": False,
        "may_open_c5": False,
        "may_grant_general_cell1_authority": False,
        "may_apply_runtime_patch": False,
        "may_modify_target_files": False,
        "may_promote_proposal_status": False,
        "may_fabricate_accepted_proposal": False,
        "must_not_infer": [
            "C5 is authorized",
            "Cell 1 is a general builder",
            "schema-consumption success proves runtime build safety",
            "one reference object proves transfer",
            "next objective is already executed",
        ],
    }

def decision_record(boundary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_next_bounded_objective_decision_v0",
        "decision_id": "cell1_next_obj_" + sha8({"source": SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_ID, "selected": SELECTED_DECISION_CLASS}),
        "source_reference_packet_ref": rel(SOURCE_CELL1_REFERENCE_PACKET_PATH),
        "source_review_receipt_ref": rel(SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_PATH),
        "selected_decision_class": SELECTED_DECISION_CLASS,
        "why_selected": "The frozen reference proves C4-to-Cell1 schema intake. The next smallest missing inter-cell edge is whether Cell1 can return a typed result object through review/Cell0 without ambiguity, authority leakage, hidden continuation, or label confusion.",
        "why_not_c5_yet": "C5 remains blocked because the current evidence is schema-consumption-only. No runtime patch, target modification, return-loop handling, or multi-family transfer evidence has been established.",
        "why_not_general_cell1_authority": "One bounded schema-consumption reference proves a local path, not general builder competence. Authority remains limited to selected bounded objectives.",
        "required_inputs_for_next_unit": [
            rel(DECISION_RECORD_PATH),
            rel(AUTHORITY_BOUNDARY_PATH),
            rel(SOURCE_CELL1_REFERENCE_PACKET_PATH),
            rel(SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_PATH),
            rel(SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH),
            rel(SOURCE_C4_CONSUMPTION_RECEIPT_PATH),
            rel(SOURCE_C2_LANE_REGISTRY_PATH),
        ],
        "forbidden_inputs_for_next_unit": [
            "ambient workspace inference",
            "latest-file guessing",
            "mtime selection",
            "unreviewed proposal packet",
            "PROPOSED_ONLY packet treated as accepted",
            "runtime build target files",
            "C5 planning treated as authorization",
            "general Cell 1 builder authority",
        ],
        "authority_boundary": {
            "may_emit_next_objective_candidate": boundary["may_emit_next_objective_candidate"],
            "may_emit_executable_command": boundary["may_emit_executable_command"],
            "may_execute_next_unit": boundary["may_execute_next_unit"],
            "may_open_c5": boundary["may_open_c5"],
            "may_grant_general_cell1_authority": boundary["may_grant_general_cell1_authority"],
            "may_apply_runtime_patch": boundary["may_apply_runtime_patch"],
        },
        "must_not_infer": boundary["must_not_infer"],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CELL1_NEXT_BOUNDED_OBJECTIVE_DECIDED",
            "next_command_goal": None,
        },
    }

def rollup(candidates: List[Dict[str, Any]], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_next_bounded_objective_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_cell1_schema_review_receipt_id": SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_ID,
        "source_cell1_schema_test_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "source_c4_consumption_receipt_id": SOURCE_C4_CONSUMPTION_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "candidate_count": len(candidates),
        "selected_decision_class": decision["selected_decision_class"],
        "decision_record_emitted_count": 1,
        "authority_boundary_emitted_count": 1,
        "objective_executed_count": 0,
        "next_command_goal_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "new_cell1_execution_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "proposal_status_promoted_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "runtime_build_artifact_emitted_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "next_unit_executed_count": 0,
        "recommended_next": RECOMMENDED_NEXT,
    }

def profile(rollup_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_next_bounded_objective_profile_v0",
        "profile_id": "cell1_next_obj_" + sha8({"selected": rollup_obj["selected_decision_class"], "source": SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_ID}),
        "status": "CELL1_NEXT_BOUNDED_OBJECTIVE_DECIDED",
        "selected_decision_class": rollup_obj["selected_decision_class"],
        "recommended_next": rollup_obj["recommended_next"],
        "objective_executed": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "next_command_goal": None,
    }

def report(rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_next_bounded_objective_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_review_receipt_consumed_count": 1,
        "frozen_reference_packet_consumed_count": 1,
        "next_decision_surface_consumed_count": 1,
        "reference_readout_emitted_count": 1,
        "objective_candidates_emitted_count": rollup_obj["candidate_count"],
        "decision_record_emitted_count": 1,
        "authority_boundary_emitted_count": 1,
        "profile_status": profile_obj["status"],
        "selected_decision_class": rollup_obj["selected_decision_class"],
        "recommended_next_handling": rollup_obj["recommended_next"],
        "objective_executed_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "new_cell1_execution_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "proposal_status_promoted_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
    }

def transition_trace(decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_next_bounded_objective_transition_trace_v0",
        "trace": [
            {
                "step": "consume_closed_reference",
                "question": "is there a frozen bounded Cell1 reference",
                "answer": SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_ID,
                "taken": "read_reference_evidence",
            },
            {
                "step": "read_reference_evidence",
                "question": "what did the reference prove and not prove",
                "answer": "schema intake proved; return loop not proved",
                "taken": "enumerate_closed_objective_classes",
            },
            {
                "step": "enumerate_closed_objective_classes",
                "question": "which bounded class covers the smallest missing Cell1 edge",
                "answer": SELECTED_DECISION_CLASS,
                "taken": "emit_authority_boundary",
            },
            {
                "step": "emit_authority_boundary",
                "question": "did the unit avoid execution/C5/authority widening",
                "answer": "yes",
                "taken": "stop",
            },
        ],
        "terminal": decision["terminal"],
    }

def validate_outputs(readout: Dict[str, Any], candidates: List[Dict[str, Any]], boundary: Dict[str, Any], decision: Dict[str, Any], rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any], report_obj: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if readout.get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("reference_readout_not_frozen")
    if len(candidates) != len(CLOSED_DECISION_CLASSES):
        failures.append("candidate_count_wrong")
    if decision.get("selected_decision_class") not in CLOSED_DECISION_CLASSES:
        failures.append("selected_class_not_closed_enum")
    if decision.get("selected_decision_class") != SELECTED_DECISION_CLASS:
        failures.append("selected_class_wrong")
    if not decision.get("why_not_c5_yet"):
        failures.append("why_not_c5_missing")
    if not decision.get("why_not_general_cell1_authority"):
        failures.append("why_not_general_authority_missing")
    if decision.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("decision_hidden_next_command")
    if boundary.get("may_emit_executable_command") is not False:
        failures.append("authority_allows_executable_command")
    if boundary.get("may_execute_next_unit") is not False:
        failures.append("authority_allows_execution")
    if boundary.get("may_open_c5") is not False:
        failures.append("authority_allows_c5")
    if boundary.get("may_grant_general_cell1_authority") is not False:
        failures.append("authority_allows_general_cell1")
    if boundary.get("may_apply_runtime_patch") is not False:
        failures.append("authority_allows_runtime_patch")
    if boundary.get("may_modify_target_files") is not False:
        failures.append("authority_allows_target_file_modification")
    if rollup_obj.get("candidate_count") != len(CLOSED_DECISION_CLASSES):
        failures.append("rollup_candidate_count_wrong")
    if rollup_obj.get("selected_decision_class") != SELECTED_DECISION_CLASS:
        failures.append("rollup_selected_class_wrong")
    for key in ZERO_COUNTER_KEYS:
        if rollup_obj.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup_obj.get(key)}")
    if profile_obj.get("objective_executed") is not False:
        failures.append("profile_claims_objective_executed")
    if profile_obj.get("c5_opened") is not False:
        failures.append("profile_claims_c5")
    if profile_obj.get("general_cell1_authority_granted") is not False:
        failures.append("profile_claims_general_cell1")
    if profile_obj.get("runtime_patch_applied") is not False:
        failures.append("profile_claims_runtime_patch")
    if profile_obj.get("target_file_modified") is not False:
        failures.append("profile_claims_target_file_modified")
    if profile_obj.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")
    for key in [
        "objective_executed_count",
        "c5_opened_count",
        "general_cell1_authority_granted_count",
        "new_cell1_execution_count",
        "runtime_patch_applied_count",
        "target_file_modified_count",
        "proposal_status_promoted_count",
        "accepted_proposal_fabricated_count",
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
    if terminal.get("stop_code") != "STOP_CELL1_NEXT_BOUNDED_OBJECTIVE_DECIDED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    readout = read_json(REFERENCE_READOUT_PATH)
    candidates = [json.loads(line) for line in CANDIDATE_RECORDS_PATH.read_text().splitlines() if line.strip()]
    boundary = read_json(AUTHORITY_BOUNDARY_PATH)
    decision = read_json(DECISION_RECORD_PATH)
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

    bad_boundary = copy.deepcopy(boundary)
    bad_boundary["may_open_c5"] = True
    add("c5_opened_by_decision_fail", validate_outputs(readout, candidates, bad_boundary, decision, rollup_obj, profile_obj, report_obj), "authority_allows_c5")

    bad_boundary = copy.deepcopy(boundary)
    bad_boundary["may_grant_general_cell1_authority"] = True
    add("general_cell1_authority_granted_fail", validate_outputs(readout, candidates, bad_boundary, decision, rollup_obj, profile_obj, report_obj), "authority_allows_general_cell1")

    bad_boundary = copy.deepcopy(boundary)
    bad_boundary["may_execute_next_unit"] = True
    add("new_cell1_execution_started_fail", validate_outputs(readout, candidates, bad_boundary, decision, rollup_obj, profile_obj, report_obj), "authority_allows_execution")

    bad_boundary = copy.deepcopy(boundary)
    bad_boundary["may_apply_runtime_patch"] = True
    add("runtime_patch_applied_fail", validate_outputs(readout, candidates, bad_boundary, decision, rollup_obj, profile_obj, report_obj), "authority_allows_runtime_patch")

    bad_boundary = copy.deepcopy(boundary)
    bad_boundary["may_modify_target_files"] = True
    add("target_file_modified_fail", validate_outputs(readout, candidates, bad_boundary, decision, rollup_obj, profile_obj, report_obj), "authority_allows_target_file_modification")

    bad_decision = copy.deepcopy(decision)
    bad_decision["selected_decision_class"] = "NOT_IN_ENUM"
    add("selected_class_not_closed_enum_fail", validate_outputs(readout, candidates, boundary, bad_decision, rollup_obj, profile_obj, report_obj), "selected_class_not_closed_enum")

    bad_decision = copy.deepcopy(decision)
    bad_decision["why_not_c5_yet"] = ""
    add("schema_success_counted_as_c5_authority_fail", validate_outputs(readout, candidates, boundary, bad_decision, rollup_obj, profile_obj, report_obj), "why_not_c5_missing")

    bad_decision = copy.deepcopy(decision)
    bad_decision["why_not_general_cell1_authority"] = ""
    add("schema_success_counted_as_general_authority_fail", validate_outputs(readout, candidates, boundary, bad_decision, rollup_obj, profile_obj, report_obj), "why_not_general_authority_missing")

    bad_decision = copy.deepcopy(decision)
    bad_decision["terminal"]["next_command_goal"] = "RUN_CELL1_HANDOFF_RETURN_LOOP_TEST"
    add("decision_surface_emits_hidden_command_fail", validate_outputs(readout, candidates, boundary, bad_decision, rollup_obj, profile_obj, report_obj), "decision_hidden_next_command")

    bad_readout = copy.deepcopy(readout)
    bad_readout["reference_status"] = "NOT_FROZEN"
    add("reference_object_not_frozen_fail", validate_outputs(bad_readout, candidates, boundary, decision, rollup_obj, profile_obj, report_obj), "reference_readout_not_frozen")

    bad_candidates = candidates[:-1]
    add("candidate_count_wrong_fail", validate_outputs(readout, bad_candidates, boundary, decision, rollup_obj, profile_obj, report_obj), "candidate_count_wrong")

    for case, counter in [
        ("c5_opened_counter_fail", "c5_opened_count"),
        ("general_cell1_authority_counter_fail", "general_cell1_authority_granted_count"),
        ("new_cell1_execution_counter_fail", "new_cell1_execution_count"),
        ("runtime_patch_counter_fail", "runtime_patch_applied_count"),
        ("target_file_modified_counter_fail", "target_file_modified_count"),
        ("proposal_status_promoted_fail", "proposal_status_promoted_count"),
        ("accepted_proposal_fabricated_fail", "accepted_proposal_fabricated_count"),
        ("hidden_next_command_fail", "hidden_next_command_count"),
        ("source_mutation_fail", "source_mutation_count"),
        ("prior_receipt_mutation_fail", "prior_receipt_mutation_count"),
        ("runtime_build_artifact_emitted_fail", "runtime_build_artifact_emitted_count"),
        ("taxonomy_registry_mutated_fail", "taxonomy_registry_mutation_count"),
        ("next_unit_executed_fail", "next_unit_executed_count"),
    ]:
        bad_rollup = copy.deepcopy(rollup_obj)
        bad_report = copy.deepcopy(report_obj)
        bad_rollup[counter] = 1
        if counter in bad_report:
            bad_report[counter] = 1
        add(case, validate_outputs(readout, candidates, boundary, decision, bad_rollup, profile_obj, bad_report), counter)

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_CELL1_NEXT_OBJECTIVE_EVIDENCE_REQUEST_REQUIRED", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "cell1_next_bounded_objective_decision_receipt_v0",
            "receipt_type": "CELL1_NEXT_BOUNDED_OBJECTIVE_DECISION_RECEIPT",
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
        print(f"cell1_next_objective_receipt_id={receipt_id}")
        print(f"cell1_next_objective_receipt_path=data/cell1_next_bounded_objective_decision_v0_receipts/{receipt_id}.json")
        return 1

    readout = reference_readout()
    candidates = objective_candidates(readout)
    boundary = authority_boundary()
    decision = decision_record(boundary)
    rollup_obj = rollup(candidates, decision)
    profile_obj = profile(rollup_obj)
    report_obj = report(rollup_obj, profile_obj)
    trace = transition_trace(decision)

    write_json(SOURCE_SURFACE_PATH, source_surface())
    write_json(REFERENCE_READOUT_PATH, readout)
    write_jsonl(CANDIDATE_RECORDS_PATH, candidates)
    write_json(DECISION_RECORD_PATH, decision)
    write_json(AUTHORITY_BOUNDARY_PATH, boundary)
    write_json(ROLLUP_PATH, rollup_obj)
    write_json(PROFILE_PATH, profile_obj)
    write_json(REPORT_PATH, report_obj)
    write_json(TRANSITION_TRACE_PATH, trace)

    failures.extend(validate_outputs(readout, candidates, boundary, decision, rollup_obj, profile_obj, report_obj))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup_obj["source_mutation_count"] = 1
        report_obj["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup_obj)
        write_json(REPORT_PATH, report_obj)

    acceptance_gate_results = {
        "CELL1_NEXT_OBJ_0_SOURCE_REVIEW_RECEIPT_CONSUMED": SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_PATH.exists(),
        "CELL1_NEXT_OBJ_1_FROZEN_REFERENCE_PACKET_CONSUMED": SOURCE_CELL1_REFERENCE_PACKET_PATH.exists(),
        "CELL1_NEXT_OBJ_2_NEXT_DECISION_SURFACE_CONSUMED": SOURCE_CELL1_NEXT_DECISION_SURFACE_PATH.exists(),
        "CELL1_NEXT_OBJ_3_REFERENCE_READOUT_EMITTED": REFERENCE_READOUT_PATH.exists(),
        "CELL1_NEXT_OBJ_4_OBJECTIVE_CANDIDATES_EMITTED": CANDIDATE_RECORDS_PATH.exists() and len(candidates) == len(CLOSED_DECISION_CLASSES),
        "CELL1_NEXT_OBJ_5_SELECTED_CLASS_FROM_CLOSED_ENUM": decision["selected_decision_class"] in CLOSED_DECISION_CLASSES,
        "CELL1_NEXT_OBJ_6_DECISION_RECORD_EMITTED": DECISION_RECORD_PATH.exists(),
        "CELL1_NEXT_OBJ_7_AUTHORITY_BOUNDARY_EMITTED": AUTHORITY_BOUNDARY_PATH.exists(),
        "CELL1_NEXT_OBJ_8_WHY_NOT_C5_OR_GENERAL_AUTHORITY_STATED": bool(decision["why_not_c5_yet"]) and bool(decision["why_not_general_cell1_authority"]),
        "CELL1_NEXT_OBJ_9_NO_C5_OPENED": rollup_obj["c5_opened_count"] == 0,
        "CELL1_NEXT_OBJ_10_NO_GENERAL_CELL1_AUTHORITY_GRANTED": rollup_obj["general_cell1_authority_granted_count"] == 0,
        "CELL1_NEXT_OBJ_11_NO_NEW_CELL1_EXECUTION": rollup_obj["new_cell1_execution_count"] == 0,
        "CELL1_NEXT_OBJ_12_NO_RUNTIME_PATCH": rollup_obj["runtime_patch_applied_count"] == 0,
        "CELL1_NEXT_OBJ_13_NO_TARGET_FILE_MODIFICATION": rollup_obj["target_file_modified_count"] == 0,
        "CELL1_NEXT_OBJ_14_NO_PROPOSAL_STATUS_PROMOTION": rollup_obj["proposal_status_promoted_count"] == 0,
        "CELL1_NEXT_OBJ_15_NO_ACCEPTED_PROPOSAL_FABRICATION": rollup_obj["accepted_proposal_fabricated_count"] == 0,
        "CELL1_NEXT_OBJ_16_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
        "CELL1_NEXT_OBJ_17_NO_HIDDEN_NEXT_COMMAND": rollup_obj["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate_name, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate_name}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_cell1_review": SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_ID,
        "selected": SELECTED_DECISION_CLASS,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "reference_object_readout": rel(REFERENCE_READOUT_PATH),
        "objective_candidate_records": rel(CANDIDATE_RECORDS_PATH),
        "objective_decision_record": rel(DECISION_RECORD_PATH),
        "objective_authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
        "rollup": rel(ROLLUP_PATH),
        "profile": rel(PROFILE_PATH),
        "report": rel(REPORT_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_review_receipt": rel(SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_PATH),
        "source_frozen_reference_packet": rel(SOURCE_CELL1_REFERENCE_PACKET_PATH),
        "source_next_decision_surface": rel(SOURCE_CELL1_NEXT_DECISION_SURFACE_PATH),
        "source_boundary_audit": rel(SOURCE_CELL1_BOUNDARY_AUDIT_PATH),
        "source_cell1_schema_test_receipt": rel(SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH),
        "source_c4_consumption_receipt": rel(SOURCE_C4_CONSUMPTION_RECEIPT_PATH),
        "source_accepted_proposal_packet": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "source_c1_patch_schema": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "source_c2_lane_registry": rel(SOURCE_C2_LANE_REGISTRY_PATH),
    }

    guards = {
        "build_mode_next_objective_decision_only": BUILD_MODE == "NEXT_OBJECTIVE_DECISION_ONLY",
        "selected_from_closed_enum": decision["selected_decision_class"] in CLOSED_DECISION_CLASSES,
        "selected_handoff_return_loop_test": decision["selected_decision_class"] == SELECTED_DECISION_CLASS,
        "may_emit_next_objective_candidate": True,
        "may_emit_executable_command": False,
        "may_execute_next_unit": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "new_cell1_execution": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "proposal_status_promoted": False,
        "accepted_proposal_fabricated": False,
        "hidden_next_command": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
    }

    receipt = {
        "schema_version": "cell1_next_bounded_objective_decision_receipt_v0",
        "receipt_type": "CELL1_NEXT_BOUNDED_OBJECTIVE_DECISION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "frozen Cell 1 schema-consumption reference packet",
        "source_cell1_schema_review_receipt_id": SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_ID,
        "source_cell1_schema_test_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "source_c4_consumption_receipt_id": SOURCE_C4_CONSUMPTION_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "cell1_next_objective_summary": {
            "profile_status": profile_obj["status"],
            "candidate_count": rollup_obj["candidate_count"],
            "selected_decision_class": rollup_obj["selected_decision_class"],
            "why_selected": decision["why_selected"],
            "why_not_c5_yet": decision["why_not_c5_yet"],
            "why_not_general_cell1_authority": decision["why_not_general_cell1_authority"],
            "recommended_next": rollup_obj["recommended_next"],
            "objective_executed": False,
            "c5_opened": False,
            "general_cell1_authority_granted": False,
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        },
        "aggregate_metrics": {
            **{k: v for k, v in report_obj.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
            "rollup": rollup_obj,
            "source_mutation_count": 1 if source_mutation_detected else report_obj["source_mutation_count"],
        },
        "acceptance_gate_results": acceptance_gate_results,
        "cell1_next_objective_guards": guards,
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
    if len(negative_controls) != 24 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
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
    print(f"cell1_next_objective_receipt_id={receipt_id}")
    print(f"cell1_next_objective_receipt_path=data/cell1_next_bounded_objective_decision_v0_receipts/{receipt_id}.json")
    print(f"cell1_next_objective_decision_path=data/cell1_next_bounded_objective_decision_v0/objective_decision_record_v0.json")
    print(f"cell1_next_objective_rollup_path=data/cell1_next_bounded_objective_decision_v0/objective_rollup_v0.json")
    print(f"cell1_next_objective_profile_path=data/cell1_next_bounded_objective_decision_v0/objective_profile_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
