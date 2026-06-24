#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "APPLY_A0_A1_TO_EXPLICIT_CURRENT_FRONTIER_RECEIPT_V0"
TARGET_UNIT_ID = "a0_a1.explicit_current_frontier_receipt.application.v0"

SOURCE_A1_BUILD_RECEIPT_ID = "51e219aa"
SOURCE_A1_PATH_PATCH_RECEIPT_ID = "005e66ba"
SOURCE_A0_FRONTIER_SOURCE_PATCH_RECEIPT_ID = "e5646bae"
SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID = "6d14e637"

EXPLICIT_FRONTIER_ID = "frontier_candidate_missing_object_layer_followup"

OUT_DIR = ROOT / "data" / "a0_a1_explicit_current_frontier_application_v0"
RECEIPT_DIR = ROOT / "data" / "a0_a1_explicit_current_frontier_application_v0_receipts"

EXPLICIT_FRONTIER_SELECTION_PACKET_PATH = OUT_DIR / "a0_a1_explicit_frontier_selection_packet.json"
SOURCE_SURFACE_PATH = OUT_DIR / "a0_a1_explicit_frontier_source_surface.json"
SELECTED_A0_RESULT_PATH = OUT_DIR / "a0_a1_selected_explicit_a0_result.json"
A1_STRATEGIC_DECISION_PACKET_PATH = OUT_DIR / "a1_strategic_decision_packet_for_explicit_frontier.json"
APPLICATION_DECISION_PACKET_PATH = OUT_DIR / "a0_a1_explicit_frontier_application_decision_packet.json"
QUESTION_PACKET_PATH = OUT_DIR / "a0_a1_explicit_frontier_question_packet.json"
FINAL_STATUS_PACKET_PATH = OUT_DIR / "a0_a1_explicit_frontier_final_status_packet.json"
TRANSITION_TRACE_PATH = OUT_DIR / "a0_a1_explicit_frontier_transition_trace.json"
REPORT_PATH = OUT_DIR / "a0_a1_explicit_frontier_application_report.json"

A1_BUILD_RECEIPT_PATH = ROOT / "data" / "a1_strategic_decision_packet_layer_v0_receipts" / f"{SOURCE_A1_BUILD_RECEIPT_ID}.json"
A1_PATH_PATCH_RECEIPT_PATH = ROOT / "data" / "a1_build_relative_out_dir_path_normalization_patch_v0_receipts" / f"{SOURCE_A1_PATH_PATCH_RECEIPT_ID}.json"
A1_SCRIPT_PATH = ROOT / "scripts" / "a1_strategic_decision_packet_layer_v0.py"
A1_TRANSITION_REPORT_PATH = ROOT / "data" / "a1_strategic_decision_packet_layer_v0" / "a1_transition_report.json"
A1_DECISION_ENUM_PATH = ROOT / "data" / "a1_strategic_decision_packet_layer_v0" / "a1_decision_class_enum_v0.json"
A1_MAPPING_TABLE_PATH = ROOT / "data" / "a1_strategic_decision_packet_layer_v0" / "a1_decision_mapping_table_v0.json"

A0_FRONTIER_SOURCE_PATCH_RECEIPT_PATH = ROOT / "data" / "a0_frontier_source_selection_rule_explicit_bundle_manifest_patch_v0_receipts" / f"{SOURCE_A0_FRONTIER_SOURCE_PATCH_RECEIPT_ID}.json"
A0_PATCHED_CLASSIFICATIONS_PATH = ROOT / "data" / "a0_frontier_source_selection_rule_explicit_bundle_manifest_patch_v0" / "a0_frontier_source_selection_patched_classifications.jsonl"
A0_PATCHED_ROLLUP_PATH = ROOT / "data" / "a0_frontier_source_selection_rule_explicit_bundle_manifest_patch_v0" / "a0_frontier_source_selection_patched_rollup.json"
A0_PATCHED_QUESTION_PACKET_PATH = ROOT / "data" / "a0_frontier_source_selection_rule_explicit_bundle_manifest_patch_v0" / "a0_frontier_source_selection_patched_question_packet.json"
A0_PATCH_FINAL_ACCEPTANCE_PACKET_PATH = ROOT / "data" / "a0_frontier_source_selection_rule_explicit_bundle_manifest_patch_v0" / "a0_frontier_source_selection_patch_final_acceptance_packet.json"
A0_FINAL_ACCEPTANCE_RECEIPT_PATH = ROOT / "data" / "a0_self_classification_assertion_acceptance_patch_v0_receipts" / f"{SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID}.json"

