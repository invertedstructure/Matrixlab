#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_O2_WEAK_FEEDBACK_HANDLING_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_handling.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_HANDLING"
MODE = "STATIC_WEAK_FEEDBACK_HANDLING_ONLY / NO_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_HANDLING_STATIC_ONLY"

WFH_DESIGN_RECEIPT_ID = "90309841"
WFH_DESIGN_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0_receipts/90309841.json"
WFH_TARGET_DEFINITION_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_handling_target_definition_v0.json"
WFH_SOURCE_SCOPE_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_handling_source_scope_v0.json"
WFH_INVENTORY_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_record_inventory_v0.json"
WFH_POLICY_ENUM_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_handling_policy_enum_v0.json"
WFH_QUESTION_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_question_packet_contract_v0.json"
WFH_SOURCE_REF_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_source_ref_request_contract_v0.json"
WFH_UNDERTYPED_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_under_typed_acceptance_contract_v0.json"
WFH_PARKING_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_parking_contract_v0.json"
WFH_C5_BLOCK_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_c5_block_contract_v0.json"
WFH_BUILD_AUTHORIZATION_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_handling_build_authorization_v0.json"
WFH_ACCEPTANCE_GATES_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_handling_acceptance_gates_v0.json"
WFH_NEGATIVE_CONTROLS_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_handling_negative_controls_v0.json"
WFH_TERMINAL_RULES_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_handling_terminal_rules_v0.json"
WFH_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_handling_target_authority_boundary_v0.json"
WFH_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_handling_target_classification_v0.json"
WFH_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_handling_target_rollup_v0.json"
WFH_PROFILE_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_handling_target_profile_v0.json"
WFH_REPORT_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_handling_target_report.json"

O2_FEEDBACK_RECORDS_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_feedback_records_v0.jsonl"
O2_RETRY_GATE_RECORDS_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_retry_gate_records_v0.jsonl"
O2_WEAK_FEEDBACK_NOTE_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_weak_feedback_note_v0.json"
O2_C5_BLOCK_STATUS_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_c5_block_status_v0.json"
POST_O2_DECISION_RECEIPT_PATH = ROOT / "data/o2_post_closure_decision_v0_receipts/2fef4830.json"

