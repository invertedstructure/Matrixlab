#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_BOUNDED_CELL1_OBJECTIVE_AFTER_RETURN_LOOP_V0"
TARGET_UNIT_ID = "cell1.next_bounded_objective.after_return_loop.v0"
LAYER = "CELL_1 / STRATEGIC_DECISION_SURFACE_AFTER_RETURN_LOOP"
MODE = "DECIDE / CLASSIFY / NO_EXECUTION"
BUILD_MODE = "NEXT_OBJECTIVE_AFTER_RETURN_LOOP_DECISION_ONLY"

SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID = "1d7c0a9b"
SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH = ROOT / "data" / "cell1_handoff_return_loop_review_or_close_v0_receipts" / "1d7c0a9b.json"
SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH = ROOT / "data" / "cell1_handoff_return_loop_review_or_close_v0" / "handoff_return_loop_frozen_reference_packet_v0.json"
SOURCE_HANDOFF_RETURN_NEXT_DECISION_SURFACE_PATH = ROOT / "data" / "cell1_handoff_return_loop_review_or_close_v0" / "handoff_return_loop_next_decision_surface_v0.json"
SOURCE_HANDOFF_RETURN_CLOSURE_DECISION_PATH = ROOT / "data" / "cell1_handoff_return_loop_review_or_close_v0" / "handoff_return_loop_closure_decision_v0.json"
SOURCE_HANDOFF_RETURN_ROLLUP_PATH = ROOT / "data" / "cell1_handoff_return_loop_review_or_close_v0" / "handoff_return_loop_review_or_close_rollup_v0.json"
SOURCE_HANDOFF_RETURN_PROFILE_PATH = ROOT / "data" / "cell1_handoff_return_loop_review_or_close_v0" / "handoff_return_loop_review_or_close_profile_v0.json"
SOURCE_HANDOFF_RETURN_READOUT_PATH = ROOT / "data" / "cell1_handoff_return_loop_review_or_close_v0" / "handoff_return_loop_readout_v0.json"
SOURCE_HANDOFF_RETURN_BOUNDARY_AUDIT_PATH = ROOT / "data" / "cell1_handoff_return_loop_review_or_close_v0" / "handoff_return_loop_boundary_audit_v0.json"

SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID = "35e62eaf"
SOURCE_HANDOFF_RETURN_TEST_RECEIPT_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_run_v0_receipts" / "35e62eaf.json"
SOURCE_HANDOFF_RETURN_PACKET_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_run_v0" / "cell1_handoff_return_result_packet_v0.json"
SOURCE_HANDOFF_RETURN_CLASSIFICATION_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_run_v0" / "return_packet_classification_record_v0.json"

SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID = "e1bc0ed0"
SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0_receipts" / "e1bc0ed0.json"
SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0" / "cell1_schema_test_frozen_reference_packet_v0.json"

SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID = "e6b0fd97"
SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0_receipts" / "e6b0fd97.json"

SOURCE_C4_CONSUMPTION_RECEIPT_ID = "c56792b7"
SOURCE_C4_CONSUMPTION_RECEIPT_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0_receipts" / "c56792b7.json"

SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID = "71bd1d92"
SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0_receipts" / "71bd1d92.json"
SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0" / "accepted_proposal_packet_v0.json"

SOURCE_C1_PATCH_RECEIPT_ID = "fffa3dd5"
SOURCE_C1_PATCH_RECEIPT_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0_receipts" / "fffa3dd5.json"
SOURCE_C1_PATCH_SCHEMA_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0" / "proposal_packet_schema_v0_1.json"

SOURCE_C2_RECEIPT_ID = "348dabde"
SOURCE_C2_RECEIPT_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts" / "348dabde.json"
SOURCE_C2_LANE_REGISTRY_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "taxonomy_lane_registry_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH,
    SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH,
    SOURCE_HANDOFF_RETURN_NEXT_DECISION_SURFACE_PATH,
    SOURCE_HANDOFF_RETURN_CLOSURE_DECISION_PATH,
    SOURCE_HANDOFF_RETURN_ROLLUP_PATH,
    SOURCE_HANDOFF_RETURN_PROFILE_PATH,
    SOURCE_HANDOFF_RETURN_READOUT_PATH,
    SOURCE_HANDOFF_RETURN_BOUNDARY_AUDIT_PATH,
    SOURCE_HANDOFF_RETURN_TEST_RECEIPT_PATH,
    SOURCE_HANDOFF_RETURN_PACKET_PATH,
    SOURCE_HANDOFF_RETURN_CLASSIFICATION_PATH,
    SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_PATH,
    SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH,
    SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH,
    SOURCE_C4_CONSUMPTION_RECEIPT_PATH,
    SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH,
    SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH,
    SOURCE_C1_PATCH_RECEIPT_PATH,
    SOURCE_C1_PATCH_SCHEMA_PATH,
    SOURCE_C2_RECEIPT_PATH,
    SOURCE_C2_LANE_REGISTRY_PATH,
]

