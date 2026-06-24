#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REQUEST_NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_evidence_request.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_EVIDENCE_REQUEST"
MODE = "REQUEST / NARROWER_TARGET_EVIDENCE / NO_PATCH"
BUILD_MODE = "NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_REQUEST_ONLY"

SOURCE_TARGET_NARROWING_RECEIPT_ID = "5b18437f"
SOURCE_TARGET_NARROWING_RECEIPT_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_run_v0_receipts" / "5b18437f.json"
SOURCE_TARGET_HINT_SCAN_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_run_v0" / "declared_source_target_hint_scan_v0.json"
SOURCE_TARGET_CANDIDATE_RECORD_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_run_v0" / "target_candidate_record_v0.json"
SOURCE_TARGET_CANDIDATE_CLASSIFICATION_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_run_v0" / "target_candidate_classification_v0.json"
SOURCE_TARGET_CLASSIFICATION_REQUEST_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_run_v0" / "target_candidate_review_classification_request_v0.json"
SOURCE_TARGET_NARROWING_AUTHORITY_AUDIT_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_run_v0" / "target_narrowing_authority_audit_v0.json"
SOURCE_TARGET_NARROWING_ROLLUP_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_run_v0" / "target_narrowing_surface_rollup_v0.json"
SOURCE_TARGET_NARROWING_PROFILE_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_run_v0" / "target_narrowing_surface_profile_v0.json"

SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_ID = "07bc35ea"
SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_design_v0_receipts" / "07bc35ea.json"
SOURCE_TARGET_CANDIDATE_CONTRACT_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_design_v0" / "bounded_target_candidate_contract_v0.json"
SOURCE_TARGET_NARROWING_DESIGN_RECORD_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_design_v0" / "target_narrowing_surface_design_record_v0.json"

SOURCE_PRECHECK_RECEIPT_ID = "c534ce7c"
SOURCE_PRECHECK_RECEIPT_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_run_v0_receipts" / "c534ce7c.json"
SOURCE_PRECHECK_CLASSIFICATION_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_run_v0" / "runtime_patch_precheck_eligibility_classification_v0.json"
SOURCE_PRECHECK_TARGET_SCAN_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_run_v0" / "bounded_runtime_patch_target_candidate_scan_v0.json"

SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID = "71bd1d92"
SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0_receipts" / "71bd1d92.json"
SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0" / "accepted_proposal_packet_v0.json"

SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID = "1d7c0a9b"
SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH = ROOT / "data" / "cell1_handoff_return_loop_review_or_close_v0_receipts" / "1d7c0a9b.json"
SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH = ROOT / "data" / "cell1_handoff_return_loop_review_or_close_v0" / "handoff_return_loop_frozen_reference_packet_v0.json"

SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID = "e1bc0ed0"
SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0_receipts" / "e1bc0ed0.json"
SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0" / "cell1_schema_test_frozen_reference_packet_v0.json"

SOURCE_C1_PATCH_RECEIPT_ID = "fffa3dd5"
SOURCE_C1_PATCH_RECEIPT_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0_receipts" / "fffa3dd5.json"
SOURCE_C1_PATCH_SCHEMA_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0" / "proposal_packet_schema_v0_1.json"

SOURCE_C2_RECEIPT_ID = "348dabde"
SOURCE_C2_RECEIPT_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts" / "348dabde.json"
SOURCE_C2_LANE_REGISTRY_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "taxonomy_lane_registry_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_TARGET_NARROWING_RECEIPT_PATH,
    SOURCE_TARGET_HINT_SCAN_PATH,
    SOURCE_TARGET_CANDIDATE_RECORD_PATH,
    SOURCE_TARGET_CANDIDATE_CLASSIFICATION_PATH,
    SOURCE_TARGET_CLASSIFICATION_REQUEST_PATH,
    SOURCE_TARGET_NARROWING_AUTHORITY_AUDIT_PATH,
    SOURCE_TARGET_NARROWING_ROLLUP_PATH,
    SOURCE_TARGET_NARROWING_PROFILE_PATH,
    SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_PATH,
    SOURCE_TARGET_CANDIDATE_CONTRACT_PATH,
    SOURCE_TARGET_NARROWING_DESIGN_RECORD_PATH,
    SOURCE_PRECHECK_RECEIPT_PATH,
    SOURCE_PRECHECK_CLASSIFICATION_PATH,
    SOURCE_PRECHECK_TARGET_SCAN_PATH,
    SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH,
    SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH,
    SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH,
    SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH,
    SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_PATH,
    SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH,
    SOURCE_C1_PATCH_RECEIPT_PATH,
    SOURCE_C1_PATCH_SCHEMA_PATH,
    SOURCE_C2_RECEIPT_PATH,
    SOURCE_C2_LANE_REGISTRY_PATH,
]

OUT_DIR = ROOT / "data" / "cell1_runtime_patch_target_evidence_request_v0"
RECEIPT_DIR = ROOT / "data" / "cell1_runtime_patch_target_evidence_request_v0_receipts"

