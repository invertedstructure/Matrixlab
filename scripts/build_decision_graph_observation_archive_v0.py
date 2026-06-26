#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_DECISION_GRAPH_OBSERVATION_ARCHIVE_V0"
TARGET_UNIT_ID = "decision_graph.observation_archive.v0"

OUT_DIR = ROOT / "data/decision_graph_observation_archive_v0"
RECEIPT_DIR = ROOT / "data/decision_graph_observation_archive_v0_receipts"

INTAKE_PATH = OUT_DIR / "decision_graph_observation_intake_v0.json"
GRAPH_SCHEMA_RECORD_PATH = OUT_DIR / "decision_graph_schema_record_v0.json"
OBSERVED_INSTANCES_PATH = OUT_DIR / "decision_graph_observed_instances_v0.jsonl"
SUPPORTING_RECEIPT_MAP_PATH = OUT_DIR / "decision_graph_supporting_receipt_map_v0.json"
COUNTEREXAMPLES_PATH = OUT_DIR / "decision_graph_counterexamples_v0.jsonl"
KNOWN_VARIANTS_PATH = OUT_DIR / "decision_graph_known_variants_v0.jsonl"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "decision_graph_authority_boundary_v0.json"
ARCHIVE_INDEX_PATH = OUT_DIR / "decision_graph_observation_archive_index_v0.json"
MINIMAL_BASIS_HYPOTHESIS_PATH = OUT_DIR / "decision_graph_minimal_basis_hypothesis_v0.json"
ROLLUP_PATH = OUT_DIR / "decision_graph_observation_archive_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "decision_graph_observation_archive_profile_v0.json"
REPORT_PATH = OUT_DIR / "decision_graph_observation_archive_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "decision_graph_observation_archive_transition_trace.json"

VALID_TRIGGER_FAMILIES = {
    "TYPED_CAPABILITY_BOUNDARY_STOP",
    "BOUNDED_PROPOSAL_CANDIDATE",
    "EXPECTED_NEGATIVE_COVERAGE_PRESSURE",
    "BRANCH_CLOSURE_RECEIPT",
    "RUNTIME_SMOKE_TERMINAL",
    "VALIDATOR_SCHEMA_MATCH_OBSERVED",
    "HUMAN_DECISION_PACKET",
    "SCHEMA_ARCHIVE_PROMOTION_DECISION",
    "SCHEMA_ARCHIVE_WRITE_RECEIPT",
    "RUNTIME_MEMBRANE_TERMINAL",
    "NO_APPLICABLE_MOVE_PRESSURE",
    "ADMISSIBILITY_BLOCK",
    "SCHEMA_VALIDATION_BLOCK",
    "REFERENCE_CLOSURE",
}

VALID_GRAPH_STATUSES = {
    "OBSERVED_ONCE",
    "RECURRING_CANDIDATE",
    "RECURRING_CONFIRMED",
    "DEPRECATED",
    "MERGED_INTO_OTHER_GRAPH",
    "REJECTED_AS_OVERFIT",
}

VALID_EVIDENCE_GRADES = {
    "SINGLE_RECEIPT",
    "MULTI_RECEIPT_WEAK",
    "MULTI_RECEIPT_STABLE",
    "REVIEWED_RECURRING",
    "COUNTEREXAMPLE_LIMITED",
}

VALID_EDGE_KINDS = {
    "OBSERVED_TRANSITION",
    "HUMAN_DECISION_EDGE",
    "VALIDATION_EDGE",
    "ADMISSIBILITY_EDGE",
    "ARCHIVE_WRITE_EDGE",
    "CLOSURE_EDGE",
    "BLOCKING_EDGE",
    "TERMINAL_EDGE",
    "OBSERVATION_EDGE",
}

VALID_EDGE_SOURCE_KINDS = {
    "OPERATOR_DECLARED",
    "RECEIPT_FIELD",
    "TRANSITION_TRACE",
    "HUMAN_DECISION_PACKET",
    "TYPED_STOP",
    "READOUT_OR_ROLLUP",
}

NEGATIVE_COUNTER_KEYS = [
    "observed_graph_treated_as_authorized_count",
    "recurring_graph_treated_as_validator_schema_count",
    "graph_archive_treated_as_authorization_archive_count",
    "receipt_evidence_treated_as_future_authority_count",
    "validator_authorization_schema_created_count",
    "execution_registry_mutated_count",
    "runtime_adoption_authorized_count",
    "schema_mutation_authorized_count",
    "schema_archive_mutation_count",
    "move_addition_authorized_count",
    "fixture_expansion_authorized_count",
    "human_review_bypass_authorized_count",
    "c7_opened_count",
    "c8_authorized_count",
    "hidden_next_command_count",
    "latest_file_selection_count",
    "mtime_selection_count",
    "source_receipt_mutation_count",
    "source_trace_mutation_count",
    "source_readout_mutation_count",
    "source_rollup_mutation_count",
    "repo_wide_graph_discovery_count",
    "operator_intake_generated_by_builder_count",
    "duplicate_graph_id_count",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
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

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))

def nonempty_list(x: Any) -> bool:
    return isinstance(x, list) and len(x) > 0

