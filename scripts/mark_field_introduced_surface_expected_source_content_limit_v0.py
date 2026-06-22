#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "MARK_FIELD_INTRODUCED_SURFACE_EXPECTED_SOURCE_CONTENT_LIMIT_V0"
TARGET_UNIT_ID = "field_introduced_surface_expected_source_content_limit.v0"

SOURCE_UPSTREAM_AUDIT_RECEIPT_ID = "6b1ea913"
SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID = "11d585b6"
SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID = "8617577b"
SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID = "2d9417fc"

TOP_GROUP_KEY_HASH = "38c604a1"

OUT_DIR = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0"
RECEIPT_DIR = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0_receipts"

MARKER_PATH = OUT_DIR / "expected_source_content_limit_marker.json"
CLOSURE_RECORD_PATH = OUT_DIR / "expected_source_content_limit_closure_record.json"
DECISION_PACKET_PATH = OUT_DIR / "expected_source_content_limit_decision_packet.json"
REPORT_PATH = OUT_DIR / "expected_source_content_limit_report.json"

UPSTREAM_AUDIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_upstream_existence_audit_v0_receipts" / f"{SOURCE_UPSTREAM_AUDIT_RECEIPT_ID}.json"
UPSTREAM_AUDIT_SCOPE_PATH = ROOT / "data" / "field_introduced_surface_upstream_existence_audit_v0" / "upstream_existence_audit_scope.json"
UPSTREAM_AUDIT_LEDGER_PATH = ROOT / "data" / "field_introduced_surface_upstream_existence_audit_v0" / "upstream_existence_audit_ledger.json"
UPSTREAM_FIELD_MATRIX_PATH = ROOT / "data" / "field_introduced_surface_upstream_existence_audit_v0" / "upstream_field_existence_matrix.json"
UPSTREAM_AUDIT_CLASSIFICATION_PATH = ROOT / "data" / "field_introduced_surface_upstream_existence_audit_v0" / "upstream_existence_audit_classification.json"
UPSTREAM_AUDIT_DECISION_PACKET_PATH = ROOT / "data" / "field_introduced_surface_upstream_existence_audit_v0" / "upstream_existence_audit_decision_packet.json"
UPSTREAM_AUDIT_REPORT_PATH = ROOT / "data" / "field_introduced_surface_upstream_existence_audit_v0" / "upstream_existence_audit_report.json"

NULL_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_null_evidence_limit_classification_v0_receipts" / f"{SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID}.json"
FIELD_INTRO_RERUN_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_taxonomy_gap_missing_label_evidence_rerun_v0_receipts" / f"{SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID}.json"
FIELD_INTRO_BUILD_RECEIPT_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0_receipts" / f"{SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID}.json"

SOURCE_FILES = [
    UPSTREAM_AUDIT_RECEIPT_PATH,
    UPSTREAM_AUDIT_SCOPE_PATH,
    UPSTREAM_AUDIT_LEDGER_PATH,
    UPSTREAM_FIELD_MATRIX_PATH,
    UPSTREAM_AUDIT_CLASSIFICATION_PATH,
    UPSTREAM_AUDIT_DECISION_PACKET_PATH,
    UPSTREAM_AUDIT_REPORT_PATH,
    NULL_LIMIT_RECEIPT_PATH,
    FIELD_INTRO_RERUN_RECEIPT_PATH,
    FIELD_INTRO_BUILD_RECEIPT_PATH,
]

HUMAN_DECISION = {
    "decision": "MARK_EXPECTED_SOURCE_CONTENT_LIMIT",
    "scope": "mark the R1000 top taxonomy-gap field-introduced surface as an expected source-content limit after explicit tracked source-chain audit found no non-null upstream values",
    "source_upstream_existence_audit_receipt_id": SOURCE_UPSTREAM_AUDIT_RECEIPT_ID,
    "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
    "authorized": [
        "emit expected source-content limit marker",
        "emit closure record for this pressure branch",
        "emit decision packet documenting that no value/taxonomy repair is authorized from this branch",
    ],
    "not_authorized": [
        "inventing missing label values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "mutating source rows",
        "mutating existing receipts",
        "executing broader upstream audit",
        "executing source-provenance repair",
        "authority widening",
        "burden optimization",
        "protocol adoption",
        "next group auto-open",
        "hidden next command",
    ],
}

