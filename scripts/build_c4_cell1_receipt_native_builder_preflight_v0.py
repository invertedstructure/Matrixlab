#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_C4_CELL1_RECEIPT_NATIVE_BUILDER_PREFLIGHT_V0"
TARGET_UNIT_ID = "c4.cell1.receipt_native_builder.preflight.v0"
LAYER = "CELL_1 / RECEIPT_NATIVE_BUILDER_PREFLIGHT"
MODE = "PREFLIGHT / GATE / SCHEMA"
BUILD_MODE = "PREFLIGHT_GATE_ONLY"

SOURCE_C3_RECEIPT_ID = "cfc79da2"
SOURCE_C3_RECEIPT_PATH = ROOT / "data" / "c3_cell0_micro_domain_shift_rehearsal_v0_receipts" / "cfc79da2.json"
SOURCE_C3_PROFILE_PATH = ROOT / "data" / "c3_cell0_micro_domain_shift_rehearsal_v0" / "c3_micro_domain_shift_profile_v0.json"
SOURCE_C3_ROLLUP_PATH = ROOT / "data" / "c3_cell0_micro_domain_shift_rehearsal_v0" / "micro_domain_shift_rollup_v0.json"
SOURCE_C3_VERDICT_PATH = ROOT / "data" / "c3_cell0_micro_domain_shift_rehearsal_v0" / "c3_interface_readiness_verdict_v0.json"
SOURCE_C3_GAP_REPORTS_PATH = ROOT / "data" / "c3_cell0_micro_domain_shift_rehearsal_v0" / "domain_shift_proposal_gap_reports_v0.jsonl"

SOURCE_C1_RECEIPT_ID = "f8f37c4e"
SOURCE_C1_RECEIPT_PATH = ROOT / "data" / "c1_cell0_proposal_layer_v0_receipts" / "f8f37c4e.json"
SOURCE_C1_PACKET_SCHEMA_PATH = ROOT / "data" / "c1_cell0_proposal_layer_v0" / "proposal_packet_schema_v0.json"

SOURCE_C2_RECEIPT_ID = "348dabde"
SOURCE_C2_RECEIPT_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts" / "348dabde.json"
SOURCE_C2_TAXONOMY_LANE_REGISTRY_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "taxonomy_lane_registry_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C3_RECEIPT_PATH,
    SOURCE_C3_PROFILE_PATH,
    SOURCE_C3_ROLLUP_PATH,
    SOURCE_C3_VERDICT_PATH,
    SOURCE_C3_GAP_REPORTS_PATH,
    SOURCE_C1_RECEIPT_PATH,
    SOURCE_C1_PACKET_SCHEMA_PATH,
    SOURCE_C2_RECEIPT_PATH,
    SOURCE_C2_TAXONOMY_LANE_REGISTRY_PATH,
]

OUT_DIR = ROOT / "data" / "c4_cell1_receipt_native_builder_v0"
RECEIPT_DIR = ROOT / "data" / "c4_cell1_receipt_native_builder_v0_receipts"

AUTHORITY_PROFILE_PATH = OUT_DIR / "cell1_builder_authority_profile_v0.json"
ACCEPTED_PROPOSAL_INPUT_SCHEMA_PATH = OUT_DIR / "cell1_accepted_proposal_input_schema_v0.json"
PATCH_PLAN_SCHEMA_PATH = OUT_DIR / "cell1_minimal_patch_plan_schema_v0.json"
PATCH_RECORD_SCHEMA_PATH = OUT_DIR / "cell1_patch_record_schema_v0.json"
PROBE_RECORD_SCHEMA_PATH = OUT_DIR / "cell1_probe_record_schema_v0.json"
VERIFICATION_RECORD_SCHEMA_PATH = OUT_DIR / "cell1_verification_record_schema_v0.json"
BUILD_RECEIPT_SCHEMA_PATH = OUT_DIR / "cell1_build_receipt_schema_v0.json"
HANDOFF_RECEIPT_SCHEMA_PATH = OUT_DIR / "cell1_handoff_receipt_schema_v0.json"
BUILDER_LOOP_TRACE_SCHEMA_PATH = OUT_DIR / "cell1_builder_loop_trace_schema_v0.json"
OPENING_GATE_EVALUATION_PATH = OUT_DIR / "c4_opening_gate_evaluation_v0.json"
BLOCKED_PREFLIGHT_ROLLUP_PATH = OUT_DIR / "c4_blocked_preflight_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c4_cell1_builder_profile_v0.json"
TRANSITION_TRACE_PATH = OUT_DIR / "c4_transition_trace.json"
REPORT_PATH = OUT_DIR / "c4_report.json"

ALLOWED_C3_VERDICT = "CELL1_READY_FOR_NARROW_ACCEPTED_PROPOSAL_TEST"
BLOCKED_C3_VERDICTS = [
    "CELL1_NOT_READY_PROPOSAL_SCHEMA_GAPS",
    "CELL1_BLOCKED_BY_LABEL_COLLAPSE",
    "CELL1_BLOCKED_BY_LOOP_GAP",
    "CELL1_BLOCKED_BY_AUTHORITY_GAP",
    "CELL1_BLOCKED_BY_EXTRACTION_GAP",
    "CELL1_BLOCKED_BY_RECEIPT_GAP",
    "CELL1_READINESS_UNCLASSIFIED",
]

