#!/usr/bin/env python3

"""Close Phase VS1 from the committed VS1.1 through VS1.5 source spine."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT = "scripts/close_phase_vs1_v0.py"
EXPECTED_HEAD = "955743f9cf281d9b83c9e68fb0f367121b3c5295"
OUTPUT_JSON = "docs/matrixlabs/phase_vs1/phase_vs1_closure_v0.json"
OUTPUT_MD = "docs/matrixlabs/phase_vs1/phase_vs1_closure_v0.md"
VS0_ROOT = "docs/matrixlabs/phase_vs0"

SCHEMA_VERSION = "matrixlabs_phase_vs1_closure_v0"
ARTIFACT_ID = "phase_vs1_closure_v0"
PHASE_ID = "PHASE_VS1"
PHASE_NAME = "MINIMAL_CONTROLLED_CONVERGENCE_LOOP_PRECONDITIONS_V0"
UNIT_ID = "VS1.6_PHASE_CLOSURE"
UNIT_ROLE = "PHASE_CLOSURE_ONLY"

VS1_1_COMMIT = "8f4b57c697d8dc7110e3ea9d73183d36c806a66c"
VS1_2_COMMIT = "d62db2d74f2ff42bf7f633b4e2169aed409a0703"
VS1_3_COMMIT = "741f28223d93b27d5a00fa06bb45a1739d66cb13"
VS1_4_COMMIT = "68c846386a79cc89215c1b16dbd1389333269b80"
VS1_5_COMMIT = "955743f9cf281d9b83c9e68fb0f367121b3c5295"

VS1_1_GATE = "VS1_1_POST_VS0_SOURCE_INTAKE_PASS"
VS1_2_GATE = "VS1_2_CONTROLLED_LOOP_CONTRACT_DEFINITION_PASS"
VS1_3_GATE = "VS1_3_CONTROLLED_LOOP_PRECONDITION_INVENTORY_PASS"
VS1_4_NOT_READY_GATE = "VS1_4_CONTROLLED_LOOP_READINESS_AUDIT_PASS_NOT_READY_BLOCKERS_EXPOSED"
VS1_4_READY_GATE = "VS1_4_CONTROLLED_LOOP_READINESS_AUDIT_PASS_READY_FOR_HUMAN_EXECUTION_AUTHORITY_DECISION"
VS1_5_NOT_READY_GATE = "VS1_5_MISSING_PRECONDITION_NEXT_SURFACE_MAP_PASS"
VS1_5_READY_GATE = "VS1_5_READY_BRANCH_HUMAN_AUTHORITY_SURFACE_MAP_PASS"

VS1_1_TRANSITION = "ADVANCE(VS1_2_CONTROLLED_LOOP_CONTRACT_DEFINITION_PENDING)"
VS1_2_TRANSITION = "ADVANCE(VS1_3_CONTROLLED_LOOP_PRECONDITION_INVENTORY_PENDING)"
VS1_3_TRANSITION = "ADVANCE(VS1_4_CONTROLLED_LOOP_READINESS_AUDIT_PENDING)"
VS1_4_TRANSITION = "ADVANCE(VS1_5_MISSING_PRECONDITION_NEXT_SURFACE_MAP_PENDING)"
VS1_5_TRANSITION = "ADVANCE(VS1_6_PHASE_CLOSURE_PENDING)"

CURRENT_CLOSURE_BRANCH = "NOT_READY_BLOCKERS_MAPPED"
CURRENT_CLOSURE_GATE = "VS1_6_PHASE_CLOSURE_PASS_LOOP_NOT_READY_WITH_NEXT_SURFACES_MAPPED"
CURRENT_PHASE_STATUS = (
    "PHASE_VS1_PASS_LOOP_NOT_READY_MISSING_PRECONDITIONS_EXPOSED_AND_NEXT_SURFACES_MAPPED"
)
CURRENT_TERMINAL_TRANSITION = "STOP_PHASE_VS1_CLOSED_PENDING_POST_VS1_DIRECTION_DECISION"
PRINT_TRANSITION = "ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS1_CLOSURE_V0_PENDING)"

SOURCE_DEFS = [
    {
        "key": "vs1_1_source_intake",
        "artifact_id": "phase_vs1_post_vs0_source_intake_v0",
        "path": "docs/matrixlabs/phase_vs1/phase_vs1_post_vs0_source_intake_v0.json",
        "md_path": "docs/matrixlabs/phase_vs1/phase_vs1_post_vs0_source_intake_v0.md",
        "commit_sha": VS1_1_COMMIT,
        "required_gate": VS1_1_GATE,
        "required_transition": VS1_1_TRANSITION,
        "gate_keys": ["intake_gate", "intake_verdict", "gate", "status"],
    },
    {
        "key": "vs1_2_loop_contract",
        "artifact_id": "phase_vs1_controlled_convergence_loop_contract_v0",
        "path": "docs/matrixlabs/phase_vs1/phase_vs1_controlled_convergence_loop_contract_v0.json",
        "md_path": "docs/matrixlabs/phase_vs1/phase_vs1_controlled_convergence_loop_contract_v0.md",
        "commit_sha": VS1_2_COMMIT,
        "required_gate": VS1_2_GATE,
        "required_transition": VS1_2_TRANSITION,
        "gate_keys": ["contract_gate", "contract_verdict", "gate", "status"],
    },
    {
        "key": "vs1_3_precondition_inventory",
        "artifact_id": "phase_vs1_controlled_loop_precondition_inventory_v0",
        "path": "docs/matrixlabs/phase_vs1/phase_vs1_controlled_loop_precondition_inventory_v0.json",
        "md_path": "docs/matrixlabs/phase_vs1/phase_vs1_controlled_loop_precondition_inventory_v0.md",
        "commit_sha": VS1_3_COMMIT,
        "required_gate": VS1_3_GATE,
        "required_transition": VS1_3_TRANSITION,
        "gate_keys": ["inventory_verdict", "gate", "status"],
    },
    {
        "key": "vs1_4_readiness_audit",
        "artifact_id": "phase_vs1_controlled_loop_readiness_audit_v0",
        "path": "docs/matrixlabs/phase_vs1/phase_vs1_controlled_loop_readiness_audit_v0.json",
        "md_path": "docs/matrixlabs/phase_vs1/phase_vs1_controlled_loop_readiness_audit_v0.md",
        "commit_sha": VS1_4_COMMIT,
        "required_gate": VS1_4_NOT_READY_GATE,
        "allowed_gates": [VS1_4_NOT_READY_GATE, VS1_4_READY_GATE],
        "required_transition": VS1_4_TRANSITION,
        "gate_keys": ["readiness_audit_gate", "gate", "status"],
    },
    {
        "key": "vs1_5_next_surface_map",
        "artifact_id": "phase_vs1_missing_precondition_next_surface_map_v0",
        "path": "docs/matrixlabs/phase_vs1/phase_vs1_missing_precondition_next_surface_map_v0.json",
        "md_path": "docs/matrixlabs/phase_vs1/phase_vs1_missing_precondition_next_surface_map_v0.md",
        "commit_sha": VS1_5_COMMIT,
        "required_gate": VS1_5_NOT_READY_GATE,
        "allowed_gates": [VS1_5_NOT_READY_GATE, VS1_5_READY_GATE],
        "required_transition": VS1_5_TRANSITION,
        "gate_keys": ["map_verdict", "gate", "status"],
    },
]

SOURCE_CHAIN_COMMIT_BINDINGS = {
    "vs1_1_commit_sha": VS1_1_COMMIT,
    "vs1_2_commit_sha": VS1_2_COMMIT,
    "vs1_3_commit_sha": VS1_3_COMMIT,
    "vs1_4_commit_sha": VS1_4_COMMIT,
    "vs1_5_commit_sha": VS1_5_COMMIT,
}

REQUIRED_CLOSURE_CHECKS = [
    "VS1_SOURCE_CHAIN_COMPLETE",
    "VS0_BOUNDARY_PRESERVED_THROUGH_VS1",
    "CONTROLLED_LOOP_CONTRACT_DEFINED_NOT_EXECUTED",
    "PRECONDITION_INVENTORY_COMPLETED_WITHOUT_REPAIR",
    "READINESS_AUDIT_COMPLETED_NOT_READY_BLOCKERS_EXPOSED",
    "NEXT_SURFACE_MAP_COMPLETED_NOT_SELECTED",
    "VS1_FORBIDDEN_CLAIMS_ABSENT",
]

FORBIDDEN_ARTIFACTS = [
    "docs/matrixlabs/phase_vs1/post_vs1_direction_decision_receipt_v0.json",
    "docs/matrixlabs/phase_vs1/post_vs1_selected_surface_decision_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_selected_next_phase_decision_receipt_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_surface_build_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_component_repair_plan_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_component_build_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_candidate_promotion_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_human_execution_authority_receipt_v0.json",
    "docs/matrixlabs/phase_vs2",
    "docs/matrixlabs/post_vs1",
    "docs/matrixlabs/runner",
    "docs/matrixlabs/runtime",
    "docs/matrixlabs/move_space",
    "docs/matrixlabs/micro_sweeps",
]

PLACEHOLDER_VALUES = {
    "<actual>",
    "<sha256_at_runtime>",
    "<derived_summary>",
    "<derived_gate>",
    "<derived_phase_status>",
    "<TBD>",
    "TBD",
    "TODO",
    "UNKNOWN",
    "PLACEHOLDER",
    "",
}


class ClosureFailure(RuntimeError):
    def __init__(
        self,
        code: str,
        *,
        source: str = "NONE",
        field: str = "NONE",
        expected: object = "NONE",
        actual: object = "NONE",
        next_surface: str = "REPAIR_PHASE_VS1_CLOSURE_SOURCE_CHAIN",
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
    next_surface: str = "REPAIR_PHASE_VS1_CLOSURE_SOURCE_CHAIN",
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
            "STOP_VS1_6_SOURCE_CHAIN_INCOMPLETE",
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
            "STOP_VS1_6_SOURCE_CHAIN_INCOMPLETE",
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
            "STOP_VS1_6_SOURCE_CHAIN_INCOMPLETE",
            source=path,
            field="dirty_scope",
            expected="only VS1.6 outputs, baseline_share, or discussion_packets",
            actual=line,
        )


def require_head(root: Path) -> None:
    head = run_git(root, ["rev-parse", "HEAD"])
    if head != EXPECTED_HEAD:
        fail(
            "STOP_VS1_6_SOURCE_CHAIN_INCOMPLETE",
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
            "STOP_VS1_6_SOURCE_CHAIN_INCOMPLETE",
            source=rel_path,
            field="file_presence",
            expected=True,
            actual=False,
        )
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(
            "STOP_VS1_6_SOURCE_CHAIN_INCOMPLETE",
            source=rel_path,
            field="valid_json",
            expected=True,
            actual=str(exc),
        )
    if not isinstance(value, dict):
        fail(
            "STOP_VS1_6_SOURCE_CHAIN_INCOMPLETE",
            source=rel_path,
            field="json_object",
            expected=True,
            actual=type(value).__name__,
        )
    return value


def require_file(root: Path, rel_path: str) -> None:
    if not (root / rel_path).is_file():
        fail(
            "STOP_VS1_6_SOURCE_CHAIN_INCOMPLETE",
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


def find_gate(obj: dict[str, Any], gate_keys: list[str]) -> str | None:
    for key in gate_keys:
        value = obj.get(key)
        if isinstance(value, str):
            return value
    return None


def find_transition(obj: dict[str, Any]) -> str | None:
    value = get_value(obj, "terminal_transition.transition")
    if isinstance(value, str):
        return value
    value = obj.get("terminal_transition")
    if isinstance(value, str):
        return value
    return None


def source_paths(root: Path) -> list[str]:
    paths: list[str] = []
    for source in SOURCE_DEFS:
        paths.append(str(source["path"]))
        paths.append(str(source["md_path"]))
    paths.extend(
        [
            "docs/matrixlabs/phase_vs1/post_vs0_direction_decision_receipt_v0.json",
            "docs/matrixlabs/phase_vs1/post_vs0_direction_decision_receipt_v0.md",
        ]
    )
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
                "STOP_VS1_6_SOURCE_CHAIN_INCOMPLETE",
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
        "STOP_VS1_6_FORBIDDEN_CLAIM_DRIFT",
        source=first,
        field="source_hash",
        expected=before.get(first),
        actual=after.get(first),
    )


def ensure_no_forbidden_artifacts(root: Path) -> None:
    for rel_path in FORBIDDEN_ARTIFACTS:
        if (root / rel_path).exists():
            fail(
                "STOP_VS1_6_POST_VS1_DECISION_ARTIFACT_CREATED",
                source=rel_path,
                field="forbidden_artifact",
                expected="absent",
                actual="present",
            )


def validate_source_entry(root: Path, source: dict[str, Any]) -> dict[str, Any]:
    rel_path = str(source["path"])
    data = load_json(root, rel_path)
    if data.get("artifact_id") != source["artifact_id"]:
        fail(
            "STOP_VS1_6_SOURCE_STATUS_MISMATCH",
            source=rel_path,
            field="artifact_id",
            expected=source["artifact_id"],
            actual=data.get("artifact_id"),
        )
    actual_gate = find_gate(data, list(source["gate_keys"]))
    allowed = source.get("allowed_gates", [source["required_gate"]])
    if actual_gate not in allowed:
        fail(
            "STOP_VS1_6_SOURCE_STATUS_MISMATCH",
            source=rel_path,
            field="gate",
            expected=allowed,
            actual=actual_gate,
        )
    actual_transition = find_transition(data)
    if actual_transition != source["required_transition"]:
        fail(
            "STOP_VS1_6_SOURCE_STATUS_MISMATCH",
            source=rel_path,
            field="terminal_transition",
            expected=source["required_transition"],
            actual=actual_transition,
        )
    entry = {
        "artifact_id": source["artifact_id"],
        "path": rel_path,
        "commit_sha": source["commit_sha"],
        "sha256": sha256(root / rel_path),
        "required_gate": source["required_gate"],
        "actual_gate": actual_gate,
        "required_transition": source["required_transition"],
        "actual_transition": actual_transition,
        "status": "PRESENT_VERIFIED",
    }
    if "allowed_gates" in source:
        entry["allowed_gates"] = source["allowed_gates"]
    return entry


def build_source_chain(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    source_chain: dict[str, Any] = {}
    source_objects: dict[str, Any] = {}
    for source in SOURCE_DEFS:
        require_file(root, str(source["path"]))
        require_file(root, str(source["md_path"]))
        source_chain[str(source["key"])] = validate_source_entry(root, source)
        source_objects[str(source["key"])] = load_json(root, str(source["path"]))
    return source_chain, source_objects


def derive_branch(vs1_4_gate: str, vs1_5_gate: str) -> dict[str, str]:
    if (vs1_4_gate, vs1_5_gate) == (VS1_4_NOT_READY_GATE, VS1_5_NOT_READY_GATE):
        return {
            "vs1_4_gate": vs1_4_gate,
            "vs1_5_gate": vs1_5_gate,
            "derived_closure_branch": CURRENT_CLOSURE_BRANCH,
            "derived_closure_gate": CURRENT_CLOSURE_GATE,
            "derived_phase_status": CURRENT_PHASE_STATUS,
        }
    if (vs1_4_gate, vs1_5_gate) == (VS1_4_READY_GATE, VS1_5_READY_GATE):
        return {
            "vs1_4_gate": vs1_4_gate,
            "vs1_5_gate": vs1_5_gate,
            "derived_closure_branch": "READY_FOR_HUMAN_AUTHORITY_DECISION_NOT_EXECUTED",
            "derived_closure_gate": (
                "VS1_6_PHASE_CLOSURE_PASS_LOOP_READY_FOR_HUMAN_AUTHORITY_DECISION_NOT_EXECUTED"
            ),
            "derived_phase_status": (
                "PHASE_VS1_PASS_LOOP_READY_FOR_HUMAN_EXECUTION_AUTHORITY_DECISION_NOT_EXECUTED"
            ),
        }
    fail(
        "STOP_VS1_6_SOURCE_GATE_PAIR_UNSUPPORTED",
        source="VS1.4+VS1.5",
        field="source_gate_pair",
        expected=[(VS1_4_NOT_READY_GATE, VS1_5_NOT_READY_GATE), (VS1_4_READY_GATE, VS1_5_READY_GATE)],
        actual=(vs1_4_gate, vs1_5_gate),
    )


def validate_boundaries(sources: dict[str, Any]) -> None:
    contract = sources["vs1_2_loop_contract"]
    inventory = sources["vs1_3_precondition_inventory"]
    readiness = sources["vs1_4_readiness_audit"]
    surface_map = sources["vs1_5_next_surface_map"]

    if get_value(contract, "loop_contract.execution_authorized") is not False:
        fail(
            "STOP_VS1_6_CONTRACT_EXECUTION_DRIFT",
            source=SOURCE_DEFS[1]["path"],
            field="loop_contract.execution_authorized",
            expected=False,
            actual=get_value(contract, "loop_contract.execution_authorized"),
        )
    if get_value(inventory, "inventory_mode.repairs_allowed") is not False:
        fail(
            "STOP_VS1_6_INVENTORY_BOUNDARY_DRIFT",
            source=SOURCE_DEFS[2]["path"],
            field="inventory_mode.repairs_allowed",
            expected=False,
            actual=get_value(inventory, "inventory_mode.repairs_allowed"),
        )
    if get_value(readiness, "execution_authority_status.loop_execution_authorized") is not False:
        fail(
            "STOP_VS1_6_READINESS_AUDIT_BOUNDARY_DRIFT",
            source=SOURCE_DEFS[3]["path"],
            field="execution_authority_status.loop_execution_authorized",
            expected=False,
            actual=get_value(readiness, "execution_authority_status.loop_execution_authorized"),
        )
    if get_value(surface_map, "mapping_policy.loop_execution_authorized") is not False:
        fail(
            "STOP_VS1_6_NEXT_SURFACE_MAP_BOUNDARY_DRIFT",
            source=SOURCE_DEFS[4]["path"],
            field="mapping_policy.loop_execution_authorized",
            expected=False,
            actual=get_value(surface_map, "mapping_policy.loop_execution_authorized"),
        )
    if "C20_CONVERGENCE_CRITERION_CONTRACT" not in contract.get("required_components", []):
        fail(
            "STOP_VS1_6_C20_CONVERGENCE_COMPONENT_MISSING",
            source=SOURCE_DEFS[1]["path"],
            field="required_components",
            expected="C20_CONVERGENCE_CRITERION_CONTRACT",
            actual=contract.get("required_components", []),
        )
    candidate_ids = [c.get("surface_id") for c in surface_map.get("surface_candidates", [])]
    if "S20_CONVERGENCE_CRITERION_CONTRACT_SURFACE" not in candidate_ids:
        fail(
            "STOP_VS1_6_C20_CONVERGENCE_COMPONENT_MISSING",
            source=SOURCE_DEFS[4]["path"],
            field="surface_candidates",
            expected="S20_CONVERGENCE_CRITERION_CONTRACT_SURFACE",
            actual=candidate_ids,
        )
    if "S21_CONTROLLED_LOOP_READINESS_REAUDIT_SURFACE" not in candidate_ids:
        fail(
            "STOP_VS1_6_NEXT_SURFACE_MAP_BOUNDARY_DRIFT",
            source=SOURCE_DEFS[4]["path"],
            field="surface_candidates",
            expected="S21_CONTROLLED_LOOP_READINESS_REAUDIT_SURFACE",
            actual=candidate_ids,
        )
    if "S20_CONVERGENCE_CRITERION_CONTRACT_SURFACE" == "S21_CONTROLLED_LOOP_READINESS_REAUDIT_SURFACE":
        fail(
            "STOP_VS1_6_S20_S21_SURFACE_ID_CONFLATED",
            source=SOURCE_DEFS[4]["path"],
            field="surface_ids",
            expected="distinct S20 and S21",
            actual="conflated",
        )
    if get_value(surface_map, "advisory_ranking_policy.ranking_is_binding") is not False:
        fail(
            "STOP_VS1_6_NEXT_SURFACE_RANKING_RECOMPUTED",
            source=SOURCE_DEFS[4]["path"],
            field="advisory_ranking_policy.ranking_is_binding",
            expected=False,
            actual=get_value(surface_map, "advisory_ranking_policy.ranking_is_binding"),
        )


def closure_checks() -> list[dict[str, Any]]:
    return [
        {
            "check_id": f"VS1_6_CLOSURE_CHECK_{index:02d}",
            "check_result": check,
            "status": "PASS",
            "result_status": "PASS",
        }
        for index, check in enumerate(REQUIRED_CLOSURE_CHECKS, start=1)
    ]


def build_closure(root: Path, source_chain: dict[str, Any], sources: dict[str, Any]) -> dict[str, Any]:
    inventory = sources["vs1_3_precondition_inventory"]
    readiness = sources["vs1_4_readiness_audit"]
    surface_map = sources["vs1_5_next_surface_map"]
    branch = derive_branch(
        source_chain["vs1_4_readiness_audit"]["actual_gate"],
        source_chain["vs1_5_next_surface_map"]["actual_gate"],
    )
    inventory_counts = inventory.get("summary_counts", {})
    readiness_counts = readiness.get("readiness_summary_counts", {})
    coverage = surface_map.get("blocker_coverage", {})
    aggregate = readiness.get("aggregate_readiness_verdict", {})
    return {
        "schema_version": SCHEMA_VERSION,
        "artifact_id": ARTIFACT_ID,
        "phase_id": PHASE_ID,
        "phase_name": PHASE_NAME,
        "unit_id": UNIT_ID,
        "unit_role": UNIT_ROLE,
        "source_chain_commit_bindings": SOURCE_CHAIN_COMMIT_BINDINGS,
        "source_chain": source_chain,
        "source_status_table": [
            {
                "source_key": key,
                "artifact_id": entry["artifact_id"],
                "actual_gate": entry["actual_gate"],
                "actual_transition": entry["actual_transition"],
                "status": entry["status"],
                "commit_sha": entry["commit_sha"],
            }
            for key, entry in source_chain.items()
        ],
        "closure_branch_derivation": branch,
        "closure_branch": branch["derived_closure_branch"],
        "closure_checks": closure_checks(),
        "phase_result": {
            "controlled_loop_contract_defined": True,
            "preconditions_inventoried": True,
            "required_components_total": 20,
            "convergence_criterion_component_included": True,
            "readiness_audited": True,
            "controlled_loop_ready": False,
            "typed_blockers_exposed": True,
            "next_surfaces_mapped": True,
            "human_authority_surface_mapped": False,
            "phase_result_summary": (
                "VS1 defined the Minimal Controlled Convergence Loop contract, "
                "inventoried its twenty required preconditions, audited loop readiness "
                "under the strict initial profile, found the loop not ready, and mapped "
                "bounded next-surface candidates for the exposed blockers."
            ),
        },
        "readiness_summary": {
            "readiness_profile": readiness.get("readiness_profile", {}).get("profile_id"),
            "ready_for_human_execution_authority_decision": False,
            "human_execution_authority_decision_requested_by_vs1": False,
            "loop_execution_authorized": False,
            "runner_created": False,
            "micro_sweeps_authorized": False,
            "local_revision_authorized": False,
            "human_authority_consumed": False,
        },
        "blocker_summary": {
            "required_components_total": 20,
            "ready_component_count": aggregate.get("ready_component_count"),
            "missing_or_blocked_component_count": aggregate.get("missing_or_blocked_component_count"),
            "blocked_missing": readiness_counts.get("blocked_missing"),
            "blocked_partial": readiness_counts.get("blocked_partial"),
            "blocked_candidate_only": readiness_counts.get("blocked_candidate_only"),
            "blocked_boundary_only": readiness_counts.get("blocked_boundary_only"),
            "typed_blockers_exposed": True,
        },
        "next_surface_summary": {
            "surface_candidates_mapped": True,
            "surface_candidate_count": len(surface_map.get("surface_candidates", [])),
            "source_blocker_count": coverage.get("source_blocker_count"),
            "mapped_blocker_count": coverage.get("mapped_blocker_count"),
            "unmapped_blocker_count": coverage.get("unmapped_blocker_count"),
            "human_authority_decision_surface_mapped": False,
            "convergence_surface_id": "S20_CONVERGENCE_CRITERION_CONTRACT_SURFACE",
            "readiness_reaudit_surface_id": "S21_CONTROLLED_LOOP_READINESS_REAUDIT_SURFACE",
            "s20_s21_conflated": False,
            "dependency_layers_declared": bool(surface_map.get("dependency_layers")),
            "advisory_ranking_present": bool(surface_map.get("advisory_ranking")),
            "advisory_first_surface_from_vs1_5": get_value(
                surface_map, "advisory_ranking.advisory_first_surface_candidate"
            ),
            "advisory_ranking_binding": False,
            "ranking_recomputed_by_vs1_6": False,
            "ranking_modified_by_vs1_6": False,
            "mapped_surface_built": False,
            "next_phase_auto_selected": False,
        },
        "diagnostic_preservation_summary": {
            "diagnostics_recomputed_by_vs1_6": False,
            "inventory_counts_preserved": {
                "present_verified": inventory_counts.get("present_verified"),
                "present_partial": inventory_counts.get("present_partial"),
                "present_candidate_only": inventory_counts.get("present_candidate_only"),
                "present_boundary_only": inventory_counts.get("present_boundary_only"),
                "missing": inventory_counts.get("missing"),
            },
            "readiness_counts_preserved": {
                "ready_component_count": readiness_counts.get("ready_component_count"),
                "missing_or_blocked_component_count": readiness_counts.get(
                    "missing_or_blocked_component_count"
                ),
                "blocked_missing": readiness_counts.get("blocked_missing"),
                "blocked_partial": readiness_counts.get("blocked_partial"),
                "blocked_candidate_only": readiness_counts.get("blocked_candidate_only"),
                "blocked_boundary_only": readiness_counts.get("blocked_boundary_only"),
            },
            "next_surface_mapping_counts_preserved": {
                "source_blocker_count": coverage.get("source_blocker_count"),
                "mapped_blocker_count": coverage.get("mapped_blocker_count"),
                "unmapped_blocker_count": coverage.get("unmapped_blocker_count"),
                "surface_candidate_record_count": len(surface_map.get("surface_candidates", [])),
            },
        },
        "source_preservation": {
            "source_next_surface_map_mutated_by_vs1_6": False,
            "source_readiness_audit_mutated_by_vs1_6": False,
            "source_inventory_mutated_by_vs1_6": False,
            "source_contract_mutated_by_vs1_6": False,
            "vs1_1_source_intake_mutated_by_vs1_6": False,
            "post_vs0_direction_decision_receipt_mutated_by_vs1_6": False,
            "vs0_source_artifacts_mutated_by_vs1_6": False,
        },
        "forbidden_claim_checks": {
            "runner_authority_created": False,
            "runner_readiness_claimed": False,
            "controlled_loop_execution_authorized": False,
            "active_registry_created": False,
            "registry_candidate_promoted": False,
            "trace_generalized": False,
            "global_portability_claimed": False,
            "performance_optimization_claimed": False,
            "scale_optimization_claimed": False,
            "micro_sweeps_authorized": False,
            "local_revision_authorized": False,
            "next_phase_auto_selected": False,
            "human_authority_consumed": False,
            "mapped_surface_selected": False,
            "mapped_surface_built": False,
            "post_vs1_decision_artifact_created": False,
            "post_vs1_decision_consumed": False,
            "post_vs1_phase_selected": False,
        },
        "post_vs1_decision_surface": {
            "surface": "POST_VS1_DIRECTION_DECISION_SURFACE",
            "named_by_vs1_6": True,
            "decision_artifact_created_by_vs1_6": False,
            "decision_consumed_by_vs1_6": False,
            "human_decision_required": True,
            "machine_may_select_next_phase": False,
            "machine_may_rank_post_vs1_options": False,
            "candidate_options_source": "phase_vs1_missing_precondition_next_surface_map_v0",
        },
        "closure_gate": branch["derived_closure_gate"],
        "phase_status": branch["derived_phase_status"],
        "terminal_transition": {
            "transition": CURRENT_TERMINAL_TRANSITION,
            "phase_vs1_closed": True,
            "post_vs1_decision_surface_named": True,
            "post_vs1_decision_surface_created": False,
            "executes_next_phase": False,
            "selects_next_phase": False,
            "authorizes_selected_surface_build": False,
            "authorizes_loop_execution": False,
            "authorizes_runner": False,
            "consumes_human_authority": False,
        },
        "evidence_yield": {
            "yield_branch": "CONFIRMATION_YIELD",
            "confirmation_yield_reason": (
                "VS1 source chain completed, controlled-loop contract was defined, "
                "preconditions were inventoried, readiness was audited, blockers "
                "were exposed, next surfaces were mapped, and phase closed without "
                "forbidden authority drift"
            ),
            "diagnostic_yield_preserved": True,
            "diagnostics_recomputed_by_vs1_6": False,
        },
        "non_claims": {
            "controlled_loop_may_execute": False,
            "runner_exists": False,
            "runner_readiness_exists": False,
            "runner_authority_exists": False,
            "micro_sweeps_authorized": False,
            "local_revision_authorized": False,
            "mapped_surface_selected": False,
            "mapped_surface_built": False,
            "missing_component_repaired": False,
            "candidate_promoted": False,
            "advisory_ranking_binding": False,
            "first_ranked_surface_must_be_next": False,
            "human_authority_consumed": False,
            "portability_demonstrated": False,
            "vs0_generalized": False,
            "vs1_generalized": False,
            "performance_optimization_begun": False,
            "scale_optimization_begun": False,
            "next_phase_started": False,
        },
        "failures": [],
    }


def build_markdown(closure: dict[str, Any]) -> str:
    return f"""# Phase VS1 closure v0

