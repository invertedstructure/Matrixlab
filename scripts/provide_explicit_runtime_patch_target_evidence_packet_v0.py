#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PROVIDE_EXPLICIT_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_evidence_packet_provided.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_PROVIDED"
MODE = "PROVIDE_EXPLICIT / ONE_TARGET_EVIDENCE_PACKET / NO_PATCH"
BUILD_MODE = "EXPLICIT_TARGET_EVIDENCE_PACKET_ONLY"

SOURCE_INPUT_REQUEST_RECEIPT_ID = "ad527bfd"
SOURCE_INPUT_REQUEST_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_input_request_v0_receipts/ad527bfd.json"
SOURCE_INPUT_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_input_request_v0/explicit_runtime_patch_target_evidence_input_contract_v0.json"
SOURCE_REVIEW_RECEIPT_ID = "76b44fed"
SOURCE_REVIEW_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_packet_review_v0_receipts/76b44fed.json"
SOURCE_REVIEW_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_packet_review_v0/target_evidence_packet_review_classification_v0.json"
SOURCE_TEMPLATE_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_packet_review_v0/proposed_runtime_patch_target_evidence_packet_template_v0.json"
SOURCE_SCHEMA_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_request_v0/runtime_patch_target_evidence_packet_schema_v0.json"
SOURCE_HINT_INVENTORY_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_request_v0/target_hint_inventory_v0.json"
SOURCE_REQUEST_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_request_v0/narrower_runtime_patch_target_evidence_request_packet_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_evidence_packet_provided_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_evidence_packet_provided_v0_receipts"

PROVIDED_PACKET_PATH = OUT_DIR / "provided_runtime_patch_target_evidence_packet_v0.json"
PROVIDED_PACKET_DIGEST_PATH = OUT_DIR / "provided_runtime_patch_target_evidence_packet_digest_v0.json"
PROVIDED_PACKET_CLASSIFICATION_PATH = OUT_DIR / "provided_runtime_patch_target_evidence_packet_classification_v0.json"
AUTHORITY_AUDIT_PATH = OUT_DIR / "provided_runtime_patch_target_evidence_packet_authority_audit_v0.json"
ROLLUP_PATH = OUT_DIR / "provided_runtime_patch_target_evidence_packet_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "provided_runtime_patch_target_evidence_packet_profile_v0.json"
REPORT_PATH = OUT_DIR / "provided_runtime_patch_target_evidence_packet_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "provided_runtime_patch_target_evidence_packet_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_INPUT_REQUEST_RECEIPT_PATH,
    SOURCE_INPUT_CONTRACT_PATH,
    SOURCE_REVIEW_RECEIPT_PATH,
    SOURCE_REVIEW_CLASSIFICATION_PATH,
    SOURCE_TEMPLATE_PATH,
    SOURCE_SCHEMA_PATH,
    SOURCE_HINT_INVENTORY_PATH,
    SOURCE_REQUEST_PACKET_PATH,
]

REQUIRED_ENV_FIELDS = [
    "SELECTED_TARGET_REF",
    "SELECTED_TARGET_KIND",
    "WHY_THIS_TARGET_IS_LOAD_BEARING",
    "WHY_OTHER_HINTS_ARE_NOT_TARGETS_JSON",
    "SOURCE_EVIDENCE_REFS_JSON",
    "VERIFICATION_GATE_REF",
    "ROLLBACK_OR_STOP_BOUNDARY_REF",
]

