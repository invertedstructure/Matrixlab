#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_V0"
TARGET_UNIT_ID = "observation.decision_edge_observability_surface_review.v0"
LAYER = "OBSERVATION_HARDENING / DECISION_EDGE_VISIBILITY / SURFACE_REVIEW"
MODE = "REVIEW / VERIFY_SIDECAR_OBSERVATIONS / NO_GRAPH_NO_TRACKER"
BUILD_MODE = "O1_SURFACE_REVIEW_ONLY"

O1_SURFACE_RECEIPT_ID = "9048434d"
O1_SURFACE_RECEIPT_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0_receipts/9048434d.json"
O1_OBSERVATION_SCHEMA_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/decision_edge_observation_record_schema_v0.json"
O1_HANDLE_SCHEMA_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/decision_edge_candidate_handle_schema_v0.json"
O1_HANDLE_RECORDS_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/decision_edge_candidate_handle_records_v0.jsonl"
O1_OBSERVATION_RECORDS_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/decision_edge_observation_records_v0.jsonl"
O1_ROLLUP_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/decision_edge_observation_rollup_v0.json"
O1_PROFILE_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/decision_edge_observation_profile_v0.json"
O1_READOUT_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/decision_edge_observation_readout_v0.json"
O1_SOURCE_SURFACE_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/o1_source_surface_v0.json"
O1_TRACE_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/o1_transition_trace.json"
O1_REPORT_PATH = ROOT / "data/o1_decision_edge_observability_surface_v0/o1_report.json"
O1_DESIGN_RECEIPT_PATH = ROOT / "data/o1_decision_edge_observability_target_design_v0_receipts/c9ef517f.json"
O1_DESIGN_AUTHORIZATION_PATH = ROOT / "data/o1_decision_edge_observability_target_design_v0/o1_build_unit_authorization_v0.json"

OUT_DIR = ROOT / "data/o1_decision_edge_observability_surface_review_v0"
RECEIPT_DIR = ROOT / "data/o1_decision_edge_observability_surface_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "o1_decision_edge_observability_surface_review_assessment_v0.json"
OBSERVATION_RECORD_REVIEW_PATH = OUT_DIR / "o1_observation_record_integrity_review_v0.json"
HANDLE_REVIEW_PATH = OUT_DIR / "o1_candidate_handle_provisionality_review_v0.json"
ROLLUP_REVIEW_PATH = OUT_DIR / "o1_rollup_profile_readout_review_v0.json"
SOURCE_SURFACE_REVIEW_PATH = OUT_DIR / "o1_source_surface_review_v0.json"
NONAUTHORITY_SAFETY_REVIEW_PATH = OUT_DIR / "o1_nonauthority_safety_review_v0.json"
CLOSURE_CANDIDATE_PATH = OUT_DIR / "o1_decision_edge_observability_surface_closure_candidate_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "o1_surface_review_downstream_decision_table_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o1_surface_review_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o1_surface_review_authority_boundary_v0.json"
ROLLUP_OUT_PATH = OUT_DIR / "o1_surface_review_rollup_v0.json"
PROFILE_OUT_PATH = OUT_DIR / "o1_surface_review_profile_v0.json"
REPORT_OUT_PATH = OUT_DIR / "o1_surface_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "o1_surface_review_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    O1_SURFACE_RECEIPT_PATH,
    O1_OBSERVATION_SCHEMA_PATH,
    O1_HANDLE_SCHEMA_PATH,
    O1_HANDLE_RECORDS_PATH,
    O1_OBSERVATION_RECORDS_PATH,
    O1_ROLLUP_PATH,
    O1_PROFILE_PATH,
    O1_READOUT_PATH,
    O1_SOURCE_SURFACE_PATH,
    O1_TRACE_PATH,
    O1_REPORT_PATH,
    O1_DESIGN_RECEIPT_PATH,
    O1_DESIGN_AUTHORIZATION_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_EMITTED"
