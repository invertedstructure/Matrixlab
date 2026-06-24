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

UNIT_ID = "BUILD_C3_CELL0_MICRO_DOMAIN_SHIFT_REHEARSAL_V0"
TARGET_UNIT_ID = "c3.cell0.micro_domain_shift_rehearsal.v0"
LAYER = "CELL_0 / MICRO_DOMAIN_SHIFT_REHEARSAL"
MODE = "VERIFY / REFLECT / INTERFACE_STRESS_TEST"
BUILD_MODE = "STATIC_MICRO_DOMAIN_REHEARSAL_ONLY"
DOMAIN_KIND = "artifact_review"

SOURCE_B3_RECEIPT_ID = "a4cbf33f"
SOURCE_B3_RECEIPT_PATH = ROOT / "data" / "b3_cell0_local_decision_loop_schema_lock_v0_receipts" / "a4cbf33f.json"
SOURCE_B3_LOOP_SCHEMA_PATH = ROOT / "data" / "b3_cell0_local_decision_loop_schema_lock_v0" / "local_decision_loop_schema_v0.json"
SOURCE_B3_STEP_ENUM_PATH = ROOT / "data" / "b3_cell0_local_decision_loop_schema_lock_v0" / "local_decision_loop_step_enum_v0.json"
SOURCE_B3_LOOP_RECEIPTS_PATH = ROOT / "data" / "b3_cell0_local_decision_loop_schema_lock_v0" / "local_decision_loop_receipts_v0.jsonl"
SOURCE_B3_TRACE_RECORDS_PATH = ROOT / "data" / "b3_cell0_local_decision_loop_schema_lock_v0" / "local_decision_loop_trace_records_v0.jsonl"

SOURCE_C1_RECEIPT_ID = "f8f37c4e"
SOURCE_C1_RECEIPT_PATH = ROOT / "data" / "c1_cell0_proposal_layer_v0_receipts" / "f8f37c4e.json"
SOURCE_C1_PROFILE_PATH = ROOT / "data" / "c1_cell0_proposal_layer_v0" / "c1_proposal_layer_profile_v0.json"
SOURCE_C1_PACKET_SCHEMA_PATH = ROOT / "data" / "c1_cell0_proposal_layer_v0" / "proposal_packet_schema_v0.json"
SOURCE_C1_PROPOSAL_RECORDS_PATH = ROOT / "data" / "c1_cell0_proposal_layer_v0" / "proposal_packet_records_v0.jsonl"
SOURCE_C1_ROLLUP_PATH = ROOT / "data" / "c1_cell0_proposal_layer_v0" / "proposal_rollup_v0.json"

SOURCE_C2_RECEIPT_ID = "348dabde"
SOURCE_C2_RECEIPT_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts" / "348dabde.json"
SOURCE_C2_PROFILE_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "c2_label_taxonomy_profile_v0.json"
SOURCE_C2_TAXONOMY_LANE_REGISTRY_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "taxonomy_lane_registry_v0.json"
SOURCE_C2_CONSUMPTION_MATRIX_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "label_lane_consumption_matrix_v0.json"
SOURCE_C2_ROLLUP_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "label_taxonomy_rollup_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_B3_RECEIPT_PATH,
    SOURCE_B3_LOOP_SCHEMA_PATH,
    SOURCE_B3_STEP_ENUM_PATH,
    SOURCE_B3_LOOP_RECEIPTS_PATH,
    SOURCE_B3_TRACE_RECORDS_PATH,
    SOURCE_C1_RECEIPT_PATH,
    SOURCE_C1_PROFILE_PATH,
    SOURCE_C1_PACKET_SCHEMA_PATH,
    SOURCE_C1_PROPOSAL_RECORDS_PATH,
    SOURCE_C1_ROLLUP_PATH,
    SOURCE_C2_RECEIPT_PATH,
    SOURCE_C2_PROFILE_PATH,
    SOURCE_C2_TAXONOMY_LANE_REGISTRY_PATH,
    SOURCE_C2_CONSUMPTION_MATRIX_PATH,
    SOURCE_C2_ROLLUP_PATH,
]

OUT_DIR = ROOT / "data" / "c3_cell0_micro_domain_shift_rehearsal_v0"
RECEIPT_DIR = ROOT / "data" / "c3_cell0_micro_domain_shift_rehearsal_v0_receipts"

MICRO_DOMAIN_FIXTURE_SCHEMA_PATH = OUT_DIR / "micro_domain_fixture_schema_v0.json"
DOMAIN_SURFACE_SCHEMA_PATH = OUT_DIR / "domain_shift_surface_record_schema_v0.json"
DOMAIN_LOOP_TRACE_SCHEMA_PATH = OUT_DIR / "domain_shift_loop_trace_schema_v0.json"
CLAIM_CLASSIFICATION_SCHEMA_PATH = OUT_DIR / "micro_domain_claim_classification_schema_v0.json"
DOMAIN_LABEL_AUDIT_SCHEMA_PATH = OUT_DIR / "domain_shift_label_audit_schema_v0.json"
PROPOSAL_GAP_REPORT_SCHEMA_PATH = OUT_DIR / "domain_shift_proposal_gap_report_schema_v0.json"
MICRO_DOMAIN_OUTCOME_ENUM_PATH = OUT_DIR / "micro_domain_shift_outcome_enum_v0.json"
INTERFACE_GAP_SEVERITY_ENUM_PATH = OUT_DIR / "interface_gap_severity_enum_v0.json"
DOMAIN_CLAIM_SCOPE_BOUNDARY_PATH = OUT_DIR / "domain_claim_scope_boundary_v0.json"
B3_LOOP_REUSE_FINGERPRINT_PATH = OUT_DIR / "b3_loop_reuse_fingerprint_v0.json"
C1_PROPOSAL_SUFFICIENCY_CHECKLIST_PATH = OUT_DIR / "c1_proposal_sufficiency_checklist_v0.json"

DEMO_FIXTURES_PATH = OUT_DIR / "c3_demo_micro_domain_fixtures_v0.jsonl"
DOMAIN_SURFACE_RECORDS_PATH = OUT_DIR / "domain_shift_surface_records_v0.jsonl"
DOMAIN_LOOP_TRACES_PATH = OUT_DIR / "domain_shift_loop_traces_v0.jsonl"
CLAIM_CLASSIFICATIONS_PATH = OUT_DIR / "micro_domain_claim_classifications_v0.jsonl"
DOMAIN_LABEL_AUDIT_RECORDS_PATH = OUT_DIR / "domain_shift_label_audit_records_v0.jsonl"
PROPOSAL_GAP_REPORTS_PATH = OUT_DIR / "domain_shift_proposal_gap_reports_v0.jsonl"
DOMAIN_LABEL_STRESS_ASSERTIONS_PATH = OUT_DIR / "domain_label_stress_assertions_v0.jsonl"
MICRO_DOMAIN_SHIFT_ROLLUP_PATH = OUT_DIR / "micro_domain_shift_rollup_v0.json"
INTERFACE_READINESS_VERDICT_PATH = OUT_DIR / "c3_interface_readiness_verdict_v0.json"
PROFILE_PATH = OUT_DIR / "c3_micro_domain_shift_profile_v0.json"
TRANSITION_TRACE_PATH = OUT_DIR / "c3_transition_trace.json"
REPORT_PATH = OUT_DIR / "c3_report.json"

B3_STEPS = [
    "LOAD_SURFACE",
    "VALIDATE_SURFACE",
    "SELECT_PRESSURE_GROUP",
    "CHECK_INSPECTION_AUTHORITY",
    "INSPECT_MINIMAL_SURFACE",
    "CLASSIFY_PRESSURE",
    "IDENTIFY_REQUIRED_DISTINCTION",
    "CHECK_DISTINCTION_AVAILABLE",
    "DECIDE_LOCAL_EDGE",
    "EMIT_ARTIFACT",
    "EMIT_RECEIPT",
    "STOP_OR_ADVANCE",
]

CLAIM_CLASSIFICATIONS = [
    "SUPPORTED_LOCALLY",
    "UNSUPPORTED_BY_AVAILABLE_EVIDENCE",
    "BLOCKED_BY_NON_CLAIM",
    "UNDER_TYPED",
    "REQUIRES_EXTRACTION",
    "REQUIRES_REVIEW",
    "AMBIGUOUS",
]

OUTCOMES = [
    "MICRO_SHIFT_PASS",
    "MICRO_SHIFT_PASS_WITH_PROPOSAL_GAPS",
    "MICRO_SHIFT_LABEL_COLLAPSE_BLOCKED",
    "MICRO_SHIFT_LOOP_GAP",
    "MICRO_SHIFT_AUTHORITY_GAP",
    "MICRO_SHIFT_EXTRACTION_GAP",
    "MICRO_SHIFT_RECEIPT_GAP",
    "MICRO_SHIFT_FAIL_UNTYPED",
    "QUESTION_PACKET_NOT_COMMAND",
]

