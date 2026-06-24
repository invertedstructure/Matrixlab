#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLASSIFY_AND_PROPOSE_TYPED_VALUE_SOURCE_PACKET_VALUES_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_value_proposition.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_VALUE_PROPOSITION"
MODE = "ABSENCE_CLASSIFICATION_AND_PROPOSITION / NO_METADATA_FILL / NO_TIE_BREAK / NO_ACCEPTANCE"
BUILD_MODE = "VALUE_PROPOSITION_SURFACE_ONLY"

SOURCE_VALUES_INPUT_REPAIR_RECEIPT_ID = "345ed2b8"
SOURCE_VALUES_INPUT_REPAIR_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0_receipts/345ed2b8.json"
SOURCE_REPAIR_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_input_repair_surface_v0.json"
SOURCE_SLOT_INVENTORY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_slot_inventory_v0.json"
SOURCE_MACHINE_SOURCE_SLOTS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_machine_source_slots_v0.json"
SOURCE_HUMAN_SCHEMA_SLOTS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_human_schema_slots_v0.json"
SOURCE_PAYLOAD_TEMPLATE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_payload_template_v0.json"
SOURCE_REVIEW_RERUN_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_review_rerun_contract_v0.json"
SOURCE_REPAIR_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_input_repair_classification_v0.json"
SOURCE_REPAIR_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_input_repair_rollup_v0.json"
SOURCE_REPAIR_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_input_repair_profile_v0.json"

SOURCE_VALUES_PACKET_DRAFT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_v0/typed_value_source_metadata_source_packet_values_packet_draft_v0.json"
SOURCE_FIELD_POLICY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_source_field_policy_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_v0_receipts"

ABSENCE_CLASSIFICATION_PATH = OUT_DIR / "typed_value_source_value_absence_classification_v0.json"
MACHINE_PROPOSITION_ATTEMPTS_PATH = OUT_DIR / "typed_value_source_machine_readable_value_proposition_attempts_v0.json"
HUMAN_SCHEMA_BOUNDARY_DIAGNOSTIC_PATH = OUT_DIR / "typed_value_source_human_schema_slot_boundary_diagnostic_v0.json"
VALUE_PROPOSITION_PACKET_PATH = OUT_DIR / "typed_value_source_value_proposition_packet_v0.json"
PROPOSITION_REVIEW_PACKET_PATH = OUT_DIR / "typed_value_source_value_proposition_review_packet_v0.json"
PROPOSED_SOURCE_PACKET_DRAFT_PATH = OUT_DIR / "typed_value_source_proposed_source_packet_draft_v0.json"
NULL_REASON_MATRIX_PATH = OUT_DIR / "typed_value_source_value_null_reason_matrix_v0.json"
AUTHORIZATION_CONTRACT_PATH = OUT_DIR / "typed_value_source_value_proposition_authorization_contract_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_value_source_value_proposition_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_value_source_value_proposition_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_value_source_value_proposition_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_value_source_value_proposition_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_value_source_value_proposition_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_value_source_value_proposition_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_VALUES_INPUT_REPAIR_RECEIPT_PATH,
    SOURCE_REPAIR_SURFACE_PATH,
    SOURCE_SLOT_INVENTORY_PATH,
    SOURCE_MACHINE_SOURCE_SLOTS_PATH,
    SOURCE_HUMAN_SCHEMA_SLOTS_PATH,
    SOURCE_PAYLOAD_TEMPLATE_PATH,
    SOURCE_REVIEW_RERUN_CONTRACT_PATH,
    SOURCE_REPAIR_CLASSIFICATION_PATH,
    SOURCE_REPAIR_ROLLUP_PATH,
    SOURCE_REPAIR_PROFILE_PATH,
    SOURCE_VALUES_PACKET_DRAFT_PATH,
    SOURCE_FIELD_POLICY_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUT_REPAIR_SURFACE_BUILT_REQUIRES_VALUES"
EXPECTED_SOURCE_STOP = "STOP_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUT_REPAIR_SURFACE_BUILT_REQUIRES_VALUES"
EXPECTED_NEXT = "SUPPLY_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUTS_V0"

