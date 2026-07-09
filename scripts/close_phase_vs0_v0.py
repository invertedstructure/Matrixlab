#!/usr/bin/env python3

"""Close Phase VS0 from committed VS0.1-VS0.5 evidence only."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT = "scripts/close_phase_vs0_v0.py"
EXPECTED_HEAD = "1a1306a2c84ef747d1a5aa50e706048b5800fa04"
OUTPUT_JSON = "docs/matrixlabs/phase_vs0/phase_vs0_closure_v0.json"
OUTPUT_MD = "docs/matrixlabs/phase_vs0/phase_vs0_closure_v0.md"

PHASE_ID = "PHASE_VS0"
PHASE_NAME = "A_TO_F_FIRST_SPECIMEN_RUNTIME_V0"
PASS_GATE = (
    "VS0_6_PHASE_CLOSURE_PASS_FIRST_A_TO_F_SPECIMEN_WITH_TYPED_STOPS_"
    "AND_EVIDENCE_YIELD"
)
PHASE_STATUS = (
    "PHASE_VS0_PASS_FIRST_A_TO_F_SPECIMEN_WITH_TYPED_NEGATIVE_STOPS_"
    "AND_EVIDENCE_YIELD"
)
TERMINAL_TRANSITION = (
    "ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS0_CLOSURE_V0_PENDING)"
)

VS0_1_JSON = "docs/matrixlabs/phase_vs0/phase_vs0_source_inventory_v0.json"
VS0_1_MD = "docs/matrixlabs/phase_vs0/phase_vs0_source_inventory_v0.md"
VS0_2_JSON = "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_build_receipt_v0.json"
VS0_2_MD = "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_build_receipt_v0.md"
VS0_3_JSON = "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_verification_v0.json"
VS0_3_MD = "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_verification_v0.md"
RUN_ROOT = "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0"
A_TO_F_ROOT = f"{RUN_ROOT}/a_to_f"
CHAIN_INDEX_JSON = f"{A_TO_F_ROOT}/phase_vs0_a_to_f_chain_index_v0.json"
CHAIN_INDEX_MD = f"{A_TO_F_ROOT}/phase_vs0_a_to_f_chain_index_v0.md"
NEGATIVE_ROOT = f"{RUN_ROOT}/negative_probes"
VS0_4_DEFINITIONS = f"{NEGATIVE_ROOT}/phase_vs0_negative_probe_definitions_v0.json"
VS0_4_JSON = f"{NEGATIVE_ROOT}/phase_vs0_negative_probe_battery_v0.json"
VS0_4_MD = f"{NEGATIVE_ROOT}/phase_vs0_negative_probe_battery_v0.md"
VS0_5_JSON = "docs/matrixlabs/phase_vs0/phase_vs0_evidence_yield_report_v0.json"
VS0_5_MD = "docs/matrixlabs/phase_vs0/phase_vs0_evidence_yield_report_v0.md"

VS0_1_STATUS = "VS0_PREFLIGHT_PASS_SCOPE_DECLARED"
VS0_2_STATUS = "VS0_2_HAPPY_PATH_BUILD_PASS_A_TO_F_PHASE_SPECIMEN_CREATED"
VS0_3_STATUS = "VS0_3_HAPPY_PATH_VERIFICATION_PASS_A_TO_F_PHASE_SPECIMEN_VERIFIED"
VS0_4_STATUS = "VS0_4_NEGATIVE_PROBES_PASS_TYPED_STOPS"
VS0_5_STATUS = "VS0_5_EVIDENCE_YIELD_REPORT_PASS_USEFUL_EVIDENCE_PRESENT"

SOURCE_COMMITS = {
    "commit_bindings_recorded": True,
    "vs0_1_source_inventory_commit_sha": (
        "742643e358af9bdb54efdcdcabdf667cbc48fd85"
    ),
    "vs0_2_happy_path_build_original_commit_sha": (
        "49ebcf1393893bbbc61c5fcd48359770c3e554e7"
    ),
    "vs0_2_happy_path_build_repair_commit_sha": (
        "9f7277608f8e475fa84f6e4697e0db0903200aac"
    ),
    "vs0_3_happy_path_verification_commit_sha": (
        "daec73d1a631225a00b7d0ad967880dd9d3b301c"
    ),
    "vs0_4_negative_probe_battery_commit_sha": (
        "6f1fb917564dd70262520778c1c8ced7a825a525"
    ),
    "vs0_5_evidence_yield_report_commit_sha": EXPECTED_HEAD,
}

FAILURE_CODES = [
    "VS0_6_STOP_SOURCE_INVENTORY_MISSING",
    "VS0_6_STOP_SOURCE_INVENTORY_NOT_PASS",
    "VS0_6_STOP_HAPPY_PATH_BUILD_MISSING",
    "VS0_6_STOP_HAPPY_PATH_BUILD_NOT_PASS",
    "VS0_6_STOP_HAPPY_PATH_VERIFICATION_MISSING",
    "VS0_6_STOP_HAPPY_PATH_VERIFICATION_NOT_PASS",
    "VS0_6_STOP_NEGATIVE_PROBE_BATTERY_MISSING",
    "VS0_6_STOP_NEGATIVE_PROBE_BATTERY_NOT_PASS",
    "VS0_6_STOP_EVIDENCE_YIELD_REPORT_MISSING",
    "VS0_6_STOP_EVIDENCE_YIELD_REPORT_NOT_PASS",
    "VS0_6_FAIL_CONFIRMATION_YIELD_ABSENT",
    "VS0_6_FAIL_DIAGNOSTIC_YIELD_ABSENT",
    "VS0_6_FAIL_DECISION_RELEVANT_EVIDENCE_ABSENT",
    "VS0_6_FAIL_SOURCE_HASH_SNAPSHOT_MISSING",
    "VS0_6_FAIL_SOURCE_COMMIT_SNAPSHOT_MISSING",
    "VS0_6_FAIL_PRIOR_VS0_SOURCE_MUTATED",
    "VS0_6_FAIL_EVIDENCE_YIELD_REPORT_MUTATED",
    "VS0_6_FAIL_A_TO_F_ARTIFACTS_MUTATED",
    "VS0_6_FAIL_NEGATIVE_PROBE_RECEIPTS_MUTATED",
    "VS0_6_FAIL_PHASE_CLOSURE_PRECLAIMED",
    "VS0_6_FAIL_ACTIVE_REGISTRY_CLAIMED",
    "VS0_6_FAIL_REGISTRY_PROMOTION_CLAIMED",
    "VS0_6_FAIL_TRACE_GENERALIZATION_CLAIMED",
    "VS0_6_FAIL_PERFORMANCE_OPTIMIZATION_CLAIMED",
    "VS0_6_FAIL_SCALE_OPTIMIZATION_CLAIMED",
    "VS0_6_FAIL_RUNNER_READINESS_CLAIMED",
    "VS0_6_FAIL_RUNNER_AUTHORITY_CREATED",
    "VS0_6_FAIL_NEXT_PHASE_AUTO_SELECTED",
    "VS0_6_FAIL_NEXT_SURFACE_CREATED_INSIDE_CLOSURE",
    "VS0_6_FAIL_DISCUSSION_PACKETS_IN_SCOPE",
    "VS0_6_FAIL_TOTAL_ILLEGAL_PATH_COVERAGE_CLAIMED",
]


class ClosureFailure(RuntimeError):
    def __init__(
        self,
        code: str,
        *,
        source: str = "NONE",
        field: str = "NONE",
        expected: object = "NONE",
        actual: object = "NONE",
        next_surface: str = "REPAIR_VS0_SOURCE_OR_CLOSURE_INPUT",
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
    next_surface: str = "REPAIR_VS0_SOURCE_OR_CLOSURE_INPUT",
) -> None:
    raise ClosureFailure(
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
            "VS0_6_FAIL_PRIOR_VS0_SOURCE_MUTATED",
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
            "VS0_6_STOP_EVIDENCE_YIELD_REPORT_MISSING",
            source=VS0_5_JSON,
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
    for line in run_git(
        root, ["status", "--short", "--untracked-files=all"]
    ).splitlines():
        path = status_path(line)
        if path in allowed_exact or any(
            path.startswith(prefix) for prefix in allowed_prefixes
        ):
            continue
        fail(
            "VS0_6_FAIL_PRIOR_VS0_SOURCE_MUTATED",
            source=path,
            field="dirty_scope",
            expected="only VS0.6 closure, baseline_share, or discussion_packets",
            actual=line,
        )


def require_head(root: Path) -> None:
    head = run_git(root, ["rev-parse", "HEAD"])
    if head != EXPECTED_HEAD:
        fail(
            "VS0_6_FAIL_SOURCE_COMMIT_SNAPSHOT_MISSING",
            field="HEAD",
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
    current: Any = obj
    for part in path.split("."):
        if not isinstance(current, dict):
            return default
        current = current.get(part, default)
    return current


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


def verify_source_statuses(root: Path) -> tuple[dict[str, Any], ...]:
    vs0_1 = load_json(root, VS0_1_JSON, "VS0_6_STOP_SOURCE_INVENTORY_MISSING")
    vs0_2 = load_json(root, VS0_2_JSON, "VS0_6_STOP_HAPPY_PATH_BUILD_MISSING")
    vs0_3 = load_json(
        root,
        VS0_3_JSON,
        "VS0_6_STOP_HAPPY_PATH_VERIFICATION_MISSING",
    )
    vs0_4 = load_json(root, VS0_4_JSON, "VS0_6_STOP_NEGATIVE_PROBE_BATTERY_MISSING")
    vs0_5 = load_json(root, VS0_5_JSON, "VS0_6_STOP_EVIDENCE_YIELD_REPORT_MISSING")

    require_equal(
        vs0_1.get("inventory_status"),
        VS0_1_STATUS,
        "VS0_6_STOP_SOURCE_INVENTORY_NOT_PASS",
        VS0_1_JSON,
        "inventory_status",
    )
    require_equal(
        vs0_2.get("happy_path_build_status"),
        VS0_2_STATUS,
        "VS0_6_STOP_HAPPY_PATH_BUILD_NOT_PASS",
        VS0_2_JSON,
        "happy_path_build_status",
    )
    require_equal(
        get_value(vs0_3, "verification_result.happy_path_verification_status"),
        VS0_3_STATUS,
        "VS0_6_STOP_HAPPY_PATH_VERIFICATION_NOT_PASS",
        VS0_3_JSON,
        "verification_result.happy_path_verification_status",
    )
    require_equal(
        get_value(vs0_4, "battery_result.negative_probe_battery_status"),
        VS0_4_STATUS,
        "VS0_6_STOP_NEGATIVE_PROBE_BATTERY_NOT_PASS",
        VS0_4_JSON,
        "battery_result.negative_probe_battery_status",
    )
    require_equal(
        get_value(vs0_5, "yield_result.evidence_yield_report_status"),
        VS0_5_STATUS,
        "VS0_6_STOP_EVIDENCE_YIELD_REPORT_NOT_PASS",
        VS0_5_JSON,
        "yield_result.evidence_yield_report_status",
    )

    source_statuses = vs0_5.get("source_statuses", {})
    expected_statuses = {
        "vs0_1_status": VS0_1_STATUS,
        "vs0_2_status": VS0_2_STATUS,
        "vs0_3_status": VS0_3_STATUS,
        "vs0_4_status": VS0_4_STATUS,
    }
    for field, expected in expected_statuses.items():
        require_equal(
            source_statuses.get(field),
            expected,
            "VS0_6_STOP_EVIDENCE_YIELD_REPORT_NOT_PASS",
            VS0_5_JSON,
            f"source_statuses.{field}",
        )

    return vs0_1, vs0_2, vs0_3, vs0_4, vs0_5


def verify_vs0_5_boundaries(vs0_5: dict[str, Any]) -> None:
    if get_value(vs0_5, "closure_readiness_boundary.phase_closed") is not False:
        fail(
            "VS0_6_FAIL_PHASE_CLOSURE_PRECLAIMED",
            source=VS0_5_JSON,
            field="closure_readiness_boundary.phase_closed",
            expected=False,
            actual=get_value(vs0_5, "closure_readiness_boundary.phase_closed"),
        )
    if get_value(vs0_5, "yield_result.phase_closure_performed_by_vs0_5") is not False:
        fail(
            "VS0_6_FAIL_PHASE_CLOSURE_PRECLAIMED",
            source=VS0_5_JSON,
            field="yield_result.phase_closure_performed_by_vs0_5",
            expected=False,
            actual=get_value(vs0_5, "yield_result.phase_closure_performed_by_vs0_5"),
        )
    if get_value(vs0_5, "yield_result.confirmation_yield_present") is not True:
        fail("VS0_6_FAIL_CONFIRMATION_YIELD_ABSENT", source=VS0_5_JSON)
    if get_value(vs0_5, "yield_result.diagnostic_yield_present") is not True:
        fail("VS0_6_FAIL_DIAGNOSTIC_YIELD_ABSENT", source=VS0_5_JSON)
    if get_value(vs0_5, "yield_result.decision_relevant_evidence_present") is not True:
        fail("VS0_6_FAIL_DECISION_RELEVANT_EVIDENCE_ABSENT", source=VS0_5_JSON)
    if get_value(vs0_5, "source_hash_snapshots.all_prior_source_hashes_unchanged") is not True:
        fail(
            "VS0_6_FAIL_SOURCE_HASH_SNAPSHOT_MISSING",
            source=VS0_5_JSON,
            field="source_hash_snapshots.all_prior_source_hashes_unchanged",
            expected=True,
            actual=get_value(
                vs0_5,
                "source_hash_snapshots.all_prior_source_hashes_unchanged",
            ),
        )
    if get_value(vs0_5, "source_commits.source_vs0_4_commit_sha") != SOURCE_COMMITS[
        "vs0_4_negative_probe_battery_commit_sha"
    ]:
        fail(
            "VS0_6_FAIL_SOURCE_COMMIT_SNAPSHOT_MISSING",
            source=VS0_5_JSON,
            field="source_commits.source_vs0_4_commit_sha",
            expected=SOURCE_COMMITS["vs0_4_negative_probe_battery_commit_sha"],
            actual=get_value(vs0_5, "source_commits.source_vs0_4_commit_sha"),
        )

    for field, code in {
        "active_registry_claimed": "VS0_6_FAIL_ACTIVE_REGISTRY_CLAIMED",
        "registry_promotion_claimed": "VS0_6_FAIL_REGISTRY_PROMOTION_CLAIMED",
        "trace_generalization_claimed": "VS0_6_FAIL_TRACE_GENERALIZATION_CLAIMED",
        "performance_optimization_claimed": (
            "VS0_6_FAIL_PERFORMANCE_OPTIMIZATION_CLAIMED"
        ),
        "scale_optimization_claimed": "VS0_6_FAIL_SCALE_OPTIMIZATION_CLAIMED",
        "runner_readiness_claimed": "VS0_6_FAIL_RUNNER_READINESS_CLAIMED",
        "runner_authority_created": "VS0_6_FAIL_RUNNER_AUTHORITY_CREATED",
        "phase_closure_claimed_by_vs0_5": "VS0_6_FAIL_PHASE_CLOSURE_PRECLAIMED",
    }.items():
        value = get_value(vs0_5, f"overclaim_guard.{field}")
        if value is not False:
            fail(
                code,
                source=VS0_5_JSON,
                field=f"overclaim_guard.{field}",
                expected=False,
                actual=value,
            )

    for field, value in vs0_5.get("source_preservation", {}).items():
        if value is not False:
            fail(
                "VS0_6_FAIL_PRIOR_VS0_SOURCE_MUTATED",
                source=VS0_5_JSON,
                field=f"source_preservation.{field}",
                expected=False,
                actual=value,
            )


def require_file(root: Path, rel_path: str, code: str) -> None:
    if not (root / rel_path).is_file():
        fail(
            code,
            source=rel_path,
            field="file_presence",
            expected=True,
            actual=False,
        )


def unique_paths(paths: list[str]) -> list[str]:
    return sorted(dict.fromkeys(paths))


def collect_hash_groups(
    root: Path,
    chain_index: dict[str, Any],
    vs0_4: dict[str, Any],
) -> dict[str, list[str]]:
    artifacts: list[str] = []
    for artifact in chain_index.get("artifacts", []):
        path = artifact.get("path")
        if not isinstance(path, str):
            fail(
                "VS0_6_FAIL_A_TO_F_ARTIFACTS_MUTATED",
                source=CHAIN_INDEX_JSON,
                field="artifacts.path",
                expected="string path",
                actual=path,
            )
        if not path.startswith(f"{A_TO_F_ROOT}/"):
            fail(
                "VS0_6_FAIL_A_TO_F_ARTIFACTS_MUTATED",
                source=CHAIN_INDEX_JSON,
                field="artifacts.path",
                expected=f"{A_TO_F_ROOT}/...",
                actual=path,
            )
        artifacts.append(path)

    receipt_paths: list[str] = []
    for probe in vs0_4.get("probe_results", []):
        path = probe.get("receipt_path")
        if not isinstance(path, str):
            fail(
                "VS0_6_FAIL_NEGATIVE_PROBE_RECEIPTS_MUTATED",
                source=VS0_4_JSON,
                field="probe_results.receipt_path",
                expected="string path",
                actual=path,
            )
        if not path.startswith(f"{NEGATIVE_ROOT}/receipts/"):
            fail(
                "VS0_6_FAIL_NEGATIVE_PROBE_RECEIPTS_MUTATED",
                source=VS0_4_JSON,
                field="probe_results.receipt_path",
                expected=f"{NEGATIVE_ROOT}/receipts/...",
                actual=path,
            )
        receipt_paths.append(path)
    if len(receipt_paths) != 10:
        fail(
            "VS0_6_FAIL_NEGATIVE_PROBE_RECEIPTS_MUTATED",
            source=VS0_4_JSON,
            field="probe_results.receipt_path_count",
            expected=10,
            actual=len(receipt_paths),
        )

    groups = {
        "vs0_1_source_inventory": [VS0_1_JSON, VS0_1_MD],
        "vs0_2_happy_path_build": [VS0_2_JSON, VS0_2_MD],
        "vs0_3_happy_path_verification": [VS0_3_JSON, VS0_3_MD],
        "vs0_4_negative_probe_battery": [
            VS0_4_DEFINITIONS,
            VS0_4_JSON,
            VS0_4_MD,
        ],
        "vs0_5_evidence_yield_report": [VS0_5_JSON, VS0_5_MD],
        "a_to_f_artifacts": [CHAIN_INDEX_JSON, CHAIN_INDEX_MD, *artifacts],
        "negative_probe_receipts": receipt_paths,
    }
    for group, paths in groups.items():
        code = "VS0_6_FAIL_PRIOR_VS0_SOURCE_MUTATED"
        if group == "vs0_5_evidence_yield_report":
            code = "VS0_6_FAIL_EVIDENCE_YIELD_REPORT_MUTATED"
        elif group == "a_to_f_artifacts":
            code = "VS0_6_FAIL_A_TO_F_ARTIFACTS_MUTATED"
        elif group == "negative_probe_receipts":
            code = "VS0_6_FAIL_NEGATIVE_PROBE_RECEIPTS_MUTATED"
        for path in paths:
            require_file(root, path, code)
    return {group: unique_paths(paths) for group, paths in groups.items()}


def hash_groups(
    root: Path,
    groups: dict[str, list[str]],
) -> dict[str, dict[str, str]]:
    return {
        group: {path: sha256(root / path) for path in paths}
        for group, paths in groups.items()
    }


def flatten_hashes(group_hashes: dict[str, dict[str, str]]) -> dict[str, str]:
    flattened: dict[str, str] = {}
    for paths in group_hashes.values():
        flattened.update(paths)
    return dict(sorted(flattened.items()))


def fail_for_hash_mutation(
    before: dict[str, dict[str, str]],
    after: dict[str, dict[str, str]],
) -> None:
    if before == after:
        return
    for group in before:
        if before[group] == after.get(group):
            continue
        code = "VS0_6_FAIL_PRIOR_VS0_SOURCE_MUTATED"
        if group == "vs0_5_evidence_yield_report":
            code = "VS0_6_FAIL_EVIDENCE_YIELD_REPORT_MUTATED"
        elif group == "a_to_f_artifacts":
            code = "VS0_6_FAIL_A_TO_F_ARTIFACTS_MUTATED"
        elif group == "negative_probe_receipts":
            code = "VS0_6_FAIL_NEGATIVE_PROBE_RECEIPTS_MUTATED"
        fail(
            code,
            source=group,
            field="source_hash_snapshot",
            expected=before[group],
            actual=after.get(group),
        )


def source_steps() -> dict[str, dict[str, Any]]:
    return {
        "vs0_1": {
            "artifact": "phase_vs0_source_inventory_v0",
            "path": VS0_1_JSON,
            "required_status": VS0_1_STATUS,
            "passed": True,
        },
        "vs0_2": {
            "artifact": "phase_vs0_happy_path_build_receipt_v0",
            "path": VS0_2_JSON,
            "required_status": VS0_2_STATUS,
            "passed": True,
        },
        "vs0_3": {
            "artifact": "phase_vs0_happy_path_verification_v0",
            "path": VS0_3_JSON,
            "required_status": VS0_3_STATUS,
            "passed": True,
        },
        "vs0_4": {
            "artifact": "phase_vs0_negative_probe_battery_v0",
            "path": VS0_4_JSON,
            "required_status": VS0_4_STATUS,
            "passed": True,
        },
        "vs0_5": {
            "artifact": "phase_vs0_evidence_yield_report_v0",
            "path": VS0_5_JSON,
            "required_status": VS0_5_STATUS,
            "passed": True,
        },
    }


def build_closure(
    before_hashes: dict[str, dict[str, str]],
    after_hashes: dict[str, dict[str, str]],
    vs0_5: dict[str, Any],
) -> dict[str, Any]:
    yield_summary = vs0_5.get("yield_summary", {})
    return {
        "schema_version": "matrixlabs_phase_vs0_closure_v0",
        "closure_id": "phase_vs0_closure_v0",
        "phase_id": PHASE_ID,
        "phase_name": PHASE_NAME,
        "phase_step": "VS0.6",
        "closure_role": "PHASE_CLOSURE_ONLY",
        "definition": (
            "VS0.6 is a machine-primary phase closure object that consumes "
            "the committed VS0.1 source inventory, VS0.2 happy-path build "
            "receipt, VS0.3 happy-path verification, VS0.4 negative probe "
            "battery, and VS0.5 Evidence Yield report; verifies that each "
            "required phase step passed; records source hashes and "
            "closure-critical non-effects; emits the final bounded Phase "
            "VS0 result; and closes the phase without claiming active "
            "registry, trace generalization, performance optimization, "
            "scale optimization, total illegal-path coverage, runner "
            "readiness, next-phase selection, or any new authority."
        ),
        "short_form": "VS0.6 seals the VS0 evidence packet.",
        "closure_gate": PASS_GATE,
        "phase_status": PHASE_STATUS,
        "source_vs0_5_required_before_closure": True,
        "source_commits": SOURCE_COMMITS,
        "source_steps": source_steps(),
        "source_hash_snapshot": {
            "hash_algorithm": "sha256",
            "source_hashes_recorded": True,
            "inputs": flatten_hashes(before_hashes),
            "groups": before_hashes,
            "after_closure": after_hashes,
            "all_source_hashes_unchanged_by_vs0_6": before_hashes == after_hashes,
        },
        "closure_execution_mode": {
            "phase_closure_only": True,
            "adds_new_evidence": False,
            "reruns_happy_path_verification": False,
            "runs_new_negative_probes": False,
            "rebuilds_evidence_yield_report": False,
            "mutates_prior_vs0_artifacts": False,
            "selects_next_phase": False,
            "creates_next_decision_surface": False,
            "creates_runner_authority": False,
            "creates_active_registry": False,
            "promotes_registry_candidate": False,
            "generalizes_trace": False,
        },
        "phase_result": {
            "a_to_f_phase_specimen_created": True,
            "happy_path_verified": True,
            "negative_probe_battery_passed": True,
            "evidence_yield_reported": True,
            "confirmation_yield_present": True,
            "diagnostic_yield_present": True,
            "decision_relevant_evidence_present": True,
        },
        "evidence_summary": {
            "confirmation_yield_sources": [
                "VS0.1 preflight pass",
                "VS0.2 happy-path build pass",
                "VS0.3 happy-path verification pass",
                "VS0.4 negative battery execution pass",
                "VS0.5 Evidence Yield report pass",
            ],
            "diagnostic_yield_sources": [
                "VS0.4 selected negative probe typed stops",
            ],
            "evidence_yield_result": "USEFUL_EVIDENCE_PRESENT",
            "decision_relevant_evidence_present": True,
            "event_count_is_descriptive_not_value_claim": True,
            "evidence_yield_report_recomputed_by_vs0_6": False,
            "confirmation_yield_events": yield_summary.get(
                "confirmation_yield_events"
            ),
            "diagnostic_yield_events": yield_summary.get("diagnostic_yield_events"),
            "total_decision_relevant_events": yield_summary.get(
                "total_decision_relevant_events"
            ),
        },
        "confirmed_boundaries": {
            "active_registry_created": False,
            "trace_generalized": False,
            "performance_optimization_claimed": False,
            "scale_optimization_claimed": False,
            "runner_readiness_claimed": False,
            "runner_authority_created": False,
            "additional_machine_proceed_authorized": False,
            "next_unit_executed": False,
            "source_authority_replaced_by_compression": False,
        },
        "coverage_boundary": {
            "selected_negative_probe_battery_passed": True,
            "selected_probe_battery_only": True,
            "all_possible_illegal_shortcuts_tested": False,
            "future_live_runtime_coverage_claimed": False,
            "multi_specimen_stability_claimed": False,
            "cross_context_generalization_claimed": False,
            "general_runtime_safety_claimed": False,
        },
        "authority_boundary": {
            "closure_grants_new_authority": False,
            "closure_authorizes_runner": False,
            "closure_authorizes_active_registry": False,
            "closure_authorizes_generalization": False,
            "closure_authorizes_next_unit_execution": False,
            "closure_authorizes_radius_renewal": False,
            "closure_authorizes_additional_machine_proceed": False,
            "closure_replaces_source_authority": False,
        },
        "closure_claim_scope": {
            "phase_vs0_closed": True,
            "closed_phase_id": PHASE_ID,
            "closed_phase_name": PHASE_NAME,
            "global_system_closed": False,
            "runner_closed_or_ready": False,
            "registry_closed_or_promoted": False,
            "future_phase_selected": False,
        },
        "phase_pass_scope": {
            "local_phase_pass": True,
            "single_a_to_f_specimen": True,
            "selected_negative_probe_battery_only": True,
            "multi_specimen_stability_claimed": False,
            "cross_context_generalization_claimed": False,
            "future_live_runtime_coverage_claimed": False,
            "runner_readiness_claimed": False,
        },
        "next_lawful_surface": {
            "surface_name": "POST_VS0_DIRECTION_DECISION_SURFACE",
            "surface_named_by_closure": True,
            "surface_artifact_created_by_closure": False,
            "decision_required": True,
            "human_decision_required": True,
            "machine_may_select_next_phase": False,
            "next_phase_auto_selected": False,
            "recommended_options_are_non_binding": True,
            "recommended_options": [
                "RUNNER_PRECONDITION_AUDIT_V0",
                "UNIT_FEEDBACK_HARDENING_V0",
                "ACTIVE_OBSERVABILITY_REGISTRY_PROMOTION_V0",
                "MULTI_SPECIMEN_STABILITY_SURFACE_V0",
                "STOP_AFTER_VS0_ARCHIVE_ONLY",
            ],
        },
        "source_preservation": {
            "vs0_1_source_inventory_mutated_by_vs0_6": False,
            "vs0_2_happy_path_build_mutated_by_vs0_6": False,
            "vs0_3_happy_path_verification_mutated_by_vs0_6": False,
            "vs0_4_negative_probe_battery_mutated_by_vs0_6": False,
            "vs0_5_evidence_yield_report_mutated_by_vs0_6": False,
            "a_to_f_artifacts_mutated_by_vs0_6": False,
            "negative_probe_receipts_mutated_by_vs0_6": False,
        },
        "precommit_phase_vs0_closure_gate": "PASS",
        "phase_vs0_closure_gate": PASS_GATE,
        "failure_vocabulary": FAILURE_CODES,
        "failures": [],
        "terminal_transition": TERMINAL_TRANSITION,
    }


def render_markdown() -> str:
    return """# Phase VS0 closure v0

