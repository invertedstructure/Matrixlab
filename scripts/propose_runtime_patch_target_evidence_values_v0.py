#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shlex
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "MATERIALIZE_RUNTIME_PATCH_TARGET_EVIDENCE_VALUES_PROPOSER_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_evidence_values_proposer.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_EVIDENCE_VALUES_PROPOSER"
MODE = "PROPOSER / BOUNDED_EVIDENCE_VALUES / NO_ACCEPTANCE"
BUILD_MODE = "VALUES_PROPOSER_CAPABILITY_ONLY"

SOURCE_OPERATOR_VALUES_RECEIPT_ID = "1ac0b44d"
SOURCE_OPERATOR_VALUES_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_operator_values_v0_receipts/1ac0b44d.json"
SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_ID = "f3d0ae10"
SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_provider_materialization_v0_receipts/f3d0ae10.json"
SOURCE_INPUT_REQUEST_RECEIPT_ID = "ad527bfd"
SOURCE_INPUT_REQUEST_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_input_request_v0_receipts/ad527bfd.json"
SOURCE_INPUT_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_input_request_v0/explicit_runtime_patch_target_evidence_input_contract_v0.json"
SOURCE_REVIEW_RECEIPT_ID = "76b44fed"
SOURCE_REVIEW_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_packet_review_v0_receipts/76b44fed.json"
SOURCE_REVIEW_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_packet_review_v0/target_evidence_packet_review_classification_v0.json"
SOURCE_SCHEMA_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_request_v0/runtime_patch_target_evidence_packet_schema_v0.json"
SOURCE_HINT_INVENTORY_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_request_v0/target_hint_inventory_v0.json"
SOURCE_REQUEST_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_request_v0/narrower_runtime_patch_target_evidence_request_packet_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_evidence_values_proposer_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_evidence_values_proposer_v0_receipts"

PROPOSAL_PATH = OUT_DIR / "runtime_patch_target_evidence_values_proposal_v0.json"
PROPOSAL_ENV_EXPORTS_PATH = OUT_DIR / "runtime_patch_target_evidence_values_proposal_env_exports.sh"
CLASSIFICATION_PATH = OUT_DIR / "runtime_patch_target_evidence_values_proposer_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "runtime_patch_target_evidence_values_proposer_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_patch_target_evidence_values_proposer_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_patch_target_evidence_values_proposer_profile_v0.json"
REPORT_PATH = OUT_DIR / "runtime_patch_target_evidence_values_proposer_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "runtime_patch_target_evidence_values_proposer_transition_trace.json"

REQUIRED_ENV_FIELDS = [
    "SELECTED_TARGET_REF",
    "SELECTED_TARGET_KIND",
    "WHY_THIS_TARGET_IS_LOAD_BEARING",
    "WHY_OTHER_HINTS_ARE_NOT_TARGETS_JSON",
    "SOURCE_EVIDENCE_REFS_JSON",
    "VERIFICATION_GATE_REF",
    "ROLLBACK_OR_STOP_BOUNDARY_REF",
]

REQUIRED_SOURCE_FILES = [
    SOURCE_OPERATOR_VALUES_RECEIPT_PATH,
    SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_PATH,
    SOURCE_INPUT_REQUEST_RECEIPT_PATH,
    SOURCE_INPUT_CONTRACT_PATH,
    SOURCE_REVIEW_RECEIPT_PATH,
    SOURCE_REVIEW_CLASSIFICATION_PATH,
    SOURCE_SCHEMA_PATH,
    SOURCE_HINT_INVENTORY_PATH,
    SOURCE_REQUEST_PACKET_PATH,
]

SOURCE_EVIDENCE_BASE = [
    SOURCE_OPERATOR_VALUES_RECEIPT_PATH,
    SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_PATH,
    SOURCE_INPUT_REQUEST_RECEIPT_PATH,
    SOURCE_INPUT_CONTRACT_PATH,
    SOURCE_REVIEW_RECEIPT_PATH,
    SOURCE_REVIEW_CLASSIFICATION_PATH,
    SOURCE_SCHEMA_PATH,
    SOURCE_HINT_INVENTORY_PATH,
    SOURCE_REQUEST_PACKET_PATH,
]