ZERO_COUNTER_KEYS = [
    "target_selected_for_build_count",
    "accepted_for_build_count",
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
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def emit_fail_receipt(failures: List[str], stop_code: str) -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    terminal = {"type": "STOP", "stop_code": stop_code, "next_command_goal": None}
    receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt = {
        "schema_version": "provided_runtime_patch_target_evidence_packet_receipt_v0",
        "receipt_type": "PROVIDED_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": "FAIL",
        "failures": failures,
        "warnings": [],
        "provided_packet_summary": {
            "classification_status": "EXPLICIT_TARGET_EVIDENCE_PACKET_NOT_PROVIDED",
            "target_candidate_declared_for_review": False,
            "target_candidate_ref": None,
            "target_selected_for_build": False,
            "accepted_for_build": False,
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "general_cell1_authority_granted": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": True,
            "recommended_next": "RERUN_PROVIDE_EXPLICIT_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_WITH_ENV_V0",
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }
    write_json(receipt_path, receipt)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"provided_target_evidence_packet_receipt_id={receipt_id}")
    print(f"provided_target_evidence_packet_receipt_path={rel(receipt_path)}")
    return 1

def parse_json_env(name: str) -> Any:
    value = os.environ.get(name, "")
    try:
        return json.loads(value)
    except Exception as exc:
        raise ValueError(f"invalid_json_env:{name}:{exc}")

def safe_local_bounded_path(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    if "EDIT_ME" in value:
        return False
    if value.startswith("FILL_ME") or value.startswith("exact/"):
        return False
    p = Path(value)
    if p.is_absolute():
        return False
    if ".." in p.parts:
        return False
    if value.startswith(".git/"):
        return False
    return True

def validate_required_env() -> List[str]:
    failures: List[str] = []
    for field in REQUIRED_ENV_FIELDS:
        value = os.environ.get(field, "")
        if not value or "EDIT_ME" in value or value.startswith("exact/"):
            failures.append(f"env_missing_or_placeholder:{field}:{value}")
    for field in ["WHY_OTHER_HINTS_ARE_NOT_TARGETS_JSON", "SOURCE_EVIDENCE_REFS_JSON"]:
        value = os.environ.get(field, "")
        if not value or "EDIT_ME" in value:
            continue
        try:
            parsed = json.loads(value)
            if not isinstance(parsed, list) or not parsed:
                failures.append(f"env_json_not_nonempty_list:{field}")
        except Exception as exc:
            failures.append(f"env_invalid_json:{field}:{exc}")
    return failures

def validate_source_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    input_receipt = read_json(SOURCE_INPUT_REQUEST_RECEIPT_PATH)
    input_contract = read_json(SOURCE_INPUT_CONTRACT_PATH)
    review_receipt = read_json(SOURCE_REVIEW_RECEIPT_PATH)
    review_classification = read_json(SOURCE_REVIEW_CLASSIFICATION_PATH)
    template = read_json(SOURCE_TEMPLATE_PATH)
    schema = read_json(SOURCE_SCHEMA_PATH)
    inventory = read_json(SOURCE_HINT_INVENTORY_PATH)

    if input_receipt.get("receipt_id") != SOURCE_INPUT_REQUEST_RECEIPT_ID or input_receipt.get("gate") != "PASS":
        failures.append("source_input_request_receipt_not_pass")
    if input_receipt.get("terminal", {}).get("stop_code") != "STOP_EXPLICIT_TARGET_EVIDENCE_INPUTS_REQUESTED":
        failures.append("source_input_request_wrong_terminal")
    if input_contract.get("recommended_next") != "RERUN_PROVIDE_EXPLICIT_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_WITH_ENV_V0":
        failures.append("input_contract_wrong_recommended_next")
    if input_contract.get("target_selected_for_build") is not False:
        failures.append("input_contract_selects_target_for_build")
    if input_contract.get("runtime_patch_authorized") is not False:
        failures.append("input_contract_authorizes_runtime_patch")

    if review_receipt.get("receipt_id") != SOURCE_REVIEW_RECEIPT_ID or review_receipt.get("gate") != "PASS":
        failures.append("source_review_receipt_not_pass")
    if review_receipt.get("terminal", {}).get("stop_code") != "STOP_TARGET_EVIDENCE_PACKET_MISSING":
        failures.append("source_review_terminal_not_missing_packet")
    if review_classification.get("review_status") != "TARGET_EVIDENCE_PACKET_MISSING":
        failures.append("source_review_status_not_missing")
    if review_classification.get("target_candidate_declared_for_review") is not False:
        failures.append("source_review_declared_candidate_unexpectedly")
    if review_classification.get("accepted_for_build") is not False:
        failures.append("source_review_accepted_for_build")
    if review_classification.get("runtime_patch_authorized") is not False:
        failures.append("source_review_authorized_runtime_patch")

    if template.get("packet_object_type") != "NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET":
        failures.append("template_wrong_packet_object_type")
    if schema.get("packet_object_type") != "NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET":
        failures.append("schema_wrong_packet_object_type")
    if inventory.get("hint_count") != 13:
        failures.append(f"hint_count_not_13:{inventory.get('hint_count')}")
    if inventory.get("target_selected") is not False:
        failures.append("inventory_target_selected_unexpectedly")

    return failures

def build_packet() -> Dict[str, Any]:
    why_other = parse_json_env("WHY_OTHER_HINTS_ARE_NOT_TARGETS_JSON")
    source_refs = parse_json_env("SOURCE_EVIDENCE_REFS_JSON")

    return {
        "schema_version": "narrower_runtime_patch_target_evidence_packet_v0",
        "packet_object_type": "NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET",
        "evidence_packet_id": "explicit_target_evidence_" + sha8({
            "target": os.environ["SELECTED_TARGET_REF"],
            "source_refs": source_refs,
            "why": os.environ["WHY_THIS_TARGET_IS_LOAD_BEARING"],
        }),
        "selected_target_ref": os.environ["SELECTED_TARGET_REF"],
        "selected_target_kind": os.environ["SELECTED_TARGET_KIND"],
        "why_this_target_is_load_bearing": os.environ["WHY_THIS_TARGET_IS_LOAD_BEARING"],
        "why_other_hints_are_not_targets": why_other,
        "source_evidence_refs": source_refs,
        "accepted_proposal_ref": "data/accepted_proposal_packet_for_c4_consumption_v0/accepted_proposal_packet_v0.json",
        "verification_gate_ref": os.environ["VERIFICATION_GATE_REF"],
        "rollback_or_stop_boundary_ref": os.environ["ROLLBACK_OR_STOP_BOUNDARY_REF"],
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
        "source_input_request_receipt_id": SOURCE_INPUT_REQUEST_RECEIPT_ID,
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "provided_packet_status": "EXPLICIT_TARGET_EVIDENCE_PACKET_PROVIDED_FOR_REVIEW_ONLY"
    }

def validate_packet(packet: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    required = read_json(SOURCE_SCHEMA_PATH).get("required_fields", [])

    for field in required:
        if field not in packet:
            failures.append(f"missing_required_field:{field}")

    if packet.get("packet_object_type") != "NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET":
        failures.append("packet_object_type_wrong")

    if not safe_local_bounded_path(packet.get("selected_target_ref")):
        failures.append("selected_target_ref_not_exact_local_bounded_path")

    if packet.get("allowed_write_scope") != "NONE":
        failures.append("allowed_write_scope_not_NONE")

    if not isinstance(packet.get("why_this_target_is_load_bearing"), str) or not packet["why_this_target_is_load_bearing"].strip():
        failures.append("load_bearing_reason_missing")

    if not isinstance(packet.get("why_other_hints_are_not_targets"), list) or not packet["why_other_hints_are_not_targets"]:
        failures.append("why_other_hints_are_not_targets_missing_or_not_list")

    refs = packet.get("source_evidence_refs")
    if not isinstance(refs, list) or not refs:
        failures.append("source_evidence_refs_missing_or_not_list")
    else:
        for ref in refs:
            if not safe_local_bounded_path(ref):
                failures.append(f"source_evidence_ref_not_local_bounded:{ref}")

    for field in ["accepted_proposal_ref", "verification_gate_ref", "rollback_or_stop_boundary_ref"]:
        if not safe_local_bounded_path(packet.get(field)):
            failures.append(f"{field}_not_local_bounded")

    auth = packet.get("authority_boundary", {})
    if auth.get("review_only") is not True:
        failures.append("authority_boundary_review_only_not_true")
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

    review = packet.get("review_request", {})
    if review.get("accepted_for_build") is not False:
        failures.append("review_request_accepts_for_build")
    if review.get("runtime_patch_authorized") is not False:
        failures.append("review_request_authorizes_runtime_patch")

    return failures

def digest(packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "provided_runtime_patch_target_evidence_packet_digest_v0",
        "provided_packet_ref": rel(PROVIDED_PACKET_PATH),
        "provided_packet_sha256": file_sha256(PROVIDED_PACKET_PATH),
        "provided_packet_sig8": file_sha256(PROVIDED_PACKET_PATH)[:8],
        "selected_target_ref": packet.get("selected_target_ref"),
        "selected_target_kind": packet.get("selected_target_kind"),
        "source_evidence_ref_count": len(packet.get("source_evidence_refs", [])) if isinstance(packet.get("source_evidence_refs"), list) else 0,
    }

def classification(packet: Dict[str, Any], failures: List[str]) -> Dict[str, Any]:
    ready = not failures
    return {
        "schema_version": "provided_runtime_patch_target_evidence_packet_classification_v0",
        "source_input_request_receipt_id": SOURCE_INPUT_REQUEST_RECEIPT_ID,
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "provided_packet_ref": rel(PROVIDED_PACKET_PATH),
        "classification_status": "EXPLICIT_TARGET_EVIDENCE_PACKET_READY_FOR_REVIEW" if ready else "EXPLICIT_TARGET_EVIDENCE_PACKET_INVALID",
        "failures": failures,
        "target_candidate_declared_for_review": ready,
        "target_candidate_ref": packet.get("selected_target_ref") if ready else None,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "recommended_next": "REVIEW_EXPLICIT_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_V0" if ready else "REPAIR_EXPLICIT_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_V0",
        "next_command_goal": None,
    }

def rollup(classif: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "provided_runtime_patch_target_evidence_packet_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_input_request_receipt_id": SOURCE_INPUT_REQUEST_RECEIPT_ID,
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "provided_packet_emitted_count": 1,
        "provided_packet_ready_for_review_count": 1 if classif["classification_status"] == "EXPLICIT_TARGET_EVIDENCE_PACKET_READY_FOR_REVIEW" else 0,
        "provided_packet_invalid_count": 1 if classif["classification_status"] != "EXPLICIT_TARGET_EVIDENCE_PACKET_READY_FOR_REVIEW" else 0,
        "target_candidate_declared_for_review_count": 1 if classif["target_candidate_declared_for_review"] else 0,
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
        "recommended_next": classif["recommended_next"],
    }

def profile(packet: Dict[str, Any], classif: Dict[str, Any], roll: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "provided_runtime_patch_target_evidence_packet_profile_v0",
        "profile_id": "provided_target_evidence_" + sha8(packet),
        "status": classif["classification_status"],
        "target_candidate_declared_for_review": classif["target_candidate_declared_for_review"],
        "target_candidate_ref": classif["target_candidate_ref"],
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "bad_counters_zero": all(roll.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "recommended_next": classif["recommended_next"],
        "next_command_goal": None,
    }

def report(classif: Dict[str, Any], roll: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "provided_runtime_patch_target_evidence_packet_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "classification_status": classif["classification_status"],
        "recommended_next_handling": classif["recommended_next"],
        **{k: roll[k] for k in [
            "provided_packet_emitted_count",
            "provided_packet_ready_for_review_count",
            "provided_packet_invalid_count",
            "target_candidate_declared_for_review_count",
            "target_selected_for_build_count",
            "accepted_for_build_count",
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
        ]}
    }

def authority_audit(classif: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "provided_runtime_patch_target_evidence_packet_authority_audit_v0",
        "audit_status": "PASS",
        "may_declare_candidate_for_review": classif["target_candidate_declared_for_review"],
        "may_select_target_for_build": False,
        "may_accept_for_build": False,
        "may_apply_runtime_patch": False,
        "may_modify_target_files": False,
        "may_open_c5": False,
        "may_grant_general_cell1_authority": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "must_not_infer": [
            "provided evidence means accepted for build",
            "candidate for review means selected target",
            "packet authorizes runtime patch",
            "packet authorizes target-file modification",
            "packet opens C5"
        ],
    }

def transition_trace(classif: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "provided_runtime_patch_target_evidence_packet_transition_trace_v0",
        "trace": [
            {
                "step": "consume_input_contract",
                "answer": SOURCE_INPUT_REQUEST_RECEIPT_ID,
                "taken": "require_explicit_env_inputs"
            },
            {
                "step": "emit_explicit_evidence_packet",
                "answer": classif["classification_status"],
                "taken": "stop_without_build_acceptance"
            }
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_EXPLICIT_TARGET_EVIDENCE_PACKET_READY_FOR_REVIEW" if classif["classification_status"] == "EXPLICIT_TARGET_EVIDENCE_PACKET_READY_FOR_REVIEW" else "STOP_EXPLICIT_TARGET_EVIDENCE_PACKET_INVALID",
            "next_command_goal": None,
        },
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    env_failures = validate_required_env()
    if env_failures:
        return emit_fail_receipt(env_failures, "STOP_EXPLICIT_TARGET_EVIDENCE_ENV_MISSING_OR_PLACEHOLDER")

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    source_failures = validate_source_basis()

    try:
        packet = build_packet()
    except ValueError as exc:
        return emit_fail_receipt([str(exc)], "STOP_EXPLICIT_TARGET_EVIDENCE_ENV_INVALID_JSON")

    write_json(PROVIDED_PACKET_PATH, packet)

    packet_failures = validate_packet(packet)
    all_failures = source_failures + packet_failures
    classif = classification(packet, all_failures)
    roll = rollup(classif)
    prof = profile(packet, classif, roll)
    rep = report(classif, roll)
    audit = authority_audit(classif)
    trace = transition_trace(classif)

    write_json(PROVIDED_PACKET_DIGEST_PATH, digest(packet))
    write_json(PROVIDED_PACKET_CLASSIFICATION_PATH, classif)
    write_json(ROLLUP_PATH, roll)
    write_json(PROFILE_PATH, prof)
    write_json(REPORT_PATH, rep)
    write_json(AUTHORITY_AUDIT_PATH, audit)
    write_json(TRANSITION_TRACE_PATH, trace)

    failures = list(all_failures)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        roll["source_mutation_count"] = 1
        rep["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, roll)
        write_json(REPORT_PATH, rep)

    acceptance_gate_results = {
        "EXPLICIT_TARGET_EVIDENCE_0_INPUT_REQUEST_RECEIPT_CONSUMED": SOURCE_INPUT_REQUEST_RECEIPT_PATH.exists(),
        "EXPLICIT_TARGET_EVIDENCE_1_REVIEW_RECEIPT_CONSUMED": SOURCE_REVIEW_RECEIPT_PATH.exists(),
        "EXPLICIT_TARGET_EVIDENCE_2_PACKET_EMITTED": PROVIDED_PACKET_PATH.exists(),
        "EXPLICIT_TARGET_EVIDENCE_3_PACKET_DIGEST_EMITTED": PROVIDED_PACKET_DIGEST_PATH.exists(),
        "EXPLICIT_TARGET_EVIDENCE_4_CLASSIFICATION_EMITTED": PROVIDED_PACKET_CLASSIFICATION_PATH.exists(),
        "EXPLICIT_TARGET_EVIDENCE_5_AUTHORITY_AUDIT_EMITTED": AUTHORITY_AUDIT_PATH.exists(),
        "EXPLICIT_TARGET_EVIDENCE_6_NO_TARGET_SELECTED_FOR_BUILD": classif.get("target_selected_for_build") is False,
        "EXPLICIT_TARGET_EVIDENCE_7_NO_ACCEPTED_FOR_BUILD": classif.get("accepted_for_build") is False,
        "EXPLICIT_TARGET_EVIDENCE_8_NO_RUNTIME_PATCH": classif.get("runtime_patch_authorized") is False,
        "EXPLICIT_TARGET_EVIDENCE_9_NO_TARGET_FILE_MODIFICATION": classif.get("target_file_modification_authorized") is False,
        "EXPLICIT_TARGET_EVIDENCE_10_NO_C5_OPENED": classif.get("c5_authorized") is False,
        "EXPLICIT_TARGET_EVIDENCE_11_NO_GENERAL_CELL1_AUTHORITY": classif.get("general_cell1_authority_granted") is False,
        "EXPLICIT_TARGET_EVIDENCE_12_NO_LATEST_FILE_GUESSING": roll.get("latest_file_guessing_count") == 0,
        "EXPLICIT_TARGET_EVIDENCE_13_NO_MTIME_SELECTION": roll.get("mtime_selection_count") == 0,
        "EXPLICIT_TARGET_EVIDENCE_14_NO_UNBOUNDED_PAYLOAD_INSPECTION": roll.get("unbounded_payload_inspection_count") == 0,
        "EXPLICIT_TARGET_EVIDENCE_15_NO_HIDDEN_NEXT_COMMAND": classif.get("next_command_goal") is None,
        "EXPLICIT_TARGET_EVIDENCE_16_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {"type": "STOP", "stop_code": "STOP_EXPLICIT_TARGET_EVIDENCE_PACKET_GATE_FAIL", "next_command_goal": None}

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "packet": packet,
        "classification": classif,
        "terminal": terminal,
        "gate": gate
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "provided_runtime_patch_target_evidence_packet_receipt_v0",
        "receipt_type": "PROVIDED_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_input_request_receipt_id": SOURCE_INPUT_REQUEST_RECEIPT_ID,
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "provided_packet_summary": {
            "classification_status": classif["classification_status"],
            "target_candidate_declared_for_review": classif["target_candidate_declared_for_review"],
            "target_candidate_ref": classif["target_candidate_ref"],
            "target_selected_for_build": False,
            "accepted_for_build": False,
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "general_cell1_authority_granted": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": prof["bad_counters_zero"],
            "recommended_next": classif["recommended_next"],
        },
        "aggregate_metrics": rep,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "provided_packet": rel(PROVIDED_PACKET_PATH),
            "provided_packet_digest": rel(PROVIDED_PACKET_DIGEST_PATH),
            "classification": rel(PROVIDED_PACKET_CLASSIFICATION_PATH),
            "authority_audit": rel(AUTHORITY_AUDIT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"provided_target_evidence_packet_receipt_id={receipt_id}")
    print(f"provided_target_evidence_packet_receipt_path={rel(receipt_path)}")
    print(f"provided_target_evidence_packet_path={rel(PROVIDED_PACKET_PATH)}")
    print(f"provided_target_evidence_packet_classification_path={rel(PROVIDED_PACKET_CLASSIFICATION_PATH)}")
    print(f"provided_target_evidence_packet_rollup_path={rel(ROLLUP_PATH)}")
    print(f"provided_target_evidence_packet_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
