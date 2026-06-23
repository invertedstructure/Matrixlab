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

UNIT_ID = "MARK_CANDIDATE_PROPOSAL_REVIEW_AS_STRUCTURAL_ONLY_AND_REQUIRE_IN_CHAT_SEMANTIC_REVIEW_V0"
TARGET_UNIT_ID = "candidate_proposal_semantic_review_barrier.r1000_taxonomy_gap.v0"

SOURCE_PROPOSAL_REVIEW_RECEIPT_ID = "a939b4a6"
SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID = "aa01c2a9"
SOURCE_PROPOSAL_LAYER_RECEIPT_ID = "6003c89c"
SOURCE_EXPECTED_LIMIT_RECEIPT_ID = "cbde4b69"
CANDIDATE_OBJECT_ID = "ce1fe7fc"

OUT_DIR = ROOT / "data" / "candidate_proposal_semantic_review_barrier_r1000_taxonomy_gap_v0"
RECEIPT_DIR = ROOT / "data" / "candidate_proposal_semantic_review_barrier_r1000_taxonomy_gap_v0_receipts"

STRUCTURAL_ONLY_RECLASSIFICATION_PATH = OUT_DIR / "candidate_review_structural_only_reclassification.json"
IN_CHAT_SEMANTIC_REVIEW_REQUEST_PATH = OUT_DIR / "in_chat_semantic_review_request.json"
SEMANTIC_REVIEW_CHECKLIST_PATH = OUT_DIR / "candidate_semantic_review_checklist.json"
APPLICATION_BLOCKER_PACKET_PATH = OUT_DIR / "candidate_application_blocker_packet.json"
BARRIER_TRANSITION_TRACE_PATH = OUT_DIR / "semantic_review_barrier_transition_trace.json"
BARRIER_REPORT_PATH = OUT_DIR / "semantic_review_barrier_report.json"

PROPOSAL_REVIEW_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_review_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_PROPOSAL_REVIEW_RECEIPT_ID}.json"
PROPOSAL_REVIEW_DECISION_PATH = ROOT / "data" / "candidate_missing_object_proposal_review_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_candidate_proposal_review_decision.json"
PROPOSAL_REVIEW_FINDINGS_PATH = ROOT / "data" / "candidate_missing_object_proposal_review_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_candidate_proposal_review_findings.json"
PROPOSAL_REVIEW_AUTHORIZATION_PACKET_PATH = ROOT / "data" / "candidate_missing_object_proposal_review_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_candidate_proposal_application_authorization_packet.json"
PROPOSAL_REVIEW_REPORT_PATH = ROOT / "data" / "candidate_missing_object_proposal_review_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_candidate_proposal_review_report.json"

PROPOSAL_APPLICATION_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID}.json"
CANDIDATE_PROPOSAL_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_candidate_missing_object_proposal.json"
TYPED_DECISION_FIELDS_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_typed_unresolved_decision_fields.jsonl"
PROPOSAL_EVIDENCE_REFS_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_proposal_evidence_refs.json"
HUMAN_SCHEMA_DECISION_PACKET_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_human_schema_decision_packet.json"

PROPOSAL_LAYER_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0_receipts" / f"{SOURCE_PROPOSAL_LAYER_RECEIPT_ID}.json"
PROPOSAL_LAYER_CONTRACT_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "candidate_missing_object_proposal_layer_contract.json"
PROPOSAL_APPLICATION_CONTRACT_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "candidate_proposal_application_contract.json"

EXPECTED_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0_receipts" / f"{SOURCE_EXPECTED_LIMIT_RECEIPT_ID}.json"