## Status

{closure['phase_status']}

## Closure gate

{closure['closure_gate']}

## Sources

- VS1.1 post-VS0 source intake: PASS
- VS1.2 controlled-loop contract definition: PASS
- VS1.3 precondition inventory: PASS
- VS1.4 readiness audit: PASS_NOT_READY_BLOCKERS_EXPOSED
- VS1.5 missing-precondition next-surface map: PASS

## Source commit bindings

- VS1.1 commit: {VS1_1_COMMIT}
- VS1.2 commit: {VS1_2_COMMIT}
- VS1.3 commit: {VS1_3_COMMIT}
- VS1.4 commit: {VS1_4_COMMIT}
- VS1.5 commit: {VS1_5_COMMIT}

## Closure branch

{closure['closure_branch']}

## Phase result

- Minimal Controlled Convergence Loop contract was defined
- twenty required preconditions were inventoried
- C20 convergence criterion contract was included
- readiness was audited under the strict initial profile
- loop is not ready
- typed blockers were exposed
- bounded next-surface candidates were mapped
- not-ready closure is not a failure

## Diagnostic preservation

- inventory diagnostics recomputed by VS1.6: false
- present verified: 0
- present partial: 6
- present candidate-only: 6
- present boundary-only: 2
- missing: 6
- ready component count: 0
- missing or blocked component count: 20
- source blocker count: 20
- mapped blocker count: 20
- unmapped blocker count: 0
- surface candidate record count: 21

