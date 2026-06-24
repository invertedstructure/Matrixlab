#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RUN_CELL1_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK_FROM_DESIGN_V0"
TARGET_UNIT_ID = "cell1.minimal_runtime_patch_test_precheck.run_from_design.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TEST_PRECHECK"
MODE = "RUN / ELIGIBILITY_PRECHECK / NO_PATCH"
BUILD_MODE = "BOUNDED_RUNTIME_PATCH_ELIGIBILITY_PRECHECK_ONLY"

SOURCE_PRECHECK_DESIGN_RECEIPT_ID = "a62d6ec2"
SOURCE_PRECHECK_DESIGN_RECEIPT_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_design_v0_receipts" / "a62d6ec2.json"
SOURCE_PRECHECK_DESIGN_RECORD_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_design_v0" / "runtime_patch_precheck_design_record_v0.json"
SOURCE_PRECHECK_CONTRACT_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_design_v0" / "runtime_patch_precheck_eligibility_contract_v0.json"
SOURCE_PRECHECK_TEST_PLAN_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_design_v0" / "runtime_patch_precheck_test_plan_v0.json"
SOURCE_PRECHECK_AUTHORITY_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_design_v0" / "runtime_patch_precheck_design_authority_boundary_v0.json"
SOURCE_PRECHECK_ROLLUP_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_design_v0" / "runtime_patch_precheck_design_rollup_v0.json"
SOURCE_PRECHECK_PROFILE_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_design_v0" / "runtime_patch_precheck_design_profile_v0.json"
SOURCE_PRECHECK_STACK_READOUT_PATH = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_design_v0" / "reference_stack_readout_v0.json"

SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_ID = "f595a9a6"
SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_PATH = ROOT / "data" / "cell1_next_bounded_objective_after_return_loop_v0_receipts" / "f595a9a6.json"
SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_DECISION_PATH = ROOT / "data" / "cell1_next_bounded_objective_after_return_loop_v0" / "objective_decision_record_v0.json"

SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID = "1d7c0a9b"
SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH = ROOT / "data" / "cell1_handoff_return_loop_review_or_close_v0_receipts" / "1d7c0a9b.json"
SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH = ROOT / "data" / "cell1_handoff_return_loop_review_or_close_v0" / "handoff_return_loop_frozen_reference_packet_v0.json"

SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID = "e1bc0ed0"
SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0_receipts" / "e1bc0ed0.json"
SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0" / "cell1_schema_test_frozen_reference_packet_v0.json"

SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID = "71bd1d92"
SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0_receipts" / "71bd1d92.json"
SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0" / "accepted_proposal_packet_v0.json"
SOURCE_ACCEPTED_PROPOSAL_REVIEW_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0" / "review_decision_record_v0.json"

SOURCE_C1_PATCH_RECEIPT_ID = "fffa3dd5"
SOURCE_C1_PATCH_RECEIPT_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0_receipts" / "fffa3dd5.json"
SOURCE_C1_PATCH_SCHEMA_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0" / "proposal_packet_schema_v0_1.json"

SOURCE_C2_RECEIPT_ID = "348dabde"
SOURCE_C2_RECEIPT_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts" / "348dabde.json"
SOURCE_C2_LANE_REGISTRY_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "taxonomy_lane_registry_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_PRECHECK_DESIGN_RECEIPT_PATH,
    SOURCE_PRECHECK_DESIGN_RECORD_PATH,
    SOURCE_PRECHECK_CONTRACT_PATH,
    SOURCE_PRECHECK_TEST_PLAN_PATH,
    SOURCE_PRECHECK_AUTHORITY_PATH,
    SOURCE_PRECHECK_ROLLUP_PATH,
    SOURCE_PRECHECK_PROFILE_PATH,
    SOURCE_PRECHECK_STACK_READOUT_PATH,
    SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_PATH,
    SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_DECISION_PATH,
    SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH,
    SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH,
    SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_PATH,
    SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH,
    SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH,
    SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH,
    SOURCE_ACCEPTED_PROPOSAL_REVIEW_PATH,
    SOURCE_C1_PATCH_RECEIPT_PATH,
    SOURCE_C1_PATCH_SCHEMA_PATH,
    SOURCE_C2_RECEIPT_PATH,
    SOURCE_C2_LANE_REGISTRY_PATH,
]

OUT_DIR = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_run_v0"
RECEIPT_DIR = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_run_v0_receipts"

SOURCE_SURFACE_PATH = OUT_DIR / "source_surface_v0.json"
DESIGN_READOUT_PATH = OUT_DIR / "precheck_design_readout_v0.json"
ELIGIBILITY_EVIDENCE_PATH = OUT_DIR / "runtime_patch_precheck_eligibility_evidence_v0.json"
BOUNDED_TARGET_CANDIDATE_SCAN_PATH = OUT_DIR / "bounded_runtime_patch_target_candidate_scan_v0.json"
VERIFICATION_GATE_SCAN_PATH = OUT_DIR / "verification_gate_scan_v0.json"
ROLLBACK_OR_STOP_SCAN_PATH = OUT_DIR / "rollback_or_stop_boundary_scan_v0.json"
ELIGIBILITY_CLASSIFICATION_PATH = OUT_DIR / "runtime_patch_precheck_eligibility_classification_v0.json"
AUTHORITY_AUDIT_PATH = OUT_DIR / "runtime_patch_precheck_authority_audit_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_patch_precheck_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_patch_precheck_profile_v0.json"
REPORT_PATH = OUT_DIR / "runtime_patch_precheck_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "runtime_patch_precheck_transition_trace.json"

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
]

