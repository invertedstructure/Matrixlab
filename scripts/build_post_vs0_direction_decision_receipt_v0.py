#!/usr/bin/env python3

"""Build the post-VS0 human direction decision receipt."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT = "scripts/build_post_vs0_direction_decision_receipt_v0.py"
EXPECTED_HEAD = "18324fd7d82da4a5f9210c1e30d94e8fe5ed783b"
CLOSURE_PATH = "docs/matrixlabs/phase_vs0/phase_vs0_closure_v0.json"
OUTPUT_JSON = (
    "docs/matrixlabs/phase_vs1/post_vs0_direction_decision_receipt_v0.json"
)
OUTPUT_MD = "docs/matrixlabs/phase_vs1/post_vs0_direction_decision_receipt_v0.md"

SOURCE_CLOSURE_GATE = (
    "VS0_6_PHASE_CLOSURE_PASS_FIRST_A_TO_F_SPECIMEN_WITH_TYPED_STOPS_"
    "AND_EVIDENCE_YIELD"
)
SOURCE_PHASE_STATUS = (
    "PHASE_VS0_PASS_FIRST_A_TO_F_SPECIMEN_WITH_TYPED_NEGATIVE_STOPS_"
    "AND_EVIDENCE_YIELD"
)
RECEIPT_GATE = "POST_VS0_DIRECTION_DECISION_RECEIPT_PASS"
RECEIPT_TRANSITION = "ADVANCE(VS1_1_POST_VS0_SOURCE_INTAKE_PENDING)"
PRINT_TRANSITION = (
    "ADVANCE(BOOKKEEPING_COMMIT_POST_VS0_DIRECTION_DECISION_RECEIPT_V0_PENDING)"
)


class DirectionReceiptFailure(RuntimeError):
    def __init__(
        self,
        code: str,
        *,
        field: str = "NONE",
        expected: object = "NONE",
        actual: object = "NONE",
    ) -> None:
        super().__init__(code)
        self.code = code
        self.field = field
        self.expected = expected
        self.actual = actual


def fail(
    code: str,
    *,
    field: str = "NONE",
    expected: object = "NONE",
    actual: object = "NONE",
) -> None:
    raise DirectionReceiptFailure(
        code,
        field=field,
        expected=expected,
        actual=actual,
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
            "STOP_POST_VS0_DIRECTION_SOURCE_CLOSURE_INVALID",
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
            "STOP_POST_VS0_DIRECTION_SOURCE_CLOSURE_INVALID",
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
        if path.startswith("docs/matrixlabs/phase_vs0/"):
            fail(
                "STOP_POST_VS0_DIRECTION_VS0_ARTIFACTS_MUTATED",
                field="dirty_vs0_path",
                expected="no dirty VS0 artifacts",
                actual=line,
            )
        fail(
            "STOP_POST_VS0_DIRECTION_SOURCE_CLOSURE_INVALID",
            field="dirty_scope",
            expected="only receipt, baseline_share, or discussion_packets",
            actual=line,
        )


def require_head(root: Path) -> None:
    head = run_git(root, ["rev-parse", "HEAD"])
    if head != EXPECTED_HEAD:
        fail(
            "STOP_POST_VS0_DIRECTION_SOURCE_CLOSURE_INVALID",
            field="HEAD",
            expected=EXPECTED_HEAD,
            actual=head,
        )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_closure(root: Path) -> dict[str, Any]:
    path = root / CLOSURE_PATH
    if not path.is_file():
        fail(
            "STOP_POST_VS0_DIRECTION_SOURCE_CLOSURE_INVALID",
            field="source_closure_path",
            expected=CLOSURE_PATH,
            actual="missing",
        )
    try:
        closure = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(
            "STOP_POST_VS0_DIRECTION_SOURCE_CLOSURE_INVALID",
            field="source_closure_json",
            expected="valid JSON object",
            actual=str(exc),
        )
    if not isinstance(closure, dict):
        fail(
            "STOP_POST_VS0_DIRECTION_SOURCE_CLOSURE_INVALID",
            field="source_closure_json",
            expected="object",
            actual=type(closure).__name__,
        )
    return closure


def get_value(obj: dict[str, Any], path: str, default: Any = None) -> Any:
    current: Any = obj
    for part in path.split("."):
        if not isinstance(current, dict):
            return default
        current = current.get(part, default)
    return current


def require_closure_field(
    closure: dict[str, Any],
    path: str,
    expected: Any,
) -> None:
    got = get_value(closure, path)
    if got != expected:
        fail(
            "STOP_POST_VS0_DIRECTION_SOURCE_CLOSURE_INVALID",
            field=path,
            expected=expected,
            actual=got,
        )


def verify_source_closure(closure: dict[str, Any]) -> None:
    expected_fields = {
        "closure_id": "phase_vs0_closure_v0",
        "phase_id": "PHASE_VS0",
        "phase_name": "A_TO_F_FIRST_SPECIMEN_RUNTIME_V0",
        "phase_step": "VS0.6",
        "closure_role": "PHASE_CLOSURE_ONLY",
        "closure_gate": SOURCE_CLOSURE_GATE,
        "phase_status": SOURCE_PHASE_STATUS,
        "closure_claim_scope.phase_vs0_closed": True,
        "next_lawful_surface.surface_name": "POST_VS0_DIRECTION_DECISION_SURFACE",
        "next_lawful_surface.surface_named_by_closure": True,
        "next_lawful_surface.surface_artifact_created_by_closure": False,
        "next_lawful_surface.human_decision_required": True,
        "next_lawful_surface.machine_may_select_next_phase": False,
        "next_lawful_surface.next_phase_auto_selected": False,
        "next_lawful_surface.recommended_options_are_non_binding": True,
    }
    for path, expected in expected_fields.items():
        require_closure_field(closure, path, expected)


def build_receipt(source_closure_sha: str) -> dict[str, Any]:
    return {
        "schema_version": "matrixlabs_post_vs0_direction_decision_receipt_v0",
        "decision_receipt_id": "post_vs0_direction_decision_receipt_v0",
        "receipt_role": "POST_VS0_DIRECTION_DECISION_ONLY",
        "source_phase": "PHASE_VS0",
        "target_phase": "PHASE_VS1",
        "source_closure": {
            "source_closure_commit_sha": EXPECTED_HEAD,
            "source_closure_id": "phase_vs0_closure_v0",
            "source_closure_path": CLOSURE_PATH,
            "source_closure_sha256": source_closure_sha,
            "source_closure_gate": SOURCE_CLOSURE_GATE,
            "source_phase_status": SOURCE_PHASE_STATUS,
            "source_phase_vs0_closed": True,
        },
        "source_next_surface": {
            "named_surface": "POST_VS0_DIRECTION_DECISION_SURFACE",
            "surface_named_by_vs0_6": True,
            "surface_artifact_created_by_vs0_6": False,
            "human_decision_required": True,
            "machine_may_select_next_phase": False,
            "next_phase_auto_selected": False,
            "recommended_options_are_non_binding": True,
        },
        "decision": {
            "decision_status": "POST_VS0_DIRECTION_DECISION_ACCEPTED",
            "decision": "DECISION_OPEN_PHASE_VS1_SOURCE_INTAKE",
            "decision_source": "HUMAN_DIRECTION",
            "decision_scope": (
                "VS1_SOURCE_INTAKE_AND_CONTRACT_DEFINITION_PREPARATION_ONLY"
            ),
            "decision_is_machine_selected": False,
            "recommended_option_selected_by_machine": False,
        },
        "allowed_scope": {
            "vs1_1_source_intake_may_be_built": True,
            "vs1_1_source_intake_may_be_run_after_receipt_commit": True,
            "vs1_2_contract_definition_preparation_may_be_reached_if_vs1_1_passes": True,
        },
        "forbidden_scope": {
            "controlled_loop_execution_authorized": False,
            "runner_creation_authorized": False,
            "runner_authority_created": False,
            "move_execution_authorized": False,
            "micro_sweeps_authorized": False,
            "registry_activation_authorized": False,
            "registry_promotion_authorized": False,
            "trace_generalization_authorized": False,
            "performance_claim_authorized": False,
            "scale_claim_authorized": False,
            "total_coverage_claim_authorized": False,
            "next_phase_selected_by_machine": False,
            "vs1_1_executed_by_this_receipt": False,
            "vs1_2_executed_by_this_receipt": False,
        },
        "next_unit": {
            "next_unit_id": "VS1_1_POST_VS0_SOURCE_INTAKE",
            "next_artifact": "phase_vs1_post_vs0_source_intake_v0",
            "next_unit_authorized_scope": "SOURCE_INTAKE_ONLY",
            "next_unit_execution_performed_by_this_receipt": False,
        },
        "source_preservation": {
            "vs0_6_closure_mutated_by_direction_receipt": False,
            "vs0_artifacts_mutated_by_direction_receipt": False,
        },
        "receipt_gate": RECEIPT_GATE,
        "terminal_transition": RECEIPT_TRANSITION,
        "failures": [],
    }


def render_markdown() -> str:
    return """# Post-VS0 direction decision receipt v0