SOURCE_FILES = [
    PROPOSAL_REVIEW_RECEIPT_PATH,
    PROPOSAL_REVIEW_DECISION_PATH,
    PROPOSAL_REVIEW_FINDINGS_PATH,
    PROPOSAL_REVIEW_AUTHORIZATION_PACKET_PATH,
    PROPOSAL_REVIEW_REPORT_PATH,
    PROPOSAL_APPLICATION_RECEIPT_PATH,
    CANDIDATE_PROPOSAL_PATH,
    TYPED_DECISION_FIELDS_PATH,
    PROPOSAL_EVIDENCE_REFS_PATH,
    HUMAN_SCHEMA_DECISION_PACKET_PATH,
    PROPOSAL_LAYER_RECEIPT_PATH,
    PROPOSAL_LAYER_CONTRACT_PATH,
    PROPOSAL_APPLICATION_CONTRACT_PATH,
    EXPECTED_LIMIT_RECEIPT_PATH,
]

SEMANTIC_REVIEW_CLASSES = [
    "STRUCTURALLY_VALID_SEMANTICALLY_SOUND",
    "STRUCTURALLY_VALID_SEMANTICALLY_UNSOUND",
    "TOO_UNDERTYPED_TO_REVIEW_STABLY",
    "MISSING_EVIDENCE_FOR_SEMANTIC_REVIEW",
    "ACCEPTABLE_ONLY_AFTER_EDITS",
    "ACCEPTABLE_FOR_SEPARATE_APPLICATION",
]

REQUIRED_REVIEW_SURFACES = [
    "proposed candidate values or fields",
    "evidence basis",
    "unresolved typed fields",
    "assumptions",
    "uncertainty reasons",
    "alternatives",
    "risk if wrong",
    "whether it sneaks in correctness claims",
    "whether it implies authorization",
    "whether it crosses taxonomy/application/source-mutation boundaries",
]

FORBIDDEN_IN_THIS_UNIT = [
    "semantic acceptance",
    "application authorization after semantic barrier",
    "proposal application",
    "target field filling",
    "null field value emission",
    "value invention",
    "taxonomy label creation",
    "taxonomy upgrade",
    "taxonomy delta proposal",
    "source mutation",
    "existing receipt mutation",
    "R1000 run",
    "pressure group opening",
    "hidden next command",
]