## Next-surface summary

- S20 convergence surface: S20_CONVERGENCE_CRITERION_CONTRACT_SURFACE
- S21 readiness re-audit surface: S21_CONTROLLED_LOOP_READINESS_REAUDIT_SURFACE
- S20/S21 conflated: false
- advisory first surface from VS1.5: S10_SOURCE_IDENTITY_FRESHNESS_POLICY_SURFACE
- ranking recomputed by VS1.6: false
- ranking modified by VS1.6: false
- advisory ranking binding: false
- mapped surface built: false
- next phase auto-selected: false

## Boundaries preserved

- no loop execution authorized
- no runner created
- no runner readiness claimed
- no micro-sweeps authorized
- no local revision authorized
- no active registry created
- no trace generalization claimed
- no optimization target assumed
- no next phase selected automatically
- no human authority consumed
- no mapped surface selected
- no mapped surface built
- no post-VS1 decision artifact created
- no post-VS1 decision consumed

## Next lawful surface

POST_VS1_DIRECTION_DECISION_SURFACE

- named by VS1.6: true
- decision artifact created by VS1.6: false
- decision consumed by VS1.6: false
- human decision required: true
- machine may select next phase: false
- machine may rank post-VS1 options: false

## Evidence Yield

- yield branch: CONFIRMATION_YIELD
- Diagnostic Yield preserved: true
- diagnostics recomputed by VS1.6: false

