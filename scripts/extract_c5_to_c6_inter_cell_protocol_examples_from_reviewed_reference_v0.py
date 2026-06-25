#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "EXTRACT_C5_TO_C6_INTER_CELL_PROTOCOL_EXAMPLES_FROM_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "c6.inter_cell_protocol_examples_from_c5_reference.v0"
LAYER = "BRIDGE / C5_TO_C6 / EXAMPLE_EXTRACTION"
MODE = "EXTRACT_ONLY / NO_C6_OPENING / NO_C6_PROTOCOL_DESIGN"
BUILD_MODE = "C5_TO_C6_EXAMPLE_EXTRACTION_ONLY"

SOURCE_POST_C5_DECISION_RECEIPT_ID = "23cb11ed"
SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_ID = "934363ba"
SOURCE_C5_BUILD_RECEIPT_ID = "b4acefb6"

SOURCE_POST_C5_DECISION_RECEIPT_PATH = ROOT / "data/c5_post_domain_shift_reference_decision_v0_receipts/23cb11ed.json"

C5_POST_DECISION_BASIS_PATH = ROOT / "data/c5_post_domain_shift_reference_decision_v0/c5_post_reference_decision_basis_v0.json"
C5_POST_SELECTED_BRANCH_PATH = ROOT / "data/c5_post_domain_shift_reference_decision_v0/c5_post_reference_selected_branch_v0.json"
C6_EXTRACTION_AUTH_PATH = ROOT / "data/c5_post_domain_shift_reference_decision_v0/c6_example_extraction_authorization_from_c5_reference_v0.json"
C5_REFERENCE_CONTINUATION_PATH = ROOT / "data/c5_post_domain_shift_reference_decision_v0/c5_reference_continuation_for_c6_examples_v0.json"
C5_POST_AUTHORITY_PATH = ROOT / "data/c5_post_domain_shift_reference_decision_v0/c5_post_reference_decision_authority_boundary_v0.json"
C5_POST_CLASSIFICATION_PATH = ROOT / "data/c5_post_domain_shift_reference_decision_v0/c5_post_reference_decision_classification_v0.json"
C5_POST_ROLLUP_PATH = ROOT / "data/c5_post_domain_shift_reference_decision_v0/c5_post_reference_decision_rollup_v0.json"
C5_POST_PROFILE_PATH = ROOT / "data/c5_post_domain_shift_reference_decision_v0/c5_post_reference_decision_profile_v0.json"

C5_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0_receipts/934363ba.json"
C5_REVIEWED_REFERENCE_PATH = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0/c5_domain_shift_reviewed_reference_v0.json"
C5_REFERENCE_INDEX_PATH = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0/c5_domain_shift_reviewed_reference_index_v0.json"

C5_BUILD_RECEIPT_PATH = ROOT / "data/c5_full_domain_shift_transition_v0_receipts/b4acefb6.json"
C5_DOMAIN_FIXTURES_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_fixture_records_v0.jsonl"
C5_PROPOSAL_PACKETS_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_proposal_packets_v0.jsonl"
C5_CELL1_BUILD_RECEIPTS_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_cell1_build_receipts_v0.jsonl"
C5_VERIFICATION_RECEIPTS_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_verification_receipts_v0.jsonl"
C5_HANDOFF_RECORDS_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_handoff_records_v0.jsonl"
C5_EDGE_OBSERVATIONS_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/decision_edge_observation_records_v0.jsonl"
C5_UNIT_FEEDBACK_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/unit_feedback_records_v0.jsonl"
C5_BUILD_ROLLUP_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_rollup_v0.json"
C5_BUILD_READOUT_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_readout_v0.json"
C5_BUILD_PROFILE_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/c5_transition_profile_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_POST_C5_DECISION_RECEIPT_PATH,
    C5_POST_DECISION_BASIS_PATH,
    C5_POST_SELECTED_BRANCH_PATH,
    C6_EXTRACTION_AUTH_PATH,
    C5_REFERENCE_CONTINUATION_PATH,
    C5_POST_AUTHORITY_PATH,
    C5_POST_CLASSIFICATION_PATH,
    C5_POST_ROLLUP_PATH,
    C5_POST_PROFILE_PATH,
    C5_REFERENCE_CLOSURE_RECEIPT_PATH,
    C5_REVIEWED_REFERENCE_PATH,
    C5_REFERENCE_INDEX_PATH,
    C5_BUILD_RECEIPT_PATH,
    C5_DOMAIN_FIXTURES_PATH,
    C5_PROPOSAL_PACKETS_PATH,
    C5_CELL1_BUILD_RECEIPTS_PATH,
    C5_VERIFICATION_RECEIPTS_PATH,
    C5_HANDOFF_RECORDS_PATH,
    C5_EDGE_OBSERVATIONS_PATH,
    C5_UNIT_FEEDBACK_PATH,
    C5_BUILD_ROLLUP_PATH,
    C5_BUILD_READOUT_PATH,
    C5_BUILD_PROFILE_PATH,
]

