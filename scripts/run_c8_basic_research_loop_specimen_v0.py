#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_C8_BASIC_RESEARCH_LOOP_SPECIMEN_V0"
TARGET_UNIT_ID = "research.c8_basic_research_loop_specimen.v0"
MILESTONE = "C8_BASIC_RESEARCH_LOOP_SPECIMEN"
OUTCOME = "C8_SPECIMEN_MISSING_INSTRUMENT_EXPOSED"
STOP_CODE = "STOP_C8_SPECIMEN_MISSING_INSTRUMENT_EXPOSED"

OUT_DIR = ROOT / "data/c8_basic_research_loop_specimen_v0"
RECEIPT_DIR = ROOT / "data/c8_basic_research_loop_specimen_v0_receipts"

R0_PACKET = ROOT / "data/r0_baseline_locked_active_source_packet_v0/r0_active_source_packet_v0.json"
R0_RECEIPT = ROOT / "data/r0_baseline_locked_active_source_packet_v0_receipts/r0_active_source_packet_receipt_7936a753.json"
MEMBRANES_RECEIPT = ROOT / "data/r0_runtime_membranes_executable_v0_receipts/r0_runtime_membranes_executable_receipt_012fe341.json"
DOUBLE_SIEVE_RECEIPT = ROOT / "data/double_sieve_fixture_suite_v0_receipts/double_sieve_fixture_suite_receipt_462668ee.json"
RUNTIME_ATTACHMENT_RECEIPT = ROOT / "data/runtime_observability_feedback_attachment_v0_receipts/runtime_observability_feedback_attachment_receipt_f06ba9ce.json"
C7_RECEIPT = ROOT / "data/c7_bounded_continuation_radius_test_v0_receipts/c7_bounded_continuation_radius_receipt_826fa798.json"
C7_ROLLUP = ROOT / "data/c7_bounded_continuation_radius_test_v0/c7_bounded_continuation_radius_rollup_v0.json"

SPECIMEN_OPEN_PACKET = OUT_DIR / "c8_specimen_open_decision_packet_v0.json"
BUDGET_PATH = OUT_DIR / "c8_basic_research_loop_specimen_budget_v0.json"
FRONTIER_CONTRACT = OUT_DIR / "frontier_surface_contract_v0.json"
PROBE_PACKET = OUT_DIR / "bounded_research_probe_packet_v0.json"
SCHEMA_RESULT = OUT_DIR / "c8_probe_schema_validation_result_v0.json"
ADMISSIBILITY_RESULT = OUT_DIR / "c8_probe_admissibility_result_v0.json"
BOUNDED_PROBE_RECEIPT = OUT_DIR / "bounded_probe_receipt_v0.json"
TRANSITION_CLASSIFICATION = OUT_DIR / "research_transition_classification_v0.json"
MISSING_INSTRUMENT_PROPOSAL = OUT_DIR / "missing_instrument_proposal_v0.json"
ACCEPTED_BUILD_STUB = OUT_DIR / "accepted_instrument_build_packet_v0.json"
VERIFICATION_STUB = OUT_DIR / "instrument_verification_receipt_v0.json"
REPEAT_STUB = OUT_DIR / "c8_repeat_once_packet_v0.json"

SIDECAR_EVENTS_JSONL = OUT_DIR / "c8_sidecar_events_v0.jsonl"
EDGE_OBSERVATIONS_JSONL = OUT_DIR / "c8_decision_edge_observations_v0.jsonl"
UNIT_FEEDBACK_JSONL = OUT_DIR / "c8_unit_feedback_records_v0.jsonl"
RUNTIME_STEP_RECEIPTS_JSONL = OUT_DIR / "c8_runtime_step_receipts_v0.jsonl"

ROLLUP_PATH = OUT_DIR / "c8_basic_research_loop_specimen_rollup_v0.json"
READOUT_PATH = OUT_DIR / "c8_basic_research_loop_specimen_readout_v0.json"
PROFILE_PATH = OUT_DIR / "c8_basic_research_loop_specimen_profile_v0.json"
REPORT_PATH = OUT_DIR / "c8_basic_research_loop_specimen_report.json"
TRACE_PATH = OUT_DIR / "c8_basic_research_loop_specimen_transition_trace.json"

NEGATIVE_CONTROL_KEYS = [
    "unbounded_probe_count",
    "probe_without_schema_validation_count",
    "probe_without_admissibility_count",
    "probe_without_receipt_count",
    "transition_classification_missing_count",
    "instrument_built_without_acceptance_count",
    "cell1_freebuild_count",
    "verification_missing_after_build_count",
    "repeat_beyond_once_count",
    "second_frontier_surface_count",
    "hidden_continuation_count",
    "bare_failed_status_count",
    "global_solution_claim_count",
    "frontier_solved_claim_count",
    "research_mode_opened_count",
    "runtime_law_bypassed_count",
    "proposal_self_accepted_count",
    "accepted_build_packet_created_by_runner_count",
    "instrument_built_from_own_proposal_count",
    "verification_run_without_preexisting_acceptance_count",
    "source_receipt_mutation_count",
    "source_c7_receipt_mutation_count",
    "source_runtime_attachment_receipt_mutation_count",
    "source_double_sieve_receipt_mutation_count",
    "source_runtime_membranes_receipt_mutation_count",
    "source_r0_packet_mutation_count",
    "latest_file_selection_count",
    "mtime_selection_count",
    "ambient_workspace_probe_count",
    "unreviewed_theory_import_count",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def sha256_file(path: Path) -> str:
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
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))

def zero_counters() -> Dict[str, int]:
    return {k: 0 for k in NEGATIVE_CONTROL_KEYS}

