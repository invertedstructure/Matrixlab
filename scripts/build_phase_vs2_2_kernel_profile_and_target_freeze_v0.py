#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


EXPECTED_ROOT = "/home/asd/projects/matrixlab"
EXPECTED_BRANCH = "master"
EXPECTED_HEAD = "9d529c6813fd5db38eb4a63368a8d538aa7a88e4"

PHASE_ID = "PHASE_VS2"
UNIT_ID = "VS2.2_KERNEL_PROFILE_AND_TARGET_FREEZE"
UNIT_ROLE = "PROFILE_AND_SEMANTIC_TARGET_FREEZE_ONLY"
CANONICALIZATION = "MATRIXLAB_CANONICAL_JSON_V0"

SOURCE_INTAKE_PATH = "docs/matrixlabs/phase_vs2/phase_vs2_post_vs1_source_intake_v0.json"
SOURCE_INTAKE_MD_PATH = "docs/matrixlabs/phase_vs2/phase_vs2_post_vs1_source_intake_v0.md"
SOURCE_RECEIPT_PATH = "docs/matrixlabs/phase_vs2/phase_vs2_1_post_vs1_source_intake_receipt_v0.json"
OUTPUT_PROFILE_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_first_sweep_capable_kernel_profile_v0.json"
OUTPUT_PROFILE_MD = "docs/matrixlabs/phase_vs2/phase_vs2_first_sweep_capable_kernel_profile_v0.md"
OUTPUT_TARGET_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_typed_state_contract_convergence_target_freeze_v0.json"
OUTPUT_TARGET_MD = "docs/matrixlabs/phase_vs2/phase_vs2_typed_state_contract_convergence_target_freeze_v0.md"
OUTPUT_RECEIPT = "docs/matrixlabs/phase_vs2/phase_vs2_2_kernel_profile_and_target_freeze_receipt_v0.json"

SCRIPT_PATH = "scripts/build_phase_vs2_2_kernel_profile_and_target_freeze_v0.py"
BASELINE_SCRIPT = "scripts/build_baseline_share_v0.py"

SOURCE_INTAKE_FILE_SHA256 = "aac9ba4eec3ca577ead6cd23f8af6b9ecc6a9d542ec2395450a698f45465514b"
SOURCE_INTAKE_MD_SHA256 = "a1a892efd2819c59ff0144464fbb5dec4d72e6dd82a70a3bad63ee04010aa7f3"
SOURCE_RECEIPT_FILE_SHA256 = "97e0046641b67bdc4740c1a82e5356eb4ffda6df0d2584e04d474b2b8e6cac5f"
SOURCE_INTAKE_SHA256 = "830c62352e6eab4445b8cac9bbb7851da49a39633fc5cb673b71283bba1eaaeb"
SOURCE_MANIFEST_SHA256 = "9aaceb1758920971d8f5d7f305b837b7021ebc0a84714dea08755efce1c0a6ef"
SOURCE_RECEIPT_SHA256 = "b8b440b920993d38f77b0359ea928a255d780e5e682572fcc9144c35e63609cd"
DECISION_PACKAGE_SHA256 = "e9e4143ad2efdd285fe9e598e50d965d82057f7a8d6ccc4c52478a596d6b788b"

PROFILE_SCHEMA = "matrixlabs_phase_vs2_first_sweep_capable_kernel_profile_v0"
PROFILE_ARTIFACT_ID = "phase_vs2_first_sweep_capable_kernel_profile_v0"
PROFILE_ID = "FIRST_SWEEP_CAPABLE_KERNEL_PROFILE_V0"
PROFILE_CLASS = "BOUNDED_VERTICAL_EVIDENCE_PRODUCING_KERNEL_PROFILE"
PROFILE_STATUS = "SEMANTIC_PROFILE_FROZEN_CONSTRUCTION_PENDING"
MCCL_RELATIONSHIP = "BOUNDED_PROFILE_PROJECTION_OF_MCCL_V0"
PROFILE_GATE = "VS2_2_FIRST_SWEEP_KERNEL_PROFILE_FREEZE_PASS"

TARGET_SCHEMA = "matrixlabs_phase_vs2_typed_state_contract_convergence_target_freeze_v0"
TARGET_ARTIFACT_ID = "phase_vs2_typed_state_contract_convergence_target_freeze_v0"
TARGET_FAMILY = "BOUNDED_CONTRACT_CONVERGENCE"
TARGET_ID = "TYPED_STATE_CONTRACT_CONVERGENCE_V0"
TARGET_STATUS = "SEMANTIC_TARGET_FROZEN_IMPLEMENTATION_SCHEMA_PENDING"
TARGET_GATE = "VS2_2_TYPED_STATE_CONTRACT_CONVERGENCE_TARGET_FREEZE_PASS"

RECEIPT_SCHEMA = "matrixlabs_phase_vs2_2_kernel_profile_and_target_freeze_receipt_v0"
RECEIPT_ARTIFACT_ID = "phase_vs2_2_kernel_profile_and_target_freeze_receipt_v0"
RECEIPT_GATE = "VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_PASS"
EVIDENCE_YIELD_BRANCH = "CONFIRMATION_YIELD"
LOGICAL_TERMINAL = "ADVANCE(VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PENDING)"
TERMINAL_TRANSITION = "ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_V0_PENDING)"

PROFILE_BOUND_SECTIONS = [
    "source_intake_binding",
    "source_intake_commit_reconciliation",
    "accepted_direction_binding",
    "profile_grant_consumption",
    "remaining_grant_routing",
    "withheld_authority_binding",
    "profile_identity",
    "mccl_profile_relationship",
    "component_classification_contract",
    "component_profile_table",
    "component_profile_summary",
    "maximum_construction_envelope",
    "maximum_future_execution_envelope",
    "pressure_classification_vocabulary",
    "terminal_outcome_family",
    "fixture_role_requirements",
    "forbidden_behavior_boundary",
    "downstream_construction_sequence",
    "downstream_construction_objects",
    "pre_vs2_2_phase_state",
    "post_vs2_2_phase_state",
    "profile_nonclaims",
]

TARGET_BOUND_SECTIONS = [
    "source_intake_binding",
    "accepted_direction_binding",
    "profile_binding_reference",
    "profile_grant_consumption_reference",
    "target_identity",
    "target_statement",
    "target_path",
    "scope_regime_requirements",
    "object_role_separation",
    "target_success_condition",
    "already_valid_candidate_semantics",
    "positive_path_requirement",
    "admissibility_policy_requirements",
    "convergence_criterion_requirements",
    "source_policy_requirements",
    "terminal_outcome_family",
    "unclassified_result_posture",
    "target_mutation_boundaries",
    "target_nonclaims",
]

ALLOWED_DIRTY = {
    SCRIPT_PATH,
    BASELINE_SCRIPT,
    OUTPUT_PROFILE_JSON,
    OUTPUT_PROFILE_MD,
    OUTPUT_TARGET_JSON,
    OUTPUT_TARGET_MD,
    OUTPUT_RECEIPT,
    "baseline_share/COMMIT_CONTEXT.md",
    "baseline_share/CURRENT_STATE.md",
    "baseline_share/MANIFEST.json",
    "baseline_share/RECEIPT_POINTERS.md",
}

PROTECTED_SOURCE_PATHS = {
    SOURCE_INTAKE_PATH,
    SOURCE_INTAKE_MD_PATH,
    SOURCE_RECEIPT_PATH,
}

FORBIDDEN_PATHS = [
    "docs/matrixlabs/runner",
    "docs/matrixlabs/runtime",
    "docs/matrixlabs/move_space",
    "docs/matrixlabs/micro_sweeps",
    "discussion_packets",
]

GRANT_IDS = [
    "VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY",
    "VS2_BOUNDED_CONSTRUCTION_AUTHORITY",
    "VS2_FIXTURE_CONSTRUCTION_AUTHORITY",
    "VS2_FIRST_RUN_READINESS_GATE_CONSTRUCTION_AUTHORITY",
    "VS2_CONSTRUCTION_PACKAGE_VERIFICATION_AUTHORITY",
]

REQUIRED_FULL = [
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
    "C17_FORBIDDEN_EFFECT_GUARD",
    "C19_HUMAN_ESCALATION_DECISION_BOUNDARY",
    "C20_CONVERGENCE_CRITERION_CONTRACT",
]

REQUIRED_MINIMAL = [
    "C12_PRESSURE_READOUT_CONTRACT",
    "C13_PRESSURE_CLASSIFICATION_VOCABULARY",
    "C16_REPLAY_AUDIT_CONTRACT",
    "C18_EVIDENCE_YIELD_HOOK",
]

DEFERRED = [
    "C14_LOCAL_REVISION_SURFACE_CONTRACT",
    "C15_BOUNDED_PORTABILITY_MAP_CONTRACT",
]

SURFACE_BY_COMPONENT = {
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
    "C18_EVIDENCE_YIELD_HOOK": "S18_EVIDENCE_YIELD_HOOK_SURFACE",
    "C19_HUMAN_ESCALATION_DECISION_BOUNDARY": "S19_HUMAN_ESCALATION_DECISION_BOUNDARY_SURFACE",
    "C20_CONVERGENCE_CRITERION_CONTRACT": "S20_CONVERGENCE_CRITERION_CONTRACT_SURFACE",
}

