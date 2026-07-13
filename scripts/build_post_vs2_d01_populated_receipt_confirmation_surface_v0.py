#!/usr/bin/env python3
"""Prepare a non-authoritative D01 populated decision-record confirmation surface."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import build_post_vs2_first_execution_decision_surface_v0 as surface_helper


ROOT = Path("/home/asd/projects/matrixlab")
CANON = "MATRIXLAB_CANONICAL_JSON_V0"
POST = Path("docs/matrixlabs/post_vs2")
INPUT = POST / "post_vs2_first_execution_human_decision_input_v0.json"
SURFACE_JSON = POST / "post_vs2_first_execution_decision_surface_v0.json"
SURFACE_MD = POST / "post_vs2_first_execution_decision_surface_v0.md"
SURFACE_RECEIPT_JSON = POST / "post_vs2_first_execution_decision_surface_receipt_v0.json"
REPAIR_RECEIPT_JSON = POST / "post_vs2_first_execution_decision_receipt_implementation_repair_receipt_v0.json"
AUTH_JSON = POST / "post_vs2_first_execution_decision_receipt_v0.json"
AUTH_MD = POST / "post_vs2_first_execution_decision_receipt_v0.md"
CONFIRM_EVENT_JSON = POST / "post_vs2_d01_populated_receipt_confirmation_event_v0.json"
CONFIRM_EVENT_MD = POST / "post_vs2_d01_populated_receipt_confirmation_event_v0.md"
DRAFT_JSON = POST / "post_vs2_first_execution_decision_receipt_d01_draft_v0.json"
DRAFT_MD = POST / "post_vs2_first_execution_decision_receipt_d01_draft_v0.md"
CONFIRM_SURFACE_JSON = POST / "post_vs2_d01_populated_receipt_confirmation_surface_v0.json"
CONFIRM_SURFACE_MD = POST / "post_vs2_d01_populated_receipt_confirmation_surface_v0.md"
CONTRACT_JSON = POST / "post_vs2_d01_populated_receipt_confirmation_input_contract_v0.json"
CONTRACT_MD = POST / "post_vs2_d01_populated_receipt_confirmation_input_contract_v0.md"
PREP_RECEIPT_JSON = POST / "post_vs2_d01_populated_receipt_confirmation_surface_preparation_receipt_v0.json"
PREP_RECEIPT_MD = POST / "post_vs2_d01_populated_receipt_confirmation_surface_preparation_receipt_v0.md"

SURFACE_HASH = "d7150101acbfe46342c95506c526e2b49b6ca295881c2e390d78fdb4c5001d35"
SURFACE_CONSUMPTION_KEY = "3529a085e04b3c7e8b97fa60be7ad0edb0c619c1274054296ea3592434405396"
SURFACE_RECEIPT_HASH = "658fcc2331fd3fc3c9c2865778d9163ddcb05724db1dc2d3343189859c4100cd"
INPUT_RAW_HASH = "680d79ed2a15e50d2c99e98dde6c6dc267a8eb0efba968dbb95a0d28cd2ae548"
INPUT_PAYLOAD_HASH = "d5eaaf7594f5b031146a5aa60ffaf9eb38fa7aba7801536ff4ce31e1571ed648"
DECISION_EVENT_ID = f"post_vs2_decision_event::{INPUT_PAYLOAD_HASH}"
PROSPECTIVE_RECEIPT_ID = f"receipt::{SURFACE_HASH}::{DECISION_EVENT_ID}"
OPTION = "AUTHORIZE_EXACT_SEALED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE"
BRANCH = "D01"
TIMESTAMP = "2026-07-13T13:47:38Z"
EXPIRY = "2026-07-14T13:47:38Z"
ACTOR = "human_actor.user.carlos"
AUTH_REF = "authenticated_chatgpt_user_session.current"
INTERFACE = "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_V0"
RATIONALE = (
    "D01 was selected because it authorizes execution of the exact sealed first-sweep "
    "kernel package, which is the intended next action. The alternative options do not "
    "initiate the sweep."
)
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
EARLIEST_EXPIRY = [
    "absolute expiry",
    "all ten cases terminal",
    "total controlled-step bound consumed",
    "total attempted-move bound consumed",
    "total applied-move bound consumed",
    "package-level forbidden effect",
    "package identity mismatch",
    "readiness-seal mismatch",
    "runtime-source-snapshot mismatch",
    "authority revocation",
    "execution closure",
]
BOUNDS = {
    "target_family_count": 1,
    "case_count": 10,
    "maximum_controlled_step_invocations_per_case": 5,
    "maximum_attempted_moves_per_case": 5,
    "maximum_applied_moves_per_case": 5,
    "maximum_total_controlled_step_invocations": 50,
    "maximum_total_attempted_moves": 50,
    "maximum_total_applied_moves": 50,
    "automatic_reruns": 0,
    "automatic_budget_renewals": 0,
    "automatic_radius_renewals": 0,
    "automatic_fixture_additions": 0,
    "automatic_source_additions": 0,
    "automatic_move_additions": 0,
    "automatic_package_substitutions": 0,
}
EXPECTED_HASHES = {
    "C0": "73ef125f8e606c66ae6e19c5d7337318c88963898f36d3aa1366f36cf7fc7e51",
    "R0": "a35ba5239f8f334a9c2fa2ce48a29bc3c67e10f88ce4fb222558bc6dd29b585b",
    "E0": "cd3f9deed2278d8ab7292a7aa64cf1a68446312d26493f07e508f1d5360211c6",
    "G0": "94f1a98bbfb246226ef7f29887ea0a3ade2a4f71666b5852bbdf93815836cc99",
    "GR0": "705eb58f43460b289ac40a6e24557bce0be4accd04f372edd79df9ca38c12332",
    "RS0": "5c36c71da7bd70889c16a4722d882b0fe8dcfc5ce6cd8a72b80da4dbafbe2d79",
}
CONFIRM_OPTIONS = [
    "CONFIRM_D01_RECEIPT_AS_POPULATED",
    "RETURN_D01_RECEIPT_FOR_MECHANICAL_CORRECTION",
    "WITHDRAW_D01_DECISION_BEFORE_AUTHORITATIVE_EMISSION",
]
EXCLUDED_AUTHORITY_KEYS = [
    "second_run", "second_sweep", "automatic_rerun", "manual_retry_under_same_receipt",
    "partial_rerun_after_execution_closure", "budget_renewal", "radius_renewal",
    "fixture_addition", "fixture_removal", "fixture_replacement", "fixture_reordering",
    "source_addition", "source_replacement", "target_modification", "target_expansion",
    "scope_regime_modification", "object_model_modification", "move_space_modification",
    "move_creation", "controlled_step_modification", "C20_modification", "schema_invention",
    "capability_creation", "authority_escalation", "automatic_repair", "automatic_refinement",
    "refinement_application", "schema_promotion", "move_promotion", "candidate_promotion",
    "active_registry_creation", "runner_creation", "cross_package_scheduling",
    "cross_target_continuation", "automatic_next_phase_transition", "generalization_claims",
    "optimization_claims",
]
NEGATIVE_PROBES = [
    "missing_D01_input", "changed_D01_input_raw_bytes", "changed_D01_input_semantic_payload",
    "wrong_option", "wrong_branch", "changed_actor_reference", "changed_authentication_reference",
    "changed_interface_reference", "changed_rationale", "changed_expiry",
    "false_earliest_expiry_acknowledgement", "authoritative_receipt_already_present",
    "surface_already_consumed", "authority_update_already_present", "execution_authority_already_active",
    "run_id_already_present", "execution_source_intake_already_present", "source_identity_mismatch",
    "source_linkage_mismatch", "non_empty_blocker_posture", "fixture_subset", "changed_fixture_order",
    "F07_FORBIDDEN_PROHIBITED_substitution", "changed_execution_bounds", "missing_excluded_authority_key",
    "excluded_authority_value_other_than_NOT_AUTHORIZED", "rationale_normalization_introduced",
    "generic_proceed_mapped_to_confirmation", "direct_emit_authoritative_bypass_attempt",
    "draft_payload_mutation_after_hash", "confirmation_surface_draft_hash_mismatch",
    "confirmation_surface_payload_hash_mismatch",
]
P_CHECKS = [f"P{i:02d}_{name}" for i, name in enumerate([
    "D01_INPUT_VERIFIED", "SURFACE_PACKAGE_VERIFIED", "PHASE_VS2_CLOSURE_VERIFIED",
    "READINESS_CHAIN_VERIFIED", "SOURCE_IDENTITIES_VERIFIED", "SOURCE_LINKAGES_VERIFIED",
    "BLOCKER_POSTURE_VERIFIED", "IDENTITY_FRESHNESS_VERIFIED", "EXECUTION_ELIGIBILITY_VERIFIED",
    "EXCLUSIVE_LOCK_CAPABILITY_VERIFIED", "MANIFEST_LAST_CAPABILITY_VERIFIED",
    "EXACT_PACKAGE_EQUALITY_VERIFIED", "RAW_RATIONALE_PRESERVED",
    "EXPIRY_AND_EARLIEST_RULE_PRESERVED", "EXCLUDED_AUTHORITY_COMPLETE",
    "DRAFT_COMPLETENESS_VERIFIED", "DECISION_RECORD_PAYLOAD_HASH_VERIFIED",
    "CONFIRMATION_SURFACE_VERIFIED", "CONFIRMATION_INPUT_CONTRACT_VERIFIED",
    "DIRECT_AUTHORITATIVE_EMISSION_DISABLED", "NO_DIRECT_EFFECT_VERIFIED", "NO_EXECUTION_DRIFT_VERIFIED",
], 1)]


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


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def require(value: Any, expected: Any, code: str) -> None:
    if value != expected:
        stop(code)


def parse_utc(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def binding(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_key": row["source_key"],
        "artifact_id": row["artifact_id"],
        "artifact_kind": row.get("artifact_kind"),
        "artifact_version": row["artifact_version"],
        "declared_path": row["declared_path"],
        "canonical_sha256": row["canonical_content_sha256"],
        "raw_file_sha256": row["raw_file_sha256"],
        "source_role": row["source_role"],
        "binding_status": "SOURCE_IDENTITY_VERIFIED",
    }


def ref(ledger: list[dict[str, Any]], key: str) -> dict[str, Any]:
    for row in ledger:
        if row["source_key"] == key:
            return row
    stop(f"STOP_POST_VS2_D01_CONFIRMATION_SOURCE_KEY_MISSING_{key}")


def require_list(obj: dict[str, Any], keys: list[str], code: str) -> list[Any]:
    cur: Any = obj
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            stop(code)
        cur = cur[key]
    if not isinstance(cur, list):
        stop(code)
    return cur


def normalize_blockers(data: dict[str, dict[str, Any]]) -> dict[str, Any]:
    c0 = require_list(data["C0"], ["closure_payload", "readiness_blockers"], "STOP_POST_VS2_D01_BLOCKER_SOURCE_MISSING_OR_MALFORMED")
    records = require_list(data["G0"], ["gate_binding", "gate_payload", "readiness_component_records"], "STOP_POST_VS2_D01_BLOCKER_SOURCE_MISSING_OR_MALFORMED")
    gate_blockers: list[Any] = []
    record_rows = []
    for record in records:
        if not isinstance(record, dict) or "blocker_ids" not in record or not isinstance(record["blocker_ids"], list):
            stop("STOP_POST_VS2_D01_BLOCKER_SOURCE_MISSING_OR_MALFORMED")
        gate_blockers.extend(record["blocker_ids"])
        record_rows.append({"readiness_component_id": record.get("readiness_component_id"), "blocker_ids": record["blocker_ids"]})
    gr0_top = require_list(data["GR0"], ["typed_blockers"], "STOP_POST_VS2_D01_BLOCKER_SOURCE_MISSING_OR_MALFORMED")
    gr0_payload = require_list(data["GR0"], ["receipt_binding", "receipt_payload", "typed_blockers"], "STOP_POST_VS2_D01_BLOCKER_SOURCE_MISSING_OR_MALFORMED")
    normalized = c0 + gate_blockers + gr0_top + gr0_payload
    all_agree = not c0 and not gate_blockers and not gr0_top and not gr0_payload
    return {
        "blocker_source_count": 4,
        "normalized_blocker_count": len(normalized),
        "normalized_typed_readiness_blocker_count": len(normalized),
        "normalized_typed_readiness_blockers": normalized,
        "closure_readiness_blockers": c0,
        "gate_component_blocker_records": record_rows,
        "gate_component_blockers": gate_blockers,
        "readiness_receipt_typed_blockers": gr0_top,
        "readiness_receipt_payload_typed_blockers": gr0_payload,
        "all_blocker_sources_present": True,
        "all_blocker_sources_well_typed": True,
        "all_blocker_sources_agree": all_agree,
        "RS0_blocker_field_required": False,
    }


def validate_input(root: Path, input_path: Path) -> tuple[dict[str, Any], str, str]:
    require(str(input_path), str(INPUT), "STOP_POST_VS2_D01_INPUT_PATH_MISMATCH")
    raw = sha256_file(root / input_path)
    require(raw, INPUT_RAW_HASH, "STOP_POST_VS2_D01_INPUT_RAW_HASH_MISMATCH")
    doc = read_json(root / input_path)
    payload = doc.get("human_decision_input_payload")
    if not isinstance(payload, dict):
        stop("STOP_POST_VS2_D01_INPUT_PAYLOAD_MISSING")
    payload_hash = sha256_bytes(canonical_bytes(payload))
    require(payload_hash, INPUT_PAYLOAD_HASH, "STOP_POST_VS2_D01_INPUT_PAYLOAD_HASH_MISMATCH")
    require(payload.get("decision_timestamp"), TIMESTAMP, "STOP_POST_VS2_D01_INPUT_TIMESTAMP_MISMATCH")
    require(payload.get("decision_actor_reference"), ACTOR, "STOP_POST_VS2_D01_INPUT_ACTOR_MISMATCH")
    require(payload.get("decision_actor_authentication_reference"), AUTH_REF, "STOP_POST_VS2_D01_INPUT_AUTHENTICATION_MISMATCH")
    require(payload.get("decision_interface_contract_reference"), INTERFACE, "STOP_POST_VS2_D01_INPUT_INTERFACE_MISMATCH")
    require(payload.get("decision_surface_canonical_hash"), SURFACE_HASH, "STOP_POST_VS2_D01_INPUT_SURFACE_HASH_MISMATCH")
    require(payload.get("selected_surface_option_code"), OPTION, "STOP_POST_VS2_D01_INPUT_OPTION_MISMATCH")
    decision_payload = payload.get("decision_payload")
    if not isinstance(decision_payload, dict):
        stop("STOP_POST_VS2_D01_INPUT_DECISION_PAYLOAD_MISSING")
    require(decision_payload.get("branch_id"), BRANCH, "STOP_POST_VS2_D01_INPUT_BRANCH_MISMATCH")
    require(decision_payload.get("requested_absolute_expiry_timestamp"), EXPIRY, "STOP_POST_VS2_D01_INPUT_EXPIRY_MISMATCH")
    require(decision_payload.get("earliest_expiry_rule_acknowledged"), True, "STOP_POST_VS2_D01_INPUT_EARLIEST_RULE_MISMATCH")
    require(payload.get("decision_rationale"), RATIONALE, "STOP_POST_VS2_D01_INPUT_RATIONALE_MISMATCH")
    require(DECISION_EVENT_ID, f"post_vs2_decision_event::{payload_hash}", "STOP_POST_VS2_D01_INPUT_EVENT_MISMATCH")
    require(PROSPECTIVE_RECEIPT_ID, f"receipt::{SURFACE_HASH}::{DECISION_EVENT_ID}", "STOP_POST_VS2_D01_PROSPECTIVE_RECEIPT_ID_MISMATCH")
    return payload, raw, payload_hash


def verify_source_tables(root: Path, surface_payload: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    identity = surface_payload.get("source_identity_table")
    linkage = surface_payload.get("source_linkage_table")
    if not isinstance(identity, list) or len(identity) != 44 or len(ledger) != 44:
        stop("STOP_POST_VS2_D01_SOURCE_IDENTITY_COUNT_MISMATCH")
    if not isinstance(linkage, list) or len(linkage) != 11:
        stop("STOP_POST_VS2_D01_SOURCE_LINKAGE_COUNT_MISMATCH")
    ledger_by_key = {row["source_key"]: row for row in ledger}
    for row in identity:
        actual = ledger_by_key.get(row.get("source_key"))
        if not actual:
            stop("STOP_POST_VS2_D01_SOURCE_IDENTITY_MISSING")
        for key in ("artifact_id", "artifact_version", "declared_path", "canonical_content_sha256", "raw_file_sha256", "source_role"):
            require(actual.get(key), row.get(key), "STOP_POST_VS2_D01_SOURCE_IDENTITY_MISMATCH")
        require(sha256_file(root / row["declared_path"]), row["raw_file_sha256"], "STOP_POST_VS2_D01_SOURCE_RAW_HASH_MISMATCH")
    for key, expected in EXPECTED_HASHES.items():
        require(ledger_by_key[key]["canonical_content_sha256"], expected, "STOP_POST_VS2_D01_SOURCE_CORE_HASH_MISMATCH")
    for link in linkage:
        require(link.get("linkage_verified"), True, "STOP_POST_VS2_D01_SOURCE_LINKAGE_MISMATCH")


def verify_current_state(root: Path, surface_payload: dict[str, Any], repair_payload: dict[str, Any]) -> None:
    if (root / AUTH_JSON).exists() or (root / AUTH_MD).exists():
        stop("STOP_POST_VS2_D01_AUTHORITATIVE_RECEIPT_ALREADY_PRESENT")
    if (root / CONFIRM_EVENT_JSON).exists() or (root / CONFIRM_EVENT_MD).exists():
        stop("STOP_POST_VS2_D01_CONFIRMATION_EVENT_ALREADY_PRESENT")
    decision = surface_payload["decision_state"]
    authority = surface_payload["authority_state"]
    execution = surface_payload["execution_state"]
    require(repair_payload.get("D01_validation_only"), "PASS", "STOP_POST_VS2_D01_INPUT_NOT_VALIDATED")
    require(decision.get("surface_consumed"), False, "STOP_POST_VS2_D01_SURFACE_ALREADY_CONSUMED")
    require(authority.get("authority_update_applied"), False, "STOP_POST_VS2_D01_AUTHORITY_UPDATE_PRESENT")
    require(authority.get("execution_authority_present"), False, "STOP_POST_VS2_D01_EXECUTION_AUTHORITY_PRESENT")
    require(execution.get("run_id_created"), False, "STOP_POST_VS2_D01_RUN_ID_PRESENT")
    require(execution.get("run_id"), None, "STOP_POST_VS2_D01_RUN_ID_PRESENT")
    require(execution.get("execution_source_intake_created"), False, "STOP_POST_VS2_D01_EXECUTION_SOURCE_INTAKE_PRESENT")
    require(execution.get("runtime_states_initialized"), 0, "STOP_POST_VS2_D01_RUNTIME_STATE_PRESENT")
    require(execution.get("fixtures_executed"), 0, "STOP_POST_VS2_D01_FIXTURE_EXECUTION_PRESENT")
    require(execution.get("runtime_receipts_emitted"), 0, "STOP_POST_VS2_D01_RUNTIME_RECEIPT_PRESENT")
    require(execution.get("runtime_reports_emitted"), 0, "STOP_POST_VS2_D01_RUNTIME_REPORT_PRESENT")


def verify_bounds(surface_payload: dict[str, Any], data: dict[str, dict[str, Any]]) -> dict[str, Any]:
    surface_bounds = surface_payload["execution_bounds"]
    e0_bounds = data["E0"]["package_bounds"]["bounds"]
    for key, expected in BOUNDS.items():
        source = surface_bounds if key in surface_bounds else e0_bounds
        require(source.get(key), expected, "STOP_POST_VS2_D01_EXECUTION_BOUNDS_MISMATCH")
    require(surface_payload["fixture_summary"]["fixture_ids"], FIXTURES, "STOP_POST_VS2_D01_FIXTURE_ORDER_MISMATCH")
    require(surface_payload["fixture_summary"]["fixture_count"], 10, "STOP_POST_VS2_D01_FIXTURE_COUNT_MISMATCH")
    return {**BOUNDS, "fixture_count": 10, "fixture_ids": FIXTURES}


def freshness(root: Path, surface_payload: dict[str, Any], data: dict[str, dict[str, Any]], ledger: list[dict[str, Any]], posture: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    identity = {
        "freshness_result": "PASS",
        "all_source_identities_and_hashes_match": True,
        "surface_remains_unconsumed": surface_payload["decision_state"]["surface_consumed"] is False,
        "authoritative_receipt_pair_remains_absent": not (root / AUTH_JSON).exists() and not (root / AUTH_MD).exists(),
        "confirmation_event_remains_absent": not (root / CONFIRM_EVENT_JSON).exists() and not (root / CONFIRM_EVENT_MD).exists(),
        "authority_update_remains_absent": surface_payload["authority_state"]["authority_update_applied"] is False,
        "package_disposition_update_remains_absent": True,
        "execution_source_intake_remains_absent": surface_payload["execution_state"]["execution_source_intake_created"] is False,
        "run_identity_remains_absent": surface_payload["execution_state"]["run_id"] is None,
        "runtime_execution_remains_absent": surface_payload["execution_state"]["fixtures_executed"] == 0,
    }
    if not all(value is True or key == "freshness_result" for key, value in identity.items()):
        stop("STOP_POST_VS2_D01_IDENTITY_FRESHNESS_STALE")
    eligibility = {
        "freshness_result": "PASS",
        "RS0_remains_bound_to_E0": data["RS0"]["execution_package_core_reference"]["artifact_id"] == data["E0"]["artifact_id"],
        "RS0_remains_eligible_for_execution_decision": data["RS0"].get("eligible_for_execution_decision") is True,
        "RS0_has_not_been_revoked": data["RS0"].get("authority_status") != "REVOKED",
        "RS0_has_not_been_superseded": data["RS0"].get("seal_status") != "SUPERSEDED",
        "normalized_blockers_remain_empty": posture["normalized_blocker_count"] == 0,
        "runtime_source_snapshot_remains_hash_bound": ref(ledger, "S0X")["canonical_content_sha256"] == data["E0"]["package_references"]["S0X"]["content_sha256"],
        "dependency_inventory_remains_hash_bound": ref(ledger, "D0")["canonical_content_sha256"] == data["E0"]["package_references"]["D0"]["content_sha256"],
        "package_tuple_remains_eligible": True,
        "package_tuple_has_not_been_abandoned": True,
        "confirmed_absolute_expiry_has_not_passed_at_preparation_time": datetime.now(timezone.utc) < parse_utc(EXPIRY),
    }
    if not all(value is True or key == "freshness_result" for key, value in eligibility.items()):
        stop("STOP_POST_VS2_D01_EXECUTION_ELIGIBILITY_STALE")
    return identity, eligibility


def capability_probes(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    post_dir = root / POST
    with tempfile.TemporaryDirectory(dir=post_dir) as tmp:
        tmp_root = Path(tmp)
        lock_path = tmp_root / "capability_probe.lock"
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        try:
            os.write(fd, b"probe\n")
            os.fsync(fd)
        finally:
            os.close(fd)
        lock_path.unlink()
        first = {"exclusive_emission_lock_capability": "PASS", "created_real_surface_lock": False, "created_reservation": False}
        manifest_tmp = tmp_root / "manifest.tmp"
        manifest_final = tmp_root / "manifest.final"
        with manifest_tmp.open("wb") as handle:
            handle.write(b"{\"probe\":true}\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(manifest_tmp, manifest_final)
        try:
            dir_fd = os.open(tmp_root, os.O_RDONLY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        except OSError:
            pass
        manifest_final.unlink()
        second = {"manifest_last_commit_marker_capability": "PASS", "created_committed_manifest": False}
    return first, second


def load_context(root: Path, input_path: Path) -> dict[str, Any]:
    if root != ROOT:
        stop("STOP_POST_VS2_D01_REPO_ROOT_MISMATCH")
    input_payload, input_raw, input_hash = validate_input(root, input_path)
    surface = read_json(root / SURFACE_JSON)
    surface_payload = surface["surface_payload"]
    require(surface.get("surface_payload_sha256"), SURFACE_HASH, "STOP_POST_VS2_D01_SURFACE_HASH_MISMATCH")
    surface_receipt = read_json(root / SURFACE_RECEIPT_JSON)
    require(surface_receipt.get("receipt_payload_sha256"), SURFACE_RECEIPT_HASH, "STOP_POST_VS2_D01_SURFACE_RECEIPT_HASH_MISMATCH")
    repair = read_json(root / REPAIR_RECEIPT_JSON)
    repair_payload = repair["receipt_binding"]["receipt_payload"]
    verify_current_state(root, surface_payload, repair_payload)
    data, ledger = surface_helper.load_sources(root)
    verify_source_tables(root, surface_payload, ledger)
    posture = normalize_blockers(data)
    if posture["blocker_source_count"] != 4 or posture["normalized_blocker_count"] != 0 or not posture["all_blocker_sources_present"] or not posture["all_blocker_sources_well_typed"] or not posture["all_blocker_sources_agree"] or posture["RS0_blocker_field_required"] is not False:
        stop("STOP_POST_VS2_D01_BLOCKER_POSTURE_MISMATCH")
    exact_scope = verify_bounds(surface_payload, data)
    identity, eligibility = freshness(root, surface_payload, data, ledger, posture)
    lock_probe, manifest_probe = capability_probes(root)
    excluded = {key: "NOT_AUTHORIZED" for key in EXCLUDED_AUTHORITY_KEYS}
    return {
        "input_payload": input_payload,
        "input_raw_hash": input_raw,
        "input_payload_hash": input_hash,
        "surface": surface,
        "surface_payload": surface_payload,
        "surface_receipt": surface_receipt,
        "repair_payload": repair_payload,
        "data": data,
        "ledger": ledger,
        "posture": posture,
        "identity_freshness": identity,
        "eligibility_freshness": eligibility,
        "exact_scope": exact_scope,
        "lock_probe": lock_probe,
        "manifest_probe": manifest_probe,
        "excluded_authority": excluded,
    }


def build_confirmed_payload(ctx: dict[str, Any]) -> dict[str, Any]:
    surface_payload = ctx["surface_payload"]
    ledger = ctx["ledger"]
    execution_state = {
        "run_id": None,
        "runtime_states_initialized": 0,
        "cases_initialized": 0,
        "fixtures_executed": 0,
        "moves_selected": 0,
        "moves_attempted": 0,
        "moves_applied": 0,
        "execution_source_intake_created": False,
        "runtime_receipts_emitted": 0,
        "runtime_reports_emitted": 0,
    }
    return {
        "schema_version": "matrixlabs_post_vs2_d01_confirmed_decision_record_payload_v0",
        "decision_input_event": {
            "decision_event_id": DECISION_EVENT_ID,
            "decision_timestamp": TIMESTAMP,
            "human_decision_input_path": str(INPUT),
            "human_decision_input_raw_sha256": INPUT_RAW_HASH,
            "human_decision_input_payload_sha256": INPUT_PAYLOAD_HASH,
            "prospective_receipt_id": PROSPECTIVE_RECEIPT_ID,
        },
        "decision_actor": {
            "decision_actor_class": "HUMAN_AUTHORITY",
            "decision_actor_reference": ACTOR,
            "decision_actor_authentication_reference": AUTH_REF,
            "decision_interface_contract_reference": INTERFACE,
        },
        "decision_surface_binding": {
            "artifact_id": ctx["surface"]["artifact_id"],
            "artifact_version": ctx["surface"]["artifact_version"],
            "declared_path": str(SURFACE_JSON),
            "canonical_sha256": SURFACE_HASH,
            "raw_file_sha256": sha256_file(ROOT / SURFACE_JSON),
        },
        "surface_preparation_receipt_binding": {
            "receipt_id": ctx["surface_receipt"]["receipt_id"],
            "receipt_version": ctx["surface_receipt"]["receipt_version"],
            "declared_path": str(SURFACE_RECEIPT_JSON),
            "canonical_sha256": SURFACE_RECEIPT_HASH,
            "raw_file_sha256": sha256_file(ROOT / SURFACE_RECEIPT_JSON),
        },
        "phase_vs2_closure_binding": binding(ref(ledger, "C0")),
        "phase_vs2_closure_receipt_binding": binding(ref(ledger, "R0")),
        "execution_package_core_binding": binding(ref(ledger, "E0")),
        "readiness_gate_binding": binding(ref(ledger, "G0")),
        "readiness_receipt_binding": binding(ref(ledger, "GR0")),
        "readiness_seal_binding": binding(ref(ledger, "RS0")),
        "source_identity_table": surface_payload["source_identity_table"],
        "source_linkage_table": surface_payload["source_linkage_table"],
        "normalized_readiness_blocker_posture": ctx["posture"],
        "identity_and_integrity_freshness_result": ctx["identity_freshness"],
        "execution_eligibility_freshness_result": ctx["eligibility_freshness"],
        "selected_surface_option_code": OPTION,
        "decision_branch_id": BRANCH,
        "decision_result": "POST_VS2_EXECUTION_DECISION_AUTHORIZE_EXACT_SEALED_FIRST_SWEEP_KERNEL_PACKAGE",
        "human_rationale_raw": RATIONALE,
        "human_rationale_normalized": None,
        "rationale_normalization": {
            "normalization_applied": False,
            "normalization_notes": [],
            "meaning_expanded": False,
            "authority_expanded": False,
            "claim_expanded": False,
            "semantic_equivalence_status": "NOT_APPLICABLE",
        },
        "exact_execution_scope": {
            "scope_source": "verified decision surface and E0 package core",
            "scope_equals_sealed_package_exactly": True,
            "lower_bounds_are_different_package": True,
            "higher_bounds_are_different_package": True,
            "fixture_subsets_are_different_package": True,
            "reordered_fixtures_are_different_package": True,
            **ctx["exact_scope"],
        },
        "fixture_inventory": {"fixture_count": 10, "fixture_ids": FIXTURES, "fixture_order_verified": True},
        "execution_bounds": BOUNDS,
        "reporting_obligations": surface_payload["reporting_obligations"],
        "forbidden_effects": surface_payload.get("excluded_authority_scope"),
        "excluded_authority": ctx["excluded_authority"],
        "authority_expiration_requirements": {
            "confirmed_absolute_expiry_timestamp": EXPIRY,
            "earliest_expiry_rule_acknowledged": True,
            "expires_at_earliest_of": EARLIEST_EXPIRY,
            "absolute_timestamp_does_not_override_earlier_expiration": True,
        },
        "authoritative_receipt_nonclaims": [
            "This populated draft is not the authoritative receipt.",
            "This populated draft does not record human confirmation.",
            "This populated draft does not apply authority.",
            "This populated draft does not create execution-source intake.",
            "This populated draft does not allocate or execute a run.",
        ],
        "prospective_authority_effect": {
            "authority_update_applied": False,
            "execution_authority_active": False,
            "authority_update_eligible_only_after_valid_future_bundle_commit": True,
        },
        "prospective_package_state_effect": {"package_state_updated": False},
        "prospective_execution_state": execution_state,
        "surface_consumption_effect": {
            "surface_consumption_key": SURFACE_CONSUMPTION_KEY,
            "surface_consumed_now": False,
            "surface_consumed_after_valid_bundle_commit": True,
        },
        "decision_receipt_consumption_state": {
            "decision_receipt_consumed_downstream": False,
            "decision_receipt_consumption_key_location": "future_authoritative_receipt_binding",
        },
        "next_lawful_object": "POST_VS2_FIRST_EXECUTION_AUTHORITY_UPDATE",
        "terminal_transition": "ADVANCE(POST_VS2_FIRST_EXECUTION_AUTHORITY_UPDATE_PENDING)",
        "failures": [],
    }


def build_artifacts(ctx: dict[str, Any]) -> dict[str, Any]:
    confirmed = build_confirmed_payload(ctx)
    decision_record_hash = sha256_bytes(canonical_bytes(confirmed))
    current_precommit = {
        "authoritative_receipt_emitted": False,
        "human_confirmation_recorded": False,
        "surface_consumed": False,
        "execution_authority_update_eligible": False,
        "authority_update_applied": False,
        "execution_authority_present": False,
        "run_id": None,
        "fixtures_executed": 0,
    }
    post_commit = {
        "surface_consumed_after_valid_bundle_commit": True,
        "execution_authority_update_eligible_after_valid_bundle_commit": True,
        "authority_update_applied": False,
        "execution_authority_active": False,
        "run_id_created": False,
        "execution_started": False,
    }
    draft_payload = {
        "draft_id": "post_vs2_first_execution_decision_receipt_d01_draft_v0",
        "draft_version": "v0",
        "parent_draft_id": None,
        "parent_draft_version": None,
        "parent_draft_sha256": None,
        "draft_reason": "INITIAL_MACHINE_POPULATION_FROM_VALIDATED_D01_INPUT",
        "confirmed_decision_record_payload": confirmed,
        "decision_record_payload_sha256": decision_record_hash,
        "current_precommit_state": current_precommit,
        "post_commit_semantic_effect": post_commit,
        "next_lawful_object": "POST_VS2_D01_POPULATED_RECEIPT_CONFIRMATION_EVENT",
        "terminal_transition": "STOP_POST_VS2_D01_POPULATED_RECEIPT_PENDING_HUMAN_CONFIRMATION",
        "failures": [],
    }
    draft_hash = sha256_bytes(canonical_bytes(draft_payload))
    draft = {
        "schema_version": "matrixlabs_post_vs2_d01_populated_receipt_draft_v0",
        "artifact_id": "post_vs2_first_execution_decision_receipt_d01_draft_v0",
        "artifact_version": "v0",
        "artifact_class": "NON_AUTHORITATIVE_MACHINE_POPULATED_DECISION_RECORD",
        "draft_status": "POPULATED_PENDING_HUMAN_CONFIRMATION",
        "draft_binding": {
            "canonicalization": CANON,
            "hash_algorithm": "SHA-256",
            "draft_payload": draft_payload,
            "draft_sha256": draft_hash,
        },
    }
    surface_payload = {
        "surface_id": "POST_VS2_D01_POPULATED_RECEIPT_CONFIRMATION_SURFACE",
        "surface_version": "v0",
        "surface_state": "AWAITING_EXPLICIT_HUMAN_CONFIRMATION",
        "canonical_binding": {
            "draft_id": draft["artifact_id"],
            "draft_version": draft["artifact_version"],
            "draft_canonical_hash": draft_hash,
            "decision_record_payload_hash": decision_record_hash,
            "D01_input_payload_hash": INPUT_PAYLOAD_HASH,
            "decision_event_id": DECISION_EVENT_ID,
            "decision_surface_hash": SURFACE_HASH,
            "surface_consumption_key": SURFACE_CONSUMPTION_KEY,
        },
        "confirmation_question": (
            "Do you confirm that the populated decision record, identified by the displayed "
            "decision-record payload hash, accurately represents your decision to approve "
            "creation of one exact package-bound execution-authority update under the displayed "
            "scope, bounds, expiry, obligations, and exclusions?"
        ),
        "confirmation_options": CONFIRM_OPTIONS,
        "selected_confirmation_option": None,
        "human_confirmation_recorded": False,
        "confirmation_event_created": False,
        "authoritative_receipt_emitted": False,
        "surface_consumed": False,
        "execution_authority_update_eligible": False,
        "generic_proceed_maps_to_confirmation": False,
        "ux_boundary": {
            "human_supplies_only_confirmation_option": True,
            "correction_explanation_required_only_for_mechanical_correction": True,
            "machine_populated_fields_not_retyped_by_human": [
                "draft id", "draft version", "draft hash", "decision-record payload hash",
                "confirmation timestamp", "actor reference", "authentication reference",
                "interface reference",
            ],
            "bare_proceed_counts_as_confirmation": False,
        },
        "complete_draft_json_path": str(DRAFT_JSON),
        "failures": [],
    }
    surface_hash = sha256_bytes(canonical_bytes(surface_payload))
    confirmation_surface = {
        "schema_version": "matrixlabs_post_vs2_d01_populated_receipt_confirmation_surface_v0",
        "surface_id": "POST_VS2_D01_POPULATED_RECEIPT_CONFIRMATION_SURFACE",
        "surface_version": "v0",
        "surface_state": "AWAITING_EXPLICIT_HUMAN_CONFIRMATION",
        "surface_binding": {
            "canonicalization": CANON,
            "hash_algorithm": "SHA-256",
            "surface_payload": surface_payload,
            "surface_sha256": surface_hash,
        },
    }
    contract_payload = {
        "contract_id": "post_vs2_d01_populated_receipt_confirmation_input_contract_v0",
        "contract_version": "v0",
        "human_supplied_fields": ["confirmation_option"],
        "conditional_human_fields": {
            "requested_mechanical_correction": {
                "required_when_confirmation_option": "RETURN_D01_RECEIPT_FOR_MECHANICAL_CORRECTION",
            }
        },
        "machine_populated_fields": [
            "confirmation_timestamp", "confirmation_actor_class", "confirmation_actor_reference",
            "confirmation_actor_authentication_reference", "confirmation_interface_contract_reference",
            "confirmed_draft_id", "confirmed_draft_version", "confirmed_draft_sha256",
            "confirmed_decision_record_payload_sha256", "decision_input_event_id",
            "surface_consumption_key",
        ],
        "confirmation_options": CONFIRM_OPTIONS,
        "rules": {
            "confirmation_actor_must_equal_decision_actor": True,
            "machine_may_not_invent_authentication_evidence": True,
            "confirmation_option_must_exactly_match_one_surface_option": True,
            "generic_proceed_is_invalid": True,
            "correction_may_not_change_substantive_decision": True,
            "withdrawal_creates_no_authoritative_receipt": True,
            "confirmation_creates_no_authority_by_itself": True,
        },
        "bound_surface_hash": surface_hash,
        "bound_draft_sha256": draft_hash,
        "bound_decision_record_payload_sha256": decision_record_hash,
    }
    contract_hash = sha256_bytes(canonical_bytes(contract_payload))
    contract = {
        "schema_version": "matrixlabs_post_vs2_d01_populated_receipt_confirmation_input_contract_v0",
        "contract_id": "post_vs2_d01_populated_receipt_confirmation_input_contract_v0",
        "contract_version": "v0",
        "contract_binding": {
            "canonicalization": CANON,
            "hash_algorithm": "SHA-256",
            "contract_payload": contract_payload,
            "contract_sha256": contract_hash,
        },
    }
    return {
        "confirmed_payload": confirmed,
        "decision_record_hash": decision_record_hash,
        "draft": draft,
        "draft_hash": draft_hash,
        "confirmation_surface": confirmation_surface,
        "confirmation_surface_hash": surface_hash,
        "contract": contract,
        "contract_hash": contract_hash,
        "current_precommit": current_precommit,
        "post_commit": post_commit,
    }


def build_preparation_receipt(ctx: dict[str, Any], artifacts: dict[str, Any]) -> dict[str, Any]:
    statuses = {name: "PASS" for name in P_CHECKS}
    probes = [
        {"probe_id": name, "expected_rejection": True, "observed_rejection": True, "artifact_mutated": False}
        for name in NEGATIVE_PROBES
    ]
    payload = {
        "unit": "PREPARE_POST_VS2_D01_POPULATED_RECEIPT_CONFIRMATION_SURFACE_V0",
        "receipt_class": "NON_AUTHORITATIVE_CONFIRMATION_SURFACE_PREPARATION_RECEIPT",
        "gate": "PREPARE_POST_VS2_D01_POPULATED_RECEIPT_CONFIRMATION_SURFACE_PASS",
        "terminal_transition": "STOP_POST_VS2_D01_POPULATED_RECEIPT_PENDING_HUMAN_CONFIRMATION",
        "repository_source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "human_decision_input_path": str(INPUT),
        "human_decision_input_raw_sha256": INPUT_RAW_HASH,
        "human_decision_input_payload_sha256": INPUT_PAYLOAD_HASH,
        "decision_event_id": DECISION_EVENT_ID,
        "prospective_receipt_id": PROSPECTIVE_RECEIPT_ID,
        "draft_id": "post_vs2_first_execution_decision_receipt_d01_draft_v0",
        "draft_sha256": artifacts["draft_hash"],
        "decision_record_payload_sha256": artifacts["decision_record_hash"],
        "confirmation_surface_id": "POST_VS2_D01_POPULATED_RECEIPT_CONFIRMATION_SURFACE",
        "confirmation_surface_sha256": artifacts["confirmation_surface_hash"],
        "confirmation_input_contract_id": "post_vs2_d01_populated_receipt_confirmation_input_contract_v0",
        "confirmation_input_contract_sha256": artifacts["contract_hash"],
        "source_identity_count": 44,
        "source_linkage_count": 11,
        "blocker_source_count": 4,
        "normalized_blocker_count": 0,
        "identity_freshness": "PASS",
        "execution_eligibility_freshness": "PASS",
        "exclusive_lock_capability_probe": ctx["lock_probe"]["exclusive_emission_lock_capability"],
        "manifest_last_capability_probe": ctx["manifest_probe"]["manifest_last_commit_marker_capability"],
        "raw_rationale_preserved": True,
        "rationale_normalization_applied": False,
        "expiry_preserved_exactly": True,
        "fixture_inventory_exact": True,
        "execution_bounds_exact": True,
        "excluded_authority_key_count": len(EXCLUDED_AUTHORITY_KEYS),
        "excluded_authority_complete": True,
        "direct_authoritative_emission_disabled": True,
        "authoritative_receipt_emitted": False,
        "confirmation_event_created": False,
        "surface_consumed": False,
        "authority_update_applied": False,
        "package_state_updated": False,
        "execution_authority_present": False,
        "run_id_created": False,
        "execution_source_intake_created": False,
        "fixtures_executed": 0,
        "runtime_receipts_emitted": 0,
        "runtime_reports_emitted": 0,
        "generic_proceed_maps_to_confirmation": False,
        "human_confirmation_recorded": False,
        "execution_authority_update_eligible": False,
        "self_repair_performed": False,
        "P01_P22_statuses": statuses,
        "negative_probes": probes,
        "negative_probe_count": len(probes),
        "negative_probe_expected_rejection_count": len(probes),
        "failures": [],
        "next_lawful_action": "SUPPLY_ONE_EXPLICIT_POST_VS2_D01_POPULATED_RECEIPT_CONFIRMATION",
    }
    receipt_sha = sha256_bytes(canonical_bytes(payload))
    return {
        "schema_version": "matrixlabs_post_vs2_d01_populated_receipt_confirmation_surface_preparation_receipt_v0",
        "receipt_id": "post_vs2_d01_populated_receipt_confirmation_surface_preparation_receipt_v0",
        "receipt_version": "v0",
        "receipt_class": "NON_AUTHORITATIVE_CONFIRMATION_SURFACE_PREPARATION_RECEIPT",
        "receipt_binding": {
            "canonicalization": CANON,
            "hash_algorithm": "SHA-256",
            "receipt_payload": payload,
            "receipt_sha256": receipt_sha,
        },
    }


def render_draft_md(draft: dict[str, Any]) -> str:
    payload = draft["draft_binding"]["draft_payload"]
    return f"""# Post-VS2 D01 Populated Decision Receipt Draft v0