OUT_DIR = ROOT / "data" / "cell1_next_bounded_objective_after_return_loop_v0"
RECEIPT_DIR = ROOT / "data" / "cell1_next_bounded_objective_after_return_loop_v0_receipts"

SOURCE_SURFACE_PATH = OUT_DIR / "source_surface_v0.json"
REFERENCE_STACK_READOUT_PATH = OUT_DIR / "reference_stack_readout_v0.json"
OBJECTIVE_CANDIDATES_PATH = OUT_DIR / "objective_candidate_records_v0.jsonl"
OBJECTIVE_DECISION_PATH = OUT_DIR / "objective_decision_record_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "objective_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "objective_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "objective_profile_v0.json"
REPORT_PATH = OUT_DIR / "objective_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "objective_transition_trace.json"

SELECTED_DECISION_CLASS = "CELL1_OBJECTIVE_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK"
RECOMMENDED_NEXT = "DESIGN_CELL1_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK_V0"

CLOSED_DECISION_CLASSES = [
    "CELL1_OBJECTIVE_ACCEPTED_PROPOSAL_VARIANT_TEST",
    "CELL1_OBJECTIVE_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK",
    "CELL1_OBJECTIVE_HANDOFF_RETURN_LOOP_VARIANT_TEST",
    "CELL1_OBJECTIVE_C5_PREFLIGHT_READINESS_CHECK",
    "CELL1_OBJECTIVE_CLOSE_CELL1_TRACK_FOR_NOW",
    "CELL1_OBJECTIVE_REPAIR_REFERENCE_STACK",
    "CELL1_OBJECTIVE_REQUEST_NARROWER_EVIDENCE",
    "QUESTION_PACKET_NOT_COMMAND",
]

ZERO_COUNTER_KEYS = [
    "objective_executed_count",
    "runtime_patch_applied_count",
    "target_file_modified_count",
    "c5_opened_count",
    "general_cell1_authority_granted_count",
    "taxonomy_registry_mutation_count",
    "proposal_status_promoted_count",
    "accepted_proposal_fabricated_count",
    "source_mutation_count",
    "prior_receipt_mutation_count",
    "hidden_next_command_count",
    "unbounded_payload_inspection_count",
]