HUMAN_DECISION = {
    "decision": "MARK_CANDIDATE_PROPOSAL_REVIEW_AS_STRUCTURAL_ONLY_AND_REQUIRE_IN_CHAT_SEMANTIC_REVIEW",
    "scope": "reinterpret the previous machine/unit proposal review as structural admissibility only and require in-chat semantic review before any application authorization",
    "source_proposal_review_receipt_id": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
    "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
    "candidate_object_id": CANDIDATE_OBJECT_ID,
    "authorized": [
        "consume previous proposal review receipt",
        "classify previous review as structural-only",
        "emit in-chat semantic review request",
        "emit semantic review checklist",
        "emit application blocker packet",
        "block accepted application until explicit in-chat semantic review completes",
        "stop without hidden next command",
    ],
    "not_authorized": [
        "semantically accepting the candidate",
        "semantically rejecting the candidate",
        "editing the candidate",
        "applying the candidate",
        "authorizing application after this barrier",
        "filling missing descriptor fields",
        "inventing values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "mutating source rows",
        "mutating existing receipts",
        "running R1000",
        "opening another pressure group",
        "hiding next command",
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
    return path.relative_to(ROOT).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
    return json.loads(path.read_text())

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
    rows: List[Dict[str, Any]] = []
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
        "proposal_review_receipt": read_json(PROPOSAL_REVIEW_RECEIPT_PATH),
        "proposal_review_decision": read_json(PROPOSAL_REVIEW_DECISION_PATH),
        "proposal_review_findings": read_json(PROPOSAL_REVIEW_FINDINGS_PATH),
        "proposal_review_authorization_packet": read_json(PROPOSAL_REVIEW_AUTHORIZATION_PACKET_PATH),
        "proposal_review_report": read_json(PROPOSAL_REVIEW_REPORT_PATH),
        "proposal_application_receipt": read_json(PROPOSAL_APPLICATION_RECEIPT_PATH),
        "candidate_proposal": read_json(CANDIDATE_PROPOSAL_PATH),
        "typed_decision_fields": read_jsonl(TYPED_DECISION_FIELDS_PATH),
        "proposal_evidence_refs": read_json(PROPOSAL_EVIDENCE_REFS_PATH),
        "human_schema_decision_packet": read_json(HUMAN_SCHEMA_DECISION_PACKET_PATH),
        "proposal_layer_receipt": read_json(PROPOSAL_LAYER_RECEIPT_PATH),
        "proposal_layer_contract": read_json(PROPOSAL_LAYER_CONTRACT_PATH),
        "proposal_application_contract": read_json(PROPOSAL_APPLICATION_CONTRACT_PATH),
        "expected_limit_receipt": read_json(EXPECTED_LIMIT_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    review_receipt = sources["proposal_review_receipt"]
    review_decision = sources["proposal_review_decision"]
    authorization_packet = sources["proposal_review_authorization_packet"]
    candidate = sources["candidate_proposal"]
    app_receipt = sources["proposal_application_receipt"]
    layer_receipt = sources["proposal_layer_receipt"]

    if review_receipt.get("receipt_id") != SOURCE_PROPOSAL_REVIEW_RECEIPT_ID:
        failures.append("proposal_review_receipt_id_wrong")
    if review_receipt.get("gate") != "PASS":
        failures.append("proposal_review_not_pass")
    if review_receipt.get("aggregate_metrics", {}).get("review_decision_status") != "ACCEPT_CANDIDATE_OBJECT":
        failures.append("proposal_review_status_not_structural_accept")
    if review_receipt.get("aggregate_metrics", {}).get("application_authorized_in_this_unit_count") != 0:
        failures.append("previous_review_authorized_current_unit")
    if review_receipt.get("aggregate_metrics", {}).get("proposal_applied_count") != 0:
        failures.append("previous_review_applied_proposal")

    if review_decision.get("candidate_object_id") != CANDIDATE_OBJECT_ID:
        failures.append("review_decision_candidate_id_wrong")
    if review_decision.get("decision_status") != "ACCEPT_CANDIDATE_OBJECT":
        failures.append("review_decision_status_wrong")
    if review_decision.get("application_authorized_in_this_unit") is not False:
        failures.append("review_decision_authorized_current_unit")

    if authorization_packet.get("application_authorized_in_this_unit") is not False:
        failures.append("authorization_packet_authorized_current_unit")

    if candidate.get("candidate_object_id") != CANDIDATE_OBJECT_ID:
        failures.append("candidate_object_id_wrong")
    if candidate.get("object_status") != "CANDIDATE_MISSING_OBJECT_PROPOSAL":
        failures.append("candidate_status_wrong")
    if candidate.get("application_authorized") is not False:
        failures.append("candidate_self_authorizes_application")

    if app_receipt.get("receipt_id") != SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID:
        failures.append("proposal_application_receipt_id_wrong")
    if app_receipt.get("gate") != "PASS":
        failures.append("proposal_application_not_pass")
    if app_receipt.get("aggregate_metrics", {}).get("proposal_applied_count") != 0:
        failures.append("proposal_application_already_applied")

    if layer_receipt.get("receipt_id") != SOURCE_PROPOSAL_LAYER_RECEIPT_ID:
        failures.append("proposal_layer_receipt_id_wrong")
    if layer_receipt.get("gate") != "PASS":
        failures.append("proposal_layer_not_pass")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_structural_only_reclassification(sources: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "candidate_review_structural_only_reclassification_v0",
        "reclassification_id": sha8({
            "source_review_receipt_id": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
            "candidate_object_id": CANDIDATE_OBJECT_ID,
            "classification": "STRUCTURAL_ONLY_NOT_SEMANTIC_ACCEPTANCE",
        }),
        "candidate_object_id": CANDIDATE_OBJECT_ID,
        "source_proposal_review_receipt_id": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
        "source_review_decision_status": sources["proposal_review_receipt"]["aggregate_metrics"]["review_decision_status"],
        "previous_review_reclassified_as": "STRUCTURAL_ADMISSIBILITY_REVIEW_ONLY",
        "not_semantic_acceptance": True,
        "not_application_authorization_after_barrier": True,
        "reason": "machine/unit review validates candidate object shape, typed unresolved fields, evidence-ref presence, and boundary guards, but does not decide semantic soundness",
        "allowed_interpretation": [
            "candidate is structurally reviewable",
            "candidate may enter in-chat semantic review",
            "candidate may not be applied before explicit semantic acceptance",
        ],
        "forbidden_interpretation": [
            "candidate is semantically accepted",
            "candidate is correct",
            "candidate may be applied immediately",
            "candidate authorizes taxonomy or source mutation",
        ],
    }

def build_semantic_review_request() -> Dict[str, Any]:
    return {
        "schema_version": "in_chat_semantic_review_request_v0",
        "request_id": sha8({
            "candidate_object_id": CANDIDATE_OBJECT_ID,
            "review": "in_chat_semantic_review_required",
        }),
        "candidate_object_id": CANDIDATE_OBJECT_ID,
        "candidate_object_ref": rel(CANDIDATE_PROPOSAL_PATH),
        "semantic_review_required": True,
        "semantic_review_location": "chat",
        "semantic_review_classes": SEMANTIC_REVIEW_CLASSES,
        "must_inspect": REQUIRED_REVIEW_SURFACES,
        "decision_rules": {
            "clearly_unsound": "reject candidate or patch proposal capability before application",
            "too_undertyped": "refine proposal capability to emit more reviewable information",
            "missing_evidence": "request or produce only the minimum separate receipt needed for semantic review without mutation",
            "acceptable_after_edits": "emit edit requirements before application",
            "acceptable_for_separate_application": "requires explicit human/schema acceptance before application unit",
        },
        "semantic_review_must_not": [
            "apply the proposal",
            "fill descriptor fields",
            "invent values",
            "create taxonomy labels",
            "mutate source rows",
            "mutate existing receipts",
            "hide next command",
        ],
        "expected_terminal": {
            "type": "STOP",
            "stop_code": "STOP_IN_CHAT_SEMANTIC_REVIEW_REQUIRED_BEFORE_APPLICATION_AUTHORIZATION",
            "next_command_goal": None,
        },
    }

def build_semantic_review_checklist() -> Dict[str, Any]:
    return {
        "schema_version": "candidate_semantic_review_checklist_v0",
        "candidate_object_id": CANDIDATE_OBJECT_ID,
        "review_questions": [
            {
                "check": "proposed_candidate_values_or_fields",
                "question": "Are the proposed fields the right missing object surface, or are they overfitted/undertyped?",
            },
            {
                "check": "evidence_basis",
                "question": "Do the cited receipts support this candidate object, or only the existence of a structural gap?",
            },
            {
                "check": "unresolved_typed_fields",
                "question": "Are unresolved fields typed enough to review, or do they need provenance/source-role details?",
            },
            {
                "check": "assumptions",
                "question": "Does the candidate smuggle assumptions about missing label identity, taxonomy context, or label spaces?",
            },
            {
                "check": "uncertainty_reasons",
                "question": "Are uncertainty reasons explicit enough to explain why fields remain unresolved?",
            },
            {
                "check": "alternatives",
                "question": "Are there plausible alternative missing-object shapes, such as provenance descriptor, label-space descriptor, or evidence-source descriptor?",
            },
            {
                "check": "risk_if_wrong",
                "question": "Would accepting this object bias later taxonomy repair, collapse multiple gaps, or make false distinguishability claims?",
            },
            {
                "check": "correctness_claims",
                "question": "Does the candidate claim correctness, or only propose a reviewable object?",
            },
            {
                "check": "authorization_implication",
                "question": "Does any field imply application authorization or taxonomy authorization?",
            },
            {
                "check": "boundary_crossing",
                "question": "Does the candidate cross taxonomy/application/source-mutation boundaries?",
            },
        ],
        "allowed_outcomes": SEMANTIC_REVIEW_CLASSES,
    }

def build_application_blocker_packet(review_request: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "candidate_application_blocker_packet_v0",
        "blocker_packet_id": sha8({
            "candidate_object_id": CANDIDATE_OBJECT_ID,
            "blocked_unit": "APPLY_ACCEPTED_CANDIDATE_MISSING_OBJECT_PROPOSAL_TO_R1000_TOP_GROUP_TAXONOMY_GAP_EVIDENCE_SURFACE_V0",
        }),
        "candidate_object_id": CANDIDATE_OBJECT_ID,
        "blocked_application_unit": "APPLY_ACCEPTED_CANDIDATE_MISSING_OBJECT_PROPOSAL_TO_R1000_TOP_GROUP_TAXONOMY_GAP_EVIDENCE_SURFACE_V0",
        "blocked_until": "EXPLICIT_IN_CHAT_SEMANTIC_REVIEW_COMPLETED_AND_HUMAN_SCHEMA_ACCEPTANCE_RECORDED",
        "previous_authorization_reclassified": "STRUCTURAL_ONLY_CANDIDACY_NOT_SEMANTIC_APPLICATION_AUTHORIZATION",
        "application_authorization_after_barrier": False,
        "application_blocked": True,
        "semantic_review_request_ref": rel(IN_CHAT_SEMANTIC_REVIEW_REQUEST_PATH),
        "allowed_next_non_application_handling": [
            "perform in-chat semantic review",
            "reject candidate",
            "patch proposal capability",
            "request more evidence",
            "emit edited candidate proposal",
            "record explicit semantic acceptance for separate application",
        ],
        "forbidden_next_handling": [
            "apply candidate without semantic review",
            "treat structural review as semantic acceptance",
            "fill unresolved descriptor fields",
            "create taxonomy labels",
            "mutate source rows",
            "mutate existing receipts",
        ],
    }

def build_transition_trace() -> Dict[str, Any]:
    return {
        "schema_version": "candidate_proposal_semantic_review_barrier_transition_trace_v0",
        "candidate_object_id": CANDIDATE_OBJECT_ID,
        "trace": [
            {
                "step": "consume_machine_review",
                "question": "did machine review structurally accept candidate",
                "answer": True,
                "taken": "reclassify_as_structural_only",
            },
            {
                "step": "reclassify_as_structural_only",
                "question": "does structural acceptance equal semantic acceptance",
                "answer": False,
                "taken": "emit_in_chat_semantic_review_request",
            },
            {
                "step": "emit_in_chat_semantic_review_request",
                "question": "can application proceed before semantic review",
                "answer": False,
                "taken": "emit_application_blocker_packet",
            },
            {
                "step": "emit_application_blocker_packet",
                "question": "hidden next command allowed",
                "answer": False,
                "taken": "STOP_IN_CHAT_SEMANTIC_REVIEW_REQUIRED_BEFORE_APPLICATION_AUTHORIZATION",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_IN_CHAT_SEMANTIC_REVIEW_REQUIRED_BEFORE_APPLICATION_AUTHORIZATION",
            "next_command_goal": None,
        },
    }

def build_report() -> Dict[str, Any]:
    return {
        "schema_version": "candidate_proposal_semantic_review_barrier_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_proposal_review_receipt_id": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
        "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        "candidate_object_id": CANDIDATE_OBJECT_ID,
        "machine_review_reclassified_count": 1,
        "structural_only_reclassification_count": 1,
        "in_chat_semantic_review_required_count": 1,
        "semantic_review_completed_count": 0,
        "semantic_acceptance_count": 0,
        "semantic_rejection_count": 0,
        "candidate_edit_emitted_count": 0,
        "application_blocker_packet_emitted_count": 1,
        "application_blocked_count": 1,
        "application_authorized_after_barrier_count": 0,
        "application_authorized_in_this_unit_count": 0,
        "proposal_applied_count": 0,
        "target_field_filled_count": 0,
        "null_field_value_emitted_count": 0,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "r1000_run_executed_count": 0,
        "pressure_group_opened_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": "PERFORM_IN_CHAT_SEMANTIC_REVIEW_OF_CANDIDATE_MISSING_OBJECT_PROPOSAL_CE1FE7FC_V0",
    }

def validate_barrier_outputs(
    reclassification: Dict[str, Any],
    request: Dict[str, Any],
    checklist: Dict[str, Any],
    blocker: Dict[str, Any],
    trace: Dict[str, Any],
    report: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if reclassification.get("previous_review_reclassified_as") != "STRUCTURAL_ADMISSIBILITY_REVIEW_ONLY":
        failures.append("reclassification_status_wrong")
    if reclassification.get("not_semantic_acceptance") is not True:
        failures.append("reclassification_does_not_block_semantic_acceptance")
    if reclassification.get("not_application_authorization_after_barrier") is not True:
        failures.append("reclassification_does_not_block_application_authorization")
    if request.get("semantic_review_required") is not True:
        failures.append("semantic_review_not_required")
    if request.get("semantic_review_location") != "chat":
        failures.append("semantic_review_location_not_chat")
    if request.get("semantic_review_classes") != SEMANTIC_REVIEW_CLASSES:
        failures.append("semantic_review_classes_wrong")
    for surface in REQUIRED_REVIEW_SURFACES:
        if surface not in request.get("must_inspect", []):
            failures.append(f"semantic_review_surface_missing:{surface}")
    if checklist.get("allowed_outcomes") != SEMANTIC_REVIEW_CLASSES:
        failures.append("checklist_allowed_outcomes_wrong")
    if blocker.get("application_blocked") is not True:
        failures.append("application_not_blocked")
    if blocker.get("application_authorization_after_barrier") is not False:
        failures.append("application_authorized_after_barrier")
    if trace.get("terminal", {}).get("stop_code") != "STOP_IN_CHAT_SEMANTIC_REVIEW_REQUIRED_BEFORE_APPLICATION_AUTHORIZATION":
        failures.append("trace_terminal_stop_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_next_not_null")

    for key in [
        "semantic_review_completed_count",
        "semantic_acceptance_count",
        "semantic_rejection_count",
        "candidate_edit_emitted_count",
        "application_authorized_after_barrier_count",
        "application_authorized_in_this_unit_count",
        "proposal_applied_count",
        "target_field_filled_count",
        "null_field_value_emitted_count",
        "field_value_invention_count",
        "taxonomy_label_creation_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "r1000_run_executed_count",
        "pressure_group_opened_count",
        "next_group_auto_opened_count",
        "hidden_next_command_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")

    if report.get("application_blocked_count") != 1:
        failures.append("application_blocked_count_wrong")
    if report.get("in_chat_semantic_review_required_count") != 1:
        failures.append("semantic_review_required_count_wrong")

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
    if metrics.get("structural_only_reclassification_count") != 1:
        failures.append("metric_structural_only_reclassification_wrong")
    if metrics.get("in_chat_semantic_review_required_count") != 1:
        failures.append("metric_semantic_review_required_wrong")
    if metrics.get("application_blocked_count") != 1:
        failures.append("metric_application_blocked_wrong")

    for key in [
        "semantic_review_completed_count",
        "semantic_acceptance_count",
        "semantic_rejection_count",
        "candidate_edit_emitted_count",
        "application_authorized_after_barrier_count",
        "application_authorized_in_this_unit_count",
        "proposal_applied_count",
        "target_field_filled_count",
        "null_field_value_emitted_count",
        "field_value_invention_count",
        "taxonomy_label_creation_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "r1000_run_executed_count",
        "pressure_group_opened_count",
        "next_group_auto_opened_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_IN_CHAT_SEMANTIC_REVIEW_REQUIRED_BEFORE_APPLICATION_AUTHORIZATION":
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

    reclassification = build_structural_only_reclassification(sources)
    request = build_semantic_review_request()
    checklist = build_semantic_review_checklist()
    blocker = build_application_blocker_packet(request)
    trace = build_transition_trace()
    report = build_report()

    write_json(STRUCTURAL_ONLY_RECLASSIFICATION_PATH, reclassification)
    write_json(IN_CHAT_SEMANTIC_REVIEW_REQUEST_PATH, request)
    write_json(SEMANTIC_REVIEW_CHECKLIST_PATH, checklist)
    write_json(APPLICATION_BLOCKER_PACKET_PATH, blocker)
    write_json(BARRIER_TRANSITION_TRACE_PATH, trace)
    write_json(BARRIER_REPORT_PATH, report)

    failures.extend(validate_barrier_outputs(reclassification, request, checklist, blocker, trace, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "SEMANTIC_BARRIER_0_PREVIOUS_REVIEW_CONSUMED": sources["proposal_review_receipt"]["receipt_id"] == SOURCE_PROPOSAL_REVIEW_RECEIPT_ID and sources["proposal_review_receipt"]["gate"] == "PASS",
        "SEMANTIC_BARRIER_1_CANDIDATE_CONSUMED": sources["candidate_proposal"]["candidate_object_id"] == CANDIDATE_OBJECT_ID,
        "SEMANTIC_BARRIER_2_RECLASSIFIED_AS_STRUCTURAL_ONLY": reclassification["previous_review_reclassified_as"] == "STRUCTURAL_ADMISSIBILITY_REVIEW_ONLY",
        "SEMANTIC_BARRIER_3_IN_CHAT_SEMANTIC_REVIEW_REQUEST_EMITTED": IN_CHAT_SEMANTIC_REVIEW_REQUEST_PATH.exists() and request["semantic_review_required"] is True,
        "SEMANTIC_BARRIER_4_REVIEW_CHECKLIST_EMITTED": SEMANTIC_REVIEW_CHECKLIST_PATH.exists() and checklist["allowed_outcomes"] == SEMANTIC_REVIEW_CLASSES,
        "SEMANTIC_BARRIER_5_APPLICATION_BLOCKER_EMITTED": APPLICATION_BLOCKER_PACKET_PATH.exists() and blocker["application_blocked"] is True,
        "SEMANTIC_BARRIER_6_NO_SEMANTIC_ACCEPTANCE_OR_REJECTION": report["semantic_acceptance_count"] == 0 and report["semantic_rejection_count"] == 0,
        "SEMANTIC_BARRIER_7_NO_APPLICATION_AUTHORIZATION_AFTER_BARRIER": report["application_authorized_after_barrier_count"] == 0 and blocker["application_authorization_after_barrier"] is False,
        "SEMANTIC_BARRIER_8_NO_PROPOSAL_APPLICATION": report["proposal_applied_count"] == 0,
        "SEMANTIC_BARRIER_9_NO_FIELD_FILLING_OR_VALUE_INVENTION": report["target_field_filled_count"] == 0 and report["field_value_invention_count"] == 0 and report["null_field_value_emitted_count"] == 0,
        "SEMANTIC_BARRIER_10_NO_TAXONOMY_ACTION": report["taxonomy_label_creation_count"] == 0 and report["taxonomy_upgrade_authorized_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "SEMANTIC_BARRIER_11_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "SEMANTIC_BARRIER_12_NO_R1000_RUN_OR_GROUP_OPEN": report["r1000_run_executed_count"] == 0 and report["pressure_group_opened_count"] == 0 and report["next_group_auto_opened_count"] == 0,
        "SEMANTIC_BARRIER_13_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_IN_CHAT_SEMANTIC_REVIEW_REQUIRED_BEFORE_APPLICATION_AUTHORIZATION",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_AUTHORITY_VIOLATION",
            "next_command_goal": None,
        }

    aggregate_metrics = {
        "source_proposal_review_receipt_id": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
        "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "candidate_object_id": CANDIDATE_OBJECT_ID,
        "machine_review_reclassified_count": 1,
        "structural_only_reclassification_count": 1,
        "in_chat_semantic_review_required_count": 1,
        "semantic_review_completed_count": 0,
        "semantic_acceptance_count": 0,
        "semantic_rejection_count": 0,
        "candidate_edit_emitted_count": 0,
        "application_blocker_packet_emitted_count": 1,
        "application_blocked_count": 1,
        "application_authorized_after_barrier_count": 0,
        "application_authorized_in_this_unit_count": 0,
        "proposal_applied_count": 0,
        "target_field_filled_count": 0,
        "null_field_value_emitted_count": 0,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "existing_receipt_mutation_count": 0,
        "r1000_run_executed_count": 0,
        "pressure_group_opened_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
        "blocked_application_unit": blocker["blocked_application_unit"],
        "recommended_next_handling": report["recommended_next_handling"],
    }

    guards = {
        "previous_review_consumed": True,
        "candidate_consumed": True,
        "previous_review_reclassified_as_structural_only": True,
        "in_chat_semantic_review_required": True,
        "application_blocked": True,
        "semantic_review_completed": False,
        "semantic_acceptance": False,
        "semantic_rejection": False,
        "application_authorized_after_barrier": False,
        "application_authorized_in_this_unit": False,
        "proposal_applied": False,
        "target_field_filled": False,
        "null_field_value_emitted": False,
        "values_invented": False,
        "taxonomy_label_created": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "r1000_run_executed": False,
        "pressure_group_opened": False,
        "next_group_auto_opened": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_review": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
        "candidate_object_id": CANDIDATE_OBJECT_ID,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "structural_only_reclassification": rel(STRUCTURAL_ONLY_RECLASSIFICATION_PATH),
        "in_chat_semantic_review_request": rel(IN_CHAT_SEMANTIC_REVIEW_REQUEST_PATH),
        "semantic_review_checklist": rel(SEMANTIC_REVIEW_CHECKLIST_PATH),
        "application_blocker_packet": rel(APPLICATION_BLOCKER_PACKET_PATH),
        "semantic_review_barrier_transition_trace": rel(BARRIER_TRANSITION_TRACE_PATH),
        "semantic_review_barrier_report": rel(BARRIER_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "candidate_proposal_semantic_review_barrier_r1000_taxonomy_gap_receipt_v0",
        "receipt_type": "CANDIDATE_PROPOSAL_SEMANTIC_REVIEW_BARRIER_R1000_TAXONOMY_GAP_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_proposal_review_receipt_id": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
        "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "candidate_object_id": CANDIDATE_OBJECT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "candidate_proposal_semantic_review_barrier_summary": {
            "candidate_object_id": CANDIDATE_OBJECT_ID,
            "previous_review_reclassified_as": "STRUCTURAL_ADMISSIBILITY_REVIEW_ONLY",
            "semantic_review_required": True,
            "semantic_review_location": "chat",
            "semantic_review_completed": False,
            "semantic_acceptance": False,
            "application_blocked": True,
            "blocked_application_unit": blocker["blocked_application_unit"],
            "allowed_semantic_review_classes": SEMANTIC_REVIEW_CLASSES,
            "recommended_next_handling": report["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "candidate_proposal_semantic_review_barrier_guards": guards,
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
    print(f"candidate_proposal_semantic_review_barrier_receipt_id={receipt_id}")
    print(f"candidate_proposal_semantic_review_barrier_receipt_path=data/candidate_proposal_semantic_review_barrier_r1000_taxonomy_gap_v0_receipts/{receipt_id}.json")
    print(f"in_chat_semantic_review_request_path=data/candidate_proposal_semantic_review_barrier_r1000_taxonomy_gap_v0/in_chat_semantic_review_request.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
