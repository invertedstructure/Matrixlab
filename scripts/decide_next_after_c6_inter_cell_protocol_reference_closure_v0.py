#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_AFTER_C6_INTER_CELL_PROTOCOL_REFERENCE_CLOSURE_V0"
TARGET_UNIT_ID = "inter_cell.protocol.reference.post_closure_decision.v0"
LAYER = "BRIDGE / INTER_CELL_PROTOCOL / POST_REFERENCE_DECISION"
MODE = "DECIDE_ONLY / SELECT_NEXT_BRANCH / NO_RUNTIME_PATCH"
BUILD_MODE = "POST_C6_PROTOCOL_REFERENCE_DECISION_ONLY"

SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID = "50849d13"
SOURCE_C6_PROTOCOL_REVIEW_RECEIPT_ID = "7535b889"
SOURCE_C6_PROTOCOL_RECEIPT_ID = "315e0d94"
SOURCE_C6_TARGET_DESIGN_RECEIPT_ID = "b0df3c9d"
SOURCE_POST_C6_DECISION_RECEIPT_ID = "89b2d2cc"
SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID = "fe882749"

SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0_receipts/50849d13.json"

C6_PROTOCOL_REVIEWED_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_reviewed_reference_v0.json"
C6_PROTOCOL_FREEZE_MANIFEST_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_reviewed_reference_freeze_manifest_v0.json"
C6_PROTOCOL_REFERENCE_INDEX_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_reviewed_reference_index_v0.json"
C6_PACKET_LAW_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_packet_law_reference_v0.json"
C6_PROTOCOL_SURFACE_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_surface_reference_v0.json"
C6_GATE19_REPAIR_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_gate19_repair_reference_v0.json"
C6_POST_CLOSURE_DECISION_READY_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_reference_post_closure_decision_ready_v0.json"
C6_REFERENCE_AUTHORITY_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_reference_closure_authority_boundary_v0.json"
C6_REFERENCE_CLASSIFICATION_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_reference_closure_classification_v0.json"
C6_REFERENCE_ROLLUP_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_reference_closure_rollup_v0.json"
C6_REFERENCE_PROFILE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_reference_closure_profile_v0.json"
C6_REFERENCE_REPORT_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_reference_closure_report.json"
C6_REFERENCE_TRACE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_reference_closure_transition_trace.json"

SOURCE_C6_PROTOCOL_REVIEW_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0_receipts/7535b889.json"
SOURCE_C6_PROTOCOL_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0_receipts/315e0d94.json"
SOURCE_C6_TARGET_DESIGN_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0_receipts/b0df3c9d.json"
SOURCE_POST_C6_DECISION_RECEIPT_PATH = ROOT / "data/c6_post_example_reference_decision_v0_receipts/89b2d2cc.json"
SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0_receipts/fe882749.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH,
    C6_PROTOCOL_REVIEWED_REFERENCE_PATH,
    C6_PROTOCOL_FREEZE_MANIFEST_PATH,
    C6_PROTOCOL_REFERENCE_INDEX_PATH,
    C6_PACKET_LAW_REFERENCE_PATH,
    C6_PROTOCOL_SURFACE_REFERENCE_PATH,
    C6_GATE19_REPAIR_REFERENCE_PATH,
    C6_POST_CLOSURE_DECISION_READY_PATH,
    C6_REFERENCE_AUTHORITY_PATH,
    C6_REFERENCE_CLASSIFICATION_PATH,
    C6_REFERENCE_ROLLUP_PATH,
    C6_REFERENCE_PROFILE_PATH,
    C6_REFERENCE_REPORT_PATH,
    C6_REFERENCE_TRACE_PATH,
    SOURCE_C6_PROTOCOL_REVIEW_RECEIPT_PATH,
    SOURCE_C6_PROTOCOL_RECEIPT_PATH,
    SOURCE_C6_TARGET_DESIGN_RECEIPT_PATH,
    SOURCE_POST_C6_DECISION_RECEIPT_PATH,
    SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH,
]

OUT_DIR = ROOT / "data/c6_inter_cell_protocol_post_reference_decision_v0"
RECEIPT_DIR = ROOT / "data/c6_inter_cell_protocol_post_reference_decision_v0_receipts"