HUMAN_DECISION = {
    "decision": "RUN_CELL1_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK_FROM_DESIGN",
    "scope": "Run the bounded eligibility precheck from the accepted design. The precheck inspects only declared source artifacts for accepted proposal, bounded target candidate, verification gate, rollback-or-stop boundary, authority boundary, and return/review surface. It emits eligibility evidence, classification, audit, rollup, profile, report, transition trace, and receipt. It does not apply a runtime patch, modify target files, open C5, grant general Cell1 authority, promote proposals, fabricate accepted proposals, or emit hidden next command.",
    "authorized": [
        "consume precheck design receipt",
        "consume eligibility contract",
        "consume accepted proposal packet",
        "inspect declared artifacts for bounded eligibility evidence",
        "emit eligibility classification",
        "emit authority audit",
        "emit receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "apply runtime patch",
        "modify target files",
        "open C5",
        "grant general Cell1 authority",
        "mutate taxonomy registry",
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

def normalize_ref_value(v: Any) -> str:
    if isinstance(v, str):
        return v.strip()
    return ""

def is_local_file_candidate(value: str) -> bool:
    if not value:
        return False
    if value.startswith(("http://", "https://", "s3://", "gs://")):
        return False
    if ".." in Path(value).parts:
        return False
    return (
        value.endswith((".py", ".json", ".jsonl", ".txt", ".md", ".yaml", ".yml"))
        or value.startswith(("src/", "scripts/", "data/", "app/"))
    )

def validate_source_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    design_receipt = read_json(SOURCE_PRECHECK_DESIGN_RECEIPT_PATH)
    design = read_json(SOURCE_PRECHECK_DESIGN_RECORD_PATH)
    contract = read_json(SOURCE_PRECHECK_CONTRACT_PATH)
    plan = read_json(SOURCE_PRECHECK_TEST_PLAN_PATH)
    authority = read_json(SOURCE_PRECHECK_AUTHORITY_PATH)
    design_rollup = read_json(SOURCE_PRECHECK_ROLLUP_PATH)
    design_profile = read_json(SOURCE_PRECHECK_PROFILE_PATH)
    stack = read_json(SOURCE_PRECHECK_STACK_READOUT_PATH)
    next_receipt = read_json(SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_PATH)
    next_decision = read_json(SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_DECISION_PATH)
    return_receipt = read_json(SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH)
    return_reference = read_json(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH)
    schema_receipt = read_json(SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_PATH)
    schema_reference = read_json(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH)
    accepted_receipt = read_json(SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH)
    accepted_packet = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    c1_receipt = read_json(SOURCE_C1_PATCH_RECEIPT_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)

    if design_receipt.get("receipt_id") != SOURCE_PRECHECK_DESIGN_RECEIPT_ID or design_receipt.get("gate") != "PASS":
        failures.append("precheck_design_receipt_not_pass")
    if design_receipt.get("terminal", {}).get("stop_code") != "STOP_CELL1_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK_DESIGNED":
        failures.append("precheck_design_wrong_terminal")
    if design.get("future_precheck_unit") != UNIT_ID:
        failures.append("design_future_precheck_unit_wrong")
    if contract.get("precheck_object_type") != "CELL1_MINIMAL_RUNTIME_PATCH_TEST_ELIGIBILITY_PRECHECK":
        failures.append("contract_precheck_object_wrong")
    if contract.get("authority_boundary", {}).get("may_apply_runtime_patch") is not False:
        failures.append("contract_allows_runtime_patch")
    if contract.get("authority_boundary", {}).get("may_modify_target_files") is not False:
        failures.append("contract_allows_target_modification")
    if contract.get("authority_boundary", {}).get("may_open_c5") is not False:
        failures.append("contract_allows_c5")
    if plan.get("future_precheck_unit") != UNIT_ID:
        failures.append("plan_future_precheck_unit_wrong")
    if plan.get("test_mode") != "BOUNDED_RUNTIME_PATCH_ELIGIBILITY_PRECHECK_ONLY":
        failures.append("plan_test_mode_wrong")
    if plan.get("next_command_goal") is not None:
        failures.append("plan_hidden_next_command")
    if authority.get("may_run_precheck_now") is not False:
        failures.append("design_authority_claims_precheck_now")
    if authority.get("may_apply_runtime_patch") is not False:
        failures.append("design_authority_allows_runtime_patch")
    if authority.get("may_modify_target_files") is not False:
        failures.append("design_authority_allows_target_modification")
    if authority.get("may_open_c5") is not False:
        failures.append("design_authority_allows_c5")
    if design_rollup.get("precheck_executed_count") != 0:
        failures.append("design_rollup_precheck_already_executed")
    if design_profile.get("status") != "CELL1_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK_DESIGNED":
        failures.append("design_profile_not_designed")
    if stack.get("schema_consumption_reference", {}).get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("stack_schema_reference_not_frozen")
    if stack.get("handoff_return_reference", {}).get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("stack_return_reference_not_frozen")
    if stack.get("accepted_proposal", {}).get("status") != "ACCEPTED_FOR_BUILD":
        failures.append("stack_accepted_proposal_not_accepted")
    if next_receipt.get("receipt_id") != SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_ID or next_receipt.get("gate") != "PASS":
        failures.append("after_return_next_objective_receipt_not_pass")
    if next_decision.get("selected_decision_class") != "CELL1_OBJECTIVE_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK":
        failures.append("after_return_next_objective_selected_wrong")
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
        "schema_version": "cell1_minimal_runtime_patch_precheck_source_surface_v0",
        "source_precheck_design_receipt_id": SOURCE_PRECHECK_DESIGN_RECEIPT_ID,
        "source_precheck_design_receipt_ref": rel(SOURCE_PRECHECK_DESIGN_RECEIPT_PATH),
        "source_precheck_design_record_ref": rel(SOURCE_PRECHECK_DESIGN_RECORD_PATH),
        "source_precheck_contract_ref": rel(SOURCE_PRECHECK_CONTRACT_PATH),
        "source_accepted_proposal_packet_ref": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "source_schema_reference_packet_ref": rel(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH),
        "source_handoff_return_reference_packet_ref": rel(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH),
        "surface_status": "EXPLICIT_RUNTIME_PATCH_ELIGIBILITY_PRECHECK_RUN_SURFACE",
    }

def design_readout() -> Dict[str, Any]:
    design = read_json(SOURCE_PRECHECK_DESIGN_RECORD_PATH)
    contract = read_json(SOURCE_PRECHECK_CONTRACT_PATH)
    plan = read_json(SOURCE_PRECHECK_TEST_PLAN_PATH)
    return {
        "schema_version": "cell1_minimal_runtime_patch_precheck_design_readout_v0",
        "design_id": design.get("design_id"),
        "contract_id": contract.get("contract_id"),
        "future_precheck_unit": plan.get("future_precheck_unit"),
        "precheck_object_type": contract.get("precheck_object_type"),
        "required_eligibility_fields": contract.get("required_eligibility_fields", []),
        "eligibility_questions": contract.get("eligibility_questions", []),
        "allowed_precheck_outcomes": contract.get("allowed_precheck_outcomes", []),
    }

def scan_bounded_target_candidates() -> Dict[str, Any]:
    accepted = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    design = read_json(SOURCE_PRECHECK_DESIGN_RECORD_PATH)
    c4_handoff_candidates = []
    c4_handoff_path = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0" / "cell1_handoff_packet_v0.json"
    if c4_handoff_path.exists():
        try:
            c4_handoff_candidates = list(iter_json_paths(read_json(c4_handoff_path)))
        except Exception:
            c4_handoff_candidates = []

    candidates: List[Dict[str, Any]] = []
    allowed_sources = [
        ("accepted_proposal_packet", accepted),
        ("precheck_design_record", design),
    ]

    for source_name, obj in allowed_sources:
        for path, value in iter_json_paths(obj):
            k = keyish(path)
            v = normalize_ref_value(value)
            if not isinstance(value, str):
                continue
            if "target" in k and is_local_file_candidate(v):
                candidates.append({
                    "source": source_name,
                    "json_path": path,
                    "candidate_ref": v,
                    "reason": "target-key-local-file-candidate",
                })
            elif "patch-target" in k or "runtime-patch-target" in k:
                if v:
                    candidates.append({
                        "source": source_name,
                        "json_path": path,
                        "candidate_ref": v,
                        "reason": "explicit-runtime-patch-target-key",
                    })

    for path, value in c4_handoff_candidates:
        k = keyish(path)
        v = normalize_ref_value(value)
        if isinstance(value, str) and "target" in k and is_local_file_candidate(v):
            candidates.append({
                "source": "c4_handoff_packet",
                "json_path": path,
                "candidate_ref": v,
                "reason": "handoff-target-local-file-candidate",
            })

    unique = []
    seen = set()
    for c in candidates:
        key = (c["candidate_ref"], c["source"], c["json_path"])
        if key not in seen:
            seen.add(key)
            unique.append(c)

    bounded_candidates = []
    for c in unique:
        ref = c["candidate_ref"]
        bounded = is_local_file_candidate(ref) and not Path(ref).is_absolute()
        exists = (ROOT / ref).exists()
        bounded_candidates.append({
            **c,
            "bounded": bounded,
            "exists_now": exists,
            "may_modify_during_precheck": False,
        })

    return {
        "schema_version": "bounded_runtime_patch_target_candidate_scan_v0",
        "scan_id": "bounded_target_scan_" + sha8({"source": SOURCE_PRECHECK_DESIGN_RECEIPT_ID, "n": len(bounded_candidates)}),
        "allowed_sources_scanned": [
            rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
            rel(SOURCE_PRECHECK_DESIGN_RECORD_PATH),
            "data/c4_consume_one_accepted_proposal_packet_v0/cell1_handoff_packet_v0.json",
        ],
        "unbounded_payload_inspection_count": 0,
        "candidate_count": len(bounded_candidates),
        "bounded_candidate_count": sum(1 for c in bounded_candidates if c["bounded"]),
        "existing_bounded_candidate_count": sum(1 for c in bounded_candidates if c["bounded"] and c["exists_now"]),
        "exactly_one_bounded_target": sum(1 for c in bounded_candidates if c["bounded"]) == 1,
        "candidates": bounded_candidates,
        "scan_status": "PASS" if sum(1 for c in bounded_candidates if c["bounded"]) == 1 else "BLOCKED_MISSING_BOUNDED_TARGET",
    }

def scan_verification_gate() -> Dict[str, Any]:
    sources = {
        "accepted_proposal_packet": read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "precheck_design_record": read_json(SOURCE_PRECHECK_DESIGN_RECORD_PATH),
        "eligibility_contract": read_json(SOURCE_PRECHECK_CONTRACT_PATH),
        "precheck_test_plan": read_json(SOURCE_PRECHECK_TEST_PLAN_PATH),
    }
    hits: List[Dict[str, Any]] = []
    for source, obj in sources.items():
        for path, value in iter_json_paths(obj):
            k = keyish(path)
            v = str(value).lower() if isinstance(value, str) else ""
            if ("verification" in k or "gate" in k or "acceptance" in k) and value not in (None, "", [], {}):
                hits.append({
                    "source": source,
                    "json_path": path,
                    "value_sig8": sha8(value),
                    "reason": "verification-or-gate-surface",
                })
            elif isinstance(value, str) and ("verification gate" in v or "acceptance gate" in v):
                hits.append({
                    "source": source,
                    "json_path": path,
                    "value_sig8": sha8(value),
                    "reason": "verification-gate-text-surface",
                })
    return {
        "schema_version": "runtime_patch_precheck_verification_gate_scan_v0",
        "scan_id": "verification_gate_scan_" + sha8({"hits": hits}),
        "allowed_sources_scanned": list(sources.keys()),
        "hit_count": len(hits),
        "verification_gate_declared": len(hits) > 0,
        "hits": hits,
        "scan_status": "PASS" if hits else "BLOCKED_MISSING_VERIFICATION_GATE",
    }

def scan_rollback_or_stop_boundary() -> Dict[str, Any]:
    sources = {
        "accepted_proposal_packet": read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "precheck_design_record": read_json(SOURCE_PRECHECK_DESIGN_RECORD_PATH),
        "eligibility_contract": read_json(SOURCE_PRECHECK_CONTRACT_PATH),
        "precheck_test_plan": read_json(SOURCE_PRECHECK_TEST_PLAN_PATH),
    }
    hits: List[Dict[str, Any]] = []
    for source, obj in sources.items():
        for path, value in iter_json_paths(obj):
            k = keyish(path)
            v = str(value).lower() if isinstance(value, str) else ""
            if any(term in k for term in ["rollback", "stop", "halt", "terminal", "failure"]):
                if value not in (None, "", [], {}):
                    hits.append({
                        "source": source,
                        "json_path": path,
                        "value_sig8": sha8(value),
                        "reason": "rollback-stop-halt-terminal-surface",
                    })
            elif isinstance(value, str) and any(term in v for term in ["rollback", "stop", "halt", "terminal"]):
                hits.append({
                    "source": source,
                    "json_path": path,
                    "value_sig8": sha8(value),
                    "reason": "rollback-stop-text-surface",
                })
    return {
        "schema_version": "runtime_patch_precheck_rollback_or_stop_boundary_scan_v0",
        "scan_id": "rollback_stop_scan_" + sha8({"hits": hits}),
        "allowed_sources_scanned": list(sources.keys()),
        "hit_count": len(hits),
        "rollback_or_stop_boundary_declared": len(hits) > 0,
        "hits": hits,
        "scan_status": "PASS" if hits else "BLOCKED_MISSING_ROLLBACK_OR_STOP_BOUNDARY",
    }

def eligibility_evidence(target_scan: Dict[str, Any], verification_scan: Dict[str, Any], rollback_scan: Dict[str, Any]) -> Dict[str, Any]:
    accepted = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    contract = read_json(SOURCE_PRECHECK_CONTRACT_PATH)
    return {
        "schema_version": "cell1_minimal_runtime_patch_precheck_eligibility_evidence_v0",
        "evidence_id": "runtime_patch_precheck_evidence_" + sha8({
            "source": SOURCE_PRECHECK_DESIGN_RECEIPT_ID,
            "target": target_scan["scan_status"],
            "verification": verification_scan["scan_status"],
            "rollback": rollback_scan["scan_status"],
        }),
        "accepted_proposal": {
            "proposal_id": accepted.get("proposal_id"),
            "status": accepted.get("status"),
            "accepted_proposal_ref": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
            "accepted_for_build": accepted.get("status") == "ACCEPTED_FOR_BUILD",
        },
        "bounded_patch_target": {
            "scan_ref": rel(BOUNDED_TARGET_CANDIDATE_SCAN_PATH),
            "exactly_one_bounded_target": target_scan["exactly_one_bounded_target"],
            "bounded_candidate_count": target_scan["bounded_candidate_count"],
            "candidate_count": target_scan["candidate_count"],
        },
        "verification_gate": {
            "scan_ref": rel(VERIFICATION_GATE_SCAN_PATH),
            "declared": verification_scan["verification_gate_declared"],
            "hit_count": verification_scan["hit_count"],
        },
        "rollback_or_stop_boundary": {
            "scan_ref": rel(ROLLBACK_OR_STOP_SCAN_PATH),
            "declared": rollback_scan["rollback_or_stop_boundary_declared"],
            "hit_count": rollback_scan["hit_count"],
        },
        "authority_boundary": contract.get("authority_boundary", {}),
        "return_packet_or_review_surface": {
            "handoff_return_reference_ref": rel(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH),
            "schema_reference_ref": rel(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH),
            "available": True,
        },
        "negative_boundary_counters": {key: 0 for key in ZERO_COUNTER_KEYS},
    }

def classify_eligibility(evidence: Dict[str, Any], target_scan: Dict[str, Any], verification_scan: Dict[str, Any], rollback_scan: Dict[str, Any]) -> Dict[str, Any]:
    contract = read_json(SOURCE_PRECHECK_CONTRACT_PATH)
    failures: List[str] = []
    outcome = "ELIGIBLE_FOR_MINIMAL_RUNTIME_PATCH_TEST_DESIGN"

    if evidence["accepted_proposal"]["accepted_for_build"] is not True:
        failures.append("accepted_proposal_not_accepted_for_build")
        outcome = "BLOCKED_ACCEPTED_PROPOSAL_GAP"
    elif target_scan["exactly_one_bounded_target"] is not True:
        failures.append("missing_exactly_one_bounded_target")
        outcome = "BLOCKED_MISSING_BOUNDED_TARGET"
    elif verification_scan["verification_gate_declared"] is not True:
        failures.append("missing_verification_gate")
        outcome = "BLOCKED_MISSING_VERIFICATION_GATE"
    elif rollback_scan["rollback_or_stop_boundary_declared"] is not True:
        failures.append("missing_rollback_or_stop_boundary")
        outcome = "BLOCKED_MISSING_ROLLBACK_OR_STOP_BOUNDARY"

    boundary = contract.get("authority_boundary", {})
    if boundary.get("may_apply_runtime_patch") is not False:
        failures.append("authority_boundary_allows_runtime_patch")
        outcome = "BLOCKED_AUTHORITY_BOUNDARY"
    if boundary.get("may_modify_target_files") is not False:
        failures.append("authority_boundary_allows_target_file_modification")
        outcome = "BLOCKED_AUTHORITY_BOUNDARY"
    if boundary.get("may_open_c5") is not False:
        failures.append("authority_boundary_allows_c5")
        outcome = "BLOCKED_AUTHORITY_BOUNDARY"
    if boundary.get("may_grant_general_cell1_authority") is not False:
        failures.append("authority_boundary_allows_general_cell1")
        outcome = "BLOCKED_AUTHORITY_BOUNDARY"

    allowed = contract.get("allowed_precheck_outcomes", [])
    if outcome not in allowed:
        failures.append(f"outcome_not_allowed:{outcome}")

    if outcome == "ELIGIBLE_FOR_MINIMAL_RUNTIME_PATCH_TEST_DESIGN":
        recommended_next = "DESIGN_CELL1_MINIMAL_RUNTIME_PATCH_TEST_V0"
    elif outcome == "BLOCKED_MISSING_BOUNDED_TARGET":
        recommended_next = "DESIGN_CELL1_RUNTIME_PATCH_TARGET_NARROWING_SURFACE_V0"
    elif outcome == "BLOCKED_MISSING_VERIFICATION_GATE":
        recommended_next = "DESIGN_CELL1_RUNTIME_PATCH_VERIFICATION_GATE_SURFACE_V0"
    elif outcome == "BLOCKED_MISSING_ROLLBACK_OR_STOP_BOUNDARY":
        recommended_next = "DESIGN_CELL1_RUNTIME_PATCH_ROLLBACK_OR_STOP_SURFACE_V0"
    else:
        recommended_next = "REVIEW_CELL1_RUNTIME_PATCH_PRECHECK_BLOCKER_V0"

    return {
        "schema_version": "cell1_minimal_runtime_patch_precheck_eligibility_classification_v0",
        "classification_id": "runtime_patch_precheck_classification_" + sha8({"outcome": outcome, "failures": failures}),
        "source_precheck_design_receipt_id": SOURCE_PRECHECK_DESIGN_RECEIPT_ID,
        "eligibility_outcome": outcome,
        "classification_status": "PASS",
        "blockers": failures,
        "eligible_for_minimal_runtime_patch_test_design": outcome == "ELIGIBLE_FOR_MINIMAL_RUNTIME_PATCH_TEST_DESIGN",
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "recommended_next": recommended_next,
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CELL1_MINIMAL_RUNTIME_PATCH_PRECHECK_COMPLETE",
            "next_command_goal": None,
        },
    }

