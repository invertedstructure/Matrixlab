#!/usr/bin/env python3

"""Build the read-only Phase VS0.5 Evidence Yield report."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT = "scripts/build_phase_vs0_evidence_yield_report_v0.py"
EXPECTED_HEAD = "6f1fb917564dd70262520778c1c8ced7a825a525"
PASS_STATUS = "VS0_5_EVIDENCE_YIELD_REPORT_PASS_USEFUL_EVIDENCE_PRESENT"

VS0_1_JSON = "docs/matrixlabs/phase_vs0/phase_vs0_source_inventory_v0.json"
VS0_1_MD = "docs/matrixlabs/phase_vs0/phase_vs0_source_inventory_v0.md"
VS0_2_JSON = (
    "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_build_receipt_v0.json"
)
VS0_2_MD = (
    "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_build_receipt_v0.md"
)
VS0_3_JSON = (
    "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_verification_v0.json"
)
VS0_3_MD = (
    "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_verification_v0.md"
)
RUN_ROOT = (
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0"
)
A_TO_F_ROOT = f"{RUN_ROOT}/a_to_f"
CHAIN_INDEX_JSON = f"{A_TO_F_ROOT}/phase_vs0_a_to_f_chain_index_v0.json"
CHAIN_INDEX_MD = f"{A_TO_F_ROOT}/phase_vs0_a_to_f_chain_index_v0.md"
NEGATIVE_ROOT = f"{RUN_ROOT}/negative_probes"
VS0_4_DEFINITIONS = (
    f"{NEGATIVE_ROOT}/phase_vs0_negative_probe_definitions_v0.json"
)
VS0_4_JSON = f"{NEGATIVE_ROOT}/phase_vs0_negative_probe_battery_v0.json"
VS0_4_MD = f"{NEGATIVE_ROOT}/phase_vs0_negative_probe_battery_v0.md"
OUTPUT_JSON = (
    "docs/matrixlabs/phase_vs0/phase_vs0_evidence_yield_report_v0.json"
)
OUTPUT_MD = "docs/matrixlabs/phase_vs0/phase_vs0_evidence_yield_report_v0.md"

VS0_1_STATUS = "VS0_PREFLIGHT_PASS_SCOPE_DECLARED"
VS0_2_STATUS = (
    "VS0_2_HAPPY_PATH_BUILD_PASS_A_TO_F_PHASE_SPECIMEN_CREATED"
)
VS0_3_STATUS = (
    "VS0_3_HAPPY_PATH_VERIFICATION_PASS_A_TO_F_PHASE_SPECIMEN_VERIFIED"
)
VS0_4_STATUS = "VS0_4_NEGATIVE_PROBES_PASS_TYPED_STOPS"

PROBE_RECEIPTS = {
    "NEG01_D4_WITHOUT_ACTIVE_ENTRY": (
        f"{NEGATIVE_ROOT}/receipts/neg01_d4_without_active_entry_v0.json"
    ),
    "NEG02_D4_WITH_RADIUS_ZERO": (
        f"{NEGATIVE_ROOT}/receipts/neg02_d4_with_radius_zero_v0.json"
    ),
    "NEG03_E2_WITHOUT_E1_TARGET": (
        f"{NEGATIVE_ROOT}/receipts/neg03_e2_without_e1_target_v0.json"
    ),
    "NEG04_E3_WITH_DROPPED_RADIUS_FIELD": (
        f"{NEGATIVE_ROOT}/receipts/neg04_e3_with_dropped_radius_field_v0.json"
    ),
    "NEG05_E4_WITH_FAILED_DECOMPRESSION_AUDIT": (
        f"{NEGATIVE_ROOT}/receipts/"
        "neg05_e4_with_failed_decompression_audit_v0.json"
    ),
    "NEG06_F2_WITHOUT_E4_CLOSURE": (
        f"{NEGATIVE_ROOT}/receipts/neg06_f2_without_e4_closure_v0.json"
    ),
    "NEG07_F2_WITH_SPECIMEN_COUNT_OVERCLAIM": (
        f"{NEGATIVE_ROOT}/receipts/"
        "neg07_f2_with_specimen_count_overclaim_v0.json"
    ),
    "NEG08_F3_WITH_GENERALIZATION_CLAIMED": (
        f"{NEGATIVE_ROOT}/receipts/"
        "neg08_f3_with_generalization_claimed_v0.json"
    ),
    "NEG09_F4_WITH_ACTIVE_REGISTRY_CREATED": (
        f"{NEGATIVE_ROOT}/receipts/"
        "neg09_f4_with_active_registry_created_v0.json"
    ),
    "NEG10_ANY_WITH_RUNNER_AUTHORITY_TRUE": (
        f"{NEGATIVE_ROOT}/receipts/"
        "neg10_any_with_runner_authority_true_v0.json"
    ),
}

FAILURE_CODES = [
    "VS0_5_STOP_SOURCE_INVENTORY_MISSING",
    "VS0_5_STOP_SOURCE_INVENTORY_NOT_PASS",
    "VS0_5_STOP_HAPPY_PATH_BUILD_MISSING",
    "VS0_5_STOP_HAPPY_PATH_BUILD_NOT_PASS",
    "VS0_5_STOP_HAPPY_PATH_VERIFICATION_MISSING",
    "VS0_5_STOP_HAPPY_PATH_VERIFICATION_NOT_PASS",
    "VS0_5_STOP_NEGATIVE_PROBE_BATTERY_MISSING",
    "VS0_5_STOP_NEGATIVE_PROBE_BATTERY_NOT_PASS",
    "VS0_5_FAIL_CONFIRMATION_YIELD_MISSING",
    "VS0_5_FAIL_DIAGNOSTIC_YIELD_MISSING",
    "VS0_5_FAIL_DIAGNOSTIC_EVENTS_MISSING_TYPED_STOPS",
    "VS0_5_FAIL_DIAGNOSTIC_FIELDS_MISSING",
    "VS0_5_FAIL_NEXT_LAWFUL_SURFACE_MISSING",
    "VS0_5_FAIL_SELF_REPAIR_ATTEMPT_PRESENT",
    "VS0_5_FAIL_HAPPY_PATH_MUTATION_PRESENT",
    "VS0_5_FAIL_PRIOR_VS0_SOURCE_MUTATED",
    "VS0_5_FAIL_NEGATIVE_PROBE_RECEIPTS_MUTATED",
    "VS0_5_FAIL_A_TO_F_ARTIFACTS_MUTATED",
    "VS0_5_FAIL_EVIDENCE_VOLUME_OVERCLAIM",
    "VS0_5_FAIL_COVERAGE_OVERCLAIM",
    "VS0_5_FAIL_PERFORMANCE_OPTIMIZATION_CLAIMED",
    "VS0_5_FAIL_SCALE_OPTIMIZATION_CLAIMED",
    "VS0_5_FAIL_ACTIVE_REGISTRY_CLAIMED",
    "VS0_5_FAIL_REGISTRY_PROMOTION_CLAIMED",
    "VS0_5_FAIL_TRACE_GENERALIZATION_CLAIMED",
    "VS0_5_FAIL_RUNNER_READINESS_CLAIMED",
    "VS0_5_FAIL_RUNNER_AUTHORITY_CREATED",
    "VS0_5_FAIL_PHASE_CLOSURE_CLAIMED",
]


class ReportFailure(RuntimeError):
    def __init__(
        self,
        code: str,
        *,
        source: str = "NONE",
        field: str = "NONE",
        expected: object = "NONE",
        actual: object = "NONE",
        next_surface: str = "REPAIR_VS0_SOURCE_OR_REPORT_INPUT",
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
    next_surface: str = "REPAIR_VS0_SOURCE_OR_REPORT_INPUT",
) -> None:
    raise ReportFailure(
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
            "VS0_5_FAIL_PRIOR_VS0_SOURCE_MUTATED",
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
            "VS0_5_STOP_NEGATIVE_PROBE_BATTERY_MISSING",
            source=VS0_4_JSON,
            field="repo_root",
            expected="git repository",
            actual=proc.stderr.strip(),
        )
    return Path(proc.stdout.strip()).resolve()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path, missing_code: str) -> dict[str, Any]:
    if not path.is_file():
        fail(
            missing_code,
            source=str(path),
            field="file_presence",
            expected=True,
            actual=False,
        )
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(
            missing_code,
            source=str(path),
            field="valid_json",
            expected=True,
            actual=str(exc),
        )
    if not isinstance(value, dict):
        fail(
            missing_code,
            source=str(path),
            field="json_object",
            expected=True,
            actual=type(value).__name__,
        )
    return value


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
    for line in run_git(
        root, ["status", "--short", "--untracked-files=all"]
    ).splitlines():
        path = status_path(line)
        if path in allowed_exact or any(
            path.startswith(prefix) for prefix in allowed_prefixes
        ):
            continue
        code = (
            "VS0_5_FAIL_A_TO_F_ARTIFACTS_MUTATED"
            if path.startswith(f"{A_TO_F_ROOT}/")
            else "VS0_5_FAIL_PRIOR_VS0_SOURCE_MUTATED"
        )
        fail(
            code,
            source=path,
            field="git_status_short",
            expected="clean prior evidence",
            actual=line,
        )


def verify_head_blob(root: Path, relative_path: str, failure_code: str) -> None:
    path = root / relative_path
    if not path.is_file():
        fail(
            failure_code,
            source=relative_path,
            field="file_presence",
            expected=True,
            actual=False,
        )
    proc = subprocess.run(
        ["git", "show", f"HEAD:{relative_path}"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    worktree_hash = sha256(path)
    if (
        proc.returncode != 0
        or hashlib.sha256(proc.stdout).hexdigest() != worktree_hash
    ):
        fail(
            failure_code,
            source=relative_path,
            field="worktree_hash",
            expected="HEAD blob hash",
            actual=worktree_hash,
        )


def require_equal(
    source: str,
    field: str,
    actual: object,
    expected: object,
    code: str,
) -> None:
    if actual != expected:
        fail(
            code,
            source=source,
            field=field,
            expected=expected,
            actual=actual,
        )


def verify_source_statuses(
    root: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    if run_git(root, ["rev-parse", "HEAD"]) != EXPECTED_HEAD:
        fail(
            "VS0_5_STOP_NEGATIVE_PROBE_BATTERY_NOT_PASS",
            source=VS0_4_JSON,
            field="source_vs0_4_commit_sha",
            expected=EXPECTED_HEAD,
            actual=run_git(root, ["rev-parse", "HEAD"]),
        )
    battery_commit = run_git(
        root, ["log", "-n", "1", "--format=%H", "--", VS0_4_JSON]
    )
    if battery_commit != EXPECTED_HEAD:
        fail(
            "VS0_5_STOP_NEGATIVE_PROBE_BATTERY_NOT_PASS",
            source=VS0_4_JSON,
            field="source_vs0_4_commit_sha",
            expected=EXPECTED_HEAD,
            actual=battery_commit,
        )

    vs0_1 = load_json(
        root / VS0_1_JSON, "VS0_5_STOP_SOURCE_INVENTORY_MISSING"
    )
    vs0_2 = load_json(
        root / VS0_2_JSON, "VS0_5_STOP_HAPPY_PATH_BUILD_MISSING"
    )
    vs0_3 = load_json(
        root / VS0_3_JSON, "VS0_5_STOP_HAPPY_PATH_VERIFICATION_MISSING"
    )
    vs0_4 = load_json(
        root / VS0_4_JSON, "VS0_5_STOP_NEGATIVE_PROBE_BATTERY_MISSING"
    )

    require_equal(
        VS0_1_JSON,
        "inventory_status",
        vs0_1.get("inventory_status"),
        VS0_1_STATUS,
        "VS0_5_STOP_SOURCE_INVENTORY_NOT_PASS",
    )
    require_equal(
        VS0_2_JSON,
        "happy_path_build_status",
        vs0_2.get("happy_path_build_status"),
        VS0_2_STATUS,
        "VS0_5_STOP_HAPPY_PATH_BUILD_NOT_PASS",
    )
    require_equal(
        VS0_3_JSON,
        "verification_result.happy_path_verification_status",
        vs0_3.get("verification_result", {}).get(
            "happy_path_verification_status"
        ),
        VS0_3_STATUS,
        "VS0_5_STOP_HAPPY_PATH_VERIFICATION_NOT_PASS",
    )
    require_equal(
        VS0_4_JSON,
        "negative_probe_battery_gate",
        vs0_4.get("negative_probe_battery_gate"),
        VS0_4_STATUS,
        "VS0_5_STOP_NEGATIVE_PROBE_BATTERY_NOT_PASS",
    )
    require_equal(
        VS0_4_JSON,
        "battery_result.negative_probe_battery_status",
        vs0_4.get("battery_result", {}).get(
            "negative_probe_battery_status"
        ),
        VS0_4_STATUS,
        "VS0_5_STOP_NEGATIVE_PROBE_BATTERY_NOT_PASS",
    )
    return vs0_1, vs0_2, vs0_3, vs0_4


def collect_source_groups(
    root: Path, vs0_4: dict[str, Any]
) -> dict[str, list[str]]:
    index = load_json(
        root / CHAIN_INDEX_JSON, "VS0_5_FAIL_A_TO_F_ARTIFACTS_MUTATED"
    )
    records = index.get("artifacts")
    if not isinstance(records, list) or len(records) != 24:
        fail(
            "VS0_5_FAIL_A_TO_F_ARTIFACTS_MUTATED",
            source=CHAIN_INDEX_JSON,
            field="artifacts",
            expected="24 indexed artifacts",
            actual=records,
        )
    a_to_f_paths = [CHAIN_INDEX_JSON, CHAIN_INDEX_MD]
    for record in records:
        path = record.get("path") if isinstance(record, dict) else None
        if not isinstance(path, str) or not path.startswith(f"{A_TO_F_ROOT}/"):
            fail(
                "VS0_5_FAIL_A_TO_F_ARTIFACTS_MUTATED",
                source=CHAIN_INDEX_JSON,
                field="artifact.path",
                expected=f"{A_TO_F_ROOT}/...",
                actual=path,
            )
        if sha256(root / path) != record.get("sha256"):
            fail(
                "VS0_5_FAIL_A_TO_F_ARTIFACTS_MUTATED",
                source=path,
                field="sha256",
                expected=record.get("sha256"),
                actual=sha256(root / path),
            )
        a_to_f_paths.append(path)

    result_ids = [
        item.get("probe_id")
        for item in vs0_4.get("probe_results", [])
        if isinstance(item, dict)
    ]
    if result_ids != list(PROBE_RECEIPTS):
        fail(
            "VS0_5_FAIL_DIAGNOSTIC_YIELD_MISSING",
            source=VS0_4_JSON,
            field="probe_results.probe_id",
            expected=list(PROBE_RECEIPTS),
            actual=result_ids,
        )

    groups = {
        "vs0_1": [VS0_1_JSON, VS0_1_MD],
        "vs0_2": [VS0_2_JSON, VS0_2_MD],
        "vs0_3": [VS0_3_JSON, VS0_3_MD],
        "vs0_4": [VS0_4_DEFINITIONS, VS0_4_JSON, VS0_4_MD],
        "a_to_f": a_to_f_paths,
        "negative_probe_receipts": list(PROBE_RECEIPTS.values()),
    }
    for group, paths in groups.items():
        failure_code = (
            "VS0_5_FAIL_A_TO_F_ARTIFACTS_MUTATED"
            if group == "a_to_f"
            else (
                "VS0_5_FAIL_NEGATIVE_PROBE_RECEIPTS_MUTATED"
                if group == "negative_probe_receipts"
                else "VS0_5_FAIL_PRIOR_VS0_SOURCE_MUTATED"
            )
        )
        for path in paths:
            verify_head_blob(root, path, failure_code)
    return groups


def hash_groups(
    root: Path, groups: dict[str, list[str]]
) -> dict[str, dict[str, str]]:
    return {
        group: {path: sha256(root / path) for path in paths}
        for group, paths in groups.items()
    }


def decision_relevance() -> dict[str, bool]:
    return {
        "constrains_next_lawful_move": True,
        "identifies_boundary_or_success": True,
        "supports_vs0_6_closure_review": True,
    }


def confirmation_events() -> list[dict[str, Any]]:
    values = [
        (
            "CY01",
            "VS0.1",
            VS0_1_JSON,
            VS0_1_STATUS,
            "phase scope and lawful starting surface confirmed",
        ),
        (
            "CY02",
            "VS0.2",
            VS0_2_JSON,
            VS0_2_STATUS,
            "A-to-F phase specimen build confirmed",
        ),
        (
            "CY03",
            "VS0.3",
            VS0_3_JSON,
            VS0_3_STATUS,
            "happy-path chain coherence and boundaries confirmed",
        ),
        (
            "CY04",
            "VS0.4",
            VS0_4_JSON,
            VS0_4_STATUS,
            "selected negative-probe battery execution confirmed",
        ),
    ]
    return [
        {
            "event_id": event_id,
            "phase_step": phase_step,
            "source_path": source_path,
            "observed_status": status,
            "confirmation": confirmation,
            "yield_branch": "CONFIRMATION_YIELD",
            "decision_relevance": decision_relevance(),
        }
        for event_id, phase_step, source_path, status, confirmation in values
    ]


def diagnostic_events(
    root: Path, vs0_4: dict[str, Any]
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    results = vs0_4.get("probe_results", [])
    if not isinstance(results, list) or len(results) != 10:
        fail(
            "VS0_5_FAIL_DIAGNOSTIC_YIELD_MISSING",
            source=VS0_4_JSON,
            field="probe_results",
            expected=10,
            actual=len(results) if isinstance(results, list) else type(results),
        )

    anchors = [
        "missing_object",
        "missing_fields",
        "violating_field",
        "violating_fields",
        "violating_field_group",
    ]
    for index, (probe_id, receipt_path) in enumerate(
        PROBE_RECEIPTS.items(), start=1
    ):
        result = results[index - 1]
        receipt = load_json(
            root / receipt_path,
            "VS0_5_FAIL_DIAGNOSTIC_YIELD_MISSING",
        )
        battery_receipt = dict(result)
        battery_receipt.pop("receipt_path", None)
        if receipt != battery_receipt:
            fail(
                "VS0_5_FAIL_DIAGNOSTIC_FIELDS_MISSING",
                source=receipt_path,
                field="battery_receipt_parity",
                expected="exact battery probe result",
                actual="mismatch",
            )

        expected = receipt.get("expected_result", {})
        observed = receipt.get("observed_result", {})
        diagnostic = receipt.get("diagnostic_fields", {})
        safety = receipt.get("probe_safety", {})
        if (
            receipt.get("probe_id") != probe_id
            or observed.get("stopped") is not True
            or observed.get("unexpected_success") is not False
            or observed.get("ambiguous_stop") is not False
            or expected.get("expected_stop_code")
            != observed.get("observed_stop_code")
        ):
            fail(
                "VS0_5_FAIL_DIAGNOSTIC_EVENTS_MISSING_TYPED_STOPS",
                source=receipt_path,
                field="typed_stop",
                expected=expected.get("expected_stop_code"),
                actual=observed.get("observed_stop_code"),
            )
        required_diagnostics = [
            "violating_object",
            "violated_boundary",
            "source_boundary",
            "expected_value",
            "actual_value",
            "next_lawful_surface",
        ]
        missing = [key for key in required_diagnostics if key not in diagnostic]
        if missing or not any(
            diagnostic.get(key) not in (None, [], {}) for key in anchors
        ):
            fail(
                "VS0_5_FAIL_DIAGNOSTIC_FIELDS_MISSING",
                source=receipt_path,
                field="diagnostic_fields",
                expected=required_diagnostics,
                actual=missing,
            )
        if not diagnostic.get("next_lawful_surface"):
            fail(
                "VS0_5_FAIL_NEXT_LAWFUL_SURFACE_MISSING",
                source=receipt_path,
                field="next_lawful_surface",
                expected="typed lawful surface",
                actual=diagnostic.get("next_lawful_surface"),
            )
        if diagnostic.get("self_repair_performed") is not False:
            fail(
                "VS0_5_FAIL_SELF_REPAIR_ATTEMPT_PRESENT",
                source=receipt_path,
                field="self_repair_performed",
                expected=False,
                actual=diagnostic.get("self_repair_performed"),
            )
        if safety.get("happy_path_mutated") is not False:
            fail(
                "VS0_5_FAIL_HAPPY_PATH_MUTATION_PRESENT",
                source=receipt_path,
                field="happy_path_mutated",
                expected=False,
                actual=safety.get("happy_path_mutated"),
            )
        events.append(
            {
                "event_id": f"DY{index:02d}",
                "probe_id": probe_id,
                "source_receipt_path": receipt_path,
                "attempted_illegal_move": receipt.get(
                    "attempted_illegal_move"
                ),
                "expected_stop_code": expected.get("expected_stop_code"),
                "observed_stop_code": observed.get("observed_stop_code"),
                "violating_object": diagnostic.get("violating_object"),
                "missing_object": diagnostic.get("missing_object"),
                "missing_fields": diagnostic.get("missing_fields"),
                "violating_field": diagnostic.get("violating_field"),
                "violating_fields": diagnostic.get("violating_fields"),
                "violating_field_group": diagnostic.get(
                    "violating_field_group"
                ),
                "violated_boundary": diagnostic.get("violated_boundary"),
                "source_boundary": diagnostic.get("source_boundary"),
                "expected_value": diagnostic.get("expected_value"),
                "actual_value": diagnostic.get("actual_value"),
                "next_lawful_surface": diagnostic.get(
                    "next_lawful_surface"
                ),
                "self_repair_performed": False,
                "happy_path_mutated": False,
                "yield_branch": "DIAGNOSTIC_YIELD",
                "decision_relevance": decision_relevance(),
            }
        )
    return events


def validate_battery_boundaries(vs0_4: dict[str, Any]) -> None:
    summary = vs0_4.get("probe_summary", {})
    expected_summary = {
        "probe_count_expected": 10,
        "probe_count_run": 10,
        "expected_typed_stop_count": 10,
        "observed_typed_stop_count": 10,
        "unexpected_pass_count": 0,
        "wrong_stop_code_count": 0,
        "ambiguous_stop_count": 0,
        "diagnostic_fields_missing_count": 0,
        "next_lawful_surface_missing_count": 0,
        "self_repair_attempt_count": 0,
        "happy_path_mutation_count": 0,
    }
    for field, expected in expected_summary.items():
        require_equal(
            VS0_4_JSON,
            f"probe_summary.{field}",
            summary.get(field),
            expected,
            (
                "VS0_5_FAIL_DIAGNOSTIC_YIELD_MISSING"
                if expected == 10
                else "VS0_5_FAIL_DIAGNOSTIC_FIELDS_MISSING"
            ),
        )

    coverage = vs0_4.get("coverage_claim", {})
    if (
        coverage.get("selected_probe_battery_only") is not True
        or coverage.get("all_possible_illegal_shortcuts_tested") is not False
        or coverage.get("future_live_runtime_coverage_claimed") is not False
        or coverage.get("phase_closure_claimed") is not False
    ):
        fail(
            "VS0_5_FAIL_COVERAGE_OVERCLAIM",
            source=VS0_4_JSON,
            field="coverage_claim",
            expected="selected battery only; no total/future/closure claim",
            actual=coverage,
        )
    result = vs0_4.get("battery_result", {})
    guarded_false = {
        "active_registry_created": "VS0_5_FAIL_ACTIVE_REGISTRY_CLAIMED",
        "source_authority_replaced": "VS0_5_FAIL_TRACE_GENERALIZATION_CLAIMED",
        "runner_authority_created": "VS0_5_FAIL_RUNNER_AUTHORITY_CREATED",
    }
    for field, code in guarded_false.items():
        if result.get(field) is not False:
            fail(
                code,
                source=VS0_4_JSON,
                field=f"battery_result.{field}",
                expected=False,
                actual=result.get(field),
            )
    non_claims = vs0_4.get("non_claims", {})
    required_non_claims = {
        "does_not_activate_registry": "VS0_5_FAIL_ACTIVE_REGISTRY_CLAIMED",
        "does_not_generalize_trace": (
            "VS0_5_FAIL_TRACE_GENERALIZATION_CLAIMED"
        ),
        "does_not_create_runner_authority": (
            "VS0_5_FAIL_RUNNER_AUTHORITY_CREATED"
        ),
        "only_selected_synthetic_shortcuts_tested": (
            "VS0_5_FAIL_COVERAGE_OVERCLAIM"
        ),
    }
    for field, code in required_non_claims.items():
        if non_claims.get(field) is not True:
            fail(
                code,
                source=VS0_4_JSON,
                field=f"non_claims.{field}",
                expected=True,
                actual=non_claims.get(field),
            )
    execution = vs0_4.get("probe_execution_mode", {})
    for field in [
        "live_runtime_execution_performed",
        "runner_execution_performed",
        "production_move_engine_called",
    ]:
        if execution.get(field) is not False:
            fail(
                "VS0_5_FAIL_RUNNER_READINESS_CLAIMED",
                source=VS0_4_JSON,
                field=f"probe_execution_mode.{field}",
                expected=False,
                actual=execution.get(field),
            )


def source_preservation(
    before: dict[str, dict[str, str]],
    after: dict[str, dict[str, str]],
) -> dict[str, bool]:
    return {
        "vs0_1_source_inventory_mutated_by_vs0_5": (
            before["vs0_1"] != after["vs0_1"]
        ),
        "vs0_2_happy_path_build_mutated_by_vs0_5": (
            before["vs0_2"] != after["vs0_2"]
        ),
        "vs0_3_happy_path_verification_mutated_by_vs0_5": (
            before["vs0_3"] != after["vs0_3"]
        ),
        "vs0_4_negative_probe_battery_mutated_by_vs0_5": (
            before["vs0_4"] != after["vs0_4"]
        ),
        "a_to_f_artifacts_mutated_by_vs0_5": (
            before["a_to_f"] != after["a_to_f"]
        ),
        "negative_probe_receipts_mutated_by_vs0_5": (
            before["negative_probe_receipts"]
            != after["negative_probe_receipts"]
        ),
    }


def build_report(
    confirmations: list[dict[str, Any]],
    diagnostics: list[dict[str, Any]],
    before_hashes: dict[str, dict[str, str]],
    after_hashes: dict[str, dict[str, str]],
) -> dict[str, Any]:
    preservation = source_preservation(before_hashes, after_hashes)
    if preservation["a_to_f_artifacts_mutated_by_vs0_5"]:
        fail("VS0_5_FAIL_A_TO_F_ARTIFACTS_MUTATED")
    if preservation["negative_probe_receipts_mutated_by_vs0_5"]:
        fail("VS0_5_FAIL_NEGATIVE_PROBE_RECEIPTS_MUTATED")
    if any(preservation.values()):
        fail("VS0_5_FAIL_PRIOR_VS0_SOURCE_MUTATED")

    return {
        "schema_version": "matrixlabs_phase_vs0_evidence_yield_report_v0",
        "report_id": "phase_vs0_evidence_yield_report_v0",
        "phase_id": "PHASE_VS0",
        "phase_step": "VS0.5",
        "report_role": "EVIDENCE_YIELD_REPORT_ONLY",
        "source_artifacts": {
            "vs0_1_source_inventory": VS0_1_JSON,
            "vs0_2_happy_path_build_receipt": VS0_2_JSON,
            "vs0_3_happy_path_verification": VS0_3_JSON,
            "vs0_4_negative_probe_battery": VS0_4_JSON,
        },
        "source_commits": {
            "source_vs0_4_commit_sha": EXPECTED_HEAD,
            "source_vs0_4_negative_probe_battery_gate": VS0_4_STATUS,
            "source_vs0_4_required_before_report": True,
        },
        "source_statuses": {
            "vs0_1_status": VS0_1_STATUS,
            "vs0_2_status": VS0_2_STATUS,
            "vs0_3_status": VS0_3_STATUS,
            "vs0_4_status": VS0_4_STATUS,
        },
        "report_execution_mode": {
            "read_only_report_over_prior_vs0_evidence": True,
            "builds_new_a_to_f_artifacts": False,
            "reruns_happy_path_verification": False,
            "runs_new_negative_probes": False,
            "performs_phase_closure": False,
            "mutates_prior_vs0_artifacts": False,
        },
        "evidence_yield_model": {
            "doctrine_version": "evidence_yield_doctrine_v0",
            "branches": {
                "confirmation_yield": (
                    "evidence obtained from successful execution"
                ),
                "diagnostic_yield": (
                    "evidence obtained from unsuccessful, halted, or "
                    "stopped execution"
                ),
            },
            "non_goal": "do_not_count_atoms",
            "useful_evidence_rule": (
                "evidence is useful when it helps determine, constrain, "
                "or audit the next lawful move"
            ),
        },
        "confirmation_yield": {
            "event_count": len(confirmations),
            "events": confirmations,
        },
        "diagnostic_yield": {
            "event_count": len(diagnostics),
            "events_source": (
                "phase_vs0_negative_probe_battery_v0.probe_results"
            ),
            "events": diagnostics,
            "expected_probe_count": 10,
            "typed_stop_count": 10,
            "unexpected_pass_count": 0,
            "ambiguous_stop_count": 0,
            "diagnostic_fields_missing_count": 0,
            "next_lawful_surface_missing_count": 0,
            "self_repair_attempt_count": 0,
            "happy_path_mutation_count": 0,
            "yield_branch": "DIAGNOSTIC_YIELD",
        },
        "yield_summary": {
            "confirmation_yield_events": 4,
            "diagnostic_yield_events": 10,
            "total_decision_relevant_events": 14,
            "confirmation_yield_result": "PASS",
            "diagnostic_yield_result": "PASS",
            "event_count_is_descriptive_not_value_claim": True,
            "evidence_volume_optimization_claimed": False,
            "performance_optimization_claimed": False,
            "scale_optimization_claimed": False,
            "decision_relevant_evidence_present": True,
            "sufficient_input_for_vs0_6_phase_closure": True,
            "phase_closure_performed_by_vs0_5": False,
        },
        "useful_evidence_checks": {
            "next_lawful_move_constrained": True,
            "successful_path_confirmed": True,
            "illegal_shortcuts_stopped": True,
            "typed_stop_codes_present": True,
            "diagnostic_fields_present": True,
            "missing_object_or_field_localized": True,
            "violated_boundaries_identified": True,
            "next_lawful_surfaces_identified": True,
            "self_repair_attempts_absent": True,
            "coverage_overclaim_absent": True,
            "runner_readiness_overclaim_absent": True,
        },
        "overclaim_guard": {
            "coverage_overclaim_detected": False,
            "performance_optimization_claimed": False,
            "scale_optimization_claimed": False,
            "active_registry_claimed": False,
            "registry_promotion_claimed": False,
            "trace_generalization_claimed": False,
            "runner_readiness_claimed": False,
            "runner_authority_created": False,
            "phase_closure_claimed_by_vs0_5": False,
        },
        "closure_readiness_boundary": {
            "sufficient_input_for_vs0_6_phase_closure": True,
            "vs0_6_phase_closure_performed": False,
            "phase_closure_authorized_by_vs0_5": False,
            "phase_closed": False,
            "next_required_object": "phase_vs0_closure_v0",
        },
        "source_hash_snapshots": {
            "hash_algorithm": "sha256",
            "before_report": before_hashes,
            "after_report": after_hashes,
            "all_prior_source_hashes_unchanged": before_hashes == after_hashes,
        },
        "source_preservation": preservation,
        "decision_relevance_result": {
            "projected_specimen_built_in_phase_namespace": True,
            "projected_happy_path_verified_without_mutation": True,
            "selected_illegal_shortcuts_stopped_with_typed_diagnostics": True,
            "no_runner_no_active_registry_no_generalization_boundaries_held": True,
            "next_lawful_move": "VS0.6_PHASE_CLOSURE",
            "runner_activation_is_next_lawful_move": False,
        },
        "if_report_fails": {
            "yield_branch": "DIAGNOSTIC_YIELD",
            "reason": (
                "failed report identifies missing source, invalid source "
                "status, missing diagnostic yield, overclaim, or mutation "
                "boundary"
            ),
        },
        "yield_result": {
            "evidence_yield_report_status": PASS_STATUS,
            "confirmation_yield_present": True,
            "diagnostic_yield_present": True,
            "decision_relevant_evidence_present": True,
            "sufficient_input_for_vs0_6_phase_closure": True,
            "phase_closure_performed_by_vs0_5": False,
            "failures": [],
        },
        "failure_vocabulary": FAILURE_CODES,
        "next_required_object": "phase_vs0_closure_v0",
        "terminal_transition": "ADVANCE(VS0_6_PHASE_CLOSURE_PENDING)",
        "precommit_phase_vs0_evidence_yield_report_gate": "PASS",
        "evidence_yield_report_gate": PASS_STATUS,
        "failures": [],
    }


def render_markdown() -> str:
    return """# Phase VS0 Evidence Yield report v0

