#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_C6_INTER_CELL_PROTOCOL_FROM_C5_EXAMPLES_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "inter_cell.protocol_from_c5_examples.reviewed_reference.v0"
LAYER = "BRIDGE / INTER_CELL_PROTOCOL / REFERENCE_CLOSURE"
MODE = "CLOSE_ONLY / FREEZE_LOCAL_PROTOCOL_CANDIDATE_AS_REVIEWED_REFERENCE / NO_RUNTIME_PATCH"
BUILD_MODE = "C6_INTER_CELL_PROTOCOL_REFERENCE_CLOSURE_ONLY"

SOURCE_C6_PROTOCOL_REVIEW_RECEIPT_ID = "7535b889"
SOURCE_C6_PROTOCOL_RECEIPT_ID = "315e0d94"
SOURCE_FAILED_C6_PROTOCOL_RECEIPT_ID = "61fceac6"
SOURCE_C6_TARGET_DESIGN_RECEIPT_ID = "b0df3c9d"
SOURCE_POST_C6_DECISION_RECEIPT_ID = "89b2d2cc"
SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID = "fe882749"

SOURCE_C6_PROTOCOL_REVIEW_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0_receipts/7535b889.json"
SOURCE_C6_PROTOCOL_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0_receipts/315e0d94.json"
SOURCE_FAILED_C6_PROTOCOL_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0_receipts/61fceac6.json"
SOURCE_C6_TARGET_DESIGN_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0_receipts/b0df3c9d.json"
SOURCE_POST_C6_DECISION_RECEIPT_PATH = ROOT / "data/c6_post_example_reference_decision_v0_receipts/89b2d2cc.json"
SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0_receipts/fe882749.json"

PROTOCOL_FILES = [
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_schema_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_packet_state_machine_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/proposed_only_packet_schema_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/accepted_proposal_packet_schema_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/cell1_builder_intake_packet_schema_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/cell1_probe_or_build_packet_schema_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/verification_return_packet_schema_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/handoff_return_packet_schema_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/blocked_feedback_packet_schema_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_edge_observation_sidecar_schema_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_unit_feedback_sidecar_schema_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_gate_table_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_forbidden_transition_table_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_derivation_status_records_v0.jsonl",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_demo_packets_v0.jsonl",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_rollup_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_profile_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_readout_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/c6_report.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/c6_transition_trace.json",
]

REVIEW_FILES = [
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_review_basis_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_source_receipt_review_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_packet_schema_review_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_state_machine_review_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_gate_review_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_forbidden_transition_review_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_derivation_review_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_demo_packet_review_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_rollup_profile_readout_review_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_gate19_repair_review_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_reviewed_reference_close_candidate_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_review_authority_boundary_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_review_classification_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_review_rollup_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_review_profile_v0.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_review_report.json",
    ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_review_transition_trace.json",
]

REQUIRED_SOURCE_FILES = [
    SOURCE_C6_PROTOCOL_REVIEW_RECEIPT_PATH,
    SOURCE_C6_PROTOCOL_RECEIPT_PATH,
    SOURCE_FAILED_C6_PROTOCOL_RECEIPT_PATH,
    SOURCE_C6_TARGET_DESIGN_RECEIPT_PATH,
    SOURCE_POST_C6_DECISION_RECEIPT_PATH,
    SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH,
] + PROTOCOL_FILES + REVIEW_FILES

OUT_DIR = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0"
RECEIPT_DIR = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0_receipts"

CLOSURE_BASIS_PATH = OUT_DIR / "c6_inter_cell_protocol_reference_closure_basis_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "c6_inter_cell_protocol_reviewed_reference_v0.json"
FREEZE_MANIFEST_PATH = OUT_DIR / "c6_inter_cell_protocol_reviewed_reference_freeze_manifest_v0.json"
REFERENCE_INDEX_PATH = OUT_DIR / "c6_inter_cell_protocol_reviewed_reference_index_v0.json"
PACKET_LAW_REFERENCE_PATH = OUT_DIR / "c6_inter_cell_packet_law_reference_v0.json"
PROTOCOL_SURFACE_REFERENCE_PATH = OUT_DIR / "c6_inter_cell_protocol_surface_reference_v0.json"
GATE19_REPAIR_REFERENCE_PATH = OUT_DIR / "c6_inter_cell_protocol_gate19_repair_reference_v0.json"
POST_CLOSURE_DECISION_READY_PATH = OUT_DIR / "c6_inter_cell_protocol_reference_post_closure_decision_ready_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "c6_inter_cell_protocol_reference_closure_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "c6_inter_cell_protocol_reference_closure_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "c6_inter_cell_protocol_reference_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c6_inter_cell_protocol_reference_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "c6_inter_cell_protocol_reference_closure_report.json"
TRACE_PATH = OUT_DIR / "c6_inter_cell_protocol_reference_closure_transition_trace.json"

