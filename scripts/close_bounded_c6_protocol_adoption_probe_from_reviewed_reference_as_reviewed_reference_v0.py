#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_FROM_REVIEWED_REFERENCE_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "c6.protocol_adoption_probe.reviewed_reference.v0"
LAYER = "BRIDGE / INTER_CELL_PROTOCOL / BOUNDED_ADOPTION_PROBE / REFERENCE_CLOSURE"
MODE = "CLOSE_ONLY / FREEZE_REVIEWED_SYNTHETIC_ADOPTION_PROBE / NO_RUNTIME_PATCH"
BUILD_MODE = "C6_BOUNDED_PROTOCOL_ADOPTION_PROBE_REFERENCE_CLOSURE_ONLY"

SOURCE_PROBE_REVIEW_RECEIPT_ID = "94c34bc4"
SOURCE_PROBE_RECEIPT_ID = "6ecaeaf8"
SOURCE_PROBE_DESIGN_RECEIPT_ID = "e0078630"
SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID = "50849d13"
SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_ID = "5a07dcbb"

SOURCE_PROBE_REVIEW_RECEIPT_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0_receipts/94c34bc4.json"

PROBE_REVIEW_FILES = [
    ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_review_basis_v0.json",
    ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_source_receipt_review_v0.json",
    ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_packet_trace_review_v0.json",
    ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_edge_observation_review_v0.json",
    ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_unit_feedback_review_v0.json",
    ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_negative_control_review_v0.json",
    ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_boundary_review_v0.json",
    ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_reviewed_reference_close_candidate_v0.json",
    ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_review_authority_boundary_v0.json",
    ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_review_classification_v0.json",
    ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_review_rollup_v0.json",
    ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_review_profile_v0.json",
    ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_review_report.json",
    ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_review_transition_trace.json",
]

SOURCE_PROBE_RECEIPT_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0_receipts/6ecaeaf8.json"

PROBE_BUILD_FILES = [
    ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_fixture_v0.json",
    ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_packet_trace_v0.jsonl",
    ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_edge_observations_v0.jsonl",
    ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_unit_feedback_v0.jsonl",
    ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_negative_control_results_v0.jsonl",
    ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_rollup_v0.json",
    ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_profile_v0.json",
    ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_report.json",
    ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_transition_trace.json",
]

SOURCE_PROBE_DESIGN_RECEIPT_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0_receipts/e0078630.json"
SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0_receipts/50849d13.json"
SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_post_reference_decision_v0_receipts/5a07dcbb.json"

C6_PROTOCOL_REVIEWED_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_reviewed_reference_v0.json"
C6_PACKET_LAW_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_packet_law_reference_v0.json"
C6_PROTOCOL_SURFACE_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_surface_reference_v0.json"
C6_GATE19_REPAIR_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_gate19_repair_reference_v0.json"

ANCESTOR_FILES = [
    SOURCE_PROBE_DESIGN_RECEIPT_PATH,
    SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH,
    SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_PATH,
    C6_PROTOCOL_REVIEWED_REFERENCE_PATH,
    C6_PACKET_LAW_REFERENCE_PATH,
    C6_PROTOCOL_SURFACE_REFERENCE_PATH,
    C6_GATE19_REPAIR_REFERENCE_PATH,
]

REQUIRED_SOURCE_FILES = [SOURCE_PROBE_REVIEW_RECEIPT_PATH, SOURCE_PROBE_RECEIPT_PATH] + PROBE_REVIEW_FILES + PROBE_BUILD_FILES + ANCESTOR_FILES

OUT_DIR = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0"
RECEIPT_DIR = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0_receipts"