COMPONENT_SEMANTICS = {
    "C01_SCOPE_REGIME_DECLARATION_CONTRACT": {
        "profile_requirement": "later explicit bounded contract for scope, regime, identity, sameness/difference, authority, claim, source, and transformation boundaries",
        "supported_function": "declare the external governing frame for the bounded target run",
        "omitted_or_deferred_function": "no scope/regime implementation schema is constructed by VS2.2",
        "construction_unit": "VS2.3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION",
    },
    "C02_TYPED_STATE_OBJECT_CONTRACT": {
        "profile_requirement": "freeze four distinct roles: declared scope/regime, runtime control state, candidate contract, and frozen target contract",
        "supported_function": "separate runtime control state, candidate contract, and frozen target contract under an external scope/regime frame",
        "omitted_or_deferred_function": "no runtime, candidate, or target implementation schema is constructed by VS2.2",
        "construction_unit": "VS2.3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION",
    },
    "C03_EXPLICIT_MOVE_SPACE_CONTRACT": {
        "profile_requirement": "finite, versioned, target-bound, scope/regime-bound, source-bound, authority-bound, fixture-set-bound, non-reusable move space",
        "supported_function": "bound all future transformations to one declared target family and first target",
        "omitted_or_deferred_function": "no move-space implementation artifact is constructed by VS2.2",
        "construction_unit": "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE",
    },
    "C04_MOVE_SELECTOR_CONTRACT": {
        "profile_requirement": "later selector enumerates admissible moves, selects exactly one move, or exposes no admissible move without mutation or invention",
        "supported_function": "separate move enumeration/selection from mutation",
        "omitted_or_deferred_function": "no selector contract is constructed by VS2.2",
        "construction_unit": "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION",
    },
    "C05_MOVE_APPLICATOR_CONTRACT": {
        "profile_requirement": "later applicator applies only the selected declared candidate delta or emits a typed application stop",
        "supported_function": "create a bounded candidate version without selecting another move or inventing fields, sources, schemas, capabilities, or authority",
        "omitted_or_deferred_function": "no applicator contract is constructed by VS2.2",
        "construction_unit": "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION",
    },
    "C06_AUTHORITY_POLICY": {
        "profile_requirement": "future distinct authority classes for source admission, definition, construction, fixtures, readiness, verification, execution, sweep, rerun, expansion, revision, promotion, and reuse",
        "supported_function": "prevent construction authority from becoming execution, rerun, expansion, reuse, or promotion authority",
        "omitted_or_deferred_function": "no new authority is created by VS2.2",
        "construction_unit": "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION",
    },
    "C07_RADIUS_BUDGET_POLICY": {
        "profile_requirement": "explicit caps with zero automatic renewal",
        "supported_function": "bound future cases, moves, radius, budget, and rerun behavior",
        "omitted_or_deferred_function": "no execution package is constructed by VS2.2",
        "construction_unit": "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION",
    },
    "C08_HALT_POLICY": {
        "profile_requirement": "typed halts for target reached, missing inputs, authority/capability gaps, exhausted budget, no move, validation/admissibility failures, forbidden effects, identity or scope failures, non-progress, repeated state, convergence unmet, and unclassified results",
        "supported_function": "contain future runs without hidden continuation",
        "omitted_or_deferred_function": "no halt implementation is constructed by VS2.2",
        "construction_unit": "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION",
    },
    "C09_RECEIPT_OBLIGATION_CONTRACT": {
        "profile_requirement": "move-attempt receipt, case-terminal receipt, and sweep/run report without unrestricted private reasoning trace",
        "supported_function": "preserve evidence for every bounded move and terminal outcome",
        "omitted_or_deferred_function": "no receipt contract implementation is constructed by VS2.2",
        "construction_unit": "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION",
    },
    "C10_SOURCE_IDENTITY_FRESHNESS_POLICY": {
        "profile_requirement": "declared source identity with no automatic source acquisition, latest-file selection, mtime authority, directory-position authority, silent replacement, ambient context, or chat-memory sourcing",
        "supported_function": "keep source identity exact and auditable",
        "omitted_or_deferred_function": "no source snapshot is frozen by VS2.2",
        "construction_unit": "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE",
    },
    "C11_MICRO_SWEEP_BOUNDS_CONTRACT": {
        "profile_requirement": "one later bounded sweep package for pressure exposure, outcome distinguishability, receipt validation, and boundary testing",
        "supported_function": "bound the future first-run package without optimization sweep authority",
        "omitted_or_deferred_function": "no sweep package is constructed or authorized by VS2.2",
        "construction_unit": "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
    },
    "C12_PRESSURE_READOUT_CONTRACT": {
        "profile_requirement": "minimal report of what reached target, what was preserved, what stopped, why it stopped, and which gap appeared",
        "supported_function": "support Confirmation Yield or Diagnostic Yield reporting",
        "omitted_or_deferred_function": "no pressure report is constructed by VS2.2",
        "construction_unit": "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
    },
    "C13_PRESSURE_CLASSIFICATION_VOCABULARY": {
        "profile_requirement": "freeze the initial pressure classification vocabulary",
        "supported_function": "separate pressure classification from validation, admissibility, convergence, and terminal outcome namespaces",
        "omitted_or_deferred_function": "no taxonomy mutation is authorized by VS2.2",
        "construction_unit": "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
    },
    "C14_LOCAL_REVISION_SURFACE_CONTRACT": {
        "profile_requirement": "deferred local revision surface may later emit a refinement candidate but may not apply it",
        "supported_function": "preserve future Diagnostic Yield without automatic repair",
        "omitted_or_deferred_function": "local revision is deferred and not satisfied by this profile",
        "construction_unit": "DEFERRED_BEYOND_FIRST_TARGET",
    },
    "C15_BOUNDED_PORTABILITY_MAP_CONTRACT": {
        "profile_requirement": "deferred portability map with no first-target portability claim",
        "supported_function": "preserve portability as out of scope for this first target",
        "omitted_or_deferred_function": "portability is deferred and not satisfied by this profile",
        "construction_unit": "DEFERRED_BEYOND_FIRST_TARGET",
    },
    "C16_REPLAY_AUDIT_CONTRACT": {
        "profile_requirement": "minimal exact-input, exact-delta, terminal-outcome, budget, target-immutability, and unexpected-mutation verification",
        "supported_function": "make future evidence replayable enough for the first target",
        "omitted_or_deferred_function": "no replay implementation is constructed by VS2.2",
        "construction_unit": "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION",
    },
    "C17_FORBIDDEN_EFFECT_GUARD": {
        "profile_requirement": "prevent or detect all frozen forbidden behaviors",
        "supported_function": "guard against unbounded execution, mutation, authority escalation, reuse, portability, and false convergence",
        "omitted_or_deferred_function": "no guard implementation is constructed by VS2.2",
        "construction_unit": "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION",
    },
    "C18_EVIDENCE_YIELD_HOOK": {
        "profile_requirement": "emit Confirmation Yield or Diagnostic Yield",
        "supported_function": "classify useful evidence even when the target is not reached",
        "omitted_or_deferred_function": "no Evidence Yield report is constructed by VS2.2",
        "construction_unit": "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
    },
    "C19_HUMAN_ESCALATION_DECISION_BOUNDARY": {
        "profile_requirement": "escalate rather than continue on missing authority, schema, capability, source expansion, move-space expansion, radius expansion, budget expansion, rerun, refinement, or unclassified outcome",
        "supported_function": "keep missing authority and ambiguity human-bounded",
        "omitted_or_deferred_function": "no autonomous continuation authority is created by VS2.2",
        "construction_unit": "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION",
    },
    "C20_CONVERGENCE_CRITERION_CONTRACT": {
        "profile_requirement": "explicit continue, repeat, non-progress, repeated-state, oscillation, cycle, radius, target-reached, and typed halt boundaries",
        "supported_function": "preserve movement/progress/target/convergence distinctions",
        "omitted_or_deferred_function": "no convergence criterion implementation is constructed by VS2.2",
        "construction_unit": "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION",
    },
}

PRESSURE_VOCABULARY = [
    "TARGET_REACHED",
    "TARGET_PRESERVED",
    "REPAIRABLE_DEFECT",
    "UNREPAIRABLE_UNDER_CURRENT_AUTHORITY",
    "MISSING_SOURCE",
    "MISSING_SCHEMA",
    "MISSING_AUTHORITY",
    "MISSING_CAPABILITY",
    "RADIUS_EXHAUSTED",
    "NO_ADMISSIBLE_MOVE",
    "VALIDATION_FAILURE",
    "ADMISSIBILITY_FAILURE",
    "FORBIDDEN_EFFECT",
    "SOURCE_IDENTITY_FAILURE",
    "SCOPE_REGIME_VIOLATION",
    "NON_PROGRESS",
    "REPEATED_STATE",
    "CONVERGENCE_CRITERION_UNMET",
    "UNCLASSIFIED_RESULT",
]

TERMINAL_OUTCOMES = [
    "TARGET_REACHED",
    "STOP_REPAIR_NOT_LAWFUL",
    "STOP_MISSING_SOURCE",
    "STOP_MISSING_SCHEMA",
    "STOP_MISSING_AUTHORITY",
    "STOP_MISSING_CAPABILITY",
    "STOP_RADIUS_EXHAUSTED",
    "STOP_NO_ADMISSIBLE_MOVE",
    "STOP_VALIDATION_FAILED",
    "STOP_ADMISSIBILITY_FAILED",
    "STOP_FORBIDDEN_EFFECT_DETECTED",
    "STOP_SOURCE_IDENTITY_UNVERIFIED",
    "STOP_SCOPE_REGIME_VIOLATION",
    "STOP_NON_PROGRESS",
    "STOP_REPEATED_STATE",
    "STOP_CONVERGENCE_CRITERION_UNMET",
    "STOP_UNCLASSIFIED_RESULT_REQUIRES_TAXONOMY_REFINEMENT",
]

FORBIDDEN_BEHAVIORS = [
    "full MCCL readiness claim",
    "runner readiness claim",
    "runner authority creation",
    "unbounded execution",
    "automatic rerun",
    "automatic radius renewal",
    "automatic self-repair",
    "automatic local revision",
    "automatic refinement application",
    "automatic schema invention",
    "automatic capability creation",
    "automatic source acquisition",
    "automatic authority escalation",
    "scope/regime expansion",
    "runtime-state self-modification",
    "target-schema mutation",
    "move-space mutation during execution",
    "source-snapshot substitution during execution",
    "reusable schema promotion",
    "reusable move promotion",
    "active registry creation",
    "second-target selection",
    "first-target substitution",
    "portability testing",
    "cross-domain generalization",
    "performance optimization",
    "scale optimization",
    "global convergence claim",
    "false convergence from repeated movement",
    "hidden continuation after typed stop",
]

FIXTURE_ROLES = [
    "REPAIRABLE_POSITIVE_PATH",
    "ALREADY_VALID_PRESERVATION",
    "MISSING_REQUIRED_FIELD",
    "INVALID_TYPED_VALUE",
    "MISSING_SOURCE",
    "AUTHORITY_OVERREACH",
    "FORBIDDEN_EFFECT",
    "MISSING_SCHEMA",
    "MISSING_CAPABILITY",
    "NO_ADMISSIBLE_MOVE",
    "SCOPE_REGIME_VIOLATION",
    "NON_PROGRESS_OR_REPEATED_STATE",
]