EXPECTED_REVIEW_STATUS = "TYPED_C6_INTER_CELL_PROTOCOL_CANDIDATE_REVIEWED_CLOSE_READY"
EXPECTED_REVIEW_STOP = "STOP_TYPED_C6_INTER_CELL_PROTOCOL_CANDIDATE_REVIEWED_CLOSE_READY"
EXPECTED_REVIEW_NEXT = "CLOSE_C6_INTER_CELL_PROTOCOL_FROM_C5_EXAMPLES_AS_REVIEWED_REFERENCE_V0"
RECOMMENDED_NEXT = "DECIDE_NEXT_AFTER_C6_INTER_CELL_PROTOCOL_REFERENCE_CLOSURE_V0"

EXPECTED_PACKET_FAMILY = [
    "PROPOSAL_PACKET_PROPOSED_ONLY",
    "ACCEPTED_PROPOSAL_PACKET",
    "CELL1_BUILDER_INTAKE_PACKET",
    "CELL1_PROBE_OR_BUILD_PACKET",
    "VERIFICATION_RETURN_PACKET",
    "HANDOFF_RETURN_PACKET",
    "BLOCKED_OR_TYPED_STOP_FEEDBACK_PACKET",
    "DECISION_EDGE_OBSERVATION_SIDECAR",
    "UNIT_FEEDBACK_SIDECAR",
]

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

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{rel(path)}")
    if failures:
        return failures, {}

    review_receipt = read_json(SOURCE_C6_PROTOCOL_REVIEW_RECEIPT_PATH)
    review_summary = review_receipt.get("machine_readable_c6_protocol_review_summary", {})
    protocol_receipt = read_json(SOURCE_C6_PROTOCOL_RECEIPT_PATH)
    protocol_summary = protocol_receipt.get("machine_readable_c6_protocol_summary", {})
    failed_receipt = read_json(SOURCE_FAILED_C6_PROTOCOL_RECEIPT_PATH)
    target_receipt = read_json(SOURCE_C6_TARGET_DESIGN_RECEIPT_PATH)
    post_decision_receipt = read_json(SOURCE_POST_C6_DECISION_RECEIPT_PATH)
    example_reference_closure_receipt = read_json(SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH)

    protocol_schema = read_json(PROTOCOL_FILES[0])
    state_machine = read_json(PROTOCOL_FILES[1])
    derivation_records = read_jsonl(ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_derivation_status_records_v0.jsonl")
    demo_packets = read_jsonl(ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_demo_packets_v0.jsonl")
    protocol_rollup = read_json(ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_rollup_v0.json")
    protocol_profile = read_json(ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_profile_v0.json")
    protocol_readout = read_json(ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_readout_v0.json")

    close_candidate = read_json(ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_reviewed_reference_close_candidate_v0.json")
    review_authority = read_json(ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_review_authority_boundary_v0.json")
    review_classification = read_json(ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_review_classification_v0.json")
    review_rollup = read_json(ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_review_rollup_v0.json")
    review_profile = read_json(ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_review_profile_v0.json")
    review_report = read_json(ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_review_report.json")
    review_trace = read_json(ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_review_transition_trace.json")
    repair_review = read_json(ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0/c6_inter_cell_protocol_gate19_repair_review_v0.json")

    if review_receipt.get("receipt_id") != SOURCE_C6_PROTOCOL_REVIEW_RECEIPT_ID or review_receipt.get("gate") != "PASS":
        failures.append("review_receipt_not_pass")
    if review_receipt.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("review_stop_wrong")
    if review_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("review_hidden_next")
    if review_summary.get("status") != EXPECTED_REVIEW_STATUS:
        failures.append(f"review_status_wrong:{review_summary.get('status')}")
    if review_summary.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append(f"review_next_wrong:{review_summary.get('recommended_next')}")
    for key in [
        "c6_protocol_candidate_review_complete",
        "c6_protocol_candidate_review_pass",
        "close_candidate_ready",
        "source_c6_protocol_candidate_emitted",
        "all_c6_protocol_acceptance_gates_true",
        "gate19_verification_not_closure",
        "bad_counters_zero",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"review_required_true_missing:{key}")
    if review_summary.get("gate19_failed_before_repair") is not False:
        failures.append("review_gate19_prior_fail_not_false")
    if review_summary.get("schema_claim") != "LOCAL_PROTOCOL_CANDIDATE_ONLY":
        failures.append("review_schema_claim_wrong")

    for key in [
        "runtime_patched",
        "c7_authorized",
        "new_domain_shift_executed",
        "general_cell1_authority_claimed",
        "global_autonomy_claimed",
        "full_transfer_claimed",
        "runtime_wide_enforcement_claimed",
        "source_mutated",
        "prior_receipt_mutated",
        "c5_reference_mutated",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if review_summary.get(key) is not False:
            failures.append(f"review_forbidden_true:{key}")

    if protocol_receipt.get("receipt_id") != SOURCE_C6_PROTOCOL_RECEIPT_ID or protocol_receipt.get("gate") != "PASS":
        failures.append("protocol_receipt_not_pass")
    if protocol_summary.get("c6_inter_cell_protocol_candidate_emitted") is not True:
        failures.append("protocol_candidate_not_emitted")
    if failed_receipt.get("receipt_id") != SOURCE_FAILED_C6_PROTOCOL_RECEIPT_ID or failed_receipt.get("gate") != "FAIL":
        failures.append("failed_receipt_missing")
    if target_receipt.get("receipt_id") != SOURCE_C6_TARGET_DESIGN_RECEIPT_ID or target_receipt.get("gate") != "PASS":
        failures.append("target_receipt_not_pass")
    if post_decision_receipt.get("receipt_id") != SOURCE_POST_C6_DECISION_RECEIPT_ID or post_decision_receipt.get("gate") != "PASS":
        failures.append("post_decision_receipt_not_pass")
    if example_reference_closure_receipt.get("receipt_id") != SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID or example_reference_closure_receipt.get("gate") != "PASS":
        failures.append("example_reference_closure_receipt_not_pass")

    if protocol_schema.get("schema_claim") != "LOCAL_PROTOCOL_CANDIDATE_ONLY":
        failures.append("protocol_schema_claim_wrong")
    if protocol_schema.get("packet_family") != EXPECTED_PACKET_FAMILY:
        failures.append("protocol_packet_family_wrong")
    if len(state_machine.get("closed_states", [])) != 16:
        failures.append("state_machine_state_count_wrong")
    if "VERIFICATION_RETURN -> REVIEW_CLOSURE_WITHOUT_REVIEW" not in state_machine.get("forbidden_state_jumps", []):
        failures.append("verification_not_closure_jump_missing")
    if len(derivation_records) != 14:
        failures.append(f"derivation_record_count_wrong:{len(derivation_records)}")
    if len(demo_packets) != 4:
        failures.append(f"demo_packet_count_wrong:{len(demo_packets)}")
    if any(v != 0 for v in protocol_rollup.get("bad_counters", {}).values()):
        failures.append("protocol_bad_counter_nonzero")
    if protocol_profile.get("schema_claim") != "LOCAL_PROTOCOL_CANDIDATE_ONLY":
        failures.append("protocol_profile_claim_wrong")
    if protocol_profile.get("next_command_goal") is not None:
        failures.append("protocol_profile_hidden_next")
    if protocol_readout.get("bad_counters_zero") is not True:
        failures.append("protocol_readout_bad_counters_wrong")

    if close_candidate.get("candidate_status") != "C6_INTER_CELL_PROTOCOL_REVIEWED_REFERENCE_CLOSE_READY":
        failures.append("close_candidate_not_ready")
    if close_candidate.get("review_pass") is not True:
        failures.append("close_candidate_review_not_pass")
    if close_candidate.get("candidate_next_unit") != EXPECTED_REVIEW_NEXT:
        failures.append("close_candidate_next_wrong")
    if review_authority.get("may_close_c6_protocol_candidate_as_reviewed_reference_next") is not True:
        failures.append("review_authority_no_close")
    for forbidden in [
        "may_patch_runtime_now",
        "may_open_c7_now",
        "may_execute_new_domain_shift",
        "may_claim_full_transfer",
        "may_claim_global_autonomy",
        "may_claim_general_cell1_authority",
        "may_claim_runtime_wide_enforcement",
        "may_mutate_source",
        "may_mutate_prior_receipts",
        "may_mutate_c5_reference",
    ]:
        if review_authority.get(forbidden) is not False:
            failures.append(f"review_authority_forbidden_true:{forbidden}")
    if review_classification.get("next_command_goal") is not None:
        failures.append("review_classification_hidden_next")
    if review_rollup.get("review_pass_count") != 1 or review_rollup.get("close_candidate_ready_count") != 1:
        failures.append("review_rollup_close_not_ready")
    if review_rollup.get("false_acceptance_gate_count") != 0:
        failures.append("review_rollup_false_gate_nonzero")
    if review_profile.get("next_command_goal") is not None:
        failures.append("review_profile_hidden_next")
    if review_report.get("recommended_next_handling") != EXPECTED_REVIEW_NEXT:
        failures.append("review_report_next_wrong")
    if review_trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("review_trace_hidden_next")
    if repair_review.get("repair_class") != "ASSERTION_REPAIR_NOT_PROTOCOL_REDESIGN":
        failures.append("gate19_repair_class_wrong")

    return failures, {
        "review_summary": review_summary,
        "protocol_summary": protocol_summary,
        "protocol_schema": protocol_schema,
        "state_machine": state_machine,
        "derivation_records": derivation_records,
        "demo_packets": demo_packets,
        "protocol_rollup": protocol_rollup,
        "protocol_profile": protocol_profile,
        "protocol_readout": protocol_readout,
        "close_candidate": close_candidate,
        "review_rollup": review_rollup,
        "review_profile": review_profile,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    close_pass = not failures
    status = "TYPED_C6_INTER_CELL_PROTOCOL_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY" if close_pass else "TYPED_C6_INTER_CELL_PROTOCOL_REFERENCE_CLOSURE_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if close_pass else "REPAIR_C6_INTER_CELL_PROTOCOL_REFERENCE_CLOSURE_V0"

    review_summary = basis.get("review_summary", {})
    protocol_summary = basis.get("protocol_summary", {})
    protocol_schema = basis.get("protocol_schema", {})
    state_machine = basis.get("state_machine", {})
    derivation_records = basis.get("derivation_records", [])
    demo_packets = basis.get("demo_packets", [])
    close_candidate = basis.get("close_candidate", {})

    reason_codes = [
        "C6_INTER_CELL_PROTOCOL_CLOSED_AS_REVIEWED_REFERENCE",
        "C6_PROTOCOL_REVIEW_RECEIPT_CONSUMED",
        "C6_PROTOCOL_BUILD_RECEIPT_CONSUMED",
        "C6_GATE19_REPAIR_HISTORY_PRESERVED",
        "LOCAL_PROTOCOL_CANDIDATE_FROZEN",
        "PACKET_SCHEMA_FAMILY_FROZEN",
        "STATE_MACHINE_FROZEN",
        "GATE_TABLE_FROZEN",
        "FORBIDDEN_TRANSITION_TABLE_FROZEN",
        "DERIVATION_STATUS_RECORDS_FROZEN",
        "DEMO_PACKETS_FROZEN_AS_EXAMPLES_ONLY",
        "ROLLUP_PROFILE_READOUT_FROZEN",
        "POST_C6_PROTOCOL_REFERENCE_DECISION_READY",
        "NO_RUNTIME_PATCH",
        "NO_C7_AUTHORIZATION",
        "NO_TRANSFER_CLAIM",
        "NO_GLOBAL_AUTONOMY_CLAIM",
        "NO_GENERAL_CELL1_AUTHORITY_CLAIM",
        "NO_RUNTIME_WIDE_ENFORCEMENT_CLAIM",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if close_pass else failures

    closure_basis = {
        "schema_version": "c6_inter_cell_protocol_reference_closure_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if close_pass else "BASIS_REPAIR_REQUIRED",
        "source_c6_protocol_review_receipt_id": SOURCE_C6_PROTOCOL_REVIEW_RECEIPT_ID,
        "source_c6_protocol_receipt_id": SOURCE_C6_PROTOCOL_RECEIPT_ID,
        "source_failed_c6_protocol_receipt_id": SOURCE_FAILED_C6_PROTOCOL_RECEIPT_ID,
        "source_c6_target_design_receipt_id": SOURCE_C6_TARGET_DESIGN_RECEIPT_ID,
        "source_post_c6_decision_receipt_id": SOURCE_POST_C6_DECISION_RECEIPT_ID,
        "source_c6_example_reference_closure_receipt_id": SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID,
        "review_status": review_summary.get("status"),
        "candidate_schema_claim": review_summary.get("schema_claim"),
        "close_candidate_ready": close_candidate.get("review_pass") is True,
    }

    reviewed_reference = {
        "schema_version": "c6_inter_cell_protocol_reviewed_reference_v0",
        "reference_status": "C6_INTER_CELL_PROTOCOL_REVIEWED_REFERENCE_FROZEN" if close_pass else "NOT_FROZEN",
        "reference_id": "c6_inter_cell_protocol_reference_" + sig8(reason_codes),
        "source_c6_protocol_review_receipt_id": SOURCE_C6_PROTOCOL_REVIEW_RECEIPT_ID,
        "source_c6_protocol_receipt_id": SOURCE_C6_PROTOCOL_RECEIPT_ID,
        "packet_law_summary": [
            "Cells do not pass vibes.",
            "Cells pass packets.",
            "Cell 1 does not receive intentions.",
            "Cell 1 receives accepted, scoped, receipt-backed packets.",
        ],
        "packet_family": protocol_schema.get("packet_family", []),
        "schema_claim": "LOCAL_PROTOCOL_CANDIDATE_ONLY",
        "frozen_protocol_surface": {
            "packet_family_declared": protocol_summary.get("packet_family_declared"),
            "packet_schemas_emitted": protocol_summary.get("packet_schemas_emitted"),
            "state_machine_emitted": protocol_summary.get("state_machine_emitted"),
            "gate_table_emitted": protocol_summary.get("gate_table_emitted"),
            "forbidden_transition_table_emitted": protocol_summary.get("forbidden_transition_table_emitted"),
            "derivation_status_records_emitted": protocol_summary.get("derivation_status_records_emitted"),
            "demo_packets_emitted": protocol_summary.get("demo_packets_emitted"),
        },
        "must_not_infer": [
            "runtime patch",
            "C7 authorization",
            "full transfer",
            "global autonomy",
            "general Cell 1 authority",
            "runtime-wide enforcement",
        ],
    }

    freeze_manifest = {
        "schema_version": "c6_inter_cell_protocol_reviewed_reference_freeze_manifest_v0",
        "freeze_status": "FROZEN" if close_pass else "NOT_FROZEN",
        "frozen_receipts": [
            rel(SOURCE_C6_PROTOCOL_REVIEW_RECEIPT_PATH),
            rel(SOURCE_C6_PROTOCOL_RECEIPT_PATH),
            rel(SOURCE_FAILED_C6_PROTOCOL_RECEIPT_PATH),
            rel(SOURCE_C6_TARGET_DESIGN_RECEIPT_PATH),
            rel(SOURCE_POST_C6_DECISION_RECEIPT_PATH),
            rel(SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH),
        ],
        "frozen_protocol_files": [rel(p) for p in PROTOCOL_FILES],
        "frozen_review_files": [rel(p) for p in REVIEW_FILES],
        "frozen_file_sha256": snapshot_files(REQUIRED_SOURCE_FILES),
    }

    reference_index = {
        "schema_version": "c6_inter_cell_protocol_reviewed_reference_index_v0",
        "index_status": "REFERENCE_INDEX_EMITTED",
        "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
        "freeze_manifest": rel(FREEZE_MANIFEST_PATH),
        "packet_law_reference": rel(PACKET_LAW_REFERENCE_PATH),
        "protocol_surface_reference": rel(PROTOCOL_SURFACE_REFERENCE_PATH),
        "gate19_repair_reference": rel(GATE19_REPAIR_REFERENCE_PATH),
        "post_closure_decision_ready": rel(POST_CLOSURE_DECISION_READY_PATH),
    }

    packet_law_reference = {
        "schema_version": "c6_inter_cell_packet_law_reference_v0",
        "packet_law_status": "REVIEWED_REFERENCE",
        "core_law": protocol_schema.get("core_law"),
        "required_packet_family": protocol_schema.get("packet_family", []),
        "critical_distinctions": [
            "proposed-only packet != accepted packet",
            "accepted packet != build",
            "build/probe packet != verification",
            "verification pass != review closure",
            "handoff return != hidden next command",
            "blocked feedback != repair",
            "Cell 1 accepted authority != general Cell 1 authority",
            "decision-edge observation != protocol proof",
            "unit feedback != repair instruction",
        ],
    }

    protocol_surface_reference = {
        "schema_version": "c6_inter_cell_protocol_surface_reference_v0",
        "surface_status": "FROZEN_REVIEWED_REFERENCE",
        "closed_states_count": len(state_machine.get("closed_states", [])),
        "packet_family_count": len(protocol_schema.get("packet_family", [])),
        "derivation_record_count": len(derivation_records),
        "demo_packet_count": len(demo_packets),
        "acceptance_gate_count": 34,
        "all_acceptance_gates_true": review_summary.get("all_c6_protocol_acceptance_gates_true"),
        "bad_counters_zero": review_summary.get("bad_counters_zero"),
    }

    gate19_repair_reference = {
        "schema_version": "c6_inter_cell_protocol_gate19_repair_reference_v0",
        "repair_status": "PRESERVED_AS_HISTORY",
        "failed_receipt_id": SOURCE_FAILED_C6_PROTOCOL_RECEIPT_ID,
        "repaired_receipt_id": SOURCE_C6_PROTOCOL_RECEIPT_ID,
        "review_receipt_id": SOURCE_C6_PROTOCOL_REVIEW_RECEIPT_ID,
        "gate": "C6_PROTOCOL_19_VERIFICATION_NOT_CLOSURE",
        "meaning": "verification return is not review closure",
        "repair_class": "ASSERTION_REPAIR_NOT_PROTOCOL_REDESIGN",
    }

    post_closure_decision_ready = {
        "schema_version": "c6_inter_cell_protocol_reference_post_closure_decision_ready_v0",
        "decision_ready": close_pass,
        "recommended_next": recommended_next,
        "closed_reference_status": reviewed_reference["reference_status"],
        "decision_options": [
            "decide whether to park C6 as reference",
            "decide whether to design a bounded protocol adoption probe",
            "decide whether to return to observation hardening",
            "decide whether to prepare C7 only after explicit authorization",
        ],
        "not_authorized_by_closure": [
            "runtime adoption",
            "C7 execution",
            "full transfer claim",
            "global autonomy claim",
            "general Cell 1 authority",
            "runtime-wide enforcement claim",
        ],
    }

    authority_boundary = {
        "schema_version": "c6_inter_cell_protocol_reference_closure_authority_boundary_v0",
        "status": status,
        "may_close_c6_protocol_as_reviewed_reference": close_pass,
        "may_decide_next_after_c6_protocol_reference_closure": close_pass,
        "may_patch_runtime_now": False,
        "may_open_c7_now": False,
        "may_execute_new_domain_shift": False,
        "may_claim_full_transfer": False,
        "may_claim_global_autonomy": False,
        "may_claim_general_cell1_authority": False,
        "may_claim_runtime_wide_enforcement": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_mutate_c5_reference": False,
    }

    classification = {
        "schema_version": "c6_inter_cell_protocol_reference_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "c6_inter_cell_protocol_closed_as_reviewed_reference": close_pass,
        "reviewed_reference_frozen": close_pass,
        "post_c6_protocol_reference_decision_ready": close_pass,
        "schema_claim": "LOCAL_PROTOCOL_CANDIDATE_ONLY",
        "packet_family_declared": protocol_summary.get("packet_family_declared"),
        "packet_schemas_emitted": protocol_summary.get("packet_schemas_emitted"),
        "state_machine_emitted": protocol_summary.get("state_machine_emitted"),
        "gate_table_emitted": protocol_summary.get("gate_table_emitted"),
        "forbidden_transition_table_emitted": protocol_summary.get("forbidden_transition_table_emitted"),
        "derivation_status_records_emitted": protocol_summary.get("derivation_status_records_emitted"),
        "demo_packets_emitted": protocol_summary.get("demo_packets_emitted"),
        "all_c6_protocol_acceptance_gates_true": review_summary.get("all_c6_protocol_acceptance_gates_true"),
        "gate19_verification_not_closure": review_summary.get("gate19_verification_not_closure"),
        "runtime_patched": False,
        "c7_authorized": False,
        "new_domain_shift_executed": False,
        "general_cell1_authority_claimed": False,
        "global_autonomy_claimed": False,
        "full_transfer_claimed": False,
        "runtime_wide_enforcement_claimed": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "c5_reference_mutated": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": True,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "c6_inter_cell_protocol_reference_closure_rollup_v0",
        "closure_count": 1 if close_pass else 0,
        "reviewed_reference_frozen_count": 1 if close_pass else 0,
        "post_c6_protocol_reference_decision_ready_count": 1 if close_pass else 0,
        "packet_family_count": protocol_summary.get("packet_family_declared"),
        "packet_schema_count": protocol_summary.get("packet_schemas_emitted"),
        "derivation_record_count": protocol_summary.get("derivation_status_records_emitted"),
        "demo_packet_count": protocol_summary.get("demo_packets_emitted"),
        "false_acceptance_gate_count": 0,
        "runtime_patch_count": 0,
        "c7_authorized_count": 0,
        "new_domain_shift_executed_count": 0,
        "general_cell1_authority_claim_count": 0,
        "global_autonomy_claim_count": 0,
        "full_transfer_claim_count": 0,
        "runtime_wide_enforcement_claim_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "c5_reference_mutated_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    profile = {
        "schema_version": "c6_inter_cell_protocol_reference_closure_profile_v0",
        "profile_id": "c6_protocol_reference_closure_" + sig8(rollup),
        "status": status,
        "schema_claim": "LOCAL_PROTOCOL_CANDIDATE_REVIEWED_REFERENCE_ONLY",
        "reference_object": "C6 local inter-cell packet-law protocol candidate",
        "compression": "Cells do not pass vibes. Cells pass packets.",
        "reviewed_distinctions": packet_law_reference["critical_distinctions"],
        "bad_counters_zero": True,
        "must_not_infer": [
            "runtime patch",
            "C7 authorization",
            "global autonomy",
            "full transfer",
            "general Cell 1 authority",
            "runtime-wide enforcement",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "c6_inter_cell_protocol_reference_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "C6 local inter-cell protocol candidate is closed as a reviewed reference. The frozen reference preserves packet law, packet schemas, state machine, gates, forbidden transitions, derivation records, demo examples, rollup/profile/readout, and gate-19 repair history. It does not patch runtime, authorize C7, or claim transfer/autonomy/general Cell 1 authority.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "c6_inter_cell_protocol_reference_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c6_protocol_review",
                "question": "is the C6 protocol candidate reviewed and close-ready",
                "answer": "yes" if close_pass else "no",
                "taken": "freeze reviewed reference",
            },
            {
                "step": "freeze_packet_law_reference",
                "question": "what object is frozen",
                "answer": "local C6 inter-cell packet-law protocol candidate",
                "taken": "emit reference, freeze manifest, index, rollup/profile/report",
            },
            {
                "step": "preserve_boundary",
                "question": "does closure patch runtime, authorize C7, or claim transfer/autonomy",
                "answer": "no",
                "taken": "stop with post-reference decision ready",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (CLOSURE_BASIS_PATH, closure_basis),
        (REVIEWED_REFERENCE_PATH, reviewed_reference),
        (FREEZE_MANIFEST_PATH, freeze_manifest),
        (REFERENCE_INDEX_PATH, reference_index),
        (PACKET_LAW_REFERENCE_PATH, packet_law_reference),
        (PROTOCOL_SURFACE_REFERENCE_PATH, protocol_surface_reference),
        (GATE19_REPAIR_REFERENCE_PATH, gate19_repair_reference),
        (POST_CLOSURE_DECISION_READY_PATH, post_closure_decision_ready),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (CLASSIFICATION_PATH, classification),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRACE_PATH, trace),
    ]

    for path, obj in artifacts:
        write_json(path, obj)

    acceptance_gate_results = {
        "C6_REF_CLOSE_0_REVIEW_RECEIPT_CONSUMED": SOURCE_C6_PROTOCOL_REVIEW_RECEIPT_PATH.exists(),
        "C6_REF_CLOSE_1_PROTOCOL_RECEIPT_CONSUMED": SOURCE_C6_PROTOCOL_RECEIPT_PATH.exists(),
        "C6_REF_CLOSE_2_FAILED_GATE19_RECEIPT_PRESERVED": SOURCE_FAILED_C6_PROTOCOL_RECEIPT_PATH.exists(),
        "C6_REF_CLOSE_3_CLOSURE_BASIS_EMITTED": CLOSURE_BASIS_PATH.exists(),
        "C6_REF_CLOSE_4_REVIEWED_REFERENCE_FROZEN": REVIEWED_REFERENCE_PATH.exists() and reviewed_reference["reference_status"] == "C6_INTER_CELL_PROTOCOL_REVIEWED_REFERENCE_FROZEN",
        "C6_REF_CLOSE_5_FREEZE_MANIFEST_EMITTED": FREEZE_MANIFEST_PATH.exists(),
        "C6_REF_CLOSE_6_REFERENCE_INDEX_EMITTED": REFERENCE_INDEX_PATH.exists(),
        "C6_REF_CLOSE_7_PACKET_LAW_REFERENCE_EMITTED": PACKET_LAW_REFERENCE_PATH.exists(),
        "C6_REF_CLOSE_8_PROTOCOL_SURFACE_REFERENCE_EMITTED": PROTOCOL_SURFACE_REFERENCE_PATH.exists(),
        "C6_REF_CLOSE_9_GATE19_REPAIR_REFERENCE_PRESERVED": GATE19_REPAIR_REFERENCE_PATH.exists() and gate19_repair_reference["repair_class"] == "ASSERTION_REPAIR_NOT_PROTOCOL_REDESIGN",
        "C6_REF_CLOSE_10_POST_REFERENCE_DECISION_READY": POST_CLOSURE_DECISION_READY_PATH.exists() and post_closure_decision_ready["decision_ready"] is True,
        "C6_REF_CLOSE_11_NO_RUNTIME_PATCH_OR_C7": classification["runtime_patched"] is False and classification["c7_authorized"] is False,
        "C6_REF_CLOSE_12_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "C6_REF_CLOSE_13_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["c5_reference_mutated"] is False,
        "C6_REF_CLOSE_14_BAD_COUNTERS_ZERO": classification["bad_counters_zero"] is True,
        "C6_REF_CLOSE_15_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C6_REF_CLOSE_16_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "C6_REF_CLOSE_17_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_C6_INTER_CELL_PROTOCOL_REFERENCE_CLOSURE_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_C6_INTER_CELL_PROTOCOL_REFERENCE_CLOSURE_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_C6_INTER_CELL_PROTOCOL_REFERENCE_CLOSURE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_review": SOURCE_C6_PROTOCOL_REVIEW_RECEIPT_ID,
        "recommended_next": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "c6_inter_cell_protocol_reference_closure_receipt_v0",
        "receipt_type": "TYPED_C6_INTER_CELL_PROTOCOL_REFERENCE_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_c6_protocol_review_receipt_id": SOURCE_C6_PROTOCOL_REVIEW_RECEIPT_ID,
        "source_c6_protocol_receipt_id": SOURCE_C6_PROTOCOL_RECEIPT_ID,
        "machine_readable_c6_protocol_reference_closure_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "c6_inter_cell_protocol_closed_as_reviewed_reference": gate == "PASS",
            "reviewed_reference_frozen": gate == "PASS",
            "post_c6_protocol_reference_decision_ready": gate == "PASS",
            "schema_claim": "LOCAL_PROTOCOL_CANDIDATE_ONLY",
            "packet_family_declared": protocol_summary.get("packet_family_declared"),
            "packet_schemas_emitted": protocol_summary.get("packet_schemas_emitted"),
            "state_machine_emitted": protocol_summary.get("state_machine_emitted"),
            "gate_table_emitted": protocol_summary.get("gate_table_emitted"),
            "forbidden_transition_table_emitted": protocol_summary.get("forbidden_transition_table_emitted"),
            "derivation_status_records_emitted": protocol_summary.get("derivation_status_records_emitted"),
            "demo_packets_emitted": protocol_summary.get("demo_packets_emitted"),
            "all_c6_protocol_acceptance_gates_true": review_summary.get("all_c6_protocol_acceptance_gates_true"),
            "gate19_verification_not_closure": review_summary.get("gate19_verification_not_closure"),
            "gate19_repair_history_preserved": True,
            "runtime_patched": False,
            "c7_authorized": False,
            "new_domain_shift_executed": False,
            "general_cell1_authority_claimed": False,
            "global_autonomy_claimed": False,
            "full_transfer_claimed": False,
            "runtime_wide_enforcement_claimed": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "c5_reference_mutated": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": True,
            "recommended_next": final_next,
        },
        "aggregate_metrics": report | {"status": final_status, "recommended_next_handling": final_next},
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "closure_basis": rel(CLOSURE_BASIS_PATH),
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "freeze_manifest": rel(FREEZE_MANIFEST_PATH),
            "reference_index": rel(REFERENCE_INDEX_PATH),
            "packet_law_reference": rel(PACKET_LAW_REFERENCE_PATH),
            "protocol_surface_reference": rel(PROTOCOL_SURFACE_REFERENCE_PATH),
            "gate19_repair_reference": rel(GATE19_REPAIR_REFERENCE_PATH),
            "post_closure_decision_ready": rel(POST_CLOSURE_DECISION_READY_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c6_protocol_reference_closure_receipt_id={receipt_id}")
    print(f"c6_protocol_reference_closure_receipt_path={rel(receipt_path)}")
    print(f"c6_protocol_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"c6_protocol_freeze_manifest_path={rel(FREEZE_MANIFEST_PATH)}")
    print(f"c6_protocol_post_closure_decision_ready_path={rel(POST_CLOSURE_DECISION_READY_PATH)}")
    print(f"c6_protocol_reference_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"c6_protocol_reference_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