FIELD_QUESTIONS = {
    "direct_evidence_strength": {
        "slot_category": "SOURCE_EVIDENCE_GRADING_BOUNDARY",
        "question": "How strong is the direct evidence for this row as a source of the required value?",
        "answer_shape": "enum: STRONG | MEDIUM | WEAK | ABSENT | UNKNOWN, with source_ref",
        "downstream_consumer": "source dominance / discriminator readiness",
    },
    "target_scope": {
        "slot_category": "TARGET_SCOPE_BOUNDARY",
        "question": "What exact target scope does this row speak for?",
        "answer_shape": "string or enum scope label, with source_ref",
        "downstream_consumer": "same-scope comparison and target candidate formation",
    },
    "target_aspect": {
        "slot_category": "TARGET_ASPECT_BOUNDARY",
        "question": "Which aspect of the target does this row describe?",
        "answer_shape": "string or enum aspect label, with source_ref",
        "downstream_consumer": "split rows that are not competing on the same aspect",
    },
    "comparison_grain": {
        "slot_category": "COMPARISON_GRAIN_BOUNDARY",
        "question": "At what grain should this row be compared to the others?",
        "answer_shape": "enum or string grain label, with source_ref",
        "downstream_consumer": "dominance comparison and tie diagnosis",
    },
    "inference_strength": {
        "slot_category": "INFERENCE_STRENGTH_BOUNDARY",
        "question": "How much inference is needed to use this row as a value source?",
        "answer_shape": "enum: DIRECT | LOW_INFERENCE | MEDIUM_INFERENCE | HIGH_INFERENCE | UNKNOWN, with source_ref",
        "downstream_consumer": "source ranking / discriminator readiness",
    },
    "verification_gate_ref": {
        "slot_category": "VERIFICATION_GATE_BOUNDARY",
        "question": "Which verification gate would validate this row/value before use?",
        "answer_shape": "artifact/ref id/path, with source_ref",
        "downstream_consumer": "proposal review and acceptance gate",
    },
    "rollback_or_stop_boundary_ref": {
        "slot_category": "ROLLBACK_OR_STOP_BOUNDARY",
        "question": "Which rollback/stop boundary applies if this row/value is wrong or unauthorized?",
        "answer_shape": "artifact/ref id/path, with source_ref",
        "downstream_consumer": "safe commit boundary",
    },
    "load_bearing_reason": {
        "slot_category": "LOAD_BEARING_JUDGMENT_BOUNDARY",
        "question": "Why is this value source load-bearing enough to affect the next decision?",
        "answer_shape": "short justification, accepted by human or prevalidated schema",
        "downstream_consumer": "authorization/proposal acceptance",
    },
    "schema_preference_key": {
        "slot_category": "SCHEMA_POLICY_BOUNDARY",
        "question": "Which accepted schema preference, if any, authorizes this row/value over alternatives?",
        "answer_shape": "prevalidated schema key/ref or null-with-reason",
        "downstream_consumer": "schema-authorized selection",
    },
    "human_preference_boundary_ref": {
        "slot_category": "HUMAN_REVIEW_BOUNDARY",
        "question": "What human review boundary authorizes choosing or rejecting this row/value?",
        "answer_shape": "human decision/ref/review id or null-with-reason",
        "downstream_consumer": "human authorization",
    },
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
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> List[str]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    receipt = read_json(SOURCE_VALUES_INPUT_REPAIR_RECEIPT_PATH)
    summary = receipt.get("values_input_repair_summary", {})
    surface = read_json(SOURCE_REPAIR_SURFACE_PATH)
    inventory = read_json(SOURCE_SLOT_INVENTORY_PATH)
    machine = read_json(SOURCE_MACHINE_SOURCE_SLOTS_PATH)
    human = read_json(SOURCE_HUMAN_SCHEMA_SLOTS_PATH)
    classif = read_json(SOURCE_REPAIR_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_REPAIR_ROLLUP_PATH)
    prof = read_json(SOURCE_REPAIR_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_VALUES_INPUT_REPAIR_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("values_input_repair_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"values_input_repair_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("values_input_repair_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"values_input_repair_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("required_slot_count") != 30:
        failures.append(f"required_slot_count_not_30:{summary.get('required_slot_count')}")
    if summary.get("machine_readable_slot_count") != 21:
        failures.append(f"machine_slot_count_not_21:{summary.get('machine_readable_slot_count')}")
    if summary.get("human_or_schema_slot_count") != 9:
        failures.append(f"human_slot_count_not_9:{summary.get('human_or_schema_slot_count')}")
    if summary.get("values_supplied") is not False:
        failures.append("values_supplied_unexpectedly")
    if summary.get("source_packet_materialized_for_review") is not False:
        failures.append("source_packet_materialized_unexpectedly")
    if summary.get("metadata_populated") is not False:
        failures.append("metadata_populated_unexpectedly")
    if summary.get("rule_refined") is not False:
        failures.append("rule_refined_unexpectedly")
    if summary.get("tie_broken") is not False:
        failures.append("tie_broken_unexpectedly")
    if summary.get("candidate_values_filled") is not False:
        failures.append("candidate_values_filled_unexpectedly")

    if surface.get("repair_status") != EXPECTED_SOURCE_STATUS:
        failures.append("repair_surface_status_wrong")
    if inventory.get("required_slot_count") != 30:
        failures.append("slot_inventory_required_count_wrong")
    if machine.get("slot_count") != 21:
        failures.append("machine_slot_count_artifact_wrong")
    if human.get("slot_count") != 9:
        failures.append("human_slot_count_artifact_wrong")
    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("repair_classification_status_wrong")
    if roll.get("metadata_populated_count") != 0:
        failures.append("repair_rollup_metadata_populated_nonzero")
    if prof.get("metadata_populated") is not False:
        failures.append("repair_profile_metadata_populated_true")

    return failures

def field_policies() -> Dict[str, Dict[str, Any]]:
    policy = read_json(SOURCE_FIELD_POLICY_PATH)
    out: Dict[str, Dict[str, Any]] = {}
    for item in policy.get("field_policies", []):
        if isinstance(item, dict) and item.get("field"):
            out[str(item["field"])] = item
    return out

def slots() -> List[Dict[str, Any]]:
    data = read_json(SOURCE_SLOT_INVENTORY_PATH)
    return [s for s in data.get("slots", []) if isinstance(s, dict)]

def source_path_from_ref(source_ref: Any) -> Path | None:
    if not isinstance(source_ref, str) or not source_ref:
        return None
    p = Path(source_ref)
    if not p.is_absolute():
        p = ROOT / p
    return p if p.exists() else None

def extract_json_path(obj: Any, json_path: Any) -> Any:
    if not isinstance(json_path, str) or not json_path:
        return None
    path = json_path.strip()
    if path.startswith("$."):
        parts = path[2:].split(".")
    elif path.startswith("/"):
        parts = [p for p in path.split("/") if p]
    else:
        parts = [p for p in path.split(".") if p]
    cur = obj
    for part in parts:
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        elif isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except Exception:
                return None
        else:
            return None
    return cur

def bounded_source_probe(slot: Dict[str, Any]) -> Dict[str, Any]:
    source_ref = slot.get("row_source_ref")
    json_path = slot.get("row_json_path")
    p = source_path_from_ref(source_ref)

    if p is None:
        return {
            "source_probe_status": "SOURCE_REF_MISSING_OR_NOT_LOCAL_FILE",
            "source_path": None,
            "source_content_found": False,
            "json_path_value_found": False,
            "json_path_value": None,
        }

    result = {
        "source_probe_status": "SOURCE_FILE_PRESENT",
        "source_path": rel(p),
        "source_content_found": True,
        "json_path_value_found": False,
        "json_path_value": None,
    }

    try:
        obj = read_json(p)
    except Exception as exc:
        result["source_probe_status"] = "SOURCE_FILE_PRESENT_JSON_UNREADABLE"
        result["json_error"] = str(exc)
        return result

    value = extract_json_path(obj, json_path)
    if value is not None:
        result["json_path_value_found"] = True
        result["json_path_value"] = value
    else:
        result["source_probe_status"] = "SOURCE_FILE_PRESENT_JSON_PATH_NOT_FOUND"

    return result

def allowed_value_from_source(slot: Dict[str, Any], probe: Dict[str, Any]) -> Tuple[Any, str, List[str]]:
    field = str(slot.get("field"))
    row_value = slot.get("row_value")

    # Strict v0: only values already appearing as explicit slot value/source evidence can be proposed.
    # We do not derive semantic metadata from row text/path. That would smuggle in inference.
    if slot.get("current_value") not in (None, "") and (slot.get("current_source_ref") or slot.get("current_evidence_or_review_ref")):
        return slot.get("current_value"), "VALUE_PRESENT_IN_SLOT", ["explicit_slot_value"]

    return None, "VALUE_PRESENT_BUT_NOT_EXTRACTED" if probe.get("source_content_found") else "SOURCE_REF_MISSING", [
        "No explicit typed field value is present in the slot.",
        "Bounded source probe is evidence for possible upstream content only, not permission to infer semantic metadata.",
        f"Field {field!r} requires typed value with source_ref or review_ref.",
        f"Row value observed: {row_value!r}",
    ]

def human_absence_reason(field: str) -> str:
    if field == "schema_preference_key":
        return "SCHEMA_AUTHORIZATION_REQUIRED"
    if field in {"load_bearing_reason", "human_preference_boundary_ref"}:
        return "HUMAN_DECISION_REQUIRED"
    return "NOT_MACHINE_INFERABLE"

def machine_absence_reason(slot: Dict[str, Any], probe: Dict[str, Any]) -> str:
    if not slot.get("row_source_ref"):
        return "SOURCE_REF_MISSING"
    if not probe.get("source_content_found"):
        return "SOURCE_CONTENT_ABSENT"
    if probe.get("json_path_value_found"):
        return "SOURCE_FIELD_NOT_TYPED"
    return "SOURCE_FIELD_NOT_TYPED"

def build_absence_and_propositions(slot_list: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    policies = field_policies()
    absence_records: List[Dict[str, Any]] = []
    machine_attempts: List[Dict[str, Any]] = []
    human_diagnostics: List[Dict[str, Any]] = []
    proposition_records: List[Dict[str, Any]] = []

    for slot in slot_list:
        field = str(slot.get("field"))
        meta = FIELD_QUESTIONS.get(field, {
            "slot_category": "UNKNOWN_TYPED_VALUE_BOUNDARY",
            "question": f"What value is required for {field}?",
            "answer_shape": "typed value with explicit source or review ref",
            "downstream_consumer": "unknown",
        })
        policy = policies.get(field, {})
        human_schema = bool(slot.get("human_schema_only"))

        probe = bounded_source_probe(slot)
        proposed_value = None
        proposed_source_ref = None
        proposition_status = "NO_PROPOSITION"
        absence_reason = None
        notes: List[str] = []

        if human_schema:
            absence_reason = human_absence_reason(field)
            proposition_status = "AUTHORIZATION_REQUIRED_NO_COMMIT"
            notes = [
                "Machine may describe the decision shape but may not commit a value.",
                "A human decision or prevalidated schema authorization is required.",
            ]
            human_diagnostics.append({
                "slot_id": slot.get("slot_id"),
                "row_uid": slot.get("row_uid"),
                "field": field,
                "slot_category": meta["slot_category"],
                "question_being_asked": meta["question"],
                "why_machine_cannot_infer": absence_reason,
                "acceptable_answer_shape": meta["answer_shape"],
                "allowed_resolver": "human_operator_or_prevalidated_schema",
                "required_authority": "human_or_prevalidated_schema_acceptance_required",
                "source_refs_needed": slot.get("allowed_sources", []),
                "downstream_consumer": meta["downstream_consumer"],
                "blocked_until_resolved": True,
                "safe_null_behavior": "leave null; do not mark discriminator ready",
                "candidate_value": None,
                "candidate_status": "not proposed by machine",
            })
        else:
            proposed_value, extraction_status, extraction_notes = allowed_value_from_source(slot, probe)
            if proposed_value is not None:
                absence_reason = None
                proposed_source_ref = slot.get("current_source_ref") or slot.get("current_evidence_or_review_ref") or slot.get("row_source_ref")
                proposition_status = "PROPOSED_SOURCE_BACKED_VALUE"
                notes = ["Value was already explicitly typed in the slot; no inference performed."]
            else:
                absence_reason = machine_absence_reason(slot, probe)
                proposition_status = "NULL_PROPOSITION_WITH_ABSENCE_REASON"
                notes = extraction_notes

            machine_attempts.append({
                "slot_id": slot.get("slot_id"),
                "row_uid": slot.get("row_uid"),
                "field": field,
                "slot_category": meta["slot_category"],
                "source_probe": probe,
                "extraction_status": proposition_status,
                "absence_reason": absence_reason,
                "proposed_value": proposed_value,
                "proposed_source_ref": proposed_source_ref,
                "notes": notes,
            })

        absence_records.append({
            "slot_id": slot.get("slot_id"),
            "row_uid": slot.get("row_uid"),
            "row_index": slot.get("row_index"),
            "field": field,
            "slot_category": meta["slot_category"],
            "human_schema_only": human_schema,
            "absence_reason": absence_reason,
            "question_being_asked": meta["question"],
            "acceptable_answer_shape": meta["answer_shape"],
            "downstream_consumer": meta["downstream_consumer"],
            "allowed_sources": slot.get("allowed_sources", []),
            "required_source_object": slot.get("required_source_object"),
            "policy_source_class": policy.get("source_class"),
            "safe_null_behavior": "leave null; do not mark discriminator ready",
        })

        proposition_records.append({
            "slot_id": slot.get("slot_id"),
            "row_uid": slot.get("row_uid"),
            "row_index": slot.get("row_index"),
            "row_source_ref": slot.get("row_source_ref"),
            "row_json_path": slot.get("row_json_path"),
            "row_value": slot.get("row_value"),
            "field": field,
            "source_class": slot.get("source_class"),
            "human_schema_only": human_schema,
            "proposition_status": proposition_status,
            "proposed_value": proposed_value,
            "proposed_source_ref": proposed_source_ref,
            "evidence_or_review_ref": None,
            "absence_reason": absence_reason,
            "authorization_required": human_schema or proposed_value is None,
            "question_being_asked": meta["question"],
            "acceptable_answer_shape": meta["answer_shape"],
            "downstream_consumer": meta["downstream_consumer"],
            "notes": notes,
        })

    return absence_records, machine_attempts, human_diagnostics, proposition_records

def build_proposed_source_packet(propositions: List[Dict[str, Any]]) -> Dict[str, Any]:
    draft = read_json(SOURCE_VALUES_PACKET_DRAFT_PATH)
    draft = json.loads(json.dumps(draft))
    by_row_field = {
        (str(p.get("row_uid")), str(p.get("field"))): p
        for p in propositions
    }

    for row in draft.get("rows", []):
        if not isinstance(row, dict):
            continue
        row_uid = str(row.get("row_uid"))
        for item in row.get("missing_metadata_to_supply", []):
            if not isinstance(item, dict):
                continue
            field = str(item.get("field"))
            prop = by_row_field.get((row_uid, field))
            if not prop:
                continue
            item["value"] = prop.get("proposed_value")
            item["source_ref"] = prop.get("proposed_source_ref")
            item["evidence_or_review_ref"] = prop.get("evidence_or_review_ref")
            item["null_reason"] = prop.get("absence_reason")
            item["proposition_status"] = prop.get("proposition_status")
            item["authorization_required"] = prop.get("authorization_required")

    draft["proposition_packet_ref"] = rel(VALUE_PROPOSITION_PACKET_PATH)
    draft["source_packet_status"] = "PROPOSED_SOURCE_PACKET_DRAFT_NOT_AUTHORIZED"
    draft["not_authorized_for_metadata_population"] = True
    return draft

def classify(propositions: List[Dict[str, Any]], machine_attempts: List[Dict[str, Any]], human_diagnostics: List[Dict[str, Any]]) -> Tuple[str, List[str], str]:
    proposed_count = sum(1 for p in propositions if p.get("proposition_status") == "PROPOSED_SOURCE_BACKED_VALUE")
    null_count = sum(1 for p in propositions if p.get("proposed_value") is None)
    human_count = len(human_diagnostics)

    reason_codes = [
        "VALUE_SLOT_ABSENCE_CLASSIFICATION_EMITTED",
        "MACHINE_READABLE_SLOTS_PROBED_WITHOUT_UNTYPED_INFERENCE",
        "HUMAN_SCHEMA_BOUNDARY_DIAGNOSTIC_EMITTED",
        "VALUE_PROPOSITION_PACKET_EMITTED",
        "AUTHORIZATION_REQUIRED_BEFORE_SOURCE_PACKET_MATERIALIZATION",
    ]
    if proposed_count:
        reason_codes.append("SOME_SOURCE_BACKED_VALUES_PROPOSED")
    if null_count:
        reason_codes.append("SOME_VALUES_REMAIN_NULL_WITH_ABSENCE_REASONS")
    if human_count:
        reason_codes.append("HUMAN_OR_SCHEMA_BOUNDARY_SLOTS_REQUIRE_AUTHORIZATION")

    status = "TYPED_VALUE_SOURCE_VALUE_PROPOSITIONS_PARTIAL_WITH_ABSENCE_CLASSIFICATION"
    next_edge = "AUTHORIZE_OR_REVIEW_TYPED_VALUE_SOURCE_VALUE_PROPOSITIONS_V0"
    return status, reason_codes, next_edge

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_value_proposition_authority_boundary_v0",
        "status": status,
        "may_classify_absence": True,
        "may_probe_explicit_source_refs": True,
        "may_emit_source_backed_propositions": True,
        "may_emit_null_reasons": True,
        "may_emit_human_schema_boundary_diagnostics": True,
        "may_request_authorization": True,
        "may_materialize_source_packet_for_review": False,
        "may_populate_metadata": False,
        "may_evaluate_discriminators": False,
        "may_refine_rule": False,
        "may_break_tie": False,
        "may_emit_candidate_values_for_target": False,
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

def rollup_obj(status: str, propositions: List[Dict[str, Any]], machine_attempts: List[Dict[str, Any]], human_diagnostics: List[Dict[str, Any]], next_edge: str) -> Dict[str, Any]:
    proposed_count = sum(1 for p in propositions if p.get("proposed_value") is not None)
    null_count = sum(1 for p in propositions if p.get("proposed_value") is None)
    return {
        "schema_version": "typed_value_source_value_proposition_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "slot_count": len(propositions),
        "machine_readable_slot_count": len(machine_attempts),
        "human_or_schema_slot_count": len(human_diagnostics),
        "source_backed_proposed_value_count": proposed_count,
        "null_proposition_count": null_count,
        "absence_classification_count": len(propositions),
        "human_schema_boundary_diagnostic_count": len(human_diagnostics),
        "proposition_packet_emitted_count": 1,
        "authorization_contract_emitted_count": 1,
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
        "schema_version": "typed_value_source_value_proposition_profile_v0",
        "profile_id": "value_proposition_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "proposition_surface_built": True,
        "value_propositions_emitted": True,
        "authorization_required": True,
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

def report_obj(status: str, reason_codes: List[str], roll: Dict[str, Any], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_value_proposition_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Values are missing from the typed input packet; this unit classifies why each slot is missing and emits propositions/null reasons rather than requesting raw numbers.",
        "slot_count": roll["slot_count"],
        "machine_readable_slot_count": roll["machine_readable_slot_count"],
        "human_or_schema_slot_count": roll["human_or_schema_slot_count"],
        "source_backed_proposed_value_count": roll["source_backed_proposed_value_count"],
        "null_proposition_count": roll["null_proposition_count"],
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
        "schema_version": "typed_value_source_value_proposition_transition_trace_v0",
        "trace": [
            {
                "step": "consume_slot_repair_surface",
                "question": "should the operator supply raw values",
                "answer": "no; machine must classify, propose, and stop at authorization",
                "taken": "build value proposition surface",
            },
            {
                "step": "classify_each_slot_absence",
                "question": "why is each value missing",
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

    slot_list = [] if failures else slots()
    absence_records, machine_attempts, human_diagnostics, propositions = build_absence_and_propositions(slot_list)
    proposed_packet = build_proposed_source_packet(propositions)

    if failures:
        status = "TYPED_VALUE_SOURCE_VALUE_PROPOSITION_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_TYPED_VALUE_SOURCE_VALUE_PROPOSITION_BASIS_V0"
    else:
        status, reason_codes, next_edge = classify(propositions, machine_attempts, human_diagnostics)

    roll = rollup_obj(status, propositions, machine_attempts, human_diagnostics, next_edge)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, roll, next_edge)
    boundary = authority_boundary_obj(status)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    classification = {
        "schema_version": "typed_value_source_value_proposition_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "slot_count": len(propositions),
        "machine_readable_slot_count": len(machine_attempts),
        "human_or_schema_slot_count": len(human_diagnostics),
        "source_backed_proposed_value_count": roll["source_backed_proposed_value_count"],
        "null_proposition_count": roll["null_proposition_count"],
        "authorization_required": True,
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

    value_packet = {
        "schema_version": "typed_value_source_value_proposition_packet_v0",
        "packet_id": "value_proposition_packet_" + sha8(propositions),
        "source_values_input_repair_receipt_id": SOURCE_VALUES_INPUT_REPAIR_RECEIPT_ID,
        "packet_status": status,
        "slot_count": len(propositions),
        "propositions": propositions,
        "authorization_required": True,
        "not_authorized_for_metadata_population": True,
        "recommended_next": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    review_packet = {
        "schema_version": "typed_value_source_value_proposition_review_packet_v0",
        "review_packet_id": "value_proposition_review_packet_" + sha8(propositions),
        "review_status": "VALUE_PROPOSITIONS_REQUIRE_AUTHORIZATION",
        "question": "Authorize, reject, or amend the typed value propositions/null reasons. Do not treat this as raw value entry.",
        "allowed_responses": [
            "AUTHORIZE_ALL_SOURCE_BACKED_AND_ACCEPT_NULL_REASONS",
            "AUTHORIZE_SELECTED_PROPOSITIONS",
            "AMEND_WITH_EXPLICIT_REVIEW_VALUES",
            "REJECT_AND_REQUIRE_NEW_PROPOSITION_SURFACE",
            "REGISTER_PREVALIDATED_SCHEMA_RULE_FOR_REPEATING_BOUNDARY",
        ],
        "proposition_packet_ref": rel(VALUE_PROPOSITION_PACKET_PATH),
        "human_schema_boundary_diagnostic_ref": rel(HUMAN_SCHEMA_BOUNDARY_DIAGNOSTIC_PATH),
        "null_reason_matrix_ref": rel(NULL_REASON_MATRIX_PATH),
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    null_matrix = {
        "schema_version": "typed_value_source_value_null_reason_matrix_v0",
        "matrix_status": "NULL_REASONS_EMITTED_FOR_UNPROPOSED_VALUES",
        "null_count": roll["null_proposition_count"],
        "records": [
            {
                "slot_id": p.get("slot_id"),
                "row_uid": p.get("row_uid"),
                "field": p.get("field"),
                "human_schema_only": p.get("human_schema_only"),
                "absence_reason": p.get("absence_reason"),
                "safe_null_behavior": "leave null; do not mark discriminator ready",
                "authorization_required": p.get("authorization_required"),
            }
            for p in propositions if p.get("proposed_value") is None
        ],
    }

    authorization_contract = {
        "schema_version": "typed_value_source_value_proposition_authorization_contract_v0",
        "contract_status": "VALUE_PROPOSITIONS_REQUIRE_AUTHORIZATION",
        "source_proposition_packet_ref": rel(VALUE_PROPOSITION_PACKET_PATH),
        "authorization_does_not_apply_metadata": True,
        "authorization_does_not_refine_rule": True,
        "authorization_does_not_break_tie": True,
        "after_authorization_next_possible_unit": "MATERIALIZE_TYPED_VALUE_SOURCE_PACKET_FROM_AUTHORIZED_PROPOSITIONS_V0",
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    write_json(ABSENCE_CLASSIFICATION_PATH, {
        "schema_version": "typed_value_source_value_absence_classification_v0",
        "classification_status": "VALUE_SLOT_ABSENCES_CLASSIFIED",
        "records": absence_records,
    })
    write_json(MACHINE_PROPOSITION_ATTEMPTS_PATH, {
        "schema_version": "typed_value_source_machine_readable_value_proposition_attempts_v0",
        "attempt_status": "MACHINE_READABLE_SLOTS_PROBED_WITHOUT_UNTYPED_INFERENCE",
        "attempts": machine_attempts,
    })
    write_json(HUMAN_SCHEMA_BOUNDARY_DIAGNOSTIC_PATH, {
        "schema_version": "typed_value_source_human_schema_slot_boundary_diagnostic_v0",
        "diagnostic_status": "HUMAN_SCHEMA_BOUNDARIES_EXPLAINED",
        "records": human_diagnostics,
    })
    write_json(VALUE_PROPOSITION_PACKET_PATH, value_packet)
    write_json(PROPOSITION_REVIEW_PACKET_PATH, review_packet)
    write_json(PROPOSED_SOURCE_PACKET_DRAFT_PATH, proposed_packet)
    write_json(NULL_REASON_MATRIX_PATH, null_matrix)
    write_json(AUTHORIZATION_CONTRACT_PATH, authorization_contract)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(AUTHORITY_BOUNDARY_PATH, boundary)
    write_json(ROLLUP_PATH, roll)
    write_json(PROFILE_PATH, prof)
    write_json(REPORT_PATH, rep)
    write_json(TRANSITION_TRACE_PATH, trace)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        roll["source_mutation_count"] = 1
        rep["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, roll)
        write_json(REPORT_PATH, rep)

    acceptance_gate_results = {
        "VALUE_PROPOSITION_0_REPAIR_RECEIPT_CONSUMED": SOURCE_VALUES_INPUT_REPAIR_RECEIPT_PATH.exists(),
        "VALUE_PROPOSITION_1_SLOT_INVENTORY_CONSUMED": SOURCE_SLOT_INVENTORY_PATH.exists(),
        "VALUE_PROPOSITION_2_ABSENCE_CLASSIFICATION_EMITTED": ABSENCE_CLASSIFICATION_PATH.exists(),
        "VALUE_PROPOSITION_3_MACHINE_ATTEMPTS_EMITTED": MACHINE_PROPOSITION_ATTEMPTS_PATH.exists(),
        "VALUE_PROPOSITION_4_HUMAN_SCHEMA_DIAGNOSTIC_EMITTED": HUMAN_SCHEMA_BOUNDARY_DIAGNOSTIC_PATH.exists(),
        "VALUE_PROPOSITION_5_PROPOSITION_PACKET_EMITTED": VALUE_PROPOSITION_PACKET_PATH.exists(),
        "VALUE_PROPOSITION_6_REVIEW_PACKET_EMITTED": PROPOSITION_REVIEW_PACKET_PATH.exists(),
        "VALUE_PROPOSITION_7_NULL_REASON_MATRIX_EMITTED": NULL_REASON_MATRIX_PATH.exists(),
        "VALUE_PROPOSITION_8_AUTHORIZATION_CONTRACT_EMITTED": AUTHORIZATION_CONTRACT_PATH.exists(),
        "VALUE_PROPOSITION_9_NO_VALUES_SUPPLIED": roll["values_supplied_count"] == 0,
        "VALUE_PROPOSITION_10_NO_SOURCE_PACKET_MATERIALIZED": roll["source_packet_materialized_for_review_count"] == 0,
        "VALUE_PROPOSITION_11_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "VALUE_PROPOSITION_12_NO_DISCRIMINATOR_READY": roll["ready_discriminator_count"] == 0,
        "VALUE_PROPOSITION_13_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "VALUE_PROPOSITION_14_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "VALUE_PROPOSITION_15_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "VALUE_PROPOSITION_16_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classification["target_candidate_declared_for_review"] is False,
        "VALUE_PROPOSITION_17_NO_TARGET_SELECTED_FOR_BUILD": classification["target_selected_for_build"] is False,
        "VALUE_PROPOSITION_18_NO_ACCEPTED_FOR_BUILD": classification["accepted_for_build"] is False,
        "VALUE_PROPOSITION_19_NO_RUNTIME_PATCH": classification["runtime_patch_authorized"] is False,
        "VALUE_PROPOSITION_20_NO_TARGET_FILE_MODIFICATION": classification["target_file_modification_authorized"] is False,
        "VALUE_PROPOSITION_21_NO_C5_OPENED": classification["c5_authorized"] is False,
        "VALUE_PROPOSITION_22_NO_GENERAL_CELL1_AUTHORITY": classification["general_cell1_authority_granted"] is False,
        "VALUE_PROPOSITION_23_NO_LATEST_FILE_GUESSING": classification["latest_file_guessing"] is False,
        "VALUE_PROPOSITION_24_NO_MTIME_SELECTION": classification["mtime_selection"] is False,
        "VALUE_PROPOSITION_25_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "VALUE_PROPOSITION_26_ACCEPTANCE_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "VALUE_PROPOSITION_27_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_VALUE_SOURCE_VALUE_PROPOSITION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "slot_count": roll["slot_count"],
        "null_count": roll["null_proposition_count"],
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_value_source_value_proposition_receipt_v0",
        "receipt_type": "TYPED_VALUE_SOURCE_VALUE_PROPOSITION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_values_input_repair_receipt_id": SOURCE_VALUES_INPUT_REPAIR_RECEIPT_ID,
        "value_proposition_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "slot_count": roll["slot_count"],
            "machine_readable_slot_count": roll["machine_readable_slot_count"],
            "human_or_schema_slot_count": roll["human_or_schema_slot_count"],
            "source_backed_proposed_value_count": roll["source_backed_proposed_value_count"],
            "null_proposition_count": roll["null_proposition_count"],
            "absence_classification_count": roll["absence_classification_count"],
            "human_schema_boundary_diagnostic_count": roll["human_schema_boundary_diagnostic_count"],
            "authorization_required": True,
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
            "absence_classification": rel(ABSENCE_CLASSIFICATION_PATH),
            "machine_proposition_attempts": rel(MACHINE_PROPOSITION_ATTEMPTS_PATH),
            "human_schema_boundary_diagnostic": rel(HUMAN_SCHEMA_BOUNDARY_DIAGNOSTIC_PATH),
            "value_proposition_packet": rel(VALUE_PROPOSITION_PACKET_PATH),
            "proposition_review_packet": rel(PROPOSITION_REVIEW_PACKET_PATH),
            "proposed_source_packet_draft": rel(PROPOSED_SOURCE_PACKET_DRAFT_PATH),
            "null_reason_matrix": rel(NULL_REASON_MATRIX_PATH),
            "authorization_contract": rel(AUTHORIZATION_CONTRACT_PATH),
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
    print(f"value_proposition_receipt_id={receipt_id}")
    print(f"value_proposition_receipt_path={rel(receipt_path)}")
    print(f"value_absence_classification_path={rel(ABSENCE_CLASSIFICATION_PATH)}")
    print(f"machine_proposition_attempts_path={rel(MACHINE_PROPOSITION_ATTEMPTS_PATH)}")
    print(f"human_schema_boundary_diagnostic_path={rel(HUMAN_SCHEMA_BOUNDARY_DIAGNOSTIC_PATH)}")
    print(f"value_proposition_packet_path={rel(VALUE_PROPOSITION_PACKET_PATH)}")
    print(f"value_proposition_review_packet_path={rel(PROPOSITION_REVIEW_PACKET_PATH)}")
    print(f"proposed_source_packet_draft_path={rel(PROPOSED_SOURCE_PACKET_DRAFT_PATH)}")
    print(f"value_null_reason_matrix_path={rel(NULL_REASON_MATRIX_PATH)}")
    print(f"value_authorization_contract_path={rel(AUTHORIZATION_CONTRACT_PATH)}")
    print(f"value_proposition_rollup_path={rel(ROLLUP_PATH)}")
    print(f"value_proposition_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