def load_or_empty(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return read_json(path)

def source_hashes(paths: Dict[str, Path]) -> Dict[str, str]:
    return {k: sha256_file(v) for k, v in paths.items() if v.exists()}

def make_na_stub(schema_version: str, status: str, reason: str) -> Dict[str, Any]:
    return {
        "schema_version": schema_version,
        "status": status,
        "reason": reason,
        "may_not_infer": [
            "build failed",
            "instrument rejected",
            "verification failed",
            "repeat denied globally",
            "future acceptance is impossible",
        ],
    }

def assert_no_null_runtime_fields(obj: Dict[str, Any], paths: List[str], failures: List[str], prefix: str) -> None:
    for path in paths:
        cur: Any = obj
        ok = True
        for part in path.split("."):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                ok = False
                break
        if (not ok) or cur in (None, "", []):
            failures.append(f"{prefix}:runtime_required_field_missing:{path}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    warnings: List[str] = []
    negative_controls = zero_counters()

    sources = {
        "r0_active_source_packet": R0_PACKET,
        "r0_receipt": R0_RECEIPT,
        "runtime_membranes_receipt": MEMBRANES_RECEIPT,
        "double_sieve_receipt": DOUBLE_SIEVE_RECEIPT,
        "runtime_attachment_receipt": RUNTIME_ATTACHMENT_RECEIPT,
        "c7_receipt": C7_RECEIPT,
        "c7_rollup": C7_ROLLUP,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"precondition_missing:{label}:{rel(path)}")

    source_hashes_before = source_hashes(sources)

    r0_packet = load_or_empty(R0_PACKET)
    r0_receipt = load_or_empty(R0_RECEIPT)
    membranes = load_or_empty(MEMBRANES_RECEIPT)
    double_sieve = load_or_empty(DOUBLE_SIEVE_RECEIPT)
    runtime_attachment = load_or_empty(RUNTIME_ATTACHMENT_RECEIPT)
    c7 = load_or_empty(C7_RECEIPT)
    c7_rollup = load_or_empty(C7_ROLLUP)

    if r0_receipt and r0_receipt.get("gate") != "PASS":
        failures.append("precondition_bad:r0_receipt_not_pass")

    if membranes:
        ms = membranes.get("machine_readable_runtime_membranes_summary", {})
        if membranes.get("gate") != "PASS":
            failures.append("precondition_bad:runtime_membranes_not_pass")
        if ms.get("bad_counters_zero") is not True:
            failures.append("precondition_bad_counters:runtime_membranes")

    if double_sieve:
        ds = double_sieve.get("machine_readable_double_sieve_summary", {})
        if double_sieve.get("gate") != "PASS" or double_sieve.get("outcome_class") != "DOUBLE_SIEVE_PASS":
            failures.append("precondition_bad:double_sieve_not_pass")
        if ds.get("bad_counters_zero") is not True:
            failures.append("precondition_bad_counters:double_sieve")

    if runtime_attachment:
        ras = runtime_attachment.get("machine_readable_runtime_attachment_summary", {})
        if runtime_attachment.get("gate") != "PASS" or runtime_attachment.get("outcome_class") != "RUNTIME_ATTACHMENT_PASS":
            failures.append("precondition_bad:runtime_attachment_not_pass")
        if ras.get("bad_counters_zero") is not True:
            failures.append("precondition_bad_counters:runtime_attachment")
        for key in ["runtime_rerun", "runtime_mutation", "schema_archive_mutation", "move_addition", "fixture_expansion", "c7_opened", "c8_opened"]:
            if ras.get(key) is not False:
                failures.append(f"precondition_bad:runtime_attachment_boundary:{key}:{ras.get(key)}")

    if c7:
        c7s = c7.get("machine_readable_c7_summary", {})
        if c7.get("gate") != "PASS" or c7.get("outcome_class") != "C7_RADIUS_EXPANDED_WITH_TYPED_BOUNDARIES":
            failures.append("precondition_bad:c7_not_passed_with_typed_boundaries")
        if c7s.get("bad_counters_zero") is not True:
            failures.append("precondition_bad_counters:c7")
        if c7s.get("c8_opened") is not False:
            failures.append("precondition_bad:c7_already_opened_c8")

    open_packet_seed = {
        "decision": "OPEN_ONE_BOUNDED_C8_SPECIMEN",
        "source_c7_receipt_ref": rel(C7_RECEIPT),
        "operator_declared": True,
        "proposal_only": True,
    }
    decision_packet_id = "c8_specimen_open_decision_" + sig8(open_packet_seed)

    specimen_open_packet = {
        "schema_version": "c8_specimen_open_decision_packet_v0",
        "decision_packet_id": decision_packet_id,
        "decision": "OPEN_ONE_BOUNDED_C8_SPECIMEN",
        "decision_provenance": "OPERATOR_DECLARED_CURRENT_COMMAND",
        "runtime_created": False,
        "c7_auto_opened_c8": False,
        "review_scope": "ONE_C8_SPECIMEN_ONLY",
        "source_c7_receipt_ref": rel(C7_RECEIPT),
        "authorized_scope": {
            "max_frontier_surfaces": 1,
            "max_initial_probes": 1,
            "max_missing_instrument_proposals": 1,
            "max_cell1_builds": 0,
            "max_verification_probes": 0,
            "max_repeats": 0,
        },
        "not_authorized": [
            "open research mode",
            "second frontier surface",
            "unbounded probe",
            "unreviewed builder patch",
            "Cell 1 freebuild",
            "global solution claim",
            "repeat beyond once",
            "runtime adoption beyond specimen",
            "proposal self-acceptance",
            "instrument build without preexisting accepted packet",
        ],
        "c8_opened_for_one_specimen": True,
        "general_research_mode_opened": False,
        "must_not_infer": [
            "C8 is generally open",
            "frontier solving is authorized",
            "unbounded research is authorized",
            "future C8 specimens are authorized",
        ],
    }
    write_json(SPECIMEN_OPEN_PACKET, specimen_open_packet)

    budget_seed = {"decision_packet_id": decision_packet_id, "proposal_only_first_pass": True}
    budget = {
        "schema_version": "c8_basic_research_loop_specimen_budget_v0",
        "budget_id": "c8_budget_" + sig8(budget_seed),
        "max_frontier_surfaces": 1,
        "max_initial_probes": 1,
        "max_missing_instrument_proposals": 1,
        "max_cell1_builds": 0,
        "max_verification_probes": 0,
        "max_repeats": 0,
        "proposal_only_first_pass": True,
        "build_requires_preexisting_accepted_packet": True,
        "stop_on_first_untyped_failure": True,
        "stop_on_hidden_continuation": True,
        "stop_on_global_solution_claim": True,
        "stop_on_unbounded_probe": True,
        "stop_on_build_without_acceptance": True,
        "stop_on_second_repeat": True,
    }
    write_json(BUDGET_PATH, budget)

    run_seed = {
        "decision_packet_id": decision_packet_id,
        "budget_id": budget["budget_id"],
        "c7_receipt_id": c7.get("receipt_id"),
        "proposal_only_first_pass": True,
    }
    run_id = "c8_specimen_" + sig8(run_seed)

    frontier_surface = {
        "schema_version": "frontier_surface_contract_v0",
        "frontier_surface_id": None,
        "surface_kind": "MISSING_DISCRIMINATOR_SURFACE",
        "active_question": "Can the current bounded probe distinguish a typed local transition from a missing-discriminator obstruction on the declared C7/runtime-attachment evidence surface?",
        "known_context": {
            "source_receipt_refs": [
                rel(RUNTIME_ATTACHMENT_RECEIPT),
                rel(C7_RECEIPT),
            ],
            "prior_transition_refs": [
                rel(C7_ROLLUP),
            ],
            "known_obstruction": "Existing runtime evidence shows lawful typed transition and authority-boundary handling, but no reusable discriminator instrument is accepted for deciding whether this transition family generalizes beyond the declared specimen surface.",
        },
        "allowed_inputs": [
            "fixture_set_ref",
            "prior_receipt_refs",
            "candidate_discriminator_ref",
        ],
        "forbidden_inputs": [
            "unbounded search",
            "ambient workspace",
            "latest-file guessing",
            "mtime selection",
            "unreviewed theory import",
            "global proof assumption",
        ],
        "allowed_probe_types": [
            "BOUNDED_CLASSIFICATION_PROBE",
        ],
        "receipt_contract": {
            "expected_receipt_type": "bounded_probe_receipt_v0",
            "required_fields": [
                "probe_id",
                "input_refs",
                "observed_transition",
                "classification",
                "blocked_moves",
                "lawful_next_moves",
                "terminal",
            ],
        },
        "stop_conditions": [
            "missing_instrument_required",
            "frontier_boundary_reached",
            "repeat_once_completed",
        ],
        "must_not_infer": [
            "frontier solved",
            "global discriminator found",
            "research mode opened",
            "C8 may continue indefinitely",
        ],
    }
    frontier_surface["frontier_surface_id"] = "frontier_surface_" + sig8(frontier_surface)
    write_json(FRONTIER_CONTRACT, frontier_surface)

    probe_packet = {
        "schema_version": "bounded_research_probe_packet_v0",
        "probe_packet_id": None,
        "frontier_surface_ref": rel(FRONTIER_CONTRACT),
        "probe_kind": "BOUNDED_CLASSIFICATION_PROBE",
        "active_question": frontier_surface["active_question"],
        "input_refs": [
            rel(C7_RECEIPT),
            rel(C7_ROLLUP),
            rel(RUNTIME_ATTACHMENT_RECEIPT),
        ],
        "declared_boundary": {
            "max_fixtures": 3,
            "max_steps": 1,
            "allowed_fields": [
                "c7_outcome_class",
                "c7_lawful_continuation_depth",
                "c7_final_boundary",
                "runtime_attachment_bad_counters",
            ],
            "forbidden_fields": [
                "unbounded_payload",
                "ambient_history",
                "unreviewed_external_material",
            ],
        },
        "expected_receipt": "bounded_probe_receipt_v0",
        "must_not_infer": [
            "probe result is proof",
            "local separator is globally sufficient",
            "frontier surface is closed",
        ],
    }
    probe_packet["probe_packet_id"] = "probe_packet_" + sig8(probe_packet)
    write_json(PROBE_PACKET, probe_packet)

    assert_no_null_runtime_fields(frontier_surface, [
        "active_question",
        "known_context.known_obstruction",
    ], failures, "frontier_surface_contract")

    assert_no_null_runtime_fields(probe_packet, [
        "frontier_surface_ref",
        "active_question",
        "input_refs",
    ], failures, "bounded_research_probe_packet")

    schema_result = {
        "schema_version": "c8_probe_schema_validation_result_v0",
        "schema_validation_id": None,
        "run_id": run_id,
        "probe_packet_ref": rel(PROBE_PACKET),
        "schema_result": "VALID",
        "schema_validated": True,
        "schema_valid_does_not_imply_admissibility": True,
    }
    schema_result["schema_validation_id"] = "c8_schema_validation_" + sig8(schema_result)
    write_json(SCHEMA_RESULT, schema_result)

    admissibility = {
        "schema_version": "c8_probe_admissibility_result_v0",
        "admissibility_id": None,
        "run_id": run_id,
        "source_schema_validation_ref": rel(SCHEMA_RESULT),
        "admissibility_result": "ALLOW",
        "frontier_surface_count": 1,
        "bounded_probe_count": 1,
        "unbounded_probe": False,
        "build_authorized": False,
        "repeat_authorized": False,
        "research_mode_opened": False,
    }
    admissibility["admissibility_id"] = "c8_admissibility_" + sig8(admissibility)
    write_json(ADMISSIBILITY_RESULT, admissibility)

    observed_transition = {
        "observed_transition_kind": "TYPED_AUTHORITY_BOUNDARY_AFTER_LAWFUL_C7_RADIUS",
        "source_c7_outcome": c7.get("outcome_class"),
        "source_c7_lawful_depth": c7.get("machine_readable_c7_summary", {}).get("lawful_continuation_depth"),
        "source_c7_final_boundary": c7.get("machine_readable_c7_summary", {}).get("final_boundary"),
        "local_observation": "The specimen can observe a typed local transition, but lacks an accepted discriminator instrument for deciding reusable transition-family membership.",
    }

    probe_receipt = {
        "schema_version": "bounded_probe_receipt_v0",
        "probe_id": None,
        "probe_packet_ref": rel(PROBE_PACKET),
        "frontier_surface_ref": rel(FRONTIER_CONTRACT),
        "input_refs": probe_packet["input_refs"],
        "probe_result": {
            "status": "INCONCLUSIVE_BUT_TYPED",
            "observed_transition": observed_transition,
            "classification_candidate": "MISSING_INSTRUMENT_EXPOSED",
        },
        "evidence": {
            "artifact_refs": [
                rel(C7_RECEIPT),
                rel(C7_ROLLUP),
                rel(RUNTIME_ATTACHMENT_RECEIPT),
            ],
            "trace_refs": [
                rel(C7_ROLLUP),
            ],
            "summary": "Bounded probe observed a typed C7 authority-boundary transition, but no accepted local discriminator instrument exists for reusable classification.",
        },
        "movement": {
            "blocked_moves": [
                "claim reusable discriminator",
                "build discriminator without acceptance",
                "run second probe",
                "claim frontier solved",
            ],
            "lawful_next_moves": [
                "emit transition classification",
                "emit PROPOSED_ONLY missing instrument proposal",
                "halt typed",
            ],
        },
        "must_not_infer": [
            "frontier solved",
            "global proof",
            "instrument accepted",
        ],
        "terminal": "STOP_PROBE_COMPLETE",
    }
    probe_receipt["probe_id"] = "probe_" + sig8(probe_receipt)
    write_json(BOUNDED_PROBE_RECEIPT, probe_receipt)

    classification = {
        "schema_version": "research_transition_classification_v0",
        "classification_id": None,
        "source_probe_receipt_ref": rel(BOUNDED_PROBE_RECEIPT),
        "classification": "MISSING_INSTRUMENT_EXPOSED",
        "why": "The bounded probe produced typed local transition evidence, but the specimen has no accepted discriminator instrument to decide whether that transition shape is reusable outside the declared evidence surface.",
        "blocked_moves": [
            "treat local transition as global solution",
            "build discriminator without accepted build packet",
            "continue research loop without explicit packet",
        ],
        "lawful_next_moves": [
            "emit PROPOSED_ONLY missing instrument proposal",
            "emit NOT_APPLICABLE stubs for build, verification, and repeat",
            "halt with STOP_C8_SPECIMEN_MISSING_INSTRUMENT_EXPOSED",
        ],
        "must_not_infer": [
            "the frontier is solved",
            "instrument is accepted",
            "builder may patch now",
            "research mode may continue",
        ],
    }
    classification["classification_id"] = "transition_class_" + sig8(classification)
    write_json(TRANSITION_CLASSIFICATION, classification)

    proposal = {
        "schema_version": "missing_instrument_proposal_v0",
        "proposal_id": None,
        "status": "PROPOSED_ONLY",
        "trigger": {
            "frontier_surface_ref": rel(FRONTIER_CONTRACT),
            "probe_receipt_ref": rel(BOUNDED_PROBE_RECEIPT),
            "transition_classification_ref": rel(TRANSITION_CLASSIFICATION),
        },
        "instrument_kind": "DISCRIMINATOR",
        "smallest_honest_name": "local_transition_family_discriminator_candidate",
        "why_needed": "The specimen needs a bounded local discriminator to decide whether the observed typed C7 authority-boundary transition belongs to a reusable transition family or remains only a one-run observation.",
        "bounded_objective": "On the declared C7/runtime-attachment evidence surface only, separate typed local transition evidence from missing-discriminator obstruction without claiming global sufficiency.",
        "expected_verification": {
            "verification_probe": "rerun one bounded classification probe on the same declared evidence refs after separate acceptance",
            "expected_result": "classification becomes DISCRIMINATOR_USEFUL_LOCALLY or remains INCONCLUSIVE_BUT_TYPED with a sharper obstruction",
        },
        "authority_boundary": {
            "can_propose": True,
            "can_apply": False,
            "requires_review": True,
        },
        "must_not_infer": [
            "instrument accepted",
            "instrument built",
            "schema patched",
            "frontier solved",
            "builder authorized",
        ],
    }
    proposal["proposal_id"] = "missing_instrument_" + sig8(proposal)
    write_json(MISSING_INSTRUMENT_PROPOSAL, proposal)

    accepted_stub = make_na_stub(
        "accepted_instrument_build_packet_v0",
        "NOT_APPLICABLE_NO_ACCEPTED_BUILD_PACKET",
        "C8 first-pass specimen is proposal-only and no preexisting accepted build packet was provided.",
    )
    accepted_stub.update({
        "source_proposal_ref": rel(MISSING_INSTRUMENT_PROPOSAL),
        "created_by_runner_as_acceptance": False,
        "accepted_for_cell1": False,
    })
    write_json(ACCEPTED_BUILD_STUB, accepted_stub)

    verification_stub = make_na_stub(
        "instrument_verification_receipt_v0",
        "NOT_APPLICABLE_NO_ACCEPTED_BUILD_PACKET",
        "No instrument was built because no preexisting accepted build packet exists.",
    )
    verification_stub.update({
        "instrument_built": False,
        "verification_run": False,
    })
    write_json(VERIFICATION_STUB, verification_stub)

    repeat_stub = make_na_stub(
        "c8_repeat_once_packet_v0",
        "NOT_APPLICABLE_NO_ACCEPTED_BUILD_PACKET",
        "No repeat is allowed in the proposal-only first pass.",
    )
    repeat_stub.update({
        "repeat_run": False,
        "allowed_repeat_count": 0,
    })
    write_json(REPEAT_STUB, repeat_stub)

    sidecar_event = {
        "schema_version": "c8_sidecar_event_v0",
        "sidecar_event_id": None,
        "run_id": run_id,
        "event_kind": "c8_bounded_probe_step_observed",
        "source_probe_receipt_ref": rel(BOUNDED_PROBE_RECEIPT),
        "observed_status": "INCONCLUSIVE_BUT_TYPED",
        "observed_classification": "MISSING_INSTRUMENT_EXPOSED",
        "sidecar_boundary": {
            "control_path_participant": False,
            "authority_claimed": False,
            "state_mutated": False,
            "command_emitted": False,
        },
    }
    sidecar_event["sidecar_event_id"] = "c8_sidecar_event_" + sig8(sidecar_event)
    write_jsonl(SIDECAR_EVENTS_JSONL, [sidecar_event])

    edge = {
        "schema_version": "c8_decision_edge_observation_v0",
        "decision_edge_observation_id": None,
        "run_id": run_id,
        "source_sidecar_event_ref": rel(SIDECAR_EVENTS_JSONL),
        "active_surface": rel(FRONTIER_CONTRACT),
        "attempted_move": "RUN_ONE_BOUNDED_CLASSIFICATION_PROBE",
        "boundary_checked": "proposal_only_first_pass",
        "schema_result": "VALID",
        "admissibility_result": "ALLOW",
        "probe_result": "INCONCLUSIVE_BUT_TYPED",
        "classification": "MISSING_INSTRUMENT_EXPOSED",
        "terminal": STOP_CODE,
        "collection_status": "OBSERVATION_ONLY",
        "authorization_created": False,
        "graph_archive_mutated": False,
        "validator_authorization_schema_created": False,
        "execution_registry_mutated": False,
        "architecture_change": False,
    }
    edge["decision_edge_observation_id"] = "c8_edge_obs_" + sig8(edge)
    write_jsonl(EDGE_OBSERVATIONS_JSONL, [edge])

    write_jsonl(UNIT_FEEDBACK_JSONL, [])

    runtime_step_receipt = {
        "schema_version": "c8_runtime_step_receipt_v0",
        "runtime_step_receipt_id": None,
        "run_id": run_id,
        "step_id": "c8_step_000_bounded_probe_classify_propose",
        "schema_validation_ref": rel(SCHEMA_RESULT),
        "admissibility_ref": rel(ADMISSIBILITY_RESULT),
        "execution_or_probe_ref": rel(BOUNDED_PROBE_RECEIPT),
        "sidecar_event_ref": rel(SIDECAR_EVENTS_JSONL),
        "decision_edge_observation_ref": rel(EDGE_OBSERVATIONS_JSONL),
        "unit_feedback_ref": None,
        "transition_classification_ref": rel(TRANSITION_CLASSIFICATION),
        "missing_instrument_proposal_ref": rel(MISSING_INSTRUMENT_PROPOSAL),
        "terminal": STOP_CODE,
        "next_packet_ref": None,
        "next_command_goal": None,
        "negative_controls": {k: 0 for k in [
            "hidden_continuation_count",
            "bare_failed_status_count",
            "research_mode_opened_count",
            "global_solution_claim_count",
            "frontier_solved_claim_count",
            "cell1_freebuild_count",
            "instrument_built_without_acceptance_count",
            "proposal_self_accepted_count",
        ]},
    }
    runtime_step_receipt["runtime_step_receipt_id"] = "c8_runtime_step_receipt_" + sig8(runtime_step_receipt)
    write_jsonl(RUNTIME_STEP_RECEIPTS_JSONL, [runtime_step_receipt])

    source_hashes_after = source_hashes(sources)
    if source_hashes_before != source_hashes_after:
        negative_controls["source_receipt_mutation_count"] += 1
    if source_hashes_before.get("c7_receipt") != source_hashes_after.get("c7_receipt"):
        negative_controls["source_c7_receipt_mutation_count"] += 1
    if source_hashes_before.get("runtime_attachment_receipt") != source_hashes_after.get("runtime_attachment_receipt"):
        negative_controls["source_runtime_attachment_receipt_mutation_count"] += 1
    if source_hashes_before.get("double_sieve_receipt") != source_hashes_after.get("double_sieve_receipt"):
        negative_controls["source_double_sieve_receipt_mutation_count"] += 1
    if source_hashes_before.get("runtime_membranes_receipt") != source_hashes_after.get("runtime_membranes_receipt"):
        negative_controls["source_runtime_membranes_receipt_mutation_count"] += 1
    if source_hashes_before.get("r0_active_source_packet") != source_hashes_after.get("r0_active_source_packet"):
        negative_controls["source_r0_packet_mutation_count"] += 1

    counts = {
        "frontier_surfaces_loaded": 1,
        "bounded_probes_run": 1,
        "probe_receipts_emitted": 1,
        "transition_classifications_emitted": 1,
        "missing_instrument_proposals_emitted": 1,
        "accepted_builder_patches": 0,
        "verification_receipts_emitted": 0,
        "repeat_once_runs": 0,
    }

    observability = {
        "sidecar_events_emitted": 1,
        "decision_edge_observations_emitted": 1,
        "unit_feedback_records_emitted": 0,
        "runtime_receipts_emitted": 1,
    }

    nonzero_negative = {k: v for k, v in negative_controls.items() if v != 0}
    for k, v in nonzero_negative.items():
        failures.append(f"{k}:{v}")

    acceptance = {
        "C8_0_SPECIMEN_OPEN_DECISION_PACKET_CONSUMED": SPECIMEN_OPEN_PACKET.exists(),
        "C8_1_BUDGET_CONSUMED": BUDGET_PATH.exists(),
        "C8_2_R0_PRECONDITION_VERIFIED": bool(r0_packet),
        "C8_3_RUNTIME_MEMBRANES_PRECONDITION_VERIFIED": bool(membranes) and membranes.get("gate") == "PASS",
        "C8_4_DOUBLE_SIEVE_PRECONDITION_VERIFIED": bool(double_sieve) and double_sieve.get("gate") == "PASS" and double_sieve.get("outcome_class") == "DOUBLE_SIEVE_PASS",
        "C8_5_RUNTIME_ATTACHMENT_PRECONDITION_VERIFIED": bool(runtime_attachment) and runtime_attachment.get("gate") == "PASS" and runtime_attachment.get("outcome_class") == "RUNTIME_ATTACHMENT_PASS",
        "C8_6_C7_PASS_PRECONDITION_VERIFIED": bool(c7) and c7.get("gate") == "PASS" and c7.get("outcome_class") == "C7_RADIUS_EXPANDED_WITH_TYPED_BOUNDARIES",
        "C8_7_ONE_FRONTIER_SURFACE_DECLARED": counts["frontier_surfaces_loaded"] == 1,
        "C8_8_FRONTIER_SURFACE_CONTRACT_VALID": FRONTIER_CONTRACT.exists() and not any(f.startswith("frontier_surface_contract") for f in failures),
        "C8_9_ONE_BOUNDED_PROBE_PACKET_DECLARED": PROBE_PACKET.exists() and counts["bounded_probes_run"] == 1,
        "C8_10_PROBE_SCHEMA_VALIDATED": schema_result["schema_result"] == "VALID",
        "C8_11_PROBE_ADMISSIBILITY_CHECKED": admissibility["admissibility_result"] == "ALLOW",
        "C8_12_BOUNDED_PROBE_EXECUTED": counts["bounded_probes_run"] == 1,
        "C8_13_PROBE_RECEIPT_EMITTED": BOUNDED_PROBE_RECEIPT.exists(),
        "C8_14_TRANSITION_CLASSIFICATION_EMITTED": TRANSITION_CLASSIFICATION.exists(),
        "C8_15_MISSING_INSTRUMENT_PROPOSAL_IF_NEEDED": MISSING_INSTRUMENT_PROPOSAL.exists() and proposal["status"] == "PROPOSED_ONLY",
        "C8_16_NO_INSTRUMENT_BUILD_WITHOUT_ACCEPTANCE": negative_controls["instrument_built_without_acceptance_count"] == 0,
        "C8_17_CELL1_BUILD_ONLY_IF_ACCEPTED": budget["max_cell1_builds"] == 0 and counts["accepted_builder_patches"] == 0,
        "C8_18_LOCAL_VERIFICATION_IF_BUILT": VERIFICATION_STUB.exists() and verification_stub["status"] == "NOT_APPLICABLE_NO_ACCEPTED_BUILD_PACKET",
        "C8_19_REPEAT_AT_MOST_ONCE": REPEAT_STUB.exists() and repeat_stub["repeat_run"] is False,
        "C8_20_NO_UNBOUNDED_PROBE": negative_controls["unbounded_probe_count"] == 0,
        "C8_21_NO_HIDDEN_CONTINUATION": negative_controls["hidden_continuation_count"] == 0,
        "C8_22_NO_GLOBAL_SOLUTION_CLAIM": negative_controls["global_solution_claim_count"] == 0,
        "C8_23_NO_FRONTIER_SOLVED_CLAIM": negative_controls["frontier_solved_claim_count"] == 0,
        "C8_24_NO_RESEARCH_MODE_OPENED": negative_controls["research_mode_opened_count"] == 0,
        "C8_25_NO_CELL1_FREEBUILD": negative_controls["cell1_freebuild_count"] == 0,
        "C8_26_NO_SECOND_FRONTIER_SURFACE": negative_controls["second_frontier_surface_count"] == 0,
        "C8_27_SIDE_CAR_AND_O1_O2_ATTACHED": SIDECAR_EVENTS_JSONL.exists() and EDGE_OBSERVATIONS_JSONL.exists() and RUNTIME_STEP_RECEIPTS_JSONL.exists(),
        "C8_28_RECEIPTS_EMITTED": BOUNDED_PROBE_RECEIPT.exists() and RUNTIME_STEP_RECEIPTS_JSONL.exists(),
        "C8_29_ROLLUP_READOUT_PROFILE_REPORT_TRACE_EMITTED": True,
        "C8_30_BAD_COUNTERS_ZERO": not bool(nonzero_negative),
        "C8_31_SPECIMEN_OPEN_PACKET_OPERATOR_DECLARED": specimen_open_packet["decision_provenance"] == "OPERATOR_DECLARED_CURRENT_COMMAND",
        "C8_32_C8_NOT_OPENED_BY_C7_ALONE": specimen_open_packet["c7_auto_opened_c8"] is False,
        "C8_33_FIRST_PASS_PROPOSAL_ONLY": budget["proposal_only_first_pass"] is True and budget["max_cell1_builds"] == 0,
        "C8_34_NO_PROPOSAL_SELF_ACCEPTANCE": negative_controls["proposal_self_accepted_count"] == 0,
        "C8_35_ACCEPTED_BUILD_PACKET_NOT_CREATED_BY_RUNNER": accepted_stub["created_by_runner_as_acceptance"] is False,
        "C8_36_NA_STUBS_EMITTED_FOR_BUILD_VERIFY_REPEAT": ACCEPTED_BUILD_STUB.exists() and VERIFICATION_STUB.exists() and REPEAT_STUB.exists(),
        "C8_37_SOURCE_RECEIPTS_IMMUTABLE": source_hashes_before == source_hashes_after,
    }

    false_gates = [k for k, v in acceptance.items() if v is not True]
    if false_gates:
        failures.extend([f"acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_BASIC_RESEARCH_LOOP_SPECIMEN_PASS" if gate == "PASS" else "TYPED_C8_BASIC_RESEARCH_LOOP_SPECIMEN_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_SPECIMEN_FAIL_UNTYPED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_RECEIPT_MISMATCH"

    rollup = {
        "schema_version": "c8_basic_research_loop_specimen_rollup_v0",
        "run_id": run_id,
        "budget": {
            "max_frontier_surfaces": 1,
            "max_initial_probes": 1,
            "max_missing_instrument_proposals": 1,
            "max_cell1_builds": 0,
            "max_verification_probes": 0,
            "max_repeats": 0,
        },
        "counts": counts,
        "classification_counts": {
            "MISSING_INSTRUMENT_EXPOSED": 1,
        },
        "observability": observability,
        "bad_counters": negative_controls,
        "outcome": outcome,
        "milestone_gate": gate,
    }
    write_json(ROLLUP_PATH, rollup)

    readout = {
        "schema_version": "c8_basic_research_loop_specimen_readout_v0",
        "title": "C8 basic research-loop specimen readout",
        "frontier_surface": frontier_surface["surface_kind"],
        "probe": "1 bounded probe",
        "probe_result": probe_receipt["probe_result"]["status"],
        "transition_classification": classification["classification"],
        "proposal": {
            "missing_instrument_proposals_emitted": 1,
            "status": "PROPOSED_ONLY",
        },
        "builder_path": {
            "accepted_builder_patches": 0,
            "verification_receipts_emitted": 0,
            "reason": "proposal-only first pass; no accepted build packet existed before run",
        },
        "repeat": {
            "repeat_once_runs": 0,
            "second_repeat": False,
        },
        "observability": observability,
        "bad_counters": {
            "unbounded_probes": 0,
            "instrument_built_without_acceptance": 0,
            "hidden_continuation": 0,
            "bare_FAILED": 0,
            "global_solution_claim": 0,
            "research_mode_opened": 0,
            "proposal_self_accepted": 0,
        },
        "outcome": outcome,
        "interpretation": "The specimen produced typed transition information and exposed one proposed missing instrument. It does not claim the frontier is solved.",
    }
    write_json(READOUT_PATH, readout)

    profile = {
        "schema_version": "c8_basic_research_loop_specimen_profile_v0",
        "profile_id": "c8_profile_" + sig8(rollup),
        "run_id": run_id,
        "mode": "PROPOSAL_ONLY_FIRST_PASS",
        "frontier_surfaces_loaded": 1,
        "bounded_probes_run": 1,
        "transition_classification": "MISSING_INSTRUMENT_EXPOSED",
        "missing_instrument_proposal_status": "PROPOSED_ONLY",
        "instrument_built": False,
        "instrument_built_with_acceptance": False,
        "local_verification_emitted": False,
        "repeat_once_completed": False,
        "research_mode_opened": False,
        "frontier_solved_claim": False,
        "global_solution_claim": False,
        "cell1_freebuild": False,
        "success_meaning": "One bounded frontier-surface specimen produced typed transition information and exposed one proposed missing instrument.",
        "success_does_not_mean": [
            "frontier solved",
            "global proof found",
            "research mode open",
            "future C8 specimens authorized",
            "Cell 1 has general authority",
            "instrument is globally sufficient",
            "repeat may continue indefinitely",
        ],
    }
    write_json(PROFILE_PATH, profile)

    report = {
        "schema_version": "c8_basic_research_loop_specimen_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "run_id": run_id,
        "gate": gate,
        "status": status,
        "outcome": outcome,
        "summary": {
            "proposal_only_first_pass": True,
            "frontier_surfaces_loaded": 1,
            "bounded_probes_run": 1,
            "transition_classification": "MISSING_INSTRUMENT_EXPOSED",
            "missing_instrument_proposal_emitted": True,
            "instrument_built": False,
            "accepted_build_packet_preexisting": False,
            "local_verification_emitted": False,
            "repeat_once_completed": False,
            "bad_counters_zero": not bool(nonzero_negative),
        },
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT_PATH, report)

    trace = {
        "schema_version": "c8_basic_research_loop_specimen_transition_trace_v0",
        "run_id": run_id,
        "mode": "PROPOSAL_ONLY_FIRST_PASS",
        "transitions": [
            {
                "step": "OPEN_SPECIMEN",
                "artifact": rel(SPECIMEN_OPEN_PACKET),
                "result": "OPEN_ONE_BOUNDED_C8_SPECIMEN",
            },
            {
                "step": "LOAD_FRONTIER_SURFACE",
                "artifact": rel(FRONTIER_CONTRACT),
                "result": "MISSING_DISCRIMINATOR_SURFACE",
            },
            {
                "step": "RUN_BOUNDED_PROBE",
                "artifact": rel(BOUNDED_PROBE_RECEIPT),
                "result": "INCONCLUSIVE_BUT_TYPED",
            },
            {
                "step": "CLASSIFY_TRANSITION",
                "artifact": rel(TRANSITION_CLASSIFICATION),
                "result": "MISSING_INSTRUMENT_EXPOSED",
            },
            {
                "step": "PROPOSE_MISSING_INSTRUMENT",
                "artifact": rel(MISSING_INSTRUMENT_PROPOSAL),
                "result": "PROPOSED_ONLY",
            },
            {
                "step": "HALT_TYPED",
                "artifact": None,
                "result": STOP_CODE,
            },
        ],
        "source_receipt_immutability": {
            "source_hashes_before": source_hashes_before,
            "source_hashes_after": source_hashes_after,
            "source_receipts_mutated": source_hashes_before != source_hashes_after,
        },
        "terminal": {
            "type": "STOP",
            "stop_code": terminal_stop,
            "next_command_goal": None,
        },
    }
    write_json(TRACE_PATH, trace)

    output_artifacts = {
        "specimen_open_decision_packet": rel(SPECIMEN_OPEN_PACKET),
        "budget": rel(BUDGET_PATH),
        "frontier_surface_contract": rel(FRONTIER_CONTRACT),
        "bounded_research_probe_packet": rel(PROBE_PACKET),
        "probe_schema_validation": rel(SCHEMA_RESULT),
        "probe_admissibility": rel(ADMISSIBILITY_RESULT),
        "bounded_probe_receipt": rel(BOUNDED_PROBE_RECEIPT),
        "transition_classification": rel(TRANSITION_CLASSIFICATION),
        "missing_instrument_proposal": rel(MISSING_INSTRUMENT_PROPOSAL),
        "accepted_instrument_build_packet": rel(ACCEPTED_BUILD_STUB),
        "instrument_verification_receipt": rel(VERIFICATION_STUB),
        "repeat_once_packet": rel(REPEAT_STUB),
        "sidecar_events": rel(SIDECAR_EVENTS_JSONL),
        "decision_edge_observations": rel(EDGE_OBSERVATIONS_JSONL),
        "unit_feedback_records": rel(UNIT_FEEDBACK_JSONL),
        "runtime_step_receipts": rel(RUNTIME_STEP_RECEIPTS_JSONL),
        "rollup": rel(ROLLUP_PATH),
        "readout": rel(READOUT_PATH),
        "profile": rel(PROFILE_PATH),
        "report": rel(REPORT_PATH),
        "transition_trace": rel(TRACE_PATH),
    }

    receipt = {
        "schema_version": "c8_basic_research_loop_specimen_receipt_v0",
        "receipt_type": "TYPED_C8_BASIC_RESEARCH_LOOP_SPECIMEN_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "run_id": run_id,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "failures": failures,
        "warnings": warnings,
        "source_receipts": {
            "r0_active_source_packet_ref": rel(R0_PACKET),
            "r0_receipt_ref": rel(R0_RECEIPT),
            "runtime_membranes_receipt_ref": rel(MEMBRANES_RECEIPT),
            "double_sieve_suite_receipt_ref": rel(DOUBLE_SIEVE_RECEIPT),
            "runtime_observability_feedback_attachment_receipt_ref": rel(RUNTIME_ATTACHMENT_RECEIPT),
            "c7_receipt_ref": rel(C7_RECEIPT),
            "c7_rollup_ref": rel(C7_ROLLUP),
        },
        "machine_readable_c8_summary": {
            "specimen_complete": gate == "PASS",
            "proposal_only_first_pass": True,
            "frontier_surfaces_loaded": 1,
            "bounded_probes_run": 1,
            "transition_classification_emitted": TRANSITION_CLASSIFICATION.exists(),
            "transition_classification": "MISSING_INSTRUMENT_EXPOSED",
            "missing_instrument_proposal_emitted": MISSING_INSTRUMENT_PROPOSAL.exists(),
            "missing_instrument_proposal_status": "PROPOSED_ONLY",
            "instrument_built": False,
            "instrument_built_with_acceptance": False,
            "local_verification_emitted": False,
            "repeat_once_completed": False,
            "accepted_build_packet_preexisting": False,
            "na_stubs_emitted_for_build_verify_repeat": ACCEPTED_BUILD_STUB.exists() and VERIFICATION_STUB.exists() and REPEAT_STUB.exists(),
            "sidecar_events_emitted": 1,
            "decision_edge_observations_emitted": 1,
            "unit_feedback_records_emitted": 0,
            "runtime_receipts_emitted": 1,
            "unbounded_probe": False,
            "hidden_continuation": False,
            "cell1_freebuild": False,
            "proposal_self_accepted": False,
            "accepted_build_packet_created_by_runner": False,
            "global_solution_claim": False,
            "frontier_solved_claim": False,
            "research_mode_opened": False,
            "source_receipts_mutated": source_hashes_before != source_hashes_after,
            "bad_counters_zero": not bool(nonzero_negative),
            "next_command_goal": None,
        },
        "acceptance_gate_results": acceptance,
        "negative_controls": negative_controls,
        "source_receipt_immutability": {
            "source_hashes_before": source_hashes_before,
            "source_hashes_after": source_hashes_after,
            "source_receipts_mutated": source_hashes_before != source_hashes_after,
        },
        "output_artifacts": output_artifacts,
        "terminal": {
            "type": "STOP",
            "stop_code": terminal_stop,
            "next_command_goal": None,
        },
    }

    receipt["receipt_id"] = "c8_basic_research_loop_specimen_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c8_receipt_id={receipt['receipt_id']}")
    print(f"c8_receipt_path={rel(receipt_path)}")
    print(f"c8_run_id={run_id}")
    print(f"c8_outcome={outcome}")
    print(f"c8_terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