HUMAN_DECISION = {
    "decision": "DECIDE_NEXT_BOUNDED_CELL1_OBJECTIVE_AFTER_RETURN_LOOP",
    "scope": "Select the next bounded Cell1 objective after the schema-consumption reference and handoff-return reference have both been closed and frozen. Emit source surface, reference stack readout, objective candidates, decision record, authority boundary, rollup, profile, report, transition trace, and receipt. Do not execute the selected objective, do not apply runtime patches, do not modify targets, do not open C5, do not grant general Cell1 authority, do not promote proposals, fabricate accepted proposals, inspect unbounded payloads, or emit hidden next command.",
    "authorized": [
        "consume frozen schema-consumption reference",
        "consume frozen handoff-return reference",
        "enumerate closed next-objective candidates",
        "select one bounded next objective",
        "emit authority boundary",
        "emit receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "execute selected objective",
        "apply runtime patch",
        "modify target files",
        "open C5",
        "grant general Cell1 authority",
        "mutate taxonomy registry",
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

    close_receipt = read_json(SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH)
    return_reference = read_json(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH)
    next_surface = read_json(SOURCE_HANDOFF_RETURN_NEXT_DECISION_SURFACE_PATH)
    closure = read_json(SOURCE_HANDOFF_RETURN_CLOSURE_DECISION_PATH)
    return_rollup = read_json(SOURCE_HANDOFF_RETURN_ROLLUP_PATH)
    return_profile = read_json(SOURCE_HANDOFF_RETURN_PROFILE_PATH)
    return_readout = read_json(SOURCE_HANDOFF_RETURN_READOUT_PATH)
    return_audit = read_json(SOURCE_HANDOFF_RETURN_BOUNDARY_AUDIT_PATH)
    return_test_receipt = read_json(SOURCE_HANDOFF_RETURN_TEST_RECEIPT_PATH)
    return_packet = read_json(SOURCE_HANDOFF_RETURN_PACKET_PATH)
    return_classification = read_json(SOURCE_HANDOFF_RETURN_CLASSIFICATION_PATH)
    schema_close_receipt = read_json(SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_PATH)
    schema_reference = read_json(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH)
    schema_test_receipt = read_json(SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH)
    c4_receipt = read_json(SOURCE_C4_CONSUMPTION_RECEIPT_PATH)
    accepted_receipt = read_json(SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH)
    accepted_packet = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    c1_receipt = read_json(SOURCE_C1_PATCH_RECEIPT_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)

    if close_receipt.get("receipt_id") != SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID or close_receipt.get("gate") != "PASS":
        failures.append("handoff_return_close_receipt_not_pass")
    if close_receipt.get("terminal", {}).get("stop_code") != "STOP_CELL1_HANDOFF_RETURN_LOOP_CLOSED_REFERENCE_ONLY":
        failures.append("handoff_return_close_wrong_terminal")
    if return_reference.get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("handoff_return_reference_not_frozen")
    if closure.get("decision") != "CLOSE_AND_FREEZE_HANDOFF_RETURN_REFERENCE":
        failures.append("handoff_return_closure_not_closed")
    if return_rollup.get("closure_status") != "CLOSED_REFERENCE_ONLY":
        failures.append("handoff_return_rollup_not_closed")
    if return_profile.get("status") != "CELL1_HANDOFF_RETURN_LOOP_CLOSED_REFERENCE_ONLY":
        failures.append("handoff_return_profile_not_closed")
    if return_readout.get("accepted_for_review") is not True or return_readout.get("accepted_for_build") is not False:
        failures.append("handoff_return_readout_wrong_acceptance_scope")
    if return_audit.get("boundary_status") != "PASS" or return_audit.get("zero_counters_clean") is not True:
        failures.append("handoff_return_audit_not_clean")
    if next_surface.get("next_command_goal") is not None:
        failures.append("handoff_return_next_surface_hidden_command")
    if "CELL1_OBJECTIVE_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK" not in next_surface.get("safe_next_decision_classes", []):
        failures.append("handoff_return_next_surface_missing_runtime_precheck_option")
    if return_test_receipt.get("receipt_id") != SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID or return_test_receipt.get("gate") != "PASS":
        failures.append("handoff_return_test_receipt_not_pass")
    if return_packet.get("origin_cell") != "CELL_1":
        failures.append("return_packet_origin_not_cell1")
    if return_classification.get("classification") != "RETURN_PACKET_ACCEPTED_FOR_REVIEW":
        failures.append("return_classification_not_review_accepted")
    if return_classification.get("accepted_for_build") is not False:
        failures.append("return_classification_accepts_for_build")
    if schema_close_receipt.get("receipt_id") != SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID or schema_close_receipt.get("gate") != "PASS":
        failures.append("schema_close_receipt_not_pass")
    if schema_reference.get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("schema_reference_not_frozen")
    if schema_test_receipt.get("receipt_id") != SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID or schema_test_receipt.get("gate") != "PASS":
        failures.append("schema_test_receipt_not_pass")
    if c4_receipt.get("receipt_id") != SOURCE_C4_CONSUMPTION_RECEIPT_ID or c4_receipt.get("gate") != "PASS":
        failures.append("c4_consumption_receipt_not_pass")
    if accepted_receipt.get("receipt_id") != SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID or accepted_receipt.get("gate") != "PASS":
        failures.append("accepted_proposal_receipt_not_pass")
    if accepted_packet.get("status") != "ACCEPTED_FOR_BUILD":
        failures.append("accepted_packet_not_accepted_for_build")
    if c1_receipt.get("receipt_id") != SOURCE_C1_PATCH_RECEIPT_ID or c1_receipt.get("gate") != "PASS":
        failures.append("c1_patch_receipt_not_pass")
    if c2_receipt.get("receipt_id") != SOURCE_C2_RECEIPT_ID or c2_receipt.get("gate") != "PASS":
        failures.append("c2_receipt_not_pass")
    return failures

def source_surface() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_next_objective_after_return_loop_source_surface_v0",
        "source_handoff_return_close_receipt_id": SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID,
        "source_handoff_return_close_receipt_ref": rel(SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH),
        "source_handoff_return_reference_packet_ref": rel(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH),
        "source_handoff_return_next_decision_surface_ref": rel(SOURCE_HANDOFF_RETURN_NEXT_DECISION_SURFACE_PATH),
        "source_schema_close_receipt_id": SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID,
        "source_schema_reference_packet_ref": rel(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH),
        "source_c4_consumption_receipt_id": SOURCE_C4_CONSUMPTION_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "surface_status": "EXPLICIT_POST_RETURN_LOOP_DECISION_SURFACE",
    }

def reference_stack_readout() -> Dict[str, Any]:
    schema_reference = read_json(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH)
    return_reference = read_json(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH)
    return_readout = read_json(SOURCE_HANDOFF_RETURN_READOUT_PATH)
    return_classification = read_json(SOURCE_HANDOFF_RETURN_CLASSIFICATION_PATH)
    return_rollup = read_json(SOURCE_HANDOFF_RETURN_ROLLUP_PATH)
    return {
        "schema_version": "cell1_reference_stack_readout_after_return_loop_v0",
        "schema_consumption_reference": {
            "reference_id": schema_reference.get("reference_id"),
            "reference_status": schema_reference.get("reference_status"),
            "source_receipt_id": SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID,
            "proves": [
                "C4 to Cell1 schema intake can consume an accepted proposal packet.",
                "A bounded schema-consumption execution can complete without runtime patch or target modification.",
            ],
        },
        "handoff_return_reference": {
            "reference_id": return_reference.get("reference_id"),
            "reference_status": return_reference.get("reference_status"),
            "source_receipt_id": SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID,
            "proves": return_reference.get("reference_meaning", []),
        },
        "return_loop_observed": {
            "classification": return_classification.get("classification"),
            "accepted_for_review": return_classification.get("accepted_for_review"),
            "accepted_for_build": return_classification.get("accepted_for_build"),
            "return_packet_emitted_count": return_rollup.get("return_packet_emitted_count", 0),
            "return_packet_validated": return_readout.get("return_packet_validated"),
        },
        "stack_now_proves": [
            "C4 to Cell1 schema intake works under one bounded accepted proposal path.",
            "Cell1 can return a typed result packet to review/Cell0 classification surface.",
            "The returned packet can be accepted for review without becoming accepted for build.",
            "The reference stack remained boundary-clean across intake and return edges.",
        ],
        "stack_does_not_prove": [
            "runtime patch safety",
            "target file modification safety",
            "C5 authorization",
            "general Cell1 authority",
            "multi-family proposal transfer",
            "the next objective has executed",
        ],
    }

def objective_candidates() -> List[Dict[str, Any]]:
    reasons = {
        "CELL1_OBJECTIVE_ACCEPTED_PROPOSAL_VARIANT_TEST": "Useful breadth test across another proposal family, but the reference stack now makes a narrower runtime-patch precheck more informative before any actual patch.",
        "CELL1_OBJECTIVE_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK": "Selected. Intake and return-loop references are now closed; the next smallest build-adjacent move is to check whether a minimal runtime patch test is eligible, without applying any patch.",
        "CELL1_OBJECTIVE_HANDOFF_RETURN_LOOP_VARIANT_TEST": "Valid later for return-loop breadth, but the first return edge already passed and closed.",
        "CELL1_OBJECTIVE_C5_PREFLIGHT_READINESS_CHECK": "Still premature. C5 should not be discussed until minimal runtime patch preconditions are inspected or explicitly blocked.",
        "CELL1_OBJECTIVE_CLOSE_CELL1_TRACK_FOR_NOW": "Valid stop option, but the current reference stack exposes a clear next bounded precheck.",
        "CELL1_OBJECTIVE_REPAIR_REFERENCE_STACK": "Not selected because both references are frozen and boundary-clean.",
        "CELL1_OBJECTIVE_REQUEST_NARROWER_EVIDENCE": "Not selected because the current receipt surface is sufficient for a precheck decision.",
        "QUESTION_PACKET_NOT_COMMAND": "Not selected because the decision surface is typed and the closed enum is available.",
    }
    scores = {
        "CELL1_OBJECTIVE_ACCEPTED_PROPOSAL_VARIANT_TEST": 80,
        "CELL1_OBJECTIVE_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK": 95,
        "CELL1_OBJECTIVE_HANDOFF_RETURN_LOOP_VARIANT_TEST": 60,
        "CELL1_OBJECTIVE_C5_PREFLIGHT_READINESS_CHECK": 35,
        "CELL1_OBJECTIVE_CLOSE_CELL1_TRACK_FOR_NOW": 50,
        "CELL1_OBJECTIVE_REPAIR_REFERENCE_STACK": 10,
        "CELL1_OBJECTIVE_REQUEST_NARROWER_EVIDENCE": 15,
        "QUESTION_PACKET_NOT_COMMAND": 5,
    }
    rows: List[Dict[str, Any]] = []
    for cls in CLOSED_DECISION_CLASSES:
        rows.append({
            "schema_version": "cell1_next_objective_after_return_loop_candidate_record_v0",
            "candidate_id": "candidate_after_return_" + sha8({"class": cls, "source": SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID}),
            "decision_class": cls,
            "score": scores[cls],
            "selected": cls == SELECTED_DECISION_CLASS,
            "selection_reason": reasons[cls],
            "authority_boundary": {
                "may_execute_now": False,
                "may_apply_runtime_patch": False,
                "may_modify_target_files": False,
                "may_open_c5": False,
                "may_grant_general_cell1_authority": False,
            },
        })
    return rows

def authority_boundary() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_next_objective_after_return_loop_authority_boundary_v0",
        "authority_boundary_id": "cell1_after_return_authority_" + sha8({"selected": SELECTED_DECISION_CLASS}),
        "selected_decision_class": SELECTED_DECISION_CLASS,
        "may_emit_next_objective_candidate": True,
        "may_emit_future_design_target": True,
        "may_emit_executable_command": False,
        "may_execute_selected_objective": False,
        "may_apply_runtime_patch": False,
        "may_modify_target_files": False,
        "may_open_c5": False,
        "may_grant_general_cell1_authority": False,
        "may_mutate_taxonomy": False,
        "may_promote_proposal_status": False,
        "may_fabricate_accepted_proposal": False,
        "must_not_infer": [
            "runtime patch is authorized",
            "target file modification is authorized",
            "C5 is authorized",
            "Cell1 is a general builder",
            "accepted-for-review equals accepted-for-build",
            "precheck equals execution",
        ],
    }

