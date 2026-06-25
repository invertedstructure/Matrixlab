#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "observation.decision_edge_observability_surface_closure.v0"
LAYER = "OBSERVATION_HARDENING / DECISION_EDGE_VISIBILITY / CLOSURE"
MODE = "CLOSE / FREEZE_REVIEWED_REFERENCE / O2_DESIGN_READY"
BUILD_MODE = "O1_SURFACE_CLOSURE_ONLY"

O1_REVIEW_RECEIPT_ID = "24c72b48"
O1_REVIEW_RECEIPT_PATH = ROOT / "data/o1_decision_edge_observability_surface_review_v0_receipts/24c72b48.json"
O1_REVIEW_ASSESSMENT_PATH = ROOT / "data/o1_decision_edge_observability_surface_review_v0/o1_decision_edge_observability_surface_review_assessment_v0.json"
O1_OBS_RECORD_REVIEW_PATH = ROOT / "data/o1_decision_edge_observability_surface_review_v0/o1_observation_record_integrity_review_v0.json"
O1_HANDLE_REVIEW_PATH = ROOT / "data/o1_decision_edge_observability_surface_review_v0/o1_candidate_handle_provisionality_review_v0.json"
O1_ROLLUP_PROFILE_READOUT_REVIEW_PATH = ROOT / "data/o1_decision_edge_observability_surface_review_v0/o1_rollup_profile_readout_review_v0.json"
O1_SOURCE_SURFACE_REVIEW_PATH = ROOT / "data/o1_decision_edge_observability_surface_review_v0/o1_source_surface_review_v0.json"
O1_NONAUTHORITY_SAFETY_REVIEW_PATH = ROOT / "data/o1_decision_edge_observability_surface_review_v0/o1_nonauthority_safety_review_v0.json"
O1_CLOSURE_CANDIDATE_PATH = ROOT / "data/o1_decision_edge_observability_surface_review_v0/o1_decision_edge_observability_surface_closure_candidate_v0.json"
O1_REVIEW_DOWNSTREAM_TABLE_PATH = ROOT / "data/o1_decision_edge_observability_surface_review_v0/o1_surface_review_downstream_decision_table_v0.json"
O1_REVIEW_CLASSIFICATION_PATH = ROOT / "data/o1_decision_edge_observability_surface_review_v0/o1_surface_review_classification_v0.json"
O1_REVIEW_AUTHORITY_PATH = ROOT / "data/o1_decision_edge_observability_surface_review_v0/o1_surface_review_authority_boundary_v0.json"
O1_REVIEW_ROLLUP_PATH = ROOT / "data/o1_decision_edge_observability_surface_review_v0/o1_surface_review_rollup_v0.json"
O1_REVIEW_PROFILE_PATH = ROOT / "data/o1_decision_edge_observability_surface_review_v0/o1_surface_review_profile_v0.json"
O1_REVIEW_REPORT_PATH = ROOT / "data/o1_decision_edge_observability_surface_review_v0/o1_surface_review_report.json"
O1_REVIEW_TRACE_PATH = ROOT / "data/o1_decision_edge_observability_surface_review_v0/o1_surface_review_transition_trace.json"

O1_SURFACE_RECEIPT_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0_receipts/9048434d.json"
O1_SURFACE_RECORDS_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/decision_edge_observation_records_v0.jsonl"
O1_SURFACE_ROLLUP_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/decision_edge_observation_rollup_v0.json"
O1_SURFACE_PROFILE_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/decision_edge_observation_profile_v0.json"
O1_SURFACE_READOUT_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/decision_edge_observation_readout_v0.json"
O1_SURFACE_SOURCE_SURFACE_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/o1_source_surface_v0.json"