EXPECTED_SOURCE_STOP = "STOP_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_EMITTED"
EXPECTED_SOURCE_NEXT = "REVIEW_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_V0"

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

    receipt = read_json(O1_SURFACE_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o1_decision_edge_observability_surface_summary", {})
    obs_schema = read_json(O1_OBSERVATION_SCHEMA_PATH)
    handle_schema = read_json(O1_HANDLE_SCHEMA_PATH)
    handle_records = read_jsonl(O1_HANDLE_RECORDS_PATH)
    obs_records = read_jsonl(O1_OBSERVATION_RECORDS_PATH)
    rollup = read_json(O1_ROLLUP_PATH)
    profile = read_json(O1_PROFILE_PATH)
    readout = read_json(O1_READOUT_PATH)
    source_surface = read_json(O1_SOURCE_SURFACE_PATH)
    trace = read_json(O1_TRACE_PATH)
    report = read_json(O1_REPORT_PATH)
    design_receipt = read_json(O1_DESIGN_RECEIPT_PATH)
    design_auth = read_json(O1_DESIGN_AUTHORIZATION_PATH)

    if receipt.get("receipt_id") != O1_SURFACE_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("o1_surface_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("o1_surface_terminal_not_expected")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"o1_surface_status_not_expected:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"o1_surface_next_not_expected:{summary.get('recommended_next')}")

    for key in [
        "candidate_handles_marked_provisional",
        "bad_counters_zero",
        "rollup_emitted",
        "profile_emitted",
        "readout_emitted",
        "source_surface_emitted",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

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
    ]:
        if summary.get(key) is not False:
            failures.append(f"summary_forbidden_true:{key}")

    if summary.get("observations_emitted") != 8:
        failures.append(f"observations_emitted_not_8:{summary.get('observations_emitted')}")
    if summary.get("source_receipt_count") != 5:
        failures.append(f"source_receipt_count_not_5:{summary.get('source_receipt_count')}")
    if summary.get("candidate_handle_count") != 13:
        failures.append(f"candidate_handle_count_not_13:{summary.get('candidate_handle_count')}")
    if summary.get("collection_status") != "OBSERVATION_ONLY":
        failures.append("collection_status_not_observation_only")
    if summary.get("schema_claim") != "NONE":
        failures.append("schema_claim_not_none")

    if obs_schema.get("schema_version") != "decision_edge_observation_record_schema_v0":
        failures.append("observation_schema_version_wrong")
    if handle_schema.get("schema_version") != "decision_edge_candidate_handle_schema_v0":
        failures.append("handle_schema_version_wrong")
    if len(handle_records) != 13:
        failures.append(f"handle_records_count_not_13:{len(handle_records)}")
    if len(obs_records) != 8:
        failures.append(f"observation_records_count_not_8:{len(obs_records)}")

    for idx, h in enumerate(handle_records):
        if h.get("schema_version") != "decision_edge_candidate_handle_v0":
            failures.append(f"handle_schema_wrong:{idx}")
        if "define final graph edge" not in h.get("forbidden_use", []):
            failures.append(f"handle_not_provisional_enough:{idx}")
        if "authorize move" not in h.get("forbidden_use", []):
            failures.append(f"handle_missing_authority_forbid:{idx}")

    for idx, obs in enumerate(obs_records):
        if obs.get("schema_version") != "decision_edge_observation_record_v0":
            failures.append(f"obs_schema_wrong:{idx}")
        if not obs.get("source", {}).get("source_receipt_ref"):
            failures.append(f"obs_missing_source_ref:{idx}")
        if not obs.get("source", {}).get("source_unit_id"):
            failures.append(f"obs_missing_source_unit:{idx}")
        if not obs.get("edge_surface", {}).get("active_object") and obs.get("classification", {}).get("confidence_class") != "UNDER_TYPED":
            failures.append(f"obs_missing_active_object:{idx}")
        if not obs.get("boundary", {}).get("boundary_checked") and obs.get("classification", {}).get("confidence_class") != "UNDER_TYPED":
            failures.append(f"obs_missing_boundary_checked:{idx}")
        if not obs.get("boundary", {}).get("boundary_result") and obs.get("classification", {}).get("confidence_class") != "UNDER_TYPED":
            failures.append(f"obs_missing_boundary_result:{idx}")
        if not isinstance(obs.get("movement", {}).get("blocked_moves"), list):
            failures.append(f"obs_blocked_moves_not_list:{idx}")
        if not isinstance(obs.get("movement", {}).get("lawful_next_moves"), list):
            failures.append(f"obs_lawful_next_moves_not_list:{idx}")
        if not isinstance(obs.get("movement", {}).get("forbidden_next_moves"), list):
            failures.append(f"obs_forbidden_next_moves_not_list:{idx}")
        if not obs.get("terminal", {}).get("terminal_result"):
            failures.append(f"obs_missing_terminal:{idx}")
        if "parent_return_payload" not in obs.get("terminal", {}):
            failures.append(f"obs_missing_parent_return_payload_field:{idx}")
        if obs.get("safety", {}).get("collection_status") != "OBSERVATION_ONLY":
            failures.append(f"obs_collection_not_observation_only:{idx}")
        if obs.get("safety", {}).get("schema_claim") != "NONE":
            failures.append(f"obs_schema_claim_not_none:{idx}")
        for key in ["architecture_change", "source_receipt_mutated", "authority_expansion", "runtime_patch_applied", "target_selected_for_build", "c5_opened"]:
            if obs.get("safety", {}).get(key) is not False:
                failures.append(f"obs_safety_true:{key}:{idx}")

    handle_counter = Counter()
    boundary_authority_count = 0
    boundary_capability_count = 0
    terminal_counter = Counter()
    for obs in obs_records:
        handle_counter.update(obs.get("classification", {}).get("candidate_edge_handles", []))
        if obs.get("boundary", {}).get("authority_boundary_exposed") is True:
            boundary_authority_count += 1
        if obs.get("boundary", {}).get("capability_boundary_exposed") is True:
            boundary_capability_count += 1
        if obs.get("terminal", {}).get("terminal_result"):
            terminal_counter[obs["terminal"]["terminal_result"]] += 1

    if rollup.get("total_observations") != len(obs_records):
        failures.append("rollup_total_observations_mismatch")
    if rollup.get("source_receipt_count") != 5:
        failures.append("rollup_source_receipt_count_wrong")
    if rollup.get("candidate_edge_handle_counts") != dict(sorted(handle_counter.items())):
        failures.append("rollup_handle_counts_mismatch")
    if rollup.get("boundary_counts", {}).get("authority_boundary_count") != boundary_authority_count:
        failures.append("rollup_authority_boundary_count_mismatch")
    if rollup.get("boundary_counts", {}).get("capability_boundary_count") != boundary_capability_count:
        failures.append("rollup_capability_boundary_count_mismatch")
    if rollup.get("terminal_result_counts") != dict(sorted(terminal_counter.items())):
        failures.append("rollup_terminal_counts_mismatch")

    bad = rollup.get("bad_counters", {})
    for key in [
        "schema_claim_count",
        "architecture_change_count",
        "source_receipt_mutation_count",
        "authority_expansion_count",
        "target_selected_for_build_count",
        "runtime_patch_count",
        "c5_opened_count",
        "command_emitted_count",
    ]:
        if bad.get(key) != 0:
            failures.append(f"bad_counter_nonzero:{key}:{bad.get(key)}")

    if profile.get("schema_claim") != "NONE":
        failures.append("profile_schema_claim_not_none")
    if profile.get("architecture_change") is not False:
        failures.append("profile_architecture_change_true")
    if "graph schema" not in profile.get("recommendation", "").lower():
        failures.append("profile_recommendation_missing_graph_schema_caution")
    if readout.get("bad_counters_zero") is not True:
        failures.append("readout_bad_counters_zero_not_true")
    if readout.get("observations_emitted") != len(obs_records):
        failures.append("readout_observation_count_mismatch")
    if "graph schema exists" not in readout.get("must_not_infer", []):
        failures.append("readout_missing_must_not_infer_graph_schema")
    if source_surface.get("selection_rule") != "explicit_refs_only":
        failures.append("source_surface_selection_rule_wrong")
    if source_surface.get("payload_inspection_allowed") is not False:
        failures.append("source_surface_payload_inspection_allowed")
    if source_surface.get("source_mutation_allowed") is not False:
        failures.append("source_surface_mutation_allowed")
    if len(source_surface.get("source_receipts", [])) != 5:
        failures.append("source_surface_receipt_count_wrong")
    if trace.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("trace_terminal_wrong")
    if report.get("observations_emitted") != 8:
        failures.append("report_observations_wrong")
    if report.get("bad_counters_zero") is not True:
        failures.append("report_bad_counters_not_true")
    if design_receipt.get("receipt_id") != "c9ef517f":
        failures.append("design_receipt_wrong")
    if design_auth.get("authorized_next_unit") != "BUILD_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_V0":
        failures.append("design_authorization_wrong")

    return failures, {
        "summary": summary,
        "obs_records": obs_records,
        "handle_records": handle_records,
        "rollup": rollup,
        "profile": profile,
        "readout": readout,
        "source_surface": source_surface,
        "handle_counter": dict(sorted(handle_counter.items())),
        "terminal_counter": dict(sorted(terminal_counter.items())),
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    obs_records = src.get("obs_records", [])
    handle_records = src.get("handle_records", [])
    rollup = src.get("rollup", {})
    profile = src.get("profile", {})
    readout = src.get("readout", {})
    source_surface = src.get("source_surface", {})
    handle_counter = src.get("handle_counter", {})
    terminal_counter = src.get("terminal_counter", {})

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    if failures:
        status = "TYPED_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_REVIEW_BASIS_FAIL"
        review_pass = False
        reason_codes = failures
        recommended_next = "REPAIR_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_V0"
    else:
        status = "TYPED_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_REVIEWED_CLEAN_CLOSE_READY"
        review_pass = True
        reason_codes = [
            "O1_SURFACE_REVIEW_COMPLETE",
            "O1_SURFACE_REVIEW_PASS",
            "OBSERVATION_RECORD_INTEGRITY_PASS",
            "CANDIDATE_HANDLES_REMAIN_PROVISIONAL",
            "ROLLUP_PROFILE_READOUT_COHERENT",
            "SOURCE_SURFACE_EXPLICIT_REFS_ONLY",
            "NONAUTHORITY_SAFETY_REVIEW_PASS",
            "BAD_COUNTERS_ZERO",
            "NO_GRAPH_SCHEMA_CLAIMED",
            "NO_GRAPH_TRACKER_CREATED",
            "NO_ARCHITECTURE_CHANGE",
            "NO_SOURCE_RECEIPT_MUTATION",
            "NO_AUTHORITY_EXPANSION",
            "NO_TARGET_SELECTED_FOR_BUILD",
            "NO_RUNTIME_PATCH_APPLIED",
            "NO_C5_OPENED",
            "NO_O2_EXECUTED",
            "O1_CLOSURE_CANDIDATE_EMITTED",
        ]
        recommended_next = "CLOSE_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_AS_REVIEWED_REFERENCE_V0"

    review_assessment = {
        "schema_version": "o1_decision_edge_observability_surface_review_assessment_v0",
        "review_status": status,
        "source_o1_surface_receipt_id": O1_SURFACE_RECEIPT_ID,
        "o1_surface_review_complete": review_pass,
        "o1_surface_review_pass": review_pass,
        "observations_reviewed": len(obs_records),
        "source_receipts_reviewed": len(source_surface.get("source_receipts", [])),
        "candidate_handles_reviewed": len(handle_records),
        "closure_candidate_ready": review_pass,
        "recommended_next": recommended_next,
    }

    observation_record_review = {
        "schema_version": "o1_observation_record_integrity_review_v0",
        "review_status": "OBSERVATION_RECORD_INTEGRITY_PASS" if review_pass else "OBSERVATION_RECORD_INTEGRITY_REPAIR_REQUIRED",
        "records_reviewed": len(obs_records),
        "records_have_source_receipt_ref": all(x.get("source", {}).get("source_receipt_ref") for x in obs_records),
        "records_have_active_object_or_undertyped": all(x.get("edge_surface", {}).get("active_object") or x.get("classification", {}).get("confidence_class") == "UNDER_TYPED" for x in obs_records),
        "records_have_boundary_checked_or_undertyped": all(x.get("boundary", {}).get("boundary_checked") or x.get("classification", {}).get("confidence_class") == "UNDER_TYPED" for x in obs_records),
        "records_have_boundary_result_or_undertyped": all(x.get("boundary", {}).get("boundary_result") or x.get("classification", {}).get("confidence_class") == "UNDER_TYPED" for x in obs_records),
        "records_have_terminal_result": all(x.get("terminal", {}).get("terminal_result") for x in obs_records),
        "records_preserve_parent_return_payload_field": all("parent_return_payload" in x.get("terminal", {}) for x in obs_records),
        "blocked_moves_recorded_as_lists": all(isinstance(x.get("movement", {}).get("blocked_moves"), list) for x in obs_records),
        "lawful_next_moves_recorded_as_lists": all(isinstance(x.get("movement", {}).get("lawful_next_moves"), list) for x in obs_records),
    }

    handle_review = {
        "schema_version": "o1_candidate_handle_provisionality_review_v0",
        "review_status": "CANDIDATE_HANDLES_PROVISIONALITY_PASS" if review_pass else "CANDIDATE_HANDLES_PROVISIONALITY_REPAIR_REQUIRED",
        "candidate_handle_count": len(handle_records),
        "candidate_edge_handle_counts": handle_counter,
        "all_handles_forbid_authorizing_moves": all("authorize move" in x.get("forbidden_use", []) for x in handle_records),
        "all_handles_forbid_final_graph_edge_definition": all("define final graph edge" in x.get("forbidden_use", []) for x in handle_records),
        "handles_are_collection_tags_only": True,
    }

    rollup_review = {
        "schema_version": "o1_rollup_profile_readout_review_v0",
        "review_status": "ROLLUP_PROFILE_READOUT_COHERENT" if review_pass else "ROLLUP_PROFILE_READOUT_REPAIR_REQUIRED",
        "rollup_total_observations": rollup.get("total_observations"),
        "readout_observations_emitted": readout.get("observations_emitted"),
        "profile_schema_claim": profile.get("schema_claim"),
        "profile_architecture_change": profile.get("architecture_change"),
        "bad_counters": rollup.get("bad_counters", {}),
        "bad_counters_zero": readout.get("bad_counters_zero"),
        "terminal_result_counts": terminal_counter,
    }

    source_surface_review = {
        "schema_version": "o1_source_surface_review_v0",
        "review_status": "SOURCE_SURFACE_EXPLICIT_REFS_ONLY_PASS" if review_pass else "SOURCE_SURFACE_REPAIR_REQUIRED",
        "source_receipt_count": len(source_surface.get("source_receipts", [])),
        "selection_rule": source_surface.get("selection_rule"),
        "inspection_mode": source_surface.get("inspection_mode"),
        "payload_inspection_allowed": source_surface.get("payload_inspection_allowed"),
        "source_mutation_allowed": source_surface.get("source_mutation_allowed"),
        "latest_file_guessing": False,
        "mtime_selection": False,
    }

    nonauthority_safety_review = {
        "schema_version": "o1_nonauthority_safety_review_v0",
        "review_status": "NONAUTHORITY_SAFETY_REVIEW_PASS" if review_pass else "NONAUTHORITY_SAFETY_REPAIR_REQUIRED",
        "collection_status": "OBSERVATION_ONLY",
        "schema_claim": "NONE",
        "observation_record_is_evidence_not_authority": True,
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
    }

    closure_candidate = {
        "schema_version": "o1_decision_edge_observability_surface_closure_candidate_v0",
        "closure_candidate_status": "O1_SURFACE_CLOSURE_CANDIDATE_READY" if review_pass else "O1_SURFACE_CLOSURE_CANDIDATE_NOT_READY",
        "o1_surface_review_pass": review_pass,
        "reviewed_reference_candidate": "o1_decision_edge_observability_surface_v0",
        "closure_meaning": "O1 decision-edge observability sidecars may be closed as a reviewed observability reference.",
        "closure_does_not_mean": [
            "decision graph built",
            "graph schema extracted",
            "candidate handles finalized",
            "authority expanded",
            "runtime patched",
            "C5 opened",
            "O2 completed",
        ],
        "recommended_after_closure": "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET_V0",
    }

    downstream_decision_table = {
        "schema_version": "o1_surface_review_downstream_decision_table_v0",
        "decision_status": "O1_SURFACE_REVIEW_DOWNSTREAM_TABLE_EMITTED",
        "records": [
            {
                "decision": "CLOSE_O1_SURFACE_AS_REVIEWED_REFERENCE",
                "selected": review_pass,
                "next_unit": "CLOSE_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_AS_REVIEWED_REFERENCE_V0" if review_pass else None,
                "why": "O1 surface reviewed clean and closure candidate emitted.",
            },
            {
                "decision": "START_O2_NOW",
                "selected": False,
                "next_unit": None,
                "why": "O2 should follow after O1 is closed as reviewed reference.",
            },
            {
                "decision": "EXTRACT_GRAPH_SCHEMA_NOW",
                "selected": False,
                "next_unit": None,
                "why": "O1 is observability, not graph schema extraction.",
            },
        ],
    }

    classification = {
        "schema_version": "o1_surface_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "o1_surface_review_complete": review_pass,
        "o1_surface_review_pass": review_pass,
        "observations_reviewed": len(obs_records),
        "source_receipt_count": len(source_surface.get("source_receipts", [])),
        "candidate_handle_count": len(handle_records),
        "candidate_handles_remain_provisional": review_pass,
        "rollup_profile_readout_coherent": review_pass,
        "source_surface_explicit_refs_only": review_pass,
        "closure_candidate_ready": review_pass,
        "recommended_next": recommended_next,
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
        "next_command_goal": None,
    }

    authority_boundary = {
        "schema_version": "o1_surface_review_authority_boundary_v0",
        "status": status,
        "may_close_o1_surface_next": review_pass,
        "may_start_o2_now": False,
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

    rollup_out = {
        "schema_version": "o1_surface_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "o1_surface_review_count": 1,
        "o1_surface_review_pass_count": 1 if review_pass else 0,
        "observations_reviewed_count": len(obs_records),
        "source_receipt_count": len(source_surface.get("source_receipts", [])),
        "candidate_handle_count": len(handle_records),
        "closure_candidate_count": 1 if review_pass else 0,
        "graph_schema_claim_count": 0,
        "graph_tracker_created_count": 0,
        "architecture_change_count": 0,
        "source_receipt_mutation_count": 0,
        "authority_expansion_count": 0,
        "target_selected_for_build_count": 0,
        "runtime_patch_count": 0,
        "c5_opened_count": 0,
        "command_emitted_count": 0,
        "unit_feedback_hardening_executed_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    zero_keys = [
        "graph_schema_claim_count",
        "graph_tracker_created_count",
        "architecture_change_count",
        "source_receipt_mutation_count",
        "authority_expansion_count",
        "target_selected_for_build_count",
        "runtime_patch_count",
        "c5_opened_count",
        "command_emitted_count",
        "unit_feedback_hardening_executed_count",
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile_out = {
        "schema_version": "o1_surface_review_profile_v0",
        "profile_id": "o1_surface_review_profile_" + sha8(rollup_out),
        "status": status,
        "o1_surface_review_pass": review_pass,
        "observations_reviewed": len(obs_records),
        "candidate_handles_remain_provisional": review_pass,
        "closure_candidate_ready": review_pass,
        "recommendation": "Close O1 as reviewed observability reference before designing O2 unit feedback hardening.",
        "graph_schema_claimed": False,
        "graph_tracker_created": False,
        "architecture_change": False,
        "authority_expansion": False,
        "runtime_patch_applied": False,
        "c5_opened": False,
        "bad_counters_zero": all(rollup_out.get(k) == 0 for k in zero_keys),
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o1_surface_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The O1 decision-edge observability surface reviewed clean. Eight sidecar observations are source-backed, terminal/boundary/movement fields are present, candidate handles remain provisional, rollup/profile/readout are coherent, source surface remains explicit-refs-only, and bad counters are zero. No graph schema, graph tracker, source mutation, authority expansion, target selection, runtime patch, C5 opening, command emission, or O2 execution occurred.",
        "observations_reviewed": len(obs_records),
        "source_receipt_count": len(source_surface.get("source_receipts", [])),
        "candidate_handle_count": len(handle_records),
        "closure_candidate_ready": review_pass,
        "recommended_next_handling": recommended_next,
        "recommended_after_closure": "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET_V0",
        "bad_counters_zero": profile_out["bad_counters_zero"],
    }

    trace = {
        "schema_version": "o1_surface_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_o1_surface",
                "question": "did O1 emit the required sidecar surface",
                "answer": "yes" if review_pass else "no",
                "taken": "review observation records, handle records, rollup, profile, readout, and source surface",
            },
            {
                "step": "verify_nonauthority_boundary",
                "question": "did O1 claim graph schema or move authority/runtime/C5/O2",
                "answer": "no",
                "taken": "emit nonauthority safety review with bad counters zero",
            },
            {
                "step": "emit_closure_candidate",
                "question": "can O1 be closed as a reviewed observability reference",
                "answer": "yes" if review_pass else "no",
                "taken": recommended_next,
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    write_json(REVIEW_ASSESSMENT_PATH, review_assessment)
    write_json(OBSERVATION_RECORD_REVIEW_PATH, observation_record_review)
    write_json(HANDLE_REVIEW_PATH, handle_review)
    write_json(ROLLUP_REVIEW_PATH, rollup_review)
    write_json(SOURCE_SURFACE_REVIEW_PATH, source_surface_review)
    write_json(NONAUTHORITY_SAFETY_REVIEW_PATH, nonauthority_safety_review)
    write_json(CLOSURE_CANDIDATE_PATH, closure_candidate)
    write_json(DOWNSTREAM_DECISION_TABLE_PATH, downstream_decision_table)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(AUTHORITY_BOUNDARY_PATH, authority_boundary)
    write_json(ROLLUP_OUT_PATH, rollup_out)
    write_json(PROFILE_OUT_PATH, profile_out)
    write_json(REPORT_OUT_PATH, report)
    write_json(TRANSITION_TRACE_PATH, trace)

    acceptance_gate_results = {
        "O1_REVIEW_0_SOURCE_SURFACE_RECEIPT_CONSUMED": O1_SURFACE_RECEIPT_PATH.exists(),
        "O1_REVIEW_1_REVIEW_ASSESSMENT_EMITTED": REVIEW_ASSESSMENT_PATH.exists(),
        "O1_REVIEW_2_OBSERVATION_RECORD_INTEGRITY_PASS": observation_record_review["review_status"] == "OBSERVATION_RECORD_INTEGRITY_PASS",
        "O1_REVIEW_3_CANDIDATE_HANDLES_PROVISIONALITY_PASS": handle_review["review_status"] == "CANDIDATE_HANDLES_PROVISIONALITY_PASS",
        "O1_REVIEW_4_ROLLUP_PROFILE_READOUT_COHERENT": rollup_review["review_status"] == "ROLLUP_PROFILE_READOUT_COHERENT",
        "O1_REVIEW_5_SOURCE_SURFACE_EXPLICIT_REFS_ONLY_PASS": source_surface_review["review_status"] == "SOURCE_SURFACE_EXPLICIT_REFS_ONLY_PASS",
        "O1_REVIEW_6_NONAUTHORITY_SAFETY_REVIEW_PASS": nonauthority_safety_review["review_status"] == "NONAUTHORITY_SAFETY_REVIEW_PASS",
        "O1_REVIEW_7_OBSERVATION_COUNT_8": len(obs_records) == 8,
        "O1_REVIEW_8_SOURCE_RECEIPT_COUNT_5": len(source_surface.get("source_receipts", [])) == 5,
        "O1_REVIEW_9_CANDIDATE_HANDLE_COUNT_13": len(handle_records) == 13,
        "O1_REVIEW_10_CLOSURE_CANDIDATE_EMITTED": closure_candidate["closure_candidate_status"] == "O1_SURFACE_CLOSURE_CANDIDATE_READY",
        "O1_REVIEW_11_NO_GRAPH_SCHEMA_CLAIM": rollup_out["graph_schema_claim_count"] == 0,
        "O1_REVIEW_12_NO_GRAPH_TRACKER": rollup_out["graph_tracker_created_count"] == 0,
        "O1_REVIEW_13_NO_ARCHITECTURE_CHANGE": rollup_out["architecture_change_count"] == 0,
        "O1_REVIEW_14_NO_SOURCE_RECEIPT_MUTATION": rollup_out["source_receipt_mutation_count"] == 0,
        "O1_REVIEW_15_NO_AUTHORITY_EXPANSION": rollup_out["authority_expansion_count"] == 0,
        "O1_REVIEW_16_NO_TARGET_SELECTED_FOR_BUILD": rollup_out["target_selected_for_build_count"] == 0,
        "O1_REVIEW_17_NO_RUNTIME_PATCH": rollup_out["runtime_patch_count"] == 0,
        "O1_REVIEW_18_NO_C5_OPENED": rollup_out["c5_opened_count"] == 0,
        "O1_REVIEW_19_NO_COMMAND_EMITTED": rollup_out["command_emitted_count"] == 0,
        "O1_REVIEW_20_NO_O2_EXECUTED": rollup_out["unit_feedback_hardening_executed_count"] == 0,
        "O1_REVIEW_21_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "O1_REVIEW_22_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_OUT_PATH.exists() and PROFILE_OUT_PATH.exists() and REPORT_OUT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "review_pass": review_pass,
        "observations": len(obs_records),
        "handles": len(handle_records),
        "bad": rollup_out,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o1_surface_review_receipt_v0",
        "receipt_type": "TYPED_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_o1_surface_receipt_id": O1_SURFACE_RECEIPT_ID,
        "machine_readable_o1_surface_review_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "o1_surface_review_complete": review_pass,
            "o1_surface_review_pass": review_pass,
            "observations_reviewed": len(obs_records),
            "source_receipt_count": len(source_surface.get("source_receipts", [])),
            "candidate_handle_count": len(handle_records),
            "candidate_handles_remain_provisional": review_pass,
            "observation_record_integrity_pass": observation_record_review["review_status"] == "OBSERVATION_RECORD_INTEGRITY_PASS",
            "rollup_profile_readout_coherent": rollup_review["review_status"] == "ROLLUP_PROFILE_READOUT_COHERENT",
            "source_surface_explicit_refs_only": source_surface_review["review_status"] == "SOURCE_SURFACE_EXPLICIT_REFS_ONLY_PASS",
            "nonauthority_safety_review_pass": nonauthority_safety_review["review_status"] == "NONAUTHORITY_SAFETY_REVIEW_PASS",
            "closure_candidate_ready": review_pass,
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
            "bad_counters_zero": profile_out["bad_counters_zero"],
            "recommended_next": recommended_next,
            "recommended_after_closure": "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET_V0",
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "review_assessment": rel(REVIEW_ASSESSMENT_PATH),
            "observation_record_review": rel(OBSERVATION_RECORD_REVIEW_PATH),
            "candidate_handle_review": rel(HANDLE_REVIEW_PATH),
            "rollup_profile_readout_review": rel(ROLLUP_REVIEW_PATH),
            "source_surface_review": rel(SOURCE_SURFACE_REVIEW_PATH),
            "nonauthority_safety_review": rel(NONAUTHORITY_SAFETY_REVIEW_PATH),
            "closure_candidate": rel(CLOSURE_CANDIDATE_PATH),
            "downstream_decision_table": rel(DOWNSTREAM_DECISION_TABLE_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "rollup": rel(ROLLUP_OUT_PATH),
            "profile": rel(PROFILE_OUT_PATH),
            "report": rel(REPORT_OUT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"o1_surface_review_receipt_id={receipt_id}")
    print(f"o1_surface_review_receipt_path={rel(receipt_path)}")
    print(f"o1_surface_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"o1_observation_record_review_path={rel(OBSERVATION_RECORD_REVIEW_PATH)}")
    print(f"o1_candidate_handle_review_path={rel(HANDLE_REVIEW_PATH)}")
    print(f"o1_rollup_profile_readout_review_path={rel(ROLLUP_REVIEW_PATH)}")
    print(f"o1_source_surface_review_path={rel(SOURCE_SURFACE_REVIEW_PATH)}")
    print(f"o1_nonauthority_safety_review_path={rel(NONAUTHORITY_SAFETY_REVIEW_PATH)}")
    print(f"o1_closure_candidate_path={rel(CLOSURE_CANDIDATE_PATH)}")
    print(f"o1_surface_review_rollup_path={rel(ROLLUP_OUT_PATH)}")
    print(f"o1_surface_review_profile_path={rel(PROFILE_OUT_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