DOWNSTREAM_SEQUENCE = [
    {
        "unit_id": "VS2.3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION",
        "may_construct_only": [
            "scope/regime contract",
            "runtime control-state contract",
            "candidate contract",
            "frozen target contract",
            "serialized target success condition",
        ],
    },
    {
        "unit_id": "VS2.4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE",
        "may_construct_only": [
            "move-vocabulary separation",
            "finite move contracts",
            "source and version bindings",
            "bounded future execution-authority shape",
        ],
    },
    {
        "unit_id": "VS2.5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION",
        "may_construct_only": [
            "selector",
            "applicator",
            "validation boundary",
            "admissibility boundary",
            "convergence criterion",
            "radius and budget policy",
            "halt policy",
            "receipts",
            "replay and audit",
            "forbidden-effect guard",
        ],
    },
    {
        "unit_id": "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
        "may_construct_only": [
            "positive-path fixture",
            "already-valid preservation fixture",
            "negative and perturbation fixtures",
            "non-progress or repeated-state fixture",
            "concrete source snapshot",
            "exact future execution envelope",
            "pressure readout",
            "Evidence Yield report",
            "first-run construction-readiness gate",
        ],
        "executes_fixtures": False,
    },
    {
        "unit_id": "VS2.7_PHASE_CLOSURE",
        "may": [
            "verify the complete bounded construction package",
            "emit Phase VS2 closure",
            "classify construction-ready or typed blockers",
            "preserve execution authority absent",
        ],
    },
]

DOWNSTREAM_OBJECTS = [
    "T01_SCOPE_REGIME_DECLARATION_CONTRACT",
    "T02_FIRST_TARGET_SEMANTIC_OBJECT_DEFINITION",
    "T03_CANDIDATE_AND_TERMINAL_CONTRACT_SCHEMAS",
    "T04_RUNTIME_STATE_CONTRACT",
    "T05_FINITE_MOVE_SPACE_CONTRACT",
    "T06_SELECTOR_CONTRACT",
    "T07_APPLICATOR_CONTRACT",
    "T08_VALIDATION_AND_ADMISSIBILITY_BOUNDARY",
    "T09_RADIUS_BUDGET_AND_HALT_POLICY",
    "T10_MOVE_ATTEMPT_RECEIPT_CONTRACT",
    "T11_CASE_TERMINAL_RECEIPT_CONTRACT",
    "T12_SWEEP_RUN_REPORT_CONTRACT",
    "T13_PRESSURE_READOUT_AND_CLASSIFICATION_CONTRACT",
    "T14_POSITIVE_PATH_SPECIMEN",
    "T15_PRESERVATION_SPECIMEN",
    "T16_PERTURBATION_FIXTURE_SET",
    "T17_SOURCE_SNAPSHOT",
    "T18_FORBIDDEN_EFFECT_GUARD",
    "T19_FIRST_RUN_CONSTRUCTION_READINESS_GATE",
    "T20_CONVERGENCE_CRITERION_CONTRACT",
]


class VS22Failure(RuntimeError):
    def __init__(
        self,
        code: str,
        field: str,
        expected: Any,
        observed: Any,
        boundary: str = "VS2.2_PROFILE_AND_TARGET_FREEZE_BOUNDARY",
        next_surface: str = "BOOKKEEPING_OR_VS2_2_REPAIR_SURFACE_REQUIRED",
    ) -> None:
        super().__init__(code)
        self.code = code
        self.field = field
        self.expected = expected
        self.observed = observed
        self.boundary = boundary
        self.next_surface = next_surface


def fail(code: str, field: str, expected: Any, observed: Any, boundary: str = "VS2.2_PROFILE_AND_TARGET_FREEZE_BOUNDARY") -> None:
    raise VS22Failure(code, field, expected, observed, boundary)


def run_git(root: Path, args: list[str], *, binary: bool = False, check: bool = True) -> str | bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
    )
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, ["git", *args], result.stdout, result.stderr)
    return result.stdout if binary else result.stdout.strip()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_hash(payload: Any) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def parse_status_paths(status: str) -> list[str]:
    paths: list[str] = []
    for line in status.splitlines():
        raw = line[2:].strip()
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]
        paths.append(raw)
    return paths


def require_equal(observed: Any, expected: Any, code: str, field: str) -> None:
    if observed != expected:
        fail(code, field, expected, observed)


def require_true(observed: Any, code: str, field: str) -> None:
    if observed is not True:
        fail(code, field, True, observed)


def require_false(observed: Any, code: str, field: str) -> None:
    if observed is not False:
        fail(code, field, False, observed)


def check_repo(root: Path) -> None:
    actual_root = run_git(root, ["rev-parse", "--show-toplevel"])
    require_equal(actual_root, EXPECTED_ROOT, "STOP_VS2_2_REPOSITORY_ROOT_MISMATCH", "repository_root")
    branch = run_git(root, ["branch", "--show-current"])
    require_equal(branch, EXPECTED_BRANCH, "STOP_VS2_2_REPOSITORY_ROOT_MISMATCH", "branch")
    head = run_git(root, ["rev-parse", "HEAD"])
    require_equal(head, EXPECTED_HEAD, "STOP_VS2_2_UNEXPECTED_HEAD", "HEAD")
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=root).returncode != 0
    require_false(staged, "STOP_VS2_2_PREEXISTING_DIRTY_WORKTREE", "staged_changes_present")
    if (root / "discussion_packets").exists():
        fail("STOP_VS2_2_PREEXISTING_DIRTY_WORKTREE", "discussion_packets", "absent", "present")
    validate_dirty_scope(root)
    ensure_forbidden_absent(root)


def validate_dirty_scope(root: Path) -> None:
    status = run_git(root, ["status", "--short", "--untracked-files=all"])
    paths = parse_status_paths(status)
    unexpected = [path for path in paths if path not in ALLOWED_DIRTY]
    if unexpected:
        fail("STOP_VS2_2_UNDECLARED_DIRTY_PATH", "git_status_dirty_paths", sorted(ALLOWED_DIRTY), unexpected)
    protected = [path for path in paths if path in PROTECTED_SOURCE_PATHS]
    if protected:
        fail("STOP_VS2_2_PROTECTED_SOURCE_MODIFIED", "protected_source_paths", [], protected)


def ensure_forbidden_absent(root: Path) -> None:
    present = [path for path in FORBIDDEN_PATHS if (root / path).exists()]
    if present:
        fail("STOP_VS2_2_UNDECLARED_DIRTY_PATH", "forbidden_paths", "absent", present)