REQUIRED_SOURCE_FILES = [
    O1_REVIEW_RECEIPT_PATH,
    O1_REVIEW_ASSESSMENT_PATH,
    O1_OBS_RECORD_REVIEW_PATH,
    O1_HANDLE_REVIEW_PATH,
    O1_ROLLUP_PROFILE_READOUT_REVIEW_PATH,
    O1_SOURCE_SURFACE_REVIEW_PATH,
    O1_NONAUTHORITY_SAFETY_REVIEW_PATH,
    O1_CLOSURE_CANDIDATE_PATH,
    O1_REVIEW_DOWNSTREAM_TABLE_PATH,
    O1_REVIEW_CLASSIFICATION_PATH,
    O1_REVIEW_AUTHORITY_PATH,
    O1_REVIEW_ROLLUP_PATH,
    O1_REVIEW_PROFILE_PATH,
    O1_REVIEW_REPORT_PATH,
    O1_REVIEW_TRACE_PATH,
    O1_SURFACE_RECEIPT_PATH,
    O1_SURFACE_RECORDS_PATH,
    O1_SURFACE_ROLLUP_PATH,
    O1_SURFACE_PROFILE_PATH,
    O1_SURFACE_READOUT_PATH,
    O1_SURFACE_SOURCE_SURFACE_PATH,
]

OUT_DIR = ROOT / "data/o1_decision_edge_observability_surface_closure_v0"
RECEIPT_DIR = ROOT / "data/o1_decision_edge_observability_surface_closure_v0_receipts"

CLOSURE_RECORD_PATH = OUT_DIR / "o1_decision_edge_observability_surface_closure_record_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "o1_decision_edge_observability_surface_reviewed_reference_v0.json"
REFERENCE_FREEZE_PATH = OUT_DIR / "o1_decision_edge_observability_surface_reference_freeze_v0.json"
RECEIPT_CHAIN_PATH = OUT_DIR / "o1_decision_edge_observability_surface_receipt_chain_v0.json"
BOUNDARY_LOCK_PATH = OUT_DIR / "o1_decision_edge_observability_surface_boundary_lock_v0.json"
O2_DESIGN_READY_SURFACE_PATH = OUT_DIR / "o1_post_closure_o2_design_ready_surface_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "o1_surface_closure_downstream_decision_table_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o1_surface_closure_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o1_surface_closure_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "o1_surface_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o1_surface_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "o1_surface_closure_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "o1_surface_closure_transition_trace.json"