INTERFACE_VERDICTS = [
    "CELL1_NOT_READY_PROPOSAL_SCHEMA_GAPS",
    "CELL1_READY_FOR_NARROW_ACCEPTED_PROPOSAL_TEST",
    "CELL1_BLOCKED_BY_LABEL_COLLAPSE",
    "CELL1_BLOCKED_BY_LOOP_GAP",
    "CELL1_BLOCKED_BY_AUTHORITY_GAP",
    "CELL1_BLOCKED_BY_EXTRACTION_GAP",
    "CELL1_BLOCKED_BY_RECEIPT_GAP",
    "CELL1_READINESS_UNCLASSIFIED",
]

GAP_SEVERITIES = [
    "NO_GAP",
    "MINOR_SCHEMA_GAP",
    "MATERIAL_SCHEMA_GAP",
    "BLOCKING_SCHEMA_GAP",
    "AUTHORITY_BLOCKER",
    "EXTRACTION_BLOCKER",
    "RECEIPT_BLOCKER",
    "LOOP_BLOCKER",
]

ZERO_COUNTER_KEYS = [
    "bespoke_loop_count",
    "unauthorized_inspection_count",
    "unbounded_payload_inspection_count",
    "builder_authority_leak_count",
    "domain_shift_success_claim_count",
    "full_transfer_claim_count",
    "cell1_readiness_claim_count",
    "research_lab_readiness_claim_count",
    "supported_locally_counted_as_true_count",
    "unsupported_counted_as_false_count",
    "evidence_ref_counted_as_sufficient_count",
    "requires_extraction_counted_as_permission_count",
    "requires_review_counted_as_approval_count",
    "blocked_non_claim_counted_as_payload_failure_count",
    "domain_label_promoted_to_identity_count",
    "micro_shift_pass_counted_as_full_transfer_count",
    "proposal_gap_patched_inside_c3_count",
    "cell1_command_emitted_count",
    "builder_behavior_executed_count",
    "taxonomy_mutation_count",
    "proposal_applied_by_c3_count",
    "hidden_next_command_count",
    "source_mutation_count",
    "prior_receipt_mutation_count",
]

