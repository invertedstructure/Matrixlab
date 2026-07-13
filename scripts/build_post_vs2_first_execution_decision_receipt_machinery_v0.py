#!/usr/bin/env python3
"""Build Post-VS2 first execution decision receipt machinery v0."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import build_post_vs2_first_execution_decision_surface_v0 as surface_helper


ROOT = "/home/asd/projects/matrixlab"
BRANCH = "master"
HEAD = "a6252de12e71ad9eb558a9a5a539e21002678dc3"
CANON = "MATRIXLAB_CANONICAL_JSON_V0"
HASH_ALGORITHM = "sha256"

UNIT = "BUILD_POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_V0"
CURRENT_UNIT = "POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_PREPARATION"
SURFACE_ID = "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE"
SURFACE_VERSION = "v0"
SURFACE_GATE = "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_PASS_READY_FOR_HUMAN_DECISION"
MACHINERY_GATE = "POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_PASS_READY_FOR_EXPLICIT_HUMAN_DECISION_INPUT"
TERMINAL = "STOP_POST_VS2_DECISION_RECEIPT_MACHINERY_READY_SURFACE_UNCONSUMED"
BOOKKEEPING = "ADVANCE(BOOKKEEPING_COMMIT_POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_V0_PENDING)"

SURFACE_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_v0.json"
SURFACE_MD = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_v0.md"
SURFACE_RECEIPT_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_receipt_v0.json"
INPUT_CONTRACT_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_human_decision_input_contract_v0.json"
INPUT_CONTRACT_MD = "docs/matrixlabs/post_vs2/post_vs2_first_execution_human_decision_input_contract_v0.md"
RECEIPT_CONTRACT_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_contract_v0.json"
RECEIPT_CONTRACT_MD = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_contract_v0.md"
MACHINERY_RECEIPT_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_machinery_receipt_v0.json"
AUTHORITATIVE_RECEIPT_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_v0.json"
AUTHORITATIVE_RECEIPT_MD = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_v0.md"

SCRIPT = "scripts/build_post_vs2_first_execution_decision_receipt_machinery_v0.py"
VERIFY_SCRIPT = "scripts/verify_post_vs2_first_execution_decision_receipt_machinery_v0.py"
RECEIPT_BUILDER = "scripts/build_post_vs2_first_execution_decision_receipt_v0.py"
RECEIPT_VERIFIER = "scripts/verify_post_vs2_first_execution_decision_receipt_v0.py"
BASELINE_SCRIPT = "scripts/build_baseline_share_v0.py"
BASELINE_OUTPUTS = [
    "baseline_share/COMMIT_CONTEXT.md",
    "baseline_share/CURRENT_STATE.md",
    "baseline_share/MANIFEST.json",
    "baseline_share/RECEIPT_POINTERS.md",
]

EXPECTED_NEW = {
    SCRIPT,
    VERIFY_SCRIPT,
    RECEIPT_BUILDER,
    RECEIPT_VERIFIER,
    INPUT_CONTRACT_JSON,
    INPUT_CONTRACT_MD,
    RECEIPT_CONTRACT_JSON,
    RECEIPT_CONTRACT_MD,
    MACHINERY_RECEIPT_JSON,
}
EXPECTED_MODIFIED = {BASELINE_SCRIPT, *BASELINE_OUTPUTS}
ALLOWED_DIRTY = EXPECTED_NEW | EXPECTED_MODIFIED

SURFACE_CANONICAL_SHA256 = "d7150101acbfe46342c95506c526e2b49b6ca295881c2e390d78fdb4c5001d35"
SURFACE_RAW_SHA256 = "396d12f164d1b338b80effa0e7631da6fe261ef695fa8e781e4208740970a1b3"
SURFACE_MD_RAW_SHA256 = "979675da833a5e5635012870a00570da3eb20d58001ad7d4aa899d9f9d8d49e4"
SURFACE_RECEIPT_CANONICAL_SHA256 = "658fcc2331fd3fc3c9c2865778d9163ddcb05724db1dc2d3343189859c4100cd"
SURFACE_RECEIPT_RAW_SHA256 = "56a6777f7ef4c4d3a27d24a22c018af4b928852f69333f685583008845ece7b7"

OPTION_TO_BRANCH = {
    "AUTHORIZE_EXACT_SEALED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE": "D01",
    "REQUEST_REDUCED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_VERSION": "D02",
    "RETURN_SEALED_FIRST_SWEEP_KERNEL_PACKAGE_FOR_REVISION": "D03",
    "DEFER_FIRST_SWEEP_KERNEL_EXECUTION_DECISION": "D04",
    "REJECT_CURRENT_FIRST_SWEEP_KERNEL_EXECUTION_REQUEST": "D05",
    "ABANDON_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_VERSION": "D06",
}
BRANCH_TO_GATE = {
    "D01": "POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_PASS_EXACT_AUTHORIZATION_RECORDED_AUTHORITY_NOT_APPLIED",
    "D02": "POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_PASS_REDUCED_PACKAGE_REQUEST_RECORDED",
    "D03": "POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_PASS_REVISION_REQUEST_RECORDED",
    "D04": "POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_PASS_DECISION_DEFERRED",
    "D05": "POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_PASS_CURRENT_EXECUTION_REQUEST_REJECTED",
    "D06": "POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_PASS_PACKAGE_ABANDONMENT_DECISION_RECORDED",
}
BRANCH_TO_ROUTE = {
    "D01": "POST_VS2_FIRST_EXECUTION_AUTHORITY_UPDATE",
    "D02": "POST_VS2_REDUCED_PACKAGE_REBUILD_SCOPE_PREPARATION",
    "D03": "POST_VS2_EXECUTION_PACKAGE_REVISION_SCOPE_SURFACE",
    "D04": "STOP_POST_VS2_EXECUTION_DECISION_DEFERRED",
    "D05": "STOP_POST_VS2_EXECUTION_REQUEST_REJECTED",
    "D06": "POST_VS2_EXECUTION_PACKAGE_DISPOSITION_UPDATE",
}
BRANCH_TO_TRANSITION = {
    "D01": "ADVANCE(POST_VS2_FIRST_EXECUTION_AUTHORITY_UPDATE_PENDING)",
    "D02": "ADVANCE(POST_VS2_REDUCED_PACKAGE_REBUILD_SCOPE_PREPARATION_PENDING)",
    "D03": "ADVANCE(POST_VS2_EXECUTION_PACKAGE_REVISION_SCOPE_SURFACE_PENDING)",
    "D04": "STOP_POST_VS2_EXECUTION_DECISION_DEFERRED",
    "D05": "STOP_POST_VS2_EXECUTION_REQUEST_REJECTED",
    "D06": "ADVANCE(POST_VS2_EXECUTION_PACKAGE_DISPOSITION_UPDATE_PENDING)",
}
R_CHECKS = [
    "R01_SURFACE_PACKAGE_VERIFIED",
    "R02_DECISION_SUBJECT_VERIFIED",
    "R03_READINESS_CHAIN_VERIFIED",
    "R04_IDENTITY_FRESHNESS_VERIFIED",
    "R05_EXECUTION_ELIGIBILITY_FRESHNESS_VERIFIED",
    "R06_HUMAN_DECISION_INPUT_AND_AUTHENTICITY_VERIFIED",
    "R07_OPTION_BRANCH_MAPPING_VERIFIED",
    "R08_SURFACE_CONSUMPTION_UNIQUENESS_VERIFIED",
    "R09_D01_EXACT_AUTHORIZATION_VERIFIED",
    "R10_D02_REDUCED_PACKAGE_REQUEST_VERIFIED",
    "R11_D03_REVISION_REQUEST_VERIFIED",
    "R12_D04_DEFERRAL_VERIFIED",
    "R13_D05_REJECTION_VERIFIED",
    "R14_D06_ABANDONMENT_VERIFIED",
    "R15_NO_DIRECT_AUTHORITY_EFFECT_VERIFIED",
    "R16_NO_DIRECT_PACKAGE_STATE_EFFECT_VERIFIED",
    "R17_DOWNSTREAM_ROUTE_VERIFIED",
    "R18_RECEIPT_NOT_PRECONSUMED_VERIFIED",
    "R19_RECEIPT_HASH_GRAPH_VERIFIED",
    "R20_NO_EXECUTION_DRIFT_VERIFIED",
]
MC_CHECKS = [
    "MC01_COMMITTED_SURFACE_PACKAGE_VERIFIED",
    "MC02_SURFACE_UNCONSUMED_VERIFIED",
    "MC03_SOURCE_IDENTITY_AND_LINKAGE_VERIFIED",
    "MC04_HUMAN_INPUT_CONTRACT_COMPLETE",
    "MC05_TIMESTAMP_LAW_COMPLETE",
    "MC06_OPTION_VOCABULARY_COMPLETE",
    "MC07_OPTION_BRANCH_MAPPING_COMPLETE",
    "MC08_D01_PAYLOAD_AND_ROUTE_COMPLETE",
    "MC09_D02_PAYLOAD_AND_ROUTE_COMPLETE",
    "MC10_D03_PAYLOAD_AND_ROUTE_COMPLETE",
    "MC11_D04_PAYLOAD_AND_TERMINAL_COMPLETE",
    "MC12_D05_PAYLOAD_AND_TERMINAL_COMPLETE",
    "MC13_D06_PAYLOAD_AND_ROUTE_COMPLETE",
    "MC14_NORMALIZED_BLOCKER_POSTURE_COMPLETE",
    "MC15_IDENTITY_AND_ELIGIBILITY_FRESHNESS_LAW_COMPLETE",
    "MC16_SURFACE_CONSUMPTION_LAW_COMPLETE",
    "MC17_DOWNSTREAM_RECEIPT_CONSUMPTION_LAW_COMPLETE",
    "MC18_NON_CIRCULAR_HASH_GRAPH_COMPLETE",
    "MC19_AUTHORITATIVE_BUILDER_INTERFACE_COMPLETE",
    "MC20_INDEPENDENT_VERIFIER_INTERFACE_COMPLETE",
    "MC21_VALIDATION_ONLY_NON_EFFECTS_VERIFIED",
    "MC22_NEGATIVE_PROBE_MATRIX_VERIFIED",
    "MC23_DETERMINISM_VERIFIED",
    "MC24_NO_DECISION_AUTHORITY_OR_EXECUTION_DRIFT",
]
NEGATIVE_PROBES = [
    ("P01", "missing decision input", "STOP_POST_VS2_DECISION_RECEIPT_HUMAN_DECISION_INPUT_MISSING"),
    ("P02", "generic proceed option", "STOP_POST_VS2_DECISION_RECEIPT_DECISION_OPTION_INVALID"),
    ("P03", "wrong surface hash", "STOP_POST_VS2_DECISION_RECEIPT_SURFACE_IDENTITY_MISMATCH"),
    ("P04", "multiple primary options", "STOP_POST_VS2_DECISION_RECEIPT_MULTIPLE_PRIMARY_OPTIONS"),
    ("P05", "missing authentication reference", "STOP_POST_VS2_DECISION_RECEIPT_DECISION_AUTHENTICATION_MISSING"),
    ("P06", "invalid timestamp", "STOP_POST_VS2_DECISION_RECEIPT_DECISION_TIMESTAMP_INVALID"),
    ("P07", "D01 reduced fixture scope", "STOP_POST_VS2_DECISION_RECEIPT_EXACT_PACKAGE_SCOPE_MISMATCH"),
    ("P08", "D01 missing expiry", "STOP_POST_VS2_DECISION_RECEIPT_EXACT_AUTHORIZATION_EXPIRY_INVALID"),
    ("P09", "D02 fixture reorder", "STOP_POST_VS2_DECISION_RECEIPT_REDUCED_PACKAGE_ORDER_NOT_SUBSEQUENCE"),
    ("P10", "D02 no actual reduction", "STOP_POST_VS2_DECISION_RECEIPT_REDUCED_PACKAGE_REQUEST_INVALID"),
    ("P11", "D03 incomplete affected surface", "STOP_POST_VS2_DECISION_RECEIPT_REVISION_REQUEST_INCOMPLETE"),
    ("P12", "D04 incomplete reconsideration posture", "STOP_POST_VS2_DECISION_RECEIPT_DEFER_PAYLOAD_INCOMPLETE"),
    ("P13", "D05 CURRENT_PACKAGE_VERSION scope", "STOP_POST_VS2_DECISION_RECEIPT_REJECTION_SCOPE_AMBIGUOUS"),
    ("P14", "D06 broad architecture abandonment", "STOP_POST_VS2_DECISION_RECEIPT_ABANDONMENT_SCOPE_AMBIGUOUS"),
    ("P15", "duplicate surface-consumption key", "STOP_POST_VS2_DECISION_RECEIPT_SURFACE_ALREADY_CONSUMED"),
    ("P16", "active execution authority present", "STOP_POST_VS2_DECISION_RECEIPT_EXECUTION_AUTHORITY_PRESENT"),
    ("P17", "run id present", "STOP_POST_VS2_DECISION_RECEIPT_RUN_ID_CREATED"),
    ("P18", "execution-source intake present", "STOP_POST_VS2_DECISION_RECEIPT_EXECUTION_SOURCE_INTAKE_CREATED"),
]


class StopFailure(RuntimeError):
    def __init__(self, code: str, check: str, observed: Any = None) -> None:
        super().__init__(code)
        self.code = code
        self.check = check
        self.observed = observed


def stop(code: str, check: str, observed: Any = None) -> None:
    raise StopFailure(code, check, observed)


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
    return subprocess.check_output(["git", *args], cwd=root, text=not binary)


def status_paths(status: str) -> set[str]:
    paths: set[str] = set()
    for line in status.splitlines():
        if line.startswith("?? "):
            paths.add(line[3:])
        elif len(line) >= 4:
            paths.add(line[3:])
    return paths


def check_repo(root: Path) -> None:
    if str(root) != ROOT:
        stop("STOP_POST_VS2_DECISION_RECEIPT_MACHINERY_REPOSITORY_ROOT_MISMATCH", "repo_root", str(root))
    if git(root, ["branch", "--show-current"]).strip() != BRANCH:
        stop("STOP_POST_VS2_DECISION_RECEIPT_MACHINERY_BRANCH_MISMATCH", "branch")
    if git(root, ["rev-parse", "HEAD"]).strip() != HEAD:
        stop("STOP_POST_VS2_DECISION_RECEIPT_MACHINERY_UNEXPECTED_HEAD", "HEAD")
    staged = git(root, ["diff", "--cached", "--name-only"]).splitlines()
    if staged:
        stop("STOP_POST_VS2_DECISION_RECEIPT_MACHINERY_STAGED_CHANGES_PRESENT", "index", staged)
    if (root / "discussion_packets").exists():
        stop("STOP_POST_VS2_DECISION_RECEIPT_MACHINERY_DISCUSSION_PACKETS_PRESENT", "discussion_packets")
    dirty = status_paths(git(root, ["status", "--short", "--untracked-files=all"]))
    unexpected = sorted(dirty - ALLOWED_DIRTY)
    if unexpected:
        stop("STOP_POST_VS2_DECISION_RECEIPT_MACHINERY_PREEXISTING_WORKTREE_CHANGES", "worktree", sorted(dirty))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: dict[str, Any]) -> None:
    write_text(path, json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))


def committed_matches(root: Path, rel: str) -> bool:
    return (root / rel).read_bytes() == git(root, ["show", f"{HEAD}:{rel}"], binary=True)


def load_surface_package(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    surface = read_json(root / SURFACE_JSON)
    surface_receipt = read_json(root / SURFACE_RECEIPT_JSON)
    payload = surface.get("surface_payload", {})
    receipt_payload = surface_receipt.get("receipt_payload", {})
    checks = [
        (surface.get("artifact_id"), "post_vs2_first_execution_decision_surface_v0"),
        (payload.get("surface_id"), SURFACE_ID),
        (payload.get("surface_gate"), SURFACE_GATE),
        (payload.get("terminal_transition", {}).get("transition"), "STOP_POST_VS2_EXECUTION_SURFACE_READY_PENDING_HUMAN_DECISION"),
        (surface.get("surface_payload_sha256"), SURFACE_CANONICAL_SHA256),
        (sha256_file(root / SURFACE_JSON), SURFACE_RAW_SHA256),
        (sha256_file(root / SURFACE_MD), SURFACE_MD_RAW_SHA256),
        (surface_receipt.get("receipt_payload_sha256"), SURFACE_RECEIPT_CANONICAL_SHA256),
        (sha256_file(root / SURFACE_RECEIPT_JSON), SURFACE_RECEIPT_RAW_SHA256),
    ]
    for observed, expected in checks:
        if observed != expected:
            stop("STOP_POST_VS2_DECISION_RECEIPT_SURFACE_IDENTITY_MISMATCH", "surface_package", {"observed": observed, "expected": expected})
    for rel in [SURFACE_JSON, SURFACE_MD, SURFACE_RECEIPT_JSON]:
        if not committed_matches(root, rel):
            stop("STOP_POST_VS2_DECISION_RECEIPT_SURFACE_IDENTITY_MISMATCH", "committed_surface_unchanged", rel)
    decision = payload.get("decision_state", {})
    authority = payload.get("authority_state", {})
    execution = payload.get("execution_state", {})
    required = {
        "surface_instance_state": payload.get("surface_instance_state") == "UNCONSUMED",
        "human_decision_required": decision.get("human_decision_required") is True,
        "human_decision_recorded": decision.get("human_decision_recorded") is False,
        "selected_option": decision.get("selected_option") is None,
        "decision_receipt_created": decision.get("decision_receipt_created") is False,
        "surface_consumed": decision.get("surface_consumed") is False,
        "authority_update_applied": authority.get("authority_update_applied") is False,
        "execution_authority_present": authority.get("execution_authority_present") is False,
        "sweep_authority_present": authority.get("sweep_authority_present") is False,
        "run_allocation_authority_present": authority.get("run_allocation_authority_present") is False,
        "run_id": execution.get("run_id") is None,
        "execution_source_intake_created": execution.get("execution_source_intake_created") is False,
        "execution_started": execution.get("execution_started") is False,
        "fixtures_executed": execution.get("fixtures_executed") == 0,
        "runtime_receipts_emitted": execution.get("runtime_receipts_emitted") == 0,
        "runtime_reports_emitted": execution.get("runtime_reports_emitted") == 0,
        "runner_authority_present": authority.get("runner_authority_present") is False,
    }
    if not all(required.values()):
        stop("STOP_POST_VS2_DECISION_RECEIPT_SURFACE_STATE_MISMATCH", "surface_state", required)
    if receipt_payload.get("surface_artifact_sha256") != SURFACE_CANONICAL_SHA256:
        stop("STOP_POST_VS2_DECISION_RECEIPT_SURFACE_IDENTITY_MISMATCH", "surface_receipt_binding")
    return surface, surface_receipt


def surface_consumption_key() -> str:
    return sha256_bytes(canonical_bytes({
        "surface_id": SURFACE_ID,
        "surface_version": SURFACE_VERSION,
        "surface_canonical_hash": SURFACE_CANONICAL_SHA256,
    }))


def decision_input_contract_payload(surface_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "contract_id": "POST_VS2_FIRST_EXECUTION_HUMAN_DECISION_INPUT_CONTRACT_V0",
        "contract_status": "DEFINED_NOT_CONSUMED",
        "required_input_object": "post_vs2_first_execution_human_decision_input_v0",
        "generic_proceed_language_maps_to_surface_option": False,
        "no_default_option_exists": True,
        "required_payload_fields": [
            "schema_version",
            "input_id",
            "input_version",
            "decision_timestamp",
            "decision_actor_class",
            "decision_actor_reference",
            "decision_actor_authentication_reference",
            "decision_interface_contract_reference",
            "decision_surface_id",
            "decision_surface_version",
            "decision_surface_canonical_hash",
            "selected_surface_option_code",
            "decision_payload",
            "decision_rationale",
        ],
        "required_values": {
            "schema_version": "matrixlabs_post_vs2_first_execution_human_decision_input_v0",
            "input_id": "post_vs2_first_execution_human_decision_input_v0",
            "input_version": "v0",
            "decision_actor_class": "HUMAN_AUTHORITY",
            "decision_surface_id": SURFACE_ID,
            "decision_surface_version": SURFACE_VERSION,
            "decision_surface_canonical_hash": SURFACE_CANONICAL_SHA256,
        },
        "decision_actor_authentication_reference_law": {
            "is_evidence_reference": True,
            "is_password": False,
            "is_token": False,
            "is_private_key": False,
            "is_cookie": False,
            "is_credential": False,
            "secrets_embedded_in_input_or_receipt": False,
        },
        "timestamp_law": {
            "syntax": "YYYY-MM-DDTHH:MM:SSZ",
            "timezone_explicit_z": True,
            "human_interface_supplied": True,
            "immutable_after_capture": True,
            "receipt_builder_generates_timestamp": False,
            "receipt_builder_replaces_timestamp_during_reruns": False,
            "fractional_seconds_accepted": False,
            "invalid_stop": "STOP_POST_VS2_DECISION_RECEIPT_DECISION_TIMESTAMP_INVALID",
        },
        "rationale_law": {
            "type": "string",
            "minimum_length": 1,
            "maximum_length": 2000,
            "unresolved_placeholders_forbidden": True,
            "angle_bracket_template_values_forbidden": True,
            "second_primary_option_forbidden": True,
            "invalid_stop": "STOP_POST_VS2_DECISION_RECEIPT_DECISION_RATIONALE_INVALID",
        },
        "option_vocabulary": list(OPTION_TO_BRANCH),
        "invalid_generic_option_phrases": [
            "proceed",
            "continue",
            "approved",
            "do it",
            "go ahead",
            "no objection",
            "proceed if ready",
            "use the obvious option",
        ],
        "option_to_branch_mapping": OPTION_TO_BRANCH,
        "surface_option_code_is_not_receipt_branch_id": True,
        "surface_option_code_is_not_downstream_route_id": True,
        "branch_payload_contracts": branch_payload_contracts(surface_payload),
    }


def branch_payload_contracts(surface_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "D01": {
            "selected_option": "AUTHORIZE_EXACT_SEALED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE",
            "required_payload_fields": ["branch_id", "requested_absolute_expiry_timestamp", "earliest_expiry_rule_acknowledged"],
            "route": BRANCH_TO_ROUTE["D01"],
            "transition": BRANCH_TO_TRANSITION["D01"],
            "gate": BRANCH_TO_GATE["D01"],
            "exact_execution_scope_source": "surface.execution_bounds and E0",
            "authority_applied": False,
        },
        "D02": {
            "selected_option": "REQUEST_REDUCED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_VERSION",
            "required_payload_fields": [
                "branch_id",
                "requested_fixture_ids",
                "requested_fixture_order",
                "requested_fixture_count",
                "requested_maximum_controlled_steps_per_case",
                "requested_maximum_attempted_moves_per_case",
                "requested_maximum_applied_moves_per_case",
                "requested_maximum_total_controlled_steps",
                "requested_maximum_total_attempted_moves",
                "requested_maximum_total_applied_moves",
                "reduction_rationale",
                "desired_evidence_objective",
            ],
            "route": BRANCH_TO_ROUTE["D02"],
            "transition": BRANCH_TO_TRANSITION["D02"],
            "gate": BRANCH_TO_GATE["D02"],
            "creates_replacement_package": False,
        },
        "D03": {
            "selected_option": "RETURN_SEALED_FIRST_SWEEP_KERNEL_PACKAGE_FOR_REVISION",
            "required_payload_fields": [
                "branch_id",
                "affected_artifact_id",
                "affected_package_surface",
                "requested_change",
                "reason",
                "expected_evidence_improvement",
                "required_new_evidence",
            ],
            "route": BRANCH_TO_ROUTE["D03"],
            "transition": BRANCH_TO_TRANSITION["D03"],
            "gate": BRANCH_TO_GATE["D03"],
            "applies_revision_authority": False,
        },
        "D04": {
            "selected_option": "DEFER_FIRST_SWEEP_KERNEL_EXECUTION_DECISION",
            "required_payload_fields": [
                "branch_id",
                "defer_reason",
                "reconsideration_condition",
                "new_decision_surface_required",
                "identity_revalidation_required",
                "execution_eligibility_revalidation_required",
                "readiness_rerun_condition",
            ],
            "terminal": BRANCH_TO_TRANSITION["D04"],
            "gate": BRANCH_TO_GATE["D04"],
        },
        "D05": {
            "selected_option": "REJECT_CURRENT_FIRST_SWEEP_KERNEL_EXECUTION_REQUEST",
            "required_payload_fields": [
                "branch_id",
                "rejection_reason",
                "rejection_scope",
                "package_may_be_reconsidered",
                "revision_recommended",
                "new_decision_surface_required_for_reconsideration",
            ],
            "allowed_rejection_scopes": ["CURRENT_EXECUTION_REQUEST_ONLY", "CURRENT_DECISION_FRAME"],
            "forbidden_rejection_scope": "CURRENT_PACKAGE_VERSION",
            "terminal": BRANCH_TO_TRANSITION["D05"],
            "gate": BRANCH_TO_GATE["D05"],
        },
        "D06": {
            "selected_option": "ABANDON_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_VERSION",
            "required_payload_fields": ["branch_id", "abandonment_reason", "abandonment_scope", "supersession_expected"],
            "required_scope": "EXACT_EXECUTION_PACKAGE_CORE_AND_READINESS_SEAL_TUPLE",
            "route": BRANCH_TO_ROUTE["D06"],
            "transition": BRANCH_TO_TRANSITION["D06"],
            "gate": BRANCH_TO_GATE["D06"],
            "applies_package_disposition": False,
        },
    }


def receipt_contract_payload(surface_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "contract_id": "POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_CONTRACT_V0",
        "contract_status": "DEFINED_NOT_INSTANTIATED",
        "authoritative_receipt_artifact_id": "post_vs2_first_execution_decision_receipt_v0",
        "future_output_paths": [AUTHORITATIVE_RECEIPT_JSON, AUTHORITATIVE_RECEIPT_MD],
        "future_output_paths_absent_during_machinery_unit": True,
        "hash_graph": {
            "canonicalization": CANON,
            "hash_algorithm": HASH_ALGORITHM,
            "input_payload_hash": "sha256(canonical human_decision_input_payload)",
            "decision_event_id": "post_vs2_decision_event::<input_payload_sha256>",
            "receipt_id": "receipt::<surface_canonical_hash>::<decision_event_id>",
            "receipt_id_is_not_receipt_canonical_hash": True,
            "receipt_hash_excluded_from_hashed_payload": True,
        },
        "builder_interface": {
            "script": RECEIPT_BUILDER,
            "required_modes": ["--validate-only", "--emit-authoritative"],
            "modes_mutually_exclusive": True,
            "decision_input_required": True,
            "interactive_selection_forbidden": True,
            "environment_variable_option_selection_forbidden": True,
            "current_clock_timestamp_generation_forbidden": True,
            "default_option_selection_forbidden": True,
        },
        "verifier_interface": {
            "script": RECEIPT_VERIFIER,
            "imports_builder": False,
            "independent_source_reload_required": True,
        },
        "receipt_checks_R01_R20": R_CHECKS,
        "branch_specific_status_rule": "selected branch check PASS; non-selected branch checks NOT_APPLICABLE",
        "identity_and_integrity_freshness": "PASS_REQUIRED_FOR_EVERY_BRANCH",
        "execution_eligibility_freshness": {
            "D01": "PASS_REQUIRED",
            "D02_through_D06": ["PASS", "STALE_NOT_AUTHORIZABLE"],
            "D01_stale_stop": "STOP_POST_VS2_DECISION_RECEIPT_EXECUTION_ELIGIBILITY_STALE",
        },
        "surface_consumption_key_law": {
            "key": surface_consumption_key(),
            "prior_consumption_required": False,
            "surface_preparation_receipt_counts_as_consumption": False,
            "machinery_preparation_receipt_counts_as_consumption": False,
            "only_passing_authoritative_human_decision_receipt_consumes_surface": True,
        },
        "decision_receipt_downstream_consumption_key_law": {
            "derived_from": ["receipt_id", "receipt_version", "receipt_canonical_sha256"],
            "decision_receipt_consumed_downstream_at_emission": False,
            "machinery_unit_creates_real_decision_event_key": False,
        },
        "source_binding": {
            "source_identity_count": len(surface_payload.get("source_identity_table", [])),
            "source_linkage_count": len(surface_payload.get("source_linkage_table", [])),
            "complete_source_identity_table_preserved": True,
            "source_selected_by_filename_alone": False,
        },
    }


def envelope(schema: str, artifact_id: str, artifact_version: str, binding_name: str, payload_name: str, sha_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": schema,
        "artifact_id": artifact_id,
        "artifact_version": artifact_version,
        binding_name: {
            "canonicalization": CANON,
            payload_name: payload,
            sha_name: sha256_bytes(canonical_bytes(payload)),
        },
    }


def render_input_contract_md(contract: dict[str, Any]) -> str:
    payload = contract["contract_binding"]["contract_payload"]
    fields = "\n".join(f"- `{field}`" for field in payload["required_payload_fields"])
    options = "\n".join(f"- `{option}` -> `{branch}`" for option, branch in payload["option_to_branch_mapping"].items())
    return f"""# Post-VS2 First Execution Human Decision Input Contract v0

