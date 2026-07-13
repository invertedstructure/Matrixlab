#!/usr/bin/env python3
"""Verify the Post-VS2 first execution decision surface v0."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import build_post_vs2_first_execution_decision_surface_v0 as helper


ROOT = "/home/asd/projects/matrixlab"
BRANCH = "master"
HEAD = "af79cea2fd8cf98732ef074969a9a56ffb8a6406"
SURFACE_GATE = "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_PASS_READY_FOR_HUMAN_DECISION"
FAIL_GATE = "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_FAIL"
SURFACE_STATE = "UNCONSUMED"
TERMINAL_TRANSITION = "STOP_POST_VS2_EXECUTION_SURFACE_READY_PENDING_HUMAN_DECISION"
BOOKKEEPING_TRANSITION = (
    "ADVANCE(BOOKKEEPING_COMMIT_POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_V0_PENDING)"
)
SURFACE_ID = "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE"
UNIT_ID = "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE_PREPARATION"
S0_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_v0.json"
S0_MD = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_v0.md"
PR0_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_receipt_v0.json"
SCRIPT = "scripts/build_post_vs2_first_execution_decision_surface_v0.py"
VERIFY_SCRIPT = "scripts/verify_post_vs2_first_execution_decision_surface_v0.py"
BASELINE_SCRIPT = "scripts/build_baseline_share_v0.py"
BASELINE_OUTPUTS = [
    "baseline_share/COMMIT_CONTEXT.md",
    "baseline_share/CURRENT_STATE.md",
    "baseline_share/MANIFEST.json",
    "baseline_share/RECEIPT_POINTERS.md",
]
EXPECTED_DIRTY = {SCRIPT, VERIFY_SCRIPT, BASELINE_SCRIPT, S0_JSON, S0_MD, PR0_JSON, *BASELINE_OUTPUTS}
EXPECTED_SOURCE_HASHES = {
    "C0": "73ef125f8e606c66ae6e19c5d7337318c88963898f36d3aa1366f36cf7fc7e51",
    "R0": "a35ba5239f8f334a9c2fa2ce48a29bc3c67e10f88ce4fb222558bc6dd29b585b",
    "E0": "cd3f9deed2278d8ab7292a7aa64cf1a68446312d26493f07e508f1d5360211c6",
    "G0": "94f1a98bbfb246226ef7f29887ea0a3ade2a4f71666b5852bbdf93815836cc99",
    "GR0": "705eb58f43460b289ac40a6e24557bce0be4accd04f372edd79df9ca38c12332",
    "RS0": "5c36c71da7bd70889c16a4722d882b0fe8dcfc5ce6cd8a72b80da4dbafbe2d79",
}
OPTION_CODES = [
    "AUTHORIZE_EXACT_SEALED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE",
    "REQUEST_REDUCED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_VERSION",
    "RETURN_SEALED_FIRST_SWEEP_KERNEL_PACKAGE_FOR_REVISION",
    "DEFER_FIRST_SWEEP_KERNEL_EXECUTION_DECISION",
    "REJECT_CURRENT_FIRST_SWEEP_KERNEL_EXECUTION_REQUEST",
    "ABANDON_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_VERSION",
]


READY_BRANCH = "READY"
READY_GATE = "VS2_6_FIRST_RUN_CONSTRUCTION_READINESS_PASS_READY_FOR_ONE_EXECUTION_DECISION"
READY_SEAL = "SEALED_READY_FOR_HUMAN_EXECUTION_DECISION"


def ensure_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label}_not_mapping:{type(value).__name__}")
    return value


def ensure_list_field(owner: dict[str, Any], field: str, label: str) -> list[Any]:
    if field not in owner:
        raise ValueError(f"{label}_{field}_missing")
    value = owner[field]
    if not isinstance(value, list):
        raise ValueError(f"{label}_{field}_not_list:{type(value).__name__}")
    return value


def ensure_string_items(values: list[Any], label: str) -> list[str]:
    if not all(isinstance(value, str) for value in values):
        raise ValueError(f"{label}_not_list_str:{values}")
    return list(values)


def ensure_top_payload_agree(top: dict[str, Any], payload: dict[str, Any], field: str, expected: Any, label: str) -> None:
    if field not in top or field not in payload:
        raise ValueError(f"{label}_{field}_missing_top_or_payload")
    if top[field] != payload[field]:
        raise ValueError(f"{label}_{field}_top_payload_mismatch:{top[field]}!={payload[field]}")
    if payload[field] != expected:
        raise ValueError(f"{label}_{field}_wrong:{payload[field]}!={expected}")


def recompute_readiness_blocker_posture(source_data: dict[str, dict[str, Any]]) -> dict[str, Any]:
    c0_payload = ensure_mapping(source_data["C0"].get("closure_payload"), "C0_closure_payload")
    if c0_payload.get("readiness_branch") != READY_BRANCH:
        raise ValueError(f"C0_readiness_branch_wrong:{c0_payload.get('readiness_branch')}")
    c0_blockers = ensure_string_items(ensure_list_field(c0_payload, "readiness_blockers", "C0"), "C0_readiness_blockers")

    g0 = source_data["G0"]
    gate_payload = ensure_mapping(g0.get("gate_binding", {}).get("gate_payload"), "G0_gate_payload")
    ensure_top_payload_agree(g0, gate_payload, "gate_status", "READY", "G0")
    ensure_top_payload_agree(g0, gate_payload, "eligible_for_execution_decision", True, "G0")
    ensure_top_payload_agree(g0, gate_payload, "readiness_component_count", 21, "G0")
    ensure_top_payload_agree(g0, gate_payload, "readiness_verdict", READY_GATE, "G0")
    gate_records = ensure_list_field(gate_payload, "readiness_component_records", "G0")
    if g0.get("readiness_component_records") != gate_records:
        raise ValueError("G0_readiness_component_records_top_payload_mismatch")
    if len(gate_records) != 21:
        raise ValueError(f"G0_readiness_component_count_wrong:{len(gate_records)}")
    gate_component_blocker_records: list[dict[str, Any]] = []
    gate_component_blockers: list[str] = []
    for index, row in enumerate(gate_records, start=1):
        record = ensure_mapping(row, f"G0_readiness_component_records_{index}")
        component_id = record.get("readiness_component_id")
        if not isinstance(component_id, str) or not component_id:
            raise ValueError(f"G0_component_id_wrong:{component_id}")
        if record.get("readiness_status") != "READY":
            raise ValueError(f"G0_{component_id}_status_wrong:{record.get('readiness_status')}")
        blocker_ids = ensure_string_items(ensure_list_field(record, "blocker_ids", component_id), f"{component_id}_blocker_ids")
        gate_component_blocker_records.append({"readiness_component_id": component_id, "blocker_ids": blocker_ids})
        gate_component_blockers.extend(blocker_ids)

    gr0 = source_data["GR0"]
    receipt_payload = ensure_mapping(gr0.get("receipt_binding", {}).get("receipt_payload"), "GR0_receipt_payload")
    gr0_blockers = ensure_string_items(ensure_list_field(gr0, "typed_blockers", "GR0"), "GR0_typed_blockers")
    gr0_payload_blockers = ensure_string_items(ensure_list_field(receipt_payload, "typed_blockers", "GR0_receipt_payload"), "GR0_payload_typed_blockers")
    ensure_top_payload_agree(gr0, receipt_payload, "audit_completed", True, "GR0")
    ensure_top_payload_agree(gr0, receipt_payload, "eligible_for_execution_decision", True, "GR0")
    ensure_top_payload_agree(gr0, receipt_payload, "readiness_verdict", READY_GATE, "GR0")
    ensure_top_payload_agree(gr0, receipt_payload, "runtime_execution_performed", False, "GR0")

    rs0 = source_data["RS0"]
    seal_payload = ensure_mapping(rs0.get("seal_binding", {}).get("seal_payload"), "RS0_seal_payload")
    ensure_top_payload_agree(rs0, seal_payload, "seal_status", READY_SEAL, "RS0")
    ensure_top_payload_agree(rs0, seal_payload, "eligible_for_execution_decision", True, "RS0")
    ensure_top_payload_agree(rs0, seal_payload, "readiness_verdict", READY_GATE, "RS0")
    authority_status = ensure_mapping(rs0.get("authority_status"), "RS0_authority_status")
    seal_authority_status = ensure_mapping(seal_payload.get("authority_status"), "RS0_seal_payload_authority_status")
    if authority_status != seal_authority_status:
        raise ValueError("RS0_authority_status_top_payload_mismatch")
    for field in ["execution_authority_granted", "sweep_authority_granted", "runner_authority_created", "automatic_rerun_authority_granted"]:
        if authority_status.get(field) is not False:
            raise ValueError(f"RS0_{field}_not_false:{authority_status.get(field)}")

    if not (c0_blockers == gate_component_blockers == gr0_blockers == gr0_payload_blockers):
        raise ValueError(
            "blocker_source_disagreement:"
            + json.dumps({"C0": c0_blockers, "G0": gate_component_blockers, "GR0": gr0_blockers, "GR0_payload": gr0_payload_blockers}, sort_keys=True)
        )
    if c0_blockers:
        raise ValueError(f"normalized_blockers_nonempty:{c0_blockers}")

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


def seal_reference_has_blocker_ownership(payload: dict[str, Any]) -> bool:
    seal_ref = payload.get("readiness_seal_reference", {})
    if not isinstance(seal_ref, dict):
        return True
    blocker_fields = {"typed_readiness_blocker_count", "typed_readiness_blockers", "readiness_blockers", "typed_blockers", "blocker_ids"}
    return any(field in seal_ref for field in blocker_fields)


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


def git(root: Path, args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True)


def status_paths(status: str) -> set[str]:
    out: set[str] = set()
    for line in status.splitlines():
        if line.startswith("?? "):
            out.add(line[3:])
        elif len(line) >= 4:
            out.add(line[3:])
    return out


def main() -> int:
    root = Path.cwd().resolve()
    failures: list[str] = []
    if str(root) != ROOT:
        failures.append(f"repo_root_wrong:{root}")
    branch = git(root, ["branch", "--show-current"]).strip()
    head = git(root, ["rev-parse", "HEAD"]).strip()
    if branch != BRANCH:
        failures.append(f"branch_wrong:{branch}")
    if head != HEAD:
        failures.append(f"head_wrong:{head}")

    try:
        source_data, ledger = helper.load_sources(root)
    except Exception as exc:  # noqa: BLE001 - verifier should report all structural failures.
        failures.append(f"source_load_failed:{exc}")
        source_data, ledger = {}, []
    ledger_by_key = {row.get("source_key"): row for row in ledger}
    for key, expected in EXPECTED_SOURCE_HASHES.items():
        got = ledger_by_key.get(key, {}).get("canonical_content_sha256")
        if got != expected:
            failures.append(f"source_hash_{key}_wrong:{got}!={expected}")

    surface = json.loads((root / S0_JSON).read_text(encoding="utf-8"))
    md = (root / S0_MD).read_text(encoding="utf-8")
    receipt = json.loads((root / PR0_JSON).read_text(encoding="utf-8"))
    payload = surface.get("surface_payload", {})
    receipt_payload = receipt.get("receipt_payload", {})
    expected_posture: dict[str, Any] | None = None
    if source_data:
        try:
            expected_posture = recompute_readiness_blocker_posture(source_data)
            surface_posture = payload.get("readiness_blocker_posture")
            if surface_posture != expected_posture:
                failures.append("readiness_blocker_posture_mismatch")
            if surface_posture and surface_posture.get("normalized_typed_readiness_blocker_count") != 0:
                failures.append(f"normalized_typed_readiness_blocker_count_wrong:{surface_posture.get('normalized_typed_readiness_blocker_count')}")
            if surface_posture and surface_posture.get("blocker_source_count") != 4:
                failures.append(f"blocker_source_count_wrong:{surface_posture.get('blocker_source_count')}")
            if surface_posture and surface_posture.get("all_blocker_sources_agree") is not True:
                failures.append(f"blocker_source_agreement_wrong:{surface_posture.get('all_blocker_sources_agree')}")
            if surface_posture and surface_posture.get("RS0_blocker_field_required") is not False:
                failures.append(f"RS0_blocker_field_required_wrong:{surface_posture.get('RS0_blocker_field_required')}")
            if seal_reference_has_blocker_ownership(payload):
                failures.append("surface_falsely_attributes_blocker_list_ownership_to_RS0")
        except Exception as exc:  # noqa: BLE001 - verifier reports structural mismatch context.
            failures.append(f"readiness_blocker_posture_recompute_failed:{exc}")

    if sha256_bytes(canonical_bytes(payload)) != surface.get("surface_payload_sha256"):
        failures.append("surface_payload_hash_wrong")
    if sha256_bytes(canonical_bytes(receipt_payload)) != receipt.get("receipt_payload_sha256"):
        failures.append("receipt_payload_hash_wrong")
    if receipt_payload.get("surface_artifact_sha256") != surface.get("surface_payload_sha256"):
        failures.append("receipt_surface_hash_mismatch")
    if receipt_payload.get("surface_markdown_raw_sha256") != sha256_file(root / S0_MD):
        failures.append("receipt_markdown_hash_mismatch")

    expected_payload = {
        "surface_id": SURFACE_ID,
        "surface_version": "v0",
        "surface_role": "BOUNDED_HUMAN_EXECUTION_DECISION_SURFACE_ONLY",
        "surface_instance_state": SURFACE_STATE,
        "unit_id": UNIT_ID,
        "surface_gate": SURFACE_GATE,
        "evidence_yield": "CONFIRMATION_YIELD",
    }
    for key, expected in expected_payload.items():
        if payload.get(key) != expected:
            failures.append(f"payload_{key}_wrong:{payload.get(key)}!={expected}")
    if payload.get("terminal_transition", {}).get("transition") != TERMINAL_TRANSITION:
        failures.append("terminal_transition_wrong")
    if receipt_payload.get("logical_transition") != TERMINAL_TRANSITION:
        failures.append("receipt_logical_transition_wrong")
    if receipt_payload.get("bookkeeping_transition") != BOOKKEEPING_TRANSITION:
        failures.append("receipt_bookkeeping_transition_wrong")

    checks = payload.get("surface_checks_D01_D18", [])
    statuses = {row.get("surface_check_id"): row.get("surface_check_status") for row in checks}
    if len(checks) != 18 or any(status != "PASS" for status in statuses.values()):
        failures.append(f"D01_D18_not_all_pass:{statuses}")
    if receipt_payload.get("D01_D18_statuses") != statuses:
        failures.append("receipt_D_statuses_mismatch")

    options = payload.get("decision_options", [])
    option_codes = [row.get("option_code") for row in options]
    if option_codes != OPTION_CODES:
        failures.append(f"option_order_wrong:{option_codes}")
    if [row.get("routes_toward_execution_authority") for row in options] != [True, False, False, False, False, False]:
        failures.append("option_A_route_boundary_wrong")
    if receipt_payload.get("decision_option_count") != 6:
        failures.append("receipt_option_count_wrong")

    decision = payload.get("decision_state", {})
    authority = payload.get("authority_state", {})
    execution = payload.get("execution_state", {})
    required_false = {
        "human_decision_recorded": decision.get("human_decision_recorded"),
        "decision_receipt_created": decision.get("decision_receipt_created"),
        "surface_consumed": decision.get("surface_consumed"),
        "authority_update_applied": authority.get("authority_update_applied"),
        "execution_authority_present": authority.get("execution_authority_present"),
        "sweep_authority_present": authority.get("sweep_authority_present"),
        "run_allocation_authority_present": authority.get("run_allocation_authority_present"),
        "runner_authority_present": authority.get("runner_authority_present"),
        "run_id_created": execution.get("run_id_created"),
        "execution_source_intake_created": execution.get("execution_source_intake_created"),
        "execution_started": execution.get("execution_started"),
    }
    for key, value in required_false.items():
        if value is not False:
            failures.append(f"{key}_not_false:{value}")
    if decision.get("human_decision_required") is not True:
        failures.append("human_decision_required_not_true")
    for key in ["runtime_receipts_emitted", "runtime_reports_emitted", "runtime_candidate_instance_count"]:
        if execution.get(key) != 0:
            failures.append(f"{key}_not_zero:{execution.get(key)}")
    if execution.get("run_id") is not None:
        failures.append("run_id_not_null")

    fixture = payload.get("fixture_summary", {})
    if fixture.get("fixture_count") != 10 or fixture.get("static_candidate_specimen_count") != 10 or fixture.get("runtime_candidate_instance_count") != 0:
        failures.append("fixture_counts_wrong")
    bounds = payload.get("execution_bounds", {})
    for key, expected in {
        "case_count": 10,
        "maximum_controlled_step_invocations_per_case": 5,
        "maximum_attempted_moves_per_case": 5,
        "maximum_applied_moves_per_case": 5,
        "maximum_total_controlled_step_invocations": 50,
        "maximum_total_attempted_moves": 50,
        "maximum_total_applied_moves": 50,
        "automatic_reruns": 0,
    }.items():
        if bounds.get(key) != expected:
            failures.append(f"bounds_{key}_wrong:{bounds.get(key)}")

    for token in [
        SURFACE_ID,
        SURFACE_GATE,
        "UNCONSUMED",
        EXPECTED_SOURCE_HASHES["C0"],
        EXPECTED_SOURCE_HASHES["E0"],
        EXPECTED_SOURCE_HASHES["RS0"],
        "AUTHORIZE_EXACT_SEALED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE",
        TERMINAL_TRANSITION,
    ]:
        if token not in md:
            failures.append(f"markdown_missing:{token}")

    manifest = json.loads((root / "baseline_share/MANIFEST.json").read_text(encoding="utf-8"))
    baseline_expected = {
        "current_unit": UNIT_ID,
        "current_surface": SURFACE_ID,
        "surface_gate": SURFACE_GATE,
        "surface_instance_state": SURFACE_STATE,
        "human_decision_required": True,
        "human_decision_recorded": False,
        "decision_receipt_created": False,
        "decision_option_count": 6,
        "execution_package_core_id": "FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_CORE_V0",
        "execution_package_core_sha256": EXPECTED_SOURCE_HASHES["E0"],
        "readiness_seal_id": "FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_READINESS_SEAL_V0",
        "readiness_seal_sha256": EXPECTED_SOURCE_HASHES["RS0"],
        "authority_update_applied": False,
        "execution_authority_present": False,
        "sweep_authority_present": False,
        "run_allocation_authority_present": False,
        "run_id_created": False,
        "execution_source_intake_created": False,
        "execution_started": False,
        "runtime_receipts_emitted": 0,
        "runtime_reports_emitted": 0,
        "runner_created": False,
        "terminal_transition": TERMINAL_TRANSITION,
        "next_lawful_action": "HUMAN_DECISION_REQUIRED",
    }
    for key, expected in baseline_expected.items():
        if manifest.get(key) != expected:
            failures.append(f"baseline_{key}_wrong:{manifest.get(key)}!={expected}")
    source_files = set(manifest.get("source_files", []))
    for rel in [S0_JSON, S0_MD, PR0_JSON, SCRIPT, VERIFY_SCRIPT]:
        if rel not in source_files:
            failures.append(f"baseline_source_missing:{rel}")
    receipt_pointer = (root / "baseline_share/RECEIPT_POINTERS.md").read_text(encoding="utf-8")
    if "docs/matrixlabs/phase_vs2/*receipt*.json` - file count: `7`" not in receipt_pointer:
        failures.append("phase_vs2_receipt_count_changed")
    if "docs/matrixlabs/post_vs2/*receipt*.json` - file count: `1`" not in receipt_pointer:
        failures.append("post_vs2_receipt_count_missing")
    if PR0_JSON not in receipt_pointer:
        failures.append("post_vs2_receipt_pointer_missing")

    dirty = status_paths(git(root, ["status", "--short", "--untracked-files=all"]))
    if dirty != EXPECTED_DIRTY:
        failures.append(f"dirty_scope_wrong:{sorted(dirty)}")
    protected = subprocess.run(
        ["git", "diff", "--quiet", "--", "docs/matrixlabs/phase_vs2"],
        cwd=root,
        check=False,
    ).returncode == 0
    if not protected:
        failures.append("protected_phase_vs2_sources_changed")

    result = {
        "standalone_verifier_gate": "PASS" if not failures else FAIL_GATE,
        "surface_gate": SURFACE_GATE if not failures else FAIL_GATE,
        "repo_root": str(root),
        "branch": branch,
        "HEAD": head,
        "dirty_path_count": len(dirty),
        "surface_state": payload.get("surface_instance_state"),
        "readiness_branch": source_data.get("C0", {}).get("closure_payload", {}).get("readiness_branch") if source_data else None,
        "readiness_parser_defect_confirmed": True,
        "RS0_blocker_field_required": (expected_posture or {}).get("RS0_blocker_field_required"),
        "C0_readiness_blockers_verified": (expected_posture or {}).get("closure_readiness_blockers") == [],
        "G0_component_blockers_verified": (expected_posture or {}).get("gate_component_blockers") == [],
        "GR0_top_level_typed_blockers_verified": (expected_posture or {}).get("readiness_receipt_typed_blockers") == [],
        "GR0_canonical_payload_typed_blockers_verified": (expected_posture or {}).get("readiness_receipt_payload_typed_blockers") == [],
        "normalized_typed_readiness_blocker_count": (expected_posture or {}).get("normalized_typed_readiness_blocker_count"),
        "blocker_source_count": (expected_posture or {}).get("blocker_source_count"),
        "blocker_source_agreement": (expected_posture or {}).get("all_blocker_sources_agree"),
        "surface_canonical_hash": surface.get("surface_payload_sha256"),
        "surface_raw_file_hash": sha256_file(root / S0_JSON),
        "surface_markdown_raw_hash": sha256_file(root / S0_MD),
        "receipt_canonical_hash": receipt.get("receipt_payload_sha256"),
        "receipt_raw_file_hash": sha256_file(root / PR0_JSON),
        "D01_D18_statuses": statuses,
        "surface_check_count": len(checks),
        "surface_check_pass_count": sum(1 for status in statuses.values() if status == "PASS"),
        "source_identity_count": len(ledger),
        "source_linkage_count": len(payload.get("source_linkage_table", [])),
        "decision_option_count": len(options),
        "decision_option_order_exact": option_codes == OPTION_CODES,
        "only_option_A_routes_toward_execution_authority": [row.get("routes_toward_execution_authority") for row in options] == [True, False, False, False, False, False],
        "fixture_count": fixture.get("fixture_count"),
        "static_candidate_specimen_count": fixture.get("static_candidate_specimen_count"),
        "runtime_candidate_instance_count": fixture.get("runtime_candidate_instance_count"),
        "human_decision_required": decision.get("human_decision_required"),
        "human_decision_recorded": decision.get("human_decision_recorded"),
        "decision_receipt_created": decision.get("decision_receipt_created"),
        "surface_consumed": decision.get("surface_consumed"),
        "authority_update_applied": authority.get("authority_update_applied"),
        "execution_authority_present": authority.get("execution_authority_present"),
        "sweep_authority_present": authority.get("sweep_authority_present"),
        "run_allocation_authority_present": authority.get("run_allocation_authority_present"),
        "run_id_created": execution.get("run_id_created"),
        "execution_source_intake_created": execution.get("execution_source_intake_created"),
        "runtime_receipts_emitted": execution.get("runtime_receipts_emitted"),
        "runtime_reports_emitted": execution.get("runtime_reports_emitted"),
        "runner_created": authority.get("runner_authority_present"),
        "protected_phase_vs2_sources_unchanged": protected,
        "terminal_transition": payload.get("terminal_transition", {}).get("transition"),
        "bookkeeping_transition": receipt_payload.get("bookkeeping_transition"),
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