def authority_audit(classification: Dict[str, Any], evidence: Dict[str, Any]) -> Dict[str, Any]:
    counters = {key: 0 for key in ZERO_COUNTER_KEYS}
    return {
        "schema_version": "cell1_minimal_runtime_patch_precheck_authority_audit_v0",
        "audit_id": "runtime_patch_precheck_audit_" + sha8({"classification": classification["eligibility_outcome"]}),
        "source_precheck_design_receipt_id": SOURCE_PRECHECK_DESIGN_RECEIPT_ID,
        "eligibility_outcome": classification["eligibility_outcome"],
        "negative_boundary_counters": counters,
        "precheck_authority": {
            "may_classify_eligibility": True,
            "may_apply_runtime_patch": False,
            "may_modify_target_files": False,
            "may_open_c5": False,
            "may_grant_general_cell1_authority": False,
            "may_promote_proposal_status": False,
            "may_fabricate_accepted_proposal": False,
        },
        "evidence_boundary": evidence["authority_boundary"],
        "audit_status": "PASS" if all(v == 0 for v in counters.values()) else "FAIL",
    }

def rollup(evidence: Dict[str, Any], target_scan: Dict[str, Any], verification_scan: Dict[str, Any], rollback_scan: Dict[str, Any], classification: Dict[str, Any], audit: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_minimal_runtime_patch_precheck_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_precheck_design_receipt_id": SOURCE_PRECHECK_DESIGN_RECEIPT_ID,
        "source_after_return_next_objective_receipt_id": SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_ID,
        "source_handoff_return_close_receipt_id": SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID,
        "source_schema_close_receipt_id": SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "accepted_proposal_present_count": 1 if evidence["accepted_proposal"]["accepted_for_build"] else 0,
        "bounded_target_candidate_count": target_scan["bounded_candidate_count"],
        "exactly_one_bounded_target_count": 1 if target_scan["exactly_one_bounded_target"] else 0,
        "verification_gate_declared_count": 1 if verification_scan["verification_gate_declared"] else 0,
        "rollback_or_stop_boundary_declared_count": 1 if rollback_scan["rollback_or_stop_boundary_declared"] else 0,
        "return_review_surface_available_count": 1 if evidence["return_packet_or_review_surface"]["available"] else 0,
        "eligibility_classification_count": 1,
        "eligibility_outcome": classification["eligibility_outcome"],
        "eligible_for_minimal_runtime_patch_test_design_count": 1 if classification["eligible_for_minimal_runtime_patch_test_design"] else 0,
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
        "recommended_next": classification["recommended_next"],
    }

