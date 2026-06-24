#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PROVIDE_OR_REVIEW_ONE_ACCEPTED_PROPOSAL_PACKET_FOR_C4_CONSUMPTION_V0"
TARGET_UNIT_ID = "review.accepted_proposal_packet_for_c4_consumption.v0"
LAYER = "REVIEW / ACCEPTED_PROPOSAL_PACKET"
MODE = "REVIEW_DECISION / ACCEPTANCE_PACKET / NO_CELL1_EXECUTION"
BUILD_MODE = "ACCEPTED_PROPOSAL_PACKET_ONLY"

SOURCE_C4_RERUN_RECEIPT_ID = "a17b6786"
SOURCE_C4_RERUN_RECEIPT_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_preflight_rerun_v0_receipts" / "a17b6786.json"
SOURCE_C4_RERUN_GATE_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_preflight_rerun_v0" / "c4_opening_gate_evaluation_v0_1.json"
SOURCE_C4_RERUN_GATE_STATUS_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_preflight_rerun_v0" / "cell1_gate_status_v0.json"
SOURCE_C4_ACCEPTED_PROPOSAL_SCHEMA_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_v0" / "cell1_accepted_proposal_input_schema_v0.json"

SOURCE_C1_PATCH_RECEIPT_ID = "fffa3dd5"
SOURCE_C1_PATCH_RECEIPT_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0_receipts" / "fffa3dd5.json"
SOURCE_C1_PATCH_SCHEMA_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0" / "proposal_packet_schema_v0_1.json"
SOURCE_C1_PATCH_DEMO_PROPOSALS_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0" / "c1_interface_patch_demo_proposals_v0.jsonl"

SOURCE_C3_RERUN_RECEIPT_ID = "d554701a"
SOURCE_C3_RERUN_RECEIPT_PATH = ROOT / "data" / "c3_micro_domain_shift_rerun_against_c1_interface_patch_v0_receipts" / "d554701a.json"
SOURCE_C3_RERUN_VERDICT_PATH = ROOT / "data" / "c3_micro_domain_shift_rerun_against_c1_interface_patch_v0" / "c3_interface_readiness_verdict_v0_1.json"

SOURCE_C2_RECEIPT_ID = "348dabde"
SOURCE_C2_RECEIPT_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts" / "348dabde.json"
SOURCE_C2_LANE_REGISTRY_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "taxonomy_lane_registry_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C4_RERUN_RECEIPT_PATH,
    SOURCE_C4_RERUN_GATE_PATH,
    SOURCE_C4_RERUN_GATE_STATUS_PATH,
    SOURCE_C4_ACCEPTED_PROPOSAL_SCHEMA_PATH,
    SOURCE_C1_PATCH_RECEIPT_PATH,
    SOURCE_C1_PATCH_SCHEMA_PATH,
    SOURCE_C1_PATCH_DEMO_PROPOSALS_PATH,
    SOURCE_C3_RERUN_RECEIPT_PATH,
    SOURCE_C3_RERUN_VERDICT_PATH,
    SOURCE_C2_RECEIPT_PATH,
    SOURCE_C2_LANE_REGISTRY_PATH,
]

OUT_DIR = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0"
RECEIPT_DIR = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0_receipts"

SOURCE_SURFACE_PATH = OUT_DIR / "accepted_proposal_source_surface_v0.json"
REVIEW_DECISION_RECORD_PATH = OUT_DIR / "review_decision_record_v0.json"
ACCEPTED_PROPOSAL_PACKET_PATH = OUT_DIR / "accepted_proposal_packet_v0.json"
ACCEPTED_PROPOSAL_VALIDATION_PATH = OUT_DIR / "accepted_proposal_validation_record_v0.json"
C4_CONSUMPTION_CONTRACT_PATH = OUT_DIR / "c4_consumption_contract_record_v0.json"
ROLLUP_PATH = OUT_DIR / "accepted_proposal_packet_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "accepted_proposal_packet_profile_v0.json"
REPORT_PATH = OUT_DIR / "accepted_proposal_packet_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "accepted_proposal_packet_transition_trace.json"

ACCEPTED_STATUS = "ACCEPTED_FOR_BUILD"
PROPOSAL_ID = "accepted_artifact_review_interface_probe_v0"
REVIEW_RECEIPT_ID = "review_" + hashlib.sha256(PROPOSAL_ID.encode()).hexdigest()[:8]

ZERO_COUNTER_KEYS = [
    "cell1_execution_opened_count",
    "cell1_execution_authorized_now_count",
    "builds_attempted",
    "builds_verified",
    "patch_applied_count",
    "probe_run_count",
    "verification_pass_emitted_count",
    "builder_command_emitted_count",
    "c4_consumption_run_count",
    "c5_opened_count",
    "taxonomy_registry_mutation_count",
    "runtime_patch_applied_count",
    "proposal_status_promoted_without_review_count",
    "proposed_only_consumed_as_accepted_count",
    "accepted_proposal_fabricated_without_review_count",
    "review_default_no_execution_violated_count",
    "source_mutation_count",
    "prior_receipt_mutation_count",
    "hidden_next_command_count",
]

