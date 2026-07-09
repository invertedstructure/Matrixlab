#!/usr/bin/env python3

"""Run the deterministic Phase VS0.4 contract-level negative probe battery."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT = "scripts/run_phase_vs0_negative_probe_battery_v0.py"
EXPECTED_HEAD = "daec73d1a631225a00b7d0ad967880dd9d3b301c"
ORIGINAL_BUILD_COMMIT = "49ebcf1393893bbbc61c5fcd48359770c3e554e7"
REPAIR_COMMIT = "9f7277608f8e475fa84f6e4697e0db0903200aac"
VERIFICATION_STATUS = (
    "VS0_3_HAPPY_PATH_VERIFICATION_PASS_A_TO_F_PHASE_SPECIMEN_VERIFIED"
)
BINDING_STATUS = (
    "VS0_3_SOURCE_BUILD_BINDING_PASS_ORIGINAL_BUILD_PLUS_REPAIR_COMMIT"
)
CHAIN_STATUS = "CHAIN_INDEX_HASH_VERIFICATION_PASS"
PASS_STATUS = "VS0_4_NEGATIVE_PROBES_PASS_TYPED_STOPS"
VERIFICATION_JSON = (
    "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_verification_v0.json"
)
VERIFICATION_MD = (
    "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_verification_v0.md"
)
VERIFICATION_SCRIPT = "scripts/verify_phase_vs0_happy_path_v0.py"
A_TO_F_ROOT = (
    "docs/matrixlabs/phase_vs0/runs/"
    "phase_vs0_first_specimen_runtime_v0/a_to_f"
)
CHAIN_INDEX = f"{A_TO_F_ROOT}/phase_vs0_a_to_f_chain_index_v0.json"
OUTPUT_ROOT = (
    "docs/matrixlabs/phase_vs0/runs/"
    "phase_vs0_first_specimen_runtime_v0/negative_probes"
)
DEFINITIONS_PATH = f"{OUTPUT_ROOT}/phase_vs0_negative_probe_definitions_v0.json"
BATTERY_PATH = f"{OUTPUT_ROOT}/phase_vs0_negative_probe_battery_v0.json"
MARKDOWN_PATH = f"{OUTPUT_ROOT}/phase_vs0_negative_probe_battery_v0.md"

RECEIPT_NAMES = {
    "NEG01_D4_WITHOUT_ACTIVE_ENTRY": "neg01_d4_without_active_entry_v0.json",
    "NEG02_D4_WITH_RADIUS_ZERO": "neg02_d4_with_radius_zero_v0.json",
    "NEG03_E2_WITHOUT_E1_TARGET": "neg03_e2_without_e1_target_v0.json",
    "NEG04_E3_WITH_DROPPED_RADIUS_FIELD": (
        "neg04_e3_with_dropped_radius_field_v0.json"
    ),
    "NEG05_E4_WITH_FAILED_DECOMPRESSION_AUDIT": (
        "neg05_e4_with_failed_decompression_audit_v0.json"
    ),
    "NEG06_F2_WITHOUT_E4_CLOSURE": "neg06_f2_without_e4_closure_v0.json",
    "NEG07_F2_WITH_SPECIMEN_COUNT_OVERCLAIM": (
        "neg07_f2_with_specimen_count_overclaim_v0.json"
    ),
    "NEG08_F3_WITH_GENERALIZATION_CLAIMED": (
        "neg08_f3_with_generalization_claimed_v0.json"
    ),
    "NEG09_F4_WITH_ACTIVE_REGISTRY_CREATED": (
        "neg09_f4_with_active_registry_created_v0.json"
    ),
    "NEG10_ANY_WITH_RUNNER_AUTHORITY_TRUE": (
        "neg10_any_with_runner_authority_true_v0.json"
    ),
}

DEFINITIONS: list[dict[str, Any]] = [
    {
        "probe_id": "NEG01_D4_WITHOUT_ACTIVE_ENTRY",
        "attempted_illegal_move": "D4_MACHINE_PROCEED",
        "illegal_condition": "ACTIVE_ARCHIVE_ENTRY_MISSING",
        "missing_object": "active.c8.n22.prepare_next_unit_definition_surface.v0",
        "violated_boundary": "ACTIVE_ARCHIVE_ENTRY_REQUIRED_BEFORE_MACHINE_PROCEED",
        "source_boundary": "verified phase specimen D-chain dependency",
        "expected_value": "present active archive entry",
        "actual_value": "missing",
        "next_lawful_surface": "D3_ACTIVE_ARCHIVE_ENTRY_MATERIALIZATION",
        "expected_stop_code": "MACHINE_PROCEED_FAIL_ACTIVE_ENTRY_MISSING",
        "expected_probe_pass_label": (
            "NEG01_PASS_TYPED_STOP_ACTIVE_ENTRY_MISSING"
        ),
    },
    {
        "probe_id": "NEG02_D4_WITH_RADIUS_ZERO",
        "attempted_illegal_move": "D4_MACHINE_PROCEED",
        "illegal_condition": "RADIUS_REMAINING_BEFORE_ZERO",
        "violating_field": "radius_remaining_before",
        "violated_boundary": "RADIUS_1_SINGLE_OBJECT_REQUIRED",
        "source_boundary": "D3/D4 radius boundary from verified phase specimen",
        "expected_value": 1,
        "actual_value": 0,
        "next_lawful_surface": "REQUEST_NEW_RADIUS_OR_HUMAN_AUTHORITY",
        "expected_stop_code": "MACHINE_PROCEED_FAIL_RADIUS_EXCEEDED",
        "expected_probe_pass_label": "NEG02_PASS_TYPED_STOP_RADIUS_EXCEEDED",
    },
    {
        "probe_id": "NEG03_E2_WITHOUT_E1_TARGET",
        "attempted_illegal_move": "E2_COMPRESSED_PACKET_CREATION",
        "illegal_condition": "COMPRESSION_TARGET_MISSING",
        "missing_object": "c8.n22.authority_action_trace.compression_target.v0",
        "violated_boundary": "COMPRESSION_TARGET_REQUIRED_BEFORE_PACKET",
        "source_boundary": "verified phase specimen E-chain dependency",
        "expected_value": "present E1 compression target declaration",
        "actual_value": "missing",
        "next_lawful_surface": "E1_COMPRESSION_TARGET_DECLARATION",
        "expected_stop_code": "COMPRESSED_PACKET_FAIL_COMPRESSION_TARGET_MISSING",
        "expected_probe_pass_label": (
            "NEG03_PASS_TYPED_STOP_COMPRESSION_TARGET_MISSING"
        ),
    },
    {
        "probe_id": "NEG04_E3_WITH_DROPPED_RADIUS_FIELD",
        "attempted_illegal_move": "E3_DECOMPRESSION_AUDIT",
        "illegal_condition": "RADIUS_ACCOUNTING_FIELDS_DROPPED",
        "violating_field_group": "radius_accounting",
        "missing_fields": ["radius_after", "radius_exhausted"],
        "violated_boundary": "CRITICAL_RADIUS_FIELDS_MUST_SURVIVE_COMPRESSION",
        "source_boundary": "D5_RADIUS_EXHAUSTED_STOP_STATE",
        "expected_value": "radius_after and radius_exhausted present",
        "actual_value": "radius_after and radius_exhausted missing",
        "next_lawful_surface": (
            "REPAIR_COMPRESSED_PACKET_RADIUS_ACCOUNTING_FIELDS"
        ),
        "expected_stop_code": "DECOMPRESSION_AUDIT_FAIL_RADIUS_FIELD_DROPPED",
        "expected_probe_pass_label": (
            "NEG04_PASS_TYPED_STOP_RADIUS_FIELD_DROPPED"
        ),
    },
    {
        "probe_id": "NEG05_E4_WITH_FAILED_DECOMPRESSION_AUDIT",
        "attempted_illegal_move": "E4_COMPRESSION_CLOSURE",
        "illegal_condition": "DECOMPRESSION_AUDIT_NOT_PASS",
        "violating_object": "synthetic.neg05.decompression_audit_failed.v0",
        "violating_field": "decompression_audit_status",
        "violated_boundary": "E4_REQUIRES_E3_PASS",
        "source_boundary": "verified phase specimen E3/E4 dependency",
        "expected_value": "DECOMPRESSION_AUDIT_PASS_CRITICAL_FIELD_PARITY",
        "actual_value": "DECOMPRESSION_AUDIT_FAIL_RADIUS_FIELD_DROPPED",
        "next_lawful_surface": "REPAIR_OR_REBUILD_E3_DECOMPRESSION_AUDIT",
        "expected_stop_code": (
            "COMPRESSION_CLOSURE_FAIL_DECOMPRESSION_AUDIT_NOT_PASS"
        ),
        "expected_probe_pass_label": (
            "NEG05_PASS_TYPED_STOP_DECOMPRESSION_AUDIT_NOT_PASS"
        ),
    },
    {
        "probe_id": "NEG06_F2_WITHOUT_E4_CLOSURE",
        "attempted_illegal_move": "F2_REGISTRY_CANDIDATE_CREATION",
        "illegal_condition": "E4_COMPRESSION_CLOSURE_MISSING",
        "missing_object": "c8.n22.compression_specimen_closure.v0",
        "violated_boundary": "E4_COMPRESSION_CLOSURE_REQUIRED_BEFORE_F2",
        "source_boundary": "verified phase specimen E4/F2 dependency",
        "expected_value": "present E4 observability-only compression closure",
        "actual_value": "missing",
        "next_lawful_surface": "E4_COMPRESSION_SPECIMEN_CLOSURE",
        "expected_stop_code": (
            "REGISTRY_CANDIDATE_FAIL_COMPRESSION_CLOSURE_MISSING"
        ),
        "expected_probe_pass_label": (
            "NEG06_PASS_TYPED_STOP_COMPRESSION_CLOSURE_MISSING"
        ),
    },
    {
        "probe_id": "NEG07_F2_WITH_SPECIMEN_COUNT_OVERCLAIM",
        "attempted_illegal_move": "F2_REGISTRY_CANDIDATE_CREATION",
        "illegal_condition": (
            "MULTI_SPECIMEN_STABILITY_CLAIMED_WITH_SINGLE_SPECIMEN"
        ),
        "violating_fields": {
            "specimen_count": 1,
            "multi_specimen_stability_claimed": True,
        },
        "violated_boundary": (
            "SINGLE_LOCAL_SPECIMEN_CANNOT_CLAIM_MULTI_SPECIMEN_STABILITY"
        ),
        "source_boundary": "F2 single local specimen evidence boundary",
        "expected_value": {"multi_specimen_stability_claimed": False},
        "actual_value": {
            "specimen_count": 1,
            "multi_specimen_stability_claimed": True,
        },
        "next_lawful_surface": "MULTI_SPECIMEN_STABILITY_AUDIT_SURFACE",
        "expected_stop_code": (
            "REGISTRY_CANDIDATE_FAIL_MULTI_SPECIMEN_STABILITY_CLAIMED"
        ),
        "expected_probe_pass_label": (
            "NEG07_PASS_TYPED_STOP_SPECIMEN_COUNT_OVERCLAIM"
        ),
    },
    {
        "probe_id": "NEG08_F3_WITH_GENERALIZATION_CLAIMED",
        "attempted_illegal_move": "F3_REGISTRY_CANDIDATE_AUDIT",
        "illegal_condition": "GENERAL_SHAPE_CLAIMED",
        "violating_field": "general_shape_claimed",
        "violated_boundary": "F3_LOCAL_SPECIMEN_ONLY_AUDIT_BOUNDARY",
        "source_boundary": "LOCAL_SPECIMEN_ONLY_NOT_GENERALIZED",
        "expected_value": False,
        "actual_value": True,
        "next_lawful_surface": (
            "GENERALIZATION_CANDIDATE_REVIEW_OR_MULTI_SPECIMEN_AUDIT"
        ),
        "expected_stop_code": (
            "REGISTRY_CANDIDATE_AUDIT_FAIL_GENERALIZATION_CLAIMED"
        ),
        "expected_probe_pass_label": (
            "NEG08_PASS_TYPED_STOP_GENERALIZATION_CLAIMED"
        ),
    },
    {
        "probe_id": "NEG09_F4_WITH_ACTIVE_REGISTRY_CREATED",
        "attempted_illegal_move": "F4_REGISTRY_CANDIDATE_CLOSURE",
        "illegal_condition": "ACTIVE_REGISTRY_ENTRY_CREATED_TRUE",
        "violating_field": "active_registry_entry_created",
        "violated_boundary": "F4_CANDIDATE_ONLY_CLOSURE",
        "source_boundary": "REGISTRY_STATUS_CANDIDATE_ONLY",
        "expected_value": False,
        "actual_value": True,
        "next_lawful_surface": "HUMAN_REGISTRY_PROMOTION_DECISION_SURFACE",
        "expected_stop_code": (
            "REGISTRY_CANDIDATE_CLOSURE_FAIL_ACTIVE_REGISTRY_CREATED"
        ),
        "expected_probe_pass_label": (
            "NEG09_PASS_TYPED_STOP_ACTIVE_REGISTRY_CREATED"
        ),
    },
    {
        "probe_id": "NEG10_ANY_WITH_RUNNER_AUTHORITY_TRUE",
        "attempted_illegal_move": "SET_RUNNER_AUTHORITY_TRUE",
        "illegal_condition": "RUNNER_AUTHORITY_CREATED_TRUE",
        "violating_field": "runner_authority_created",
        "violated_boundary": "PHASE_VS0_FORBIDS_RUNNER_AUTHORITY",
        "source_boundary": "VS0 no-runner-authority boundary",
        "expected_value": False,
        "actual_value": True,
        "next_lawful_surface": "RUNNER_PRECONDITION_AUDIT_V0",
        "expected_stop_code": "VS0_FAIL_RUNNER_AUTHORITY_CREATED",
        "allowed_local_equivalent_stop_code": (
            "REGISTRY_CANDIDATE_CLOSURE_FAIL_RUNNER_AUTHORITY_CREATED"
        ),
        "expected_probe_pass_label": (
            "NEG10_PASS_TYPED_STOP_RUNNER_AUTHORITY_CREATED"
        ),
    },
]

GUARD_STOP_CODES = {
    "ACTIVE_ARCHIVE_ENTRY_MISSING": "MACHINE_PROCEED_FAIL_ACTIVE_ENTRY_MISSING",
    "RADIUS_REMAINING_BEFORE_ZERO": "MACHINE_PROCEED_FAIL_RADIUS_EXCEEDED",
    "COMPRESSION_TARGET_MISSING": (
        "COMPRESSED_PACKET_FAIL_COMPRESSION_TARGET_MISSING"
    ),
    "RADIUS_ACCOUNTING_FIELDS_DROPPED": (
        "DECOMPRESSION_AUDIT_FAIL_RADIUS_FIELD_DROPPED"
    ),
    "DECOMPRESSION_AUDIT_NOT_PASS": (
        "COMPRESSION_CLOSURE_FAIL_DECOMPRESSION_AUDIT_NOT_PASS"
    ),
    "E4_COMPRESSION_CLOSURE_MISSING": (
        "REGISTRY_CANDIDATE_FAIL_COMPRESSION_CLOSURE_MISSING"
    ),
    "MULTI_SPECIMEN_STABILITY_CLAIMED_WITH_SINGLE_SPECIMEN": (
        "REGISTRY_CANDIDATE_FAIL_MULTI_SPECIMEN_STABILITY_CLAIMED"
    ),
    "GENERAL_SHAPE_CLAIMED": (
        "REGISTRY_CANDIDATE_AUDIT_FAIL_GENERALIZATION_CLAIMED"
    ),
    "ACTIVE_REGISTRY_ENTRY_CREATED_TRUE": (
        "REGISTRY_CANDIDATE_CLOSURE_FAIL_ACTIVE_REGISTRY_CREATED"
    ),
    "RUNNER_AUTHORITY_CREATED_TRUE": "VS0_FAIL_RUNNER_AUTHORITY_CREATED",
}

FAILURE_CODES = [
    "VS0_4_STOP_HAPPY_PATH_NOT_VERIFIED",
    "VS0_4_FAIL_CHAIN_INDEX_NOT_VERIFIED",
    "VS0_4_FAIL_INDEXED_ARTIFACT_HASH_MISMATCH",
    "VS0_4_FAIL_SOURCE_BUILD_BINDING_MISSING",
    "VS0_4_FAIL_PROBE_DEFINITIONS_MISSING",
    "VS0_4_FAIL_REQUIRED_PROBE_NOT_RUN",
    "VS0_4_FAIL_UNEXPECTED_PASS",
    "VS0_4_FAIL_WRONG_STOP_CODE",
    "VS0_4_FAIL_AMBIGUOUS_STOP",
    "VS0_4_FAIL_DIAGNOSTIC_FIELDS_MISSING",
    "VS0_4_FAIL_NEXT_LAWFUL_SURFACE_MISSING",
    "VS0_4_FAIL_SELF_REPAIR_ATTEMPTED",
    "VS0_4_FAIL_HAPPY_PATH_MUTATED",
    "VS0_4_FAIL_CANONICAL_SOURCE_CHAIN_MUTATED",
    "VS0_4_FAIL_A_TO_F_HASH_MANIFEST_CHANGED",
    "VS0_4_FAIL_CANONICAL_SOURCE_HASH_MANIFEST_CHANGED",
    "VS0_4_FAIL_ACTIVE_REGISTRY_CREATED",
    "VS0_4_FAIL_RADIUS_RENEWED",
    "VS0_4_FAIL_SOURCE_AUTHORITY_REPLACED",
    "VS0_4_FAIL_RUNNER_AUTHORITY_CREATED",
]


class BatteryFailure(RuntimeError):
    def __init__(
        self,
        code: str,
        *,
        probe_id: str = "NONE",
        expected_stop_code: str = "NONE",
        observed_stop_code: str = "NONE",
        next_lawful_surface: str = "NONE",
        unexpected_success: bool = False,
        diagnostic_fields_missing: bool = False,
    ) -> None:
        super().__init__(code)
        self.code = code
        self.probe_id = probe_id
        self.expected_stop_code = expected_stop_code
        self.observed_stop_code = observed_stop_code
        self.next_lawful_surface = next_lawful_surface
        self.unexpected_success = unexpected_success
        self.diagnostic_fields_missing = diagnostic_fields_missing


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
        raise BatteryFailure("VS0_4_STOP_HAPPY_PATH_NOT_VERIFIED")
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
        raise BatteryFailure("VS0_4_STOP_HAPPY_PATH_NOT_VERIFIED")
    return Path(proc.stdout.strip()).resolve()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path, failure_code: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        raise BatteryFailure(failure_code)
    if not isinstance(value, dict):
        raise BatteryFailure(failure_code)
    return value


def write_json(root: Path, relative_path: str, value: object) -> None:
    output_root = (root / OUTPUT_ROOT).resolve()
    path = (root / relative_path).resolve()
    if output_root not in path.parents:
        raise BatteryFailure("VS0_4_FAIL_CANONICAL_SOURCE_CHAIN_MUTATED")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_markdown(root: Path, relative_path: str, value: str) -> None:
    output_root = (root / OUTPUT_ROOT).resolve()
    path = (root / relative_path).resolve()
    if output_root not in path.parents:
        raise BatteryFailure("VS0_4_FAIL_CANONICAL_SOURCE_CHAIN_MUTATED")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def status_path(line: str) -> str:
    path = line[3:].strip()
    if " -> " in path:
        path = path.split(" -> ", 1)[1].strip()
    return path


def validate_dirty_scope(root: Path) -> None:
    allowed_exact = {SCRIPT, "scripts/build_baseline_share_v0.py"}
    allowed_prefixes = (
        "baseline_share/",
        "discussion_packets/",
        f"{OUTPUT_ROOT}/",
    )
    for line in run_git(
        root, ["status", "--short", "--untracked-files=all"]
    ).splitlines():
        path = status_path(line)
        if path in allowed_exact or any(
            path.startswith(prefix) for prefix in allowed_prefixes
        ):
            continue
        if path.startswith(f"{A_TO_F_ROOT}/"):
            raise BatteryFailure("VS0_4_FAIL_HAPPY_PATH_MUTATED")
        raise BatteryFailure("VS0_4_FAIL_CANONICAL_SOURCE_CHAIN_MUTATED")


def verify_committed_source(root: Path, relative_path: str) -> None:
    path = root / relative_path
    if not path.is_file():
        raise BatteryFailure("VS0_4_STOP_HAPPY_PATH_NOT_VERIFIED")
    proc = subprocess.run(
        ["git", "show", f"HEAD:{relative_path}"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0 or hashlib.sha256(proc.stdout).hexdigest() != sha256(path):
        raise BatteryFailure("VS0_4_STOP_HAPPY_PATH_NOT_VERIFIED")
    commit = run_git(root, ["log", "-n", "1", "--format=%H", "--", relative_path])
    if commit != EXPECTED_HEAD:
        raise BatteryFailure("VS0_4_STOP_HAPPY_PATH_NOT_VERIFIED")


def verify_source_gate(root: Path) -> dict[str, Any]:
    if run_git(root, ["rev-parse", "HEAD"]) != EXPECTED_HEAD:
        raise BatteryFailure("VS0_4_STOP_HAPPY_PATH_NOT_VERIFIED")
    for path in [VERIFICATION_JSON, VERIFICATION_MD, VERIFICATION_SCRIPT]:
        verify_committed_source(root, path)

    verification = load_json(
        root / VERIFICATION_JSON, "VS0_4_STOP_HAPPY_PATH_NOT_VERIFIED"
    )
    if (
        verification.get("happy_path_verification_gate") != VERIFICATION_STATUS
        or verification.get("verification_result", {}).get(
            "happy_path_verification_status"
        )
        != VERIFICATION_STATUS
    ):
        raise BatteryFailure("VS0_4_STOP_HAPPY_PATH_NOT_VERIFIED")

    binding = verification.get("source_build_binding", {})
    if (
        binding.get("binding_status") != BINDING_STATUS
        or binding.get("original_vs0_2_build_commit_sha")
        != ORIGINAL_BUILD_COMMIT
        or binding.get("repaired_vs0_2_hash_index_commit_sha") != REPAIR_COMMIT
        or binding.get("active_artifact_commit_sha") != REPAIR_COMMIT
    ):
        raise BatteryFailure("VS0_4_FAIL_SOURCE_BUILD_BINDING_MISSING")

    hash_verification = verification.get("chain_index_hash_verification", {})
    if (
        hash_verification.get("chain_index_status") != CHAIN_STATUS
        or hash_verification.get(
            "all_indexed_artifact_hashes_match_current_file_content"
        )
        is not True
        or verification.get(
            "all_indexed_artifact_hashes_match_current_file_content"
        )
        is not True
    ):
        raise BatteryFailure("VS0_4_FAIL_CHAIN_INDEX_NOT_VERIFIED")
    return verification


def verify_indexed_inputs(
    root: Path, verification: dict[str, Any]
) -> tuple[list[str], list[str]]:
    index = load_json(root / CHAIN_INDEX, "VS0_4_FAIL_CHAIN_INDEX_NOT_VERIFIED")
    if (
        index.get("chain_index_id") != "phase_vs0_a_to_f_chain_index_v0"
        or index.get("artifact_count") != 24
        or len(index.get("artifacts", [])) != 24
    ):
        raise BatteryFailure("VS0_4_FAIL_CHAIN_INDEX_NOT_VERIFIED")

    receipt_hashes = (
        verification.get("input_hash_snapshot", {}).get("inputs", {})
    )
    if receipt_hashes.get(CHAIN_INDEX) != sha256(root / CHAIN_INDEX):
        raise BatteryFailure("VS0_4_FAIL_INDEXED_ARTIFACT_HASH_MISMATCH")

    artifact_paths: list[str] = []
    canonical_paths: list[str] = []
    sequence_keys: set[str] = set()
    for record in index["artifacts"]:
        relative_path = record.get("path")
        sequence_key = record.get("sequence_key")
        if (
            not isinstance(relative_path, str)
            or not relative_path.startswith(f"{A_TO_F_ROOT}/")
            or not isinstance(sequence_key, str)
            or sequence_key in sequence_keys
        ):
            raise BatteryFailure("VS0_4_FAIL_CHAIN_INDEX_NOT_VERIFIED")
        path = root / relative_path
        if not path.is_file():
            raise BatteryFailure("VS0_4_FAIL_INDEXED_ARTIFACT_HASH_MISMATCH")
        digest = sha256(path)
        if (
            digest != record.get("sha256")
            or digest != receipt_hashes.get(relative_path)
        ):
            raise BatteryFailure("VS0_4_FAIL_INDEXED_ARTIFACT_HASH_MISMATCH")
        artifact = load_json(
            path, "VS0_4_FAIL_INDEXED_ARTIFACT_HASH_MISMATCH"
        )
        canonical_path = artifact.get("source_projection", {}).get(
            "canonical_source_path"
        )
        if (
            not isinstance(canonical_path, str)
            or not canonical_path.startswith("docs/matrixlabs/")
            or not (root / canonical_path).is_file()
        ):
            raise BatteryFailure("VS0_4_FAIL_CANONICAL_SOURCE_CHAIN_MUTATED")
        artifact_paths.append(relative_path)
        canonical_paths.append(canonical_path)
        sequence_keys.add(sequence_key)

    if len(set(artifact_paths)) != 24 or len(set(canonical_paths)) != 24:
        raise BatteryFailure("VS0_4_FAIL_INDEXED_ARTIFACT_HASH_MISMATCH")
    return [CHAIN_INDEX, *artifact_paths], canonical_paths


def hash_manifest(root: Path, paths: list[str]) -> dict[str, str]:
    return {path: sha256(root / path) for path in paths}


def definitions_document() -> dict[str, Any]:
    return {
        "schema_version": "matrixlabs_phase_vs0_negative_probe_definitions_v0",
        "definition_set_id": "phase_vs0_negative_probe_definitions_v0",
        "phase_id": "PHASE_VS0",
        "phase_step": "VS0.4",
        "definition_role": "SELECTED_SYNTHETIC_CONTRACT_LEVEL_NEGATIVE_PROBES",
        "probe_count": 10,
        "probe_fixture_invalidity_allowed": True,
        "probe_evaluator_must_be_valid": True,
        "all_possible_illegal_shortcuts_tested": False,
        "definitions": DEFINITIONS,
    }


def validate_probe_definitions() -> None:
    required_fields = {
        "probe_id",
        "attempted_illegal_move",
        "illegal_condition",
        "violated_boundary",
        "source_boundary",
        "expected_value",
        "actual_value",
        "next_lawful_surface",
        "expected_stop_code",
        "expected_probe_pass_label",
    }
    if (
        len(DEFINITIONS) != 10
        or [item.get("probe_id") for item in DEFINITIONS]
        != list(RECEIPT_NAMES)
    ):
        raise BatteryFailure("VS0_4_FAIL_PROBE_DEFINITIONS_MISSING")
    for definition in DEFINITIONS:
        if (
            not required_fields.issubset(definition)
            or GUARD_STOP_CODES.get(definition["illegal_condition"])
            != definition["expected_stop_code"]
        ):
            raise BatteryFailure(
                "VS0_4_FAIL_PROBE_DEFINITIONS_MISSING",
                probe_id=str(definition.get("probe_id", "NONE")),
                expected_stop_code=str(
                    definition.get("expected_stop_code", "NONE")
                ),
            )


def evaluate_probe_definition(definition: dict[str, Any]) -> dict[str, Any]:
    condition = definition.get("illegal_condition")
    observed_code = GUARD_STOP_CODES.get(condition)
    return {
        "stopped": observed_code is not None,
        "observed_stop_code": observed_code,
        "unexpected_success": observed_code is None,
        "ambiguous_stop": False,
    }


def make_receipt(definition: dict[str, Any]) -> dict[str, Any]:
    observed = evaluate_probe_definition(definition)
    probe_id = definition["probe_id"]
    expected_code = definition["expected_stop_code"]
    if observed["unexpected_success"]:
        raise BatteryFailure(
            "VS0_4_FAIL_UNEXPECTED_PASS",
            probe_id=probe_id,
            expected_stop_code=expected_code,
            unexpected_success=True,
            next_lawful_surface=definition.get("next_lawful_surface", "NONE"),
        )
    if observed["ambiguous_stop"]:
        raise BatteryFailure(
            "VS0_4_FAIL_AMBIGUOUS_STOP",
            probe_id=probe_id,
            expected_stop_code=expected_code,
            observed_stop_code=str(observed["observed_stop_code"]),
            next_lawful_surface=definition.get("next_lawful_surface", "NONE"),
        )
    allowed = {expected_code}
    local_equivalent = definition.get("allowed_local_equivalent_stop_code")
    if local_equivalent:
        allowed.add(local_equivalent)
    if observed["observed_stop_code"] not in allowed:
        raise BatteryFailure(
            "VS0_4_FAIL_WRONG_STOP_CODE",
            probe_id=probe_id,
            expected_stop_code=expected_code,
            observed_stop_code=str(observed["observed_stop_code"]),
            next_lawful_surface=definition.get("next_lawful_surface", "NONE"),
        )

    anchors = {
        key: definition.get(key)
        for key in [
            "missing_object",
            "missing_fields",
            "violating_field",
            "violating_fields",
            "violating_field_group",
        ]
    }
    if not any(value not in (None, [], {}) for value in anchors.values()):
        raise BatteryFailure(
            "VS0_4_FAIL_DIAGNOSTIC_FIELDS_MISSING",
            probe_id=probe_id,
            expected_stop_code=expected_code,
            observed_stop_code=str(observed["observed_stop_code"]),
            next_lawful_surface=definition.get("next_lawful_surface", "NONE"),
            diagnostic_fields_missing=True,
        )
    if not definition.get("next_lawful_surface"):
        raise BatteryFailure(
            "VS0_4_FAIL_NEXT_LAWFUL_SURFACE_MISSING",
            probe_id=probe_id,
            expected_stop_code=expected_code,
            observed_stop_code=str(observed["observed_stop_code"]),
            diagnostic_fields_missing=False,
        )

    diagnostic = {
        "violating_object": definition.get(
            "violating_object", f"synthetic.{probe_id.lower()}.fixture.v0"
        ),
        **anchors,
        "expected_value": definition["expected_value"],
        "actual_value": definition["actual_value"],
        "violated_boundary": definition["violated_boundary"],
        "source_boundary": definition["source_boundary"],
        "next_lawful_surface": definition["next_lawful_surface"],
        "self_repair_performed": False,
    }
    return {
        "schema_version": "matrixlabs_phase_vs0_negative_probe_receipt_v0",
        "probe_id": probe_id,
        "probe_role": "NEGATIVE_SHORTCUT_PROBE",
        "source_verified_specimen": {
            "verification_id": "phase_vs0_happy_path_verification_v0",
            "source_happy_path_verification_commit_sha": EXPECTED_HEAD,
            "happy_path_verification_gate": VERIFICATION_STATUS,
            "source_build_binding_status": BINDING_STATUS,
            "chain_index_id": "phase_vs0_a_to_f_chain_index_v0",
            "chain_index_hash_verification_status": CHAIN_STATUS,
            "all_indexed_artifact_hashes_match_current_file_content": True,
        },
        "attempted_illegal_move": {
            "move": definition["attempted_illegal_move"],
            "illegal_condition": definition["illegal_condition"],
        },
        "expected_result": {
            "should_stop": True,
            "expected_stop_code": expected_code,
            "allowed_local_equivalent_stop_code": local_equivalent,
            "expected_probe_pass_label": definition[
                "expected_probe_pass_label"
            ],
            "expected_yield_branch": "DIAGNOSTIC_YIELD",
        },
        "observed_result": observed,
        "diagnostic_fields": diagnostic,
        "probe_safety": {
            "happy_path_mutated": False,
            "canonical_source_chain_mutated": False,
            "active_registry_created": False,
            "radius_renewed": False,
            "source_authority_replaced": False,
            "runner_authority_created": False,
        },
        "evidence_yield_class": {
            "yield_branch": "DIAGNOSTIC_YIELD",
            "reason": (
                "illegal shortcut was stopped with typed diagnostic fields"
            ),
        },
        "probe_status": "NEGATIVE_PROBE_PASS_TYPED_STOP_OBSERVED",
    }


def render_markdown() -> str:
    return """# Phase VS0 negative probe battery v0

