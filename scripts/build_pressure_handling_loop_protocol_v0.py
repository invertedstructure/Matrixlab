#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_PRESSURE_HANDLING_LOOP_PROTOCOL_V0"
TARGET_UNIT_ID = "pressure_handling_loop_protocol.v0"
EXPECTED_NEXT_UNIT = "APPLY_PRESSURE_HANDLING_LOOP_TO_R1000_TOP_GROUP_TAXONOMY_GAP_V0"

SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID = "7c9718e0"
SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID = "a121ff40"
SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID = "fabba052"
SOURCE_COARSENING_REVIEW_RECEIPT_ID = "f03689e3"
SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID = "f09b8395"

OUT_DIR = ROOT / "data" / "pressure_handling_loop_protocol_v0"
RECEIPT_DIR = ROOT / "data" / "pressure_handling_loop_protocol_v0_receipts"

STATE_SCHEMA_PATH = OUT_DIR / "pressure_handling_state_schema_v0.json"
GROUP_SCHEMA_PATH = OUT_DIR / "pressure_group_schema_v0.json"
CLASSIFICATION_SCHEMA_PATH = OUT_DIR / "pressure_classification_schema_v0.json"
EVIDENCE_SCHEMA_PATH = OUT_DIR / "pressure_evidence_sufficiency_schema_v0.json"
TRANSITION_SCHEMA_PATH = OUT_DIR / "pressure_handling_transition_schema_v0.json"
RESOLUTION_SCHEMA_PATH = OUT_DIR / "pressure_resolution_schema_v0.json"
PROTOCOL_PATH = OUT_DIR / "pressure_handling_loop_protocol.json"
REPORT_PATH = OUT_DIR / "pressure_handling_loop_report.json"
DECISION_PACKET_PATH = OUT_DIR / "pressure_handling_loop_decision_packet.json"

TOP_GROUP_RECEIPT_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0_receipts" / f"{SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID}.json"
TOP_GROUP_SELECTION_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_selection.json"
TOP_GROUP_MEMBERSHIP_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_event_membership.jsonl"
TOP_GROUP_FRAGMENTS_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_representative_fragments.json"
TOP_GROUP_EVIDENCE_ROLLUP_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_evidence_rollup.json"
TOP_GROUP_CLASSIFICATION_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_classification.json"
TOP_GROUP_DECISION_PACKET_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_decision_packet.json"
TOP_GROUP_REPAIR_PROPOSAL_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_repair_objective_proposal.json"
R1000_SCALE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0_receipts" / f"{SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID}.json"
CANDIDATE_C_RECEIPT_PATH = ROOT / "data" / "r250_pressure_candidate_c_interrogation_v0_receipts" / f"{SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID}.json"
COARSENING_RECEIPT_PATH = ROOT / "data" / "r250_pressure_coarsening_review_v0_receipts" / f"{SOURCE_COARSENING_REVIEW_RECEIPT_ID}.json"
PRESSURE_METRICS_RECEIPT_PATH = ROOT / "data" / "r250_pressure_metrics_v0_receipts" / f"{SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID}.json"

SOURCE_FILES = [
    TOP_GROUP_RECEIPT_PATH,
    TOP_GROUP_SELECTION_PATH,
    TOP_GROUP_MEMBERSHIP_PATH,
    TOP_GROUP_FRAGMENTS_PATH,
    TOP_GROUP_EVIDENCE_ROLLUP_PATH,
    TOP_GROUP_CLASSIFICATION_PATH,
    TOP_GROUP_DECISION_PACKET_PATH,
    TOP_GROUP_REPAIR_PROPOSAL_PATH,
    R1000_SCALE_RECEIPT_PATH,
    CANDIDATE_C_RECEIPT_PATH,
    COARSENING_RECEIPT_PATH,
    PRESSURE_METRICS_RECEIPT_PATH,
]

STATES = [
    "RUN_OBJECTIVE",
    "DETECT_PRESSURE",
    "SELECT_PRESSURE_GROUP",
    "INSPECT_PRESSURE_GROUP",
    "CHECK_EVIDENCE_SUFFICIENCY",
    "CLASSIFY_PRESSURE_GROUP",
    "HANDLE_FIXABLE_PRESSURE",
    "HANDLE_HEALTHY_EXPECTED_PRESSURE",
    "HANDLE_NOT_ENOUGH_EVIDENCE",
    "RERUN_AFTER_HANDLING",
    "CHECK_PRESSURE_RESOLUTION",
    "MOVE_TO_NEXT_PRESSURE_GROUP",
    "PROCEED_TO_NEXT_OBJECTIVE",
    "STOP_HUMAN_DECISION_REQUIRED",
    "STOP_GATE_FAIL",
    "STOP_AUTHORITY_VIOLATION",
    "STOP_RECEIPT_MISMATCH",
]

CLASSIFICATIONS = [
    "FIXABLE_PRESSURE",
    "HEALTHY_EXPECTED_PRESSURE",
    "NOT_ENOUGH_EVIDENCE",
]

EVIDENCE_CLASSES = [
    "EVIDENCE_SUFFICIENT_FOR_FIXABLE_CLASSIFICATION",
    "EVIDENCE_SUFFICIENT_FOR_HEALTHY_CLASSIFICATION",
    "EVIDENCE_INSUFFICIENT_NEEDS_MORE_FRAGMENTS",
    "EVIDENCE_INSUFFICIENT_NEEDS_DEEPER_MEMBERSHIP",
    "EVIDENCE_INSUFFICIENT_NEEDS_FIELD_EXTRACTION",
    "EVIDENCE_INSUFFICIENT_NEEDS_TOP_TWO_COMPARISON",
    "EVIDENCE_INSUFFICIENT_NEEDS_SCALE_BAND",
    "EVIDENCE_BLOCKED_BY_AUTHORITY",
]

RESOLUTION_CLASSES = [
    "PRESSURE_GONE",
    "PRESSURE_REDUCED",
    "PRESSURE_UNCHANGED",
    "PRESSURE_WORSENED",
    "PRESSURE_SHIFTED",
]

PRESSURE_GROUP_FIELDS = [
    "pressure_group_key_hash",
    "pressure_lens_id",
    "pressure_lens_fields",
    "parent_pressure_class",
    "pressure_subtype",
    "halt_reason",
    "group_count",
    "group_share",
    "rank",
    "second_group_count",
    "dominant_margin",
    "dominant_margin_share",
    "low_margin_warning",
    "source_event_ids",
    "source_receipt_refs",
    "source_trace_refs",
    "representative_fragment_refs",
    "classification",
    "evidence_sufficiency_class",
    "handling_status",
    "resolution_status",
]

