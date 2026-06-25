#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_C5_TO_C6_INTER_CELL_PROTOCOL_EXAMPLES_FROM_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "c6.inter_cell_protocol_examples_from_c5_reference_review.v0"
LAYER = "BRIDGE / C5_TO_C6 / EXAMPLE_EXTRACTION_REVIEW"
MODE = "REVIEW_ONLY / VERIFY_EXAMPLES / NO_C6_OPENING / NO_C6_PROTOCOL_DESIGN"
BUILD_MODE = "C5_TO_C6_EXAMPLE_REVIEW_ONLY"

SOURCE_C6_EXTRACT_RECEIPT_ID = "c486e477"
SOURCE_POST_C5_DECISION_RECEIPT_ID = "23cb11ed"
SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_ID = "934363ba"

SOURCE_C6_EXTRACT_RECEIPT_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0_receipts/c486e477.json"

EXTRACTION_BASIS_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_example_extraction_basis_v0.json"
EXAMPLE_SCHEMA_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_inter_cell_protocol_example_schema_v0.json"
EXAMPLES_JSONL_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_inter_cell_protocol_examples_from_c5_v0.jsonl"
EXAMPLE_CATALOG_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_inter_cell_protocol_example_catalog_v0.json"
PROPOSAL_EXAMPLES_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_proposal_packet_examples_from_c5_v0.json"
ACCEPTED_PACKET_EXAMPLES_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_accepted_review_packet_examples_from_c5_v0.json"
CELL1_PROBE_EXAMPLES_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_cell1_probe_examples_from_c5_v0.json"
VERIFICATION_EXAMPLES_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_verification_examples_from_c5_v0.json"
HANDOFF_EXAMPLES_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_handoff_examples_from_c5_v0.json"
BLOCKED_FEEDBACK_EXAMPLES_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_blocked_feedback_examples_from_c5_v0.json"
EDGE_EXAMPLES_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_edge_observation_examples_from_c5_v0.json"
PROTOCOL_PRESSURE_READOUT_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_protocol_pressure_readout_from_c5_examples_v0.json"
REVIEW_CANDIDATE_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_example_extraction_review_candidate_v0.json"
EXTRACT_AUTHORITY_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_example_extraction_authority_boundary_v0.json"
EXTRACT_CLASSIFICATION_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_example_extraction_classification_v0.json"
EXTRACT_ROLLUP_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_example_extraction_rollup_v0.json"
EXTRACT_PROFILE_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_example_extraction_profile_v0.json"
EXTRACT_REPORT_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_example_extraction_report.json"
EXTRACT_TRACE_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_example_extraction_transition_trace.json"

SOURCE_POST_C5_DECISION_RECEIPT_PATH = ROOT / "data/c5_post_domain_shift_reference_decision_v0_receipts/23cb11ed.json"
SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0_receipts/934363ba.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C6_EXTRACT_RECEIPT_PATH,
    EXTRACTION_BASIS_PATH,
    EXAMPLE_SCHEMA_PATH,
    EXAMPLES_JSONL_PATH,
    EXAMPLE_CATALOG_PATH,
    PROPOSAL_EXAMPLES_PATH,
    ACCEPTED_PACKET_EXAMPLES_PATH,
    CELL1_PROBE_EXAMPLES_PATH,
    VERIFICATION_EXAMPLES_PATH,
    HANDOFF_EXAMPLES_PATH,
    BLOCKED_FEEDBACK_EXAMPLES_PATH,
    EDGE_EXAMPLES_PATH,
    PROTOCOL_PRESSURE_READOUT_PATH,
    REVIEW_CANDIDATE_PATH,
    EXTRACT_AUTHORITY_PATH,
    EXTRACT_CLASSIFICATION_PATH,
    EXTRACT_ROLLUP_PATH,
    EXTRACT_PROFILE_PATH,
    EXTRACT_REPORT_PATH,
    EXTRACT_TRACE_PATH,
    SOURCE_POST_C5_DECISION_RECEIPT_PATH,
    SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_PATH,
]

OUT_DIR = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0"
RECEIPT_DIR = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0_receipts"