SOURCE_SURFACE_PATH = OUT_DIR / "source_surface_v0.json"
TARGET_AMBIGUITY_READOUT_PATH = OUT_DIR / "target_ambiguity_readout_v0.json"
TARGET_HINT_INVENTORY_PATH = OUT_DIR / "target_hint_inventory_v0.json"
NARROWER_EVIDENCE_REQUEST_PACKET_PATH = OUT_DIR / "narrower_runtime_patch_target_evidence_request_packet_v0.json"
TARGET_EVIDENCE_PACKET_SCHEMA_PATH = OUT_DIR / "runtime_patch_target_evidence_packet_schema_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "target_evidence_request_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "target_evidence_request_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "target_evidence_request_profile_v0.json"
REPORT_PATH = OUT_DIR / "target_evidence_request_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "target_evidence_request_transition_trace.json"

RECOMMENDED_NEXT = "PROVIDE_OR_REVIEW_NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_V0"

ZERO_COUNTER_KEYS = [
    "runtime_patch_applied_count",
    "target_file_modified_count",
    "target_candidate_declared_count",
    "c5_opened_count",
    "general_cell1_authority_granted_count",
    "taxonomy_registry_mutation_count",
    "proposal_status_promoted_count",
    "accepted_proposal_fabricated_count",
    "source_mutation_count",
    "prior_receipt_mutation_count",
    "hidden_next_command_count",
    "unbounded_payload_inspection_count",
    "latest_file_guessing_count",
    "mtime_selection_count",
]

HUMAN_DECISION = {
    "decision": "REQUEST_NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE",
    "scope": "Convert the target-narrowing outcome into a precise narrower evidence request. The prior surface found 13 bounded existing hints and correctly withheld a target candidate. This unit asks for evidence sufficient to identify exactly one bounded runtime patch target, without selecting a target, applying a patch, modifying files, opening C5, or widening authority.",
    "authorized": [
        "consume target-narrowing surface receipt",
        "consume target hint scan",
        "summarize ambiguity",
        "emit narrower target evidence request packet",
        "emit target evidence packet schema",
        "emit authority boundary",
        "emit receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "select target candidate",
        "apply runtime patch",
        "modify target files",
        "open C5",
        "grant general Cell1 authority",
        "promote proposal status",
        "fabricate accepted proposal",
        "use latest-file guessing",
        "use mtime selection",
        "inspect unbounded payload",
        "emit hidden next command",
    ],
}

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
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
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def validate_source_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    receipt = read_json(SOURCE_TARGET_NARROWING_RECEIPT_PATH)
    scan = read_json(SOURCE_TARGET_HINT_SCAN_PATH)
    record = read_json(SOURCE_TARGET_CANDIDATE_RECORD_PATH)
    classification = read_json(SOURCE_TARGET_CANDIDATE_CLASSIFICATION_PATH)
    request = read_json(SOURCE_TARGET_CLASSIFICATION_REQUEST_PATH)
    audit = read_json(SOURCE_TARGET_NARROWING_AUTHORITY_AUDIT_PATH)
    rollup = read_json(SOURCE_TARGET_NARROWING_ROLLUP_PATH)
    profile = read_json(SOURCE_TARGET_NARROWING_PROFILE_PATH)
    design_receipt = read_json(SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_PATH)
    contract = read_json(SOURCE_TARGET_CANDIDATE_CONTRACT_PATH)
    precheck_receipt = read_json(SOURCE_PRECHECK_RECEIPT_PATH)
    precheck_classification = read_json(SOURCE_PRECHECK_CLASSIFICATION_PATH)
    precheck_scan = read_json(SOURCE_PRECHECK_TARGET_SCAN_PATH)
    accepted_receipt = read_json(SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH)
    accepted_packet = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    return_receipt = read_json(SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH)
    return_reference = read_json(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH)
    schema_receipt = read_json(SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_PATH)
    schema_reference = read_json(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH)
    c1_receipt = read_json(SOURCE_C1_PATCH_RECEIPT_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)

    if receipt.get("receipt_id") != SOURCE_TARGET_NARROWING_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("target_narrowing_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != "STOP_CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_COMPLETE":
        failures.append("target_narrowing_wrong_terminal")
    if classification.get("candidate_status") != "TARGET_CANDIDATE_WITHHELD_NO_SINGLE_TARGET":
        failures.append("target_candidate_not_withheld")
    if classification.get("target_candidate_declared") is not False:
        failures.append("target_candidate_declared_unexpectedly")
    if classification.get("target_candidate_withheld") is not True:
        failures.append("target_candidate_not_withheld_flag")
    if classification.get("recommended_next") != UNIT_ID:
        failures.append("target_narrowing_recommended_next_not_this_unit")
    if record.get("target_ref") is not None:
        failures.append("withheld_candidate_has_target_ref")
    if request.get("request_kind") != "REQUEST_NARROWER_TARGET_EVIDENCE":
        failures.append("classification_request_kind_wrong")
    if request.get("review_only") is not True:
        failures.append("classification_request_not_review_only")
    if request.get("accepted_for_build") is not False:
        failures.append("classification_request_accepts_for_build")
    if scan.get("hint_count") != 13:
        failures.append(f"hint_count_not_13:{scan.get('hint_count')}")
    if scan.get("bounded_hint_count") != 13:
        failures.append(f"bounded_hint_count_not_13:{scan.get('bounded_hint_count')}")
    if scan.get("existing_bounded_hint_count") != 13:
        failures.append(f"existing_bounded_hint_count_not_13:{scan.get('existing_bounded_hint_count')}")
    if scan.get("latest_file_guessing_count") != 0:
        failures.append("scan_used_latest_file_guessing")
    if scan.get("mtime_selection_count") != 0:
        failures.append("scan_used_mtime_selection")
    if scan.get("unbounded_payload_inspection_count") != 0:
        failures.append("scan_used_unbounded_payload_inspection")
    if audit.get("audit_status") != "PASS":
        failures.append("target_narrowing_audit_not_pass")
    for key in [
        "runtime_patch_applied_count",
        "target_file_modified_count",
        "c5_opened_count",
        "general_cell1_authority_granted_count",
        "proposal_status_promoted_count",
        "accepted_proposal_fabricated_count",
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
        "unbounded_payload_inspection_count",
    ]:
        if rollup.get(key) != 0:
            failures.append(f"target_narrowing_rollup_counter_nonzero:{key}:{rollup.get(key)}")
    if profile.get("status") != "CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_COMPLETE":
        failures.append("target_narrowing_profile_not_complete")
    if design_receipt.get("receipt_id") != SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_ID or design_receipt.get("gate") != "PASS":
        failures.append("target_narrowing_design_receipt_not_pass")
    if contract.get("candidate_object_type") != "BOUNDED_RUNTIME_PATCH_TARGET_CANDIDATE":
        failures.append("target_candidate_contract_wrong")
    if precheck_receipt.get("receipt_id") != SOURCE_PRECHECK_RECEIPT_ID or precheck_receipt.get("gate") != "PASS":
        failures.append("precheck_receipt_not_pass")
    if precheck_classification.get("eligibility_outcome") != "BLOCKED_MISSING_BOUNDED_TARGET":
        failures.append("precheck_not_missing_target")
    if precheck_scan.get("bounded_candidate_count") != 0:
        failures.append("precheck_scan_not_zero_candidates")
    if accepted_receipt.get("receipt_id") != SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID or accepted_receipt.get("gate") != "PASS":
        failures.append("accepted_proposal_receipt_not_pass")
    if accepted_packet.get("status") != "ACCEPTED_FOR_BUILD":
        failures.append("accepted_packet_not_accepted_for_build")
    if return_receipt.get("receipt_id") != SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID or return_receipt.get("gate") != "PASS":
        failures.append("handoff_return_receipt_not_pass")
    if return_reference.get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("handoff_return_reference_not_frozen")
    if schema_receipt.get("receipt_id") != SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID or schema_receipt.get("gate") != "PASS":
        failures.append("schema_close_receipt_not_pass")
    if schema_reference.get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("schema_reference_not_frozen")
    if c1_receipt.get("receipt_id") != SOURCE_C1_PATCH_RECEIPT_ID or c1_receipt.get("gate") != "PASS":
        failures.append("c1_patch_receipt_not_pass")
    if c2_receipt.get("receipt_id") != SOURCE_C2_RECEIPT_ID or c2_receipt.get("gate") != "PASS":
        failures.append("c2_receipt_not_pass")
    return failures

def source_surface() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_evidence_request_source_surface_v0",
        "source_target_narrowing_receipt_id": SOURCE_TARGET_NARROWING_RECEIPT_ID,
        "source_target_narrowing_receipt_ref": rel(SOURCE_TARGET_NARROWING_RECEIPT_PATH),
        "source_target_hint_scan_ref": rel(SOURCE_TARGET_HINT_SCAN_PATH),
        "source_target_candidate_classification_ref": rel(SOURCE_TARGET_CANDIDATE_CLASSIFICATION_PATH),
        "source_accepted_proposal_packet_ref": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "surface_status": "EXPLICIT_NARROWER_TARGET_EVIDENCE_REQUEST_SURFACE",
    }

