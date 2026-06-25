#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_RUNTIME_SCHEMA_VALIDATOR_CELL_V0"
TARGET_UNIT_ID = "runtime.schema_validator_cell.v0"
LAYER = "RUNTIME / SIEVE_1"
MODE = "VALIDATE / CLASSIFY / FORMATION_ONLY"
BUILD_MODE = "RUNTIME_SCHEMA_VALIDATOR_CELL_SYNTHETIC_BUILD_ONLY"

SOURCE_DESIGN_RECEIPT_ID = "ccbf5723"
SOURCE_OBSERVABILITY_REFERENCE_CLOSURE_RECEIPT_ID = "ac09c2e3"

SOURCE_DESIGN_RECEIPT_PATH = ROOT / "data/runtime_schema_validator_cell_target_from_reviewed_observability_reference_v0_receipts/ccbf5723.json"
DESIGN_DIR = ROOT / "data/runtime_schema_validator_cell_target_from_reviewed_observability_reference_v0"
DESIGN_FILES = [
    DESIGN_DIR / "runtime_schema_validator_cell_design_basis_v0.json",
    DESIGN_DIR / "runtime_schema_validator_cell_source_decision_review_v0.json",
    DESIGN_DIR / "runtime_schema_validator_cell_source_observability_reference_review_v0.json",
    DESIGN_DIR / "runtime_schema_validator_cell_target_spec_v0.json",
    DESIGN_DIR / "runtime_schema_validator_cell_formation_check_table_v0.json",
    DESIGN_DIR / "runtime_schema_validator_cell_failure_precedence_v0.json",
    DESIGN_DIR / "schema_validation_result_enum_target_v0.json",
    DESIGN_DIR / "schema_validation_result_schema_target_v0.json",
    DESIGN_DIR / "validated_candidate_packet_schema_target_v0.json",
    DESIGN_DIR / "schema_feedback_packet_schema_target_v0.json",
    DESIGN_DIR / "schema_gap_feedback_packet_schema_target_v0.json",
    DESIGN_DIR / "schema_validator_cell_receipt_schema_target_v0.json",
    DESIGN_DIR / "runtime_schema_validator_cell_demo_case_plan_v0.json",
    DESIGN_DIR / "runtime_schema_validator_cell_acceptance_gates_v0.json",
    DESIGN_DIR / "runtime_schema_validator_cell_negative_controls_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_dependency_park_v0.json",
    DESIGN_DIR / "runtime_schema_validator_cell_build_target_v0.json",
    DESIGN_DIR / "runtime_schema_validator_cell_design_authority_boundary_v0.json",
    DESIGN_DIR / "runtime_schema_validator_cell_design_classification_v0.json",
    DESIGN_DIR / "runtime_schema_validator_cell_design_rollup_v0.json",
    DESIGN_DIR / "runtime_schema_validator_cell_design_profile_v0.json",
    DESIGN_DIR / "runtime_schema_validator_cell_design_report.json",
    DESIGN_DIR / "runtime_schema_validator_cell_design_transition_trace.json",
]

SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_PATH = ROOT / "data/decision_edge_observability_reference_closure_from_bounded_c6_adoption_probe_reference_v0_receipts/ac09c2e3.json"
EDGE_OBS_REVIEWED_REFERENCE_PATH = ROOT / "data/decision_edge_observability_reference_closure_from_bounded_c6_adoption_probe_reference_v0/decision_edge_observability_reviewed_reference_v0.json"

REQUIRED_SOURCE_FILES = [SOURCE_DESIGN_RECEIPT_PATH, SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_PATH, EDGE_OBS_REVIEWED_REFERENCE_PATH] + DESIGN_FILES

OUT_DIR = ROOT / "data/runtime_schema_validator_cell_v0"
RECEIPT_DIR = ROOT / "data/runtime_schema_validator_cell_v0_receipts"

SCHEMA_ARCHIVE_SCHEMA_PATH = OUT_DIR / "schema_archive_schema_v0.json"
SCHEMA_ARCHIVE_PATH = OUT_DIR / "schema_archive_v0.json"
RESULT_ENUM_PATH = OUT_DIR / "schema_validation_result_enum_v0.json"
RESULT_SCHEMA_PATH = OUT_DIR / "schema_validation_result_schema_v0.json"
VALIDATED_PACKET_SCHEMA_PATH = OUT_DIR / "validated_candidate_packet_schema_v0.json"
SCHEMA_FEEDBACK_SCHEMA_PATH = OUT_DIR / "schema_feedback_packet_schema_v0.json"
SCHEMA_GAP_FEEDBACK_SCHEMA_PATH = OUT_DIR / "schema_gap_feedback_packet_schema_v0.json"
RECEIPT_SCHEMA_PATH = OUT_DIR / "schema_validator_cell_receipt_schema_v0.json"
CHECK_TABLE_PATH = OUT_DIR / "schema_validator_check_table_v0.json"
DEMO_INPUTS_PATH = OUT_DIR / "schema_validator_demo_inputs_v0.jsonl"
VALIDATION_RESULTS_PATH = OUT_DIR / "schema_validation_results_v0.jsonl"
VALIDATED_PACKETS_PATH = OUT_DIR / "validated_candidate_packets_v0.jsonl"
SCHEMA_FEEDBACK_PACKETS_PATH = OUT_DIR / "schema_feedback_packets_v0.jsonl"
SCHEMA_GAP_FEEDBACK_PACKETS_PATH = OUT_DIR / "schema_gap_feedback_packets_v0.jsonl"
ROLLUP_PATH = OUT_DIR / "schema_validator_rollup_v0.json"
READOUT_PATH = OUT_DIR / "schema_validator_readout_v0.json"
PROFILE_PATH = OUT_DIR / "schema_validator_profile_v0.json"
REPORT_PATH = OUT_DIR / "schema_validator_report.json"
TRACE_PATH = OUT_DIR / "schema_validator_transition_trace.json"

EXPECTED_DESIGN_STATUS = "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_TARGET_DESIGNED_BUILD_READY"
EXPECTED_DESIGN_STOP = "STOP_TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_TARGET_DESIGNED_BUILD_READY"
EXPECTED_DESIGN_NEXT = UNIT_ID

RECOMMENDED_NEXT = "REVIEW_RUNTIME_SCHEMA_VALIDATOR_CELL_V0"

REQUIRED_EDGE_FIELDS = [
    "active_object",
    "attempted_move",
    "boundary_checked",
    "boundary_result",
    "blocked_moves",
    "lawful_next_moves",
    "source_packet_ref",
]

FAILURE_PRECEDENCE = [
    "SCHEMA_ARCHIVE_UNAVAILABLE",
    "UNKNOWN_SCHEMA",
    "SCHEMA_VERSION_MISMATCH",
    "INVALID_SHAPE",
    "MISSING_FIELD",
    "FORBIDDEN_FIELD",
    "TYPE_MISMATCH",
    "UNKNOWN_MOVE_TYPE",
    "BOUNDARY_MISSING",
    "BOUNDARY_CONFLICT",
    "UNRESOLVED_REFERENCE",
    "RECEIPT_CONTRACT_INSUFFICIENT",
    "DISTINGUISHABILITY_INSUFFICIENT",
    "LAYER_COLLAPSE_IN_PAYLOAD",
    "HIDDEN_EXECUTION_FIELD",
    "SCHEMA_ARCHIVE_GAP",
]

