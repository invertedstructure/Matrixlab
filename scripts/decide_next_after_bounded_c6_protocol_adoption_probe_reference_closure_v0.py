#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_AFTER_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REFERENCE_CLOSURE_V0"
TARGET_UNIT_ID = "c6.bounded_adoption_probe.reference.post_closure_decision.v0"
LAYER = "BRIDGE / INTER_CELL_PROTOCOL / BOUNDED_ADOPTION_PROBE / POST_REFERENCE_DECISION"
MODE = "DECIDE_ONLY / SELECT_NEXT_BRANCH / NO_RUNTIME_PATCH"
BUILD_MODE = "POST_BOUNDED_C6_ADOPTION_PROBE_REFERENCE_DECISION_ONLY"

SOURCE_REF_CLOSE_RECEIPT_ID = "ac9451cc"
SOURCE_REF_CLOSE_RECEIPT_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0_receipts/ac9451cc.json"

PROBE_REFERENCE_CLOSURE_BASIS_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_reference_closure_basis_v0.json"
PROBE_REVIEWED_REFERENCE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_reviewed_reference_v0.json"
PROBE_FREEZE_MANIFEST_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_reviewed_reference_freeze_manifest_v0.json"
PROBE_REFERENCE_INDEX_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_reference_index_v0.json"
PROBE_PACKET_LAW_SURVIVAL_REFERENCE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_packet_law_survival_reference_v0.json"
PROBE_OBSERVABILITY_REFERENCE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_observability_reference_v0.json"
PROBE_UNIT_FEEDBACK_REFERENCE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_unit_feedback_reference_v0.json"
PROBE_NEGATIVE_CONTROL_REFERENCE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_negative_control_reference_v0.json"
PROBE_POST_CLOSURE_DECISION_READY_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_reference_post_closure_decision_ready_v0.json"
PROBE_REFERENCE_AUTHORITY_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_reference_closure_authority_boundary_v0.json"
PROBE_REFERENCE_CLASSIFICATION_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_reference_closure_classification_v0.json"
PROBE_REFERENCE_ROLLUP_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_reference_closure_rollup_v0.json"
PROBE_REFERENCE_PROFILE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_reference_closure_profile_v0.json"
PROBE_REFERENCE_REPORT_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_reference_closure_report.json"
PROBE_REFERENCE_TRACE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_reference_closure_transition_trace.json"

SOURCE_PROBE_REVIEW_RECEIPT_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0_receipts/94c34bc4.json"
SOURCE_PROBE_RECEIPT_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0_receipts/6ecaeaf8.json"
SOURCE_PROBE_DESIGN_RECEIPT_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0_receipts/e0078630.json"
SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0_receipts/50849d13.json"

PROBE_EDGE_OBSERVATIONS_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_edge_observations_v0.jsonl"
PROBE_UNIT_FEEDBACK_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_unit_feedback_v0.jsonl"
PROBE_PACKET_TRACE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_packet_trace_v0.jsonl"
PROBE_NEGATIVE_CONTROL_RESULTS_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_negative_control_results_v0.jsonl"

REQUIRED_SOURCE_FILES = [
    SOURCE_REF_CLOSE_RECEIPT_PATH,
    PROBE_REFERENCE_CLOSURE_BASIS_PATH,
    PROBE_REVIEWED_REFERENCE_PATH,
    PROBE_FREEZE_MANIFEST_PATH,
    PROBE_REFERENCE_INDEX_PATH,
    PROBE_PACKET_LAW_SURVIVAL_REFERENCE_PATH,
    PROBE_OBSERVABILITY_REFERENCE_PATH,
    PROBE_UNIT_FEEDBACK_REFERENCE_PATH,
    PROBE_NEGATIVE_CONTROL_REFERENCE_PATH,
    PROBE_POST_CLOSURE_DECISION_READY_PATH,
    PROBE_REFERENCE_AUTHORITY_PATH,
    PROBE_REFERENCE_CLASSIFICATION_PATH,
    PROBE_REFERENCE_ROLLUP_PATH,
    PROBE_REFERENCE_PROFILE_PATH,
    PROBE_REFERENCE_REPORT_PATH,
    PROBE_REFERENCE_TRACE_PATH,
    SOURCE_PROBE_REVIEW_RECEIPT_PATH,
    SOURCE_PROBE_RECEIPT_PATH,
    SOURCE_PROBE_DESIGN_RECEIPT_PATH,
    SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH,
    PROBE_EDGE_OBSERVATIONS_PATH,
    PROBE_UNIT_FEEDBACK_PATH,
    PROBE_PACKET_TRACE_PATH,
    PROBE_NEGATIVE_CONTROL_RESULTS_PATH,
]

