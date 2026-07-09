#!/usr/bin/env python3

"""Verify the PHASE VS0.2 happy-path A-to-F specimen without mutation."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


VERIFIER = "scripts/verify_phase_vs0_happy_path_v0.py"
PREFLIGHT = "docs/matrixlabs/phase_vs0/phase_vs0_source_inventory_v0.json"
BUILD_RECEIPT = "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_build_receipt_v0.json"
ORIGINAL_BUILD_COMMIT = "49ebcf1393893bbbc61c5fcd48359770c3e554e7"
REPAIR_COMMIT = "9f7277608f8e475fa84f6e4697e0db0903200aac"
BINDING_STATUS = "VS0_3_SOURCE_BUILD_BINDING_PASS_ORIGINAL_BUILD_PLUS_REPAIR_COMMIT"
OUTPUT_ROOT = "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/a_to_f"
CHAIN_INDEX = f"{OUTPUT_ROOT}/phase_vs0_a_to_f_chain_index_v0.json"
OUTPUT_JSON = "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_verification_v0.json"
OUTPUT_MD = "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_verification_v0.md"

SCHEMA_VERSION = "matrixlabs_phase_vs0_happy_path_verification_v0"
VERIFICATION_ID = "phase_vs0_happy_path_verification_v0"
PASS_STATUS = "VS0_3_HAPPY_PATH_VERIFICATION_PASS_A_TO_F_PHASE_SPECIMEN_VERIFIED"
TERMINAL_TRANSITION = "ADVANCE(VS0_4_NEGATIVE_SHORTCUT_PROBE_BATTERY_PENDING)"
BUILD_STATUS = "VS0_2_HAPPY_PATH_BUILD_PASS_A_TO_F_PHASE_SPECIMEN_CREATED"

EXPECTED_TERMINALS = ["A4", "B3", "C3", "D5", "E4", "F4"]
EXPECTED_EDGES = [
    ["A4", "B3"],
    ["B3", "C3"],
    ["C3", "D5"],
    ["D5", "E4"],
    ["E4", "F4"],
]
TERMINAL_FILES = {
    "A4": "a4_authority_transition_closure_v0.json",
    "B3": "b3_router_specimen_closure_v0.json",
    "C3": "c3_candidate_archive_admissibility_audit_v0.json",
    "D5": "d5_machine_proceed_closure_v0.json",
    "E4": "e4_compression_specimen_closure_v0.json",
    "F4": "f4_registry_candidate_closure_projection_v0.json",
}
TERMINAL_STATUSES = {
    "A4": "BLOCK_A_PASS_AUTHORITY_ADVANCED_TO_BASIS",
    "B3": "BLOCK_B_PASS_READ_ONLY_ROUTE_CLASSIFIED",
    "C3": "CANDIDATE_AUDIT_PASS_WELL_FORMED_NOT_PROMOTED",
    "D5": "MACHINE_PROCEED_CLOSURE_PASS_RADIUS_EXHAUSTED_STOP",
    "E4": "COMPRESSION_CLOSURE_PASS_OBSERVABILITY_ONLY",
    "F4": "REGISTRY_CANDIDATE_CLOSURE_PASS_CANDIDATE_ONLY",
}

FAILURE_CODES = [
    "VS0_3_STOP_HAPPY_PATH_BUILD_NOT_PASS",
    "VS0_3_FAIL_BUILD_RECEIPT_MISSING",
    "VS0_3_FAIL_BUILD_RECEIPT_NOT_PASS",
    "VS0_3_FAIL_BUILD_RECEIPT_WRONG_NEXT_OBJECT",
    "VS0_3_FAIL_BUILD_RECEIPT_CLAIMS_VERIFICATION_ALREADY_PERFORMED",
    "VS0_3_FAIL_CHAIN_INDEX_MISSING",
    "VS0_3_FAIL_CHAIN_INDEX_STATUS_MISMATCH",
    "VS0_3_FAIL_CHAIN_INDEX_ORDER_MISMATCH",
    "VS0_3_FAIL_CHAIN_INDEX_DEPENDENCY_EDGE_MISMATCH",
    "VS0_3_FAIL_CHAIN_INDEX_HASH_MISMATCH",
    "VS0_3_FAIL_PHASE_ARTIFACT_COUNT_MISMATCH",
    "VS0_3_FAIL_A4_MISSING",
    "VS0_3_FAIL_B3_MISSING",
    "VS0_3_FAIL_C3_MISSING",
    "VS0_3_FAIL_D5_MISSING",
    "VS0_3_FAIL_E4_MISSING",
    "VS0_3_FAIL_F4_MISSING",
    "VS0_3_FAIL_TERMINAL_CLOSURE_STATUS_MISMATCH",
    "VS0_3_FAIL_SOURCE_CHAIN_BROKEN",
    "VS0_3_FAIL_B3_DOES_NOT_REFERENCE_A4",
    "VS0_3_FAIL_C3_DOES_NOT_REFERENCE_B3",
    "VS0_3_FAIL_D5_DOES_NOT_REFERENCE_C3",
    "VS0_3_FAIL_E4_DOES_NOT_REFERENCE_D5",
    "VS0_3_FAIL_F4_DOES_NOT_REFERENCE_E4",
    "VS0_3_FAIL_AUTHORITY_STATE_PARITY_MISMATCH",
    "VS0_3_FAIL_REQUESTED_ACTION_PARITY_MISMATCH",
    "VS0_3_FAIL_SCOPE_PARITY_MISMATCH",
    "VS0_3_FAIL_SCOPE_OVERBROAD",
    "VS0_3_FAIL_CANDIDATE_STATUS_STRENGTHENED",
    "VS0_3_FAIL_C3_NOT_PROMOTED_BOUNDARY_DROPPED",
    "VS0_3_FAIL_PROMOTION_DECISION_MISSING",
    "VS0_3_FAIL_ACTIVE_ARCHIVE_ENTRY_SCOPE_MISMATCH",
    "VS0_3_FAIL_DECLARED_SCOPE_USE_OVERBROAD",
    "VS0_3_FAIL_MACHINE_ACTION_MISMATCH",
    "VS0_3_FAIL_UNIT_EXECUTED",
    "VS0_3_FAIL_RUNTIME_EXECUTED",
    "VS0_3_FAIL_RADIUS_NOT_CONSUMED",
    "VS0_3_FAIL_RADIUS_NOT_EXHAUSTED",
    "VS0_3_FAIL_RADIUS_RENEWED_AFTER_D5",
    "VS0_3_FAIL_COMPRESSION_TRACE_LABEL_MISMATCH",
    "VS0_3_FAIL_DECOMPRESSION_AUDIT_NOT_PASS",
    "VS0_3_FAIL_COMPRESSION_REPLACED_SOURCE_AUTHORITY",
    "VS0_3_FAIL_COMPRESSION_AUTHORIZED_REUSE",
    "VS0_3_FAIL_COMPRESSION_RENEWED_RADIUS",
    "VS0_3_FAIL_REGISTRY_TRACE_LABEL_MISMATCH",
    "VS0_3_FAIL_REGISTRY_STATUS_NOT_CANDIDATE",
    "VS0_3_FAIL_SPECIMEN_COUNT_MISMATCH",
    "VS0_3_FAIL_GENERALIZATION_CLAIMED",
    "VS0_3_FAIL_REGISTRY_ACTIVATED",
    "VS0_3_FAIL_ADDITIONAL_MACHINE_PROCEED_AUTHORIZED",
    "VS0_3_FAIL_NEXT_UNIT_EXECUTED",
    "VS0_3_FAIL_SOURCE_AUTHORITY_REPLACED_BY_COMPRESSION",
    "VS0_3_FAIL_RUNNER_AUTHORITY_CREATED",
    "VS0_3_FAIL_DISCUSSION_PACKETS_IN_SCOPE",
    "VS0_3_FAIL_VS0_3_MUTATED_PHASE_ARTIFACTS",
    "VS0_3_FAIL_VS0_3_RERAN_BUILDER",
    "VS0_3_FAIL_VS0_3_REPAIRED_ARTIFACTS",
    "VS0_3_FAIL_VS0_3_RAN_NEGATIVE_PROBES",
    "VS0_3_FAIL_VS0_3_CLOSED_PHASE",
    "VS0_3_FAIL_SOURCE_BUILD_BINDING_MISSING",
    "VS0_3_FAIL_SOURCE_BUILD_BINDING_UNEXPECTED_ORIGINAL_COMMIT",
    "VS0_3_FAIL_REPAIR_COMMIT_BINDING_MISSING",
    "VS0_3_FAIL_REPAIR_COMMIT_BINDING_UNEXPECTED",
    "VS0_3_FAIL_ACTIVE_ARTIFACT_COMMIT_MISMATCH",
]


class VerificationFailure(RuntimeError):
    def __init__(
        self,
        code: str,
        *,
        object_id: str = "",
        path: str = "",
        field: str = "",
        expected: object = None,
        actual: object = None,
        boundary: str = "",
        next_surface: str = "REPAIR_PROPOSAL_FOR_VS0_2_PHASE_ARTIFACT",
    ) -> None:
        super().__init__(code)
        self.code = code
        self.object_id = object_id
        self.path = path
        self.field = field
        self.expected = expected
        self.actual = actual
        self.boundary = boundary
        self.next_surface = next_surface


def fail(
    code: str,
    *,
    object_id: str = "",
    path: str = "",
    field: str = "",
    expected: object = None,
    actual: object = None,
    boundary: str = "",
) -> None:
    raise VerificationFailure(
        code,
        object_id=object_id,
        path=path,
        field=field,
        expected=expected,
        actual=actual,
        boundary=boundary,
    )


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
        fail("VS0_3_STOP_HAPPY_PATH_BUILD_NOT_PASS", actual=proc.stderr.strip())
    return Path(proc.stdout.strip()).resolve()


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
        fail("VS0_3_FAIL_VS0_3_MUTATED_PHASE_ARTIFACTS", actual=proc.stderr.strip())
    return proc.stdout.rstrip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path, missing_code: str) -> dict[str, Any]:
    if not path.is_file():
        fail(missing_code, path=str(path), expected="present", actual="missing")
    try:
        value = json.loads(path.read_text())
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(missing_code, path=str(path), expected="valid JSON", actual=str(exc))
    if not isinstance(value, dict):
        fail(missing_code, path=str(path), expected="JSON object", actual=type(value).__name__)
    return value


def expect(
    value: object,
    wanted: object,
    code: str,
    *,
    object_id: str,
    path: str,
    field: str,
    boundary: str,
) -> None:
    if value != wanted:
        fail(
            code,
            object_id=object_id,
            path=path,
            field=field,
            expected=wanted,
            actual=value,
            boundary=boundary,
        )


def contains_scalar(value: object, wanted: object) -> bool:
    if isinstance(value, dict):
        return any(contains_scalar(item, wanted) for item in value.values())
    if isinstance(value, list):
        return any(contains_scalar(item, wanted) for item in value)
    return value == wanted


def find_key_values(value: object, wanted_key: str) -> list[object]:
    found: list[object] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key == wanted_key:
                found.append(item)
            found.extend(find_key_values(item, wanted_key))
    elif isinstance(value, list):
        for item in value:
            found.extend(find_key_values(item, wanted_key))
    return found


def validate_dirty_scope(root: Path) -> None:
    status = run_git(root, ["status", "--short"]).splitlines()
    allowed_exact = {VERIFIER, "scripts/build_baseline_share_v0.py"}
    allowed_prefixes = (
        "baseline_share/",
        "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_verification_v0.",
    )
    for line in status:
        path = line[3:]
        if path == "discussion_packets/" or path in allowed_exact:
            continue
        if any(path.startswith(prefix) for prefix in allowed_prefixes):
            continue
        fail(
            "VS0_3_FAIL_VS0_3_MUTATED_PHASE_ARTIFACTS",
            path=path,
            field="git_status_short",
            expected="clean verification input",
            actual=line,
            boundary="VS0.3 read-only verification scope",
        )


def load_committed_input(
    root: Path, relative_path: str, missing_code: str
) -> tuple[dict[str, Any], str, str]:
    path = root / relative_path
    value = load_json(path, missing_code)
    digest = sha256(path)
    proc = subprocess.run(
        ["git", "show", f"HEAD:{relative_path}"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0 or hashlib.sha256(proc.stdout).hexdigest() != digest:
        fail(
            "VS0_3_FAIL_VS0_3_MUTATED_PHASE_ARTIFACTS",
            path=relative_path,
            field="worktree_hash",
            expected="HEAD blob hash",
            actual=digest,
            boundary="committed VS0.2 verification input",
        )
    commit = run_git(root, ["log", "-n", "1", "--format=%H", "--", relative_path])
    return value, digest, commit


def verify_build_receipt(root: Path) -> tuple[dict[str, Any], str, str]:
    receipt, digest, commit = load_committed_input(
        root, BUILD_RECEIPT, "VS0_3_FAIL_BUILD_RECEIPT_MISSING"
    )
    if commit != ORIGINAL_BUILD_COMMIT:
        fail(
            "VS0_3_FAIL_SOURCE_BUILD_BINDING_UNEXPECTED_ORIGINAL_COMMIT",
            object_id="phase_vs0_happy_path_build_receipt_v0",
            path=BUILD_RECEIPT,
            field="original_vs0_2_build_commit_sha",
            expected=ORIGINAL_BUILD_COMMIT,
            actual=commit,
            boundary="original VS0.2 build receipt binding",
        )
    required = {
        "schema_version": "matrixlabs_phase_vs0_happy_path_build_receipt_v0",
        "build_receipt_id": "phase_vs0_happy_path_build_receipt_v0",
        "phase_id": "PHASE_VS0",
        "phase_step": "VS0.2",
        "build_role": "HAPPY_PATH_A_TO_F_PHASE_SPECIMEN_BUILD_ONLY",
        "happy_path_build_status": BUILD_STATUS,
        "happy_path_build_gate": BUILD_STATUS,
        "next_required_object": "phase_vs0_happy_path_verification_v0",
        "terminal_transition": "ADVANCE(VS0_3_HAPPY_PATH_CLOSURE_VERIFICATION_PENDING)",
    }
    for field, wanted in required.items():
        code = (
            "VS0_3_FAIL_BUILD_RECEIPT_WRONG_NEXT_OBJECT"
            if field == "next_required_object"
            else "VS0_3_FAIL_BUILD_RECEIPT_NOT_PASS"
        )
        expect(
            receipt.get(field),
            wanted,
            code,
            object_id="phase_vs0_happy_path_build_receipt_v0",
            path=BUILD_RECEIPT,
            field=field,
            boundary="VS0.2 build receipt pass gate",
        )
    for field in [
        "independent_cross_block_verification_performed",
        "phase_closure_performed",
    ]:
        expect(
            receipt.get(field),
            False,
            "VS0_3_FAIL_BUILD_RECEIPT_CLAIMS_VERIFICATION_ALREADY_PERFORMED",
            object_id="phase_vs0_happy_path_build_receipt_v0",
            path=BUILD_RECEIPT,
            field=field,
            boundary="VS0.2 cannot self-verify or close phase",
        )
    legacy_binding = receipt.get("source_build_commit_sha")
    if legacy_binding is not None and legacy_binding != ORIGINAL_BUILD_COMMIT:
        fail(
            "VS0_3_FAIL_SOURCE_BUILD_BINDING_UNEXPECTED_ORIGINAL_COMMIT",
            object_id="phase_vs0_happy_path_build_receipt_v0",
            path=BUILD_RECEIPT,
            field="source_build_commit_sha",
            expected=ORIGINAL_BUILD_COMMIT,
            actual=legacy_binding,
            boundary="optional legacy original-build binding",
        )
    return receipt, digest, commit


def verify_source_build_binding(
    root: Path, build_receipt_commit: str
) -> dict[str, Any]:
    active_head = run_git(root, ["rev-parse", "HEAD"])
    if active_head != REPAIR_COMMIT:
        fail(
            "VS0_3_FAIL_ACTIVE_ARTIFACT_COMMIT_MISMATCH",
            object_id="phase_vs0_first_specimen_runtime_v0",
            path=OUTPUT_ROOT,
            field="active_artifact_commit_sha",
            expected=REPAIR_COMMIT,
            actual=active_head,
            boundary="active repaired artifact-chain HEAD binding",
        )
    index_commit = run_git(
        root, ["log", "-n", "1", "--format=%H", "--", CHAIN_INDEX]
    )
    if index_commit != REPAIR_COMMIT:
        fail(
            "VS0_3_FAIL_REPAIR_COMMIT_BINDING_UNEXPECTED",
            object_id="phase_vs0_a_to_f_chain_index_v0",
            path=CHAIN_INDEX,
            field="repaired_vs0_2_hash_index_commit_sha",
            expected=REPAIR_COMMIT,
            actual=index_commit,
            boundary="repaired chain-index commit binding",
        )
    if build_receipt_commit != ORIGINAL_BUILD_COMMIT:
        fail(
            "VS0_3_FAIL_SOURCE_BUILD_BINDING_MISSING",
            object_id="phase_vs0_happy_path_build_receipt_v0",
            path=BUILD_RECEIPT,
            field="original_vs0_2_build_commit_sha",
            expected=ORIGINAL_BUILD_COMMIT,
            actual=build_receipt_commit,
            boundary="original VS0.2 build receipt binding",
        )
    return {
        "binding_status": BINDING_STATUS,
        "original_vs0_2_build_commit_sha": ORIGINAL_BUILD_COMMIT,
        "repaired_vs0_2_hash_index_commit_sha": REPAIR_COMMIT,
        "active_artifact_commit_sha": REPAIR_COMMIT,
        "build_receipt_commit_binding_may_remain_original": True,
        "repair_commit_binding_required": True,
        "repair_commit_binding_verified": True,
    }


def verify_chain_index(
    root: Path,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, str]]:
    index, index_digest, _ = load_committed_input(
        root, CHAIN_INDEX, "VS0_3_FAIL_CHAIN_INDEX_MISSING"
    )
    required = {
        "schema_version": "matrixlabs_phase_vs0_a_to_f_chain_index_v0",
        "chain_index_id": "phase_vs0_a_to_f_chain_index_v0",
        "phase_id": "PHASE_VS0",
        "phase_step": "VS0.2",
        "index_role": "BUILD_CHAIN_INDEX_ONLY",
        "run_id": "phase_vs0_first_specimen_runtime_v0",
        "independent_cross_block_verification_performed": False,
        "phase_closure_performed": False,
    }
    for field, wanted in required.items():
        expect(
            index.get(field),
            wanted,
            "VS0_3_FAIL_CHAIN_INDEX_STATUS_MISMATCH",
            object_id="phase_vs0_a_to_f_chain_index_v0",
            path=CHAIN_INDEX,
            field=field,
            boundary="VS0.2 build chain index identity",
        )
    expect(
        index.get("ordered_terminal_chain"),
        EXPECTED_TERMINALS,
        "VS0_3_FAIL_CHAIN_INDEX_ORDER_MISMATCH",
        object_id="phase_vs0_a_to_f_chain_index_v0",
        path=CHAIN_INDEX,
        field="ordered_terminal_chain",
        boundary="A4 to F4 terminal order",
    )
    expect(
        index.get("dependency_edges"),
        EXPECTED_EDGES,
        "VS0_3_FAIL_CHAIN_INDEX_DEPENDENCY_EDGE_MISMATCH",
        object_id="phase_vs0_a_to_f_chain_index_v0",
        path=CHAIN_INDEX,
        field="dependency_edges",
        boundary="A4 to F4 dependency chain",
    )
    records = index.get("artifacts", [])
    expect(
        len(records),
        24,
        "VS0_3_FAIL_PHASE_ARTIFACT_COUNT_MISMATCH",
        object_id="phase_vs0_a_to_f_chain_index_v0",
        path=CHAIN_INDEX,
        field="artifacts",
        boundary="phase artifact count",
    )
    artifacts: dict[str, dict[str, Any]] = {}
    input_hashes = {CHAIN_INDEX: index_digest}
    for record in records:
        relative_path = record.get("path", "")
        if not relative_path.startswith(f"{OUTPUT_ROOT}/"):
            fail(
                "VS0_3_FAIL_CHAIN_INDEX_STATUS_MISMATCH",
                object_id=str(record.get("object_id")),
                path=relative_path,
                field="path",
                expected=f"{OUTPUT_ROOT}/...",
                actual=relative_path,
                boundary="phase verification target namespace",
            )
        value, digest, _ = load_committed_input(
            root, relative_path, "VS0_3_FAIL_PHASE_ARTIFACT_COUNT_MISMATCH"
        )
        expect(
            digest,
            record.get("sha256"),
            "VS0_3_FAIL_CHAIN_INDEX_HASH_MISMATCH",
            object_id=str(record.get("object_id")),
            path=relative_path,
            field="sha256",
            boundary="indexed artifact hash stability",
        )
        expect(
            value.get("object_id"),
            record.get("object_id"),
            "VS0_3_FAIL_CHAIN_INDEX_STATUS_MISMATCH",
            object_id=str(record.get("object_id")),
            path=relative_path,
            field="object_id",
            boundary="declared phase artifact identity",
        )
        key = str(record.get("sequence_key"))
        artifacts[key] = value
        input_hashes[relative_path] = digest
    expect(
        len(artifacts),
        24,
        "VS0_3_FAIL_PHASE_ARTIFACT_COUNT_MISMATCH",
        object_id="phase_vs0_a_to_f_chain_index_v0",
        path=CHAIN_INDEX,
        field="unique sequence keys",
        boundary="phase artifact index uniqueness",
    )
    return index, artifacts, input_hashes


def verify_terminal_closures(
    root: Path, artifacts: dict[str, dict[str, Any]]
) -> tuple[dict[str, bool], dict[str, str]]:
    presence: dict[str, bool] = {}
    for key in EXPECTED_TERMINALS:
        relative_path = f"{OUTPUT_ROOT}/{TERMINAL_FILES[key]}"
        present = (root / relative_path).is_file() and key in artifacts
        presence[key] = present
        if not present:
            fail(
                f"VS0_3_FAIL_{key}_MISSING",
                object_id=key,
                path=relative_path,
                field="present",
                expected=True,
                actual=False,
                boundary="terminal closure presence",
            )

    anchor_checks = {
        "A4": [
            "A_CHAIN_BUILD_PASS_AUTHORITY_ACCEPTED_AS_BASIS_ONLY",
            "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        ],
        "B3": [
            "B_CHAIN_BUILD_PASS_READ_ONLY_ROUTE_CLASSIFIED",
            "ROUTE_MACHINE_MAY_PREPARE_ONLY",
        ],
        "C3": ["CANDIDATE_AUDIT_PASS_WELL_FORMED_NOT_PROMOTED"],
        "D5": ["MACHINE_PROCEED_CLOSURE_PASS_RADIUS_EXHAUSTED_STOP"],
        "E4": ["COMPRESSION_CLOSURE_PASS_OBSERVABILITY_ONLY"],
        "F4": ["REGISTRY_CANDIDATE_CLOSURE_PASS_CANDIDATE_ONLY"],
    }
    for key, anchors in anchor_checks.items():
        for anchor in anchors:
            if not contains_scalar(artifacts[key], anchor):
                fail(
                    "VS0_3_FAIL_TERMINAL_CLOSURE_STATUS_MISMATCH",
                    object_id=key,
                    path=f"{OUTPUT_ROOT}/{TERMINAL_FILES[key]}",
                    field="terminal status anchor",
                    expected=anchor,
                    actual="absent",
                    boundary="terminal closure status",
                )
    return presence, TERMINAL_STATUSES


def verify_source_chain_order(
    artifacts: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    checks = {
        "b3_references_a4": artifacts["B1"]["dependency"]["upstream_object_key"] == "A4",
        "c3_references_b3": artifacts["C1"]["dependency"]["upstream_object_key"] == "B3",
        "d5_references_c3": artifacts["D1"]["dependency"]["upstream_object_key"] == "C3",
        "e4_references_d5": artifacts["E1"]["dependency"]["upstream_object_key"] == "D5",
        "f4_references_e4": artifacts["F1"]["dependency"]["upstream_object_key"] == "E4",
    }
    codes = {
        "b3_references_a4": "VS0_3_FAIL_B3_DOES_NOT_REFERENCE_A4",
        "c3_references_b3": "VS0_3_FAIL_C3_DOES_NOT_REFERENCE_B3",
        "d5_references_c3": "VS0_3_FAIL_D5_DOES_NOT_REFERENCE_C3",
        "e4_references_d5": "VS0_3_FAIL_E4_DOES_NOT_REFERENCE_D5",
        "f4_references_e4": "VS0_3_FAIL_F4_DOES_NOT_REFERENCE_E4",
    }
    for field, passed in checks.items():
        if not passed:
            fail(
                codes[field],
                object_id=field,
                field="segment entry dependency",
                expected=True,
                actual=False,
                boundary="cross-segment source-chain order",
            )
    return {"source_chain_order_status": "SOURCE_CHAIN_ORDER_PASS", **checks}


def require_anchor(
    artifact: dict[str, Any],
    key: str,
    anchor: object,
    code: str,
    boundary: str,
) -> None:
    if not contains_scalar(artifact, anchor):
        fail(
            code,
            object_id=key,
            path=f"{OUTPUT_ROOT}/{key.lower()}...",
            field="semantic anchor",
            expected=anchor,
            actual="absent",
            boundary=boundary,
        )


def verify_cross_block_parity(
    artifacts: dict[str, dict[str, Any]]
) -> dict[str, str]:
    require_anchor(
        artifacts["A2"],
        "A2",
        "DECISION_ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        "VS0_3_FAIL_AUTHORITY_STATE_PARITY_MISMATCH",
        "human decision parity",
    )
    for key in ["A3", "A4"]:
        require_anchor(
            artifacts[key],
            key,
            "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
            "VS0_3_FAIL_AUTHORITY_STATE_PARITY_MISMATCH",
            "accepted-basis authority state",
        )

    for key in ["B1", "D4"]:
        require_anchor(
            artifacts[key],
            key,
            "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
            "VS0_3_FAIL_REQUESTED_ACTION_PARITY_MISMATCH",
            "requested action parity",
        )
    require_anchor(
        artifacts["B2"],
        "B2",
        "ROUTE_MACHINE_MAY_PREPARE_ONLY",
        "VS0_3_FAIL_REQUESTED_ACTION_PARITY_MISMATCH",
        "route classification parity",
    )

    for key in ["B1", "D4"]:
        require_anchor(
            artifacts[key],
            key,
            "PREPARE_SURFACE_ONLY",
            "VS0_3_FAIL_SCOPE_PARITY_MISMATCH",
            "preparation-only scope",
        )
    require_anchor(
        artifacts["D4_OUTPUT"],
        "D4_OUTPUT",
        "C8_N22_BASIS_ONLY",
        "VS0_3_FAIL_SCOPE_PARITY_MISMATCH",
        "C8 n22 basis scope",
    )

    require_anchor(
        artifacts["C2"],
        "C2",
        "ARCHIVE_STATUS_CANDIDATE",
        "VS0_3_FAIL_CANDIDATE_STATUS_STRENGTHENED",
        "candidate status before promotion",
    )
    for anchor in [
        "CANDIDATE_AUDIT_PASS_WELL_FORMED_NOT_PROMOTED",
        False,
    ]:
        require_anchor(
            artifacts["C3"],
            "C3",
            anchor,
            "VS0_3_FAIL_C3_NOT_PROMOTED_BOUNDARY_DROPPED",
            "C3 candidate remains not promoted",
        )

    require_anchor(
        artifacts["D2"],
        "D2",
        "DECISION_PROMOTE_CANDIDATE_FOR_DECLARED_SCOPE",
        "VS0_3_FAIL_PROMOTION_DECISION_MISSING",
        "declared-scope promotion decision",
    )
    for anchor in [
        "ARCHIVE_STATUS_PREAPPROVED_ACTIVE",
        "PROMOTION_GRANTED_FOR_DECLARED_SCOPE",
        "USE_GRANTED_FOR_DECLARED_SCOPE_ONLY",
        "ACTIVE_ARCHIVE_ENTRY_ACTIVE",
    ]:
        require_anchor(
            artifacts["D3"],
            "D3",
            anchor,
            "VS0_3_FAIL_ACTIVE_ARCHIVE_ENTRY_SCOPE_MISMATCH",
            "active archive entry declared scope",
        )

    d4 = artifacts["D4"]["payload"]
    expect(
        d4.get("machine_action_count"),
        1,
        "VS0_3_FAIL_MACHINE_ACTION_MISMATCH",
        object_id="D4",
        path=f"{OUTPUT_ROOT}/d4_machine_proceed_v0.json",
        field="machine_action_count",
        boundary="single D4 preparation action",
    )
    expect(
        d4.get("machine_preparation_action_performed"),
        True,
        "VS0_3_FAIL_MACHINE_ACTION_MISMATCH",
        object_id="D4",
        path=f"{OUTPUT_ROOT}/d4_machine_proceed_v0.json",
        field="machine_preparation_action_performed",
        boundary="single D4 preparation action",
    )
    for key in ["D4", "D5"]:
        for field in ["unit_executed", "runtime_executed"]:
            values = find_key_values(artifacts[key], field)
            if any(value is True for value in values):
                fail(
                    "VS0_3_FAIL_UNIT_EXECUTED"
                    if field == "unit_executed"
                    else "VS0_3_FAIL_RUNTIME_EXECUTED",
                    object_id=key,
                    field=field,
                    expected=False,
                    actual=True,
                    boundary="preparation action is not execution",
                )

    radius_expectations = {
        "D3": [1],
        "D4": [1, 0],
        "D5": [0, True],
        "E1": [0],
        "E4": [0],
        "F4": [0],
    }
    for key, anchors in radius_expectations.items():
        for anchor in anchors:
            require_anchor(
                artifacts[key],
                key,
                anchor,
                "VS0_3_FAIL_RADIUS_NOT_EXHAUSTED",
                "radius exhaustion parity",
            )
    expect(
        d4.get("radius_consumed"),
        1,
        "VS0_3_FAIL_RADIUS_NOT_CONSUMED",
        object_id="D4",
        path=f"{OUTPUT_ROOT}/d4_machine_proceed_v0.json",
        field="radius_consumed",
        boundary="single-use radius consumption",
    )

    for key in ["E1", "E2"]:
        require_anchor(
            artifacts[key],
            key,
            "C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0",
            "VS0_3_FAIL_COMPRESSION_TRACE_LABEL_MISMATCH",
            "compression trace label parity",
        )
    require_anchor(
        artifacts["E3"],
        "E3",
        "DECOMPRESSION_AUDIT_PASS_CRITICAL_FIELD_PARITY",
        "VS0_3_FAIL_DECOMPRESSION_AUDIT_NOT_PASS",
        "decompression parity",
    )
    for anchor in [
        "COMPRESSION_CLOSURE_PASS_OBSERVABILITY_ONLY",
        "OBSERVABILITY_SHORTCUT_ONLY",
        True,
    ]:
        require_anchor(
            artifacts["E4"],
            "E4",
            anchor,
            "VS0_3_FAIL_COMPRESSION_REPLACED_SOURCE_AUTHORITY",
            "observability-only compression boundary",
        )
    for key in ["E1", "E2", "E3", "E4"]:
        for field in [
            "compressed_packet_may_replace_source_authority",
            "compressed_packet_may_authorize_reuse",
            "compressed_packet_may_renew_radius",
            "compressed_packet_may_create_runner_authority",
        ]:
            expect(
                artifacts[key]["non_effects"].get(field),
                False,
                "VS0_3_FAIL_COMPRESSION_REPLACED_SOURCE_AUTHORITY",
                object_id=key,
                path=f"{OUTPUT_ROOT}/{key.lower()}...",
                field=field,
                boundary="compression non-effects",
            )

    for key in ["F2", "F4"]:
        require_anchor(
            artifacts[key],
            key,
            "REGISTRY_STATUS_CANDIDATE",
            "VS0_3_FAIL_REGISTRY_STATUS_NOT_CANDIDATE",
            "registry candidate status",
        )
        require_anchor(
            artifacts[key],
            key,
            1,
            "VS0_3_FAIL_SPECIMEN_COUNT_MISMATCH",
            "single local specimen",
        )
        require_anchor(
            artifacts[key],
            key,
            "SINGLE_LOCAL_SPECIMEN",
            "VS0_3_FAIL_SPECIMEN_COUNT_MISMATCH",
            "single local specimen",
        )
        require_anchor(
            artifacts[key],
            key,
            "LOCAL_SPECIMEN_ONLY_NOT_GENERALIZED",
            "VS0_3_FAIL_GENERALIZATION_CLAIMED",
            "local-only generalization boundary",
        )
    require_anchor(
        artifacts["F2"],
        "F2",
        "C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0",
        "VS0_3_FAIL_REGISTRY_TRACE_LABEL_MISMATCH",
        "registry trace label parity",
    )

    return {
        "authority_state_parity": "AUTHORITY_STATE_PARITY_PASS",
        "requested_action_parity": "REQUESTED_ACTION_PARITY_PASS",
        "scope_parity": "SCOPE_PARITY_PASS",
        "candidate_status_parity": "CANDIDATE_STATUS_PARITY_PASS",
        "promotion_active_archive_entry_parity": "PROMOTION_ACTIVE_ARCHIVE_ENTRY_PARITY_PASS",
        "machine_action_parity": "MACHINE_ACTION_PARITY_PASS",
        "radius_parity": "RADIUS_PARITY_PASS_EXHAUSTED",
        "compression_parity": "COMPRESSION_PARITY_PASS_OBSERVABILITY_ONLY",
        "registry_candidate_parity": "REGISTRY_CANDIDATE_PARITY_PASS_CANDIDATE_ONLY",
    }


def verify_global_forbidden_effects(
    artifacts: dict[str, dict[str, Any]], build_receipt: dict[str, Any]
) -> dict[str, bool]:
    forbidden = {
        "active_registry_entry_created": "VS0_3_FAIL_ACTIVE_REGISTRY_CREATED",
        "registry_entry_activated": "VS0_3_FAIL_REGISTRY_ACTIVATED",
        "trace_generalized": "VS0_3_FAIL_TRACE_GENERALIZED",
        "generalization_claimed": "VS0_3_FAIL_GENERALIZATION_CLAIMED",
        "declared_scope_use_expanded": "VS0_3_FAIL_DECLARED_SCOPE_USE_EXPANDED",
        "declared_scope_expanded": "VS0_3_FAIL_DECLARED_SCOPE_USE_EXPANDED",
        "radius_renewed_after_d5": "VS0_3_FAIL_RADIUS_RENEWED_AFTER_D5",
        "radius_renewed": "VS0_3_FAIL_RADIUS_RENEWED_AFTER_D5",
        "additional_machine_proceed_authorized": "VS0_3_FAIL_ADDITIONAL_MACHINE_PROCEED_AUTHORIZED",
        "next_unit_executed": "VS0_3_FAIL_NEXT_UNIT_EXECUTED",
        "unit_executed": "VS0_3_FAIL_UNIT_EXECUTED",
        "runtime_executed": "VS0_3_FAIL_RUNTIME_EXECUTED",
        "source_authority_replaced_by_compression": "VS0_3_FAIL_SOURCE_AUTHORITY_REPLACED_BY_COMPRESSION",
        "phase_projection_replaces_source_authority": "VS0_3_FAIL_SOURCE_AUTHORITY_REPLACED_BY_COMPRESSION",
        "runner_authority_created": "VS0_3_FAIL_RUNNER_AUTHORITY_CREATED",
        "discussion_packets_committed": "VS0_3_FAIL_DISCUSSION_PACKETS_IN_SCOPE",
    }
    values_to_scan = [*artifacts.values(), build_receipt]
    for field, code in forbidden.items():
        for value in values_to_scan:
            if any(item is True for item in find_key_values(value, field)):
                fail(
                    code,
                    field=field,
                    expected=False,
                    actual=True,
                    boundary="global forbidden-effect verification",
                )
    return {
        "active_registry_created": False,
        "trace_generalized": False,
        "declared_scope_use_expanded": False,
        "radius_renewed_after_d5": False,
        "additional_machine_proceed_authorized": False,
        "next_unit_executed": False,
        "runtime_executed": False,
        "source_authority_replaced_by_compression": False,
        "runner_authority_created": False,
        "discussion_packets_committed": False,
    }


def build_verification_receipt(
    build_receipt_digest: str,
    source_build_binding: dict[str, Any],
    index: dict[str, Any],
    presence: dict[str, bool],
    statuses: dict[str, str],
    order: dict[str, Any],
    parity: dict[str, str],
    global_effects: dict[str, bool],
    input_hashes: dict[str, str],
) -> dict[str, Any]:
    self_non_effects = {
        "vs0_3_built_new_a_to_f_artifacts": False,
        "vs0_3_repaired_a_to_f_artifacts": False,
        "vs0_3_reran_vs0_2_builder": False,
        "vs0_3_ran_negative_probes": False,
        "vs0_3_closed_phase": False,
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "verification_id": VERIFICATION_ID,
        "phase_id": "PHASE_VS0",
        "phase_step": "VS0.3",
        "verification_role": "HAPPY_PATH_A_TO_F_PHASE_SPECIMEN_CLOSURE_VERIFICATION_ONLY",
        "generated_by": VERIFIER,
        "source_build_receipt": {
            "build_receipt_id": "phase_vs0_happy_path_build_receipt_v0",
            "build_receipt_path": BUILD_RECEIPT,
            "legacy_source_build_commit_sha": ORIGINAL_BUILD_COMMIT,
            "original_vs0_2_build_commit_sha": ORIGINAL_BUILD_COMMIT,
            "repaired_vs0_2_hash_index_commit_sha": REPAIR_COMMIT,
            "active_artifact_commit_sha": REPAIR_COMMIT,
            "source_build_receipt_sha256": build_receipt_digest,
            "build_gate": BUILD_STATUS,
            "independent_cross_block_verification_performed_by_vs0_2": False,
        },
        "source_build_binding": source_build_binding,
        "verification_target_namespace": {
            "run_id": "phase_vs0_first_specimen_runtime_v0",
            "a_to_f_output_root": OUTPUT_ROOT,
            "canonical_source_chain_may_be_read": False,
            "canonical_source_chain_may_be_mutated": False,
            "phase_run_artifacts_may_be_read": True,
            "phase_run_artifacts_may_be_mutated": False,
        },
        "field_reading_policy": {
            "explicit_paths_preferred": True,
            "declared_object_id_required": True,
            "semantic_anchor_search_allowed_for_phase_specimen_fields": True,
            "latest_file_resolution_allowed": False,
            "mtime_resolution_allowed": False,
            "directory_scan_meaning_allowed": False,
        },
        "read_only_verification_boundary": {
            "vs0_2_artifacts_modified_by_vs0_3": False,
            "a_to_f_phase_artifacts_modified_by_vs0_3": False,
            "canonical_source_chain_modified_by_vs0_3": False,
            "builder_rerun_by_vs0_3": False,
            "repair_performed_by_vs0_3": False,
            "negative_probes_run_by_vs0_3": False,
            "phase_closure_performed_by_vs0_3": False,
            "input_hash_snapshot_before_after_match": True,
        },
        "input_hash_snapshot": {
            "hash_algorithm": "sha256",
            "inputs": input_hashes,
        },
        "chain_index_hash_verification": {
            "chain_index_status": "CHAIN_INDEX_HASH_VERIFICATION_PASS",
            "chain_index_id": "phase_vs0_a_to_f_chain_index_v0",
            "ordered_terminal_chain": EXPECTED_TERMINALS,
            "dependency_edges_verified": True,
            "phase_artifact_json_count": len(index["artifacts"]),
            "all_indexed_artifact_hashes_match_current_file_content": True,
        },
        "terminal_closure_presence": presence,
        "terminal_closure_statuses": statuses,
        "terminal_closure_presence_pass": True,
        "source_chain_order": order,
        "cross_block_parity": parity,
        "global_forbidden_effects": global_effects,
        "vs0_3_self_non_effects": self_non_effects,
        "verification_result": {
            "happy_path_verification_status": PASS_STATUS,
            "a_to_f_chain_verified_under_declared_gates": True,
            "semantic_leak_detected": False,
            "authority_smuggling_detected": False,
            "failures": [],
        },
        "evidence_yield_class": {
            "yield_branch": "CONFIRMATION_YIELD",
            "reason": "successful verification confirmed the built happy-path phase specimen preserved declared boundaries",
        },
        "next_required_object": "phase_vs0_negative_probe_battery_v0",
        "terminal_transition": TERMINAL_TRANSITION,
        "precommit_phase_vs0_happy_path_verification_gate": "PASS",
        "happy_path_verification_gate": PASS_STATUS,
        "build_receipt_present": True,
        "build_receipt_status": BUILD_STATUS,
        "original_vs0_2_build_commit_sha": ORIGINAL_BUILD_COMMIT,
        "repaired_vs0_2_hash_index_commit_sha": REPAIR_COMMIT,
        "active_artifact_commit_sha": REPAIR_COMMIT,
        "chain_index_present": True,
        "chain_index_hash_verification_status": "CHAIN_INDEX_HASH_VERIFICATION_PASS",
        "phase_artifact_json_count": len(index["artifacts"]),
        "all_indexed_artifact_hashes_match_current_file_content": True,
        "a4_present": True,
        "b3_present": True,
        "c3_present": True,
        "d5_present": True,
        "e4_present": True,
        "f4_present": True,
        "a4_status": statuses["A4"],
        "b3_status": statuses["B3"],
        "c3_status": statuses["C3"],
        "d5_status": statuses["D5"],
        "e4_status": statuses["E4"],
        "f4_status": statuses["F4"],
        "source_chain_order_pass": True,
        **parity,
        "d5_radius_after": 0,
        "d5_radius_exhausted": True,
        **global_effects,
        **self_non_effects,
        "evidence_yield_branch": "CONFIRMATION_YIELD",
        "commit_created": False,
        "push_executed": False,
        "failures": [],
        "failure_vocabulary": FAILURE_CODES,
    }


def render_markdown() -> str:
    return f"""# Phase VS0 happy-path verification v0