## Status

VS0_5_EVIDENCE_YIELD_REPORT_PASS_USEFUL_EVIDENCE_PRESENT

## Evidence Yield doctrine

- Confirmation Yield: evidence obtained from successful execution
- Diagnostic Yield: evidence obtained from unsuccessful, halted, or stopped execution

## Sources

- VS0.1 source inventory: PASS
- VS0.2 happy-path build: PASS
- VS0.3 happy-path verification: PASS
- VS0.4 negative probe battery: PASS

## Confirmation Yield

- VS0.1 confirmed phase scope and lawful starting surface.
- VS0.2 confirmed the A\u2192F phase specimen could be built.
- VS0.3 confirmed the happy-path chain was coherent and bounded.
- VS0.4 confirmed selected illegal shortcut probes stopped as expected.

## Diagnostic Yield

- 10 selected illegal shortcut probes produced typed stops.
- 10/10 expected stop codes matched.
- 0 unexpected passes.
- 0 ambiguous stops.
- 0 missing diagnostic fields.
- 0 missing next lawful surfaces.
- 0 self-repair attempts.
- 0 happy-path mutations.

## Useful evidence result

The VS0 execution sequence produced decision-relevant evidence about what held, what stopped, what boundaries were enforced, and what lawful object is available next.

The event count is descriptive. The value comes from decision relevance.