OUT_DIR = ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0"
RECEIPT_DIR = ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0_receipts"

DECISION_BASIS_PATH = OUT_DIR / "post_bounded_probe_reference_decision_basis_v0.json"
DECISION_OPTIONS_PATH = OUT_DIR / "post_bounded_probe_reference_decision_options_v0.json"
SELECTED_BRANCH_PATH = OUT_DIR / "post_bounded_probe_reference_selected_branch_v0.json"
OBSERVABILITY_EXTRACTION_TARGET_PATH = OUT_DIR / "decision_edge_observability_extraction_target_v0.json"
REFERENCE_PARK_RECORD_PATH = OUT_DIR / "bounded_probe_reference_park_record_v0.json"
DEFERRED_BRANCHES_PATH = OUT_DIR / "post_bounded_probe_reference_deferred_branches_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "post_bounded_probe_reference_decision_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "post_bounded_probe_reference_decision_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "post_bounded_probe_reference_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "post_bounded_probe_reference_decision_profile_v0.json"
REPORT_PATH = OUT_DIR / "post_bounded_probe_reference_decision_report.json"
TRACE_PATH = OUT_DIR / "post_bounded_probe_reference_decision_transition_trace.json"

EXPECTED_SOURCE_STATUS = "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY"
EXPECTED_SOURCE_STOP = "STOP_TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY"
EXPECTED_SOURCE_NEXT = "DECIDE_NEXT_AFTER_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REFERENCE_CLOSURE_V0"