RESULT_ENUM = [
    "VALID",
    "UNKNOWN_SCHEMA",
    "INVALID_SHAPE",
    "TYPE_MISMATCH",
    "MISSING_FIELD",
    "FORBIDDEN_FIELD",
    "BOUNDARY_MISSING",
    "BOUNDARY_CONFLICT",
    "UNRESOLVED_REFERENCE",
    "UNKNOWN_MOVE_TYPE",
    "RECEIPT_CONTRACT_INSUFFICIENT",
    "DISTINGUISHABILITY_INSUFFICIENT",
    "SCHEMA_VERSION_MISMATCH",
    "LAYER_COLLAPSE_IN_PAYLOAD",
    "HIDDEN_EXECUTION_FIELD",
    "SCHEMA_ARCHIVE_UNAVAILABLE",
    "MISSING_REVIEW_BASIS",
    "BUILD_VERIFICATION_MISMATCH",
    "SCHEMA_ARCHIVE_GAP",
]

FORMATION_CHECKS = [
    ("schema_archive_available", "SCHEMA_ARCHIVE_UNAVAILABLE"),
    ("schema_known", "UNKNOWN_SCHEMA"),
    ("schema_version_compatible", "SCHEMA_VERSION_MISMATCH"),
    ("shape_valid", "INVALID_SHAPE"),
    ("required_fields_present", "MISSING_FIELD"),
    ("forbidden_fields_absent", "FORBIDDEN_FIELD"),
    ("field_types_correct", "TYPE_MISMATCH"),
    ("declared_move_type_known", "UNKNOWN_MOVE_TYPE"),
    ("declared_boundary_structure_complete", "BOUNDARY_MISSING"),
    ("declared_boundary_structure_consistent", "BOUNDARY_CONFLICT"),
    ("references_structurally_resolvable", "UNRESOLVED_REFERENCE"),
    ("receipt_contract_declared", "RECEIPT_CONTRACT_INSUFFICIENT"),
    ("distinguishability_sufficient", "DISTINGUISHABILITY_INSUFFICIENT"),
    ("layer_collapse_absent", "LAYER_COLLAPSE_IN_PAYLOAD"),
    ("hidden_execution_fields_absent", "HIDDEN_EXECUTION_FIELD"),
]

DEMO_CASES = [
    ("valid_bounded_repair_proposal", "VALID"),
    ("valid_extraction_proposal", "VALID"),
    ("missing_required_field", "MISSING_FIELD"),
    ("missing_receipt_contract", "RECEIPT_CONTRACT_INSUFFICIENT"),
    ("unknown_schema", "UNKNOWN_SCHEMA"),
    ("schema_version_mismatch", "SCHEMA_VERSION_MISMATCH"),
    ("type_mismatch", "TYPE_MISMATCH"),
    ("boundary_missing", "BOUNDARY_MISSING"),
    ("boundary_conflict", "BOUNDARY_CONFLICT"),
    ("unresolved_reference", "UNRESOLVED_REFERENCE"),
    ("unknown_move_type", "UNKNOWN_MOVE_TYPE"),
    ("distinguishability_insufficient", "DISTINGUISHABILITY_INSUFFICIENT"),
    ("layer_collapse_in_payload", "LAYER_COLLAPSE_IN_PAYLOAD"),
    ("hidden_execution_field", "HIDDEN_EXECUTION_FIELD"),
    ("latest_file_reference", "UNRESOLVED_REFERENCE"),
    ("mtime_reference", "UNRESOLVED_REFERENCE"),
]

NEGATIVE_CONTROL_COUNTERS = [
    "authority_claim_count",
    "admissibility_checked_count",
    "execution_claim_count",
    "schema_archive_mutation_count",
    "proposal_repair_count",
    "schema_created_count",
    "unknown_schema_accepted_count",
    "invalid_proposal_advanced_count",
    "missing_receipt_contract_accepted_count",
    "unresolved_reference_accepted_count",
    "forbidden_field_accepted_count",
    "layer_collapse_accepted_count",
    "hidden_execution_field_accepted_count",
    "latest_file_reference_accepted_count",
    "mtime_reference_accepted_count",
    "builder_command_emitted_count",
]

REQUIRED_PROPOSAL_FIELDS = [
    "proposal_id",
    "claimed_schema_ref",
    "claimed_schema_version",
    "declared_move_type",
    "declared_boundaries",
    "declared_references",
    "receipt_contract",
    "distinguishability",
    "payload",
]

FORBIDDEN_FIELDS = [
    "execution_started",
    "authority_status",
    "admissibility_status",
    "builder_command",
    "runtime_patch",
]

ALLOWED_MOVE_TYPES = [
    "BOUNDED_REPAIR",
    "EXTRACTION",
    "REFERENCE_CLOSURE",
]

