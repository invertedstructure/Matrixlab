#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DESIGN_CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_narrowing_surface.design.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_NARROWING_SURFACE_DESIGN"
MODE = "DESIGN / TARGET_NARROWING_SURFACE / NO_PATCH"
BUILD_MODE = "RUNTIME_PATCH_TARGET_NARROWING_SURFACE_DESIGN_ONLY"

SOURCE_PRECHECK_RECEIPT_ID = "c534ce7c"
SOURCE_PRECHECK_RECEIPT_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_run_v0_receipts" / "c534ce7c.json"
SOURCE_PRECHECK_EVIDENCE_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_run_v0" / "runtime_patch_precheck_eligibility_evidence_v0.json"
SOURCE_PRECHECK_CLASSIFICATION_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_run_v0" / "runtime_patch_precheck_eligibility_classification_v0.json"
SOURCE_PRECHECK_TARGET_SCAN_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_run_v0" / "bounded_runtime_patch_target_candidate_scan_v0.json"
SOURCE_PRECHECK_VERIFICATION_SCAN_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_run_v0" / "verification_gate_scan_v0.json"
SOURCE_PRECHECK_ROLLBACK_SCAN_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_run_v0" / "rollback_or_stop_boundary_scan_v0.json"
SOURCE_PRECHECK_AUTHORITY_AUDIT_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_run_v0" / "runtime_patch_precheck_authority_audit_v0.json"
SOURCE_PRECHECK_ROLLUP_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_run_v0" / "runtime_patch_precheck_rollup_v0.json"
SOURCE_PRECHECK_PROFILE_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_run_v0" / "runtime_patch_precheck_profile_v0.json"

SOURCE_PRECHECK_DESIGN_RECEIPT_ID = "a62d6ec2"
SOURCE_PRECHECK_DESIGN_RECEIPT_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_design_v0_receipts" / "a62d6ec2.json"
SOURCE_PRECHECK_DESIGN_RECORD_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_design_v0" / "runtime_patch_precheck_design_record_v0.json"
SOURCE_PRECHECK_CONTRACT_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_design_v0" / "runtime_patch_precheck_eligibility_contract_v0.json"

SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_ID = "f595a9a6"
SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_PATH = ROOT / "data" / "cell1_next_bounded_objective_after_return_loop_v0_receipts" / "f595a9a6.json"

SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID = "1d7c0a9b"
SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH = ROOT / "data" / "cell1_handoff_return_loop_review_or_close_v0_receipts" / "1d7c0a9b.json"
SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH = ROOT / "data" / "cell1_handoff_return_loop_review_or_close_v0" / "handoff_return_loop_frozen_reference_packet_v0.json"

SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID = "e1bc0ed0"
SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0_receipts" / "e1bc0ed0.json"
SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0" / "cell1_schema_test_frozen_reference_packet_v0.json"

SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID = "71bd1d92"
SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0_receipts" / "71bd1d92.json"
SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0" / "accepted_proposal_packet_v0.json"

SOURCE_C1_PATCH_RECEIPT_ID = "fffa3dd5"
SOURCE_C1_PATCH_RECEIPT_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0_receipts" / "fffa3dd5.json"
SOURCE_C1_PATCH_SCHEMA_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0" / "proposal_packet_schema_v0_1.json"

SOURCE_C2_RECEIPT_ID = "348dabde"
SOURCE_C2_RECEIPT_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts" / "348dabde.json"
SOURCE_C2_LANE_REGISTRY_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "taxonomy_lane_registry_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_PRECHECK_RECEIPT_PATH,
    SOURCE_PRECHECK_EVIDENCE_PATH,
    SOURCE_PRECHECK_CLASSIFICATION_PATH,
    SOURCE_PRECHECK_TARGET_SCAN_PATH,
    SOURCE_PRECHECK_VERIFICATION_SCAN_PATH,
    SOURCE_PRECHECK_ROLLBACK_SCAN_PATH,
    SOURCE_PRECHECK_AUTHORITY_AUDIT_PATH,
    SOURCE_PRECHECK_ROLLUP_PATH,
    SOURCE_PRECHECK_PROFILE_PATH,
    SOURCE_PRECHECK_DESIGN_RECEIPT_PATH,
    SOURCE_PRECHECK_DESIGN_RECORD_PATH,
    SOURCE_PRECHECK_CONTRACT_PATH,
    SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_PATH,
    SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH,
    SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH,
    SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_PATH,
    SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH,
    SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH,
    SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH,
    SOURCE_C1_PATCH_RECEIPT_PATH,
    SOURCE_C1_PATCH_SCHEMA_PATH,
    SOURCE_C2_RECEIPT_PATH,
    SOURCE_C2_LANE_REGISTRY_PATH,
]

OUT_DIR = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_design_v0"
RECEIPT_DIR = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_design_v0_receipts"

SOURCE_SURFACE_PATH = OUT_DIR / "source_surface_v0.json"
PRECHECK_BLOCKER_READOUT_PATH = OUT_DIR / "precheck_blocker_readout_v0.json"
TARGET_NARROWING_DESIGN_RECORD_PATH = OUT_DIR / "target_narrowing_surface_design_record_v0.json"
TARGET_CANDIDATE_CONTRACT_PATH = OUT_DIR / "bounded_target_candidate_contract_v0.json"
TARGET_NARROWING_TEST_PLAN_PATH = OUT_DIR / "target_narrowing_surface_test_plan_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "target_narrowing_surface_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "target_narrowing_surface_design_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "target_narrowing_surface_design_profile_v0.json"
REPORT_PATH = OUT_DIR / "target_narrowing_surface_design_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "target_narrowing_surface_design_transition_trace.json"

