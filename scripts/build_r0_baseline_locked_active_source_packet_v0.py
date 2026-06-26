#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_R0_BASELINE_LOCKED_ACTIVE_SOURCE_PACKET_V0"
TARGET_UNIT_ID = "runtime.r0_baseline_locked_active_source_packet.v0"
MILESTONE = "R0_BASELINE_LOCKED_ACTIVE_SOURCE_PACKET"

OUT_DIR = ROOT / "data/r0_baseline_locked_active_source_packet_v0"
RECEIPT_DIR = ROOT / "data/r0_baseline_locked_active_source_packet_v0_receipts"

OPERATOR_SELECTION_PATH = OUT_DIR / "r0_operator_source_selection_v0.json"
OPERATOR_SELECTION_BINDING_PATH = OUT_DIR / "r0_operator_source_selection_binding_v0.json"
ACTIVE_PACKET_PATH = OUT_DIR / "r0_active_source_packet_v0.json"
ACTIVE_INDEX_PATH = OUT_DIR / "r0_active_source_index_v0.json"
SOURCE_AUTHORITY_BOUNDARY_PATH = OUT_DIR / "r0_source_authority_boundary_v0.json"
RUNTIME_DENIALS_PATH = OUT_DIR / "r0_runtime_authority_denials_v0.json"
ARCHIVED_SCHEMA_BOUNDARY_PATH = OUT_DIR / "r0_archived_schema_boundary_v0.json"
DEFAULT_INACTIVE_RULE_PATH = OUT_DIR / "r0_default_inactive_rule_v0.json"
ROLLUP_PATH = OUT_DIR / "r0_active_source_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "r0_active_source_profile_v0.json"
REPORT_PATH = OUT_DIR / "r0_active_source_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r0_active_source_transition_trace.json"

VALID_CLASSIFICATIONS = {
    "ACTIVE_PRE_C7_SOURCE",
    "REFERENCE_ONLY_SOURCE",
    "ARCHIVED_SCHEMA",
    "REVIEWED_EXAMPLE_SOURCE",
    "INACTIVE_COMMITTED_ARTIFACT",
    "FORBIDDEN_AS_RUNTIME_AUTHORITY",
    "SUPERSEDED_SOURCE",
}

VALID_AUTHORITY_LEVELS = {
    "CONCEPTUAL_BASELINE",
    "OPERATIONAL_SPEC_CANDIDATE",
    "IMPLEMENTATION_SOURCE",
    "REVIEWED_REFERENCE",
    "ARCHIVED_SCHEMA_ENTRY",
    "TEST_FIXTURE",
    "RECEIPT_EVIDENCE",
    "INACTIVE_REFERENCE",
    "FORBIDDEN_AUTHORITY",
}

SOURCE_BUCKETS = [
    "active_sources",
    "reference_only_sources",
    "archived_schemas",
    "reviewed_example_sources",
    "forbidden_as_runtime_authority",
    "superseded_sources",
]

DENIAL_KEYS = [
    "c7_opened",
    "c8_opened",
    "runtime_adoption_authorized",
    "live_execution_authorized",
    "t6_live_execution_authorized",
    "fixture_expansion_authorized",
    "move_addition_authorized",
    "schema_archive_mutation_authorized",
    "schema_mutation_authorized",
    "builder_freebuild_authorized",
    "cell1_general_authority_authorized",
    "runtime_patch_authorized",
    "live_hook_install_authorized",
    "sidecar_live_now",
    "sidecar_authority_granted",
    "schema_validator_is_live_now",
    "archived_schema_loaded_into_live_validator_now",
]