## Closure readiness boundary

- sufficient input for VS0.6 phase closure: true
- VS0.6 phase closure performed: false
- phase closure authorized by VS0.5: false
- phase closed: false

## Next required object

phase_vs0_closure_v0

## Terminal transition

ADVANCE(VS0_6_PHASE_CLOSURE_PENDING)

## Non-claims

- VS0.5 does not close Phase VS0.
- VS0.5 does not claim total illegal-path coverage.
- VS0.5 does not claim performance optimization.
- VS0.5 does not claim scale optimization.
- VS0.5 does not activate a registry.
- VS0.5 does not promote a registry candidate.
- VS0.5 does not generalize the trace.
- VS0.5 does not authorize runner behavior.
"""


def markdown_contains_overclaim(md: str) -> list[str]:
    """
    Return affirmative overclaim hits while allowing explicit false boundaries.
    """
    allowed_patterns = [
        r"\bphase closed\s*[:=]\s*false\b",
        r"\bphase_closed\s*[:=]\s*false\b",
        r"\bvs0\.5 does not close phase vs0\b",
        r"\bdoes not close phase vs0\b",
        r"\bdoes not claim total illegal-path coverage\b",
        r"\bdoes not claim performance optimization\b",
        r"\bdoes not claim scale optimization\b",
        r"\bdoes not activate a registry\b",
        r"\bdoes not promote a registry candidate\b",
        r"\bdoes not authorize runner behavior\b",
        r"\bvs0\.6 phase closure performed\s*[:=]\s*false\b",
        r"\bphase closure authorized by vs0\.5\s*[:=]\s*false\b",
    ]
    forbidden_patterns = {
        "runtime ready": r"\bruntime ready\b",
        "runner ready": r"\brunner ready\b",
        "registry active": r"\bregistry active\b",
        "registry promoted": r"\bregistry promoted\b",
        "all illegal paths tested": r"\ball illegal paths tested\b",
        "total coverage": r"\btotal coverage\b",
        "performance improved": r"\bperformance improved\b",
        "scale improved": r"\bscale improved\b",
        "phase closed": (
            r"\bphase(?:\s+vs0)?\s+(?:is\s+|has\s+)?closed\b|"
            r"\bphase closed successfully\b"
        ),
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


def fail_for_markdown_overclaims(hits: list[str]) -> None:
    first_hit = hits[0].lower() if hits else ""
    label_to_code = {
        "runtime ready": "VS0_5_FAIL_RUNNER_READINESS_CLAIMED",
        "runner ready": "VS0_5_FAIL_RUNNER_READINESS_CLAIMED",
        "registry active": "VS0_5_FAIL_ACTIVE_REGISTRY_CLAIMED",
        "registry promoted": "VS0_5_FAIL_REGISTRY_PROMOTION_CLAIMED",
        "all illegal paths tested": "VS0_5_FAIL_COVERAGE_OVERCLAIM",
        "total coverage": "VS0_5_FAIL_COVERAGE_OVERCLAIM",
        "performance improved": (
            "VS0_5_FAIL_PERFORMANCE_OPTIMIZATION_CLAIMED"
        ),
        "scale improved": "VS0_5_FAIL_SCALE_OPTIMIZATION_CLAIMED",
        "phase closed": "VS0_5_FAIL_PHASE_CLOSURE_CLAIMED",
    }
    code = "VS0_5_FAIL_COVERAGE_OVERCLAIM"
    for label, candidate_code in label_to_code.items():
        if label in first_hit:
            code = candidate_code
            break
    fail(
        code,
        source=OUTPUT_MD,
        field="markdown_overclaim_guard",
        expected=[],
        actual=hits,
        next_surface="REPAIR_VS0_5_FORBIDDEN_PHRASE_GUARD",
    )


def write_json(root: Path, value: dict[str, Any]) -> None:
    path = (root / OUTPUT_JSON).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_markdown(root: Path, value: str) -> None:
    path = (root / OUTPUT_MD).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def print_complete() -> None:
    lines = [
        "BUILD_PHASE_VS0_EVIDENCE_YIELD_REPORT_V0_COMPLETE",
        "report_id=phase_vs0_evidence_yield_report_v0",
        "schema_version=matrixlabs_phase_vs0_evidence_yield_report_v0",
        "phase_id=PHASE_VS0",
        "phase_step=VS0.5",
        "report_role=EVIDENCE_YIELD_REPORT_ONLY",
        f"source_vs0_4_commit_sha={EXPECTED_HEAD}",
        f"source_inventory_status={VS0_1_STATUS}",
        f"happy_path_build_status={VS0_2_STATUS}",
        f"happy_path_verification_status={VS0_3_STATUS}",
        f"negative_probe_battery_status={VS0_4_STATUS}",
        "confirmation_yield_present=true",
        "diagnostic_yield_present=true",
        "confirmation_yield_event_count=4",
        "diagnostic_yield_event_count=10",
        "total_decision_relevant_events=14",
        "event_count_is_descriptive_not_value_claim=true",
        "decision_relevant_evidence_present=true",
        "sufficient_input_for_vs0_6_phase_closure=true",
        "phase_closure_performed_by_vs0_5=false",
        "phase_closure_authorized_by_vs0_5=false",
        "phase_closed=false",
        "coverage_overclaim_detected=false",
        "performance_optimization_claimed=false",
        "scale_optimization_claimed=false",
        "active_registry_claimed=false",
        "registry_promotion_claimed=false",
        "trace_generalization_claimed=false",
        "runner_readiness_claimed=false",
        "runner_authority_created=false",
        "vs0_1_source_inventory_mutated_by_vs0_5=false",
        "vs0_2_happy_path_build_mutated_by_vs0_5=false",
        "vs0_3_happy_path_verification_mutated_by_vs0_5=false",
        "vs0_4_negative_probe_battery_mutated_by_vs0_5=false",
        "a_to_f_artifacts_mutated_by_vs0_5=false",
        "negative_probe_receipts_mutated_by_vs0_5=false",
        "precommit_phase_vs0_evidence_yield_report_gate=PASS",
        f"evidence_yield_report_gate={PASS_STATUS}",
        "commit_created=false",
        "push_executed=false",
        "next_required_object=phase_vs0_closure_v0",
        (
            "terminal_transition=ADVANCE("
            "BOOKKEEPING_COMMIT_PHASE_VS0_EVIDENCE_YIELD_REPORT_V0_PENDING)"
        ),
    ]
    print("\n".join(lines))


def print_typed_stop(exc: ReportFailure) -> None:
    lines = [
        "BUILD_PHASE_VS0_EVIDENCE_YIELD_REPORT_V0_TYPED_STOP",
        "report_id=phase_vs0_evidence_yield_report_v0",
        "phase_id=PHASE_VS0",
        "phase_step=VS0.5",
        f"evidence_yield_report_gate={exc.code}",
        "yield_branch=DIAGNOSTIC_YIELD",
        f"missing_or_invalid_source={exc.source}",
        f"violating_field={exc.field}",
        f"expected_value={exc.expected}",
        f"actual_value={exc.actual}",
        f"next_lawful_surface={exc.next_surface}",
        "self_repair_performed=false",
        "phase_closure_performed_by_vs0_5=false",
        "commit_created=false",
        "push_executed=false",
        f"terminal_transition=STOP({exc.code})",
    ]
    print("\n".join(lines))


def run() -> int:
    root = detect_repo_root(Path.cwd())
    validate_dirty_scope(root)
    _, _, _, vs0_4 = verify_source_statuses(root)
    validate_battery_boundaries(vs0_4)
    groups = collect_source_groups(root, vs0_4)
    before_hashes = hash_groups(root, groups)
    confirmations = confirmation_events()
    diagnostics = diagnostic_events(root, vs0_4)
    if len(confirmations) != 4:
        fail("VS0_5_FAIL_CONFIRMATION_YIELD_MISSING")
    if len(diagnostics) != 10:
        fail("VS0_5_FAIL_DIAGNOSTIC_YIELD_MISSING")

    after_hashes = hash_groups(root, groups)
    report = build_report(
        confirmations,
        diagnostics,
        before_hashes,
        after_hashes,
    )
    markdown = render_markdown()
    overclaim_hits = markdown_contains_overclaim(markdown)
    if overclaim_hits:
        fail_for_markdown_overclaims(overclaim_hits)

    write_json(root, report)
    write_markdown(root, markdown)

    final_hashes = hash_groups(root, groups)
    if final_hashes != after_hashes:
        fail("VS0_5_FAIL_PRIOR_VS0_SOURCE_MUTATED")
    validate_dirty_scope(root)
    print_complete()
    return 0


def main() -> int:
    try:
        return run()
    except ReportFailure as exc:
        print_typed_stop(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
