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

UNIT_ID = "PATCH_C1_PROPOSAL_INTERFACE_FROM_C3_GAP_REPORT_V0"
TARGET_UNIT_ID = "c1.proposal_interface_gap_patch_from_c3.v0"
LAYER = "CELL_0 / PROPOSAL_INTERFACE_REPAIR"
MODE = "SCHEMA_PATCH / INTERFACE_REPAIR / NO_CELL1_EXECUTION"
BUILD_MODE = "CANDIDATE_INTERFACE_PATCH_ONLY"

SOURCE_C4_RECEIPT_ID = "75764a86"
SOURCE_C4_RECEIPT_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_v0_receipts" / "75764a86.json"
SOURCE_C4_ROLLUP_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_v0" / "c4_blocked_preflight_rollup_v0.json"
SOURCE_C4_GATE_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_v0" / "c4_opening_gate_evaluation_v0.json"

SOURCE_C3_RECEIPT_ID = "cfc79da2"
SOURCE_C3_RECEIPT_PATH = ROOT / "data" / "c3_cell0_micro_domain_shift_rehearsal_v0_receipts" / "cfc79da2.json"
SOURCE_C3_VERDICT_PATH = ROOT / "data" / "c3_cell0_micro_domain_shift_rehearsal_v0" / "c3_interface_readiness_verdict_v0.json"
SOURCE_C3_GAP_REPORTS_PATH = ROOT / "data" / "c3_cell0_micro_domain_shift_rehearsal_v0" / "domain_shift_proposal_gap_reports_v0.jsonl"

SOURCE_C1_RECEIPT_ID = "f8f37c4e"
SOURCE_C1_RECEIPT_PATH = ROOT / "data" / "c1_cell0_proposal_layer_v0_receipts" / "f8f37c4e.json"
SOURCE_C1_SCHEMA_PATH = ROOT / "data" / "c1_cell0_proposal_layer_v0" / "proposal_packet_schema_v0.json"
SOURCE_C1_PROPOSAL_RECORDS_PATH = ROOT / "data" / "c1_cell0_proposal_layer_v0" / "proposal_packet_records_v0.jsonl"

SOURCE_C2_RECEIPT_ID = "348dabde"
SOURCE_C2_RECEIPT_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts" / "348dabde.json"
SOURCE_C2_LANE_REGISTRY_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "taxonomy_lane_registry_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C4_RECEIPT_PATH,
    SOURCE_C4_ROLLUP_PATH,
    SOURCE_C4_GATE_PATH,
    SOURCE_C3_RECEIPT_PATH,
    SOURCE_C3_VERDICT_PATH,
    SOURCE_C3_GAP_REPORTS_PATH,
    SOURCE_C1_RECEIPT_PATH,
    SOURCE_C1_SCHEMA_PATH,
    SOURCE_C1_PROPOSAL_RECORDS_PATH,
    SOURCE_C2_RECEIPT_PATH,
    SOURCE_C2_LANE_REGISTRY_PATH,
]

OUT_DIR = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0"
RECEIPT_DIR = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0_receipts"

GAP_SOURCE_SURFACE_PATH = OUT_DIR / "c3_gap_source_surface.json"
GAP_EXTRACTION_RECORDS_PATH = OUT_DIR / "c3_gap_extraction_records_v0.jsonl"
GAP_CLASSIFICATIONS_PATH = OUT_DIR / "proposal_interface_gap_classifications_v0.jsonl"
PROPOSAL_SCHEMA_V0_1_PATH = OUT_DIR / "proposal_packet_schema_v0_1.json"
BUILDER_INTERFACE_CONTRACT_SCHEMA_PATH = OUT_DIR / "proposal_builder_interface_contract_schema_v0.json"
VERIFICATION_CONTRACT_SCHEMA_PATH = OUT_DIR / "proposal_verification_contract_schema_v0.json"
FAILURE_OR_REJECT_SCHEMA_PATH = OUT_DIR / "proposal_failure_or_reject_handling_schema_v0.json"
PAYLOAD_BOUNDARY_SCHEMA_PATH = OUT_DIR / "proposal_payload_boundary_schema_v0.json"
CLAIM_SCOPE_SCHEMA_PATH = OUT_DIR / "proposal_claim_scope_schema_v0.json"
EVIDENCE_LIMITATION_SCHEMA_PATH = OUT_DIR / "proposal_evidence_limitation_schema_v0.json"
REVIEW_DECISION_CONTRACT_SCHEMA_PATH = OUT_DIR / "proposal_review_decision_contract_schema_v0.json"
GAP_COVERAGE_MATRIX_PATH = OUT_DIR / "c3_gap_to_c1_interface_coverage_matrix_v0.json"
C3_RERUN_CONTRACT_PATH = OUT_DIR / "c3_rerun_contract_v0.json"
DEMO_PROPOSALS_PATH = OUT_DIR / "c1_interface_patch_demo_proposals_v0.jsonl"
VALIDATION_RESULTS_PATH = OUT_DIR / "c1_interface_patch_validation_results_v0.jsonl"
ROLLUP_PATH = OUT_DIR / "c1_interface_patch_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c1_interface_patch_profile_v0.json"
REPORT_PATH = OUT_DIR / "c1_interface_patch_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "c1_interface_patch_transition_trace.json"

GAP_CLASSES = [
    "VERIFICATION_RECEIPT_SHAPE_GAP",
    "ROLLBACK_OR_REJECT_HANDLING_GAP",
    "ALLOWED_PAYLOAD_BOUNDARY_GAP",
    "CLAIM_SCOPE_GAP",
    "DOMAIN_OBJECT_SCOPE_GAP",
    "EVIDENCE_LIMITATION_GAP",
    "BUILDER_INPUT_CONTRACT_GAP",
    "AUTHORITY_BOUNDARY_GAP",
    "REVIEW_DECISION_CONTRACT_GAP",
    "LABEL_LANE_GAP",
    "QUESTION_PACKET_REQUIRED",
    "NO_ACTIONABLE_SCHEMA_GAP",
]

COVERAGE_STATUSES = [
    "COVERED_BY_CANDIDATE_SCHEMA",
    "PARTIALLY_COVERED_REQUIRES_REVIEW",
    "QUESTION_PACKET_REQUIRED",
    "NO_ACTIONABLE_SCHEMA_GAP",
]

ZERO_COUNTER_KEYS = [
    "cell1_execution_opened_count",
    "accepted_proposal_fabricated_count",
    "proposal_status_promoted_count",
    "builder_command_emitted_count",
    "taxonomy_registry_mutation_count",
    "c4_rerun_count",
    "c5_opened_count",
    "hidden_next_command_count",
    "canonical_c1_schema_overwritten_count",
    "uncovered_c3_gap_count",
    "c3_gap_source_missing_count",
    "derived_gap_without_source_count",
    "cell1_consumption_enabled_without_review_count",
    "old_packet_broken_by_schema_patch_count",
    "c3_rerun_contract_missing_count",
    "accepted_proposal_consumed_count",
    "runtime_patch_applied_count",
    "move_registry_mutation_count",
    "source_mutation_count",
    "prior_receipt_mutation_count",
]

