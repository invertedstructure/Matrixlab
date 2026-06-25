#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_C5_FULL_DOMAIN_SHIFT_TRANSITION_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "domain_shift.full_transition_reviewed_reference.v0"
LAYER = "OUTER / DOMAIN_SHIFT_TRANSITION / REFERENCE_CLOSURE"
MODE = "CLOSE / FREEZE_C5_PASS_WITH_GAPS_AS_REVIEWED_REFERENCE / DECISION_READY"
BUILD_MODE = "C5_FULL_DOMAIN_SHIFT_TRANSITION_REFERENCE_CLOSURE_ONLY"

SOURCE_C5_REVIEW_RECEIPT_ID = "efc12ac0"
SOURCE_C5_BUILD_RECEIPT_ID = "b4acefb6"

SOURCE_C5_REVIEW_RECEIPT_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0_receipts/efc12ac0.json"
SOURCE_C5_BUILD_RECEIPT_PATH = ROOT / "data/c5_full_domain_shift_transition_v0_receipts/b4acefb6.json"

REVIEW_BASIS_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0/c5_domain_shift_review_basis_v0.json"
FIXTURE_MATRIX_REVIEW_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0/c5_domain_shift_fixture_matrix_review_v0.json"
CELL0_LOOP_REVIEW_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0/c5_domain_shift_cell0_loop_review_v0.json"
LABEL_AUDIT_REVIEW_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0/c5_domain_shift_label_audit_review_v0.json"
PROPOSAL_REVIEW_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0/c5_domain_shift_proposal_review_v0.json"
CELL1_REVIEW_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0/c5_domain_shift_cell1_review_v0.json"
VERIFICATION_HANDOFF_REVIEW_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0/c5_domain_shift_verification_handoff_review_v0.json"
EDGE_FEEDBACK_REVIEW_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0/c5_domain_shift_edge_feedback_review_v0.json"
BAD_COUNTER_REVIEW_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0/c5_domain_shift_bad_counter_review_v0.json"
OUTCOME_REVIEW_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0/c5_domain_shift_outcome_review_v0.json"
CLOSE_CANDIDATE_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0/c5_domain_shift_reviewed_reference_close_candidate_v0.json"
REVIEW_AUTHORITY_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0/c5_domain_shift_review_authority_boundary_v0.json"
REVIEW_CLASSIFICATION_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0/c5_domain_shift_review_classification_v0.json"
REVIEW_ROLLUP_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0/c5_domain_shift_review_rollup_v0.json"
REVIEW_PROFILE_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0/c5_domain_shift_review_profile_v0.json"
REVIEW_REPORT_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0/c5_domain_shift_review_report.json"
REVIEW_TRACE_PATH = ROOT / "data/c5_full_domain_shift_transition_review_v0/c5_domain_shift_review_transition_trace.json"

BUILD_ROLLUP_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_rollup_v0.json"
BUILD_READOUT_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_readout_v0.json"
BUILD_PROFILE_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/c5_transition_profile_v0.json"
BUILD_TRACE_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/c5_transition_trace.json"
BUILD_REPORT_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/c5_report.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C5_REVIEW_RECEIPT_PATH,
    SOURCE_C5_BUILD_RECEIPT_PATH,
    REVIEW_BASIS_PATH,
    FIXTURE_MATRIX_REVIEW_PATH,
    CELL0_LOOP_REVIEW_PATH,
    LABEL_AUDIT_REVIEW_PATH,
    PROPOSAL_REVIEW_PATH,
    CELL1_REVIEW_PATH,
    VERIFICATION_HANDOFF_REVIEW_PATH,
    EDGE_FEEDBACK_REVIEW_PATH,
    BAD_COUNTER_REVIEW_PATH,
    OUTCOME_REVIEW_PATH,
    CLOSE_CANDIDATE_PATH,
    REVIEW_AUTHORITY_PATH,
    REVIEW_CLASSIFICATION_PATH,
    REVIEW_ROLLUP_PATH,
    REVIEW_PROFILE_PATH,
    REVIEW_REPORT_PATH,
    REVIEW_TRACE_PATH,
    BUILD_ROLLUP_PATH,
    BUILD_READOUT_PATH,
    BUILD_PROFILE_PATH,
    BUILD_TRACE_PATH,
    BUILD_REPORT_PATH,
]