OUT_DIR = ROOT / "data/c6_example_extraction_from_c5_reference_v0"
RECEIPT_DIR = ROOT / "data/c6_example_extraction_from_c5_reference_v0_receipts"

EXTRACTION_BASIS_PATH = OUT_DIR / "c6_example_extraction_basis_v0.json"
EXAMPLE_SCHEMA_PATH = OUT_DIR / "c6_inter_cell_protocol_example_schema_v0.json"
EXAMPLES_JSONL_PATH = OUT_DIR / "c6_inter_cell_protocol_examples_from_c5_v0.jsonl"
EXAMPLE_CATALOG_PATH = OUT_DIR / "c6_inter_cell_protocol_example_catalog_v0.json"
PROPOSAL_EXAMPLES_PATH = OUT_DIR / "c6_proposal_packet_examples_from_c5_v0.json"
ACCEPTED_PACKET_EXAMPLES_PATH = OUT_DIR / "c6_accepted_review_packet_examples_from_c5_v0.json"
CELL1_PROBE_EXAMPLES_PATH = OUT_DIR / "c6_cell1_probe_examples_from_c5_v0.json"
VERIFICATION_EXAMPLES_PATH = OUT_DIR / "c6_verification_examples_from_c5_v0.json"
HANDOFF_EXAMPLES_PATH = OUT_DIR / "c6_handoff_examples_from_c5_v0.json"
BLOCKED_FEEDBACK_EXAMPLES_PATH = OUT_DIR / "c6_blocked_feedback_examples_from_c5_v0.json"
EDGE_EXAMPLES_PATH = OUT_DIR / "c6_edge_observation_examples_from_c5_v0.json"
PROTOCOL_PRESSURE_READOUT_PATH = OUT_DIR / "c6_protocol_pressure_readout_from_c5_examples_v0.json"
REVIEW_CANDIDATE_PATH = OUT_DIR / "c6_example_extraction_review_candidate_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "c6_example_extraction_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "c6_example_extraction_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "c6_example_extraction_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c6_example_extraction_profile_v0.json"
REPORT_PATH = OUT_DIR / "c6_example_extraction_report.json"
TRACE_PATH = OUT_DIR / "c6_example_extraction_transition_trace.json"