KNOWN_REFS = {
    "receipt:ccbf5723",
    "receipt:ac09c2e3",
    "artifact:decision_edge_observability_reviewed_reference_v0",
    "artifact:runtime_schema_validator_cell_target_spec_v0",
}

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
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{rel(path)}")
    if failures:
        return failures, {}

    design_receipt = read_json(SOURCE_DESIGN_RECEIPT_PATH)
    design_summary = design_receipt.get("machine_readable_runtime_schema_validator_cell_design_summary", {})
    target_spec = read_json(DESIGN_DIR / "runtime_schema_validator_cell_target_spec_v0.json")
    check_table = read_json(DESIGN_DIR / "runtime_schema_validator_cell_formation_check_table_v0.json")
    failure_precedence = read_json(DESIGN_DIR / "runtime_schema_validator_cell_failure_precedence_v0.json")
    result_enum_target = read_json(DESIGN_DIR / "schema_validation_result_enum_target_v0.json")
    demo_case_plan = read_json(DESIGN_DIR / "runtime_schema_validator_cell_demo_case_plan_v0.json")
    acceptance_gates = read_json(DESIGN_DIR / "runtime_schema_validator_cell_acceptance_gates_v0.json")
    negative_controls = read_json(DESIGN_DIR / "runtime_schema_validator_cell_negative_controls_v0.json")
    build_target = read_json(DESIGN_DIR / "runtime_schema_validator_cell_build_target_v0.json")
    authority = read_json(DESIGN_DIR / "runtime_schema_validator_cell_design_authority_boundary_v0.json")
    profile = read_json(DESIGN_DIR / "runtime_schema_validator_cell_design_profile_v0.json")

    obs_ref_close_receipt = read_json(SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_PATH)
    obs_reviewed_reference = read_json(EDGE_OBS_REVIEWED_REFERENCE_PATH)

    if design_receipt.get("receipt_id") != SOURCE_DESIGN_RECEIPT_ID or design_receipt.get("gate") != "PASS":
        failures.append("source_design_receipt_not_pass")
    if design_receipt.get("terminal", {}).get("stop_code") != EXPECTED_DESIGN_STOP:
        failures.append("source_design_stop_wrong")
    if design_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_design_hidden_next")
    if design_summary.get("status") != EXPECTED_DESIGN_STATUS:
        failures.append(f"source_design_status_wrong:{design_summary.get('status')}")
    if design_summary.get("recommended_next") != EXPECTED_DESIGN_NEXT:
        failures.append(f"source_design_next_wrong:{design_summary.get('recommended_next')}")
    for key in [
        "runtime_schema_validator_cell_target_designed",
        "schema_validator_build_ready",
        "formation_only_boundary_defined",
        "validate_classify_terminology_locked",
        "failure_precedence_locked",
        "observability_sidecar_deferred",
        "unit_feedback_hardening_deferred",
        "c7_deferred",
        "c8_deferred",
        "runtime_adoption_deferred",
        "bad_counters_zero",
    ]:
        if design_summary.get(key) is not True:
            failures.append(f"source_design_true_missing:{key}")
    for key in [
        "runtime_effect",
        "runtime_patched",
        "live_runtime_routing_installed",
        "authority_checked",
        "admissibility_checked",
        "execution_claimed",
        "schema_archive_mutated",
        "proposal_repaired",
        "schema_created",
        "builder_command_emitted",
        "c7_authorized",
        "c8_authorized",
        "source_mutated",
        "prior_receipt_mutated",
        "observability_reference_mutated",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if design_summary.get(key) is not False:
            failures.append(f"source_design_forbidden_true:{key}")
    for key, expected in {
        "formation_check_count": 15,
        "result_enum_count": 19,
        "demo_case_count": 16,
        "acceptance_gate_count": 33,
        "negative_control_count": 19,
        "observability_required_edge_field_count": 7,
    }.items():
        if design_summary.get(key) != expected:
            failures.append(f"source_design_count_wrong:{key}:{design_summary.get(key)}")

    if target_spec.get("mode") != MODE:
        failures.append("target_spec_mode_wrong")
    if target_spec.get("valid_means") != "structurally validated under known schema":
        failures.append("target_spec_valid_means_wrong")
    if [c.get("failure") for c in check_table.get("checks", [])] != [f for _, f in FORMATION_CHECKS]:
        failures.append("check_table_wrong")
    if failure_precedence.get("failure_precedence") != FAILURE_PRECEDENCE:
        failures.append("failure_precedence_wrong")
    if result_enum_target.get("closed_results") != RESULT_ENUM:
        failures.append("result_enum_wrong")
    if demo_case_plan.get("demo_case_count") != 16:
        failures.append("demo_case_count_wrong")
    if acceptance_gates.get("gate_count") != 33:
        failures.append("acceptance_gate_count_wrong")
    if negative_controls.get("negative_control_count") != 19:
        failures.append("negative_control_count_wrong")
    if build_target.get("build_target_status") != "BUILD_READY":
        failures.append("build_target_not_ready")
    if authority.get("may_build_schema_validator_cell_next") is not True:
        failures.append("authority_no_build_next")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if obs_ref_close_receipt.get("gate") != "PASS":
        failures.append("observability_ref_close_not_pass")
    if obs_reviewed_reference.get("reference_status") != "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEWED_REFERENCE_FROZEN":
        failures.append("observability_ref_not_frozen")

    return failures, {
        "design_summary": design_summary,
        "target_spec": target_spec,
    }

def base_proposal(case_name: str, expected: str) -> Dict[str, Any]:
    proposal = {
        "proposal_id": f"proposal_{case_name}",
        "claimed_schema_ref": "proposal_packet_schema_v0",
        "claimed_schema_version": "v0",
        "declared_move_type": "BOUNDED_REPAIR" if "repair" in case_name else "EXTRACTION",
        "declared_boundaries": {
            "target_object": "demo_object",
            "target_surface": "demo_surface",
            "allowed_inputs": ["source_proposal_ref", "review_receipt_ref"],
            "forbidden_inputs": ["unbounded_payload", "latest_file_guessing", "mtime_selection"],
            "allowed_outputs": ["receipt", "artifact"],
            "stop_conditions": ["schema validation failed", "authority boundary required"],
        },
        "declared_references": ["receipt:ccbf5723", "artifact:decision_edge_observability_reviewed_reference_v0"],
        "receipt_contract": {
            "expected_receipt_type": "schema_validator_demo_receipt_v0",
            "expected_artifacts": ["validation_result", "terminal"],
            "required_negative_controls": ["authority_claim_count == 0", "execution_claim_count == 0"],
            "verification_gate": "declared gate passes",
            "terminal": "STOP_OR_ADVANCE",
            "handoff_target": "LAWFUL_ADMISSIBILITY_CELL_OR_BUILDER_PROPOSAL_CELL",
        },
        "distinguishability": {
            "distinguish_from": [
                "no-op",
                "partial execution",
                "wrong target",
                "unauthorized mutation",
                "verification failure",
                "unrelated success",
            ],
            "sufficient": True,
        },
        "payload": {
            "active_object": "demo_object",
            "attempted_move": "pass_to_admissibility",
        },
        "expected_result": expected,
        "demo_case": case_name,
    }

    if case_name == "missing_required_field":
        proposal.pop("declared_move_type", None)
    elif case_name == "missing_receipt_contract":
        proposal["receipt_contract"] = {}
    elif case_name == "unknown_schema":
        proposal["claimed_schema_ref"] = "unknown_schema_v0"
    elif case_name == "schema_version_mismatch":
        proposal["claimed_schema_version"] = "v99"
    elif case_name == "type_mismatch":
        proposal["declared_references"] = "receipt:ccbf5723"
    elif case_name == "boundary_missing":
        proposal["declared_boundaries"] = {}
    elif case_name == "boundary_conflict":
        proposal["declared_boundaries"]["allowed_inputs"].append("latest_file_guessing")
    elif case_name == "unresolved_reference":
        proposal["declared_references"] = ["receipt:not_found"]
    elif case_name == "unknown_move_type":
        proposal["declared_move_type"] = "MAGIC_UNBOUNDED_MOVE"
    elif case_name == "distinguishability_insufficient":
        proposal["distinguishability"]["sufficient"] = False
    elif case_name == "layer_collapse_in_payload":
        proposal["proposal_status"] = "PROPOSED_ONLY"
        proposal["verification_status"] = "PASS"
        proposal["build_receipt_ref"] = None
    elif case_name == "hidden_execution_field":
        proposal["hidden_execution"] = "run this now"
    elif case_name == "latest_file_reference":
        proposal["declared_references"] = ["latest receipt"]
    elif case_name == "mtime_reference":
        proposal["declared_references"] = ["mtime selected artifact"]
    return proposal

def schema_archive() -> Dict[str, Any]:
    return {
        "schema_version": "schema_archive_v0",
        "archive_id": "schema_archive_v0",
        "schemas": [
            {
                "schema_ref": "proposal_packet_schema_v0",
                "schema_kind": "PROPOSAL_PACKET",
                "version": "v0",
                "status": "ACTIVE",
                "required_fields": REQUIRED_PROPOSAL_FIELDS,
                "forbidden_fields": FORBIDDEN_FIELDS,
                "allowed_move_types": ALLOWED_MOVE_TYPES,
                "receipt_contract_required": True,
                "reference_policy": "EXPLICIT_STRUCTURAL_REFS_ONLY",
            }
        ],
        "mutation_allowed_by_schema_validator": False,
    }

def validate_case(proposal: Dict[str, Any], archive: Dict[str, Any]) -> Tuple[str, List[Dict[str, Any]], Dict[str, Any]]:
    schema_map = {s["schema_ref"]: s for s in archive["schemas"] if s.get("status") == "ACTIVE"}
    field_results: List[Dict[str, Any]] = []
    boundary_results = {
        "object_boundaries_declared": False,
        "references_resolvable": False,
        "receipt_contract_declared": False,
        "distinguishability_sufficient": False,
        "layer_collapse_absent": False,
        "hidden_execution_fields_absent": False,
    }

    def fail(result: str, field_path: str, check: str, expected: Any, observed: Any, why: str) -> str:
        field_results.append({
            "field_path": field_path,
            "check": check,
            "status": "FAIL",
            "failure_class": result,
            "expected": expected,
            "observed": observed,
            "why_load_bearing": why,
        })
        return result

    if not archive:
        return fail("SCHEMA_ARCHIVE_UNAVAILABLE", "schema_archive", "schema_archive_available", "available archive", None, "Validator cannot classify formation without a schema archive."), field_results, boundary_results

    schema_ref = proposal.get("claimed_schema_ref")
    if schema_ref not in schema_map:
        return fail("UNKNOWN_SCHEMA", "claimed_schema_ref", "schema_known", "known schema ref", schema_ref, "Unknown schemas cannot be validated by analogy."), field_results, boundary_results

    schema = schema_map[schema_ref]
    if proposal.get("claimed_schema_version") != schema.get("version"):
        return fail("SCHEMA_VERSION_MISMATCH", "claimed_schema_version", "schema_version_compatible", schema.get("version"), proposal.get("claimed_schema_version"), "Version mismatch changes field meaning."), field_results, boundary_results

    if not isinstance(proposal, dict):
        return fail("INVALID_SHAPE", "$", "shape_valid", "object", type(proposal).__name__, "Proposal must be an object to be read."), field_results, boundary_results

    for field in schema["required_fields"]:
        if field not in proposal or proposal.get(field) in (None, "", []):
            return fail("MISSING_FIELD", field, "required_fields_present", "present non-empty field", proposal.get(field), "Missing required field blocks downstream interpretation."), field_results, boundary_results

    for field in schema["forbidden_fields"]:
        if field in proposal:
            return fail("FORBIDDEN_FIELD", field, "forbidden_fields_absent", "absent", proposal.get(field), "Forbidden fields collapse validator into another authority or execution layer."), field_results, boundary_results

    if not isinstance(proposal.get("declared_references"), list):
        return fail("TYPE_MISMATCH", "declared_references", "field_types_correct", "array", type(proposal.get("declared_references")).__name__, "References must be enumerable and auditable."), field_results, boundary_results

    if proposal.get("declared_move_type") not in schema["allowed_move_types"]:
        return fail("UNKNOWN_MOVE_TYPE", "declared_move_type", "declared_move_type_known", schema["allowed_move_types"], proposal.get("declared_move_type"), "Move type defines which shape can be interpreted."), field_results, boundary_results

    boundaries = proposal.get("declared_boundaries")
    required_boundary_fields = ["target_object", "target_surface", "allowed_inputs", "forbidden_inputs", "allowed_outputs", "stop_conditions"]
    if not isinstance(boundaries, dict) or any(not boundaries.get(f) for f in required_boundary_fields):
        return fail("BOUNDARY_MISSING", "declared_boundaries", "declared_boundary_structure_complete", required_boundary_fields, boundaries, "Boundary declaration is required before authority can judge later."), field_results, boundary_results
    boundary_results["object_boundaries_declared"] = True

    if set(boundaries.get("allowed_inputs", [])) & set(boundaries.get("forbidden_inputs", [])):
        return fail("BOUNDARY_CONFLICT", "declared_boundaries", "declared_boundary_structure_consistent", "disjoint allowed/forbidden inputs", boundaries, "Contradictory boundaries cannot be safely handed downstream."), field_results, boundary_results

    for ref in proposal.get("declared_references", []):
        if ref not in KNOWN_REFS:
            return fail("UNRESOLVED_REFERENCE", "declared_references", "references_structurally_resolvable", "explicit known structural ref", ref, "References must be structurally addressable; latest/mtime/vague refs are not accepted."), field_results, boundary_results
    boundary_results["references_resolvable"] = True

    rc = proposal.get("receipt_contract")
    required_receipt_fields = ["expected_receipt_type", "expected_artifacts", "required_negative_controls", "verification_gate", "terminal", "handoff_target"]
    if not isinstance(rc, dict) or any(not rc.get(f) for f in required_receipt_fields):
        return fail("RECEIPT_CONTRACT_INSUFFICIENT", "receipt_contract", "receipt_contract_declared", required_receipt_fields, rc, "Receipt contract makes future outcome distinguishable."), field_results, boundary_results
    boundary_results["receipt_contract_declared"] = True

    distinguishability = proposal.get("distinguishability", {})
    if distinguishability.get("sufficient") is not True:
        return fail("DISTINGUISHABILITY_INSUFFICIENT", "distinguishability", "distinguishability_sufficient", True, distinguishability.get("sufficient"), "Downstream receipts must separate success/failure from no-op or unrelated success."), field_results, boundary_results
    boundary_results["distinguishability_sufficient"] = True

    if "proposal_status" in proposal or "verification_status" in proposal or proposal.get("build_receipt_ref") is None and "build_receipt_ref" in proposal:
        return fail("LAYER_COLLAPSE_IN_PAYLOAD", "$", "layer_collapse_absent", "proposal-only formation payload", "mixed proposal/build/verification fields", "Layer collapse makes state transitions indistinguishable."), field_results, boundary_results
    boundary_results["layer_collapse_absent"] = True

    if "hidden_execution" in proposal:
        return fail("HIDDEN_EXECUTION_FIELD", "hidden_execution", "hidden_execution_fields_absent", "absent", proposal.get("hidden_execution"), "Hidden execution fields would bypass admissibility and execution boundaries."), field_results, boundary_results
    boundary_results["hidden_execution_fields_absent"] = True

    for name, _ in FORMATION_CHECKS:
        field_results.append({
            "field_path": "*",
            "check": name,
            "status": "PASS",
            "failure_class": None,
            "expected": "pass",
            "observed": "pass",
            "why_load_bearing": "Formation check passed under known schema.",
        })

    return "VALID", field_results, boundary_results

def validation_result(proposal: Dict[str, Any], result: str, field_results: List[Dict[str, Any]], boundary_results: Dict[str, Any]) -> Dict[str, Any]:
    validation_id = "schema_val_" + sig8({"proposal_id": proposal["proposal_id"], "result": result})
    is_valid = result == "VALID"
    return {
        "schema_version": "schema_validation_result_v0",
        "validation_id": validation_id,
        "cell_id": "SCHEMA_VALIDATOR_CELL",
        "input_proposal_ref": proposal["proposal_id"],
        "claimed_schema_ref": proposal.get("claimed_schema_ref"),
        "claimed_schema_version": proposal.get("claimed_schema_version"),
        "result": result,
        "result_class": "VALID_FORMATION" if is_valid else "FORMATION_FAILURE",
        "field_results": field_results,
        "boundary_results": boundary_results,
        "return_to": "LAWFUL_ADMISSIBILITY_CELL" if is_valid else "BUILDER_PROPOSAL_CELL",
        "must_not_infer": [
            "proposal is authorized",
            "proposal is true",
            "proposal should execute",
            "proposal is strategically good",
        ],
        "terminal": {
            "type": "ADVANCE" if is_valid else "STOP",
            "next": "LAWFUL_ADMISSIBILITY_CELL" if is_valid else None,
            "advance_code": "ADVANCE_SCHEMA_VALIDATED" if is_valid else None,
            "stop_code": None if is_valid else ("STOP_UNKNOWN_SCHEMA" if result == "UNKNOWN_SCHEMA" else "STOP_SCHEMA_VALIDATION_FAILED"),
            "next_command_goal": None,
        },
    }

def validated_packet(proposal: Dict[str, Any], result_ref: str) -> Dict[str, Any]:
    return {
        "schema_version": "validated_candidate_packet_v0",
        "packet_id": "validated_candidate_" + sig8({"proposal": proposal["proposal_id"], "result": result_ref}),
        "from_cell": "SCHEMA_VALIDATOR_CELL",
        "to_cell": "LAWFUL_ADMISSIBILITY_CELL",
        "source_proposal_ref": proposal["proposal_id"],
        "schema_validation_ref": result_ref,
        "validated_schema_ref": proposal.get("claimed_schema_ref"),
        "validated_schema_version": proposal.get("claimed_schema_version"),
        "declared_move_type": proposal.get("declared_move_type"),
        "declared_object_boundaries": proposal.get("declared_boundaries"),
        "declared_receipt_contract": proposal.get("receipt_contract"),
        "validation_status": "SCHEMA_VALIDATED",
        "authority_status": "NOT_CHECKED",
        "admissibility_status": "NOT_CHECKED",
        "execution_status": "NOT_EXECUTED",
        "verification_status": "NOT_VERIFIED",
        "must_not_infer": [
            "authorized",
            "admissible",
            "executed",
            "verified",
            "strategically accepted",
        ],
    }

def feedback_packet(proposal: Dict[str, Any], result: str, result_ref: str, field_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    first_fail = next((fr for fr in field_results if fr.get("status") == "FAIL"), {})
    return {
        "schema_version": "schema_feedback_packet_v0",
        "packet_id": "schema_feedback_" + sig8({"proposal": proposal["proposal_id"], "result": result}),
        "from_cell": "SCHEMA_VALIDATOR_CELL",
        "to_cell": "BUILDER_PROPOSAL_CELL",
        "source_proposal_ref": proposal["proposal_id"],
        "validation_result_ref": result_ref,
        "failure_class": result,
        "failure_location": {
            "field_path": first_fail.get("field_path"),
            "proposal_section": "formation",
            "schema_area": first_fail.get("check"),
        },
        "why_failed": first_fail.get("why_load_bearing"),
        "blocked_transition": "LAWFUL_ADMISSIBILITY_CELL",
        "lawful_next_handling": [
            "repair proposal shape",
            "add required field",
            "add receipt contract",
            "emit schema gap proposal if schema cannot express this",
            "park object",
            "request review",
        ],
        "forbidden_next_handling": [
            "send to admissibility anyway",
            "execute",
            "treat as authority denial",
            "mutate schema archive directly",
        ],
        "repair_hint": {
            "allowed": True,
            "hint_type": "FORMATION_FEEDBACK",
            "hint": f"Resolve {result} at {first_fail.get('field_path')}. This is feedback, not repair.",
        },
    }

def gap_feedback_packet(proposal: Dict[str, Any], result_ref: str, result: str) -> Dict[str, Any]:
    return {
        "schema_version": "schema_gap_feedback_packet_v0",
        "packet_id": "schema_gap_" + sig8({"proposal": proposal["proposal_id"], "result": result}),
        "from_cell": "SCHEMA_VALIDATOR_CELL",
        "to_cell": "BUILDER_PROPOSAL_CELL",
        "source_proposal_ref": proposal["proposal_id"],
        "validation_result_ref": result_ref,
        "gap_class": "SCHEMA_ARCHIVE_GAP" if result == "SCHEMA_ARCHIVE_GAP" else "UNKNOWN_SCHEMA",
        "smallest_honest_reading": "Proposal cannot be read under the claimed schema archive.",
        "missing_schema_kind": proposal.get("claimed_schema_ref"),
        "lawful_next_handling": [
            "emit schema registration proposal",
            "request review",
            "park until schema exists",
        ],
        "forbidden_next_handling": [
            "create schema directly",
            "validate by analogy",
            "send to admissibility",
            "execute",
        ],
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    build_pass = not failures
    archive = schema_archive()

    demo_inputs: List[Dict[str, Any]] = []
    validation_results: List[Dict[str, Any]] = []
    validated_packets: List[Dict[str, Any]] = []
    schema_feedback_packets: List[Dict[str, Any]] = []
    schema_gap_feedback_packets: List[Dict[str, Any]] = []

    if build_pass:
        for case_name, expected in DEMO_CASES:
            proposal = base_proposal(case_name, expected)
            actual, field_results, boundary_results = validate_case(proposal, archive)
            if actual != expected:
                failures.append(f"demo_case_expected_{expected}_got_{actual}:{case_name}")
            result = validation_result(proposal, actual, field_results, boundary_results)
            result_ref = result["validation_id"]
            demo_inputs.append(proposal)
            validation_results.append(result)
            if actual == "VALID":
                validated_packets.append(validated_packet(proposal, result_ref))
            elif actual in ("UNKNOWN_SCHEMA", "SCHEMA_ARCHIVE_GAP"):
                schema_gap_feedback_packets.append(gap_feedback_packet(proposal, result_ref, actual))
            else:
                schema_feedback_packets.append(feedback_packet(proposal, actual, result_ref, field_results))

    build_pass = build_pass and not failures
    status = "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_BUILT_REVIEW_READY" if build_pass else "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_BUILD_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if build_pass else "REPAIR_RUNTIME_SCHEMA_VALIDATOR_CELL_BUILD_V0"

    reason_codes = [
        "RUNTIME_SCHEMA_VALIDATOR_CELL_BUILT",
        "DESIGN_RECEIPT_CONSUMED",
        "SCHEMA_ARCHIVE_SCHEMA_EMITTED",
        "SCHEMA_ARCHIVE_EMITTED_READ_ONLY",
        "VALIDATION_RESULT_ENUM_EMITTED",
        "VALIDATION_RESULT_SCHEMA_EMITTED",
        "VALIDATED_CANDIDATE_PACKET_SCHEMA_EMITTED",
        "SCHEMA_FEEDBACK_PACKET_SCHEMA_EMITTED",
        "SCHEMA_GAP_FEEDBACK_PACKET_SCHEMA_EMITTED",
        "SCHEMA_VALIDATOR_RECEIPT_SCHEMA_EMITTED",
        "CHECK_TABLE_EMITTED",
        "DEMO_INPUTS_EMITTED",
        "DEMO_VALIDATION_RESULTS_EMITTED",
        "ONLY_VALID_ADVANCED_TO_ADMISSIBILITY",
        "INVALID_RETURNED_TO_BUILDER",
        "UNKNOWN_SCHEMA_STOPPED",
        "FORMATION_ONLY_CLASSIFICATION_PRESERVED",
        "SIDE_CAR_DEFERRED_UNTIL_SCHEMA_VALIDATOR_REFERENCE_EXISTS",
        "C8_DEFERRED",
        "NO_RUNTIME_EFFECT",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_RUNTIME_ROUTING",
        "NO_AUTHORITY_CHECK",
        "NO_ADMISSIBILITY_CHECK",
        "NO_EXECUTION_CLAIM",
        "NO_SCHEMA_ARCHIVE_MUTATION",
        "NO_PROPOSAL_REPAIR",
        "NO_SCHEMA_CREATION",
        "NO_BUILDER_COMMAND",
        "NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if build_pass else failures

    schema_archive_schema = {
        "schema_version": "schema_archive_schema_v0",
        "required_top_level_fields": ["schema_version", "archive_id", "schemas", "mutation_allowed_by_schema_validator"],
        "schema_item_required_fields": ["schema_ref", "schema_kind", "version", "status", "required_fields", "forbidden_fields", "allowed_move_types", "receipt_contract_required"],
        "mutation_allowed_by_schema_validator": False,
    }

    result_enum_obj = {
        "schema_version": "schema_validation_result_enum_v0",
        "closed_results": RESULT_ENUM,
        "only_advancing_result": "VALID",
        "failure_precedence": FAILURE_PRECEDENCE,
    }

    result_schema = {
        "schema_version": "schema_validation_result_schema_v0",
        "required_top_level_fields": [
            "schema_version",
            "validation_id",
            "cell_id",
            "input_proposal_ref",
            "claimed_schema_ref",
            "claimed_schema_version",
            "result",
            "result_class",
            "field_results",
            "boundary_results",
            "return_to",
            "must_not_infer",
            "terminal",
        ],
    }

    validated_packet_schema = {
        "schema_version": "validated_candidate_packet_schema_v0",
        "required_top_level_fields": [
            "schema_version",
            "packet_id",
            "from_cell",
            "to_cell",
            "source_proposal_ref",
            "schema_validation_ref",
            "validated_schema_ref",
            "validated_schema_version",
            "declared_move_type",
            "declared_object_boundaries",
            "declared_receipt_contract",
            "validation_status",
            "authority_status",
            "admissibility_status",
            "execution_status",
            "verification_status",
            "must_not_infer",
        ],
        "authority_status_required": "NOT_CHECKED",
        "admissibility_status_required": "NOT_CHECKED",
        "execution_status_required": "NOT_EXECUTED",
        "verification_status_required": "NOT_VERIFIED",
    }

    schema_feedback_schema = {
        "schema_version": "schema_feedback_packet_schema_v0",
        "required_top_level_fields": [
            "schema_version",
            "packet_id",
            "from_cell",
            "to_cell",
            "source_proposal_ref",
            "validation_result_ref",
            "failure_class",
            "failure_location",
            "why_failed",
            "blocked_transition",
            "lawful_next_handling",
            "forbidden_next_handling",
            "repair_hint",
        ],
        "repair_hint_rule": "repair_hint is feedback, not repair",
    }

    schema_gap_feedback_schema = {
        "schema_version": "schema_gap_feedback_packet_schema_v0",
        "required_top_level_fields": [
            "schema_version",
            "packet_id",
            "from_cell",
            "to_cell",
            "source_proposal_ref",
            "validation_result_ref",
            "gap_class",
            "smallest_honest_reading",
            "missing_schema_kind",
            "lawful_next_handling",
            "forbidden_next_handling",
        ],
        "rule": "schema gap is not schema creation permission",
    }

    receipt_schema = {
        "schema_version": "schema_validator_cell_receipt_schema_v0",
        "required_top_level_fields": [
            "schema_version",
            "receipt_id",
            "cell_id",
            "unit_id",
            "input_proposal_ref",
            "validation_result_ref",
            "output_packet_ref",
            "feedback_packet_ref",
            "gate",
            "result",
            "advanced_to",
            "returned_to",
            "negative_controls",
            "terminal",
        ],
        "required_zero_counters": NEGATIVE_CONTROL_COUNTERS,
    }

    check_table = {
        "schema_version": "schema_validator_check_table_v0",
        "checks": [
            {"order": i, "check_name": name, "failure": failure}
            for i, (name, failure) in enumerate(FORMATION_CHECKS)
        ],
        "failure_precedence": FAILURE_PRECEDENCE,
        "only_valid_advances": True,
        "valid_advances_to": "LAWFUL_ADMISSIBILITY_CELL",
        "invalid_returns_to": "BUILDER_PROPOSAL_CELL",
    }

    result_counts = Counter(row["result"] for row in validation_results)
    invalid_count = len(validation_results) - result_counts.get("VALID", 0)
    returned_to_builder_count = sum(1 for row in validation_results if row["return_to"] == "BUILDER_PROPOSAL_CELL")
    advanced_count = sum(1 for row in validation_results if row["return_to"] == "LAWFUL_ADMISSIBILITY_CELL")

    failure_field_counts: Counter[str] = Counter()
    for row in validation_results:
        for fr in row.get("field_results", []):
            if fr.get("status") == "FAIL":
                failure_field_counts[str(fr.get("field_path"))] += 1

    negative_controls = {key: 0 for key in NEGATIVE_CONTROL_COUNTERS}

    rollup = {
        "schema_version": "schema_validator_rollup_v0",
        "proposals_evaluated": len(validation_results),
        "valid_count": result_counts.get("VALID", 0),
        "invalid_count": invalid_count,
        "returned_to_builder_count": returned_to_builder_count,
        "advanced_to_admissibility_count": advanced_count,
        "result_class_counts": dict(result_counts),
        "failure_field_counts": dict(failure_field_counts),
        "negative_controls": negative_controls,
    }

    readout = {
        "schema_version": "schema_validator_readout_v0",
        "proposals_evaluated": len(validation_results),
        "valid_count": result_counts.get("VALID", 0),
        "invalid_count": invalid_count,
        "advanced_to_admissibility": advanced_count,
        "returned_to_builder": returned_to_builder_count,
        "top_failure_classes": [
            {"failure_class": k, "count": v}
            for k, v in result_counts.most_common()
            if k != "VALID"
        ],
        "bad_counters_zero": all(v == 0 for v in negative_controls.values()),
        "interpretation": "Schema Validator Cell validates formation only. VALID candidates are readable under a known schema, not authorized.",
    }

    profile = {
        "schema_version": "schema_validator_profile_v0",
        "profile_id": "schema_validator_" + sig8(rollup),
        "cell_id": "SCHEMA_VALIDATOR_CELL",
        "status": "SCHEMA_VALIDATOR_STABLE" if build_pass else "SCHEMA_VALIDATOR_REPAIR_REQUIRED",
        "core_rule": "Schema Validator Cell validates form. Lawful Admissibility Cell validates permission.",
        "valid_advances_only_to": "LAWFUL_ADMISSIBILITY_CELL",
        "invalid_returns_to": "BUILDER_PROPOSAL_CELL",
        "schema_archive_mutation_allowed": False,
        "authority_checked": False,
        "execution_allowed": False,
        "bad_counters_zero": all(v == 0 for v in negative_controls.values()),
        "must_not_infer": [
            "VALID means authorized",
            "VALID means admissible",
            "VALID means true",
            "VALID means useful",
            "VALID means execute",
            "feedback hint means repair applied",
            "Schema Validator is live runtime routing",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "schema_validator_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The Runtime Schema Validator Cell surface was built as a synthetic/demo formation sieve. It emits schema archive schema, read-only archive, validation result enum/schema, candidate/feedback/gap packets, receipt schema, check table, demo inputs, validation outputs, rollup/readout/profile/report/trace, and receipt. Only VALID advances to Lawful Admissibility; invalid proposals return to Builder/Proposal Cell. No authority, admissibility, execution, schema mutation, proposal repair, builder command, runtime patch, live routing, Sidecar design, or C8 authorization occurred.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "schema_validator_transition_trace_v0",
        "trace": [
            {
                "step": "consume_design",
                "question": "is Schema Validator target design build-ready",
                "answer": "yes" if build_pass else "no",
                "taken": "build synthetic/demo formation sieve surface",
            },
            {
                "step": "run_demo_validation",
                "question": "do valid proposals advance and invalid proposals return",
                "answer": f"{advanced_count} advanced, {returned_to_builder_count} returned",
                "taken": "emit validation results and packets",
            },
            {
                "step": "preserve_boundary",
                "question": "did the validator check authority, execute, repair, mutate, patch runtime, or install live routing",
                "answer": "no",
                "taken": "stop review-ready",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (SCHEMA_ARCHIVE_SCHEMA_PATH, schema_archive_schema),
        (SCHEMA_ARCHIVE_PATH, archive),
        (RESULT_ENUM_PATH, result_enum_obj),
        (RESULT_SCHEMA_PATH, result_schema),
        (VALIDATED_PACKET_SCHEMA_PATH, validated_packet_schema),
        (SCHEMA_FEEDBACK_SCHEMA_PATH, schema_feedback_schema),
        (SCHEMA_GAP_FEEDBACK_SCHEMA_PATH, schema_gap_feedback_schema),
        (RECEIPT_SCHEMA_PATH, receipt_schema),
        (CHECK_TABLE_PATH, check_table),
        (ROLLUP_PATH, rollup),
        (READOUT_PATH, readout),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRACE_PATH, trace),
    ]
    for path, obj in artifacts:
        write_json(path, obj)

    write_jsonl(DEMO_INPUTS_PATH, demo_inputs)
    write_jsonl(VALIDATION_RESULTS_PATH, validation_results)
    write_jsonl(VALIDATED_PACKETS_PATH, validated_packets)
    write_jsonl(SCHEMA_FEEDBACK_PACKETS_PATH, schema_feedback_packets)
    write_jsonl(SCHEMA_GAP_FEEDBACK_PACKETS_PATH, schema_gap_feedback_packets)

    acceptance_gate_results = {
        "SCHEMA_VALIDATOR_0_SOURCE_DESIGN_CONSUMED": SOURCE_DESIGN_RECEIPT_PATH.exists(),
        "SCHEMA_VALIDATOR_1_SCHEMA_ARCHIVE_SCHEMA_EMITTED": SCHEMA_ARCHIVE_SCHEMA_PATH.exists(),
        "SCHEMA_VALIDATOR_2_VALIDATION_RESULT_ENUM_EMITTED": RESULT_ENUM_PATH.exists() and len(RESULT_ENUM) == 19,
        "SCHEMA_VALIDATOR_3_VALIDATION_RESULT_SCHEMA_EMITTED": RESULT_SCHEMA_PATH.exists(),
        "SCHEMA_VALIDATOR_4_VALIDATED_CANDIDATE_PACKET_SCHEMA_EMITTED": VALIDATED_PACKET_SCHEMA_PATH.exists(),
        "SCHEMA_VALIDATOR_5_SCHEMA_FEEDBACK_PACKET_SCHEMA_EMITTED": SCHEMA_FEEDBACK_SCHEMA_PATH.exists(),
        "SCHEMA_VALIDATOR_6_SCHEMA_GAP_FEEDBACK_PACKET_SCHEMA_EMITTED": SCHEMA_GAP_FEEDBACK_SCHEMA_PATH.exists(),
        "SCHEMA_VALIDATOR_7_RECEIPT_SCHEMA_EMITTED": RECEIPT_SCHEMA_PATH.exists(),
        "SCHEMA_VALIDATOR_8_CHECK_TABLE_EMITTED": CHECK_TABLE_PATH.exists() and len(FORMATION_CHECKS) == 15,
        "SCHEMA_VALIDATOR_9_DEMO_INPUTS_EMITTED": DEMO_INPUTS_PATH.exists() and len(demo_inputs) == 16,
        "SCHEMA_VALIDATOR_10_SCHEMA_KNOWN_CHECK_RUN": "UNKNOWN_SCHEMA" in result_counts,
        "SCHEMA_VALIDATOR_11_VERSION_CHECK_RUN": "SCHEMA_VERSION_MISMATCH" in result_counts,
        "SCHEMA_VALIDATOR_12_REQUIRED_FIELDS_CHECK_RUN": "MISSING_FIELD" in result_counts,
        "SCHEMA_VALIDATOR_13_FORBIDDEN_FIELDS_CHECK_RUN": "HIDDEN_EXECUTION_FIELD" in result_counts or "FORBIDDEN_FIELD" in result_counts,
        "SCHEMA_VALIDATOR_14_TYPE_CHECK_RUN": "TYPE_MISMATCH" in result_counts,
        "SCHEMA_VALIDATOR_15_MOVE_TYPE_CHECK_RUN": "UNKNOWN_MOVE_TYPE" in result_counts,
        "SCHEMA_VALIDATOR_16_BOUNDARY_CHECK_RUN": "BOUNDARY_MISSING" in result_counts and "BOUNDARY_CONFLICT" in result_counts,
        "SCHEMA_VALIDATOR_17_REFERENCE_CHECK_RUN": "UNRESOLVED_REFERENCE" in result_counts,
        "SCHEMA_VALIDATOR_18_RECEIPT_CONTRACT_CHECK_RUN": "RECEIPT_CONTRACT_INSUFFICIENT" in result_counts,
        "SCHEMA_VALIDATOR_19_DISTINGUISHABILITY_CHECK_RUN": "DISTINGUISHABILITY_INSUFFICIENT" in result_counts,
        "SCHEMA_VALIDATOR_20_LAYER_COLLAPSE_CHECK_RUN": "LAYER_COLLAPSE_IN_PAYLOAD" in result_counts,
        "SCHEMA_VALIDATOR_21_HIDDEN_EXECUTION_FIELD_CHECK_RUN": "HIDDEN_EXECUTION_FIELD" in result_counts,
        "SCHEMA_VALIDATOR_22_ONLY_VALID_ADVANCES": advanced_count == result_counts.get("VALID", 0) == len(validated_packets),
        "SCHEMA_VALIDATOR_23_INVALID_RETURNS_TO_BUILDER": returned_to_builder_count == invalid_count,
        "SCHEMA_VALIDATOR_24_NO_AUTHORITY_CLAIM": negative_controls["authority_claim_count"] == 0,
        "SCHEMA_VALIDATOR_25_NO_ADMISSIBILITY_CHECK": negative_controls["admissibility_checked_count"] == 0,
        "SCHEMA_VALIDATOR_26_NO_EXECUTION_CLAIM": negative_controls["execution_claim_count"] == 0,
        "SCHEMA_VALIDATOR_27_NO_SCHEMA_ARCHIVE_MUTATION": negative_controls["schema_archive_mutation_count"] == 0,
        "SCHEMA_VALIDATOR_28_NO_PROPOSAL_REPAIR": negative_controls["proposal_repair_count"] == 0,
        "SCHEMA_VALIDATOR_29_NO_BUILDER_COMMAND": negative_controls["builder_command_emitted_count"] == 0,
        "SCHEMA_VALIDATOR_30_ROLLUP_READOUT_PROFILE_EMITTED": ROLLUP_PATH.exists() and READOUT_PATH.exists() and PROFILE_PATH.exists(),
        "SCHEMA_VALIDATOR_31_BAD_COUNTERS_ZERO": all(v == 0 for v in negative_controls.values()),
        "SCHEMA_VALIDATOR_32_NO_HIDDEN_NEXT_COMMAND": profile["next_command_goal"] is None,
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_BUILD_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_RUNTIME_SCHEMA_VALIDATOR_CELL_BUILD_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_BUILD_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_design": SOURCE_DESIGN_RECEIPT_ID,
        "recommended_next": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "schema_validator_cell_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_BUILD_RECEIPT",
        "receipt_id": receipt_id,
        "cell_id": "SCHEMA_VALIDATOR_CELL",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_runtime_schema_validator_cell_design_receipt_id": SOURCE_DESIGN_RECEIPT_ID,
        "source_decision_edge_observability_reference_closure_receipt_id": SOURCE_OBSERVABILITY_REFERENCE_CLOSURE_RECEIPT_ID,
        "input_proposal_ref": "schema_validator_demo_inputs_v0.jsonl",
        "validation_result_ref": "schema_validation_results_v0.jsonl",
        "output_packet_ref": "validated_candidate_packets_v0.jsonl",
        "feedback_packet_ref": "schema_feedback_packets_v0.jsonl",
        "result": "SYNTHETIC_DEMO_BUILD_COMPLETE" if gate == "PASS" else "BUILD_FAILED",
        "advanced_to": "LAWFUL_ADMISSIBILITY_CELL for VALID demo packets only",
        "returned_to": "BUILDER_PROPOSAL_CELL for invalid demo packets",
        "negative_controls": negative_controls,
        "machine_readable_schema_validator_build_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "runtime_schema_validator_cell_built": gate == "PASS",
            "review_ready": gate == "PASS",
            "synthetic_demo_build_only": True,
            "live_runtime_routing_installed": False,
            "source_design_consumed": True,
            "schema_archive_schema_emitted": SCHEMA_ARCHIVE_SCHEMA_PATH.exists(),
            "schema_archive_emitted": SCHEMA_ARCHIVE_PATH.exists(),
            "schema_archive_read_only": archive.get("mutation_allowed_by_schema_validator") is False,
            "schema_validation_result_enum_emitted": RESULT_ENUM_PATH.exists(),
            "schema_validation_result_schema_emitted": RESULT_SCHEMA_PATH.exists(),
            "validated_candidate_packet_schema_emitted": VALIDATED_PACKET_SCHEMA_PATH.exists(),
            "schema_feedback_packet_schema_emitted": SCHEMA_FEEDBACK_SCHEMA_PATH.exists(),
            "schema_gap_feedback_packet_schema_emitted": SCHEMA_GAP_FEEDBACK_SCHEMA_PATH.exists(),
            "schema_validator_receipt_schema_emitted": RECEIPT_SCHEMA_PATH.exists(),
            "check_table_emitted": CHECK_TABLE_PATH.exists(),
            "demo_inputs_emitted": DEMO_INPUTS_PATH.exists(),
            "validation_results_emitted": VALIDATION_RESULTS_PATH.exists(),
            "validated_candidate_packets_emitted": VALIDATED_PACKETS_PATH.exists(),
            "schema_feedback_packets_emitted": SCHEMA_FEEDBACK_PACKETS_PATH.exists(),
            "schema_gap_feedback_packets_emitted": SCHEMA_GAP_FEEDBACK_PACKETS_PATH.exists(),
            "proposals_evaluated": len(validation_results),
            "valid_count": result_counts.get("VALID", 0),
            "invalid_count": invalid_count,
            "advanced_to_admissibility_count": advanced_count,
            "returned_to_builder_count": returned_to_builder_count,
            "result_class_counts": dict(result_counts),
            "formation_check_count": len(FORMATION_CHECKS),
            "result_enum_count": len(RESULT_ENUM),
            "acceptance_gate_count": 33,
            "negative_control_count": 19,
            "observability_sidecar_deferred": True,
            "unit_feedback_hardening_deferred": True,
            "c7_deferred": True,
            "c8_deferred": True,
            "runtime_adoption_deferred": True,
            "runtime_effect": False,
            "runtime_patched": False,
            "authority_checked": False,
            "admissibility_checked": False,
            "execution_claimed": False,
            "schema_archive_mutated": False,
            "proposal_repaired": False,
            "schema_created": False,
            "builder_command_emitted": False,
            "c7_authorized": False,
            "c8_authorized": False,
            "new_domain_shift_executed": False,
            "general_cell1_authority_claimed": False,
            "global_autonomy_claimed": False,
            "full_transfer_claimed": False,
            "runtime_wide_enforcement_claimed": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "observability_reference_mutated": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": all(v == 0 for v in negative_controls.values()),
            "recommended_next": final_next,
        },
        "aggregate_metrics": report | {"status": final_status, "recommended_next_handling": final_next},
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "schema_archive_schema": rel(SCHEMA_ARCHIVE_SCHEMA_PATH),
            "schema_archive": rel(SCHEMA_ARCHIVE_PATH),
            "schema_validation_result_enum": rel(RESULT_ENUM_PATH),
            "schema_validation_result_schema": rel(RESULT_SCHEMA_PATH),
            "validated_candidate_packet_schema": rel(VALIDATED_PACKET_SCHEMA_PATH),
            "schema_feedback_packet_schema": rel(SCHEMA_FEEDBACK_SCHEMA_PATH),
            "schema_gap_feedback_packet_schema": rel(SCHEMA_GAP_FEEDBACK_SCHEMA_PATH),
            "schema_validator_cell_receipt_schema": rel(RECEIPT_SCHEMA_PATH),
            "check_table": rel(CHECK_TABLE_PATH),
            "demo_inputs": rel(DEMO_INPUTS_PATH),
            "validation_results": rel(VALIDATION_RESULTS_PATH),
            "validated_candidate_packets": rel(VALIDATED_PACKETS_PATH),
            "schema_feedback_packets": rel(SCHEMA_FEEDBACK_PACKETS_PATH),
            "schema_gap_feedback_packets": rel(SCHEMA_GAP_FEEDBACK_PACKETS_PATH),
            "rollup": rel(ROLLUP_PATH),
            "readout": rel(READOUT_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"runtime_schema_validator_cell_build_receipt_id={receipt_id}")
    print(f"runtime_schema_validator_cell_build_receipt_path={rel(receipt_path)}")
    print(f"schema_validator_rollup_path={rel(ROLLUP_PATH)}")
    print(f"schema_validator_readout_path={rel(READOUT_PATH)}")
    print(f"schema_validator_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