FUTURE_TARGET_NARROWING_UNIT = "RUN_CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_FROM_DESIGN_V0"

ZERO_COUNTER_KEYS = [
    "target_narrowing_executed_count",
    "runtime_patch_applied_count",
    "target_file_modified_count",
    "c5_opened_count",
    "general_cell1_authority_granted_count",
    "taxonomy_registry_mutation_count",
    "proposal_status_promoted_count",
    "accepted_proposal_fabricated_count",
    "source_mutation_count",
    "prior_receipt_mutation_count",
    "hidden_next_command_count",
    "unbounded_payload_inspection_count",
]

HUMAN_DECISION = {
    "decision": "DESIGN_CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE",
    "scope": "Design the bounded target-narrowing surface forced by the runtime patch eligibility precheck blocker. The surface asks for exactly one bounded runtime patch target candidate and defines how that candidate may be declared, validated, rejected, or withheld. This unit emits design artifacts only. It does not run the target-narrowing surface, does not apply a runtime patch, does not modify target files, does not open C5, and does not grant general Cell1 authority.",
    "authorized": [
        "consume runtime patch precheck receipt",
        "consume precheck blocker classification",
        "consume bounded target scan",
        "design one target-narrowing surface",
        "emit bounded target candidate contract",
        "emit future target-narrowing test plan",
        "emit authority boundary",
        "emit receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "run target-narrowing surface now",
        "apply runtime patch",
        "modify target files",
        "open C5",
        "grant general Cell1 authority",
        "promote proposal status",
        "fabricate accepted proposal",
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

    precheck_receipt = read_json(SOURCE_PRECHECK_RECEIPT_PATH)
    evidence = read_json(SOURCE_PRECHECK_EVIDENCE_PATH)
    classification = read_json(SOURCE_PRECHECK_CLASSIFICATION_PATH)
    target_scan = read_json(SOURCE_PRECHECK_TARGET_SCAN_PATH)
    verification_scan = read_json(SOURCE_PRECHECK_VERIFICATION_SCAN_PATH)
    rollback_scan = read_json(SOURCE_PRECHECK_ROLLBACK_SCAN_PATH)
    audit = read_json(SOURCE_PRECHECK_AUTHORITY_AUDIT_PATH)
    rollup = read_json(SOURCE_PRECHECK_ROLLUP_PATH)
    profile = read_json(SOURCE_PRECHECK_PROFILE_PATH)
    design_receipt = read_json(SOURCE_PRECHECK_DESIGN_RECEIPT_PATH)
    design = read_json(SOURCE_PRECHECK_DESIGN_RECORD_PATH)
    contract = read_json(SOURCE_PRECHECK_CONTRACT_PATH)
    after_return = read_json(SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_PATH)
    return_receipt = read_json(SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH)
    return_reference = read_json(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH)
    schema_receipt = read_json(SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_PATH)
    schema_reference = read_json(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH)
    accepted_receipt = read_json(SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH)
    accepted_packet = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    c1_receipt = read_json(SOURCE_C1_PATCH_RECEIPT_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)

    if precheck_receipt.get("receipt_id") != SOURCE_PRECHECK_RECEIPT_ID or precheck_receipt.get("gate") != "PASS":
        failures.append("precheck_receipt_not_pass")
    if precheck_receipt.get("terminal", {}).get("stop_code") != "STOP_CELL1_MINIMAL_RUNTIME_PATCH_PRECHECK_COMPLETE":
        failures.append("precheck_wrong_terminal")
    if classification.get("eligibility_outcome") != "BLOCKED_MISSING_BOUNDED_TARGET":
        failures.append("precheck_not_blocked_missing_bounded_target")
    if classification.get("runtime_patch_authorized") is not False:
        failures.append("precheck_classification_authorizes_runtime_patch")
    if classification.get("target_file_modification_authorized") is not False:
        failures.append("precheck_classification_authorizes_target_modification")
    if classification.get("c5_authorized") is not False:
        failures.append("precheck_classification_authorizes_c5")
    if target_scan.get("bounded_candidate_count") != 0:
        failures.append("target_scan_not_zero_bounded_candidates")
    if target_scan.get("exactly_one_bounded_target") is not False:
        failures.append("target_scan_claims_exactly_one_target")
    if evidence.get("accepted_proposal", {}).get("accepted_for_build") is not True:
        failures.append("accepted_proposal_not_present_in_evidence")
    if evidence.get("return_packet_or_review_surface", {}).get("available") is not True:
        failures.append("return_review_surface_not_available")
    if verification_scan.get("verification_gate_declared") is not True:
        failures.append("verification_gate_missing")
    if rollback_scan.get("rollback_or_stop_boundary_declared") is not True:
        failures.append("rollback_or_stop_boundary_missing")
    if audit.get("audit_status") != "PASS":
        failures.append("precheck_authority_audit_not_pass")
    for key in [
        "runtime_patch_applied_count",
        "target_file_modified_count",
        "c5_opened_count",
        "general_cell1_authority_granted_count",
        "proposal_status_promoted_count",
        "accepted_proposal_fabricated_count",
        "unbounded_payload_inspection_count",
        "hidden_next_command_count",
    ]:
        if rollup.get(key) != 0:
            failures.append(f"precheck_rollup_counter_nonzero:{key}:{rollup.get(key)}")
    if profile.get("status") != "CELL1_MINIMAL_RUNTIME_PATCH_PRECHECK_COMPLETE":
        failures.append("precheck_profile_not_complete")
    if profile.get("recommended_next") != UNIT_ID:
        failures.append("precheck_recommended_next_not_this_unit")
    if design_receipt.get("receipt_id") != SOURCE_PRECHECK_DESIGN_RECEIPT_ID or design_receipt.get("gate") != "PASS":
        failures.append("precheck_design_receipt_not_pass")
    if design.get("future_precheck_unit") != "RUN_CELL1_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK_FROM_DESIGN_V0":
        failures.append("precheck_design_future_unit_wrong")
    if contract.get("authority_boundary", {}).get("may_apply_runtime_patch") is not False:
        failures.append("precheck_contract_allows_runtime_patch")
    if after_return.get("receipt_id") != SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_ID or after_return.get("gate") != "PASS":
        failures.append("after_return_objective_receipt_not_pass")
    if return_receipt.get("receipt_id") != SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID or return_receipt.get("gate") != "PASS":
        failures.append("handoff_return_close_receipt_not_pass")
    if return_reference.get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("handoff_return_reference_not_frozen")
    if schema_receipt.get("receipt_id") != SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID or schema_receipt.get("gate") != "PASS":
        failures.append("schema_close_receipt_not_pass")
    if schema_reference.get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("schema_reference_not_frozen")
    if accepted_receipt.get("receipt_id") != SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID or accepted_receipt.get("gate") != "PASS":
        failures.append("accepted_proposal_receipt_not_pass")
    if accepted_packet.get("status") != "ACCEPTED_FOR_BUILD":
        failures.append("accepted_packet_not_accepted_for_build")
    if c1_receipt.get("receipt_id") != SOURCE_C1_PATCH_RECEIPT_ID or c1_receipt.get("gate") != "PASS":
        failures.append("c1_patch_receipt_not_pass")
    if c2_receipt.get("receipt_id") != SOURCE_C2_RECEIPT_ID or c2_receipt.get("gate") != "PASS":
        failures.append("c2_receipt_not_pass")
    return failures

def source_surface() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_narrowing_surface_design_source_surface_v0",
        "source_precheck_receipt_id": SOURCE_PRECHECK_RECEIPT_ID,
        "source_precheck_receipt_ref": rel(SOURCE_PRECHECK_RECEIPT_PATH),
        "source_precheck_classification_ref": rel(SOURCE_PRECHECK_CLASSIFICATION_PATH),
        "source_precheck_target_scan_ref": rel(SOURCE_PRECHECK_TARGET_SCAN_PATH),
        "source_accepted_proposal_packet_ref": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "source_schema_reference_packet_ref": rel(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH),
        "source_handoff_return_reference_packet_ref": rel(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH),
        "surface_status": "EXPLICIT_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_DESIGN",
    }

def precheck_blocker_readout() -> Dict[str, Any]:
    classification = read_json(SOURCE_PRECHECK_CLASSIFICATION_PATH)
    target_scan = read_json(SOURCE_PRECHECK_TARGET_SCAN_PATH)
    rollup = read_json(SOURCE_PRECHECK_ROLLUP_PATH)
    return {
        "schema_version": "cell1_runtime_patch_target_narrowing_precheck_blocker_readout_v0",
        "source_precheck_receipt_id": SOURCE_PRECHECK_RECEIPT_ID,
        "eligibility_outcome": classification.get("eligibility_outcome"),
        "blocker": "MISSING_BOUNDED_RUNTIME_PATCH_TARGET",
        "accepted_proposal_present_count": rollup.get("accepted_proposal_present_count"),
        "bounded_target_candidate_count": target_scan.get("bounded_candidate_count"),
        "exactly_one_bounded_target": target_scan.get("exactly_one_bounded_target"),
        "verification_gate_declared_count": rollup.get("verification_gate_declared_count"),
        "rollback_or_stop_boundary_declared_count": rollup.get("rollback_or_stop_boundary_declared_count"),
        "return_review_surface_available_count": rollup.get("return_review_surface_available_count"),
        "what_is_known": [
            "accepted proposal exists",
            "verification gate surface exists",
            "rollback-or-stop boundary exists",
            "return/review surface exists",
            "no bounded runtime patch target candidate is declared",
        ],
        "what_is_not_known": [
            "which file or artifact may be patched",
            "whether exactly one target can be named",
            "whether the target is inside the allowed write scope",
            "whether the target has rollback/verification coupling",
        ],
    }

def target_candidate_contract() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_candidate_contract_v0",
        "contract_id": "target_candidate_contract_" + sha8({"source": SOURCE_PRECHECK_RECEIPT_ID}),
        "candidate_object_type": "BOUNDED_RUNTIME_PATCH_TARGET_CANDIDATE",
        "required_fields": [
            "target_candidate_id",
            "target_ref",
            "target_kind",
            "why_this_target",
            "source_evidence_refs",
            "allowed_write_scope",
            "verification_gate_ref",
            "rollback_or_stop_boundary_ref",
            "authority_boundary",
            "negative_boundary_counters",
            "classification_request",
        ],
        "allowed_target_kinds": [
            "SCRIPT_FILE",
            "SOURCE_FILE",
            "SCHEMA_FILE",
            "CONFIG_FILE",
            "TEST_FILE",
            "REFERENCE_ARTIFACT"
        ],
        "allowed_candidate_outcomes": [
            "TARGET_CANDIDATE_DECLARED_FOR_REVIEW",
            "TARGET_CANDIDATE_WITHHELD_NO_SINGLE_TARGET",
            "TARGET_CANDIDATE_REPAIR_REQUIRED",
            "TARGET_CANDIDATE_BLOCKED_AUTHORITY",
            "REQUEST_NARROWER_EVIDENCE"
        ],
        "candidate_rules": [
            "exactly one target candidate may be declared",
            "target_ref must be local and bounded",
            "target_ref must not use latest-file or mtime inference",
            "target_ref does not authorize writing",
            "verification gate must be referenced",
            "rollback-or-stop boundary must be referenced",
            "classification is review-only",
        ],
        "authority_boundary": {
            "may_declare_target_candidate_later": True,
            "may_apply_runtime_patch": False,
            "may_modify_target_files": False,
            "may_open_c5": False,
            "may_grant_general_cell1_authority": False,
            "may_promote_proposal_status": False,
            "may_fabricate_accepted_proposal": False,
            "may_use_latest_file_guessing": False,
            "may_use_mtime_selection": False,
        },
        "must_not_infer": [
            "declared target equals write authority",
            "target candidate equals runtime patch approval",
            "runtime patch safety",
            "C5 readiness",
            "general Cell1 builder authority",
            "accepted proposal implies target file",
        ],
    }