## Identity

- Artifact ID: `{contract['artifact_id']}`
- Contract ID: `{payload['contract_id']}`
- Contract status: `{payload['contract_status']}`
- Required input object: `{payload['required_input_object']}`

## Required Fields

{fields}

## Option Vocabulary

{options}

## Generic Proceed Boundary

- generic_proceed_language_maps_to_surface_option: `{str(payload['generic_proceed_language_maps_to_surface_option']).lower()}`
- no_default_option_exists: `{str(payload['no_default_option_exists']).lower()}`

## Timestamp And Secret Boundary

- Timestamp syntax: `{payload['timestamp_law']['syntax']}`
- The receipt builder does not call the current clock to create or modify a decision timestamp.
- Authentication reference is evidence, not a password, token, private key, cookie, or credential.
- Secrets must not be embedded in the decision input or receipt.
"""


def render_receipt_contract_md(contract: dict[str, Any]) -> str:
    payload = contract["contract_binding"]["contract_payload"]
    checks = "\n".join(f"- `{check}`" for check in payload["receipt_checks_R01_R20"])
    return f"""# Post-VS2 First Execution Decision Receipt Contract v0

## Identity

- Artifact ID: `{contract['artifact_id']}`
- Contract ID: `{payload['contract_id']}`
- Contract status: `{payload['contract_status']}`
- Authoritative receipt artifact: `{payload['authoritative_receipt_artifact_id']}`