def target_ambiguity_readout() -> Dict[str, Any]:
    scan = read_json(SOURCE_TARGET_HINT_SCAN_PATH)
    classification = read_json(SOURCE_TARGET_CANDIDATE_CLASSIFICATION_PATH)
    return {
        "schema_version": "cell1_runtime_patch_target_ambiguity_readout_v0",
        "source_target_narrowing_receipt_id": SOURCE_TARGET_NARROWING_RECEIPT_ID,
        "candidate_status": classification.get("candidate_status"),
        "ambiguity_class": "TOO_MANY_BOUNDED_EXISTING_TARGET_HINTS",
        "hint_count": scan.get("hint_count"),
        "bounded_hint_count": scan.get("bounded_hint_count"),
        "existing_bounded_hint_count": scan.get("existing_bounded_hint_count"),
        "target_ref": None,
        "narrower_evidence_required": True,
        "what_is_known": [
            "target-narrowing surface executed",
            "target candidate was withheld",
            "13 bounded existing hints were observed",
            "no latest-file guessing was used",
            "no mtime selection was used",
            "no target file was modified",
        ],
        "what_is_missing": [
            "one explicit chosen target_ref",
            "reason why this target is load-bearing",
            "source evidence linking chosen target to accepted proposal",
            "verification gate for that exact target",
            "rollback-or-stop boundary for that exact target",
            "confirmation that all other hints are non-target context",
        ],
    }