def decision_record(boundary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_next_objective_after_return_loop_decision_v0",
        "decision_id": "cell1_after_return_next_obj_" + sha8({"source": SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID, "selected": SELECTED_DECISION_CLASS}),
        "source_handoff_return_reference_packet_ref": rel(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH),
        "source_schema_reference_packet_ref": rel(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH),
        "selected_decision_class": SELECTED_DECISION_CLASS,
        "why_selected": "The stack now has two closed references: C4-to-Cell1 schema intake and Cell1-to-review/Cell0 return semantics. The next smallest build-adjacent objective is not a runtime patch; it is a precheck that asks whether a minimal runtime patch test has the required accepted proposal, bounded target, verification gate, and rollback/stop boundary.",
        "why_not_runtime_patch_execution": "No runtime patch may execute from this decision. The selected class is a precheck only; it inspects eligibility and can block or request narrower evidence.",
        "why_not_c5_yet": "C5 remains blocked because no runtime patch precheck or runtime-backed Cell1 build evidence has been accepted. The return-loop reference only proves return semantics.",
        "why_not_general_cell1_authority": "The reference stack proves two local Cell1 edges, not general builder authority. Authority remains bounded to explicitly selected units.",
        "required_inputs_for_next_unit": [
            rel(OBJECTIVE_DECISION_PATH),
            rel(AUTHORITY_BOUNDARY_PATH),
            rel(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH),
            rel(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH),
            rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
            rel(SOURCE_C1_PATCH_SCHEMA_PATH),
            rel(SOURCE_C2_LANE_REGISTRY_PATH),
        ],
        "forbidden_inputs_for_next_unit": [
            "ambient workspace inference",
            "latest-file guessing",
            "mtime selection",
            "unreviewed proposal packet",
            "PROPOSED_ONLY packet treated as accepted",
            "runtime target writes during precheck",
            "C5 planning treated as authorization",
            "general Cell1 builder authority",
        ],
        "authority_boundary": {
            "may_emit_next_objective_candidate": boundary["may_emit_next_objective_candidate"],
            "may_emit_future_design_target": boundary["may_emit_future_design_target"],
            "may_emit_executable_command": boundary["may_emit_executable_command"],
            "may_execute_selected_objective": boundary["may_execute_selected_objective"],
            "may_apply_runtime_patch": boundary["may_apply_runtime_patch"],
            "may_modify_target_files": boundary["may_modify_target_files"],
            "may_open_c5": boundary["may_open_c5"],
            "may_grant_general_cell1_authority": boundary["may_grant_general_cell1_authority"],
        },
        "must_not_infer": boundary["must_not_infer"],
        "recommended_next": RECOMMENDED_NEXT,
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CELL1_NEXT_BOUNDED_OBJECTIVE_AFTER_RETURN_LOOP_DECIDED",
            "next_command_goal": None,
        },
    }