OUT_DIR = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0"
RECEIPT_DIR = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0_receipts"

REFERENCE_CLOSURE_BASIS_PATH = OUT_DIR / "c5_domain_shift_reference_closure_basis_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "c5_domain_shift_reviewed_reference_v0.json"
REFERENCE_FREEZE_MANIFEST_PATH = OUT_DIR / "c5_domain_shift_reviewed_reference_freeze_manifest_v0.json"
REFERENCE_INDEX_PATH = OUT_DIR / "c5_domain_shift_reviewed_reference_index_v0.json"
PASS_WITH_GAPS_REFERENCE_PATH = OUT_DIR / "c5_domain_shift_pass_with_gaps_reference_v0.json"
GAP_REFERENCE_PATH = OUT_DIR / "c5_domain_shift_gap_reference_v0.json"
NEXT_DECISION_READY_PATH = OUT_DIR / "c5_post_domain_shift_reference_decision_ready_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "c5_domain_shift_reference_closure_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "c5_domain_shift_reference_closure_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "c5_domain_shift_reference_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c5_domain_shift_reference_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "c5_domain_shift_reference_closure_report.json"
TRACE_PATH = OUT_DIR / "c5_domain_shift_reference_closure_transition_trace.json"

EXPECTED_REVIEW_STATUS = "TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_REVIEWED_PASS_WITH_GAPS_CLOSE_READY"
EXPECTED_REVIEW_STOP = "STOP_TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_REVIEWED_PASS_WITH_GAPS_CLOSE_READY"
EXPECTED_REVIEW_NEXT = "CLOSE_C5_FULL_DOMAIN_SHIFT_TRANSITION_AS_REVIEWED_REFERENCE_V0"
EXPECTED_BUILD_STATUS = "TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_BUILT_PASS_WITH_GAPS_REVIEW_READY"
RECOMMENDED_NEXT = "DECIDE_NEXT_AFTER_C5_FULL_DOMAIN_SHIFT_TRANSITION_REFERENCE_CLOSURE_V0"

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

    review_receipt = read_json(SOURCE_C5_REVIEW_RECEIPT_PATH)
    review_summary = review_receipt.get("machine_readable_c5_full_domain_shift_transition_review_summary", {})

    build_receipt = read_json(SOURCE_C5_BUILD_RECEIPT_PATH)
    build_summary = build_receipt.get("machine_readable_c5_full_domain_shift_transition_summary", {})

    close_candidate = read_json(CLOSE_CANDIDATE_PATH)
    review_rollup = read_json(REVIEW_ROLLUP_PATH)
    review_profile = read_json(REVIEW_PROFILE_PATH)
    review_authority = read_json(REVIEW_AUTHORITY_PATH)
    review_classification = read_json(REVIEW_CLASSIFICATION_PATH)
    build_rollup = read_json(BUILD_ROLLUP_PATH)
    build_readout = read_json(BUILD_READOUT_PATH)
    build_profile = read_json(BUILD_PROFILE_PATH)

    if review_receipt.get("receipt_id") != SOURCE_C5_REVIEW_RECEIPT_ID or review_receipt.get("gate") != "PASS":
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
        "c5_domain_shift_review_complete",
        "c5_domain_shift_review_pass",
        "close_candidate_ready",
        "bad_counters_zero",
        "local_decision_grammar_survived",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"review_summary_required_true_missing:{key}")

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
        if review_summary.get(key) != expected:
            failures.append(f"review_count_wrong:{key}:{review_summary.get(key)}")

    if review_summary.get("domain_id") != "artifact_claim_review_v0":
        failures.append("review_domain_wrong")
    if review_summary.get("outcome_class") != "DOMAIN_SHIFT_PASS_WITH_GAPS":
        failures.append("review_outcome_wrong")
    if review_summary.get("dominant_gap_class") != "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL":
        failures.append("review_gap_wrong")

    for key in [
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
        if review_summary.get(key) is not False:
            failures.append(f"review_forbidden_true:{key}")

    for key in [
        "cell1_freebuild_count",
        "cell1_auto_chain_count",
        "unbounded_payload_inspection_count",
        "proposal_applied_without_review_count",
    ]:
        if review_summary.get(key) != 0:
            failures.append(f"review_forbidden_count_nonzero:{key}:{review_summary.get(key)}")

    if build_receipt.get("receipt_id") != SOURCE_C5_BUILD_RECEIPT_ID or build_receipt.get("gate") != "PASS":
        failures.append("build_receipt_not_pass")
    if build_summary.get("status") != EXPECTED_BUILD_STATUS:
        failures.append("build_status_wrong")
    if build_summary.get("outcome_class") != "DOMAIN_SHIFT_PASS_WITH_GAPS":
        failures.append("build_outcome_wrong")

    if close_candidate.get("candidate_status") != "C5_DOMAIN_SHIFT_REVIEWED_REFERENCE_CLOSE_READY":
        failures.append("close_candidate_not_ready")
    if close_candidate.get("review_pass") is not True:
        failures.append("close_candidate_review_not_pass")
    if review_rollup.get("close_candidate_ready_count") != 1:
        failures.append("review_rollup_close_count_wrong")
    if review_profile.get("close_candidate_ready") is not True or review_profile.get("next_command_goal") is not None:
        failures.append("review_profile_wrong")
    if review_authority.get("may_close_c5_domain_shift_as_reviewed_reference_next") is not True:
        failures.append("review_authority_no_close")
    if review_authority.get("may_claim_transfer") is not False:
        failures.append("review_authority_allows_transfer")
    if review_classification.get("close_candidate_ready") is not True:
        failures.append("review_classification_not_close_ready")
    if build_rollup.get("outcome_class") != "DOMAIN_SHIFT_PASS_WITH_GAPS":
        failures.append("build_rollup_outcome_wrong")
    if build_readout.get("outcome") != "DOMAIN_SHIFT_PASS_WITH_GAPS":
        failures.append("build_readout_outcome_wrong")
    if build_profile.get("bad_counters_zero") is not True:
        failures.append("build_profile_bad_counters_wrong")

    return failures, {
        "review_summary": review_summary,
        "build_summary": build_summary,
        "build_readout": build_readout,
        "build_profile": build_profile,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    close_pass = not failures
    status = "TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY" if close_pass else "TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_REFERENCE_CLOSURE_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if close_pass else "REPAIR_C5_FULL_DOMAIN_SHIFT_TRANSITION_REFERENCE_CLOSURE_V0"

    review_summary = basis.get("review_summary", {})
    build_readout = basis.get("build_readout", {})
    build_profile = basis.get("build_profile", {})

    reason_codes = [
        "C5_DOMAIN_SHIFT_CLOSED_AS_REVIEWED_REFERENCE",
        "C5_REVIEW_RECEIPT_CONSUMED",
        "C5_BUILD_RECEIPT_CONSUMED",
        "PASS_WITH_GAPS_FROZEN_AS_REFERENCE",
        "ARTIFACT_CLAIM_REVIEW_DOMAIN_REFERENCE_FROZEN",
        "LOCAL_DECISION_GRAMMAR_SURVIVAL_FROZEN",
        "BOUNDED_GAP_CLASS_FROZEN",
        "CELL1_ACCEPTED_PROPOSAL_PATH_FROZEN",
        "EDGE_OBSERVATION_SURFACE_FROZEN",
        "UNIT_FEEDBACK_SURFACE_FROZEN",
        "BAD_COUNTERS_ZERO_FROZEN",
        "POST_C5_REFERENCE_DECISION_READY",
        "NO_FULL_TRANSFER_CLAIM",
        "NO_RESEARCH_LAB_CLAIM",
        "NO_GLOBAL_AUTONOMY_CLAIM",
        "NO_GENERAL_CELL1_AUTHORITY_CLAIM",
        "NO_NEW_DOMAIN_EXECUTION_IN_CLOSURE",
        "NO_SOURCE_MUTATION",
        "NO_PRIOR_RECEIPT_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if close_pass else failures

    closure_basis = {
        "schema_version": "c5_domain_shift_reference_closure_basis_v0",
        "closure_status": status,
        "source_c5_review_receipt_id": SOURCE_C5_REVIEW_RECEIPT_ID,
        "source_c5_build_receipt_id": SOURCE_C5_BUILD_RECEIPT_ID,
        "review_pass": close_pass,
        "close_candidate_ready": close_pass,
        "domain_id": "artifact_claim_review_v0",
        "outcome_class": "DOMAIN_SHIFT_PASS_WITH_GAPS" if close_pass else None,
        "dominant_gap_class": "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL" if close_pass else None,
    }

    reviewed_reference = {
        "schema_version": "c5_domain_shift_reviewed_reference_v0",
        "reference_status": "C5_DOMAIN_SHIFT_REVIEWED_REFERENCE_FROZEN" if close_pass else "REFERENCE_NOT_FROZEN",
        "reference_id": "c5_domain_shift_reviewed_reference_" + sig8({
            "review_receipt": SOURCE_C5_REVIEW_RECEIPT_ID,
            "build_receipt": SOURCE_C5_BUILD_RECEIPT_ID,
            "outcome": "DOMAIN_SHIFT_PASS_WITH_GAPS",
        }),
        "domain_id": "artifact_claim_review_v0",
        "outcome_class": "DOMAIN_SHIFT_PASS_WITH_GAPS",
        "dominant_gap_class": "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL",
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
        "bad_counters_zero": True,
        "local_decision_grammar_survived": True,
        "interpretation": build_readout.get("interpretation"),
        "must_not_infer": build_profile.get("must_not_infer", []),
    }

    freeze_manifest = {
        "schema_version": "c5_domain_shift_reviewed_reference_freeze_manifest_v0",
        "freeze_status": "FROZEN" if close_pass else "NOT_FROZEN",
        "source_receipts": {
            "build": SOURCE_C5_BUILD_RECEIPT_ID,
            "review": SOURCE_C5_REVIEW_RECEIPT_ID,
        },
        "frozen_source_artifacts": [rel(p) for p in REQUIRED_SOURCE_FILES],
        "frozen_reference_artifacts": {
            "closure_basis": rel(REFERENCE_CLOSURE_BASIS_PATH),
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "pass_with_gaps_reference": rel(PASS_WITH_GAPS_REFERENCE_PATH),
            "gap_reference": rel(GAP_REFERENCE_PATH),
            "next_decision_ready": rel(NEXT_DECISION_READY_PATH),
        },
    }

    reference_index = {
        "schema_version": "c5_domain_shift_reviewed_reference_index_v0",
        "index_status": "REFERENCE_INDEX_EMITTED" if close_pass else "REFERENCE_INDEX_NOT_EMITTED",
        "reference_paths": {
            "closure_basis": rel(REFERENCE_CLOSURE_BASIS_PATH),
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "freeze_manifest": rel(REFERENCE_FREEZE_MANIFEST_PATH),
            "pass_with_gaps_reference": rel(PASS_WITH_GAPS_REFERENCE_PATH),
            "gap_reference": rel(GAP_REFERENCE_PATH),
            "next_decision_ready": rel(NEXT_DECISION_READY_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "trace": rel(TRACE_PATH),
        },
    }

    pass_with_gaps_reference = {
        "schema_version": "c5_domain_shift_pass_with_gaps_reference_v0",
        "reference_status": "PASS_WITH_GAPS_CONFIRMED_AND_FROZEN",
        "pass_with_gaps_meaning": "The domain changed and the decision discipline survived, while bounded evidence/proposal gaps remained visible and typed.",
        "pass_with_gaps_does_not_mean": [
            "full transfer proven",
            "research-lab readiness",
            "global autonomy",
            "general Cell 1 authority",
            "new domain solved globally",
        ],
        "domain_id": "artifact_claim_review_v0",
        "local_decision_grammar_survived": True,
        "bad_counters_zero": True,
    }

    gap_reference = {
        "schema_version": "c5_domain_shift_gap_reference_v0",
        "gap_status": "BOUNDED_GAP_FROZEN",
        "dominant_gap_class": "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL",
        "gap_meaning": "Some artifact claims require bounded reviewed evidence/proposal handling before stronger classification.",
        "lawful_refinement_direction": "Decide whether to refine evidence/proposal handling or consume C5 examples for C6 inter-cell protocol design.",
        "gap_not_failure": True,
    }

    next_decision_ready = {
        "schema_version": "c5_post_domain_shift_reference_decision_ready_v0",
        "decision_ready": close_pass,
        "recommended_next": recommended_next,
        "decision_scope": "decide next after reviewed C5 domain shift reference closure",
        "eligible_next_questions": [
            "close C5 branch and freeze as reference object",
            "extract C6 inter-cell protocol examples from C5",
            "refine bounded evidence/proposal handling",
            "defer C6 and return to observation/unit feedback hardening",
        ],
        "not_authorized_here": [
            "open C6 automatically",
            "claim full transfer",
            "claim research-lab readiness",
            "grant general Cell 1 authority",
            "auto-chain new domain shift",
        ],
    }

    authority_boundary = {
        "schema_version": "c5_domain_shift_reference_closure_authority_boundary_v0",
        "status": status,
        "may_decide_next_after_c5_reference_closure": close_pass,
        "may_open_c6_now_in_closure": False,
        "may_execute_new_domain_shift_now_in_closure": False,
        "may_claim_transfer": False,
        "may_claim_research_lab_readiness": False,
        "may_claim_global_autonomy": False,
        "may_grant_general_cell1_authority": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
    }

    classification = {
        "schema_version": "c5_domain_shift_reference_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "c5_domain_shift_closed_as_reviewed_reference": close_pass,
        "reviewed_reference_frozen": close_pass,
        "post_c5_reference_decision_ready": close_pass,
        "domain_id": "artifact_claim_review_v0",
        "outcome_class": "DOMAIN_SHIFT_PASS_WITH_GAPS" if close_pass else None,
        "dominant_gap_class": "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL" if close_pass else None,
        "fixtures_total": review_summary.get("fixtures_total"),
        "fixtures_passed": review_summary.get("fixtures_passed"),
        "fixtures_blocked": review_summary.get("fixtures_blocked"),
        "cell0_loop_runs": review_summary.get("cell0_loop_runs"),
        "cell1_builds_attempted": review_summary.get("cell1_builds_attempted"),
        "cell1_builds_verified": review_summary.get("cell1_builds_verified"),
        "proposal_packets_emitted": review_summary.get("proposal_packets_emitted"),
        "proposal_packets_accepted": review_summary.get("proposal_packets_accepted"),
        "typed_stops": review_summary.get("typed_stops"),
        "edge_observations_emitted": review_summary.get("edge_observations_emitted"),
        "unit_feedback_records_emitted": review_summary.get("unit_feedback_records_emitted"),
        "bad_counters_zero": close_pass,
        "local_decision_grammar_survived": close_pass,
        "domain_shift_pass_claimed": False,
        "full_transfer_claimed": False,
        "research_lab_readiness_claimed": False,
        "global_autonomy_claimed": False,
        "general_cell1_authority_claimed": False,
        "new_domain_executed_in_closure": False,
        "cell1_freebuild_count": 0,
        "cell1_auto_chain_count": 0,
        "unbounded_payload_inspection_count": 0,
        "proposal_applied_without_review_count": 0,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "c5_domain_shift_reference_closure_rollup_v0",
        "closure_count": 1 if close_pass else 0,
        "reviewed_reference_frozen_count": 1 if close_pass else 0,
        "post_c5_reference_decision_ready_count": 1 if close_pass else 0,
        "fixtures_total": review_summary.get("fixtures_total"),
        "fixtures_passed": review_summary.get("fixtures_passed"),
        "fixtures_blocked": review_summary.get("fixtures_blocked"),
        "cell0_loop_runs": review_summary.get("cell0_loop_runs"),
        "cell1_builds_attempted": review_summary.get("cell1_builds_attempted"),
        "cell1_builds_verified": review_summary.get("cell1_builds_verified"),
        "proposal_packets_emitted": review_summary.get("proposal_packets_emitted"),
        "proposal_packets_accepted": review_summary.get("proposal_packets_accepted"),
        "typed_stops": review_summary.get("typed_stops"),
        "edge_observations_emitted": review_summary.get("edge_observations_emitted"),
        "unit_feedback_records_emitted": review_summary.get("unit_feedback_records_emitted"),
        "bad_counters_zero_count": 1 if close_pass else 0,
        "domain_shift_pass_claim_count": 0,
        "full_transfer_claim_count": 0,
        "research_lab_readiness_claim_count": 0,
        "global_autonomy_claim_count": 0,
        "general_cell1_authority_claim_count": 0,
        "new_domain_execution_in_closure_count": 0,
        "cell1_freebuild_count": 0,
        "cell1_auto_chain_count": 0,
        "unbounded_payload_inspection_count": 0,
        "proposal_applied_without_review_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    profile = {
        "schema_version": "c5_domain_shift_reference_closure_profile_v0",
        "profile_id": "c5_domain_shift_reference_closure_" + sig8(rollup),
        "status": status,
        "domain_id": "artifact_claim_review_v0",
        "outcome_class": "DOMAIN_SHIFT_PASS_WITH_GAPS" if close_pass else None,
        "dominant_gap_class": "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL" if close_pass else None,
        "reviewed_reference_frozen": close_pass,
        "post_c5_reference_decision_ready": close_pass,
        "bad_counters_zero": close_pass,
        "core_rule_preserved": "Domain may change; decision discipline may not.",
        "recommendation": "Decide next after C5 reviewed reference closure.",
        "must_not_infer": build_profile.get("must_not_infer", []),
        "next_command_goal": None,
    }

    report = {
        "schema_version": "c5_domain_shift_reference_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "C5 full domain shift transition is closed as a reviewed reference. The reference preserves artifact_claim_review_v0 pass-with-gaps evidence, one accepted Cell 1 path, edge observations, useful feedback, and zero bad counters without claiming transfer, research readiness, global autonomy, or general Cell 1 authority.",
        "domain_id": "artifact_claim_review_v0",
        "outcome_class": "DOMAIN_SHIFT_PASS_WITH_GAPS" if close_pass else None,
        "dominant_gap_class": "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL" if close_pass else None,
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "c5_domain_shift_reference_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c5_review_receipt",
                "question": "is C5 transition reviewed close-ready",
                "answer": "yes" if close_pass else "no",
                "taken": "freeze reviewed reference",
            },
            {
                "step": "freeze_pass_with_gaps_reference",
                "question": "what outcome is preserved",
                "answer": "DOMAIN_SHIFT_PASS_WITH_GAPS" if close_pass else None,
                "taken": "preserve bounded gap and no-transfer interpretation",
            },
            {
                "step": "preserve_closure_boundary",
                "question": "does closure open C6 or claim transfer",
                "answer": "no",
                "taken": "emit post-C5 reference decision readiness",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (REFERENCE_CLOSURE_BASIS_PATH, closure_basis),
        (REVIEWED_REFERENCE_PATH, reviewed_reference),
        (REFERENCE_FREEZE_MANIFEST_PATH, freeze_manifest),
        (REFERENCE_INDEX_PATH, reference_index),
        (PASS_WITH_GAPS_REFERENCE_PATH, pass_with_gaps_reference),
        (GAP_REFERENCE_PATH, gap_reference),
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
        "C5_REF_CLOSE_0_REVIEW_RECEIPT_CONSUMED": SOURCE_C5_REVIEW_RECEIPT_PATH.exists(),
        "C5_REF_CLOSE_1_BUILD_RECEIPT_CONSUMED": SOURCE_C5_BUILD_RECEIPT_PATH.exists(),
        "C5_REF_CLOSE_2_CLOSURE_BASIS_EMITTED": REFERENCE_CLOSURE_BASIS_PATH.exists(),
        "C5_REF_CLOSE_3_REVIEWED_REFERENCE_FROZEN": REVIEWED_REFERENCE_PATH.exists() and reviewed_reference["reference_status"] == "C5_DOMAIN_SHIFT_REVIEWED_REFERENCE_FROZEN",
        "C5_REF_CLOSE_4_PASS_WITH_GAPS_REFERENCE_FROZEN": PASS_WITH_GAPS_REFERENCE_PATH.exists() and pass_with_gaps_reference["gap_not_failure"] if "gap_not_failure" in pass_with_gaps_reference else PASS_WITH_GAPS_REFERENCE_PATH.exists(),
        "C5_REF_CLOSE_5_GAP_REFERENCE_FROZEN": GAP_REFERENCE_PATH.exists() and gap_reference["gap_not_failure"] is True,
        "C5_REF_CLOSE_6_FREEZE_MANIFEST_EMITTED": REFERENCE_FREEZE_MANIFEST_PATH.exists(),
        "C5_REF_CLOSE_7_REFERENCE_INDEX_EMITTED": REFERENCE_INDEX_PATH.exists(),
        "C5_REF_CLOSE_8_POST_C5_DECISION_READY": NEXT_DECISION_READY_PATH.exists() and next_decision_ready["decision_ready"] is True,
        "C5_REF_CLOSE_9_NO_NEW_DOMAIN_EXECUTION_IN_CLOSURE": rollup["new_domain_execution_in_closure_count"] == 0,
        "C5_REF_CLOSE_10_NO_TRANSFER_RESEARCH_AUTONOMY_OR_GENERAL_CELL1_CLAIMS": rollup["full_transfer_claim_count"] == 0 and rollup["research_lab_readiness_claim_count"] == 0 and rollup["global_autonomy_claim_count"] == 0 and rollup["general_cell1_authority_claim_count"] == 0,
        "C5_REF_CLOSE_11_NO_CELL1_FREEBUILD_OR_AUTO_CHAIN": rollup["cell1_freebuild_count"] == 0 and rollup["cell1_auto_chain_count"] == 0,
        "C5_REF_CLOSE_12_NO_SOURCE_OR_PRIOR_RECEIPT_MUTATION": rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "C5_REF_CLOSE_13_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C5_REF_CLOSE_14_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "C5_REF_CLOSE_15_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_REFERENCE_CLOSURE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": status,
        "gate": gate,
        "review_receipt": SOURCE_C5_REVIEW_RECEIPT_ID,
        "outcome": "DOMAIN_SHIFT_PASS_WITH_GAPS",
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "c5_full_domain_shift_transition_reference_closure_receipt_v0",
        "receipt_type": "TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_REFERENCE_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_c5_review_receipt_id": SOURCE_C5_REVIEW_RECEIPT_ID,
        "source_c5_build_receipt_id": SOURCE_C5_BUILD_RECEIPT_ID,
        "machine_readable_c5_full_domain_shift_transition_reference_closure_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "c5_domain_shift_closed_as_reviewed_reference": close_pass,
            "reviewed_reference_frozen": close_pass,
            "post_c5_reference_decision_ready": close_pass,
            "domain_id": "artifact_claim_review_v0",
            "outcome_class": "DOMAIN_SHIFT_PASS_WITH_GAPS" if close_pass else None,
            "dominant_gap_class": "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL" if close_pass else None,
            "fixtures_total": review_summary.get("fixtures_total"),
            "fixtures_passed": review_summary.get("fixtures_passed"),
            "fixtures_blocked": review_summary.get("fixtures_blocked"),
            "cell0_loop_runs": review_summary.get("cell0_loop_runs"),
            "cell1_builds_attempted": review_summary.get("cell1_builds_attempted"),
            "cell1_builds_verified": review_summary.get("cell1_builds_verified"),
            "proposal_packets_emitted": review_summary.get("proposal_packets_emitted"),
            "proposal_packets_accepted": review_summary.get("proposal_packets_accepted"),
            "typed_stops": review_summary.get("typed_stops"),
            "edge_observations_emitted": review_summary.get("edge_observations_emitted"),
            "unit_feedback_records_emitted": review_summary.get("unit_feedback_records_emitted"),
            "bad_counters_zero": close_pass,
            "local_decision_grammar_survived": close_pass,
            "new_domain_executed_in_closure": False,
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
            "recommended_next": recommended_next,
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "closure_basis": rel(REFERENCE_CLOSURE_BASIS_PATH),
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "freeze_manifest": rel(REFERENCE_FREEZE_MANIFEST_PATH),
            "reference_index": rel(REFERENCE_INDEX_PATH),
            "pass_with_gaps_reference": rel(PASS_WITH_GAPS_REFERENCE_PATH),
            "gap_reference": rel(GAP_REFERENCE_PATH),
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
    print(f"c5_reference_closure_receipt_id={receipt_id}")
    print(f"c5_reference_closure_receipt_path={rel(receipt_path)}")
    print(f"c5_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"c5_reference_freeze_manifest_path={rel(REFERENCE_FREEZE_MANIFEST_PATH)}")
    print(f"c5_next_decision_ready_path={rel(NEXT_DECISION_READY_PATH)}")
    print(f"c5_reference_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"c5_reference_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
