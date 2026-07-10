#!/usr/bin/env python3

"""Build VS1.5 missing precondition next-surface map from VS1.4 readiness audit."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT = "scripts/build_phase_vs1_missing_precondition_next_surface_map_v0.py"
EXPECTED_HEAD = "68c846386a79cc89215c1b16dbd1389333269b80"
OUTPUT_JSON = (
    "docs/matrixlabs/phase_vs1/"
    "phase_vs1_missing_precondition_next_surface_map_v0.json"
)
OUTPUT_MD = (
    "docs/matrixlabs/phase_vs1/"
    "phase_vs1_missing_precondition_next_surface_map_v0.md"
)

SOURCE_READINESS_AUDIT_JSON = (
    "docs/matrixlabs/phase_vs1/phase_vs1_controlled_loop_readiness_audit_v0.json"
)
SOURCE_READINESS_AUDIT_MD = (
    "docs/matrixlabs/phase_vs1/phase_vs1_controlled_loop_readiness_audit_v0.md"
)
SOURCE_INVENTORY_JSON = (
    "docs/matrixlabs/phase_vs1/phase_vs1_controlled_loop_precondition_inventory_v0.json"
)
SOURCE_INVENTORY_MD = (
    "docs/matrixlabs/phase_vs1/phase_vs1_controlled_loop_precondition_inventory_v0.md"
)
SOURCE_CONTRACT_JSON = (
    "docs/matrixlabs/phase_vs1/phase_vs1_controlled_convergence_loop_contract_v0.json"
)
SOURCE_CONTRACT_MD = (
    "docs/matrixlabs/phase_vs1/phase_vs1_controlled_convergence_loop_contract_v0.md"
)
SOURCE_INTAKE_JSON = "docs/matrixlabs/phase_vs1/phase_vs1_post_vs0_source_intake_v0.json"
SOURCE_INTAKE_MD = "docs/matrixlabs/phase_vs1/phase_vs1_post_vs0_source_intake_v0.md"
DIRECTION_JSON = "docs/matrixlabs/phase_vs1/post_vs0_direction_decision_receipt_v0.json"
DIRECTION_MD = "docs/matrixlabs/phase_vs1/post_vs0_direction_decision_receipt_v0.md"
VS0_ROOT = "docs/matrixlabs/phase_vs0"

SCHEMA_VERSION = "matrixlabs_phase_vs1_missing_precondition_next_surface_map_v0"
ARTIFACT_ID = "phase_vs1_missing_precondition_next_surface_map_v0"
PHASE_ID = "PHASE_VS1"
UNIT_ID = "VS1.5_MISSING_PRECONDITION_NEXT_SURFACE_MAP"
UNIT_ROLE = "NEXT_SURFACE_MAPPING_ONLY"

SOURCE_READINESS_AUDIT_GATE = (
    "VS1_4_CONTROLLED_LOOP_READINESS_AUDIT_PASS_NOT_READY_BLOCKERS_EXPOSED"
)
SOURCE_READINESS_READY_GATE = (
    "VS1_4_CONTROLLED_LOOP_READINESS_AUDIT_PASS_READY_FOR_HUMAN_EXECUTION_AUTHORITY_DECISION"
)
SOURCE_READINESS_TRANSITION = "ADVANCE(VS1_5_MISSING_PRECONDITION_NEXT_SURFACE_MAP_PENDING)"
PRIMARY_VERDICT = "CONTROLLED_LOOP_NOT_READY_MIXED_BLOCKERS"
MAP_VERDICT = "VS1_5_MISSING_PRECONDITION_NEXT_SURFACE_MAP_PASS"
ARTIFACT_TRANSITION = "ADVANCE(VS1_6_PHASE_CLOSURE_PENDING)"
PRINT_TRANSITION = (
    "ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS1_MISSING_PRECONDITION_NEXT_SURFACE_MAP_V0_PENDING)"
)

EXPECTED_COMPONENTS = [
    "C01_SCOPE_REGIME_DECLARATION_CONTRACT",
    "C02_TYPED_STATE_OBJECT_CONTRACT",
    "C03_EXPLICIT_MOVE_SPACE_CONTRACT",
    "C04_MOVE_SELECTOR_CONTRACT",
    "C05_MOVE_APPLICATOR_CONTRACT",
    "C06_AUTHORITY_POLICY",
    "C07_RADIUS_BUDGET_POLICY",
    "C08_HALT_POLICY",
    "C09_RECEIPT_OBLIGATION_CONTRACT",
    "C10_SOURCE_IDENTITY_FRESHNESS_POLICY",
    "C11_MICRO_SWEEP_BOUNDS_CONTRACT",
    "C12_PRESSURE_READOUT_CONTRACT",
    "C13_PRESSURE_CLASSIFICATION_VOCABULARY",
    "C14_LOCAL_REVISION_SURFACE_CONTRACT",
    "C15_BOUNDED_PORTABILITY_MAP_CONTRACT",
    "C16_REPLAY_AUDIT_CONTRACT",
    "C17_FORBIDDEN_EFFECT_GUARD",
    "C18_EVIDENCE_YIELD_REPORT_HOOK",
    "C19_HUMAN_ESCALATION_DECISION_BOUNDARY",
    "C20_CONVERGENCE_CRITERION_CONTRACT",
]

EXPECTED_SURFACES = [
    "S01_SCOPE_REGIME_DECLARATION_CONTRACT_SURFACE",
    "S02_TYPED_STATE_OBJECT_CONTRACT_SURFACE",
    "S03_MOVE_SPACE_CONTRACT_SURFACE",
    "S04_MOVE_SELECTOR_CONTRACT_SURFACE",
    "S05_MOVE_APPLICATOR_CONTRACT_SURFACE",
    "S06_AUTHORITY_POLICY_SURFACE",
    "S07_RADIUS_BUDGET_POLICY_SURFACE",
    "S08_HALT_POLICY_SURFACE",
    "S09_RECEIPT_OBLIGATION_CONTRACT_SURFACE",
    "S10_SOURCE_IDENTITY_FRESHNESS_POLICY_SURFACE",
    "S11_MICRO_SWEEP_BOUNDS_CONTRACT_SURFACE",
    "S12_PRESSURE_READOUT_CONTRACT_SURFACE",
    "S13_PRESSURE_CLASSIFICATION_VOCABULARY_SURFACE",
    "S14_LOCAL_REVISION_SURFACE_CONTRACT",
    "S15_BOUNDED_PORTABILITY_MAP_CONTRACT_SURFACE",
    "S16_REPLAY_AUDIT_CONTRACT_SURFACE",
    "S17_FORBIDDEN_EFFECT_GUARD_SURFACE",
    "S18_EVIDENCE_YIELD_HOOK_SURFACE",
    "S19_HUMAN_ESCALATION_DECISION_BOUNDARY_SURFACE",
    "S20_CONVERGENCE_CRITERION_CONTRACT_SURFACE",
    "S21_CONTROLLED_LOOP_READINESS_REAUDIT_SURFACE",
]

COMPONENT_TO_SURFACE = {
    "C01_SCOPE_REGIME_DECLARATION_CONTRACT": "S01_SCOPE_REGIME_DECLARATION_CONTRACT_SURFACE",
    "C02_TYPED_STATE_OBJECT_CONTRACT": "S02_TYPED_STATE_OBJECT_CONTRACT_SURFACE",
    "C03_EXPLICIT_MOVE_SPACE_CONTRACT": "S03_MOVE_SPACE_CONTRACT_SURFACE",
    "C04_MOVE_SELECTOR_CONTRACT": "S04_MOVE_SELECTOR_CONTRACT_SURFACE",
    "C05_MOVE_APPLICATOR_CONTRACT": "S05_MOVE_APPLICATOR_CONTRACT_SURFACE",
    "C06_AUTHORITY_POLICY": "S06_AUTHORITY_POLICY_SURFACE",
    "C07_RADIUS_BUDGET_POLICY": "S07_RADIUS_BUDGET_POLICY_SURFACE",
    "C08_HALT_POLICY": "S08_HALT_POLICY_SURFACE",
    "C09_RECEIPT_OBLIGATION_CONTRACT": "S09_RECEIPT_OBLIGATION_CONTRACT_SURFACE",
    "C10_SOURCE_IDENTITY_FRESHNESS_POLICY": "S10_SOURCE_IDENTITY_FRESHNESS_POLICY_SURFACE",
    "C11_MICRO_SWEEP_BOUNDS_CONTRACT": "S11_MICRO_SWEEP_BOUNDS_CONTRACT_SURFACE",
    "C12_PRESSURE_READOUT_CONTRACT": "S12_PRESSURE_READOUT_CONTRACT_SURFACE",
    "C13_PRESSURE_CLASSIFICATION_VOCABULARY": "S13_PRESSURE_CLASSIFICATION_VOCABULARY_SURFACE",
    "C14_LOCAL_REVISION_SURFACE_CONTRACT": "S14_LOCAL_REVISION_SURFACE_CONTRACT",
    "C15_BOUNDED_PORTABILITY_MAP_CONTRACT": "S15_BOUNDED_PORTABILITY_MAP_CONTRACT_SURFACE",
    "C16_REPLAY_AUDIT_CONTRACT": "S16_REPLAY_AUDIT_CONTRACT_SURFACE",
    "C17_FORBIDDEN_EFFECT_GUARD": "S17_FORBIDDEN_EFFECT_GUARD_SURFACE",
    "C18_EVIDENCE_YIELD_REPORT_HOOK": "S18_EVIDENCE_YIELD_HOOK_SURFACE",
    "C19_HUMAN_ESCALATION_DECISION_BOUNDARY": "S19_HUMAN_ESCALATION_DECISION_BOUNDARY_SURFACE",
    "C20_CONVERGENCE_CRITERION_CONTRACT": "S20_CONVERGENCE_CRITERION_CONTRACT_SURFACE",
}

SURFACE_TYPE = {
    "S01_SCOPE_REGIME_DECLARATION_CONTRACT_SURFACE": "CONTRACT_DEFINITION_SURFACE",
    "S02_TYPED_STATE_OBJECT_CONTRACT_SURFACE": "CONTRACT_DEFINITION_SURFACE",
    "S03_MOVE_SPACE_CONTRACT_SURFACE": "CONTRACT_DEFINITION_SURFACE",
    "S04_MOVE_SELECTOR_CONTRACT_SURFACE": "CONTRACT_DEFINITION_SURFACE",
    "S05_MOVE_APPLICATOR_CONTRACT_SURFACE": "CONTRACT_DEFINITION_SURFACE",
    "S06_AUTHORITY_POLICY_SURFACE": "POLICY_DEFINITION_SURFACE",
    "S07_RADIUS_BUDGET_POLICY_SURFACE": "POLICY_DEFINITION_SURFACE",
    "S08_HALT_POLICY_SURFACE": "POLICY_DEFINITION_SURFACE",
    "S09_RECEIPT_OBLIGATION_CONTRACT_SURFACE": "RECEIPT_CONTRACT_SURFACE",
    "S10_SOURCE_IDENTITY_FRESHNESS_POLICY_SURFACE": "SOURCE_IDENTITY_VERIFICATION_SURFACE",
    "S11_MICRO_SWEEP_BOUNDS_CONTRACT_SURFACE": "SWEEP_BOUNDING_SURFACE",
    "S12_PRESSURE_READOUT_CONTRACT_SURFACE": "READOUT_VOCABULARY_SURFACE",
    "S13_PRESSURE_CLASSIFICATION_VOCABULARY_SURFACE": "READOUT_VOCABULARY_SURFACE",
    "S14_LOCAL_REVISION_SURFACE_CONTRACT": "REVISION_SURFACE_CONTRACT",
    "S15_BOUNDED_PORTABILITY_MAP_CONTRACT_SURFACE": "PORTABILITY_MAP_CONTRACT_SURFACE",
    "S16_REPLAY_AUDIT_CONTRACT_SURFACE": "REPLAY_AUDIT_CONTRACT_SURFACE",
    "S17_FORBIDDEN_EFFECT_GUARD_SURFACE": "FORBIDDEN_EFFECT_GUARD_SURFACE",
    "S18_EVIDENCE_YIELD_HOOK_SURFACE": "EVIDENCE_YIELD_HOOK_SURFACE",
    "S19_HUMAN_ESCALATION_DECISION_BOUNDARY_SURFACE": "HUMAN_ESCALATION_BOUNDARY_SURFACE",
    "S20_CONVERGENCE_CRITERION_CONTRACT_SURFACE": "CONVERGENCE_CRITERION_CONTRACT_SURFACE",
    "S21_CONTROLLED_LOOP_READINESS_REAUDIT_SURFACE": "CONTROLLED_LOOP_READINESS_REAUDIT_SURFACE",
}

SURFACE_STATUS = {
    "S01_SCOPE_REGIME_DECLARATION_CONTRACT_SURFACE": "SURFACE_REQUIRES_SCHEMA_FIRST",
    "S02_TYPED_STATE_OBJECT_CONTRACT_SURFACE": "SURFACE_REQUIRES_SCHEMA_FIRST",
    "S03_MOVE_SPACE_CONTRACT_SURFACE": "SURFACE_REQUIRES_SCHEMA_FIRST",
    "S04_MOVE_SELECTOR_CONTRACT_SURFACE": "SURFACE_REQUIRES_SCHEMA_FIRST",
    "S05_MOVE_APPLICATOR_CONTRACT_SURFACE": "SURFACE_REQUIRES_SCHEMA_FIRST",
    "S06_AUTHORITY_POLICY_SURFACE": "SURFACE_REQUIRES_AUTHORITY_FIRST",
    "S07_RADIUS_BUDGET_POLICY_SURFACE": "SURFACE_REQUIRED_BLOCKER",
    "S08_HALT_POLICY_SURFACE": "SURFACE_REQUIRED_BLOCKER",
    "S09_RECEIPT_OBLIGATION_CONTRACT_SURFACE": "SURFACE_REQUIRED_BLOCKER",
    "S10_SOURCE_IDENTITY_FRESHNESS_POLICY_SURFACE": "SURFACE_REQUIRES_SOURCE_VERIFICATION_FIRST",
    "S11_MICRO_SWEEP_BOUNDS_CONTRACT_SURFACE": "SURFACE_REQUIRED_BLOCKER",
    "S12_PRESSURE_READOUT_CONTRACT_SURFACE": "SURFACE_REQUIRED_BLOCKER",
    "S13_PRESSURE_CLASSIFICATION_VOCABULARY_SURFACE": "SURFACE_REQUIRED_BLOCKER",
    "S14_LOCAL_REVISION_SURFACE_CONTRACT": "SURFACE_REQUIRED_BLOCKER",
    "S15_BOUNDED_PORTABILITY_MAP_CONTRACT_SURFACE": "SURFACE_REQUIRED_BLOCKER",
    "S16_REPLAY_AUDIT_CONTRACT_SURFACE": "SURFACE_REQUIRED_BLOCKER",
    "S17_FORBIDDEN_EFFECT_GUARD_SURFACE": "SURFACE_REQUIRED_BLOCKER",
    "S18_EVIDENCE_YIELD_HOOK_SURFACE": "SURFACE_REQUIRED_BLOCKER",
    "S19_HUMAN_ESCALATION_DECISION_BOUNDARY_SURFACE": "SURFACE_REQUIRES_HUMAN_DECISION",
    "S20_CONVERGENCE_CRITERION_CONTRACT_SURFACE": "SURFACE_REQUIRED_BLOCKER",
    "S21_CONTROLLED_LOOP_READINESS_REAUDIT_SURFACE": "SURFACE_OPTIONAL_SUPPORT",
}

DEPENDENCY_LAYERS = [
    {
        "layer": 0,
        "layer_name": "SOURCE_TRUST",
        "surface_ids": ["S10_SOURCE_IDENTITY_FRESHNESS_POLICY_SURFACE"],
    },
    {
        "layer": 1,
        "layer_name": "SCOPE_REGIME_CONVERGENCE_AND_CORE_STRUCTURAL_CONTRACTS",
        "surface_ids": [
            "S01_SCOPE_REGIME_DECLARATION_CONTRACT_SURFACE",
            "S02_TYPED_STATE_OBJECT_CONTRACT_SURFACE",
            "S03_MOVE_SPACE_CONTRACT_SURFACE",
            "S04_MOVE_SELECTOR_CONTRACT_SURFACE",
            "S05_MOVE_APPLICATOR_CONTRACT_SURFACE",
            "S20_CONVERGENCE_CRITERION_CONTRACT_SURFACE",
        ],
    },
    {
        "layer": 2,
        "layer_name": "CONTROL_AND_AUTHORITY",
        "surface_ids": [
            "S06_AUTHORITY_POLICY_SURFACE",
            "S07_RADIUS_BUDGET_POLICY_SURFACE",
            "S08_HALT_POLICY_SURFACE",
            "S19_HUMAN_ESCALATION_DECISION_BOUNDARY_SURFACE",
        ],
    },
    {
        "layer": 3,
        "layer_name": "RECEIPT_AND_AUDIT",
        "surface_ids": [
            "S09_RECEIPT_OBLIGATION_CONTRACT_SURFACE",
            "S16_REPLAY_AUDIT_CONTRACT_SURFACE",
            "S17_FORBIDDEN_EFFECT_GUARD_SURFACE",
        ],
    },
    {
        "layer": 4,
        "layer_name": "SWEEP_AND_PRESSURE",
        "surface_ids": [
            "S11_MICRO_SWEEP_BOUNDS_CONTRACT_SURFACE",
            "S12_PRESSURE_READOUT_CONTRACT_SURFACE",
            "S13_PRESSURE_CLASSIFICATION_VOCABULARY_SURFACE",
            "S18_EVIDENCE_YIELD_HOOK_SURFACE",
        ],
    },
    {
        "layer": 5,
        "layer_name": "REVISION_AND_PORTABILITY",
        "surface_ids": [
            "S14_LOCAL_REVISION_SURFACE_CONTRACT",
            "S15_BOUNDED_PORTABILITY_MAP_CONTRACT_SURFACE",
        ],
    },
    {
        "layer": 6,
        "layer_name": "READINESS_REAUDIT",
        "surface_ids": ["S21_CONTROLLED_LOOP_READINESS_REAUDIT_SURFACE"],
    },
]

RANKING_ORDER = [
    "S10_SOURCE_IDENTITY_FRESHNESS_POLICY_SURFACE",
    "S01_SCOPE_REGIME_DECLARATION_CONTRACT_SURFACE",
    "S02_TYPED_STATE_OBJECT_CONTRACT_SURFACE",
    "S03_MOVE_SPACE_CONTRACT_SURFACE",
    "S04_MOVE_SELECTOR_CONTRACT_SURFACE",
    "S05_MOVE_APPLICATOR_CONTRACT_SURFACE",
    "S20_CONVERGENCE_CRITERION_CONTRACT_SURFACE",
    "S06_AUTHORITY_POLICY_SURFACE",
    "S07_RADIUS_BUDGET_POLICY_SURFACE",
    "S08_HALT_POLICY_SURFACE",
    "S19_HUMAN_ESCALATION_DECISION_BOUNDARY_SURFACE",
    "S09_RECEIPT_OBLIGATION_CONTRACT_SURFACE",
    "S16_REPLAY_AUDIT_CONTRACT_SURFACE",
    "S17_FORBIDDEN_EFFECT_GUARD_SURFACE",
    "S11_MICRO_SWEEP_BOUNDS_CONTRACT_SURFACE",
    "S12_PRESSURE_READOUT_CONTRACT_SURFACE",
    "S13_PRESSURE_CLASSIFICATION_VOCABULARY_SURFACE",
    "S18_EVIDENCE_YIELD_HOOK_SURFACE",
    "S14_LOCAL_REVISION_SURFACE_CONTRACT",
    "S15_BOUNDED_PORTABILITY_MAP_CONTRACT_SURFACE",
    "S21_CONTROLLED_LOOP_READINESS_REAUDIT_SURFACE",
]
RANK_BY_SURFACE = {surface_id: index for index, surface_id in enumerate(RANKING_ORDER, start=1)}

FORBIDDEN_EFFECTS = [
    "do_not_authorize_loop_execution",
    "do_not_create_runner",
    "do_not_run_micro_sweeps",
    "do_not_generalize_trace",
    "do_not_select_next_phase",
    "do_not_build_surface_artifact",
    "do_not_repair_component",
    "do_not_promote_candidate",
]

FORBIDDEN_ARTIFACTS = [
    "docs/matrixlabs/runner",
    "docs/matrixlabs/runtime",
    "docs/matrixlabs/move_space",
    "docs/matrixlabs/micro_sweeps",
    "docs/matrixlabs/phase_vs1/phase_vs1_selected_next_phase_decision_receipt_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_surface_build_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_component_repair_plan_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_component_build_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_candidate_promotion_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_human_execution_authority_receipt_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_closure_v0.json",
]

PLACEHOLDER_VALUES = {
    "<derived_candidate_or_null>",
    "<derived_rank>",
    "<surface_id>",
    "<TBD>",
    "TBD",
    "TODO",
    "UNKNOWN",
    "PLACEHOLDER",
    "",
}


class MapFailure(RuntimeError):
    def __init__(
        self,
        code: str,
        *,
        source: str = "NONE",
        blocker: str = "NONE",
        surface: str = "NONE",
        field: str = "NONE",
        expected: object = "NONE",
        actual: object = "NONE",
        next_surface: str = "REPAIR_VS1_5_MISSING_PRECONDITION_MAP_INPUT",
    ) -> None:
        super().__init__(code)
        self.code = code
        self.source = source
        self.blocker = blocker
        self.surface = surface
        self.field = field
        self.expected = expected
        self.actual = actual
        self.next_surface = next_surface


def fail(
    code: str,
    *,
    source: str = "NONE",
    blocker: str = "NONE",
    surface: str = "NONE",
    field: str = "NONE",
    expected: object = "NONE",
    actual: object = "NONE",
    next_surface: str = "REPAIR_VS1_5_MISSING_PRECONDITION_MAP_INPUT",
) -> None:
    raise MapFailure(
        code,
        source=source,
        blocker=blocker,
        surface=surface,
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
            "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
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
            "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
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
        if path in allowed_exact or any(path.startswith(prefix) for prefix in allowed_prefixes):
            continue
        fail(
            "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
            source=path,
            field="dirty_scope",
            expected="only VS1.5 outputs, baseline_share, or discussion_packets",
            actual=line,
        )


def require_head(root: Path) -> None:
    head = run_git(root, ["rev-parse", "HEAD"])
    if head != EXPECTED_HEAD:
        fail(
            "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
            source="HEAD",
            field="commit_sha",
            expected=EXPECTED_HEAD,
            actual=head,
        )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(root: Path, rel_path: str) -> dict[str, Any]:
    path = root / rel_path
    if not path.is_file():
        fail(
            "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
            source=rel_path,
            field="file_presence",
            expected=True,
            actual=False,
        )
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(
            "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
            source=rel_path,
            field="valid_json",
            expected=True,
            actual=str(exc),
        )
    if not isinstance(value, dict):
        fail(
            "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
            source=rel_path,
            field="json_object",
            expected=True,
            actual=type(value).__name__,
        )
    return value


def require_file(root: Path, rel_path: str) -> None:
    if not (root / rel_path).is_file():
        fail(
            "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
            source=rel_path,
            field="file_presence",
            expected=True,
            actual=False,
        )


def get_value(obj: dict[str, Any], path: str, default: Any = None) -> Any:
    cur: Any = obj
    for part in path.split("."):
        if not isinstance(cur, dict):
            return default
        cur = cur.get(part, default)
    return cur


def source_paths(root: Path) -> list[str]:
    paths = [
        SOURCE_READINESS_AUDIT_JSON,
        SOURCE_READINESS_AUDIT_MD,
        SOURCE_INVENTORY_JSON,
        SOURCE_INVENTORY_MD,
        SOURCE_CONTRACT_JSON,
        SOURCE_CONTRACT_MD,
        SOURCE_INTAKE_JSON,
        SOURCE_INTAKE_MD,
        DIRECTION_JSON,
        DIRECTION_MD,
    ]
    vs0_root = root / VS0_ROOT
    if vs0_root.is_dir():
        for path in sorted(vs0_root.rglob("*")):
            if path.is_file():
                paths.append(path.relative_to(root).as_posix())
    return sorted(set(paths))


def capture_source_hashes(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for rel_path in source_paths(root):
        path = root / rel_path
        if not path.is_file():
            fail(
                "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
                source=rel_path,
                field="source_file",
                expected="present",
                actual="missing",
            )
        hashes[rel_path] = sha256(path)
    return hashes


def validate_source_preservation(before: dict[str, str], after: dict[str, str]) -> None:
    if before == after:
        return
    changed = sorted(
        path for path in set(before) | set(after) if before.get(path) != after.get(path)
    )
    first = changed[0] if changed else "unknown"
    fail(
        "STOP_VS1_5_SOURCE_MUTATED",
        source=first,
        field="source_hash",
        expected=before.get(first),
        actual=after.get(first),
    )


def ensure_no_forbidden_artifacts(root: Path) -> None:
    for rel_path in FORBIDDEN_ARTIFACTS:
        if (root / rel_path).exists():
            fail(
                "STOP_VS1_5_FORBIDDEN_ARTIFACT_EXISTS",
                source=rel_path,
                field="forbidden_artifact",
                expected="absent",
                actual="present",
            )


def dependency_layer_for(surface_id: str) -> int:
    for layer in DEPENDENCY_LAYERS:
        if surface_id in layer["surface_ids"]:
            return int(layer["layer"])
    fail(
        "STOP_VS1_5_SURFACE_FIELD_INVALID",
        surface=surface_id,
        field="dependency_layer",
        expected="declared layer",
        actual="missing",
    )


def validate_source_audit(audit: dict[str, Any]) -> None:
    if audit.get("artifact_id") != "phase_vs1_controlled_loop_readiness_audit_v0":
        fail(
            "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
            source=SOURCE_READINESS_AUDIT_JSON,
            field="artifact_id",
            expected="phase_vs1_controlled_loop_readiness_audit_v0",
            actual=audit.get("artifact_id"),
        )
    if audit.get("readiness_audit_gate") != SOURCE_READINESS_AUDIT_GATE:
        fail(
            "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
            source=SOURCE_READINESS_AUDIT_JSON,
            field="readiness_audit_gate",
            expected=SOURCE_READINESS_AUDIT_GATE,
            actual=audit.get("readiness_audit_gate"),
        )
    if get_value(audit, "terminal_transition.transition") != SOURCE_READINESS_TRANSITION:
        fail(
            "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
            source=SOURCE_READINESS_AUDIT_JSON,
            field="terminal_transition.transition",
            expected=SOURCE_READINESS_TRANSITION,
            actual=get_value(audit, "terminal_transition.transition"),
        )
    if get_value(audit, "aggregate_readiness_verdict.primary_verdict") != PRIMARY_VERDICT:
        fail(
            "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
            source=SOURCE_READINESS_AUDIT_JSON,
            field="aggregate_readiness_verdict.primary_verdict",
            expected=PRIMARY_VERDICT,
            actual=get_value(audit, "aggregate_readiness_verdict.primary_verdict"),
        )
    if get_value(audit, "aggregate_readiness_verdict.controlled_loop_ready") is not False:
        fail(
            "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
            source=SOURCE_READINESS_AUDIT_JSON,
            field="aggregate_readiness_verdict.controlled_loop_ready",
            expected=False,
            actual=get_value(audit, "aggregate_readiness_verdict.controlled_loop_ready"),
        )
    if get_value(audit, "aggregate_readiness_verdict.missing_or_blocked_component_count") != 20:
        fail(
            "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
            source=SOURCE_READINESS_AUDIT_JSON,
            field="aggregate_readiness_verdict.missing_or_blocked_component_count",
            expected=20,
            actual=get_value(
                audit, "aggregate_readiness_verdict.missing_or_blocked_component_count"
            ),
        )


def derivations_by_component(audit: dict[str, Any]) -> dict[str, dict[str, Any]]:
    derivations = get_value(audit, "readiness_derivation_table.component_derivations", [])
    if not isinstance(derivations, list) or len(derivations) != 20:
        fail(
            "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
            source=SOURCE_READINESS_AUDIT_JSON,
            field="readiness_derivation_table.component_derivations",
            expected=20,
            actual=len(derivations) if isinstance(derivations, list) else type(derivations).__name__,
        )
    by_component: dict[str, dict[str, Any]] = {}
    for record in derivations:
        if not isinstance(record, dict):
            fail(
                "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
                source=SOURCE_READINESS_AUDIT_JSON,
                field="component_derivation",
                expected="object",
                actual=type(record).__name__,
            )
        key = record.get("component_key")
        if key in PLACEHOLDER_VALUES or key not in EXPECTED_COMPONENTS:
            fail(
                "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
                source=SOURCE_READINESS_AUDIT_JSON,
                blocker=str(key),
                field="component_key",
                expected=EXPECTED_COMPONENTS,
                actual=key,
            )
        by_component[key] = record
    if list(by_component.keys()) != EXPECTED_COMPONENTS:
        fail(
            "STOP_VS1_5_READINESS_AUDIT_NOT_PASS",
            source=SOURCE_READINESS_AUDIT_JSON,
            field="component_derivation_order",
            expected=EXPECTED_COMPONENTS,
            actual=list(by_component.keys()),
        )
    return by_component


def build_surface_candidate(
    surface_id: str,
    component_key: str | None,
    derivation: dict[str, Any] | None,
) -> dict[str, Any]:
    layer = dependency_layer_for(surface_id)
    if component_key and derivation:
        readiness_result = derivation.get("primary_readiness_status")
        secondary = derivation.get("secondary_readiness_blockers", [])
        blockers = [readiness_result, *secondary]
        blocker_classes = derivation.get("blocker_classes", [])
        component_ids = [component_key]
    else:
        readiness_result = PRIMARY_VERDICT
        blockers = ["READINESS_REAUDIT_AFTER_BLOCKERS"]
        blocker_classes = ["READINESS_REAUDIT_BLOCKER"]
        component_ids = EXPECTED_COMPONENTS.copy()
    rank = RANK_BY_SURFACE[surface_id]
    ranking_basis = (
        f"non-binding advisory rank {rank}; dependency layer {layer}; "
        "S21 remains after unresolved required blocker surfaces"
    )
    return {
        "surface_id": surface_id,
        "surface_name": surface_id[4:] if surface_id.startswith("S") else surface_id,
        "surface_type": SURFACE_TYPE[surface_id],
        "surface_status": SURFACE_STATUS[surface_id],
        "source_readiness_result": readiness_result,
        "source_readiness_blockers": blockers,
        "component_ids_addressed": component_ids,
        "blocker_classes_addressed": blocker_classes,
        "dependency_layer": layer,
        "rank": rank,
        "ranking_basis": ranking_basis,
        "expected_output_artifact": (
            "docs/matrixlabs/phase_vs1/candidate_surface_records/"
            f"{surface_id.lower()}_v0.json"
        ),
        "required_inputs": [
            SOURCE_READINESS_AUDIT_JSON,
            SOURCE_INVENTORY_JSON,
            SOURCE_CONTRACT_JSON,
            component_key or "all_prior_required_blocker_surfaces",
        ],
        "required_authority": "HUMAN_OR_NEXT_PHASE_SELECTION_REQUIRED",
        "forbidden_effects": FORBIDDEN_EFFECTS.copy(),
        "may_be_selected_by_human": True,
        "machine_selected": False,
        "surface_candidate_record_created_by_vs1_5": True,
        "surface_artifact_created_by_vs1_5": False,
        "surface_build_authorized_by_vs1_5": False,
        "surface_selected_by_vs1_5": False,
    }


def build_surface_map(root: Path, audit: dict[str, Any]) -> dict[str, Any]:
    derivations = derivations_by_component(audit)
    surface_candidates = []
    for surface_id in EXPECTED_SURFACES:
        component_key = next(
            (
                component
                for component, mapped_surface in COMPONENT_TO_SURFACE.items()
                if mapped_surface == surface_id
            ),
            None,
        )
        surface_candidates.append(
            build_surface_candidate(
                surface_id,
                component_key,
                derivations.get(component_key) if component_key else None,
            )
        )
    ranked = sorted(
        [
        {
            "surface_id": candidate["surface_id"],
            "rank": candidate["rank"],
            "ranking_basis": candidate["ranking_basis"],
            "ranking_is_binding": False,
            "machine_selected": False,
            "build_authorized": False,
        }
        for candidate in surface_candidates
        ],
        key=lambda item: item["rank"],
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "artifact_id": ARTIFACT_ID,
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "unit_role": UNIT_ROLE,
        "source_readiness_audit": {
            "artifact_id": "phase_vs1_controlled_loop_readiness_audit_v0",
            "path": SOURCE_READINESS_AUDIT_JSON,
            "commit_sha": EXPECTED_HEAD,
            "sha256": sha256(root / SOURCE_READINESS_AUDIT_JSON),
            "allowed_statuses": [
                SOURCE_READINESS_AUDIT_GATE,
                SOURCE_READINESS_READY_GATE,
            ],
            "required_transition": SOURCE_READINESS_TRANSITION,
            "source_role": "TYPED_READINESS_RESULT_SOURCE",
        },
        "expected_current_branch_from_vs1_4": {
            "source_readiness_audit_commit_sha": EXPECTED_HEAD,
            "readiness_audit_gate": SOURCE_READINESS_AUDIT_GATE,
            "primary_verdict": PRIMARY_VERDICT,
            "controlled_loop_ready": False,
            "ready_component_count": 0,
            "missing_or_blocked_component_count": 20,
            "mapping_branch": "NOT_READY_BLOCKER_MAP",
            "ready_branch_surface_included": False,
        },
        "mapping_branch": "NOT_READY_BLOCKER_MAP",
        "mapping_policy": {
            "maps_typed_readiness_results_only": True,
            "repairs_allowed": False,
            "component_build_allowed": False,
            "candidate_promotion_allowed": False,
            "loop_execution_authorized": False,
            "runner_created": False,
            "next_phase_auto_selected": False,
            "authority_consumed": False,
            "surface_artifact_creation_allowed": False,
            "machine_selection_allowed": False,
        },
        "blocker_coverage": {
            "source_blocker_count": 20,
            "mapped_blocker_count": 20,
            "unmapped_blocker_count": 0,
            "all_typed_blockers_mapped": True,
            "out_of_scope_blockers": [],
        },
        "blocker_to_surface_map": {
            component: [surface] for component, surface in COMPONENT_TO_SURFACE.items()
        },
        "surface_candidates": surface_candidates,
        "dependency_layers": DEPENDENCY_LAYERS,
        "advisory_ranking_policy": {
            "ranking_enabled": True,
            "ranking_is_binding": False,
            "ranking_affects_candidate_validity": False,
            "ranking_selects_next_phase": False,
            "ranking_authorizes_build": False,
            "ranking_authorizes_repair": False,
            "ranking_authorizes_execution": False,
            "allowed_ranking_criteria": [
                "source_identity_freshness_first",
                "scope_and_core_contracts_before_control_policy",
                "receipt_and_guard_surfaces_before_sweep_surfaces",
                "readiness_reaudit_after_required_blocker_surfaces",
            ],
            "forbidden_ranking_criteria": [
                "speed_to_execution",
                "machine_preference",
                "auto_select_next_phase",
                "authorize_build_from_rank",
            ],
        },
        "advisory_ranking": {
            "ranking_enabled": True,
            "ranking_is_binding": False,
            "machine_selected_next_phase": False,
            "advisory_first_surface_candidate": "S10_SOURCE_IDENTITY_FRESHNESS_POLICY_SURFACE",
            "advisory_first_surface_is_selected_next_phase": False,
            "ranking_basis": "non-binding dependency and source-trust ordering only",
        },
        "ranked_surface_candidates": ranked,
        "readiness_reaudit_boundary": {
            "s21_candidate_allowed": True,
            "s21_requires_prior_blocker_resolution_evidence": True,
            "s21_ranked_before_unresolved_required_blockers": False,
            "s21_executed_by_vs1_5": False,
        },
        "ready_branch_surface_candidate": {
            "surface_id": "S_READY_HUMAN_EXECUTION_AUTHORITY_DECISION_SURFACE",
            "included_current_branch": False,
            "included_only_if_ready_branch": True,
            "surface_type": "AUTHORITY_DECISION_SURFACE",
            "machine_selected": False,
            "authority_consumed": False,
            "loop_execution_authorized": False,
        },
        "vs1_6_boundary": {
            "vs1_6_may_close_phase_vs1_from_map": True,
            "vs1_6_may_select_post_vs1_phase": False,
            "vs1_6_may_authorize_surface_build": False,
            "vs1_6_may_authorize_loop_execution": False,
            "vs1_6_built": False,
            "vs1_6_run": False,
        },
        "forbidden_claim_checks": {
            "surface_built": False,
            "surface_artifact_created": False,
            "repair_attempted": False,
            "component_build_attempted": False,
            "candidate_promotion_attempted": False,
            "human_authority_consumed": False,
            "loop_execution_authorized": False,
            "runner_created": False,
            "micro_sweeps_authorized": False,
            "local_revision_authorized": False,
            "next_phase_auto_selected": False,
            "ranking_used_as_selection": False,
            "global_generalization_claimed": False,
            "optimization_target_assumed": False,
            "phase_closure_claimed": False,
            "post_vs1_phase_selected": False,
            "vs1_6_executed": False,
        },
        "source_preservation": {
            "source_readiness_audit_mutated_by_vs1_5": False,
            "source_inventory_mutated_by_vs1_5": False,
            "source_contract_mutated_by_vs1_5": False,
            "vs1_1_source_intake_mutated_by_vs1_5": False,
            "post_vs0_direction_decision_receipt_mutated_by_vs1_5": False,
            "vs0_source_artifacts_mutated_by_vs1_5": False,
        },
        "non_claims": {
            "loop_ready": False,
            "loop_may_execute": False,
            "runner_exists": False,
            "runner_readiness_exists": False,
            "runner_authority_exists": False,
            "mapped_surface_selected": False,
            "mapped_surface_built": False,
            "missing_component_repaired": False,
            "candidate_promoted": False,
            "advisory_ranking_binding": False,
            "first_ranked_surface_must_be_next": False,
            "human_authority_consumed": False,
            "micro_sweeps_authorized": False,
            "local_revision_authorized": False,
            "portability_demonstrated": False,
            "vs0_generalized": False,
            "performance_optimization_begun": False,
            "scale_optimization_begun": False,
            "vs1_6_executed": False,
            "phase_closure_claimed": False,
            "post_vs1_phase_selected": False,
        },
        "evidence_yield": {
            "yield_branch": "CONFIRMATION_YIELD",
            "confirmation_yield_reason": (
                "typed VS1.4 readiness blockers were converted into bounded "
                "candidate surface records with non-binding ranking and no build, "
                "repair, promotion, selection, execution, or authority consumption"
            ),
            "diagnostic_yield_available_on_mapping_failure": True,
        },
        "map_verdict": MAP_VERDICT,
        "terminal_transition": {
            "transition": ARTIFACT_TRANSITION,
            "executes_vs1_6": False,
            "authorizes_selected_surface_build": False,
            "authorizes_loop_execution": False,
            "authorizes_runner": False,
            "selects_post_vs1_phase": False,
        },
        "failures": [],
    }


def markdown_contains_vs1_5_overclaim(md_text: str) -> list[str]:
    hits: list[str] = []
    allowed_patterns = [
        r"\bloop ready\s*[:=]\s*false\b",
        r"\bloop may execute\s*[:=]\s*false\b",
        r"\brunner exists\s*[:=]\s*false\b",
        r"\brunner readiness exists\s*[:=]\s*false\b",
        r"\brunner authority exists\s*[:=]\s*false\b",
        r"\bmapped surface selected\s*[:=]\s*false\b",
        r"\bmapped surface built\s*[:=]\s*false\b",
        r"\bmissing component repaired\s*[:=]\s*false\b",
        r"\bcandidate promoted\s*[:=]\s*false\b",
        r"\badvisory ranking binding\s*[:=]\s*false\b",
        r"\bfirst ranked surface must be next\s*[:=]\s*false\b",
        r"\bhuman authority consumed\s*[:=]\s*false\b",
        r"\bmicro-sweeps authorized\s*[:=]\s*false\b",
        r"\blocal revision authorized\s*[:=]\s*false\b",
        r"\bportability demonstrated\s*[:=]\s*false\b",
        r"\bvs0 generalized\s*[:=]\s*false\b",
        r"\bperformance optimization begun\s*[:=]\s*false\b",
        r"\bscale optimization begun\s*[:=]\s*false\b",
        r"\bvs1\.6 executed\s*[:=]\s*false\b",
        r"\bvs1\.6 built\s*[:=]\s*false\b",
        r"\bvs1\.6 run\s*[:=]\s*false\b",
        r"\bvs1\.6 may select post-vs1 phase\s*[:=]\s*false\b",
        r"\bvs1\.6 may authorize surface build\s*[:=]\s*false\b",
        r"\bvs1\.6 may authorize loop execution\s*[:=]\s*false\b",
        r"\bsurface artifacts created by vs1\.5\s*[:=]\s*false\b",
        r"\bsurface build authorized by vs1\.5\s*[:=]\s*false\b",
        r"\bsurfaces selected by vs1\.5\s*[:=]\s*false\b",
        r"\branking is binding\s*[:=]\s*false\b",
        r"\branking selects next phase\s*[:=]\s*false\b",
        r"\branking authorizes build\s*[:=]\s*false\b",
        r"\branking authorizes repair\s*[:=]\s*false\b",
        r"\branking authorizes execution\s*[:=]\s*false\b",
        r"\badvisory first surface is selected next phase\s*[:=]\s*false\b",
        r"\bs21 ranked before unresolved required blockers\s*[:=]\s*false\b",
        r"\bs21 executed by vs1\.5\s*[:=]\s*false\b",
        r"\bdoes not .*select\b",
        r"\bdoes not .*authorize\b",
        r"\bdoes not .*build\b",
        r"\bdoes not .*repair\b",
        r"\bdoes not .*promote\b",
        r"\bdoes not .*execute\b",
    ]
    forbidden_patterns = {
        "loop ready": r"\bloop ready\b",
        "loop may execute": r"\bloop may execute\b",
        "runner exists": r"\brunner exists\b",
        "runner ready": r"\brunner ready\b",
        "runner authority exists": r"\brunner authority exists\b",
        "mapped surface selected": r"\bmapped surface selected\b",
        "mapped surface built": r"\bmapped surface built\b",
        "missing component repaired": r"\bmissing component repaired\b",
        "candidate promoted": r"\bcandidate promoted\b",
        "advisory ranking binding": r"\badvisory ranking binding\b",
        "first ranked surface must be next": r"\bfirst ranked surface must be next\b",
        "human authority consumed": r"\bhuman authority consumed\b",
        "micro-sweeps authorized": r"\bmicro-sweeps authorized\b",
        "local revision authorized": r"\blocal revision authorized\b",
        "portability demonstrated": r"\bportability demonstrated\b",
        "VS0 generalized": r"\bvs0 generalized\b",
        "performance optimization begun": r"\bperformance optimization begun\b",
        "scale optimization begun": r"\bscale optimization begun\b",
        "VS1.6 executed": r"\bvs1\.6 executed\b",
        "phase closed": r"\bphase closed\b",
        "post-VS1 phase selected": r"\bpost-vs1 phase selected\b",
    }
    for lineno, raw_line in enumerate(md_text.splitlines(), start=1):
        line = raw_line.strip().lower()
        if not line:
            continue
        if any(re.search(pattern, line) for pattern in allowed_patterns):
            continue
        for label, pattern in forbidden_patterns.items():
            if re.search(pattern, line):
                hits.append(f"line {lineno}: {label}: {raw_line}")
    return hits


def build_markdown(surface_map: dict[str, Any]) -> str:
    layer_lines = []
    for layer in surface_map["dependency_layers"]:
        layer_lines.append(
            f"- Layer {layer['layer']} {layer['layer_name']}: "
            + ", ".join(layer["surface_ids"])
        )
    candidate_lines = []
    for candidate in surface_map["surface_candidates"]:
        candidate_lines.append(
            f"- {candidate['surface_id']} | type: {candidate['surface_type']} | "
            f"status: {candidate['surface_status']} | "
            f"dependency layer: {candidate['dependency_layer']} | "
            f"rank: {candidate['rank']} | "
            f"component ids addressed: {', '.join(candidate['component_ids_addressed'])} | "
            f"required authority: {candidate['required_authority']} | "
            f"forbidden effects: {', '.join(candidate['forbidden_effects'])}"
        )
    return f"""# Phase VS1.5 missing precondition next-surface map v0