DECISION_BASIS_PATH = OUT_DIR / "post_c6_protocol_reference_decision_basis_v0.json"
DECISION_OPTIONS_PATH = OUT_DIR / "post_c6_protocol_reference_decision_options_v0.json"
SELECTED_BRANCH_PATH = OUT_DIR / "post_c6_protocol_reference_selected_branch_v0.json"
BOUNDED_ADOPTION_PROBE_TARGET_PATH = OUT_DIR / "c6_bounded_protocol_adoption_probe_target_v0.json"
REFERENCE_PARK_RECORD_PATH = OUT_DIR / "c6_protocol_reference_park_record_v0.json"
DEFERRED_BRANCHES_PATH = OUT_DIR / "post_c6_protocol_reference_deferred_branches_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "post_c6_protocol_reference_decision_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "post_c6_protocol_reference_decision_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "post_c6_protocol_reference_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "post_c6_protocol_reference_decision_profile_v0.json"
REPORT_PATH = OUT_DIR / "post_c6_protocol_reference_decision_report.json"
TRACE_PATH = OUT_DIR / "post_c6_protocol_reference_decision_transition_trace.json"

EXPECTED_SOURCE_STATUS = "TYPED_C6_INTER_CELL_PROTOCOL_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY"
EXPECTED_SOURCE_STOP = "STOP_TYPED_C6_INTER_CELL_PROTOCOL_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY"
EXPECTED_SOURCE_NEXT = "DECIDE_NEXT_AFTER_C6_INTER_CELL_PROTOCOL_REFERENCE_CLOSURE_V0"