HUMAN_DECISION = {
    "decision": "BUILD_FIXED_LOCAL_PRESSURE_HANDLING_LOOP_PROTOCOL",
    "scope": "protocol_construction_only",
    "loop_rule": "pressure_authorizes_inspection_not_action",
    "rank_rule": "stable_rank_authorizes_inspection_order_not_repair",
    "not_authorized": [
        "repair_execution",
        "taxonomy_upgrade",
        "authority_widening",
        "burden_optimization",
        "extraction_repair",
        "ranked_protocol_global_adoption",
        "next_group_auto_open",
        "next_objective_without_supplied_objective_id",
    ],
}

MUST_NOT_INFER = [
    "protocol construction is not pressure handling yet",
    "pressure does not authorize action",
    "pressure authorizes inspection",
    "inspection plus enough evidence authorizes classification",
    "classification may emit proposal, skip, evidence request, next group recommendation, or proceed recommendation",
    "classification does not execute repair",
    "stable rank authorizes inspection order only",
    "stable rank does not authorize repair",
    "no taxonomy upgrade from pressure alone",
    "no authority widening from pressure alone",
    "no optimization from pressure alone",
    "no extraction repair from pressure alone",
    "no next objective without supplied objective id",
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

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

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
        "top_group_receipt": read_json(TOP_GROUP_RECEIPT_PATH),
        "top_group_selection": read_json(TOP_GROUP_SELECTION_PATH),
        "top_group_membership": read_jsonl(TOP_GROUP_MEMBERSHIP_PATH),
        "top_group_fragments": read_json(TOP_GROUP_FRAGMENTS_PATH),
        "top_group_evidence": read_json(TOP_GROUP_EVIDENCE_ROLLUP_PATH),
        "top_group_classification": read_json(TOP_GROUP_CLASSIFICATION_PATH),
        "top_group_packet": read_json(TOP_GROUP_DECISION_PACKET_PATH),
        "top_group_repair_proposal": read_json(TOP_GROUP_REPAIR_PROPOSAL_PATH),
        "r1000_scale_receipt": read_json(R1000_SCALE_RECEIPT_PATH),
        "candidate_c_receipt": read_json(CANDIDATE_C_RECEIPT_PATH),
        "coarsening_receipt": read_json(COARSENING_RECEIPT_PATH),
        "pressure_metrics_receipt": read_json(PRESSURE_METRICS_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    top = sources["top_group_receipt"]
    scale = sources["r1000_scale_receipt"]
    candidate = sources["candidate_c_receipt"]
    coarsening = sources["coarsening_receipt"]
    pressure = sources["pressure_metrics_receipt"]

    if top.get("receipt_id") != SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID:
        failures.append("top_group_receipt_id_wrong")
    if top.get("gate") != "PASS":
        failures.append("top_group_receipt_not_pass")
    if top.get("unit_id") != "CLASSIFY_R1000_CANDIDATE_C_TOP_PRESSURE_GROUP_V0":
        failures.append("top_group_unit_wrong")
    if top.get("top_group_summary", {}).get("classification") != "NOT_ENOUGH_EVIDENCE":
        failures.append("top_group_not_current_unresolved_class")
    if top.get("top_group_summary", {}).get("parent_pressure_class") != "TAXONOMY_PRESSURE":
        failures.append("top_group_parent_wrong")
    if top.get("top_group_summary", {}).get("pressure_subtype") != "missing_label":
        failures.append("top_group_subtype_wrong")
    if top.get("top_group_summary", {}).get("halt_reason") != "STOP_TAXONOMY_GAP":
        failures.append("top_group_halt_wrong")
    if top.get("aggregate_metrics", {}).get("top_group_count") != 25:
        failures.append("top_group_count_wrong")
    if top.get("aggregate_metrics", {}).get("repair_objective_proposal_emitted") is not False:
        failures.append("top_group_repair_proposal_already_emitted")
    if top.get("terminal", {}).get("type") != "STOP":
        failures.append("top_group_terminal_not_stop")
    if top.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("top_group_hidden_next_command")

    if scale.get("receipt_id") != SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID or scale.get("gate") != "PASS":
        failures.append("r1000_scale_receipt_not_pass")
    if scale.get("scale_stability_summary", {}).get("rank_order_preserved") is not True:
        failures.append("r1000_rank_not_preserved")
    if candidate.get("receipt_id") != SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID or candidate.get("gate") != "PASS":
        failures.append("candidate_c_receipt_not_pass")
    if coarsening.get("receipt_id") != SOURCE_COARSENING_REVIEW_RECEIPT_ID or coarsening.get("gate") != "PASS":
        failures.append("coarsening_receipt_not_pass")
    if pressure.get("receipt_id") != SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID or pressure.get("gate") != "PASS":
        failures.append("pressure_metrics_receipt_not_pass")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_schemas() -> Dict[str, Any]:
    state_schema = {
        "schema_version": "pressure_handling_state_schema_v0",
        "states": STATES,
        "terminal_states": [
            "STOP_HUMAN_DECISION_REQUIRED",
            "STOP_GATE_FAIL",
            "STOP_AUTHORITY_VIOLATION",
            "STOP_RECEIPT_MISMATCH",
        ],
        "nonterminal_states": [state for state in STATES if not state.startswith("STOP_")],
    }

    group_schema = {
        "schema_version": "pressure_group_schema_v0",
        "required_fields": PRESSURE_GROUP_FIELDS,
        "pressure_lens_rule": "accepted_lens_fields_only",
        "group_key_forbidden_fields": [
            "work_item_id",
            "slot_id",
            "source_receipt_ref",
            "source_trace_ref",
            "receipt_id",
            "trace_id",
            "timestamp",
            "file_path",
        ],
    }

    classification_schema = {
        "schema_version": "pressure_classification_schema_v0",
        "classes": CLASSIFICATIONS,
        "priority": [
            "NOT_ENOUGH_EVIDENCE",
            "HEALTHY_EXPECTED_PRESSURE",
            "FIXABLE_PRESSURE",
        ],
        "fixable_required_conditions": [
            "specific operational cause exists",
            "bounded repair scope exists",
            "source evidence supports repair direction",
            "repair can be tested by explicit gates",
            "repair does not require taxonomy upgrade unless separately proposed",
            "repair does not widen authority",
            "repair does not rely on pressure label alone",
        ],
        "healthy_expected_conditions": [
            "pressure represents expected halt",
            "lawful authority boundary",
            "expected human decision point",
            "expected evidence requirement",
            "non-actionable diagnostic signal",
        ],
        "not_enough_evidence_conditions": [
            "fragments are insufficient",
            "group mixes causes",
            "pressure subtype is too vague",
            "repair would require guessing",
            "classification would require taxonomy or authority change",
            "evidence fields are missing",
            "operational cause is not inspectable yet",
        ],
        "fixable_may_emit": ["repair objective proposal"],
        "fixable_must_not_emit": [
            "repair command",
            "source mutation",
            "taxonomy upgrade",
            "authority widening",
            "optimization",
        ],
        "not_enough_must_not_emit": ["repair proposal"],
    }

    evidence_schema = {
        "schema_version": "pressure_evidence_sufficiency_schema_v0",
        "classes": EVIDENCE_CLASSES,
        "evidence_enough_if_all": [
            "representative fragments exist",
            "membership is explicit",
            "source event refs are explicit",
            "source receipt refs are explicit",
            "source trace refs are explicit",
            "pressure subtype is interpretable",
            "operational cause can be inspected",
            "classification does not require guessing",
            "classification does not require unauthorized taxonomy or authority change",
        ],
        "evidence_request_required_fields": [
            "evidence_request_id",
            "source_pressure_group_key_hash",
            "evidence_sufficiency_class",
            "missing_evidence_reason",
            "requested_artifacts",
            "forbidden_scope",
            "terminal_rule",
        ],
        "taxonomy": "local_provisional_reviewed_delta_only",
    }

    transition_schema = {
        "schema_version": "pressure_handling_transition_schema_v0",
        "transition_fields": [
            "from_state",
            "condition",
            "to_state",
            "required_outputs",
            "forbidden_outputs",
            "terminal_rule",
        ],
    }

    resolution_schema = {
        "schema_version": "pressure_resolution_schema_v0",
        "classes": RESOLUTION_CLASSES,
        "required_fields": [
            "source_handling_receipt_id",
            "rerun_receipt_id",
            "same_lens_or_changed_lens",
            "pressure_group_before",
            "pressure_group_after",
            "pressure_delta",
            "resolution_class",
        ],
    }

    return {
        "state_schema": state_schema,
        "group_schema": group_schema,
        "classification_schema": classification_schema,
        "evidence_schema": evidence_schema,
        "transition_schema": transition_schema,
        "resolution_schema": resolution_schema,
    }

def build_protocol(sources: Dict[str, Any], schemas: Dict[str, Any]) -> Dict[str, Any]:
    top = sources["top_group_receipt"]
    transitions = [
        {
            "from_state": "RUN_OBJECTIVE",
            "condition": "no pressure",
            "to_state": "PROCEED_TO_NEXT_OBJECTIVE",
            "required_outputs": ["run_receipt", "pressure_summary", "terminal_state"],
            "forbidden_outputs": ["repair_command", "taxonomy_upgrade", "authority_widening"],
            "terminal_rule": "advance only if parent objective supplies next objective id",
        },
        {
            "from_state": "RUN_OBJECTIVE",
            "condition": "pressure found",
            "to_state": "DETECT_PRESSURE",
            "required_outputs": ["run_receipt", "pressure_summary", "terminal_state"],
            "forbidden_outputs": ["repair_command"],
            "terminal_rule": "continue loop",
        },
        {
            "from_state": "DETECT_PRESSURE",
            "condition": "pressure groups exist",
            "to_state": "SELECT_PRESSURE_GROUP",
            "required_outputs": [
                "pressure_found",
                "pressure_group_count",
                "pressure_group_profile",
                "pressure_group_lens",
                "pressure_group_rank_order",
                "pressure_group_stability_status",
            ],
            "forbidden_outputs": ["repair_command", "objective_command"],
            "terminal_rule": "continue loop",
        },
        {
            "from_state": "DETECT_PRESSURE",
            "condition": "no pressure groups",
            "to_state": "PROCEED_TO_NEXT_OBJECTIVE",
            "required_outputs": ["pressure_found:false", "pressure_group_count:0"],
            "forbidden_outputs": ["repair_command"],
            "terminal_rule": "advance only if parent objective supplies next objective id",
        },
        {
            "from_state": "SELECT_PRESSURE_GROUP",
            "condition": "actionable group exists",
            "to_state": "INSPECT_PRESSURE_GROUP",
            "required_outputs": [
                "selected_pressure_group_key_hash",
                "selection_rule",
                "rank_order",
            ],
            "forbidden_outputs": ["repair_command", "repair_proposal"],
            "terminal_rule": "stable rank authorizes inspection order only",
        },
        {
            "from_state": "INSPECT_PRESSURE_GROUP",
            "condition": "membership and fragments extracted",
            "to_state": "CHECK_EVIDENCE_SUFFICIENCY",
            "required_outputs": [
                "pressure_group_selection",
                "pressure_group_membership",
                "pressure_group_representative_fragments",
                "pressure_group_evidence_rollup",
            ],
            "forbidden_outputs": ["repair_command"],
            "terminal_rule": "continue loop",
        },
        {
            "from_state": "CHECK_EVIDENCE_SUFFICIENCY",
            "condition": "evidence sufficient",
            "to_state": "CLASSIFY_PRESSURE_GROUP",
            "required_outputs": ["evidence_sufficiency_class"],
            "forbidden_outputs": ["repair_command"],
            "terminal_rule": "continue loop",
        },
        {
            "from_state": "CHECK_EVIDENCE_SUFFICIENCY",
            "condition": "evidence insufficient",
            "to_state": "HANDLE_NOT_ENOUGH_EVIDENCE",
            "required_outputs": ["evidence_sufficiency_class", "missing_evidence_reason"],
            "forbidden_outputs": ["repair_proposal", "repair_command"],
            "terminal_rule": "STOP_HUMAN_DECISION_REQUIRED",
        },
        {
            "from_state": "CLASSIFY_PRESSURE_GROUP",
            "condition": "FIXABLE_PRESSURE",
            "to_state": "HANDLE_FIXABLE_PRESSURE",
            "required_outputs": ["classification_exactly_once", "classification_reason"],
            "forbidden_outputs": ["repair_command"],
            "terminal_rule": "continue loop",
        },
        {
            "from_state": "CLASSIFY_PRESSURE_GROUP",
            "condition": "HEALTHY_EXPECTED_PRESSURE",
            "to_state": "HANDLE_HEALTHY_EXPECTED_PRESSURE",
            "required_outputs": ["classification_exactly_once", "classification_reason"],
            "forbidden_outputs": ["repair_proposal", "repair_command"],
            "terminal_rule": "continue loop",
        },
        {
            "from_state": "CLASSIFY_PRESSURE_GROUP",
            "condition": "NOT_ENOUGH_EVIDENCE",
            "to_state": "HANDLE_NOT_ENOUGH_EVIDENCE",
            "required_outputs": ["classification_exactly_once", "classification_reason"],
            "forbidden_outputs": ["repair_proposal", "repair_command"],
            "terminal_rule": "STOP_HUMAN_DECISION_REQUIRED",
        },
        {
            "from_state": "HANDLE_FIXABLE_PRESSURE",
            "condition": "concrete bounded repair objective exists",
            "to_state": "STOP_HUMAN_DECISION_REQUIRED",
            "required_outputs": [
                "repair_objective_id",
                "repair_scope",
                "source_pressure_group_key_hash",
                "source_evidence_refs",
                "files_or_modules_to_inspect",
                "expected_acceptance_gates",
                "forbidden_scope",
                "terminal_rule",
            ],
            "forbidden_outputs": ["repair_command", "source_mutation"],
            "terminal_rule": "human may authorize repair unit",
        },
        {
            "from_state": "HANDLE_HEALTHY_EXPECTED_PRESSURE",
            "condition": "group accepted as healthy expected pressure",
            "to_state": "MOVE_TO_NEXT_PRESSURE_GROUP",
            "required_outputs": [
                "accepted_pressure_group_key_hash",
                "acceptance_reason",
                "skip_recommendation",
                "next_group_rank_to_inspect",
            ],
            "forbidden_outputs": ["next_group_auto_open_without_permission", "repair_command"],
            "terminal_rule": "default STOP_HUMAN_DECISION_REQUIRED unless loop continuation explicitly permitted",
        },
        {
            "from_state": "HANDLE_NOT_ENOUGH_EVIDENCE",
            "condition": "missing evidence class emitted",
            "to_state": "STOP_HUMAN_DECISION_REQUIRED",
            "required_outputs": [
                "evidence_request_id",
                "source_pressure_group_key_hash",
                "evidence_sufficiency_class",
                "missing_evidence_reason",
                "requested_artifacts",
                "forbidden_scope",
                "terminal_rule",
            ],
            "forbidden_outputs": ["repair_proposal", "repair_command"],
            "terminal_rule": "human may authorize evidence unit",
        },
        {
            "from_state": "RERUN_AFTER_HANDLING",
            "condition": "accepted repair, accepted skip, or evidence update completed",
            "to_state": "CHECK_PRESSURE_RESOLUTION",
            "required_outputs": [
                "source_handling_receipt_id",
                "rerun_receipt_id",
                "same_lens_or_changed_lens",
                "pressure_group_before",
                "pressure_group_after",
                "pressure_delta",
            ],
            "forbidden_outputs": ["skip_resolution_check"],
            "terminal_rule": "continue loop",
        },
        {
            "from_state": "CHECK_PRESSURE_RESOLUTION",
            "condition": "PRESSURE_GONE",
            "to_state": "MOVE_TO_NEXT_PRESSURE_GROUP",
            "required_outputs": ["resolution_class", "pressure_delta"],
            "forbidden_outputs": ["repair_command"],
            "terminal_rule": "continue loop",
        },
        {
            "from_state": "CHECK_PRESSURE_RESOLUTION",
            "condition": "PRESSURE_REDUCED",
            "to_state": "MOVE_TO_NEXT_PRESSURE_GROUP_OR_STOP_HUMAN_DECISION_REQUIRED",
            "required_outputs": ["resolution_class", "pressure_delta", "human_rule"],
            "forbidden_outputs": ["automatic_repair"],
            "terminal_rule": "human rule decides continuation",
        },
        {
            "from_state": "CHECK_PRESSURE_RESOLUTION",
            "condition": "PRESSURE_UNCHANGED",
            "to_state": "INSPECT_PRESSURE_GROUP",
            "required_outputs": ["resolution_class", "pressure_delta"],
            "forbidden_outputs": ["pretend_resolved"],
            "terminal_rule": "continue investigation",
        },
        {
            "from_state": "CHECK_PRESSURE_RESOLUTION",
            "condition": "PRESSURE_WORSENED",
            "to_state": "STOP_HUMAN_DECISION_REQUIRED",
            "required_outputs": ["resolution_class", "pressure_delta"],
            "forbidden_outputs": ["auto_continue"],
            "terminal_rule": "STOP_HUMAN_DECISION_REQUIRED",
        },
        {
            "from_state": "CHECK_PRESSURE_RESOLUTION",
            "condition": "PRESSURE_SHIFTED",
            "to_state": "DETECT_PRESSURE",
            "required_outputs": ["resolution_class", "pressure_delta"],
            "forbidden_outputs": ["stale_group_selection"],
            "terminal_rule": "redetect pressure",
        },
        {
            "from_state": "MOVE_TO_NEXT_PRESSURE_GROUP",
            "condition": "another actionable group exists",
            "to_state": "SELECT_PRESSURE_GROUP",
            "required_outputs": ["next_actionable_group_key_hash"],
            "forbidden_outputs": ["auto_repair"],
            "terminal_rule": "only if loop continuation explicitly permitted",
        },
        {
            "from_state": "MOVE_TO_NEXT_PRESSURE_GROUP",
            "condition": "no actionable group exists",
            "to_state": "PROCEED_TO_NEXT_OBJECTIVE",
            "required_outputs": [
                "pressure_handling_complete:true",
                "remaining_actionable_pressure_groups:0",
                "next_objective_allowed:true",
            ],
            "forbidden_outputs": ["advance_without_next_objective_id"],
            "terminal_rule": "ADVANCE only if parent objective runner supplies next objective id else STOP_HUMAN_DECISION_REQUIRED",
        },
    ]

    first_application_target = {
        "next_unit_id": EXPECTED_NEXT_UNIT,
        "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "top_group_key_hash": top["top_group_summary"]["top_group_key_hash"],
        "classification": top["top_group_summary"]["classification"],
        "parent_pressure_class": top["top_group_summary"]["parent_pressure_class"],
        "pressure_subtype": top["top_group_summary"]["pressure_subtype"],
        "halt_reason": top["top_group_summary"]["halt_reason"],
        "top_group_count": top["top_group_summary"]["top_group_count"],
        "handling_state": "HANDLE_NOT_ENOUGH_EVIDENCE",
        "next_handling": [
            "request_or_gather_more_evidence",
            "repeat_inspection",
            "classify_when_evidence_is_sufficient",
        ],
        "must_not_repair_taxonomy": True,
    }

    protocol = {
        "schema_version": "pressure_handling_loop_protocol_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "human_decision": HUMAN_DECISION,
        "core_law": [
            "Pressure does not authorize action.",
            "Pressure authorizes inspection.",
            "Inspection plus enough evidence authorizes classification.",
            "Stable rank authorizes inspection order.",
            "Stable rank does not authorize repair.",
            "No repair is executed without an explicit repair unit.",
            "No taxonomy upgrade, authority widening, optimization, or extraction repair is allowed from pressure alone.",
        ],
        "states": STATES,
        "classifications": CLASSIFICATIONS,
        "evidence_sufficiency_classes": EVIDENCE_CLASSES,
        "resolution_classes": RESOLUTION_CLASSES,
        "pressure_group_fields": PRESSURE_GROUP_FIELDS,
        "transitions": transitions,
        "schemas": {
            "state_schema": rel(STATE_SCHEMA_PATH),
            "group_schema": rel(GROUP_SCHEMA_PATH),
            "classification_schema": rel(CLASSIFICATION_SCHEMA_PATH),
            "evidence_sufficiency_schema": rel(EVIDENCE_SCHEMA_PATH),
            "transition_schema": rel(TRANSITION_SCHEMA_PATH),
            "resolution_schema": rel(RESOLUTION_SCHEMA_PATH),
        },
        "first_application_target": first_application_target,
        "must_not_infer": MUST_NOT_INFER,
        "repair_executed": False,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "extraction_repair_authorized": False,
        "ranked_protocol_globally_adopted": False,
        "next_group_auto_opened": False,
        "source_mutation": False,
        "review_only": False,
    }
    return protocol

def build_report(protocol: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "pressure_handling_loop_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_receipts": {
            "source_r1000_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
            "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
            "source_candidate_c_interrogation_receipt_id": SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID,
            "source_coarsening_review_receipt_id": SOURCE_COARSENING_REVIEW_RECEIPT_ID,
            "source_pressure_metrics_repair_receipt_id": SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID,
        },
        "protocol_state_count": len(protocol["states"]),
        "transition_count": len(protocol["transitions"]),
        "classification_count": len(protocol["classifications"]),
        "evidence_sufficiency_class_count": len(protocol["evidence_sufficiency_classes"]),
        "resolution_class_count": len(protocol["resolution_classes"]),
        "first_application_target": protocol["first_application_target"],
        "summary": "Pressure handling loop protocol emitted with state machine, transition rules, classification rules, evidence sufficiency rules, resolution rules, and first application target.",
        "action_executed": False,
        "repair_executed": False,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "extraction_repair_authorized": False,
        "ranked_protocol_globally_adopted": False,
        "next_group_auto_opened": False,
        "hidden_next_command": False,
    }

def build_decision_packet(protocol: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "pressure_handling_loop_decision_packet_v0",
        "packet_type": "PROTOCOL_BUILD_ADVANCE_PACKET",
        "source_unit_id": UNIT_ID,
        "decision": "advance_to_first_application_unit",
        "next_unit_id": EXPECTED_NEXT_UNIT,
        "first_application_target": protocol["first_application_target"],
        "allowed_human_choices": [
            "ADVANCE_TO_FIRST_APPLICATION_UNIT",
            "REVIEW_PROTOCOL_BEFORE_APPLICATION",
            "REJECT_PRESSURE_HANDLING_LOOP_PROTOCOL",
        ],
        "may_emit_repair_command": False,
        "may_execute_repair": False,
        "may_authorize_taxonomy_upgrade": False,
        "may_authorize_authority_widening": False,
        "may_authorize_optimization": False,
        "may_authorize_extraction_repair": False,
        "may_auto_open_next_group": False,
        "may_advance_without_next_unit_id": False,
    }

def validate_protocol(protocol: Dict[str, Any], report: Dict[str, Any], packet: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if protocol.get("unit_id") != UNIT_ID:
        failures.append("protocol_unit_wrong")
    if protocol.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("protocol_target_wrong")
    for state in STATES:
        if state not in protocol.get("states", []):
            failures.append(f"state_missing:{state}")
    for cls in CLASSIFICATIONS:
        if cls not in protocol.get("classifications", []):
            failures.append(f"classification_missing:{cls}")
    for cls in EVIDENCE_CLASSES:
        if cls not in protocol.get("evidence_sufficiency_classes", []):
            failures.append(f"evidence_class_missing:{cls}")
    for cls in RESOLUTION_CLASSES:
        if cls not in protocol.get("resolution_classes", []):
            failures.append(f"resolution_class_missing:{cls}")
    for field in PRESSURE_GROUP_FIELDS:
        if field not in protocol.get("pressure_group_fields", []):
            failures.append(f"pressure_group_field_missing:{field}")

    transition_pairs = {(t["from_state"], t["condition"], t["to_state"]) for t in protocol.get("transitions", [])}
    required_transition_checks = {
        "no_pressure_to_next_objective": ("RUN_OBJECTIVE", "no pressure", "PROCEED_TO_NEXT_OBJECTIVE"),
        "pressure_to_detection": ("RUN_OBJECTIVE", "pressure found", "DETECT_PRESSURE"),
        "pressure_to_inspection": ("SELECT_PRESSURE_GROUP", "actionable group exists", "INSPECT_PRESSURE_GROUP"),
        "evidence_sufficient_to_classification": ("CHECK_EVIDENCE_SUFFICIENCY", "evidence sufficient", "CLASSIFY_PRESSURE_GROUP"),
        "evidence_insufficient_to_request": ("CHECK_EVIDENCE_SUFFICIENCY", "evidence insufficient", "HANDLE_NOT_ENOUGH_EVIDENCE"),
        "fixable_to_proposal": ("CLASSIFY_PRESSURE_GROUP", "FIXABLE_PRESSURE", "HANDLE_FIXABLE_PRESSURE"),
        "healthy_to_skip": ("CLASSIFY_PRESSURE_GROUP", "HEALTHY_EXPECTED_PRESSURE", "HANDLE_HEALTHY_EXPECTED_PRESSURE"),
        "not_enough_to_evidence_request": ("CLASSIFY_PRESSURE_GROUP", "NOT_ENOUGH_EVIDENCE", "HANDLE_NOT_ENOUGH_EVIDENCE"),
        "rerun_after_handling": ("RERUN_AFTER_HANDLING", "accepted repair, accepted skip, or evidence update completed", "CHECK_PRESSURE_RESOLUTION"),
        "pressure_gone_to_next_group": ("CHECK_PRESSURE_RESOLUTION", "PRESSURE_GONE", "MOVE_TO_NEXT_PRESSURE_GROUP"),
        "no_actionable_to_next_objective": ("MOVE_TO_NEXT_PRESSURE_GROUP", "no actionable group exists", "PROCEED_TO_NEXT_OBJECTIVE"),
    }
    for name, triple in required_transition_checks.items():
        if triple not in transition_pairs:
            failures.append(f"required_transition_missing:{name}:{triple}")

    for transition in protocol.get("transitions", []):
        forbidden = transition.get("forbidden_outputs", [])
        if transition["from_state"] in {"HANDLE_FIXABLE_PRESSURE", "HANDLE_NOT_ENOUGH_EVIDENCE"} and "repair_command" not in forbidden:
            failures.append(f"repair_command_not_forbidden:{transition['from_state']}:{transition['condition']}")
        if transition["from_state"] == "MOVE_TO_NEXT_PRESSURE_GROUP" and transition["condition"] == "another actionable group exists":
            if "auto_repair" not in forbidden:
                failures.append("next_group_transition_missing_auto_repair_forbidden")

    target = protocol.get("first_application_target", {})
    if target.get("next_unit_id") != EXPECTED_NEXT_UNIT:
        failures.append("first_application_next_unit_wrong")
    if target.get("source_top_group_classification_receipt_id") != SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID:
        failures.append("first_application_source_wrong")
    if target.get("top_group_key_hash") != "38c604a1":
        failures.append("first_application_top_group_wrong")
    if target.get("classification") != "NOT_ENOUGH_EVIDENCE":
        failures.append("first_application_classification_wrong")
    if target.get("parent_pressure_class") != "TAXONOMY_PRESSURE":
        failures.append("first_application_parent_wrong")
    if target.get("pressure_subtype") != "missing_label":
        failures.append("first_application_subtype_wrong")
    if target.get("halt_reason") != "STOP_TAXONOMY_GAP":
        failures.append("first_application_halt_wrong")
    if target.get("must_not_repair_taxonomy") is not True:
        failures.append("first_application_must_not_repair_taxonomy_missing")

    for key in [
        "repair_executed",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "optimization_authorized",
        "extraction_repair_authorized",
        "ranked_protocol_globally_adopted",
        "next_group_auto_opened",
        "source_mutation",
    ]:
        if protocol.get(key) is not False:
            failures.append(f"protocol_guard_not_false:{key}:{protocol.get(key)}")

    for key in [
        "action_executed",
        "repair_executed",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "optimization_authorized",
        "extraction_repair_authorized",
        "ranked_protocol_globally_adopted",
        "next_group_auto_opened",
        "hidden_next_command",
    ]:
        if report.get(key) is not False:
            failures.append(f"report_guard_not_false:{key}:{report.get(key)}")

    if packet.get("packet_type") != "PROTOCOL_BUILD_ADVANCE_PACKET":
        failures.append("packet_type_wrong")
    if packet.get("next_unit_id") != EXPECTED_NEXT_UNIT:
        failures.append("packet_next_unit_wrong")
    for key in [
        "may_emit_repair_command",
        "may_execute_repair",
        "may_authorize_taxonomy_upgrade",
        "may_authorize_authority_widening",
        "may_authorize_optimization",
        "may_authorize_extraction_repair",
        "may_auto_open_next_group",
        "may_advance_without_next_unit_id",
    ]:
        if packet.get(key) is not False:
            failures.append(f"packet_guard_not_false:{key}:{packet.get(key)}")

    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    if receipt.get("source_r1000_top_group_classification_receipt_id") != SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID:
        failures.append("source_top_group_wrong")
    if receipt.get("expected_next_unit_on_success") != EXPECTED_NEXT_UNIT:
        failures.append("expected_next_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "PRESSURE_LOOP_0_SOURCE_SURFACE_VERIFIED",
        "PRESSURE_LOOP_1_HUMAN_PROTOCOL_DECISION_RECORDED",
        "PRESSURE_LOOP_2_STATE_MACHINE_EMITTED",
        "PRESSURE_LOOP_3_TRANSITION_RULES_EMITTED",
        "PRESSURE_LOOP_4_PRESSURE_GROUP_SCHEMA_EMITTED",
        "PRESSURE_LOOP_5_CLASSIFICATION_SCHEMA_EMITTED",
        "PRESSURE_LOOP_6_EVIDENCE_SUFFICIENCY_SCHEMA_EMITTED",
        "PRESSURE_LOOP_7_RESOLUTION_SCHEMA_EMITTED",
        "PRESSURE_LOOP_8_NO_PRESSURE_TO_NEXT_OBJECTIVE_RULE_EMITTED",
        "PRESSURE_LOOP_9_PRESSURE_TO_INSPECTION_RULE_EMITTED",
        "PRESSURE_LOOP_10_EVIDENCE_SUFFICIENCY_RULE_EMITTED",
        "PRESSURE_LOOP_11_CLASSIFICATION_RULE_EMITTED",
        "PRESSURE_LOOP_12_FIXABLE_TO_REPAIR_PROPOSAL_ONLY_RULE_EMITTED",
        "PRESSURE_LOOP_13_HEALTHY_TO_ACCEPT_SKIP_RULE_EMITTED",
        "PRESSURE_LOOP_14_NOT_ENOUGH_EVIDENCE_TO_EVIDENCE_REQUEST_RULE_EMITTED",
        "PRESSURE_LOOP_15_RERUN_AFTER_HANDLING_RULE_EMITTED",
        "PRESSURE_LOOP_16_PRESSURE_GONE_TO_NEXT_GROUP_RULE_EMITTED",
        "PRESSURE_LOOP_17_NO_ACTIONABLE_GROUPS_TO_NEXT_OBJECTIVE_RULE_EMITTED",
        "PRESSURE_LOOP_18_FIRST_APPLICATION_TARGET_EMITTED",
        "PRESSURE_LOOP_19_NO_ACTION_EXECUTED",
        "PRESSURE_LOOP_20_NO_SOURCE_MUTATION",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    for key in [
        "action_executed_count",
        "repair_executed_count",
        "repair_command_emitted_count",
        "taxonomy_upgrade_authorized_count",
        "authority_widening_authorized_count",
        "optimization_authorized_count",
        "extraction_repair_authorized_count",
        "ranked_protocol_globally_adopted_count",
        "next_group_auto_opened_count",
        "next_objective_without_supplied_id_count",
        "source_mutation_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")
    if metrics.get("state_count") != len(STATES):
        failures.append("state_count_wrong")
    if metrics.get("classification_count") != len(CLASSIFICATIONS):
        failures.append("classification_count_wrong")
    if metrics.get("evidence_sufficiency_class_count") != len(EVIDENCE_CLASSES):
        failures.append("evidence_count_wrong")
    if metrics.get("resolution_class_count") != len(RESOLUTION_CLASSES):
        failures.append("resolution_count_wrong")
    if metrics.get("first_application_target") != EXPECTED_NEXT_UNIT:
        failures.append("first_application_metric_wrong")

    guards = receipt.get("pressure_loop_guards", {})
    for key in [
        "source_surface_verified",
        "human_protocol_decision_recorded",
        "state_machine_emitted",
        "transition_rules_emitted",
        "pressure_group_schema_emitted",
        "classification_schema_emitted",
        "evidence_sufficiency_schema_emitted",
        "resolution_schema_emitted",
        "first_application_target_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "action_executed",
        "repair_executed",
        "repair_command_emitted",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "optimization_authorized",
        "extraction_repair_authorized",
        "ranked_protocol_globally_adopted",
        "next_group_auto_opened",
        "next_objective_without_supplied_id",
        "source_mutation",
        "hidden_next_command",
    ]:
        if guards.get(key) is not False:
            failures.append(f"guard_not_false:{key}:{guards.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "ADVANCE":
        failures.append(f"terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != EXPECTED_NEXT_UNIT:
        failures.append(f"terminal_next_wrong:{terminal}")
    if terminal.get("stop_code") is not None:
        failures.append(f"terminal_stop_not_null:{terminal}")

    return failures

def main() -> int:
    source_before = snapshot_files(SOURCE_FILES)
    sources = load_sources()
    failures: List[str] = validate_sources(sources)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    schemas = build_schemas()
    protocol = build_protocol(sources, schemas)
    report = build_report(protocol)
    packet = build_decision_packet(protocol)

    write_json(STATE_SCHEMA_PATH, schemas["state_schema"])
    write_json(GROUP_SCHEMA_PATH, schemas["group_schema"])
    write_json(CLASSIFICATION_SCHEMA_PATH, schemas["classification_schema"])
    write_json(EVIDENCE_SCHEMA_PATH, schemas["evidence_schema"])
    write_json(TRANSITION_SCHEMA_PATH, schemas["transition_schema"])
    write_json(RESOLUTION_SCHEMA_PATH, schemas["resolution_schema"])
    write_json(PROTOCOL_PATH, protocol)
    write_json(REPORT_PATH, report)
    write_json(DECISION_PACKET_PATH, packet)

    failures.extend(validate_protocol(protocol, report, packet))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    transition_pairs = {(t["from_state"], t["condition"], t["to_state"]) for t in protocol["transitions"]}

    acceptance_gate_results = {
        "PRESSURE_LOOP_0_SOURCE_SURFACE_VERIFIED": len(validate_sources(sources)) == 0,
        "PRESSURE_LOOP_1_HUMAN_PROTOCOL_DECISION_RECORDED": HUMAN_DECISION["decision"] == "BUILD_FIXED_LOCAL_PRESSURE_HANDLING_LOOP_PROTOCOL",
        "PRESSURE_LOOP_2_STATE_MACHINE_EMITTED": STATE_SCHEMA_PATH.exists() and set(STATES).issubset(set(protocol["states"])),
        "PRESSURE_LOOP_3_TRANSITION_RULES_EMITTED": TRANSITION_SCHEMA_PATH.exists() and len(protocol["transitions"]) >= 20,
        "PRESSURE_LOOP_4_PRESSURE_GROUP_SCHEMA_EMITTED": GROUP_SCHEMA_PATH.exists(),
        "PRESSURE_LOOP_5_CLASSIFICATION_SCHEMA_EMITTED": CLASSIFICATION_SCHEMA_PATH.exists(),
        "PRESSURE_LOOP_6_EVIDENCE_SUFFICIENCY_SCHEMA_EMITTED": EVIDENCE_SCHEMA_PATH.exists(),
        "PRESSURE_LOOP_7_RESOLUTION_SCHEMA_EMITTED": RESOLUTION_SCHEMA_PATH.exists(),
        "PRESSURE_LOOP_8_NO_PRESSURE_TO_NEXT_OBJECTIVE_RULE_EMITTED": ("RUN_OBJECTIVE", "no pressure", "PROCEED_TO_NEXT_OBJECTIVE") in transition_pairs,
        "PRESSURE_LOOP_9_PRESSURE_TO_INSPECTION_RULE_EMITTED": ("SELECT_PRESSURE_GROUP", "actionable group exists", "INSPECT_PRESSURE_GROUP") in transition_pairs,
        "PRESSURE_LOOP_10_EVIDENCE_SUFFICIENCY_RULE_EMITTED": ("CHECK_EVIDENCE_SUFFICIENCY", "evidence sufficient", "CLASSIFY_PRESSURE_GROUP") in transition_pairs and ("CHECK_EVIDENCE_SUFFICIENCY", "evidence insufficient", "HANDLE_NOT_ENOUGH_EVIDENCE") in transition_pairs,
        "PRESSURE_LOOP_11_CLASSIFICATION_RULE_EMITTED": all(cls in protocol["classifications"] for cls in CLASSIFICATIONS),
        "PRESSURE_LOOP_12_FIXABLE_TO_REPAIR_PROPOSAL_ONLY_RULE_EMITTED": ("CLASSIFY_PRESSURE_GROUP", "FIXABLE_PRESSURE", "HANDLE_FIXABLE_PRESSURE") in transition_pairs,
        "PRESSURE_LOOP_13_HEALTHY_TO_ACCEPT_SKIP_RULE_EMITTED": ("CLASSIFY_PRESSURE_GROUP", "HEALTHY_EXPECTED_PRESSURE", "HANDLE_HEALTHY_EXPECTED_PRESSURE") in transition_pairs,
        "PRESSURE_LOOP_14_NOT_ENOUGH_EVIDENCE_TO_EVIDENCE_REQUEST_RULE_EMITTED": ("CLASSIFY_PRESSURE_GROUP", "NOT_ENOUGH_EVIDENCE", "HANDLE_NOT_ENOUGH_EVIDENCE") in transition_pairs,
        "PRESSURE_LOOP_15_RERUN_AFTER_HANDLING_RULE_EMITTED": ("RERUN_AFTER_HANDLING", "accepted repair, accepted skip, or evidence update completed", "CHECK_PRESSURE_RESOLUTION") in transition_pairs,
        "PRESSURE_LOOP_16_PRESSURE_GONE_TO_NEXT_GROUP_RULE_EMITTED": ("CHECK_PRESSURE_RESOLUTION", "PRESSURE_GONE", "MOVE_TO_NEXT_PRESSURE_GROUP") in transition_pairs,
        "PRESSURE_LOOP_17_NO_ACTIONABLE_GROUPS_TO_NEXT_OBJECTIVE_RULE_EMITTED": ("MOVE_TO_NEXT_PRESSURE_GROUP", "no actionable group exists", "PROCEED_TO_NEXT_OBJECTIVE") in transition_pairs,
        "PRESSURE_LOOP_18_FIRST_APPLICATION_TARGET_EMITTED": protocol["first_application_target"]["next_unit_id"] == EXPECTED_NEXT_UNIT,
        "PRESSURE_LOOP_19_NO_ACTION_EXECUTED": report["action_executed"] is False and report["repair_executed"] is False,
        "PRESSURE_LOOP_20_NO_SOURCE_MUTATION": source_mutation_detected is False,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "ADVANCE",
        "next_command_goal": EXPECTED_NEXT_UNIT,
        "stop_code": None,
    }
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}
    if any([
        protocol["repair_executed"],
        protocol["taxonomy_upgrade_authorized"],
        protocol["authority_widening_authorized"],
        protocol["optimization_authorized"],
        protocol["extraction_repair_authorized"],
    ]):
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}
    if not all([
        STATE_SCHEMA_PATH.exists(),
        GROUP_SCHEMA_PATH.exists(),
        CLASSIFICATION_SCHEMA_PATH.exists(),
        EVIDENCE_SCHEMA_PATH.exists(),
        TRANSITION_SCHEMA_PATH.exists(),
        RESOLUTION_SCHEMA_PATH.exists(),
        PROTOCOL_PATH.exists(),
    ]):
        terminal = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}

    aggregate_metrics = {
        "state_count": len(protocol["states"]),
        "transition_count": len(protocol["transitions"]),
        "classification_count": len(protocol["classifications"]),
        "evidence_sufficiency_class_count": len(protocol["evidence_sufficiency_classes"]),
        "resolution_class_count": len(protocol["resolution_classes"]),
        "pressure_group_field_count": len(protocol["pressure_group_fields"]),
        "first_application_target": EXPECTED_NEXT_UNIT,
        "source_top_group_key_hash": protocol["first_application_target"]["top_group_key_hash"],
        "source_top_group_classification": protocol["first_application_target"]["classification"],
        "action_executed_count": 0,
        "repair_executed_count": 0,
        "repair_command_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "authority_widening_authorized_count": 0,
        "optimization_authorized_count": 0,
        "extraction_repair_authorized_count": 0,
        "ranked_protocol_globally_adopted_count": 0,
        "next_group_auto_opened_count": 0,
        "next_objective_without_supplied_id_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "hidden_next_command_count": 0,
    }

    guards = {
        "source_surface_verified": len(validate_sources(sources)) == 0,
        "human_protocol_decision_recorded": True,
        "state_machine_emitted": STATE_SCHEMA_PATH.exists(),
        "transition_rules_emitted": TRANSITION_SCHEMA_PATH.exists(),
        "pressure_group_schema_emitted": GROUP_SCHEMA_PATH.exists(),
        "classification_schema_emitted": CLASSIFICATION_SCHEMA_PATH.exists(),
        "evidence_sufficiency_schema_emitted": EVIDENCE_SCHEMA_PATH.exists(),
        "resolution_schema_emitted": RESOLUTION_SCHEMA_PATH.exists(),
        "first_application_target_emitted": protocol["first_application_target"]["next_unit_id"] == EXPECTED_NEXT_UNIT,
        "action_executed": False,
        "repair_executed": False,
        "repair_command_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "extraction_repair_authorized": False,
        "ranked_protocol_globally_adopted": False,
        "next_group_auto_opened": False,
        "next_objective_without_supplied_id": False,
        "source_mutation": source_mutation_detected,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_top_group_receipt": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "first_application_target": EXPECTED_NEXT_UNIT,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "pressure_handling_state_schema": rel(STATE_SCHEMA_PATH),
        "pressure_group_schema": rel(GROUP_SCHEMA_PATH),
        "pressure_classification_schema": rel(CLASSIFICATION_SCHEMA_PATH),
        "pressure_evidence_sufficiency_schema": rel(EVIDENCE_SCHEMA_PATH),
        "pressure_handling_transition_schema": rel(TRANSITION_SCHEMA_PATH),
        "pressure_resolution_schema": rel(RESOLUTION_SCHEMA_PATH),
        "pressure_handling_loop_protocol": rel(PROTOCOL_PATH),
        "pressure_handling_loop_report": rel(REPORT_PATH),
        "pressure_handling_loop_decision_packet": rel(DECISION_PACKET_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "pressure_handling_loop_protocol_receipt_v0",
        "receipt_type": "PRESSURE_HANDLING_LOOP_PROTOCOL_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_r1000_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        "source_candidate_c_interrogation_receipt_id": SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID,
        "source_coarsening_review_receipt_id": SOURCE_COARSENING_REVIEW_RECEIPT_ID,
        "source_pressure_metrics_repair_receipt_id": SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID,
        "expected_next_unit_on_success": EXPECTED_NEXT_UNIT,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "first_application_target": protocol["first_application_target"],
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "pressure_loop_guards": guards,
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
    print(f"pressure_handling_loop_protocol_receipt_id={receipt_id}")
    print(f"pressure_handling_loop_protocol_receipt_path=data/pressure_handling_loop_protocol_v0_receipts/{receipt_id}.json")
    print(f"pressure_handling_loop_protocol_path=data/pressure_handling_loop_protocol_v0/pressure_handling_loop_protocol.json")
    print(f"pressure_handling_loop_decision_packet_path=data/pressure_handling_loop_protocol_v0/pressure_handling_loop_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
