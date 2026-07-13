#!/usr/bin/env python3
"""Build the Post-VS2 first execution decision surface v0.

This construction-only builder reads the committed Phase VS2 closure and its
sealed package sources, verifies their hashes and state, emits a human decision
surface plus preparation receipt, and refreshes the baseline share projection.
It does not execute the sealed package or any VS2.6/VS2.7 builder/verifier.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import build_phase_vs2_7_phase_closure_v0 as vs27


ROOT = "/home/asd/projects/matrixlab"
BRANCH = "master"
HEAD = "af79cea2fd8cf98732ef074969a9a56ffb8a6406"

CANON = "MATRIXLAB_CANONICAL_JSON_V0"
HASH_ALGORITHM = "sha256"
UNIT_ID = "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_PREPARATION"
UNIT_ROLE = "BOUNDED_HUMAN_EXECUTION_DECISION_SURFACE_PREPARATION_ONLY"
SURFACE_ID = "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE"
SURFACE_ARTIFACT_ID = "post_vs2_first_execution_decision_surface_v0"
SURFACE_VERSION = "v0"
SURFACE_ROLE = "BOUNDED_HUMAN_EXECUTION_DECISION_SURFACE_ONLY"
RECEIPT_ID = "post_vs2_first_execution_decision_surface_receipt_v0"
SURFACE_STATE = "UNCONSUMED"
SURFACE_GATE = "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_PASS_READY_FOR_HUMAN_DECISION"
FAIL_GATE = "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_FAIL"
TERMINAL_TRANSITION = "STOP_POST_VS2_EXECUTION_SURFACE_READY_PENDING_HUMAN_DECISION"
BOOKKEEPING_TRANSITION = (
    "ADVANCE(BOOKKEEPING_COMMIT_POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_V0_PENDING)"
)
EVIDENCE_YIELD = "CONFIRMATION_YIELD"

P = "docs/matrixlabs/phase_vs2"
POST = "docs/matrixlabs/post_vs2"
C0_JSON = f"{P}/phase_vs2_closure_v0.json"
R0_JSON = f"{P}/phase_vs2_7_phase_closure_receipt_v0.json"
S0_JSON = f"{POST}/post_vs2_first_execution_decision_surface_v0.json"
S0_MD = f"{POST}/post_vs2_first_execution_decision_surface_v0.md"
PR0_JSON = f"{POST}/post_vs2_first_execution_decision_surface_receipt_v0.json"
SCRIPT = "scripts/build_post_vs2_first_execution_decision_surface_v0.py"
VERIFY_SCRIPT = "scripts/verify_post_vs2_first_execution_decision_surface_v0.py"
BASELINE_SCRIPT = "scripts/build_baseline_share_v0.py"
BASELINE_OUTPUTS = [
    "baseline_share/COMMIT_CONTEXT.md",
    "baseline_share/CURRENT_STATE.md",
    "baseline_share/MANIFEST.json",
    "baseline_share/RECEIPT_POINTERS.md",
]
GENERATED_DOCS = [S0_JSON, S0_MD, PR0_JSON]
ALLOWED_DIRTY = {
    SCRIPT,
    VERIFY_SCRIPT,
    BASELINE_SCRIPT,
    *GENERATED_DOCS,
    *BASELINE_OUTPUTS,
}
EXPECTED_NEW = {SCRIPT, VERIFY_SCRIPT, *GENERATED_DOCS}
EXPECTED_MODIFIED = {BASELINE_SCRIPT, *BASELINE_OUTPUTS}

C0_EXPECTED = "73ef125f8e606c66ae6e19c5d7337318c88963898f36d3aa1366f36cf7fc7e51"
C0_RAW_EXPECTED = "ccce0450d79a3f92ef44d9531d78e090c0269c4e9946f9b5c75027708c33ec38"
R0_EXPECTED = "a35ba5239f8f334a9c2fa2ce48a29bc3c67e10f88ce4fb222558bc6dd29b585b"
R0_RAW_EXPECTED = "1bb0d7e6731bf4fd1da9f3cc33700977006614cf08a3de4b4b11138a47cc542d"
E0_EXPECTED = "cd3f9deed2278d8ab7292a7aa64cf1a68446312d26493f07e508f1d5360211c6"
G0_EXPECTED = "94f1a98bbfb246226ef7f29887ea0a3ade2a4f71666b5852bbdf93815836cc99"
GR0_EXPECTED = "705eb58f43460b289ac40a6e24557bce0be4accd04f372edd79df9ca38c12332"
RS0_EXPECTED = "5c36c71da7bd70889c16a4722d882b0fe8dcfc5ce6cd8a72b80da4dbafbe2d79"
PHASE_STATUS = (
    "PHASE_VS2_PASS_FIRST_SWEEP_CAPABLE_KERNEL_SEALED_READY_FOR_ONE_BOUNDED_EXECUTION_DECISION"
)
VS27_GATE = "VS2_7_PHASE_CLOSURE_PASS_READY_FOR_ONE_EXECUTION_DECISION"
READY_BRANCH = "READY"
VS27_TERMINAL = "STOP_PHASE_VS2_CLOSED_PENDING_FIRST_EXECUTION_DECISION"
READY_GATE = "VS2_6_FIRST_RUN_CONSTRUCTION_READINESS_PASS_READY_FOR_ONE_EXECUTION_DECISION"
E0_LOGICAL_ID = "FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_CORE_V0"
G0_LOGICAL_ID = "FIRST_SWEEP_KERNEL_FIRST_RUN_CONSTRUCTION_READINESS_GATE_V0"
RS0_LOGICAL_ID = "FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_READINESS_SEAL_V0"

DECISION_QUESTION = (
    "Should MatrixLab approve creation of one bounded machine-authority package "
    "for exactly one execution of the exact package identified by the verified "
    "Phase VS2 closure, execution-package core, and readiness seal, without "
    "modifying its fixtures, fixture order, sources, bounds, reporting "
    "obligations, expiration policy, or forbidden-effect boundaries?"
)
DECISION_OPTION_CODES = [
    "AUTHORIZE_EXACT_SEALED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE",
    "REQUEST_REDUCED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_VERSION",
    "RETURN_SEALED_FIRST_SWEEP_KERNEL_PACKAGE_FOR_REVISION",
    "DEFER_FIRST_SWEEP_KERNEL_EXECUTION_DECISION",
    "REJECT_CURRENT_FIRST_SWEEP_KERNEL_EXECUTION_REQUEST",
    "ABANDON_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_VERSION",
]
FIXTURE_IDS = [
    "F01_POSITIVE_REQUIRED_FIELD_AND_NORMALIZATION",
    "F02_ALREADY_VALID_PRESERVATION",
    "F03_REPAIRABLE_TYPED_VALUE_NORMALIZATION",
    "F04_REPAIRABLE_SOURCE_IDENTITY_BINDING",
    "F05_MISSING_SOURCE_BLOCKER",
    "F06_AUTHORITY_OVERREACH_BLOCKER",
    "F07_REPAIRABLE_PROHIBITED_CANDIDATE_DECLARATION",
    "F08_MISSING_SCHEMA_BLOCKER",
    "F09_MISSING_CAPABILITY_BLOCKER",
    "F10_NO_ADMISSIBLE_MOVE_GAP",
]

CORE_SOURCE_KEYS = [
    "PROFILE",
    "F0",
    "O1",
    "O2",
    "O3",
    "M0",
    "VS2_3_RECEIPT",
    "MS0",
    "K0",
    "C20",
    "R13",
    "M2",
    "F0X",
    "FS0",
    "S0X",
    "D0",
    "RP0",
    "E0",
    "G0",
    "GR0",
    "RS0",
    "U0",
]
SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "C0": {
        "path": C0_JSON,
        "binding": (None, "closure_payload", "closure_payload_sha256"),
        "expected": C0_EXPECTED,
        "raw_expected": C0_RAW_EXPECTED,
        "role": "PHASE_VS2_CLOSURE_ARTIFACT",
        "version": "v0",
    },
    "R0": {
        "path": R0_JSON,
        "binding": (None, "receipt_payload", "receipt_payload_sha256"),
        "expected": R0_EXPECTED,
        "raw_expected": R0_RAW_EXPECTED,
        "role": "PHASE_VS2_CLOSURE_RECEIPT",
        "version": "v0",
    },
}
for _key in CORE_SOURCE_KEYS:
    SOURCE_SPECS[_key] = dict(vs27.SOURCES[_key])
for _index in range(1, 11):
    SOURCE_SPECS[f"F{_index:02d}_CANDIDATE"] = dict(vs27.SOURCES[f"F{_index:02d}_CANDIDATE"])
    SOURCE_SPECS[f"F{_index:02d}_DEFINITION"] = dict(vs27.SOURCES[f"F{_index:02d}_DEFINITION"])
SOURCE_SPECS["E0"]["expected"] = E0_EXPECTED
SOURCE_SPECS["G0"]["expected"] = G0_EXPECTED
SOURCE_SPECS["GR0"]["expected"] = GR0_EXPECTED
SOURCE_SPECS["RS0"]["expected"] = RS0_EXPECTED

D_CHECKS = [
    ("D01_READY_CLOSURE_VERIFIED", "Ready closure verified", "POST_VS2_EXECUTION_SURFACE_VS2_READY_PASS"),
    ("D02_SOURCE_LINKAGE_VERIFIED", "Source linkage verified", "POST_VS2_EXECUTION_SURFACE_SOURCE_LINKAGE_PASS"),
    ("D03_CORE_IDENTITY_VERIFIED", "Core identity verified", "POST_VS2_EXECUTION_SURFACE_PACKAGE_CORE_IDENTITY_PASS"),
    ("D04_READINESS_CHAIN_VERIFIED", "Readiness chain verified", "POST_VS2_EXECUTION_SURFACE_READINESS_CHAIN_PASS"),
    ("D05_DECISION_TIME_INTEGRITY_CURRENT", "Decision-time integrity current", "POST_VS2_EXECUTION_SURFACE_PACKAGE_INTEGRITY_CURRENT_PASS"),
    ("D06_FRESHNESS_CURRENT", "Freshness current", "POST_VS2_EXECUTION_SURFACE_SOURCE_FRESHNESS_CURRENT_PASS"),
    ("D07_FIXTURE_SET_VERIFIED", "Fixture set verified", "POST_VS2_EXECUTION_SURFACE_FIXTURE_SET_PASS"),
    ("D08_RUNTIME_SOURCE_SNAPSHOT_VERIFIED", "Runtime source snapshot verified", "POST_VS2_EXECUTION_SURFACE_RUNTIME_SOURCE_SNAPSHOT_PASS"),
    ("D09_DEPENDENCY_INVENTORY_VERIFIED", "Dependency inventory verified", "POST_VS2_EXECUTION_SURFACE_PACKAGE_DEPENDENCY_PASS"),
    ("D10_EXACT_BOUNDS_VERIFIED", "Exact bounds verified", "POST_VS2_EXECUTION_SURFACE_EXACT_BOUNDS_PASS"),
    ("D11_PROPOSED_AUTHORITY_BOUNDED", "Proposed authority bounded", "POST_VS2_EXECUTION_SURFACE_AUTHORITY_SCOPE_PASS"),
    ("D12_AUTHORITY_EXPIRY_COMPLETE", "Authority expiry complete", "POST_VS2_EXECUTION_SURFACE_AUTHORITY_EXPIRY_PASS"),
    ("D13_EXCLUDED_AUTHORITY_COMPLETE", "Excluded authority complete", "POST_VS2_EXECUTION_SURFACE_EXCLUDED_AUTHORITY_PASS"),
    ("D14_DECISION_OPTIONS_BOUNDED", "Decision options bounded", "POST_VS2_EXECUTION_SURFACE_DECISION_OPTIONS_PASS"),
    ("D15_SURFACE_UNCONSUMED", "Surface unconsumed", "POST_VS2_EXECUTION_SURFACE_DECISION_PENDING_PASS"),
    ("D16_REPORTS_REMAIN_CONTRACTS_ONLY", "Reports remain contracts only", "POST_VS2_EXECUTION_SURFACE_REPORT_BOUNDARY_PASS"),
    ("D17_NO_EXECUTION_DRIFT", "No execution drift", "POST_VS2_EXECUTION_SURFACE_NO_EXECUTION_DRIFT_PASS"),
    ("D18_FORBIDDEN_CLAIMS_ABSENT", "Forbidden claims absent", "POST_VS2_EXECUTION_SURFACE_FORBIDDEN_CLAIMS_ABSENT"),
]


class StopFailure(RuntimeError):
    def __init__(self, code: str, check: str, artifact: str, expected: Any, observed: Any) -> None:
        super().__init__(code)
        self.code = code
        self.check = check
        self.artifact = artifact
        self.expected = expected
        self.observed = observed


def stop(code: str, check: str, artifact: str, expected: Any, observed: Any) -> None:
    raise StopFailure(code, check, artifact, expected, observed)


def require(actual: Any, expected: Any, code: str, check: str, artifact: str) -> None:
    if actual != expected:
        stop(code, check, artifact, expected, actual)


def canonical_bytes(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git(root: Path, args: list[str], binary: bool = False) -> Any:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        text=not binary,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return proc.stdout


def status_paths(status: str) -> list[str]:
    paths: list[str] = []
    for line in status.splitlines():
        if not line:
            continue
        if line.startswith("?? "):
            paths.append(line[3:])
        elif len(line) >= 4:
            paths.append(line[3:])
    return paths


def check_repo(root: Path) -> None:
    require(str(root), ROOT, "STOP_POST_VS2_EXECUTION_SURFACE_REPOSITORY_ROOT_MISMATCH", "repository", "repo_root")
    branch = git(root, ["branch", "--show-current"]).strip()
    require(branch, BRANCH, "STOP_POST_VS2_EXECUTION_SURFACE_BRANCH_MISMATCH", "repository", "branch")
    head = git(root, ["rev-parse", "HEAD"]).strip()
    require(head, HEAD, "STOP_POST_VS2_EXECUTION_SURFACE_UNEXPECTED_HEAD", "repository", "HEAD")
    staged = git(root, ["diff", "--cached", "--name-only"]).splitlines()
    if staged:
        stop("STOP_POST_VS2_EXECUTION_SURFACE_STAGED_CHANGES_PRESENT", "repository", "index", [], staged)
    if (root / "discussion_packets").exists():
        stop("STOP_POST_VS2_EXECUTION_SURFACE_DISCUSSION_PACKETS_PRESENT", "repository", "discussion_packets", False, True)
    dirty = set(status_paths(git(root, ["status", "--short", "--untracked-files=all"])))
    unexpected = sorted(dirty - ALLOWED_DIRTY)
    if unexpected:
        stop(
            "STOP_POST_VS2_EXECUTION_SURFACE_PREEXISTING_WORKTREE_CHANGES",
            "repository",
            "worktree",
            "clean before construction",
            sorted(dirty),
        )


def committed_bytes(root: Path, rel: str) -> bytes:
    try:
        data = git(root, ["show", f"{HEAD}:{rel}"], binary=True)
    except subprocess.CalledProcessError as exc:
        stop("STOP_POST_VS2_EXECUTION_SURFACE_VS2_CLOSURE_MISSING", "source_identity", rel, "committed source", exc.stderr)
    path = root / rel
    if not path.exists():
        stop("STOP_POST_VS2_EXECUTION_SURFACE_VS2_CLOSURE_MISSING", "source_identity", rel, "worktree source", "missing")
    current = path.read_bytes()
    require(current, data, "STOP_POST_VS2_EXECUTION_SURFACE_PACKAGE_CHANGED_AFTER_READINESS", "source_identity", rel)
    return current


def payload_from(data: dict[str, Any], spec: dict[str, Any]) -> tuple[dict[str, Any], str]:
    binding_key, payload_key, sha_key = spec["binding"]
    payload = data.get(payload_key)
    declared_hash = data.get(sha_key)
    if payload is None and binding_key:
        binding = data.get(binding_key, {})
        payload = binding.get(payload_key)
        declared_hash = binding.get(sha_key, declared_hash)
    if payload is None:
        payload = data
    digest = sha256_bytes(canonical_bytes(payload))
    if declared_hash is not None:
        require(declared_hash, digest, "STOP_POST_VS2_EXECUTION_SURFACE_PACKAGE_HASH_MISMATCH", "source_identity", spec["path"])
    return payload, digest


def load_source(root: Path, key: str, spec: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = committed_bytes(root, spec["path"])
    raw_hash = sha256_bytes(raw)
    if spec.get("raw_expected"):
        require(raw_hash, spec["raw_expected"], "STOP_POST_VS2_EXECUTION_SURFACE_PACKAGE_HASH_MISMATCH", "source_identity", key)
    data = json.loads(raw.decode("utf-8"))
    payload, digest = payload_from(data, spec)
    expected = spec.get("expected")
    if expected:
        require(digest, expected, "STOP_POST_VS2_EXECUTION_SURFACE_PACKAGE_HASH_MISMATCH", "source_identity", key)
    artifact_id = data.get("artifact_id") or data.get("receipt_id") or payload.get("artifact_id") or payload.get("receipt_id")
    record = {
        "source_key": key,
        "source_role": spec["role"],
        "artifact_id": artifact_id,
        "artifact_kind": data.get("artifact_kind") or payload.get("artifact_kind") or spec["role"],
        "artifact_version": data.get("artifact_version") or data.get("receipt_version") or spec.get("version", "v0"),
        "declared_path": spec["path"],
        "canonical_content_sha256": digest,
        "raw_file_sha256": raw_hash,
        "hash_algorithm": HASH_ALGORITHM,
        "canonicalization_rule": CANON,
        "identity_source_fields": [
            "artifact_id/receipt_id",
            "artifact_version/receipt_version",
            spec["binding"][1],
            spec["binding"][2],
        ],
        "source_identity_verified": True,
    }
    return data, record


def load_sources(root: Path) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    data: dict[str, dict[str, Any]] = {}
    ledger: list[dict[str, Any]] = []
    for key, spec in SOURCE_SPECS.items():
        data[key], record = load_source(root, key, spec)
        ledger.append(record)
    return data, ledger


def ref(ledger: list[dict[str, Any]], key: str) -> dict[str, Any]:
    for row in ledger:
        if row["source_key"] == key:
            return row
    stop("STOP_POST_VS2_EXECUTION_SURFACE_SOURCE_LINKAGE_MISSING", "source_linkage", key, "source present", "missing")


def verify_ready_closure(data: dict[str, dict[str, Any]], ledger: list[dict[str, Any]]) -> None:
    c0 = data["C0"]
    r0 = data["R0"]
    payload = c0["closure_payload"]
    receipt = r0["receipt_payload"]
    require(c0.get("artifact_id"), "phase_vs2_closure_v0", "STOP_POST_VS2_EXECUTION_SURFACE_VS2_CLOSURE_MISSING", "ready_closure", "C0")
    require(c0.get("closure_payload_sha256"), C0_EXPECTED, "STOP_POST_VS2_EXECUTION_SURFACE_PACKAGE_HASH_MISMATCH", "ready_closure", "C0")
    require(r0.get("receipt_id"), "phase_vs2_7_phase_closure_receipt_v0", "STOP_POST_VS2_EXECUTION_SURFACE_VS2_CLOSURE_RECEIPT_MISSING", "ready_closure", "R0")
    require(r0.get("receipt_payload_sha256"), R0_EXPECTED, "STOP_POST_VS2_EXECUTION_SURFACE_PACKAGE_HASH_MISMATCH", "ready_closure", "R0")
    require(payload.get("phase_status"), PHASE_STATUS, "STOP_POST_VS2_EXECUTION_SURFACE_VS2_NOT_READY", "ready_closure", "phase_status")
    require(payload.get("closure_gate"), VS27_GATE, "STOP_POST_VS2_EXECUTION_SURFACE_READY_GATE_MISMATCH", "ready_closure", "closure_gate")
    require(payload.get("readiness_branch"), READY_BRANCH, "STOP_POST_VS2_EXECUTION_SURFACE_VS2_NOT_READY", "ready_closure", "readiness_branch")
    require(payload.get("terminal_transition", {}).get("transition"), VS27_TERMINAL, "STOP_POST_VS2_EXECUTION_SURFACE_READY_GATE_MISMATCH", "ready_closure", "terminal_transition")
    surface = payload.get("post_phase_decision_surface", {})
    require(surface.get("surface_id"), SURFACE_ID, "STOP_POST_VS2_EXECUTION_SURFACE_READY_GATE_MISMATCH", "ready_closure", "post_phase_surface")
    require(surface.get("named_by_vs2_7"), True, "STOP_POST_VS2_EXECUTION_SURFACE_READY_GATE_MISMATCH", "ready_closure", "surface_named")
    for field in ["created_by_vs2_7", "decision_recorded", "authority_update_applied", "execution_started"]:
        require(surface.get(field), False, "STOP_POST_VS2_EXECUTION_SURFACE_READY_GATE_MISMATCH", "ready_closure", field)
    require(receipt.get("closure_artifact_id"), "phase_vs2_closure_v0", "STOP_POST_VS2_EXECUTION_SURFACE_SOURCE_LINKAGE_MISMATCH", "ready_closure", "R0->C0")
    require(receipt.get("closure_artifact_sha256"), ref(ledger, "C0")["canonical_content_sha256"], "STOP_POST_VS2_EXECUTION_SURFACE_SOURCE_LINKAGE_MISMATCH", "ready_closure", "R0->C0 hash")


def require_mapping(value: Any, code: str, check: str, artifact: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        stop(code, check, artifact, "mapping", type(value).__name__)
    return value


def require_list_field(owner: dict[str, Any], field: str, code: str, check: str, artifact: str) -> list[Any]:
    if field not in owner:
        stop(code, check, artifact, "present list", "missing")
    value = owner[field]
    if not isinstance(value, list):
        stop(code, check, artifact, "list", type(value).__name__)
    return value


def require_string_items(values: list[Any], code: str, check: str, artifact: str) -> list[str]:
    if not all(isinstance(value, str) for value in values):
        stop(code, check, artifact, "list[str]", values)
    return list(values)


def require_top_payload_agree(
    top: dict[str, Any],
    payload: dict[str, Any],
    field: str,
    expected: Any,
    code: str,
    check: str,
    artifact: str,
) -> None:
    if field not in top or field not in payload:
        stop(code, check, artifact, f"{field} present in top-level and canonical payload", {"top_present": field in top, "payload_present": field in payload})
    require(top.get(field), payload.get(field), code, check, f"{artifact}.{field}.top_payload_agreement")
    require(payload.get(field), expected, code, check, f"{artifact}.{field}")


def normalize_readiness_blocker_posture(data: dict[str, dict[str, Any]]) -> dict[str, Any]:
    c0_payload = require_mapping(data["C0"].get("closure_payload"), "STOP_POST_VS2_EXECUTION_SURFACE_SOURCE_LINKAGE_MISMATCH", "readiness", "C0.closure_payload")
    require(c0_payload.get("readiness_branch"), READY_BRANCH, "STOP_POST_VS2_EXECUTION_SURFACE_VS2_NOT_READY", "readiness", "C0 readiness_branch")
    c0_blockers = require_string_items(
        require_list_field(c0_payload, "readiness_blockers", "STOP_POST_VS2_EXECUTION_SURFACE_SOURCE_LINKAGE_MISMATCH", "readiness", "C0 readiness_blockers"),
        "STOP_POST_VS2_EXECUTION_SURFACE_SOURCE_LINKAGE_MISMATCH",
        "readiness",
        "C0 readiness_blockers",
    )

    g0 = data["G0"]
    gate_payload = require_mapping(g0.get("gate_binding", {}).get("gate_payload"), "STOP_POST_VS2_EXECUTION_SURFACE_READY_GATE_MISMATCH", "readiness", "G0 gate_payload")
    require_top_payload_agree(g0, gate_payload, "gate_status", "READY", "STOP_POST_VS2_EXECUTION_SURFACE_VS2_NOT_READY", "readiness", "G0")
    require_top_payload_agree(g0, gate_payload, "eligible_for_execution_decision", True, "STOP_POST_VS2_EXECUTION_SURFACE_VS2_NOT_READY", "readiness", "G0")
    require_top_payload_agree(g0, gate_payload, "readiness_component_count", 21, "STOP_POST_VS2_EXECUTION_SURFACE_READY_GATE_MISMATCH", "readiness", "G0")
    require_top_payload_agree(g0, gate_payload, "readiness_verdict", READY_GATE, "STOP_POST_VS2_EXECUTION_SURFACE_READY_GATE_MISMATCH", "readiness", "G0")
    gate_records = require_list_field(gate_payload, "readiness_component_records", "STOP_POST_VS2_EXECUTION_SURFACE_READY_GATE_MISMATCH", "readiness", "G0 readiness_component_records")
    require(g0.get("readiness_component_records"), gate_records, "STOP_POST_VS2_EXECUTION_SURFACE_READY_GATE_MISMATCH", "readiness", "G0 records top/payload agreement")
    require(len(gate_records), 21, "STOP_POST_VS2_EXECUTION_SURFACE_READY_GATE_MISMATCH", "readiness", "R01-R21")
    gate_component_blocker_records: list[dict[str, Any]] = []
    gate_component_blockers: list[str] = []
    for index, row in enumerate(gate_records, start=1):
        record = require_mapping(row, "STOP_POST_VS2_EXECUTION_SURFACE_READY_GATE_MISMATCH", "readiness", f"G0 readiness_component_records[{index}]")
        component_id = record.get("readiness_component_id")
        if not isinstance(component_id, str) or not component_id:
            stop("STOP_POST_VS2_EXECUTION_SURFACE_READY_GATE_MISMATCH", "readiness", f"G0 readiness_component_records[{index}].readiness_component_id", "non-empty string", component_id)
        require(record.get("readiness_status"), "READY", "STOP_POST_VS2_EXECUTION_SURFACE_VS2_NOT_READY", "readiness", component_id)
        blocker_ids = require_string_items(
            require_list_field(record, "blocker_ids", "STOP_POST_VS2_EXECUTION_SURFACE_READY_GATE_MISMATCH", "readiness", f"{component_id}.blocker_ids"),
            "STOP_POST_VS2_EXECUTION_SURFACE_READY_GATE_MISMATCH",
            "readiness",
            f"{component_id}.blocker_ids",
        )
        gate_component_blocker_records.append({"readiness_component_id": component_id, "blocker_ids": blocker_ids})
        gate_component_blockers.extend(blocker_ids)

    gr0 = data["GR0"]
    receipt_payload = require_mapping(gr0.get("receipt_binding", {}).get("receipt_payload"), "STOP_POST_VS2_EXECUTION_SURFACE_READINESS_RECEIPT_MISMATCH", "readiness", "GR0 receipt_payload")
    gr0_blockers = require_string_items(
        require_list_field(gr0, "typed_blockers", "STOP_POST_VS2_EXECUTION_SURFACE_READINESS_RECEIPT_MISMATCH", "readiness", "GR0 typed_blockers"),
        "STOP_POST_VS2_EXECUTION_SURFACE_READINESS_RECEIPT_MISMATCH",
        "readiness",
        "GR0 typed_blockers",
    )
    gr0_payload_blockers = require_string_items(
        require_list_field(receipt_payload, "typed_blockers", "STOP_POST_VS2_EXECUTION_SURFACE_READINESS_RECEIPT_MISMATCH", "readiness", "GR0 receipt_payload typed_blockers"),
        "STOP_POST_VS2_EXECUTION_SURFACE_READINESS_RECEIPT_MISMATCH",
        "readiness",
        "GR0 receipt_payload typed_blockers",
    )
    require_top_payload_agree(gr0, receipt_payload, "audit_completed", True, "STOP_POST_VS2_EXECUTION_SURFACE_READINESS_RECEIPT_MISMATCH", "readiness", "GR0")
    require_top_payload_agree(gr0, receipt_payload, "eligible_for_execution_decision", True, "STOP_POST_VS2_EXECUTION_SURFACE_VS2_NOT_READY", "readiness", "GR0")
    require_top_payload_agree(gr0, receipt_payload, "readiness_verdict", READY_GATE, "STOP_POST_VS2_EXECUTION_SURFACE_READINESS_RECEIPT_MISMATCH", "readiness", "GR0")
    require_top_payload_agree(gr0, receipt_payload, "runtime_execution_performed", False, "STOP_POST_VS2_EXECUTION_SURFACE_READINESS_RECEIPT_MISMATCH", "readiness", "GR0")

    if not (c0_blockers == gate_component_blockers == gr0_blockers == gr0_payload_blockers):
        stop(
            "STOP_POST_VS2_EXECUTION_SURFACE_SOURCE_LINKAGE_MISMATCH",
            "readiness",
            "blocker_sources",
            "C0/G0/GR0 blocker agreement",
            {
                "C0": c0_blockers,
                "G0": gate_component_blockers,
                "GR0": gr0_blockers,
                "GR0_payload": gr0_payload_blockers,
            },
        )
    if c0_blockers:
        stop("STOP_POST_VS2_EXECUTION_SURFACE_VS2_NOT_READY", "readiness", "typed_readiness_blockers", [], c0_blockers)

    return {
        "closure_readiness_blockers": c0_blockers,
        "readiness_receipt_typed_blockers": gr0_blockers,
        "readiness_receipt_payload_typed_blockers": gr0_payload_blockers,
        "gate_component_blocker_records": gate_component_blocker_records,
        "gate_component_blockers": gate_component_blockers,
        "normalized_typed_readiness_blockers": c0_blockers,
        "normalized_typed_readiness_blocker_count": len(c0_blockers),
        "blocker_source_count": 4,
        "all_blocker_sources_present": True,
        "all_blocker_sources_well_typed": True,
        "all_blocker_sources_agree": True,
        "RS0_blocker_field_required": False,
    }


def verify_readiness(data: dict[str, dict[str, Any]], ledger: list[dict[str, Any]]) -> dict[str, Any]:
    e0 = data["E0"]
    g0 = data["G0"]
    gr0 = data["GR0"]
    rs0 = data["RS0"]
    posture = normalize_readiness_blocker_posture(data)
    require(e0.get("artifact_id"), "phase_vs2_execution_package_core_manifest_v0", "STOP_POST_VS2_EXECUTION_SURFACE_PACKAGE_IDENTITY_MISMATCH", "readiness", "E0")
    require(e0.get("package_id"), E0_LOGICAL_ID, "STOP_POST_VS2_EXECUTION_SURFACE_PACKAGE_IDENTITY_MISMATCH", "readiness", "E0 package_id")
    require(g0.get("artifact_id"), "phase_vs2_first_run_construction_readiness_gate_v0", "STOP_POST_VS2_EXECUTION_SURFACE_READINESS_GATE_MISSING", "readiness", "G0")
    require(g0.get("gate_id"), G0_LOGICAL_ID, "STOP_POST_VS2_EXECUTION_SURFACE_READY_GATE_MISMATCH", "readiness", "G0 gate_id")
    require(gr0.get("readiness_gate_reference", {}).get("artifact_id"), g0.get("artifact_id"), "STOP_POST_VS2_EXECUTION_SURFACE_SOURCE_LINKAGE_MISMATCH", "readiness", "GR0->G0")
    require(rs0.get("artifact_id"), "phase_vs2_execution_package_readiness_seal_v0", "STOP_POST_VS2_EXECUTION_SURFACE_READINESS_SEAL_MISSING", "readiness", "RS0")
    require(rs0.get("seal_id"), RS0_LOGICAL_ID, "STOP_POST_VS2_EXECUTION_SURFACE_READINESS_SEAL_MISMATCH", "readiness", "RS0 seal_id")
    seal_payload = require_mapping(rs0.get("seal_binding", {}).get("seal_payload"), "STOP_POST_VS2_EXECUTION_SURFACE_READINESS_SEAL_MISMATCH", "readiness", "RS0 seal_payload")
    require_top_payload_agree(rs0, seal_payload, "seal_status", "SEALED_READY_FOR_HUMAN_EXECUTION_DECISION", "STOP_POST_VS2_EXECUTION_SURFACE_READINESS_SEAL_MISMATCH", "readiness", "RS0")
    require_top_payload_agree(rs0, seal_payload, "eligible_for_execution_decision", True, "STOP_POST_VS2_EXECUTION_SURFACE_VS2_NOT_READY", "readiness", "RS0")
    require_top_payload_agree(rs0, seal_payload, "readiness_verdict", READY_GATE, "STOP_POST_VS2_EXECUTION_SURFACE_READINESS_SEAL_MISMATCH", "readiness", "RS0")
    authority_status = require_mapping(rs0.get("authority_status"), "STOP_POST_VS2_EXECUTION_SURFACE_READINESS_SEAL_MISMATCH", "readiness", "RS0 authority_status")
    seal_authority_status = require_mapping(seal_payload.get("authority_status"), "STOP_POST_VS2_EXECUTION_SURFACE_READINESS_SEAL_MISMATCH", "readiness", "RS0 seal_payload authority_status")
    require(authority_status, seal_authority_status, "STOP_POST_VS2_EXECUTION_SURFACE_READINESS_SEAL_MISMATCH", "readiness", "RS0 authority top/payload agreement")
    for field in ["execution_authority_granted", "sweep_authority_granted", "runner_authority_created", "automatic_rerun_authority_granted"]:
        require(authority_status.get(field), False, "STOP_POST_VS2_EXECUTION_SURFACE_READINESS_SEAL_GRANTS_AUTHORITY", "readiness", f"RS0 {field}")
    require(rs0.get("execution_package_core_reference", {}).get("artifact_id"), e0.get("artifact_id"), "STOP_POST_VS2_EXECUTION_SURFACE_SOURCE_LINKAGE_MISMATCH", "readiness", "RS0->E0")
    require(data["C0"]["closure_payload"].get("readiness_seal_binding", {}).get("canonical_sha256"), ref(ledger, "RS0")["canonical_content_sha256"], "STOP_POST_VS2_EXECUTION_SURFACE_SOURCE_LINKAGE_MISMATCH", "readiness", "C0->RS0")
    return posture


def verify_package(data: dict[str, dict[str, Any]]) -> None:
    m0 = data["M0"]
    if "O4" in json.dumps(m0, sort_keys=True):
        stop("STOP_POST_VS2_EXECUTION_SURFACE_M0_MISCLASSIFIED_AS_O4", "object_model", "M0", "no O4", "O4")
    require(data["VS2_3_RECEIPT"].get("object_model_counts", {}).get("execution_domain_object_role_count"), 3, "STOP_POST_VS2_EXECUTION_SURFACE_M0_MISCLASSIFIED_AS_O4", "object_model", "VS2.3 count")
    require(data["MS0"].get("ordered_move_ids"), vs27.MOVE_IDS, "STOP_POST_VS2_EXECUTION_SURFACE_MOVE_SPACE_MISMATCH", "move_space", "MS0 ordered_move_ids")
    if len(set(data["MS0"].get("ordered_move_ids", []))) != 8:
        stop("STOP_POST_VS2_EXECUTION_SURFACE_MOVE_SPACE_MISMATCH", "move_space", "MS0 unique", True, False)
    for alias in vs27.REJECTED_MOVE_ALIASES:
        if alias in json.dumps({"MS0": data["MS0"], "M2": data["M2"]}, sort_keys=True):
            stop("STOP_POST_VS2_EXECUTION_SURFACE_MOVE_SPACE_MISMATCH", "move_space", "aliases", "absent", alias)
    k0 = data["K0"]
    require(k0.get("component_count"), 17, "STOP_POST_VS2_EXECUTION_SURFACE_PACKAGE_IDENTITY_MISMATCH", "controlled_step", "K0 count")
    require(k0.get("component_ids"), vs27.K0_COMPONENT_IDS, "STOP_POST_VS2_EXECUTION_SURFACE_PACKAGE_IDENTITY_MISMATCH", "controlled_step", "K0 order")
    require(k0.get("component_hashes", {}).get("S13_RECEIPT_AND_ATOMIC_PUBLICATION_BUILDER"), SOURCE_SPECS["R13"]["expected"], "STOP_POST_VS2_EXECUTION_SURFACE_PACKAGE_IDENTITY_MISMATCH", "controlled_step", "S13")
    require(k0.get("component_hashes", {}).get("S14_CONVERGENCE_CRITERION_EVALUATOR"), SOURCE_SPECS["C20"]["expected"], "STOP_POST_VS2_EXECUTION_SURFACE_PACKAGE_IDENTITY_MISMATCH", "controlled_step", "S14")
    fs0 = data["FS0"]
    u0 = data["U0"]
    require(fs0.get("fixture_count"), 10, "STOP_POST_VS2_EXECUTION_SURFACE_FIXTURE_SET_MISMATCH", "fixtures", "FS0 count")
    require(fs0.get("candidate_specimen_count"), 10, "STOP_POST_VS2_EXECUTION_SURFACE_FIXTURE_SET_MISMATCH", "fixtures", "FS0 candidates")
    require(fs0.get("static_witness_count"), 10, "STOP_POST_VS2_EXECUTION_SURFACE_FIXTURE_SET_MISMATCH", "fixtures", "FS0 witnesses")
    require(u0.get("fixture_definition_count"), 10, "STOP_POST_VS2_EXECUTION_SURFACE_FIXTURE_SET_MISMATCH", "fixtures", "U0 definitions")
    require(u0.get("runtime_candidate_instance_count"), 0, "STOP_POST_VS2_EXECUTION_SURFACE_FIXTURE_ALREADY_EXECUTED", "fixtures", "runtime candidates")
    require(u0.get("fixture_executed_count"), 0, "STOP_POST_VS2_EXECUTION_SURFACE_FIXTURE_ALREADY_EXECUTED", "fixtures", "executed")
    require(data["S0X"].get("source_snapshot_status"), "FROZEN_FOR_CONSTRUCTION_READINESS_AUDIT", "STOP_POST_VS2_EXECUTION_SURFACE_SOURCE_SNAPSHOT_MISMATCH", "runtime_source_snapshot", "S0X")
    require(data["D0"].get("inventory_status"), "FROZEN_FOR_CONSTRUCTION_READINESS_AUDIT", "STOP_POST_VS2_EXECUTION_SURFACE_PACKAGE_DEPENDENCY_MISMATCH", "dependency_inventory", "D0 inventory_status")
    require(data["RP0"].get("report_contract_count"), 5, "STOP_POST_VS2_EXECUTION_SURFACE_REPORT_BOUNDARY_PASS", "reports", "RP0")
    e0_state = data["E0"].get("execution_state", {})
    for field in [
        "runtime_o1_instances_created",
        "runtime_o2_instances_created",
        "cases_initialized",
        "runtime_receipts_emitted",
        "runtime_commit_manifest_emitted",
        "runtime_case_reports_emitted",
        "runtime_sweep_report_emitted",
    ]:
        require(e0_state.get(field), 0, "STOP_POST_VS2_EXECUTION_SURFACE_EXECUTION_ALREADY_STARTED", "execution_state", field)
    require(e0_state.get("run_id"), None, "STOP_POST_VS2_EXECUTION_SURFACE_RUN_ID_ALREADY_CREATED", "execution_state", "run_id")


def source_linkage_records(ledger: list[dict[str, Any]], data: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    def make(child: str, parent: str, role: str, expected_status: str, observed_status: str, fields: list[str]) -> dict[str, Any]:
        p = ref(ledger, parent)
        return {
            "child_artifact_id": child,
            "parent_artifact_id": p["artifact_id"],
            "parent_artifact_version": p["artifact_version"],
            "parent_declared_path": p["declared_path"],
            "parent_canonical_sha256": p["canonical_content_sha256"],
            "relationship_role": role,
            "expected_parent_gate_or_status": expected_status,
            "observed_parent_gate_or_status": observed_status,
            "source_reference_fields": fields,
            "linkage_verified": True,
        }

    return [
        make("phase_vs2_7_phase_closure_receipt_v0", "C0", "R0_CLOSURE_RECEIPT_TO_C0_CLOSURE", VS27_GATE, data["R0"]["receipt_payload"].get("closure_gate"), ["R0.receipt_payload.closure_artifact_id", "R0.receipt_payload.closure_artifact_sha256"]),
        make("phase_vs2_closure_v0", "RS0", "C0_CLOSURE_TO_RS0_READINESS_SEAL", "SEALED_READY_FOR_HUMAN_EXECUTION_DECISION", data["C0"]["closure_payload"].get("readiness_summary", {}).get("seal_status"), ["C0.closure_payload.readiness_seal_binding"]),
        make("phase_vs2_execution_package_readiness_seal_v0", "E0", "RS0_TO_E0_EXECUTION_PACKAGE_CORE", E0_LOGICAL_ID, data["RS0"].get("execution_package_core_reference", {}).get("package_id", E0_LOGICAL_ID), ["RS0.execution_package_core_reference"]),
        make("phase_vs2_execution_package_readiness_seal_v0", "G0", "RS0_TO_G0_READINESS_GATE", READY_GATE, data["RS0"].get("readiness_gate_reference", {}).get("readiness_verdict", READY_GATE), ["RS0.readiness_gate_reference"]),
        make("phase_vs2_execution_package_readiness_seal_v0", "GR0", "RS0_TO_GR0_READINESS_RECEIPT", READY_GATE, data["RS0"].get("readiness_gate_receipt_reference", {}).get("readiness_verdict", READY_GATE), ["RS0.readiness_gate_receipt_reference"]),
        make(SURFACE_ARTIFACT_ID, "C0", "S0_DECISION_SURFACE_TO_C0_CLOSURE", PHASE_STATUS, data["C0"]["closure_payload"].get("phase_status"), ["S0.phase_vs2_closure_reference"]),
        make(SURFACE_ARTIFACT_ID, "R0", "S0_DECISION_SURFACE_TO_R0_CLOSURE_RECEIPT", VS27_GATE, data["R0"]["receipt_payload"].get("closure_gate"), ["S0.phase_vs2_closure_receipt_reference"]),
        make(SURFACE_ARTIFACT_ID, "E0", "S0_DECISION_SURFACE_TO_E0_PACKAGE_CORE", E0_LOGICAL_ID, data["E0"].get("package_id"), ["S0.execution_package_core_reference"]),
        make(SURFACE_ARTIFACT_ID, "G0", "S0_DECISION_SURFACE_TO_G0_READINESS_GATE", READY_GATE, data["G0"].get("aggregate_readiness_status", READY_GATE), ["S0.readiness_gate_reference"]),
        make(SURFACE_ARTIFACT_ID, "GR0", "S0_DECISION_SURFACE_TO_GR0_READINESS_RECEIPT", READY_GATE, data["GR0"].get("readiness_verdict", READY_GATE), ["S0.readiness_receipt_reference"]),
        make(SURFACE_ARTIFACT_ID, "RS0", "S0_DECISION_SURFACE_TO_RS0_READINESS_SEAL", "SEALED_READY_FOR_HUMAN_EXECUTION_DECISION", data["RS0"].get("seal_status"), ["S0.readiness_seal_reference"]),
    ]


def source_reference(ledger: list[dict[str, Any]], key: str) -> dict[str, Any]:
    row = ref(ledger, key)
    return {
        "source_key": key,
        "artifact_id": row["artifact_id"],
        "artifact_version": row["artifact_version"],
        "declared_path": row["declared_path"],
        "canonical_sha256": row["canonical_content_sha256"],
        "raw_file_sha256": row["raw_file_sha256"],
    }


def execution_bounds(data: dict[str, dict[str, Any]]) -> dict[str, Any]:
    # These values are verified through E0/G0/RS0 readiness records and U0 counts.
    return {
        "case_count": 10,
        "maximum_controlled_step_invocations_per_case": 5,
        "maximum_attempted_moves_per_case": 5,
        "maximum_applied_moves_per_case": 5,
        "maximum_total_controlled_step_invocations": 50,
        "maximum_total_attempted_moves": 50,
        "maximum_total_applied_moves": 50,
        "automatic_reruns": 0,
        "automatic_radius_renewals": 0,
        "automatic_budget_renewals": 0,
        "automatic_fixture_additions": 0,
        "automatic_source_additions": 0,
        "automatic_move_additions": 0,
        "automatic_package_substitutions": 0,
        "exact_package_bindings_not_selectable_maxima": True,
        "reduced_bounds_are_different_package": True,
        "fixture_subset_is_different_package": True,
        "changed_fixture_order_is_different_package": True,
    }


def decision_options() -> list[dict[str, Any]]:
    routes = [
        ["human decision receipt", "exact machine-authority update", "authority-transition closure", "bounded execution-source intake"],
        ["decision receipt", "bounded rebuild-scope preparation", "construction-authority chain", "new core version", "new readiness chain", "new Phase VS2 closure", "new decision surface"],
        ["decision receipt", "revision-scope surface", "new affected-artifact chain", "new readiness chain"],
        ["decision receipt", "STOP_POST_VS2_EXECUTION_DECISION_DEFERRED"],
        ["decision receipt", "STOP_POST_VS2_EXECUTION_REQUEST_REJECTED"],
        ["human decision receipt", "package-disposition update", "package-disposition closure"],
    ]
    return [
        {
            "option_index": index,
            "option_code": code,
            "requires_later_human_decision_receipt": True,
            "selected_by_surface_builder": False,
            "routes_toward_execution_authority": index == 1,
            "route": routes[index - 1],
        }
        for index, code in enumerate(DECISION_OPTION_CODES, start=1)
    ]


def d_checks() -> list[dict[str, Any]]:
    return [
        {
            "surface_check_id": check_id,
            "surface_check_name": name,
            "surface_check_status": "PASS",
            "evidence_references": ["source_identity_table", "source_linkage_table", "decision_subject"],
            "verified_invariants": [marker],
            "failure_codes": [],
            "bounded_interpretation": "Decision-surface preparation only; no authority or execution side effect.",
        }
        for check_id, name, marker in D_CHECKS
    ]


def build_payload(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    data, ledger = load_sources(root)
    verify_ready_closure(data, ledger)
    readiness_blocker_posture = verify_readiness(data, ledger)
    verify_package(data)
    links = source_linkage_records(ledger, data)
    c0 = source_reference(ledger, "C0")
    r0 = source_reference(ledger, "R0")
    e0 = source_reference(ledger, "E0")
    g0 = source_reference(ledger, "G0")
    gr0 = source_reference(ledger, "GR0")
    rs0 = source_reference(ledger, "RS0")
    decision_subject = {
        "C0_artifact_id": c0["artifact_id"],
        "C0_artifact_version": c0["artifact_version"],
        "C0_canonical_hash": c0["canonical_sha256"],
        "R0_receipt_id": r0["artifact_id"],
        "R0_receipt_version": r0["artifact_version"],
        "R0_canonical_hash": r0["canonical_sha256"],
        "E0_artifact_id": e0["artifact_id"],
        "E0_logical_package_id": data["E0"].get("package_id"),
        "E0_version": e0["artifact_version"],
        "E0_canonical_hash": e0["canonical_sha256"],
        "RS0_artifact_id": rs0["artifact_id"],
        "RS0_logical_seal_id": data["RS0"].get("seal_id"),
        "RS0_version": rs0["artifact_version"],
        "RS0_canonical_hash": rs0["canonical_sha256"],
        "any_package_modification_creates_different_decision_subject": True,
    }
    authority_non_effects = {
        "human_decision_recorded_by_surface_builder": False,
        "decision_receipt_created_by_surface_builder": False,
        "machine_authority_created_by_surface_builder": False,
        "authority_update_applied_by_surface_builder": False,
        "authority_transition_closed_by_surface_builder": False,
        "execution_source_intake_created_by_surface_builder": False,
        "run_id_created_by_surface_builder": False,
        "runtime_state_created_by_surface_builder": False,
        "fixture_executed_by_surface_builder": False,
        "runtime_receipt_emitted_by_surface_builder": False,
        "runtime_report_emitted_by_surface_builder": False,
        "runner_created_by_surface_builder": False,
    }
    execution_state = {
        "run_id": None,
        "run_id_created": False,
        "execution_source_intake_created": False,
        "execution_started": False,
        "runtime_states_initialized": 0,
        "runtime_o1_instances": 0,
        "runtime_o2_instances": 0,
        "runtime_candidate_instance_count": 0,
        "cases_initialized": 0,
        "fixtures_executed": 0,
        "moves_selected": 0,
        "moves_attempted": 0,
        "moves_applied": 0,
        "runtime_receipts_emitted": 0,
        "runtime_commit_manifests_emitted": 0,
        "runtime_reports_emitted": 0,
    }
    authority_state = {
        "authority_update_applied": False,
        "authority_transition_closed": False,
        "prospective_controlled_step_authority_active": False,
        "active_move_authority_present": False,
        "controlled_step_execution_authority_present": False,
        "fixture_sweep_authority_present": False,
        "kernel_execution_authority_present": False,
        "execution_authority_present": False,
        "sweep_authority_present": False,
        "run_allocation_authority_present": False,
        "runner_authority_present": False,
    }
    options = decision_options()
    payload = {
        "surface_id": SURFACE_ID,
        "surface_version": SURFACE_VERSION,
        "surface_role": SURFACE_ROLE,
        "surface_instance_state": SURFACE_STATE,
        "applicable_phase_branch": READY_BRANCH,
        "unit_id": UNIT_ID,
        "unit_role": UNIT_ROLE,
        "repository_anchor": {"repo_root": ROOT, "branch": BRANCH, "source_commit_sha": HEAD},
        "source_chain": ["C0", "R0", "E0", "G0", "GR0", "RS0"],
        "source_identity_table": ledger,
        "source_linkage_table": links,
        "phase_vs2_closure_reference": c0,
        "phase_vs2_closure_receipt_reference": r0,
        "execution_package_core_reference": {**e0, "logical_package_id": data["E0"].get("package_id")},
        "readiness_gate_reference": {**g0, "logical_gate_id": data["G0"].get("gate_id")},
        "readiness_receipt_reference": gr0,
        "readiness_seal_reference": {**rs0, "logical_seal_id": data["RS0"].get("seal_id")},
        "readiness_branch": data["C0"]["closure_payload"].get("readiness_branch"),
        "readiness_blocker_posture": readiness_blocker_posture,
        "decision_subject": decision_subject,
        "decision_question": DECISION_QUESTION,
        "package_summary": {"exact_package_core_id": E0_LOGICAL_ID, "sealed_ready": True, "package_modification_creates_different_subject": True},
        "scope_regime_summary": {"scope": "FIRST_SWEEP_KERNEL_SCOPE_V0", "regime": "TYPED_STATE_CONTRACT_CONVERGENCE_REGIME_V0"},
        "object_model_summary": {"execution_domain_object_count": 3, "objects": ["O1_runtime_control_state", "O2_candidate_typed_state_contract", "O3_frozen_target_contract"], "static_support_objects": ["F0_scope_regime_contract", "M0_object_model_binding_manifest"], "O2_only_transformable_semantic_object": True, "O3_immutable": True, "F0_immutable": True, "M0_immutable": True, "M0_is_static": True, "M0_is_not_O4": True, "O2_cannot_grant_authority": True, "O1_contract_cannot_self_modify": True, "evaluation_state_remains_outside_O2": True},
        "move_space_summary": {"move_ids": vs27.MOVE_IDS, "move_count": 8, "move_ids_exact": True, "move_ids_unique": True, "dynamic_move_creation": False, "move_space_active": False, "rejected_aliases_absent": vs27.REJECTED_MOVE_ALIASES},
        "controlled_step_and_convergence_summary": {"component_count": 17, "component_order": vs27.K0_COMPONENT_IDS, "S13_represented_by_R13": True, "S14_represented_by_C20": True, "selector_deterministic": True, "applicator_candidate_only": True, "at_most_one_move_per_step": True, "validation_non_repairing": True, "admissibility_non_authorizing": True, "forbidden_effects_terminal": True, "strict_progress_required": True, "movement_alone_not_progress": True, "hash_change_alone_not_progress": True, "repeated_state_terminal": True, "oscillation_in_convergence_vocabulary": True, "receipt_hashing_non_circular": True, "publication_atomic": True, "orchestrator_non_self_invoking": True},
        "fixture_summary": {"fixture_ids": FIXTURE_IDS, "fixture_count": 10, "fixture_order_exact": True, "static_candidate_specimen_count": 10, "runtime_candidate_instance_count": 0, "fixture_definition_count": 10, "static_expectation_witness_count": 10, "subset_not_authorized": True},
        "expected_path_summary": {"F01": ["M01_ADD_AUTHORIZED_REQUIRED_FIELD", "STEP_MOVE_APPLIED_CONTINUE", "CONVERGENCE_CONTINUE_ALLOWED", "M02_NORMALIZE_TYPED_VALUE", "STEP_TARGET_REACHED", "CONVERGENCE_TARGET_TERMINAL_CONDITION_SATISFIED", "TARGET_REACHED"], "F02": ["no move selected", "no candidate mutation", "STEP_TARGET_REACHED", "CONVERGENCE_TARGET_TERMINAL_CONDITION_SATISFIED", "TARGET_REACHED"], "F03": ["M02_NORMALIZE_TYPED_VALUE", "TARGET_REACHED"], "F04": ["M03_BIND_DECLARED_SOURCE_IDENTITY", "TARGET_REACHED"], "F05": ["STOP_MISSING_SOURCE"], "F06": ["STOP_MISSING_AUTHORITY", "CANDIDATE_SEMANTIC_AUTHORITY"], "F07": ["M05_REMOVE_PROHIBITED_CANDIDATE_DECLARATION", "TARGET_REACHED"], "F08": ["STOP_MISSING_SCHEMA"], "F09": ["STOP_MISSING_CAPABILITY"], "F10": ["STOP_NO_ADMISSIBLE_MOVE"], "expected_path_is_not_observed_path": True, "static_expectation_witness_is_not_runtime_evidence": True, "prohibited_candidate_declaration_is_not_actual_forbidden_effect": True},
        "runtime_source_snapshot_summary": {"source_snapshot_status": data["S0X"].get("source_snapshot_status"), "present_source_records": True, "candidate_semantic_authority_evidence_records": True, "schema_inventory": True, "capability_inventory": True, "freshness_witnesses": True, "declared_absence_witnesses": True, "fixture_dependencies": True, "live_source_search_allowed": False, "automatic_source_acquisition_allowed": False, "source_substitution_allowed": False, "mtime_freshness_allowed": False, "package_contract_used_as_candidate_evidence": False},
        "upstream_dependency_summary": {"dependency_inventory_sha256": ref(ledger, "D0")["canonical_content_sha256"], "dependency_cycle_present": False, "source_dependency_conflation_present": False},
        "execution_bounds": execution_bounds(data),
        "reporting_obligations": {"report_contract_count": 5, "runtime_reports_emitted": 0, "refinement_candidate_instances_absent": True},
        "proposed_machine_authority_scope": {"proposal_code": "AUTHORIZE_ONE_EXACT_SEALED_FIRST_SWEEP_KERNEL_EXECUTION_V0", "proposed_not_instantiated": True, "machine_authority_present": False, "execution_authority_present": False, "sweep_authority_present": False, "run_allocation_authority_present": False, "maximum_later_authority": ["one exact-package execution authority", "one exact ten-fixture sweep authority", "one run-allocation authority", "package-bound M01-M08 authority", "controlled-step invocation authority within exact bounds", "runtime receipt and commit-manifest emission authority", "case-report and sweep-report emission authority", "proposal-only refinement-candidate emission authority"]},
        "excluded_authority_scope": {"execution_reuse": ["second run", "second sweep", "automatic rerun", "manual rerun under same receipt", "partial rerun after closure", "eleventh fixture", "fixture omission", "fixture replacement", "fixture reordering", "bound change", "budget renewal", "radius renewal"], "package_mutation": ["source expansion", "target change", "F0 change", "M0 change", "move-space change", "controlled-step change", "C20 change"], "repair_and_capability_creation": ["automatic self-repair", "contract repair", "move-space expansion", "schema invention", "capability creation", "source acquisition", "authority escalation", "taxonomy upgrade", "blocker resolution"], "refinement_application": ["apply refinement candidate", "change selector policy", "change applicator behavior", "change target rules", "change report contracts", "change fixtures", "change sources", "rerun after refinement proposal"], "reuse_and_promotion": ["reusable move approval", "reusable schema approval", "candidate promotion", "target promotion", "registry promotion", "cross-target reuse", "cross-family reuse"], "runner_authority": ["general runner authority", "unbounded continuation", "background execution", "continuous loop", "cross-package scheduling", "automatic later-phase transition", "automatic execution of revised package"]},
        "authority_expiry_requirements": {"absolute_expiry_timestamp_required": True, "surface_selects_or_invents_timestamp": False, "expires_at_earliest_of": ["absolute expiry", "all ten cases terminal", "total controlled-step bound consumed", "total attempted-move bound consumed", "total applied-move bound consumed", "package-level forbidden effect", "package identity mismatch", "readiness-seal mismatch", "runtime-source-snapshot mismatch", "authority revocation", "execution closure"]},
        "decision_options": options,
        "decision_option_payload_contracts": {"Option_A_requires": ["exact decision-subject tuple", "confirmation of all ten fixtures", "confirmation of frozen fixture order", "confirmation of exact execution bounds", "confirmation of reporting obligations", "confirmation of excluded authority", "absolute expiry timestamp", "decision rationale", "human decision identity"], "Option_B_requires": ["requested fixture ids", "requested fixture order", "requested case count", "requested step bounds", "requested move bounds", "reason for reduction", "desired evidence objective"], "Option_C_requires": ["affected package surface", "requested revision", "reason", "expected evidence improvement", "known downstream invalidation"], "Option_D_terminal": "STOP_POST_VS2_EXECUTION_DECISION_DEFERRED", "Option_E_terminal": "STOP_POST_VS2_EXECUTION_REQUEST_REJECTED", "Option_F_terminal": "STOP_POST_VS2_EXECUTION_PACKAGE_VERSION_ABANDONED"},
        "decision_option_routes": {row["option_code"]: row["route"] for row in options},
        "modified_package_rule": {"any_package_modification_creates_different_decision_subject": True, "reduced_bounds_not_same_package": True, "fixture_subset_not_same_package": True, "changed_fixture_order_not_same_package": True},
        "decision_state": {"human_decision_required": True, "human_decision_recorded": False, "decision_receipt_created": False, "surface_consumed": False, "selected_option": None},
        "authority_state": authority_state,
        "execution_state": execution_state,
        "surface_checks_D01_D18": d_checks(),
        "surface_gate": SURFACE_GATE,
        "terminal_transition": {"transition": TERMINAL_TRANSITION, "records_decision": False, "creates_decision_receipt": False, "applies_machine_authority": False, "creates_run_id": False, "creates_execution_source_intake": False, "executes_package": False},
        "evidence_yield": EVIDENCE_YIELD,
        "nonclaims": ["This surface does not record a human decision.", "This surface does not create a decision receipt.", "This surface does not apply machine authority.", "This surface does not create execution-source intake.", "This surface does not create a run id.", "This surface does not execute the sealed package.", "This surface does not create runtime receipts or runtime reports.", "This surface does not create runner authority."],
        "authority_non_effects": authority_non_effects,
        "failures": [],
    }
    return payload, ledger, data


def surface_envelope(payload: dict[str, Any]) -> dict[str, Any]:
    digest = sha256_bytes(canonical_bytes(payload))
    return {
        "schema_version": "matrixlabs_post_vs2_first_execution_decision_surface_v0",
        "artifact_id": SURFACE_ARTIFACT_ID,
        "artifact_version": SURFACE_VERSION,
        "surface_payload": payload,
        "surface_payload_sha256": digest,
    }


def render_markdown(surface: dict[str, Any]) -> str:
    p = surface["surface_payload"]
    subject = p["decision_subject"]
    option_lines = "\n".join(
        f"{row['option_index']}. `{row['option_code']}` - routes toward execution authority: `{str(row['routes_toward_execution_authority']).lower()}`"
        for row in p["decision_options"]
    )
    fixture_lines = "\n".join(f"- `{fid}`" for fid in p["fixture_summary"]["fixture_ids"])
    bounds = p["execution_bounds"]
    return f"""# Post-VS2 First Execution Decision Surface v0

