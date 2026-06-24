#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RERUN_C4_CELL1_RECEIPT_NATIVE_BUILDER_PREFLIGHT_V0"
TARGET_UNIT_ID = "c4.cell1.receipt_native_builder.preflight_rerun.v0"
LAYER = "CELL_1 / RECEIPT_NATIVE_BUILDER_PREFLIGHT"
MODE = "PREFLIGHT / GATE / RERUN"
BUILD_MODE = "PREFLIGHT_GATE_RERUN_ONLY"

SOURCE_C3_RERUN_RECEIPT_ID = "d554701a"
SOURCE_C3_RERUN_RECEIPT_PATH = ROOT / "data" / "c3_micro_domain_shift_rerun_against_c1_interface_patch_v0_receipts" / "d554701a.json"
SOURCE_C3_RERUN_PROFILE_PATH = ROOT / "data" / "c3_micro_domain_shift_rerun_against_c1_interface_patch_v0" / "c3_rerun_profile_v0.json"
SOURCE_C3_RERUN_ROLLUP_PATH = ROOT / "data" / "c3_micro_domain_shift_rerun_against_c1_interface_patch_v0" / "c3_rerun_rollup_v0.json"
SOURCE_C3_RERUN_VERDICT_PATH = ROOT / "data" / "c3_micro_domain_shift_rerun_against_c1_interface_patch_v0" / "c3_interface_readiness_verdict_v0_1.json"

SOURCE_C4_PREFLIGHT_RECEIPT_ID = "75764a86"
SOURCE_C4_PREFLIGHT_RECEIPT_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_v0_receipts" / "75764a86.json"
SOURCE_C4_AUTHORITY_PROFILE_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_v0" / "cell1_builder_authority_profile_v0.json"
SOURCE_C4_ACCEPTED_PROPOSAL_SCHEMA_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_v0" / "cell1_accepted_proposal_input_schema_v0.json"
SOURCE_C4_LOOP_TRACE_SCHEMA_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_v0" / "cell1_builder_loop_trace_schema_v0.json"

SOURCE_C1_PATCH_RECEIPT_ID = "fffa3dd5"
SOURCE_C1_PATCH_RECEIPT_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0_receipts" / "fffa3dd5.json"
SOURCE_C1_PATCH_SCHEMA_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0" / "proposal_packet_schema_v0_1.json"

SOURCE_C2_RECEIPT_ID = "348dabde"
SOURCE_C2_RECEIPT_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts" / "348dabde.json"
SOURCE_C2_LANE_REGISTRY_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "taxonomy_lane_registry_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C3_RERUN_RECEIPT_PATH,
    SOURCE_C3_RERUN_PROFILE_PATH,
    SOURCE_C3_RERUN_ROLLUP_PATH,
    SOURCE_C3_RERUN_VERDICT_PATH,
    SOURCE_C4_PREFLIGHT_RECEIPT_PATH,
    SOURCE_C4_AUTHORITY_PROFILE_PATH,
    SOURCE_C4_ACCEPTED_PROPOSAL_SCHEMA_PATH,
    SOURCE_C4_LOOP_TRACE_SCHEMA_PATH,
    SOURCE_C1_PATCH_RECEIPT_PATH,
    SOURCE_C1_PATCH_SCHEMA_PATH,
    SOURCE_C2_RECEIPT_PATH,
    SOURCE_C2_LANE_REGISTRY_PATH,
]

OUT_DIR = ROOT / "data" / "c4_cell1_receipt_native_builder_preflight_rerun_v0"
RECEIPT_DIR = ROOT / "data" / "c4_cell1_receipt_native_builder_preflight_rerun_v0_receipts"

SOURCE_SURFACE_PATH = OUT_DIR / "c4_preflight_rerun_source_surface_v0.json"
OPENING_GATE_EVALUATION_PATH = OUT_DIR / "c4_opening_gate_evaluation_v0_1.json"
ACCEPTED_PROPOSAL_READINESS_RECORD_PATH = OUT_DIR / "accepted_proposal_readiness_record_v0.json"
CELL1_GATE_STATUS_PATH = OUT_DIR / "cell1_gate_status_v0.json"
ROLLUP_PATH = OUT_DIR / "c4_preflight_rerun_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c4_preflight_rerun_profile_v0.json"
REPORT_PATH = OUT_DIR / "c4_preflight_rerun_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "c4_preflight_rerun_transition_trace.json"

ALLOWED_C3_VERDICT = "CELL1_READY_FOR_NARROW_ACCEPTED_PROPOSAL_TEST"