EXPECTED_POST_C5_STATUS = "TYPED_C5_POST_REFERENCE_DECISION_SELECTED_C6_EXAMPLE_EXTRACTION_READY"
EXPECTED_NEXT_UNIT = "EXTRACT_C5_TO_C6_INTER_CELL_PROTOCOL_EXAMPLES_FROM_REVIEWED_REFERENCE_V0"
EXPECTED_SELECTED_BRANCH = "EXTRACT_C5_TO_C6_INTER_CELL_PROTOCOL_EXAMPLES_FROM_REVIEWED_REFERENCE"
RECOMMENDED_NEXT = "REVIEW_C5_TO_C6_INTER_CELL_PROTOCOL_EXAMPLES_FROM_REVIEWED_REFERENCE_V0"

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

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{rel(path)}")
    if failures:
        return failures, {}

    decision_receipt = read_json(SOURCE_POST_C5_DECISION_RECEIPT_PATH)
    decision_summary = decision_receipt.get("machine_readable_c5_post_reference_decision_summary", {})
    selected_branch = read_json(C5_POST_SELECTED_BRANCH_PATH)
    auth = read_json(C6_EXTRACTION_AUTH_PATH)
    decision_authority = read_json(C5_POST_AUTHORITY_PATH)
    decision_profile = read_json(C5_POST_PROFILE_PATH)

    closure_receipt = read_json(C5_REFERENCE_CLOSURE_RECEIPT_PATH)
    reviewed_reference = read_json(C5_REVIEWED_REFERENCE_PATH)
    build_receipt = read_json(C5_BUILD_RECEIPT_PATH)
    build_summary = build_receipt.get("machine_readable_c5_full_domain_shift_transition_summary", {})

    fixtures = read_jsonl(C5_DOMAIN_FIXTURES_PATH)
    proposals = read_jsonl(C5_PROPOSAL_PACKETS_PATH)
    builds = read_jsonl(C5_CELL1_BUILD_RECEIPTS_PATH)
    verifications = read_jsonl(C5_VERIFICATION_RECEIPTS_PATH)
    handoffs = read_jsonl(C5_HANDOFF_RECORDS_PATH)
    edges = read_jsonl(C5_EDGE_OBSERVATIONS_PATH)
    feedback = read_jsonl(C5_UNIT_FEEDBACK_PATH)
    build_rollup = read_json(C5_BUILD_ROLLUP_PATH)
    build_profile = read_json(C5_BUILD_PROFILE_PATH)

    if decision_receipt.get("receipt_id") != SOURCE_POST_C5_DECISION_RECEIPT_ID or decision_receipt.get("gate") != "PASS":
        failures.append("post_c5_decision_receipt_not_pass")
    if decision_summary.get("status") != EXPECTED_POST_C5_STATUS:
        failures.append(f"post_c5_decision_status_wrong:{decision_summary.get('status')}")
    if decision_summary.get("selected_next_branch") != EXPECTED_SELECTED_BRANCH:
        failures.append("post_c5_selected_branch_wrong")
    if decision_summary.get("selected_next_unit") != EXPECTED_NEXT_UNIT:
        failures.append("post_c5_selected_next_wrong")
    if decision_summary.get("recommended_next") != EXPECTED_NEXT_UNIT:
        failures.append("post_c5_recommended_next_wrong")
    if decision_summary.get("c6_example_extraction_authorized_next") is not True:
        failures.append("c6_extraction_not_authorized_next")

    for key in [
        "c6_opened",
        "c6_design_executed",
        "c6_example_extraction_executed_in_decision",
        "new_domain_shift_executed",
        "full_transfer_claimed",
        "research_lab_readiness_claimed",
        "global_autonomy_claimed",
        "general_cell1_authority_claimed",
        "source_mutated",
        "prior_receipt_mutated",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if decision_summary.get(key) is not False:
            failures.append(f"post_c5_forbidden_true:{key}")

    if selected_branch.get("selected_next_unit") != EXPECTED_NEXT_UNIT:
        failures.append("selected_branch_next_wrong")
    if auth.get("authorization_status") != "C6_EXAMPLE_EXTRACTION_AUTHORIZED_NEXT":
        failures.append("auth_status_wrong")
    if auth.get("authorized_next_unit") != EXPECTED_NEXT_UNIT:
        failures.append("auth_unit_wrong")
    if decision_authority.get("may_execute_c6_example_extraction_next") is not True:
        failures.append("decision_authority_no_extraction")
    if decision_authority.get("may_open_c6_now_in_decision") is not False:
        failures.append("decision_authority_allows_c6_open")
    if decision_profile.get("c6_opened") is not False or decision_profile.get("c6_design_executed") is not False:
        failures.append("decision_profile_c6_boundary_wrong")
    if closure_receipt.get("receipt_id") != SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_ID or closure_receipt.get("gate") != "PASS":
        failures.append("closure_receipt_wrong")
    if reviewed_reference.get("reference_status") != "C5_DOMAIN_SHIFT_REVIEWED_REFERENCE_FROZEN":
        failures.append("reviewed_reference_not_frozen")
    if build_receipt.get("receipt_id") != SOURCE_C5_BUILD_RECEIPT_ID or build_receipt.get("gate") != "PASS":
        failures.append("build_receipt_wrong")

    if len(fixtures) != 5:
        failures.append(f"fixture_count_wrong:{len(fixtures)}")
    if len(proposals) != 2:
        failures.append(f"proposal_count_wrong:{len(proposals)}")
    if sum(1 for p in proposals if p.get("proposal_status") == "ACCEPTED") != 1:
        failures.append("accepted_proposal_count_wrong")
    if sum(1 for p in proposals if p.get("proposal_status") == "PROPOSED_ONLY") != 1:
        failures.append("proposed_only_count_wrong")
    if len(builds) != 1:
        failures.append("build_count_wrong")
    if any(b.get("freebuild_count") != 0 or b.get("auto_chain_count") != 0 or b.get("scope_expansion_count") != 0 for b in builds):
        failures.append("cell1_forbidden_counter_nonzero")
    if len(verifications) != 5:
        failures.append("verification_count_wrong")
    if len(handoffs) != 1:
        failures.append("handoff_count_wrong")
    if len(edges) != 45:
        failures.append("edge_count_wrong")
    if len(feedback) != 2:
        failures.append("feedback_count_wrong")
    if any(f.get("feedback_quality") != "DIAGNOSTIC_USEFUL" or f.get("bare_failed_status") is not False for f in feedback):
        failures.append("feedback_quality_wrong")
    if build_rollup.get("bad_counters") and any(v != 0 for v in build_rollup.get("bad_counters", {}).values()):
        failures.append("build_bad_counter_nonzero")
    if build_profile.get("bad_counters_zero") is not True:
        failures.append("build_profile_bad_counters_wrong")
    if build_summary.get("outcome_class") != "DOMAIN_SHIFT_PASS_WITH_GAPS":
        failures.append("build_summary_outcome_wrong")

    return failures, {
        "decision_summary": decision_summary,
        "fixtures": fixtures,
        "proposals": proposals,
        "builds": builds,
        "verifications": verifications,
        "handoffs": handoffs,
        "edges": edges,
        "feedback": feedback,
        "build_summary": build_summary,
        "build_profile": build_profile,
    }

def find_by(rows: List[Dict[str, Any]], key: str, value: Any) -> List[Dict[str, Any]]:
    return [r for r in rows if r.get(key) == value]

def make_example(example_type: str, title: str, source_refs: List[str], payload: Dict[str, Any], protocol_use: str) -> Dict[str, Any]:
    return {
        "schema_version": "c6_inter_cell_protocol_example_v0",
        "example_id": "c6_example_" + sig8({"type": example_type, "title": title, "source_refs": source_refs, "payload": payload}),
        "example_type": example_type,
        "title": title,
        "source_refs": source_refs,
        "payload": payload,
        "protocol_use": protocol_use,
        "allowed_c6_use": [
            "derive inter-cell message fields",
            "derive review/acceptance boundary fields",
            "derive verification/handoff return fields",
            "derive blocked-build/feedback handling fields",
        ],
        "forbidden_c6_use": [
            "open C6 automatically",
            "treat example as full protocol",
            "claim full transfer",
            "grant general Cell 1 authority",
            "auto-chain builds",
        ],
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    extraction_pass = not failures

    decision_summary = basis.get("decision_summary", {})
    fixtures = basis.get("fixtures", [])
    proposals = basis.get("proposals", [])
    builds = basis.get("builds", [])
    verifications = basis.get("verifications", [])
    handoffs = basis.get("handoffs", [])
    edges = basis.get("edges", [])
    feedback = basis.get("feedback", [])
    build_profile = basis.get("build_profile", {})

    accepted_proposals = [p for p in proposals if p.get("proposal_status") == "ACCEPTED"]
    proposed_only = [p for p in proposals if p.get("proposal_status") == "PROPOSED_ONLY"]
    accepted = accepted_proposals[0] if accepted_proposals else {}
    proposed = proposed_only[0] if proposed_only else {}
    accepted_fixture = accepted.get("fixture_label")
    accepted_proposal_id = accepted.get("proposal_id")
    accepted_verifications = [v for v in verifications if v.get("proposal_id") == accepted_proposal_id]
    accepted_handoffs = [h for h in handoffs if h.get("proposal_id") == accepted_proposal_id]

    examples: List[Dict[str, Any]] = []

    if proposed:
        examples.append(make_example(
            "PROPOSAL_PACKET_PROPOSED_ONLY",
            "Proposed-only bounded extraction request stays non-command",
            [rel(C5_PROPOSAL_PACKETS_PATH)],
            {
                "proposal": proposed,
                "boundary": "proposal packet != accepted command",
                "review_request_is_not_approval": True,
                "cell1_consumption_allowed": False,
            },
            "C6 must represent proposed-only packets distinctly from accepted commands."
        ))

    if accepted:
        examples.append(make_example(
            "ACCEPTED_PROPOSAL_PACKET",
            "Accepted bounded Cell 1 probe proposal",
            [rel(C5_PROPOSAL_PACKETS_PATH)],
            {
                "proposal": accepted,
                "boundary": "review approval exists before Cell 1 consumption",
                "cell1_consumption_allowed": True,
            },
            "C6 must carry accepted proposal scope, review basis, and allowed target surface."
        ))

    if builds:
        examples.append(make_example(
            "CELL1_ACCEPTED_PROPOSAL_CONSUMPTION",
            "Cell 1 consumes exactly one accepted proposal",
            [rel(C5_CELL1_BUILD_RECEIPTS_PATH)],
            {
                "cell1_build_receipt": builds[0],
                "freebuild_count": builds[0].get("freebuild_count"),
                "auto_chain_count": builds[0].get("auto_chain_count"),
                "scope_expansion_count": builds[0].get("scope_expansion_count"),
            },
            "C6 must bind builder execution to accepted proposal scope and zero freebuild/auto-chain counters."
        ))

    if accepted_verifications:
        examples.append(make_example(
            "VERIFICATION_RETURN",
            "Verification receipt returns bounded observation without global truth",
            [rel(C5_VERIFICATION_RECEIPTS_PATH)],
            {
                "verification_receipt": accepted_verifications[0],
                "must_not_infer": accepted_verifications[0].get("must_not_infer", []),
            },
            "C6 must require verification receipts and preserve must-not-infer constraints."
        ))

    if accepted_handoffs:
        examples.append(make_example(
            "HANDOFF_RETURN_TO_CELL0",
            "Cell 1 handoff returns verified bounded result",
            [rel(C5_HANDOFF_RECORDS_PATH)],
            {
                "handoff_record": accepted_handoffs[0],
                "forbidden_next_handling": accepted_handoffs[0].get("forbidden_next_handling", []),
            },
            "C6 must model return-to-Cell0/review instead of auto-chaining new builds."
        ))

    for fb in feedback:
        examples.append(make_example(
            "BLOCKED_OR_TYPED_STOP_FEEDBACK",
            "Typed stop with diagnostic unit feedback: " + str(fb.get("fixture_label")),
            [rel(C5_UNIT_FEEDBACK_PATH)],
            {
                "feedback_record": fb,
                "bare_failed_status": fb.get("bare_failed_status"),
                "blocked_next_moves": fb.get("blocked_next_moves", []),
                "lawful_next_refinement_or_question": fb.get("lawful_next_refinement_or_question"),
            },
            "C6 must preserve blocked-build/typed-stop feedback payloads as returnable inter-cell evidence."
        ))

    selected_edge_handles = [
        "PROPOSE_VALIDATE_EDGE",
        "BUILDER_HANDOFF_EDGE",
        "VERIFICATION_RETURN_EDGE",
        "CAPABILITY_BOUNDARY_EDGE",
        "GUARD_AUTHORITY_EDGE",
    ]
    edge_examples = [e for e in edges if e.get("fixture_label") == accepted_fixture and e.get("edge_handle") in selected_edge_handles]
    for edge in edge_examples:
        examples.append(make_example(
            "DECISION_EDGE_OBSERVATION",
            "Decision edge observation for " + str(edge.get("edge_handle")),
            [rel(C5_EDGE_OBSERVATIONS_PATH)],
            {
                "edge_observation": edge,
            },
            "C6 must use edge observations to preserve visible inter-cell transitions."
        ))

    proposal_examples = {
        "schema_version": "c6_proposal_packet_examples_from_c5_v0",
        "source": rel(C5_PROPOSAL_PACKETS_PATH),
        "proposed_only_examples": proposed_only,
        "accepted_examples": accepted_proposals,
        "distinction": "PROPOSED_ONLY != ACCEPTED",
    }

    accepted_packet_examples = {
        "schema_version": "c6_accepted_review_packet_examples_from_c5_v0",
        "accepted_count": len(accepted_proposals),
        "accepted_packets": accepted_proposals,
        "required_c6_fields": [
            "proposal_id",
            "proposal_status",
            "review_receipt_ref",
            "accepted_status",
            "authority_boundary",
            "payload_boundary",
            "target_surface",
            "verification_contract",
        ],
    }

    cell1_probe_examples = {
        "schema_version": "c6_cell1_probe_examples_from_c5_v0",
        "build_count": len(builds),
        "builds": builds,
        "required_c6_fields": [
            "proposal_id",
            "accepted_status",
            "review_receipt_ref",
            "target_surface",
            "patch_or_probe_ref",
            "verification_receipt_ref",
            "handoff_receipt_ref",
            "scope_expansion_count",
            "freebuild_count",
            "auto_chain_count",
        ],
    }

    verification_examples = {
        "schema_version": "c6_verification_examples_from_c5_v0",
        "verification_count": len(verifications),
        "accepted_path_verifications": accepted_verifications,
        "all_verifications": verifications,
        "must_preserve": ["verification_status", "observed", "must_not_infer"],
    }

    handoff_examples = {
        "schema_version": "c6_handoff_examples_from_c5_v0",
        "handoff_count": len(handoffs),
        "handoffs": handoffs,
        "must_preserve": ["from_cell", "to", "handoff_status", "allowed_next_handling", "forbidden_next_handling"],
    }

    blocked_feedback_examples = {
        "schema_version": "c6_blocked_feedback_examples_from_c5_v0",
        "feedback_count": len(feedback),
        "feedback_records": feedback,
        "must_preserve": [
            "why_failed",
            "where_failed",
            "failed_relative_to_domain_object",
            "failed_relative_to_source_surface",
            "failed_relative_to_boundary",
            "failed_relative_to_missing_capability_or_evidence",
            "blocked_next_moves",
            "lawful_next_refinement_or_question",
        ],
    }

    edge_subset = {
        "schema_version": "c6_edge_observation_examples_from_c5_v0",
        "edge_observation_source_count": len(edges),
        "selected_edge_example_count": len(edge_examples),
        "selected_edge_examples": edge_examples,
        "must_preserve": ["edge_handle", "boundary_type", "blocked_moves", "lawful_next_moves", "parent_return_payload_preserved"],
    }

    protocol_pressure_readout = {
        "schema_version": "c6_protocol_pressure_readout_from_c5_examples_v0",
        "pressure_summary": "C5 examples show C6 needs typed inter-cell packets for proposal, acceptance, builder consumption, verification return, handoff, and blocked feedback.",
        "fields_c6_likely_needs": [
            "source_cell",
            "target_cell",
            "proposal_id",
            "proposal_status",
            "review_receipt_ref",
            "accepted_status",
            "authority_boundary",
            "payload_boundary",
            "target_surface",
            "allowed_inputs",
            "forbidden_inputs",
            "verification_contract",
            "patch_or_probe_ref",
            "verification_receipt_ref",
            "handoff_receipt_ref",
            "blocked_next_moves",
            "lawful_next_refinement_or_question",
            "must_not_infer",
        ],
        "open_questions_for_later_c6_design": [
            "Which fields are required versus optional across all inter-cell packets?",
            "How should C6 represent return-to-review versus return-to-Cell0?",
            "How should a blocked builder path be distinguished from a verified handoff?",
            "How should edge observations attach to inter-cell packet lineage?",
        ],
        "not_a_c6_protocol_design": True,
    }

    extraction_basis = {
        "schema_version": "c6_example_extraction_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if extraction_pass else "BASIS_REPAIR_REQUIRED",
        "source_post_c5_decision_receipt_id": SOURCE_POST_C5_DECISION_RECEIPT_ID,
        "source_c5_reference_closure_receipt_id": SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_ID,
        "source_c5_build_receipt_id": SOURCE_C5_BUILD_RECEIPT_ID,
        "domain_id": "artifact_claim_review_v0",
        "c6_example_extraction_authorized": extraction_pass,
        "selected_next_branch": EXPECTED_SELECTED_BRANCH,
        "reviewed_reference_frozen": True,
        "c6_opened": False,
        "c6_design_executed": False,
    }

    example_schema = {
        "schema_version": "c6_inter_cell_protocol_example_schema_v0",
        "record_schema": {
            "schema_version": "c6_inter_cell_protocol_example_v0",
            "example_id": "c6_example_<sig8>",
            "example_type": None,
            "title": None,
            "source_refs": [],
            "payload": {},
            "protocol_use": None,
            "allowed_c6_use": [],
            "forbidden_c6_use": [],
        },
        "closed_example_types": sorted(set(e["example_type"] for e in examples)),
    }

    example_catalog = {
        "schema_version": "c6_inter_cell_protocol_example_catalog_v0",
        "example_count": len(examples),
        "example_types": sorted(set(e["example_type"] for e in examples)),
        "examples": [
            {
                "example_id": e["example_id"],
                "example_type": e["example_type"],
                "title": e["title"],
                "protocol_use": e["protocol_use"],
            }
            for e in examples
        ],
    }

    review_candidate = {
        "schema_version": "c6_example_extraction_review_candidate_v0",
        "candidate_status": "C6_EXAMPLE_EXTRACTION_REVIEW_READY" if extraction_pass else "C6_EXAMPLE_EXTRACTION_REPAIR_REQUIRED",
        "example_count": len(examples),
        "proposal_examples_extracted": len(proposals),
        "accepted_proposal_examples_extracted": len(accepted_proposals),
        "cell1_probe_examples_extracted": len(builds),
        "verification_examples_extracted": len(verifications),
        "handoff_examples_extracted": len(handoffs),
        "blocked_feedback_examples_extracted": len(feedback),
        "edge_examples_extracted": len(edge_examples),
        "review_should_check": [
            "examples are extracted from C5 reviewed reference only",
            "proposed-only and accepted proposal examples remain distinct",
            "Cell 1 example consumes accepted proposal only",
            "verification and handoff return are preserved",
            "blocked feedback is diagnostic",
            "C6 not opened and not designed in extraction",
        ],
    }

    authority_boundary = {
        "schema_version": "c6_example_extraction_authority_boundary_v0",
        "status": "TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_REVIEW_READY" if extraction_pass else "TYPED_C6_EXAMPLE_EXTRACTION_GATE_FAIL",
        "may_review_examples_next": extraction_pass,
        "may_open_c6_now": False,
        "may_design_c6_protocol_now": False,
        "may_execute_c6_protocol_now": False,
        "may_execute_new_domain_shift": False,
        "may_mutate_c5_reference": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_claim_transfer": False,
        "may_claim_global_autonomy": False,
        "may_grant_general_cell1_authority": False,
    }

    classification = {
        "schema_version": "c6_example_extraction_classification_v0",
        "classification_status": authority_boundary["status"],
        "c6_example_extraction_complete": extraction_pass,
        "c6_example_extraction_review_ready": extraction_pass,
        "examples_extracted": len(examples),
        "example_types_extracted": sorted(set(e["example_type"] for e in examples)),
        "proposal_packet_examples_extracted": len(proposals),
        "accepted_packet_examples_extracted": len(accepted_proposals),
        "cell1_probe_examples_extracted": len(builds),
        "verification_examples_extracted": len(verifications),
        "handoff_examples_extracted": len(handoffs),
        "blocked_feedback_examples_extracted": len(feedback),
        "edge_examples_extracted": len(edge_examples),
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
        "recommended_next": RECOMMENDED_NEXT if extraction_pass else "REPAIR_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_V0",
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "c6_example_extraction_rollup_v0",
        "extraction_count": 1 if extraction_pass else 0,
        "examples_extracted": len(examples),
        "proposal_packet_examples": len(proposals),
        "accepted_packet_examples": len(accepted_proposals),
        "cell1_probe_examples": len(builds),
        "verification_examples": len(verifications),
        "handoff_examples": len(handoffs),
        "blocked_feedback_examples": len(feedback),
        "edge_examples": len(edge_examples),
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
        "recommended_next": RECOMMENDED_NEXT if extraction_pass else "REPAIR_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_V0",
    }

    zero_keys = [
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

    profile = {
        "schema_version": "c6_example_extraction_profile_v0",
        "profile_id": "c6_example_extraction_" + sig8(rollup),
        "status": authority_boundary["status"],
        "examples_extracted": len(examples),
        "example_catalog_ref": rel(EXAMPLE_CATALOG_PATH),
        "protocol_pressure_readout_ref": rel(PROTOCOL_PRESSURE_READOUT_PATH),
        "review_ready": extraction_pass,
        "bad_counters_zero": all(rollup[k] == 0 for k in zero_keys),
        "c6_opened": False,
        "c6_design_executed": False,
        "c6_protocol_emitted": False,
        "recommendation": "Review extracted C5-to-C6 examples before designing any C6 protocol.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "c6_example_extraction_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": authority_boundary["status"],
        "receipt_backed_claim": "Extracted concrete C5-to-C6 inter-cell protocol examples from the reviewed C5 reference: proposed-only packet, accepted proposal, Cell 1 bounded probe, verification return, handoff return, diagnostic blocked feedback, and decision-edge observations. C6 was not opened or designed.",
        "examples_extracted": len(examples),
        "recommended_next_handling": RECOMMENDED_NEXT if extraction_pass else "REPAIR_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_V0",
    }

    trace = {
        "schema_version": "c6_example_extraction_transition_trace_v0",
        "trace": [
            {
                "step": "consume_post_c5_decision",
                "question": "is C6 example extraction authorized next",
                "answer": "yes" if extraction_pass else "no",
                "taken": "read reviewed C5 reference and C5 build artifacts",
            },
            {
                "step": "extract_inter_cell_examples",
                "question": "which C5 examples should C6 consume later",
                "answer": "proposal, acceptance, Cell1 probe, verification, handoff, feedback, edge observations",
                "taken": "emit example catalog and typed examples",
            },
            {
                "step": "preserve_no_c6_open_boundary",
                "question": "does extraction open or design C6",
                "answer": "no",
                "taken": "emit review-ready extraction object",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + authority_boundary["status"],
            "next_command_goal": None,
        },
    }

    artifacts = [
        (EXTRACTION_BASIS_PATH, extraction_basis),
        (EXAMPLE_SCHEMA_PATH, example_schema),
        (EXAMPLE_CATALOG_PATH, example_catalog),
        (PROPOSAL_EXAMPLES_PATH, proposal_examples),
        (ACCEPTED_PACKET_EXAMPLES_PATH, accepted_packet_examples),
        (CELL1_PROBE_EXAMPLES_PATH, cell1_probe_examples),
        (VERIFICATION_EXAMPLES_PATH, verification_examples),
        (HANDOFF_EXAMPLES_PATH, handoff_examples),
        (BLOCKED_FEEDBACK_EXAMPLES_PATH, blocked_feedback_examples),
        (EDGE_EXAMPLES_PATH, edge_subset),
        (PROTOCOL_PRESSURE_READOUT_PATH, protocol_pressure_readout),
        (REVIEW_CANDIDATE_PATH, review_candidate),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (CLASSIFICATION_PATH, classification),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRACE_PATH, trace),
    ]
    for path, obj in artifacts:
        write_json(path, obj)
    write_jsonl(EXAMPLES_JSONL_PATH, examples)

    if len(examples) < 10:
        failures.append(f"example_count_too_low:{len(examples)}")
    if not accepted_proposals:
        failures.append("no_accepted_proposal_example")
    if not proposed_only:
        failures.append("no_proposed_only_example")
    if not builds:
        failures.append("no_cell1_probe_example")
    if not accepted_verifications:
        failures.append("no_accepted_verification_example")
    if not handoffs:
        failures.append("no_handoff_example")
    if not feedback:
        failures.append("no_feedback_example")
    if not edge_examples:
        failures.append("no_edge_examples")

    acceptance_gate_results = {
        "C6_EXTRACT_0_POST_C5_DECISION_RECEIPT_CONSUMED": SOURCE_POST_C5_DECISION_RECEIPT_PATH.exists(),
        "C6_EXTRACT_1_AUTHORIZATION_CONSUMED": C6_EXTRACTION_AUTH_PATH.exists(),
        "C6_EXTRACT_2_REVIEWED_C5_REFERENCE_CONSUMED": C5_REVIEWED_REFERENCE_PATH.exists(),
        "C6_EXTRACT_3_EXAMPLE_SCHEMA_EMITTED": EXAMPLE_SCHEMA_PATH.exists(),
        "C6_EXTRACT_4_EXAMPLES_JSONL_EMITTED": EXAMPLES_JSONL_PATH.exists() and len(examples) >= 10,
        "C6_EXTRACT_5_PROPOSAL_EXAMPLES_EXTRACTED": len(proposals) == 2,
        "C6_EXTRACT_6_ACCEPTED_PACKET_EXAMPLE_EXTRACTED": len(accepted_proposals) == 1,
        "C6_EXTRACT_7_CELL1_PROBE_EXAMPLE_EXTRACTED": len(builds) == 1,
        "C6_EXTRACT_8_VERIFICATION_EXAMPLES_EXTRACTED": len(verifications) == 5,
        "C6_EXTRACT_9_HANDOFF_EXAMPLE_EXTRACTED": len(handoffs) == 1,
        "C6_EXTRACT_10_BLOCKED_FEEDBACK_EXAMPLES_EXTRACTED": len(feedback) == 2,
        "C6_EXTRACT_11_EDGE_EXAMPLES_EXTRACTED": len(edge_examples) >= 5,
        "C6_EXTRACT_12_PROTOCOL_PRESSURE_READOUT_EMITTED": PROTOCOL_PRESSURE_READOUT_PATH.exists(),
        "C6_EXTRACT_13_REVIEW_CANDIDATE_READY": review_candidate["candidate_status"] == "C6_EXAMPLE_EXTRACTION_REVIEW_READY",
        "C6_EXTRACT_14_NO_C6_OPENED": classification["c6_opened"] is False,
        "C6_EXTRACT_15_NO_C6_DESIGN_EXECUTED": classification["c6_design_executed"] is False,
        "C6_EXTRACT_16_NO_C6_PROTOCOL_EMITTED": classification["c6_protocol_emitted"] is False,
        "C6_EXTRACT_17_NO_SOURCE_OR_PRIOR_RECEIPT_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False,
        "C6_EXTRACT_18_NO_C5_REFERENCE_MUTATION": classification["c5_reference_mutated"] is False,
        "C6_EXTRACT_19_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False,
        "C6_EXTRACT_20_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C6_EXTRACT_21_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "C6_EXTRACT_22_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_REVIEW_READY" if gate == "PASS" else "TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if gate == "PASS" else "REPAIR_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": status,
        "gate": gate,
        "examples": len(examples),
        "source_decision": SOURCE_POST_C5_DECISION_RECEIPT_ID,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "c6_example_extraction_from_c5_reference_receipt_v0",
        "receipt_type": "TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_post_c5_decision_receipt_id": SOURCE_POST_C5_DECISION_RECEIPT_ID,
        "source_c5_reference_closure_receipt_id": SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_ID,
        "machine_readable_c6_example_extraction_summary": {
            "status": status,
            "c6_example_extraction_complete": gate == "PASS",
            "c6_example_extraction_review_ready": gate == "PASS",
            "examples_extracted": len(examples),
            "proposal_packet_examples_extracted": len(proposals),
            "accepted_packet_examples_extracted": len(accepted_proposals),
            "cell1_probe_examples_extracted": len(builds),
            "verification_examples_extracted": len(verifications),
            "handoff_examples_extracted": len(handoffs),
            "blocked_feedback_examples_extracted": len(feedback),
            "edge_examples_extracted": len(edge_examples),
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
            "recommended_next": recommended_next,
        },
        "aggregate_metrics": report | {"status": status, "recommended_next_handling": recommended_next},
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "extraction_basis": rel(EXTRACTION_BASIS_PATH),
            "example_schema": rel(EXAMPLE_SCHEMA_PATH),
            "examples_jsonl": rel(EXAMPLES_JSONL_PATH),
            "example_catalog": rel(EXAMPLE_CATALOG_PATH),
            "proposal_examples": rel(PROPOSAL_EXAMPLES_PATH),
            "accepted_packet_examples": rel(ACCEPTED_PACKET_EXAMPLES_PATH),
            "cell1_probe_examples": rel(CELL1_PROBE_EXAMPLES_PATH),
            "verification_examples": rel(VERIFICATION_EXAMPLES_PATH),
            "handoff_examples": rel(HANDOFF_EXAMPLES_PATH),
            "blocked_feedback_examples": rel(BLOCKED_FEEDBACK_EXAMPLES_PATH),
            "edge_examples": rel(EDGE_EXAMPLES_PATH),
            "protocol_pressure_readout": rel(PROTOCOL_PRESSURE_READOUT_PATH),
            "review_candidate": rel(REVIEW_CANDIDATE_PATH),
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
    print(f"c6_example_extraction_receipt_id={receipt_id}")
    print(f"c6_example_extraction_receipt_path={rel(receipt_path)}")
    print(f"c6_examples_jsonl_path={rel(EXAMPLES_JSONL_PATH)}")
    print(f"c6_example_catalog_path={rel(EXAMPLE_CATALOG_PATH)}")
    print(f"c6_protocol_pressure_readout_path={rel(PROTOCOL_PRESSURE_READOUT_PATH)}")
    print(f"c6_example_extraction_rollup_path={rel(ROLLUP_PATH)}")
    print(f"c6_example_extraction_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