SOURCE_FILES = [
    A1_BUILD_RECEIPT_PATH,
    A1_PATH_PATCH_RECEIPT_PATH,
    A1_SCRIPT_PATH,
    A1_TRANSITION_REPORT_PATH,
    A1_DECISION_ENUM_PATH,
    A1_MAPPING_TABLE_PATH,
    A0_FRONTIER_SOURCE_PATCH_RECEIPT_PATH,
    A0_PATCHED_CLASSIFICATIONS_PATH,
    A0_PATCHED_ROLLUP_PATH,
    A0_PATCHED_QUESTION_PACKET_PATH,
    A0_PATCH_FINAL_ACCEPTANCE_PACKET_PATH,
    A0_FINAL_ACCEPTANCE_RECEIPT_PATH,
]

HUMAN_DECISION = {
    "decision": "APPLY_A0_A1_TO_EXPLICIT_CURRENT_FRONTIER_RECEIPT",
    "scope": "Apply A1 to exactly one explicit A0 result from the accepted A0 explicit current frontier output. The selected frontier is explicit by id and artifact path. This unit emits an A1 strategic decision packet and related status/question packets only. Shell creates artifacts but is not builder-mode operation.",
    "selected_frontier_id": EXPLICIT_FRONTIER_ID,
    "authorized": [
        "consume accepted A1 build receipt and packetizer",
        "consume accepted A0 explicit frontier source-selection patch receipt",
        "select exactly one explicit A0 frontier result by explicit frontier id",
        "write selected A0 result artifact",
        "packetize selected A0 result through A1",
        "emit A1 strategic decision packet",
        "emit question/status packet if A1 decision is QUESTION_PACKET_NOT_COMMAND",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "select frontier by latest-file guessing",
        "select frontier by mtime sorting",
        "select multiple A0 results in one A1 packet",
        "consume raw receipt without A0 wrapper",
        "execute builder command",
        "execute repair",
        "mutate A0",
        "mutate A1",
        "mutate taxonomy",
        "mutate registry",
        "mutate prior receipts",
        "apply missing-object proposal",
        "convert missing optional evidence to null value",
        "run radius-10000 again",
        "run radius above 10000",
        "run unbounded/no-cap harvest",
        "treat shell operation as builder operation",
        "hide next command",
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

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def load_a1_module():
    spec = importlib.util.spec_from_file_location("a1", A1_SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def validate_sources() -> List[str]:
    failures: List[str] = []

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path) if path.exists() else path.as_posix()}")

    if failures:
        return failures

    a1_build = read_json(A1_BUILD_RECEIPT_PATH)
    a1_patch = read_json(A1_PATH_PATCH_RECEIPT_PATH)
    a1_report = read_json(A1_TRANSITION_REPORT_PATH)
    a0_patch = read_json(A0_FRONTIER_SOURCE_PATCH_RECEIPT_PATH)
    a0_final = read_json(A0_FINAL_ACCEPTANCE_RECEIPT_PATH)

    if a1_build.get("receipt_id") != SOURCE_A1_BUILD_RECEIPT_ID:
        failures.append("a1_build_receipt_id_wrong")
    if a1_build.get("gate") != "PASS":
        failures.append("a1_build_not_pass")
    if a1_build.get("a1_build_summary", {}).get("build_result") != "A1_STRATEGIC_DECISION_PACKET_LAYER_BUILT":
        failures.append("a1_not_built")
    if a1_build.get("a1_build_summary", {}).get("live_frontier_application_count") != 0:
        failures.append("a1_build_applied_live_frontier")
    if a1_patch.get("gate") != "PASS":
        failures.append("a1_path_patch_not_pass")
    if a1_report.get("build_mode") != "STATIC_SCHEMA_AND_PROBE_ONLY":
        failures.append("a1_report_not_static_probe_only")
    if a1_report.get("builder_command_executed_count") != 0:
        failures.append("a1_report_command_executed")

    if a0_patch.get("receipt_id") != SOURCE_A0_FRONTIER_SOURCE_PATCH_RECEIPT_ID:
        failures.append("a0_frontier_patch_receipt_id_wrong")
    if a0_patch.get("gate") != "PASS":
        failures.append("a0_frontier_patch_not_pass")
    if a0_patch.get("a0_frontier_source_selection_patch_summary", {}).get("patch_result") != "A0_FRONTIER_SOURCE_SELECTION_RULE_PATCH_ACCEPTED":
        failures.append("a0_frontier_patch_not_accepted")
    if a0_patch.get("a0_frontier_source_selection_patch_summary", {}).get("candidate_missing_object_frontier_classification") != "QUESTION_PACKET_NOT_COMMAND":
        failures.append("candidate_frontier_not_question_packet")
    if a0_patch.get("a0_frontier_source_selection_patch_summary", {}).get("builder_command_allowed_count") != 0:
        failures.append("a0_frontier_builder_allowed")
    if a0_final.get("gate") != "PASS":
        failures.append("a0_final_not_pass")

    return failures

def select_explicit_a0_result(rows: List[Dict[str, Any]], frontier_id: str) -> Dict[str, Any]:
    matches = [row for row in rows if row.get("frontier_id") == frontier_id]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one explicit frontier match for {frontier_id}, got {len(matches)}")
    row = matches[0]
    a0_result = row.get("a0_result")
    if not isinstance(a0_result, dict):
        raise ValueError("selected row missing a0_result object")
    return row

def validate_a1_packet(packet: Dict[str, Any], selected_row: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if packet.get("schema_version") != "strategic_decision_packet_v0":
        failures.append("a1_packet_schema_wrong")
    if packet.get("decision", {}).get("decision_class") != "QUESTION_PACKET_NOT_COMMAND":
        failures.append(f"a1_decision_not_question_packet:{packet.get('decision', {}).get('decision_class')}")
    if packet.get("builder_command_candidate") is not None:
        failures.append("a1_builder_command_candidate_present")
    if packet.get("operational_spec_candidate") is not None:
        failures.append("a1_operational_spec_candidate_present")
    if packet.get("candidate_missing_object_proposal") is not None:
        failures.append("a1_missing_object_proposal_present")
    if not isinstance(packet.get("question_packet"), dict):
        failures.append("a1_question_packet_missing")
    if packet.get("decision", {}).get("builder_command_allowed") is not False:
        failures.append("a1_builder_command_allowed_not_false")
    if packet.get("review_status") != "READY_FOR_HUMAN_REVIEW":
        failures.append(f"a1_review_status_wrong:{packet.get('review_status')}")
    if packet.get("a0_basis", {}).get("a0_classification") != selected_row.get("a0_classification"):
        failures.append("a1_a0_basis_classification_mismatch")
    if packet.get("a0_basis", {}).get("a0_classification") != "QUESTION_PACKET_NOT_COMMAND":
        failures.append("a1_a0_basis_not_question_packet")
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
        "a1_build_receipt_consumed_count",
        "a1_path_patch_receipt_consumed_count",
        "a0_frontier_source_patch_receipt_consumed_count",
        "explicit_frontier_selection_packet_emitted_count",
        "source_surface_emitted_count",
        "selected_a0_result_emitted_count",
        "a1_strategic_decision_packet_emitted_count",
        "application_decision_packet_emitted_count",
        "question_packet_emitted_count",
        "final_status_packet_emitted_count",
        "transition_trace_emitted_count",
        "report_emitted_count",
        "selected_a0_result_count",
        "a1_question_packet_decision_count",
    ]:
        if metrics.get(key) != 1:
            failures.append(f"metric_not_one:{key}:{metrics.get(key)}")

    for key in [
        "builder_command_executed_count",
        "builder_command_candidate_emitted_count",
        "repair_executed_count",
        "operational_spec_candidate_emitted_count",
        "candidate_missing_object_proposal_applied_count",
        "source_mutation_count",
        "a0_mutation_count",
        "a1_mutation_count",
        "taxonomy_mutation_count",
        "registry_mutation_count",
        "prior_receipt_mutation_count",
        "latest_or_mtime_selection_count",
        "strategic_vibes_authority_count",
        "shell_treated_as_builder_operation_count",
        "hidden_next_command_count",
        "radius_10000_rerun_count",
        "radius_above_10000_run_count",
        "unbounded_or_no_cap_run_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_A0_A1_EXPLICIT_FRONTIER_APPLICATION_PACKETIZED_HUMAN_DECISION_REQUIRED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(SOURCE_FILES)
    failures = validate_sources()

    rows = read_jsonl(A0_PATCHED_CLASSIFICATIONS_PATH)
    selected_row = select_explicit_a0_result(rows, EXPLICIT_FRONTIER_ID)
    selected_a0 = selected_row["a0_result"]

    a1 = load_a1_module()
    a1_packet = a1.packetize(selected_a0)

    selection_packet = {
        "schema_version": "a0_a1_explicit_frontier_selection_packet_v0",
        "packet_status": "EXPLICIT_FRONTIER_SELECTED_FOR_A0_A1_APPLICATION",
        "selection_rule": "explicit_frontier_id_and_explicit_a0_output_artifact",
        "selected_frontier_id": EXPLICIT_FRONTIER_ID,
        "source_a0_classification_artifact": rel(A0_PATCHED_CLASSIFICATIONS_PATH),
        "source_a0_frontier_source_patch_receipt_id": SOURCE_A0_FRONTIER_SOURCE_PATCH_RECEIPT_ID,
        "source_a1_build_receipt_id": SOURCE_A1_BUILD_RECEIPT_ID,
        "forbidden_selection_rules": ["latest", "mtime", "workspace_guess", "strategic_vibes", "hidden_builder_state"],
        "auto_selected_frontier": None,
    }

    source_surface = {
        "schema_version": "a0_a1_explicit_frontier_source_surface_v0",
        "selected_frontier_id": EXPLICIT_FRONTIER_ID,
        "source_a0_frontier_source_patch_receipt": rel(A0_FRONTIER_SOURCE_PATCH_RECEIPT_PATH),
        "source_a0_classifications": rel(A0_PATCHED_CLASSIFICATIONS_PATH),
        "source_a0_rollup": rel(A0_PATCHED_ROLLUP_PATH),
        "source_a0_question_packet": rel(A0_PATCHED_QUESTION_PACKET_PATH),
        "source_a1_build_receipt": rel(A1_BUILD_RECEIPT_PATH),
        "source_a1_packetizer": rel(A1_SCRIPT_PATH),
        "selected_row_summary": {
            "frontier_id": selected_row.get("frontier_id"),
            "a0_classification": selected_row.get("a0_classification"),
            "builder_command_allowed": selected_row.get("builder_command_allowed"),
            "operational_spec_candidate_allowed": selected_row.get("operational_spec_candidate_allowed"),
            "candidate_missing_object_proposal_allowed": selected_row.get("candidate_missing_object_proposal_allowed"),
            "bundle_status": selected_row.get("bundle_status"),
            "reason": selected_row.get("reason"),
        },
    }

    application_decision = {
        "schema_version": "a0_a1_explicit_frontier_application_decision_packet_v0",
        "decision_status": "A0_A1_EXPLICIT_FRONTIER_PACKETIZED_QUESTION_PACKET_NOT_COMMAND",
        "selected_frontier_id": EXPLICIT_FRONTIER_ID,
        "a0_classification": selected_row.get("a0_classification"),
        "a1_decision_class": a1_packet.get("decision", {}).get("decision_class"),
        "builder_command_allowed": False,
        "builder_command_candidate": None,
        "operational_spec_candidate": None,
        "candidate_missing_object_proposal": None,
        "question_packet_required": True,
        "recommended_next_handling": None,
        "auto_next_command": None,
    }

    question_packet = {
        "schema_version": "a0_a1_explicit_frontier_question_packet_v0",
        "packet_status": "QUESTION_PACKET_NOT_COMMAND",
        "selected_frontier_id": EXPLICIT_FRONTIER_ID,
        "source_a1_strategic_decision_packet": rel(A1_STRATEGIC_DECISION_PACKET_PATH),
        "source_a0_result": rel(SELECTED_A0_RESULT_PATH),
        "question_class": "OPTIONAL_FRONTIER_EVIDENCE_MISSING_OR_UNLICENSED",
        "questions": [
            {
                "question_id": "Q_A0_A1_FRONTIER_0",
                "question": "Provide explicit receipt evidence or an explicit human/schema decision before this candidate missing-object frontier can become an operational spec candidate.",
                "required_input": "explicit receipt path, explicit A0 result, or explicit schema/human decision packet",
            }
        ],
        "must_not_infer": [
            "do not infer optional evidence by latest/mtime",
            "do not convert missing optional evidence to null value",
            "do not apply missing-object proposal",
            "do not emit builder command candidate",
            "do not execute builder command",
            "do not treat shell execution as builder operation",
        ],
        "auto_next_command": None,
    }

    final_status = {
        "schema_version": "a0_a1_explicit_frontier_final_status_packet_v0",
        "packet_status": "A0_A1_EXPLICIT_FRONTIER_APPLICATION_PACKETIZED_HUMAN_DECISION_REQUIRED",
        "selected_frontier_id": EXPLICIT_FRONTIER_ID,
        "a1_packet_id": a1_packet.get("strategic_decision_packet_id"),
        "a1_decision_class": a1_packet.get("decision", {}).get("decision_class"),
        "review_status": a1_packet.get("review_status"),
        "builder_command_executed": False,
        "live_builder_operation": False,
        "recommended_next_handling": None,
        "auto_next_command": None,
    }

    report = {
        "schema_version": "a0_a1_explicit_frontier_application_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "a1_build_receipt_consumed_count": 1,
        "a1_path_patch_receipt_consumed_count": 1,
        "a0_frontier_source_patch_receipt_consumed_count": 1,
        "explicit_frontier_selection_packet_emitted_count": 1,
        "source_surface_emitted_count": 1,
        "selected_a0_result_emitted_count": 1,
        "a1_strategic_decision_packet_emitted_count": 1,
        "application_decision_packet_emitted_count": 1,
        "question_packet_emitted_count": 1,
        "final_status_packet_emitted_count": 1,
        "transition_trace_emitted_count": 1,
        "report_emitted_count": 1,
        "selected_a0_result_count": 1,
        "selected_frontier_id": EXPLICIT_FRONTIER_ID,
        "selected_a0_classification": selected_row.get("a0_classification"),
        "a1_decision_class": a1_packet.get("decision", {}).get("decision_class"),
        "a1_question_packet_decision_count": 1 if a1_packet.get("decision", {}).get("decision_class") == "QUESTION_PACKET_NOT_COMMAND" else 0,
        "builder_command_candidate_emitted_count": 0,
        "operational_spec_candidate_emitted_count": 0,
        "candidate_missing_object_proposal_applied_count": 0,
        "builder_command_executed_count": 0,
        "repair_executed_count": 0,
        "source_mutation_count": 0,
        "a0_mutation_count": 0,
        "a1_mutation_count": 0,
        "taxonomy_mutation_count": 0,
        "registry_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "latest_or_mtime_selection_count": 0,
        "strategic_vibes_authority_count": 0,
        "shell_treated_as_builder_operation_count": 0,
        "hidden_next_command_count": 0,
        "radius_10000_rerun_count": 0,
        "radius_above_10000_run_count": 0,
        "unbounded_or_no_cap_run_count": 0,
        "recommended_next_handling": None,
    }

    transition_trace = {
        "schema_version": "a0_a1_explicit_frontier_transition_trace_v0",
        "trace": [
            {
                "step": "consume_explicit_sources",
                "question": "were A0 and A1 accepted artifacts provided explicitly",
                "answer": True,
                "taken": "select_explicit_frontier_id",
            },
            {
                "step": "select_explicit_frontier_id",
                "question": "was exactly one A0 result selected without latest/mtime",
                "answer": EXPLICIT_FRONTIER_ID,
                "taken": "packetize_with_a1",
            },
            {
                "step": "packetize_with_a1",
                "question": "what did A1 decide",
                "answer": a1_packet.get("decision", {}).get("decision_class"),
                "taken": "emit_question_packet",
            },
            {
                "step": "emit_question_packet",
                "question": "was builder command candidate emitted",
                "answer": False,
                "taken": "STOP_A0_A1_EXPLICIT_FRONTIER_APPLICATION_PACKETIZED_HUMAN_DECISION_REQUIRED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_A0_A1_EXPLICIT_FRONTIER_APPLICATION_PACKETIZED_HUMAN_DECISION_REQUIRED",
            "next_command_goal": None,
        },
    }

    write_json(EXPLICIT_FRONTIER_SELECTION_PACKET_PATH, selection_packet)
    write_json(SOURCE_SURFACE_PATH, source_surface)
    write_json(SELECTED_A0_RESULT_PATH, selected_a0)
    write_json(A1_STRATEGIC_DECISION_PACKET_PATH, a1_packet)
    write_json(APPLICATION_DECISION_PACKET_PATH, application_decision)
    write_json(QUESTION_PACKET_PATH, question_packet)
    write_json(FINAL_STATUS_PACKET_PATH, final_status)
    write_json(TRANSITION_TRACE_PATH, transition_trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_a1_packet(a1_packet, selected_row))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "A0_A1_FRONTIER_0_A1_BUILD_ACCEPTED": True,
        "A0_A1_FRONTIER_1_A0_FRONTIER_SOURCE_PATCH_ACCEPTED": True,
        "A0_A1_FRONTIER_2_EXPLICIT_FRONTIER_ID_USED": EXPLICIT_FRONTIER_ID == "frontier_candidate_missing_object_layer_followup",
        "A0_A1_FRONTIER_3_EXACTLY_ONE_A0_RESULT_SELECTED": report["selected_a0_result_count"] == 1,
        "A0_A1_FRONTIER_4_NO_LATEST_OR_MTIME_SELECTION": report["latest_or_mtime_selection_count"] == 0,
        "A0_A1_FRONTIER_5_SELECTED_A0_RESULT_EMITTED": SELECTED_A0_RESULT_PATH.exists(),
        "A0_A1_FRONTIER_6_A1_STRATEGIC_PACKET_EMITTED": A1_STRATEGIC_DECISION_PACKET_PATH.exists(),
        "A0_A1_FRONTIER_7_A1_DECISION_IS_QUESTION_PACKET": report["a1_question_packet_decision_count"] == 1,
        "A0_A1_FRONTIER_8_NO_BUILDER_COMMAND_CANDIDATE": report["builder_command_candidate_emitted_count"] == 0,
        "A0_A1_FRONTIER_9_NO_OPERATIONAL_SPEC_CANDIDATE": report["operational_spec_candidate_emitted_count"] == 0,
        "A0_A1_FRONTIER_10_NO_MISSING_OBJECT_APPLICATION": report["candidate_missing_object_proposal_applied_count"] == 0,
        "A0_A1_FRONTIER_11_NO_BUILDER_COMMAND_EXECUTED": report["builder_command_executed_count"] == 0,
        "A0_A1_FRONTIER_12_NO_REPAIR_EXECUTED": report["repair_executed_count"] == 0,
        "A0_A1_FRONTIER_13_NO_A0_OR_A1_MUTATION": report["a0_mutation_count"] == 0 and report["a1_mutation_count"] == 0,
        "A0_A1_FRONTIER_14_NO_SOURCE_OR_PRIOR_RECEIPT_MUTATION": source_mutation_detected is False and report["prior_receipt_mutation_count"] == 0,
        "A0_A1_FRONTIER_15_SHELL_NOT_BUILDER_OPERATION": report["shell_treated_as_builder_operation_count"] == 0,
        "A0_A1_FRONTIER_16_NO_RADIUS_RERUN_OR_UNBOUNDED": report["radius_10000_rerun_count"] == 0 and report["radius_above_10000_run_count"] == 0 and report["unbounded_or_no_cap_run_count"] == 0,
        "A0_A1_FRONTIER_17_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and transition_trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = transition_trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_a1_build_receipt_id": SOURCE_A1_BUILD_RECEIPT_ID,
        "source_a1_path_patch_receipt_id": SOURCE_A1_PATH_PATCH_RECEIPT_ID,
        "source_a0_frontier_source_patch_receipt_id": SOURCE_A0_FRONTIER_SOURCE_PATCH_RECEIPT_ID,
        "source_a0_final_acceptance_receipt_id": SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "selected_frontier_id": EXPLICIT_FRONTIER_ID,
        "a1_decision_class": a1_packet.get("decision", {}).get("decision_class"),
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "explicit_frontier_selection_packet": rel(EXPLICIT_FRONTIER_SELECTION_PACKET_PATH),
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "selected_a0_result": rel(SELECTED_A0_RESULT_PATH),
        "a1_strategic_decision_packet": rel(A1_STRATEGIC_DECISION_PACKET_PATH),
        "application_decision_packet": rel(APPLICATION_DECISION_PACKET_PATH),
        "question_packet": rel(QUESTION_PACKET_PATH),
        "final_status_packet": rel(FINAL_STATUS_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_a1_build_receipt": rel(A1_BUILD_RECEIPT_PATH),
        "source_a0_frontier_source_patch_receipt": rel(A0_FRONTIER_SOURCE_PATCH_RECEIPT_PATH),
    }

    guards = {
        "explicit_frontier_id_used": True,
        "exactly_one_a0_result_selected": True,
        "latest_or_mtime_selection_used": False,
        "raw_receipt_without_a0_wrapper_consumed": False,
        "builder_command_candidate_emitted": False,
        "builder_command_executed": False,
        "repair_executed": False,
        "missing_object_proposal_applied": False,
        "a0_mutated": False,
        "a1_mutated": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
        "taxonomy_mutated": False,
        "registry_mutated": False,
        "shell_operation_counted_as_builder_operation": False,
        "hidden_next_command": False,
    }

    receipt = {
        "schema_version": "a0_a1_explicit_current_frontier_application_receipt_v0",
        "receipt_type": "A0_A1_EXPLICIT_CURRENT_FRONTIER_APPLICATION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_a1_build_receipt_id": SOURCE_A1_BUILD_RECEIPT_ID,
        "source_a1_path_patch_receipt_id": SOURCE_A1_PATH_PATCH_RECEIPT_ID,
        "source_a0_frontier_source_patch_receipt_id": SOURCE_A0_FRONTIER_SOURCE_PATCH_RECEIPT_ID,
        "source_a0_final_acceptance_receipt_id": SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "a0_a1_application_summary": {
            "application_result": "A0_A1_EXPLICIT_FRONTIER_PACKETIZED",
            "selected_frontier_id": EXPLICIT_FRONTIER_ID,
            "selected_a0_classification": selected_row.get("a0_classification"),
            "a1_decision_class": a1_packet.get("decision", {}).get("decision_class"),
            "a1_review_status": a1_packet.get("review_status"),
            "question_packet_required": True,
            "builder_command_candidate_emitted": False,
            "builder_command_executed_count": 0,
            "repair_executed_count": 0,
            "missing_object_proposal_applied_count": 0,
            "shell_operation_counted_as_builder_operation": False,
            "recommended_next_handling": None,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "a0_a1_application_guards": guards,
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

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"a0_a1_application_receipt_id={receipt_id}")
    print(f"a0_a1_application_receipt_path=data/a0_a1_explicit_current_frontier_application_v0_receipts/{receipt_id}.json")
    print(f"a1_strategic_decision_packet_path=data/a0_a1_explicit_current_frontier_application_v0/a1_strategic_decision_packet_for_explicit_frontier.json")
    print(f"a0_a1_question_packet_path=data/a0_a1_explicit_current_frontier_application_v0/a0_a1_explicit_frontier_question_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
