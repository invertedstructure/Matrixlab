#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RERUN_C3_MICRO_DOMAIN_SHIFT_REHEARSAL_AGAINST_C1_INTERFACE_PATCH_V0"
TARGET_UNIT_ID = "c3.micro_domain_shift_rerun_against_c1_interface_patch.v0"
LAYER = "CELL_0 / MICRO_DOMAIN_SHIFT_RERUN"
MODE = "VERIFY / RERUN / INTERFACE_REHEARSAL"
BUILD_MODE = "RERUN_AGAINST_CANDIDATE_INTERFACE_PATCH_ONLY"

SOURCE_C1_PATCH_RECEIPT_ID = "fffa3dd5"
SOURCE_C1_PATCH_RECEIPT_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0_receipts" / "fffa3dd5.json"
SOURCE_C1_PATCH_PROFILE_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0" / "c1_interface_patch_profile_v0.json"
SOURCE_C1_PATCH_ROLLUP_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0" / "c1_interface_patch_rollup_v0.json"
SOURCE_C1_PATCH_SCHEMA_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0" / "proposal_packet_schema_v0_1.json"
SOURCE_C1_PATCH_COVERAGE_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0" / "c3_gap_to_c1_interface_coverage_matrix_v0.json"
SOURCE_C1_PATCH_RERUN_CONTRACT_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0" / "c3_rerun_contract_v0.json"
SOURCE_C1_PATCH_VALIDATION_RESULTS_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0" / "c1_interface_patch_validation_results_v0.jsonl"

SOURCE_C3_RECEIPT_ID = "cfc79da2"
SOURCE_C3_RECEIPT_PATH = ROOT / "data" / "c3_cell0_micro_domain_shift_rehearsal_v0_receipts" / "cfc79da2.json"
SOURCE_C3_VERDICT_PATH = ROOT / "data" / "c3_cell0_micro_domain_shift_rehearsal_v0" / "c3_interface_readiness_verdict_v0.json"
SOURCE_C3_GAP_REPORTS_PATH = ROOT / "data" / "c3_cell0_micro_domain_shift_rehearsal_v0" / "domain_shift_proposal_gap_reports_v0.jsonl"

SOURCE_C4_PREFLIGHT_RECEIPT_ID = "75764a86"
SOURCE_C4_PREFLIGHT_RECEIPT_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_v0_receipts" / "75764a86.json"
SOURCE_C4_PREFLIGHT_GATE_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_v0" / "c4_opening_gate_evaluation_v0.json"

SOURCE_C2_RECEIPT_ID = "348dabde"
SOURCE_C2_RECEIPT_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts" / "348dabde.json"
SOURCE_C2_LANE_REGISTRY_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "taxonomy_lane_registry_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C1_PATCH_RECEIPT_PATH,
    SOURCE_C1_PATCH_PROFILE_PATH,
    SOURCE_C1_PATCH_ROLLUP_PATH,
    SOURCE_C1_PATCH_SCHEMA_PATH,
    SOURCE_C1_PATCH_COVERAGE_PATH,
    SOURCE_C1_PATCH_RERUN_CONTRACT_PATH,
    SOURCE_C1_PATCH_VALIDATION_RESULTS_PATH,
    SOURCE_C3_RECEIPT_PATH,
    SOURCE_C3_VERDICT_PATH,
    SOURCE_C3_GAP_REPORTS_PATH,
    SOURCE_C4_PREFLIGHT_RECEIPT_PATH,
    SOURCE_C4_PREFLIGHT_GATE_PATH,
    SOURCE_C2_RECEIPT_PATH,
    SOURCE_C2_LANE_REGISTRY_PATH,
]

OUT_DIR = ROOT / "data" / "c3_micro_domain_shift_rerun_against_c1_interface_patch_v0"
RECEIPT_DIR = ROOT / "data" / "c3_micro_domain_shift_rerun_against_c1_interface_patch_v0_receipts"

SOURCE_SURFACE_PATH = OUT_DIR / "c3_rerun_source_surface_v0.json"
PATCHED_INTERFACE_REHEARSAL_RECORDS_PATH = OUT_DIR / "patched_interface_rehearsal_records_v0.jsonl"
PROPOSAL_INTERFACE_VALIDATION_RECORDS_PATH = OUT_DIR / "proposal_interface_validation_records_v0.jsonl"
CELL1_READINESS_PROBE_RECORDS_PATH = OUT_DIR / "cell1_readiness_probe_records_v0.jsonl"
PREVIOUS_GAP_COMPARISON_PATH = OUT_DIR / "previous_gap_comparison_v0.json"
C3_RERUN_CONTRACT_RESULT_PATH = OUT_DIR / "c3_rerun_contract_result_v0.json"
UPDATED_VERDICT_PATH = OUT_DIR / "c3_interface_readiness_verdict_v0_1.json"
ROLLUP_PATH = OUT_DIR / "c3_rerun_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c3_rerun_profile_v0.json"
REPORT_PATH = OUT_DIR / "c3_rerun_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "c3_rerun_transition_trace.json"

ZERO_COUNTER_KEYS = [
    "cell1_execution_opened_count",
    "accepted_proposal_fabricated_count",
    "proposal_status_promoted_count",
    "builder_command_emitted_count",
    "c4_rerun_count",
    "c5_opened_count",
    "hidden_next_command_count",
    "taxonomy_registry_mutation_count",
    "runtime_patch_applied_count",
    "source_mutation_count",
    "prior_receipt_mutation_count",
    "canonical_c1_schema_replaced_count",
    "unbounded_payload_inspection_count",
    "schema_gap_ignored_count",
    "old_gap_declared_fixed_without_field_count",
    "ready_verdict_without_contract_count",
    "ready_verdict_counted_as_cell1_execution_count",
]

