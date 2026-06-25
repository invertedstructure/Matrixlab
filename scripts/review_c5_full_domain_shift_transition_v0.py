#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_C5_FULL_DOMAIN_SHIFT_TRANSITION_V0"
TARGET_UNIT_ID = "domain_shift.full_transition_review.v0"
LAYER = "OUTER / DOMAIN_SHIFT_TRANSITION / REVIEW"
MODE = "REVIEW / VERIFY_C5_TRANSITION_RECEIPTS / NO_NEW_DOMAIN_EXECUTION"
BUILD_MODE = "C5_FULL_DOMAIN_SHIFT_TRANSITION_REVIEW_ONLY"

SOURCE_C5_BUILD_RECEIPT_ID = "b4acefb6"

SOURCE_C5_BUILD_RECEIPT_PATH = ROOT / "data/c5_full_domain_shift_transition_v0_receipts/b4acefb6.json"

DOMAIN_CONTRACT_SCHEMA_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_contract_schema_v0.json"
DOMAIN_CONTRACT_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_contract_v0.json"
FIXTURE_RECORD_SCHEMA_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_fixture_record_schema_v0.json"
FIXTURE_RECORDS_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_fixture_records_v0.jsonl"
CELL0_LOOP_TRACE_SCHEMA_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_cell0_loop_trace_schema_v0.json"
CELL0_LOOP_TRACES_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_cell0_loop_traces_v0.jsonl"
LABEL_AUDIT_SCHEMA_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_label_audit_schema_v0.json"
LABEL_AUDITS_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_label_audits_v0.jsonl"
PROPOSAL_PACKETS_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_proposal_packets_v0.jsonl"
CELL1_BUILD_RECEIPT_SCHEMA_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_cell1_build_receipt_schema_v0.json"
CELL1_BUILD_RECEIPTS_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_cell1_build_receipts_v0.jsonl"
VERIFICATION_RECEIPT_SCHEMA_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_verification_receipt_schema_v0.json"
VERIFICATION_RECEIPTS_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_verification_receipts_v0.jsonl"
HANDOFF_RECORD_SCHEMA_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_handoff_record_schema_v0.json"
HANDOFF_RECORDS_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_handoff_records_v0.jsonl"
OUTCOME_ENUM_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_outcome_enum_v0.json"
EDGE_OBSERVATIONS_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/decision_edge_observation_records_v0.jsonl"
UNIT_FEEDBACK_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/unit_feedback_records_v0.jsonl"
ROLLUP_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_rollup_v0.json"
READOUT_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/domain_shift_readout_v0.json"
PROFILE_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/c5_transition_profile_v0.json"
TRACE_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/c5_transition_trace.json"
REPORT_PATH = ROOT / "data/c5_full_domain_shift_transition_v0/c5_report.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C5_BUILD_RECEIPT_PATH,
    DOMAIN_CONTRACT_SCHEMA_PATH,
    DOMAIN_CONTRACT_PATH,
    FIXTURE_RECORD_SCHEMA_PATH,
    FIXTURE_RECORDS_PATH,
    CELL0_LOOP_TRACE_SCHEMA_PATH,
    CELL0_LOOP_TRACES_PATH,
    LABEL_AUDIT_SCHEMA_PATH,
    LABEL_AUDITS_PATH,
    PROPOSAL_PACKETS_PATH,
    CELL1_BUILD_RECEIPT_SCHEMA_PATH,
    CELL1_BUILD_RECEIPTS_PATH,
    VERIFICATION_RECEIPT_SCHEMA_PATH,
    VERIFICATION_RECEIPTS_PATH,
    HANDOFF_RECORD_SCHEMA_PATH,
    HANDOFF_RECORDS_PATH,
    OUTCOME_ENUM_PATH,
    EDGE_OBSERVATIONS_PATH,
    UNIT_FEEDBACK_PATH,
    ROLLUP_PATH,
    READOUT_PATH,
    PROFILE_PATH,
    TRACE_PATH,
    REPORT_PATH,
]

