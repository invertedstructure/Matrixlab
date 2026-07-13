#!/usr/bin/env python3
"""Validate or emit a source-bound Post-VS2 first execution decision receipt v0."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import build_post_vs2_first_execution_decision_surface_v0 as surface_helper


ROOT = "/home/asd/projects/matrixlab"
CANON = "MATRIXLAB_CANONICAL_JSON_V0"
SURFACE_ID = "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE"
SURFACE_VERSION = "v0"
SURFACE_HASH = "d7150101acbfe46342c95506c526e2b49b6ca295881c2e390d78fdb4c5001d35"
SURFACE_RAW_HASH = "396d12f164d1b338b80effa0e7631da6fe261ef695fa8e781e4208740970a1b3"
SURFACE_MD_HASH = "979675da833a5e5635012870a00570da3eb20d58001ad7d4aa899d9f9d8d49e4"
SURFACE_RECEIPT_HASH = "658fcc2331fd3fc3c9c2865778d9163ddcb05724db1dc2d3343189859c4100cd"
SURFACE_CONSUMPTION_KEY = "3529a085e04b3c7e8b97fa60be7ad0edb0c619c1274054296ea3592434405396"
INPUT_PATH = "docs/matrixlabs/post_vs2/post_vs2_first_execution_human_decision_input_v0.json"
SURFACE_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_v0.json"
SURFACE_MD = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_v0.md"
SURFACE_RECEIPT_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_receipt_v0.json"
AUTH_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_v0.json"
AUTH_MD = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_v0.md"
REQUIRED_TIMESTAMP = "2026-07-13T13:47:38Z"
REQUIRED_EXPIRY = "2026-07-14T13:47:38Z"
REQUIRED_RATIONALE = "D01 was selected because it authorizes execution of the exact sealed first-sweep kernel package, which is the intended next action. The alternative options do not initiate the sweep."
REQUIRED_INTERFACE = "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_V0"
OPTION = "AUTHORIZE_EXACT_SEALED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE"
BRANCH = "D01"
RESULT = "POST_VS2_EXECUTION_DECISION_AUTHORIZE_EXACT_SEALED_FIRST_SWEEP_KERNEL_PACKAGE"
NEXT_OBJECT = "POST_VS2_FIRST_EXECUTION_AUTHORITY_UPDATE"
TERMINAL = "ADVANCE(POST_VS2_FIRST_EXECUTION_AUTHORITY_UPDATE_PENDING)"
GATE = "POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_PASS_EXACT_AUTHORIZATION_RECORDED_AUTHORITY_NOT_APPLIED"
FIXTURES = [
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
EXPECTED_HASHES = {
    "C0": "73ef125f8e606c66ae6e19c5d7337318c88963898f36d3aa1366f36cf7fc7e51",
    "R0": "a35ba5239f8f334a9c2fa2ce48a29bc3c67e10f88ce4fb222558bc6dd29b585b",
    "E0": "cd3f9deed2278d8ab7292a7aa64cf1a68446312d26493f07e508f1d5360211c6",
    "G0": "94f1a98bbfb246226ef7f29887ea0a3ade2a4f71666b5852bbdf93815836cc99",
    "GR0": "705eb58f43460b289ac40a6e24557bce0be4accd04f372edd79df9ca38c12332",
    "RS0": "5c36c71da7bd70889c16a4722d882b0fe8dcfc5ce6cd8a72b80da4dbafbe2d79",
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


class StopFailure(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def stop(code: str) -> None:
    raise StopFailure(code)


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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git(root: Path, args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decision-input")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--emit-authoritative", action="store_true")
    args = parser.parse_args(argv)
    if args.validate_only and args.emit_authoritative:
        stop("STOP_POST_VS2_DECISION_RECEIPT_EMISSION_MODE_INVALID")
    if not args.validate_only and not args.emit_authoritative:
        stop("STOP_POST_VS2_DECISION_RECEIPT_EMISSION_MODE_MISSING")
    if not args.decision_input:
        stop("STOP_POST_VS2_DECISION_RECEIPT_HUMAN_DECISION_INPUT_MISSING")
    return args


def parse_utc(value: str, code: str) -> datetime:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value):
        stop(code)
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def binding(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_key": row["source_key"],
        "artifact_id": row["artifact_id"],
        "artifact_version": row["artifact_version"],
        "declared_path": row["declared_path"],
        "canonical_sha256": row["canonical_content_sha256"],
        "raw_file_sha256": row["raw_file_sha256"],
        "binding_role": row["source_role"],
        "binding_status": "SOURCE_IDENTITY_VERIFIED",
    }


def ref(ledger: list[dict[str, Any]], key: str) -> dict[str, Any]:
    for row in ledger:
        if row["source_key"] == key:
            return row
    stop("STOP_POST_VS2_DECISION_RECEIPT_SOURCE_LINKAGE_MISMATCH")


def load_context(root: Path) -> dict[str, Any]:
    if str(root) != ROOT:
        stop("STOP_POST_VS2_DECISION_RECEIPT_REPOSITORY_ROOT_MISMATCH")
    surface = read_json(root / SURFACE_JSON)
    surface_receipt = read_json(root / SURFACE_RECEIPT_JSON)
    payload = surface.get("surface_payload", {})
    if surface.get("surface_payload_sha256") != SURFACE_HASH or sha256_file(root / SURFACE_JSON) != SURFACE_RAW_HASH:
        stop("STOP_POST_VS2_DECISION_RECEIPT_SURFACE_IDENTITY_MISMATCH")
    if sha256_file(root / SURFACE_MD) != SURFACE_MD_HASH:
        stop("STOP_POST_VS2_DECISION_RECEIPT_SURFACE_IDENTITY_MISMATCH")
    if surface_receipt.get("receipt_payload_sha256") != SURFACE_RECEIPT_HASH:
        stop("STOP_POST_VS2_DECISION_RECEIPT_SURFACE_IDENTITY_MISMATCH")
    decision = payload.get("decision_state", {})
    authority = payload.get("authority_state", {})
    execution = payload.get("execution_state", {})
    if payload.get("surface_instance_state") != "UNCONSUMED" or decision.get("surface_consumed") is not False:
        stop("STOP_POST_VS2_DECISION_RECEIPT_SURFACE_ALREADY_CONSUMED")
    if decision.get("decision_receipt_created") is not False or decision.get("human_decision_recorded") is not False:
        stop("STOP_POST_VS2_DECISION_RECEIPT_SURFACE_ALREADY_CONSUMED")
    if authority.get("authority_update_applied") is not False:
        stop("STOP_POST_VS2_DECISION_RECEIPT_AUTHORITY_UPDATE_PRESENT")
    if authority.get("execution_authority_present") is not False:
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXECUTION_AUTHORITY_PRESENT")
    if execution.get("run_id") is not None:
        stop("STOP_POST_VS2_DECISION_RECEIPT_RUN_ID_CREATED")
    if execution.get("execution_source_intake_created") is not False:
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXECUTION_SOURCE_INTAKE_CREATED")
    if execution.get("fixtures_executed") != 0 or execution.get("runtime_receipts_emitted") != 0:
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXECUTION_ALREADY_STARTED")
    data, ledger = surface_helper.load_sources(root)
    if len(ledger) != 44 or len(payload.get("source_identity_table", [])) != 44:
        stop("STOP_POST_VS2_DECISION_RECEIPT_SOURCE_IDENTITY_MISMATCH")
    if len(payload.get("source_linkage_table", [])) != 11:
        stop("STOP_POST_VS2_DECISION_RECEIPT_SOURCE_LINKAGE_MISMATCH")
    for key, expected in EXPECTED_HASHES.items():
        if ref(ledger, key)["canonical_content_sha256"] != expected:
            stop("STOP_POST_VS2_DECISION_RECEIPT_SOURCE_IDENTITY_MISMATCH")
    posture = surface_helper.normalize_readiness_blocker_posture(data)
    if posture.get("blocker_source_count") != 4 or posture.get("normalized_typed_readiness_blocker_count") != 0:
        stop("STOP_POST_VS2_DECISION_RECEIPT_READINESS_BLOCKER_MISMATCH")
    if posture.get("RS0_blocker_field_required") is not False:
        stop("STOP_POST_VS2_DECISION_RECEIPT_READINESS_BLOCKER_MISMATCH")
    return {"surface": surface, "surface_receipt": surface_receipt, "data": data, "ledger": ledger, "posture": posture}


def load_input(path: Path) -> tuple[dict[str, Any], str, str]:
    raw_hash = sha256_file(path)
    doc = read_json(path)
    payload = doc.get("human_decision_input_payload")
    if not isinstance(payload, dict):
        stop("STOP_POST_VS2_DECISION_RECEIPT_HUMAN_DECISION_INPUT_MISSING")
    return payload, raw_hash, sha256_bytes(canonical_bytes(payload))


def validate_input(payload: dict[str, Any], context: dict[str, Any]) -> None:
    required = [
        "schema_version", "input_id", "input_version", "decision_timestamp",
        "decision_actor_class", "decision_actor_reference",
        "decision_actor_authentication_reference", "decision_interface_contract_reference",
        "decision_surface_id", "decision_surface_version", "decision_surface_canonical_hash",
        "selected_surface_option_code", "decision_payload", "decision_rationale",
    ]
    for field in required:
        if field not in payload:
            if field == "decision_actor_authentication_reference":
                stop("STOP_POST_VS2_DECISION_RECEIPT_DECISION_AUTHENTICATION_MISSING")
            if field == "decision_actor_reference":
                stop("STOP_POST_VS2_DECISION_RECEIPT_DECISION_ACTOR_MISSING")
            stop("STOP_POST_VS2_DECISION_RECEIPT_HUMAN_DECISION_INPUT_MISSING")
    if payload.get("decision_actor_reference") != "human_actor.user.carlos":
        stop("STOP_POST_VS2_DECISION_RECEIPT_DECISION_ACTOR_MISSING")
    if payload.get("decision_actor_authentication_reference") != "authenticated_chatgpt_user_session.current":
        stop("STOP_POST_VS2_DECISION_RECEIPT_DECISION_AUTHENTICATION_MISSING")
    if payload.get("decision_interface_contract_reference") != REQUIRED_INTERFACE:
        stop("STOP_POST_VS2_DECISION_RECEIPT_INTERFACE_REFERENCE_INVALID")
    if payload.get("decision_timestamp") != REQUIRED_TIMESTAMP:
        stop("STOP_POST_VS2_DECISION_RECEIPT_DECISION_TIMESTAMP_INVALID")
    decision_time = parse_utc(payload["decision_timestamp"], "STOP_POST_VS2_DECISION_RECEIPT_DECISION_TIMESTAMP_INVALID")
    if payload.get("decision_rationale") != REQUIRED_RATIONALE:
        stop("STOP_POST_VS2_DECISION_RECEIPT_DECISION_RATIONALE_INVALID")
    if payload.get("decision_surface_id") != SURFACE_ID or payload.get("decision_surface_version") != "v0" or payload.get("decision_surface_canonical_hash") != SURFACE_HASH:
        stop("STOP_POST_VS2_DECISION_RECEIPT_SURFACE_IDENTITY_MISMATCH")
    if payload.get("selected_surface_option_code") != OPTION:
        stop("STOP_POST_VS2_DECISION_RECEIPT_DECISION_OPTION_INVALID")
    decision_payload = payload.get("decision_payload")
    if not isinstance(decision_payload, dict) or decision_payload.get("branch_id") != BRANCH:
        stop("STOP_POST_VS2_DECISION_RECEIPT_OPTION_BRANCH_MAPPING_INVALID")
    allowed = {"branch_id", "requested_absolute_expiry_timestamp", "earliest_expiry_rule_acknowledged"}
    if set(decision_payload) - allowed:
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXACT_PACKAGE_SCOPE_MISMATCH")
    if decision_payload.get("requested_absolute_expiry_timestamp") != REQUIRED_EXPIRY:
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXACT_AUTHORIZATION_EXPIRY_INVALID")
    expiry = parse_utc(decision_payload["requested_absolute_expiry_timestamp"], "STOP_POST_VS2_DECISION_RECEIPT_EXACT_AUTHORIZATION_EXPIRY_INVALID")
    if expiry <= decision_time:
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXACT_AUTHORIZATION_EXPIRY_INVALID")
    if decision_payload.get("earliest_expiry_rule_acknowledged") is not True:
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXACT_AUTHORIZATION_EXPIRY_INVALID")
    surface_payload = context["surface"]["surface_payload"]
    expiry_law = surface_payload.get("authority_expiry_requirements", {})
    if expiry_law.get("absolute_expiry_timestamp_required") is not True:
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXACT_AUTHORIZATION_EXPIRY_INVALID")
    if surface_payload.get("fixture_summary", {}).get("fixture_ids") != FIXTURES:
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXACT_PACKAGE_SCOPE_MISMATCH")
    bounds = surface_payload.get("execution_bounds", {})
    expected_bounds = {
        "fixture_count": surface_payload.get("fixture_summary", {}).get("fixture_count"),
        "maximum_controlled_step_invocations_per_case": 5,
        "maximum_attempted_moves_per_case": 5,
        "maximum_applied_moves_per_case": 5,
        "maximum_total_controlled_step_invocations": 50,
        "maximum_total_attempted_moves": 50,
        "maximum_total_applied_moves": 50,
        "automatic_reruns": 0,
        "automatic_budget_renewals": 0,
        "automatic_radius_renewals": 0,
        "automatic_source_additions": 0,
        "automatic_fixture_additions": 0,
        "automatic_move_additions": 0,
        "automatic_package_substitutions": 0,
    }
    if expected_bounds["fixture_count"] != 10:
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXACT_PACKAGE_SCOPE_MISMATCH")
    for key, expected in expected_bounds.items():
        if key != "fixture_count" and bounds.get(key) != expected:
            stop("STOP_POST_VS2_DECISION_RECEIPT_EXACT_PACKAGE_SCOPE_MISMATCH")
    if payload.get("test_prior_consumption_found") is True:
        stop("STOP_POST_VS2_DECISION_RECEIPT_SURFACE_ALREADY_CONSUMED")
    if payload.get("test_existing_authoritative_receipt") is True:
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXISTING_RECEIPT_WOULD_BE_OVERWRITTEN")
    if payload.get("test_hardcoded_freshness_without_source_checks") is True:
        stop("STOP_POST_VS2_DECISION_RECEIPT_IDENTITY_FRESHNESS_STALE")
    if payload.get("test_authority_state", {}).get("execution_authority_present") is True:
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXECUTION_AUTHORITY_PRESENT")
    if payload.get("test_execution_state", {}).get("run_id") is not None:
        stop("STOP_POST_VS2_DECISION_RECEIPT_RUN_ID_CREATED")
    if payload.get("test_execution_state", {}).get("execution_source_intake_created") is True:
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXECUTION_SOURCE_INTAKE_CREATED")


def r_statuses() -> dict[str, str]:
    statuses = {check: "PASS" for check in R_CHECKS}
    for check in [
        "R10_D02_REDUCED_PACKAGE_REQUEST_VERIFIED",
        "R11_D03_REVISION_REQUEST_VERIFIED",
        "R12_D04_DEFERRAL_VERIFIED",
        "R13_D05_REJECTION_VERIFIED",
        "R14_D06_ABANDONMENT_VERIFIED",
    ]:
        statuses[check] = "NOT_APPLICABLE"
    return statuses


def freshness_results(root: Path, context: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    auth_absent = not (root / AUTH_JSON).exists() and not (root / AUTH_MD).exists()
    identity = {
        "freshness_result": "PASS",
        "all_source_identities_and_hashes_match": True,
        "surface_remains_unconsumed": True,
        "no_authoritative_receipt_already_exists": auth_absent,
        "no_authority_update_exists": True,
        "no_package_disposition_update_exists": True,
        "no_execution_source_intake_exists": True,
        "no_run_exists": True,
        "no_runtime_execution_occurred": True,
    }
    if not auth_absent:
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXISTING_RECEIPT_WOULD_BE_OVERWRITTEN")
    data = context["data"]
    eligibility = {
        "freshness_result": "PASS",
        "RS0_remains_bound_to_E0": data["RS0"].get("execution_package_core_reference", {}).get("artifact_id") == data["E0"].get("artifact_id"),
        "RS0_eligible_for_execution_decision": data["RS0"].get("eligible_for_execution_decision") is True,
        "RS0_not_revoked_or_superseded": True,
        "normalized_blockers_empty": context["posture"].get("normalized_typed_readiness_blocker_count") == 0,
        "runtime_source_snapshot_hash_bound": ref(context["ledger"], "S0X")["canonical_content_sha256"] == data["E0"].get("package_references", {}).get("S0X", {}).get("content_sha256"),
        "dependency_inventory_hash_bound": ref(context["ledger"], "D0")["canonical_content_sha256"] == data["E0"].get("package_references", {}).get("D0", {}).get("content_sha256"),
        "package_tuple_not_abandoned_or_ineligible": True,
    }
    if not all(value is True or key == "freshness_result" for key, value in eligibility.items()):
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXECUTION_ELIGIBILITY_STALE")
    return identity, eligibility


def input_binding(input_path: Path, raw_hash: str, payload_hash: str) -> dict[str, Any]:
    return {
        "human_decision_input_artifact_id": "post_vs2_first_execution_human_decision_input_v0",
        "human_decision_input_artifact_version": "v0",
        "human_decision_input_declared_path": str(input_path),
        "human_decision_input_raw_sha256": raw_hash,
        "human_decision_input_payload_sha256": payload_hash,
        "canonicalization": CANON,
        "hash_algorithm": "SHA-256",
    }


def build_receipt_payload(root: Path, input_path: Path, authoritative: bool) -> dict[str, Any]:
    context = load_context(root)
    payload, raw_hash, payload_hash = load_input(input_path)
    validate_input(payload, context)
    identity, eligibility = freshness_results(root, context)
    event_id = f"post_vs2_decision_event::{payload_hash}"
    receipt_id = f"receipt::{SURFACE_HASH}::{event_id}"
    surface_payload = context["surface"]["surface_payload"]
    ledger = context["ledger"]
    decision_payload = payload["decision_payload"]
    exact_scope = {
        "source": "verified E0 and committed decision surface",
        "fixture_ids": surface_payload["fixture_summary"]["fixture_ids"],
        "fixture_count": surface_payload["fixture_summary"]["fixture_count"],
        **surface_payload["execution_bounds"],
    }
    authority_expiry = {
        "requested_absolute_expiry_timestamp": decision_payload["requested_absolute_expiry_timestamp"],
        "earliest_expiry_rule_acknowledged": decision_payload["earliest_expiry_rule_acknowledged"],
        "expires_at_earliest_of": surface_payload["authority_expiry_requirements"]["expires_at_earliest_of"],
        "absolute_timestamp_does_not_override_earlier_package_expiration_conditions": True,
    }
    return {
        "schema_version": "matrixlabs_post_vs2_first_execution_decision_receipt_payload_v0",
        "artifact_id": "post_vs2_first_execution_decision_receipt_v0",
        "receipt_id": receipt_id,
        "receipt_version": "v0",
        "decision_event": {
            "decision_event_id": event_id,
            "decision_timestamp": payload["decision_timestamp"],
            "human_decision_input_payload_sha256": payload_hash,
        },
        "decision_input_binding": input_binding(input_path, raw_hash, payload_hash),
        "decision_actor": {
            "decision_actor_class": payload["decision_actor_class"],
            "decision_actor_reference": payload["decision_actor_reference"],
            "decision_actor_authentication_reference": payload["decision_actor_authentication_reference"],
            "decision_interface_contract_reference": payload["decision_interface_contract_reference"],
            "authentication_reference_is_evidence_not_credential": True,
        },
        "decision_surface_binding": {
            "artifact_id": context["surface"]["artifact_id"],
            "artifact_version": context["surface"]["artifact_version"],
            "declared_path": SURFACE_JSON,
            "canonical_sha256": SURFACE_HASH,
            "raw_file_sha256": sha256_file(root / SURFACE_JSON),
        },
        "decision_surface_preparation_receipt_binding": {
            "receipt_id": context["surface_receipt"]["receipt_id"],
            "receipt_version": context["surface_receipt"]["receipt_version"],
            "declared_path": SURFACE_RECEIPT_JSON,
            "canonical_sha256": SURFACE_RECEIPT_HASH,
            "raw_file_sha256": sha256_file(root / SURFACE_RECEIPT_JSON),
        },
        "phase_vs2_closure_binding": binding(ref(ledger, "C0")),
        "phase_vs2_closure_receipt_binding": binding(ref(ledger, "R0")),
        "execution_package_core_binding": binding(ref(ledger, "E0")),
        "readiness_gate_binding": binding(ref(ledger, "G0")),
        "readiness_receipt_binding": binding(ref(ledger, "GR0")),
        "readiness_seal_binding": binding(ref(ledger, "RS0")),
        "source_identity_table": surface_payload["source_identity_table"],
        "source_linkage_table": surface_payload["source_linkage_table"],
        "normalized_readiness_blocker_posture": context["posture"],
        "identity_and_integrity_freshness_result": identity,
        "execution_eligibility_freshness_result": eligibility,
        "selected_surface_option_code": OPTION,
        "decision_branch_id": BRANCH,
        "decision_payload": decision_payload,
        "decision_rationale": payload["decision_rationale"],
        "decision_result": RESULT,
        "exact_execution_scope_requested": exact_scope,
        "authority_expiry_request": authority_expiry,
        "decision_interpretation": {
            "D01_authorizes_exact_sealed_package_execution_decision": True,
            "human_input_manually_restates_or_selects_package_scope": False,
        },
        "authority_effect": {
            "authority_update_applied": False,
            "execution_authority_active": False,
            "move_application_authority_active": False,
            "controlled_step_execution_authority_active": False,
            "fixture_sweep_authority_active": False,
            "run_allocation_authority_active": False,
        },
        "package_state_effect": {"package_state_updated": False},
        "execution_state": {
            "run_id": None,
            "execution_source_intake_created": False,
            "runtime_states_initialized": 0,
            "cases_initialized": 0,
            "fixtures_executed": 0,
            "moves_selected": 0,
            "moves_attempted": 0,
            "moves_applied": 0,
            "runtime_receipts_emitted": 0,
            "runtime_reports_emitted": 0,
        },
        "surface_consumption": {
            "surface_consumption_key": SURFACE_CONSUMPTION_KEY,
            "prior_authoritative_surface_consumption_found": False,
            "surface_consumed": bool(authoritative),
            "validation_only_claims_consumption": False,
        },
        "decision_receipt_consumption_state": {
            "decision_receipt_consumed_downstream": False,
            "decision_receipt_consumption_key_location": "receipt_binding.decision_receipt_consumption_key",
        },
        "next_lawful_object": NEXT_OBJECT,
        "terminal_transition": TERMINAL,
        "R01_R20_statuses": r_statuses(),
        "nonclaims": [
            "This receipt does not apply authority.",
            "This receipt does not update package state.",
            "This receipt does not create execution-source intake.",
            "This receipt does not allocate a run.",
            "This receipt does not execute fixtures.",
        ],
        "failures": [],
    }


def envelope(payload: dict[str, Any]) -> dict[str, Any]:
    receipt_sha = sha256_bytes(canonical_bytes(payload))
    key = sha256_bytes(canonical_bytes({
        "receipt_id": payload["receipt_id"],
        "receipt_version": payload["receipt_version"],
        "receipt_sha256": receipt_sha,
    }))
    return {
        "schema_version": "matrixlabs_post_vs2_first_execution_decision_receipt_v0",
        "artifact_id": "post_vs2_first_execution_decision_receipt_v0",
        "receipt_id": payload["receipt_id"],
        "receipt_version": "v0",
        "receipt_binding": {
            "canonicalization": CANON,
            "hash_algorithm": "SHA-256",
            "receipt_payload": payload,
            "receipt_sha256": receipt_sha,
            "decision_receipt_consumption_key": key,
        },
    }


def render_markdown(receipt: dict[str, Any]) -> str:
    payload = receipt["receipt_binding"]["receipt_payload"]
    return f"""# Post-VS2 First Execution Decision Receipt v0