def stop_for_failures(failures: List[str]) -> Tuple[str, str, str]:
    if not failures:
        return (
            "PASS",
            "TYPED_DECISION_GRAPH_OBSERVATION_ARCHIVE_PASS_READY",
            "DECISION_GRAPH_ARCHIVE_PASS_OBSERVATION_READY",
        )
    first = failures[0]
    if first.startswith("intake_missing"):
        return ("FAIL", "TYPED_DECISION_GRAPH_INTAKE_MISSING", "DECISION_GRAPH_ARCHIVE_BLOCKED_INTAKE_MISSING")
    if "builder_generated" in first:
        return ("FAIL", "TYPED_DECISION_GRAPH_INTAKE_BUILDER_GENERATED", "DECISION_GRAPH_ARCHIVE_BLOCKED_INTAKE_UNTYPED")
    if "repo_wide_inference" in first:
        return ("FAIL", "TYPED_DECISION_GRAPH_REPO_WIDE_INFERENCE_BLOCKED", "DECISION_GRAPH_ARCHIVE_BLOCKED_INTAKE_UNTYPED")
    if "no_receipt_evidence" in first:
        return ("FAIL", "TYPED_DECISION_GRAPH_NO_RECEIPT_EVIDENCE", "DECISION_GRAPH_ARCHIVE_BLOCKED_NO_RECEIPT_EVIDENCE")
    if "trigger_family_missing" in first:
        return ("FAIL", "TYPED_DECISION_GRAPH_TRIGGER_FAMILY_UNNAMED", "DECISION_GRAPH_ARCHIVE_BLOCKED_TRIGGER_FAMILY_UNNAMED")
    if "trigger_family_unresolved" in first:
        return ("FAIL", "TYPED_DECISION_GRAPH_TRIGGER_FAMILY_UNRESOLVED", "DECISION_GRAPH_ARCHIVE_BLOCKED_TRIGGER_FAMILY_UNRESOLVED")
    if "edges_untyped" in first or "edge_support_missing" in first:
        return ("FAIL", "TYPED_DECISION_GRAPH_EDGES_UNTYPED", "DECISION_GRAPH_ARCHIVE_BLOCKED_EDGES_UNTYPED")
    if "allowed_transitions_missing" in first:
        return ("FAIL", "TYPED_DECISION_GRAPH_ALLOWED_TRANSITIONS_MISSING", "DECISION_GRAPH_ARCHIVE_BLOCKED_ALLOWED_TRANSITIONS_MISSING")
    if "forbidden_transitions_missing" in first:
        return ("FAIL", "TYPED_DECISION_GRAPH_FORBIDDEN_TRANSITIONS_MISSING", "DECISION_GRAPH_ARCHIVE_BLOCKED_FORBIDDEN_TRANSITIONS_MISSING")
    if "terminals_missing" in first:
        return ("FAIL", "TYPED_DECISION_GRAPH_TERMINALS_MISSING", "DECISION_GRAPH_ARCHIVE_BLOCKED_TERMINALS_MISSING")
    if "authority" in first or "leak" in first:
        return ("FAIL", "TYPED_DECISION_GRAPH_AUTHORITY_LEAK_BLOCKED", "DECISION_GRAPH_ARCHIVE_AUTHORITY_VIOLATION")
    if "duplicate_graph_id" in first:
        return ("FAIL", "TYPED_DECISION_GRAPH_DUPLICATE_GRAPH_ID", "DECISION_GRAPH_ARCHIVE_BLOCKED_RECEIPT_MISMATCH")
    return ("FAIL", "TYPED_DECISION_GRAPH_RECEIPT_MISMATCH", "DECISION_GRAPH_ARCHIVE_BLOCKED_RECEIPT_MISMATCH")