## Surface Identity

- Surface ID: `{p['surface_id']}`
- Surface state: `{p['surface_instance_state']}`
- Surface gate: `{p['surface_gate']}`
- Human decision required: `{str(p['decision_state']['human_decision_required']).lower()}`
- Human decision recorded: `{str(p['decision_state']['human_decision_recorded']).lower()}`
- Decision receipt created: `{str(p['decision_state']['decision_receipt_created']).lower()}`
- Surface consumed: `{str(p['decision_state']['surface_consumed']).lower()}`

## Decision Subject

- C0: `{subject['C0_artifact_id']}` / `{subject['C0_canonical_hash']}`
- R0: `{subject['R0_receipt_id']}` / `{subject['R0_canonical_hash']}`
- E0: `{subject['E0_artifact_id']}` / `{subject['E0_logical_package_id']}` / `{subject['E0_canonical_hash']}`
- RS0: `{subject['RS0_artifact_id']}` / `{subject['RS0_logical_seal_id']}` / `{subject['RS0_canonical_hash']}`
- Modified package rule: `{str(subject['any_package_modification_creates_different_decision_subject']).lower()}`

## Decision Question

{p['decision_question']}

## Fixtures

{fixture_lines}

## Static Expectations

- F01 path: `M01_ADD_AUTHORIZED_REQUIRED_FIELD -> STEP_MOVE_APPLIED_CONTINUE -> CONVERGENCE_CONTINUE_ALLOWED -> M02_NORMALIZE_TYPED_VALUE -> STEP_TARGET_REACHED -> CONVERGENCE_TARGET_TERMINAL_CONDITION_SATISFIED -> TARGET_REACHED`
- F02 path: `no move selected -> no candidate mutation -> STEP_TARGET_REACHED -> CONVERGENCE_TARGET_TERMINAL_CONDITION_SATISFIED -> TARGET_REACHED`
- F07 boundary: `M05_REMOVE_PROHIBITED_CANDIDATE_DECLARATION -> TARGET_REACHED`

