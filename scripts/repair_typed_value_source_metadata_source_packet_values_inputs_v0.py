#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REPAIR_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUTS_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_packet_values_input_repair.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUT_REPAIR"
MODE = "VALUES_INPUT_REPAIR_SURFACE / NO_METADATA_FILL / NO_TIE_BREAK / NO_ACCEPTANCE"
BUILD_MODE = "VALUES_INPUT_REPAIR_ONLY"

SOURCE_VALUES_RECEIPT_ID = "34444c0b"
SOURCE_VALUES_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_v0_receipts/34444c0b.json"
SOURCE_VALUES_INPUT_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_v0/typed_value_source_metadata_source_packet_values_input_contract_v0.json"
SOURCE_VALUES_REQUEST_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_v0/typed_value_source_metadata_source_packet_values_request_v0.json"
SOURCE_VALUES_ENV_TEMPLATE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_v0/typed_value_source_metadata_source_packet_values_env_template_v0.sh"
SOURCE_VALUES_PACKET_DRAFT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_v0/typed_value_source_metadata_source_packet_values_packet_draft_v0.json"
SOURCE_VALUES_MISSING_FIELDS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_v0/typed_value_source_metadata_source_packet_values_missing_fields_v0.json"
SOURCE_VALUES_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_v0/typed_value_source_metadata_source_packet_values_classification_v0.json"
SOURCE_VALUES_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_v0/typed_value_source_metadata_source_packet_values_rollup_v0.json"
SOURCE_VALUES_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_v0/typed_value_source_metadata_source_packet_values_profile_v0.json"

SOURCE_BRIDGE_RECEIPT_ID = "68a12602"
SOURCE_BRIDGE_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0_receipts/68a12602.json"
SOURCE_FIELD_POLICY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_source_field_policy_v0.json"
SOURCE_ROW_REQUIREMENTS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_row_source_requirements_v0.json"
SOURCE_HUMAN_SCHEMA_ONLY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_human_schema_only_fields_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0_receipts"

REPAIR_SURFACE_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_input_repair_surface_v0.json"
SLOT_INVENTORY_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_slot_inventory_v0.json"
MACHINE_SOURCE_SLOTS_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_machine_source_slots_v0.json"
HUMAN_SCHEMA_SLOTS_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_human_schema_slots_v0.json"
PAYLOAD_TEMPLATE_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_payload_template_v0.json"
ENV_EXPORTS_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_repair_env_exports_v0.sh"
REVIEW_RERUN_CONTRACT_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_review_rerun_contract_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_input_repair_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_input_repair_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_input_repair_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_input_repair_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_input_repair_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_input_repair_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_VALUES_RECEIPT_PATH,
    SOURCE_VALUES_INPUT_CONTRACT_PATH,
    SOURCE_VALUES_REQUEST_PATH,
    SOURCE_VALUES_ENV_TEMPLATE_PATH,
    SOURCE_VALUES_PACKET_DRAFT_PATH,
    SOURCE_VALUES_MISSING_FIELDS_PATH,
    SOURCE_VALUES_CLASSIFICATION_PATH,
    SOURCE_VALUES_ROLLUP_PATH,
    SOURCE_VALUES_PROFILE_PATH,
    SOURCE_BRIDGE_RECEIPT_PATH,
    SOURCE_FIELD_POLICY_PATH,
    SOURCE_ROW_REQUIREMENTS_PATH,
    SOURCE_HUMAN_SCHEMA_ONLY_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUT_INVALID"
