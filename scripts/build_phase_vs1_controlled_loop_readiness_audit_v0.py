#!/usr/bin/env python3

"""Build VS1.4 controlled loop readiness audit from committed VS1.3 inventory."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT = "scripts/build_phase_vs1_controlled_loop_readiness_audit_v0.py"
EXPECTED_HEAD = "741f28223d93b27d5a00fa06bb45a1739d66cb13"
OUTPUT_JSON = "docs/matrixlabs/phase_vs1/phase_vs1_controlled_loop_readiness_audit_v0.json"
OUTPUT_MD = "docs/matrixlabs/phase_vs1/phase_vs1_controlled_loop_readiness_audit_v0.md"

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

SCHEMA_VERSION = "matrixlabs_phase_vs1_controlled_loop_readiness_audit_v0"
ARTIFACT_ID = "phase_vs1_controlled_loop_readiness_audit_v0"
PHASE_ID = "PHASE_VS1"
UNIT_ID = "VS1.4_CONTROLLED_LOOP_READINESS_AUDIT"
UNIT_ROLE = "READINESS_AUDIT_ONLY"

SOURCE_INVENTORY_STATUS = "VS1_3_CONTROLLED_LOOP_PRECONDITION_INVENTORY_PASS"
SOURCE_INVENTORY_TRANSITION = "ADVANCE(VS1_4_CONTROLLED_LOOP_READINESS_AUDIT_PENDING)"
CONTRACT_STATUS = "VS1_2_CONTROLLED_LOOP_CONTRACT_DEFINITION_PASS"
READINESS_GATE = "VS1_4_CONTROLLED_LOOP_READINESS_AUDIT_PASS_NOT_READY_BLOCKERS_EXPOSED"
PRIMARY_VERDICT = "CONTROLLED_LOOP_NOT_READY_MIXED_BLOCKERS"
ARTIFACT_TRANSITION = "ADVANCE(VS1_5_MISSING_PRECONDITION_NEXT_SURFACE_MAP_PENDING)"
PRINT_TRANSITION = (
    "ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS1_CONTROLLED_LOOP_READINESS_AUDIT_V0_PENDING)"
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

VALID_READINESS = {
    "READY",
    "BLOCKED_MISSING",
    "BLOCKED_PARTIAL",
    "BLOCKED_CANDIDATE_ONLY",
    "BLOCKED_BOUNDARY_ONLY",
    "BLOCKED_INSUFFICIENT",
    "BLOCKED_SOURCE_UNVERIFIED",
    "BLOCKED_OUT_OF_SCOPE",
    "BLOCKED_AUTHORITY_REQUIRED",
    "BLOCKED_PROMOTION_REQUIRED",
    "BLOCKED_SCHEMA_REQUIRED",
    "BLOCKED_HUMAN_DECISION_REQUIRED",
    "BLOCKED_SOURCE_STATUS_REQUIRED",
    "BLOCKED_CONTRACT_REVISION_REQUIRED",
}
STATUS_TO_READINESS = {
    "PRESENT_VERIFIED": "READY",
    "PRESENT_PARTIAL": "BLOCKED_PARTIAL",
    "PRESENT_CANDIDATE_ONLY": "BLOCKED_CANDIDATE_ONLY",
    "PRESENT_BOUNDARY_ONLY": "BLOCKED_BOUNDARY_ONLY",
    "MISSING": "BLOCKED_MISSING",
    "INSUFFICIENT": "BLOCKED_INSUFFICIENT",
    "SOURCE_UNVERIFIED": "BLOCKED_SOURCE_UNVERIFIED",
    "OUT_OF_SCOPE": "BLOCKED_OUT_OF_SCOPE",
}
BLOCKER_TO_READINESS = {
    "AUTHORITY_REQUIRED": "BLOCKED_AUTHORITY_REQUIRED",
    "PROMOTION_REQUIRED": "BLOCKED_PROMOTION_REQUIRED",
    "SCHEMA_REQUIRED": "BLOCKED_SCHEMA_REQUIRED",
    "HUMAN_DECISION_REQUIRED": "BLOCKED_HUMAN_DECISION_REQUIRED",
    "SOURCE_STATUS_REQUIRED": "BLOCKED_SOURCE_STATUS_REQUIRED",
    "CONTRACT_REVISION_REQUIRED": "BLOCKED_CONTRACT_REVISION_REQUIRED",
}
READINESS_COUNT_KEY = {
    "READY": "ready",
    "BLOCKED_MISSING": "blocked_missing",
    "BLOCKED_PARTIAL": "blocked_partial",
    "BLOCKED_CANDIDATE_ONLY": "blocked_candidate_only",
    "BLOCKED_BOUNDARY_ONLY": "blocked_boundary_only",
    "BLOCKED_INSUFFICIENT": "blocked_insufficient",
    "BLOCKED_SOURCE_UNVERIFIED": "blocked_source_unverified",
    "BLOCKED_OUT_OF_SCOPE": "blocked_out_of_scope",
    "BLOCKED_AUTHORITY_REQUIRED": "blocked_authority_required",
    "BLOCKED_PROMOTION_REQUIRED": "blocked_promotion_required",
    "BLOCKED_SCHEMA_REQUIRED": "blocked_schema_required",
    "BLOCKED_HUMAN_DECISION_REQUIRED": "blocked_human_decision_required",
    "BLOCKED_SOURCE_STATUS_REQUIRED": "blocked_source_status_required",
    "BLOCKED_CONTRACT_REVISION_REQUIRED": "blocked_contract_revision_required",
}
PLACEHOLDER_VALUES = {"<readiness_status>", "<TBD>", "TBD", "TODO", "UNKNOWN", "PLACEHOLDER", ""}

COMPONENT_STOP = {
    "C01": "STOP_CONTROLLED_LOOP_SCOPE_REGIME_CONTRACT_NOT_READY",
    "C02": "STOP_CONTROLLED_LOOP_STATE_OBJECT_NOT_READY",
    "C03": "STOP_CONTROLLED_LOOP_MOVE_SPACE_NOT_READY",
    "C04": "STOP_CONTROLLED_LOOP_MOVE_SELECTOR_NOT_READY",
    "C05": "STOP_CONTROLLED_LOOP_MOVE_APPLICATOR_NOT_READY",
    "C06": "STOP_CONTROLLED_LOOP_AUTHORITY_POLICY_NOT_READY",
    "C07": "STOP_CONTROLLED_LOOP_RADIUS_POLICY_NOT_READY",
    "C08": "STOP_CONTROLLED_LOOP_HALT_POLICY_NOT_READY",
    "C09": "STOP_CONTROLLED_LOOP_RECEIPT_CONTRACT_NOT_READY",
    "C10": "STOP_CONTROLLED_LOOP_SOURCE_POLICY_NOT_READY",
    "C11": "STOP_CONTROLLED_LOOP_MICRO_SWEEP_BOUNDS_NOT_READY",
    "C12": "STOP_CONTROLLED_LOOP_PRESSURE_READOUT_NOT_READY",
    "C13": "STOP_CONTROLLED_LOOP_PRESSURE_CLASSIFIER_NOT_READY",
    "C14": "STOP_CONTROLLED_LOOP_LOCAL_REVISION_SURFACE_NOT_READY",
    "C15": "STOP_CONTROLLED_LOOP_PORTABILITY_MAP_NOT_READY",
    "C16": "STOP_CONTROLLED_LOOP_REPLAY_AUDIT_NOT_READY",
    "C17": "STOP_CONTROLLED_LOOP_FORBIDDEN_EFFECT_GUARD_NOT_READY",
    "C18": "STOP_CONTROLLED_LOOP_EVIDENCE_YIELD_HOOK_NOT_READY",
    "C19": "STOP_CONTROLLED_LOOP_HUMAN_ESCALATION_BOUNDARY_NOT_READY",
    "C20": "STOP_CONTROLLED_LOOP_CONVERGENCE_CRITERION_NOT_READY",
}
COMPONENT_CLASS = {
    "C01": ["SCOPE_REGIME_BLOCKER"],
    "C02": ["STRUCTURAL_BLOCKER"],
    "C03": ["STRUCTURAL_BLOCKER"],
    "C04": ["STRUCTURAL_BLOCKER"],
    "C05": ["STRUCTURAL_BLOCKER"],
    "C06": ["AUTHORITY_BLOCKER"],
    "C07": ["CONTROL_BLOCKER"],
    "C08": ["CONTROL_BLOCKER"],
    "C09": ["AUDIT_BLOCKER"],
    "C10": ["AUDIT_BLOCKER", "SOURCE_TRUST_BLOCKER"],
    "C11": ["CONTROL_BLOCKER"],
    "C12": ["OBSERVABILITY_BLOCKER"],
    "C13": ["OBSERVABILITY_BLOCKER"],
    "C14": ["REVISION_BLOCKER"],
    "C15": ["PORTABILITY_BLOCKER"],
    "C16": ["AUDIT_BLOCKER"],
    "C17": ["AUDIT_BLOCKER"],
    "C18": ["OBSERVABILITY_BLOCKER"],
    "C19": ["GOVERNANCE_BLOCKER"],
    "C20": ["CONVERGENCE_BLOCKER"],
}
FLAG_CLASS = {
    "AUTHORITY_REQUIRED": ["AUTHORITY_BLOCKER"],
    "PROMOTION_REQUIRED": ["PROMOTION_BLOCKER"],
    "SCHEMA_REQUIRED": ["SCHEMA_BLOCKER"],
    "HUMAN_DECISION_REQUIRED": ["GOVERNANCE_BLOCKER"],
    "SOURCE_STATUS_REQUIRED": ["SOURCE_TRUST_BLOCKER"],
    "CONTRACT_REVISION_REQUIRED": ["CONTRACT_REVISION_BLOCKER"],
}
BLOCKER_CLASSES = [
    "SCOPE_REGIME_BLOCKER",
    "STRUCTURAL_BLOCKER",
    "AUTHORITY_BLOCKER",
    "CONTROL_BLOCKER",
    "OBSERVABILITY_BLOCKER",
    "REVISION_BLOCKER",
    "PORTABILITY_BLOCKER",
    "AUDIT_BLOCKER",
    "GOVERNANCE_BLOCKER",
    "SOURCE_TRUST_BLOCKER",
    "SCHEMA_BLOCKER",
    "PROMOTION_BLOCKER",
    "CONVERGENCE_BLOCKER",
    "CONTRACT_REVISION_BLOCKER",
]

FORBIDDEN_ARTIFACTS = [
    "docs/matrixlabs/runner",
    "docs/matrixlabs/runtime",
    "docs/matrixlabs/move_space",
    "docs/matrixlabs/micro_sweeps",
    "docs/matrixlabs/phase_vs1/phase_vs1_missing_precondition_next_surface_map_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_missing_precondition_next_surface_map_v0.md",
    "docs/matrixlabs/phase_vs1/phase_vs1_component_repair_plan_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_candidate_promotion_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_controlled_loop_readiness_certificate_v0.json",
]


class AuditFailure(RuntimeError):
    def __init__(
        self,
        code: str,
        *,
        source: str = "NONE",
        component: str = "NONE",
        field: str = "NONE",
        expected: object = "NONE",
        actual: object = "NONE",
        next_surface: str = "REPAIR_VS1_4_READINESS_AUDIT_INPUT",
    ) -> None:
        super().__init__(code)
        self.code = code
        self.source = source
        self.component = component
        self.field = field
        self.expected = expected
        self.actual = actual
        self.next_surface = next_surface


def fail(
    code: str,
    *,
    source: str = "NONE",
    component: str = "NONE",
    field: str = "NONE",
    expected: object = "NONE",
    actual: object = "NONE",
    next_surface: str = "REPAIR_VS1_4_READINESS_AUDIT_INPUT",
) -> None:
    raise AuditFailure(
        code,
        source=source,
        component=component,
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
            "STOP_VS1_4_PRECONDITION_INVENTORY_NOT_PASS",
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
            "STOP_VS1_4_PRECONDITION_INVENTORY_NOT_PASS",
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
        if path in {SOURCE_INVENTORY_JSON, SOURCE_INVENTORY_MD}:
            fail(
                "STOP_VS1_4_SOURCE_INVENTORY_MUTATED",
                source=path,
                field="dirty_scope",
                expected="unchanged VS1.3 inventory",
                actual=line,
            )
        if path in {SOURCE_CONTRACT_JSON, SOURCE_CONTRACT_MD}:
            fail(
                "STOP_VS1_4_SOURCE_CONTRACT_MUTATED",
                source=path,
                field="dirty_scope",
                expected="unchanged VS1.2 contract",
                actual=line,
            )
        if path.startswith(f"{VS0_ROOT}/"):
            fail(
                "STOP_VS1_4_SOURCE_CONTRACT_MUTATED",
                source=path,
                field="dirty_scope",
                expected="unchanged source artifacts",
                actual=line,
            )
        fail(
            "STOP_VS1_4_PRECONDITION_INVENTORY_NOT_PASS",
            source=path,
            field="dirty_scope",
            expected="only VS1.4 outputs, baseline_share, or discussion_packets",
            actual=line,
        )


def require_head(root: Path) -> None:
    head = run_git(root, ["rev-parse", "HEAD"])
    if head != EXPECTED_HEAD:
        fail(
            "STOP_VS1_4_PRECONDITION_INVENTORY_NOT_PASS",
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
            "STOP_VS1_4_PRECONDITION_INVENTORY_NOT_PASS",
            source=rel_path,
            field="file_presence",
            expected=True,
            actual=False,
        )
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(
            "STOP_VS1_4_PRECONDITION_INVENTORY_NOT_PASS",
            source=rel_path,
            field="valid_json",
            expected=True,
            actual=str(exc),
        )
    if not isinstance(value, dict):
        fail(
            "STOP_VS1_4_PRECONDITION_INVENTORY_NOT_PASS",
            source=rel_path,
            field="json_object",
            expected=True,
            actual=type(value).__name__,
        )
    return value


def require_file(root: Path, rel_path: str) -> None:
    if not (root / rel_path).is_file():
        fail(
            "STOP_VS1_4_PRECONDITION_INVENTORY_NOT_PASS",
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
                "STOP_VS1_4_PRECONDITION_INVENTORY_NOT_PASS",
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
    if first in {SOURCE_INVENTORY_JSON, SOURCE_INVENTORY_MD}:
        code = "STOP_VS1_4_SOURCE_INVENTORY_MUTATED"
    elif first in {SOURCE_CONTRACT_JSON, SOURCE_CONTRACT_MD}:
        code = "STOP_VS1_4_SOURCE_CONTRACT_MUTATED"
    else:
        code = "STOP_VS1_4_SOURCE_CONTRACT_MUTATED"
    fail(
        code,
        source=first,
        field="source_hash",
        expected=before.get(first),
        actual=after.get(first),
    )


def validate_source_inputs(inventory: dict[str, Any], contract: dict[str, Any]) -> None:
    if inventory.get("artifact_id") != "phase_vs1_controlled_loop_precondition_inventory_v0":
        fail(
            "STOP_VS1_4_PRECONDITION_INVENTORY_NOT_PASS",
            source=SOURCE_INVENTORY_JSON,
            field="artifact_id",
            expected="phase_vs1_controlled_loop_precondition_inventory_v0",
            actual=inventory.get("artifact_id"),
        )
    if inventory.get("inventory_verdict") != SOURCE_INVENTORY_STATUS:
        fail(
            "STOP_VS1_4_PRECONDITION_INVENTORY_NOT_PASS",
            source=SOURCE_INVENTORY_JSON,
            field="inventory_verdict",
            expected=SOURCE_INVENTORY_STATUS,
            actual=inventory.get("inventory_verdict"),
        )
    if get_value(inventory, "terminal_transition.transition") != SOURCE_INVENTORY_TRANSITION:
        fail(
            "STOP_VS1_4_PRECONDITION_INVENTORY_NOT_PASS",
            source=SOURCE_INVENTORY_JSON,
            field="terminal_transition.transition",
            expected=SOURCE_INVENTORY_TRANSITION,
            actual=get_value(inventory, "terminal_transition.transition"),
        )
    if get_value(inventory, "inventory_mode.readiness_audit_performed") is not False:
        fail(
            "STOP_VS1_4_PRECONDITION_INVENTORY_NOT_PASS",
            source=SOURCE_INVENTORY_JSON,
            field="inventory_mode.readiness_audit_performed",
            expected=False,
            actual=get_value(inventory, "inventory_mode.readiness_audit_performed"),
        )
    if contract.get("contract_verdict") != CONTRACT_STATUS:
        fail(
            "STOP_VS1_4_PRECONDITION_INVENTORY_NOT_PASS",
            source=SOURCE_CONTRACT_JSON,
            field="contract_verdict",
            expected=CONTRACT_STATUS,
            actual=contract.get("contract_verdict"),
        )
    if contract.get("required_components") != EXPECTED_COMPONENTS:
        fail(
            "STOP_VS1_4_COMPONENT_SET_MISMATCH",
            source=SOURCE_CONTRACT_JSON,
            field="required_components",
            expected=EXPECTED_COMPONENTS,
            actual=contract.get("required_components"),
        )


def ensure_no_forbidden_artifacts(root: Path) -> None:
    for rel_path in FORBIDDEN_ARTIFACTS:
        if (root / rel_path).exists():
            fail(
                "STOP_VS1_4_VS1_5_ARTIFACT_CREATED",
                source=rel_path,
                field="forbidden_artifact",
                expected="absent",
                actual="present",
            )


def markdown_contains_vs1_4_overclaim(md: str) -> list[str]:
    hits: list[str] = []
    allowed_patterns = [
        r"\bloop may execute\s*[:=]\s*false\b",
        r"\bhuman execution authority requested\s*[:=]\s*false\b",
        r"\bhuman execution authority granted\s*[:=]\s*false\b",
        r"\brunner exists\s*[:=]\s*false\b",
        r"\brunner readiness exists\s*[:=]\s*false\b",
        r"\brunner authority exists\s*[:=]\s*false\b",
        r"\bmicro-sweeps authorized\s*[:=]\s*false\b",
        r"\blocal revision authorized\s*[:=]\s*false\b",
        r"\bmissing components should be built\s*[:=]\s*false\b",
        r"\bwhich missing component should be built first\s*[:=]\s*false\b",
        r"\bcandidate components should be promoted\s*[:=]\s*false\b",
        r"\bactive registry required next\s*[:=]\s*false\b",
        r"\bportability demonstrated\s*[:=]\s*false\b",
        r"\bvs0 generalized\s*[:=]\s*false\b",
        r"\bperformance optimization begun\s*[:=]\s*false\b",
        r"\bscale optimization begun\s*[:=]\s*false\b",
        r"\bvs1\.5 executed\s*[:=]\s*false\b",
        r"\bvs1\.5 built\s*[:=]\s*false\b",
        r"\bvs1\.5 run\s*[:=]\s*false\b",
        r"\bmissing precondition next-surface map created\s*[:=]\s*false\b",
        r"\bnext surfaces ranked\s*[:=]\s*false\b",
        r"\brepair sequence created\s*[:=]\s*false\b",
        r"\bcomponent build authorized\s*[:=]\s*false\b",
        r"\bloop execution authorized\s*[:=]\s*false\b",
        r"\brunner created\s*[:=]\s*false\b",
        r"\bregistry activation authorized\s*[:=]\s*false\b",
        r"\btrace generalization authorized\s*[:=]\s*false\b",
        r"\bready for human execution-authority decision is execution authority\s*[:=]\s*false\b",
        r"\bhuman execution-authority decision requested by vs1\.4\s*[:=]\s*false\b",
        r"\bcontrolled loop ready\s*[:=]\s*false\b",
        r"\bready for human execution-authority decision\s*[:=]\s*false\b",
        r"\bdoes not .*repair blockers\b",
        r"\bdoes not .*rank them\b",
        r"\bdoes not .*build missing objects\b",
        r"\bdoes not .*promote candidates\b",
        r"\bdoes not .*authorize execution\b",
        r"\bdoes not .*request human execution authority\b",
        r"\bdoes not .*run micro-sweeps\b",
        r"\bdoes not .*create a runner\b",
        r"\bdoes not .*execute vs1\.5\b",
    ]
    forbidden_patterns = {
        "loop may execute": r"\bloop may execute\b",
        "human execution authority granted": r"\bhuman execution authority granted\b",
        "human execution authority requested": r"\bhuman execution authority requested\b",
        "runner exists": r"\brunner exists\b",
        "runner ready": r"\brunner ready\b",
        "runner authority exists": r"\brunner authority exists\b",
        "runtime ready": r"\bruntime ready\b",
        "micro-sweeps authorized": r"\bmicro-sweeps authorized\b",
        "local revision authorized": r"\blocal revision authorized\b",
        "missing components should be built": r"\bmissing components should be built\b",
        "candidate promoted": r"\bcandidate promoted\b",
        "component repaired": r"\bcomponent repaired\b",
        "next component selected": r"\bnext component selected\b",
        "repair plan created": r"\brepair plan created\b",
        "next surfaces ranked": r"\bnext surfaces ranked\b",
        "VS1.5 executed": r"\bvs1\.5 executed\b",
        "portability demonstrated": r"\bportability demonstrated\b",
        "VS0 generalized": r"\bvs0 generalized\b",
        "performance optimization begun": r"\bperformance optimization begun\b",
        "scale optimization begun": r"\bscale optimization begun\b",
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


def derive_component(
    inventory_record: dict[str, Any],
) -> dict[str, Any]:
    component_id = inventory_record["component_id"]
    component_name = inventory_record["component_name"]
    component_key = f"{component_id}_{component_name}"
    source_status = inventory_record["primary_inventory_status"]
    source_blockers = inventory_record.get("blocker_flags", [])
    if source_status not in STATUS_TO_READINESS:
        fail(
            "STOP_VS1_4_COMPONENT_STATUS_DERIVATION_FAILED",
            component=component_key,
            field="primary_inventory_status",
            expected=sorted(STATUS_TO_READINESS),
            actual=source_status,
        )
    secondary = [
        BLOCKER_TO_READINESS[flag]
        for flag in source_blockers
        if flag in BLOCKER_TO_READINESS
    ]
    primary = STATUS_TO_READINESS[source_status]
    if source_status == "PRESENT_VERIFIED" and secondary:
        primary = secondary[0]
    if source_status != "PRESENT_VERIFIED" and primary == "READY":
        fail(
            "STOP_VS1_4_NON_PRESENT_VERIFIED_UPGRADED",
            component=component_key,
            field="primary_readiness_status",
            expected="blocked status",
            actual=primary,
        )
    classes = list(COMPONENT_CLASS.get(component_id, []))
    for flag in source_blockers:
        for cls in FLAG_CLASS.get(flag, []):
            if cls not in classes:
                classes.append(cls)
    return {
        "component_id": component_id,
        "component_name": component_name,
        "component_key": component_key,
        "source_inventory_status": source_status,
        "source_blocker_flags": source_blockers,
        "primary_readiness_status": primary,
        "secondary_readiness_blockers": secondary,
        "blocker_classes": classes,
        "component_stop_if_blocked": COMPONENT_STOP[component_id],
        "readiness_reason": (
            f"{component_key} derives {primary} from VS1.3 status {source_status}; "
            "secondary blockers are preserved without repair, promotion, or upgrade."
        ),
        "derived_from_vs1_3_inventory": True,
        "component_upgraded_by_vs1_4": False,
        "component_repaired_by_vs1_4": False,
        "component_promoted_by_vs1_4": False,
        "may_feed_vs1_5_missing_precondition_map": True,
    }


def build_derivations(inventory: dict[str, Any]) -> tuple[dict[str, str], list[dict[str, Any]]]:
    records = inventory.get("component_records")
    if not isinstance(records, list) or len(records) != 20:
        fail(
            "STOP_VS1_4_COMPONENT_TABLE_MISSING",
            source=SOURCE_INVENTORY_JSON,
            field="component_records",
            expected=20,
            actual=len(records) if isinstance(records, list) else type(records).__name__,
        )
    by_key = {
        f"{record.get('component_id')}_{record.get('component_name')}": record
        for record in records
        if isinstance(record, dict)
    }
    if list(inventory.get("component_status_table", {}).keys()) != EXPECTED_COMPONENTS:
        fail(
            "STOP_VS1_4_COMPONENT_SET_MISMATCH",
            source=SOURCE_INVENTORY_JSON,
            field="component_status_table",
            expected=EXPECTED_COMPONENTS,
            actual=list(inventory.get("component_status_table", {}).keys()),
        )
    table: dict[str, str] = {}
    derivations: list[dict[str, Any]] = []
    for key in EXPECTED_COMPONENTS:
        record = by_key.get(key)
        if not record:
            fail(
                "STOP_VS1_4_COMPONENT_TABLE_MISSING",
                source=SOURCE_INVENTORY_JSON,
                component=key,
                field="component_records",
                expected="present",
                actual="missing",
            )
        derived = derive_component(record)
        readiness = derived["primary_readiness_status"]
        if readiness in PLACEHOLDER_VALUES:
            fail(
                "STOP_VS1_4_PLACEHOLDER_READINESS_STATUS_EMITTED",
                component=key,
                field="primary_readiness_status",
                expected="non-placeholder",
                actual=readiness,
            )
        if readiness not in VALID_READINESS:
            fail(
                "STOP_VS1_4_COMPONENT_READINESS_STATUS_INVALID",
                component=key,
                field="primary_readiness_status",
                expected=sorted(VALID_READINESS),
                actual=readiness,
            )
        table[key] = readiness
        derivations.append(derived)
    return table, derivations


def summarize_readiness(derivations: list[dict[str, Any]]) -> dict[str, int]:
    counts = {
        "required_components_total": 20,
        "ready_component_count": 0,
        "missing_or_blocked_component_count": 0,
        "ready": 0,
        "blocked_missing": 0,
        "blocked_partial": 0,
        "blocked_candidate_only": 0,
        "blocked_boundary_only": 0,
        "blocked_insufficient": 0,
        "blocked_source_unverified": 0,
        "blocked_out_of_scope": 0,
        "blocked_authority_required": 0,
        "blocked_promotion_required": 0,
        "blocked_schema_required": 0,
        "blocked_human_decision_required": 0,
        "blocked_source_status_required": 0,
        "blocked_contract_revision_required": 0,
    }
    for record in derivations:
        readiness = record["primary_readiness_status"]
        counts[READINESS_COUNT_KEY[readiness]] += 1
        if readiness == "READY":
            counts["ready_component_count"] += 1
        else:
            counts["missing_or_blocked_component_count"] += 1
    return counts


def summarize_secondary(derivations: list[dict[str, Any]]) -> dict[str, int]:
    counts = {
        "blocked_authority_required": 0,
        "blocked_promotion_required": 0,
        "blocked_schema_required": 0,
        "blocked_human_decision_required": 0,
        "blocked_source_status_required": 0,
        "blocked_contract_revision_required": 0,
    }
    for record in derivations:
        for blocker in record["secondary_readiness_blockers"]:
            counts[READINESS_COUNT_KEY[blocker]] += 1
    return counts


def build_blocker_table(derivations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for record in derivations:
        if record["primary_readiness_status"] == "READY":
            continue
        rows.append(
            {
                "component_key": record["component_key"],
                "primary_readiness_status": record["primary_readiness_status"],
                "secondary_readiness_blockers": record["secondary_readiness_blockers"],
                "blocker_classes": record["blocker_classes"],
                "component_stop_if_blocked": record["component_stop_if_blocked"],
                "reason": record["readiness_reason"],
            }
        )
    return rows


def build_blocker_class_summary(derivations: list[dict[str, Any]]) -> dict[str, Any]:
    class_counts = {cls: 0 for cls in BLOCKER_CLASSES}
    for record in derivations:
        if record["primary_readiness_status"] == "READY":
            continue
        for cls in record["blocker_classes"]:
            class_counts[cls] += 1
    summary: dict[str, Any] = {
        cls: class_counts[cls] > 0 for cls in BLOCKER_CLASSES
    }
    summary["class_counts"] = class_counts
    return summary


def build_audit(root: Path, inventory: dict[str, Any]) -> dict[str, Any]:
    table, derivations = build_derivations(inventory)
    summary = summarize_readiness(derivations)
    secondary = summarize_secondary(derivations)
    blocker_table = build_blocker_table(derivations)
    blocker_classes = build_blocker_class_summary(derivations)
    ready = summary["ready_component_count"] == 20
    primary_verdict = (
        "CONTROLLED_LOOP_READY_FOR_HUMAN_EXECUTION_AUTHORITY_DECISION"
        if ready
        else PRIMARY_VERDICT
    )
    gate = (
        "VS1_4_CONTROLLED_LOOP_READINESS_AUDIT_PASS_READY_FOR_HUMAN_EXECUTION_AUTHORITY_DECISION"
        if ready
        else READINESS_GATE
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "artifact_id": ARTIFACT_ID,
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "unit_role": UNIT_ROLE,
        "source_inventory": {
            "artifact_id": "phase_vs1_controlled_loop_precondition_inventory_v0",
            "path": SOURCE_INVENTORY_JSON,
            "commit_sha": EXPECTED_HEAD,
            "sha256": sha256(root / SOURCE_INVENTORY_JSON),
            "required_status": SOURCE_INVENTORY_STATUS,
            "required_transition": SOURCE_INVENTORY_TRANSITION,
            "source_role": "COMPONENT_STATUS_TABLE",
        },
        "source_contract": {
            "artifact_id": "phase_vs1_controlled_convergence_loop_contract_v0",
            "path": SOURCE_CONTRACT_JSON,
            "source_role": "MCCL_CONTRACT_REFERENCE",
        },
        "readiness_target": {
            "loop_name": "MINIMAL_CONTROLLED_CONVERGENCE_LOOP",
            "short_name": "MCCL",
            "ready_for_human_execution_authority_decision_is_execution_authority": False,
        },
        "readiness_profile": {
            "profile_id": "MCCL_STRICT_INITIAL_READINESS_PROFILE_V0",
            "required_components_total": 20,
            "readiness_rule": "ALL_DECLARED_COMPONENTS_MUST_BE_READY",
            "weaker_profile_defined": False,
            "all_components_ready_required_for_ready_verdict": True,
        },
        "readiness_audit_pass_semantics": {
            "not_ready_can_pass": True,
            "not_ready_is_phase_failure": False,
            "unclear_not_ready_reason_is_failure": True,
            "ready_for_human_decision_is_not_execution_authority": True,
            "all_components_ready_required_for_ready_verdict": True,
        },
        "readiness_derivation_policy": {
            "derivation_source": "VS1.3 primary_inventory_status + blocker_flags",
            "primary_inventory_status_derived_first": True,
            "blocker_flags_secondary_for_non_present_verified": True,
            "only_present_verified_can_be_downgraded_by_blocker_flags": True,
            "non_present_verified_may_not_be_upgraded": True,
            "secondary_blockers_preserved": True,
        },
        "component_readiness_table": table,
        "readiness_derivation_table": {
            "derivation_source": "VS1.3 primary_inventory_status + blocker_flags",
            "component_derivations": derivations,
        },
        "readiness_summary_counts": summary,
        "secondary_blocker_summary": secondary,
        "blocker_table": blocker_table,
        "blocker_class_summary": blocker_classes,
        "aggregate_readiness_verdict": {
            "controlled_loop_ready": ready,
            "primary_verdict": primary_verdict,
            "ready_for_human_execution_authority_decision": ready,
            "human_execution_authority_decision_requested_by_vs1_4": False,
            "missing_or_blocked_component_count": summary["missing_or_blocked_component_count"],
            "ready_component_count": summary["ready_component_count"],
        },
        "execution_authority_status": {
            "loop_execution_authorized": False,
            "runner_created": False,
            "micro_sweeps_authorized": False,
            "local_revision_authorized": False,
            "registry_activation_authorized": False,
            "trace_generalization_authorized": False,
        },
        "forbidden_claim_checks": {
            "execution_authority_claimed": False,
            "loop_execution_authorized": False,
            "runner_created": False,
            "micro_sweeps_authorized": False,
            "local_revision_authorized": False,
            "component_build_attempted": False,
            "repair_attempted": False,
            "candidate_promotion_attempted": False,
            "next_surface_ranking_attempted": False,
            "missing_precondition_map_created": False,
            "global_generalization_claimed": False,
            "optimization_target_assumed": False,
        },
        "vs1_5_boundary": {
            "vs1_5_may_map_missing_preconditions_after_commit": True,
            "vs1_5_built": False,
            "vs1_5_run": False,
            "missing_precondition_next_surface_map_created": False,
            "next_surfaces_ranked": False,
            "repair_sequence_created": False,
            "component_build_authorized": False,
        },
        "source_preservation": {
            "source_inventory_mutated_by_vs1_4": False,
            "source_contract_mutated_by_vs1_4": False,
            "vs1_1_source_intake_mutated_by_vs1_4": False,
            "post_vs0_direction_decision_receipt_mutated_by_vs1_4": False,
            "vs0_source_artifacts_mutated_by_vs1_4": False,
        },
        "non_claims": {
            "loop_may_execute": False,
            "human_execution_authority_requested": False,
            "human_execution_authority_granted": False,
            "runner_exists": False,
            "runner_readiness_exists": False,
            "runner_authority_exists": False,
            "micro_sweeps_authorized": False,
            "local_revision_authorized": False,
            "missing_components_should_be_built": False,
            "which_missing_component_should_be_built_first": False,
            "candidate_components_should_be_promoted": False,
            "active_registry_required_next": False,
            "portability_demonstrated": False,
            "vs0_generalized": False,
            "performance_optimization_begun": False,
            "scale_optimization_begun": False,
            "vs1_5_executed": False,
        },
        "evidence_yield": {
            "yield_branch": "CONFIRMATION_YIELD",
            "confirmation_yield_reason": (
                "the strict readiness audit completed, derived component readiness "
                "from VS1.3 inventory, exposed typed blockers, and preserved "
                "non-execution boundaries"
            ),
            "diagnostic_yield_present": True,
            "diagnostic_yield_reason": (
                "the MCCL is not ready and the blocking components/classes are typed"
            ),
        },
        "readiness_audit_gate": gate,
        "terminal_transition": {
            "transition": ARTIFACT_TRANSITION,
            "executes_vs1_5": False,
            "authorizes_loop_execution": False,
            "authorizes_repair": False,
            "authorizes_component_build": False,
            "authorizes_ranking": False,
        },
        "failures": [],
    }


def build_markdown(audit: dict[str, Any]) -> str:
    rows = [
        "| Component | Primary readiness status | Secondary blockers |",
        "| --- | --- | --- |",
    ]
    derivations = audit["readiness_derivation_table"]["component_derivations"]
    for record in derivations:
        rows.append(
            "| "
            + " | ".join(
                [
                    record["component_key"],
                    record["primary_readiness_status"],
                    ", ".join(record["secondary_readiness_blockers"]) or "none",
                ]
            )
            + " |"
        )
    class_summary = audit["blocker_class_summary"]
    class_lines = "\n".join(
        f"- {cls}: {str(class_summary[cls]).lower()} ({class_summary['class_counts'][cls]})"
        for cls in BLOCKER_CLASSES
    )
    return f"""# Phase VS1.4 controlled loop readiness audit v0