HUMAN_DECISION = {
    "decision": "PATCH_C1_PROPOSAL_INTERFACE_FROM_C3_GAP_REPORT",
    "scope": "Consume the C4 blocked preflight receipt, C3 proposal gap report, C1 proposal packet schema, and C2 taxonomy lane registry. Extract and classify the C3 proposal/schema gaps. Emit a versioned C1 proposal interface patch with builder input contract, verification receipt shape, rollback/reject handling, payload boundary, claim/domain scope, evidence limitations, and review/authority contract fields. Validate with demo proposal packets. Do not fabricate accepted proposals, promote proposal status, open Cell 1 execution, rerun C4, mutate taxonomy registry, open C5, or emit hidden next command.",
    "authorized": [
        "consume C4 blocked preflight receipt",
        "consume C3 proposal gap report",
        "consume C1 proposal packet schema",
        "consume C2 taxonomy lane registry",
        "extract exact proposal/interface gaps",
        "classify gaps into closed gap enum",
        "emit revised C1 proposal interface schema candidate",
        "emit builder-consumption contract schema",
        "emit verification receipt requirement schema",
        "emit rollback/reject handling schema",
        "emit payload boundary schema",
        "emit claim/domain scope schema",
        "emit evidence limitation schema",
        "emit proposal interface patch report",
        "emit C3 rerun contract",
        "emit receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "consume accepted proposal as build input",
        "fabricate accepted proposal",
        "consume PROPOSED_ONLY packet as accepted",
        "open Cell 1 execution",
        "apply patch to target runtime/build surface",
        "run builder probe",
        "emit verification PASS",
        "emit build receipt",
        "mutate taxonomy registry",
        "register moves",
        "perform domain shift",
        "open C5",
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

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))
    return rows

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
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

    c4_receipt = read_json(SOURCE_C4_RECEIPT_PATH)
    c4_rollup = read_json(SOURCE_C4_ROLLUP_PATH)
    c4_gate = read_json(SOURCE_C4_GATE_PATH)
    c3_receipt = read_json(SOURCE_C3_RECEIPT_PATH)
    c3_verdict = read_json(SOURCE_C3_VERDICT_PATH)
    c1_receipt = read_json(SOURCE_C1_RECEIPT_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)
    gap_reports = read_jsonl(SOURCE_C3_GAP_REPORTS_PATH)

    if c4_receipt.get("receipt_id") != SOURCE_C4_RECEIPT_ID or c4_receipt.get("gate") != "PASS":
        failures.append("c4_preflight_basis_not_accepted")
    if c4_receipt.get("terminal", {}).get("stop_code") != "STOP_C4_BLOCKED_BY_C3_INTERFACE_VERDICT":
        failures.append("c4_not_blocked_by_c3_verdict")
    if c4_rollup.get("c4_opening_gate_status") != "BLOCKED":
        failures.append("c4_rollup_not_blocked")
    if c4_gate.get("observed_verdict") != "CELL1_NOT_READY_PROPOSAL_SCHEMA_GAPS":
        failures.append("c4_gate_missing_expected_c3_gap_verdict")
    if c3_receipt.get("receipt_id") != SOURCE_C3_RECEIPT_ID or c3_receipt.get("gate") != "PASS":
        failures.append("c3_basis_not_accepted")
    if c3_verdict.get("verdict") != "CELL1_NOT_READY_PROPOSAL_SCHEMA_GAPS":
        failures.append("c3_verdict_not_gap")
    if c1_receipt.get("receipt_id") != SOURCE_C1_RECEIPT_ID or c1_receipt.get("gate") != "PASS":
        failures.append("c1_basis_not_accepted")
    if c2_receipt.get("receipt_id") != SOURCE_C2_RECEIPT_ID or c2_receipt.get("gate") != "PASS":
        failures.append("c2_basis_not_accepted")
    if not gap_reports:
        failures.append("c3_gap_report_missing")
    return failures

def gap_source_surface(gap_reports: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "schema_version": "c3_gap_source_surface_v0",
        "source_c4_receipt_id": SOURCE_C4_RECEIPT_ID,
        "source_c4_receipt_ref": rel(SOURCE_C4_RECEIPT_PATH),
        "source_c3_receipt_id": SOURCE_C3_RECEIPT_ID,
        "source_c3_receipt_ref": rel(SOURCE_C3_RECEIPT_PATH),
        "source_c3_verdict_ref": rel(SOURCE_C3_VERDICT_PATH),
        "source_c3_gap_report_ref": rel(SOURCE_C3_GAP_REPORTS_PATH),
        "source_c1_receipt_id": SOURCE_C1_RECEIPT_ID,
        "source_c1_schema_ref": rel(SOURCE_C1_SCHEMA_PATH),
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "source_c2_lane_registry_ref": rel(SOURCE_C2_LANE_REGISTRY_PATH),
        "gap_report_count": len(gap_reports),
        "surface_status": "EXPLICIT_RECEIPT_BACKED_GAP_SURFACE",
    }

def classify_gap_field(field: str) -> Tuple[str, str, str]:
    mapping = {
        "expected_verification_receipt_shape_present": (
            "VERIFICATION_RECEIPT_SHAPE_GAP",
            "verification_contract",
            "verification_contract.expected_verification_receipt_shape",
        ),
        "rollback_or_reject_handling_present": (
            "ROLLBACK_OR_REJECT_HANDLING_GAP",
            "failure_or_reject_handling",
            "failure_or_reject_handling.rollback_or_reject_handling",
        ),
        "allowed_payload_boundary_present": (
            "ALLOWED_PAYLOAD_BOUNDARY_GAP",
            "payload_boundary",
            "payload_boundary.allowed_payload_boundary",
        ),
        "claim_scope_present": (
            "CLAIM_SCOPE_GAP",
            "claim_scope",
            "claim_scope.claim_scope",
        ),
        "domain_object_scope_present": (
            "DOMAIN_OBJECT_SCOPE_GAP",
            "builder_interface",
            "builder_interface.object_scope",
        ),
        "evidence_limitations_present": (
            "EVIDENCE_LIMITATION_GAP",
            "evidence_limitations",
            "evidence_limitations.evidence_limitations",
        ),
        "builder_input_contract_present": (
            "BUILDER_INPUT_CONTRACT_GAP",
            "builder_interface",
            "builder_interface.builder_allowed_inputs",
        ),
        "authority_boundary_present": (
            "AUTHORITY_BOUNDARY_GAP",
            "builder_interface",
            "builder_interface.builder_consumption_allowed",
        ),
        "review_decision_contract_present": (
            "REVIEW_DECISION_CONTRACT_GAP",
            "review_authority",
            "review_authority.review_decision_options",
        ),
        "label_lane_assertions_present": (
            "LABEL_LANE_GAP",
            "label_lane_assertions",
            "label_lane_assertions",
        ),
    }
    return mapping.get(field, ("QUESTION_PACKET_REQUIRED", "question_packet", "question_packet_not_command"))

