#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_AFTER_C5_TO_C6_INTER_CELL_PROTOCOL_EXAMPLES_REFERENCE_CLOSURE_V0"
TARGET_UNIT_ID = "c6.post_example_reference_decision.v0"
LAYER = "BRIDGE / C5_TO_C6 / POST_EXAMPLE_REFERENCE_DECISION"
MODE = "DECIDE_ONLY / SELECT_C6_PROTOCOL_TARGET_DESIGN / NO_PROTOCOL_BUILD"
BUILD_MODE = "POST_C6_EXAMPLE_REFERENCE_DECISION_ONLY"

SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID = "fe882749"
SOURCE_C6_EXAMPLE_REVIEW_RECEIPT_ID = "727a881c"
SOURCE_C6_EXAMPLE_EXTRACTION_RECEIPT_ID = "c486e477"
SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_ID = "934363ba"
SOURCE_POST_C5_DECISION_RECEIPT_ID = "23cb11ed"

SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0_receipts/fe882749.json"

C6_EXAMPLE_REVIEWED_REFERENCE_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0/c6_example_extraction_reviewed_reference_v0.json"
C6_EXAMPLE_FREEZE_MANIFEST_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0/c6_example_extraction_reviewed_reference_freeze_manifest_v0.json"
C6_EXAMPLE_REFERENCE_INDEX_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0/c6_example_extraction_reviewed_reference_index_v0.json"
C6_EXAMPLE_SURFACE_REFERENCE_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0/c6_inter_cell_example_surface_reference_v0.json"
C6_PROTOCOL_PRESSURE_REFERENCE_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0/c6_protocol_pressure_reference_non_design_v0.json"
C6_EXAMPLE_NEXT_DECISION_READY_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0/c6_example_reference_post_closure_decision_ready_v0.json"
C6_EXAMPLE_REFERENCE_AUTHORITY_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0/c6_example_reference_closure_authority_boundary_v0.json"
C6_EXAMPLE_REFERENCE_CLASSIFICATION_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0/c6_example_reference_closure_classification_v0.json"
C6_EXAMPLE_REFERENCE_ROLLUP_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0/c6_example_reference_closure_rollup_v0.json"
C6_EXAMPLE_REFERENCE_PROFILE_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0/c6_example_reference_closure_profile_v0.json"
C6_EXAMPLE_REFERENCE_REPORT_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0/c6_example_reference_closure_report.json"
C6_EXAMPLE_REFERENCE_TRACE_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0/c6_example_reference_closure_transition_trace.json"

C6_EXAMPLES_JSONL_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_inter_cell_protocol_examples_from_c5_v0.jsonl"
C6_EXAMPLE_CATALOG_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_inter_cell_protocol_example_catalog_v0.json"
C6_EXAMPLE_SCHEMA_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_inter_cell_protocol_example_schema_v0.json"
C6_PROTOCOL_PRESSURE_READOUT_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_protocol_pressure_readout_from_c5_examples_v0.json"

SOURCE_C6_EXAMPLE_REVIEW_RECEIPT_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_review_v0_receipts/727a881c.json"
SOURCE_C6_EXAMPLE_EXTRACTION_RECEIPT_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0_receipts/c486e477.json"
SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c5_full_domain_shift_transition_reference_closure_v0_receipts/934363ba.json"
SOURCE_POST_C5_DECISION_RECEIPT_PATH = ROOT / "data/c5_post_domain_shift_reference_decision_v0_receipts/23cb11ed.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH,
    C6_EXAMPLE_REVIEWED_REFERENCE_PATH,
    C6_EXAMPLE_FREEZE_MANIFEST_PATH,
    C6_EXAMPLE_REFERENCE_INDEX_PATH,
    C6_EXAMPLE_SURFACE_REFERENCE_PATH,
    C6_PROTOCOL_PRESSURE_REFERENCE_PATH,
    C6_EXAMPLE_NEXT_DECISION_READY_PATH,
    C6_EXAMPLE_REFERENCE_AUTHORITY_PATH,
    C6_EXAMPLE_REFERENCE_CLASSIFICATION_PATH,
    C6_EXAMPLE_REFERENCE_ROLLUP_PATH,
    C6_EXAMPLE_REFERENCE_PROFILE_PATH,
    C6_EXAMPLE_REFERENCE_REPORT_PATH,
    C6_EXAMPLE_REFERENCE_TRACE_PATH,
    C6_EXAMPLES_JSONL_PATH,
    C6_EXAMPLE_CATALOG_PATH,
    C6_EXAMPLE_SCHEMA_PATH,
    C6_PROTOCOL_PRESSURE_READOUT_PATH,
    SOURCE_C6_EXAMPLE_REVIEW_RECEIPT_PATH,
    SOURCE_C6_EXAMPLE_EXTRACTION_RECEIPT_PATH,
    SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_PATH,
    SOURCE_POST_C5_DECISION_RECEIPT_PATH,
]