## Status

{audit['readiness_audit_gate']}

## Source inventory

- source inventory: phase_vs1_controlled_loop_precondition_inventory_v0
- source inventory commit: {EXPECTED_HEAD}
- required source inventory status: {SOURCE_INVENTORY_STATUS}
- source role: COMPONENT_STATUS_TABLE

## Readiness target

- loop name: MINIMAL_CONTROLLED_CONVERGENCE_LOOP
- short name: MCCL
- ready for human execution-authority decision is execution authority: false

## Readiness profile

- profile id: MCCL_STRICT_INITIAL_READINESS_PROFILE_V0
- required components total: 20
- readiness rule: ALL_DECLARED_COMPONENTS_MUST_BE_READY
- weaker profile defined: false

## Derivation policy

- derivation source: VS1.3 primary_inventory_status + blocker_flags
- primary inventory status derived first: true
- blocker flags secondary for non-present-verified: true
- only PRESENT_VERIFIED can be downgraded by blocker flags: true
- non-PRESENT_VERIFIED may not be upgraded: true
- secondary blockers preserved: true

## Readiness summary

- controlled loop ready: false
- primary verdict: CONTROLLED_LOOP_NOT_READY_MIXED_BLOCKERS
- ready for human execution-authority decision: false
- human execution-authority decision requested by VS1.4: false
- ready component count: 0
- missing or blocked component count: 20

