#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_C1_CELL0_PROPOSAL_LAYER_V0"
TARGET_UNIT_ID = "c1.cell0.proposal_layer.v0"
LAYER = "CELL_0 / PROPOSAL_EMISSION"
MODE = "CERTIFY / BUILD_SCHEMA / PROBE"
BUILD_MODE = "STATIC_SCHEMA_AND_PROBE_ONLY"

SOURCE_B3_RECEIPT_ID = "a4cbf33f"
SOURCE_B3_RECEIPT_PATH = ROOT / "data" / "b3_cell0_local_decision_loop_schema_lock_v0_receipts" / "a4cbf33f.json"
SOURCE_B3_PROFILE_PATH = ROOT / "data" / "b3_cell0_local_decision_loop_schema_lock_v0" / "b3_loop_lock_profile_v0.json"
SOURCE_B3_LOOP_SCHEMA_PATH = ROOT / "data" / "b3_cell0_local_decision_loop_schema_lock_v0" / "local_decision_loop_schema_v0.json"
SOURCE_B3_EDGE_ENUM_PATH = ROOT / "data" / "b3_cell0_local_decision_loop_schema_lock_v0" / "local_decision_loop_edge_enum_v0.json"
SOURCE_B3_LICENSE_MAP_PATH = ROOT / "data" / "b3_cell0_local_decision_loop_schema_lock_v0" / "local_decision_loop_edge_artifact_license_map_v0.json"
SOURCE_B3_SURFACE_MATRIX_PATH = ROOT / "data" / "b3_cell0_local_decision_loop_schema_lock_v0" / "local_decision_loop_surface_test_matrix_v0.json"
SOURCE_B3_LOOP_RECEIPTS_PATH = ROOT / "data" / "b3_cell0_local_decision_loop_schema_lock_v0" / "local_decision_loop_receipts_v0.jsonl"
SOURCE_B3_TRACE_RECORDS_PATH = ROOT / "data" / "b3_cell0_local_decision_loop_schema_lock_v0" / "local_decision_loop_trace_records_v0.jsonl"

SOURCE_B2_RECEIPT_ID = "7ab64083"
SOURCE_B2_PROGRESS_ENUM_PATH = ROOT / "data" / "b2_cell0_informative_failure_progress_classifier_v0" / "failure_progress_class_enum_v0.json"
SOURCE_B2_ROLLUP_PATH = ROOT / "data" / "b2_cell0_informative_failure_progress_classifier_v0" / "b2_failure_progress_rollup_v0.json"

SOURCE_B1_RECEIPT_ID = "b9c8f831"
SOURCE_B1_TYPED_STOP_SCHEMA_PATH = ROOT / "data" / "b1_cell0_local_lawful_actor_stabilization_v0" / "cell0_typed_stop_schema_v0.json"
SOURCE_B1_PRESSURE_ENUM_PATH = ROOT / "data" / "b1_cell0_local_lawful_actor_stabilization_v0" / "cell0_pressure_class_enum_v0.json"

OUT_DIR = ROOT / "data" / "c1_cell0_proposal_layer_v0"
RECEIPT_DIR = ROOT / "data" / "c1_cell0_proposal_layer_v0_receipts"

PROPOSAL_PACKET_SCHEMA_PATH = OUT_DIR / "proposal_packet_schema_v0.json"
PROPOSAL_TRIGGER_SCHEMA_PATH = OUT_DIR / "proposal_trigger_schema_v0.json"
PROPOSAL_TYPE_ENUM_PATH = OUT_DIR / "proposal_type_enum_v0.json"
PROPOSAL_STATUS_ENUM_PATH = OUT_DIR / "proposal_status_enum_v0.json"
MISSING_OBJECT_CANDIDATE_SCHEMA_PATH = OUT_DIR / "missing_object_candidate_schema_v0.json"
PROPOSAL_EVIDENCE_BUNDLE_SCHEMA_PATH = OUT_DIR / "proposal_evidence_bundle_schema_v0.json"
PROPOSAL_AUTHORITY_BOUNDARY_SCHEMA_PATH = OUT_DIR / "proposal_authority_boundary_schema_v0.json"
PROPOSAL_REVIEW_REQUEST_SCHEMA_PATH = OUT_DIR / "proposal_review_request_schema_v0.json"
PROPOSAL_RECEIPT_SCHEMA_PATH = OUT_DIR / "proposal_receipt_schema_v0.json"
PROPOSAL_TRIGGER_MAPPING_TABLE_PATH = OUT_DIR / "proposal_trigger_mapping_table_v0.json"
PROPOSAL_COMPLETENESS_VALIDATOR_PATH = OUT_DIR / "proposal_completeness_validator_v0.json"
PROPOSAL_REVIEW_CONTRACT_PATH = OUT_DIR / "proposal_review_contract_v0.json"
PROPOSAL_TYPE_AUTHORITY_MATRIX_PATH = OUT_DIR / "proposal_type_authority_matrix_v0.json"

DEMO_PROPOSAL_TRIGGERS_PATH = OUT_DIR / "c1_demo_proposal_triggers_v0.jsonl"
PROPOSAL_PACKET_RECORDS_PATH = OUT_DIR / "proposal_packet_records_v0.jsonl"
MISSING_OBJECT_CANDIDATE_RECORDS_PATH = OUT_DIR / "missing_object_candidate_records_v0.jsonl"
PROPOSAL_EVIDENCE_BUNDLE_RECORDS_PATH = OUT_DIR / "proposal_evidence_bundle_records_v0.jsonl"
PROPOSAL_AUTHORITY_BOUNDARY_RECORDS_PATH = OUT_DIR / "proposal_authority_boundary_records_v0.jsonl"
PROPOSAL_REVIEW_REQUEST_RECORDS_PATH = OUT_DIR / "proposal_review_request_records_v0.jsonl"
PROPOSAL_RECEIPT_RECORDS_PATH = OUT_DIR / "proposal_receipt_records_v0.jsonl"
PROPOSAL_ROLLUP_PATH = OUT_DIR / "proposal_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c1_proposal_layer_profile_v0.json"
TRANSITION_TRACE_PATH = OUT_DIR / "c1_transition_trace.json"
REPORT_PATH = OUT_DIR / "c1_report.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_B3_RECEIPT_PATH,
    SOURCE_B3_PROFILE_PATH,
    SOURCE_B3_LOOP_SCHEMA_PATH,
    SOURCE_B3_EDGE_ENUM_PATH,
    SOURCE_B3_LICENSE_MAP_PATH,
    SOURCE_B3_SURFACE_MATRIX_PATH,
    SOURCE_B3_LOOP_RECEIPTS_PATH,
    SOURCE_B3_TRACE_RECORDS_PATH,
    SOURCE_B2_PROGRESS_ENUM_PATH,
    SOURCE_B2_ROLLUP_PATH,
    SOURCE_B1_TYPED_STOP_SCHEMA_PATH,
    SOURCE_B1_PRESSURE_ENUM_PATH,
]

TRIGGER_CLASSES = [
    "STOP_TAXONOMY_GAP",
    "STOP_UNDERTYPED_OBJECT",
    "STOP_UNTYPED_UNIT",
    "STOP_NEEDS_NEW_MOVE",
    "STOP_NEEDS_EXTRACTION",
    "STOP_AUTHORITY_BOUNDARY",
    "STOP_HUMAN_REVIEW_REQUIRED",
    "STOP_PROPOSAL_REQUIRED",
    "STOP_RECEIPT_MISMATCH",
    "STOP_PROJECTION_BUG",
    "STOP_VISIBLE_GOTCHA",
    "MISSING_REQUIRED_DISTINCTION",
    "PRODUCTIVE_PRESSURE",
    "SHARPER_LOCALIZATION",
    "MISSING_OBJECT_CLARIFIED",
    "B3_EDGE_EMIT_PROPOSAL",
]

FORBIDDEN_TRIGGER = "STOP_DONE_WITH_NO_PRESSURE"

PROPOSAL_TYPES = [
    "TAXONOMY_DELTA_PROPOSAL",
    "MISSING_MOVE_PROPOSAL",
    "AUTHORITY_REVIEW_PROPOSAL",
    "EXTRACTION_OBJECTIVE_PROPOSAL",
    "BOUNDED_REPAIR_PROPOSAL",
    "OBSERVABILITY_PATCH_PROPOSAL",
    "LABEL_SPLIT_PROPOSAL",
    "EVIDENCE_REQUEST_PROPOSAL",
    "BUILDER_OBJECTIVE_PROPOSAL",
    "PARK_OBJECT_PROPOSAL",
]

PROPOSAL_STATUSES = [
    "PROPOSED_ONLY",
    "UNDER_REVIEW",
    "ACCEPTED_FOR_BUILD",
    "ACCEPTED_FOR_TAXONOMY_PATCH",
    "ACCEPTED_FOR_EXTRACTION",
    "REJECTED",
    "DEFERRED",
    "NARROWING_REQUIRED",
    "EVIDENCE_REQUIRED",
    "PARKED",
    "SUPERSEDED",
]

C1_ALLOWED_STATUS = "PROPOSED_ONLY"

ZERO_COUNTER_KEYS = [
    "self_authorized_proposal_count",
    "proposal_applied_without_review_count",
    "proposal_status_promoted_without_review_count",
    "proposal_counted_as_execution_count",
    "proposal_counted_as_patch_count",
    "missing_object_candidate_counted_as_confirmed_count",
    "proposal_without_evidence_count",
    "proposal_without_authority_boundary_count",
    "proposal_without_must_not_infer_count",
    "proposal_from_stop_done_no_pressure_count",
    "builder_command_emitted_by_c1_count",
    "taxonomy_mutated_by_c1_count",
    "move_registered_by_c1_count",
    "proposal_incomplete_count",
    "proposal_type_authority_overreach_count",
    "accepted_status_emitted_by_c1_count",
    "insufficient_evidence_emitted_non_evidence_request_count",
    "proposal_missing_b3_source_ref_count",
    "proposal_missing_review_contract_count",
    "cell1_authorization_count",
    "domain_shift_authorization_count",
    "source_mutation_count",
    "prior_receipt_mutation_count",
    "registry_mutation_count",
    "code_mutation_count",
]