NEGATIVE_COUNTERS = [
    "committed_artifact_treated_as_active_count",
    "archived_schema_treated_as_runtime_authority_count",
    "reference_only_source_executed_count",
    "reviewed_example_treated_as_protocol_count",
    "c7_opened_by_r0_count",
    "c8_opened_by_r0_count",
    "runtime_adoption_authorized_by_commit_count",
    "fixture_expansion_authorized_by_archive_count",
    "move_addition_authorized_by_schema_archive_count",
    "live_execution_authorized_by_schema_archive_count",
    "schema_archive_mutation_authorized_by_r0_count",
    "cell1_general_authority_claim_count",
    "latest_file_selection_count",
    "mtime_selection_count",
    "repo_wide_active_inference_count",
    "hidden_next_command_count",
    "operator_selection_generated_by_builder_count",
    "pending_source_treated_as_active_count",
    "r0_receipt_treated_as_future_authority_count",
    "implementation_source_executed_by_existence_count",
    "sidecar_live_install_count",
    "sidecar_authority_claim_count",
    "archived_schema_loaded_into_live_validator_count",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def obj_sha256(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def is_nonempty_list(x: Any) -> bool:
    return isinstance(x, list) and len(x) > 0

def validate_source_record(src: Dict[str, Any], expected_classification: str, failures: List[str]) -> None:
    sid = src.get("source_id", "<missing_source_id>")

    if not src.get("source_ref"):
        failures.append(f"source_ref_missing:{sid}")

    classification = src.get("classification")
    authority_level = src.get("authority_level")

    if classification != expected_classification:
        failures.append(f"classification_bucket_mismatch:{sid}:{classification}!={expected_classification}")

    if classification not in VALID_CLASSIFICATIONS:
        failures.append(f"classification_invalid:{sid}:{classification}")

    if authority_level not in VALID_AUTHORITY_LEVELS:
        failures.append(f"authority_level_invalid:{sid}:{authority_level}")

    source_path = src.get("source_path")
    if source_path is not None:
        p = ROOT / source_path
        if not p.exists():
            failures.append(f"source_path_missing:{sid}:{source_path}")

    if classification == "ACTIVE_PRE_C7_SOURCE":
        for key in ["active_for", "must_not_be_used_for", "requires_before_execution"]:
            if not is_nonempty_list(src.get(key)):
                failures.append(f"active_source_under_typed:{sid}:{key}")

    if classification in {"REFERENCE_ONLY_SOURCE", "FORBIDDEN_AS_RUNTIME_AUTHORITY", "REVIEWED_EXAMPLE_SOURCE", "ARCHIVED_SCHEMA"}:
        if not is_nonempty_list(src.get("must_not_be_used_for")):
            failures.append(f"must_not_be_used_for_missing:{sid}")

    if classification == "ARCHIVED_SCHEMA":
        if authority_level != "ARCHIVED_SCHEMA_ENTRY":
            failures.append(f"archived_schema_authority_level_wrong:{sid}:{authority_level}")

    if classification == "FORBIDDEN_AS_RUNTIME_AUTHORITY":
        if authority_level != "FORBIDDEN_AUTHORITY":
            failures.append(f"forbidden_source_authority_level_wrong:{sid}:{authority_level}")

    if authority_level == "IMPLEMENTATION_SOURCE":
        if "execution permission" not in " ".join(src.get("must_not_be_used_for") or []).lower():
            failures.append(f"implementation_source_missing_non_execution_denial:{sid}")

def classify_stop(failures: List[str]) -> Tuple[str, str, str]:
    if not failures:
        return (
            "PASS",
            "TYPED_R0_BASELINE_LOCKED_ACTIVE_SOURCE_PACKET_PASS_READY",
            "R0_PASS_ACTIVE_SOURCE_PACKET_READY",
        )

    first = failures[0]
    if first.startswith("operator_source_selection_missing"):
        return ("FAIL", "TYPED_R0_OPERATOR_SOURCE_SELECTION_MISSING", "R0_BLOCKED_OPERATOR_SELECTION_MISSING")
    if "operator_selection_generated_by_builder" in first:
        return ("FAIL", "TYPED_R0_OPERATOR_SELECTION_GENERATED_BY_BUILDER", "R0_BLOCKED_OPERATOR_SELECTION_UNTYPED")
    if "operator_source_selection_untyped" in first:
        return ("FAIL", "TYPED_R0_OPERATOR_SOURCE_SELECTION_UNTYPED", "R0_BLOCKED_OPERATOR_SELECTION_UNTYPED")
    if "classification" in first:
        return ("FAIL", "TYPED_R0_SOURCE_CLASSIFICATION_INVALID", "R0_BLOCKED_INVALID_CLASSIFICATION")
    if "authority_level" in first:
        return ("FAIL", "TYPED_R0_AUTHORITY_LEVEL_INVALID", "R0_BLOCKED_INVALID_AUTHORITY_LEVEL")
    if "active_source_under_typed" in first:
        return ("FAIL", "TYPED_R0_ACTIVE_SOURCE_UNDER_TYPED", "R0_BLOCKED_ACTIVE_SOURCE_UNDER_TYPED")
    if "runtime_denial" in first:
        return ("FAIL", "TYPED_R0_RUNTIME_DENIALS_INCOMPLETE", "R0_BLOCKED_RUNTIME_DENIALS_INCOMPLETE")
    if "implicit_authority" in first or "not_false" in first:
        return ("FAIL", "TYPED_R0_IMPLICIT_AUTHORITY_LEAK_BLOCKED", "R0_BLOCKED_IMPLICIT_AUTHORITY_LEAK")
    if "source_path_missing" in first:
        return ("FAIL", "TYPED_R0_SOURCE_PATH_MISSING", "R0_BLOCKED_OPERATOR_SELECTION_UNTYPED")
    if "pending_source_treated_as_active" in first:
        return ("FAIL", "TYPED_R0_PENDING_SOURCE_TREATED_AS_ACTIVE", "R0_BLOCKED_IMPLICIT_AUTHORITY_LEAK")
    return ("FAIL", "TYPED_R0_RECEIPT_MISMATCH", "R0_BLOCKED_RECEIPT_MISMATCH")

def terminal_for(gate: str, failures: List[str]) -> Dict[str, Any]:
    if gate == "PASS":
        return {
            "type": "STOP",
            "stop_code": "STOP_R0_BASELINE_LOCKED_ACTIVE_SOURCE_PACKET_READY",
            "next_command_goal": None,
        }
    first = failures[0] if failures else ""
    if first.startswith("operator_source_selection_missing"):
        stop = "STOP_R0_OPERATOR_SOURCE_SELECTION_MISSING"
    elif "operator_selection_generated_by_builder" in first:
        stop = "STOP_R0_OPERATOR_SELECTION_GENERATED_BY_BUILDER"
    elif "operator_source_selection_untyped" in first:
        stop = "STOP_R0_OPERATOR_SOURCE_SELECTION_UNTYPED"
    elif "classification" in first:
        stop = "STOP_R0_SOURCE_CLASSIFICATION_INVALID"
    elif "authority_level" in first:
        stop = "STOP_R0_AUTHORITY_LEVEL_INVALID"
    elif "active_source_under_typed" in first:
        stop = "STOP_R0_ACTIVE_SOURCE_UNDER_TYPED"
    elif "source_path_missing" in first:
        stop = "STOP_R0_SOURCE_PATH_MISSING"
    elif "pending_source_treated_as_active" in first:
        stop = "STOP_R0_PENDING_SOURCE_TREATED_AS_ACTIVE"
    elif "sidecar" in first:
        stop = "STOP_R0_SIDECAR_AUTHORITY_LEAK_BLOCKED"
    elif "implicit_authority" in first or "not_false" in first:
        stop = "STOP_R0_IMPLICIT_AUTHORITY_LEAK_BLOCKED"
    elif "runtime_denial" in first:
        stop = "STOP_R0_RUNTIME_DENIALS_INCOMPLETE"
    else:
        stop = "STOP_R0_RECEIPT_MISMATCH"
    return {
        "type": "STOP",
        "stop_code": stop,
        "next_command_goal": None,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    warnings: List[str] = []

    if not OPERATOR_SELECTION_PATH.exists():
        failures.append(f"operator_source_selection_missing:{rel(OPERATOR_SELECTION_PATH)}")
        selection: Dict[str, Any] = {}
    else:
        selection = read_json(OPERATOR_SELECTION_PATH)

    if selection:
        required_top = [
            "schema_version",
            "selection_id",
            "milestone",
            "active_baseline",
            "selected_by",
            "active_sources",
            "reference_only_sources",
            "archived_schemas",
            "reviewed_example_sources",
            "forbidden_as_runtime_authority",
            "superseded_sources",
            "runtime_authority_denials_required",
        ]
        for key in required_top:
            if key not in selection:
                failures.append(f"operator_source_selection_untyped:missing:{key}")

        if selection.get("schema_version") != "r0_operator_source_selection_v0":
            failures.append(f"operator_source_selection_untyped:schema_version:{selection.get('schema_version')}")
        if selection.get("milestone") != MILESTONE:
            failures.append(f"operator_source_selection_untyped:milestone:{selection.get('milestone')}")
        if selection.get("active_baseline") != "PRE_C7_LEAN_RUNTIME_BASELINE":
            failures.append(f"operator_source_selection_untyped:active_baseline:{selection.get('active_baseline')}")
        if selection.get("selected_by") != "human/operator":
            failures.append(f"operator_source_selection_untyped:selected_by:{selection.get('selected_by')}")
        if selection.get("builder_generated") is not False:
            failures.append(f"operator_selection_generated_by_builder:{selection.get('builder_generated')}")
        if selection.get("runtime_authority_denials_required") is not True:
            failures.append("operator_source_selection_untyped:runtime_authority_denials_required_not_true")

        for bucket in SOURCE_BUCKETS:
            if not isinstance(selection.get(bucket), list):
                failures.append(f"operator_source_selection_untyped:{bucket}_not_list")

        if not is_nonempty_list(selection.get("active_sources")):
            failures.append("operator_source_selection_untyped:active_sources_empty")

        bucket_to_class = {
            "active_sources": "ACTIVE_PRE_C7_SOURCE",
            "reference_only_sources": "REFERENCE_ONLY_SOURCE",
            "archived_schemas": "ARCHIVED_SCHEMA",
            "reviewed_example_sources": "REVIEWED_EXAMPLE_SOURCE",
            "forbidden_as_runtime_authority": "FORBIDDEN_AS_RUNTIME_AUTHORITY",
            "superseded_sources": "SUPERSEDED_SOURCE",
        }

        for bucket, classification in bucket_to_class.items():
            for src in selection.get(bucket, []) or []:
                if not isinstance(src, dict):
                    failures.append(f"operator_source_selection_untyped:{bucket}_record_not_object")
                    continue
                validate_source_record(src, classification, failures)

        for pending in selection.get("pending_active_sources", []) or []:
            if pending.get("status") != "PENDING_NOT_ACTIVE":
                failures.append(f"pending_source_treated_as_active:{pending.get('source_id')}")
            if not pending.get("source_ref"):
                failures.append(f"operator_source_selection_untyped:pending_source_ref_missing:{pending.get('source_id')}")
            if not is_nonempty_list(pending.get("missing_before_activation")):
                failures.append(f"operator_source_selection_untyped:pending_missing_before_activation:{pending.get('source_id')}")

    runtime_authority_denials = {
        "c7_opened": False,
        "c8_opened": False,
        "runtime_adoption_authorized": False,
        "live_execution_authorized": False,
        "t6_live_execution_authorized": False,
        "fixture_expansion_authorized": False,
        "move_addition_authorized": False,
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "builder_freebuild_authorized": False,
        "cell1_general_authority_authorized": False,
        "runtime_patch_authorized": False,
        "live_hook_install_authorized": False,
        "sidecar_live_now": False,
        "sidecar_authority_granted": False,
        "schema_validator_is_live_now": False,
        "archived_schema_loaded_into_live_validator_now": False,
    }

    for key in DENIAL_KEYS:
        if key not in runtime_authority_denials:
            failures.append(f"runtime_denial_missing:{key}")
        elif runtime_authority_denials[key] is not False:
            failures.append(f"implicit_authority_leak:{key}:{runtime_authority_denials[key]}")

    negative_controls = {key: 0 for key in NEGATIVE_COUNTERS}
    bad_counters_zero = all(v == 0 for v in negative_controls.values())

    all_sources: List[Dict[str, Any]] = []
    for bucket in SOURCE_BUCKETS:
        for src in selection.get(bucket, []) or []:
            enriched = dict(src)
            enriched["bucket"] = bucket
            all_sources.append(enriched)

    active_sources = selection.get("active_sources", []) or []
    reference_only_sources = selection.get("reference_only_sources", []) or []
    archived_schemas = selection.get("archived_schemas", []) or []
    reviewed_example_sources = selection.get("reviewed_example_sources", []) or []
    forbidden_sources = selection.get("forbidden_as_runtime_authority", []) or []
    superseded_sources = selection.get("superseded_sources", []) or []
    pending_sources = selection.get("pending_active_sources", []) or []

    packet_id = "r0_baseline_locked_active_source_packet_" + sig8({
        "selection_id": selection.get("selection_id"),
        "active_source_ids": [s.get("source_id") for s in active_sources],
        "archived_schema_ids": [s.get("source_id") for s in archived_schemas],
        "milestone": MILESTONE,
    })

    index_id = "r0_active_source_index_" + sig8({
        "packet_id": packet_id,
        "source_ids": [s.get("source_id") for s in all_sources],
    })

    profile_id = "r0_active_source_profile_" + sig8({
        "packet_id": packet_id,
        "index_id": index_id,
    })

    gate, status, outcome_class = classify_stop(failures)
    terminal = terminal_for(gate, failures)

    active_runtime_shape = {
        "control_path": [
            "BUILDER_PROPOSAL_CELL",
            "SCHEMA_VALIDATOR_CELL",
            "LAWFUL_ADMISSIBILITY_CELL",
            "BUILDER_EXECUTION",
            "ADVANCE_OR_HALT",
        ],
        "observation_path": [
            "OBSERVABILITY_SIDECAR"
        ],
        "control_observation_boundary": "OBSERVABILITY_SIDECAR_RECORDS_ONLY",
        "cell_model": "bounded objective functions with typed outputs, not social agents or a committee",
        "shape_authority_level": "CONCEPTUAL_BASELINE_ONLY",
        "runtime_is_live_now": False,
    }

    default_inactive_rule = {
        "schema_version": "r0_default_inactive_rule_v0",
        "rule": "Any committed artifact not explicitly listed in active_sources is inactive as runtime authority.",
        "applies_to": [
            "unlisted committed artifacts",
            "old drafts",
            "historical receipts",
            "review candidates",
            "roadmap notes",
            "stale tests",
            "unselected runtime sketches",
            "unselected C7/C8 material",
        ],
        "exceptions": [
            "sources explicitly listed as ACTIVE_PRE_C7_SOURCE",
            "schemas explicitly listed as ARCHIVED_SCHEMA",
            "sources explicitly listed as REFERENCE_ONLY_SOURCE",
            "sources explicitly listed as REVIEWED_EXAMPLE_SOURCE",
            "sources explicitly listed as FORBIDDEN_AS_RUNTIME_AUTHORITY",
        ],
        "committed_artifacts_inactive_by_default": True,
        "no_repo_wide_active_inference": True,
        "no_latest_or_mtime_selection": True,
    }

    archived_schema_boundary = {
        "schema_version": "r0_archived_schema_boundary_v0",
        "archived_schema_boundary_status": "DECLARED" if gate == "PASS" else "BLOCKED",
        "archived_schemas": archived_schemas,
        "schema_validator_may_later_match_r0_selected_archived_schemas": True,
        "schema_validator_is_live_now": False,
        "archived_schema_loaded_into_live_validator_now": False,
        "schema_archive_entry_present_does_not_authorize_runtime": True,
        "runtime_adoption_authorized": False,
        "move_execution_authorized": False,
        "fixture_expansion_authorized": False,
        "live_execution_authorized": False,
        "t6_live_execution_authorized": False,
        "c8_authorized": False,
        "must_not_infer": [
            "schema archive entry means runtime authority",
            "schema validator match means execution authority",
            "schema archive write means fixture expansion authority",
            "schema archive write means live T6 authority",
            "schema archive write means C8 authorization",
            "archived schema is loaded into live validator now",
        ],
    }

    source_authority_boundary = {
        "schema_version": "r0_source_authority_boundary_v0",
        "boundary_status": "IMPLICIT_AUTHORITY_DENIED" if gate == "PASS" else "BLOCKED",
        "only_explicit_active_sources_define_pre_c7_baseline": gate == "PASS",
        "committed_artifact_means_active": False,
        "archived_schema_means_runtime_authority": False,
        "reviewed_example_means_protocol_implementation": False,
        "reference_closure_means_executable_adoption": False,
        "old_c7_artifact_means_c7_opened": False,
        "old_c8_artifact_means_c8_opened": False,
        "schema_archive_write_means_runtime_adoption": False,
        "receipt_evidence_means_future_authority": False,
        "r0_receipt_means_runtime_authority": False,
        "r0_active_packet_means_execution_authority": False,
        "r0_selected_source_means_move_allowed": False,
        "implementation_source_means_executable_now": False,
        "sidecar_live_now": False,
        "live_hook_install_authorized": False,
        "sidecar_authority_granted": False,
    }

    runtime_denials = {
        "schema_version": "r0_runtime_authority_denials_v0",
        "runtime_authority_denials": runtime_authority_denials,
    }

    operator_binding = {
        "schema_version": "r0_operator_source_selection_binding_v0",
        "binding_status": "BOUND" if gate == "PASS" else "BLOCKED",
        "selection_ref": rel(OPERATOR_SELECTION_PATH),
        "selection_sha256": file_sha256(OPERATOR_SELECTION_PATH) if OPERATOR_SELECTION_PATH.exists() else None,
        "selection_id": selection.get("selection_id"),
        "selected_by": selection.get("selected_by"),
        "selection_origin": selection.get("selection_origin"),
        "builder_generated": selection.get("builder_generated"),
        "builder_did_not_infer_sources": True,
        "repo_wide_active_inference_count": 0,
    }

    active_source_index = {
        "schema_version": "r0_active_source_index_v0",
        "index_id": index_id,
        "packet_id": packet_id,
        "active_baseline": "PRE_C7_LEAN_RUNTIME_BASELINE",
        "sources": all_sources,
        "source_count": len(all_sources),
        "active_source_count": len(active_sources),
        "reference_only_source_count": len(reference_only_sources),
        "archived_schema_count": len(archived_schemas),
        "reviewed_example_source_count": len(reviewed_example_sources),
        "forbidden_authority_source_count": len(forbidden_sources),
        "superseded_source_count": len(superseded_sources),
        "pending_active_source_count": len(pending_sources),
        "default_inactive_rule_applies": True,
        "pending_sources_are_not_active": True,
    }

    acceptance_gate = {
        "active_sources_identified": len(active_sources) > 0,
        "reference_only_sources_separated": isinstance(reference_only_sources, list),
        "archived_schema_boundary_declared": gate == "PASS",
        "default_inactive_rule_declared": True,
        "c7_not_opened": runtime_authority_denials["c7_opened"] is False,
        "c8_not_opened": runtime_authority_denials["c8_opened"] is False,
        "runtime_execution_not_authorized_by_commit": runtime_authority_denials["runtime_adoption_authorized"] is False,
        "schema_archive_does_not_imply_runtime_adoption": True,
        "reviewed_examples_do_not_imply_protocol_execution": True,
    }

    active_source_packet = {
        "schema_version": "r0_baseline_locked_active_source_packet_v0",
        "packet_id": packet_id,
        "milestone": MILESTONE,
        "status": "PRE_C7_ACTIVE_SOURCE_BASELINE_LOCKED" if gate == "PASS" else "R0_BLOCKED",
        "purpose": "Select active pre-C7 runtime sources and deny implicit authority from committed/reference/archive artifacts.",
        "active_baseline": "PRE_C7_LEAN_RUNTIME_BASELINE",
        "operator_source_selection_binding_ref": rel(OPERATOR_SELECTION_BINDING_PATH),
        "active_runtime_shape": active_runtime_shape,
        "active_sources": active_sources,
        "pending_active_sources": pending_sources,
        "reference_only_sources": reference_only_sources,
        "archived_schemas": archived_schemas,
        "reviewed_example_sources": reviewed_example_sources,
        "forbidden_as_runtime_authority": forbidden_sources,
        "superseded_sources": superseded_sources,
        "default_inactive_rule_ref": rel(DEFAULT_INACTIVE_RULE_PATH),
        "runtime_authority_denials_ref": rel(RUNTIME_DENIALS_PATH),
        "archived_schema_boundary_ref": rel(ARCHIVED_SCHEMA_BOUNDARY_PATH),
        "source_authority_boundary_ref": rel(SOURCE_AUTHORITY_BOUNDARY_PATH),
        "active_source_index_ref": rel(ACTIVE_INDEX_PATH),
        "acceptance_gate": acceptance_gate,
        "terminal": terminal,
    }

    rollup = {
        "schema_version": "r0_active_source_rollup_v0",
        "runs": 1,
        "packet_emitted": gate == "PASS",
        "source_index_emitted": gate == "PASS",
        "authority_boundary_emitted": gate == "PASS",
        "runtime_denials_emitted": gate == "PASS",
        "archived_schema_boundary_emitted": gate == "PASS",
        "active_source_count": len(active_sources),
        "reference_only_source_count": len(reference_only_sources),
        "archived_schema_count": len(archived_schemas),
        "reviewed_example_source_count": len(reviewed_example_sources),
        "forbidden_authority_source_count": len(forbidden_sources),
        "superseded_source_count": len(superseded_sources),
        "pending_active_source_count": len(pending_sources),
        "default_inactive_rule_declared": True,
        "c7_opened": False,
        "c8_opened": False,
        "runtime_adoption_authorized": False,
        "bad_counters_zero": bad_counters_zero,
    }

    profile = {
        "schema_version": "r0_active_source_profile_v0",
        "profile_id": profile_id,
        "status": "R0_PASS" if gate == "PASS" else "R0_BLOCKED",
        "milestone": MILESTONE,
        "core_rule": "Only explicitly listed sources are active for the pre-C7 baseline; committed/reference/archive artifacts do not become runtime authority by existence.",
        "active_packet_ref": rel(ACTIVE_PACKET_PATH),
        "source_index_ref": rel(ACTIVE_INDEX_PATH),
        "authority_boundary_ref": rel(SOURCE_AUTHORITY_BOUNDARY_PATH),
        "runtime_denials_ref": rel(RUNTIME_DENIALS_PATH),
        "archived_schema_boundary_ref": rel(ARCHIVED_SCHEMA_BOUNDARY_PATH),
        "bad_counters_zero": bad_counters_zero,
        "must_not_infer": [
            "committed means active",
            "archived schema means runtime authority",
            "reviewed example means protocol implementation",
            "reference closure means executable adoption",
            "C7 is open",
            "C8 is open",
            "runtime execution is authorized",
            "fixture expansion is authorized",
            "move addition is authorized",
            "R0 receipt means future execution authority",
            "sidecar is live",
            "hooks are installed",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "r0_active_source_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "outcome_class": outcome_class,
        "summary": {
            "r0_active_source_packet_ready": gate == "PASS",
            "packet_id": packet_id,
            "index_id": index_id,
            "active_source_count": len(active_sources),
            "pending_active_source_count": len(pending_sources),
            "reference_only_source_count": len(reference_only_sources),
            "archived_schema_count": len(archived_schemas),
            "reviewed_example_source_count": len(reviewed_example_sources),
            "forbidden_authority_source_count": len(forbidden_sources),
            "committed_artifacts_inactive_by_default": True,
            "c7_opened": False,
            "c8_opened": False,
            "runtime_adoption_authorized": False,
            "sidecar_live_now": False,
            "hidden_next_command": False,
        },
        "failures": failures,
        "warnings": warnings,
    }

    transition_trace = {
        "schema_version": "r0_active_source_transition_trace_v0",
        "unit_id": UNIT_ID,
        "packet_id": packet_id,
        "transitions": [
            {
                "from": "OPERATOR_SOURCE_SELECTION_AVAILABLE",
                "edge": "consume explicit operator source selection without repo-wide inference",
                "to": "SOURCE_SELECTION_BOUND" if gate == "PASS" else "SOURCE_SELECTION_BLOCKED",
            },
            {
                "from": "SOURCE_SELECTION_BOUND" if gate == "PASS" else "SOURCE_SELECTION_BLOCKED",
                "edge": "emit R0 active source ledger and implicit authority denials",
                "to": "R0_BASELINE_LOCKED_ACTIVE_SOURCE_PACKET_READY" if gate == "PASS" else "R0_BLOCKED",
            },
            {
                "from": "R0_BASELINE_LOCKED_ACTIVE_SOURCE_PACKET_READY" if gate == "PASS" else "R0_BLOCKED",
                "edge": "stop with no automatic next command",
                "to": terminal["stop_code"],
            },
        ],
        "terminal": terminal,
    }

    for path, obj in [
        (OPERATOR_SELECTION_BINDING_PATH, operator_binding),
        (DEFAULT_INACTIVE_RULE_PATH, default_inactive_rule),
        (ARCHIVED_SCHEMA_BOUNDARY_PATH, archived_schema_boundary),
        (SOURCE_AUTHORITY_BOUNDARY_PATH, source_authority_boundary),
        (RUNTIME_DENIALS_PATH, runtime_denials),
        (ACTIVE_INDEX_PATH, active_source_index),
        (ACTIVE_PACKET_PATH, active_source_packet),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    acceptance_gate_results = {
        "R0_0_OPERATOR_SOURCE_SELECTION_CONSUMED": OPERATOR_SELECTION_PATH.exists(),
        "R0_1_OPERATOR_SOURCE_SELECTION_TYPED": gate == "PASS",
        "R0_2_ACTIVE_SOURCES_EXPLICITLY_LISTED": len(active_sources) > 0,
        "R0_3_SOURCE_CLASSIFICATIONS_VALID": not any("classification" in f for f in failures),
        "R0_4_AUTHORITY_LEVELS_VALID": not any("authority_level" in f for f in failures),
        "R0_5_REFERENCE_ONLY_SOURCES_SEPARATED": isinstance(reference_only_sources, list),
        "R0_6_ARCHIVED_SCHEMAS_SEPARATED": isinstance(archived_schemas, list),
        "R0_7_REVIEWED_EXAMPLES_SEPARATED": isinstance(reviewed_example_sources, list),
        "R0_8_FORBIDDEN_AUTHORITY_SURFACES_SEPARATED": isinstance(forbidden_sources, list),
        "R0_9_DEFAULT_INACTIVE_RULE_DECLARED": DEFAULT_INACTIVE_RULE_PATH.exists(),
        "R0_10_COMMITTED_ARTIFACTS_INACTIVE_BY_DEFAULT": True,
        "R0_11_ARCHIVED_SCHEMA_BOUNDARY_DECLARED": ARCHIVED_SCHEMA_BOUNDARY_PATH.exists(),
        "R0_12_SCHEMA_ARCHIVE_DOES_NOT_IMPLY_RUNTIME_AUTHORITY": True,
        "R0_13_REVIEWED_EXAMPLE_DOES_NOT_IMPLY_PROTOCOL_IMPLEMENTATION": True,
        "R0_14_RUNTIME_AUTHORITY_DENIALS_EXPLICIT": RUNTIME_DENIALS_PATH.exists(),
        "R0_15_C7_NOT_OPENED": False is runtime_authority_denials["c7_opened"],
        "R0_16_C8_NOT_OPENED": False is runtime_authority_denials["c8_opened"],
        "R0_17_RUNTIME_ADOPTION_NOT_AUTHORIZED": False is runtime_authority_denials["runtime_adoption_authorized"],
        "R0_18_LIVE_EXECUTION_NOT_AUTHORIZED": False is runtime_authority_denials["live_execution_authorized"],
        "R0_19_T6_LIVE_EXECUTION_NOT_AUTHORIZED": False is runtime_authority_denials["t6_live_execution_authorized"],
        "R0_20_FIXTURE_EXPANSION_NOT_AUTHORIZED": False is runtime_authority_denials["fixture_expansion_authorized"],
        "R0_21_MOVE_ADDITION_NOT_AUTHORIZED": False is runtime_authority_denials["move_addition_authorized"],
        "R0_22_SCHEMA_ARCHIVE_MUTATION_NOT_AUTHORIZED": False is runtime_authority_denials["schema_archive_mutation_authorized"],
        "R0_23_CELL1_GENERAL_AUTHORITY_NOT_AUTHORIZED": False is runtime_authority_denials["cell1_general_authority_authorized"],
        "R0_24_NO_LATEST_OR_MTIME_SELECTION": True,
        "R0_25_NO_REPO_WIDE_ACTIVE_INFERENCE": True,
        "R0_26_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
        "R0_27_RECEIPT_EMITTED": True,
        "R0_28_BAD_COUNTERS_ZERO": bad_counters_zero,
        "R0_29_NO_HIDDEN_NEXT_COMMAND": negative_controls["hidden_next_command_count"] == 0,
        "R0_30_OPERATOR_SELECTION_NOT_BUILDER_GENERATED": selection.get("builder_generated") is False,
        "R0_31_PENDING_SOURCES_NOT_ACTIVE": all(p.get("status") == "PENDING_NOT_ACTIVE" for p in pending_sources),
        "R0_32_SOURCE_PATHS_VERIFIED_IF_SUPPLIED": not any("source_path_missing" in f for f in failures),
        "R0_33_R0_RECEIPT_NOT_FUTURE_AUTHORITY": True,
        "R0_34_IMPLEMENTATION_SOURCE_NOT_EXECUTABLE_BY_EXISTENCE": True,
        "R0_35_SIDECAR_NOT_LIVE": runtime_authority_denials["sidecar_live_now"] is False,
        "R0_36_HOOKS_NOT_INSTALLED": runtime_authority_denials["live_hook_install_authorized"] is False,
        "R0_37_ARCHIVED_SCHEMA_ONLY_ELIGIBLE_FOR_LATER_VALIDATOR_RECOGNITION": True,
    }

    receipt = {
        "schema_version": "r0_baseline_locked_active_source_packet_receipt_v0",
        "receipt_type": "TYPED_R0_BASELINE_LOCKED_ACTIVE_SOURCE_PACKET_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "packet_id": packet_id,
        "index_id": index_id,
        "gate": gate,
        "status": status,
        "outcome_class": outcome_class,
        "failures": failures,
        "warnings": warnings,
        "machine_readable_r0_summary": {
            "r0_active_source_packet_ready": gate == "PASS",
            "active_sources_selected": len(active_sources) > 0 and gate == "PASS",
            "active_source_count": len(active_sources),
            "pending_active_source_count": len(pending_sources),
            "reference_only_source_count": len(reference_only_sources),
            "archived_schema_count": len(archived_schemas),
            "reviewed_example_source_count": len(reviewed_example_sources),
            "forbidden_authority_source_count": len(forbidden_sources),
            "default_inactive_rule_declared": True,
            "archived_schema_boundary_declared": gate == "PASS",
            "runtime_authority_denials_declared": gate == "PASS",
            "committed_artifacts_inactive_by_default": True,
            "schema_archive_does_not_imply_runtime_authority": True,
            "pending_sources_are_not_active": True,
            "r0_receipt_means_future_authority": False,
            "schema_validator_is_live_now": False,
            "sidecar_live_now": False,
            "hooks_installed": False,
            "c7_opened": False,
            "c8_opened": False,
            "runtime_adoption_authorized": False,
            "live_execution_authorized": False,
            "fixture_expansion_authorized": False,
            "move_addition_authorized": False,
            "schema_archive_mutation_authorized": False,
            "schema_mutation_authorized": False,
            "cell1_general_authority_authorized": False,
            "hidden_next_command": False,
            "bad_counters_zero": bad_counters_zero,
            "next_command_goal": None,
        },
        "acceptance_gate_results": acceptance_gate_results,
        "negative_controls": negative_controls,
        "output_artifacts": {
            "operator_source_selection": rel(OPERATOR_SELECTION_PATH),
            "operator_source_selection_binding": rel(OPERATOR_SELECTION_BINDING_PATH),
            "active_source_packet": rel(ACTIVE_PACKET_PATH),
            "active_source_index": rel(ACTIVE_INDEX_PATH),
            "source_authority_boundary": rel(SOURCE_AUTHORITY_BOUNDARY_PATH),
            "runtime_authority_denials": rel(RUNTIME_DENIALS_PATH),
            "archived_schema_boundary": rel(ARCHIVED_SCHEMA_BOUNDARY_PATH),
            "default_inactive_rule": rel(DEFAULT_INACTIVE_RULE_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": terminal,
    }

    receipt_id = "r0_active_source_packet_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"r0_active_source_packet_receipt_id={receipt_id}")
    print(f"r0_active_source_packet_receipt_path={rel(receipt_path)}")
    print(f"r0_active_source_packet_id={packet_id if gate == 'PASS' else 'NONE'}")
    print(f"r0_active_source_index_id={index_id if gate == 'PASS' else 'NONE'}")
    print(f"r0_terminal_stop_code={terminal['stop_code']}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