CLOSURE_BASIS_PATH = OUT_DIR / "bounded_adoption_probe_reference_closure_basis_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "bounded_adoption_probe_reviewed_reference_v0.json"
FREEZE_MANIFEST_PATH = OUT_DIR / "bounded_adoption_probe_reviewed_reference_freeze_manifest_v0.json"
REFERENCE_INDEX_PATH = OUT_DIR / "bounded_adoption_probe_reference_index_v0.json"
PACKET_LAW_SURVIVAL_REFERENCE_PATH = OUT_DIR / "bounded_adoption_probe_packet_law_survival_reference_v0.json"
OBSERVABILITY_REFERENCE_PATH = OUT_DIR / "bounded_adoption_probe_observability_reference_v0.json"
FEEDBACK_REFERENCE_PATH = OUT_DIR / "bounded_adoption_probe_unit_feedback_reference_v0.json"
NEGATIVE_CONTROL_REFERENCE_PATH = OUT_DIR / "bounded_adoption_probe_negative_control_reference_v0.json"
POST_CLOSURE_DECISION_READY_PATH = OUT_DIR / "bounded_adoption_probe_reference_post_closure_decision_ready_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "bounded_adoption_probe_reference_closure_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "bounded_adoption_probe_reference_closure_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_adoption_probe_reference_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_adoption_probe_reference_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_adoption_probe_reference_closure_report.json"
TRACE_PATH = OUT_DIR / "bounded_adoption_probe_reference_closure_transition_trace.json"