## Component readiness table

{chr(10).join(rows)}

## Blocker class summary

{class_lines}

## Execution authority status

- loop execution authorized: false
- runner created: false
- micro-sweeps authorized: false
- local revision authorized: false
- registry activation authorized: false
- trace generalization authorized: false

## VS1.5 boundary

- VS1.5 may map missing preconditions after commit: true
- VS1.5 built: false
- VS1.5 run: false
- missing precondition next-surface map created: false
- next surfaces ranked: false
- repair sequence created: false
- component build authorized: false

## Non-claims

- loop may execute: false
- human execution authority requested: false
- human execution authority granted: false
- runner exists: false
- runner readiness exists: false
- runner authority exists: false
- micro-sweeps authorized: false
- local revision authorized: false
- missing components should be built: false
- which missing component should be built first: false
- candidate components should be promoted: false
- active registry required next: false
- portability demonstrated: false
- VS0 generalized: false
- performance optimization begun: false
- scale optimization begun: false
- VS1.5 executed: false

## Evidence Yield

- yield branch: CONFIRMATION_YIELD
- Diagnostic Yield present: true

## Terminal transition

{ARTIFACT_TRANSITION}

## Boundary statement

VS1.4 audits readiness from the committed VS1.3 inventory. It exposes a typed not-ready result under the strict all-components-ready profile. It does not repair blockers, rank them, build missing objects, promote candidates, authorize execution, request human execution authority, run micro-sweeps, create a runner, or execute VS1.5.
"""


def validate_audit(audit: dict[str, Any], md: str) -> None:
    if audit.get("schema_version") != SCHEMA_VERSION:
        fail(
            "STOP_VS1_4_PRECONDITION_INVENTORY_NOT_PASS",
            field="schema_version",
            expected=SCHEMA_VERSION,
            actual=audit.get("schema_version"),
        )
    table = audit.get("component_readiness_table", {})
    if list(table.keys()) != EXPECTED_COMPONENTS:
        fail(
            "STOP_VS1_4_COMPONENT_SET_MISMATCH",
            field="component_readiness_table",
            expected=EXPECTED_COMPONENTS,
            actual=list(table.keys()) if isinstance(table, dict) else table,
        )
    derivations = get_value(audit, "readiness_derivation_table.component_derivations", [])
    if not isinstance(derivations, list) or len(derivations) != 20:
        fail(
            "STOP_VS1_4_COMPONENT_TABLE_MISSING",
            field="component_derivations",
            expected=20,
            actual=len(derivations) if isinstance(derivations, list) else type(derivations).__name__,
        )
    for record in derivations:
        readiness = record.get("primary_readiness_status")
        if readiness in PLACEHOLDER_VALUES:
            fail(
                "STOP_VS1_4_PLACEHOLDER_READINESS_STATUS_EMITTED",
                component=record.get("component_key", "NONE"),
                field="primary_readiness_status",
                expected="non-placeholder",
                actual=readiness,
            )
        if readiness not in VALID_READINESS:
            fail(
                "STOP_VS1_4_COMPONENT_READINESS_STATUS_INVALID",
                component=record.get("component_key", "NONE"),
                field="primary_readiness_status",
                expected=sorted(VALID_READINESS),
                actual=readiness,
            )
        if record.get("component_upgraded_by_vs1_4") is not False:
            fail(
                "STOP_VS1_4_NON_PRESENT_VERIFIED_UPGRADED",
                component=record.get("component_key", "NONE"),
                field="component_upgraded_by_vs1_4",
                expected=False,
                actual=record.get("component_upgraded_by_vs1_4"),
            )
    summary = audit.get("readiness_summary_counts", {})
    expected_current = {
        "ready_component_count": 0,
        "missing_or_blocked_component_count": 20,
        "ready": 0,
        "blocked_missing": 6,
        "blocked_partial": 6,
        "blocked_candidate_only": 6,
        "blocked_boundary_only": 2,
        "blocked_insufficient": 0,
        "blocked_source_unverified": 0,
        "blocked_out_of_scope": 0,
    }
    for key, expected in expected_current.items():
        if summary.get(key) != expected:
            fail(
                "STOP_VS1_4_AGGREGATE_READINESS_RULE_MISSING",
                field=f"readiness_summary_counts.{key}",
                expected=expected,
                actual=summary.get(key),
            )
    false_paths = [
        "aggregate_readiness_verdict.controlled_loop_ready",
        "aggregate_readiness_verdict.ready_for_human_execution_authority_decision",
        "aggregate_readiness_verdict.human_execution_authority_decision_requested_by_vs1_4",
        "execution_authority_status.loop_execution_authorized",
        "execution_authority_status.runner_created",
        "execution_authority_status.micro_sweeps_authorized",
        "execution_authority_status.local_revision_authorized",
        "vs1_5_boundary.vs1_5_built",
        "vs1_5_boundary.vs1_5_run",
        "vs1_5_boundary.missing_precondition_next_surface_map_created",
        "vs1_5_boundary.next_surfaces_ranked",
        "vs1_5_boundary.repair_sequence_created",
        "vs1_5_boundary.component_build_authorized",
        "terminal_transition.executes_vs1_5",
        "terminal_transition.authorizes_loop_execution",
        "terminal_transition.authorizes_repair",
        "terminal_transition.authorizes_component_build",
        "terminal_transition.authorizes_ranking",
    ]
    for path in false_paths:
        if get_value(audit, path) is not False:
            fail(
                "STOP_VS1_4_EXECUTION_AUTHORITY_CLAIMED",
                field=path,
                expected=False,
                actual=get_value(audit, path),
            )
    if get_value(audit, "aggregate_readiness_verdict.primary_verdict") != PRIMARY_VERDICT:
        fail(
            "STOP_VS1_4_READY_VERDICT_AMBIGUOUS",
            field="aggregate_readiness_verdict.primary_verdict",
            expected=PRIMARY_VERDICT,
            actual=get_value(audit, "aggregate_readiness_verdict.primary_verdict"),
        )
    if audit.get("readiness_audit_gate") != READINESS_GATE:
        fail(
            "STOP_VS1_4_NOT_READY_REASON_UNCLEAR",
            field="readiness_audit_gate",
            expected=READINESS_GATE,
            actual=audit.get("readiness_audit_gate"),
        )
    hits = markdown_contains_vs1_4_overclaim(md)
    if hits:
        fail(
            "STOP_VS1_4_EXECUTION_AUTHORITY_CLAIMED",
            source=OUTPUT_MD,
            field="markdown_overclaim_guard",
            expected=[],
            actual=hits,
        )


def emit_success_readout() -> None:
    print("BUILD_PHASE_VS1_CONTROLLED_LOOP_READINESS_AUDIT_V0_COMPLETE")
    print(f"artifact_id={ARTIFACT_ID}")
    print(f"schema_version={SCHEMA_VERSION}")
    print(f"phase_id={PHASE_ID}")
    print(f"unit_id={UNIT_ID}")
    print(f"unit_role={UNIT_ROLE}")
    print(f"source_inventory_commit_sha={EXPECTED_HEAD}")
    print(f"source_inventory_required_status={SOURCE_INVENTORY_STATUS}")
    print(f"source_inventory_required_transition={SOURCE_INVENTORY_TRANSITION}")
    print("loop_name=MINIMAL_CONTROLLED_CONVERGENCE_LOOP")
    print("short_name=MCCL")
    print("readiness_profile=MCCL_STRICT_INITIAL_READINESS_PROFILE_V0")
    print("readiness_rule=ALL_DECLARED_COMPONENTS_MUST_BE_READY")
    print("readiness_audit_pass_semantics_not_ready_can_pass=true")
    print("primary_inventory_status_derived_first=true")
    print("secondary_blockers_preserved=true")
    print("non_present_verified_may_not_be_upgraded=true")
    print("required_components_total=20")
    print("all_components_assessed=true")
    print("component_readiness_statuses_derived=true")
    print("ready_component_count=0")
    print("missing_or_blocked_component_count=20")
    print("blocked_missing=6")
    print("blocked_partial=6")
    print("blocked_candidate_only=6")
    print("blocked_boundary_only=2")
    print("blocked_insufficient=0")
    print("blocked_source_unverified=0")
    print("blocked_out_of_scope=0")
    print("controlled_loop_ready=false")
    print(f"primary_verdict={PRIMARY_VERDICT}")
    print("ready_for_human_execution_authority_decision=false")
    print("human_execution_authority_decision_requested_by_vs1_4=false")
    print("loop_execution_authorized=false")
    print("runner_created=false")
    print("micro_sweeps_authorized=false")
    print("local_revision_authorized=false")
    print("registry_activation_authorized=false")
    print("trace_generalization_authorized=false")
    print("component_build_attempted=false")
    print("repair_attempted=false")
    print("candidate_promotion_attempted=false")
    print("next_surface_ranking_attempted=false")
    print("missing_precondition_next_surface_map_created=false")
    print("vs1_5_built=false")
    print("vs1_5_run=false")
    print("next_surfaces_ranked=false")
    print("repair_sequence_created=false")
    print("component_build_authorized=false")
    print("source_inventory_mutated_by_vs1_4=false")
    print("source_contract_mutated_by_vs1_4=false")
    print("vs1_1_source_intake_mutated_by_vs1_4=false")
    print("post_vs0_direction_decision_receipt_mutated_by_vs1_4=false")
    print("vs0_source_artifacts_mutated_by_vs1_4=false")
    print("evidence_yield_branch=CONFIRMATION_YIELD")
    print("diagnostic_yield_present=true")
    print(f"readiness_audit_gate={READINESS_GATE}")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition={PRINT_TRANSITION}")


def emit_typed_stop(exc: AuditFailure) -> None:
    print("BUILD_PHASE_VS1_CONTROLLED_LOOP_READINESS_AUDIT_V0_TYPED_STOP")
    print(f"artifact_id={ARTIFACT_ID}")
    print(f"phase_id={PHASE_ID}")
    print(f"unit_id={UNIT_ID}")
    print(f"readiness_audit_gate={exc.code}")
    print("yield_branch=DIAGNOSTIC_YIELD")
    print(f"missing_or_invalid_source={exc.source}")
    print(f"violating_component={exc.component}")
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
        SOURCE_INVENTORY_JSON,
        SOURCE_INVENTORY_MD,
        SOURCE_CONTRACT_JSON,
        SOURCE_CONTRACT_MD,
        SOURCE_INTAKE_JSON,
        DIRECTION_JSON,
        SOURCE_INTAKE_MD,
        DIRECTION_MD,
    ]:
        require_file(root, rel_path)
    inventory = load_json(root, SOURCE_INVENTORY_JSON)
    contract = load_json(root, SOURCE_CONTRACT_JSON)
    load_json(root, SOURCE_INTAKE_JSON)
    load_json(root, DIRECTION_JSON)
    validate_source_inputs(inventory, contract)
    before_hashes = capture_source_hashes(root)
    audit = build_audit(root, inventory)
    md = build_markdown(audit)
    validate_audit(audit, md)
    output_json = root / OUTPUT_JSON
    output_md = root / OUTPUT_MD
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
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
    except AuditFailure as exc:
        emit_typed_stop(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