SELECTED_BRANCH = "DESIGN_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE"
SELECTED_NEXT_UNIT = "DESIGN_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_FROM_REVIEWED_REFERENCE_V0"

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

    closure_receipt = read_json(SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH)
    closure_summary = closure_receipt.get("machine_readable_c6_protocol_reference_closure_summary", {})

    reviewed_reference = read_json(C6_PROTOCOL_REVIEWED_REFERENCE_PATH)
    freeze_manifest = read_json(C6_PROTOCOL_FREEZE_MANIFEST_PATH)
    reference_index = read_json(C6_PROTOCOL_REFERENCE_INDEX_PATH)
    packet_law_reference = read_json(C6_PACKET_LAW_REFERENCE_PATH)
    protocol_surface_reference = read_json(C6_PROTOCOL_SURFACE_REFERENCE_PATH)
    gate19_repair_reference = read_json(C6_GATE19_REPAIR_REFERENCE_PATH)
    post_closure_decision_ready = read_json(C6_POST_CLOSURE_DECISION_READY_PATH)
    authority = read_json(C6_REFERENCE_AUTHORITY_PATH)
    classification = read_json(C6_REFERENCE_CLASSIFICATION_PATH)
    rollup = read_json(C6_REFERENCE_ROLLUP_PATH)
    profile = read_json(C6_REFERENCE_PROFILE_PATH)
    report = read_json(C6_REFERENCE_REPORT_PATH)
    trace = read_json(C6_REFERENCE_TRACE_PATH)

    review_receipt = read_json(SOURCE_C6_PROTOCOL_REVIEW_RECEIPT_PATH)
    protocol_receipt = read_json(SOURCE_C6_PROTOCOL_RECEIPT_PATH)
    target_receipt = read_json(SOURCE_C6_TARGET_DESIGN_RECEIPT_PATH)
    post_c6_decision_receipt = read_json(SOURCE_POST_C6_DECISION_RECEIPT_PATH)
    example_reference_closure = read_json(SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH)

    if closure_receipt.get("receipt_id") != SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID or closure_receipt.get("gate") != "PASS":
        failures.append("source_c6_protocol_reference_closure_receipt_not_pass")
    if closure_receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_stop_wrong")
    if closure_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_hidden_next")
    if closure_summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_status_wrong:{closure_summary.get('status')}")
    if closure_summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_next_wrong:{closure_summary.get('recommended_next')}")

    for key in [
        "c6_inter_cell_protocol_closed_as_reviewed_reference",
        "reviewed_reference_frozen",
        "post_c6_protocol_reference_decision_ready",
        "all_c6_protocol_acceptance_gates_true",
        "gate19_verification_not_closure",
        "gate19_repair_history_preserved",
        "bad_counters_zero",
    ]:
        if closure_summary.get(key) is not True:
            failures.append(f"closure_required_true_missing:{key}")

    if closure_summary.get("schema_claim") != "LOCAL_PROTOCOL_CANDIDATE_ONLY":
        failures.append("closure_schema_claim_wrong")
    if closure_summary.get("packet_family_declared") != 9:
        failures.append("packet_family_count_wrong")
    if closure_summary.get("packet_schemas_emitted") != 9:
        failures.append("packet_schema_count_wrong")
    if closure_summary.get("derivation_status_records_emitted") != 14:
        failures.append("derivation_count_wrong")
    if closure_summary.get("demo_packets_emitted") != 4:
        failures.append("demo_packet_count_wrong")

    for key in [
        "runtime_patched",
        "c7_authorized",
        "new_domain_shift_executed",
        "general_cell1_authority_claimed",
        "global_autonomy_claimed",
        "full_transfer_claimed",
        "runtime_wide_enforcement_claimed",
        "source_mutated",
        "prior_receipt_mutated",
        "c5_reference_mutated",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if closure_summary.get(key) is not False:
            failures.append(f"closure_forbidden_true:{key}")

    if reviewed_reference.get("reference_status") != "C6_INTER_CELL_PROTOCOL_REVIEWED_REFERENCE_FROZEN":
        failures.append("reviewed_reference_not_frozen")
    if freeze_manifest.get("freeze_status") != "FROZEN":
        failures.append("freeze_manifest_not_frozen")
    if reference_index.get("index_status") != "REFERENCE_INDEX_EMITTED":
        failures.append("reference_index_wrong")
    if packet_law_reference.get("packet_law_status") != "REVIEWED_REFERENCE":
        failures.append("packet_law_status_wrong")
    if protocol_surface_reference.get("surface_status") != "FROZEN_REVIEWED_REFERENCE":
        failures.append("surface_reference_wrong")
    if gate19_repair_reference.get("repair_class") != "ASSERTION_REPAIR_NOT_PROTOCOL_REDESIGN":
        failures.append("gate19_repair_reference_wrong")
    if post_closure_decision_ready.get("decision_ready") is not True:
        failures.append("post_closure_decision_not_ready")
    if post_closure_decision_ready.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append("post_closure_decision_next_wrong")

    if authority.get("may_decide_next_after_c6_protocol_reference_closure") is not True:
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
        "may_mutate_c5_reference",
    ]:
        if authority.get(forbidden) is not False:
            failures.append(f"authority_forbidden_true:{forbidden}")

    if classification.get("next_command_goal") is not None:
        failures.append("classification_hidden_next")
    if rollup.get("post_c6_protocol_reference_decision_ready_count") != 1:
        failures.append("rollup_decision_ready_wrong")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if report.get("recommended_next_handling") != EXPECTED_SOURCE_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_hidden_next")

    for ancestor, expected, name in [
        (review_receipt, SOURCE_C6_PROTOCOL_REVIEW_RECEIPT_ID, "review"),
        (protocol_receipt, SOURCE_C6_PROTOCOL_RECEIPT_ID, "protocol"),
        (target_receipt, SOURCE_C6_TARGET_DESIGN_RECEIPT_ID, "target"),
        (post_c6_decision_receipt, SOURCE_POST_C6_DECISION_RECEIPT_ID, "post_c6_decision"),
        (example_reference_closure, SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID, "example_reference_closure"),
    ]:
        if ancestor.get("receipt_id") != expected or ancestor.get("gate") != "PASS":
            failures.append(f"ancestor_not_pass:{name}")

    return failures, {
        "closure_summary": closure_summary,
        "reviewed_reference": reviewed_reference,
        "packet_law_reference": packet_law_reference,
        "protocol_surface_reference": protocol_surface_reference,
        "post_closure_decision_ready": post_closure_decision_ready,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    decision_pass = not failures
    status = "TYPED_POST_C6_PROTOCOL_REFERENCE_DECISION_SELECTED_BOUNDED_ADOPTION_PROBE_READY" if decision_pass else "TYPED_POST_C6_PROTOCOL_REFERENCE_DECISION_GATE_FAIL"
    recommended_next = SELECTED_NEXT_UNIT if decision_pass else "REPAIR_POST_C6_PROTOCOL_REFERENCE_DECISION_V0"

    closure_summary = basis.get("closure_summary", {})
    reviewed_reference = basis.get("reviewed_reference", {})
    packet_law_reference = basis.get("packet_law_reference", {})
    protocol_surface_reference = basis.get("protocol_surface_reference", {})
    post_closure_decision_ready = basis.get("post_closure_decision_ready", {})

    reason_codes = [
        "POST_C6_PROTOCOL_REFERENCE_DECISION_COMPLETE",
        "C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_CONSUMED",
        "C6_REVIEWED_PROTOCOL_REFERENCE_CONFIRMED",
        "PACKET_LAW_REFERENCE_CONFIRMED",
        "PROTOCOL_SURFACE_REFERENCE_CONFIRMED",
        "GATE19_REPAIR_HISTORY_CONFIRMED",
        "BOUNDED_PROTOCOL_ADOPTION_PROBE_SELECTED",
        "REFERENCE_PARKED_AS_AVAILABLE_OBJECT",
        "NO_RUNTIME_PATCH",
        "NO_C7_AUTHORIZATION",
        "NO_TRANSFER_CLAIM",
        "NO_GLOBAL_AUTONOMY_CLAIM",
        "NO_GENERAL_CELL1_AUTHORITY_CLAIM",
        "NO_RUNTIME_WIDE_ENFORCEMENT_CLAIM",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if decision_pass else failures

    decision_basis = {
        "schema_version": "post_c6_protocol_reference_decision_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if decision_pass else "BASIS_REPAIR_REQUIRED",
        "source_c6_protocol_reference_closure_receipt_id": SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID,
        "source_c6_protocol_review_receipt_id": SOURCE_C6_PROTOCOL_REVIEW_RECEIPT_ID,
        "source_c6_protocol_receipt_id": SOURCE_C6_PROTOCOL_RECEIPT_ID,
        "reference_status": reviewed_reference.get("reference_status"),
        "schema_claim": closure_summary.get("schema_claim"),
        "post_closure_decision_options": post_closure_decision_ready.get("decision_options", []),
        "packet_law_compression": "Cells do not pass vibes. Cells pass packets.",
        "decision_ready": decision_pass,
    }

    decision_options = {
        "schema_version": "post_c6_protocol_reference_decision_options_v0",
        "decision_status": "NEXT_BRANCH_SELECTED" if decision_pass else "NO_BRANCH_SELECTED",
        "options": [
            {
                "branch": SELECTED_BRANCH,
                "selected": decision_pass,
                "next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
                "why": "The C6 protocol is frozen as a reviewed reference. The next useful move is a bounded adoption probe design, not runtime-wide adoption.",
            },
            {
                "branch": "PARK_C6_PROTOCOL_REFERENCE_ONLY",
                "selected": False,
                "next_unit": None,
                "why": "Reference remains parked and available, but parking alone does not test the packet-law surface.",
            },
            {
                "branch": "RETURN_TO_OBSERVATION_HARDENING_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Important soon, but the C6 protocol should first get one bounded adoption-probe design so observation hardening has packet edges to inspect.",
            },
            {
                "branch": "OPEN_C7",
                "selected": False,
                "next_unit": None,
                "why": "Forbidden here. C7 requires explicit later authorization after bounded protocol handling is tested.",
            },
            {
                "branch": "PATCH_RUNTIME_WITH_C6_PROTOCOL",
                "selected": False,
                "next_unit": None,
                "why": "Too broad. Runtime-wide enforcement is explicitly not authorized by the C6 reference closure.",
            },
        ],
    }

    selected_branch = {
        "schema_version": "post_c6_protocol_reference_selected_branch_v0",
        "selected_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "selected_scope": "design one bounded adoption probe for the reviewed C6 local inter-cell protocol reference",
        "selected_does_not": [
            "patch runtime",
            "run C7",
            "claim full transfer",
            "claim global autonomy",
            "grant general Cell 1 authority",
            "claim runtime-wide enforcement",
            "mutate C6 reviewed reference",
        ],
    }

    bounded_adoption_probe_target = {
        "schema_version": "c6_bounded_protocol_adoption_probe_target_v0",
        "target_status": "BOUNDED_ADOPTION_PROBE_TARGET_SELECTED" if decision_pass else "NOT_SELECTED",
        "target_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "source_reference_receipt": SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID,
        "probe_goal": "Design a bounded probe that consumes the reviewed C6 packet-law reference and applies it to one explicit inter-cell flow without runtime-wide adoption.",
        "probe_must_consume": [
            "reviewed C6 protocol reference",
            "packet-law reference",
            "protocol surface reference",
            "gate19 repair reference",
        ],
        "probe_must_test": [
            "proposed-only packet is not Cell 1 consumable",
            "accepted packet requires review receipt",
            "Cell 1 intake is scoped",
            "probe/build is not verification",
            "verification is not closure",
            "handoff is not hidden next command",
            "blocked feedback is not repair",
            "edge observation sidecar is emitted",
            "unit feedback sidecar is emitted for block/failure/stop/NA",
        ],
        "probe_must_not_do": [
            "patch runtime",
            "claim runtime-wide enforcement",
            "authorize C7",
            "execute new domain shift",
            "claim transfer",
            "claim autonomy",
            "grant general Cell 1 authority",
        ],
    }

    reference_park_record = {
        "schema_version": "c6_protocol_reference_park_record_v0",
        "park_status": "PARKED_AS_REVIEWED_REFERENCE_AVAILABLE_FOR_CONSUMPTION",
        "reference_receipt": SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID,
        "reference_path": rel(C6_PROTOCOL_REVIEWED_REFERENCE_PATH),
        "packet_law_reference_path": rel(C6_PACKET_LAW_REFERENCE_PATH),
        "meaning": "C6 remains a reviewed local protocol candidate reference. It can be consumed by bounded future units but does not itself change runtime behavior.",
    }

    deferred_branches = {
        "schema_version": "post_c6_protocol_reference_deferred_branches_v0",
        "deferred": [
            "OPEN_C7",
            "PATCH_RUNTIME_WITH_C6_PROTOCOL",
            "CLAIM_RUNTIME_WIDE_ENFORCEMENT",
            "CLAIM_FULL_TRANSFER",
            "CLAIM_GLOBAL_AUTONOMY",
            "GRANT_GENERAL_CELL1_AUTHORITY",
            "RUN_NEW_DOMAIN_SHIFT",
        ],
        "why": "The current legal edge is bounded adoption-probe design only.",
    }

    authority_boundary = {
        "schema_version": "post_c6_protocol_reference_decision_authority_boundary_v0",
        "status": status,
        "may_design_bounded_c6_protocol_adoption_probe_next": decision_pass,
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
    }

    classification = {
        "schema_version": "post_c6_protocol_reference_decision_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "post_c6_protocol_reference_decision_complete": decision_pass,
        "selected_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": recommended_next,
        "bounded_adoption_probe_design_ready": decision_pass,
        "c6_reference_parked_available": decision_pass,
        "schema_claim": "POST_REFERENCE_DECISION_ONLY",
        "source_reference_status": reviewed_reference.get("reference_status"),
        "packet_family_declared": closure_summary.get("packet_family_declared"),
        "packet_schemas_emitted": closure_summary.get("packet_schemas_emitted"),
        "all_c6_protocol_acceptance_gates_true": closure_summary.get("all_c6_protocol_acceptance_gates_true"),
        "gate19_verification_not_closure": closure_summary.get("gate19_verification_not_closure"),
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
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": True,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "post_c6_protocol_reference_decision_rollup_v0",
        "decision_count": 1 if decision_pass else 0,
        "bounded_adoption_probe_selected_count": 1 if decision_pass else 0,
        "reference_parked_available_count": 1 if decision_pass else 0,
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
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    profile = {
        "schema_version": "post_c6_protocol_reference_decision_profile_v0",
        "profile_id": "post_c6_protocol_reference_decision_" + sig8(rollup),
        "status": status,
        "decision": "select bounded adoption-probe design from reviewed C6 protocol reference",
        "why_this_edge": "The protocol reference exists, but broad runtime adoption is not authorized. A bounded adoption-probe design is the smallest useful next test.",
        "reference_compression": "Cells do not pass vibes. Cells pass packets.",
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
        "schema_version": "post_c6_protocol_reference_decision_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The post-C6 protocol reference decision consumed the frozen C6 packet-law reference and selected a bounded adoption-probe design as the next lawful object. It did not patch runtime, authorize C7, execute a new domain shift, or claim transfer/autonomy/general Cell 1 authority.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "post_c6_protocol_reference_decision_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c6_protocol_reference_closure",
                "question": "is the C6 protocol reference frozen and decision-ready",
                "answer": "yes" if decision_pass else "no",
                "taken": "evaluate next branch options",
            },
            {
                "step": "select_bounded_probe_design",
                "question": "what is the smallest useful next edge",
                "answer": SELECTED_NEXT_UNIT if decision_pass else recommended_next,
                "taken": "select bounded adoption-probe design",
            },
            {
                "step": "preserve_boundary",
                "question": "does this patch runtime, authorize C7, or claim transfer/autonomy",
                "answer": "no",
                "taken": "stop with selected bounded probe design",
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
        (BOUNDED_ADOPTION_PROBE_TARGET_PATH, bounded_adoption_probe_target),
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
        "POST_C6_PROTOCOL_DECISION_0_REFERENCE_CLOSURE_RECEIPT_CONSUMED": SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH.exists(),
        "POST_C6_PROTOCOL_DECISION_1_REVIEWED_REFERENCE_CONFIRMED": reviewed_reference.get("reference_status") == "C6_INTER_CELL_PROTOCOL_REVIEWED_REFERENCE_FROZEN",
        "POST_C6_PROTOCOL_DECISION_2_PACKET_LAW_REFERENCE_CONFIRMED": packet_law_reference.get("packet_law_status") == "REVIEWED_REFERENCE",
        "POST_C6_PROTOCOL_DECISION_3_PROTOCOL_SURFACE_CONFIRMED": protocol_surface_reference.get("surface_status") == "FROZEN_REVIEWED_REFERENCE",
        "POST_C6_PROTOCOL_DECISION_4_DECISION_BASIS_EMITTED": DECISION_BASIS_PATH.exists(),
        "POST_C6_PROTOCOL_DECISION_5_OPTIONS_EMITTED": DECISION_OPTIONS_PATH.exists(),
        "POST_C6_PROTOCOL_DECISION_6_BOUNDED_ADOPTION_PROBE_SELECTED": selected_branch["selected_next_unit"] == SELECTED_NEXT_UNIT,
        "POST_C6_PROTOCOL_DECISION_7_BOUNDED_ADOPTION_PROBE_TARGET_EMITTED": BOUNDED_ADOPTION_PROBE_TARGET_PATH.exists(),
        "POST_C6_PROTOCOL_DECISION_8_REFERENCE_PARK_RECORD_EMITTED": REFERENCE_PARK_RECORD_PATH.exists(),
        "POST_C6_PROTOCOL_DECISION_9_DEFERRED_FORBIDDEN_BRANCHES_EMITTED": DEFERRED_BRANCHES_PATH.exists(),
        "POST_C6_PROTOCOL_DECISION_10_NO_RUNTIME_PATCH_OR_C7": classification["runtime_patched"] is False and classification["c7_authorized"] is False,
        "POST_C6_PROTOCOL_DECISION_11_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "POST_C6_PROTOCOL_DECISION_12_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["c6_reviewed_reference_mutated"] is False,
        "POST_C6_PROTOCOL_DECISION_13_BAD_COUNTERS_ZERO": classification["bad_counters_zero"] is True,
        "POST_C6_PROTOCOL_DECISION_14_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "POST_C6_PROTOCOL_DECISION_15_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "POST_C6_PROTOCOL_DECISION_16_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_POST_C6_PROTOCOL_REFERENCE_DECISION_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_POST_C6_PROTOCOL_REFERENCE_DECISION_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_POST_C6_PROTOCOL_REFERENCE_DECISION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_reference": SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID,
        "selected_next": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "post_c6_protocol_reference_decision_receipt_v0",
        "receipt_type": "TYPED_POST_C6_PROTOCOL_REFERENCE_DECISION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_c6_protocol_reference_closure_receipt_id": SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID,
        "machine_readable_post_c6_protocol_reference_decision_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "post_c6_protocol_reference_decision_complete": gate == "PASS",
            "selected_branch": SELECTED_BRANCH if gate == "PASS" else None,
            "selected_next_unit": final_next,
            "bounded_adoption_probe_design_ready": gate == "PASS",
            "c6_reference_parked_available": gate == "PASS",
            "source_reference_status": reviewed_reference.get("reference_status"),
            "schema_claim": "POST_REFERENCE_DECISION_ONLY",
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
            "bounded_adoption_probe_target": rel(BOUNDED_ADOPTION_PROBE_TARGET_PATH),
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
    print(f"post_c6_protocol_reference_decision_receipt_id={receipt_id}")
    print(f"post_c6_protocol_reference_decision_receipt_path={rel(receipt_path)}")
    print(f"bounded_adoption_probe_target_path={rel(BOUNDED_ADOPTION_PROBE_TARGET_PATH)}")
    print(f"post_c6_protocol_reference_decision_rollup_path={rel(ROLLUP_PATH)}")
    print(f"post_c6_protocol_reference_decision_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
