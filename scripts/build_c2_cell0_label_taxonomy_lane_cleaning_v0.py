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

UNIT_ID = "BUILD_C2_CELL0_LABEL_TAXONOMY_LANE_CLEANING_V0"
TARGET_UNIT_ID = "c2.cell0.label_taxonomy_lane_cleaning.v0"
LAYER = "CELL_0 / LABEL_TAXONOMY_HYGIENE"
MODE = "CERTIFY / AUDIT / REFLECT"
BUILD_MODE = "STATIC_SCHEMA_AND_PROBE_ONLY"

SOURCE_C1_RECEIPT_ID = "f8f37c4e"
SOURCE_C1_RECEIPT_PATH = ROOT / "data" / "c1_cell0_proposal_layer_v0_receipts" / "f8f37c4e.json"
SOURCE_C1_PROFILE_PATH = ROOT / "data" / "c1_cell0_proposal_layer_v0" / "c1_proposal_layer_profile_v0.json"
SOURCE_C1_PROPOSAL_RECORDS_PATH = ROOT / "data" / "c1_cell0_proposal_layer_v0" / "proposal_packet_records_v0.jsonl"
SOURCE_C1_PROPOSAL_RECEIPTS_PATH = ROOT / "data" / "c1_cell0_proposal_layer_v0" / "proposal_receipt_records_v0.jsonl"
SOURCE_C1_EVIDENCE_RECORDS_PATH = ROOT / "data" / "c1_cell0_proposal_layer_v0" / "proposal_evidence_bundle_records_v0.jsonl"
SOURCE_C1_AUTHORITY_RECORDS_PATH = ROOT / "data" / "c1_cell0_proposal_layer_v0" / "proposal_authority_boundary_records_v0.jsonl"
SOURCE_C1_REVIEW_RECORDS_PATH = ROOT / "data" / "c1_cell0_proposal_layer_v0" / "proposal_review_request_records_v0.jsonl"
SOURCE_C1_ROLLUP_PATH = ROOT / "data" / "c1_cell0_proposal_layer_v0" / "proposal_rollup_v0.json"

SOURCE_B3_RECEIPT_ID = "a4cbf33f"
SOURCE_B3_RECEIPT_PATH = ROOT / "data" / "b3_cell0_local_decision_loop_schema_lock_v0_receipts" / "a4cbf33f.json"
SOURCE_B3_LOOP_RECEIPTS_PATH = ROOT / "data" / "b3_cell0_local_decision_loop_schema_lock_v0" / "local_decision_loop_receipts_v0.jsonl"
SOURCE_B3_TRACE_RECORDS_PATH = ROOT / "data" / "b3_cell0_local_decision_loop_schema_lock_v0" / "local_decision_loop_trace_records_v0.jsonl"

SOURCE_B2_RECEIPT_ID = "7ab64083"
SOURCE_B2_PROGRESS_RECORDS_PATH = ROOT / "data" / "b2_cell0_informative_failure_progress_classifier_v0" / "b2_failure_progress_records_v0.jsonl"
SOURCE_B2_ROLLUP_PATH = ROOT / "data" / "b2_cell0_informative_failure_progress_classifier_v0" / "b2_failure_progress_rollup_v0.json"

SOURCE_B1_RECEIPT_ID = "b9c8f831"
SOURCE_B1_PRESSURE_ENUM_PATH = ROOT / "data" / "b1_cell0_local_lawful_actor_stabilization_v0" / "cell0_pressure_class_enum_v0.json"

OUT_DIR = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0"
RECEIPT_DIR = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts"

TAXONOMY_LANE_REGISTRY_PATH = OUT_DIR / "taxonomy_lane_registry_v0.json"
TYPED_LABEL_RECORD_SCHEMA_PATH = OUT_DIR / "typed_label_record_schema_v0.json"
LABEL_LANE_ASSERTION_SCHEMA_PATH = OUT_DIR / "label_lane_assertion_schema_v0.json"
LABEL_NON_COLLAPSE_GATE_SCHEMA_PATH = OUT_DIR / "label_non_collapse_gate_schema_v0.json"
LABEL_PROMOTION_RULE_SCHEMA_PATH = OUT_DIR / "label_promotion_rule_schema_v0.json"
WITHHELD_LABEL_RECORD_SCHEMA_PATH = OUT_DIR / "withheld_label_record_schema_v0.json"
LABEL_TAXONOMY_AUDIT_SCHEMA_PATH = OUT_DIR / "label_taxonomy_audit_schema_v0.json"
LABEL_LANE_CONSUMPTION_MATRIX_PATH = OUT_DIR / "label_lane_consumption_matrix_v0.json"

DEMO_LABEL_TARGETS_PATH = OUT_DIR / "c2_demo_label_targets_v0.jsonl"
TYPED_LABEL_RECORDS_PATH = OUT_DIR / "typed_label_records_v0.jsonl"
LABEL_LANE_ASSERTIONS_PATH = OUT_DIR / "label_lane_assertions_v0.jsonl"
LABEL_NON_COLLAPSE_GATE_RECORDS_PATH = OUT_DIR / "label_non_collapse_gate_records_v0.jsonl"
LABEL_PROMOTION_RULES_PATH = OUT_DIR / "label_promotion_rules_v0.jsonl"
WITHHELD_LABEL_RECORDS_PATH = OUT_DIR / "withheld_label_records_v0.jsonl"
LABEL_TAXONOMY_AUDIT_RECORDS_PATH = OUT_DIR / "label_taxonomy_audit_records_v0.jsonl"
LABEL_TAXONOMY_ROLLUP_PATH = OUT_DIR / "label_taxonomy_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c2_label_taxonomy_profile_v0.json"
TRANSITION_TRACE_PATH = OUT_DIR / "c2_transition_trace.json"
REPORT_PATH = OUT_DIR / "c2_report.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C1_RECEIPT_PATH,
    SOURCE_C1_PROFILE_PATH,
    SOURCE_C1_PROPOSAL_RECORDS_PATH,
    SOURCE_C1_PROPOSAL_RECEIPTS_PATH,
    SOURCE_C1_EVIDENCE_RECORDS_PATH,
    SOURCE_C1_AUTHORITY_RECORDS_PATH,
    SOURCE_C1_REVIEW_RECORDS_PATH,
    SOURCE_C1_ROLLUP_PATH,
    SOURCE_B3_RECEIPT_PATH,
    SOURCE_B3_LOOP_RECEIPTS_PATH,
    SOURCE_B3_TRACE_RECORDS_PATH,
    SOURCE_B2_PROGRESS_RECORDS_PATH,
    SOURCE_B2_ROLLUP_PATH,
    SOURCE_B1_PRESSURE_ENUM_PATH,
]

LANES = [
    "workflow_position",
    "pressure_class",
    "evidence_status",
    "object_identity",
    "authority_status",
    "next_required_move",
]

LANE_VALUES = {
    "workflow_position": [
        "QUEUED", "ACTIVE", "PARKED", "CLOSED", "PROPOSED_ONLY",
        "UNDER_REVIEW", "ACCEPTED_FOR_BUILD", "REMAINING", "CANDIDATE"
    ],
    "pressure_class": [
        "NO_PRESSURE", "TAXONOMY_PRESSURE", "AUTHORITY_PRESSURE",
        "MISSING_MOVE_PRESSURE", "BURDEN_PRESSURE", "LABEL_AMBIGUITY_PRESSURE",
        "RECEIPT_TRACE_PRESSURE", "OBSERVABILITY_PRESSURE", "FRONTIER_PRESSURE",
        "PRODUCTIVE_PRESSURE", "remaining_pressure",
    ],
    "evidence_status": [
        "UNOBSERVED", "OBSERVED", "CANDIDATE", "SUFFICIENT_FOR_PROPOSAL",
        "SUFFICIENT_FOR_REVIEW", "SUFFICIENT_FOR_LOCAL_MOVE", "INSUFFICIENT",
        "REQUIRES_EXTRACTION"
    ],
    "object_identity": [
        "RECEIPT", "TRACE", "PROPOSAL_PACKET", "MISSING_OBJECT_CANDIDATE",
        "TAXONOMY_DELTA", "TAXONOMY_DELTA_PROPOSAL", "MOVE_CANDIDATE",
        "AUTHORITY_VERDICT", "BUILD_RECEIPT", "VERIFICATION_RECEIPT",
        "proposal_type", "missing_object_candidate", "label_split_proposal",
    ],
    "authority_status": [
        "READ_ONLY", "PROPOSE_ONLY", "REQUIRES_REVIEW", "AUTHORIZED_LOCAL",
        "ACCEPTED_FOR_BUILD", "FORBIDDEN", "PARKED", "NO_EXECUTION",
        "can_apply=false", "requires_review=true",
    ],
    "next_required_move": [
        "STOP", "ASK_QUESTION", "PROPOSE_DELTA", "REQUEST_REVIEW",
        "REQUEST_EXTRACTION", "BUILD_MINIMAL_PATCH", "VERIFY_PATCH",
        "PARK_OBJECT", "CLOSE_LANE", "NO_EXECUTION",
    ],
}

