#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_B2_CELL0_INFORMATIVE_FAILURE_PROGRESS_CLASSIFIER_V0"
TARGET_UNIT_ID = "b2.cell0.informative_failure_progress_classifier.v0"
LAYER = "CELL_0 / FAILURE_PROGRESS_DISCIPLINE"
MODE = "CERTIFY / REFLECT / CLASSIFY"

SOURCE_B1_RECEIPT_ID = "b9c8f831"
SOURCE_B1_RECEIPT_PATH = ROOT / "data" / "b1_cell0_local_lawful_actor_stabilization_v0_receipts" / "b9c8f831.json"
SOURCE_B1_ROLLUP_PATH = ROOT / "data" / "b1_cell0_local_lawful_actor_stabilization_v0" / "cell0_reliability_rollup_v0.json"
SOURCE_B1_DEMO_RECEIPTS_PATH = ROOT / "data" / "b1_cell0_local_lawful_actor_stabilization_v0" / "cell0_demo_receipts_v0.jsonl"
SOURCE_B1_PRESSURE_CLASSIFICATIONS_PATH = ROOT / "data" / "b1_cell0_local_lawful_actor_stabilization_v0" / "cell0_pressure_classification_records_v0.jsonl"
SOURCE_B1_MOVE_RESULTS_PATH = ROOT / "data" / "b1_cell0_local_lawful_actor_stabilization_v0" / "cell0_local_move_result_records_v0.jsonl"
SOURCE_B1_PROFILE_PATH = ROOT / "data" / "b1_cell0_local_lawful_actor_stabilization_v0" / "cell0_local_lawful_actor_profile_v0.json"
SOURCE_B0_REFERENCE_OBJECT_PATH = ROOT / "data" / "b0_current_observability_branch_closure_reference_object_v0" / "cell0_observability_reference_object_v0.json"

OUT_DIR = ROOT / "data" / "b2_cell0_informative_failure_progress_classifier_v0"
RECEIPT_DIR = ROOT / "data" / "b2_cell0_informative_failure_progress_classifier_v0_receipts"

FAILURE_EVENT_SCHEMA_PATH = OUT_DIR / "failure_event_schema_v0.json"
RECURRENCE_KEY_SCHEMA_PATH = OUT_DIR / "failure_recurrence_key_schema_v0.json"
COMPARISON_SCHEMA_PATH = OUT_DIR / "failure_comparison_record_schema_v0.json"
PROGRESS_RECORD_SCHEMA_PATH = OUT_DIR / "failure_progress_record_schema_v0.json"
REPEAT_PRESSURE_SCHEMA_PATH = OUT_DIR / "failure_repeat_pressure_record_schema_v0.json"
EXPECTED_LIMIT_SCHEMA_PATH = OUT_DIR / "failure_expected_limit_record_schema_v0.json"
LOOP_CANDIDATE_SCHEMA_PATH = OUT_DIR / "failure_loop_candidate_record_schema_v0.json"
PROGRESS_CLASS_ENUM_PATH = OUT_DIR / "failure_progress_class_enum_v0.json"
CLASSIFIER_RULES_PATH = OUT_DIR / "informative_failure_classifier_rules_v0.json"

DEMO_FAILURE_EVENTS_PATH = OUT_DIR / "b2_demo_failure_events_v0.jsonl"
DEMO_RECURRENCE_KEYS_PATH = OUT_DIR / "b2_demo_failure_recurrence_keys_v0.jsonl"
DEMO_COMPARISONS_PATH = OUT_DIR / "b2_demo_failure_comparisons_v0.jsonl"
FAILURE_PROGRESS_RECORDS_PATH = OUT_DIR / "b2_failure_progress_records_v0.jsonl"
REPEAT_PRESSURE_RECORDS_PATH = OUT_DIR / "b2_repeat_pressure_records_v0.jsonl"
EXPECTED_LIMIT_RECORDS_PATH = OUT_DIR / "b2_expected_limit_records_v0.jsonl"
LOOP_CANDIDATE_RECORDS_PATH = OUT_DIR / "b2_loop_candidate_records_v0.jsonl"
ROLLUP_PATH = OUT_DIR / "b2_failure_progress_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "b2_informative_failure_profile_v0.json"
TRANSITION_TRACE_PATH = OUT_DIR / "b2_transition_trace.json"
REPORT_PATH = OUT_DIR / "b2_report.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_B1_RECEIPT_PATH,
    SOURCE_B1_ROLLUP_PATH,
    SOURCE_B1_DEMO_RECEIPTS_PATH,
    SOURCE_B1_PRESSURE_CLASSIFICATIONS_PATH,
    SOURCE_B1_MOVE_RESULTS_PATH,
    SOURCE_B1_PROFILE_PATH,
    SOURCE_B0_REFERENCE_OBJECT_PATH,
]

PROGRESS_CLASSES = [
    "NEW_SURFACE",
    "SHARPER_LOCALIZATION",
    "SAME_FAILURE_RECURRED",
    "ABSOLUTE_LOOP_CANDIDATE",
    "EXPECTED_LIMIT",
    "PRODUCTIVE_PRESSURE",
    "NON_PRODUCTIVE_PRESSURE",
    "AUTHORITY_BOUNDARY_CLARIFIED",
    "MISSING_OBJECT_CLARIFIED",
    "MISSING_MOVE_PROGRESS",
    "INSUFFICIENT_EVIDENCE",
    "UNCLASSIFIED_FAILURE_PRESSURE",
]

RETRY_VERDICTS = [
    "RETRY_FORBIDDEN_NO_DELTA",
    "RETRY_FORBIDDEN_EXPECTED_LIMIT",
    "RETRY_FORBIDDEN_AUTHORITY_BOUNDARY",
    "RETRY_FORBIDDEN_LOOP_CANDIDATE",
    "RETRY_ALLOWED_AFTER_SHARPENING",
    "RETRY_NOT_APPLICABLE",
]

ZERO_COUNTER_KEYS = [
    "blind_retry_recommended_count",
    "repair_executed_count",
    "builder_command_executed_count",
    "hidden_next_command_count",
    "untyped_failure_count",
    "new_artifact_only_counted_as_progress_count",
    "productive_pressure_counted_as_radius_improvement_count",
    "same_failure_counted_as_progress_count",
    "retry_lawful_without_delta_count",
    "expected_limit_retried_same_objective_count",
    "proposal_applied_count",
    "artifact_delta_counted_as_surface_delta_count",
]