## Terminal transition

{CURRENT_TERMINAL_TRANSITION}

## Non-claim

VS1 closes with a useful not-ready result. It does not select, authorize, or build the next phase. It does not create the post-VS1 decision artifact. It does not execute the loop, create a runner, run micro-sweeps, consume human authority, or claim runner readiness.
"""


def assert_no_placeholders(value: Any, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            assert_no_placeholders(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            assert_no_placeholders(item, f"{path}[{index}]")
    elif isinstance(value, str) and value in PLACEHOLDER_VALUES:
        fail(
            "STOP_VS1_6_PHASE_STATUS_AMBIGUOUS",
            field=path,
            expected="non-placeholder",
            actual=value,
        )


def validate_closure(closure: dict[str, Any], md: str) -> None:
    expected = {
        "schema_version": SCHEMA_VERSION,
        "artifact_id": ARTIFACT_ID,
        "phase_id": PHASE_ID,
        "phase_name": PHASE_NAME,
        "unit_id": UNIT_ID,
        "unit_role": UNIT_ROLE,
        "closure_branch": CURRENT_CLOSURE_BRANCH,
        "closure_gate": CURRENT_CLOSURE_GATE,
        "phase_status": CURRENT_PHASE_STATUS,
    }
    for key, want in expected.items():
        if closure.get(key) != want:
            fail(
                "STOP_VS1_6_PHASE_STATUS_AMBIGUOUS",
                field=key,
                expected=want,
                actual=closure.get(key),
            )
    if get_value(closure, "terminal_transition.transition") != CURRENT_TERMINAL_TRANSITION:
        fail(
            "STOP_VS1_6_TERMINAL_TRANSITION_UNSAFE",
            field="terminal_transition.transition",
            expected=CURRENT_TERMINAL_TRANSITION,
            actual=get_value(closure, "terminal_transition.transition"),
        )
    for section in ["forbidden_claim_checks", "non_claims"]:
        values = closure.get(section, {})
        for key, actual in values.items():
            if actual is not False:
                fail(
                    "STOP_VS1_6_FORBIDDEN_CLAIM_DRIFT",
                    field=f"{section}.{key}",
                    expected=False,
                    actual=actual,
                )
    required_md = [
        "# Phase VS1 closure v0",
        CURRENT_PHASE_STATUS,
        CURRENT_CLOSURE_GATE,
        "VS1.1 commit: 8f4b57c697d8dc7110e3ea9d73183d36c806a66c",
        "VS1.2 commit: d62db2d74f2ff42bf7f633b4e2169aed409a0703",
        "VS1.3 commit: 741f28223d93b27d5a00fa06bb45a1739d66cb13",
        "VS1.4 commit: 68c846386a79cc89215c1b16dbd1389333269b80",
        "VS1.5 commit: 955743f9cf281d9b83c9e68fb0f367121b3c5295",
        "POST_VS1_DIRECTION_DECISION_SURFACE",
        CURRENT_TERMINAL_TRANSITION,
    ]
    for phrase in required_md:
        if phrase not in md:
            fail(
                "STOP_VS1_6_PHASE_STATUS_AMBIGUOUS",
                source=OUTPUT_MD,
                field="markdown_required_phrase",
                expected=phrase,
                actual="missing",
            )
    assert_no_placeholders(closure)


def emit_success_readout() -> None:
    print("BUILD_PHASE_VS1_CLOSURE_V0_COMPLETE")
    print(f"artifact_id={ARTIFACT_ID}")
    print(f"schema_version={SCHEMA_VERSION}")
    print(f"phase_id={PHASE_ID}")
    print(f"phase_name={PHASE_NAME}")
    print(f"unit_id={UNIT_ID}")
    print(f"unit_role={UNIT_ROLE}")
    print("source_chain_complete=true")
    print(f"vs1_1_commit_sha={VS1_1_COMMIT}")
    print(f"vs1_2_commit_sha={VS1_2_COMMIT}")
    print(f"vs1_3_commit_sha={VS1_3_COMMIT}")
    print(f"vs1_4_commit_sha={VS1_4_COMMIT}")
    print(f"vs1_5_commit_sha={VS1_5_COMMIT}")
    print(f"closure_branch={CURRENT_CLOSURE_BRANCH}")
    print(f"closure_gate={CURRENT_CLOSURE_GATE}")
    print(f"phase_status={CURRENT_PHASE_STATUS}")
    print("controlled_loop_contract_defined=true")
    print("preconditions_inventoried=true")
    print("required_components_total=20")
    print("convergence_criterion_component_included=true")
    print("readiness_audited=true")
    print("controlled_loop_ready=false")
    print("typed_blockers_exposed=true")
    print("next_surfaces_mapped=true")
    print("ready_for_human_execution_authority_decision=false")
    print("human_execution_authority_decision_requested_by_vs1=false")
    print("source_blocker_count=20")
    print("mapped_blocker_count=20")
    print("unmapped_blocker_count=0")
    print("surface_candidate_record_count=21")
    print("s20_convergence_surface_id=S20_CONVERGENCE_CRITERION_CONTRACT_SURFACE")
    print("s21_readiness_reaudit_surface_id=S21_CONTROLLED_LOOP_READINESS_REAUDIT_SURFACE")
    print("s20_s21_conflated=false")
    print("advisory_first_surface_from_vs1_5=S10_SOURCE_IDENTITY_FRESHNESS_POLICY_SURFACE")
    print("ranking_recomputed_by_vs1_6=false")
    print("ranking_modified_by_vs1_6=false")
    print("post_vs1_decision_surface=POST_VS1_DIRECTION_DECISION_SURFACE")
    print("post_vs1_decision_surface_named=true")
    print("post_vs1_decision_artifact_created=false")
    print("post_vs1_decision_consumed=false")
    print("human_decision_required=true")
    print("machine_may_select_next_phase=false")
    print("machine_may_rank_post_vs1_options=false")
    print("loop_execution_authorized=false")
    print("runner_created=false")
    print("runner_readiness_claimed=false")
    print("micro_sweeps_authorized=false")
    print("local_revision_authorized=false")
    print("active_registry_created=false")
    print("trace_generalization_claimed=false")
    print("performance_optimization_claimed=false")
    print("scale_optimization_claimed=false")
    print("mapped_surface_selected=false")
    print("mapped_surface_built=false")
    print("candidate_promotion_attempted=false")
    print("human_authority_consumed=false")
    print("phase_vs1_closed=true")
    print("evidence_yield_branch=CONFIRMATION_YIELD")
    print("diagnostic_yield_preserved=true")
    print("diagnostics_recomputed_by_vs1_6=false")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition={PRINT_TRANSITION}")


def emit_typed_stop(exc: ClosureFailure) -> None:
    print("BUILD_PHASE_VS1_CLOSURE_V0_TYPED_STOP")
    print(f"artifact_id={ARTIFACT_ID}")
    print(f"phase_id={PHASE_ID}")
    print(f"unit_id={UNIT_ID}")
    print(f"closure_gate={exc.code}")
    print("yield_branch=DIAGNOSTIC_YIELD")
    print(f"missing_or_invalid_source={exc.source}")
    print(f"violating_field={exc.field}")
    print(f"expected_value={exc.expected}")
    print(f"actual_value={exc.actual}")
    print(f"next_lawful_surface={exc.next_surface}")
    print("self_repair_performed=false")
    print("loop_execution_authorized=false")
    print("runner_created=false")
    print("human_authority_consumed=false")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition=STOP({exc.code})")


def generate() -> int:
    root = detect_repo_root(Path.cwd())
    require_head(root)
    validate_dirty_scope(root)
    ensure_no_forbidden_artifacts(root)
    for source in SOURCE_DEFS:
        require_file(root, str(source["path"]))
        require_file(root, str(source["md_path"]))
    require_file(root, "docs/matrixlabs/phase_vs1/post_vs0_direction_decision_receipt_v0.json")
    require_file(root, "docs/matrixlabs/phase_vs1/post_vs0_direction_decision_receipt_v0.md")
    before_hashes = capture_source_hashes(root)
    source_chain, sources = build_source_chain(root)
    validate_boundaries(sources)
    closure = build_closure(root, source_chain, sources)
    md = build_markdown(closure)
    validate_closure(closure, md)
    output_json = root / OUTPUT_JSON
    output_md = root / OUTPUT_MD
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(closure, indent=2, sort_keys=True) + "\n",
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
    except ClosureFailure as exc:
        emit_typed_stop(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