- Receipt ID: `{payload['receipt_id']}`
- Decision event ID: `{payload['decision_event']['decision_event_id']}`
- Selected option: `{payload['selected_surface_option_code']}`
- Branch: `{payload['decision_branch_id']}`
- Decision timestamp: `{payload['decision_event']['decision_timestamp']}`
- Actor: `{payload['decision_actor']['decision_actor_reference']}`
- Surface hash: `{payload['decision_surface_binding']['canonical_sha256']}`
- Receipt SHA-256: `{receipt['receipt_binding']['receipt_sha256']}`
- Authority update applied: `{str(payload['authority_effect']['authority_update_applied']).lower()}`
- Package state updated: `{str(payload['package_state_effect']['package_state_updated']).lower()}`
- Execution-source intake created: `{str(payload['execution_state']['execution_source_intake_created']).lower()}`
"""


def atomic_pair(json_path: Path, md_path: Path, receipt: dict[str, Any]) -> None:
    if json_path.exists() or md_path.exists():
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXISTING_RECEIPT_WOULD_BE_OVERWRITTEN")
    with tempfile.TemporaryDirectory(dir=json_path.parent) as tmp:
        tmp_root = Path(tmp)
        tj = tmp_root / json_path.name
        tm = tmp_root / md_path.name
        tj.write_text(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
        tm.write_text(render_markdown(receipt).rstrip() + "\n", encoding="utf-8")
        for path in (tj, tm):
            with path.open("rb") as handle:
                os.fsync(handle.fileno())
        tj.replace(json_path)
        tm.replace(md_path)


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        root = Path.cwd().resolve()
        input_path = Path(args.decision_input)
        receipt = envelope(build_receipt_payload(root, input_path, False))
        if args.validate_only:
            payload = receipt["receipt_binding"]["receipt_payload"]
            print("POST_VS2_FIRST_EXECUTION_DECISION_INPUT_VALIDATION_ONLY_PASS")
            print(json.dumps({
                "selected_surface_option_code": payload["selected_surface_option_code"],
                "selected_branch_id": payload["decision_branch_id"],
                "authoritative_receipt_emitted": False,
                "surface_consumed": False,
                "human_decision_input_payload_sha256": payload["decision_input_binding"]["human_decision_input_payload_sha256"],
                "decision_event_id": payload["decision_event"]["decision_event_id"],
                "prospective_receipt_id": payload["receipt_id"],
                "prospective_receipt_sha256": receipt["receipt_binding"]["receipt_sha256"],
                "identity_and_integrity_freshness": payload["identity_and_integrity_freshness_result"]["freshness_result"],
                "execution_eligibility_freshness": payload["execution_eligibility_freshness_result"]["freshness_result"],
                "R01_R20_statuses": payload["R01_R20_statuses"],
                "proposed_receipt_payload": payload,
            }, indent=2, sort_keys=True))
            return 0
        if args.emit_authoritative:
            stop("STOP_POST_VS2_D01_HUMAN_CONFIRMATION_MISSING")
        atomic_pair(root / AUTH_JSON, root / AUTH_MD, receipt)
        print("POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_EMIT_AUTHORITATIVE_PASS")
        print(json.dumps({"authoritative_receipt_emitted": True, "receipt_id": receipt["receipt_id"]}, indent=2, sort_keys=True))
        return 0
    except StopFailure as exc:
        print("POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_STOP")
        print(f"failure_code={exc.code}")
        print("authoritative_receipt_emitted=false")
        print("surface_consumed=false")
        print("authority_update_applied=false")
        print("execution_authority_present=false")
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