def target_narrowing_design_record(contract: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_narrowing_surface_design_record_v0",
        "design_id": "target_narrowing_design_" + sha8({"source": SOURCE_PRECHECK_RECEIPT_ID, "contract": contract["contract_id"]}),
        "source_precheck_receipt_id": SOURCE_PRECHECK_RECEIPT_ID,
        "source_blocker": "BLOCKED_MISSING_BOUNDED_TARGET",
        "future_target_narrowing_unit": FUTURE_TARGET_NARROWING_UNIT,
        "design_goal": "Design a bounded surface that can declare, withhold, or request repair for exactly one runtime patch target candidate without modifying that target.",
        "input_surface": {
            "source_precheck_classification_ref": rel(SOURCE_PRECHECK_CLASSIFICATION_PATH),
            "source_precheck_target_scan_ref": rel(SOURCE_PRECHECK_TARGET_SCAN_PATH),
            "source_accepted_proposal_packet_ref": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
            "source_schema_reference_packet_ref": rel(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH),
            "source_handoff_return_reference_packet_ref": rel(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH),
            "source_c1_patch_schema_ref": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
            "source_c2_lane_registry_ref": rel(SOURCE_C2_LANE_REGISTRY_PATH),
        },
        "target_candidate_contract_ref": rel(TARGET_CANDIDATE_CONTRACT_PATH),
        "narrowing_edges": [
            "read accepted proposal and existing precheck evidence",
            "search only declared source surfaces for target candidate hints",
            "declare exactly one bounded candidate if evidence is sufficient",
            "withhold candidate if no honest single target exists",
            "emit classification request for candidate review",
            "stop without target modification",
        ],
        "failure_classes_to_detect": [
            "TARGET_CANDIDATE_MISSING",
            "MULTIPLE_TARGET_CANDIDATES",
            "TARGET_REF_UNBOUNDED",
            "TARGET_REF_DOES_NOT_EXIST",
            "TARGET_SCOPE_USES_LATEST_FILE_GUESSING",
            "TARGET_SCOPE_USES_MTIME_SELECTION",
            "TARGET_SCOPE_AUTHORITY_LEAK",
            "TARGET_CANDIDATE_HIDDEN_NEXT_COMMAND",
            "TARGET_CANDIDATE_CLAIMS_PATCH_AUTHORITY",
            "TARGET_CANDIDATE_CLAIMS_C5_AUTHORITY",
        ],
        "non_goals": [
            "runtime patch application",
            "target file modification",
            "runtime patch verification execution",
            "C5 opening",
            "general Cell1 authority",
            "proposal status promotion",
            "accepted proposal fabrication",
        ],
    }

