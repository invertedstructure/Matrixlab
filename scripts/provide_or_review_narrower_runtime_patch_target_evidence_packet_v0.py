#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PROVIDE_OR_REVIEW_NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_evidence_packet_review.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_REVIEW"
MODE = "PROVIDE_OR_REVIEW / NARROWER_TARGET_EVIDENCE / NO_PATCH"
BUILD_MODE = "TARGET_EVIDENCE_PACKET_REVIEW_OR_TEMPLATE_ONLY"

SOURCE_TARGET_EVIDENCE_REQUEST_RECEIPT_ID = "e5b289f7"
SOURCE_TARGET_EVIDENCE_REQUEST_RECEIPT_PATH = ROOT / "data" / "cell1_runtime_patch_target_evidence_request_v0_receipts" / "e5b289f7.json"
SOURCE_TARGET_EVIDENCE_REQUEST_PACKET_PATH = ROOT / "data" / "cell1_runtime_patch_target_evidence_request_v0" / "narrower_runtime_patch_target_evidence_request_packet_v0.json"
SOURCE_TARGET_EVIDENCE_PACKET_SCHEMA_PATH = ROOT / "data" / "cell1_runtime_patch_target_evidence_request_v0" / "runtime_patch_target_evidence_packet_schema_v0.json"
SOURCE_TARGET_HINT_INVENTORY_PATH = ROOT / "data" / "cell1_runtime_patch_target_evidence_request_v0" / "target_hint_inventory_v0.json"
SOURCE_TARGET_EVIDENCE_AUTHORITY_BOUNDARY_PATH = ROOT / "data" / "cell1_runtime_patch_target_evidence_request_v0" / "target_evidence_request_authority_boundary_v0.json"
SOURCE_TARGET_EVIDENCE_REQUEST_ROLLUP_PATH = ROOT / "data" / "cell1_runtime_patch_target_evidence_request_v0" / "target_evidence_request_rollup_v0.json"
SOURCE_TARGET_EVIDENCE_REQUEST_PROFILE_PATH = ROOT / "data" / "cell1_runtime_patch_target_evidence_request_v0" / "target_evidence_request_profile_v0.json"

CANDIDATE_PACKET_PATH = ROOT / os.environ.get(
    "TARGET_EVIDENCE_PACKET_CANDIDATE_PATH",
    "data/cell1_runtime_patch_target_evidence_packet_review_v0/proposed_runtime_patch_target_evidence_packet_v0.json",
)

REQUIRED_SOURCE_FILES = [
    SOURCE_TARGET_EVIDENCE_REQUEST_RECEIPT_PATH,
    SOURCE_TARGET_EVIDENCE_REQUEST_PACKET_PATH,
    SOURCE_TARGET_EVIDENCE_PACKET_SCHEMA_PATH,
    SOURCE_TARGET_HINT_INVENTORY_PATH,
    SOURCE_TARGET_EVIDENCE_AUTHORITY_BOUNDARY_PATH,
    SOURCE_TARGET_EVIDENCE_REQUEST_ROLLUP_PATH,
    SOURCE_TARGET_EVIDENCE_REQUEST_PROFILE_PATH,
]

OUT_DIR = ROOT / "data" / "cell1_runtime_patch_target_evidence_packet_review_v0"
RECEIPT_DIR = ROOT / "data" / "cell1_runtime_patch_target_evidence_packet_review_v0_receipts"

INTAKE_SURFACE_PATH = OUT_DIR / "target_evidence_packet_intake_surface_v0.json"
PACKET_TEMPLATE_PATH = OUT_DIR / "proposed_runtime_patch_target_evidence_packet_template_v0.json"
CANDIDATE_PACKET_DIGEST_PATH = OUT_DIR / "candidate_target_evidence_packet_digest_v0.json"
REVIEW_CLASSIFICATION_PATH = OUT_DIR / "target_evidence_packet_review_classification_v0.json"
AUTHORITY_AUDIT_PATH = OUT_DIR / "target_evidence_packet_review_authority_audit_v0.json"
ROLLUP_PATH = OUT_DIR / "target_evidence_packet_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "target_evidence_packet_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "target_evidence_packet_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "target_evidence_packet_review_transition_trace.json"

