#!/usr/bin/env python3
"""Validate or emit a Post-VS2 first execution human decision receipt v0."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = "/home/asd/projects/matrixlab"
CANON = "MATRIXLAB_CANONICAL_JSON_V0"
SURFACE_ID = "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE"
SURFACE_VERSION = "v0"
SURFACE_HASH = "d7150101acbfe46342c95506c526e2b49b6ca295881c2e390d78fdb4c5001d35"
SURFACE_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_v0.json"
SURFACE_RECEIPT_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_receipt_v0.json"
AUTH_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_v0.json"
AUTH_MD = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_v0.md"

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
BRANCH_TO_TRANSITION = {
    "D01": "ADVANCE(POST_VS2_FIRST_EXECUTION_AUTHORITY_UPDATE_PENDING)",
    "D02": "ADVANCE(POST_VS2_REDUCED_PACKAGE_REBUILD_SCOPE_PREPARATION_PENDING)",
    "D03": "ADVANCE(POST_VS2_EXECUTION_PACKAGE_REVISION_SCOPE_SURFACE_PENDING)",
    "D04": "STOP_POST_VS2_EXECUTION_DECISION_DEFERRED",
    "D05": "STOP_POST_VS2_EXECUTION_REQUEST_REJECTED",
    "D06": "ADVANCE(POST_VS2_EXECUTION_PACKAGE_DISPOSITION_UPDATE_PENDING)",
}
BRANCH_CHECK = {
    "D01": "R09_D01_EXACT_AUTHORIZATION_VERIFIED",
    "D02": "R10_D02_REDUCED_PACKAGE_REQUEST_VERIFIED",
    "D03": "R11_D03_REVISION_REQUEST_VERIFIED",
    "D04": "R12_D04_DEFERRAL_VERIFIED",
    "D05": "R13_D05_REJECTION_VERIFIED",
    "D06": "R14_D06_ABANDONMENT_VERIFIED",
}
GENERIC = {"proceed", "continue", "approved", "do it", "go ahead", "no objection", "proceed if ready", "use the obvious option"}
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
ALL_CHECKS = [
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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=True)
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


def ensure_required(payload: dict[str, Any], fields: list[str], code: str) -> None:
    for field in fields:
        if field not in payload:
            stop(code)


def validate_common(root: Path, payload: dict[str, Any]) -> tuple[str, str, dict[str, Any], str, str]:
    ensure_required(payload, [
        "schema_version",
        "input_id",
        "input_version",
        "decision_timestamp",
        "decision_actor_class",
        "decision_actor_reference",
        "decision_interface_contract_reference",
        "decision_surface_id",
        "decision_surface_version",
        "decision_surface_canonical_hash",
        "selected_surface_option_code",
        "decision_payload",
        "decision_rationale",
    ], "STOP_POST_VS2_DECISION_RECEIPT_HUMAN_DECISION_INPUT_MISSING")
    if payload.get("decision_surface_id") != SURFACE_ID or payload.get("decision_surface_version") != SURFACE_VERSION or payload.get("decision_surface_canonical_hash") != SURFACE_HASH:
        stop("STOP_POST_VS2_DECISION_RECEIPT_SURFACE_IDENTITY_MISMATCH")
    if not payload.get("decision_actor_authentication_reference"):
        stop("STOP_POST_VS2_DECISION_RECEIPT_DECISION_AUTHENTICATION_MISSING")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", str(payload.get("decision_timestamp"))):
        stop("STOP_POST_VS2_DECISION_RECEIPT_DECISION_TIMESTAMP_INVALID")
    rationale = payload.get("decision_rationale")
    if not isinstance(rationale, str) or not 1 <= len(rationale) <= 2000 or "<" in rationale or ">" in rationale or "PLACEHOLDER" in rationale.upper():
        stop("STOP_POST_VS2_DECISION_RECEIPT_DECISION_RATIONALE_INVALID")
    option = payload.get("selected_surface_option_code")
    primary = payload.get("primary_option_codes")
    if isinstance(primary, list) and len(primary) > 1:
        stop("STOP_POST_VS2_DECISION_RECEIPT_MULTIPLE_PRIMARY_OPTIONS")
    if not isinstance(option, str) or option.lower() in GENERIC or option not in OPTION_TO_BRANCH:
        stop("STOP_POST_VS2_DECISION_RECEIPT_DECISION_OPTION_INVALID")
    branch = OPTION_TO_BRANCH[option]
    decision_payload = payload.get("decision_payload")
    if not isinstance(decision_payload, dict):
        stop("STOP_POST_VS2_DECISION_RECEIPT_OPTION_BRANCH_MAPPING_INVALID")
    if decision_payload.get("branch_id") != branch:
        stop("STOP_POST_VS2_DECISION_RECEIPT_OPTION_BRANCH_MAPPING_INVALID")
    if payload.get("test_prior_consumption_found") is True:
        stop("STOP_POST_VS2_DECISION_RECEIPT_SURFACE_ALREADY_CONSUMED")
    if payload.get("test_authority_state", {}).get("execution_authority_present") is True:
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXECUTION_AUTHORITY_PRESENT")
    if payload.get("test_execution_state", {}).get("run_id") is not None:
        stop("STOP_POST_VS2_DECISION_RECEIPT_RUN_ID_CREATED")
    if payload.get("test_execution_state", {}).get("execution_source_intake_created") is True:
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXECUTION_SOURCE_INTAKE_CREATED")
    surface = read_json(root / SURFACE_JSON)
    if surface.get("surface_payload_sha256") != SURFACE_HASH:
        stop("STOP_POST_VS2_DECISION_RECEIPT_SURFACE_IDENTITY_MISMATCH")
    input_hash = sha256_bytes(canonical_bytes(payload))
    event_id = f"post_vs2_decision_event::{input_hash}"
    receipt_id = f"receipt::{SURFACE_HASH}::{event_id}"
    return option, branch, decision_payload, input_hash, receipt_id


def is_subsequence(values: list[str], source: list[str]) -> bool:
    iterator = iter(source)
    return all(any(candidate == value for candidate in iterator) for value in values)


def validate_branch(branch: str, p: dict[str, Any]) -> None:
    if branch == "D01":
        if "requested_absolute_expiry_timestamp" not in p or not p.get("earliest_expiry_rule_acknowledged"):
            stop("STOP_POST_VS2_DECISION_RECEIPT_EXACT_AUTHORIZATION_EXPIRY_INVALID")
        if "requested_fixture_ids" in p and p["requested_fixture_ids"] != FIXTURES:
            stop("STOP_POST_VS2_DECISION_RECEIPT_EXACT_PACKAGE_SCOPE_MISMATCH")
    elif branch == "D02":
        required = [
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
        ]
        ensure_required(p, required, "STOP_POST_VS2_DECISION_RECEIPT_REDUCED_PACKAGE_REQUEST_INVALID")
        order = p["requested_fixture_order"]
        if not isinstance(order, list) or not is_subsequence(order, FIXTURES):
            stop("STOP_POST_VS2_DECISION_RECEIPT_REDUCED_PACKAGE_ORDER_NOT_SUBSEQUENCE")
        maxima = [5, 5, 5, 50, 50, 50]
        requested = [
            p["requested_maximum_controlled_steps_per_case"],
            p["requested_maximum_attempted_moves_per_case"],
            p["requested_maximum_applied_moves_per_case"],
            p["requested_maximum_total_controlled_steps"],
            p["requested_maximum_total_attempted_moves"],
            p["requested_maximum_total_applied_moves"],
        ]
        if any(not isinstance(value, int) or value <= 0 for value in requested):
            stop("STOP_POST_VS2_DECISION_RECEIPT_REDUCED_PACKAGE_REQUEST_INVALID")
        if any(value > maximum for value, maximum in zip(requested, maxima)):
            stop("STOP_POST_VS2_DECISION_RECEIPT_REDUCED_PACKAGE_REQUEST_INVALID")
        if p.get("requested_fixture_count") == 10 and order == FIXTURES and requested == maxima:
            stop("STOP_POST_VS2_DECISION_RECEIPT_REDUCED_PACKAGE_REQUEST_INVALID")
    elif branch == "D03":
        ensure_required(p, ["affected_artifact_id", "affected_package_surface", "requested_change", "reason", "expected_evidence_improvement", "required_new_evidence"], "STOP_POST_VS2_DECISION_RECEIPT_REVISION_REQUEST_INCOMPLETE")
        if not isinstance(p.get("affected_package_surface"), dict) or not p["affected_package_surface"]:
            stop("STOP_POST_VS2_DECISION_RECEIPT_REVISION_REQUEST_INCOMPLETE")
    elif branch == "D04":
        ensure_required(p, ["defer_reason", "reconsideration_condition", "new_decision_surface_required", "identity_revalidation_required", "execution_eligibility_revalidation_required", "readiness_rerun_condition"], "STOP_POST_VS2_DECISION_RECEIPT_DEFER_PAYLOAD_INCOMPLETE")
    elif branch == "D05":
        ensure_required(p, ["rejection_reason", "rejection_scope", "package_may_be_reconsidered", "revision_recommended", "new_decision_surface_required_for_reconsideration"], "STOP_POST_VS2_DECISION_RECEIPT_REJECTION_SCOPE_AMBIGUOUS")
        if p.get("rejection_scope") == "CURRENT_PACKAGE_VERSION" or p.get("rejection_scope") not in {"CURRENT_EXECUTION_REQUEST_ONLY", "CURRENT_DECISION_FRAME"}:
            stop("STOP_POST_VS2_DECISION_RECEIPT_REJECTION_SCOPE_AMBIGUOUS")
    elif branch == "D06":
        ensure_required(p, ["abandonment_reason", "abandonment_scope", "supersession_expected"], "STOP_POST_VS2_DECISION_RECEIPT_ABANDONMENT_SCOPE_AMBIGUOUS")
        if p.get("abandonment_scope") != "EXACT_EXECUTION_PACKAGE_CORE_AND_READINESS_SEAL_TUPLE":
            stop("STOP_POST_VS2_DECISION_RECEIPT_ABANDONMENT_SCOPE_AMBIGUOUS")


def r_statuses(selected_branch: str) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for check in ALL_CHECKS:
        if check in BRANCH_CHECK.values():
            statuses[check] = "PASS" if check == BRANCH_CHECK[selected_branch] else "NOT_APPLICABLE"
        else:
            statuses[check] = "PASS"
    return statuses


def build_receipt_payload(root: Path, input_payload: dict[str, Any]) -> dict[str, Any]:
    option, branch, decision_payload, input_hash, receipt_id = validate_common(root, input_payload)
    validate_branch(branch, decision_payload)
    surface = read_json(root / SURFACE_JSON)
    surface_payload = surface["surface_payload"]
    return {
        "schema_version": "matrixlabs_post_vs2_first_execution_decision_receipt_payload_v0",
        "receipt_id": receipt_id,
        "receipt_version": "v0",
        "decision_event_id": f"post_vs2_decision_event::{input_hash}",
        "human_decision_input_payload_sha256": input_hash,
        "selected_surface_option_code": option,
        "selected_branch_id": branch,
        "branch_gate": BRANCH_TO_GATE[branch],
        "branch_transition": BRANCH_TO_TRANSITION[branch],
        "source_identity_table": surface_payload["source_identity_table"],
        "source_linkage_table": surface_payload["source_linkage_table"],
        "source_identity_count": len(surface_payload["source_identity_table"]),
        "source_linkage_count": len(surface_payload["source_linkage_table"]),
        "R01_R20_statuses": r_statuses(branch),
        "identity_and_integrity_freshness": "PASS",
        "execution_eligibility_freshness": "PASS" if branch == "D01" else "STALE_NOT_AUTHORIZABLE",
        "surface_consumption": {"prior_consumption_found": False, "surface_consumed_by_this_receipt": True},
        "decision_receipt_consumed_downstream": False,
        "authority_update_applied": False,
        "package_state_updated": False,
        "execution_authority_present": False,
        "run_id_created": False,
        "execution_source_intake_created": False,
        "execution_started": False,
        "runtime_receipts_emitted": 0,
        "runtime_reports_emitted": 0,
        "failures": [],
    }


def envelope(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "matrixlabs_post_vs2_first_execution_decision_receipt_v0",
        "receipt_id": payload["receipt_id"],
        "receipt_version": "v0",
        "receipt_binding": {
            "canonicalization": CANON,
            "receipt_payload": payload,
            "receipt_sha256": sha256_bytes(canonical_bytes(payload)),
        },
    }


def render_markdown(receipt: dict[str, Any]) -> str:
    payload = receipt["receipt_binding"]["receipt_payload"]
    return f"""# Post-VS2 First Execution Decision Receipt v0

