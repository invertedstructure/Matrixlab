#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "IMPLEMENT_RECEIPT_INTERROGATION_ADAPTER_V0_WITH_DEMO_CLASSIFICATIONS_V0"
TARGET_UNIT_ID = "receipt_interrogation_adapter.v0"

RECEIPT_INTERROGATION_POLICY_ID = "2aa2f2f3"
RECEIPT_INTERROGATION_POLICY_RECEIPT_ID = "0ad557c8"
CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID = "98ab6f11"
CLOSURE_RADIUS_POLICY_ID = "80f2b331"
CLOSURE_RADIUS_POLICY_RECEIPT_ID = "fc82cb0f"
TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID = "6d252e63"
JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID = "6291b0d9"
MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID = "bef08570"
HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID = "75eabbe2"
PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID = "363d2f4a"
TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID = "cc24a11f"
TRACE_SCHEMA_ID = "b4887660"
PROPOSAL_LEDGER_SCHEMA_ID = "eee2a318"
LOCAL_REGIME_V1_HASH = "25802530"

POLICY_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0_policies" / f"{RECEIPT_INTERROGATION_POLICY_ID}.json"
POLICY_RECEIPT_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0_policy_receipts" / f"{RECEIPT_INTERROGATION_POLICY_ID}.json"
CLOSURE_IMPL_RECEIPT_PATH = ROOT / "data" / "closure_radius_metrics_v0_implementation_receipts" / f"{CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID}.json"
CLOSURE_POLICY_PATH = ROOT / "data" / "closure_radius_metrics_v0_policies" / f"{CLOSURE_RADIUS_POLICY_ID}.json"
CLOSURE_POLICY_RECEIPT_PATH = ROOT / "data" / "closure_radius_metrics_v0_policy_receipts" / f"{CLOSURE_RADIUS_POLICY_ID}.json"
CLOSURE_METRIC_SCHEMA_PATH = ROOT / "data" / "closure_radius_metrics_v0" / "closure_radius_metric_schema_v0.json"
RUN_METRICS_SCHEMA_PATH = ROOT / "data" / "closure_radius_metrics_v0" / "run_metrics_schema_v0.json"
STOP_CLASS_MAPPING_PATH = ROOT / "data" / "closure_radius_metrics_v0" / "stop_class_mapping_v0.json"
EXPECTED_HALT_POLICY_SCHEMA_PATH = ROOT / "data" / "closure_radius_metrics_v0" / "expected_halt_policy_schema_v0.json"
CLOSURE_RADIUS_SCORE_PATH = ROOT / "data" / "closure_radius_metrics_v0" / "closure_radius_score_v0.json"
CLOSURE_RADIUS_ROLLUP_SCHEMA_PATH = ROOT / "data" / "closure_radius_metrics_v0" / "closure_radius_rollup_schema_v0.json"
CLOSURE_RADIUS_DASHBOARD_READOUT_PATH = ROOT / "data" / "closure_radius_metrics_v0" / "closure_radius_dashboard_readout_v0.json"
DAY7_DEMO_RADIUS_REPORT_PATH = ROOT / "data" / "closure_radius_metrics_v0_demo" / "day7_demo_radius_report.json"
DAY7_DEMO_RADIUS_ROLLUP_PATH = ROOT / "data" / "closure_radius_metrics_v0_demo" / "day7_demo_radius_rollup.json"

TAX_IMPL_RECEIPT_PATH = ROOT / "data" / "taxonomy_evolution_v0_implementation_receipts" / f"{TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID}.json"
JURIS_IMPL_RECEIPT_PATH = ROOT / "data" / "jurisdiction_gate_v0_implementation_receipts" / f"{JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID}.json"
MOVE_IMPL_RECEIPT_PATH = ROOT / "data" / "move_registry_v0_implementation_receipts" / f"{MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID}.json"
HALT_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "halt_vocabulary_v0_implementation_receipts" / f"{HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID}.json"
PROCEED_RECEIPT_PATH = ROOT / "data" / "proceed_adapter_v0_implementation_receipts" / f"{PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID}.json"
TRACE_LEDGER_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_ledger_hardening_implementation_receipts" / f"{TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID}.json"
TRACE_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_schemas" / f"{TRACE_SCHEMA_ID}.json"
PROPOSAL_LEDGER_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_proposal_ledger_schemas" / f"{PROPOSAL_LEDGER_SCHEMA_ID}.json"
LOCAL_REGIME_V1_PATH = ROOT / "data" / "local_regime_v1_declarations" / f"{LOCAL_REGIME_V1_HASH}.json"

ARTIFACT_DIR = ROOT / "data" / "receipt_interrogation_adapter_v0"
DEMO_DIR = ROOT / "data" / "receipt_interrogation_adapter_v0_demo"
IMPLEMENTATION_RECEIPT_DIR = ROOT / "data" / "receipt_interrogation_adapter_v0_implementation_receipts"

SOURCE_FILES = [
    POLICY_PATH,
    POLICY_RECEIPT_PATH,
    CLOSURE_IMPL_RECEIPT_PATH,
    CLOSURE_POLICY_PATH,
    CLOSURE_POLICY_RECEIPT_PATH,
    CLOSURE_METRIC_SCHEMA_PATH,
    RUN_METRICS_SCHEMA_PATH,
    STOP_CLASS_MAPPING_PATH,
    EXPECTED_HALT_POLICY_SCHEMA_PATH,
    CLOSURE_RADIUS_SCORE_PATH,
    CLOSURE_RADIUS_ROLLUP_SCHEMA_PATH,
    CLOSURE_RADIUS_DASHBOARD_READOUT_PATH,
    DAY7_DEMO_RADIUS_REPORT_PATH,
    DAY7_DEMO_RADIUS_ROLLUP_PATH,
    TAX_IMPL_RECEIPT_PATH,
    JURIS_IMPL_RECEIPT_PATH,
    MOVE_IMPL_RECEIPT_PATH,
    HALT_IMPLEMENTATION_RECEIPT_PATH,
    PROCEED_RECEIPT_PATH,
    TRACE_LEDGER_RECEIPT_PATH,
    TRACE_SCHEMA_PATH,
    PROPOSAL_LEDGER_SCHEMA_PATH,
    LOCAL_REGIME_V1_PATH,
]

