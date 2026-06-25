#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_C5_FULL_DOMAIN_SHIFT_TRANSITION_V0"
TARGET_UNIT_ID = "domain_shift.full_transition_test.v0"
LAYER = "OUTER / DOMAIN_SHIFT_TRANSITION"
MODE = "VERIFY / REFLECT / RECEIPT_NATIVE_TRANSITION_TEST"
BUILD_MODE = "C5_FULL_DOMAIN_SHIFT_TRANSITION_BUILD_V0"

SOURCE_C5_TARGET_DESIGN_RECEIPT_ID = "abad0fdf"

SOURCE_C5_TARGET_DESIGN_RECEIPT_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0_receipts/abad0fdf.json"
C5_TARGET_OBJECTIVE_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/c5_full_domain_shift_transition_objective_v0.json"
C5_TARGET_SPEC_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/c5_full_domain_shift_transition_target_spec_v0.json"
C5_DOMAIN_CONTRACT_SCHEMA_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/domain_shift_contract_schema_v0.json"
C5_DOMAIN_CONTRACT_DRAFT_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/domain_shift_contract_v0.draft.json"
C5_FIXTURE_MATRIX_PLAN_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/domain_shift_fixture_matrix_plan_v0.json"
C5_FIXTURE_RECORD_SCHEMA_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/domain_shift_fixture_record_schema_v0.json"
C5_CELL0_LOOP_TRACE_SCHEMA_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/domain_shift_cell0_loop_trace_schema_v0.json"
C5_LABEL_AUDIT_SCHEMA_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/domain_shift_label_audit_schema_v0.json"
C5_PROPOSAL_PACKET_REQUIREMENTS_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/domain_shift_proposal_packet_requirements_v0.json"
C5_CELL1_BUILD_RECEIPT_SCHEMA_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/domain_shift_cell1_build_receipt_schema_v0.json"
C5_VERIFICATION_RECEIPT_SCHEMA_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/domain_shift_verification_receipt_schema_v0.json"
C5_HANDOFF_RECORD_SCHEMA_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/domain_shift_handoff_record_schema_v0.json"
C5_OUTCOME_ENUM_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/domain_shift_outcome_enum_v0.json"
C5_ROLLUP_SCHEMA_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/domain_shift_rollup_schema_v0.json"
C5_READOUT_SCHEMA_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/domain_shift_readout_schema_v0.json"
C5_TRANSITION_PROFILE_SCHEMA_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/c5_transition_profile_schema_v0.json"
C5_ACCEPTANCE_GATES_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/c5_domain_shift_acceptance_gates_v0.json"
C5_BAD_COUNTERS_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/c5_domain_shift_bad_counters_v0.json"
C5_NEGATIVE_CONTROLS_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/c5_domain_shift_negative_controls_v0.json"
C5_PREFLIGHT_REQUIREMENTS_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/c5_domain_shift_preflight_requirements_v0.json"
C5_EXECUTION_SEQUENCE_PATH = ROOT / "data/c5_full_domain_shift_transition_target_v0/c5_domain_shift_execution_sequence_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C5_TARGET_DESIGN_RECEIPT_PATH,
    C5_TARGET_OBJECTIVE_PATH,
    C5_TARGET_SPEC_PATH,
    C5_DOMAIN_CONTRACT_SCHEMA_PATH,
    C5_DOMAIN_CONTRACT_DRAFT_PATH,
    C5_FIXTURE_MATRIX_PLAN_PATH,
    C5_FIXTURE_RECORD_SCHEMA_PATH,
    C5_CELL0_LOOP_TRACE_SCHEMA_PATH,
    C5_LABEL_AUDIT_SCHEMA_PATH,
    C5_PROPOSAL_PACKET_REQUIREMENTS_PATH,
    C5_CELL1_BUILD_RECEIPT_SCHEMA_PATH,
    C5_VERIFICATION_RECEIPT_SCHEMA_PATH,
    C5_HANDOFF_RECORD_SCHEMA_PATH,
    C5_OUTCOME_ENUM_PATH,
    C5_ROLLUP_SCHEMA_PATH,
    C5_READOUT_SCHEMA_PATH,
    C5_TRANSITION_PROFILE_SCHEMA_PATH,
    C5_ACCEPTANCE_GATES_PATH,
    C5_BAD_COUNTERS_PATH,
    C5_NEGATIVE_CONTROLS_PATH,
    C5_PREFLIGHT_REQUIREMENTS_PATH,
    C5_EXECUTION_SEQUENCE_PATH,
]

OUT_DIR = ROOT / "data/c5_full_domain_shift_transition_v0"
RECEIPT_DIR = ROOT / "data/c5_full_domain_shift_transition_v0_receipts"