## Status

{MAP_VERDICT}

## Source readiness audit

- source readiness audit: phase_vs1_controlled_loop_readiness_audit_v0
- source readiness audit commit: {EXPECTED_HEAD}
- required source readiness audit gate: {SOURCE_READINESS_AUDIT_GATE}
- source role: TYPED_READINESS_RESULT_SOURCE

## Mapping branch

- mapping branch: NOT_READY_BLOCKER_MAP
- ready branch surface included: false

## Mapping policy

- maps typed readiness results only: true
- repairs allowed: false
- component build allowed: false
- candidate promotion allowed: false
- loop execution authorized: false
- runner created: false
- next phase auto-selected: false
- authority consumed: false

## Blocker coverage

- source blocker count: 20
- mapped blocker count: 20
- unmapped blocker count: 0
- all typed blockers mapped: true

## Surface candidate semantics

- surface candidate records created by VS1.5: true
- surface artifacts created by VS1.5: false
- surface build authorized by VS1.5: false
- surfaces selected by VS1.5: false

## Dependency layers

{chr(10).join(layer_lines)}

## Surface candidates

{chr(10).join(candidate_lines)}

## Advisory ranking

- ranking enabled: true
- ranking is binding: false
- ranking affects candidate validity: false
- ranking selects next phase: false
- ranking authorizes build: false
- ranking authorizes repair: false
- ranking authorizes execution: false
- advisory first surface candidate: S10_SOURCE_IDENTITY_FRESHNESS_POLICY_SURFACE
- advisory first surface is selected next phase: false