ZERO_COUNTER_KEYS = [
    "proposed_only_packet_consumed_count",
    "proposal_accepted_by_cell1_count",
    "scope_expansion_count",
    "extra_objective_invented_count",
    "forbidden_input_touched_count",
    "unbounded_payload_inspection_count",
    "patch_without_plan_count",
    "patch_without_authority_count",
    "patch_without_verification_count",
    "verification_pass_counted_as_global_correctness_count",
    "build_success_counted_as_proposal_closure_without_review_count",
    "auto_chain_next_build_count",
    "cell1_opened_new_objective_count",
    "cell1_execution_opened_count",
    "cell1_opened_despite_c3_block_count",
    "schema_only_artifact_counted_as_build_count",
    "blocked_preflight_counted_as_failure_count",
    "accepted_proposal_fabricated_count",
    "patch_applied_during_preflight_count",
    "probe_run_during_preflight_count",
    "verification_pass_emitted_during_preflight_count",
    "builder_command_emitted_count",
    "hidden_next_command_count",
    "source_mutation_count",
    "prior_receipt_mutation_count",
]

HUMAN_DECISION = {
    "decision": "BUILD_C4_CELL1_RECEIPT_NATIVE_BUILDER_PREFLIGHT",
    "scope": "Build C4 as a preflight/gate surface for the first narrow Cell 1 receipt-native builder. Emit Cell 1 authority profile, accepted proposal input schema, builder loop record schemas, opening gate evaluation, blocked preflight rollup, profile, report, and receipt. Because C3 currently reports CELL1_NOT_READY_PROPOSAL_SCHEMA_GAPS, do not consume any proposal, do not open Cell 1 execution, do not apply patches, do not run probes, and stop with STOP_C4_BLOCKED_BY_C3_INTERFACE_VERDICT.",
    "authorized": [
        "consume C3 interface verdict",
        "consume C1/C2/C3 receipt basis",
        "emit Cell 1 builder authority profile",
        "emit accepted proposal input schema",
        "emit Cell 1 builder loop schemas",
        "emit opening gate evaluation",
        "emit blocked preflight rollup",
        "emit C4 profile",
        "emit C4 report",
        "emit C4 receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "consume accepted proposal as build input",
        "consume PROPOSED_ONLY packet",
        "accept proposal",
        "apply patch",
        "run builder probe",
        "emit verification PASS",
        "emit build verified receipt",
        "open Cell 1 execution",
        "mutate taxonomy",
        "touch target files",
        "auto-chain next build",
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

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def validate_source_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    c3_receipt = read_json(SOURCE_C3_RECEIPT_PATH)
    c3_profile = read_json(SOURCE_C3_PROFILE_PATH)
    c3_rollup = read_json(SOURCE_C3_ROLLUP_PATH)
    c3_verdict = read_json(SOURCE_C3_VERDICT_PATH)
    c1_receipt = read_json(SOURCE_C1_RECEIPT_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)

    if c3_receipt.get("receipt_id") != SOURCE_C3_RECEIPT_ID or c3_receipt.get("gate") != "PASS":
        failures.append("c3_basis_not_accepted")
    if c3_profile.get("status") != "C3_MICRO_SHIFT_REHEARSAL_COMPLETE":
        failures.append("c3_profile_not_complete")
    if c3_rollup.get("interface_readiness_verdict") != "CELL1_NOT_READY_PROPOSAL_SCHEMA_GAPS":
        failures.append(f"c3_rollup_unexpected_verdict:{c3_rollup.get('interface_readiness_verdict')}")
    if c3_verdict.get("verdict") != "CELL1_NOT_READY_PROPOSAL_SCHEMA_GAPS":
        failures.append(f"c3_verdict_unexpected:{c3_verdict.get('verdict')}")
    if c1_receipt.get("receipt_id") != SOURCE_C1_RECEIPT_ID or c1_receipt.get("gate") != "PASS":
        failures.append("c1_basis_not_accepted")
    if c2_receipt.get("receipt_id") != SOURCE_C2_RECEIPT_ID or c2_receipt.get("gate") != "PASS":
        failures.append("c2_basis_not_accepted")
    if len(read_jsonl(SOURCE_C3_GAP_REPORTS_PATH)) < 1:
        failures.append("c3_gap_report_basis_missing")
    return failures

def authority_profile() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_builder_authority_profile_v0",
        "cell_id": "CELL_1",
        "allowed": [
            "consume accepted proposal packets",
            "produce minimal patch plan",
            "apply bounded patch if authorized",
            "run bounded probe",
            "emit verification, build, and handoff receipts",
        ],
        "forbidden": [
            "consume proposed-only packets",
            "accept proposals",
            "invent new objectives",
            "widen scope",
            "auto-chain builds",
            "mutate registries without accepted proposal",
            "claim global correctness",
        ],
        "default_on_ambiguity": "STOP",
        "preflight_status": "DEFINED_BUT_NOT_OPENED",
    }

def accepted_proposal_input_schema() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_accepted_proposal_input_schema_v0",
        "required_fields": [
            "proposal_id",
            "proposal_type",
            "status",
            "review_receipt_ref",
            "bounded_objective",
            "target_surface",
            "allowed_inputs",
            "forbidden_inputs",
            "expected_patch_shape",
            "verification_requirement",
            "stop_conditions",
        ],
        "accepted_statuses": [
            "ACCEPTED_FOR_BUILD",
            "ACCEPTED_FOR_TAXONOMY_PATCH",
            "ACCEPTED_FOR_EXTRACTION",
            "ACCEPTED_FOR_OBSERVABILITY_PATCH",
            "ACCEPTED_FOR_MOVE_REGISTRATION",
        ],
        "rejected_statuses": [
            "PROPOSED_ONLY",
            "UNDER_REVIEW",
            "DEFERRED",
            "REJECTED",
            "PARKED",
            "EVIDENCE_REQUIRED",
            "NARROWING_REQUIRED",
            "SUPERSEDED",
        ],
        "preflight_rule": "No proposal may be consumed while C3 interface verdict blocks Cell 1.",
    }