EXPECTED_SOURCE_STOP = "STOP_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUT_INVALID"
EXPECTED_NEXT = "REPAIR_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUTS_V0"

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

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    receipt = read_json(SOURCE_VALUES_RECEIPT_PATH)
    summary = receipt.get("typed_metadata_source_packet_values_summary", {})
    classif = read_json(SOURCE_VALUES_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_VALUES_ROLLUP_PATH)
    profile = read_json(SOURCE_VALUES_PROFILE_PATH)
    missing = read_json(SOURCE_VALUES_MISSING_FIELDS_PATH)
    draft = read_json(SOURCE_VALUES_PACKET_DRAFT_PATH)
    bridge_receipt = read_json(SOURCE_BRIDGE_RECEIPT_PATH)
    bridge_summary = bridge_receipt.get("typed_metadata_source_bridge_summary", {})

    if receipt.get("receipt_id") != SOURCE_VALUES_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_values_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_values_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_values_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"source_values_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("values_input_present") is not False:
        failures.append("source_values_input_present_unexpectedly")
    if summary.get("values_source") is not None:
        failures.append("source_values_source_unexpectedly_present")
    if summary.get("complete_value_slot_count") != 0:
        failures.append("source_values_complete_slots_nonzero")
    if summary.get("missing_value_slot_count") != 30:
        failures.append(f"source_values_missing_slots_not_30:{summary.get('missing_value_slot_count')}")
    if summary.get("source_packet_materialized_for_review") is not False:
        failures.append("source_packet_materialized_unexpectedly")
    if summary.get("metadata_populated") is not False:
        failures.append("source_metadata_populated_unexpectedly")
    if summary.get("rule_refined") is not False:
        failures.append("source_rule_refined_unexpectedly")
    if summary.get("tie_broken") is not False:
        failures.append("source_tie_broken_unexpectedly")
    if summary.get("candidate_values_filled") is not False:
        failures.append("source_candidate_values_filled_unexpectedly")

    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("source_values_classification_status_wrong")
    if roll.get("metadata_populated_count") != 0:
        failures.append("source_values_rollup_metadata_populated_nonzero")
    if profile.get("metadata_populated") is not False:
        failures.append("source_values_profile_metadata_populated_true")
    if missing.get("missing_value_slot_count") != 30:
        failures.append("missing_fields_artifact_missing_slot_count_not_30")
    if draft.get("object_type") != "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET":
        failures.append("values_packet_draft_object_type_wrong")

    if bridge_receipt.get("receipt_id") != SOURCE_BRIDGE_RECEIPT_ID or bridge_receipt.get("gate") != "PASS":
        failures.append("source_bridge_receipt_not_pass")
    if bridge_summary.get("status") != "TYPED_VALUE_SOURCE_METADATA_SOURCE_BRIDGE_BUILT_REQUIRES_SOURCE_PACKET":
        failures.append("source_bridge_status_wrong")

    return failures

def field_policies() -> Dict[str, Dict[str, Any]]:
    policy = read_json(SOURCE_FIELD_POLICY_PATH)
    out = {}
    for p in policy.get("field_policies", []):
        if isinstance(p, dict) and p.get("field"):
            out[str(p["field"])] = p
    return out

def build_slot_inventory() -> List[Dict[str, Any]]:
    draft = read_json(SOURCE_VALUES_PACKET_DRAFT_PATH)
    policies = field_policies()
    rows = draft.get("rows", [])
    inventory: List[Dict[str, Any]] = []

    for row in rows:
        if not isinstance(row, dict):
            continue
        for item in row.get("missing_metadata_to_supply", []):
            if not isinstance(item, dict):
                continue
            field = str(item.get("field"))
            policy = policies.get(field, {})
            source_class = item.get("source_class") or policy.get("source_class")
            human_schema_only = bool(item.get("human_schema_only") or policy.get("human_schema_only"))
            slot = {
                "slot_id": "slot_" + sha8({
                    "row_uid": row.get("row_uid"),
                    "field": field,
                    "source_class": source_class,
                }),
                "row_uid": row.get("row_uid"),
                "row_index": row.get("row_index"),
                "row_source_ref": row.get("source_ref"),
                "row_json_path": row.get("json_path"),
                "row_value": row.get("value"),
                "field": field,
                "source_class": source_class,
                "required_source_object": item.get("required_source_object") or policy.get("required_source_object"),
                "human_schema_only": human_schema_only,
                "allowed_sources": policy.get("allowed_sources", []),
                "required_value_shape": {
                    "value": "non-null",
                    "source_ref": "required unless evidence_or_review_ref is supplied",
                    "evidence_or_review_ref": "required for human/schema-only fields",
                    "source_class": source_class,
                    "notes": "optional",
                },
                "current_value": item.get("value"),
                "current_source_ref": item.get("source_ref"),
                "current_evidence_or_review_ref": item.get("evidence_or_review_ref"),
                "slot_status": "VALUE_REQUIRED",
            }
            inventory.append(slot)
    return inventory