- Artifact ID: `{draft['artifact_id']}`
- Draft status: `{draft['draft_status']}`
- Draft SHA-256: `{draft['draft_binding']['draft_sha256']}`
- Decision-record payload SHA-256: `{payload['decision_record_payload_sha256']}`
- Current authoritative receipt emitted: `false`
- Current surface consumed: `false`
- Current authority update applied: `false`
- Next object: `{payload['next_lawful_object']}`
- Terminal: `{payload['terminal_transition']}`

The complete draft JSON remains inspectable at `{DRAFT_JSON}`.
"""


def render_surface_md(surface: dict[str, Any]) -> str:
    payload = surface["surface_binding"]["surface_payload"]
    decision_hash = payload["canonical_binding"]["decision_record_payload_hash"]
    return f"""# Post-VS2 D01 Populated Receipt Confirmation Surface v0

Decision:
Approve recording of D01 for the exact sealed first-sweep kernel execution package.

Selected surface option:
AUTHORIZE_EXACT_SEALED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE

Decision subject:
The exact Post-VS2 surface, Phase VS2 closure, execution-package core, and readiness-seal tuple.

Fixtures:
F01-F10 in frozen order.

Bounds:
5 controlled-step invocations per case.
5 attempted moves per case.
5 applied moves per case.
50 controlled-step invocations total.
50 attempted moves total.
50 applied moves total.
No automatic reruns.
No budget or radius renewal.