RECOMMENDED_NEXT_IF_MISSING = "PROVIDE_EXPLICIT_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_V0"
RECOMMENDED_NEXT_IF_INVALID = "REPAIR_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_V0"
RECOMMENDED_NEXT_IF_READY = "REQUEST_HUMAN_ACCEPT_OR_REJECT_RUNTIME_PATCH_TARGET_CANDIDATE_V0"

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
    "decision": "PROVIDE_OR_REVIEW_NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET",
    "scope": (
        "Review one explicitly provided narrower runtime patch target evidence packet if present at the declared "
        "candidate path, or emit a fillable packet template and withhold target selection if no packet is present. "
        "This unit may not select a target by itself, may not apply a runtime patch, may not modify target files, "
        "may not open C5, and may not widen authority."
    ),
    "authorized": [
        "consume target evidence request receipt",
        "consume evidence request packet",
        "consume evidence packet schema",
        "consume target hint inventory",
        "inspect one declared candidate evidence packet path if present",
        "validate candidate evidence packet fields and authority boundary",
        "emit fillable evidence packet template if candidate is absent",
        "emit review classification",
        "emit receipt",
        "stop with no hidden next command",
    ],
    "not_authorized": [
        "select target by preference",
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
            failures.append(f"required_source_missing:{rel(path) if path.exists() else path.as_posix()}")
    if failures:
        return failures

    receipt = read_json(SOURCE_TARGET_EVIDENCE_REQUEST_RECEIPT_PATH)
    request = read_json(SOURCE_TARGET_EVIDENCE_REQUEST_PACKET_PATH)
    schema = read_json(SOURCE_TARGET_EVIDENCE_PACKET_SCHEMA_PATH)
    inventory = read_json(SOURCE_TARGET_HINT_INVENTORY_PATH)
    boundary = read_json(SOURCE_TARGET_EVIDENCE_AUTHORITY_BOUNDARY_PATH)
    rollup = read_json(SOURCE_TARGET_EVIDENCE_REQUEST_ROLLUP_PATH)
    profile = read_json(SOURCE_TARGET_EVIDENCE_REQUEST_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_TARGET_EVIDENCE_REQUEST_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("target_evidence_request_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != "STOP_NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_REQUESTED":
        failures.append("target_evidence_request_wrong_terminal")
    if request.get("request_kind") != "REQUEST_NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE":
        failures.append("source_request_kind_wrong")
    if request.get("target_candidate_declared") is not False:
        failures.append("source_request_declared_target_candidate")
    if request.get("runtime_patch_authorized") is not False:
        failures.append("source_request_authorized_runtime_patch")
    if schema.get("packet_object_type") != "NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET":
        failures.append("source_schema_wrong_packet_object_type")
    if inventory.get("hint_count") != 13:
        failures.append(f"source_inventory_hint_count_not_13:{inventory.get('hint_count')}")
    if inventory.get("target_selected") is not False:
        failures.append("source_inventory_target_selected")
    for key in [
        "may_select_target",
        "may_declare_target_candidate",
        "may_apply_runtime_patch",
        "may_modify_target_files",
        "may_open_c5",
        "may_grant_general_cell1_authority",
        "may_use_latest_file_guessing",
        "may_use_mtime_selection",
    ]:
        if boundary.get(key) is not False:
            failures.append(f"source_boundary_authority_not_false:{key}")
    for key in ZERO_COUNTER_KEYS:
        if rollup.get(key) != 0:
            failures.append(f"source_rollup_counter_nonzero:{key}:{rollup.get(key)}")
    if profile.get("status") != "NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_REQUESTED":
        failures.append("source_profile_not_evidence_requested")
    return failures

def intake_surface(candidate_exists: bool) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_evidence_packet_intake_surface_v0",
        "source_target_evidence_request_receipt_id": SOURCE_TARGET_EVIDENCE_REQUEST_RECEIPT_ID,
        "source_target_evidence_request_receipt_ref": rel(SOURCE_TARGET_EVIDENCE_REQUEST_RECEIPT_PATH),
        "source_request_packet_ref": rel(SOURCE_TARGET_EVIDENCE_REQUEST_PACKET_PATH),
        "source_schema_ref": rel(SOURCE_TARGET_EVIDENCE_PACKET_SCHEMA_PATH),
        "source_hint_inventory_ref": rel(SOURCE_TARGET_HINT_INVENTORY_PATH),
        "candidate_packet_path": rel(CANDIDATE_PACKET_PATH),
        "candidate_packet_exists": candidate_exists,
        "intake_status": "CANDIDATE_PACKET_PRESENT" if candidate_exists else "CANDIDATE_PACKET_MISSING_TEMPLATE_EMITTED",
    }

def packet_template() -> Dict[str, Any]:
    return {
        "schema_version": "narrower_runtime_patch_target_evidence_packet_template_v0",
        "packet_object_type": "NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET",
        "evidence_packet_id": "FILL_ME_EXPLICIT_ID",
        "selected_target_ref": "FILL_ME_EXACTLY_ONE_LOCAL_BOUNDED_PATH",
        "selected_target_kind": "FILL_ME_TARGET_KIND",
        "why_this_target_is_load_bearing": "FILL_ME",
        "why_other_hints_are_not_targets": [
            "FILL_ME_FOR_EACH_NON_TARGET_HINT_OR_EXPLICITLY_REFERENCE_INVENTORY_ROWS"
        ],
        "source_evidence_refs": [
            "FILL_ME_AT_LEAST_ONE_EXPLICIT_SOURCE_ARTIFACT"
        ],
        "accepted_proposal_ref": "data/accepted_proposal_packet_for_c4_consumption_v0/accepted_proposal_packet_v0.json",
        "verification_gate_ref": "FILL_ME_EXACT_GATE_FOR_THIS_TARGET",
        "rollback_or_stop_boundary_ref": "FILL_ME_EXACT_BOUNDARY_FOR_THIS_TARGET",
        "allowed_write_scope": "NONE",
        "authority_boundary": {
            "review_only": True,
            "may_name_one_candidate_target_for_review": True,
            "may_apply_runtime_patch": False,
            "may_modify_target_files": False,
            "may_open_c5": False,
            "may_grant_general_cell1_authority": False,
            "may_use_latest_file_guessing": False,
            "may_use_mtime_selection": False,
            "may_promote_proposal_status": False,
            "may_fabricate_accepted_proposal": False
        },
        "review_request": {
            "request_kind": "REVIEW_ONLY_TARGET_EVIDENCE_PACKET",
            "accepted_for_build": False,
            "target_candidate_declared_by_packet": True,
            "runtime_patch_authorized": False
        },
        "template_status": "TEMPLATE_ONLY_NOT_ACCEPTED_FOR_BUILD"
    }

def digest_candidate(candidate_exists: bool) -> Dict[str, Any]:
    if not candidate_exists:
        return {
            "schema_version": "cell1_runtime_patch_target_evidence_candidate_digest_v0",
            "candidate_packet_exists": False,
            "candidate_packet_ref": rel(CANDIDATE_PACKET_PATH),
            "candidate_packet_sha256": None,
            "candidate_packet_sig8": None,
            "candidate_parse_ok": None,
            "candidate_top_keys": [],
        }
    try:
        obj = read_json(CANDIDATE_PACKET_PATH)
        return {
            "schema_version": "cell1_runtime_patch_target_evidence_candidate_digest_v0",
            "candidate_packet_exists": True,
            "candidate_packet_ref": rel(CANDIDATE_PACKET_PATH),
            "candidate_packet_sha256": file_sha256(CANDIDATE_PACKET_PATH),
            "candidate_packet_sig8": file_sha256(CANDIDATE_PACKET_PATH)[:8],
            "candidate_parse_ok": True,
            "candidate_top_keys": sorted(obj.keys()),
        }
    except Exception as exc:
        return {
            "schema_version": "cell1_runtime_patch_target_evidence_candidate_digest_v0",
            "candidate_packet_exists": True,
            "candidate_packet_ref": rel(CANDIDATE_PACKET_PATH),
            "candidate_packet_sha256": file_sha256(CANDIDATE_PACKET_PATH),
            "candidate_packet_sig8": file_sha256(CANDIDATE_PACKET_PATH)[:8],
            "candidate_parse_ok": False,
            "candidate_parse_error": str(exc),
            "candidate_top_keys": [],
        }

def safe_local_bounded_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or value.startswith("FILL_ME"):
        return False
    p = Path(value)
    if p.is_absolute():
        return False
    if ".." in p.parts:
        return False
    forbidden_prefixes = (".git/", "/")
    return not any(value.startswith(prefix) for prefix in forbidden_prefixes)

def validate_candidate_packet(candidate_exists: bool) -> Tuple[str, List[str], Optional[Dict[str, Any]], Optional[str]]:
    if not candidate_exists:
        return "TARGET_EVIDENCE_PACKET_MISSING", ["candidate_packet_missing"], None, None

    try:
        packet = read_json(CANDIDATE_PACKET_PATH)
    except Exception as exc:
        return "TARGET_EVIDENCE_PACKET_INVALID_JSON", [f"candidate_packet_invalid_json:{exc}"], None, None

    schema = read_json(SOURCE_TARGET_EVIDENCE_PACKET_SCHEMA_PATH)
    required = schema.get("required_fields", [])
    failures: List[str] = []

    for field in required:
        if field not in packet:
            failures.append(f"missing_required_field:{field}")

    if packet.get("packet_object_type") != "NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET":
        failures.append("packet_object_type_wrong_or_missing")

    selected_target_ref = packet.get("selected_target_ref")
    if not safe_local_bounded_path(selected_target_ref):
        failures.append("selected_target_ref_not_exact_local_bounded_path")

    if packet.get("allowed_write_scope") != "NONE":
        failures.append("allowed_write_scope_not_NONE")

    source_refs = packet.get("source_evidence_refs")
    if not isinstance(source_refs, list) or len(source_refs) == 0 or not all(isinstance(x, str) and x for x in source_refs):
        failures.append("source_evidence_refs_missing_or_empty")

    why = packet.get("why_this_target_is_load_bearing")
    if not isinstance(why, str) or not why.strip() or why.startswith("FILL_ME"):
        failures.append("why_this_target_is_load_bearing_missing")

    other = packet.get("why_other_hints_are_not_targets")
    if not isinstance(other, list) or len(other) == 0:
        failures.append("why_other_hints_are_not_targets_missing")

    for field in ["accepted_proposal_ref", "verification_gate_ref", "rollback_or_stop_boundary_ref"]:
        value = packet.get(field)
        if not isinstance(value, str) or not value.strip() or value.startswith("FILL_ME"):
            failures.append(f"{field}_missing")

    auth = packet.get("authority_boundary")
    if not isinstance(auth, dict):
        failures.append("authority_boundary_missing_or_not_object")
    else:
        for key in [
            "may_apply_runtime_patch",
            "may_modify_target_files",
            "may_open_c5",
            "may_grant_general_cell1_authority",
            "may_use_latest_file_guessing",
            "may_use_mtime_selection",
            "may_promote_proposal_status",
            "may_fabricate_accepted_proposal",
        ]:
            if auth.get(key) is not False:
                failures.append(f"authority_boundary_not_false:{key}")

    review = packet.get("review_request")
    if not isinstance(review, dict):
        failures.append("review_request_missing_or_not_object")
    else:
        if review.get("accepted_for_build") is not False:
            failures.append("review_request_accepts_for_build")
        if review.get("runtime_patch_authorized") is not False:
            failures.append("review_request_authorizes_runtime_patch")

    target_candidate_ref = selected_target_ref if not failures else None
    if failures:
        return "TARGET_EVIDENCE_PACKET_INSUFFICIENT", failures, packet, target_candidate_ref
    return "TARGET_EVIDENCE_PACKET_READY_FOR_REVIEW", [], packet, selected_target_ref

def review_classification(candidate_exists: bool) -> Dict[str, Any]:
    status, failures, packet, target_candidate_ref = validate_candidate_packet(candidate_exists)
    if status == "TARGET_EVIDENCE_PACKET_READY_FOR_REVIEW":
        recommended_next = RECOMMENDED_NEXT_IF_READY
        target_candidate_declared_for_review = True
    elif status == "TARGET_EVIDENCE_PACKET_MISSING":
        recommended_next = RECOMMENDED_NEXT_IF_MISSING
        target_candidate_declared_for_review = False
    else:
        recommended_next = RECOMMENDED_NEXT_IF_INVALID
        target_candidate_declared_for_review = False

    return {
        "schema_version": "cell1_runtime_patch_target_evidence_packet_review_classification_v0",
        "source_target_evidence_request_receipt_id": SOURCE_TARGET_EVIDENCE_REQUEST_RECEIPT_ID,
        "candidate_packet_ref": rel(CANDIDATE_PACKET_PATH),
        "candidate_packet_exists": candidate_exists,
        "review_status": status,
        "failures": failures,
        "target_candidate_declared_for_review": target_candidate_declared_for_review,
        "target_candidate_ref": target_candidate_ref,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

def authority_audit(classification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_evidence_packet_review_authority_audit_v0",
        "audit_status": "PASS",
        "candidate_packet_exists": classification["candidate_packet_exists"],
        "review_status": classification["review_status"],
        "may_declare_candidate_for_review": classification["review_status"] == "TARGET_EVIDENCE_PACKET_READY_FOR_REVIEW",
        "may_select_target_for_build": False,
        "may_apply_runtime_patch": False,
        "may_modify_target_files": False,
        "may_open_c5": False,
        "may_grant_general_cell1_authority": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "must_not_infer": [
            "ready_for_review means accepted for build",
            "candidate for review means selected target",
            "candidate packet authorizes patching",
            "missing packet allows target fabrication",
            "invalid packet allows best-effort target selection",
        ],
    }

def rollup(candidate_exists: bool, classification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_evidence_packet_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_target_evidence_request_receipt_id": SOURCE_TARGET_EVIDENCE_REQUEST_RECEIPT_ID,
        "candidate_packet_exists_count": 1 if candidate_exists else 0,
        "candidate_packet_missing_count": 0 if candidate_exists else 1,
        "candidate_packet_ready_for_review_count": 1 if classification["review_status"] == "TARGET_EVIDENCE_PACKET_READY_FOR_REVIEW" else 0,
        "candidate_packet_insufficient_count": 1 if classification["review_status"] in ["TARGET_EVIDENCE_PACKET_INSUFFICIENT", "TARGET_EVIDENCE_PACKET_INVALID_JSON"] else 0,
        "template_emitted_count": 0 if candidate_exists else 1,
        "target_candidate_declared_for_review_count": 1 if classification["target_candidate_declared_for_review"] else 0,
        "target_selected_for_build_count": 0,
        "accepted_for_build_count": 0,
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

def profile(rollup_obj: Dict[str, Any], classification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_evidence_packet_review_profile_v0",
        "profile_id": "target_evidence_packet_review_" + sha8({
            "source": SOURCE_TARGET_EVIDENCE_REQUEST_RECEIPT_ID,
            "status": classification["review_status"],
            "candidate": rel(CANDIDATE_PACKET_PATH),
        }),
        "status": classification["review_status"],
        "candidate_packet_exists": classification["candidate_packet_exists"],
        "target_candidate_declared_for_review": classification["target_candidate_declared_for_review"],
        "target_candidate_ref": classification["target_candidate_ref"],
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "recommended_next": classification["recommended_next"],
        "next_command_goal": None,
    }

def report(rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_runtime_patch_target_evidence_packet_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_target_evidence_request_receipt_consumed_count": 1,
        "candidate_packet_exists_count": rollup_obj["candidate_packet_exists_count"],
        "candidate_packet_missing_count": rollup_obj["candidate_packet_missing_count"],
        "template_emitted_count": rollup_obj["template_emitted_count"],
        "review_status": profile_obj["status"],
        "recommended_next_handling": rollup_obj["recommended_next"],
        "target_candidate_declared_for_review_count": rollup_obj["target_candidate_declared_for_review_count"],
        "target_selected_for_build_count": 0,
        "accepted_for_build_count": 0,
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
    if classification["review_status"] == "TARGET_EVIDENCE_PACKET_READY_FOR_REVIEW":
        taken = "withhold_build_acceptance_and_request_human_accept_or_reject_candidate"
        stop_code = "STOP_TARGET_EVIDENCE_PACKET_READY_FOR_REVIEW"
    elif classification["review_status"] == "TARGET_EVIDENCE_PACKET_MISSING":
        taken = "emit_template_and_request_explicit_evidence_packet"
        stop_code = "STOP_TARGET_EVIDENCE_PACKET_MISSING"
    else:
        taken = "request_packet_repair"
        stop_code = "STOP_TARGET_EVIDENCE_PACKET_INSUFFICIENT"

    return {
        "schema_version": "cell1_runtime_patch_target_evidence_packet_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_evidence_request_surface",
                "question": "is there a declared candidate evidence packet path",
                "answer": rel(CANDIDATE_PACKET_PATH),
                "taken": "inspect_declared_path_only",
            },
            {
                "step": "review_candidate_or_emit_template",
                "question": "can exactly one bounded target candidate be named for review without build acceptance",
                "answer": classification["review_status"],
                "taken": taken,
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": stop_code,
            "next_command_goal": None,
        },
    }

def validate_outputs(candidate_exists: bool, classification: Dict[str, Any], audit: Dict[str, Any], rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any], report_obj: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if audit.get("audit_status") != "PASS":
        failures.append("audit_not_pass")
    if classification.get("target_selected_for_build") is not False:
        failures.append("classification_selects_target_for_build")
    if classification.get("accepted_for_build") is not False:
        failures.append("classification_accepts_for_build")
    if classification.get("runtime_patch_authorized") is not False:
        failures.append("classification_authorizes_runtime_patch")
    if classification.get("target_file_modification_authorized") is not False:
        failures.append("classification_authorizes_target_file_modification")
    if classification.get("c5_authorized") is not False:
        failures.append("classification_authorizes_c5")
    if classification.get("general_cell1_authority_granted") is not False:
        failures.append("classification_grants_general_cell1_authority")
    if classification.get("next_command_goal") is not None:
        failures.append("classification_hidden_next_command")
    if not candidate_exists and classification.get("target_candidate_declared_for_review") is not False:
        failures.append("missing_candidate_declares_target_candidate_for_review")
    for key in ["may_select_target_for_build", "may_apply_runtime_patch", "may_modify_target_files", "may_open_c5", "may_grant_general_cell1_authority", "may_use_latest_file_guessing", "may_use_mtime_selection"]:
        if audit.get(key) is not False:
            failures.append(f"audit_authority_not_false:{key}")
    for key in ZERO_COUNTER_KEYS:
        if rollup_obj.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup_obj.get(key)}")
    for key in [
        "target_selected_for_build_count",
        "accepted_for_build_count",
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
    if profile_obj.get("target_selected_for_build") is not False:
        failures.append("profile_selects_target_for_build")
    if profile_obj.get("accepted_for_build") is not False:
        failures.append("profile_accepts_for_build")
    if profile_obj.get("runtime_patch_applied") is not False:
        failures.append("profile_claims_runtime_patch")
    if profile_obj.get("target_file_modified") is not False:
        failures.append("profile_claims_target_file_modified")
    if profile_obj.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")
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
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    candidate_exists = CANDIDATE_PACKET_PATH.exists()
    classification = read_json(REVIEW_CLASSIFICATION_PATH)
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

    bad = copy.deepcopy(classification)
    bad["target_selected_for_build"] = True
    add("classification_selects_target_for_build_fail", validate_outputs(candidate_exists, bad, audit, rollup_obj, profile_obj, report_obj), "classification_selects_target_for_build")

    bad = copy.deepcopy(classification)
    bad["accepted_for_build"] = True
    add("classification_accepts_for_build_fail", validate_outputs(candidate_exists, bad, audit, rollup_obj, profile_obj, report_obj), "classification_accepts_for_build")

    bad = copy.deepcopy(classification)
    bad["runtime_patch_authorized"] = True
    add("classification_authorizes_runtime_patch_fail", validate_outputs(candidate_exists, bad, audit, rollup_obj, profile_obj, report_obj), "classification_authorizes_runtime_patch")

    bad = copy.deepcopy(classification)
    bad["target_file_modification_authorized"] = True
    add("classification_authorizes_target_file_modification_fail", validate_outputs(candidate_exists, bad, audit, rollup_obj, profile_obj, report_obj), "classification_authorizes_target_file_modification")

    bad = copy.deepcopy(classification)
    bad["next_command_goal"] = "APPLY_PATCH"
    add("classification_hidden_next_command_fail", validate_outputs(candidate_exists, bad, audit, rollup_obj, profile_obj, report_obj), "classification_hidden_next_command")

    for case, key, expected in [
        ("audit_allows_select_target_for_build_fail", "may_select_target_for_build", "audit_authority_not_false:may_select_target_for_build"),
        ("audit_allows_runtime_patch_fail", "may_apply_runtime_patch", "audit_authority_not_false:may_apply_runtime_patch"),
        ("audit_allows_target_file_modification_fail", "may_modify_target_files", "audit_authority_not_false:may_modify_target_files"),
        ("audit_allows_c5_fail", "may_open_c5", "audit_authority_not_false:may_open_c5"),
        ("audit_allows_general_cell1_authority_fail", "may_grant_general_cell1_authority", "audit_authority_not_false:may_grant_general_cell1_authority"),
        ("audit_allows_latest_file_guessing_fail", "may_use_latest_file_guessing", "audit_authority_not_false:may_use_latest_file_guessing"),
        ("audit_allows_mtime_selection_fail", "may_use_mtime_selection", "audit_authority_not_false:may_use_mtime_selection"),
    ]:
        bad_audit = copy.deepcopy(audit)
        bad_audit[key] = True
        add(case, validate_outputs(candidate_exists, classification, bad_audit, rollup_obj, profile_obj, report_obj), expected)

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
        add(case, validate_outputs(candidate_exists, classification, audit, bad_rollup, profile_obj, bad_report), counter)

    bad_profile = copy.deepcopy(profile_obj)
    bad_profile["accepted_for_build"] = True
    add("profile_accepts_for_build_fail", validate_outputs(candidate_exists, classification, audit, rollup_obj, bad_profile, report_obj), "profile_accepts_for_build")

    bad_profile = copy.deepcopy(profile_obj)
    bad_profile["runtime_patch_applied"] = True
    add("profile_claims_runtime_patch_fail", validate_outputs(candidate_exists, classification, audit, rollup_obj, bad_profile, report_obj), "profile_claims_runtime_patch")

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_TARGET_EVIDENCE_PACKET_REVIEW_DEPENDENCY_MISSING", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "cell1_runtime_patch_target_evidence_packet_review_receipt_v0",
            "receipt_type": "CELL1_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_REVIEW_RECEIPT",
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
        return 1

    candidate_exists = CANDIDATE_PACKET_PATH.exists()

    write_json(INTAKE_SURFACE_PATH, intake_surface(candidate_exists))
    if not candidate_exists:
        write_json(PACKET_TEMPLATE_PATH, packet_template())

    digest = digest_candidate(candidate_exists)
    write_json(CANDIDATE_PACKET_DIGEST_PATH, digest)

    classification = review_classification(candidate_exists)
    audit = authority_audit(classification)
    rollup_obj = rollup(candidate_exists, classification)
    profile_obj = profile(rollup_obj, classification)
    report_obj = report(rollup_obj, profile_obj)
    trace = transition_trace(classification)

    write_json(REVIEW_CLASSIFICATION_PATH, classification)
    write_json(AUTHORITY_AUDIT_PATH, audit)
    write_json(ROLLUP_PATH, rollup_obj)
    write_json(PROFILE_PATH, profile_obj)
    write_json(REPORT_PATH, report_obj)
    write_json(TRANSITION_TRACE_PATH, trace)

    failures.extend(validate_outputs(candidate_exists, classification, audit, rollup_obj, profile_obj, report_obj))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    if source_before != source_after:
        failures.append("source_file_hash_changed")
        rollup_obj["source_mutation_count"] = 1
        report_obj["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup_obj)
        write_json(REPORT_PATH, report_obj)

    if classification["review_status"] == "TARGET_EVIDENCE_PACKET_READY_FOR_REVIEW":
        stop_code = "STOP_TARGET_EVIDENCE_PACKET_READY_FOR_REVIEW"
    elif classification["review_status"] == "TARGET_EVIDENCE_PACKET_MISSING":
        stop_code = "STOP_TARGET_EVIDENCE_PACKET_MISSING"
    else:
        stop_code = "STOP_TARGET_EVIDENCE_PACKET_INSUFFICIENT"

    acceptance_gate_results = {
        "TARGET_EVIDENCE_PACKET_REVIEW_0_SOURCE_REQUEST_RECEIPT_CONSUMED": SOURCE_TARGET_EVIDENCE_REQUEST_RECEIPT_PATH.exists(),
        "TARGET_EVIDENCE_PACKET_REVIEW_1_INTAKE_SURFACE_EMITTED": INTAKE_SURFACE_PATH.exists(),
        "TARGET_EVIDENCE_PACKET_REVIEW_2_TEMPLATE_OR_CANDIDATE_DIGEST_EMITTED": PACKET_TEMPLATE_PATH.exists() or CANDIDATE_PACKET_DIGEST_PATH.exists(),
        "TARGET_EVIDENCE_PACKET_REVIEW_3_REVIEW_CLASSIFICATION_EMITTED": REVIEW_CLASSIFICATION_PATH.exists(),
        "TARGET_EVIDENCE_PACKET_REVIEW_4_AUTHORITY_AUDIT_EMITTED": AUTHORITY_AUDIT_PATH.exists(),
        "TARGET_EVIDENCE_PACKET_REVIEW_5_NO_TARGET_SELECTED_FOR_BUILD": classification.get("target_selected_for_build") is False,
        "TARGET_EVIDENCE_PACKET_REVIEW_6_NO_ACCEPTED_FOR_BUILD": classification.get("accepted_for_build") is False,
        "TARGET_EVIDENCE_PACKET_REVIEW_7_NO_RUNTIME_PATCH": classification.get("runtime_patch_authorized") is False,
        "TARGET_EVIDENCE_PACKET_REVIEW_8_NO_TARGET_FILE_MODIFICATION": classification.get("target_file_modification_authorized") is False,
        "TARGET_EVIDENCE_PACKET_REVIEW_9_NO_C5_OPENED": classification.get("c5_authorized") is False,
        "TARGET_EVIDENCE_PACKET_REVIEW_10_NO_GENERAL_CELL1_AUTHORITY": classification.get("general_cell1_authority_granted") is False,
        "TARGET_EVIDENCE_PACKET_REVIEW_11_NO_LATEST_FILE_GUESSING": rollup_obj.get("latest_file_guessing_count") == 0,
        "TARGET_EVIDENCE_PACKET_REVIEW_12_NO_MTIME_SELECTION": rollup_obj.get("mtime_selection_count") == 0,
        "TARGET_EVIDENCE_PACKET_REVIEW_13_NO_UNBOUNDED_PAYLOAD_INSPECTION": rollup_obj.get("unbounded_payload_inspection_count") == 0,
        "TARGET_EVIDENCE_PACKET_REVIEW_14_NO_HIDDEN_NEXT_COMMAND": classification.get("next_command_goal") is None,
        "TARGET_EVIDENCE_PACKET_REVIEW_15_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = {"type": "STOP", "stop_code": stop_code if gate == "PASS" else "STOP_TARGET_EVIDENCE_PACKET_REVIEW_GATE_FAIL", "next_command_goal": None}
    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "source": SOURCE_TARGET_EVIDENCE_REQUEST_RECEIPT_ID,
        "classification": classification,
        "terminal": terminal,
        "gate": gate,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "cell1_runtime_patch_target_evidence_packet_review_receipt_v0",
        "receipt_type": "CELL1_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "narrower runtime patch target evidence packet review",
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "human_decision": HUMAN_DECISION,
        "source_target_evidence_request_receipt_id": SOURCE_TARGET_EVIDENCE_REQUEST_RECEIPT_ID,
        "candidate_packet_ref": rel(CANDIDATE_PACKET_PATH),
        "candidate_packet_exists": candidate_exists,
        "target_evidence_packet_review_summary": {
            "review_status": classification["review_status"],
            "candidate_packet_exists": candidate_exists,
            "target_candidate_declared_for_review": classification["target_candidate_declared_for_review"],
            "target_candidate_ref": classification["target_candidate_ref"],
            "target_selected_for_build": False,
            "accepted_for_build": False,
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "general_cell1_authority_granted": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": profile_obj["bad_counters_zero"],
            "recommended_next": classification["recommended_next"],
        },
        "aggregate_metrics": report_obj,
        "acceptance_gate_results": acceptance_gate_results,
        "negative_controls": [],
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "intake_surface": rel(INTAKE_SURFACE_PATH),
            "packet_template": rel(PACKET_TEMPLATE_PATH) if PACKET_TEMPLATE_PATH.exists() else None,
            "candidate_packet_digest": rel(CANDIDATE_PACKET_DIGEST_PATH),
            "review_classification": rel(REVIEW_CLASSIFICATION_PATH),
            "authority_audit": rel(AUTHORITY_AUDIT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
            "source_request_packet": rel(SOURCE_TARGET_EVIDENCE_REQUEST_PACKET_PATH),
            "source_evidence_packet_schema": rel(SOURCE_TARGET_EVIDENCE_PACKET_SCHEMA_PATH),
            "source_hint_inventory": rel(SOURCE_TARGET_HINT_INVENTORY_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)
    controls = run_negative_controls(receipt_path)
    receipt["negative_controls"] = controls

    if not all(c.get("negative_control_pass") is True for c in controls):
        receipt["gate"] = "FAIL"
        receipt["failures"].append("negative_control_failed")
    receipt_failures = validate_receipt(receipt)
    if receipt_failures:
        receipt["gate"] = "FAIL"
        receipt["failures"].extend(receipt_failures)

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"target_evidence_packet_review_receipt_id={receipt['receipt_id']}")
    print(f"target_evidence_packet_review_receipt_path={rel(receipt_path)}")
    print(f"target_evidence_packet_review_classification_path={rel(REVIEW_CLASSIFICATION_PATH)}")
    print(f"target_evidence_packet_template_path={rel(PACKET_TEMPLATE_PATH) if PACKET_TEMPLATE_PATH.exists() else ''}")
    print(f"target_evidence_packet_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"target_evidence_packet_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