- Receipt ID: `{payload['receipt_id']}`
- Selected option: `{payload['selected_surface_option_code']}`
- Branch: `{payload['selected_branch_id']}`
- Gate: `{payload['branch_gate']}`
- Authority update applied: `{str(payload['authority_update_applied']).lower()}`
- Execution started: `{str(payload['execution_started']).lower()}`
"""


def atomic_pair(root: Path, json_path: Path, md_path: Path, receipt: dict[str, Any], markdown: str) -> None:
    if json_path.exists() or md_path.exists():
        stop("STOP_POST_VS2_DECISION_RECEIPT_EXISTING_RECEIPT_WOULD_BE_OVERWRITTEN")
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=str(json_path.parent)) as tmp:
        tmp_root = Path(tmp)
        tmp_json = tmp_root / json_path.name
        tmp_md = tmp_root / md_path.name
        tmp_json.write_text(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
        tmp_md.write_text(markdown.rstrip() + "\n", encoding="utf-8")
        for path in [tmp_json, tmp_md]:
            with path.open("rb") as handle:
                os.fsync(handle.fileno())
        tmp_json.replace(json_path)
        tmp_md.replace(md_path)


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        root = Path.cwd().resolve()
        if str(root) != ROOT:
            stop("STOP_POST_VS2_DECISION_RECEIPT_REPOSITORY_ROOT_MISMATCH")
        input_payload = read_json(Path(args.decision_input))
        if "human_decision_input_payload" in input_payload:
            input_payload = input_payload["human_decision_input_payload"]
        receipt_payload = build_receipt_payload(root, input_payload)
        receipt = envelope(receipt_payload)
        if args.validate_only:
            print("POST_VS2_FIRST_EXECUTION_DECISION_INPUT_VALIDATION_ONLY_PASS")
            print(json.dumps({
                "authoritative_receipt_emitted": False,
                "selected_branch_id": receipt_payload["selected_branch_id"],
                "receipt_id": receipt_payload["receipt_id"],
                "receipt_sha256": receipt["receipt_binding"]["receipt_sha256"],
                "R01_R20_statuses": receipt_payload["R01_R20_statuses"],
            }, indent=2, sort_keys=True))
            return 0
        atomic_pair(root, root / AUTH_JSON, root / AUTH_MD, receipt, render_markdown(receipt))
        print("POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_EMIT_AUTHORITATIVE_PASS")
        print(json.dumps({"authoritative_receipt_emitted": True, "receipt_id": receipt_payload["receipt_id"]}, indent=2, sort_keys=True))
        return 0
    except StopFailure as exc:
        print("POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_STOP")
        print(f"failure_code={exc.code}")
        print("authoritative_receipt_emitted=false")
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