def target_hint_inventory() -> Dict[str, Any]:
    scan = read_json(SOURCE_TARGET_HINT_SCAN_PATH)
    hints = scan.get("hints", [])
    rows = []
    for i, h in enumerate(hints):
        rows.append({
            "hint_index": i,
            "source": h.get("source"),
            "json_path": h.get("json_path"),
            "hint_ref": h.get("hint_ref"),
            "exists_now": h.get("exists_now"),
            "bounded": h.get("bounded"),
            "reason": h.get("reason"),
            "classification": "AMBIGUOUS_HINT_NOT_TARGET_SELECTION",
        })
    return {
        "schema_version": "cell1_runtime_patch_target_hint_inventory_v0",
        "source_scan_ref": rel(SOURCE_TARGET_HINT_SCAN_PATH),
        "hint_count": len(rows),
        "bounded_hint_count": sum(1 for row in rows if row["bounded"] is True),
        "existing_bounded_hint_count": sum(1 for row in rows if row["bounded"] is True and row["exists_now"] is True),
        "target_selected": False,
        "rows": rows,
    }

def evidence_packet_schema() -> Dict[str, Any]:
    return {
        "schema_version": "runtime_patch_target_evidence_packet_schema_v0",
        "packet_object_type": "NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET",
        "required_fields": [
            "evidence_packet_id",
            "selected_target_ref",
            "selected_target_kind",
            "why_this_target_is_load_bearing",
            "why_other_hints_are_not_targets",
            "source_evidence_refs",
            "accepted_proposal_ref",
            "verification_gate_ref",
            "rollback_or_stop_boundary_ref",
            "allowed_write_scope",
            "authority_boundary",
            "review_request",
        ],
        "constraints": [
            "selected_target_ref must be exactly one local bounded path",
            "selected_target_ref must not be selected by latest-file guessing",
            "selected_target_ref must not be selected by mtime ordering",
            "source_evidence_refs must include at least one explicit source artifact",
            "allowed_write_scope must remain NONE until separately authorized",
            "review_request must be review-only",
            "packet must not authorize runtime patch application",
            "packet must not authorize target file modification",
            "packet must not open C5",
        ],
        "allowed_packet_outcomes": [
            "TARGET_EVIDENCE_PACKET_READY_FOR_REVIEW",
            "TARGET_EVIDENCE_PACKET_INSUFFICIENT",
            "TARGET_EVIDENCE_PACKET_REJECTED_AUTHORITY_LEAK",
            "REQUEST_NARROWER_EVIDENCE"
        ],
        "authority_boundary": {
            "may_name_one_candidate_target_for_review": True,
            "may_apply_runtime_patch": False,
            "may_modify_target_files": False,
            "may_open_c5": False,
            "may_grant_general_cell1_authority": False,
            "may_use_latest_file_guessing": False,
            "may_use_mtime_selection": False,
            "may_promote_proposal_status": False,
            "may_fabricate_accepted_proposal": False,
        },
    }

def evidence_request_packet(inventory: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "narrower_runtime_patch_target_evidence_request_packet_v0",
        "request_id": "target_evidence_request_" + sha8({"source": SOURCE_TARGET_NARROWING_RECEIPT_ID, "hint_count": inventory["hint_count"]}),
        "request_kind": "REQUEST_NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE",
        "source_target_narrowing_receipt_id": SOURCE_TARGET_NARROWING_RECEIPT_ID,
        "source_target_narrowing_classification": "TARGET_CANDIDATE_WITHHELD_NO_SINGLE_TARGET",
        "source_hint_inventory_ref": rel(TARGET_HINT_INVENTORY_PATH),
        "evidence_packet_schema_ref": rel(TARGET_EVIDENCE_PACKET_SCHEMA_PATH),
        "ambiguity_class": "TOO_MANY_BOUNDED_EXISTING_TARGET_HINTS",
        "hint_count": inventory["hint_count"],
        "bounded_hint_count": inventory["bounded_hint_count"],
        "existing_bounded_hint_count": inventory["existing_bounded_hint_count"],
        "requested_decision": "Provide or review one explicit bounded runtime patch target evidence packet, or confirm that no single target can yet be selected.",
        "required_evidence": schema["required_fields"],
        "must_answer": [
            "Which single target_ref is being proposed?",
            "Why is that target_ref the load-bearing patch target?",
            "Which source artifacts prove it?",
            "Why are the other observed hints not the target?",
            "What verification gate checks this exact target?",
            "What rollback-or-stop boundary applies to this exact target?",
        ],
        "review_only": True,
        "accepted_for_build": False,
        "target_candidate_declared": False,
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "next_command_goal": None,
    }

def authority_boundary() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_evidence_request_authority_boundary_v0",
        "authority_boundary_id": "target_evidence_request_authority_" + sha8({"source": SOURCE_TARGET_NARROWING_RECEIPT_ID}),
        "may_emit_request_packet": True,
        "may_emit_evidence_packet_schema": True,
        "may_select_target": False,
        "may_declare_target_candidate": False,
        "may_apply_runtime_patch": False,
        "may_modify_target_files": False,
        "may_open_c5": False,
        "may_grant_general_cell1_authority": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "may_promote_proposal_status": False,
        "may_fabricate_accepted_proposal": False,
        "must_not_infer": [
            "request packet selects a target",
            "evidence request authorizes patching",
            "evidence request authorizes target writes",
            "13 hints can be collapsed by preference",
            "latest file may be chosen",
            "mtime may be used as tie-breaker",
        ],
    }

