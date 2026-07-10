#!/usr/bin/env python3

"""Build VS1.1 post-VS0 source intake from committed source artifacts."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT = "scripts/build_phase_vs1_post_vs0_source_intake_v0.py"
EXPECTED_HEAD = "f8c51de1beb0cad8e918325acc9a6028a87206ae"
OUTPUT_JSON = "docs/matrixlabs/phase_vs1/phase_vs1_post_vs0_source_intake_v0.json"
OUTPUT_MD = "docs/matrixlabs/phase_vs1/phase_vs1_post_vs0_source_intake_v0.md"

DIRECTION_JSON = "docs/matrixlabs/phase_vs1/post_vs0_direction_decision_receipt_v0.json"
DIRECTION_MD = "docs/matrixlabs/phase_vs1/post_vs0_direction_decision_receipt_v0.md"
VS0_1_JSON = "docs/matrixlabs/phase_vs0/phase_vs0_source_inventory_v0.json"
VS0_2_JSON = "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_build_receipt_v0.json"
VS0_3_JSON = "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_verification_v0.json"
NEGATIVE_ROOT = (
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/"
    "negative_probes"
)
VS0_4_JSON = f"{NEGATIVE_ROOT}/phase_vs0_negative_probe_battery_v0.json"
VS0_5_JSON = "docs/matrixlabs/phase_vs0/phase_vs0_evidence_yield_report_v0.json"
VS0_6_JSON = "docs/matrixlabs/phase_vs0/phase_vs0_closure_v0.json"
CHAIN_INDEX_JSON = (
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/"
    "a_to_f/phase_vs0_a_to_f_chain_index_v0.json"
)

VS0_1_STATUS = "VS0_PREFLIGHT_PASS_SCOPE_DECLARED"
VS0_2_STATUS = "VS0_2_HAPPY_PATH_BUILD_PASS_A_TO_F_PHASE_SPECIMEN_CREATED"
VS0_3_STATUS = "VS0_3_HAPPY_PATH_VERIFICATION_PASS_A_TO_F_PHASE_SPECIMEN_VERIFIED"
VS0_4_STATUS = "VS0_4_NEGATIVE_PROBES_PASS_TYPED_STOPS"
VS0_5_STATUS = "VS0_5_EVIDENCE_YIELD_REPORT_PASS_USEFUL_EVIDENCE_PRESENT"
VS0_6_STATUS = (
    "PHASE_VS0_PASS_FIRST_A_TO_F_SPECIMEN_WITH_TYPED_NEGATIVE_STOPS_"
    "AND_EVIDENCE_YIELD"
)
VS0_6_GATE = (
    "VS0_6_PHASE_CLOSURE_PASS_FIRST_A_TO_F_SPECIMEN_WITH_TYPED_STOPS_"
    "AND_EVIDENCE_YIELD"
)
DIRECTION_GATE = "POST_VS0_DIRECTION_DECISION_RECEIPT_PASS"
PASS_VERDICT = "VS1_1_POST_VS0_SOURCE_INTAKE_PASS"
TERMINAL_TRANSITION = "ADVANCE(VS1_2_CONTROLLED_LOOP_CONTRACT_DEFINITION_PENDING)"
PRINT_TRANSITION = (
    "ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS1_POST_VS0_SOURCE_INTAKE_V0_PENDING)"
)

FORBIDDEN_ARTIFACTS = [
    "scripts/build_phase_vs1_controlled_convergence_loop_contract_v0.py",
    "docs/matrixlabs/phase_vs1/phase_vs1_controlled_convergence_loop_contract_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_controlled_convergence_loop_contract_v0.md",
    "docs/matrixlabs/runner",
    "docs/matrixlabs/runtime",
    "docs/matrixlabs/move_space",
    "docs/matrixlabs/micro_sweeps",
]


class IntakeFailure(RuntimeError):
    def __init__(
        self,
        code: str,
        *,
        source: str = "NONE",
        field: str = "NONE",
        expected: object = "NONE",
        actual: object = "NONE",
        next_surface: str = "REPAIR_VS1_1_SOURCE_INTAKE_INPUT",
    ) -> None:
        super().__init__(code)
        self.code = code
        self.source = source
        self.field = field
        self.expected = expected
        self.actual = actual
        self.next_surface = next_surface


def fail(
    code: str,
    *,
    source: str = "NONE",
    field: str = "NONE",
    expected: object = "NONE",
    actual: object = "NONE",
    next_surface: str = "REPAIR_VS1_1_SOURCE_INTAKE_INPUT",
) -> None:
    raise IntakeFailure(
        code,
        source=source,
        field=field,
        expected=expected,
        actual=actual,
        next_surface=next_surface,
    )


def run_git(root: Path, args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(
            "STOP_VS1_1_SOURCE_IDENTITY_UNVERIFIED",
            source="git",
            field="git_command",
            expected="success",
            actual=proc.stderr.strip(),
        )
    return proc.stdout.rstrip()


def detect_repo_root(start: Path) -> Path:
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(
            "STOP_VS1_1_SOURCE_IDENTITY_UNVERIFIED",
            source="repo",
            field="repo_root",
            expected="git repository",
            actual=proc.stderr.strip(),
        )
    return Path(proc.stdout.strip()).resolve()


def status_path(line: str) -> str:
    path = line[3:].strip()
    if " -> " in path:
        path = path.split(" -> ", 1)[1].strip()
    return path


def validate_dirty_scope(root: Path) -> None:
    allowed_exact = {
        SCRIPT,
        "scripts/build_baseline_share_v0.py",
        OUTPUT_JSON,
        OUTPUT_MD,
    }
    allowed_prefixes = ("baseline_share/", "discussion_packets/")
    for line in run_git(root, ["status", "--short", "--untracked-files=all"]).splitlines():
        path = status_path(line)
        if path in allowed_exact or any(path.startswith(p) for p in allowed_prefixes):
            continue
        if path.startswith("docs/matrixlabs/phase_vs0/"):
            fail(
                "STOP_VS1_1_VS0_SOURCE_MUTATED",
                source=path,
                field="dirty_scope",
                expected="no dirty VS0 source artifacts",
                actual=line,
            )
        if path in {DIRECTION_JSON, DIRECTION_MD}:
            fail(
                "STOP_VS1_1_DIRECTION_RECEIPT_MUTATED",
                source=path,
                field="dirty_scope",
                expected="direction receipt unchanged",
                actual=line,
            )
        fail(
            "STOP_VS1_1_FORBIDDEN_INPUT_USED",
            source=path,
            field="dirty_scope",
            expected="only VS1.1 output, baseline_share, or discussion_packets",
            actual=line,
        )


def require_head(root: Path) -> None:
    head = run_git(root, ["rev-parse", "HEAD"])
    if head != EXPECTED_HEAD:
        fail(
            "STOP_VS1_1_SOURCE_IDENTITY_UNVERIFIED",
            source="HEAD",
            field="commit_sha",
            expected=EXPECTED_HEAD,
            actual=head,
        )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(root: Path, rel_path: str, missing_code: str) -> dict[str, Any]:
    path = root / rel_path
    if not path.is_file():
        fail(
            missing_code,
            source=rel_path,
            field="file_presence",
            expected=True,
            actual=False,
        )
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(
            missing_code,
            source=rel_path,
            field="valid_json",
            expected=True,
            actual=str(exc),
        )
    if not isinstance(value, dict):
        fail(
            missing_code,
            source=rel_path,
            field="json_object",
            expected=True,
            actual=type(value).__name__,
        )
    return value


def get_value(obj: dict[str, Any], path: str, default: Any = None) -> Any:
    cur: Any = obj
    for part in path.split("."):
        if not isinstance(cur, dict):
            return default
        cur = cur.get(part, default)
    return cur


def require_equal(
    value: Any,
    expected: Any,
    code: str,
    source: str,
    field: str,
) -> None:
    if value != expected:
        fail(
            code,
            source=source,
            field=field,
            expected=expected,
            actual=value,
        )


def ensure_forbidden_artifacts_absent(root: Path) -> None:
    existing = [path for path in FORBIDDEN_ARTIFACTS if (root / path).exists()]
    if existing:
        fail(
            "STOP_VS1_1_VS1_2_ARTIFACT_CREATED",
            source="forbidden_artifacts",
            field="path_presence",
            expected=[],
            actual=existing,
        )


def verify_direction_receipt(direction: dict[str, Any]) -> None:
    require_equal(direction.get("receipt_gate"), DIRECTION_GATE, "STOP_VS1_1_POST_VS0_DIRECTION_DECISION_MISSING", DIRECTION_JSON, "receipt_gate")
    require_equal(get_value(direction, "decision.decision_status"), "POST_VS0_DIRECTION_DECISION_ACCEPTED", "STOP_VS1_1_POST_VS0_DIRECTION_DECISION_MISSING", DIRECTION_JSON, "decision.decision_status")
    require_equal(get_value(direction, "decision.decision"), "DECISION_OPEN_PHASE_VS1_SOURCE_INTAKE", "STOP_VS1_1_POST_VS0_DIRECTION_DECISION_MISSING", DIRECTION_JSON, "decision.decision")
    require_equal(get_value(direction, "decision.decision_scope"), "VS1_SOURCE_INTAKE_AND_CONTRACT_DEFINITION_PREPARATION_ONLY", "STOP_VS1_1_POST_VS0_DIRECTION_DECISION_MISSING", DIRECTION_JSON, "decision.decision_scope")
    for field in [
        "controlled_loop_execution_authorized",
        "runner_creation_authorized",
        "runner_authority_created",
        "move_execution_authorized",
        "micro_sweeps_authorized",
        "registry_activation_authorized",
        "registry_promotion_authorized",
        "trace_generalization_authorized",
        "performance_claim_authorized",
        "scale_claim_authorized",
        "total_coverage_claim_authorized",
        "next_phase_selected_by_machine",
        "vs1_1_executed_by_this_receipt",
        "vs1_2_executed_by_this_receipt",
    ]:
        require_equal(
            get_value(direction, f"forbidden_scope.{field}"),
            False,
            "STOP_VS1_1_POST_VS0_DIRECTION_AUTHORITY_OVERBROAD",
            DIRECTION_JSON,
            f"forbidden_scope.{field}",
        )
    require_equal(get_value(direction, "next_unit.next_unit_authorized_scope"), "SOURCE_INTAKE_ONLY", "STOP_VS1_1_INTAKE_SCOPE_OVERBROAD", DIRECTION_JSON, "next_unit.next_unit_authorized_scope")
    require_equal(get_value(direction, "next_unit.next_unit_execution_performed_by_this_receipt"), False, "STOP_VS1_1_INTAKE_SCOPE_OVERBROAD", DIRECTION_JSON, "next_unit.next_unit_execution_performed_by_this_receipt")


def verify_vs0_chain(
    vs0_1: dict[str, Any],
    vs0_2: dict[str, Any],
    vs0_3: dict[str, Any],
    vs0_4: dict[str, Any],
    vs0_5: dict[str, Any],
    vs0_6: dict[str, Any],
) -> None:
    require_equal(vs0_1.get("inventory_status"), VS0_1_STATUS, "STOP_VS1_1_MISSING_VS0_SOURCE_CHAIN", VS0_1_JSON, "inventory_status")
    require_equal(vs0_2.get("happy_path_build_status"), VS0_2_STATUS, "STOP_VS1_1_MISSING_VS0_SOURCE_CHAIN", VS0_2_JSON, "happy_path_build_status")
    require_equal(get_value(vs0_3, "verification_result.happy_path_verification_status"), VS0_3_STATUS, "STOP_VS1_1_MISSING_VS0_SOURCE_CHAIN", VS0_3_JSON, "verification_result.happy_path_verification_status")
    require_equal(get_value(vs0_4, "battery_result.negative_probe_battery_status"), VS0_4_STATUS, "STOP_VS1_1_MISSING_VS0_SOURCE_CHAIN", VS0_4_JSON, "battery_result.negative_probe_battery_status")
    require_equal(get_value(vs0_5, "yield_result.evidence_yield_report_status"), VS0_5_STATUS, "STOP_VS1_1_EVIDENCE_YIELD_MISSING", VS0_5_JSON, "yield_result.evidence_yield_report_status")
    require_equal(vs0_6.get("phase_status"), VS0_6_STATUS, "STOP_VS1_1_VS0_NOT_CLOSED", VS0_6_JSON, "phase_status")
    require_equal(vs0_6.get("closure_gate"), VS0_6_GATE, "STOP_VS1_1_VS0_NOT_CLOSED", VS0_6_JSON, "closure_gate")
    require_equal(get_value(vs0_6, "closure_claim_scope.phase_vs0_closed"), True, "STOP_VS1_1_VS0_NOT_CLOSED", VS0_6_JSON, "closure_claim_scope.phase_vs0_closed")


def verify_evidence_and_boundaries(
    vs0_4: dict[str, Any],
    vs0_5: dict[str, Any],
    vs0_6: dict[str, Any],
) -> None:
    for path in [
        "yield_result.confirmation_yield_present",
        "yield_result.diagnostic_yield_present",
        "yield_result.decision_relevant_evidence_present",
    ]:
        require_equal(get_value(vs0_5, path), True, "STOP_VS1_1_EVIDENCE_YIELD_MISSING", VS0_5_JSON, path)

    expected_probe_fields = {
        "probe_summary.probe_count_expected": 10,
        "probe_summary.probe_count_run": 10,
        "probe_summary.expected_typed_stop_count": 10,
        "probe_summary.observed_typed_stop_count": 10,
        "probe_summary.unexpected_pass_count": 0,
        "probe_summary.ambiguous_stop_count": 0,
        "probe_summary.diagnostic_fields_missing_count": 0,
        "probe_summary.next_lawful_surface_missing_count": 0,
        "probe_summary.self_repair_attempt_count": 0,
        "probe_summary.happy_path_mutation_count": 0,
        "probe_summary.canonical_source_chain_mutation_count": 0,
        "battery_result.all_expected_stop_codes_matched": True,
        "battery_result.all_stops_typed": True,
    }
    for path, expected in expected_probe_fields.items():
        require_equal(get_value(vs0_4, path), expected, "STOP_VS1_1_NEGATIVE_STOP_EVIDENCE_UNUSABLE", VS0_4_JSON, path)

    boundary_false = {
        "confirmed_boundaries.active_registry_created": "STOP_VS1_1_VS0_BOUNDARY_DRIFT",
        "confirmed_boundaries.trace_generalized": "STOP_VS1_1_VS0_BOUNDARY_DRIFT",
        "confirmed_boundaries.runner_authority_created": "STOP_VS1_1_VS0_BOUNDARY_DRIFT",
        "confirmed_boundaries.runner_readiness_claimed": "STOP_VS1_1_VS0_BOUNDARY_DRIFT",
        "confirmed_boundaries.performance_optimization_claimed": "STOP_VS1_1_VS0_BOUNDARY_DRIFT",
        "confirmed_boundaries.scale_optimization_claimed": "STOP_VS1_1_VS0_BOUNDARY_DRIFT",
        "confirmed_boundaries.next_unit_executed": "STOP_VS1_1_VS0_BOUNDARY_DRIFT",
        "confirmed_boundaries.additional_machine_proceed_authorized": "STOP_VS1_1_VS0_BOUNDARY_DRIFT",
        "coverage_boundary.all_possible_illegal_shortcuts_tested": "STOP_VS1_1_VS0_BOUNDARY_DRIFT",
        "coverage_boundary.future_live_runtime_coverage_claimed": "STOP_VS1_1_VS0_BOUNDARY_DRIFT",
        "next_lawful_surface.surface_artifact_created_by_closure": "STOP_VS1_1_NEXT_SURFACE_STATUS_UNSAFE",
        "next_lawful_surface.machine_may_select_next_phase": "STOP_VS1_1_NEXT_SURFACE_STATUS_UNSAFE",
        "next_lawful_surface.next_phase_auto_selected": "STOP_VS1_1_NEXT_SURFACE_STATUS_UNSAFE",
    }
    for path, code in boundary_false.items():
        require_equal(get_value(vs0_6, path), False, code, VS0_6_JSON, path)
    require_equal(get_value(vs0_6, "next_lawful_surface.surface_name"), "POST_VS0_DIRECTION_DECISION_SURFACE", "STOP_VS1_1_NEXT_SURFACE_STATUS_UNSAFE", VS0_6_JSON, "next_lawful_surface.surface_name")
    require_equal(get_value(vs0_6, "next_lawful_surface.human_decision_required"), True, "STOP_VS1_1_NEXT_SURFACE_STATUS_UNSAFE", VS0_6_JSON, "next_lawful_surface.human_decision_required")


def git_tracked_paths(root: Path, prefix: str) -> list[str]:
    out = run_git(root, ["ls-files", prefix])
    return sorted(line for line in out.splitlines() if line)


def collect_hash_paths(root: Path, vs0_4: dict[str, Any], chain_index: dict[str, Any]) -> list[str]:
    paths = [DIRECTION_JSON, DIRECTION_MD]
    paths.extend(git_tracked_paths(root, "docs/matrixlabs/phase_vs0"))
    for probe in vs0_4.get("probe_results", []):
        receipt_path = probe.get("receipt_path")
        if isinstance(receipt_path, str):
            paths.append(receipt_path)
    for artifact in chain_index.get("artifacts", []):
        artifact_path = artifact.get("path")
        if isinstance(artifact_path, str):
            paths.append(artifact_path)
    unique = sorted(dict.fromkeys(paths))
    missing = [path for path in unique if not (root / path).is_file()]
    if missing:
        fail(
            "STOP_VS1_1_MISSING_VS0_SOURCE_CHAIN",
            source="source_hash_paths",
            field="file_presence",
            expected="all source paths present",
            actual=missing,
        )
    return unique


def hash_paths(root: Path, paths: list[str]) -> dict[str, str]:
    return {path: sha256(root / path) for path in paths}


def fail_for_hash_mutation(before: dict[str, str], after: dict[str, str]) -> None:
    if before == after:
        return
    changed = [path for path, digest in before.items() if after.get(path) != digest]
    if any(path in {DIRECTION_JSON, DIRECTION_MD} for path in changed):
        code = "STOP_VS1_1_DIRECTION_RECEIPT_MUTATED"
    elif any(path == VS0_6_JSON for path in changed):
        code = "STOP_VS1_1_VS0_CLOSURE_MUTATED"
    else:
        code = "STOP_VS1_1_VS0_SOURCE_MUTATED"
    fail(
        code,
        source="source_preservation",
        field="changed_paths",
        expected=[],
        actual=changed,
    )


def source_chain_status() -> dict[str, str]:
    return {
        "vs0_1_source_inventory": "PRESENT_VERIFIED",
        "vs0_2_happy_path_build": "PRESENT_VERIFIED",
        "vs0_3_happy_path_verification": "PRESENT_VERIFIED",
        "vs0_4_negative_probe_battery": "PRESENT_VERIFIED",
        "vs0_5_evidence_yield_report": "PRESENT_VERIFIED",
        "vs0_6_phase_closure": "PRESENT_VERIFIED",
        "post_vs0_direction_decision_receipt": "PRESENT_VERIFIED",
    }


def source_status_table() -> dict[str, dict[str, Any]]:
    return {
        "post_vs0_direction_decision_receipt": {
            "status": "PRESENT_VERIFIED",
            "required_gate": DIRECTION_GATE,
            "passed": True,
        },
        "vs0_1_source_inventory": {
            "status": "PRESENT_VERIFIED",
            "required_status": VS0_1_STATUS,
            "passed": True,
        },
        "vs0_2_happy_path_build": {
            "status": "PRESENT_VERIFIED",
            "required_status": VS0_2_STATUS,
            "passed": True,
        },
        "vs0_3_happy_path_verification": {
            "status": "PRESENT_VERIFIED",
            "required_status": VS0_3_STATUS,
            "passed": True,
        },
        "vs0_4_negative_probe_battery": {
            "status": "PRESENT_VERIFIED",
            "required_status": VS0_4_STATUS,
            "passed": True,
        },
        "vs0_5_evidence_yield_report": {
            "status": "PRESENT_VERIFIED",
            "required_status": VS0_5_STATUS,
            "passed": True,
        },
        "vs0_6_phase_closure": {
            "status": "PRESENT_VERIFIED",
            "required_status": VS0_6_STATUS,
            "passed": True,
        },
    }


def build_intake(direction_hash: str, closure_hash: str, source_hashes: dict[str, str]) -> dict[str, Any]:
    return {
        "schema_version": "matrixlabs_phase_vs1_post_vs0_source_intake_v0",
        "artifact_id": "phase_vs1_post_vs0_source_intake_v0",
        "phase_id": "PHASE_VS1",
        "unit_id": "VS1.1_POST_VS0_SOURCE_INTAKE",
        "unit_role": "SOURCE_INTAKE_ONLY",
        "source_phase": "PHASE_VS0",
        "source_authority_basis": {
            "post_vs0_direction_decision_required": True,
            "decision_artifact": "post_vs0_direction_decision_receipt_v0",
            "decision_artifact_path": DIRECTION_JSON,
            "decision_artifact_commit_sha": EXPECTED_HEAD,
            "decision_artifact_sha256": direction_hash,
            "required_decision": "DECISION_OPEN_PHASE_VS1_SOURCE_INTAKE",
            "required_decision_status": "POST_VS0_DIRECTION_DECISION_ACCEPTED",
            "allowed_scope": "VS1_SOURCE_INTAKE_AND_CONTRACT_DEFINITION_PREPARATION_ONLY",
            "loop_execution_authorized": False,
            "runner_authority_created": False,
            "move_execution_authorized": False,
            "micro_sweeps_authorized": False,
            "registry_activation_authorized": False,
            "trace_generalization_authorized": False,
            "performance_claim_authorized": False,
            "next_phase_selected_by_machine": False,
            "machine_may_select_next_phase": False,
        },
        "source_vs0_6_closure_binding": {
            "source_vs0_6_closure_commit_sha": "18324fd7d82da4a5f9210c1e30d94e8fe5ed783b",
            "source_vs0_6_closure_id": "phase_vs0_closure_v0",
            "source_vs0_6_closure_path": VS0_6_JSON,
            "source_vs0_6_closure_sha256": closure_hash,
            "source_vs0_6_closure_gate": VS0_6_GATE,
            "source_vs0_6_phase_status": VS0_6_STATUS,
            "source_vs0_6_phase_vs0_closed": True,
            "source_vs0_6_required_before_intake": True,
        },
        "source_chain": source_chain_status(),
        "source_identity_snapshot": {
            "source_hashes_verified": True,
            "source_commits_recorded": True,
            "latest_file_resolution_used": False,
            "mtime_resolution_used": False,
            "directory_scan_authority_used": False,
            "baseline_share_used_as_source_authority": False,
            "discussion_packets_used_as_source_authority": False,
            "chat_memory_used_as_source_authority": False,
            "source_hashes": source_hashes,
        },
        "source_status_table": source_status_table(),
        "intake_checks": {
            "post_vs0_direction_basis": "POST_VS0_DIRECTION_DECISION_ACCEPTED",
            "vs0_source_chain": "VS0_SOURCE_CHAIN_PRESENT",
            "vs0_source_identity": "VS0_SOURCE_IDENTITY_VERIFIED",
            "vs0_closure_status": "VS0_CLOSURE_STATUS_ACCEPTED",
            "evidence_yield": "VS0_EVIDENCE_YIELD_PRESENT",
            "typed_negative_stops": "VS0_TYPED_NEGATIVE_STOPS_ACCEPTED",
            "boundary_preservation": "VS0_BOUNDARY_PRESERVATION_PASS",
            "next_lawful_surface_status": "POST_VS0_NEXT_SURFACE_STATUS_ACCEPTED",
            "intake_scope": "VS1_1_INTAKE_SCOPE_NON_EXECUTABLE",
        },
        "evidence_yield_status": {
            "confirmation_yield_present": True,
            "diagnostic_yield_present": True,
            "decision_relevant_evidence_present": True,
            "evidence_yield_implies_optimization": False,
        },
        "negative_probe_status": {
            "selected_probe_battery_passed": True,
            "typed_negative_stops_present": True,
            "expected_stop_codes_matched": True,
            "unexpected_passes_absent": True,
            "ambiguous_stops_absent": True,
            "missing_diagnostic_fields_absent": True,
            "missing_next_lawful_surfaces_absent": True,
            "self_repair_attempts_absent": True,
            "happy_path_mutations_absent": True,
            "canonical_source_chain_mutations_absent": True,
            "total_illegal_path_coverage_claimed": False,
            "future_live_runtime_coverage_claimed": False,
        },
        "boundary_preservation_status": {
            "active_registry_created": False,
            "registry_candidate_promoted": False,
            "trace_generalized": False,
            "runner_authority_created": False,
            "runner_readiness_claimed": False,
            "performance_optimization_claimed": False,
            "scale_optimization_claimed": False,
            "next_unit_execution_authorized": False,
            "additional_machine_proceed_authorized": False,
            "controlled_loop_execution_authorized": False,
            "move_execution_authorized": False,
            "micro_sweeps_authorized": False,
        },
        "next_lawful_surface_status": {
            "named_surface": "POST_VS0_DIRECTION_DECISION_SURFACE",
            "surface_artifact_created_by_vs0_6": False,
            "human_decision_required": True,
            "machine_may_select_next_phase": False,
            "next_phase_auto_selected": False,
            "recommended_options_non_binding": True,
        },
        "accepted_input_scope": {
            "scope": "BOUNDED_LOCAL_VS0_EVIDENCE_CHAIN_ONLY",
            "may_feed_vs1_2_contract_definition": True,
            "may_feed_loop_execution": False,
            "may_feed_runner_creation": False,
            "may_feed_move_execution": False,
            "may_feed_micro_sweeps": False,
            "may_feed_registry_activation": False,
            "may_feed_trace_generalization": False,
            "may_feed_optimization_claim": False,
        },
        "forbidden_input_scope": [
            "runner authority",
            "generalized trace",
            "active registry",
            "optimization claim",
            "global portability claim",
            "future runtime coverage claim",
            "multi-specimen stability claim",
            "machine-selected next phase",
            "controlled-loop readiness",
            "loop execution authority",
        ],
        "vs1_2_boundary": {
            "vs1_2_contract_definition_may_start": True,
            "vs1_2_contract_defined": False,
            "vs1_2_contract_validated": False,
            "controlled_loop_contract_exists": False,
            "controlled_loop_preconditions_passed": False,
            "vs1_2_execution_authorized": False,
            "vs1_2_contract_definition_may_be_prepared_after_commit": True,
            "controlled_loop_readiness_audited": False,
            "controlled_loop_execution_authorized": False,
        },
        "source_preservation": {
            "post_vs0_direction_decision_receipt_mutated_by_vs1_1": False,
            "vs0_1_source_inventory_mutated_by_vs1_1": False,
            "vs0_2_happy_path_build_mutated_by_vs1_1": False,
            "vs0_3_happy_path_verification_mutated_by_vs1_1": False,
            "vs0_4_negative_probe_battery_mutated_by_vs1_1": False,
            "vs0_5_evidence_yield_report_mutated_by_vs1_1": False,
            "vs0_6_phase_closure_mutated_by_vs1_1": False,
            "a_to_f_artifacts_mutated_by_vs1_1": False,
            "negative_probe_receipts_mutated_by_vs1_1": False,
        },
        "receipt_obligations": {
            "source_artifacts_consumed": True,
            "source_status_table_emitted": True,
            "boundary_checks_emitted": True,
            "accepted_non_claims_emitted": True,
            "forbidden_inferences_checked": True,
            "terminal_transition_emitted": True,
        },
        "intake_verdict": PASS_VERDICT,
        "terminal_transition": TERMINAL_TRANSITION,
        "failures": [],
    }


def render_markdown() -> str:
    return """# Phase VS1.1 post-VS0 source intake v0