MUST_NOT_INFER = [
    "expected source-content limit is scoped to the explicit tracked source chain",
    "expected source-content limit does not prove universal upstream nonexistence",
    "expected source-content limit does not resolve taxonomy by creating labels",
    "expected source-content limit does not authorize value invention",
    "expected source-content limit closes this pressure branch unless a broader audit is later authorized",
    "do not mutate source rows or receipts",
    "do not auto-open next group",
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
    return path.relative_to(ROOT).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def tracked(path: Path) -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", rel(path)],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def load_sources() -> Dict[str, Any]:
    return {
        "upstream_audit_receipt": read_json(UPSTREAM_AUDIT_RECEIPT_PATH),
        "upstream_audit_scope": read_json(UPSTREAM_AUDIT_SCOPE_PATH),
        "upstream_audit_ledger": read_json(UPSTREAM_AUDIT_LEDGER_PATH),
        "upstream_field_matrix": read_json(UPSTREAM_FIELD_MATRIX_PATH),
        "upstream_audit_classification": read_json(UPSTREAM_AUDIT_CLASSIFICATION_PATH),
        "upstream_audit_decision_packet": read_json(UPSTREAM_AUDIT_DECISION_PACKET_PATH),
        "upstream_audit_report": read_json(UPSTREAM_AUDIT_REPORT_PATH),
        "null_limit_receipt": read_json(NULL_LIMIT_RECEIPT_PATH),
        "field_intro_rerun_receipt": read_json(FIELD_INTRO_RERUN_RECEIPT_PATH),
        "field_intro_build_receipt": read_json(FIELD_INTRO_BUILD_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    audit_receipt = sources["upstream_audit_receipt"]
    audit_metrics = audit_receipt.get("aggregate_metrics", {})
    audit_packet = sources["upstream_audit_decision_packet"]

    if audit_receipt.get("receipt_id") != SOURCE_UPSTREAM_AUDIT_RECEIPT_ID:
        failures.append("upstream_audit_receipt_id_wrong")
    if audit_receipt.get("gate") != "PASS":
        failures.append("upstream_audit_not_pass")
    if audit_metrics.get("classification") != "UPSTREAM_VALUES_NOT_FOUND_IN_AUDITED_CHAIN":
        failures.append("upstream_audit_classification_wrong")
    if audit_metrics.get("audited_values_found") is not False:
        failures.append("audited_values_found_unexpected")
    if audit_metrics.get("audited_non_null_value_count_total") != 0:
        failures.append("audited_non_null_values_present")
    if audit_metrics.get("all_field_values_absent_in_audited_chain") is not True:
        failures.append("audited_chain_values_not_absent")
    if audit_metrics.get("universal_upstream_nonexistence_proven") is not False:
        failures.append("universal_nonexistence_overclaimed_by_source")
    if audit_metrics.get("expected_limit_marked") is not False:
        failures.append("expected_limit_already_marked")
    if audit_packet.get("next_if_mark_expected_source_content_limit") != UNIT_ID:
        failures.append("audit_packet_mark_next_unit_wrong")
    if audit_packet.get("may_mark_expected_limit") is not False:
        failures.append("audit_packet_wrongly_authorizes_marking_itself")
    if sources["null_limit_receipt"].get("receipt_id") != SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID:
        failures.append("null_limit_receipt_id_wrong")
    if sources["field_intro_rerun_receipt"].get("receipt_id") != SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID:
        failures.append("field_intro_rerun_receipt_id_wrong")
    if sources["field_intro_build_receipt"].get("receipt_id") != SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID:
        failures.append("field_intro_build_receipt_id_wrong")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_marker(sources: Dict[str, Any]) -> Dict[str, Any]:
    audit_metrics = sources["upstream_audit_receipt"]["aggregate_metrics"]
    marker_id = sha8({
        "unit": UNIT_ID,
        "source_audit": SOURCE_UPSTREAM_AUDIT_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "mark": "EXPECTED_SOURCE_CONTENT_LIMIT",
    })
    return {
        "schema_version": "field_introduced_surface_expected_source_content_limit_marker_v0",
        "marker_id": marker_id,
        "marker_type": "EXPECTED_SOURCE_CONTENT_LIMIT",
        "source_upstream_existence_audit_receipt_id": SOURCE_UPSTREAM_AUDIT_RECEIPT_ID,
        "source_null_limit_classification_receipt_id": SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID,
        "source_field_introduced_surface_rerun_receipt_id": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
        "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "limit_scope": "explicit_tracked_source_chain_only",
        "classification_before_mark": audit_metrics["classification"],
        "audited_source_count": audit_metrics["audited_source_count"],
        "audited_existing_source_count": audit_metrics["audited_existing_source_count"],
        "audited_row_count_total": audit_metrics["audited_row_count_total"],
        "audited_key_present_count_total": audit_metrics["audited_key_present_count_total"],
        "audited_non_null_value_count_total": audit_metrics["audited_non_null_value_count_total"],
        "audited_values_found": audit_metrics["audited_values_found"],
        "all_field_values_absent_in_audited_chain": audit_metrics["all_field_values_absent_in_audited_chain"],
        "expected_limit_marked": True,
        "universal_upstream_nonexistence_proven": False,
        "taxonomy_gap_resolved": False,
        "taxonomy_delta_authorized": False,
        "taxonomy_upgrade_authorized": False,
        "value_inference_authorized": False,
        "branch_resolution": "EXPECTED_SOURCE_CONTENT_LIMIT_MARKED_NO_VALUE_OR_TAXONOMY_REPAIR_AUTHORIZED",
        "marked_at": now_iso(),
    }

def build_closure_record(marker: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "field_introduced_surface_expected_source_content_limit_closure_record_v0",
        "closure_id": sha8({
            "marker_id": marker["marker_id"],
            "closure": "R1000_TOP_GROUP_TAXONOMY_GAP_EXPECTED_SOURCE_CONTENT_LIMIT",
        }),
        "source_marker_id": marker["marker_id"],
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "closed_branch": "R1000_TOP_GROUP_TAXONOMY_GAP_FIELD_INTRODUCED_NULL_EVIDENCE_BRANCH",
        "closure_class": "EXPECTED_SOURCE_CONTENT_LIMIT",
        "closure_reason": "explicit tracked source-chain audit found no non-null values for introduced fields",
        "closed_against": [
            "value invention",
            "taxonomy label creation",
            "taxonomy upgrade",
            "source mutation",
            "receipt mutation",
            "source-provenance repair from this branch",
        ],
        "remaining_open_options_only_by_new_authorization": [
            "request broader upstream existence audit",
            "reinspect field-introduced surface",
            "reopen classification if new source evidence appears",
        ],
        "branch_closed": True,
        "next_group_auto_opened": False,
    }

def build_decision_packet(marker: Dict[str, Any], closure: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "field_introduced_surface_expected_source_content_limit_decision_packet_v0",
        "packet_type": "CLOSURE_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "source_marker_id": marker["marker_id"],
        "source_closure_id": closure["closure_id"],
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "closure_class": closure["closure_class"],
        "branch_closed": True,
        "recommended_next_handling": "RETURN_TO_PRESSURE_QUEUE_OR_SELECT_NEXT_HUMAN_AUTHORIZED_OBJECTIVE",
        "allowed_followup_choices": [
            "RETURN_TO_PRESSURE_QUEUE",
            "REQUEST_BROADER_UPSTREAM_EXISTENCE_AUDIT",
            "REOPEN_IF_NEW_SOURCE_EVIDENCE_APPEARS",
            "SELECT_NEXT_HUMAN_AUTHORIZED_OBJECTIVE",
        ],
        "may_emit_next_command": False,
        "may_auto_open_next_group": False,
        "may_invent_missing_label_value": False,
        "may_create_taxonomy_label": False,
        "may_upgrade_taxonomy": False,
        "may_emit_taxonomy_delta": False,
        "may_mutate_source": False,
        "may_mutate_existing_receipts": False,
        "review_only": True,
    }

def build_report(marker: Dict[str, Any], closure: Dict[str, Any], packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "field_introduced_surface_expected_source_content_limit_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_receipts": {
            "source_upstream_existence_audit_receipt_id": SOURCE_UPSTREAM_AUDIT_RECEIPT_ID,
            "source_null_limit_classification_receipt_id": SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID,
            "source_field_introduced_surface_rerun_receipt_id": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
            "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
        },
        "marker_id": marker["marker_id"],
        "closure_id": closure["closure_id"],
        "limit_scope": marker["limit_scope"],
        "expected_limit_marked": True,
        "branch_closed": True,
        "classification": marker["branch_resolution"],
        "recommended_next_handling": packet["recommended_next_handling"],
        "universal_upstream_nonexistence_proven": False,
        "taxonomy_gap_resolved": False,
        "audited_values_found": marker["audited_values_found"],
        "audited_non_null_value_count_total": marker["audited_non_null_value_count_total"],
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "historical_source_overwrite_count": 0,
        "existing_receipt_mutation_count": 0,
        "source_mutation_count": 0,
        "source_semantics_mutation_count": 0,
        "source_provenance_repair_executed_count": 0,
        "broader_audit_executed_count": 0,
        "expected_limit_marked_count": 1,
        "taxonomy_delta_proposal_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "next_command_emitted_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
        "review_only": True,
    }

def validate_outputs(marker: Dict[str, Any], closure: Dict[str, Any], packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if marker["marker_type"] != "EXPECTED_SOURCE_CONTENT_LIMIT":
        failures.append("marker_type_wrong")
    if marker["expected_limit_marked"] is not True:
        failures.append("expected_limit_not_marked")
    if marker["audited_values_found"] is not False:
        failures.append("marker_values_found")
    if marker["audited_non_null_value_count_total"] != 0:
        failures.append("marker_non_null_count_wrong")
    if marker["universal_upstream_nonexistence_proven"] is not False:
        failures.append("marker_universal_nonexistence_overclaim")
    if marker["taxonomy_gap_resolved"] is not False:
        failures.append("marker_taxonomy_gap_resolved_wrongly")
    if marker["taxonomy_delta_authorized"] is not False:
        failures.append("marker_taxonomy_delta_authorized")
    if marker["taxonomy_upgrade_authorized"] is not False:
        failures.append("marker_taxonomy_upgrade_authorized")
    if marker["value_inference_authorized"] is not False:
        failures.append("marker_value_inference_authorized")

    if closure["branch_closed"] is not True:
        failures.append("closure_not_closed")
    if closure["next_group_auto_opened"] is not False:
        failures.append("closure_auto_opened_next_group")
    if packet["packet_type"] != "CLOSURE_PACKET_NOT_COMMAND":
        failures.append("packet_type_wrong")
    for key in [
        "may_emit_next_command",
        "may_auto_open_next_group",
        "may_invent_missing_label_value",
        "may_create_taxonomy_label",
        "may_upgrade_taxonomy",
        "may_emit_taxonomy_delta",
        "may_mutate_source",
        "may_mutate_existing_receipts",
    ]:
        if packet.get(key) is not False:
            failures.append(f"packet_guard_not_false:{key}:{packet.get(key)}")

    if report["expected_limit_marked_count"] != 1:
        failures.append("report_expected_limit_marked_count_wrong")
    for key in [
        "field_value_invention_count",
        "taxonomy_label_creation_count",
        "historical_source_overwrite_count",
        "existing_receipt_mutation_count",
        "source_mutation_count",
        "source_semantics_mutation_count",
        "source_provenance_repair_executed_count",
        "broader_audit_executed_count",
        "taxonomy_delta_proposal_emitted_count",
        "taxonomy_upgrade_authorized_count",
        "next_command_emitted_count",
        "next_group_auto_opened_count",
        "hidden_next_command_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")
    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    if receipt.get("source_upstream_existence_audit_receipt_id") != SOURCE_UPSTREAM_AUDIT_RECEIPT_ID:
        failures.append("source_audit_receipt_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "EXPECTED_LIMIT_0_UPSTREAM_AUDIT_CONSUMED",
        "EXPECTED_LIMIT_1_HUMAN_DECISION_RECORDED",
        "EXPECTED_LIMIT_2_MARKER_EMITTED",
        "EXPECTED_LIMIT_3_BRANCH_CLOSURE_RECORDED",
        "EXPECTED_LIMIT_4_NO_VALUE_OR_TAXONOMY_ACTION",
        "EXPECTED_LIMIT_5_NO_SOURCE_OR_RECEIPT_MUTATION",
        "EXPECTED_LIMIT_6_NO_BROADER_AUDIT_EXECUTED",
        "EXPECTED_LIMIT_7_NO_NEXT_GROUP_AUTO_OPEN",
        "EXPECTED_LIMIT_8_NO_HIDDEN_NEXT_COMMAND",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("expected_limit_marked") is not True:
        failures.append("metric_expected_limit_not_marked")
    if metrics.get("expected_limit_marked_count") != 1:
        failures.append("metric_expected_limit_mark_count_wrong")
    if metrics.get("branch_closed") is not True:
        failures.append("metric_branch_not_closed")
    if metrics.get("audited_values_found") is not False:
        failures.append("metric_values_found")
    if metrics.get("audited_non_null_value_count_total") != 0:
        failures.append("metric_non_null_count_wrong")
    if metrics.get("universal_upstream_nonexistence_proven") is not False:
        failures.append("metric_universal_nonexistence_overclaim")
    if metrics.get("taxonomy_gap_resolved") is not False:
        failures.append("metric_taxonomy_gap_resolved_wrongly")
    for key in [
        "field_value_invention_count",
        "taxonomy_label_creation_count",
        "historical_source_overwrite_count",
        "existing_receipt_mutation_count",
        "source_mutation_count",
        "source_semantics_mutation_count",
        "source_provenance_repair_executed_count",
        "broader_audit_executed_count",
        "taxonomy_delta_proposal_emitted_count",
        "taxonomy_upgrade_authorized_count",
        "next_command_emitted_count",
        "next_group_auto_opened_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    guards = receipt.get("expected_source_content_limit_guards", {})
    for key in [
        "upstream_audit_consumed",
        "human_decision_recorded",
        "expected_limit_marker_emitted",
        "branch_closure_recorded",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "values_invented",
        "taxonomy_label_created",
        "taxonomy_delta_proposal_emitted",
        "taxonomy_upgrade_authorized",
        "historical_source_overwritten",
        "existing_receipts_mutated",
        "source_mutated",
        "source_semantics_mutated",
        "source_provenance_repair_executed",
        "broader_audit_executed",
        "next_command_emitted",
        "next_group_auto_opened",
        "hidden_next_command",
        "universal_nonexistence_overclaimed",
    ]:
        if guards.get(key) is not False:
            failures.append(f"guard_not_false:{key}:{guards.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_BRANCH_CLOSED_EXPECTED_SOURCE_CONTENT_LIMIT":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")

    return failures

def main() -> int:
    source_before = snapshot_files(SOURCE_FILES)
    sources = load_sources()
    failures: List[str] = validate_sources(sources)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    marker = build_marker(sources)
    closure = build_closure_record(marker)
    packet = build_decision_packet(marker, closure)
    report = build_report(marker, closure, packet)

    write_json(MARKER_PATH, marker)
    write_json(CLOSURE_RECORD_PATH, closure)
    write_json(DECISION_PACKET_PATH, packet)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(marker, closure, packet, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "EXPECTED_LIMIT_0_UPSTREAM_AUDIT_CONSUMED": sources["upstream_audit_receipt"]["receipt_id"] == SOURCE_UPSTREAM_AUDIT_RECEIPT_ID and sources["upstream_audit_receipt"]["gate"] == "PASS",
        "EXPECTED_LIMIT_1_HUMAN_DECISION_RECORDED": HUMAN_DECISION["decision"] == "MARK_EXPECTED_SOURCE_CONTENT_LIMIT",
        "EXPECTED_LIMIT_2_MARKER_EMITTED": MARKER_PATH.exists() and marker["expected_limit_marked"] is True,
        "EXPECTED_LIMIT_3_BRANCH_CLOSURE_RECORDED": CLOSURE_RECORD_PATH.exists() and closure["branch_closed"] is True,
        "EXPECTED_LIMIT_4_NO_VALUE_OR_TAXONOMY_ACTION": report["field_value_invention_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0 and report["taxonomy_upgrade_authorized_count"] == 0,
        "EXPECTED_LIMIT_5_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "EXPECTED_LIMIT_6_NO_BROADER_AUDIT_EXECUTED": report["broader_audit_executed_count"] == 0,
        "EXPECTED_LIMIT_7_NO_NEXT_GROUP_AUTO_OPEN": report["next_group_auto_opened_count"] == 0,
        "EXPECTED_LIMIT_8_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and report["next_command_emitted_count"] == 0,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {"type": "STOP", "stop_code": "STOP_BRANCH_CLOSED_EXPECTED_SOURCE_CONTENT_LIMIT", "next_command_goal": None}
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}
    if any([
        report["field_value_invention_count"],
        report["taxonomy_label_creation_count"],
        report["historical_source_overwrite_count"],
        report["existing_receipt_mutation_count"],
        report["source_mutation_count"],
        report["source_semantics_mutation_count"],
        report["source_provenance_repair_executed_count"],
        report["broader_audit_executed_count"],
        report["taxonomy_delta_proposal_emitted_count"],
        report["taxonomy_upgrade_authorized_count"],
        report["next_command_emitted_count"],
        report["next_group_auto_opened_count"],
        report["hidden_next_command_count"],
    ]):
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_upstream_existence_audit_receipt_id": SOURCE_UPSTREAM_AUDIT_RECEIPT_ID,
        "source_null_limit_classification_receipt_id": SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID,
        "source_field_introduced_surface_rerun_receipt_id": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
        "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "marker_id": marker["marker_id"],
        "closure_id": closure["closure_id"],
        "limit_scope": marker["limit_scope"],
        "expected_limit_marked": True,
        "expected_limit_marked_count": 1,
        "branch_closed": True,
        "branch_resolution": marker["branch_resolution"],
        "audited_values_found": marker["audited_values_found"],
        "audited_non_null_value_count_total": marker["audited_non_null_value_count_total"],
        "universal_upstream_nonexistence_proven": False,
        "taxonomy_gap_resolved": False,
        "recommended_next_handling": packet["recommended_next_handling"],
        "marker_emitted_count": 1,
        "closure_record_emitted_count": 1,
        "decision_packet_emitted_count": 1,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "historical_source_overwrite_count": 0,
        "existing_receipt_mutation_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "source_semantics_mutation_count": 0,
        "source_provenance_repair_executed_count": 0,
        "broader_audit_executed_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "next_command_emitted_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
    }

    guards = {
        "upstream_audit_consumed": True,
        "human_decision_recorded": True,
        "expected_limit_marker_emitted": True,
        "branch_closure_recorded": True,
        "values_invented": False,
        "taxonomy_label_created": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "historical_source_overwritten": False,
        "existing_receipts_mutated": False,
        "source_mutated": source_mutation_detected,
        "source_semantics_mutated": False,
        "source_provenance_repair_executed": False,
        "broader_audit_executed": False,
        "next_command_emitted": False,
        "next_group_auto_opened": False,
        "hidden_next_command": False,
        "universal_nonexistence_overclaimed": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_audit": SOURCE_UPSTREAM_AUDIT_RECEIPT_ID,
        "marker_id": marker["marker_id"],
        "closure_id": closure["closure_id"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "expected_source_content_limit_marker": rel(MARKER_PATH),
        "expected_source_content_limit_closure_record": rel(CLOSURE_RECORD_PATH),
        "expected_source_content_limit_decision_packet": rel(DECISION_PACKET_PATH),
        "expected_source_content_limit_report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "field_introduced_surface_expected_source_content_limit_receipt_v0",
        "receipt_type": "FIELD_INTRODUCED_SURFACE_EXPECTED_SOURCE_CONTENT_LIMIT_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_upstream_existence_audit_receipt_id": SOURCE_UPSTREAM_AUDIT_RECEIPT_ID,
        "source_null_limit_classification_receipt_id": SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID,
        "source_field_introduced_surface_rerun_receipt_id": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
        "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
        "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "expected_source_content_limit_summary": {
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "marker_id": marker["marker_id"],
            "closure_id": closure["closure_id"],
            "limit_scope": marker["limit_scope"],
            "expected_limit_marked": True,
            "branch_closed": True,
            "branch_resolution": marker["branch_resolution"],
            "audited_values_found": marker["audited_values_found"],
            "audited_non_null_value_count_total": marker["audited_non_null_value_count_total"],
            "universal_upstream_nonexistence_proven": False,
            "taxonomy_gap_resolved": False,
            "recommended_next_handling": packet["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "expected_source_content_limit_guards": guards,
        "must_not_infer": MUST_NOT_INFER,
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
    print(f"expected_source_content_limit_receipt_id={receipt_id}")
    print(f"expected_source_content_limit_receipt_path=data/field_introduced_surface_expected_source_content_limit_v0_receipts/{receipt_id}.json")
    print(f"expected_source_content_limit_marker_path=data/field_introduced_surface_expected_source_content_limit_v0/expected_source_content_limit_marker.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