## Status

PHASE_VS0_PASS_FIRST_A_TO_F_SPECIMEN_WITH_TYPED_NEGATIVE_STOPS_AND_EVIDENCE_YIELD

## Closure gate

VS0_6_PHASE_CLOSURE_PASS_FIRST_A_TO_F_SPECIMEN_WITH_TYPED_STOPS_AND_EVIDENCE_YIELD

## Sources

- VS0.1 source inventory: PASS
- VS0.2 happy-path A\u2192F build: PASS
- VS0.3 happy-path verification: PASS
- VS0.4 negative probe battery: PASS
- VS0.5 Evidence Yield report: PASS

## Phase result

- one A\u2192F phase specimen was created
- happy path was verified
- selected illegal shortcuts stopped with typed diagnostics
- Confirmation Yield was present
- Diagnostic Yield was present
- useful decision-relevant evidence was present
- Phase VS0 closed: true

## Boundaries preserved

- no active registry created
- no trace generalization claimed
- no performance optimization claimed
- no scale optimization claimed
- no runner readiness claimed
- no runner authority created
- no next-unit execution authorized
- no additional machine proceed authorized

## Coverage boundary

- selected negative probe battery passed
- selected probe battery only: true
- all possible illegal shortcuts tested: false
- future live runtime coverage claimed: false
- multi-specimen stability claimed: false
- cross-context generalization claimed: false