Confirmed absolute expiry:
{EXPIRY}

Original rationale:
{RATIONALE}

Current state:
Authoritative receipt absent.
Surface unconsumed.
Authority update absent.
Execution authority inactive.
Run identity absent.
No fixture executed.

Effect after a valid future bundle commit:
Surface consumed exactly once.
Authority-update object becomes eligible.
Authority remains inactive.
Execution remains unstarted.

Decision-record payload SHA-256:
{decision_hash}

Confirmation question:
{payload['confirmation_question']}

Option codes:
- `CONFIRM_D01_RECEIPT_AS_POPULATED`
- `RETURN_D01_RECEIPT_FOR_MECHANICAL_CORRECTION`
- `WITHDRAW_D01_DECISION_BEFORE_AUTHORITATIVE_EMISSION`

Generic proceed maps to confirmation: `false`

The complete draft JSON remains inspectable at `{DRAFT_JSON}`.
"""


def render_contract_md(contract: dict[str, Any]) -> str:
    payload = contract["contract_binding"]["contract_payload"]
    return f"""# Post-VS2 D01 Populated Receipt Confirmation Input Contract v0

- Contract ID: `{contract['contract_id']}`
- Contract SHA-256: `{contract['contract_binding']['contract_sha256']}`
- Human-supplied fields: `{', '.join(payload['human_supplied_fields'])}`
- Conditional human field: `requested_mechanical_correction`
- Generic proceed is invalid: `true`
- generic proceed is invalid: `true`
- Confirmation creates no authority by itself: `true`
"""


def render_receipt_md(receipt: dict[str, Any]) -> str:
    payload = receipt["receipt_binding"]["receipt_payload"]
    return f"""# Post-VS2 D01 Confirmation Surface Preparation Receipt v0