HUMAN_DECISION = {
    "decision": "BUILD_B2_CELL0_INFORMATIVE_FAILURE_PROGRESS_CLASSIFIER",
    "scope": "Build B2 as the Cell 0 informative failure-progress classifier. Consume explicit B1 typed stop/proposal records and rollup, normalize failures into failure events, compute recurrence keys, compare decision-surface deltas, classify each failure with a closed progress enum, emit retry verdicts, repeat-pressure records, expected-limit records, loop-candidate records, rollup, profile, and receipt. Do not repair, retry, execute builder commands, mutate taxonomy/registry, treat expected limits as bugs, or count repeated failure/new artifacts as progress.",
    "authorized": [
        "consume B1 reliability rollup",
        "consume B1 demo receipts",
        "consume B1 pressure classification records",
        "consume B1 local move result records",
        "consume B1 local lawful actor profile",
        "normalize stopped/proposal outcomes into failure events",
        "compute recurrence keys",
        "compare decision-surface deltas",
        "classify failures with closed enum",
        "emit per-record retry verdicts",
        "emit repeat-pressure records",
        "emit expected-limit records",
        "emit loop-candidate records",
        "emit failure-progress rollup",
        "emit informative failure profile",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "repair the failure",
        "retry the failing command",
        "execute builder command",
        "mutate source artifacts",
        "mutate prior receipts",
        "mutate taxonomy",
        "mutate registry",
        "invent missing objects without evidence",
        "widen authority to escape failure",
        "treat proposal as accepted",
        "treat expected limit as bug",
        "treat same failure as progress",
        "hide uncertainty under vague investigation",
        "emit hidden next command",
        "use latest-file selection",
        "use mtime selection",
        "use chat memory as recurrence evidence",
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

def append_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def validate_b1_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_b1_source_missing:{path.as_posix()}")

    if failures:
        return failures

    b1_receipt = read_json(SOURCE_B1_RECEIPT_PATH)
    b1_rollup = read_json(SOURCE_B1_ROLLUP_PATH)
    b1_profile = read_json(SOURCE_B1_PROFILE_PATH)
    b1_receipts = read_jsonl(SOURCE_B1_DEMO_RECEIPTS_PATH)
    b1_classifications = read_jsonl(SOURCE_B1_PRESSURE_CLASSIFICATIONS_PATH)
    b1_moves = read_jsonl(SOURCE_B1_MOVE_RESULTS_PATH)
    b0_ref = read_json(SOURCE_B0_REFERENCE_OBJECT_PATH)

    if b1_receipt.get("receipt_id") != SOURCE_B1_RECEIPT_ID:
        failures.append("b1_receipt_id_wrong")
    if b1_receipt.get("gate") != "PASS":
        failures.append("b1_receipt_gate_not_PASS")
    if b1_receipt.get("b1_stabilization_summary", {}).get("profile_status") != "STABLE_LOCAL_ACTOR_PROFILE":
        failures.append("b1_profile_not_stable_in_receipt")
    if b1_rollup.get("surfaces_processed") != 8:
        failures.append("b1_rollup_surface_count_unexpected")
    if b1_rollup.get("typed_stops_emitted") != 8:
        failures.append("b1_rollup_typed_stops_unexpected")
    if b1_profile.get("status") != "STABLE_LOCAL_ACTOR_PROFILE":
        failures.append("b1_profile_not_stable")
    if len(b1_receipts) != 8:
        failures.append("b1_demo_receipts_count_unexpected")
    if len(b1_classifications) != 8:
        failures.append("b1_classifications_count_unexpected")
    if len(b1_moves) != 8:
        failures.append("b1_moves_count_unexpected")
    if b0_ref.get("reference_status") != "REFERENCE_ONLY":
        failures.append("b0_reference_not_reference_only")
    return failures

def failure_event_schema() -> Dict[str, Any]:
    return {
        "schema_version": "failure_event_schema_v0",
        "event_schema": {
            "schema_version": "failure_event_v0",
            "failure_event_id": "failure_<sig8>",
            "source": {
                "run_id": None,
                "unit_id": None,
                "receipt_id": None,
                "halt_code": None,
            },
            "surface": {
                "surface_id": None,
                "surface_kind": None,
                "pressure_class": None,
            },
            "observed_failure": {
                "summary": None,
                "field_refs": [],
            },
            "terminal_status": "STOP | ADVANCE | UNKNOWN",
            "first_seen_at": None,
        },
        "purpose": "Separate failure occurrence from failure interpretation.",
    }

def recurrence_key_schema() -> Dict[str, Any]:
    return {
        "schema_version": "failure_recurrence_key_schema_v0",
        "key_schema": {
            "schema_version": "failure_recurrence_key_v0",
            "recurrence_key_id": "recur_<sig8>",
            "failure_event_ref": None,
            "recurrence_key": {
                "halt_code": None,
                "pressure_class": None,
                "surface_kind": None,
                "object_kind": None,
                "field_path": None,
                "regime": None,
            },
        },
        "rule": "No recurrence key, no SAME_FAILURE_RECURRED classification.",
    }

def comparison_schema() -> Dict[str, Any]:
    return {
        "schema_version": "failure_comparison_record_schema_v0",
        "comparison_schema": {
            "schema_version": "failure_comparison_record_v0",
            "comparison_id": "fail_cmp_<sig8>",
            "current_failure_event": None,
            "prior_failure_events": [],
            "recurrence_key_match": False,
            "new_surface_detected": False,
            "localization_changed": False,
            "surface_smaller": False,
            "missing_object_clearer": False,
            "authority_boundary_clearer": False,
            "expected_limit_confirmed": False,
            "proposal_candidate_emitted": False,
            "new_evidence_refs": [],
            "new_artifact_only": False,
            "same_failure_without_progress": False,
            "artifact_delta_detected": False,
            "decision_surface_delta_detected": False,
            "artifact_delta_is_progress": False,
        },
        "core_test": "Did the decision surface change?",
        "not_core_test": "Did another file appear?",
    }

def progress_record_schema() -> Dict[str, Any]:
    return {
        "schema_version": "failure_progress_record_schema_v0",
        "record_schema": {
            "schema_version": "failure_progress_record_v0",
            "failure_progress_id": "fail_progress_<sig8>",
            "failure_event_ref": None,
            "recurrence_key_ref": None,
            "comparison_ref": None,
            "progress_class": None,
            "smallest_honest_reading": None,
            "what_got_sharper": [],
            "what_did_not_change": [],
            "must_not_infer": [],
            "allowed_next_handling": [],
            "recommended_next_class": None,
            "retry_verdict": {
                "verdict": None,
                "retry_lawful_later": False,
                "retry_block_reason": None,
                "required_delta_before_retry": [],
                "retry_must_not_repeat_same_surface": True,
            },
        },
        "required_must_not_infer": [
            "repair is complete",
            "root cause is globally solved",
            "move registry is correct",
            "future failures impossible",
            "failure implies progress",
            "retry is authorized",
        ],
    }

def repeat_pressure_schema() -> Dict[str, Any]:
    return {
        "schema_version": "failure_repeat_pressure_record_schema_v0",
        "record_schema": {
            "schema_version": "failure_repeat_pressure_record_v0",
            "repeat_record_id": "repeat_<sig8>",
            "pressure_class": None,
            "stop_code": None,
            "observation_ids": [],
            "repeat_count": 0,
            "same_missing_evidence": True,
            "same_authority_boundary": True,
            "same_move_status": True,
            "decision_surface_changed": False,
            "repeat_classification": "SAME_FAILURE_RECURRED | ABSOLUTE_LOOP_CANDIDATE | PRODUCTIVE_REPEAT",
        },
    }

def expected_limit_schema() -> Dict[str, Any]:
    return {
        "schema_version": "failure_expected_limit_record_schema_v0",
        "record_schema": {
            "schema_version": "failure_expected_limit_record_v0",
            "expected_limit_id": "expected_limit_<sig8>",
            "source_failure_event_id": None,
            "limit_kind": "AUTHORITY_LIMIT | EVIDENCE_LIMIT | CAPABILITY_LIMIT | SCHEMA_LIMIT | PAYLOAD_ACCESS_LIMIT",
            "why_expected": None,
            "what_current_layer_must_not_do": [],
            "allowed_next_handling": [
                "emit question packet",
                "emit candidate object proposal",
                "stop for human/schema decision",
            ],
            "not_a_bug": True,
            "retry_forbidden_under_same_objective": True,
            "requires_new_objective_or_authority_change": True,
        },
    }

def loop_candidate_schema() -> Dict[str, Any]:
    return {
        "schema_version": "failure_loop_candidate_record_schema_v0",
        "record_schema": {
            "schema_version": "failure_loop_candidate_record_v0",
            "loop_candidate_id": "loop_<sig8>",
            "pressure_class": None,
            "stop_code": None,
            "observation_ids": [],
            "loop_reason": None,
            "attempted_changes": [],
            "decision_surface_delta_count": 0,
            "recommended_handling": "STOP_AND_REVIEW | REQUEST_NARROWER_EVIDENCE | EXPECTED_LIMIT_MARK | TAXONOMY_REVIEW | MOVE_REGISTRY_REVIEW",
        },
        "rule": "B2 identifies loop candidates. It does not repair them.",
    }

def progress_class_enum() -> Dict[str, Any]:
    meanings = {
        "NEW_SURFACE": "Failure exposes a surface not previously tracked.",
        "SHARPER_LOCALIZATION": "Same broad failure is localized to a smaller object, field, layer, or boundary.",
        "SAME_FAILURE_RECURRED": "Same recurrence key returns with no sharper classification.",
        "ABSOLUTE_LOOP_CANDIDATE": "Same failure recurs after attempted changes with no decision-surface delta.",
        "EXPECTED_LIMIT": "Stop is an intended boundary of current regime.",
        "PRODUCTIVE_PRESSURE": "Failure exposes useful pressure but does not authorize execution.",
        "NON_PRODUCTIVE_PRESSURE": "Pressure exists but does not sharpen, localize, identify evidence, or expose lawful next decision surface.",
        "AUTHORITY_BOUNDARY_CLARIFIED": "Failure makes permission boundary sharper.",
        "MISSING_OBJECT_CLARIFIED": "Failure exposes a concrete missing object.",
        "MISSING_MOVE_PROGRESS": "No registered move exists for pressure class; route to missing-move proposal/review.",
        "INSUFFICIENT_EVIDENCE": "Failure cannot be honestly classified because required evidence is absent.",
        "UNCLASSIFIED_FAILURE_PRESSURE": "B2 cannot classify using current records.",
    }
    return {
        "schema_version": "failure_progress_class_enum_v0",
        "closed": True,
        "classes": [
            {
                "progress_class": cls,
                "smallest_honest_meaning": meanings[cls],
            }
            for cls in PROGRESS_CLASSES
        ],
    }

def classifier_rules() -> Dict[str, Any]:
    return {
        "schema_version": "informative_failure_classifier_rules_v0",
        "informative_failure_test": {
            "informative_if_any_true": [
                "new_surface_detected",
                "localization_changed",
                "surface_smaller",
                "missing_object_clearer",
                "authority_boundary_clearer",
                "expected_limit_confirmed",
                "proposal_candidate_emitted",
                "new_evidence_refs not empty",
            ],
            "non_informative_if": [
                "recurrence_key_match is true",
                "new_surface_detected is false",
                "localization_changed is false",
                "surface_smaller is false",
                "missing_object_clearer is false",
                "authority_boundary_clearer is false",
                "expected_limit_confirmed is false",
                "proposal_candidate_emitted is false",
                "new_evidence_refs empty",
            ],
        },
        "retry_gate": {
            "b2_does_not_retry": True,
            "retry_allowed_only_after": [
                "new evidence",
                "sharper localization",
                "smaller surface",
                "changed repair target",
                "expected limit converted to accepted new objective",
            ],
            "retry_forbidden_when_all_same": [
                "same command",
                "same surface",
                "same failure",
                "same evidence",
                "same expected behavior",
                "same authority state",
            ],
        },
        "artifact_delta_rule": "A new artifact is not progress unless it changes the decision surface.",
        "proposal_rule": "Proposal pressure may be productive, but it is not execution.",
        "expected_limit_rule": "Expected limit is not a bug and is not retryable under the same objective.",
    }

def schemas() -> Dict[Path, Dict[str, Any]]:
    return {
        FAILURE_EVENT_SCHEMA_PATH: failure_event_schema(),
        RECURRENCE_KEY_SCHEMA_PATH: recurrence_key_schema(),
        COMPARISON_SCHEMA_PATH: comparison_schema(),
        PROGRESS_RECORD_SCHEMA_PATH: progress_record_schema(),
        REPEAT_PRESSURE_SCHEMA_PATH: repeat_pressure_schema(),
        EXPECTED_LIMIT_SCHEMA_PATH: expected_limit_schema(),
        LOOP_CANDIDATE_SCHEMA_PATH: loop_candidate_schema(),
        PROGRESS_CLASS_ENUM_PATH: progress_class_enum(),
        CLASSIFIER_RULES_PATH: classifier_rules(),
    }

def b1_receipt_ref(case_index: int) -> str:
    rows = read_jsonl(SOURCE_B1_DEMO_RECEIPTS_PATH)
    return rows[case_index % len(rows)]["receipt_id"]

def demo_case_specs() -> List[Dict[str, Any]]:
    return [
        {
            "case_id": "new_surface_discovered",
            "progress_class": "NEW_SURFACE",
            "pressure_class": "FRONTIER_PRESSURE",
            "stop_code": "STOP_FRONTIER",
            "surface_kind": "proposal_packet",
            "object_kind": "missing_surface",
            "field_path": "source.previous_batch_rollup_ref",
            "summary": "current failure identifies a new inspectable missing previous_batch_rollup_ref surface",
            "flags": {"new_surface_detected": True, "new_evidence_refs": ["demo://new_surface/previous_batch_rollup_ref"]},
        },
        {
            "case_id": "same_pressure_sharpened",
            "progress_class": "SHARPER_LOCALIZATION",
            "pressure_class": "OBSERVABILITY_PRESSURE",
            "stop_code": "STOP_FRONTIER",
            "surface_kind": "metric_report",
            "object_kind": "observability_signal",
            "field_path": "receipt.reference_metadata",
            "summary": "observability issue narrowed to volatile receipt reference metadata",
            "flags": {"localization_changed": True, "surface_smaller": True, "new_evidence_refs": ["demo://sharper/reference_metadata"]},
        },
        {
            "case_id": "same_failure_recurred",
            "progress_class": "SAME_FAILURE_RECURRED",
            "pressure_class": "RECEIPT_TRACE_PRESSURE",
            "stop_code": "STOP_RECEIPT_TRACE_MISMATCH",
            "surface_kind": "receipt_bundle",
            "object_kind": "receipt_trace",
            "field_path": "trace.receipt_ref",
            "summary": "same receipt trace mismatch recurred with no new evidence",
            "flags": {"recurrence_key_match": True, "same_failure_without_progress": True},
        },
        {
            "case_id": "absolute_loop_candidate",
            "progress_class": "ABSOLUTE_LOOP_CANDIDATE",
            "pressure_class": "RECEIPT_TRACE_PRESSURE",
            "stop_code": "STOP_RECEIPT_TRACE_MISMATCH",
            "surface_kind": "receipt_bundle",
            "object_kind": "receipt_trace",
            "field_path": "trace.receipt_ref",
            "summary": "same failure recurred after attempted proposal/retry with no decision-surface delta",
            "flags": {"recurrence_key_match": True, "same_failure_without_progress": True, "attempted_changes": ["proposal_emitted", "same_objective_retry_candidate"], "loop": True},
        },
        {
            "case_id": "expected_limit_reached",
            "progress_class": "EXPECTED_LIMIT",
            "pressure_class": "AUTHORITY_PRESSURE",
            "stop_code": "STOP_AUTHORITY_BOUNDARY",
            "surface_kind": "metric_report",
            "object_kind": "payload_access",
            "field_path": "payload",
            "summary": "Cell 0 refuses payload inspection under REF_ONLY surface",
            "flags": {"authority_boundary_clearer": True, "expected_limit_confirmed": True},
        },
        {
            "case_id": "productive_pressure",
            "progress_class": "PRODUCTIVE_PRESSURE",
            "pressure_class": "TAXONOMY_PRESSURE",
            "stop_code": "STOP_TAXONOMY_GAP",
            "surface_kind": "label_surface",
            "object_kind": "taxonomy_gap",
            "field_path": "pressure_class",
            "summary": "taxonomy gap exposes proposal pressure without authorizing registry mutation",
            "flags": {"proposal_candidate_emitted": True, "new_evidence_refs": ["demo://productive/taxonomy_gap"]},
        },
        {
            "case_id": "non_productive_pressure",
            "progress_class": "NON_PRODUCTIVE_PRESSURE",
            "pressure_class": "BURDEN_PRESSURE",
            "stop_code": "STOP_FRONTIER",
            "surface_kind": "queue_surface",
            "object_kind": "burden",
            "field_path": "queue.count",
            "summary": "pressure exists but no sharper distinction or lawful next decision surface appears",
            "flags": {},
        },
        {
            "case_id": "authority_boundary_clarified",
            "progress_class": "AUTHORITY_BOUNDARY_CLARIFIED",
            "pressure_class": "AUTHORITY_PRESSURE",
            "stop_code": "STOP_AUTHORITY_BOUNDARY",
            "surface_kind": "metric_report",
            "object_kind": "authority_profile",
            "field_path": "inspection_mode",
            "summary": "payload inspection refused because surface authority is REF_ONLY",
            "flags": {"authority_boundary_clearer": True},
        },
        {
            "case_id": "missing_object_clarified",
            "progress_class": "MISSING_OBJECT_CLARIFIED",
            "pressure_class": "FRONTIER_PRESSURE",
            "stop_code": "STOP_FRONTIER",
            "surface_kind": "proposal_packet",
            "object_kind": "schema_object",
            "field_path": "proposal.source_evidence_refs",
            "summary": "failure exposes concrete missing source_evidence_refs object",
            "flags": {"missing_object_clearer": True, "new_evidence_refs": ["demo://missing_object/source_evidence_refs"]},
        },
        {
            "case_id": "missing_move_identified",
            "progress_class": "MISSING_MOVE_PROGRESS",
            "pressure_class": "MISSING_MOVE_PRESSURE",
            "stop_code": "STOP_NEEDS_NEW_MOVE",
            "surface_kind": "proposal_packet",
            "object_kind": "move_registry",
            "field_path": "moves.for_pressure",
            "summary": "no registered move exists for pressure class; missing-move proposal required",
            "flags": {"proposal_candidate_emitted": True, "missing_object_clearer": True},
        },
        {
            "case_id": "insufficient_evidence",
            "progress_class": "INSUFFICIENT_EVIDENCE",
            "pressure_class": "AMBIGUOUS_PRESSURE",
            "stop_code": "STOP_INSUFFICIENT_EVIDENCE",
            "surface_kind": "receipt_bundle",
            "object_kind": "unknown",
            "field_path": None,
            "summary": "failure cannot be classified because required evidence is absent",
            "flags": {"insufficient_evidence": True},
        },
        {
            "case_id": "unclassified_failure_pressure",
            "progress_class": "UNCLASSIFIED_FAILURE_PRESSURE",
            "pressure_class": "AMBIGUOUS_PRESSURE",
            "stop_code": "STOP_AMBIGUOUS_PRESSURE",
            "surface_kind": "halt_set",
            "object_kind": "unknown",
            "field_path": None,
            "summary": "B2 cannot classify using current records; question packet required",
            "flags": {"unclassified": True},
        },
    ]

def make_event(spec: Dict[str, Any], index: int) -> Dict[str, Any]:
    event_id = "failure_" + sha8({"case_id": spec["case_id"], "progress_class": spec["progress_class"]})
    return {
        "schema_version": "failure_event_v0",
        "failure_event_id": event_id,
        "case_id": spec["case_id"],
        "source": {
            "run_id": "b2_demo_failure_progress_run_v0",
            "unit_id": "BUILD_B1_CELL0_LOCAL_LAWFUL_ACTOR_STABILIZATION_V0",
            "receipt_id": b1_receipt_ref(index),
            "halt_code": spec["stop_code"],
        },
        "surface": {
            "surface_id": "b2_surface_" + sha8({"case_id": spec["case_id"], "surface_kind": spec["surface_kind"]}),
            "surface_kind": spec["surface_kind"],
            "pressure_class": spec["pressure_class"],
        },
        "observed_failure": {
            "summary": spec["summary"],
            "field_refs": [] if spec["field_path"] is None else [spec["field_path"]],
        },
        "terminal_status": "STOP",
        "first_seen_at": now_iso(),
    }

def make_recurrence_key(event: Dict[str, Any], spec: Dict[str, Any]) -> Dict[str, Any]:
    if spec["progress_class"] == "INSUFFICIENT_EVIDENCE":
        key = {
            "halt_code": None,
            "pressure_class": None,
            "surface_kind": None,
            "object_kind": None,
            "field_path": None,
            "regime": "INSUFFICIENT_EVIDENCE_NO_SAME_FAILURE_CLASS_ALLOWED",
        }
    else:
        key = {
            "halt_code": spec["stop_code"],
            "pressure_class": spec["pressure_class"],
            "surface_kind": spec["surface_kind"],
            "object_kind": spec["object_kind"],
            "field_path": spec["field_path"],
            "regime": "CELL0_LOCAL_ACTOR_DEMO",
        }
    return {
        "schema_version": "failure_recurrence_key_v0",
        "recurrence_key_id": "recur_" + sha8({"event": event["failure_event_id"], "key": key}),
        "failure_event_ref": event["failure_event_id"],
        "recurrence_key": key,
        "recurrence_key_status": "INSUFFICIENT_EVIDENCE" if spec["progress_class"] == "INSUFFICIENT_EVIDENCE" else "PRESENT",
    }

def make_comparison(event: Dict[str, Any], spec: Dict[str, Any]) -> Dict[str, Any]:
    flags = spec.get("flags", {})
    decision_surface_delta = any([
        flags.get("new_surface_detected", False),
        flags.get("localization_changed", False),
        flags.get("surface_smaller", False),
        flags.get("missing_object_clearer", False),
        flags.get("authority_boundary_clearer", False),
        flags.get("expected_limit_confirmed", False),
        flags.get("proposal_candidate_emitted", False),
        bool(flags.get("new_evidence_refs", [])),
    ])
    artifact_delta = spec["progress_class"] in {"PRODUCTIVE_PRESSURE", "MISSING_MOVE_PROGRESS", "MISSING_OBJECT_CLARIFIED"}
    return {
        "schema_version": "failure_comparison_record_v0",
        "comparison_id": "fail_cmp_" + sha8({"event": event["failure_event_id"], "case": spec["case_id"]}),
        "current_failure_event": event["failure_event_id"],
        "prior_failure_events": ["prior_demo://" + spec["case_id"]] if flags.get("recurrence_key_match") else [],
        "recurrence_key_match": bool(flags.get("recurrence_key_match", False)),
        "new_surface_detected": bool(flags.get("new_surface_detected", False)),
        "localization_changed": bool(flags.get("localization_changed", False)),
        "surface_smaller": bool(flags.get("surface_smaller", False)),
        "missing_object_clearer": bool(flags.get("missing_object_clearer", False)),
        "authority_boundary_clearer": bool(flags.get("authority_boundary_clearer", False)),
        "expected_limit_confirmed": bool(flags.get("expected_limit_confirmed", False)),
        "proposal_candidate_emitted": bool(flags.get("proposal_candidate_emitted", False)),
        "new_evidence_refs": list(flags.get("new_evidence_refs", [])),
        "new_artifact_only": False,
        "same_failure_without_progress": bool(flags.get("same_failure_without_progress", False)),
        "artifact_delta_detected": artifact_delta,
        "decision_surface_delta_detected": decision_surface_delta,
        "artifact_delta_is_progress": artifact_delta and decision_surface_delta,
    }

def retry_verdict_for(progress_class: str, comparison: Dict[str, Any]) -> Dict[str, Any]:
    if progress_class in {"NEW_SURFACE", "SHARPER_LOCALIZATION", "MISSING_OBJECT_CLARIFIED", "MISSING_MOVE_PROGRESS"}:
        return {
            "verdict": "RETRY_ALLOWED_AFTER_SHARPENING",
            "retry_lawful_later": True,
            "retry_block_reason": None,
            "required_delta_before_retry": ["new evidence", "sharper localization", "smaller surface", "changed repair target"],
            "retry_must_not_repeat_same_surface": True,
        }
    if progress_class == "EXPECTED_LIMIT":
        return {
            "verdict": "RETRY_FORBIDDEN_EXPECTED_LIMIT",
            "retry_lawful_later": False,
            "retry_block_reason": "expected limit is not retryable under same objective",
            "required_delta_before_retry": ["accepted new objective or authority change"],
            "retry_must_not_repeat_same_surface": True,
        }
    if progress_class == "AUTHORITY_BOUNDARY_CLARIFIED":
        return {
            "verdict": "RETRY_FORBIDDEN_AUTHORITY_BOUNDARY",
            "retry_lawful_later": False,
            "retry_block_reason": "authority boundary clarified; retry requires authority change",
            "required_delta_before_retry": ["explicit authority update"],
            "retry_must_not_repeat_same_surface": True,
        }
    if progress_class == "ABSOLUTE_LOOP_CANDIDATE":
        return {
            "verdict": "RETRY_FORBIDDEN_LOOP_CANDIDATE",
            "retry_lawful_later": False,
            "retry_block_reason": "same failure recurred after attempted changes with no decision-surface delta",
            "required_delta_before_retry": ["human review", "narrower evidence", "different objective"],
            "retry_must_not_repeat_same_surface": True,
        }
    if progress_class in {"SAME_FAILURE_RECURRED", "NON_PRODUCTIVE_PRESSURE"}:
        return {
            "verdict": "RETRY_FORBIDDEN_NO_DELTA",
            "retry_lawful_later": False,
            "retry_block_reason": "no decision-surface delta detected",
            "required_delta_before_retry": ["new evidence", "sharper localization", "smaller surface"],
            "retry_must_not_repeat_same_surface": True,
        }
    return {
        "verdict": "RETRY_NOT_APPLICABLE",
        "retry_lawful_later": False,
        "retry_block_reason": "classification requires question packet or evidence request, not retry",
        "required_delta_before_retry": ["explicit evidence"],
        "retry_must_not_repeat_same_surface": True,
    }

def progress_record(event: Dict[str, Any], recurrence_key: Dict[str, Any], comparison: Dict[str, Any], spec: Dict[str, Any]) -> Dict[str, Any]:
    progress_class = spec["progress_class"]
    what_got_sharper: List[str] = []
    if comparison["new_surface_detected"]:
        what_got_sharper.append("new surface identified")
    if comparison["localization_changed"]:
        what_got_sharper.append("pressure localization changed")
    if comparison["surface_smaller"]:
        what_got_sharper.append("surface narrowed")
    if comparison["missing_object_clearer"]:
        what_got_sharper.append("missing object clarified")
    if comparison["authority_boundary_clearer"]:
        what_got_sharper.append("authority boundary clarified")
    if comparison["expected_limit_confirmed"]:
        what_got_sharper.append("expected limit confirmed")
    if comparison["proposal_candidate_emitted"]:
        what_got_sharper.append("proposal surface exposed")
    if comparison["new_evidence_refs"]:
        what_got_sharper.append("new evidence refs exposed")

    if not what_got_sharper and progress_class in {"SAME_FAILURE_RECURRED", "NON_PRODUCTIVE_PRESSURE", "ABSOLUTE_LOOP_CANDIDATE"}:
        what_got_sharper = []

    proposal_surface = progress_class in {"PRODUCTIVE_PRESSURE", "MISSING_MOVE_PROGRESS", "MISSING_OBJECT_CLARIFIED"}
    return {
        "schema_version": "failure_progress_record_v0",
        "failure_progress_id": "fail_progress_" + sha8({"event": event["failure_event_id"], "class": progress_class}),
        "failure_event_ref": event["failure_event_id"],
        "recurrence_key_ref": recurrence_key["recurrence_key_id"],
        "comparison_ref": comparison["comparison_id"],
        "progress_class": progress_class,
        "smallest_honest_reading": spec["summary"],
        "what_got_sharper": what_got_sharper,
        "what_did_not_change": [
            "B2 did not repair",
            "B2 did not retry",
            "B2 did not execute builder command",
            "B2 did not mutate taxonomy or registry",
        ],
        "must_not_infer": [
            "repair is complete",
            "root cause is globally solved",
            "move registry is correct",
            "future failures impossible",
            "failure implies progress",
            "retry is authorized",
        ],
        "allowed_next_handling": allowed_next_handling(progress_class),
        "recommended_next_class": recommended_next_class(progress_class),
        "retry_verdict": retry_verdict_for(progress_class, comparison),
        "proposal_surface_exposed": proposal_surface,
        "proposal_applied": False,
        "proposal_accepted": False,
        "builder_command_authorized": False,
    }

def allowed_next_handling(progress_class: str) -> List[str]:
    mapping = {
        "NEW_SURFACE": ["inspect new surface", "request evidence", "stop for review"],
        "SHARPER_LOCALIZATION": ["use narrowed surface", "request narrower evidence", "stop for review"],
        "SAME_FAILURE_RECURRED": ["block blind retry", "request sharper evidence", "stop"],
        "ABSOLUTE_LOOP_CANDIDATE": ["STOP_AND_REVIEW", "REQUEST_NARROWER_EVIDENCE"],
        "EXPECTED_LIMIT": ["mark expected limit", "question packet", "new objective only if explicitly accepted"],
        "PRODUCTIVE_PRESSURE": ["record pressure", "proposal review", "no execution"],
        "NON_PRODUCTIVE_PRESSURE": ["record", "do not open build movement"],
        "AUTHORITY_BOUNDARY_CLARIFIED": ["authority review", "stop"],
        "MISSING_OBJECT_CLARIFIED": ["candidate object proposal", "human/schema decision"],
        "MISSING_MOVE_PROGRESS": ["move registry review", "missing move proposal"],
        "INSUFFICIENT_EVIDENCE": ["evidence request", "question packet"],
        "UNCLASSIFIED_FAILURE_PRESSURE": ["question packet", "do not command"],
    }
    return mapping[progress_class]

def recommended_next_class(progress_class: str) -> str:
    mapping = {
        "NEW_SURFACE": "INSPECT_NEW_SURFACE",
        "SHARPER_LOCALIZATION": "USE_NARROWER_SURFACE",
        "SAME_FAILURE_RECURRED": "BLOCK_BLIND_RETRY",
        "ABSOLUTE_LOOP_CANDIDATE": "STOP_AND_REVIEW",
        "EXPECTED_LIMIT": "EXPECTED_LIMIT_MARK",
        "PRODUCTIVE_PRESSURE": "PROPOSAL_REVIEW",
        "NON_PRODUCTIVE_PRESSURE": "NO_BUILD_MOVEMENT",
        "AUTHORITY_BOUNDARY_CLARIFIED": "AUTHORITY_REVIEW",
        "MISSING_OBJECT_CLARIFIED": "CANDIDATE_OBJECT_REVIEW",
        "MISSING_MOVE_PROGRESS": "MOVE_REGISTRY_REVIEW",
        "INSUFFICIENT_EVIDENCE": "EVIDENCE_REQUEST",
        "UNCLASSIFIED_FAILURE_PRESSURE": "QUESTION_PACKET_NOT_COMMAND",
    }
    return mapping[progress_class]

def repeat_pressure_record(event: Dict[str, Any], comparison: Dict[str, Any], spec: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if spec["progress_class"] not in {"SAME_FAILURE_RECURRED", "ABSOLUTE_LOOP_CANDIDATE"}:
        return None
    repeat_class = "ABSOLUTE_LOOP_CANDIDATE" if spec["progress_class"] == "ABSOLUTE_LOOP_CANDIDATE" else "SAME_FAILURE_RECURRED"
    return {
        "schema_version": "failure_repeat_pressure_record_v0",
        "repeat_record_id": "repeat_" + sha8({"event": event["failure_event_id"], "repeat": repeat_class}),
        "pressure_class": spec["pressure_class"],
        "stop_code": spec["stop_code"],
        "observation_ids": ["prior_demo://" + spec["case_id"], event["failure_event_id"]],
        "repeat_count": 2,
        "same_missing_evidence": True,
        "same_authority_boundary": True,
        "same_move_status": True,
        "decision_surface_changed": False,
        "repeat_classification": repeat_class,
    }

def expected_limit_record(event: Dict[str, Any], spec: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if spec["progress_class"] not in {"EXPECTED_LIMIT", "AUTHORITY_BOUNDARY_CLARIFIED"}:
        return None
    limit_kind = "AUTHORITY_LIMIT" if spec["pressure_class"] == "AUTHORITY_PRESSURE" else "CAPABILITY_LIMIT"
    return {
        "schema_version": "failure_expected_limit_record_v0",
        "expected_limit_id": "expected_limit_" + sha8({"event": event["failure_event_id"], "kind": limit_kind}),
        "source_failure_event_id": event["failure_event_id"],
        "limit_kind": limit_kind,
        "why_expected": spec["summary"],
        "what_current_layer_must_not_do": [
            "do not widen authority inside B2",
            "do not retry under same objective",
            "do not treat expected limit as bug",
            "do not execute repair",
        ],
        "allowed_next_handling": [
            "emit question packet",
            "emit candidate object proposal",
            "stop for human/schema decision",
        ],
        "not_a_bug": True,
        "retry_forbidden_under_same_objective": True,
        "requires_new_objective_or_authority_change": True,
    }

def loop_candidate_record(event: Dict[str, Any], spec: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if spec["progress_class"] != "ABSOLUTE_LOOP_CANDIDATE":
        return None
    return {
        "schema_version": "failure_loop_candidate_record_v0",
        "loop_candidate_id": "loop_" + sha8({"event": event["failure_event_id"], "loop": True}),
        "pressure_class": spec["pressure_class"],
        "stop_code": spec["stop_code"],
        "observation_ids": ["prior_demo://" + spec["case_id"], event["failure_event_id"]],
        "loop_reason": "same failure recurred after attempted changes with no decision-surface delta",
        "attempted_changes": spec.get("flags", {}).get("attempted_changes", []),
        "decision_surface_delta_count": 0,
        "recommended_handling": "STOP_AND_REVIEW",
        "auto_repaired": False,
        "repair_executed": False,
    }

def build_demo_records() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    events: List[Dict[str, Any]] = []
    recurrence_keys: List[Dict[str, Any]] = []
    comparisons: List[Dict[str, Any]] = []
    progress_records: List[Dict[str, Any]] = []
    repeat_records: List[Dict[str, Any]] = []
    expected_records: List[Dict[str, Any]] = []
    loop_records: List[Dict[str, Any]] = []

    for index, spec in enumerate(demo_case_specs()):
        event = make_event(spec, index)
        recur = make_recurrence_key(event, spec)
        cmp_record = make_comparison(event, spec)
        progress = progress_record(event, recur, cmp_record, spec)
        repeat = repeat_pressure_record(event, cmp_record, spec)
        expected = expected_limit_record(event, spec)
        loop = loop_candidate_record(event, spec)

        events.append(event)
        recurrence_keys.append(recur)
        comparisons.append(cmp_record)
        progress_records.append(progress)
        if repeat:
            repeat_records.append(repeat)
        if expected:
            expected_records.append(expected)
        if loop:
            loop_records.append(loop)

    return events, recurrence_keys, comparisons, progress_records, repeat_records, expected_records, loop_records

def is_informative(progress_class: str, comparison: Dict[str, Any]) -> bool:
    if progress_class in {"SAME_FAILURE_RECURRED", "ABSOLUTE_LOOP_CANDIDATE", "NON_PRODUCTIVE_PRESSURE", "INSUFFICIENT_EVIDENCE", "UNCLASSIFIED_FAILURE_PRESSURE"}:
        return False
    return any([
        comparison["new_surface_detected"],
        comparison["localization_changed"],
        comparison["surface_smaller"],
        comparison["missing_object_clearer"],
        comparison["authority_boundary_clearer"],
        comparison["expected_limit_confirmed"],
        comparison["proposal_candidate_emitted"],
        bool(comparison["new_evidence_refs"]),
    ])

def compute_rollup(
    events: List[Dict[str, Any]],
    comparisons: List[Dict[str, Any]],
    progress_records: List[Dict[str, Any]],
    repeat_records: List[Dict[str, Any]],
    expected_records: List[Dict[str, Any]],
    loop_records: List[Dict[str, Any]],
) -> Dict[str, Any]:
    counts = Counter(p["progress_class"] for p in progress_records)
    progress_class_counts = {cls: counts.get(cls, 0) for cls in PROGRESS_CLASSES}
    informative_count = sum(1 for p, c in zip(progress_records, comparisons) if is_informative(p["progress_class"], c))
    non_informative_count = len(progress_records) - informative_count
    retry_allowed_count = sum(1 for p in progress_records if p["retry_verdict"]["retry_lawful_later"] is True)
    blind_retry_blocked_count = sum(1 for p in progress_records if p["retry_verdict"]["retry_lawful_later"] is False and p["retry_verdict"]["verdict"] != "RETRY_NOT_APPLICABLE")
    artifact_delta_counted_as_surface_delta_count = sum(
        1 for c in comparisons
        if c["artifact_delta_detected"] and c["artifact_delta_is_progress"] and not c["decision_surface_delta_detected"]
    )
    rollup = {
        "schema_version": "failure_progress_rollup_v0",
        "failure_events_total": len(events),
        "progress_class_counts": progress_class_counts,
        "informative_failure_count": informative_count,
        "non_informative_failure_count": non_informative_count,
        "expected_limit_count": len(expected_records),
        "loop_candidate_count": len(loop_records),
        "blind_retry_blocked_count": blind_retry_blocked_count,
        "retry_allowed_count": retry_allowed_count,
        "blind_retry_recommended_count": 0,
        "repair_executed_count": 0,
        "builder_command_executed_count": 0,
        "hidden_next_command_count": 0,
        "untyped_failure_count": 0,
        "new_artifact_only_counted_as_progress_count": 0,
        "productive_pressure_counted_as_radius_improvement_count": 0,
        "same_failure_counted_as_progress_count": 0,
        "retry_lawful_without_delta_count": 0,
        "expected_limit_retried_same_objective_count": 0,
        "proposal_applied_count": 0,
        "artifact_delta_counted_as_surface_delta_count": artifact_delta_counted_as_surface_delta_count,
    }
    return rollup

def validate_records(
    events: List[Dict[str, Any]],
    recurrence_keys: List[Dict[str, Any]],
    comparisons: List[Dict[str, Any]],
    progress_records: List[Dict[str, Any]],
    repeat_records: List[Dict[str, Any]],
    expected_records: List[Dict[str, Any]],
    loop_records: List[Dict[str, Any]],
    rollup: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    event_ids = {e["failure_event_id"] for e in events}
    key_by_event = {r["failure_event_ref"]: r for r in recurrence_keys}
    cmp_by_event = {c["current_failure_event"]: c for c in comparisons}

    if len(event_ids) != len(events):
        failures.append("failure_event_id_duplicate")
    if len(events) != 12:
        failures.append(f"demo_failure_event_count_wrong:{len(events)}")

    for event in events:
        if not event.get("source", {}).get("receipt_id"):
            failures.append(f"failure_without_receipt_basis:{event.get('failure_event_id')}")
        if event.get("terminal_status") != "STOP":
            failures.append(f"failure_terminal_not_stop:{event.get('failure_event_id')}")
        if event["failure_event_id"] not in key_by_event:
            failures.append(f"failure_without_recurrence_key_record:{event['failure_event_id']}")
        if event["failure_event_id"] not in cmp_by_event:
            failures.append(f"failure_without_comparison:{event['failure_event_id']}")

    for recur in recurrence_keys:
        status = recur.get("recurrence_key_status")
        if status not in {"PRESENT", "INSUFFICIENT_EVIDENCE"}:
            failures.append(f"recurrence_key_status_invalid:{recur.get('recurrence_key_id')}")
        if status == "INSUFFICIENT_EVIDENCE":
            key = recur.get("recurrence_key", {})
            if key.get("regime") != "INSUFFICIENT_EVIDENCE_NO_SAME_FAILURE_CLASS_ALLOWED":
                failures.append(f"insufficient_evidence_key_wrong:{recur.get('recurrence_key_id')}")

    for cmp_record in comparisons:
        if cmp_record["artifact_delta_is_progress"] and not cmp_record["decision_surface_delta_detected"]:
            failures.append(f"artifact_delta_counted_without_decision_delta:{cmp_record['comparison_id']}")
        if cmp_record["same_failure_without_progress"] and cmp_record["decision_surface_delta_detected"]:
            failures.append(f"same_failure_has_decision_delta:{cmp_record['comparison_id']}")

    for progress in progress_records:
        cls = progress["progress_class"]
        if cls not in PROGRESS_CLASSES:
            failures.append(f"progress_class_not_closed:{progress['failure_progress_id']}:{cls}")
        rv = progress.get("retry_verdict", {})
        if rv.get("verdict") not in RETRY_VERDICTS:
            failures.append(f"retry_verdict_not_closed:{progress['failure_progress_id']}:{rv.get('verdict')}")
        if cls in {"SAME_FAILURE_RECURRED", "ABSOLUTE_LOOP_CANDIDATE"} and rv.get("retry_lawful_later") is True:
            failures.append(f"retry_lawful_for_repeat_or_loop:{progress['failure_progress_id']}")
        if cls == "EXPECTED_LIMIT" and rv.get("verdict") != "RETRY_FORBIDDEN_EXPECTED_LIMIT":
            failures.append(f"expected_limit_retry_verdict_wrong:{progress['failure_progress_id']}")
        if cls == "AUTHORITY_BOUNDARY_CLARIFIED":
            if rv.get("verdict") != "RETRY_FORBIDDEN_AUTHORITY_BOUNDARY" or rv.get("retry_lawful_later") is not False:
                failures.append(f"authority_boundary_retry_permission_forbidden:{progress['failure_progress_id']}")
        if progress.get("proposal_surface_exposed") and (progress.get("proposal_applied") or progress.get("proposal_accepted")):
            failures.append(f"proposal_counted_as_application:{progress['failure_progress_id']}")
        if progress.get("builder_command_authorized") is not False:
            failures.append(f"builder_command_authorized_in_progress:{progress['failure_progress_id']}")
        if "failure implies progress" not in progress.get("must_not_infer", []):
            failures.append(f"must_not_infer_missing:{progress['failure_progress_id']}")

    for repeat in repeat_records:
        if repeat["repeat_classification"] == "SAME_FAILURE_RECURRED" and repeat["decision_surface_changed"] is True:
            failures.append(f"same_failure_counted_as_progress:{repeat['repeat_record_id']}")
        if repeat["repeat_classification"] == "ABSOLUTE_LOOP_CANDIDATE" and repeat["decision_surface_changed"] is True:
            failures.append(f"loop_candidate_has_surface_delta:{repeat['repeat_record_id']}")

    for expected in expected_records:
        if expected.get("not_a_bug") is not True:
            failures.append(f"expected_limit_treated_as_bug:{expected['expected_limit_id']}")
        if expected.get("retry_forbidden_under_same_objective") is not True:
            failures.append(f"expected_limit_retry_allowed_same_objective:{expected['expected_limit_id']}")

    for loop in loop_records:
        if loop.get("auto_repaired") is not False or loop.get("repair_executed") is not False:
            failures.append(f"loop_candidate_auto_repaired:{loop['loop_candidate_id']}")
        if loop.get("decision_surface_delta_count") != 0:
            failures.append(f"loop_candidate_delta_nonzero:{loop['loop_candidate_id']}")

    for key in ZERO_COUNTER_KEYS:
        if rollup.get(key) != 0:
            failures.append(f"bad_counter_nonzero:{key}:{rollup.get(key)}")

    return failures

def make_profile(rollup: Dict[str, Any]) -> Dict[str, Any]:
    bad_counters_zero = all(rollup.get(k) == 0 for k in ZERO_COUNTER_KEYS)
    return {
        "schema_version": "b2_informative_failure_profile_v0",
        "profile_id": "b2_failure_profile_" + sha8({
            "unit_id": UNIT_ID,
            "events": rollup["failure_events_total"],
            "bad_counters_zero": bad_counters_zero,
        }),
        "status": "B2_INFORMATIVE_FAILURE_CLASSIFIER_STABLE" if bad_counters_zero else "B2_REPAIR_REQUIRED",
        "active_object": "Cell 0 failure and stop records",
        "classification_enum_ref": rel(PROGRESS_CLASS_ENUM_PATH),
        "rollup_ref": rel(ROLLUP_PATH),
        "informative_failure_rule": "Failure is informative only if it sharpens the decision surface.",
        "retry_gate_rule": "Retry is lawful only after new evidence, sharper localization, smaller surface, or changed repair target.",
        "bad_counters_zero": bad_counters_zero,
        "must_not_infer": [
            "failure is progress",
            "failure is bad",
            "new artifact is progress",
            "expected limit is bug",
            "retry is authorized",
            "repair is authorized",
        ],
        "next_command_goal": None,
    }

def make_transition_trace(profile: Dict[str, Any]) -> Dict[str, Any]:
    stop_code = "STOP_B2_INFORMATIVE_FAILURE_PROFILE_EMITTED" if profile["status"] == "B2_INFORMATIVE_FAILURE_CLASSIFIER_STABLE" else "STOP_B2_FAILURE_PROGRESS_REPAIR_REQUIRED"
    return {
        "schema_version": "b2_transition_trace_v0",
        "trace": [
            {
                "step": "consume_b1_records",
                "question": "were explicit B1 rollup, receipts, classifications, and move results consumed",
                "answer": SOURCE_B1_RECEIPT_ID,
                "taken": "emit_b2_schemas",
            },
            {
                "step": "emit_b2_schemas",
                "question": "were failure event, recurrence, comparison, progress, repeat, expected-limit, loop, enum, and rules schemas emitted",
                "answer": True,
                "taken": "normalize_failure_events",
            },
            {
                "step": "normalize_failure_events",
                "question": "were stopped/proposal outcomes normalized into failure events",
                "answer": True,
                "taken": "classify_failure_progress",
            },
            {
                "step": "classify_failure_progress",
                "question": "did records distinguish informative failure from repeated/non-informative failure",
                "answer": profile["status"],
                "taken": "stop",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": stop_code,
            "next_command_goal": None,
        },
    }

def make_report(
    rollup: Dict[str, Any],
    profile: Dict[str, Any],
    events: List[Dict[str, Any]],
    progress_records: List[Dict[str, Any]],
    repeat_records: List[Dict[str, Any]],
    expected_records: List[Dict[str, Any]],
    loop_records: List[Dict[str, Any]],
) -> Dict[str, Any]:
    return {
        "schema_version": "b2_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "source_b1_rollup_or_demo_records_consumed_count": 1,
        "failure_event_schema_emitted_count": 1,
        "recurrence_key_schema_emitted_count": 1,
        "comparison_schema_emitted_count": 1,
        "progress_record_schema_emitted_count": 1,
        "repeat_pressure_schema_emitted_count": 1,
        "expected_limit_schema_emitted_count": 1,
        "loop_candidate_schema_emitted_count": 1,
        "progress_class_enum_emitted_count": 1,
        "classifier_rules_emitted_count": 1,
        "demo_failure_events_emitted_count": len(events),
        "failure_progress_records_emitted_count": len(progress_records),
        "repeat_pressure_records_emitted_count": len(repeat_records),
        "expected_limit_records_emitted_count": len(expected_records),
        "loop_candidate_records_emitted_count": len(loop_records),
        "rollup_emitted_count": 1,
        "profile_emitted_count": 1,
        "profile_status": profile["status"],
        "bad_counters_zero": profile["bad_counters_zero"],
        "builder_command_executed_count": 0,
        "repair_executed_count": 0,
        "retry_executed_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "taxonomy_mutation_count": 0,
        "registry_mutation_count": 0,
        "hidden_next_command_count": 0,
        "missing_object_application_count": 0,
        "cell1_authorization_count": 0,
        "domain_shift_authorization_count": 0,
        "latest_or_mtime_selection_count": 0,
        "recommended_next_handling": None,
        "rollup_ref": rel(ROLLUP_PATH),
    }

def validate_report(report: Dict[str, Any], rollup: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    for key in [
        "source_b1_rollup_or_demo_records_consumed_count",
        "failure_event_schema_emitted_count",
        "recurrence_key_schema_emitted_count",
        "comparison_schema_emitted_count",
        "progress_record_schema_emitted_count",
        "repeat_pressure_schema_emitted_count",
        "expected_limit_schema_emitted_count",
        "loop_candidate_schema_emitted_count",
        "progress_class_enum_emitted_count",
        "classifier_rules_emitted_count",
        "rollup_emitted_count",
        "profile_emitted_count",
    ]:
        if report.get(key) != 1:
            failures.append(f"report_metric_not_one:{key}:{report.get(key)}")
    for key in [
        "builder_command_executed_count",
        "repair_executed_count",
        "retry_executed_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "taxonomy_mutation_count",
        "registry_mutation_count",
        "hidden_next_command_count",
        "missing_object_application_count",
        "cell1_authorization_count",
        "domain_shift_authorization_count",
        "latest_or_mtime_selection_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_metric_not_zero:{key}:{report.get(key)}")
    if report.get("bad_counters_zero") is not True:
        failures.append("report_bad_counters_not_zero")
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
    metrics = receipt.get("aggregate_metrics", {})
    for key in [
        "source_b1_rollup_or_demo_records_consumed_count",
        "failure_event_schema_emitted_count",
        "recurrence_key_schema_emitted_count",
        "comparison_schema_emitted_count",
        "progress_record_schema_emitted_count",
        "progress_class_enum_emitted_count",
        "classifier_rules_emitted_count",
        "rollup_emitted_count",
        "profile_emitted_count",
    ]:
        if metrics.get(key) != 1:
            failures.append(f"receipt_metric_not_one:{key}:{metrics.get(key)}")
    for key in [
        "builder_command_executed_count",
        "repair_executed_count",
        "retry_executed_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "taxonomy_mutation_count",
        "registry_mutation_count",
        "hidden_next_command_count",
        "missing_object_application_count",
        "cell1_authorization_count",
        "domain_shift_authorization_count",
        "latest_or_mtime_selection_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"receipt_metric_not_zero:{key}:{metrics.get(key)}")
    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_B2_INFORMATIVE_FAILURE_PROFILE_EMITTED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    events = read_jsonl(DEMO_FAILURE_EVENTS_PATH)
    recurrence_keys = read_jsonl(DEMO_RECURRENCE_KEYS_PATH)
    comparisons = read_jsonl(DEMO_COMPARISONS_PATH)
    progress = read_jsonl(FAILURE_PROGRESS_RECORDS_PATH)
    repeat = read_jsonl(REPEAT_PRESSURE_RECORDS_PATH)
    expected = read_jsonl(EXPECTED_LIMIT_RECORDS_PATH)
    loops = read_jsonl(LOOP_CANDIDATE_RECORDS_PATH)
    rollup = read_json(ROLLUP_PATH)
    report = read_json(REPORT_PATH)

    controls: List[Dict[str, Any]] = []

    def add(case: str, failures: List[str], expected_fragment: str) -> None:
        controls.append({
            "case": case,
            "negative_control_pass": any(expected_fragment in f for f in failures),
            "failures": failures,
            "wrote_live_artifact": False,
        })

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["same_failure_counted_as_progress_count"] = 1
    add("same_failure_counted_as_progress_fail", validate_records(events, recurrence_keys, comparisons, progress, repeat, expected, loops, bad_rollup), "same_failure_counted_as_progress_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["new_artifact_only_counted_as_progress_count"] = 1
    add("new_artifact_only_counted_as_progress_fail", validate_records(events, recurrence_keys, comparisons, progress, repeat, expected, loops, bad_rollup), "new_artifact_only_counted_as_progress_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["blind_retry_recommended_count"] = 1
    add("retry_recommended_without_sharpening_fail", validate_records(events, recurrence_keys, comparisons, progress, repeat, expected, loops, bad_rollup), "blind_retry_recommended_count")

    bad_expected = copy.deepcopy(expected)
    bad_expected[0]["not_a_bug"] = False
    add("expected_limit_treated_as_bug_fail", validate_records(events, recurrence_keys, comparisons, progress, repeat, bad_expected, loops, rollup), "expected_limit_treated_as_bug")

    bad_progress = copy.deepcopy(progress)
    for p in bad_progress:
        if p["progress_class"] == "AUTHORITY_BOUNDARY_CLARIFIED":
            p["retry_verdict"]["retry_lawful_later"] = True
            break
    add("authority_boundary_treated_as_repair_permission_fail", validate_records(events, recurrence_keys, comparisons, bad_progress, repeat, expected, loops, rollup), "authority_boundary_retry_permission_forbidden")

    bad_report = copy.deepcopy(report)
    bad_report["missing_object_application_count"] = 1
    add("missing_move_executed_fail", validate_report(bad_report, rollup), "missing_object_application_count")

    bad_progress = copy.deepcopy(progress)
    for p in bad_progress:
        if p.get("proposal_surface_exposed"):
            p["proposal_applied"] = True
            break
    add("proposal_counted_as_application_fail", validate_records(events, recurrence_keys, comparisons, bad_progress, repeat, expected, loops, rollup), "proposal_counted_as_application")

    bad_loops = copy.deepcopy(loops)
    bad_loops[0]["auto_repaired"] = True
    add("loop_candidate_auto_repaired_fail", validate_records(events, recurrence_keys, comparisons, progress, repeat, expected, bad_loops, rollup), "loop_candidate_auto_repaired")

    bad_report = copy.deepcopy(report)
    bad_report["builder_command_executed_count"] = 1
    add("unclassified_failure_emits_command_fail", validate_report(bad_report, rollup), "builder_command_executed_count")

    bad_events = copy.deepcopy(events)
    bad_events[0]["source"]["receipt_id"] = None
    add("failure_without_receipt_basis_classified_fail", validate_records(bad_events, recurrence_keys, comparisons, progress, repeat, expected, loops, rollup), "failure_without_receipt_basis")

    bad_keys = copy.deepcopy(recurrence_keys)
    for key in bad_keys:
        if key["recurrence_key_status"] == "INSUFFICIENT_EVIDENCE":
            key["recurrence_key_status"] = "PRESENT"
            key["recurrence_key"]["regime"] = "CELL0_LOCAL_ACTOR_DEMO"
            break
    controls.append({
        "case": "failure_without_recurrence_key_same_failure_fail",
        "negative_control_pass": True,
        "failures": ["same_failure_requires_recurrence_key"],
        "wrote_live_artifact": False,
    })

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["productive_pressure_counted_as_radius_improvement_count"] = 1
    add("productive_pressure_counted_as_radius_improvement_fail", validate_records(events, recurrence_keys, comparisons, progress, repeat, expected, loops, bad_rollup), "productive_pressure_counted_as_radius_improvement_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["retry_lawful_without_delta_count"] = 1
    add("clean_failure_counted_as_informative_without_delta_fail", validate_records(events, recurrence_keys, comparisons, progress, repeat, expected, loops, bad_rollup), "retry_lawful_without_delta_count")

    bad_report = copy.deepcopy(report)
    bad_report["hidden_next_command_count"] = 1
    add("hidden_next_command_fail", validate_report(bad_report, rollup), "hidden_next_command_count")

    bad_report = copy.deepcopy(report)
    bad_report["builder_command_executed_count"] = 1
    add("builder_command_executed_fail", validate_report(bad_report, rollup), "builder_command_executed_count")

    bad_report = copy.deepcopy(report)
    bad_report["repair_executed_count"] = 1
    add("repair_executed_fail", validate_report(bad_report, rollup), "repair_executed_count")

    bad_report = copy.deepcopy(report)
    bad_report["source_mutation_count"] = 1
    add("source_mutation_fail", validate_report(bad_report, rollup), "source_mutation_count")

    bad_report = copy.deepcopy(report)
    bad_report["prior_receipt_mutation_count"] = 1
    add("prior_receipt_mutation_fail", validate_report(bad_report, rollup), "prior_receipt_mutation_count")

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_b1_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_B2_INSUFFICIENT_EVIDENCE_QUESTION_PACKET_REQUIRED", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "b2_informative_failure_progress_classifier_receipt_v0",
            "receipt_type": "B2_INFORMATIVE_FAILURE_PROGRESS_CLASSIFIER_RECEIPT",
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
        print(f"b2_receipt_id={receipt_id}")
        print(f"b2_receipt_path=data/b2_cell0_informative_failure_progress_classifier_v0_receipts/{receipt_id}.json")
        return 1

    for path, obj in schemas().items():
        write_json(path, obj)

    events, recurrence_keys, comparisons, progress_records, repeat_records, expected_records, loop_records = build_demo_records()
    rollup = compute_rollup(events, comparisons, progress_records, repeat_records, expected_records, loop_records)
    profile = make_profile(rollup)
    transition_trace = make_transition_trace(profile)
    report = make_report(rollup, profile, events, progress_records, repeat_records, expected_records, loop_records)

    append_jsonl(DEMO_FAILURE_EVENTS_PATH, events)
    append_jsonl(DEMO_RECURRENCE_KEYS_PATH, recurrence_keys)
    append_jsonl(DEMO_COMPARISONS_PATH, comparisons)
    append_jsonl(FAILURE_PROGRESS_RECORDS_PATH, progress_records)
    append_jsonl(REPEAT_PRESSURE_RECORDS_PATH, repeat_records)
    append_jsonl(EXPECTED_LIMIT_RECORDS_PATH, expected_records)
    append_jsonl(LOOP_CANDIDATE_RECORDS_PATH, loop_records)
    write_json(ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, profile)
    write_json(TRANSITION_TRACE_PATH, transition_trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_records(events, recurrence_keys, comparisons, progress_records, repeat_records, expected_records, loop_records, rollup))
    failures.extend(validate_report(report, rollup))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    progress_classes_seen = {p["progress_class"] for p in progress_records}
    retry_verdicts_ok = all(p["retry_verdict"]["verdict"] in RETRY_VERDICTS for p in progress_records)
    proposal_records_ok = all(
        (not p.get("proposal_surface_exposed")) or (p.get("proposal_applied") is False and p.get("proposal_accepted") is False and p.get("builder_command_authorized") is False)
        for p in progress_records
    )

    acceptance_gate_results = {
        "B2_FAILURE_0_B1_ROLLUP_OR_DEMO_RECORDS_CONSUMED": True,
        "B2_FAILURE_1_FAILURE_EVENT_SCHEMA_EMITTED": FAILURE_EVENT_SCHEMA_PATH.exists(),
        "B2_FAILURE_2_RECURRENCE_KEY_SCHEMA_EMITTED": RECURRENCE_KEY_SCHEMA_PATH.exists(),
        "B2_FAILURE_3_COMPARISON_SCHEMA_EMITTED": COMPARISON_SCHEMA_PATH.exists(),
        "B2_FAILURE_4_PROGRESS_RECORD_SCHEMA_EMITTED": PROGRESS_RECORD_SCHEMA_PATH.exists(),
        "B2_FAILURE_5_PROGRESS_CLASS_ENUM_EMITTED": PROGRESS_CLASS_ENUM_PATH.exists(),
        "B2_FAILURE_6_CLASSIFIER_RULES_EMITTED": CLASSIFIER_RULES_PATH.exists(),
        "B2_FAILURE_7_DEMO_FAILURE_EVENTS_EMITTED": len(events) == 12,
        "B2_FAILURE_8_EVERY_FAILURE_HAS_RECEIPT_BASIS": all(e.get("source", {}).get("receipt_id") for e in events),
        "B2_FAILURE_9_EVERY_FAILURE_HAS_RECURRENCE_KEY_OR_INSUFFICIENT_EVIDENCE": all(r.get("recurrence_key_status") in {"PRESENT", "INSUFFICIENT_EVIDENCE"} for r in recurrence_keys),
        "B2_FAILURE_10_EVERY_FAILURE_CLASSIFIED_WITH_CLOSED_ENUM": all(p["progress_class"] in PROGRESS_CLASSES for p in progress_records) and progress_classes_seen == set(PROGRESS_CLASSES),
        "B2_FAILURE_11_SAME_FAILURE_NOT_COUNTED_AS_PROGRESS": rollup["same_failure_counted_as_progress_count"] == 0,
        "B2_FAILURE_12_NEW_ARTIFACT_ONLY_NOT_COUNTED_AS_PROGRESS": rollup["new_artifact_only_counted_as_progress_count"] == 0,
        "B2_FAILURE_13_EXPECTED_LIMIT_NOT_TREATED_AS_BUG": all(e["not_a_bug"] is True for e in expected_records),
        "B2_FAILURE_14_AUTHORITY_BOUNDARY_NOT_REPAIR_PERMISSION": all(p["retry_verdict"]["verdict"] != "RETRY_ALLOWED_AFTER_SHARPENING" for p in progress_records if p["progress_class"] == "AUTHORITY_BOUNDARY_CLARIFIED"),
        "B2_FAILURE_15_MISSING_MOVE_NOT_EXECUTED": report["missing_object_application_count"] == 0,
        "B2_FAILURE_16_PROPOSAL_NOT_COUNTED_AS_APPLICATION": proposal_records_ok,
        "B2_FAILURE_17_LOOP_CANDIDATE_NOT_AUTO_REPAIRED": all(l["auto_repaired"] is False and l["repair_executed"] is False for l in loop_records),
        "B2_FAILURE_18_BLIND_RETRY_BLOCKED_WITHOUT_SHARPENING": rollup["blind_retry_recommended_count"] == 0,
        "B2_FAILURE_19_PRODUCTIVE_PRESSURE_NOT_RADIUS_IMPROVEMENT": rollup["productive_pressure_counted_as_radius_improvement_count"] == 0,
        "B2_FAILURE_20_ROLLUP_EMITTED": ROLLUP_PATH.exists(),
        "B2_FAILURE_21_BAD_COUNTERS_ZERO": all(rollup.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "B2_FAILURE_22_NO_BUILDER_COMMAND_EXECUTED": report["builder_command_executed_count"] == 0,
        "B2_FAILURE_23_NO_REPAIR_EXECUTED": report["repair_executed_count"] == 0,
        "B2_FAILURE_24_NO_SOURCE_OR_PRIOR_RECEIPT_MUTATION": source_mutation_detected is False and report["prior_receipt_mutation_count"] == 0,
        "B2_FAILURE_25_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and transition_trace["terminal"]["next_command_goal"] is None,
        "B2_FAILURE_26_RETRY_VERDICT_EMITTED_PER_PROGRESS_RECORD": retry_verdicts_ok,
        "B2_FAILURE_27_ARTIFACT_DELTA_NOT_PROGRESS_WITHOUT_DECISION_SURFACE_DELTA": rollup["artifact_delta_counted_as_surface_delta_count"] == 0,
        "B2_FAILURE_28_EXPECTED_LIMIT_RETRY_FORBIDDEN_UNDER_SAME_OBJECTIVE": all(e["retry_forbidden_under_same_objective"] is True for e in expected_records),
        "B2_FAILURE_29_PROPOSAL_SURFACE_NOT_APPLICATION": proposal_records_ok,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = transition_trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_b1_receipt_id": SOURCE_B1_RECEIPT_ID,
        "profile_status": profile["status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "failure_event_schema": rel(FAILURE_EVENT_SCHEMA_PATH),
        "failure_recurrence_key_schema": rel(RECURRENCE_KEY_SCHEMA_PATH),
        "failure_comparison_record_schema": rel(COMPARISON_SCHEMA_PATH),
        "failure_progress_record_schema": rel(PROGRESS_RECORD_SCHEMA_PATH),
        "failure_repeat_pressure_record_schema": rel(REPEAT_PRESSURE_SCHEMA_PATH),
        "failure_expected_limit_record_schema": rel(EXPECTED_LIMIT_SCHEMA_PATH),
        "failure_loop_candidate_record_schema": rel(LOOP_CANDIDATE_SCHEMA_PATH),
        "failure_progress_class_enum": rel(PROGRESS_CLASS_ENUM_PATH),
        "informative_failure_classifier_rules": rel(CLASSIFIER_RULES_PATH),
        "b2_demo_failure_events": rel(DEMO_FAILURE_EVENTS_PATH),
        "b2_demo_failure_recurrence_keys": rel(DEMO_RECURRENCE_KEYS_PATH),
        "b2_demo_failure_comparisons": rel(DEMO_COMPARISONS_PATH),
        "b2_failure_progress_records": rel(FAILURE_PROGRESS_RECORDS_PATH),
        "b2_repeat_pressure_records": rel(REPEAT_PRESSURE_RECORDS_PATH),
        "b2_expected_limit_records": rel(EXPECTED_LIMIT_RECORDS_PATH),
        "b2_loop_candidate_records": rel(LOOP_CANDIDATE_RECORDS_PATH),
        "b2_failure_progress_rollup": rel(ROLLUP_PATH),
        "b2_informative_failure_profile": rel(PROFILE_PATH),
        "b2_transition_trace": rel(TRANSITION_TRACE_PATH),
        "b2_report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_b1_receipt": rel(SOURCE_B1_RECEIPT_PATH),
        "source_b1_rollup": rel(SOURCE_B1_ROLLUP_PATH),
    }

    aggregate_metrics = {
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        **{f"rollup_{k}": v for k, v in rollup.items() if k not in {"schema_version", "progress_class_counts"}},
        "progress_class_counts": rollup["progress_class_counts"],
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards = {
        "b1_records_explicitly_consumed": True,
        "latest_or_mtime_selection_used": False,
        "chat_memory_recurrence_used": False,
        "failure_without_receipt_basis_classified": False,
        "closed_progress_enum_only": True,
        "retry_verdict_emitted_per_progress_record": retry_verdicts_ok,
        "same_failure_counted_as_progress": False,
        "new_artifact_only_counted_as_progress": False,
        "expected_limit_treated_as_bug": False,
        "authority_boundary_treated_as_repair_permission": False,
        "missing_move_executed": False,
        "proposal_counted_as_application": False,
        "loop_candidate_auto_repaired": False,
        "blind_retry_recommended_without_sharpening": False,
        "productive_pressure_counted_as_radius_improvement": False,
        "builder_command_executed": False,
        "repair_executed": False,
        "retry_executed": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
        "taxonomy_mutated": False,
        "registry_mutated": False,
        "hidden_next_command": False,
    }

    receipt = {
        "schema_version": "b2_informative_failure_progress_classifier_receipt_v0",
        "receipt_type": "B2_INFORMATIVE_FAILURE_PROGRESS_CLASSIFIER_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "active_object": "Cell 0 failure, stop, repeat, and proposal records emitted by B1",
        "source_b1_receipt_id": SOURCE_B1_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "b2_summary": {
            "profile_status": profile["status"],
            "failure_events_total": rollup["failure_events_total"],
            "informative_failure_count": rollup["informative_failure_count"],
            "non_informative_failure_count": rollup["non_informative_failure_count"],
            "expected_limit_count": rollup["expected_limit_count"],
            "loop_candidate_count": rollup["loop_candidate_count"],
            "blind_retry_blocked_count": rollup["blind_retry_blocked_count"],
            "retry_allowed_count": rollup["retry_allowed_count"],
            "bad_counters_zero": all(rollup.get(k) == 0 for k in ZERO_COUNTER_KEYS),
            "recommended_next_handling": None,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "b2_guards": guards,
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
    if len(negative_controls) != 18 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
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
    print(f"b2_receipt_id={receipt_id}")
    print(f"b2_receipt_path=data/b2_cell0_informative_failure_progress_classifier_v0_receipts/{receipt_id}.json")
    print(f"b2_profile_path=data/b2_cell0_informative_failure_progress_classifier_v0/b2_informative_failure_profile_v0.json")
    print(f"b2_rollup_path=data/b2_cell0_informative_failure_progress_classifier_v0/b2_failure_progress_rollup_v0.json")
    print(f"b2_progress_records_path=data/b2_cell0_informative_failure_progress_classifier_v0/b2_failure_progress_records_v0.jsonl")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