REVIEW_BASIS_PATH = OUT_DIR / "c6_example_extraction_review_basis_v0.json"
SCHEMA_REVIEW_PATH = OUT_DIR / "c6_inter_cell_protocol_example_schema_review_v0.json"
CATALOG_REVIEW_PATH = OUT_DIR / "c6_inter_cell_protocol_example_catalog_review_v0.json"
EXAMPLE_SURFACE_REVIEW_PATH = OUT_DIR / "c6_inter_cell_protocol_example_surface_review_v0.json"
PROPOSAL_REVIEW_PATH = OUT_DIR / "c6_proposal_packet_example_review_v0.json"
ACCEPTED_PACKET_REVIEW_PATH = OUT_DIR / "c6_accepted_packet_example_review_v0.json"
CELL1_PROBE_REVIEW_PATH = OUT_DIR / "c6_cell1_probe_example_review_v0.json"
VERIFICATION_REVIEW_PATH = OUT_DIR / "c6_verification_example_review_v0.json"
HANDOFF_REVIEW_PATH = OUT_DIR / "c6_handoff_example_review_v0.json"
BLOCKED_FEEDBACK_REVIEW_PATH = OUT_DIR / "c6_blocked_feedback_example_review_v0.json"
EDGE_REVIEW_PATH = OUT_DIR / "c6_edge_observation_example_review_v0.json"
PROTOCOL_PRESSURE_REVIEW_PATH = OUT_DIR / "c6_protocol_pressure_readout_review_v0.json"
CLOSE_CANDIDATE_PATH = OUT_DIR / "c6_example_extraction_reviewed_reference_close_candidate_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "c6_example_extraction_review_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "c6_example_extraction_review_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "c6_example_extraction_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c6_example_extraction_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "c6_example_extraction_review_report.json"
TRACE_PATH = OUT_DIR / "c6_example_extraction_review_transition_trace.json"

EXPECTED_EXTRACT_STATUS = "TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_REVIEW_READY"
EXPECTED_EXTRACT_NEXT = "REVIEW_C5_TO_C6_INTER_CELL_PROTOCOL_EXAMPLES_FROM_REVIEWED_REFERENCE_V0"
RECOMMENDED_NEXT = "CLOSE_C5_TO_C6_INTER_CELL_PROTOCOL_EXAMPLES_FROM_REVIEWED_REFERENCE_AS_REVIEWED_REFERENCE_V0"

EXPECTED_TYPES = {
    "PROPOSAL_PACKET_PROPOSED_ONLY",
    "ACCEPTED_PROPOSAL_PACKET",
    "CELL1_ACCEPTED_PROPOSAL_CONSUMPTION",
    "VERIFICATION_RETURN",
    "HANDOFF_RETURN_TO_CELL0",
    "BLOCKED_OR_TYPED_STOP_FEEDBACK",
    "DECISION_EDGE_OBSERVATION",
}

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

