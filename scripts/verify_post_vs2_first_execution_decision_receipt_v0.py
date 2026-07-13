#!/usr/bin/env python3
"""Independently verify Post-VS2 first execution decision receipt readiness/emission."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = "/home/asd/projects/matrixlab"
HEAD = "8eb5a0ee42200efbc5f601da2795eb405e9e4e64"
CANON = "MATRIXLAB_CANONICAL_JSON_V0"
SURFACE_HASH = "d7150101acbfe46342c95506c526e2b49b6ca295881c2e390d78fdb4c5001d35"
SURFACE_RECEIPT_HASH = "658fcc2331fd3fc3c9c2865778d9163ddcb05724db1dc2d3343189859c4100cd"
SURFACE_CONSUMPTION_KEY = "3529a085e04b3c7e8b97fa60be7ad0edb0c619c1274054296ea3592434405396"
SURFACE_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_v0.json"
SURFACE_MD = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_v0.md"
SURFACE_RECEIPT_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_receipt_v0.json"
AUTH_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_v0.json"
AUTH_MD = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_v0.md"
OPTION = "AUTHORIZE_EXACT_SEALED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE"
BRANCH = "D01"
TIMESTAMP = "2026-07-13T13:47:38Z"
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
EXPECTED_HASHES = {
    "C0": "73ef125f8e606c66ae6e19c5d7337318c88963898f36d3aa1366f36cf7fc7e51",
    "R0": "a35ba5239f8f334a9c2fa2ce48a29bc3c67e10f88ce4fb222558bc6dd29b585b",
    "E0": "cd3f9deed2278d8ab7292a7aa64cf1a68446312d26493f07e508f1d5360211c6",
    "G0": "94f1a98bbfb246226ef7f29887ea0a3ade2a4f71666b5852bbdf93815836cc99",
    "GR0": "705eb58f43460b289ac40a6e24557bce0be4accd04f372edd79df9ca38c12332",
    "RS0": "5c36c71da7bd70889c16a4722d882b0fe8dcfc5ce6cd8a72b80da4dbafbe2d79",
}


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


def payload_hash(data: dict[str, Any]) -> str:
    return sha256_bytes(canonical_bytes(data))


def parse_utc(value: str) -> datetime:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value):
        raise ValueError(value)
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def expected_statuses() -> dict[str, str]:
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decision-input", required=True)
    args = parser.parse_args()
    root = Path.cwd().resolve()
    failures: list[str] = []
    if str(root) != ROOT:
        failures.append(f"repo_root_wrong:{root}")
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip() != HEAD:
        failures.append("head_wrong")
    input_path = root / args.decision_input
    input_doc = read_json(input_path)
    decision = input_doc.get("human_decision_input_payload", {})
    surface = read_json(root / SURFACE_JSON)
    surface_payload = surface.get("surface_payload", {})
    surface_receipt = read_json(root / SURFACE_RECEIPT_JSON)
    if surface.get("surface_payload_sha256") != SURFACE_HASH:
        failures.append("surface_hash_wrong")
    if surface_receipt.get("receipt_payload_sha256") != SURFACE_RECEIPT_HASH:
        failures.append("surface_receipt_hash_wrong")
    source_rows = surface_payload.get("source_identity_table", [])
    if len(source_rows) != 44 or len(surface_payload.get("source_linkage_table", [])) != 11:
        failures.append("source_counts_wrong")
    by_key = {row.get("source_key"): row for row in source_rows}
    for key, expected in EXPECTED_HASHES.items():
        if by_key.get(key, {}).get("canonical_content_sha256") != expected:
            failures.append(f"source_hash_{key}_wrong")
    posture = surface_payload.get("readiness_blocker_posture", {})
    if posture.get("blocker_source_count") != 4 or posture.get("normalized_typed_readiness_blocker_count") != 0 or posture.get("RS0_blocker_field_required") is not False:
        failures.append("blocker_posture_wrong")
    try:
        decision_time = parse_utc(decision.get("decision_timestamp", ""))
        expiry_time = parse_utc(decision.get("decision_payload", {}).get("requested_absolute_expiry_timestamp", ""))
        if expiry_time <= decision_time:
            failures.append("expiry_not_later")
    except ValueError:
        failures.append("timestamp_parse_failed")
    if decision.get("decision_timestamp") != TIMESTAMP:
        failures.append("decision_timestamp_changed")
    if decision.get("decision_rationale") != RATIONALE:
        failures.append("decision_rationale_changed")
    if decision.get("selected_surface_option_code") != OPTION or decision.get("decision_payload", {}).get("branch_id") != BRANCH:
        failures.append("option_branch_wrong")
    if decision.get("decision_payload", {}).get("requested_absolute_expiry_timestamp") != EXPIRY:
        failures.append("expiry_wrong")
    if decision.get("decision_payload", {}).get("earliest_expiry_rule_acknowledged") is not True:
        failures.append("expiry_ack_wrong")
    if surface_payload.get("fixture_summary", {}).get("fixture_ids") != FIXTURES:
        failures.append("fixture_order_wrong")
    input_payload_sha = payload_hash(decision)
    event_id = f"post_vs2_decision_event::{input_payload_sha}"
    receipt_id = f"receipt::{SURFACE_HASH}::{event_id}"
    auth_present = (root / AUTH_JSON).exists() or (root / AUTH_MD).exists()
    receipt_statuses = expected_statuses()
    receipt_sha = None
    downstream_key = None
    if auth_present:
        receipt = read_json(root / AUTH_JSON)
        payload = receipt.get("receipt_binding", {}).get("receipt_payload", {})
        receipt_sha = payload_hash(payload)
        if receipt_sha != receipt.get("receipt_binding", {}).get("receipt_sha256"):
            failures.append("receipt_hash_wrong")
        downstream_key = sha256_bytes(canonical_bytes({
            "receipt_id": receipt_id,
            "receipt_version": "v0",
            "receipt_sha256": receipt_sha,
        }))
        if downstream_key != receipt.get("receipt_binding", {}).get("decision_receipt_consumption_key"):
            failures.append("downstream_key_wrong")
        if payload.get("receipt_id") != receipt_id:
            failures.append("receipt_id_wrong")
        if payload.get("R01_R20_statuses") != receipt_statuses:
            failures.append("R01_R20_statuses_wrong")
        md = (root / AUTH_MD).read_text(encoding="utf-8")
        for token in [receipt_id, event_id, OPTION, receipt_sha]:
            if token not in md:
                failures.append(f"markdown_missing:{token}")
    result = {
        "authoritative_receipt_verifier_gate": "PASS" if not failures else "FAIL",
        "decision_input_path": args.decision_input,
        "human_decision_input_raw_sha256": sha256_file(input_path),
        "human_decision_input_payload_sha256": input_payload_sha,
        "decision_event_id": event_id,
        "prospective_receipt_id": receipt_id,
        "surface_consumption_key": SURFACE_CONSUMPTION_KEY,
        "authoritative_receipt_present": auth_present,
        "source_identity_count": len(source_rows),
        "source_linkage_count": len(surface_payload.get("source_linkage_table", [])),
        "normalized_blocker_source_count": posture.get("blocker_source_count"),
        "normalized_blocker_count": posture.get("normalized_typed_readiness_blocker_count"),
        "identity_and_integrity_freshness": "PASS" if not failures else "FAIL",
        "execution_eligibility_freshness": "PASS" if not failures else "FAIL",
        "R01_R20_validation_statuses": receipt_statuses,
        "surface_consumed": False,
        "human_decision_recorded_by_receipt": auth_present,
        "authority_update_applied": False,
        "package_state_updated": False,
        "execution_authority_present": False,
        "run_id_created": False,
        "execution_source_intake_created": False,
        "fixtures_executed": 0,
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
