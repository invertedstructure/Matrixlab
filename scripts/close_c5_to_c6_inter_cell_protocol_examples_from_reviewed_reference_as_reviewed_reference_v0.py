#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_C5_TO_C6_INTER_CELL_PROTOCOL_EXAMPLES_FROM_REVIEWED_REFERENCE_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "c6.inter_cell_protocol_examples_from_c5_reference.reviewed_reference.v0"
LAYER = "BRIDGE / C5_TO_C6 / EXAMPLE_REFERENCE_CLOSURE"
MODE = "CLOSE_ONLY / FREEZE_EXAMPLES_AS_REVIEWED_REFERENCE / NO_C6_OPENING"
BUILD_MODE = "C5_TO_C6_EXAMPLE_REFERENCE_CLOSURE_ONLY"

SOURCE_C6_EXAMPLE_REVIEW_RECEIPT_ID = "727a881c"
SOURCE_C6_EXAMPLE_EXTRACTION_RECEIPT_ID = "c486e477"

SOURCE_C6_EXAMPLE_REVIEW_RECEIPT_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0_receipts/727a881c.json"
SOURCE_C6_EXAMPLE_EXTRACTION_RECEIPT_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0_receipts/c486e477.json"

REVIEW_BASIS_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_example_extraction_review_basis_v0.json"
SCHEMA_REVIEW_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_inter_cell_protocol_example_schema_review_v0.json"
CATALOG_REVIEW_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_inter_cell_protocol_example_catalog_review_v0.json"
EXAMPLE_SURFACE_REVIEW_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_inter_cell_protocol_example_surface_review_v0.json"
PROPOSAL_REVIEW_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_proposal_packet_example_review_v0.json"
ACCEPTED_PACKET_REVIEW_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_accepted_packet_example_review_v0.json"
CELL1_PROBE_REVIEW_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_cell1_probe_example_review_v0.json"
VERIFICATION_REVIEW_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_verification_example_review_v0.json"
HANDOFF_REVIEW_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_handoff_example_review_v0.json"
BLOCKED_FEEDBACK_REVIEW_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_blocked_feedback_example_review_v0.json"
EDGE_REVIEW_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_edge_observation_example_review_v0.json"
PROTOCOL_PRESSURE_REVIEW_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_protocol_pressure_readout_review_v0.json"
CLOSE_CANDIDATE_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_example_extraction_reviewed_reference_close_candidate_v0.json"
REVIEW_AUTHORITY_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_example_extraction_review_authority_boundary_v0.json"
REVIEW_CLASSIFICATION_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_example_extraction_review_classification_v0.json"
REVIEW_ROLLUP_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_example_extraction_review_rollup_v0.json"
REVIEW_PROFILE_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_example_extraction_review_profile_v0.json"
REVIEW_REPORT_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_example_extraction_review_report.json"
REVIEW_TRACE_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0/c6_example_extraction_review_transition_trace.json"

EXTRACTION_EXAMPLES_JSONL_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_inter_cell_protocol_examples_from_c5_v0.jsonl"
EXTRACTION_CATALOG_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_inter_cell_protocol_example_catalog_v0.json"
EXTRACTION_SCHEMA_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_inter_cell_protocol_example_schema_v0.json"
EXTRACTION_PRESSURE_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_protocol_pressure_readout_from_c5_examples_v0.json"
EXTRACTION_ROLLUP_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_example_extraction_rollup_v0.json"
EXTRACTION_PROFILE_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_example_extraction_profile_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C6_EXAMPLE_REVIEW_RECEIPT_PATH,
    SOURCE_C6_EXAMPLE_EXTRACTION_RECEIPT_PATH,
    REVIEW_BASIS_PATH,
    SCHEMA_REVIEW_PATH,
    CATALOG_REVIEW_PATH,
    EXAMPLE_SURFACE_REVIEW_PATH,
    PROPOSAL_REVIEW_PATH,
    ACCEPTED_PACKET_REVIEW_PATH,
    CELL1_PROBE_REVIEW_PATH,
    VERIFICATION_REVIEW_PATH,
    HANDOFF_REVIEW_PATH,
    BLOCKED_FEEDBACK_REVIEW_PATH,
    EDGE_REVIEW_PATH,
    PROTOCOL_PRESSURE_REVIEW_PATH,
    CLOSE_CANDIDATE_PATH,
    REVIEW_AUTHORITY_PATH,
    REVIEW_CLASSIFICATION_PATH,
    REVIEW_ROLLUP_PATH,
    REVIEW_PROFILE_PATH,
    REVIEW_REPORT_PATH,
    REVIEW_TRACE_PATH,
    EXTRACTION_EXAMPLES_JSONL_PATH,
    EXTRACTION_CATALOG_PATH,
    EXTRACTION_SCHEMA_PATH,
    EXTRACTION_PRESSURE_PATH,
    EXTRACTION_ROLLUP_PATH,
    EXTRACTION_PROFILE_PATH,
]