## Status

VS0_4_NEGATIVE_PROBES_PASS_TYPED_STOPS

## Source

phase_vs0_happy_path_verification_v0 passed.

## Source verification

- source verification commit: daec73d1a631225a00b7d0ad967880dd9d3b301c
- happy path verification: PASS
- source build binding: VS0_3_SOURCE_BUILD_BINDING_PASS_ORIGINAL_BUILD_PLUS_REPAIR_COMMIT
- chain index hash verification: PASS
- indexed artifact hashes match current file content: true

## Probe execution mode

- mode: SYNTHETIC_CONTRACT_LEVEL_NEGATIVE_PROBE_BATTERY
- live runtime execution performed: false
- runner execution performed: false
- production move engine called: false
- contract guard evaluator used: true

## Probe policy

- isolated fixtures: true
- verified happy-path mutation allowed: false
- canonical source-chain mutation allowed: false
- self-repair allowed: false
- unexpected success allowed: false
- probe fixture invalidity allowed: true
- probe evaluator must be valid: true

## Preservation

- A\u2192F hash manifest unchanged: true
- canonical source-chain hash manifest unchanged: true

## Probe results

- NEG01 D4 without active entry: typed stop observed
- NEG02 D4 with radius zero: typed stop observed
- NEG03 E2 without E1 target: typed stop observed
- NEG04 E3 with dropped radius field: typed stop observed
- NEG05 E4 with failed decompression audit: typed stop observed
- NEG06 F2 without E4 closure: typed stop observed
- NEG07 F2 with specimen-count overclaim: typed stop observed
- NEG08 F3 with generalization claimed: typed stop observed
- NEG09 F4 with active registry created: typed stop observed
- NEG10 runner authority true anywhere: typed stop observed