## Status

{PASS_STATUS}

## Evidence Yield

CONFIRMATION_YIELD

## Verified build receipt

phase_vs0_happy_path_build_receipt_v0

## Source build binding

- original VS0.2 build commit: {ORIGINAL_BUILD_COMMIT}
- repaired VS0.2 hash/index commit: {REPAIR_COMMIT}
- active artifact commit: {REPAIR_COMMIT}
- binding status: {BINDING_STATUS}

## Verified namespace

{OUTPUT_ROOT}

## Chain index and hashes

- chain index: PASS
- phase artifact JSON count: 24
- indexed artifact hashes: PASS

## Terminal closures

- A4 authority transition closure: PASS
- B3 read-only router closure: PASS
- C3 candidate archive audit: PASS
- D5 machine proceed closure: PASS
- E4 compression closure: PASS
- F4 registry candidate closure projection: PASS

## Cross-block parity

- authority state parity: PASS
- requested action parity: PASS
- scope parity: PASS
- candidate status parity: PASS
- promotion and active archive entry parity: PASS
- machine action parity: PASS
- radius parity: PASS, exhausted
- compression parity: PASS, observability-only
- registry candidate parity: PASS, candidate-only

## Global forbidden effects

- no active registry created
- no trace generalization claimed
- no declared scope expansion
- no radius renewed after D5
- no additional machine proceed authorized
- no next unit executed
- no runtime executed
- no source authority replaced by compression
- no runner authority created