def split_slots(inventory: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    human_schema = [s for s in inventory if s.get("human_schema_only")]
    machine = [s for s in inventory if not s.get("human_schema_only")]
    return machine, human_schema

def values_by_row_uid_template(inventory: List[Dict[str, Any]]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for slot in inventory:
        row_uid = str(slot["row_uid"])
        out.setdefault(row_uid, {})
        out[row_uid][slot["field"]] = {
            "value": None,
            "source_ref": None,
            "source_class": slot["source_class"],
            "evidence_or_review_ref": None,
            "notes": None,
        }
    return out

def build_payload_template(inventory: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_payload_template_v0",
        "payload_template_id": "source_packet_values_payload_template_" + sha8(inventory),
        "accepted_input_shape": {
            "values_by_row_uid": values_by_row_uid_template(inventory),
        },
        "alternative_input_shape": "full TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET object from values_packet_draft with nulls filled",
        "required_slot_count": len(inventory),
        "fill_rules": [
            "Every supplied value must include source_ref or evidence_or_review_ref.",
            "human_schema_only=true slots require evidence_or_review_ref.",
            "source_class must match the slot source_class.",
            "Do not infer from latest file, mtime, row order, or dominance score.",
        ],
        "forbidden_actions": [
            "metadata population",
            "discriminator evaluation",
            "dominance rule refinement",
            "tie break",
            "target candidate declaration",
            "target selection",
            "acceptance for build",
            "runtime patch",
            "C5 opening",
        ],
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def build_surface(inventory: List[Dict[str, Any]], machine_slots: List[Dict[str, Any]], human_slots: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_input_repair_surface_v0",
        "repair_surface_id": "values_input_repair_surface_" + sha8(inventory),
        "source_values_receipt_id": SOURCE_VALUES_RECEIPT_ID,
        "source_packet_review_receipt_id": "90cb2053",
        "source_bridge_receipt_id": SOURCE_BRIDGE_RECEIPT_ID,
        "repair_status": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUT_REPAIR_SURFACE_BUILT_REQUIRES_VALUES",
        "receipt_backed_claim": "Values packet contract exists but no values payload was provided.",
        "required_slot_count": len(inventory),
        "machine_readable_slot_count": len(machine_slots),
        "human_or_schema_slot_count": len(human_slots),
        "slot_inventory_ref": rel(SLOT_INVENTORY_PATH),
        "machine_source_slots_ref": rel(MACHINE_SOURCE_SLOTS_PATH),
        "human_schema_slots_ref": rel(HUMAN_SCHEMA_SLOTS_PATH),
        "payload_template_ref": rel(PAYLOAD_TEMPLATE_PATH),
        "values_packet_draft_ref": rel(SOURCE_VALUES_PACKET_DRAFT_PATH),
        "values_input_contract_ref": rel(SOURCE_VALUES_INPUT_CONTRACT_PATH),
        "next_input_env_json": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_JSON",
        "next_input_env_path": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_PATH",
        "not_authorized": [
            "fill metadata",
            "evaluate discriminators",
            "refine dominance rule",
            "break tie",
            "fill candidate values",
            "declare target candidate for review",
            "select target for build",
            "accept for build",
            "apply runtime patch",
            "open C5",
            "grant general Cell1 authority",
            "latest-file guessing",
            "mtime selection",
        ],
        "recommended_next": "SUPPLY_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUTS_V0",
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def build_review_rerun_contract() -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_review_rerun_contract_v0",
        "contract_status": "VALUES_INPUT_REPAIR_BUILT_REVIEW_RERUN_CONTRACT_EMITTED",
        "step_1_supply_values_to": [
            "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_JSON",
            "or TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_PATH",
        ],
        "step_2_rerun_unit": "PROVIDE_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_V0",
        "step_3_if_packet_materialized_set": {
            "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_PATH": rel(SOURCE_VALUES_PACKET_DRAFT_PATH),
        },
        "step_4_review_unit": "PROVIDE_OR_REVIEW_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_V0",
        "must_not_skip_to": [
            "metadata population",
            "discriminator evaluation",
            "dominance rule refinement",
            "tie break",
            "runtime patch",
        ],
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def classify(inventory: List[Dict[str, Any]], machine_slots: List[Dict[str, Any]], human_slots: List[Dict[str, Any]]) -> Tuple[str, List[str], str]:
    reason_codes = [
        "VALUES_INPUT_REPAIR_SURFACE_EMITTED",
        "VALUES_SLOT_INVENTORY_EMITTED",
        "MACHINE_READABLE_AND_HUMAN_SCHEMA_SLOTS_SPLIT",
        "PAYLOAD_TEMPLATE_EMITTED",
        "VALUES_STILL_NOT_SUPPLIED",
    ]
    if machine_slots:
        reason_codes.append("MACHINE_READABLE_SOURCE_VALUES_REQUIRED")
    if human_slots:
        reason_codes.append("HUMAN_OR_SCHEMA_VALUES_REQUIRED")
    status = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUT_REPAIR_SURFACE_BUILT_REQUIRES_VALUES"
    next_edge = "SUPPLY_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUTS_V0"
    return status, reason_codes, next_edge

def classification_obj(status: str, reason_codes: List[str], next_edge: str, inventory: List[Dict[str, Any]], machine_slots: List[Dict[str, Any]], human_slots: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_input_repair_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "required_slot_count": len(inventory),
        "machine_readable_slot_count": len(machine_slots),
        "human_or_schema_slot_count": len(human_slots),
        "values_supplied": False,
        "source_packet_materialized_for_review": False,
        "metadata_populated": False,
        "ready_discriminator_count": 0,
        "real_tie_proven": False,
        "rule_refined": False,
        "tie_broken": False,
        "candidate_values_filled": False,
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "recommended_next": next_edge,
        "next_command_goal": None,
    }

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_input_repair_authority_boundary_v0",
        "status": status,
        "may_emit_input_repair_surface": True,
        "may_emit_payload_template": True,
        "may_split_machine_vs_human_schema_slots": True,
        "may_supply_values": False,
        "may_materialize_source_packet_for_review": False,
        "may_populate_metadata": False,
        "may_evaluate_discriminators": False,
        "may_refine_rule": False,
        "may_break_tie": False,
        "may_emit_candidate_values": False,
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
    }

def rollup_obj(status: str, inventory: List[Dict[str, Any]], machine_slots: List[Dict[str, Any]], human_slots: List[Dict[str, Any]], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_input_repair_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "repair_surface_emitted_count": 1,
        "slot_inventory_emitted_count": 1,
        "payload_template_emitted_count": 1,
        "env_exports_emitted_count": 1,
        "required_slot_count": len(inventory),
        "machine_readable_slot_count": len(machine_slots),
        "human_or_schema_slot_count": len(human_slots),
        "values_supplied_count": 0,
        "source_packet_materialized_for_review_count": 0,
        "metadata_populated_count": 0,
        "ready_discriminator_count": 0,
        "rule_refined_count": 0,
        "tie_broken_count": 0,
        "candidate_values_filled_count": 0,
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
        "recommended_next": next_edge,
    }

def profile_obj(roll: Dict[str, Any]) -> Dict[str, Any]:
    zero_keys = [
        "values_supplied_count",
        "source_packet_materialized_for_review_count",
        "metadata_populated_count",
        "ready_discriminator_count",
        "rule_refined_count",
        "tie_broken_count",
        "candidate_values_filled_count",
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
    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_input_repair_profile_v0",
        "profile_id": "values_input_repair_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "repair_surface_built": True,
        "values_supplied": False,
        "source_packet_materialized_for_review": False,
        "metadata_populated": False,
        "ready_discriminator_count": 0,
        "rule_refined": False,
        "tie_broken": False,
        "candidate_values_filled": False,
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": all(roll.get(k) == 0 for k in zero_keys),
        "recommended_next": roll["recommended_next"],
        "next_command_goal": None,
    }

def report_obj(status: str, reason_codes: List[str], inventory: List[Dict[str, Any]], machine_slots: List[Dict[str, Any]], human_slots: List[Dict[str, Any]], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_input_repair_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Values input was invalid because no values payload was provided; this unit turns that halt into an explicit slot-level supply surface.",
        "required_slot_count": len(inventory),
        "machine_readable_slot_count": len(machine_slots),
        "human_or_schema_slot_count": len(human_slots),
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "values_supplied_count": 0,
        "source_packet_materialized_for_review_count": 0,
        "metadata_populated_count": 0,
        "ready_discriminator_count": 0,
        "rule_refined_count": 0,
        "tie_broken_count": 0,
        "candidate_values_filled_count": 0,
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

def transition_trace_obj(status: str, reason_codes: List[str], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_input_repair_transition_trace_v0",
        "trace": [
            {
                "step": "consume_values_input_invalid_halt",
                "question": "why did source-packet value provision halt",
                "answer": "values_payload_not_provided",
                "taken": "build slot-level input repair surface",
            },
            {
                "step": "split_required_slots",
                "question": "what must be supplied before packet materialization",
                "answer": status,
                "reason_codes": reason_codes,
                "taken": next_edge,
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_basis()

    if failures:
        inventory: List[Dict[str, Any]] = []
        machine_slots: List[Dict[str, Any]] = []
        human_slots: List[Dict[str, Any]] = []
        status = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUT_REPAIR_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUT_REPAIR_BASIS_V0"
    else:
        inventory = build_slot_inventory()
        machine_slots, human_slots = split_slots(inventory)
        status, reason_codes, next_edge = classify(inventory, machine_slots, human_slots)

    surface = build_surface(inventory, machine_slots, human_slots) if not failures else {
        "schema_version": "typed_value_source_metadata_source_packet_values_input_repair_surface_v0",
        "repair_status": status,
        "required_slot_count": 0,
        "machine_readable_slot_count": 0,
        "human_or_schema_slot_count": 0,
        "recommended_next": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }
    payload_template = build_payload_template(inventory)

    classif = classification_obj(status, reason_codes, next_edge, inventory, machine_slots, human_slots)
    boundary = authority_boundary_obj(status)
    roll = rollup_obj(status, inventory, machine_slots, human_slots, next_edge)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, inventory, machine_slots, human_slots, next_edge)
    trace = transition_trace_obj(status, reason_codes, next_edge)
    rerun = build_review_rerun_contract()

    write_json(SLOT_INVENTORY_PATH, {
        "schema_version": "typed_value_source_metadata_source_packet_values_slot_inventory_v0",
        "inventory_status": "SOURCE_PACKET_VALUE_SLOTS_INVENTORIED",
        "required_slot_count": len(inventory),
        "slots": inventory,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    })
    write_json(MACHINE_SOURCE_SLOTS_PATH, {
        "schema_version": "typed_value_source_metadata_source_packet_values_machine_source_slots_v0",
        "slot_group_status": "MACHINE_READABLE_SOURCE_SLOTS_IDENTIFIED",
        "slot_count": len(machine_slots),
        "slots": machine_slots,
    })
    write_json(HUMAN_SCHEMA_SLOTS_PATH, {
        "schema_version": "typed_value_source_metadata_source_packet_values_human_schema_slots_v0",
        "slot_group_status": "HUMAN_OR_SCHEMA_SOURCE_SLOTS_IDENTIFIED",
        "slot_count": len(human_slots),
        "slots": human_slots,
        "machine_must_not_infer": [s["field"] for s in human_slots],
    })
    write_json(PAYLOAD_TEMPLATE_PATH, payload_template)
    write_json(REPAIR_SURFACE_PATH, surface)
    write_json(REVIEW_RERUN_CONTRACT_PATH, rerun)
    write_json(CLASSIFICATION_PATH, classif)
    write_json(AUTHORITY_BOUNDARY_PATH, boundary)
    write_json(ROLLUP_PATH, roll)
    write_json(PROFILE_PATH, prof)
    write_json(REPORT_PATH, rep)
    write_json(TRANSITION_TRACE_PATH, trace)

    env_text = f'''# values input repair env exports v0
# Fill the JSON payload at:
#   {rel(PAYLOAD_TEMPLATE_PATH)}
#
# Then re-run:
#   export TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_PATH="{rel(PAYLOAD_TEMPLATE_PATH)}"
#   python3 scripts/provide_typed_value_source_metadata_source_packet_values_v0.py
#
# If the values packet is materialized for review, then set:
#   export TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_PATH="data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_v0/typed_value_source_metadata_source_packet_values_packet_draft_v0.json"
# and re-run:
#   python3 scripts/provide_or_review_typed_value_source_metadata_source_packet_v0.py
'''
    write_text(ENV_EXPORTS_PATH, env_text)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        roll["source_mutation_count"] = 1
        rep["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, roll)
        write_json(REPORT_PATH, rep)

    acceptance_gate_results = {
        "VALUES_INPUT_REPAIR_0_SOURCE_VALUES_RECEIPT_CONSUMED": SOURCE_VALUES_RECEIPT_PATH.exists(),
        "VALUES_INPUT_REPAIR_1_VALUES_PACKET_DRAFT_CONSUMED": SOURCE_VALUES_PACKET_DRAFT_PATH.exists(),
        "VALUES_INPUT_REPAIR_2_SLOT_INVENTORY_EMITTED": SLOT_INVENTORY_PATH.exists(),
        "VALUES_INPUT_REPAIR_3_MACHINE_SOURCE_SLOTS_EMITTED": MACHINE_SOURCE_SLOTS_PATH.exists(),
        "VALUES_INPUT_REPAIR_4_HUMAN_SCHEMA_SLOTS_EMITTED": HUMAN_SCHEMA_SLOTS_PATH.exists(),
        "VALUES_INPUT_REPAIR_5_PAYLOAD_TEMPLATE_EMITTED": PAYLOAD_TEMPLATE_PATH.exists(),
        "VALUES_INPUT_REPAIR_6_REPAIR_SURFACE_EMITTED": REPAIR_SURFACE_PATH.exists(),
        "VALUES_INPUT_REPAIR_7_ENV_EXPORTS_EMITTED": ENV_EXPORTS_PATH.exists(),
        "VALUES_INPUT_REPAIR_8_REVIEW_RERUN_CONTRACT_EMITTED": REVIEW_RERUN_CONTRACT_PATH.exists(),
        "VALUES_INPUT_REPAIR_9_NO_VALUES_SUPPLIED": roll["values_supplied_count"] == 0,
        "VALUES_INPUT_REPAIR_10_NO_SOURCE_PACKET_MATERIALIZED": roll["source_packet_materialized_for_review_count"] == 0,
        "VALUES_INPUT_REPAIR_11_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "VALUES_INPUT_REPAIR_12_NO_DISCRIMINATOR_READY": roll["ready_discriminator_count"] == 0,
        "VALUES_INPUT_REPAIR_13_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "VALUES_INPUT_REPAIR_14_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "VALUES_INPUT_REPAIR_15_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "VALUES_INPUT_REPAIR_16_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classif["target_candidate_declared_for_review"] is False,
        "VALUES_INPUT_REPAIR_17_NO_TARGET_SELECTED_FOR_BUILD": classif["target_selected_for_build"] is False,
        "VALUES_INPUT_REPAIR_18_NO_ACCEPTED_FOR_BUILD": classif["accepted_for_build"] is False,
        "VALUES_INPUT_REPAIR_19_NO_RUNTIME_PATCH": classif["runtime_patch_authorized"] is False,
        "VALUES_INPUT_REPAIR_20_NO_TARGET_FILE_MODIFICATION": classif["target_file_modification_authorized"] is False,
        "VALUES_INPUT_REPAIR_21_NO_C5_OPENED": classif["c5_authorized"] is False,
        "VALUES_INPUT_REPAIR_22_NO_GENERAL_CELL1_AUTHORITY": classif["general_cell1_authority_granted"] is False,
        "VALUES_INPUT_REPAIR_23_NO_LATEST_FILE_GUESSING": classif["latest_file_guessing"] is False,
        "VALUES_INPUT_REPAIR_24_NO_MTIME_SELECTION": classif["mtime_selection"] is False,
        "VALUES_INPUT_REPAIR_25_NO_HIDDEN_NEXT_COMMAND": classif["next_command_goal"] is None,
        "VALUES_INPUT_REPAIR_26_ACCEPTANCE_BOUNDARY_RETAINED": classif["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "VALUES_INPUT_REPAIR_27_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUT_REPAIR_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "required_slots": len(inventory),
        "machine_slots": len(machine_slots),
        "human_slots": len(human_slots),
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_value_source_metadata_source_packet_values_input_repair_receipt_v0",
        "receipt_type": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUT_REPAIR_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_values_receipt_id": SOURCE_VALUES_RECEIPT_ID,
        "source_bridge_receipt_id": SOURCE_BRIDGE_RECEIPT_ID,
        "values_input_repair_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "required_slot_count": len(inventory),
            "machine_readable_slot_count": len(machine_slots),
            "human_or_schema_slot_count": len(human_slots),
            "values_supplied": False,
            "source_packet_materialized_for_review": False,
            "metadata_populated": False,
            "ready_discriminator_count": 0,
            "real_tie_proven": False,
            "rule_refined": False,
            "tie_broken": False,
            "candidate_values_filled": False,
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
            "recommended_next": next_edge,
        },
        "aggregate_metrics": rep,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "repair_surface": rel(REPAIR_SURFACE_PATH),
            "slot_inventory": rel(SLOT_INVENTORY_PATH),
            "machine_source_slots": rel(MACHINE_SOURCE_SLOTS_PATH),
            "human_schema_slots": rel(HUMAN_SCHEMA_SLOTS_PATH),
            "payload_template": rel(PAYLOAD_TEMPLATE_PATH),
            "env_exports": rel(ENV_EXPORTS_PATH),
            "review_rerun_contract": rel(REVIEW_RERUN_CONTRACT_PATH),
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
    print(f"values_input_repair_receipt_id={receipt_id}")
    print(f"values_input_repair_receipt_path={rel(receipt_path)}")
    print(f"values_input_repair_surface_path={rel(REPAIR_SURFACE_PATH)}")
    print(f"values_input_slot_inventory_path={rel(SLOT_INVENTORY_PATH)}")
    print(f"values_input_machine_source_slots_path={rel(MACHINE_SOURCE_SLOTS_PATH)}")
    print(f"values_input_human_schema_slots_path={rel(HUMAN_SCHEMA_SLOTS_PATH)}")
    print(f"values_input_payload_template_path={rel(PAYLOAD_TEMPLATE_PATH)}")
    print(f"values_input_env_exports_path={rel(ENV_EXPORTS_PATH)}")
    print(f"values_input_review_rerun_contract_path={rel(REVIEW_RERUN_CONTRACT_PATH)}")
    print(f"values_input_repair_rollup_path={rel(ROLLUP_PATH)}")
    print(f"values_input_repair_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