OUT_DIR = ROOT / "data/c6_post_example_reference_decision_v0"
RECEIPT_DIR = ROOT / "data/c6_post_example_reference_decision_v0_receipts"

DECISION_BASIS_PATH = OUT_DIR / "c6_post_example_reference_decision_basis_v0.json"
DECISION_OPTIONS_PATH = OUT_DIR / "c6_post_example_reference_decision_options_v0.json"
SELECTED_BRANCH_PATH = OUT_DIR / "c6_post_example_reference_selected_branch_v0.json"
C6_TARGET_DESIGN_AUTH_PATH = OUT_DIR / "c6_protocol_target_design_authorization_from_reviewed_examples_v0.json"
C6_OBJECTIVE_BINDING_PATH = OUT_DIR / "c6_inter_cell_protocol_objective_binding_v0.json"
C6_DESIGN_TARGET_SEED_PATH = OUT_DIR / "c6_inter_cell_protocol_target_design_seed_v0.json"
DEFERRED_BRANCHES_PATH = OUT_DIR / "c6_post_example_reference_deferred_branches_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "c6_post_example_reference_decision_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "c6_post_example_reference_decision_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "c6_post_example_reference_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c6_post_example_reference_decision_profile_v0.json"
REPORT_PATH = OUT_DIR / "c6_post_example_reference_decision_report.json"
TRACE_PATH = OUT_DIR / "c6_post_example_reference_decision_transition_trace.json"

EXPECTED_SOURCE_STATUS = "TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY"
EXPECTED_SOURCE_STOP = "STOP_TYPED_C6_EXAMPLE_EXTRACTION_FROM_C5_REFERENCE_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY"
EXPECTED_SOURCE_NEXT = "DECIDE_NEXT_AFTER_C5_TO_C6_INTER_CELL_PROTOCOL_EXAMPLES_REFERENCE_CLOSURE_V0"

SELECTED_BRANCH = "DESIGN_C6_INTER_CELL_PROTOCOL_FROM_C5_EXAMPLES_TARGET"
SELECTED_NEXT_UNIT = "DESIGN_C6_INTER_CELL_PROTOCOL_FROM_C5_EXAMPLES_TARGET_V0"
FUTURE_BUILD_UNIT = "BUILD_C6_INTER_CELL_PROTOCOL_FROM_C5_EXAMPLES_V0"