REQUIRED_SOURCE_FILES = [
    WFH_DESIGN_RECEIPT_PATH,
    WFH_TARGET_DEFINITION_PATH,
    WFH_SOURCE_SCOPE_PATH,
    WFH_INVENTORY_PATH,
    WFH_POLICY_ENUM_PATH,
    WFH_QUESTION_CONTRACT_PATH,
    WFH_SOURCE_REF_CONTRACT_PATH,
    WFH_UNDERTYPED_CONTRACT_PATH,
    WFH_PARKING_CONTRACT_PATH,
    WFH_C5_BLOCK_CONTRACT_PATH,
    WFH_BUILD_AUTHORIZATION_PATH,
    WFH_ACCEPTANCE_GATES_PATH,
    WFH_NEGATIVE_CONTROLS_PATH,
    WFH_TERMINAL_RULES_PATH,
    WFH_AUTHORITY_PATH,
    WFH_CLASSIFICATION_PATH,
    WFH_ROLLUP_PATH,
    WFH_PROFILE_PATH,
    WFH_REPORT_PATH,
    O2_FEEDBACK_RECORDS_PATH,
    O2_RETRY_GATE_RECORDS_PATH,
    O2_WEAK_FEEDBACK_NOTE_PATH,
    O2_C5_BLOCK_STATUS_PATH,
    POST_O2_DECISION_RECEIPT_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_handling_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_handling_v0_receipts"

HANDLING_RECORDS_PATH = OUT_DIR / "o2_weak_feedback_handling_records_v0.jsonl"
QUESTION_PACKETS_PATH = OUT_DIR / "o2_weak_feedback_question_packets_v0.jsonl"
SOURCE_REF_REQUESTS_PATH = OUT_DIR / "o2_weak_feedback_source_ref_requests_v0.jsonl"
UNDERTYPED_ACCEPTANCE_CANDIDATES_PATH = OUT_DIR / "o2_under_typed_acceptance_candidates_v0.jsonl"
PARKING_RECORDS_PATH = OUT_DIR / "o2_weak_feedback_parking_records_v0.jsonl"
C5_BLOCK_RECORDS_PATH = OUT_DIR / "o2_weak_feedback_c5_block_records_v0.jsonl"

HANDLING_READOUT_PATH = OUT_DIR / "o2_weak_feedback_handling_readout_v0.json"
HANDLING_ROLLUP_PATH = OUT_DIR / "o2_weak_feedback_handling_rollup_v0.json"
HANDLING_PROFILE_PATH = OUT_DIR / "o2_weak_feedback_handling_profile_v0.json"
HANDLING_REPORT_PATH = OUT_DIR / "o2_weak_feedback_handling_report.json"
HANDLING_TRACE_PATH = OUT_DIR / "o2_weak_feedback_handling_transition_trace.json"

EXPECTED_DESIGN_STATUS = "TYPED_O2_WEAK_FEEDBACK_HANDLING_TARGET_DESIGNED_BUILD_READY"
EXPECTED_DESIGN_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_HANDLING_TARGET_DESIGNED_BUILD_READY"
EXPECTED_DESIGN_NEXT = "BUILD_O2_WEAK_FEEDBACK_HANDLING_V0"

HANDLING_POLICIES = {
    "QUESTION_PACKET_REQUIRED",
    "SOURCE_REF_REQUEST_REQUIRED",
    "UNDER_TYPED_ACCEPTANCE_CANDIDATE",
    "PARK_WITH_REASON",
    "LIVE_AUDIT_REQUEST_CANDIDATE_ONLY",
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
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    design_receipt = read_json(WFH_DESIGN_RECEIPT_PATH)
    design_summary = design_receipt.get("machine_readable_o2_weak_feedback_target_summary", {})
    target_definition = read_json(WFH_TARGET_DEFINITION_PATH)
    inventory = read_json(WFH_INVENTORY_PATH)
    policy_enum = read_json(WFH_POLICY_ENUM_PATH)
    build_auth = read_json(WFH_BUILD_AUTHORIZATION_PATH)
    c5_contract = read_json(WFH_C5_BLOCK_CONTRACT_PATH)
    authority = read_json(WFH_AUTHORITY_PATH)
    rollup = read_json(WFH_ROLLUP_PATH)
    profile = read_json(WFH_PROFILE_PATH)
    feedback_records = read_jsonl(O2_FEEDBACK_RECORDS_PATH)
    retry_gates = read_jsonl(O2_RETRY_GATE_RECORDS_PATH)
    weak_note = read_json(O2_WEAK_FEEDBACK_NOTE_PATH)
    c5_block = read_json(O2_C5_BLOCK_STATUS_PATH)

    if design_receipt.get("receipt_id") != WFH_DESIGN_RECEIPT_ID or design_receipt.get("gate") != "PASS":
        failures.append("weak_feedback_target_design_receipt_not_pass")
    if design_receipt.get("terminal", {}).get("stop_code") != EXPECTED_DESIGN_STOP:
        failures.append("weak_feedback_target_design_terminal_not_expected")
    if design_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("weak_feedback_target_design_hidden_next_command")
    if design_summary.get("status") != EXPECTED_DESIGN_STATUS:
        failures.append(f"weak_feedback_target_design_status_not_expected:{design_summary.get('status')}")
    if design_summary.get("recommended_next") != EXPECTED_DESIGN_NEXT:
        failures.append(f"weak_feedback_target_design_next_not_expected:{design_summary.get('recommended_next')}")

    for key in [
        "target_designed",
        "handling_policy_enum_frozen",
        "question_packet_contract_frozen",
        "source_ref_request_contract_frozen",
        "under_typed_acceptance_contract_frozen",
        "parking_contract_frozen",
        "c5_block_contract_frozen",
        "bad_counters_zero",
    ]:
        if design_summary.get(key) is not True:
            failures.append(f"design_required_true_missing:{key}")

    for key in [
        "weak_feedback_resolved",
        "c5_opened",
        "live_feedback_audit_executed",
        "repair_applied",
        "retry_executed",
        "target_selected_for_build",
        "runtime_patch_applied",
        "source_mutated",
        "prior_receipt_mutated",
        "architecture_change",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if design_summary.get(key) is not False:
            failures.append(f"design_forbidden_true:{key}")

    if design_summary.get("authorized_next_unit") != EXPECTED_DESIGN_NEXT:
        failures.append("authorized_next_wrong")
    if design_summary.get("authorized_build_mode") != "STATIC_WEAK_FEEDBACK_HANDLING_ONLY":
        failures.append("authorized_build_mode_wrong")
    if design_summary.get("weak_feedback_count") != 3:
        failures.append("weak_feedback_count_wrong")
    if design_summary.get("under_typed_feedback_count") != 2:
        failures.append("under_typed_count_wrong")
    if design_summary.get("ambiguous_requires_question_count") != 1:
        failures.append("ambiguous_count_wrong")
    if design_summary.get("weak_records_inventoried_count") != 3:
        failures.append("inventory_count_wrong")
    if design_summary.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("c5_readiness_wrong")
    if target_definition.get("target_mode_for_build") != "STATIC_WEAK_FEEDBACK_HANDLING_ONLY":
        failures.append("target_definition_mode_wrong")
    if inventory.get("weak_feedback_count") != 3:
        failures.append("inventory_artifact_count_wrong")
    if inventory.get("resolution_performed") is not False:
        failures.append("inventory_resolution_performed")
    if set(policy_enum.get("handling_policy_enum", [])) != HANDLING_POLICIES:
        failures.append("handling_policy_enum_wrong")
    if build_auth.get("authorized_next_unit") != EXPECTED_DESIGN_NEXT:
        failures.append("build_auth_next_wrong")
    if build_auth.get("authorized_build_mode") != "STATIC_WEAK_FEEDBACK_HANDLING_ONLY":
        failures.append("build_auth_mode_wrong")
    if c5_contract.get("design_unit_does_not_unblock_c5") is not True:
        failures.append("c5_contract_design_unblock_wrong")
    if c5_contract.get("c5_opened") is not False:
        failures.append("c5_contract_opened")
    if authority.get("may_build_o2_weak_feedback_handling_next") is not True:
        failures.append("authority_does_not_allow_build")
    if authority.get("may_open_c5") is not False:
        failures.append("authority_allows_c5")
    if rollup.get("build_authorized_next_count") != 1:
        failures.append("rollup_build_authorized_wrong")
    if profile.get("authorized_next_unit") != EXPECTED_DESIGN_NEXT:
        failures.append("profile_next_wrong")
    if len(feedback_records) != 10:
        failures.append(f"feedback_records_count_wrong:{len(feedback_records)}")
    if len(retry_gates) != 10:
        failures.append(f"retry_gate_count_wrong:{len(retry_gates)}")
    if weak_note.get("weak_feedback_count") != 3:
        failures.append("weak_note_count_wrong")
    if c5_block.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("c5_block_not_blocked")

    inventory_records = inventory.get("records", [])
    if len(inventory_records) != 3:
        failures.append(f"inventory_records_count_wrong:{len(inventory_records)}")
    for rec in inventory_records:
        if rec.get("resolution_status") != "UNRESOLVED":
            failures.append(f"inventory_record_resolved:{rec.get('source_feedback_ref')}")
        if rec.get("handling_status") != "TARGET_DESIGN_ONLY":
            failures.append(f"inventory_record_handling_status_wrong:{rec.get('source_feedback_ref')}")

    feedback_by_id = {x.get("feedback_id"): x for x in feedback_records}
    return failures, {
        "design_summary": design_summary,
        "inventory_records": inventory_records,
        "feedback_by_id": feedback_by_id,
    }

def choose_primary_policy(inv: Dict[str, Any]) -> str:
    q = inv.get("feedback_quality_class")
    candidates = inv.get("handling_candidates", [])
    if q == "AMBIGUOUS_REQUIRES_QUESTION":
        return "QUESTION_PACKET_REQUIRED"
    if "SOURCE_REF_REQUEST_REQUIRED" in candidates:
        return "SOURCE_REF_REQUEST_REQUIRED"
    if "QUESTION_PACKET_REQUIRED" in candidates:
        return "QUESTION_PACKET_REQUIRED"
    return "PARK_WITH_REASON"

def build_question_packet(inv: Dict[str, Any], policy: str) -> Dict[str, Any]:
    missing_fields = []
    if not inv.get("failed_relative_to_boundary"):
        missing_fields.append("failed_relative_to_boundary")
    if inv.get("feedback_quality_class") == "AMBIGUOUS_REQUIRES_QUESTION":
        missing_fields.append("ambiguous_label_or_classification_discriminator")
    if inv.get("feedback_quality_class") == "UNDER_TYPED_FEEDBACK":
        missing_fields.append("typed_source_evidence")

    if not missing_fields:
        missing_fields = ["confirm_handling_path"]

    return {
        "schema_version": "o2_weak_feedback_question_packet_v0",
        "question_packet_id": "weak_question_" + sha8({"source": inv.get("source_feedback_ref"), "policy": policy}),
        "source_feedback_ref": inv.get("source_feedback_ref"),
        "question_kind": "AMBIGUOUS_LABEL" if inv.get("feedback_quality_class") == "AMBIGUOUS_REQUIRES_QUESTION" else "UNKNOWN_UNDER_TYPED",
        "question_text": (
            "What typed evidence, discriminator, or authority boundary is required before this weak feedback can be resolved or explicitly accepted?"
        ),
        "missing_fields": missing_fields,
        "acceptable_answer_types": [
            "explicit_source_ref",
            "explicit_boundary_ref",
            "explicit_discriminator",
            "explicit_under_typed_acceptance_decision",
            "park_with_reason",
        ],
        "blocked_until_answered": True,
        "c5_block_preserved": True,
        "status": "PROPOSED_ONLY",
    }

def build_source_ref_request(inv: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "o2_weak_feedback_source_ref_request_v0",
        "source_ref_request_id": "weak_source_ref_request_" + sha8({"source": inv.get("source_feedback_ref")}),
        "source_feedback_ref": inv.get("source_feedback_ref"),
        "requested_source_surface": inv.get("source_surface_ref", "typed_source_surface_or_receipt_trace"),
        "requested_evidence_refs": [
            "source receipt or trace ref for " + str(inv.get("source_unit_id")),
            "boundary/refinement evidence for " + str(inv.get("where_failed")),
        ],
        "why_needed": "Weak feedback is under-typed and cannot be resolved without explicit source evidence.",
        "status": "REQUEST_CANDIDATE_ONLY",
    }

def build_under_typed_acceptance_candidate(inv: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "o2_under_typed_acceptance_candidate_v0",
        "acceptance_candidate_id": "under_typed_acceptance_" + sha8({"source": inv.get("source_feedback_ref")}),
        "source_feedback_ref": inv.get("source_feedback_ref"),
        "acceptance_scope": "C5_BLOCKING",
        "acceptance_reason": "Record has enough typed diagnostic shape to be parked or accepted as under-typed material, but not enough to unblock C5.",
        "human_or_validator_review_required": True,
        "c5_unblock_allowed": False,
        "status": "CANDIDATE_ONLY",
    }

def build_parking_record(inv: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "o2_weak_feedback_parking_record_v0",
        "parking_id": "weak_parking_" + sha8({"source": inv.get("source_feedback_ref")}),
        "source_feedback_ref": inv.get("source_feedback_ref"),
        "park_reason": "Weak feedback remains unresolved after static handling; preserve it without counting as solved.",
        "blocked_moves": [
            "open C5",
            "count weak feedback as resolved",
            "retry same failure",
            "repair without explicit evidence",
        ],
        "lawful_reopen_conditions": [
            "question packet answered",
            "source-ref request satisfied",
            "under-typed acceptance explicitly reviewed",
            "later live audit target designed with explicit source refs",
        ],
        "status": "PARKED_WITH_REASON",
    }

def build_c5_block_record(inv: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "o2_weak_feedback_c5_block_record_v0",
        "c5_block_record_id": "weak_c5_block_" + sha8({"source": inv.get("source_feedback_ref")}),
        "source_feedback_ref": inv.get("source_feedback_ref"),
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_opened": False,
        "block_reason": "Weak feedback handling emitted candidate/question/parking records but did not resolve or accept the weak record.",
        "unblock_requires_reviewed_resolution_or_acceptance": True,
    }

def build_handling_record(inv: Dict[str, Any], primary_policy: str, question_packet: Dict[str, Any] | None, source_ref_request: Dict[str, Any] | None, acceptance_candidate: Dict[str, Any] | None, parking_record: Dict[str, Any], c5_block_record: Dict[str, Any]) -> Dict[str, Any]:
    outputs = {
        "question_packet_ref": question_packet.get("question_packet_id") if question_packet else None,
        "source_ref_request_ref": source_ref_request.get("source_ref_request_id") if source_ref_request else None,
        "under_typed_acceptance_candidate_ref": acceptance_candidate.get("acceptance_candidate_id") if acceptance_candidate else None,
        "parking_record_ref": parking_record.get("parking_id"),
        "c5_block_record_ref": c5_block_record.get("c5_block_record_id"),
    }
    return {
        "schema_version": "o2_weak_feedback_handling_record_v0",
        "handling_record_id": "weak_handling_" + sha8({"source": inv.get("source_feedback_ref"), "policy": primary_policy, "outputs": outputs}),
        "source_feedback_ref": inv.get("source_feedback_ref"),
        "source_unit_id": inv.get("source_unit_id"),
        "feedback_quality_class": inv.get("feedback_quality_class"),
        "primary_handling_policy": primary_policy,
        "handling_candidates_considered": inv.get("handling_candidates", []),
        "outputs": outputs,
        "resolution_status": "UNRESOLVED",
        "handling_status": "HANDLED_STATICALLY_NOT_RESOLVED",
        "c5_block_preserved": True,
        "must_not_infer": [
            "weak feedback resolved",
            "question packet answered",
            "source-ref request satisfied",
            "under-typed acceptance approved",
            "live audit complete",
            "repair applied",
            "retry authorized",
            "C5 opened",
        ],
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    design_summary = src.get("design_summary", {})
    inventory_records = src.get("inventory_records", [])
    feedback_by_id = src.get("feedback_by_id", {})

    handling_records: List[Dict[str, Any]] = []
    question_packets: List[Dict[str, Any]] = []
    source_ref_requests: List[Dict[str, Any]] = []
    undertyped_acceptance_candidates: List[Dict[str, Any]] = []
    parking_records: List[Dict[str, Any]] = []
    c5_block_records: List[Dict[str, Any]] = []

    for inv in inventory_records:
        primary_policy = choose_primary_policy(inv)

        question_packet = None
        source_ref_request = None
        acceptance_candidate = None

        if primary_policy == "QUESTION_PACKET_REQUIRED" or "QUESTION_PACKET_REQUIRED" in inv.get("handling_candidates", []):
            question_packet = build_question_packet(inv, primary_policy)
            question_packets.append(question_packet)

        if "SOURCE_REF_REQUEST_REQUIRED" in inv.get("handling_candidates", []):
            source_ref_request = build_source_ref_request(inv)
            source_ref_requests.append(source_ref_request)

        if "UNDER_TYPED_ACCEPTANCE_CANDIDATE" in inv.get("handling_candidates", []):
            acceptance_candidate = build_under_typed_acceptance_candidate(inv)
            undertyped_acceptance_candidates.append(acceptance_candidate)

        parking_record = build_parking_record(inv)
        c5_block_record = build_c5_block_record(inv)
        parking_records.append(parking_record)
        c5_block_records.append(c5_block_record)

        handling_records.append(
            build_handling_record(
                inv,
                primary_policy,
                question_packet,
                source_ref_request,
                acceptance_candidate,
                parking_record,
                c5_block_record,
            )
        )

    write_jsonl(HANDLING_RECORDS_PATH, handling_records)
    write_jsonl(QUESTION_PACKETS_PATH, question_packets)
    write_jsonl(SOURCE_REF_REQUESTS_PATH, source_ref_requests)
    write_jsonl(UNDERTYPED_ACCEPTANCE_CANDIDATES_PATH, undertyped_acceptance_candidates)
    write_jsonl(PARKING_RECORDS_PATH, parking_records)
    write_jsonl(C5_BLOCK_RECORDS_PATH, c5_block_records)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    policy_counts = Counter(x.get("primary_handling_policy") for x in handling_records)
    quality_counts = Counter(x.get("feedback_quality_class") for x in handling_records)

    # Required correctness checks.
    if len(handling_records) != 3:
        failures.append(f"handling_records_count_wrong:{len(handling_records)}")
    if len(question_packets) < 1:
        failures.append("no_question_packets_emitted")
    if len(source_ref_requests) < 2:
        failures.append(f"source_ref_requests_less_than_2:{len(source_ref_requests)}")
    if len(undertyped_acceptance_candidates) < 1:
        failures.append("no_under_typed_acceptance_candidates")
    if len(parking_records) != 3:
        failures.append(f"parking_records_count_wrong:{len(parking_records)}")
    if len(c5_block_records) != 3:
        failures.append(f"c5_block_records_count_wrong:{len(c5_block_records)}")

    for rec in handling_records:
        if rec.get("resolution_status") != "UNRESOLVED":
            failures.append(f"handling_resolved:{rec.get('source_feedback_ref')}")
        if rec.get("c5_block_preserved") is not True:
            failures.append(f"c5_block_not_preserved:{rec.get('source_feedback_ref')}")

    for qp in question_packets:
        if qp.get("status") != "PROPOSED_ONLY":
            failures.append(f"question_packet_not_proposed_only:{qp.get('question_packet_id')}")
        if qp.get("blocked_until_answered") is not True:
            failures.append(f"question_packet_not_blocking:{qp.get('question_packet_id')}")
        if qp.get("c5_block_preserved") is not True:
            failures.append(f"question_packet_c5_not_preserved:{qp.get('question_packet_id')}")

    for req in source_ref_requests:
        if req.get("status") != "REQUEST_CANDIDATE_ONLY":
            failures.append(f"source_ref_request_not_candidate_only:{req.get('source_ref_request_id')}")

    for cand in undertyped_acceptance_candidates:
        if cand.get("status") != "CANDIDATE_ONLY":
            failures.append(f"under_typed_acceptance_not_candidate:{cand.get('acceptance_candidate_id')}")
        if cand.get("c5_unblock_allowed") is not False:
            failures.append(f"under_typed_acceptance_unblocks_c5:{cand.get('acceptance_candidate_id')}")

    for parked in parking_records:
        if parked.get("status") != "PARKED_WITH_REASON":
            failures.append(f"parking_status_wrong:{parked.get('parking_id')}")

    for block in c5_block_records:
        if block.get("c5_opened") is not False:
            failures.append(f"c5_block_record_opened:{block.get('c5_block_record_id')}")
        if block.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
            failures.append(f"c5_block_record_wrong_readiness:{block.get('c5_block_record_id')}")

    status = "TYPED_O2_WEAK_FEEDBACK_HANDLING_STATIC_RECORDS_EMITTED_REVIEW_READY" if not failures else "TYPED_O2_WEAK_FEEDBACK_HANDLING_GATE_FAIL"
    recommended_next = "REVIEW_O2_WEAK_FEEDBACK_HANDLING_V0" if not failures else "REPAIR_O2_WEAK_FEEDBACK_HANDLING_V0"

    reason_codes = [
        "WEAK_FEEDBACK_HANDLING_STATIC_RECORDS_EMITTED",
        "WEAK_FEEDBACK_TARGET_DESIGN_RECEIPT_CONSUMED",
        "THREE_WEAK_FEEDBACK_RECORDS_HANDLED_STATICALLY",
        "QUESTION_PACKET_CANDIDATES_EMITTED",
        "SOURCE_REF_REQUEST_CANDIDATES_EMITTED",
        "UNDER_TYPED_ACCEPTANCE_CANDIDATES_EMITTED",
        "PARKED_WITH_REASON_RECORDS_EMITTED",
        "C5_BLOCK_RECORDS_EMITTED",
        "HANDLING_RECORDS_MARK_UNRESOLVED",
        "QUESTION_PACKETS_PROPOSED_ONLY",
        "SOURCE_REF_REQUESTS_CANDIDATE_ONLY",
        "UNDER_TYPED_ACCEPTANCE_CANDIDATES_ONLY",
        "C5_BLOCK_PRESERVED",
        "NO_WEAK_FEEDBACK_RESOLUTION_ATTEMPTED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_TARGET_SELECTED_FOR_BUILD",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
        "NO_C5_OPENED",
    ] if not failures else failures

    rollup = {
        "schema_version": "o2_weak_feedback_handling_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "weak_records_handled_count": len(handling_records),
        "weak_feedback_count": design_summary.get("weak_feedback_count"),
        "under_typed_feedback_count": design_summary.get("under_typed_feedback_count"),
        "ambiguous_requires_question_count": design_summary.get("ambiguous_requires_question_count"),
        "quality_counts": dict(sorted(quality_counts.items())),
        "primary_policy_counts": dict(sorted(policy_counts.items())),
        "question_packet_candidates_count": len(question_packets),
        "source_ref_request_candidates_count": len(source_ref_requests),
        "under_typed_acceptance_candidates_count": len(undertyped_acceptance_candidates),
        "parking_records_count": len(parking_records),
        "c5_block_records_count": len(c5_block_records),
        "weak_feedback_resolved_count": 0,
        "question_packets_answered_count": 0,
        "source_ref_requests_satisfied_count": 0,
        "under_typed_acceptance_approved_count": 0,
        "parked_records_counted_as_resolved_count": 0,
        "live_feedback_audit_executed_count": 0,
        "repair_applied_count": 0,
        "retry_executed_count": 0,
        "target_selected_for_build_count": 0,
        "runtime_patch_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "architecture_change_count": 0,
        "c5_opened_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    zero_keys = [
        "weak_feedback_resolved_count",
        "question_packets_answered_count",
        "source_ref_requests_satisfied_count",
        "under_typed_acceptance_approved_count",
        "parked_records_counted_as_resolved_count",
        "live_feedback_audit_executed_count",
        "repair_applied_count",
        "retry_executed_count",
        "target_selected_for_build_count",
        "runtime_patch_count",
        "source_mutated_count",
        "prior_receipt_mutated_count",
        "architecture_change_count",
        "c5_opened_count",
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    readout = {
        "schema_version": "o2_weak_feedback_handling_readout_v0",
        "weak_records_handled": len(handling_records),
        "question_packet_candidates": len(question_packets),
        "source_ref_request_candidates": len(source_ref_requests),
        "under_typed_acceptance_candidates": len(undertyped_acceptance_candidates),
        "parking_records": len(parking_records),
        "c5_block_records": len(c5_block_records),
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "interpretation": "The 3 weak records now have static handling records, but none are resolved. C5 remains blocked until a later reviewed unit answers/accepts/satisfies or explicitly parks them under an approved policy.",
    }

    profile = {
        "schema_version": "o2_weak_feedback_handling_profile_v0",
        "profile_id": "o2_weak_feedback_handling_profile_" + sha8(rollup),
        "status": status,
        "weak_records_handled": len(handling_records),
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Review weak-feedback handling records next; do not treat handling records as resolution.",
        "must_not_infer": [
            "weak feedback resolved",
            "question packet answered",
            "source-ref request satisfied",
            "under-typed acceptance approved",
            "live audit complete",
            "C5 opened",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_weak_feedback_handling_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The O2 weak-feedback handling unit emitted static handling records for the 3 weak records. It emitted question packet candidates, source-ref request candidates, under-typed acceptance candidates, parked-with-reason records, and C5 block records. It did not resolve weak feedback, answer question packets, satisfy source-ref requests, approve under-typed acceptance, run live audit, repair, retry, select target, patch runtime, mutate sources, or open C5.",
        "weak_records_handled": len(handling_records),
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_weak_feedback_handling_transition_trace_v0",
        "trace": [
            {
                "step": "consume_weak_feedback_target_design",
                "question": "is static weak-feedback handling authorized",
                "answer": "yes",
                "taken": "emit handling records",
            },
            {
                "step": "handle_three_weak_records",
                "question": "were the 3 weak records given handling outputs",
                "answer": "yes",
                "taken": "emit question/source-ref/acceptance/parking/C5 block records",
            },
            {
                "step": "preserve_block",
                "question": "did handling resolve weak feedback or unblock C5",
                "answer": "no",
                "taken": "preserve unresolved status and C5 block",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    write_json(HANDLING_ROLLUP_PATH, rollup)
    write_json(HANDLING_READOUT_PATH, readout)
    write_json(HANDLING_PROFILE_PATH, profile)
    write_json(HANDLING_REPORT_PATH, report)
    write_json(HANDLING_TRACE_PATH, trace)

    acceptance_gate_results = {
        "WFH_BUILD_0_TARGET_DESIGN_RECEIPT_CONSUMED": WFH_DESIGN_RECEIPT_PATH.exists(),
        "WFH_BUILD_1_THREE_WEAK_RECORDS_HANDLED": len(handling_records) == 3,
        "WFH_BUILD_2_QUESTION_PACKET_CANDIDATES_EMITTED": len(question_packets) >= 1,
        "WFH_BUILD_3_SOURCE_REF_REQUEST_CANDIDATES_EMITTED": len(source_ref_requests) >= 2,
        "WFH_BUILD_4_UNDER_TYPED_ACCEPTANCE_CANDIDATES_EMITTED": len(undertyped_acceptance_candidates) >= 1,
        "WFH_BUILD_5_PARKING_RECORDS_EMITTED": len(parking_records) == 3,
        "WFH_BUILD_6_C5_BLOCK_RECORDS_EMITTED": len(c5_block_records) == 3,
        "WFH_BUILD_7_HANDLING_RECORDS_UNRESOLVED": all(x.get("resolution_status") == "UNRESOLVED" for x in handling_records),
        "WFH_BUILD_8_QUESTION_PACKETS_PROPOSED_ONLY": all(x.get("status") == "PROPOSED_ONLY" for x in question_packets),
        "WFH_BUILD_9_SOURCE_REF_REQUESTS_CANDIDATE_ONLY": all(x.get("status") == "REQUEST_CANDIDATE_ONLY" for x in source_ref_requests),
        "WFH_BUILD_10_UNDER_TYPED_ACCEPTANCE_CANDIDATE_ONLY": all(x.get("status") == "CANDIDATE_ONLY" for x in undertyped_acceptance_candidates),
        "WFH_BUILD_11_PARKING_NOT_RESOLUTION": rollup["parked_records_counted_as_resolved_count"] == 0,
        "WFH_BUILD_12_C5_BLOCK_PRESERVED": rollup["c5_opened_count"] == 0 and all(x.get("c5_feedback_readiness") == "BLOCKED_BY_WEAK_FEEDBACK" for x in c5_block_records),
        "WFH_BUILD_13_NO_WEAK_FEEDBACK_RESOLUTION": rollup["weak_feedback_resolved_count"] == 0,
        "WFH_BUILD_14_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "WFH_BUILD_15_NO_REPAIR_RETRY_TARGET_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["target_selected_for_build_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "WFH_BUILD_16_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "WFH_BUILD_17_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "WFH_BUILD_18_NO_HIDDEN_NEXT_COMMAND": profile["next_command_goal"] is None,
        "WFH_BUILD_19_ROLLUP_READOUT_PROFILE_REPORT_TRACE_EMITTED": HANDLING_ROLLUP_PATH.exists() and HANDLING_READOUT_PATH.exists() and HANDLING_PROFILE_PATH.exists() and HANDLING_REPORT_PATH.exists() and HANDLING_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_HANDLING_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "weak_records": len(handling_records),
        "question_packets": len(question_packets),
        "source_ref_requests": len(source_ref_requests),
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_handling_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_HANDLING_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_weak_feedback_target_design_receipt_id": WFH_DESIGN_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_handling_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "weak_feedback_handling_built": gate == "PASS",
            "weak_records_handled_count": len(handling_records),
            "weak_feedback_count": design_summary.get("weak_feedback_count"),
            "under_typed_feedback_count": design_summary.get("under_typed_feedback_count"),
            "ambiguous_requires_question_count": design_summary.get("ambiguous_requires_question_count"),
            "question_packet_candidates_emitted": len(question_packets),
            "source_ref_request_candidates_emitted": len(source_ref_requests),
            "under_typed_acceptance_candidates_emitted": len(undertyped_acceptance_candidates),
            "parking_records_emitted": len(parking_records),
            "c5_block_records_emitted": len(c5_block_records),
            "weak_feedback_resolved": False,
            "question_packets_answered": False,
            "source_ref_requests_satisfied": False,
            "under_typed_acceptance_approved": False,
            "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
            "c5_opened": False,
            "live_feedback_audit_executed": False,
            "repair_applied": False,
            "retry_executed": False,
            "target_selected_for_build": False,
            "runtime_patch_applied": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "architecture_change": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": profile["bad_counters_zero"],
            "recommended_next": recommended_next,
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "handling_records": rel(HANDLING_RECORDS_PATH),
            "question_packets": rel(QUESTION_PACKETS_PATH),
            "source_ref_requests": rel(SOURCE_REF_REQUESTS_PATH),
            "under_typed_acceptance_candidates": rel(UNDERTYPED_ACCEPTANCE_CANDIDATES_PATH),
            "parking_records": rel(PARKING_RECORDS_PATH),
            "c5_block_records": rel(C5_BLOCK_RECORDS_PATH),
            "rollup": rel(HANDLING_ROLLUP_PATH),
            "readout": rel(HANDLING_READOUT_PATH),
            "profile": rel(HANDLING_PROFILE_PATH),
            "report": rel(HANDLING_REPORT_PATH),
            "transition_trace": rel(HANDLING_TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"weak_feedback_handling_receipt_id={receipt_id}")
    print(f"weak_feedback_handling_receipt_path={rel(receipt_path)}")
    print(f"weak_feedback_handling_records_path={rel(HANDLING_RECORDS_PATH)}")
    print(f"weak_feedback_question_packets_path={rel(QUESTION_PACKETS_PATH)}")
    print(f"weak_feedback_source_ref_requests_path={rel(SOURCE_REF_REQUESTS_PATH)}")
    print(f"under_typed_acceptance_candidates_path={rel(UNDERTYPED_ACCEPTANCE_CANDIDATES_PATH)}")
    print(f"weak_feedback_parking_records_path={rel(PARKING_RECORDS_PATH)}")
    print(f"weak_feedback_c5_block_records_path={rel(C5_BLOCK_RECORDS_PATH)}")
    print(f"weak_feedback_handling_rollup_path={rel(HANDLING_ROLLUP_PATH)}")
    print(f"weak_feedback_handling_profile_path={rel(HANDLING_PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