HUMAN_DECISION = {
    "decision": "RERUN_C3_MICRO_DOMAIN_SHIFT_REHEARSAL_AGAINST_C1_INTERFACE_PATCH",
    "scope": "Rerun C3 micro-domain shift rehearsal against the C1 proposal interface patch candidate. Consume the C1 interface patch receipt, v0_1 candidate schema, gap coverage matrix, C3 rerun contract, original C3 gap report/verdict, C4 blocked preflight receipt, and C2 lane registry. Test whether the previous proposal/schema gaps are resolved or narrowed by the candidate interface. Emit updated interface-readiness verdict, rollup, profile, report, and receipt. Do not open Cell 1, do not rerun C4, do not fabricate accepted proposals, do not mutate taxonomy, and do not emit hidden next command.",
    "authorized": [
        "consume C1 interface patch candidate",
        "consume C3 rerun contract",
        "consume original C3 gap report and verdict",
        "consume C4 blocked preflight receipt",
        "consume C2 lane registry",
        "rerun micro-domain interface rehearsal against patched schema",
        "compare previous gap coverage to patched fields",
        "emit updated C3 interface readiness verdict",
        "emit C3 rerun receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "open Cell 1 execution",
        "consume accepted proposal as build input",
        "fabricate accepted proposal",
        "promote PROPOSED_ONLY to accepted",
        "rerun C4",
        "open C5",
        "mutate taxonomy registry",
        "apply runtime patch",
        "claim full domain shift",
        "emit hidden next command",
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
            if line.strip():
                rows.append(json.loads(line))
    return rows

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def validate_source_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    c1_patch_receipt = read_json(SOURCE_C1_PATCH_RECEIPT_PATH)
    c1_patch_profile = read_json(SOURCE_C1_PATCH_PROFILE_PATH)
    c1_patch_rollup = read_json(SOURCE_C1_PATCH_ROLLUP_PATH)
    patched_schema = read_json(SOURCE_C1_PATCH_SCHEMA_PATH)
    coverage = read_json(SOURCE_C1_PATCH_COVERAGE_PATH)
    rerun_contract = read_json(SOURCE_C1_PATCH_RERUN_CONTRACT_PATH)
    c3_receipt = read_json(SOURCE_C3_RECEIPT_PATH)
    c3_verdict = read_json(SOURCE_C3_VERDICT_PATH)
    c4_receipt = read_json(SOURCE_C4_PREFLIGHT_RECEIPT_PATH)
    c4_gate = read_json(SOURCE_C4_PREFLIGHT_GATE_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)

    if c1_patch_receipt.get("receipt_id") != SOURCE_C1_PATCH_RECEIPT_ID or c1_patch_receipt.get("gate") != "PASS":
        failures.append("c1_interface_patch_basis_not_accepted")
    if c1_patch_profile.get("status") != "C1_PROPOSAL_INTERFACE_PATCH_READY_FOR_C3_RERUN":
        failures.append("c1_patch_profile_not_ready_for_rerun")
    if c1_patch_rollup.get("interface_patch_status") != "CANDIDATE_INTERFACE_PATCH":
        failures.append("c1_patch_not_candidate_interface_patch")
    if c1_patch_rollup.get("uncovered_c3_gap_count") != 0:
        failures.append("c1_patch_has_uncovered_gaps")
    if patched_schema.get("schema_version") != "proposal_packet_schema_v0_1":
        failures.append("patched_schema_wrong_version")
    if patched_schema.get("interface_patch_status") != "CANDIDATE_INTERFACE_PATCH":
        failures.append("patched_schema_not_candidate")
    if patched_schema.get("canonical_c1_schema_replaced") is not False:
        failures.append("patched_schema_claims_canonical_replaced")
    if patched_schema.get("requires_c3_rerun") is not True:
        failures.append("patched_schema_missing_rerun_requirement")
    if coverage.get("uncovered_gap_count") != 0:
        failures.append("coverage_uncovered_gaps_nonzero")
    if rerun_contract.get("patched_interface_schema_ref") != rel(SOURCE_C1_PATCH_SCHEMA_PATH):
        failures.append("rerun_contract_schema_ref_mismatch")
    if c3_receipt.get("receipt_id") != SOURCE_C3_RECEIPT_ID or c3_receipt.get("gate") != "PASS":
        failures.append("original_c3_basis_not_accepted")
    if c3_verdict.get("verdict") != "CELL1_NOT_READY_PROPOSAL_SCHEMA_GAPS":
        failures.append("original_c3_verdict_not_gap")
    if c4_receipt.get("receipt_id") != SOURCE_C4_PREFLIGHT_RECEIPT_ID or c4_receipt.get("gate") != "PASS":
        failures.append("c4_preflight_basis_not_accepted")
    if c4_gate.get("c4_opening_gate_status") != "BLOCKED":
        failures.append("c4_preflight_gate_not_blocked")
    if c2_receipt.get("receipt_id") != SOURCE_C2_RECEIPT_ID or c2_receipt.get("gate") != "PASS":
        failures.append("c2_basis_not_accepted")
    if not read_jsonl(SOURCE_C3_GAP_REPORTS_PATH):
        failures.append("original_c3_gap_reports_missing")
    return failures

def source_surface() -> Dict[str, Any]:
    return {
        "schema_version": "c3_rerun_source_surface_v0",
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c1_patch_receipt_ref": rel(SOURCE_C1_PATCH_RECEIPT_PATH),
        "patched_interface_schema_ref": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "source_c3_receipt_id": SOURCE_C3_RECEIPT_ID,
        "source_c3_gap_report_ref": rel(SOURCE_C3_GAP_REPORTS_PATH),
        "source_c4_preflight_receipt_id": SOURCE_C4_PREFLIGHT_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "surface_status": "EXPLICIT_C1_PATCH_RERUN_SURFACE",
    }

def required_sections() -> List[str]:
    return [
        "builder_interface",
        "verification_contract",
        "failure_or_reject_handling",
        "claim_scope",
        "payload_boundary",
        "evidence_limitations",
        "review_authority",
    ]

def make_rehearsal_records() -> List[Dict[str, Any]]:
    schema = read_json(SOURCE_C1_PATCH_SCHEMA_PATH)
    coverage = read_json(SOURCE_C1_PATCH_COVERAGE_PATH)
    records: List[Dict[str, Any]] = []
    for section in required_sections():
        records.append({
            "schema_version": "patched_interface_rehearsal_record_v0",
            "record_id": "rehearsal_" + sha8({"section": section}),
            "section": section,
            "present": section in schema,
            "candidate_schema_ref": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
            "cell1_execution_opened": False,
            "status": "PASS" if section in schema else "MISSING",
        })
    for row in coverage.get("coverage_rows", []):
        records.append({
            "schema_version": "patched_interface_rehearsal_record_v0",
            "record_id": "coverage_" + sha8({"gap": row.get("gap_record_ref"), "fields": row.get("patched_fields", [])}),
            "gap_record_ref": row.get("gap_record_ref"),
            "gap_class": row.get("gap_class"),
            "patched_fields": row.get("patched_fields", []),
            "coverage_status": row.get("coverage_status"),
            "cell1_execution_opened": False,
            "status": "PASS" if row.get("coverage_status") == "COVERED_BY_CANDIDATE_SCHEMA" else "BLOCKED",
        })
    return records

def make_validation_records() -> List[Dict[str, Any]]:
    prior_validations = read_jsonl(SOURCE_C1_PATCH_VALIDATION_RESULTS_PATH)
    records = []
    for v in prior_validations:
        records.append({
            "schema_version": "proposal_interface_validation_record_v0",
            "validation_ref": v.get("proposal_id"),
            "source_validation_result": v.get("result"),
            "cell1_consumable": v.get("cell1_consumable", False),
            "proposed_only_remains_blocked": v.get("proposed_only_remains_not_cell1_consumable", False) or v.get("cell1_consumable", False) is False,
            "rerun_interpretation": "VALID_FOR_REVIEW_NOT_CELL1_CONSUMPTION" if v.get("cell1_consumable", False) is False else "INVALID_CELL1_CONSUMABLE_WITHOUT_REVIEW",
            "status": "PASS" if v.get("cell1_consumable", False) is False else "FAIL",
        })
    return records

def make_readiness_probes(rehearsal_records: List[Dict[str, Any]], validation_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    schema = read_json(SOURCE_C1_PATCH_SCHEMA_PATH)
    probes = [
        {
            "schema_version": "cell1_readiness_probe_record_v0",
            "probe_id": "probe_required_sections_" + sha8(required_sections()),
            "probe_kind": "SCHEMA_SECTION_COVERAGE",
            "observed": {section: section in schema for section in required_sections()},
            "result": "PASS" if all(section in schema for section in required_sections()) else "FAIL",
            "cell1_execution_opened": False,
        },
        {
            "schema_version": "cell1_readiness_probe_record_v0",
            "probe_id": "probe_gap_coverage_" + sha8({"records": len(rehearsal_records)}),
            "probe_kind": "C3_GAP_COVERAGE",
            "observed": {
                "covered_gap_rows": sum(1 for r in rehearsal_records if r.get("coverage_status") == "COVERED_BY_CANDIDATE_SCHEMA"),
                "blocked_gap_rows": sum(1 for r in rehearsal_records if r.get("status") == "BLOCKED"),
            },
            "result": "PASS" if all(r.get("status") != "BLOCKED" for r in rehearsal_records) else "FAIL",
            "cell1_execution_opened": False,
        },
        {
            "schema_version": "cell1_readiness_probe_record_v0",
            "probe_id": "probe_proposed_only_blocked_" + sha8({"records": len(validation_records)}),
            "probe_kind": "PROPOSED_ONLY_REMAINS_BLOCKED",
            "observed": {
                "validation_records": len(validation_records),
                "cell1_consumable_records": sum(1 for r in validation_records if r.get("cell1_consumable") is True),
            },
            "result": "PASS" if all(r.get("cell1_consumable") is False for r in validation_records) else "FAIL",
            "cell1_execution_opened": False,
        },
        {
            "schema_version": "cell1_readiness_probe_record_v0",
            "probe_id": "probe_review_authority_" + sha8(schema.get("review_authority", {})),
            "probe_kind": "REVIEW_AUTHORITY_CHAIN",
            "observed": {
                "review_required": schema.get("review_authority", {}).get("review_required"),
                "default_without_review": schema.get("review_authority", {}).get("default_without_review"),
                "cell1_may_accept": schema.get("review_authority", {}).get("cell1_may_accept"),
                "builder_consumption_allowed": schema.get("builder_interface", {}).get("builder_consumption_allowed"),
            },
            "result": "PASS" if schema.get("review_authority", {}).get("review_required") is True and schema.get("review_authority", {}).get("cell1_may_accept") is False else "FAIL",
            "cell1_execution_opened": False,
        },
    ]
    return probes

def previous_gap_comparison(rehearsal_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    previous_gap_reports = read_jsonl(SOURCE_C3_GAP_REPORTS_PATH)
    coverage = read_json(SOURCE_C1_PATCH_COVERAGE_PATH)
    return {
        "schema_version": "previous_gap_comparison_v0",
        "source_c3_receipt_id": SOURCE_C3_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "previous_gap_report_count": len(previous_gap_reports),
        "coverage_rows_total": len(coverage.get("coverage_rows", [])),
        "coverage_rows_passed": sum(1 for r in rehearsal_records if r.get("coverage_status") == "COVERED_BY_CANDIDATE_SCHEMA"),
        "previous_gap_resolved_or_narrowed": coverage.get("uncovered_gap_count") == 0,
        "remaining_gap_count": 0 if coverage.get("uncovered_gap_count") == 0 else coverage.get("uncovered_gap_count"),
        "must_not_infer": [
            "Cell 1 executed",
            "proposal accepted",
            "C4 preflight rerun",
            "C5 authorized",
        ],
    }

def updated_verdict(probes: List[Dict[str, Any]], comparison: Dict[str, Any]) -> Dict[str, Any]:
    all_probe_pass = all(p.get("result") == "PASS" for p in probes)
    ready = all_probe_pass and comparison.get("remaining_gap_count") == 0
    verdict = "CELL1_READY_FOR_NARROW_ACCEPTED_PROPOSAL_TEST" if ready else "CELL1_NOT_READY_PROPOSAL_SCHEMA_GAPS"
    return {
        "schema_version": "c3_interface_readiness_verdict_v0_1",
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_original_c3_receipt_id": SOURCE_C3_RECEIPT_ID,
        "verdict": verdict,
        "previous_verdict": "CELL1_NOT_READY_PROPOSAL_SCHEMA_GAPS",
        "verdict_changed": verdict != "CELL1_NOT_READY_PROPOSAL_SCHEMA_GAPS",
        "reason": "C1 proposal interface candidate now covers C3-reported proposal/schema gaps and preserves review/acceptance boundaries." if ready else "C1 proposal interface candidate still leaves proposal/schema gaps.",
        "cell1_execution_opened": False,
        "c4_rerun_executed": False,
        "cell1_consumption_authorized_now": False,
        "c4_preflight_may_be_rerun_later": ready,
        "must_not_infer": [
            "Cell 1 execution occurred",
            "proposal accepted",
            "C4 opened in this unit",
            "full domain shift authorized",
        ],
    }

def contract_result(verdict: Dict[str, Any]) -> Dict[str, Any]:
    contract = read_json(SOURCE_C1_PATCH_RERUN_CONTRACT_PATH)
    allowed = contract.get("expected_possible_outcomes", [])
    return {
        "schema_version": "c3_rerun_contract_result_v0",
        "source_contract_ref": rel(SOURCE_C1_PATCH_RERUN_CONTRACT_PATH),
        "rerun_goal": contract.get("rerun_goal"),
        "observed_outcome": verdict["verdict"],
        "observed_outcome_allowed_by_contract": verdict["verdict"] in allowed,
        "contract_status": "PASS" if verdict["verdict"] in allowed else "FAIL",
        "next_recommended_handling": "RERUN_C4_CELL1_RECEIPT_NATIVE_BUILDER_PREFLIGHT_V0" if verdict["verdict"] == "CELL1_READY_FOR_NARROW_ACCEPTED_PROPOSAL_TEST" else "REFINE_C1_INTERFACE_PATCH_OR_QUESTION_PACKET",
    }

def rollup(rehearsal_records: List[Dict[str, Any]], validation_records: List[Dict[str, Any]], probes: List[Dict[str, Any]], comparison: Dict[str, Any], verdict: Dict[str, Any], contract: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c3_rerun_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_original_c3_receipt_id": SOURCE_C3_RECEIPT_ID,
        "source_c4_preflight_receipt_id": SOURCE_C4_PREFLIGHT_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "patched_interface_schema_ref": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "rehearsal_records_total": len(rehearsal_records),
        "rehearsal_records_passed": sum(1 for r in rehearsal_records if r.get("status") == "PASS"),
        "validation_records_total": len(validation_records),
        "validation_records_passed": sum(1 for r in validation_records if r.get("status") == "PASS"),
        "readiness_probes_total": len(probes),
        "readiness_probes_passed": sum(1 for p in probes if p.get("result") == "PASS"),
        "previous_gap_report_count": comparison["previous_gap_report_count"],
        "previous_gap_resolved_or_narrowed": comparison["previous_gap_resolved_or_narrowed"],
        "remaining_gap_count": comparison["remaining_gap_count"],
        "updated_interface_readiness_verdict": verdict["verdict"],
        "verdict_changed": verdict["verdict_changed"],
        "contract_status": contract["contract_status"],
        "cell1_execution_opened_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "proposal_status_promoted_count": 0,
        "builder_command_emitted_count": 0,
        "c4_rerun_count": 0,
        "c5_opened_count": 0,
        "hidden_next_command_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "runtime_patch_applied_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "canonical_c1_schema_replaced_count": 0,
        "unbounded_payload_inspection_count": 0,
        "schema_gap_ignored_count": 0,
        "old_gap_declared_fixed_without_field_count": 0,
        "ready_verdict_without_contract_count": 0,
        "ready_verdict_counted_as_cell1_execution_count": 0,
        "recommended_next": "RERUN_C4_CELL1_RECEIPT_NATIVE_BUILDER_PREFLIGHT_V0" if verdict["verdict"] == "CELL1_READY_FOR_NARROW_ACCEPTED_PROPOSAL_TEST" else "REFINE_C1_INTERFACE_PATCH_OR_QUESTION_PACKET",
    }

def profile(rollup_obj: Dict[str, Any]) -> Dict[str, Any]:
    ready = rollup_obj["updated_interface_readiness_verdict"] == "CELL1_READY_FOR_NARROW_ACCEPTED_PROPOSAL_TEST"
    return {
        "schema_version": "c3_rerun_profile_v0",
        "profile_id": "c3_rerun_" + sha8({"verdict": rollup_obj["updated_interface_readiness_verdict"], "source": SOURCE_C1_PATCH_RECEIPT_ID}),
        "status": "C3_RERUN_INTERFACE_READY_FOR_C4_PREFLIGHT" if ready else "C3_RERUN_STILL_BLOCKED_BY_PROPOSAL_SCHEMA_GAPS",
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_original_c3_receipt_id": SOURCE_C3_RECEIPT_ID,
        "updated_verdict_ref": rel(UPDATED_VERDICT_PATH),
        "rollup_ref": rel(ROLLUP_PATH),
        "cell1_execution_opened": False,
        "c4_rerun_executed": False,
        "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "must_not_infer": [
            "Cell 1 execution occurred",
            "proposal accepted",
            "C4 executed",
            "C5 authorized",
            "full domain shift ready",
        ],
        "next_command_goal": None,
    }

def report(rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c3_rerun_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_c1_patch_consumed_count": 1,
        "source_c3_gap_report_consumed_count": 1,
        "source_c4_preflight_consumed_count": 1,
        "source_c2_lane_registry_consumed_count": 1,
        "patched_interface_schema_consumed_count": 1,
        "rehearsal_records_emitted_count": rollup_obj["rehearsal_records_total"],
        "validation_records_emitted_count": rollup_obj["validation_records_total"],
        "readiness_probe_records_emitted_count": rollup_obj["readiness_probes_total"],
        "previous_gap_comparison_emitted_count": 1,
        "updated_verdict_emitted_count": 1,
        "contract_result_emitted_count": 1,
        "profile_status": profile_obj["status"],
        "updated_interface_readiness_verdict": rollup_obj["updated_interface_readiness_verdict"],
        "previous_gap_resolved_or_narrowed": rollup_obj["previous_gap_resolved_or_narrowed"],
        "remaining_gap_count": rollup_obj["remaining_gap_count"],
        "cell1_execution_opened_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "proposal_status_promoted_count": 0,
        "builder_command_emitted_count": 0,
        "c4_rerun_count": 0,
        "c5_opened_count": 0,
        "hidden_next_command_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "runtime_patch_applied_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "recommended_next_handling": rollup_obj["recommended_next"],
    }

def transition_trace(verdict: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c3_rerun_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c1_interface_patch",
                "question": "is there a candidate C1 interface patch ready for C3 rerun",
                "answer": SOURCE_C1_PATCH_RECEIPT_ID,
                "taken": "rehearse_micro_domain_interface_against_patch",
            },
            {
                "step": "rehearse_micro_domain_interface_against_patch",
                "question": "does candidate interface cover previous proposal/schema gaps",
                "answer": verdict["verdict"],
                "taken": "emit_updated_c3_verdict",
            },
            {
                "step": "emit_updated_c3_verdict",
                "question": "does C3 now permit C4 preflight rerun",
                "answer": verdict.get("c4_preflight_may_be_rerun_later"),
                "taken": "stop",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_C3_RERUN_READY_FOR_C4_PREFLIGHT_RERUN" if verdict["verdict"] == "CELL1_READY_FOR_NARROW_ACCEPTED_PROPOSAL_TEST" else "STOP_C3_RERUN_STILL_BLOCKED_BY_PROPOSAL_SCHEMA_GAPS",
            "next_command_goal": None,
        },
    }

def validate_outputs(rehearsal_records: List[Dict[str, Any]], validation_records: List[Dict[str, Any]], probes: List[Dict[str, Any]], comparison: Dict[str, Any], verdict: Dict[str, Any], contract: Dict[str, Any], rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any], report_obj: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if not rehearsal_records:
        failures.append("rehearsal_records_missing")
    if any(r.get("status") != "PASS" for r in rehearsal_records):
        failures.append("rehearsal_record_failed")
    if not validation_records:
        failures.append("validation_records_missing")
    if any(v.get("status") != "PASS" for v in validation_records):
        failures.append("validation_record_failed")
    if not probes:
        failures.append("readiness_probes_missing")
    if any(p.get("result") != "PASS" for p in probes):
        failures.append("readiness_probe_failed")
    if comparison.get("remaining_gap_count") != 0:
        failures.append(f"remaining_gap_count_nonzero:{comparison.get('remaining_gap_count')}")
    if verdict.get("verdict") not in ["CELL1_READY_FOR_NARROW_ACCEPTED_PROPOSAL_TEST", "CELL1_NOT_READY_PROPOSAL_SCHEMA_GAPS", "QUESTION_PACKET_NOT_COMMAND"]:
        failures.append(f"invalid_updated_verdict:{verdict.get('verdict')}")
    if verdict.get("verdict") == "CELL1_READY_FOR_NARROW_ACCEPTED_PROPOSAL_TEST" and contract.get("contract_status") != "PASS":
        failures.append("ready_verdict_without_contract")
    if verdict.get("cell1_execution_opened") is not False:
        failures.append("verdict_claims_cell1_execution_opened")
    if verdict.get("cell1_consumption_authorized_now") is not False:
        failures.append("verdict_authorizes_cell1_consumption_now")
    if verdict.get("c4_rerun_executed") is not False:
        failures.append("verdict_claims_c4_rerun_executed")

    for key in ZERO_COUNTER_KEYS:
        if rollup_obj.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup_obj.get(key)}")
    if profile_obj.get("cell1_execution_opened") is not False:
        failures.append("profile_cell1_execution_opened")
    if profile_obj.get("c4_rerun_executed") is not False:
        failures.append("profile_c4_rerun_executed")
    if profile_obj.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")
    for key in [
        "cell1_execution_opened_count",
        "accepted_proposal_fabricated_count",
        "proposal_status_promoted_count",
        "builder_command_emitted_count",
        "c4_rerun_count",
        "c5_opened_count",
        "hidden_next_command_count",
        "taxonomy_registry_mutation_count",
        "runtime_patch_applied_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
    ]:
        if report_obj.get(key) != 0:
            failures.append(f"report_counter_nonzero:{key}:{report_obj.get(key)}")
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
    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") not in ["STOP_C3_RERUN_READY_FOR_C4_PREFLIGHT_RERUN", "STOP_C3_RERUN_STILL_BLOCKED_BY_PROPOSAL_SCHEMA_GAPS"]:
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    rehearsal_records = read_jsonl(PATCHED_INTERFACE_REHEARSAL_RECORDS_PATH)
    validation_records = read_jsonl(PROPOSAL_INTERFACE_VALIDATION_RECORDS_PATH)
    probes = read_jsonl(CELL1_READINESS_PROBE_RECORDS_PATH)
    comparison = read_json(PREVIOUS_GAP_COMPARISON_PATH)
    verdict = read_json(UPDATED_VERDICT_PATH)
    contract = read_json(C3_RERUN_CONTRACT_RESULT_PATH)
    rollup_obj = read_json(ROLLUP_PATH)
    profile_obj = read_json(PROFILE_PATH)
    report_obj = read_json(REPORT_PATH)

    controls: List[Dict[str, Any]] = []

    def add(case: str, failures: List[str], expected_fragment: str) -> None:
        controls.append({
            "case": case,
            "negative_control_pass": any(expected_fragment in f for f in failures),
            "failures": failures,
            "wrote_live_artifact": False,
        })

    bad_rehearsal = copy.deepcopy(rehearsal_records)
    bad_rehearsal[0]["status"] = "MISSING"
    add("patched_interface_section_missing_fail", validate_outputs(bad_rehearsal, validation_records, probes, comparison, verdict, contract, rollup_obj, profile_obj, report_obj), "rehearsal_record_failed")

    bad_validation = copy.deepcopy(validation_records)
    bad_validation[0]["status"] = "FAIL"
    add("proposal_interface_validation_fail", validate_outputs(rehearsal_records, bad_validation, probes, comparison, verdict, contract, rollup_obj, profile_obj, report_obj), "validation_record_failed")

    bad_probes = copy.deepcopy(probes)
    bad_probes[0]["result"] = "FAIL"
    add("readiness_probe_fail", validate_outputs(rehearsal_records, validation_records, bad_probes, comparison, verdict, contract, rollup_obj, profile_obj, report_obj), "readiness_probe_failed")

    bad_comparison = copy.deepcopy(comparison)
    bad_comparison["remaining_gap_count"] = 1
    add("remaining_gap_count_nonzero_fail", validate_outputs(rehearsal_records, validation_records, probes, bad_comparison, verdict, contract, rollup_obj, profile_obj, report_obj), "remaining_gap_count_nonzero")

    bad_contract = copy.deepcopy(contract)
    bad_contract["contract_status"] = "FAIL"
    add("ready_verdict_without_contract_fail", validate_outputs(rehearsal_records, validation_records, probes, comparison, verdict, bad_contract, rollup_obj, profile_obj, report_obj), "ready_verdict_without_contract")

    bad_verdict = copy.deepcopy(verdict)
    bad_verdict["cell1_execution_opened"] = True
    add("verdict_claims_cell1_execution_fail", validate_outputs(rehearsal_records, validation_records, probes, comparison, bad_verdict, contract, rollup_obj, profile_obj, report_obj), "verdict_claims_cell1_execution_opened")

    bad_verdict = copy.deepcopy(verdict)
    bad_verdict["cell1_consumption_authorized_now"] = True
    add("verdict_authorizes_cell1_now_fail", validate_outputs(rehearsal_records, validation_records, probes, comparison, bad_verdict, contract, rollup_obj, profile_obj, report_obj), "verdict_authorizes_cell1_consumption_now")

    bad_verdict = copy.deepcopy(verdict)
    bad_verdict["c4_rerun_executed"] = True
    add("verdict_claims_c4_rerun_fail", validate_outputs(rehearsal_records, validation_records, probes, comparison, bad_verdict, contract, rollup_obj, profile_obj, report_obj), "verdict_claims_c4_rerun_executed")

    for case, counter in [
        ("cell1_execution_opened_fail", "cell1_execution_opened_count"),
        ("accepted_proposal_fabricated_fail", "accepted_proposal_fabricated_count"),
        ("proposal_status_promoted_fail", "proposal_status_promoted_count"),
        ("builder_command_emitted_fail", "builder_command_emitted_count"),
        ("c4_rerun_inside_c3_rerun_fail", "c4_rerun_count"),
        ("c5_opened_inside_c3_rerun_fail", "c5_opened_count"),
        ("taxonomy_registry_mutated_fail", "taxonomy_registry_mutation_count"),
        ("runtime_patch_applied_fail", "runtime_patch_applied_count"),
        ("hidden_next_command_fail", "hidden_next_command_count"),
        ("source_mutation_fail", "source_mutation_count"),
        ("prior_receipt_mutation_fail", "prior_receipt_mutation_count"),
        ("ready_verdict_counted_as_cell1_execution_fail", "ready_verdict_counted_as_cell1_execution_count"),
    ]:
        bad_rollup = copy.deepcopy(rollup_obj)
        bad_report = copy.deepcopy(report_obj)
        bad_rollup[counter] = 1
        if counter in bad_report:
            bad_report[counter] = 1
        add(case, validate_outputs(rehearsal_records, validation_records, probes, comparison, verdict, contract, bad_rollup, profile_obj, bad_report), counter)

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_C3_RERUN_DEPENDENCY_MISSING", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "c3_rerun_against_c1_interface_patch_receipt_v0",
            "receipt_type": "C3_RERUN_AGAINST_C1_INTERFACE_PATCH_RECEIPT",
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
        print(f"c3_rerun_receipt_id={receipt_id}")
        print(f"c3_rerun_receipt_path=data/c3_micro_domain_shift_rerun_against_c1_interface_patch_v0_receipts/{receipt_id}.json")
        return 1

    rehearsal_records = make_rehearsal_records()
    validation_records = make_validation_records()
    probes = make_readiness_probes(rehearsal_records, validation_records)
    comparison = previous_gap_comparison(rehearsal_records)
    verdict = updated_verdict(probes, comparison)
    contract = contract_result(verdict)
    rollup_obj = rollup(rehearsal_records, validation_records, probes, comparison, verdict, contract)
    profile_obj = profile(rollup_obj)
    report_obj = report(rollup_obj, profile_obj)
    trace = transition_trace(verdict)

    write_json(SOURCE_SURFACE_PATH, source_surface())
    write_jsonl(PATCHED_INTERFACE_REHEARSAL_RECORDS_PATH, rehearsal_records)
    write_jsonl(PROPOSAL_INTERFACE_VALIDATION_RECORDS_PATH, validation_records)
    write_jsonl(CELL1_READINESS_PROBE_RECORDS_PATH, probes)
    write_json(PREVIOUS_GAP_COMPARISON_PATH, comparison)
    write_json(UPDATED_VERDICT_PATH, verdict)
    write_json(C3_RERUN_CONTRACT_RESULT_PATH, contract)
    write_json(ROLLUP_PATH, rollup_obj)
    write_json(PROFILE_PATH, profile_obj)
    write_json(REPORT_PATH, report_obj)
    write_json(TRANSITION_TRACE_PATH, trace)

    failures.extend(validate_outputs(rehearsal_records, validation_records, probes, comparison, verdict, contract, rollup_obj, profile_obj, report_obj))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup_obj["source_mutation_count"] = 1
        report_obj["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup_obj)
        write_json(REPORT_PATH, report_obj)

    acceptance_gate_results = {
        "C3_RERUN_0_C1_INTERFACE_PATCH_RECEIPT_CONSUMED": SOURCE_C1_PATCH_RECEIPT_PATH.exists(),
        "C3_RERUN_1_PATCHED_SCHEMA_CONSUMED": SOURCE_C1_PATCH_SCHEMA_PATH.exists(),
        "C3_RERUN_2_C3_RERUN_CONTRACT_CONSUMED": SOURCE_C1_PATCH_RERUN_CONTRACT_PATH.exists(),
        "C3_RERUN_3_ORIGINAL_C3_GAP_REPORT_CONSUMED": SOURCE_C3_GAP_REPORTS_PATH.exists(),
        "C3_RERUN_4_C4_BLOCKED_PREFLIGHT_BASIS_CONSUMED": SOURCE_C4_PREFLIGHT_RECEIPT_PATH.exists(),
        "C3_RERUN_5_C2_LANE_REGISTRY_CONSUMED": SOURCE_C2_LANE_REGISTRY_PATH.exists(),
        "C3_RERUN_6_PATCHED_INTERFACE_REHEARSAL_RECORDS_EMITTED": len(rehearsal_records) > 0,
        "C3_RERUN_7_PROPOSAL_INTERFACE_VALIDATION_RECORDS_EMITTED": len(validation_records) > 0,
        "C3_RERUN_8_CELL1_READINESS_PROBES_EMITTED": len(probes) > 0,
        "C3_RERUN_9_PREVIOUS_GAP_COMPARISON_EMITTED": PREVIOUS_GAP_COMPARISON_PATH.exists(),
        "C3_RERUN_10_UPDATED_VERDICT_EMITTED": UPDATED_VERDICT_PATH.exists(),
        "C3_RERUN_11_UPDATED_VERDICT_ALLOWED_BY_CONTRACT": contract["contract_status"] == "PASS",
        "C3_RERUN_12_PREVIOUS_GAP_RESOLVED_OR_NARROWED": comparison["previous_gap_resolved_or_narrowed"] is True and comparison["remaining_gap_count"] == 0,
        "C3_RERUN_13_VERDICT_READY_FOR_NARROW_ACCEPTED_PROPOSAL_TEST": verdict["verdict"] == "CELL1_READY_FOR_NARROW_ACCEPTED_PROPOSAL_TEST",
        "C3_RERUN_14_NO_CELL1_EXECUTION_OPENED": rollup_obj["cell1_execution_opened_count"] == 0 and verdict["cell1_execution_opened"] is False,
        "C3_RERUN_15_NO_ACCEPTED_PROPOSAL_FABRICATED": rollup_obj["accepted_proposal_fabricated_count"] == 0,
        "C3_RERUN_16_NO_C4_RERUN_IN_THIS_UNIT": rollup_obj["c4_rerun_count"] == 0 and verdict["c4_rerun_executed"] is False,
        "C3_RERUN_17_NO_C5_OPENED": rollup_obj["c5_opened_count"] == 0,
        "C3_RERUN_18_NO_TAXONOMY_MUTATION": rollup_obj["taxonomy_registry_mutation_count"] == 0,
        "C3_RERUN_19_NO_RUNTIME_PATCH": rollup_obj["runtime_patch_applied_count"] == 0,
        "C3_RERUN_20_NO_HIDDEN_NEXT_COMMAND": rollup_obj["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
        "C3_RERUN_21_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_c1_patch": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c3": SOURCE_C3_RECEIPT_ID,
        "updated_verdict": verdict["verdict"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "patched_interface_rehearsal_records": rel(PATCHED_INTERFACE_REHEARSAL_RECORDS_PATH),
        "proposal_interface_validation_records": rel(PROPOSAL_INTERFACE_VALIDATION_RECORDS_PATH),
        "cell1_readiness_probe_records": rel(CELL1_READINESS_PROBE_RECORDS_PATH),
        "previous_gap_comparison": rel(PREVIOUS_GAP_COMPARISON_PATH),
        "c3_rerun_contract_result": rel(C3_RERUN_CONTRACT_RESULT_PATH),
        "updated_interface_readiness_verdict": rel(UPDATED_VERDICT_PATH),
        "rollup": rel(ROLLUP_PATH),
        "profile": rel(PROFILE_PATH),
        "report": rel(REPORT_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_c1_patch_receipt": rel(SOURCE_C1_PATCH_RECEIPT_PATH),
        "source_c1_patch_schema": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "source_c3_receipt": rel(SOURCE_C3_RECEIPT_PATH),
        "source_c4_preflight_receipt": rel(SOURCE_C4_PREFLIGHT_RECEIPT_PATH),
        "source_c2_lane_registry": rel(SOURCE_C2_LANE_REGISTRY_PATH),
    }

    guards = {
        "build_mode_rerun_against_candidate_interface_patch_only": BUILD_MODE == "RERUN_AGAINST_CANDIDATE_INTERFACE_PATCH_ONLY",
        "candidate_interface_patch_consumed": True,
        "original_c3_gap_report_consumed": True,
        "previous_gap_resolved_or_narrowed": comparison["previous_gap_resolved_or_narrowed"],
        "updated_verdict_ready_for_c4_preflight": verdict["verdict"] == "CELL1_READY_FOR_NARROW_ACCEPTED_PROPOSAL_TEST",
        "cell1_execution_opened": False,
        "accepted_proposal_fabricated": False,
        "proposal_status_promoted": False,
        "builder_command_emitted": False,
        "c4_rerun_executed": False,
        "c5_opened": False,
        "taxonomy_registry_mutated": False,
        "runtime_patch_applied": False,
        "hidden_next_command": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
    }

    receipt = {
        "schema_version": "c3_rerun_against_c1_interface_patch_receipt_v0",
        "receipt_type": "C3_RERUN_AGAINST_C1_INTERFACE_PATCH_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "C3 micro-domain shift rehearsal against C1 proposal interface patch candidate",
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_original_c3_receipt_id": SOURCE_C3_RECEIPT_ID,
        "source_c4_preflight_receipt_id": SOURCE_C4_PREFLIGHT_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "c3_rerun_summary": {
            "profile_status": profile_obj["status"],
            "previous_verdict": verdict["previous_verdict"],
            "updated_interface_readiness_verdict": verdict["verdict"],
            "verdict_changed": verdict["verdict_changed"],
            "previous_gap_resolved_or_narrowed": comparison["previous_gap_resolved_or_narrowed"],
            "remaining_gap_count": comparison["remaining_gap_count"],
            "rehearsal_records_total": rollup_obj["rehearsal_records_total"],
            "readiness_probes_total": rollup_obj["readiness_probes_total"],
            "readiness_probes_passed": rollup_obj["readiness_probes_passed"],
            "cell1_execution_opened": False,
            "c4_rerun_executed": False,
            "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
            "recommended_next": rollup_obj["recommended_next"],
        },
        "aggregate_metrics": {
            **{k: v for k, v in report_obj.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
            "rollup": rollup_obj,
            "source_mutation_count": 1 if source_mutation_detected else report_obj["source_mutation_count"],
        },
        "acceptance_gate_results": acceptance_gate_results,
        "c3_rerun_guards": guards,
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
    if len(negative_controls) != 20 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
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
    print(f"c3_rerun_receipt_id={receipt_id}")
    print(f"c3_rerun_receipt_path=data/c3_micro_domain_shift_rerun_against_c1_interface_patch_v0_receipts/{receipt_id}.json")
    print(f"c3_rerun_profile_path=data/c3_micro_domain_shift_rerun_against_c1_interface_patch_v0/c3_rerun_profile_v0.json")
    print(f"c3_rerun_rollup_path=data/c3_micro_domain_shift_rerun_against_c1_interface_patch_v0/c3_rerun_rollup_v0.json")
    print(f"c3_rerun_verdict_path=data/c3_micro_domain_shift_rerun_against_c1_interface_patch_v0/c3_interface_readiness_verdict_v0_1.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