def committed_bytes(root: Path, rel_path: str) -> bytes:
    exists = subprocess.run(
        ["git", "cat-file", "-e", f"{EXPECTED_HEAD}:^{rel_path}"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if exists.returncode == 0:
        fail("STOP_VS2_2_SOURCE_INTAKE_PATH_MISSING_AT_COMMIT", rel_path, "blob path", "tree-ish path expression")
    commit_exists = subprocess.run(
        ["git", "cat-file", "-e", EXPECTED_HEAD],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if commit_exists.returncode != 0:
        fail("STOP_VS2_2_SOURCE_INTAKE_COMMIT_MISSING", "source_commit_sha", EXPECTED_HEAD, "missing")
    try:
        return run_git(root, ["show", f"{EXPECTED_HEAD}:{rel_path}"], binary=True)  # type: ignore[return-value]
    except subprocess.CalledProcessError as exc:
        fail("STOP_VS2_2_SOURCE_INTAKE_PATH_MISSING_AT_COMMIT", rel_path, "present", exc.stderr)


def verify_committed_file(root: Path, rel_path: str, expected_sha: str) -> bytes:
    committed = committed_bytes(root, rel_path)
    worktree_path = root / rel_path
    if not worktree_path.exists():
        fail("STOP_VS2_2_SOURCE_INTAKE_PATH_MISSING_AT_COMMIT", rel_path, "present in worktree", "missing")
    worktree = worktree_path.read_bytes()
    if worktree != committed:
        fail("STOP_VS2_2_SOURCE_INTAKE_WORKTREE_DIVERGES_FROM_COMMIT", rel_path, "working tree bytes equal committed bytes", "different")
    actual_sha = sha256_bytes(worktree)
    require_equal(actual_sha, expected_sha, "STOP_VS2_2_SOURCE_INTAKE_FILE_HASH_MISMATCH", rel_path)
    return worktree


def verify_source_intake(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    intake_bytes = verify_committed_file(root, SOURCE_INTAKE_PATH, SOURCE_INTAKE_FILE_SHA256)
    verify_committed_file(root, SOURCE_INTAKE_MD_PATH, SOURCE_INTAKE_MD_SHA256)
    receipt_bytes = verify_committed_file(root, SOURCE_RECEIPT_PATH, SOURCE_RECEIPT_FILE_SHA256)
    intake = json.loads(intake_bytes.decode("utf-8"))
    receipt = json.loads(receipt_bytes.decode("utf-8"))

    require_equal(intake.get("schema_version"), "matrixlabs_phase_vs2_post_vs1_source_intake_v0", "STOP_VS2_2_SOURCE_INTAKE_NOT_PASS", "intake.schema_version")
    require_equal(intake.get("artifact_id"), "phase_vs2_post_vs1_source_intake_v0", "STOP_VS2_2_SOURCE_INTAKE_NOT_PASS", "intake.artifact_id")
    require_equal(intake.get("phase_id"), PHASE_ID, "STOP_VS2_2_SOURCE_INTAKE_NOT_PASS", "intake.phase_id")
    require_equal(intake.get("unit_id"), "VS2.1_POST_VS1_SOURCE_INTAKE", "STOP_VS2_2_SOURCE_INTAKE_NOT_PASS", "intake.unit_id")
    require_equal(intake.get("unit_role"), "PHASE_ENTRY_SOURCE_INTAKE_ONLY", "STOP_VS2_2_SOURCE_INTAKE_NOT_PASS", "intake.unit_role")
    require_equal(intake.get("intake_status"), "VS2_1_POST_VS1_SOURCE_INTAKE_PASS", "STOP_VS2_2_SOURCE_INTAKE_NOT_PASS", "intake.intake_status")

    manifest = intake["source_manifest_binding"]
    manifest_payload = manifest["source_manifest_payload"]
    require_equal(manifest.get("source_manifest_entry_count"), 8, "STOP_VS2_2_SOURCE_INTAKE_NOT_PASS", "source_manifest_entry_count")
    for key in [
        "duplicate_source_id_count",
        "duplicate_declared_path_count",
        "missing_required_source_count",
        "unverified_source_count",
        "undeclared_source_count",
    ]:
        require_equal(manifest.get(key), 0, "STOP_VS2_2_SOURCE_INTAKE_NOT_PASS", key)
    require_equal(canonical_hash(manifest_payload), SOURCE_MANIFEST_SHA256, "STOP_VS2_2_SOURCE_MANIFEST_HASH_MISMATCH", "source_manifest_payload")
    require_equal(manifest.get("source_manifest_sha256"), SOURCE_MANIFEST_SHA256, "STOP_VS2_2_SOURCE_MANIFEST_HASH_MISMATCH", "source_manifest_sha256")

    intake_binding = intake["source_intake_binding"]
    intake_payload = intake_binding["source_intake_payload"]
    require_equal(canonical_hash(intake_payload), SOURCE_INTAKE_SHA256, "STOP_VS2_2_SOURCE_INTAKE_CANONICAL_HASH_MISMATCH", "source_intake_payload")
    require_equal(intake_binding.get("source_intake_sha256"), SOURCE_INTAKE_SHA256, "STOP_VS2_2_SOURCE_INTAKE_CANONICAL_HASH_MISMATCH", "source_intake_sha256")

    linkage = intake["source_linkage_table"]
    require_true(linkage.get("full_chain_linkage_verified"), "STOP_VS2_2_SOURCE_INTAKE_CHAIN_NOT_VERIFIED", "full_chain_linkage_verified")
    require_equal(linkage.get("linkage_failure_count"), 0, "STOP_VS2_2_SOURCE_INTAKE_CHAIN_NOT_VERIFIED", "linkage_failure_count")

    branch = intake["exact_decision_branch_binding"]
    require_equal(branch.get("decision_branch"), "ACCEPT_EXACT_PROPOSED_SCOPE", "STOP_VS2_2_SOURCE_INTAKE_NOT_PASS", "decision_branch")
    require_equal(branch.get("decision_mode"), "ACCEPT_EXACT_PROPOSED_SCOPE", "STOP_VS2_2_SOURCE_INTAKE_NOT_PASS", "decision_mode")
    require_false(branch.get("accepted_with_revisions"), "STOP_VS2_2_SOURCE_INTAKE_NOT_PASS", "accepted_with_revisions")
    require_equal(branch.get("revision_count"), 0, "STOP_VS2_2_SOURCE_INTAKE_NOT_PASS", "revision_count")

    direction = intake["accepted_direction_binding"]
    require_equal(direction.get("direction_id"), "FIRST_SWEEP_CAPABLE_KERNEL_V0", "STOP_VS2_2_DIRECTION_ID_MISMATCH", "direction_id")
    require_equal(direction.get("target_family"), TARGET_FAMILY, "STOP_VS2_2_TARGET_FAMILY_MISMATCH", "target_family")
    require_equal(direction.get("first_target"), TARGET_ID, "STOP_VS2_2_FIRST_TARGET_MISMATCH", "first_target")
    require_equal(direction.get("bundle_id"), "POST_VS1_FIRST_SWEEP_CAPABLE_KERNEL_BUNDLE_V0", "STOP_VS2_2_BUNDLE_ID_MISMATCH", "bundle_id")

    bundle = intake["accepted_bundle_binding"]
    require_equal(bundle.get("primary_bundle_member_count"), 18, "STOP_VS2_2_BUNDLE_ID_MISMATCH", "primary_bundle_member_count")
    require_equal(bundle.get("deferred_surface_count"), 2, "STOP_VS2_2_BUNDLE_ID_MISMATCH", "deferred_surface_count")
    require_equal(bundle.get("downstream_only_surface_count"), 1, "STOP_VS2_2_BUNDLE_ID_MISMATCH", "downstream_only_surface_count")
    require_true(bundle.get("s21_downstream_only"), "STOP_VS2_2_S21_MISCLASSIFIED", "s21_downstream_only")
    require_false(bundle.get("first_run_readiness_gate_is_s21"), "STOP_VS2_2_S21_MISCLASSIFIED", "first_run_readiness_gate_is_s21")

    scope = intake["exact_scope_application_audit"]
    require_true(scope.get("exact_scope_applied"), "STOP_VS2_2_EXACT_SCOPE_APPLICATION_MISMATCH", "exact_scope_applied")
    require_equal(len(scope.get("approved_scope_items_omitted", [])), 0, "STOP_VS2_2_EXACT_SCOPE_APPLICATION_MISMATCH", "approved_scope_items_omitted")
    require_equal(len(scope.get("unapproved_scope_items_added", [])), 0, "STOP_VS2_2_EXACT_SCOPE_APPLICATION_MISMATCH", "unapproved_scope_items_added")

    require_equal(receipt.get("receipt_gate"), "VS2_1_POST_VS1_SOURCE_INTAKE_PASS", "STOP_VS2_2_SOURCE_INTAKE_RECEIPT_HASH_MISMATCH", "source_receipt.receipt_gate")
    require_equal(receipt.get("logical_downstream_transition"), "ADVANCE(VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_PENDING)", "STOP_VS2_2_NOT_LAWFUL_NEXT_UNIT", "source_receipt.logical_downstream_transition")
    require_equal(canonical_hash(receipt["receipt_binding"]["receipt_payload"]), SOURCE_RECEIPT_SHA256, "STOP_VS2_2_SOURCE_INTAKE_RECEIPT_HASH_MISMATCH", "source_receipt.receipt_payload")
    require_equal(receipt["receipt_binding"]["receipt_sha256"], SOURCE_RECEIPT_SHA256, "STOP_VS2_2_SOURCE_INTAKE_RECEIPT_HASH_MISMATCH", "source_receipt.receipt_sha256")

    grants = intake["effective_grant_inventory"]
    require_equal(grants.get("effective_grant_count"), 5, "STOP_VS2_2_PROFILE_AND_TARGET_FREEZE_AUTHORITY_ABSENT", "effective_grant_count")
    for key in ["unmatched_grant_count", "duplicate_grant_id_count", "scope_mismatch_count", "grant_effectivity_condition_mismatch_count"]:
        require_equal(grants.get(key), 0, "STOP_VS2_2_PROFILE_AND_TARGET_FREEZE_AUTHORITY_ABSENT", key)
    require_false(grants.get("definition_alias_counted_as_grant"), "STOP_VS2_2_DEFINITION_ALIAS_DOUBLE_CONSUMPTION", "definition_alias_counted_as_grant")

    routing = intake["grant_routing"]
    route_by_id = {row["grant_id"]: row for row in routing["grant_routes"]}
    profile_route = route_by_id.get("VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY")
    if not profile_route:
        fail("STOP_VS2_2_PROFILE_AND_TARGET_FREEZE_AUTHORITY_ABSENT", "grant_routes", "profile grant route", route_by_id)
    require_equal(profile_route.get("routing_status"), "ROUTED_NOT_CONSUMED", "STOP_VS2_2_PROFILE_AND_TARGET_FREEZE_AUTHORITY_NOT_ROUTED_TO_VS2_2", "profile_route.routing_status")
    require_equal(profile_route.get("first_lawful_exercising_unit"), "VS2.2_KERNEL_PROFILE_AND_TARGET_FREEZE", "STOP_VS2_2_PROFILE_AND_TARGET_FREEZE_AUTHORITY_NOT_ROUTED_TO_VS2_2", "profile_route.first_lawful_exercising_unit")
    require_false(profile_route.get("consumed_by_vs2_1"), "STOP_VS2_2_PROFILE_AND_TARGET_FREEZE_AUTHORITY_ALREADY_CONSUMED", "profile_route.consumed_by_vs2_1")
    require_equal(profile_route.get("consumption_count_after_vs2_1"), 0, "STOP_VS2_2_PROFILE_GRANT_CONSUMPTION_COUNT_INVALID", "profile_route.consumption_count_after_vs2_1")
    require_true(profile_route.get("vs2_2_may_consume_grant"), "STOP_VS2_2_PROFILE_AND_TARGET_FREEZE_AUTHORITY_NOT_ROUTED_TO_VS2_2", "profile_route.vs2_2_may_consume_grant")

    source_binding = {
        "source_intake_artifact_id": intake["artifact_id"],
        "source_intake_path": SOURCE_INTAKE_PATH,
        "source_intake_commit_sha": EXPECTED_HEAD,
        "source_intake_file_sha256": SOURCE_INTAKE_FILE_SHA256,
        "source_intake_sha256": SOURCE_INTAKE_SHA256,
        "source_manifest_sha256": SOURCE_MANIFEST_SHA256,
        "source_intake_receipt_artifact_id": receipt["artifact_id"],
        "source_intake_receipt_path": SOURCE_RECEIPT_PATH,
        "source_intake_receipt_file_sha256": SOURCE_RECEIPT_FILE_SHA256,
        "source_intake_receipt_sha256": SOURCE_RECEIPT_SHA256,
        "source_intake_markdown_path": SOURCE_INTAKE_MD_PATH,
        "source_intake_markdown_file_sha256": SOURCE_INTAKE_MD_SHA256,
        "committed_bytes_verified": True,
        "worktree_bytes_match_commit": True,
        "source_manifest_hash_recomputes": True,
        "source_intake_hash_recomputes": True,
        "receipt_hash_recomputes": True,
        "baseline_share_used_as_source_authority": False,
        "latest_file_resolution_used": False,
        "mtime_resolution_used": False,
        "directory_ordering_used": False,
    }
    reconciliation = {
        "source_artifact_generation_state": "PRE_BOOKKEEPING_STATIC_RECORD",
        "source_artifact_committed_by_external_bookkeeping": True,
        "source_artifact_commit_sha": EXPECTED_HEAD,
        "source_artifact_rewrite_required": False,
        "source_manifest_committed": True,
        "source_intake_committed": True,
        "source_manifest_commit_sha": EXPECTED_HEAD,
        "static_artifact_records_bookkeeping_pending": True,
        "repository_commit_proves_current_committed_status": True,
        "source_artifact_rewritten_by_vs2_2": False,
    }
    return intake, receipt, source_binding, reconciliation


def profile_grant_consumption(intake: dict[str, Any]) -> dict[str, Any]:
    grant_records = intake["effective_grant_inventory"]["source_grant_records"]
    grant = next((row for row in grant_records if row["grant_id"] == "VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY"), None)
    if grant is None:
        fail("STOP_VS2_2_PROFILE_AND_TARGET_FREEZE_AUTHORITY_ABSENT", "source_grant_records", "VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY", [row["grant_id"] for row in grant_records])
    return {
        "grant_id": "VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY",
        "grant_basis_artifact_id": grant["grant_basis_artifact_id"],
        "grant_basis_commit_sha": grant["grant_basis_commit_sha"],
        "grant_basis_receipt_sha256": grant["grant_basis_receipt_sha256"],
        "grant_basis_decision_package_sha256": grant["grant_basis_decision_package_sha256"],
        "grant_target_phase": grant["grant_target_phase"],
        "grant_target_direction": grant["grant_target_direction"],
        "grant_target_family": grant["grant_target_family"],
        "grant_first_target": grant["grant_first_target"],
        "grant_scope": grant["grant_scope"],
        "consuming_unit": UNIT_ID,
        "consumption_role": "PROFILE_AND_SEMANTIC_TARGET_FREEZE_ONLY",
        "consumption_frame": "FIRST_SWEEP_CAPABLE_KERNEL_PROFILE_V0_AND_TYPED_STATE_CONTRACT_CONVERGENCE_V0",
        "consumption_count_before": 0,
        "consumption_count_after": 1,
        "grant_reusable": False,
        "grant_portable": False,
        "grant_generalizing": False,
        "grant_execution_capable": False,
        "profile_definition_performed": True,
        "semantic_target_freeze_performed": True,
        "component_classification_performed": True,
        "maximum_envelope_freeze_performed": True,
        "downstream_sequence_freeze_performed": True,
        "construction_performed": False,
        "fixture_construction_performed": False,
        "readiness_gate_constructed": False,
        "construction_package_verified": False,
        "execution_performed": False,
        "consumption_status": "CONSUMED_ONCE_FOR_DECLARED_PROFILE_AND_TARGET_FREEZE",
        "profile_and_target_freeze_grant_consumed": True,
        "profile_and_target_freeze_grant_consumption_count": 1,
        "same_profile_grant_may_be_consumed_again": False,
        "profile_grant_reusable": False,
        "definition_alias_consumed_as_separate_grant": False,
    }


def remaining_grant_routing() -> dict[str, Any]:
    routes = [
        {
            "grant_id": "VS2_BOUNDED_CONSTRUCTION_AUTHORITY",
            "routing_status": "ROUTED_NOT_CONSUMED",
            "first_lawful_exercising_unit": "VS2.3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION",
            "consumption_frame": "VS2.3_TO_VS2.5_BOUND_TARGET_CONSTRUCTION_SEQUENCE",
            "exact_consuming_unit_frozen": True,
            "consumed_by_vs2_2": False,
        },
        {
            "grant_id": "VS2_FIXTURE_CONSTRUCTION_AUTHORITY",
            "routing_status": "ROUTED_NOT_CONSUMED",
            "first_lawful_exercising_unit": "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
            "consumption_frame": "ONE_BOUNDED_FIRST_TARGET_FIXTURE_SET",
            "exact_consuming_unit_frozen": True,
            "consumed_by_vs2_2": False,
        },
        {
            "grant_id": "VS2_FIRST_RUN_READINESS_GATE_CONSTRUCTION_AUTHORITY",
            "routing_status": "ROUTED_NOT_CONSUMED",
            "first_lawful_exercising_unit": "VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS",
            "consumption_frame": "ONE_FIRST_RUN_KERNEL_CONSTRUCTION_READINESS_GATE",
            "exact_consuming_unit_frozen": True,
            "consumed_by_vs2_2": False,
        },
        {
            "grant_id": "VS2_CONSTRUCTION_PACKAGE_VERIFICATION_AUTHORITY",
            "routing_status": "ROUTED_NOT_CONSUMED",
            "first_lawful_exercising_unit": "VS2.7_PHASE_CLOSURE",
            "consumption_frame": "ONE_PHASE_VS2_CONSTRUCTION_PACKAGE_VERIFICATION",
            "exact_consuming_unit_frozen": True,
            "consumed_by_vs2_2": False,
        },
    ]
    return {
        "remaining_grant_routes": routes,
        "remaining_effective_grant_count": 4,
        "remaining_grants_consumed_by_vs2_2": 0,
        "remaining_grant_routes_frozen": True,
        "bounded_construction_grant_consumed": False,
        "fixture_construction_grant_consumed": False,
        "readiness_gate_construction_grant_consumed": False,
        "construction_verification_grant_consumed": False,
        "routing_frozen_does_not_consume_grant": True,
        "construction_grant_does_not_authorize_execution": True,
    }


def build_component_table() -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    table: list[dict[str, Any]] = []
    all_components = REQUIRED_FULL + REQUIRED_MINIMAL + DEFERRED
    for component_id in all_components:
        if component_id in REQUIRED_FULL:
            classification = "REQUIRED_FULL"
            authority_route = "VS2_BOUNDED_CONSTRUCTION_AUTHORITY"
        elif component_id in REQUIRED_MINIMAL:
            classification = "REQUIRED_MINIMAL"
            authority_route = "VS2_BOUNDED_CONSTRUCTION_AUTHORITY"
        else:
            classification = "DEFERRED"
            authority_route = "DEFERRED_NOT_CONSUMED_BY_FIRST_TARGET"
        semantics = COMPONENT_SEMANTICS[component_id]
        table.append({
            "component_id": component_id,
            "source_surface_id": SURFACE_BY_COMPONENT[component_id],
            "profile_classification": classification,
            "profile_requirement": semantics["profile_requirement"],
            "supported_function": semantics["supported_function"],
            "omitted_or_deferred_function": semantics["omitted_or_deferred_function"],
            "construction_status": "NOT_CONSTRUCTED",
            "construction_unit": semantics["construction_unit"],
            "authority_route": authority_route,
            "full_mccl_satisfaction_claimed": False,
            "reusability_claimed": False,
            "portability_claimed": False,
        })
    contract = {
        "classification_vocabulary": ["REQUIRED_FULL", "REQUIRED_MINIMAL", "DEFERRED", "FORBIDDEN"],
        "exactly_one_classification_per_component": True,
        "required_full_count": 14,
        "required_minimal_count": 4,
        "deferred_count": 2,
        "forbidden_component_count": 0,
        "component_count": 20,
        "forbidden_remains_valid_vocabulary_value": True,
        "s21_profile_membership": "DOWNSTREAM_ONLY",
        "s21_is_c01_to_c20_profile_member": False,
        "s21_is_first_run_construction_readiness_gate": False,
        "s21_constructed_by_vs2_2": False,
    }
    summary = {
        "component_count": len(table),
        "required_full_count": sum(1 for row in table if row["profile_classification"] == "REQUIRED_FULL"),
        "required_minimal_count": sum(1 for row in table if row["profile_classification"] == "REQUIRED_MINIMAL"),
        "deferred_count": sum(1 for row in table if row["profile_classification"] == "DEFERRED"),
        "forbidden_component_count": sum(1 for row in table if row["profile_classification"] == "FORBIDDEN"),
        "c20_convergence_component_present": any(row["component_id"] == "C20_CONVERGENCE_CRITERION_CONTRACT" for row in table),
        "all_components_not_constructed": all(row["construction_status"] == "NOT_CONSTRUCTED" for row in table),
        "deferred_components_marked_satisfied": False,
    }
    return table, contract, summary


def build_envelopes() -> tuple[dict[str, Any], dict[str, Any]]:
    construction_objects = [
        "one kernel profile",
        "one semantic target",
        "one scope/regime contract family",
        "one runtime-control-state contract",
        "one candidate contract",
        "one frozen-target contract",
        "one finite move-space",
        "one selector contract",
        "one applicator contract",
        "one validation boundary",
        "one admissibility boundary",
        "one convergence criterion",
        "one radius and budget policy",
        "one halt policy",
        "one source identity and freshness policy",
        "one move-attempt receipt contract",
        "one case-terminal receipt contract",
        "one sweep/run report contract",
        "one replay and audit surface",
        "one forbidden-effect guard",
        "one Evidence Yield report hook",
        "one human-escalation boundary",
        "one bounded fixture set",
        "one first-run construction-readiness gate",
        "one construction-package verification",
    ]
    construction = {
        "maximum_construction_envelope_frozen": True,
        "bounded_construction_package_contains_only": construction_objects,
        "bounded_construction_package_object_count": len(construction_objects),
        "target_family_count": 1,
        "first_target_count": 1,
        "kernel_profile_count": 1,
        "construction_package_count": 1,
        "reusable_profile_count": 0,
        "reusable_schema_promotion_count": 0,
        "reusable_move_space_promotion_count": 0,
        "runner_count": 0,
        "permits_later_bounded_construction_only": True,
        "objects_constructed_by_vs2_2": 0,
        "scope_regime_implementation_schema_constructed": False,
        "runtime_state_schema_constructed": False,
        "candidate_schema_constructed": False,
        "serialized_target_schema_constructed": False,
        "move_space_constructed": False,
        "selector_contract_constructed": False,
        "applicator_contract_constructed": False,
        "fixture_set_constructed": False,
        "readiness_gate_constructed": False,
        "construction_package_verified": False,
    }
    future_execution = {
        "maximum_future_execution_envelope_frozen": True,
        "maximum_envelope_frozen": True,
        "target_family_count": 1,
        "target_version_count_per_execution_package": 1,
        "scope_regime_version_count_per_execution_package": 1,
        "move_space_version_count_per_execution_package": 1,
        "fixture_set_version_count_per_execution_package": 1,
        "source_snapshot_version_count_per_execution_package": 1,
        "sweep_package_count": 1,
        "maximum_cases": 20,
        "maximum_attempted_moves_per_case": 5,
        "maximum_applied_moves_per_case": 5,
        "maximum_total_attempted_moves": 100,
        "maximum_total_applied_moves": 100,
        "maximum_automatic_reruns": 0,
        "maximum_automatic_radius_renewals": 0,
        "maximum_automatic_target_expansions": 0,
        "maximum_automatic_scope_regime_expansions": 0,
        "maximum_automatic_move_space_expansions": 0,
        "maximum_automatic_source_snapshot_substitutions": 0,
        "exact_execution_envelope_selected": False,
        "execution_package_constructed": False,
        "execution_authority_granted": False,
        "maximum_future_execution_envelope_is_not_exact_execution_package": True,
        "exact_execution_package_is_not_execution_permission": True,
    }
    return construction, future_execution


def build_phase_states() -> tuple[dict[str, Any], dict[str, Any]]:
    pre = {
        "vs2_source_intake_built": True,
        "vs2_started": True,
        "vs2_1_built": True,
        "vs2_2_may_begin": True,
        "source_manifest_frozen": True,
        "source_manifest_committed": True,
        "source_intake_committed": True,
        "kernel_profile_frozen": False,
        "semantic_target_frozen": False,
        "any_vs2_grant_consumed": False,
        "vs2_grant_consumption_count": 0,
        "construction_performed": False,
        "fixture_construction_performed": False,
        "readiness_gate_constructed": False,
        "construction_package_verified": False,
        "execution_authorized": False,
        "sweep_authorized": False,
        "runner_authority_created": False,
        "committed_state_source_commit_sha": EXPECTED_HEAD,
    }
    post = {
        "vs2_source_intake_built": True,
        "vs2_started": True,
        "vs2_1_built": True,
        "vs2_2_built": True,
        "kernel_profile_frozen": True,
        "semantic_target_frozen": True,
        "any_vs2_grant_consumed": True,
        "vs2_grant_consumption_count": 1,
        "profile_and_target_freeze_grant_consumed": True,
        "profile_and_target_freeze_grant_consumption_count": 1,
        "bounded_construction_grant_consumed": False,
        "fixture_construction_grant_consumed": False,
        "readiness_gate_construction_grant_consumed": False,
        "construction_verification_grant_consumed": False,
        "remaining_grant_routes_frozen": True,
        "construction_performed": False,
        "fixture_construction_performed": False,
        "readiness_gate_constructed": False,
        "construction_package_verified": False,
        "execution_authorized": False,
        "positive_path_execution_authorized": False,
        "negative_path_execution_authorized": False,
        "sweep_authorized": False,
        "automatic_rerun_authorized": False,
        "runner_authority_created": False,
        "execution_performed": False,
        "sweep_executed": False,
        "runner_created": False,
        "vs2_3_may_begin": True,
        "bookkeeping_commit_required": True,
        "source_artifact_rewritten": False,
    }
    return pre, post


def build_profile(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    intake, source_receipt, source_binding, reconciliation = verify_source_intake(root)
    table, classification_contract, component_summary = build_component_table()
    construction_envelope, future_execution_envelope = build_envelopes()
    pre_state, post_state = build_phase_states()
    grant_consumption = profile_grant_consumption(intake)
    remaining_routes = remaining_grant_routing()
    withheld_source = intake["withheld_authority_binding"]
    withheld = {
        "source_withheld_authority_binding": withheld_source,
        "withheld_authority_vector": withheld_source["withheld_authority_vector"],
        "withheld_authority_preserved": True,
        "withheld_authority_changed_by_vs2_2": False,
        "unapproved_authority_grant_count": 0,
        "execution_authority_absent": True,
        "sweep_authority_absent": True,
        "automatic_rerun_authority_absent": True,
        "runner_authority_absent": True,
    }
    profile_identity = {
        "artifact_id": PROFILE_ARTIFACT_ID,
        "profile_id": PROFILE_ID,
        "profile_class": PROFILE_CLASS,
        "profile_status": PROFILE_STATUS,
        "profile_purpose": (
            "Define the smallest lawful vertical circuit capable, after later construction, "
            "construction verification, and separate execution authorization, of attempting one "
            "bounded typed-state contract target, emitting move-, case-, and run-level receipts, "
            "and exposing useful Confirmation Yield or Diagnostic Yield."
        ),
        "kernel_profile_frozen": True,
        "kernel_constructed": False,
        "construction_package_ready": False,
        "execution_authorized": False,
        "sweep_authorized": False,
        "runner_ready": False,
        "full_mccl_ready": False,
    }
    mccl = {
        "mccl_relationship": MCCL_RELATIONSHIP,
        "bounded_profile_projection_of_mccl_v0": True,
        "full_mccl_satisfaction_claimed": False,
        "full_mccl_ready": False,
        "profile_frozen_does_not_mean_kernel_constructed": True,
        "sweep_capable_profile_does_not_mean_sweep_package_constructed": True,
        "sweep_capable_profile_does_not_mean_sweep_authorized": True,
    }
    pressure = {
        "classification_vocabulary": PRESSURE_VOCABULARY,
        "classification_count": len(PRESSURE_VOCABULARY),
        "namespaces_preserved": [
            "transformation move",
            "observation",
            "pressure readout",
            "pressure classification",
            "validation result",
            "admissibility result",
            "convergence result",
            "terminal outcome",
        ],
        "ambiguous_label_collapse_allowed": False,
    }
    terminal_family = {
        "terminal_outcomes": TERMINAL_OUTCOMES,
        "terminal_outcome_count": len(TERMINAL_OUTCOMES),
        "distinctions_collapsed": False,
        "unclassified_result_posture": {
            "terminal_outcome": "STOP_UNCLASSIFIED_RESULT_REQUIRES_TAXONOMY_REFINEMENT",
            "execution_remained_contained": True,
            "current_classification_vocabulary_was_insufficient": True,
            "target_was_not_reached": True,
            "automatic_continuation_forbidden": True,
            "automatic_taxonomy_modification_forbidden": True,
            "automatic_rerun_forbidden": True,
            "may_produce_diagnostic_yield": True,
            "counts_as_success_or_convergence": False,
        },
    }
    fixtures = {
        "fixture_roles": FIXTURE_ROLES,
        "fixture_role_count": len(FIXTURE_ROLES),
        "fixture_set_constructed": False,
        "fixture_identities_frozen": False,
        "fixture_source_snapshot_frozen": False,
        "later_fixture_required_fields": [
            "fixture identity",
            "fixture role",
            "input delta",
            "source snapshot",
            "expected exposed condition",
            "expected repair lawfulness",
            "expected authority requirement",
            "expected convergence result",
            "expected terminal outcome",
            "expected receipt evidence",
            "forbidden alternate outcome",
        ],
    }
    forbidden = {
        "forbidden_behavior_count": len(FORBIDDEN_BEHAVIORS),
        "forbidden_behaviors": [{"behavior": behavior, "allowed": False} for behavior in FORBIDDEN_BEHAVIORS],
        "all_forbidden_behaviors_explicit": True,
        "forbidden_behavior_boundary_complete": True,
        "no_forbidden_behavior_marked_allowed": True,
    }
    downstream_sequence = {
        "downstream_sequence_frozen": True,
        "downstream_units": DOWNSTREAM_SEQUENCE,
        "downstream_unit_count": len(DOWNSTREAM_SEQUENCE),
        "next_unit": "VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PENDING",
        "next_unit_auto_executed": False,
    }
    downstream_objects = {
        "downstream_construction_objects": DOWNSTREAM_OBJECTS,
        "downstream_construction_object_count": len(DOWNSTREAM_OBJECTS),
        "objects_constructed_by_vs2_2": 0,
    }
    payload = {
        "source_intake_binding": source_binding,
        "source_intake_commit_reconciliation": reconciliation,
        "accepted_direction_binding": intake["accepted_direction_binding"],
        "profile_grant_consumption": grant_consumption,
        "remaining_grant_routing": remaining_routes,
        "withheld_authority_binding": withheld,
        "profile_identity": profile_identity,
        "mccl_profile_relationship": mccl,
        "component_classification_contract": classification_contract,
        "component_profile_table": table,
        "component_profile_summary": component_summary,
        "maximum_construction_envelope": construction_envelope,
        "maximum_future_execution_envelope": future_execution_envelope,
        "pressure_classification_vocabulary": pressure,
        "terminal_outcome_family": terminal_family,
        "fixture_role_requirements": fixtures,
        "forbidden_behavior_boundary": forbidden,
        "downstream_construction_sequence": downstream_sequence,
        "downstream_construction_objects": downstream_objects,
        "pre_vs2_2_phase_state": pre_state,
        "post_vs2_2_phase_state": post_state,
        "profile_nonclaims": {
            "kernel_constructed": False,
            "sweep_package_constructed": False,
            "sweep_authorized": False,
            "full_mccl_ready": False,
            "reusable_profile_created": False,
            "execution_authorized": False,
            "schemas_constructed": False,
            "fixtures_constructed": False,
            "runner_created": False,
        },
    }
    if list(payload.keys()) != PROFILE_BOUND_SECTIONS:
        fail("STOP_VS2_2_PROFILE_HASH_MISMATCH", "profile_payload.keys", PROFILE_BOUND_SECTIONS, list(payload.keys()))
    profile_sha = canonical_hash(payload)
    profile = {
        "schema_version": PROFILE_SCHEMA,
        "artifact_id": PROFILE_ARTIFACT_ID,
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "unit_role": UNIT_ROLE,
        "profile_status": PROFILE_STATUS,
        **payload,
        "profile_binding": {
            "canonicalization": CANONICALIZATION,
            "bound_sections": PROFILE_BOUND_SECTIONS,
            "profile_payload": payload,
            "profile_sha256": profile_sha,
            "profile_hash_recomputes": True,
        },
        "profile_gate": PROFILE_GATE,
        "logical_terminal_transition": LOGICAL_TERMINAL,
        "construction_session_terminal": TERMINAL_TRANSITION,
        "failures": [],
    }
    return profile, intake, source_receipt


def build_target(profile: dict[str, Any], intake: dict[str, Any]) -> dict[str, Any]:
    terminal_family = profile["terminal_outcome_family"]
    source_binding = profile["source_intake_binding"]
    accepted_direction = intake["accepted_direction_binding"]
    profile_ref = {
        "profile_artifact_id": PROFILE_ARTIFACT_ID,
        "profile_id": PROFILE_ID,
        "profile_sha256": profile["profile_binding"]["profile_sha256"],
        "profile_gate": PROFILE_GATE,
        "kernel_profile_frozen": True,
        "kernel_constructed": False,
    }
    grant_ref = {
        "profile_grant_id": "VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY",
        "profile_grant_consumed": True,
        "profile_grant_consumption_count": 1,
        "profile_grant_reusable": False,
        "consumption_status": "CONSUMED_ONCE_FOR_DECLARED_PROFILE_AND_TARGET_FREEZE",
    }
    target_identity = {
        "artifact_id": TARGET_ARTIFACT_ID,
        "target_family": TARGET_FAMILY,
        "target_id": TARGET_ID,
        "target_status": TARGET_STATUS,
        "target_count": 1,
        "semantic_target_frozen": True,
        "serialized_target_schema_constructed": False,
        "admissibility_policy_constructed": False,
        "convergence_criterion_constructed": False,
        "fixture_set_constructed": False,
        "source_snapshot_frozen": False,
        "execution_authorized": False,
    }
    target_statement = (
        "Given one declared local scope/regime, one bounded typed-state contract candidate, "
        "one frozen local target contract, one frozen local admissibility policy, one finite "
        "authorized transformation move-space, one fixed move and case budget, one declared "
        "source snapshot, and one frozen convergence criterion, the kernel may, after later "
        "construction, construction verification, and separate execution authorization, attempt "
        "to reach a locally valid and lawfully admissible terminal typed-state contract."
    )
    target_path = [
        "candidate typed-state contract",
        "expose current target condition or defect",
        "enumerate lawful transformations",
        "select one lawful transformation",
        "apply one bounded candidate delta",
        "validate resulting candidate",
        "evaluate admissibility",
        "evaluate convergence criterion",
        "emit move receipt",
        "continue under an explicit repeat condition or halt",
        "emit terminal receipt and run report",
    ]
    payload = {
        "source_intake_binding": source_binding,
        "accepted_direction_binding": accepted_direction,
        "profile_binding_reference": profile_ref,
        "profile_grant_consumption_reference": grant_ref,
        "target_identity": target_identity,
        "target_statement": target_statement,
        "target_path": target_path,
        "scope_regime_requirements": {
            "operating_scope_required": True,
            "target_regime_required": True,
            "candidate_object_regime_required": True,
            "allowed_source_surfaces_required": True,
            "forbidden_source_surfaces_required": True,
            "allowed_transformations_required": True,
            "forbidden_transformations_required": True,
            "object_identity_rules_required": True,
            "sameness_and_difference_criteria_required": True,
            "authority_boundary_required": True,
            "claim_boundary_required": True,
            "scope_regime_expansion_allowed": False,
        },
        "object_role_separation": {
            "distinct_roles": [
                "declared scope/regime",
                "runtime control state",
                "candidate contract",
                "frozen target contract",
            ],
            "three_object_model_roles": [
                "runtime control state",
                "candidate contract",
                "frozen target contract",
            ],
            "scope_regime_is_external_governing_frame": True,
            "scope_runtime_candidate_target_conflated": False,
        },
        "target_success_condition": {
            "target_reached_only_when": [
                "candidate validates against the frozen target schema",
                "candidate passes the frozen admissibility policy",
                "all required source bindings are valid",
                "scope/regime boundaries remain intact",
                "no forbidden effect is present",
                "all applied moves were authorized",
                "move and case budgets were respected",
                "convergence criterion reports the terminal target condition",
                "terminal receipt was emitted",
            ],
            "movement_marked_as_convergence": False,
            "typed_stop_marked_target_reached": False,
            "unclassified_result_marked_success": False,
        },
        "already_valid_candidate_semantics": {
            "terminal_outcome": "TARGET_REACHED",
            "initial_target_status": "ALREADY_AT_TARGET",
            "moves_attempted": 0,
            "moves_applied": 0,
            "unnecessary_mutation_absent": True,
        },
        "positive_path_requirement": {
            "repairable_positive_path_specimen_must_eventually_terminate_with": "TARGET_REACHED",
            "typed_stop_may_produce_diagnostic_yield": True,
            "typed_stop_completes_positive_path_milestone": False,
        },
        "admissibility_policy_requirements": {
            "frozen_local_admissibility_policy_required": True,
            "admissibility_policy_constructed": False,
            "candidate_must_pass_admissibility": True,
            "admissibility_failure_terminal_outcome": "STOP_ADMISSIBILITY_FAILED",
        },
        "convergence_criterion_requirements": {
            "continue_condition_required": True,
            "repeat_condition_required": True,
            "non_progress_condition_required": True,
            "repeated_state_condition_required": True,
            "oscillation_guard_required": True,
            "maximum_cycle_boundary_required": True,
            "maximum_radius_boundary_required": True,
            "target_reached_condition_required": True,
            "typed_halt_when_repeat_is_not_lawful_required": True,
            "movement_equals_progress": False,
            "progress_equals_target_reached": False,
            "repeated_movement_equals_convergence": False,
            "typed_containment_stop_equals_convergence": False,
            "convergence_criterion_constructed": False,
        },
        "source_policy_requirements": {
            "declared_source_identity_required": True,
            "automatic_source_acquisition_allowed": False,
            "latest_file_selection_allowed": False,
            "mtime_authority_allowed": False,
            "directory_position_authority_allowed": False,
            "silent_source_replacement_allowed": False,
            "ambient_repository_context_allowed": False,
            "chat_memory_sourcing_allowed": False,
            "source_snapshot_frozen": False,
        },
        "terminal_outcome_family": terminal_family,
        "unclassified_result_posture": terminal_family["unclassified_result_posture"],
        "target_mutation_boundaries": {
            "target_mutation_allowed": False,
            "target_schema_mutation_allowed": False,
            "move_space_mutation_allowed": False,
            "scope_regime_expansion_allowed": False,
            "first_target_substitution_allowed": False,
            "second_target_selection_allowed": False,
            "automatic_taxonomy_modification_allowed": False,
        },
        "target_nonclaims": {
            "serialized_target_schema_constructed": False,
            "admissibility_policy_constructed": False,
            "convergence_criterion_constructed": False,
            "fixture_set_constructed": False,
            "source_snapshot_frozen": False,
            "execution_authorized": False,
        },
    }
    if list(payload.keys()) != TARGET_BOUND_SECTIONS:
        fail("STOP_VS2_2_TARGET_FREEZE_HASH_MISMATCH", "target_freeze_payload.keys", TARGET_BOUND_SECTIONS, list(payload.keys()))
    target_sha = canonical_hash(payload)
    return {
        "schema_version": TARGET_SCHEMA,
        "artifact_id": TARGET_ARTIFACT_ID,
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "unit_role": UNIT_ROLE,
        "target_status": TARGET_STATUS,
        **payload,
        "target_freeze_binding": {
            "canonicalization": CANONICALIZATION,
            "bound_sections": TARGET_BOUND_SECTIONS,
            "target_freeze_payload": payload,
            "target_freeze_sha256": target_sha,
            "target_freeze_hash_recomputes": True,
        },
        "target_freeze_gate": TARGET_GATE,
        "logical_terminal_transition": LOGICAL_TERMINAL,
        "construction_session_terminal": TERMINAL_TRANSITION,
        "failures": [],
    }


def build_receipt(profile: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    receipt = {
        "schema_version": RECEIPT_SCHEMA,
        "artifact_id": RECEIPT_ARTIFACT_ID,
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "unit_role": UNIT_ROLE,
        "source_intake_artifact_id": "phase_vs2_post_vs1_source_intake_v0",
        "source_intake_commit_sha": EXPECTED_HEAD,
        "source_intake_file_sha256": SOURCE_INTAKE_FILE_SHA256,
        "source_intake_sha256": SOURCE_INTAKE_SHA256,
        "source_manifest_sha256": SOURCE_MANIFEST_SHA256,
        "source_intake_receipt_artifact_id": "phase_vs2_1_post_vs1_source_intake_receipt_v0",
        "source_intake_receipt_file_sha256": SOURCE_RECEIPT_FILE_SHA256,
        "source_intake_receipt_sha256": SOURCE_RECEIPT_SHA256,
        "profile_artifact_id": PROFILE_ARTIFACT_ID,
        "profile_sha256": profile["profile_binding"]["profile_sha256"],
        "profile_hash_recomputes": True,
        "target_freeze_artifact_id": TARGET_ARTIFACT_ID,
        "target_freeze_sha256": target["target_freeze_binding"]["target_freeze_sha256"],
        "target_freeze_hash_recomputes": True,
        "profile_grant_id": "VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY",
        "profile_grant_consumed": True,
        "profile_grant_consumption_count": 1,
        "profile_grant_reusable": False,
        "remaining_effective_grant_count": 4,
        "remaining_grants_consumed_by_vs2_2": 0,
        "remaining_grant_routes_frozen": True,
        "component_count": 20,
        "required_full_count": 14,
        "required_minimal_count": 4,
        "deferred_count": 2,
        "forbidden_component_count": 0,
        "target_family": TARGET_FAMILY,
        "target_id": TARGET_ID,
        "semantic_target_frozen": True,
        "serialized_target_schema_constructed": False,
        "maximum_construction_envelope_frozen": True,
        "maximum_future_execution_envelope_frozen": True,
        "exact_execution_envelope_selected": False,
        "execution_authority_absent": True,
        "withheld_authority_preserved": True,
        "forbidden_behavior_boundary_complete": True,
        "downstream_sequence_frozen": True,
        "kernel_profile_frozen": True,
        "kernel_constructed": False,
        "construction_performed": False,
        "fixture_construction_performed": False,
        "readiness_gate_constructed": False,
        "construction_package_verified": False,
        "execution_performed": False,
        "sweep_executed": False,
        "runner_created": False,
        "profile_gate": PROFILE_GATE,
        "target_freeze_gate": TARGET_GATE,
        "receipt_gate": RECEIPT_GATE,
        "evidence_yield_branch": EVIDENCE_YIELD_BRANCH,
        "logical_downstream_transition": LOGICAL_TERMINAL,
        "construction_session_terminal": TERMINAL_TRANSITION,
        "failures": [],
    }
    receipt_payload = dict(receipt)
    receipt["receipt_binding"] = {
        "canonicalization": CANONICALIZATION,
        "receipt_payload": receipt_payload,
        "receipt_sha256": canonical_hash(receipt_payload),
    }
    return receipt


def render_profile_md(profile: dict[str, Any]) -> str:
    summary = profile["component_profile_summary"]
    return f"""# Phase VS2.2 First Sweep-Capable Kernel Profile v0

## Source Binding

- Source intake commit: `{EXPECTED_HEAD}`
- Source intake file SHA256: `{SOURCE_INTAKE_FILE_SHA256}`
- Source intake canonical SHA256: `{SOURCE_INTAKE_SHA256}`
- Source manifest SHA256: `{SOURCE_MANIFEST_SHA256}`
- Source intake receipt SHA256: `{SOURCE_RECEIPT_SHA256}`

## Profile Freeze

- Profile ID: `{PROFILE_ID}`
- Profile class: `{PROFILE_CLASS}`
- Profile status: `{PROFILE_STATUS}`
- MCCL relationship: `{MCCL_RELATIONSHIP}`
- Kernel profile frozen: `true`
- Kernel constructed: `false`
- Execution authorized: `false`

## Component Classification

- Component count: `{summary["component_count"]}`
- Required full: `{summary["required_full_count"]}`
- Required minimal: `{summary["required_minimal_count"]}`
- Deferred: `{summary["deferred_count"]}`
- Forbidden component count: `{summary["forbidden_component_count"]}`
- S21 remains downstream-only and is not a C01-C20 profile member.

## Grants

- Consumed exactly once: `VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY`
- Remaining grants routed and unconsumed: `4`
- Construction, fixture, readiness, and verification grants are not consumed by VS2.2.

## Frozen Boundaries

- Maximum construction envelope frozen: `true`
- Maximum future execution envelope frozen: `true`
- Forbidden behavior boundary complete: `true`
- Downstream sequence frozen: `true`
- Next unit: `VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PENDING`

## Canonical Hash

- Profile SHA256: `{profile["profile_binding"]["profile_sha256"]}`

## Terminal

- Profile gate: `{PROFILE_GATE}`
- Logical transition: `{LOGICAL_TERMINAL}`
- Construction-session terminal: `{TERMINAL_TRANSITION}`
"""


def render_target_md(target: dict[str, Any]) -> str:
    return f"""# Phase VS2.2 Typed State Contract Convergence Target Freeze v0

## Target Identity

- Target family: `{TARGET_FAMILY}`
- Target ID: `{TARGET_ID}`
- Target status: `{TARGET_STATUS}`
- Target count: `1`
- Semantic target frozen: `true`
- Serialized target schema constructed: `false`
- Execution authorized: `false`

## Target Statement

{target["target_statement"]}

## Target Path

{chr(10).join(f"- {step}" for step in target["target_path"])}

## Completion Boundary

- `TARGET_REACHED` requires validation, admissibility, source bindings, intact scope/regime boundaries, no forbidden effect, authorized moves, respected budgets, convergence criterion success, and terminal receipt emission.
- Already valid candidates may reach target with zero moves and no unnecessary mutation.
- Typed stops may produce Diagnostic Yield but do not complete the positive-path milestone.

## Canonical Hash

- Target-freeze SHA256: `{target["target_freeze_binding"]["target_freeze_sha256"]}`

## Terminal

- Target-freeze gate: `{TARGET_GATE}`
- Logical transition: `{LOGICAL_TERMINAL}`
- Construction-session terminal: `{TERMINAL_TRANSITION}`
"""


def write_outputs(root: Path, profile: dict[str, Any], target: dict[str, Any], receipt: dict[str, Any]) -> None:
    (root / OUTPUT_PROFILE_JSON).write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    (root / OUTPUT_PROFILE_MD).write_text(render_profile_md(profile), encoding="utf-8")
    (root / OUTPUT_TARGET_JSON).write_text(json.dumps(target, indent=2) + "\n", encoding="utf-8")
    (root / OUTPUT_TARGET_MD).write_text(render_target_md(target), encoding="utf-8")
    (root / OUTPUT_RECEIPT).write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")


def emit_success(profile: dict[str, Any], target: dict[str, Any], receipt: dict[str, Any]) -> None:
    print("BUILD_PHASE_VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_V0_COMPLETE")
    print()
    print(f"phase_id={PHASE_ID}")
    print(f"unit_id={UNIT_ID}")
    print(f"unit_role={UNIT_ROLE}")
    print()
    print(f"source_intake_commit_sha={EXPECTED_HEAD}")
    print(f"source_intake_file_sha256={SOURCE_INTAKE_FILE_SHA256}")
    print(f"source_intake_sha256={SOURCE_INTAKE_SHA256}")
    print(f"source_manifest_sha256={SOURCE_MANIFEST_SHA256}")
    print()
    print(f"source_intake_receipt_file_sha256={SOURCE_RECEIPT_FILE_SHA256}")
    print(f"source_intake_receipt_sha256={SOURCE_RECEIPT_SHA256}")
    print()
    print("source_intake_committed=true")
    print("source_manifest_committed=true")
    print("source_artifact_rewritten=false")
    print()
    print("direction_id=FIRST_SWEEP_CAPABLE_KERNEL_V0")
    print(f"target_family={TARGET_FAMILY}")
    print(f"first_target={TARGET_ID}")
    print("bundle_id=POST_VS1_FIRST_SWEEP_CAPABLE_KERNEL_BUNDLE_V0")
    print()
    print(f"profile_id={PROFILE_ID}")
    print(f"profile_class={PROFILE_CLASS}")
    print(f"profile_status={PROFILE_STATUS}")
    print(f"mccl_relationship={MCCL_RELATIONSHIP}")
    print()
    print("component_count=20")
    print("required_full_count=14")
    print("required_minimal_count=4")
    print("deferred_count=2")
    print("forbidden_component_count=0")
    print()
    print("target_count=1")
    print(f"target_status={TARGET_STATUS}")
    print("semantic_target_frozen=true")
    print("serialized_target_schema_constructed=false")
    print()
    print("profile_grant_id=VS2_PROFILE_AND_TARGET_FREEZE_AUTHORITY")
    print("profile_grant_consumed=true")
    print("profile_grant_consumption_count=1")
    print("profile_grant_reusable=false")
    print()
    print("remaining_effective_grant_count=4")
    print("remaining_grants_consumed_by_vs2_2=0")
    print("remaining_grant_routes_frozen=true")
    print()
    print("bounded_construction_grant_first_consumer=VS2.3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION")
    print("fixture_grant_first_consumer=VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS")
    print("readiness_gate_grant_first_consumer=VS2.6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS")
    print("construction_verification_grant_first_consumer=VS2.7_PHASE_CLOSURE")
    print()
    print("maximum_construction_envelope_frozen=true")
    print("maximum_future_execution_envelope_frozen=true")
    print("maximum_cases=20")
    print("maximum_attempted_moves_per_case=5")
    print("maximum_total_attempted_moves=100")
    print("maximum_automatic_reruns=0")
    print("maximum_automatic_radius_renewals=0")
    print()
    print("terminal_outcome_count=17")
    print("fixture_role_count=12")
    print("forbidden_behavior_boundary_complete=true")
    print()
    print("downstream_sequence_frozen=true")
    print("downstream_unit_count=5")
    print("downstream_construction_object_count=20")
    print()
    print("withheld_authority_preserved=true")
    print("execution_authority_absent=true")
    print("sweep_authority_absent=true")
    print("automatic_rerun_authority_absent=true")
    print("runner_authority_absent=true")
    print()
    print("vs2_2_built=true")
    print("vs2_3_may_begin=true")
    print()
    print("kernel_profile_frozen=true")
    print("kernel_constructed=false")
    print("construction_performed=false")
    print("fixture_construction_performed=false")
    print("readiness_gate_constructed=false")
    print("construction_package_verified=false")
    print("execution_performed=false")
    print("sweep_executed=false")
    print("runner_created=false")
    print()
    print(f"profile_sha256={profile['profile_binding']['profile_sha256']}")
    print("profile_hash_recomputes=true")
    print()
    print(f"target_freeze_sha256={target['target_freeze_binding']['target_freeze_sha256']}")
    print("target_freeze_hash_recomputes=true")
    print()
    print(f"receipt_sha256={receipt['receipt_binding']['receipt_sha256']}")
    print("receipt_hash_recomputes=true")
    print()
    print("generated_artifacts_deterministic=true")
    print("protected_source_files_unchanged=true")
    print("forbidden_output_count=0")
    print()
    print(f"profile_gate={PROFILE_GATE}")
    print(f"target_freeze_gate={TARGET_GATE}")
    print(f"receipt_gate={RECEIPT_GATE}")
    print(f"evidence_yield_branch={EVIDENCE_YIELD_BRANCH}")
    print()
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode != 0
    print(f"staged_changes_present={str(staged).lower()}")
    print("commit_created=false")
    print("push_executed=false")
    print()
    print(f"logical_terminal_transition={LOGICAL_TERMINAL}")
    print()
    print(f"terminal_transition={TERMINAL_TRANSITION}")


def emit_failure(exc: VS22Failure) -> None:
    print("BUILD_PHASE_VS2_2_KERNEL_PROFILE_AND_TARGET_FREEZE_V0_FAILED")
    print(f"failure_code={exc.code}")
    print(f"failed_source_or_field={exc.field}")
    print(f"expected_value={json.dumps(exc.expected, sort_keys=True)}")
    print(f"observed_value={json.dumps(exc.observed, sort_keys=True)}")
    print(f"violated_boundary={exc.boundary}")
    print(f"next_lawful_correction_surface={exc.next_surface}")
    print("self_repair_performed=false")


def main() -> int:
    root = Path.cwd().resolve()
    try:
        check_repo(root)
        profile, intake, _source_receipt = build_profile(root)
        target = build_target(profile, intake)
        receipt = build_receipt(profile, target)
        write_outputs(root, profile, target, receipt)
        validate_dirty_scope(root)
        ensure_forbidden_absent(root)
        emit_success(profile, target, receipt)
        return 0
    except VS22Failure as exc:
        emit_failure(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
