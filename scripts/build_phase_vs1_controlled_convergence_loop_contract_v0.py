#!/usr/bin/env python3

"""Build VS1.2 Minimal Controlled Convergence Loop contract definition."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT = "scripts/build_phase_vs1_controlled_convergence_loop_contract_v0.py"
EXPECTED_HEAD = "8f4b57c697d8dc7110e3ea9d73183d36c806a66c"
OUTPUT_JSON = (
    "docs/matrixlabs/phase_vs1/"
    "phase_vs1_controlled_convergence_loop_contract_v0.json"
)
OUTPUT_MD = (
    "docs/matrixlabs/phase_vs1/"
    "phase_vs1_controlled_convergence_loop_contract_v0.md"
)

SOURCE_INTAKE_JSON = (
    "docs/matrixlabs/phase_vs1/phase_vs1_post_vs0_source_intake_v0.json"
)
SOURCE_INTAKE_MD = (
    "docs/matrixlabs/phase_vs1/phase_vs1_post_vs0_source_intake_v0.md"
)
DIRECTION_JSON = "docs/matrixlabs/phase_vs1/post_vs0_direction_decision_receipt_v0.json"
DIRECTION_MD = "docs/matrixlabs/phase_vs1/post_vs0_direction_decision_receipt_v0.md"
VS0_CLOSURE_JSON = "docs/matrixlabs/phase_vs0/phase_vs0_closure_v0.json"
VS0_CLOSURE_MD = "docs/matrixlabs/phase_vs0/phase_vs0_closure_v0.md"
VS0_ROOT = "docs/matrixlabs/phase_vs0"

SCHEMA_VERSION = "matrixlabs_phase_vs1_controlled_convergence_loop_contract_v0"
ARTIFACT_ID = "phase_vs1_controlled_convergence_loop_contract_v0"
PHASE_ID = "PHASE_VS1"
UNIT_ID = "VS1.2_CONTROLLED_CONVERGENCE_LOOP_CONTRACT_DEFINITION"
UNIT_ROLE = "CONTRACT_DEFINITION_ONLY"

SOURCE_INTAKE_STATUS = "VS1_1_POST_VS0_SOURCE_INTAKE_PASS"
SOURCE_INTAKE_TRANSITION = (
    "ADVANCE(VS1_2_CONTROLLED_LOOP_CONTRACT_DEFINITION_PENDING)"
)
PASS_VERDICT = "VS1_2_CONTROLLED_LOOP_CONTRACT_DEFINITION_PASS"
ARTIFACT_TRANSITION = (
    "ADVANCE(VS1_3_CONTROLLED_LOOP_PRECONDITION_INVENTORY_PENDING)"
)
PRINT_TRANSITION = (
    "ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS1_CONTROLLED_CONVERGENCE_LOOP_"
    "CONTRACT_V0_PENDING)"
)

LOOP_NAME = "MINIMAL_CONTROLLED_CONVERGENCE_LOOP"
SHORT_NAME = "MCCL"
CONTRACT_STATUS = "DEFINED_NOT_AUTHORIZED"
LOOP_DEFINITION = (
    "A Minimal Controlled Convergence Loop is a bounded, receipt-producing loop "
    "shape that may, if later authorized and found ready, load a declared typed "
    "state inside a declared scope/regime, select lawful moves from an explicit "
    "move-space, apply moves under authority/radius/halt rules, emit receipts, "
    "expose pressure through bounded micro-sweeps across declared variations, "
    "classify what held or failed, permit only separately authorized local "
    "revision proposals, record bounded portability conditions, and repeat or "
    "halt under an explicit repeat/halt policy."
)
CONVERGENCE_DEFINITION = (
    "bounded progression toward a declared local terminal condition, typed halt, "
    "or decision surface under explicit radius, receipt, pressure, and authority "
    "rules"
)

FORBIDDEN_ARTIFACTS = [
    "docs/matrixlabs/runner",
    "docs/matrixlabs/runtime",
    "docs/matrixlabs/move_space",
    "docs/matrixlabs/micro_sweeps",
    (
        "docs/matrixlabs/phase_vs1/"
        "phase_vs1_controlled_loop_precondition_inventory_v0.json"
    ),
    (
        "docs/matrixlabs/phase_vs1/"
        "phase_vs1_controlled_loop_precondition_inventory_v0.md"
    ),
    (
        "docs/matrixlabs/phase_vs1/"
        "phase_vs1_controlled_loop_readiness_certificate_v0.json"
    ),
]

MINIMUM_CONVERGENCE_CRITERION_FIELDS = [
    "local_terminal_condition",
    "allowed_repeat_condition",
    "non_progress_condition",
    "oscillation_or_repeated_state_guard",
    "max_cycle_or_radius_boundary",
    "evidence_required_to_continue",
    "typed_halt_when_not_met",
]

LOOP_STAGES: list[dict[str, Any]] = [
    {
        "stage_id": "L0_SCOPE_REGIME_DECLARATION",
        "stage_name": "Scope / Regime Declaration",
        "stage_role": "defines local scope and allowed regime movement",
        "required_fields": [
            "scope_id",
            "regime_id",
            "allowed_source_surfaces",
            "forbidden_source_surfaces",
            "allowed_regime_transitions",
            "forbidden_regime_transitions",
            "object_identity_rules",
            "sameness_difference_criteria",
            "authority_boundary",
            "claim_boundary",
        ],
        "contract_requirement": (
            "A controlled loop cannot begin without knowing which regime it is "
            "operating inside and what regime movement is allowed."
        ),
        "missing_stop": "STOP_CONTROLLED_LOOP_SCOPE_REGIME_CONTRACT_MISSING",
        "executable_in_vs1_2": False,
    },
    {
        "stage_id": "L1_STATE_INTAKE",
        "stage_name": "State Intake",
        "stage_role": "defines the required starting typed state object",
        "required_fields": [
            "state_id",
            "source_artifacts",
            "authority_state",
            "current_loop_position",
            "available_move_references",
            "radius_budget_state",
            "prior_receipts",
            "known_forbidden_effects",
            "current_halt_condition_if_any",
        ],
        "contract_requirement": (
            "A controlled loop cannot begin without a typed state object."
        ),
        "missing_stop": "STOP_CONTROLLED_LOOP_STATE_OBJECT_MISSING",
        "executable_in_vs1_2": False,
    },
    {
        "stage_id": "L2_MOVE_SPACE_ADMISSION",
        "stage_name": "Move-Space Admission",
        "stage_role": "defines the explicit set of moves the loop may consider",
        "required_fields": [
            "move_id",
            "move_kind",
            "input_shape",
            "output_shape",
            "authority_requirement",
            "radius_cost",
            "receipt_obligation",
            "halt_conditions",
            "forbidden_effects",
            "source_freshness_requirements",
        ],
        "contract_requirement": (
            "No implicit move-space. No inferred moves. No latest-object guessing."
        ),
        "missing_stop": "STOP_CONTROLLED_LOOP_MOVE_SPACE_MISSING",
        "executable_in_vs1_2": False,
    },
    {
        "stage_id": "L3_MOVE_SELECTION",
        "stage_name": "Move Selection",
        "stage_role": "defines the rule by which one move may be selected",
        "required_fields": [
            "deterministic_or_seeded_stochastic_rule",
            "bounded_selection_scope",
            "source_awareness",
            "authority_awareness",
            "radius_awareness",
            "halt_awareness",
            "receipt_awareness",
        ],
        "forbidden_selector_behavior": [
            "select_by_vibes",
            "select_by_newest_file",
            "select_by_human_looking_importance",
            "select_by_unstated_priority",
            "select_forbidden_repair",
            "select_next_phase_automatically",
        ],
        "contract_requirement": (
            "Move selection must be bounded, source-aware, authority-aware, "
            "radius-aware, halt-aware, and receipt-aware."
        ),
        "missing_stop": "STOP_CONTROLLED_LOOP_MOVE_SELECTOR_MISSING",
        "executable_in_vs1_2": False,
    },
    {
        "stage_id": "L4_MOVE_APPLICATION_CONTRACT",
        "stage_name": "Move Application Contract",
        "stage_role": "defines how an admitted move would be applied if later authorized",
        "required_fields": [
            "input_object",
            "move_object",
            "authority_source",
            "precondition_checks",
            "state_transition_rule",
            "output_object",
            "receipt_obligation",
            "failure_behavior",
            "rollback_or_no_mutation_boundary",
        ],
        "contract_requirement": (
            "Move application must produce either a typed output or a typed stop."
        ),
        "missing_stop": "STOP_CONTROLLED_LOOP_MOVE_APPLICATOR_MISSING",
        "executable_in_vs1_2": False,
    },
    {
        "stage_id": "L5_RECEIPT_EMISSION",
        "stage_name": "Receipt Emission",
        "stage_role": "defines the minimum receipt obligation for every attempted move",
        "required_fields": [
            "attempted_move",
            "source_state",
            "authority_basis",
            "radius_before",
            "radius_consumed",
            "radius_after",
            "preconditions_checked",
            "output_or_stop",
            "forbidden_effects_checked",
            "next_lawful_surface",
            "self_repair_flag",
        ],
        "contract_requirement": "No receipt, no loop step.",
        "missing_stop": "STOP_CONTROLLED_LOOP_RECEIPT_CONTRACT_MISSING",
        "executable_in_vs1_2": False,
    },
    {
        "stage_id": "L6_MICRO_SWEEP_BOUNDS_CONTRACT",
        "stage_name": "Micro-Sweep Bounds Contract",
        "stage_role": (
            "defines bounded repeated executions over declared variations if "
            "later authorized"
        ),
        "required_fields": [
            "sweep_id",
            "sweep_purpose",
            "variation_set",
            "max_cases",
            "max_steps",
            "radius_budget",
            "allowed_moves",
            "stop_conditions",
            "receipt_aggregation",
            "forbidden_inference_boundary",
        ],
        "contract_requirement": (
            "Micro-sweeps expose pressure. They do not optimize goals by default. "
            "They do not create generalization by repetition. They are not "
            "authorized by VS1.2."
        ),
        "missing_stop": "STOP_CONTROLLED_LOOP_MICRO_SWEEP_BOUNDS_MISSING",
        "executable_in_vs1_2": False,
    },
    {
        "stage_id": "L7_PRESSURE_READOUT",
        "stage_name": "Pressure Readout",
        "stage_role": (
            "defines readout shape for signals produced by future authorized "
            "execution or halted execution"
        ),
        "required_fields": [
            "what_held",
            "what_failed",
            "what_stopped",
            "what_was_missing",
            "what_boundary_was_hit",
            "what_became_ambiguous",
            "what_cost_or_burden_appeared",
            "what_source_became_stale",
            "what_next_surface_was_exposed",
        ],
        "contract_requirement": "Pressure readout precedes pressure classification.",
        "missing_stop": "STOP_CONTROLLED_LOOP_PRESSURE_READOUT_MISSING",
        "executable_in_vs1_2": False,
    },
    {
        "stage_id": "L8_PRESSURE_CLASSIFICATION",
        "stage_name": "Pressure Classification",
        "stage_role": "defines classification of pressure into typed families",
        "required_fields": [
            "classification_vocabulary",
            "classification_basis",
            "source_reference",
            "next_surface",
        ],
        "contract_requirement": (
            "Pressure must be classified before revision is proposed."
        ),
        "missing_stop": "STOP_CONTROLLED_LOOP_PRESSURE_CLASSIFIER_MISSING",
        "executable_in_vs1_2": False,
    },
    {
        "stage_id": "L9_LOCAL_REVISION_SURFACE",
        "stage_name": "Local Revision Surface",
        "stage_role": "defines the lawful surface where local revision may be proposed",
        "required_fields": [
            "revision_target",
            "revision_basis",
            "authority_requirement",
            "proposal_only_flag",
            "application_authority",
        ],
        "allowed_revision_targets": [
            "language",
            "schema",
            "move_space",
            "boundary_vocabulary",
            "receipt_obligation",
            "halt_vocabulary",
            "pressure_classification",
            "portability_map_schema",
        ],
        "contract_requirement": (
            "Pressure may justify a proposed local revision. Pressure does not "
            "self-authorize revision."
        ),
        "missing_stop": "STOP_CONTROLLED_LOOP_LOCAL_REVISION_SURFACE_MISSING",
        "executable_in_vs1_2": False,
    },
    {
        "stage_id": "L10_BOUNDED_PORTABILITY_MAPPING",
        "stage_name": "Bounded Portability Mapping",
        "stage_role": "defines how the loop records whether a shape carried across cases",
        "required_fields": [
            "source_case",
            "target_case",
            "declared_transport_or_adaptation",
            "what_remained_stable",
            "what_changed",
            "what_failed",
            "what_required_local_revision",
            "what_remains_untested",
            "claim_boundary",
            "receipt_references",
        ],
        "allowed_claim_shape": [
            "tested_under_X",
            "failed_under_Y",
            "adapted_under_Z",
            "untested_under_W",
        ],
        "forbidden_claim": "this_generalizes_globally",
        "contract_requirement": (
            "Portability is receipt-backed and condition-indexed."
        ),
        "missing_stop": "STOP_CONTROLLED_LOOP_PORTABILITY_MAP_MISSING",
        "executable_in_vs1_2": False,
    },
    {
        "stage_id": "L11_REPEAT_OR_HALT_DECISION",
        "stage_name": "Repeat / Halt Decision",
        "stage_role": (
            "defines how the loop decides whether another bounded cycle may occur"
        ),
        "required_fields": ["repeat_requires", "halt_requires"],
        "repeat_requires": [
            "remaining_radius",
            "allowed_move",
            "valid_state",
            "no_unresolved_hard_stop",
            "receipt_from_prior_step",
            "no_forbidden_effect_leak",
            "explicit_repeat_policy",
            "declared_convergence_criterion_not_yet_met",
        ],
        "halt_requires": [
            "typed_halt_code",
            "reason",
            "state_snapshot",
            "next_lawful_surface",
            "self_repair_false_unless_explicitly_authorized",
        ],
        "contract_requirement": (
            "Repeat is a controlled transition. It is not ambient continuation."
        ),
        "missing_stop": "STOP_CONTROLLED_LOOP_REPEAT_HALT_POLICY_MISSING",
        "executable_in_vs1_2": False,
    },
]

PRESSURE_CLASSIFICATION_VOCABULARY = [
    "MISSING_OBJECT",
    "MISSING_FIELD",
    "AUTHORITY_ABSENT",
    "AUTHORITY_DRIFT",
    "BOUNDARY_VIOLATION",
    "RADIUS_EXHAUSTED",
    "SOURCE_STALE_OR_UNKNOWN",
    "MOVE_SPACE_GAP",
    "RECEIPT_OBLIGATION_GAP",
    "HALT_POLICY_GAP",
    "PRESSURE_READOUT_GAP",
    "LANGUAGE_AMBIGUITY",
    "LOCAL_REVISION_REQUIRED",
    "PORTABILITY_BOUNDARY_HIT",
    "BURDEN_SIGNAL",
    "UNEXPECTED_SUCCESS",
    "AMBIGUOUS_STOP",
]

REQUIRED_COMPONENTS = [
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

ALLOWED_FUTURE_INVENTORY_QUESTIONS = [
    "Is the component present?",
    "Is the component missing?",
    "Is the component candidate-only?",
    "Is the component insufficient?",
    "Does the component require authority?",
    "Does the component require promotion?",
    "Does the component require a schema?",
    "Is the component out of scope?",
    "Which exact next surface would be lawful if the component is missing or blocked?",
]

FORBIDDEN_FUTURE_INVENTORY_QUESTIONS = [
    "Can we run the loop now without completing the inventory?",
    "Can we execute a micro-sweep?",
    "Can we apply a local revision?",
    "Can we activate a runner?",
    "Can we infer portability from VS0?",
    "Can we promote a candidate because it appears useful?",
    "Can we generalize from one specimen?",
]


class ContractFailure(RuntimeError):
    def __init__(
        self,
        code: str,
        *,
        section: str = "NONE",
        field: str = "NONE",
        expected: object = "NONE",
        actual: object = "NONE",
        next_surface: str = "REPAIR_VS1_2_CONTRACT_DEFINITION_INPUT",
    ) -> None:
        super().__init__(code)
        self.code = code
        self.section = section
        self.field = field
        self.expected = expected
        self.actual = actual
        self.next_surface = next_surface


def fail(
    code: str,
    *,
    section: str = "NONE",
    field: str = "NONE",
    expected: object = "NONE",
    actual: object = "NONE",
    next_surface: str = "REPAIR_VS1_2_CONTRACT_DEFINITION_INPUT",
) -> None:
    raise ContractFailure(
        code,
        section=section,
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
            "STOP_VS1_2_POST_VS0_SOURCE_INTAKE_NOT_PASS",
            section="git",
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
            "STOP_VS1_2_POST_VS0_SOURCE_INTAKE_NOT_PASS",
            section="repo",
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
    status = run_git(root, ["status", "--short", "--untracked-files=all"])
    for line in status.splitlines():
        path = status_path(line)
        if path in allowed_exact or any(path.startswith(p) for p in allowed_prefixes):
            continue
        if path in {SOURCE_INTAKE_JSON, SOURCE_INTAKE_MD}:
            fail(
                "STOP_VS1_2_SOURCE_INTAKE_MUTATED",
                section="dirty_scope",
                field=path,
                expected="unchanged source intake",
                actual=line,
            )
        if path in {DIRECTION_JSON, DIRECTION_MD}:
            fail(
                "STOP_VS1_2_DIRECTION_RECEIPT_MUTATED",
                section="dirty_scope",
                field=path,
                expected="unchanged direction receipt",
                actual=line,
            )
        if path in {VS0_CLOSURE_JSON, VS0_CLOSURE_MD}:
            fail(
                "STOP_VS1_2_VS0_CLOSURE_MUTATED",
                section="dirty_scope",
                field=path,
                expected="unchanged VS0.6 closure",
                actual=line,
            )
        if path.startswith(f"{VS0_ROOT}/"):
            fail(
                "STOP_VS1_2_VS0_SOURCE_MUTATED",
                section="dirty_scope",
                field=path,
                expected="unchanged VS0 source artifacts",
                actual=line,
            )
        fail(
            "STOP_VS1_2_POST_VS0_SOURCE_INTAKE_NOT_PASS",
            section="dirty_scope",
            field=path,
            expected="only VS1.2 outputs, baseline_share, or discussion_packets",
            actual=line,
        )


def require_head(root: Path) -> None:
    head = run_git(root, ["rev-parse", "HEAD"])
    if head != EXPECTED_HEAD:
        fail(
            "STOP_VS1_2_POST_VS0_SOURCE_INTAKE_NOT_PASS",
            section="source_intake",
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
            "STOP_VS1_2_POST_VS0_SOURCE_INTAKE_NOT_PASS",
            section="input_files",
            field=rel_path,
            expected="present JSON file",
            actual="missing",
        )
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(
            "STOP_VS1_2_POST_VS0_SOURCE_INTAKE_NOT_PASS",
            section="input_files",
            field=rel_path,
            expected="valid JSON object",
            actual=str(exc),
        )
    if not isinstance(value, dict):
        fail(
            "STOP_VS1_2_POST_VS0_SOURCE_INTAKE_NOT_PASS",
            section="input_files",
            field=rel_path,
            expected="JSON object",
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
    section: str,
    field: str,
) -> None:
    if value != expected:
        fail(
            code,
            section=section,
            field=field,
            expected=expected,
            actual=value,
        )


def require_file(root: Path, rel_path: str) -> None:
    if not (root / rel_path).is_file():
        fail(
            "STOP_VS1_2_POST_VS0_SOURCE_INTAKE_NOT_PASS",
            section="input_files",
            field=rel_path,
            expected="present source file",
            actual="missing",
        )


def source_paths(root: Path) -> list[str]:
    paths = [
        SOURCE_INTAKE_JSON,
        SOURCE_INTAKE_MD,
        DIRECTION_JSON,
        DIRECTION_MD,
        VS0_CLOSURE_JSON,
        VS0_CLOSURE_MD,
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
                "STOP_VS1_2_POST_VS0_SOURCE_INTAKE_NOT_PASS",
                section="source_preservation",
                field=rel_path,
                expected="present source artifact",
                actual="missing",
            )
        hashes[rel_path] = sha256(path)
    return hashes


def validate_source_preservation(
    before: dict[str, str],
    after: dict[str, str],
) -> None:
    if before == after:
        return
    changed = sorted(
        path
        for path in set(before) | set(after)
        if before.get(path) != after.get(path)
    )
    first = changed[0] if changed else "unknown"
    if first in {SOURCE_INTAKE_JSON, SOURCE_INTAKE_MD}:
        code = "STOP_VS1_2_SOURCE_INTAKE_MUTATED"
    elif first in {DIRECTION_JSON, DIRECTION_MD}:
        code = "STOP_VS1_2_DIRECTION_RECEIPT_MUTATED"
    elif first in {VS0_CLOSURE_JSON, VS0_CLOSURE_MD}:
        code = "STOP_VS1_2_VS0_CLOSURE_MUTATED"
    elif first.startswith(f"{VS0_ROOT}/"):
        code = "STOP_VS1_2_VS0_SOURCE_MUTATED"
    else:
        code = "STOP_VS1_2_POST_VS0_SOURCE_INTAKE_NOT_PASS"
    fail(
        code,
        section="source_preservation",
        field=first,
        expected=before.get(first),
        actual=after.get(first),
    )


def validate_source_intake(intake: dict[str, Any]) -> None:
    require_equal(
        intake.get("artifact_id"),
        "phase_vs1_post_vs0_source_intake_v0",
        "STOP_VS1_2_POST_VS0_SOURCE_INTAKE_NOT_PASS",
        "source_intake",
        "artifact_id",
    )
    require_equal(
        intake.get("intake_verdict"),
        SOURCE_INTAKE_STATUS,
        "STOP_VS1_2_POST_VS0_SOURCE_INTAKE_NOT_PASS",
        "source_intake",
        "intake_verdict",
    )
    require_equal(
        intake.get("terminal_transition"),
        SOURCE_INTAKE_TRANSITION,
        "STOP_VS1_2_POST_VS0_SOURCE_INTAKE_NOT_PASS",
        "source_intake",
        "terminal_transition",
    )
    require_equal(
        get_value(intake, "accepted_input_scope.may_feed_loop_execution"),
        False,
        "STOP_VS1_2_EXECUTION_AUTHORITY_CLAIMED",
        "source_intake",
        "accepted_input_scope.may_feed_loop_execution",
    )
    require_equal(
        get_value(intake, "accepted_input_scope.may_feed_vs1_2_contract_definition"),
        True,
        "STOP_VS1_2_POST_VS0_SOURCE_INTAKE_NOT_PASS",
        "source_intake",
        "accepted_input_scope.may_feed_vs1_2_contract_definition",
    )
    require_equal(
        get_value(intake, "vs1_2_boundary.vs1_2_contract_definition_may_start"),
        True,
        "STOP_VS1_2_POST_VS0_SOURCE_INTAKE_NOT_PASS",
        "source_intake",
        "vs1_2_boundary.vs1_2_contract_definition_may_start",
    )
    require_equal(
        get_value(intake, "vs1_2_boundary.vs1_2_contract_defined"),
        False,
        "STOP_VS1_2_POST_VS0_SOURCE_INTAKE_NOT_PASS",
        "source_intake",
        "vs1_2_boundary.vs1_2_contract_defined",
    )


def ensure_no_forbidden_artifacts(root: Path) -> None:
    for rel_path in FORBIDDEN_ARTIFACTS:
        if (root / rel_path).exists():
            fail(
                "STOP_VS1_2_FORBIDDEN_EXECUTION_ARTIFACT_CREATED",
                section="forbidden_artifacts",
                field=rel_path,
                expected="absent",
                actual="present",
            )


def markdown_contains_vs1_2_overclaim(md: str) -> list[str]:
    hits: list[str] = []
    allowed_patterns = [
        r"\bexecution authorized\s*[:=]\s*false\b",
        r"\brunner created\s*[:=]\s*false\b",
        r"\brunner authority created by source intake\s*[:=]\s*false\b",
        r"\bloop execution authorized by source intake\s*[:=]\s*false\b",
        r"\bmicro-sweeps authorized\s*[:=]\s*false\b",
        r"\blocal revision authorized\s*[:=]\s*false\b",
        r"\bportability claimed\s*[:=]\s*false\b",
        r"\bglobal generalization claimed\s*[:=]\s*false\b",
        r"\bperformance optimization claimed\s*[:=]\s*false\b",
        r"\bscale optimization claimed\s*[:=]\s*false\b",
        r"\boptimization claimed\s*[:=]\s*false\b",
        r"\bglobal convergence claimed\s*[:=]\s*false\b",
        r"\bsuccess guaranteed\s*[:=]\s*false\b",
        r"\bdomain metric supplied by vs1\.2\s*[:=]\s*false\b",
        r"\bcomponents inventoried\s*[:=]\s*false\b",
        r"\ball components present\s*[:=]\s*false\b",
        r"\bcomponent sufficiency checked\s*[:=]\s*false\b",
        r"\bcomponent authority checked\s*[:=]\s*false\b",
        r"\bcomponent missingness checked\s*[:=]\s*false\b",
        r"\bvs1\.3 may certify loop readiness\s*[:=]\s*false\b",
        r"\bvs1\.3 may execute loop\s*[:=]\s*false\b",
        r"\bvs1\.3 may authorize micro-sweeps\s*[:=]\s*false\b",
        r"\bvs1\.3 may apply revisions\s*[:=]\s*false\b",
        r"\bvs1\.3 may create runner\s*[:=]\s*false\b",
        r"\bcontract authorized for execution\s*[:=]\s*false\b",
        r"\bcontract readiness certified\s*[:=]\s*false\b",
        r"\bcontract component inventory complete\s*[:=]\s*false\b",
        r"\bcontract execution preconditions passed\s*[:=]\s*false\b",
        r"\bdoes not inventory component presence\b",
        r"\bdoes not .*certify readiness\b",
        r"\bdoes not .*authorize execution\b",
        r"\bdoes not .*create a runner\b",
        r"\bdoes not .*create move-space\b",
        r"\bdoes not .*run micro-sweeps\b",
        r"\bdoes not .*authorize local revision\b",
        r"\bdoes not .*demonstrate portability\b",
        r"\bdoes not .*generalize vs0\b",
        r"\bdoes not .*optimize performance\b",
        r"\bdoes not .*optimize scale\b",
        r"\bdoes not .*execute vs1\.3\b",
        r"\bcontract status\s*[:=]\s*defined_not_authorized\b",
        r"\bdefines .* contract only\b",
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
        "all components present": r"\ball components present\b",
        "component inventory complete": r"\bcomponent inventory complete\b",
        "loop readiness certified": r"\bloop readiness certified\b",
        "controlled loop preconditions passed": (
            r"\bcontrolled loop preconditions passed\b"
        ),
        "portability demonstrated": r"\bportability demonstrated\b",
        "VS0 generalized": r"\bvs0 generalized\b",
    }

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


def build_contract(root: Path, intake: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "artifact_id": ARTIFACT_ID,
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "unit_role": UNIT_ROLE,
        "source_intake": {
            "artifact_id": "phase_vs1_post_vs0_source_intake_v0",
            "path": SOURCE_INTAKE_JSON,
            "commit_sha": EXPECTED_HEAD,
            "sha256": sha256(root / SOURCE_INTAKE_JSON),
            "required_status": SOURCE_INTAKE_STATUS,
            "required_transition": SOURCE_INTAKE_TRANSITION,
            "source_role": "BOUNDED_LOCAL_VS0_EVIDENCE_ADMITTED_FOR_DEFINITION",
            "loop_execution_authorized_by_source_intake": False,
            "runner_authority_created_by_source_intake": False,
            "source_vs0_remains_bounded_local_evidence": True,
        },
        "loop_contract": {
            "loop_name": LOOP_NAME,
            "short_name": SHORT_NAME,
            "contract_status": CONTRACT_STATUS,
            "definition": LOOP_DEFINITION,
            "compact_shape": [
                "declared_scope_or_regime",
                "typed_state",
                "lawful_move",
                "receipt",
                "bounded_micro_sweep_contract",
                "pressure_readout",
                "pressure_classification",
                "local_revision_surface",
                "bounded_portability_map",
                "repeat_or_halt",
            ],
            "execution_authorized": False,
            "runner_created": False,
            "micro_sweeps_authorized": False,
            "local_revision_authorized": False,
            "portability_claimed": False,
            "global_generalization_claimed": False,
            "performance_optimization_claimed": False,
            "scale_optimization_claimed": False,
        },
        "convergence_meaning": {
            "definition": CONVERGENCE_DEFINITION,
            "optimization_claimed": False,
            "global_convergence_claimed": False,
            "success_guaranteed": False,
            "domain_metric_supplied_by_vs1_2": False,
            "convergence_criterion_required_before_execution": True,
            "minimum_convergence_criterion_fields": MINIMUM_CONVERGENCE_CRITERION_FIELDS,
            "missing_convergence_criterion_stop": (
                "STOP_CONTROLLED_LOOP_CONVERGENCE_CRITERION_MISSING"
            ),
        },
        "loop_stages": LOOP_STAGES,
        "pressure_classification_vocabulary": PRESSURE_CLASSIFICATION_VOCABULARY,
        "required_components": REQUIRED_COMPONENTS,
        "component_presence_claims": {
            "components_declared": True,
            "components_inventoried": False,
            "all_components_present": False,
            "component_sufficiency_checked": False,
            "component_authority_checked": False,
            "component_missingness_checked": False,
        },
        "future_inventory_target": {
            "next_unit": "phase_vs1_controlled_loop_precondition_inventory_v0",
            "next_unit_role": "INVENTORY_DECLARED_COMPONENTS",
            "executes_loop": False,
            "certifies_readiness": False,
            "authorizes_micro_sweeps": False,
        },
        "allowed_future_inventory_questions": ALLOWED_FUTURE_INVENTORY_QUESTIONS,
        "forbidden_future_inventory_questions": FORBIDDEN_FUTURE_INVENTORY_QUESTIONS,
        "vs1_3_boundary": {
            "vs1_3_may_inventory_declared_components": True,
            "vs1_3_may_certify_loop_readiness": False,
            "vs1_3_may_execute_loop": False,
            "vs1_3_may_authorize_micro_sweeps": False,
            "vs1_3_may_apply_revisions": False,
            "vs1_3_may_create_runner": False,
        },
        "contract_boundary": {
            "contract_defined": True,
            "contract_authorized_for_execution": False,
            "contract_readiness_certified": False,
            "contract_component_inventory_complete": False,
            "contract_execution_preconditions_passed": False,
        },
        "forbidden_execution_claims": {
            "controlled_loop_exists_as_executable": False,
            "controlled_loop_ready": False,
            "controlled_loop_authorized": False,
            "runner_exists": False,
            "runner_readiness_exists": False,
            "runner_authority_exists": False,
            "move_space_exists": False,
            "selector_exists": False,
            "applicator_exists": False,
            "micro_sweeps_authorized": False,
            "pressure_classification_operational": False,
            "local_revision_authorized": False,
            "next_unit_executed": False,
        },
        "forbidden_generalization_claims": {
            "portability_demonstrated": False,
            "vs0_generalized": False,
            "global_generalization_claimed": False,
            "performance_optimization_begun": False,
            "scale_optimization_begun": False,
            "total_coverage_claimed": False,
        },
        "evidence_yield": {
            "yield_branch": "CONFIRMATION_YIELD",
            "confirmation_yield_reason": (
                "controlled loop contract was defined with bounded convergence "
                "meaning, declared stages, required component list, future "
                "inventory target, and preserved non-execution boundaries"
            ),
            "diagnostic_yield_available_on_typed_stop": True,
        },
        "source_preservation": {
            "vs1_1_source_intake_mutated_by_vs1_2": False,
            "post_vs0_direction_decision_receipt_mutated_by_vs1_2": False,
            "vs0_6_phase_closure_mutated_by_vs1_2": False,
            "vs0_source_artifacts_mutated_by_vs1_2": False,
        },
        "receipt_obligations": {
            "unit_id_emitted": True,
            "source_intake_consumed": True,
            "loop_name_emitted": True,
            "loop_definition_emitted": True,
            "convergence_meaning_emitted": True,
            "loop_stages_emitted": True,
            "required_component_list_emitted": True,
            "allowed_future_inventory_questions_emitted": True,
            "forbidden_future_inventory_questions_emitted": True,
            "future_inventory_target_emitted": True,
            "forbidden_claims_checked": True,
            "contract_verdict_emitted": True,
            "terminal_transition_emitted": True,
        },
        "contract_verdict": PASS_VERDICT,
        "terminal_transition": {
            "transition": ARTIFACT_TRANSITION,
            "executes_vs1_3": False,
            "authorizes_loop_execution": False,
            "authorizes_micro_sweeps": False,
            "authorizes_local_revision": False,
        },
        "failures": [],
    }


def build_markdown() -> str:
    stage_lines = "\n".join(f"- {stage['stage_id']}" for stage in LOOP_STAGES)
    component_lines = "\n".join(f"- {component}" for component in REQUIRED_COMPONENTS)
    return f"""# Phase VS1.2 controlled convergence loop contract v0

