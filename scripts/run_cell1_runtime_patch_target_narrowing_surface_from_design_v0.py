#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RUN_CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_FROM_DESIGN_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_narrowing_surface.run_from_design.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_NARROWING_SURFACE"
MODE = "RUN / TARGET_NARROWING_SURFACE / NO_PATCH"
BUILD_MODE = "BOUNDED_TARGET_NARROWING_SURFACE_ONLY"

SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_ID = "07bc35ea"
SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_design_v0_receipts" / "07bc35ea.json"
SOURCE_TARGET_NARROWING_DESIGN_RECORD_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_design_v0" / "target_narrowing_surface_design_record_v0.json"
SOURCE_TARGET_CANDIDATE_CONTRACT_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_design_v0" / "bounded_target_candidate_contract_v0.json"
SOURCE_TARGET_NARROWING_TEST_PLAN_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_design_v0" / "target_narrowing_surface_test_plan_v0.json"
SOURCE_TARGET_NARROWING_AUTHORITY_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_design_v0" / "target_narrowing_surface_authority_boundary_v0.json"
SOURCE_TARGET_NARROWING_ROLLUP_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_design_v0" / "target_narrowing_surface_design_rollup_v0.json"
SOURCE_TARGET_NARROWING_PROFILE_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_design_v0" / "target_narrowing_surface_design_profile_v0.json"
SOURCE_PRECHECK_BLOCKER_READOUT_PATH = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_design_v0" / "precheck_blocker_readout_v0.json"

SOURCE_PRECHECK_RECEIPT_ID = "c534ce7c"
SOURCE_PRECHECK_RECEIPT_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_run_v0_receipts" / "c534ce7c.json"
SOURCE_PRECHECK_CLASSIFICATION_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_run_v0" / "runtime_patch_precheck_eligibility_classification_v0.json"
SOURCE_PRECHECK_TARGET_SCAN_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_run_v0" / "bounded_runtime_patch_target_candidate_scan_v0.json"
SOURCE_PRECHECK_EVIDENCE_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_run_v0" / "runtime_patch_precheck_eligibility_evidence_v0.json"

SOURCE_PRECHECK_DESIGN_RECEIPT_ID = "a62d6ec2"
SOURCE_PRECHECK_DESIGN_RECEIPT_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_design_v0_receipts" / "a62d6ec2.json"
SOURCE_PRECHECK_CONTRACT_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_design_v0" / "runtime_patch_precheck_eligibility_contract_v0.json"

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
    SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_PATH,
    SOURCE_TARGET_NARROWING_DESIGN_RECORD_PATH,
    SOURCE_TARGET_CANDIDATE_CONTRACT_PATH,
    SOURCE_TARGET_NARROWING_TEST_PLAN_PATH,
    SOURCE_TARGET_NARROWING_AUTHORITY_PATH,
    SOURCE_TARGET_NARROWING_ROLLUP_PATH,
    SOURCE_TARGET_NARROWING_PROFILE_PATH,
    SOURCE_PRECHECK_BLOCKER_READOUT_PATH,
    SOURCE_PRECHECK_RECEIPT_PATH,
    SOURCE_PRECHECK_CLASSIFICATION_PATH,
    SOURCE_PRECHECK_TARGET_SCAN_PATH,
    SOURCE_PRECHECK_EVIDENCE_PATH,
    SOURCE_PRECHECK_DESIGN_RECEIPT_PATH,
    SOURCE_PRECHECK_CONTRACT_PATH,
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

OUT_DIR = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_run_v0"
RECEIPT_DIR = ROOT / "data" / "cell1_runtime_patch_target_narrowing_surface_run_v0_receipts"

SOURCE_SURFACE_PATH = OUT_DIR / "source_surface_v0.json"
DESIGN_READOUT_PATH = OUT_DIR / "target_narrowing_design_readout_v0.json"
DECLARED_SOURCE_SCAN_PATH = OUT_DIR / "declared_source_target_hint_scan_v0.json"
TARGET_CANDIDATE_RECORD_PATH = OUT_DIR / "target_candidate_record_v0.json"
TARGET_CANDIDATE_CLASSIFICATION_PATH = OUT_DIR / "target_candidate_classification_v0.json"
CLASSIFICATION_REQUEST_PATH = OUT_DIR / "target_candidate_review_classification_request_v0.json"
AUTHORITY_AUDIT_PATH = OUT_DIR / "target_narrowing_authority_audit_v0.json"
ROLLUP_PATH = OUT_DIR / "target_narrowing_surface_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "target_narrowing_surface_profile_v0.json"
REPORT_PATH = OUT_DIR / "target_narrowing_surface_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "target_narrowing_surface_transition_trace.json"

ZERO_COUNTER_KEYS = [
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
    "latest_file_guessing_count",
    "mtime_selection_count",
]