def rollup(candidates: List[Dict[str, Any]], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_next_objective_after_return_loop_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_handoff_return_close_receipt_id": SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID,
        "source_schema_close_receipt_id": SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID,
        "source_handoff_return_test_receipt_id": SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID,
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
        "recommended_next": decision["recommended_next"],
    }

def profile(rollup_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_next_objective_after_return_loop_profile_v0",
        "profile_id": "cell1_after_return_next_obj_" + sha8({"source": SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID}),
        "status": "CELL1_NEXT_OBJECTIVE_AFTER_RETURN_LOOP_DECIDED",
        "selected_decision_class": rollup_obj["selected_decision_class"],
        "recommended_next": rollup_obj["recommended_next"],
        "objective_executed": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "next_command_goal": None,
    }

def report(rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_next_objective_after_return_loop_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "reference_stack_readout_emitted_count": 1,
        "objective_candidates_emitted_count": rollup_obj["candidate_count"],
        "decision_record_emitted_count": 1,
        "authority_boundary_emitted_count": 1,
        "profile_status": profile_obj["status"],
        "selected_decision_class": rollup_obj["selected_decision_class"],
        "recommended_next_handling": rollup_obj["recommended_next"],
        "objective_executed_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
    }

def transition_trace(decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_next_objective_after_return_loop_transition_trace_v0",
        "trace": [
            {
                "step": "consume_reference_stack",
                "question": "are schema intake and return-loop references both frozen",
                "answer": "yes",
                "taken": "enumerate_next_objective_classes",
            },
            {
                "step": "enumerate_next_objective_classes",
                "question": "what is the smallest build-adjacent but non-executing objective",
                "answer": SELECTED_DECISION_CLASS,
                "taken": "emit_authority_boundary",
            },
            {
                "step": "emit_authority_boundary",
                "question": "does the decision avoid runtime patch/C5/general authority",
                "answer": "yes",
                "taken": "stop",
            },
        ],
        "terminal": decision["terminal"],
    }

