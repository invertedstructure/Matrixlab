#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REPAIR_OR_NARROW_RUNTIME_PATCH_TARGET_EVIDENCE_VALUES_PROPOSER_INPUTS_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_evidence_values_proposer_input_repair.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_EVIDENCE_VALUES_PROPOSER_INPUT_REPAIR"
MODE = "DIAGNOSE_SOURCE_SURFACE / NO_PROPOSAL_ACCEPTANCE / NO_PATCH"
BUILD_MODE = "VALUES_PROPOSER_INPUT_REPAIR_ONLY"

SOURCE_VALUES_PROPOSER_RECEIPT_ID = "85d2d8e3"
SOURCE_VALUES_PROPOSER_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_values_proposer_v0_receipts/85d2d8e3.json"
SOURCE_VALUES_PROPOSAL_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_values_proposer_v0/runtime_patch_target_evidence_values_proposal_v0.json"
SOURCE_VALUES_PROPOSER_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_values_proposer_v0/runtime_patch_target_evidence_values_proposer_classification_v0.json"

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

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_evidence_values_proposer_input_repair_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_evidence_values_proposer_input_repair_v0_receipts"

SOURCE_SURFACE_MAP_PATH = OUT_DIR / "runtime_patch_target_value_source_surface_map_v0.json"
BRIDGE_REPAIR_RECOMMENDATION_PATH = OUT_DIR / "runtime_patch_target_value_source_bridge_repair_recommendation_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "runtime_patch_target_value_source_surface_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "runtime_patch_target_value_source_surface_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_patch_target_value_source_surface_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_patch_target_value_source_surface_profile_v0.json"
REPORT_PATH = OUT_DIR / "runtime_patch_target_value_source_surface_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "runtime_patch_target_value_source_surface_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_VALUES_PROPOSER_RECEIPT_PATH,
    SOURCE_VALUES_PROPOSAL_PATH,
    SOURCE_VALUES_PROPOSER_CLASSIFICATION_PATH,
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

