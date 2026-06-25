#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_AFTER_C5_FULL_DOMAIN_SHIFT_TRANSITION_REFERENCE_CLOSURE_V0"
TARGET_UNIT_ID = "domain_shift.post_c5_reference_decision.v0"
LAYER = "OUTER / DOMAIN_SHIFT_TRANSITION / POST_REFERENCE_DECISION"
MODE = "DECIDE_ONLY / SELECT_C6_EXAMPLE_EXTRACTION / NO_C6_OPENING"
BUILD_MODE = "POST_C5_DOMAIN_SHIFT_REFERENCE_DECISION_ONLY"

SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_ID = "934363ba"
SOURCE_C5_BUILD_RECEIPT_ID = "b4acefb6"
SOURCE_C5_REVIEW_RECEIPT_ID = "efc12ac0"

SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0_receipts/934363ba.json"

C5_REVIEWED_REFERENCE_PATH = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0/c5_domain_shift_reviewed_reference_v0.json"
C5_FREEZE_MANIFEST_PATH = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0/c5_domain_shift_reviewed_reference_freeze_manifest_v0.json"
C5_REFERENCE_INDEX_PATH = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0/c5_domain_shift_reviewed_reference_index_v0.json"
C5_PASS_WITH_GAPS_REFERENCE_PATH = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0/c5_domain_shift_pass_with_gaps_reference_v0.json"
C5_GAP_REFERENCE_PATH = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0/c5_domain_shift_gap_reference_v0.json"
C5_NEXT_DECISION_READY_PATH = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0/c5_post_domain_shift_reference_decision_ready_v0.json"
C5_REFERENCE_AUTHORITY_PATH = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0/c5_domain_shift_reference_closure_authority_boundary_v0.json"
C5_REFERENCE_CLASSIFICATION_PATH = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0/c5_domain_shift_reference_closure_classification_v0.json"
C5_REFERENCE_ROLLUP_PATH = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0/c5_domain_shift_reference_closure_rollup_v0.json"
C5_REFERENCE_PROFILE_PATH = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0/c5_domain_shift_reference_closure_profile_v0.json"
C5_REFERENCE_REPORT_PATH = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0/c5_domain_shift_reference_closure_report.json"
C5_REFERENCE_TRACE_PATH = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0/c5_domain_shift_reference_closure_transition_trace.json"

C5_BUILD_RECEIPT_PATH = ROOT / "data/c5_full_domain_shift_transition_v0_receipts/b4acefb6.json"
C5_REVIEW_RECEIPT_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0_receipts/efc12ac0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_PATH,
    C5_REVIEWED_REFERENCE_PATH,
    C5_FREEZE_MANIFEST_PATH,
    C5_REFERENCE_INDEX_PATH,
    C5_PASS_WITH_GAPS_REFERENCE_PATH,
    C5_GAP_REFERENCE_PATH,
    C5_NEXT_DECISION_READY_PATH,
    C5_REFERENCE_AUTHORITY_PATH,
    C5_REFERENCE_CLASSIFICATION_PATH,
    C5_REFERENCE_ROLLUP_PATH,
    C5_REFERENCE_PROFILE_PATH,
    C5_REFERENCE_REPORT_PATH,
    C5_REFERENCE_TRACE_PATH,
    C5_BUILD_RECEIPT_PATH,
    C5_REVIEW_RECEIPT_PATH,
]

OUT_DIR = ROOT / "data/c5_post_domain_shift_reference_decision_v0"
RECEIPT_DIR = ROOT / "data/c5_post_domain_shift_reference_decision_v0_receipts"

DECISION_BASIS_PATH = OUT_DIR / "c5_post_reference_decision_basis_v0.json"
DECISION_OPTIONS_PATH = OUT_DIR / "c5_post_reference_decision_options_v0.json"
SELECTED_BRANCH_PATH = OUT_DIR / "c5_post_reference_selected_branch_v0.json"
C6_EXAMPLE_EXTRACTION_AUTH_PATH = OUT_DIR / "c6_example_extraction_authorization_from_c5_reference_v0.json"
C5_REFERENCE_CONTINUATION_PATH = OUT_DIR / "c5_reference_continuation_for_c6_examples_v0.json"
DEFERRED_BRANCHES_PATH = OUT_DIR / "c5_post_reference_deferred_branches_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "c5_post_reference_decision_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "c5_post_reference_decision_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "c5_post_reference_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c5_post_reference_decision_profile_v0.json"
REPORT_PATH = OUT_DIR / "c5_post_reference_decision_report.json"
TRACE_PATH = OUT_DIR / "c5_post_reference_decision_transition_trace.json"