def patch_plan_schema() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_minimal_patch_plan_schema_v0",
        "plan_schema": {
            "schema_version": "cell1_minimal_patch_plan_v0",
            "patch_plan_id": "patch_plan_<sig8>",
            "proposal_id": None,
            "proposal_type": None,
            "target_surface": None,
            "planned_change": None,
            "files_expected_to_change": [],
            "files_forbidden_to_change": [],
            "objects_expected_to_change": [],
            "objects_forbidden_to_change": [],
            "expected_tests": [],
            "scope_risk": "LOW | MEDIUM | HIGH",
            "requires_review_before_apply": False,
        },
        "preflight_status": "SCHEMA_ONLY",
    }

def patch_record_schema() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_patch_record_schema_v0",
        "record_schema": {
            "schema_version": "cell1_patch_record_v0",
            "patch_id": "patch_<sig8>",
            "proposal_id": None,
            "patch_plan_ref": None,
            "patch_status": "APPLIED | NOT_APPLIED",
            "changed_files": [],
            "changed_objects": [],
            "scope_expansion_count": 0,
            "forbidden_file_touch_count": 0,
            "forbidden_object_touch_count": 0,
        },
        "preflight_status": "SCHEMA_ONLY_NO_PATCH",
    }

def probe_record_schema() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_probe_record_schema_v0",
        "record_schema": {
            "schema_version": "cell1_probe_record_v0",
            "probe_id": "probe_<sig8>",
            "proposal_id": None,
            "patch_id": None,
            "probe_kind": "TARGETED_TEST | SCHEMA_VALIDATION | NEGATIVE_CONTROL | RECEIPT_COMPARISON | LABEL_AUDIT | EXTRACTION_BOUNDARY_CHECK",
            "command_or_test_ref": None,
            "result": "PASS | FAIL | NA",
            "logs_ref": None,
        },
        "preflight_status": "SCHEMA_ONLY_NO_PROBE",
    }

def verification_record_schema() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_verification_record_schema_v0",
        "record_schema": {
            "schema_version": "cell1_verification_record_v0",
            "verification_id": "verify_<sig8>",
            "proposal_id": None,
            "patch_id": None,
            "expected_gate": None,
            "observed": {},
            "negative_controls": {},
            "verification_status": "PASS | FAIL | NA_MISSING_FIXTURE | NA_MISSING_TARGET | NA_UNAUTHORIZED_TEST",
            "must_not_infer": [
                "global correctness",
                "future failures impossible",
                "unrelated proposal accepted",
                "Cell 1 can build generally",
            ],
        },
        "preflight_status": "SCHEMA_ONLY_NO_VERIFICATION",
    }

def build_receipt_schema() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_build_receipt_schema_v0",
        "receipt_schema": {
            "schema_version": "cell1_build_receipt_v0",
            "build_receipt_id": "build_<sig8>",
            "cell_id": "CELL_1",
            "input_proposal": {
                "proposal_id": None,
                "proposal_type": None,
                "status": None,
                "review_receipt_ref": None,
            },
            "build_scope": {
                "bounded_objective": None,
                "target_surface": None,
                "allowed_inputs_used": [],
                "forbidden_inputs_touched": [],
            },
            "patch": {
                "patch_plan_ref": None,
                "patch_record_ref": None,
                "patch_status": "APPLIED | NOT_APPLIED",
            },
            "verification": {
                "verification_record_ref": None,
                "verification_status": "PASS | FAIL | NA",
            },
            "negative_controls": {},
            "handoff": {
                "return_to": "CELL_0_OR_REVIEW",
                "handoff_status": None,
            },
            "terminal": {
                "type": "STOP",
                "stop_code": None,
                "next_command_goal": None,
            },
        },
        "preflight_status": "SCHEMA_ONLY_NO_BUILD_RECEIPT_INSTANCE",
    }