## Readiness re-audit boundary

- S21 candidate allowed: true
- S21 requires prior blocker-resolution evidence: true
- S21 ranked before unresolved required blockers: false
- S21 executed by VS1.5: false

## VS1.6 boundary

- VS1.6 may close Phase VS1 from map: true
- VS1.6 may select post-VS1 phase: false
- VS1.6 may authorize surface build: false
- VS1.6 may authorize loop execution: false
- VS1.6 built: false
- VS1.6 run: false

## Non-claims

- loop ready: false
- loop may execute: false
- runner exists: false
- runner readiness exists: false
- runner authority exists: false
- mapped surface selected: false
- mapped surface built: false
- missing component repaired: false
- candidate promoted: false
- advisory ranking binding: false
- first ranked surface must be next: false
- human authority consumed: false
- micro-sweeps authorized: false
- local revision authorized: false
- portability demonstrated: false
- VS0 generalized: false
- performance optimization begun: false
- scale optimization begun: false
- VS1.6 executed: false

## Evidence Yield

- yield branch: CONFIRMATION_YIELD
- Diagnostic Yield available on mapping failure: true

## Terminal transition

{ARTIFACT_TRANSITION}

## Boundary statement

VS1.5 maps typed VS1.4 readiness blockers into bounded candidate surface records. It creates a map artifact, not the mapped surface artifacts. Advisory ranking is non-binding and cannot select, authorize, build, repair, promote, or execute anything. VS1.5 does not close the phase, execute VS1.6, consume authority, create a runner, run micro-sweeps, or authorize loop execution.
"""


def validate_surface_map(surface_map: dict[str, Any], md: str) -> None:
    checks = {
        "schema_version": SCHEMA_VERSION,
        "artifact_id": ARTIFACT_ID,
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "unit_role": UNIT_ROLE,
        "mapping_branch": "NOT_READY_BLOCKER_MAP",
        "map_verdict": MAP_VERDICT,
    }
    for key, expected in checks.items():
        if surface_map.get(key) != expected:
            fail(
                "STOP_VS1_5_SURFACE_FIELD_INVALID",
                field=key,
                expected=expected,
                actual=surface_map.get(key),
            )
    candidates = surface_map.get("surface_candidates")
    if not isinstance(candidates, list) or [c.get("surface_id") for c in candidates] != EXPECTED_SURFACES:
        fail(
            "STOP_VS1_5_SURFACE_FIELD_INVALID",
            field="surface_candidates",
            expected=EXPECTED_SURFACES,
            actual=[c.get("surface_id") for c in candidates] if isinstance(candidates, list) else candidates,
        )
    for candidate in candidates:
        surface_id = candidate["surface_id"]
        if candidate.get("rank") in PLACEHOLDER_VALUES or not isinstance(candidate.get("rank"), int):
            fail(
                "STOP_VS1_5_SURFACE_FIELD_INVALID",
                surface=surface_id,
                field="rank",
                expected="integer",
                actual=candidate.get("rank"),
            )
        for key in [
            "may_be_selected_by_human",
            "surface_candidate_record_created_by_vs1_5",
        ]:
            if candidate.get(key) is not True:
                fail(
                    "STOP_VS1_5_SURFACE_FIELD_INVALID",
                    surface=surface_id,
                    field=key,
                    expected=True,
                    actual=candidate.get(key),
                )
        for key in [
            "machine_selected",
            "surface_artifact_created_by_vs1_5",
            "surface_build_authorized_by_vs1_5",
            "surface_selected_by_vs1_5",
        ]:
            if candidate.get(key) is not False:
                fail(
                    "STOP_VS1_5_SURFACE_FIELD_INVALID",
                    surface=surface_id,
                    field=key,
                    expected=False,
                    actual=candidate.get(key),
                )
        for effect in FORBIDDEN_EFFECTS:
            if effect not in candidate.get("forbidden_effects", []):
                fail(
                    "STOP_VS1_5_SURFACE_FIELD_INVALID",
                    surface=surface_id,
                    field="forbidden_effects",
                    expected=effect,
                    actual=candidate.get("forbidden_effects"),
                )
    if markdown_contains_vs1_5_overclaim(md):
        fail(
            "STOP_VS1_5_MARKDOWN_OVERCLAIM",
            source=OUTPUT_MD,
            field="markdown_overclaim_guard",
            expected=[],
            actual=markdown_contains_vs1_5_overclaim(md),
        )


def emit_success_readout() -> None:
    print("BUILD_PHASE_VS1_MISSING_PRECONDITION_NEXT_SURFACE_MAP_V0_COMPLETE")
    print(f"artifact_id={ARTIFACT_ID}")
    print(f"schema_version={SCHEMA_VERSION}")
    print(f"phase_id={PHASE_ID}")
    print(f"unit_id={UNIT_ID}")
    print(f"unit_role={UNIT_ROLE}")
    print(f"source_readiness_audit_commit_sha={EXPECTED_HEAD}")
    print(f"source_readiness_audit_required_gate={SOURCE_READINESS_AUDIT_GATE}")
    print(f"source_readiness_audit_required_transition={SOURCE_READINESS_TRANSITION}")
    print("mapping_branch=NOT_READY_BLOCKER_MAP")
    print("ready_branch_surface_included=false")
    print("source_blocker_count=20")
    print("mapped_blocker_count=20")
    print("unmapped_blocker_count=0")
    print("all_typed_blockers_mapped=true")
    print("surface_candidate_record_count=21")
    print("surface_candidate_records_created_by_vs1_5=true")
    print("surface_artifacts_created_by_vs1_5=false")
    print("surface_build_authorized_by_vs1_5=false")
    print("surfaces_selected_by_vs1_5=false")
    print("dependency_layers_declared=true")
    print("advisory_ranking_enabled=true")
    print("advisory_ranking_is_binding=false")
    print("ranking_affects_candidate_validity=false")
    print("ranking_selects_next_phase=false")
    print("ranking_authorizes_build=false")
    print("ranking_authorizes_repair=false")
    print("ranking_authorizes_execution=false")
    print("advisory_first_surface_candidate=S10_SOURCE_IDENTITY_FRESHNESS_POLICY_SURFACE")
    print("advisory_first_surface_selected_next_phase=false")
    print("machine_selected_next_phase=false")
    print("s21_candidate_allowed=true")
    print("s21_requires_prior_blocker_resolution_evidence=true")
    print("s21_ranked_before_unresolved_required_blockers=false")
    print("s21_executed_by_vs1_5=false")
    print("vs1_6_may_close_phase_vs1_from_map=true")
    print("vs1_6_may_select_post_vs1_phase=false")
    print("vs1_6_may_authorize_surface_build=false")
    print("vs1_6_may_authorize_loop_execution=false")
    print("vs1_6_built=false")
    print("vs1_6_run=false")
    print("repair_attempted=false")
    print("component_build_attempted=false")
    print("candidate_promotion_attempted=false")
    print("human_authority_consumed=false")
    print("loop_execution_authorized=false")
    print("runner_created=false")
    print("micro_sweeps_authorized=false")
    print("local_revision_authorized=false")
    print("phase_closure_claimed=false")
    print("post_vs1_phase_selected=false")
    print("source_readiness_audit_mutated_by_vs1_5=false")
    print("source_inventory_mutated_by_vs1_5=false")
    print("source_contract_mutated_by_vs1_5=false")
    print("vs1_1_source_intake_mutated_by_vs1_5=false")
    print("post_vs0_direction_decision_receipt_mutated_by_vs1_5=false")
    print("vs0_source_artifacts_mutated_by_vs1_5=false")
    print("evidence_yield_branch=CONFIRMATION_YIELD")
    print("diagnostic_yield_available_on_mapping_failure=true")
    print(f"map_verdict={MAP_VERDICT}")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition={PRINT_TRANSITION}")


def emit_typed_stop(exc: MapFailure) -> None:
    print("BUILD_PHASE_VS1_MISSING_PRECONDITION_NEXT_SURFACE_MAP_V0_TYPED_STOP")
    print(f"artifact_id={ARTIFACT_ID}")
    print(f"phase_id={PHASE_ID}")
    print(f"unit_id={UNIT_ID}")
    print(f"map_verdict={exc.code}")
    print("yield_branch=DIAGNOSTIC_YIELD")
    print(f"missing_or_invalid_source={exc.source}")
    print(f"unmapped_blocker={exc.blocker}")
    print(f"violating_surface={exc.surface}")
    print(f"violating_field={exc.field}")
    print(f"expected_value={exc.expected}")
    print(f"actual_value={exc.actual}")
    print(f"next_lawful_surface={exc.next_surface}")
    print("self_repair_performed=false")
    print("loop_execution_authorized=false")
    print("runner_created=false")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition=STOP({exc.code})")


def generate() -> int:
    root = detect_repo_root(Path.cwd())
    require_head(root)
    validate_dirty_scope(root)
    ensure_no_forbidden_artifacts(root)
    for rel_path in [
        SOURCE_READINESS_AUDIT_JSON,
        SOURCE_READINESS_AUDIT_MD,
        SOURCE_INVENTORY_JSON,
        SOURCE_INVENTORY_MD,
        SOURCE_CONTRACT_JSON,
        SOURCE_CONTRACT_MD,
        SOURCE_INTAKE_JSON,
        SOURCE_INTAKE_MD,
        DIRECTION_JSON,
        DIRECTION_MD,
    ]:
        require_file(root, rel_path)
    audit = load_json(root, SOURCE_READINESS_AUDIT_JSON)
    load_json(root, SOURCE_INVENTORY_JSON)
    load_json(root, SOURCE_CONTRACT_JSON)
    load_json(root, SOURCE_INTAKE_JSON)
    load_json(root, DIRECTION_JSON)
    validate_source_audit(audit)
    before_hashes = capture_source_hashes(root)
    surface_map = build_surface_map(root, audit)
    md = build_markdown(surface_map)
    validate_surface_map(surface_map, md)
    output_json = root / OUTPUT_JSON
    output_md = root / OUTPUT_MD
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(surface_map, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    output_md.write_text(md, encoding="utf-8")
    after_hashes = capture_source_hashes(root)
    validate_source_preservation(before_hashes, after_hashes)
    validate_dirty_scope(root)
    ensure_no_forbidden_artifacts(root)
    emit_success_readout()
    return 0


def main() -> int:
    try:
        return generate()
    except MapFailure as exc:
        emit_typed_stop(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