## VS0.3 read-only boundary

- no A\u2192F artifacts built by VS0.3
- no A\u2192F artifacts repaired by VS0.3
- no VS0.2 builder rerun by VS0.3
- no negative probes run by VS0.3
- no phase closure performed by VS0.3

## Next required object

phase_vs0_negative_probe_battery_v0

## Terminal transition

{TERMINAL_TRANSITION}

## Non-claim

VS0.3 verifies the happy path only. It does not run negative probes or close Phase VS0."""


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_diagnostic(root: Path, exc: VerificationFailure) -> None:
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "verification_id": VERIFICATION_ID,
        "phase_id": "PHASE_VS0",
        "phase_step": "VS0.3",
        "verification_result": {
            "happy_path_verification_status": exc.code,
            "a_to_f_chain_verified_under_declared_gates": False,
            "semantic_leak_detected": "LEAK" in exc.code
            or any(token in exc.code for token in ["RADIUS", "REGISTRY", "GENERALIZATION", "RUNNER"]),
            "authority_smuggling_detected": "AUTHORITY" in exc.code,
            "failures": [exc.code],
        },
        "diagnostic": {
            "yield_branch": "DIAGNOSTIC_YIELD",
            "violating_object": exc.object_id,
            "violating_path": exc.path,
            "violating_field": exc.field,
            "expected_value": exc.expected,
            "actual_value": exc.actual,
            "source_boundary": exc.boundary,
            "next_lawful_surface": exc.next_surface,
            "self_repair_performed": False,
        },
        "read_only_verification_boundary": {
            "vs0_2_artifacts_modified_by_vs0_3": False,
            "a_to_f_phase_artifacts_modified_by_vs0_3": False,
            "canonical_source_chain_modified_by_vs0_3": False,
            "builder_rerun_by_vs0_3": False,
            "repair_performed_by_vs0_3": False,
            "negative_probes_run_by_vs0_3": False,
            "phase_closure_performed_by_vs0_3": False,
        },
        "evidence_yield_class": {"yield_branch": "DIAGNOSTIC_YIELD"},
        "precommit_phase_vs0_happy_path_verification_gate": "PASS",
        "happy_path_verification_gate": exc.code,
        "commit_created": False,
        "push_executed": False,
        "terminal_transition": f"STOP({exc.code})",
    }
    write_json(root / OUTPUT_JSON, receipt)
    write_text(
        root / OUTPUT_MD,
        f"# Phase VS0 happy-path verification v0\n\n"
        f"## Status\n\n{exc.code}\n\n"
        f"## Evidence Yield\n\nDIAGNOSTIC_YIELD\n\n"
        f"## Non-claim\n\nNo repair was performed.",
    )


def verify() -> int:
    root = detect_repo_root(Path.cwd())
    validate_dirty_scope(root)
    _, preflight_digest, _ = load_committed_input(
        root, PREFLIGHT, "VS0_3_STOP_HAPPY_PATH_BUILD_NOT_PASS"
    )
    source_build_receipt, build_receipt_digest, build_receipt_commit = (
        verify_build_receipt(root)
    )
    source_build_binding = verify_source_build_binding(root, build_receipt_commit)
    index, artifacts, input_hashes = verify_chain_index(root)
    input_hashes[PREFLIGHT] = preflight_digest
    input_hashes[BUILD_RECEIPT] = build_receipt_digest
    presence, statuses = verify_terminal_closures(root, artifacts)
    order = verify_source_chain_order(artifacts)
    parity = verify_cross_block_parity(artifacts)
    global_effects = verify_global_forbidden_effects(artifacts, source_build_receipt)

    input_hashes_after = {
        relative_path: sha256(root / relative_path)
        for relative_path in input_hashes
    }
    if input_hashes_after != input_hashes:
        fail(
            "VS0_3_FAIL_VS0_3_MUTATED_PHASE_ARTIFACTS",
            field="input_hash_snapshot",
            expected=input_hashes,
            actual=input_hashes_after,
            boundary="VS0.3 read-only before/after snapshot",
        )

    receipt = build_verification_receipt(
        build_receipt_digest,
        source_build_binding,
        index,
        presence,
        statuses,
        order,
        parity,
        global_effects,
        input_hashes,
    )
    write_json(root / OUTPUT_JSON, receipt)
    write_text(root / OUTPUT_MD, render_markdown())
    print(f"Wrote {OUTPUT_JSON}")
    print(f"Wrote {OUTPUT_MD}")
    print(f"happy_path_verification_gate={PASS_STATUS}")
    print(f"terminal_transition={TERMINAL_TRANSITION}")
    return 0


def main() -> int:
    root: Path | None = None
    try:
        root = detect_repo_root(Path.cwd())
        return verify()
    except VerificationFailure as exc:
        if root is not None:
            write_diagnostic(root, exc)
        print(f"STOP({exc.code}): {exc.field or exc.path or exc.code}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