## Status

POST_VS0_DIRECTION_DECISION_RECEIPT_PASS

## Source closure

- source phase: PHASE_VS0
- source closure id: phase_vs0_closure_v0
- source closure commit: 18324fd7d82da4a5f9210c1e30d94e8fe5ed783b
- source closure gate: VS0_6_PHASE_CLOSURE_PASS_FIRST_A_TO_F_SPECIMEN_WITH_TYPED_STOPS_AND_EVIDENCE_YIELD
- source phase status: PHASE_VS0_PASS_FIRST_A_TO_F_SPECIMEN_WITH_TYPED_NEGATIVE_STOPS_AND_EVIDENCE_YIELD
- Phase VS0 closed: true

## Decision

- decision: DECISION_OPEN_PHASE_VS1_SOURCE_INTAKE
- decision source: HUMAN_DIRECTION
- allowed scope: VS1_SOURCE_INTAKE_AND_CONTRACT_DEFINITION_PREPARATION_ONLY
- machine selected next phase: false

## Allowed

- VS1.1 source intake may be built
- VS1.1 source intake may run after this receipt is committed
- VS1.2 contract definition preparation may be reached only if VS1.1 passes

## Forbidden

- controlled loop execution authorized: false
- runner creation authorized: false
- move execution authorized: false
- micro-sweeps authorized: false
- registry activation authorized: false
- trace generalization authorized: false
- performance claim authorized: false
- scale claim authorized: false
- next phase selected by machine: false