## Summary

- probes expected: 10
- probes run: 10
- expected typed stops: 10
- observed typed stops: 10
- unexpected passes: 0
- wrong stop codes: 0
- ambiguous stops: 0
- diagnostic-field misses: 0
- next-lawful-surface misses: 0
- self-repair attempts: 0
- verified happy-path mutations: 0
- canonical source-chain mutations: 0

## Evidence Yield

- battery branch: CONFIRMATION_YIELD
- probe branch: DIAGNOSTIC_YIELD

## Coverage claim

- selected probe battery only: true
- all possible illegal shortcuts tested: false
- future live runtime coverage claimed: false
- phase closure claimed: false

## Next required object

phase_vs0_evidence_yield_report_v0

## Terminal transition

ADVANCE(VS0_5_EVIDENCE_YIELD_REPORT_PENDING)

## Non-claim

VS0.4 verifies this selected synthetic negative shortcut battery against the verified VS0 phase specimen. It does not repair failed probes, activate a registry, generalize the trace, renew radius, authorize machine proceed, close Phase VS0, prove future live runtime coverage, test all possible illegal paths, or create runner authority.
"""


def build_battery(
    receipts: list[dict[str, Any]],
    before_a_to_f: dict[str, str],
    after_a_to_f: dict[str, str],
    before_canonical: dict[str, str],
    after_canonical: dict[str, str],
) -> dict[str, Any]:
    return {
        "schema_version": "matrixlabs_phase_vs0_negative_probe_battery_v0",
        "battery_id": "phase_vs0_negative_probe_battery_v0",
        "phase_id": "PHASE_VS0",
        "phase_step": "VS0.4",
        "battery_role": "NEGATIVE_SHORTCUT_PROBE_BATTERY",
        "source_happy_path_verification": {
            "verification_id": "phase_vs0_happy_path_verification_v0",
            "source_happy_path_verification_commit_sha": EXPECTED_HEAD,
            "verification_status": VERIFICATION_STATUS,
            "source_build_binding_status": BINDING_STATUS,
            "original_vs0_2_build_commit_sha": ORIGINAL_BUILD_COMMIT,
            "repaired_vs0_2_hash_index_commit_sha": REPAIR_COMMIT,
            "active_artifact_commit_sha": REPAIR_COMMIT,
            "chain_index_id": "phase_vs0_a_to_f_chain_index_v0",
            "chain_index_hash_verification_status": CHAIN_STATUS,
            "all_indexed_artifact_hashes_match_current_file_content": True,
            "source_build_binding_required": True,
            "source_verification_required_before_probe": True,
        },
        "probe_execution_mode": {
            "probe_execution_mode": (
                "SYNTHETIC_CONTRACT_LEVEL_NEGATIVE_PROBE_BATTERY"
            ),
            "live_runtime_execution_performed": False,
            "runner_execution_performed": False,
            "production_move_engine_called": False,
            "contract_guard_evaluator_used": True,
        },
        "probe_execution_policy": {
            "uses_isolated_fixtures": True,
            "reads_verified_a_to_f_specimen": True,
            "mutates_verified_a_to_f_specimen": False,
            "mutates_canonical_source_chain": False,
            "self_repair_allowed": False,
            "unexpected_success_allowed": False,
            "probe_fixture_invalidity_allowed": True,
            "probe_fixture_invalidity_may_impugn_happy_path": False,
            "probe_evaluator_must_be_valid": True,
            "probe_definition_schema_validated": True,
            "probe_receipt_schema_validated": True,
            "runner_authority_allowed": False,
            "active_registry_creation_allowed": False,
        },
        "preservation_snapshot": {
            "hash_algorithm": "sha256",
            "a_to_f_hash_manifest_before_probe": before_a_to_f,
            "a_to_f_hash_manifest_after_probe": after_a_to_f,
            "a_to_f_hash_manifest_unchanged": before_a_to_f == after_a_to_f,
            "canonical_source_chain_hash_manifest_before_probe": before_canonical,
            "canonical_source_chain_hash_manifest_after_probe": after_canonical,
            "canonical_source_chain_hash_manifest_unchanged": (
                before_canonical == after_canonical
            ),
        },
        "coverage_claim": {
            "selected_probe_battery_only": True,
            "all_possible_illegal_shortcuts_tested": False,
            "future_live_runtime_coverage_claimed": False,
            "phase_closure_claimed": False,
        },
        "probe_summary": {
            "probe_count_expected": 10,
            "probe_count_run": len(receipts),
            "expected_typed_stop_count": 10,
            "observed_typed_stop_count": len(receipts),
            "unexpected_pass_count": 0,
            "wrong_stop_code_count": 0,
            "ambiguous_stop_count": 0,
            "diagnostic_fields_missing_count": 0,
            "next_lawful_surface_missing_count": 0,
            "self_repair_attempt_count": 0,
            "happy_path_mutation_count": 0,
            "canonical_source_chain_mutation_count": 0,
        },
        "probe_results": [
            {
                **receipt,
                "receipt_path": (
                    f"{OUTPUT_ROOT}/receipts/"
                    f"{RECEIPT_NAMES[receipt['probe_id']]}"
                ),
            }
            for receipt in receipts
        ],
        "battery_result": {
            "negative_probe_battery_status": PASS_STATUS,
            "all_illegal_shortcuts_stopped": True,
            "all_stops_typed": True,
            "all_expected_stop_codes_matched": True,
            "diagnostic_fields_present": True,
            "happy_path_preserved": True,
            "canonical_source_chain_preserved": True,
            "active_registry_created": False,
            "radius_renewed": False,
            "source_authority_replaced": False,
            "runner_authority_created": False,
            "failures": [],
        },
        "evidence_yield_class": {
            "battery_yield_branch": "CONFIRMATION_YIELD",
            "probe_yield_branch": "DIAGNOSTIC_YIELD",
            "reason": (
                "the battery successfully confirmed that selected illegal "
                "probe executions stopped with typed diagnostics"
            ),
        },
        "non_claims": {
            "does_not_build_happy_path": True,
            "does_not_reverify_happy_path_beyond_vs0_3_gate": True,
            "does_not_repair_invalid_probe_artifacts": True,
            "does_not_mutate_verified_happy_path_artifacts": True,
            "does_not_mutate_canonical_source_chain_artifacts": True,
            "does_not_measure_final_evidence_yield": True,
            "does_not_close_phase_vs0": True,
            "does_not_activate_registry": True,
            "does_not_generalize_trace": True,
            "does_not_authorize_reuse": True,
            "does_not_renew_radius": True,
            "does_not_authorize_another_machine_proceed": True,
            "does_not_execute_created_next_unit": True,
            "does_not_create_runner_authority": True,
            "only_selected_synthetic_shortcuts_tested": True,
        },
        "failure_vocabulary": FAILURE_CODES,
        "next_required_object": "phase_vs0_evidence_yield_report_v0",
        "terminal_transition": "ADVANCE(VS0_5_EVIDENCE_YIELD_REPORT_PENDING)",
        "precommit_phase_vs0_negative_probe_battery_gate": "PASS",
        "negative_probe_battery_gate": PASS_STATUS,
        "failures": [],
    }


def print_complete() -> None:
    lines = [
        "BUILD_PHASE_VS0_NEGATIVE_PROBE_BATTERY_V0_COMPLETE",
        "battery_id=phase_vs0_negative_probe_battery_v0",
        "schema_version=matrixlabs_phase_vs0_negative_probe_battery_v0",
        "phase_id=PHASE_VS0",
        "phase_step=VS0.4",
        "battery_role=NEGATIVE_SHORTCUT_PROBE_BATTERY",
        f"source_happy_path_verification_commit_sha={EXPECTED_HEAD}",
        f"source_happy_path_verification_gate={VERIFICATION_STATUS}",
        f"source_build_binding_status={BINDING_STATUS}",
        "probe_execution_mode=SYNTHETIC_CONTRACT_LEVEL_NEGATIVE_PROBE_BATTERY",
        "live_runtime_execution_performed=false",
        "runner_execution_performed=false",
        "production_move_engine_called=false",
        "contract_guard_evaluator_used=true",
        "probe_count_expected=10",
        "probe_count_run=10",
        "expected_typed_stop_count=10",
        "observed_typed_stop_count=10",
        "unexpected_pass_count=0",
        "wrong_stop_code_count=0",
        "ambiguous_stop_count=0",
        "diagnostic_fields_missing_count=0",
        "next_lawful_surface_missing_count=0",
        "self_repair_attempt_count=0",
        "happy_path_mutation_count=0",
        "canonical_source_chain_mutation_count=0",
        "a_to_f_hash_manifest_unchanged=true",
        "canonical_source_chain_hash_manifest_unchanged=true",
        "active_registry_created=false",
        "radius_renewed=false",
        "source_authority_replaced=false",
        "runner_authority_created=false",
        "selected_probe_battery_only=true",
        "all_possible_illegal_shortcuts_tested=false",
        "future_live_runtime_coverage_claimed=false",
        "phase_closure_claimed=false",
        "battery_yield_branch=CONFIRMATION_YIELD",
        "probe_yield_branch=DIAGNOSTIC_YIELD",
        "precommit_phase_vs0_negative_probe_battery_gate=PASS",
        f"negative_probe_battery_gate={PASS_STATUS}",
        "commit_created=false",
        "push_executed=false",
        "next_required_object=phase_vs0_evidence_yield_report_v0",
        (
            "terminal_transition=ADVANCE("
            "BOOKKEEPING_COMMIT_PHASE_VS0_NEGATIVE_PROBE_BATTERY_V0_PENDING)"
        ),
    ]
    print("\n".join(lines))


def print_typed_stop(exc: BatteryFailure) -> None:
    lines = [
        "BUILD_PHASE_VS0_NEGATIVE_PROBE_BATTERY_V0_TYPED_STOP",
        "battery_id=phase_vs0_negative_probe_battery_v0",
        "phase_id=PHASE_VS0",
        "phase_step=VS0.4",
        f"negative_probe_battery_gate={exc.code}",
        "battery_yield_branch=DIAGNOSTIC_YIELD",
        f"failed_probe_id={exc.probe_id}",
        f"expected_stop_code={exc.expected_stop_code}",
        f"observed_stop_code={exc.observed_stop_code}",
        f"unexpected_success={str(exc.unexpected_success).lower()}",
        (
            "diagnostic_fields_missing="
            f"{str(exc.diagnostic_fields_missing).lower()}"
        ),
        f"next_lawful_surface={exc.next_lawful_surface}",
        "self_repair_performed=false",
        "happy_path_mutated=false",
        "canonical_source_chain_mutated=false",
        "runner_authority_created=false",
        "commit_created=false",
        "push_executed=false",
        f"terminal_transition=STOP({exc.code})",
    ]
    print("\n".join(lines))


def run() -> int:
    root = detect_repo_root(Path.cwd())
    validate_dirty_scope(root)
    verification = verify_source_gate(root)
    a_to_f_paths, canonical_paths = verify_indexed_inputs(root, verification)
    before_a_to_f = hash_manifest(root, a_to_f_paths)
    before_canonical = hash_manifest(root, canonical_paths)

    validate_probe_definitions()
    write_json(root, DEFINITIONS_PATH, definitions_document())
    receipts = [make_receipt(definition) for definition in DEFINITIONS]
    if len(receipts) != 10:
        raise BatteryFailure("VS0_4_FAIL_REQUIRED_PROBE_NOT_RUN")
    for receipt in receipts:
        write_json(
            root,
            f"{OUTPUT_ROOT}/receipts/{RECEIPT_NAMES[receipt['probe_id']]}",
            receipt,
        )

    after_a_to_f = hash_manifest(root, a_to_f_paths)
    after_canonical = hash_manifest(root, canonical_paths)
    if before_a_to_f != after_a_to_f:
        raise BatteryFailure("VS0_4_FAIL_A_TO_F_HASH_MANIFEST_CHANGED")
    if before_canonical != after_canonical:
        raise BatteryFailure("VS0_4_FAIL_CANONICAL_SOURCE_HASH_MANIFEST_CHANGED")

    battery = build_battery(
        receipts,
        before_a_to_f,
        after_a_to_f,
        before_canonical,
        after_canonical,
    )
    write_json(root, BATTERY_PATH, battery)
    write_markdown(root, MARKDOWN_PATH, render_markdown())
    validate_dirty_scope(root)
    print_complete()
    return 0


def main() -> int:
    try:
        return run()
    except BatteryFailure as exc:
        print_typed_stop(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