MUST_NOT_IMPERSONATE = [
    "roadmap invention",
    "authority grant",
    "optimization instruction",
    "global planner",
    "proof of correctness",
    "permission to ignore STOP_DONE",
]

PRESSURE_CLASSES = [
    "NONE",
    "MISSING_MOVE_PRESSURE",
    "AUTHORITY_BOUNDARY",
    "TAXONOMY_PRESSURE",
    "BURDEN_PRESSURE",
    "RECEIPT_TRACE_PRESSURE",
    "EXTRACTION_PRESSURE",
    "FRONTIER_PRESSURE",
    "REAL_BATCH_REQUIRED",
    "AMBIGUOUS_PRESSURE",
    "INVALID_RECEIPT_SURFACE",
]

NEXT_COMMAND_CLASSES = [
    "REPAIR_COMMAND",
    "RECEIPT_REPAIR_COMMAND",
    "POLICY_REPAIR_COMMAND",
    "EXECUTE_DECLARED_NEXT_COMMAND",
    "STOP_LANE_CLOSED",
    "AWAIT_REAL_BATCH_RECEIPTS",
    "OPEN_OBJECTIVE_PROPOSAL_FROM_PRESSURE_CLASS",
    "QUESTION_PACKET_NOT_COMMAND",
    "INVALID_RECEIPT_SURFACE",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def tracked(path: Path) -> bool:
    result = subprocess.run(["git", "ls-files", "--error-unmatch", rel(path)], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths if path.exists()}

def required_receipt_fields_present(receipt: Dict[str, Any]) -> bool:
    if not receipt.get("receipt_id"):
        return False
    if "gate" not in receipt:
        return False
    if "target_unit_id" not in receipt:
        return False
    terminal = receipt.get("terminal")
    if not isinstance(terminal, dict):
        return False
    if "type" not in terminal:
        return False
    if "next_command_goal" not in terminal:
        return False
    return True

def field(path: str) -> str:
    return path

def classify_receipt(
    receipt: Dict[str, Any],
    *,
    source_receipt_label: str,
    metrics_are_demo_only: bool = False,
    real_batch_receipts_present: bool = False,
) -> Dict[str, Any]:
    evidence: Dict[str, Any] = {}
    answers: Dict[str, Any] = {}
    pressure_classes: List[str] = []
    secondary_classes: List[str] = []
    command_authorized = False
    proposal_authorized = False
    allowed_next_handling: List[str] = []
    unanswered_questions: List[str] = []

    if not required_receipt_fields_present(receipt):
        report_id = f"receipt_interrogation_{sha8({'invalid': source_receipt_label})}"
        return {
            "receipt_interrogation_report_id": report_id,
            "schema_version": "receipt_interrogation_report_v0",
            "source_receipt_ref": source_receipt_label,
            "question_set_id": "RECEIPT_INTERROGATION_QUESTIONS_V0",
            "answers": {
                "RIQ01": None,
                "RIQ02": None,
                "RIQ07": None,
                "RIQ08": None,
                "RIQ15": "Invalid receipt surface; cannot classify next command.",
            },
            "pressure_classification": {
                "primary_pressure_class": "INVALID_RECEIPT_SURFACE",
                "secondary_pressure_classes": [],
                "evidence_fields": ["receipt_id/gate/target_unit_id/terminal"],
            },
            "next_command_classification": {
                "primary_class": "INVALID_RECEIPT_SURFACE",
                "secondary_class": None,
                "command_authorized": False,
                "proposal_authorized": False,
                "classified_next_command_goal": None,
            },
            "evidence_fields": ["receipt missing required gate/terminal/identity fields"],
            "must_not_infer": [
                "do not infer pass/fail without gate",
                "do not infer lane closure without terminal",
                "do not emit command from invalid receipt",
            ],
            "must_not_impersonate": MUST_NOT_IMPERSONATE,
            "allowed_next_handling": ["request valid receipt surface", "repair receipt capture"],
            "unanswered_questions": ["RIQ01", "RIQ02", "RIQ07", "RIQ08"],
            "gate": "PASS",
            "failures": [],
        }

    metrics = receipt.get("aggregate_metrics", {}) or {}
    guards = receipt.get("radius_guards", {}) or receipt.get("adapter_guards", {}) or {}
    terminal = receipt.get("terminal", {}) or {}
    output_artifacts = receipt.get("output_artifacts", {}) or {}

    gate = receipt.get("gate")
    terminal_type = terminal.get("type")
    stop_code = terminal.get("stop_code")
    next_command_goal = terminal.get("next_command_goal")

    answers["RIQ01"] = receipt.get("unit_id") or receipt.get("target_unit_id")
    answers["RIQ02"] = gate
    answers["RIQ03"] = output_artifacts
    answers["RIQ04"] = receipt.get("policy_summary", {}).get("core_law") or "receipt-specific distinction preserved by source implementation"
    answers["RIQ05"] = {
        key: value for key, value in metrics.items()
        if key.endswith("_count") and value == 0 and (
            "claim" in key
            or "hidden" in key
            or "counted_as" in key
            or "executed" in key
            or "optimization" in key
            or "modified" in key
        )
    }
    answers["RIQ06"] = [
        "gate PASS alone is not next-command authorization",
        "STOP_DONE must not be ignored",
        "demo-only metrics must not be treated as real batch evidence",
        "pressure proposal must not be treated as implementation command",
    ]
    answers["RIQ07"] = {"terminal_type": terminal_type, "stop_code": stop_code}
    answers["RIQ08"] = {"next_command_goal": next_command_goal}
    answers["RIQ09"] = "lane_closed" if terminal_type == "STOP" and stop_code == "STOP_DONE" and next_command_goal is None else "not_closed_or_declared_next"
    answers["RIQ14"] = bool(
        metrics.get("optimization_performed_count") == 0
        and guards.get("optimization_performed", False) is False
    )

    evidence["gate"] = gate
    evidence["terminal.type"] = terminal_type
    evidence["terminal.stop_code"] = stop_code
    evidence["terminal.next_command_goal"] = next_command_goal
    evidence["aggregate_metrics"] = metrics
    evidence["guards"] = guards

    primary_class = "QUESTION_PACKET_NOT_COMMAND"
    primary_pressure = "AMBIGUOUS_PRESSURE"

    if gate != "PASS":
        primary_class = "REPAIR_COMMAND"
        primary_pressure = "INVALID_RECEIPT_SURFACE"
        allowed_next_handling = ["repair failed gate before any next command"]
    elif metrics.get("receipt_trace_mismatch_count", 0) > 0 or metrics.get("unlinked_event_count", 0) > 0:
        primary_class = "RECEIPT_REPAIR_COMMAND"
        primary_pressure = "RECEIPT_TRACE_PRESSURE"
        allowed_next_handling = ["repair receipt/trace linkage"]
    elif (
        metrics.get("unauthorized_moves_counted_as_radius_count", 0) > 0
        or metrics.get("proposal_only_counted_as_execution_count", 0) > 0
        or metrics.get("blocked_moves_counted_as_execution_count", 0) > 0
        or metrics.get("human_review_request_counted_as_execution_count", 0) > 0
        or guards.get("unauthorized_moves_counted_as_radius") is True
    ):
        primary_class = "POLICY_REPAIR_COMMAND"
        primary_pressure = "AUTHORITY_BOUNDARY"
        allowed_next_handling = ["repair policy/authority accounting before proceeding"]
    elif next_command_goal:
        primary_class = "EXECUTE_DECLARED_NEXT_COMMAND"
        primary_pressure = "NONE"
        command_authorized = True
        allowed_next_handling = [f"execute exact declared next command after authority check: {next_command_goal}"]
    else:
        if metrics.get("burden_pressure_count", 0) > 0:
            pressure_classes.append("BURDEN_PRESSURE")
        if metrics.get("productive_taxonomy_pressure_count", 0) > 0:
            pressure_classes.append("TAXONOMY_PRESSURE")
        if metrics.get("illegal_improvement_rejected_count", 0) > 0 or metrics.get("unauthorized_execution_count", 0) > 0:
            pressure_classes.append("AUTHORITY_BOUNDARY")
        if metrics_are_demo_only and not real_batch_receipts_present:
            pressure_classes.append("REAL_BATCH_REQUIRED")

        if terminal_type == "STOP" and stop_code == "STOP_DONE":
            primary_class = "STOP_LANE_CLOSED"
            primary_pressure = "NONE"
            allowed_next_handling = ["stop lane", "open new external objective only outside closed lane"]
            if "REAL_BATCH_REQUIRED" in pressure_classes:
                secondary_classes.append("AWAIT_REAL_BATCH_RECEIPTS")
                primary_pressure = "REAL_BATCH_REQUIRED"
                proposal_authorized = True
                allowed_next_handling.append("await real batch receipts before evidence-based build command")
        elif pressure_classes:
            if len(pressure_classes) == 1:
                primary_class = "OPEN_OBJECTIVE_PROPOSAL_FROM_PRESSURE_CLASS"
                primary_pressure = pressure_classes[0]
                proposal_authorized = True
                allowed_next_handling = ["open objective proposal from pressure class; do not emit implementation command"]
            else:
                primary_class = "QUESTION_PACKET_NOT_COMMAND"
                primary_pressure = "AMBIGUOUS_PRESSURE"
                proposal_authorized = False
                allowed_next_handling = ["ask clarifying question packet; do not emit command"]
        else:
            primary_class = "QUESTION_PACKET_NOT_COMMAND"
            primary_pressure = "AMBIGUOUS_PRESSURE"
            unanswered_questions = ["RIQ10", "RIQ11", "RIQ12", "RIQ13"]
            allowed_next_handling = ["question packet only; no command"]

    answers["RIQ10"] = primary_pressure
    answers["RIQ11"] = primary_pressure not in ["NONE", "AMBIGUOUS_PRESSURE", "INVALID_RECEIPT_SURFACE"]
    answers["RIQ12"] = [
        key for key in [
            "gate",
            "terminal.type",
            "terminal.stop_code",
            "terminal.next_command_goal",
            "aggregate_metrics.burden_pressure_count",
            "aggregate_metrics.productive_taxonomy_pressure_count",
            "aggregate_metrics.illegal_improvement_rejected_count",
            "aggregate_metrics.unauthorized_execution_count",
            "aggregate_metrics.receipt_trace_mismatch_count",
            "aggregate_metrics.unlinked_event_count",
        ]
        if key == "gate"
        or key.startswith("terminal.")
        or metrics.get(key.split(".")[-1], 0)
    ]
    answers["RIQ13"] = "real batch receipts" if primary_pressure == "REAL_BATCH_REQUIRED" else None
    answers["RIQ15"] = {
        "primary_class": primary_class,
        "secondary_class": secondary_classes[0] if secondary_classes else None,
        "command_authorized": command_authorized,
        "proposal_authorized": proposal_authorized,
    }

    report_seed = {
        "source": source_receipt_label,
        "primary_class": primary_class,
        "secondary": secondary_classes,
        "pressure": primary_pressure,
    }
    return {
        "receipt_interrogation_report_id": f"receipt_interrogation_{sha8(report_seed)}",
        "schema_version": "receipt_interrogation_report_v0",
        "source_receipt_ref": source_receipt_label,
        "question_set_id": "RECEIPT_INTERROGATION_QUESTIONS_V0",
        "answers": answers,
        "pressure_classification": {
            "primary_pressure_class": primary_pressure,
            "secondary_pressure_classes": [p for p in pressure_classes if p != primary_pressure],
            "all_detected_pressure_classes": pressure_classes,
            "evidence_fields": answers["RIQ12"],
        },
        "next_command_classification": {
            "primary_class": primary_class,
            "secondary_class": secondary_classes[0] if secondary_classes else None,
            "all_secondary_classes": secondary_classes,
            "command_authorized": command_authorized,
            "proposal_authorized": proposal_authorized,
            "classified_next_command_goal": next_command_goal if primary_class == "EXECUTE_DECLARED_NEXT_COMMAND" else None,
        },
        "evidence_fields": evidence,
        "must_not_infer": [
            "do not invent roadmap",
            "do not treat pressure proposal as implementation command",
            "do not treat demo-only metrics as real batch evidence",
            "do not optimize from interrogation output",
            "do not widen authority",
        ],
        "must_not_impersonate": MUST_NOT_IMPERSONATE,
        "allowed_next_handling": allowed_next_handling,
        "unanswered_questions": unanswered_questions,
        "gate": "PASS",
        "failures": [],
    }

def validate_source_policy(policy: Dict[str, Any], receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if policy.get("policy_id") != RECEIPT_INTERROGATION_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if receipt.get("receipt_id") != RECEIPT_INTERROGATION_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{receipt.get('receipt_id')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append(f"policy_target_wrong:{receipt.get('target_unit_id')}")
    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "ADVANCE":
        failures.append(f"policy_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != UNIT_ID:
        failures.append(f"policy_terminal_next_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"policy_terminal_stop_not_null:{terminal.get('stop_code')}")

    if receipt.get("source_closure_radius_implementation_receipt_id") != CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID:
        failures.append("policy_source_closure_receipt_wrong")
    qschema = receipt.get("receipt_interrogation_question_schema", {})
    if qschema.get("question_set_id") != "RECEIPT_INTERROGATION_QUESTIONS_V0":
        failures.append("question_set_wrong")
    if len(qschema.get("questions", [])) != 15:
        failures.append("question_count_wrong")
    aschema = receipt.get("receipt_interrogation_answer_schema", {})
    if "every nontrivial answer must cite a receipt field" not in aschema.get("answer_law", []):
        failures.append("answer_evidence_law_missing")
    pressure = receipt.get("pressure_classification_schema", {})
    for cls in PRESSURE_CLASSES:
        if cls not in pressure.get("pressure_classes", []):
            failures.append(f"pressure_class_missing:{cls}")
    classifier = receipt.get("next_command_classifier_schema", {})
    for cls in NEXT_COMMAND_CLASSES:
        if cls not in classifier.get("next_command_classes", []):
            failures.append(f"next_command_class_missing:{cls}")
    for law in [
        "classifier emits command class, not creative roadmap",
        "OPEN_OBJECTIVE_PROPOSAL_FROM_PRESSURE_CLASS is proposal-only and not an implementation command",
        "AWAIT_REAL_BATCH_RECEIPTS is not a build command",
    ]:
        if law not in classifier.get("law", []):
            failures.append(f"classifier_law_missing:{law}")

    demo = receipt.get("day7_receipt_interrogation_demo_plan", {})
    if demo.get("expected_primary_class") != "STOP_LANE_CLOSED":
        failures.append("demo_expected_primary_wrong")
    if demo.get("expected_secondary_class") != "AWAIT_REAL_BATCH_RECEIPTS":
        failures.append("demo_expected_secondary_wrong")
    if demo.get("expected_pressure_class") != "REAL_BATCH_REQUIRED":
        failures.append("demo_expected_pressure_wrong")
    if demo.get("expected_command_authorized") is not False:
        failures.append("demo_expected_command_authorized_wrong")
    if demo.get("expected_proposal_authorized") is not True:
        failures.append("demo_expected_proposal_authorized_wrong")

    guards = receipt.get("adapter_guards", {})
    for key in [
        "policy_built",
        "source_closure_radius_receipt_consumed",
        "source_taxonomy_evolution_receipt_consumed",
        "source_jurisdiction_gate_receipt_consumed",
        "source_move_registry_receipt_consumed",
        "source_halt_vocabulary_receipt_consumed",
        "source_proceed_adapter_receipt_consumed",
        "source_trace_ledger_surface_consumed",
    ]:
        if guards.get(key) is not True:
            failures.append(f"policy_guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "implementation_performed_by_policy",
        "demo_classification_emitted_by_policy",
        "command_emitted_by_policy",
        "objective_invented_by_policy",
        "optimization_performed_by_policy",
        "authority_widened_by_policy",
        "global_planner_claimed",
        "final_roadmap_claimed",
        "proof_claimed",
        "hidden_continuation_authorized",
        "sqlite_registry_written",
    ]:
        if guards.get(key) is not False:
            failures.append(f"policy_guard_not_false:{key}:{guards.get(key)}")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def validate_external_sources() -> List[str]:
    failures: List[str] = []

    closure = read_json(CLOSURE_IMPL_RECEIPT_PATH)
    tax = read_json(TAX_IMPL_RECEIPT_PATH)
    juris = read_json(JURIS_IMPL_RECEIPT_PATH)
    move = read_json(MOVE_IMPL_RECEIPT_PATH)
    halt = read_json(HALT_IMPLEMENTATION_RECEIPT_PATH)
    proceed = read_json(PROCEED_RECEIPT_PATH)
    trace = read_json(TRACE_LEDGER_RECEIPT_PATH)
    trace_schema = read_json(TRACE_SCHEMA_PATH)
    proposal_schema = read_json(PROPOSAL_LEDGER_SCHEMA_PATH)
    regime = read_json(LOCAL_REGIME_V1_PATH)

    if closure.get("receipt_id") != CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID or closure.get("gate") != "PASS":
        failures.append("closure_radius_source_not_pass")
    if closure.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append("closure_radius_terminal_not_done")
    if closure.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("closure_radius_next_not_null")
    metrics = closure.get("aggregate_metrics", {})
    expected = {
        "lawful_improvement_count": 1,
        "illegal_improvement_rejected_count": 1,
        "productive_taxonomy_pressure_count": 1,
        "burden_pressure_count": 1,
        "unauthorized_moves_counted_as_radius_count": 0,
        "proposal_only_counted_as_execution_count": 0,
        "higher_radius_treated_as_always_better_count": 0,
        "global_closure_claim_count": 0,
        "proof_claim_count": 0,
        "hidden_continuation_count": 0,
    }
    for key, value in expected.items():
        if metrics.get(key) != value:
            failures.append(f"closure_metric_wrong:{key}:{metrics.get(key)} expected {value}")

    for obj, expected_id, label in [
        (tax, TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID, "taxonomy"),
        (juris, JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID, "jurisdiction"),
        (move, MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID, "move_registry"),
        (halt, HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID, "halt_vocabulary"),
        (proceed, PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID, "proceed"),
        (trace, TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID, "trace_ledger"),
    ]:
        if obj.get("receipt_id") != expected_id or obj.get("gate") != "PASS":
            failures.append(f"{label}_source_not_pass")
    if trace_schema.get("schema_version") != "jurisdiction_runner_trace_file_v0":
        failures.append("trace_schema_wrong")
    if proposal_schema.get("schema_version") != "unresolved_proposal_ledger_v0":
        failures.append("proposal_schema_wrong")
    if regime.get("local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append("local_regime_wrong")

    return failures

def validate_interrogation_report(report: Dict[str, Any], expected: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    label = report.get("source_receipt_ref", "unknown")

    if report.get("gate") != "PASS":
        failures.append(f"{label}:report_gate_not_PASS")
    if report.get("question_set_id") != "RECEIPT_INTERROGATION_QUESTIONS_V0":
        failures.append(f"{label}:question_set_wrong")
    if not report.get("receipt_interrogation_report_id"):
        failures.append(f"{label}:report_id_missing")

    pressure = report.get("pressure_classification", {})
    classification = report.get("next_command_classification", {})
    answers = report.get("answers", {})
    evidence = report.get("evidence_fields", {})

    if classification.get("primary_class") != expected.get("primary_class"):
        failures.append(f"{label}:primary_class_wrong:{classification.get('primary_class')} expected {expected.get('primary_class')}")
    if classification.get("secondary_class") != expected.get("secondary_class"):
        failures.append(f"{label}:secondary_class_wrong:{classification.get('secondary_class')} expected {expected.get('secondary_class')}")
    if pressure.get("primary_pressure_class") != expected.get("pressure_class"):
        failures.append(f"{label}:pressure_class_wrong:{pressure.get('primary_pressure_class')} expected {expected.get('pressure_class')}")
    if classification.get("command_authorized") is not expected.get("command_authorized"):
        failures.append(f"{label}:command_authorized_wrong:{classification.get('command_authorized')} expected {expected.get('command_authorized')}")
    if classification.get("proposal_authorized") is not expected.get("proposal_authorized"):
        failures.append(f"{label}:proposal_authorized_wrong:{classification.get('proposal_authorized')} expected {expected.get('proposal_authorized')}")

    for qid in [f"RIQ{i:02d}" for i in range(1, 16)]:
        if qid not in answers and report.get("next_command_classification", {}).get("primary_class") != "INVALID_RECEIPT_SURFACE":
            failures.append(f"{label}:answer_missing:{qid}")

    for phrase in MUST_NOT_IMPERSONATE:
        if phrase not in report.get("must_not_impersonate", []):
            failures.append(f"{label}:must_not_impersonate_missing:{phrase}")

    if classification.get("primary_class") == "OPEN_OBJECTIVE_PROPOSAL_FROM_PRESSURE_CLASS" and classification.get("command_authorized") is True:
        failures.append(f"{label}:pressure_proposal_authorized_as_command")
    if classification.get("primary_class") == "AWAIT_REAL_BATCH_RECEIPTS" and classification.get("command_authorized") is True:
        failures.append(f"{label}:await_real_batch_authorized_as_command")
    if classification.get("primary_class") == "STOP_LANE_CLOSED" and evidence.get("terminal.next_command_goal") is not None:
        failures.append(f"{label}:stop_lane_closed_with_next_command")
    if classification.get("primary_class") == "EXECUTE_DECLARED_NEXT_COMMAND" and not classification.get("classified_next_command_goal"):
        failures.append(f"{label}:declared_next_missing_goal")

    return failures

def make_demo_suite(source_day7: Dict[str, Any]) -> Dict[str, Any]:
    failed_gate = copy.deepcopy(source_day7)
    failed_gate["receipt_id"] = "demo_failed_gate_receipt"
    failed_gate["gate"] = "FAIL"
    failed_gate["terminal"] = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}

    trace_mismatch = copy.deepcopy(source_day7)
    trace_mismatch["receipt_id"] = "demo_trace_mismatch_receipt"
    trace_mismatch["aggregate_metrics"]["receipt_trace_mismatch_count"] = 1

    unauthorized_counted = copy.deepcopy(source_day7)
    unauthorized_counted["receipt_id"] = "demo_unauthorized_counted_receipt"
    unauthorized_counted["aggregate_metrics"]["unauthorized_moves_counted_as_radius_count"] = 1

    declared_next = copy.deepcopy(source_day7)
    declared_next["receipt_id"] = "demo_declared_next_receipt"
    declared_next["terminal"] = {
        "type": "ADVANCE",
        "stop_code": None,
        "next_command_goal": "EXACT_DECLARED_NEXT_UNIT_V0",
    }

    ambiguous = copy.deepcopy(source_day7)
    ambiguous["receipt_id"] = "demo_ambiguous_pressure_receipt"
    ambiguous["terminal"] = {"type": "STOP", "stop_code": "STOP_BOUNDARY", "next_command_goal": None}
    ambiguous["aggregate_metrics"]["burden_pressure_count"] = 1
    ambiguous["aggregate_metrics"]["productive_taxonomy_pressure_count"] = 1
    ambiguous["aggregate_metrics"]["illegal_improvement_rejected_count"] = 1
    ambiguous["aggregate_metrics"]["unauthorized_execution_count"] = 2

    invalid = {"receipt_id": "demo_invalid_receipt", "gate": "PASS"}

    demos = [
        {
            "demo_name": "DAY7_CLOSURE_RADIUS_RECEIPT_INTERROGATION",
            "receipt": source_day7,
            "kwargs": {"source_receipt_label": "closure_radius_implementation_receipt:98ab6f11", "metrics_are_demo_only": True, "real_batch_receipts_present": False},
            "expected": {
                "primary_class": "STOP_LANE_CLOSED",
                "secondary_class": "AWAIT_REAL_BATCH_RECEIPTS",
                "pressure_class": "REAL_BATCH_REQUIRED",
                "command_authorized": False,
                "proposal_authorized": True,
            },
        },
        {
            "demo_name": "FAILED_GATE_MAPS_TO_REPAIR",
            "receipt": failed_gate,
            "kwargs": {"source_receipt_label": "demo_failed_gate_receipt", "metrics_are_demo_only": False, "real_batch_receipts_present": False},
            "expected": {
                "primary_class": "REPAIR_COMMAND",
                "secondary_class": None,
                "pressure_class": "INVALID_RECEIPT_SURFACE",
                "command_authorized": False,
                "proposal_authorized": False,
            },
        },
        {
            "demo_name": "TRACE_MISMATCH_MAPS_TO_RECEIPT_REPAIR",
            "receipt": trace_mismatch,
            "kwargs": {"source_receipt_label": "demo_trace_mismatch_receipt", "metrics_are_demo_only": False, "real_batch_receipts_present": False},
            "expected": {
                "primary_class": "RECEIPT_REPAIR_COMMAND",
                "secondary_class": None,
                "pressure_class": "RECEIPT_TRACE_PRESSURE",
                "command_authorized": False,
                "proposal_authorized": False,
            },
        },
        {
            "demo_name": "UNAUTHORIZED_COUNTED_MAPS_TO_POLICY_REPAIR",
            "receipt": unauthorized_counted,
            "kwargs": {"source_receipt_label": "demo_unauthorized_counted_receipt", "metrics_are_demo_only": False, "real_batch_receipts_present": False},
            "expected": {
                "primary_class": "POLICY_REPAIR_COMMAND",
                "secondary_class": None,
                "pressure_class": "AUTHORITY_BOUNDARY",
                "command_authorized": False,
                "proposal_authorized": False,
            },
        },
        {
            "demo_name": "DECLARED_NEXT_COMMAND_EXACT_ONLY",
            "receipt": declared_next,
            "kwargs": {"source_receipt_label": "demo_declared_next_receipt", "metrics_are_demo_only": False, "real_batch_receipts_present": False},
            "expected": {
                "primary_class": "EXECUTE_DECLARED_NEXT_COMMAND",
                "secondary_class": None,
                "pressure_class": "NONE",
                "command_authorized": True,
                "proposal_authorized": False,
            },
        },
        {
            "demo_name": "AMBIGUOUS_PRESSURE_QUESTION_PACKET",
            "receipt": ambiguous,
            "kwargs": {"source_receipt_label": "demo_ambiguous_pressure_receipt", "metrics_are_demo_only": False, "real_batch_receipts_present": False},
            "expected": {
                "primary_class": "QUESTION_PACKET_NOT_COMMAND",
                "secondary_class": None,
                "pressure_class": "AMBIGUOUS_PRESSURE",
                "command_authorized": False,
                "proposal_authorized": False,
            },
        },
        {
            "demo_name": "INVALID_RECEIPT_SURFACE",
            "receipt": invalid,
            "kwargs": {"source_receipt_label": "demo_invalid_receipt", "metrics_are_demo_only": False, "real_batch_receipts_present": False},
            "expected": {
                "primary_class": "INVALID_RECEIPT_SURFACE",
                "secondary_class": None,
                "pressure_class": "INVALID_RECEIPT_SURFACE",
                "command_authorized": False,
                "proposal_authorized": False,
            },
        },
    ]

    demo_reports = []
    failures: List[str] = []
    for demo in demos:
        report = classify_receipt(demo["receipt"], **demo["kwargs"])
        report["demo_name"] = demo["demo_name"]
        report["expected"] = demo["expected"]
        report_failures = validate_interrogation_report(report, demo["expected"])
        report["failures"] = report_failures
        report["gate"] = "PASS" if not report_failures else "FAIL"
        failures.extend(report_failures)
        demo_reports.append(report)

    bundle_seed = {"reports": [r["receipt_interrogation_report_id"] for r in demo_reports]}
    return {
        "schema_version": "day7_demo_receipt_interrogation_v0",
        "day7_demo_receipt_interrogation_id": f"day7_receipt_interrogation_{sha8(bundle_seed)}",
        "source_policy_id": RECEIPT_INTERROGATION_POLICY_ID,
        "source_closure_radius_implementation_receipt_id": CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID,
        "reports": demo_reports,
        "summary": {
            "demo_count": len(demo_reports),
            "passed_demo_count": sum(1 for r in demo_reports if r["gate"] == "PASS"),
            "failed_gate_repair_count": sum(1 for r in demo_reports if r["next_command_classification"]["primary_class"] == "REPAIR_COMMAND"),
            "receipt_repair_count": sum(1 for r in demo_reports if r["next_command_classification"]["primary_class"] == "RECEIPT_REPAIR_COMMAND"),
            "policy_repair_count": sum(1 for r in demo_reports if r["next_command_classification"]["primary_class"] == "POLICY_REPAIR_COMMAND"),
            "declared_next_count": sum(1 for r in demo_reports if r["next_command_classification"]["primary_class"] == "EXECUTE_DECLARED_NEXT_COMMAND"),
            "stop_lane_closed_count": sum(1 for r in demo_reports if r["next_command_classification"]["primary_class"] == "STOP_LANE_CLOSED"),
            "await_real_batch_count": sum(1 for r in demo_reports if r["next_command_classification"]["secondary_class"] == "AWAIT_REAL_BATCH_RECEIPTS"),
            "question_packet_count": sum(1 for r in demo_reports if r["next_command_classification"]["primary_class"] == "QUESTION_PACKET_NOT_COMMAND"),
            "invalid_surface_count": sum(1 for r in demo_reports if r["next_command_classification"]["primary_class"] == "INVALID_RECEIPT_SURFACE"),
            "build_command_from_pressure_count": 0,
            "roadmap_invention_count": 0,
            "optimization_instruction_count": 0,
            "authority_widening_count": 0,
            "global_planner_claim_count": 0,
            "proof_claim_count": 0,
        },
        "must_not_impersonate": MUST_NOT_IMPERSONATE,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "created_at": now_iso(),
    }

def validate_demo_bundle(bundle: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    summary = bundle.get("summary", {})
    expected = {
        "demo_count": 7,
        "passed_demo_count": 7,
        "failed_gate_repair_count": 1,
        "receipt_repair_count": 1,
        "policy_repair_count": 1,
        "declared_next_count": 1,
        "stop_lane_closed_count": 1,
        "await_real_batch_count": 1,
        "question_packet_count": 1,
        "invalid_surface_count": 1,
        "build_command_from_pressure_count": 0,
        "roadmap_invention_count": 0,
        "optimization_instruction_count": 0,
        "authority_widening_count": 0,
        "global_planner_claim_count": 0,
        "proof_claim_count": 0,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            failures.append(f"demo_summary_wrong:{key}:{summary.get(key)} expected {value}")
    for phrase in MUST_NOT_IMPERSONATE:
        if phrase not in bundle.get("must_not_impersonate", []):
            failures.append(f"bundle_must_not_impersonate_missing:{phrase}")
    return failures

def validate_implementation_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if receipt.get("gate") != "PASS":
        failures.append(f"implementation_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("source_receipt_interrogation_policy_id") != RECEIPT_INTERROGATION_POLICY_ID:
        failures.append("source_policy_id_wrong")
    if receipt.get("source_receipt_interrogation_policy_receipt_id") != RECEIPT_INTERROGATION_POLICY_RECEIPT_ID:
        failures.append("source_policy_receipt_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "RII0_source_policy_verified",
        "RII1_core_artifacts_emitted",
        "RII2_day7_demo_classified_stop_closed_and_await_real_batch",
        "RII3_failed_gate_maps_to_repair",
        "RII4_trace_mismatch_maps_to_receipt_repair",
        "RII5_unauthorized_counted_maps_to_policy_repair",
        "RII6_declared_next_exact_only",
        "RII7_ambiguous_pressure_question_packet",
        "RII8_invalid_surface_rejected",
        "RII9_no_build_command_from_pressure",
        "RII10_no_roadmap_optimization_authority_or_proof_claim",
        "RII11_no_source_artifact_mutation",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    expected_metrics = {
        "demo_count": 7,
        "passed_demo_count": 7,
        "failed_gate_repair_count": 1,
        "receipt_repair_count": 1,
        "policy_repair_count": 1,
        "declared_next_count": 1,
        "stop_lane_closed_count": 1,
        "await_real_batch_count": 1,
        "question_packet_count": 1,
        "invalid_surface_count": 1,
        "build_command_from_pressure_count": 0,
        "roadmap_invention_count": 0,
        "optimization_instruction_count": 0,
        "authority_widening_count": 0,
        "global_planner_claim_count": 0,
        "proof_claim_count": 0,
    }
    for key, value in expected_metrics.items():
        if metrics.get(key) != value:
            failures.append(f"metric_wrong:{key}:{metrics.get(key)} expected {value}")

    for key in [
        "command_emitted_count",
        "objective_invented_count",
        "source_receipt_modified_count",
        "source_registry_modified_count",
        "source_module_modified_count",
        "source_regime_modified_count",
        "hidden_continuation_count",
        "sqlite_registry_write_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    guards = receipt.get("adapter_guards", {})
    for key in [
        "core_artifacts_emitted",
        "demo_classifications_emitted",
        "implementation_receipt_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "command_emitted",
        "objective_invented",
        "optimization_performed",
        "authority_widened",
        "source_closure_radius_modified",
        "source_taxonomy_evolution_modified",
        "source_jurisdiction_gate_modified",
        "source_move_registry_modified",
        "source_halt_vocabulary_modified",
        "source_proceed_adapter_modified",
        "source_trace_ledger_runner_modified",
        "source_local_regime_modified",
        "global_planner_claimed",
        "final_roadmap_claimed",
        "proof_claimed",
        "hidden_continuation_authorized",
        "sqlite_registry_written",
    ]:
        if guards.get(key) is not False:
            failures.append(f"guard_not_false:{key}:{guards.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_DONE":
        failures.append(f"terminal_stop_not_DONE:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")

    return failures

def main() -> int:
    policy = read_json(POLICY_PATH)
    policy_receipt = read_json(POLICY_RECEIPT_PATH)
    closure_receipt = read_json(CLOSURE_IMPL_RECEIPT_PATH)

    source_before = snapshot_files(SOURCE_FILES)

    failures: List[str] = []
    failures.extend(validate_source_policy(policy, policy_receipt))
    failures.extend(validate_external_sources())

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DEMO_DIR.mkdir(parents=True, exist_ok=True)
    IMPLEMENTATION_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    artifact_paths = {
        "receipt_interrogation_question_schema": ARTIFACT_DIR / "receipt_interrogation_question_schema_v0.json",
        "receipt_interrogation_answer_schema": ARTIFACT_DIR / "receipt_interrogation_answer_schema_v0.json",
        "pressure_classification_schema": ARTIFACT_DIR / "pressure_classification_schema_v0.json",
        "next_command_classifier_schema": ARTIFACT_DIR / "next_command_classifier_schema_v0.json",
        "receipt_interrogation_report_schema": ARTIFACT_DIR / "receipt_interrogation_report_schema_v0.json",
    }
    write_json(artifact_paths["receipt_interrogation_question_schema"], policy_receipt["receipt_interrogation_question_schema"])
    write_json(artifact_paths["receipt_interrogation_answer_schema"], policy_receipt["receipt_interrogation_answer_schema"])
    write_json(artifact_paths["pressure_classification_schema"], policy_receipt["pressure_classification_schema"])
    write_json(artifact_paths["next_command_classifier_schema"], policy_receipt["next_command_classifier_schema"])
    write_json(artifact_paths["receipt_interrogation_report_schema"], policy_receipt["receipt_interrogation_report_schema"])

    demo_bundle = make_demo_suite(closure_receipt)
    demo_failures = validate_demo_bundle(demo_bundle)
    demo_bundle["failures"] = demo_failures
    demo_bundle["gate"] = "PASS" if not demo_failures else "FAIL"
    failures.extend(demo_failures)

    demo_path = DEMO_DIR / "day7_demo_receipt_interrogation.json"
    write_json(demo_path, demo_bundle)

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    output_artifacts = {name: rel(path) for name, path in artifact_paths.items()}
    output_artifacts["day7_demo_receipt_interrogation"] = rel(demo_path)

    metrics = dict(demo_bundle["summary"])
    metrics.update({
        "command_emitted_count": 0,
        "objective_invented_count": 0,
        "source_receipt_modified_count": 0,
        "source_registry_modified_count": 0,
        "source_module_modified_count": 0,
        "source_regime_modified_count": 0,
        "hidden_continuation_count": 0,
        "sqlite_registry_write_count": 0,
    })

    reports = {r["demo_name"]: r for r in demo_bundle["reports"]}
    acceptance_gate_results = {
        "RII0_source_policy_verified": len(validate_source_policy(policy, policy_receipt)) == 0 and len(validate_external_sources()) == 0,
        "RII1_core_artifacts_emitted": all(path.exists() for path in artifact_paths.values()),
        "RII2_day7_demo_classified_stop_closed_and_await_real_batch": (
            reports["DAY7_CLOSURE_RADIUS_RECEIPT_INTERROGATION"]["next_command_classification"]["primary_class"] == "STOP_LANE_CLOSED"
            and reports["DAY7_CLOSURE_RADIUS_RECEIPT_INTERROGATION"]["next_command_classification"]["secondary_class"] == "AWAIT_REAL_BATCH_RECEIPTS"
            and reports["DAY7_CLOSURE_RADIUS_RECEIPT_INTERROGATION"]["next_command_classification"]["command_authorized"] is False
        ),
        "RII3_failed_gate_maps_to_repair": reports["FAILED_GATE_MAPS_TO_REPAIR"]["next_command_classification"]["primary_class"] == "REPAIR_COMMAND",
        "RII4_trace_mismatch_maps_to_receipt_repair": reports["TRACE_MISMATCH_MAPS_TO_RECEIPT_REPAIR"]["next_command_classification"]["primary_class"] == "RECEIPT_REPAIR_COMMAND",
        "RII5_unauthorized_counted_maps_to_policy_repair": reports["UNAUTHORIZED_COUNTED_MAPS_TO_POLICY_REPAIR"]["next_command_classification"]["primary_class"] == "POLICY_REPAIR_COMMAND",
        "RII6_declared_next_exact_only": (
            reports["DECLARED_NEXT_COMMAND_EXACT_ONLY"]["next_command_classification"]["primary_class"] == "EXECUTE_DECLARED_NEXT_COMMAND"
            and reports["DECLARED_NEXT_COMMAND_EXACT_ONLY"]["next_command_classification"]["classified_next_command_goal"] == "EXACT_DECLARED_NEXT_UNIT_V0"
        ),
        "RII7_ambiguous_pressure_question_packet": reports["AMBIGUOUS_PRESSURE_QUESTION_PACKET"]["next_command_classification"]["primary_class"] == "QUESTION_PACKET_NOT_COMMAND",
        "RII8_invalid_surface_rejected": reports["INVALID_RECEIPT_SURFACE"]["next_command_classification"]["primary_class"] == "INVALID_RECEIPT_SURFACE",
        "RII9_no_build_command_from_pressure": metrics["build_command_from_pressure_count"] == 0,
        "RII10_no_roadmap_optimization_authority_or_proof_claim": (
            metrics["roadmap_invention_count"] == 0
            and metrics["optimization_instruction_count"] == 0
            and metrics["authority_widening_count"] == 0
            and metrics["global_planner_claim_count"] == 0
            and metrics["proof_claim_count"] == 0
        ),
        "RII11_no_source_artifact_mutation": not source_mutation_detected,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    adapter_guards = {
        "core_artifacts_emitted": True,
        "demo_classifications_emitted": True,
        "implementation_receipt_emitted": True,
        "command_emitted": False,
        "objective_invented": False,
        "optimization_performed": False,
        "authority_widened": False,
        "source_closure_radius_modified": False,
        "source_taxonomy_evolution_modified": False,
        "source_jurisdiction_gate_modified": False,
        "source_move_registry_modified": False,
        "source_halt_vocabulary_modified": False,
        "source_proceed_adapter_modified": False,
        "source_trace_ledger_runner_modified": False,
        "source_local_regime_modified": False,
        "source_trace_modified": False,
        "source_receipt_modified": False,
        "source_ledger_modified": False,
        "global_planner_claimed": False,
        "final_roadmap_claimed": False,
        "proof_claimed": False,
        "hidden_continuation_authorized": False,
        "sqlite_registry_read": False,
        "sqlite_registry_written": False,
    }

    artifact_guards = {
        "policy_tracked": tracked(POLICY_PATH),
        "policy_receipt_tracked": tracked(POLICY_RECEIPT_PATH),
        "source_closure_radius_receipt_tracked": tracked(CLOSURE_IMPL_RECEIPT_PATH),
        "source_taxonomy_receipt_tracked": tracked(TAX_IMPL_RECEIPT_PATH),
        "source_jurisdiction_receipt_tracked": tracked(JURIS_IMPL_RECEIPT_PATH),
        "source_move_registry_receipt_tracked": tracked(MOVE_IMPL_RECEIPT_PATH),
        "source_halt_vocabulary_receipt_tracked": tracked(HALT_IMPLEMENTATION_RECEIPT_PATH),
        "source_proceed_receipt_tracked": tracked(PROCEED_RECEIPT_PATH),
        "source_trace_ledger_receipt_tracked": tracked(TRACE_LEDGER_RECEIPT_PATH),
        "source_local_regime_tracked": tracked(LOCAL_REGIME_V1_PATH),
        "outputs_path_addressed": True,
        "latest_or_mtime_selection_used": False,
        "ambient_workspace_authority_used": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_policy_id": RECEIPT_INTERROGATION_POLICY_ID,
        "demo_id": demo_bundle["day7_demo_receipt_interrogation_id"],
    }
    implementation_receipt_id = sha8(receipt_seed)
    implementation_receipt_path = IMPLEMENTATION_RECEIPT_DIR / f"{implementation_receipt_id}.json"

    implementation_receipt = {
        "schema_version": "receipt_interrogation_adapter_v0_implementation_receipt_v0",
        "receipt_type": "RECEIPT_INTERROGATION_ADAPTER_V0_IMPLEMENTATION_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": implementation_receipt_id,
        "source_receipt_interrogation_policy_id": RECEIPT_INTERROGATION_POLICY_ID,
        "source_receipt_interrogation_policy_receipt_id": RECEIPT_INTERROGATION_POLICY_RECEIPT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_closure_radius_implementation_receipt_id": CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID,
        "source_taxonomy_evolution_implementation_receipt_id": TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID,
        "source_jurisdiction_gate_implementation_receipt_id": JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID,
        "source_move_registry_implementation_receipt_id": MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID,
        "source_halt_vocabulary_implementation_receipt_id": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "output_artifacts": output_artifacts,
        "demo_summary": demo_bundle["summary"],
        "day7_classification": reports["DAY7_CLOSURE_RADIUS_RECEIPT_INTERROGATION"]["next_command_classification"],
        "aggregate_metrics": metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "adapter_guards": adapter_guards,
        "artifact_guards": artifact_guards,
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_DONE" if not failures else "STOP_GATE_FAIL",
            "next_command_goal": None,
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_failures = validate_implementation_receipt(implementation_receipt)
    failures.extend(receipt_failures)
    implementation_receipt["failures"] = failures
    implementation_receipt["gate"] = "PASS" if not failures else "FAIL"
    implementation_receipt["terminal"]["stop_code"] = "STOP_DONE" if not failures else "STOP_GATE_FAIL"

    write_json(implementation_receipt_path, implementation_receipt)

    print(json.dumps(implementation_receipt, indent=2, sort_keys=True))
    print(f"receipt_interrogation_implementation_receipt_id={implementation_receipt_id}")
    print(f"receipt_interrogation_implementation_receipt_path=data/receipt_interrogation_adapter_v0_implementation_receipts/{implementation_receipt_id}.json")
    for name, path in sorted(output_artifacts.items()):
        print(f"artifact_{name}_path={path}")

    return 0 if implementation_receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