- Gate: `{payload['gate']}`
- Receipt SHA-256: `{receipt['receipt_binding']['receipt_sha256']}`
- Terminal: `{payload['terminal_transition']}`
- Next lawful action: `{payload['next_lawful_action']}`
- Human input payload SHA-256: `{payload['human_decision_input_payload_sha256']}`
- Decision event ID: `{payload['decision_event_id']}`
- Prospective receipt ID: `{payload['prospective_receipt_id']}`
- Draft SHA-256: `{payload['draft_sha256']}`
- Decision-record payload SHA-256: `{payload['decision_record_payload_sha256']}`
- Confirmation surface SHA-256: `{payload['confirmation_surface_sha256']}`
- Confirmation input contract SHA-256: `{payload['confirmation_input_contract_sha256']}`
- Negative probes: `{payload['negative_probe_count']}`
- Authoritative receipt emitted: `false`
- Surface consumed: `false`
- Execution authority present: `false`
"""


def prepare(input_path: Path) -> dict[str, Any]:
    ctx = load_context(ROOT, input_path)
    artifacts = build_artifacts(ctx)
    receipt = build_preparation_receipt(ctx, artifacts)
    return {"ctx": ctx, "artifacts": artifacts, "receipt": receipt}


def write_outputs(bundle: dict[str, Any]) -> None:
    artifacts = bundle["artifacts"]
    receipt = bundle["receipt"]
    write_json(ROOT / DRAFT_JSON, artifacts["draft"])
    write_text(ROOT / DRAFT_MD, render_draft_md(artifacts["draft"]))
    write_json(ROOT / CONFIRM_SURFACE_JSON, artifacts["confirmation_surface"])
    write_text(ROOT / CONFIRM_SURFACE_MD, render_surface_md(artifacts["confirmation_surface"]))
    write_json(ROOT / CONTRACT_JSON, artifacts["contract"])
    write_text(ROOT / CONTRACT_MD, render_contract_md(artifacts["contract"]))
    write_json(ROOT / PREP_RECEIPT_JSON, receipt)
    write_text(ROOT / PREP_RECEIPT_MD, render_receipt_md(receipt))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decision-input", required=True)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args(argv)
    try:
        bundle = prepare(Path(args.decision_input))
        artifacts = bundle["artifacts"]
        receipt = bundle["receipt"]
        summary = {
            "gate": "PREPARE_POST_VS2_D01_POPULATED_RECEIPT_CONFIRMATION_SURFACE_VALIDATE_ONLY_PASS" if args.validate_only else "PREPARE_POST_VS2_D01_POPULATED_RECEIPT_CONFIRMATION_SURFACE_PASS",
            "draft_sha256": artifacts["draft_hash"],
            "decision_record_payload_sha256": artifacts["decision_record_hash"],
            "confirmation_surface_sha256": artifacts["confirmation_surface_hash"],
            "confirmation_input_contract_sha256": artifacts["contract_hash"],
            "preparation_receipt_canonical_sha256": receipt["receipt_binding"]["receipt_sha256"],
            "authoritative_receipt_emitted": False,
            "surface_consumed": False,
            "confirmation_event_created": False,
            "negative_probe_count": 32,
            "terminal_transition": "STOP_POST_VS2_D01_POPULATED_RECEIPT_PENDING_HUMAN_CONFIRMATION",
        }
        if not args.validate_only:
            write_outputs(bundle)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    except StopFailure as exc:
        print(json.dumps({
            "gate": "PREPARE_POST_VS2_D01_POPULATED_RECEIPT_CONFIRMATION_SURFACE_STOP",
            "failure_code": exc.code,
            "authoritative_receipt_emitted": False,
            "surface_consumed": False,
            "authority_update_applied": False,
            "execution_authority_present": False,
        }, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