## Next unit

VS1_1_POST_VS0_SOURCE_INTAKE

## Terminal transition

ADVANCE(VS1_1_POST_VS0_SOURCE_INTAKE_PENDING)

## Non-claim

This receipt opens VS1.1 source intake only. It does not authorize controlled-loop execution, runner creation, move execution, micro-sweeps, registry activation, trace generalization, optimization claims, total coverage claims, or machine-selected next phase.
"""


def markdown_contains_post_vs0_direction_overclaim(md: str) -> list[str]:
    hits: list[str] = []
    allowed_patterns = [
        r"\bcontrolled loop execution authorized\s*[:=]\s*false\b",
        r"\brunner creation authorized\s*[:=]\s*false\b",
        r"\brunner authority created\s*[:=]\s*false\b",
        r"\bmove execution authorized\s*[:=]\s*false\b",
        r"\bmicro-sweeps authorized\s*[:=]\s*false\b",
        r"\bregistry activation authorized\s*[:=]\s*false\b",
        r"\bregistry promotion authorized\s*[:=]\s*false\b",
        r"\btrace generalization authorized\s*[:=]\s*false\b",
        r"\bperformance claim authorized\s*[:=]\s*false\b",
        r"\bscale claim authorized\s*[:=]\s*false\b",
        r"\btotal coverage claim authorized\s*[:=]\s*false\b",
        r"\bnext phase selected by machine\s*[:=]\s*false\b",
        r"\bmachine selected next phase\s*[:=]\s*false\b",
        r"\bdoes not authorize controlled-loop execution\b",
        r"\bdoes not authorize .*runner creation\b",
        r"\bdoes not authorize .*move execution\b",
        r"\bdoes not authorize .*micro-sweeps\b",
        r"\bdoes not authorize .*registry activation\b",
        r"\bdoes not authorize .*trace generalization\b",
        r"\bdoes not authorize .*optimization claims\b",
        r"\bdoes not authorize .*total coverage claims\b",
        r"\bdoes not authorize .*machine-selected next phase\b",
        r"\bopens vs1\.1 source intake only\b",
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


def fail_for_markdown_overclaims(hits: list[str]) -> None:
    fail(
        "STOP_POST_VS0_DIRECTION_SOURCE_CLOSURE_INVALID",
        field="markdown_overclaim_guard",
        expected=[],
        actual=hits,
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
        "BUILD_POST_VS0_DIRECTION_DECISION_RECEIPT_V0_COMPLETE",
        "decision_receipt_id=post_vs0_direction_decision_receipt_v0",
        "schema_version=matrixlabs_post_vs0_direction_decision_receipt_v0",
        "receipt_role=POST_VS0_DIRECTION_DECISION_ONLY",
        "source_phase=PHASE_VS0",
        "target_phase=PHASE_VS1",
        f"source_closure_commit_sha={EXPECTED_HEAD}",
        "source_closure_id=phase_vs0_closure_v0",
        f"source_closure_gate={SOURCE_CLOSURE_GATE}",
        f"source_phase_status={SOURCE_PHASE_STATUS}",
        "source_phase_vs0_closed=true",
        "decision_status=POST_VS0_DIRECTION_DECISION_ACCEPTED",
        "decision=DECISION_OPEN_PHASE_VS1_SOURCE_INTAKE",
        "decision_source=HUMAN_DIRECTION",
        "decision_scope=VS1_SOURCE_INTAKE_AND_CONTRACT_DEFINITION_PREPARATION_ONLY",
        "decision_is_machine_selected=false",
        "vs1_1_source_intake_may_be_built=true",
        "vs1_1_source_intake_may_be_run_after_receipt_commit=true",
        "controlled_loop_execution_authorized=false",
        "runner_creation_authorized=false",
        "runner_authority_created=false",
        "move_execution_authorized=false",
        "micro_sweeps_authorized=false",
        "registry_activation_authorized=false",
        "registry_promotion_authorized=false",
        "trace_generalization_authorized=false",
        "performance_claim_authorized=false",
        "scale_claim_authorized=false",
        "total_coverage_claim_authorized=false",
        "next_phase_selected_by_machine=false",
        "vs1_1_executed_by_this_receipt=false",
        "vs1_2_executed_by_this_receipt=false",
        "next_unit_id=VS1_1_POST_VS0_SOURCE_INTAKE",
        "next_artifact=phase_vs1_post_vs0_source_intake_v0",
        "next_unit_authorized_scope=SOURCE_INTAKE_ONLY",
        "next_unit_execution_performed_by_this_receipt=false",
        "vs0_6_closure_mutated_by_direction_receipt=false",
        "vs0_artifacts_mutated_by_direction_receipt=false",
        f"receipt_gate={RECEIPT_GATE}",
        "commit_created=false",
        "push_executed=false",
        f"terminal_transition={PRINT_TRANSITION}",
    ]
    print("\n".join(lines))


def print_typed_stop(exc: DirectionReceiptFailure) -> None:
    lines = [
        "BUILD_POST_VS0_DIRECTION_DECISION_RECEIPT_V0_TYPED_STOP",
        "decision_receipt_id=post_vs0_direction_decision_receipt_v0",
        f"stop_code={exc.code}",
        f"violating_field={exc.field}",
        f"expected_value={exc.expected}",
        f"actual_value={exc.actual}",
        "vs1_1_executed_by_this_receipt=false",
        "controlled_loop_execution_authorized=false",
        "runner_authority_created=false",
        "commit_created=false",
        "push_executed=false",
        f"terminal_transition=STOP({exc.code})",
    ]
    print("\n".join(lines))


def run() -> int:
    root = detect_repo_root(Path.cwd())
    require_head(root)
    validate_dirty_scope(root)
    closure = load_closure(root)
    verify_source_closure(closure)
    before_closure_hash = sha256(root / CLOSURE_PATH)

    markdown = render_markdown()
    overclaim_hits = markdown_contains_post_vs0_direction_overclaim(markdown)
    if overclaim_hits:
        fail_for_markdown_overclaims(overclaim_hits)

    receipt = build_receipt(before_closure_hash)
    write_json(root, receipt)
    write_markdown(root, markdown)

    after_closure_hash = sha256(root / CLOSURE_PATH)
    if after_closure_hash != before_closure_hash:
        fail(
            "STOP_POST_VS0_DIRECTION_SOURCE_CLOSURE_MUTATED",
            field="source_closure_sha256",
            expected=before_closure_hash,
            actual=after_closure_hash,
        )
    validate_dirty_scope(root)
    print_complete()
    return 0


def main() -> int:
    try:
        return run()
    except DirectionReceiptFailure as exc:
        print_typed_stop(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