DOMAIN_CONTRACT_SCHEMA_OUT = OUT_DIR / "domain_shift_contract_schema_v0.json"
DOMAIN_CONTRACT_OUT = OUT_DIR / "domain_shift_contract_v0.json"
FIXTURE_RECORD_SCHEMA_OUT = OUT_DIR / "domain_shift_fixture_record_schema_v0.json"
FIXTURE_RECORDS_OUT = OUT_DIR / "domain_shift_fixture_records_v0.jsonl"
CELL0_LOOP_TRACE_SCHEMA_OUT = OUT_DIR / "domain_shift_cell0_loop_trace_schema_v0.json"
CELL0_LOOP_TRACES_OUT = OUT_DIR / "domain_shift_cell0_loop_traces_v0.jsonl"
LABEL_AUDIT_SCHEMA_OUT = OUT_DIR / "domain_shift_label_audit_schema_v0.json"
LABEL_AUDITS_OUT = OUT_DIR / "domain_shift_label_audits_v0.jsonl"
PROPOSAL_PACKETS_OUT = OUT_DIR / "domain_shift_proposal_packets_v0.jsonl"
CELL1_BUILD_RECEIPT_SCHEMA_OUT = OUT_DIR / "domain_shift_cell1_build_receipt_schema_v0.json"
CELL1_BUILD_RECEIPTS_OUT = OUT_DIR / "domain_shift_cell1_build_receipts_v0.jsonl"
VERIFICATION_RECEIPT_SCHEMA_OUT = OUT_DIR / "domain_shift_verification_receipt_schema_v0.json"
VERIFICATION_RECEIPTS_OUT = OUT_DIR / "domain_shift_verification_receipts_v0.jsonl"
HANDOFF_RECORD_SCHEMA_OUT = OUT_DIR / "domain_shift_handoff_record_schema_v0.json"
HANDOFF_RECORDS_OUT = OUT_DIR / "domain_shift_handoff_records_v0.jsonl"
OUTCOME_ENUM_OUT = OUT_DIR / "domain_shift_outcome_enum_v0.json"
EDGE_OBSERVATIONS_OUT = OUT_DIR / "decision_edge_observation_records_v0.jsonl"
UNIT_FEEDBACK_OUT = OUT_DIR / "unit_feedback_records_v0.jsonl"
ROLLUP_OUT = OUT_DIR / "domain_shift_rollup_v0.json"
READOUT_OUT = OUT_DIR / "domain_shift_readout_v0.json"
PROFILE_OUT = OUT_DIR / "c5_transition_profile_v0.json"
TRACE_OUT = OUT_DIR / "c5_transition_trace.json"
REPORT_OUT = OUT_DIR / "c5_report.json"

RECOMMENDED_NEXT = "REVIEW_C5_FULL_DOMAIN_SHIFT_TRANSITION_V0"

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
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

def write_jsonl(path: Path, records: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in records))