EXPECTED_REVIEW_STATUS = "TYPED_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_REVIEWED_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_STOP = "STOP_TYPED_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_REVIEWED_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_NEXT = "CLOSE_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_AS_REVIEWED_REFERENCE_V0"

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

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    review_receipt = read_json(O1_REVIEW_RECEIPT_PATH)
    review_summary = review_receipt.get("machine_readable_o1_surface_review_summary", {})
    assessment = read_json(O1_REVIEW_ASSESSMENT_PATH)
    obs_review = read_json(O1_OBS_RECORD_REVIEW_PATH)
    handle_review = read_json(O1_HANDLE_REVIEW_PATH)
    rpr_review = read_json(O1_ROLLUP_PROFILE_READOUT_REVIEW_PATH)
    source_review = read_json(O1_SOURCE_SURFACE_REVIEW_PATH)
    safety_review = read_json(O1_NONAUTHORITY_SAFETY_REVIEW_PATH)
    closure_candidate = read_json(O1_CLOSURE_CANDIDATE_PATH)
    review_rollup = read_json(O1_REVIEW_ROLLUP_PATH)
    review_profile = read_json(O1_REVIEW_PROFILE_PATH)
    surface_receipt = read_json(O1_SURFACE_RECEIPT_PATH)
    obs_records = read_jsonl(O1_SURFACE_RECORDS_PATH)
    surface_rollup = read_json(O1_SURFACE_ROLLUP_PATH)
    surface_readout = read_json(O1_SURFACE_READOUT_PATH)

    if review_receipt.get("receipt_id") != O1_REVIEW_RECEIPT_ID or review_receipt.get("gate") != "PASS":
        failures.append("o1_review_receipt_not_pass")
    if review_receipt.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("o1_review_terminal_not_expected")
    if review_summary.get("status") != EXPECTED_REVIEW_STATUS:
        failures.append(f"o1_review_status_not_expected:{review_summary.get('status')}")
    if review_summary.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append(f"o1_review_next_not_expected:{review_summary.get('recommended_next')}")
    if review_summary.get("recommended_after_closure") != "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET_V0":
        failures.append("recommended_after_closure_not_o2_design")

    for key in [
        "o1_surface_review_complete",
        "o1_surface_review_pass",
        "candidate_handles_remain_provisional",
        "observation_record_integrity_pass",
        "rollup_profile_readout_coherent",
        "source_surface_explicit_refs_only",
        "nonauthority_safety_review_pass",
        "closure_candidate_ready",
        "bad_counters_zero",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"review_summary_required_true_missing:{key}")

    for key in [
        "graph_schema_claimed",
        "graph_tracker_created",
        "architecture_change",
        "source_receipt_mutated",
        "authority_expansion",
        "target_selected_for_build",
        "runtime_patch_applied",
        "c5_opened",
        "command_emitted",
        "unit_feedback_hardening_executed",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if review_summary.get(key) is not False:
            failures.append(f"review_summary_forbidden_true:{key}")

    expected_counts = {
        "observations_reviewed": 8,
        "source_receipt_count": 5,
        "candidate_handle_count": 13,
    }
    for key, expected in expected_counts.items():
        if review_summary.get(key) != expected:
            failures.append(f"review_summary_count_wrong:{key}:{review_summary.get(key)}")

    if assessment.get("closure_candidate_ready") is not True:
        failures.append("assessment_closure_candidate_not_ready")
    if obs_review.get("review_status") != "OBSERVATION_RECORD_INTEGRITY_PASS":
        failures.append("observation_record_review_not_pass")
    if handle_review.get("review_status") != "CANDIDATE_HANDLES_PROVISIONALITY_PASS":
        failures.append("handle_review_not_pass")
    if rpr_review.get("review_status") != "ROLLUP_PROFILE_READOUT_COHERENT":
        failures.append("rollup_profile_readout_review_not_coherent")
    if source_review.get("review_status") != "SOURCE_SURFACE_EXPLICIT_REFS_ONLY_PASS":
        failures.append("source_surface_review_not_pass")
    if safety_review.get("review_status") != "NONAUTHORITY_SAFETY_REVIEW_PASS":
        failures.append("safety_review_not_pass")
    if closure_candidate.get("closure_candidate_status") != "O1_SURFACE_CLOSURE_CANDIDATE_READY":
        failures.append("closure_candidate_not_ready")
    if closure_candidate.get("recommended_after_closure") != "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET_V0":
        failures.append("closure_candidate_after_not_o2_design")
    if review_rollup.get("closure_candidate_count") != 1:
        failures.append("review_rollup_closure_count_wrong")
    if review_profile.get("closure_candidate_ready") is not True:
        failures.append("review_profile_closure_not_ready")
    if surface_receipt.get("receipt_id") != "9048434d":
        failures.append("surface_receipt_wrong")
    if len(obs_records) != 8:
        failures.append(f"obs_records_count_wrong:{len(obs_records)}")
    if surface_rollup.get("total_observations") != 8:
        failures.append("surface_rollup_observation_count_wrong")
    if surface_readout.get("bad_counters_zero") is not True:
        failures.append("surface_readout_bad_counters_not_zero")

    return failures, {
        "review_summary": review_summary,
        "obs_records": obs_records,
        "surface_rollup": surface_rollup,
        "surface_readout": surface_readout,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    review_summary = src.get("review_summary", {})
    obs_records = src.get("obs_records", [])
    surface_rollup = src.get("surface_rollup", {})
    surface_readout = src.get("surface_readout", {})

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    if failures:
        status = "TYPED_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_CLOSURE_BASIS_FAIL"
        closed = False
        reason_codes = failures
        recommended_next = "REPAIR_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_CLOSURE_V0"
    else:
        status = "TYPED_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_CLOSED_AS_REVIEWED_REFERENCE_O2_DESIGN_READY"
        closed = True
        reason_codes = [
            "O1_SURFACE_CLOSED_AS_REVIEWED_REFERENCE",
            "O1_SURFACE_REVIEW_RECEIPT_CONSUMED",
            "EIGHT_OBSERVATION_SIDECARS_FROZEN_AS_REVIEWED_REFERENCE",
            "FIVE_SOURCE_RECEIPTS_FROZEN_IN_SOURCE_SURFACE",
            "THIRTEEN_CANDIDATE_HANDLES_FROZEN_AS_PROVISIONAL_REFERENCE",
            "ROLLUP_PROFILE_READOUT_FROZEN",
            "NONAUTHORITY_BOUNDARY_LOCKED",
            "O2_UNIT_FEEDBACK_HARDENING_DESIGN_READY",
            "NO_O2_EXECUTED",
            "NO_GRAPH_SCHEMA_CLAIMED",
            "NO_GRAPH_TRACKER_CREATED",
            "NO_ARCHITECTURE_CHANGE",
            "NO_SOURCE_RECEIPT_MUTATION",
            "NO_AUTHORITY_EXPANSION",
            "NO_TARGET_SELECTED_FOR_BUILD",
            "NO_RUNTIME_PATCH_APPLIED",
            "NO_C5_OPENED",
        ]
        recommended_next = "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET_V0"

    closure_record = {
        "schema_version": "o1_decision_edge_observability_surface_closure_record_v0",
        "closure_status": "CLOSED_AS_REVIEWED_REFERENCE" if closed else "CLOSURE_NOT_RECORDED",
        "source_review_receipt_id": O1_REVIEW_RECEIPT_ID,
        "closed_object": "o1_decision_edge_observability_surface_v0",
        "closure_basis": {
            "o1_surface_review_pass": closed,
            "observations_reviewed": len(obs_records),
            "source_receipt_count": review_summary.get("source_receipt_count"),
            "candidate_handle_count": review_summary.get("candidate_handle_count"),
            "closure_candidate_ready": review_summary.get("closure_candidate_ready"),
        },
        "closure_meaning": "O1 sidecar decision-edge observations are reviewed and frozen as an observability reference.",
        "closure_does_not_mean": [
            "decision graph built",
            "graph schema extracted",
            "candidate handles finalized",
            "authority expanded",
            "target selected for build",
            "runtime patched",
            "C5 opened",
            "O2 executed",
        ],
    }

    reviewed_reference = {
        "schema_version": "o1_decision_edge_observability_surface_reviewed_reference_v0",
        "reference_status": "FROZEN_REVIEWED_REFERENCE" if closed else "REFERENCE_NOT_FROZEN",
        "reference_object_id": "o1_decision_edge_observability_surface_reviewed_reference_" + sha8({
            "source_review_receipt_id": O1_REVIEW_RECEIPT_ID,
            "observations": len(obs_records),
            "source_receipt_count": review_summary.get("source_receipt_count"),
            "candidate_handle_count": review_summary.get("candidate_handle_count"),
        }),
        "source_review_receipt_id": O1_REVIEW_RECEIPT_ID,
        "source_surface_receipt_id": "9048434d",
        "source_design_receipt_id": "c9ef517f",
        "observations_frozen": len(obs_records),
        "source_receipt_count": review_summary.get("source_receipt_count"),
        "candidate_handle_count": review_summary.get("candidate_handle_count"),
        "reference_use": "future units may cite this reviewed O1 surface to inspect receipt-side decision-edge observations",
        "reference_not_authority_for": [
            "graph schema extraction",
            "candidate handle finalization",
            "runtime patching",
            "C5 opening",
            "O2 completion",
            "target selection",
            "authority expansion",
        ],
    }

    reference_freeze = {
        "schema_version": "o1_decision_edge_observability_surface_reference_freeze_v0",
        "freeze_status": "FREEZE_COMPLETE" if closed else "FREEZE_NOT_COMPLETE",
        "frozen_reference_path": rel(REVIEWED_REFERENCE_PATH),
        "frozen_receipt_chain_path": rel(RECEIPT_CHAIN_PATH),
        "may_mutate_prior_artifacts": False,
        "may_reopen_without_explicit_new_objective": False,
        "may_treat_as_graph_schema": False,
        "may_treat_candidate_handles_as_final": False,
    }

    receipt_chain = {
        "schema_version": "o1_decision_edge_observability_surface_receipt_chain_v0",
        "chain_status": "RECEIPT_CHAIN_PRESERVED",
        "receipts": [
            {"stage": "o1_target_design", "receipt_id": "c9ef517f"},
            {"stage": "o1_surface_build", "receipt_id": "9048434d"},
            {"stage": "o1_surface_review", "receipt_id": O1_REVIEW_RECEIPT_ID},
        ],
        "closure_receipt_pending": True,
    }

    boundary_lock = {
        "schema_version": "o1_decision_edge_observability_surface_boundary_lock_v0",
        "boundary_lock_status": "BOUNDARIES_LOCKED_AT_CLOSURE",
        "o1_surface_closed": closed,
        "collection_status": "OBSERVATION_ONLY",
        "schema_claim": "NONE",
        "candidate_handles_provisional": True,
        "graph_schema_claimed": False,
        "graph_tracker_created": False,
        "architecture_change": False,
        "source_receipt_mutated": False,
        "authority_expansion": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "c5_opened": False,
        "command_emitted": False,
        "unit_feedback_hardening_executed": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
    }

    o2_ready_surface = {
        "schema_version": "o1_post_closure_o2_design_ready_surface_v0",
        "surface_status": "O2_DESIGN_READY_AFTER_O1_CLOSURE" if closed else "O2_DESIGN_NOT_READY",
        "authorized_next_unit": "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET_V0" if closed else None,
        "authorization_scope": "design the O2 unit feedback hardening target only",
        "authorization_does_not_allow": [
            "execute O2 feedback hardening",
            "mutate O1",
            "extract graph schema",
            "create graph tracker",
            "select runtime target",
            "patch runtime",
            "open C5",
            "expand authority",
        ],
    }

    downstream_decision_table = {
        "schema_version": "o1_surface_closure_downstream_decision_table_v0",
        "decision_status": "O1_SURFACE_CLOSURE_DOWNSTREAM_TABLE_EMITTED",
        "records": [
            {
                "decision": "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET",
                "selected": closed,
                "next_unit": "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET_V0" if closed else None,
                "why": "O1 is closed as reviewed observability reference; O2 target design is the next cheap high-value hardening step.",
            },
            {
                "decision": "EXECUTE_UNIT_FEEDBACK_HARDENING_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Only O2 design is authorized next; execution requires its own target design and build unit.",
            },
            {
                "decision": "EXTRACT_GRAPH_SCHEMA_NOW",
                "selected": False,
                "next_unit": None,
                "why": "O1 closure preserves observability reference only, not graph schema authority.",
            },
        ],
    }

    classification = {
        "schema_version": "o1_surface_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "o1_surface_closed": closed,
        "closed_as_reviewed_reference": closed,
        "reviewed_reference_emitted": closed,
        "observations_frozen": len(obs_records),
        "source_receipt_count": review_summary.get("source_receipt_count"),
        "candidate_handle_count": review_summary.get("candidate_handle_count"),
        "candidate_handles_remain_provisional": True,
        "o2_design_ready": closed,
        "o2_executed": False,
        "recommended_next": recommended_next,
        "collection_status": "OBSERVATION_ONLY",
        "schema_claim": "NONE",
        "graph_schema_claimed": False,
        "graph_tracker_created": False,
        "architecture_change": False,
        "source_receipt_mutated": False,
        "authority_expansion": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "c5_opened": False,
        "command_emitted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "next_command_goal": None,
    }

    authority_boundary = {
        "schema_version": "o1_surface_closure_authority_boundary_v0",
        "status": status,
        "may_design_o2_target_next": closed,
        "may_execute_o2_now": False,
        "may_extract_graph_schema": False,
        "may_create_graph_tracker": False,
        "may_promote_candidate_handles_to_final_primitives": False,
        "may_mutate_source_receipts": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "may_select_target_for_build": False,
        "may_patch_runtime": False,
        "may_open_c5": False,
        "may_expand_authority": False,
    }

    rollup = {
        "schema_version": "o1_surface_closure_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "o1_surface_closed_count": 1 if closed else 0,
        "reviewed_reference_emitted_count": 1 if closed else 0,
        "observations_frozen_count": len(obs_records),
        "source_receipt_count": review_summary.get("source_receipt_count"),
        "candidate_handle_count": review_summary.get("candidate_handle_count"),
        "o2_design_ready_count": 1 if closed else 0,
        "o2_executed_count": 0,
        "graph_schema_claim_count": 0,
        "graph_tracker_created_count": 0,
        "architecture_change_count": 0,
        "source_receipt_mutation_count": 0,
        "authority_expansion_count": 0,
        "target_selected_for_build_count": 0,
        "runtime_patch_count": 0,
        "c5_opened_count": 0,
        "command_emitted_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    zero_keys = [
        "o2_executed_count",
        "graph_schema_claim_count",
        "graph_tracker_created_count",
        "architecture_change_count",
        "source_receipt_mutation_count",
        "authority_expansion_count",
        "target_selected_for_build_count",
        "runtime_patch_count",
        "c5_opened_count",
        "command_emitted_count",
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "o1_surface_closure_profile_v0",
        "profile_id": "o1_surface_closure_profile_" + sha8(rollup),
        "status": status,
        "o1_surface_closed": closed,
        "closed_as_reviewed_reference": closed,
        "observations_frozen": len(obs_records),
        "candidate_handles_remain_provisional": True,
        "o2_design_ready": closed,
        "o2_executed": False,
        "recommendation": "Proceed to O2 target design: unit feedback hardening. Do not execute O2 until its target design is accepted.",
        "graph_schema_claimed": False,
        "graph_tracker_created": False,
        "architecture_change": False,
        "authority_expansion": False,
        "runtime_patch_applied": False,
        "c5_opened": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o1_surface_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "O1 was closed as a reviewed observability reference. Eight reviewed decision-edge sidecars, five explicit source receipts, thirteen provisional candidate handles, rollup/profile/readout, source surface, review, and receipt chain are frozen as reference context. This closure authorizes the next O2 target-design unit only. It does not execute O2, extract a graph schema, create a graph tracker, mutate sources, expand authority, select a target, patch runtime, or open C5.",
        "observations_frozen": len(obs_records),
        "source_receipt_count": review_summary.get("source_receipt_count"),
        "candidate_handle_count": review_summary.get("candidate_handle_count"),
        "recommended_next_handling": recommended_next,
        "bad_counters_zero": profile["bad_counters_zero"],
    }

    trace = {
        "schema_version": "o1_surface_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_o1_review",
                "question": "is O1 reviewed clean and close-ready",
                "answer": "yes" if closed else "no",
                "taken": "close O1 as reviewed reference",
            },
            {
                "step": "freeze_reference",
                "question": "what gets frozen",
                "answer": "8 reviewed sidecar observations, 5 source receipts, 13 provisional handles, rollup/profile/readout, and receipt chain",
                "taken": "emit reviewed reference and boundary lock",
            },
            {
                "step": "authorize_next_target_design",
                "question": "what is lawful after closure",
                "answer": recommended_next,
                "taken": "authorize O2 design target only",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    write_json(CLOSURE_RECORD_PATH, closure_record)
    write_json(REVIEWED_REFERENCE_PATH, reviewed_reference)
    write_json(REFERENCE_FREEZE_PATH, reference_freeze)
    write_json(RECEIPT_CHAIN_PATH, receipt_chain)
    write_json(BOUNDARY_LOCK_PATH, boundary_lock)
    write_json(O2_DESIGN_READY_SURFACE_PATH, o2_ready_surface)
    write_json(DOWNSTREAM_DECISION_TABLE_PATH, downstream_decision_table)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(AUTHORITY_BOUNDARY_PATH, authority_boundary)
    write_json(ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, profile)
    write_json(REPORT_PATH, report)
    write_json(TRANSITION_TRACE_PATH, trace)

    acceptance_gate_results = {
        "O1_CLOSE_0_REVIEW_RECEIPT_CONSUMED": O1_REVIEW_RECEIPT_PATH.exists(),
        "O1_CLOSE_1_CLOSURE_RECORD_EMITTED": CLOSURE_RECORD_PATH.exists(),
        "O1_CLOSE_2_REVIEWED_REFERENCE_EMITTED": REVIEWED_REFERENCE_PATH.exists(),
        "O1_CLOSE_3_REFERENCE_FREEZE_EMITTED": REFERENCE_FREEZE_PATH.exists(),
        "O1_CLOSE_4_RECEIPT_CHAIN_EMITTED": RECEIPT_CHAIN_PATH.exists(),
        "O1_CLOSE_5_BOUNDARY_LOCK_EMITTED": BOUNDARY_LOCK_PATH.exists(),
        "O1_CLOSE_6_EIGHT_OBSERVATIONS_FROZEN": len(obs_records) == 8,
        "O1_CLOSE_7_FIVE_SOURCE_RECEIPTS_FROZEN": review_summary.get("source_receipt_count") == 5,
        "O1_CLOSE_8_THIRTEEN_PROVISIONAL_HANDLES_FROZEN": review_summary.get("candidate_handle_count") == 13,
        "O1_CLOSE_9_O2_DESIGN_READY_SURFACE_EMITTED": O2_DESIGN_READY_SURFACE_PATH.exists(),
        "O1_CLOSE_10_NO_O2_EXECUTED": rollup["o2_executed_count"] == 0,
        "O1_CLOSE_11_NO_GRAPH_SCHEMA_CLAIM": rollup["graph_schema_claim_count"] == 0,
        "O1_CLOSE_12_NO_GRAPH_TRACKER": rollup["graph_tracker_created_count"] == 0,
        "O1_CLOSE_13_NO_ARCHITECTURE_CHANGE": rollup["architecture_change_count"] == 0,
        "O1_CLOSE_14_NO_SOURCE_RECEIPT_MUTATION": rollup["source_receipt_mutation_count"] == 0,
        "O1_CLOSE_15_NO_AUTHORITY_EXPANSION": rollup["authority_expansion_count"] == 0,
        "O1_CLOSE_16_NO_TARGET_SELECTED_FOR_BUILD": rollup["target_selected_for_build_count"] == 0,
        "O1_CLOSE_17_NO_RUNTIME_PATCH": rollup["runtime_patch_count"] == 0,
        "O1_CLOSE_18_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "O1_CLOSE_19_NO_COMMAND_EMITTED": rollup["command_emitted_count"] == 0,
        "O1_CLOSE_20_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "O1_CLOSE_21_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "O1_CLOSE_22_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_CLOSURE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "closed": closed,
        "observations": len(obs_records),
        "o2_design_ready": closed,
        "o2_executed": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o1_surface_closure_receipt_v0",
        "receipt_type": "TYPED_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_o1_review_receipt_id": O1_REVIEW_RECEIPT_ID,
        "machine_readable_o1_surface_closure_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "o1_surface_closed": closed,
            "closed_as_reviewed_reference": closed,
            "reviewed_reference_emitted": closed,
            "observations_frozen": len(obs_records),
            "source_receipt_count": review_summary.get("source_receipt_count"),
            "candidate_handle_count": review_summary.get("candidate_handle_count"),
            "candidate_handles_remain_provisional": True,
            "o2_design_ready": closed,
            "o2_executed": False,
            "collection_status": "OBSERVATION_ONLY",
            "schema_claim": "NONE",
            "graph_schema_claimed": False,
            "graph_tracker_created": False,
            "architecture_change": False,
            "source_receipt_mutated": False,
            "authority_expansion": False,
            "target_selected_for_build": False,
            "runtime_patch_applied": False,
            "c5_opened": False,
            "command_emitted": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": profile["bad_counters_zero"],
            "recommended_next": recommended_next,
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "closure_record": rel(CLOSURE_RECORD_PATH),
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "reference_freeze": rel(REFERENCE_FREEZE_PATH),
            "receipt_chain": rel(RECEIPT_CHAIN_PATH),
            "boundary_lock": rel(BOUNDARY_LOCK_PATH),
            "o2_design_ready_surface": rel(O2_DESIGN_READY_SURFACE_PATH),
            "downstream_decision_table": rel(DOWNSTREAM_DECISION_TABLE_PATH),
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
    print(f"o1_surface_closure_receipt_id={receipt_id}")
    print(f"o1_surface_closure_receipt_path={rel(receipt_path)}")
    print(f"o1_surface_closure_record_path={rel(CLOSURE_RECORD_PATH)}")
    print(f"o1_surface_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"o1_surface_reference_freeze_path={rel(REFERENCE_FREEZE_PATH)}")
    print(f"o1_surface_receipt_chain_path={rel(RECEIPT_CHAIN_PATH)}")
    print(f"o1_surface_boundary_lock_path={rel(BOUNDARY_LOCK_PATH)}")
    print(f"o1_o2_design_ready_surface_path={rel(O2_DESIGN_READY_SURFACE_PATH)}")
    print(f"o1_surface_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"o1_surface_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