## Status

{PASS_VERDICT}

## Source intake

- source intake: phase_vs1_post_vs0_source_intake_v0
- source intake commit: {EXPECTED_HEAD}
- required source intake status: {SOURCE_INTAKE_STATUS}
- source role: BOUNDED_LOCAL_VS0_EVIDENCE_ADMITTED_FOR_DEFINITION
- loop execution authorized by source intake: false
- runner authority created by source intake: false

## Contract target

- loop name: {LOOP_NAME}
- short name: {SHORT_NAME}
- contract status: {CONTRACT_STATUS}
- execution authorized: false
- runner created: false
- micro-sweeps authorized: false
- local revision authorized: false
- portability claimed: false
- global generalization claimed: false
- performance optimization claimed: false
- scale optimization claimed: false

## Definition

{LOOP_DEFINITION}

## Convergence meaning

Convergence means {CONVERGENCE_DEFINITION}.

- optimization claimed: false
- global convergence claimed: false
- success guaranteed: false
- domain metric supplied by VS1.2: false
- convergence criterion required before execution: true

## Loop stages

{stage_lines}

## Required components

{component_lines}

## Component presence boundary

- components declared: true
- components inventoried: false
- all components present: false
- component sufficiency checked: false
- component authority checked: false
- component missingness checked: false

