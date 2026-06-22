#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_RECEIPT_INTERROGATION_ADAPTER_V0_POLICY_V0"
NEXT_GOAL = "IMPLEMENT_RECEIPT_INTERROGATION_ADAPTER_V0_WITH_DEMO_CLASSIFICATIONS_V0"
TARGET_UNIT_ID = "receipt_interrogation_adapter.v0"

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

OUT_DIR = ROOT / "data" / "receipt_interrogation_adapter_v0_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "receipt_interrogation_adapter_v0_policy_receipts"

SOURCE_FILES = [
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

QUESTION_SET = [
    {"id": "RIQ01", "question": "What unit/lane did this receipt close?", "section": "identity"},
    {"id": "RIQ02", "question": "Did the declared gate pass?", "section": "identity"},
    {"id": "RIQ03", "question": "What artifact IDs/paths were produced or accepted?", "section": "identity"},
    {"id": "RIQ04", "question": "What distinction did this receipt preserve?", "section": "boundary"},
    {"id": "RIQ05", "question": "What negative controls passed?", "section": "boundary"},
    {"id": "RIQ06", "question": "What must not be counted as success?", "section": "boundary"},
    {"id": "RIQ07", "question": "Did the receipt emit STOP_DONE, ADVANCE, or another STOP code?", "section": "terminal"},
    {"id": "RIQ08", "question": "Is next_command_goal null or populated?", "section": "terminal"},
    {"id": "RIQ09", "question": "If null, is the lane actually closed or merely waiting for external input?", "section": "terminal"},
    {"id": "RIQ10", "question": "What pressure class remains, if any?", "section": "pressure"},
    {"id": "RIQ11", "question": "Is there evidence for a dominant bottleneck?", "section": "pressure"},
    {"id": "RIQ12", "question": "If yes, which receipt fields prove it?", "section": "pressure"},
    {"id": "RIQ13", "question": "If no, what is the smallest lawful next evidence-gathering objective?", "section": "pressure"},
    {"id": "RIQ14", "question": "Is optimization forbidden at this point?", "section": "guard"},
    {"id": "RIQ15", "question": "Is a new objective allowed, or must the loop stop?", "section": "classifier"},
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

RECEIPT_INTERROGATION_QUESTION_SCHEMA = {
    "schema_version": "receipt_interrogation_question_schema_v0",
    "question_set_id": "RECEIPT_INTERROGATION_QUESTIONS_V0",
    "questions": QUESTION_SET,
    "law": [
        "questions classify receipt-licensed next-boundary state",
        "questions do not invent objective details",
        "questions do not authorize work by themselves",
    ],
}

RECEIPT_INTERROGATION_ANSWER_SCHEMA = {
    "schema_version": "receipt_interrogation_answer_schema_v0",
    "required_fields": [
        "receipt_ref",
        "question_set_id",
        "answers",
        "evidence_fields",
        "must_not_infer",
        "unanswered_questions",
    ],
    "answer_law": [
        "every nontrivial answer must cite a receipt field",
        "missing receipt fields must produce INVALID_RECEIPT_SURFACE or QUESTION_PACKET_NOT_COMMAND",
        "answers may classify pressure but must not invent commands",
    ],
}

PRESSURE_CLASSIFICATION_SCHEMA = {
    "schema_version": "pressure_classification_schema_v0",
    "pressure_classes": PRESSURE_CLASSES,
    "classification_rules": {
        "NONE": "gate PASS, terminal STOP_DONE, next_command_goal null, no live pressure metrics, no missing evidence",
        "MISSING_MOVE_PRESSURE": "receipt shows STOP_NEEDS_NEW_MOVE, STOP_NO_APPLICABLE_MOVE, missing move delta, or move registry gap",
        "AUTHORITY_BOUNDARY": "receipt shows STOP_AUTHORITY_BOUNDARY, STOP_HUMAN_REVIEW_REQUIRED, STOP_PROPOSAL_REQUIRED, STOP_FORBIDDEN_MOVE, or unauthorized execution",
        "TAXONOMY_PRESSURE": "receipt shows STOP_TAXONOMY_GAP, undertyped/untyped object or unresolved taxonomy pressure",
        "BURDEN_PRESSURE": "receipt shows burden_pressure_count > 0, receipt burden expansion, or trace density pressure",
        "RECEIPT_TRACE_PRESSURE": "receipt_trace_mismatch_count > 0 or missing/unlinked trace refs",
        "EXTRACTION_PRESSURE": "receipt shows STOP_NEEDS_EXTRACTION or unresolved extraction dependency",
        "FRONTIER_PRESSURE": "receipt shows STOP_FRONTIER or frontier boundary",
        "REAL_BATCH_REQUIRED": "receipt gate PASS with demo-only metrics and no real batch receipts",
        "AMBIGUOUS_PRESSURE": "more than one live pressure class is plausible and no dominant evidence field resolves it",
        "INVALID_RECEIPT_SURFACE": "receipt missing gate, terminal, target unit, receipt id, or required source links",
    },
    "law": [
        "pressure class requires evidence fields",
        "pressure can license a proposal or evidence wait, not necessarily a build command",
        "dominant pressure must not hide secondary pressure",
    ],
}

NEXT_COMMAND_CLASSIFIER_SCHEMA = {
    "schema_version": "next_command_classifier_schema_v0",
    "next_command_classes": NEXT_COMMAND_CLASSES,
    "rules_ordered": [
        {"if": "receipt missing required gate/terminal/identity fields", "emit": "INVALID_RECEIPT_SURFACE"},
        {"if": "gate != PASS", "emit": "REPAIR_COMMAND"},
        {"if": "receipt_trace_mismatch_count > 0 or missing trace links > 0", "emit": "RECEIPT_REPAIR_COMMAND"},
        {"if": "unauthorized movement counted as radius or authority integrity violated", "emit": "POLICY_REPAIR_COMMAND"},
        {"if": "next_command_goal is populated", "emit": "EXECUTE_DECLARED_NEXT_COMMAND", "guard": "only exact declared command after authority check"},
        {"if": "STOP_DONE and next_command_goal is null and no pressure remains", "emit": "STOP_LANE_CLOSED"},
        {"if": "STOP_DONE and next_command_goal is null and metrics are demo-only", "emit": "AWAIT_REAL_BATCH_RECEIPTS"},
        {"if": "dominant pressure exists", "emit": "OPEN_OBJECTIVE_PROPOSAL_FROM_PRESSURE_CLASS"},
        {"if": "pressure ambiguous", "emit": "QUESTION_PACKET_NOT_COMMAND"},
    ],
    "law": [
        "classifier emits command class, not creative roadmap",
        "OPEN_OBJECTIVE_PROPOSAL_FROM_PRESSURE_CLASS is proposal-only and not an implementation command",
        "AWAIT_REAL_BATCH_RECEIPTS is not a build command",
        "STOP_LANE_CLOSED is terminal unless a new external objective is opened",
        "classifier must not optimize, widen authority, or claim global planning",
    ],
}

RECEIPT_INTERROGATION_REPORT_SCHEMA = {
    "schema_version": "receipt_interrogation_report_schema_v0",
    "required_fields": [
        "receipt_interrogation_report_id",
        "source_receipt_ref",
        "question_set_id",
        "answers",
        "pressure_classification",
        "next_command_classification",
        "evidence_fields",
        "must_not_impersonate",
        "allowed_next_handling",
    ],
    "must_not_impersonate": [
        "roadmap invention",
        "authority grant",
        "optimization instruction",
        "global planner",
        "proof of correctness",
        "permission to ignore STOP_DONE",
    ],
}

DAY7_RECEIPT_INTERROGATION_DEMO_PLAN = {
    "schema_version": "receipt_interrogation_demo_plan_v0",
    "demo_name": "DAY7_CLOSURE_RADIUS_RECEIPT_INTERROGATION",
    "source_receipt_id": CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID,
    "expected_primary_class": "STOP_LANE_CLOSED",
    "expected_secondary_class": "AWAIT_REAL_BATCH_RECEIPTS",
    "expected_pressure_class": "REAL_BATCH_REQUIRED",
    "expected_command_authorized": False,
    "expected_proposal_authorized": True,
    "interpretation": "The Day 7 lane is closed, but the metrics are demo-only, so no build command is licensed by the receipt alone.",
}

REQUIRED_IMPLEMENTATION_ARTIFACTS = {
    "receipt_interrogation_question_schema": "data/receipt_interrogation_adapter_v0/receipt_interrogation_question_schema_v0.json",
    "receipt_interrogation_answer_schema": "data/receipt_interrogation_adapter_v0/receipt_interrogation_answer_schema_v0.json",
    "pressure_classification_schema": "data/receipt_interrogation_adapter_v0/pressure_classification_schema_v0.json",
    "next_command_classifier_schema": "data/receipt_interrogation_adapter_v0/next_command_classifier_schema_v0.json",
    "receipt_interrogation_report_schema": "data/receipt_interrogation_adapter_v0/receipt_interrogation_report_schema_v0.json",
    "day7_demo_receipt_interrogation": "data/receipt_interrogation_adapter_v0_demo/day7_demo_receipt_interrogation.json",
    "implementation_receipt": "data/receipt_interrogation_adapter_v0_implementation_receipts/<receipt_id>.json",
}

ACCEPTANCE_GATES = {
    "RIA0_source_surface_verified": {"required": True, "description": "Consumes explicit closure-radius implementation receipt and prior control surfaces by exact id."},
    "RIA1_question_set_declared": {"required": True, "description": "Fixed receipt interrogation question set is declared."},
    "RIA2_answer_schema_requires_evidence_fields": {"required": True, "description": "Answers must point to receipt fields."},
    "RIA3_pressure_classes_declared": {"required": True, "description": "Pressure classes include NONE, repair, authority, taxonomy, burden, receipt/trace, extraction, frontier, real batch, ambiguous, invalid."},
    "RIA4_next_command_classifier_declared": {"required": True, "description": "Classifier emits finite next command classes."},
    "RIA5_failed_gate_maps_to_repair": {"required": True, "description": "Failed gate emits repair class only."},
    "RIA6_trace_mismatch_maps_to_receipt_repair": {"required": True, "description": "Trace mismatch emits receipt repair class."},
    "RIA7_unauthorized_execution_maps_to_policy_repair": {"required": True, "description": "Authority/radius integrity violation emits policy repair class."},
    "RIA8_declared_next_command_only_exact_after_authority_check": {"required": True, "description": "Populated next_command_goal allows only exact declared command after authority check."},
    "RIA9_stop_done_null_next_closes_lane_unless_pressure_or_demo_only": {"required": True, "description": "STOP_DONE with null next closes lane unless pressure/evidence wait remains."},
    "RIA10_demo_only_metrics_classify_as_await_real_batch": {"required": True, "description": "Demo-only metrics produce AWAIT_REAL_BATCH_RECEIPTS, not a build command."},
    "RIA11_pressure_objective_is_proposal_not_command": {"required": True, "description": "Dominant pressure may open objective proposal, not direct implementation command."},
    "RIA12_ambiguous_pressure_emits_question_packet": {"required": True, "description": "Ambiguity emits QUESTION_PACKET_NOT_COMMAND."},
    "RIA13_classifier_does_not_optimize_or_invent_roadmap": {"required": True, "description": "Adapter does not optimize or invent roadmap."},
    "RIA14_no_authority_widening_global_planner_or_proof_claim": {"required": True, "description": "No authority widening, global planner, final roadmap, or proof claim."},
}

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

def validate_inputs() -> List[str]:
    failures: List[str] = []

    closure_impl = read_json(CLOSURE_IMPL_RECEIPT_PATH)
    closure_policy = read_json(CLOSURE_POLICY_PATH)
    closure_policy_receipt = read_json(CLOSURE_POLICY_RECEIPT_PATH)
    day7_demo_report = read_json(DAY7_DEMO_RADIUS_REPORT_PATH)
    day7_rollup = read_json(DAY7_DEMO_RADIUS_ROLLUP_PATH)
    tax_impl = read_json(TAX_IMPL_RECEIPT_PATH)
    juris_impl = read_json(JURIS_IMPL_RECEIPT_PATH)
    move_impl = read_json(MOVE_IMPL_RECEIPT_PATH)
    halt_impl = read_json(HALT_IMPLEMENTATION_RECEIPT_PATH)
    proceed = read_json(PROCEED_RECEIPT_PATH)
    trace_ledger = read_json(TRACE_LEDGER_RECEIPT_PATH)
    trace_schema = read_json(TRACE_SCHEMA_PATH)
    proposal_ledger = read_json(PROPOSAL_LEDGER_SCHEMA_PATH)
    regime = read_json(LOCAL_REGIME_V1_PATH)

    if closure_impl.get("receipt_id") != CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID or closure_impl.get("gate") != "PASS":
        failures.append("closure_radius_implementation_source_not_pass")
    if closure_impl.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append("closure_radius_terminal_not_done")
    if closure_impl.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("closure_radius_next_command_not_null")
    if closure_impl.get("aggregate_metrics", {}).get("lawful_improvement_count") != 1:
        failures.append("closure_radius_lawful_improvement_count_wrong")
    if closure_impl.get("aggregate_metrics", {}).get("productive_taxonomy_pressure_count") != 1:
        failures.append("closure_radius_productive_taxonomy_pressure_count_wrong")
    if closure_impl.get("aggregate_metrics", {}).get("illegal_improvement_rejected_count") != 1:
        failures.append("closure_radius_illegal_improvement_rejected_count_wrong")
    if closure_impl.get("aggregate_metrics", {}).get("burden_pressure_count") != 1:
        failures.append("closure_radius_burden_pressure_count_wrong")
    for key in [
        "unauthorized_moves_counted_as_radius_count",
        "proposal_only_counted_as_execution_count",
        "blocked_moves_counted_as_execution_count",
        "human_review_request_counted_as_execution_count",
        "taxonomy_proposal_counted_as_patch_count",
        "halt_counts_hidden_under_average_count",
        "higher_radius_treated_as_always_better_count",
        "optimization_performed_count",
        "global_closure_claim_count",
        "final_intelligence_claim_count",
        "autonomy_claim_count",
        "proof_claim_count",
        "hidden_continuation_count",
    ]:
        if closure_impl.get("aggregate_metrics", {}).get(key) != 0:
            failures.append(f"closure_radius_metric_not_zero:{key}:{closure_impl.get('aggregate_metrics', {}).get(key)}")

    if closure_policy.get("policy_id") != CLOSURE_RADIUS_POLICY_ID:
        failures.append("closure_policy_id_wrong")
    if closure_policy_receipt.get("receipt_id") != CLOSURE_RADIUS_POLICY_RECEIPT_ID:
        failures.append("closure_policy_receipt_id_wrong")
    if day7_demo_report.get("gate") != "PASS" or day7_rollup.get("gate") != "PASS":
        failures.append("day7_demo_or_rollup_not_pass")
    if day7_demo_report.get("summary", {}).get("scenario_count") != 4:
        failures.append("day7_demo_scenario_count_wrong")
    if day7_rollup.get("batch_scope", {}).get("runs_total") != 4:
        failures.append("day7_rollup_runs_total_wrong")

    if tax_impl.get("receipt_id") != TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID or tax_impl.get("gate") != "PASS":
        failures.append("taxonomy_source_not_pass")
    if juris_impl.get("receipt_id") != JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID or juris_impl.get("gate") != "PASS":
        failures.append("jurisdiction_source_not_pass")
    if move_impl.get("receipt_id") != MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID or move_impl.get("gate") != "PASS":
        failures.append("move_registry_source_not_pass")
    if halt_impl.get("receipt_id") != HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID or halt_impl.get("gate") != "PASS":
        failures.append("halt_vocab_source_not_pass")
    if proceed.get("receipt_id") != PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID or proceed.get("gate") != "PASS":
        failures.append("proceed_source_not_pass")
    if trace_ledger.get("receipt_id") != TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID or trace_ledger.get("gate") != "PASS":
        failures.append("trace_ledger_source_not_pass")
    if trace_schema.get("schema_version") != "jurisdiction_runner_trace_file_v0":
        failures.append("trace_schema_wrong")
    if proposal_ledger.get("schema_version") != "unresolved_proposal_ledger_v0":
        failures.append("proposal_ledger_wrong")
    if regime.get("local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append("local_regime_wrong")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def validate_policy(policy: Dict[str, Any], receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if policy.get("gate") != "PASS":
        failures.append(f"policy_gate_not_PASS:{policy.get('gate')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if policy.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{policy.get('policy_status')}")
    if policy.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append(f"target_wrong:{policy.get('target_unit_id')}")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append(f"receipt_target_wrong:{receipt.get('target_unit_id')}")

    qschema = policy.get("receipt_interrogation_question_schema", {})
    if qschema.get("question_set_id") != "RECEIPT_INTERROGATION_QUESTIONS_V0":
        failures.append("question_set_id_wrong")
    if len(qschema.get("questions", [])) != 15:
        failures.append(f"question_count_wrong:{len(qschema.get('questions', []))}")
    for qid in [f"RIQ{i:02d}" for i in range(1, 16)]:
        if qid not in [q.get("id") for q in qschema.get("questions", [])]:
            failures.append(f"question_missing:{qid}")
    if "questions do not authorize work by themselves" not in qschema.get("law", []):
        failures.append("question_no_authority_law_missing")

    aschema = policy.get("receipt_interrogation_answer_schema", {})
    for field in ["receipt_ref", "question_set_id", "answers", "evidence_fields", "must_not_infer", "unanswered_questions"]:
        if field not in aschema.get("required_fields", []):
            failures.append(f"answer_required_missing:{field}")
    if "every nontrivial answer must cite a receipt field" not in aschema.get("answer_law", []):
        failures.append("answer_evidence_law_missing")

    pressure = policy.get("pressure_classification_schema", {})
    for cls in PRESSURE_CLASSES:
        if cls not in pressure.get("pressure_classes", []):
            failures.append(f"pressure_class_missing:{cls}")
    if "pressure class requires evidence fields" not in pressure.get("law", []):
        failures.append("pressure_evidence_law_missing")
    if "pressure can license a proposal or evidence wait, not necessarily a build command" not in pressure.get("law", []):
        failures.append("pressure_not_command_law_missing")

    classifier = policy.get("next_command_classifier_schema", {})
    for cls in NEXT_COMMAND_CLASSES:
        if cls not in classifier.get("next_command_classes", []):
            failures.append(f"next_command_class_missing:{cls}")
    classifier_laws = classifier.get("law", [])
    if "classifier emits command class, not creative roadmap" not in classifier_laws:
        failures.append("classifier_not_roadmap_law_missing")
    if "OPEN_OBJECTIVE_PROPOSAL_FROM_PRESSURE_CLASS is proposal-only and not an implementation command" not in classifier_laws:
        failures.append("pressure_proposal_not_command_law_missing")
    if "AWAIT_REAL_BATCH_RECEIPTS is not a build command" not in classifier_laws:
        failures.append("await_real_batch_not_command_law_missing")
    rules = classifier.get("rules_ordered", [])
    required_emits = [
        "INVALID_RECEIPT_SURFACE",
        "REPAIR_COMMAND",
        "RECEIPT_REPAIR_COMMAND",
        "POLICY_REPAIR_COMMAND",
        "EXECUTE_DECLARED_NEXT_COMMAND",
        "STOP_LANE_CLOSED",
        "AWAIT_REAL_BATCH_RECEIPTS",
        "OPEN_OBJECTIVE_PROPOSAL_FROM_PRESSURE_CLASS",
        "QUESTION_PACKET_NOT_COMMAND",
    ]
    for emit in required_emits:
        if emit not in [r.get("emit") for r in rules]:
            failures.append(f"classifier_rule_missing:{emit}")

    report_schema = policy.get("receipt_interrogation_report_schema", {})
    for field in ["source_receipt_ref", "answers", "pressure_classification", "next_command_classification", "evidence_fields"]:
        if field not in report_schema.get("required_fields", []):
            failures.append(f"report_required_missing:{field}")
    for phrase in ["roadmap invention", "authority grant", "optimization instruction", "global planner", "proof of correctness", "permission to ignore STOP_DONE"]:
        if phrase not in report_schema.get("must_not_impersonate", []):
            failures.append(f"report_must_not_impersonate_missing:{phrase}")

    demo = policy.get("day7_receipt_interrogation_demo_plan", {})
    if demo.get("expected_primary_class") != "STOP_LANE_CLOSED":
        failures.append("day7_demo_primary_class_wrong")
    if demo.get("expected_secondary_class") != "AWAIT_REAL_BATCH_RECEIPTS":
        failures.append("day7_demo_secondary_class_wrong")
    if demo.get("expected_pressure_class") != "REAL_BATCH_REQUIRED":
        failures.append("day7_demo_pressure_wrong")
    if demo.get("expected_command_authorized") is not False:
        failures.append("day7_demo_command_authorized_wrong")
    if demo.get("expected_proposal_authorized") is not True:
        failures.append("day7_demo_proposal_authorized_wrong")

    gates = policy.get("acceptance_gates", {})
    for gate in ACCEPTANCE_GATES:
        if gates.get(gate, {}).get("required") is not True:
            failures.append(f"acceptance_gate_missing:{gate}")

    guards = policy.get("adapter_guards", {})
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
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "implementation_performed_by_policy",
        "demo_classification_emitted_by_policy",
        "command_emitted_by_policy",
        "objective_invented_by_policy",
        "optimization_performed_by_policy",
        "authority_widened_by_policy",
        "source_closure_radius_modified",
        "source_taxonomy_evolution_modified",
        "source_jurisdiction_gate_modified",
        "source_move_registry_modified",
        "source_halt_vocabulary_modified",
        "source_proceed_adapter_modified",
        "source_trace_ledger_runner_modified",
        "global_planner_claimed",
        "final_roadmap_claimed",
        "proof_claimed",
        "hidden_continuation_authorized",
        "sqlite_registry_written",
    ]:
        if guards.get(key) is not False:
            failures.append(f"guard_not_false:{key}:{guards.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "ADVANCE":
        failures.append(f"terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != NEXT_GOAL:
        failures.append(f"terminal_next_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"terminal_stop_not_null:{terminal.get('stop_code')}")

    return failures

def build_policy(write_outputs: bool = True) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    failures = validate_inputs()

    seed = {
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_closure_receipt": CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID,
        "question_set": "RECEIPT_INTERROGATION_QUESTIONS_V0",
        "next_goal": NEXT_GOAL,
    }
    policy_id = sha8(seed)

    adapter_guards = {
        "policy_built": True,
        "source_closure_radius_receipt_consumed": True,
        "source_taxonomy_evolution_receipt_consumed": True,
        "source_jurisdiction_gate_receipt_consumed": True,
        "source_move_registry_receipt_consumed": True,
        "source_halt_vocabulary_receipt_consumed": True,
        "source_proceed_adapter_receipt_consumed": True,
        "source_trace_ledger_surface_consumed": True,
        "implementation_performed_by_policy": False,
        "demo_classification_emitted_by_policy": False,
        "command_emitted_by_policy": False,
        "objective_invented_by_policy": False,
        "optimization_performed_by_policy": False,
        "authority_widened_by_policy": False,
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

    policy = {
        "schema_version": "receipt_interrogation_adapter_v0_policy_v0",
        "policy_type": "RECEIPT_INTERROGATION_ADAPTER_V0_POLICY",
        "policy_id": policy_id,
        "unit_id": UNIT_ID,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "target_unit_id": TARGET_UNIT_ID,
        "source_closure_radius_implementation_receipt_id": CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID,
        "source_closure_radius_policy_id": CLOSURE_RADIUS_POLICY_ID,
        "source_closure_radius_policy_receipt_id": CLOSURE_RADIUS_POLICY_RECEIPT_ID,
        "source_taxonomy_evolution_implementation_receipt_id": TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID,
        "source_jurisdiction_gate_implementation_receipt_id": JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID,
        "source_move_registry_implementation_receipt_id": MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID,
        "source_halt_vocabulary_implementation_receipt_id": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "policy_summary": {
            "purpose": "Given an implementation receipt, ask a fixed question set and classify the receipt-licensed next-boundary state.",
            "core_law": "The adapter classifies licensed next-boundary state; it does not invent the next project.",
            "non_goal": "no roadmap invention, no optimization, no authority widening, no proof claim, no hidden command after STOP_DONE",
            "current_day7_expected_classification": "STOP_LANE_CLOSED plus AWAIT_REAL_BATCH_RECEIPTS",
        },
        "receipt_interrogation_question_schema": RECEIPT_INTERROGATION_QUESTION_SCHEMA,
        "receipt_interrogation_answer_schema": RECEIPT_INTERROGATION_ANSWER_SCHEMA,
        "pressure_classification_schema": PRESSURE_CLASSIFICATION_SCHEMA,
        "next_command_classifier_schema": NEXT_COMMAND_CLASSIFIER_SCHEMA,
        "receipt_interrogation_report_schema": RECEIPT_INTERROGATION_REPORT_SCHEMA,
        "day7_receipt_interrogation_demo_plan": DAY7_RECEIPT_INTERROGATION_DEMO_PLAN,
        "required_implementation_artifacts": REQUIRED_IMPLEMENTATION_ARTIFACTS,
        "acceptance_gates": ACCEPTANCE_GATES,
        "authorized_operations_next": {
            "read_receipt_interrogation_policy": True,
            "read_receipt_interrogation_policy_receipt": True,
            "write_question_schema": True,
            "write_answer_schema": True,
            "write_pressure_classification_schema": True,
            "write_next_command_classifier_schema": True,
            "write_report_schema": True,
            "emit_day7_demo_receipt_interrogation": True,
            "emit_implementation_receipt": True,
        },
        "forbidden_operations_next": {
            "invent_roadmap": True,
            "emit_build_command_from_pressure_directly": True,
            "optimize_runner": True,
            "widen_authority": True,
            "ignore_stop_done": True,
            "treat_demo_only_as_real_batch": True,
            "mutate_source_receipts": True,
            "mutate_source_registries": True,
            "modify_source_modules": True,
            "claim_global_planner": True,
            "claim_final_roadmap": True,
            "claim_proof": True,
            "hidden_continuation_after_terminal": True,
            "sqlite_registry_write": True,
            "latest_or_mtime_selection": True,
            "ambient_workspace_authority": True,
        },
        "safety_clauses": {
            "policy_only": True,
            "does_not_emit_demo_classification": True,
            "does_not_emit_command": True,
            "does_not_invent_objective": True,
            "does_not_optimize": True,
            "does_not_widen_authority": True,
            "does_not_modify_source_artifacts": True,
            "does_not_claim_global_planning": True,
            "next_unit_required_for_implementation": True,
        },
        "adapter_guards": adapter_guards,
        "terminal": {
            "type": "ADVANCE",
            "next_command_goal": NEXT_GOAL,
            "stop_code": None,
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "policy_id": policy_id,
        "target_unit_id": TARGET_UNIT_ID,
        "source_closure_receipt": CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID,
        "terminal": policy["terminal"],
    }
    receipt_id = sha8(receipt_seed)
    policy["policy_receipt_id"] = receipt_id

    receipt = {
        "schema_version": "receipt_interrogation_adapter_v0_policy_receipt_v0",
        "receipt_type": "RECEIPT_INTERROGATION_ADAPTER_V0_POLICY_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": receipt_id,
        "policy_id": policy_id,
        "policy_status": policy["policy_status"],
        "target_unit_id": TARGET_UNIT_ID,
        "source_closure_radius_implementation_receipt_id": CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID,
        "source_closure_radius_policy_id": CLOSURE_RADIUS_POLICY_ID,
        "source_closure_radius_policy_receipt_id": CLOSURE_RADIUS_POLICY_RECEIPT_ID,
        "source_taxonomy_evolution_implementation_receipt_id": TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID,
        "source_jurisdiction_gate_implementation_receipt_id": JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID,
        "source_move_registry_implementation_receipt_id": MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID,
        "source_halt_vocabulary_implementation_receipt_id": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "policy_summary": policy["policy_summary"],
        "receipt_interrogation_question_schema": RECEIPT_INTERROGATION_QUESTION_SCHEMA,
        "receipt_interrogation_answer_schema": RECEIPT_INTERROGATION_ANSWER_SCHEMA,
        "pressure_classification_schema": PRESSURE_CLASSIFICATION_SCHEMA,
        "next_command_classifier_schema": NEXT_COMMAND_CLASSIFIER_SCHEMA,
        "receipt_interrogation_report_schema": RECEIPT_INTERROGATION_REPORT_SCHEMA,
        "day7_receipt_interrogation_demo_plan": DAY7_RECEIPT_INTERROGATION_DEMO_PLAN,
        "required_implementation_artifacts": REQUIRED_IMPLEMENTATION_ARTIFACTS,
        "acceptance_gates": ACCEPTANCE_GATES,
        "authorized_operations_next": policy["authorized_operations_next"],
        "forbidden_operations_next": policy["forbidden_operations_next"],
        "safety_clauses": policy["safety_clauses"],
        "adapter_guards": adapter_guards,
        "terminal": policy["terminal"],
        "gate": policy["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    failures.extend(validate_policy(policy, receipt))
    policy["failures"] = failures
    receipt["failures"] = failures
    policy["gate"] = "PASS" if not failures else "FAIL"
    receipt["gate"] = policy["gate"]

    if write_outputs:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
        write_json(OUT_DIR / f"{policy_id}.json", policy)
        write_json(OUT_RECEIPT_DIR / f"{policy_id}.json", receipt)

    return policy, receipt

def main() -> int:
    policy, receipt = build_policy(write_outputs=True)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"receipt_interrogation_policy_id={policy['policy_id']}")
    print(f"receipt_interrogation_policy_receipt_id={receipt['receipt_id']}")
    print(f"receipt_interrogation_policy_path=data/receipt_interrogation_adapter_v0_policies/{policy['policy_id']}.json")
    print(f"receipt_interrogation_policy_receipt_path=data/receipt_interrogation_adapter_v0_policy_receipts/{policy['policy_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