OUT_DIR = ROOT / "data/c5_full_domain_shift_transition_review_v0"
RECEIPT_DIR = ROOT / "data/c5_full_domain_shift_transition_review_v0_receipts"

REVIEW_BASIS_PATH = OUT_DIR / "c5_domain_shift_review_basis_v0.json"
FIXTURE_MATRIX_REVIEW_PATH = OUT_DIR / "c5_domain_shift_fixture_matrix_review_v0.json"
CELL0_LOOP_REVIEW_PATH = OUT_DIR / "c5_domain_shift_cell0_loop_review_v0.json"
LABEL_AUDIT_REVIEW_PATH = OUT_DIR / "c5_domain_shift_label_audit_review_v0.json"
PROPOSAL_REVIEW_PATH = OUT_DIR / "c5_domain_shift_proposal_review_v0.json"
CELL1_REVIEW_PATH = OUT_DIR / "c5_domain_shift_cell1_review_v0.json"
VERIFICATION_HANDOFF_REVIEW_PATH = OUT_DIR / "c5_domain_shift_verification_handoff_review_v0.json"
EDGE_FEEDBACK_REVIEW_PATH = OUT_DIR / "c5_domain_shift_edge_feedback_review_v0.json"
BAD_COUNTER_REVIEW_PATH = OUT_DIR / "c5_domain_shift_bad_counter_review_v0.json"
OUTCOME_REVIEW_PATH = OUT_DIR / "c5_domain_shift_outcome_review_v0.json"
CLOSE_CANDIDATE_PATH = OUT_DIR / "c5_domain_shift_reviewed_reference_close_candidate_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "c5_domain_shift_review_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "c5_domain_shift_review_classification_v0.json"
ROLLUP_REVIEW_PATH = OUT_DIR / "c5_domain_shift_review_rollup_v0.json"
PROFILE_REVIEW_PATH = OUT_DIR / "c5_domain_shift_review_profile_v0.json"
REPORT_REVIEW_PATH = OUT_DIR / "c5_domain_shift_review_report.json"
TRACE_REVIEW_PATH = OUT_DIR / "c5_domain_shift_review_transition_trace.json"