EXPECTED_EXAMPLE_TYPES = [
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

    closure_receipt = read_json(SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH)
    closure_summary = closure_receipt.get("machine_readable_c6_example_reference_closure_summary", {})

    reviewed_reference = read_json(C6_EXAMPLE_REVIEWED_REFERENCE_PATH)
    freeze_manifest = read_json(C6_EXAMPLE_FREEZE_MANIFEST_PATH)
    reference_index = read_json(C6_EXAMPLE_REFERENCE_INDEX_PATH)
    surface_reference = read_json(C6_EXAMPLE_SURFACE_REFERENCE_PATH)
    pressure_reference = read_json(C6_PROTOCOL_PRESSURE_REFERENCE_PATH)
    decision_ready = read_json(C6_EXAMPLE_NEXT_DECISION_READY_PATH)
    authority = read_json(C6_EXAMPLE_REFERENCE_AUTHORITY_PATH)
    classification = read_json(C6_EXAMPLE_REFERENCE_CLASSIFICATION_PATH)
    rollup = read_json(C6_EXAMPLE_REFERENCE_ROLLUP_PATH)
    profile = read_json(C6_EXAMPLE_REFERENCE_PROFILE_PATH)
    report = read_json(C6_EXAMPLE_REFERENCE_REPORT_PATH)
    trace = read_json(C6_EXAMPLE_REFERENCE_TRACE_PATH)

    examples = read_jsonl(C6_EXAMPLES_JSONL_PATH)
    catalog = read_json(C6_EXAMPLE_CATALOG_PATH)
    example_schema = read_json(C6_EXAMPLE_SCHEMA_PATH)
    pressure_readout = read_json(C6_PROTOCOL_PRESSURE_READOUT_PATH)

    review_receipt = read_json(SOURCE_C6_EXAMPLE_REVIEW_RECEIPT_PATH)
    extraction_receipt = read_json(SOURCE_C6_EXAMPLE_EXTRACTION_RECEIPT_PATH)
    c5_reference_closure = read_json(SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_PATH)
    post_c5_decision = read_json(SOURCE_POST_C5_DECISION_RECEIPT_PATH)

    if closure_receipt.get("receipt_id") != SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID or closure_receipt.get("gate") != "PASS":
        failures.append("source_c6_example_reference_closure_receipt_not_pass")
    if closure_receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_stop_wrong")
    if closure_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_hidden_next")
    if closure_summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_status_wrong:{closure_summary.get('status')}")
    if closure_summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_next_wrong:{closure_summary.get('recommended_next')}")

    for key in [
        "c6_example_extraction_closed_as_reviewed_reference",
        "reviewed_reference_frozen",
        "post_example_reference_decision_ready",
        "protocol_pressure_readout_is_not_protocol_design",
        "bad_counters_zero",
    ]:
        if closure_summary.get(key) is not True:
            failures.append(f"closure_summary_required_true_missing:{key}")

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
        if closure_summary.get(key) != expected:
            failures.append(f"closure_count_wrong:{key}:{closure_summary.get(key)}")

    if sorted(closure_summary.get("example_types_reviewed", [])) != EXPECTED_EXAMPLE_TYPES:
        failures.append("closure_example_types_wrong")

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
        if closure_summary.get(key) is not False:
            failures.append(f"closure_forbidden_true:{key}")

    if reviewed_reference.get("reference_status") != "C6_EXAMPLE_EXTRACTION_REVIEWED_REFERENCE_FROZEN":
        failures.append("reviewed_reference_not_frozen")
    if freeze_manifest.get("freeze_status") != "FROZEN":
        failures.append("freeze_manifest_not_frozen")
    if reference_index.get("index_status") != "REFERENCE_INDEX_EMITTED":
        failures.append("reference_index_wrong")
    if surface_reference.get("examples_count") != 12:
        failures.append("surface_reference_count_wrong")
    if pressure_reference.get("not_a_c6_protocol_design") is not True:
        failures.append("pressure_reference_claims_design")
    if decision_ready.get("decision_ready") is not True or decision_ready.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append("decision_ready_wrong")
    if authority.get("may_decide_next_after_c6_example_reference_closure") is not True:
        failures.append("authority_no_decide")
    for forbidden in [
        "may_open_c6_now_in_closure",
        "may_design_c6_protocol_now_in_closure",
        "may_emit_c6_protocol_now_in_closure",
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
    if classification.get("post_example_reference_decision_ready") is not True:
        failures.append("classification_decision_not_ready")
    if classification.get("next_command_goal") is not None:
        failures.append("classification_hidden_next")
    if rollup.get("post_example_reference_decision_ready_count") != 1:
        failures.append("rollup_decision_ready_wrong")
    if profile.get("post_example_reference_decision_ready") is not True or profile.get("next_command_goal") is not None:
        failures.append("profile_wrong")
    if report.get("recommended_next_handling") != EXPECTED_SOURCE_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_hidden_next")

    if len(examples) != 12:
        failures.append(f"examples_jsonl_count_wrong:{len(examples)}")
    if catalog.get("example_count") != 12:
        failures.append("catalog_count_wrong")
    if sorted(catalog.get("example_types", [])) != EXPECTED_EXAMPLE_TYPES:
        failures.append("catalog_types_wrong")
    if sorted(example_schema.get("closed_example_types", [])) != EXPECTED_EXAMPLE_TYPES:
        failures.append("example_schema_types_wrong")
    if pressure_readout.get("not_a_c6_protocol_design") is not True:
        failures.append("pressure_readout_claims_design")

    if review_receipt.get("receipt_id") != SOURCE_C6_EXAMPLE_REVIEW_RECEIPT_ID or review_receipt.get("gate") != "PASS":
        failures.append("review_receipt_wrong")
    if extraction_receipt.get("receipt_id") != SOURCE_C6_EXAMPLE_EXTRACTION_RECEIPT_ID or extraction_receipt.get("gate") != "PASS":
        failures.append("extraction_receipt_wrong")
    if c5_reference_closure.get("receipt_id") != SOURCE_C5_REFERENCE_CLOSURE_RECEIPT_ID or c5_reference_closure.get("gate") != "PASS":
        failures.append("c5_reference_closure_receipt_wrong")
    if post_c5_decision.get("receipt_id") != SOURCE_POST_C5_DECISION_RECEIPT_ID or post_c5_decision.get("gate") != "PASS":
        failures.append("post_c5_decision_receipt_wrong")

    return failures, {
        "closure_summary": closure_summary,
        "catalog": catalog,
        "pressure_readout": pressure_readout,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    decision_pass = not failures
    status = "TYPED_C6_POST_EXAMPLE_REFERENCE_DECISION_SELECTED_PROTOCOL_TARGET_DESIGN_READY" if decision_pass else "TYPED_C6_POST_EXAMPLE_REFERENCE_DECISION_GATE_FAIL"
    recommended_next = SELECTED_NEXT_UNIT if decision_pass else "REPAIR_C6_POST_EXAMPLE_REFERENCE_DECISION_V0"

    closure_summary = basis.get("closure_summary", {})
    catalog = basis.get("catalog", {})
    pressure_readout = basis.get("pressure_readout", {})

    reason_codes = [
        "POST_C6_EXAMPLE_REFERENCE_DECISION_COMPLETE",
        "C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_CONSUMED",
        "C6_REVIEWED_EXAMPLE_REFERENCE_CONFIRMED",
        "C6_EXAMPLE_SURFACE_CONFIRMED",
        "C6_PROTOCOL_PRESSURE_CONFIRMED_AS_NON_DESIGN",
        "C6_PROTOCOL_TARGET_DESIGN_SELECTED_NEXT",
        "C6_BUILD_NOT_EXECUTED_IN_DECISION",
        "C6_PROTOCOL_NOT_EMITTED_IN_DECISION",
        "C6_RUNTIME_NOT_PATCHED",
        "C7_NOT_AUTHORIZED",
        "NO_NEW_DOMAIN_SHIFT_EXECUTED",
        "NO_TRANSFER_CLAIM",
        "NO_GLOBAL_AUTONOMY_CLAIM",
        "NO_GENERAL_CELL1_AUTHORITY_CLAIM",
        "NO_RUNTIME_WIDE_ENFORCEMENT_CLAIM",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if decision_pass else failures

    decision_basis = {
        "schema_version": "c6_post_example_reference_decision_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if decision_pass else "BASIS_REPAIR_REQUIRED",
        "source_c6_example_reference_closure_receipt_id": SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID,
        "source_c6_example_review_receipt_id": SOURCE_C6_EXAMPLE_REVIEW_RECEIPT_ID,
        "source_c6_example_extraction_receipt_id": SOURCE_C6_EXAMPLE_EXTRACTION_RECEIPT_ID,
        "examples_reviewed": closure_summary.get("examples_reviewed"),
        "example_types_reviewed": closure_summary.get("example_types_reviewed", []),
        "protocol_pressure_is_not_design": True,
        "post_example_reference_decision_ready": True,
    }

    decision_options = {
        "schema_version": "c6_post_example_reference_decision_options_v0",
        "decision_status": "NEXT_BRANCH_SELECTED" if decision_pass else "NO_BRANCH_SELECTED",
        "options": [
            {
                "branch": SELECTED_BRANCH,
                "selected": decision_pass,
                "next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
                "future_build_unit": FUTURE_BUILD_UNIT,
                "why": "The reviewed example reference is frozen; the next lawful edge is target design before protocol build.",
            },
            {
                "branch": "BUILD_C6_INTER_CELL_PROTOCOL_FROM_C5_EXAMPLES_DIRECTLY",
                "selected": False,
                "next_unit": None,
                "why": "Too fast. Build objective is valid, but the target should be designed/frozen first.",
            },
            {
                "branch": "DEFER_C6_AND_RETURN_TO_OBSERVATION_HARDENING",
                "selected": False,
                "next_unit": None,
                "why": "Valid later, but the current bridge has enough reviewed examples to design a target.",
            },
            {
                "branch": "RUN_NEW_DOMAIN_SHIFT",
                "selected": False,
                "next_unit": None,
                "why": "Not needed and not authorized before C6 packet discipline exists.",
            },
            {
                "branch": "OPEN_C7",
                "selected": False,
                "next_unit": None,
                "why": "C7 is explicitly not authorized before C6 communication discipline exists.",
            },
        ],
    }

    selected_branch = {
        "schema_version": "c6_post_example_reference_selected_branch_v0",
        "selected_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "future_build_unit": FUTURE_BUILD_UNIT,
        "selection_scope": "design a C6 inter-cell protocol target from reviewed C5-to-C6 examples",
        "selection_does_not": [
            "build C6 protocol now",
            "emit protocol candidate now",
            "open C7",
            "patch runtime",
            "claim transfer",
            "claim global autonomy",
            "grant general Cell 1 authority",
            "claim runtime-wide enforcement",
        ],
    }

    target_design_auth = {
        "schema_version": "c6_protocol_target_design_authorization_from_reviewed_examples_v0",
        "authorization_status": "C6_PROTOCOL_TARGET_DESIGN_AUTHORIZED_NEXT" if decision_pass else "NOT_AUTHORIZED",
        "authorized_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "future_build_unit_after_design_review": FUTURE_BUILD_UNIT,
        "authorized_scope": [
            "consume reviewed C5-to-C6 example reference closure receipt",
            "consume reviewed example catalog and pressure readout",
            "design target for local inter-cell protocol candidate",
            "preserve packet-law doctrine",
            "preserve accepted-only Cell 1 consumption",
            "preserve verification, handoff, blocked feedback, edge observation, and unit feedback requirements",
        ],
        "not_authorized_in_this_decision": [
            "emit C6 protocol candidate",
            "open C7",
            "patch runtime",
            "execute new domain shift",
            "grant general Cell 1 authority",
            "claim full transfer",
            "claim global autonomy",
            "claim runtime-wide enforcement",
        ],
    }

    objective_binding = {
        "schema_version": "c6_inter_cell_protocol_objective_binding_v0",
        "objective_status": "BOUND_AS_TARGET_DESIGN_INPUT" if decision_pass else "NOT_BOUND",
        "objective_unit_candidate": FUTURE_BUILD_UNIT,
        "clean_doctrine": [
            "Cells do not pass vibes.",
            "Cells pass packets.",
            "Cell 1 does not receive intentions.",
            "Cell 1 receives accepted, scoped, receipt-backed packets.",
        ],
        "core_law": "No cell may consume, transform, or act on another cell output unless that output is wrapped in an explicit protocol packet with source, destination, authority, scope, status, allowed inputs, forbidden inputs, expected return, forbidden interpretations, and receipt basis.",
        "required_packet_family": [
            "PROPOSAL_PACKET_PROPOSED_ONLY",
            "ACCEPTED_PROPOSAL_PACKET",
            "CELL1_BUILDER_INTAKE_PACKET",
            "CELL1_PROBE_OR_BUILD_PACKET",
            "VERIFICATION_RETURN_PACKET",
            "HANDOFF_RETURN_PACKET",
            "BLOCKED_OR_TYPED_STOP_FEEDBACK_PACKET",
            "DECISION_EDGE_OBSERVATION_SIDECAR",
            "UNIT_FEEDBACK_SIDECAR",
        ],
        "must_preserve_distinctions": [
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
        "schema_claim": "LOCAL_PROTOCOL_CANDIDATE_ONLY",
    }

    design_target_seed = {
        "schema_version": "c6_inter_cell_protocol_target_design_seed_v0",
        "target_design_ready": decision_pass,
        "proposed_target_unit": "inter_cell.protocol_from_c5_examples.target.v0",
        "future_build_unit": FUTURE_BUILD_UNIT,
        "source_example_reference_receipt": SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID,
        "examples_reviewed": closure_summary.get("examples_reviewed"),
        "example_types_reviewed": closure_summary.get("example_types_reviewed", []),
        "example_catalog_ref": rel(C6_EXAMPLE_CATALOG_PATH),
        "examples_jsonl_ref": rel(C6_EXAMPLES_JSONL_PATH),
        "pressure_readout_ref": rel(C6_PROTOCOL_PRESSURE_READOUT_PATH),
        "fields_c6_likely_needs": pressure_readout.get("fields_c6_likely_needs", []),
        "target_should_emit": [
            "packet family",
            "packet schemas",
            "state machine",
            "gate table",
            "forbidden transition table",
            "derivation status records",
            "negative controls",
            "rollup/profile/readout",
            "terminal stop with next_command_goal null",
        ],
        "target_must_not_emit": [
            "protocol candidate build artifacts",
            "runtime patch",
            "C7 artifacts",
            "general Cell 1 authority",
            "full-transfer claim",
            "global-autonomy claim",
            "runtime-wide enforcement claim",
        ],
    }

    deferred_branches = {
        "schema_version": "c6_post_example_reference_deferred_branches_v0",
        "deferred": [
            "BUILD_C6_INTER_CELL_PROTOCOL_FROM_C5_EXAMPLES_DIRECTLY",
            "OPEN_C7",
            "RUN_NEW_DOMAIN_SHIFT",
            "PATCH_RUNTIME_WITH_C6",
            "CLAIM_RUNTIME_WIDE_ENFORCEMENT",
            "GRANT_GENERAL_CELL1_AUTHORITY",
        ],
        "why": "The selected edge is target design from a reviewed example reference, not protocol build or runtime adoption.",
    }

    authority_boundary = {
        "schema_version": "c6_post_example_reference_decision_authority_boundary_v0",
        "status": status,
        "may_execute_c6_protocol_target_design_next": decision_pass,
        "may_build_c6_protocol_now_in_decision": False,
        "may_emit_c6_protocol_now_in_decision": False,
        "may_patch_runtime_now_in_decision": False,
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
        "schema_version": "c6_post_example_reference_decision_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "post_example_reference_decision_complete": decision_pass,
        "selected_next_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": recommended_next,
        "future_build_unit": FUTURE_BUILD_UNIT if decision_pass else None,
        "c6_protocol_target_design_authorized_next": decision_pass,
        "c6_protocol_built_in_decision": False,
        "c6_protocol_emitted_in_decision": False,
        "runtime_patched": False,
        "c7_authorized": False,
        "new_domain_shift_executed": False,
        "examples_reviewed": closure_summary.get("examples_reviewed"),
        "example_types_reviewed": closure_summary.get("example_types_reviewed", []),
        "bad_counters_zero": True,
        "full_transfer_claimed": False,
        "global_autonomy_claimed": False,
        "general_cell1_authority_claimed": False,
        "runtime_wide_enforcement_claimed": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "c5_reference_mutated": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "c6_post_example_reference_decision_rollup_v0",
        "decision_count": 1 if decision_pass else 0,
        "selected_c6_protocol_target_design_count": 1 if decision_pass else 0,
        "c6_protocol_target_design_authorized_next_count": 1 if decision_pass else 0,
        "c6_protocol_built_in_decision_count": 0,
        "c6_protocol_emitted_in_decision_count": 0,
        "runtime_patched_count": 0,
        "c7_authorized_count": 0,
        "new_domain_shift_executed_count": 0,
        "examples_reviewed": closure_summary.get("examples_reviewed"),
        "example_type_count": len(closure_summary.get("example_types_reviewed", [])),
        "full_transfer_claim_count": 0,
        "global_autonomy_claim_count": 0,
        "general_cell1_authority_claim_count": 0,
        "runtime_wide_enforcement_claim_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "c5_reference_mutated_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    zero_keys = [
        "c6_protocol_built_in_decision_count",
        "c6_protocol_emitted_in_decision_count",
        "runtime_patched_count",
        "c7_authorized_count",
        "new_domain_shift_executed_count",
        "full_transfer_claim_count",
        "global_autonomy_claim_count",
        "general_cell1_authority_claim_count",
        "runtime_wide_enforcement_claim_count",
        "source_mutated_count",
        "prior_receipt_mutated_count",
        "c5_reference_mutated_count",
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "c6_post_example_reference_decision_profile_v0",
        "profile_id": "c6_post_example_reference_decision_" + sig8(rollup),
        "status": status,
        "selected_next_unit": recommended_next,
        "future_build_unit": FUTURE_BUILD_UNIT if decision_pass else None,
        "decision": "design C6 inter-cell protocol target from reviewed C5-to-C6 example reference",
        "schema_claim": "TARGET_DESIGN_SELECTION_ONLY",
        "examples_reviewed": closure_summary.get("examples_reviewed"),
        "bad_counters_zero": all(rollup[k] == 0 for k in zero_keys),
        "c6_protocol_built_in_decision": False,
        "c6_protocol_emitted_in_decision": False,
        "c7_authorized": False,
        "runtime_patched": False,
        "recommendation": "Run the C6 protocol target design unit next; build only after design/review/closure.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "c6_post_example_reference_decision_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The post-example-reference decision selected C6 inter-cell protocol target design from the reviewed C5-to-C6 example reference. It did not build or emit the C6 protocol, patch runtime, authorize C7, run a new domain shift, or claim transfer/autonomy/general Cell 1 authority.",
        "selected_next_unit": recommended_next,
        "future_build_unit_after_design": FUTURE_BUILD_UNIT if decision_pass else None,
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "c6_post_example_reference_decision_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c6_example_reference_closure",
                "question": "is the reviewed C5-to-C6 example reference frozen and decision-ready",
                "answer": "yes" if decision_pass else "no",
                "taken": "evaluate C6 protocol target design branch",
            },
            {
                "step": "select_target_design_before_build",
                "question": "should C6 build directly or design the target first",
                "answer": SELECTED_NEXT_UNIT if decision_pass else recommended_next,
                "taken": "authorize target design only",
            },
            {
                "step": "preserve_no_protocol_build_boundary",
                "question": "does this decision build/emit C6 protocol or authorize C7",
                "answer": "no",
                "taken": "stop with selected target design unit",
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
        (C6_TARGET_DESIGN_AUTH_PATH, target_design_auth),
        (C6_OBJECTIVE_BINDING_PATH, objective_binding),
        (C6_DESIGN_TARGET_SEED_PATH, design_target_seed),
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
        "POST_C6_EXAMPLE_DECISION_0_REFERENCE_CLOSURE_RECEIPT_CONSUMED": SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH.exists(),
        "POST_C6_EXAMPLE_DECISION_1_DECISION_BASIS_EMITTED": DECISION_BASIS_PATH.exists(),
        "POST_C6_EXAMPLE_DECISION_2_REVIEWED_EXAMPLE_REFERENCE_CONFIRMED": decision_basis["post_example_reference_decision_ready"] is True,
        "POST_C6_EXAMPLE_DECISION_3_OPTIONS_EMITTED": DECISION_OPTIONS_PATH.exists(),
        "POST_C6_EXAMPLE_DECISION_4_PROTOCOL_TARGET_DESIGN_SELECTED": selected_branch["selected_next_unit"] == SELECTED_NEXT_UNIT,
        "POST_C6_EXAMPLE_DECISION_5_PROTOCOL_TARGET_DESIGN_AUTHORIZED_NEXT": target_design_auth["authorized_next_unit"] == SELECTED_NEXT_UNIT,
        "POST_C6_EXAMPLE_DECISION_6_OBJECTIVE_BOUND_AS_TARGET_DESIGN_INPUT": objective_binding["objective_status"] == "BOUND_AS_TARGET_DESIGN_INPUT",
        "POST_C6_EXAMPLE_DECISION_7_TARGET_DESIGN_SEED_EMITTED": C6_DESIGN_TARGET_SEED_PATH.exists() and design_target_seed["target_design_ready"] is True,
        "POST_C6_EXAMPLE_DECISION_8_NO_PROTOCOL_BUILD_IN_DECISION": classification["c6_protocol_built_in_decision"] is False,
        "POST_C6_EXAMPLE_DECISION_9_NO_PROTOCOL_EMISSION_IN_DECISION": classification["c6_protocol_emitted_in_decision"] is False,
        "POST_C6_EXAMPLE_DECISION_10_NO_RUNTIME_PATCH": classification["runtime_patched"] is False,
        "POST_C6_EXAMPLE_DECISION_11_NO_C7_AUTHORIZATION": classification["c7_authorized"] is False,
        "POST_C6_EXAMPLE_DECISION_12_NO_NEW_DOMAIN_SHIFT": classification["new_domain_shift_executed"] is False,
        "POST_C6_EXAMPLE_DECISION_13_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "POST_C6_EXAMPLE_DECISION_14_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["c5_reference_mutated"] is False,
        "POST_C6_EXAMPLE_DECISION_15_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "POST_C6_EXAMPLE_DECISION_16_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "POST_C6_EXAMPLE_DECISION_17_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_C6_POST_EXAMPLE_REFERENCE_DECISION_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_C6_POST_EXAMPLE_REFERENCE_DECISION_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_C6_POST_EXAMPLE_REFERENCE_DECISION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "selected_next_unit": final_next,
        "source_reference": SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "c6_post_example_reference_decision_receipt_v0",
        "receipt_type": "TYPED_C6_POST_EXAMPLE_REFERENCE_DECISION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_c6_example_reference_closure_receipt_id": SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID,
        "machine_readable_c6_post_example_reference_decision_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "post_example_reference_decision_complete": gate == "PASS",
            "selected_next_branch": SELECTED_BRANCH if gate == "PASS" else None,
            "selected_next_unit": final_next,
            "future_build_unit": FUTURE_BUILD_UNIT if gate == "PASS" else None,
            "c6_protocol_target_design_authorized_next": gate == "PASS",
            "c6_protocol_built_in_decision": False,
            "c6_protocol_emitted_in_decision": False,
            "runtime_patched": False,
            "c7_authorized": False,
            "new_domain_shift_executed": False,
            "examples_reviewed": closure_summary.get("examples_reviewed"),
            "example_types_reviewed": closure_summary.get("example_types_reviewed", []),
            "bad_counters_zero": profile["bad_counters_zero"],
            "full_transfer_claimed": False,
            "global_autonomy_claimed": False,
            "general_cell1_authority_claimed": False,
            "runtime_wide_enforcement_claimed": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "c5_reference_mutated": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "recommended_next": final_next,
        },
        "aggregate_metrics": report | {"status": final_status, "recommended_next_handling": final_next},
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "decision_basis": rel(DECISION_BASIS_PATH),
            "decision_options": rel(DECISION_OPTIONS_PATH),
            "selected_branch": rel(SELECTED_BRANCH_PATH),
            "target_design_authorization": rel(C6_TARGET_DESIGN_AUTH_PATH),
            "objective_binding": rel(C6_OBJECTIVE_BINDING_PATH),
            "target_design_seed": rel(C6_DESIGN_TARGET_SEED_PATH),
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
    print(f"post_c6_example_reference_decision_receipt_id={receipt_id}")
    print(f"post_c6_example_reference_decision_receipt_path={rel(receipt_path)}")
    print(f"post_c6_example_reference_decision_basis_path={rel(DECISION_BASIS_PATH)}")
    print(f"c6_protocol_target_design_authorization_path={rel(C6_TARGET_DESIGN_AUTH_PATH)}")
    print(f"c6_protocol_target_design_seed_path={rel(C6_DESIGN_TARGET_SEED_PATH)}")
    print(f"post_c6_example_reference_decision_rollup_path={rel(ROLLUP_PATH)}")
    print(f"post_c6_example_reference_decision_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