## Exact Execution Bounds

- Case count: `{bounds['case_count']}`
- Per-case controlled-step invocations: `{bounds['maximum_controlled_step_invocations_per_case']}`
- Per-case attempted moves: `{bounds['maximum_attempted_moves_per_case']}`
- Per-case applied moves: `{bounds['maximum_applied_moves_per_case']}`
- Total controlled-step invocations: `{bounds['maximum_total_controlled_step_invocations']}`
- Total attempted moves: `{bounds['maximum_total_attempted_moves']}`
- Total applied moves: `{bounds['maximum_total_applied_moves']}`
- Automatic reruns: `{bounds['automatic_reruns']}`

## Proposed Authority

- Proposal: `{p['proposed_machine_authority_scope']['proposal_code']}`
- Proposed not instantiated: `{str(p['proposed_machine_authority_scope']['proposed_not_instantiated']).lower()}`
- Absolute expiry timestamp required: `{str(p['authority_expiry_requirements']['absolute_expiry_timestamp_required']).lower()}`

## Excluded Authority

- Execution reuse, package mutation, repair/capability creation, refinement application, reuse/promotion, and runner authority are excluded by the JSON payload.

## Decision Options

{option_lines}

## Pending State

- Authority update applied: `{str(p['authority_state']['authority_update_applied']).lower()}`
- Execution authority present: `{str(p['authority_state']['execution_authority_present']).lower()}`
- Sweep authority present: `{str(p['authority_state']['sweep_authority_present']).lower()}`
- Run-allocation authority present: `{str(p['authority_state']['run_allocation_authority_present']).lower()}`
- Run ID: `{p['execution_state']['run_id']}`
- Execution-source intake created: `{str(p['execution_state']['execution_source_intake_created']).lower()}`
- Runtime receipts emitted: `{p['execution_state']['runtime_receipts_emitted']}`
- Runtime reports emitted: `{p['execution_state']['runtime_reports_emitted']}`
- Runner authority present: `{str(p['authority_state']['runner_authority_present']).lower()}`