## Status

VS1_1_POST_VS0_SOURCE_INTAKE_PASS

## Source authority basis

- direction receipt: post_vs0_direction_decision_receipt_v0
- direction receipt commit: f8c51de1beb0cad8e918325acc9a6028a87206ae
- decision: DECISION_OPEN_PHASE_VS1_SOURCE_INTAKE
- decision scope: VS1_SOURCE_INTAKE_AND_CONTRACT_DEFINITION_PREPARATION_ONLY
- machine selected next phase: false

## VS0 source admitted

- source phase: PHASE_VS0
- VS0.1 source inventory: PRESENT_VERIFIED
- VS0.2 happy-path A\u2192F build: PRESENT_VERIFIED
- VS0.3 happy-path verification: PRESENT_VERIFIED
- VS0.4 negative probe battery: PRESENT_VERIFIED
- VS0.5 Evidence Yield report: PRESENT_VERIFIED
- VS0.6 phase closure: PRESENT_VERIFIED

## Intake result

- intake verdict: VS1_1_POST_VS0_SOURCE_INTAKE_PASS
- accepted input scope: BOUNDED_LOCAL_VS0_EVIDENCE_CHAIN_ONLY
- may feed VS1.2 contract definition: true
- may feed loop execution: false

## Evidence Yield