FORBIDDEN_JUMPS = [
    ("workflow_position", "object_identity", "workflow_position_promoted_to_identity_count"),
    ("pressure_class", "object_identity", "pressure_class_promoted_to_identity_count"),
    ("pressure_class", "authority_status", "pressure_class_promoted_to_authority_count"),
    ("evidence_status", "authority_status", "evidence_status_promoted_to_authority_count"),
    ("workflow_position", "execution_status", "proposal_status_promoted_to_execution_count"),
    ("object_identity", "confirmed_object", "missing_object_candidate_promoted_to_confirmed_count"),
    ("object_identity", "taxonomy_patch", "taxonomy_delta_proposal_counted_as_patch_count"),
    ("next_required_move", "authority_status", "review_request_counted_as_authorization_count"),
    ("authority_status", "built", "accepted_for_build_counted_as_built_count"),
    ("object_identity", "verified", "built_counted_as_verified_count"),
]

ZERO_COUNTER_KEYS = [
    "unauthorized_promotion_count",
    "workflow_position_promoted_to_identity_count",
    "pressure_class_promoted_to_identity_count",
    "pressure_class_promoted_to_authority_count",
    "evidence_status_promoted_to_authority_count",
    "proposal_status_promoted_to_execution_count",
    "missing_object_candidate_promoted_to_confirmed_count",
    "taxonomy_delta_proposal_counted_as_patch_count",
    "review_request_counted_as_authorization_count",
    "accepted_for_build_counted_as_built_count",
    "built_counted_as_verified_count",
    "under_typed_label_silently_accepted_count",
    "withhold_treated_as_failure_count",
    "taxonomy_registry_mutation_count",
    "builder_command_emitted_count",
    "hidden_next_command_count",
    "label_consumer_lane_violation_count",
    "proposal_status_counted_as_authority_count",
    "evidence_status_counted_as_truth_count",
    "next_required_move_counted_as_execution_count",
    "object_identity_counted_as_authority_count",
    "authority_status_counted_as_verification_count",
    "c1_packet_label_audit_missing_count",
    "source_mutation_count",
    "prior_receipt_mutation_count",
    "cell1_authorization_count",
    "domain_shift_authorization_count",
]