ZERO_COUNTER_KEYS = [
    "accepted_proposals_consumed",
    "proposed_only_packet_consumed_count",
    "accepted_proposal_fabricated_count",
    "proposal_accepted_by_cell1_count",
    "proposal_status_promoted_count",
    "builds_attempted",
    "builds_verified",
    "cell1_execution_opened_count",
    "patch_applied_count",
    "probe_run_count",
    "verification_pass_emitted_count",
    "builder_command_emitted_count",
    "hidden_next_command_count",
    "c5_opened_count",
    "taxonomy_registry_mutation_count",
    "runtime_patch_applied_count",
    "source_mutation_count",
    "prior_receipt_mutation_count",
    "ready_verdict_counted_as_cell1_execution_count",
    "gate_open_counted_as_build_count",
    "accepted_proposal_required_but_missing_count",
]

HUMAN_DECISION = {
    "decision": "RERUN_C4_CELL1_RECEIPT_NATIVE_BUILDER_PREFLIGHT",
    "scope": "Rerun C4 preflight after C3 rerun updated the interface readiness verdict to CELL1_READY_FOR_NARROW_ACCEPTED_PROPOSAL_TEST. Consume the updated C3 rerun verdict, prior C4 preflight schema surface, C1 proposal interface patch candidate, and C2 lane registry. Emit a new C4 opening gate evaluation showing the gate is open for one narrow accepted proposal packet. Do not consume or fabricate an accepted proposal, do not open Cell 1 execution, do not apply patches, do not run probes, do not emit verification PASS, and stop with no next command goal.",
    "authorized": [
        "consume updated C3 rerun verdict",
        "consume prior C4 preflight schema surface",
        "consume C1 interface patch candidate",
        "consume C2 lane registry",
        "evaluate C4 opening gate",
        "emit Cell 1 gate status ready for one narrow accepted proposal packet",
        "emit C4 preflight rerun rollup/profile/report/receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "consume accepted proposal as build input",
        "fabricate accepted proposal",
        "consume PROPOSED_ONLY packet",
        "accept proposal",
        "open Cell 1 execution",
        "apply patch",
        "run builder probe",
        "emit verification PASS",
        "emit build receipt",
        "mutate taxonomy registry",
        "run C5",
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

    c3_receipt = read_json(SOURCE_C3_RERUN_RECEIPT_PATH)
    c3_profile = read_json(SOURCE_C3_RERUN_PROFILE_PATH)
    c3_rollup = read_json(SOURCE_C3_RERUN_ROLLUP_PATH)
    c3_verdict = read_json(SOURCE_C3_RERUN_VERDICT_PATH)
    c4_receipt = read_json(SOURCE_C4_PREFLIGHT_RECEIPT_PATH)
    c4_authority = read_json(SOURCE_C4_AUTHORITY_PROFILE_PATH)
    c4_schema = read_json(SOURCE_C4_ACCEPTED_PROPOSAL_SCHEMA_PATH)
    c1_patch_receipt = read_json(SOURCE_C1_PATCH_RECEIPT_PATH)
    c1_schema = read_json(SOURCE_C1_PATCH_SCHEMA_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)

    if c3_receipt.get("receipt_id") != SOURCE_C3_RERUN_RECEIPT_ID or c3_receipt.get("gate") != "PASS":
        failures.append("c3_rerun_basis_not_accepted")
    if c3_profile.get("status") != "C3_RERUN_INTERFACE_READY_FOR_C4_PREFLIGHT":
        failures.append("c3_rerun_profile_not_ready")
    if c3_rollup.get("updated_interface_readiness_verdict") != ALLOWED_C3_VERDICT:
        failures.append(f"c3_rerun_rollup_not_ready:{c3_rollup.get('updated_interface_readiness_verdict')}")
    if c3_verdict.get("verdict") != ALLOWED_C3_VERDICT:
        failures.append(f"c3_rerun_verdict_not_ready:{c3_verdict.get('verdict')}")
    if c3_verdict.get("cell1_execution_opened") is not False:
        failures.append("c3_rerun_verdict_claims_cell1_execution")
    if c3_verdict.get("c4_rerun_executed") is not False:
        failures.append("c3_rerun_verdict_claims_c4_rerun")
    if c3_verdict.get("cell1_consumption_authorized_now") is not False:
        failures.append("c3_rerun_verdict_authorizes_cell1_consumption_now")
    if c4_receipt.get("receipt_id") != SOURCE_C4_PREFLIGHT_RECEIPT_ID or c4_receipt.get("gate") != "PASS":
        failures.append("prior_c4_preflight_basis_not_accepted")
    if c4_authority.get("cell_id") != "CELL_1" or c4_authority.get("default_on_ambiguity") != "STOP":
        failures.append("c4_authority_profile_invalid")
    if "ACCEPTED_FOR_BUILD" not in c4_schema.get("accepted_statuses", []):
        failures.append("c4_accepted_proposal_schema_missing_accepted_status")
    if c1_patch_receipt.get("receipt_id") != SOURCE_C1_PATCH_RECEIPT_ID or c1_patch_receipt.get("gate") != "PASS":
        failures.append("c1_patch_basis_not_accepted")
    if c1_schema.get("schema_version") != "proposal_packet_schema_v0_1":
        failures.append("c1_patch_schema_wrong_version")
    if c1_schema.get("canonical_c1_schema_replaced") is not False:
        failures.append("c1_patch_schema_claims_canonical_replacement")
    if c1_schema.get("review_authority", {}).get("cell1_may_accept") is not False:
        failures.append("c1_patch_schema_allows_cell1_acceptance")
    if c2_receipt.get("receipt_id") != SOURCE_C2_RECEIPT_ID or c2_receipt.get("gate") != "PASS":
        failures.append("c2_basis_not_accepted")
    return failures

def source_surface() -> Dict[str, Any]:
    return {
        "schema_version": "c4_preflight_rerun_source_surface_v0",
        "source_c3_rerun_receipt_id": SOURCE_C3_RERUN_RECEIPT_ID,
        "source_c3_rerun_receipt_ref": rel(SOURCE_C3_RERUN_RECEIPT_PATH),
        "source_c3_rerun_verdict_ref": rel(SOURCE_C3_RERUN_VERDICT_PATH),
        "source_c4_preflight_receipt_id": SOURCE_C4_PREFLIGHT_RECEIPT_ID,
        "source_c4_preflight_receipt_ref": rel(SOURCE_C4_PREFLIGHT_RECEIPT_PATH),
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c1_patch_schema_ref": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "source_c2_lane_registry_ref": rel(SOURCE_C2_LANE_REGISTRY_PATH),
        "surface_status": "EXPLICIT_C4_PREFLIGHT_RERUN_SURFACE",
    }

def opening_gate_evaluation() -> Dict[str, Any]:
    verdict = read_json(SOURCE_C3_RERUN_VERDICT_PATH)
    observed = verdict.get("verdict")
    gate_open = observed == ALLOWED_C3_VERDICT
    return {
        "schema_version": "c4_opening_gate_evaluation_v0_1",
        "source_c3_rerun_receipt_id": SOURCE_C3_RERUN_RECEIPT_ID,
        "source_c3_rerun_verdict_ref": rel(SOURCE_C3_RERUN_VERDICT_PATH),
        "allowed_verdict": ALLOWED_C3_VERDICT,
        "observed_verdict": observed,
        "prior_c4_preflight_receipt_id": SOURCE_C4_PREFLIGHT_RECEIPT_ID,
        "c4_opening_gate_status": "OPEN_FOR_NARROW_ACCEPTED_PROPOSAL_TEST" if gate_open else "BLOCKED",
        "blocking_reason": None if gate_open else "C3_INTERFACE_VERDICT",
        "accepted_proposal_required_for_execution": True,
        "accepted_proposal_present": False,
        "accepted_proposal_consumption_allowed_later": gate_open,
        "cell1_execution_opened": False,
        "cell1_execution_authorized_now": False,
        "must_not_infer": [
            "Cell 1 executed",
            "accepted proposal exists",
            "proposal accepted by Cell 1",
            "build occurred",
            "C5 authorized",
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_C4_PREFLIGHT_READY_FOR_ACCEPTED_PROPOSAL_PACKET" if gate_open else "STOP_C4_BLOCKED_BY_C3_INTERFACE_VERDICT",
            "next_command_goal": None,
        },
    }

def accepted_proposal_readiness_record(gate: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "accepted_proposal_readiness_record_v0",
        "record_id": "accepted_proposal_readiness_" + sha8({"gate": gate["c4_opening_gate_status"]}),
        "accepted_proposal_input_schema_ref": rel(SOURCE_C4_ACCEPTED_PROPOSAL_SCHEMA_PATH),
        "c1_candidate_interface_schema_ref": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "required_statuses": read_json(SOURCE_C4_ACCEPTED_PROPOSAL_SCHEMA_PATH).get("accepted_statuses", []),
        "rejected_statuses": read_json(SOURCE_C4_ACCEPTED_PROPOSAL_SCHEMA_PATH).get("rejected_statuses", []),
        "review_receipt_required": True,
        "accepted_proposal_present": False,
        "readiness_status": "READY_TO_EVALUATE_ONE_ACCEPTED_PROPOSAL_PACKET",
        "cell1_execution_opened": False,
        "must_not_infer": [
            "accepted proposal exists",
            "Cell 1 can accept proposal",
            "proposal status may be promoted",
        ],
    }

def cell1_gate_status(gate: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_gate_status_v0",
        "cell_id": "CELL_1",
        "gate_status": gate["c4_opening_gate_status"],
        "execution_status": "NOT_OPENED",
        "next_required_input": "ONE_ACCEPTED_PROPOSAL_PACKET_WITH_REVIEW_RECEIPT",
        "next_required_input_present": False,
        "may_consume_proposed_only": False,
        "may_accept_proposal": False,
        "may_open_cell1_execution_now": False,
        "may_rerun_c4_execution_now": False,
        "terminal": gate["terminal"],
    }

def rollup(gate: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c4_preflight_rerun_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_c3_rerun_receipt_id": SOURCE_C3_RERUN_RECEIPT_ID,
        "source_c3_rerun_verdict": gate["observed_verdict"],
        "source_prior_c4_preflight_receipt_id": SOURCE_C4_PREFLIGHT_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "c4_opening_gate_status": gate["c4_opening_gate_status"],
        "accepted_proposal_required_for_execution": True,
        "accepted_proposals_consumed": 0,
        "builds_attempted": 0,
        "builds_verified": 0,
        "builds_blocked": 0,
        "gate_opened_for_future_accepted_proposal_count": 1 if gate["c4_opening_gate_status"] == "OPEN_FOR_NARROW_ACCEPTED_PROPOSAL_TEST" else 0,
        "cell1_execution_opened_count": 0,
        "proposed_only_packet_consumed_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "proposal_accepted_by_cell1_count": 0,
        "proposal_status_promoted_count": 0,
        "patch_applied_count": 0,
        "probe_run_count": 0,
        "verification_pass_emitted_count": 0,
        "builder_command_emitted_count": 0,
        "hidden_next_command_count": 0,
        "c5_opened_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "runtime_patch_applied_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "ready_verdict_counted_as_cell1_execution_count": 0,
        "gate_open_counted_as_build_count": 0,
        "accepted_proposal_required_but_missing_count": 0,
        "recommended_next": "PROVIDE_OR_REVIEW_ONE_ACCEPTED_PROPOSAL_PACKET_FOR_C4_CONSUMPTION",
    }

def profile(rollup_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c4_preflight_rerun_profile_v0",
        "profile_id": "c4_preflight_rerun_" + sha8({"gate": rollup_obj["c4_opening_gate_status"], "source": SOURCE_C3_RERUN_RECEIPT_ID}),
        "status": "C4_PREFLIGHT_READY_FOR_ACCEPTED_PROPOSAL_PACKET",
        "cell_id": "CELL_1",
        "active_object": "Cell 1 receipt-native builder opening gate after C3 rerun",
        "source_c3_rerun_receipt_id": SOURCE_C3_RERUN_RECEIPT_ID,
        "source_prior_c4_preflight_receipt_id": SOURCE_C4_PREFLIGHT_RECEIPT_ID,
        "opening_gate_ref": rel(OPENING_GATE_EVALUATION_PATH),
        "rollup_ref": rel(ROLLUP_PATH),
        "cell1_execution_opened": False,
        "accepted_proposal_consumed": False,
        "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "must_not_infer": [
            "Cell 1 executed",
            "accepted proposal exists",
            "build occurred",
            "verification passed",
            "C5 authorized",
        ],
        "next_command_goal": None,
    }

def report(rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c4_preflight_rerun_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_c3_rerun_verdict_consumed_count": 1,
        "source_prior_c4_preflight_consumed_count": 1,
        "source_c1_patch_schema_consumed_count": 1,
        "source_c2_lane_registry_consumed_count": 1,
        "opening_gate_evaluation_emitted_count": 1,
        "accepted_proposal_readiness_record_emitted_count": 1,
        "cell1_gate_status_emitted_count": 1,
        "profile_status": profile_obj["status"],
        "c4_opening_gate_status": rollup_obj["c4_opening_gate_status"],
        "accepted_proposals_consumed": rollup_obj["accepted_proposals_consumed"],
        "builds_attempted": rollup_obj["builds_attempted"],
        "builds_verified": rollup_obj["builds_verified"],
        "gate_opened_for_future_accepted_proposal_count": rollup_obj["gate_opened_for_future_accepted_proposal_count"],
        "cell1_execution_opened_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "proposal_status_promoted_count": 0,
        "builder_command_emitted_count": 0,
        "hidden_next_command_count": 0,
        "c5_opened_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "runtime_patch_applied_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "recommended_next_handling": rollup_obj["recommended_next"],
    }

def transition_trace(gate: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c4_preflight_rerun_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c3_rerun_verdict",
                "question": "does C3 rerun permit C4 preflight to open for narrow accepted proposal test",
                "answer": gate["observed_verdict"],
                "taken": "open_gate_for_future_accepted_proposal_packet",
            },
            {
                "step": "open_gate_for_future_accepted_proposal_packet",
                "question": "does this unit have an accepted proposal packet to consume",
                "answer": False,
                "taken": "emit_ready_for_accepted_proposal_packet_stop",
            },
            {
                "step": "stop_without_cell1_execution",
                "question": "did C4 avoid build execution and hidden continuation",
                "answer": True,
                "taken": "stop",
            },
        ],
        "terminal": gate["terminal"],
    }