- Confirmation Yield present: true
- Diagnostic Yield present: true
- decision-relevant evidence present: true
- Evidence Yield implies optimization: false

## Typed negative stops

- selected probe battery passed: true
- typed negative stops present: true
- unexpected passes absent: true
- ambiguous stops absent: true
- missing diagnostic fields absent: true
- missing next lawful surfaces absent: true
- self-repair attempts absent: true

## Boundaries preserved

- active registry created: false
- registry candidate promoted: false
- trace generalized: false
- runner authority created: false
- runner readiness claimed: false
- performance optimization claimed: false
- scale optimization claimed: false
- controlled loop execution authorized: false
- move execution authorized: false
- micro-sweeps authorized: false

## VS1.2 boundary

- VS1.2 contract definition may start: true
- VS1.2 contract defined: false
- controlled loop contract exists: false
- controlled loop preconditions passed: false
- controlled loop execution authorized: false

## Terminal transition

ADVANCE(VS1_2_CONTROLLED_LOOP_CONTRACT_DEFINITION_PENDING)

## Non-claim

VS1.1 admits VS0 only as bounded local evidence for VS1.2 contract-definition preparation. It does not define the loop contract, inventory component presence, certify readiness, authorize execution, create a runner, create move-space, run micro-sweeps, activate a registry, generalize the trace, claim portability, claim optimization, or select the next phase by machine authority.
"""


def markdown_contains_vs1_1_overclaim(md: str) -> list[str]:
    allowed_patterns = [
        r"\bcontrolled loop execution authorized\s*[:=]\s*false\b",
        r"\bmove execution authorized\s*[:=]\s*false\b",
        r"\bmicro-sweeps authorized\s*[:=]\s*false\b",
        r"\brunner authority created\s*[:=]\s*false\b",
        r"\brunner readiness claimed\s*[:=]\s*false\b",
        r"\bactive registry created\s*[:=]\s*false\b",
        r"\bregistry candidate promoted\s*[:=]\s*false\b",
        r"\btrace generalized\s*[:=]\s*false\b",
        r"\bperformance optimization claimed\s*[:=]\s*false\b",
        r"\bscale optimization claimed\s*[:=]\s*false\b",
        r"\bevidence yield implies optimization\s*[:=]\s*false\b",
        r"\bmachine selected next phase\s*[:=]\s*false\b",
        r"\bmay feed loop execution\s*[:=]\s*false\b",
        r"\bvs1\.2 contract defined\s*[:=]\s*false\b",
        r"\bcontrolled loop contract exists\s*[:=]\s*false\b",
        r"\bcontrolled loop preconditions passed\s*[:=]\s*false\b",
        r"\bdoes not define the loop contract\b",
        r"\bdoes not .*inventory component presence\b",
        r"\bdoes not .*certify readiness\b",
        r"\bdoes not .*authorize execution\b",
        r"\bdoes not .*create a runner\b",
        r"\bdoes not .*create move-space\b",
        r"\bdoes not .*run micro-sweeps\b",
        r"\bdoes not .*activate a registry\b",
        r"\bdoes not .*generalize the trace\b",
        r"\bdoes not .*claim portability\b",
        r"\bdoes not .*claim optimization\b",
        r"\bdoes not .*select the next phase by machine authority\b",
        r"\badmits vs0 only as bounded local evidence\b",
    ]
    forbidden_patterns = {
        "runner ready": r"\brunner ready\b",
        "runtime ready": r"\bruntime ready\b",
        "registry active": r"\bregistry active\b",
        "registry promoted": r"\bregistry promoted\b",
        "controlled loop ready": r"\bcontrolled loop ready\b",
        "controlled loop executing": r"\bcontrolled loop executing\b",
        "micro-sweeps authorized": r"\bmicro-sweeps authorized\b",
        "move execution authorized": r"\bmove execution authorized\b",
        "system safe": r"\bsystem safe\b",
        "all shortcuts covered": r"\ball shortcuts covered\b",
        "total coverage": r"\btotal coverage\b",
        "performance improved": r"\bperformance improved\b",
        "scale improved": r"\bscale improved\b",
        "next phase selected by machine": r"\bnext phase selected by machine\b",
        "VS1.2 contract defined": r"\bvs1\.2 contract defined\b",
        "controlled loop contract exists": r"\bcontrolled loop contract exists\b",
        "controlled loop preconditions passed": r"\bcontrolled loop preconditions passed\b",
    }
    hits: list[str] = []
    for lineno, raw_line in enumerate(md.splitlines(), start=1):
        line = raw_line.strip().lower()
        if not line:
            continue
        if any(re.search(pattern, line) for pattern in allowed_patterns):
            continue
        for label, pattern in forbidden_patterns.items():
            if re.search(pattern, line):
                hits.append(f"line {lineno}: {label}: {raw_line}")
    return hits


def write_json(root: Path, value: dict[str, Any]) -> None:
    path = root / OUTPUT_JSON
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_markdown(root: Path, value: str) -> None:
    path = root / OUTPUT_MD
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def print_complete() -> None:
    lines = [
        "BUILD_PHASE_VS1_POST_VS0_SOURCE_INTAKE_V0_COMPLETE",
        "artifact_id=phase_vs1_post_vs0_source_intake_v0",
        "schema_version=matrixlabs_phase_vs1_post_vs0_source_intake_v0",
        "phase_id=PHASE_VS1",
        "unit_id=VS1.1_POST_VS0_SOURCE_INTAKE",
        "unit_role=SOURCE_INTAKE_ONLY",
        "source_phase=PHASE_VS0",
        f"source_direction_decision_receipt_commit_sha={EXPECTED_HEAD}",
        f"source_direction_decision_receipt_gate={DIRECTION_GATE}",
        "source_vs0_6_closure_commit_sha=18324fd7d82da4a5f9210c1e30d94e8fe5ed783b",
        f"source_vs0_6_closure_gate={VS0_6_GATE}",
        f"source_vs0_6_phase_status={VS0_6_STATUS}",
        "post_vs0_direction_basis=POST_VS0_DIRECTION_DECISION_ACCEPTED",
        "vs0_source_chain=VS0_SOURCE_CHAIN_PRESENT",
        "vs0_source_identity=VS0_SOURCE_IDENTITY_VERIFIED",
        "vs0_closure_status=VS0_CLOSURE_STATUS_ACCEPTED",
        "evidence_yield=VS0_EVIDENCE_YIELD_PRESENT",
        "typed_negative_stops=VS0_TYPED_NEGATIVE_STOPS_ACCEPTED",
        "boundary_preservation=VS0_BOUNDARY_PRESERVATION_PASS",
        "next_lawful_surface_status=POST_VS0_NEXT_SURFACE_STATUS_ACCEPTED",
        "intake_scope=VS1_1_INTAKE_SCOPE_NON_EXECUTABLE",
        "confirmation_yield_present=true",
        "diagnostic_yield_present=true",
        "decision_relevant_evidence_present=true",
        "selected_probe_battery_passed=true",
        "typed_negative_stops_present=true",
        "active_registry_created=false",
        "registry_candidate_promoted=false",
        "trace_generalized=false",
        "runner_authority_created=false",
        "runner_readiness_claimed=false",
        "performance_optimization_claimed=false",
        "scale_optimization_claimed=false",
        "controlled_loop_execution_authorized=false",
        "move_execution_authorized=false",
        "micro_sweeps_authorized=false",
        "accepted_input_scope=BOUNDED_LOCAL_VS0_EVIDENCE_CHAIN_ONLY",
        "may_feed_vs1_2_contract_definition=true",
        "may_feed_loop_execution=false",
        "vs1_2_contract_definition_may_start=true",
        "vs1_2_contract_defined=false",
        "controlled_loop_contract_exists=false",
        "controlled_loop_preconditions_passed=false",
        "post_vs0_direction_decision_receipt_mutated_by_vs1_1=false",
        "vs0_1_source_inventory_mutated_by_vs1_1=false",
        "vs0_2_happy_path_build_mutated_by_vs1_1=false",
        "vs0_3_happy_path_verification_mutated_by_vs1_1=false",
        "vs0_4_negative_probe_battery_mutated_by_vs1_1=false",
        "vs0_5_evidence_yield_report_mutated_by_vs1_1=false",
        "vs0_6_phase_closure_mutated_by_vs1_1=false",
        "a_to_f_artifacts_mutated_by_vs1_1=false",
        "negative_probe_receipts_mutated_by_vs1_1=false",
        f"intake_verdict={PASS_VERDICT}",
        "commit_created=false",
        "push_executed=false",
        f"terminal_transition={PRINT_TRANSITION}",
    ]
    print("\n".join(lines))


def print_typed_stop(exc: IntakeFailure) -> None:
    lines = [
        "BUILD_PHASE_VS1_POST_VS0_SOURCE_INTAKE_V0_TYPED_STOP",
        "artifact_id=phase_vs1_post_vs0_source_intake_v0",
        "phase_id=PHASE_VS1",
        "unit_id=VS1.1_POST_VS0_SOURCE_INTAKE",
        f"intake_verdict={exc.code}",
        "yield_branch=DIAGNOSTIC_YIELD",
        f"missing_or_invalid_source={exc.source}",
        f"violating_field={exc.field}",
        f"expected_value={exc.expected}",
        f"actual_value={exc.actual}",
        f"next_lawful_surface={exc.next_surface}",
        "self_repair_performed=false",
        "loop_execution_authorized=false",
        "runner_authority_created=false",
        "commit_created=false",
        "push_executed=false",
        f"terminal_transition=STOP({exc.code})",
    ]
    print("\n".join(lines))


def run() -> int:
    root = detect_repo_root(Path.cwd())
    require_head(root)
    ensure_forbidden_artifacts_absent(root)
    validate_dirty_scope(root)

    direction = load_json(root, DIRECTION_JSON, "STOP_VS1_1_POST_VS0_DIRECTION_DECISION_MISSING")
    vs0_1 = load_json(root, VS0_1_JSON, "STOP_VS1_1_MISSING_VS0_SOURCE_CHAIN")
    vs0_2 = load_json(root, VS0_2_JSON, "STOP_VS1_1_MISSING_VS0_SOURCE_CHAIN")
    vs0_3 = load_json(root, VS0_3_JSON, "STOP_VS1_1_MISSING_VS0_SOURCE_CHAIN")
    vs0_4 = load_json(root, VS0_4_JSON, "STOP_VS1_1_MISSING_VS0_SOURCE_CHAIN")
    vs0_5 = load_json(root, VS0_5_JSON, "STOP_VS1_1_EVIDENCE_YIELD_MISSING")
    vs0_6 = load_json(root, VS0_6_JSON, "STOP_VS1_1_VS0_NOT_CLOSED")
    chain_index = load_json(root, CHAIN_INDEX_JSON, "STOP_VS1_1_MISSING_VS0_SOURCE_CHAIN")

    verify_direction_receipt(direction)
    verify_vs0_chain(vs0_1, vs0_2, vs0_3, vs0_4, vs0_5, vs0_6)
    verify_evidence_and_boundaries(vs0_4, vs0_5, vs0_6)

    hash_path_list = collect_hash_paths(root, vs0_4, chain_index)
    before_hashes = hash_paths(root, hash_path_list)
    markdown = render_markdown()
    overclaim_hits = markdown_contains_vs1_1_overclaim(markdown)
    if overclaim_hits:
        fail(
            "STOP_VS1_1_FORBIDDEN_INPUT_USED",
            source=OUTPUT_MD,
            field="markdown_overclaim_guard",
            expected=[],
            actual=overclaim_hits,
        )

    intake = build_intake(
        before_hashes[DIRECTION_JSON],
        before_hashes[VS0_6_JSON],
        before_hashes,
    )
    write_json(root, intake)
    write_markdown(root, markdown)

    after_hashes = hash_paths(root, hash_path_list)
    fail_for_hash_mutation(before_hashes, after_hashes)
    ensure_forbidden_artifacts_absent(root)
    validate_dirty_scope(root)
    print_complete()
    return 0


def main() -> int:
    try:
        return run()
    except IntakeFailure as exc:
        print_typed_stop(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