def target_narrowing_test_plan(contract: Dict[str, Any], design: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_narrowing_surface_test_plan_v0",
        "test_plan_id": "target_narrowing_plan_" + sha8({"design": design["design_id"]}),
        "future_target_narrowing_unit": FUTURE_TARGET_NARROWING_UNIT,
        "design_record_ref": rel(TARGET_NARROWING_DESIGN_RECORD_PATH),
        "target_candidate_contract_ref": rel(TARGET_CANDIDATE_CONTRACT_PATH),
        "test_mode": "BOUNDED_TARGET_NARROWING_SURFACE_ONLY",
        "steps": [
            "load design receipt and target candidate contract",
            "load runtime patch precheck blocker evidence",
            "load accepted proposal packet",
            "load frozen schema-intake and handoff-return references",
            "inspect declared surfaces for target candidate hints",
            "emit one candidate or withhold with explicit reason",
            "emit candidate classification request",
            "emit rollup/profile/receipt",
            "stop",
        ],
        "acceptance_requirements": [
            "source precheck blocker preserved",
            "accepted proposal preserved",
            "target candidate count is exactly one or explicitly withheld",
            "target reference does not use latest-file guessing",
            "target reference does not use mtime selection",
            "no runtime patch applied",
            "no target file modified",
            "no C5 opened",
            "no general Cell1 authority",
            "no hidden next command",
        ],
        "recommended_next_after_design": FUTURE_TARGET_NARROWING_UNIT,
        "next_command_goal": None,
    }