def validate_outputs(readout: Dict[str, Any], candidates: List[Dict[str, Any]], boundary: Dict[str, Any], decision: Dict[str, Any], rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any], report_obj: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if readout.get("schema_consumption_reference", {}).get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("schema_reference_not_frozen")
    if readout.get("handoff_return_reference", {}).get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("handoff_return_reference_not_frozen")
    if readout.get("return_loop_observed", {}).get("accepted_for_review") is not True:
        failures.append("return_loop_not_accepted_for_review")
    if readout.get("return_loop_observed", {}).get("accepted_for_build") is not False:
        failures.append("return_loop_accepts_for_build")
    if len(candidates) != len(CLOSED_DECISION_CLASSES):
        failures.append("candidate_count_wrong")
    if decision.get("selected_decision_class") not in CLOSED_DECISION_CLASSES:
        failures.append("selected_class_not_closed_enum")
    if decision.get("selected_decision_class") != SELECTED_DECISION_CLASS:
        failures.append("selected_class_wrong")
    if not decision.get("why_not_runtime_patch_execution"):
        failures.append("why_not_runtime_patch_execution_missing")
    if not decision.get("why_not_c5_yet"):
        failures.append("why_not_c5_missing")
    if not decision.get("why_not_general_cell1_authority"):
        failures.append("why_not_general_authority_missing")
    if decision.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("decision_hidden_next_command")
    if boundary.get("may_emit_executable_command") is not False:
        failures.append("authority_allows_executable_command")
    if boundary.get("may_execute_selected_objective") is not False:
        failures.append("authority_allows_selected_objective_execution")
    if boundary.get("may_apply_runtime_patch") is not False:
        failures.append("authority_allows_runtime_patch")
    if boundary.get("may_modify_target_files") is not False:
        failures.append("authority_allows_target_file_modification")
    if boundary.get("may_open_c5") is not False:
        failures.append("authority_allows_c5")
    if boundary.get("may_grant_general_cell1_authority") is not False:
        failures.append("authority_allows_general_cell1")
    for key in ZERO_COUNTER_KEYS:
        if rollup_obj.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup_obj.get(key)}")
    if rollup_obj.get("candidate_count") != len(CLOSED_DECISION_CLASSES):
        failures.append("rollup_candidate_count_wrong")
    if rollup_obj.get("selected_decision_class") != SELECTED_DECISION_CLASS:
        failures.append("rollup_selected_class_wrong")
    if profile_obj.get("objective_executed") is not False:
        failures.append("profile_claims_objective_executed")
    if profile_obj.get("runtime_patch_applied") is not False:
        failures.append("profile_claims_runtime_patch")
    if profile_obj.get("target_file_modified") is not False:
        failures.append("profile_claims_target_file_modified")
    if profile_obj.get("c5_opened") is not False:
        failures.append("profile_claims_c5")
    if profile_obj.get("general_cell1_authority_granted") is not False:
        failures.append("profile_claims_general_cell1")
    if profile_obj.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")
    for key in [
        "objective_executed_count",
        "runtime_patch_applied_count",
        "target_file_modified_count",
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
    if terminal.get("stop_code") != "STOP_CELL1_NEXT_BOUNDED_OBJECTIVE_AFTER_RETURN_LOOP_DECIDED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    readout = read_json(REFERENCE_STACK_READOUT_PATH)
    candidates = [json.loads(line) for line in OBJECTIVE_CANDIDATES_PATH.read_text().splitlines() if line.strip()]
    boundary = read_json(AUTHORITY_BOUNDARY_PATH)
    decision = read_json(OBJECTIVE_DECISION_PATH)
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

    bad_readout = copy.deepcopy(readout)
    bad_readout["handoff_return_reference"]["reference_status"] = "NOT_FROZEN"
    add("handoff_return_reference_not_frozen_fail", validate_outputs(bad_readout, candidates, boundary, decision, rollup_obj, profile_obj, report_obj), "handoff_return_reference_not_frozen")

    bad_readout = copy.deepcopy(readout)
    bad_readout["return_loop_observed"]["accepted_for_build"] = True
    add("return_loop_accepts_for_build_fail", validate_outputs(bad_readout, candidates, boundary, decision, rollup_obj, profile_obj, report_obj), "return_loop_accepts_for_build")

    bad_candidates = candidates[:-1]
    add("candidate_count_wrong_fail", validate_outputs(readout, bad_candidates, boundary, decision, rollup_obj, profile_obj, report_obj), "candidate_count_wrong")

    bad_decision = copy.deepcopy(decision)
    bad_decision["selected_decision_class"] = "CELL1_OBJECTIVE_C5_PREFLIGHT_READINESS_CHECK"
    add("selected_class_wrong_fail", validate_outputs(readout, candidates, boundary, bad_decision, rollup_obj, profile_obj, report_obj), "selected_class_wrong")

    bad_decision = copy.deepcopy(decision)
    bad_decision["why_not_runtime_patch_execution"] = ""
    add("why_not_runtime_patch_execution_missing_fail", validate_outputs(readout, candidates, boundary, bad_decision, rollup_obj, profile_obj, report_obj), "why_not_runtime_patch_execution_missing")

    bad_decision = copy.deepcopy(decision)
    bad_decision["terminal"]["next_command_goal"] = "RUN_RUNTIME_PATCH"
    add("decision_hidden_next_command_fail", validate_outputs(readout, candidates, boundary, bad_decision, rollup_obj, profile_obj, report_obj), "decision_hidden_next_command")

    for case, field, expected in [
        ("authority_allows_executable_command_fail", "may_emit_executable_command", "authority_allows_executable_command"),
        ("authority_allows_selected_objective_execution_fail", "may_execute_selected_objective", "authority_allows_selected_objective_execution"),
        ("authority_allows_runtime_patch_fail", "may_apply_runtime_patch", "authority_allows_runtime_patch"),
        ("authority_allows_target_file_modification_fail", "may_modify_target_files", "authority_allows_target_file_modification"),
        ("authority_allows_c5_fail", "may_open_c5", "authority_allows_c5"),
        ("authority_allows_general_cell1_fail", "may_grant_general_cell1_authority", "authority_allows_general_cell1"),
    ]:
        bad_boundary = copy.deepcopy(boundary)
        bad_boundary[field] = True
        add(case, validate_outputs(readout, candidates, bad_boundary, decision, rollup_obj, profile_obj, report_obj), expected)

    for case, counter in [
        ("objective_executed_fail", "objective_executed_count"),
        ("runtime_patch_applied_fail", "runtime_patch_applied_count"),
        ("target_file_modified_fail", "target_file_modified_count"),
        ("c5_opened_fail", "c5_opened_count"),
        ("general_cell1_authority_granted_fail", "general_cell1_authority_granted_count"),
        ("taxonomy_registry_mutated_fail", "taxonomy_registry_mutation_count"),
        ("proposal_status_promoted_fail", "proposal_status_promoted_count"),
        ("accepted_proposal_fabricated_fail", "accepted_proposal_fabricated_count"),
        ("source_mutation_fail", "source_mutation_count"),
        ("prior_receipt_mutation_fail", "prior_receipt_mutation_count"),
        ("hidden_next_command_fail", "hidden_next_command_count"),
        ("unbounded_payload_inspection_fail", "unbounded_payload_inspection_count"),
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
        terminal = {"type": "STOP", "stop_code": "STOP_CELL1_NEXT_OBJECTIVE_AFTER_RETURN_LOOP_EVIDENCE_REQUEST_REQUIRED", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "cell1_next_objective_after_return_loop_receipt_v0",
            "receipt_type": "CELL1_NEXT_OBJECTIVE_AFTER_RETURN_LOOP_RECEIPT",
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
        print(f"cell1_after_return_next_objective_receipt_id={receipt_id}")
        print(f"cell1_after_return_next_objective_receipt_path=data/cell1_next_bounded_objective_after_return_loop_v0_receipts/{receipt_id}.json")
        return 1

    readout = reference_stack_readout()
    candidates = objective_candidates()
    boundary = authority_boundary()
    decision = decision_record(boundary)
    rollup_obj = rollup(candidates, decision)
    profile_obj = profile(rollup_obj)
    report_obj = report(rollup_obj, profile_obj)
    trace = transition_trace(decision)

    write_json(SOURCE_SURFACE_PATH, source_surface())
    write_json(REFERENCE_STACK_READOUT_PATH, readout)
    write_jsonl(OBJECTIVE_CANDIDATES_PATH, candidates)
    write_json(OBJECTIVE_DECISION_PATH, decision)
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
        "AFTER_RETURN_OBJ_0_HANDOFF_RETURN_CLOSE_RECEIPT_CONSUMED": SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH.exists(),
        "AFTER_RETURN_OBJ_1_HANDOFF_RETURN_REFERENCE_CONSUMED": SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH.exists(),
        "AFTER_RETURN_OBJ_2_SCHEMA_REFERENCE_CONSUMED": SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH.exists(),
        "AFTER_RETURN_OBJ_3_REFERENCE_STACK_READOUT_EMITTED": REFERENCE_STACK_READOUT_PATH.exists(),
        "AFTER_RETURN_OBJ_4_OBJECTIVE_CANDIDATES_EMITTED": OBJECTIVE_CANDIDATES_PATH.exists() and len(candidates) == len(CLOSED_DECISION_CLASSES),
        "AFTER_RETURN_OBJ_5_SELECTED_CLASS_FROM_CLOSED_ENUM": decision["selected_decision_class"] in CLOSED_DECISION_CLASSES,
        "AFTER_RETURN_OBJ_6_SELECTED_RUNTIME_PATCH_PRECHECK": decision["selected_decision_class"] == SELECTED_DECISION_CLASS,
        "AFTER_RETURN_OBJ_7_DECISION_RECORD_EMITTED": OBJECTIVE_DECISION_PATH.exists(),
        "AFTER_RETURN_OBJ_8_AUTHORITY_BOUNDARY_EMITTED": AUTHORITY_BOUNDARY_PATH.exists(),
        "AFTER_RETURN_OBJ_9_NO_OBJECTIVE_EXECUTION": rollup_obj["objective_executed_count"] == 0,
        "AFTER_RETURN_OBJ_10_NO_RUNTIME_PATCH": rollup_obj["runtime_patch_applied_count"] == 0,
        "AFTER_RETURN_OBJ_11_NO_TARGET_FILE_MODIFICATION": rollup_obj["target_file_modified_count"] == 0,
        "AFTER_RETURN_OBJ_12_NO_C5_OPENED": rollup_obj["c5_opened_count"] == 0,
        "AFTER_RETURN_OBJ_13_NO_GENERAL_CELL1_AUTHORITY": rollup_obj["general_cell1_authority_granted_count"] == 0,
        "AFTER_RETURN_OBJ_14_NO_PROPOSAL_PROMOTION": rollup_obj["proposal_status_promoted_count"] == 0,
        "AFTER_RETURN_OBJ_15_NO_ACCEPTED_PROPOSAL_FABRICATION": rollup_obj["accepted_proposal_fabricated_count"] == 0,
        "AFTER_RETURN_OBJ_16_NO_HIDDEN_NEXT_COMMAND": rollup_obj["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
        "AFTER_RETURN_OBJ_17_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    for gate_name, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate_name}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_handoff_return_close": SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID,
        "selected": SELECTED_DECISION_CLASS,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "reference_stack_readout": rel(REFERENCE_STACK_READOUT_PATH),
        "objective_candidate_records": rel(OBJECTIVE_CANDIDATES_PATH),
        "objective_decision_record": rel(OBJECTIVE_DECISION_PATH),
        "objective_authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
        "rollup": rel(ROLLUP_PATH),
        "profile": rel(PROFILE_PATH),
        "report": rel(REPORT_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_handoff_return_close_receipt": rel(SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH),
        "source_handoff_return_reference_packet": rel(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH),
        "source_schema_reference_packet": rel(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH),
        "source_accepted_proposal_packet": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "source_c1_patch_schema": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "source_c2_lane_registry": rel(SOURCE_C2_LANE_REGISTRY_PATH),
    }

    guards = {
        "build_mode_next_objective_after_return_loop_decision_only": BUILD_MODE == "NEXT_OBJECTIVE_AFTER_RETURN_LOOP_DECISION_ONLY",
        "selected_runtime_patch_precheck": decision["selected_decision_class"] == SELECTED_DECISION_CLASS,
        "recommended_next": RECOMMENDED_NEXT,
        "objective_executed": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "proposal_status_promoted": False,
        "accepted_proposal_fabricated": False,
        "hidden_next_command": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
    }

    receipt = {
        "schema_version": "cell1_next_objective_after_return_loop_receipt_v0",
        "receipt_type": "CELL1_NEXT_OBJECTIVE_AFTER_RETURN_LOOP_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "next bounded Cell1 objective after closed schema-intake and return-loop references",
        "source_handoff_return_close_receipt_id": SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID,
        "source_handoff_return_test_receipt_id": SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID,
        "source_schema_close_receipt_id": SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID,
        "source_cell1_schema_test_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "source_c4_consumption_receipt_id": SOURCE_C4_CONSUMPTION_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "after_return_next_objective_summary": {
            "profile_status": profile_obj["status"],
            "candidate_count": rollup_obj["candidate_count"],
            "selected_decision_class": rollup_obj["selected_decision_class"],
            "recommended_next": rollup_obj["recommended_next"],
            "why_selected": decision["why_selected"],
            "why_not_runtime_patch_execution": decision["why_not_runtime_patch_execution"],
            "why_not_c5_yet": decision["why_not_c5_yet"],
            "why_not_general_cell1_authority": decision["why_not_general_cell1_authority"],
            "objective_executed": False,
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "general_cell1_authority_granted": False,
            "bad_counters_zero": profile_obj["bad_counters_zero"],
        },
        "aggregate_metrics": {
            **{k: v for k, v in report_obj.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
            "rollup": rollup_obj,
            "source_mutation_count": 1 if source_mutation_detected else report_obj["source_mutation_count"],
        },
        "acceptance_gate_results": acceptance_gate_results,
        "after_return_next_objective_guards": guards,
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
    print(f"cell1_after_return_next_objective_receipt_id={receipt_id}")
    print(f"cell1_after_return_next_objective_receipt_path=data/cell1_next_bounded_objective_after_return_loop_v0_receipts/{receipt_id}.json")
    print(f"cell1_after_return_next_objective_decision_path=data/cell1_next_bounded_objective_after_return_loop_v0/objective_decision_record_v0.json")
    print(f"cell1_after_return_next_objective_rollup_path=data/cell1_next_bounded_objective_after_return_loop_v0/objective_rollup_v0.json")
    print(f"cell1_after_return_next_objective_profile_path=data/cell1_next_bounded_objective_after_return_loop_v0/objective_profile_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