def handoff_receipt_schema() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_receipt_schema_v0",
        "handoff_schema": {
            "schema_version": "cell1_handoff_receipt_v0",
            "handoff_id": "handoff_<sig8>",
            "from_cell": "CELL_1",
            "to": "CELL_0_OR_REVIEW",
            "proposal_id": None,
            "build_receipt_ref": None,
            "handoff_status": None,
            "allowed_next_handling": [
                "Cell 0 may consume verification receipt",
                "review may close proposal",
                "if failure recurs, emit new failure progress record",
            ],
            "forbidden_next_handling": [
                "Cell 1 continues to next proposal automatically",
                "Cell 1 opens new build objective",
                "verification pass treated as global correctness",
            ],
        },
        "preflight_status": "SCHEMA_ONLY_NO_HANDOFF_INSTANCE",
    }

def loop_trace_schema() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_builder_loop_trace_schema_v0",
        "loop_steps": [
            "LOAD_ACCEPTED_PROPOSAL",
            "VALIDATE_ACCEPTANCE",
            "VALIDATE_SCOPE",
            "LOAD_TARGET_SURFACE",
            "PLAN_MINIMAL_PATCH",
            "CHECK_PATCH_AUTHORITY",
            "APPLY_PATCH_OR_STOP",
            "RUN_BOUNDED_PROBE",
            "VERIFY_GATE",
            "EMIT_BUILD_RECEIPT",
            "HANDOFF_TO_CELL0_OR_REVIEW",
            "STOP",
        ],
        "preflight_status": "DECLARED_NOT_EXECUTED",
        "rule": "No loop step may execute while C3 interface verdict blocks Cell 1.",
    }

def schema_outputs() -> Dict[Path, Dict[str, Any]]:
    return {
        AUTHORITY_PROFILE_PATH: authority_profile(),
        ACCEPTED_PROPOSAL_INPUT_SCHEMA_PATH: accepted_proposal_input_schema(),
        PATCH_PLAN_SCHEMA_PATH: patch_plan_schema(),
        PATCH_RECORD_SCHEMA_PATH: patch_record_schema(),
        PROBE_RECORD_SCHEMA_PATH: probe_record_schema(),
        VERIFICATION_RECORD_SCHEMA_PATH: verification_record_schema(),
        BUILD_RECEIPT_SCHEMA_PATH: build_receipt_schema(),
        HANDOFF_RECEIPT_SCHEMA_PATH: handoff_receipt_schema(),
        BUILDER_LOOP_TRACE_SCHEMA_PATH: loop_trace_schema(),
    }

def opening_gate_evaluation() -> Dict[str, Any]:
    verdict = read_json(SOURCE_C3_VERDICT_PATH)
    c3_verdict = verdict.get("verdict")
    blocked = c3_verdict in BLOCKED_C3_VERDICTS
    return {
        "schema_version": "c4_opening_gate_evaluation_v0",
        "source_c3_receipt_id": SOURCE_C3_RECEIPT_ID,
        "source_c3_verdict_ref": rel(SOURCE_C3_VERDICT_PATH),
        "allowed_verdict": ALLOWED_C3_VERDICT,
        "observed_verdict": c3_verdict,
        "blocked_verdicts": BLOCKED_C3_VERDICTS,
        "c4_opening_gate_status": "BLOCKED" if blocked else "OPEN",
        "blocking_reason": "C3_INTERFACE_VERDICT" if blocked else None,
        "cell1_execution_opened": False,
        "accepted_proposal_consumption_allowed": False if blocked else True,
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_C4_BLOCKED_BY_C3_INTERFACE_VERDICT" if blocked else "STOP_C4_PREFLIGHT_READY_FOR_ACCEPTED_PROPOSAL",
            "next_command_goal": None,
        },
    }

def blocked_preflight_rollup(gate: Dict[str, Any]) -> Dict[str, Any]:
    neg = {key: 0 for key in ZERO_COUNTER_KEYS}
    return {
        "schema_version": "c4_blocked_preflight_rollup_v0",
        "build_mode": BUILD_MODE,
        "c3_interface_verdict_checked": True,
        "c3_interface_verdict": gate["observed_verdict"],
        "c4_opening_gate_status": gate["c4_opening_gate_status"],
        "accepted_proposals_consumed": 0,
        "builds_attempted": 0,
        "builds_verified": 0,
        "builds_failed": 0,
        "builds_blocked": 1 if gate["c4_opening_gate_status"] == "BLOCKED" else 0,
        "schemas_emitted": True,
        "cell1_execution_opened": False,
        "negative_controls": neg,
        "handoff_summary": {
            "returned_to_cell0": 0,
            "returned_to_review": 0,
            "parked": 0,
        },
        "recommended_next": None,
    }