EXPECTED_SOURCE_STATUS = "TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY"
EXPECTED_SOURCE_STOP = "STOP_TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY"
EXPECTED_SOURCE_NEXT = "DECIDE_NEXT_AFTER_C5_FULL_DOMAIN_SHIFT_TRANSITION_REFERENCE_CLOSURE_V0"

SELECTED_BRANCH = "EXTRACT_C5_TO_C6_INTER_CELL_PROTOCOL_EXAMPLES_FROM_REVIEWED_REFERENCE"
SELECTED_NEXT_UNIT = "EXTRACT_C5_TO_C6_INTER_CELL_PROTOCOL_EXAMPLES_FROM_REVIEWED_REFERENCE_V0"

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

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{rel(path)}")
    if failures:
        return failures, {}

    closure_receipt = read_json(SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_PATH)
    closure_summary = closure_receipt.get("machine_readable_c5_full_domain_shift_transition_reference_closure_summary", {})

    reviewed_reference = read_json(C5_REVIEWED_REFERENCE_PATH)
    freeze_manifest = read_json(C5_FREEZE_MANIFEST_PATH)
    reference_index = read_json(C5_REFERENCE_INDEX_PATH)
    pass_with_gaps_reference = read_json(C5_PASS_WITH_GAPS_REFERENCE_PATH)
    gap_reference = read_json(C5_GAP_REFERENCE_PATH)
    decision_ready = read_json(C5_NEXT_DECISION_READY_PATH)
    authority = read_json(C5_REFERENCE_AUTHORITY_PATH)
    classification = read_json(C5_REFERENCE_CLASSIFICATION_PATH)
    rollup = read_json(C5_REFERENCE_ROLLUP_PATH)
    profile = read_json(C5_REFERENCE_PROFILE_PATH)
    report = read_json(C5_REFERENCE_REPORT_PATH)
    trace = read_json(C5_REFERENCE_TRACE_PATH)

    build_receipt = read_json(C5_BUILD_RECEIPT_PATH)
    review_receipt = read_json(C5_REVIEW_RECEIPT_PATH)

    if closure_receipt.get("receipt_id") != SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_ID or closure_receipt.get("gate") != "PASS":
        failures.append("source_c5_reference_closure_receipt_not_pass")
    if closure_receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_c5_reference_stop_wrong")
    if closure_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_c5_reference_hidden_next")
    if closure_summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_c5_reference_status_wrong:{closure_summary.get('status')}")
    if closure_summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_c5_reference_next_wrong:{closure_summary.get('recommended_next')}")

    for key in [
        "c5_domain_shift_closed_as_reviewed_reference",
        "reviewed_reference_frozen",
        "post_c5_reference_decision_ready",
        "bad_counters_zero",
        "local_decision_grammar_survived",
    ]:
        if closure_summary.get(key) is not True:
            failures.append(f"closure_summary_required_true_missing:{key}")

    expected_counts = {
        "fixtures_total": 5,
        "fixtures_passed": 3,
        "fixtures_blocked": 2,
        "cell0_loop_runs": 5,
        "cell1_builds_attempted": 1,
        "cell1_builds_verified": 1,
        "proposal_packets_emitted": 2,
        "proposal_packets_accepted": 1,
        "typed_stops": 2,
        "edge_observations_emitted": 45,
        "unit_feedback_records_emitted": 2,
    }
    for key, expected in expected_counts.items():
        if closure_summary.get(key) != expected:
            failures.append(f"closure_count_wrong:{key}:{closure_summary.get(key)}")

    if closure_summary.get("domain_id") != "artifact_claim_review_v0":
        failures.append("closure_domain_wrong")
    if closure_summary.get("outcome_class") != "DOMAIN_SHIFT_PASS_WITH_GAPS":
        failures.append("closure_outcome_wrong")
    if closure_summary.get("dominant_gap_class") != "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL":
        failures.append("closure_gap_wrong")

    for key in [
        "new_domain_executed_in_closure",
        "domain_shift_pass_claimed",
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
        if closure_summary.get(key) is not False:
            failures.append(f"closure_forbidden_true:{key}")

    for key in [
        "cell1_freebuild_count",
        "cell1_auto_chain_count",
        "unbounded_payload_inspection_count",
        "proposal_applied_without_review_count",
    ]:
        if closure_summary.get(key) != 0:
            failures.append(f"closure_forbidden_count_nonzero:{key}:{closure_summary.get(key)}")

    if reviewed_reference.get("reference_status") != "C5_DOMAIN_SHIFT_REVIEWED_REFERENCE_FROZEN":
        failures.append("reviewed_reference_not_frozen")
    if reviewed_reference.get("outcome_class") != "DOMAIN_SHIFT_PASS_WITH_GAPS":
        failures.append("reviewed_reference_outcome_wrong")
    if freeze_manifest.get("freeze_status") != "FROZEN":
        failures.append("freeze_manifest_not_frozen")
    if reference_index.get("index_status") != "REFERENCE_INDEX_EMITTED":
        failures.append("reference_index_wrong")
    if pass_with_gaps_reference.get("reference_status") != "PASS_WITH_GAPS_CONFIRMED_AND_FROZEN":
        failures.append("pass_with_gaps_reference_wrong")
    if pass_with_gaps_reference.get("local_decision_grammar_survived") is not True:
        failures.append("pass_with_gaps_grammar_not_survived")
    if gap_reference.get("gap_status") != "BOUNDED_GAP_FROZEN":
        failures.append("gap_reference_wrong")
    if decision_ready.get("decision_ready") is not True or decision_ready.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append("decision_ready_wrong")
    if authority.get("may_decide_next_after_c5_reference_closure") is not True:
        failures.append("authority_no_decide")
    for forbidden in [
        "may_open_c6_now_in_closure",
        "may_execute_new_domain_shift_now_in_closure",
        "may_claim_transfer",
        "may_claim_research_lab_readiness",
        "may_claim_global_autonomy",
        "may_grant_general_cell1_authority",
        "may_mutate_source",
        "may_mutate_prior_receipts",
    ]:
        if authority.get(forbidden) is not False:
            failures.append(f"authority_forbidden_true:{forbidden}")
    if classification.get("post_c5_reference_decision_ready") is not True:
        failures.append("classification_decision_not_ready")
    if rollup.get("post_c5_reference_decision_ready_count") != 1:
        failures.append("rollup_decision_ready_wrong")
    if profile.get("post_c5_reference_decision_ready") is not True or profile.get("next_command_goal") is not None:
        failures.append("profile_wrong")
    if report.get("recommended_next_handling") != EXPECTED_SOURCE_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_hidden_next")
    if build_receipt.get("receipt_id") != SOURCE_C5_BUILD_RECEIPT_ID or build_receipt.get("gate") != "PASS":
        failures.append("build_receipt_wrong")
    if review_receipt.get("receipt_id") != SOURCE_C5_REVIEW_RECEIPT_ID or review_receipt.get("gate") != "PASS":
        failures.append("review_receipt_wrong")

    return failures, {"closure_summary": closure_summary, "reviewed_reference": reviewed_reference}

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    decision_pass = not failures
    status = "TYPED_C5_POST_REFERENCE_DECISION_SELECTED_C6_EXAMPLE_EXTRACTION_READY" if decision_pass else "TYPED_C5_POST_REFERENCE_DECISION_GATE_FAIL"
    recommended_next = SELECTED_NEXT_UNIT if decision_pass else "REPAIR_C5_POST_REFERENCE_DECISION_V0"

    closure_summary = basis.get("closure_summary", {})

    reason_codes = [
        "POST_C5_REFERENCE_DECISION_COMPLETE",
        "C5_REFERENCE_CLOSURE_RECEIPT_CONSUMED",
        "C5_REVIEWED_REFERENCE_CONFIRMED",
        "PASS_WITH_GAPS_REFERENCE_CONFIRMED",
        "BOUNDED_GAP_REFERENCE_CONFIRMED",
        "C6_EXAMPLE_EXTRACTION_SELECTED_NEXT",
        "C6_NOT_OPENED_IN_DECISION",
        "C6_DESIGN_NOT_EXECUTED_IN_DECISION",
        "NO_NEW_DOMAIN_SHIFT_EXECUTED",
        "NO_TRANSFER_CLAIM",
        "NO_RESEARCH_LAB_CLAIM",
        "NO_GLOBAL_AUTONOMY_CLAIM",
        "NO_GENERAL_CELL1_AUTHORITY_CLAIM",
        "NO_SOURCE_MUTATION",
        "NO_PRIOR_RECEIPT_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if decision_pass else failures

    decision_basis = {
        "schema_version": "c5_post_reference_decision_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if decision_pass else "BASIS_REPAIR_REQUIRED",
        "source_c5_reference_closure_receipt_id": SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_ID,
        "domain_id": "artifact_claim_review_v0",
        "outcome_class": "DOMAIN_SHIFT_PASS_WITH_GAPS",
        "dominant_gap_class": "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL",
        "reviewed_reference_frozen": True,
        "post_c5_reference_decision_ready": True,
        "c5_examples_available_for_c6": True,
        "example_surfaces_available": [
            "proposal packet sent to Cell 1",
            "accepted command / review packet",
            "Cell 1 bounded probe record",
            "verification receipt",
            "handoff receipt",
            "typed stop with useful feedback",
            "return-to-review payload candidate",
        ],
    }

    decision_options = {
        "schema_version": "c5_post_reference_decision_options_v0",
        "decision_status": "NEXT_BRANCH_SELECTED" if decision_pass else "NO_BRANCH_SELECTED",
        "options": [
            {
                "branch": SELECTED_BRANCH,
                "selected": decision_pass,
                "next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
                "why": "C5 produced concrete proposal, accepted Cell 1, verification, handoff, edge, and feedback examples; C6 should consume examples before protocol design.",
            },
            {
                "branch": "DESIGN_C6_INTER_CELL_PROTOCOL_DIRECTLY",
                "selected": False,
                "next_unit": None,
                "why": "Too much. First extract the C5 examples that C6 should consume.",
            },
            {
                "branch": "REFINE_C5_BOUNDED_EVIDENCE_PROPOSAL_HANDLING",
                "selected": False,
                "next_unit": None,
                "why": "The dominant gap is useful, but the immediate next reusable object is the C5-to-C6 example surface.",
            },
            {
                "branch": "RUN_ADDITIONAL_DOMAIN_SHIFT_SLICE",
                "selected": False,
                "next_unit": None,
                "why": "No additional slice is needed before extracting the first C6 protocol examples.",
            },
            {
                "branch": "CLOSE_AND_RETURN_TO_OBSERVATION_HARDENING",
                "selected": False,
                "next_unit": None,
                "why": "Reference is closed, but it now exposes concrete inter-cell examples worth freezing.",
            },
        ],
    }

    selected_branch = {
        "schema_version": "c5_post_reference_selected_branch_v0",
        "selected_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "selection_scope": "example extraction from reviewed C5 reference for later C6 inter-cell protocol design",
        "selection_does_not": [
            "open C6",
            "design C6",
            "execute new domain shift",
            "claim full transfer",
            "claim research-lab readiness",
            "grant general Cell 1 authority",
            "mutate source",
            "mutate prior receipts",
        ],
    }

    c6_example_auth = {
        "schema_version": "c6_example_extraction_authorization_from_c5_reference_v0",
        "authorization_status": "C6_EXAMPLE_EXTRACTION_AUTHORIZED_NEXT" if decision_pass else "NOT_AUTHORIZED",
        "authorized_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "authorized_scope": [
            "consume reviewed C5 reference closure receipt",
            "extract concrete inter-cell examples from C5 artifacts",
            "preserve proposal packet, accepted review packet, Cell 1 probe, verification, handoff, blocked/typed feedback examples",
            "emit review-ready C6 example surface",
        ],
        "not_authorized_in_this_decision": [
            "open C6",
            "design full C6 protocol",
            "execute another domain shift",
            "auto-chain Cell 1 builds",
            "claim transfer",
            "claim global autonomy",
        ],
    }

    c5_reference_continuation = {
        "schema_version": "c5_reference_continuation_for_c6_examples_v0",
        "reference_status": "C5_REVIEWED_REFERENCE_AVAILABLE_FOR_EXAMPLE_EXTRACTION",
        "source_reference_closure_receipt_id": SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_ID,
        "domain_id": "artifact_claim_review_v0",
        "outcome_class": "DOMAIN_SHIFT_PASS_WITH_GAPS",
        "fixtures_total": closure_summary.get("fixtures_total"),
        "proposal_packets_emitted": closure_summary.get("proposal_packets_emitted"),
        "proposal_packets_accepted": closure_summary.get("proposal_packets_accepted"),
        "cell1_builds_attempted": closure_summary.get("cell1_builds_attempted"),
        "cell1_builds_verified": closure_summary.get("cell1_builds_verified"),
        "edge_observations_emitted": closure_summary.get("edge_observations_emitted"),
        "unit_feedback_records_emitted": closure_summary.get("unit_feedback_records_emitted"),
    }

    deferred_branches = {
        "schema_version": "c5_post_reference_deferred_branches_v0",
        "deferred": [
            "DESIGN_C6_INTER_CELL_PROTOCOL_DIRECTLY",
            "OPEN_C6",
            "RUN_ADDITIONAL_DOMAIN_SHIFT_SLICE",
            "REFINE_C5_EVIDENCE_PROPOSAL_HANDLING",
            "CLAIM_TRANSFER",
            "CLAIM_RESEARCH_READINESS",
            "GRANT_GENERAL_CELL1_AUTHORITY",
        ],
        "why": "The selected edge is only example extraction from the reviewed C5 reference.",
    }

    authority_boundary = {
        "schema_version": "c5_post_reference_decision_authority_boundary_v0",
        "status": status,
        "may_execute_c6_example_extraction_next": decision_pass,
        "may_open_c6_now_in_decision": False,
        "may_design_c6_now_in_decision": False,
        "may_execute_new_domain_shift_now_in_decision": False,
        "may_claim_transfer": False,
        "may_claim_research_lab_readiness": False,
        "may_claim_global_autonomy": False,
        "may_grant_general_cell1_authority": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
    }

    classification = {
        "schema_version": "c5_post_reference_decision_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "post_c5_reference_decision_complete": decision_pass,
        "selected_next_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": recommended_next,
        "c6_example_extraction_authorized_next": decision_pass,
        "c6_opened": False,
        "c6_design_executed": False,
        "c6_example_extraction_executed_in_decision": False,
        "new_domain_shift_executed": False,
        "domain_id": "artifact_claim_review_v0",
        "outcome_class": "DOMAIN_SHIFT_PASS_WITH_GAPS",
        "dominant_gap_class": "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL",
        "reviewed_reference_frozen": True,
        "post_c5_reference_decision_ready": True,
        "fixtures_total": closure_summary.get("fixtures_total"),
        "cell1_builds_verified": closure_summary.get("cell1_builds_verified"),
        "proposal_packets_emitted": closure_summary.get("proposal_packets_emitted"),
        "proposal_packets_accepted": closure_summary.get("proposal_packets_accepted"),
        "edge_observations_emitted": closure_summary.get("edge_observations_emitted"),
        "unit_feedback_records_emitted": closure_summary.get("unit_feedback_records_emitted"),
        "bad_counters_zero": True,
        "full_transfer_claimed": False,
        "research_lab_readiness_claimed": False,
        "global_autonomy_claimed": False,
        "general_cell1_authority_claimed": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "c5_post_reference_decision_rollup_v0",
        "decision_count": 1 if decision_pass else 0,
        "selected_c6_example_extraction_count": 1 if decision_pass else 0,
        "c6_example_extraction_authorized_next_count": 1 if decision_pass else 0,
        "c6_opened_count": 0,
        "c6_design_executed_count": 0,
        "c6_example_extraction_executed_in_decision_count": 0,
        "new_domain_shift_executed_count": 0,
        "reviewed_reference_frozen_count": 1,
        "post_c5_reference_decision_ready_count": 1,
        "fixtures_total": closure_summary.get("fixtures_total"),
        "proposal_packets_emitted": closure_summary.get("proposal_packets_emitted"),
        "proposal_packets_accepted": closure_summary.get("proposal_packets_accepted"),
        "cell1_builds_verified": closure_summary.get("cell1_builds_verified"),
        "edge_observations_emitted": closure_summary.get("edge_observations_emitted"),
        "unit_feedback_records_emitted": closure_summary.get("unit_feedback_records_emitted"),
        "full_transfer_claim_count": 0,
        "research_lab_readiness_claim_count": 0,
        "global_autonomy_claim_count": 0,
        "general_cell1_authority_claim_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    zero_keys = [
        "c6_opened_count",
        "c6_design_executed_count",
        "c6_example_extraction_executed_in_decision_count",
        "new_domain_shift_executed_count",
        "full_transfer_claim_count",
        "research_lab_readiness_claim_count",
        "global_autonomy_claim_count",
        "general_cell1_authority_claim_count",
        "source_mutated_count",
        "prior_receipt_mutated_count",
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "c5_post_reference_decision_profile_v0",
        "profile_id": "c5_post_reference_decision_" + sig8(rollup),
        "status": status,
        "selected_next_unit": recommended_next,
        "decision": "extract C5-to-C6 inter-cell protocol examples from reviewed C5 reference",
        "domain_id": "artifact_claim_review_v0",
        "outcome_class": "DOMAIN_SHIFT_PASS_WITH_GAPS",
        "bad_counters_zero": all(rollup[k] == 0 for k in zero_keys),
        "c6_opened": False,
        "c6_design_executed": False,
        "recommendation": "Run the C5-to-C6 example extraction unit next. Do not open or design C6 in this decision.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "c5_post_reference_decision_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The post-C5 decision selected C5-to-C6 inter-cell protocol example extraction as the next branch. It did not open C6, design C6, execute another domain shift, or claim transfer/autonomy/general Cell 1 authority.",
        "selected_next_unit": recommended_next,
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "c5_post_reference_decision_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c5_reference_closure",
                "question": "is the C5 pass-with-gaps reference frozen and decision-ready",
                "answer": "yes" if decision_pass else "no",
                "taken": "evaluate next branch",
            },
            {
                "step": "select_c6_example_extraction",
                "question": "what should consume the C5 reference first",
                "answer": SELECTED_NEXT_UNIT if decision_pass else recommended_next,
                "taken": "authorize example extraction only",
            },
            {
                "step": "preserve_no_c6_open_boundary",
                "question": "does this decision open or design C6",
                "answer": "no",
                "taken": "stop with selected next unit",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (DECISION_BASIS_PATH, decision_basis),
        (DECISION_OPTIONS_PATH, decision_options),
        (SELECTED_BRANCH_PATH, selected_branch),
        (C6_EXAMPLE_EXTRACTION_AUTH_PATH, c6_example_auth),
        (C5_REFERENCE_CONTINUATION_PATH, c5_reference_continuation),
        (DEFERRED_BRANCHES_PATH, deferred_branches),
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
        "POST_C5_DECISION_0_REFERENCE_CLOSURE_RECEIPT_CONSUMED": SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_PATH.exists(),
        "POST_C5_DECISION_1_DECISION_BASIS_EMITTED": DECISION_BASIS_PATH.exists(),
        "POST_C5_DECISION_2_REVIEWED_REFERENCE_CONFIRMED": decision_basis["reviewed_reference_frozen"] is True,
        "POST_C5_DECISION_3_OPTIONS_EMITTED": DECISION_OPTIONS_PATH.exists(),
        "POST_C5_DECISION_4_C6_EXAMPLE_EXTRACTION_SELECTED": selected_branch["selected_next_unit"] == SELECTED_NEXT_UNIT,
        "POST_C5_DECISION_5_C6_EXAMPLE_EXTRACTION_AUTHORIZED_NEXT": c6_example_auth["authorized_next_unit"] == SELECTED_NEXT_UNIT,
        "POST_C5_DECISION_6_NO_C6_OPENED_IN_DECISION": classification["c6_opened"] is False,
        "POST_C5_DECISION_7_NO_C6_DESIGN_EXECUTED_IN_DECISION": classification["c6_design_executed"] is False,
        "POST_C5_DECISION_8_NO_EXAMPLE_EXTRACTION_EXECUTED_IN_DECISION": classification["c6_example_extraction_executed_in_decision"] is False,
        "POST_C5_DECISION_9_NO_NEW_DOMAIN_SHIFT": classification["new_domain_shift_executed"] is False,
        "POST_C5_DECISION_10_NO_TRANSFER_RESEARCH_AUTONOMY_GENERAL_AUTHORITY_CLAIMS": classification["full_transfer_claimed"] is False and classification["research_lab_readiness_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False,
        "POST_C5_DECISION_11_NO_SOURCE_OR_PRIOR_RECEIPT_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False,
        "POST_C5_DECISION_12_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "POST_C5_DECISION_13_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "POST_C5_DECISION_14_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_C5_POST_REFERENCE_DECISION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": status,
        "gate": gate,
        "selected_next_unit": recommended_next,
        "c6_opened": False,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "c5_post_domain_shift_reference_decision_receipt_v0",
        "receipt_type": "TYPED_C5_POST_DOMAIN_SHIFT_REFERENCE_DECISION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_c5_reference_closure_receipt_id": SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_ID,
        "machine_readable_c5_post_reference_decision_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "post_c5_reference_decision_complete": decision_pass,
            "selected_next_branch": SELECTED_BRANCH if decision_pass else None,
            "selected_next_unit": recommended_next,
            "c6_example_extraction_authorized_next": decision_pass,
            "c6_opened": False,
            "c6_design_executed": False,
            "c6_example_extraction_executed_in_decision": False,
            "new_domain_shift_executed": False,
            "domain_id": "artifact_claim_review_v0",
            "outcome_class": "DOMAIN_SHIFT_PASS_WITH_GAPS",
            "dominant_gap_class": "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL",
            "reviewed_reference_frozen": True,
            "post_c5_reference_decision_ready": True,
            "fixtures_total": closure_summary.get("fixtures_total"),
            "proposal_packets_emitted": closure_summary.get("proposal_packets_emitted"),
            "proposal_packets_accepted": closure_summary.get("proposal_packets_accepted"),
            "cell1_builds_verified": closure_summary.get("cell1_builds_verified"),
            "edge_observations_emitted": closure_summary.get("edge_observations_emitted"),
            "unit_feedback_records_emitted": closure_summary.get("unit_feedback_records_emitted"),
            "bad_counters_zero": profile["bad_counters_zero"],
            "full_transfer_claimed": False,
            "research_lab_readiness_claimed": False,
            "global_autonomy_claimed": False,
            "general_cell1_authority_claimed": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "recommended_next": recommended_next,
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "decision_basis": rel(DECISION_BASIS_PATH),
            "decision_options": rel(DECISION_OPTIONS_PATH),
            "selected_branch": rel(SELECTED_BRANCH_PATH),
            "c6_example_extraction_authorization": rel(C6_EXAMPLE_EXTRACTION_AUTH_PATH),
            "c5_reference_continuation": rel(C5_REFERENCE_CONTINUATION_PATH),
            "deferred_branches": rel(DEFERRED_BRANCHES_PATH),
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
    print(f"post_c5_reference_decision_receipt_id={receipt_id}")
    print(f"post_c5_reference_decision_receipt_path={rel(receipt_path)}")
    print(f"post_c5_reference_decision_basis_path={rel(DECISION_BASIS_PATH)}")
    print(f"post_c5_selected_branch_path={rel(SELECTED_BRANCH_PATH)}")
    print(f"c6_example_extraction_authorization_path={rel(C6_EXAMPLE_EXTRACTION_AUTH_PATH)}")
    print(f"post_c5_reference_decision_rollup_path={rel(ROLLUP_PATH)}")
    print(f"post_c5_reference_decision_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