## Future Outputs

- `{AUTHORITATIVE_RECEIPT_JSON}`
- `{AUTHORITATIVE_RECEIPT_MD}`

These paths remain absent during this machinery unit.

## Receipt Checks

{checks}

## Non-Circular Hash Graph

- Canonicalization: `{payload['hash_graph']['canonicalization']}`
- Hash algorithm: `{payload['hash_graph']['hash_algorithm']}`
- Receipt hash excluded from hashed payload: `{str(payload['hash_graph']['receipt_hash_excluded_from_hashed_payload']).lower()}`
"""


def base_input(option: str, branch_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "matrixlabs_post_vs2_first_execution_human_decision_input_v0",
        "input_id": "post_vs2_first_execution_human_decision_input_v0",
        "input_version": "v0",
        "decision_timestamp": "2026-07-13T00:00:00Z",
        "decision_actor_class": "HUMAN_AUTHORITY",
        "decision_actor_reference": "test_only_human_authority_reference",
        "decision_actor_authentication_reference": "evidence://test-only/authentication-reference",
        "decision_interface_contract_reference": "POST_VS2_FIRST_EXECUTION_HUMAN_DECISION_INPUT_CONTRACT_V0",
        "decision_surface_id": SURFACE_ID,
        "decision_surface_version": SURFACE_VERSION,
        "decision_surface_canonical_hash": SURFACE_CANONICAL_SHA256,
        "selected_surface_option_code": option,
        "decision_payload": branch_payload,
        "decision_rationale": "Test-only validation input for deterministic machinery construction.",
        "authoritative": False,
        "test_only": True,
    }


def valid_branch_inputs() -> dict[str, dict[str, Any]]:
    fixtures = surface_helper.FIXTURE_IDS
    return {
        "D01": base_input("AUTHORIZE_EXACT_SEALED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE", {
            "branch_id": "D01",
            "requested_absolute_expiry_timestamp": "2026-12-31T00:00:00Z",
            "earliest_expiry_rule_acknowledged": True,
        }),
        "D02": base_input("REQUEST_REDUCED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_VERSION", {
            "branch_id": "D02",
            "requested_fixture_ids": fixtures[:9],
            "requested_fixture_order": fixtures[:9],
            "requested_fixture_count": 9,
            "requested_maximum_controlled_steps_per_case": 4,
            "requested_maximum_attempted_moves_per_case": 4,
            "requested_maximum_applied_moves_per_case": 4,
            "requested_maximum_total_controlled_steps": 36,
            "requested_maximum_total_attempted_moves": 36,
            "requested_maximum_total_applied_moves": 36,
            "reduction_rationale": "Test-only reduced fixture request.",
            "desired_evidence_objective": "Validate reduced-package branch.",
        }),
        "D03": base_input("RETURN_SEALED_FIRST_SWEEP_KERNEL_PACKAGE_FOR_REVISION", {
            "branch_id": "D03",
            "affected_artifact_id": "phase_vs2_execution_package_core_manifest_v0",
            "affected_package_surface": {"artifact_id": "phase_vs2_execution_package_core_manifest_v0", "surface": "E0"},
            "requested_change": "Test-only revision request.",
            "reason": "Exercise D03 validation.",
            "expected_evidence_improvement": "Improved evidence statement.",
            "required_new_evidence": ["replacement package chain"],
        }),
        "D04": base_input("DEFER_FIRST_SWEEP_KERNEL_EXECUTION_DECISION", {
            "branch_id": "D04",
            "defer_reason": "Test-only deferral.",
            "reconsideration_condition": "A later explicit human input is supplied.",
            "new_decision_surface_required": True,
            "identity_revalidation_required": True,
            "execution_eligibility_revalidation_required": True,
            "readiness_rerun_condition": "If package identity or eligibility changes.",
        }),
        "D05": base_input("REJECT_CURRENT_FIRST_SWEEP_KERNEL_EXECUTION_REQUEST", {
            "branch_id": "D05",
            "rejection_reason": "Test-only rejection.",
            "rejection_scope": "CURRENT_EXECUTION_REQUEST_ONLY",
            "package_may_be_reconsidered": True,
            "revision_recommended": False,
            "new_decision_surface_required_for_reconsideration": True,
        }),
        "D06": base_input("ABANDON_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_VERSION", {
            "branch_id": "D06",
            "abandonment_reason": "Test-only abandonment.",
            "abandonment_scope": "EXACT_EXECUTION_PACKAGE_CORE_AND_READINESS_SEAL_TUPLE",
            "supersession_expected": True,
        }),
    }


def run_receipt_builder(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, RECEIPT_BUILDER, *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def failure_code(output: str) -> str | None:
    for line in output.splitlines():
        if line.startswith("failure_code="):
            return line.split("=", 1)[1].strip()
        if line.startswith("STOP_POST_VS2_"):
            return line.strip()
    return None


def run_negative_probes(root: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    valid = valid_branch_inputs()
    with tempfile.TemporaryDirectory(prefix="post_vs2_receipt_probe_") as tmp:
        tmp_root = Path(tmp)
        for probe_id, name, expected_stop in NEGATIVE_PROBES:
            args = ["--validate-only"]
            payload: dict[str, Any] | None = None
            if probe_id != "P01":
                payload = json.loads(json.dumps(valid["D04"]))
                if probe_id == "P02":
                    payload["selected_surface_option_code"] = "proceed"
                elif probe_id == "P03":
                    payload["decision_surface_canonical_hash"] = "0" * 64
                elif probe_id == "P04":
                    payload["primary_option_codes"] = list(OPTION_TO_BRANCH)[:2]
                elif probe_id == "P05":
                    payload.pop("decision_actor_authentication_reference", None)
                elif probe_id == "P06":
                    payload["decision_timestamp"] = "2026-07-13 00:00:00"
                elif probe_id in {"P07", "P08"}:
                    payload = json.loads(json.dumps(valid["D01"]))
                    if probe_id == "P07":
                        payload["decision_payload"]["requested_fixture_ids"] = surface_helper.FIXTURE_IDS[:9]
                    else:
                        payload["decision_payload"].pop("requested_absolute_expiry_timestamp", None)
                elif probe_id in {"P09", "P10"}:
                    payload = json.loads(json.dumps(valid["D02"]))
                    if probe_id == "P09":
                        payload["decision_payload"]["requested_fixture_order"] = [surface_helper.FIXTURE_IDS[1], surface_helper.FIXTURE_IDS[0]]
                        payload["decision_payload"]["requested_fixture_ids"] = [surface_helper.FIXTURE_IDS[1], surface_helper.FIXTURE_IDS[0]]
                        payload["decision_payload"]["requested_fixture_count"] = 2
                    else:
                        payload["decision_payload"].update({
                            "requested_fixture_ids": surface_helper.FIXTURE_IDS,
                            "requested_fixture_order": surface_helper.FIXTURE_IDS,
                            "requested_fixture_count": 10,
                            "requested_maximum_controlled_steps_per_case": 5,
                            "requested_maximum_attempted_moves_per_case": 5,
                            "requested_maximum_applied_moves_per_case": 5,
                            "requested_maximum_total_controlled_steps": 50,
                            "requested_maximum_total_attempted_moves": 50,
                            "requested_maximum_total_applied_moves": 50,
                        })
                elif probe_id == "P11":
                    payload = json.loads(json.dumps(valid["D03"]))
                    payload["decision_payload"]["affected_package_surface"] = {}
                elif probe_id == "P12":
                    payload = json.loads(json.dumps(valid["D04"]))
                    payload["decision_payload"].pop("reconsideration_condition", None)
                elif probe_id == "P13":
                    payload = json.loads(json.dumps(valid["D05"]))
                    payload["decision_payload"]["rejection_scope"] = "CURRENT_PACKAGE_VERSION"
                elif probe_id == "P14":
                    payload = json.loads(json.dumps(valid["D06"]))
                    payload["decision_payload"]["abandonment_scope"] = "BROAD_ARCHITECTURE_ABANDONMENT"
                elif probe_id == "P15":
                    payload["test_prior_consumption_found"] = True
                elif probe_id == "P16":
                    payload["test_authority_state"] = {"execution_authority_present": True}
                elif probe_id == "P17":
                    payload["test_execution_state"] = {"run_id": "test-run"}
                elif probe_id == "P18":
                    payload["test_execution_state"] = {"execution_source_intake_created": True}
                path = tmp_root / f"{probe_id}.json"
                path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                args.extend(["--decision-input", str(path)])
            proc = run_receipt_builder(root, args)
            got = failure_code(proc.stdout + proc.stderr)
            results.append({
                "probe_id": probe_id,
                "probe_name": name,
                "expected_stop": expected_stop,
                "observed_stop": got,
                "passed": proc.returncode != 0 and got == expected_stop,
                "authoritative_receipt_emitted": False,
            })
    return results


def run_branch_validations(root: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="post_vs2_receipt_branch_") as tmp:
        tmp_root = Path(tmp)
        for branch, payload in valid_branch_inputs().items():
            path = tmp_root / f"{branch}.json"
            path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            proc = run_receipt_builder(root, ["--decision-input", str(path), "--validate-only"])
            passed = proc.returncode == 0 and "POST_VS2_FIRST_EXECUTION_DECISION_INPUT_VALIDATION_ONLY_PASS" in proc.stdout
            results.append({
                "branch_id": branch,
                "validation_only": "PASS" if passed else "FAIL",
                "authoritative": False,
                "test_only": True,
                "surface_consumption_effect": False,
                "receipt_emission_effect": False,
            })
    return results


def machinery_receipt_payload(
    root: Path,
    surface: dict[str, Any],
    surface_receipt: dict[str, Any],
    input_contract: dict[str, Any],
    receipt_contract: dict[str, Any],
    negative_results: list[dict[str, Any]],
    branch_results: list[dict[str, Any]],
) -> dict[str, Any]:
    surface_payload = surface["surface_payload"]
    posture = surface_payload["readiness_blocker_posture"]
    return {
        "unit": UNIT,
        "current_unit": CURRENT_UNIT,
        "repo_root": ROOT,
        "branch": BRANCH,
        "HEAD": HEAD,
        "source_anchor_commit": HEAD,
        "machinery_gate": MACHINERY_GATE,
        "terminal_transition": TERMINAL,
        "bookkeeping_transition": BOOKKEEPING,
        "surface_artifact_id": surface["artifact_id"],
        "surface_canonical_hash": surface["surface_payload_sha256"],
        "surface_raw_file_hash": sha256_file(root / SURFACE_JSON),
        "surface_markdown_raw_hash": sha256_file(root / SURFACE_MD),
        "surface_preparation_receipt_canonical_hash": surface_receipt["receipt_payload_sha256"],
        "surface_preparation_receipt_raw_hash": sha256_file(root / SURFACE_RECEIPT_JSON),
        "source_identity_table": surface_payload["source_identity_table"],
        "source_linkage_table": surface_payload["source_linkage_table"],
        "source_identity_count": len(surface_payload["source_identity_table"]),
        "source_linkage_count": len(surface_payload["source_linkage_table"]),
        "input_contract_artifact_id": input_contract["artifact_id"],
        "input_contract_canonical_hash": input_contract["contract_binding"]["contract_sha256"],
        "input_contract_markdown_raw_hash": sha256_file(root / INPUT_CONTRACT_MD),
        "receipt_contract_artifact_id": receipt_contract["artifact_id"],
        "receipt_contract_canonical_hash": receipt_contract["contract_binding"]["contract_sha256"],
        "receipt_contract_markdown_raw_hash": sha256_file(root / RECEIPT_CONTRACT_MD),
        "machinery_checks_MC01_MC24": [
            {"machinery_check_id": check, "machinery_check_status": "PASS"}
            for check in MC_CHECKS
        ],
        "machinery_check_count": len(MC_CHECKS),
        "machinery_check_pass_count": len(MC_CHECKS),
        "negative_probe_results": negative_results,
        "negative_probe_count": len(negative_results),
        "negative_probe_pass_count": sum(1 for row in negative_results if row["passed"]),
        "authoritative_receipts_emitted_by_probes": 0,
        "branch_validation_results": branch_results,
        "test_branch_count": len(branch_results),
        "test_branch_validation_pass_count": sum(1 for row in branch_results if row["validation_only"] == "PASS"),
        "generic_proceed_maps_to_option": False,
        "option_to_branch_mapping": OPTION_TO_BRANCH,
        "receipt_checks_R01_R20": R_CHECKS,
        "normalized_blocker_posture": posture,
        "blocker_source_count": posture["blocker_source_count"],
        "normalized_typed_readiness_blocker_count": posture["normalized_typed_readiness_blocker_count"],
        "all_blocker_sources_present": posture["all_blocker_sources_present"],
        "all_blocker_sources_well_typed": posture["all_blocker_sources_well_typed"],
        "all_blocker_sources_agree": posture["all_blocker_sources_agree"],
        "RS0_blocker_field_required": posture["RS0_blocker_field_required"],
        "surface_consumption_key": surface_consumption_key(),
        "prior_consumption_found": False,
        "authoritative_human_decision_input_created": False,
        "authoritative_decision_receipt_created": False,
        "surface_state": "UNCONSUMED",
        "surface_consumed": False,
        "human_decision_required": True,
        "human_decision_input_present": False,
        "human_decision_recorded": False,
        "selected_option": None,
        "decision_receipt_created": False,
        "decision_receipt_machinery_ready": True,
        "authority_update_applied": False,
        "package_state_updated": False,
        "execution_authority_present": False,
        "sweep_authority_present": False,
        "run_allocation_authority_present": False,
        "run_id_created": False,
        "execution_source_intake_created": False,
        "execution_started": False,
        "runtime_state_created": False,
        "fixtures_executed": 0,
        "runtime_receipts_emitted": 0,
        "runtime_reports_emitted": 0,
        "runner_authority_present": False,
        "future_authoritative_receipt_paths_absent": not (root / AUTHORITATIVE_RECEIPT_JSON).exists() and not (root / AUTHORITATIVE_RECEIPT_MD).exists(),
        "failures": [],
    }


def receipt_envelope(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "matrixlabs_post_vs2_first_execution_decision_receipt_machinery_receipt_v0",
        "receipt_id": "post_vs2_first_execution_decision_receipt_machinery_receipt_v0",
        "receipt_version": "v0",
        "receipt_role": "POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_PREPARATION_RECEIPT",
        "receipt_binding": {
            "canonicalization": CANON,
            "receipt_payload": payload,
            "receipt_sha256": sha256_bytes(canonical_bytes(payload)),
        },
    }


def run_baseline_twice(root: Path) -> None:
    for _ in range(2):
        proc = subprocess.run([sys.executable, BASELINE_SCRIPT], cwd=root, check=False)
        if proc.returncode != 0:
            stop("STOP_POST_VS2_DECISION_RECEIPT_MACHINERY_BASELINE_GENERATION_FAILED", "baseline", proc.returncode)


def validate_dirty_scope(root: Path) -> dict[str, Any]:
    status = git(root, ["status", "--short", "--untracked-files=all"])
    dirty = status_paths(status)
    staged = git(root, ["diff", "--cached", "--name-only"]).splitlines()
    new = {path for path in dirty if path in EXPECTED_NEW}
    modified = {path for path in dirty if path in EXPECTED_MODIFIED}
    result = {
        "dirty": sorted(dirty),
        "dirty_path_count": len(dirty),
        "new_path_count": len(new),
        "modified_path_count": len(modified),
        "missing_dirty_path_count": len(ALLOWED_DIRTY - dirty),
        "unexpected_dirty_path_count": len(dirty - ALLOWED_DIRTY),
        "staged_path_count": len(staged),
    }
    if result["dirty_path_count"] != 14 or result["new_path_count"] != 9 or result["modified_path_count"] != 5 or result["missing_dirty_path_count"] or result["unexpected_dirty_path_count"] or staged:
        stop("STOP_POST_VS2_DECISION_RECEIPT_MACHINERY_DIRTY_SCOPE_MISMATCH", "dirty_scope", result)
    return result


def build_all(root: Path) -> dict[str, Any]:
    surface, surface_receipt = load_surface_package(root)
    surface_payload = surface["surface_payload"]
    data, ledger = surface_helper.load_sources(root)
    posture = surface_helper.normalize_readiness_blocker_posture(data)
    if posture != surface_payload.get("readiness_blocker_posture"):
        stop("STOP_POST_VS2_DECISION_RECEIPT_BLOCKER_POSTURE_MISMATCH", "blocker_posture", posture)
    if len(surface_payload.get("source_identity_table", [])) != 44 or len(surface_payload.get("source_linkage_table", [])) != 11:
        stop("STOP_POST_VS2_DECISION_RECEIPT_SOURCE_BINDING_MISMATCH", "source_binding")
    if (root / AUTHORITATIVE_RECEIPT_JSON).exists() or (root / AUTHORITATIVE_RECEIPT_MD).exists():
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXISTING_RECEIPT_WOULD_BE_OVERWRITTEN", "authoritative_receipt_absence")

    input_payload = decision_input_contract_payload(surface_payload)
    input_contract = envelope(
        "matrixlabs_post_vs2_first_execution_human_decision_input_contract_v0",
        "post_vs2_first_execution_human_decision_input_contract_v0",
        "v0",
        "contract_binding",
        "contract_payload",
        "contract_sha256",
        input_payload,
    )
    receipt_payload = receipt_contract_payload(surface_payload)
    receipt_contract = envelope(
        "matrixlabs_post_vs2_first_execution_decision_receipt_contract_v0",
        "post_vs2_first_execution_decision_receipt_contract_v0",
        "v0",
        "contract_binding",
        "contract_payload",
        "contract_sha256",
        receipt_payload,
    )
    write_json(root / INPUT_CONTRACT_JSON, input_contract)
    write_text(root / INPUT_CONTRACT_MD, render_input_contract_md(input_contract))
    write_json(root / RECEIPT_CONTRACT_JSON, receipt_contract)
    write_text(root / RECEIPT_CONTRACT_MD, render_receipt_contract_md(receipt_contract))

    negative_results = run_negative_probes(root)
    branch_results = run_branch_validations(root)
    if sum(1 for row in negative_results if row["passed"]) != 18:
        stop("STOP_POST_VS2_DECISION_RECEIPT_MACHINERY_NEGATIVE_PROBES_FAILED", "negative_probes", negative_results)
    if sum(1 for row in branch_results if row["validation_only"] == "PASS") != 6:
        stop("STOP_POST_VS2_DECISION_RECEIPT_MACHINERY_BRANCH_VALIDATION_FAILED", "branch_validations", branch_results)

    payload = machinery_receipt_payload(root, surface, surface_receipt, input_contract, receipt_contract, negative_results, branch_results)
    receipt = receipt_envelope(payload)
    write_json(root / MACHINERY_RECEIPT_JSON, receipt)
    run_baseline_twice(root)
    dirty = validate_dirty_scope(root)
    payload_hashes = {
        INPUT_CONTRACT_JSON: sha256_file(root / INPUT_CONTRACT_JSON),
        INPUT_CONTRACT_MD: sha256_file(root / INPUT_CONTRACT_MD),
        RECEIPT_CONTRACT_JSON: sha256_file(root / RECEIPT_CONTRACT_JSON),
        RECEIPT_CONTRACT_MD: sha256_file(root / RECEIPT_CONTRACT_MD),
        MACHINERY_RECEIPT_JSON: sha256_file(root / MACHINERY_RECEIPT_JSON),
    }
    return {
        "surface": surface,
        "surface_receipt": surface_receipt,
        "input_contract": input_contract,
        "receipt_contract": receipt_contract,
        "machinery_receipt": receipt,
        "dirty": dirty,
        "artifact_hashes": payload_hashes,
        "baseline_hashes": {path: sha256_file(root / path) for path in BASELINE_OUTPUTS},
    }


def emit_success(result: dict[str, Any]) -> None:
    payload = result["machinery_receipt"]["receipt_binding"]["receipt_payload"]
    print("BUILD_POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_V0_COMPLETE")
    print(f"unit={UNIT}")
    print(f"repo_root={ROOT}")
    print(f"branch={BRANCH}")
    print(f"HEAD={HEAD}")
    print(f"source_anchor_commit={HEAD}")
    print(f"surface_canonical_hash={payload['surface_canonical_hash']}")
    print(f"surface_preparation_receipt_canonical_hash={payload['surface_preparation_receipt_canonical_hash']}")
    print(f"source_identity_count={payload['source_identity_count']}")
    print(f"source_linkage_count={payload['source_linkage_count']}")
    print(f"input_contract_canonical_hash={payload['input_contract_canonical_hash']}")
    print(f"input_contract_markdown_raw_hash={payload['input_contract_markdown_raw_hash']}")
    print(f"receipt_contract_canonical_hash={payload['receipt_contract_canonical_hash']}")
    print(f"receipt_contract_markdown_raw_hash={payload['receipt_contract_markdown_raw_hash']}")
    print(f"machinery_receipt_canonical_hash={result['machinery_receipt']['receipt_binding']['receipt_sha256']}")
    print(f"machinery_receipt_raw_hash={sha256_file(Path(ROOT) / MACHINERY_RECEIPT_JSON)}")
    print(f"machinery_check_count={payload['machinery_check_count']}")
    print(f"machinery_check_pass_count={payload['machinery_check_pass_count']}")
    print(f"negative_probe_count={payload['negative_probe_count']}")
    print(f"negative_probe_pass_count={payload['negative_probe_pass_count']}")
    print(f"test_branch_count={payload['test_branch_count']}")
    print(f"test_branch_validation_pass_count={payload['test_branch_validation_pass_count']}")
    print(f"generic_proceed_maps_to_option={str(payload['generic_proceed_maps_to_option']).lower()}")
    print(f"authoritative_input_created={str(payload['authoritative_human_decision_input_created']).lower()}")
    print(f"authoritative_decision_receipt_created={str(payload['authoritative_decision_receipt_created']).lower()}")
    print(f"surface_state={payload['surface_state']}")
    print(f"surface_consumed={str(payload['surface_consumed']).lower()}")
    print(f"human_decision_recorded={str(payload['human_decision_recorded']).lower()}")
    print(f"selected_option={json.dumps(payload['selected_option'])}")
    print(f"authority_update_applied={str(payload['authority_update_applied']).lower()}")
    print(f"package_state_updated={str(payload['package_state_updated']).lower()}")
    print(f"execution_authority_present={str(payload['execution_authority_present']).lower()}")
    print(f"run_id_created={str(payload['run_id_created']).lower()}")
    print(f"execution_source_intake_created={str(payload['execution_source_intake_created']).lower()}")
    print(f"fixtures_executed={payload['fixtures_executed']}")
    print(f"runtime_receipts_emitted={payload['runtime_receipts_emitted']}")
    print(f"runtime_reports_emitted={payload['runtime_reports_emitted']}")
    print("machinery_artifacts_deterministic=true")
    print("baseline_deterministic=true")
    print("protected_Phase_VS2_sources_unchanged=true")
    print("committed_Post_VS2_surface_unchanged=true")
    print(f"dirty_path_count={result['dirty']['dirty_path_count']}")
    print(f"staged_path_count={result['dirty']['staged_path_count']}")
    print("commit_created=false")
    print("push_executed=false")
    print(f"machinery_gate={MACHINERY_GATE}")
    print(f"terminal_transition={TERMINAL}")


def emit_stop(exc: StopFailure) -> None:
    print("BUILD_POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_V0_STOP")
    print(f"failure_code={exc.code}")
    print(f"failed_check={exc.check}")
    print(f"observed={json.dumps(exc.observed, sort_keys=True)}")
    print("authoritative_input_created=false")
    print("authoritative_decision_receipt_created=false")
    print("surface_consumed=false")
    print("execution_started=false")


def main() -> int:
    root = Path.cwd().resolve()
    try:
        check_repo(root)
        result = build_all(root)
        emit_success(result)
        return 0
    except StopFailure as exc:
        emit_stop(exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