def authority_boundary() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_narrowing_surface_authority_boundary_v0",
        "authority_boundary_id": "target_narrowing_authority_" + sha8({"source": SOURCE_PRECHECK_RECEIPT_ID}),
        "may_emit_design_artifacts": True,
        "may_emit_future_target_narrowing_plan": True,
        "may_run_target_narrowing_now": False,
        "may_apply_runtime_patch": False,
        "may_modify_target_files": False,
        "may_open_c5": False,
        "may_grant_general_cell1_authority": False,
        "may_mutate_taxonomy": False,
        "may_promote_proposal_status": False,
        "may_fabricate_accepted_proposal": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "must_not_infer": [
            "target-narrowing surface has executed",
            "a target has been accepted",
            "target file writes are authorized",
            "runtime patch is authorized",
            "C5 is authorized",
            "Cell1 is a general builder",
        ],
    }

def rollup(contract: Dict[str, Any], design: Dict[str, Any], plan: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_narrowing_surface_design_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_precheck_receipt_id": SOURCE_PRECHECK_RECEIPT_ID,
        "source_precheck_design_receipt_id": SOURCE_PRECHECK_DESIGN_RECEIPT_ID,
        "source_after_return_next_objective_receipt_id": SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_ID,
        "source_handoff_return_close_receipt_id": SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID,
        "source_schema_close_receipt_id": SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "source_blocker": "BLOCKED_MISSING_BOUNDED_TARGET",
        "future_target_narrowing_unit": FUTURE_TARGET_NARROWING_UNIT,
        "target_candidate_contract_emitted_count": 1,
        "design_record_emitted_count": 1,
        "target_narrowing_test_plan_emitted_count": 1,
        "authority_boundary_emitted_count": 1,
        "target_narrowing_executed_count": 0,
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
        "recommended_next": FUTURE_TARGET_NARROWING_UNIT,
    }

def profile(rollup_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_narrowing_surface_design_profile_v0",
        "profile_id": "target_narrowing_design_" + sha8({"source": SOURCE_PRECHECK_RECEIPT_ID}),
        "status": "CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_DESIGNED",
        "source_blocker": rollup_obj["source_blocker"],
        "future_target_narrowing_unit": rollup_obj["future_target_narrowing_unit"],
        "target_narrowing_executed": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "next_command_goal": None,
    }