HUMAN_DECISION = {
    "decision": "PROVIDE_OR_REVIEW_ONE_ACCEPTED_PROPOSAL_PACKET_FOR_C4_CONSUMPTION",
    "scope": "Create exactly one review-backed accepted proposal packet for later C4 consumption. Consume the open C4 preflight rerun gate, C1 proposal interface patch candidate, C3 rerun verdict, and C2 lane registry. Emit one review decision record, one accepted proposal packet, one validation record, one C4 consumption contract record, rollup, profile, report, and receipt. Do not run C4 consumption, do not open Cell 1 execution, do not build, patch, probe, verify, mutate taxonomy, open C5, or emit hidden next command.",
    "authorized": [
        "consume C4 preflight rerun gate",
        "consume C1 proposal interface candidate",
        "consume C3 rerun verdict",
        "consume C2 lane registry",
        "emit one review-backed accepted proposal packet",
        "emit accepted proposal validation record",
        "emit C4 consumption contract record",
        "emit receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "run C4 consumption",
        "open Cell 1 execution",
        "apply patch",
        "run probe",
        "emit verification PASS",
        "emit build receipt",
        "mutate taxonomy registry",
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

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def validate_source_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    c4_receipt = read_json(SOURCE_C4_RERUN_RECEIPT_PATH)
    c4_gate = read_json(SOURCE_C4_RERUN_GATE_PATH)
    c4_gate_status = read_json(SOURCE_C4_RERUN_GATE_STATUS_PATH)
    c4_schema = read_json(SOURCE_C4_ACCEPTED_PROPOSAL_SCHEMA_PATH)
    c1_receipt = read_json(SOURCE_C1_PATCH_RECEIPT_PATH)
    c1_schema = read_json(SOURCE_C1_PATCH_SCHEMA_PATH)
    c3_receipt = read_json(SOURCE_C3_RERUN_RECEIPT_PATH)
    c3_verdict = read_json(SOURCE_C3_RERUN_VERDICT_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)

    if c4_receipt.get("receipt_id") != SOURCE_C4_RERUN_RECEIPT_ID or c4_receipt.get("gate") != "PASS":
        failures.append("c4_preflight_rerun_basis_not_accepted")
    if c4_gate.get("c4_opening_gate_status") != "OPEN_FOR_NARROW_ACCEPTED_PROPOSAL_TEST":
        failures.append("c4_gate_not_open_for_narrow_test")
    if c4_gate.get("accepted_proposal_required_for_execution") is not True:
        failures.append("c4_gate_missing_accepted_proposal_requirement")
    if c4_gate.get("accepted_proposal_present") is not False:
        failures.append("c4_gate_claims_existing_accepted_proposal")
    if c4_gate.get("cell1_execution_opened") is not False:
        failures.append("c4_gate_claims_cell1_execution")
    if c4_gate_status.get("next_required_input") != "ONE_ACCEPTED_PROPOSAL_PACKET_WITH_REVIEW_RECEIPT":
        failures.append("c4_gate_status_wrong_next_input")
    if c4_gate_status.get("execution_status") != "NOT_OPENED":
        failures.append("c4_gate_status_execution_opened")
    if ACCEPTED_STATUS not in c4_schema.get("accepted_statuses", []):
        failures.append("accepted_status_not_allowed_by_c4_schema")
    if c1_receipt.get("receipt_id") != SOURCE_C1_PATCH_RECEIPT_ID or c1_receipt.get("gate") != "PASS":
        failures.append("c1_patch_basis_not_accepted")
    if c1_schema.get("schema_version") != "proposal_packet_schema_v0_1":
        failures.append("c1_patch_schema_wrong_version")
    if c1_schema.get("review_authority", {}).get("review_required") is not True:
        failures.append("c1_patch_schema_review_not_required")
    if c1_schema.get("review_authority", {}).get("cell1_may_accept") is not False:
        failures.append("c1_patch_schema_allows_cell1_acceptance")
    if c3_receipt.get("receipt_id") != SOURCE_C3_RERUN_RECEIPT_ID or c3_receipt.get("gate") != "PASS":
        failures.append("c3_rerun_basis_not_accepted")
    if c3_verdict.get("verdict") != "CELL1_READY_FOR_NARROW_ACCEPTED_PROPOSAL_TEST":
        failures.append("c3_verdict_not_ready")
    if c2_receipt.get("receipt_id") != SOURCE_C2_RECEIPT_ID or c2_receipt.get("gate") != "PASS":
        failures.append("c2_basis_not_accepted")
    if not read_jsonl(SOURCE_C1_PATCH_DEMO_PROPOSALS_PATH):
        failures.append("c1_patch_demo_proposals_missing")
    return failures

def source_surface() -> Dict[str, Any]:
    return {
        "schema_version": "accepted_proposal_source_surface_v0",
        "source_c4_preflight_rerun_receipt_id": SOURCE_C4_RERUN_RECEIPT_ID,
        "source_c4_preflight_rerun_receipt_ref": rel(SOURCE_C4_RERUN_RECEIPT_PATH),
        "source_c4_opening_gate_ref": rel(SOURCE_C4_RERUN_GATE_PATH),
        "source_c4_gate_status_ref": rel(SOURCE_C4_RERUN_GATE_STATUS_PATH),
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c1_patch_schema_ref": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "source_c3_rerun_receipt_id": SOURCE_C3_RERUN_RECEIPT_ID,
        "source_c3_rerun_verdict_ref": rel(SOURCE_C3_RERUN_VERDICT_PATH),
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "source_c2_lane_registry_ref": rel(SOURCE_C2_LANE_REGISTRY_PATH),
        "surface_status": "EXPLICIT_REVIEW_BACKED_ACCEPTANCE_SURFACE",
    }

def review_decision_record() -> Dict[str, Any]:
    return {
        "schema_version": "review_decision_record_v0",
        "review_receipt_id": REVIEW_RECEIPT_ID,
        "proposal_id": PROPOSAL_ID,
        "review_decision": ACCEPTED_STATUS,
        "gate": "PASS",
        "authorizes_exact_proposal_id": True,
        "accepted_status_output": ACCEPTED_STATUS,
        "review_basis": [
            rel(SOURCE_C4_RERUN_RECEIPT_PATH),
            rel(SOURCE_C4_RERUN_GATE_PATH),
            rel(SOURCE_C1_PATCH_SCHEMA_PATH),
            rel(SOURCE_C3_RERUN_VERDICT_PATH),
        ],
        "review_scope": {
            "may_c4_consume_later": True,
            "may_cell1_execute_now": False,
            "may_patch_now": False,
            "may_probe_now": False,
            "may_verify_now": False,
            "may_open_c5": False,
        },
        "must_not_infer": [
            "Cell 1 execution",
            "build occurred",
            "verification PASS",
            "C5 authorized",
            "future accepted proposals authorized",
        ],
    }

def accepted_proposal_packet() -> Dict[str, Any]:
    c1_schema = read_json(SOURCE_C1_PATCH_SCHEMA_PATH)
    return {
        "schema_version": "accepted_proposal_packet_v0",
        "proposal_id": PROPOSAL_ID,
        "proposal_type": "BUILDER_OBJECTIVE_PROPOSAL",
        "status": ACCEPTED_STATUS,
        "review_receipt_ref": rel(REVIEW_DECISION_RECORD_PATH),
        "review_receipt_id": REVIEW_RECEIPT_ID,
        "source_candidate_interface_schema_ref": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "bounded_objective": "Run one future C4/Cell1 receipt-native builder consumption test against this accepted artifact-review interface proposal, limited to schema/receipt validation and no unrelated scope.",
        "target_surface": "accepted_proposal_packet_for_c4_consumption_v0",
        "allowed_inputs": [
            rel(ACCEPTED_PROPOSAL_PACKET_PATH),
            rel(REVIEW_DECISION_RECORD_PATH),
            rel(SOURCE_C4_ACCEPTED_PROPOSAL_SCHEMA_PATH),
            rel(SOURCE_C1_PATCH_SCHEMA_PATH),
            rel(SOURCE_C2_LANE_REGISTRY_PATH),
        ],
        "forbidden_inputs": [
            "unbounded_payload",
            "ambient_workspace_inference",
            "latest_file_guessing",
            "runtime_patch_targets",
            "taxonomy_registry_mutation",
            "C5_artifacts",
        ],
        "expected_patch_shape": {
            "patch_kind": "NO_RUNTIME_PATCH_SCHEMA_CONSUMPTION_TEST",
            "files_expected_to_change": [],
            "files_forbidden_to_change": [
                "src/matrixlab/cli.py",
                "data/c2_cell0_label_taxonomy_lane_cleaning_v0/taxonomy_lane_registry_v0.json",
            ],
            "patch_application_expected": False,
        },
        "verification_requirement": {
            "expected_verification_receipt_shape": "cell1_verification_record_v0",
            "required_checks": [
                "accepted proposal status is accepted by review",
                "review receipt authorizes exact proposal id",
                "PROPOSED_ONLY is not consumed",
                "no Cell 1 execution unless C4 consumes packet in later unit",
                "no runtime patch for no-op schema-consumption test",
            ],
        },
        "stop_conditions": [
            "STOP_C4_ACCEPTED_PROPOSAL_UNDERTYPED",
            "STOP_C4_REVIEW_RECEIPT_MISSING",
            "STOP_BUILD_SCOPE_VIOLATION",
            "STOP_CELL1_NO_RUNTIME_PATCH_REQUIRED",
        ],
        "builder_interface": {
            **c1_schema["builder_interface"],
            "builder_consumption_allowed": True,
            "builder_allowed_inputs": [
                rel(ACCEPTED_PROPOSAL_PACKET_PATH),
                rel(REVIEW_DECISION_RECORD_PATH),
                rel(SOURCE_C4_ACCEPTED_PROPOSAL_SCHEMA_PATH),
                rel(SOURCE_C1_PATCH_SCHEMA_PATH),
            ],
            "builder_forbidden_inputs": [
                "unbounded_payload",
                "runtime_patch_targets",
                "taxonomy_registry_mutation",
                "C5_artifacts",
            ],
            "required_input_refs": [
                rel(ACCEPTED_PROPOSAL_PACKET_PATH),
                rel(REVIEW_DECISION_RECORD_PATH),
            ],
            "target_surface": "accepted_proposal_packet_for_c4_consumption_v0",
            "domain_kind": "artifact_review",
            "object_kind": "accepted_proposal_packet",
            "object_scope": "one review-backed accepted proposal packet for future C4 consumption",
            "out_of_scope_objects": [
                "general Cell 1 builder authority",
                "runtime patching",
                "C5 domain shift",
            ],
        },
        "verification_contract": {
            **c1_schema["verification_contract"],
            "expected_verification_receipt_shape": "cell1_verification_record_v0",
            "verification_requirement": "future C4 consumption must verify schema/receipt contract only",
            "required_negative_controls": [
                "proposed_only_packet_consumed_count == 0",
                "proposal_status_promoted_count == 0",
                "runtime_patch_applied_count == 0",
            ],
        },
        "failure_or_reject_handling": {
            **c1_schema["failure_or_reject_handling"],
            "rollback_or_reject_handling": "return_to_review_without_cell1_continuation",
            "park_condition": "missing_review_receipt_or_schema_gap",
            "repair_condition": "accepted_proposal_contract_missing_field",
            "stop_condition": "STOP_C4_ACCEPTED_PROPOSAL_UNDERTYPED",
        },
        "claim_scope": {
            **c1_schema["claim_scope"],
            "claim_kind": "local_builder_intake_claim",
            "claim_scope": "this packet is structurally acceptable for future C4 consumption",
            "claim_nonclaims": [
                "Cell 1 executed",
                "build occurred",
                "runtime patch applied",
                "C5 authorized",
            ],
            "verification_claim_boundary": "future verification checks only this proposal packet and review receipt contract",
        },
        "payload_boundary": {
            **c1_schema["payload_boundary"],
            "inspection_mode": "REF_ONLY",
            "allowed_payload_boundary": [
                "accepted proposal packet fields",
                "review decision record fields",
                "declared schema refs",
            ],
            "forbidden_payload_boundary": [
                "unbounded payload",
                "arbitrary repository scan",
                "runtime build targets",
            ],
        },
        "evidence_limitations": {
            **c1_schema["evidence_limitations"],
            "evidence_status": "SUFFICIENT_FOR_C4_CONSUMPTION_TEST",
            "evidence_refs": [
                SOURCE_C4_RERUN_RECEIPT_ID,
                SOURCE_C1_PATCH_RECEIPT_ID,
                SOURCE_C3_RERUN_RECEIPT_ID,
                SOURCE_C2_RECEIPT_ID,
            ],
            "evidence_limitations": [
                "does not prove Cell 1 execution correctness",
                "does not prove runtime patch correctness",
                "does not authorize C5",
            ],
            "must_not_infer_from_evidence": [
                "global correctness",
                "Cell 1 already executed",
                "build verified",
            ],
        },
        "review_authority": {
            **c1_schema["review_authority"],
            "review_required": True,
            "default_without_review": "NO_EXECUTION",
            "cell1_may_accept": False,
        },
        "must_not_infer": [
            "Cell 1 executed",
            "build occurred",
            "verification passed",
            "runtime patch is authorized",
            "C5 is authorized",
        ],
    }

def validation_record(packet: Dict[str, Any], review: Dict[str, Any]) -> Dict[str, Any]:
    c4_schema = read_json(SOURCE_C4_ACCEPTED_PROPOSAL_SCHEMA_PATH)
    failures: List[str] = []
    if packet.get("status") not in c4_schema.get("accepted_statuses", []):
        failures.append("status_not_c4_accepted")
    if packet.get("review_receipt_id") != review.get("review_receipt_id"):
        failures.append("review_receipt_id_mismatch")
    if review.get("authorizes_exact_proposal_id") is not True:
        failures.append("review_does_not_authorize_exact_proposal_id")
    if review.get("proposal_id") != packet.get("proposal_id"):
        failures.append("review_proposal_id_mismatch")
    for field in [
        "bounded_objective",
        "target_surface",
        "allowed_inputs",
        "forbidden_inputs",
        "expected_patch_shape",
        "verification_requirement",
        "stop_conditions",
        "builder_interface",
        "verification_contract",
        "failure_or_reject_handling",
        "claim_scope",
        "payload_boundary",
        "evidence_limitations",
        "review_authority",
    ]:
        if field not in packet:
            failures.append(f"packet_missing_field:{field}")
    if packet.get("builder_interface", {}).get("builder_consumption_allowed") is not True:
        failures.append("builder_consumption_not_marked_for_future_c4")
    if packet.get("review_authority", {}).get("cell1_may_accept") is not False:
        failures.append("packet_allows_cell1_acceptance")
    if packet.get("expected_patch_shape", {}).get("patch_application_expected") is not False:
        failures.append("packet_expects_runtime_patch")
    return {
        "schema_version": "accepted_proposal_validation_record_v0",
        "validation_id": "accepted_validation_" + sha8({"proposal": packet.get("proposal_id"), "review": review.get("review_receipt_id")}),
        "proposal_id": packet.get("proposal_id"),
        "review_receipt_id": review.get("review_receipt_id"),
        "c4_accepted_status_allowed": packet.get("status") in c4_schema.get("accepted_statuses", []),
        "required_fields_present": len([f for f in failures if f.startswith("packet_missing_field:")]) == 0,
        "review_receipt_authorizes_exact_proposal": review.get("authorizes_exact_proposal_id") is True and review.get("proposal_id") == packet.get("proposal_id"),
        "cell1_execution_opened": False,
        "future_c4_consumption_candidate": True,
        "validation_status": "PASS" if not failures else "FAIL",
        "failures": failures,
    }

def c4_consumption_contract(packet: Dict[str, Any], review: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c4_consumption_contract_record_v0",
        "contract_id": "c4_contract_" + sha8({"proposal": packet["proposal_id"], "review": review["review_receipt_id"]}),
        "accepted_proposal_packet_ref": rel(ACCEPTED_PROPOSAL_PACKET_PATH),
        "review_decision_record_ref": rel(REVIEW_DECISION_RECORD_PATH),
        "future_c4_unit": "CONSUME_ONE_ACCEPTED_PROPOSAL_PACKET_WITH_C4_V0",
        "future_cell1_execution_allowed_by_this_unit": False,
        "future_c4_may_consume_if": [
            "packet.status is accepted",
            "review receipt exists and authorizes exact proposal id",
            "C4 opening gate remains open",
            "packet validates against accepted proposal input schema",
        ],
        "future_c4_must_not_infer": [
            "Cell 1 may accept proposal",
            "runtime patch is automatically required",
            "C5 is authorized",
            "review of this packet accepts future packets",
        ],
    }

def rollup(packet: Dict[str, Any], review: Dict[str, Any], validation: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "accepted_proposal_packet_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_c4_preflight_rerun_receipt_id": SOURCE_C4_RERUN_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c3_rerun_receipt_id": SOURCE_C3_RERUN_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "accepted_proposal_packets_emitted": 1,
        "review_decision_records_emitted": 1,
        "proposal_id": packet["proposal_id"],
        "review_receipt_id": review["review_receipt_id"],
        "proposal_status": packet["status"],
        "validation_status": validation["validation_status"],
        "future_c4_consumption_candidate_count": 1 if validation["future_c4_consumption_candidate"] else 0,
        "cell1_execution_opened_count": 0,
        "cell1_execution_authorized_now_count": 0,
        "builds_attempted": 0,
        "builds_verified": 0,
        "patch_applied_count": 0,
        "probe_run_count": 0,
        "verification_pass_emitted_count": 0,
        "builder_command_emitted_count": 0,
        "c4_consumption_run_count": 0,
        "c5_opened_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "runtime_patch_applied_count": 0,
        "proposal_status_promoted_without_review_count": 0,
        "proposed_only_consumed_as_accepted_count": 0,
        "accepted_proposal_fabricated_without_review_count": 0,
        "review_default_no_execution_violated_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next": "CONSUME_ONE_ACCEPTED_PROPOSAL_PACKET_WITH_C4_V0",
    }

def profile(rollup_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "accepted_proposal_packet_profile_v0",
        "profile_id": "accepted_proposal_" + sha8({"proposal": rollup_obj["proposal_id"], "review": rollup_obj["review_receipt_id"]}),
        "status": "ACCEPTED_PROPOSAL_PACKET_READY_FOR_C4_CONSUMPTION",
        "accepted_proposal_packet_ref": rel(ACCEPTED_PROPOSAL_PACKET_PATH),
        "review_decision_record_ref": rel(REVIEW_DECISION_RECORD_PATH),
        "validation_record_ref": rel(ACCEPTED_PROPOSAL_VALIDATION_PATH),
        "cell1_execution_opened": False,
        "c4_consumption_run": False,
        "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "must_not_infer": [
            "Cell 1 executed",
            "build occurred",
            "verification passed",
            "runtime patch applied",
            "C5 authorized",
        ],
        "next_command_goal": None,
    }

def report(rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "accepted_proposal_packet_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_c4_preflight_rerun_consumed_count": 1,
        "source_c1_patch_schema_consumed_count": 1,
        "source_c3_rerun_verdict_consumed_count": 1,
        "source_c2_lane_registry_consumed_count": 1,
        "review_decision_record_emitted_count": 1,
        "accepted_proposal_packet_emitted_count": 1,
        "accepted_proposal_validation_emitted_count": 1,
        "c4_consumption_contract_emitted_count": 1,
        "profile_status": profile_obj["status"],
        "accepted_proposal_packets_emitted": rollup_obj["accepted_proposal_packets_emitted"],
        "future_c4_consumption_candidate_count": rollup_obj["future_c4_consumption_candidate_count"],
        "cell1_execution_opened_count": 0,
        "cell1_execution_authorized_now_count": 0,
        "builds_attempted": 0,
        "builds_verified": 0,
        "patch_applied_count": 0,
        "probe_run_count": 0,
        "verification_pass_emitted_count": 0,
        "builder_command_emitted_count": 0,
        "c4_consumption_run_count": 0,
        "c5_opened_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "runtime_patch_applied_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": rollup_obj["recommended_next"],
    }

def transition_trace() -> Dict[str, Any]:
    return {
        "schema_version": "accepted_proposal_packet_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c4_preflight_rerun_gate",
                "question": "is C4 ready for one accepted proposal packet",
                "answer": "OPEN_FOR_NARROW_ACCEPTED_PROPOSAL_TEST",
                "taken": "emit_review_decision",
            },
            {
                "step": "emit_review_decision",
                "question": "does review accept exactly one proposal id",
                "answer": REVIEW_RECEIPT_ID,
                "taken": "emit_accepted_proposal_packet",
            },
            {
                "step": "emit_accepted_proposal_packet",
                "question": "was Cell 1 execution avoided",
                "answer": True,
                "taken": "stop_for_future_c4_consumption",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_ACCEPTED_PROPOSAL_PACKET_READY_FOR_C4_CONSUMPTION",
            "next_command_goal": None,
        },
    }