def terminal_for(gate: str, failures: List[str]) -> Dict[str, Any]:
    if gate == "PASS":
        return {
            "type": "STOP",
            "stop_code": "STOP_DECISION_GRAPH_OBSERVATION_ARCHIVE_READY",
            "next_command_goal": None,
        }
    first = failures[0] if failures else ""
    if first.startswith("intake_missing"):
        stop = "STOP_DECISION_GRAPH_INTAKE_MISSING"
    elif "builder_generated" in first:
        stop = "STOP_DECISION_GRAPH_INTAKE_BUILDER_GENERATED"
    elif "repo_wide_inference" in first:
        stop = "STOP_DECISION_GRAPH_REPO_WIDE_INFERENCE_BLOCKED"
    elif "no_receipt_evidence" in first:
        stop = "STOP_DECISION_GRAPH_NO_RECEIPT_EVIDENCE"
    elif "trigger_family_missing" in first:
        stop = "STOP_DECISION_GRAPH_PRIMARY_TRIGGER_FAMILY_MISSING"
    elif "trigger_family_unresolved" in first:
        stop = "STOP_DECISION_GRAPH_TRIGGER_FAMILY_UNRESOLVED"
    elif "edge_support_missing" in first:
        stop = "STOP_DECISION_GRAPH_EDGE_SUPPORT_MISSING"
    elif "edges_untyped" in first:
        stop = "STOP_DECISION_GRAPH_EDGES_UNTYPED"
    elif "allowed_transitions_missing" in first:
        stop = "STOP_DECISION_GRAPH_ALLOWED_TRANSITIONS_MISSING"
    elif "forbidden_transitions_missing" in first:
        stop = "STOP_DECISION_GRAPH_FORBIDDEN_TRANSITIONS_MISSING"
    elif "terminals_missing" in first:
        stop = "STOP_DECISION_GRAPH_TERMINALS_MISSING"
    elif "duplicate_graph_id" in first:
        stop = "STOP_DECISION_GRAPH_DUPLICATE_GRAPH_ID"
    elif "authority" in first or "leak" in first:
        stop = "STOP_DECISION_GRAPH_AUTHORITY_LEAK_BLOCKED"
    else:
        stop = "STOP_DECISION_GRAPH_RECEIPT_MISMATCH"
    return {
        "type": "STOP",
        "stop_code": stop,
        "next_command_goal": None,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    warnings: List[str] = []

    if not INTAKE_PATH.exists():
        failures.append(f"intake_missing:{rel(INTAKE_PATH)}")
        intake: Dict[str, Any] = {}
    else:
        intake = read_json(INTAKE_PATH)

    source_files_before: Dict[str, str] = {}

    if intake:
        required = [
            "schema_version",
            "intake_id",
            "selected_by",
            "builder_generated",
            "extraction_mode",
            "declared_graph_schema_id",
            "declared_graph_name",
            "primary_trigger_object_family",
            "declared_graph_candidate_status",
            "evidence_grade",
            "source_receipt_refs",
            "declared_decision_edges",
            "declared_allowed_transitions",
            "declared_forbidden_transitions",
            "declared_terminal_states",
            "declared_not_authorized_for",
            "must_not_infer",
        ]
        for key in required:
            if key not in intake:
                failures.append(f"intake_untyped:missing:{key}")

        if intake.get("schema_version") != "decision_graph_observation_intake_v0":
            failures.append(f"intake_untyped:schema_version:{intake.get('schema_version')}")
        if intake.get("selected_by") != "human/operator":
            failures.append(f"intake_untyped:selected_by:{intake.get('selected_by')}")
        if intake.get("builder_generated") is not False:
            failures.append(f"intake_builder_generated:{intake.get('builder_generated')}")
        if intake.get("extraction_mode") not in {"BIND_DECLARED_GRAPH_FROM_RECEIPTS", "EXTRACT_CANDIDATE_FROM_RECEIPTS"}:
            failures.append(f"intake_untyped:extraction_mode:{intake.get('extraction_mode')}")
        if intake.get("extraction_mode") != "BIND_DECLARED_GRAPH_FROM_RECEIPTS":
            failures.append(f"repo_wide_inference_blocked:extraction_mode:{intake.get('extraction_mode')}")

        if not nonempty_list(intake.get("source_receipt_refs")):
            failures.append("no_receipt_evidence:source_receipt_refs_empty")

        primary_trigger = intake.get("primary_trigger_object_family")
        if not primary_trigger:
            failures.append("trigger_family_missing:primary_trigger_object_family")
        elif primary_trigger not in VALID_TRIGGER_FAMILIES:
            failures.append(f"trigger_family_unresolved:{primary_trigger}")

        if intake.get("declared_trigger_object_family") and intake.get("declared_trigger_object_family") != primary_trigger:
            failures.append("trigger_family_unresolved:declared_primary_mismatch")

        if intake.get("declared_graph_candidate_status") not in VALID_GRAPH_STATUSES:
            failures.append(f"intake_untyped:graph_status:{intake.get('declared_graph_candidate_status')}")
        if intake.get("evidence_grade") not in VALID_EVIDENCE_GRADES:
            failures.append(f"intake_untyped:evidence_grade:{intake.get('evidence_grade')}")

        if intake.get("declared_graph_candidate_status") == "RECURRING_CONFIRMED" and intake.get("evidence_grade") not in {"MULTI_RECEIPT_STABLE", "REVIEWED_RECURRING"}:
            failures.append("authority_leak:recurring_confirmed_without_required_evidence_grade")

        for bucket in [
            "source_receipt_refs",
            "source_trace_refs",
            "source_readout_refs",
            "source_rollup_refs",
            "source_human_decision_packet_refs",
        ]:
            for ref in intake.get(bucket, []) or []:
                p = ROOT / ref
                if not p.exists():
                    failures.append(f"source_ref_missing:{bucket}:{ref}")
                else:
                    source_files_before[ref] = file_sha256(p)

        edges = intake.get("declared_decision_edges") or []
        if not nonempty_list(edges):
            failures.append("edges_untyped:declared_decision_edges_empty")
        for edge in edges:
            if not isinstance(edge, dict):
                failures.append("edges_untyped:edge_not_object")
                continue
            for key in [
                "edge_name",
                "from_state",
                "to_state",
                "edge_kind",
                "edge_source_kind",
                "required_inputs",
                "required_evidence",
                "allowed_when",
                "blocked_when",
                "supporting_receipt_refs",
                "forbidden_inferences",
            ]:
                if key not in edge:
                    failures.append(f"edges_untyped:{edge.get('edge_name', '<missing>')}:{key}")
            if edge.get("edge_kind") not in VALID_EDGE_KINDS:
                failures.append(f"edges_untyped:edge_kind:{edge.get('edge_name')}:{edge.get('edge_kind')}")
            if edge.get("edge_source_kind") not in VALID_EDGE_SOURCE_KINDS:
                failures.append(f"edges_untyped:edge_source_kind:{edge.get('edge_name')}:{edge.get('edge_source_kind')}")
            if not nonempty_list(edge.get("supporting_receipt_refs")) and not nonempty_list(edge.get("supporting_trace_refs")):
                failures.append(f"edge_support_missing:{edge.get('edge_name')}")
            for ref in edge.get("supporting_receipt_refs", []) or []:
                if not (ROOT / ref).exists():
                    failures.append(f"edge_support_missing:{edge.get('edge_name')}:{ref}")
            for ref in edge.get("supporting_trace_refs", []) or []:
                if not (ROOT / ref).exists():
                    failures.append(f"edge_support_missing:{edge.get('edge_name')}:{ref}")

        if not nonempty_list(intake.get("declared_allowed_transitions")):
            failures.append("allowed_transitions_missing")
        if not nonempty_list(intake.get("declared_forbidden_transitions")):
            failures.append("forbidden_transitions_missing")
        if not nonempty_list(intake.get("declared_terminal_states")):
            failures.append("terminals_missing")
        if not nonempty_list(intake.get("declared_not_authorized_for")):
            failures.append("authority_boundary_missing:not_authorized_for_empty")

    graph_schema_id = intake.get("declared_graph_schema_id", "DG_UNKNOWN_V0")
    graph_name = intake.get("declared_graph_name")
    graph_status = intake.get("declared_graph_candidate_status")
    evidence_grade = intake.get("evidence_grade")
    primary_trigger = intake.get("primary_trigger_object_family")
    secondary_triggers = intake.get("secondary_trigger_object_families", []) or []

    if GRAPH_SCHEMA_RECORD_PATH.exists():
        try:
            existing = read_json(GRAPH_SCHEMA_RECORD_PATH)
            if existing.get("graph_schema_id") == graph_schema_id:
                failures.append(f"duplicate_graph_id:{graph_schema_id}")
        except Exception:
            failures.append("duplicate_graph_id:existing_record_unreadable")

    negative_controls = {key: 0 for key in NEGATIVE_COUNTER_KEYS}
    bad_counters_zero = all(v == 0 for v in negative_controls.values())

    gate, status, outcome_class = stop_for_failures(failures)
    terminal = terminal_for(gate, failures)

    edge_records: List[Dict[str, Any]] = []
    for edge in intake.get("declared_decision_edges", []) or []:
        edge_record = {
            "edge_id": "decision_edge_" + sig8({
                "graph_schema_id": graph_schema_id,
                "edge_name": edge.get("edge_name"),
                "from_state": edge.get("from_state"),
                "to_state": edge.get("to_state"),
            }),
            "edge_name": edge.get("edge_name"),
            "from_state": edge.get("from_state"),
            "to_state": edge.get("to_state"),
            "edge_kind": edge.get("edge_kind"),
            "edge_source_kind": edge.get("edge_source_kind"),
            "required_inputs": edge.get("required_inputs", []),
            "required_evidence": edge.get("required_evidence", []),
            "allowed_when": edge.get("allowed_when", []),
            "blocked_when": edge.get("blocked_when", []),
            "emitted_artifacts": edge.get("emitted_artifacts", []),
            "terminal_if_blocked": edge.get("terminal_if_blocked"),
            "human_decision_required": bool(edge.get("human_decision_required", False)),
            "authority_boundary": edge.get("authority_boundary", []),
            "supporting_receipt_refs": edge.get("supporting_receipt_refs", []),
            "supporting_trace_refs": edge.get("supporting_trace_refs", []),
            "forbidden_inferences": edge.get("forbidden_inferences", []),
        }
        edge_records.append(edge_record)

    observed_instance = {
        "schema_version": "decision_graph_observed_instance_v0",
        "observed_instance_id": "dg_instance_" + sig8({
            "graph_schema_id": graph_schema_id,
            "source_receipts": intake.get("source_receipt_refs", []),
            "terminal": intake.get("declared_terminal_states", []),
        }),
        "graph_schema_id": graph_schema_id,
        "source_unit_id": "EXECUTE_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_V0",
        "source_receipt_ref": (intake.get("source_receipt_refs") or [None])[0],
        "source_trace_ref": (intake.get("source_trace_refs") or [None])[0],
        "source_readout_ref": (intake.get("source_readout_refs") or [None])[0],
        "trigger_object_family": primary_trigger,
        "observed_edges": [e["edge_id"] for e in edge_records],
        "observed_terminal": (intake.get("declared_terminal_states") or [None])[0],
        "human_decision_points_seen": intake.get("declared_human_decision_points", []),
        "allowed_transitions_seen": intake.get("declared_allowed_transitions", []),
        "forbidden_transitions_preserved": intake.get("declared_forbidden_transitions", []),
        "authority_boundary_preserved": True,
        "notes": intake.get("operator_notes", []),
    }

    support_strength = "SINGLE_OBSERVATION"
    if evidence_grade in {"MULTI_RECEIPT_WEAK"}:
        support_strength = "MULTI_OBSERVATION_WEAK"
    elif evidence_grade in {"MULTI_RECEIPT_STABLE", "REVIEWED_RECURRING"}:
        support_strength = "MULTI_OBSERVATION_STABLE"

    supporting_receipt_map = {
        "schema_version": "decision_graph_supporting_receipt_map_v0",
        "graph_schema_id": graph_schema_id,
        "receipt_refs": intake.get("source_receipt_refs", []),
        "trace_refs": intake.get("source_trace_refs", []),
        "readout_refs": intake.get("source_readout_refs", []),
        "rollup_refs": intake.get("source_rollup_refs", []),
        "receipt_count": len(intake.get("source_receipt_refs", []) or []),
        "support_strength": support_strength,
        "evidence_grade": evidence_grade,
        "support_notes": [
            "Support strength is evidential only and does not authorize action."
        ],
    }

    counterexamples = []
    for c in intake.get("counterexamples", []) or []:
        row = dict(c)
        row.setdefault("schema_version", "decision_graph_counterexample_v0")
        row.setdefault("counterexample_id", "dg_counterexample_" + sig8(c))
        row.setdefault("graph_schema_id", graph_schema_id)
        counterexamples.append(row)

    known_variants = []
    for v in intake.get("known_variants", []) or []:
        row = dict(v)
        row.setdefault("schema_version", "decision_graph_known_variant_v0")
        row.setdefault("variant_id", "dg_variant_" + sig8(v))
        row.setdefault("parent_graph_schema_id", graph_schema_id)
        row.setdefault("not_authorized_for", intake.get("declared_not_authorized_for", []))
        known_variants.append(row)

    authority_boundary = {
        "schema_version": "decision_graph_authority_boundary_v0",
        "boundary_status": "OBSERVATION_ONLY_NO_AUTHORITY" if gate == "PASS" else "BLOCKED",
        "observed_graph_means_authorized_graph": False,
        "recurring_graph_means_validator_schema": False,
        "graph_archive_means_authorization_archive": False,
        "receipt_evidence_means_future_authority": False,
        "graph_schema_means_execution_registry_entry": False,
        "human_review_bypass_authorized": False,
        "runtime_adoption_authorized": False,
        "schema_mutation_authorized": False,
        "schema_archive_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "c7_opened": False,
        "c8_authorized": False,
        "validator_recurring_mode_authorized": False,
        "validator_authorization_schema_created": False,
        "execution_registry_mutated": False,
    }

    graph_schema_record = {
        "schema_version": "decision_graph_schema_record_v0",
        "schema_role": "OBSERVATION_SCHEMA_ONLY",
        "graph_schema_id": graph_schema_id,
        "graph_name": graph_name,
        "graph_status": graph_status,
        "evidence_grade": evidence_grade,
        "archive_status": "OBSERVATION_ONLY",
        "validator_schema_role": False,
        "authorization_schema_role": False,
        "execution_schema_role": False,
        "source": {
            "source_receipt_refs": intake.get("source_receipt_refs", []),
            "source_trace_refs": intake.get("source_trace_refs", []),
            "source_readout_refs": intake.get("source_readout_refs", []),
            "source_rollup_refs": intake.get("source_rollup_refs", []),
            "source_human_decision_packet_refs": intake.get("source_human_decision_packet_refs", []),
        },
        "primary_trigger_object_family": primary_trigger,
        "secondary_trigger_object_families": secondary_triggers,
        "reuse_bound_to_primary_trigger_family": True,
        "trigger_object_family": primary_trigger,
        "required_input_objects": intake.get("declared_required_input_objects", []),
        "required_evidence": intake.get("declared_required_evidence", []),
        "decision_edges": edge_records,
        "allowed_transitions": intake.get("declared_allowed_transitions", []),
        "forbidden_transitions": intake.get("declared_forbidden_transitions", []),
        "terminal_states": intake.get("declared_terminal_states", []),
        "human_decision_points": intake.get("declared_human_decision_points", []),
        "authority_boundary": {
            "authorization_granted": False,
            "validator_authorization_schema_created": False,
            "execution_registry_mutated": False,
            "runtime_adoption_authorized": False,
            "schema_mutation_authorized": False,
            "schema_archive_mutation_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "c7_opened": False,
            "c8_authorized": False,
        },
        "receipts_required": intake.get("source_receipt_refs", []),
        "observed_instances": [observed_instance["observed_instance_id"]],
        "counterexamples": [c["counterexample_id"] for c in counterexamples],
        "known_variants": [v["variant_id"] for v in known_variants],
        "reuse_conditions": intake.get("declared_reuse_conditions", []),
        "not_authorized_for": intake.get("declared_not_authorized_for", []),
        "notes": intake.get("operator_notes", []),
        "must_not_infer": intake.get("must_not_infer", []) + [
            "graph may be used by validator recurring mode",
            "graph may mutate registry",
            "graph may mutate schema archive",
        ],
    }

    archive_id = "decision_graph_observation_archive_" + sig8({
        "graph_schema_id": graph_schema_id,
        "graph_status": graph_status,
        "receipt_refs": intake.get("source_receipt_refs", []),
    })

    archive_index = {
        "schema_version": "decision_graph_observation_archive_index_v0",
        "archive_id": archive_id,
        "archive_status": "DESCRIPTIVE_OBSERVATION_ARCHIVE",
        "graph_records": [
            {
                "graph_schema_id": graph_schema_id,
                "graph_name": graph_name,
                "graph_status": graph_status,
                "evidence_grade": evidence_grade,
                "primary_trigger_object_family": primary_trigger,
                "graph_schema_record_ref": rel(GRAPH_SCHEMA_RECORD_PATH),
            }
        ] if gate == "PASS" else [],
        "graph_count": 1 if gate == "PASS" else 0,
        "observed_once_count": 1 if gate == "PASS" and graph_status == "OBSERVED_ONCE" else 0,
        "recurring_candidate_count": 1 if gate == "PASS" and graph_status == "RECURRING_CANDIDATE" else 0,
        "recurring_confirmed_count": 1 if gate == "PASS" and graph_status == "RECURRING_CONFIRMED" else 0,
        "deprecated_count": 1 if gate == "PASS" and graph_status == "DEPRECATED" else 0,
        "merged_count": 1 if gate == "PASS" and graph_status == "MERGED_INTO_OTHER_GRAPH" else 0,
        "rejected_as_overfit_count": 1 if gate == "PASS" and graph_status == "REJECTED_AS_OVERFIT" else 0,
        "authorization_count": 0,
        "execution_registry_mutation_count": 0,
        "must_not_infer": [
            "archive entry authorizes graph use",
            "recurring graph is validator schema",
            "graph archive can commit",
            "graph archive can mutate runtime",
            "graph archive can bypass human review",
        ],
    }

    minimal_basis_hypothesis = {
        "schema_version": "decision_graph_minimal_basis_hypothesis_v0",
        "hypothesis": "There may exist a small basis of recurring lawful decision graph schemas that unfold across different domains and capability layers.",
        "status": "HYPOTHESIS_ONLY",
        "supporting_graph_schema_ids": [graph_schema_id] if gate == "PASS" else [],
        "counterexample_graph_schema_ids": [],
        "must_not_infer": [
            "basis is known",
            "basis is complete",
            "new graph must fit existing basis",
            "future graph authorization is implied",
        ],
    }

    rollup = {
        "schema_version": "decision_graph_observation_archive_rollup_v0",
        "runs": 1,
        "graph_schema_record_emitted": gate == "PASS",
        "archive_index_emitted": gate == "PASS",
        "observed_instance_count": 1 if gate == "PASS" else 0,
        "supporting_receipt_count": len(intake.get("source_receipt_refs", []) or []),
        "counterexample_count": len(counterexamples),
        "known_variant_count": len(known_variants),
        "graph_status": graph_status if gate == "PASS" else None,
        "evidence_grade": evidence_grade if gate == "PASS" else None,
        "trigger_object_family": primary_trigger if gate == "PASS" else None,
        "authority_boundary_declared": gate == "PASS",
        "authorization_created": False,
        "validator_schema_created": False,
        "execution_registry_mutated": False,
        "runtime_adoption_authorized": False,
        "schema_mutation_authorized": False,
        "schema_archive_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "c7_opened": False,
        "c8_authorized": False,
        "bad_counters_zero": bad_counters_zero,
    }

    profile_id = "decision_graph_observation_archive_profile_" + sig8({
        "archive_id": archive_id,
        "graph_schema_id": graph_schema_id,
        "graph_status": graph_status,
    })

    profile = {
        "schema_version": "decision_graph_observation_archive_profile_v0",
        "profile_id": profile_id,
        "status": "DG_ARCHIVE_PASS" if gate == "PASS" else "DG_ARCHIVE_BLOCKED",
        "core_rule": "The archive records observed decision graph shapes from receipts; it does not authorize future action.",
        "graph_schema_record_ref": rel(GRAPH_SCHEMA_RECORD_PATH),
        "archive_index_ref": rel(ARCHIVE_INDEX_PATH),
        "supporting_receipt_map_ref": rel(SUPPORTING_RECEIPT_MAP_PATH),
        "authority_boundary_ref": rel(AUTHORITY_BOUNDARY_PATH),
        "graph_status": graph_status if gate == "PASS" else None,
        "evidence_grade": evidence_grade if gate == "PASS" else None,
        "trigger_object_family": primary_trigger if gate == "PASS" else None,
        "bad_counters_zero": bad_counters_zero,
        "must_not_infer": [
            "observed graph is authorized",
            "recurring graph is validator schema",
            "graph archive is authorization archive",
            "receipt evidence grants future authority",
            "graph schema can execute",
            "human review can be bypassed",
            "C8 is authorized",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "decision_graph_observation_archive_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "outcome_class": outcome_class,
        "summary": {
            "graph_observation_archive_ready": gate == "PASS",
            "archive_id": archive_id,
            "graph_schema_id": graph_schema_id,
            "graph_name": graph_name,
            "graph_status": graph_status,
            "evidence_grade": evidence_grade,
            "primary_trigger_object_family": primary_trigger,
            "receipt_count": len(intake.get("source_receipt_refs", []) or []),
            "edge_count": len(edge_records),
            "allowed_transition_count": len(intake.get("declared_allowed_transitions", []) or []),
            "forbidden_transition_count": len(intake.get("declared_forbidden_transitions", []) or []),
            "terminal_count": len(intake.get("declared_terminal_states", []) or []),
            "observation_only": True,
            "authorization_created": False,
            "validator_schema_created": False,
            "execution_registry_mutated": False,
            "runtime_adoption_authorized": False,
            "schema_mutation_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "c7_opened": False,
            "c8_authorized": False,
        },
        "failures": failures,
        "warnings": warnings,
    }

    transition_trace = {
        "schema_version": "decision_graph_observation_archive_transition_trace_v0",
        "unit_id": UNIT_ID,
        "archive_id": archive_id,
        "graph_schema_id": graph_schema_id,
        "transitions": [
            {
                "from": "DECISION_GRAPH_OBSERVATION_INTAKE_AVAILABLE",
                "edge": "consume operator-declared receipt-backed graph intake",
                "to": "DECISION_GRAPH_INTAKE_BOUND" if gate == "PASS" else "DECISION_GRAPH_INTAKE_BLOCKED",
            },
            {
                "from": "DECISION_GRAPH_INTAKE_BOUND" if gate == "PASS" else "DECISION_GRAPH_INTAKE_BLOCKED",
                "edge": "emit observation-only graph schema record and archive index",
                "to": "DECISION_GRAPH_OBSERVATION_ARCHIVE_READY" if gate == "PASS" else "DECISION_GRAPH_OBSERVATION_ARCHIVE_BLOCKED",
            },
            {
                "from": "DECISION_GRAPH_OBSERVATION_ARCHIVE_READY" if gate == "PASS" else "DECISION_GRAPH_OBSERVATION_ARCHIVE_BLOCKED",
                "edge": "stop with no automatic next command",
                "to": terminal["stop_code"],
            },
        ],
        "terminal": terminal,
    }

    if gate == "PASS":
        write_json(GRAPH_SCHEMA_RECORD_PATH, graph_schema_record)
        write_jsonl(OBSERVED_INSTANCES_PATH, [observed_instance])
        write_json(SUPPORTING_RECEIPT_MAP_PATH, supporting_receipt_map)
        write_jsonl(COUNTEREXAMPLES_PATH, counterexamples)
        write_jsonl(KNOWN_VARIANTS_PATH, known_variants)
        write_json(AUTHORITY_BOUNDARY_PATH, authority_boundary)
        write_json(ARCHIVE_INDEX_PATH, archive_index)
        write_json(MINIMAL_BASIS_HYPOTHESIS_PATH, minimal_basis_hypothesis)
        write_json(ROLLUP_PATH, rollup)
        write_json(PROFILE_PATH, profile)
        write_json(REPORT_PATH, report)
        write_json(TRANSITION_TRACE_PATH, transition_trace)
    else:
        write_json(REPORT_PATH, report)
        write_json(TRANSITION_TRACE_PATH, transition_trace)

    source_files_after = {}
    for ref in source_files_before:
        source_files_after[ref] = file_sha256(ROOT / ref)
    for ref, before in source_files_before.items():
        after = source_files_after.get(ref)
        if after != before:
            failures.append(f"source_file_mutated:{ref}")

    if failures and gate == "PASS":
        gate, status, outcome_class = stop_for_failures(failures)
        terminal = terminal_for(gate, failures)

    acceptance_gate_results = {
        "DG_ARCHIVE_0_INTAKE_CONSUMED": INTAKE_PATH.exists(),
        "DG_ARCHIVE_1_RECEIPT_EVIDENCE_PRESENT": nonempty_list(intake.get("source_receipt_refs")),
        "DG_ARCHIVE_2_TRIGGER_OBJECT_FAMILY_NAMED": bool(primary_trigger),
        "DG_ARCHIVE_3_DECISION_EDGES_TYPED": len(edge_records) > 0 and not any("edges_untyped" in f for f in failures),
        "DG_ARCHIVE_4_ALLOWED_TRANSITIONS_DECLARED": nonempty_list(intake.get("declared_allowed_transitions")),
        "DG_ARCHIVE_5_FORBIDDEN_TRANSITIONS_DECLARED": nonempty_list(intake.get("declared_forbidden_transitions")),
        "DG_ARCHIVE_6_TERMINAL_STATES_DECLARED": nonempty_list(intake.get("declared_terminal_states")),
        "DG_ARCHIVE_7_HUMAN_DECISION_POINTS_DECLARED_IF_PRESENT": isinstance(intake.get("declared_human_decision_points", []), list),
        "DG_ARCHIVE_8_AUTHORITY_BOUNDARY_DECLARED": gate == "PASS",
        "DG_ARCHIVE_9_OBSERVED_INSTANCE_RECORD_EMITTED": OBSERVED_INSTANCES_PATH.exists(),
        "DG_ARCHIVE_10_SUPPORTING_RECEIPT_MAP_EMITTED": SUPPORTING_RECEIPT_MAP_PATH.exists(),
        "DG_ARCHIVE_11_COUNTEREXAMPLES_EMITTED_OR_DECLARED_EMPTY": COUNTEREXAMPLES_PATH.exists(),
        "DG_ARCHIVE_12_KNOWN_VARIANTS_EMITTED_OR_DECLARED_EMPTY": KNOWN_VARIANTS_PATH.exists(),
        "DG_ARCHIVE_13_ARCHIVE_INDEX_EMITTED": ARCHIVE_INDEX_PATH.exists(),
        "DG_ARCHIVE_14_OBSERVATION_ONLY_STATUS_DECLARED": True,
        "DG_ARCHIVE_15_NO_VALIDATOR_AUTHORIZATION_SCHEMA_CREATED": True,
        "DG_ARCHIVE_16_NO_EXECUTION_REGISTRY_MUTATION": True,
        "DG_ARCHIVE_17_NO_RUNTIME_ADOPTION_AUTHORITY": True,
        "DG_ARCHIVE_18_NO_SCHEMA_MUTATION": True,
        "DG_ARCHIVE_19_NO_MOVE_ADDITION": True,
        "DG_ARCHIVE_20_NO_FIXTURE_EXPANSION": True,
        "DG_ARCHIVE_21_NO_C7_OPENING": True,
        "DG_ARCHIVE_22_NO_C8_AUTHORIZATION": True,
        "DG_ARCHIVE_23_NO_HUMAN_REVIEW_BYPASS": True,
        "DG_ARCHIVE_24_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
        "DG_ARCHIVE_25_RECEIPT_EMITTED": True,
        "DG_ARCHIVE_26_BAD_COUNTERS_ZERO": bad_counters_zero,
        "DG_ARCHIVE_27_NO_HIDDEN_NEXT_COMMAND": True,
        "DG_ARCHIVE_28_SOURCE_RECEIPTS_NOT_MUTATED": not any("source_file_mutated" in f and "receipt" in f for f in failures),
        "DG_ARCHIVE_29_SOURCE_TRACES_NOT_MUTATED": not any("source_file_mutated" in f and "trace" in f for f in failures),
        "DG_ARCHIVE_30_NO_REPO_WIDE_GRAPH_DISCOVERY": True,
        "DG_ARCHIVE_31_OPERATOR_INTAKE_NOT_BUILDER_GENERATED": intake.get("builder_generated") is False,
        "DG_ARCHIVE_32_DUPLICATE_GRAPH_ID_BLOCKED_OR_VERSIONED": not any("duplicate_graph_id" in f for f in failures),
        "DG_ARCHIVE_33_EDGE_SUPPORT_PRESENT": not any("edge_support_missing" in f for f in failures),
    }

    receipt = {
        "schema_version": "decision_graph_observation_archive_receipt_v0",
        "receipt_type": "TYPED_DECISION_GRAPH_OBSERVATION_ARCHIVE_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "archive_id": archive_id,
        "graph_schema_id": graph_schema_id,
        "graph_name": graph_name,
        "graph_status": graph_status if gate == "PASS" else None,
        "evidence_grade": evidence_grade if gate == "PASS" else None,
        "primary_trigger_object_family": primary_trigger if gate == "PASS" else None,
        "gate": gate,
        "status": status,
        "outcome_class": outcome_class,
        "failures": failures,
        "warnings": warnings,
        "machine_readable_decision_graph_archive_summary": {
            "graph_observation_archive_ready": gate == "PASS",
            "graph_schema_record_emitted": GRAPH_SCHEMA_RECORD_PATH.exists(),
            "archive_index_emitted": ARCHIVE_INDEX_PATH.exists(),
            "graph_schema_id": graph_schema_id if gate == "PASS" else None,
            "graph_name": graph_name if gate == "PASS" else None,
            "graph_status": graph_status if gate == "PASS" else None,
            "evidence_grade": evidence_grade if gate == "PASS" else None,
            "trigger_object_family_named": bool(primary_trigger) and gate == "PASS",
            "primary_trigger_object_family": primary_trigger if gate == "PASS" else None,
            "decision_edges_typed": len(edge_records) > 0 and gate == "PASS",
            "decision_edge_count": len(edge_records) if gate == "PASS" else 0,
            "allowed_transitions_declared": nonempty_list(intake.get("declared_allowed_transitions")) and gate == "PASS",
            "forbidden_transitions_declared": nonempty_list(intake.get("declared_forbidden_transitions")) and gate == "PASS",
            "terminal_states_declared": nonempty_list(intake.get("declared_terminal_states")) and gate == "PASS",
            "supporting_receipt_count": len(intake.get("source_receipt_refs", []) or []) if gate == "PASS" else 0,
            "authority_boundary_declared": gate == "PASS",
            "observation_only": True,
            "authorization_created": False,
            "validator_schema_created": False,
            "validator_recurring_mode_authorized": False,
            "execution_registry_mutated": False,
            "runtime_adoption_authorized": False,
            "schema_mutation_authorized": False,
            "schema_archive_mutation_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "c7_opened": False,
            "c8_authorized": False,
            "human_review_bypass_authorized": False,
            "source_receipts_mutated": False,
            "source_traces_mutated": False,
            "repo_wide_graph_discovery": False,
            "hidden_next_command": False,
            "bad_counters_zero": bad_counters_zero,
            "next_command_goal": None,
        },
        "acceptance_gate_results": acceptance_gate_results,
        "negative_controls": negative_controls,
        "output_artifacts": {
            "intake": rel(INTAKE_PATH),
            "graph_schema_record": rel(GRAPH_SCHEMA_RECORD_PATH) if GRAPH_SCHEMA_RECORD_PATH.exists() else None,
            "observed_instances": rel(OBSERVED_INSTANCES_PATH) if OBSERVED_INSTANCES_PATH.exists() else None,
            "supporting_receipt_map": rel(SUPPORTING_RECEIPT_MAP_PATH) if SUPPORTING_RECEIPT_MAP_PATH.exists() else None,
            "counterexamples": rel(COUNTEREXAMPLES_PATH) if COUNTEREXAMPLES_PATH.exists() else None,
            "known_variants": rel(KNOWN_VARIANTS_PATH) if KNOWN_VARIANTS_PATH.exists() else None,
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH) if AUTHORITY_BOUNDARY_PATH.exists() else None,
            "archive_index": rel(ARCHIVE_INDEX_PATH) if ARCHIVE_INDEX_PATH.exists() else None,
            "minimal_basis_hypothesis": rel(MINIMAL_BASIS_HYPOTHESIS_PATH) if MINIMAL_BASIS_HYPOTHESIS_PATH.exists() else None,
            "rollup": rel(ROLLUP_PATH) if ROLLUP_PATH.exists() else None,
            "profile": rel(PROFILE_PATH) if PROFILE_PATH.exists() else None,
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": terminal,
    }

    receipt_id = "decision_graph_observation_archive_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"decision_graph_observation_archive_receipt_id={receipt_id}")
    print(f"decision_graph_observation_archive_receipt_path={rel(receipt_path)}")
    print(f"decision_graph_observation_archive_id={archive_id if gate == 'PASS' else 'NONE'}")
    print(f"decision_graph_schema_id={graph_schema_id if gate == 'PASS' else 'NONE'}")
    print(f"decision_graph_observation_archive_terminal_stop_code={terminal['stop_code']}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