ALLOWED_SURFACES = [
    SOURCE_VALUES_PROPOSER_RECEIPT_PATH,
    SOURCE_VALUES_PROPOSAL_PATH,
    SOURCE_VALUES_PROPOSER_CLASSIFICATION_PATH,
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

PATH_LIKE_RE = re.compile(r"^[A-Za-z0-9_./:-]+$")
SEMANTIC_TERMS = {
    "target",
    "candidate",
    "runtime",
    "patch",
    "value",
    "values",
    "hint",
    "ref",
    "path",
    "source",
    "evidence",
    "verification",
    "gate",
    "rollback",
    "boundary",
    "stop",
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
    if len(value) > 500:
        return False
    if not PATH_LIKE_RE.match(value):
        return False
    return "/" in value or value.endswith((".json", ".jsonl", ".txt", ".csv", ".py", ".md"))

def semantic_score(path: str, value: Any) -> int:
    text = path.lower()
    if isinstance(value, str):
        text += " " + value.lower()
    score = 0
    for term in SEMANTIC_TERMS:
        if term in text:
            score += 1
    return score

def validate_source_basis() -> List[str]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    values_proposer = read_json(SOURCE_VALUES_PROPOSER_RECEIPT_PATH)
    values_proposal = read_json(SOURCE_VALUES_PROPOSAL_PATH)
    values_classification = read_json(SOURCE_VALUES_PROPOSER_CLASSIFICATION_PATH)
    operator_values = read_json(SOURCE_OPERATOR_VALUES_RECEIPT_PATH)
    provider = read_json(SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_PATH)
    input_receipt = read_json(SOURCE_INPUT_REQUEST_RECEIPT_PATH)
    input_contract = read_json(SOURCE_INPUT_CONTRACT_PATH)
    review = read_json(SOURCE_REVIEW_RECEIPT_PATH)
    review_classification = read_json(SOURCE_REVIEW_CLASSIFICATION_PATH)
    schema = read_json(SOURCE_SCHEMA_PATH)
    inventory = read_json(SOURCE_HINT_INVENTORY_PATH)

    if values_proposer.get("receipt_id") != SOURCE_VALUES_PROPOSER_RECEIPT_ID or values_proposer.get("gate") != "PASS":
        failures.append("values_proposer_receipt_not_pass")
    if values_proposer.get("values_proposer_summary", {}).get("status") != "NO_BOUNDED_TARGET_VALUE_SOURCE":
        failures.append("values_proposer_source_not_no_bounded_target_value_source")
    if values_proposer.get("terminal", {}).get("stop_code") != "STOP_NO_BOUNDED_TARGET_VALUE_SOURCE":
        failures.append("values_proposer_wrong_terminal")
    if values_proposal.get("proposal_status") != "NO_BOUNDED_TARGET_VALUE_SOURCE":
        failures.append("values_proposal_wrong_status")
    if values_classification.get("classification_status") != "NO_BOUNDED_TARGET_VALUE_SOURCE":
        failures.append("values_classification_wrong_status")

    if operator_values.get("receipt_id") != SOURCE_OPERATOR_VALUES_RECEIPT_ID or operator_values.get("gate") != "PASS":
        failures.append("operator_values_receipt_not_pass")
    if operator_values.get("operator_values_summary", {}).get("status") != "OPERATOR_TARGET_EVIDENCE_VALUES_MISSING_OR_INVALID":
        failures.append("operator_values_source_not_missing_or_invalid")

    if provider.get("receipt_id") != SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_ID or provider.get("gate") != "PASS":
        failures.append("provider_materialization_receipt_not_pass")
    if provider.get("provider_materialization_summary", {}).get("status") != "EXPLICIT_TARGET_EVIDENCE_PROVIDER_MATERIALIZED":
        failures.append("provider_not_materialized")

    if input_receipt.get("receipt_id") != SOURCE_INPUT_REQUEST_RECEIPT_ID or input_receipt.get("gate") != "PASS":
        failures.append("input_request_receipt_not_pass")
    if input_contract.get("target_selected_for_build") is not False:
        failures.append("input_contract_selects_target_for_build")
    if input_contract.get("runtime_patch_authorized") is not False:
        failures.append("input_contract_authorizes_runtime_patch")

    if review.get("receipt_id") != SOURCE_REVIEW_RECEIPT_ID or review.get("gate") != "PASS":
        failures.append("review_receipt_not_pass")
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

def collect_surface_map() -> Dict[str, Any]:
    source_summaries: List[Dict[str, Any]] = []
    path_like_values: List[Dict[str, Any]] = []
    semantic_hits: List[Dict[str, Any]] = []
    hint_inventory_rows: List[Dict[str, Any]] = []
    typed_value_source_rows: List[Dict[str, Any]] = []

    for source_path in ALLOWED_SURFACES:
        obj = read_json(source_path)
        rel_source = rel(source_path)

        top_keys = sorted(obj.keys()) if isinstance(obj, dict) else []
        source_summary = {
            "source_ref": rel_source,
            "top_level_keys": top_keys,
            "sha256": file_sha256(source_path),
        }
        source_summaries.append(source_summary)

        for path, value in walk(obj):
            score = semantic_score(path, value)

            if score >= 2:
                semantic_hits.append({
                    "source_ref": rel_source,
                    "json_path": path,
                    "semantic_score": score,
                    "value_type": type(value).__name__,
                    "value_preview": value[:160] if isinstance(value, str) else None,
                })

            if safe_local_bounded_path(value):
                row = {
                    "source_ref": rel_source,
                    "json_path": path,
                    "value": value,
                    "semantic_score": score,
                }
                path_like_values.append(row)

                lower_path = path.lower()
                lower_value = value.lower() if isinstance(value, str) else ""
                if any(t in lower_path for t in ["target", "candidate", "runtime_patch", "patch_target"]) or any(t in lower_value for t in ["target", "runtime_patch", "patch_target"]):
                    typed_value_source_rows.append({
                        **row,
                        "candidate_reason": "path-like value has target/runtime/patch semantic marker",
                    })

            if rel_source == rel(SOURCE_HINT_INVENTORY_PATH) and isinstance(value, dict):
                keys = sorted(str(k) for k in value.keys())
                local_refs = []
                for child_path, child_value in walk(value):
                    if safe_local_bounded_path(child_value):
                        local_refs.append({"json_path": child_path, "value": child_value})
                if keys or local_refs:
                    hint_inventory_rows.append({
                        "json_path": path,
                        "keys": keys,
                        "local_ref_count": len(local_refs),
                        "local_refs": local_refs[:20],
                        "has_target_marker": any("target" in k.lower() or "candidate" in k.lower() for k in keys),
                        "has_verification_marker": any("verification" in k.lower() or "gate" in k.lower() for k in keys),
                        "has_rollback_marker": any("rollback" in k.lower() or "boundary" in k.lower() or "stop" in k.lower() for k in keys),
                    })

    unique_path_values = {}
    for row in path_like_values:
        key = (row["source_ref"], row["json_path"], row["value"])
        unique_path_values[key] = row

    unique_typed_rows = {}
    for row in typed_value_source_rows:
        key = (row["source_ref"], row["json_path"], row["value"])
        unique_typed_rows[key] = row

    map_obj = {
        "schema_version": "runtime_patch_target_value_source_surface_map_v0",
        "source_surface_map_id": "value_source_surface_" + sha8({
            "sources": [rel(p) for p in ALLOWED_SURFACES],
            "path_like_count": len(unique_path_values),
            "typed_count": len(unique_typed_rows),
        }),
        "allowed_surface_count": len(ALLOWED_SURFACES),
        "allowed_surfaces": source_summaries,
        "path_like_value_count": len(unique_path_values),
        "path_like_values": list(unique_path_values.values())[:300],
        "semantic_hit_count": len(semantic_hits),
        "semantic_hits": sorted(semantic_hits, key=lambda x: x["semantic_score"], reverse=True)[:300],
        "hint_inventory_row_count": len(hint_inventory_rows),
        "hint_inventory_rows": hint_inventory_rows[:300],
        "typed_value_source_row_count": len(unique_typed_rows),
        "typed_value_source_rows": list(unique_typed_rows.values())[:300],
    }
    return map_obj

def classify_surface(surface: Dict[str, Any]) -> Tuple[str, List[str], str]:
    path_like_count = surface["path_like_value_count"]
    typed_count = surface["typed_value_source_row_count"]
    hint_row_count = surface["hint_inventory_row_count"]

    if path_like_count == 0 and hint_row_count == 0:
        return (
            "VALUE_SOURCE_SURFACE_ABSENT",
            ["NO_PATH_LIKE_VALUES", "NO_HINT_INVENTORY_ROWS_EXTRACTED"],
            "RETURN_TO_TARGET_NARROWING_WITH_VALUE_SOURCE_REQUIREMENT_V0",
        )

    if typed_count == 0 and (path_like_count > 0 or hint_row_count > 0):
        return (
            "VALUE_SOURCE_SURFACE_PRESENT_BUT_UNTYPED",
            ["PATH_OR_HINT_SURFACE_EXISTS", "NO_TYPED_TARGET_VALUE_SOURCE_ROWS"],
            "TYPE_RUNTIME_PATCH_TARGET_HINT_INVENTORY_AS_VALUE_SOURCE_V0",
        )

    if typed_count == 1:
        return (
            "VALUE_SOURCE_SURFACE_BRIDGE_READY",
            ["ONE_TYPED_TARGET_VALUE_SOURCE_ROW"],
            "MATERIALIZE_TARGET_VALUE_SOURCE_BRIDGE_FROM_SURFACE_MAP_V0",
        )

    return (
        "VALUE_SOURCE_SURFACE_MULTIPLE_AMBIGUOUS",
        ["MULTIPLE_TYPED_TARGET_VALUE_SOURCE_ROWS", "NO_SINGLE_DOMINANT_VALUE_SOURCE"],
        "NARROW_RUNTIME_PATCH_TARGET_VALUE_SOURCE_SURFACE_V0",
    )

def recommendation_obj(status: str, reason_codes: List[str], next_object: str, surface: Dict[str, Any]) -> Dict[str, Any]:
    if status == "VALUE_SOURCE_SURFACE_PRESENT_BUT_UNTYPED":
        instruction = (
            "Allowed evidence surfaces contain hint/path/semantic material, but no typed target-value-source row. "
            "Next repair should add a bridge schema that marks which bounded hint field is allowed to become SELECTED_TARGET_REF, "
            "and where verification/rollback refs must come from."
        )
    elif status == "VALUE_SOURCE_SURFACE_BRIDGE_READY":
        instruction = (
            "Exactly one typed target-value-source row is visible. Next repair may materialize a bridge adapter from this surface map, "
            "still without declaring target for review or accepting for build."
        )
    elif status == "VALUE_SOURCE_SURFACE_MULTIPLE_AMBIGUOUS":
        instruction = (
            "Multiple typed target-value-source rows exist. Next repair must narrow or rank by explicit schema rule, not preference."
        )
    else:
        instruction = (
            "No usable bounded value-source surface exists. Return to target narrowing and require a value-source-bearing artifact."
        )

    return {
        "schema_version": "runtime_patch_target_value_source_bridge_repair_recommendation_v0",
        "recommendation_status": status,
        "reason_codes": reason_codes,
        "recommended_next": next_object,
        "repair_instruction": instruction,
        "surface_counts": {
            "allowed_surface_count": surface["allowed_surface_count"],
            "path_like_value_count": surface["path_like_value_count"],
            "semantic_hit_count": surface["semantic_hit_count"],
            "hint_inventory_row_count": surface["hint_inventory_row_count"],
            "typed_value_source_row_count": surface["typed_value_source_row_count"],
        },
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "not_authorized": [
            "select target for build",
            "declare target candidate for review",
            "accept proposal",
            "apply runtime patch",
            "modify target files",
            "open C5",
            "grant general Cell1 authority",
            "use latest-file guessing",
            "use mtime selection",
            "collapse ambiguity by preference"
        ],
    }

def classification_obj(status: str, reason_codes: List[str], next_object: str, surface: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "runtime_patch_target_value_source_surface_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "recommended_next": next_object,
        "path_like_value_count": surface["path_like_value_count"],
        "semantic_hit_count": surface["semantic_hit_count"],
        "hint_inventory_row_count": surface["hint_inventory_row_count"],
        "typed_value_source_row_count": surface["typed_value_source_row_count"],
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "next_command_goal": None,
    }

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "runtime_patch_target_value_source_surface_authority_boundary_v0",
        "status": status,
        "may_inspect_allowed_evidence_surfaces": True,
        "may_emit_source_surface_map": True,
        "may_emit_repair_recommendation": True,
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
            "path-like value is automatically a target",
            "hint row is automatically a selected target",
            "repair recommendation authorizes patching",
            "source-surface bridge is equivalent to build acceptance"
        ],
    }