OUT_DIR = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0"
RECEIPT_DIR = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0_receipts"

CLOSURE_BASIS_PATH = OUT_DIR / "c6_example_reference_closure_basis_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "c6_example_extraction_reviewed_reference_v0.json"
FREEZE_MANIFEST_PATH = OUT_DIR / "c6_example_extraction_reviewed_reference_freeze_manifest_v0.json"
REFERENCE_INDEX_PATH = OUT_DIR / "c6_example_extraction_reviewed_reference_index_v0.json"
EXAMPLE_SURFACE_REFERENCE_PATH = OUT_DIR / "c6_inter_cell_example_surface_reference_v0.json"
PROTOCOL_PRESSURE_REFERENCE_PATH = OUT_DIR / "c6_protocol_pressure_reference_non_design_v0.json"
NEXT_DECISION_READY_PATH = OUT_DIR / "c6_example_reference_post_closure_decision_ready_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "c6_example_reference_closure_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "c6_example_reference_closure_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "c6_example_reference_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c6_example_reference_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "c6_example_reference_closure_report.json"
TRACE_PATH = OUT_DIR / "c6_example_reference_closure_transition_trace.json"

EXPECTED_REVIEW_STATUS = "TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_REVIEWED_CLOSE_READY"
EXPECTED_REVIEW_STOP = "STOP_TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_REVIEWED_CLOSE_READY"
EXPECTED_REVIEW_NEXT = "CLOSE_C5_TO_C6_INTER_CELL_PROTOCOL_EXAMPLES_FROM_REVIEWED_REFERENCE_AS_REVIEWED_REFERENCE_V0"
RECOMMENDED_NEXT = "DECIDE_NEXT_AFTER_C5_TO_C6_INTER_CELL_PROTOCOL_EXAMPLES_REFERENCE_CLOSURE_V0"