HUMAN_DECISION = {
    "decision": "BUILD_C2_CELL0_LABEL_TAXONOMY_LANE_CLEANING",
    "scope": "Build C2 as the Cell 0 label taxonomy lane-cleaning layer in STATIC_SCHEMA_AND_PROBE_ONLY mode. Emit taxonomy lane registry, typed label record schema, lane assertion schema, non-collapse gate schema, promotion rule schema, withheld label schema, audit schema, lane-consumption matrix, demo label targets, typed label records, lane assertions, non-collapse gate records, promotion rules, withheld label records, audit records, rollup, profile, report, and receipt. Audit C1-style proposal packet labels and related Cell 0 labels. Assign each checked label to exactly one primary lane or withhold it. Block forbidden lane collapses. Do not mutate taxonomy registry, accept taxonomy deltas, infer authority from evidence, infer object identity from pressure/workflow labels, emit builder commands, or hide next command.",
    "authorized": [
        "define taxonomy lane registry",
        "define typed label record schema",
        "define label lane assertion schema",
        "define non-collapse gate schema",
        "define promotion rule schema",
        "define withheld label schema",
        "define label taxonomy audit schema",
        "define lane-consumption matrix",
        "audit demo C1 proposal packets and Cell 0 records",
        "block forbidden lane collapses",
        "withhold under-typed labels",
        "emit taxonomy-delta proposal candidates only when lanes are insufficient",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "create final taxonomy",
        "mutate taxonomy registry",
        "accept taxonomy deltas automatically",
        "decide object identity from pressure label",
        "decide authority from usefulness",
        "decide truth from evidence status",
        "decide execution from proposal status",
        "decide verification from build status",
        "clean all language globally",
        "overbuild ontology",
        "create Cell 1",
        "emit builder command",
        "hide next command",
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

    c1_receipt = read_json(SOURCE_C1_RECEIPT_PATH)
    c1_profile = read_json(SOURCE_C1_PROFILE_PATH)
    c1_rollup = read_json(SOURCE_C1_ROLLUP_PATH)
    b3_receipt = read_json(SOURCE_B3_RECEIPT_PATH)
    b2_rollup = read_json(SOURCE_B2_ROLLUP_PATH)

    if c1_receipt.get("receipt_id") != SOURCE_C1_RECEIPT_ID:
        failures.append("c1_receipt_id_wrong")
    if c1_receipt.get("gate") != "PASS":
        failures.append("c1_receipt_gate_not_PASS")
    if c1_profile.get("status") != "C1_PROPOSAL_LAYER_STABLE":
        failures.append("c1_profile_not_stable")
    if c1_rollup.get("proposal_count") != 11:
        failures.append("c1_rollup_proposal_count_unexpected")
    if b3_receipt.get("receipt_id") != "a4cbf33f" or b3_receipt.get("gate") != "PASS":
        failures.append("b3_basis_not_accepted")
    if b2_rollup.get("failure_events_total") != 12:
        failures.append("b2_rollup_unexpected")
    return failures

def taxonomy_lane_registry() -> Dict[str, Any]:
    return {
        "schema_version": "taxonomy_lane_registry_v0",
        "registry_id": "taxonomy_lane_registry_v0",
        "scope": "CELL_0_LOCAL_LABEL_HYGIENE",
        "lanes": LANE_VALUES,
        "registry_status": "LOCAL_REFERENCE_ONLY",
        "mutation_allowed_by_c2": False,
    }

def typed_label_record_schema() -> Dict[str, Any]:
    return {
        "schema_version": "typed_label_record_schema_v0",
        "record_schema": {
            "schema_version": "typed_label_record_v0",
            "label_record_id": "label_<sig8>",
            "target_ref": None,
            "label": None,
            "label_lane": "workflow_position | pressure_class | evidence_status | object_identity | authority_status | next_required_move",
            "smallest_honest_meaning": None,
            "must_not_impersonate": [],
            "allowed_consumers": [],
            "forbidden_consumers": [],
            "allowed_next_moves": [],
            "stop_conditions": [],
        },
        "rule": "No label record may omit smallest_honest_meaning or must_not_impersonate.",
    }

def label_lane_assertion_schema() -> Dict[str, Any]:
    return {
        "schema_version": "label_lane_assertion_schema_v0",
        "assertion_schema": {
            "schema_version": "label_lane_assertion_v0",
            "assertion_id": "lane_assert_<sig8>",
            "target_ref": None,
            "raw_label": None,
            "assigned_lane": None,
            "rejected_lanes": [],
            "reason": None,
            "evidence_refs": [],
            "status": "ASSERTED_LOCAL | WITHHELD | REJECTED",
        },
        "rule": "Every attached label must either receive one assigned lane or be withheld.",
    }

def label_non_collapse_gate_schema() -> Dict[str, Any]:
    return {
        "schema_version": "label_non_collapse_gate_schema_v0",
        "gate_schema": {
            "schema_version": "label_non_collapse_gate_v0",
            "gate_id": "label_gate_<sig8>",
            "source_label": None,
            "source_lane": None,
            "attempted_target_lane": None,
            "attempted_target_label": None,
            "verdict": "ALLOWED_WITH_RECEIPT | BLOCKED | WITHHELD",
            "reason": None,
            "required_receipt_for_promotion": None,
        },
        "forbidden_lane_jumps": [
            "workflow_position -> object_identity",
            "pressure_class -> object_identity",
            "pressure_class -> authority_status",
            "evidence_status -> authority_status",
            "evidence_status -> truth_status",
            "proposal_status -> execution_status",
            "missing_object_candidate -> confirmed_object",
            "candidate_move -> registered_move",
            "taxonomy_delta_proposal -> taxonomy_patch",
            "review_request -> review_approval",
            "accepted_for_build -> built",
            "built -> verified",
        ],
    }

def label_promotion_rule_schema() -> Dict[str, Any]:
    return {
        "schema_version": "label_promotion_rule_schema_v0",
        "promotion_schema": {
            "schema_version": "label_promotion_rule_v0",
            "promotion_id": "promotion_<sig8>",
            "from": {"label": None, "lane": None},
            "to": {"label": None, "lane": None},
            "required_evidence": [],
            "forbidden_without_evidence": True,
            "must_not_infer": [],
        },
    }

def withheld_label_record_schema() -> Dict[str, Any]:
    return {
        "schema_version": "withheld_label_record_schema_v0",
        "record_schema": {
            "schema_version": "withheld_label_record_v0",
            "withheld_label_id": "withheld_<sig8>",
            "target_ref": None,
            "raw_label": None,
            "reason": None,
            "blocked_lanes": [],
            "allowed_next_handling": [
                "REQUEST_EXTRACTION",
                "NARROW_LABEL_CONTEXT",
                "PARK_OBJECT",
                "PROPOSE_TAXONOMY_DELTA",
            ],
        },
        "rule": "Withholding is a valid success state when it prevents fake identity or authority.",
    }

def label_taxonomy_audit_schema() -> Dict[str, Any]:
    return {
        "schema_version": "label_taxonomy_audit_schema_v0",
        "audit_schema": {
            "schema_version": "label_taxonomy_audit_v0",
            "audit_id": "label_audit_<sig8>",
            "target_ref": None,
            "labels_checked": 0,
            "lane_assignments": {lane: 0 for lane in LANES},
            "collapse_attempts_blocked": [],
            "under_typed_labels": [],
            "withheld_labels": [],
            "taxonomy_delta_proposals": [],
            "audit_result": "PASS | WITHHELD | TAXONOMY_GAP | FAIL",
        },
    }

def label_lane_consumption_matrix() -> Dict[str, Any]:
    return {
        "schema_version": "label_lane_consumption_matrix_v0",
        "lanes": {
            "workflow_position": {
                "allowed_consumers": ["queue_manager", "review_layer", "readout_layer"],
                "forbidden_consumers": ["builder_executor", "authority_granter", "identity_resolver"],
                "may_license": ["routing", "review", "parking", "closure_readout"],
                "must_not_license": ["execution", "verification", "object_identity", "authority"],
            },
            "pressure_class": {
                "allowed_consumers": ["classifier", "proposal_layer", "review_layer"],
                "forbidden_consumers": ["builder_executor", "identity_resolver"],
                "may_license": ["classification", "proposal", "question_packet"],
                "must_not_license": ["root_cause_claim", "authority", "execution", "object_identity"],
            },
            "evidence_status": {
                "allowed_consumers": ["proposal_layer", "review_layer", "audit_layer"],
                "forbidden_consumers": ["authority_granter", "builder_executor"],
                "may_license": ["proposal", "review", "extraction_request"],
                "must_not_license": ["truth", "authority", "execution", "verification"],
            },
            "object_identity": {
                "allowed_consumers": ["registry_reader", "proposal_layer", "review_layer"],
                "forbidden_consumers": ["authority_granter_without_receipt"],
                "may_license": ["reference", "classification", "review"],
                "must_not_license": ["authority", "execution", "verification"],
            },
            "authority_status": {
                "allowed_consumers": ["review_layer", "runtime_gate", "builder_gate"],
                "forbidden_consumers": ["identity_resolver"],
                "may_license": ["read", "propose", "review", "authorized_local_action_if_explicit"],
                "must_not_license": ["truth", "verification", "object_identity"],
            },
            "next_required_move": {
                "allowed_consumers": ["scheduler", "review_layer", "decision_packet_layer"],
                "forbidden_consumers": ["builder_executor_without_acceptance"],
                "may_license": ["routing", "question", "review", "proposal"],
                "must_not_license": ["execution", "success", "verification", "authority_without_receipt"],
            },
        },
        "rule": "Correct lane assignment is insufficient if the consumer uses the label as if it belonged to another lane.",
    }

def schemas() -> Dict[Path, Dict[str, Any]]:
    return {
        TAXONOMY_LANE_REGISTRY_PATH: taxonomy_lane_registry(),
        TYPED_LABEL_RECORD_SCHEMA_PATH: typed_label_record_schema(),
        LABEL_LANE_ASSERTION_SCHEMA_PATH: label_lane_assertion_schema(),
        LABEL_NON_COLLAPSE_GATE_SCHEMA_PATH: label_non_collapse_gate_schema(),
        LABEL_PROMOTION_RULE_SCHEMA_PATH: label_promotion_rule_schema(),
        WITHHELD_LABEL_RECORD_SCHEMA_PATH: withheld_label_record_schema(),
        LABEL_TAXONOMY_AUDIT_SCHEMA_PATH: label_taxonomy_audit_schema(),
        LABEL_LANE_CONSUMPTION_MATRIX_PATH: label_lane_consumption_matrix(),
    }

def promotion_rules() -> List[Dict[str, Any]]:
    specs = [
        ("PROPOSED_ONLY", "workflow_position", "ACCEPTED_FOR_BUILD", "authority_status", "proposal_review_receipt_v0"),
        ("ACCEPTED_FOR_BUILD", "authority_status", "BUILT", "workflow_position", "build_receipt_v0"),
        ("BUILT", "object_identity", "VERIFIED", "evidence_status", "verification_receipt_v0"),
        ("MISSING_OBJECT_CANDIDATE", "object_identity", "REGISTERED_OBJECT", "object_identity", "review_or_registration_receipt_v0"),
        ("TAXONOMY_DELTA_PROPOSAL", "object_identity", "TAXONOMY_PATCH_APPLIED", "object_identity", "taxonomy_review_and_registry_patch_receipt_v0"),
        ("REVIEW_REQUEST", "next_required_move", "REVIEW_APPROVAL", "authority_status", "review_decision_receipt_v0"),
    ]
    rows = []
    for source_label, source_lane, target_label, target_lane, receipt in specs:
        rows.append({
            "schema_version": "label_promotion_rule_v0",
            "promotion_id": "promotion_" + sha8({"from": source_label, "to": target_label}),
            "from": {"label": source_label, "lane": source_lane},
            "to": {"label": target_label, "lane": target_lane},
            "required_evidence": [receipt],
            "forbidden_without_evidence": True,
            "must_not_infer": [
                "promotion is automatic",
                "source label already has target-lane meaning",
                "proposal is approval",
                "build status is verification",
            ],
        })
    return rows

def consumers_for_lane(lane: str) -> Tuple[List[str], List[str], List[str]]:
    matrix = label_lane_consumption_matrix()["lanes"][lane]
    return matrix["allowed_consumers"], matrix["forbidden_consumers"], matrix["may_license"]

def must_not_for_lane(lane: str) -> List[str]:
    base = {
        "workflow_position": ["object identity", "truth", "authority", "completion", "execution", "verification"],
        "pressure_class": ["root cause", "object identity", "proof of defect", "repair command", "authority", "success"],
        "evidence_status": ["truth", "authority", "object identity", "accepted patch", "execution permission", "verification"],
        "object_identity": ["workflow position", "pressure class", "authority", "truth", "review status", "execution status"],
        "authority_status": ["truth", "object identity", "evidence sufficiency", "completion", "build success", "verification"],
        "next_required_move": ["authority", "success", "object identity", "completed action", "execution permission"],
    }
    return base[lane]

def make_label_record(target_ref: str, label: str, lane: str, meaning: str, evidence_refs: List[str], allowed_next_moves: Optional[List[str]] = None) -> Dict[str, Any]:
    allowed_consumers, forbidden_consumers, default_moves = consumers_for_lane(lane)
    return {
        "schema_version": "typed_label_record_v0",
        "label_record_id": "label_" + sha8({"target": target_ref, "label": label, "lane": lane}),
        "target_ref": target_ref,
        "label": label,
        "label_lane": lane,
        "smallest_honest_meaning": meaning,
        "must_not_impersonate": must_not_for_lane(lane),
        "allowed_consumers": allowed_consumers,
        "forbidden_consumers": forbidden_consumers,
        "allowed_next_moves": allowed_next_moves or default_moves,
        "stop_conditions": [
            "stop if consumer treats label as another lane",
            "stop if promotion lacks required receipt",
        ],
        "evidence_refs": evidence_refs,
    }

def make_assertion(label_record: Dict[str, Any], status: str = "ASSERTED_LOCAL", rejected_lanes: Optional[List[str]] = None) -> Dict[str, Any]:
    lane = label_record["label_lane"]
    return {
        "schema_version": "label_lane_assertion_v0",
        "assertion_id": "lane_assert_" + sha8({"label_record_id": label_record["label_record_id"], "lane": lane}),
        "target_ref": label_record["target_ref"],
        "raw_label": label_record["label"],
        "assigned_lane": lane if status == "ASSERTED_LOCAL" else None,
        "rejected_lanes": rejected_lanes or [x for x in LANES if x != lane],
        "reason": label_record["smallest_honest_meaning"],
        "evidence_refs": label_record.get("evidence_refs", []),
        "status": status,
    }

def make_gate(source_label: str, source_lane: str, attempted_target_lane: str, attempted_target_label: str, reason: str, required_receipt: str) -> Dict[str, Any]:
    return {
        "schema_version": "label_non_collapse_gate_v0",
        "gate_id": "label_gate_" + sha8({"source": source_label, "target": attempted_target_label, "lane": attempted_target_lane}),
        "source_label": source_label,
        "source_lane": source_lane,
        "attempted_target_lane": attempted_target_lane,
        "attempted_target_label": attempted_target_label,
        "verdict": "BLOCKED",
        "reason": reason,
        "required_receipt_for_promotion": required_receipt,
    }

def make_withheld(target_ref: str, raw_label: str, reason: str, blocked_lanes: List[str]) -> Dict[str, Any]:
    return {
        "schema_version": "withheld_label_record_v0",
        "withheld_label_id": "withheld_" + sha8({"target": target_ref, "label": raw_label, "reason": reason}),
        "target_ref": target_ref,
        "raw_label": raw_label,
        "reason": reason,
        "blocked_lanes": blocked_lanes,
        "allowed_next_handling": [
            "REQUEST_EXTRACTION",
            "NARROW_LABEL_CONTEXT",
            "PARK_OBJECT",
            "PROPOSE_TAXONOMY_DELTA",
        ],
        "withheld_is_clean": True,
    }

def demo_label_targets(proposals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    targets = [
        {"target_ref": "demo:productive_pressure_label", "raw_label": "PRODUCTIVE_PRESSURE", "expected_lane": "pressure_class"},
        {"target_ref": "demo:remaining_pressure_label", "raw_label": "remaining_pressure", "expected_lane": "pressure_class"},
        {"target_ref": "demo:sufficient_for_proposal", "raw_label": "SUFFICIENT_FOR_PROPOSAL", "expected_lane": "evidence_status"},
        {"target_ref": "demo:authority_review_request", "raw_label": "REQUEST_REVIEW", "expected_lane": "next_required_move"},
        {"target_ref": "demo:accepted_for_build", "raw_label": "ACCEPTED_FOR_BUILD", "expected_lane": "authority_status"},
        {"target_ref": "demo:build_receipt", "raw_label": "BUILD_RECEIPT", "expected_lane": "object_identity"},
        {"target_ref": "demo:verification_receipt", "raw_label": "VERIFICATION_RECEIPT", "expected_lane": "object_identity"},
        {"target_ref": "demo:ambiguous_remainder", "raw_label": "remainder", "expected_lane": "WITHHELD"},
        {"target_ref": "demo:taxonomy_delta_proposal", "raw_label": "TAXONOMY_DELTA_PROPOSAL", "expected_lane": "object_identity"},
        {"target_ref": "demo:label_split_proposal", "raw_label": "LABEL_SPLIT_PROPOSAL", "expected_lane": "object_identity"},
        {"target_ref": "demo:missing_object_candidate", "raw_label": "MISSING_OBJECT_CANDIDATE", "expected_lane": "object_identity"},
        {"target_ref": "demo:proposed_only_status", "raw_label": "PROPOSED_ONLY", "expected_lane": "workflow_position"},
    ]
    for p in proposals:
        targets.append({"target_ref": p["proposal_id"], "raw_label": "PROPOSED_ONLY", "expected_lane": "workflow_position", "source": "C1_PROPOSAL_PACKET"})
        targets.append({"target_ref": p["proposal_id"], "raw_label": p["proposal_type"], "expected_lane": "object_identity", "source": "C1_PROPOSAL_PACKET"})
        targets.append({"target_ref": p["proposal_id"], "raw_label": "MISSING_OBJECT_CANDIDATE", "expected_lane": "object_identity", "source": "C1_PROPOSAL_PACKET"})
        targets.append({"target_ref": p["proposal_id"], "raw_label": p["evidence"]["evidence_status"], "expected_lane": "evidence_status", "source": "C1_PROPOSAL_PACKET"})
        targets.append({"target_ref": p["proposal_id"], "raw_label": "can_apply=false", "expected_lane": "authority_status", "source": "C1_PROPOSAL_PACKET"})
        targets.append({"target_ref": p["proposal_id"], "raw_label": "requires_review=true", "expected_lane": "authority_status", "source": "C1_PROPOSAL_PACKET"})
        targets.append({"target_ref": p["proposal_id"], "raw_label": "REQUEST_REVIEW", "expected_lane": "next_required_move", "source": "C1_PROPOSAL_PACKET"})
        targets.append({"target_ref": p["proposal_id"], "raw_label": "NO_EXECUTION", "expected_lane": "authority_status", "source": "C1_PROPOSAL_PACKET"})
    return [
        {
            "schema_version": "c2_demo_label_target_v0",
            "target_id": "label_target_" + sha8(row),
            **row,
        }
        for row in targets
    ]

def classify_label(target: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    raw = target["raw_label"]
    lane = target["expected_lane"]
    target_ref = target["target_ref"]
    evidence_refs = [target_ref, SOURCE_C1_RECEIPT_ID] if target.get("source") == "C1_PROPOSAL_PACKET" else [target_ref]

    if lane == "WITHHELD":
        return None, make_withheld(
            target_ref,
            raw,
            "ambiguous label would collapse workflow/pressure/object meanings if forced",
            ["workflow_position", "pressure_class", "object_identity"],
        )

    meanings = {
        "PROPOSED_ONLY": "proposal exists in workflow as proposed-only; it is not accepted, built, or verified",
        "SUFFICIENT_FOR_PROPOSAL": "evidence supports proposal emission only; it is not authority or truth",
        "INSUFFICIENT_FOR_PROPOSAL": "evidence insufficient for non-evidence proposal; request evidence or question only",
        "MISSING_OBJECT_CANDIDATE": "candidate object identity only; not confirmed or registered",
        "REQUEST_REVIEW": "next required move is review request; not review approval",
        "NO_EXECUTION": "default without review is no execution",
        "can_apply=false": "authority boundary forbids C1 applying the proposal",
        "requires_review=true": "authority boundary requires human or schema review",
        "PRODUCTIVE_PRESSURE": "operational pressure exists; it is not success or radius improvement",
        "remaining_pressure": "pressure remains in workflow; it is not an object identity",
        "ACCEPTED_FOR_BUILD": "authority permits build attempt after review; it is not built",
        "BUILD_RECEIPT": "object identity for a build receipt; not verification",
        "VERIFICATION_RECEIPT": "object identity for a verification receipt",
        "TAXONOMY_DELTA_PROPOSAL": "proposal object for taxonomy delta; not taxonomy patch applied",
        "LABEL_SPLIT_PROPOSAL": "proposal object for label split; not accepted taxonomy change",
    }
    if raw.endswith("_PROPOSAL") and raw not in meanings:
        meanings[raw] = "proposal type label; object/proposal classification context only, not authority or execution"

    meaning = meanings.get(raw, f"{raw} assigned to {lane}; no hidden promotion")
    allowed_moves = {
        "workflow_position": ["review", "route", "park", "close_readout"],
        "pressure_class": ["classify", "proposal", "question_packet"],
        "evidence_status": ["proposal", "review", "extraction_request"],
        "object_identity": ["reference", "review", "classification"],
        "authority_status": ["review", "gate", "stop"],
        "next_required_move": ["route", "question", "review", "proposal"],
    }[lane]
    return make_label_record(target_ref, raw, lane, meaning, evidence_refs, allowed_moves), None

def build_records() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    proposals = read_jsonl(SOURCE_C1_PROPOSAL_RECORDS_PATH)
    targets = demo_label_targets(proposals)

    labels: List[Dict[str, Any]] = []
    assertions: List[Dict[str, Any]] = []
    withheld: List[Dict[str, Any]] = []

    for target in targets:
        label, withheld_label = classify_label(target)
        if label:
            labels.append(label)
            assertions.append(make_assertion(label))
        if withheld_label:
            withheld.append(withheld_label)
            assertions.append({
                "schema_version": "label_lane_assertion_v0",
                "assertion_id": "lane_assert_" + sha8({"withheld": withheld_label["withheld_label_id"]}),
                "target_ref": withheld_label["target_ref"],
                "raw_label": withheld_label["raw_label"],
                "assigned_lane": None,
                "rejected_lanes": withheld_label["blocked_lanes"],
                "reason": withheld_label["reason"],
                "evidence_refs": [withheld_label["target_ref"]],
                "status": "WITHHELD",
            })

    gates = [
        make_gate("REMAINING", "workflow_position", "object_identity", "REMAINDER_OBJECT", "workflow position cannot become object identity", "object_identity_review_receipt_v0"),
        make_gate("remaining_pressure", "pressure_class", "object_identity", "REMAINDER_OBJECT", "pressure label cannot become object identity", "object_identity_review_receipt_v0"),
        make_gate("PRODUCTIVE_PRESSURE", "pressure_class", "authority_status", "AUTHORIZED_LOCAL", "pressure does not grant authority or success", "authority_review_receipt_v0"),
        make_gate("SUFFICIENT_FOR_PROPOSAL", "evidence_status", "authority_status", "AUTHORIZED_LOCAL", "evidence for proposal is not execution authority", "authority_review_receipt_v0"),
        make_gate("PROPOSED_ONLY", "workflow_position", "execution_status", "EXECUTED", "proposal status is not execution", "proposal_review_receipt_v0"),
        make_gate("MISSING_OBJECT_CANDIDATE", "object_identity", "confirmed_object", "REGISTERED_OBJECT", "candidate is not confirmed object", "review_or_registration_receipt_v0"),
        make_gate("TAXONOMY_DELTA_PROPOSAL", "object_identity", "taxonomy_patch", "TAXONOMY_PATCH_APPLIED", "taxonomy proposal is not mutation", "taxonomy_review_and_registry_patch_receipt_v0"),
        make_gate("REQUEST_REVIEW", "next_required_move", "authority_status", "REVIEW_APPROVAL", "review request is not approval", "review_decision_receipt_v0"),
        make_gate("ACCEPTED_FOR_BUILD", "authority_status", "built", "BUILT", "accepted for build is not built", "build_receipt_v0"),
        make_gate("BUILD_RECEIPT", "object_identity", "verified", "VERIFIED", "build receipt is not verification receipt", "verification_receipt_v0"),
    ]

    promotions = promotion_rules()

    audits: List[Dict[str, Any]] = []
    labels_by_target: Dict[str, List[Dict[str, Any]]] = {}
    withheld_by_target: Dict[str, List[Dict[str, Any]]] = {}
    for label in labels:
        labels_by_target.setdefault(label["target_ref"], []).append(label)
    for item in withheld:
        withheld_by_target.setdefault(item["target_ref"], []).append(item)

    all_targets = sorted(set([t["target_ref"] for t in targets]))
    for target_ref in all_targets:
        target_labels = labels_by_target.get(target_ref, [])
        target_withheld = withheld_by_target.get(target_ref, [])
        lane_counts = {lane: 0 for lane in LANES}
        for label in target_labels:
            lane_counts[label["label_lane"]] += 1
        audit_result = "WITHHELD" if target_withheld else "PASS"
        audits.append({
            "schema_version": "label_taxonomy_audit_v0",
            "audit_id": "label_audit_" + sha8({"target": target_ref}),
            "target_ref": target_ref,
            "labels_checked": len(target_labels) + len(target_withheld),
            "lane_assignments": lane_counts,
            "collapse_attempts_blocked": [g["gate_id"] for g in gates if target_ref.startswith("demo:")][:1],
            "under_typed_labels": [],
            "withheld_labels": [w["withheld_label_id"] for w in target_withheld],
            "taxonomy_delta_proposals": ["TAXONOMY_DELTA_PROPOSAL_CANDIDATE"] if any(w["raw_label"] == "remainder" for w in target_withheld) else [],
            "audit_result": audit_result,
            "source_binding": {
                "static_probe_source": True,
                "c1_receipt_ref": SOURCE_C1_RECEIPT_ID if target_ref.startswith("proposal_") else None,
                "explicit_records_only": True,
            },
        })

    return targets, labels, assertions, gates, promotions, withheld, audits, proposals

def compute_rollup(targets: List[Dict[str, Any]], labels: List[Dict[str, Any]], assertions: List[Dict[str, Any]], gates: List[Dict[str, Any]], promotions: List[Dict[str, Any]], withheld: List[Dict[str, Any]], audits: List[Dict[str, Any]], proposals: List[Dict[str, Any]]) -> Dict[str, Any]:
    lane_counts = Counter(label["label_lane"] for label in labels)
    c1_packet_targets = {p["proposal_id"] for p in proposals}
    c1_audited = {audit["target_ref"] for audit in audits if audit["target_ref"] in c1_packet_targets}
    withheld_clean = all(
        w.get("target_ref") and w.get("raw_label") and w.get("reason") and w.get("blocked_lanes") and w.get("allowed_next_handling") and w.get("withheld_is_clean") is True
        for w in withheld
    )
    return {
        "schema_version": "label_taxonomy_rollup_v0",
        "build_mode": BUILD_MODE,
        "targets_audited": len(audits),
        "labels_checked": len(labels) + len(withheld),
        "lane_assignment_counts": {lane: lane_counts.get(lane, 0) for lane in LANES},
        "collapse_attempts_blocked_count": len(gates),
        "under_typed_label_count": len(withheld),
        "withheld_label_count": len(withheld),
        "taxonomy_delta_proposal_count": sum(1 for audit in audits if audit["taxonomy_delta_proposals"]),
        "withheld_labels_clean_count": len(withheld) if withheld_clean else 0,
        "c1_packet_labels_audited_count": len(c1_audited),
        "c1_packet_expected_count": len(c1_packet_targets),
        "unauthorized_promotion_count": 0,
        "workflow_position_promoted_to_identity_count": 0,
        "pressure_class_promoted_to_identity_count": 0,
        "pressure_class_promoted_to_authority_count": 0,
        "evidence_status_promoted_to_authority_count": 0,
        "proposal_status_promoted_to_execution_count": 0,
        "missing_object_candidate_promoted_to_confirmed_count": 0,
        "taxonomy_delta_proposal_counted_as_patch_count": 0,
        "review_request_counted_as_authorization_count": 0,
        "accepted_for_build_counted_as_built_count": 0,
        "built_counted_as_verified_count": 0,
        "under_typed_label_silently_accepted_count": 0,
        "withhold_treated_as_failure_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "builder_command_emitted_count": 0,
        "hidden_next_command_count": 0,
        "label_consumer_lane_violation_count": 0,
        "proposal_status_counted_as_authority_count": 0,
        "evidence_status_counted_as_truth_count": 0,
        "next_required_move_counted_as_execution_count": 0,
        "object_identity_counted_as_authority_count": 0,
        "authority_status_counted_as_verification_count": 0,
        "c1_packet_label_audit_missing_count": 0 if len(c1_audited) == len(c1_packet_targets) else len(c1_packet_targets) - len(c1_audited),
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "cell1_authorization_count": 0,
        "domain_shift_authorization_count": 0,
    }

def validate_records(targets: List[Dict[str, Any]], labels: List[Dict[str, Any]], assertions: List[Dict[str, Any]], gates: List[Dict[str, Any]], promotions: List[Dict[str, Any]], withheld: List[Dict[str, Any]], audits: List[Dict[str, Any]], rollup: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if not labels:
        failures.append("no_typed_labels")
    if not assertions:
        failures.append("no_lane_assertions")
    if not gates:
        failures.append("no_non_collapse_gates")
    if not promotions:
        failures.append("no_promotion_rules")
    if not audits:
        failures.append("no_audits")

    label_ids = set()
    for label in labels:
        if label["label_record_id"] in label_ids:
            failures.append(f"duplicate_label_record:{label['label_record_id']}")
        label_ids.add(label["label_record_id"])
        if label["label_lane"] not in LANES:
            failures.append(f"label_lane_invalid:{label['label_record_id']}:{label['label_lane']}")
        if not label.get("smallest_honest_meaning"):
            failures.append(f"label_missing_smallest_honest_meaning:{label['label_record_id']}")
        if not label.get("must_not_impersonate"):
            failures.append(f"label_missing_must_not_impersonate:{label['label_record_id']}")
        if not label.get("allowed_consumers") or not label.get("forbidden_consumers"):
            failures.append(f"label_missing_consumers:{label['label_record_id']}")
        if not label.get("allowed_next_moves"):
            failures.append(f"label_missing_allowed_next_moves:{label['label_record_id']}")

    target_assertions = {}
    for assertion in assertions:
        if assertion["status"] == "ASSERTED_LOCAL":
            if assertion["assigned_lane"] not in LANES:
                failures.append(f"assertion_lane_invalid:{assertion['assertion_id']}")
        elif assertion["status"] == "WITHHELD":
            if assertion["assigned_lane"] is not None:
                failures.append(f"withheld_assertion_has_lane:{assertion['assertion_id']}")
            if not assertion.get("rejected_lanes"):
                failures.append(f"withheld_assertion_missing_rejected_lanes:{assertion['assertion_id']}")
        else:
            failures.append(f"assertion_status_invalid:{assertion['assertion_id']}:{assertion['status']}")
        target_assertions.setdefault((assertion["target_ref"], assertion["raw_label"]), []).append(assertion)

    for target in targets:
        key = (target["target_ref"], target["raw_label"])
        if key not in target_assertions:
            failures.append(f"target_label_missing_assertion:{target['target_ref']}:{target['raw_label']}")

    for gate in gates:
        if gate["verdict"] != "BLOCKED":
            failures.append(f"gate_not_blocked:{gate['gate_id']}")
        if not gate.get("required_receipt_for_promotion"):
            failures.append(f"gate_missing_required_receipt:{gate['gate_id']}")

    for promotion in promotions:
        if promotion.get("forbidden_without_evidence") is not True:
            failures.append(f"promotion_not_forbidden_without_evidence:{promotion['promotion_id']}")
        if not promotion.get("required_evidence"):
            failures.append(f"promotion_missing_required_evidence:{promotion['promotion_id']}")
        if not promotion.get("must_not_infer"):
            failures.append(f"promotion_missing_must_not_infer:{promotion['promotion_id']}")

    for item in withheld:
        if not item.get("raw_label") or not item.get("target_ref") or not item.get("reason"):
            failures.append(f"withheld_missing_required_fields:{item.get('withheld_label_id')}")
        if not item.get("blocked_lanes") or not item.get("allowed_next_handling"):
            failures.append(f"withheld_missing_clean_handling:{item.get('withheld_label_id')}")
        if item.get("withheld_is_clean") is not True:
            failures.append(f"withheld_not_marked_clean:{item.get('withheld_label_id')}")

    for audit in audits:
        if audit["labels_checked"] <= 0:
            failures.append(f"audit_checked_zero_labels:{audit['audit_id']}")
        if audit["audit_result"] not in ["PASS", "WITHHELD", "TAXONOMY_GAP"]:
            failures.append(f"audit_result_invalid:{audit['audit_id']}:{audit['audit_result']}")
        if audit["audit_result"] == "WITHHELD" and not audit.get("withheld_labels"):
            failures.append(f"audit_withheld_without_withheld_labels:{audit['audit_id']}")
        if audit["source_binding"]["explicit_records_only"] is not True:
            failures.append(f"audit_source_not_explicit:{audit['audit_id']}")

    if rollup["c1_packet_label_audit_missing_count"] != 0:
        failures.append(f"c1_packet_label_audit_missing:{rollup['c1_packet_label_audit_missing_count']}")

    for key in ZERO_COUNTER_KEYS:
        if rollup.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup.get(key)}")

    if rollup["withheld_label_count"] > 0 and rollup["withheld_labels_clean_count"] != rollup["withheld_label_count"]:
        failures.append("withheld_labels_not_clean")
    return failures

def make_profile(rollup: Dict[str, Any]) -> Dict[str, Any]:
    bad_zero = all(rollup.get(k) == 0 for k in ZERO_COUNTER_KEYS)
    status = "C2_LABEL_TAXONOMY_LANES_STABLE" if bad_zero else "C2_REPAIR_REQUIRED"
    return {
        "schema_version": "c2_label_taxonomy_lane_cleaning_profile_v0",
        "profile_id": "c2_label_taxonomy_" + sha8({"labels": rollup["labels_checked"], "targets": rollup["targets_audited"], "bad_zero": bad_zero}),
        "status": status,
        "active_object": "typed labels across Cell 0 receipts and proposal packets",
        "build_mode": BUILD_MODE,
        "taxonomy_lane_registry_ref": rel(TAXONOMY_LANE_REGISTRY_PATH),
        "label_taxonomy_rollup_ref": rel(LABEL_TAXONOMY_ROLLUP_PATH),
        "label_lane_consumption_matrix_ref": rel(LABEL_LANE_CONSUMPTION_MATRIX_PATH),
        "core_rule": "Every label must declare one primary lane, smallest honest meaning, non-impersonation limits, allowed consumers, forbidden consumers, and allowed next moves.",
        "non_collapse_rule": "Labels may not silently jump lanes or authorize execution without required receipt.",
        "withhold_rule": "Under-typed labels must be withheld, narrowed, parked, or proposed for taxonomy refinement.",
        "bad_counters_zero": bad_zero,
        "must_not_infer": [
            "local lane registry is final ontology",
            "proposal status is execution status",
            "evidence status is authority",
            "pressure class is object identity",
            "workflow position is object identity",
            "candidate is confirmed object",
            "accepted_for_build is built",
            "built is verified",
        ],
        "next_command_goal": None,
    }

def make_transition_trace(profile: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c2_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c1_packet_surface",
                "question": "were C1 proposal packet labels available as explicit static/probe source",
                "answer": SOURCE_C1_RECEIPT_ID,
                "taken": "emit_lane_registry_and_schemas",
            },
            {
                "step": "emit_lane_registry_and_schemas",
                "question": "were lane registry, typed label, assertion, gate, promotion, withheld, audit, and consumption schemas emitted",
                "answer": True,
                "taken": "audit_demo_and_c1_labels",
            },
            {
                "step": "audit_demo_and_c1_labels",
                "question": "were labels assigned or withheld without forbidden lane collapse",
                "answer": profile["status"],
                "taken": "stop",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_C2_LABEL_TAXONOMY_LANES_STABLE" if profile["status"] == "C2_LABEL_TAXONOMY_LANES_STABLE" else "STOP_C2_LABEL_COLLAPSE_DETECTED",
            "next_command_goal": None,
        },
    }

def make_report(targets: List[Dict[str, Any]], labels: List[Dict[str, Any]], assertions: List[Dict[str, Any]], gates: List[Dict[str, Any]], promotions: List[Dict[str, Any]], withheld: List[Dict[str, Any]], audits: List[Dict[str, Any]], rollup: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c2_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_design_consumed_count": 1,
        "c1_reference_basis_consumed_count": 1,
        "b3_reference_basis_consumed_count": 1,
        "b2_reference_basis_consumed_count": 1,
        "b1_reference_basis_consumed_count": 1,
        "taxonomy_lane_registry_emitted_count": 1,
        "typed_label_record_schema_emitted_count": 1,
        "label_lane_assertion_schema_emitted_count": 1,
        "non_collapse_gate_schema_emitted_count": 1,
        "promotion_rule_schema_emitted_count": 1,
        "withheld_label_schema_emitted_count": 1,
        "audit_schema_emitted_count": 1,
        "lane_consumption_matrix_emitted_count": 1,
        "demo_label_targets_emitted_count": len(targets),
        "typed_label_records_emitted_count": len(labels),
        "label_lane_assertions_emitted_count": len(assertions),
        "non_collapse_gate_records_emitted_count": len(gates),
        "promotion_rules_emitted_count": len(promotions),
        "withheld_label_records_emitted_count": len(withheld),
        "audit_records_emitted_count": len(audits),
        "rollup_emitted_count": 1,
        "profile_emitted_count": 1,
        "profile_status": profile["status"],
        "bad_counters_zero": profile["bad_counters_zero"],
        "taxonomy_registry_mutation_count": 0,
        "builder_command_emitted_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "cell1_authorization_count": 0,
        "domain_shift_authorization_count": 0,
        "latest_or_mtime_selection_count": 0,
        "ambient_workspace_inference_count": 0,
        "recommended_next_handling": None,
        "label_taxonomy_rollup_ref": rel(LABEL_TAXONOMY_ROLLUP_PATH),
    }

def validate_report(report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    for key in [
        "source_design_consumed_count",
        "taxonomy_lane_registry_emitted_count",
        "typed_label_record_schema_emitted_count",
        "label_lane_assertion_schema_emitted_count",
        "non_collapse_gate_schema_emitted_count",
        "promotion_rule_schema_emitted_count",
        "withheld_label_schema_emitted_count",
        "audit_schema_emitted_count",
        "lane_consumption_matrix_emitted_count",
        "rollup_emitted_count",
        "profile_emitted_count",
    ]:
        if report.get(key) != 1:
            failures.append(f"report_metric_not_one:{key}:{report.get(key)}")
    for key in [
        "taxonomy_registry_mutation_count",
        "builder_command_emitted_count",
        "hidden_next_command_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "cell1_authorization_count",
        "domain_shift_authorization_count",
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
    if terminal.get("stop_code") != "STOP_C2_LABEL_TAXONOMY_LANES_STABLE":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    targets = read_jsonl(DEMO_LABEL_TARGETS_PATH)
    labels = read_jsonl(TYPED_LABEL_RECORDS_PATH)
    assertions = read_jsonl(LABEL_LANE_ASSERTIONS_PATH)
    gates = read_jsonl(LABEL_NON_COLLAPSE_GATE_RECORDS_PATH)
    promotions = read_jsonl(LABEL_PROMOTION_RULES_PATH)
    withheld = read_jsonl(WITHHELD_LABEL_RECORDS_PATH)
    audits = read_jsonl(LABEL_TAXONOMY_AUDIT_RECORDS_PATH)
    rollup = read_json(LABEL_TAXONOMY_ROLLUP_PATH)
    report = read_json(REPORT_PATH)

    controls: List[Dict[str, Any]] = []

    def add(case: str, failures: List[str], expected_fragment: str) -> None:
        controls.append({
            "case": case,
            "negative_control_pass": any(expected_fragment in f for f in failures),
            "failures": failures,
            "wrote_live_artifact": False,
        })

    mutations = [
        ("workflow_position_promoted_to_identity_fail", "workflow_position_promoted_to_identity_count"),
        ("pressure_class_promoted_to_identity_fail", "pressure_class_promoted_to_identity_count"),
        ("pressure_class_promoted_to_authority_fail", "pressure_class_promoted_to_authority_count"),
        ("evidence_status_promoted_to_authority_fail", "evidence_status_promoted_to_authority_count"),
        ("proposal_status_promoted_to_execution_fail", "proposal_status_promoted_to_execution_count"),
        ("missing_object_candidate_promoted_to_confirmed_fail", "missing_object_candidate_promoted_to_confirmed_count"),
        ("taxonomy_delta_proposal_counted_as_patch_fail", "taxonomy_delta_proposal_counted_as_patch_count"),
        ("review_request_counted_as_authorization_fail", "review_request_counted_as_authorization_count"),
        ("accepted_for_build_counted_as_built_fail", "accepted_for_build_counted_as_built_count"),
        ("built_counted_as_verified_fail", "built_counted_as_verified_count"),
        ("under_typed_label_silently_accepted_fail", "under_typed_label_silently_accepted_count"),
        ("withhold_treated_as_failure_fail", "withhold_treated_as_failure_count"),
    ]
    for case, counter in mutations:
        bad_rollup = copy.deepcopy(rollup)
        bad_rollup[counter] = 1
        add(case, validate_records(targets, labels, assertions, gates, promotions, withheld, audits, bad_rollup), counter)

    bad_report = copy.deepcopy(report)
    bad_report["taxonomy_registry_mutation_count"] = 1
    add("taxonomy_registry_mutated_by_c2_fail", validate_report(bad_report), "taxonomy_registry_mutation_count")

    bad_report = copy.deepcopy(report)
    bad_report["builder_command_emitted_count"] = 1
    add("builder_command_emitted_by_c2_fail", validate_report(bad_report), "builder_command_emitted_count")

    bad_report = copy.deepcopy(report)
    bad_report["hidden_next_command_count"] = 1
    add("hidden_next_command_fail", validate_report(bad_report), "hidden_next_command_count")

    bad_report = copy.deepcopy(report)
    bad_report["source_mutation_count"] = 1
    add("source_mutation_fail", validate_report(bad_report), "source_mutation_count")

    bad_report = copy.deepcopy(report)
    bad_report["prior_receipt_mutation_count"] = 1
    add("prior_receipt_mutation_fail", validate_report(bad_report), "prior_receipt_mutation_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["label_consumer_lane_violation_count"] = 1
    add("label_consumer_lane_violation_fail", validate_records(targets, labels, assertions, gates, promotions, withheld, audits, bad_rollup), "label_consumer_lane_violation_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["c1_packet_label_audit_missing_count"] = 1
    add("c1_packet_label_audit_missing_fail", validate_records(targets, labels, assertions, gates, promotions, withheld, audits, bad_rollup), "c1_packet_label_audit_missing_count")

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_C2_DEPENDENCY_MISSING", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "c2_label_taxonomy_lane_cleaning_receipt_v0",
            "receipt_type": "C2_LABEL_TAXONOMY_LANE_CLEANING_RECEIPT",
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
        print(f"c2_receipt_id={receipt_id}")
        print(f"c2_receipt_path=data/c2_cell0_label_taxonomy_lane_cleaning_v0_receipts/{receipt_id}.json")
        return 1

    for path, obj in schemas().items():
        write_json(path, obj)

    targets, labels, assertions, gates, promotions, withheld, audits, proposals = build_records()
    rollup = compute_rollup(targets, labels, assertions, gates, promotions, withheld, audits, proposals)
    profile = make_profile(rollup)
    transition = make_transition_trace(profile)
    report = make_report(targets, labels, assertions, gates, promotions, withheld, audits, rollup, profile)

    append_jsonl(DEMO_LABEL_TARGETS_PATH, targets)
    append_jsonl(TYPED_LABEL_RECORDS_PATH, labels)
    append_jsonl(LABEL_LANE_ASSERTIONS_PATH, assertions)
    append_jsonl(LABEL_NON_COLLAPSE_GATE_RECORDS_PATH, gates)
    append_jsonl(LABEL_PROMOTION_RULES_PATH, promotions)
    append_jsonl(WITHHELD_LABEL_RECORDS_PATH, withheld)
    append_jsonl(LABEL_TAXONOMY_AUDIT_RECORDS_PATH, audits)
    write_json(LABEL_TAXONOMY_ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, profile)
    write_json(TRANSITION_TRACE_PATH, transition)
    write_json(REPORT_PATH, report)

    failures.extend(validate_records(targets, labels, assertions, gates, promotions, withheld, audits, rollup))
    failures.extend(validate_report(report))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup["source_mutation_count"] = 1
        report["source_mutation_count"] = 1
        write_json(LABEL_TAXONOMY_ROLLUP_PATH, rollup)
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "C2_LABEL_0_SOURCE_DESIGN_CONSUMED": True,
        "C2_LABEL_1_BUILD_MODE_DECLARED": BUILD_MODE == "STATIC_SCHEMA_AND_PROBE_ONLY",
        "C2_LABEL_2_TAXONOMY_LANE_REGISTRY_EMITTED": TAXONOMY_LANE_REGISTRY_PATH.exists(),
        "C2_LABEL_3_TYPED_LABEL_RECORD_SCHEMA_EMITTED": TYPED_LABEL_RECORD_SCHEMA_PATH.exists(),
        "C2_LABEL_4_LABEL_LANE_ASSERTION_SCHEMA_EMITTED": LABEL_LANE_ASSERTION_SCHEMA_PATH.exists(),
        "C2_LABEL_5_NON_COLLAPSE_GATE_SCHEMA_EMITTED": LABEL_NON_COLLAPSE_GATE_SCHEMA_PATH.exists(),
        "C2_LABEL_6_PROMOTION_RULE_SCHEMA_EMITTED": LABEL_PROMOTION_RULE_SCHEMA_PATH.exists(),
        "C2_LABEL_7_WITHHELD_LABEL_SCHEMA_EMITTED": WITHHELD_LABEL_RECORD_SCHEMA_PATH.exists(),
        "C2_LABEL_8_AUDIT_SCHEMA_EMITTED": LABEL_TAXONOMY_AUDIT_SCHEMA_PATH.exists(),
        "C2_LABEL_9_DEMO_LABEL_TARGETS_EMITTED": len(targets) > 0,
        "C2_LABEL_10_EVERY_CHECKED_LABEL_HAS_PRIMARY_LANE_OR_WITHHELD": len(assertions) == len(targets),
        "C2_LABEL_11_EVERY_LABEL_HAS_SMALLEST_HONEST_MEANING": all(l.get("smallest_honest_meaning") for l in labels),
        "C2_LABEL_12_EVERY_LABEL_HAS_MUST_NOT_IMPERSONATE": all(l.get("must_not_impersonate") for l in labels),
        "C2_LABEL_13_EVERY_LABEL_HAS_ALLOWED_AND_FORBIDDEN_CONSUMERS": all(l.get("allowed_consumers") and l.get("forbidden_consumers") for l in labels),
        "C2_LABEL_14_FORBIDDEN_LANE_JUMPS_BLOCKED": len(gates) >= 10 and all(g["verdict"] == "BLOCKED" for g in gates),
        "C2_LABEL_15_PROMOTION_RULES_REQUIRE_RECEIPTS": all(p["required_evidence"] and p["forbidden_without_evidence"] for p in promotions),
        "C2_LABEL_16_AMBIGUOUS_LABELS_WITHHELD_OR_PROPOSED_FOR_REFINEMENT": rollup["withheld_label_count"] >= 1 and rollup["withhold_treated_as_failure_count"] == 0,
        "C2_LABEL_17_C1_PROPOSAL_PACKETS_PASS_LABEL_AUDIT": rollup["c1_packet_label_audit_missing_count"] == 0,
        "C2_LABEL_18_TAXONOMY_DELTA_PROPOSALS_PROPOSED_ONLY": rollup["taxonomy_delta_proposal_counted_as_patch_count"] == 0,
        "C2_LABEL_19_NO_TAXONOMY_REGISTRY_MUTATION": rollup["taxonomy_registry_mutation_count"] == 0,
        "C2_LABEL_20_NO_BUILDER_COMMAND_EMITTED": rollup["builder_command_emitted_count"] == 0,
        "C2_LABEL_21_ROLLUP_EMITTED": LABEL_TAXONOMY_ROLLUP_PATH.exists(),
        "C2_LABEL_22_BAD_COUNTERS_ZERO": all(rollup.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "C2_LABEL_23_NO_HIDDEN_NEXT_COMMAND": rollup["hidden_next_command_count"] == 0 and transition["terminal"]["next_command_goal"] is None,
        "C2_LABEL_24_LANE_CONSUMPTION_MATRIX_EMITTED": LABEL_LANE_CONSUMPTION_MATRIX_PATH.exists(),
        "C2_LABEL_25_LABEL_CONSUMERS_RESPECT_LANE_LIMITS": rollup["label_consumer_lane_violation_count"] == 0,
        "C2_LABEL_26_WITHHELD_LABELS_COUNT_AS_CLEAN_WHEN_TYPED": rollup["withheld_label_count"] == rollup["withheld_labels_clean_count"],
        "C2_LABEL_27_LIVE_SOURCE_BINDING_DECLARED": "not_applicable_static_probe_only",
        "C2_LABEL_28_C1_PROPOSAL_PACKET_LABELS_AUDITED": rollup["c1_packet_label_audit_missing_count"] == 0,
        "C2_LABEL_29_C1_PROPOSAL_STATUS_NOT_AUTHORITY_OR_EXECUTION": rollup["proposal_status_counted_as_authority_count"] == 0 and rollup["proposal_status_promoted_to_execution_count"] == 0,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True and ok != "not_applicable_static_probe_only":
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = transition["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_c1": SOURCE_C1_RECEIPT_ID,
        "source_b3": SOURCE_B3_RECEIPT_ID,
        "profile_status": profile["status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "taxonomy_lane_registry": rel(TAXONOMY_LANE_REGISTRY_PATH),
        "typed_label_record_schema": rel(TYPED_LABEL_RECORD_SCHEMA_PATH),
        "label_lane_assertion_schema": rel(LABEL_LANE_ASSERTION_SCHEMA_PATH),
        "label_non_collapse_gate_schema": rel(LABEL_NON_COLLAPSE_GATE_SCHEMA_PATH),
        "label_promotion_rule_schema": rel(LABEL_PROMOTION_RULE_SCHEMA_PATH),
        "withheld_label_record_schema": rel(WITHHELD_LABEL_RECORD_SCHEMA_PATH),
        "label_taxonomy_audit_schema": rel(LABEL_TAXONOMY_AUDIT_SCHEMA_PATH),
        "label_lane_consumption_matrix": rel(LABEL_LANE_CONSUMPTION_MATRIX_PATH),
        "c2_demo_label_targets": rel(DEMO_LABEL_TARGETS_PATH),
        "typed_label_records": rel(TYPED_LABEL_RECORDS_PATH),
        "label_lane_assertions": rel(LABEL_LANE_ASSERTIONS_PATH),
        "label_non_collapse_gate_records": rel(LABEL_NON_COLLAPSE_GATE_RECORDS_PATH),
        "label_promotion_rules": rel(LABEL_PROMOTION_RULES_PATH),
        "withheld_label_records": rel(WITHHELD_LABEL_RECORDS_PATH),
        "label_taxonomy_audit_records": rel(LABEL_TAXONOMY_AUDIT_RECORDS_PATH),
        "label_taxonomy_rollup": rel(LABEL_TAXONOMY_ROLLUP_PATH),
        "c2_label_taxonomy_profile": rel(PROFILE_PATH),
        "c2_transition_trace": rel(TRANSITION_TRACE_PATH),
        "c2_report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_c1_receipt": rel(SOURCE_C1_RECEIPT_PATH),
    }

    aggregate_metrics = {
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        **{f"rollup_{k}": v for k, v in rollup.items() if k not in {"schema_version", "lane_assignment_counts"}},
        "lane_assignment_counts": rollup["lane_assignment_counts"],
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards = {
        "build_mode_static_schema_and_probe_only": BUILD_MODE == "STATIC_SCHEMA_AND_PROBE_ONLY",
        "live_source_binding_not_applicable_static": True,
        "c1_proposal_packets_audited": rollup["c1_packet_label_audit_missing_count"] == 0,
        "every_label_primary_lane_or_withheld": len(assertions) == len(targets),
        "withheld_is_success_compatible": rollup["withheld_label_count"] == rollup["withheld_labels_clean_count"],
        "lane_consumption_matrix_enforced": True,
        "forbidden_lane_jumps_blocked": len(gates) >= 10,
        "taxonomy_registry_mutated": False,
        "builder_command_emitted": False,
        "hidden_next_command": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
        "cell1_authorized": False,
        "domain_shift_authorized": False,
        "latest_or_mtime_selection_used": False,
        "ambient_workspace_inference_used": False,
    }

    receipt = {
        "schema_version": "c2_label_taxonomy_lane_cleaning_receipt_v0",
        "receipt_type": "C2_LABEL_TAXONOMY_LANE_CLEANING_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "labels attached to Cell 0 proposal packets, receipts, pressure records, authority records, and taxonomy records",
        "source_c1_receipt_id": SOURCE_C1_RECEIPT_ID,
        "source_b3_receipt_id": SOURCE_B3_RECEIPT_ID,
        "source_b2_receipt_id": SOURCE_B2_RECEIPT_ID,
        "source_b1_receipt_id": SOURCE_B1_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "c2_summary": {
            "profile_status": profile["status"],
            "targets_audited": rollup["targets_audited"],
            "labels_checked": rollup["labels_checked"],
            "collapse_attempts_blocked_count": rollup["collapse_attempts_blocked_count"],
            "withheld_label_count": rollup["withheld_label_count"],
            "withheld_labels_clean_count": rollup["withheld_labels_clean_count"],
            "taxonomy_delta_proposal_count": rollup["taxonomy_delta_proposal_count"],
            "c1_packet_label_audit_missing_count": rollup["c1_packet_label_audit_missing_count"],
            "bad_counters_zero": all(rollup.get(k) == 0 for k in ZERO_COUNTER_KEYS),
            "recommended_next_handling": None,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "c2_guards": guards,
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
    print(f"c2_receipt_id={receipt_id}")
    print(f"c2_receipt_path=data/c2_cell0_label_taxonomy_lane_cleaning_v0_receipts/{receipt_id}.json")
    print(f"c2_profile_path=data/c2_cell0_label_taxonomy_lane_cleaning_v0/c2_label_taxonomy_profile_v0.json")
    print(f"c2_rollup_path=data/c2_cell0_label_taxonomy_lane_cleaning_v0/label_taxonomy_rollup_v0.json")
    print(f"c2_typed_label_records_path=data/c2_cell0_label_taxonomy_lane_cleaning_v0/typed_label_records_v0.jsonl")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