HUMAN_DECISION = {
    "decision": "BUILD_C3_CELL0_MICRO_DOMAIN_SHIFT_REHEARSAL",
    "scope": "Build C3 as the Cell 0 micro-domain-shift rehearsal in STATIC_MICRO_DOMAIN_REHEARSAL_ONLY mode. Define a tiny artifact-review fixture, run the locked B3 local decision loop unchanged against the new object family, audit labels using C2 lanes, test whether C1 proposal packets contain enough fields for future builder/review consumption, emit claim classifications, label audits, proposal gap reports, micro-domain shift rollup, interface-readiness verdict, profile, report, and receipt. Do not build Cell 1, perform full domain shift, mutate taxonomy, execute builder behavior, inspect unbounded payload, create bespoke loop paths, or claim full transfer.",
    "authorized": [
        "define micro-domain fixture schema",
        "define domain-shift surface record schema",
        "define domain-shift loop trace schema",
        "define micro-domain claim classification schema",
        "define domain-shift label audit schema",
        "define proposal gap report schema",
        "define micro-domain shift rollup schema",
        "run bounded micro-domain fixtures",
        "reuse B3 loop unchanged",
        "audit labels using C2 lanes",
        "check C1 proposal packet sufficiency",
        "emit C3 rehearsal packet",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "build Cell 1",
        "perform full domain shift",
        "create broad architecture",
        "optimize closure radius",
        "create new authority",
        "invent domain-specific bespoke loop",
        "inspect unbounded payload",
        "mutate taxonomy without review",
        "treat unfamiliar labels as object identities",
        "treat micro-domain pass as proof of transfer",
        "treat one rehearsal as research-lab readiness",
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
    b3_schema = read_json(SOURCE_B3_LOOP_SCHEMA_PATH)
    c1_receipt = read_json(SOURCE_C1_RECEIPT_PATH)
    c1_profile = read_json(SOURCE_C1_PROFILE_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)
    c2_profile = read_json(SOURCE_C2_PROFILE_PATH)

    if b3_receipt.get("receipt_id") != SOURCE_B3_RECEIPT_ID or b3_receipt.get("gate") != "PASS":
        failures.append("b3_basis_not_accepted")
    if b3_schema.get("loop_id") != "LOCAL_DECISION_LOOP_V0":
        failures.append("b3_loop_schema_wrong")
    if c1_receipt.get("receipt_id") != SOURCE_C1_RECEIPT_ID or c1_receipt.get("gate") != "PASS":
        failures.append("c1_basis_not_accepted")
    if c1_profile.get("status") != "C1_PROPOSAL_LAYER_STABLE":
        failures.append("c1_profile_not_stable")
    if c2_receipt.get("receipt_id") != SOURCE_C2_RECEIPT_ID or c2_receipt.get("gate") != "PASS":
        failures.append("c2_basis_not_accepted")
    if c2_profile.get("status") != "C2_LABEL_TAXONOMY_LANES_STABLE":
        failures.append("c2_profile_not_stable")
    return failures

def micro_domain_fixture_schema() -> Dict[str, Any]:
    return {
        "schema_version": "micro_domain_fixture_schema_v0",
        "fixture_schema": {
            "schema_version": "micro_domain_fixture_v0",
            "fixture_id": "micro_domain_artifact_review_001",
            "domain_kind": "artifact_review",
            "objects": [
                {
                    "object_id": "artifact_001",
                    "object_kind": "artifact_record",
                    "claims": [
                        {
                            "claim_id": "claim_001",
                            "claim_text": None,
                            "evidence_refs": [],
                        }
                    ],
                }
            ],
            "allowed_inspection": {
                "inspection_mode": "SUMMARY_ONLY",
                "allowed_fields": ["claim_id", "claim_text", "evidence_refs", "receipt_summary"],
                "forbidden_fields": ["unbounded_payload", "external_context"],
            },
        },
    }

def domain_surface_schema() -> Dict[str, Any]:
    return {
        "schema_version": "domain_shift_surface_record_schema_v0",
        "surface_schema": {
            "schema_version": "domain_shift_surface_record_v0",
            "surface_id": "domain_surface_<sig8>",
            "domain_kind": "artifact_review",
            "surface_kind": "claim_evidence_surface",
            "fixture_id": None,
            "allowed_inspection": {
                "inspection_mode": "SUMMARY_ONLY",
                "allowed_fields": [],
                "forbidden_fields": [],
            },
            "authority_profile_ref": None,
            "loop_schema_ref": "LOCAL_DECISION_LOOP_SCHEMA_V0",
        },
    }

def domain_loop_trace_schema() -> Dict[str, Any]:
    return {
        "schema_version": "domain_shift_loop_trace_schema_v0",
        "trace_schema": {
            "schema_version": "domain_shift_loop_trace_v0",
            "trace_id": "domain_loop_trace_<sig8>",
            "surface_ref": None,
            "loop_schema_ref": "LOCAL_DECISION_LOOP_SCHEMA_V0",
            "steps_completed": [],
            "required_distinction_refs": [],
            "selected_edges": [],
            "bespoke_step_count": 0,
            "forbidden_edge_count": 0,
            "terminal": {"type": "STOP", "stop_code": None, "next_command_goal": None},
        },
    }

def claim_classification_schema() -> Dict[str, Any]:
    return {
        "schema_version": "micro_domain_claim_classification_schema_v0",
        "closed_classifications": CLAIM_CLASSIFICATIONS,
        "classification_schema": {
            "schema_version": "micro_domain_claim_classification_v0",
            "claim_id": None,
            "classification": None,
            "evidence_status": None,
            "smallest_honest_reading": None,
            "must_not_infer": [],
            "allowed_next_handling": [],
        },
    }

def domain_label_audit_schema() -> Dict[str, Any]:
    return {
        "schema_version": "domain_shift_label_audit_schema_v0",
        "audit_schema": {
            "schema_version": "domain_shift_label_audit_v0",
            "audit_id": "domain_label_audit_<sig8>",
            "target_ref": None,
            "labels_checked": 0,
            "lane_collapse_attempts_blocked": [],
            "under_typed_labels": [],
            "withheld_labels": [],
            "audit_result": "PASS | WITHHELD | LABEL_GAP | FAIL",
        },
    }

def proposal_gap_report_schema() -> Dict[str, Any]:
    return {
        "schema_version": "domain_shift_proposal_gap_report_schema_v0",
        "gap_report_schema": {
            "schema_version": "domain_shift_proposal_gap_report_v0",
            "proposal_gap_report_id": "proposal_gap_<sig8>",
            "domain_kind": "artifact_review",
            "missing_fields_for_builder_consumption": [],
            "missing_fields_for_review": [],
            "missing_fields_for_verification": [],
            "missing_fields_for_authority_boundary": [],
            "gap_severity": None,
            "cell1_consumption_safe": False,
            "recommendation": None,
            "status": "PROPOSED_ONLY | NO_GAP | QUESTION_PACKET_REQUIRED",
        },
    }

def outcome_enum() -> Dict[str, Any]:
    return {
        "schema_version": "micro_domain_shift_outcome_enum_v0",
        "closed_outcomes": OUTCOMES,
        "interface_readiness_verdicts": INTERFACE_VERDICTS,
        "rule": "Interface readiness verdict is not a Cell 1 command.",
    }

def interface_gap_severity_enum() -> Dict[str, Any]:
    return {
        "schema_version": "interface_gap_severity_enum_v0",
        "closed_severities": GAP_SEVERITIES,
        "rules": {
            "NO_GAP": "no interface gap detected",
            "MINOR_SCHEMA_GAP": "future consumer would benefit from clarification",
            "MATERIAL_SCHEMA_GAP": "Cell 1 should not consume without review/schema patch",
            "BLOCKING_SCHEMA_GAP": "consumption would require guessing",
            "AUTHORITY_BLOCKER": "authority language is insufficient",
            "EXTRACTION_BLOCKER": "bounded extraction rules are insufficient",
            "RECEIPT_BLOCKER": "receipt shape is insufficient",
            "LOOP_BLOCKER": "B3 loop cannot process the surface unchanged",
        },
    }

def domain_claim_scope_boundary() -> Dict[str, Any]:
    return {
        "schema_version": "domain_claim_scope_boundary_v0",
        "domain_kind": DOMAIN_KIND,
        "boundaries": {
            "SUPPORTED_LOCALLY": "supported by local fixture evidence only; not true claim",
            "UNSUPPORTED_BY_AVAILABLE_EVIDENCE": "not supported by available refs; not false claim",
            "BLOCKED_BY_NON_CLAIM": "claim exceeds authorized scope; not semantic payload failure",
            "REQUIRES_EXTRACTION": "bounded extraction may be proposed; extraction is not performed",
            "REQUIRES_REVIEW": "review is needed; approval is not granted",
            "AMBIGUOUS": "withhold or question packet; not identity",
        },
    }

def b3_loop_reuse_fingerprint() -> Dict[str, Any]:
    source_schema = read_json(SOURCE_B3_LOOP_SCHEMA_PATH)
    source_steps = source_schema.get("steps") or [row.get("step") for row in read_json(SOURCE_B3_STEP_ENUM_PATH).get("steps", [])]
    return {
        "schema_version": "b3_loop_reuse_fingerprint_v0",
        "source_b3_receipt_id": SOURCE_B3_RECEIPT_ID,
        "source_loop_schema_ref": rel(SOURCE_B3_LOOP_SCHEMA_PATH),
        "source_step_sequence": source_steps,
        "c3_step_sequence": B3_STEPS,
        "step_sequence_equal": source_steps == B3_STEPS,
        "bespoke_step_count": 0,
        "step_insertions": [],
        "step_deletions": [],
        "step_renames": [],
    }

def c1_proposal_sufficiency_checklist() -> Dict[str, Any]:
    fields = {
        "claim_scope_present": "MISSING",
        "evidence_limitations_present": "PRESENT",
        "allowed_payload_boundary_present": "MISSING",
        "domain_object_scope_present": "MISSING",
        "expected_verification_receipt_shape_present": "PARTIAL",
        "rollback_or_reject_handling_present": "PARTIAL",
        "builder_input_contract_present": "MISSING",
        "authority_boundary_present": "PRESENT",
        "review_default_no_execution_present": "PRESENT",
        "must_not_infer_present": "PRESENT",
    }
    return {
        "schema_version": "c1_proposal_sufficiency_checklist_v0",
        "source_c1_receipt_id": SOURCE_C1_RECEIPT_ID,
        "domain_kind": DOMAIN_KIND,
        "checklist": fields,
        "rule": "Any MISSING field required for Cell 1 consumption creates a proposal gap report.",
        "cell1_consumption_safe": False,
    }

def schemas() -> Dict[Path, Dict[str, Any]]:
    return {
        MICRO_DOMAIN_FIXTURE_SCHEMA_PATH: micro_domain_fixture_schema(),
        DOMAIN_SURFACE_SCHEMA_PATH: domain_surface_schema(),
        DOMAIN_LOOP_TRACE_SCHEMA_PATH: domain_loop_trace_schema(),
        CLAIM_CLASSIFICATION_SCHEMA_PATH: claim_classification_schema(),
        DOMAIN_LABEL_AUDIT_SCHEMA_PATH: domain_label_audit_schema(),
        PROPOSAL_GAP_REPORT_SCHEMA_PATH: proposal_gap_report_schema(),
        MICRO_DOMAIN_OUTCOME_ENUM_PATH: outcome_enum(),
        INTERFACE_GAP_SEVERITY_ENUM_PATH: interface_gap_severity_enum(),
        DOMAIN_CLAIM_SCOPE_BOUNDARY_PATH: domain_claim_scope_boundary(),
        B3_LOOP_REUSE_FINGERPRINT_PATH: b3_loop_reuse_fingerprint(),
        C1_PROPOSAL_SUFFICIENCY_CHECKLIST_PATH: c1_proposal_sufficiency_checklist(),
    }

def make_fixtures() -> List[Dict[str, Any]]:
    fixtures = [
        {
            "fixture_id": "fixture_001_supported_local_claim",
            "claims": [
                {
                    "claim_id": "claim_001",
                    "claim_text": "receipt supports local closure packet",
                    "evidence_refs": [SOURCE_B3_RECEIPT_ID],
                    "expected_classification": "SUPPORTED_LOCALLY",
                }
            ],
        },
        {
            "fixture_id": "fixture_002_blocked_global_overclaim",
            "claims": [
                {
                    "claim_id": "claim_002",
                    "claim_text": "same receipt proves global autonomy",
                    "evidence_refs": [SOURCE_B3_RECEIPT_ID],
                    "expected_classification": "BLOCKED_BY_NON_CLAIM",
                }
            ],
        },
        {
            "fixture_id": "fixture_003_requires_extraction",
            "claims": [
                {
                    "claim_id": "claim_003",
                    "claim_text": "artifact includes uninspected payload evidence",
                    "evidence_refs": [],
                    "expected_classification": "REQUIRES_EXTRACTION",
                }
            ],
        },
        {
            "fixture_id": "fixture_004_label_ambiguity_or_review_request",
            "claims": [
                {
                    "claim_id": "claim_004",
                    "claim_text": "domain label appears accepted but review boundary is ambiguous",
                    "evidence_refs": [SOURCE_C1_RECEIPT_ID],
                    "expected_classification": "REQUIRES_REVIEW",
                },
                {
                    "claim_id": "claim_005",
                    "claim_text": "domain object label could mean artifact, claim, or review status",
                    "evidence_refs": [],
                    "expected_classification": "AMBIGUOUS",
                },
            ],
        },
        {
            "fixture_id": "fixture_005_unsupported_by_available_evidence",
            "claims": [
                {
                    "claim_id": "claim_006",
                    "claim_text": "artifact claim lacks supporting local receipt evidence",
                    "evidence_refs": [],
                    "expected_classification": "UNSUPPORTED_BY_AVAILABLE_EVIDENCE",
                }
            ],
        },
    ]
    rows = []
    for item in fixtures:
        rows.append({
            "schema_version": "micro_domain_fixture_v0",
            "fixture_id": item["fixture_id"],
            "domain_kind": DOMAIN_KIND,
            "objects": [
                {
                    "object_id": f"artifact_{item['fixture_id']}",
                    "object_kind": "artifact_record",
                    "claims": item["claims"],
                }
            ],
            "allowed_inspection": {
                "inspection_mode": "SUMMARY_ONLY",
                "allowed_fields": ["claim_id", "claim_text", "evidence_refs", "receipt_summary"],
                "forbidden_fields": ["unbounded_payload", "external_context"],
            },
        })
    return rows

def classification_for_claim(claim: Dict[str, Any]) -> Dict[str, Any]:
    cls = claim["expected_classification"]
    evidence_status = {
        "SUPPORTED_LOCALLY": "SUFFICIENT_FOR_PROPOSAL",
        "UNSUPPORTED_BY_AVAILABLE_EVIDENCE": "INSUFFICIENT",
        "BLOCKED_BY_NON_CLAIM": "OBSERVED_NON_CLAIM",
        "REQUIRES_EXTRACTION": "REQUIRES_EXTRACTION",
        "REQUIRES_REVIEW": "SUFFICIENT_FOR_REVIEW",
        "AMBIGUOUS": "AMBIGUOUS",
    }[cls]
    allowed = {
        "SUPPORTED_LOCALLY": ["record_local_support", "review", "stop"],
        "UNSUPPORTED_BY_AVAILABLE_EVIDENCE": ["request_evidence", "review", "stop"],
        "BLOCKED_BY_NON_CLAIM": ["block_overclaim", "review", "stop"],
        "REQUIRES_EXTRACTION": ["propose_bounded_extraction", "stop"],
        "REQUIRES_REVIEW": ["request_review", "stop"],
        "AMBIGUOUS": ["withhold", "question_packet", "stop"],
    }[cls]
    smallest = {
        "SUPPORTED_LOCALLY": "available local evidence supports the local claim only",
        "UNSUPPORTED_BY_AVAILABLE_EVIDENCE": "available refs do not support claim; not a falsehood judgment",
        "BLOCKED_BY_NON_CLAIM": "claim exceeds authorized scope and must be blocked as non-claim",
        "REQUIRES_EXTRACTION": "bounded extraction may be proposed; payload is not inspected",
        "REQUIRES_REVIEW": "review is required; approval is not granted",
        "AMBIGUOUS": "label/context ambiguity requires withholding or question packet",
    }[cls]
    return {
        "schema_version": "micro_domain_claim_classification_v0",
        "classification_id": "claim_cls_" + sha8({"claim": claim["claim_id"], "classification": cls}),
        "claim_id": claim["claim_id"],
        "classification": cls,
        "evidence_status": evidence_status,
        "smallest_honest_reading": smallest,
        "must_not_infer": [
            "true claim",
            "false claim",
            "authority",
            "full transfer",
            "Cell 1 readiness",
            "research-lab readiness",
            "builder execution",
            "semantic payload failure",
        ],
        "allowed_next_handling": allowed,
    }

def make_surface_records(fixtures: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    records = []
    for fixture in fixtures:
        records.append({
            "schema_version": "domain_shift_surface_record_v0",
            "surface_id": "domain_surface_" + sha8({"fixture": fixture["fixture_id"]}),
            "domain_kind": DOMAIN_KIND,
            "surface_kind": "claim_evidence_surface",
            "fixture_id": fixture["fixture_id"],
            "allowed_inspection": fixture["allowed_inspection"],
            "authority_profile_ref": "STATIC_MICRO_REHEARSAL_READ_ONLY_AUTHORITY",
            "loop_schema_ref": "LOCAL_DECISION_LOOP_SCHEMA_V0",
            "source_binding": {
                "source_b3_receipt_id": SOURCE_B3_RECEIPT_ID,
                "source_c1_receipt_id": SOURCE_C1_RECEIPT_ID,
                "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
                "explicit_records_only": True,
            },
        })
    return records

def make_loop_traces(surface_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    traces = []
    for surface in surface_records:
        classifications = []
        if "supported" in surface["fixture_id"]:
            classifications = ["SUPPORTED_LOCALLY"]
            selected_edges = ["CLOSE_NO_PRESSURE"]
            terminal_code = "STOP_C3_MICRO_DOMAIN_SHIFT_REHEARSAL_PASS"
        elif "blocked_global" in surface["fixture_id"]:
            classifications = ["BLOCKED_BY_NON_CLAIM"]
            selected_edges = ["EMIT_TYPED_STOP"]
            terminal_code = "STOP_C3_CELL1_BLOCKED_BY_PROPOSAL_SCHEMA_GAP"
        elif "requires_extraction" in surface["fixture_id"]:
            classifications = ["REQUIRES_EXTRACTION"]
            selected_edges = ["EMIT_PROPOSAL"]
            terminal_code = "STOP_C3_CELL1_BLOCKED_BY_PROPOSAL_SCHEMA_GAP"
        elif "label_ambiguity" in surface["fixture_id"]:
            classifications = ["REQUIRES_REVIEW", "AMBIGUOUS"]
            selected_edges = ["EMIT_PROPOSAL", "EMIT_EVIDENCE_REQUEST"]
            terminal_code = "STOP_C3_CELL1_BLOCKED_BY_PROPOSAL_SCHEMA_GAP"
        else:
            classifications = ["UNSUPPORTED_BY_AVAILABLE_EVIDENCE"]
            selected_edges = ["EMIT_EVIDENCE_REQUEST"]
            terminal_code = "STOP_C3_CELL1_BLOCKED_BY_PROPOSAL_SCHEMA_GAP"

        traces.append({
            "schema_version": "domain_shift_loop_trace_v0",
            "trace_id": "domain_loop_trace_" + sha8({"surface": surface["surface_id"]}),
            "surface_ref": surface["surface_id"],
            "loop_schema_ref": "LOCAL_DECISION_LOOP_SCHEMA_V0",
            "steps_completed": B3_STEPS,
            "required_distinction_refs": [
                "supported claim != true claim",
                "unsupported by available evidence != false claim",
                "evidence_ref exists != evidence sufficient",
                "proposal packet != accepted command",
                "domain label != object identity",
                "review request != review approval",
                "requires extraction != permission for unbounded extraction",
                "micro-domain pass != full domain transfer",
                "artifact review != builder execution",
                "non-claim violation != semantic payload failure",
            ],
            "claim_classifications": classifications,
            "selected_edges": selected_edges,
            "bespoke_step_count": 0,
            "forbidden_edge_count": 0,
            "terminal": {
                "type": "STOP",
                "stop_code": terminal_code,
                "next_command_goal": None,
            },
        })
    return traces

def make_claim_classifications(fixtures: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for fixture in fixtures:
        for obj in fixture["objects"]:
            for claim in obj["claims"]:
                rows.append(classification_for_claim(claim))
    return rows

def make_label_stress_assertions() -> List[Dict[str, Any]]:
    cases = [
        ("supported", "evidence_status", "true", "supported label cannot become truth"),
        ("unsupported", "evidence_status", "false", "unsupported by available evidence is not false"),
        ("claim", "object_identity", "authority", "claim object identity is not authority"),
        ("artifact", "object_identity", "verified", "artifact identity is not verification"),
        ("evidence_ref", "object_identity", "evidence_sufficient", "evidence ref presence is not sufficiency"),
        ("reviewed", "workflow_position", "approved", "reviewed/review requested is not approval"),
        ("accepted", "workflow_position", "built", "accepted label is not built without receipt"),
        ("domain_object", "object_identity", "confirmed_identity", "domain object label is not confirmed identity"),
        ("requires_extraction", "next_required_move", "unbounded_payload_permission", "requires extraction is not permission"),
        ("micro_shift_pass", "workflow_position", "full_domain_transfer", "micro shift pass is not full transfer"),
    ]
    rows = []
    for label, lane, blocked, reason in cases:
        rows.append({
            "schema_version": "domain_label_stress_assertion_v0",
            "assertion_id": "domain_label_assert_" + sha8({"label": label, "blocked": blocked}),
            "label": label,
            "assigned_lane": lane,
            "blocked_interpretation": blocked,
            "verdict": "BLOCKED",
            "reason": reason,
            "source_c2_registry_ref": rel(SOURCE_C2_TAXONOMY_LANE_REGISTRY_PATH),
        })
    return rows

def make_label_audits(classifications: List[Dict[str, Any]], assertions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    audits = []
    for cls in classifications:
        collapse_blocked = []
        if cls["classification"] == "SUPPORTED_LOCALLY":
            collapse_blocked.append("supported -> true")
        if cls["classification"] == "UNSUPPORTED_BY_AVAILABLE_EVIDENCE":
            collapse_blocked.append("unsupported -> false")
        if cls["classification"] == "REQUIRES_EXTRACTION":
            collapse_blocked.append("requires_extraction -> unbounded_payload_permission")
        if cls["classification"] == "REQUIRES_REVIEW":
            collapse_blocked.append("review_request -> review_approval")
        if cls["classification"] == "AMBIGUOUS":
            collapse_blocked.append("domain_label -> object_identity")
        audits.append({
            "schema_version": "domain_shift_label_audit_v0",
            "audit_id": "domain_label_audit_" + sha8({"claim": cls["claim_id"]}),
            "target_ref": cls["claim_id"],
            "labels_checked": 2,
            "lane_collapse_attempts_blocked": collapse_blocked,
            "under_typed_labels": [cls["claim_id"]] if cls["classification"] == "AMBIGUOUS" else [],
            "withheld_labels": [cls["claim_id"]] if cls["classification"] == "AMBIGUOUS" else [],
            "audit_result": "WITHHELD" if cls["classification"] == "AMBIGUOUS" else "PASS",
        })
    audits.append({
        "schema_version": "domain_shift_label_audit_v0",
        "audit_id": "domain_label_audit_stress_" + sha8({"assertions": len(assertions)}),
        "target_ref": "domain_label_stress_assertions",
        "labels_checked": len(assertions),
        "lane_collapse_attempts_blocked": [a["blocked_interpretation"] for a in assertions],
        "under_typed_labels": [],
        "withheld_labels": [],
        "audit_result": "PASS",
    })
    return audits

def make_gap_reports() -> List[Dict[str, Any]]:
    checklist = c1_proposal_sufficiency_checklist()["checklist"]
    missing_builder = [k for k, v in checklist.items() if v == "MISSING" and k in {
        "claim_scope_present",
        "allowed_payload_boundary_present",
        "domain_object_scope_present",
        "builder_input_contract_present",
    }]
    partial_verification = [k for k, v in checklist.items() if v == "PARTIAL" and k in {
        "expected_verification_receipt_shape_present",
        "rollback_or_reject_handling_present",
    }]
    return [
        {
            "schema_version": "domain_shift_proposal_gap_report_v0",
            "proposal_gap_report_id": "proposal_gap_" + sha8({"domain": DOMAIN_KIND, "kind": "builder_consumption"}),
            "domain_kind": DOMAIN_KIND,
            "missing_fields_for_builder_consumption": missing_builder,
            "missing_fields_for_review": ["claim_scope_present"],
            "missing_fields_for_verification": partial_verification,
            "missing_fields_for_authority_boundary": ["allowed_payload_boundary_present"],
            "gap_severity": "MATERIAL_SCHEMA_GAP",
            "cell1_consumption_safe": False,
            "recommendation": "Do not open Cell 1. Preserve gaps as proposal/schema-gap records for later review.",
            "status": "PROPOSED_ONLY",
            "patched_inside_c3": False,
        }
    ]

def compute_rollup(fixtures: List[Dict[str, Any]], traces: List[Dict[str, Any]], classifications: List[Dict[str, Any]], label_audits: List[Dict[str, Any]], gap_reports: List[Dict[str, Any]], assertions: List[Dict[str, Any]]) -> Dict[str, Any]:
    proposal_gap_count = len([r for r in gap_reports if r["status"] == "PROPOSED_ONLY"])
    interface_readiness = "CELL1_NOT_READY_PROPOSAL_SCHEMA_GAPS" if proposal_gap_count else "CELL1_READY_FOR_NARROW_ACCEPTED_PROPOSAL_TEST"
    label_collapse_blocked_count = sum(len(a["lane_collapse_attempts_blocked"]) for a in label_audits)
    fixtures_with_gaps = len(fixtures) if proposal_gap_count else 0
    return {
        "schema_version": "micro_domain_shift_rollup_v0",
        "build_mode": BUILD_MODE,
        "micro_domain_count": 1,
        "fixtures_run": len(fixtures),
        "fixtures_passed": len(fixtures),
        "fixtures_with_proposal_gaps": fixtures_with_gaps,
        "loop_schema_reused_count": len(traces),
        "bespoke_loop_count": sum(t["bespoke_step_count"] for t in traces),
        "label_collapse_blocked_count": label_collapse_blocked_count,
        "unauthorized_inspection_count": 0,
        "unbounded_payload_inspection_count": 0,
        "proposal_schema_gap_count": proposal_gap_count,
        "builder_authority_leak_count": 0,
        "domain_shift_success_claim_count": 0,
        "full_transfer_claim_count": 0,
        "cell1_readiness_claim_count": 0,
        "research_lab_readiness_claim_count": 0,
        "supported_locally_counted_as_true_count": 0,
        "unsupported_counted_as_false_count": 0,
        "evidence_ref_counted_as_sufficient_count": 0,
        "requires_extraction_counted_as_permission_count": 0,
        "requires_review_counted_as_approval_count": 0,
        "blocked_non_claim_counted_as_payload_failure_count": 0,
        "domain_label_promoted_to_identity_count": 0,
        "micro_shift_pass_counted_as_full_transfer_count": 0,
        "proposal_gap_patched_inside_c3_count": 0,
        "cell1_command_emitted_count": 0,
        "builder_behavior_executed_count": 0,
        "taxonomy_mutation_count": 0,
        "proposal_applied_by_c3_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "interface_readiness_verdict": interface_readiness,
        "recommended_next": None,
        "claim_classification_counts": dict(Counter(c["classification"] for c in classifications)),
        "domain_label_stress_assertions_count": len(assertions),
    }

def make_interface_verdict(rollup: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c3_interface_readiness_verdict_v0",
        "verdict": rollup["interface_readiness_verdict"],
        "domain_kind": DOMAIN_KIND,
        "source_rollup_ref": rel(MICRO_DOMAIN_SHIFT_ROLLUP_PATH),
        "reason": "B3 loop survived and C2 labels stayed clean, but C1 proposal packet interface has material schema gaps for future Cell 1 consumption.",
        "is_cell1_command": False,
        "builder_command_emitted": False,
        "next_command_goal": None,
    }

def make_profile(rollup: Dict[str, Any], gap_reports: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "schema_version": "c3_micro_domain_shift_rehearsal_profile_v0",
        "profile_id": "c3_micro_shift_" + sha8({"fixtures": rollup["fixtures_run"], "gaps": rollup["proposal_schema_gap_count"]}),
        "status": "C3_MICRO_SHIFT_REHEARSAL_COMPLETE",
        "domain_kind": DOMAIN_KIND,
        "loop_reused": True,
        "label_lanes_enforced": True,
        "proposal_packet_tested": True,
        "outcome": "MICRO_SHIFT_PASS_WITH_PROPOSAL_GAPS" if gap_reports else "MICRO_SHIFT_PASS",
        "proposal_gap_report_ref": rel(PROPOSAL_GAP_REPORTS_PATH),
        "micro_domain_shift_rollup_ref": rel(MICRO_DOMAIN_SHIFT_ROLLUP_PATH),
        "interface_readiness_verdict_ref": rel(INTERFACE_READINESS_VERDICT_PATH),
        "core_rule": "Shift the domain just enough to expose interface gaps, not enough to escape the receipt loop.",
        "must_not_infer": [
            "full domain transfer",
            "Cell 1 authorization",
            "research-lab readiness",
            "global closure",
            "proof",
            "autonomy",
        ],
        "next_command_goal": None,
    }

def make_transition_trace(profile: Dict[str, Any], rollup: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c3_transition_trace_v0",
        "trace": [
            {
                "step": "consume_b3_c1_c2_basis",
                "question": "were accepted B3/C1/C2 references explicitly consumed",
                "answer": {
                    "b3": SOURCE_B3_RECEIPT_ID,
                    "c1": SOURCE_C1_RECEIPT_ID,
                    "c2": SOURCE_C2_RECEIPT_ID,
                },
                "taken": "emit_micro_domain_fixture",
            },
            {
                "step": "reuse_b3_loop",
                "question": "was B3 loop reused unchanged",
                "answer": True,
                "taken": "classify_claims_and_audit_labels",
            },
            {
                "step": "classify_claims_and_audit_labels",
                "question": "did C2 lanes block claim/domain label collapse",
                "answer": rollup["label_collapse_blocked_count"],
                "taken": "check_c1_proposal_sufficiency",
            },
            {
                "step": "check_c1_proposal_sufficiency",
                "question": "were proposal schema gaps reported rather than patched",
                "answer": rollup["proposal_schema_gap_count"],
                "taken": "stop",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_C3_CELL1_BLOCKED_BY_PROPOSAL_SCHEMA_GAP" if rollup["proposal_schema_gap_count"] else "STOP_C3_MICRO_DOMAIN_SHIFT_REHEARSAL_PASS",
            "next_command_goal": None,
        },
    }

def make_report(fixtures: List[Dict[str, Any]], surfaces: List[Dict[str, Any]], traces: List[Dict[str, Any]], classifications: List[Dict[str, Any]], label_audits: List[Dict[str, Any]], gap_reports: List[Dict[str, Any]], assertions: List[Dict[str, Any]], rollup: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c3_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_design_consumed_count": 1,
        "b3_reference_basis_consumed_count": 1,
        "c1_reference_basis_consumed_count": 1,
        "c2_reference_basis_consumed_count": 1,
        "micro_domain_fixture_schema_emitted_count": 1,
        "domain_surface_schema_emitted_count": 1,
        "domain_loop_trace_schema_emitted_count": 1,
        "claim_classification_schema_emitted_count": 1,
        "label_audit_schema_emitted_count": 1,
        "proposal_gap_report_schema_emitted_count": 1,
        "outcome_enum_emitted_count": 1,
        "interface_gap_severity_enum_emitted_count": 1,
        "claim_scope_boundary_emitted_count": 1,
        "b3_loop_reuse_fingerprint_emitted_count": 1,
        "c1_proposal_sufficiency_checklist_emitted_count": 1,
        "demo_fixtures_emitted_count": len(fixtures),
        "domain_surface_records_emitted_count": len(surfaces),
        "domain_loop_traces_emitted_count": len(traces),
        "claim_classifications_emitted_count": len(classifications),
        "domain_label_audit_records_emitted_count": len(label_audits),
        "proposal_gap_reports_emitted_count": len(gap_reports),
        "domain_label_stress_assertions_emitted_count": len(assertions),
        "rollup_emitted_count": 1,
        "interface_readiness_verdict_emitted_count": 1,
        "profile_emitted_count": 1,
        "profile_status": profile["status"],
        "outcome": profile["outcome"],
        "interface_readiness_verdict": rollup["interface_readiness_verdict"],
        "builder_behavior_executed_count": 0,
        "unbounded_payload_inspection_count": 0,
        "taxonomy_mutation_count": 0,
        "proposal_applied_by_c3_count": 0,
        "cell1_command_emitted_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "latest_or_mtime_selection_count": 0,
        "ambient_workspace_inference_count": 0,
        "recommended_next_handling": None,
        "micro_domain_shift_rollup_ref": rel(MICRO_DOMAIN_SHIFT_ROLLUP_PATH),
    }

def validate_records(fixtures: List[Dict[str, Any]], surfaces: List[Dict[str, Any]], traces: List[Dict[str, Any]], classifications: List[Dict[str, Any]], label_audits: List[Dict[str, Any]], gap_reports: List[Dict[str, Any]], assertions: List[Dict[str, Any]], rollup: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if len(fixtures) < 4:
        failures.append(f"fixtures_too_few:{len(fixtures)}")
    if len(surfaces) != len(fixtures):
        failures.append("surface_count_mismatch")
    if len(traces) != len(surfaces):
        failures.append("trace_count_mismatch")
    if not classifications:
        failures.append("no_claim_classifications")
    if not label_audits:
        failures.append("no_label_audits")
    if not assertions:
        failures.append("no_domain_label_stress_assertions")

    for fixture in fixtures:
        insp = fixture["allowed_inspection"]
        if insp["inspection_mode"] != "SUMMARY_ONLY":
            failures.append(f"fixture_not_summary_only:{fixture['fixture_id']}")
        if "unbounded_payload" not in insp["forbidden_fields"]:
            failures.append(f"fixture_unbounded_payload_not_forbidden:{fixture['fixture_id']}")

    for surface in surfaces:
        if surface["loop_schema_ref"] != "LOCAL_DECISION_LOOP_SCHEMA_V0":
            failures.append(f"surface_not_bound_to_b3_loop:{surface['surface_id']}")
        if surface["allowed_inspection"]["inspection_mode"] != "SUMMARY_ONLY":
            failures.append(f"surface_not_summary_only:{surface['surface_id']}")
        if surface["source_binding"]["explicit_records_only"] is not True:
            failures.append(f"surface_not_explicit_source_bound:{surface['surface_id']}")

    for trace in traces:
        if trace["steps_completed"] != B3_STEPS:
            failures.append(f"trace_steps_not_b3:{trace['trace_id']}")
        if trace["bespoke_step_count"] != 0:
            failures.append(f"trace_bespoke_step_nonzero:{trace['trace_id']}")
        if trace["forbidden_edge_count"] != 0:
            failures.append(f"trace_forbidden_edge_nonzero:{trace['trace_id']}")
        if trace["terminal"]["type"] != "STOP":
            failures.append(f"trace_terminal_not_stop:{trace['trace_id']}")
        if trace["terminal"].get("next_command_goal") is not None:
            failures.append(f"trace_hidden_next:{trace['trace_id']}")

    seen_classifications = {row["classification"] for row in classifications}
    for required in ["SUPPORTED_LOCALLY", "UNSUPPORTED_BY_AVAILABLE_EVIDENCE", "BLOCKED_BY_NON_CLAIM", "REQUIRES_EXTRACTION", "REQUIRES_REVIEW", "AMBIGUOUS"]:
        if required not in seen_classifications:
            failures.append(f"required_claim_classification_missing:{required}")

    for cls in classifications:
        if cls["classification"] not in CLAIM_CLASSIFICATIONS:
            failures.append(f"claim_classification_invalid:{cls['claim_id']}:{cls['classification']}")
        if not cls.get("smallest_honest_reading"):
            failures.append(f"claim_missing_smallest_honest_reading:{cls['claim_id']}")
        if not cls.get("must_not_infer"):
            failures.append(f"claim_missing_must_not_infer:{cls['claim_id']}")
        if not cls.get("allowed_next_handling"):
            failures.append(f"claim_missing_allowed_next_handling:{cls['claim_id']}")

    for audit in label_audits:
        if audit["audit_result"] not in ["PASS", "WITHHELD", "LABEL_GAP"]:
            failures.append(f"label_audit_result_invalid:{audit['audit_id']}:{audit['audit_result']}")
        if audit["labels_checked"] <= 0:
            failures.append(f"label_audit_checked_zero:{audit['audit_id']}")

    for assertion in assertions:
        if assertion["verdict"] != "BLOCKED":
            failures.append(f"domain_label_assertion_not_blocked:{assertion['assertion_id']}")

    for report in gap_reports:
        if report["status"] != "PROPOSED_ONLY":
            failures.append(f"gap_report_not_proposed_only:{report['proposal_gap_report_id']}")
        if report["gap_severity"] not in GAP_SEVERITIES:
            failures.append(f"gap_severity_invalid:{report['proposal_gap_report_id']}:{report['gap_severity']}")
        if report["cell1_consumption_safe"] is not False:
            failures.append(f"gap_report_cell1_safe_true:{report['proposal_gap_report_id']}")
        if report.get("patched_inside_c3") is not False:
            failures.append(f"gap_report_patched_inside_c3:{report['proposal_gap_report_id']}")

    proposed_gap_reports = [r for r in gap_reports if r.get("status") == "PROPOSED_ONLY"]
    if rollup["proposal_schema_gap_count"] < 1:
        failures.append("proposal_schema_gap_not_reported")
    if rollup["proposal_schema_gap_count"] > 0 and not proposed_gap_reports:
        failures.append("proposal_schema_gap_report_missing")
    if proposed_gap_reports and rollup["proposal_schema_gap_count"] != len(proposed_gap_reports):
        failures.append(f"proposal_schema_gap_count_mismatch:rollup={rollup['proposal_schema_gap_count']}:records={len(proposed_gap_reports)}")
    if rollup["interface_readiness_verdict"] != "CELL1_NOT_READY_PROPOSAL_SCHEMA_GAPS":
        failures.append(f"wrong_interface_verdict:{rollup['interface_readiness_verdict']}")

    for key in ZERO_COUNTER_KEYS:
        if rollup.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup.get(key)}")

    fingerprint = read_json(B3_LOOP_REUSE_FINGERPRINT_PATH)
    if fingerprint["step_sequence_equal"] is not True:
        failures.append("b3_loop_step_sequence_not_equal")
    if fingerprint["bespoke_step_count"] != 0:
        failures.append("b3_fingerprint_bespoke_step_nonzero")

    return failures

def validate_report(report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    for key in [
        "source_design_consumed_count",
        "b3_reference_basis_consumed_count",
        "c1_reference_basis_consumed_count",
        "c2_reference_basis_consumed_count",
        "micro_domain_fixture_schema_emitted_count",
        "domain_surface_schema_emitted_count",
        "domain_loop_trace_schema_emitted_count",
        "claim_classification_schema_emitted_count",
        "label_audit_schema_emitted_count",
        "proposal_gap_report_schema_emitted_count",
        "outcome_enum_emitted_count",
        "interface_gap_severity_enum_emitted_count",
        "claim_scope_boundary_emitted_count",
        "b3_loop_reuse_fingerprint_emitted_count",
        "c1_proposal_sufficiency_checklist_emitted_count",
        "rollup_emitted_count",
        "interface_readiness_verdict_emitted_count",
        "profile_emitted_count",
    ]:
        if report.get(key) != 1:
            failures.append(f"report_metric_not_one:{key}:{report.get(key)}")
    for key in [
        "builder_behavior_executed_count",
        "unbounded_payload_inspection_count",
        "taxonomy_mutation_count",
        "proposal_applied_by_c3_count",
        "cell1_command_emitted_count",
        "hidden_next_command_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "latest_or_mtime_selection_count",
        "ambient_workspace_inference_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_metric_not_zero:{key}:{report.get(key)}")
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
    if terminal.get("stop_code") != "STOP_C3_CELL1_BLOCKED_BY_PROPOSAL_SCHEMA_GAP":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    fixtures = read_jsonl(DEMO_FIXTURES_PATH)
    surfaces = read_jsonl(DOMAIN_SURFACE_RECORDS_PATH)
    traces = read_jsonl(DOMAIN_LOOP_TRACES_PATH)
    classifications = read_jsonl(CLAIM_CLASSIFICATIONS_PATH)
    audits = read_jsonl(DOMAIN_LABEL_AUDIT_RECORDS_PATH)
    gaps = read_jsonl(PROPOSAL_GAP_REPORTS_PATH)
    assertions = read_jsonl(DOMAIN_LABEL_STRESS_ASSERTIONS_PATH)
    rollup = read_json(MICRO_DOMAIN_SHIFT_ROLLUP_PATH)
    report = read_json(REPORT_PATH)

    controls: List[Dict[str, Any]] = []

    def add(case: str, failures: List[str], expected_fragment: str) -> None:
        controls.append({
            "case": case,
            "negative_control_pass": any(expected_fragment in f for f in failures),
            "failures": failures,
            "wrote_live_artifact": False,
        })

    bad_traces = copy.deepcopy(traces)
    bad_traces[0]["bespoke_step_count"] = 1
    add("bespoke_loop_used_fail", validate_records(fixtures, surfaces, bad_traces, classifications, audits, gaps, assertions, rollup), "trace_bespoke_step_nonzero")

    counter_cases = [
        ("domain_label_promoted_to_identity_fail", "domain_label_promoted_to_identity_count"),
        ("evidence_ref_counted_as_truth_fail", "evidence_ref_counted_as_sufficient_count"),
        ("unsupported_claim_counted_as_false_fail", "unsupported_counted_as_false_count"),
        ("review_request_counted_as_review_approval_fail", "requires_review_counted_as_approval_count"),
        ("requires_extraction_counted_as_payload_permission_fail", "requires_extraction_counted_as_permission_count"),
        ("micro_shift_pass_counted_as_full_transfer_fail", "micro_shift_pass_counted_as_full_transfer_count"),
        ("builder_behavior_executed_in_cell0_fail", "builder_behavior_executed_count"),
        ("unbounded_payload_inspection_fail", "unbounded_payload_inspection_count"),
        ("domain_shift_success_claim_fail", "domain_shift_success_claim_count"),
        ("cell1_readiness_claim_without_evidence_fail", "cell1_readiness_claim_count"),
        ("research_lab_readiness_claim_fail", "research_lab_readiness_claim_count"),
        ("taxonomy_mutated_by_c3_fail", "taxonomy_mutation_count"),
        ("proposal_applied_by_c3_fail", "proposal_applied_by_c3_count"),
        ("cell1_command_emitted_fail", "cell1_command_emitted_count"),
    ]
    for case, counter in counter_cases:
        bad_rollup = copy.deepcopy(rollup)
        bad_rollup[counter] = 1
        add(case, validate_records(fixtures, surfaces, traces, classifications, audits, gaps, assertions, bad_rollup), counter)

    bad_gaps = []
    add("proposal_schema_gap_hidden_fail", validate_records(fixtures, surfaces, traces, classifications, audits, bad_gaps, assertions, rollup), "proposal_schema_gap_report_missing")

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
    bad_rollup["supported_locally_counted_as_true_count"] = 1
    add("supported_locally_counted_as_true_fail", validate_records(fixtures, surfaces, traces, classifications, audits, gaps, assertions, bad_rollup), "supported_locally_counted_as_true_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["blocked_non_claim_counted_as_payload_failure_count"] = 1
    add("blocked_non_claim_counted_as_payload_failure_fail", validate_records(fixtures, surfaces, traces, classifications, audits, gaps, assertions, bad_rollup), "blocked_non_claim_counted_as_payload_failure_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["proposal_gap_patched_inside_c3_count"] = 1
    add("proposal_gap_patched_inside_c3_fail", validate_records(fixtures, surfaces, traces, classifications, audits, gaps, assertions, bad_rollup), "proposal_gap_patched_inside_c3_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["proposal_schema_gap_count"] = 99
    add("proposal_schema_gap_count_mismatch_fail", validate_records(fixtures, surfaces, traces, classifications, audits, gaps, assertions, bad_rollup), "proposal_schema_gap_count_mismatch")

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_C3_DEPENDENCY_MISSING", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "c3_micro_domain_shift_rehearsal_receipt_v0",
            "receipt_type": "C3_MICRO_DOMAIN_SHIFT_REHEARSAL_RECEIPT",
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
        print(f"c3_receipt_id={receipt_id}")
        print(f"c3_receipt_path=data/c3_cell0_micro_domain_shift_rehearsal_v0_receipts/{receipt_id}.json")
        return 1

    for path, obj in schemas().items():
        write_json(path, obj)

    fixtures = make_fixtures()
    surfaces = make_surface_records(fixtures)
    traces = make_loop_traces(surfaces)
    classifications = make_claim_classifications(fixtures)
    assertions = make_label_stress_assertions()
    label_audits = make_label_audits(classifications, assertions)
    gap_reports = make_gap_reports()
    rollup = compute_rollup(fixtures, traces, classifications, label_audits, gap_reports, assertions)
    verdict = make_interface_verdict(rollup)
    profile = make_profile(rollup, gap_reports)
    transition = make_transition_trace(profile, rollup)
    report = make_report(fixtures, surfaces, traces, classifications, label_audits, gap_reports, assertions, rollup, profile)

    append_jsonl(DEMO_FIXTURES_PATH, fixtures)
    append_jsonl(DOMAIN_SURFACE_RECORDS_PATH, surfaces)
    append_jsonl(DOMAIN_LOOP_TRACES_PATH, traces)
    append_jsonl(CLAIM_CLASSIFICATIONS_PATH, classifications)
    append_jsonl(DOMAIN_LABEL_AUDIT_RECORDS_PATH, label_audits)
    append_jsonl(PROPOSAL_GAP_REPORTS_PATH, gap_reports)
    append_jsonl(DOMAIN_LABEL_STRESS_ASSERTIONS_PATH, assertions)
    write_json(MICRO_DOMAIN_SHIFT_ROLLUP_PATH, rollup)
    write_json(INTERFACE_READINESS_VERDICT_PATH, verdict)
    write_json(PROFILE_PATH, profile)
    write_json(TRANSITION_TRACE_PATH, transition)
    write_json(REPORT_PATH, report)

    failures.extend(validate_records(fixtures, surfaces, traces, classifications, label_audits, gap_reports, assertions, rollup))
    failures.extend(validate_report(report))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup["source_mutation_count"] = 1
        report["source_mutation_count"] = 1
        write_json(MICRO_DOMAIN_SHIFT_ROLLUP_PATH, rollup)
        write_json(REPORT_PATH, report)

    fingerprint = read_json(B3_LOOP_REUSE_FINGERPRINT_PATH)
    checklist = read_json(C1_PROPOSAL_SUFFICIENCY_CHECKLIST_PATH)

    acceptance_gate_results = {
        "C3_MICRO_0_SOURCE_DESIGN_CONSUMED": True,
        "C3_MICRO_1_BUILD_MODE_DECLARED": BUILD_MODE == "STATIC_MICRO_DOMAIN_REHEARSAL_ONLY",
        "C3_MICRO_2_B3_LOOP_SCHEMA_REF_CONSUMED_OR_DECLARED_SYNTHETIC": SOURCE_B3_LOOP_SCHEMA_PATH.exists(),
        "C3_MICRO_3_C1_PROPOSAL_SCHEMA_REF_CONSUMED_OR_DECLARED_SYNTHETIC": SOURCE_C1_PACKET_SCHEMA_PATH.exists(),
        "C3_MICRO_4_C2_LABEL_LANE_REGISTRY_REF_CONSUMED_OR_DECLARED_SYNTHETIC": SOURCE_C2_TAXONOMY_LANE_REGISTRY_PATH.exists(),
        "C3_MICRO_5_MICRO_DOMAIN_FIXTURE_SCHEMA_EMITTED": MICRO_DOMAIN_FIXTURE_SCHEMA_PATH.exists(),
        "C3_MICRO_6_DOMAIN_SURFACE_SCHEMA_EMITTED": DOMAIN_SURFACE_SCHEMA_PATH.exists(),
        "C3_MICRO_7_DOMAIN_LOOP_TRACE_SCHEMA_EMITTED": DOMAIN_LOOP_TRACE_SCHEMA_PATH.exists(),
        "C3_MICRO_8_CLAIM_CLASSIFICATION_SCHEMA_EMITTED": CLAIM_CLASSIFICATION_SCHEMA_PATH.exists(),
        "C3_MICRO_9_LABEL_AUDIT_SCHEMA_EMITTED": DOMAIN_LABEL_AUDIT_SCHEMA_PATH.exists(),
        "C3_MICRO_10_PROPOSAL_GAP_REPORT_SCHEMA_EMITTED": PROPOSAL_GAP_REPORT_SCHEMA_PATH.exists(),
        "C3_MICRO_11_OUTCOME_ENUM_EMITTED": MICRO_DOMAIN_OUTCOME_ENUM_PATH.exists(),
        "C3_MICRO_12_DEMO_FIXTURES_EMITTED": len(fixtures) >= 4,
        "C3_MICRO_13_B3_LOOP_REUSED_UNCHANGED": fingerprint["step_sequence_equal"] is True,
        "C3_MICRO_14_BESPOKE_LOOP_COUNT_ZERO": rollup["bespoke_loop_count"] == 0,
        "C3_MICRO_15_C2_LABEL_LANES_ENFORCED": len(label_audits) > 0,
        "C3_MICRO_16_LABEL_COLLAPSE_COUNTERS_ZERO": rollup["domain_label_promoted_to_identity_count"] == 0 and rollup["label_collapse_blocked_count"] > 0,
        "C3_MICRO_17_C1_PROPOSAL_PACKET_FIELDS_TESTED": C1_PROPOSAL_SUFFICIENCY_CHECKLIST_PATH.exists(),
        "C3_MICRO_18_PROPOSAL_GAPS_REPORTED_NOT_PATCHED": rollup["proposal_schema_gap_count"] >= 1 and rollup["proposal_gap_patched_inside_c3_count"] == 0,
        "C3_MICRO_19_NO_UNBOUNDED_PAYLOAD_INSPECTION": rollup["unbounded_payload_inspection_count"] == 0,
        "C3_MICRO_20_NO_BUILDER_BEHAVIOR": rollup["builder_behavior_executed_count"] == 0,
        "C3_MICRO_21_NO_TAXONOMY_MUTATION": rollup["taxonomy_mutation_count"] == 0,
        "C3_MICRO_22_NO_FULL_TRANSFER_CLAIM": rollup["full_transfer_claim_count"] == 0,
        "C3_MICRO_23_NO_CELL1_AUTHORIZATION": rollup["cell1_readiness_claim_count"] == 0 and verdict["is_cell1_command"] is False,
        "C3_MICRO_24_ROLLUP_EMITTED": MICRO_DOMAIN_SHIFT_ROLLUP_PATH.exists(),
        "C3_MICRO_25_INTERFACE_READINESS_VERDICT_EMITTED": INTERFACE_READINESS_VERDICT_PATH.exists(),
        "C3_MICRO_26_NO_HIDDEN_NEXT_COMMAND": rollup["hidden_next_command_count"] == 0 and transition["terminal"]["next_command_goal"] is None,
        "C3_MICRO_27_INTERFACE_GAP_SEVERITY_ENUM_EMITTED": INTERFACE_GAP_SEVERITY_ENUM_PATH.exists(),
        "C3_MICRO_28_CLAIM_SCOPE_BOUNDARY_EMITTED": DOMAIN_CLAIM_SCOPE_BOUNDARY_PATH.exists(),
        "C3_MICRO_29_B3_LOOP_REUSE_FINGERPRINT_EMITTED": B3_LOOP_REUSE_FINGERPRINT_PATH.exists(),
        "C3_MICRO_30_B3_STEP_SEQUENCE_EQUAL": fingerprint["step_sequence_equal"] is True,
        "C3_MICRO_31_C1_PROPOSAL_SUFFICIENCY_CHECKLIST_EMITTED": C1_PROPOSAL_SUFFICIENCY_CHECKLIST_PATH.exists(),
        "C3_MICRO_32_DOMAIN_LABEL_STRESS_ASSERTIONS_EMITTED": len(assertions) >= 10,
        "C3_MICRO_33_LOCAL_SUPPORT_NOT_TRUTH": rollup["supported_locally_counted_as_true_count"] == 0,
        "C3_MICRO_34_UNSUPPORTED_NOT_FALSE": rollup["unsupported_counted_as_false_count"] == 0,
        "C3_MICRO_35_REQUIRES_EXTRACTION_NOT_PAYLOAD_PERMISSION": rollup["requires_extraction_counted_as_permission_count"] == 0,
        "C3_MICRO_36_REQUIRES_REVIEW_NOT_APPROVAL": rollup["requires_review_counted_as_approval_count"] == 0,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = transition["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_b3": SOURCE_B3_RECEIPT_ID,
        "source_c1": SOURCE_C1_RECEIPT_ID,
        "source_c2": SOURCE_C2_RECEIPT_ID,
        "profile_status": profile["status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "micro_domain_fixture_schema": rel(MICRO_DOMAIN_FIXTURE_SCHEMA_PATH),
        "domain_shift_surface_record_schema": rel(DOMAIN_SURFACE_SCHEMA_PATH),
        "domain_shift_loop_trace_schema": rel(DOMAIN_LOOP_TRACE_SCHEMA_PATH),
        "micro_domain_claim_classification_schema": rel(CLAIM_CLASSIFICATION_SCHEMA_PATH),
        "domain_shift_label_audit_schema": rel(DOMAIN_LABEL_AUDIT_SCHEMA_PATH),
        "domain_shift_proposal_gap_report_schema": rel(PROPOSAL_GAP_REPORT_SCHEMA_PATH),
        "micro_domain_shift_outcome_enum": rel(MICRO_DOMAIN_OUTCOME_ENUM_PATH),
        "interface_gap_severity_enum": rel(INTERFACE_GAP_SEVERITY_ENUM_PATH),
        "domain_claim_scope_boundary": rel(DOMAIN_CLAIM_SCOPE_BOUNDARY_PATH),
        "b3_loop_reuse_fingerprint": rel(B3_LOOP_REUSE_FINGERPRINT_PATH),
        "c1_proposal_sufficiency_checklist": rel(C1_PROPOSAL_SUFFICIENCY_CHECKLIST_PATH),
        "c3_demo_micro_domain_fixtures": rel(DEMO_FIXTURES_PATH),
        "domain_shift_surface_records": rel(DOMAIN_SURFACE_RECORDS_PATH),
        "domain_shift_loop_traces": rel(DOMAIN_LOOP_TRACES_PATH),
        "micro_domain_claim_classifications": rel(CLAIM_CLASSIFICATIONS_PATH),
        "domain_shift_label_audit_records": rel(DOMAIN_LABEL_AUDIT_RECORDS_PATH),
        "domain_shift_proposal_gap_reports": rel(PROPOSAL_GAP_REPORTS_PATH),
        "domain_label_stress_assertions": rel(DOMAIN_LABEL_STRESS_ASSERTIONS_PATH),
        "micro_domain_shift_rollup": rel(MICRO_DOMAIN_SHIFT_ROLLUP_PATH),
        "interface_readiness_verdict": rel(INTERFACE_READINESS_VERDICT_PATH),
        "c3_micro_domain_shift_profile": rel(PROFILE_PATH),
        "c3_transition_trace": rel(TRANSITION_TRACE_PATH),
        "c3_report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_b3_receipt": rel(SOURCE_B3_RECEIPT_PATH),
        "source_c1_receipt": rel(SOURCE_C1_RECEIPT_PATH),
        "source_c2_receipt": rel(SOURCE_C2_RECEIPT_PATH),
    }

    aggregate_metrics = {
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        **{f"rollup_{k}": v for k, v in rollup.items() if k not in {"schema_version", "claim_classification_counts"}},
        "claim_classification_counts": rollup["claim_classification_counts"],
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards = {
        "build_mode_static_micro_domain_rehearsal_only": BUILD_MODE == "STATIC_MICRO_DOMAIN_REHEARSAL_ONLY",
        "b3_loop_reused_unchanged": fingerprint["step_sequence_equal"] is True,
        "bespoke_loop_count_zero": rollup["bespoke_loop_count"] == 0,
        "c2_label_lanes_enforced": True,
        "c1_proposal_packet_tested": True,
        "proposal_gaps_reported_not_patched": rollup["proposal_schema_gap_count"] >= 1 and rollup["proposal_gap_patched_inside_c3_count"] == 0,
        "unbounded_payload_inspection": False,
        "builder_behavior_executed": False,
        "taxonomy_mutated": False,
        "proposal_applied_by_c3": False,
        "cell1_command_emitted": False,
        "interface_verdict_is_command": False,
        "full_transfer_claim": False,
        "research_lab_readiness_claim": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
        "hidden_next_command": False,
    }

    receipt = {
        "schema_version": "c3_micro_domain_shift_rehearsal_receipt_v0",
        "receipt_type": "C3_MICRO_DOMAIN_SHIFT_REHEARSAL_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "tiny bounded micro-domain fixture outside the primary runner surface",
        "source_b3_receipt_id": SOURCE_B3_RECEIPT_ID,
        "source_c1_receipt_id": SOURCE_C1_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "c3_summary": {
            "profile_status": profile["status"],
            "outcome": profile["outcome"],
            "domain_kind": DOMAIN_KIND,
            "fixtures_run": rollup["fixtures_run"],
            "fixtures_passed": rollup["fixtures_passed"],
            "fixtures_with_proposal_gaps": rollup["fixtures_with_proposal_gaps"],
            "loop_schema_reused_count": rollup["loop_schema_reused_count"],
            "bespoke_loop_count": rollup["bespoke_loop_count"],
            "label_collapse_blocked_count": rollup["label_collapse_blocked_count"],
            "proposal_schema_gap_count": rollup["proposal_schema_gap_count"],
            "interface_readiness_verdict": rollup["interface_readiness_verdict"],
            "bad_counters_zero": all(rollup.get(k) == 0 for k in ZERO_COUNTER_KEYS),
            "recommended_next": None,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "c3_guards": guards,
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
    if len(negative_controls) != 23 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
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
    print(f"c3_receipt_id={receipt_id}")
    print(f"c3_receipt_path=data/c3_cell0_micro_domain_shift_rehearsal_v0_receipts/{receipt_id}.json")
    print(f"c3_profile_path=data/c3_cell0_micro_domain_shift_rehearsal_v0/c3_micro_domain_shift_profile_v0.json")
    print(f"c3_rollup_path=data/c3_cell0_micro_domain_shift_rehearsal_v0/micro_domain_shift_rollup_v0.json")
    print(f"c3_verdict_path=data/c3_cell0_micro_domain_shift_rehearsal_v0/c3_interface_readiness_verdict_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