def validate_outputs(gate: Dict[str, Any], readiness: Dict[str, Any], gate_status: Dict[str, Any], rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any], report_obj: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if gate["observed_verdict"] != ALLOWED_C3_VERDICT:
        failures.append(f"opening_gate_observed_verdict_not_ready:{gate['observed_verdict']}")
    if gate["c4_opening_gate_status"] != "OPEN_FOR_NARROW_ACCEPTED_PROPOSAL_TEST":
        failures.append(f"opening_gate_not_open:{gate['c4_opening_gate_status']}")
    if gate["cell1_execution_opened"] is not False:
        failures.append("opening_gate_claims_cell1_execution")
    if gate["cell1_execution_authorized_now"] is not False:
        failures.append("opening_gate_authorizes_cell1_execution_now")
    if gate["accepted_proposal_present"] is not False:
        failures.append("opening_gate_claims_accepted_proposal_present")
    if readiness["accepted_proposal_present"] is not False:
        failures.append("readiness_claims_accepted_proposal_present")
    if readiness["cell1_execution_opened"] is not False:
        failures.append("readiness_claims_cell1_execution_opened")
    if gate_status["execution_status"] != "NOT_OPENED":
        failures.append("gate_status_execution_opened")
    if gate_status["may_consume_proposed_only"] is not False:
        failures.append("gate_status_allows_proposed_only")
    if gate_status["may_accept_proposal"] is not False:
        failures.append("gate_status_allows_cell1_acceptance")
    if gate_status["may_open_cell1_execution_now"] is not False:
        failures.append("gate_status_allows_cell1_execution_now")
    if gate_status["next_required_input"] != "ONE_ACCEPTED_PROPOSAL_PACKET_WITH_REVIEW_RECEIPT":
        failures.append("gate_status_wrong_next_required_input")
    for key in ZERO_COUNTER_KEYS:
        if rollup_obj.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup_obj.get(key)}")
    if rollup_obj["gate_opened_for_future_accepted_proposal_count"] != 1:
        failures.append("gate_open_future_count_not_one")
    if profile_obj["cell1_execution_opened"] is not False:
        failures.append("profile_claims_cell1_execution_opened")
    if profile_obj["accepted_proposal_consumed"] is not False:
        failures.append("profile_claims_accepted_proposal_consumed")
    if profile_obj["next_command_goal"] is not None:
        failures.append("profile_hidden_next_command")
    for key in [
        "accepted_proposals_consumed",
        "builds_attempted",
        "builds_verified",
        "cell1_execution_opened_count",
        "accepted_proposal_fabricated_count",
        "proposal_status_promoted_count",
        "builder_command_emitted_count",
        "hidden_next_command_count",
        "c5_opened_count",
        "taxonomy_registry_mutation_count",
        "runtime_patch_applied_count",
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
    if terminal.get("stop_code") != "STOP_C4_PREFLIGHT_READY_FOR_ACCEPTED_PROPOSAL_PACKET":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    gate = read_json(OPENING_GATE_EVALUATION_PATH)
    readiness = read_json(ACCEPTED_PROPOSAL_READINESS_RECORD_PATH)
    gate_status = read_json(CELL1_GATE_STATUS_PATH)
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

    bad_gate = copy.deepcopy(gate)
    bad_gate["observed_verdict"] = "CELL1_NOT_READY_PROPOSAL_SCHEMA_GAPS"
    add("ready_verdict_missing_fail", validate_outputs(bad_gate, readiness, gate_status, rollup_obj, profile_obj, report_obj), "opening_gate_observed_verdict_not_ready")

    bad_gate = copy.deepcopy(gate)
    bad_gate["c4_opening_gate_status"] = "BLOCKED"
    add("gate_remains_blocked_fail", validate_outputs(bad_gate, readiness, gate_status, rollup_obj, profile_obj, report_obj), "opening_gate_not_open")

    bad_gate = copy.deepcopy(gate)
    bad_gate["cell1_execution_opened"] = True
    add("opening_gate_claims_cell1_execution_fail", validate_outputs(bad_gate, readiness, gate_status, rollup_obj, profile_obj, report_obj), "opening_gate_claims_cell1_execution")

    bad_gate = copy.deepcopy(gate)
    bad_gate["cell1_execution_authorized_now"] = True
    add("opening_gate_authorizes_cell1_now_fail", validate_outputs(bad_gate, readiness, gate_status, rollup_obj, profile_obj, report_obj), "opening_gate_authorizes_cell1_execution_now")

    bad_gate = copy.deepcopy(gate)
    bad_gate["accepted_proposal_present"] = True
    add("accepted_proposal_present_without_input_fail", validate_outputs(bad_gate, readiness, gate_status, rollup_obj, profile_obj, report_obj), "opening_gate_claims_accepted_proposal_present")

    bad_gate_status = copy.deepcopy(gate_status)
    bad_gate_status["may_consume_proposed_only"] = True
    add("proposed_only_consumption_allowed_fail", validate_outputs(gate, readiness, bad_gate_status, rollup_obj, profile_obj, report_obj), "gate_status_allows_proposed_only")

    bad_gate_status = copy.deepcopy(gate_status)
    bad_gate_status["may_accept_proposal"] = True
    add("cell1_acceptance_allowed_fail", validate_outputs(gate, readiness, bad_gate_status, rollup_obj, profile_obj, report_obj), "gate_status_allows_cell1_acceptance")

    bad_gate_status = copy.deepcopy(gate_status)
    bad_gate_status["may_open_cell1_execution_now"] = True
    add("cell1_execution_allowed_now_fail", validate_outputs(gate, readiness, bad_gate_status, rollup_obj, profile_obj, report_obj), "gate_status_allows_cell1_execution_now")

    for case, counter in [
        ("accepted_proposals_consumed_fail", "accepted_proposals_consumed"),
        ("accepted_proposal_fabricated_fail", "accepted_proposal_fabricated_count"),
        ("proposal_status_promoted_fail", "proposal_status_promoted_count"),
        ("build_attempted_during_preflight_rerun_fail", "builds_attempted"),
        ("cell1_execution_opened_fail", "cell1_execution_opened_count"),
        ("patch_applied_fail", "patch_applied_count"),
        ("probe_run_fail", "probe_run_count"),
        ("verification_pass_emitted_fail", "verification_pass_emitted_count"),
        ("builder_command_emitted_fail", "builder_command_emitted_count"),
        ("hidden_next_command_fail", "hidden_next_command_count"),
        ("c5_opened_fail", "c5_opened_count"),
        ("taxonomy_registry_mutated_fail", "taxonomy_registry_mutation_count"),
        ("runtime_patch_applied_fail", "runtime_patch_applied_count"),
        ("source_mutation_fail", "source_mutation_count"),
        ("prior_receipt_mutation_fail", "prior_receipt_mutation_count"),
        ("ready_verdict_counted_as_cell1_execution_fail", "ready_verdict_counted_as_cell1_execution_count"),
        ("gate_open_counted_as_build_fail", "gate_open_counted_as_build_count"),
    ]:
        bad_rollup = copy.deepcopy(rollup_obj)
        bad_report = copy.deepcopy(report_obj)
        bad_rollup[counter] = 1
        if counter in bad_report:
            bad_report[counter] = 1
        add(case, validate_outputs(gate, readiness, gate_status, bad_rollup, profile_obj, bad_report), counter)

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_C4_PREFLIGHT_RERUN_DEPENDENCY_MISSING", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "c4_preflight_rerun_receipt_v0",
            "receipt_type": "C4_PREFLIGHT_RERUN_RECEIPT",
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
        print(f"c4_preflight_rerun_receipt_id={receipt_id}")
        print(f"c4_preflight_rerun_receipt_path=data/c4_cell1_receipt_native_builder_preflight_rerun_v0_receipts/{receipt_id}.json")
        return 1

    gate = opening_gate_evaluation()
    readiness = accepted_proposal_readiness_record(gate)
    gate_status = cell1_gate_status(gate)
    rollup_obj = rollup(gate)
    profile_obj = profile(rollup_obj)
    report_obj = report(rollup_obj, profile_obj)
    trace = transition_trace(gate)

    write_json(SOURCE_SURFACE_PATH, source_surface())
    write_json(OPENING_GATE_EVALUATION_PATH, gate)
    write_json(ACCEPTED_PROPOSAL_READINESS_RECORD_PATH, readiness)
    write_json(CELL1_GATE_STATUS_PATH, gate_status)
    write_json(ROLLUP_PATH, rollup_obj)
    write_json(PROFILE_PATH, profile_obj)
    write_json(REPORT_PATH, report_obj)
    write_json(TRANSITION_TRACE_PATH, trace)

    failures.extend(validate_outputs(gate, readiness, gate_status, rollup_obj, profile_obj, report_obj))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup_obj["source_mutation_count"] = 1
        report_obj["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup_obj)
        write_json(REPORT_PATH, report_obj)

    acceptance_gate_results = {
        "C4_RERUN_0_C3_RERUN_VERDICT_CONSUMED": SOURCE_C3_RERUN_VERDICT_PATH.exists(),
        "C4_RERUN_1_C3_VERDICT_READY": gate["observed_verdict"] == ALLOWED_C3_VERDICT,
        "C4_RERUN_2_PRIOR_C4_PREFLIGHT_SCHEMA_SURFACE_CONSUMED": SOURCE_C4_ACCEPTED_PROPOSAL_SCHEMA_PATH.exists() and SOURCE_C4_AUTHORITY_PROFILE_PATH.exists(),
        "C4_RERUN_3_C1_INTERFACE_PATCH_SCHEMA_CONSUMED": SOURCE_C1_PATCH_SCHEMA_PATH.exists(),
        "C4_RERUN_4_C2_LANE_REGISTRY_CONSUMED": SOURCE_C2_LANE_REGISTRY_PATH.exists(),
        "C4_RERUN_5_OPENING_GATE_EVALUATION_EMITTED": OPENING_GATE_EVALUATION_PATH.exists(),
        "C4_RERUN_6_OPENING_GATE_OPEN_FOR_NARROW_ACCEPTED_PROPOSAL_TEST": gate["c4_opening_gate_status"] == "OPEN_FOR_NARROW_ACCEPTED_PROPOSAL_TEST",
        "C4_RERUN_7_ACCEPTED_PROPOSAL_REQUIRED_FOR_EXECUTION": gate["accepted_proposal_required_for_execution"] is True,
        "C4_RERUN_8_NO_ACCEPTED_PROPOSAL_CONSUMED": rollup_obj["accepted_proposals_consumed"] == 0,
        "C4_RERUN_9_NO_PROPOSED_ONLY_CONSUMED": rollup_obj["proposed_only_packet_consumed_count"] == 0,
        "C4_RERUN_10_NO_ACCEPTED_PROPOSAL_FABRICATED": rollup_obj["accepted_proposal_fabricated_count"] == 0,
        "C4_RERUN_11_NO_CELL1_EXECUTION_OPENED": rollup_obj["cell1_execution_opened_count"] == 0 and gate["cell1_execution_opened"] is False,
        "C4_RERUN_12_NO_BUILD_ATTEMPTED": rollup_obj["builds_attempted"] == 0,
        "C4_RERUN_13_NO_PATCH_PROBE_OR_VERIFICATION": rollup_obj["patch_applied_count"] == 0 and rollup_obj["probe_run_count"] == 0 and rollup_obj["verification_pass_emitted_count"] == 0,
        "C4_RERUN_14_NO_BUILDER_COMMAND_EMITTED": rollup_obj["builder_command_emitted_count"] == 0,
        "C4_RERUN_15_NO_C5_OPENED": rollup_obj["c5_opened_count"] == 0,
        "C4_RERUN_16_NO_TAXONOMY_OR_RUNTIME_MUTATION": rollup_obj["taxonomy_registry_mutation_count"] == 0 and rollup_obj["runtime_patch_applied_count"] == 0,
        "C4_RERUN_17_READY_VERDICT_NOT_COUNTED_AS_CELL1_EXECUTION": rollup_obj["ready_verdict_counted_as_cell1_execution_count"] == 0,
        "C4_RERUN_18_GATE_OPEN_NOT_COUNTED_AS_BUILD": rollup_obj["gate_open_counted_as_build_count"] == 0,
        "C4_RERUN_19_NO_HIDDEN_NEXT_COMMAND": rollup_obj["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
        "C4_RERUN_20_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    for gate_name, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate_name}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_c3_rerun": SOURCE_C3_RERUN_RECEIPT_ID,
        "source_c4_preflight": SOURCE_C4_PREFLIGHT_RECEIPT_ID,
        "gate": gate["c4_opening_gate_status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "opening_gate_evaluation": rel(OPENING_GATE_EVALUATION_PATH),
        "accepted_proposal_readiness_record": rel(ACCEPTED_PROPOSAL_READINESS_RECORD_PATH),
        "cell1_gate_status": rel(CELL1_GATE_STATUS_PATH),
        "rollup": rel(ROLLUP_PATH),
        "profile": rel(PROFILE_PATH),
        "report": rel(REPORT_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_c3_rerun_receipt": rel(SOURCE_C3_RERUN_RECEIPT_PATH),
        "source_c3_rerun_verdict": rel(SOURCE_C3_RERUN_VERDICT_PATH),
        "source_prior_c4_preflight_receipt": rel(SOURCE_C4_PREFLIGHT_RECEIPT_PATH),
        "source_c4_accepted_proposal_schema": rel(SOURCE_C4_ACCEPTED_PROPOSAL_SCHEMA_PATH),
        "source_c1_patch_schema": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "source_c2_lane_registry": rel(SOURCE_C2_LANE_REGISTRY_PATH),
    }

    guards = {
        "build_mode_preflight_gate_rerun_only": BUILD_MODE == "PREFLIGHT_GATE_RERUN_ONLY",
        "c3_rerun_verdict_ready": gate["observed_verdict"] == ALLOWED_C3_VERDICT,
        "opening_gate_open_for_narrow_accepted_proposal_test": gate["c4_opening_gate_status"] == "OPEN_FOR_NARROW_ACCEPTED_PROPOSAL_TEST",
        "accepted_proposal_required_for_execution": True,
        "accepted_proposal_consumed": False,
        "accepted_proposal_fabricated": False,
        "proposed_only_packet_consumed": False,
        "cell1_execution_opened": False,
        "patch_applied": False,
        "probe_run": False,
        "verification_pass_emitted": False,
        "builder_command_emitted": False,
        "c5_opened": False,
        "taxonomy_registry_mutated": False,
        "runtime_patch_applied": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
    }

    receipt = {
        "schema_version": "c4_preflight_rerun_receipt_v0",
        "receipt_type": "C4_PREFLIGHT_RERUN_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "Cell 1 receipt-native builder opening gate after C3 rerun",
        "source_c3_rerun_receipt_id": SOURCE_C3_RERUN_RECEIPT_ID,
        "source_prior_c4_preflight_receipt_id": SOURCE_C4_PREFLIGHT_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "c4_preflight_rerun_summary": {
            "profile_status": profile_obj["status"],
            "source_c3_rerun_verdict": gate["observed_verdict"],
            "c4_opening_gate_status": gate["c4_opening_gate_status"],
            "accepted_proposal_required_for_execution": True,
            "accepted_proposals_consumed": 0,
            "builds_attempted": 0,
            "builds_verified": 0,
            "cell1_execution_opened": False,
            "gate_opened_for_future_accepted_proposal_count": rollup_obj["gate_opened_for_future_accepted_proposal_count"],
            "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
            "recommended_next": rollup_obj["recommended_next"],
        },
        "aggregate_metrics": {
            **{k: v for k, v in report_obj.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
            "rollup": rollup_obj,
            "source_mutation_count": 1 if source_mutation_detected else report_obj["source_mutation_count"],
        },
        "acceptance_gate_results": acceptance_gate_results,
        "c4_preflight_rerun_guards": guards,
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
    if len(negative_controls) != 25 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
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
    print(f"c4_preflight_rerun_receipt_id={receipt_id}")
    print(f"c4_preflight_rerun_receipt_path=data/c4_cell1_receipt_native_builder_preflight_rerun_v0_receipts/{receipt_id}.json")
    print(f"c4_preflight_rerun_profile_path=data/c4_cell1_receipt_native_builder_preflight_rerun_v0/c4_preflight_rerun_profile_v0.json")
    print(f"c4_preflight_rerun_rollup_path=data/c4_cell1_receipt_native_builder_preflight_rerun_v0/c4_preflight_rerun_rollup_v0.json")
    print(f"c4_preflight_rerun_gate_path=data/c4_cell1_receipt_native_builder_preflight_rerun_v0/c4_opening_gate_evaluation_v0_1.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