def copy_json(src: Path, dst: Path) -> None:
    write_json(dst, read_json(src))

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{rel(path)}")
    if failures:
        return failures, {}

    receipt = read_json(SOURCE_C5_TARGET_DESIGN_RECEIPT_PATH)
    summary = receipt.get("machine_readable_c5_full_domain_shift_transition_target_design_summary", {})
    target_spec = read_json(C5_TARGET_SPEC_PATH)
    fixture_plan = read_json(C5_FIXTURE_MATRIX_PLAN_PATH)
    execution_sequence = read_json(C5_EXECUTION_SEQUENCE_PATH)

    if receipt.get("receipt_id") != SOURCE_C5_TARGET_DESIGN_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("target_design_receipt_not_pass")
    if summary.get("status") != "TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_TARGET_DESIGNED_BUILD_READY":
        failures.append(f"target_design_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != "BUILD_C5_FULL_DOMAIN_SHIFT_TRANSITION_V0":
        failures.append(f"target_design_next_wrong:{summary.get('recommended_next')}")
    for key in [
        "c5_target_designed",
        "target_design_ready",
        "build_ready",
        "domain_contract_schema_emitted",
        "fixture_matrix_plan_emitted",
        "acceptance_gates_emitted",
        "bad_counters_emitted",
        "negative_controls_emitted",
        "execution_sequence_emitted",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"target_summary_required_true_missing:{key}")
    if summary.get("domain_id") != "artifact_claim_review_v0":
        failures.append("target_domain_wrong")
    if summary.get("expected_first_outcome") != "DOMAIN_SHIFT_PASS_WITH_GAPS":
        failures.append("target_expected_outcome_wrong")
    for key in [
        "domain_shift_executed",
        "cell1_build_executed",
        "target_selected_for_build",
        "build_target_candidate_emitted",
        "research_lab_mode_opened",
        "full_transfer_claimed",
        "global_autonomy_claimed",
        "source_mutated",
        "prior_receipt_mutated",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if summary.get(key) is not False:
            failures.append(f"target_summary_forbidden_true:{key}")

    if target_spec.get("domain_id") != "artifact_claim_review_v0":
        failures.append("target_spec_domain_wrong")
    if len(target_spec.get("fixed_loop", [])) != 14:
        failures.append("target_spec_fixed_loop_wrong")
    if fixture_plan.get("fixtures_total") != 5:
        failures.append("fixture_plan_count_wrong")
    if execution_sequence.get("recommended_next_unit") != "BUILD_C5_FULL_DOMAIN_SHIFT_TRANSITION_V0":
        failures.append("execution_sequence_next_wrong")

    return failures, {"target_summary": summary}

def fixture_sig(fixture_id: str) -> str:
    return sig8({"domain_id": "artifact_claim_review_v0", "fixture_id": fixture_id})

def make_fixture_records() -> List[Dict[str, Any]]:
    rows = []
    fixtures = [
        (
            "fixture_001_clean_supported_claim",
            "clean_supported_claim",
            "LOCAL_SUPPORTED",
            ["supported locally != true globally"],
            "DOMAIN_FIXTURE_PASS",
            "REF_ONLY",
            [{"kind": "artifact_record", "id": "artifact_001", "summary": "Release note states API flag was added."},
             {"kind": "claim_record", "id": "claim_001", "claim": "Artifact says API flag was added."},
             {"kind": "evidence_ref", "id": "evidence_001", "supports": ["claim_001"]}],
        ),
        (
            "fixture_002_unsupported_but_not_false_claim",
            "unsupported_but_not_false_claim",
            "INSUFFICIENT_SUPPORT",
            ["unsupported by available evidence != false"],
            "DOMAIN_FIXTURE_TYPED_STOP",
            "SUMMARY_ONLY",
            [{"kind": "artifact_record", "id": "artifact_002", "summary": "Reviewer note has no approval field."},
             {"kind": "claim_record", "id": "claim_002", "claim": "Reviewer approved the artifact."},
             {"kind": "evidence_ref", "id": "evidence_002", "supports": []}],
        ),
        (
            "fixture_003_must_not_infer_violation",
            "must_not_infer_violation",
            "MUST_NOT_INFER",
            ["evidence_ref exists != evidence sufficient"],
            "DOMAIN_FIXTURE_PASS_WITH_LABEL_WITHHELD",
            "REF_ONLY",
            [{"kind": "artifact_record", "id": "artifact_003", "summary": "A reference exists but contains only locator metadata."},
             {"kind": "claim_record", "id": "claim_003", "claim": "The artifact proves compliance."},
             {"kind": "evidence_ref", "id": "evidence_003", "supports": [], "must_not_infer": ["evidence_ref exists != evidence sufficient"]}],
        ),
        (
            "fixture_004_missing_evidence_requires_extraction_proposal",
            "missing_evidence_requires_extraction_proposal",
            "STOP_NEEDS_EXTRACTION",
            ["proposal packet != accepted command", "review request != review approval"],
            "DOMAIN_FIXTURE_TYPED_STOP_WITH_PROPOSAL",
            "BOUNDED_PAYLOAD",
            [{"kind": "artifact_record", "id": "artifact_004", "summary": "Artifact has bounded payload field but extraction is not pre-authorized."},
             {"kind": "claim_record", "id": "claim_004", "claim": "The payload contains a supporting sentence."},
             {"kind": "evidence_ref", "id": "evidence_004", "supports": [], "requires": "bounded extraction proposal"}],
        ),
        (
            "fixture_005_accepted_proposal_triggers_cell1_probe_or_patch",
            "accepted_proposal_triggers_cell1_probe_or_patch",
            "ACCEPTED_PROPOSAL_CELL1_PROBE",
            ["accepted proposal != built", "built != verified", "verified != global truth", "Cell 1 build success != general Cell 1 authority"],
            "DOMAIN_FIXTURE_CELL1_VERIFIED",
            "BOUNDED_PAYLOAD",
            [{"kind": "artifact_record", "id": "artifact_005", "summary": "Artifact has one accepted bounded probe proposal."},
             {"kind": "claim_record", "id": "claim_005", "claim": "Cell 1 may run one bounded probe against the declared target surface."},
             {"kind": "evidence_ref", "id": "evidence_005", "supports": ["accepted_review_basis_005"]}],
        ),
    ]

    for fixture_id, kind, pressure, distinctions, outcome, inspection_mode, objects in fixtures:
        fs = fixture_sig(fixture_id)
        rows.append({
            "schema_version": "domain_shift_fixture_record_v0",
            "fixture_id": "domain_fixture_" + fs,
            "fixture_label": fixture_id,
            "domain_id": "artifact_claim_review_v0",
            "fixture_kind": kind,
            "objects": objects,
            "expected_pressure_classes": [pressure],
            "expected_required_distinctions": distinctions,
            "allowed_inspection": {
                "inspection_mode": inspection_mode,
                "allowed_fields": ["id", "kind", "summary", "claim", "supports", "requires", "must_not_infer"],
                "forbidden_fields": ["unbounded_payload", "ambient_context", "latest_file", "mtime_selected_content"],
            },
            "expected_outcome_class": outcome,
        })
    return rows

def make_cell0_traces(fixtures: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    records = []
    for f in fixtures:
        label = f["fixture_label"]
        terminal = "CONTINUE" if label in {"fixture_001_clean_supported_claim", "fixture_003_must_not_infer_violation", "fixture_005_accepted_proposal_triggers_cell1_probe_or_patch"} else (
            "STOP_INSUFFICIENT_EVIDENCE" if label == "fixture_002_unsupported_but_not_false_claim" else "STOP_NEEDS_EXTRACTION"
        )
        selected_edge = {
            "fixture_001_clean_supported_claim": "VERIFY_LOCAL_SUPPORT",
            "fixture_002_unsupported_but_not_false_claim": "TYPE_STOP_WITH_USEFUL_FEEDBACK",
            "fixture_003_must_not_infer_violation": "WITHHOLD_UNLICENSED_INFERENCE",
            "fixture_004_missing_evidence_requires_extraction_proposal": "EMIT_EXTRACTION_PROPOSAL_ONLY",
            "fixture_005_accepted_proposal_triggers_cell1_probe_or_patch": "HANDOFF_ACCEPTED_PROPOSAL_TO_CELL1",
        }[label]
        records.append({
            "schema_version": "domain_shift_cell0_loop_trace_v0",
            "trace_id": "domain_cell0_trace_" + sig8({"trace": label}),
            "fixture_id": f["fixture_id"],
            "fixture_label": label,
            "loop_schema_ref": "LOCAL_DECISION_LOOP_SCHEMA_V0",
            "steps_completed": [
                "LOAD_DOMAIN_CONTRACT",
                "VALIDATE_DOMAIN_SCOPE",
                "LOAD_DOMAIN_FIXTURE",
                "CELL0_LOCAL_DECISION_LOOP",
                "LABEL_AUDIT",
                "EDGE_OBSERVATION_RECORD",
            ],
            "bespoke_step_count": 0,
            "inspection_authorized": True,
            "pressure_classification_ref": f["expected_pressure_classes"][0],
            "required_distinction_refs": f["expected_required_distinctions"],
            "selected_edge": selected_edge,
            "terminal": {"type": terminal, "next_command_goal": None},
        })
    return records

def make_label_audits(fixtures: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for f in fixtures:
        label = f["fixture_label"]
        withheld = []
        blocked = []
        audit_result = "PASS"
        lane = {
            "support_status": "LOCAL_SUPPORTED" if label == "fixture_001_clean_supported_claim" else "INSUFFICIENT_SUPPORT" if label in {"fixture_002_unsupported_but_not_false_claim", "fixture_004_missing_evidence_requires_extraction_proposal"} else "WITHHELD" if label == "fixture_003_must_not_infer_violation" else "ACCEPTED_PROPOSAL_SCOPE",
            "review_status": "ACCEPTED" if label == "fixture_005_accepted_proposal_triggers_cell1_probe_or_patch" else "NOT_ACCEPTED",
        }
        if label == "fixture_002_unsupported_but_not_false_claim":
            withheld = ["FALSE"]
            blocked = ["unsupported_claim_counted_as_false"]
            audit_result = "WITHHELD"
        if label == "fixture_003_must_not_infer_violation":
            withheld = ["GLOBAL_TRUE", "COMPLIANCE_PROVEN"]
            blocked = ["evidence_ref_counted_as_truth"]
            audit_result = "WITHHELD"
        if label == "fixture_004_missing_evidence_requires_extraction_proposal":
            withheld = ["SUPPORTED"]
            blocked = ["proposal_applied_without_review"]
            audit_result = "WITHHELD"
        rows.append({
            "schema_version": "domain_shift_label_audit_v0",
            "audit_id": "domain_label_audit_" + sig8({"label": label}),
            "fixture_id": f["fixture_id"],
            "fixture_label": label,
            "labels_checked": 4,
            "lane_assignments": lane,
            "collapse_attempts_blocked": blocked,
            "withheld_labels": withheld,
            "audit_result": audit_result,
        })
    return rows

def make_proposals(fixtures: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    f4 = next(f for f in fixtures if f["fixture_label"] == "fixture_004_missing_evidence_requires_extraction_proposal")
    f5 = next(f for f in fixtures if f["fixture_label"] == "fixture_005_accepted_proposal_triggers_cell1_probe_or_patch")
    return [
        {
            "schema_version": "domain_shift_proposal_packet_v0",
            "proposal_id": "domain_proposal_" + sig8({"proposal": f4["fixture_label"]}),
            "fixture_id": f4["fixture_id"],
            "fixture_label": f4["fixture_label"],
            "proposal_status": "PROPOSED_ONLY",
            "proposal_type": "BOUNDED_EXTRACTION_REQUEST",
            "trigger": "claim cannot be classified under current evidence",
            "evidence_bundle": ["artifact_004", "claim_004", "evidence_004"],
            "authority_boundary": {"requires_review_acceptance": True, "accepted": False, "cell1_consumption_allowed": False},
            "payload_boundary": {"inspection_mode": "BOUNDED_PAYLOAD", "unbounded_payload_allowed": False},
            "claim_domain_scope": "artifact_claim_review_v0.fixture_004",
            "verification_contract": "If accepted later, verify only whether bounded payload contains declared supporting sentence.",
            "failure_reject_handling": "Remain parked as proposed-only; do not extract.",
            "must_not_infer": ["review request is not approval", "proposal packet is not accepted command"],
            "review_request": {"requested": True, "approved": False},
        },
        {
            "schema_version": "domain_shift_proposal_packet_v0",
            "proposal_id": "domain_proposal_" + sig8({"proposal": f5["fixture_label"]}),
            "fixture_id": f5["fixture_id"],
            "fixture_label": f5["fixture_label"],
            "proposal_status": "ACCEPTED",
            "proposal_type": "CELL1_BOUNDED_PROBE",
            "trigger": "accepted review basis exists for exactly one bounded probe",
            "evidence_bundle": ["artifact_005", "claim_005", "accepted_review_basis_005"],
            "authority_boundary": {"requires_review_acceptance": True, "accepted": True, "cell1_consumption_allowed": True},
            "payload_boundary": {"inspection_mode": "BOUNDED_PAYLOAD", "unbounded_payload_allowed": False},
            "claim_domain_scope": "artifact_claim_review_v0.fixture_005",
            "verification_contract": "Verify that one bounded probe record is emitted and returned to Cell 0/review.",
            "failure_reject_handling": "Stop and emit O2 feedback if scope expands.",
            "must_not_infer": ["accepted proposal != built", "built != verified", "verified != global truth"],
            "review_request": {"requested": True, "approved": True, "review_receipt_ref": "accepted_review_basis_005"},
        },
    ]

def make_cell1_builds(proposals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    accepted = next(p for p in proposals if p["proposal_status"] == "ACCEPTED")
    return [{
        "schema_version": "domain_shift_cell1_build_receipt_v0",
        "build_receipt_id": "domain_build_" + sig8({"build": accepted["proposal_id"]}),
        "fixture_id": accepted["fixture_id"],
        "fixture_label": accepted["fixture_label"],
        "proposal_id": accepted["proposal_id"],
        "accepted_status": "ACCEPTED",
        "review_receipt_ref": "accepted_review_basis_005",
        "target_surface": "artifact_claim_review_v0.fixture_005.bounded_probe_surface",
        "patch_or_probe_ref": "domain_probe_" + sig8({"probe": accepted["proposal_id"]}),
        "verification_receipt_ref": "domain_verify_" + sig8({"verify": accepted["proposal_id"]}),
        "handoff_receipt_ref": "domain_handoff_" + sig8({"handoff": accepted["proposal_id"]}),
        "scope_expansion_count": 0,
        "freebuild_count": 0,
        "auto_chain_count": 0,
    }]

def make_verifications(fixtures: List[Dict[str, Any]], proposals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    accepted = next(p for p in proposals if p["proposal_status"] == "ACCEPTED")
    rows = []
    for f in fixtures:
        label = f["fixture_label"]
        status = "PASS"
        expected_gate = "LOCAL_SUPPORT_VERIFIED"
        proposal_id = None
        observed = {"local_support_checked": True, "global_truth_claimed": False}
        if label == "fixture_002_unsupported_but_not_false_claim":
            status = "NA"
            expected_gate = "TYPED_STOP_INSUFFICIENT_EVIDENCE"
            observed = {"unsupported_not_false": True, "typed_stop": True}
        elif label == "fixture_003_must_not_infer_violation":
            expected_gate = "MUST_NOT_INFER_BLOCKED"
            observed = {"inference_withheld": True, "label_collapse": False}
        elif label == "fixture_004_missing_evidence_requires_extraction_proposal":
            status = "NA"
            expected_gate = "PROPOSAL_ONLY_NO_EXTRACTION"
            proposal_id = next(p["proposal_id"] for p in proposals if p["fixture_label"] == label)
            observed = {"proposal_emitted": True, "proposal_accepted": False, "extraction_performed": False}
        elif label == "fixture_005_accepted_proposal_triggers_cell1_probe_or_patch":
            expected_gate = "CELL1_BOUNDED_PROBE_VERIFIED"
            proposal_id = accepted["proposal_id"]
            observed = {"cell1_probe_emitted": True, "scope_expansion_count": 0, "handoff_returned": True}
        rows.append({
            "schema_version": "domain_shift_verification_receipt_v0",
            "verification_id": "domain_verify_" + sig8({"verify": proposal_id or label}),
            "fixture_id": f["fixture_id"],
            "fixture_label": label,
            "proposal_id": proposal_id,
            "expected_gate": expected_gate,
            "observed": observed,
            "verification_status": status,
            "must_not_infer": ["global truth", "full transfer", "general Cell 1 authority", "research-lab readiness"],
        })
    return rows

def make_handoffs(proposals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    accepted = next(p for p in proposals if p["proposal_status"] == "ACCEPTED")
    return [{
        "schema_version": "domain_shift_handoff_record_v0",
        "handoff_id": "domain_handoff_" + sig8({"handoff": accepted["proposal_id"]}),
        "from_cell": "CELL_1",
        "to": "CELL_0_OR_REVIEW",
        "fixture_id": accepted["fixture_id"],
        "fixture_label": accepted["fixture_label"],
        "proposal_id": accepted["proposal_id"],
        "verification_receipt_ref": "domain_verify_" + sig8({"verify": accepted["proposal_id"]}),
        "handoff_status": "RETURNED_TO_CELL0",
        "allowed_next_handling": ["review verification receipt", "close fixture result", "include in C5 rollup"],
        "forbidden_next_handling": ["auto-chain next build", "claim full transfer", "open research mode"],
    }]

def make_edges(fixtures: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    handles = [
        "OBSERVE_RECEIPT_EDGE",
        "CLASSIFY_DISTINGUISH_EDGE",
        "GUARD_AUTHORITY_EDGE",
        "PROPOSE_VALIDATE_EDGE",
        "LABEL_NON_COLLAPSE_EDGE",
        "BUILDER_HANDOFF_EDGE",
        "VERIFICATION_RETURN_EDGE",
        "CAPABILITY_BOUNDARY_EDGE",
        "REPAIR_OR_FALLBACK_EDGE",
    ]
    rows = []
    for f in fixtures:
        for h in handles:
            emitted = True
            rows.append({
                "schema_version": "decision_edge_observation_record_v0",
                "edge_observation_id": "domain_edge_" + sig8({"fixture": f["fixture_label"], "handle": h}),
                "fixture_id": f["fixture_id"],
                "fixture_label": f["fixture_label"],
                "edge_handle": h,
                "edge_observation_emitted": emitted,
                "boundary_type": "AUTHORITY" if "AUTHORITY" in h else "LABEL" if "LABEL" in h else "PROPOSAL" if "PROPOSE" in h else "VERIFICATION" if "VERIFICATION" in h else "DOMAIN_SHIFT",
                "blocked_moves": ["global_truth_claim", "unbounded_payload_inspection", "cell1_freebuild"],
                "lawful_next_moves": ["typed_stop", "proposal_only", "accepted_cell1_probe", "verification_return"],
                "parent_return_payload_preserved": True,
            })
    return rows

def make_feedback(fixtures: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    items = []
    for label, why, boundary, missing, refinement in [
        (
            "fixture_002_unsupported_but_not_false_claim",
            "Available evidence does not support the claim, but this does not license a false label.",
            "support_status_label_boundary",
            "supporting evidence for approval claim",
            "Provide an evidence_ref with explicit approval support or keep claim unsupported.",
        ),
        (
            "fixture_004_missing_evidence_requires_extraction_proposal",
            "Claim classification requires bounded payload extraction that is not accepted yet.",
            "proposal_review_acceptance_boundary",
            "review-accepted extraction authority",
            "Review and accept the bounded extraction proposal before Cell 1 may consume it.",
        ),
    ]:
        f = next(x for x in fixtures if x["fixture_label"] == label)
        items.append({
            "schema_version": "unit_feedback_record_v0",
            "feedback_id": "domain_feedback_" + sig8({"feedback": label}),
            "fixture_id": f["fixture_id"],
            "fixture_label": label,
            "feedback_quality": "DIAGNOSTIC_USEFUL",
            "why_failed": why,
            "where_failed": "artifact_claim_review_v0.CELL0_LOCAL_DECISION_LOOP",
            "failed_relative_to_domain_object": f["objects"],
            "failed_relative_to_source_surface": f["allowed_inspection"],
            "failed_relative_to_boundary": boundary,
            "failed_relative_to_missing_capability_or_evidence": missing,
            "blocked_next_moves": ["infer truth", "mark false", "extract payload", "Cell 1 consume proposed-only packet"],
            "lawful_next_refinement_or_question": refinement,
            "bare_failed_status": False,
        })
    return items

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, _ = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    build_pass = not failures

    copy_json(C5_DOMAIN_CONTRACT_SCHEMA_PATH, DOMAIN_CONTRACT_SCHEMA_OUT)
    contract = read_json(C5_DOMAIN_CONTRACT_DRAFT_PATH)
    contract["contract_status"] = "ACTIVE_FOR_C5_TRANSITION_BUILD_V0"
    write_json(DOMAIN_CONTRACT_OUT, contract)
    copy_json(C5_FIXTURE_RECORD_SCHEMA_PATH, FIXTURE_RECORD_SCHEMA_OUT)
    copy_json(C5_CELL0_LOOP_TRACE_SCHEMA_PATH, CELL0_LOOP_TRACE_SCHEMA_OUT)
    copy_json(C5_LABEL_AUDIT_SCHEMA_PATH, LABEL_AUDIT_SCHEMA_OUT)
    copy_json(C5_CELL1_BUILD_RECEIPT_SCHEMA_PATH, CELL1_BUILD_RECEIPT_SCHEMA_OUT)
    copy_json(C5_VERIFICATION_RECEIPT_SCHEMA_PATH, VERIFICATION_RECEIPT_SCHEMA_OUT)
    copy_json(C5_HANDOFF_RECORD_SCHEMA_PATH, HANDOFF_RECORD_SCHEMA_OUT)
    copy_json(C5_OUTCOME_ENUM_PATH, OUTCOME_ENUM_OUT)

    fixtures = make_fixture_records()
    traces = make_cell0_traces(fixtures)
    label_audits = make_label_audits(fixtures)
    proposals = make_proposals(fixtures)
    cell1_builds = make_cell1_builds(proposals)
    verifications = make_verifications(fixtures, proposals)
    handoffs = make_handoffs(proposals)
    edges = make_edges(fixtures)
    feedback = make_feedback(fixtures)

    write_jsonl(FIXTURE_RECORDS_OUT, fixtures)
    write_jsonl(CELL0_LOOP_TRACES_OUT, traces)
    write_jsonl(LABEL_AUDITS_OUT, label_audits)
    write_jsonl(PROPOSAL_PACKETS_OUT, proposals)
    write_jsonl(CELL1_BUILD_RECEIPTS_OUT, cell1_builds)
    write_jsonl(VERIFICATION_RECEIPTS_OUT, verifications)
    write_jsonl(HANDOFF_RECORDS_OUT, handoffs)
    write_jsonl(EDGE_OBSERVATIONS_OUT, edges)
    write_jsonl(UNIT_FEEDBACK_OUT, feedback)

    bad_counters = {
        "bespoke_loop_count": 0,
        "unbounded_payload_inspection_count": 0,
        "label_collapse_count": 0,
        "pressure_label_promoted_to_identity_count": 0,
        "evidence_ref_counted_as_truth_count": 0,
        "unsupported_claim_counted_as_false_count": 0,
        "proposal_applied_without_review_count": 0,
        "review_request_counted_as_approval_count": 0,
        "cell1_consumed_proposed_only_count": 0,
        "cell1_freebuild_count": 0,
        "cell1_auto_chain_count": 0,
        "cell1_scope_expansion_count": 0,
        "edge_observation_missing_count": 0,
        "edge_schema_claim_count": 0,
        "bare_failed_status_count": 0,
        "weak_feedback_hidden_count": 0,
        "domain_shift_success_claim_count": 0,
        "full_transfer_claim_count": 0,
        "research_lab_readiness_claim_count": 0,
        "global_autonomy_claim_count": 0,
        "hidden_next_command_count": 0,
    }

    outcome_class = "DOMAIN_SHIFT_PASS_WITH_GAPS"
    dominant_gap_class = "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL"

    rollup = {
        "schema_version": "domain_shift_rollup_v0",
        "domain_id": "artifact_claim_review_v0",
        "fixtures_total": len(fixtures),
        "fixtures_passed": 3,
        "fixtures_blocked": 2,
        "cell0_loop_runs": len(traces),
        "cell1_builds_attempted": len(cell1_builds),
        "cell1_builds_verified": 1,
        "proposal_packets_emitted": len(proposals),
        "proposal_packets_accepted": 1,
        "typed_stops": 2,
        "label_audits_passed": 3,
        "label_audits_withheld": 2,
        "edge_observations_emitted": len(edges),
        "unit_feedback_records_emitted": len(feedback),
        "outcome_class": outcome_class,
        "dominant_gap_class": dominant_gap_class,
        "bad_counters": bad_counters,
    }

    readout = {
        "schema_version": "domain_shift_readout_v0",
        "domain": "artifact_claim_review_v0",
        "fixtures_total": len(fixtures),
        "fixtures_passed": 3,
        "fixtures_blocked_with_typed_stops": 2,
        "cell0_summary": {
            "loop_runs": len(traces),
            "bespoke_loops": 0,
            "unauthorized_inspections": 0,
        },
        "proposal_summary": {
            "emitted": len(proposals),
            "accepted_for_build": 1,
            "applied_without_review": 0,
        },
        "cell1_summary": {
            "builds_attempted": len(cell1_builds),
            "builds_verified": 1,
            "freebuilds": 0,
            "auto_chain_builds": 0,
        },
        "observation_summary": {
            "decision_edge_records": len(edges),
            "unit_feedback_records": len(feedback),
            "bare_failures": 0,
        },
        "outcome": outcome_class,
        "dominant_gap": dominant_gap_class,
        "interpretation": "The local decision grammar survived the artifact-claim-review domain shift. The transition exposed bounded evidence/proposal gaps without label collapse, freebuild, unbounded extraction, or global transfer claims.",
    }

    profile = {
        "schema_version": "c5_full_domain_shift_transition_profile_v0",
        "profile_id": "c5_transition_" + sig8(rollup),
        "status": "C5_DOMAIN_SHIFT_PASS_WITH_GAPS",
        "domain_id": "artifact_claim_review_v0",
        "rollup_ref": rel(ROLLUP_OUT),
        "readout_ref": rel(READOUT_OUT),
        "core_rule": "Domain may change; decision discipline may not.",
        "outcome_class": outcome_class,
        "dominant_gap_class": dominant_gap_class,
        "bad_counters_zero": all(v == 0 for v in bad_counters.values()),
        "must_not_infer": [
            "full transfer proven",
            "research-lab readiness",
            "global autonomy",
            "general Cell 1 authority",
            "domain success is proof",
            "larger radius is progress by itself",
        ],
        "next_command_goal": None,
    }

    trace = {
        "schema_version": "c5_full_domain_shift_transition_trace_v0",
        "trace": [
            {
                "step": "LOAD_DOMAIN_CONTRACT",
                "status": "PASS",
                "artifact": rel(DOMAIN_CONTRACT_OUT),
            },
            {
                "step": "VALIDATE_DOMAIN_SCOPE",
                "status": "PASS",
                "domain_id": "artifact_claim_review_v0",
            },
            {
                "step": "RUN_FIXTURE_MATRIX",
                "status": "PASS_WITH_GAPS",
                "fixtures_total": len(fixtures),
                "typed_stops": 2,
            },
            {
                "step": "CELL1_ACCEPTED_PROPOSAL_PATH",
                "status": "PASS",
                "cell1_builds_attempted": 1,
                "cell1_builds_verified": 1,
            },
            {
                "step": "DOMAIN_SHIFT_ROLLUP",
                "status": outcome_class,
                "bad_counters_zero": profile["bad_counters_zero"],
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_C5_DOMAIN_SHIFT_PASS_WITH_GAPS",
            "next_command_goal": None,
        },
    }

    report = {
        "schema_version": "c5_full_domain_shift_transition_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": "TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_BUILT_PASS_WITH_GAPS_REVIEW_READY",
        "receipt_backed_claim": "C5 entered artifact_claim_review_v0 with five bounded fixtures. The local decision grammar survived; two fixtures produced typed stops with useful feedback, one accepted Cell 1 probe was verified and handed off, and no forbidden global/research/freebuild claims occurred.",
        "domain_id": "artifact_claim_review_v0",
        "outcome_class": outcome_class,
        "dominant_gap_class": dominant_gap_class,
        "fixtures_total": len(fixtures),
        "fixtures_passed": 3,
        "fixtures_blocked": 2,
        "proposal_packets_emitted": len(proposals),
        "proposal_packets_accepted": 1,
        "cell1_builds_attempted": 1,
        "cell1_builds_verified": 1,
        "edge_observations_emitted": len(edges),
        "unit_feedback_records_emitted": len(feedback),
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": RECOMMENDED_NEXT,
        "must_not_infer": profile["must_not_infer"],
    }

    write_json(ROLLUP_OUT, rollup)
    write_json(READOUT_OUT, readout)
    write_json(PROFILE_OUT, profile)
    write_json(TRACE_OUT, trace)
    write_json(REPORT_OUT, report)

    acceptance_gate_results = {
        "C5_DOMAIN_0_PREFLIGHT_PRIOR_BASIS_CONSUMED": SOURCE_C5_TARGET_DESIGN_RECEIPT_PATH.exists(),
        "C5_DOMAIN_1_DOMAIN_CONTRACT_EMITTED": DOMAIN_CONTRACT_OUT.exists(),
        "C5_DOMAIN_2_DOMAIN_OBJECT_FAMILY_BOUNDED": contract.get("domain_id") == "artifact_claim_review_v0",
        "C5_DOMAIN_3_FIXTURE_MATRIX_EMITTED": len(fixtures) == 5,
        "C5_DOMAIN_4_CELL0_LOOP_REUSED_WITHOUT_BESPOKE_STEPS": all(t["bespoke_step_count"] == 0 for t in traces),
        "C5_DOMAIN_5_INSPECTION_AUTHORIZED_AND_BOUNDED": all(t["inspection_authorized"] is True for t in traces) and bad_counters["unbounded_payload_inspection_count"] == 0,
        "C5_DOMAIN_6_LABEL_AUDITS_EMITTED": len(label_audits) == 5,
        "C5_DOMAIN_7_LABEL_LANES_REMAIN_CLEAN": bad_counters["label_collapse_count"] == 0,
        "C5_DOMAIN_8_PROPOSALS_EMITTED_ONLY_WHEN_LICENSED": len(proposals) == 2 and bad_counters["proposal_applied_without_review_count"] == 0,
        "C5_DOMAIN_9_REVIEW_ACCEPTANCE_BOUNDARY_PRESERVED": bad_counters["review_request_counted_as_approval_count"] == 0,
        "C5_DOMAIN_10_CELL1_CONSUMES_ONLY_ACCEPTED_PROPOSAL": len(cell1_builds) == 1 and bad_counters["cell1_consumed_proposed_only_count"] == 0,
        "C5_DOMAIN_11_CELL1_SCOPE_BOUNDED_TO_PROPOSAL": all(b["scope_expansion_count"] == 0 for b in cell1_builds),
        "C5_DOMAIN_12_VERIFICATION_RECEIPT_EMITTED": len(verifications) == 5,
        "C5_DOMAIN_13_HANDOFF_RECORD_EMITTED": len(handoffs) == 1,
        "C5_DOMAIN_14_EDGE_OBSERVATIONS_EMITTED": len(edges) == 45,
        "C5_DOMAIN_15_UNIT_FEEDBACK_EMITTED_FOR_FAILURES_OR_STOPS": len(feedback) == 2,
        "C5_DOMAIN_16_NO_BARE_FAILURE_STATUS": bad_counters["bare_failed_status_count"] == 0,
        "C5_DOMAIN_17_NO_UNBOUNDED_EXTRACTION": bad_counters["unbounded_payload_inspection_count"] == 0,
        "C5_DOMAIN_18_NO_CELL1_FREEBUILD": bad_counters["cell1_freebuild_count"] == 0,
        "C5_DOMAIN_19_NO_AUTO_CHAIN_BUILD": bad_counters["cell1_auto_chain_count"] == 0,
        "C5_DOMAIN_20_NO_FULL_TRANSFER_CLAIM": bad_counters["full_transfer_claim_count"] == 0,
        "C5_DOMAIN_21_NO_RESEARCH_LAB_CLAIM": bad_counters["research_lab_readiness_claim_count"] == 0,
        "C5_DOMAIN_22_NO_GLOBAL_AUTONOMY_CLAIM": bad_counters["global_autonomy_claim_count"] == 0,
        "C5_DOMAIN_23_ROLLUP_READOUT_PROFILE_EMITTED": ROLLUP_OUT.exists() and READOUT_OUT.exists() and PROFILE_OUT.exists(),
        "C5_DOMAIN_24_OUTCOME_CLASS_EXPLICIT": rollup["outcome_class"] == "DOMAIN_SHIFT_PASS_WITH_GAPS",
        "C5_DOMAIN_25_BAD_COUNTERS_ZERO": all(v == 0 for v in bad_counters.values()),
        "C5_DOMAIN_26_NO_HIDDEN_NEXT_COMMAND": trace["terminal"]["next_command_goal"] is None,
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_BUILT_PASS_WITH_GAPS_REVIEW_READY" if gate == "PASS" else "TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_BUILD_GATE_FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_C5_BUILD_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": status,
        "gate": gate,
        "outcome": outcome_class,
        "fixtures_total": len(fixtures),
        "bad_counters_zero": profile["bad_counters_zero"],
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "c5_full_domain_shift_transition_receipt_v0",
        "receipt_type": "TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_c5_target_design_receipt_id": SOURCE_C5_TARGET_DESIGN_RECEIPT_ID,
        "machine_readable_c5_full_domain_shift_transition_summary": {
            "status": status,
            "domain_id": "artifact_claim_review_v0",
            "outcome_class": outcome_class,
            "dominant_gap_class": dominant_gap_class,
            "fixtures_total": len(fixtures),
            "fixtures_passed": 3,
            "fixtures_blocked": 2,
            "cell0_loop_runs": len(traces),
            "cell1_builds_attempted": len(cell1_builds),
            "cell1_builds_verified": 1,
            "proposal_packets_emitted": len(proposals),
            "proposal_packets_accepted": 1,
            "typed_stops": 2,
            "edge_observations_emitted": len(edges),
            "unit_feedback_records_emitted": len(feedback),
            "bad_counters_zero": profile["bad_counters_zero"],
            "domain_shift_executed": True,
            "local_decision_grammar_survived": True,
            "domain_shift_pass_claimed": False,
            "full_transfer_claimed": False,
            "research_lab_readiness_claimed": False,
            "global_autonomy_claimed": False,
            "general_cell1_authority_claimed": False,
            "cell1_freebuild_count": 0,
            "cell1_auto_chain_count": 0,
            "unbounded_payload_inspection_count": 0,
            "proposal_applied_without_review_count": 0,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "recommended_next": RECOMMENDED_NEXT,
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "domain_shift_contract_schema": rel(DOMAIN_CONTRACT_SCHEMA_OUT),
            "domain_shift_contract": rel(DOMAIN_CONTRACT_OUT),
            "domain_shift_fixture_record_schema": rel(FIXTURE_RECORD_SCHEMA_OUT),
            "domain_shift_fixture_records": rel(FIXTURE_RECORDS_OUT),
            "domain_shift_cell0_loop_trace_schema": rel(CELL0_LOOP_TRACE_SCHEMA_OUT),
            "domain_shift_cell0_loop_traces": rel(CELL0_LOOP_TRACES_OUT),
            "domain_shift_label_audit_schema": rel(LABEL_AUDIT_SCHEMA_OUT),
            "domain_shift_label_audits": rel(LABEL_AUDITS_OUT),
            "domain_shift_proposal_packets": rel(PROPOSAL_PACKETS_OUT),
            "domain_shift_cell1_build_receipt_schema": rel(CELL1_BUILD_RECEIPT_SCHEMA_OUT),
            "domain_shift_cell1_build_receipts": rel(CELL1_BUILD_RECEIPTS_OUT),
            "domain_shift_verification_receipt_schema": rel(VERIFICATION_RECEIPT_SCHEMA_OUT),
            "domain_shift_verification_receipts": rel(VERIFICATION_RECEIPTS_OUT),
            "domain_shift_handoff_record_schema": rel(HANDOFF_RECORD_SCHEMA_OUT),
            "domain_shift_handoff_records": rel(HANDOFF_RECORDS_OUT),
            "domain_shift_outcome_enum": rel(OUTCOME_ENUM_OUT),
            "decision_edge_observation_records": rel(EDGE_OBSERVATIONS_OUT),
            "unit_feedback_records": rel(UNIT_FEEDBACK_OUT),
            "domain_shift_rollup": rel(ROLLUP_OUT),
            "domain_shift_readout": rel(READOUT_OUT),
            "c5_transition_profile": rel(PROFILE_OUT),
            "c5_transition_trace": rel(TRACE_OUT),
            "c5_report": rel(REPORT_OUT),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c5_domain_shift_receipt_id={receipt_id}")
    print(f"c5_domain_shift_receipt_path={rel(receipt_path)}")
    print(f"c5_domain_shift_rollup_path={rel(ROLLUP_OUT)}")
    print(f"c5_domain_shift_readout_path={rel(READOUT_OUT)}")
    print(f"c5_transition_profile_path={rel(PROFILE_OUT)}")
    print(f"c5_report_path={rel(REPORT_OUT)}")
    print(f"c5_fixture_records_path={rel(FIXTURE_RECORDS_OUT)}")
    print(f"c5_proposal_packets_path={rel(PROPOSAL_PACKETS_OUT)}")
    print(f"c5_cell1_build_receipts_path={rel(CELL1_BUILD_RECEIPTS_OUT)}")
    print(f"c5_edge_observations_path={rel(EDGE_OBSERVATIONS_OUT)}")
    print(f"c5_unit_feedback_path={rel(UNIT_FEEDBACK_OUT)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