## Next lawful surface

POST_VS0_DIRECTION_DECISION_SURFACE

- surface named by closure: true
- surface artifact created by closure: false
- human decision required: true
- machine may select next phase: false
- next phase auto-selected: false
- recommended options are non-binding: true

## Non-claim

VS0.6 closes Phase VS0 only as a bounded local phase closure. It does not select or authorize the next phase, activate a registry, promote a registry candidate, generalize the trace, optimize performance, claim total coverage, or create runner authority.
"""


def markdown_contains_vs0_6_overclaim(md: str) -> list[str]:
    """
    Return forbidden VS0.6 overclaim hits while allowing local closure.
    """
    allowed_patterns = [
        r"\bphase vs0 closed\s*[:=]\s*true\b",
        r"\bphase_vs0_closed\s*[:=]\s*true\b",
        r"\bvs0\.6 closes phase vs0\b",
        r"\bcloses phase vs0 only as a bounded local phase closure\b",
        r"\bdoes not select or authorize the next phase\b",
        r"\bdoes not activate a registry\b",
        r"\bdoes not promote a registry candidate\b",
        r"\bdoes not generalize the trace\b",
        r"\bdoes not .* optimize performance\b",
        r"\bdoes not .* claim total coverage\b",
        r"\bdoes not .* create runner authority\b",
        r"\ball possible illegal shortcuts tested\s*[:=]\s*false\b",
        r"\bfuture live runtime coverage claimed\s*[:=]\s*false\b",
        r"\bmulti-specimen stability claimed\s*[:=]\s*false\b",
        r"\bcross-context generalization claimed\s*[:=]\s*false\b",
        r"\bmachine may select next phase\s*[:=]\s*false\b",
        r"\bnext phase auto-selected\s*[:=]\s*false\b",
        r"\bsurface artifact created by closure\s*[:=]\s*false\b",
        r"\brecommended options are non-binding\s*[:=]\s*true\b",
    ]
    forbidden_patterns = {
        "runtime ready": r"\bruntime ready\b",
        "runner ready": r"\brunner ready\b",
        "registry active": r"\bregistry active\b",
        "registry promoted": r"\bregistry promoted\b",
        "system safe": r"\bsystem safe\b",
        "all shortcuts covered": r"\ball shortcuts covered\b",
        "all illegal paths tested": r"\ball illegal paths tested\b",
        "total coverage": r"\btotal coverage\b",
        "performance improved": r"\bperformance improved\b",
        "scale improved": r"\bscale improved\b",
        "next phase selected": r"\bnext phase selected\b",
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
        "runtime ready": "VS0_6_FAIL_RUNNER_READINESS_CLAIMED",
        "runner ready": "VS0_6_FAIL_RUNNER_READINESS_CLAIMED",
        "registry active": "VS0_6_FAIL_ACTIVE_REGISTRY_CLAIMED",
        "registry promoted": "VS0_6_FAIL_REGISTRY_PROMOTION_CLAIMED",
        "system safe": "VS0_6_FAIL_TRACE_GENERALIZATION_CLAIMED",
        "all shortcuts covered": (
            "VS0_6_FAIL_TOTAL_ILLEGAL_PATH_COVERAGE_CLAIMED"
        ),
        "all illegal paths tested": (
            "VS0_6_FAIL_TOTAL_ILLEGAL_PATH_COVERAGE_CLAIMED"
        ),
        "total coverage": "VS0_6_FAIL_TOTAL_ILLEGAL_PATH_COVERAGE_CLAIMED",
        "performance improved": (
            "VS0_6_FAIL_PERFORMANCE_OPTIMIZATION_CLAIMED"
        ),
        "scale improved": "VS0_6_FAIL_SCALE_OPTIMIZATION_CLAIMED",
        "next phase selected": "VS0_6_FAIL_NEXT_PHASE_AUTO_SELECTED",
    }
    code = "VS0_6_FAIL_TOTAL_ILLEGAL_PATH_COVERAGE_CLAIMED"
    for label, candidate in label_to_code.items():
        if label in first_hit:
            code = candidate
            break
    fail(
        code,
        source=OUTPUT_MD,
        field="markdown_overclaim_guard",
        expected=[],
        actual=hits,
        next_surface="REPAIR_VS0_6_CLOSURE_MARKDOWN",
    )


def write_json(root: Path, value: dict[str, Any]) -> None:
    path = root / OUTPUT_JSON
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_markdown(root: Path, value: str) -> None:
    path = root / OUTPUT_MD
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def print_complete() -> None:
    lines = [
        "BUILD_PHASE_VS0_CLOSURE_V0_COMPLETE",
        "closure_id=phase_vs0_closure_v0",
        "schema_version=matrixlabs_phase_vs0_closure_v0",
        "phase_id=PHASE_VS0",
        "phase_name=A_TO_F_FIRST_SPECIMEN_RUNTIME_V0",
        "phase_step=VS0.6",
        "closure_role=PHASE_CLOSURE_ONLY",
        f"source_vs0_5_commit_sha={EXPECTED_HEAD}",
        f"source_inventory_status={VS0_1_STATUS}",
        f"happy_path_build_status={VS0_2_STATUS}",
        f"happy_path_verification_status={VS0_3_STATUS}",
        f"negative_probe_battery_status={VS0_4_STATUS}",
        f"evidence_yield_report_status={VS0_5_STATUS}",
        "source_hash_snapshot_recorded=true",
        "source_commit_snapshot_recorded=true",
        "confirmation_yield_present=true",
        "diagnostic_yield_present=true",
        "decision_relevant_evidence_present=true",
        "phase_vs0_closed=true",
        "local_phase_pass=true",
        "single_a_to_f_specimen=true",
        "selected_negative_probe_battery_only=true",
        "active_registry_claimed=false",
        "registry_promotion_claimed=false",
        "trace_generalization_claimed=false",
        "performance_optimization_claimed=false",
        "scale_optimization_claimed=false",
        "runner_readiness_claimed=false",
        "runner_authority_created=false",
        "all_possible_illegal_shortcuts_tested=false",
        "future_live_runtime_coverage_claimed=false",
        "multi_specimen_stability_claimed=false",
        "cross_context_generalization_claimed=false",
        "next_lawful_surface=POST_VS0_DIRECTION_DECISION_SURFACE",
        "next_surface_named_by_closure=true",
        "next_surface_created_by_vs0_6=false",
        "human_decision_required=true",
        "machine_may_select_next_phase=false",
        "next_phase_auto_selected=false",
        "recommended_options_are_non_binding=true",
        "vs0_1_source_inventory_mutated_by_vs0_6=false",
        "vs0_2_happy_path_build_mutated_by_vs0_6=false",
        "vs0_3_happy_path_verification_mutated_by_vs0_6=false",
        "vs0_4_negative_probe_battery_mutated_by_vs0_6=false",
        "vs0_5_evidence_yield_report_mutated_by_vs0_6=false",
        "a_to_f_artifacts_mutated_by_vs0_6=false",
        "negative_probe_receipts_mutated_by_vs0_6=false",
        "precommit_phase_vs0_closure_gate=PASS",
        f"phase_vs0_closure_gate={PASS_GATE}",
        f"phase_status={PHASE_STATUS}",
        "commit_created=false",
        "push_executed=false",
        f"terminal_transition={TERMINAL_TRANSITION}",
    ]
    print("\n".join(lines))


def print_typed_stop(exc: ClosureFailure) -> None:
    lines = [
        "BUILD_PHASE_VS0_CLOSURE_V0_TYPED_STOP",
        "closure_id=phase_vs0_closure_v0",
        "phase_id=PHASE_VS0",
        "phase_step=VS0.6",
        f"phase_vs0_closure_gate={exc.code}",
        f"missing_or_invalid_source={exc.source}",
        f"violating_field={exc.field}",
        f"expected_value={exc.expected}",
        f"actual_value={exc.actual}",
        f"next_lawful_surface={exc.next_surface}",
        "phase_vs0_closed=false",
        "commit_created=false",
        "push_executed=false",
        f"terminal_transition=STOP({exc.code})",
    ]
    print("\n".join(lines))


def run() -> int:
    root = detect_repo_root(Path.cwd())
    require_head(root)
    validate_dirty_scope(root)

    _, _, _, vs0_4, vs0_5 = verify_source_statuses(root)
    verify_vs0_5_boundaries(vs0_5)
    chain_index = load_json(
        root,
        CHAIN_INDEX_JSON,
        "VS0_6_FAIL_A_TO_F_ARTIFACTS_MUTATED",
    )
    groups = collect_hash_groups(root, chain_index, vs0_4)
    before_hashes = hash_groups(root, groups)
    if not before_hashes:
        fail("VS0_6_FAIL_SOURCE_HASH_SNAPSHOT_MISSING")

    after_hashes = hash_groups(root, groups)
    fail_for_hash_mutation(before_hashes, after_hashes)

    closure = build_closure(before_hashes, after_hashes, vs0_5)
    markdown = render_markdown()
    overclaim_hits = markdown_contains_vs0_6_overclaim(markdown)
    if overclaim_hits:
        fail_for_markdown_overclaims(overclaim_hits)

    write_json(root, closure)
    write_markdown(root, markdown)

    final_hashes = hash_groups(root, groups)
    fail_for_hash_mutation(before_hashes, final_hashes)
    validate_dirty_scope(root)
    print_complete()
    return 0


def main() -> int:
    try:
        return run()
    except ClosureFailure as exc:
        print_typed_stop(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