def profile(rollup: Dict[str, Any]) -> Dict[str, Any]:
    bad_zero = all(rollup["negative_controls"].get(k) == 0 for k in ZERO_COUNTER_KEYS)
    return {
        "schema_version": "c4_cell1_receipt_native_builder_profile_v0",
        "profile_id": "c4_cell1_builder_" + sha8({"verdict": rollup["c3_interface_verdict"], "blocked": rollup["builds_blocked"]}),
        "status": "C4_BLOCKED",
        "cell_id": "CELL_1",
        "active_object": "one accepted proposal packet",
        "build_mode": BUILD_MODE,
        "builder_authority_profile_ref": rel(AUTHORITY_PROFILE_PATH),
        "build_rollup_ref": rel(BLOCKED_PREFLIGHT_ROLLUP_PATH),
        "core_rule": "Cell 1 may build only what Cell 0 proposed and review accepted.",
        "handoff_rule": "Cell 1 must return verification/build/handoff receipts and stop.",
        "bad_counters_zero": bad_zero,
        "must_not_infer": [
            "Cell 1 is a general builder",
            "proposal is enough without acceptance",
            "build success is verification success",
            "verification pass is global correctness",
            "one accepted proposal grants broad builder authority",
            "Cell 2 is authorized",
        ],
        "next_command_goal": None,
    }

def transition_trace(gate: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c4_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c3_interface_verdict",
                "question": "does C3 permit narrow accepted proposal Cell 1 test",
                "answer": gate["observed_verdict"],
                "taken": "block_cell1_opening",
            },
            {
                "step": "emit_schema_only_surface",
                "question": "can C4 define Cell 1 intake/build receipt schemas without execution",
                "answer": True,
                "taken": "emit_blocked_preflight_receipt",
            },
            {
                "step": "emit_blocked_preflight_receipt",
                "question": "did C4 stop without opening Cell 1",
                "answer": gate["cell1_execution_opened"] is False,
                "taken": "stop",
            },
        ],
        "terminal": gate["terminal"],
    }

def report(gate: Dict[str, Any], rollup: Dict[str, Any], prof: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c4_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_design_consumed_count": 1,
        "c3_interface_verdict_checked_count": 1,
        "c3_interface_blocked_count": 1 if gate["c4_opening_gate_status"] == "BLOCKED" else 0,
        "builder_authority_profile_emitted_count": 1,
        "accepted_proposal_input_schema_emitted_count": 1,
        "builder_loop_schemas_emitted_count": 7,
        "opening_gate_evaluation_emitted_count": 1,
        "blocked_preflight_rollup_emitted_count": 1,
        "profile_emitted_count": 1,
        "profile_status": prof["status"],
        "accepted_proposals_consumed": rollup["accepted_proposals_consumed"],
        "builds_attempted": rollup["builds_attempted"],
        "builds_verified": rollup["builds_verified"],
        "builds_blocked": rollup["builds_blocked"],
        "cell1_execution_opened_count": 0,
        "cell1_opened_despite_c3_block_count": 0,
        "schema_only_artifact_counted_as_build_count": 0,
        "blocked_preflight_counted_as_failure_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "patch_applied_during_preflight_count": 0,
        "probe_run_during_preflight_count": 0,
        "verification_pass_emitted_during_preflight_count": 0,
        "builder_command_emitted_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "latest_or_mtime_selection_count": 0,
        "ambient_workspace_inference_count": 0,
        "recommended_next_handling": None,
    }

def validate_rollup(rollup: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if rollup["build_mode"] != BUILD_MODE:
        failures.append("rollup_build_mode_wrong")
    if rollup["c3_interface_verdict_checked"] is not True:
        failures.append("c3_verdict_not_checked")
    if rollup["c3_interface_verdict"] != "CELL1_NOT_READY_PROPOSAL_SCHEMA_GAPS":
        failures.append(f"wrong_c3_verdict:{rollup['c3_interface_verdict']}")
    if rollup["c4_opening_gate_status"] != "BLOCKED":
        failures.append(f"opening_gate_not_blocked:{rollup['c4_opening_gate_status']}")
    if rollup["accepted_proposals_consumed"] != 0:
        failures.append(f"accepted_proposals_consumed_nonzero:{rollup['accepted_proposals_consumed']}")
    if rollup["builds_attempted"] != 0:
        failures.append(f"builds_attempted_nonzero:{rollup['builds_attempted']}")
    if rollup["builds_verified"] != 0:
        failures.append(f"builds_verified_nonzero:{rollup['builds_verified']}")
    if rollup["builds_blocked"] != 1:
        failures.append(f"builds_blocked_not_one:{rollup['builds_blocked']}")
    if rollup["cell1_execution_opened"] is not False:
        failures.append("cell1_execution_opened_true")
    for key in ZERO_COUNTER_KEYS:
        if rollup["negative_controls"].get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup['negative_controls'].get(key)}")
    return failures