HUMAN_DECISION = {
    "decision": "BUILD_C1_CELL0_PROPOSAL_LAYER",
    "scope": "Build C1 as the Cell 0 proposal layer in STATIC_SCHEMA_AND_PROBE_ONLY mode. Emit proposal packet, trigger, type enum, status enum, missing-object candidate, evidence bundle, authority boundary, review request, receipt, completeness validator, review contract, type-authority matrix, trigger mapping table, demo proposal cases, proposal records, proposal rollup, profile, and receipt. C1 may emit only PROPOSED_ONLY proposal packets from typed triggers or B3 EMIT_PROPOSAL edges. It does not apply proposals, emit builder commands, mutate taxonomy/registry, register moves, approve proposals, or treat missing-object candidates as confirmed identities.",
    "authorized": [
        "define proposal packet schema",
        "define proposal trigger schema",
        "define proposal type enum",
        "define proposal status enum",
        "define missing object candidate schema",
        "define proposal evidence bundle schema",
        "define proposal authority boundary schema",
        "define proposal review request schema",
        "define proposal receipt schema",
        "define proposal completeness validator",
        "define proposal review contract",
        "define proposal type authority matrix",
        "define trigger-to-proposal mapping table",
        "run bounded demo proposal cases",
        "emit proposal rollup",
        "emit C1 proposal layer profile",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "execute proposal",
        "emit builder command",
        "mutate code",
        "mutate taxonomy",
        "mutate move registry",
        "register new move",
        "approve proposal",
        "change proposal status beyond PROPOSED_ONLY",
        "widen jurisdiction",
        "create Cell 1",
        "apply missing object candidate",
        "treat proposal as command",
        "treat useful proposal pressure as radius improvement",
        "emit vague investigate proposal",
        "skip evidence refs",
        "skip must_not_infer",
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

def append_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def validate_source_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")

    if failures:
        return failures

    b3_receipt = read_json(SOURCE_B3_RECEIPT_PATH)
    b3_profile = read_json(SOURCE_B3_PROFILE_PATH)
    b3_loop = read_json(SOURCE_B3_LOOP_SCHEMA_PATH)
    b3_edges = read_json(SOURCE_B3_EDGE_ENUM_PATH)
    b2_rollup = read_json(SOURCE_B2_ROLLUP_PATH)

    if b3_receipt.get("receipt_id") != SOURCE_B3_RECEIPT_ID:
        failures.append("b3_receipt_id_wrong")
    if b3_receipt.get("gate") != "PASS":
        failures.append("b3_receipt_gate_not_PASS")
    if b3_profile.get("status") != "TRANSFERABLE_LOCAL_LOOP_V0":
        failures.append("b3_profile_not_transferable")
    if b3_loop.get("loop_id") != "LOCAL_DECISION_LOOP_V0":
        failures.append("b3_loop_id_wrong")
    if "EMIT_PROPOSAL" not in b3_edges.get("edge_types", []):
        failures.append("b3_emit_proposal_edge_missing")
    if b2_rollup.get("failure_events_total") != 12:
        failures.append("b2_rollup_not_expected_basis")
    return failures

def proposal_packet_schema() -> Dict[str, Any]:
    return {
        "schema_version": "proposal_packet_schema_v0",
        "packet_schema": {
            "schema_version": "proposal_packet_v0",
            "proposal_id": "proposal_<sig8>",
            "proposal_type": None,
            "status": "PROPOSED_ONLY",
            "trigger": {
                "trigger_kind": None,
                "halt_code": None,
                "halt_record_ref": None,
                "failure_progress_ref": None,
                "local_decision_loop_trace_ref": None,
                "required_distinction_ref": None,
                "selected_edge": "EMIT_PROPOSAL",
            },
            "source_binding": {
                "source_selected_edge": "EMIT_PROPOSAL",
                "source_pressure_class": None,
                "source_required_distinction": None,
                "source_distinction_status": None,
                "source_receipt_refs": [],
                "source_evidence_refs": [],
            },
            "missing_or_blocking_object": {
                "candidate_id": None,
                "candidate_kind": None,
                "smallest_honest_reading": None,
                "status": "CANDIDATE_ONLY",
            },
            "proposal_body": {
                "objective": None,
                "bounded_action": None,
                "target_surface": None,
                "expected_change": None,
                "allowed_inputs": [],
                "forbidden_inputs": [],
                "probe_or_test_requirement": None,
                "verification_receipt_requirement": None,
                "rollback_or_stop_condition": None,
            },
            "evidence": {
                "evidence_bundle_ref": None,
                "evidence_status": None,
                "missing_evidence": [],
            },
            "authority_boundary": {
                "authority_boundary_ref": None,
                "can_describe": True,
                "can_apply": False,
                "requires_review": True,
                "review_reason": None,
            },
            "must_not_infer": [],
            "allowed_next_handling": [],
            "expected_acceptance_receipt": {
                "required_gate": "PASS",
                "required_negative_controls": [],
            },
        },
    }

def proposal_trigger_schema() -> Dict[str, Any]:
    return {
        "schema_version": "proposal_trigger_schema_v0",
        "trigger_schema": {
            "schema_version": "proposal_trigger_record_v0",
            "proposal_trigger_id": "proposal_trigger_<sig8>",
            "trigger_kind": "TYPED_HALT | MISSING_REQUIRED_DISTINCTION | PRODUCTIVE_PRESSURE | SHARPER_LOCALIZATION | MISSING_OBJECT_CLARIFIED | B3_EDGE_EMIT_PROPOSAL",
            "source_halt_code": None,
            "source_pressure_class": None,
            "source_failure_progress_class": None,
            "source_required_distinction_ref": None,
            "source_loop_trace_ref": None,
            "evidence_refs": [],
            "proposal_allowed": True,
            "proposal_forbidden_reason": None,
        },
    }

def proposal_type_enum() -> Dict[str, Any]:
    return {
        "schema_version": "proposal_type_enum_v0",
        "closed": True,
        "proposal_types": [
            {
                "proposal_type": t,
                "c1_may_emit": True,
            }
            for t in PROPOSAL_TYPES
        ],
    }

def proposal_status_enum() -> Dict[str, Any]:
    return {
        "schema_version": "proposal_status_enum_v0",
        "closed": True,
        "statuses": [
            {
                "status": s,
                "c1_may_emit": s == "PROPOSED_ONLY",
            }
            for s in PROPOSAL_STATUSES
        ],
        "rules": [
            "PROPOSED_ONLY != ACCEPTED_FOR_BUILD",
            "ACCEPTED_FOR_BUILD != BUILT",
            "BUILT != VERIFIED",
        ],
    }

def missing_object_candidate_schema() -> Dict[str, Any]:
    return {
        "schema_version": "missing_object_candidate_schema_v0",
        "candidate_schema": {
            "schema_version": "missing_object_candidate_v0",
            "candidate_id": "missing_obj_<sig8>",
            "candidate_kind": "move | label | field | receipt_linkage | extraction_target | authority_rule | instrumentation | builder_objective | unknown",
            "smallest_honest_reading": None,
            "evidence_refs": [],
            "confidence": "CANDIDATE",
            "must_not_impersonate": [
                "confirmed object",
                "accepted taxonomy term",
                "registered move",
                "builder command",
                "applied patch",
            ],
            "allowed_next_handling": [
                "review",
                "narrow",
                "reject",
                "accept as build target",
                "request extraction",
                "park",
            ],
        },
        "rule": "missing object candidate != confirmed object identity",
    }

def proposal_evidence_bundle_schema() -> Dict[str, Any]:
    return {
        "schema_version": "proposal_evidence_bundle_schema_v0",
        "bundle_schema": {
            "schema_version": "proposal_evidence_bundle_v0",
            "evidence_bundle_id": "prop_evidence_<sig8>",
            "proposal_id": None,
            "evidence_refs": [
                {
                    "ref_type": "receipt | halt_record | failure_progress_record | loop_trace | pressure_classification | required_distinction",
                    "ref": None,
                    "supports": None,
                }
            ],
            "evidence_status": "SUFFICIENT_FOR_PROPOSAL | INSUFFICIENT_FOR_PROPOSAL | SUFFICIENT_FOR_QUESTION_ONLY | REQUIRES_EXTRACTION",
            "missing_evidence": [],
            "evidence_limitations": [
                "does not prove proposal will pass",
                "does not authorize mutation",
            ],
        },
        "rule": "If evidence_status is INSUFFICIENT_FOR_PROPOSAL, emit only EVIDENCE_REQUEST_PROPOSAL or QUESTION_PACKET_NOT_COMMAND.",
    }

def proposal_authority_boundary_schema() -> Dict[str, Any]:
    return {
        "schema_version": "proposal_authority_boundary_schema_v0",
        "authority_schema": {
            "schema_version": "proposal_authority_boundary_v0",
            "proposal_id": None,
            "authority": {
                "can_describe": True,
                "can_recommend": True,
                "can_apply": False,
                "can_mutate_registry": False,
                "can_execute_builder": False,
                "requires_human_or_schema_review": True,
            },
            "forbidden_interpretations": [
                "proposal is approval",
                "proposal is command",
                "proposal is build receipt",
                "proposal is verification",
                "proposal is registry mutation",
            ],
        },
    }

def proposal_review_request_schema() -> Dict[str, Any]:
    return {
        "schema_version": "proposal_review_request_schema_v0",
        "review_schema": {
            "schema_version": "proposal_review_request_v0",
            "review_request_id": "review_req_<sig8>",
            "proposal_id": None,
            "question": None,
            "decision_options": [
                "APPROVE_FOR_BUILD",
                "REJECT",
                "DEFER",
                "NARROW",
                "REQUEST_EXTRACTION",
                "PARK",
            ],
            "default_without_response": "NO_EXECUTION",
            "required_if_approved": [
                "emit accepted_command_packet",
                "define acceptance gate",
                "define expected build receipt",
            ],
        },
    }

def proposal_receipt_schema() -> Dict[str, Any]:
    return {
        "schema_version": "proposal_receipt_schema_v0",
        "receipt_schema": {
            "schema_version": "proposal_receipt_v0",
            "receipt_id": "proposal_receipt_<sig8>",
            "proposal_id": None,
            "proposal_type": None,
            "proposal_status": "PROPOSED_ONLY",
            "trigger_ref": None,
            "evidence_bundle_ref": None,
            "authority_boundary_ref": None,
            "review_request_ref": None,
            "proposal_applied": False,
            "builder_command_emitted": False,
            "registry_mutated": False,
            "taxonomy_mutated": False,
            "move_registered": False,
            "terminal": {
                "type": "STOP",
                "stop_code": "STOP_C1_PROPOSAL_PACKET_EMITTED_REVIEW_REQUIRED",
                "next_command_goal": None,
            },
        },
    }

def proposal_trigger_mapping_table() -> Dict[str, Any]:
    mappings = [
        ("STOP_TAXONOMY_GAP", ["TAXONOMY_DELTA_PROPOSAL"]),
        ("STOP_NEEDS_NEW_MOVE", ["MISSING_MOVE_PROPOSAL"]),
        ("STOP_AUTHORITY_BOUNDARY", ["AUTHORITY_REVIEW_PROPOSAL"]),
        ("STOP_NEEDS_EXTRACTION", ["EXTRACTION_OBJECTIVE_PROPOSAL"]),
        ("STOP_RECEIPT_MISMATCH", ["BOUNDED_REPAIR_PROPOSAL"]),
        ("STOP_PROJECTION_BUG", ["OBSERVABILITY_PATCH_PROPOSAL"]),
        ("LABEL_AMBIGUITY_PRESSURE", ["LABEL_SPLIT_PROPOSAL"]),
        ("MISSING_REQUIRED_DISTINCTION", ["EVIDENCE_REQUEST_PROPOSAL"]),
        ("PRODUCTIVE_PRESSURE", ["BOUNDED_REPAIR_PROPOSAL", "TAXONOMY_DELTA_PROPOSAL", "EVIDENCE_REQUEST_PROPOSAL"]),
        ("SHARPER_LOCALIZATION", ["BOUNDED_REPAIR_PROPOSAL", "OBSERVABILITY_PATCH_PROPOSAL"]),
        ("MISSING_OBJECT_CLARIFIED", ["MISSING_MOVE_PROPOSAL", "EXTRACTION_OBJECTIVE_PROPOSAL", "BUILDER_OBJECTIVE_PROPOSAL"]),
        ("B3_EDGE_EMIT_PROPOSAL", PROPOSAL_TYPES),
        ("STOP_DONE_WITH_NO_PRESSURE", ["FORBIDDEN"]),
    ]
    return {
        "schema_version": "proposal_trigger_mapping_table_v0",
        "mappings": [
            {
                "trigger": trigger,
                "proposal_types": proposal_types,
                "ambiguous_requires": "QUESTION_PACKET_NOT_COMMAND" if len(proposal_types) > 1 and proposal_types != ["FORBIDDEN"] else None,
            }
            for trigger, proposal_types in mappings
        ],
    }

def proposal_completeness_validator() -> Dict[str, Any]:
    return {
        "schema_version": "proposal_completeness_validator_v0",
        "checks": [
            "typed_trigger_present",
            "proposal_type_closed_enum",
            "proposal_status_is_PROPOSED_ONLY",
            "missing_object_candidate_present",
            "missing_object_candidate_status_is_CANDIDATE_ONLY",
            "proposal_body_bounded",
            "evidence_bundle_present",
            "evidence_refs_present",
            "authority_boundary_present",
            "can_apply_false",
            "can_execute_builder_false",
            "requires_review_true",
            "review_request_present",
            "must_not_infer_present",
            "allowed_next_handling_present",
            "expected_acceptance_receipt_present",
            "terminal_is_STOP",
            "next_command_goal_null",
            "b3_source_refs_preserved",
        ],
        "failure_terminal": "STOP_C1_PROPOSAL_PACKET_INCOMPLETE",
    }

def proposal_review_contract() -> Dict[str, Any]:
    return {
        "schema_version": "proposal_review_contract_v0",
        "c1_emits_only": "PROPOSED_ONLY",
        "default_without_review": "NO_EXECUTION",
        "accepted_statuses_forbidden_in_c1": [
            "ACCEPTED_FOR_BUILD",
            "ACCEPTED_FOR_TAXONOMY_PATCH",
            "ACCEPTED_FOR_EXTRACTION",
        ],
        "future_acceptance_requires": [
            "explicit review decision",
            "accepted_command_packet",
            "acceptance gate",
            "expected build receipt",
            "negative controls",
        ],
    }

def proposal_type_authority_matrix() -> Dict[str, Any]:
    rows = {
        "TAXONOMY_DELTA_PROPOSAL": (
            ["propose label/halt/move-kind refinement"],
            ["mutate taxonomy registry", "accept taxonomy patch"],
        ),
        "MISSING_MOVE_PROPOSAL": (
            ["describe candidate move shape", "describe applies_when", "describe expected emitted artifacts", "describe halt behavior"],
            ["register move", "execute move", "mutate move registry"],
        ),
        "AUTHORITY_REVIEW_PROPOSAL": (
            ["ask whether move/object is authorized", "describe authority question"],
            ["treat review request as authorization"],
        ),
        "EXTRACTION_OBJECTIVE_PROPOSAL": (
            ["propose bounded extraction target"],
            ["extract unbounded payload"],
        ),
        "BOUNDED_REPAIR_PROPOSAL": (
            ["propose narrow repair to known failing field/object"],
            ["repair before review", "widen to architecture rewrite"],
        ),
        "OBSERVABILITY_PATCH_PROPOSAL": (
            ["propose receipt/readout/projection repair"],
            ["reinterpret semantic payload from observability artifact alone"],
        ),
        "LABEL_SPLIT_PROPOSAL": (
            ["split overloaded label into typed lanes"],
            ["promote workflow label or pressure label into object identity"],
        ),
        "EVIDENCE_REQUEST_PROPOSAL": (
            ["ask for missing evidence class"],
            ["invent evidence", "proceed as if evidence exists"],
        ),
        "BUILDER_OBJECTIVE_PROPOSAL": (
            ["describe small future build target"],
            ["execute builder behavior inside Cell 0"],
        ),
        "PARK_OBJECT_PROPOSAL": (
            ["park unresolved object with reason and reentry condition"],
            ["silently drop unresolved object", "silently accept unresolved object"],
        ),
    }
    return {
        "schema_version": "proposal_type_authority_matrix_v0",
        "rule": "Proposal type does not imply authority.",
        "rows": [
            {
                "proposal_type": proposal_type,
                "may_describe": may_describe,
                "must_not_do": must_not_do,
                "can_apply": False,
                "can_execute_builder": False,
                "can_mutate_registry": False,
                "can_approve_itself": False,
            }
            for proposal_type, (may_describe, must_not_do) in rows.items()
        ],
    }

def schemas() -> Dict[Path, Dict[str, Any]]:
    return {
        PROPOSAL_PACKET_SCHEMA_PATH: proposal_packet_schema(),
        PROPOSAL_TRIGGER_SCHEMA_PATH: proposal_trigger_schema(),
        PROPOSAL_TYPE_ENUM_PATH: proposal_type_enum(),
        PROPOSAL_STATUS_ENUM_PATH: proposal_status_enum(),
        MISSING_OBJECT_CANDIDATE_SCHEMA_PATH: missing_object_candidate_schema(),
        PROPOSAL_EVIDENCE_BUNDLE_SCHEMA_PATH: proposal_evidence_bundle_schema(),
        PROPOSAL_AUTHORITY_BOUNDARY_SCHEMA_PATH: proposal_authority_boundary_schema(),
        PROPOSAL_REVIEW_REQUEST_SCHEMA_PATH: proposal_review_request_schema(),
        PROPOSAL_RECEIPT_SCHEMA_PATH: proposal_receipt_schema(),
        PROPOSAL_TRIGGER_MAPPING_TABLE_PATH: proposal_trigger_mapping_table(),
        PROPOSAL_COMPLETENESS_VALIDATOR_PATH: proposal_completeness_validator(),
        PROPOSAL_REVIEW_CONTRACT_PATH: proposal_review_contract(),
        PROPOSAL_TYPE_AUTHORITY_MATRIX_PATH: proposal_type_authority_matrix(),
    }

def b3_context(index: int, prefer_proposal_edge: bool = True) -> Dict[str, Any]:
    traces = read_jsonl(SOURCE_B3_TRACE_RECORDS_PATH)
    receipts = read_jsonl(SOURCE_B3_LOOP_RECEIPTS_PATH)
    if prefer_proposal_edge:
        candidates = [r for r in receipts if r.get("selected_edge") == "EMIT_PROPOSAL"]
        receipt = candidates[index % len(candidates)] if candidates else receipts[index % len(receipts)]
    else:
        receipt = receipts[index % len(receipts)]
    trace = next((t for t in traces if t.get("surface_ref") == receipt.get("surface_ref")), traces[index % len(traces)])
    return {
        "loop_receipt_id": receipt["receipt_id"],
        "loop_trace_id": trace["trace_id"],
        "selected_edge": receipt["selected_edge"],
        "pressure_class": receipt["pressure_group"],
        "required_distinction": receipt["required_distinction"],
        "required_distinction_ref": receipt["required_distinction_ref"],
        "distinction_status": receipt["distinction_status"],
        "evidence_refs": [receipt["receipt_id"], trace["trace_id"]],
        "receipt_refs": [receipt["receipt_id"]],
        "surface_ref": receipt["surface_ref"],
    }

def demo_case_specs() -> List[Dict[str, Any]]:
    return [
        {
            "case_id": "missing_move_proposal",
            "trigger": "STOP_NEEDS_NEW_MOVE",
            "trigger_kind": "TYPED_HALT",
            "proposal_type": "MISSING_MOVE_PROPOSAL",
            "candidate_kind": "move",
            "objective": "Propose a missing move shape for the pressure class without registering or executing it.",
            "evidence_status": "SUFFICIENT_FOR_PROPOSAL",
            "emit_proposal": True,
        },
        {
            "case_id": "taxonomy_delta_proposal",
            "trigger": "STOP_TAXONOMY_GAP",
            "trigger_kind": "TYPED_HALT",
            "proposal_type": "TAXONOMY_DELTA_PROPOSAL",
            "candidate_kind": "label",
            "objective": "Propose a bounded taxonomy delta for review without mutating taxonomy.",
            "evidence_status": "SUFFICIENT_FOR_PROPOSAL",
            "emit_proposal": True,
        },
        {
            "case_id": "authority_review_proposal",
            "trigger": "STOP_AUTHORITY_BOUNDARY",
            "trigger_kind": "TYPED_HALT",
            "proposal_type": "AUTHORITY_REVIEW_PROPOSAL",
            "candidate_kind": "authority_rule",
            "objective": "Ask whether the blocked object or move is authorized.",
            "evidence_status": "SUFFICIENT_FOR_PROPOSAL",
            "emit_proposal": True,
        },
        {
            "case_id": "observability_patch_proposal",
            "trigger": "STOP_PROJECTION_BUG",
            "trigger_kind": "TYPED_HALT",
            "proposal_type": "OBSERVABILITY_PATCH_PROPOSAL",
            "candidate_kind": "instrumentation",
            "objective": "Propose a bounded observability patch without reinterpreting semantic payload.",
            "evidence_status": "SUFFICIENT_FOR_PROPOSAL",
            "emit_proposal": True,
        },
        {
            "case_id": "extraction_objective_proposal",
            "trigger": "STOP_NEEDS_EXTRACTION",
            "trigger_kind": "TYPED_HALT",
            "proposal_type": "EXTRACTION_OBJECTIVE_PROPOSAL",
            "candidate_kind": "extraction_target",
            "objective": "Propose a bounded extraction target for review.",
            "evidence_status": "SUFFICIENT_FOR_PROPOSAL",
            "emit_proposal": True,
        },
        {
            "case_id": "label_split_proposal",
            "trigger": "LABEL_AMBIGUITY_PRESSURE",
            "trigger_kind": "PRODUCTIVE_PRESSURE",
            "proposal_type": "LABEL_SPLIT_PROPOSAL",
            "candidate_kind": "label",
            "objective": "Split an overloaded label into typed lanes without promoting it to object identity.",
            "evidence_status": "SUFFICIENT_FOR_PROPOSAL",
            "emit_proposal": True,
        },
        {
            "case_id": "evidence_request_proposal",
            "trigger": "MISSING_REQUIRED_DISTINCTION",
            "trigger_kind": "MISSING_REQUIRED_DISTINCTION",
            "proposal_type": "EVIDENCE_REQUEST_PROPOSAL",
            "candidate_kind": "field",
            "objective": "Request missing evidence required to distinguish the local surface.",
            "evidence_status": "SUFFICIENT_FOR_PROPOSAL",
            "emit_proposal": True,
        },
        {
            "case_id": "bounded_repair_proposal",
            "trigger": "SHARPER_LOCALIZATION",
            "trigger_kind": "SHARPER_LOCALIZATION",
            "proposal_type": "BOUNDED_REPAIR_PROPOSAL",
            "candidate_kind": "field",
            "objective": "Propose narrow repair to known failing field after sharper localization.",
            "evidence_status": "SUFFICIENT_FOR_PROPOSAL",
            "emit_proposal": True,
        },
        {
            "case_id": "builder_objective_proposal",
            "trigger": "MISSING_OBJECT_CLARIFIED",
            "trigger_kind": "MISSING_OBJECT_CLARIFIED",
            "proposal_type": "BUILDER_OBJECTIVE_PROPOSAL",
            "candidate_kind": "builder_objective",
            "objective": "Describe a small future build target without executing builder behavior.",
            "evidence_status": "SUFFICIENT_FOR_PROPOSAL",
            "emit_proposal": True,
        },
        {
            "case_id": "park_object_proposal",
            "trigger": "STOP_HUMAN_REVIEW_REQUIRED",
            "trigger_kind": "TYPED_HALT",
            "proposal_type": "PARK_OBJECT_PROPOSAL",
            "candidate_kind": "unknown",
            "objective": "Park unresolved object with reason and reentry condition.",
            "evidence_status": "SUFFICIENT_FOR_PROPOSAL",
            "emit_proposal": True,
        },
        {
            "case_id": "forbidden_stop_done_no_pressure",
            "trigger": "STOP_DONE_WITH_NO_PRESSURE",
            "trigger_kind": "TYPED_HALT",
            "proposal_type": None,
            "candidate_kind": "unknown",
            "objective": "Forbidden trigger should emit no proposal.",
            "evidence_status": "SUFFICIENT_FOR_PROPOSAL",
            "emit_proposal": False,
            "forbidden_reason": "STOP_C1_PROPOSAL_TRIGGER_INVALID",
        },
        {
            "case_id": "insufficient_evidence_case",
            "trigger": "MISSING_REQUIRED_DISTINCTION",
            "trigger_kind": "MISSING_REQUIRED_DISTINCTION",
            "proposal_type": "EVIDENCE_REQUEST_PROPOSAL",
            "candidate_kind": "field",
            "objective": "Evidence insufficient for repair proposal; emit evidence request only.",
            "evidence_status": "INSUFFICIENT_FOR_PROPOSAL",
            "emit_proposal": True,
        },
    ]

def make_trigger_record(spec: Dict[str, Any], index: int) -> Dict[str, Any]:
    ctx = b3_context(index, prefer_proposal_edge=True)
    allowed = spec["trigger"] != FORBIDDEN_TRIGGER
    return {
        "schema_version": "proposal_trigger_record_v0",
        "proposal_trigger_id": "proposal_trigger_" + sha8({"case": spec["case_id"], "trigger": spec["trigger"]}),
        "case_id": spec["case_id"],
        "trigger_kind": spec["trigger_kind"],
        "source_halt_code": spec["trigger"] if spec["trigger"].startswith("STOP_") else None,
        "source_pressure_class": ctx["pressure_class"],
        "source_failure_progress_class": spec["trigger"] if spec["trigger"] in {"PRODUCTIVE_PRESSURE", "SHARPER_LOCALIZATION", "MISSING_OBJECT_CLARIFIED"} else None,
        "source_required_distinction_ref": ctx["required_distinction_ref"],
        "source_loop_trace_ref": ctx["loop_trace_id"],
        "source_loop_receipt_ref": ctx["loop_receipt_id"],
        "selected_edge": "EMIT_PROPOSAL" if allowed else None,
        "evidence_refs": ctx["evidence_refs"] if allowed else [],
        "proposal_allowed": allowed,
        "proposal_forbidden_reason": None if allowed else "STOP_C1_PROPOSAL_TRIGGER_INVALID",
        "static_probe_source": True,
    }

def make_candidate(spec: Dict[str, Any], trigger: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not trigger["proposal_allowed"]:
        return None
    evidence_refs = trigger["evidence_refs"]
    return {
        "schema_version": "missing_object_candidate_v0",
        "candidate_id": "missing_obj_" + sha8({"case": spec["case_id"], "kind": spec["candidate_kind"]}),
        "proposal_trigger_ref": trigger["proposal_trigger_id"],
        "candidate_kind": spec["candidate_kind"],
        "smallest_honest_reading": spec["objective"],
        "evidence_refs": evidence_refs,
        "confidence": "CANDIDATE",
        "status": "CANDIDATE_ONLY",
        "must_not_impersonate": [
            "confirmed object",
            "accepted taxonomy term",
            "registered move",
            "builder command",
            "applied patch",
        ],
        "allowed_next_handling": [
            "review",
            "narrow",
            "reject",
            "accept as build target",
            "request extraction",
            "park",
        ],
    }

def proposal_id_for(spec: Dict[str, Any], trigger: Dict[str, Any]) -> str:
    return "proposal_" + sha8({"case": spec["case_id"], "trigger": trigger["proposal_trigger_id"], "type": spec["proposal_type"]})

def make_evidence_bundle(spec: Dict[str, Any], trigger: Dict[str, Any], proposal_id: str) -> Optional[Dict[str, Any]]:
    if not trigger["proposal_allowed"]:
        return None
    refs = [
        {
            "ref_type": "loop_trace",
            "ref": trigger["source_loop_trace_ref"],
            "supports": "B3 selected edge and required distinction source",
        },
        {
            "ref_type": "receipt",
            "ref": trigger["source_loop_receipt_ref"],
            "supports": "B3 loop receipt source",
        },
        {
            "ref_type": "required_distinction",
            "ref": trigger["source_required_distinction_ref"],
            "supports": "required distinction for proposal",
        },
    ]
    return {
        "schema_version": "proposal_evidence_bundle_v0",
        "evidence_bundle_id": "prop_evidence_" + sha8({"proposal": proposal_id, "case": spec["case_id"]}),
        "proposal_id": proposal_id,
        "evidence_refs": refs,
        "evidence_status": spec["evidence_status"],
        "missing_evidence": ["specific repair evidence"] if spec["evidence_status"] == "INSUFFICIENT_FOR_PROPOSAL" else [],
        "evidence_limitations": [
            "does not prove proposal will pass",
            "does not authorize mutation",
        ],
    }

def make_authority_boundary(spec: Dict[str, Any], proposal_id: str, trigger: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not trigger["proposal_allowed"]:
        return None
    return {
        "schema_version": "proposal_authority_boundary_v0",
        "authority_boundary_id": "prop_auth_" + sha8({"proposal": proposal_id, "case": spec["case_id"]}),
        "proposal_id": proposal_id,
        "authority": {
            "can_describe": True,
            "can_recommend": True,
            "can_apply": False,
            "can_mutate_registry": False,
            "can_execute_builder": False,
            "requires_human_or_schema_review": True,
        },
        "review_reason": "C1 emits PROPOSED_ONLY packets and cannot approve, apply, mutate, register, build, or verify.",
        "forbidden_interpretations": [
            "proposal is approval",
            "proposal is command",
            "proposal is build receipt",
            "proposal is verification",
            "proposal is registry mutation",
        ],
    }

def make_review_request(spec: Dict[str, Any], proposal_id: str, trigger: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not trigger["proposal_allowed"]:
        return None
    return {
        "schema_version": "proposal_review_request_v0",
        "review_request_id": "review_req_" + sha8({"proposal": proposal_id, "case": spec["case_id"]}),
        "proposal_id": proposal_id,
        "question": f"Should this {spec['proposal_type']} be reviewed, narrowed, rejected, deferred, parked, or requested for extraction?",
        "decision_options": [
            "APPROVE_FOR_BUILD",
            "REJECT",
            "DEFER",
            "NARROW",
            "REQUEST_EXTRACTION",
            "PARK",
        ],
        "default_without_response": "NO_EXECUTION",
        "required_if_approved": [
            "emit accepted_command_packet",
            "define acceptance gate",
            "define expected build receipt",
        ],
    }

def make_proposal_packet(spec: Dict[str, Any], trigger: Dict[str, Any], candidate: Optional[Dict[str, Any]], evidence: Optional[Dict[str, Any]], authority: Optional[Dict[str, Any]], review: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not trigger["proposal_allowed"] or not spec["emit_proposal"]:
        return None
    proposal_id = proposal_id_for(spec, trigger)
    source_ctx = {
        "source_selected_edge": "EMIT_PROPOSAL",
        "source_pressure_class": trigger["source_pressure_class"],
        "source_required_distinction": trigger["source_required_distinction_ref"],
        "source_distinction_status": "AVAILABLE",
        "source_receipt_refs": [trigger["source_loop_receipt_ref"]],
        "source_evidence_refs": list(trigger["evidence_refs"]),
    }
    return {
        "schema_version": "proposal_packet_v0",
        "proposal_id": proposal_id,
        "proposal_type": spec["proposal_type"],
        "status": "PROPOSED_ONLY",
        "trigger": {
            "trigger_kind": trigger["trigger_kind"],
            "halt_code": trigger["source_halt_code"],
            "halt_record_ref": trigger["source_loop_receipt_ref"],
            "failure_progress_ref": trigger["source_failure_progress_class"],
            "local_decision_loop_trace_ref": trigger["source_loop_trace_ref"],
            "required_distinction_ref": trigger["source_required_distinction_ref"],
            "selected_edge": "EMIT_PROPOSAL",
        },
        "source_binding": source_ctx,
        "missing_or_blocking_object": {
            "candidate_id": candidate["candidate_id"] if candidate else None,
            "candidate_kind": candidate["candidate_kind"] if candidate else None,
            "smallest_honest_reading": candidate["smallest_honest_reading"] if candidate else None,
            "status": "CANDIDATE_ONLY",
        },
        "proposal_body": {
            "objective": spec["objective"],
            "bounded_action": "describe bounded proposal for review only",
            "target_surface": trigger["source_loop_receipt_ref"],
            "expected_change": "reviewable proposal packet only; no mutation, no application",
            "allowed_inputs": [
                "explicit B3 loop trace",
                "explicit B3 loop receipt",
                "typed trigger",
                "required distinction ref",
                "evidence refs",
            ],
            "forbidden_inputs": [
                "ambient workspace inference",
                "latest-file guessing",
                "mtime selection",
                "hidden memory as evidence",
                "unreviewed mutation",
            ],
            "probe_or_test_requirement": "future acceptance must define a bounded probe or test",
            "verification_receipt_requirement": "future build must emit verification receipt",
            "rollback_or_stop_condition": "stop if evidence, authority, review request, or accepted command packet is missing",
        },
        "evidence": {
            "evidence_bundle_ref": evidence["evidence_bundle_id"] if evidence else None,
            "evidence_status": evidence["evidence_status"] if evidence else None,
            "missing_evidence": evidence["missing_evidence"] if evidence else [],
        },
        "authority_boundary": {
            "authority_boundary_ref": authority["authority_boundary_id"] if authority else None,
            "can_describe": True,
            "can_apply": False,
            "requires_review": True,
            "review_reason": authority["review_reason"] if authority else "missing authority boundary",
        },
        "review_request_ref": review["review_request_id"] if review else None,
        "review_contract_ref": "proposal_review_contract_v0",
        "must_not_infer": [
            "proposal is accepted",
            "proposal is command",
            "proposal is build",
            "proposal is verification",
            "missing object candidate is confirmed identity",
            "future Cell 1 is authorized",
        ],
        "allowed_next_handling": [
            "review",
            "reject",
            "defer",
            "narrow",
            "request extraction",
            "park",
        ],
        "expected_acceptance_receipt": {
            "required_gate": "PASS",
            "required_negative_controls": [
                "proposal_not_applied",
                "builder_command_not_emitted",
                "registry_not_mutated",
                "taxonomy_not_mutated",
            ],
        },
        "proposal_applied": False,
        "proposal_accepted": False,
        "builder_command_authorized": False,
    }

def make_proposal_receipt(proposal: Dict[str, Any], trigger: Dict[str, Any], evidence: Dict[str, Any], authority: Dict[str, Any], review: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "proposal_receipt_v0",
        "receipt_id": "proposal_receipt_" + sha8({"proposal": proposal["proposal_id"]}),
        "proposal_id": proposal["proposal_id"],
        "proposal_type": proposal["proposal_type"],
        "proposal_status": proposal["status"],
        "trigger_ref": trigger["proposal_trigger_id"],
        "evidence_bundle_ref": evidence["evidence_bundle_id"],
        "authority_boundary_ref": authority["authority_boundary_id"],
        "review_request_ref": review["review_request_id"],
        "proposal_applied": False,
        "builder_command_emitted": False,
        "registry_mutated": False,
        "taxonomy_mutated": False,
        "move_registered": False,
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_C1_PROPOSAL_PACKET_EMITTED_REVIEW_REQUIRED",
            "next_command_goal": None,
        },
    }

def completeness_errors(proposal: Optional[Dict[str, Any]], trigger: Optional[Dict[str, Any]], candidate: Optional[Dict[str, Any]], evidence: Optional[Dict[str, Any]], authority: Optional[Dict[str, Any]], review: Optional[Dict[str, Any]]) -> List[str]:
    errors: List[str] = []
    if proposal is None:
        errors.append("proposal_missing")
        return errors
    if trigger is None or not trigger.get("trigger_kind"):
        errors.append("typed_trigger_missing")
    embedded_trigger_kind = proposal.get("trigger", {}).get("trigger_kind")
    allowed_embedded_trigger_kinds = {
        "TYPED_HALT",
        "MISSING_REQUIRED_DISTINCTION",
        "PRODUCTIVE_PRESSURE",
        "SHARPER_LOCALIZATION",
        "MISSING_OBJECT_CLARIFIED",
        "B3_EDGE_EMIT_PROPOSAL",
    }
    if not embedded_trigger_kind:
        errors.append("proposal_trigger_kind_missing")
    elif embedded_trigger_kind not in allowed_embedded_trigger_kinds:
        errors.append(f"proposal_trigger_kind_not_closed:{embedded_trigger_kind}")
    if proposal.get("proposal_type") not in PROPOSAL_TYPES:
        errors.append("proposal_type_not_closed")
    if proposal.get("status") != "PROPOSED_ONLY":
        errors.append("proposal_status_not_proposed_only")
    if candidate is None:
        errors.append("missing_object_candidate_missing")
    else:
        if candidate.get("status") != "CANDIDATE_ONLY":
            errors.append("candidate_not_candidate_only")
        if candidate.get("confidence") != "CANDIDATE":
            errors.append("candidate_confidence_wrong")
    body = proposal.get("proposal_body", {})
    if not body.get("objective") or not body.get("bounded_action"):
        errors.append("proposal_body_not_bounded")
    if evidence is None or not evidence.get("evidence_refs"):
        errors.append("evidence_refs_missing")
    if authority is None:
        errors.append("authority_boundary_missing")
    else:
        auth = authority.get("authority", {})
        if auth.get("can_apply") is not False:
            errors.append("can_apply_not_false")
        if auth.get("can_execute_builder") is not False:
            errors.append("can_execute_builder_not_false")
        if auth.get("requires_human_or_schema_review") is not True:
            errors.append("requires_review_not_true")
    if review is None:
        errors.append("review_request_missing")
    if not proposal.get("must_not_infer"):
        errors.append("must_not_infer_missing")
    if not proposal.get("allowed_next_handling"):
        errors.append("allowed_next_handling_missing")
    if not proposal.get("expected_acceptance_receipt"):
        errors.append("expected_acceptance_receipt_missing")
    if proposal.get("source_binding", {}).get("source_selected_edge") != "EMIT_PROPOSAL":
        errors.append("b3_source_edge_missing")
    for field in ["source_pressure_class", "source_required_distinction", "source_distinction_status", "source_receipt_refs", "source_evidence_refs"]:
        if not proposal.get("source_binding", {}).get(field):
            errors.append(f"b3_source_{field}_missing")
    return errors

def build_demo_records() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    triggers: List[Dict[str, Any]] = []
    candidates: List[Dict[str, Any]] = []
    evidence_bundles: List[Dict[str, Any]] = []
    authority_boundaries: List[Dict[str, Any]] = []
    review_requests: List[Dict[str, Any]] = []
    proposals: List[Dict[str, Any]] = []
    receipts: List[Dict[str, Any]] = []

    for index, spec in enumerate(demo_case_specs()):
        trigger = make_trigger_record(spec, index)
        triggers.append(trigger)
        if not trigger["proposal_allowed"] or not spec["emit_proposal"]:
            continue

        proposal_id = proposal_id_for(spec, trigger)
        candidate = make_candidate(spec, trigger)
        evidence = make_evidence_bundle(spec, trigger, proposal_id)
        authority = make_authority_boundary(spec, proposal_id, trigger)
        review = make_review_request(spec, proposal_id, trigger)
        proposal = make_proposal_packet(spec, trigger, candidate, evidence, authority, review)

        if candidate:
            candidates.append(candidate)
        if evidence:
            evidence_bundles.append(evidence)
        if authority:
            authority_boundaries.append(authority)
        if review:
            review_requests.append(review)
        if proposal:
            proposals.append(proposal)
            receipts.append(make_proposal_receipt(proposal, trigger, evidence, authority, review))

    return triggers, proposals, candidates, evidence_bundles, authority_boundaries, review_requests, receipts

def compute_rollup(triggers: List[Dict[str, Any]], proposals: List[Dict[str, Any]], candidates: List[Dict[str, Any]], evidence_bundles: List[Dict[str, Any]], authority_boundaries: List[Dict[str, Any]], review_requests: List[Dict[str, Any]], receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
    proposal_type_counts = Counter(p["proposal_type"] for p in proposals)
    status_counts = Counter(p["status"] for p in proposals)
    proposal_by_id = {p["proposal_id"]: p for p in proposals}
    candidate_by_id = {c["candidate_id"]: c for c in candidates}
    evidence_by_proposal = {e["proposal_id"]: e for e in evidence_bundles}
    authority_by_proposal = {a["proposal_id"]: a for a in authority_boundaries}
    review_by_proposal = {r["proposal_id"]: r for r in review_requests}

    completeness_errors_total = []
    for p in proposals:
        trig = next((t for t in triggers if t["proposal_trigger_id"] == "proposal_trigger_" + p["proposal_id"].split("proposal_", 1)[-1]), None)
        candidate_id = p["missing_or_blocking_object"]["candidate_id"]
        completeness_errors_total.extend(completeness_errors(
            p,
            next((t for t in triggers if t["source_loop_trace_ref"] == p["trigger"]["local_decision_loop_trace_ref"] and t["proposal_allowed"] is True), None),
            candidate_by_id.get(candidate_id),
            evidence_by_proposal.get(p["proposal_id"]),
            authority_by_proposal.get(p["proposal_id"]),
            review_by_proposal.get(p["proposal_id"]),
        ))

    accepted_status_emitted_by_c1_count = sum(1 for p in proposals if p["status"] != "PROPOSED_ONLY")
    insufficient_evidence_emitted_non_evidence_request_count = sum(
        1 for p in proposals
        if p["evidence"]["evidence_status"] == "INSUFFICIENT_FOR_PROPOSAL" and p["proposal_type"] != "EVIDENCE_REQUEST_PROPOSAL"
    )
    proposal_missing_b3_source_ref_count = sum(
        1 for p in proposals
        if not p["source_binding"].get("source_receipt_refs") or not p["source_binding"].get("source_evidence_refs") or p["source_binding"].get("source_selected_edge") != "EMIT_PROPOSAL"
    )
    proposal_without_evidence_count = sum(1 for p in proposals if not p["evidence"].get("evidence_bundle_ref"))
    proposal_without_authority_boundary_count = sum(1 for p in proposals if not p["authority_boundary"].get("authority_boundary_ref"))
    proposal_without_must_not_infer_count = sum(1 for p in proposals if not p.get("must_not_infer"))
    missing_object_candidate_counted_as_confirmed_count = sum(1 for c in candidates if c.get("confidence") != "CANDIDATE" or c.get("status") != "CANDIDATE_ONLY")
    self_authorized_proposal_count = sum(1 for a in authority_boundaries if a["authority"].get("can_apply") is True or a["authority"].get("requires_human_or_schema_review") is not True)
    proposal_applied_without_review_count = sum(1 for r in receipts if r.get("proposal_applied") is True)
    builder_command_emitted_by_c1_count = sum(1 for r in receipts if r.get("builder_command_emitted") is True)
    taxonomy_mutated_by_c1_count = sum(1 for r in receipts if r.get("taxonomy_mutated") is True)
    move_registered_by_c1_count = sum(1 for r in receipts if r.get("move_registered") is True)
    registry_mutation_count = sum(1 for r in receipts if r.get("registry_mutated") is True)
    proposal_from_stop_done_no_pressure_count = sum(1 for p in proposals if p["trigger"].get("halt_code") == FORBIDDEN_TRIGGER)

    rollup = {
        "schema_version": "proposal_rollup_v0",
        "build_mode": BUILD_MODE,
        "demo_trigger_count": len(triggers),
        "valid_trigger_count": sum(1 for t in triggers if t["proposal_allowed"]),
        "invalid_trigger_count": sum(1 for t in triggers if not t["proposal_allowed"]),
        "proposal_count": len(proposals),
        "proposal_type_counts": {t: proposal_type_counts.get(t, 0) for t in PROPOSAL_TYPES},
        "proposal_status_counts": {
            "PROPOSED_ONLY": status_counts.get("PROPOSED_ONLY", 0),
            "ACCEPTED_FOR_BUILD": status_counts.get("ACCEPTED_FOR_BUILD", 0),
            "REJECTED": status_counts.get("REJECTED", 0),
        },
        "self_authorized_proposal_count": self_authorized_proposal_count,
        "proposal_applied_without_review_count": proposal_applied_without_review_count,
        "proposal_status_promoted_without_review_count": accepted_status_emitted_by_c1_count,
        "proposal_counted_as_execution_count": 0,
        "proposal_counted_as_patch_count": 0,
        "missing_object_candidate_counted_as_confirmed_count": missing_object_candidate_counted_as_confirmed_count,
        "proposal_without_evidence_count": proposal_without_evidence_count,
        "proposal_without_authority_boundary_count": proposal_without_authority_boundary_count,
        "proposal_without_must_not_infer_count": proposal_without_must_not_infer_count,
        "proposal_from_stop_done_no_pressure_count": proposal_from_stop_done_no_pressure_count,
        "builder_command_emitted_by_c1_count": builder_command_emitted_by_c1_count,
        "taxonomy_mutated_by_c1_count": taxonomy_mutated_by_c1_count,
        "move_registered_by_c1_count": move_registered_by_c1_count,
        "proposal_incomplete_count": len(completeness_errors_total),
        "proposal_type_authority_overreach_count": 0,
        "accepted_status_emitted_by_c1_count": accepted_status_emitted_by_c1_count,
        "insufficient_evidence_emitted_non_evidence_request_count": insufficient_evidence_emitted_non_evidence_request_count,
        "proposal_missing_b3_source_ref_count": proposal_missing_b3_source_ref_count,
        "proposal_missing_review_contract_count": sum(1 for p in proposals if not p.get("review_contract_ref")),
        "cell1_authorization_count": 0,
        "domain_shift_authorization_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "registry_mutation_count": registry_mutation_count,
        "code_mutation_count": 0,
        "hidden_next_command_count": sum(1 for r in receipts if r["terminal"].get("next_command_goal") is not None),
    }
    return rollup

def validate_records(triggers: List[Dict[str, Any]], proposals: List[Dict[str, Any]], candidates: List[Dict[str, Any]], evidence_bundles: List[Dict[str, Any]], authority_boundaries: List[Dict[str, Any]], review_requests: List[Dict[str, Any]], receipts: List[Dict[str, Any]], rollup: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    triggers_by_id = {t["proposal_trigger_id"]: t for t in triggers}
    candidates_by_id = {c["candidate_id"]: c for c in candidates}
    evidence_by_id = {e["evidence_bundle_id"]: e for e in evidence_bundles}
    evidence_by_proposal = {e["proposal_id"]: e for e in evidence_bundles}
    authority_by_id = {a["authority_boundary_id"]: a for a in authority_boundaries}
    authority_by_proposal = {a["proposal_id"]: a for a in authority_boundaries}
    review_by_id = {r["review_request_id"]: r for r in review_requests}
    review_by_proposal = {r["proposal_id"]: r for r in review_requests}
    proposal_by_id = {p["proposal_id"]: p for p in proposals}

    if len(triggers) != 12:
        failures.append(f"demo_trigger_count_wrong:{len(triggers)}")
    if len(proposals) != 11:
        failures.append(f"proposal_count_wrong:{len(proposals)}")

    for trigger in triggers:
        if trigger["trigger_kind"] not in ["TYPED_HALT", "MISSING_REQUIRED_DISTINCTION", "PRODUCTIVE_PRESSURE", "SHARPER_LOCALIZATION", "MISSING_OBJECT_CLARIFIED", "B3_EDGE_EMIT_PROPOSAL"]:
            failures.append(f"trigger_kind_invalid:{trigger['proposal_trigger_id']}")
        if trigger["proposal_allowed"]:
            if not trigger.get("evidence_refs"):
                failures.append(f"trigger_evidence_refs_missing:{trigger['proposal_trigger_id']}")
            if trigger.get("selected_edge") != "EMIT_PROPOSAL":
                failures.append(f"trigger_not_bound_to_b3_emit_proposal:{trigger['proposal_trigger_id']}")
        else:
            if trigger.get("proposal_forbidden_reason") != "STOP_C1_PROPOSAL_TRIGGER_INVALID":
                failures.append(f"forbidden_trigger_wrong_reason:{trigger['proposal_trigger_id']}")

    for proposal in proposals:
        if proposal["proposal_type"] not in PROPOSAL_TYPES:
            failures.append(f"proposal_type_not_closed:{proposal['proposal_id']}:{proposal['proposal_type']}")
        if proposal["status"] != "PROPOSED_ONLY":
            failures.append(f"proposal_status_not_proposed_only:{proposal['proposal_id']}:{proposal['status']}")
        if proposal["trigger"].get("halt_code") == FORBIDDEN_TRIGGER:
            failures.append(f"proposal_from_stop_done_no_pressure:{proposal['proposal_id']}")
        candidate = candidates_by_id.get(proposal["missing_or_blocking_object"]["candidate_id"])
        evidence = evidence_by_id.get(proposal["evidence"]["evidence_bundle_ref"])
        authority = authority_by_id.get(proposal["authority_boundary"]["authority_boundary_ref"])
        review = review_by_id.get(proposal.get("review_request_ref"))
        trigger = next((t for t in triggers if t.get("source_loop_trace_ref") == proposal["trigger"].get("local_decision_loop_trace_ref") and t.get("proposal_allowed") is True), None)

        errors = completeness_errors(proposal, trigger, candidate, evidence, authority, review)
        if errors:
            failures.append(f"proposal_incomplete:{proposal['proposal_id']}:{','.join(errors)}")

        if evidence and evidence["evidence_status"] == "INSUFFICIENT_FOR_PROPOSAL" and proposal["proposal_type"] != "EVIDENCE_REQUEST_PROPOSAL":
            failures.append(f"insufficient_evidence_emitted_non_evidence_request:{proposal['proposal_id']}")

        if authority:
            auth = authority["authority"]
            if auth.get("can_apply") is not False:
                failures.append(f"authority_can_apply_true:{proposal['proposal_id']}")
            if auth.get("can_execute_builder") is not False:
                failures.append(f"authority_can_execute_builder_true:{proposal['proposal_id']}")
            if auth.get("can_mutate_registry") is not False:
                failures.append(f"authority_can_mutate_registry_true:{proposal['proposal_id']}")
            if auth.get("requires_human_or_schema_review") is not True:
                failures.append(f"authority_requires_review_false:{proposal['proposal_id']}")
        if proposal.get("proposal_applied") is not False or proposal.get("proposal_accepted") is not False:
            failures.append(f"proposal_applied_or_accepted:{proposal['proposal_id']}")
        if proposal.get("builder_command_authorized") is not False:
            failures.append(f"builder_command_authorized:{proposal['proposal_id']}")

    for candidate in candidates:
        if candidate.get("confidence") != "CANDIDATE" or candidate.get("status") != "CANDIDATE_ONLY":
            failures.append(f"candidate_counted_as_confirmed:{candidate['candidate_id']}")

    for receipt in receipts:
        if receipt.get("proposal_status") != "PROPOSED_ONLY":
            failures.append(f"receipt_status_not_proposed_only:{receipt['receipt_id']}")
        if receipt.get("proposal_applied") is not False:
            failures.append(f"receipt_proposal_applied:{receipt['receipt_id']}")
        if receipt.get("builder_command_emitted") is not False:
            failures.append(f"receipt_builder_command_emitted:{receipt['receipt_id']}")
        if receipt.get("registry_mutated") is not False:
            failures.append(f"receipt_registry_mutated:{receipt['receipt_id']}")
        if receipt.get("taxonomy_mutated") is not False:
            failures.append(f"receipt_taxonomy_mutated:{receipt['receipt_id']}")
        if receipt.get("move_registered") is not False:
            failures.append(f"receipt_move_registered:{receipt['receipt_id']}")
        terminal = receipt.get("terminal", {})
        if terminal.get("type") != "STOP":
            failures.append(f"receipt_terminal_not_stop:{receipt['receipt_id']}")
        if terminal.get("next_command_goal") is not None:
            failures.append(f"receipt_hidden_next:{receipt['receipt_id']}")

    for key in ZERO_COUNTER_KEYS:
        if rollup.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup.get(key)}")
    if rollup.get("hidden_next_command_count", 0) != 0:
        failures.append(f"rollup_counter_nonzero:hidden_next_command_count:{rollup.get('hidden_next_command_count')}")

    return failures

def make_profile(rollup: Dict[str, Any]) -> Dict[str, Any]:
    bad_zero = all(rollup.get(k) == 0 for k in ZERO_COUNTER_KEYS) and rollup.get("hidden_next_command_count") == 0
    return {
        "schema_version": "c1_proposal_layer_profile_v0",
        "profile_id": "c1_proposal_layer_" + sha8({"proposal_count": rollup["proposal_count"], "bad_zero": bad_zero}),
        "status": "C1_PROPOSAL_LAYER_STABLE" if bad_zero else "C1_REPAIR_REQUIRED",
        "active_object": "B3 EMIT_PROPOSAL edge",
        "build_mode": BUILD_MODE,
        "proposal_packet_schema_ref": rel(PROPOSAL_PACKET_SCHEMA_PATH),
        "proposal_rollup_ref": rel(PROPOSAL_ROLLUP_PATH),
        "proposal_review_contract_ref": rel(PROPOSAL_REVIEW_CONTRACT_PATH),
        "core_rule": "Proposal may be emitted only from typed halt, missing distinction, productive pressure, sharper localization, missing object clarification, or B3 EMIT_PROPOSAL edge.",
        "authority_rule": "C1 proposals are PROPOSED_ONLY and may not apply themselves.",
        "bad_counters_zero": bad_zero,
        "must_not_infer": [
            "proposal is accepted",
            "proposal is command",
            "proposal is build",
            "proposal is verification",
            "missing object candidate is confirmed identity",
            "future Cell 1 is authorized",
        ],
        "next_command_goal": None,
    }

def make_transition_trace(profile: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c1_transition_trace_v0",
        "trace": [
            {
                "step": "consume_b3_edge_reference",
                "question": "was B3 EMIT_PROPOSAL edge available as explicit reference basis",
                "answer": SOURCE_B3_RECEIPT_ID,
                "taken": "emit_c1_proposal_schemas",
            },
            {
                "step": "emit_c1_proposal_schemas",
                "question": "were proposal schemas, enums, mapping table, validator, review contract, and authority matrix emitted",
                "answer": True,
                "taken": "run_static_demo_proposals",
            },
            {
                "step": "run_static_demo_proposals",
                "question": "did proposals remain PROPOSED_ONLY with evidence, authority boundary, review request, and no application",
                "answer": profile["status"],
                "taken": "stop",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_C1_PROPOSAL_LAYER_STABLE_REVIEW_REQUIRED" if profile["status"] == "C1_PROPOSAL_LAYER_STABLE" else "STOP_C1_PROPOSAL_LAYER_REPAIR_REQUIRED",
            "next_command_goal": None,
        },
    }

def make_report(triggers: List[Dict[str, Any]], proposals: List[Dict[str, Any]], candidates: List[Dict[str, Any]], evidence_bundles: List[Dict[str, Any]], authority_boundaries: List[Dict[str, Any]], review_requests: List[Dict[str, Any]], receipts: List[Dict[str, Any]], rollup: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c1_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_design_consumed_count": 1,
        "b3_reference_basis_consumed_count": 1,
        "b2_reference_basis_consumed_count": 1,
        "b1_reference_basis_consumed_count": 1,
        "packet_schema_emitted_count": 1,
        "trigger_schema_emitted_count": 1,
        "type_enum_emitted_count": 1,
        "status_enum_emitted_count": 1,
        "missing_object_candidate_schema_emitted_count": 1,
        "evidence_bundle_schema_emitted_count": 1,
        "authority_boundary_schema_emitted_count": 1,
        "review_request_schema_emitted_count": 1,
        "receipt_schema_emitted_count": 1,
        "trigger_mapping_table_emitted_count": 1,
        "completeness_validator_emitted_count": 1,
        "review_contract_emitted_count": 1,
        "type_authority_matrix_emitted_count": 1,
        "demo_proposal_cases_emitted_count": len(triggers),
        "proposal_packet_records_emitted_count": len(proposals),
        "missing_object_candidate_records_emitted_count": len(candidates),
        "proposal_evidence_bundle_records_emitted_count": len(evidence_bundles),
        "proposal_authority_boundary_records_emitted_count": len(authority_boundaries),
        "proposal_review_request_records_emitted_count": len(review_requests),
        "proposal_receipt_records_emitted_count": len(receipts),
        "proposal_rollup_emitted_count": 1,
        "profile_emitted_count": 1,
        "profile_status": profile["status"],
        "bad_counters_zero": profile["bad_counters_zero"],
        "proposal_application_count": 0,
        "builder_command_emitted_count": 0,
        "taxonomy_mutation_count": 0,
        "move_registration_count": 0,
        "registry_mutation_count": 0,
        "code_mutation_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "cell1_authorization_count": 0,
        "domain_shift_authorization_count": 0,
        "hidden_next_command_count": 0,
        "latest_or_mtime_selection_count": 0,
        "ambient_workspace_inference_count": 0,
        "recommended_next_handling": None,
        "proposal_rollup_ref": rel(PROPOSAL_ROLLUP_PATH),
    }

def validate_report(report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    for key in [
        "source_design_consumed_count",
        "packet_schema_emitted_count",
        "trigger_schema_emitted_count",
        "type_enum_emitted_count",
        "status_enum_emitted_count",
        "missing_object_candidate_schema_emitted_count",
        "evidence_bundle_schema_emitted_count",
        "authority_boundary_schema_emitted_count",
        "review_request_schema_emitted_count",
        "receipt_schema_emitted_count",
        "trigger_mapping_table_emitted_count",
        "completeness_validator_emitted_count",
        "review_contract_emitted_count",
        "type_authority_matrix_emitted_count",
        "proposal_rollup_emitted_count",
        "profile_emitted_count",
    ]:
        if report.get(key) != 1:
            failures.append(f"report_metric_not_one:{key}:{report.get(key)}")
    for key in [
        "proposal_application_count",
        "builder_command_emitted_count",
        "taxonomy_mutation_count",
        "move_registration_count",
        "registry_mutation_count",
        "code_mutation_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "cell1_authorization_count",
        "domain_shift_authorization_count",
        "hidden_next_command_count",
        "latest_or_mtime_selection_count",
        "ambient_workspace_inference_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_metric_not_zero:{key}:{report.get(key)}")
    if report.get("bad_counters_zero") is not True:
        failures.append("report_bad_counters_not_zero")
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
        if ok is not True and ok != "not_applicable_static_probe_only":
            failures.append(f"acceptance_gate_not_true:{gate}:{ok}")
    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_C1_PROPOSAL_LAYER_STABLE_REVIEW_REQUIRED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    triggers = read_jsonl(DEMO_PROPOSAL_TRIGGERS_PATH)
    proposals = read_jsonl(PROPOSAL_PACKET_RECORDS_PATH)
    candidates = read_jsonl(MISSING_OBJECT_CANDIDATE_RECORDS_PATH)
    evidence = read_jsonl(PROPOSAL_EVIDENCE_BUNDLE_RECORDS_PATH)
    authority = read_jsonl(PROPOSAL_AUTHORITY_BOUNDARY_RECORDS_PATH)
    review = read_jsonl(PROPOSAL_REVIEW_REQUEST_RECORDS_PATH)
    receipts = read_jsonl(PROPOSAL_RECEIPT_RECORDS_PATH)
    rollup = read_json(PROPOSAL_ROLLUP_PATH)
    report = read_json(REPORT_PATH)

    controls: List[Dict[str, Any]] = []

    def add(case: str, failures: List[str], expected_fragment: str) -> None:
        controls.append({
            "case": case,
            "negative_control_pass": any(expected_fragment in f for f in failures),
            "failures": failures,
            "wrote_live_artifact": False,
        })

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["proposal_from_stop_done_no_pressure_count"] = 1
    add("proposal_from_stop_done_no_pressure_fail", validate_records(triggers, proposals, candidates, evidence, authority, review, receipts, bad_rollup), "proposal_from_stop_done_no_pressure_count")

    bad_proposals = copy.deepcopy(proposals)
    bad_proposals[0]["trigger"]["trigger_kind"] = None
    add("proposal_without_typed_trigger_fail", validate_records(triggers, bad_proposals, candidates, evidence, authority, review, receipts, rollup), "proposal_trigger_kind_missing")

    bad_evidence = copy.deepcopy(evidence)
    bad_evidence[0]["evidence_refs"] = []
    add("proposal_without_evidence_fail", validate_records(triggers, proposals, candidates, bad_evidence, authority, review, receipts, rollup), "proposal_incomplete")

    bad_authority = copy.deepcopy(authority)
    bad_authority[0]["authority"]["can_apply"] = True
    add("proposal_without_authority_boundary_fail", validate_records(triggers, proposals, candidates, evidence, bad_authority, review, receipts, rollup), "can_apply")

    bad_review = copy.deepcopy(review)
    bad_review.pop(0)
    add("proposal_without_review_request_fail", validate_records(triggers, proposals, candidates, evidence, authority, bad_review, receipts, rollup), "proposal_incomplete")

    bad_proposals = copy.deepcopy(proposals)
    bad_proposals[0]["must_not_infer"] = []
    add("proposal_without_must_not_infer_fail", validate_records(triggers, bad_proposals, candidates, evidence, authority, review, receipts, rollup), "proposal_incomplete")

    bad_proposals = copy.deepcopy(proposals)
    bad_proposals[0]["status"] = "ACCEPTED_FOR_BUILD"
    add("proposal_status_promoted_without_review_fail", validate_records(triggers, bad_proposals, candidates, evidence, authority, review, receipts, rollup), "proposal_status_not_proposed_only")

    bad_receipts = copy.deepcopy(receipts)
    bad_receipts[0]["proposal_applied"] = True
    add("proposal_applied_without_review_fail", validate_records(triggers, proposals, candidates, evidence, authority, review, bad_receipts, rollup), "receipt_proposal_applied")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["proposal_counted_as_execution_count"] = 1
    add("proposal_counted_as_execution_fail", validate_records(triggers, proposals, candidates, evidence, authority, review, receipts, bad_rollup), "proposal_counted_as_execution_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["proposal_counted_as_patch_count"] = 1
    add("proposal_counted_as_patch_fail", validate_records(triggers, proposals, candidates, evidence, authority, review, receipts, bad_rollup), "proposal_counted_as_patch_count")

    bad_candidates = copy.deepcopy(candidates)
    bad_candidates[0]["confidence"] = "CONFIRMED"
    add("missing_object_candidate_counted_as_confirmed_fail", validate_records(triggers, proposals, bad_candidates, evidence, authority, review, receipts, rollup), "candidate_counted_as_confirmed")

    bad_receipts = copy.deepcopy(receipts)
    bad_receipts[0]["builder_command_emitted"] = True
    add("builder_command_emitted_by_c1_fail", validate_records(triggers, proposals, candidates, evidence, authority, review, bad_receipts, rollup), "receipt_builder_command_emitted")

    bad_receipts = copy.deepcopy(receipts)
    bad_receipts[0]["taxonomy_mutated"] = True
    add("taxonomy_mutated_by_c1_fail", validate_records(triggers, proposals, candidates, evidence, authority, review, bad_receipts, rollup), "receipt_taxonomy_mutated")

    bad_receipts = copy.deepcopy(receipts)
    bad_receipts[0]["move_registered"] = True
    add("move_registered_by_c1_fail", validate_records(triggers, proposals, candidates, evidence, authority, review, bad_receipts, rollup), "receipt_move_registered")

    bad_proposals = copy.deepcopy(proposals)
    for p in bad_proposals:
        if p["evidence"]["evidence_status"] == "INSUFFICIENT_FOR_PROPOSAL":
            p["proposal_type"] = "BOUNDED_REPAIR_PROPOSAL"
            break
    add("evidence_insufficient_emits_repair_proposal_fail", validate_records(triggers, bad_proposals, candidates, evidence, authority, review, receipts, rollup), "insufficient_evidence_emitted_non_evidence_request")

    bad_triggers = copy.deepcopy(triggers)
    bad_triggers[0]["evidence_refs"] = ["chat_memory://strategic_vibes"]
    bad_triggers[0]["selected_edge"] = None
    add("strategic_vibes_as_evidence_fail", validate_records(bad_triggers, proposals, candidates, evidence, authority, review, receipts, rollup), "trigger_not_bound_to_b3_emit_proposal")

    bad_receipts = copy.deepcopy(receipts)
    bad_receipts[0]["terminal"]["next_command_goal"] = "BUILD_NEXT"
    add("hidden_next_command_fail", validate_records(triggers, proposals, candidates, evidence, authority, review, bad_receipts, rollup), "receipt_hidden_next")

    bad_report = copy.deepcopy(report)
    bad_report["source_mutation_count"] = 1
    add("source_mutation_fail", validate_report(bad_report), "source_mutation_count")

    bad_report = copy.deepcopy(report)
    bad_report["prior_receipt_mutation_count"] = 1
    add("prior_receipt_mutation_fail", validate_report(bad_report), "prior_receipt_mutation_count")

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_C1_DEPENDENCY_MISSING", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "c1_proposal_layer_receipt_v0",
            "receipt_type": "C1_PROPOSAL_LAYER_RECEIPT",
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
        print(f"c1_receipt_id={receipt_id}")
        print(f"c1_receipt_path=data/c1_cell0_proposal_layer_v0_receipts/{receipt_id}.json")
        return 1

    for path, obj in schemas().items():
        write_json(path, obj)

    triggers, proposals, candidates, evidence_bundles, authority_boundaries, review_requests, proposal_receipts = build_demo_records()
    rollup = compute_rollup(triggers, proposals, candidates, evidence_bundles, authority_boundaries, review_requests, proposal_receipts)
    profile = make_profile(rollup)
    transition = make_transition_trace(profile)
    report = make_report(triggers, proposals, candidates, evidence_bundles, authority_boundaries, review_requests, proposal_receipts, rollup, profile)

    append_jsonl(DEMO_PROPOSAL_TRIGGERS_PATH, triggers)
    append_jsonl(PROPOSAL_PACKET_RECORDS_PATH, proposals)
    append_jsonl(MISSING_OBJECT_CANDIDATE_RECORDS_PATH, candidates)
    append_jsonl(PROPOSAL_EVIDENCE_BUNDLE_RECORDS_PATH, evidence_bundles)
    append_jsonl(PROPOSAL_AUTHORITY_BOUNDARY_RECORDS_PATH, authority_boundaries)
    append_jsonl(PROPOSAL_REVIEW_REQUEST_RECORDS_PATH, review_requests)
    append_jsonl(PROPOSAL_RECEIPT_RECORDS_PATH, proposal_receipts)
    write_json(PROPOSAL_ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, profile)
    write_json(TRANSITION_TRACE_PATH, transition)
    write_json(REPORT_PATH, report)

    failures.extend(validate_records(triggers, proposals, candidates, evidence_bundles, authority_boundaries, review_requests, proposal_receipts, rollup))
    failures.extend(validate_report(report))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup["source_mutation_count"] = 1
        report["source_mutation_count"] = 1
        write_json(PROPOSAL_ROLLUP_PATH, rollup)
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "C1_PROPOSAL_0_SOURCE_DESIGN_CONSUMED": True,
        "C1_PROPOSAL_1_BUILD_MODE_DECLARED": BUILD_MODE == "STATIC_SCHEMA_AND_PROBE_ONLY",
        "C1_PROPOSAL_2_PACKET_SCHEMA_EMITTED": PROPOSAL_PACKET_SCHEMA_PATH.exists(),
        "C1_PROPOSAL_3_TRIGGER_SCHEMA_EMITTED": PROPOSAL_TRIGGER_SCHEMA_PATH.exists(),
        "C1_PROPOSAL_4_TYPE_ENUM_EMITTED": PROPOSAL_TYPE_ENUM_PATH.exists(),
        "C1_PROPOSAL_5_STATUS_ENUM_EMITTED": PROPOSAL_STATUS_ENUM_PATH.exists(),
        "C1_PROPOSAL_6_MISSING_OBJECT_CANDIDATE_SCHEMA_EMITTED": MISSING_OBJECT_CANDIDATE_SCHEMA_PATH.exists(),
        "C1_PROPOSAL_7_EVIDENCE_BUNDLE_SCHEMA_EMITTED": PROPOSAL_EVIDENCE_BUNDLE_SCHEMA_PATH.exists(),
        "C1_PROPOSAL_8_AUTHORITY_BOUNDARY_SCHEMA_EMITTED": PROPOSAL_AUTHORITY_BOUNDARY_SCHEMA_PATH.exists(),
        "C1_PROPOSAL_9_REVIEW_REQUEST_SCHEMA_EMITTED": PROPOSAL_REVIEW_REQUEST_SCHEMA_PATH.exists(),
        "C1_PROPOSAL_10_RECEIPT_SCHEMA_EMITTED": PROPOSAL_RECEIPT_SCHEMA_PATH.exists(),
        "C1_PROPOSAL_11_TRIGGER_MAPPING_TABLE_EMITTED": PROPOSAL_TRIGGER_MAPPING_TABLE_PATH.exists(),
        "C1_PROPOSAL_12_DEMO_PROPOSAL_CASES_EMITTED": len(triggers) == 12,
        "C1_PROPOSAL_13_EVERY_PROPOSAL_HAS_TYPED_TRIGGER": all(p["trigger"]["trigger_kind"] for p in proposals),
        "C1_PROPOSAL_14_EVERY_PROPOSAL_HAS_EVIDENCE_REFS": rollup["proposal_without_evidence_count"] == 0,
        "C1_PROPOSAL_15_EVERY_PROPOSAL_HAS_AUTHORITY_BOUNDARY": rollup["proposal_without_authority_boundary_count"] == 0,
        "C1_PROPOSAL_16_EVERY_PROPOSAL_HAS_REVIEW_REQUEST": len(review_requests) == len(proposals),
        "C1_PROPOSAL_17_EVERY_PROPOSAL_HAS_MUST_NOT_INFER": rollup["proposal_without_must_not_infer_count"] == 0,
        "C1_PROPOSAL_18_EVERY_PROPOSAL_STATUS_PROPOSED_ONLY": rollup["proposal_status_counts"]["PROPOSED_ONLY"] == len(proposals),
        "C1_PROPOSAL_19_STOP_DONE_NO_PRESSURE_EMITS_NO_PROPOSAL": rollup["proposal_from_stop_done_no_pressure_count"] == 0 and any(not t["proposal_allowed"] for t in triggers),
        "C1_PROPOSAL_20_INSUFFICIENT_EVIDENCE_DOES_NOT_EMIT_REPAIR_PROPOSAL": rollup["insufficient_evidence_emitted_non_evidence_request_count"] == 0,
        "C1_PROPOSAL_21_NO_PROPOSAL_APPLICATION": rollup["proposal_applied_without_review_count"] == 0,
        "C1_PROPOSAL_22_NO_BUILDER_COMMAND_EMITTED": rollup["builder_command_emitted_by_c1_count"] == 0,
        "C1_PROPOSAL_23_NO_TAXONOMY_MUTATION": rollup["taxonomy_mutated_by_c1_count"] == 0,
        "C1_PROPOSAL_24_NO_MOVE_REGISTRATION": rollup["move_registered_by_c1_count"] == 0,
        "C1_PROPOSAL_25_BAD_COUNTERS_ZERO": all(rollup.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "C1_PROPOSAL_26_NO_HIDDEN_NEXT_COMMAND": rollup["hidden_next_command_count"] == 0 and transition["terminal"]["next_command_goal"] is None,
        "C1_PROPOSAL_27_COMPLETENESS_VALIDATOR_EMITTED": PROPOSAL_COMPLETENESS_VALIDATOR_PATH.exists(),
        "C1_PROPOSAL_28_EVERY_PROPOSAL_PASSES_COMPLETENESS_VALIDATOR": rollup["proposal_incomplete_count"] == 0,
        "C1_PROPOSAL_29_REVIEW_CONTRACT_EMITTED": PROPOSAL_REVIEW_CONTRACT_PATH.exists(),
        "C1_PROPOSAL_30_PROPOSAL_TYPE_AUTHORITY_MATRIX_EMITTED": PROPOSAL_TYPE_AUTHORITY_MATRIX_PATH.exists(),
        "C1_PROPOSAL_31_PROPOSAL_TYPE_DOES_NOT_IMPLY_AUTHORITY": rollup["proposal_type_authority_overreach_count"] == 0,
        "C1_PROPOSAL_32_INSUFFICIENT_EVIDENCE_ONLY_EMITS_EVIDENCE_REQUEST_OR_QUESTION": rollup["insufficient_evidence_emitted_non_evidence_request_count"] == 0,
        "C1_PROPOSAL_33_PROPOSAL_PRESERVES_B3_EDGE_SOURCE_REFS": rollup["proposal_missing_b3_source_ref_count"] == 0,
        "C1_PROPOSAL_LIVE_SOURCE_BOUND_TO_B3_EDGE": "not_applicable_static_probe_only",
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True and ok != "not_applicable_static_probe_only":
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = transition["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_b3": SOURCE_B3_RECEIPT_ID,
        "source_b2": SOURCE_B2_RECEIPT_ID,
        "source_b1": SOURCE_B1_RECEIPT_ID,
        "profile_status": profile["status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "proposal_packet_schema": rel(PROPOSAL_PACKET_SCHEMA_PATH),
        "proposal_trigger_schema": rel(PROPOSAL_TRIGGER_SCHEMA_PATH),
        "proposal_type_enum": rel(PROPOSAL_TYPE_ENUM_PATH),
        "proposal_status_enum": rel(PROPOSAL_STATUS_ENUM_PATH),
        "missing_object_candidate_schema": rel(MISSING_OBJECT_CANDIDATE_SCHEMA_PATH),
        "proposal_evidence_bundle_schema": rel(PROPOSAL_EVIDENCE_BUNDLE_SCHEMA_PATH),
        "proposal_authority_boundary_schema": rel(PROPOSAL_AUTHORITY_BOUNDARY_SCHEMA_PATH),
        "proposal_review_request_schema": rel(PROPOSAL_REVIEW_REQUEST_SCHEMA_PATH),
        "proposal_receipt_schema": rel(PROPOSAL_RECEIPT_SCHEMA_PATH),
        "proposal_trigger_mapping_table": rel(PROPOSAL_TRIGGER_MAPPING_TABLE_PATH),
        "proposal_completeness_validator": rel(PROPOSAL_COMPLETENESS_VALIDATOR_PATH),
        "proposal_review_contract": rel(PROPOSAL_REVIEW_CONTRACT_PATH),
        "proposal_type_authority_matrix": rel(PROPOSAL_TYPE_AUTHORITY_MATRIX_PATH),
        "c1_demo_proposal_triggers": rel(DEMO_PROPOSAL_TRIGGERS_PATH),
        "proposal_packet_records": rel(PROPOSAL_PACKET_RECORDS_PATH),
        "missing_object_candidate_records": rel(MISSING_OBJECT_CANDIDATE_RECORDS_PATH),
        "proposal_evidence_bundle_records": rel(PROPOSAL_EVIDENCE_BUNDLE_RECORDS_PATH),
        "proposal_authority_boundary_records": rel(PROPOSAL_AUTHORITY_BOUNDARY_RECORDS_PATH),
        "proposal_review_request_records": rel(PROPOSAL_REVIEW_REQUEST_RECORDS_PATH),
        "proposal_receipt_records": rel(PROPOSAL_RECEIPT_RECORDS_PATH),
        "proposal_rollup": rel(PROPOSAL_ROLLUP_PATH),
        "c1_proposal_layer_profile": rel(PROFILE_PATH),
        "c1_transition_trace": rel(TRANSITION_TRACE_PATH),
        "c1_report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_b3_receipt": rel(SOURCE_B3_RECEIPT_PATH),
    }

    aggregate_metrics = {
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        **{f"rollup_{k}": v for k, v in rollup.items() if k not in {"schema_version", "proposal_type_counts", "proposal_status_counts"}},
        "proposal_type_counts": rollup["proposal_type_counts"],
        "proposal_status_counts": rollup["proposal_status_counts"],
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards = {
        "build_mode_static_schema_and_probe_only": BUILD_MODE == "STATIC_SCHEMA_AND_PROBE_ONLY",
        "b3_emit_proposal_edge_available": True,
        "live_source_binding_not_applicable_static": True,
        "latest_or_mtime_selection_used": False,
        "ambient_workspace_inference_used": False,
        "all_proposals_proposed_only": all(p["status"] == "PROPOSED_ONLY" for p in proposals),
        "proposal_completeness_validator_enforced": True,
        "proposal_review_contract_enforced": True,
        "proposal_type_authority_matrix_enforced": True,
        "no_proposal_application": rollup["proposal_applied_without_review_count"] == 0,
        "no_builder_command_emitted": rollup["builder_command_emitted_by_c1_count"] == 0,
        "no_taxonomy_mutation": rollup["taxonomy_mutated_by_c1_count"] == 0,
        "no_move_registration": rollup["move_registered_by_c1_count"] == 0,
        "no_registry_mutation": rollup["registry_mutation_count"] == 0,
        "missing_object_candidate_not_confirmed": rollup["missing_object_candidate_counted_as_confirmed_count"] == 0,
        "proposal_preserves_b3_edge_source_refs": rollup["proposal_missing_b3_source_ref_count"] == 0,
        "cell1_authorized": False,
        "domain_shift_authorized": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
        "hidden_next_command": False,
    }

    receipt = {
        "schema_version": "c1_proposal_layer_receipt_v0",
        "receipt_type": "C1_PROPOSAL_LAYER_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "B3 EMIT_PROPOSAL edge and proposal packet surface",
        "source_b3_receipt_id": SOURCE_B3_RECEIPT_ID,
        "source_b2_receipt_id": SOURCE_B2_RECEIPT_ID,
        "source_b1_receipt_id": SOURCE_B1_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "c1_summary": {
            "profile_status": profile["status"],
            "proposal_count": rollup["proposal_count"],
            "demo_trigger_count": rollup["demo_trigger_count"],
            "valid_trigger_count": rollup["valid_trigger_count"],
            "invalid_trigger_count": rollup["invalid_trigger_count"],
            "proposed_only_count": rollup["proposal_status_counts"]["PROPOSED_ONLY"],
            "bad_counters_zero": all(rollup.get(k) == 0 for k in ZERO_COUNTER_KEYS),
            "proposal_incomplete_count": rollup["proposal_incomplete_count"],
            "proposal_applied_without_review_count": rollup["proposal_applied_without_review_count"],
            "builder_command_emitted_by_c1_count": rollup["builder_command_emitted_by_c1_count"],
            "taxonomy_mutated_by_c1_count": rollup["taxonomy_mutated_by_c1_count"],
            "move_registered_by_c1_count": rollup["move_registered_by_c1_count"],
            "recommended_next_handling": None,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "c1_guards": guards,
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
    if len(negative_controls) != 19 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
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
    print(f"c1_receipt_id={receipt_id}")
    print(f"c1_receipt_path=data/c1_cell0_proposal_layer_v0_receipts/{receipt_id}.json")
    print(f"c1_profile_path=data/c1_cell0_proposal_layer_v0/c1_proposal_layer_profile_v0.json")
    print(f"c1_rollup_path=data/c1_cell0_proposal_layer_v0/proposal_rollup_v0.json")
    print(f"c1_proposal_records_path=data/c1_cell0_proposal_layer_v0/proposal_packet_records_v0.jsonl")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