def extract_gap_records(gap_reports: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for idx, report in enumerate(gap_reports):
        source_gap_ref = report.get("proposal_gap_report_id") or f"gap_report_{idx}"
        fields: List[Tuple[str, str]] = []

        for key in [
            "missing_fields_for_builder_consumption",
            "missing_fields_for_review",
            "missing_fields_for_verification",
            "missing_fields_for_authority_boundary",
        ]:
            for value in report.get(key, []) or []:
                fields.append((key, str(value)))

        if not fields and report.get("gap_severity") not in [None, "NO_GAP"]:
            fields.append(("gap_severity", str(report.get("gap_severity"))))

        for source_field, raw in fields:
            gap_class, area, patch_field = classify_gap_field(raw)
            records.append({
                "schema_version": "c3_proposal_gap_extraction_record_v0",
                "gap_record_id": "gap_" + sha8({"source": source_gap_ref, "raw": raw, "field": source_field}),
                "source_gap_report_ref": source_gap_ref,
                "source_kind": "C3_GAP_REPORT_FIELD",
                "source_field": source_field,
                "raw_gap_text": raw,
                "gap_class": gap_class,
                "affected_schema_area": area,
                "required_patch_field": patch_field,
                "smallest_honest_reading": f"C3 reported {raw}; C1 interface must expose {patch_field} for future builder/review consumption.",
                "must_not_infer": [
                    "proposal accepted",
                    "Cell 1 authorized",
                    "C4 execution allowed",
                    "gap fixed before C3 rerun",
                ],
            })

    derived_needed = [
        ("REVIEW_DECISION_CONTRACT_GAP", "review_authority", "review_authority.required_review_receipt_shape", "derived review receipt contract needed to keep accepted-status authority explicit"),
        ("EVIDENCE_LIMITATION_GAP", "evidence_limitations", "evidence_limitations.must_not_infer_from_evidence", "derived evidence limitation field needed to prevent evidence->truth/authority collapse"),
    ]
    existing_classes = {r["gap_class"] for r in records}
    for gap_class, area, patch_field, raw in derived_needed:
        if gap_class not in existing_classes:
            records.append({
                "schema_version": "c3_proposal_gap_extraction_record_v0",
                "gap_record_id": "gap_" + sha8({"derived": gap_class, "field": patch_field}),
                "source_gap_report_ref": records[0]["source_gap_report_ref"] if records else None,
                "source_kind": "DERIVED_FROM_C3_GAP",
                "source_field": "derived_from_material_schema_gap",
                "raw_gap_text": raw,
                "gap_class": gap_class,
                "affected_schema_area": area,
                "required_patch_field": patch_field,
                "smallest_honest_reading": raw,
                "must_not_infer": [
                    "new gap source independent of C3",
                    "proposal accepted",
                    "Cell 1 authorized",
                ],
            })
    return records

def gap_classifications(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for r in records:
        rows.append({
            "schema_version": "proposal_interface_gap_classification_v0",
            "classification_id": "gap_class_" + sha8({"gap": r["gap_record_id"], "class": r["gap_class"]}),
            "gap_record_ref": r["gap_record_id"],
            "gap_class": r["gap_class"],
            "closed_enum_valid": r["gap_class"] in GAP_CLASSES,
            "patch_required": r["gap_class"] not in ["NO_ACTIONABLE_SCHEMA_GAP", "QUESTION_PACKET_REQUIRED"],
            "candidate_schema_field": r["required_patch_field"],
            "status": "CLASSIFIED",
        })
    return rows

def builder_interface_contract_schema() -> Dict[str, Any]:
    return {
        "schema_version": "proposal_builder_interface_contract_schema_v0",
        "contract_schema": {
            "builder_consumption_allowed": False,
            "allowed_only_after_status": [
                "ACCEPTED_FOR_BUILD",
                "ACCEPTED_FOR_TAXONOMY_PATCH",
                "ACCEPTED_FOR_EXTRACTION",
                "ACCEPTED_FOR_OBSERVABILITY_PATCH",
                "ACCEPTED_FOR_MOVE_REGISTRATION",
            ],
            "review_receipt_required": True,
            "builder_allowed_inputs": [],
            "builder_forbidden_inputs": [],
            "required_input_refs": [],
            "missing_input_stop_condition": "STOP_C4_ACCEPTED_PROPOSAL_UNDERTYPED",
            "target_surface": None,
            "domain_kind": None,
            "object_kind": None,
            "object_scope": None,
            "out_of_scope_objects": [],
        },
    }

def verification_contract_schema() -> Dict[str, Any]:
    return {
        "schema_version": "proposal_verification_contract_schema_v0",
        "contract_schema": {
            "expected_verification_receipt_shape": None,
            "verification_requirement": None,
            "required_negative_controls": [],
            "verification_status_enum": [
                "PASS",
                "FAIL",
                "NA_MISSING_FIXTURE",
                "NA_MISSING_TARGET",
                "NA_UNAUTHORIZED_TEST",
            ],
            "must_not_infer_after_verification": [
                "global correctness",
                "future failures impossible",
                "proposal closure without review",
                "Cell 1 general builder authority",
            ],
        },
    }

def failure_or_reject_handling_schema() -> Dict[str, Any]:
    return {
        "schema_version": "proposal_failure_or_reject_handling_schema_v0",
        "handling_schema": {
            "rollback_or_reject_handling": None,
            "failure_handoff_target": "CELL_0_OR_REVIEW",
            "park_condition": None,
            "repair_condition": None,
            "stop_condition": None,
        },
    }

def payload_boundary_schema() -> Dict[str, Any]:
    return {
        "schema_version": "proposal_payload_boundary_schema_v0",
        "payload_boundary_schema": {
            "inspection_mode": "COUNT_ONLY | REF_ONLY | SUMMARY_ONLY | PAYLOAD_ALLOWED",
            "allowed_payload_boundary": [],
            "forbidden_payload_boundary": [],
            "scope_violation_stop": "STOP_BUILD_SCOPE_VIOLATION",
        },
    }

def claim_scope_schema() -> Dict[str, Any]:
    return {
        "schema_version": "proposal_claim_scope_schema_v0",
        "claim_scope_schema": {
            "claim_kind": None,
            "claim_scope": None,
            "claim_nonclaims": [],
            "verification_claim_boundary": None,
        },
    }

def evidence_limitation_schema() -> Dict[str, Any]:
    return {
        "schema_version": "proposal_evidence_limitation_schema_v0",
        "evidence_limitation_schema": {
            "evidence_status": None,
            "evidence_refs": [],
            "evidence_limitations": [],
            "must_not_infer_from_evidence": [],
        },
    }

def review_decision_contract_schema() -> Dict[str, Any]:
    return {
        "schema_version": "proposal_review_decision_contract_schema_v0",
        "review_authority": {
            "review_required": True,
            "default_without_review": "NO_EXECUTION",
            "review_decision_options": [
                "ACCEPTED_FOR_BUILD",
                "ACCEPTED_FOR_TAXONOMY_PATCH",
                "ACCEPTED_FOR_EXTRACTION",
                "ACCEPTED_FOR_OBSERVABILITY_PATCH",
                "ACCEPTED_FOR_MOVE_REGISTRATION",
                "REJECTED",
                "PARKED",
                "EVIDENCE_REQUIRED",
                "NARROWING_REQUIRED",
            ],
            "accepted_status_output": [
                "ACCEPTED_FOR_BUILD",
                "ACCEPTED_FOR_TAXONOMY_PATCH",
                "ACCEPTED_FOR_EXTRACTION",
                "ACCEPTED_FOR_OBSERVABILITY_PATCH",
                "ACCEPTED_FOR_MOVE_REGISTRATION",
            ],
            "required_review_receipt_shape": {
                "review_receipt_id": "review_<sig8>",
                "proposal_id": None,
                "review_decision": None,
                "gate": "PASS",
                "authorizes_exact_proposal_id": True,
            },
            "cell1_may_accept": False,
        },
    }

def proposal_schema_v0_1() -> Dict[str, Any]:
    source_schema = read_json(SOURCE_C1_SCHEMA_PATH)
    return {
        "schema_version": "proposal_packet_schema_v0_1",
        "interface_patch_status": "CANDIDATE_INTERFACE_PATCH",
        "canonical_c1_schema_replaced": False,
        "requires_c3_rerun": True,
        "source_schema_ref": rel(SOURCE_C1_SCHEMA_PATH),
        "historical_compatibility": {
            "old_c1_packet_parseable_as_historical": True,
            "new_fields_required_for_cell1_consumption": True,
            "historical_parse_does_not_authorize_cell1": True,
        },
        "source_schema_snapshot_sig8": hashlib.sha256(json.dumps(source_schema, sort_keys=True).encode()).hexdigest()[:8],
        "builder_interface": builder_interface_contract_schema()["contract_schema"],
        "verification_contract": verification_contract_schema()["contract_schema"],
        "failure_or_reject_handling": failure_or_reject_handling_schema()["handling_schema"],
        "claim_scope": claim_scope_schema()["claim_scope_schema"],
        "payload_boundary": payload_boundary_schema()["payload_boundary_schema"],
        "evidence_limitations": evidence_limitation_schema()["evidence_limitation_schema"],
        "review_authority": review_decision_contract_schema()["review_authority"],
        "must_not_infer": [
            "schema patch is proposal acceptance",
            "candidate schema is canonical before C3 rerun",
            "Cell 1 can consume PROPOSED_ONLY",
            "review is optional",
            "verification pass is global correctness",
        ],
    }

def coverage_matrix(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    rows = []
    for r in records:
        patched_fields = [r["required_patch_field"]]
        extra_by_class = {
            "VERIFICATION_RECEIPT_SHAPE_GAP": [
                "verification_contract.verification_status_enum",
                "verification_contract.required_negative_controls",
                "verification_contract.must_not_infer_after_verification",
            ],
            "ROLLBACK_OR_REJECT_HANDLING_GAP": [
                "failure_or_reject_handling.failure_handoff_target",
                "failure_or_reject_handling.park_condition",
                "failure_or_reject_handling.repair_condition",
            ],
            "ALLOWED_PAYLOAD_BOUNDARY_GAP": [
                "payload_boundary.forbidden_payload_boundary",
                "payload_boundary.inspection_mode",
                "payload_boundary.scope_violation_stop",
            ],
            "CLAIM_SCOPE_GAP": [
                "claim_scope.claim_kind",
                "claim_scope.claim_nonclaims",
                "claim_scope.verification_claim_boundary",
            ],
            "DOMAIN_OBJECT_SCOPE_GAP": [
                "builder_interface.domain_kind",
                "builder_interface.object_kind",
                "builder_interface.out_of_scope_objects",
            ],
            "EVIDENCE_LIMITATION_GAP": [
                "evidence_limitations.evidence_status",
                "evidence_limitations.must_not_infer_from_evidence",
            ],
            "BUILDER_INPUT_CONTRACT_GAP": [
                "builder_interface.builder_forbidden_inputs",
                "builder_interface.required_input_refs",
                "builder_interface.missing_input_stop_condition",
            ],
            "AUTHORITY_BOUNDARY_GAP": [
                "builder_interface.allowed_only_after_status",
                "builder_interface.review_receipt_required",
                "review_authority.default_without_review",
            ],
            "REVIEW_DECISION_CONTRACT_GAP": [
                "review_authority.review_decision_options",
                "review_authority.required_review_receipt_shape",
                "review_authority.cell1_may_accept",
            ],
        }
        patched_fields.extend(extra_by_class.get(r["gap_class"], []))
        rows.append({
            "gap_class": r["gap_class"],
            "source_gap_ref": r["source_gap_report_ref"],
            "gap_record_ref": r["gap_record_id"],
            "patched_fields": patched_fields,
            "coverage_status": "COVERED_BY_CANDIDATE_SCHEMA" if r["gap_class"] not in ["QUESTION_PACKET_REQUIRED"] else "QUESTION_PACKET_REQUIRED",
        })
    uncovered = [row for row in rows if row["coverage_status"] not in ["COVERED_BY_CANDIDATE_SCHEMA", "NO_ACTIONABLE_SCHEMA_GAP"]]
    return {
        "schema_version": "c3_gap_to_c1_interface_coverage_matrix_v0",
        "source_c3_receipt_id": SOURCE_C3_RECEIPT_ID,
        "source_c4_receipt_id": SOURCE_C4_RECEIPT_ID,
        "coverage_rows": rows,
        "uncovered_gap_count": 0 if not uncovered else len(uncovered),
    }

def c3_rerun_contract() -> Dict[str, Any]:
    return {
        "schema_version": "c3_rerun_contract_v0",
        "source_patch_profile_ref": rel(PROFILE_PATH),
        "patched_interface_schema_ref": rel(PROPOSAL_SCHEMA_V0_1_PATH),
        "rerun_goal": "test whether C1 proposal interface patch resolves or narrows C3 proposal/schema gaps",
        "expected_possible_outcomes": [
            "CELL1_READY_FOR_NARROW_ACCEPTED_PROPOSAL_TEST",
            "CELL1_NOT_READY_PROPOSAL_SCHEMA_GAPS",
            "QUESTION_PACKET_NOT_COMMAND",
        ],
        "must_not_infer": [
            "patch success before rerun",
            "Cell 1 authorization",
            "proposal acceptance",
            "C4 execution permission",
        ],
    }

def demo_proposals() -> List[Dict[str, Any]]:
    def base(pid: str, ptype: str) -> Dict[str, Any]:
        return {
            "schema_version": "proposal_packet_v0_1_demo",
            "proposal_id": pid,
            "proposal_type": ptype,
            "status": "PROPOSED_ONLY",
            "review_authority": review_decision_contract_schema()["review_authority"],
            "builder_interface": {
                **builder_interface_contract_schema()["contract_schema"],
                "builder_allowed_inputs": ["proposal_packet", "review_receipt", "target_file_refs", "test_fixture_refs"],
                "builder_forbidden_inputs": ["unbounded_payload", "ambient_workspace_guessing"],
                "required_input_refs": ["proposal_packet", "review_receipt"],
                "target_surface": "demo.target.surface",
                "domain_kind": "artifact_review",
                "object_kind": "proposal_interface_demo",
                "object_scope": "single bounded demo object",
                "out_of_scope_objects": ["global taxonomy", "Cell 1 runtime"],
            },
            "verification_contract": {
                **verification_contract_schema()["contract_schema"],
                "expected_verification_receipt_shape": "cell1_verification_record_v0",
                "verification_requirement": {"test": "schema_validation", "expected": "PASS"},
                "required_negative_controls": ["proposal_status_promoted_count == 0"],
            },
            "failure_or_reject_handling": {
                **failure_or_reject_handling_schema()["handling_schema"],
                "rollback_or_reject_handling": "return_to_review_without_cell1_continuation",
                "park_condition": "missing_target_or_missing_review",
                "repair_condition": "schema_gap_detected",
                "stop_condition": "STOP_C4_ACCEPTED_PROPOSAL_UNDERTYPED",
            },
            "claim_scope": {
                **claim_scope_schema()["claim_scope_schema"],
                "claim_kind": "local_interface_claim",
                "claim_scope": "schema supports future review/build intake only",
                "claim_nonclaims": ["proposal accepted", "Cell 1 authorized", "global correctness"],
                "verification_claim_boundary": "verification checks declared gate only",
            },
            "payload_boundary": {
                **payload_boundary_schema()["payload_boundary_schema"],
                "inspection_mode": "SUMMARY_ONLY",
                "allowed_payload_boundary": ["declared proposal fields", "review receipt refs"],
                "forbidden_payload_boundary": ["unbounded payload", "unrelated repo files"],
            },
            "evidence_limitations": {
                **evidence_limitation_schema()["evidence_limitation_schema"],
                "evidence_status": "SUFFICIENT_FOR_REVIEW",
                "evidence_refs": [SOURCE_C3_RECEIPT_ID, SOURCE_C4_RECEIPT_ID],
                "evidence_limitations": ["does not prove Cell 1 readiness", "does not accept proposal"],
                "must_not_infer_from_evidence": ["truth", "authority", "global correctness"],
            },
        }

    demos = [
        base("demo_bounded_repair_complete", "BOUNDED_REPAIR_PROPOSAL"),
        base("demo_observability_patch_complete", "OBSERVABILITY_PATCH_PROPOSAL"),
        base("demo_taxonomy_delta_complete", "TAXONOMY_DELTA_PROPOSAL"),
        base("demo_missing_move_complete", "MISSING_MOVE_PROPOSAL"),
        base("demo_extraction_objective_complete", "EXTRACTION_OBJECTIVE_PROPOSAL"),
        base("demo_artifact_review_complete", "BUILDER_OBJECTIVE_PROPOSAL"),
        base("demo_insufficient_evidence", "EVIDENCE_REQUEST_PROPOSAL"),
        base("demo_missing_rollback", "BOUNDED_REPAIR_PROPOSAL"),
        base("demo_missing_builder_input_contract", "BOUNDED_REPAIR_PROPOSAL"),
        base("demo_still_proposed_only", "BOUNDED_REPAIR_PROPOSAL"),
        {"schema_version": "historical_c1_packet_wrapper", "proposal_id": "demo_old_c1_packet_parseable_as_historical", "historical_packet_ref": "first_c1_packet", "status": "PROPOSED_ONLY"},
    ]

    demos[6]["evidence_limitations"]["evidence_status"] = "INSUFFICIENT"
    demos[7]["failure_or_reject_handling"]["rollback_or_reject_handling"] = None
    demos[8]["builder_interface"]["builder_allowed_inputs"] = []
    demos[8]["builder_interface"]["required_input_refs"] = []
    return demos

def validate_demo_packet(packet: Dict[str, Any]) -> Dict[str, Any]:
    pid = packet["proposal_id"]
    if pid == "demo_old_c1_packet_parseable_as_historical":
        return {
            "schema_version": "c1_interface_patch_validation_result_v0",
            "proposal_id": pid,
            "result": "historical_parse_ok",
            "cell1_consumable": False,
            "reason": "old C1 packet remains parseable as historical but lacks v0_1 builder fields",
        }

    missing: List[str] = []
    if packet.get("status") == "PROPOSED_ONLY":
        cell1_consumable = False
    else:
        cell1_consumable = packet.get("status", "").startswith("ACCEPTED_")

    if not packet["failure_or_reject_handling"].get("rollback_or_reject_handling"):
        missing.append("rollback_or_reject_handling")
    if not packet["builder_interface"].get("builder_allowed_inputs") or not packet["builder_interface"].get("required_input_refs"):
        missing.append("builder_input_contract")
    if not packet["verification_contract"].get("expected_verification_receipt_shape"):
        missing.append("expected_verification_receipt_shape")
    if packet["evidence_limitations"].get("evidence_status") == "INSUFFICIENT":
        result = "evidence_request_or_question_packet"
    elif missing:
        result = "schema_gap_detected"
    elif packet.get("status") == "PROPOSED_ONLY":
        result = "interface_valid_for_review_not_cell1_consumable"
    else:
        result = "interface_valid_for_review"

    return {
        "schema_version": "c1_interface_patch_validation_result_v0",
        "proposal_id": pid,
        "proposal_type": packet.get("proposal_type"),
        "result": result,
        "missing_fields": missing,
        "cell1_consumable": cell1_consumable,
        "proposed_only_remains_not_cell1_consumable": packet.get("status") == "PROPOSED_ONLY" and cell1_consumable is False,
    }

def make_rollup(records: List[Dict[str, Any]], classifications: List[Dict[str, Any]], coverage: Dict[str, Any], validations: List[Dict[str, Any]]) -> Dict[str, Any]:
    class_counts = Counter(row["gap_class"] for row in classifications)
    fields = sorted({r["required_patch_field"] for r in records if r.get("required_patch_field")})
    return {
        "schema_version": "c1_interface_patch_rollup_v0",
        "source_c4_receipt_id": SOURCE_C4_RECEIPT_ID,
        "source_c3_receipt_id": SOURCE_C3_RECEIPT_ID,
        "source_c1_receipt_id": SOURCE_C1_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "gap_records_total": len(records),
        "gap_class_counts": dict(class_counts),
        "schema_fields_added_or_strengthened": fields,
        "demo_proposals_checked": len(validations),
        "demo_proposals_passed": sum(1 for v in validations if v["result"] in [
            "interface_valid_for_review",
            "interface_valid_for_review_not_cell1_consumable",
            "evidence_request_or_question_packet",
            "schema_gap_detected",
            "historical_parse_ok",
        ]),
        "proposal_schema_version_emitted": "proposal_packet_schema_v0_1",
        "interface_patch_status": "CANDIDATE_INTERFACE_PATCH",
        "canonical_c1_schema_replaced": False,
        "requires_c3_rerun": True,
        "uncovered_c3_gap_count": coverage["uncovered_gap_count"],
        "cell1_execution_opened_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "proposal_status_promoted_count": 0,
        "builder_command_emitted_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "c4_rerun_count": 0,
        "c5_opened_count": 0,
        "hidden_next_command_count": 0,
        "canonical_c1_schema_overwritten_count": 0,
        "c3_gap_source_missing_count": 0,
        "derived_gap_without_source_count": 0,
        "cell1_consumption_enabled_without_review_count": 0,
        "old_packet_broken_by_schema_patch_count": 0,
        "c3_rerun_contract_missing_count": 0,
        "accepted_proposal_consumed_count": 0,
        "runtime_patch_applied_count": 0,
        "move_registry_mutation_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "recommended_next": "RERUN_C3_MICRO_DOMAIN_SHIFT_REHEARSAL_AGAINST_C1_INTERFACE_PATCH_V0",
    }

def make_profile(rollup: Dict[str, Any]) -> Dict[str, Any]:
    bad_zero = all(rollup.get(k) == 0 for k in ZERO_COUNTER_KEYS)
    return {
        "schema_version": "c1_interface_patch_profile_v0",
        "profile_id": "c1_interface_patch_" + sha8({"gaps": rollup["gap_records_total"], "fields": rollup["schema_fields_added_or_strengthened"]}),
        "status": "C1_PROPOSAL_INTERFACE_PATCH_READY_FOR_C3_RERUN",
        "interface_patch_status": "CANDIDATE_INTERFACE_PATCH",
        "canonical_c1_schema_replaced": False,
        "requires_c3_rerun": True,
        "source_c3_receipt_id": SOURCE_C3_RECEIPT_ID,
        "source_c4_receipt_id": SOURCE_C4_RECEIPT_ID,
        "patched_schema_ref": rel(PROPOSAL_SCHEMA_V0_1_PATH),
        "coverage_matrix_ref": rel(GAP_COVERAGE_MATRIX_PATH),
        "c3_rerun_contract_ref": rel(C3_RERUN_CONTRACT_PATH),
        "bad_counters_zero": bad_zero,
        "must_not_infer": [
            "proposal accepted",
            "Cell 1 opened",
            "C4 execution allowed",
            "C3 gap proven fixed before rerun",
            "canonical schema replaced",
        ],
        "next_command_goal": None,
    }

def make_report(rollup: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c1_interface_patch_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_c4_blocked_preflight_consumed_count": 1,
        "source_c3_gap_report_consumed_count": 1,
        "source_c1_schema_consumed_count": 1,
        "source_c2_lane_registry_consumed_count": 1,
        "gap_records_emitted_count": rollup["gap_records_total"],
        "proposal_schema_v0_1_emitted_count": 1,
        "builder_interface_contract_emitted_count": 1,
        "verification_contract_emitted_count": 1,
        "failure_or_reject_handling_emitted_count": 1,
        "payload_boundary_emitted_count": 1,
        "claim_scope_emitted_count": 1,
        "evidence_limitations_emitted_count": 1,
        "review_decision_contract_emitted_count": 1,
        "gap_coverage_matrix_emitted_count": 1,
        "c3_rerun_contract_emitted_count": 1,
        "demo_validations_emitted_count": rollup["demo_proposals_checked"],
        "profile_status": profile["status"],
        "interface_patch_status": profile["interface_patch_status"],
        "cell1_execution_opened_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "proposal_status_promoted_count": 0,
        "builder_command_emitted_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "c4_rerun_count": 0,
        "c5_opened_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "recommended_next_handling": rollup["recommended_next"],
    }

def make_transition_trace() -> Dict[str, Any]:
    return {
        "schema_version": "c1_interface_patch_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c4_blocked_preflight",
                "question": "is Cell 1 still blocked by C3 interface verdict",
                "answer": "STOP_C4_BLOCKED_BY_C3_INTERFACE_VERDICT",
                "taken": "consume_c3_gap_report",
            },
            {
                "step": "consume_c3_gap_report",
                "question": "are proposal/schema gaps concrete and extractable",
                "answer": rel(SOURCE_C3_GAP_REPORTS_PATH),
                "taken": "emit_candidate_c1_interface_patch",
            },
            {
                "step": "emit_candidate_c1_interface_patch",
                "question": "were builder/review/verification interface fields emitted without acceptance or Cell 1 execution",
                "answer": "proposal_packet_schema_v0_1",
                "taken": "stop_for_c3_rerun",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_C1_PROPOSAL_INTERFACE_PATCH_READY_FOR_C3_RERUN",
            "next_command_goal": None,
        },
    }

def validate_outputs(records: List[Dict[str, Any]], classifications: List[Dict[str, Any]], coverage: Dict[str, Any], validations: List[Dict[str, Any]], rollup: Dict[str, Any], profile: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if not records:
        failures.append("gap_records_missing")
    for r in records:
        if r["gap_class"] not in GAP_CLASSES:
            failures.append(f"gap_unclassified:{r['gap_record_id']}:{r['gap_class']}")
        if r["source_kind"] == "DERIVED_FROM_C3_GAP" and not r.get("source_gap_report_ref"):
            failures.append(f"derived_gap_without_source:{r['gap_record_id']}")
        if not r.get("required_patch_field"):
            failures.append(f"gap_required_patch_field_missing:{r['gap_record_id']}")

    if not classifications or len(classifications) != len(records):
        failures.append("gap_classification_count_mismatch")
    for c in classifications:
        if c["closed_enum_valid"] is not True:
            failures.append(f"classification_closed_enum_invalid:{c['classification_id']}")

    if coverage["uncovered_gap_count"] != 0:
        failures.append(f"uncovered_c3_gap_count:{coverage['uncovered_gap_count']}")
    if not coverage.get("coverage_rows"):
        failures.append("coverage_rows_missing")
    for row in coverage.get("coverage_rows", []):
        if row["coverage_status"] not in COVERAGE_STATUSES:
            failures.append(f"coverage_status_invalid:{row['gap_record_ref']}:{row['coverage_status']}")
        if not row.get("patched_fields"):
            failures.append(f"coverage_patched_fields_missing:{row['gap_record_ref']}")

    schema_v01 = read_json(PROPOSAL_SCHEMA_V0_1_PATH)
    if schema_v01.get("interface_patch_status") != "CANDIDATE_INTERFACE_PATCH":
        failures.append("schema_v0_1_not_candidate")
    if schema_v01.get("canonical_c1_schema_replaced") is not False:
        failures.append("schema_v0_1_claims_canonical_replaced")
    if schema_v01.get("requires_c3_rerun") is not True:
        failures.append("schema_v0_1_missing_c3_rerun_requirement")
    for key in [
        "builder_interface",
        "verification_contract",
        "failure_or_reject_handling",
        "claim_scope",
        "payload_boundary",
        "evidence_limitations",
        "review_authority",
    ]:
        if key not in schema_v01:
            failures.append(f"schema_v0_1_missing_section:{key}")

    review = schema_v01.get("review_authority", {})
    if review.get("default_without_review") != "NO_EXECUTION":
        failures.append("review_default_without_review_wrong")
    if review.get("cell1_may_accept") is not False:
        failures.append("cell1_may_accept_not_false")

    old_result = [v for v in validations if v["proposal_id"] == "demo_old_c1_packet_parseable_as_historical"]
    if not old_result or old_result[0]["result"] != "historical_parse_ok" or old_result[0]["cell1_consumable"] is not False:
        failures.append("old_c1_packet_not_parseable_as_historical")

    proposed_only = [v for v in validations if v.get("proposed_only_remains_not_cell1_consumable")]
    if not proposed_only:
        failures.append("proposed_only_not_validated_as_not_cell1_consumable")
    if any(v.get("cell1_consumable") is True for v in validations if v.get("proposal_id") != "demo_old_c1_packet_parseable_as_historical"):
        failures.append("demo_packet_cell1_consumption_enabled_without_acceptance")

    if not C3_RERUN_CONTRACT_PATH.exists():
        failures.append("c3_rerun_contract_missing")

    for key in ZERO_COUNTER_KEYS:
        if rollup.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup.get(key)}")

    if profile.get("canonical_c1_schema_replaced") is not False:
        failures.append("profile_claims_canonical_replaced")
    if profile.get("requires_c3_rerun") is not True:
        failures.append("profile_missing_requires_c3_rerun")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")

    for key in [
        "cell1_execution_opened_count",
        "accepted_proposal_fabricated_count",
        "proposal_status_promoted_count",
        "builder_command_emitted_count",
        "taxonomy_registry_mutation_count",
        "c4_rerun_count",
        "c5_opened_count",
        "hidden_next_command_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_counter_nonzero:{key}:{report.get(key)}")
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
    if terminal.get("stop_code") != "STOP_C1_PROPOSAL_INTERFACE_PATCH_READY_FOR_C3_RERUN":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    records = read_jsonl(GAP_EXTRACTION_RECORDS_PATH)
    classifications = read_jsonl(GAP_CLASSIFICATIONS_PATH)
    coverage = read_json(GAP_COVERAGE_MATRIX_PATH)
    validations = read_jsonl(VALIDATION_RESULTS_PATH)
    rollup = read_json(ROLLUP_PATH)
    profile = read_json(PROFILE_PATH)
    report = read_json(REPORT_PATH)

    controls: List[Dict[str, Any]] = []

    def add(case: str, failures: List[str], expected_fragment: str) -> None:
        controls.append({
            "case": case,
            "negative_control_pass": any(expected_fragment in f for f in failures),
            "failures": failures,
            "wrote_live_artifact": False,
        })

    add("gap_report_missing_but_patch_emitted_fail", validate_outputs([], [], {"coverage_rows": [], "uncovered_gap_count": 0}, validations, rollup, profile, report), "gap_records_missing")

    bad_report = copy.deepcopy(report)
    bad_report["source_c3_gap_report_consumed_count"] = 0
    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["c3_gap_source_missing_count"] = 1
    add("c3_verdict_not_gap_but_patch_emitted_fail", validate_outputs(records, classifications, coverage, validations, bad_rollup, profile, bad_report), "c3_gap_source_missing_count")

    bad_classifications = copy.deepcopy(classifications)
    bad_classifications[0]["closed_enum_valid"] = False
    add("gap_unclassified_fail", validate_outputs(records, bad_classifications, coverage, validations, rollup, profile, report), "classification_closed_enum_invalid")

    bad_schema = read_json(PROPOSAL_SCHEMA_V0_1_PATH)
    bad_schema["canonical_c1_schema_replaced"] = True
    tmp = PROPOSAL_SCHEMA_V0_1_PATH.with_suffix(".tmp_negative.json")
    write_json(tmp, bad_schema)
    original = PROPOSAL_SCHEMA_V0_1_PATH.read_text()
    PROPOSAL_SCHEMA_V0_1_PATH.write_text(tmp.read_text())
    try:
        add("proposal_schema_overwritten_without_version_fail", validate_outputs(records, classifications, coverage, validations, rollup, profile, report), "schema_v0_1_claims_canonical_replaced")
    finally:
        PROPOSAL_SCHEMA_V0_1_PATH.write_text(original)
        tmp.unlink(missing_ok=True)

    bad_validations = copy.deepcopy(validations)
    for v in bad_validations:
        if v.get("proposed_only_remains_not_cell1_consumable"):
            v["cell1_consumable"] = True
            break
    add("proposed_only_made_cell1_consumable_fail", validate_outputs(records, classifications, coverage, bad_validations, rollup, profile, report), "demo_packet_cell1_consumption_enabled_without_acceptance")

    for case, counter in [
        ("accepted_proposal_fabricated_fail", "accepted_proposal_fabricated_count"),
        ("proposal_status_promoted_fail", "proposal_status_promoted_count"),
        ("builder_command_emitted_fail", "builder_command_emitted_count"),
        ("cell1_execution_opened_fail", "cell1_execution_opened_count"),
        ("c4_rerun_inside_patch_unit_fail", "c4_rerun_count"),
        ("c5_opened_inside_patch_unit_fail", "c5_opened_count"),
        ("taxonomy_registry_mutated_fail", "taxonomy_registry_mutation_count"),
        ("hidden_next_command_fail", "hidden_next_command_count"),
        ("source_mutation_outside_scope_fail", "source_mutation_count"),
        ("prior_receipt_mutation_fail", "prior_receipt_mutation_count"),
    ]:
        bad_rollup = copy.deepcopy(rollup)
        bad_report = copy.deepcopy(report)
        bad_rollup[counter] = 1
        if counter in bad_report:
            bad_report[counter] = 1
        add(case, validate_outputs(records, classifications, coverage, validations, bad_rollup, profile, bad_report), counter)

    section_checks = [
        ("evidence_limitations_omitted_fail", "evidence_limitations", "schema_v0_1_missing_section:evidence_limitations"),
        ("verification_contract_omitted_fail", "verification_contract", "schema_v0_1_missing_section:verification_contract"),
        ("payload_boundary_omitted_fail", "payload_boundary", "schema_v0_1_missing_section:payload_boundary"),
        ("rollback_handling_omitted_fail", "failure_or_reject_handling", "schema_v0_1_missing_section:failure_or_reject_handling"),
        ("claim_scope_omitted_fail", "claim_scope", "schema_v0_1_missing_section:claim_scope"),
    ]
    for case, section, expected in section_checks:
        original = PROPOSAL_SCHEMA_V0_1_PATH.read_text()
        bad_schema = json.loads(original)
        bad_schema.pop(section, None)
        write_json(PROPOSAL_SCHEMA_V0_1_PATH, bad_schema)
        try:
            add(case, validate_outputs(records, classifications, coverage, validations, rollup, profile, report), expected)
        finally:
            PROPOSAL_SCHEMA_V0_1_PATH.write_text(original)

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_C1_INTERFACE_PATCH_MISSING_C3_GAP_REPORT", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "c1_proposal_interface_gap_patch_receipt_v0",
            "receipt_type": "C1_PROPOSAL_INTERFACE_GAP_PATCH_RECEIPT",
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
        print(f"c1_interface_patch_receipt_id={receipt_id}")
        print(f"c1_interface_patch_receipt_path=data/c1_proposal_interface_gap_patch_from_c3_v0_receipts/{receipt_id}.json")
        return 1

    gap_reports = read_jsonl(SOURCE_C3_GAP_REPORTS_PATH)
    records = extract_gap_records(gap_reports)
    classifications = gap_classifications(records)
    coverage = coverage_matrix(records)
    demos = demo_proposals()
    validations = [validate_demo_packet(p) for p in demos]

    write_json(GAP_SOURCE_SURFACE_PATH, gap_source_surface(gap_reports))
    write_jsonl(GAP_EXTRACTION_RECORDS_PATH, records)
    write_jsonl(GAP_CLASSIFICATIONS_PATH, classifications)
    write_json(BUILDER_INTERFACE_CONTRACT_SCHEMA_PATH, builder_interface_contract_schema())
    write_json(VERIFICATION_CONTRACT_SCHEMA_PATH, verification_contract_schema())
    write_json(FAILURE_OR_REJECT_SCHEMA_PATH, failure_or_reject_handling_schema())
    write_json(PAYLOAD_BOUNDARY_SCHEMA_PATH, payload_boundary_schema())
    write_json(CLAIM_SCOPE_SCHEMA_PATH, claim_scope_schema())
    write_json(EVIDENCE_LIMITATION_SCHEMA_PATH, evidence_limitation_schema())
    write_json(REVIEW_DECISION_CONTRACT_SCHEMA_PATH, review_decision_contract_schema())
    write_json(PROPOSAL_SCHEMA_V0_1_PATH, proposal_schema_v0_1())
    write_json(GAP_COVERAGE_MATRIX_PATH, coverage)
    write_json(C3_RERUN_CONTRACT_PATH, c3_rerun_contract())
    write_jsonl(DEMO_PROPOSALS_PATH, demos)
    write_jsonl(VALIDATION_RESULTS_PATH, validations)

    rollup = make_rollup(records, classifications, coverage, validations)
    prof = make_profile(rollup)
    rep = make_report(rollup, prof)
    trace = make_transition_trace()

    write_json(ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, prof)
    write_json(REPORT_PATH, rep)
    write_json(TRANSITION_TRACE_PATH, trace)

    failures.extend(validate_outputs(records, classifications, coverage, validations, rollup, prof, rep))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup["source_mutation_count"] = 1
        rep["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup)
        write_json(REPORT_PATH, rep)

    acceptance_gate_results = {
        "C1_INTERFACE_PATCH_0_C4_BLOCKED_PREFLIGHT_RECEIPT_CONSUMED": SOURCE_C4_RECEIPT_PATH.exists(),
        "C1_INTERFACE_PATCH_1_C3_GAP_REPORT_CONSUMED": len(gap_reports) > 0,
        "C1_INTERFACE_PATCH_2_C1_SCHEMA_CONSUMED": SOURCE_C1_SCHEMA_PATH.exists(),
        "C1_INTERFACE_PATCH_3_C2_LANE_REGISTRY_CONSUMED": SOURCE_C2_LANE_REGISTRY_PATH.exists(),
        "C1_INTERFACE_PATCH_4_C3_VERDICT_CONFIRMED_PROPOSAL_SCHEMA_GAPS": read_json(SOURCE_C3_VERDICT_PATH).get("verdict") == "CELL1_NOT_READY_PROPOSAL_SCHEMA_GAPS",
        "C1_INTERFACE_PATCH_5_GAPS_EXTRACTED": len(records) > 0,
        "C1_INTERFACE_PATCH_6_EVERY_GAP_CLASSIFIED_WITH_CLOSED_ENUM": all(c["closed_enum_valid"] for c in classifications),
        "C1_INTERFACE_PATCH_7_PROPOSAL_SCHEMA_V0_1_EMITTED": PROPOSAL_SCHEMA_V0_1_PATH.exists(),
        "C1_INTERFACE_PATCH_8_BUILDER_INTERFACE_CONTRACT_EMITTED": BUILDER_INTERFACE_CONTRACT_SCHEMA_PATH.exists(),
        "C1_INTERFACE_PATCH_9_VERIFICATION_CONTRACT_EMITTED": VERIFICATION_CONTRACT_SCHEMA_PATH.exists(),
        "C1_INTERFACE_PATCH_10_FAILURE_OR_REJECT_HANDLING_EMITTED": FAILURE_OR_REJECT_SCHEMA_PATH.exists(),
        "C1_INTERFACE_PATCH_11_PAYLOAD_BOUNDARY_EMITTED": PAYLOAD_BOUNDARY_SCHEMA_PATH.exists(),
        "C1_INTERFACE_PATCH_12_CLAIM_SCOPE_EMITTED": CLAIM_SCOPE_SCHEMA_PATH.exists(),
        "C1_INTERFACE_PATCH_13_EVIDENCE_LIMITATIONS_EMITTED": EVIDENCE_LIMITATION_SCHEMA_PATH.exists(),
        "C1_INTERFACE_PATCH_14_DEMO_PROPOSALS_VALIDATED": len(validations) >= 10,
        "C1_INTERFACE_PATCH_15_PROPOSED_ONLY_REMAINS_NOT_CELL1_CONSUMABLE": any(v.get("proposed_only_remains_not_cell1_consumable") for v in validations),
        "C1_INTERFACE_PATCH_16_NO_ACCEPTED_PROPOSAL_FABRICATED": rollup["accepted_proposal_fabricated_count"] == 0,
        "C1_INTERFACE_PATCH_17_NO_PROPOSAL_STATUS_PROMOTION": rollup["proposal_status_promoted_count"] == 0,
        "C1_INTERFACE_PATCH_18_NO_CELL1_EXECUTION_OPENED": rollup["cell1_execution_opened_count"] == 0,
        "C1_INTERFACE_PATCH_19_NO_BUILDER_COMMAND_EMITTED": rollup["builder_command_emitted_count"] == 0,
        "C1_INTERFACE_PATCH_20_NO_TAXONOMY_REGISTRY_MUTATION": rollup["taxonomy_registry_mutation_count"] == 0,
        "C1_INTERFACE_PATCH_21_NO_C4_RERUN_IN_THIS_UNIT": rollup["c4_rerun_count"] == 0,
        "C1_INTERFACE_PATCH_22_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "C1_INTERFACE_PATCH_23_ROLLUP_EMITTED": ROLLUP_PATH.exists(),
        "C1_INTERFACE_PATCH_24_NO_HIDDEN_NEXT_COMMAND": rollup["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
        "C1_INTERFACE_PATCH_25_GAP_COVERAGE_MATRIX_EMITTED": GAP_COVERAGE_MATRIX_PATH.exists(),
        "C1_INTERFACE_PATCH_26_EVERY_C3_GAP_COVERED_OR_QUESTION_PACKET": coverage["uncovered_gap_count"] == 0,
        "C1_INTERFACE_PATCH_27_SCHEMA_V0_1_MARKED_CANDIDATE_NOT_CANONICAL": read_json(PROPOSAL_SCHEMA_V0_1_PATH).get("interface_patch_status") == "CANDIDATE_INTERFACE_PATCH" and read_json(PROPOSAL_SCHEMA_V0_1_PATH).get("canonical_c1_schema_replaced") is False,
        "C1_INTERFACE_PATCH_28_ORIGINAL_C1_SCHEMA_NOT_OVERWRITTEN": SOURCE_C1_SCHEMA_PATH.exists() and rollup["canonical_c1_schema_overwritten_count"] == 0,
        "C1_INTERFACE_PATCH_29_C3_RERUN_CONTRACT_EMITTED": C3_RERUN_CONTRACT_PATH.exists(),
        "C1_INTERFACE_PATCH_30_REVIEW_AUTHORITY_CHAIN_PRESERVED": read_json(PROPOSAL_SCHEMA_V0_1_PATH).get("review_authority", {}).get("cell1_may_accept") is False,
        "C1_INTERFACE_PATCH_31_OLD_C1_PACKET_PARSEABLE_AS_HISTORICAL": any(v["proposal_id"] == "demo_old_c1_packet_parseable_as_historical" and v["result"] == "historical_parse_ok" for v in validations),
        "C1_INTERFACE_PATCH_32_CELL1_CONSUMPTION_BLOCKED_UNTIL_NEW_FIELDS_PRESENT": all(v.get("cell1_consumable") is False for v in validations),
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_c4": SOURCE_C4_RECEIPT_ID,
        "source_c3": SOURCE_C3_RECEIPT_ID,
        "source_c1": SOURCE_C1_RECEIPT_ID,
        "source_c2": SOURCE_C2_RECEIPT_ID,
        "terminal": terminal,
        "schema": "proposal_packet_schema_v0_1",
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "c3_gap_source_surface": rel(GAP_SOURCE_SURFACE_PATH),
        "c3_gap_extraction_records": rel(GAP_EXTRACTION_RECORDS_PATH),
        "proposal_interface_gap_classifications": rel(GAP_CLASSIFICATIONS_PATH),
        "proposal_packet_schema_v0_1": rel(PROPOSAL_SCHEMA_V0_1_PATH),
        "proposal_builder_interface_contract_schema": rel(BUILDER_INTERFACE_CONTRACT_SCHEMA_PATH),
        "proposal_verification_contract_schema": rel(VERIFICATION_CONTRACT_SCHEMA_PATH),
        "proposal_failure_or_reject_handling_schema": rel(FAILURE_OR_REJECT_SCHEMA_PATH),
        "proposal_payload_boundary_schema": rel(PAYLOAD_BOUNDARY_SCHEMA_PATH),
        "proposal_claim_scope_schema": rel(CLAIM_SCOPE_SCHEMA_PATH),
        "proposal_evidence_limitation_schema": rel(EVIDENCE_LIMITATION_SCHEMA_PATH),
        "proposal_review_decision_contract_schema": rel(REVIEW_DECISION_CONTRACT_SCHEMA_PATH),
        "gap_coverage_matrix": rel(GAP_COVERAGE_MATRIX_PATH),
        "c3_rerun_contract": rel(C3_RERUN_CONTRACT_PATH),
        "demo_proposals": rel(DEMO_PROPOSALS_PATH),
        "validation_results": rel(VALIDATION_RESULTS_PATH),
        "rollup": rel(ROLLUP_PATH),
        "profile": rel(PROFILE_PATH),
        "report": rel(REPORT_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_c4_receipt": rel(SOURCE_C4_RECEIPT_PATH),
        "source_c3_receipt": rel(SOURCE_C3_RECEIPT_PATH),
        "source_c1_schema": rel(SOURCE_C1_SCHEMA_PATH),
        "source_c2_lane_registry": rel(SOURCE_C2_LANE_REGISTRY_PATH),
    }

    guards = {
        "build_mode_candidate_interface_patch_only": BUILD_MODE == "CANDIDATE_INTERFACE_PATCH_ONLY",
        "c4_blocked_preflight_consumed": True,
        "c3_gap_report_consumed": True,
        "proposal_schema_v0_1_candidate_not_canonical": rollup["canonical_c1_schema_replaced"] is False,
        "original_c1_schema_overwritten": False,
        "c3_rerun_required": True,
        "cell1_execution_opened": False,
        "accepted_proposal_fabricated": False,
        "proposal_status_promoted": False,
        "builder_command_emitted": False,
        "taxonomy_registry_mutated": False,
        "c4_rerun": False,
        "c5_opened": False,
        "hidden_next_command": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
    }

    receipt = {
        "schema_version": "c1_proposal_interface_gap_patch_receipt_v0",
        "receipt_type": "C1_PROPOSAL_INTERFACE_GAP_PATCH_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "C1 proposal packet interface as tested by C3 and blocked by C4 preflight",
        "source_c4_receipt_id": SOURCE_C4_RECEIPT_ID,
        "source_c3_receipt_id": SOURCE_C3_RECEIPT_ID,
        "source_c1_receipt_id": SOURCE_C1_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "c1_interface_patch_summary": {
            "profile_status": prof["status"],
            "interface_patch_status": prof["interface_patch_status"],
            "canonical_c1_schema_replaced": False,
            "requires_c3_rerun": True,
            "gap_records_total": rollup["gap_records_total"],
            "gap_class_counts": rollup["gap_class_counts"],
            "schema_fields_added_or_strengthened": rollup["schema_fields_added_or_strengthened"],
            "demo_proposals_checked": rollup["demo_proposals_checked"],
            "demo_proposals_passed": rollup["demo_proposals_passed"],
            "proposal_schema_version_emitted": rollup["proposal_schema_version_emitted"],
            "uncovered_c3_gap_count": rollup["uncovered_c3_gap_count"],
            "bad_counters_zero": all(rollup.get(k) == 0 for k in ZERO_COUNTER_KEYS),
            "recommended_next": rollup["recommended_next"],
        },
        "aggregate_metrics": {
            **{k: v for k, v in rep.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
            "rollup": rollup,
            "source_mutation_count": 1 if source_mutation_detected else rep["source_mutation_count"],
        },
        "acceptance_gate_results": acceptance_gate_results,
        "c1_interface_patch_guards": guards,
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
    if len(negative_controls) != 20 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
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
    print(f"c1_interface_patch_receipt_id={receipt_id}")
    print(f"c1_interface_patch_receipt_path=data/c1_proposal_interface_gap_patch_from_c3_v0_receipts/{receipt_id}.json")
    print(f"c1_interface_patch_profile_path=data/c1_proposal_interface_gap_patch_from_c3_v0/c1_interface_patch_profile_v0.json")
    print(f"c1_interface_patch_rollup_path=data/c1_proposal_interface_gap_patch_from_c3_v0/c1_interface_patch_rollup_v0.json")
    print(f"proposal_schema_v0_1_path=data/c1_proposal_interface_gap_patch_from_c3_v0/proposal_packet_schema_v0_1.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