def validate_report(report_obj: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    for key in [
        "source_design_consumed_count",
        "c3_interface_verdict_checked_count",
        "c3_interface_blocked_count",
        "builder_authority_profile_emitted_count",
        "accepted_proposal_input_schema_emitted_count",
        "opening_gate_evaluation_emitted_count",
        "blocked_preflight_rollup_emitted_count",
        "profile_emitted_count",
    ]:
        if report_obj.get(key) != 1:
            failures.append(f"report_metric_not_one:{key}:{report_obj.get(key)}")
    for key in [
        "accepted_proposals_consumed",
        "builds_attempted",
        "builds_verified",
        "cell1_execution_opened_count",
        "cell1_opened_despite_c3_block_count",
        "schema_only_artifact_counted_as_build_count",
        "blocked_preflight_counted_as_failure_count",
        "accepted_proposal_fabricated_count",
        "patch_applied_during_preflight_count",
        "probe_run_during_preflight_count",
        "verification_pass_emitted_during_preflight_count",
        "builder_command_emitted_count",
        "hidden_next_command_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "latest_or_mtime_selection_count",
        "ambient_workspace_inference_count",
    ]:
        if report_obj.get(key) != 0:
            failures.append(f"report_metric_not_zero:{key}:{report_obj.get(key)}")
    if report_obj.get("builds_blocked") != 1:
        failures.append(f"report_builds_blocked_not_one:{report_obj.get('builds_blocked')}")
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
        if ok is not True and ok != "not_applicable_preflight_blocked":
            failures.append(f"acceptance_gate_not_true:{gate}:{ok}")
    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_C4_BLOCKED_BY_C3_INTERFACE_VERDICT":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    rollup = read_json(BLOCKED_PREFLIGHT_ROLLUP_PATH)
    report_obj = read_json(REPORT_PATH)
    controls: List[Dict[str, Any]] = []

    def add(case: str, failures: List[str], expected_fragment: str) -> None:
        controls.append({
            "case": case,
            "negative_control_pass": any(expected_fragment in f for f in failures),
            "failures": failures,
            "wrote_live_artifact": False,
        })

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["negative_controls"]["cell1_opened_despite_c3_block_count"] = 1
    add("cell1_opened_despite_c3_block_fail", validate_rollup(bad_rollup), "cell1_opened_despite_c3_block_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["negative_controls"]["schema_only_artifact_counted_as_build_count"] = 1
    add("schema_only_artifact_counted_as_build_fail", validate_rollup(bad_rollup), "schema_only_artifact_counted_as_build_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["negative_controls"]["blocked_preflight_counted_as_failure_count"] = 1
    add("blocked_preflight_counted_as_failure_fail", validate_rollup(bad_rollup), "blocked_preflight_counted_as_failure_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["negative_controls"]["accepted_proposal_fabricated_count"] = 1
    add("accepted_proposal_fabricated_fail", validate_rollup(bad_rollup), "accepted_proposal_fabricated_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["negative_controls"]["proposed_only_packet_consumed_count"] = 1
    add("proposed_only_packet_consumed_fail", validate_rollup(bad_rollup), "proposed_only_packet_consumed_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["negative_controls"]["proposal_accepted_by_cell1_count"] = 1
    add("proposal_accepted_by_cell1_fail", validate_rollup(bad_rollup), "proposal_accepted_by_cell1_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["negative_controls"]["patch_applied_during_preflight_count"] = 1
    add("patch_applied_during_preflight_fail", validate_rollup(bad_rollup), "patch_applied_during_preflight_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["negative_controls"]["probe_run_during_preflight_count"] = 1
    add("probe_run_during_preflight_fail", validate_rollup(bad_rollup), "probe_run_during_preflight_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["negative_controls"]["verification_pass_emitted_during_preflight_count"] = 1
    add("verification_pass_emitted_during_preflight_fail", validate_rollup(bad_rollup), "verification_pass_emitted_during_preflight_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["negative_controls"]["hidden_next_command_count"] = 1
    add("hidden_next_command_fail", validate_rollup(bad_rollup), "hidden_next_command_count")

    bad_report = copy.deepcopy(report_obj)
    bad_report["source_mutation_count"] = 1
    add("source_mutation_fail", validate_report(bad_report), "source_mutation_count")

    bad_report = copy.deepcopy(report_obj)
    bad_report["prior_receipt_mutation_count"] = 1
    add("prior_receipt_mutation_fail", validate_report(bad_report), "prior_receipt_mutation_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["c4_opening_gate_status"] = "OPEN"
    add("c3_block_not_respected_fail", validate_rollup(bad_rollup), "opening_gate_not_blocked")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["builds_attempted"] = 1
    add("build_attempted_during_blocked_preflight_fail", validate_rollup(bad_rollup), "builds_attempted_nonzero")

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_C4_DEPENDENCY_MISSING", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "c4_cell1_receipt_native_builder_preflight_receipt_v0",
            "receipt_type": "C4_CELL1_RECEIPT_NATIVE_BUILDER_PREFLIGHT_RECEIPT",
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
        print(f"c4_receipt_id={receipt_id}")
        print(f"c4_receipt_path=data/c4_cell1_receipt_native_builder_v0_receipts/{receipt_id}.json")
        return 1

    for path, obj in schema_outputs().items():
        write_json(path, obj)

    gate_eval = opening_gate_evaluation()
    rollup = blocked_preflight_rollup(gate_eval)
    prof = profile(rollup)
    trace = transition_trace(gate_eval)
    report_obj = report(gate_eval, rollup, prof)

    write_json(OPENING_GATE_EVALUATION_PATH, gate_eval)
    write_json(BLOCKED_PREFLIGHT_ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, prof)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report_obj)

    failures.extend(validate_rollup(rollup))
    failures.extend(validate_report(report_obj))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup["negative_controls"]["source_mutation_count"] = 1
        report_obj["source_mutation_count"] = 1
        write_json(BLOCKED_PREFLIGHT_ROLLUP_PATH, rollup)
        write_json(REPORT_PATH, report_obj)

    terminal = gate_eval["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    acceptance_gate_results = {
        "C4_PREFLIGHT_0_SOURCE_DESIGN_CONSUMED": True,
        "C4_PREFLIGHT_1_BUILD_MODE_PREFLIGHT_GATE_ONLY": BUILD_MODE == "PREFLIGHT_GATE_ONLY",
        "C4_PREFLIGHT_2_C3_VERDICT_CONSUMED": gate_eval["observed_verdict"] is not None,
        "C4_PREFLIGHT_3_C3_VERDICT_BLOCKS_CELL1": gate_eval["c4_opening_gate_status"] == "BLOCKED",
        "C4_PREFLIGHT_4_CELL1_AUTHORITY_PROFILE_EMITTED": AUTHORITY_PROFILE_PATH.exists(),
        "C4_PREFLIGHT_5_ACCEPTED_PROPOSAL_INPUT_SCHEMA_EMITTED": ACCEPTED_PROPOSAL_INPUT_SCHEMA_PATH.exists(),
        "C4_PREFLIGHT_6_CELL1_BUILDER_LOOP_SCHEMAS_EMITTED": all(p.exists() for p in [
            PATCH_PLAN_SCHEMA_PATH,
            PATCH_RECORD_SCHEMA_PATH,
            PROBE_RECORD_SCHEMA_PATH,
            VERIFICATION_RECORD_SCHEMA_PATH,
            BUILD_RECEIPT_SCHEMA_PATH,
            HANDOFF_RECEIPT_SCHEMA_PATH,
            BUILDER_LOOP_TRACE_SCHEMA_PATH,
        ]),
        "C4_PREFLIGHT_7_NO_ACCEPTED_PROPOSAL_CONSUMED": rollup["accepted_proposals_consumed"] == 0,
        "C4_PREFLIGHT_8_NO_PROPOSED_ONLY_CONSUMED": rollup["negative_controls"]["proposed_only_packet_consumed_count"] == 0,
        "C4_PREFLIGHT_9_NO_PATCH_APPLIED": rollup["negative_controls"]["patch_applied_during_preflight_count"] == 0,
        "C4_PREFLIGHT_10_NO_PROBE_RUN": rollup["negative_controls"]["probe_run_during_preflight_count"] == 0,
        "C4_PREFLIGHT_11_NO_VERIFICATION_PASS_EMITTED": rollup["negative_controls"]["verification_pass_emitted_during_preflight_count"] == 0,
        "C4_PREFLIGHT_12_NO_BUILD_RECEIPT_MARKED_VERIFIED": rollup["builds_verified"] == 0,
        "C4_PREFLIGHT_13_NO_CELL1_EXECUTION_OPENED": rollup["cell1_execution_opened"] is False,
        "C4_PREFLIGHT_14_NO_BUILDER_COMMAND_EMITTED": rollup["negative_controls"]["builder_command_emitted_count"] == 0,
        "C4_PREFLIGHT_15_NO_HIDDEN_NEXT_COMMAND": rollup["negative_controls"]["hidden_next_command_count"] == 0 and terminal["next_command_goal"] is None,
        "C4_PREFLIGHT_16_BLOCKED_ROLLUP_EMITTED": BLOCKED_PREFLIGHT_ROLLUP_PATH.exists(),
        "C4_PREFLIGHT_17_STOP_C4_BLOCKED_BY_C3_INTERFACE_VERDICT": terminal["stop_code"] == "STOP_C4_BLOCKED_BY_C3_INTERFACE_VERDICT",
        "C4_CELL1_11_ONLY_ACCEPTED_PROPOSAL_CONSUMED": "not_applicable_preflight_blocked",
        "C4_CELL1_15_MINIMAL_PATCH_PLAN_EMITTED_BEFORE_PATCH": "not_applicable_preflight_blocked",
        "C4_CELL1_16_PATCH_AUTHORITY_CHECKED": "not_applicable_preflight_blocked",
        "C4_CELL1_17_PATCH_SCOPED_TO_TARGET_SURFACE": "not_applicable_preflight_blocked",
        "C4_CELL1_18_BOUNDED_PROBE_RUN": "not_applicable_preflight_blocked",
        "C4_CELL1_19_VERIFICATION_RECORD_EMITTED": "not_applicable_preflight_blocked",
        "C4_CELL1_20_BUILD_RECEIPT_EMITTED": "not_applicable_preflight_blocked",
        "C4_CELL1_21_HANDOFF_RECEIPT_EMITTED": "not_applicable_preflight_blocked",
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True and ok != "not_applicable_preflight_blocked":
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_c3": SOURCE_C3_RECEIPT_ID,
        "observed_verdict": gate_eval["observed_verdict"],
        "terminal": terminal,
        "build_mode": BUILD_MODE,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "cell1_builder_authority_profile": rel(AUTHORITY_PROFILE_PATH),
        "cell1_accepted_proposal_input_schema": rel(ACCEPTED_PROPOSAL_INPUT_SCHEMA_PATH),
        "cell1_minimal_patch_plan_schema": rel(PATCH_PLAN_SCHEMA_PATH),
        "cell1_patch_record_schema": rel(PATCH_RECORD_SCHEMA_PATH),
        "cell1_probe_record_schema": rel(PROBE_RECORD_SCHEMA_PATH),
        "cell1_verification_record_schema": rel(VERIFICATION_RECORD_SCHEMA_PATH),
        "cell1_build_receipt_schema": rel(BUILD_RECEIPT_SCHEMA_PATH),
        "cell1_handoff_receipt_schema": rel(HANDOFF_RECEIPT_SCHEMA_PATH),
        "cell1_builder_loop_trace_schema": rel(BUILDER_LOOP_TRACE_SCHEMA_PATH),
        "c4_opening_gate_evaluation": rel(OPENING_GATE_EVALUATION_PATH),
        "c4_blocked_preflight_rollup": rel(BLOCKED_PREFLIGHT_ROLLUP_PATH),
        "c4_cell1_builder_profile": rel(PROFILE_PATH),
        "c4_transition_trace": rel(TRANSITION_TRACE_PATH),
        "c4_report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_c3_receipt": rel(SOURCE_C3_RECEIPT_PATH),
        "source_c3_verdict": rel(SOURCE_C3_VERDICT_PATH),
        "source_c1_receipt": rel(SOURCE_C1_RECEIPT_PATH),
        "source_c2_receipt": rel(SOURCE_C2_RECEIPT_PATH),
    }

    aggregate_metrics = {
        **{k: v for k, v in report_obj.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "rollup": rollup,
        "source_mutation_count": 1 if source_mutation_detected else report_obj["source_mutation_count"],
    }

    guards = {
        "build_mode_preflight_gate_only": BUILD_MODE == "PREFLIGHT_GATE_ONLY",
        "c3_verdict_consumed": True,
        "c3_verdict_blocks_cell1": gate_eval["c4_opening_gate_status"] == "BLOCKED",
        "cell1_execution_opened": False,
        "accepted_proposal_consumed": False,
        "proposed_only_packet_consumed": False,
        "patch_applied": False,
        "probe_run": False,
        "verification_pass_emitted": False,
        "build_receipt_marked_verified": False,
        "builder_command_emitted": False,
        "hidden_next_command": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
    }

    receipt = {
        "schema_version": "c4_cell1_receipt_native_builder_preflight_receipt_v0",
        "receipt_type": "C4_CELL1_RECEIPT_NATIVE_BUILDER_PREFLIGHT_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "Cell 1 receipt-native builder opening gate",
        "source_c3_receipt_id": SOURCE_C3_RECEIPT_ID,
        "source_c3_interface_verdict": gate_eval["observed_verdict"],
        "source_c1_receipt_id": SOURCE_C1_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "c4_summary": {
            "profile_status": prof["status"],
            "c3_interface_verdict": gate_eval["observed_verdict"],
            "c4_opening_gate_status": gate_eval["c4_opening_gate_status"],
            "accepted_proposals_consumed": rollup["accepted_proposals_consumed"],
            "builds_attempted": rollup["builds_attempted"],
            "builds_verified": rollup["builds_verified"],
            "builds_blocked": rollup["builds_blocked"],
            "cell1_execution_opened": rollup["cell1_execution_opened"],
            "schemas_emitted": rollup["schemas_emitted"],
            "bad_counters_zero": all(rollup["negative_controls"].get(k) == 0 for k in ZERO_COUNTER_KEYS),
            "recommended_next": None,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "c4_guards": guards,
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
    if len(negative_controls) != 14 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
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
    print(f"c4_receipt_id={receipt_id}")
    print(f"c4_receipt_path=data/c4_cell1_receipt_native_builder_v0_receipts/{receipt_id}.json")
    print(f"c4_profile_path=data/c4_cell1_receipt_native_builder_v0/c4_cell1_builder_profile_v0.json")
    print(f"c4_rollup_path=data/c4_cell1_receipt_native_builder_v0/c4_blocked_preflight_rollup_v0.json")
    print(f"c4_gate_path=data/c4_cell1_receipt_native_builder_v0/c4_opening_gate_evaluation_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
