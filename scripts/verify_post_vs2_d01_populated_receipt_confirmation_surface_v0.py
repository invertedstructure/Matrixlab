#!/usr/bin/env python3
"""Verify the Post-VS2 D01 populated receipt confirmation surface artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path("/home/asd/projects/matrixlab")
POST = Path("docs/matrixlabs/post_vs2")
INPUT = POST / "post_vs2_first_execution_human_decision_input_v0.json"
SURFACE_JSON = POST / "post_vs2_first_execution_decision_surface_v0.json"
AUTH_JSON = POST / "post_vs2_first_execution_decision_receipt_v0.json"
AUTH_MD = POST / "post_vs2_first_execution_decision_receipt_v0.md"
DRAFT_JSON = POST / "post_vs2_first_execution_decision_receipt_d01_draft_v0.json"
DRAFT_MD = POST / "post_vs2_first_execution_decision_receipt_d01_draft_v0.md"
CONFIRM_SURFACE_JSON = POST / "post_vs2_d01_populated_receipt_confirmation_surface_v0.json"
CONFIRM_SURFACE_MD = POST / "post_vs2_d01_populated_receipt_confirmation_surface_v0.md"
CONTRACT_JSON = POST / "post_vs2_d01_populated_receipt_confirmation_input_contract_v0.json"
CONTRACT_MD = POST / "post_vs2_d01_populated_receipt_confirmation_input_contract_v0.md"
PREP_RECEIPT_JSON = POST / "post_vs2_d01_populated_receipt_confirmation_surface_preparation_receipt_v0.json"
PREP_RECEIPT_MD = POST / "post_vs2_d01_populated_receipt_confirmation_surface_preparation_receipt_v0.md"
INPUT_RAW_HASH = "680d79ed2a15e50d2c99e98dde6c6dc267a8eb0efba968dbb95a0d28cd2ae548"
INPUT_PAYLOAD_HASH = "d5eaaf7594f5b031146a5aa60ffaf9eb38fa7aba7801536ff4ce31e1571ed648"
SURFACE_HASH = "d7150101acbfe46342c95506c526e2b49b6ca295881c2e390d78fdb4c5001d35"
SURFACE_CONSUMPTION_KEY = "3529a085e04b3c7e8b97fa60be7ad0edb0c619c1274054296ea3592434405396"
DECISION_EVENT_ID = f"post_vs2_decision_event::{INPUT_PAYLOAD_HASH}"
PROSPECTIVE_RECEIPT_ID = f"receipt::{SURFACE_HASH}::{DECISION_EVENT_ID}"
OPTION = "AUTHORIZE_EXACT_SEALED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE"
BRANCH = "D01"
EXPIRY = "2026-07-14T13:47:38Z"
RATIONALE = "D01 was selected because it authorizes execution of the exact sealed first-sweep kernel package, which is the intended next action. The alternative options do not initiate the sweep."
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


def get_source(surface_payload: dict[str, Any], key: str) -> dict[str, Any]:
    for row in surface_payload["source_identity_table"]:
        if row["source_key"] == key:
            return row
    raise AssertionError(f"missing source key {key}")


def blocker_posture(root: Path, surface_payload: dict[str, Any]) -> dict[str, Any]:
    c0 = read_json(root / get_source(surface_payload, "C0")["declared_path"])
    g0 = read_json(root / get_source(surface_payload, "G0")["declared_path"])
    gr0 = read_json(root / get_source(surface_payload, "GR0")["declared_path"])
    c0_blockers = c0["closure_payload"]["readiness_blockers"]
    gate_records = g0["gate_binding"]["gate_payload"]["readiness_component_records"]
    gate_blockers = []
    for record in gate_records:
        ids = record["blocker_ids"]
        if not isinstance(ids, list):
            raise AssertionError("malformed gate blocker ids")
        gate_blockers.extend(ids)
    gr0_top = gr0["typed_blockers"]
    gr0_payload = gr0["receipt_binding"]["receipt_payload"]["typed_blockers"]
    normalized = c0_blockers + gate_blockers + gr0_top + gr0_payload
    return {
        "blocker_source_count": 4,
        "normalized_blocker_count": len(normalized),
        "all_blocker_sources_present": True,
        "all_blocker_sources_well_typed": True,
        "all_blocker_sources_agree": not normalized,
        "RS0_blocker_field_required": False,
    }


def verify() -> dict[str, Any]:
    failures: list[str] = []
    try:
        input_doc = read_json(ROOT / INPUT)
        input_payload = input_doc["human_decision_input_payload"]
        if sha256_file(ROOT / INPUT) != INPUT_RAW_HASH:
            failures.append("input_raw_hash")
        if sha256_bytes(canonical_bytes(input_payload)) != INPUT_PAYLOAD_HASH:
            failures.append("input_payload_hash")
        if input_payload["selected_surface_option_code"] != OPTION or input_payload["decision_payload"]["branch_id"] != BRANCH:
            failures.append("input_option_branch")
        if input_payload["decision_rationale"] != RATIONALE:
            failures.append("input_rationale")
        if input_payload["decision_payload"]["requested_absolute_expiry_timestamp"] != EXPIRY or input_payload["decision_payload"]["earliest_expiry_rule_acknowledged"] is not True:
            failures.append("input_expiry")

        surface = read_json(ROOT / SURFACE_JSON)
        surface_payload = surface["surface_payload"]
        if surface["surface_payload_sha256"] != SURFACE_HASH:
            failures.append("surface_hash")
        identities = surface_payload["source_identity_table"]
        linkages = surface_payload["source_linkage_table"]
        if len(identities) != 44:
            failures.append("source_identity_count")
        if len(linkages) != 11:
            failures.append("source_linkage_count")
        for row in identities:
            if sha256_file(ROOT / row["declared_path"]) != row["raw_file_sha256"]:
                failures.append(f"raw_hash:{row['source_key']}")
        for link in linkages:
            if link.get("linkage_verified") is not True:
                failures.append("source_linkage")
        posture = blocker_posture(ROOT, surface_payload)
        if posture["blocker_source_count"] != 4 or posture["normalized_blocker_count"] != 0 or posture["all_blocker_sources_agree"] is not True:
            failures.append("blocker_posture")

        draft = read_json(ROOT / DRAFT_JSON)
        draft_payload = draft["draft_binding"]["draft_payload"]
        confirmed = draft_payload["confirmed_decision_record_payload"]
        decision_record_hash = sha256_bytes(canonical_bytes(confirmed))
        if decision_record_hash != draft_payload["decision_record_payload_sha256"]:
            failures.append("decision_record_hash")
        if sha256_bytes(canonical_bytes(draft_payload)) != draft["draft_binding"]["draft_sha256"]:
            failures.append("draft_hash")
        if confirmed["fixture_inventory"]["fixture_ids"] != FIXTURES or confirmed["fixture_inventory"]["fixture_count"] != 10:
            failures.append("fixture_inventory")
        if confirmed["human_rationale_raw"] != RATIONALE or confirmed["human_rationale_normalized"] is not None:
            failures.append("rationale_boundary")
        excluded = confirmed["excluded_authority"]
        if sorted(excluded) != sorted(EXCLUDED_AUTHORITY_KEYS) or any(value != "NOT_AUTHORIZED" for value in excluded.values()):
            failures.append("excluded_authority")
        if confirmed["authority_expiration_requirements"]["confirmed_absolute_expiry_timestamp"] != EXPIRY:
            failures.append("expiry")
        if confirmed["identity_and_integrity_freshness_result"]["freshness_result"] != "PASS" or confirmed["execution_eligibility_freshness_result"]["freshness_result"] != "PASS":
            failures.append("freshness")

        confirmation_surface = read_json(ROOT / CONFIRM_SURFACE_JSON)
        surface_payload2 = confirmation_surface["surface_binding"]["surface_payload"]
        if surface_payload2["canonical_binding"]["draft_canonical_hash"] != draft["draft_binding"]["draft_sha256"]:
            failures.append("surface_draft_hash")
        if surface_payload2["canonical_binding"]["decision_record_payload_hash"] != decision_record_hash:
            failures.append("surface_payload_hash")
        if sha256_bytes(canonical_bytes(surface_payload2)) != confirmation_surface["surface_binding"]["surface_sha256"]:
            failures.append("confirmation_surface_hash")
        if surface_payload2["generic_proceed_maps_to_confirmation"] is not False:
            failures.append("generic_proceed")

        contract = read_json(ROOT / CONTRACT_JSON)
        contract_payload = contract["contract_binding"]["contract_payload"]
        if sha256_bytes(canonical_bytes(contract_payload)) != contract["contract_binding"]["contract_sha256"]:
            failures.append("contract_hash")
        if contract_payload["rules"]["generic_proceed_is_invalid"] is not True:
            failures.append("contract_generic_proceed")

        receipt = read_json(ROOT / PREP_RECEIPT_JSON)
        receipt_payload = receipt["receipt_binding"]["receipt_payload"]
        if sha256_bytes(canonical_bytes(receipt_payload)) != receipt["receipt_binding"]["receipt_sha256"]:
            failures.append("prep_receipt_hash")
        if receipt_payload["negative_probe_count"] != 32 or receipt_payload["negative_probe_expected_rejection_count"] != 32:
            failures.append("negative_probe_count")
        if any(value != "PASS" for value in receipt_payload["P01_P22_statuses"].values()) or sorted(receipt_payload["P01_P22_statuses"]) != sorted(P_CHECKS):
            failures.append("P01_P22")
        if receipt_payload["gate"] != "PREPARE_POST_VS2_D01_POPULATED_RECEIPT_CONFIRMATION_SURFACE_PASS":
            failures.append("prep_gate")

        md_checks = {
            DRAFT_MD: [draft["draft_binding"]["draft_sha256"], decision_record_hash],
            CONFIRM_SURFACE_MD: [decision_record_hash, OPTION, "CONFIRM_D01_RECEIPT_AS_POPULATED", "RETURN_D01_RECEIPT_FOR_MECHANICAL_CORRECTION", "WITHDRAW_D01_DECISION_BEFORE_AUTHORITATIVE_EMISSION"],
            CONTRACT_MD: [contract["contract_binding"]["contract_sha256"], "generic proceed"],
            PREP_RECEIPT_MD: [receipt["receipt_binding"]["receipt_sha256"], "Authoritative receipt emitted: `false`"],
        }
        for path, markers in md_checks.items():
            text = (ROOT / path).read_text(encoding="utf-8")
            for marker in markers:
                if marker not in text:
                    failures.append(f"markdown:{path}:{marker}")

        direct_builder_source = (ROOT / "scripts/build_post_vs2_first_execution_decision_receipt_v0.py").read_text(encoding="utf-8")
        guard_markers = [
            "STOP_POST_VS2_D01_HUMAN_CONFIRMATION_MISSING",
            "receipt = envelope(build_receipt_payload(root, input_path, False))",
            "if args.emit_authoritative:",
            "surface_consumed=false",
            "authority_update_applied=false",
            "execution_authority_present=false",
        ]
        if any(marker not in direct_builder_source for marker in guard_markers):
            failures.append("direct_emit_authoritative_guard_missing")
        if direct_builder_source.find("STOP_POST_VS2_D01_HUMAN_CONFIRMATION_MISSING") > direct_builder_source.find("atomic_pair(root / AUTH_JSON"):
            failures.append("direct_emit_authoritative_guard_after_writer")
        if (ROOT / AUTH_JSON).exists() or (ROOT / AUTH_MD).exists():
            failures.append("authoritative_receipt_created")

        for flag, expected in {
            "authoritative_receipt_emitted": False,
            "confirmation_event_created": False,
            "surface_consumed": False,
            "authority_update_applied": False,
            "execution_authority_present": False,
            "run_id_created": False,
            "execution_source_intake_created": False,
            "fixtures_executed": 0,
            "runtime_receipts_emitted": 0,
            "runtime_reports_emitted": 0,
        }.items():
            if receipt_payload.get(flag) != expected:
                failures.append(f"non_effect:{flag}")
    except Exception as exc:
        failures.append(f"exception:{type(exc).__name__}:{exc}")
    return {
        "verifier_gate": "POST_VS2_D01_POPULATED_RECEIPT_CONFIRMATION_SURFACE_VERIFIER_PASS" if not failures else "POST_VS2_D01_POPULATED_RECEIPT_CONFIRMATION_SURFACE_VERIFIER_FAIL",
        "failures": failures,
        "source_identity_count": 44 if not failures or "source_identity_count" not in failures else None,
        "source_linkage_count": 11 if not failures or "source_linkage_count" not in failures else None,
        "decision_event_id": DECISION_EVENT_ID,
        "prospective_receipt_id": PROSPECTIVE_RECEIPT_ID,
        "authoritative_receipt_emitted": False,
        "surface_consumed": False,
    }


def main() -> int:
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["verifier_gate"].endswith("_PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