def rollup_obj(status: str, surface: Dict[str, Any], next_object: str) -> Dict[str, Any]:
    return {
        "schema_version": "runtime_patch_target_value_source_surface_rollup_v0",
        "build_mode": BUILD_MODE,
        "surface_classification": status,
        "allowed_surface_count": surface["allowed_surface_count"],
        "path_like_value_count": surface["path_like_value_count"],
        "semantic_hit_count": surface["semantic_hit_count"],
        "hint_inventory_row_count": surface["hint_inventory_row_count"],
        "typed_value_source_row_count": surface["typed_value_source_row_count"],
        "source_surface_map_emitted_count": 1,
        "bridge_repair_recommendation_emitted_count": 1,
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
        "recommended_next": next_object,
    }

def profile_obj(status: str, roll: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "runtime_patch_target_value_source_surface_profile_v0",
        "profile_id": "value_source_surface_repair_" + sha8({"status": status, "counts": roll}),
        "status": status,
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": all(roll.get(k) == 0 for k in [
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
        ]),
        "recommended_next": roll["recommended_next"],
        "next_command_goal": None,
    }

def report_obj(status: str, reason_codes: List[str], surface: Dict[str, Any], next_object: str) -> Dict[str, Any]:
    return {
        "schema_version": "runtime_patch_target_value_source_surface_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "allowed_surface_count": surface["allowed_surface_count"],
        "path_like_value_count": surface["path_like_value_count"],
        "semantic_hit_count": surface["semantic_hit_count"],
        "hint_inventory_row_count": surface["hint_inventory_row_count"],
        "typed_value_source_row_count": surface["typed_value_source_row_count"],
        "recommended_next_handling": next_object,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
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

def trace_obj(status: str, reason_codes: List[str], next_object: str) -> Dict[str, Any]:
    return {
        "schema_version": "runtime_patch_target_value_source_surface_transition_trace_v0",
        "trace": [
            {
                "step": "consume_values_proposer_no_source_halt",
                "question": "did the proposer fail structurally or lack a typed value source",
                "answer": "proposer ran and halted with NO_BOUNDED_TARGET_VALUE_SOURCE",
                "taken": "inspect_allowed_source_surface",
            },
            {
                "step": "classify_source_surface",
                "question": "is source absent, present-but-untyped, bridge-ready, or multiple",
                "answer": status,
                "reason_codes": reason_codes,
                "taken": next_object,
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
    failures = validate_source_basis()

    if failures:
        surface = {
            "schema_version": "runtime_patch_target_value_source_surface_map_v0",
            "source_surface_map_id": "value_source_surface_source_fail_" + sha8(failures),
            "allowed_surface_count": len(ALLOWED_SURFACES),
            "allowed_surfaces": [],
            "path_like_value_count": 0,
            "path_like_values": [],
            "semantic_hit_count": 0,
            "semantic_hits": [],
            "hint_inventory_row_count": 0,
            "hint_inventory_rows": [],
            "typed_value_source_row_count": 0,
            "typed_value_source_rows": [],
        }
        status = "VALUE_SOURCE_SURFACE_SOURCE_BASIS_FAIL"
        reason_codes = failures
        next_object = "REPAIR_VALUES_PROPOSER_SOURCE_BASIS_V0"
    else:
        surface = collect_surface_map()
        status, reason_codes, next_object = classify_surface(surface)

    recommendation = recommendation_obj(status, reason_codes, next_object, surface)
    classification = classification_obj(status, reason_codes, next_object, surface)
    boundary = authority_boundary_obj(status)
    roll = rollup_obj(status, surface, next_object)
    prof = profile_obj(status, roll)
    rep = report_obj(status, reason_codes, surface, next_object)
    tr = trace_obj(status, reason_codes, next_object)

    write_json(SOURCE_SURFACE_MAP_PATH, surface)
    write_json(BRIDGE_REPAIR_RECOMMENDATION_PATH, recommendation)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(AUTHORITY_BOUNDARY_PATH, boundary)
    write_json(ROLLUP_PATH, roll)
    write_json(PROFILE_PATH, prof)
    write_json(REPORT_PATH, rep)
    write_json(TRANSITION_TRACE_PATH, tr)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        roll["source_mutation_count"] = 1
        rep["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, roll)
        write_json(REPORT_PATH, rep)

    acceptance_gate_results = {
        "VALUE_SOURCE_SURFACE_0_VALUES_PROPOSER_RECEIPT_CONSUMED": SOURCE_VALUES_PROPOSER_RECEIPT_PATH.exists(),
        "VALUE_SOURCE_SURFACE_1_HINT_INVENTORY_CONSUMED": SOURCE_HINT_INVENTORY_PATH.exists(),
        "VALUE_SOURCE_SURFACE_2_REQUEST_PACKET_CONSUMED": SOURCE_REQUEST_PACKET_PATH.exists(),
        "VALUE_SOURCE_SURFACE_3_SOURCE_SURFACE_MAP_EMITTED": SOURCE_SURFACE_MAP_PATH.exists(),
        "VALUE_SOURCE_SURFACE_4_BRIDGE_REPAIR_RECOMMENDATION_EMITTED": BRIDGE_REPAIR_RECOMMENDATION_PATH.exists(),
        "VALUE_SOURCE_SURFACE_5_CLASSIFICATION_EMITTED": CLASSIFICATION_PATH.exists(),
        "VALUE_SOURCE_SURFACE_6_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classification["target_candidate_declared_for_review"] is False,
        "VALUE_SOURCE_SURFACE_7_NO_TARGET_SELECTED_FOR_BUILD": classification["target_selected_for_build"] is False,
        "VALUE_SOURCE_SURFACE_8_NO_ACCEPTED_FOR_BUILD": classification["accepted_for_build"] is False,
        "VALUE_SOURCE_SURFACE_9_NO_RUNTIME_PATCH": classification["runtime_patch_authorized"] is False,
        "VALUE_SOURCE_SURFACE_10_NO_TARGET_FILE_MODIFICATION": classification["target_file_modification_authorized"] is False,
        "VALUE_SOURCE_SURFACE_11_NO_C5_OPENED": classification["c5_authorized"] is False,
        "VALUE_SOURCE_SURFACE_12_NO_GENERAL_CELL1_AUTHORITY": classification["general_cell1_authority_granted"] is False,
        "VALUE_SOURCE_SURFACE_13_NO_LATEST_FILE_GUESSING": classification["latest_file_guessing"] is False,
        "VALUE_SOURCE_SURFACE_14_NO_MTIME_SELECTION": classification["mtime_selection"] is False,
        "VALUE_SOURCE_SURFACE_15_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "VALUE_SOURCE_SURFACE_16_ACCEPTANCE_BOUNDARY_RETAINED": boundary["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "VALUE_SOURCE_SURFACE_17_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = tr["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_VALUE_SOURCE_SURFACE_REPAIR_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "reason_codes": reason_codes,
        "counts": {
            "path_like": surface["path_like_value_count"],
            "hint_rows": surface["hint_inventory_row_count"],
            "typed_rows": surface["typed_value_source_row_count"],
        },
        "terminal": terminal,
        "gate": gate,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "runtime_patch_target_value_source_surface_repair_receipt_v0",
        "receipt_type": "RUNTIME_PATCH_TARGET_VALUE_SOURCE_SURFACE_REPAIR_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_values_proposer_receipt_id": SOURCE_VALUES_PROPOSER_RECEIPT_ID,
        "source_operator_values_receipt_id": SOURCE_OPERATOR_VALUES_RECEIPT_ID,
        "source_provider_materialization_receipt_id": SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_ID,
        "source_input_request_receipt_id": SOURCE_INPUT_REQUEST_RECEIPT_ID,
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "value_source_surface_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "allowed_surface_count": surface["allowed_surface_count"],
            "path_like_value_count": surface["path_like_value_count"],
            "semantic_hit_count": surface["semantic_hit_count"],
            "hint_inventory_row_count": surface["hint_inventory_row_count"],
            "typed_value_source_row_count": surface["typed_value_source_row_count"],
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
            "recommended_next": next_object,
        },
        "aggregate_metrics": rep,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "source_surface_map": rel(SOURCE_SURFACE_MAP_PATH),
            "bridge_repair_recommendation": rel(BRIDGE_REPAIR_RECOMMENDATION_PATH),
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
    print(f"value_source_surface_repair_receipt_id={receipt_id}")
    print(f"value_source_surface_repair_receipt_path={rel(receipt_path)}")
    print(f"value_source_surface_map_path={rel(SOURCE_SURFACE_MAP_PATH)}")
    print(f"value_source_bridge_repair_recommendation_path={rel(BRIDGE_REPAIR_RECOMMENDATION_PATH)}")
    print(f"value_source_surface_classification_path={rel(CLASSIFICATION_PATH)}")
    print(f"value_source_surface_rollup_path={rel(ROLLUP_PATH)}")
    print(f"value_source_surface_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