EXPECTED_TYPES = [
    "ACCEPTED_PROPOSAL_PACKET",
    "BLOCKED_OR_TYPED_STOP_FEEDBACK",
    "CELL1_ACCEPTED_PROPOSAL_CONSUMPTION",
    "DECISION_EDGE_OBSERVATION",
    "HANDOFF_RETURN_TO_CELL0",
    "PROPOSAL_PACKET_PROPOSED_ONLY",
    "VERIFICATION_RETURN",
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

    review_receipt = read_json(SOURCE_C6_EXAMPLE_REVIEW_RECEIPT_PATH)
    review_summary = review_receipt.get("machine_readable_c6_example_extraction_review_summary", {})

    extract_receipt = read_json(SOURCE_C6_EXAMPLE_EXTRACTION_RECEIPT_PATH)
    extract_summary = extract_receipt.get("machine_readable_c6_example_extraction_summary", {})

    close_candidate = read_json(CLOSE_CANDIDATE_PATH)
    review_authority = read_json(REVIEW_AUTHORITY_PATH)
    review_classification = read_json(REVIEW_CLASSIFICATION_PATH)
    review_rollup = read_json(REVIEW_ROLLUP_PATH)
    review_profile = read_json(REVIEW_PROFILE_PATH)
    review_report = read_json(REVIEW_REPORT_PATH)
    review_trace = read_json(REVIEW_TRACE_PATH)

    examples = read_jsonl(EXTRACTION_EXAMPLES_JSONL_PATH)
    catalog = read_json(EXTRACTION_CATALOG_PATH)
    schema = read_json(EXTRACTION_SCHEMA_PATH)
    pressure = read_json(EXTRACTION_PRESSURE_PATH)

    if review_receipt.get("receipt_id") != SOURCE_C6_EXAMPLE_REVIEW_RECEIPT_ID or review_receipt.get("gate") != "PASS":
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
        "c6_example_extraction_review_complete",
        "c6_example_extraction_review_pass",
        "close_candidate_ready",
        "protocol_pressure_readout_reviewed",
        "protocol_pressure_readout_is_not_protocol_design",
        "bad_counters_zero",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"review_summary_required_true_missing:{key}")

    expected_counts = {
        "examples_reviewed": 12,
        "proposal_packet_examples_reviewed": 2,
        "accepted_packet_examples_reviewed": 1,
        "cell1_probe_examples_reviewed": 1,
        "verification_examples_reviewed": 5,
        "handoff_examples_reviewed": 1,
        "blocked_feedback_examples_reviewed": 2,
        "edge_examples_reviewed": 5,
    }
    for key, expected in expected_counts.items():
        if review_summary.get(key) != expected:
            failures.append(f"review_count_wrong:{key}:{review_summary.get(key)}")

    if sorted(review_summary.get("example_types_reviewed", [])) != EXPECTED_TYPES:
        failures.append("review_example_types_wrong")

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
        if review_summary.get(key) is not False:
            failures.append(f"review_forbidden_true:{key}")

    if extract_receipt.get("receipt_id") != SOURCE_C6_EXAMPLE_EXTRACTION_RECEIPT_ID or extract_receipt.get("gate") != "PASS":
        failures.append("extract_receipt_not_pass")
    if extract_summary.get("examples_extracted") != 12:
        failures.append("extract_examples_count_wrong")
    if close_candidate.get("candidate_status") != "C6_EXAMPLE_EXTRACTION_REVIEWED_REFERENCE_CLOSE_READY":
        failures.append("close_candidate_not_ready")
    if close_candidate.get("review_pass") is not True:
        failures.append("close_candidate_review_not_pass")
    if review_authority.get("may_close_examples_as_reviewed_reference_next") is not True:
        failures.append("review_authority_no_close")
    for forbidden in [
        "may_open_c6_now_in_review",
        "may_design_c6_protocol_now_in_review",
        "may_emit_c6_protocol_now_in_review",
        "may_execute_new_domain_shift",
        "may_mutate_c5_reference",
        "may_mutate_source",
        "may_mutate_prior_receipts",
        "may_claim_transfer",
        "may_claim_global_autonomy",
        "may_grant_general_cell1_authority",
    ]:
        if review_authority.get(forbidden) is not False:
            failures.append(f"review_authority_forbidden_true:{forbidden}")

    if review_classification.get("close_candidate_ready") is not True:
        failures.append("review_classification_close_not_ready")
    if review_classification.get("next_command_goal") is not None:
        failures.append("review_classification_hidden_next")
    if review_rollup.get("review_pass_count") != 1 or review_rollup.get("close_candidate_ready_count") != 1:
        failures.append("review_rollup_wrong")
    if review_profile.get("close_candidate_ready") is not True or review_profile.get("next_command_goal") is not None:
        failures.append("review_profile_wrong")
    if review_report.get("recommended_next_handling") != EXPECTED_REVIEW_NEXT:
        failures.append("review_report_next_wrong")
    if review_trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("review_trace_hidden_next")

    if len(examples) != 12:
        failures.append(f"examples_jsonl_count_wrong:{len(examples)}")
    if catalog.get("example_count") != 12:
        failures.append("catalog_count_wrong")
    if sorted(catalog.get("example_types", [])) != EXPECTED_TYPES:
        failures.append("catalog_types_wrong")
    if sorted(schema.get("closed_example_types", [])) != EXPECTED_TYPES:
        failures.append("schema_types_wrong")
    if pressure.get("not_a_c6_protocol_design") is not True:
        failures.append("pressure_claims_protocol_design")

    return failures, {
        "review_summary": review_summary,
        "extract_summary": extract_summary,
        "examples": examples,
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

    close_pass = not failures
    status = "TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY" if close_pass else "TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_REFERENCE_CLOSURE_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if close_pass else "REPAIR_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_REFERENCE_CLOSURE_V0"

    review_summary = basis.get("review_summary", {})
    examples = basis.get("examples", [])
    catalog = basis.get("catalog", {})
    pressure = basis.get("pressure", {})

    reason_codes = [
        "C6_EXAMPLE_EXTRACTION_CLOSED_AS_REVIEWED_REFERENCE",
        "C6_EXAMPLE_REVIEW_RECEIPT_CONSUMED",
        "C6_EXAMPLE_EXTRACTION_RECEIPT_CONSUMED",
        "EXAMPLE_SURFACE_FROZEN",
        "EXAMPLE_SCHEMA_FROZEN",
        "EXAMPLE_CATALOG_FROZEN",
        "PROPOSED_ONLY_PACKET_EXAMPLE_FROZEN",
        "ACCEPTED_PROPOSAL_PACKET_EXAMPLE_FROZEN",
        "CELL1_BOUNDED_PROBE_EXAMPLE_FROZEN",
        "VERIFICATION_RETURN_EXAMPLE_FROZEN",
        "HANDOFF_RETURN_EXAMPLE_FROZEN",
        "DIAGNOSTIC_BLOCKED_FEEDBACK_EXAMPLES_FROZEN",
        "DECISION_EDGE_EXAMPLES_FROZEN",
        "PROTOCOL_PRESSURE_READOUT_FROZEN_AS_NON_DESIGN",
        "POST_EXAMPLE_REFERENCE_DECISION_READY",
        "NO_C6_OPENING",
        "NO_C6_DESIGN",
        "NO_C6_PROTOCOL_EMISSION",
        "NO_TRANSFER_CLAIM",
        "NO_GLOBAL_AUTONOMY_CLAIM",
        "NO_GENERAL_CELL1_AUTHORITY_CLAIM",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if close_pass else failures

    closure_basis = {
        "schema_version": "c6_example_reference_closure_basis_v0",
        "closure_status": status,
        "source_c6_example_review_receipt_id": SOURCE_C6_EXAMPLE_REVIEW_RECEIPT_ID,
        "source_c6_example_extraction_receipt_id": SOURCE_C6_EXAMPLE_EXTRACTION_RECEIPT_ID,
        "review_pass": close_pass,
        "close_candidate_ready": close_pass,
        "examples_reviewed": review_summary.get("examples_reviewed"),
        "example_types_reviewed": review_summary.get("example_types_reviewed", []),
    }

    reviewed_reference = {
        "schema_version": "c6_example_extraction_reviewed_reference_v0",
        "reference_status": "C6_EXAMPLE_EXTRACTION_REVIEWED_REFERENCE_FROZEN" if close_pass else "REFERENCE_NOT_FROZEN",
        "reference_id": "c6_example_reference_" + sig8({
            "review_receipt": SOURCE_C6_EXAMPLE_REVIEW_RECEIPT_ID,
            "extract_receipt": SOURCE_C6_EXAMPLE_EXTRACTION_RECEIPT_ID,
            "examples_reviewed": review_summary.get("examples_reviewed"),
        }),
        "examples_reviewed": review_summary.get("examples_reviewed"),
        "example_types_reviewed": review_summary.get("example_types_reviewed", []),
        "proposal_packet_examples_reviewed": review_summary.get("proposal_packet_examples_reviewed"),
        "accepted_packet_examples_reviewed": review_summary.get("accepted_packet_examples_reviewed"),
        "cell1_probe_examples_reviewed": review_summary.get("cell1_probe_examples_reviewed"),
        "verification_examples_reviewed": review_summary.get("verification_examples_reviewed"),
        "handoff_examples_reviewed": review_summary.get("handoff_examples_reviewed"),
        "blocked_feedback_examples_reviewed": review_summary.get("blocked_feedback_examples_reviewed"),
        "edge_examples_reviewed": review_summary.get("edge_examples_reviewed"),
        "protocol_pressure_readout_reviewed": True,
        "protocol_pressure_readout_is_not_protocol_design": True,
        "c6_opened": False,
        "c6_design_executed": False,
        "c6_protocol_emitted": False,
    }

    freeze_manifest = {
        "schema_version": "c6_example_extraction_reviewed_reference_freeze_manifest_v0",
        "freeze_status": "FROZEN" if close_pass else "NOT_FROZEN",
        "source_receipts": {
            "extraction": SOURCE_C6_EXAMPLE_EXTRACTION_RECEIPT_ID,
            "review": SOURCE_C6_EXAMPLE_REVIEW_RECEIPT_ID,
        },
        "frozen_source_artifacts": [rel(p) for p in REQUIRED_SOURCE_FILES],
        "frozen_reference_artifacts": {
            "closure_basis": rel(CLOSURE_BASIS_PATH),
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "example_surface_reference": rel(EXAMPLE_SURFACE_REFERENCE_PATH),
            "protocol_pressure_reference": rel(PROTOCOL_PRESSURE_REFERENCE_PATH),
            "next_decision_ready": rel(NEXT_DECISION_READY_PATH),
        },
    }

    reference_index = {
        "schema_version": "c6_example_extraction_reviewed_reference_index_v0",
        "index_status": "REFERENCE_INDEX_EMITTED" if close_pass else "REFERENCE_INDEX_NOT_EMITTED",
        "reference_paths": {
            "closure_basis": rel(CLOSURE_BASIS_PATH),
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "freeze_manifest": rel(FREEZE_MANIFEST_PATH),
            "example_surface_reference": rel(EXAMPLE_SURFACE_REFERENCE_PATH),
            "protocol_pressure_reference": rel(PROTOCOL_PRESSURE_REFERENCE_PATH),
            "next_decision_ready": rel(NEXT_DECISION_READY_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "trace": rel(TRACE_PATH),
        },
    }

    example_surface_reference = {
        "schema_version": "c6_inter_cell_example_surface_reference_v0",
        "reference_status": "EXAMPLE_SURFACE_FROZEN",
        "examples_count": len(examples),
        "example_catalog_ref": rel(EXTRACTION_CATALOG_PATH),
        "examples_jsonl_ref": rel(EXTRACTION_EXAMPLES_JSONL_PATH),
        "example_types": catalog.get("example_types", []),
        "surface_meaning": "Concrete examples from C5 for later C6 inter-cell protocol design.",
        "surface_does_not_mean": [
            "C6 protocol exists",
            "C6 is open",
            "general Cell 1 authority is granted",
            "full transfer is proven",
        ],
    }

    protocol_pressure_reference = {
        "schema_version": "c6_protocol_pressure_reference_non_design_v0",
        "reference_status": "PROTOCOL_PRESSURE_READOUT_FROZEN_AS_NON_DESIGN",
        "protocol_pressure_readout_ref": rel(EXTRACTION_PRESSURE_PATH),
        "fields_c6_likely_needs": pressure.get("fields_c6_likely_needs", []),
        "open_questions_for_later_c6_design": pressure.get("open_questions_for_later_c6_design", []),
        "not_a_c6_protocol_design": True,
    }

    next_decision_ready = {
        "schema_version": "c6_example_reference_post_closure_decision_ready_v0",
        "decision_ready": close_pass,
        "recommended_next": recommended_next,
        "decision_scope": "decide next after reviewed C5-to-C6 example reference closure",
        "eligible_next_questions": [
            "design C6 inter-cell protocol target from reviewed examples",
            "defer C6 and return to observation/unit feedback hardening",
            "extract a narrower C6 packet schema target only",
            "freeze C5/C6 bridge and stop the branch",
        ],
        "not_authorized_here": [
            "open C6 automatically",
            "emit C6 protocol",
            "execute C6 protocol",
            "run a new domain shift",
            "claim full transfer",
            "grant general Cell 1 authority",
        ],
    }

    authority_boundary = {
        "schema_version": "c6_example_reference_closure_authority_boundary_v0",
        "status": status,
        "may_decide_next_after_c6_example_reference_closure": close_pass,
        "may_open_c6_now_in_closure": False,
        "may_design_c6_protocol_now_in_closure": False,
        "may_emit_c6_protocol_now_in_closure": False,
        "may_execute_new_domain_shift": False,
        "may_mutate_c5_reference": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_claim_transfer": False,
        "may_claim_global_autonomy": False,
        "may_grant_general_cell1_authority": False,
    }

    classification = {
        "schema_version": "c6_example_reference_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "c6_example_extraction_closed_as_reviewed_reference": close_pass,
        "reviewed_reference_frozen": close_pass,
        "post_example_reference_decision_ready": close_pass,
        "examples_reviewed": review_summary.get("examples_reviewed"),
        "example_types_reviewed": review_summary.get("example_types_reviewed", []),
        "proposal_packet_examples_reviewed": review_summary.get("proposal_packet_examples_reviewed"),
        "accepted_packet_examples_reviewed": review_summary.get("accepted_packet_examples_reviewed"),
        "cell1_probe_examples_reviewed": review_summary.get("cell1_probe_examples_reviewed"),
        "verification_examples_reviewed": review_summary.get("verification_examples_reviewed"),
        "handoff_examples_reviewed": review_summary.get("handoff_examples_reviewed"),
        "blocked_feedback_examples_reviewed": review_summary.get("blocked_feedback_examples_reviewed"),
        "edge_examples_reviewed": review_summary.get("edge_examples_reviewed"),
        "protocol_pressure_readout_is_not_protocol_design": True,
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
        "schema_version": "c6_example_reference_closure_rollup_v0",
        "closure_count": 1 if close_pass else 0,
        "reviewed_reference_frozen_count": 1 if close_pass else 0,
        "post_example_reference_decision_ready_count": 1 if close_pass else 0,
        "examples_reviewed": review_summary.get("examples_reviewed"),
        "example_type_count": len(review_summary.get("example_types_reviewed", [])),
        "proposal_packet_examples_reviewed": review_summary.get("proposal_packet_examples_reviewed"),
        "accepted_packet_examples_reviewed": review_summary.get("accepted_packet_examples_reviewed"),
        "cell1_probe_examples_reviewed": review_summary.get("cell1_probe_examples_reviewed"),
        "verification_examples_reviewed": review_summary.get("verification_examples_reviewed"),
        "handoff_examples_reviewed": review_summary.get("handoff_examples_reviewed"),
        "blocked_feedback_examples_reviewed": review_summary.get("blocked_feedback_examples_reviewed"),
        "edge_examples_reviewed": review_summary.get("edge_examples_reviewed"),
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
        "schema_version": "c6_example_reference_closure_profile_v0",
        "profile_id": "c6_example_reference_closure_" + sig8(rollup),
        "status": status,
        "reviewed_reference_frozen": close_pass,
        "post_example_reference_decision_ready": close_pass,
        "examples_reviewed": review_summary.get("examples_reviewed"),
        "example_types_reviewed": review_summary.get("example_types_reviewed", []),
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
        "recommendation": "Decide next after closing the reviewed C5-to-C6 example reference.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "c6_example_reference_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "C5-to-C6 inter-cell protocol examples are closed as a reviewed reference. The frozen reference preserves the example surface for later C6 protocol design without opening C6, emitting a protocol, mutating references, or claiming transfer/autonomy/general Cell 1 authority.",
        "examples_reviewed": review_summary.get("examples_reviewed"),
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "c6_example_reference_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_example_review_receipt",
                "question": "is the C5-to-C6 example surface reviewed and close-ready",
                "answer": "yes" if close_pass else "no",
                "taken": "freeze reviewed example reference",
            },
            {
                "step": "freeze_example_reference",
                "question": "what is frozen",
                "answer": "examples, schema, catalog, pressure readout, and no-design boundary",
                "taken": "emit reference index and freeze manifest",
            },
            {
                "step": "preserve_no_c6_open_boundary",
                "question": "does closure open/design/emit C6",
                "answer": "no",
                "taken": "emit post-example-reference decision readiness",
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
        (EXAMPLE_SURFACE_REFERENCE_PATH, example_surface_reference),
        (PROTOCOL_PRESSURE_REFERENCE_PATH, protocol_pressure_reference),
        (NEXT_DECISION_READY_PATH, next_decision_ready),
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
        "C6_EXAMPLE_REF_CLOSE_0_REVIEW_RECEIPT_CONSUMED": SOURCE_C6_EXAMPLE_REVIEW_RECEIPT_PATH.exists(),
        "C6_EXAMPLE_REF_CLOSE_1_EXTRACTION_RECEIPT_CONSUMED": SOURCE_C6_EXAMPLE_EXTRACTION_RECEIPT_PATH.exists(),
        "C6_EXAMPLE_REF_CLOSE_2_CLOSURE_BASIS_EMITTED": CLOSURE_BASIS_PATH.exists(),
        "C6_EXAMPLE_REF_CLOSE_3_REVIEWED_REFERENCE_FROZEN": REVIEWED_REFERENCE_PATH.exists() and reviewed_reference["reference_status"] == "C6_EXAMPLE_EXTRACTION_REVIEWED_REFERENCE_FROZEN",
        "C6_EXAMPLE_REF_CLOSE_4_FREEZE_MANIFEST_EMITTED": FREEZE_MANIFEST_PATH.exists(),
        "C6_EXAMPLE_REF_CLOSE_5_REFERENCE_INDEX_EMITTED": REFERENCE_INDEX_PATH.exists(),
        "C6_EXAMPLE_REF_CLOSE_6_EXAMPLE_SURFACE_REFERENCE_EMITTED": EXAMPLE_SURFACE_REFERENCE_PATH.exists() and example_surface_reference["examples_count"] == 12,
        "C6_EXAMPLE_REF_CLOSE_7_PROTOCOL_PRESSURE_REFERENCE_NON_DESIGN": PROTOCOL_PRESSURE_REFERENCE_PATH.exists() and protocol_pressure_reference["not_a_c6_protocol_design"] is True,
        "C6_EXAMPLE_REF_CLOSE_8_POST_REFERENCE_DECISION_READY": NEXT_DECISION_READY_PATH.exists() and next_decision_ready["decision_ready"] is True,
        "C6_EXAMPLE_REF_CLOSE_9_NO_C6_OPENED": classification["c6_opened"] is False,
        "C6_EXAMPLE_REF_CLOSE_10_NO_C6_DESIGN_OR_PROTOCOL_EMISSION": classification["c6_design_executed"] is False and classification["c6_protocol_emitted"] is False,
        "C6_EXAMPLE_REF_CLOSE_11_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["c5_reference_mutated"] is False,
        "C6_EXAMPLE_REF_CLOSE_12_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False,
        "C6_EXAMPLE_REF_CLOSE_13_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C6_EXAMPLE_REF_CLOSE_14_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "C6_EXAMPLE_REF_CLOSE_15_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_REFERENCE_CLOSURE_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_REFERENCE_CLOSURE_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_REFERENCE_CLOSURE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_review_receipt": SOURCE_C6_EXAMPLE_REVIEW_RECEIPT_ID,
        "examples_reviewed": review_summary.get("examples_reviewed"),
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "c6_example_extraction_from_c5_reference_reference_closure_receipt_v0",
        "receipt_type": "TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_REFERENCE_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_c6_example_review_receipt_id": SOURCE_C6_EXAMPLE_REVIEW_RECEIPT_ID,
        "source_c6_example_extraction_receipt_id": SOURCE_C6_EXAMPLE_EXTRACTION_RECEIPT_ID,
        "machine_readable_c6_example_reference_closure_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "c6_example_extraction_closed_as_reviewed_reference": gate == "PASS",
            "reviewed_reference_frozen": gate == "PASS",
            "post_example_reference_decision_ready": gate == "PASS",
            "examples_reviewed": review_summary.get("examples_reviewed"),
            "example_types_reviewed": review_summary.get("example_types_reviewed", []),
            "proposal_packet_examples_reviewed": review_summary.get("proposal_packet_examples_reviewed"),
            "accepted_packet_examples_reviewed": review_summary.get("accepted_packet_examples_reviewed"),
            "cell1_probe_examples_reviewed": review_summary.get("cell1_probe_examples_reviewed"),
            "verification_examples_reviewed": review_summary.get("verification_examples_reviewed"),
            "handoff_examples_reviewed": review_summary.get("handoff_examples_reviewed"),
            "blocked_feedback_examples_reviewed": review_summary.get("blocked_feedback_examples_reviewed"),
            "edge_examples_reviewed": review_summary.get("edge_examples_reviewed"),
            "protocol_pressure_readout_is_not_protocol_design": True,
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
            "closure_basis": rel(CLOSURE_BASIS_PATH),
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "freeze_manifest": rel(FREEZE_MANIFEST_PATH),
            "reference_index": rel(REFERENCE_INDEX_PATH),
            "example_surface_reference": rel(EXAMPLE_SURFACE_REFERENCE_PATH),
            "protocol_pressure_reference": rel(PROTOCOL_PRESSURE_REFERENCE_PATH),
            "next_decision_ready": rel(NEXT_DECISION_READY_PATH),
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
    print(f"c6_example_reference_closure_receipt_id={receipt_id}")
    print(f"c6_example_reference_closure_receipt_path={rel(receipt_path)}")
    print(f"c6_example_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"c6_example_freeze_manifest_path={rel(FREEZE_MANIFEST_PATH)}")
    print(f"c6_example_next_decision_ready_path={rel(NEXT_DECISION_READY_PATH)}")
    print(f"c6_example_reference_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"c6_example_reference_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