## VS1.3 boundary

- VS1.3 may inventory declared components: true
- VS1.3 may certify loop readiness: false
- VS1.3 may execute loop: false
- VS1.3 may authorize micro-sweeps: false
- VS1.3 may apply revisions: false
- VS1.3 may create runner: false

## Contract boundary

- contract defined: true
- contract authorized for execution: false
- contract readiness certified: false
- contract component inventory complete: false
- contract execution preconditions passed: false

## Evidence Yield

- yield branch: CONFIRMATION_YIELD
- Diagnostic Yield available on typed stop: true

## Terminal transition

{ARTIFACT_TRANSITION}

## Non-claim

VS1.2 defines the Minimal Controlled Convergence Loop contract only. It does not inventory component presence, certify readiness, authorize execution, create a runner, create move-space, run micro-sweeps, authorize local revision, demonstrate portability, generalize VS0, optimize performance, optimize scale, or execute VS1.3.
"""


def validate_contract(contract: dict[str, Any], md: str) -> None:
    if contract.get("schema_version") != SCHEMA_VERSION:
        fail(
            "STOP_VS1_2_LOOP_DEFINITION_MISSING",
            section="contract",
            field="schema_version",
            expected=SCHEMA_VERSION,
            actual=contract.get("schema_version"),
        )
    if get_value(contract, "loop_contract.loop_name") != LOOP_NAME:
        fail(
            "STOP_VS1_2_LOOP_NAME_MISSING",
            section="loop_contract",
            field="loop_name",
            expected=LOOP_NAME,
            actual=get_value(contract, "loop_contract.loop_name"),
        )
    if not get_value(contract, "loop_contract.definition"):
        fail(
            "STOP_VS1_2_LOOP_DEFINITION_MISSING",
            section="loop_contract",
            field="definition",
            expected="non-empty definition",
            actual=get_value(contract, "loop_contract.definition"),
        )
    if get_value(contract, "convergence_meaning.definition") != CONVERGENCE_DEFINITION:
        fail(
            "STOP_VS1_2_CONVERGENCE_MEANING_MISSING",
            section="convergence_meaning",
            field="definition",
            expected=CONVERGENCE_DEFINITION,
            actual=get_value(contract, "convergence_meaning.definition"),
        )
    for key in [
        "optimization_claimed",
        "global_convergence_claimed",
        "success_guaranteed",
        "domain_metric_supplied_by_vs1_2",
    ]:
        if get_value(contract, f"convergence_meaning.{key}") is not False:
            fail(
                "STOP_VS1_2_CONVERGENCE_MEANING_OVERBROAD",
                section="convergence_meaning",
                field=key,
                expected=False,
                actual=get_value(contract, f"convergence_meaning.{key}"),
            )
    if get_value(
        contract,
        "convergence_meaning.convergence_criterion_required_before_execution",
    ) is not True:
        fail(
            "STOP_VS1_2_CONVERGENCE_CRITERION_REQUIREMENT_MISSING",
            section="convergence_meaning",
            field="convergence_criterion_required_before_execution",
            expected=True,
            actual=get_value(
                contract,
                "convergence_meaning.convergence_criterion_required_before_execution",
            ),
        )
    if [s.get("stage_id") for s in contract.get("loop_stages", [])] != [
        s["stage_id"] for s in LOOP_STAGES
    ]:
        fail(
            "STOP_VS1_2_LOOP_STAGE_CONTRACTS_MISSING",
            section="loop_stages",
            field="stage_ids",
            expected=[s["stage_id"] for s in LOOP_STAGES],
            actual=[s.get("stage_id") for s in contract.get("loop_stages", [])],
        )
    for stage in contract.get("loop_stages", []):
        if stage.get("executable_in_vs1_2") is not False:
            fail(
                "STOP_VS1_2_NEXT_UNIT_EXECUTED",
                section="loop_stages",
                field=f"{stage.get('stage_id')}.executable_in_vs1_2",
                expected=False,
                actual=stage.get("executable_in_vs1_2"),
            )
    if contract.get("required_components") != REQUIRED_COMPONENTS:
        fail(
            "STOP_VS1_2_REQUIRED_COMPONENT_LIST_MISSING",
            section="required_components",
            field="required_components",
            expected=REQUIRED_COMPONENTS,
            actual=contract.get("required_components"),
        )
    if get_value(contract, "component_presence_claims.components_declared") is not True:
        fail(
            "STOP_VS1_2_REQUIRED_COMPONENT_LIST_MISSING",
            section="component_presence_claims",
            field="components_declared",
            expected=True,
            actual=get_value(contract, "component_presence_claims.components_declared"),
        )
    for key in [
        "components_inventoried",
        "all_components_present",
        "component_sufficiency_checked",
        "component_authority_checked",
        "component_missingness_checked",
    ]:
        if get_value(contract, f"component_presence_claims.{key}") is not False:
            fail(
                "STOP_VS1_2_COMPONENT_PRESENCE_CLAIMED",
                section="component_presence_claims",
                field=key,
                expected=False,
                actual=get_value(contract, f"component_presence_claims.{key}"),
            )
    if get_value(contract, "future_inventory_target.next_unit") != (
        "phase_vs1_controlled_loop_precondition_inventory_v0"
    ):
        fail(
            "STOP_VS1_2_FUTURE_INVENTORY_TARGET_MISSING",
            section="future_inventory_target",
            field="next_unit",
            expected="phase_vs1_controlled_loop_precondition_inventory_v0",
            actual=get_value(contract, "future_inventory_target.next_unit"),
        )
    if contract.get("allowed_future_inventory_questions") != (
        ALLOWED_FUTURE_INVENTORY_QUESTIONS
    ):
        fail(
            "STOP_VS1_2_ALLOWED_INVENTORY_QUESTIONS_MISSING",
            section="allowed_future_inventory_questions",
            field="questions",
            expected=ALLOWED_FUTURE_INVENTORY_QUESTIONS,
            actual=contract.get("allowed_future_inventory_questions"),
        )
    if contract.get("forbidden_future_inventory_questions") != (
        FORBIDDEN_FUTURE_INVENTORY_QUESTIONS
    ):
        fail(
            "STOP_VS1_2_FORBIDDEN_INVENTORY_QUESTIONS_MISSING",
            section="forbidden_future_inventory_questions",
            field="questions",
            expected=FORBIDDEN_FUTURE_INVENTORY_QUESTIONS,
            actual=contract.get("forbidden_future_inventory_questions"),
        )
    false_checks = {
        "loop_contract.execution_authorized": "STOP_VS1_2_EXECUTION_AUTHORITY_CLAIMED",
        "loop_contract.runner_created": "STOP_VS1_2_RUNNER_CREATED",
        "loop_contract.micro_sweeps_authorized": "STOP_VS1_2_MICRO_SWEEPS_AUTHORIZED",
        "loop_contract.local_revision_authorized": "STOP_VS1_2_LOCAL_REVISION_AUTHORIZED",
        "loop_contract.portability_claimed": "STOP_VS1_2_PORTABILITY_CLAIMED",
        "loop_contract.global_generalization_claimed": (
            "STOP_VS1_2_GLOBAL_GENERALIZATION_CLAIMED"
        ),
        "loop_contract.performance_optimization_claimed": (
            "STOP_VS1_2_OPTIMIZATION_TARGET_ASSUMED"
        ),
        "loop_contract.scale_optimization_claimed": (
            "STOP_VS1_2_OPTIMIZATION_TARGET_ASSUMED"
        ),
        "contract_boundary.contract_readiness_certified": (
            "STOP_VS1_2_READINESS_CERTIFIED"
        ),
        "terminal_transition.executes_vs1_3": "STOP_VS1_2_NEXT_UNIT_EXECUTED",
    }
    for path, code in false_checks.items():
        if get_value(contract, path) is not False:
            fail(
                code,
                section=path.rsplit(".", 1)[0],
                field=path.rsplit(".", 1)[1],
                expected=False,
                actual=get_value(contract, path),
            )
    if get_value(contract, "terminal_transition.transition") != ARTIFACT_TRANSITION:
        fail(
            "STOP_VS1_2_NEXT_UNIT_EXECUTED",
            section="terminal_transition",
            field="transition",
            expected=ARTIFACT_TRANSITION,
            actual=get_value(contract, "terminal_transition.transition"),
        )
    hits = markdown_contains_vs1_2_overclaim(md)
    if hits:
        fail(
            "STOP_VS1_2_GLOBAL_GENERALIZATION_CLAIMED",
            section="markdown",
            field="overclaim_guard",
            expected=[],
            actual=hits,
        )


def emit_success_readout() -> None:
    print("BUILD_PHASE_VS1_CONTROLLED_CONVERGENCE_LOOP_CONTRACT_V0_COMPLETE")
    print(f"artifact_id={ARTIFACT_ID}")
    print(f"schema_version={SCHEMA_VERSION}")
    print(f"phase_id={PHASE_ID}")
    print(f"unit_id={UNIT_ID}")
    print(f"unit_role={UNIT_ROLE}")
    print(f"source_intake_commit_sha={EXPECTED_HEAD}")
    print(f"source_intake_required_status={SOURCE_INTAKE_STATUS}")
    print(f"source_intake_required_transition={SOURCE_INTAKE_TRANSITION}")
    print(f"loop_name={LOOP_NAME}")
    print(f"short_name={SHORT_NAME}")
    print(f"contract_status={CONTRACT_STATUS}")
    print("contract_defined=true")
    print("contract_authorized_for_execution=false")
    print("contract_readiness_certified=false")
    print("contract_component_inventory_complete=false")
    print("contract_execution_preconditions_passed=false")
    print("convergence_meaning_bounded=true")
    print("convergence_optimization_claimed=false")
    print("global_convergence_claimed=false")
    print("success_guaranteed=false")
    print("domain_metric_supplied_by_vs1_2=false")
    print("convergence_criterion_required_before_execution=true")
    print(f"loop_stage_count={len(LOOP_STAGES)}")
    print(f"required_component_count={len(REQUIRED_COMPONENTS)}")
    print("components_declared=true")
    print("components_inventoried=false")
    print("all_components_present=false")
    print("component_sufficiency_checked=false")
    print("component_authority_checked=false")
    print("component_missingness_checked=false")
    print("vs1_3_may_inventory_declared_components=true")
    print("vs1_3_may_certify_loop_readiness=false")
    print("vs1_3_may_execute_loop=false")
    print("vs1_3_may_authorize_micro_sweeps=false")
    print("vs1_3_may_apply_revisions=false")
    print("vs1_3_may_create_runner=false")
    print("execution_authorized=false")
    print("runner_created=false")
    print("move_space_created=false")
    print("micro_sweeps_authorized=false")
    print("local_revision_authorized=false")
    print("portability_claimed=false")
    print("global_generalization_claimed=false")
    print("performance_optimization_claimed=false")
    print("scale_optimization_claimed=false")
    print("pressure_classification_operational=false")
    print("evidence_yield_branch=CONFIRMATION_YIELD")
    print("diagnostic_yield_available_on_typed_stop=true")
    print("vs1_1_source_intake_mutated_by_vs1_2=false")
    print("post_vs0_direction_decision_receipt_mutated_by_vs1_2=false")
    print("vs0_6_phase_closure_mutated_by_vs1_2=false")
    print("vs0_source_artifacts_mutated_by_vs1_2=false")
    print("vs1_3_built=false")
    print("vs1_3_run=false")
    print("controlled_loop_created=false")
    print("runner_created=false")
    print("runtime_created=false")
    print("move_space_created=false")
    print("micro_sweeps_created=false")
    print("readiness_certificate_created=false")
    print(f"contract_verdict={PASS_VERDICT}")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition={PRINT_TRANSITION}")


def emit_typed_stop(exc: ContractFailure) -> None:
    print("BUILD_PHASE_VS1_CONTROLLED_CONVERGENCE_LOOP_CONTRACT_V0_TYPED_STOP")
    print(f"artifact_id={ARTIFACT_ID}")
    print(f"phase_id={PHASE_ID}")
    print(f"unit_id={UNIT_ID}")
    print(f"contract_verdict={exc.code}")
    print("yield_branch=DIAGNOSTIC_YIELD")
    print(f"missing_or_invalid_section={exc.section}")
    print(f"violating_field={exc.field}")
    print(f"expected_value={exc.expected}")
    print(f"actual_value={exc.actual}")
    print(f"next_lawful_surface={exc.next_surface}")
    print("self_repair_performed=false")
    print("execution_authorized=false")
    print("runner_created=false")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition=STOP({exc.code})")


def generate() -> int:
    root = detect_repo_root(Path.cwd())
    require_head(root)
    validate_dirty_scope(root)
    ensure_no_forbidden_artifacts(root)
    require_file(root, SOURCE_INTAKE_MD)
    require_file(root, DIRECTION_MD)
    require_file(root, VS0_CLOSURE_MD)
    intake = load_json(root, SOURCE_INTAKE_JSON)
    load_json(root, DIRECTION_JSON)
    load_json(root, VS0_CLOSURE_JSON)
    validate_source_intake(intake)
    before_hashes = capture_source_hashes(root)

    contract = build_contract(root, intake)
    md = build_markdown()
    validate_contract(contract, md)

    output_json = root / OUTPUT_JSON
    output_md = root / OUTPUT_MD
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(contract, indent=2, sort_keys=True) + "\n",
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
    except ContractFailure as exc:
        emit_typed_stop(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