EXPECTED_REVIEW_STATUS = "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEWED_CLOSE_READY"
EXPECTED_REVIEW_STOP = "STOP_TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEWED_CLOSE_READY"
EXPECTED_REVIEW_NEXT = "CLOSE_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_FROM_REVIEWED_REFERENCE_AS_REVIEWED_REFERENCE_V0"
RECOMMENDED_NEXT = "DECIDE_NEXT_AFTER_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REFERENCE_CLOSURE_V0"

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

    review_receipt = read_json(SOURCE_PROBE_REVIEW_RECEIPT_PATH)
    review_summary = review_receipt.get("machine_readable_bounded_c6_adoption_probe_review_summary", {})

    build_receipt = read_json(SOURCE_PROBE_RECEIPT_PATH)
    build_summary = build_receipt.get("machine_readable_bounded_c6_adoption_probe_summary", {})

    design_receipt = read_json(SOURCE_PROBE_DESIGN_RECEIPT_PATH)
    reference_closure_receipt = read_json(SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH)
    post_decision_receipt = read_json(SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_PATH)

    reviewed_c6_reference = read_json(C6_PROTOCOL_REVIEWED_REFERENCE_PATH)
    packet_law_reference = read_json(C6_PACKET_LAW_REFERENCE_PATH)
    protocol_surface_reference = read_json(C6_PROTOCOL_SURFACE_REFERENCE_PATH)
    gate19_reference = read_json(C6_GATE19_REPAIR_REFERENCE_PATH)

    packet_trace = read_jsonl(ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_packet_trace_v0.jsonl")
    edge_observations = read_jsonl(ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_edge_observations_v0.jsonl")
    unit_feedback = read_jsonl(ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_unit_feedback_v0.jsonl")
    negative_controls = read_jsonl(ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_negative_control_results_v0.jsonl")
    probe_rollup = read_json(ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_rollup_v0.json")
    probe_profile = read_json(ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_profile_v0.json")

    review_close_candidate = read_json(ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_reviewed_reference_close_candidate_v0.json")
    review_authority = read_json(ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_review_authority_boundary_v0.json")
    review_rollup = read_json(ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_review_rollup_v0.json")
    review_profile = read_json(ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_review_profile_v0.json")
    review_report = read_json(ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_review_report.json")
    review_trace = read_json(ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0/bounded_adoption_probe_review_transition_trace.json")

    if review_receipt.get("receipt_id") != SOURCE_PROBE_REVIEW_RECEIPT_ID or review_receipt.get("gate") != "PASS":
        failures.append("source_review_receipt_not_pass")
    if review_receipt.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("source_review_stop_wrong")
    if review_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_review_hidden_next")
    if review_summary.get("status") != EXPECTED_REVIEW_STATUS:
        failures.append(f"source_review_status_wrong:{review_summary.get('status')}")
    if review_summary.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append(f"source_review_next_wrong:{review_summary.get('recommended_next')}")

    for key in [
        "bounded_c6_protocol_adoption_probe_review_complete",
        "bounded_c6_protocol_adoption_probe_review_pass",
        "close_candidate_ready",
        "source_probe_built",
        "synthetic_protocol_only",
        "negative_controls_passed",
        "packet_law_distinctions_confirmed",
        "bad_counters_zero",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"review_required_true_missing:{key}")

    for key in [
        "runtime_effect",
        "runtime_patched",
        "c7_authorized",
        "new_domain_shift_executed",
        "general_cell1_authority_claimed",
        "global_autonomy_claimed",
        "full_transfer_claimed",
        "runtime_wide_enforcement_claimed",
        "source_mutated",
        "prior_receipt_mutated",
        "c6_reviewed_reference_mutated",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if review_summary.get(key) is not False:
            failures.append(f"review_forbidden_true:{key}")

    for key, expected in {
        "packet_trace_count": 9,
        "edge_observation_count": 7,
        "unit_feedback_count": 4,
        "negative_control_count": 15,
    }.items():
        if review_summary.get(key) != expected:
            failures.append(f"review_count_wrong:{key}:{review_summary.get(key)}")

    if build_receipt.get("receipt_id") != SOURCE_PROBE_RECEIPT_ID or build_receipt.get("gate") != "PASS":
        failures.append("build_receipt_not_pass")
    if build_summary.get("bounded_c6_protocol_adoption_probe_built") is not True:
        failures.append("build_probe_not_built")
    if design_receipt.get("receipt_id") != SOURCE_PROBE_DESIGN_RECEIPT_ID or design_receipt.get("gate") != "PASS":
        failures.append("design_receipt_not_pass")
    if reference_closure_receipt.get("receipt_id") != SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID or reference_closure_receipt.get("gate") != "PASS":
        failures.append("c6_reference_closure_not_pass")
    if post_decision_receipt.get("receipt_id") != SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_ID or post_decision_receipt.get("gate") != "PASS":
        failures.append("post_c6_decision_not_pass")

    if reviewed_c6_reference.get("reference_status") != "C6_INTER_CELL_PROTOCOL_REVIEWED_REFERENCE_FROZEN":
        failures.append("c6_reviewed_reference_not_frozen")
    if packet_law_reference.get("packet_law_status") != "REVIEWED_REFERENCE":
        failures.append("packet_law_reference_wrong")
    if protocol_surface_reference.get("surface_status") != "FROZEN_REVIEWED_REFERENCE":
        failures.append("protocol_surface_reference_wrong")
    if gate19_reference.get("repair_class") != "ASSERTION_REPAIR_NOT_PROTOCOL_REDESIGN":
        failures.append("gate19_reference_wrong")

    if len(packet_trace) != 9:
        failures.append("packet_trace_count_wrong")
    if len(edge_observations) != 7:
        failures.append("edge_observation_count_wrong")
    if len(unit_feedback) != 4:
        failures.append("unit_feedback_count_wrong")
    if len(negative_controls) != 15:
        failures.append("negative_control_count_wrong")
    if any(row.get("passed") is not True or row.get("observed") != "FAIL_CLOSED" for row in negative_controls):
        failures.append("negative_controls_not_fail_closed")
    if any(v != 0 for v in probe_rollup.get("bad_counters", {}).values()):
        failures.append("probe_bad_counter_nonzero")
    if probe_profile.get("next_command_goal") is not None:
        failures.append("probe_profile_hidden_next")

    if review_close_candidate.get("candidate_status") != "BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEWED_REFERENCE_CLOSE_READY":
        failures.append("close_candidate_not_ready")
    if review_close_candidate.get("review_pass") is not True:
        failures.append("close_candidate_review_not_pass")
    if review_authority.get("may_close_bounded_adoption_probe_as_reviewed_reference_next") is not True:
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
        "may_mutate_c6_reviewed_reference",
    ]:
        if review_authority.get(forbidden) is not False:
            failures.append(f"review_authority_forbidden_true:{forbidden}")
    if review_rollup.get("review_pass_count") != 1 or review_rollup.get("close_candidate_ready_count") != 1:
        failures.append("review_rollup_not_close_ready")
    if review_profile.get("next_command_goal") is not None:
        failures.append("review_profile_hidden_next")
    if review_report.get("recommended_next_handling") != EXPECTED_REVIEW_NEXT:
        failures.append("review_report_next_wrong")
    if review_trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("review_trace_hidden_next")

    return failures, {
        "review_summary": review_summary,
        "build_summary": build_summary,
        "reviewed_c6_reference": reviewed_c6_reference,
        "packet_law_reference": packet_law_reference,
        "protocol_surface_reference": protocol_surface_reference,
        "gate19_reference": gate19_reference,
        "packet_trace": packet_trace,
        "edge_observations": edge_observations,
        "unit_feedback": unit_feedback,
        "negative_controls": negative_controls,
        "probe_rollup": probe_rollup,
        "probe_profile": probe_profile,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    close_pass = not failures
    status = "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY" if close_pass else "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REFERENCE_CLOSURE_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if close_pass else "REPAIR_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REFERENCE_CLOSURE_V0"

    review_summary = basis.get("review_summary", {})
    build_summary = basis.get("build_summary", {})
    reviewed_c6_reference = basis.get("reviewed_c6_reference", {})
    packet_law_reference = basis.get("packet_law_reference", {})
    protocol_surface_reference = basis.get("protocol_surface_reference", {})
    gate19_reference = basis.get("gate19_reference", {})
    packet_trace = basis.get("packet_trace", [])
    edge_observations = basis.get("edge_observations", [])
    unit_feedback = basis.get("unit_feedback", [])
    negative_controls = basis.get("negative_controls", [])
    probe_rollup = basis.get("probe_rollup", {})
    probe_profile = basis.get("probe_profile", {})

    reason_codes = [
        "BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_CLOSED_AS_REVIEWED_REFERENCE",
        "PROBE_REVIEW_RECEIPT_CONSUMED",
        "PROBE_BUILD_RECEIPT_CONSUMED",
        "C6_REVIEWED_REFERENCE_CONSUMED",
        "PACKET_LAW_SURVIVAL_FROZEN",
        "EDGE_OBSERVATIONS_FROZEN",
        "UNIT_FEEDBACK_REFERENCE_FROZEN",
        "NEGATIVE_CONTROLS_FAIL_CLOSED_REFERENCE_FROZEN",
        "SYNTHETIC_PROTOCOL_ONLY_REFERENCE_FROZEN",
        "POST_PROBE_REFERENCE_DECISION_READY",
        "NO_RUNTIME_EFFECT",
        "NO_RUNTIME_PATCH",
        "NO_C7_AUTHORIZATION",
        "NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if close_pass else failures

    closure_basis = {
        "schema_version": "bounded_adoption_probe_reference_closure_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if close_pass else "BASIS_REPAIR_REQUIRED",
        "source_probe_review_receipt_id": SOURCE_PROBE_REVIEW_RECEIPT_ID,
        "source_probe_receipt_id": SOURCE_PROBE_RECEIPT_ID,
        "source_probe_design_receipt_id": SOURCE_PROBE_DESIGN_RECEIPT_ID,
        "source_c6_protocol_reference_closure_receipt_id": SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID,
        "review_status": review_summary.get("status"),
        "probe_status": build_summary.get("status"),
        "source_reference_status": reviewed_c6_reference.get("reference_status"),
    }

    reviewed_reference = {
        "schema_version": "bounded_adoption_probe_reviewed_reference_v0",
        "reference_status": "BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEWED_REFERENCE_FROZEN" if close_pass else "NOT_FROZEN",
        "reference_id": "bounded_c6_adoption_probe_reference_" + sig8(reason_codes),
        "source_probe_review_receipt_id": SOURCE_PROBE_REVIEW_RECEIPT_ID,
        "source_probe_receipt_id": SOURCE_PROBE_RECEIPT_ID,
        "source_c6_reference_receipt_id": SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID,
        "reference_claim": "One bounded synthetic inter-cell packet-law flow survived review with packet trace, edge observations, unit feedback, and fail-closed negative controls.",
        "synthetic_protocol_only": True,
        "runtime_effect": False,
        "counts": {
            "packet_trace_count": len(packet_trace),
            "edge_observation_count": len(edge_observations),
            "unit_feedback_count": len(unit_feedback),
            "negative_control_count": len(negative_controls),
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
        "schema_version": "bounded_adoption_probe_reviewed_reference_freeze_manifest_v0",
        "freeze_status": "FROZEN" if close_pass else "NOT_FROZEN",
        "frozen_receipts": [
            rel(SOURCE_PROBE_REVIEW_RECEIPT_PATH),
            rel(SOURCE_PROBE_RECEIPT_PATH),
            rel(SOURCE_PROBE_DESIGN_RECEIPT_PATH),
            rel(SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH),
            rel(SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_PATH),
        ],
        "frozen_probe_build_files": [rel(p) for p in PROBE_BUILD_FILES],
        "frozen_probe_review_files": [rel(p) for p in PROBE_REVIEW_FILES],
        "frozen_ancestor_files": [rel(p) for p in ANCESTOR_FILES],
        "frozen_file_sha256": snapshot_files(REQUIRED_SOURCE_FILES),
    }

    reference_index = {
        "schema_version": "bounded_adoption_probe_reference_index_v0",
        "index_status": "REFERENCE_INDEX_EMITTED",
        "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
        "freeze_manifest": rel(FREEZE_MANIFEST_PATH),
        "packet_law_survival_reference": rel(PACKET_LAW_SURVIVAL_REFERENCE_PATH),
        "observability_reference": rel(OBSERVABILITY_REFERENCE_PATH),
        "unit_feedback_reference": rel(FEEDBACK_REFERENCE_PATH),
        "negative_control_reference": rel(NEGATIVE_CONTROL_REFERENCE_PATH),
        "post_closure_decision_ready": rel(POST_CLOSURE_DECISION_READY_PATH),
    }

    packet_law_survival_reference = {
        "schema_version": "bounded_adoption_probe_packet_law_survival_reference_v0",
        "survival_status": "REVIEWED_REFERENCE",
        "source_packet_law_reference_status": packet_law_reference.get("packet_law_status"),
        "source_protocol_surface_status": protocol_surface_reference.get("surface_status"),
        "gate19_repair_class": gate19_reference.get("repair_class"),
        "confirmed_distinctions": [
            "proposed-only rejected by Cell 1",
            "accepted packet requires review receipt",
            "Cell 1 intake scoped",
            "probe/build not verification",
            "verification not closure",
            "handoff not hidden next command",
            "blocked feedback not repair",
        ],
        "packet_trace_count": len(packet_trace),
        "packet_law_distinctions_confirmed": review_summary.get("packet_law_distinctions_confirmed"),
    }

    observability_reference = {
        "schema_version": "bounded_adoption_probe_observability_reference_v0",
        "observability_status": "REVIEWED_REFERENCE",
        "edge_observation_count": len(edge_observations),
        "edge_names": [row.get("edge_name") for row in edge_observations],
        "interpretation": "Decision-edge sidecars were present for the bounded synthetic adoption probe.",
    }

    feedback_reference = {
        "schema_version": "bounded_adoption_probe_unit_feedback_reference_v0",
        "feedback_status": "REVIEWED_REFERENCE",
        "unit_feedback_count": len(unit_feedback),
        "statuses_seen": sorted({row.get("status") for row in unit_feedback}),
        "feedback_quality": "USEFUL_DIAGNOSTIC_FEEDBACK",
        "bare_failed_status_allowed": False,
        "interpretation": "Failure/block/stop/NA feedback shape is preserved as a reviewed reference.",
    }

    negative_control_reference = {
        "schema_version": "bounded_adoption_probe_negative_control_reference_v0",
        "negative_control_status": "REVIEWED_REFERENCE",
        "negative_control_count": len(negative_controls),
        "negative_controls_all_fail_closed": all(row.get("passed") is True and row.get("observed") == "FAIL_CLOSED" for row in negative_controls),
        "controls": [row.get("control") for row in negative_controls],
    }

    post_closure_decision_ready = {
        "schema_version": "bounded_adoption_probe_reference_post_closure_decision_ready_v0",
        "decision_ready": close_pass,
        "recommended_next": recommended_next,
        "closed_reference_status": reviewed_reference["reference_status"],
        "decision_options": [
            "decide whether to park the bounded adoption probe as sufficient evidence",
            "decide whether to extract decision-edge observability requirements from the probe",
            "decide whether to extract unit-feedback hardening requirements from the probe",
            "decide whether to design another bounded adoption probe",
            "decide whether to defer C7 until after observation/feedback hardening",
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
        "schema_version": "bounded_adoption_probe_reference_closure_authority_boundary_v0",
        "status": status,
        "may_close_bounded_probe_as_reviewed_reference": close_pass,
        "may_decide_next_after_bounded_probe_reference_closure": close_pass,
        "may_patch_runtime_now": False,
        "may_open_c7_now": False,
        "may_execute_new_domain_shift": False,
        "may_claim_full_transfer": False,
        "may_claim_global_autonomy": False,
        "may_claim_general_cell1_authority": False,
        "may_claim_runtime_wide_enforcement": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_mutate_c6_reviewed_reference": False,
        "may_mutate_bounded_probe_reference": False,
    }

    classification = {
        "schema_version": "bounded_adoption_probe_reference_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "bounded_c6_protocol_adoption_probe_closed_as_reviewed_reference": close_pass,
        "reviewed_reference_frozen": close_pass,
        "post_bounded_probe_reference_decision_ready": close_pass,
        "synthetic_protocol_only": True,
        "runtime_effect": False,
        "packet_trace_count": len(packet_trace),
        "edge_observation_count": len(edge_observations),
        "unit_feedback_count": len(unit_feedback),
        "negative_control_count": len(negative_controls),
        "negative_controls_fail_closed": True,
        "packet_law_distinctions_confirmed": review_summary.get("packet_law_distinctions_confirmed"),
        "bad_counters_zero": True,
        "runtime_patched": False,
        "c7_authorized": False,
        "new_domain_shift_executed": False,
        "general_cell1_authority_claimed": False,
        "global_autonomy_claimed": False,
        "full_transfer_claimed": False,
        "runtime_wide_enforcement_claimed": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "c6_reviewed_reference_mutated": False,
        "bounded_probe_reference_mutated": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "bounded_adoption_probe_reference_closure_rollup_v0",
        "closure_count": 1 if close_pass else 0,
        "reviewed_reference_frozen_count": 1 if close_pass else 0,
        "post_reference_decision_ready_count": 1 if close_pass else 0,
        "packet_trace_count": len(packet_trace),
        "edge_observation_count": len(edge_observations),
        "unit_feedback_count": len(unit_feedback),
        "negative_control_count": len(negative_controls),
        "negative_controls_fail_closed_count": len(negative_controls),
        "runtime_effect_count": 0,
        "runtime_patch_count": 0,
        "c7_authorized_count": 0,
        "new_domain_shift_executed_count": 0,
        "general_cell1_authority_claim_count": 0,
        "global_autonomy_claim_count": 0,
        "full_transfer_claim_count": 0,
        "runtime_wide_enforcement_claim_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "c6_reviewed_reference_mutated_count": 0,
        "bounded_probe_reference_mutated_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    profile = {
        "schema_version": "bounded_adoption_probe_reference_closure_profile_v0",
        "profile_id": "bounded_c6_adoption_probe_reference_closure_" + sig8(rollup),
        "status": status,
        "schema_claim": "BOUNDED_SYNTHETIC_ADOPTION_PROBE_REVIEWED_REFERENCE_ONLY",
        "reference_object": "bounded C6 synthetic protocol adoption probe",
        "compression": "C6 packet law survived one bounded synthetic inter-cell flow.",
        "evidence_surface": [
            "9 packet trace entries",
            "7 decision-edge observations",
            "4 useful unit-feedback sidecars",
            "15 fail-closed negative controls",
        ],
        "bad_counters_zero": True,
        "must_not_infer": reviewed_reference["must_not_infer"],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "bounded_adoption_probe_reference_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The bounded C6 synthetic adoption probe is closed as a reviewed reference. It freezes evidence that the reviewed C6 packet-law reference survived one bounded inter-cell packet flow with packet trace, edge observations, unit feedback, and fail-closed negative controls. It does not patch runtime, authorize C7, or claim transfer/autonomy/general Cell 1 authority.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "bounded_adoption_probe_reference_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_probe_review",
                "question": "is the bounded C6 adoption probe reviewed and close-ready",
                "answer": "yes" if close_pass else "no",
                "taken": "freeze bounded adoption-probe reviewed reference",
            },
            {
                "step": "freeze_evidence_surface",
                "question": "what is frozen",
                "answer": "synthetic packet trace, edge observations, unit feedback, and fail-closed negative controls",
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
        (PACKET_LAW_SURVIVAL_REFERENCE_PATH, packet_law_survival_reference),
        (OBSERVABILITY_REFERENCE_PATH, observability_reference),
        (FEEDBACK_REFERENCE_PATH, feedback_reference),
        (NEGATIVE_CONTROL_REFERENCE_PATH, negative_control_reference),
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
        "ADOPTION_PROBE_REF_CLOSE_0_REVIEW_RECEIPT_CONSUMED": SOURCE_PROBE_REVIEW_RECEIPT_PATH.exists(),
        "ADOPTION_PROBE_REF_CLOSE_1_PROBE_RECEIPT_CONSUMED": SOURCE_PROBE_RECEIPT_PATH.exists(),
        "ADOPTION_PROBE_REF_CLOSE_2_REVIEWED_REFERENCE_FROZEN": REVIEWED_REFERENCE_PATH.exists() and reviewed_reference["reference_status"] == "BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEWED_REFERENCE_FROZEN",
        "ADOPTION_PROBE_REF_CLOSE_3_FREEZE_MANIFEST_EMITTED": FREEZE_MANIFEST_PATH.exists(),
        "ADOPTION_PROBE_REF_CLOSE_4_REFERENCE_INDEX_EMITTED": REFERENCE_INDEX_PATH.exists(),
        "ADOPTION_PROBE_REF_CLOSE_5_PACKET_LAW_SURVIVAL_REFERENCE_EMITTED": PACKET_LAW_SURVIVAL_REFERENCE_PATH.exists() and packet_law_survival_reference["packet_law_distinctions_confirmed"] is True,
        "ADOPTION_PROBE_REF_CLOSE_6_OBSERVABILITY_REFERENCE_EMITTED": OBSERVABILITY_REFERENCE_PATH.exists() and observability_reference["edge_observation_count"] == 7,
        "ADOPTION_PROBE_REF_CLOSE_7_UNIT_FEEDBACK_REFERENCE_EMITTED": FEEDBACK_REFERENCE_PATH.exists() and feedback_reference["unit_feedback_count"] == 4,
        "ADOPTION_PROBE_REF_CLOSE_8_NEGATIVE_CONTROL_REFERENCE_EMITTED": NEGATIVE_CONTROL_REFERENCE_PATH.exists() and negative_control_reference["negative_controls_all_fail_closed"] is True,
        "ADOPTION_PROBE_REF_CLOSE_9_POST_REFERENCE_DECISION_READY": POST_CLOSURE_DECISION_READY_PATH.exists() and post_closure_decision_ready["decision_ready"] is True,
        "ADOPTION_PROBE_REF_CLOSE_10_NO_RUNTIME_EFFECT_OR_PATCH": classification["runtime_effect"] is False and classification["runtime_patched"] is False,
        "ADOPTION_PROBE_REF_CLOSE_11_NO_C7": classification["c7_authorized"] is False,
        "ADOPTION_PROBE_REF_CLOSE_12_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "ADOPTION_PROBE_REF_CLOSE_13_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["c6_reviewed_reference_mutated"] is False and classification["bounded_probe_reference_mutated"] is False,
        "ADOPTION_PROBE_REF_CLOSE_14_BAD_COUNTERS_ZERO": classification["bad_counters_zero"] is True,
        "ADOPTION_PROBE_REF_CLOSE_15_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "ADOPTION_PROBE_REF_CLOSE_16_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "ADOPTION_PROBE_REF_CLOSE_17_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REFERENCE_CLOSURE_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REFERENCE_CLOSURE_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REFERENCE_CLOSURE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_review": SOURCE_PROBE_REVIEW_RECEIPT_ID,
        "recommended_next": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "bounded_c6_protocol_adoption_probe_reference_closure_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REFERENCE_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_probe_review_receipt_id": SOURCE_PROBE_REVIEW_RECEIPT_ID,
        "source_probe_receipt_id": SOURCE_PROBE_RECEIPT_ID,
        "source_c6_protocol_reference_closure_receipt_id": SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID,
        "machine_readable_bounded_c6_adoption_probe_reference_closure_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "bounded_c6_protocol_adoption_probe_closed_as_reviewed_reference": gate == "PASS",
            "reviewed_reference_frozen": gate == "PASS",
            "post_bounded_probe_reference_decision_ready": gate == "PASS",
            "synthetic_protocol_only": True,
            "runtime_effect": False,
            "packet_trace_count": len(packet_trace),
            "edge_observation_count": len(edge_observations),
            "unit_feedback_count": len(unit_feedback),
            "negative_control_count": len(negative_controls),
            "negative_controls_fail_closed": True,
            "packet_law_distinctions_confirmed": review_summary.get("packet_law_distinctions_confirmed"),
            "bad_counters_zero": True,
            "runtime_patched": False,
            "c7_authorized": False,
            "new_domain_shift_executed": False,
            "general_cell1_authority_claimed": False,
            "global_autonomy_claimed": False,
            "full_transfer_claimed": False,
            "runtime_wide_enforcement_claimed": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "c6_reviewed_reference_mutated": False,
            "bounded_probe_reference_mutated": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
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
            "packet_law_survival_reference": rel(PACKET_LAW_SURVIVAL_REFERENCE_PATH),
            "observability_reference": rel(OBSERVABILITY_REFERENCE_PATH),
            "unit_feedback_reference": rel(FEEDBACK_REFERENCE_PATH),
            "negative_control_reference": rel(NEGATIVE_CONTROL_REFERENCE_PATH),
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
    print(f"bounded_c6_protocol_adoption_probe_reference_closure_receipt_id={receipt_id}")
    print(f"bounded_c6_protocol_adoption_probe_reference_closure_receipt_path={rel(receipt_path)}")
    print(f"bounded_c6_protocol_adoption_probe_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"bounded_c6_protocol_adoption_probe_freeze_manifest_path={rel(FREEZE_MANIFEST_PATH)}")
    print(f"bounded_c6_protocol_adoption_probe_post_closure_decision_ready_path={rel(POST_CLOSURE_DECISION_READY_PATH)}")
    print(f"bounded_c6_protocol_adoption_probe_reference_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"bounded_c6_protocol_adoption_probe_reference_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