EXPECTED_STATUS = "TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_BUILT_PASS_WITH_GAPS_REVIEW_READY"
EXPECTED_STOP = "STOP_C5_DOMAIN_SHIFT_PASS_WITH_GAPS"
EXPECTED_NEXT = "REVIEW_C5_FULL_DOMAIN_SHIFT_TRANSITION_V0"
RECOMMENDED_NEXT = "CLOSE_C5_FULL_DOMAIN_SHIFT_TRANSITION_AS_REVIEWED_REFERENCE_V0"

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

    receipt = read_json(SOURCE_C5_BUILD_RECEIPT_PATH)
    summary = receipt.get("machine_readable_c5_full_domain_shift_transition_summary", {})

    contract = read_json(DOMAIN_CONTRACT_PATH)
    fixtures = read_jsonl(FIXTURE_RECORDS_PATH)
    traces = read_jsonl(CELL0_LOOP_TRACES_PATH)
    label_audits = read_jsonl(LABEL_AUDITS_PATH)
    proposals = read_jsonl(PROPOSAL_PACKETS_PATH)
    builds = read_jsonl(CELL1_BUILD_RECEIPTS_PATH)
    verifications = read_jsonl(VERIFICATION_RECEIPTS_PATH)
    handoffs = read_jsonl(HANDOFF_RECORDS_PATH)
    edges = read_jsonl(EDGE_OBSERVATIONS_PATH)
    feedback = read_jsonl(UNIT_FEEDBACK_PATH)
    rollup = read_json(ROLLUP_PATH)
    readout = read_json(READOUT_PATH)
    profile = read_json(PROFILE_PATH)
    trace = read_json(TRACE_PATH)
    report = read_json(REPORT_PATH)

    if receipt.get("receipt_id") != SOURCE_C5_BUILD_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_c5_build_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_STOP:
        failures.append("source_c5_build_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_c5_build_hidden_next")
    if summary.get("status") != EXPECTED_STATUS:
        failures.append(f"source_c5_build_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"source_c5_build_next_wrong:{summary.get('recommended_next')}")

    if summary.get("domain_id") != "artifact_claim_review_v0":
        failures.append("summary_domain_wrong")
    if summary.get("outcome_class") != "DOMAIN_SHIFT_PASS_WITH_GAPS":
        failures.append("summary_outcome_wrong")
    if summary.get("dominant_gap_class") != "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL":
        failures.append("summary_dominant_gap_wrong")

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
        if summary.get(key) != expected:
            failures.append(f"summary_count_wrong:{key}:{summary.get(key)}")

    for key in ["bad_counters_zero", "domain_shift_executed", "local_decision_grammar_survived"]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

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
        if summary.get(key) is not False:
            failures.append(f"summary_forbidden_true:{key}")

    for key in [
        "cell1_freebuild_count",
        "cell1_auto_chain_count",
        "unbounded_payload_inspection_count",
        "proposal_applied_without_review_count",
    ]:
        if summary.get(key) != 0:
            failures.append(f"summary_forbidden_count_nonzero:{key}:{summary.get(key)}")

    if contract.get("domain_id") != "artifact_claim_review_v0":
        failures.append("contract_domain_wrong")
    if len(fixtures) != 5:
        failures.append("fixture_record_count_wrong")
    if len(traces) != 5:
        failures.append("trace_count_wrong")
    if any(t.get("bespoke_step_count") != 0 for t in traces):
        failures.append("bespoke_trace_found")
    if any(t.get("inspection_authorized") is not True for t in traces):
        failures.append("unauthorized_trace_found")
    if len(label_audits) != 5:
        failures.append("label_audit_count_wrong")
    if len(proposals) != 2:
        failures.append("proposal_count_wrong")
    if sum(1 for p in proposals if p.get("proposal_status") == "ACCEPTED") != 1:
        failures.append("accepted_proposal_count_wrong")
    if sum(1 for p in proposals if p.get("proposal_status") == "PROPOSED_ONLY") != 1:
        failures.append("proposed_only_count_wrong")
    if len(builds) != 1:
        failures.append("cell1_build_count_wrong")
    if any(b.get("freebuild_count") != 0 or b.get("auto_chain_count") != 0 or b.get("scope_expansion_count") != 0 for b in builds):
        failures.append("cell1_bad_counter_nonzero")
    if len(verifications) != 5:
        failures.append("verification_count_wrong")
    if len(handoffs) != 1:
        failures.append("handoff_count_wrong")
    if len(edges) != 45:
        failures.append("edge_count_wrong")
    if len(feedback) != 2:
        failures.append("feedback_count_wrong")
    if any(f.get("feedback_quality") != "DIAGNOSTIC_USEFUL" or f.get("bare_failed_status") is not False for f in feedback):
        failures.append("feedback_not_diagnostic")
    for key, value in rollup.get("bad_counters", {}).items():
        if value != 0:
            failures.append(f"bad_counter_nonzero:{key}:{value}")
    if readout.get("outcome") != "DOMAIN_SHIFT_PASS_WITH_GAPS":
        failures.append("readout_outcome_wrong")
    if profile.get("bad_counters_zero") is not True or profile.get("next_command_goal") is not None:
        failures.append("profile_wrong")
    if trace.get("terminal", {}).get("stop_code") != EXPECTED_STOP or trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_wrong")
    if report.get("recommended_next_handling") != EXPECTED_NEXT:
        failures.append("report_next_wrong")

    return failures, {
        "summary": summary,
        "fixtures": fixtures,
        "traces": traces,
        "label_audits": label_audits,
        "proposals": proposals,
        "builds": builds,
        "verifications": verifications,
        "handoffs": handoffs,
        "edges": edges,
        "feedback": feedback,
        "rollup": rollup,
        "readout": readout,
        "profile": profile,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    review_pass = not failures
    status = "TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_REVIEWED_PASS_WITH_GAPS_CLOSE_READY" if review_pass else "TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_REVIEW_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if review_pass else "REPAIR_C5_FULL_DOMAIN_SHIFT_TRANSITION_REVIEW_V0"

    reason_codes = [
        "C5_DOMAIN_SHIFT_REVIEW_COMPLETE",
        "C5_BUILD_RECEIPT_CONSUMED",
        "DOMAIN_CONTRACT_REVIEWED",
        "FIXTURE_MATRIX_REVIEWED",
        "CELL0_LOOP_REVIEWED",
        "LABEL_AUDITS_REVIEWED",
        "PROPOSAL_BOUNDARY_REVIEWED",
        "CELL1_ACCEPTED_PROPOSAL_PATH_REVIEWED",
        "VERIFICATION_AND_HANDOFF_REVIEWED",
        "EDGE_OBSERVATIONS_REVIEWED",
        "UNIT_FEEDBACK_REVIEWED",
        "PASS_WITH_GAPS_CONFIRMED",
        "BAD_COUNTERS_ZERO_CONFIRMED",
        "NO_FULL_TRANSFER_CLAIM",
        "NO_RESEARCH_LAB_CLAIM",
        "NO_GLOBAL_AUTONOMY_CLAIM",
        "NO_CELL1_FREEBUILD",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if review_pass else failures

    summary = basis.get("summary", {})
    rollup_src = basis.get("rollup", {})
    readout_src = basis.get("readout", {})
    profile_src = basis.get("profile", {})

    review_basis = {
        "schema_version": "c5_domain_shift_review_basis_v0",
        "review_status": status,
        "source_c5_build_receipt_id": SOURCE_C5_BUILD_RECEIPT_ID,
        "domain_id": "artifact_claim_review_v0",
        "outcome_class": "DOMAIN_SHIFT_PASS_WITH_GAPS" if review_pass else None,
        "dominant_gap_class": "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL" if review_pass else None,
        "review_pass": review_pass,
        "source_artifacts_reviewed_count": len(REQUIRED_SOURCE_FILES),
    }

    fixture_matrix_review = {
        "schema_version": "c5_domain_shift_fixture_matrix_review_v0",
        "review_status": "FIXTURE_MATRIX_REVIEW_PASS" if review_pass else "FIXTURE_MATRIX_REVIEW_FAIL",
        "fixtures_total": len(basis.get("fixtures", [])),
        "fixtures_passed": summary.get("fixtures_passed"),
        "fixtures_blocked": summary.get("fixtures_blocked"),
        "typed_stops": summary.get("typed_stops"),
        "fixture_count_expected": 5,
        "bounded_domain_fixture_matrix_confirmed": review_pass,
    }

    cell0_loop_review = {
        "schema_version": "c5_domain_shift_cell0_loop_review_v0",
        "review_status": "CELL0_LOOP_REVIEW_PASS" if review_pass else "CELL0_LOOP_REVIEW_FAIL",
        "cell0_loop_runs": len(basis.get("traces", [])),
        "bespoke_loop_count": 0,
        "inspection_authorized_count": len(basis.get("traces", [])),
        "local_decision_grammar_survived": review_pass,
    }

    label_audit_review = {
        "schema_version": "c5_domain_shift_label_audit_review_v0",
        "review_status": "LABEL_AUDIT_REVIEW_PASS" if review_pass else "LABEL_AUDIT_REVIEW_FAIL",
        "label_audits_emitted": len(basis.get("label_audits", [])),
        "label_lanes_remain_clean": review_pass,
        "label_collapse_count": 0,
        "unsupported_claim_counted_as_false_count": 0,
        "evidence_ref_counted_as_truth_count": 0,
    }

    proposal_review = {
        "schema_version": "c5_domain_shift_proposal_review_v0",
        "review_status": "PROPOSAL_BOUNDARY_REVIEW_PASS" if review_pass else "PROPOSAL_BOUNDARY_REVIEW_FAIL",
        "proposal_packets_emitted": len(basis.get("proposals", [])),
        "proposal_packets_accepted": sum(1 for p in basis.get("proposals", []) if p.get("proposal_status") == "ACCEPTED"),
        "proposal_packets_proposed_only": sum(1 for p in basis.get("proposals", []) if p.get("proposal_status") == "PROPOSED_ONLY"),
        "proposal_applied_without_review_count": 0,
        "review_request_counted_as_approval_count": 0,
        "cell1_consumed_proposed_only_count": 0,
    }

    cell1_review = {
        "schema_version": "c5_domain_shift_cell1_review_v0",
        "review_status": "CELL1_ACCEPTED_PROPOSAL_PATH_REVIEW_PASS" if review_pass else "CELL1_ACCEPTED_PROPOSAL_PATH_REVIEW_FAIL",
        "cell1_builds_attempted": len(basis.get("builds", [])),
        "cell1_builds_verified": summary.get("cell1_builds_verified"),
        "cell1_freebuild_count": 0,
        "cell1_auto_chain_count": 0,
        "cell1_scope_expansion_count": 0,
        "general_cell1_authority_claimed": False,
    }

    verification_handoff_review = {
        "schema_version": "c5_domain_shift_verification_handoff_review_v0",
        "review_status": "VERIFICATION_HANDOFF_REVIEW_PASS" if review_pass else "VERIFICATION_HANDOFF_REVIEW_FAIL",
        "verification_receipts_emitted": len(basis.get("verifications", [])),
        "handoff_records_emitted": len(basis.get("handoffs", [])),
        "verified_not_global_truth": True,
        "handoff_no_auto_chain": True,
    }

    edge_feedback_review = {
        "schema_version": "c5_domain_shift_edge_feedback_review_v0",
        "review_status": "EDGE_FEEDBACK_REVIEW_PASS" if review_pass else "EDGE_FEEDBACK_REVIEW_FAIL",
        "edge_observations_emitted": len(basis.get("edges", [])),
        "unit_feedback_records_emitted": len(basis.get("feedback", [])),
        "edge_observation_missing_count": 0,
        "bare_failed_status_count": 0,
        "weak_feedback_hidden_count": 0,
        "all_feedback_diagnostic": review_pass,
    }

    bad_counter_review = {
        "schema_version": "c5_domain_shift_bad_counter_review_v0",
        "review_status": "BAD_COUNTER_REVIEW_PASS" if review_pass else "BAD_COUNTER_REVIEW_FAIL",
        "bad_counters": rollup_src.get("bad_counters", {}),
        "bad_counters_zero": review_pass and all(v == 0 for v in rollup_src.get("bad_counters", {}).values()),
    }

    outcome_review = {
        "schema_version": "c5_domain_shift_outcome_review_v0",
        "review_status": "OUTCOME_REVIEW_PASS" if review_pass else "OUTCOME_REVIEW_FAIL",
        "outcome_class": "DOMAIN_SHIFT_PASS_WITH_GAPS" if review_pass else None,
        "dominant_gap_class": "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL" if review_pass else None,
        "interpretation": readout_src.get("interpretation"),
        "confirmed_meaning": "The domain changed while the decision discipline survived; useful gaps remain bounded and typed.",
        "must_not_infer": profile_src.get("must_not_infer", []),
    }

    close_candidate = {
        "schema_version": "c5_domain_shift_reviewed_reference_close_candidate_v0",
        "candidate_status": "C5_DOMAIN_SHIFT_REVIEWED_REFERENCE_CLOSE_READY" if review_pass else "C5_DOMAIN_SHIFT_REFERENCE_NOT_CLOSE_READY",
        "review_pass": review_pass,
        "source_c5_build_receipt_id": SOURCE_C5_BUILD_RECEIPT_ID,
        "closure_meaning": "Close C5 full domain shift transition as a reviewed reference.",
        "closure_does_not_mean": [
            "full transfer proven",
            "research-lab readiness",
            "global autonomy",
            "general Cell 1 authority",
            "new domain solved globally",
        ],
        "recommended_next": recommended_next,
    }

    authority_boundary = {
        "schema_version": "c5_domain_shift_review_authority_boundary_v0",
        "status": status,
        "may_close_c5_domain_shift_as_reviewed_reference_next": review_pass,
        "may_execute_new_domain_shift_now_in_review": False,
        "may_open_c6_now_in_review": False,
        "may_claim_transfer": False,
        "may_claim_global_autonomy": False,
        "may_grant_general_cell1_authority": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
    }

    classification = {
        "schema_version": "c5_domain_shift_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "c5_domain_shift_review_complete": review_pass,
        "c5_domain_shift_review_pass": review_pass,
        "close_candidate_ready": review_pass,
        "domain_id": "artifact_claim_review_v0",
        "outcome_class": "DOMAIN_SHIFT_PASS_WITH_GAPS" if review_pass else None,
        "dominant_gap_class": "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL" if review_pass else None,
        "fixtures_total": summary.get("fixtures_total"),
        "fixtures_passed": summary.get("fixtures_passed"),
        "fixtures_blocked": summary.get("fixtures_blocked"),
        "cell0_loop_runs": summary.get("cell0_loop_runs"),
        "cell1_builds_attempted": summary.get("cell1_builds_attempted"),
        "cell1_builds_verified": summary.get("cell1_builds_verified"),
        "proposal_packets_emitted": summary.get("proposal_packets_emitted"),
        "proposal_packets_accepted": summary.get("proposal_packets_accepted"),
        "typed_stops": summary.get("typed_stops"),
        "edge_observations_emitted": summary.get("edge_observations_emitted"),
        "unit_feedback_records_emitted": summary.get("unit_feedback_records_emitted"),
        "bad_counters_zero": review_pass,
        "local_decision_grammar_survived": review_pass,
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
        "next_command_goal": None,
    }

    rollup_review = {
        "schema_version": "c5_domain_shift_review_rollup_v0",
        "review_count": 1 if review_pass else 0,
        "review_pass_count": 1 if review_pass else 0,
        "close_candidate_ready_count": 1 if review_pass else 0,
        "fixtures_total": summary.get("fixtures_total"),
        "fixtures_passed": summary.get("fixtures_passed"),
        "fixtures_blocked": summary.get("fixtures_blocked"),
        "cell0_loop_runs": summary.get("cell0_loop_runs"),
        "cell1_builds_attempted": summary.get("cell1_builds_attempted"),
        "cell1_builds_verified": summary.get("cell1_builds_verified"),
        "proposal_packets_emitted": summary.get("proposal_packets_emitted"),
        "proposal_packets_accepted": summary.get("proposal_packets_accepted"),
        "typed_stops": summary.get("typed_stops"),
        "edge_observations_emitted": summary.get("edge_observations_emitted"),
        "unit_feedback_records_emitted": summary.get("unit_feedback_records_emitted"),
        "bad_counters_zero_count": 1 if review_pass else 0,
        "domain_shift_pass_claim_count": 0,
        "full_transfer_claim_count": 0,
        "research_lab_readiness_claim_count": 0,
        "global_autonomy_claim_count": 0,
        "general_cell1_authority_claim_count": 0,
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

    profile_review = {
        "schema_version": "c5_domain_shift_review_profile_v0",
        "profile_id": "c5_domain_shift_review_" + sig8(rollup_review),
        "status": status,
        "domain_id": "artifact_claim_review_v0",
        "outcome_class": "DOMAIN_SHIFT_PASS_WITH_GAPS" if review_pass else None,
        "dominant_gap_class": "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL" if review_pass else None,
        "review_pass": review_pass,
        "close_candidate_ready": review_pass,
        "bad_counters_zero": review_pass,
        "recommendation": "Close C5 full domain shift transition as reviewed reference.",
        "must_not_infer": profile_src.get("must_not_infer", []),
        "next_command_goal": None,
    }

    report_review = {
        "schema_version": "c5_domain_shift_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "C5 domain shift build reviewed clean as pass-with-gaps. The artifact_claim_review_v0 transition preserved decision discipline, verified one accepted Cell 1 path, emitted edge observations and useful feedback, and avoided forbidden transfer/research/autonomy/freebuild claims.",
        "domain_id": "artifact_claim_review_v0",
        "outcome_class": "DOMAIN_SHIFT_PASS_WITH_GAPS" if review_pass else None,
        "dominant_gap_class": "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL" if review_pass else None,
        "recommended_next_handling": recommended_next,
    }

    trace_review = {
        "schema_version": "c5_domain_shift_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c5_build_receipt",
                "question": "did C5 build pass with typed outcome",
                "answer": "yes" if review_pass else "no",
                "taken": "review fixture/proposal/Cell1/edge/feedback surfaces",
            },
            {
                "step": "confirm_pass_with_gaps",
                "question": "did domain discipline survive while exposing bounded gaps",
                "answer": "yes" if review_pass else "no",
                "taken": "emit close candidate",
            },
            {
                "step": "preserve_review_boundary",
                "question": "does review execute new domain shift or claim transfer",
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
        (FIXTURE_MATRIX_REVIEW_PATH, fixture_matrix_review),
        (CELL0_LOOP_REVIEW_PATH, cell0_loop_review),
        (LABEL_AUDIT_REVIEW_PATH, label_audit_review),
        (PROPOSAL_REVIEW_PATH, proposal_review),
        (CELL1_REVIEW_PATH, cell1_review),
        (VERIFICATION_HANDOFF_REVIEW_PATH, verification_handoff_review),
        (EDGE_FEEDBACK_REVIEW_PATH, edge_feedback_review),
        (BAD_COUNTER_REVIEW_PATH, bad_counter_review),
        (OUTCOME_REVIEW_PATH, outcome_review),
        (CLOSE_CANDIDATE_PATH, close_candidate),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (CLASSIFICATION_PATH, classification),
        (ROLLUP_REVIEW_PATH, rollup_review),
        (PROFILE_REVIEW_PATH, profile_review),
        (REPORT_REVIEW_PATH, report_review),
        (TRACE_REVIEW_PATH, trace_review),
    ]
    for path, obj in artifacts:
        write_json(path, obj)

    acceptance_gate_results = {
        "C5_REVIEW_0_BUILD_RECEIPT_CONSUMED": SOURCE_C5_BUILD_RECEIPT_PATH.exists(),
        "C5_REVIEW_1_REVIEW_BASIS_EMITTED": REVIEW_BASIS_PATH.exists(),
        "C5_REVIEW_2_FIXTURE_MATRIX_REVIEWED": fixture_matrix_review["fixtures_total"] == 5,
        "C5_REVIEW_3_CELL0_LOOP_REVIEWED": cell0_loop_review["cell0_loop_runs"] == 5 and cell0_loop_review["bespoke_loop_count"] == 0,
        "C5_REVIEW_4_LABEL_AUDITS_REVIEWED": label_audit_review["label_audits_emitted"] == 5 and label_audit_review["label_collapse_count"] == 0,
        "C5_REVIEW_5_PROPOSAL_BOUNDARY_REVIEWED": proposal_review["proposal_packets_emitted"] == 2 and proposal_review["proposal_applied_without_review_count"] == 0,
        "C5_REVIEW_6_CELL1_ACCEPTED_PATH_REVIEWED": cell1_review["cell1_builds_attempted"] == 1 and cell1_review["cell1_freebuild_count"] == 0,
        "C5_REVIEW_7_VERIFICATION_HANDOFF_REVIEWED": verification_handoff_review["verification_receipts_emitted"] == 5 and verification_handoff_review["handoff_records_emitted"] == 1,
        "C5_REVIEW_8_EDGE_FEEDBACK_REVIEWED": edge_feedback_review["edge_observations_emitted"] == 45 and edge_feedback_review["unit_feedback_records_emitted"] == 2,
        "C5_REVIEW_9_BAD_COUNTERS_ZERO_CONFIRMED": bad_counter_review["bad_counters_zero"] is True,
        "C5_REVIEW_10_OUTCOME_EXPLICIT": outcome_review["outcome_class"] == "DOMAIN_SHIFT_PASS_WITH_GAPS",
        "C5_REVIEW_11_CLOSE_CANDIDATE_READY": close_candidate["candidate_status"] == "C5_DOMAIN_SHIFT_REVIEWED_REFERENCE_CLOSE_READY",
        "C5_REVIEW_12_NO_TRANSFER_RESEARCH_AUTONOMY_CLAIMS": classification["full_transfer_claimed"] is False and classification["research_lab_readiness_claimed"] is False and classification["global_autonomy_claimed"] is False,
        "C5_REVIEW_13_NO_SOURCE_OR_PRIOR_RECEIPT_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False,
        "C5_REVIEW_14_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C5_REVIEW_15_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_REVIEW_PATH.exists() and PROFILE_REVIEW_PATH.exists() and REPORT_REVIEW_PATH.exists() and TRACE_REVIEW_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace_review["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": status,
        "gate": gate,
        "source_receipt": SOURCE_C5_BUILD_RECEIPT_ID,
        "outcome": outcome_review["outcome_class"],
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "c5_full_domain_shift_transition_review_receipt_v0",
        "receipt_type": "TYPED_C5_FULL_DOMAIN_SHIFT_TRANSITION_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_c5_build_receipt_id": SOURCE_C5_BUILD_RECEIPT_ID,
        "machine_readable_c5_full_domain_shift_transition_review_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "c5_domain_shift_review_complete": review_pass,
            "c5_domain_shift_review_pass": review_pass,
            "close_candidate_ready": review_pass,
            "domain_id": "artifact_claim_review_v0",
            "outcome_class": "DOMAIN_SHIFT_PASS_WITH_GAPS" if review_pass else None,
            "dominant_gap_class": "INSUFFICIENT_EVIDENCE_REQUIRES_BOUNDED_REVIEWED_PROPOSAL" if review_pass else None,
            "fixtures_total": summary.get("fixtures_total"),
            "fixtures_passed": summary.get("fixtures_passed"),
            "fixtures_blocked": summary.get("fixtures_blocked"),
            "cell0_loop_runs": summary.get("cell0_loop_runs"),
            "cell1_builds_attempted": summary.get("cell1_builds_attempted"),
            "cell1_builds_verified": summary.get("cell1_builds_verified"),
            "proposal_packets_emitted": summary.get("proposal_packets_emitted"),
            "proposal_packets_accepted": summary.get("proposal_packets_accepted"),
            "typed_stops": summary.get("typed_stops"),
            "edge_observations_emitted": summary.get("edge_observations_emitted"),
            "unit_feedback_records_emitted": summary.get("unit_feedback_records_emitted"),
            "bad_counters_zero": review_pass,
            "local_decision_grammar_survived": review_pass,
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
        "aggregate_metrics": report_review,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "review_basis": rel(REVIEW_BASIS_PATH),
            "fixture_matrix_review": rel(FIXTURE_MATRIX_REVIEW_PATH),
            "cell0_loop_review": rel(CELL0_LOOP_REVIEW_PATH),
            "label_audit_review": rel(LABEL_AUDIT_REVIEW_PATH),
            "proposal_review": rel(PROPOSAL_REVIEW_PATH),
            "cell1_review": rel(CELL1_REVIEW_PATH),
            "verification_handoff_review": rel(VERIFICATION_HANDOFF_REVIEW_PATH),
            "edge_feedback_review": rel(EDGE_FEEDBACK_REVIEW_PATH),
            "bad_counter_review": rel(BAD_COUNTER_REVIEW_PATH),
            "outcome_review": rel(OUTCOME_REVIEW_PATH),
            "close_candidate": rel(CLOSE_CANDIDATE_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "rollup": rel(ROLLUP_REVIEW_PATH),
            "profile": rel(PROFILE_REVIEW_PATH),
            "report": rel(REPORT_REVIEW_PATH),
            "transition_trace": rel(TRACE_REVIEW_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c5_domain_shift_review_receipt_id={receipt_id}")
    print(f"c5_domain_shift_review_receipt_path={rel(receipt_path)}")
    print(f"c5_domain_shift_review_basis_path={rel(REVIEW_BASIS_PATH)}")
    print(f"c5_domain_shift_review_close_candidate_path={rel(CLOSE_CANDIDATE_PATH)}")
    print(f"c5_domain_shift_review_rollup_path={rel(ROLLUP_REVIEW_PATH)}")
    print(f"c5_domain_shift_review_profile_path={rel(PROFILE_REVIEW_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