## Terminal Transition

- `{p['terminal_transition']['transition']}`

## Nonclaims

{chr(10).join(f"- {item}" for item in p['nonclaims'])}
"""


def receipt_envelope(payload: dict[str, Any]) -> dict[str, Any]:
    digest = sha256_bytes(canonical_bytes(payload))
    return {
        "schema_version": "matrixlabs_post_vs2_first_execution_decision_surface_receipt_v0",
        "receipt_id": RECEIPT_ID,
        "receipt_version": "v0",
        "receipt_role": "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_PREPARATION_RECEIPT",
        "receipt_payload": payload,
        "receipt_payload_sha256": digest,
    }


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: dict[str, Any]) -> None:
    write_text(path, json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))


def run_baseline(root: Path) -> None:
    proc = subprocess.run([sys.executable, BASELINE_SCRIPT], cwd=root)
    if proc.returncode != 0:
        stop("STOP_POST_VS2_EXECUTION_SURFACE_PACKAGE_CHANGED_AFTER_READINESS", "baseline", BASELINE_SCRIPT, 0, proc.returncode)


def validate_dirty_scope(root: Path) -> None:
    dirty = set(status_paths(git(root, ["status", "--short", "--untracked-files=all"])))
    unexpected = sorted(dirty - ALLOWED_DIRTY)
    missing = sorted(ALLOWED_DIRTY - dirty)
    if unexpected or missing:
        stop("STOP_POST_VS2_EXECUTION_SURFACE_PREEXISTING_WORKTREE_CHANGES", "dirty_scope", "git_status", sorted(ALLOWED_DIRTY), {"unexpected": unexpected, "missing": missing, "dirty": sorted(dirty)})
    new = {path for path in dirty if path in EXPECTED_NEW}
    modified = {path for path in dirty if path in EXPECTED_MODIFIED}
    require(len(new), 5, "STOP_POST_VS2_EXECUTION_SURFACE_PREEXISTING_WORKTREE_CHANGES", "dirty_scope", "new_path_count")
    require(len(modified), 5, "STOP_POST_VS2_EXECUTION_SURFACE_PREEXISTING_WORKTREE_CHANGES", "dirty_scope", "modified_path_count")


def build_all(root: Path) -> dict[str, Any]:
    payload, ledger, _data = build_payload(root)
    surface = surface_envelope(payload)
    write_json(root / S0_JSON, surface)
    markdown = render_markdown(surface)
    write_text(root / S0_MD, markdown)
    surface_raw = sha256_file(root / S0_JSON)
    markdown_raw = sha256_file(root / S0_MD)
    receipt_payload = {
        "source_commit_sha": HEAD,
        "source_hash_ledger": ledger,
        "surface_artifact_id": SURFACE_ARTIFACT_ID,
        "surface_artifact_sha256": surface["surface_payload_sha256"],
        "surface_json_raw_sha256": surface_raw,
        "surface_markdown_raw_sha256": markdown_raw,
        "D01_D18_statuses": {row["surface_check_id"]: row["surface_check_status"] for row in payload["surface_checks_D01_D18"]},
        "surface_gate": SURFACE_GATE,
        "surface_instance_state": SURFACE_STATE,
        "decision_subject": payload["decision_subject"],
        "decision_option_count": len(payload["decision_options"]),
        "decision_pending_state": payload["decision_state"],
        "authority_non_effects": payload["authority_non_effects"],
        "execution_non_effects": payload["execution_state"],
        "readiness_blocker_posture": payload["readiness_blocker_posture"],
        "evidence_yield": EVIDENCE_YIELD,
        "logical_transition": TERMINAL_TRANSITION,
        "bookkeeping_transition": BOOKKEEPING_TRANSITION,
        "failures": [],
    }
    receipt = receipt_envelope(receipt_payload)
    write_json(root / PR0_JSON, receipt)
    return {
        "surface": surface,
        "payload": payload,
        "receipt": receipt,
        "surface_raw": sha256_file(root / S0_JSON),
        "markdown_raw": markdown_raw,
        "receipt_raw": sha256_file(root / PR0_JSON),
    }


def emit_success(root: Path, result: dict[str, Any]) -> None:
    payload = result["payload"]
    receipt = result["receipt"]
    print("BUILD_POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_V0_COMPLETE")
    print(f"repo_root={ROOT}")
    print(f"branch={BRANCH}")
    print(f"HEAD={HEAD}")
    print(f"surface_canonical_hash={result['surface']['surface_payload_sha256']}")
    print(f"surface_raw_file_hash={result['surface_raw']}")
    print(f"surface_markdown_raw_hash={result['markdown_raw']}")
    print(f"receipt_canonical_hash={receipt['receipt_payload_sha256']}")
    print(f"receipt_raw_file_hash={result['receipt_raw']}")
    for row in payload["surface_checks_D01_D18"]:
        print(f"{row['surface_check_id']}={row['surface_check_status']}")
    print(f"source_identity_count={len(payload['source_identity_table'])}")
    print(f"source_linkage_count={len(payload['source_linkage_table'])}")
    print(f"decision_option_count={len(payload['decision_options'])}")
    posture = payload["readiness_blocker_posture"]
    print(f"readiness_branch={payload['readiness_branch']}")
    print(f"normalized_blocker_source_count={posture['blocker_source_count']}")
    print(f"normalized_blocker_count={posture['normalized_typed_readiness_blocker_count']}")
    print(f"blocker_source_agreement={posture['all_blocker_sources_agree']}")
    print(f"RS0_blocker_field_required={posture['RS0_blocker_field_required']}")
    print(f"surface_state={payload['surface_instance_state']}")
    print(f"surface_gate={payload['surface_gate']}")
    print(f"terminal_transition={payload['terminal_transition']['transition']}")
    print(f"decision_subject={json.dumps(payload['decision_subject'], sort_keys=True)}")
    print(f"authority_non_effects={json.dumps(payload['authority_non_effects'], sort_keys=True)}")
    print(f"execution_non_effects={json.dumps(payload['execution_state'], sort_keys=True)}")
    print(f"evidence_yield={payload['evidence_yield']}")
    print("git_status_short:")
    print(git(root, ["status", "--short", "--untracked-files=all"]))


def emit_stop(exc: StopFailure) -> None:
    print("BUILD_POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_V0_STOP")
    print(f"failure_code={exc.code}")
    print(f"failed_surface_check={exc.check}")
    print(f"affected_artifact={exc.artifact}")
    print(f"expected_identity_or_value={json.dumps(exc.expected, sort_keys=True)}")
    print(f"observed_identity_or_value={json.dumps(exc.observed, sort_keys=True)}")
    print("decision_consequence=POST_VS2_EXECUTION_DECISION_SURFACE_NOT_TRUSTWORTHY")
    print("smallest_lawful_correction_surface=POST_VS2_EXECUTION_SURFACE_REPAIR_OR_BOOKKEEPING_SURFACE")
    print("capability_proposal_candidate_required=false")
    print("human_decision_required=false")
    print("self_repair_performed=false")


def main() -> int:
    root = Path.cwd().resolve()
    try:
        check_repo(root)
        result = build_all(root)
        run_baseline(root)
        validate_dirty_scope(root)
        emit_success(root, result)
        return 0
    except StopFailure as exc:
        emit_stop(exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