def rollup(inventory: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_evidence_request_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_target_narrowing_receipt_id": SOURCE_TARGET_NARROWING_RECEIPT_ID,
        "source_target_narrowing_design_receipt_id": SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_ID,
        "source_precheck_receipt_id": SOURCE_PRECHECK_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "hint_count": inventory["hint_count"],
        "bounded_hint_count": inventory["bounded_hint_count"],
        "existing_bounded_hint_count": inventory["existing_bounded_hint_count"],
        "target_evidence_request_packet_emitted_count": 1,
        "target_evidence_packet_schema_emitted_count": 1,
        "target_selected_count": 0,
        "target_candidate_declared_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "proposal_status_promoted_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "unbounded_payload_inspection_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": RECOMMENDED_NEXT,
    }

def profile(rollup_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_evidence_request_profile_v0",
        "profile_id": "target_evidence_request_" + sha8({"source": SOURCE_TARGET_NARROWING_RECEIPT_ID}),
        "status": "NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_REQUESTED",
        "ambiguity_class": "TOO_MANY_BOUNDED_EXISTING_TARGET_HINTS",
        "hint_count": rollup_obj["hint_count"],
        "target_selected": False,
        "target_candidate_declared": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "recommended_next": rollup_obj["recommended_next"],
        "next_command_goal": None,
    }

def report(rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_evidence_request_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_target_narrowing_receipt_consumed_count": 1,
        "target_ambiguity_readout_emitted_count": 1,
        "target_hint_inventory_emitted_count": 1,
        "target_evidence_request_packet_emitted_count": rollup_obj["target_evidence_request_packet_emitted_count"],
        "target_evidence_packet_schema_emitted_count": rollup_obj["target_evidence_packet_schema_emitted_count"],
        "profile_status": profile_obj["status"],
        "recommended_next_handling": rollup_obj["recommended_next"],
        "target_selected_count": 0,
        "target_candidate_declared_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "proposal_status_promoted_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
    }

def transition_trace() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_evidence_request_transition_trace_v0",
        "trace": [
            {
                "step": "consume_target_narrowing_surface",
                "question": "why was no target candidate declared",
                "answer": "13 bounded existing hints, no single honest target",
                "taken": "emit_narrower_evidence_request",
            },
            {
                "step": "emit_narrower_evidence_request",
                "question": "what exact evidence is needed before target declaration",
                "answer": rel(NARROWER_EVIDENCE_REQUEST_PACKET_PATH),
                "taken": "stop",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_REQUESTED",
            "next_command_goal": None,
        },
    }