HUMAN_DECISION = {
    "decision": "RUN_CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_FROM_DESIGN",
    "scope": "Run the bounded target-narrowing surface from design. Inspect only declared source surfaces for a single bounded runtime patch target candidate. Declare exactly one candidate only if evidence is sufficient; otherwise withhold the target and request narrower evidence. This unit does not apply a runtime patch, does not modify target files, does not open C5, and does not grant general Cell1 authority.",
    "authorized": [
        "consume target-narrowing design receipt",
        "consume target candidate contract",
        "consume runtime patch precheck blocker",
        "inspect declared source surfaces for target hints",
        "emit candidate record or withhold record",
        "emit review classification request",
        "emit authority audit",
        "emit receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
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

def iter_json_paths(obj: Any, prefix: str = "$") -> Iterable[Tuple[str, Any]]:
    yield prefix, obj
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from iter_json_paths(v, f"{prefix}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_json_paths(v, f"{prefix}[{i}]")

def keyish(path: str) -> str:
    return path.lower().replace("_", "-").replace(".", "-")

def is_local_file_candidate(value: str) -> bool:
    if not isinstance(value, str):
        return False
    value = value.strip()
    if not value:
        return False
    if value.startswith(("http://", "https://", "s3://", "gs://", "/")):
        return False
    if ".." in Path(value).parts:
        return False
    return (
        value.endswith((".py", ".json", ".jsonl", ".txt", ".md", ".yaml", ".yml", ".toml"))
        or value.startswith(("src/", "scripts/", "data/", "app/", "tests/"))
    )

def validate_source_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    design_receipt = read_json(SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_PATH)
    design = read_json(SOURCE_TARGET_NARROWING_DESIGN_RECORD_PATH)
    contract = read_json(SOURCE_TARGET_CANDIDATE_CONTRACT_PATH)
    plan = read_json(SOURCE_TARGET_NARROWING_TEST_PLAN_PATH)
    authority = read_json(SOURCE_TARGET_NARROWING_AUTHORITY_PATH)
    rollup = read_json(SOURCE_TARGET_NARROWING_ROLLUP_PATH)
    profile = read_json(SOURCE_TARGET_NARROWING_PROFILE_PATH)
    blocker = read_json(SOURCE_PRECHECK_BLOCKER_READOUT_PATH)
    precheck_receipt = read_json(SOURCE_PRECHECK_RECEIPT_PATH)
    precheck_classification = read_json(SOURCE_PRECHECK_CLASSIFICATION_PATH)
    precheck_target_scan = read_json(SOURCE_PRECHECK_TARGET_SCAN_PATH)
    precheck_evidence = read_json(SOURCE_PRECHECK_EVIDENCE_PATH)
    accepted_receipt = read_json(SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH)
    accepted_packet = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    return_receipt = read_json(SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH)
    return_reference = read_json(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH)
    schema_receipt = read_json(SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_PATH)
    schema_reference = read_json(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH)
    c1_receipt = read_json(SOURCE_C1_PATCH_RECEIPT_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)

    if design_receipt.get("receipt_id") != SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_ID or design_receipt.get("gate") != "PASS":
        failures.append("target_narrowing_design_receipt_not_pass")
    if design_receipt.get("terminal", {}).get("stop_code") != "STOP_CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_DESIGNED":
        failures.append("target_narrowing_design_wrong_terminal")
    if design.get("future_target_narrowing_unit") != UNIT_ID:
        failures.append("design_future_target_narrowing_unit_wrong")
    if contract.get("candidate_object_type") != "BOUNDED_RUNTIME_PATCH_TARGET_CANDIDATE":
        failures.append("contract_candidate_object_wrong")
    for key in ["may_apply_runtime_patch", "may_modify_target_files", "may_open_c5", "may_grant_general_cell1_authority", "may_use_latest_file_guessing", "may_use_mtime_selection"]:
        if contract.get("authority_boundary", {}).get(key) is not False:
            failures.append(f"contract_authority_not_false:{key}")
    if plan.get("future_target_narrowing_unit") != UNIT_ID:
        failures.append("plan_future_target_narrowing_unit_wrong")
    if plan.get("test_mode") != "BOUNDED_TARGET_NARROWING_SURFACE_ONLY":
        failures.append("plan_test_mode_wrong")
    if plan.get("next_command_goal") is not None:
        failures.append("plan_hidden_next_command")
    for key in ["may_run_target_narrowing_now", "may_apply_runtime_patch", "may_modify_target_files", "may_open_c5", "may_grant_general_cell1_authority", "may_use_latest_file_guessing", "may_use_mtime_selection"]:
        if authority.get(key) is not False:
            failures.append(f"design_authority_not_false:{key}")
    if rollup.get("target_narrowing_executed_count") != 0:
        failures.append("design_rollup_already_executed")
    if profile.get("status") != "CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_DESIGNED":
        failures.append("design_profile_not_designed")
    if blocker.get("blocker") != "MISSING_BOUNDED_RUNTIME_PATCH_TARGET":
        failures.append("blocker_readout_wrong")
    if precheck_receipt.get("receipt_id") != SOURCE_PRECHECK_RECEIPT_ID or precheck_receipt.get("gate") != "PASS":
        failures.append("precheck_receipt_not_pass")
    if precheck_classification.get("eligibility_outcome") != "BLOCKED_MISSING_BOUNDED_TARGET":
        failures.append("precheck_classification_not_missing_target")
    if precheck_target_scan.get("bounded_candidate_count") != 0:
        failures.append("precheck_target_scan_not_zero")
    if precheck_evidence.get("accepted_proposal", {}).get("accepted_for_build") is not True:
        failures.append("precheck_evidence_no_accepted_proposal")
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
        "schema_version": "cell1_runtime_patch_target_narrowing_surface_source_surface_v0",
        "source_target_narrowing_design_receipt_id": SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_ID,
        "source_target_narrowing_design_receipt_ref": rel(SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_PATH),
        "source_target_candidate_contract_ref": rel(SOURCE_TARGET_CANDIDATE_CONTRACT_PATH),
        "source_precheck_receipt_id": SOURCE_PRECHECK_RECEIPT_ID,
        "source_precheck_classification_ref": rel(SOURCE_PRECHECK_CLASSIFICATION_PATH),
        "source_accepted_proposal_packet_ref": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "surface_status": "EXPLICIT_TARGET_NARROWING_RUN_SURFACE",
    }

def design_readout() -> Dict[str, Any]:
    design = read_json(SOURCE_TARGET_NARROWING_DESIGN_RECORD_PATH)
    contract = read_json(SOURCE_TARGET_CANDIDATE_CONTRACT_PATH)
    blocker = read_json(SOURCE_PRECHECK_BLOCKER_READOUT_PATH)
    return {
        "schema_version": "cell1_runtime_patch_target_narrowing_design_readout_v0",
        "design_id": design.get("design_id"),
        "contract_id": contract.get("contract_id"),
        "source_blocker": design.get("source_blocker"),
        "blocker": blocker.get("blocker"),
        "candidate_object_type": contract.get("candidate_object_type"),
        "allowed_candidate_outcomes": contract.get("allowed_candidate_outcomes", []),
        "candidate_rules": contract.get("candidate_rules", []),
        "future_target_narrowing_unit": design.get("future_target_narrowing_unit"),
    }

def declared_source_target_hint_scan() -> Dict[str, Any]:
    sources = {
        "accepted_proposal_packet": read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "target_narrowing_design_record": read_json(SOURCE_TARGET_NARROWING_DESIGN_RECORD_PATH),
        "target_candidate_contract": read_json(SOURCE_TARGET_CANDIDATE_CONTRACT_PATH),
        "precheck_evidence": read_json(SOURCE_PRECHECK_EVIDENCE_PATH),
        "precheck_target_scan": read_json(SOURCE_PRECHECK_TARGET_SCAN_PATH),
    }

    hints: List[Dict[str, Any]] = []
    for source, obj in sources.items():
        for path, value in iter_json_paths(obj):
            k = keyish(path)
            if not isinstance(value, str):
                continue
            v = value.strip()
            if "latest" in v.lower() or "mtime" in v.lower():
                continue
            if ("target" in k or "patch" in k or "file" in k or "ref" in k) and is_local_file_candidate(v):
                hints.append({
                    "source": source,
                    "json_path": path,
                    "hint_ref": v,
                    "exists_now": (ROOT / v).exists(),
                    "bounded": True,
                    "reason": "declared-source-local-bounded-file-like-ref",
                })

    unique = []
    seen = set()
    for h in hints:
        key = (h["source"], h["json_path"], h["hint_ref"])
        if key not in seen:
            seen.add(key)
            unique.append(h)

    candidate_hints = [
        h for h in unique
        if h["hint_ref"] not in {
            "data/accepted_proposal_packet_for_c4_consumption_v0/accepted_proposal_packet_v0.json",
            "data/cell1_schema_consumption_test_review_or_close_v0/cell1_schema_test_frozen_reference_packet_v0.json",
            "data/cell1_handoff_return_loop_review_or_close_v0/handoff_return_loop_frozen_reference_packet_v0.json",
        }
    ]

    return {
        "schema_version": "cell1_runtime_patch_target_narrowing_declared_source_target_hint_scan_v0",
        "scan_id": "target_hint_scan_" + sha8({"source": SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_ID, "n": len(candidate_hints)}),
        "allowed_sources_scanned": list(sources.keys()),
        "hint_count": len(candidate_hints),
        "bounded_hint_count": sum(1 for h in candidate_hints if h["bounded"]),
        "existing_bounded_hint_count": sum(1 for h in candidate_hints if h["bounded"] and h["exists_now"]),
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "unbounded_payload_inspection_count": 0,
        "hints": candidate_hints,
        "scan_status": "HAS_SINGLE_TARGET_HINT" if len(candidate_hints) == 1 else "NO_SINGLE_TARGET_HINT",
    }

def target_candidate_record(scan: Dict[str, Any]) -> Dict[str, Any]:
    contract = read_json(SOURCE_TARGET_CANDIDATE_CONTRACT_PATH)
    if scan["hint_count"] == 1:
        h = scan["hints"][0]
        return {
            "schema_version": "cell1_runtime_patch_target_candidate_record_v0",
            "target_candidate_id": "target_candidate_" + sha8(h),
            "candidate_status": "TARGET_CANDIDATE_DECLARED_FOR_REVIEW",
            "target_ref": h["hint_ref"],
            "target_kind": "SCRIPT_FILE" if h["hint_ref"].endswith(".py") else "REFERENCE_ARTIFACT",
            "why_this_target": "Exactly one bounded target-like reference was found in declared source surfaces.",
            "source_evidence_refs": [
                rel(SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_PATH),
                rel(SOURCE_PRECHECK_RECEIPT_PATH),
                rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
                h["source"] + ":" + h["json_path"],
            ],
            "allowed_write_scope": "NONE_DURING_TARGET_NARROWING",
            "verification_gate_ref": rel(SOURCE_PRECHECK_CLASSIFICATION_PATH),
            "rollback_or_stop_boundary_ref": rel(SOURCE_PRECHECK_CLASSIFICATION_PATH),
            "authority_boundary": contract.get("authority_boundary", {}),
            "negative_boundary_counters": {key: 0 for key in ZERO_COUNTER_KEYS},
            "classification_request": "REQUEST_TARGET_CANDIDATE_REVIEW_ONLY",
            "runtime_patch_authorized": False,
            "target_file_modification_authorized": False,
            "c5_authorized": False,
            "general_cell1_authority_granted": False,
        }
    return {
        "schema_version": "cell1_runtime_patch_target_candidate_record_v0",
        "target_candidate_id": "target_candidate_withheld_" + sha8({"source": SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_ID, "hint_count": scan["hint_count"]}),
        "candidate_status": "TARGET_CANDIDATE_WITHHELD_NO_SINGLE_TARGET",
        "target_ref": None,
        "target_kind": None,
        "why_this_target": None,
        "withheld_reason": "No single bounded runtime patch target candidate was visible in declared source surfaces.",
        "source_evidence_refs": [
            rel(SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_PATH),
            rel(SOURCE_PRECHECK_RECEIPT_PATH),
            rel(SOURCE_PRECHECK_TARGET_SCAN_PATH),
            rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        ],
        "allowed_write_scope": "NONE_DURING_TARGET_NARROWING",
        "verification_gate_ref": rel(SOURCE_PRECHECK_CLASSIFICATION_PATH),
        "rollback_or_stop_boundary_ref": rel(SOURCE_PRECHECK_CLASSIFICATION_PATH),
        "negative_boundary_counters": {key: 0 for key in ZERO_COUNTER_KEYS},
        "classification_request": "REQUEST_NARROWER_TARGET_EVIDENCE",
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
    }

def classify_candidate(record: Dict[str, Any], scan: Dict[str, Any]) -> Dict[str, Any]:
    contract = read_json(SOURCE_TARGET_CANDIDATE_CONTRACT_PATH)
    allowed = contract.get("allowed_candidate_outcomes", [])
    outcome = record["candidate_status"]
    if outcome not in allowed:
        outcome = "TARGET_CANDIDATE_REPAIR_REQUIRED"
    recommended_next = {
        "TARGET_CANDIDATE_DECLARED_FOR_REVIEW": "REVIEW_CELL1_RUNTIME_PATCH_TARGET_CANDIDATE_V0",
        "TARGET_CANDIDATE_WITHHELD_NO_SINGLE_TARGET": "REQUEST_NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_V0",
        "TARGET_CANDIDATE_REPAIR_REQUIRED": "REPAIR_CELL1_RUNTIME_PATCH_TARGET_CANDIDATE_SURFACE_V0",
        "TARGET_CANDIDATE_BLOCKED_AUTHORITY": "REVIEW_CELL1_RUNTIME_PATCH_TARGET_AUTHORITY_BOUNDARY_V0",
        "REQUEST_NARROWER_EVIDENCE": "REQUEST_NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_V0",
    }[outcome]
    return {
        "schema_version": "cell1_runtime_patch_target_candidate_classification_v0",
        "classification_id": "target_candidate_classification_" + sha8({"outcome": outcome, "scan": scan["scan_id"]}),
        "candidate_status": outcome,
        "target_candidate_declared": outcome == "TARGET_CANDIDATE_DECLARED_FOR_REVIEW",
        "target_candidate_withheld": outcome == "TARGET_CANDIDATE_WITHHELD_NO_SINGLE_TARGET",
        "target_ref": record.get("target_ref"),
        "hint_count": scan["hint_count"],
        "bounded_hint_count": scan["bounded_hint_count"],
        "recommended_next": recommended_next,
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "proposal_status_promoted": False,
        "accepted_proposal_fabricated": False,
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_COMPLETE",
            "next_command_goal": None,
        },
    }

def classification_request(record: Dict[str, Any], classification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_candidate_review_classification_request_v0",
        "request_id": "target_candidate_review_request_" + sha8({"candidate": record["target_candidate_id"], "classification": classification["classification_id"]}),
        "candidate_ref": rel(TARGET_CANDIDATE_RECORD_PATH),
        "classification_ref": rel(TARGET_CANDIDATE_CLASSIFICATION_PATH),
        "request_kind": record["classification_request"],
        "review_only": True,
        "accepted_for_build": False,
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "next_command_goal": None,
    }

def authority_audit(record: Dict[str, Any], classification: Dict[str, Any]) -> Dict[str, Any]:
    counters = {key: 0 for key in ZERO_COUNTER_KEYS}
    return {
        "schema_version": "cell1_runtime_patch_target_narrowing_authority_audit_v0",
        "audit_id": "target_narrowing_audit_" + sha8({"classification": classification["candidate_status"]}),
        "candidate_status": classification["candidate_status"],
        "negative_boundary_counters": counters,
        "target_narrowing_authority": {
            "may_declare_candidate_for_review": classification["target_candidate_declared"],
            "may_apply_runtime_patch": False,
            "may_modify_target_files": False,
            "may_open_c5": False,
            "may_grant_general_cell1_authority": False,
            "may_promote_proposal_status": False,
            "may_fabricate_accepted_proposal": False,
            "may_use_latest_file_guessing": False,
            "may_use_mtime_selection": False,
        },
        "record_authority": {
            "runtime_patch_authorized": record.get("runtime_patch_authorized"),
            "target_file_modification_authorized": record.get("target_file_modification_authorized"),
            "c5_authorized": record.get("c5_authorized"),
            "general_cell1_authority_granted": record.get("general_cell1_authority_granted"),
        },
        "audit_status": "PASS",
    }

def rollup(scan: Dict[str, Any], record: Dict[str, Any], classification: Dict[str, Any], audit: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_narrowing_surface_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_target_narrowing_design_receipt_id": SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_ID,
        "source_precheck_receipt_id": SOURCE_PRECHECK_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "hint_count": scan["hint_count"],
        "bounded_hint_count": scan["bounded_hint_count"],
        "existing_bounded_hint_count": scan["existing_bounded_hint_count"],
        "target_candidate_record_emitted_count": 1,
        "target_candidate_declared_count": 1 if classification["target_candidate_declared"] else 0,
        "target_candidate_withheld_count": 1 if classification["target_candidate_withheld"] else 0,
        "candidate_status": classification["candidate_status"],
        "classification_request_emitted_count": 1,
        "authority_audit_pass_count": 1 if audit["audit_status"] == "PASS" else 0,
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
        "recommended_next": classification["recommended_next"],
    }

def profile(rollup_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_narrowing_surface_profile_v0",
        "profile_id": "target_narrowing_surface_" + sha8({"source": SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_ID, "status": rollup_obj["candidate_status"]}),
        "status": "CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_COMPLETE",
        "candidate_status": rollup_obj["candidate_status"],
        "target_candidate_declared": rollup_obj["target_candidate_declared_count"] == 1,
        "target_candidate_withheld": rollup_obj["target_candidate_withheld_count"] == 1,
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
        "schema_version": "cell1_runtime_patch_target_narrowing_surface_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_target_narrowing_design_receipt_consumed_count": 1,
        "declared_source_scan_emitted_count": 1,
        "target_candidate_record_emitted_count": rollup_obj["target_candidate_record_emitted_count"],
        "classification_request_emitted_count": rollup_obj["classification_request_emitted_count"],
        "authority_audit_pass_count": rollup_obj["authority_audit_pass_count"],
        "profile_status": profile_obj["status"],
        "candidate_status": rollup_obj["candidate_status"],
        "recommended_next_handling": rollup_obj["recommended_next"],
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

def transition_trace(classification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_narrowing_surface_transition_trace_v0",
        "trace": [
            {
                "step": "consume_target_narrowing_design",
                "question": "was a target-narrowing surface designed from the missing-target blocker",
                "answer": SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_ID,
                "taken": "scan_declared_sources",
            },
            {
                "step": "scan_declared_sources",
                "question": "is exactly one bounded target candidate visible without guessing",
                "answer": classification["candidate_status"],
                "taken": "emit_candidate_record_or_withhold",
            },
            {
                "step": "emit_candidate_record_or_withhold",
                "question": "what is the honest next handling surface",
                "answer": classification["recommended_next"],
                "taken": "stop",
            },
        ],
        "terminal": classification["terminal"],
    }

def validate_outputs(scan: Dict[str, Any], record: Dict[str, Any], classification: Dict[str, Any], request: Dict[str, Any], audit: Dict[str, Any], rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any], report_obj: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    allowed = read_json(SOURCE_TARGET_CANDIDATE_CONTRACT_PATH).get("allowed_candidate_outcomes", [])
    if classification.get("candidate_status") not in allowed:
        failures.append("candidate_status_not_allowed")
    if classification.get("runtime_patch_authorized") is not False:
        failures.append("classification_authorizes_runtime_patch")
    if classification.get("target_file_modification_authorized") is not False:
        failures.append("classification_authorizes_target_modification")
    if classification.get("c5_authorized") is not False:
        failures.append("classification_authorizes_c5")
    if classification.get("general_cell1_authority_granted") is not False:
        failures.append("classification_grants_general_cell1")
    if classification.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("classification_hidden_next_command")
    if request.get("review_only") is not True:
        failures.append("request_not_review_only")
    if request.get("accepted_for_build") is not False:
        failures.append("request_accepts_for_build")
    if request.get("runtime_patch_authorized") is not False:
        failures.append("request_authorizes_runtime_patch")
    if request.get("target_file_modification_authorized") is not False:
        failures.append("request_authorizes_target_modification")
    if request.get("next_command_goal") is not None:
        failures.append("request_hidden_next_command")
    if audit.get("audit_status") != "PASS":
        failures.append("authority_audit_not_pass")
    for key in ["may_apply_runtime_patch", "may_modify_target_files", "may_open_c5", "may_grant_general_cell1_authority", "may_use_latest_file_guessing", "may_use_mtime_selection"]:
        if audit.get("target_narrowing_authority", {}).get(key) is not False:
            failures.append(f"audit_authority_not_false:{key}")
    if scan.get("latest_file_guessing_count") != 0:
        failures.append("scan_latest_file_guessing")
    if scan.get("mtime_selection_count") != 0:
        failures.append("scan_mtime_selection")
    if scan.get("unbounded_payload_inspection_count") != 0:
        failures.append("scan_unbounded_payload_inspection")
    if classification["target_candidate_declared"] and record.get("target_ref") is None:
        failures.append("declared_candidate_missing_target_ref")
    if classification["target_candidate_withheld"] and record.get("target_ref") is not None:
        failures.append("withheld_candidate_has_target_ref")
    for key in ZERO_COUNTER_KEYS:
        if rollup_obj.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup_obj.get(key)}")
    if rollup_obj.get("target_candidate_record_emitted_count") != 1:
        failures.append("target_candidate_record_count_not_one")
    if rollup_obj.get("classification_request_emitted_count") != 1:
        failures.append("classification_request_count_not_one")
    if profile_obj.get("runtime_patch_applied") is not False:
        failures.append("profile_claims_runtime_patch")
    if profile_obj.get("target_file_modified") is not False:
        failures.append("profile_claims_target_file_modified")
    if profile_obj.get("c5_opened") is not False:
        failures.append("profile_claims_c5")
    if profile_obj.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")
    for key in [
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
    if terminal.get("stop_code") != "STOP_CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_COMPLETE":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    scan = read_json(DECLARED_SOURCE_SCAN_PATH)
    record = read_json(TARGET_CANDIDATE_RECORD_PATH)
    classification = read_json(TARGET_CANDIDATE_CLASSIFICATION_PATH)
    request = read_json(CLASSIFICATION_REQUEST_PATH)
    audit = read_json(AUTHORITY_AUDIT_PATH)
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

    bad_classification = copy.deepcopy(classification)
    bad_classification["candidate_status"] = "NOT_ALLOWED"
    add("candidate_status_not_allowed_fail", validate_outputs(scan, record, bad_classification, request, audit, rollup_obj, profile_obj, report_obj), "candidate_status_not_allowed")

    bad_classification = copy.deepcopy(classification)
    bad_classification["runtime_patch_authorized"] = True
    add("classification_authorizes_runtime_patch_fail", validate_outputs(scan, record, bad_classification, request, audit, rollup_obj, profile_obj, report_obj), "classification_authorizes_runtime_patch")

    bad_classification = copy.deepcopy(classification)
    bad_classification["target_file_modification_authorized"] = True
    add("classification_authorizes_target_modification_fail", validate_outputs(scan, record, bad_classification, request, audit, rollup_obj, profile_obj, report_obj), "classification_authorizes_target_modification")

    bad_classification = copy.deepcopy(classification)
    bad_classification["terminal"]["next_command_goal"] = "RUN_PATCH"
    add("classification_hidden_next_command_fail", validate_outputs(scan, record, bad_classification, request, audit, rollup_obj, profile_obj, report_obj), "classification_hidden_next_command")

    bad_request = copy.deepcopy(request)
    bad_request["accepted_for_build"] = True
    add("request_accepts_for_build_fail", validate_outputs(scan, record, classification, bad_request, audit, rollup_obj, profile_obj, report_obj), "request_accepts_for_build")

    bad_request = copy.deepcopy(request)
    bad_request["runtime_patch_authorized"] = True
    add("request_authorizes_runtime_patch_fail", validate_outputs(scan, record, classification, bad_request, audit, rollup_obj, profile_obj, report_obj), "request_authorizes_runtime_patch")

    for case, key, expected in [
        ("audit_authority_allows_runtime_patch_fail", "may_apply_runtime_patch", "audit_authority_not_false:may_apply_runtime_patch"),
        ("audit_authority_allows_target_file_modification_fail", "may_modify_target_files", "audit_authority_not_false:may_modify_target_files"),
        ("audit_authority_allows_c5_fail", "may_open_c5", "audit_authority_not_false:may_open_c5"),
        ("audit_authority_allows_latest_file_guessing_fail", "may_use_latest_file_guessing", "audit_authority_not_false:may_use_latest_file_guessing"),
        ("audit_authority_allows_mtime_selection_fail", "may_use_mtime_selection", "audit_authority_not_false:may_use_mtime_selection"),
    ]:
        bad_audit = copy.deepcopy(audit)
        bad_audit["target_narrowing_authority"][key] = True
        add(case, validate_outputs(scan, record, classification, request, bad_audit, rollup_obj, profile_obj, report_obj), expected)

    for case, key, expected in [
        ("scan_latest_file_guessing_fail", "latest_file_guessing_count", "scan_latest_file_guessing"),
        ("scan_mtime_selection_fail", "mtime_selection_count", "scan_mtime_selection"),
        ("scan_unbounded_payload_inspection_fail", "unbounded_payload_inspection_count", "scan_unbounded_payload_inspection"),
    ]:
        bad_scan = copy.deepcopy(scan)
        bad_scan[key] = 1
        add(case, validate_outputs(bad_scan, record, classification, request, audit, rollup_obj, profile_obj, report_obj), expected)

    if classification.get("target_candidate_withheld") is True:
        bad_record = copy.deepcopy(record)
        bad_record["target_ref"] = "src/fake.py"
        add("withheld_candidate_has_target_ref_fail", validate_outputs(scan, bad_record, classification, request, audit, rollup_obj, profile_obj, report_obj), "withheld_candidate_has_target_ref")
    else:
        bad_record = copy.deepcopy(record)
        bad_record["target_ref"] = None
        add("declared_candidate_missing_target_ref_fail", validate_outputs(scan, bad_record, classification, request, audit, rollup_obj, profile_obj, report_obj), "declared_candidate_missing_target_ref")

    for case, counter in [
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
        add(case, validate_outputs(scan, record, classification, request, audit, bad_rollup, profile_obj, bad_report), counter)

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_EVIDENCE_REQUEST_REQUIRED", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "cell1_runtime_patch_target_narrowing_surface_receipt_v0",
            "receipt_type": "CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_RECEIPT",
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
        print(f"target_narrowing_surface_receipt_id={receipt_id}")
        print(f"target_narrowing_surface_receipt_path=data/cell1_runtime_patch_target_narrowing_surface_run_v0_receipts/{receipt_id}.json")
        return 1

    design_readout_obj = design_readout()
    scan = declared_source_target_hint_scan()
    record = target_candidate_record(scan)
    classification = classify_candidate(record, scan)
    request = classification_request(record, classification)
    audit = authority_audit(record, classification)
    rollup_obj = rollup(scan, record, classification, audit)
    profile_obj = profile(rollup_obj)
    report_obj = report(rollup_obj, profile_obj)
    trace = transition_trace(classification)

    write_json(SOURCE_SURFACE_PATH, source_surface())
    write_json(DESIGN_READOUT_PATH, design_readout_obj)
    write_json(DECLARED_SOURCE_SCAN_PATH, scan)
    write_json(TARGET_CANDIDATE_RECORD_PATH, record)
    write_json(TARGET_CANDIDATE_CLASSIFICATION_PATH, classification)
    write_json(CLASSIFICATION_REQUEST_PATH, request)
    write_json(AUTHORITY_AUDIT_PATH, audit)
    write_json(ROLLUP_PATH, rollup_obj)
    write_json(PROFILE_PATH, profile_obj)
    write_json(REPORT_PATH, report_obj)
    write_json(TRANSITION_TRACE_PATH, trace)

    failures.extend(validate_outputs(scan, record, classification, request, audit, rollup_obj, profile_obj, report_obj))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup_obj["source_mutation_count"] = 1
        report_obj["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup_obj)
        write_json(REPORT_PATH, report_obj)

    acceptance_gate_results = {
        "TARGET_NARROWING_RUN_0_DESIGN_RECEIPT_CONSUMED": SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_PATH.exists(),
        "TARGET_NARROWING_RUN_1_CONTRACT_CONSUMED": SOURCE_TARGET_CANDIDATE_CONTRACT_PATH.exists(),
        "TARGET_NARROWING_RUN_2_PRECHECK_BLOCKER_CONSUMED": SOURCE_PRECHECK_CLASSIFICATION_PATH.exists(),
        "TARGET_NARROWING_RUN_3_DECLARED_SOURCE_SCAN_EMITTED": DECLARED_SOURCE_SCAN_PATH.exists(),
        "TARGET_NARROWING_RUN_4_CANDIDATE_RECORD_EMITTED": TARGET_CANDIDATE_RECORD_PATH.exists(),
        "TARGET_NARROWING_RUN_5_CLASSIFICATION_EMITTED": TARGET_CANDIDATE_CLASSIFICATION_PATH.exists(),
        "TARGET_NARROWING_RUN_6_CLASSIFICATION_REQUEST_EMITTED": CLASSIFICATION_REQUEST_PATH.exists(),
        "TARGET_NARROWING_RUN_7_AUTHORITY_AUDIT_PASS": audit["audit_status"] == "PASS",
        "TARGET_NARROWING_RUN_8_OUTCOME_CLOSED_ENUM": classification["candidate_status"] in read_json(SOURCE_TARGET_CANDIDATE_CONTRACT_PATH).get("allowed_candidate_outcomes", []),
        "TARGET_NARROWING_RUN_9_NO_RUNTIME_PATCH": rollup_obj["runtime_patch_applied_count"] == 0,
        "TARGET_NARROWING_RUN_10_NO_TARGET_FILE_MODIFICATION": rollup_obj["target_file_modified_count"] == 0,
        "TARGET_NARROWING_RUN_11_NO_C5_OPENED": rollup_obj["c5_opened_count"] == 0,
        "TARGET_NARROWING_RUN_12_NO_GENERAL_CELL1_AUTHORITY": rollup_obj["general_cell1_authority_granted_count"] == 0,
        "TARGET_NARROWING_RUN_13_NO_PROPOSAL_PROMOTION": rollup_obj["proposal_status_promoted_count"] == 0,
        "TARGET_NARROWING_RUN_14_NO_ACCEPTED_PROPOSAL_FABRICATION": rollup_obj["accepted_proposal_fabricated_count"] == 0,
        "TARGET_NARROWING_RUN_15_NO_UNBOUNDED_PAYLOAD_INSPECTION": rollup_obj["unbounded_payload_inspection_count"] == 0,
        "TARGET_NARROWING_RUN_16_NO_LATEST_FILE_GUESSING": rollup_obj["latest_file_guessing_count"] == 0,
        "TARGET_NARROWING_RUN_17_NO_MTIME_SELECTION": rollup_obj["mtime_selection_count"] == 0,
        "TARGET_NARROWING_RUN_18_NO_HIDDEN_NEXT_COMMAND": rollup_obj["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
        "TARGET_NARROWING_RUN_19_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    for gate_name, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate_name}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_design": SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_ID,
        "candidate_status": classification["candidate_status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "design_readout": rel(DESIGN_READOUT_PATH),
        "declared_source_target_hint_scan": rel(DECLARED_SOURCE_SCAN_PATH),
        "target_candidate_record": rel(TARGET_CANDIDATE_RECORD_PATH),
        "target_candidate_classification": rel(TARGET_CANDIDATE_CLASSIFICATION_PATH),
        "classification_request": rel(CLASSIFICATION_REQUEST_PATH),
        "authority_audit": rel(AUTHORITY_AUDIT_PATH),
        "rollup": rel(ROLLUP_PATH),
        "profile": rel(PROFILE_PATH),
        "report": rel(REPORT_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_target_narrowing_design_receipt": rel(SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_PATH),
        "source_target_candidate_contract": rel(SOURCE_TARGET_CANDIDATE_CONTRACT_PATH),
        "source_precheck_receipt": rel(SOURCE_PRECHECK_RECEIPT_PATH),
        "source_precheck_classification": rel(SOURCE_PRECHECK_CLASSIFICATION_PATH),
        "source_accepted_proposal_packet": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
    }

    guards = {
        "build_mode_bounded_target_narrowing_surface_only": BUILD_MODE == "BOUNDED_TARGET_NARROWING_SURFACE_ONLY",
        "candidate_status": classification["candidate_status"],
        "target_candidate_declared": classification["target_candidate_declared"],
        "target_candidate_withheld": classification["target_candidate_withheld"],
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "unbounded_payload_inspection": False,
        "hidden_next_command": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
    }

    receipt = {
        "schema_version": "cell1_runtime_patch_target_narrowing_surface_receipt_v0",
        "receipt_type": "CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "bounded Cell1 runtime patch target narrowing surface",
        "source_target_narrowing_design_receipt_id": SOURCE_TARGET_NARROWING_DESIGN_RECEIPT_ID,
        "source_precheck_receipt_id": SOURCE_PRECHECK_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_handoff_return_close_receipt_id": SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID,
        "source_schema_close_receipt_id": SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "target_narrowing_surface_summary": {
            "profile_status": profile_obj["status"],
            "candidate_status": classification["candidate_status"],
            "target_candidate_declared": classification["target_candidate_declared"],
            "target_candidate_withheld": classification["target_candidate_withheld"],
            "hint_count": rollup_obj["hint_count"],
            "bounded_hint_count": rollup_obj["bounded_hint_count"],
            "existing_bounded_hint_count": rollup_obj["existing_bounded_hint_count"],
            "target_ref": classification["target_ref"],
            "recommended_next": rollup_obj["recommended_next"],
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "general_cell1_authority_granted": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": profile_obj["bad_counters_zero"],
        },
        "aggregate_metrics": {
            **{k: v for k, v in report_obj.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
            "rollup": rollup_obj,
            "source_mutation_count": 1 if source_mutation_detected else report_obj["source_mutation_count"],
        },
        "acceptance_gate_results": acceptance_gate_results,
        "target_narrowing_surface_guards": guards,
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
    if len(negative_controls) != 28 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
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
    print(f"target_narrowing_surface_receipt_id={receipt_id}")
    print(f"target_narrowing_surface_receipt_path=data/cell1_runtime_patch_target_narrowing_surface_run_v0_receipts/{receipt_id}.json")
    print(f"target_narrowing_surface_candidate_path=data/cell1_runtime_patch_target_narrowing_surface_run_v0/target_candidate_record_v0.json")
    print(f"target_narrowing_surface_classification_path=data/cell1_runtime_patch_target_narrowing_surface_run_v0/target_candidate_classification_v0.json")
    print(f"target_narrowing_surface_rollup_path=data/cell1_runtime_patch_target_narrowing_surface_run_v0/target_narrowing_surface_rollup_v0.json")
    print(f"target_narrowing_surface_profile_path=data/cell1_runtime_patch_target_narrowing_surface_run_v0/target_narrowing_surface_profile_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