SELECTED_BRANCH = "EXTRACT_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_FROM_BOUNDED_C6_ADOPTION_PROBE_REFERENCE"
SELECTED_NEXT_UNIT = "EXTRACT_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_FROM_BOUNDED_C6_ADOPTION_PROBE_REFERENCE_V0"

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

    receipt = read_json(SOURCE_REF_CLOSE_RECEIPT_PATH)
    summary = receipt.get("machine_readable_bounded_c6_adoption_probe_reference_closure_summary", {})

    reviewed_reference = read_json(PROBE_REVIEWED_REFERENCE_PATH)
    freeze_manifest = read_json(PROBE_FREEZE_MANIFEST_PATH)
    reference_index = read_json(PROBE_REFERENCE_INDEX_PATH)
    packet_law_survival_reference = read_json(PROBE_PACKET_LAW_SURVIVAL_REFERENCE_PATH)
    observability_reference = read_json(PROBE_OBSERVABILITY_REFERENCE_PATH)
    unit_feedback_reference = read_json(PROBE_UNIT_FEEDBACK_REFERENCE_PATH)
    negative_control_reference = read_json(PROBE_NEGATIVE_CONTROL_REFERENCE_PATH)
    post_closure_decision_ready = read_json(PROBE_POST_CLOSURE_DECISION_READY_PATH)
    authority = read_json(PROBE_REFERENCE_AUTHORITY_PATH)
    classification = read_json(PROBE_REFERENCE_CLASSIFICATION_PATH)
    rollup = read_json(PROBE_REFERENCE_ROLLUP_PATH)
    profile = read_json(PROBE_REFERENCE_PROFILE_PATH)
    report = read_json(PROBE_REFERENCE_REPORT_PATH)
    trace = read_json(PROBE_REFERENCE_TRACE_PATH)

    probe_review_receipt = read_json(SOURCE_PROBE_REVIEW_RECEIPT_PATH)
    probe_receipt = read_json(SOURCE_PROBE_RECEIPT_PATH)
    probe_design_receipt = read_json(SOURCE_PROBE_DESIGN_RECEIPT_PATH)
    c6_reference_receipt = read_json(SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH)

    edge_observations = read_jsonl(PROBE_EDGE_OBSERVATIONS_PATH)
    unit_feedback = read_jsonl(PROBE_UNIT_FEEDBACK_PATH)
    packet_trace = read_jsonl(PROBE_PACKET_TRACE_PATH)
    negative_controls = read_jsonl(PROBE_NEGATIVE_CONTROL_RESULTS_PATH)

    if receipt.get("receipt_id") != SOURCE_REF_CLOSE_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_reference_closure_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_hidden_next")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "bounded_c6_protocol_adoption_probe_closed_as_reviewed_reference",
        "reviewed_reference_frozen",
        "post_bounded_probe_reference_decision_ready",
        "synthetic_protocol_only",
        "negative_controls_fail_closed",
        "packet_law_distinctions_confirmed",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"source_required_true_missing:{key}")

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
        "bounded_probe_reference_mutated",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if summary.get(key) is not False:
            failures.append(f"source_forbidden_true:{key}")

    for key, expected in {
        "packet_trace_count": 9,
        "edge_observation_count": 7,
        "unit_feedback_count": 4,
        "negative_control_count": 15,
    }.items():
        if summary.get(key) != expected:
            failures.append(f"source_count_wrong:{key}:{summary.get(key)}")

    if reviewed_reference.get("reference_status") != "BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEWED_REFERENCE_FROZEN":
        failures.append("reviewed_reference_not_frozen")
    if freeze_manifest.get("freeze_status") != "FROZEN":
        failures.append("freeze_manifest_not_frozen")
    if reference_index.get("index_status") != "REFERENCE_INDEX_EMITTED":
        failures.append("reference_index_wrong")
    if packet_law_survival_reference.get("survival_status") != "REVIEWED_REFERENCE":
        failures.append("packet_law_survival_reference_wrong")
    if packet_law_survival_reference.get("packet_law_distinctions_confirmed") is not True:
        failures.append("packet_law_survival_not_confirmed")
    if observability_reference.get("observability_status") != "REVIEWED_REFERENCE":
        failures.append("observability_reference_wrong")
    if observability_reference.get("edge_observation_count") != 7:
        failures.append("observability_edge_count_wrong")
    if unit_feedback_reference.get("feedback_status") != "REVIEWED_REFERENCE":
        failures.append("unit_feedback_reference_wrong")
    if unit_feedback_reference.get("unit_feedback_count") != 4:
        failures.append("unit_feedback_count_wrong")
    if negative_control_reference.get("negative_control_status") != "REVIEWED_REFERENCE":
        failures.append("negative_control_reference_wrong")
    if negative_control_reference.get("negative_controls_all_fail_closed") is not True:
        failures.append("negative_controls_not_fail_closed")
    if post_closure_decision_ready.get("decision_ready") is not True:
        failures.append("post_closure_decision_not_ready")
    if post_closure_decision_ready.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append("post_closure_next_wrong")

    if authority.get("may_decide_next_after_bounded_probe_reference_closure") is not True:
        failures.append("authority_no_decide")
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
        "may_mutate_bounded_probe_reference",
    ]:
        if authority.get(forbidden) is not False:
            failures.append(f"authority_forbidden_true:{forbidden}")

    if classification.get("next_command_goal") is not None:
        failures.append("classification_hidden_next")
    if rollup.get("post_reference_decision_ready_count") != 1:
        failures.append("rollup_decision_ready_wrong")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if report.get("recommended_next_handling") != EXPECTED_SOURCE_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_hidden_next")

    for ancestor, name in [
        (probe_review_receipt, "probe_review"),
        (probe_receipt, "probe_build"),
        (probe_design_receipt, "probe_design"),
        (c6_reference_receipt, "c6_reference_closure"),
    ]:
        if ancestor.get("gate") != "PASS":
            failures.append(f"ancestor_not_pass:{name}")

    if len(edge_observations) != 7:
        failures.append("edge_observation_rows_wrong")
    if len(unit_feedback) != 4:
        failures.append("unit_feedback_rows_wrong")
    if len(packet_trace) != 9:
        failures.append("packet_trace_rows_wrong")
    if len(negative_controls) != 15:
        failures.append("negative_control_rows_wrong")
    if any(row.get("runtime_effect") is not False for row in edge_observations):
        failures.append("edge_observation_runtime_effect")
    if any(row.get("feedback_quality_class") != "USEFUL_DIAGNOSTIC_FEEDBACK" for row in unit_feedback):
        failures.append("unit_feedback_quality_wrong")
    if any(row.get("passed") is not True or row.get("observed") != "FAIL_CLOSED" for row in negative_controls):
        failures.append("negative_controls_wrong")

    return failures, {
        "summary": summary,
        "reviewed_reference": reviewed_reference,
        "observability_reference": observability_reference,
        "unit_feedback_reference": unit_feedback_reference,
        "packet_law_survival_reference": packet_law_survival_reference,
        "post_closure_decision_ready": post_closure_decision_ready,
        "edge_observations": edge_observations,
        "unit_feedback": unit_feedback,
        "packet_trace": packet_trace,
        "negative_controls": negative_controls,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    decision_pass = not failures
    status = "TYPED_POST_BOUNDED_C6_ADOPTION_PROBE_REFERENCE_DECISION_SELECTED_OBSERVABILITY_EXTRACTION_READY" if decision_pass else "TYPED_POST_BOUNDED_C6_ADOPTION_PROBE_REFERENCE_DECISION_GATE_FAIL"
    recommended_next = SELECTED_NEXT_UNIT if decision_pass else "REPAIR_POST_BOUNDED_C6_ADOPTION_PROBE_REFERENCE_DECISION_V0"

    summary = basis.get("summary", {})
    reviewed_reference = basis.get("reviewed_reference", {})
    observability_reference = basis.get("observability_reference", {})
    unit_feedback_reference = basis.get("unit_feedback_reference", {})
    packet_law_survival_reference = basis.get("packet_law_survival_reference", {})
    post_closure_decision_ready = basis.get("post_closure_decision_ready", {})
    edge_observations = basis.get("edge_observations", [])
    unit_feedback = basis.get("unit_feedback", [])
    packet_trace = basis.get("packet_trace", [])
    negative_controls = basis.get("negative_controls", [])

    reason_codes = [
        "POST_BOUNDED_C6_ADOPTION_PROBE_REFERENCE_DECISION_COMPLETE",
        "BOUNDED_ADOPTION_PROBE_REFERENCE_CLOSURE_RECEIPT_CONSUMED",
        "BOUNDED_ADOPTION_PROBE_REVIEWED_REFERENCE_CONFIRMED",
        "PACKET_LAW_SURVIVAL_REFERENCE_CONFIRMED",
        "OBSERVABILITY_REFERENCE_CONFIRMED",
        "UNIT_FEEDBACK_REFERENCE_PARKED_FOR_NEXT_HARDENING",
        "DECISION_EDGE_OBSERVABILITY_EXTRACTION_SELECTED",
        "C7_DEFERRED",
        "RUNTIME_ADOPTION_DEFERRED",
        "UNIT_FEEDBACK_HARDENING_DEFERRED_UNTIL_AFTER_OBSERVABILITY_EXTRACTION",
        "NO_RUNTIME_EFFECT",
        "NO_RUNTIME_PATCH",
        "NO_C7_AUTHORIZATION",
        "NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if decision_pass else failures

    edge_names = [row.get("edge_name") for row in edge_observations]
    feedback_statuses = sorted({row.get("status") for row in unit_feedback})

    decision_basis = {
        "schema_version": "post_bounded_probe_reference_decision_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if decision_pass else "BASIS_REPAIR_REQUIRED",
        "source_reference_closure_receipt_id": SOURCE_REF_CLOSE_RECEIPT_ID,
        "source_reference_status": reviewed_reference.get("reference_status"),
        "packet_law_survival_status": packet_law_survival_reference.get("survival_status"),
        "observability_status": observability_reference.get("observability_status"),
        "edge_observation_count": len(edge_observations),
        "unit_feedback_count": len(unit_feedback),
        "packet_trace_count": len(packet_trace),
        "negative_control_count": len(negative_controls),
    }

    decision_options = {
        "schema_version": "post_bounded_probe_reference_decision_options_v0",
        "decision_status": "NEXT_BRANCH_SELECTED" if decision_pass else "NO_BRANCH_SELECTED",
        "options_from_reference": post_closure_decision_ready.get("decision_options", []),
        "options": [
            {
                "branch": SELECTED_BRANCH,
                "selected": decision_pass,
                "next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
                "why": "The bounded probe generated 7 decision-edge observations. Extracting their requirements is the next smallest observation-hardening move.",
            },
            {
                "branch": "EXTRACT_UNIT_FEEDBACK_HARDENING_REQUIREMENTS_FROM_BOUNDED_C6_ADOPTION_PROBE_REFERENCE",
                "selected": False,
                "next_unit": None,
                "why": "Important next, but it follows decision-edge observability extraction so feedback has clearer edge context.",
            },
            {
                "branch": "PARK_BOUNDED_C6_ADOPTION_PROBE_REFERENCE_AS_SUFFICIENT",
                "selected": False,
                "next_unit": None,
                "why": "Reference remains parked, but the edge-observation surface is immediately useful for observation hardening.",
            },
            {
                "branch": "DESIGN_ANOTHER_BOUNDED_ADOPTION_PROBE",
                "selected": False,
                "next_unit": None,
                "why": "Not yet. Repeating probes before extracting the observed edge surface would add evidence without improving observability.",
            },
            {
                "branch": "OPEN_C7",
                "selected": False,
                "next_unit": None,
                "why": "Forbidden here. C7 stays deferred until after observation and feedback hardening.",
            },
            {
                "branch": "PATCH_RUNTIME_WITH_C6_PROTOCOL",
                "selected": False,
                "next_unit": None,
                "why": "Forbidden here. The reference does not authorize runtime-wide enforcement.",
            },
        ],
    }

    selected_branch = {
        "schema_version": "post_bounded_probe_reference_selected_branch_v0",
        "selected_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "selected_scope": "extract decision-edge observability requirements from the reviewed bounded C6 adoption-probe reference",
        "selected_sources": {
            "reference_closure_receipt": SOURCE_REF_CLOSE_RECEIPT_ID,
            "reviewed_reference": rel(PROBE_REVIEWED_REFERENCE_PATH),
            "observability_reference": rel(PROBE_OBSERVABILITY_REFERENCE_PATH),
            "edge_observations": rel(PROBE_EDGE_OBSERVATIONS_PATH),
        },
        "selected_does_not": [
            "patch runtime",
            "authorize C7",
            "claim full transfer",
            "claim global autonomy",
            "grant general Cell 1 authority",
            "claim runtime-wide enforcement",
            "mutate bounded probe reference",
        ],
    }

    observability_extraction_target = {
        "schema_version": "decision_edge_observability_extraction_target_v0",
        "target_status": "OBSERVABILITY_EXTRACTION_TARGET_SELECTED" if decision_pass else "NOT_SELECTED",
        "target_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "source_reference_receipt": SOURCE_REF_CLOSE_RECEIPT_ID,
        "goal": "Extract a reusable decision-edge observability requirement set from the bounded C6 adoption-probe reference.",
        "must_consume": [
            rel(PROBE_REVIEWED_REFERENCE_PATH),
            rel(PROBE_OBSERVABILITY_REFERENCE_PATH),
            rel(PROBE_EDGE_OBSERVATIONS_PATH),
            rel(PROBE_PACKET_TRACE_PATH),
            rel(PROBE_PACKET_LAW_SURVIVAL_REFERENCE_PATH),
        ],
        "edge_names_to_extract": edge_names,
        "minimum_requirement_fields": [
            "active_object",
            "attempted_move",
            "boundary_checked",
            "boundary_result",
            "blocked_moves",
            "lawful_next_moves",
            "source_packet_ref",
        ],
        "must_preserve_distinctions": [
            "decision-edge observation is not protocol proof",
            "observation sidecar is not authority",
            "handoff is not hidden next command",
            "verification is not closure",
            "blocked feedback is not repair",
            "edge visibility is not runtime adoption",
        ],
        "must_not_do": [
            "patch runtime",
            "open C7",
            "execute a new domain shift",
            "mutate source reference",
            "claim transfer",
            "claim autonomy",
            "claim general Cell 1 authority",
            "claim runtime-wide enforcement",
        ],
    }

    reference_park_record = {
        "schema_version": "bounded_probe_reference_park_record_v0",
        "park_status": "PARKED_AS_REVIEWED_REFERENCE_AVAILABLE_FOR_CONSUMPTION",
        "reference_receipt": SOURCE_REF_CLOSE_RECEIPT_ID,
        "reference_path": rel(PROBE_REVIEWED_REFERENCE_PATH),
        "meaning": "The bounded C6 adoption probe remains frozen and available as reviewed evidence. The current decision only selects edge-observability extraction.",
    }

    deferred_branches = {
        "schema_version": "post_bounded_probe_reference_deferred_branches_v0",
        "deferred": [
            "OPEN_C7",
            "PATCH_RUNTIME_WITH_C6_PROTOCOL",
            "CLAIM_RUNTIME_WIDE_ENFORCEMENT",
            "CLAIM_FULL_TRANSFER",
            "CLAIM_GLOBAL_AUTONOMY",
            "GRANT_GENERAL_CELL1_AUTHORITY",
            "RUN_NEW_DOMAIN_SHIFT",
            "EXTRACT_UNIT_FEEDBACK_HARDENING_REQUIREMENTS_FROM_BOUNDED_C6_ADOPTION_PROBE_REFERENCE",
            "DESIGN_ANOTHER_BOUNDED_ADOPTION_PROBE",
        ],
        "why": "Decision-edge observability extraction is the smallest useful next hardening move after this reference closure.",
    }

    authority_boundary = {
        "schema_version": "post_bounded_probe_reference_decision_authority_boundary_v0",
        "status": status,
        "may_extract_decision_edge_observability_requirements_next": decision_pass,
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
        "schema_version": "post_bounded_probe_reference_decision_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "post_bounded_probe_reference_decision_complete": decision_pass,
        "selected_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": recommended_next,
        "decision_edge_observability_extraction_ready": decision_pass,
        "bounded_probe_reference_parked_available": decision_pass,
        "unit_feedback_hardening_deferred": True,
        "c7_deferred": True,
        "runtime_adoption_deferred": True,
        "source_reference_status": reviewed_reference.get("reference_status"),
        "packet_trace_count": len(packet_trace),
        "edge_observation_count": len(edge_observations),
        "unit_feedback_count": len(unit_feedback),
        "negative_control_count": len(negative_controls),
        "feedback_statuses_parked_for_next_hardening": feedback_statuses,
        "runtime_effect": False,
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
        "bad_counters_zero": True,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "post_bounded_probe_reference_decision_rollup_v0",
        "decision_count": 1 if decision_pass else 0,
        "observability_extraction_selected_count": 1 if decision_pass else 0,
        "bounded_probe_reference_parked_count": 1 if decision_pass else 0,
        "unit_feedback_hardening_selected_count": 0,
        "c7_authorized_count": 0,
        "runtime_adoption_count": 0,
        "new_domain_shift_executed_count": 0,
        "packet_trace_count": len(packet_trace),
        "edge_observation_count": len(edge_observations),
        "unit_feedback_count": len(unit_feedback),
        "negative_control_count": len(negative_controls),
        "runtime_effect_count": 0,
        "runtime_patch_count": 0,
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
        "schema_version": "post_bounded_probe_reference_decision_profile_v0",
        "profile_id": "post_bounded_probe_ref_decision_" + sig8(rollup),
        "status": status,
        "decision": "select decision-edge observability extraction from bounded C6 adoption-probe reference",
        "why_this_edge": "The bounded probe produced a clean edge-observation surface. Extracting it is the next observation-hardening move before unit-feedback hardening or C7.",
        "edge_observations_available": edge_names,
        "must_not_infer": [
            "runtime patch",
            "C7 authorization",
            "global autonomy",
            "full transfer",
            "general Cell 1 authority",
            "runtime-wide enforcement",
        ],
        "bad_counters_zero": True,
        "next_command_goal": None,
    }

    report = {
        "schema_version": "post_bounded_probe_reference_decision_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The post-bounded-probe reference decision consumed the frozen bounded C6 adoption-probe reference and selected decision-edge observability requirement extraction as the next lawful object. It leaves unit-feedback hardening parked for the following hardening move and does not patch runtime, authorize C7, execute a new domain shift, or claim transfer/autonomy/general Cell 1 authority.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "post_bounded_probe_reference_decision_transition_trace_v0",
        "trace": [
            {
                "step": "consume_bounded_probe_reference_closure",
                "question": "is the bounded C6 adoption-probe reference frozen and decision-ready",
                "answer": "yes" if decision_pass else "no",
                "taken": "evaluate post-reference branches",
            },
            {
                "step": "select_observability_extraction",
                "question": "what is the smallest useful hardening edge",
                "answer": SELECTED_NEXT_UNIT if decision_pass else recommended_next,
                "taken": "select decision-edge observability extraction",
            },
            {
                "step": "defer_broader_moves",
                "question": "does this authorize C7, runtime adoption, or unit-feedback hardening now",
                "answer": "no",
                "taken": "stop with extraction-ready decision",
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
        (OBSERVABILITY_EXTRACTION_TARGET_PATH, observability_extraction_target),
        (REFERENCE_PARK_RECORD_PATH, reference_park_record),
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
        "POST_BOUNDED_PROBE_DECISION_0_REFERENCE_CLOSURE_RECEIPT_CONSUMED": SOURCE_REF_CLOSE_RECEIPT_PATH.exists(),
        "POST_BOUNDED_PROBE_DECISION_1_REVIEWED_REFERENCE_CONFIRMED": reviewed_reference.get("reference_status") == "BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEWED_REFERENCE_FROZEN",
        "POST_BOUNDED_PROBE_DECISION_2_OBSERVABILITY_REFERENCE_CONFIRMED": observability_reference.get("observability_status") == "REVIEWED_REFERENCE",
        "POST_BOUNDED_PROBE_DECISION_3_EDGE_OBSERVATIONS_CONFIRMED": len(edge_observations) == 7,
        "POST_BOUNDED_PROBE_DECISION_4_DECISION_BASIS_EMITTED": DECISION_BASIS_PATH.exists(),
        "POST_BOUNDED_PROBE_DECISION_5_OPTIONS_EMITTED": DECISION_OPTIONS_PATH.exists(),
        "POST_BOUNDED_PROBE_DECISION_6_OBSERVABILITY_EXTRACTION_SELECTED": selected_branch["selected_next_unit"] == SELECTED_NEXT_UNIT,
        "POST_BOUNDED_PROBE_DECISION_7_OBSERVABILITY_EXTRACTION_TARGET_EMITTED": OBSERVABILITY_EXTRACTION_TARGET_PATH.exists(),
        "POST_BOUNDED_PROBE_DECISION_8_REFERENCE_PARK_RECORD_EMITTED": REFERENCE_PARK_RECORD_PATH.exists(),
        "POST_BOUNDED_PROBE_DECISION_9_DEFERRED_BRANCHES_EMITTED": DEFERRED_BRANCHES_PATH.exists(),
        "POST_BOUNDED_PROBE_DECISION_10_UNIT_FEEDBACK_HARDENING_DEFERRED": classification["unit_feedback_hardening_deferred"] is True,
        "POST_BOUNDED_PROBE_DECISION_11_C7_DEFERRED": classification["c7_deferred"] is True,
        "POST_BOUNDED_PROBE_DECISION_12_NO_RUNTIME_EFFECT_OR_PATCH": classification["runtime_effect"] is False and classification["runtime_patched"] is False,
        "POST_BOUNDED_PROBE_DECISION_13_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "POST_BOUNDED_PROBE_DECISION_14_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["bounded_probe_reference_mutated"] is False,
        "POST_BOUNDED_PROBE_DECISION_15_BAD_COUNTERS_ZERO": classification["bad_counters_zero"] is True,
        "POST_BOUNDED_PROBE_DECISION_16_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "POST_BOUNDED_PROBE_DECISION_17_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "POST_BOUNDED_PROBE_DECISION_18_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_POST_BOUNDED_C6_ADOPTION_PROBE_REFERENCE_DECISION_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_POST_BOUNDED_C6_ADOPTION_PROBE_REFERENCE_DECISION_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_POST_BOUNDED_C6_ADOPTION_PROBE_REFERENCE_DECISION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_reference": SOURCE_REF_CLOSE_RECEIPT_ID,
        "selected_next": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "post_bounded_c6_adoption_probe_reference_decision_receipt_v0",
        "receipt_type": "TYPED_POST_BOUNDED_C6_ADOPTION_PROBE_REFERENCE_DECISION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_bounded_probe_reference_closure_receipt_id": SOURCE_REF_CLOSE_RECEIPT_ID,
        "machine_readable_post_bounded_probe_reference_decision_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "post_bounded_probe_reference_decision_complete": gate == "PASS",
            "selected_branch": SELECTED_BRANCH if gate == "PASS" else None,
            "selected_next_unit": final_next,
            "decision_edge_observability_extraction_ready": gate == "PASS",
            "bounded_probe_reference_parked_available": gate == "PASS",
            "unit_feedback_hardening_deferred": True,
            "c7_deferred": True,
            "runtime_adoption_deferred": True,
            "source_reference_status": reviewed_reference.get("reference_status"),
            "packet_trace_count": len(packet_trace),
            "edge_observation_count": len(edge_observations),
            "unit_feedback_count": len(unit_feedback),
            "negative_control_count": len(negative_controls),
            "runtime_effect": False,
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
            "bad_counters_zero": True,
            "recommended_next": final_next,
        },
        "aggregate_metrics": report | {"status": final_status, "recommended_next_handling": final_next},
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "decision_basis": rel(DECISION_BASIS_PATH),
            "decision_options": rel(DECISION_OPTIONS_PATH),
            "selected_branch": rel(SELECTED_BRANCH_PATH),
            "observability_extraction_target": rel(OBSERVABILITY_EXTRACTION_TARGET_PATH),
            "reference_park_record": rel(REFERENCE_PARK_RECORD_PATH),
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
    print(f"post_bounded_probe_reference_decision_receipt_id={receipt_id}")
    print(f"post_bounded_probe_reference_decision_receipt_path={rel(receipt_path)}")
    print(f"decision_edge_observability_extraction_target_path={rel(OBSERVABILITY_EXTRACTION_TARGET_PATH)}")
    print(f"post_bounded_probe_reference_decision_rollup_path={rel(ROLLUP_PATH)}")
    print(f"post_bounded_probe_reference_decision_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