def validate_outputs(inventory: Dict[str, Any], schema: Dict[str, Any], request: Dict[str, Any], boundary: Dict[str, Any], rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any], report_obj: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if inventory.get("hint_count") != 13:
        failures.append("inventory_hint_count_not_13")
    if inventory.get("target_selected") is not False:
        failures.append("inventory_claims_target_selected")
    if schema.get("packet_object_type") != "NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET":
        failures.append("schema_wrong_packet_object_type")
    for key in ["may_apply_runtime_patch", "may_modify_target_files", "may_open_c5", "may_grant_general_cell1_authority", "may_use_latest_file_guessing", "may_use_mtime_selection"]:
        if schema.get("authority_boundary", {}).get(key) is not False:
            failures.append(f"schema_authority_not_false:{key}")
    if request.get("request_kind") != "REQUEST_NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE":
        failures.append("request_kind_wrong")
    if request.get("review_only") is not True:
        failures.append("request_not_review_only")
    if request.get("accepted_for_build") is not False:
        failures.append("request_accepts_for_build")
    if request.get("target_candidate_declared") is not False:
        failures.append("request_declares_target_candidate")
    if request.get("runtime_patch_authorized") is not False:
        failures.append("request_authorizes_runtime_patch")
    if request.get("target_file_modification_authorized") is not False:
        failures.append("request_authorizes_target_modification")
    if request.get("c5_authorized") is not False:
        failures.append("request_authorizes_c5")
    if request.get("next_command_goal") is not None:
        failures.append("request_hidden_next_command")
    for key in ["may_select_target", "may_declare_target_candidate", "may_apply_runtime_patch", "may_modify_target_files", "may_open_c5", "may_grant_general_cell1_authority", "may_use_latest_file_guessing", "may_use_mtime_selection"]:
        if boundary.get(key) is not False:
            failures.append(f"boundary_authority_not_false:{key}")
    for key in ZERO_COUNTER_KEYS:
        if rollup_obj.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup_obj.get(key)}")
    if rollup_obj.get("target_evidence_request_packet_emitted_count") != 1:
        failures.append("request_packet_count_not_one")
    if rollup_obj.get("target_evidence_packet_schema_emitted_count") != 1:
        failures.append("schema_count_not_one")
    if profile_obj.get("target_selected") is not False:
        failures.append("profile_claims_target_selected")
    if profile_obj.get("target_candidate_declared") is not False:
        failures.append("profile_claims_target_candidate_declared")
    if profile_obj.get("runtime_patch_applied") is not False:
        failures.append("profile_claims_runtime_patch")
    if profile_obj.get("target_file_modified") is not False:
        failures.append("profile_claims_target_file_modified")
    if profile_obj.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")
    for key in [
        "target_selected_count",
        "target_candidate_declared_count",
        "runtime_patch_applied_count",
        "target_file_modified_count",
        "c5_opened_count",
        "general_cell1_authority_granted_count",
        "taxonomy_registry_mutation_count",
        "proposal_status_promoted_count",
        "accepted_proposal_fabricated_count",
        "hidden_next_command_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
    ]:
        if report_obj.get(key) != 0:
            failures.append(f"report_counter_nonzero:{key}:{report_obj.get(key)}")
    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    for gate, ok in receipt.get("acceptance_gate_results", {}).items():
        if ok is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{ok}")
    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_REQUESTED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    inventory = read_json(TARGET_HINT_INVENTORY_PATH)
    schema = read_json(TARGET_EVIDENCE_PACKET_SCHEMA_PATH)
    request = read_json(NARROWER_EVIDENCE_REQUEST_PACKET_PATH)
    boundary = read_json(AUTHORITY_BOUNDARY_PATH)
    rollup_obj = read_json(ROLLUP_PATH)
    profile_obj = read_json(PROFILE_PATH)
    report_obj = read_json(REPORT_PATH)

    controls: List[Dict[str, Any]] = []

    def add(case: str, failures: List[str], expected_fragment: str) -> None:
        controls.append({
            "case": case,
            "negative_control_pass": any(expected_fragment in f for f in failures),
            "failures": failures,
            "wrote_live_artifact": False,
        })

    bad_inventory = copy.deepcopy(inventory)
    bad_inventory["target_selected"] = True
    add("inventory_claims_target_selected_fail", validate_outputs(bad_inventory, schema, request, boundary, rollup_obj, profile_obj, report_obj), "inventory_claims_target_selected")

    bad_schema = copy.deepcopy(schema)
    bad_schema["authority_boundary"]["may_apply_runtime_patch"] = True
    add("schema_authority_allows_runtime_patch_fail", validate_outputs(inventory, bad_schema, request, boundary, rollup_obj, profile_obj, report_obj), "schema_authority_not_false:may_apply_runtime_patch")

    bad_schema = copy.deepcopy(schema)
    bad_schema["authority_boundary"]["may_use_latest_file_guessing"] = True
    add("schema_authority_allows_latest_file_guessing_fail", validate_outputs(inventory, bad_schema, request, boundary, rollup_obj, profile_obj, report_obj), "schema_authority_not_false:may_use_latest_file_guessing")

    bad_request = copy.deepcopy(request)
    bad_request["accepted_for_build"] = True
    add("request_accepts_for_build_fail", validate_outputs(inventory, schema, bad_request, boundary, rollup_obj, profile_obj, report_obj), "request_accepts_for_build")

    bad_request = copy.deepcopy(request)
    bad_request["target_candidate_declared"] = True
    add("request_declares_target_candidate_fail", validate_outputs(inventory, schema, bad_request, boundary, rollup_obj, profile_obj, report_obj), "request_declares_target_candidate")

    bad_request = copy.deepcopy(request)
    bad_request["runtime_patch_authorized"] = True
    add("request_authorizes_runtime_patch_fail", validate_outputs(inventory, schema, bad_request, boundary, rollup_obj, profile_obj, report_obj), "request_authorizes_runtime_patch")

    bad_request = copy.deepcopy(request)
    bad_request["target_file_modification_authorized"] = True
    add("request_authorizes_target_modification_fail", validate_outputs(inventory, schema, bad_request, boundary, rollup_obj, profile_obj, report_obj), "request_authorizes_target_modification")

    bad_request = copy.deepcopy(request)
    bad_request["next_command_goal"] = "SELECT_TARGET"
    add("request_hidden_next_command_fail", validate_outputs(inventory, schema, bad_request, boundary, rollup_obj, profile_obj, report_obj), "request_hidden_next_command")

    for case, key, expected in [
        ("boundary_allows_target_selection_fail", "may_select_target", "boundary_authority_not_false:may_select_target"),
        ("boundary_allows_candidate_declaration_fail", "may_declare_target_candidate", "boundary_authority_not_false:may_declare_target_candidate"),
        ("boundary_allows_runtime_patch_fail", "may_apply_runtime_patch", "boundary_authority_not_false:may_apply_runtime_patch"),
        ("boundary_allows_target_file_modification_fail", "may_modify_target_files", "boundary_authority_not_false:may_modify_target_files"),
        ("boundary_allows_c5_fail", "may_open_c5", "boundary_authority_not_false:may_open_c5"),
        ("boundary_allows_latest_file_guessing_fail", "may_use_latest_file_guessing", "boundary_authority_not_false:may_use_latest_file_guessing"),
        ("boundary_allows_mtime_selection_fail", "may_use_mtime_selection", "boundary_authority_not_false:may_use_mtime_selection"),
    ]:
        bad_boundary = copy.deepcopy(boundary)
        bad_boundary[key] = True
        add(case, validate_outputs(inventory, schema, request, bad_boundary, rollup_obj, profile_obj, report_obj), expected)

    for case, counter in [
        ("target_selected_fail", "target_selected_count"),
        ("target_candidate_declared_fail", "target_candidate_declared_count"),
        ("runtime_patch_applied_fail", "runtime_patch_applied_count"),
        ("target_file_modified_fail", "target_file_modified_count"),
        ("c5_opened_fail", "c5_opened_count"),
        ("general_cell1_authority_granted_fail", "general_cell1_authority_granted_count"),
        ("taxonomy_registry_mutated_fail", "taxonomy_registry_mutation_count"),
        ("proposal_status_promoted_fail", "proposal_status_promoted_count"),
        ("accepted_proposal_fabricated_fail", "accepted_proposal_fabricated_count"),
        ("source_mutation_fail", "source_mutation_count"),
        ("prior_receipt_mutation_fail", "prior_receipt_mutation_count"),
        ("hidden_next_command_fail", "hidden_next_command_count"),
        ("unbounded_payload_inspection_fail", "unbounded_payload_inspection_count"),
        ("latest_file_guessing_fail", "latest_file_guessing_count"),
        ("mtime_selection_fail", "mtime_selection_count"),
    ]:
        bad_rollup = copy.deepcopy(rollup_obj)
        bad_report = copy.deepcopy(report_obj)
        bad_rollup[counter] = 1
        if counter in bad_report:
            bad_report[counter] = 1
        add(case, validate_outputs(inventory, schema, request, boundary, bad_rollup, profile_obj, bad_report), counter)

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_REQUEST_EVIDENCE_REQUEST_REQUIRED", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "cell1_runtime_patch_target_evidence_request_receipt_v0",
            "receipt_type": "CELL1_RUNTIME_PATCH_TARGET_EVIDENCE_REQUEST_RECEIPT",
            "receipt_id": receipt_id,
            "unit_id": UNIT_ID,
            "target_unit_id": TARGET_UNIT_ID,
            "gate": "FAIL",
            "failures": failures,
            "terminal": terminal,
            "created_at": now_iso(),
        }
        write_json(receipt_path, receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        print(f"target_evidence_request_receipt_id={receipt_id}")
        print(f"target_evidence_request_receipt_path=data/cell1_runtime_patch_target_evidence_request_v0_receipts/{receipt_id}.json")
        return 1

    readout = target_ambiguity_readout()
    inventory = target_hint_inventory()
    schema = evidence_packet_schema()
    request = evidence_request_packet(inventory, schema)
    boundary = authority_boundary()
    rollup_obj = rollup(inventory)
    profile_obj = profile(rollup_obj)
    report_obj = report(rollup_obj, profile_obj)
    trace = transition_trace()

    write_json(SOURCE_SURFACE_PATH, source_surface())
    write_json(TARGET_AMBIGUITY_READOUT_PATH, readout)
    write_json(TARGET_HINT_INVENTORY_PATH, inventory)
    write_json(TARGET_EVIDENCE_PACKET_SCHEMA_PATH, schema)
    write_json(NARROWER_EVIDENCE_REQUEST_PACKET_PATH, request)
    write_json(AUTHORITY_BOUNDARY_PATH, boundary)
    write_json(ROLLUP_PATH, rollup_obj)
    write_json(PROFILE_PATH, profile_obj)
    write_json(REPORT_PATH, report_obj)
    write_json(TRANSITION_TRACE_PATH, trace)

    failures.extend(validate_outputs(inventory, schema, request, boundary, rollup_obj, profile_obj, report_obj))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup_obj["source_mutation_count"] = 1
        report_obj["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup_obj)
        write_json(REPORT_PATH, report_obj)

    acceptance_gate_results = {
        "TARGET_EVIDENCE_REQUEST_0_TARGET_NARROWING_RECEIPT_CONSUMED": SOURCE_TARGET_NARROWING_RECEIPT_PATH.exists(),
        "TARGET_EVIDENCE_REQUEST_1_WITHHELD_STATUS_CONFIRMED": readout["narrower_evidence_required"] is True,
        "TARGET_EVIDENCE_REQUEST_2_AMBIGUITY_READOUT_EMITTED": TARGET_AMBIGUITY_READOUT_PATH.exists(),
        "TARGET_EVIDENCE_REQUEST_3_HINT_INVENTORY_EMITTED": TARGET_HINT_INVENTORY_PATH.exists(),
        "TARGET_EVIDENCE_REQUEST_4_EVIDENCE_PACKET_SCHEMA_EMITTED": TARGET_EVIDENCE_PACKET_SCHEMA_PATH.exists(),
        "TARGET_EVIDENCE_REQUEST_5_REQUEST_PACKET_EMITTED": NARROWER_EVIDENCE_REQUEST_PACKET_PATH.exists(),
        "TARGET_EVIDENCE_REQUEST_6_AUTHORITY_BOUNDARY_EMITTED": AUTHORITY_BOUNDARY_PATH.exists(),
        "TARGET_EVIDENCE_REQUEST_7_NO_TARGET_SELECTED": rollup_obj["target_selected_count"] == 0,
        "TARGET_EVIDENCE_REQUEST_8_NO_TARGET_CANDIDATE_DECLARED": rollup_obj["target_candidate_declared_count"] == 0,
        "TARGET_EVIDENCE_REQUEST_9_NO_RUNTIME_PATCH": rollup_obj["runtime_patch_applied_count"] == 0,
        "TARGET_EVIDENCE_REQUEST_10_NO_TARGET_FILE_MODIFICATION": rollup_obj["target_file_modified_count"] == 0,
        "TARGET_EVIDENCE_REQUEST_11_NO_C5_OPENED": rollup_obj["c5_opened_count"] == 0,
        "TARGET_EVIDENCE_REQUEST_12_NO_GENERAL_CELL1_AUTHORITY": rollup_obj["general_cell1_authority_granted_count"] == 0,
        "TARGET_EVIDENCE_REQUEST_13_NO_LATEST_FILE_GUESSING": rollup_obj["latest_file_guessing_count"] == 0,
        "TARGET_EVIDENCE_REQUEST_14_NO_MTIME_SELECTION": rollup_obj["mtime_selection_count"] == 0,
        "TARGET_EVIDENCE_REQUEST_15_NO_UNBOUNDED_PAYLOAD_INSPECTION": rollup_obj["unbounded_payload_inspection_count"] == 0,
        "TARGET_EVIDENCE_REQUEST_16_NO_HIDDEN_NEXT_COMMAND": rollup_obj["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
        "TARGET_EVIDENCE_REQUEST_17_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    for gate_name, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate_name}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_target_narrowing": SOURCE_TARGET_NARROWING_RECEIPT_ID,
        "hint_count": inventory["hint_count"],
        "recommended_next": RECOMMENDED_NEXT,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "target_ambiguity_readout": rel(TARGET_AMBIGUITY_READOUT_PATH),
        "target_hint_inventory": rel(TARGET_HINT_INVENTORY_PATH),
        "narrower_evidence_request_packet": rel(NARROWER_EVIDENCE_REQUEST_PACKET_PATH),
        "target_evidence_packet_schema": rel(TARGET_EVIDENCE_PACKET_SCHEMA_PATH),
        "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
        "rollup": rel(ROLLUP_PATH),
        "profile": rel(PROFILE_PATH),
        "report": rel(REPORT_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_target_narrowing_receipt": rel(SOURCE_TARGET_NARROWING_RECEIPT_PATH),
        "source_target_hint_scan": rel(SOURCE_TARGET_HINT_SCAN_PATH),
        "source_target_candidate_classification": rel(SOURCE_TARGET_CANDIDATE_CLASSIFICATION_PATH),
        "source_accepted_proposal_packet": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
    }

    guards = {
        "build_mode_narrower_target_evidence_request_only": BUILD_MODE == "NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_REQUEST_ONLY",
        "ambiguity_class": "TOO_MANY_BOUNDED_EXISTING_TARGET_HINTS",
        "hint_count": inventory["hint_count"],
        "target_selected": False,
        "target_candidate_declared": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "unbounded_payload_inspection": False,
        "hidden_next_command": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
    }

    receipt = {
        "schema_version": "cell1_runtime_patch_target_evidence_request_receipt_v0",
        "receipt_type": "CELL1_RUNTIME_PATCH_TARGET_EVIDENCE_REQUEST_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "narrower runtime patch target evidence request",
        "source_target_narrowing_receipt_id": SOURCE_TARGET_NARROWING_RECEIPT_ID,
        "source_target_narrowing_design_receipt_id": SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_ID,
        "source_precheck_receipt_id": SOURCE_PRECHECK_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_handoff_return_close_receipt_id": SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID,
        "source_schema_close_receipt_id": SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "target_evidence_request_summary": {
            "profile_status": profile_obj["status"],
            "ambiguity_class": profile_obj["ambiguity_class"],
            "hint_count": rollup_obj["hint_count"],
            "bounded_hint_count": rollup_obj["bounded_hint_count"],
            "existing_bounded_hint_count": rollup_obj["existing_bounded_hint_count"],
            "target_selected": False,
            "target_candidate_declared": False,
            "request_packet_emitted": True,
            "evidence_packet_schema_emitted": True,
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "general_cell1_authority_granted": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": profile_obj["bad_counters_zero"],
            "recommended_next": rollup_obj["recommended_next"],
        },
        "aggregate_metrics": {
            **{k: v for k, v in report_obj.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
            "rollup": rollup_obj,
            "source_mutation_count": 1 if source_mutation_detected else report_obj["source_mutation_count"],
        },
        "acceptance_gate_results": acceptance_gate_results,
        "target_evidence_request_guards": guards,
        "terminal": terminal,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_failures = validate_receipt(receipt)
    failures.extend(receipt_failures)
    receipt["failures"] = failures
    receipt["gate"] = "PASS" if not failures else "FAIL"
    if failures:
        receipt["terminal"] = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}

    write_json(receipt_path, receipt)

    negative_controls = run_negative_controls(receipt_path)
    if len(negative_controls) != 30 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
        receipt = read_json(receipt_path)
        receipt["gate"] = "FAIL"
        receipt["failures"].append("negative_controls_failed")
        receipt["negative_controls"] = negative_controls
        receipt["terminal"] = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}
        write_json(receipt_path, receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 1

    receipt = read_json(receipt_path)
    receipt["negative_controls"] = negative_controls
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"target_evidence_request_receipt_id={receipt_id}")
    print(f"target_evidence_request_receipt_path=data/cell1_runtime_patch_target_evidence_request_v0_receipts/{receipt_id}.json")
    print(f"target_evidence_request_packet_path=data/cell1_runtime_patch_target_evidence_request_v0/narrower_runtime_patch_target_evidence_request_packet_v0.json")
    print(f"target_evidence_packet_schema_path=data/cell1_runtime_patch_target_evidence_request_v0/runtime_patch_target_evidence_packet_schema_v0.json")
    print(f"target_hint_inventory_path=data/cell1_runtime_patch_target_evidence_request_v0/target_hint_inventory_v0.json")
    print(f"target_evidence_request_rollup_path=data/cell1_runtime_patch_target_evidence_request_v0/target_evidence_request_rollup_v0.json")
    print(f"target_evidence_request_profile_path=data/cell1_runtime_patch_target_evidence_request_v0/target_evidence_request_profile_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