def report(rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_narrowing_surface_design_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_precheck_receipt_consumed_count": 1,
        "precheck_blocker_readout_emitted_count": 1,
        "target_candidate_contract_emitted_count": rollup_obj["target_candidate_contract_emitted_count"],
        "design_record_emitted_count": rollup_obj["design_record_emitted_count"],
        "target_narrowing_test_plan_emitted_count": rollup_obj["target_narrowing_test_plan_emitted_count"],
        "authority_boundary_emitted_count": rollup_obj["authority_boundary_emitted_count"],
        "profile_status": profile_obj["status"],
        "future_target_narrowing_unit": rollup_obj["future_target_narrowing_unit"],
        "recommended_next_handling": rollup_obj["recommended_next"],
        "target_narrowing_executed_count": 0,
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

def transition_trace(plan: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_narrowing_surface_design_transition_trace_v0",
        "trace": [
            {
                "step": "consume_runtime_patch_precheck",
                "question": "what blocked runtime patch eligibility",
                "answer": "BLOCKED_MISSING_BOUNDED_TARGET",
                "taken": "design_target_narrowing_surface",
            },
            {
                "step": "design_target_narrowing_surface",
                "question": "what surface can expose exactly one bounded target without writing it",
                "answer": rel(TARGET_CANDIDATE_CONTRACT_PATH),
                "taken": "emit_future_target_narrowing_plan",
            },
            {
                "step": "emit_future_target_narrowing_plan",
                "question": "did the unit avoid patching, target writes, C5, and general authority",
                "answer": "yes",
                "taken": "stop",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_DESIGNED",
            "next_command_goal": None,
        },
    }

def validate_outputs(contract: Dict[str, Any], design: Dict[str, Any], plan: Dict[str, Any], boundary: Dict[str, Any], rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any], report_obj: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if contract.get("candidate_object_type") != "BOUNDED_RUNTIME_PATCH_TARGET_CANDIDATE":
        failures.append("contract_wrong_candidate_object_type")
    if contract.get("authority_boundary", {}).get("may_apply_runtime_patch") is not False:
        failures.append("contract_allows_runtime_patch")
    if contract.get("authority_boundary", {}).get("may_modify_target_files") is not False:
        failures.append("contract_allows_target_file_modification")
    if contract.get("authority_boundary", {}).get("may_open_c5") is not False:
        failures.append("contract_allows_c5")
    if contract.get("authority_boundary", {}).get("may_use_latest_file_guessing") is not False:
        failures.append("contract_allows_latest_file_guessing")
    if contract.get("authority_boundary", {}).get("may_use_mtime_selection") is not False:
        failures.append("contract_allows_mtime_selection")
    if design.get("source_blocker") != "BLOCKED_MISSING_BOUNDED_TARGET":
        failures.append("design_wrong_source_blocker")
    if design.get("future_target_narrowing_unit") != FUTURE_TARGET_NARROWING_UNIT:
        failures.append("design_wrong_future_target_narrowing_unit")
    if "runtime patch application" not in design.get("non_goals", []):
        failures.append("design_missing_runtime_patch_nongoal")
    if plan.get("future_target_narrowing_unit") != FUTURE_TARGET_NARROWING_UNIT:
        failures.append("plan_wrong_future_target_narrowing_unit")
    if plan.get("next_command_goal") is not None:
        failures.append("plan_hidden_next_command")
    if boundary.get("may_run_target_narrowing_now") is not False:
        failures.append("authority_allows_target_narrowing_execution")
    if boundary.get("may_apply_runtime_patch") is not False:
        failures.append("authority_allows_runtime_patch")
    if boundary.get("may_modify_target_files") is not False:
        failures.append("authority_allows_target_file_modification")
    if boundary.get("may_open_c5") is not False:
        failures.append("authority_allows_c5")
    if boundary.get("may_grant_general_cell1_authority") is not False:
        failures.append("authority_allows_general_cell1")
    if boundary.get("may_use_latest_file_guessing") is not False:
        failures.append("authority_allows_latest_file_guessing")
    if boundary.get("may_use_mtime_selection") is not False:
        failures.append("authority_allows_mtime_selection")
    for key in ZERO_COUNTER_KEYS:
        if rollup_obj.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup_obj.get(key)}")
    if rollup_obj.get("target_candidate_contract_emitted_count") != 1:
        failures.append("target_candidate_contract_count_not_one")
    if rollup_obj.get("design_record_emitted_count") != 1:
        failures.append("design_record_count_not_one")
    if rollup_obj.get("target_narrowing_test_plan_emitted_count") != 1:
        failures.append("target_narrowing_plan_count_not_one")
    if profile_obj.get("target_narrowing_executed") is not False:
        failures.append("profile_claims_target_narrowing_executed")
    if profile_obj.get("runtime_patch_applied") is not False:
        failures.append("profile_claims_runtime_patch")
    if profile_obj.get("target_file_modified") is not False:
        failures.append("profile_claims_target_file_modified")
    if profile_obj.get("c5_opened") is not False:
        failures.append("profile_claims_c5")
    if profile_obj.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")
    for key in [
        "target_narrowing_executed_count",
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
    if terminal.get("stop_code") != "STOP_CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_DESIGNED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    contract = read_json(TARGET_CANDIDATE_CONTRACT_PATH)
    design = read_json(TARGET_NARROWING_DESIGN_RECORD_PATH)
    plan = read_json(TARGET_NARROWING_TEST_PLAN_PATH)
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

    bad_contract = copy.deepcopy(contract)
    bad_contract["authority_boundary"]["may_apply_runtime_patch"] = True
    add("contract_allows_runtime_patch_fail", validate_outputs(bad_contract, design, plan, boundary, rollup_obj, profile_obj, report_obj), "contract_allows_runtime_patch")

    bad_contract = copy.deepcopy(contract)
    bad_contract["authority_boundary"]["may_modify_target_files"] = True
    add("contract_allows_target_file_modification_fail", validate_outputs(bad_contract, design, plan, boundary, rollup_obj, profile_obj, report_obj), "contract_allows_target_file_modification")

    bad_contract = copy.deepcopy(contract)
    bad_contract["authority_boundary"]["may_use_latest_file_guessing"] = True
    add("contract_allows_latest_file_guessing_fail", validate_outputs(bad_contract, design, plan, boundary, rollup_obj, profile_obj, report_obj), "contract_allows_latest_file_guessing")

    bad_design = copy.deepcopy(design)
    bad_design["source_blocker"] = "ELIGIBLE_FOR_MINIMAL_RUNTIME_PATCH_TEST_DESIGN"
    add("design_wrong_source_blocker_fail", validate_outputs(contract, bad_design, plan, boundary, rollup_obj, profile_obj, report_obj), "design_wrong_source_blocker")

    bad_plan = copy.deepcopy(plan)
    bad_plan["next_command_goal"] = "RUN_TARGET_NARROWING"
    add("plan_hidden_next_command_fail", validate_outputs(contract, design, bad_plan, boundary, rollup_obj, profile_obj, report_obj), "plan_hidden_next_command")

    for case, field, expected in [
        ("authority_allows_target_narrowing_execution_fail", "may_run_target_narrowing_now", "authority_allows_target_narrowing_execution"),
        ("authority_allows_runtime_patch_fail", "may_apply_runtime_patch", "authority_allows_runtime_patch"),
        ("authority_allows_target_file_modification_fail", "may_modify_target_files", "authority_allows_target_file_modification"),
        ("authority_allows_c5_fail", "may_open_c5", "authority_allows_c5"),
        ("authority_allows_general_cell1_fail", "may_grant_general_cell1_authority", "authority_allows_general_cell1"),
        ("authority_allows_latest_file_guessing_fail", "may_use_latest_file_guessing", "authority_allows_latest_file_guessing"),
        ("authority_allows_mtime_selection_fail", "may_use_mtime_selection", "authority_allows_mtime_selection"),
    ]:
        bad_boundary = copy.deepcopy(boundary)
        bad_boundary[field] = True
        add(case, validate_outputs(contract, design, plan, bad_boundary, rollup_obj, profile_obj, report_obj), expected)

    for case, counter in [
        ("target_narrowing_executed_fail", "target_narrowing_executed_count"),
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
    ]:
        bad_rollup = copy.deepcopy(rollup_obj)
        bad_report = copy.deepcopy(report_obj)
        bad_rollup[counter] = 1
        if counter in bad_report:
            bad_report[counter] = 1
        add(case, validate_outputs(contract, design, plan, boundary, bad_rollup, profile_obj, bad_report), counter)

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_DESIGN_EVIDENCE_REQUEST_REQUIRED", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "cell1_runtime_patch_target_narrowing_surface_design_receipt_v0",
            "receipt_type": "CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_DESIGN_RECEIPT",
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
        print(f"target_narrowing_surface_design_receipt_id={receipt_id}")
        print(f"target_narrowing_surface_design_receipt_path=data/cell1_runtime_patch_target_narrowing_surface_design_v0_receipts/{receipt_id}.json")
        return 1

    readout = precheck_blocker_readout()
    contract = target_candidate_contract()
    design = target_narrowing_design_record(contract)
    plan = target_narrowing_test_plan(contract, design)
    boundary = authority_boundary()
    rollup_obj = rollup(contract, design, plan)
    profile_obj = profile(rollup_obj)
    report_obj = report(rollup_obj, profile_obj)
    trace = transition_trace(plan)

    write_json(SOURCE_SURFACE_PATH, source_surface())
    write_json(PRECHECK_BLOCKER_READOUT_PATH, readout)
    write_json(TARGET_CANDIDATE_CONTRACT_PATH, contract)
    write_json(TARGET_NARROWING_DESIGN_RECORD_PATH, design)
    write_json(TARGET_NARROWING_TEST_PLAN_PATH, plan)
    write_json(AUTHORITY_BOUNDARY_PATH, boundary)
    write_json(ROLLUP_PATH, rollup_obj)
    write_json(PROFILE_PATH, profile_obj)
    write_json(REPORT_PATH, report_obj)
    write_json(TRANSITION_TRACE_PATH, trace)

    failures.extend(validate_outputs(contract, design, plan, boundary, rollup_obj, profile_obj, report_obj))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup_obj["source_mutation_count"] = 1
        report_obj["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup_obj)
        write_json(REPORT_PATH, report_obj)

    acceptance_gate_results = {
        "TARGET_NARROWING_DESIGN_0_PRECHECK_RECEIPT_CONSUMED": SOURCE_PRECHECK_RECEIPT_PATH.exists(),
        "TARGET_NARROWING_DESIGN_1_BLOCKER_CONFIRMED": readout["blocker"] == "MISSING_BOUNDED_RUNTIME_PATCH_TARGET",
        "TARGET_NARROWING_DESIGN_2_PRECHECK_BLOCKER_READOUT_EMITTED": PRECHECK_BLOCKER_READOUT_PATH.exists(),
        "TARGET_NARROWING_DESIGN_3_TARGET_CANDIDATE_CONTRACT_EMITTED": TARGET_CANDIDATE_CONTRACT_PATH.exists(),
        "TARGET_NARROWING_DESIGN_4_DESIGN_RECORD_EMITTED": TARGET_NARROWING_DESIGN_RECORD_PATH.exists(),
        "TARGET_NARROWING_DESIGN_5_TEST_PLAN_EMITTED": TARGET_NARROWING_TEST_PLAN_PATH.exists(),
        "TARGET_NARROWING_DESIGN_6_AUTHORITY_BOUNDARY_EMITTED": AUTHORITY_BOUNDARY_PATH.exists(),
        "TARGET_NARROWING_DESIGN_7_NO_TARGET_NARROWING_EXECUTED": rollup_obj["target_narrowing_executed_count"] == 0,
        "TARGET_NARROWING_DESIGN_8_NO_RUNTIME_PATCH": rollup_obj["runtime_patch_applied_count"] == 0,
        "TARGET_NARROWING_DESIGN_9_NO_TARGET_FILE_MODIFICATION": rollup_obj["target_file_modified_count"] == 0,
        "TARGET_NARROWING_DESIGN_10_NO_C5_OPENED": rollup_obj["c5_opened_count"] == 0,
        "TARGET_NARROWING_DESIGN_11_NO_GENERAL_CELL1_AUTHORITY": rollup_obj["general_cell1_authority_granted_count"] == 0,
        "TARGET_NARROWING_DESIGN_12_NO_PROPOSAL_PROMOTION": rollup_obj["proposal_status_promoted_count"] == 0,
        "TARGET_NARROWING_DESIGN_13_NO_ACCEPTED_PROPOSAL_FABRICATION": rollup_obj["accepted_proposal_fabricated_count"] == 0,
        "TARGET_NARROWING_DESIGN_14_NO_UNBOUNDED_PAYLOAD_INSPECTION": rollup_obj["unbounded_payload_inspection_count"] == 0,
        "TARGET_NARROWING_DESIGN_15_NO_HIDDEN_NEXT_COMMAND": rollup_obj["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
        "TARGET_NARROWING_DESIGN_16_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    for gate_name, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate_name}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_precheck": SOURCE_PRECHECK_RECEIPT_ID,
        "future_target_narrowing_unit": FUTURE_TARGET_NARROWING_UNIT,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "precheck_blocker_readout": rel(PRECHECK_BLOCKER_READOUT_PATH),
        "target_candidate_contract": rel(TARGET_CANDIDATE_CONTRACT_PATH),
        "target_narrowing_design_record": rel(TARGET_NARROWING_DESIGN_RECORD_PATH),
        "target_narrowing_test_plan": rel(TARGET_NARROWING_TEST_PLAN_PATH),
        "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
        "rollup": rel(ROLLUP_PATH),
        "profile": rel(PROFILE_PATH),
        "report": rel(REPORT_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_precheck_receipt": rel(SOURCE_PRECHECK_RECEIPT_PATH),
        "source_precheck_classification": rel(SOURCE_PRECHECK_CLASSIFICATION_PATH),
        "source_precheck_target_scan": rel(SOURCE_PRECHECK_TARGET_SCAN_PATH),
        "source_accepted_proposal_packet": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "source_schema_reference_packet": rel(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH),
        "source_handoff_return_reference_packet": rel(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH),
    }

    guards = {
        "build_mode_target_narrowing_surface_design_only": BUILD_MODE == "RUNTIME_PATCH_TARGET_NARROWING_SURFACE_DESIGN_ONLY",
        "source_blocker": "BLOCKED_MISSING_BOUNDED_TARGET",
        "future_target_narrowing_unit": FUTURE_TARGET_NARROWING_UNIT,
        "target_narrowing_executed": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "proposal_status_promoted": False,
        "accepted_proposal_fabricated": False,
        "unbounded_payload_inspection": False,
        "hidden_next_command": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
    }

    receipt = {
        "schema_version": "cell1_runtime_patch_target_narrowing_surface_design_receipt_v0",
        "receipt_type": "CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_DESIGN_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "bounded Cell1 runtime patch target narrowing surface design",
        "source_precheck_receipt_id": SOURCE_PRECHECK_RECEIPT_ID,
        "source_precheck_design_receipt_id": SOURCE_PRECHECK_DESIGN_RECEIPT_ID,
        "source_after_return_next_objective_receipt_id": SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_ID,
        "source_handoff_return_close_receipt_id": SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID,
        "source_schema_close_receipt_id": SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "target_narrowing_surface_design_summary": {
            "profile_status": profile_obj["status"],
            "source_blocker": rollup_obj["source_blocker"],
            "future_target_narrowing_unit": FUTURE_TARGET_NARROWING_UNIT,
            "target_candidate_contract_emitted_count": rollup_obj["target_candidate_contract_emitted_count"],
            "design_record_emitted_count": rollup_obj["design_record_emitted_count"],
            "target_narrowing_test_plan_emitted_count": rollup_obj["target_narrowing_test_plan_emitted_count"],
            "target_narrowing_executed": False,
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "general_cell1_authority_granted": False,
            "bad_counters_zero": profile_obj["bad_counters_zero"],
            "recommended_next": rollup_obj["recommended_next"],
        },
        "aggregate_metrics": {
            **{k: v for k, v in report_obj.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
            "rollup": rollup_obj,
            "source_mutation_count": 1 if source_mutation_detected else report_obj["source_mutation_count"],
        },
        "acceptance_gate_results": acceptance_gate_results,
        "target_narrowing_surface_design_guards": guards,
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
    if len(negative_controls) != 24 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
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
    print(f"target_narrowing_surface_design_receipt_id={receipt_id}")
    print(f"target_narrowing_surface_design_receipt_path=data/cell1_runtime_patch_target_narrowing_surface_design_v0_receipts/{receipt_id}.json")
    print(f"target_narrowing_surface_design_record_path=data/cell1_runtime_patch_target_narrowing_surface_design_v0/target_narrowing_surface_design_record_v0.json")
    print(f"target_candidate_contract_path=data/cell1_runtime_patch_target_narrowing_surface_design_v0/bounded_target_candidate_contract_v0.json")
    print(f"target_narrowing_surface_test_plan_path=data/cell1_runtime_patch_target_narrowing_surface_design_v0/target_narrowing_surface_test_plan_v0.json")
    print(f"target_narrowing_surface_rollup_path=data/cell1_runtime_patch_target_narrowing_surface_design_v0/target_narrowing_surface_design_rollup_v0.json")
    print(f"target_narrowing_surface_profile_path=data/cell1_runtime_patch_target_narrowing_surface_design_v0/target_narrowing_surface_design_profile_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