def validate_outputs(packet: Dict[str, Any], review: Dict[str, Any], validation: Dict[str, Any], contract: Dict[str, Any], rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any], report_obj: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if packet.get("status") != ACCEPTED_STATUS:
        failures.append(f"packet_status_not_accepted:{packet.get('status')}")
    if packet.get("review_receipt_id") != review.get("review_receipt_id"):
        failures.append("packet_review_ref_mismatch")
    if review.get("review_decision") != ACCEPTED_STATUS:
        failures.append("review_decision_not_accepted")
    if review.get("authorizes_exact_proposal_id") is not True:
        failures.append("review_not_exact_proposal")
    if review.get("proposal_id") != packet.get("proposal_id"):
        failures.append("review_proposal_mismatch")
    if validation.get("validation_status") != "PASS":
        failures.append("accepted_proposal_validation_failed")
    if validation.get("future_c4_consumption_candidate") is not True:
        failures.append("not_future_c4_consumption_candidate")
    if contract.get("future_cell1_execution_allowed_by_this_unit") is not False:
        failures.append("contract_allows_cell1_execution_now")
    if packet.get("review_authority", {}).get("cell1_may_accept") is not False:
        failures.append("packet_allows_cell1_acceptance")
    if packet.get("expected_patch_shape", {}).get("patch_application_expected") is not False:
        failures.append("packet_expects_runtime_patch")
    for key in ZERO_COUNTER_KEYS:
        if rollup_obj.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup_obj.get(key)}")
    if rollup_obj.get("accepted_proposal_packets_emitted") != 1:
        failures.append("accepted_packet_count_not_one")
    if rollup_obj.get("review_decision_records_emitted") != 1:
        failures.append("review_record_count_not_one")
    if profile_obj.get("cell1_execution_opened") is not False:
        failures.append("profile_claims_cell1_execution")
    if profile_obj.get("c4_consumption_run") is not False:
        failures.append("profile_claims_c4_consumption_run")
    if profile_obj.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")
    for key in [
        "cell1_execution_opened_count",
        "cell1_execution_authorized_now_count",
        "builds_attempted",
        "builds_verified",
        "patch_applied_count",
        "probe_run_count",
        "verification_pass_emitted_count",
        "builder_command_emitted_count",
        "c4_consumption_run_count",
        "c5_opened_count",
        "taxonomy_registry_mutation_count",
        "runtime_patch_applied_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "hidden_next_command_count",
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
    if terminal.get("stop_code") != "STOP_ACCEPTED_PROPOSAL_PACKET_READY_FOR_C4_CONSUMPTION":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    packet = read_json(ACCEPTED_PROPOSAL_PACKET_PATH)
    review = read_json(REVIEW_DECISION_RECORD_PATH)
    validation = read_json(ACCEPTED_PROPOSAL_VALIDATION_PATH)
    contract = read_json(C4_CONSUMPTION_CONTRACT_PATH)
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

    bad_packet = copy.deepcopy(packet)
    bad_packet["status"] = "PROPOSED_ONLY"
    add("proposal_not_accepted_fail", validate_outputs(bad_packet, review, validation, contract, rollup_obj, profile_obj, report_obj), "packet_status_not_accepted")

    bad_review = copy.deepcopy(review)
    bad_review["review_decision"] = "PARKED"
    add("review_not_accepted_fail", validate_outputs(packet, bad_review, validation, contract, rollup_obj, profile_obj, report_obj), "review_decision_not_accepted")

    bad_review = copy.deepcopy(review)
    bad_review["proposal_id"] = "wrong_proposal"
    add("review_wrong_proposal_fail", validate_outputs(packet, bad_review, validation, contract, rollup_obj, profile_obj, report_obj), "review_proposal_mismatch")

    bad_validation = copy.deepcopy(validation)
    bad_validation["validation_status"] = "FAIL"
    add("accepted_proposal_validation_fail", validate_outputs(packet, review, bad_validation, contract, rollup_obj, profile_obj, report_obj), "accepted_proposal_validation_failed")

    bad_contract = copy.deepcopy(contract)
    bad_contract["future_cell1_execution_allowed_by_this_unit"] = True
    add("contract_allows_cell1_execution_fail", validate_outputs(packet, review, validation, bad_contract, rollup_obj, profile_obj, report_obj), "contract_allows_cell1_execution_now")

    bad_packet = copy.deepcopy(packet)
    bad_packet["review_authority"]["cell1_may_accept"] = True
    add("packet_allows_cell1_acceptance_fail", validate_outputs(bad_packet, review, validation, contract, rollup_obj, profile_obj, report_obj), "packet_allows_cell1_acceptance")

    bad_packet = copy.deepcopy(packet)
    bad_packet["expected_patch_shape"]["patch_application_expected"] = True
    add("packet_expects_runtime_patch_fail", validate_outputs(bad_packet, review, validation, contract, rollup_obj, profile_obj, report_obj), "packet_expects_runtime_patch")

    for case, counter in [
        ("cell1_execution_opened_fail", "cell1_execution_opened_count"),
        ("cell1_execution_authorized_now_fail", "cell1_execution_authorized_now_count"),
        ("build_attempted_fail", "builds_attempted"),
        ("build_verified_fail", "builds_verified"),
        ("patch_applied_fail", "patch_applied_count"),
        ("probe_run_fail", "probe_run_count"),
        ("verification_pass_emitted_fail", "verification_pass_emitted_count"),
        ("builder_command_emitted_fail", "builder_command_emitted_count"),
        ("c4_consumption_run_fail", "c4_consumption_run_count"),
        ("c5_opened_fail", "c5_opened_count"),
        ("taxonomy_registry_mutated_fail", "taxonomy_registry_mutation_count"),
        ("runtime_patch_applied_fail", "runtime_patch_applied_count"),
        ("proposal_status_promoted_without_review_fail", "proposal_status_promoted_without_review_count"),
        ("proposed_only_consumed_as_accepted_fail", "proposed_only_consumed_as_accepted_count"),
        ("accepted_proposal_fabricated_without_review_fail", "accepted_proposal_fabricated_without_review_count"),
        ("review_default_no_execution_violated_fail", "review_default_no_execution_violated_count"),
        ("source_mutation_fail", "source_mutation_count"),
        ("prior_receipt_mutation_fail", "prior_receipt_mutation_count"),
        ("hidden_next_command_fail", "hidden_next_command_count"),
    ]:
        bad_rollup = copy.deepcopy(rollup_obj)
        bad_report = copy.deepcopy(report_obj)
        bad_rollup[counter] = 1
        if counter in bad_report:
            bad_report[counter] = 1
        add(case, validate_outputs(packet, review, validation, contract, bad_rollup, profile_obj, bad_report), counter)

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_ACCEPTED_PROPOSAL_DEPENDENCY_MISSING", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "accepted_proposal_packet_receipt_v0",
            "receipt_type": "ACCEPTED_PROPOSAL_PACKET_RECEIPT",
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
        print(f"accepted_proposal_receipt_id={receipt_id}")
        print(f"accepted_proposal_receipt_path=data/accepted_proposal_packet_for_c4_consumption_v0_receipts/{receipt_id}.json")
        return 1

    review = review_decision_record()
    packet = accepted_proposal_packet()
    validation = validation_record(packet, review)
    contract = c4_consumption_contract(packet, review)
    rollup_obj = rollup(packet, review, validation)
    profile_obj = profile(rollup_obj)
    report_obj = report(rollup_obj, profile_obj)
    trace = transition_trace()

    write_json(SOURCE_SURFACE_PATH, source_surface())
    write_json(REVIEW_DECISION_RECORD_PATH, review)
    write_json(ACCEPTED_PROPOSAL_PACKET_PATH, packet)
    write_json(ACCEPTED_PROPOSAL_VALIDATION_PATH, validation)
    write_json(C4_CONSUMPTION_CONTRACT_PATH, contract)
    write_json(ROLLUP_PATH, rollup_obj)
    write_json(PROFILE_PATH, profile_obj)
    write_json(REPORT_PATH, report_obj)
    write_json(TRANSITION_TRACE_PATH, trace)

    failures.extend(validate_outputs(packet, review, validation, contract, rollup_obj, profile_obj, report_obj))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup_obj["source_mutation_count"] = 1
        report_obj["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup_obj)
        write_json(REPORT_PATH, report_obj)

    acceptance_gate_results = {
        "ACCEPTED_PROPOSAL_0_C4_PREFLIGHT_RERUN_GATE_CONSUMED": SOURCE_C4_RERUN_GATE_PATH.exists(),
        "ACCEPTED_PROPOSAL_1_C4_GATE_OPEN_FOR_ACCEPTED_PROPOSAL": read_json(SOURCE_C4_RERUN_GATE_PATH).get("c4_opening_gate_status") == "OPEN_FOR_NARROW_ACCEPTED_PROPOSAL_TEST",
        "ACCEPTED_PROPOSAL_2_C1_PATCH_SCHEMA_CONSUMED": SOURCE_C1_PATCH_SCHEMA_PATH.exists(),
        "ACCEPTED_PROPOSAL_3_C3_RERUN_VERDICT_CONSUMED": SOURCE_C3_RERUN_VERDICT_PATH.exists(),
        "ACCEPTED_PROPOSAL_4_C2_LANE_REGISTRY_CONSUMED": SOURCE_C2_LANE_REGISTRY_PATH.exists(),
        "ACCEPTED_PROPOSAL_5_REVIEW_DECISION_RECORD_EMITTED": REVIEW_DECISION_RECORD_PATH.exists(),
        "ACCEPTED_PROPOSAL_6_REVIEW_DECISION_ACCEPTS_EXACT_PROPOSAL": review["review_decision"] == ACCEPTED_STATUS and review["authorizes_exact_proposal_id"] is True,
        "ACCEPTED_PROPOSAL_7_ACCEPTED_PACKET_EMITTED": ACCEPTED_PROPOSAL_PACKET_PATH.exists(),
        "ACCEPTED_PROPOSAL_8_PACKET_STATUS_ACCEPTED_FOR_BUILD": packet["status"] == ACCEPTED_STATUS,
        "ACCEPTED_PROPOSAL_9_PACKET_VALIDATES_FOR_C4_CONSUMPTION": validation["validation_status"] == "PASS",
        "ACCEPTED_PROPOSAL_10_C4_CONSUMPTION_CONTRACT_EMITTED": C4_CONSUMPTION_CONTRACT_PATH.exists(),
        "ACCEPTED_PROPOSAL_11_NO_CELL1_EXECUTION_OPENED": rollup_obj["cell1_execution_opened_count"] == 0,
        "ACCEPTED_PROPOSAL_12_NO_BUILD_PATCH_PROBE_VERIFY": rollup_obj["builds_attempted"] == 0 and rollup_obj["patch_applied_count"] == 0 and rollup_obj["probe_run_count"] == 0 and rollup_obj["verification_pass_emitted_count"] == 0,
        "ACCEPTED_PROPOSAL_13_NO_C4_CONSUMPTION_RUN": rollup_obj["c4_consumption_run_count"] == 0,
        "ACCEPTED_PROPOSAL_14_NO_C5_OPENED": rollup_obj["c5_opened_count"] == 0,
        "ACCEPTED_PROPOSAL_15_NO_TAXONOMY_OR_RUNTIME_MUTATION": rollup_obj["taxonomy_registry_mutation_count"] == 0 and rollup_obj["runtime_patch_applied_count"] == 0,
        "ACCEPTED_PROPOSAL_16_NO_HIDDEN_NEXT_COMMAND": rollup_obj["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
        "ACCEPTED_PROPOSAL_17_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    for gate_name, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate_name}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "proposal_id": PROPOSAL_ID,
        "review_receipt_id": REVIEW_RECEIPT_ID,
        "source_c4": SOURCE_C4_RERUN_RECEIPT_ID,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "review_decision_record": rel(REVIEW_DECISION_RECORD_PATH),
        "accepted_proposal_packet": rel(ACCEPTED_PROPOSAL_PACKET_PATH),
        "accepted_proposal_validation_record": rel(ACCEPTED_PROPOSAL_VALIDATION_PATH),
        "c4_consumption_contract_record": rel(C4_CONSUMPTION_CONTRACT_PATH),
        "rollup": rel(ROLLUP_PATH),
        "profile": rel(PROFILE_PATH),
        "report": rel(REPORT_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_c4_preflight_rerun_receipt": rel(SOURCE_C4_RERUN_RECEIPT_PATH),
        "source_c4_opening_gate": rel(SOURCE_C4_RERUN_GATE_PATH),
        "source_c1_patch_schema": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "source_c3_rerun_verdict": rel(SOURCE_C3_RERUN_VERDICT_PATH),
        "source_c2_lane_registry": rel(SOURCE_C2_LANE_REGISTRY_PATH),
    }

    guards = {
        "build_mode_accepted_proposal_packet_only": BUILD_MODE == "ACCEPTED_PROPOSAL_PACKET_ONLY",
        "review_decision_accepts_exact_proposal": True,
        "accepted_packet_emitted": True,
        "future_c4_consumption_candidate": True,
        "cell1_execution_opened": False,
        "c4_consumption_run": False,
        "build_attempted": False,
        "patch_applied": False,
        "probe_run": False,
        "verification_pass_emitted": False,
        "c5_opened": False,
        "taxonomy_registry_mutated": False,
        "runtime_patch_applied": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
    }

    receipt = {
        "schema_version": "accepted_proposal_packet_receipt_v0",
        "receipt_type": "ACCEPTED_PROPOSAL_PACKET_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "one review-backed accepted proposal packet for future C4 consumption",
        "source_c4_preflight_rerun_receipt_id": SOURCE_C4_RERUN_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c3_rerun_receipt_id": SOURCE_C3_RERUN_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "accepted_proposal_summary": {
            "profile_status": profile_obj["status"],
            "proposal_id": packet["proposal_id"],
            "proposal_status": packet["status"],
            "review_receipt_id": review["review_receipt_id"],
            "validation_status": validation["validation_status"],
            "future_c4_consumption_candidate_count": rollup_obj["future_c4_consumption_candidate_count"],
            "cell1_execution_opened": False,
            "c4_consumption_run": False,
            "builds_attempted": 0,
            "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
            "recommended_next": rollup_obj["recommended_next"],
        },
        "aggregate_metrics": {
            **{k: v for k, v in report_obj.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
            "rollup": rollup_obj,
            "source_mutation_count": 1 if source_mutation_detected else report_obj["source_mutation_count"],
        },
        "acceptance_gate_results": acceptance_gate_results,
        "accepted_proposal_guards": guards,
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
    if len(negative_controls) != 26 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
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
    print(f"accepted_proposal_receipt_id={receipt_id}")
    print(f"accepted_proposal_receipt_path=data/accepted_proposal_packet_for_c4_consumption_v0_receipts/{receipt_id}.json")
    print(f"accepted_proposal_packet_path=data/accepted_proposal_packet_for_c4_consumption_v0/accepted_proposal_packet_v0.json")
    print(f"review_decision_record_path=data/accepted_proposal_packet_for_c4_consumption_v0/review_decision_record_v0.json")
    print(f"accepted_proposal_rollup_path=data/accepted_proposal_packet_for_c4_consumption_v0/accepted_proposal_packet_rollup_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