def profile(rollup_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_minimal_runtime_patch_precheck_profile_v0",
        "profile_id": "runtime_patch_precheck_" + sha8({"source": SOURCE_PRECHECK_DESIGN_RECEIPT_ID, "outcome": rollup_obj["eligibility_outcome"]}),
        "status": "CELL1_MINIMAL_RUNTIME_PATCH_PRECHECK_COMPLETE",
        "eligibility_outcome": rollup_obj["eligibility_outcome"],
        "eligible_for_minimal_runtime_patch_test_design": rollup_obj["eligible_for_minimal_runtime_patch_test_design_count"] == 1,
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
        "schema_version": "cell1_minimal_runtime_patch_precheck_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_precheck_design_receipt_consumed_count": 1,
        "eligibility_evidence_emitted_count": 1,
        "target_candidate_scan_emitted_count": 1,
        "verification_gate_scan_emitted_count": 1,
        "rollback_or_stop_scan_emitted_count": 1,
        "eligibility_classification_emitted_count": 1,
        "authority_audit_emitted_count": 1,
        "profile_status": profile_obj["status"],
        "eligibility_outcome": rollup_obj["eligibility_outcome"],
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
        "schema_version": "cell1_minimal_runtime_patch_precheck_transition_trace_v0",
        "trace": [
            {
                "step": "consume_precheck_design",
                "question": "is a valid runtime-patch eligibility precheck design available",
                "answer": SOURCE_PRECHECK_DESIGN_RECEIPT_ID,
                "taken": "inspect_accepted_proposal",
            },
            {
                "step": "inspect_accepted_proposal",
                "question": "does an accepted proposal packet exist",
                "answer": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
                "taken": "scan_bounded_target",
            },
            {
                "step": "scan_bounded_target",
                "question": "is exactly one bounded runtime patch target candidate visible in declared sources",
                "answer": classification["eligibility_outcome"],
                "taken": "classify_eligibility",
            },
            {
                "step": "classify_eligibility",
                "question": "what is the smallest honest next handling surface",
                "answer": classification["recommended_next"],
                "taken": "stop",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CELL1_MINIMAL_RUNTIME_PATCH_PRECHECK_COMPLETE",
            "next_command_goal": None,
        },
    }

def validate_outputs(evidence: Dict[str, Any], target_scan: Dict[str, Any], verification_scan: Dict[str, Any], rollback_scan: Dict[str, Any], classification: Dict[str, Any], audit: Dict[str, Any], rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any], report_obj: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    allowed = read_json(SOURCE_PRECHECK_CONTRACT_PATH).get("allowed_precheck_outcomes", [])
    if classification.get("eligibility_outcome") not in allowed:
        failures.append("classification_outcome_not_allowed")
    if classification.get("classification_status") != "PASS":
        failures.append("classification_not_pass")
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
    if audit.get("audit_status") != "PASS":
        failures.append("authority_audit_not_pass")
    if audit.get("precheck_authority", {}).get("may_apply_runtime_patch") is not False:
        failures.append("audit_authority_allows_runtime_patch")
    if audit.get("precheck_authority", {}).get("may_modify_target_files") is not False:
        failures.append("audit_authority_allows_target_modification")
    if audit.get("precheck_authority", {}).get("may_open_c5") is not False:
        failures.append("audit_authority_allows_c5")
    if evidence.get("negative_boundary_counters", {}).get("unbounded_payload_inspection_count") != 0:
        failures.append("evidence_unbounded_payload_inspection")
    if target_scan.get("unbounded_payload_inspection_count") != 0:
        failures.append("target_scan_unbounded_payload_inspection")
    for key in ZERO_COUNTER_KEYS:
        if rollup_obj.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup_obj.get(key)}")
    if rollup_obj.get("eligibility_classification_count") != 1:
        failures.append("classification_count_not_one")
    if rollup_obj.get("accepted_proposal_present_count") != 1:
        failures.append("accepted_proposal_present_count_not_one")
    if profile_obj.get("runtime_patch_applied") is not False:
        failures.append("profile_claims_runtime_patch")
    if profile_obj.get("target_file_modified") is not False:
        failures.append("profile_claims_target_file_modified")
    if profile_obj.get("c5_opened") is not False:
        failures.append("profile_claims_c5")
    if profile_obj.get("general_cell1_authority_granted") is not False:
        failures.append("profile_claims_general_cell1")
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
    if terminal.get("stop_code") != "STOP_CELL1_MINIMAL_RUNTIME_PATCH_PRECHECK_COMPLETE":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    evidence = read_json(ELIGIBILITY_EVIDENCE_PATH)
    target_scan = read_json(BOUNDED_TARGET_CANDIDATE_SCAN_PATH)
    verification_scan = read_json(VERIFICATION_GATE_SCAN_PATH)
    rollback_scan = read_json(ROLLBACK_OR_STOP_SCAN_PATH)
    classification = read_json(ELIGIBILITY_CLASSIFICATION_PATH)
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
    bad_classification["eligibility_outcome"] = "NOT_A_CLOSED_OUTCOME"
    add("classification_outcome_not_allowed_fail", validate_outputs(evidence, target_scan, verification_scan, rollback_scan, bad_classification, audit, rollup_obj, profile_obj, report_obj), "classification_outcome_not_allowed")

    bad_classification = copy.deepcopy(classification)
    bad_classification["runtime_patch_authorized"] = True
    add("classification_authorizes_runtime_patch_fail", validate_outputs(evidence, target_scan, verification_scan, rollback_scan, bad_classification, audit, rollup_obj, profile_obj, report_obj), "classification_authorizes_runtime_patch")

    bad_classification = copy.deepcopy(classification)
    bad_classification["target_file_modification_authorized"] = True
    add("classification_authorizes_target_modification_fail", validate_outputs(evidence, target_scan, verification_scan, rollback_scan, bad_classification, audit, rollup_obj, profile_obj, report_obj), "classification_authorizes_target_modification")

    bad_classification = copy.deepcopy(classification)
    bad_classification["c5_authorized"] = True
    add("classification_authorizes_c5_fail", validate_outputs(evidence, target_scan, verification_scan, rollback_scan, bad_classification, audit, rollup_obj, profile_obj, report_obj), "classification_authorizes_c5")

    bad_classification = copy.deepcopy(classification)
    bad_classification["terminal"]["next_command_goal"] = "RUN_RUNTIME_PATCH"
    add("classification_hidden_next_command_fail", validate_outputs(evidence, target_scan, verification_scan, rollback_scan, bad_classification, audit, rollup_obj, profile_obj, report_obj), "classification_hidden_next_command")

    bad_audit = copy.deepcopy(audit)
    bad_audit["precheck_authority"]["may_apply_runtime_patch"] = True
    add("audit_authority_allows_runtime_patch_fail", validate_outputs(evidence, target_scan, verification_scan, rollback_scan, classification, bad_audit, rollup_obj, profile_obj, report_obj), "audit_authority_allows_runtime_patch")

    bad_audit = copy.deepcopy(audit)
    bad_audit["precheck_authority"]["may_modify_target_files"] = True
    add("audit_authority_allows_target_modification_fail", validate_outputs(evidence, target_scan, verification_scan, rollback_scan, classification, bad_audit, rollup_obj, profile_obj, report_obj), "audit_authority_allows_target_modification")

    bad_evidence = copy.deepcopy(evidence)
    bad_evidence["negative_boundary_counters"]["unbounded_payload_inspection_count"] = 1
    add("evidence_unbounded_payload_inspection_fail", validate_outputs(bad_evidence, target_scan, verification_scan, rollback_scan, classification, audit, rollup_obj, profile_obj, report_obj), "evidence_unbounded_payload_inspection")

    bad_target_scan = copy.deepcopy(target_scan)
    bad_target_scan["unbounded_payload_inspection_count"] = 1
    add("target_scan_unbounded_payload_inspection_fail", validate_outputs(evidence, bad_target_scan, verification_scan, rollback_scan, classification, audit, rollup_obj, profile_obj, report_obj), "target_scan_unbounded_payload_inspection")

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
    ]:
        bad_rollup = copy.deepcopy(rollup_obj)
        bad_report = copy.deepcopy(report_obj)
        bad_rollup[counter] = 1
        if counter in bad_report:
            bad_report[counter] = 1
        add(case, validate_outputs(evidence, target_scan, verification_scan, rollback_scan, classification, audit, bad_rollup, profile_obj, bad_report), counter)

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_CELL1_MINIMAL_RUNTIME_PATCH_PRECHECK_EVIDENCE_REQUEST_REQUIRED", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "cell1_minimal_runtime_patch_precheck_receipt_v0",
            "receipt_type": "CELL1_MINIMAL_RUNTIME_PATCH_PRECHECK_RECEIPT",
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
        print(f"minimal_runtime_patch_precheck_receipt_id={receipt_id}")
        print(f"minimal_runtime_patch_precheck_receipt_path=data/cell1_minimal_runtime_patch_test_precheck_run_v0_receipts/{receipt_id}.json")
        return 1

    design_readout_obj = design_readout()
    target_scan = scan_bounded_target_candidates()
    verification_scan = scan_verification_gate()
    rollback_scan = scan_rollback_or_stop_boundary()
    evidence = eligibility_evidence(target_scan, verification_scan, rollback_scan)
    classification = classify_eligibility(evidence, target_scan, verification_scan, rollback_scan)
    audit = authority_audit(classification, evidence)
    rollup_obj = rollup(evidence, target_scan, verification_scan, rollback_scan, classification, audit)
    profile_obj = profile(rollup_obj)
    report_obj = report(rollup_obj, profile_obj)
    trace = transition_trace(classification)

    write_json(SOURCE_SURFACE_PATH, source_surface())
    write_json(DESIGN_READOUT_PATH, design_readout_obj)
    write_json(BOUNDED_TARGET_CANDIDATE_SCAN_PATH, target_scan)
    write_json(VERIFICATION_GATE_SCAN_PATH, verification_scan)
    write_json(ROLLBACK_OR_STOP_SCAN_PATH, rollback_scan)
    write_json(ELIGIBILITY_EVIDENCE_PATH, evidence)
    write_json(ELIGIBILITY_CLASSIFICATION_PATH, classification)
    write_json(AUTHORITY_AUDIT_PATH, audit)
    write_json(ROLLUP_PATH, rollup_obj)
    write_json(PROFILE_PATH, profile_obj)
    write_json(REPORT_PATH, report_obj)
    write_json(TRANSITION_TRACE_PATH, trace)

    failures.extend(validate_outputs(evidence, target_scan, verification_scan, rollback_scan, classification, audit, rollup_obj, profile_obj, report_obj))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup_obj["source_mutation_count"] = 1
        report_obj["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup_obj)
        write_json(REPORT_PATH, report_obj)

    acceptance_gate_results = {
        "RUNTIME_PATCH_PRECHECK_0_DESIGN_RECEIPT_CONSUMED": SOURCE_PRECHECK_DESIGN_RECEIPT_PATH.exists(),
        "RUNTIME_PATCH_PRECHECK_1_CONTRACT_CONSUMED": SOURCE_PRECHECK_CONTRACT_PATH.exists(),
        "RUNTIME_PATCH_PRECHECK_2_ACCEPTED_PROPOSAL_CONSUMED": SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH.exists(),
        "RUNTIME_PATCH_PRECHECK_3_ELIGIBILITY_EVIDENCE_EMITTED": ELIGIBILITY_EVIDENCE_PATH.exists(),
        "RUNTIME_PATCH_PRECHECK_4_TARGET_SCAN_EMITTED": BOUNDED_TARGET_CANDIDATE_SCAN_PATH.exists(),
        "RUNTIME_PATCH_PRECHECK_5_VERIFICATION_SCAN_EMITTED": VERIFICATION_GATE_SCAN_PATH.exists(),
        "RUNTIME_PATCH_PRECHECK_6_ROLLBACK_STOP_SCAN_EMITTED": ROLLBACK_OR_STOP_SCAN_PATH.exists(),
        "RUNTIME_PATCH_PRECHECK_7_CLASSIFICATION_EMITTED": ELIGIBILITY_CLASSIFICATION_PATH.exists() and classification["classification_status"] == "PASS",
        "RUNTIME_PATCH_PRECHECK_8_OUTCOME_CLOSED_ENUM": classification["eligibility_outcome"] in read_json(SOURCE_PRECHECK_CONTRACT_PATH).get("allowed_precheck_outcomes", []),
        "RUNTIME_PATCH_PRECHECK_9_AUTHORITY_AUDIT_PASS": audit["audit_status"] == "PASS",
        "RUNTIME_PATCH_PRECHECK_10_NO_RUNTIME_PATCH": rollup_obj["runtime_patch_applied_count"] == 0,
        "RUNTIME_PATCH_PRECHECK_11_NO_TARGET_FILE_MODIFICATION": rollup_obj["target_file_modified_count"] == 0,
        "RUNTIME_PATCH_PRECHECK_12_NO_C5_OPENED": rollup_obj["c5_opened_count"] == 0,
        "RUNTIME_PATCH_PRECHECK_13_NO_GENERAL_CELL1_AUTHORITY": rollup_obj["general_cell1_authority_granted_count"] == 0,
        "RUNTIME_PATCH_PRECHECK_14_NO_PROPOSAL_PROMOTION": rollup_obj["proposal_status_promoted_count"] == 0,
        "RUNTIME_PATCH_PRECHECK_15_NO_ACCEPTED_PROPOSAL_FABRICATION": rollup_obj["accepted_proposal_fabricated_count"] == 0,
        "RUNTIME_PATCH_PRECHECK_16_NO_UNBOUNDED_PAYLOAD_INSPECTION": rollup_obj["unbounded_payload_inspection_count"] == 0,
        "RUNTIME_PATCH_PRECHECK_17_NO_HIDDEN_NEXT_COMMAND": rollup_obj["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
        "RUNTIME_PATCH_PRECHECK_18_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    for gate_name, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate_name}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_precheck_design": SOURCE_PRECHECK_DESIGN_RECEIPT_ID,
        "eligibility_outcome": classification["eligibility_outcome"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "design_readout": rel(DESIGN_READOUT_PATH),
        "eligibility_evidence": rel(ELIGIBILITY_EVIDENCE_PATH),
        "bounded_target_candidate_scan": rel(BOUNDED_TARGET_CANDIDATE_SCAN_PATH),
        "verification_gate_scan": rel(VERIFICATION_GATE_SCAN_PATH),
        "rollback_or_stop_boundary_scan": rel(ROLLBACK_OR_STOP_SCAN_PATH),
        "eligibility_classification": rel(ELIGIBILITY_CLASSIFICATION_PATH),
        "authority_audit": rel(AUTHORITY_AUDIT_PATH),
        "rollup": rel(ROLLUP_PATH),
        "profile": rel(PROFILE_PATH),
        "report": rel(REPORT_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_precheck_design_receipt": rel(SOURCE_PRECHECK_DESIGN_RECEIPT_PATH),
        "source_precheck_contract": rel(SOURCE_PRECHECK_CONTRACT_PATH),
        "source_accepted_proposal_packet": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "source_schema_reference_packet": rel(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH),
        "source_handoff_return_reference_packet": rel(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH),
    }

    guards = {
        "build_mode_bounded_runtime_patch_eligibility_precheck_only": BUILD_MODE == "BOUNDED_RUNTIME_PATCH_ELIGIBILITY_PRECHECK_ONLY",
        "eligibility_outcome": classification["eligibility_outcome"],
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "proposal_status_promoted": False,
        "accepted_proposal_fabricated": False,
        "unbounded_payload_inspection": False,
        "hidden_next_command": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
    }

    receipt = {
        "schema_version": "cell1_minimal_runtime_patch_precheck_receipt_v0",
        "receipt_type": "CELL1_MINIMAL_RUNTIME_PATCH_PRECHECK_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "bounded Cell1 minimal runtime patch eligibility precheck",
        "source_precheck_design_receipt_id": SOURCE_PRECHECK_DESIGN_RECEIPT_ID,
        "source_after_return_next_objective_receipt_id": SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_ID,
        "source_handoff_return_close_receipt_id": SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID,
        "source_schema_close_receipt_id": SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "minimal_runtime_patch_precheck_summary": {
            "profile_status": profile_obj["status"],
            "eligibility_outcome": classification["eligibility_outcome"],
            "eligible_for_minimal_runtime_patch_test_design": classification["eligible_for_minimal_runtime_patch_test_design"],
            "accepted_proposal_present_count": rollup_obj["accepted_proposal_present_count"],
            "bounded_target_candidate_count": rollup_obj["bounded_target_candidate_count"],
            "exactly_one_bounded_target_count": rollup_obj["exactly_one_bounded_target_count"],
            "verification_gate_declared_count": rollup_obj["verification_gate_declared_count"],
            "rollback_or_stop_boundary_declared_count": rollup_obj["rollback_or_stop_boundary_declared_count"],
            "return_review_surface_available_count": rollup_obj["return_review_surface_available_count"],
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
        "minimal_runtime_patch_precheck_guards": guards,
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
    if len(negative_controls) != 20 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
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
    print(f"minimal_runtime_patch_precheck_receipt_id={receipt_id}")
    print(f"minimal_runtime_patch_precheck_receipt_path=data/cell1_minimal_runtime_patch_test_precheck_run_v0_receipts/{receipt_id}.json")
    print(f"minimal_runtime_patch_precheck_evidence_path=data/cell1_minimal_runtime_patch_test_precheck_run_v0/runtime_patch_precheck_eligibility_evidence_v0.json")
    print(f"minimal_runtime_patch_precheck_classification_path=data/cell1_minimal_runtime_patch_test_precheck_run_v0/runtime_patch_precheck_eligibility_classification_v0.json")
    print(f"minimal_runtime_patch_precheck_rollup_path=data/cell1_minimal_runtime_patch_test_precheck_run_v0/runtime_patch_precheck_rollup_v0.json")
    print(f"minimal_runtime_patch_precheck_profile_path=data/cell1_minimal_runtime_patch_test_precheck_run_v0/runtime_patch_precheck_profile_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