ZERO_COUNTER_KEYS = [
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

def safe_local_bounded_path(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    if "EDIT_ME" in value or "FILL_ME" in value:
        return False
    if value.startswith("exact/"):
        return False
    p = Path(value)
    if p.is_absolute():
        return False
    if ".." in p.parts:
        return False
    if value.startswith(".git/"):
        return False
    return True

def validate_source_basis() -> List[str]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    operator_values = read_json(SOURCE_OPERATOR_VALUES_RECEIPT_PATH)
    provider = read_json(SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_PATH)
    input_receipt = read_json(SOURCE_INPUT_REQUEST_RECEIPT_PATH)
    input_contract = read_json(SOURCE_INPUT_CONTRACT_PATH)
    review = read_json(SOURCE_REVIEW_RECEIPT_PATH)
    review_classification = read_json(SOURCE_REVIEW_CLASSIFICATION_PATH)
    schema = read_json(SOURCE_SCHEMA_PATH)
    inventory = read_json(SOURCE_HINT_INVENTORY_PATH)

    if operator_values.get("receipt_id") != SOURCE_OPERATOR_VALUES_RECEIPT_ID or operator_values.get("gate") != "PASS":
        failures.append("operator_values_receipt_not_pass")
    if operator_values.get("operator_values_summary", {}).get("status") != "OPERATOR_TARGET_EVIDENCE_VALUES_MISSING_OR_INVALID":
        failures.append("operator_values_source_not_missing_or_invalid")
    if operator_values.get("terminal", {}).get("stop_code") != "STOP_OPERATOR_TARGET_EVIDENCE_VALUES_MISSING_OR_INVALID":
        failures.append("operator_values_wrong_terminal")

    if provider.get("receipt_id") != SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_ID or provider.get("gate") != "PASS":
        failures.append("provider_materialization_receipt_not_pass")
    if provider.get("provider_materialization_summary", {}).get("status") != "EXPLICIT_TARGET_EVIDENCE_PROVIDER_MATERIALIZED":
        failures.append("provider_not_materialized")

    if input_receipt.get("receipt_id") != SOURCE_INPUT_REQUEST_RECEIPT_ID or input_receipt.get("gate") != "PASS":
        failures.append("input_request_receipt_not_pass")
    if input_contract.get("required_env_fields") != REQUIRED_ENV_FIELDS:
        failures.append("input_contract_required_fields_changed")
    if input_contract.get("target_selected_for_build") is not False:
        failures.append("input_contract_selects_target_for_build")
    if input_contract.get("runtime_patch_authorized") is not False:
        failures.append("input_contract_authorizes_runtime_patch")

    if review.get("receipt_id") != SOURCE_REVIEW_RECEIPT_ID or review.get("gate") != "PASS":
        failures.append("review_receipt_not_pass")
    if review.get("terminal", {}).get("stop_code") != "STOP_TARGET_EVIDENCE_PACKET_MISSING":
        failures.append("review_wrong_terminal")
    if review_classification.get("review_status") != "TARGET_EVIDENCE_PACKET_MISSING":
        failures.append("review_status_not_missing")
    if review_classification.get("target_selected_for_build") is not False:
        failures.append("review_selected_target_for_build")
    if review_classification.get("accepted_for_build") is not False:
        failures.append("review_accepted_for_build")
    if review_classification.get("runtime_patch_authorized") is not False:
        failures.append("review_authorized_runtime_patch")

    if schema.get("packet_object_type") != "NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET":
        failures.append("schema_wrong_packet_object_type")
    if inventory.get("hint_count") != 13:
        failures.append(f"hint_count_not_13:{inventory.get('hint_count')}")
    if inventory.get("target_selected") is not False:
        failures.append("inventory_target_selected_unexpectedly")

    return failures

def walk(obj: Any, path: str = "") -> Iterable[Tuple[str, Any]]:
    yield path, obj
    if isinstance(obj, dict):
        for k, v in obj.items():
            next_path = f"{path}.{k}" if path else str(k)
            yield from walk(v, next_path)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            next_path = f"{path}[{i}]"
            yield from walk(v, next_path)

def candidate_ref_from_dict(d: Dict[str, Any]) -> Optional[str]:
    for key in [
        "selected_target_ref",
        "target_ref",
        "runtime_patch_target_ref",
        "candidate_target_ref",
        "candidate_ref",
        "artifact_ref",
        "file_ref",
        "source_ref",
        "path",
        "ref",
    ]:
        value = d.get(key)
        if safe_local_bounded_path(value):
            return value
    return None

def candidate_kind_from_dict(d: Dict[str, Any]) -> str:
    for key in ["selected_target_kind", "target_kind", "runtime_patch_target_kind", "candidate_kind", "hint_kind", "kind", "type", "object_type"]:
        value = d.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return "runtime_patch_target"

def has_explicit_target_marker(d: Dict[str, Any]) -> bool:
    for key in [
        "explicit_target_candidate",
        "target_candidate",
        "selected_target_candidate",
        "load_bearing_target_candidate",
        "single_target_candidate",
        "dominant_target_candidate",
        "proposer_selected",
    ]:
        if d.get(key) is True:
            return True

    for key in ["status", "classification", "role", "candidate_status", "decision"]:
        value = d.get(key)
        if isinstance(value, str) and value in {
            "TARGET_CANDIDATE",
            "SELECTED_TARGET_CANDIDATE",
            "LOAD_BEARING_TARGET_CANDIDATE",
            "SINGLE_TARGET_CANDIDATE",
            "DOMINANT_TARGET_CANDIDATE",
        }:
            return True

    return False

def extract_candidate_hints(inventory: Dict[str, Any]) -> List[Dict[str, Any]]:
    hints: List[Dict[str, Any]] = []
    seen = set()

    for path, obj in walk(inventory):
        if isinstance(obj, dict):
            ref = candidate_ref_from_dict(obj)
            if ref and ref not in seen:
                seen.add(ref)
                hints.append({
                    "hint_id": obj.get("hint_id") or obj.get("id") or path,
                    "ref": ref,
                    "kind": candidate_kind_from_dict(obj),
                    "explicit_target_marker": has_explicit_target_marker(obj),
                    "source_path": path,
                    "raw_keys": sorted(str(k) for k in obj.keys()),
                })

    return hints

def find_semantic_ref(objs: List[Tuple[str, Dict[str, Any]]], include_terms: List[str], preferred_fallback: Optional[str] = None) -> Optional[str]:
    candidates: List[str] = []
    for source_name, obj in objs:
        for path, value in walk(obj):
            lower_path = path.lower()
            if all(term in lower_path for term in include_terms) and safe_local_bounded_path(value):
                candidates.append(value)
    unique = sorted(set(candidates))
    if len(unique) == 1:
        return unique[0]
    return preferred_fallback

def classify_and_build_values() -> Tuple[str, List[str], Dict[str, Any], Dict[str, Any]]:
    inventory = read_json(SOURCE_HINT_INVENTORY_PATH)
    request_packet = read_json(SOURCE_REQUEST_PACKET_PATH)
    input_contract = read_json(SOURCE_INPUT_CONTRACT_PATH)
    schema = read_json(SOURCE_SCHEMA_PATH)
    review_classification = read_json(SOURCE_REVIEW_CLASSIFICATION_PATH)

    hints = extract_candidate_hints(inventory)
    unique_hints: Dict[str, Dict[str, Any]] = {h["ref"]: h for h in hints}
    marked = [h for h in unique_hints.values() if h["explicit_target_marker"]]

    source_objs = [
        (rel(SOURCE_HINT_INVENTORY_PATH), inventory),
        (rel(SOURCE_REQUEST_PACKET_PATH), request_packet),
        (rel(SOURCE_INPUT_CONTRACT_PATH), input_contract),
        (rel(SOURCE_SCHEMA_PATH), schema),
        (rel(SOURCE_REVIEW_CLASSIFICATION_PATH), review_classification),
    ]

    reason_codes: List[str] = []
    selected_hint: Optional[Dict[str, Any]] = None

    if len(marked) == 1:
        selected_hint = marked[0]
    elif len(marked) > 1:
        reason_codes.append("MULTIPLE_EXPLICIT_TARGET_MARKERS")
    elif len(unique_hints) == 1:
        selected_hint = list(unique_hints.values())[0]
    elif len(unique_hints) > 1:
        reason_codes.append("MULTIPLE_BOUNDED_TARGETS_NO_DOMINANCE")
    else:
        reason_codes.append("NO_BOUNDED_TARGET_VALUE_SOURCE")

    verification_gate_ref = find_semantic_ref(source_objs, ["verification", "gate"])
    rollback_or_stop_boundary_ref = (
        find_semantic_ref(source_objs, ["rollback", "boundary"])
        or find_semantic_ref(source_objs, ["stop", "boundary"])
        or find_semantic_ref(source_objs, ["rollback"])
    )

    if not verification_gate_ref:
        reason_codes.append("MISSING_VERIFICATION_GATE_REF")
    if not rollback_or_stop_boundary_ref:
        reason_codes.append("MISSING_ROLLBACK_OR_STOP_BOUNDARY_REF")

    if selected_hint and not safe_local_bounded_path(selected_hint["ref"]):
        reason_codes.append("SELECTED_TARGET_REF_NOT_LOCAL_BOUNDED")

    if reason_codes:
        if "MULTIPLE_BOUNDED_TARGETS_NO_DOMINANCE" in reason_codes:
            status = "MULTIPLE_BOUNDED_TARGETS_NO_DOMINANCE"
        elif "MULTIPLE_EXPLICIT_TARGET_MARKERS" in reason_codes:
            status = "MULTIPLE_BOUNDED_TARGETS_NO_DOMINANCE"
        elif "NO_BOUNDED_TARGET_VALUE_SOURCE" in reason_codes:
            status = "NO_BOUNDED_TARGET_VALUE_SOURCE"
        elif "MISSING_VERIFICATION_GATE_REF" in reason_codes:
            status = "MISSING_VERIFICATION_GATE_REF"
        elif "MISSING_ROLLBACK_OR_STOP_BOUNDARY_REF" in reason_codes:
            status = "MISSING_ROLLBACK_OR_STOP_BOUNDARY_REF"
        else:
            status = "VALUES_PROPOSAL_NOT_READY"
    else:
        status = "VALUES_PROPOSAL_READY"

    field_source_map: Dict[str, Any] = {
        "candidate_hint_count": len(unique_hints),
        "explicit_target_marker_count": len(marked),
        "candidate_hints": list(unique_hints.values()),
        "source_evidence_base": [rel(p) for p in SOURCE_EVIDENCE_BASE],
        "verification_gate_ref_source": "bounded semantic extraction from allowed evidence surfaces" if verification_gate_ref else None,
        "rollback_or_stop_boundary_ref_source": "bounded semantic extraction from allowed evidence surfaces" if rollback_or_stop_boundary_ref else None,
    }

    candidate_values: Dict[str, Any] = {}
    if status == "VALUES_PROPOSAL_READY" and selected_hint:
        other_reasons = []
        for ref, h in sorted(unique_hints.items()):
            if ref == selected_hint["ref"]:
                continue
            other_reasons.append({
                "hint_ref": ref,
                "reason": "not selected because exactly one bounded target candidate carried the explicit dominance marker, while this hint remained non-dominant context",
                "source_path": h["source_path"],
            })

        candidate_values = {
            "SELECTED_TARGET_REF": selected_hint["ref"],
            "SELECTED_TARGET_KIND": selected_hint["kind"],
            "WHY_THIS_TARGET_IS_LOAD_BEARING": (
                "Selected by bounded evidence-values proposer because exactly one allowed evidence-surface hint "
                "resolved as the runtime patch target candidate, and provider/intake receipts show the only remaining blocker is target-evidence values."
            ),
            "WHY_OTHER_HINTS_ARE_NOT_TARGETS_JSON": json.dumps(other_reasons),
            "SOURCE_EVIDENCE_REFS_JSON": json.dumps([rel(p) for p in SOURCE_EVIDENCE_BASE]),
            "VERIFICATION_GATE_REF": verification_gate_ref,
            "ROLLBACK_OR_STOP_BOUNDARY_REF": rollback_or_stop_boundary_ref,
        }

        field_source_map.update({
            "SELECTED_TARGET_REF": {"value": selected_hint["ref"], "source": selected_hint["source_path"]},
            "SELECTED_TARGET_KIND": {"value": selected_hint["kind"], "source": selected_hint["source_path"]},
            "WHY_THIS_TARGET_IS_LOAD_BEARING": {"source": [rel(SOURCE_OPERATOR_VALUES_RECEIPT_PATH), rel(SOURCE_HINT_INVENTORY_PATH)]},
            "WHY_OTHER_HINTS_ARE_NOT_TARGETS_JSON": {"source": rel(SOURCE_HINT_INVENTORY_PATH), "other_hint_count": len(other_reasons)},
            "SOURCE_EVIDENCE_REFS_JSON": {"source": "fixed allowed evidence surface list"},
            "VERIFICATION_GATE_REF": {"value": verification_gate_ref},
            "ROLLBACK_OR_STOP_BOUNDARY_REF": {"value": rollback_or_stop_boundary_ref},
        })

    return status, reason_codes, candidate_values, field_source_map

def write_env_exports(values: Dict[str, Any]) -> None:
    lines = [
        "# Proposed values only. Human/prevalidated-schema acceptance boundary still applies.",
        "# Source this file only to test the existing intake/provider path; it does not authorize build acceptance or patching.",
    ]
    for field in REQUIRED_ENV_FIELDS:
        lines.append(f"export {field}={shlex.quote(str(values[field]))}")
    lines.append("")
    PROPOSAL_ENV_EXPORTS_PATH.write_text("\n".join(lines))

def stop_code_for_status(status: str) -> str:
    return {
        "VALUES_PROPOSAL_READY": "STOP_RUNTIME_PATCH_TARGET_EVIDENCE_VALUES_PROPOSAL_READY",
        "NO_BOUNDED_TARGET_VALUE_SOURCE": "STOP_NO_BOUNDED_TARGET_VALUE_SOURCE",
        "MULTIPLE_BOUNDED_TARGETS_NO_DOMINANCE": "STOP_MULTIPLE_BOUNDED_TARGETS_NO_DOMINANCE",
        "MISSING_VERIFICATION_GATE_REF": "STOP_MISSING_VERIFICATION_GATE_REF",
        "MISSING_ROLLBACK_OR_STOP_BOUNDARY_REF": "STOP_MISSING_ROLLBACK_OR_STOP_BOUNDARY_REF",
    }.get(status, "STOP_RUNTIME_PATCH_TARGET_EVIDENCE_VALUES_PROPOSAL_NOT_READY")

def proposal_obj(status: str, reason_codes: List[str], values: Dict[str, Any], field_source_map: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "runtime_patch_target_evidence_values_proposal_v0",
        "proposal_type": "RUNTIME_PATCH_TARGET_EVIDENCE_VALUES_PROPOSAL",
        "proposal_id": "values_proposal_" + sha8({"status": status, "values": values, "reasons": reason_codes}),
        "proposal_status": status,
        "reason_codes": reason_codes,
        "candidate_values": values if status == "VALUES_PROPOSAL_READY" else {},
        "field_source_map": field_source_map,
        "source_operator_values_receipt_id": SOURCE_OPERATOR_VALUES_RECEIPT_ID,
        "source_provider_materialization_receipt_id": SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_ID,
        "source_input_request_receipt_id": SOURCE_INPUT_REQUEST_RECEIPT_ID,
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "recommended_next": "REVIEW_RUNTIME_PATCH_TARGET_EVIDENCE_VALUES_PROPOSAL_V0" if status == "VALUES_PROPOSAL_READY" else "REPAIR_OR_NARROW_RUNTIME_PATCH_TARGET_EVIDENCE_VALUES_PROPOSER_INPUTS_V0",
    }

def classification_obj(proposal: Dict[str, Any]) -> Dict[str, Any]:
    status = proposal["proposal_status"]
    ready = status == "VALUES_PROPOSAL_READY"
    return {
        "schema_version": "runtime_patch_target_evidence_values_proposer_classification_v0",
        "classification_status": status,
        "proposal_ready": ready,
        "reason_codes": proposal["reason_codes"],
        "candidate_values_filled_count": len(proposal["candidate_values"]) if ready else 0,
        "required_values_count": len(REQUIRED_ENV_FIELDS),
        "target_candidate_proposed_count": 1 if ready else 0,
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "recommended_next": proposal["recommended_next"],
        "next_command_goal": None,
    }

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "runtime_patch_target_evidence_values_proposer_authority_boundary_v0",
        "status": status,
        "may_inspect_allowed_evidence_surfaces": True,
        "may_emit_candidate_values_proposal": True,
        "may_emit_env_exports_if_proposal_ready": status == "VALUES_PROPOSAL_READY",
        "may_declare_target_candidate_for_review": False,
        "may_select_target_for_build": False,
        "may_accept_for_build": False,
        "may_apply_runtime_patch": False,
        "may_modify_target_files": False,
        "may_open_c5": False,
        "may_grant_general_cell1_authority": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "must_not_infer": [
            "proposed values are accepted values",
            "proposed target ref is selected for build",
            "proposal authorizes patching",
            "ambiguity can be collapsed by preference",
            "13 bounded hints imply one target"
        ],
    }

def rollup_obj(status: str) -> Dict[str, Any]:
    ready = status == "VALUES_PROPOSAL_READY"
    return {
        "schema_version": "runtime_patch_target_evidence_values_proposer_rollup_v0",
        "build_mode": BUILD_MODE,
        "values_proposal_ready_count": 1 if ready else 0,
        "values_proposal_not_ready_count": 0 if ready else 1,
        "target_candidate_proposed_count": 1 if ready else 0,
        "target_candidate_declared_for_review_count": 0,
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
        "recommended_next": "REVIEW_RUNTIME_PATCH_TARGET_EVIDENCE_VALUES_PROPOSAL_V0" if ready else "REPAIR_OR_NARROW_RUNTIME_PATCH_TARGET_EVIDENCE_VALUES_PROPOSER_INPUTS_V0",
    }

def profile_obj(status: str, roll: Dict[str, Any], proposal: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "runtime_patch_target_evidence_values_proposer_profile_v0",
        "profile_id": "values_proposer_" + sha8({"status": status, "proposal": proposal}),
        "status": status,
        "proposal_ready": status == "VALUES_PROPOSAL_READY",
        "target_candidate_proposed": status == "VALUES_PROPOSAL_READY",
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": all(roll.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "recommended_next": roll["recommended_next"],
        "next_command_goal": None,
    }

def report_obj(status: str, proposal: Dict[str, Any], roll: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "runtime_patch_target_evidence_values_proposer_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": proposal["reason_codes"],
        "candidate_values_filled_count": len(proposal["candidate_values"]),
        "acceptance_boundary": proposal["acceptance_boundary"],
        "recommended_next_handling": roll["recommended_next"],
        "target_candidate_proposed_count": roll["target_candidate_proposed_count"],
        "target_candidate_declared_for_review_count": 0,
        "target_selected_for_build_count": 0,
        "accepted_for_build_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
    }

def trace_obj(status: str, reason_codes: List[str]) -> Dict[str, Any]:
    return {
        "schema_version": "runtime_patch_target_evidence_values_proposer_transition_trace_v0",
        "trace": [
            {
                "step": "consume_missing_values_checker_halt",
                "question": "is the checker missing or are the values missing",
                "answer": "checker exists; values are missing",
                "taken": "materialize_bounded_values_proposer",
            },
            {
                "step": "inspect_allowed_evidence_surfaces",
                "question": "can exactly one target-evidence value set be proposed without guessing",
                "answer": status,
                "reason_codes": reason_codes,
                "taken": "emit_proposal_or_typed_halt_without_acceptance",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": stop_code_for_status(status),
            "next_command_goal": None,
        },
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    source_failures = validate_source_basis()

    if source_failures:
        status = "SOURCE_BASIS_FAIL"
        reason_codes = source_failures
        values: Dict[str, Any] = {}
        field_source_map: Dict[str, Any] = {}
    else:
        status, reason_codes, values, field_source_map = classify_and_build_values()

    proposal = proposal_obj(status, reason_codes, values, field_source_map)
    classif = classification_obj(proposal)
    boundary = authority_boundary_obj(status)
    roll = rollup_obj(status)
    prof = profile_obj(status, roll, proposal)
    rep = report_obj(status, proposal, roll)
    tr = trace_obj(status, reason_codes)

    write_json(PROPOSAL_PATH, proposal)
    if status == "VALUES_PROPOSAL_READY":
        write_env_exports(values)
    elif PROPOSAL_ENV_EXPORTS_PATH.exists():
        PROPOSAL_ENV_EXPORTS_PATH.unlink()

    write_json(CLASSIFICATION_PATH, classif)
    write_json(AUTHORITY_BOUNDARY_PATH, boundary)
    write_json(ROLLUP_PATH, roll)
    write_json(PROFILE_PATH, prof)
    write_json(REPORT_PATH, rep)
    write_json(TRANSITION_TRACE_PATH, tr)

    failures: List[str] = []
    if source_failures:
        failures.extend(source_failures)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        roll["source_mutation_count"] = 1
        rep["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, roll)
        write_json(REPORT_PATH, rep)

    acceptance_gate_results = {
        "VALUES_PROPOSER_0_OPERATOR_VALUES_RECEIPT_CONSUMED": SOURCE_OPERATOR_VALUES_RECEIPT_PATH.exists(),
        "VALUES_PROPOSER_1_PROVIDER_MATERIALIZATION_RECEIPT_CONSUMED": SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_PATH.exists(),
        "VALUES_PROPOSER_2_INPUT_CONTRACT_CONSUMED": SOURCE_INPUT_CONTRACT_PATH.exists(),
        "VALUES_PROPOSER_3_HINT_INVENTORY_CONSUMED": SOURCE_HINT_INVENTORY_PATH.exists(),
        "VALUES_PROPOSER_4_PROPOSAL_EMITTED": PROPOSAL_PATH.exists(),
        "VALUES_PROPOSER_5_CLASSIFICATION_EMITTED": CLASSIFICATION_PATH.exists(),
        "VALUES_PROPOSER_6_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classif["target_candidate_declared_for_review"] is False,
        "VALUES_PROPOSER_7_NO_TARGET_SELECTED_FOR_BUILD": classif["target_selected_for_build"] is False,
        "VALUES_PROPOSER_8_NO_ACCEPTED_FOR_BUILD": classif["accepted_for_build"] is False,
        "VALUES_PROPOSER_9_NO_RUNTIME_PATCH": classif["runtime_patch_authorized"] is False,
        "VALUES_PROPOSER_10_NO_TARGET_FILE_MODIFICATION": classif["target_file_modification_authorized"] is False,
        "VALUES_PROPOSER_11_NO_C5_OPENED": classif["c5_authorized"] is False,
        "VALUES_PROPOSER_12_NO_GENERAL_CELL1_AUTHORITY": classif["general_cell1_authority_granted"] is False,
        "VALUES_PROPOSER_13_NO_LATEST_FILE_GUESSING": classif["latest_file_guessing"] is False,
        "VALUES_PROPOSER_14_NO_MTIME_SELECTION": classif["mtime_selection"] is False,
        "VALUES_PROPOSER_15_NO_HIDDEN_NEXT_COMMAND": classif["next_command_goal"] is None,
        "VALUES_PROPOSER_16_ACCEPTANCE_BOUNDARY_RETAINED": boundary["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "VALUES_PROPOSER_17_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = tr["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_RUNTIME_PATCH_TARGET_EVIDENCE_VALUES_PROPOSER_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "proposal": proposal,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "runtime_patch_target_evidence_values_proposer_receipt_v0",
        "receipt_type": "RUNTIME_PATCH_TARGET_EVIDENCE_VALUES_PROPOSER_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_operator_values_receipt_id": SOURCE_OPERATOR_VALUES_RECEIPT_ID,
        "source_provider_materialization_receipt_id": SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_ID,
        "source_input_request_receipt_id": SOURCE_INPUT_REQUEST_RECEIPT_ID,
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "values_proposer_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "proposal_ready": status == "VALUES_PROPOSAL_READY",
            "candidate_values_filled_count": len(values),
            "target_candidate_proposed": status == "VALUES_PROPOSAL_READY",
            "target_candidate_declared_for_review": False,
            "target_selected_for_build": False,
            "accepted_for_build": False,
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "general_cell1_authority_granted": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
            "bad_counters_zero": prof["bad_counters_zero"],
            "recommended_next": prof["recommended_next"],
        },
        "aggregate_metrics": rep,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "proposal": rel(PROPOSAL_PATH),
            "proposal_env_exports": rel(PROPOSAL_ENV_EXPORTS_PATH) if PROPOSAL_ENV_EXPORTS_PATH.exists() else None,
            "classification": rel(CLASSIFICATION_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
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
    print(f"values_proposer_receipt_id={receipt_id}")
    print(f"values_proposer_receipt_path={rel(receipt_path)}")
    print(f"values_proposal_path={rel(PROPOSAL_PATH)}")
    print(f"values_proposal_env_exports_path={rel(PROPOSAL_ENV_EXPORTS_PATH) if PROPOSAL_ENV_EXPORTS_PATH.exists() else ''}")
    print(f"values_proposer_classification_path={rel(CLASSIFICATION_PATH)}")
    print(f"values_proposer_rollup_path={rel(ROLLUP_PATH)}")
    print(f"values_proposer_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