def count_type(examples: List[Dict[str, Any]], typ: str) -> int:
    return sum(1 for x in examples if x.get("example_type") == typ)

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{rel(path)}")
    if failures:
        return failures, {}

    extract_receipt = read_json(SOURCE_C6_EXTRACT_RECEIPT_PATH)
    extract_summary = extract_receipt.get("machine_readable_c6_example_extraction_summary", {})
    examples = read_jsonl(EXAMPLES_JSONL_PATH)
    catalog = read_json(EXAMPLE_CATALOG_PATH)
    schema = read_json(EXAMPLE_SCHEMA_PATH)
    proposal_examples = read_json(PROPOSAL_EXAMPLES_PATH)
    accepted_examples = read_json(ACCEPTED_PACKET_EXAMPLES_PATH)
    cell1_examples = read_json(CELL1_PROBE_EXAMPLES_PATH)
    verification_examples = read_json(VERIFICATION_EXAMPLES_PATH)
    handoff_examples = read_json(HANDOFF_EXAMPLES_PATH)
    blocked_feedback_examples = read_json(BLOCKED_FEEDBACK_EXAMPLES_PATH)
    edge_examples = read_json(EDGE_EXAMPLES_PATH)
    pressure = read_json(PROTOCOL_PRESSURE_READOUT_PATH)
    candidate = read_json(REVIEW_CANDIDATE_PATH)
    authority = read_json(EXTRACT_AUTHORITY_PATH)
    classification = read_json(EXTRACT_CLASSIFICATION_PATH)
    rollup = read_json(EXTRACT_ROLLUP_PATH)
    profile = read_json(EXTRACT_PROFILE_PATH)
    report = read_json(EXTRACT_REPORT_PATH)
    trace = read_json(EXTRACT_TRACE_PATH)
    post_c5_decision = read_json(SOURCE_POST_C5_DECISION_RECEIPT_PATH)
    c5_reference_closure = read_json(SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_PATH)

    if extract_receipt.get("receipt_id") != SOURCE_C6_EXTRACT_RECEIPT_ID or extract_receipt.get("gate") != "PASS":
        failures.append("extract_receipt_not_pass")
    if extract_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("extract_receipt_hidden_next")
    if extract_summary.get("status") != EXPECTED_EXTRACT_STATUS:
        failures.append(f"extract_status_wrong:{extract_summary.get('status')}")
    if extract_summary.get("recommended_next") != EXPECTED_EXTRACT_NEXT:
        failures.append(f"extract_next_wrong:{extract_summary.get('recommended_next')}")
    for key in ["c6_example_extraction_complete", "c6_example_extraction_review_ready", "bad_counters_zero"]:
        if extract_summary.get(key) is not True:
            failures.append(f"extract_summary_required_true_missing:{key}")

    expected_counts = {
        "examples_extracted": 12,
        "proposal_packet_examples_extracted": 2,
        "accepted_packet_examples_extracted": 1,
        "cell1_probe_examples_extracted": 1,
        "verification_examples_extracted": 5,
        "handoff_examples_extracted": 1,
        "blocked_feedback_examples_extracted": 2,
        "edge_examples_extracted": 5,
    }
    for key, expected in expected_counts.items():
        if extract_summary.get(key) != expected:
            failures.append(f"extract_count_wrong:{key}:{extract_summary.get(key)}")

    for key in [
        "c6_opened",
        "c6_design_executed",
        "c6_protocol_emitted",
        "new_domain_shift_executed",
        "source_mutated",
        "prior_receipt_mutated",
        "c5_reference_mutated",
        "full_transfer_claimed",
        "global_autonomy_claimed",
        "general_cell1_authority_claimed",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if extract_summary.get(key) is not False:
            failures.append(f"extract_forbidden_true:{key}")

    if len(examples) != 12:
        failures.append(f"examples_jsonl_count_wrong:{len(examples)}")
    actual_types = {x.get("example_type") for x in examples}
    missing_types = sorted(EXPECTED_TYPES - actual_types)
    if missing_types:
        failures.append("missing_example_types:" + ",".join(missing_types))

    if count_type(examples, "PROPOSAL_PACKET_PROPOSED_ONLY") != 1:
        failures.append("proposed_only_example_count_wrong")
    if count_type(examples, "ACCEPTED_PROPOSAL_PACKET") != 1:
        failures.append("accepted_proposal_example_count_wrong")
    if count_type(examples, "CELL1_ACCEPTED_PROPOSAL_CONSUMPTION") != 1:
        failures.append("cell1_consumption_example_count_wrong")
    if count_type(examples, "VERIFICATION_RETURN") != 1:
        failures.append("verification_return_example_count_wrong")
    if count_type(examples, "HANDOFF_RETURN_TO_CELL0") != 1:
        failures.append("handoff_return_example_count_wrong")
    if count_type(examples, "BLOCKED_OR_TYPED_STOP_FEEDBACK") != 2:
        failures.append("blocked_feedback_example_count_wrong")
    if count_type(examples, "DECISION_EDGE_OBSERVATION") != 5:
        failures.append("edge_example_count_wrong")

    for ex in examples:
        forbidden = ex.get("forbidden_c6_use", [])
        for required in ["open C6 automatically", "treat example as full protocol", "claim full transfer", "grant general Cell 1 authority", "auto-chain builds"]:
            if required not in forbidden:
                failures.append(f"example_missing_forbidden_use:{ex.get('example_id')}:{required}")

    if catalog.get("example_count") != 12:
        failures.append("catalog_count_wrong")
    if set(catalog.get("example_types", [])) != actual_types:
        failures.append("catalog_type_set_wrong")
    if set(schema.get("closed_example_types", [])) != actual_types:
        failures.append("schema_closed_type_set_wrong")

    if len(proposal_examples.get("proposed_only_examples", [])) != 1:
        failures.append("proposal_proposed_only_count_wrong")
    if len(proposal_examples.get("accepted_examples", [])) != 1:
        failures.append("proposal_accepted_count_wrong")
    if proposal_examples.get("distinction") != "PROPOSED_ONLY != ACCEPTED":
        failures.append("proposal_distinction_wrong")

    if accepted_examples.get("accepted_count") != 1:
        failures.append("accepted_count_wrong")
    if cell1_examples.get("build_count") != 1:
        failures.append("cell1_build_count_wrong")
    for build in cell1_examples.get("builds", []):
        if build.get("freebuild_count") != 0 or build.get("auto_chain_count") != 0 or build.get("scope_expansion_count") != 0:
            failures.append("cell1_build_bad_counter_nonzero")

    if verification_examples.get("verification_count") != 5:
        failures.append("verification_count_wrong")
    if handoff_examples.get("handoff_count") != 1:
        failures.append("handoff_count_wrong")
    if blocked_feedback_examples.get("feedback_count") != 2:
        failures.append("blocked_feedback_count_wrong")
    for fb in blocked_feedback_examples.get("feedback_records", []):
        if fb.get("feedback_quality") != "DIAGNOSTIC_USEFUL" or fb.get("bare_failed_status") is not False:
            failures.append("blocked_feedback_not_diagnostic")

    if edge_examples.get("selected_edge_example_count") != 5:
        failures.append("edge_selected_count_wrong")
    if pressure.get("not_a_c6_protocol_design") is not True:
        failures.append("pressure_readout_claims_protocol_design")
    if not pressure.get("fields_c6_likely_needs"):
        failures.append("pressure_fields_missing")
    if candidate.get("candidate_status") != "C6_EXAMPLE_EXTRACTION_REVIEW_READY":
        failures.append("review_candidate_not_ready")
    if authority.get("may_review_examples_next") is not True:
        failures.append("authority_no_review_next")
    for forbidden in [
        "may_open_c6_now",
        "may_design_c6_protocol_now",
        "may_execute_c6_protocol_now",
        "may_execute_new_domain_shift",
        "may_mutate_c5_reference",
        "may_mutate_source",
        "may_mutate_prior_receipts",
        "may_claim_transfer",
        "may_claim_global_autonomy",
        "may_grant_general_cell1_authority",
    ]:
        if authority.get(forbidden) is not False:
            failures.append(f"authority_forbidden_true:{forbidden}")
    if classification.get("c6_example_extraction_review_ready") is not True:
        failures.append("classification_review_not_ready")
    if classification.get("next_command_goal") is not None:
        failures.append("classification_hidden_next")
    for key, value in rollup.items():
        if key.endswith("_count") and key in {
            "c6_opened_count",
            "c6_design_executed_count",
            "c6_protocol_emitted_count",
            "new_domain_shift_executed_count",
            "source_mutated_count",
            "prior_receipt_mutated_count",
            "c5_reference_mutated_count",
            "full_transfer_claim_count",
            "global_autonomy_claim_count",
            "general_cell1_authority_claim_count",
            "hidden_next_command_count",
            "latest_file_guessing_count",
            "mtime_selection_count",
        } and value != 0:
            failures.append(f"rollup_forbidden_count_nonzero:{key}:{value}")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if profile.get("c6_opened") is not False or profile.get("c6_design_executed") is not False or profile.get("c6_protocol_emitted") is not False:
        failures.append("profile_c6_boundary_wrong")
    if report.get("recommended_next_handling") != EXPECTED_EXTRACT_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_hidden_next")
    if post_c5_decision.get("receipt_id") != SOURCE_POST_C5_DECISION_RECEIPT_ID or post_c5_decision.get("gate") != "PASS":
        failures.append("post_c5_decision_receipt_wrong")
    if c5_reference_closure.get("receipt_id") != SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_ID or c5_reference_closure.get("gate") != "PASS":
        failures.append("c5_reference_closure_receipt_wrong")

    return failures, {
        "summary": extract_summary,
        "examples": examples,
        "actual_types": sorted(actual_types),
        "catalog": catalog,
        "pressure": pressure,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    review_pass = not failures
    status = "TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_REVIEWED_CLOSE_READY" if review_pass else "TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_REVIEW_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if review_pass else "REPAIR_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_REVIEW_V0"

    summary = basis.get("summary", {})
    examples = basis.get("examples", [])
    actual_types = basis.get("actual_types", [])
    pressure = basis.get("pressure", {})

    reason_codes = [
        "C6_EXAMPLE_EXTRACTION_REVIEW_COMPLETE",
        "C6_EXAMPLE_EXTRACTION_RECEIPT_CONSUMED",
        "C5_REVIEWED_REFERENCE_SOURCE_CONFIRMED",
        "EXAMPLE_SCHEMA_REVIEWED",
        "EXAMPLE_CATALOG_REVIEWED",
        "PROPOSED_ONLY_PACKET_EXAMPLE_REVIEWED",
        "ACCEPTED_PROPOSAL_PACKET_EXAMPLE_REVIEWED",
        "CELL1_BOUNDED_PROBE_EXAMPLE_REVIEWED",
        "VERIFICATION_RETURN_EXAMPLE_REVIEWED",
        "HANDOFF_RETURN_EXAMPLE_REVIEWED",
        "DIAGNOSTIC_BLOCKED_FEEDBACK_EXAMPLES_REVIEWED",
        "DECISION_EDGE_EXAMPLES_REVIEWED",
        "PROTOCOL_PRESSURE_READOUT_REVIEWED_AS_NON_PROTOCOL_DESIGN",
        "CLOSE_CANDIDATE_READY",
        "NO_C6_OPENING",
        "NO_C6_PROTOCOL_DESIGN",
        "NO_C6_PROTOCOL_EMISSION",
        "NO_TRANSFER_CLAIM",
        "NO_GLOBAL_AUTONOMY_CLAIM",
        "NO_GENERAL_CELL1_AUTHORITY_CLAIM",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if review_pass else failures

    review_basis = {
        "schema_version": "c6_example_extraction_review_basis_v0",
        "review_status": status,
        "source_c6_example_extraction_receipt_id": SOURCE_C6_EXTRACT_RECEIPT_ID,
        "source_post_c5_decision_receipt_id": SOURCE_POST_C5_DECISION_RECEIPT_ID,
        "source_c5_reference_closure_receipt_id": SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_ID,
        "review_pass": review_pass,
        "examples_extracted": len(examples),
        "example_types": actual_types,
    }

    schema_review = {
        "schema_version": "c6_inter_cell_protocol_example_schema_review_v0",
        "review_status": "PASS" if review_pass else "FAIL",
        "schema_present": EXAMPLE_SCHEMA_PATH.exists(),
        "closed_example_types_reviewed": actual_types,
        "schema_is_example_schema_not_protocol_schema": True,
    }

    catalog_review = {
        "schema_version": "c6_inter_cell_protocol_example_catalog_review_v0",
        "review_status": "PASS" if review_pass else "FAIL",
        "example_count": len(examples),
        "example_types": actual_types,
        "catalog_complete": review_pass,
    }

    example_surface_review = {
        "schema_version": "c6_inter_cell_protocol_example_surface_review_v0",
        "review_status": "PASS" if review_pass else "FAIL",
        "examples_reviewed_count": len(examples),
        "required_surfaces_present": {
            "proposed_only_packet": "PROPOSAL_PACKET_PROPOSED_ONLY" in actual_types,
            "accepted_packet": "ACCEPTED_PROPOSAL_PACKET" in actual_types,
            "cell1_consumption": "CELL1_ACCEPTED_PROPOSAL_CONSUMPTION" in actual_types,
            "verification_return": "VERIFICATION_RETURN" in actual_types,
            "handoff_return": "HANDOFF_RETURN_TO_CELL0" in actual_types,
            "blocked_feedback": "BLOCKED_OR_TYPED_STOP_FEEDBACK" in actual_types,
            "decision_edge_observation": "DECISION_EDGE_OBSERVATION" in actual_types,
        },
    }

    proposal_review = {
        "schema_version": "c6_proposal_packet_example_review_v0",
        "review_status": "PASS" if review_pass else "FAIL",
        "proposed_only_examples": summary.get("proposal_packet_examples_extracted"),
        "accepted_examples": summary.get("accepted_packet_examples_extracted"),
        "distinction_preserved": "PROPOSED_ONLY != ACCEPTED",
        "proposal_packet_not_command": True,
    }

    accepted_packet_review = {
        "schema_version": "c6_accepted_packet_example_review_v0",
        "review_status": "PASS" if review_pass else "FAIL",
        "accepted_packet_examples": summary.get("accepted_packet_examples_extracted"),
        "review_acceptance_boundary_preserved": True,
        "cell1_consumption_allowed_only_after_acceptance": True,
    }

    cell1_probe_review = {
        "schema_version": "c6_cell1_probe_example_review_v0",
        "review_status": "PASS" if review_pass else "FAIL",
        "cell1_probe_examples": summary.get("cell1_probe_examples_extracted"),
        "freebuild_count": 0,
        "auto_chain_count": 0,
        "scope_expansion_count": 0,
    }

    verification_review = {
        "schema_version": "c6_verification_example_review_v0",
        "review_status": "PASS" if review_pass else "FAIL",
        "verification_examples": summary.get("verification_examples_extracted"),
        "verification_not_global_truth": True,
    }

    handoff_review = {
        "schema_version": "c6_handoff_example_review_v0",
        "review_status": "PASS" if review_pass else "FAIL",
        "handoff_examples": summary.get("handoff_examples_extracted"),
        "handoff_return_not_auto_chain": True,
    }

    blocked_feedback_review = {
        "schema_version": "c6_blocked_feedback_example_review_v0",
        "review_status": "PASS" if review_pass else "FAIL",
        "blocked_feedback_examples": summary.get("blocked_feedback_examples_extracted"),
        "feedback_diagnostic": True,
        "bare_failed_status_count": 0,
    }

    edge_review = {
        "schema_version": "c6_edge_observation_example_review_v0",
        "review_status": "PASS" if review_pass else "FAIL",
        "edge_examples": summary.get("edge_examples_extracted"),
        "edge_examples_preserve_inter_cell_transition_visibility": True,
    }

    pressure_review = {
        "schema_version": "c6_protocol_pressure_readout_review_v0",
        "review_status": "PASS" if review_pass else "FAIL",
        "pressure_readout_present": bool(pressure),
        "not_a_c6_protocol_design": pressure.get("not_a_c6_protocol_design") is True,
        "fields_c6_likely_needs_count": len(pressure.get("fields_c6_likely_needs", [])),
        "open_questions_count": len(pressure.get("open_questions_for_later_c6_design", [])),
    }

    close_candidate = {
        "schema_version": "c6_example_extraction_reviewed_reference_close_candidate_v0",
        "candidate_status": "C6_EXAMPLE_EXTRACTION_REVIEWED_REFERENCE_CLOSE_READY" if review_pass else "C6_EXAMPLE_EXTRACTION_REFERENCE_NOT_CLOSE_READY",
        "review_pass": review_pass,
        "source_c6_example_extraction_receipt_id": SOURCE_C6_EXTRACT_RECEIPT_ID,
        "closure_meaning": "Close extracted C5-to-C6 examples as reviewed reference.",
        "closure_does_not_mean": [
            "C6 opened",
            "C6 protocol designed",
            "C6 protocol emitted",
            "full transfer proven",
            "general Cell 1 authority granted",
        ],
        "recommended_next": recommended_next,
    }

    authority_boundary = {
        "schema_version": "c6_example_extraction_review_authority_boundary_v0",
        "status": status,
        "may_close_examples_as_reviewed_reference_next": review_pass,
        "may_open_c6_now_in_review": False,
        "may_design_c6_protocol_now_in_review": False,
        "may_emit_c6_protocol_now_in_review": False,
        "may_execute_new_domain_shift": False,
        "may_mutate_c5_reference": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_claim_transfer": False,
        "may_claim_global_autonomy": False,
        "may_grant_general_cell1_authority": False,
    }

    classification = {
        "schema_version": "c6_example_extraction_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "c6_example_extraction_review_complete": review_pass,
        "c6_example_extraction_review_pass": review_pass,
        "close_candidate_ready": review_pass,
        "examples_reviewed": len(examples),
        "example_types_reviewed": actual_types,
        "proposal_packet_examples_reviewed": summary.get("proposal_packet_examples_extracted"),
        "accepted_packet_examples_reviewed": summary.get("accepted_packet_examples_extracted"),
        "cell1_probe_examples_reviewed": summary.get("cell1_probe_examples_extracted"),
        "verification_examples_reviewed": summary.get("verification_examples_extracted"),
        "handoff_examples_reviewed": summary.get("handoff_examples_extracted"),
        "blocked_feedback_examples_reviewed": summary.get("blocked_feedback_examples_extracted"),
        "edge_examples_reviewed": summary.get("edge_examples_extracted"),
        "protocol_pressure_readout_reviewed": True,
        "c6_opened": False,
        "c6_design_executed": False,
        "c6_protocol_emitted": False,
        "new_domain_shift_executed": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "c5_reference_mutated": False,
        "full_transfer_claimed": False,
        "global_autonomy_claimed": False,
        "general_cell1_authority_claimed": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "c6_example_extraction_review_rollup_v0",
        "review_count": 1 if review_pass else 0,
        "review_pass_count": 1 if review_pass else 0,
        "close_candidate_ready_count": 1 if review_pass else 0,
        "examples_reviewed": len(examples),
        "example_type_count": len(actual_types),
        "proposal_packet_examples_reviewed": summary.get("proposal_packet_examples_extracted"),
        "accepted_packet_examples_reviewed": summary.get("accepted_packet_examples_extracted"),
        "cell1_probe_examples_reviewed": summary.get("cell1_probe_examples_extracted"),
        "verification_examples_reviewed": summary.get("verification_examples_extracted"),
        "handoff_examples_reviewed": summary.get("handoff_examples_extracted"),
        "blocked_feedback_examples_reviewed": summary.get("blocked_feedback_examples_extracted"),
        "edge_examples_reviewed": summary.get("edge_examples_extracted"),
        "c6_opened_count": 0,
        "c6_design_executed_count": 0,
        "c6_protocol_emitted_count": 0,
        "new_domain_shift_executed_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "c5_reference_mutated_count": 0,
        "full_transfer_claim_count": 0,
        "global_autonomy_claim_count": 0,
        "general_cell1_authority_claim_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    profile = {
        "schema_version": "c6_example_extraction_review_profile_v0",
        "profile_id": "c6_example_extraction_review_" + sig8(rollup),
        "status": status,
        "review_pass": review_pass,
        "close_candidate_ready": review_pass,
        "examples_reviewed": len(examples),
        "example_types_reviewed": actual_types,
        "c6_opened": False,
        "c6_design_executed": False,
        "c6_protocol_emitted": False,
        "bad_counters_zero": all(
            rollup[k] == 0 for k in [
                "c6_opened_count",
                "c6_design_executed_count",
                "c6_protocol_emitted_count",
                "new_domain_shift_executed_count",
                "source_mutated_count",
                "prior_receipt_mutated_count",
                "c5_reference_mutated_count",
                "full_transfer_claim_count",
                "global_autonomy_claim_count",
                "general_cell1_authority_claim_count",
                "hidden_next_command_count",
                "latest_file_guessing_count",
                "mtime_selection_count",
            ]
        ),
        "recommendation": "Close the reviewed C5-to-C6 example extraction as a reference before any C6 protocol design.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "c6_example_extraction_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "C5-to-C6 example extraction reviewed clean. The review confirms the examples cover proposed-only packets, accepted proposal packets, Cell 1 bounded probe consumption, verification return, handoff return, diagnostic blocked feedback, and decision-edge observations. C6 remains unopened and undesigned.",
        "examples_reviewed": len(examples),
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "c6_example_extraction_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c6_example_extraction_receipt",
                "question": "did extraction complete and become review-ready",
                "answer": "yes" if review_pass else "no",
                "taken": "review extracted examples and boundaries",
            },
            {
                "step": "confirm_example_surface",
                "question": "do examples cover proposal, acceptance, Cell1, verification, handoff, feedback, and edge surfaces",
                "answer": "yes" if review_pass else "no",
                "taken": "emit close candidate",
            },
            {
                "step": "preserve_no_c6_design_boundary",
                "question": "does review open or design C6",
                "answer": "no",
                "taken": "recommend closure as reviewed reference",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (REVIEW_BASIS_PATH, review_basis),
        (SCHEMA_REVIEW_PATH, schema_review),
        (CATALOG_REVIEW_PATH, catalog_review),
        (EXAMPLE_SURFACE_REVIEW_PATH, example_surface_review),
        (PROPOSAL_REVIEW_PATH, proposal_review),
        (ACCEPTED_PACKET_REVIEW_PATH, accepted_packet_review),
        (CELL1_PROBE_REVIEW_PATH, cell1_probe_review),
        (VERIFICATION_REVIEW_PATH, verification_review),
        (HANDOFF_REVIEW_PATH, handoff_review),
        (BLOCKED_FEEDBACK_REVIEW_PATH, blocked_feedback_review),
        (EDGE_REVIEW_PATH, edge_review),
        (PROTOCOL_PRESSURE_REVIEW_PATH, pressure_review),
        (CLOSE_CANDIDATE_PATH, close_candidate),
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
        "C6_EXAMPLE_REVIEW_0_EXTRACTION_RECEIPT_CONSUMED": SOURCE_C6_EXTRACT_RECEIPT_PATH.exists(),
        "C6_EXAMPLE_REVIEW_1_REVIEW_BASIS_EMITTED": REVIEW_BASIS_PATH.exists(),
        "C6_EXAMPLE_REVIEW_2_SCHEMA_REVIEWED": schema_review["review_status"] == "PASS",
        "C6_EXAMPLE_REVIEW_3_CATALOG_REVIEWED": catalog_review["example_count"] == 12,
        "C6_EXAMPLE_REVIEW_4_REQUIRED_SURFACES_PRESENT": all(example_surface_review["required_surfaces_present"].values()),
        "C6_EXAMPLE_REVIEW_5_PROPOSAL_DISTINCTION_PRESERVED": proposal_review["proposal_packet_not_command"] is True,
        "C6_EXAMPLE_REVIEW_6_ACCEPTED_PACKET_BOUNDARY_REVIEWED": accepted_packet_review["review_acceptance_boundary_preserved"] is True,
        "C6_EXAMPLE_REVIEW_7_CELL1_PROBE_BOUNDARY_REVIEWED": cell1_probe_review["freebuild_count"] == 0 and cell1_probe_review["auto_chain_count"] == 0,
        "C6_EXAMPLE_REVIEW_8_VERIFICATION_REVIEWED": verification_review["verification_examples"] == 5,
        "C6_EXAMPLE_REVIEW_9_HANDOFF_REVIEWED": handoff_review["handoff_examples"] == 1,
        "C6_EXAMPLE_REVIEW_10_BLOCKED_FEEDBACK_REVIEWED": blocked_feedback_review["blocked_feedback_examples"] == 2 and blocked_feedback_review["bare_failed_status_count"] == 0,
        "C6_EXAMPLE_REVIEW_11_EDGE_EXAMPLES_REVIEWED": edge_review["edge_examples"] == 5,
        "C6_EXAMPLE_REVIEW_12_PRESSURE_READOUT_REVIEWED_AS_NON_PROTOCOL_DESIGN": pressure_review["not_a_c6_protocol_design"] is True,
        "C6_EXAMPLE_REVIEW_13_CLOSE_CANDIDATE_READY": close_candidate["candidate_status"] == "C6_EXAMPLE_EXTRACTION_REVIEWED_REFERENCE_CLOSE_READY",
        "C6_EXAMPLE_REVIEW_14_NO_C6_OPENED": classification["c6_opened"] is False,
        "C6_EXAMPLE_REVIEW_15_NO_C6_DESIGN_EXECUTED": classification["c6_design_executed"] is False,
        "C6_EXAMPLE_REVIEW_16_NO_C6_PROTOCOL_EMITTED": classification["c6_protocol_emitted"] is False,
        "C6_EXAMPLE_REVIEW_17_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["c5_reference_mutated"] is False,
        "C6_EXAMPLE_REVIEW_18_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False,
        "C6_EXAMPLE_REVIEW_19_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C6_EXAMPLE_REVIEW_20_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "C6_EXAMPLE_REVIEW_21_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_REVIEW_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_REVIEW_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_extract_receipt": SOURCE_C6_EXTRACT_RECEIPT_ID,
        "examples_reviewed": len(examples),
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "c6_example_extraction_from_c5_reference_review_receipt_v0",
        "receipt_type": "TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_c6_example_extraction_receipt_id": SOURCE_C6_EXTRACT_RECEIPT_ID,
        "machine_readable_c6_example_extraction_review_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "c6_example_extraction_review_complete": gate == "PASS",
            "c6_example_extraction_review_pass": gate == "PASS",
            "close_candidate_ready": gate == "PASS",
            "examples_reviewed": len(examples),
            "example_types_reviewed": actual_types,
            "proposal_packet_examples_reviewed": summary.get("proposal_packet_examples_extracted"),
            "accepted_packet_examples_reviewed": summary.get("accepted_packet_examples_extracted"),
            "cell1_probe_examples_reviewed": summary.get("cell1_probe_examples_extracted"),
            "verification_examples_reviewed": summary.get("verification_examples_extracted"),
            "handoff_examples_reviewed": summary.get("handoff_examples_extracted"),
            "blocked_feedback_examples_reviewed": summary.get("blocked_feedback_examples_extracted"),
            "edge_examples_reviewed": summary.get("edge_examples_extracted"),
            "protocol_pressure_readout_reviewed": gate == "PASS",
            "protocol_pressure_readout_is_not_protocol_design": pressure_review["not_a_c6_protocol_design"],
            "c6_opened": False,
            "c6_design_executed": False,
            "c6_protocol_emitted": False,
            "new_domain_shift_executed": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "c5_reference_mutated": False,
            "full_transfer_claimed": False,
            "global_autonomy_claimed": False,
            "general_cell1_authority_claimed": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": profile["bad_counters_zero"],
            "recommended_next": final_next,
        },
        "aggregate_metrics": report | {"status": final_status, "recommended_next_handling": final_next},
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "review_basis": rel(REVIEW_BASIS_PATH),
            "schema_review": rel(SCHEMA_REVIEW_PATH),
            "catalog_review": rel(CATALOG_REVIEW_PATH),
            "example_surface_review": rel(EXAMPLE_SURFACE_REVIEW_PATH),
            "proposal_review": rel(PROPOSAL_REVIEW_PATH),
            "accepted_packet_review": rel(ACCEPTED_PACKET_REVIEW_PATH),
            "cell1_probe_review": rel(CELL1_PROBE_REVIEW_PATH),
            "verification_review": rel(VERIFICATION_REVIEW_PATH),
            "handoff_review": rel(HANDOFF_REVIEW_PATH),
            "blocked_feedback_review": rel(BLOCKED_FEEDBACK_REVIEW_PATH),
            "edge_review": rel(EDGE_REVIEW_PATH),
            "protocol_pressure_review": rel(PROTOCOL_PRESSURE_REVIEW_PATH),
            "close_candidate": rel(CLOSE_CANDIDATE_PATH),
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
    print(f"c6_example_extraction_review_receipt_id={receipt_id}")
    print(f"c6_example_extraction_review_receipt_path={rel(receipt_path)}")
    print(f"c6_example_extraction_review_basis_path={rel(REVIEW_BASIS_PATH)}")
    print(f"c6_example_extraction_close_candidate_path={rel(CLOSE_CANDIDATE_PATH)}")
    print(f"c6_example_extraction_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"c6_example_extraction_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
